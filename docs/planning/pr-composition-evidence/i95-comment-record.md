# The draft comment on upstream issue #95: what it rests on and what it leaves out (S329, 2026-10-15; refreshed S405, 2026-10-30; recomposed S406, 2026-10-31)

**Recomposed at S406 (2026-10-31).** He found the S405 text hard to follow ("I find this text hard to understand. Clarify"). The facts are the same; the text is recomposed: the result comes first, his four findings are always "your finding N" and this comment's three points are A, B and C (the S405 text numbered its own points 1 to 3 beside his findings 3 and 4), each term (minimum, fence, marker, unmeasured) is explained where it first appears, and the script moved to the end. Re-checking every statement for the rewrite found three errors in the S405 text, now fixed: (1) "799 bytes is over" is wrong, the minimum is 800 so 799 is **under** (his correction; S405's `CHANGELOG.md` and `HANDOFFS.md` entries say "799 over" too, where it is true as the tool's status word, `over` being a failing row, but the same words in the outward comment read as a size claim; those two are append-only history and are not edited, S406's entries say so); (2) it put the config line in the second commit, but it is in the first (`cadb4780`; the record's own S405 row said the second); (3) it called the first way out "not over budget" and credited it to his "alternatively", but his wording is "UNMEASURED". The config key is also now described as it is, a marker string (`<project-name>`) that the placeholder contains, not the placeholder text. The text grew from 4,658 B to 5,423 B. The statements re-run for it are the rows of §1 marked (S406).

**Refreshed at S405 (2026-10-30).** The S329 text was written before the fix existed. S404 built it on this tree, so the draft now says what the change does (the new statements are the last rows of §1, from
`i95-comment-refresh.py` and its saved output), its lean in item 1 became the choice that was built, and its closing offer describes the two commits. Nothing else in the text changed except a clause
saying the four files are unchanged on upstream's `main` today (`git diff f34769f..upstream/main` on them is empty at `d50ce290`; the issue is still open with 0 comments, last edited 2026-10-15T23:54:35Z).

The draft is `i95-comment-draft.md`: the exact text, nothing else, so it can be pasted. **It is not posted.** Posting a comment on `KJ5HST/methodology` is his explicit go-ahead,
each time. The issue is <https://github.com/KJ5HST/methodology/issues/95>; it is the maintainer's own, opened 2026-10-15 21:00Z. Its body was edited at 23:54:35Z the same day; the diff
(`gh api graphql`, `userContentEdits`) removes the "Generated with Claude Code" footer and nothing else, so the derivation in `i95-record.md` still stands. The route is R1 of
`i95-record.md` §6, his S328 pick.

## 1. What each statement rests on

| The draft says | Evidence | Where |
|---|---|---|
| all four findings reproduce on `f34769f`; the control passes | the issue's two repros and its control, run with the tool upstream ships | `i95-dayzero-output.txt:6-21` (the upstream block: seed line 5 at `:6`, cases `notes` `:7`, `template` `:13`, `control` `:18`), saved at S328 on the same pinned blobs |
| the placeholder is 182 characters and 182 bytes; fenced alone it exits 2 with "only 182 B" | case `fenced`; the repro block in the draft, run verbatim against an export of `f34769f` (exit 2, same message) | `i95-comment-check-output.txt`, `fenced` row |
| 800 passes and 799 does not; 618 more characters than the placeholder | cases `at-800`, `at-799` | `i95-comment-check-output.txt` |
| `:452` records `len(body.encode())`, `:453` compares `len(body.strip())`, `:455` prints it with "B", `:384` is the line cap | the source lines, printed from the export | `i95-comment-check-output.txt`, "source lines" |
| 300 Chinese characters are 900 bytes and are refused as "only 300 B" | case `cjk-300`; the draft's `export BODY=...` variant, run verbatim | `i95-comment-check-output.txt` |
| 10 of 12 projects declare `max_line_bytes`, all on `SESSION_NOTES.md`; 0 lines flip; the tool's `measure_file` agrees on every file | `i95-adopters.py`, run a second time because three projects had committed since the first | `i95-comment-adopters-output.txt` (totals line), `i95-adopters-output.txt` (the first run, equal totals) |
| the two counts (raw bytes, `len(l.encode())`) are equal on all 10 files | the `bytes` and `encode` columns | `i95-comment-adopters-output.txt` |
| (S405) the adopter figure still holds | `i95-adopters.py` run again at the projects' current commits: the same totals line (10 of 12, 0 lines flip, `measure_file` agrees) | `i95-comment-adopters-output-2.txt` (totals line) |
| (S405) the four files involved are unchanged on `main` today | `git diff f34769f..upstream/main` on `context_budget.py`, `context-budget.json`, `CLAUDE_TEMPLATE.md`, `SESSION_NOTES.md`: 0 lines, at `upstream/main` `d50ce290` | read at S405's claim; re-run before posting |
| (S405) with the change, a fresh `bin/sync` plus the template as `CLAUDE.md` exits 1, no row over, the one finding the placeholder warning, `SESSION_NOTES.md` ok, `LEARNINGS.md` unmeasured | case `fork-day-zero` (real `bin/sync --layout legacy` into an empty git project); the issue's two repros on this tree's seeds give exit 1 and exit 1 against upstream's exit 2 and exit 2 | `i95-comment-refresh-output.txt` (`up-notes`, `up-template`, `fork-notes`, `fork-template`, `fork-day-zero`) |
| (S405) the placeholder row reads `warn`, keeps its size, and the 800 floor is not applied while it stands; after it is replaced 799 bytes is under the minimum (the row reads `over`, the tool's word for a failing row) and 800 passes; 300 CJK characters (900 bytes) pass | cases `fork-template` / `fork-day-zero` (`CLAUDE.md=warn`, kinds `placeholder` only, no `protected`), `floor-799`, `floor-800`, `floor-cjk-300`; the row's size (3,438 B) is in the tool's table, seen by running the tool without `--json` on the same project | `i95-comment-refresh-output.txt`; the size is not saved there |
| (S405) the change is two commits; the first holds the tool, the config line and its tests, the second the seeds and the `bin/tests.sh` test with a control (S405 wrote "the second holds ... the config line"; corrected at S406) | `cadb4780` (tool, config line, 8 tests) and `19a4ecb8` (the two seeds, Test 35 with its paired control, 3 tests); the commit order is the reverse of the S329 draft's, because Test 35 asserts the warning the tool commit adds | `git show --stat` of each; `CHANGELOG.md` entries 'S404 work (1 of 2)' and '(2 of 2)' |
| (S406) the config names a marker string that the template's placeholder contains (`protected_placeholder`, `<project-name>`); while the fenced block contains it the row is `warn` with the remedy "Write your purpose", otherwise the 800 floor applies | `git show cadb4780 -- starter-kit/context-budget.json` (the key and its note); `starter-kit/context_budget.py:555-562` (`marker in body` raises the `placeholder` finding and `warn`; the `elif` at `:562` is the floor) and `:682` (the remedy title); the template's fenced sentence is 92 bytes and contains `<project-name>` | read at S406 on this tree |
| (S406) the second commit's seed edits: `SESSION_NOTES.md` line 5 wrapped and a `## Session History` heading added; `CLAUDE_TEMPLATE.md` has the fence around the Purpose placeholder | `git show 19a4ecb8 -- starter-kit/SESSION_NOTES.md starter-kit/CLAUDE_TEMPLATE.md` | read at S406 |
| (S406) the test: syncs into a temporary project (`--layout legacy`), copies the template to `CLAUDE.md`, asserts no row over and the one finding the placeholder warning; the paired control plants a 400-byte line in the seed `SESSION_NOTES.md` and expects `over=1 kinds=line_bytes,placeholder` | `git show 19a4ecb8 -- bin/tests.sh` (Test 35's day-zero block) | read at S406 |
| (S406) "unmeasured" is the status the tool already uses for a file it cannot measure | `starter-kit/context_budget.py` at `f34769f`, `:343` (`status ∈ ok \| warn \| over \| unmeasured`), `:351` and `:356` | `git show f34769f:starter-kit/context_budget.py` |
| (S406) every figure re-run for the rewrite still holds | `i95-comment-refresh.py` re-run at S406 (its 8 case lines identical to `i95-comment-refresh-output.txt`); `i95-adopters.py` re-run (totals line identical to `i95-comment-adopters-output-2.txt`; the `bytes` and `encode` columns equal on all 10 files, 0 flips); `git diff f34769f upstream/main` on the four files: 0 lines at `d50ce290` | no new output file (the outputs equal the saved ones); `i95-comment-adopters-output-2.txt`, `i95-comment-refresh-output.txt` |

`measure_file` exists upstream (`starter-kit/context_budget.py:342`). The draft names no adopter project, no session number, no backlog or plan code, and no path that exists only on the fork; `grep` of it for those
found nothing.

## 2. Left out on purpose (his to add)

- **The new-layout finding** (`i95-record.md` §3.3: a fresh `bin/sync --layout new` leaves `SESSION_NOTES.md` unmeasured). Upstream's `bin/sync` has no `--layout` flag, so the finding is about code he has not been
  sent; saying it would preview the pull request in a comment on a different issue. If he wants it, one sentence: the pass-control should be run in the layout the seed config's paths name, because a layout that
  installs the files elsewhere makes it pass with nothing measured.
- **The side reading** that three projects already have 39 to 44 lines over the cap they declare (`i95-comment-adopters-output.txt`): a remark about the cap's value, not about the fix. At S405's re-run the
  figures moved (`i95-comment-adopters-output-2.txt`): the same two projects with 64 and 44 lines over, a third at 7 (its notes file was trimmed), and two with 1 each; the totals line did not change.
- **The merge results** (`i95-compose-output.txt`): they describe the pull request candidate, which he has not been sent.
- **Project names.** One of the 12 is a private person's project; the draft gives counts only.

## 3. Choices inside the draft that are his

1. **The offer** (last paragraph). It commits him to a pull request if the maintainer says yes. `i95-record.md` §6 recommends R1 and R2 only if asked, so the offer is worded as "say so and I will". Since S405 it
   also says the change is built, and that it has been run on his own copy, not on the maintainer's `main` (see §4); delete that sentence to say less.
2. **The design choice** in point A (a still-placeholder purpose is a `warn` that keeps its size, not "unmeasured", not a placeholder padded to 800). Until S405 this was a lean ("I lean towards the first"); it is now
   what was built (S404's choice A at its Present gate), stated with the reason the measurement gives, and left to the maintainer in the last sentence of point A.
3. **The footer.** Earlier replies to upstream carry it (`docs/planning/pr80-reply-f1.md`); KJ5HST removed it from his own issue body at 23:54Z, which may or may not be a preference. Delete the last line to post without it.
4. **"12 projects of mine"** is his voice; the 12 are the projects `i95-adopters.py` reads (`pr3-adopters.py`'s list).

## 4. What none of it shows

His actual fix (his may touch other regions), **the change applied to upstream's `main`** (S404 built and tested it on this tree: `bash bin/tests.sh` 694 passed, 0 failed in a clean clone, 174 tests in
`tools/test_context_budget.py`; this tree's `context_budget.py` carries other changes, so the draft says it was run "on my own copy" and would be re-run on his `main`), Windows, `--source github`, and any project that
is not his. The 12-project figure is as of S405's re-run (2026-10-30); a project's next commit can move the per-file counts (they moved between S329 and S405, the totals did not).
