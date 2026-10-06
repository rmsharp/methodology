#!/usr/bin/env bash
# What would the fork's NEXT resync (merging upstream/main into fork main) meet if this repository's own
# instance files had moved into methodology/?  Measured on throwaway clones; the real repo is only read.
#   1  Does git still pair each moved file with its root original (rename detection), measured against the
#      merge base with upstream/main (the commit a resync merges from)?
#   2  A synthetic upstream commit (one line into each root file upstream also owns, plus one NEW shard) is
#      merge-tree'd against the fork with the files moved, and against the fork unmoved (the control).
# Needs the refs `upstream/main` and `main`. Run from the repo root:
#   bash docs/planning/methodology-subdirectory-evidence/resync-after-move.sh
set -u
SRC="$(git rev-parse --show-toplevel)" || exit 3
BASE="$(git merge-base main upstream/main)" || exit 3
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
git clone -q --no-local "$SRC" "$T/c"; cd "$T/c" || exit 3
git config core.hooksPath /dev/null; git config user.email t@t; git config user.name t; git config commit.gpgsign false
git checkout -q main
UNMOVED="$(git rev-parse HEAD)"
mkdir methodology
for f in CHANGELOG.md HANDOFFS.md .context-budget.json .context-budget-history.jsonl .quality-gates.json \
         .gitattributes dashboard_history.jsonl; do git mv "$f" "methodology/$f"; done
git mv docs/archive methodology/archive
git commit -q -m 'instance files and archive move'; MOVED="$(git rev-parse HEAD)"
printf 'merge base with upstream/main: %s\n' "$(git rev-parse --short "$BASE")"
printf '\n== 1. rename detection, merge base -> fork with the files moved ==\n'
git diff -M --name-status "$BASE" "$MOVED" | grep -E 'CHANGELOG|HANDOFFS|context-budget|quality-gates|gitattributes|dashboard_history' | grep -v 'docs/'
printf '(R100 = paired as a rename; a D and an A = NOT paired, even at the default 50%% threshold)\n'
printf 'ledgers at a 30%% threshold: '; git diff -M30% --name-status "$BASE" "$MOVED" -- CHANGELOG.md HANDOFFS.md methodology/CHANGELOG.md methodology/HANDOFFS.md | tr '\n' ' '; printf '\n'

git checkout -q -b up "$BASE"
printf '\n<!-- up -->\n' >> CHANGELOG.md; printf '\n<!-- up -->\n' >> HANDOFFS.md; printf 'x\n' >> .gitattributes
python3 -I - <<'PYEOF'
import json
for f in (".context-budget.json", ".quality-gates.json"):
    d = json.load(open(f)); d["_up_edit"] = "x"; open(f, "w").write(json.dumps(d, indent=2) + "\n")
PYEOF
printf 'new shard\n' > docs/archive/CHANGELOG-through-2099-01-01.md
git add -A; git commit -q -m 'upstream-like edit'; UP="$(git rev-parse HEAD)"
printf '\n== 2a. fork UNMOVED vs the upstream-like edit (control) ==\n'
git merge-tree --write-tree --name-only "$UNMOVED" "$UP" 2>&1 | grep -E '^(CONFLICT|Auto-merging)'
printf '\n== 2b. fork with the files MOVED vs the same edit ==\n'
git merge-tree --write-tree --name-only "$MOVED" "$UP" 2>&1 | grep -E '^(CONFLICT|Auto-merging)' | cut -c1-110
