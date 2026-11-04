#!/usr/bin/env bash
# Piece 6 of docs/planning/issue100-fixes-plan.md: would raising the unit-test floors in .quality-gates.json,
# as a fifth commit on the composed branch, add conflict regions against the open pull requests?
#   bash docs/planning/issue100-plan-evidence/piece6-floor-trial.sh <composed-ref> <budget-suite-count> <trimmer-suite-count>
# It builds three throwaway commits in the object database (a temporary index, the working tree and every
# ref untouched) on top of <composed-ref>: raise both floors; raise only the budget suite's; raise only the
# trimmer suite's. For each it runs piece-merge-trials.sh and prints the (a) baseline and (b) lines.
# The piece adds no region when every (b) equals its (a). The variants are unreferenced objects; git gc
# removes them. The counts come from the composed tree (python3 tools/test_context_budget.py, ... trim.py).
set -eu
BASE=${1:?usage: piece6-floor-trial.sh <composed-ref> <budget-suite-count> <trimmer-suite-count>}
CB=${2:?budget count}
TR=${3:?trimmer count}
cd "$(git rev-parse --show-toplevel)"
HERE=docs/planning/issue100-plan-evidence
export GIT_AUTHOR_NAME=trial GIT_AUTHOR_EMAIL=trial@example.invalid GIT_AUTHOR_DATE="2026-01-01T00:00:00Z"
export GIT_COMMITTER_NAME=trial GIT_COMMITTER_EMAIL=trial@example.invalid GIT_COMMITTER_DATE="2026-01-01T00:00:00Z"
orig=$(mktemp); trap 'rm -f "$orig" "${idx:-}"' EXIT
git show "$BASE:.quality-gates.json" > "$orig"

variant() {   # variant <label> <raise budget 0|1> <raise trimmer 0|1>: prints the new commit's sha
  local label=$1 rb=$2 rt=$3 new blob tree sha
  new=$(mktemp)
  python3 -I - "$orig" "$new" "$rb" "$rt" "$CB" "$TR" <<'PY'
import json, re, sys
src, dst, rb, rt, cb, tr = sys.argv[1:]
text = open(src, encoding="utf-8").read()
def bump(text, gate, value):
    pat = re.compile(r'("name": "%s",\s*"direction": "min",\s*"threshold": )(\d+)' % re.escape(gate))
    m = pat.search(text)
    if not m: sys.exit("gate not found: " + gate)
    if int(m.group(2)) > int(value): sys.exit("would loosen " + gate)
    return text[:m.start(2)] + str(value) + text[m.end(2):]
if rb == "1": text = bump(text, "context-budget-unit-tests", cb)
if rt == "1": text = bump(text, "trimmer-unit-tests", tr)
json.loads(text)
open(dst, "w", encoding="utf-8").write(text)
PY
  idx=$(mktemp -u)
  blob=$(git hash-object -w "$new")
  GIT_INDEX_FILE=$idx git read-tree "$BASE"
  GIT_INDEX_FILE=$idx git update-index --cacheinfo "100644,$blob,.quality-gates.json"
  tree=$(GIT_INDEX_FILE=$idx git write-tree)
  sha=$(git commit-tree "$tree" -p "$BASE" -m "trial: $label")
  rm -f "$new" "$idx"; idx=
  echo "$sha"
}

echo "composed $(git rev-parse --short "$BASE"); budget-suite floor -> $CB, trimmer-suite floor -> $TR"
for spec in "raise-both 1 1" "raise-budget-only 1 0" "raise-trimmer-only 0 1"; do
  set -- $spec
  sha=$(variant "$1" "$2" "$3")
  echo "== variant $1 ($(git rev-parse --short "$sha")): files changed vs composed: $(git diff --name-only "$BASE" "$sha" | tr '\n' ' ')"
  bash "$HERE/piece-merge-trials.sh" "$sha" 2>&1 | grep -E '^#|\(a\)|\(b\)'
done
