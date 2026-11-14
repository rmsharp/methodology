#!/usr/bin/env bash
# 16 copies of pipeline-loop.sh at once: a fork storm of short-lived processes, the load that parallel test suites
# make. A CPU spinner is NOT this load: a new short process is scheduled ahead of a spinner (measured: 0 failures
# in 16,000 pipelines at load average 100 with 48 spinners).
# Usage: bash storm.sh [N per copy]    (default 2000; prints each copy's line, then the totals)
N=${1:-2000}; HERE="$(cd "$(dirname "$0")" && pwd)"; T="$(mktemp -d)"
for k in $(seq 1 16); do bash "$HERE/pipeline-loop.sh" "$N" > "$T/$k.out" 2>&1 & done
wait
grep -h 'N=' "$T"/*.out | grep -v 'statuses:none' | cut -c1-220
grep -h 'N=' "$T"/*.out | sed -E 's/.*5c-pattern \(byte ~650\) fails=([0-9]+) +5b-pattern \(byte ~416\) fails=([0-9]+).*/\1 \2/' \
  | awk -v n="$N" '{a+=$1;b+=$2;r+=n} END{print "TOTAL pipelines per pattern=" r "  5c fails=" a "  5b fails=" b}'
echo "load: $(uptime | sed 's/.*load averages*: //')"
rm -rf "$T"
