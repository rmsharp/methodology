#!/bin/bash
# P17 rehearsal: vscode_quarto_ext, in --no-local clones only. The real repository is only cloned and read.
# The clones MUST live outside any path that contains the word "scratchpad": the project's .vscodeignore carries the line
# `scratchpad/**` and vsce 3.9.2 then lists NOTHING for a clone under such a directory (measured S298: `vsce ls` printed an
# empty line and check-package read "0 files"). Use SCRATCH=$HOME/.cache/p17-rehearsal, not the session scratchpad.
# The adopter has no tracked hook, no per-clone hook (core.hooksPath unset, .git/hooks empty), no CI; its own checks are
#   npm test (vitest, 68 files / 4583 tests, about 6 s), npm run check-package (the deny-by-default .vsix gate, the
#   `release-gate` of its .quality-gates.json), check-backlog, check-types, and its two declared gates (ledger-lag, release-gate).
# Not run, stated: test:integration and test:lsp (they need a downloaded VS Code, .vscode-test is 21 GB), vsce package.
# Arms:  base   unsynced control
#        ctrl   synced, nothing else (what the sync alone does to the project's gate; run 1 showed .gitattributes is NOT packaged)
#        t1     sync + --tier 1, as the tool leaves it
#        tall   sync + --tier all, as the tool leaves it
#        t1A    sync + .vscodeignore denies methodology/** (own commit, before the move) + --tier 1
#        tallA  sync + .vscodeignore denies methodology/** (own commit, before the move) + --tier all
# Every arm gets node_modules and dist/ by APFS clone (/bin/cp -Rc; the PATH's cp is GNU and has no -c).
set -u
S=${SCRATCH:?set SCRATCH to a directory whose path does not contain "scratchpad"}
case "$S" in *scratchpad*) echo "SCRATCH must not contain scratchpad"; exit 9;; esac
R=$S/p17
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

for n in base ctrl t1 tall t1A tallA; do
  git clone -q --no-local "$A" "$R/$n"
  /bin/cp -Rc "$A/node_modules" "$R/$n/node_modules"
  /bin/cp -Rc "$A/dist" "$R/$n/dist"
done
printf 'cloned 6 arms, status of each: %s\n' "$(for n in base ctrl t1 tall t1A tallA; do git -C "$R/$n" status --porcelain | wc -l | tr -d ' '; done | tr '\n' ' ')"

# a hand-written ledger entry in the adopter's own format, newest on top under its first month heading
ledger_entry() {  # ledger_entry <ledger path> <title> <change>
  python3 - "$1" "$2" "$3" <<'PYEOF'
import sys
p, title, change = sys.argv[1:4]
t = open(p, encoding="utf-8").read()
anchor = "## 2026-09\n\n"
assert t.count(anchor) == 1, "anchor not found exactly once in %s" % p
entry = ("### 2026-10-11 · [ad hoc] %s\n- **Change:** %s\n- **Commit/PR:** the commit that ships this entry\n"
         "- **Session:** rehearsal · **Verified:** n/a\n- **Model:** Claude Sonnet 5.5\n\n" % (title, change))
open(p, "w", encoding="utf-8").write(t.replace(anchor, anchor + entry, 1))
PYEOF
}

