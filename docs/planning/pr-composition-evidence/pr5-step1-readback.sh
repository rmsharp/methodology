#!/usr/bin/env bash
# PR5 step 1: read back the candidate branch on the fork's origin. Read-only: git objects, `git ls-remote` and
# GitHub's read endpoints; nothing is written or pushed. Run from the repository root:
#   bash docs/planning/pr-composition-evidence/pr5-step1-readback.sh <upstream> <candidate> <remote-branch>
# e.g.   ... d50ce290d921 47637be21425 feat/methodology-directory
# Every figure is printed beside the command that made it. Exit 0 only when every check below agrees; each failed
# check prints FAIL and the exit code is 1 (a red line inside a script that goes on must still end the script red).
set -u
UP=${1:?upstream commit}; CAND=${2:?candidate commit}; BR=${3:?remote branch name on origin}
FAILS=0
check() { if [ "$2" = "$3" ]; then echo "  ok   $1: $2"; else echo "  FAIL $1: got '$2', expected '$3'"; FAILS=$((FAILS+1)); fi; }

UPF=$(git rev-parse "$UP^{commit}") || exit 3; CANDF=$(git rev-parse "$CAND^{commit}") || exit 3
echo "upstream  $UPF"; echo "candidate $CANDF"; echo "remote branch origin/$BR"

echo; echo "== 1. the candidate, locally (git rev-list, git merge-base)"
N=$(git rev-list --count "$UPF..$CANDF"); echo "  commits over upstream: $N"
check "merges inside the range" "$(git rev-list --merges --count "$UPF..$CANDF")" "0"
check "merge-base equals upstream's tip" "$(git merge-base "$UPF" "$CANDF")" "$UPF"

echo; echo "== 2. the fork's origin (git ls-remote --heads origin)"
check "origin's $BR equals the candidate" "$(git ls-remote --heads origin "refs/heads/$BR" | cut -f1)" "$CANDF"
echo "  origin's other heads: $(git ls-remote --heads origin | cut -f2 | sed 's#refs/heads/##' | grep -vxF "$BR" | tr '\n' ' ')"

echo; echo "== 3. GitHub's own comparison with upstream's main (gh api repos/KJ5HST/methodology/compare/...)"
CMP=$(gh api "repos/KJ5HST/methodology/compare/main...rmsharp:$BR" --jq '[.status,.ahead_by,.behind_by,.merge_base_commit.sha,(.files|length)]|join(" ")') || { echo "  FAIL compare call"; FAILS=$((FAILS+1)); CMP="- - - - -"; }
set -- $CMP; echo "  status=$1 ahead_by=$2 behind_by=$3 merge_base=${4:0:12} files=$5"
check "GitHub status" "$1" "ahead"; check "GitHub ahead_by" "$2" "$N"; check "GitHub behind_by" "$3" "0"; check "GitHub merge base" "$4" "$UPF"

echo; echo "== 4. upstream, now (git ls-remote upstream; gh pr list)"
check "upstream main" "$(git ls-remote upstream refs/heads/main | cut -f1)" "$UPF"
check "pull requests from head '$BR' on upstream (none yet)" "$(gh pr list -R KJ5HST/methodology --head "$BR" --state all --json number --jq 'length')" "0"
gh pr list -R KJ5HST/methodology --state open --json number,headRefOid,mergeable,mergeStateStatus --jq '.[]|"  open #\(.number) head \(.headRefOid[0:8]) \(.mergeable) \(.mergeStateStatus)"'

echo; if [ "$FAILS" -eq 0 ]; then echo "READ-BACK OK (0 failed)"; else echo "READ-BACK FAILED ($FAILS failed)"; fi
[ "$FAILS" -eq 0 ]
