#!/bin/bash
# P15 rehearsal: nprcgenekeepr, in --no-local clones only. The real repository is only cloned and read.
# Arms:  base   unsynced control, the project's own per-clone hook copied in
#        ctrl   synced (--force for the one locally modified file), old hook
#        t1     synced + --tier 1, old hook
#        t1h    synced + the hook rewritten by `context_budget.py install-hook` + --tier 1
#        tall   synced + --tier all, the adopter's OLD context-budget hook kept
#        tallh  synced + the hook rewritten by `context_budget.py install-hook` + --tier all
#        tallx  as tallh, plus the real tree's non-tracked files copied in (4 ignored generated files, .claude/settings.local.json)
# The hook is the point of this adopter: it has NO tracked hook and core.hooksPath is unset, but .git/hooks/pre-commit
# (238 B, 2026-09-19, untracked, per clone) runs `python3 "$(git rev-parse --show-toplevel)/context_budget.py" --precommit`,
# a root path. A clone does not inherit it, so every arm gets it copied in by hand.
set -u
S=${SCRATCH:?set SCRATCH to a scratch directory}
R=$S/p15
A=$HOME/Development/nprcgenekeepr
M=$HOME/Development/methodology
TRAILER='Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>'
rm -rf "$R"; mkdir -p "$R"
exec > "$R/log.txt" 2>&1
printf 'start %s\n' "$(date)"
printf 'adopter HEAD %s on %s\n' "$(git -C "$A" rev-parse HEAD)" "$(git -C "$A" rev-parse --abbrev-ref HEAD)"
printf 'source HEAD  %s\n' "$(git -C "$M" rev-parse HEAD)"
printf 'adopter core.hooksPath=[%s]; status: [%s]\n' "$(git -C "$A" config core.hooksPath)" "$(git -C "$A" status --porcelain | tr '\n' ' ')"
cp -p "$A/.git/hooks/pre-commit" "$R/real-hook.sh"
shasum -a 256 "$R/real-hook.sh" | cut -c1-16

ledger_entry() {  # ledger_entry <ledger path> <title> <change>: under the 2026-10 heading, newest on top
  python3 - "$1" "$2" "$3" <<'PYEOF'
import re, sys
p, title, change = sys.argv[1:4]
t = open(p, encoding="utf-8").read()
m = re.search(r"^## 2026-10\n\n", t, re.M)
entry = "### 2026-10-11 · [ad hoc] %s: %s\n\n" % (title, change)
open(p, "w", encoding="utf-8").write(t[:m.end()] + entry + t[m.end():])
PYEOF
}

for n in base ctrl t1 t1h tall tallh tallx; do
  git clone -q --no-local "$A" "$R/$n"
  cp -p "$R/real-hook.sh" "$R/$n/.git/hooks/pre-commit"
done
# tallx: the real tree's non-tracked files
for f in .context-budget-history.jsonl .quality-gates-results.json dashboard.html dashboard_history.jsonl; do cp -p "$A/$f" "$R/tallx/$f"; done
mkdir -p "$R/tallx/.claude"; cp -p "$A/.claude/settings.local.json" "$R/tallx/.claude/settings.local.json"
( cd "$R/tallx" && shasum -a 256 .context-budget-history.jsonl .quality-gates-results.json dashboard.html dashboard_history.jsonl .claude/settings.local.json > "$R/tallx.nontracked.before.sha" )
printf 'tallx status before sync: [%s]\n' "$(git -C "$R/tallx" status --porcelain | tr '\n' ' ')"

# base: the adopter's own tools, before anything
"$M/bin/status" "$R/base" > "$R/base.status.txt" 2>&1; printf 'status base exit=%s\n' "$?"
( cd "$R/base" && python3 methodology_dashboard.py --no-open > "$R/base.dash.txt" 2>&1; printf 'dash base exit=%s\n' "$?" )
git -C "$R/base" checkout -q -- dashboard_history.jsonl 2>/dev/null

# the sync: dry run and WITHOUT --force first in ctrl alone, so the refusal is read before it is overridden
"$M/bin/sync" --dry-run "$R/ctrl" > "$R/ctrl.sync-dry.txt" 2>&1; printf 'sync --dry-run ctrl exit=%s\n' "$?"
for n in ctrl t1 t1h tall tallh tallx; do
  "$M/bin/sync" "$R/$n" > "$R/$n.sync.txt" 2>&1; rc=$?
  printf 'sync %s (no --force) exit=%s\n' "$n" "$rc"
  if [ "$rc" -ne 0 ]; then
    "$M/bin/sync" --force "$R/$n" > "$R/$n.sync-force.txt" 2>&1; printf 'sync %s --force exit=%s\n' "$n" "$?"
  fi
  ledger_entry "$R/$n/CHANGELOG.md" "Synced the methodology files (rehearsal text)" "bin/sync wrote the methodology files."
  git -C "$R/$n" add -A
  git -C "$R/$n" commit -q -m "chore(methodology): sync framework update from canonical" > "$R/$n.sync-commit.txt" 2>&1; printf 'commit %s (sync, old hook armed) exit=%s\n' "$n" "$?"
  printf '  %s status after sync: [%s]\n' "$n" "$(git -C "$R/$n" status --porcelain | tr '\n' ' ')"
