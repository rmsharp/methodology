#!/usr/bin/env bash
# Does `echo` write a multi-line string in more than one piece? A reader that is already waiting and quits after its
# first byte kills an echo that still has a write to make (status 141). The same bytes on ONE line never do.
# Usage: bash waiting-reader.sh [N]    (default 200 per case)
set -uo pipefail
N=${1:-200}
ML="$(python3 -c "print('\n'.join(['x'*80]*27), end='')")"     # 27 lines
SL="$(python3 -c "print('x'*2186, end='')")"                    # one line, the same size
for label in ML SL; do
  case $label in ML) V="$ML";; SL) V="$SL";; esac
  c0=0; c141=0
  for ((i=0;i<N;i++)); do
    { sleep 0.02; echo "$V"; } | head -c 1 >/dev/null
    st=${PIPESTATUS[0]}
    [ "$st" = 0 ] && c0=$((c0+1)); [ "$st" = 141 ] && c141=$((c141+1))
  done
  echo "$label (${#V} B, $(printf '%s\n' "$V" | wc -l | tr -d ' ') line(s)): echo status 0 x$c0, 141 (SIGPIPE) x$c141 of $N"
done
