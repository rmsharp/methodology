#!/usr/bin/env bash
# PR2 Part 2, layer 6 (the sync layers): every measurement the record cites, in one saved run.
#   layer6-measure.sh <fork-repo> <layer-commit> <parent-commit> <source-rev> [<scratch-dir>]
# <fork-repo> holds the candidate's commits as local objects (here: this repository after a forced fetch of
# `pr2/candidate`) and the fork's tip <source-rev> the builder reads. <parent-commit> is layer 5's `dd581fe`;
# <layer-commit> is the layer's LAST commit (the layer is three: prep, tools, suite). Everything runs in scratch clones
# under <scratch-dir> (default ~/.cache/pr2-layer6-measure); nothing in <fork-repo> is written. Serial.
# Sections: 1 unit suites; 2 the contrast (the layer's test files against the parent's tools); 3 mutants (one at a
# time, files restored after each); 4 the builder reproduces the layer's tree and refuses on one byte of drift;
# 5 the layout-literal scanner; 6 the two open pull requests; 7 the scrub input; 8 the changed files.
# Reads `layer-contrast.sh`, `layer-outcomes.py` and `layer6-build.py` beside it.
set -u
FORK=${1:?fork repository}; LAYER=${2:?layer commit}; PARENT=${3:?parent commit}; SRCREV=${4:?source revision}
W=${5:-$HOME/.cache/pr2-layer6-measure}
HERE=$(cd "$(dirname "$0")" && pwd)
rm -rf "$W"; mkdir -p "$W"
clone() { git clone --no-local -q "$FORK" "$1" && git -C "$1" checkout -q "$2" && git -C "$1" config user.name measure && git -C "$1" config user.email m@m && git -C "$1" config --unset core.hooksPath 2>/dev/null; return 0; }
count() { sed -n 's/^Ran \([0-9]*\) tests.*/\1/p'; }
clone "$W/new" "$LAYER"; clone "$W/old" "$PARENT"

echo "## Section 1: unit suites"
echo "### the sync layer's suite on the layer (python3 tools/test_sync_layouts.py), $LAYER"
( cd "$W/new" && python3 -B tools/test_sync_layouts.py 2>&1 | grep -E "^(Ran|OK|FAILED)" )
echo "### the layout suite on the layer (python3 tools/test_layout_resolver.py)"
( cd "$W/new" && python3 -B tools/test_layout_resolver.py 2>&1 | grep -E "^(Ran|OK|FAILED)" )
echo "### the layout suite on the parent, $PARENT"
( cd "$W/old" && python3 -B tools/test_layout_resolver.py 2>&1 | grep -E "^(Ran|OK|FAILED)" )
echo "### the sync suite exists at the parent? $(git -C "$W/old" cat-file -e "HEAD:tools/test_sync_layouts.py" 2>/dev/null && echo yes || echo no)"

echo; echo "## Section 2: the contrast (layer-contrast.sh, layer-outcomes.py): the layer's test file run against the PARENT's tools"
for T in tools/test_sync_layouts.py tools/test_layout_resolver.py; do
  clone "$W/old-$(basename "$T" .py)" "$PARENT"
  echo "### $T"
  bash "$HERE/layer-contrast.sh" "$W/old-$(basename "$T" .py)" "$W/new" "$T" "$W/out-$(basename "$T" .py)" 2>&1
  python3 - "$W/out-$(basename "$T" .py)" <<'PY'
import sys
out = sys.argv[1]
def load(n):
    return dict(l.rsplit(" ", 1) for l in open("%s/%s" % (out, n)).read().splitlines() if l)
a, b, c = load("old-on-old.txt"), load("new-on-old.txt"), load("new-on-new.txt")
print("old tests that fail on the old tool with the new file:")
for t in sorted(a):
    if b.get(t) == "bad":
        print("  bad " + t)
added = sorted(set(c) - set(a))
if len(added) <= 3:
    print("added tests, outcome on the old tool:")
    for t in added:
        print("  %s %s" % (b.get(t), t))
PY
done

