#!/usr/bin/env bash
# BL-101 P3: did the trimmer's change alter what `--reverify` says about any OLD shard?
# For every tracked shard in docs/archive/, the verdict of the PREVIOUS tool (read from git at the
# commit named in $1) and of the CURRENT starter-kit/methodology_trim.py, side by side: the exit code
# and the proof's own output, the tool's version string normalised away. `--reverify` is read-only.
# Run from the repo root:   bash docs/planning/methodology-subdirectory-evidence/trim-reverify-differential.sh <previous-tool-commit>
# Takes several minutes (two bash proofs per shard).
set -u
OLD_REF="${1:?usage: trim-reverify-differential.sh <the commit holding the previous methodology_trim.py>}"
SRC="$(git rev-parse --show-toplevel)" || exit 3
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
git -C "$SRC" show "$OLD_REF:starter-kit/methodology_trim.py" > "$T/old_trim.py" || exit 3
cd "$SRC" || exit 3
printf 'previous tool: %s (%s)\ncurrent tool : %s\n' "$OLD_REF" "$(python3 "$T/old_trim.py" --version)" "$(python3 starter-kit/methodology_trim.py --version)"
n=0; same=0; : > "$T/pairs.txt"; : > "$T/diffs.txt"
while read -r shard; do
  n=$((n + 1))
  python3 "$T/old_trim.py" --reverify "$shard" > "$T/o.txt" 2>&1; oc=$?
  python3 starter-kit/methodology_trim.py --reverify "$shard" > "$T/n.txt" 2>&1; nc=$?
  sed -E 's/v1\.[0-9]+\.[0-9]+/vX/g' "$T/o.txt" > "$T/o.norm"; sed -E 's/v1\.[0-9]+\.[0-9]+/vX/g' "$T/n.txt" > "$T/n.norm"
  printf '%s\t%s\n' "$oc" "$nc" >> "$T/pairs.txt"
  if [ "$oc" = "$nc" ] && cmp -s "$T/o.norm" "$T/n.norm"; then same=$((same + 1))
  else printf '%s\told=%s new=%s\n' "$shard" "$oc" "$nc" >> "$T/diffs.txt"; diff "$T/o.norm" "$T/n.norm" | head -6 >> "$T/diffs.txt"; fi
done < <(git ls-files 'docs/archive/*-through-*.md' | sort)
printf 'shards compared: %s, identical verdict and output: %s\n' "$n" "$same"
printf 'histogram of (previous exit, current exit):\n'; sort "$T/pairs.txt" | uniq -c | awk '{printf "  previous exit %s -> current exit %s  x%s\n", $2, $3, $1}'
printf 'differences:\n'; if [ -s "$T/diffs.txt" ]; then cat "$T/diffs.txt"; else printf '  none\n'; fi
[ "$same" = "$n" ]
