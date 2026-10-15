#!/usr/bin/env bash
# The scrub: do the two open pull requests conflict with the candidate any differently before and after its ten commits?
#   bash d6-conflicts.sh <repo> <before> <after> <pr-head> [<pr-head> ...]      (read-only: git merge-tree builds no working tree)
set -u
REPO=${1:?repo}; BEFORE=${2:?commit before}; AFTER=${3:?commit after}; shift 3
cd "$REPO" || exit 3
for pr in "$@"; do
    echo "== $pr ($(git rev-parse --short "$pr"))"
    for c in "$BEFORE" "$AFTER"; do
        out=$(git merge-tree --write-tree --name-only "$c" "$pr" 2>&1); rc=$?
        printf '  %s: exit %s; conflicted paths: ' "$(git rev-parse --short "$c")" "$rc"
        printf '%s\n' "$out" | sed -n '2,/^$/p' | grep -v '^$' | tr '\n' ' '; echo
    done
done
