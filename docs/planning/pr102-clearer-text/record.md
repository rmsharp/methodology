# Upstream pull request #102: a clearer title and body (BL-132)

**Status: DRAFT. Nothing on #102 was changed.** The pull request is still at head `c93f1feb45ec423d631b465b0235ec939ee5e339` on branch `issue100-batch-a`, with the title and body it was opened with. Posting this text is the operator's separate go-ahead, with the exact text shown to him first (use `gh api -X PATCH repos/KJ5HST/methodology/pulls/102` with `title` and `body` read from the two files here, then read both back and compare byte for byte; not `gh pr edit`). Pushing to the branch is not part of it: the head stays at `c93f1feb`.

**Files.** `title.txt` (99 B) and `body.md` (10,402 B) are the postable text and nothing else. The old body is 5,835 characters (`gh pr view 102 --json body`); the new one is about 1.8 times as long. The complaint was an unstated purpose, not length, so the added bytes are definitions, the purpose and the ask, each judged by whether a reader needs it to decide; the mechanics of the network call (process group, Ctrl-C, ssh options) were cut to a pointer at the commit message.

## What the operator reported

"The purpose for the PR is not clearly stated." (BL-132, verbatim in `BACKLOG-DETAIL.md`.) Nothing more was known about what he found unclear, so the first step was to read the pull request as a stranger would.

## The cold read

One fresh agent, no knowledge of this repository, three phases, each a file it was given only at that phase: (A) the title alone, (B) the title and the first 12 lines of the body (what the page shows first), (C) the whole body. It was told the maintainer's own vocabulary (runner, trimmer, ledger, receipt, seed, gate, ratchet, `bin/status`, Disclosure Hook, "adopter") and told not to flag it, and to flag only invented terms, forward references, pronouns with two referents, figurative words of place, motion or possession, counts without a denominator, and claims stronger than the text shows. It could use only the Read tool on the named file. Its answers were claims; each was checked against the code, the commit messages or a run before it was used.

| What the reader found | Checked against | In the draft |
|---|---|---|
| A, B, C: the text never says what went wrong for anyone; the nearest is a pointer ("the issue's scenario") | #100's Summary and finding 1; the four commit messages | The opening paragraph states #100's scenario in two sentences; each commit gets a **Problem** line |
| B, C: the text never says why four changes are one pull request, and "the other commits apply on their own" argues against it | `docs/planning/issue100-fixes-plan.md` §0 and the merge trials below | The opening paragraph states the criterion (no line that #96, #98 or #99 also change); the ask paragraph states the one dependency (commit 2 needs commit 1) |
| B, C: the reviewer is never told what to do | n/a | A **What is asked of you** paragraph |
| C: the largest behaviour change (a network call, by default, in a status command) is in the last table row and a mechanics paragraph | the diff: 575 of the 1,359 added lines are tests for it | Moved into the ask, as the one decision that is the maintainer's, with the switch that turns it off |
| A: "three fixes" read from a title with four items joined by semicolons; C: "one per item of the issue" overstated (findings 5 and 6 are partial, one "smaller point" is not a finding) | #100's findings | Title is one purpose plus "three smaller fixes"; the opening says "one for each of four points" |
| B: "keeps", "names" (three senses), "asks", "paid for by a cut in 1B", "headroom under its ceiling", "best effort", "keeps its id", "the verify script", "umask" | the commit messages and `.context-budget.json` (runner limit 18,900 tokens x 2.8107 B per token = 53,122 B; the file is 52,839 B at the base and 52,828 B at the tip, so 283 B then 294 B under it) | Each replaced by what happens; two commit headlines and one sentence of #100 that contain "keeps" or "names" are quoted unchanged |
| B, C: "New tests 17 / 12 / 29" and "261 ... 229, 177, 256 and 45" have no unit and no relation | `.quality-gates.json` at the tip: 261 is `tests-sh-passed`; 229, 177, 256, 45 are the dashboard, context-budget, trimmer and ratchet suites (floors 229, 148, 227, 45; 148 + 29 = 177 and 227 + 17 + 12 = 256) | Units and suite names; the floors stay as the PR leaves them |
| C: "usually a few seconds" against 0.8 s measured; "12 s to 56 s" with only 13 s explained | the commit message of commit 4; a run today (below) | The measured ranges, as measurements; today's 36 s against 7 s and its 11 s test |
| C: "never in `--precommit`" has no test cited; "attributes off, which is GitHub's view" is unshown | commit 4's message lists the `--precommit` test; the merge-trial script's header explains `--attr-source` | "a test checks this"; the trial re-run today, with the reason in one clause |

## Figures: re-measured today, and carried

**Re-measured today** on a scratch clone of the PR tip (`c93f1feb`, no hooks, nothing written to this repository): `python3 starter-kit/quality_ratchet.py --run` read 12/12 pass, 0 fail, 0 unmeasured (results `78a9bbfccfbd`, manifest `06181a10ec42`), with `tests-sh-passed` 261, 0 failed, and the suites 229, 177, 256 and 45; `tools/test_context_budget.py` ran 177 tests, 0 failures, 0 errors, 2 skipped, in 36 s at the tip against 7 s at the base `d50ce290` (one run each), the slowest test being the one that waits out the 10-second limit at 11.2 s; `bash docs/planning/issue100-plan-evidence/piece-merge-trials.sh c93f1feb...` read #99 `47637be2` 0 regions with and without the tip, #98 `65990cda` 0 and 0, #96 `b4af3293` 1 region in `CHANGELOG.md` with and without it; `upstream/main` is still `d50ce290`, the PR's merge base; the runner sizes.

**Carried from the commit message of commit 4, not re-run** (they need the network): the `git ls-remote` call time of 0.3 to 3.7 s against github.com on two afternoons; whole `bin/status` runs of 2.5 to 3.0 s against 1.7 to 2.2 s with the check off; the `context_budget.py --status --remote` run from a checkout at v4.1. The draft states them as measurements from one machine, not as typical times.

## What this draft does not decide

- **Posting it** is his go-ahead, each time, after he has seen this text.
- **The offer "If you would rather it were opt-in, say so"** (the ask paragraph) is the author's to keep or cut; it invites a change to commit 4 and commits nobody to it.
- **Two "smaller points" in #100 have no commit and no plan item**: the trimmer's `FRONTMATTER_FIELD_ABSENT` warning on the `HANDOFFS.md` seed (still present on `upstream/main`; this fork's own trims print it too) and the dashboard's only size risk naming a vendored header. The old body did not list them as left out; the draft does. Whether to build them is a backlog question, not done here.
- **Whether the draft is now clear** is tested by one more cold read of these exact files (result recorded below when it is done); a rating is not used.
