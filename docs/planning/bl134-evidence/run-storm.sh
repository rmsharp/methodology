#!/usr/bin/env bash
# The storm round: 16 copies at once (a fork storm), bracketed by the stored BL-133 positive control (the same form
# BL-133 found exposed, in the same machine state). Real pipelines first, then the amplified reader on the sites with
# the most bytes. Usage: bash run-storm.sh
HERE="$(cd "$(dirname "$0")" && pwd)"; BL133="$HERE/../bl133-diagnosis-evidence"
ld() { uptime | sed 's/.*load averages*: //'; }
echo "start $(date '+%F %T')  load $(ld)"
echo "== control before: BL-133's storm.sh, echo \"\$OUT\" | grep -q, 16 x 1000"
bash "$BL133/storm.sh" 1000 | tail -3
echo "== the 14 sites, the exact pipeline, 16 copies each"
for pair in s259:400 s397:400 s411:400 s431:400 s432:400 s4725:400 s5533:400 s2318:150 s2326:150 s2335:150 s2343:150 s2351:150 s3377:60 s388:6; do
    bash "$HERE/storm.sh" "${pair%%:*}" "${pair##*:}" loop | grep -v '^load'
done
echo "== the amplified waiting reader (quits after one byte), 16 copies each, the sites with the most bytes"
for pair in s5533:150 s431:150 s432:150 s3377:60 s397:150; do
    bash "$HERE/storm.sh" "${pair%%:*}" "${pair##*:}" amp | grep -v '^load'
done
echo "== control after"
bash "$BL133/storm.sh" 1000 | tail -3
echo "end   $(date '+%F %T')  load $(ld)"
