#!/usr/bin/env bash
# Do the frozen .verify.sh losslessness proofs survive a move of the live ledgers, and of the
# shard directory? Three scratch clones of the CURRENT HEAD: base (nothing moved), A (CHANGELOG.md
# and HANDOFFS.md moved into methodology/), B (A, plus docs/archive moved to methodology/archive).
# Every tracked *.verify.sh is run in each; the exit-code histograms and per-proof differences are
# printed. Read-only against the real repo (it only clones it). Takes several minutes.
# Run from the repo root:   bash docs/planning/methodology-subdirectory-evidence/frozen-proofs.sh
set -u
SRC="$(git rev-parse --show-toplevel)" || exit 3
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
for d in base A B; do
  git clone -q --no-local "$SRC" "$T/$d"
  git -C "$T/$d" config core.hooksPath /dev/null
  git -C "$T/$d" config user.email t@t; git -C "$T/$d" config user.name t; git -C "$T/$d" config commit.gpgsign false
done
( cd "$T/A" && mkdir methodology && git mv CHANGELOG.md methodology/ && git mv HANDOFFS.md methodology/ && git commit -q -m A )
( cd "$T/B" && mkdir methodology && git mv CHANGELOG.md methodology/ && git mv HANDOFFS.md methodology/ \
    && git mv docs/archive methodology/archive && git commit -q -m B )
run() {  # run <clone> <out>
  ( cd "$1" && git ls-files '*.verify.sh' | sort | while read -r f; do
      bash "$f" >/dev/null 2>&1; printf '%s\t%s\n' "$?" "$(basename "$f")"; done ) > "$2"
}
for d in base A B; do run "$T/$d" "$T/out-$d.txt"; done
for d in base A B; do
  printf '%-5s proofs=%s  ' "$d" "$(wc -l < "$T/out-$d.txt" | tr -d ' ')"
  cut -f1 "$T/out-$d.txt" | sort | uniq -c | awk '{printf "exit%s x%s  ", $2, $1}'; printf '\n'
done
for d in A B; do
  n=$(join -t"$(printf '\t')" -j2 <(sort -k2 "$T/out-base.txt") <(sort -k2 "$T/out-$d.txt") \
      | awk -F'\t' '$2!=$3' | wc -l | tr -d ' ')
  printf 'proofs whose exit code differs, base vs %s: %s\n' "$d" "$n"
done
printf 'baseline exit-1 proofs (pre-existing; the BL-36 class):\n'; awk -F'\t' '$1 == 1' "$T/out-base.txt"
