#!/usr/bin/env bash
# What the candidate (`pr2/candidate`) and the fork's tip conflict with in `upstream/main` now that #92 and #94 have merged,
# and in the heads of the two upstream pull requests still open (#98, #96). The successor of `conflicts.sh`, which names the
# two that merged. Run from anywhere inside the repository:  bash docs/planning/pr-composition-evidence/conflicts-after-merge.sh
# Reads git and `gh`; writes nothing but its own output. `git merge-tree --write-tree` builds the merge in the object database
# only. `--attr-source` is the EMPTY tree, so `merge=union` does not apply: that is what GitHub's server-side merge does
# (the scratch PR #90 measured it), and it is why a ledger file reads as conflicting here.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 3
EMPTY=4b825dc642cb6eb9a060e54bf8d69288fbee4904
OLDBASE=f34769f3   # upstream/main when the plan was measured
CAND=pr2/candidate
git fetch -q upstream || { echo "git fetch upstream failed"; exit 3; }
UP=$(git rev-parse upstream/main)
echo "upstream/main ${UP:0:8}: $(git rev-list --count "$OLDBASE..upstream/main") commits past $OLDBASE; fork main $(git rev-parse --short HEAD) is $(git rev-list --count upstream/main..HEAD) past upstream/main and $(git rev-list --count HEAD..upstream/main) behind it"
echo "$CAND $(git rev-parse --short "$CAND"): $(git rev-list --count "$OLDBASE..$CAND") commits past $OLDBASE; merge-base with upstream/main $(git merge-base "$CAND" upstream/main | cut -c1-8)"
for n in 92 94 96 98; do
  echo "PR #$n: $(gh pr view "$n" --repo KJ5HST/methodology --json state,mergedAt,mergeable,headRefOid --jq '"\(.state) merged=\(.mergedAt // "-") mergeable=\(.mergeable) head=\(.headRefOid[0:8])"')"
done
for n in 96 98; do
  sha=$(gh pr view "$n" --repo KJ5HST/methodology --json headRefOid --jq .headRefOid)
  git cat-file -e "$sha^{commit}" 2>/dev/null || git fetch -q upstream "pull/$n/head"
  eval "HEAD_$n=$sha"
done
measure() {   # measure <label> <ours-ref> <theirs-ref>
  local out rc tree
  out=$(git --attr-source=$EMPTY merge-tree --write-tree --name-only "$2" "$3" 2>&1); rc=$?
  tree=$(printf '%s\n' "$out" | head -1)
  echo "== $1: merge-tree exit $rc (0 clean, 1 conflicts)"
  if [ "$rc" -eq 1 ]; then
    local total=0 n f
    for f in $(printf '%s\n' "$out" | sed -n '2,/^$/p' | grep -v '^$'); do
      n=$(git show "$tree:$f" | grep -c '^<<<<<<<'); total=$((total + n))
      echo "   $f: $n conflict region(s)"
    done
    echo "   total: $total region(s)"
  fi
}
for side in "$CAND" HEAD; do
  measure "$side against upstream/main" "$side" upstream/main
  measure "$side against #98's head (upstream/main plus #98)" "$side" "$HEAD_98"
  measure "$side against #96's head" "$side" "$HEAD_96"
done
echo "== files each open pull request changes, against its own base, that the candidate also changes (candidate vs $OLDBASE)"
git diff --name-only "$OLDBASE" "$CAND" | sort > /tmp/cand-files.$$
for n in 96 98; do
  eval "sha=\$HEAD_$n"
  base=$(git merge-base upstream/main "$sha")
  echo "   #$n ($(git diff --name-only "$base" "$sha" | wc -l | tr -d ' ') files): $(git diff --name-only "$base" "$sha" | sort | comm -12 - /tmp/cand-files.$$ | tr '\n' ' ')"
done
rm -f /tmp/cand-files.$$
echo "== TRIM_VERSION on each side (upstream/main carries the maintainer's review fixes as 1.8.2)"
for r in upstream/main "$CAND"; do printf '   %-14s %s\n' "$r" "$(git show "$r:starter-kit/methodology_trim.py" | grep -m1 -E '^TRIM_VERSION' | cut -c1-40)"; done
