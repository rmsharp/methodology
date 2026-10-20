#!/usr/bin/env bash
# PR2 Part 2 layer verification (plan section 5, PR2 row): one layer's commit in a CLEAN --no-local clone.
# Prints, in order: the commit and its dirty-path count; the changed files against the base (the parent
# commit); the quality ratchet's --run (which runs bin/tests.sh and every declared gate); the layout scanner's
# summary line; the read-set budget's verdict line (context_budget.py --status, read-only); every tracked
# *.verify.sh proof's exit code. Serial. Takes 10 to 30 minutes; run it as
#   nohup bash docs/planning/pr-composition-evidence/layer-verify.sh <candidate-repo> <commit> [<dst>] &
# and wait for its last line (`layer-verify done`). The criterion for each line is the plan's, stated beside it:
#   ratchet exit 0, every gate pass, 0 unmeasured; the scanner's count is a to-do list until the last layer
#   that resolves a tool, and 0 only then; budget exit 0 (no file over a hard ceiling: the runner's 18,900-token
#   read ceiling is the one a layer's prose can cross); every .verify.sh exit equal to the base's.
set -u
SRC=${1:?candidate repository}; COMMIT=${2:?commit}
DST=${3:-$HOME/.cache/pr2-layer-verify}
rm -rf "$DST"
git clone --no-local -q "$SRC" "$DST" || exit 3
cd "$DST" || exit 3
git checkout -q "$COMMIT" || exit 3
git config --unset core.hooksPath 2>/dev/null
echo "verifying $(git rev-parse HEAD) in a clean clone; $(git status --short | wc -l | tr -d ' ') dirty paths"
echo "changed against its parent $(git rev-parse --short HEAD~1):"
git diff --numstat HEAD~1 HEAD | sed 's/^/  /'
python3 starter-kit/quality_ratchet.py --run
echo "ratchet exit $?"
if [ -x bin/check-layout-literals ]; then
    python3 bin/check-layout-literals | tail -1
    echo "scanner exit ${PIPESTATUS[0]}"
fi
python3 starter-kit/context_budget.py --status | grep -E 'over budget|exceeds'
echo "budget exit ${PIPESTATUS[0]}"
for proof in $(git ls-files '*.verify.sh'); do
    bash "$proof" > /dev/null 2>&1
    echo "proof $proof exit $?"
done
echo "layer-verify done"
