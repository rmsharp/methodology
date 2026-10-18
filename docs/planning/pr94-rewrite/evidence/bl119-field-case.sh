#!/usr/bin/env bash
# BL-119 field case: a depth-1 clone of <repo>'s tip, so the trim commit's parent is absent from it,
# then one archived piece's frozen proof and `--reverify` under the old trimmer and under the new one.
# It is the procedure S338 ran by hand on fork `main` (bl119-main-field-case-1.8.0-vs-1.8.1.txt), made a
# script so the same lines can be produced for the pull request candidate.
#
#   bash bl119-field-case.sh <label> <repo> <shard> <old-trimmer> <new-trimmer> <scratch-dir>
#
# <repo> is a local repository whose tip holds the piece and its proof; <old-trimmer> and <new-trimmer>
# are paths to the two versions of methodology_trim.py. Reads git only; writes only <scratch-dir>.
set -u
LABEL=${1:?label}; REPO=${2:?repository}; SHARD=${3:?archived piece}; OLD=${4:?old trimmer}
NEW=${5:?new trimmer}; W=${6:?scratch dir}
rm -rf "$W"
git clone --depth 1 -q "file://$REPO" "$W" || exit 3
cd "$W" || exit 3
ver() { grep -m1 '^TRIM_VERSION' "$1" | sed -E 's/^TRIM_VERSION = "([^"]+)".*/\1/'; }

echo "BL-119, $LABEL: the field case on a depth-1 clone."
echo "Clone: git clone --depth 1 file://<repo> at $(git rev-parse --short HEAD)" \
     "($(git rev-list --count HEAD) commit; the trim commit's parent is absent)."
echo "Shard: $SHARD (its proof is frozen)."
echo

out=$(bash "$SHARD.verify.sh" 2>&1); rc=$?
echo "== 1. the frozen proof: bash $SHARD.verify.sh  -> exit $rc"
echo "$out"; echo

cp "$OLD" starter-kit/methodology_trim.py
out=$(python3 -I starter-kit/methodology_trim.py --reverify "$SHARD" 2>&1); rc=$?
echo "== 2. --reverify under $(ver "$OLD") (the old trimmer, copied into the clone)  -> exit $rc"
echo "$out"; echo

cp "$NEW" starter-kit/methodology_trim.py
out=$(python3 -I starter-kit/methodology_trim.py --reverify "$SHARD" 2>&1); rc=$?
echo "== 3. --reverify under $(ver "$NEW") (the new trimmer, copied into the same clone)  -> exit $rc"
echo "$out"
