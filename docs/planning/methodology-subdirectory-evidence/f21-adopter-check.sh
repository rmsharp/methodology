#!/bin/bash
# BL-101 F21 (S300): the tool's ledger entry, on the adopter whose ledger it landed inside a fence in (`chat_verification`, P16).
# The adopter is cloned with --no-local at a3174b3 (the commit before the move `ebbfabd`: synced, with the layout-aware hook) into
# SCRATCH (a path WITHOUT the word `scratchpad`, F23); the real repository is only cloned and read. Two arms, each synced with
# bin/sync (no --force) from ITS tool's own checkout and given a ledger entry in the adopter's format before the move:
#   old   the tool as it stood before F21 (OLD_TOOL_SHA), the commit that reproduces the defect
#   new   the tool under test (the checkout this script sits in)
# For each, a real `--tier all --apply` in the clone, then: the line of the tool's entry, the line of the "Entries go below"
# marker, whether the entry sits inside a fence (the trimmer's fence_scan), `check-ledger` on the moved ledger, and the moved
# ledger against the hand-corrected one the adopter committed (0a8ef90).
# Usage: SCRATCH=$HOME/.cache/f21 OLD_TOOL_SHA=ca2a653 f21-adopter-check.sh
set -u
S=${SCRATCH:?set SCRATCH to a directory whose path does not contain "scratchpad"}
case "$S" in *scratchpad*) echo "SCRATCH must not contain scratchpad"; exit 9;; esac
OLD=${OLD_TOOL_SHA:?set OLD_TOOL_SHA to the commit before the fix}
R=$S/f21
A=$HOME/Development/chat_verification
M=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
BASE=a3174b3
HAND=0a8ef90
TRAILER='Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>'
rm -rf "$R"; mkdir -p "$R"
printf 'start %s\n' "$(date)"
printf 'adopter HEAD %s; base %s; hand-corrected %s\n' "$(git -C "$A" rev-parse --short HEAD)" "$BASE" "$HAND"
printf 'tool under test %s; the tool before the fix %s\n' "$(git -C "$M" rev-parse --short HEAD)" "$OLD"
git clone -q --no-local "$M" "$R/tool-old" && git -C "$R/tool-old" checkout -q "$OLD"
git -C "$M" status --porcelain | grep -v '^??' | sed 's/^/tool under test, modified: /'

ledger_entry() {  # ledger_entry <ledger> <title>: an entry in the adopter's own format below its "Entries go below" line
  python3 - "$1" "$2" <<'PYEOF'
import sys
p, title = sys.argv[1:3]
t = open(p, encoding="utf-8").read()
anchor = "<!-- Entries go below, newest on top. -->\n\n"
assert t.count(anchor) == 1, "anchor not found exactly once in %s" % p
entry = ("### 2026-10-12 · [ad hoc] %s\n- **Change:** %s\n- **Commit/PR:** the commit that ships this entry\n"
         "- **Session:** F21 check · **Verified:** n/a\n\n" % (title, title))
open(p, "w", encoding="utf-8").write(t.replace(anchor, anchor + entry))
PYEOF
}

for arm in old new; do
  T=$M; [ "$arm" = old ] && T=$R/tool-old
  C=$R/$arm
  git clone -q --no-local "$A" "$C" && git -C "$C" checkout -q "$BASE" && git -C "$C" config core.hooksPath .githooks
  "$T/bin/sync" "$C" > "$R/$arm.sync.txt" 2>&1; printf '%s: sync exit=%s\n' "$arm" "$?"
  if ! git -C "$C" diff --quiet || [ -n "$(git -C "$C" status --porcelain)" ]; then
    ledger_entry "$C/CHANGELOG.md" "Methodology sync"
    git -C "$C" add -A && git -C "$C" commit -q -m "chore(methodology): sync" > "$R/$arm.synccommit.txt" 2>&1; printf '%s: sync commit exit=%s\n' "$arm" "$?"
  fi
  "$T/bin/migrate-layout" "$C" --tier all --json > "$R/$arm.dry.json" 2> "$R/$arm.dry.err"; printf '%s: dry run exit=%s\n' "$arm" "$?"
  "$T/bin/migrate-layout" "$C" --tier all --apply --trailer "$TRAILER" > "$R/$arm.apply.txt" 2>&1; printf '%s: apply exit=%s\n' "$arm" "$?"
  python3 - "$C" "$arm" "$M" "$A" "$HAND" <<'PYEOF'
import difflib, importlib.util, re, subprocess, sys
C, arm, M, A, HAND = sys.argv[1:6]
spec = importlib.util.spec_from_file_location("trim", M + "/starter-kit/methodology_trim.py")
trim = importlib.util.module_from_spec(spec); sys.dont_write_bytecode = True; spec.loader.exec_module(trim)
text = open(C + "/methodology/CHANGELOG.md", encoding="utf-8").read()
lines = text.split("\n")
mine = [i for i, l in enumerate(lines) if "Layout migration" in l and l.startswith("### ")]
marker = [i for i, l in enumerate(lines) if l.startswith("<!-- Entries go below")]
inside = {i for i, _s, inside_before, _info in trim.fence_scan(lines) if inside_before}
print("%s: the tool's entry at line %s; the marker at line %s; inside a fence: %s" % (
    arm, [i + 1 for i in mine], [i + 1 for i in marker], [i in inside for i in mine]))
hand = subprocess.run(["git", "-C", A, "show", HAND + ":methodology/CHANGELOG.md"], capture_output=True, text=True).stdout.split("\n")
d = [l for l in difflib.unified_diff(hand, lines, "hand-corrected " + HAND, arm, n=0, lineterm="") if not l.startswith(("---", "+++", "@@"))]
print("%s: against the adopter's hand-corrected ledger %s: %d differing line(s)" % (arm, HAND, len(d)))
for l in d[:12]:
    print("    " + l[:150])
def findings(path):
    r = subprocess.run([sys.executable, "-B", M + "/bin/check-ledger", "--file", path], capture_output=True, text=True)
    return (r.stderr.strip().splitlines() or r.stdout.strip().splitlines() or ["?"])[0][:90]
open(C + "/../hand.md", "w", encoding="utf-8").write("\n".join(hand))
print("%s: check-ledger on the moved ledger: %s; on the adopter's hand-corrected one: %s" % (arm, findings(C + "/methodology/CHANGELOG.md"), findings(C + "/../hand.md")))
PYEOF
done
printf 'end %s\n' "$(date)"
