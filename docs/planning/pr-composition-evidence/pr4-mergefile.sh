#!/usr/bin/env bash
# PR4: why the pull request sends whole files. For every file the methodology/ work changed between the copy it
# started from and the fork's tip, that upstream also has: a three-way merge of upstream's copy, the starting copy
# and the tip's copy. `git merge-file`'s exit status is the number of conflict regions (0 = merges clean).
# Reads git objects into a scratch directory; writes nothing in the repository.
#   bash docs/planning/pr-composition-evidence/pr4-mergefile.sh <repo> <start> <upstream> <tip> <scratch-dir>
set -u
SRC=${1:?repository}; BASE=${2:?the copy the work started from}; UP=${3:?upstream commit}; TIP=${4:?tip}; T=${5:?scratch dir}
cd "$SRC" || exit 3
rm -rf "$T"; mkdir -p "$T"
tot=0; nf=0; ok=0; dash=0
for f in $(git diff --name-only "$BASE" "$TIP" -- . ':!docs' ':!CLAUDE.md' ':!README.md' ':!CHANGELOG.md' ':!HANDOFFS.md' \
           ':!dashboard_history.jsonl' ':!dashboard.html' ':!.context-budget.json'); do
  git cat-file -e "$UP:$f" 2>/dev/null || continue          # a file upstream lacks cannot conflict
  git show "$BASE:$f" > "$T/base" 2>/dev/null || continue
  git show "$UP:$f" > "$T/ours"; git show "$TIP:$f" > "$T/theirs"
  git merge-file -p "$T/ours" "$T/base" "$T/theirs" > /dev/null; rc=$?
  if [ "$rc" -gt 0 ]; then
    tot=$((tot+rc)); nf=$((nf+1)); echo "$rc  $f"
    case "$f" in */methodology_dashboard.py) dash=$((dash+rc));; esac
  else ok=$((ok+1)); fi
done
echo "conflict regions: $tot in $nf files (the dashboard's two copies: $dash); files that merge clean: $ok"
