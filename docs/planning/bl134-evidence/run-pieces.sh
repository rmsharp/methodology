#!/usr/bin/env bash
# How each of the 14 streams reaches its final `grep -q` (the size of each read by a reader that is already waiting),
# with bash `echo` of 2,186 B as the contrast (the form BL-133 found exposed). Usage: bash run-pieces.sh [N] [N for s388]
N="${1:-60}"; N388="${2:-15}"; HERE="$(cd "$(dirname "$0")" && pwd)"
echo "start $(date '+%F %T')  load $(uptime | sed 's/.*load averages*: //')"
for s in $(bash "$HERE/bl134-measure.sh" list); do
    if [ "$s" = s388 ]; then bash "$HERE/bl134-measure.sh" pieces "$s" "$N388"; else bash "$HERE/bl134-measure.sh" pieces "$s" "$N"; fi
done
for label in SL ML; do
    case $label in SL) V="$(python3 -c "print('x'*2186, end='')")";; ML) V="$(python3 -c "print('\n'.join(['x'*80]*27), end='')")";; esac
    declare -A t=(); for ((i = 0; i < N; i++)); do r="$({ sleep 0.06; echo "$V"; } | python3 -I "$HERE/piece-reader.py")"; t["$r"]=$(( ${t["$r"]:-0} + 1 )); done
    o=""; for k in "${!t[@]}"; do o="$o [$k]x${t[$k]}"; done; echo "contrast bash echo $label (${#V} B) N=$N reads seen:$o"; unset t
done
echo "end   $(date '+%F %T')  load $(uptime | sed 's/.*load averages*: //')"
