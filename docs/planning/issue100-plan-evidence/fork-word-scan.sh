#!/usr/bin/env bash
# fork-word-scan.sh -- does text meant for the maintainer still carry this fork's own words?
#
# Fork only; not distributed. Added at S417 after the same miss happened in two sessions in a row:
# the word `upstream` (the maintainer's own repository is not "upstream" to him) was left out of a
# hand-typed pattern at S416 and again at S417, and survived in "Upstream's own gates on a clean
# clone of the tip" until a second scan found it. The pattern lives here, once, so the next scan
# is this script and not a pattern typed from memory.
#
# Usage:  bash docs/planning/issue100-plan-evidence/fork-word-scan.sh [BRANCH-OR-SHA] [DRAFT-FILE]
#   BRANCH-OR-SHA  the tip whose diff and commit messages are scanned (default issue100-batch-a)
#   DRAFT-FILE     the file holding the PR TEXT block (default the Batch A draft)
#   BASE           environment variable, the ref the branch is measured from (default upstream/main)
#
# Three places are scanned separately, because a hit in one says nothing about the others:
#   1. the text between the BEGIN PR TEXT and END PR TEXT markers of DRAFT-FILE
#   2. the ADDED lines of `git diff BASE BRANCH`
#   3. the commit messages in BASE..BRANCH
# Exit 0: no hit in any place. Exit 1: at least one hit (printed with its place and line).
# Exit 2: a usage or git error (a scan that could not read a place is not a clean scan).

set -u
cd "$(git rev-parse --show-toplevel)" || exit 2

BRANCH=${1:-issue100-batch-a}
DRAFT=${2:-docs/planning/issue100-batch-a-pr-draft.md}
BASE=${BASE:-upstream/main}

# A: words of this fork, matched in every place, any case.
A='BL-[0-9]+|\bS[0-9]{3}\b|the operator|Learning #|docs/planning|issue100|piece [0-9]|Batch [AB]|scratch clone|we chose|I measured|the fork|\bfork\b|upstream|the plan\b'
# B: first-person and plan-label tokens, matched case-sensitively in prose places only (code has
# variables named i, I/O, F1 and the like).
B='\bI\b|\bmy\b|\bF[1-6]\b|\bD[1-8]\b'

[ -f "$DRAFT" ] || { echo "fork-word-scan: no such draft file: $DRAFT" >&2; exit 2; }
git rev-parse --verify --quiet "$BRANCH^{commit}" >/dev/null || { echo "fork-word-scan: not a commit: $BRANCH" >&2; exit 2; }
git rev-parse --verify --quiet "$BASE^{commit}" >/dev/null || { echo "fork-word-scan: not a commit: $BASE" >&2; exit 2; }

hits=0
# scan LABEL USE_B  (text on stdin)
scan() {
  local label=$1 use_b=$2 text found fa fb=""
  text=$(cat)
  fa=$(printf '%s\n' "$text" | grep -n -i -E "$A")
  if [ "$use_b" = yes ]; then
    fb=$(printf '%s\n' "$text" | grep -n -E "$B" | sed 's/^/B /')
  fi
  found=$(printf '%s\n%s\n' "$fa" "$fb" | sed '/^$/d')
  if [ -n "$found" ]; then
    echo "HIT  $label"
    printf '%s\n' "$found" | cut -c1-220 | sed 's/^/       /'
    hits=$((hits + 1))
  else
    echo "ok   $label: no hit"
  fi
}

block=$(sed -n '/BEGIN PR TEXT/,/END PR TEXT/p' "$DRAFT")
[ -n "$block" ] || { echo "fork-word-scan: no PR TEXT block in $DRAFT" >&2; exit 2; }
# Each scan reads a here-string or a process substitution, never a pipe: a pipe would run the
# function in a subshell and the hit counter would be lost (the first version exited 0 with hits).
scan "PR TEXT block of $DRAFT ($(printf '%s' "$block" | wc -c | tr -d ' ') B)" yes <<<"$block"

scan "added lines of git diff $BASE $BRANCH" no < <(git diff "$BASE" "$BRANCH" | grep '^+' | grep -v '^+++')

scan "commit messages in $BASE..$BRANCH ($(git rev-list --count "$BASE..$BRANCH") commits)" yes < <(git log "$BASE..$BRANCH" --format='%B')

if [ "$hits" -eq 0 ]; then echo "fork-word-scan: 0 places with a hit"; exit 0; fi
echo "fork-word-scan: $hits place(s) with a hit"; exit 1
