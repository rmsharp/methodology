#!/usr/bin/env bash
# BL-119: the figures decision 3 of the one-PR text rests on, on the old tips and the new ones, in one place.
# For each pair (candidate tip, #94 head): `git merge-tree --write-tree --name-only` (exit 0 clean, 1 conflicts) with the
# conflict regions per file, for the candidate and for its first commit `bbe0dc3` alone; then pr4-supersede.sh (the lines
# #94 adds to the trimmer, its tests and the gate file, and how many are absent here as exact lines). Reads git objects
# only; writes nothing. The first row reproduces draft 10's published figures, which is the check on the method.
#   bash docs/planning/pr-composition-evidence/bl119-decision3.sh
set -u
R=$(git rev-parse --show-toplevel) || exit 3
cd "$R" || exit 3
one() { # label ours theirs
  out=$(git merge-tree --write-tree --name-only "$2" "$3" 2>&1); rc=$?
  tree=$(printf '%s\n' "$out" | head -1); tot=0; files=0; list=""
  if [ "$rc" -eq 1 ]; then
    for f in $(printf '%s\n' "$out" | sed -n '2,/^$/p' | grep -v '^$'); do
      n=$(git show "$tree:$f" | grep -c '^<<<<<<<'); tot=$((tot+n)); files=$((files+1)); list="$list $f=$n"
    done
  fi
  echo "$1: exit $rc; $files file(s), $tot region(s):$list"
}
for pair in "cfcc713 2308553" "cfcc713 1082d3b" "3cba1e5 1082d3b"; do
  set -- $pair
  echo "######## candidate $1 against #94 at $2"
  one "  the candidate" "$1" "$2"
  one "  bbe0dc3 alone" bbe0dc3 "$2"
  bash docs/planning/pr-composition-evidence/pr4-supersede.sh "$R" "$1" f34769f "$2" | grep -E 'adds' | sed 's/^/  /'
done
echo "######## candidate 3cba1e5 against #92 at fa2bb5d"
one "  the candidate" 3cba1e5 fa2bb5d
