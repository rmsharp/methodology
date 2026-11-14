#!/usr/bin/env bash
# Where does `tr -s '\n ' '  ' < starter-kit/HANDOFFS.md` (bin/tests.sh:5533) first write its output in more than one piece?
# S449, BL-134. The real seed text is padded with single-spaced words to each size (padding `tr -s` cannot squeeze away),
# then run ten times into a reader that is ALREADY WAITING (piece-reader.py: the producer starts 60 ms after the reader,
# the arrangement that killed its known positive at S448). Each line prints the distinct read patterns and their counts.
# How to read it: the sizes below are SEED sizes; the stream `tr -s` writes is the seed minus what it squeezes (90 B for
# the real seed: 13,723 B in, 13,633 B out). A stream over 16,384 B shows as [16384, rest]; a split just over the edge can
# hide when the second write lands before the reader's read (S448's thresholds.sh read a 16,385 B stream as one piece 10
# of 10), so the rows just over the edge VARY from run to run (17,000 B: split 1 of 10 in one run, 4 of 10 in another; 18,000 B:
# split 10 of 10, 10 of 10 and 8 of 10 in three runs) and prove nothing either way. The positive control is the large sizes
# (24,000 B and up, [16384, rest] every time): a 16 KiB pipe is full after the first write, so the second cannot land first;
# they show tr writes 16,384 B blocks, which is where the ceiling comes from.
# Usage: bash tr-edge-sweep.sh [REPO_ROOT]     (about 15 s)
HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="${1:-$(cd "$HERE/../../.." && pwd)}"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
SEED="$ROOT/starter-kit/HANDOFFS.md"
reads() { # $1 the producer command; ten runs; print the distinct patterns
    declare -A t=(); local i r o k
    for ((i = 0; i < 10; i++)); do r="$({ sleep 0.06; bash -c "$1"; } | python3 -I "$HERE/piece-reader.py")"; t["$r"]=$(( ${t["$r"]:-0} + 1 )); done
    o=""; for k in "${!t[@]}"; do o="$o [$k]x${t[$k]}"; done; echo "$o"
}
echo "seed bytes: $(wc -c < "$SEED" | tr -d ' '); tr -s stream bytes: $(tr -s '\n ' '  ' < "$SEED" | wc -c | tr -d ' ')"
for S in 13723 16384 16385 17000 18000 20000 24000 28000 32767 32768; do
    python3 -I - "$S" "$SEED" "$T/real.in" <<'PY'
import sys
s = int(sys.argv[1]); seed = open(sys.argv[2], "rb").read()
open(sys.argv[3], "wb").write(seed[:s] if s <= len(seed) else (seed + b"word " * (s // 5 + 2))[:s])
PY
    printf '%6s B seed  ' "$S"; reads "tr -s '\\n ' '  ' < $T/real.in"
done
