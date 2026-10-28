#!/usr/bin/env bash
# PR2b: each remaining candidate commit applied ALONE onto a layer's tip, without checking anything out.
# Usage:  bash pr2b-next-alone.sh <repo> <tip> <from> <to> [<old candidate ref>]      (numbers count from 1 along
#         `git log --reverse upstream/main..<old candidate ref>`; default ref pr2/candidate; <from>..<to> inclusive)
# For each commit C: git merge-tree --write-tree --name-only --merge-base=C^ <tip> C   (exit 0 clean, 1 conflicts).
# Alone, not in order: a conflict measured alone can vanish in order (seen at layers 6 and 7, and for commits 9
# and 10 at layer 7), so the figures are estimates for the next layers, not predictions of the final series.
# Read-only: merge-tree builds objects in the object database and checks nothing out.
set -u
REPO=${1:?repo}; TIP=${2:?tip}; FROM=${3:?first number}; TO=${4:?last number}; OLD=${5:-pr2/candidate}
cd "$REPO" || exit 3
echo "# each remaining candidate commit (numbers $FROM to $TO of $OLD, in its order) applied ALONE onto the tip $(git rev-parse --short=8 "$TIP"),"
echo "# by: git merge-tree --write-tree --name-only --merge-base=<commit>^ $(git rev-parse --short=8 "$TIP") <commit>   (exit 0 clean, 1 conflicts)"
git log --reverse --format='%H %h %s' upstream/main.."$OLD" | sed -n "${FROM},${TO}p" | while read -r full short subject; do
  out=$(git merge-tree --write-tree --name-only --merge-base="${full}^" "$TIP" "$full" 2>&1); rc=$?
  printf '%s exit %s  %s\n' "$short" "$rc" "$(printf '%s' "$subject" | cut -c1-90)"
  if [ "$rc" -ne 0 ]; then
    # after the tree id: the conflicted file names, then a blank line, then the informational messages
    printf '%s\n' "$out" | sed -n '2,/^$/p' | grep -v '^$' | sed 's/^/      conflicted: /'
  fi
done
