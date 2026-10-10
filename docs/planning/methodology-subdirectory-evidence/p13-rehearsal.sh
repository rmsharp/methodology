#!/bin/bash
# P13 rehearsal: airqino, in --no-local clones only. The real repository is only cloned and read.
# Arms: base (unsynced), ctrl (synced), t1 (synced + --tier 1), tall (synced + --tier all),
#       tallx (as tall, plus the real tree's four untracked files copied in and excluded locally,
#              which is the state the real apply needs: the tool refuses a dirty tree, untracked files included),
#       tallm (as tallx, with the three generated files' NEW names excluded as well: the first run of tallx read
#              "clean tree: NO" after the move, because the moved files sit untracked at methodology/).
# Every arm that is synced gets a hand-written sync entry under a new `## 2026-10` heading, the project's own
# convention (CLAUDE.md, "Legacy layout, left as written"), so the tool's entry is placed against the real shape.
# The adopter's own build equivalent is `python3 -m pytest -q` (its gates tests-exit and tests-passed run the same
# command). It has no CI, no hooks (core.hooksPath unset, .git/hooks empty) and no moved path in a gate command.
set -u
S=${SCRATCH:?set SCRATCH to a scratch directory}
R=$S/p13
A=$HOME/Development/airqino
M=$HOME/Development/methodology
UNTRACKED=".context-budget-history.jsonl .quality-gates-results.json dashboard_history.jsonl docs/HARDWARE.html"
rm -rf "$R"; mkdir -p "$R"
exec > "$R/log.txt" 2>&1
printf 'start %s\n' "$(date)"
printf 'adopter HEAD %s\n' "$(git -C "$A" rev-parse HEAD)"
printf 'source HEAD  %s\n' "$(git -C "$M" rev-parse HEAD)"

for n in base ctrl t1 tall tallx tallm; do git clone -q --no-local "$A" "$R/$n"; done
for f in $UNTRACKED; do
  cp -p "$A/$f" "$R/tallx/$f"
  printf '/%s\n' "$f" >> "$R/tallx/.git/info/exclude"
done
for f in $UNTRACKED; do cp -p "$A/$f" "$R/tallm/$f"; printf '/%s\n' "$f" >> "$R/tallm/.git/info/exclude"; done
for f in .context-budget-history.jsonl .quality-gates-results.json dashboard_history.jsonl; do printf '/methodology/%s\n' "$f" >> "$R/tallm/.git/info/exclude"; done
( cd "$R/tallx" && shasum -a 256 $UNTRACKED > "$R/tallx.untracked.before.sha" )
cp "$R/tallx.untracked.before.sha" "$R/tallm.untracked.before.sha"
printf 'tallx status before sync: [%s]\n' "$(git -C "$R/tallx" status --porcelain | tr '\n' ' ')"

tests() {  # tests <dir> <label>
  ( cd "$1" && python3 -m pytest -q > "$R/$2.pytest.txt" 2>&1; printf 'pytest %s exit=%s  %s\n' "$2" "$?" "$(tail -1 "$R/$2.pytest.txt")" )
}
ratchet() {  # ratchet <dir> <label> <path to quality_ratchet.py inside it>
  ( cd "$1" && python3 "$3" --run > "$R/$2.ratchet.txt" 2>&1; printf 'ratchet %s exit=%s  %s\n' "$2" "$?" "$(tail -1 "$R/$2.ratchet.txt")" )
}

tests "$R/base" base
ratchet "$R/base" base quality_ratchet.py
"$M/bin/status" "$R/base" > "$R/base.status.txt" 2>&1; printf 'status base exit=%s\n' "$?"

# the sync, WITHOUT --force first, in ctrl alone, so the refusal (if any) is read before it is overridden
"$M/bin/sync" --dry-run "$R/ctrl" > "$R/ctrl.sync-dry.txt" 2>&1; printf 'sync --dry-run ctrl exit=%s\n' "$?"

# the hand-written sync entry: a new `## 2026-10` heading and the entry under it, above the first entry.
# (The real commit's entry carries the real counts and results; this one has the same shape.)
sync_entry() {  # sync_entry <dir>
  python3 - "$1/CHANGELOG.md" <<'PYEOF'
import re, sys
p = sys.argv[1]
t = open(p, encoding="utf-8").read()
m = re.search(r"^### \d{4}-\d{2}-\d{2} \u00b7 ", t, re.M)
entry = ("## 2026-10\n\n### 2026-10-10 \u00b7 [ad hoc] Methodology sync (rehearsal text)\n"
         "- **Change:** `bin/sync` wrote the methodology files.\n- **Commit/PR:** this commit\n"
         "- **Session:** rehearsal \u00b7 **Verified:** n/a\n- **Model:** n/a\n\n")
open(p, "w", encoding="utf-8").write(t[:m.start()] + entry + t[m.start():])
PYEOF
}

