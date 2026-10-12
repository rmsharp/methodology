#!/bin/bash
# P16 rehearsal: chat_verification, in --no-local clones only. The real repository is only cloned and read.
# Every clone arms the project's ledger hook the way the real tree does (core.hooksPath = .githooks, a per-clone
# setting a clone does not inherit): register row F2 / plan C5 (the adopter's older ledger hook names CHANGELOG.md
# at the root and fails open once the ledger leaves it).
# Arms:  base   unsynced control
#        ctrl   synced
#        t1     synced + --tier 1
#        tall   synced + --tier all, the adopter's OLD hook kept   (the fail-open arm)
#        tallh  synced + the canonical layout-aware hook (its own commit) + --tier all
#        tallx  as tallh, plus the real tree's non-tracked files copied in (ignored: dashboard.html, __pycache__/)
# The adopter has no tests, no CI and no declared gate; its own checks are context_budget.py (a ceiling on the files a
# session reads), the dashboard, and a LATER commit through the hook (plan C5's case X2).
# Unlike P14's script a refusal by bin/sync is NOT forced: it is logged and the arm stops (F7 / F19: match first).
set -u
S=${SCRATCH:?set SCRATCH to a scratch directory}
R=$S/p16
A=$HOME/Development/chat_verification
M=$HOME/Development/methodology
TRAILER='Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>'
rm -rf "$R"; mkdir -p "$R"
exec > "$R/log.txt" 2>&1
printf 'start %s\n' "$(date)"
printf 'adopter HEAD %s\n' "$(git -C "$A" rev-parse HEAD)"
printf 'source HEAD  %s\n' "$(git -C "$M" rev-parse HEAD)"
printf 'adopter core.hooksPath=[%s]; status: [%s]\n' "$(git -C "$A" config core.hooksPath)" "$(git -C "$A" status --porcelain | tr '\n' ' ')"

for n in base ctrl t1 tall tallh tallx; do
  git clone -q --no-local "$A" "$R/$n"
  git -C "$R/$n" config core.hooksPath .githooks
done
# tallx: the real tree's non-tracked files (both ignored by the project's .gitignore).
cp -Rp "$A/__pycache__" "$R/tallx/__pycache__"
cp -p "$A/dashboard.html" "$R/tallx/"
( cd "$R/tallx" && shasum -a 256 dashboard.html $(find __pycache__ -type f | sort) > "$R/tallx.nontracked.before.sha" )
printf 'tallx non-tracked files hashed: %s\n' "$(wc -l < "$R/tallx.nontracked.before.sha" | tr -d ' ')"
printf 'tallx status before sync: [%s]\n' "$(git -C "$R/tallx" status --porcelain | tr '\n' ' ')"

# the hand-written ledger entry, in the adopter's own format, below its "Entries go below" line
ledger_entry() {  # ledger_entry <ledger path> <title> <change>
  python3 - "$1" "$2" "$3" <<'PYEOF'
import sys
p, title, change = sys.argv[1:4]
t = open(p, encoding="utf-8").read()
anchor = "<!-- Entries go below, newest on top. -->\n\n"
assert t.count(anchor) == 1, "anchor not found exactly once in %s" % p
entry = ("### 2026-10-11 · [ad hoc] %s\n- **Change:** %s\n- **Commit/PR:** this commit\n"
         "- **Session:** rehearsal · **Verified:** n/a\n\n" % (title, change))
open(p, "w", encoding="utf-8").write(t.replace(anchor, anchor + entry))
PYEOF
}

probe() {  # probe <dir> <label>: a LATER commit, with no ledger entry, then with one. Undone in the scratch clone.
  [ -d "$1/.git" ] || { printf 'probe %s: no clone\n' "$2"; return; }
  ( cd "$1" || exit
    L=CHANGELOG.md; [ -f methodology/CHANGELOG.md ] && L=methodology/CHANGELOG.md
    mkdir -p docs/planning
    printf 'probe\n' >> docs/planning/probe.txt; git add docs/planning/probe.txt
    git commit -q -m "probe: tracked content, no ledger entry" > "$R/$2.probe-noledger.txt" 2>&1; rc=$?
    printf 'probe %s (tracked content, NO ledger entry, ledger at %s) exit=%s\n' "$2" "$L" "$rc"
    if [ "$rc" -eq 0 ]; then git reset -q --hard HEAD~1; else git reset -q; rm -f docs/planning/probe.txt; fi
    git status --porcelain | sed 's/^/    leftover: /'
    mkdir -p docs/planning   # a passing first probe is reset away with its directory
    printf 'probe\n' >> docs/planning/probe.txt; git add docs/planning/probe.txt
    ledger_entry "$L" "probe entry" "a probe commit" ; git add "$L"
    git commit -q -m "probe: tracked content and a ledger entry" > "$R/$2.probe-ledger.txt" 2>&1; rc=$?
    printf 'probe %s (tracked content WITH a ledger entry) exit=%s\n' "$2" "$rc"
    if [ "$rc" -eq 0 ]; then git reset -q --hard HEAD~1; else git reset -q --hard HEAD; fi )
}

