#!/bin/bash
# BL-105 build phase 4, vscode_quarto_ext: the final check. The project's OWN gates and Phase 0 in the new layout, from a fresh
# --no-local clone of the real HEAD (head: the synced tree with PROJECT_LEARNINGS.md under methodology/; the SESSION_NOTES shard and its proof stay, the tool's own call), the same reads on
# a clone of the commit before the move (ctrl: the synced tree with them at the old places), and LATER commits through the
# ledger-lag gate (the adopter has no hook: its gate is what notices a commit with no ledger entry).
# Nothing here touches the real tree, which cannot run its release gate cheaply (its untracked scratchpad/ is 66 GB and vsce
# walks it). SCRATCH must not contain the word "scratchpad" (F23).
set -u
S=${SCRATCH:?set SCRATCH to a directory whose path does not contain "scratchpad"}
case "$S" in *scratchpad*) echo "SCRATCH must not contain scratchpad"; exit 9;; esac
R=$S/p4-final; A=$HOME/Development/vscode_quarto_ext; M=$HOME/Development/methodology
CTRL=${CTRL_SHA:?set CTRL_SHA to the commit before the move in the adopter (the sync commit)}
BASE=${BASE_SHA:?set BASE_SHA to the adopter commit before the sync (0c8d9669)}
strip() { sed 's/\x1b\[[0-9;]*m//g'; }
rm -rf "$R"; mkdir -p "$R"; exec > "$R/log.txt" 2>&1
printf 'adopter HEAD %s\n' "$(git -C "$A" rev-parse HEAD)"
git clone -q --no-local "$A" "$R/head"
git clone -q --no-local "$A" "$R/ctrl"; git -C "$R/ctrl" checkout -q "$CTRL"
git clone -q --no-local "$A" "$R/base"; git -C "$R/base" checkout -q "$BASE"
printf 'control at %s, base at %s\n' "$(git -C "$R/ctrl" rev-parse --short HEAD)" "$(git -C "$R/base" rev-parse --short HEAD)"
for n in head ctrl base; do /bin/cp -Rc "$A/node_modules" "$R/$n/node_modules"; /bin/cp -Rc "$A/dist" "$R/$n/dist"; done

cd "$R/head" || exit 1
# Phase 0 in the new layout (read steps run from the project root)
for f in methodology/SESSION_RUNNER.md methodology/SAFEGUARDS.md methodology/SESSION_NOTES.md methodology/CHANGELOG.md methodology/HANDOFFS.md methodology/PROJECT_LEARNINGS.md; do test -f "$f" && printf 'present %s\n' "$f" || printf 'MISSING %s\n' "$f"; done
test -e PROJECT_LEARNINGS.md && echo 'STILL AT THE OLD PLACE PROJECT_LEARNINGS.md' || echo 'gone from the old place: PROJECT_LEARNINGS.md'
# the shard and its proof STAY (the tool left them: its proof exits 2 at the new place): they must still be at the old place
for f in docs/archive/SESSION_NOTES-through-S253.md docs/archive/SESSION_NOTES-through-S253.md.verify.sh; do test -f "$f" && printf 'stays, as the tool said: %s\n' "$f" || printf 'MISSING (should have stayed) %s\n' "$f"; done
cmp methodology/SAFEGUARDS.md "$M/starter-kit/SAFEGUARDS.md" && echo 'SAFEGUARDS byte-identical to canonical'
cmp methodology/SESSION_RUNNER.md "$M/starter-kit/SESSION_RUNNER.md" && echo 'SESSION_RUNNER byte-identical to canonical'
cmp methodology/BOOTSTRAP.md "$M/starter-kit/BOOTSTRAP.md" && echo 'BOOTSTRAP byte-identical to canonical'
grep -n -m1 'ACTIVE TASK' methodology/SESSION_NOTES.md || echo 'no ACTIVE TASK line in methodology/SESSION_NOTES.md'
printf 'git status lines: %s\n' "$(git status --short | wc -l | tr -d ' ')"; git log --oneline -5 | cut -c1-120
F=$(git log -1 --format=%H -- methodology/CHANGELOG.md); printf 'CHANGELOG frontier %s; undocumented after it: %s\n' "${F:0:7}" "$(git rev-list --count --no-merges "$F"..HEAD)"
H=$(git log -1 --format=%H -- methodology/HANDOFFS.md); printf 'HANDOFFS frontier %s; commits after: %s\n' "${H:0:7}" "$(git rev-list --count --no-merges "$H"..HEAD)"
printf 'merges since the frontier: %s\n' "$(git log --merges --oneline "$F"..HEAD | wc -l | tr -d ' ')"
printf 'tool entry in methodology/CHANGELOG.md: %s\n' "$(grep -n 'Layout top-up' methodology/CHANGELOG.md | head -1 | cut -c1-140)"
printf 'code fences before the first dated heading (F21 read): %s\n' "$(awk '/^```/{c++} /^## 20|^### 20/{exit} END{print c+0}' methodology/CHANGELOG.md)"
printf 'follow: PROJECT_LEARNINGS.md commits before %s, after %s\n' "$(git -C "$R/ctrl" log --follow --oneline -- PROJECT_LEARNINGS.md | wc -l | tr -d ' ')" "$(git log --follow --oneline -- methodology/PROJECT_LEARNINGS.md | wc -l | tr -d ' ')"
git show --stat -M --format='%h %s' HEAD | head -12 | cut -c1-140

