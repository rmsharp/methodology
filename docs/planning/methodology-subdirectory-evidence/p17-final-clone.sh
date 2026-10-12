#!/bin/bash
# P17 final check: the project's OWN gates and Phase 0 in the new layout, from a fresh --no-local clone of the real
# vscode_quarto_ext HEAD (head), the same reads on a clone of the commit before the move (ctrl: the synced tree), and LATER
# commits through the ledger-lag gate (the adopter has no hook: its gate is what notices a commit with no ledger entry).
# Nothing here touches the real tree, which cannot run its release gate cheaply (its untracked scratchpad/ is 66 GB and vsce
# walks it). SCRATCH must not contain the word "scratchpad" (the project's .vscodeignore line `scratchpad/**` empties vsce ls
# for a clone under such a path: P17 rehearsal run 1).
set -u
S=${SCRATCH:?set SCRATCH to a directory whose path does not contain "scratchpad"}
case "$S" in *scratchpad*) echo "SCRATCH must not contain scratchpad"; exit 9;; esac
R=$S/p17-final; A=$HOME/Development/vscode_quarto_ext; M=$HOME/Development/methodology
CTRL=${CTRL_SHA:?set CTRL_SHA to the commit before the move in the adopter}
strip() { sed 's/\x1b\[[0-9;]*m//g'; }
rm -rf "$R"; mkdir -p "$R"; exec > "$R/log.txt" 2>&1
printf 'adopter HEAD %s\n' "$(git -C "$A" rev-parse HEAD)"
git clone -q --no-local "$A" "$R/head"
git clone -q --no-local "$A" "$R/ctrl"; git -C "$R/ctrl" checkout -q "$CTRL"
printf 'control at %s\n' "$(git -C "$R/ctrl" rev-parse --short HEAD)"
for n in head ctrl; do /bin/cp -Rc "$A/node_modules" "$R/$n/node_modules"; /bin/cp -Rc "$A/dist" "$R/$n/dist"; done

cd "$R/head" || exit 1
# Phase 0 in the new layout (read steps run from the project root)
for f in methodology/SESSION_RUNNER.md methodology/SAFEGUARDS.md methodology/SESSION_NOTES.md methodology/CHANGELOG.md methodology/HANDOFFS.md; do test -f "$f" && printf 'present %s\n' "$f" || printf 'MISSING %s\n' "$f"; done
cmp methodology/SAFEGUARDS.md "$M/starter-kit/SAFEGUARDS.md" && echo 'SAFEGUARDS byte-identical to canonical'
cmp methodology/SESSION_RUNNER.md "$M/starter-kit/SESSION_RUNNER.md" && echo 'SESSION_RUNNER byte-identical to canonical'
grep -n -m1 'ACTIVE TASK' methodology/SESSION_NOTES.md || echo 'no ACTIVE TASK line in methodology/SESSION_NOTES.md'
printf 'git status lines: %s\n' "$(git status --short | wc -l | tr -d ' ')"; git log --oneline -5 | cut -c1-120
F=$(git log -1 --format=%H -- methodology/CHANGELOG.md); printf 'CHANGELOG frontier %s; undocumented after it: %s\n' "${F:0:7}" "$(git rev-list --count --no-merges "$F"..HEAD)"
H=$(git log -1 --format=%H -- methodology/HANDOFFS.md); printf 'HANDOFFS frontier %s; commits after: %s\n' "${H:0:7}" "$(git rev-list --count --no-merges "$H"..HEAD)"
printf 'merges since the frontier: %s\n' "$(git log --merges --oneline "$F"..HEAD | wc -l | tr -d ' ')"
printf 'tool entry in methodology/CHANGELOG.md: %s\n' "$(grep -n 'Layout migration:' methodology/CHANGELOG.md | head -1 | cut -c1-120)"
printf 'code fences before the first dated heading (F21 read): %s\n' "$(awk '/^```/{c++} /^## 20|^### 20/{exit} END{print c+0}' methodology/CHANGELOG.md)"

