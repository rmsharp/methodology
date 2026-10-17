#!/bin/bash
# For every frozen shard in THIS fork: --reverify exit under the PR tip's trimmer (1.7.0) and under the changed one (1.8.0).
S=$1; OLD=$2; NEW=$3; OUT=$4
cd /Users/rmsharp/Development/methodology || exit 9
rm -f "$OUT/done" "$OUT/compare.tsv"
for s in $(git ls-files 'docs/archive/*.md' | grep -E '/(HANDOFFS|CHANGELOG)-through-'); do
  python3 -I "$OLD" --reverify "$s" > "$OUT/$(basename $s).old.txt" 2>&1; a=$?
  python3 -I "$NEW" --reverify "$s" > "$OUT/$(basename $s).new.txt" 2>&1; b=$?
  printf '%s\t%s\t%s\n' "$s" "$a" "$b" >> "$OUT/compare.tsv"
done
echo "finished $(wc -l < "$OUT/compare.tsv") shards" > "$OUT/done"
