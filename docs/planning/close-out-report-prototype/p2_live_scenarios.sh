#!/bin/bash
# BL-79 P2 (S254): the plan's four real-harness scenarios (decision-table rows 1, 2, 5, 6) for
# starter-kit/close_out_report.py --hook, on the real Claude Code harness.
#
#   bash docs/planning/close-out-report-prototype/p2_live_scenarios.sh              # spends: about $0.11 on haiku
#   SETUP_ONLY=1 bash docs/planning/close-out-report-prototype/p2_live_scenarios.sh  # builds the fixtures, spends nothing
#
# Scratch repos live OUTSIDE this repository (SCRATCH, default a fresh mktemp dir); the hook snippet is the one
# in the plan's section 4 P2, installed in the scratch repo's own .claude/settings.local.json, never this one's.
# The fixture ledger comes from the COMMITTED test constant, not a working tree (EVIDENCE.md: a live fixture
# copied from an already-completed tree proves nothing). Each `claude -p` call is capped at $0.15.
# The first run (2026-10-03, claude 2.1.288, haiku) used an in-session copy of this script that differed only in
# how REPO, SCRATCH and the tool's source were found.
set -u
REPO=$(git rev-parse --show-toplevel)
S=${SCRATCH:-$(mktemp -d)}
mkdir -p "$S"
echo "scratch: $S"

mk() {  # mk DIR: a git repo with a pending newest receipt, the tool, the hook snippet, two scripts
  d=$1; mkdir -p "$d/starter-kit" "$d/.claude"
  git -C "$REPO" show HEAD:starter-kit/close_out_report.py > "$d/starter-kit/close_out_report.py"
  (cd "$REPO/tools" && python3 -c "
import sys; sys.dont_write_bytecode = True
import test_close_out_report as T
open('$d/HANDOFFS.md', 'w').write(T.LEDGER.format(status='pending'))")
  cat > "$d/.claude/settings.local.json" <<'EOF'
{"hooks": {
  "SessionStart": [{"hooks": [{"type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR\"/starter-kit/close_out_report.py --hook"}]}],
  "Stop":         [{"hooks": [{"type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR\"/starter-kit/close_out_report.py --hook"}]}]
}}
EOF
  printf '#!/bin/sh\nsed -i "" "s/^status: pending/status: complete/" HANDOFFS.md\ngit commit -qam close-out\n' > "$d/close.sh"
  printf '#!/bin/sh\necho x > later.txt\ngit add later.txt\ngit commit -qm later\n' > "$d/later.sh"
  (cd "$d" && git init -q . && git config user.email t@e.com && git config user.name T && git config commit.gpgsign false \
     && echo ".claude/" >> .git/info/exclude && git add -A && git commit -qm "claim: S2 pending")
}
run() {  # run DIR OUTFILE ARGS...
  d=$1; out=$2; shift 2
  (cd "$d" && timeout 240 claude -p --model haiku --output-format json --allowedTools Bash --max-budget-usd 0.15 "$@" > "$out" 2> "$out.err")
  echo "  exit=$? -> $(basename "$out")"
}

mk "$S/r1"; mk "$S/r2"
[ -n "${SETUP_ONLY:-}" ] && { echo "setup only: fixtures built, nothing run"; exit 0; }

echo "== row 1: receipt still pending, plain reply (expect: no block, no log)"
run "$S/r1" "$S/r1.t1.json" "Reply with exactly one word: hello"

echo "== row 2: close-out done, final message 'Done.' (expect: one block, then a clean report)"
run "$S/r2" "$S/r2.t1.json" "Run exactly this shell command: sh close.sh   Then reply with exactly: Done."
echo "== row 5: a later turn, nothing changed (expect: allowed, no second report)"
run "$S/r2" "$S/r2.t2.json" --continue "Reply with exactly: thanks"
echo "== row 6: a commit after the report (expect: blocked again, fresh report with the new HEAD)"
run "$S/r2" "$S/r2.t3.json" --continue "Run exactly this shell command: sh later.sh   Then reply with exactly: Pushed."

echo; echo "== what the hook logged (two blocks and two reports expected in r2; none in r1)"
cat "$S/r1/.git/close-out-report.log" 2>/dev/null || echo "r1: (no log)"
cat "$S/r2/.git/close-out-report.log" 2>/dev/null
echo "== the last report against the scratch repo's current HEAD (expect OK)"
python3 -c "import json,sys; print(json.load(open('$S/r2.t3.json'))['result'])" | (cd "$S/r2" && python3 starter-kit/close_out_report.py --check -)
echo "== cost: total_cost_usd is cumulative per session, so take each session's LAST file"
python3 - "$S" <<'EOF'
import json, sys
s = sys.argv[1]
print("r1 $%.4f + r2 $%.4f" % (json.load(open(s + "/r1.t1.json"))["total_cost_usd"], json.load(open(s + "/r2.t3.json"))["total_cost_usd"]))
EOF
