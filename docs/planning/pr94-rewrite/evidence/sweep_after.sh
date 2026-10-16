#!/bin/bash
# usage: sweep_after.sh REPO_DIR TRIM_TOOL OUT_DIR SHARD_LIST
# AFTER only: TRIM_TOOL --reverify <shard> for every shard; writes OUT_DIR/summary.tsv and OUT_DIR/done.
set -u
R=$1; T=$2; OUT=$3; LIST=$4
rm -rf "$OUT"; mkdir -p "$OUT"
cd "$R" || { echo "no repo" > "$OUT/done"; exit 9; }
n=0
while IFS= read -r s; do
  n=$((n+1))
  b=$(basename "$s")
  python3 -I "$T" --reverify "$s" > "$OUT/$b.after.txt" 2>&1; arc=$?
  printf '%s\t%s\n' "$s" "$arc" >> "$OUT/summary.tsv"
done < "$LIST"
echo "finished $n shards" > "$OUT/done"