# the project's own checks and the tool's reads: head, ctrl and base
checks() {  # checks <dir> <label>
  ( cd "$1" || exit
    npm test > "$R/$2.npmtest.txt" 2>&1; printf 'npm test %s exit=%s  %s  %s\n' "$2" "$?" "$(strip < "$R/$2.npmtest.txt" | grep -E '^ +Test Files' | tr -s ' ')" "$(strip < "$R/$2.npmtest.txt" | grep -E '^ +Tests ' | tr -s ' ')"
    npm run check-package > "$R/$2.check-package.txt" 2>&1; printf 'check-package %s exit=%s  %s\n' "$2" "$?" "$(strip < "$R/$2.check-package.txt" | grep -E '^check-package:' | cut -c1-110)"
    npm run check-backlog > "$R/$2.check-backlog.txt" 2>&1; printf 'check-backlog %s exit=%s\n' "$2" "$?"
    npm run check-types > "$R/$2.check-types.txt" 2>&1; printf 'check-types %s exit=%s\n' "$2" "$?"
    python3 methodology/quality_ratchet.py --run > "$R/$2.ratchet.txt" 2>&1; printf 'ratchet %s exit=%s  %s\n' "$2" "$?" "$(strip < "$R/$2.ratchet.txt" | grep 'quality_ratchet:' | sed 's/.*quality_ratchet: //')"
    python3 methodology/context_budget.py --status > "$R/$2.budget.txt" 2>&1; printf 'context_budget %s exit=%s\n' "$2" "$?"
    strip < "$R/$2.budget.txt" | grep -E 'PROJECT_LEARNINGS|context budget' | sed 's/^/    /' | cut -c1-200
    "$M/bin/check-ledger" > "$R/$2.check-ledger.txt" 2>&1; printf 'check-ledger %s exit=%s  %s\n' "$2" "$?" "$(grep -o 'check-ledger: [0-9]* finding' "$R/$2.check-ledger.txt")"
    "$M/bin/check-handoff" > "$R/$2.check-handoff.txt" 2>&1; printf 'check-handoff %s exit=%s  %s\n' "$2" "$?" "$(sed -n 1p "$R/$2.check-handoff.txt" | sed 's#/[^ ]*/HANDOFFS.md##' | cut -c1-80)" )
}
checks "$R/base" base
checks "$R/ctrl" ctrl
checks "$R/head" head
for n in base ctrl head; do ( cd "$R/$n" && node_modules/.bin/vsce ls | sort > "$R/$n.vsce-ls.txt" ); done
printf 'packaged set (vsce ls): base %s paths, ctrl %s, head %s; head differs from base by %s lines, from ctrl by %s\n' "$(wc -l < "$R/base.vsce-ls.txt" | tr -d ' ')" "$(wc -l < "$R/ctrl.vsce-ls.txt" | tr -d ' ')" "$(wc -l < "$R/head.vsce-ls.txt" | tr -d ' ')" "$(diff "$R/base.vsce-ls.txt" "$R/head.vsce-ls.txt" | grep -c '^[<>]')" "$(diff "$R/ctrl.vsce-ls.txt" "$R/head.vsce-ls.txt" | grep -c '^[<>]')"
for n in base head; do ( cd "$R/$n" && npx vsce package -o "$R/$n.vsix" > "$R/$n.vsce-package.txt" 2>&1; printf 'vsce package %s exit=%s  %s B  %s entries\n' "$n" "$?" "$(ls -l "$R/$n.vsix" | awk '{print $5}')" "$(unzip -Z1 "$R/$n.vsix" | wc -l | tr -d ' ')" ); done
printf 'vsix entry lists differ (base vs head): %s lines\n' "$(diff <(unzip -Z1 "$R/base.vsix" | sort) <(unzip -Z1 "$R/head.vsix" | sort) | grep -c '^[<>]')"
( cd "$R/ctrl" && bash docs/archive/SESSION_NOTES-through-S253.md.verify.sh > "$R/ctrl.shard-proof.txt" 2>&1; printf 'shard proof ctrl (old place): exit=%s  %s\n' "$?" "$(strip < "$R/ctrl.shard-proof.txt" | tail -1 | cut -c1-140)" )
( cd "$R/head" && bash docs/archive/SESSION_NOTES-through-S253.md.verify.sh > "$R/head.shard-proof.txt" 2>&1; printf 'shard proof head (it stays at the old place): exit=%s  %s\n' "$?" "$(strip < "$R/head.shard-proof.txt" | tail -1 | cut -c1-140)" )
"$M/bin/status" "$R/head" > "$R/head.status.txt" 2>&1; printf 'status head exit=%s  %s  tracked current: %s  not current: %s\n' "$?" "$(strip < "$R/head.status.txt" | grep '^layout:' | tr -s ' ')" "$(strip < "$R/head.status.txt" | grep -c ' tracked .* current')" "$(strip < "$R/head.status.txt" | grep ' tracked ' | grep -vc ' current')"
"$M/bin/check-links" --tree "$R/ctrl" > "$R/ctrl.links.txt" 2>&1; printf 'check-links ctrl exit=%s  %s\n' "$?" "$(sed -n 1p "$R/ctrl.links.txt" | cut -c1-90)"
"$M/bin/check-links" --tree "$R/head" > "$R/head.links.txt" 2>&1; printf 'check-links head exit=%s  %s\n' "$?" "$(sed -n 1p "$R/head.links.txt" | cut -c1-90)"
diff <(sort "$R/ctrl.links.txt") <(sort "$R/head.links.txt") > "$R/links.diff.txt"; printf 'check-links: %s lines differ between ctrl and head\n' "$(grep -c '^[<>]' "$R/links.diff.txt")"
for n in ctrl head; do ( cd "$R/$n" && python3 methodology/methodology_dashboard.py --no-open > "$R/$n.dash.txt" 2>&1; printf '  dashboard %s: %s\n' "$n" "$(strip < "$R/$n.dash.txt" | grep 'Health:' | tr -s ' ')" ); done

