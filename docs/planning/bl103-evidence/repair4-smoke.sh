#!/usr/bin/env bash
# repair4-smoke.sh -- BL-103 option (c), S452: the real tool's printed pair, read by the real lint.
#
# Run from the repository root:   bash docs/planning/bl103-evidence/repair4-smoke.sh
# Everything happens in a scratch directory that is removed at the end; nothing in the repository is written.
#   1. quality_ratchet.py --run on a throwaway project (one gate passes, one times out, one has no command);
#   2. the two lines it prints after the table (`cite in the receipt:` and `and name them:`) are cut out of its output;
#   3. the newest COMPLETE receipt of this repository's HANDOFFS.md is copied twice with its `runtime_smoke` replaced:
#      once with the citation + the clause + ` -- by hand: ...`, once with the citation alone;
#   4. bin/check-handoff reads both. Expected: the first exits 0, the second exits 1 with its unmeasured-gates finding.
# Exit 0 only when both behave so. Surface: this machine; the lint is canonical-only, so an adopter has no copy of it.
set -uo pipefail
REPO=$(git rev-parse --show-toplevel) || exit 3
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
cd "$T" && git init -q . || exit 3
cat > .quality-gates.json <<'JSON'
{"version":1,"gates":[
 {"name":"fast-ok","direction":"max","threshold":0,"command":"true"},
 {"name":"slow-suite","direction":"max","threshold":0,"command":"sleep 30","timeout_seconds":1},
 {"name":"declared-only","direction":"min","threshold":1}
]}
JSON
OUT=$(python3 "$REPO/starter-kit/quality_ratchet.py" --run | sed 's/\x1b\[[0-9;]*m//g'); TOOL_RC=${PIPESTATUS[0]}
echo "tool exit: $TOOL_RC (1 = unmeasured)"
CITE=$(printf '%s\n' "$OUT" | sed -n 's/^  cite in the receipt: //p')
CLAUSE=$(printf '%s\n' "$OUT" | sed -n 's/^  and name them: *//p')
echo "cite:   $CITE"; echo "clause: $CLAUSE"
python3 -I - "$REPO" "$CITE" "$CLAUSE" <<'PY' || exit 3
import re, sys
repo, cite, clause = sys.argv[1:4]
s = open(repo + "/HANDOFFS.md", encoding="utf-8").read()
blocks = re.findall(r"```handoff\n.*?\n```\n", s, flags=re.S)
blk = next(b for b in blocks if re.search(r"^status: complete$", b, flags=re.M))
def build(smoke):
    return "# Handoff Receipts\n\n" + re.sub(r"^runtime_smoke: .*$", lambda m: "runtime_smoke: " + smoke, blk, flags=re.M)
open("with-clause.md", "w").write(build(cite + "; " + clause + " — by hand: 7 and 12"))
open("bare.md", "w").write(build(cite))
PY
FAIL=0
echo; echo "== the citation, the clause and a by-hand tail"; python3 "$REPO/bin/check-handoff" --file with-clause.md | head -1; RC1=${PIPESTATUS[0]}
echo "exit $RC1 (expected 0)"; [ "$RC1" = 0 ] || FAIL=1
echo; echo "== the citation alone"; python3 "$REPO/bin/check-handoff" --file bare.md | head -2; RC2=${PIPESTATUS[0]}
echo "exit $RC2 (expected 1)"; [ "$RC2" = 1 ] || FAIL=1
[ "$TOOL_RC" = 1 ] || FAIL=1
echo; [ $FAIL = 0 ] && echo "SMOKE OK" || echo "SMOKE FAILED"
exit $FAIL
