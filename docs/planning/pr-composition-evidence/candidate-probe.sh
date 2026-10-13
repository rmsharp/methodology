#!/usr/bin/env bash
# Feasibility probe (S308): upstream's tree with this fork's shipped files laid over it, then upstream's own question,
# "does the shell suite pass?". NOT a candidate pull request: nothing was ported, scrubbed or split; it measures how
# portable the fork's files and tests already are.
#
#   bash docs/planning/pr-composition-evidence/candidate-probe.sh [SCRATCH_DIR]
#
# The overlay is every path the fork changed under starter-kit, workstreams, bin, tools, .githooks and the three manuals
# (HOW_TO_USE.md, ITERATIVE_METHODOLOGY.md, FRAMEWORK_APPARATUS.md). It leaves out this repository's own root files
# (CLAUDE.md, README.md, the two JSON configs, the ledgers) and docs/. Takes 10 to 20 minutes; run it serially, never beside
# another suite, and from a launch that survives the terminal:  nohup bash ... &  (the suite is long).
# The scratch directory is a --no-local clone: nothing here touches the working tree.
set -u
SRC=$(git rev-parse --show-toplevel) || exit 3
DST=${1:-$HOME/.cache/pr-candidate-probe}
rm -rf "$DST"
git clone --no-local -q "$SRC" "$DST" || exit 3
cd "$DST" || exit 3
TIP=$(git -C "$SRC" rev-parse HEAD)
UP=$(git -C "$SRC" rev-parse upstream/main)
git checkout -q --detach "$UP"
git checkout "$TIP" -- starter-kit workstreams bin tools .githooks HOW_TO_USE.md ITERATIVE_METHODOLOGY.md FRAMEWORK_APPARATUS.md
git config --unset core.hooksPath 2>/dev/null
echo "base $(git rev-parse --short "$UP") (upstream/main); overlay from $(git rev-parse --short "$TIP"); $(git diff --cached --shortstat)"
bash bin/tests.sh > "$DST.suite.txt" 2>&1
rc=$?
echo "bin/tests.sh exit $rc: $(grep '^== Summary' "$DST.suite.txt")"
echo "failing blocks:"
awk '/^== Test/{t=$0} /FAIL:/{print "  " t}' "$DST.suite.txt" | sort -u | cut -c1-150
exit $rc
