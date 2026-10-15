#!/usr/bin/env bash
# PR2 Part 2, the checkers' layer: the measurements the record cites that the other scripts do not print, in one saved run.
#   layer6b-measure.sh <fork-repo> <layer-commit> <parent-commit> <source-rev> <scratch-dir>
# <fork-repo> holds the candidate's commits as local objects (this repository after a forced fetch of `pr2/candidate`) and the
# fork's tip <source-rev> the builder reads. <parent-commit> is layer 6's `0aa1897`; <layer-commit> is the layer's LAST commit
# (the layer is two: the tools, then the suite). Everything runs in scratch clones under <scratch-dir>; nothing in <fork-repo>
# is written. Serial. The contrast, the mutants, the probe and the real-corpus check have their own scripts and outputs:
# layer-contrast.sh (+ layer-outcomes.py), layer6b-mutate.py, layer6b-probe.sh, layer6b-realtree.sh.
# Sections: 1 unit suites; 2 the builder reproduces the layer's tree and refuses on drift; 3 the layout-literal scanner;
# 4 the two open pull requests; 5 the scrub input; 6 the changed files and the candidate's size against upstream.
set -u
FORK=${1:?fork repository}; LAYER=${2:?layer commit}; PARENT=${3:?parent commit}; SRCREV=${4:?source revision}; W=${5:?scratch dir}/layer6b-measure
HERE=$(cd "$(dirname "$0")" && pwd)
rm -rf "$W"; mkdir -p "$W"
clone() { git clone --no-local -q "$FORK" "$1" && git -C "$1" checkout -q "$2" && git -C "$1" config user.name measure && git -C "$1" config user.email m@m && git -C "$1" config --unset core.hooksPath 2>/dev/null; return 0; }
clone "$W/new" "$LAYER"; clone "$W/old" "$PARENT"

echo "## Section 1: unit suites"
echo "### the checkers' suite on the layer (python3 tools/test_checker_layouts.py), $LAYER"
( cd "$W/new" && python3 -B tools/test_checker_layouts.py 2>&1 | grep -E "^(Ran|OK|FAILED)" )
echo "### the layout suite on the layer / on the parent (python3 tools/test_layout_resolver.py)"
( cd "$W/new" && python3 -B tools/test_layout_resolver.py 2>&1 | grep -E "^(Ran|OK|FAILED)" | tr '\n' ' '; echo )
( cd "$W/old" && python3 -B tools/test_layout_resolver.py 2>&1 | grep -E "^(Ran|OK|FAILED)" | tr '\n' ' '; echo )
echo "### the checkers' suite exists at the parent? $(git -C "$W/old" cat-file -e "HEAD:tools/test_checker_layouts.py" 2>/dev/null && echo yes || echo no)"

echo; echo "## Section 2: the builder reproduces the layer's tree, and refuses on drift"
clone "$W/repro" "$PARENT"
CHK=$(cd "$W/new" && python3 -B tools/test_checker_layouts.py 2>&1 | sed -n 's/^Ran \([0-9]*\) tests.*/\1/p')
PASSED=$(git -C "$FORK" show "$LAYER:.quality-gates.json" | python3 -c 'import json,sys; print([g for g in json.load(sys.stdin)["gates"] if g["name"]=="tests-sh-passed"][0]["threshold"])')
( cd "$W/repro" \
  && python3 "$HERE/layer6b-build.py" "$FORK" "$SRCREV" . --stage tools | tail -1 && git add -A && git -c commit.gpgsign=false commit -q -m tools \
  && python3 "$HERE/layer6b-build.py" "$FORK" "$SRCREV" . --stage suite | tail -1 \
  && python3 "$HERE/layer6b-build.py" "$FORK" "$SRCREV" . --stage suite --checker-count "$CHK" --passed "$PASSED" | tail -1 \
  && git add -A && echo "built tree   $(git write-tree | cut -c1-12)" )
echo "layer's tree $(git -C "$W/new" rev-parse "HEAD^{tree}" | cut -c1-12)"
clone "$W/drift" "$PARENT"
printf '\n' >> "$W/drift/bin/check-handoff"
git -C "$W/drift" commit -q -am "one byte of drift in the candidate's bin/check-handoff"
( cd "$W/drift" && python3 "$HERE/layer6b-build.py" "$FORK" "$SRCREV" . --stage tools 2>&1 | tail -1 | cut -c1-240 )
echo "dirty paths after the refusal: $(git -C "$W/drift" status --short | wc -l | tr -d ' ')"

