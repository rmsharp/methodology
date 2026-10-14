#!/usr/bin/env bash
# PR2 Part 1, the first measurement (S311): the plan's section 3 reads Part 1 as the 25 files of
# upstream/main..c8b9ddd (ledgers and docs/ left out), "a tree the fork's suite passed", and says whether it is
# green on UPSTREAM's tree is PR2's first measurement. This lays exactly those files over upstream/main and runs the
# shell suite. NOT the candidate: nothing is left out, parametrised or scrubbed. Takes 10 to 20 minutes; serial;
#   nohup bash docs/planning/pr-composition-evidence/part1-literal.sh &
set -u
SRC=$(git rev-parse --show-toplevel) || exit 3
DST=${1:-$HOME/.cache/pr2-part1-literal}
UP=$(git -C "$SRC" rev-parse upstream/main)
BASE=$(git -C "$SRC" rev-parse c8b9ddd)
rm -rf "$DST"
git clone --no-local -q "$SRC" "$DST" || exit 3
cd "$DST" || exit 3
git config --unset core.hooksPath 2>/dev/null
git checkout -q --detach "$UP"
git diff --name-only "$UP" "$BASE" -- . ':(exclude)docs' ':(exclude)CHANGELOG.md' ':(exclude)HANDOFFS.md' \
    ':(exclude)dashboard_history.jsonl' ':(exclude)dashboard.html' | xargs git checkout "$BASE" --
echo "base $(git rev-parse --short "$UP"); overlay $(git rev-parse --short "$BASE"); $(git diff --cached --shortstat)"
bash bin/tests.sh > "$DST.suite.txt" 2>&1
rc=$?
echo "bin/tests.sh exit $rc: $(grep '^== Summary' "$DST.suite.txt")"
echo "failing blocks:"
awk '/^== Test/{t=$0} /FAIL:/{print "  " t}' "$DST.suite.txt" | sort -u | cut -c1-150
echo "the dashboard unit suite alone (a unit suite is ONE check in the shell suite):"
python3 -I tools/test_methodology_dashboard.py 2>&1 | grep -E '^(Ran |FAILED|OK|FAIL: )' | cut -c1-200
exit $rc
