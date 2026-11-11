#!/usr/bin/env bash
# Reproduces the defect in docs/planning/sync-seed-paths-plan.md and measures its oracle (what bin/migrate-layout
# produces). READ-ONLY for the repository: every write goes to a throwaway directory that is removed on exit.
# Standard tools only: bash, git, python3. Run from anywhere:   bash docs/planning/sync-seed-paths-evidence/reproduce.sh
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="${METHODOLOGY_REPO:-$(cd "$HERE/../../.." && pwd)}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
export GIT_AUTHOR_NAME=scratch GIT_AUTHOR_EMAIL=scratch@example.invalid
export GIT_COMMITTER_NAME=scratch GIT_COMMITTER_EMAIL=scratch@example.invalid
# The synced rows carry `canonical: ../methodology/starter-kit/...`, relative to the project: give both throwaway
# projects the sibling checkout an adopter has.
ln -s "$REPO" "$TMP/methodology"
strip() { sed 's/\x1b\[[0-9;]*m//g'; }
# Both projects get the two files the budget config also names that sync does not provide (a purpose statement in
# CLAUDE.md inside its protected block, and LEARNINGS.md), so the one thing left to differ between them is the layout.
own_files() {
  python3 - "$1" <<'PY'
import sys
r = sys.argv[1]
open(r + "/CLAUDE.md", "w").write("<!-- budget:protected -->\n" + "A throwaway project for a reproduction; it states its purpose here.\n" * 20 + "<!-- /budget:protected -->\n")
open(r + "/LEARNINGS.md", "w").write("# Learnings\n")
PY
}

echo "== Part 1: a fresh project started with bin/sync --layout new =="
mkdir "$TMP/new" && git -C "$TMP/new" init -q && own_files "$TMP/new"
python3 "$REPO/bin/sync" "$TMP/new" --layout new --source local >/dev/null 2>&1
echo "sync --layout new exit: $?"

echo "[E1] the values the two seeded configs carry"
python3 - "$TMP/new" <<'PY'
import json, sys
r = sys.argv[1]
c = json.load(open(r + "/methodology/.context-budget.json"))
q = json.load(open(r + "/methodology/.quality-gates.json"))
for f in c["files"]:
    print("  budget row    ", f["path"])
for f in c["synced"]:
    print("  synced row    ", f["path"])
print("  results_file  ", q.get("results_file"))
PY

echo "[E2] context_budget.py --status, run from the project root: the three rows that name a moved file"
(cd "$TMP/new" && python3 methodology/context_budget.py --status 2>&1 | strip \
    | grep -E 'SESSION_NOTES|SESSION_RUNNER|SAFEGUARDS'; echo "  exit code of the tool: ${PIPESTATUS[0]}")

echo "[E3] quality_ratchet.py --run, run from the project root: where the results file lands"
(cd "$TMP/new" && python3 methodology/quality_ratchet.py --run >/dev/null 2>&1; echo "  exit code of the tool: $?")
echo "  results at the project root:     $([ -e "$TMP/new/.quality-gates-results.json" ] && echo yes || echo no)"
echo "  results under methodology/:      $([ -e "$TMP/new/methodology/.quality-gates-results.json" ] && echo yes || echo no)"

echo
echo "== Part 2: the oracle: a project started in the legacy layout, then moved by bin/migrate-layout =="
mkdir "$TMP/old" && git -C "$TMP/old" init -q && own_files "$TMP/old"
python3 "$REPO/bin/sync" "$TMP/old" --layout legacy --source local >/dev/null 2>&1
echo "sync --layout legacy exit: $?"
# The migration refuses a move that would drop a file under 90% similarity (git log --follow would lose its history):
# a seeded ledger is too small to take the migration's entry, so pad it. The configs are not touched by the padding.
python3 - "$TMP/old" <<'PY'
import sys
p = sys.argv[1] + "/CHANGELOG.md"
s = open(p).read()
s += "\n" + "".join(
    "### 2026-10-%02d · [ad hoc] filler entry %d -- padding so the ledger keeps its history across a move\n\n"
    "Body line for entry %d, long enough to count toward the similarity ratio.\n\n" % ((i % 27) + 1, i, i)
    for i in range(60))
open(p, "w").write(s)
PY
git -C "$TMP/old" add -A && git -C "$TMP/old" commit -q -m "scratch: legacy sync, padded ledger"
python3 "$REPO/bin/migrate-layout" "$TMP/old" --apply >/dev/null 2>&1
echo "migrate-layout --apply exit: $?"

echo "[E4] migrated configs against a fresh --layout new sync (< migrated, > fresh sync; no line = identical)"
for f in .context-budget.json .quality-gates.json; do
  echo "  $f"
  diff "$TMP/old/methodology/$f" "$TMP/new/methodology/$f" | grep '^[<>]' | sed 's/^/    /'
done

echo "[E5] what migration changes in each canonical seed (< the seed as shipped, > migrated)"
for pair in ".context-budget.json:starter-kit/context-budget.json" ".quality-gates.json:starter-kit/quality-gates.json"; do
  d="${pair%%:*}"; s="${pair##*:}"
  echo "  $d"
  diff "$REPO/$s" "$TMP/old/methodology/$d" | grep '^[<>]' | sed 's/^/    /'
done

echo "[E6] the same project, after migration: the three rows are measured"
(cd "$TMP/old" && python3 methodology/context_budget.py --status 2>&1 | strip \
    | grep -E 'SESSION_NOTES|SESSION_RUNNER|SAFEGUARDS'; echo "  exit code of the tool: ${PIPESTATUS[0]}")
