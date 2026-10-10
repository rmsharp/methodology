#!/bin/bash
# P13 final check: Phase 0 in the new layout, from a fresh --no-local clone of the real airqino HEAD, and the same
# reads on a clone of the synced commit before the move (the control). Nothing here touches the real tree.
set -u
S=${SCRATCH:?set SCRATCH to a scratch directory}
R=$S/p13-final; A=$HOME/Development/airqino; M=$HOME/Development/methodology
SYNC=${SYNC_SHA:?set SYNC_SHA to the sync commit in the adopter}
rm -rf "$R"; mkdir -p "$R"; exec > "$R/log.txt" 2>&1
printf 'adopter HEAD %s\n' "$(git -C "$A" rev-parse HEAD)"
git clone -q --no-local "$A" "$R/head"
git clone -q --no-local "$A" "$R/ctrl"; git -C "$R/ctrl" checkout -q "$SYNC"; printf 'control at %s\n' "$(git -C "$R/ctrl" rev-parse --short HEAD)"

cd "$R/head"
# Phase 0 in the new layout (read steps run from the project root)
for f in methodology/SESSION_RUNNER.md methodology/SAFEGUARDS.md methodology/SESSION_NOTES.md methodology/CHANGELOG.md methodology/HANDOFFS.md; do test -f "$f" && printf 'present %s\n' "$f" || printf 'MISSING %s\n' "$f"; done
cmp methodology/SAFEGUARDS.md "$M/starter-kit/SAFEGUARDS.md" && echo 'SAFEGUARDS byte-identical to canonical'
cmp methodology/SESSION_RUNNER.md "$M/starter-kit/SESSION_RUNNER.md" && echo 'SESSION_RUNNER byte-identical to canonical'
grep -n -m1 'ACTIVE TASK' methodology/SESSION_NOTES.md
printf 'git status lines: %s\n' "$(git status --short | wc -l | tr -d ' ')"; git log --oneline -4 | cut -c1-110
F=$(git log -1 --format=%H -- methodology/CHANGELOG.md); printf 'CHANGELOG frontier %s; undocumented after it: %s\n' "${F:0:7}" "$(git rev-list --count --no-merges "$F"..HEAD)"
H=$(git log -1 --format=%H -- methodology/HANDOFFS.md); printf 'HANDOFFS frontier %s; commits after: %s\n' "${H:0:7}" "$(git rev-list --count --no-merges "$H"..HEAD)"
printf 'merges since the frontier: %s\n' "$(git log --merges --oneline "$F"..HEAD | wc -l | tr -d ' ')"
python3 methodology/methodology_dashboard.py --no-open > "$R/head.dash.txt" 2>&1; printf 'dashboard head exit=%s\n' "$?"
( cd "$R/ctrl" && python3 methodology_dashboard.py --no-open > "$R/ctrl.dash.txt" 2>&1; printf 'dashboard ctrl exit=%s\n' "$?" )
for n in ctrl head; do printf '  %s: %s\n' "$n" "$(sed 's/\x1b\[[0-9;]*m//g' "$R/$n.dash.txt" | grep 'Health:' | tr -s ' ')"; done

# the adopter's own build equivalent and its gates, from the clones
( cd "$R/ctrl" && python3 -m pytest -q > "$R/ctrl.pytest.txt" 2>&1; printf 'pytest ctrl exit=%s  %s\n' "$?" "$(tail -1 "$R/ctrl.pytest.txt")" )
python3 -m pytest -q > "$R/head.pytest.txt" 2>&1; printf 'pytest head exit=%s  %s\n' "$?" "$(tail -1 "$R/head.pytest.txt")"
( cd "$R/ctrl" && python3 quality_ratchet.py --run > "$R/ctrl.ratchet.txt" 2>&1; printf 'ratchet ctrl exit=%s  %s\n' "$?" "$(sed 's/\x1b\[[0-9;]*m//g' "$R/ctrl.ratchet.txt" | grep 'quality_ratchet:' | sed 's/.*quality_ratchet: //')" )
python3 methodology/quality_ratchet.py --run > "$R/head.ratchet.txt" 2>&1; printf 'ratchet head exit=%s  %s\n' "$?" "$(sed 's/\x1b\[[0-9;]*m//g' "$R/head.ratchet.txt" | grep 'quality_ratchet:' | sed 's/.*quality_ratchet: //')"

# bin/status, check-links and the checkers, as the tool's own before-and-after
"$M/bin/status" "$R/head" > "$R/head.status.txt" 2>&1; printf 'status head exit=%s  tracked current: %s\n' "$?" "$(sed 's/\x1b\[[0-9;]*m//g' "$R/head.status.txt" | grep -c ' tracked  *current')"
"$M/bin/check-links" --tree "$R/head" > "$R/head.links.txt" 2>&1; printf 'check-links head exit=%s\n' "$?"; sed -n 2,3p "$R/head.links.txt" | cut -c1-200
touch "$R/DONE"
