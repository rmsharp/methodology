#!/usr/bin/env bash
# PR2 Part 2, the prose layer: the measurements the record cites that the other scripts do not print, in one saved run.
#   layer6c-measure.sh <fork-repo> <layer-commit> <parent-commit> <source-rev> <scratch-dir>
# <fork-repo> holds the candidate's commits as local objects (this repository after a forced fetch of `pr2/candidate`) and the
# fork's tip <source-rev> the builder reads. <parent-commit> is the checkers' layer's `505541c`; <layer-commit> is the layer's
# LAST commit (the layer is five: four of documents, then the check that holds both layouts). Everything runs in scratch clones
# under <scratch-dir>; nothing in <fork-repo> is written. Serial. The mutants and the migration-suite probe have their own
# scripts and outputs: layer6c-mutate.py, layer6c-probe.sh.
# Sections: 1 the simulated adopter tree after each commit; 2 the builder reproduces the layer's tree and refuses on drift;
# 3 the new check on the parent and on the layer; 4 real projects synced in both layouts, and the prose's own example commands;
# 5 the commands and flags the added prose names, and where each exists; 6 the two open pull requests; 7 the scrub input;
# 8 the changed files and the candidate's size against upstream.
set -u
FORK=${1:?fork repository}; LAYER=${2:?layer commit}; PARENT=${3:?parent commit}; SRCREV=${4:?source revision}; W=${5:?scratch dir}/layer6c-measure
HERE=$(cd "$(dirname "$0")" && pwd)
rm -rf "$W"; mkdir -p "$W"
clone() { git clone --no-local -q "$FORK" "$1" && git -C "$1" checkout -q "$2" && git -C "$1" config user.name measure && git -C "$1" config user.email m@m && git -C "$1" config --unset core.hooksPath 2>/dev/null; return 0; }
first_line() { "$@" 2>&1 | head -1 | sed -E 's/ in the simulated adopter tree.*//; s/^check-links: //' | cut -c1-110; }

echo "## Section 1: the simulated adopter tree after each commit (bin/check-links, each layout; the parent first)"
clone "$W/walk" "$PARENT"
for c in $PARENT $(git -C "$W/walk" rev-list --reverse "$PARENT..$LAYER"); do
  git -C "$W/walk" checkout -q "$c"
  printf '%s %-72s files %2s\n' "$(git -C "$W/walk" rev-parse --short "$c")" "$(git -C "$W/walk" log -1 --format=%s | cut -c1-72)" \
    "$([ "$c" = "$PARENT" ] && echo - || git -C "$W/walk" diff --name-only "$c~1" "$c" | wc -l | tr -d ' ')"
  for lay in legacy new; do
    printf '    %-7s %s\n' "$lay" "$(cd "$W/walk" && first_line python3 bin/check-links --layout $lay)"
  done
done

echo; echo "## Section 2: the builder reproduces the layer's tree, and refuses on drift"
clone "$W/new" "$LAYER"; clone "$W/repro" "$PARENT"
PASSED=$(git -C "$FORK" show "$LAYER:.quality-gates.json" | python3 -c 'import json,sys; print([g for g in json.load(sys.stdin)["gates"] if g["name"]=="tests-sh-passed"][0]["threshold"])')
( cd "$W/repro" && for st in docs1 docs2 docs3 docs4; do
      python3 "$HERE/layer6c-build.py" "$FORK" "$SRCREV" . --stage $st | tail -1 | cut -c1-70 && git add -A && git -c commit.gpgsign=false commit -q -m $st || exit 1
  done \
  && python3 "$HERE/layer6c-build.py" "$FORK" "$SRCREV" . --stage tests | tail -1 \
  && python3 "$HERE/layer6c-build.py" "$FORK" "$SRCREV" . --stage tests --passed "$PASSED" | tail -1 \
  && git add -A && echo "built tree   $(git write-tree | cut -c1-12)" )
echo "layer's tree $(git -C "$W/new" rev-parse "HEAD^{tree}" | cut -c1-12)"
clone "$W/drift" "$PARENT"
printf '\nOne line of drift.\n' >> "$W/drift/starter-kit/SESSION_RUNNER.md"
git -C "$W/drift" commit -q -am "drift in the candidate's SESSION_RUNNER.md"
( cd "$W/drift" && python3 "$HERE/layer6c-build.py" "$FORK" "$SRCREV" . --stage docs1 2>&1 | tail -1 | cut -c1-240 )
echo "dirty paths after the refusal: $(git -C "$W/drift" status --short | wc -l | tr -d ' ')"

