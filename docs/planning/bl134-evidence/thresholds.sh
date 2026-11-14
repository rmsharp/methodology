#!/usr/bin/env bash
# At what payload size does each producer type used by the 14 sites start writing in more than one piece?
# For each tool and size, 10 runs through a reader that is already waiting (piece-reader.py); prints the distinct
# read patterns. Usage: bash thresholds.sh   (about a minute)
HERE="$(cd "$(dirname "$0")" && pwd)"; T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
reads() { # $1.. the producer command, run in a bash -c after a 60 ms delay; 10 runs; print the distinct patterns
    declare -A t=(); local i r o k
    for ((i = 0; i < 10; i++)); do r="$({ sleep 0.06; bash -c "$1"; } | python3 -I "$HERE/piece-reader.py")"; t["$r"]=$(( ${t["$r"]:-0} + 1 )); done
    o=""; for k in "${!t[@]}"; do o="$o [$k]x${t[$k]}"; done; echo "$o"
}
for S in 4096 8192 8193 16384 16385 32768 65536; do
    python3 -c "
import sys; s=int(sys.argv[1])
open('$T/tr.in','w').write(('word ' * (s // 5 + 1))[:s].replace('word wor', 'word\nwor'))
open('$T/oneline.in','w').write('x' * (s - 1) + '\n')
" "$S"
    echo "== about $S B"
    printf '  %-34s' "tr -s (site :5533)";            reads "tr -s '\\n ' '  ' < $T/tr.in"
    printf '  %-34s' "grep, one line (sites :431/432)"; reads "grep '^x' $T/oneline.in"
    printf '  %-34s' "python print (surface_check,"; echo; printf '  %-34s' "   model-report, status)";   reads "python3 -c \"print('x' * $((S - 1)))\""
    printf '  %-34s' "head -1 (site :4725)";           reads "head -1 $T/oneline.in"
    printf '  %-34s' "bash echo \"\$VAR\" (the BL-133 form)"; reads "V=\$(cat $T/oneline.in); echo \"\$V\""
done
