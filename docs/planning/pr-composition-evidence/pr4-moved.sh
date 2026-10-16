#!/usr/bin/env bash
# PR4: what does each tool's plain `bin/sync` do to a project that has ALREADY moved its files under methodology/?
# One throwaway project is built by this branch's own sync (--layout new) and committed; it is copied twice; upstream's
# sync runs on one copy and this branch's on the other; what each wrote is counted, inside and outside methodology/.
# Reads exports of the two tips; writes only under <work-dir>. Exit codes are printed bare.
#   bash docs/planning/pr-composition-evidence/pr4-moved.sh <repo> <upstream> <candidate> <work-dir>
set -u
SRC=${1:?repository holding both commits}; UP=${2:?upstream commit}; CAND=${3:?candidate commit}; W=${4:?work dir}
rm -rf "$W"; mkdir -p "$W/up" "$W/cand"
git -C "$SRC" archive "$UP" | tar -x -C "$W/up" || exit 3
git -C "$SRC" archive "$CAND" | tar -x -C "$W/cand" || exit 3
mk() { git init -q "$1"; git -C "$1" config user.email fixture@example.invalid; git -C "$1" config user.name fixture; git -C "$1" commit -q --allow-empty -m init; }
mk "$W/base"
python3 -I "$W/cand/bin/sync" --layout new "$W/base" > "$W/base-sync.txt" 2>&1; echo "a project moved by this branch's sync (--layout new): exit $?"
git -C "$W/base" add -A && git -C "$W/base" commit -q -m "framework files in methodology/"
echo "  tracked files under methodology/: $(git -C "$W/base" ls-files methodology | wc -l | tr -d ' '); tracked outside methodology/: $(git -C "$W/base" ls-files | grep -vc '^methodology/')"
for t in up cand; do
  label=$([ "$t" = up ] && echo "upstream's" || echo "this branch's")
  cp -R "$W/base" "$W/$t-project"
  python3 -I "$W/$t/bin/sync" "$W/$t-project" > "$W/$t-sync.txt" 2>&1; rc=$?
  git -C "$W/$t-project" status --porcelain --untracked-files=all | awk '{print $2}' > "$W/$t-paths.txt"
  total=$(grep -c . "$W/$t-paths.txt"); inside=$(grep -c '^methodology/' "$W/$t-paths.txt")
  echo "== $label plain bin/sync on that project: exit $rc"
  echo "  paths written: $total  (inside methodology/: $inside, outside: $((total - inside)))"
  grep . "$W/$t-paths.txt" | grep -v '^methodology/' | head -5 | sed 's/^/    e.g. /'
done
echo; echo "pr4-moved done"
