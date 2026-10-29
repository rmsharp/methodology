#!/usr/bin/env bash
# PR2b layer 23: the grouping plan's DONE criterion "the tree equals 866ea59c8738 plus 26's edits", checked by rebuilding the tree.
# The plan's tree came from a throwaway branch in S393 and was never kept, so this rebuilds it: the eleven clean commits of the
# old candidate (series 21-25, 27, 28, 29, 30, 32, 33; NOT 26) onto layer 21's tip d818ca17 in a scratch --no-local clone, then
# compares (a) its tree id with the plan's prefix and (b) the diff from that tree to the layer tip with 26' (d9f583c3) by patch-id.
# Usage: bash pr2b-layer23-treecheck.sh <fork repository> <scratch dir for the clone>     (read-only for the repository)
set -u
REPO=${1:?fork repository}; DIR=${2:?scratch dir (created fresh)}
rm -rf "$DIR"
git clone --no-local -q "$REPO" "$DIR" || exit 3
cd "$DIR" || exit 3
git config --unset core.hooksPath 2>/dev/null
git checkout -q -b t d818ca17 || exit 3
for c in c933b0f9 d31c25da c1cdc2ec 71e00e89 ea751caa 72e0c991 a62bfecf cfcc713b 8ace51e8 ccd5620e 28f99a70; do
  git cherry-pick -x "$c" >/dev/null 2>&1 || { echo "pick $c FAILED"; exit 4; }
done
echo "eleven picks (21-25, 27, 32, 33, 28, 29, 30; no 26): $(git rev-list --count d818ca17..HEAD) commits on d818ca17"
echo "tree of the eleven: $(git rev-parse 'HEAD^{tree}')"
echo "plan's tree prefix 866ea59c8738 matches: $(git rev-parse 'HEAD^{tree}' | grep -c '^866ea59c8738')   (1 = yes)"
git fetch -q "$REPO" pr2b/candidate:refs/heads/tip || exit 3
echo "layer tip (pr2b/candidate): $(git rev-parse tip)"
echo "diff, eleven-pick tree to layer tip:$(git diff --shortstat t tip)"
echo "  files: $(git diff --name-only t tip | tr '\n' ' ')"
echo "patch-id of that diff: $(git diff t tip | git patch-id --stable | cut -c1-12)"
echo "patch-id of 26' d9f583c3: $(git show d9f583c3 | git patch-id --stable | cut -c1-12)"
