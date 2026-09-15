#!/usr/bin/env bash
# pr82-review-repro.sh -- re-runs every demonstration in docs/planning/pr82-review.md (S169, 2026-09-15).
#
# Usage:  bash docs/planning/pr82-review-repro.sh [REF]
#   REF defaults to upstream/feat/quality-ratchet, PR #82's head branch. The review was written
#   against c84e7d96a76c458586b44cf1947a75f2d14ce66c; the script prints the sha it actually used.
#
# It writes only under a fresh mktemp directory and never touches this repository's working tree.
# Needs git, python3 and bash. Each line prints what it observed beside what the review recorded,
# so a changed result shows without opening the review. Section 8 (tokens) is manual: its
# instrument is the Claude Code Read tool's refusal message, which no script can call.
set -u
REF="${1:-upstream/feat/quality-ratchet}"
REPO="$(git rev-parse --show-toplevel)" || exit 3
SHA="$(git -C "$REPO" rev-parse --verify "${REF}^{commit}")" || { echo "unknown ref: $REF"; exit 3; }
W="$(mktemp -d "${TMPDIR:-/tmp}/pr82-repro.XXXXXX")"
TREE="$W/tree"; mkdir -p "$TREE"
git -C "$REPO" archive "$SHA" | tar -x -C "$TREE" || exit 3
K="$TREE/starter-kit"
echo "PR #82 tree: $SHA (the review: c84e7d96)"
echo "work dir:    $W"

mk() {  # a throwaway repo with the ratchet at its root, where bin/sync installs it
    d="$(mktemp -d "$W/$1.XXXX")"; cd "$d" || exit 3
    git init -q; git config user.email t@t; git config user.name t
    cp "$K/quality_ratchet.py" quality_ratchet.py
}
manifest() {  # one gate "g": floor $1, measured value 5
    printf '{"version":1,"gates":[{"name":"g","direction":"min","threshold":%s,"command":"echo 5","extract":"(\\\\d+)"}]}\n' "$1" > .quality-gates.json
}
chained_hook() {  # the shape PR #82 chains into .githooks/pre-commit: guarded by [ -f manifest ]
    mkdir -p .githooks
    cat > .githooks/pre-commit <<'H'
#!/bin/sh
top=$(git rev-parse --show-toplevel)
if [ -f "$top/.quality-gates.json" ] && [ -f "$top/quality_ratchet.py" ]; then
	python3 "$top/quality_ratchet.py" --precommit || exit $?
fi
H
    chmod +x .githooks/pre-commit; git config core.hooksPath .githooks
}
dashboard() {  # what PR #82's dashboard collects for the repo in $1
    python3 - "$1" "$K" <<'PY'
import sys; sys.dont_write_bytecode = True
from pathlib import Path
sys.path.insert(0, sys.argv[2])
import methodology_dashboard as md
m = md.collect_gate_metrics(Path(sys.argv[1]))
print("    dashboard: declared", m["declared"], "| loosened",
      [(l["kind"], l["from"], l["to"]) for l in m["loosened"]],
      "| coverage_measured_pass", m["coverage_measured_pass"])
PY
}

echo; echo "== 1. Delete the manifest, then re-add it lower (PR #82's chained hook)"
mk delete; chained_hook; manifest 5; git add -A; git commit -q -m "floor 5" >/dev/null
manifest 4; git add .quality-gates.json
git commit -q -m "lower 5->4" >/dev/null 2>&1; echo "  control: lower 5->4                exit $?  (review: 1, refused)"
git commit -q --no-verify -m "lower 5->4, bypassed" >/dev/null; echo "  the same with --no-verify          exit $?  (review: 0)"
git rm -q .quality-gates.json; git commit -q -m "delete the manifest" >/dev/null 2>&1; echo "  delete the manifest                exit $?  (review: 0, passed)"
manifest 1; git add .quality-gates.json; git commit -q -m "re-add at floor 1" >/dev/null 2>&1; echo "  re-add it at floor 1               exit $?  (review: 0, 'first manifest commit')"
dashboard "$d"; echo "    (review: only the 5->4 bypass is reported; 4->1 by delete and re-add is not)"

