#!/bin/bash
# usage: sweep.sh REPO_DIR TRIM_TOOL OUT_DIR SHARD_LIST
# For each shard: BEFORE = its frozen proof run as shipped; AFTER = TRIM_TOOL --reverify <shard>.
# Writes OUT_DIR/summary.tsv (shard, before_rc, after_rc) and OUT_DIR/done when finished.
set -u
R=$1; T=$2; OUT=$3; LIST=$4
mkdir -p "$OUT"
rm -f "$OUT/done" "$OUT/summary.tsv"
cd "$R" || { echo "no repo" > "$OUT/done"; exit 9; }
git sparse-checkout init --no-cone > /dev/null 2>&1
git sparse-checkout set '/docs/archive/' '/CHANGELOG.md' '/HANDOFFS.md' '/SESSION_NOTES.md' > /dev/null 2>&1
git checkout -q --detach 82433662 || { echo "checkout failed" > "$OUT/done"; exit 8; }
n=0
while IFS= read -r s; do
  n=$((n+1))
  b=$(basename "$s")
  bash "$s.verify.sh" > "$OUT/$b.before.txt" 2>&1; brc=$?
  python3 -I "$T" --reverify "$s" > "$OUT/$b.after.txt" 2>&1; arc=$?
  printf '%s\t%s\t%s\n' "$s" "$brc" "$arc" >> "$OUT/summary.tsv"
done < "$LIST"
echo "finished $n shards" > "$OUT/done"