echo; echo "## Section 3: mutants (one at a time on the layer's tree; the named suite run; files restored after each)"
M="$W/new"
runs() { ( cd "$M" && python3 -B "$1" 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | head -8 ); }
restore() { git -C "$M" checkout -q -- . ; echo "  (restored; dirty paths: $(git -C "$M" status --short | wc -l | tr -d ' '))"; }
mut() { # $1 label, $2 file, $3 python expression on s, $4... the suites to run
  echo "mutant $1:"
  python3 - "$M/$2" "$3" <<'PY'
import sys
p, expr = sys.argv[1], sys.argv[2]
s = open(p, encoding="utf-8").read()
t = eval(expr)
if t == s:
    sys.exit("mutant did not apply")
open(p, "w", encoding="utf-8").write(t)
PY
  if [ $? -eq 0 ]; then for suite in "${@:4}"; do echo " [$suite]"; runs "$suite"; done; fi; restore
}
mut "A (one comment line inside bin/sync's embedded resolver block)" bin/sync \
    's.replace("# --- layout resolver: BEGIN ---\n", "# --- layout resolver: BEGIN ---\n# mutant\n", 1)' tools/test_layout_resolver.py
mut "B (a root literal outside the block in bin/status)" bin/status \
    's + "\nX_MUTANT = open(\"CHANGELOG.md\")\n"' tools/test_sync_layouts.py
mut "C (the scanner no longer skips the two left-out checkers)" bin/check-layout-literals \
    's.replace("    \"bin/check-handoff\":", "    \"bin/x-check-handoff\":", 1).replace("    \"bin/check-ledger\":", "    \"bin/x-check-ledger\":", 1)' tools/test_sync_layouts.py tools/test_layout_resolver.py
mut "D1 (bin/sync no longer refuses a project asked for the other layout)" bin/sync \
    's.replace("    if have and have != requested:\n", "    if False:\n", 1)' tools/test_sync_layouts.py
mut "D2 (bin/sync no longer refuses a half-migrated project)" bin/sync \
    's.replace("    if kind == \"half\":\n", "    if False:\n", 1)' tools/test_sync_layouts.py
echo "control (unmutated, the sync suite):"; runs tools/test_sync_layouts.py

echo; echo "## Section 4: the builder reproduces the layer's tree, and refuses on one byte of drift"
clone "$W/repro" "$PARENT"
LAYER_SYNC=$(cd "$W/new" && python3 -B tools/test_sync_layouts.py 2>&1 | count)
LAYER_LAYOUT=$(cd "$W/new" && python3 -B tools/test_layout_resolver.py 2>&1 | count)
LAYER_PASSED=$(git -C "$FORK" show "$LAYER:.quality-gates.json" | python3 -c 'import json,sys; print([g for g in json.load(sys.stdin)["gates"] if g["name"]=="tests-sh-passed"][0]["threshold"])')
( cd "$W/repro" \
  && python3 "$HERE/layer6-build.py" "$FORK" "$SRCREV" . --stage prep | tail -1 && git add -A && git -c commit.gpgsign=false commit -q -m prep \
  && python3 "$HERE/layer6-build.py" "$FORK" "$SRCREV" . --stage tools | tail -1 && git add -A && git -c commit.gpgsign=false commit -q -m tools \
  && python3 "$HERE/layer6-build.py" "$FORK" "$SRCREV" . --stage suite | tail -1 \
  && python3 "$HERE/layer6-build.py" "$FORK" "$SRCREV" . --stage suite --sync-count "$LAYER_SYNC" --passed "$LAYER_PASSED" --layout-count "$LAYER_LAYOUT" | tail -1 \
  && git add -A && echo "built tree   $(git write-tree | cut -c1-12)" )
echo "layer's tree $(git -C "$W/new" rev-parse "HEAD^{tree}" | cut -c1-12)"
clone "$W/drift" "$PARENT"
printf '\n' >> "$W/drift/bin/sync"
git -C "$W/drift" commit -q -am "one byte of drift in the candidate's bin/sync"
( cd "$W/drift" && python3 "$HERE/layer6-build.py" "$FORK" "$SRCREV" . --stage tools 2>&1 | tail -1 | cut -c1-240 )
echo "dirty paths after the refusal: $(git -C "$W/drift" status --short | wc -l | tr -d ' ')"

