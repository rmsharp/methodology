# The draft comment on upstream issue #95: what it rests on and what it leaves out (S329, 2026-10-15)

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

`measure_file` exists upstream (`starter-kit/context_budget.py:342`). The draft names no adopter project, no session number, no backlog or plan code, and no path that exists only on the fork; `grep` of it for those
found nothing.

## 2. Left out on purpose (his to add)

- **The new-layout finding** (`i95-record.md` §3.3: a fresh `bin/sync --layout new` leaves `SESSION_NOTES.md` unmeasured). Upstream's `bin/sync` has no `--layout` flag, so the finding is about code he has not been
  sent; saying it would preview the pull request in a comment on a different issue. If he wants it, one sentence: the pass-control should be run in the layout the seed config's paths name, because a layout that
  installs the files elsewhere makes it pass with nothing measured.
- **The side reading** that three projects already have 39 to 44 lines over the cap they declare (`i95-comment-adopters-output.txt`): a remark about the cap's value, not about the fix.
- **The merge results** (`i95-compose-output.txt`): they describe the pull request candidate, which he has not been sent.
- **Project names.** One of the 12 is a private person's project; the draft gives counts only.

## 3. Choices inside the draft that are his

1. **The offer** (last paragraph). It commits him to a pull request if the maintainer says yes. `i95-record.md` §6 recommends R1 and R2 only if asked, so the offer is worded as "say so and I will".
2. **The lean** in item 1 (treat a still-placeholder purpose as unmeasured). It follows from the 800-versus-799 measurement; it is an opinion and is worded as one.
3. **The footer.** Earlier replies to upstream carry it (`docs/planning/pr80-reply-f1.md`); KJ5HST removed it from his own issue body at 23:54Z, which may or may not be a preference. Delete the last line to post without it.
4. **"12 projects of mine"** is his voice; the 12 are the projects `i95-adopters.py` reads (`pr3-adopters.py`'s list).

## 4. What none of it shows

His actual fix (his may touch other regions), the full suite on any patched tree (none was patched), Windows, `--source github`, and any project that is not his. The 12-project figure is as of 2026-10-16T02:05Z; a project's
next commit can move it (three moved between S328's run and this one, none changed the totals).
