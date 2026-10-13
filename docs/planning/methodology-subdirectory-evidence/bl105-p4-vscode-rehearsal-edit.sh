#!/bin/bash
# BL-105 build phase 4, vscode_quarto_ext: the arm `edit` of the rehearsal (the second run; the first, bl105-p4-vscode-rehearsal.sh,
# is the tool alone). The tool's rewrite of CLAUDE.md leaves "(project root, committed)" beside `methodology/PROJECT_LEARNINGS.md`
# (CLAUDE.md:263, a sentence that states WHERE the file is: false after the move). The adopter's own one-line fix goes in its own
# commit BEFORE the move, as phase 4 asks of every hand edit: sync commit, edit commit, then bin/migrate-layout --apply.
# Clones only; SCRATCH must not contain "scratchpad" (F23). Reads the first run's base.vsce-ls.txt and topup clone from SCRATCH/p4.
set -u
S=${SCRATCH:?set SCRATCH to a directory whose path does not contain "scratchpad"}
case "$S" in *scratchpad*) echo "SCRATCH must not contain scratchpad"; exit 9;; esac
R=$S/p4e; P=$S/p4
A=$HOME/Development/vscode_quarto_ext; M=$HOME/Development/methodology
TRAILER='Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>'
rm -rf "$R"; mkdir -p "$R"; exec > "$R/log.txt" 2>&1
strip() { sed 's/\x1b\[[0-9;]*m//g'; }
printf 'start %s\nadopter HEAD %s\n' "$(date)" "$(git -C "$A" rev-parse HEAD)"
git clone -q --no-local "$A" "$R/edit"; /bin/cp -Rc "$A/node_modules" "$R/edit/node_modules"; /bin/cp -Rc "$A/dist" "$R/edit/dist"

ledger_entry() {  # ledger_entry <ledger path> <title> <change>
  python3 -I - "$1" "$2" "$3" <<'PYEOF'
import sys
p, title, change = sys.argv[1:4]
t = open(p, encoding="utf-8").read()
anchor = "## 2026-10\n\n"
assert t.count(anchor) == 1
open(p, "w", encoding="utf-8").write(t.replace(anchor, anchor + "### 2026-10-13 · [ad hoc] %s\n\n%s\n\n" % (title, change), 1))
PYEOF
}
claude_md_edit() {  # the one-line fix, asserted to match exactly once
  python3 -I - "$1/CLAUDE.md" <<'PYEOF'
import sys
p = sys.argv[1]
t = open(p, encoding="utf-8").read()
old = "(project root, committed) — extracted there on"
new = "(committed) — extracted there on"
assert t.count(old) == 1, t.count(old)
open(p, "w", encoding="utf-8").write(t.replace(old, new, 1))
PYEOF
}
commit_all() { git -C "$1" add -A; git -C "$1" commit -q -m "$2" > "$R/commit.$(git -C "$1" rev-list --count HEAD).txt" 2>&1; printf 'commit (%s) exit=%s\n' "$2" "$?"; }

"$M/bin/sync" "$R/edit" > "$R/sync.txt" 2>&1; printf 'sync exit=%s\n' "$?"
ledger_entry "$R/edit/methodology/CHANGELOG.md" "Methodology sync (rehearsal text)" "bin/sync wrote the methodology files."
commit_all "$R/edit" "chore(methodology): sync"
claude_md_edit "$R/edit"
ledger_entry "$R/edit/methodology/CHANGELOG.md" "CLAUDE.md: the learnings pointer no longer says where the file is (rehearsal text)" "One phrase."
commit_all "$R/edit" "docs(claude): the learnings pointer no longer says the file is at the project root, before the layout move"
git -C "$R/edit" show --stat --format= HEAD | sed 's/^/    /'
"$M/bin/migrate-layout" "$R/edit" > "$R/migrate-dry.txt" 2>&1; printf 'migrate dry-run exit=%s  moves: %s\n' "$?" "$(strip < "$R/migrate-dry.txt" | grep -c '^  git mv')"
"$M/bin/migrate-layout" "$R/edit" --apply --trailer "$TRAILER" > "$R/migrate.txt" 2>&1; printf 'migrate --apply exit=%s\n' "$?"
printf 'status after: [%s]  HEAD %s\n' "$(git -C "$R/edit" status --porcelain | tr '\n' ' ')" "$(git -C "$R/edit" log --oneline -1 | cut -c1-90)"
printf 'CLAUDE.md pointer after the move:\n'; grep -n -A1 '^See \[`methodology/PROJECT_LEARNINGS.md`\]' "$R/edit/CLAUDE.md" | cut -c1-160 | sed 's/^/    /'
printf 'CLAUDE.md "project root" mentions of the file after: %s\n' "$(grep -c 'project root, committed' "$R/edit/CLAUDE.md")"

( cd "$R/edit" || exit
  npm test > "$R/npmtest.txt" 2>&1; printf 'npm test exit=%s  %s  %s\n' "$?" "$(strip < "$R/npmtest.txt" | grep -E '^ +Test Files' | tr -s ' ')" "$(strip < "$R/npmtest.txt" | grep -E '^ +Tests ' | tr -s ' ')"
  npm run check-package > "$R/check-package.txt" 2>&1; printf 'check-package exit=%s  %s\n' "$?" "$(strip < "$R/check-package.txt" | grep -E '^check-package:' | cut -c1-80)"
  node_modules/.bin/vsce ls 2>/dev/null | sort > "$R/vsce-ls.txt"; printf 'vsce ls: %s paths; differ from base: %s lines\n' "$(wc -l < "$R/vsce-ls.txt" | tr -d ' ')" "$(diff "$P/base.vsce-ls.txt" "$R/vsce-ls.txt" | grep -c '^[<>]')"
  npm run check-backlog > "$R/check-backlog.txt" 2>&1; printf 'check-backlog exit=%s\n' "$?"
  npm run check-types > "$R/check-types.txt" 2>&1; printf 'check-types exit=%s\n' "$?"
  python3 methodology/quality_ratchet.py --run > "$R/ratchet.txt" 2>&1; printf 'ratchet exit=%s  %s\n' "$?" "$(strip < "$R/ratchet.txt" | grep 'quality_ratchet:' | sed 's/.*quality_ratchet: //')"
  python3 methodology/context_budget.py --status > "$R/budget.txt" 2>&1; printf 'context_budget exit=%s  %s\n' "$?" "$(strip < "$R/budget.txt" | grep 'context budget' | tr -s ' ')" )
# the edit arm against the first run's topup arm: tracked content must differ in CLAUDE.md's one phrase and the ledger only
printf 'tracked files, edit vs topup: %s lines differ in the file list\n' "$(diff <(git -C "$R/edit" ls-files | sort) <(git -C "$P/topup" ls-files | sort) | grep -c '^[<>]')"
diff -rq --exclude=.git --exclude=node_modules --exclude=dist --exclude=__pycache__ --exclude=dashboard.html --exclude=dashboard_history.jsonl --exclude='.context-budget-history.jsonl' --exclude=.quality-gates-results.json "$R/edit" "$P/topup" | sed "s#$R/##;s#$P/##" | sed 's/^/    /'
diff <(git -C "$R/edit" show HEAD:CLAUDE.md) <(git -C "$P/topup" show HEAD:CLAUDE.md) | sed 's/^/    CLAUDE.md edit-vs-topup: /' | cut -c1-200
printf 'done %s\n' "$(date)"; touch "$R/DONE"