echo; echo "## Section 5: the layout-literal scanner on the layer (a series; a gate at 0 from the layer on)"
( cd "$W/old" && python3 bin/check-layout-literals | grep -E '^[^ ]+: [0-9]+ sites?$|^check-layout-literals' ) | sed 's/^/parent: /'
( cd "$W/new" && python3 bin/check-layout-literals | grep -E '^[^ ]+: [0-9]+ sites?$|^not scanned|^check-layout-literals' ) | sed 's/^/layer:  /'
( cd "$W/new" && python3 bin/check-layout-literals >/dev/null; echo "layer:  scanner exit $?" )

echo; echo "## Section 6: the two open pull requests (git merge-tree --write-tree; exit 0 clean, 1 conflicts)"
for n in 94 92; do
  sha=$(gh pr view "$n" --repo KJ5HST/methodology --json headRefOid --jq .headRefOid)
  git -C "$FORK" cat-file -e "$sha^{commit}" 2>/dev/null || git -C "$FORK" fetch -q upstream "pull/$n/head"
  echo "#$n head ${sha:0:12}"
  for tip in "$PARENT" "$LAYER"; do
    out=$(git -C "$FORK" merge-tree --write-tree --name-only "$tip" "$sha" 2>&1); rc=$?
    first=$(printf '%s\n' "$out" | head -1)
    echo "== tip ${tip:0:7} against #$n: exit $rc (first line $(printf '%s' "$first" | grep -qE '^[0-9a-f]{40}$' && echo 'is a tree' || echo "IS NOT A TREE: $first"))"
    if [ "$rc" -eq 1 ]; then
      for f in $(printf '%s\n' "$out" | sed -n '2,/^$/p' | grep -v '^$'); do
        echo "   $f: $(git -C "$FORK" show "$first:$f" | grep -c '^<<<<<<<') conflict region(s)"
      done
    fi
  done
done

echo; echo "## Section 7: scrub input (a coarse regular expression over the layer's added lines, per file; the scrub is its own commit after the layers)"
for f in $(git -C "$W/new" diff --name-only "$PARENT" "$LAYER"); do
  git -C "$W/new" diff "$PARENT" "$LAYER" -- "$f" | grep -E '^\+' | grep -vE '^\+\+\+' > "$W/added.txt"
  printf '%-36s added %5d | BL- %3d | phase %3d | session %3d | docs/planning %3d | learning %3d | FM %3d | plan %3d\n' "$f" \
    "$(wc -l < "$W/added.txt")" \
    "$(grep -cE 'BL-[0-9]+' "$W/added.txt")" "$(grep -cE '\bP[0-9]\b' "$W/added.txt")" "$(grep -cE '\bS[0-9]{2,3}\b' "$W/added.txt")" \
    "$(grep -c 'docs/planning/' "$W/added.txt")" "$(grep -ciE 'learning #' "$W/added.txt")" "$(grep -ciE 'FM #|failure mode #' "$W/added.txt")" \
    "$(grep -ciE "plan [0-9]|plan's|section [0-9]|plan C[0-9]|plan D[0-9]" "$W/added.txt")"
done

echo; echo "## Section 8: the changed files, per commit and in all (git diff --numstat), and the layer's size"
git -C "$W/new" log --format='%h %s' "$PARENT..$LAYER" | cut -c1-150
for c in $(git -C "$W/new" rev-list --reverse "$PARENT..$LAYER"); do
  echo "commit $(git -C "$W/new" rev-parse --short "$c"): $(git -C "$W/new" diff --name-only "$c~1" "$c" | wc -l | tr -d ' ') files"
done
git -C "$W/new" diff --numstat "$PARENT" "$LAYER" | awk '{a+=$1; d+=$2; printf "  %6s %6s  %s\n",$1,$2,$3} END {printf "  all: %d files, +%d / -%d\n", NR, a, d}'
echo; echo "layer6-measure done"
