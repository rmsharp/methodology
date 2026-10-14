# PR2, Part 1: the earlier lineage built on upstream's tree

**Status: BUILT and verified, un-pushed, nothing sent.** Session S311, 2026-10-13. This is PR2's first checkpoint of two to four
(`../upstream-pr-composition-plan.md` §5); Part 2's layers are not started. Every figure below is printed by a script in this
directory (`part1-*.sh`, `part1-*.py`) or by a command named beside it; the saved outputs are `part1-*-output.txt`.

## 1. The answer first

1. **The candidate exists.** Branch `pr2/candidate` in this repository (a local ref with no upstream, so a bare `git push` cannot send
   it) is one commit, `bbe0dc3`, on `upstream/main` `f34769f`: **9 files, +7,765 / −575**. It was built in a scratch clone
   (`~/.cache/s311-pr2`, no remote) and fetched here so it survives that directory.
2. **It is green on upstream's tree, which the plan named its first unknown (§3).** In a clean `--no-local` clone of `bbe0dc3`:
   `quality_ratchet.py --run` **12/12 pass · 0 fail · 0 unmeasured** (results `3d7518cbbfea`, manifest `0ca43ccb57ba`); the shell suite
   **271 passed, 0 failed, 0 skipped** against upstream's own 261 / 0 / 0; the dashboard suite 354 tests (upstream's gate floor
   was 229); the trimmer suite 181 (its floor 124). The one shipped `.verify.sh` exits 0 in upstream's tree and in the candidate's.
3. **The literal Part 1 of plan §3 is not green:** the 25 files of `upstream/main..c8b9ddd` laid over upstream's tree run the suite to
   **433 passed, 14 failed, 2 skipped** (`part1-literal-output.txt`), in the same nine blocks as the HEAD probe of §2.3. Eight are blocks
   of tools or ledger rules §4 leaves on the fork (the `check-handoff` lints, `model-report`, `check-learnings`, the ledger-norm test);
   the ninth, Test 18, holds three dashboard unit tests that read this repository's own files, and the close-out report suite (E).
4. **§3 and §4 of the plan disagree about what Part 1 holds, and I followed §4.** §3 says Part 1 *is* the 24 files of `c8b9ddd`;
   §4 says the pull request carries themes A to D and leaves E, F and G on the fork. Part 1 here is §4's reading: those files minus E, F
   and G, minus the files whose whole difference is token or comment churn (§3 below), plus the tests. The plan's §3 should say so.

## 2. What it carries

| File | Change | Why it is in Part 1 |
|---|---|---|
| `starter-kit/methodology_dashboard.py`, `tools/methodology_dashboard.py` (twins, byte-identical) | 2.11.3 → 2.21.0, +1,353 / −210 each, whole file | theme D, decision D3 (the whole lineage). **2.21.0, not the 2.22.0 of the fork's tip:** the last step is a Part 2 layer |
| `tools/test_methodology_dashboard.py` | +3,245 / −115 | its unit suite, 356 tests at `c8b9ddd`, **354 carried** (§4) |
| `starter-kit/methodology_trim.py` | 1.5.0 → 1.7.0, +430 / −22 | theme C. 1.7.0 is the fork's carry of issue #93, so it overlaps open PR #94 (plan §2.2) |
| `tools/test_methodology_trim.py` | +1,136 | its unit suite, 181 tests |
| `FRAMEWORK_APPARATUS.md` | +11 | the one paragraph the trimmer's new `FRONTIER_PENDING_STUB` warning is documented by |
| `starter-kit/BOOTSTRAP.md` | +2 / −2 | the never-overwrite row names `.gitattributes`, which `bin/_manifest.py` already classes as a seed |
| `bin/tests.sh` | +232 / −13 | a `skip()` primitive counted in the summary; the exec-bit check derived from the manifest (it named one tool); pipelines read under `pipefail` become here-strings in three blocks; **Test 35**, which pins `BOOTSTRAP.md`'s row to the manifest's seed list; **Test 36**, the lint that fails the suite if an early-exiting consumer decides a fail arm |
| `.quality-gates.json` | +3 / −3, three thresholds | tightened by exactly what the commit adds: `tests-sh-passed` 261 → 271, `dashboard-unit-tests` 229 → 354, `trimmer-unit-tests` 124 → 181 |

`bin/tests.sh` is **upstream's file with the fork's version of seven blocks and two more appended** (`part1-build-tests-sh.py` builds it
from two revisions): the preamble, the summary, and Tests 1, 9, 15, 16 and 20, which differ from upstream's only in the ways the table
names. Upstream's numbering stays; the fork renumbered its blocks (upstream's 26 and 27 to 34 are the fork's 41 and 46 to 53), which is churn,
not content. **Test 36 is what holds the three conversions in place:** the scanner finds 10 sites in upstream's file and 0 in the
candidate's (`python3` over the block's own heredoc, as the test does).

