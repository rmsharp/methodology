#!/usr/bin/env bash
# BL-101 P3 runtime check, on REAL data: this repository's own ledgers, moved under methodology/ in a
# scratch clone the way the migration will move them, then trimmed with the CURRENT
# starter-kit/methodology_trim.py. For each ledger: the dry run names a shard under methodology/archive/,
# the write lands, the proof passes before the commit, after it, and from a SECOND --no-local clone, and
# --reverify agrees. Nothing is written to the real repository (it is only cloned).
# Run from the repo root:   bash docs/planning/methodology-subdirectory-evidence/trim-in-new-layout.sh
set -u
SRC="$(git rev-parse --show-toplevel)" || exit 3
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
TOOL="$SRC/starter-kit/methodology_trim.py"
git clone -q --no-local "$SRC" "$T/m" || exit 3
cd "$T/m" || exit 3
git config core.hooksPath /dev/null; git config user.email t@t; git config user.name t; git config commit.gpgsign false
mkdir methodology && git mv CHANGELOG.md methodology/ && git mv HANDOFFS.md methodology/
cp starter-kit/SESSION_RUNNER.md methodology/SESSION_RUNNER.md     # the framework anchor that makes the tree read as the new layout
git add -A && git commit -q -m "move the ledgers under methodology/"
printf 'tool: %s\nscratch tree: ledgers under methodology/, shards expected under methodology/archive/\n\n' "$(python3 "$TOOL" --version)"
rc=0
for spec in "HANDOFFS.md 1" "CHANGELOG.md 100"; do
  set -- $spec; f="methodology/$1"; keep="$2"
  printf '== %s (keep %s records) ==\n' "$f" "$keep"
  python3 "$TOOL" --file "$f" --cut "$keep" --force --today 2026-10-07 | grep -E '^\s+\[(DRY_RUN|L1_OK|L2_OK|L3_OK|LAYOUT_|TRANSFORM_)' | sed 's/^ *//' | cut -c1-170
  python3 "$TOOL" --file "$f" --cut "$keep" --force --write --today 2026-10-07 > "$T/write.txt" 2>&1
  grep -E '\[(WROTE|P1A_OK|L1_OK|L2_OK|L3_OK)\]' "$T/write.txt" | sed 's/^ *//' | cut -c1-150
  shard="$(git status --short -uall | awk '/^\?\? methodology\/archive\/.*[^h]\.md$/ {print $2}')"
  [ -n "$shard" ] || { echo "FAIL: no shard under methodology/archive/ was written; the tool said:"; sed 's/^/    | /' "$T/write.txt" | cut -c1-200; rc=1; continue; }
  printf 'shard: %s (%s B), rebased links in it: %s, back link: %s\n' "$shard" "$(wc -c < "$shard" | tr -d ' ')" \
    "$(grep -o '](\.\./[^)]*)' "$shard" | wc -l | tr -d ' ')" "$(grep -m1 -o '(\.\./[A-Z]*\.md)' "$shard")"
  printf 'files written outside methodology/: %s\n' "$(git status --short -uall | awk '{print $2}' | grep -vc '^methodology/')"
  bash "$shard.verify.sh" > "$T/pre.txt" 2>&1; pre=$?
  git add -A && git commit -q -m "trim $f"
  bash "$shard.verify.sh" > "$T/post.txt" 2>&1; post=$?
  git clone -q --no-local "$T/m" "$T/c-$1" && ( cd "$T/c-$1" && bash "$shard.verify.sh" > "$T/clone.txt" 2>&1 ); clone=$?
  python3 "$TOOL" --reverify "$shard" > "$T/rev.txt" 2>&1; rev=$?
  printf 'proof exit: before the commit %s, after it %s, from a --no-local clone %s; --reverify %s\n' "$pre" "$post" "$clone" "$rev"
  tail -1 "$T/clone.txt" | cut -c1-150
  [ "$pre$post$clone$rev" = "0000" ] || rc=1
  echo
done
printf 'ledger entries written into methodology/CHANGELOG.md by the two trims: %s\n' "$(grep -c 'Ledger trim: `methodology/' methodology/CHANGELOG.md)"
printf 'a root CHANGELOG.md or HANDOFFS.md appeared: %s\n' "$(ls CHANGELOG.md HANDOFFS.md 2>/dev/null | wc -l | tr -d ' ')"
exit $rc
