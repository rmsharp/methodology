# PR2b sizing record (S376, 2026-10-26)

**Question.** How much of rebuilding `pr2/candidate` (34 commits over `f34769f3`) on `upstream/main` (`d50ce290`) is textual conflict, and where?
**Method.** [`pr2b-sizing.py`](pr2b-sizing.py), output [`pr2b-sizing-output.txt`](pr2b-sizing-output.txt) (re-run: `python3 docs/planning/pr-composition-evidence/pr2b-sizing.py`, about 10 s; two runs were byte-equal). It applies the 34 commits one at a time, each onto the result of the one before (`git merge-tree --write-tree --merge-base=<commit>^`, the semantics of `git cherry-pick`), in a throwaway bare `--no-local` clone. Nothing is kept, resolved or sent. Git 2.56.0; attributes off (GitHub's view).

## The answer

**4 of the 34 commits stop on a textual conflict (policy B below, the plan's resolution); the other 30 apply with none. Under policy A, 3 stop.** Every stop is in four files: `starter-kit/methodology_trim.py`, `tools/test_methodology_trim.py`, `FRAMEWORK_APPARATUS.md`, `.quality-gates.json`.

| # | Commit | Regions (A / B) | What it is, and what the rebuild does with it |
|---|---|---|---|
| 1 | `bbe0dc35` | 28 / 28 | The lineage commit: trimmer 1.7.0, dashboard 2.21.0, tests. 26 of the 28 regions are the trimmer and its tests, which upstream already merged as #94: candidate's copy to upstream's is +198 / -30 lines of 2,757 (trimmer), +832 / -20 of 4,239 (tests). **Reading:** take upstream's side there; read the two regions in `FRAMEWORK_APPARATUS.md` and `.quality-gates.json`. |
| 5 | `98ca7fc9` | 1 / 3 | The layout hunks (1.8.0): +228 / -92 in the trimmer, +497 / -1 in its tests. **This is the fork's real addition to the trimmer, and the only stop that is new judgment** (reading): onto 1.8.2 it meets one trimmer region (56 lines ours, 14 theirs), one tests region where both sides *add* (806 against 493 lines) and one gates region. |
| 26 | `2276f4ef` | 0 / 7 | The comment scrub of the trimmer and its tests. It conflicts only when upstream's trimmer survives (B). **Reading:** redo it as a scrub pass over the rebuilt files, not a resolution. |
| 34 | `3cba1e50` | 3 / 8 | The 1.8.1 abort-code fix. **Read from both files:** upstream's trimmer already defines `unfinished(` and prints "the proof did not finish"; its 1.8.2 header refines the same exit-3 rule; 5 of this commit's 6 tests are in upstream's test file by name or reworded (`test_a_shard_that_is_there_and_cannot_be_read_is_the_same_abort`). The sixth, a pin that the proof template differs from 1.7.0's only in the abort hunk, has no counterpart, and upstream's 1.8.2 changed the template further (`python3 -I`). **Reading:** superseded; drop it. |

## What was measured, and what only derived

- **Control (measured).** One merge of the whole candidate against `upstream/main` reads **46 regions in 4 files**, S375's figure, so this counting agrees with the earlier instrument.
- **Prediction (derived first, then checked).** A commit can stop only if it touches a file upstream changed since the base (8 files; 17 of the 34 commits touch one). It held: every stopper is among the 17. Fourteen of the 17 did not stop under A, thirteen under B.
- **Two ways to go on past a conflict**, because the choice changes what later commits meet. A: the commit's side wins (the candidate's old trimmer survives): 3 commits stop (1, 5, 34), **32 regions**. B: upstream's side wins (the plan's resolution, "upstream's 1.8.2 plus the fork's layout hunks"): 4 commits stop (1, 5, 26, 34), **46 regions**, equal to the control. The real cost is a person reading each region and lies between the two. Neither is a resolution.
- **A region is a unit of the marker style.** The default style (46) and `zdiff3` (17 for the same control) cut one clash differently. The `zdiff3` view is used only to tell a collision of two *additions at one spot* (empty base: 9 of 17 in the control, 7 in each stacked run) from two changes to the same lines. An empty base is not "keep both": in commit 1 the two additions are near-copies of one lineage, and keeping both would double a definition.

## What this does not show

1. **Applying with no conflict is not green.** Each layer still needs the PR2 row's clean-clone checks (the suite, `quality_ratchet.py --run`, `bin/check-links --layout both`, `bin/check-layout-literals`, the shard-proof histogram). None was run. Most of PR2b's time probably lies there, and it was not measured.
2. **"Two to three sessions" is still a guess.** What changed is that the conflict surface is known: 4 commits, 4 files, one of them (5) new judgment.
3. **The gate numbers move.** Commits 1 and 34 touch `.quality-gates.json`; the trimmer-test count there must be re-derived on the rebuilt tree (tighten only).
4. **Surface.** A bare clone on this machine with attributes off. The maintainer merges locally with upstream's attributes; the candidate changes no ledger, so it does not matter for these four files. It cannot show test results.

## An order the rebuild could take (derived from the table, an estimate)

Branch from `d50ce290` (keep `pr2/candidate`). Commit 1 with the trimmer and its tests taken from upstream; commits 2 to 4; commit 5 resolved by reading (the session's real work); commits 6 to 25 and 27 to 33 as they apply, each layer checked in a clean clone; the scrub of commit 26 re-run over the rebuilt trimmer and tests; commit 34 dropped. One layer per session, a claim first.