echo; echo "## Section 3: the new check (bin/check-links --layout both, what Test 10's second block runs) on the parent and on the layer"
( cd "$W/walk" && git checkout -q "$PARENT" && python3 bin/check-links --layout both >/dev/null 2>&1; echo "parent $PARENT: exit $?"; python3 bin/check-links --layout both 2>&1 | grep -E '^check-links:' | cut -c1-150 )
( cd "$W/new" && python3 bin/check-links --layout both >/dev/null 2>&1; echo "layer  $LAYER: exit $?"; python3 bin/check-links --layout both 2>&1 | grep -E '^check-links:' | cut -c1-150 )

echo; echo "## Section 4: real projects synced by the layer's own bin/sync in each layout, the links read in the project itself, and the prose's example commands run in it"
for lay in new legacy; do
  P="$W/proj-$lay"; mkdir "$P"; git -C "$P" init -q
  ( cd "$W/new" && python3 bin/sync "$P" --mode=commit --layout $lay >/dev/null 2>&1; echo "sync --layout $lay: exit $?" )
  ( cd "$W/new" && python3 bin/check-links --tree "$P" 2>&1 | head -1 | sed -E 's# at /.*##' | cut -c1-140 )
done
( cd "$W/proj-new" && python3 methodology/methodology_trim.py --file methodology/CHANGELOG.md --check >/dev/null 2>&1; echo "the runner's example in the migrated project (python3 methodology/methodology_trim.py --file methodology/CHANGELOG.md --check): exit $?" )
( cd "$W/proj-legacy" && python3 methodology_trim.py --file CHANGELOG.md --check >/dev/null 2>&1; echo "the same command in the legacy project, without the prefix: exit $?" )
( cd "$W/proj-new" && python3 methodology/methodology_trim.py --file CHANGELOG.md --check >/dev/null 2>&1; echo "the legacy form in the migrated project (no methodology/ in front of the file): exit $?" )
( cd "$W/proj-new" && find . -type f -not -path './.git/*' | sort > "$W/before.txt"; python3 methodology/methodology_dashboard.py >/dev/null 2>&1; rc=$?
  find . -type f -not -path './.git/*' | sort > "$W/after.txt"
  echo "BOOTSTRAP's example in the migrated project (python3 methodology/methodology_dashboard.py): exit $rc; files it wrote: $(comm -13 "$W/before.txt" "$W/after.txt" | tr '\n' ' ')" )

echo; echo "## Section 5: the flags and tools the layer's added prose names, and where each exists (the candidate at the layer; the tip's migrate-layout, which the NEXT layer carries)"
git -C "$W/new" diff "$PARENT" "$LAYER" -- '*.md' | grep -E '^\+' | grep -vE '^\+\+\+' > "$W/added.txt"
TOOLS="bin/sync bin/status bin/check-ledger bin/check-handoff bin/check-links starter-kit/methodology_trim.py starter-kit/context_budget.py starter-kit/quality_ratchet.py starter-kit/methodology_dashboard.py"
for tok in $(grep -oE '(^|[^[:alnum:]-])--[a-z][a-z-]+' "$W/added.txt" | grep -oE '\-\-[a-z][a-z-]+' | sort -u); do
  where=""
  for t in $TOOLS; do grep -q -- "$tok" "$W/new/$t" 2>/dev/null && where="$where $t"; done
  git -C "$FORK" show "$SRCREV:bin/migrate-layout" | grep -q -- "$tok" && where="$where [tip: bin/migrate-layout]"
  printf '  %-14s %s\n' "$tok" "${where:-NOWHERE}"
done
for t in $(grep -oE 'bin/[A-Za-z_-]+(\.py)?' "$W/added.txt" | sort -u); do
  printf '  %-26s %s\n' "$t" "$([ -e "$W/new/$t" ] && echo 'in the candidate at the layer' || { git -C "$FORK" cat-file -e "$SRCREV:$t" 2>/dev/null && echo 'NOT in the candidate; in the tip (the next layer)' || echo NOWHERE; })"