for n in ctrl t1 tall tallx tallm; do
  "$M/bin/sync" "$R/$n" > "$R/$n.sync.txt" 2>&1; rc=$?
  printf 'sync %s (no --force) exit=%s\n' "$n" "$rc"
  if [ "$rc" -ne 0 ]; then
    "$M/bin/sync" --force "$R/$n" > "$R/$n.sync-force.txt" 2>&1; printf 'sync %s --force exit=%s\n' "$n" "$?"
  fi
  sync_entry "$R/$n"
  git -C "$R/$n" add -A
  git -C "$R/$n" commit -q -m "chore(methodology): sync"; printf 'commit %s exit=%s\n' "$n" "$?"
  printf '  %s status after sync: [%s]\n' "$n" "$(git -C "$R/$n" status --porcelain | tr '\n' ' ')"
done

for n in t1 tall tallx tallm; do
  t=all; [ "$n" = t1 ] && t=1
  "$M/bin/migrate-layout" "$R/$n" --tier $t > "$R/$n.migrate-dry.txt" 2>&1; printf 'migrate dry-run %s exit=%s\n' "$n" "$?"
  "$M/bin/migrate-layout" "$R/$n" --tier $t --apply > "$R/$n.migrate.txt" 2>&1; printf 'migrate --apply %s (tier %s) exit=%s\n' "$n" "$t" "$?"
done

# tallx and tallm, straight after the move (the ratchet and the dashboard rewrite two of these files later):
# did the four untracked files arrive intact, by sha256, where the tool put them? and is the tree clean?
for n in tallx tallm; do
  ( cd "$R/$n" && for f in .context-budget-history.jsonl .quality-gates-results.json dashboard_history.jsonl; do
      [ -e "$f" ] && printf '%s: %s STILL AT THE ROOT\n' "$n" "$f"
      want=$(grep -F " $f" "$R/$n.untracked.before.sha" | awk '{print $1}')
      got=$(shasum -a 256 "methodology/$f" 2>/dev/null | awk '{print $1}')
      [ "$want" = "$got" ] && printf '%s: methodology/%s intact (sha256 %s)\n' "$n" "$f" "${got:0:12}" || printf '%s: methodology/%s DIFFERS or is absent (want %s got %s)\n' "$n" "$f" "${want:0:12}" "${got:0:12}"
    done
    want=$(grep -F ' docs/HARDWARE.html' "$R/$n.untracked.before.sha" | awk '{print $1}')
    got=$(shasum -a 256 docs/HARDWARE.html 2>/dev/null | awk '{print $1}')
    [ "$want" = "$got" ] && printf '%s: docs/HARDWARE.html in place and intact (sha256 %s)\n' "$n" "${got:0:12}" || printf '%s: docs/HARDWARE.html DIFFERS or is absent\n' "$n"
    printf '%s: git status --porcelain after the move: [%s]\n' "$n" "$(git status --porcelain | tr '\n' ' ')" )
done

# where did the tool's ledger entry land, against the hand-written sync entry and its month heading?
for n in tall tallm; do
  printf '%s: ledger order after the move (headings and entry titles, first 6):\n' "$n"
  grep -n -E '^## |^### ' "$R/$n/methodology/CHANGELOG.md" | head -6 | cut -c1-150 | sed 's/^/    /'
done

tests "$R/ctrl" ctrl
ratchet "$R/ctrl" ctrl quality_ratchet.py
for n in t1 tall tallx tallm; do
  tests "$R/$n" "$n"
  ratchet "$R/$n" "$n" methodology/quality_ratchet.py
done
for n in ctrl t1 tall tallx tallm; do
  "$M/bin/status" "$R/$n" > "$R/$n.status.txt" 2>&1; printf 'status %s exit=%s\n' "$n" "$?"
done

# the dashboard in each arm (it writes where it lives)
( cd "$R/ctrl" && python3 methodology_dashboard.py --no-open > "$R/ctrl.dash.txt" 2>&1; printf 'dash ctrl exit=%s\n' "$?" )
for n in t1 tall tallx tallm; do
  ( cd "$R/$n" && python3 methodology/methodology_dashboard.py --no-open > "$R/$n.dash.txt" 2>&1; printf 'dash %s exit=%s\n' "$n" "$?" )
done

printf 'done %s\n' "$(date)"
touch "$R/DONE"
