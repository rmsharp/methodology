#!/usr/bin/env bash
# PR2 Part 2, the last layer (bin/migrate-layout): the measurements the record cites that the other scripts do not print, in one saved run.
#   layer7b-measure.sh <fork-repo> <layer-commit> <parent-commit> <source-rev> <scratch-dir>
# <fork-repo> holds the candidate's commits as local objects (this repository after a forced fetch of `pr2/candidate`) and the fork's
# tip <source-rev> the builder reads. <parent-commit> is the prose layer's `18cda0f`; <layer-commit> is the layer's LAST commit (the layer
# is two: the tool, then its suite and gates). Everything runs in scratch clones under <scratch-dir>; nothing in <fork-repo> is written.
# Serial. The mutants have their own script and output (layer7b-mutate.py); the shell suite, the migration suite and the ratchet run are
# layer-verify.sh's and the saved suite outputs.
# Sections: 1 the files, per commit and in all, and which are the tip's bytes whole; 2 the builder reproduces the layer's tree and refuses
# on drift; 3 the scanner, the layout suite and the link check on the parent and on the layer; 4 the tool run as a command in a project
# the layer's own bin/sync wrote; 5 the prose's claims about the tool, read against the tool that now exists; 6 the two open pull requests;
# 7 scrub input; 8 the candidate against upstream.
set -u
FORK=${1:?fork repository}; LAYER=${2:?layer commit}; PARENT=${3:?parent commit}; SRCREV=${4:?source revision}; W=${5:?scratch dir}/layer7b-measure
HERE=$(cd "$(dirname "$0")" && pwd)
rm -rf "$W"; mkdir -p "$W"
export PYTHONDONTWRITEBYTECODE=1
clone() { git clone --no-local -q "$FORK" "$1" && git -C "$1" checkout -q "$2" && git -C "$1" config user.name measure && git -C "$1" config user.email m@m && git -C "$1" config --unset core.hooksPath 2>/dev/null; return 0; }

echo "## Section 1: the files, per commit and in all; and which are the tip's bytes whole (git rev-parse of the two blobs)"
git -C "$FORK" log --format='%h %s' "$PARENT..$LAYER" | cut -c1-150
for c in $(git -C "$FORK" rev-list --reverse "$PARENT..$LAYER"); do
  echo "commit $(git -C "$FORK" rev-parse --short "$c"): $(git -C "$FORK" diff --name-only "$c~1" "$c" | wc -l | tr -d ' ') files"
done
git -C "$FORK" diff --numstat "$PARENT" "$LAYER" | awk '{a+=$1; d+=$2; printf "  %6s %6s  %s\n",$1,$2,$3} END {printf "  all: %d files, +%d / -%d\n", NR, a, d}'
for f in bin/migrate-layout tools/test_migrate_layout.py tools/test_sync_layouts.py tools/test_layout_resolver.py bin/tests.sh .quality-gates.json; do
  a=$(git -C "$FORK" rev-parse "$LAYER:$f" | cut -c1-9); b=$(git -C "$FORK" rev-parse "$SRCREV:$f" | cut -c1-9)
  printf '  %-34s layer %s  tip %s  %s\n' "$f" "$a" "$b" "$([ "$a" = "$b" ] && echo 'the tip'"'"'s bytes whole' || echo 'differs from the tip (by design: see the record)')"
done
printf '  mode of bin/migrate-layout at the layer: %s\n' "$(git -C "$FORK" ls-tree "$LAYER" bin/migrate-layout | cut -d' ' -f1)"

echo; echo "## Section 2: the builder reproduces the layer's tree, and refuses on drift"
clone "$W/new" "$LAYER"; clone "$W/repro" "$PARENT"
( cd "$W/repro" \
  && python3 -I -B "$HERE/layer7b-build.py" "$FORK" "$SRCREV" . --stage tool | tail -1 && git add -A && git -c commit.gpgsign=false commit -q -m tool \
  && python3 -I -B "$HERE/layer7b-build.py" "$FORK" "$SRCREV" . --stage suite --slow-seconds 365 | tail -1 \
  && python3 -I -B "$HERE/layer7b-build.py" "$FORK" "$SRCREV" . --stage suite --migrate-count 280 --passed 302 --layout-count 76 | tail -1 \
  && git add -A && echo "built tree   $(git write-tree | cut -c1-12)" )
