#!/usr/bin/env bash
# Two git behaviours the plan relies on, measured in throwaway repos (nothing here touches a real one).
#   E1  a methodology/.gitattributes carrying `CHANGELOG.md merge=union` merges two ledger edits
#       cleanly; the same merge with no attributes file conflicts (the control).
#   E2  after `git mv CHANGELOG.md methodology/CHANGELOG.md`, a plain `git log -- <new path>` stops at
#       the move; `git log --follow` reaches the older commits; the OLD path still answers in full.
# Run:  bash git-behaviour.sh
set -u
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
mk() { git init -q -b main "$1"; git -C "$1" config user.email t@t; git -C "$1" config user.name t; git -C "$1" config commit.gpgsign false; }

mk "$T/e1"; cd "$T/e1" || exit 3
mkdir methodology
printf 'CHANGELOG.md merge=union\n*.jsonl merge=union\n' > methodology/.gitattributes
printf '# ledger\n\nbase\n' > methodology/CHANGELOG.md
git add -A; git commit -q -m base
git checkout -q -b a; printf '# ledger\n\nA entry\nbase\n' > methodology/CHANGELOG.md; git commit -qam a
git checkout -q main; git checkout -q -b b; printf '# ledger\n\nB entry\nbase\n' > methodology/CHANGELOG.md; git commit -qam b
git merge -q a -m merge >/dev/null 2>&1; printf 'E1 nested attributes: merge exit=%s (0 = clean union)\n' "$?"

mk "$T/e1c"; cd "$T/e1c" || exit 3
mkdir methodology; printf '# ledger\n\nbase\n' > methodology/CHANGELOG.md; git add -A; git commit -q -m base
git checkout -q -b a; printf '# ledger\n\nA entry\nbase\n' > methodology/CHANGELOG.md; git commit -qam a
git checkout -q main; git checkout -q -b b; printf '# ledger\n\nB entry\nbase\n' > methodology/CHANGELOG.md; git commit -qam b
git merge -q a -m merge >/dev/null 2>&1; printf 'E1 control, no attributes: merge exit=%s (1 = conflict)\n' "$?"

mk "$T/e2"; cd "$T/e2" || exit 3
printf '# ledger\n\none\n' > CHANGELOG.md; git add -A; git commit -q -m c1
printf '# ledger\n\ntwo\none\n' > CHANGELOG.md; git commit -qam c2
mkdir methodology; git mv CHANGELOG.md methodology/CHANGELOG.md; git commit -qm move
printf '# ledger\n\nthree\ntwo\none\n' > methodology/CHANGELOG.md; git commit -qam c3
printf 'E2 plain log, new path : %s\n' "$(git log --format=%s -- methodology/CHANGELOG.md | tr '\n' ' ')"
printf 'E2 --follow, new path  : %s\n' "$(git log --follow --format=%s -- methodology/CHANGELOG.md | tr '\n' ' ')"
printf 'E2 plain log, old path : %s\n' "$(git log --format=%s -- CHANGELOG.md | tr '\n' ' ')"
printf 'E2 frontier (git log -1 -- new path): %s\n' "$(git log -1 --format=%s -- methodology/CHANGELOG.md)"