## 3. What it leaves out, and why (each checked against the diff)

| Not carried | Why |
|---|---|
| E `close_out_report.py` and its test; F `bin/check-handoff` lints, `check-overhead`, `model-report`, `check-learnings`; G `CLAUDE.md`, `README.md`, `.context-budget*`, `.gitignore` | plan §4 |
| `.githooks/pre-commit`, `bin/_manifest.py`, `HOW_TO_USE.md` | **the whole difference is comment or token churn** (`git diff upstream/main c8b9ddd`: the hook's three hunks are two comments and one test label, the manifest's two are a test number in a docstring and a comment, `HOW_TO_USE.md`'s is "since S130"). Carrying them adds churn and tokens for nothing |
| `starter-kit/SESSION_RUNNER.md` | its hunks are the plan-surface rule of issue #75 (the fork's row BL-70, which plan §8 lists as *not part of this plan*) and a ledger-bullet edit. A separate decision |
| Test 42 (the sibling lint, for producers read from the real repo) | it flags **1 site in upstream's own block** (`$OUT23`, line 607 of the candidate) and its scanner control mutates a line inside a `model-report` block (F), so it needs a site converted and a control rewritten. Part 2's shell-suite layer |
| The fork's Tests 23, 24, 29 to 34, 37 to 40 and 44 | blocks of F tools, or of this repository's own ledgers (plan §2.3); its Test 36 pins the #75 rule the runner's row leaves out |

## 4. Decisions I took that the plan did not

1. **Two dashboard tests are left out, not parametrised.** `test_backlog_is_watched_but_never_given_a_trim_row` and
   `test_the_fleet_facts_the_disposition_was_decided_on_are_stated_not_assumed` assert facts about this repository's own
   `docs/planning/BACKLOG.md`. A skip-if-absent guard would silence them *on the fork* if that file ever moved, which is the failure
   they exist to catch. **Cost:** the fork's test file becomes a superset of upstream's, so each later resync meets two extra tests.
2. **One is parametrised.** `test_record_counter_matches_the_trimmers_zoning_on_every_real_ledger` floored its comparison count at 6; upstream
   has 5 real ledgers. The floor is now `min(6, ledgers present)`, with a hard assertion that the four named ledgers exist, so on the
   fork nothing changes and a loop that compares nothing still fails.
3. **The candidate commit carries no `CHANGELOG.md` entry.** The scratch clone runs no hooks, and upstream's own ledger is the
   maintainer's. Whether the pull request adds entries is for the approval picker (plan §5, PR4).
4. **The scrub is not done** (plan §5 puts it in its own commit, after the layers). Added-line counts, `part1-files-and-tokens-output.txt`
   (taken at `bbe0dc3`): 88 lines with a backlog code, 80 with a session number,
   33 naming a `docs/planning/` path, 25 citing a learning, 44 with a plan-phase code, 15 with an issue number. **Seven plan documents the
   added lines cite do not exist upstream**; `docs/planning/BACKLOG.md` (18 lines) is also a path the dashboard *reads*, so the scrub must
   tell a cited path from a watched one.
5. **A Part 1 commit that is amended three times, not one commit per step.** The candidate has one commit by design (the plan's Part 1); the
   amendments were Test 36 (found by measuring, §3), and the gate floors, which follow the measured counts.

## 5. What this does not show

The surface is this machine: clean clones, serial runs, `nohup` and a done-file. **Not shown:** Windows; a maintainer's machine; hooks
armed in another clone (none ran here); upstream CI (there is none); whether the maintainer wants the dashboard lineage (plan §8's own
unknown). The 271 is upstream's tree plus Part 1, not the final pull request: Part 2 adds layers that change the counts, and the gate floors
move with them. **A mistake of this session's, kept here because it bears on the figures:** my first draft of this record said Test 45
needed every pipeline converted first and could not be carried; measuring the scanner (10 sites upstream, 0 after the three blocks) showed
it could, and it is carried as Test 36.

## 6. Next

PR2's remaining sessions are Part 2's layers, each a checkpoint commit with this directory's `part1-verify.sh` run on it, in the plan's
order (§3): the resolver and scanner; the gate layer (hook and ratchet); the trimmer 1.7.0 → 1.8.0; the context-budget gate; the dashboard
2.21.0 → 2.22.0; the sync layers and `bin/migrate-layout`; then the prose. The nine blocks of §2.3 are already settled for Part 1 (left
with the F and E tools); each later layer meets its own population blocks. Re-run: `bash part1-literal.sh` for §1.3;
`bash part1-verify.sh <repo> bbe0dc3` for §1.2.
