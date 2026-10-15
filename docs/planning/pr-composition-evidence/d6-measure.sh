#!/usr/bin/env bash
# PR2 Part 2, D6's small commit: the measurements the record quotes. Read-only against the candidate; works in its own clone.
#   bash d6-measure.sh <fork> <fork-rev> <candidate-repo> <commit> <work-dir>
# <candidate-repo> holds <commit> (D6's) on pr2/candidate; <work-dir> is created and removed.
set -u
export PYTHONDONTWRITEBYTECODE=1
FORK=${1:?fork}; REV=${2:?fork rev}; SRC=${3:?candidate repo}; D6=${4:?D6 commit}; W=${5:?work dir}
rm -rf "$W"; git clone --no-local -q "$SRC" "$W" || exit 3
cd "$W" || exit 3
git config --unset core.hooksPath 2>/dev/null
status_line() {  # the runner's row of `context_budget.py --status`, colour stripped, and the exit code read bare
    python3 starter-kit/context_budget.py --status > .status.out 2>&1; rc=$?
    sed 's/\x1b\[[0-9;]*m//g' .status.out | grep -E 'SESSION_RUNNER.md +(≈|[0-9])' | head -1 | sed 's/^ *//'
    echo "    exit $rc; runner $(wc -c < starter-kit/SESSION_RUNNER.md | tr -d ' ') B"
}

echo "## Section 1: the runner's read-set reading (context_budget.py --status) along the candidate, one commit at a time"
echo "(505541c is the layer's parent and equals upstream/main's runner; c8d4375 is the prose layer's first commit)"
for r in 505541c c8d4375 18cda0f ab35e96 "$D6"; do
    git checkout -q "$r" || exit 3
    echo "-- $r $(git log -1 --format=%s | cut -c1-70)"
    status_line
done
rm -f .status.out

echo; echo "## Section 2: the counterfactual, D6 as first answered: the runner's 3E sentence carried too (the fork tip's own text)"
git checkout -q "$D6" || exit 3
python3 - "$FORK" "$REV" <<'PY'
import subprocess, sys
fork, rev = sys.argv[1], sys.argv[2]
tip = subprocess.run(["git", "-C", fork, "show", rev + ":starter-kit/SESSION_RUNNER.md"], capture_output=True, check=True).stdout.decode()
key = "A run that reads unmeasured gates is not a clean one"
new_line = [l for l in tip.splitlines(keepends=True) if key in l]
assert len(new_line) == 1, len(new_line)
prefix = new_line[0].split(" " + key)[0]
text = open("starter-kit/SESSION_RUNNER.md", encoding="utf-8").read()
lines = text.splitlines(keepends=True)
hit = [i for i, l in enumerate(lines) if l.rstrip("\n") == prefix]
assert len(hit) == 1, hit
lines[hit[0]] = new_line[0]
open("starter-kit/SESSION_RUNNER.md", "w", encoding="utf-8").write("".join(lines))
print("applied the tip's 3E line to the candidate's runner: +%d B" % (len(new_line[0].encode()) - len(prefix.encode()) - 1))
PY
status_line
git checkout -q -- starter-kit/SESSION_RUNNER.md; rm -f .status.out

echo; echo "## Section 3: what D6 changes, and what it does not"
git diff --numstat "$D6~1" "$D6" | sed 's/^/  /'
echo "  files in the commit: $(git diff --name-only "$D6~1" "$D6" | wc -l | tr -d ' ')"
echo "  the runner is untouched: $(git diff --quiet "$D6~1" "$D6" -- starter-kit/SESSION_RUNNER.md && echo yes || echo NO)"
echo "  a gate or budget file touched: $(git diff --name-only "$D6~1" "$D6" | grep -c -E '^\.quality-gates\.json$|^\.context-budget\.json$')"

echo; echo "## Section 4: the claims the added text makes about tools, against the candidate at $D6"
echo "  'unmeasured' in bin/check-handoff: $(grep -c -i unmeasured bin/check-handoff) (the clause lint is not carried, so the paragraph keeps upstream's sentence)"
echo "  'unmeasured' printed by quality_ratchet.py (summary line): $(grep -c -E "unmeasured · results" starter-kit/quality_ratchet.py) line(s)"
echo "  'timeout_seconds' declared in quality_ratchet.py: $(grep -c 'timeout_seconds' starter-kit/quality_ratchet.py) mention(s)"
git diff -U0 "$D6~1" "$D6" | grep -E '^\+[^+]' | grep -F 'bin/check-handoff' | sed 's/^/  the checker sentence as shipped: /'

echo; echo "## Section 5: scrub input (a coarse regular expression over the added lines)"
n=$(git diff -U0 "$D6~1" "$D6" | grep -E '^\+[^+]' | wc -l | tr -d ' ')
h=$(git diff -U0 "$D6~1" "$D6" | grep -E '^\+[^+]' | grep -c -i -E 'BL-[0-9]|\bS[0-9]{2,3}\b|docs/planning|\bfork\b|operator|Learning #|PR[0-9]|issue #[0-9]')
echo "  $n added line(s); fork tokens (backlog code, session number, docs/planning, fork, operator, learning, PR number, issue number): $h"
m=$(git log -1 --format=%B "$D6" | grep -c -i -E 'BL-[0-9]|\bS[0-9]{2,3}\b|docs/planning|\bfork\b|operator|Learning #|PR[0-9]|issue #[0-9]')
echo "  the commit message: $m such token(s)"

echo; echo "## Section 6: the layout check and the migration suite's inputs are unchanged"
python3 bin/check-links --layout both > /dev/null 2>&1; echo "  bin/check-links --layout both exit $?"
cd / && rm -rf "$W"
echo "d6-measure done"
