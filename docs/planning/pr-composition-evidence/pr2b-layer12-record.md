# PR2b layer 12: the checkers' own suite, its gate, and the layout scanner now reads both, on `upstream/main` (S388, 2026-10-28)

**Status: BUILT and verified, local, un-pushed to `KJ5HST/methodology`, nothing sent there.** This is the twelfth checkpoint of PR2b
(`../upstream-pr-composition-plan.md` section 5, the PR2b row; layers 1 to 11 are `pr2b-layer1-record.md` to `pr2b-layer11-record.md`). Every figure is
printed by a script here or by a command named beside it. The saved outputs are `pr2b-layer12-verify-output.txt` (the clean-clone run, four parts),
`pr2b-layer12-measure-output.txt` (the scanner on the parent and on the commit, the scrub count, the merges with `upstream/main` and the open pull requests' heads),
`pr2b-layer12-next-alone-output.txt` (commits 13 to 20, each applied alone onto this tip), `pr2b-layer12-check-links-both-output.txt` (the 35 dangling links, unchanged) and
`pr2b-layer12-expectations.txt` (fifteen expectations, written **before** the cherry-pick and **kept as written**; see item 7 for the one header figure in it that is wrong).

## 1. The answer first

1. **The layer exists.** Branch `pr2b/candidate` (a local ref with no upstream, so a bare `git push` cannot send it) now has twelve commits on `upstream/main`
   `d50ce290`: layers 1 to 11 (`fbcef390`, `41a1e580`, `7d87cb2b`, `1d93579a`, `62680cd2`, `f767ced0`, `e5210601`, `07ec025b`, `97425a70`, `19417746`, `877ba05d`, unchanged, ancestors) and layer 12 `19a5769b` (tree `108284f7`): **5 files, +230 / -7**,
   built in a scratch `--no-local` clone and fetched here (fast-forward only, after the verification, with the parent checked equal to the old tip first). `pr2/candidate` (`3cba1e50`) is kept as it was.
2. **It applied cleanly, and nothing was re-judged.** `git cherry-pick -x 505541c3` onto `877ba05d` exited 0 (08:40:49). The replayed commit is **equal to the original by `git patch-id --stable`** (`d308632776c5` for both),
   and `git diff --numstat` is the original's: `9 1 .quality-gates.json`, `0 2 bin/check-layout-literals`, `10 0 bin/tests.sh`, `204 0 tools/test_checker_layouts.py`, `7 4 tools/test_layout_resolver.py`.
3. **The replayed message's figures held.** It says 11 tests (measured: `Ran 11 tests`, OK), "tests-sh-passed goes 299 to 300" (measured 300), "14 files, 0 sites" (measured) and "the layout-unit-tests floor (76) is unchanged" (measured 76).
4. **It is green in a clean clone** (section 4): the quality ratchet **16/16 pass, 0 fail, 0 unmeasured**, results `6e788a952599`, manifest `d0e1c782db6e` (both differ from layer 11's `d5d188a311b2` and `474b645391ae`, as they must: a gate is added and a floor rises), every measured value equal to its floor;
   the shell suite run directly: **300 passed, 0 failed, 0 skipped**, Test 15 still `(30 == 30)`. One verification only: the commit verified is the commit kept.
5. **The scanner's 0 is now a reading, not an exemption.** The tracked scanner prints `scanned 14 files; 0 sites (0 path, 0 text); 124 acknowledged; 189 prose not counted`; its not-scanned list is the manifest and `bin/tests.sh` (plus the dashboard twin, printed as not scanned but scanned once through its original). The two exemptions layer 10 added are gone, so **the series now carries no exemption whose reason expires in a later commit** (layer 10's and layer 11's gotcha, closed by this commit).
6. **My claim-time expectations, scored** (fifteen). E1 the cherry-pick exits 0: **confirmed**. E2 patch-id equal: **confirmed**. E3 the five numstat pairs: **confirmed**. E4 layout suite 76, checker suite 11, sync suite 82, dashboard suite 395: **confirmed** (2 s, 2 s, 47 s, 55 s; the build clone stayed clean). E5 ratchet 16/16, every floor equal, both digests different: **confirmed**.
   E6 `bash bin/tests.sh` 300/0/0 with Test 15 `30 == 30`: **confirmed**. E7 the scanner's summary line exactly as measured at layer 11 by commit 12's tool, and two real exemptions: **confirmed**. E8 the shard's `--reverify` exit 0, budget exit 0, the tracked proof exit 0: **confirmed**. E9 `check-links` plain exit 0 and `--layout both` the same 35 dangling links in 13 files: **confirmed** (identical to layer 11's output apart from hashes).
   E10 clean with `upstream/main` (tree `108284f7`, equal to the layer's own), 5 regions with #98's head and 4 with #96's: **confirmed**, both the parent's counts. E11 the scrub regex matches 3 to 8 of the 230 added lines: **confirmed at the low edge**, 3 of 230 (`.quality-gates.json` 1, `bin/tests.sh` 1, `tools/test_checker_layouts.py` 1: the three places I named).
   E13 timing: **confirmed**, ratchet part 10 min 47 s (08:43:05 to 08:53:52) and `bin/tests.sh` 6 min 21 s (to 09:00:13); load average 14.9 at 08:40, 7.4 at 08:42 (the launch), 7.0 at 09:01. E14 (the fork's own 24 gates at close-out) is scored in the close-out receipt.
   **E12 was wrong in one verdict.** I said 13 to 16, 18 and 20 stay clean and "17 and 19 still conflict in `.quality-gates.json`", adding that commit 12's own edit of that file made "a vanishing or a new conflict possible". **17 (`18cda0f2`) is now clean alone**; 19 (`ab35e965`) still conflicts. The reason is in the numbers, not in my forecast: `tests-sh-passed`'s floor is a chain, 299 to 300 in commit 12, 300 to 301 in 17, 301 to 302 in 19 (`git show` of each), so each later commit's edit conflicts until its predecessor is in the tip. With commit 12 in, the tip reads 300 and 17's edit applies; 19's reads 301 against a tip at 300 and conflicts. In order, 19 should clear once 17 is in (a prediction about layer 17, not a measurement).
   **E15 was badly worded** (it describes a cross-run of two scanners that I did not make). Scored on the reading I ran: commit 12's scanner over layer 12's own tree prints the line layer 11 saved from running the same tool over layer 11's tree (`14 files; 0 sites; 124 acknowledged; 189 prose`): **confirmed**. Layer 11's older scanner over this tree was not run.
7. **One figure in the expectations file is wrong and the file was left as written:** its header says "written 08:41 CDT", an estimate typed ahead of the clock; the file's modification time is **08:40:26**, before the cherry-pick at 08:40:49. The order the record claims (written before the replay) holds either way.

## 2. What it carries

| File | Change | Why it is in the layer |
|---|---|---|
| `tools/test_checker_layouts.py` | +204 / -0 (new) | 11 tests that run `bin/check-ledger` and `bin/check-handoff` as commands in scratch projects: the ledger at the root, under `methodology/`, in a tie the runner decides, and in a half-migrated tree; `check-ledger --all` over shards in either layout; a repository itself called `methodology`; and a named ledger (`--file`) in a half-migrated tree |
| `.quality-gates.json` | +9 / -1 | adds the gate `checker-layout-unit-tests` (min 11, `python3 tools/test_checker_layouts.py`) and raises `tests-sh-passed` 299 to 300 |
| `bin/tests.sh` | +10 / -0 | runs the new suite, one pass/fail line |
| `bin/check-layout-literals` | +0 / -2 | removes the two `NOT_SCANNED_ALWAYS` entries layer 10 added (`bin/check-handoff`, `bin/check-ledger`) |
| `tools/test_layout_resolver.py` | +7 / -4 | the scan-set test names the two checkers; the test that pinned the exemption becomes one that pins the exact exempt list (the manifest and the suite), so the suite stays at 76 tests |

Read from the diffs (`git show 505541c3`); the figures come from the commands in section 4.

## 3. The scanner

`pr2b-layer12-measure-output.txt` section 3: parent `877ba05d` **12 files, 0 sites, 117 acknowledged**; commit **14 files, 0 sites, 124 acknowledged**. Sites per file: none differ. Acknowledged per file: `bin/check-handoff` 0 to 6, `bin/check-ledger` 0 to 1 (the same-line `layout: ok` markers commit 11 added; they were not counted at the parent because the two files were exempt from the scan there). That is the second half of the measurement layer 11 made: with commit 12's tool on layer 10's tree it read ten sites, on layer 11's none, and now the tracked scanner reads the same zero.

## 4. Verification in a clean clone

`pr2b-layer-driver.sh 12` (S386's script, unchanged), serial, hooks not armed, on `19a5769b`.

| Check | Result |
|---|---|
| quality ratchet `--run` | 16/16 pass, 0 fail, 0 unmeasured, results `6e788a952599`, manifest `d0e1c782db6e` |
| each gate against its floor | `tests-sh-passed` 300 (floor 300), `dashboard-unit-tests` 395, `context-budget-unit-tests` 163, `trimmer-unit-tests` 265, `ratchet-unit-tests` 120, `layout-unit-tests` 76, `checker-layout-unit-tests` 11, `sync-layout-unit-tests` 82, `layout-literals` 0, the rest 0: every value at its floor |
| scanner | 14 files, 0 sites, 124 acknowledged |
| read-set budget | exit 0, nothing over budget |
| tracked proof `docs/archive/CHANGELOG-through-2026-09-30.md.verify.sh` | exit 0 |
| `bash bin/tests.sh` | 300 passed, 0 failed, 0 skipped |
| `--reverify` on that shard | exit 0 |
| `check-links` (no flag) and `--layout legacy` | exit 0, 116 links in 23 files |
| `check-links --layout new` and `both` | exit 1, the 35 dangling links in 13 files, identical to layer 11's apart from hashes |
| cheap suites in the build clone | layout 76, checker 11, sync 82, dashboard 395, all OK |

## 5. The two open pull requests

Measured in `pr2b-layer12-measure-output.txt` section 5 (merge-tree with the empty attribute tree, GitHub's view), heads read from GitHub at this session: #98 `65990cda`, #96 `ad5c980f`. **#98:** exit 1, **5 regions in 3 files** (`.quality-gates.json` 1, `starter-kit/methodology_trim.py` 3, `tools/test_methodology_trim.py` 1), **identical to the parent's**. **#96:** exit 1, **4 regions in 3 files** (`.quality-gates.json` 2, `CHANGELOG.md` 1, `bin/tests.sh` 1), identical to the parent's. So the layer adds 0 regions to either.
**Unlike layer 11, this commit edits files the heads also edit** (`git diff --numstat upstream/main <head> -- <the five files>`, from the repository root with `.quality-gates.json` as the positive control: #98 `1 1` on `.quality-gates.json` only; #96 `9 2` on `.quality-gates.json` and `7 0` on `bin/tests.sh`). The count of regions is measured; **their lengths are not**, and the commit's edits (a new gate object, a ten-line block, a threshold 299 to 300) could lengthen a region without adding one.

## 6. What this does not show

1. **The surface** is this machine: clean clones, serial runs, hooks **not armed** (`layer-verify.sh` unsets `core.hooksPath`). Windows is untried and no adopter was run (PR3's table is not re-run; the plan says it is, after all layers).
2. **The suite drives the checkers in scratch projects.** Its own comment in `bin/tests.sh` says it "does not run them over this repository (the real-tree check is the evidence script of the P4 session)"; I did not re-run that script.
3. **The region lengths** in section 5, and **the forecast that 19 clears once 17 is in**, are not measured.
4. **E12's verdict for 17 and E15's wording were wrong** (section 1, items 6); the other verdicts held.
5. **Layers 13 to 33 are untested here.** Nothing in this record claims anything about them beyond the merge-tree verdicts of section 7, which are estimates.

## 7. Next

**Commit 13 onward** of the candidate: 21 commits remain (13 to 33; 34 is dropped as superseded). Commits 13 to 16 are the four `docs(layout)` commits: 13 `c8d43754` (5 files: `starter-kit/BOOTSTRAP.md` 30/12, `CLAUDE_TEMPLATE.md` 3/2, `HANDOFFS.md` 1/1, `SAFEGUARDS.md` 1/1, `SESSION_RUNNER.md` 13/11), 14 `04918ce3` (5 files: `FRAMEWORK_APPARATUS.md` 4/0, `HOW_TO_USE.md` 4/3, `ITERATIVE_METHODOLOGY.md` 7/7, `starter-kit/CHANGELOG.md` 1/1, `RECOMMENDED_SKILLS.md` 14/14), 15 `23e6e66a` (5 workstream files, 1 or 2 lines each), 16 `0248ebf2` (2 files, 1/1 each). They edit the runner and the framework documents, which are in the read set the budget gate (`context_budget.py --status`) measures: that line is the one a prose layer can turn red (the runner's 18,900-token ceiling), so read it, not only its exit code.
**The next commits alone, measured here** (`pr2b-layer12-next-alone-output.txt`): clean: 13 (`c8d43754`), 14 (`04918ce3`), 15 (`23e6e66a`), 16 (`0248ebf2`), 17 (`18cda0f2`, newly clean), 18 (`2942e46c`), 20 (`5afc9621`); conflicting: 19 (`ab35e965`, `.quality-gates.json`). Alone, not in order.
Re-run this layer: fetch `pr2b/candidate` into a scratch `--no-local` clone (a branch at layer 12's tip), then
`nohup bash docs/planning/pr-composition-evidence/pr2b-layer-driver.sh 12 <repo> <build clone> <clean clone> <output file> <done file> &`, and
`python3 -I docs/planning/pr-composition-evidence/pr2b-layer-measure.py <repo> <commit> upstream/main <the open PRs' heads>` **from the repository root** with the heads as full SHAs: the saved measurement used `upstream/main`,
`65990cda6afdff7242a63b6a47dd5a2eb120b55a` (#98) and `ad5c980f345758df3dae8276e778c0883ded833c` (#96). The next commits alone: `bash docs/planning/pr-composition-evidence/pr2b-next-alone.sh <repo> <tip> 13 20`.
Run the cheap suites first (`tools/test_layout_resolver.py`, 2 s; `tools/test_checker_layouts.py`, 2 s; `tools/test_sync_layouts.py`, 47 s; `tools/test_methodology_dashboard.py`, 55 s), and `cd` to the repository before any `git diff -- <path>`.
