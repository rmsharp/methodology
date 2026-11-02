#!/usr/bin/env bash
# Merge trials for one piece of docs/planning/issue100-fixes-plan.md (section 2, "Proof each piece owes").
#   bash docs/planning/issue100-plan-evidence/piece-merge-trials.sh <piece-ref>
# For each open upstream pull request head, it counts the conflict regions of
#   (a) upstream/main merged with the head          -- the head's own conflicts, the baseline
#   (b) the piece's commit merged with the head      -- the baseline plus whatever the piece adds
# and prints the files in conflict and the regions per file. The piece "adds no conflict region that
# head did not already have" when (b) lists no file and no region that (a) does not.
# Read-only: `git merge-tree --write-tree` builds the merge in the object database only, and
# `--attr-source` is the EMPTY tree so `merge=union` does not apply, which is what GitHub's
# server-side merge does (see pr-composition-evidence/conflicts-after-merge.sh).
# The heads are read from `gh pr view`; a head that moved prints a different hash on its line.
set -u
PIECE=${1:?usage: piece-merge-trials.sh <piece-ref>}
cd "$(git rev-parse --show-toplevel)" || exit 3
EMPTY=4b825dc642cb6eb9a060e54bf8d69288fbee4904
git rev-parse --verify -q "$PIECE^{commit}" >/dev/null || { echo "no such ref: $PIECE"; exit 3; }
echo "piece $PIECE $(git rev-parse --short "$PIECE"); merge-base with upstream/main $(git merge-base "$PIECE" upstream/main | cut -c1-8); upstream/main $(git rev-parse --short upstream/main)"
echo "commits past upstream/main: $(git rev-list --count upstream/main.."$PIECE"); files: $(git diff --name-only upstream/main "$PIECE" | tr '\n' ' ')"
measure() {   # measure <ours> <theirs>: prints "<exit> <total regions> <file:regions ...>"
  local out rc tree total=0 n f detail=""
  out=$(git --attr-source=$EMPTY merge-tree --write-tree --name-only "$1" "$2" 2>&1); rc=$?
  tree=$(printf '%s\n' "$out" | head -1)
  if [ "$rc" -eq 1 ]; then
    for f in $(printf '%s\n' "$out" | sed -n '2,/^$/p' | grep -v '^$'); do
      n=$(git show "$tree:$f" | grep -c '^<<<<<<<'); total=$((total + n)); detail="$detail $f:$n"
    done
  fi
  echo "exit=$rc regions=$total${detail:+ [$detail ]}"
}
for n in 99 98 96; do
  sha=$(gh pr view "$n" --repo KJ5HST/methodology --json headRefOid --jq .headRefOid)
  git cat-file -e "$sha^{commit}" 2>/dev/null || git fetch -q upstream "pull/$n/head"
  echo "#$n head ${sha:0:8}"
  echo "   (a) upstream/main + head : $(measure upstream/main "$sha")"
  echo "   (b) piece        + head : $(measure "$PIECE" "$sha")"
done
