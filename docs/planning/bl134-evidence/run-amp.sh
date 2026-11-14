#!/usr/bin/env bash
# The amplified pass over all 14 sites, bracketed by the positive control. Usage: bash run-amp.sh [N] [N for s388]
# s388's producer is a real `bin/status` run (about 3 s each), so it gets a smaller N.
N="${1:-300}"; N388="${2:-60}"; HERE="$(cd "$(dirname "$0")" && pwd)"
echo "start $(date '+%F %T')  load $(uptime | sed 's/.*load averages*: //')"
bash "$HERE/bl134-measure.sh" control 200
for s in $(bash "$HERE/bl134-measure.sh" list); do
    if [ "$s" = s388 ]; then bash "$HERE/bl134-measure.sh" amp "$s" "$N388"; else bash "$HERE/bl134-measure.sh" amp "$s" "$N"; fi
done
bash "$HERE/bl134-measure.sh" control 200
echo "end   $(date '+%F %T')  load $(uptime | sed 's/.*load averages*: //')"
