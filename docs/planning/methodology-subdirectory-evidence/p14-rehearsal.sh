#!/bin/bash
# P14 rehearsal: church_growth, in --no-local clones only. The real repository is only cloned and read.
# Every clone arms the project's ledger hook the way the real tree does (core.hooksPath = .githooks, a per-clone
# setting a clone does not inherit), because the real tree's hook is the thing this adopter adds to the plan:
# register row F2 / plan C5 (the adopter's older ledger hook names CHANGELOG.md at the root and fails open
# once the ledger leaves it).
# Arms:  base   unsynced control
#        ctrl   synced
#        t1     synced + --tier 1
#        tall   synced + --tier all, the adopter's OLD hook kept   (the fail-open arm)
#        tallh  synced + the canonical layout-aware hook (its own commit) + --tier all
#        tallx  as tallh, plus the real tree's non-tracked files copied in (the stray __pycache__/ excluded locally,
#               which is what the real apply needs, and the two ignored generated files)
# The adopter has no tests, no CI and no gates (doc-only, `.methodology-profile`); its build equivalent is the
# dashboard's read of it, the tool's own checks, and a LATER commit through the hook (plan C5's case X2).
set -u
S=${SCRATCH:?set SCRATCH to a scratch directory}
R=$S/p14
A=$HOME/Development/church_growth
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
# tallx: the real tree's non-tracked files. __pycache__/ is untracked (dirt), the two generated files are ignored.
cp -Rp "$A/__pycache__" "$R/tallx/__pycache__"
cp -p "$A/dashboard.html" "$A/dashboard_history.jsonl" "$R/tallx/"
printf '/__pycache__/\n' >> "$R/tallx/.git/info/exclude"
( cd "$R/tallx" && shasum -a 256 __pycache__/methodology_dashboard.cpython-310.pyc dashboard.html dashboard_history.jsonl > "$R/tallx.nontracked.before.sha" )
printf 'tallx status before sync: [%s]\n' "$(git -C "$R/tallx" status --porcelain | tr '\n' ' ')"

# the hand-written ledger entry, in the adopter's own format, above its first dated entry
ledger_entry() {  # ledger_entry <ledger path> <title> <change>
  python3 - "$1" "$2" "$3" <<'PYEOF'
import re, sys
p, title, change = sys.argv[1:4]
t = open(p, encoding="utf-8").read()
m = re.search(r"^### \d{4}-\d{2}-\d{2} · ", t, re.M)
entry = ("### 2026-10-10 · [ad hoc] %s\n- **Change:** %s\n- **Commit/PR:** this commit\n"
         "- **Session:** rehearsal · **Verified:** n/a\n\n" % (title, change))
open(p, "w", encoding="utf-8").write(t[:m.start()] + entry + t[m.start():])
PYEOF
}

probe() {  # probe <dir> <label>: a LATER commit, with no ledger entry, then with one. Undone in the scratch clone.
  [ -d "$1/.git" ] || { printf 'probe %s: no clone\n' "$2"; return; }
  ( cd "$1" || exit
    L=CHANGELOG.md; [ -f methodology/CHANGELOG.md ] && L=methodology/CHANGELOG.md
    printf 'probe\n' >> docs/planning/probe.txt; git add docs/planning/probe.txt
    git commit -q -m "probe: tracked content, no ledger entry" > "$R/$2.probe-noledger.txt" 2>&1; rc=$?
    printf 'probe %s (tracked content, NO ledger entry, ledger at %s) exit=%s\n' "$2" "$L" "$rc"
    if [ "$rc" -eq 0 ]; then git reset -q --hard HEAD~1; else git reset -q; rm -f docs/planning/probe.txt; fi
    git status --porcelain | sed 's/^/    leftover: /'
    printf 'probe\n' >> docs/planning/probe.txt; git add docs/planning/probe.txt
    ledger_entry "$L" "probe entry" "a probe commit" ; git add "$L"
    git commit -q -m "probe: tracked content and a ledger entry" > "$R/$2.probe-ledger.txt" 2>&1; rc=$?
    printf 'probe %s (tracked content WITH a ledger entry) exit=%s\n' "$2" "$rc"
    if [ "$rc" -eq 0 ]; then git reset -q --hard HEAD~1; else git reset -q --hard HEAD; fi )
}
export -f ledger_entry 2>/dev/null || true

# base: the dashboard before anything (the adopter's own copy, 39 versions behind)
( cd "$R/base" && python3 methodology_dashboard.py --no-open > "$R/base.dash.txt" 2>&1; printf 'dash base exit=%s\n' "$?" )
"$M/bin/status" "$R/base" > "$R/base.status.txt" 2>&1; printf 'status base exit=%s\n' "$?"
probe "$R/base" base

