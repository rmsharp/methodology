#!/usr/bin/env bash
# Piece 4 of docs/planning/issue100-fixes-plan.md: does the runner sentence still land in the right place,
# and does the runner stay under its own token ceiling, once the piece is MERGED with each open pull request?
#   bash docs/planning/issue100-plan-evidence/piece4-merged-runner-check.sh <piece-ref> "<sentence>"
# For upstream/main and for each open upstream pull request head it prints: the runner's size at that head, its
# size in the tree of (piece merged with that head), the delta, the ceiling from THAT head's .context-budget.json
# (max_tokens x bytes_per_token, rounded -- the arithmetic plan-evidence.py's [budget-*] lines use), the headroom
# after the merge, how many times the sentence occurs, and the three lines above it.
# Read-only: `git merge-tree --write-tree` builds the merge in the object database only; `--attr-source` is the
# EMPTY tree, so `merge=union` does not apply (what GitHub's server-side merge does). A merge that conflicts in the
# runner prints "CONFLICT" for that head and no sizes.
set -u
PIECE=${1:?usage: piece4-merged-runner-check.sh <piece-ref> "<sentence>"}
SENTENCE=${2:?usage: piece4-merged-runner-check.sh <piece-ref> "<sentence>"}
cd "$(git rev-parse --show-toplevel)" || exit 3
EMPTY=4b825dc642cb6eb9a060e54bf8d69288fbee4904
RUNNER=starter-kit/SESSION_RUNNER.md
git rev-parse --verify -q "$PIECE^{commit}" >/dev/null || { echo "no such ref: $PIECE"; exit 3; }

ceiling_at() {   # ceiling_at <ref>: the runner's byte ceiling in that ref's .context-budget.json
  git show "$1:.context-budget.json" | python3 -c "
import json, sys
c = json.load(sys.stdin)
for f in c['files']:
    if f.get('class') == 'read-set' and 'max_tokens' in f and f['path'].endswith('SESSION_RUNNER.md'):
        print(round(f['max_tokens'] * f.get('bytes_per_token', c.get('bytes_per_token'))))"
}

report() {   # report <label> <head-ref>
  local label=$1 head=$2 tree size headsize ceil n
  tree=$(git --attr-source=$EMPTY merge-tree --write-tree "$PIECE" "$head" 2>/dev/null | head -1)
  if ! git cat-file -e "$tree:$RUNNER" 2>/dev/null || git show "$tree:$RUNNER" | grep -q '^<<<<<<<'; then
    echo "$label: CONFLICT in the runner"; return
  fi
  size=$(git cat-file -s "$tree:$RUNNER"); headsize=$(git cat-file -s "$head:$RUNNER"); ceil=$(ceiling_at "$head")
  n=$(git show "$tree:$RUNNER" | grep -cF -- "$SENTENCE")
  echo "$label: runner at head ${headsize} B; merged with piece ${size} B (delta $((size - headsize))); ceiling at that head ${ceil}; headroom before $((ceil - headsize)), after $((ceil - size)); sentence occurs ${n}x"
  git show "$tree:$RUNNER" | grep -n -B3 -F -- "$SENTENCE" | cut -c1-110 | sed 's/^/     /'
}

echo "piece $PIECE $(git rev-parse --short "$PIECE"); upstream/main $(git rev-parse --short upstream/main)"
report "upstream/main" upstream/main
for n in 99 98 96; do
  sha=$(gh pr view "$n" --repo KJ5HST/methodology --json headRefOid --jq .headRefOid)
  git cat-file -e "$sha^{commit}" 2>/dev/null || git fetch -q upstream "pull/$n/head"
  report "#$n head ${sha:0:8}" "$sha"
done
