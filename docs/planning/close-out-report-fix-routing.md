# How the `close_out_report.py` fix reaches upstream — a routing recommendation

**Status:** recommendation (2026-11-07); **the operator chose R1 at the close-out picker the same day**
(section 8). **Nothing here has been sent to
`KJ5HST/methodology`**; every outward step below needs his own go-ahead, each time, and each text is shown
to him first. All figures were measured on 2026-11-07 in scratch worktrees (they vanish; the commands are
given so a later session can re-measure).

## 1. What is being decided

`starter-kit/close_out_report.py` is the tool that prints and checks the Phase 3G close-out report (the
last message a session gives the operator). It exists upstream only inside open pull request **#96**
(head `ad5c980f`, version 1.1.0, open since 2026-10-20, 0 comments, 0 reviews). It is not in
`upstream/main` (`d50ce290`), not in the sync manifest and not in the runner there (checked: 0 hits).

An adopter project found two defects in it. **Both are in lines #96 adds.** The fork already has the fix
(version 1.2.1, commit `29bac609`). The decision is where that fix goes upstream.

## 2. The defects, reproduced on #96's tool (v1.1.0)

Each row is a scratch git repository holding a different `HANDOFFS.md`; "seed" means the file
`starter-kit/HANDOFFS.md` that every adopter receives, whose Format section shows an example receipt
inside a four-backtick fence. "Hook" means the Stop-hook mode (`--hook`) that blocks a session ending without
the report. Outputs are as printed.

| # | Ledger | #96 tool (v1.1.0) | with the fix (1.2.1) |
|---|---|---|---|
| 1 | seed + one real complete receipt (S2) below it | `refused: newest receipt (S<N>) is <pending \| complete>, not complete: write the close-out receipt first`, exit 2 | report printed, exit 0 |
| 2 | one Session 1 receipt, no `predecessor_score` (as the seed tells Session 1), no seed text | `refused: newest receipt has no numeric predecessor_score`, exit 2 | report printed, "n/a, first session", exit 0 |
| 3 | Stop hook: session starts on the bare seed, a complete receipt is written during it, the session ends with "All done, bye." | allows the stop, prints **nothing** | blocks, names the missing report lines |

`bin/check-handoff` (the structural checker) passes the ledger of row 1. The tool and the checker read the
same file with different fence rules. Cause 1 is `_FENCE` (`close_out_report.py:39` at `ad5c980f`), one
flat regex that counts the example as the newest receipt; cause 2 is the numeric-score test (`:80-82`).
On this tool a seed plus a Session 1 receipt fails on cause 1 first, so row 2 leaves the seed text out to
show cause 2 alone. Rows 1 and 3 are the adopter's own seed cases; row 2 is its Session 1 case.

## 3. Where each place stands

| Place | Has the tool? | Has the fix? |
|---|---|---|
| `upstream/main` `d50ce290` | no | no |
| PR #96 `ad5c980f` | yes, 1.1.0 (936 added lines in 9 files) | no |
| PR #99 `47637be2` (the `methodology/` directory move) | **no** (0 files named `close_out_report` in its tree) | no |
| the fork | yes, 1.2.1 (1.2.0 added the layout resolver, 1.2.1 is the fix) | yes |

Adopters of the fork get 1.2.1 by `bin/sync`; that is a separate path from upstream and is unaffected.

## 4. The routes

**R1 — one added commit on #96's branch.** The fix does not apply as it stands: `git apply --3way` of
`29bac609`'s two code files conflicts in both: the tool at the version line, where the fork's 1.2.0
resolver block sits beside it, and the tests at the end of the file, where the new test classes land.
Resolved by hand in a scratch worktree at `ad5c980f`:

- the tool takes the fix without the resolver: version 1.1.1, **+56 −16 lines**;
- the tests: **+233 −8 lines**, 21 tests, three hunks adapted by hand (an import; the test that reads the
  repository's own receipts, which is written for upstream's receipts; the two new test classes). One
  assertion expected three real ledger files and upstream's tree has two, so it became "at least two";
