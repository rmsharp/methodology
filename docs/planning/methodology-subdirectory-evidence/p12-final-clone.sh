#!/bin/bash
set -u
S=${SCRATCH:?set SCRATCH to a scratch directory}
R=$S/p12-final; A=$HOME/Development/feedback-loop-comparison; M=$HOME/Development/methodology
rm -rf "$R"; mkdir -p "$R"; exec > "$R/log.txt" 2>&1
printf 'adopter HEAD %s\n' "$(git -C "$A" rev-parse HEAD)"
git clone -q --no-local "$A" "$R/head"
cd "$R/head"
# Phase 0 in the new layout (read steps run from the project root)
for f in methodology/SESSION_RUNNER.md methodology/SAFEGUARDS.md methodology/SESSION_NOTES.md methodology/CHANGELOG.md methodology/HANDOFFS.md; do test -f "$f" && printf 'present %s\n' "$f" || printf 'MISSING %s\n' "$f"; done
cmp methodology/SAFEGUARDS.md "$M/starter-kit/SAFEGUARDS.md" && echo 'SAFEGUARDS byte-identical to canonical'
cmp methodology/SESSION_RUNNER.md "$M/starter-kit/SESSION_RUNNER.md" && echo 'SESSION_RUNNER byte-identical to canonical'
grep -n -m1 'ACTIVE TASK' methodology/SESSION_NOTES.md
git status --short | wc -l; git log --oneline -5; git diff --stat | tail -1
python3 methodology/methodology_dashboard.py --no-open > "$R/dash.txt" 2>&1; printf 'dashboard exit=%s\n' "$?"
F=$(git log -1 --format=%H -- methodology/CHANGELOG.md); printf 'CHANGELOG frontier %s; undocumented: %s\n' "$F" "$(git rev-list --count --no-merges "$F"..HEAD)"
H=$(git log -1 --format=%H -- methodology/HANDOFFS.md); printf 'HANDOFFS frontier %s; commits after: %s\n' "$H" "$(git rev-list --count --no-merges "$H"..HEAD)"
git log --merges --oneline "$F"..HEAD | wc -l
# the adopter's own build equivalent
quarto render index.qmd > "$R/render.txt" 2>&1; printf 'render exit=%s warnings=%s\n' "$?" "$(grep -c -i warning "$R/render.txt")"
printf 'html %s pdftext %s\n' "$(shasum -a 256 index.html | cut -c1-12)" "$(pdftotext index.pdf - 2>/dev/null | shasum -a 256 | cut -c1-12)"
touch "$R/DONE"
