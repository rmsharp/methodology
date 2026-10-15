#!/bin/bash
# Rebuild the whole scrub range from the candidate's tip in a fresh scratch clone (S324).
#   scrub-run.sh CLONE_DIR [GROUPS...]        default: C6 C7 C5 C4 C3 C2 C1 (phase A, comments and docstrings) then B1 B2 B3 (phase B, printed text)
# The clone starts at 5afc962, the candidate's tip before the scrub; each group is one commit, in the order given. A group
# named C* is built by scrub-build.py and one named B* by scrub-build-b.py, from scrub-edits.txt and scrub-edits-b.txt.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(git -C "$HERE" rev-parse --show-toplevel)"
CLONE="$1"; shift
if [ "$#" -eq 0 ]; then set -- C6 C7 C5 C4 C3 C2 C1 B1 B2 B3; fi
# the base is the commit the scrub starts from, pinned under refs/pr2/candidate-before-scrub so that it stays reachable and
# the range can be rebuilt after the local ref pr2/candidate has moved on to the scrub's tip
[ "$(git -C "$ROOT" rev-parse --short refs/pr2/candidate-before-scrub)" = 5afc962 ] || { echo "refs/pr2/candidate-before-scrub is not 5afc962" >&2; exit 2; }
rm -rf "$CLONE"
git clone -q --no-local "$ROOT" "$CLONE"
git -C "$CLONE" fetch -q "$ROOT" refs/pr2/candidate-before-scrub
git -C "$CLONE" checkout -q --detach 5afc962
for g in "$@"; do
    case "$g" in
        C*) python3 -I "$HERE/scrub-build.py" "$CLONE" "$g" --write | tail -1 ;;
        B*) python3 -I "$HERE/scrub-build-b.py" "$CLONE" "$g" --write | tail -1 ;;
        *) echo "unknown group $g" >&2; exit 2 ;;
    esac
done
git -C "$CLONE" log --oneline 5afc962..HEAD
echo "tree $(git -C "$CLONE" rev-parse 'HEAD^{tree}')"
