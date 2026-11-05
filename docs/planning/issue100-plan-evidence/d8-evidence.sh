#!/usr/bin/env bash
# Evidence for decision D8 of docs/planning/issue100-fixes-plan.md (S419): what a Phase 0 step that runs
# the budget tool would print, and what the fork's fix for upstream issue #95 would cost to send.
#   bash docs/planning/issue100-plan-evidence/d8-evidence.sh [ADOPTER_PARENT_DIR]
# READ-ONLY. It runs the fork's starter-kit/context_budget.py with --json, which writes no history line,
# from inside each named adopter directory; it never writes into an adopter and never recurses over the
# parent directory (the twelve names are listed below). The merge trials use `git merge-tree --write-tree`,
# which builds objects only; --attr-source is the EMPTY tree so merge=union does not apply, as on GitHub.
# Tags: [survey-*] one line per adopter and the totals; [replay-*] the fork's two #95 commits replayed.
set -u
PARENT=${1:-$HOME/Development}
cd "$(git rev-parse --show-toplevel)" || exit 3
ROOT=$PWD
TOOL=$ROOT/starter-kit/context_budget.py
EMPTY=4b825dc642cb6eb9a060e54bf8d69288fbee4904
echo "# d8-evidence: fork HEAD $(git rev-parse --short=8 HEAD), upstream/main $(git rev-parse --short=8 upstream/main), tool $(python3 -I "$TOOL" --help | head -1 | cut -d' ' -f1-2)"

echo
echo "# 1. the shipping budget tool (the fork's) read on each adopter's files as they are today"
ADOPTERS="airqino chat_verification church_growth colossians_1_15_20 data_quality_assurance feedback-loop-comparison model_project_constructor mts-system nprcgenekeepr Philippians vscode_quarto_ext wsfct"
n=0; e0=0; e1=0; e2=0; fence=0; solely=0
for d in $ADOPTERS; do
  [ -d "$PARENT/$d" ] || { echo "[survey-skip] $d: no directory under $PARENT"; continue; }
  line=$(cd "$PARENT/$d" && python3 -I "$TOOL" --json 2>/dev/null | python3 -I -c '
import sys, json
d = json.load(sys.stdin)
over = [f for f in d["files"] if f["status"] == "over"]
msgs = lambda f: [x["msg"] for x in f["findings"]]
fence = any("fence is missing" in m for f in d["files"] for m in msgs(f))
# over ONLY because of the missing fence: every over file is over for that one finding alone
solely = bool(over) and all(msgs(f) and all("fence is missing" in m for m in msgs(f)) for f in over)
print(len(over), int(fence), int(solely), ",".join(f["path"].split("/")[-1].replace(" ", "_") for f in over) or "-")
')
  rc=$(cd "$PARENT/$d" && python3 -I "$TOOL" --status >/dev/null 2>&1; echo $?)
  set -- $line
  echo "[survey-adopter] $d exit=$rc over_files=$1 fence_missing=$2 over_only_for_fence=$3 over=$4"
  n=$((n+1)); fence=$((fence+$2)); solely=$((solely+$3))
  case $rc in 0) e0=$((e0+1));; 1) e1=$((e1+1));; 2) e2=$((e2+1));; esac
done
echo "[survey-total] adopters=$n exit0=$e0 exit1=$e1 exit2=$e2 fence_missing=$fence over_only_for_fence=$solely"

echo
echo "# 2. the fork's two #95 commits (cadb4780 the tool, 19a4ecb8 the seeds and Test 35) replayed onto each head"
echo "#    base = the fork's tree before them, so this is an UPPER BOUND on conflicts; CHANGELOG.md is the fork's own ledger"
BASE=$(git rev-parse cadb4780^); THEIRS=$(git rev-parse 19a4ecb8)
echo "[replay-files] $(git diff --name-only "$BASE" "$THEIRS" | tr '\n' ' ')"
for pr in 102 99 98 96; do
  sha=$(gh pr view "$pr" --repo KJ5HST/methodology --json headRefOid --jq .headRefOid)
  git cat-file -e "$sha^{commit}" 2>/dev/null || git fetch -q upstream "pull/$pr/head"
  echo "[replay-head] #$pr ${sha:0:8} VERSION $(git show "$sha:starter-kit/context_budget.py" | grep -m1 '^VERSION' | cut -d'#' -f1 | tr -d ' ')"
done
trial() {   # trial <label> <target>
  local out rc tree detail="" f n
  out=$(git --attr-source=$EMPTY merge-tree --write-tree --name-only --merge-base="$BASE" "$2" "$THEIRS" 2>&1); rc=$?
  tree=$(printf '%s\n' "$out" | head -1)
  if [ "$rc" -eq 1 ]; then
    for f in $(printf '%s\n' "$out" | sed -n '2,/^$/p' | grep -v '^$' | sort -u); do
      n=$(git show "$tree:$f" 2>/dev/null | grep -c '^<<<<<<<'); detail="$detail $f:$n"
    done
  fi
  echo "[replay-trial] $1 exit=$rc regions per file:${detail:- none}"
  if [ "$rc" -eq 1 ]; then   # name the first line of the region in the tool, so the note below is a measurement
    echo "[replay-region] $1 starter-kit/context_budget.py first line of the target side: $(git show "$tree:starter-kit/context_budget.py" | awk '/^<<<<<<</{getline; print; exit}' | cut -c1-60)"
  fi
}
trial "upstream/main $(git rev-parse --short=8 upstream/main)" upstream/main
for pr in 102 99 98 96; do
  sha=$(gh pr view "$pr" --repo KJ5HST/methodology --json headRefOid --jq .headRefOid)
  trial "#$pr ${sha:0:8}" "$sha"
done
echo "[replay-note] the one non-ledger region is the VERSION line of starter-kit/context_budget.py (upstream 1.3.1, #99 1.4.0, the fork 1.4.1)"