done

echo; echo "## Section 6: the two open pull requests (git merge-tree --write-tree; exit 0 clean, 1 conflicts)"
for n in 94 92; do
  sha=$(gh pr view "$n" --repo KJ5HST/methodology --json headRefOid --jq .headRefOid)
  git -C "$FORK" cat-file -e "$sha^{commit}" 2>/dev/null || git -C "$FORK" fetch -q upstream "pull/$n/head"
  echo "#$n head ${sha:0:12}"
  for tip in "$PARENT" "$LAYER"; do
    out=$(git -C "$FORK" merge-tree --write-tree --name-only "$tip" "$sha" 2>&1); rc=$?
    first=$(printf '%s\n' "$out" | head -1)
    echo "== tip ${tip:0:7} against #$n: exit $rc (first line $(printf '%s' "$first" | grep -qE '^[0-9a-f]{40}$' && echo 'is a tree' || echo "IS NOT A TREE: $first"))"
    if [ "$rc" -eq 1 ]; then
      for f in $(printf '%s\n' "$out" | sed -n '2,/^$/p' | grep -v '^$'); do
        echo "   $f: $(git -C "$FORK" show "$first:$f" | grep -c '^<<<<<<<') conflict region(s)"
      done
    fi
  done
done

echo; echo "## Section 7: scrub input (a coarse regular expression over the layer's added lines, per file; the scrub is its own commit after the layers)"
for f in $(git -C "$W/new" diff --name-only "$PARENT" "$LAYER"); do
  git -C "$W/new" diff "$PARENT" "$LAYER" -- "$f" | grep -E '^\+' | grep -vE '^\+\+\+' > "$W/added1.txt"
  printf '%-58s added %4d | BL- %2d | phase %2d | session %2d | docs/planning %2d | learning %2d | FM %2d | plan %2d\n' "$f" \
    "$(wc -l < "$W/added1.txt")" \
    "$(grep -cE 'BL-[0-9]+' "$W/added1.txt")" "$(grep -cE '\bP[0-9]\b' "$W/added1.txt")" "$(grep -cE '\bS[0-9]{2,3}\b' "$W/added1.txt")" \
    "$(grep -c 'docs/planning/' "$W/added1.txt")" "$(grep -ciE 'learning #' "$W/added1.txt")" "$(grep -ciE 'FM #|failure mode #' "$W/added1.txt")" \
    "$(grep -ciE "plan [0-9]|plan's|section [0-9]|plan C[0-9]|plan D[0-9]" "$W/added1.txt")"
done
for c in $(git -C "$W/new" rev-list --reverse "$PARENT..$LAYER"); do
  git -C "$W/new" log -1 --format=%B "$c" > "$W/msg.txt"
  echo "commit $(git -C "$W/new" rev-parse --short "$c") message: $(grep -ciE 'BL-[0-9]+|\bS[0-9]{2,3}\b|\bP[0-9]\b|plan [0-9]|learning #' "$W/msg.txt") line(s) with a backlog code, session number, phase, plan section or learning"
done

echo; echo "## Section 8: the changed files, per commit and in all (git diff --numstat), and the candidate against upstream"
git -C "$W/new" log --format='%h %s' "$PARENT..$LAYER" | cut -c1-150
for c in $(git -C "$W/new" rev-list --reverse "$PARENT..$LAYER"); do
  echo "commit $(git -C "$W/new" rev-parse --short "$c"): $(git -C "$W/new" diff --name-only "$c~1" "$c" | wc -l | tr -d ' ') files"
done
git -C "$W/new" diff --numstat "$PARENT" "$LAYER" | awk '{a+=$1; d+=$2; printf "  %6s %6s  %s\n",$1,$2,$3} END {printf "  all: %d files, +%d / -%d\n", NR, a, d}'
UP=$(git -C "$FORK" rev-parse --short upstream/main)
echo "the candidate $(git -C "$W/new" rev-parse --short HEAD) against upstream/main $UP: $(git -C "$FORK" rev-list --count "upstream/main..$LAYER") commits; $(git -C "$FORK" diff --shortstat upstream/main "$LAYER")"
echo; echo "layer6c-measure done"
