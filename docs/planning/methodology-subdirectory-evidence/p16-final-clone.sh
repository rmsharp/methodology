#!/bin/bash
# P16 final check: Phase 0 in the new layout, from a fresh --no-local clone of the real chat_verification HEAD, the same
# reads on a clone of the commit before the move (the control: the synced tree with the replaced hook), and LATER
# commits through the hook the real tree committed (plan C5's X2: the move commit itself passes under either hook;
# what matters is the commit after it). Nothing here touches the real tree.
set -u
S=${SCRATCH:?set SCRATCH to a scratch directory}
R=$S/p16-final; A=$HOME/Development/chat_verification; M=$HOME/Development/methodology
CTRL=${CTRL_SHA:?set CTRL_SHA to the commit before the move in the adopter}
strip() { sed 's/\x1b\[[0-9;]*m//g'; }
rm -rf "$R"; mkdir -p "$R"; exec > "$R/log.txt" 2>&1
printf 'adopter HEAD %s\n' "$(git -C "$A" rev-parse HEAD)"
git clone -q --no-local "$A" "$R/head"; git -C "$R/head" config core.hooksPath .githooks
git clone -q --no-local "$A" "$R/ctrl"; git -C "$R/ctrl" checkout -q "$CTRL"; git -C "$R/ctrl" config core.hooksPath .githooks
printf 'control at %s\n' "$(git -C "$R/ctrl" rev-parse --short HEAD)"

cd "$R/head" || exit 1
# Phase 0 in the new layout (read steps run from the project root)
for f in methodology/SESSION_RUNNER.md methodology/SAFEGUARDS.md methodology/SESSION_NOTES.md methodology/CHANGELOG.md methodology/HANDOFFS.md; do test -f "$f" && printf 'present %s\n' "$f" || printf 'MISSING %s\n' "$f"; done
cmp methodology/SAFEGUARDS.md "$M/starter-kit/SAFEGUARDS.md" && echo 'SAFEGUARDS byte-identical to canonical'
cmp methodology/SESSION_RUNNER.md "$M/starter-kit/SESSION_RUNNER.md" && echo 'SESSION_RUNNER byte-identical to canonical'
grep -n -m1 'ACTIVE TASK' methodology/SESSION_NOTES.md || echo 'no ACTIVE TASK line in methodology/SESSION_NOTES.md'
printf 'git status lines: %s\n' "$(git status --short | wc -l | tr -d ' ')"; git log --oneline -6 | cut -c1-110
F=$(git log -1 --format=%H -- methodology/CHANGELOG.md); printf 'CHANGELOG frontier %s; undocumented after it: %s\n' "${F:0:7}" "$(git rev-list --count --no-merges "$F"..HEAD)"
H=$(git log -1 --format=%H -- methodology/HANDOFFS.md); printf 'HANDOFFS frontier %s; commits after: %s (the S9 receipt there is still pending)\n' "${H:0:7}" "$(git rev-list --count --no-merges "$H"..HEAD)"
printf 'merges since the frontier: %s\n' "$(git log --merges --oneline "$F"..HEAD | wc -l | tr -d ' ')"
# the ledger header's example block reads as it did before the migration, and the tool's entry is above the entries
python3 -I - "$R/head/methodology/CHANGELOG.md" "$R/ctrl/CHANGELOG.md" <<'PYEOF'
import sys
a, b = (open(p, encoding="utf-8").read() for p in sys.argv[1:3])
mark = "<!-- Entries go below, newest on top. -->"
print("ledger header (before the entries) identical to the control's: %s" % (a.split(mark)[0] == b.split(mark)[0]))
i, j = a.index("Layout migration:"), a.index(mark)
print("the tool's entry is below the entries marker: %s" % (i > j))
PYEOF
python3 methodology/methodology_dashboard.py --no-open > "$R/head.dash.txt" 2>&1; printf 'dashboard head exit=%s\n' "$?"
( cd "$R/ctrl" && python3 methodology_dashboard.py --no-open > "$R/ctrl.dash.txt" 2>&1; printf 'dashboard ctrl exit=%s\n' "$?" )
for n in ctrl head; do printf '  %s: %s\n' "$n" "$(strip < "$R/$n.dash.txt" | grep 'Health:' | tr -s ' ')"; done