echo; echo "== 2. The hook install-hook writes: deleting the manifest locks the repository"
mk lockout; manifest 5; git add -A; git commit -q -m base >/dev/null
python3 quality_ratchet.py install-hook >/dev/null
git rm -q .quality-gates.json; git commit -q -m "delete the manifest" >/dev/null 2>&1; echo "  delete the manifest                exit $?  (review: 1)"
git commit -q --no-verify -m "delete, bypassed" >/dev/null; echo "  the same with --no-verify          exit $?  (review: 0)"
echo x > unrelated.txt; git add unrelated.txt
git commit -q -m "an unrelated change" >/dev/null 2>&1; echo "  any later commit                   exit $?  (review: 1, 'no .quality-gates.json found')"

echo; echo "== 3. Count gates measure how many tests exist, not whether they pass or run"
mk counts
cat > t_fail.py <<'P'
import unittest
class T(unittest.TestCase):
    def test_a(self): self.assertTrue(True)
    def test_b(self): self.assertEqual(1, 2)
    def test_c(self): self.assertEqual(1, 3)
unittest.main()
P
cat > t_skip.py <<'P'
import unittest
class T(unittest.TestCase):
    @unittest.skip("x")
    def test_a(self): pass
    @unittest.skip("x")
    def test_b(self): pass
    @unittest.skip("x")
    def test_c(self): pass
unittest.main()
P
cat > .quality-gates.json <<'J'
{"version":1,"gates":[
 {"name":"count, 2 of 3 failing","direction":"min","threshold":3,"command":"python3 t_fail.py","extract":"Ran (\\d+) tests"},
 {"name":"count, all 3 skipped","direction":"min","threshold":3,"command":"python3 t_skip.py","extract":"Ran (\\d+) tests"},
 {"name":"passed floor beside a failure","direction":"min","threshold":134,"command":"printf '== Summary: 134 passed, 1 failed ==\\n'; exit 1","extract":"== Summary: (\\d+) passed"}
]}
J
git add -A; git commit -q -m base >/dev/null
python3 quality_ratchet.py --run --json > run.json; echo "  --run                              exit $?  (review: 0)"
python3 -c "import json; d=json.load(open('run.json')); print('   ', d['summary'], [(g['name'], g['measured'], g['status']) for g in d['gates']])"
echo "    (review: 3 pass, 0 fail -- over two failing tests, three skipped ones, and a failed row)"

echo; echo "== 4. The dashboard's mirror of compare(): a direction flip and a command edit"
python3 - "$K" <<'PY'
import sys; sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
import quality_ratchet as qr, methodology_dashboard as md
old  = {"gates": [{"name": "g", "direction": "min", "threshold": 5, "command": "python3 -m unittest", "extract": r"Ran (\d+) tests"}]}
flip = {"gates": [{"name": "g", "direction": "max", "threshold": 5, "command": "python3 -m unittest", "extract": r"Ran (\d+) tests"}]}
cmd  = {"gates": [{"name": "g", "direction": "min", "threshold": 5, "command": "echo 'Ran 999 tests'", "extract": r"Ran (\d+) tests"}]}
r, w = qr.compare(old, flip); print("  direction flip: the tool refuses", len(r), "| the dashboard reports", md._gate_loosenings(old, flip))
r, w = qr.compare(old, cmd);  print("  command edit:   the tool refuses", len(r), "warns", len(w), "| the dashboard reports", md._gate_loosenings(old, cmd))
PY
echo "    (review: flip refused 1 / reported []; command refused 0, warned 1 / reported [])"

