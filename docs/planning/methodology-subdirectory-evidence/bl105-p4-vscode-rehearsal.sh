#!/bin/bash
# BL-105 build phase 4, the adopter vscode_quarto_ext (already in the new layout since P17): the rehearsal, in --no-local clones
# only. The real repository is cloned and read, never written, and none of its gates is run in it (its untracked scratchpad/ is
# 66 GB and vsce walks it).
# The clones MUST live outside any path that contains the word "scratchpad" (F23: the project's .vscodeignore carries
# `scratchpad/**`, and vsce then lists NOTHING for a clone under such a path, so check-package reads "0 files" on the unmoved base).
# Use SCRATCH=$HOME/.cache/s309-rehearsal, not the session scratchpad.
# The project has no tracked hook, no per-clone hook, no CI. Its own checks: npm test (vitest), npm run check-package (the
# deny-by-default .vsix gate, its `release-gate`), check-backlog, check-types, quality_ratchet.py --run (ledger-lag, release-gate).
# Not run, stated: test:integration, test:lsp, observe:posit (each needs a downloaded VS Code, .vscode-test is 21 GB).
# Arms:  base   the real HEAD, untouched (control: what the project reads today)
#        ctrl   base + bin/sync (committed with a ledger entry): what the sync alone does
#        topup  ctrl + bin/migrate-layout --apply (the companion top-up: the tool as it leaves the project, no hand edit)
# Every arm gets node_modules and dist/ by APFS clone (/bin/cp -Rc; the PATH's cp is GNU and has no -c).
set -u
S=${SCRATCH:?set SCRATCH to a directory whose path does not contain "scratchpad"}
case "$S" in *scratchpad*) echo "SCRATCH must not contain scratchpad"; exit 9;; esac
R=$S/p4
A=$HOME/Development/vscode_quarto_ext
M=$HOME/Development/methodology
TRAILER='Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>'
rm -rf "$R"; mkdir -p "$R"
exec > "$R/log.txt" 2>&1
printf 'start %s\n' "$(date)"
printf 'adopter HEAD %s\n' "$(git -C "$A" rev-parse HEAD)"
printf 'source HEAD  %s\n' "$(git -C "$M" rev-parse HEAD)"
printf 'adopter core.hooksPath=[%s]; tracked status: [%s]\n' "$(git -C "$A" config core.hooksPath)" "$(git -C "$A" status --porcelain --untracked-files=no | tr '\n' ' ')"

strip() { sed 's/\x1b\[[0-9;]*m//g'; }

for n in base ctrl topup; do
  git clone -q --no-local "$A" "$R/$n"
  /bin/cp -Rc "$A/node_modules" "$R/$n/node_modules"
  /bin/cp -Rc "$A/dist" "$R/$n/dist"
done
printf 'cloned 3 arms, status of each: %s\n' "$(for n in base ctrl topup; do git -C "$R/$n" status --porcelain | wc -l | tr -d ' '; done | tr '\n' ' ')"

# a hand-written ledger entry in the adopter's own format, newest on top under its first month heading
ledger_entry() {  # ledger_entry <ledger path> <title> <change>
  python3 -I - "$1" "$2" "$3" <<'PYEOF'
import sys
p, title, change = sys.argv[1:4]
t = open(p, encoding="utf-8").read()
anchor = "## 2026-10\n\n"
assert t.count(anchor) == 1, "anchor not found exactly once in %s" % p
entry = ("### 2026-10-13 · [ad hoc] %s\n\n%s\n\n" % (title, change))
open(p, "w", encoding="utf-8").write(t.replace(anchor, anchor + entry, 1))
PYEOF
}

commit_all() {  # commit_all <dir> <message>
  git -C "$1" add -A
  git -C "$1" commit -q -m "$2" > "$R/$(basename "$1").commit.$(git -C "$1" rev-list --count HEAD).txt" 2>&1; printf 'commit %s (%s) exit=%s\n' "$(basename "$1")" "$2" "$?"
}