strip() { sed 's/\x1b\[[0-9;]*m//g'; }

reads() {  # reads <dir> <label>: the project's own checks, run from its root, in whichever layout it has
  ( cd "$1" || exit
    cb=context_budget.py; [ -f methodology/context_budget.py ] && cb=methodology/context_budget.py
    python3 "$cb" --status > "$R/$2.budget.txt" 2>&1; printf 'context_budget --status %s exit=%s\n' "$2" "$?"
    "$M/bin/check-ledger" > "$R/$2.check-ledger.txt" 2>&1; printf 'check-ledger %s exit=%s  %s\n' "$2" "$?" "$(head -1 "$R/$2.check-ledger.txt" | cut -c1-90)"
    "$M/bin/check-handoff" > "$R/$2.check-handoff.txt" 2>&1; printf 'check-handoff %s exit=%s  %s\n' "$2" "$?" "$(head -1 "$R/$2.check-handoff.txt" | cut -c1-90)" )
}

# base: before anything (the adopter's own copy of the tools)
( cd "$R/base" && python3 methodology_dashboard.py --no-open > "$R/base.dash.txt" 2>&1; printf 'dash base exit=%s\n' "$?" )
"$M/bin/status" "$R/base" > "$R/base.status.txt" 2>&1; printf 'status base exit=%s\n' "$?"
reads "$R/base" base
probe "$R/base" base

# the sync, WITHOUT --force: a dry run in ctrl alone, so a refusal (if any) is read before anything is applied
"$M/bin/sync" --dry-run "$R/ctrl" > "$R/ctrl.sync-dry.txt" 2>&1; printf 'sync --dry-run ctrl exit=%s\n' "$?"

for n in ctrl t1 tall tallh tallx; do
  "$M/bin/sync" "$R/$n" > "$R/$n.sync.txt" 2>&1; rc=$?
  printf 'sync %s (no --force) exit=%s\n' "$n" "$rc"
  if [ "$rc" -ne 0 ]; then printf 'REFUSED in %s: not forced (F7/F19); the arm stops after the sync\n' "$n"; continue; fi
  ledger_entry "$R/$n/CHANGELOG.md" "Methodology sync (rehearsal text)" "bin/sync wrote the methodology files."
  git -C "$R/$n" add -A
  git -C "$R/$n" commit -q -m "chore(methodology): sync" > "$R/$n.sync-commit.txt" 2>&1; printf 'commit %s (sync, OLD hook armed) exit=%s\n' "$n" "$?"
  printf '  %s status after sync: [%s]\n' "$n" "$(git -C "$R/$n" status --porcelain | tr '\n' ' ')"
done

reads "$R/ctrl" ctrl
# the control, unmoved, with the adopter's old hook: a later commit with no ledger entry is refused (plan C5)
probe "$R/ctrl" ctrl

# the hook replacement, its own commit, in the arms that take it
for n in tallh tallx; do
  cp -p "$M/.githooks/pre-commit" "$R/$n/.githooks/pre-commit"
  ledger_entry "$R/$n/CHANGELOG.md" "Replaced the ledger hook with the layout-aware one" ".githooks/pre-commit now follows the ledger under methodology/."
  git -C "$R/$n" add -A
  git -C "$R/$n" commit -q -m "chore(hooks): replace the ledger hook with the layout-aware one" > "$R/$n.hook-commit.txt" 2>&1; printf 'commit %s (hook replaced) exit=%s\n' "$n" "$?"
done
( cd "$R/tallh" && sh .githooks/pre-commit --selftest > "$R/tallh.hook-selftest.txt" 2>&1; printf 'hook --selftest (tallh) exit=%s  %s\n' "$?" "$(tail -1 "$R/tallh.hook-selftest.txt")" )