echo "layer's tree $(git -C "$W/new" rev-parse "HEAD^{tree}" | cut -c1-12)"
clone "$W/drift" "$PARENT"
printf '\n# one line of drift\n' >> "$W/drift/bin/sync"
git -C "$W/drift" commit -q -am "drift in the candidate's bin/sync"
( cd "$W/drift" && python3 -I -B "$HERE/layer7b-build.py" "$FORK" "$SRCREV" . --stage tool 2>&1 | tail -1 | cut -c1-240 )
echo "dirty paths after the refusal: $(git -C "$W/drift" status --short | wc -l | tr -d ' ')"
clone "$W/drift2" "$PARENT"
printf '\n' >> "$W/drift2/tools/test_sync_layouts.py"
git -C "$W/drift2" commit -q -am "drift in the candidate's sync suite"
( cd "$W/drift2" && python3 -I -B "$HERE/layer7b-build.py" "$FORK" "$SRCREV" . --stage tool 2>&1 | tail -1 | cut -c1-240 )
echo "dirty paths after the refusal: $(git -C "$W/drift2" status --short | wc -l | tr -d ' ')"

echo; echo "## Section 3: the scanner, the layout suite and the link check, on the parent and on the layer"
clone "$W/parent" "$PARENT"
for t in parent new; do
  ( cd "$W/$t" && echo "-- $t ($(git rev-parse --short HEAD))"
    python3 bin/check-layout-literals | tail -1 | cut -c1-150
    python3 tools/test_layout_resolver.py 2>&1 | grep -aE '^Ran |^OK|^FAILED' | tr '\n' ' '; echo
    python3 bin/check-links --layout both 2>&1 | grep -E '^check-links:' | cut -c1-150 )
done

echo; echo "## Section 4: the tool run as a command in a project the layer's own bin/sync wrote (legacy layout), dry run then --apply, and its refusals"
P="$W/proj"; mkdir "$P"; git -C "$P" init -q; git -C "$P" config user.name measure; git -C "$P" config user.email m@m
git -C "$P" commit -q --allow-empty -m "initial commit"
( cd "$W/new" && python3 bin/sync "$P" --mode=commit --layout legacy >/dev/null 2>&1; echo "sync --layout legacy: exit $?" )
if [ -n "$(git -C "$P" status --short)" ]; then git -C "$P" add -A && git -C "$P" commit -q -m "sync the methodology files before the layout migration" && echo "(bin/sync wrote the files; committed them as the adopters' script does)"; fi
echo "project: $(git -C "$P" log --oneline | wc -l | tr -d ' ') commit(s), $(git -C "$P" ls-files | wc -l | tr -d ' ') tracked files, status: $(git -C "$P" status --short | wc -l | tr -d ' ') dirty"
( cd "$W/new" && python3 bin/status "$P" 2>&1 | grep -E '^layout:|layout:' | head -2 )
( cd "$W/new" && python3 bin/migrate-layout "$P" > "$W/dry.out" 2>&1; echo "dry run: exit $? (writes nothing: $(git -C "$P" status --short | wc -l | tr -d ' ') dirty paths)"; sed -n 1,6p "$W/dry.out" | cut -c1-170 )
echo "-- a dirty tree is refused:"
echo x > "$P/stray.txt"
( cd "$W/new" && python3 bin/migrate-layout "$P" --apply > "$W/refuse.out" 2>&1; echo "apply on a dirty tree: exit $?"; grep -iE 'dirty|refus' "$W/refuse.out" | head -3 | cut -c1-170 )
rm -f "$P/stray.txt"
echo "-- an apply over the seed ledger, which is a few lines long, is rolled back by the tool's own rule (a moved file must stay 90% similar):"
BEFORE=$(git -C "$P" rev-parse HEAD)
( cd "$W/new" && python3 bin/migrate-layout "$P" --apply > "$W/apply0.out" 2>&1; echo "apply: exit $?"; grep -E '^ROLLED BACK' "$W/apply0.out" | cut -c1-200 )
echo "  after the rollback: HEAD $([ "$(git -C "$P" rev-parse HEAD)" = "$BEFORE" ] && echo unchanged || echo CHANGED), dirty paths $(git -C "$P" status --short | wc -l | tr -d ' '), runner at the root $([ -e "$P/SESSION_RUNNER.md" ] && echo yes || echo no)"
echo "-- the same project with a ledger of 80 entries (a real project's ledger is longer), then an apply:"
for i in $(seq 1 80); do printf '### 2026-09-%02d · [ad hoc] entry %d\n\nA line of what the session did, with enough words in it to look like a ledger line.\n\n' $(( (i % 28) + 1 )) "$i" >> "$P/CHANGELOG.md"; done
git -C "$P" commit -q -am "a project ledger with history"
BEFORE=$(git -C "$P" rev-parse HEAD); NBEFORE=$(git -C "$P" rev-list --count HEAD)
( cd "$W/new" && python3 bin/migrate-layout "$P" --apply > "$W/apply.out" 2>&1; echo "apply: exit $?"; grep -A7 -E '^checks \(before' "$W/apply.out" | cut -c1-200; grep -E '^APPLIED' "$W/apply.out" )
echo "after: $(git -C "$P" rev-list --count HEAD) commit(s) against $NBEFORE before; the migration commit: $(git -C "$P" log -1 --format=%s | cut -c1-90)"
echo "  renames git follows in it: $(git -C "$P" show -M --name-status --format= HEAD | grep -c '^R') of $(git -C "$P" show -M --name-status --format= HEAD | wc -l | tr -d ' ') paths; lowest similarity: $(git -C "$P" show -M --name-status --format= HEAD | grep '^R' | cut -c2-4 | sort -n | head -1 | sed 's/^0*//')%"
echo "  not renamed: $(git -C "$P" show -M --name-status --format= HEAD | grep -v '^R' | tr '\t' ' ' | tr '\n' ';' | cut -c1-200)"
echo "  files at the root now: $(git -C "$P" ls-files | grep -vc /) ; under methodology/: $(git -C "$P" ls-files methodology | wc -l | tr -d ' ')"
echo "  the runner at the root: $([ -e "$P/SESSION_RUNNER.md" ] && echo yes || echo no); under methodology/: $([ -e "$P/methodology/SESSION_RUNNER.md" ] && echo yes || echo no); dirty after: $(git -C "$P" status --short | wc -l | tr -d ' ')"
( cd "$W/new" && python3 bin/status "$P" 2>&1 | grep -E 'layout:' | head -1 )
( cd "$W/new" && python3 bin/migrate-layout "$P" > "$W/again.out" 2>&1; echo "a second run on the migrated project: exit $? ($(head -1 "$W/again.out" | cut -c1-120))" )

