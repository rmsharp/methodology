# PR5 step 1 — the candidate branch is on the fork's origin

Read the answer first, then the checks, then what this does not show.

## The answer

The fork's `origin` now holds `feat/methodology-directory` at `47637be21425e5a5ad3603e85a4a0d4259f8f2e7`: the 33
commits of the local branch `pr2b/candidate`, directly on `upstream/main` `d50ce290d921`. **Nothing was sent to
`KJ5HST/methodology`**: no pull request exists from that branch, #98 and #96 are untouched, and upstream's `main` has
not moved. Step 2 (opening the pull request) and step 3 (answering comments) are not started; each is its own go-ahead.

## What was done, in order

1. **His picks (Phase 0 picker, 2026-10-29):** deliverable 'PR5 step 1: push the candidate (Recommended)'; the trim
   'Yes, trim 4 to 3 (Recommended)'; then, asked separately, the remote name 'feat/methodology-directory (Recommended)'
   (the other offered was the local name `pr2b/candidate`). The name is the one a maintainer sees in the pull request
   header (`rmsharp:feat/methodology-directory` into `KJ5HST:main`); it follows the fork's `feat/<topic>` branches.
2. **Guards, read just before the push** (all printed in this session's terminal; the same checks are now in the script):
   tip `47637be21425`; 33 commits, 0 merges; merge-base equals `upstream/main`'s tip; the name free on `origin`
   (`git ls-remote --heads origin refs/heads/feat/methodology-directory` empty); `origin/main` equal to the local
   `origin/main` (`b063c61a`); all 33 commits authored by the operator (already the fork's public author); a grep of the
   added lines of `d50ce290..47637be2` for GitHub, OpenAI, AWS, Slack and Google key shapes and private-key headers read
   0 hits; there is no pre-push hook (`.githooks` holds `commit-msg` and `pre-commit`).
3. **The push:** `git push origin pr2b/candidate:refs/heads/feat/methodology-directory`. No `-u` (the local branch's
   configuration is unchanged), no force; exit 0, `* [new branch] pr2b/candidate -> feat/methodology-directory`. GitHub
   printed its usual 'Create a pull request' hint; nobody visited it.
4. **The read-back:** `pr5-step1-readback.sh` (read-only; exit 0 only when every check agrees), output in
   `pr5-step1-readback-output.txt`: `origin`'s head equals the local tip; GitHub's own comparison with upstream's `main`
   reads `status=ahead ahead_by=33 behind_by=0 merge_base=d50ce290d921 files=47` (S397 measured 47 files); upstream's
   `main` is `d50ce290d921`; no pull request from that head; open pull requests #98 (`65990cda`, MERGEABLE, CLEAN) and
   #96 (`ad5c980f`, CONFLICTING, DIRTY). A control against a branch name that does not exist printed 6 `FAIL` lines
   and exited 1, so the script can go red.

## What this does not show

- That the pull request will open cleanly: step 2 was not run. The script's 'pull requests from this head: 0' is
  `gh pr list --head <name>`, which matches the branch name only, so a same-named branch from another fork would count
  too (none exists).
- That GitHub shows the same 47 files a reviewer sees after upstream's `main` moves; the comparison is against
  `d50ce290d921` at the time it ran.
- Whether the maintainer wants the name. It can change any time before step 2 by deleting the remote branch
  (`git push origin --delete feat/methodology-directory`) and pushing again; after step 2 the head is fixed.
- No expectations file was saved before this step: one push, no prediction beyond the guards' own outcomes.

## For step 2 (his go-ahead; not started)

Run `bash docs/planning/pr-composition-evidence/pr5-step1-readback.sh d50ce290d921 47637be21425 feat/methodology-directory`
first. If `upstream/main`, #98's head or #96's head moved, the figures in the text are stale: re-verify the branch and
re-run `pr4b-claims.sh` before opening anything. The text is `docs/planning/upstream-pr-body.md`: line 7 is the title
(after `**Title:** `), lines 9 to 105 are the body (21,684 B), lines 1 to 6 are the draft's own header and must not go
into the pull request. Its first body line is `@KJ5HST:`, which notifies him on posting: show the exact command and the
body to the operator and open only on his go-ahead.
