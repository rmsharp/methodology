#!/usr/bin/env bash
# PR2 Part 1 verification (plan section 5, PR2 row): the candidate's Part 1 commit in a CLEAN --no-local clone,
# the quality ratchet's --run (which runs bin/tests.sh and every declared gate), serial.
#   nohup bash docs/planning/pr-composition-evidence/part1-verify.sh <candidate-repo> <commit> &
set -u
SRC=${1:?candidate repository}; COMMIT=${2:?commit}
DST=${3:-$HOME/.cache/pr2-part1-verify}
rm -rf "$DST"
git clone --no-local -q "$SRC" "$DST" || exit 3
cd "$DST" || exit 3
git checkout -q "$COMMIT" || exit 3
git config --unset core.hooksPath 2>/dev/null
echo "verifying $(git rev-parse HEAD) in a clean clone; $(git status --short | wc -l) dirty paths"
python3 starter-kit/quality_ratchet.py --run
echo "ratchet exit $?"