vscodeignore_edit() {  # vscodeignore_edit <dir>: deny methodology/** in the .vsix, the one line the move needs (F11, F20)
  printf '
# Methodology: the directory the framework files move to (BL-101 P17); vsce matches without matchBase, so a bare name is the root only.
methodology/**
' >> "$1/.vscodeignore"
}

commit_all() {  # commit_all <dir> <message>
  git -C "$1" add -A
  git -C "$1" commit -q -m "$2" > "$R/$(basename "$1").commit.$(git -C "$1" rev-list --count HEAD).txt" 2>&1; printf 'commit %s (%s) exit=%s\n' "$(basename "$1")" "$2" "$?"
}

proj() {  # proj <dir> <label>: the project's OWN checks, then the tool's, from the project root, in whichever layout it has
  ( cd "$1" || exit
    pre=""; [ -f methodology/context_budget.py ] && pre="methodology/"
    t0=$(date +%s); npm test > "$R/$2.npmtest.txt" 2>&1; rc=$?
    printf 'npm test %s exit=%s  %s  %s  (%s s)\n' "$2" "$rc" "$(strip < "$R/$2.npmtest.txt" | grep -E '^ +Test Files' | tr -s ' ')" "$(strip < "$R/$2.npmtest.txt" | grep -E '^ +Tests ' | tr -s ' ')" "$(( $(date +%s) - t0 ))"
    npm run check-package > "$R/$2.check-package.txt" 2>&1; rc=$?
    printf 'check-package %s exit=%s  %s\n' "$2" "$rc" "$(strip < "$R/$2.check-package.txt" | grep -E '^check-package:' | cut -c1-150)"
    strip < "$R/$2.check-package.txt" | grep -E '✗' | sed 's/^/    /' | cut -c1-200
    node_modules/.bin/vsce ls 2>/dev/null | sort > "$R/$2.vsce-ls.txt"; printf 'vsce ls %s: %s paths\n' "$2" "$(wc -l < "$R/$2.vsce-ls.txt" | tr -d ' ')"
    npm run check-backlog > "$R/$2.check-backlog.txt" 2>&1; printf 'check-backlog %s exit=%s  %s\n' "$2" "$?" "$(strip < "$R/$2.check-backlog.txt" | grep -E '^check-backlog:' | cut -c1-100)"
    npm run check-types > "$R/$2.check-types.txt" 2>&1; printf 'check-types %s exit=%s\n' "$2" "$?"
    python3 "${pre}quality_ratchet.py" --run > "$R/$2.ratchet.txt" 2>&1; rc=$?
    printf 'ratchet %s exit=%s  %s\n' "$2" "$rc" "$(strip < "$R/$2.ratchet.txt" | grep 'quality_ratchet:' | sed 's/.*quality_ratchet: //')"
    strip < "$R/$2.ratchet.txt" | grep -E '^ +(ledger-lag|release-gate)' | sed 's/^/    /'
    python3 "${pre}context_budget.py" --status > "$R/$2.budget.txt" 2>&1; printf 'context_budget --status %s exit=%s\n' "$2" "$?"
    "$M/bin/check-ledger" > "$R/$2.check-ledger.txt" 2>&1; printf 'check-ledger %s exit=%s  %s\n' "$2" "$?" "$(head -1 "$R/$2.check-ledger.txt" | cut -c1-90)"
    "$M/bin/check-handoff" > "$R/$2.check-handoff.txt" 2>&1; printf 'check-handoff %s exit=%s  %s\n' "$2" "$?" "$(head -1 "$R/$2.check-handoff.txt" | cut -c1-90)"
    printf 'git status %s: [%s]\n' "$2" "$(git status --porcelain | tr '\n' ' ')" )
}

# base: before anything
proj "$R/base" base
"$M/bin/status" "$R/base" > "$R/base.status.txt" 2>&1; printf 'status base exit=%s\n' "$?"

# the sync, no --force: a dry run first, so a refusal (if any) is read before anything is applied
"$M/bin/sync" --dry-run "$R/ctrl" > "$R/ctrl.sync-dry.txt" 2>&1; printf 'sync --dry-run ctrl exit=%s\n' "$?"

# ctrl: the sync alone
"$M/bin/sync" "$R/ctrl" > "$R/ctrl.sync.txt" 2>&1; rc=$?; printf 'sync ctrl (no --force) exit=%s\n' "$rc"
[ "$rc" -eq 0 ] || { printf 'REFUSED in ctrl: not forced (F7/F19: match first)\n'; exit 3; }
printf 'ctrl untracked after the sync: [%s]\n' "$(git -C "$R/ctrl" status --porcelain | grep '^??' | tr '\n' ' ')"
proj "$R/ctrl" ctrl-after-sync-uncommitted
ledger_entry "$R/ctrl/CHANGELOG.md" "Methodology sync (rehearsal text)" "bin/sync wrote the methodology files."
commit_all "$R/ctrl" "chore(methodology): sync"
proj "$R/ctrl" ctrl

# t1, tall: the sync alone; t1A, tallA: the .vscodeignore commit first (own commit, own entry), then the sync
for n in t1 tall t1A tallA; do
  case "$n" in
    t1A|tallA)
      vscodeignore_edit "$R/$n"
      ledger_entry "$R/$n/CHANGELOG.md" "Deny methodology/ in .vscodeignore" "methodology/** is denied in the .vsix before the framework files move there."
      commit_all "$R/$n" "chore(vsix): deny methodology/ in .vscodeignore, before the move" ;;
  esac
  "$M/bin/sync" "$R/$n" > "$R/$n.sync.txt" 2>&1; printf 'sync %s (no --force) exit=%s\n' "$n" "$?"
  ledger_entry "$R/$n/CHANGELOG.md" "Methodology sync (rehearsal text)" "bin/sync wrote the methodology files."
  commit_all "$R/$n" "chore(methodology): sync"
done

for n in t1 tall t1A tallA; do
  t=all; case "$n" in t1|t1A) t=1;; esac
  "$M/bin/migrate-layout" "$R/$n" --tier $t > "$R/$n.migrate-dry.txt" 2>&1; printf 'migrate dry-run %s exit=%s\n' "$n" "$?"
  "$M/bin/migrate-layout" "$R/$n" --tier $t --apply --trailer "$TRAILER" > "$R/$n.migrate.txt" 2>&1; printf 'migrate --apply %s (tier %s) exit=%s\n' "$n" "$t" "$?"
  printf '  %s status after the move: [%s]  HEAD %s\n' "$n" "$(git -C "$R/$n" status --porcelain | tr '\n' ' ')" "$(git -C "$R/$n" log --oneline -1 | cut -c1-70)"
done

for n in t1 tall t1A tallA; do proj "$R/$n" "$n"; done

# the packaged set: base against the adapted arm (F20's question: does the move change what ships?)
printf 'diff base vs tallA packaged set: %s lines differ\n' "$(diff "$R/base.vsce-ls.txt" "$R/tallA.vsce-ls.txt" | grep -c '^[<>]')"
printf 'diff base vs tall  packaged set: %s lines differ\n' "$(diff "$R/base.vsce-ls.txt" "$R/tall.vsce-ls.txt" | grep -c '^[<>]')"
diff "$R/base.vsce-ls.txt" "$R/tall.vsce-ls.txt" | head -8 | sed 's/^/    tall: /'

# where did the tool's ledger entry land, and what did it do to the adopter's configs and CLAUDE.md
for n in ctrl tallA; do
  L=CHANGELOG.md; [ -f "$R/$n/methodology/CHANGELOG.md" ] && L=methodology/CHANGELOG.md
  printf '%s: first dated entries of %s (line: heading):\n' "$n" "$L"
  awk '/^## 20|^### 20/{print NR": "substr($0,1,120)} ' "$R/$n/$L" | head -4 | sed 's/^/    /'
done
printf 'tallA: ledger lines inside a code fence before the first dated heading: %s\n' "$(awk '/^```/{f=!f} /^## 20|^### 20/{exit} f{c++} END{print c+0}' "$R/tallA/methodology/CHANGELOG.md")"
git -C "$R/tallA" show --stat --format= HEAD -- .quality-gates.json methodology/.quality-gates.json methodology/.context-budget.json CLAUDE.md .gitignore | tail -8
git -C "$R/tallA" diff HEAD~1 HEAD -M -- methodology/.quality-gates.json | grep '^[-+]' | grep -v '^+++\|^---' | cut -c1-260 | head -12

for n in t1 t1A tallA; do
  "$M/bin/check-links" --tree "$R/$n" > "$R/$n.links.txt" 2>&1; printf 'check-links %s exit=%s\n' "$n" "$?"
done
for n in ctrl t1 tall t1A tallA; do
  "$M/bin/status" "$R/$n" > "$R/$n.status.txt" 2>&1; printf 'status %s exit=%s  %s\n' "$n" "$?" "$(strip < "$R/$n.status.txt" | grep '^layout:' | tr -s ' ')"
done

# the dashboard in each arm (it writes where it lives; last, because it appends to the tracked history)
( cd "$R/base" && python3 methodology_dashboard.py --no-open > "$R/base.dash.txt" 2>&1; printf 'dash base exit=%s\n' "$?" )
( cd "$R/ctrl" && python3 methodology_dashboard.py --no-open > "$R/ctrl.dash.txt" 2>&1; printf 'dash ctrl exit=%s\n' "$?" )
for n in t1 tall t1A tallA; do
  ( cd "$R/$n" && python3 methodology/methodology_dashboard.py --no-open > "$R/$n.dash.txt" 2>&1; printf 'dash %s exit=%s\n' "$n" "$?" )
done
for n in base ctrl t1 tall t1A tallA; do printf '  dashboard %s: %s\n' "$n" "$(strip < "$R/$n.dash.txt" | grep 'Health:' | tr -s ' ')"; done

printf 'done %s\n' "$(date)"
touch "$R/DONE"