echo; echo "== 5. The dashboard's coverage bonus keys on a gate's name"
mk coverage
printf '%s\n' '{"version":1,"gates":[{"name":"coverage","direction":"min","threshold":90,"command":"echo 100","extract":"(\\d+)"}]}' > .quality-gates.json
git add -A; git commit -q -m base >/dev/null
python3 quality_ratchet.py --run >/dev/null; echo "  --run                              exit $?  (review: 0)"
dashboard "$d"; echo "    (review: coverage_measured_pass True -- 'echo 100' earns the +2)"

echo; echo "== 6. check-handoff's gate-citation lint (D9): shape, not resolution"
d="$(mktemp -d "$W/lint.XXXX")"; cp "$TREE/.quality-gates.json" "$d/"
python3 - "$TREE/HANDOFFS.md" "$d" <<'PY'
import re, sys
s = open(sys.argv[1], encoding="utf-8").read(); d = sys.argv[2]
pat = r"quality_ratchet:\s*\d+/\d+\s+pass"
open(d + "/as-published.md", "w", encoding="utf-8").write(s)
open(d + "/zero-of-nine.md", "w", encoding="utf-8").write(re.sub(pat, "quality_ratchet: 0/9 pass", s, count=1))
open(d + "/no-citation.md", "w", encoding="utf-8").write(re.sub(pat, "no gate run cited", s))
PY
for v in as-published zero-of-nine no-citation; do
    cp "$d/$v.md" "$d/HANDOFFS.md"
    python3 "$TREE/bin/check-handoff" --file "$d/HANDOFFS.md" >/dev/null 2>&1
    echo "  $v: exit $?"
done
echo "    (review: as-published 0, zero-of-nine 0, no-citation 1)"

echo; echo "== 7. install-hook in a fresh clone of the canonical repository (no core.hooksPath)"
d="$(mktemp -d "$W/canonical.XXXX")"; cp -R "$TREE/." "$d/"; cd "$d" || exit 3
git init -q; git config user.email t@t; git config user.name t; git add -A; git commit -q -m base >/dev/null
python3 starter-kit/quality_ratchet.py install-hook >/dev/null; echo "  install-hook                       exit $?  (review: 0)"
git commit --allow-empty -q -m probe >/dev/null 2>&1; echo "  any commit afterwards              exit $?  (review: 1, can't open <root>/quality_ratchet.py)"

echo; echo "== 8. Token measurements -- manual; the instrument is the Read tool's refusal"
T="$W/tok"; mkdir -p "$T"
MAIN="$(git -C "$REPO" rev-parse --verify upstream/main^{commit})"
echo "  upstream/main: $MAIN (the review: 8b4dc2c3)"
for pair in "main:$MAIN" "pr82:$SHA"; do
    k="${pair%%:*}"; r="${pair#*:}"
    git -C "$REPO" show "${r}:CLAUDE.md" > "$T/c.$k"; cat "$T/c.$k" "$T/c.$k" > "$T/claude-$k-x2.md"
    git -C "$REPO" show "${r}:starter-kit/SESSION_RUNNER.md" > "$T/r.$k"
    git -C "$REPO" show "${r}:starter-kit/SAFEGUARDS.md" > "$T/s.$k"
    cat "$T/r.$k" "$T/s.$k" "$T/r.$k" "$T/s.$k" > "$T/pair-$k-x2.md"
    cat "$T/r.$k" "$T/r.$k" > "$T/runner-$k-x2.md"
done
ls -1 "$T"/*-x2.md | sed 's/^/  /'
echo "  Read each file with an explicit limit that spans it (limit 2000). The Read tool refuses with"
echo "  'File content (N tokens) exceeds maximum allowed tokens (25000)'; the file's tokens are N/2."
echo "  The review's N: pair-main 48,555 (the control: it equals the recorded 48,555), pair-pr82 49,683,"
echo "  runner-main 36,955 (a second control), runner-pr82 37,795, claude-main 46,841, claude-pr82 46,965."
