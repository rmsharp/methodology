#!/bin/bash
# P12 rehearsal: feedback-loop-comparison, in --no-local clones only. The real repository is only cloned.
# Arms: base (unsynced), ctrl (synced), t1 (synced + --tier 1), tall (synced + --tier all).
# The adopter's own build equivalent is `quarto render index.qmd` (html + pdf): it has no tests, proofs, CI or remote.
set -u
S=${SCRATCH:?set SCRATCH to a scratch directory}
R=$S/p12
A=$HOME/Development/feedback-loop-comparison
M=$HOME/Development/methodology
rm -rf "$R"; mkdir -p "$R"
exec > "$R/log.txt" 2>&1
printf 'start %s\n' "$(date)"
printf 'adopter HEAD %s\n' "$(git -C "$A" rev-parse HEAD)"
printf 'source HEAD  %s\n' "$(git -C "$M" rev-parse HEAD)"

for n in base ctrl t1 tall; do git clone -q --no-local "$A" "$R/$n"; done

render() {  # render <dir> <label>
  local d=$1 l=$2
  ( cd "$d" && /usr/bin/time -p quarto render index.qmd > "$R/$l.render.txt" 2>&1; printf 'render %s exit=%s\n' "$l" "$?" )
  printf '  warnings in %s: %s\n' "$l" "$(grep -c -i 'warning' "$R/$l.render.txt")"
  ls -l "$d"/index.html "$d"/index.pdf 2>&1 | awk '{print "  " $5, $9}'
}

render "$R/base" base

for n in ctrl t1 tall; do
  "$M/bin/sync" --force "$R/$n" > "$R/$n.sync.txt" 2>&1; printf 'sync %s exit=%s\n' "$n" "$?"
  git -C "$R/$n" add -A
  git -C "$R/$n" commit -q -m "chore(methodology): sync" ; printf 'commit %s exit=%s\n' "$n" "$?"
done

"$M/bin/migrate-layout" "$R/t1" --tier 1 --apply > "$R/t1.migrate.txt" 2>&1;   printf 'migrate t1 exit=%s\n' "$?"
"$M/bin/migrate-layout" "$R/tall" --tier all --apply > "$R/tall.migrate.txt" 2>&1; printf 'migrate tall exit=%s\n' "$?"

for n in ctrl t1 tall; do
  render "$R/$n" "$n"
  "$M/bin/status" "$R/$n" > "$R/$n.status.txt" 2>&1; printf 'status %s exit=%s\n' "$n" "$?"
done

# the dashboard in each arm
( cd "$R/ctrl" && python3 methodology_dashboard.py --no-open > "$R/ctrl.dash.txt" 2>&1; printf 'dash ctrl exit=%s\n' "$?" )
for n in t1 tall; do
  ( cd "$R/$n" && python3 methodology/methodology_dashboard.py --no-open > "$R/$n.dash.txt" 2>&1; printf 'dash %s exit=%s\n' "$n" "$?" )
done

printf 'done %s\n' "$(date)"
touch "$R/DONE"
