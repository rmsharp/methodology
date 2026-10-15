# PR2, Part 2, the prose layer: the framework documents say where the methodology files sit, and every reference in them resolves in both layouts

**Status: BUILT, verified in a clean clone, nothing sent.** Session S321, 2026-10-14. This is the eleventh PR2 session
(`../upstream-pr-composition-plan.md` §3 and §5; `layer6b-record.md` §5 named this layer). The local ref `pr2/candidate` moved
`505541c` to **`18cda0f`**, five commits, 19 files, +95 / -61; the candidate is now 17 commits, 44 files, +15,373 / -1,145 against `upstream/main` (`f34769f`).
Every figure below is printed by a script in this directory or by a command named beside it; the saved outputs are `layer6c-*-output.txt`.

## 1. The answer first

1. **Five commits of at most five files** (the cap is per commit; `SAFEGUARDS.md`). Four are documents, the fifth is the check that holds both layouts. What was run where: the shell suite on `c8d4375` alone (**300 passed, 0 failed, 0 skipped**, 5 min 23 s, load average 13.5 at launch, `layer6c-commit1-suite-output.txt`);
   `bin/check-links` in both layouts at every commit (§2); the shell suite on the final tree before its gate edit (301, below); the whole ratchet on `18cda0f`. The two middle commits (`04918ce`, `23e6e66`) are prose only; the shell suite was not run on either alone.

   | Commit | Files | +/- | What | Dangling in the `methodology/` layout after it |
   |---|---|---|---|---|
   | `c8d4375` `docs(layout)` | `starter-kit/` `SESSION_RUNNER.md`, `BOOTSTRAP.md`, `CLAUDE_TEMPLATE.md`, `SAFEGUARDS.md`, `HANDOFFS.md` | +48 / -27 | the operating files say where the files sit; their references hold in both layouts | 35 to **31** |
   | `04918ce` `docs(layout)` | `FRAMEWORK_APPARATUS.md`, `HOW_TO_USE.md`, `ITERATIVE_METHODOLOGY.md`, `starter-kit/CHANGELOG.md`, `starter-kit/RECOMMENDED_SKILLS.md` | +30 / -25 | the framework documents and the skills index | 31 to **8** |
   | `23e6e66` `docs(layout)` | five workstream and campaign documents | +6 / -6 | 1 of 2 | 8 to **2** |
   | `0248ebf` `docs(layout)` | `workstreams/TEMPLATE_CAMPAIGN.md`, `TEMPLATE_WORKSTREAM.md` | +2 / -2 | 2 of 2 | 2 to **0** |
   | `18cda0f` `test(layout)` | `bin/tests.sh`, `.quality-gates.json` | +9 / -1 | Test 10's second block: `bin/check-links --layout both`; `tests-sh-passed` 300 to 301 | 0 |

