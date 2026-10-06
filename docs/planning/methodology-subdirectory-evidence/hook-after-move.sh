#!/usr/bin/env bash
# What does THIS repository's .githooks/pre-commit (the reference ledger gate) do once the ledger has
# moved to methodology/CHANGELOG.md?  Two throwaway clones of the current HEAD, hooks ON
# (core.hooksPath .githooks), nothing in the real repo touched.
#   X1  the move commit itself: `git mv CHANGELOG.md methodology/CHANGELOG.md`, committed with the
#       hook on. Refused, or passed?
#   X2  a LATER commit that changes tracked content and does not touch the ledger, after the move
#       (the move having been committed with --no-verify to set the state up). Refused, or passed?
#       Passed means the ledger gate no longer binds: it fails OPEN, silently (BL-77's failure mode).
#   C   control: the same later commit in an UNMOVED clone. It must be refused.
# Run from the repo root:   bash docs/planning/methodology-subdirectory-evidence/hook-after-move.sh
set -u
# The disclosure hook (.githooks/commit-msg) refuses a commit without a Co-Authored-By trailer when an
# agent harness is detected. It is not what is being measured, so it is switched off for this script.
export METHODOLOGY_REQUIRE_COAUTHOR=0
SRC="$(git rev-parse --show-toplevel)" || exit 3
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
mk() {
  git clone -q --no-local "$SRC" "$1"
  git -C "$1" config core.hooksPath .githooks
  git -C "$1" config user.email t@t; git -C "$1" config user.name t; git -C "$1" config commit.gpgsign false
}
later() {  # a content change that does not touch the ledger
  printf '\nx\n' >> "$1/docs/planning/BACKLOG.md"; git -C "$1" add docs/planning/BACKLOG.md
  git -C "$1" commit -q -m later >/dev/null 2>"$2"; echo $?
}
mk "$T/c"
printf 'C  control, unmoved ledger, later commit: exit=%s (expect nonzero: refused)\n' "$(later "$T/c" "$T/c.err")"
head -2 "$T/c.err" | sed 's/^/     /'

mk "$T/x1"; mkdir "$T/x1/methodology"; git -C "$T/x1" mv CHANGELOG.md methodology/CHANGELOG.md
git -C "$T/x1" commit -q -m move >/dev/null 2>"$T/x1.err"; rc=$?
printf 'X1 the move commit itself, hook on: exit=%s (0 = passed, nonzero = refused)\n' "$rc"
head -2 "$T/x1.err" | sed 's/^/     /'

mk "$T/x2"; mkdir "$T/x2/methodology"; git -C "$T/x2" mv CHANGELOG.md methodology/CHANGELOG.md
git -C "$T/x2" commit -q --no-verify -m move
printf 'X2 later commit after the move, hook on: exit=%s (0 = PASSED: the ledger gate fails open)\n' "$(later "$T/x2" "$T/x2.err")"
head -2 "$T/x2.err" | sed 's/^/     /'