- the gate `close-out-report-unit-tests` floor rises 68 → 89 (a tightening);
- **result: 89 tests pass on #96's own tree, and 89 pass with the fixed files copied into a merge of #96
  into `upstream/main`** (that merge was clean). `bin/tests.sh` counts the whole unit suite as one pass
  (`bin/tests.sh:267`), so the shell suite's total is unchanged. The full shell suite was **not** run.
- #96 would grow from 936 to about 1,200 added lines (936 − 24 it replaces + 289). The two original
  commits keep their hashes (a plain push, no force); #96 allows maintainer edits.
- Two added lines name the adopter project and a path that exists only in that project
  (`docs/upstream/close_out_report-receipt-parsing.md`); they must be reworded before any push.

**R2 — into #99. Not workable.** #99's tree has no `close_out_report` file, so carrying the fix there
means carrying the whole tool, which is #96's content, into a pull request whose purpose is the directory
move, and it would then collide with #96.

**R3 — an issue upstream.** The adopter's report (`claude_work/docs/upstream/close_out_report-receipt-parsing.md`,
6,969 B, outside this repository) is well made but describes the fork: "v1.2.0", `bin/_manifest.py:68` and
`:72`, `SESSION_RUNNER.md:298`, a synced tag. Upstream has none of those (checked). It would need
rewriting against #96's lines, and it would be an issue about code that is not merged, which is what a
comment on the pull request is for. It also adds one more item to a list the maintainer has not
answered (no maintainer reply on any of #93, #95, #97, #100, #101) while leaving #96 as it is.

**R0 — hold on the fork (his earlier choice for the manifest follow-up, not for this fix).** Nothing goes
out. If #96 is merged as written, the defects ship to every adopter who copies the tool, and the fix
becomes a second pull request after it (1.1.1).

## 5. Recommendation: R1

It is the only route that makes upstream correct on its first merge, adds no new item to the maintainer's
queue, and touches nothing he has reviewed (0 reviews). The defects are in #96's own lines, so the fix
belongs in #96. R2 cannot be done; R3 spends more of his attention for less. **R0 is the sensible choice if
you would rather not change a pull request that has had no response**; nothing is lost by waiting except
that #96 stays defective.

Not verified, and to be before anything is pushed: the full `bin/tests.sh` and `quality_ratchet.py --run`
on the real commit; that the fork's next resync conflict set is unchanged (inference: the tool and its
tests already conflict add/add, so editing them adds no new file to the set); how the maintainer will
receive a larger #96.

## 6. If you choose R1 — steps, each its own session and go-ahead

1. **Build** the commit on the local branch `feat/close-out-report-tool` (at `ad5c980f`): the two code
   files, the gate floor, one changelog entry; reword the two adopter-naming lines. DONE: unit suite 89/89
   on that branch **and** on its merge into `upstream/main`; `bin/tests.sh` and the gate run green on both;
   the added lines scanned for fork words (`BL-`, session numbers, "the fork", the adopter's name).
   Surface: scratch worktrees and local hooks; it cannot show GitHub's mergeability label (#96 reads
   CONFLICTING from the changelog union-merge gap alone) or the maintainer's judgment. Shown to you; not pushed.
