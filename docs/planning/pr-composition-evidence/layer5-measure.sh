#!/usr/bin/env bash
# PR2 Part 2, layer 5 (the dashboard 2.22.0): every measurement the record cites, in one saved run.
#   layer5-measure.sh <fork-repo> <layer-commit> <parent-commit> <source-rev> [<scratch-dir>]
# <fork-repo> holds the candidate's commits as local objects (here: this repository after a forced fetch of
# `pr2/candidate`) and the fork's tip <source-rev> the builder reads. Everything runs in scratch clones under
# <scratch-dir> (default ~/.cache/pr2-layer5-measure); nothing in <fork-repo> is written. Serial.
# Sections: 1 unit suites; 2 the contrast (the layer's test files against the parent's tools); 3 three mutants of
# the layout suite's new lines; 4 the builder reproduces the layer's tree and refuses on one byte of drift;
# 5 the layout-literal scanner; 6 the two open pull requests; 7 the scrub input (a coarse regular expression over
# the layer's added lines). Pass 2 reads `layer-contrast.sh`, `layer-outcomes.py` and `layer5-build.py` beside it.
set -u
FORK=${1:?fork repository}; LAYER=${2:?layer commit}; PARENT=${3:?parent commit}; SRCREV=${4:?source revision}
W=${5:-$HOME/.cache/pr2-layer5-measure}
HERE=$(cd "$(dirname "$0")" && pwd)
rm -rf "$W"; mkdir -p "$W"
clone() { git clone --no-local -q "$FORK" "$1" && git -C "$1" checkout -q "$2" && git -C "$1" config user.name measure && git -C "$1" config user.email m@m; }
clone "$W/new" "$LAYER"; clone "$W/old" "$PARENT"

echo "## Section 1: unit suites"
echo "### the layer's dashboard suite on the layer's dashboard (python3 tools/test_methodology_dashboard.py), $LAYER"
( cd "$W/new" && python3 tools/test_methodology_dashboard.py 2>&1 | grep -E "^(Ran|OK|FAILED)" )
echo "### the candidate BEFORE the layer, its own suite on the old dashboard (2.21.0), $PARENT"
( cd "$W/old" && python3 tools/test_methodology_dashboard.py 2>&1 | grep -E "^(Ran|OK|FAILED)" )
echo "### the layout suite on the layer (python3 tools/test_layout_resolver.py)"
( cd "$W/new" && python3 tools/test_layout_resolver.py 2>&1 | grep -E "^(Ran|OK|FAILED)" )

echo; echo "## Section 2: the contrast (layer-contrast.sh, layer-outcomes.py): the layer's test file run against the PARENT's tools"
for T in tools/test_methodology_dashboard.py tools/test_layout_resolver.py; do
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
if len(set(c) - set(a)) <= 3:
    print("added tests, outcome on the old tool:")
    for t in sorted(set(c) - set(a)):
        print("  %s %s" % (b.get(t), t))
PY
done

echo; echo "## Section 3: three mutants (one at a time on the layer's dashboards, the layout suite run, files restored after each)"
M="$W/new"
runl() { ( cd "$M" && python3 tools/test_layout_resolver.py 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" ); }
restore() { git -C "$M" checkout -q -- starter-kit/methodology_dashboard.py tools/methodology_dashboard.py; echo "  (restored; dirty paths: $(git -C "$M" status --short | wc -l | tr -d ' '))"; }
echo "mutant A (one comment line inside the embedded block, starter-kit copy):"
python3 - "$M" <<'PY'
import sys
p = sys.argv[1] + "/starter-kit/methodology_dashboard.py"; t = open(p, encoding="utf-8").read()
open(p, "w", encoding="utf-8").write(t.replace("# --- layout resolver: BEGIN ---\n", "# --- layout resolver: BEGIN ---\n# mutant\n", 1))
PY
runl; restore
echo "mutant A2 (the same line inside the block of the tools/ twin only):"
python3 - "$M" <<'PY'
import sys
p = sys.argv[1] + "/tools/methodology_dashboard.py"; t = open(p, encoding="utf-8").read()
open(p, "w", encoding="utf-8").write(t.replace("# --- layout resolver: BEGIN ---\n", "# --- layout resolver: BEGIN ---\n# mutant\n", 1))
PY
runl; restore
echo "mutant B (open('CHANGELOG.md') outside the block, starter-kit copy):"
printf "\nX_MUTANT = open('CHANGELOG.md')\n" >> "$M/starter-kit/methodology_dashboard.py"
runl; restore
echo "control (unmutated):"; runl

echo; echo "## Section 4: the builder reproduces the layer's tree, and refuses on one byte of drift"
clone "$W/repro" "$PARENT"
( cd "$W/repro" \
  && python3 "$HERE/layer5-build.py" "$FORK" "$SRCREV" . | tail -1 \
  && python3 "$HERE/layer5-build.py" "$FORK" "$SRCREV" . --dashboard-count "$(cd "$W/new" && python3 tools/test_methodology_dashboard.py 2>&1 | sed -n 's/^Ran \([0-9]*\) tests.*/\1/p')" \
        --layout-count "$(cd "$W/new" && python3 tools/test_layout_resolver.py 2>&1 | sed -n 's/^Ran \([0-9]*\) tests.*/\1/p')" | tail -1 \
  && git add -A && echo "built tree   $(git write-tree | cut -c1-12)" )
echo "layer's tree $(git -C "$W/new" rev-parse "HEAD^{tree}" | cut -c1-12)"
clone "$W/drift" "$PARENT"
printf '\n' >> "$W/drift/starter-kit/methodology_dashboard.py"
git -C "$W/drift" commit -q -am "one byte of drift in the candidate's starter-kit twin"
( cd "$W/drift" && python3 "$HERE/layer5-build.py" "$FORK" "$SRCREV" . 2>&1 | tail -1 | cut -c1-240 )
echo "dirty paths after the refusal: $(git -C "$W/drift" status --short | wc -l | tr -d ' ')"

echo; echo "## Section 5: the layout-literal scanner on the layer (a series, not yet a gate)"
( cd "$W/old" && python3 bin/check-layout-literals | grep -E '^[^ ]+: [0-9]+ sites?$|^check-layout-literals' ) | sed 's/^/parent: /'
( cd "$W/new" && python3 bin/check-layout-literals | grep -E '^[^ ]+: [0-9]+ sites?$|^check-layout-literals' ) | sed 's/^/layer:  /'

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
  printf '%-44s added %5d | BL- %3d | phase %3d | session %3d | docs/planning %3d | learning %3d | FM %3d | plan %3d\n' "$f" \
    "$(wc -l < "$W/added.txt")" \
    "$(grep -cE 'BL-[0-9]+' "$W/added.txt")" "$(grep -cE '\bP[0-9]\b' "$W/added.txt")" "$(grep -cE '\bS[0-9]{2,3}\b' "$W/added.txt")" \
    "$(grep -c 'docs/planning/' "$W/added.txt")" "$(grep -ciE 'learning #' "$W/added.txt")" "$(grep -ciE 'FM #|failure mode #' "$W/added.txt")" \
    "$(grep -ciE "plan [0-9]|plan's|section [0-9]" "$W/added.txt")"
done
echo; echo "layer5-measure done"
