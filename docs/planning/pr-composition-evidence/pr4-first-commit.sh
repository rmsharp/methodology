#!/usr/bin/env bash
# PR4: does the first commit of the series stand alone on upstream's tip? A clean --no-local clone of that commit,
# the shell suite and the gate run, serially, exit codes read bare. About 10 minutes.
#   nohup bash docs/planning/pr-composition-evidence/pr4-first-commit.sh <repo> <commit> <work-dir> > <work-dir>/out.txt 2>&1 &
set -u
SRC=${1:?repository}; C=${2:?commit}; W=${3:?work dir}
rm -rf "$W/clone"; mkdir -p "$W"
git clone --no-local -q "$SRC" "$W/clone" || exit 3
cd "$W/clone" && git checkout -q "$C" && git config --unset core.hooksPath 2>/dev/null
echo "commit $(git rev-parse HEAD), $(git status --short | wc -l | tr -d ' ') dirty paths, parent $(git rev-parse --short HEAD~1), files changed: $(git show --numstat --format= HEAD | wc -l | tr -d ' ')"
bash bin/tests.sh > "$W/suite.txt" 2>&1; echo "suite exit $?"; tail -1 "$W/suite.txt"
python3 starter-kit/quality_ratchet.py --run > "$W/ratchet.txt" 2>&1; echo "ratchet exit $?"
sed 's/\x1b\[[0-9;]*m//g' "$W/ratchet.txt" | grep -E 'quality gates — run'
echo "pr4-first-commit done"
