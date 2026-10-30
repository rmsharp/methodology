# PR5 step 2 — the pull request is open on KJ5HST/methodology

Read the answer first, then the checks, then what this does not show.

## The answer

**Pull request #99 is open** at https://github.com/KJ5HST/methodology/pull/99, from `rmsharp:feat/methodology-directory`
(`47637be21425`, 33 commits directly on `upstream/main` `d50ce290d921`) into `KJ5HST:main`. State OPEN, not a draft,
MERGEABLE / CLEAN, 47 files, +18,367 / -1,098 (the figures the text states), 0 comments and 0 reviews when read back.
Its title and body are the text he approved (draft 12), lines 7 and 9 to 105 of `docs/planning/upstream-pr-body.md`,
plus one line at the end (see 2). Step 3 (answering comments) is not started and is its own go-ahead.

## What was done, in order

1. **His picks (Phase 0 picker, 2026-10-30):** deliverable 'PR5 step 2: open the PR (Recommended)'; the trim 'Yes, trim 4
   to 3 (Recommended)'. Then, after the exact command, title and body were shown: **'Yes, open it as shown
   (Recommended)'** (the others offered were 'Yes, but without the added line', 'Show me the whole body here first' and
   'No, not now').
2. **The text.** Title: line 7 without `**Title:** ` (104 B). Body: lines 9 to 105 byte for byte (21,684 B), then a blank
   line and `🤖 Generated with [Claude Code](https://claude.com/claude-code)` (67 B), 21,751 B in all. The last line is the
   one addition, made because the harness this session runs under asks that a pull request description end with it; it
   was shown to him as the only change to his approved text, with the option to leave it off.
3. **Checks before opening:** `pr4-body-check.py docs/planning/upstream-pr-body.md pr2b/candidate upstream/main` exit 0,
   its output equal to `pr4b-body-check-output.txt` once hashes are removed; `gh auth status` logged in as `rmsharp`
   (scopes `repo`, `workflow`); `KJ5HST/methodology` default branch `main`, no `.github` directory or pull request
   template on `upstream/main`; the account's permission there reads WRITE (not used: the pull request comes from the
   fork's branch).
4. **Guards, one script, immediately before the command** (it opened the pull request only if all held): the step-1
   read-back `pr5-step1-readback.sh d50ce290d921 47637be21425 feat/methodology-directory` exit 0; `upstream/main`
   `d50ce290d921`; #98's head `65990cda`; #96's head `ad5c980f`; 0 pull requests (any state) from the head; the body file
   equal to lines 9 to 105. All held, and the script printed 'ALL GUARDS GREEN -- opening'.
5. **The command:** `gh pr create -R KJ5HST/methodology --base main --head rmsharp:feat/methodology-directory --title
   "$(cat <title file>)" --body-file <body file>`. Exit 0, URL `https://github.com/KJ5HST/methodology/pull/99`.
6. **The read-back:** `pr5-step2-readback.sh 99 d50ce290d921 47637be21425 feat/methodology-directory` (read-only; exit 0
   only when every check agrees), output in `pr5-step2-readback-output.txt`: state, base, head owner and branch, head
   commit, 33 commits, 47 files, lines added and removed (each recomputed from `git diff` against upstream), the title,
   and the body (21,750 B and the same SHA-256 prefix `849ddf357ec3` as the text rebuilt from the draft); `origin`'s
   branch still equals the candidate; `upstream/main` unchanged. **A control** with a wrong candidate and a branch that
   does not exist printed 7 `FAIL` lines and exited 1, so the script can go red.

## What this does not show

- **How the maintainer will answer.** 0 comments and 0 reviews is one read, taken minutes after posting.
- **That the merge state stays clean.** MERGEABLE / CLEAN is true against `d50ce290d921` now. If #98 merges first, the text
  already says what happens (decision 3: conflicts in 3 files and 5 regions against #98's current head).
- **The body's trailing newline:** the script compares the two texts after the shell strips trailing newlines (21,750 B on
  both sides). By hand, right after opening, `gh api repos/KJ5HST/methodology/pulls/99 -q .body` wrote 21,752 B, which is
  GitHub's body plus the one newline `-q` appends, so GitHub holds the file's 21,751 B; that hand check is not in the script.
- **Whether the maintainer wants the branch name, the footer line or the 27 cherry-pick lines.** All three are visible to
  him now; the text asks about the lines (decision 4).

## For step 3 (his go-ahead; not started)

Read first: `gh pr view 99 -R KJ5HST/methodology --json state,mergeable,mergeStateStatus,comments,reviews` and the same for 98
and 96; then `bash docs/planning/pr-composition-evidence/pr5-step2-readback.sh 99 d50ce290d921 47637be21425 feat/methodology-directory`.
On a reply, read it in full, show the reply text inline, post only on his go-ahead. **Pushing to `feat/methodology-directory`
now changes #99** (every push updates it), so any rebase on #98 or any dropped commit is an outward act with its own
go-ahead. To withdraw: `gh pr close 99 -R KJ5HST/methodology` (also an outward act; the branch and the commits stay).