# LATER commits in each clone (no hook is armed: the project has none), read through its own ledger-lag gate
later() {  # later <dir> <label>
  ( cd "$1" || exit
    mkdir -p docs/planning; printf 'probe\n' >> docs/planning/probe.txt; git add docs/planning/probe.txt
    git commit -q -m "probe: tracked content, no ledger entry" > "$R/$2.probe-noledger.txt" 2>&1; printf 'LATER commit, NO ledger entry (%s): exit=%s\n' "$2" "$?"
    python3 methodology/quality_ratchet.py --run > "$R/$2.ratchet-after-noledger.txt" 2>&1; printf '  ledger-lag after it: %s\n' "$(strip < "$R/$2.ratchet-after-noledger.txt" | grep -E '^ +ledger-lag' | tr -s ' ')"
    printf 'probe 2\n' >> docs/planning/probe.txt; git add docs/planning/probe.txt
    python3 -I - methodology/CHANGELOG.md <<'PYEOF'
import sys
p = sys.argv[1]; t = open(p, encoding="utf-8").read()
a = "## 2026-10\n\n"
e = "### 2026-10-13 · [ad hoc] probe entry\n\na probe commit\n\n"
assert t.count(a) == 1
open(p, "w", encoding="utf-8").write(t.replace(a, a + e, 1))
PYEOF
    git add methodology/CHANGELOG.md; git commit -q -m "probe: tracked content and a ledger entry" > "$R/$2.probe-ledger.txt" 2>&1; printf 'LATER commit, WITH a ledger entry at methodology/CHANGELOG.md (%s): exit=%s\n' "$2" "$?"
    python3 methodology/quality_ratchet.py --run > "$R/$2.ratchet-after-ledger.txt" 2>&1; printf '  ledger-lag after it: %s\n' "$(strip < "$R/$2.ratchet-after-ledger.txt" | grep -E '^ +ledger-lag' | tr -s ' ')" )
}
later "$R/head" head
touch "$R/DONE"