# the gates (none are declared) and the tool's own reads
( cd "$R/ctrl" && python3 quality_ratchet.py --run > "$R/ctrl.ratchet.txt" 2>&1; printf 'ratchet ctrl exit=%s  %s\n' "$?" "$(strip < "$R/ctrl.ratchet.txt" | grep 'quality_ratchet:' | sed 's/.*quality_ratchet: //')" )
python3 methodology/quality_ratchet.py --run > "$R/head.ratchet.txt" 2>&1; printf 'ratchet head exit=%s  %s\n' "$?" "$(strip < "$R/head.ratchet.txt" | grep 'quality_ratchet:' | sed 's/.*quality_ratchet: //')"
"$M/bin/status" "$R/head" > "$R/head.status.txt" 2>&1; printf 'status head exit=%s  %s  tracked current: %s\n' "$?" "$(strip < "$R/head.status.txt" | grep '^layout:' | tr -s ' ')" "$(strip < "$R/head.status.txt" | grep -c ' tracked .* current')"
"$M/bin/check-links" --tree "$R/head" > "$R/head.links.txt" 2>&1; printf 'check-links head exit=%s\n' "$?"; sed -n 1,3p "$R/head.links.txt" | cut -c1-200
( cd "$R/ctrl" && python3 context_budget.py --status > "$R/ctrl.budget.txt" 2>&1; printf 'context_budget ctrl exit=%s\n' "$?" )
python3 methodology/context_budget.py --status > "$R/head.budget.txt" 2>&1; printf 'context_budget head exit=%s\n' "$?"
for n in ctrl head; do printf '  %s: %s\n' "$n" "$(strip < "$R/$n.budget.txt" | grep 'context budget' | tr -s ' ')"; done
"$M/bin/check-ledger" > "$R/head.check-ledger.txt" 2>&1; printf 'check-ledger head exit=%s  %s\n' "$?" "$(grep -o 'check-ledger: [0-9]* finding' "$R/head.check-ledger.txt")"
"$M/bin/check-handoff" > "$R/head.check-handoff.txt" 2>&1; printf 'check-handoff head exit=%s  %s\n' "$?" "$(sed -n 1p "$R/head.check-handoff.txt" | cut -c1-70)"

# the committed hook: its self-test, then LATER commits in the head clone (hooks armed, as in the real tree)
sh .githooks/pre-commit --selftest > "$R/head.hook-selftest.txt" 2>&1; printf 'hook --selftest (head) exit=%s  %s\n' "$?" "$(tail -1 "$R/head.hook-selftest.txt")"
cmp .githooks/pre-commit "$M/.githooks/pre-commit" && echo 'the committed hook is byte-identical to the canonical one'
git reset -q --hard HEAD; git clean -q -fd
mkdir -p docs/planning; printf 'probe\n' >> docs/planning/probe.txt; git add docs/planning/probe.txt
git commit -q -m "probe: tracked content, no ledger entry" > "$R/head.probe-noledger.txt" 2>&1; printf 'LATER commit, tracked content, NO ledger entry: exit=%s (want 1)\n' "$?"
sed 's/^/    hook said: /' "$R/head.probe-noledger.txt" | head -3 | cut -c1-160
git reset -q; rm -f docs/planning/probe.txt
mkdir -p docs/planning; printf 'probe\n' >> docs/planning/probe.txt; git add docs/planning/probe.txt
python3 -I - methodology/CHANGELOG.md <<'PYEOF'
import sys
p = sys.argv[1]; t = open(p, encoding="utf-8").read()
a = "<!-- Entries go below, newest on top. -->\n\n"
e = "### 2026-10-11 · [ad hoc] probe entry\n- **Change:** a probe commit\n- **Commit/PR:** this commit\n- **Session:** probe\n\n"
open(p, "w", encoding="utf-8").write(t.replace(a, a + e))
PYEOF
git add methodology/CHANGELOG.md
git commit -q -m "probe: tracked content and a ledger entry" > "$R/head.probe-ledger.txt" 2>&1; printf 'LATER commit, tracked content WITH a ledger entry at methodology/CHANGELOG.md: exit=%s (want 0)\n' "$?"
git reset -q --hard HEAD~1 2>/dev/null
# an edit of a committed entry must be refused too (the never-edit rule follows the ledger)
sed -i.bak 's/Sync the methodology files from the methodology repository (23 files)/EDITED/' methodology/CHANGELOG.md 2>/dev/null; rm -f methodology/CHANGELOG.md.bak
git add methodology/CHANGELOG.md
git commit -q -m "probe: edit a committed entry" > "$R/head.probe-edit.txt" 2>&1; printf 'LATER commit, a committed ledger entry EDITED: exit=%s (want 1)\n' "$?"
sed 's/^/    hook said: /' "$R/head.probe-edit.txt" | head -3 | cut -c1-160
git reset -q --hard HEAD
touch "$R/DONE"