for n in t1 tall tallh tallx; do
  t=all; [ "$n" = t1 ] && t=1
  "$M/bin/migrate-layout" "$R/$n" --tier $t > "$R/$n.migrate-dry.txt" 2>&1; printf 'migrate dry-run %s exit=%s\n' "$n" "$?"
  "$M/bin/migrate-layout" "$R/$n" --tier $t --apply --trailer "$TRAILER" > "$R/$n.migrate.txt" 2>&1; printf 'migrate --apply %s (tier %s) exit=%s\n' "$n" "$t" "$?"
  printf '  %s status after the move: [%s]  HEAD %s\n' "$n" "$(git -C "$R/$n" status --porcelain | tr '\n' ' ')" "$(git -C "$R/$n" log --oneline -1 | cut -c1-70)"
done

# tallx straight after the move: the non-tracked files, by sha256, and the tree
( cd "$R/tallx"
  while read -r want f; do
    if [ -e "$f" ]; then at="$f"; elif [ -e "methodology/$f" ]; then at="methodology/$f"; else at=""; fi
    if [ -z "$at" ]; then printf 'tallx: %s ABSENT at the root and under methodology/\n' "$f"; continue; fi
    got=$(shasum -a 256 "$at" | awk '{print $1}')
    [ "$want" = "$got" ] && printf 'tallx: %s intact at %s (%s)\n' "$f" "$at" "${got:0:12}" || printf 'tallx: %s DIFFERS at %s (want %s got %s)\n' "$f" "$at" "${want:0:12}" "${got:0:12}"
  done < "$R/tallx.nontracked.before.sha"
  printf 'tallx: git status --porcelain after the move: [%s]\n' "$(git status --porcelain | tr '\n' ' ')" )

for n in t1 tall tallh tallx; do reads "$R/$n" "$n"; done

# the LATER commit, after the move: the adopter's old hook (tall) against the layout-aware one (tallh, tallx)
for n in tall tallh tallx; do probe "$R/$n" "$n"; done

# where did the tool's ledger entry land (F8)? line numbers of the 2026-10 entries, first four
for n in ctrl tall tallh; do
  L=CHANGELOG.md; [ -f "$R/$n/methodology/CHANGELOG.md" ] && L=methodology/CHANGELOG.md
  printf '%s: ledger %s, first dated entries after the "Entries go below" line:\n' "$n" "$L"
  awk '/Entries go below, newest on top/{f=1;next} f&&/^### 20/{print NR": "substr($0,1,140)}' "$R/$n/$L" | head -4 | sed 's/^/    /'
done

# the ratchet in each arm that has the tool (it writes where it lives)
( cd "$R/ctrl" && python3 quality_ratchet.py --run > "$R/ctrl.ratchet.txt" 2>&1; printf 'ratchet ctrl exit=%s  %s\n' "$?" "$(strip < "$R/ctrl.ratchet.txt" | grep 'quality_ratchet:' | sed 's/.*quality_ratchet: //')" )
for n in t1 tall tallh tallx; do
  ( cd "$R/$n" && python3 methodology/quality_ratchet.py --run > "$R/$n.ratchet.txt" 2>&1; printf 'ratchet %s exit=%s  %s\n' "$n" "$?" "$(strip < "$R/$n.ratchet.txt" | grep 'quality_ratchet:' | sed 's/.*quality_ratchet: //')" )
done
for n in ctrl t1 tall tallh tallx; do
  "$M/bin/status" "$R/$n" > "$R/$n.status.txt" 2>&1; printf 'status %s exit=%s  %s\n' "$n" "$?" "$(strip < "$R/$n.status.txt" | grep '^layout:' | tr -s ' ')"
done
for n in t1 tallh; do
  "$M/bin/check-links" --tree "$R/$n" > "$R/$n.links.txt" 2>&1; printf 'check-links %s exit=%s\n' "$n" "$?"
done

# the dashboard in each arm (it writes where it lives; last, because it appends to the tracked history)
( cd "$R/ctrl" && python3 methodology_dashboard.py --no-open > "$R/ctrl.dash.txt" 2>&1; printf 'dash ctrl exit=%s\n' "$?" )
for n in t1 tall tallh tallx; do
  ( cd "$R/$n" && python3 methodology/methodology_dashboard.py --no-open > "$R/$n.dash.txt" 2>&1; printf 'dash %s exit=%s\n' "$n" "$?" )
done
for n in base ctrl t1 tall tallh tallx; do printf '  dashboard %s: %s\n' "$n" "$(strip < "$R/$n.dash.txt" | grep 'Health:' | tr -s ' ')"; done

printf 'done %s\n' "$(date)"
touch "$R/DONE"