2. **Push** the commit to `origin/feat/close-out-report-tool` (this is what updates #96). DONE: `git ls-remote`
   reads the pushed sha; the PR's head equals it.
3. **Comment** on #96 with the text below, read back byte for byte.

## 7. Outward text (drafts; the comment's figures re-measured 2026-11-08, nothing posted)

**Commit message.**

```
fix(close-out): close_out_report.py 1.1.1 reads the shipped HANDOFFS.md seed the way bin/check-handoff does

Two defects, both visible in any project whose HANDOFFS.md came from
starter-kit/HANDOFFS.md.

1. The receipt scanner was one flat regex, so the seed's four-backtick Format
   example counted as the newest receipt. The report command refused ("newest
   receipt (S<N>) is <pending | complete>") however complete the real newest
   receipt was, and the --hook check allowed every Stop without saying so.
   parse_receipts now follows bin/check-handoff's block rule: a fenced region
   opened by anything but ```handoff is skipped whole.
2. The seed tells Session 1 to leave predecessor_score out, and the tool refused
   a newest receipt without one. Session 1 now prints "n/a, first session" and
   the lint accepts that line.

21 tests added (68 to 89): the tool and the hook run on the real seed, Session 1,
and a parity test that fails on the first ledger where the tool and
bin/check-handoff disagree about what the receipts are. The gate floor for
close-out-report-unit-tests rises 68 to 89.
```

**Comment on #96.**

> While running this tool in a project whose `HANDOFFS.md` came from the `starter-kit` seed I found two
> defects in the code this pull request adds, and pushed one commit on top of `ad5c980f` to fix them (the
> two original commits are unchanged).
>
> 1. The seed wraps its Format example in a four-backtick fence; `_FENCE` is one flat regex, so the example
>    counts as the newest receipt. `python3 starter-kit/close_out_report.py` refuses
>    (`refused: newest receipt (S<N>) is <pending | complete>, not complete: write the close-out receipt first`,
>    exit 2) however complete the real newest receipt is, and `--hook` allows every Stop without saying so.
>    `bin/check-handoff` reads the same file correctly.
> 2. Session 1 has no `predecessor_score` (the seed says to omit it) and the tool refuses it
>    (`refused: newest receipt has no numeric predecessor_score`).
>
> The commit: `starter-kit/close_out_report.py` +56 −16 (1.1.0 → 1.1.1), `tools/test_close_out_report.py`
> +233 −8 (the suite goes from 68 to 89 tests), the `close-out-report-unit-tests` gate floor 68 → 89.
> Measured on the new head `b4af3293` and on a merge of it into `main` (`d50ce290`), which is clean:
> `python3 tools/test_close_out_report.py` 89 tests, OK; `bash bin/tests.sh` 262 passed, 0 failed;
> `python3 starter-kit/quality_ratchet.py --run` 13/13 gates pass.
>
> To reproduce on `ad5c980f`: in a scratch git repository, save `starter-kit/HANDOFFS.md` as `HANDOFFS.md`,
> add one complete receipt below its Format section, commit, and from that directory run
> `python3 <path>/close_out_report.py --deliverable D --outcome done --well W --badly B --predecessor P --next N`.
> It reads `./HANDOFFS.md` (`--ledger`; `--cwd` only names the repository whose HEAD the report cites).
> At `ad5c980f` it prints the refusal above; at `b4af3293` it prints the report.

*Measured 2026-11-08, serially, in scratch trees (gone): unit suite 89 tests OK on `b4af3293` and on its
merge into `d50ce290` (68 on `ad5c980f`; 21 new test ids, 0 removed); `bin/tests.sh` 262 passed, 0 failed on
both; gates 13/13 on both (branch results `571d09d34c3d`, manifest `e6210da5d324`; merge `51c1b61c0c41`,
`8aac22368a80`); the three symptoms of section 2 re-run against the pushed 1.1.1 tool, not the fork's 1.2.1.*

## 8. Decisions for the operator

1. **Route: decided, R1** (2026-11-07, at the close-out picker, with both drafts in section 7 shown to
   him first). R0 and R3 were offered and not chosen; R2 is not workable. This records the route only:
   building the commit (section 6, step 1), pushing it, and posting the comment are each a later step
   needing his separate go-ahead.
2. **Decided** (2026-11-09, at the close-out picker, with the text shown to him in full first): the comment
   **as drafted** (section 7). **Posted** 2026-11-09 (S434), at his separate go-ahead ('post it as drafted',
   given after the text was shown to him inline): comment 6745597446 on #96
   (`https://github.com/KJ5HST/methodology/pull/96#issuecomment-6745597446`), read back from the API equal to
   the text byte for byte (1,821 B). `b4af3293` and `d50ce290`, which the text names, were re-checked live
   immediately before and had not moved. Step 3 of section 6 is done; a reply on #96 is his to read first.
