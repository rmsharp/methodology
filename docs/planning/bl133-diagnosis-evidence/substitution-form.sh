#!/usr/bin/env bash
# BL-97's measured shape: a 1,540 B payload with the match on its SECOND line, three forms, under `set -uo pipefail`.
# Usage: bash substitution-form.sh [N]  (default 3000 per form). Statuses are "echo grep"; here-string has one.
set -uo pipefail
N=${1:-3000}; T="$(mktemp -d)"
python3 - "$T/payload.txt" <<'PY'
import sys
line1 = "a" * 700
line2 = "per-record budget by 3 bytes " + "b" * 40
rest = "c" * (1540 - len(line1) - len(line2) - 2)
open(sys.argv[1], "w").write(line1 + "\n" + line2 + "\n" + rest)
PY
OUT="$(cat "$T/payload.txt")"
echo "payload $(wc -c < "$T/payload.txt") B"
for MODE in subst var here; do
  fails=0; seen=""
  for ((i=0;i<N;i++)); do
    case $MODE in
      subst) echo "$(cat "$T/payload.txt")" | grep -q 'per-record budget by'; st="${PIPESTATUS[*]}" ;;
      var)   echo "$OUT" | grep -q 'per-record budget by'; st="${PIPESTATUS[*]}" ;;
      here)  grep -q 'per-record budget by' <<<"$OUT"; st="${PIPESTATUS[*]}" ;;
    esac
    [ "$st" = "0 0" ] || [ "$st" = "0" ] || { fails=$((fails+1)); seen="$seen [$st]"; }
  done
  printf '%-6s N=%d fails=%d statuses:%s\n' "$MODE" "$N" "$fails" "${seen:- none}" | cut -c1-200
done
rm -rf "$T"