proj() {  # proj <dir> <label>: the project's OWN checks, then the tool's, from the project root (always the new layout)
  ( cd "$1" || exit
    t0=$(date +%s); npm test > "$R/$2.npmtest.txt" 2>&1; rc=$?
    printf 'npm test %s exit=%s  %s  %s  (%s s)\n' "$2" "$rc" "$(strip < "$R/$2.npmtest.txt" | grep -E '^ +Test Files' | tr -s ' ')" "$(strip < "$R/$2.npmtest.txt" | grep -E '^ +Tests ' | tr -s ' ')" "$(( $(date +%s) - t0 ))"
    npm run check-package > "$R/$2.check-package.txt" 2>&1; rc=$?
    printf 'check-package %s exit=%s  %s\n' "$2" "$rc" "$(strip < "$R/$2.check-package.txt" | grep -E '^check-package:' | cut -c1-150)"
    strip < "$R/$2.check-package.txt" | grep -E '✗' | sed 's/^/    /' | cut -c1-200
    node_modules/.bin/vsce ls 2>/dev/null | sort > "$R/$2.vsce-ls.txt"; printf 'vsce ls %s: %s paths\n' "$2" "$(wc -l < "$R/$2.vsce-ls.txt" | tr -d ' ')"
    npm run check-backlog > "$R/$2.check-backlog.txt" 2>&1; printf 'check-backlog %s exit=%s  %s\n' "$2" "$?" "$(strip < "$R/$2.check-backlog.txt" | grep -E '^check-backlog:' | cut -c1-100)"
    npm run check-types > "$R/$2.check-types.txt" 2>&1; printf 'check-types %s exit=%s\n' "$2" "$?"
    python3 methodology/quality_ratchet.py --run > "$R/$2.ratchet.txt" 2>&1; rc=$?
    printf 'ratchet %s exit=%s  %s\n' "$2" "$rc" "$(strip < "$R/$2.ratchet.txt" | grep 'quality_ratchet:' | sed 's/.*quality_ratchet: //')"
    strip < "$R/$2.ratchet.txt" | grep -E '^ +(ledger-lag|release-gate)' | sed 's/^/    /'
    python3 methodology/context_budget.py --status > "$R/$2.budget.txt" 2>&1; printf 'context_budget --status %s exit=%s\n' "$2" "$?"
    strip < "$R/$2.budget.txt" | grep -E 'PROJECT_LEARNINGS|context budget' | sed 's/^/    /' | cut -c1-200
    "$M/bin/check-ledger" > "$R/$2.check-ledger.txt" 2>&1; printf 'check-ledger %s exit=%s  %s\n' "$2" "$?" "$(head -1 "$R/$2.check-ledger.txt" | cut -c1-90)"
    "$M/bin/check-handoff" > "$R/$2.check-handoff.txt" 2>&1; printf 'check-handoff %s exit=%s  %s\n' "$2" "$?" "$(head -1 "$R/$2.check-handoff.txt" | cut -c1-90)"
    printf 'git status %s: [%s]\n' "$2" "$(git status --porcelain | tr '\n' ' ')" )
}

shard_proof() {  # shard_proof <dir> <label> <relative path of the .verify.sh>: exit code and last line, from the project root
  ( cd "$1" || exit
    bash "$3" > "$R/$2.shard-proof.txt" 2>&1; printf 'shard proof %s (%s): exit=%s  %s\n' "$2" "$3" "$?" "$(strip < "$R/$2.shard-proof.txt" | tail -1 | cut -c1-140)" )
}

# base: before anything
proj "$R/base" base
shard_proof "$R/base" base docs/archive/SESSION_NOTES-through-S253.md.verify.sh
"$M/bin/status" "$R/base" > "$R/base.status.txt" 2>&1; printf 'status base exit=%s\n' "$?"
"$M/bin/migrate-layout" "$R/base" > "$R/base.migrate-dry.txt" 2>&1; printf 'migrate dry-run base (expected: REFUSED not-current) exit=%s\n' "$?"

# the sync, no --force: a dry run first, so a refusal (if any) is read before anything is applied
"$M/bin/sync" --dry-run "$R/ctrl" > "$R/ctrl.sync-dry.txt" 2>&1; printf 'sync --dry-run ctrl exit=%s\n' "$?"
"$M/bin/sync" "$R/ctrl" > "$R/ctrl.sync.txt" 2>&1; rc=$?; printf 'sync ctrl (no --force) exit=%s\n' "$rc"
[ "$rc" -eq 0 ] || { printf 'REFUSED in ctrl: not forced (F7/F19: match first)\n'; exit 3; }
printf 'ctrl untracked after the sync: [%s]\n' "$(git -C "$R/ctrl" status --porcelain | grep '^??' | tr '\n' ' ')"
ledger_entry "$R/ctrl/methodology/CHANGELOG.md" "Methodology sync (rehearsal text)" "bin/sync wrote the methodology files."
commit_all "$R/ctrl" "chore(methodology): sync"
proj "$R/ctrl" ctrl
"$M/bin/status" "$R/ctrl" > "$R/ctrl.status.txt" 2>&1; printf 'status ctrl exit=%s  tracked current: %s\n' "$?" "$(strip < "$R/ctrl.status.txt" | grep -c ' tracked .* current')"

