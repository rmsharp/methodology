#!/usr/bin/env bash
# PR5 step 2: read back the pull request that was opened on KJ5HST/methodology. Read-only: `gh pr view`, `gh api`
# (GET), `git ls-remote` and git objects; nothing is written, edited or pushed. Run from the repository root:
#   bash docs/planning/pr-composition-evidence/pr5-step2-readback.sh <pr-number> <upstream> <candidate> <remote-branch>
# e.g.   ... 99 d50ce290d921 47637be21425 feat/methodology-directory
# The expected title and body are rebuilt from docs/planning/upstream-pr-body.md (title: line 7 after '**Title:** ';
# body: lines 9 to 105, then one blank line and the attribution line) and compared with what GitHub holds.
# Exit 0 only when every check below agrees; each failed check prints FAIL and the exit code is 1.
set -u
PR=${1:?pull request number}; UP=${2:?upstream commit}; CAND=${3:?candidate commit}; BR=${4:?remote branch name}
DRAFT=docs/planning/upstream-pr-body.md
FOOTER='🤖 Generated with [Claude Code](https://claude.com/claude-code)'
FAILS=0
check() { if [ "$2" = "$3" ]; then echo "  ok   $1: $2"; else echo "  FAIL $1: got '$2', expected '$3'"; FAILS=$((FAILS+1)); fi; }

UPF=$(git rev-parse "$UP^{commit}") || exit 3; CANDF=$(git rev-parse "$CAND^{commit}") || exit 3
N=$(git rev-list --count "$UPF..$CANDF"); STAT=$(git diff --shortstat "$UPF" "$CANDF")
echo "pull request #$PR; upstream $UPF; candidate $CANDF ($N commits); $STAT"

echo; echo "== 1. the pull request (gh pr view)"
J=$(gh pr view "$PR" -R KJ5HST/methodology --json state,isDraft,baseRefName,headRefName,headRepositoryOwner,headRefOid,title,commits,changedFiles,additions,deletions,comments,reviews,mergeable,mergeStateStatus) || { echo "  FAIL gh pr view"; exit 1; }
f() { printf '%s' "$J" | python3 -c "import sys,json; d=json.load(sys.stdin); print($1)"; }
check "state" "$(f 'd["state"]')" "OPEN"
check "draft" "$(f 'str(d["isDraft"]).lower()')" "false"
check "base" "$(f 'd["baseRefName"]')" "main"
check "head" "$(f 'd["headRepositoryOwner"]["login"]+":"+d["headRefName"]')" "rmsharp:$BR"
check "head commit" "$(f 'd["headRefOid"]')" "$CANDF"
check "commits" "$(f 'len(d["commits"])')" "$N"
check "files changed" "$(f 'd["changedFiles"]')" "$(git diff --name-only "$UPF" "$CANDF" | wc -l | tr -d ' ')"
check "lines added" "$(f 'd["additions"]')" "$(git diff --numstat "$UPF" "$CANDF" | awk '{s+=$1} END{print s}')"
check "lines removed" "$(f 'd["deletions"]')" "$(git diff --numstat "$UPF" "$CANDF" | awk '{s+=$2} END{print s}')"
echo "  info mergeable=$(f 'd["mergeable"]') mergeStateStatus=$(f 'd["mergeStateStatus"]') comments=$(f 'len(d["comments"])') reviews=$(f 'len(d["reviews"])')"

echo; echo "== 2. the title and the body, against the approved draft"
check "title" "$(f 'd["title"]')" "$(sed -n 7p "$DRAFT" | sed 's/^\*\*Title:\*\* //')"
EXP=$(sed -n 9,105p "$DRAFT"; printf '\n%s\n' "$FOOTER")
GOT=$(gh api "repos/KJ5HST/methodology/pulls/$PR" --jq .body | tr -d '\r')
check "body bytes" "$(printf '%s' "$GOT" | wc -c | tr -d ' ')" "$(printf '%s' "$EXP" | wc -c | tr -d ' ')"
check "body text (sha of the two)" "$(printf '%s' "$GOT" | shasum -a 256 | cut -c1-12)" "$(printf '%s' "$EXP" | shasum -a 256 | cut -c1-12)"

echo; echo "== 3. the fork's branch and upstream, now (git ls-remote)"
check "origin's $BR equals the candidate" "$(git ls-remote --heads origin "refs/heads/$BR" | cut -f1)" "$CANDF"
check "upstream main" "$(git ls-remote upstream refs/heads/main | cut -f1)" "$UPF"
gh pr list -R KJ5HST/methodology --state open --json number,headRefOid,mergeable,mergeStateStatus --jq '.[]|"  open #\(.number) head \(.headRefOid[0:8]) \(.mergeable) \(.mergeStateStatus)"'

echo; if [ "$FAILS" -eq 0 ]; then echo "READ-BACK OK (0 failed)"; else echo "READ-BACK FAILED ($FAILS failed)"; fi
[ "$FAILS" -eq 0 ]