# the sync, WITHOUT --force first, in ctrl alone, so a refusal (if any) is read before it is overridden
"$M/bin/sync" --dry-run "$R/ctrl" > "$R/ctrl.sync-dry.txt" 2>&1; printf 'sync --dry-run ctrl exit=%s\n' "$?"

for n in ctrl t1 tall tallh tallx; do
  "$M/bin/sync" "$R/$n" > "$R/$n.sync.txt" 2>&1; rc=$?
  printf 'sync %s (no --force) exit=%s\n' "$n" "$rc"
  if [ "$rc" -ne 0 ]; then
    "$M/bin/sync" --force "$R/$n" > "$R/$n.sync-force.txt" 2>&1; printf 'sync %s --force exit=%s\n' "$n" "$?"
  fi
  ledger_entry "$R/$n/CHANGELOG.md" "Methodology sync (rehearsal text)" "bin/sync wrote the methodology files."
  git -C "$R/$n" add -A
  git -C "$R/$n" commit -q -m "chore(methodology): sync" > "$R/$n.sync-commit.txt" 2>&1; printf 'commit %s (sync, OLD hook armed) exit=%s\n' "$n" "$?"
  printf '  %s status after sync: [%s]\n' "$n" "$(git -C "$R/$n" status --porcelain | tr '\n' ' ')"
done

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
done

# tallx straight after the move: the three non-tracked files, by sha256, and the tree
( cd "$R/tallx"
  want=$(grep -F ' __pycache__/' "$R/tallx.nontracked.before.sha" | awk '{print $1}'); got=$(shasum -a 256 __pycache__/methodology_dashboard.cpython-310.pyc 2>/dev/null | awk '{print $1}')
  [ "$want" = "$got" ] && printf 'tallx: __pycache__ pyc in place and intact (%s)\n' "${got:0:12}" || printf 'tallx: __pycache__ pyc DIFFERS or is absent\n'
  for f in dashboard.html dashboard_history.jsonl; do
    [ -e "$f" ] && printf 'tallx: %s STILL AT THE ROOT\n' "$f"
    want=$(grep -F " $f" "$R/tallx.nontracked.before.sha" | awk '{print $1}'); got=$(shasum -a 256 "methodology/$f" 2>/dev/null | awk '{print $1}')
    [ "$want" = "$got" ] && printf 'tallx: methodology/%s intact (%s)\n' "$f" "${got:0:12}" || printf 'tallx: methodology/%s DIFFERS or is absent (want %s got %s)\n' "$f" "${want:0:12}" "${got:0:12}"
  done
  printf 'tallx: git status --porcelain after the move: [%s]\n' "$(git status --porcelain | tr '\n' ' ')" )

# the LATER commit, after the move: the adopter's old hook (tall) against the layout-aware one (tallh, tallx)
for n in tall tallh tallx; do probe "$R/$n" "$n"; done

# where did the tool's ledger entry land?
for n in tall tallh; do
  printf '%s: ledger order after the move (first 5 entry titles):\n' "$n"
  grep -n -E '^### 20' "$R/$n/methodology/CHANGELOG.md" | head -5 | cut -c1-150 | sed 's/^/    /'
done

# the ratchet in each arm that has the tool (it writes where it lives)
( cd "$R/ctrl" && python3 quality_ratchet.py --run > "$R/ctrl.ratchet.txt" 2>&1; printf 'ratchet ctrl exit=%s  %s\n' "$?" "$(tail -1 "$R/ctrl.ratchet.txt")" )
for n in t1 tall tallh tallx; do
  ( cd "$R/$n" && python3 methodology/quality_ratchet.py --run > "$R/$n.ratchet.txt" 2>&1; printf 'ratchet %s exit=%s  %s\n' "$n" "$?" "$(tail -1 "$R/$n.ratchet.txt")" )
done
for n in ctrl t1 tall tallh tallx; do
  "$M/bin/status" "$R/$n" > "$R/$n.status.txt" 2>&1; printf 'status %s exit=%s\n' "$n" "$?"
done

# the dashboard in each arm (it writes where it lives)
( cd "$R/ctrl" && python3 methodology_dashboard.py --no-open > "$R/ctrl.dash.txt" 2>&1; printf 'dash ctrl exit=%s\n' "$?" )
for n in t1 tall tallh tallx; do
  ( cd "$R/$n" && python3 methodology/methodology_dashboard.py --no-open > "$R/$n.dash.txt" 2>&1; printf 'dash %s exit=%s\n' "$n" "$?" )
done

printf 'done %s\n' "$(date)"
touch "$R/DONE"