# topup: the same sync commit, then the move
"$M/bin/sync" "$R/topup" > "$R/topup.sync.txt" 2>&1; printf 'sync topup (no --force) exit=%s\n' "$?"
ledger_entry "$R/topup/methodology/CHANGELOG.md" "Methodology sync (rehearsal text)" "bin/sync wrote the methodology files."
commit_all "$R/topup" "chore(methodology): sync"
"$M/bin/migrate-layout" "$R/topup" > "$R/topup.migrate-dry.txt" 2>&1; printf 'migrate dry-run topup exit=%s\n' "$?"
"$M/bin/migrate-layout" "$R/topup" --apply --trailer "$TRAILER" > "$R/topup.migrate.txt" 2>&1; printf 'migrate --apply topup exit=%s\n' "$?"
printf '  topup status after the move: [%s]  HEAD %s\n' "$(git -C "$R/topup" status --porcelain | tr '\n' ' ')" "$(git -C "$R/topup" log --oneline -1 | cut -c1-90)"
git -C "$R/topup" show --stat -M --format= HEAD | tail -12 | sed 's/^/    /'
proj "$R/topup" topup
shard_proof "$R/topup" topup methodology/archive/SESSION_NOTES-through-S253.md.verify.sh
"$M/bin/status" "$R/topup" > "$R/topup.status.txt" 2>&1; printf 'status topup exit=%s  %s  tracked current: %s\n' "$?" "$(strip < "$R/topup.status.txt" | grep '^layout:' | tr -s ' ')" "$(strip < "$R/topup.status.txt" | grep -c ' tracked .* current')"

# the packaged set: base against topup (the question F20 and F24 asked: does the move change what ships?)
printf 'diff base vs ctrl  packaged set: %s lines differ\n' "$(diff "$R/base.vsce-ls.txt" "$R/ctrl.vsce-ls.txt" | grep -c '^[<>]')"
printf 'diff base vs topup packaged set: %s lines differ\n' "$(diff "$R/base.vsce-ls.txt" "$R/topup.vsce-ls.txt" | grep -c '^[<>]')"
diff "$R/base.vsce-ls.txt" "$R/topup.vsce-ls.txt" | head -8 | sed 's/^/    /'
( cd "$R/base" && npx vsce package -o "$R/base.vsix" > "$R/base.vsce-package.txt" 2>&1; printf 'vsce package base exit=%s  %s B  %s entries\n' "$?" "$(ls -l "$R/base.vsix" | awk '{print $5}')" "$(unzip -Z1 "$R/base.vsix" | wc -l | tr -d ' ')" )
( cd "$R/topup" && npx vsce package -o "$R/topup.vsix" > "$R/topup.vsce-package.txt" 2>&1; printf 'vsce package topup exit=%s  %s B  %s entries\n' "$?" "$(ls -l "$R/topup.vsix" | awk '{print $5}')" "$(unzip -Z1 "$R/topup.vsix" | wc -l | tr -d ' ')" )
printf 'vsix entry lists differ: %s lines\n' "$(diff <(unzip -Z1 "$R/base.vsix" | sort) <(unzip -Z1 "$R/topup.vsix" | sort) | grep -c '^[<>]')"

# what the tool did to the configs and CLAUDE.md, and where its ledger entry landed
printf 'topup: first dated entries of methodology/CHANGELOG.md (line: heading):\n'
awk '/^## 20|^### 20/{print NR": "substr($0,1,140)} ' "$R/topup/methodology/CHANGELOG.md" | head -4 | sed 's/^/    /'
printf 'topup: ledger lines inside a code fence before the first dated heading: %s\n' "$(awk '/^```/{f=!f} /^## 20|^### 20/{exit} f{c++} END{print c+0}' "$R/topup/methodology/CHANGELOG.md")"
git -C "$R/topup" diff HEAD~1 HEAD -M -- methodology/.context-budget.json methodology/.quality-gates.json CLAUDE.md .gitignore | grep '^[-+]' | grep -v '^+++\|^---' | cut -c1-240 | head -30
"$M/bin/check-links" --tree "$R/ctrl" > "$R/ctrl.links.txt" 2>&1; printf 'check-links ctrl exit=%s  %s\n' "$?" "$(sed -n 1p "$R/ctrl.links.txt" | cut -c1-110)"
"$M/bin/check-links" --tree "$R/topup" > "$R/topup.links.txt" 2>&1; printf 'check-links topup exit=%s  %s\n' "$?" "$(sed -n 1p "$R/topup.links.txt" | cut -c1-110)"
diff <(sort "$R/ctrl.links.txt") <(sort "$R/topup.links.txt") > "$R/links.diff.txt"; printf 'check-links: %s lines differ between ctrl and topup\n' "$(grep -c '^[<>]' "$R/links.diff.txt")"

# the dashboard in each arm (it writes where it lives; last, because it appends to the tracked history)
for n in base ctrl topup; do
  ( cd "$R/$n" && python3 methodology/methodology_dashboard.py --no-open > "$R/$n.dash.txt" 2>&1; printf 'dash %s exit=%s  %s\n' "$n" "$?" "$(strip < "$R/$n.dash.txt" | grep 'Health:' | tr -s ' ')" )
done

printf 'done %s\n' "$(date)"
touch "$R/DONE"
