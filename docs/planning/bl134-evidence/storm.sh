#!/usr/bin/env bash
# 16 copies of bl134-measure.sh at once for ONE site: a fork storm of short-lived processes, the load that parallel
# test suites make (bl133-diagnosis-evidence/storm.sh is the same idea; a CPU spinner is NOT this load).
# Usage: bash storm.sh SITE N [MODE] [COPIES]   MODE is loop (default: the exact pipeline) or amp (a reader that quits
#        after one byte); N is runs PER COPY; COPIES defaults to 16. Prints each copy's line that was not clean, then
#        the totals and the machine's load at the end.
S="${1:?site}"; N="${2:-500}"; MODE="${3:-loop}"; C="${4:-16}"
HERE="$(cd "$(dirname "$0")" && pwd)"; T="$(mktemp -d)"
for k in $(seq 1 "$C"); do bash "$HERE/bl134-measure.sh" "$MODE" "$S" "$N" > "$T/$k.out" 2>&1 & done
wait
grep -h 'site=' "$T"/*.out | grep -v 'statuses: none' | cut -c1-220
bad=$(grep -h 'site=' "$T"/*.out | grep -c . ); broken=$(grep -l 'FIXTURE-BROKEN' "$T"/*.out 2>/dev/null | wc -l | tr -d ' ')
grep -h 'site=' "$T"/*.out | sed -E 's/.*sigpipe=([0-9]+).*/\1/' | awk -v n="$N" -v s="$S" -v m="$MODE" -v c="$C" \
    '{k+=$1; r+=n} END{printf "TOTAL site=%s mode=%s copies=%d pipelines=%d sigpipe=%d\n", s, m, c, r, k}'
[ "$broken" != 0 ] && echo "WARNING: $broken copy(ies) reported FIXTURE-BROKEN"
echo "load at the end: $(uptime | sed 's/.*load averages*: //')"
rm -rf "$T"