echo; echo "## Section 5: the prose's claims about the tool, read against the tool that now exists (the prose layer's NOT CHECKED, S321's record section 4)"
git -C "$W/new" diff 505541c "$PARENT" -- '*.md' | grep -E '^\+' | grep -vE '^\+\+\+' > "$W/added.txt"
echo "lines the prose layer added that name the tool: $(grep -c 'migrate-layout' "$W/added.txt")"
grep 'migrate-layout' "$W/added.txt" | cut -c1-230
for tok in $(grep -oE '(^|[^[:alnum:]-])--[a-z][a-z-]+' "$W/added.txt" | grep -oE '\-\-[a-z][a-z-]+' | sort -u); do
  where=""
  for t in bin/migrate-layout bin/sync bin/status bin/check-links bin/check-ledger bin/check-handoff starter-kit/methodology_trim.py starter-kit/context_budget.py starter-kit/quality_ratchet.py starter-kit/methodology_dashboard.py; do
    grep -q -- "$tok" "$W/new/$t" 2>/dev/null && where="$where $t"
  done
  printf '  %-14s %s\n' "$tok" "${where:-NOWHERE}"
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
  printf '%-34s added %4d | BL- %3d | phase %3d | session %3d | docs/planning %3d | learning %2d | FM %2d | plan %3d\n' "$f" \
    "$(wc -l < "$W/added1.txt")" \
    "$(grep -cE 'BL-[0-9]+' "$W/added1.txt")" "$(grep -cE '\bP[0-9]+\b' "$W/added1.txt")" "$(grep -cE '\bS[0-9]{2,3}\b' "$W/added1.txt")" \
    "$(grep -c 'docs/planning/' "$W/added1.txt")" "$(grep -ciE 'learning #' "$W/added1.txt")" "$(grep -ciE 'FM #|failure mode #' "$W/added1.txt")" \
    "$(grep -ciE "plan [0-9]|plan's|section [0-9]|plan C[0-9]|plan D[0-9]" "$W/added1.txt")"
done
for c in $(git -C "$W/new" rev-list --reverse "$PARENT..$LAYER"); do
  git -C "$W/new" log -1 --format=%B "$c" > "$W/msg.txt"
  echo "commit $(git -C "$W/new" rev-parse --short "$c") message: $(grep -ciE 'BL-[0-9]+|\bS[0-9]{2,3}\b|\bP[0-9]\b|plan [0-9]|learning #' "$W/msg.txt") line(s) with a backlog code, session number, phase, plan section or learning"
done

echo; echo "## Section 8: the candidate against upstream"
UP=$(git -C "$FORK" rev-parse --short upstream/main)
echo "the candidate $(git -C "$W/new" rev-parse --short HEAD) against upstream/main $UP: $(git -C "$FORK" rev-list --count "upstream/main..$LAYER") commits; $(git -C "$FORK" diff --shortstat upstream/main "$LAYER")"
echo; echo "layer7b-measure done"
