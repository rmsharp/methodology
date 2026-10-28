# PR2b layer 11: the checkers (`bin/check-ledger`, `bin/check-handoff`) find a project's ledger at the root or under `methodology/`, on `upstream/main` (S387, 2026-10-27)

**Status: BUILT and verified, local, un-pushed to `KJ5HST/methodology`, nothing sent there.** This is the eleventh checkpoint of PR2b
(`../upstream-pr-composition-plan.md` section 5, the PR2b row; layers 1 to 10 are `pr2b-layer1-record.md` to `pr2b-layer10-record.md`). Every figure is
printed by a script here or by a command named beside it. The saved outputs are `pr2b-layer11-verify-output.txt` (the clean-clone run, four parts),
`pr2b-layer11-measure-output.txt` (the scanner on the parent and on the commit, the scrub count, the merges with `upstream/main` and the open pull requests' heads),
`pr2b-layer11-next-alone-output.txt` (commits 12 to 20, each applied alone onto this tip), `pr2b-layer11-check-links-both-output.txt` (the 35 dangling links, unchanged),
`pr2b-layer11-scanner12-output.txt` (the scanner of commit 12 run over this layer's tree and its parent's) and
`pr2b-layer11-expectations.txt` (fifteen expectations, written 23:24:46 CDT before the cherry-pick and **kept as written**). What I read from files and what a command measured are labelled.

## 1. The answer first

1. **The layer exists.** Branch `pr2b/candidate` (a local ref with no upstream, so a bare `git push` cannot send it) now has eleven commits on `upstream/main`
   `d50ce290`: layers 1 to 10 (`fbcef390`, `41a1e580`, `7d87cb2b`, `1d93579a`, `62680cd2`, `f767ced0`, `e5210601`, `07ec025b`, `97425a70`, `19417746`, unchanged, ancestors) and layer 11 `877ba05d` (tree `f46a2e94`): **3 files, +134 / -19**,
   built in a scratch `--no-local` clone and fetched here (fast-forward only, after the verification). `pr2/candidate` (`3cba1e50`) is kept as it was.
2. **It applied cleanly, and nothing was re-judged.** `git cherry-pick -x a459b8bb` onto `19417746` exited 0. The replayed commit is **equal to the original by `git patch-id --stable`** (`ca25ad902d25` for both),
   and `git diff --numstat` is the original's: `60 13 bin/check-handoff`, `72 5 bin/check-ledger`, `2 1 tools/test_layout_resolver.py`.
3. **The replayed message's one figure held.** It says "the shell suite passes on this commit: 299 passed, 0 failed, 0 skipped" (measured, **299 / 0 / 0**).
4. **It is green in a clean clone** (section 4): the quality ratchet **15/15 pass, 0 fail, 0 unmeasured**, results `d5d188a311b2`, manifest `474b645391ae` (both equal layer 10's, as they must be: the commit does not touch `.quality-gates.json`), every measured value equal to its floor;
   the shell suite run directly: **299 passed, 0 failed, 0 skipped**, Test 15 still `(30 == 30)`. One verification only: the commit verified is the commit kept.
5. **The scanner's 0 over 12 files does not move, because the two checkers are still exempt** (layer 10's `NOT_SCANNED_ALWAYS`). What the commit does is measured separately, by commit 12's scanner (`bin/check-layout-literals` taken from `505541c3`, exemptions removed), run over two trees
   (`pr2b-layer11-scanner12-output.txt`): on layer 10's tree it reads **10 sites (3 path, 7 text), all ten in `bin/check-handoff` (6) and `bin/check-ledger` (4)**; on this layer's tree it reads **0 sites over 14 files, 124 acknowledged** (layer 10's scanner on the same tree: 12 files, 117 acknowledged). **So commit 11 resolves the ten sites and commit 12 makes the scanner read them.** This settles what layer 10's record could only infer from the two diffs.
6. **My claim-time expectations, scored** (fifteen, in `pr2b-layer11-expectations.txt`; **E4 to E6 and E8 restate figures the commit's message or layer 10 gave**, so they test the replay, not my judgment; the real forecasts are E7, E10, E11, E12 and E15).
   E1 the cherry-pick exits 0: **confirmed**. E2 patch-id equal: **confirmed**. E3 the three numstat pairs: **confirmed**. E4 layout suite 76, sync suite 82, dashboard suite 395: **confirmed** (the 76 was the one I was least sure of; the `COPIES` list is walked in one test method). E5 ratchet 15/15, every floor equal, `.quality-gates.json` unchanged: **confirmed**.
   E6 `bash bin/tests.sh` 299/0/0 with Test 15 `30 == 30`: **confirmed**. E7 scanner stays 0 over 12 files: **confirmed**. E8 the shard's `--reverify` exit 0, budget exit 0, the tracked proof exit 0: **confirmed**. E9 `check-links` plain exit 0, `--layout both` the same 35 dangling links: **confirmed** (the output equals layer 10's apart from hashes; 38 lines each).
   E10 clean with `upstream/main` (tree equal to the layer's own), the same 5 regions with #98's head and 4 with #96's: **confirmed**. E13 timing: **confirmed**, ratchet part 10 min 38 s (23:27:03 to 23:37:41) and `bin/tests.sh` 6 min 15 s (to 23:43:56), load average 7.6 at launch. E14 (the fork's own 24 gates at close-out) is scored in the close-out receipt.
   E15 (added at claim time for this layer, since its code has no suite until commit 12) commit 12's `tools/test_checker_layouts.py`, taken from `505541c3` and run untracked in the build clone against this layer's tree: **confirmed**, `Ran 11 tests`, `OK` (the file removed afterwards; the clone was clean).
   **Two forecasts were wrong in their detail:**
   **E11** said the scrub regex would match "fewer than 15% of the 134 added lines, most of them comment lines inside the two copies of the embedded resolver block". The threshold held, the reason did not: it matched **0 of 134** (60, 72 and 2 by file). The resolver block carries no fork-internal reference, so the later scrub commit has nothing to do here.
   **E12** said "17, 18 and 19 still conflict" and gave as its reason that "commit 11 edits only the COPIES list in the one shared test file, which 18 conflicts in". The reason had the sign backwards: **18 (`2942e46c`) now applies clean alone** because commit 11's `COPIES` edit is the change that commit 18 conflicted on at layer 10's tip. 12, 13 to 16 and 20 stay clean as forecast; 17 (`18cda0f2`) and 19 (`ab35e965`) conflict, both in `.quality-gates.json`.
   **One check was not in the expectations file:** the scanner run in item 5 (commit 12's scanner over two trees). I added it after the run, from layer 10's record (section 7: "the scanner at 14 files with 0 sites" as an expectation for commit 12), so it is a measurement, not a forecast I can score.

## 2. What it carries

| File | Change | Why it is in the layer |
|---|---|---|
| `bin/check-ledger` | +72 / -5 | embeds the layout resolver block and finds the ledger at the root or under `methodology/` (`default_ledger()`, the runner deciding a tie); refuses a half-migrated tree with exit 2 naming both files; `--all` reads the archived shards beside the ledger in either layout (`shard_dirs()`), and in a repository that is itself called `methodology` it still reads `docs/archive/` |
| `bin/check-handoff` | +60 / -13 | the same resolver block and reading (`default_path()`); refuses a half-migrated tree with exit 1 naming both (`HalfMigrated`); the same-line `layout: ok` markers that acknowledge a conventional file name in message text |
| `tools/test_layout_resolver.py` | +2 / -1 | the layout suite's `COPIES` list gains the two tools, so the suite asserts their embedded block is byte-identical to the module's |

Read from the diffs (`git show a459b8bb`). `bin/check-ledger` is replaced whole by its next revision; `bin/check-handoff` is this tree's copy plus the layout reading and nothing else, as the message says.

## 3. The scanner

The scanner gate (`layout-literals`) still reads 12 files and 0 sites, as at layer 10, parent to commit with no per-file difference (`pr2b-layer11-measure-output.txt` section 3). Its 0 remains a statement about scope until commit 12 removes the two exemptions. The measurement that matters for the series is item 5 of section 1: with the exemptions removed the scanner reads the ten sites on layer 10's tree and none on layer 11's, so commit 12 will turn on cleanly.
Split the two across pull requests and upstream still sees, between them, an exemption whose reason expires one commit later (layer 10's gotcha, unchanged).

## 4. Verification in a clean clone

`pr2b-layer-driver.sh 11` (S386's script, unchanged), serial, hooks not armed, on `877ba05d`: `layer-verify.sh` (ratchet `--run`, scanner summary line, read-set budget, every tracked `.verify.sh`), then `bash bin/tests.sh` directly, then the trimmer's `--reverify` on the one tracked shard, then `bin/check-links` in each `--layout` value.

| Check | Result |
|---|---|
| quality ratchet `--run` | 15/15 pass, 0 fail, 0 unmeasured, results `d5d188a311b2`, manifest `474b645391ae` |
| each gate against its floor | `tests-sh-passed` 299 (floor 299), `dashboard-unit-tests` 395, `context-budget-unit-tests` 163, `trimmer-unit-tests` 265, `ratchet-unit-tests` 120, `layout-unit-tests` 76, `sync-layout-unit-tests` 82, `layout-literals` 0, the rest 0: every value at its floor |
| scanner | 12 files, 0 sites, 117 acknowledged |
| read-set budget | exit 0, nothing over budget |
| tracked proof `docs/archive/CHANGELOG-through-2026-09-30.md.verify.sh` | exit 0 |
| `bash bin/tests.sh` | 299 passed, 0 failed, 0 skipped |
| `--reverify` on that shard | exit 0 |
| `check-links` (no flag) and `--layout legacy` | exit 0, 116 links in 23 files |
| `check-links --layout new` and `both` | exit 1, the 35 dangling links in 13 files, identical to layer 10's apart from hashes |
| `.quality-gates.json` after the replay | **unchanged** (the commit adds no gate and raises no floor) |
| cheap suites in the build clone | `tools/test_layout_resolver.py` 76, `tools/test_sync_layouts.py` 82, `tools/test_methodology_dashboard.py` 395, all OK |

## 5. The two open pull requests

Measured in `pr2b-layer11-measure-output.txt` section 5 (merge-tree with the empty attribute tree, GitHub's view), heads read from GitHub at this session: #98 `65990cda`, #96 `ad5c980f`. **#98:** the commit gives **exit 1, 5 regions in 3 files** (`.quality-gates.json` 1, `starter-kit/methodology_trim.py` 3, `tools/test_methodology_trim.py` 1), **identical to the parent's**; `upstream/main` alone with #98 is clean. **#96:** **exit 1, 4 regions in 3 files** (`.quality-gates.json` 2, `CHANGELOG.md` 1, `bin/tests.sh` 1), identical to the parent's; `upstream/main` alone with #96 reads 1 (`CHANGELOG.md`, the `merge=union` display gap). So the layer adds 0 regions to either.
**Why:** neither head touches any of the three files (`git diff --numstat upstream/main <head> -- <the three files and .quality-gates.json>`, run from the repository root with `.quality-gates.json` as the positive control: it printed `1 1` for #98 and `9 2` for #96, and nothing for the three). The commit edits none of the regions the heads already conflict in, so **the regions do not grow either** (an inference from that, not a measurement of their lengths; layer 10's growth came from editing inside them).

## 6. What this does not show

1. **The surface** is this machine: clean clones, serial runs, hooks **not armed** (`layer-verify.sh` unsets `core.hooksPath`). Windows is untried and no adopter was run (PR3's table is not re-run; the plan says it is, after all layers).
2. **The checkers' behaviour was shown by commit 12's suite, not by a suite in this tree.** E15 ran `505541c3`'s `tools/test_checker_layouts.py` untracked against this layer's tree: 11 tests, which drive each checker as a command in scratch projects in four shapes (legacy, new, a tie the runner decides, half-migrated; the half-migrated ones assert exit 2 for `check-ledger` and exit 1 for `check-handoff`, naming both files). Neither checker was run over an adopter's real tree here; the comment commit 12 adds to `bin/tests.sh` says the suite "drives the tools; it does not run them over this repository (the real-tree check is the evidence script of the P4 session)", and I did not re-run that script.
3. **The scanner check of item 5 is a read of commit 12's tool over this tree**, not a gate and not an assertion any layer carries. It shows the ten sites are resolved; it does not show commit 12 is correct.
4. **E11's reason and E12's reason were wrong** (section 1, item 6); the verdicts I committed to held except commit 18's, which turned clean.
5. **Layers 12 to 33 are untested here.** Nothing in this record claims anything about them beyond the merge-tree verdicts of section 7, which are estimates.

## 7. Next

**Commit 12 onward** of the candidate: 22 commits remain (12 to 33; 34 is dropped as superseded). Commit 12 (`505541c3`, `test(checkers): the checkers' own suite, its gate, and the layout scanner now reads both`) is 5 files by `git show --numstat` (`tools/test_checker_layouts.py` 204/0, `.quality-gates.json` 9/1, `bin/tests.sh` 10/0, `tools/test_layout_resolver.py` 7/4, `bin/check-layout-literals` 0/2), **clean alone** on this tip (exit 0), and it **removes the two exemptions layer 10 added**, so with it the exemption pair is gone from the series. Expect, from its message and from this record (expectations to write down at that session's claim, not results): the gate `checker-layout-unit-tests` added (16 gates), `tests-sh-passed` 299 to 300, `layout-unit-tests` held at 76, the scanner at 14 files with 0 sites (measured in item 5 of section 1 with this commit's tool, so the one number in that list that already has a measurement), and the suite itself at 11 tests (measured at E15).
**The next commits alone, measured here** (`pr2b-layer11-next-alone-output.txt`): clean: 12 (`505541c3`), 13 to 16 (`c8d43754`, `04918ce3`, `23e6e66a`, `0248ebf2`), 18 (`2942e46c`, newly clean), 20 (`5afc9621`); conflicting: 17 (`18cda0f2`, `.quality-gates.json`) and 19 (`ab35e965`, `.quality-gates.json`). Alone, not in order: a list conflict has vanished in order before, and a clean one could appear in order.
Re-run this layer: fetch `pr2b/candidate` into a scratch `--no-local` clone (a branch at layer 11's tip), then
`nohup bash docs/planning/pr-composition-evidence/pr2b-layer-driver.sh 11 <repo> <build clone> <clean clone> <output file> <done file> &`, and
`python3 -I docs/planning/pr-composition-evidence/pr2b-layer-measure.py <repo> <commit> upstream/main <the open PRs' heads>` **from the repository root** with the heads as full SHAs: the saved measurement used `upstream/main`,
`65990cda6afdff7242a63b6a47dd5a2eb120b55a` (#98) and `ad5c980f345758df3dae8276e778c0883ded833c` (#96). The next commits alone: `bash docs/planning/pr-composition-evidence/pr2b-next-alone.sh <repo> <tip> 12 20`.
Run the cheap suites first (`tools/test_layout_resolver.py`, 2 s; `tools/test_sync_layouts.py`, 40 s; `tools/test_methodology_dashboard.py`, 55 s), and `cd` to the repository before any `git diff -- <path>`.
