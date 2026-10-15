#!/usr/bin/env bash
# The checkers' layer on a REAL corpus, not a fixture: this fork's own action ledger, receipt ledger and their archived
# shards (hundreds of KB, written over months by a hundred sessions), placed three ways in scratch git repositories
#
#   legacy     CHANGELOG.md and HANDOFFS.md at the root, the shards in docs/archive/
#   new        the same files under methodology/ (with its runner), the shards in methodology/archive/
#   new-docs   the same under methodology/, the shards still in docs/archive/ (the archive moves last)
#
# and read by the OLD tools (the candidate before the layer, `0aa1897`) and the NEW tools (the layer's last commit).
# A tool that reads the layout correctly must say the SAME THING about the same bytes wherever they sit, and the new tool
# must say what the old one said about the legacy tree. What this shows: equality of output and exit code across layouts,
# on bytes no fixture invented. What it does not show: that the output is RIGHT (an old tool's findings on these files are
# whatever they are; this compares, it does not judge), or anything about a tree the fork does not have.
#
#   bash layer6b-realtree.sh <fork-repo> <fork-rev> <candidate-repo> <old-rev> <new-rev> <scratch-dir>
set -u
FORK=${1:?fork repository}; FREV=${2:?fork rev}; CAND=${3:?candidate repository}; OLD=${4:?old rev}; NEW=${5:?new rev}; OUT=${6:?scratch dir}
rm -rf "$OUT/rt"; mkdir -p "$OUT/rt/tools-old" "$OUT/rt/tools-new"
for t in check-ledger check-handoff; do
    git -C "$CAND" show "$OLD:bin/$t" > "$OUT/rt/tools-old/$t"; git -C "$CAND" show "$NEW:bin/$t" > "$OUT/rt/tools-new/$t"
done
SHARDS_C=$(git -C "$FORK" ls-tree --name-only "$FREV" docs/archive/ | grep -E 'archive/CHANGELOG-.*\.md$')
SHARDS_H=$(git -C "$FORK" ls-tree --name-only "$FREV" docs/archive/ | grep -E 'archive/HANDOFFS-.*\.md$')
echo "corpus: fork $(git -C "$FORK" rev-parse --short "$FREV"): CHANGELOG.md $(git -C "$FORK" show "$FREV:CHANGELOG.md" | wc -c | tr -d ' ') B + $(echo "$SHARDS_C" | wc -l | tr -d ' ') shards; HANDOFFS.md $(git -C "$FORK" show "$FREV:HANDOFFS.md" | wc -c | tr -d ' ') B + $(echo "$SHARDS_H" | wc -l | tr -d ' ') shards"

tree() {   # name  ledger-dir  shard-dir
    local d="$OUT/rt/$1"
    mkdir -p "$d"; git init -q "$d"
    mkdir -p "$d/$2" "$d/$3"
    git -C "$FORK" show "$FREV:CHANGELOG.md" > "$d/$2/CHANGELOG.md"; git -C "$FORK" show "$FREV:HANDOFFS.md" > "$d/$2/HANDOFFS.md"
    for s in $SHARDS_C $SHARDS_H; do git -C "$FORK" show "$FREV:$s" > "$d/$3/$(basename "$s")"; done
    if [ "$2" != . ]; then echo runner > "$d/$2/SESSION_RUNNER.md"; fi
}
tree legacy . docs/archive
tree new methodology methodology/archive
tree new-docs methodology docs/archive

run() {   # label  tools-dir  tree  tool  args...
    local label=$1 tools=$2 tree=$3 tool=$4; shift 4
    ( cd "$OUT/rt/$tree" && python3 -B "$OUT/rt/$tools/$tool" "$@" > "$OUT/rt/$label.out" 2>&1; echo $? > "$OUT/rt/$label.rc" )
    sed -i.bak -e "s#$OUT/rt/$tree#<ROOT>#g" "$OUT/rt/$label.out"; rm -f "$OUT/rt/$label.out.bak"
    printf '%-44s exit %s  %s B  %s\n' "$label" "$(cat "$OUT/rt/$label.rc")" "$(wc -c < "$OUT/rt/$label.out" | tr -d ' ')" "$(head -c 110 "$OUT/rt/$label.out" | head -1)"
}
for tool_args in "check-ledger --all" "check-ledger" "check-handoff --all" "check-handoff"; do
    set -- $tool_args; tool=$1; shift; tag=$(echo "$tool_args" | tr ' ' '_' | tr -d '-')
    run "old-$tag-legacy" tools-old legacy "$tool" "$@"
    run "new-$tag-legacy" tools-new legacy "$tool" "$@"
    run "new-$tag-new" tools-new new "$tool" "$@"
    run "new-$tag-new-docs" tools-new new-docs "$tool" "$@"
    for l in new-$tag-new new-$tag-new-docs; do
        # a path the tool prints names where the ledger sits: only that part is allowed to differ
        sed -e 's#<ROOT>/methodology/#<ROOT>/#g' -e 's#<ROOT>/archive/#<ROOT>/docs/archive/#g' "$OUT/rt/$l.out" > "$OUT/rt/$l.norm"
    done
    cmp -s "$OUT/rt/old-$tag-legacy.out" "$OUT/rt/new-$tag-legacy.out" && echo "   old == new on the legacy tree (output)" || echo "   OLD DIFFERS FROM NEW on the legacy tree (output)"
    [ "$(cat "$OUT/rt/old-$tag-legacy.rc")" = "$(cat "$OUT/rt/new-$tag-legacy.rc")" ] && echo "   old == new on the legacy tree (exit)" || echo "   OLD DIFFERS FROM NEW on the legacy tree (exit)"
    for l in new new-docs; do
        cmp -s "$OUT/rt/new-$tag-legacy.out" "$OUT/rt/new-$tag-$l.norm" && echo "   legacy == $l (output, paths normalised)" || { echo "   LEGACY DIFFERS FROM $l (output):"; diff "$OUT/rt/new-$tag-legacy.out" "$OUT/rt/new-$tag-$l.norm" | head -6; }
        [ "$(cat "$OUT/rt/new-$tag-legacy.rc")" = "$(cat "$OUT/rt/new-$tag-$l.rc")" ] && echo "   legacy == $l (exit)" || echo "   LEGACY DIFFERS FROM $l (exit)"
    done
done
echo "layer6b-realtree done"
