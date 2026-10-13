#!/usr/bin/env bash
# What the fork's tip conflicts with in the two open upstream pull requests (S308).
# Run from anywhere inside the repository:  bash docs/planning/pr-composition-evidence/conflicts.sh
# Reads git and `gh`; writes nothing but its own output. `git merge-tree --write-tree` builds the merge in the object
# database only: no index, no working tree, no ref moves.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 3
for n in 94 92; do
  sha=$(gh pr view "$n" --repo KJ5HST/methodology --json headRefOid --jq .headRefOid)
  state=$(gh pr view "$n" --repo KJ5HST/methodology --json state,mergeable --jq '.state + " " + .mergeable')
  git cat-file -e "$sha^{commit}" 2>/dev/null || git fetch -q upstream "pull/$n/head"
  echo "== PR #$n head ${sha:0:12} ($state), files: $(gh pr view "$n" --repo KJ5HST/methodology --json files --jq '[.files[].path] | join(", ")')"
  out=$(git merge-tree --write-tree --name-only HEAD "$sha" 2>&1); rc=$?
  tree=$(printf '%s\n' "$out" | head -1)
  echo "   merge-tree exit $rc (0 clean, 1 conflicts)"
  printf '%s\n' "$out" | sed -n '2,/^$/p' | grep -v '^$' | sed 's/^/   conflicted: /'
  if [ "$rc" -eq 1 ]; then
    for f in $(printf '%s\n' "$out" | sed -n '2,/^$/p' | grep -v '^$'); do
      echo "   $f: $(git show "$tree:$f" | grep -c '^<<<<<<<') conflict region(s)"
    done
  fi
  # Is the fork's own copy of the PR's work a superset? The fork carries issue #93's trimmer work as its own commits.
  echo "   PR files whose HEAD blob equals the PR head's blob:"
  for f in $(gh pr view "$n" --repo KJ5HST/methodology --json files --jq '.files[].path'); do
    a=$(git rev-parse -q --verify "HEAD:$f" 2>/dev/null); b=$(git rev-parse -q --verify "$sha:$f" 2>/dev/null)
    [ "$a" = "$b" ] && echo "      same     $f" || echo "      differs  $f"
  done
done