done

# the hook rewritten, in the arms that take it (untracked, so no commit)
for n in t1h tallh tallx; do
  ( cd "$R/$n" && python3 context_budget.py install-hook > "$R/$n.install-hook.txt" 2>&1; printf 'install-hook %s exit=%s\n' "$n" "$?" )
  cp -p "$R/$n/.git/hooks/pre-commit" "$R/$n.hook-after.sh"
done
sed -n 1,12p "$R/tallh.hook-after.sh" > "$R/tallh.hook-after.head.txt"

for n in t1 t1h tall tallh tallx; do
  t=all; [ "$n" = t1 ] && t=1; [ "$n" = t1h ] && t=1
  "$M/bin/migrate-layout" "$R/$n" --tier $t > "$R/$n.migrate-dry.txt" 2>&1; printf 'migrate dry-run %s exit=%s\n' "$n" "$?"
  "$M/bin/migrate-layout" "$R/$n" --tier $t --apply --trailer "$TRAILER" > "$R/$n.migrate.txt" 2>&1; printf 'migrate --apply %s (tier %s) exit=%s\n' "$n" "$t" "$?"
  printf '  %s HEAD subject: %s\n' "$n" "$(git -C "$R/$n" log -1 --format=%s | cut -c1-90)"
  printf '  %s status after: [%s]\n' "$n" "$(git -C "$R/$n" status --porcelain | head -5 | tr '\n' ' ')"
done

# tallx straight after the move: the non-tracked files, by sha256
( cd "$R/tallx"
  for f in .context-budget-history.jsonl .quality-gates-results.json dashboard.html dashboard_history.jsonl; do
    want=$(grep -F " $f" "$R/tallx.nontracked.before.sha" | awk '{print $1}')
    if [ -e "$f" ]; then got=$(shasum -a 256 "$f" | awk '{print $1}'); printf 'tallx: %s STILL AT THE ROOT (%s)\n' "$f" "$([ "$want" = "$got" ] && echo intact || echo DIFFERS)"; fi
    got=$(shasum -a 256 "methodology/$f" 2>/dev/null | awk '{print $1}')
    [ -n "$got" ] && printf 'tallx: methodology/%s %s\n' "$f" "$([ "$want" = "$got" ] && echo intact || echo DIFFERS)"
  done
  got=$(shasum -a 256 .claude/settings.local.json 2>/dev/null | awk '{print $1}'); want=$(grep -F ' .claude/settings.local.json' "$R/tallx.nontracked.before.sha" | awk '{print $1}')
  printf 'tallx: .claude/settings.local.json %s\n' "$([ "$want" = "$got" ] && echo intact || echo DIFFERS)" )

# a LATER commit through the project's hook, after the move: the old hook (tall) against the rewritten one (tallh, tallx)
probe() {  # probe <dir> <label>
  ( cd "$1" || exit
    mkdir -p inst; printf 'probe\n' >> inst/probe.txt; git add inst/probe.txt
    git commit -q -m "probe: a small tracked file" > "$R/$2.probe-small.txt" 2>&1; rc=$?
    printf 'probe %s (a small tracked file) exit=%s\n' "$2" "$rc"
    if [ "$rc" -eq 0 ]; then git reset -q --hard HEAD~1; else git reset -q; rm -f inst/probe.txt; fi
    size=$(wc -c < CLAUDE.md); pad=$(( 28500 - size )); [ "$pad" -lt 100 ] && pad=100
    python3 -c "open('CLAUDE.md','a').write('\n' + 'x'*$pad + '\n')"; git add CLAUDE.md
    git commit -q -m "probe: CLAUDE.md grows past its 28,000 B ceiling" > "$R/$2.probe-grow.txt" 2>&1; rc=$?
    printf 'probe %s (CLAUDE.md %s B -> %s B, ceiling 28000) exit=%s\n' "$2" "$size" "$(wc -c < CLAUDE.md)" "$rc"
    if [ "$rc" -eq 0 ]; then git reset -q --hard HEAD~1; else git reset -q --hard HEAD; fi
    git status --porcelain | sed 's/^/    leftover: /' )
}
for n in ctrl t1h tallh tallx; do probe "$R/$n" "$n"; done

for n in ctrl t1 t1h tall tallh tallx; do
  "$M/bin/status" "$R/$n" > "$R/$n.status.txt" 2>&1; printf 'status %s exit=%s\n' "$n" "$?"
done
printf 'done %s\n' "$(date)"
touch "$R/DONE"