echo; echo "## Section 3: the layout-literal scanner on the layer (a series: it read 14 sites in 14 files at layer 5, 0 sites in 12 files at layer 6)"
( cd "$W/old" && python3 -B - <<'PY'
import importlib.machinery, importlib.util, sys
sys.dont_write_bytecode = True
loader = importlib.machinery.SourceFileLoader("cll", "bin/check-layout-literals")
cll = importlib.util.module_from_spec(importlib.util.spec_from_loader("cll", loader)); loader.exec_module(cll)
for rel in ("bin/check-handoff", "bin/check-ledger"):
    sites, acked, prose, problems = cll.scan_text(rel, open(rel, encoding="utf-8").read())
    print("parent, %s read by hand (the parent's scanner exempts it): %d sites, %d acknowledged" % (rel, len(sites), len(acked)))
PY
)
( cd "$W/new" && python3 bin/check-layout-literals | grep -E '^check-layout-literals' | sed 's/^/layer:  /' )
( cd "$W/new" && python3 bin/check-layout-literals >/dev/null; echo "layer:  scanner exit $?" )
( cd "$W/new" && python3 -B - <<'PY'
import importlib.machinery, importlib.util, sys
sys.dont_write_bytecode = True
loader = importlib.machinery.SourceFileLoader("cll", "bin/check-layout-literals")
cll = importlib.util.module_from_spec(importlib.util.spec_from_loader("cll", loader)); loader.exec_module(cll)
r = cll.scan_root(__import__("pathlib").Path("."))
print("layer:  exempt from the scan:", sorted(r["not_scanned"]))
PY
)

echo; echo "## Section 4: the two open pull requests (git merge-tree --write-tree; exit 0 clean, 1 conflicts)"
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

echo; echo "## Section 5: scrub input (a coarse regular expression over the layer's added lines, per file; the scrub is its own commit after the layers)"
for f in $(git -C "$W/new" diff --name-only "$PARENT" "$LAYER"); do
  git -C "$W/new" diff "$PARENT" "$LAYER" -- "$f" | grep -E '^\+' | grep -vE '^\+\+\+' > "$W/added.txt"
  printf '%-36s added %5d | BL- %3d | phase %3d | session %3d | docs/planning %3d | learning %3d | FM %3d | plan %3d\n' "$f" \
    "$(wc -l < "$W/added.txt")" \
    "$(grep -cE 'BL-[0-9]+' "$W/added.txt")" "$(grep -cE '\bP[0-9]\b' "$W/added.txt")" "$(grep -cE '\bS[0-9]{2,3}\b' "$W/added.txt")" \
    "$(grep -c 'docs/planning/' "$W/added.txt")" "$(grep -ciE 'learning #' "$W/added.txt")" "$(grep -ciE 'FM #|failure mode #' "$W/added.txt")" \
    "$(grep -ciE "plan [0-9]|plan's|section [0-9]|plan C[0-9]|plan D[0-9]" "$W/added.txt")"
done

echo; echo "## Section 6: the changed files, per commit and in all (git diff --numstat), and the candidate against upstream"
git -C "$W/new" log --format='%h %s' "$PARENT..$LAYER" | cut -c1-150
for c in $(git -C "$W/new" rev-list --reverse "$PARENT..$LAYER"); do
  echo "commit $(git -C "$W/new" rev-parse --short "$c"): $(git -C "$W/new" diff --name-only "$c~1" "$c" | wc -l | tr -d ' ') files"
done
git -C "$W/new" diff --numstat "$PARENT" "$LAYER" | awk '{a+=$1; d+=$2; printf "  %6s %6s  %s\n",$1,$2,$3} END {printf "  all: %d files, +%d / -%d\n", NR, a, d}'
UP=$(git -C "$FORK" rev-parse --short upstream/main)
echo "the candidate $(git -C "$W/new" rev-parse --short HEAD) against upstream/main $UP: $(git -C "$W/new" rev-list --count "$UP..HEAD" 2>/dev/null || git -C "$FORK" rev-list --count "upstream/main..$LAYER") commits; $(git -C "$FORK" diff --shortstat upstream/main "$LAYER")"
echo; echo "layer6b-measure done"