# the project's own checks and the tool's reads, head and ctrl
checks() {  # checks <dir> <label> <prefix>
  ( cd "$1" || exit
    npm test > "$R/$2.npmtest.txt" 2>&1; printf 'npm test %s exit=%s  %s  %s\n' "$2" "$?" "$(strip < "$R/$2.npmtest.txt" | grep -E '^ +Test Files' | tr -s ' ')" "$(strip < "$R/$2.npmtest.txt" | grep -E '^ +Tests ' | tr -s ' ')"
    npm run check-package > "$R/$2.check-package.txt" 2>&1; printf 'check-package %s exit=%s  %s\n' "$2" "$?" "$(strip < "$R/$2.check-package.txt" | grep -E '^check-package:' | cut -c1-110)"
    npm run check-backlog > "$R/$2.check-backlog.txt" 2>&1; printf 'check-backlog %s exit=%s\n' "$2" "$?"
    npm run check-types > "$R/$2.check-types.txt" 2>&1; printf 'check-types %s exit=%s\n' "$2" "$?"
    python3 "$3quality_ratchet.py" --run > "$R/$2.ratchet.txt" 2>&1; printf 'ratchet %s exit=%s  %s\n' "$2" "$?" "$(strip < "$R/$2.ratchet.txt" | grep 'quality_ratchet:' | sed 's/.*quality_ratchet: //')"
    python3 "$3context_budget.py" --status > "$R/$2.budget.txt" 2>&1; printf 'context_budget %s exit=%s  %s\n' "$2" "$?" "$(strip < "$R/$2.budget.txt" | grep 'context budget' | tr -s ' ')"
    "$M/bin/check-ledger" > "$R/$2.check-ledger.txt" 2>&1; printf 'check-ledger %s exit=%s  %s\n' "$2" "$?" "$(grep -o 'check-ledger: [0-9]* finding' "$R/$2.check-ledger.txt")"
    "$M/bin/check-handoff" > "$R/$2.check-handoff.txt" 2>&1; printf 'check-handoff %s exit=%s  %s\n' "$2" "$?" "$(sed -n 1p "$R/$2.check-handoff.txt" | sed 's#/[^ ]*/HANDOFFS.md##' | cut -c1-80)" )
}
checks "$R/ctrl" ctrl ""
checks "$R/head" head "methodology/"
( cd "$R/head" && node_modules/.bin/vsce ls | sort > "$R/head.vsce-ls.txt"; cd "$R/ctrl" && node_modules/.bin/vsce ls | sort > "$R/ctrl.vsce-ls.txt" )
printf 'packaged set (vsce ls): ctrl %s paths, head %s paths, differ %s lines\n' "$(wc -l < "$R/ctrl.vsce-ls.txt" | tr -d ' ')" "$(wc -l < "$R/head.vsce-ls.txt" | tr -d ' ')" "$(diff "$R/ctrl.vsce-ls.txt" "$R/head.vsce-ls.txt" | grep -c '^[<>]')"
( cd "$R/head" && npx vsce package -o "$R/head.vsix" > "$R/head.vsce-package.txt" 2>&1; printf 'vsce package head exit=%s  %s B  %s entries\n' "$?" "$(ls -l "$R/head.vsix" | awk '{print $5}')" "$(unzip -Z1 "$R/head.vsix" | wc -l | tr -d ' ')" )
"$M/bin/status" "$R/head" > "$R/head.status.txt" 2>&1; printf 'status head exit=%s  %s  tracked current: %s\n' "$?" "$(strip < "$R/head.status.txt" | grep '^layout:' | tr -s ' ')" "$(strip < "$R/head.status.txt" | grep -c ' tracked .* current')"
"$M/bin/check-links" --tree "$R/head" > "$R/head.links.txt" 2>&1; printf 'check-links head exit=%s  %s\n' "$?" "$(sed -n 1p "$R/head.links.txt" | cut -c1-90)"
( cd "$R/ctrl" && python3 methodology_dashboard.py --no-open > "$R/ctrl.dash.txt" 2>&1 )
( cd "$R/head" && python3 methodology/methodology_dashboard.py --no-open > "$R/head.dash.txt" 2>&1 )
for n in ctrl head; do printf '  dashboard %s: %s\n' "$n" "$(strip < "$R/$n.dash.txt" | grep 'Health:' | tr -s ' ')"; done

# LATER commits in each clone (no hook is armed: the project has none), read through its own ledger-lag gate
later() {  # later <dir> <label> <prefix> <ledger path>
  ( cd "$1" || exit
    mkdir -p docs/planning; printf 'probe\n' >> docs/planning/probe.txt; git add docs/planning/probe.txt
    git commit -q -m "probe: tracked content, no ledger entry" > "$R/$2.probe-noledger.txt" 2>&1; printf 'LATER commit, NO ledger entry (%s): exit=%s\n' "$2" "$?"
    python3 "$3quality_ratchet.py" --run > "$R/$2.ratchet-after-noledger.txt" 2>&1; printf '  ledger-lag after it: %s\n' "$(strip < "$R/$2.ratchet-after-noledger.txt" | grep -E '^ +ledger-lag' | tr -s ' ')"
    printf 'probe 2\n' >> docs/planning/probe.txt; git add docs/planning/probe.txt
    python3 -I - "$4" <<'PYEOF'
import sys
p = sys.argv[1]; t = open(p, encoding="utf-8").read()
a = "## 2026-09\n\n"
e = "### 2026-10-11 · [ad hoc] probe entry\n- **Change:** a probe commit\n- **Commit/PR:** this commit\n- **Session:** probe\n- **Model:** probe\n\n"
open(p, "w", encoding="utf-8").write(t.replace(a, a + e, 1))
PYEOF
    git add "$4"; git commit -q -m "probe: tracked content and a ledger entry" > "$R/$2.probe-ledger.txt" 2>&1; printf 'LATER commit, WITH a ledger entry at %s (%s): exit=%s\n' "$4" "$2" "$?"
    python3 "$3quality_ratchet.py" --run > "$R/$2.ratchet-after-ledger.txt" 2>&1; printf '  ledger-lag after it: %s\n' "$(strip < "$R/$2.ratchet-after-ledger.txt" | grep -E '^ +ledger-lag' | tr -s ' ')" )
}
later "$R/ctrl" ctrl "" CHANGELOG.md
later "$R/head" head "methodology/" methodology/CHANGELOG.md
touch "$R/DONE"