2. **The layer is the layout hunks only, and the tip's documents carry more than that.** Of the 23 framework documents, 6 are equal to the candidate's and 17 differ (+102 / -67 over 62 hunks: `layer6c-report-output.txt`).
   **54 hunks (+86 / -60) are layout** (35 `reference` hunks, which put a bare name in a code span where a relative link or a `docs/methodology/` path held only in the legacy layout; 19 `layout text`
   hunks, new prose about the `methodology/` layout). **8 hunks (+16 / -7) are not layout and are not carried:** the unmeasured-gate clause (3 hunks in `SESSION_RUNNER.md`, `starter-kit/HANDOFFS.md`, `HOW_TO_USE.md`,
   +7 / -4: plan §4's seam); issue #75's plan-surface rule (3 hunks in `SESSION_RUNNER.md`, +7 / -1: plan §8 leaves it out); a model-tag sentence in `SESSION_RUNNER.md` (+1 / -1); a session number in `HOW_TO_USE.md`
   (`plus, since S130,`, +1 / -1). **S320 left this open ("whether any of the 17 carries fork-only text beyond layout") and the answer is yes**; the probes before this one used the tip's documents whole and could not see it.
3. **The migration tool's own suite passes on the layout-only prose.** `layer6c-probe.sh` puts the tip's `bin/migrate-layout` and its suites on the candidate: at the parent (`505541c`) the two classes that hold the failures read **10 of 23 failed** (60 s);
   at `18cda0f` **the whole 280-test suite runs OK in 329 s** (`layer6c-probe-output.txt`). S320's NOT CHECKED, "the 280 are a statement about the pair, not about the prose layer's own commit", is answered, and for the layout-only prose.
4. **Verified: `layer-verify.sh` on `18cda0f` in a clean `--no-local` clone** (`layer6c-verify-output.txt`, 8 min 26 s, load average 3.45 at launch): the ratchet **16/16 pass, 0 fail, 0 unmeasured, results `7a4736a489ee`, manifest `682c7e6d2333`**;
   `tests-sh-passed` reads 301 (the floor, 300 plus the one new `pass` line; the suite alone on the tests stage: **301 passed, 0 failed, 0 skipped**, `layer6c-tests-suite-output.txt`); `layout-unit-tests` 76 and `checker-layout-unit-tests` 11 unchanged;
   the scanner **14 files, 0 sites**; the one shipped `.verify.sh` proof exit 0.
5. **The cost to a legacy reader, stated.** The relative links across the 23 distributed documents go from **116 to 80** in the legacy layout (`layer6c-measure-output.txt` §1): 36 clickable links become a bare name in a code span so that the same text holds in both layouts. Nothing dangles in the legacy layout before or after.

## 2. What was measured, and how

| Check | Result | Output |
|---|---|---|
| The simulated adopter tree after each commit (`bin/check-links`, each layout) | legacy OK at every commit; the `methodology/` layout 35, 31, 8, 2, 0, 0 dangling | `layer6c-measure-output.txt` §1 |
| The new check on the PARENT (`bin/check-links --layout both`, the command Test 10's second block runs) | **exit 1, 35 dangling** at `505541c`; exit 0 at `18cda0f` | §3 |
| Mutants, one per layout hunk (put back the candidate's own text): `bin/check-links --layout both` | **`reference`: 28 of 35 killed, 7 survived; `layout text`: 0 of 19 killed** (54 mutants, control green) | `layer6c-mutate-output.txt` |
| End to end: mutant 53 (`TEMPLATE_CAMPAIGN.md`'s runner link put back), the whole shell suite | Test 10's FIRST block still PASSes (legacy is fine); the new block FAILs; **300 passed, 1 failed, 0 skipped**, exit 1. Only the new block catches it | `layer6c-mutate-e2e-output.txt` |
| Real projects synced by the layer's own `bin/sync --layout new` and `--layout legacy`, links read in the project (`check-links --tree`) | both exit 0: 80 links across 23 files resolve | §4 |
| The prose's own example commands, run in the synced projects | `python3 methodology/methodology_trim.py --file methodology/CHANGELOG.md --check` exit 0 (migrated); the bare form exit 0 (legacy); **the legacy form in the migrated project exit 3** (so the rule matters); `python3 methodology/methodology_dashboard.py` exit 0, wrote `methodology/dashboard.html` and `methodology/dashboard_history.jsonl` | §4 |
| The builder reproduces the layer's tree and refuses on drift | built tree `03437e32f5c3` = the layer's; a line appended to the candidate's `SESSION_RUNNER.md` is refused ("blob `98f4881`, not `71ad950`"), 0 dirty paths | §2 |
| `layer6c-reference-check.py`, a backstop for the `reference` rule | 32 of 35 differ from the old text only by link syntax and paths; the other 3 name `FRAMEWORK_APPARATUS.md` where the link's TARGET did: the same pattern | `layer6c-reference-check-output.txt` |
| The two open pull requests (`git merge-tree`) | #94: the same 15 regions in the same 3 files at the parent and at the layer (1, 9, 5); #92 clean at both. The layer adds no conflict | §6 |

**What the mutation round says.** The 28 killed are every link that dangled in the `methodology/` layout. **The 26 that survived are not defects of the layer: they are lines no check in this tree reads.** Six of the seven `reference` survivors are `docs/methodology/…` paths spelled
in a code span (`SESSION_RUNNER.md`'s workstream table at lines 61, 67, 70 and 76, `SAFEGUARDS.md:108`, `BOOTSTRAP.md:423`), which `check-links` does not follow; the seventh is `BOOTSTRAP.md`'s link to `PROJECT_LEARNINGS.md`, a project-owned file the checker does not
resolve. All 19 `layout text` hunks survive by construction: nothing asserts what the new prose says. They were checked by reading every changed line, by the flag and tool table (`layer6c-measure-output.txt` §5) and by running the prose's own examples (§4).

## 3. Decisions I took that the plan did not

1. **Layout hunks only; eight hunks are NOT carried.** The plan said "the prose" and the probe counted 17 differing documents; neither said that some of their differences are not layout. Carrying the tip's documents whole would have sent issue #75's rule (which the plan's §8 leaves out) and a session number. The unmeasured-gate clause is plan §4's seam
   and is **his call** (see §5); it is left out of this layer and named.
2. **Five commits, not one.** 17 documents at five per commit is four commits; the check goes last because it reads red until every reference is fixed.
3. **The block's two comment lines are reworded.** The tip's said "BL-101 P9" and "it read exit 1, 36 dangling, before P9": a fork token, and a figure that is false on this tree (the parent reads 35). Every other line of the block is the tip's own.
4. **Classification by rule, then read.** `layer6c-build.py` partitions each document's git zero-context hunks and REFUSES a hunk that is neither a layout hunk nor named in `NOT_LAYOUT`; the rule is loose (a hunk naming `methodology/` or "layout" passes), so every one of the 169 changed lines was also read in this session.
5. **Not touched:** `bin/migrate-layout` and its suite (the next layer), the scrub, `README.md`, `CLAUDE.md`.

## 4. What this does not show

The surface is this machine (load average 3 to 54 over the session, the highest readings from another project's browser tests running beside it): clean clones, serial runs, `nohup` and done-files. **Not shown:**
- the prose's CLAIMS about tools the candidate does not yet carry: `bin/migrate-layout`, `--apply` and `--tier` are named in BOOTSTRAP's *Two layouts* section and exist only in the tip's tool (`layer6c-measure-output.txt` §5), which the next layer carries; they were read against the tip's tool, not run here;
- an adopter's real documents (the documents synced are the candidate's own); Windows; a maintainer's machine; upstream CI (there is none); the candidate merged with #94 (derived, the same 15 regions, not resolved);
- the 26 survivors of §2: prose and path spellings no check reads. A check for path-spelled references (`docs/methodology/` in a distributed document outside the places that mean the legacy layout) does not exist in the fork either: a candidate for a backlog row if he asks.

**Scrub input** (`layer6c-measure-output.txt` §7, a coarse regular expression over the 95 added lines): backlog codes 0, a phase 0, a session number 0, a `docs/planning/` path 0, a plan section 0, in every file and in all five commit messages; the 5 "failure mode" matches are the framework's own sentences carried on a changed line.

## 5. Next, and a decision for him

**`bin/migrate-layout`, the last Part 2 layer** (plan §3 as amended): re-base `layer7-build.py` (`COPIES_OLD` at `:70` ends `"bin/sync", "bin/status", "bin/check-links")` and the candidate's `COPIES` ends `"bin/check-ledger", "bin/check-handoff")`), write the paired gate (BL-109's shape),
and replace `layer7-probe.sh`'s `docs` state with this layer's commits as the first check: `layer6c-probe.sh` is that check run once, 280 OK.
**For him: the unmeasured-gate prose** (3 hunks in 3 files, +7 / -4). Plan §4 says it ships as prose; the candidate carries the ratchet change that makes "unmeasured" a real reading (1.5.0), and not the lint that enforces the clause. Options: (a) a small commit after `bin/migrate-layout`, with the PR's text stating that the lint stays on the fork *(recommended)*;
(b) leave it on the fork; (c) decide at the PR's text.
Re-run this layer: `bash layer-verify.sh <candidate> 18cda0f`; rebuild: `python3 layer6c-build.py <fork> 7087493 <clone-at-505541c> --stage docs1`, commit, `--stage docs2` to `docs4`, `--stage tests`, then `--stage tests --passed 301`; the rest: `layer6c-build.py … --report --candidate-rev 505541c`,
`layer6c-measure.sh`, `layer6c-mutate.py <fork> 7087493 <clone-at-18cda0f> 505541c [--e2e 53]`, `layer6c-probe.sh`, `layer6c-reference-check.py`.
