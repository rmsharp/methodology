# PR2b layer 9: the sync layer (`bin/sync`, `bin/status`, `bin/check-links`, `bin/_manifest_reader.py`) on `upstream/main` (S385, 2026-10-27)

**Status: BUILT and verified, local, un-pushed to `KJ5HST/methodology`, nothing sent there.** This is the ninth checkpoint of PR2b
(`../upstream-pr-composition-plan.md` section 5, the PR2b row; layers 1 to 8 are `pr2b-layer1-record.md` to `pr2b-layer8-record.md`). Every figure is
printed by a script here or by a command named beside it. The saved outputs are `pr2b-layer9-verify-output.txt` (the clean-clone run, four parts),
`pr2b-layer9-measure-output.txt` (the scanner on the parent and on the commit, the scrub count, the merges with `upstream/main` and the open pull requests' heads),
`pr2b-layer9-next-alone-output.txt` (the next eleven candidate commits, each applied alone onto this tip), `pr2b-layer9-check-links-both-output.txt` (the 35 dangling links) and
`pr2b-layer9-probe-output.txt` (Test 15's two counts over this layer's own `bin/status`). What I read from files and what a command measured are labelled.
Two scripts are new and tracked beside them: `pr2b-layer-driver.sh` (the verification's four parts in order, which S383 and S384 ran from a scratchpad file) and `pr2b-next-alone.sh`.

## 1. The answer first

1. **The layer exists.** Branch `pr2b/candidate` (a local ref with no upstream, so a bare `git push` cannot send it) now has nine commits on `upstream/main`
   `d50ce290`: layers 1 to 8 (`fbcef390`, `41a1e580`, `7d87cb2b`, `1d93579a`, `62680cd2`, `f767ced0`, `e5210601`, `07ec025b`, unchanged, ancestors) and layer 9 `97425a70` (tree `c8f801b0`): **5 files, +447 / -108**,
   built in a scratch `--no-local` clone and fetched here (fast-forward only, after the verification). `pr2/candidate` (`3cba1e50`) is kept as it was.
2. **It applied cleanly, and nothing was re-judged.** `git cherry-pick -x 261b8d36` onto `07ec025b` exited 0. The replayed commit is **equal to the original by `git patch-id --stable`** (`c37ac29a640b` for both).
   `git diff --numstat` is the original's: `65 7 bin/_manifest_reader.py`, `150 47 bin/check-links`, `85 21 bin/status`, `145 32 bin/sync`, `2 1 tools/test_layout_resolver.py`.
3. **Neither open pull request touches any of the five files.** `git diff --stat upstream/main <head> -- <the five>` is empty for #98's head (`65990cda`) and for #96's (`ad5c980f`); read before building. The merge-tree rows (section 4) confirm it: the layer adds 0 regions to either.
4. **The replayed message's figures held**, so none was changed. It says "the shell suite passes unchanged on this commit: 298 passed, 0 failed, 0 skipped": measured, **298 passed, 0 failed, 0 skipped**.
5. **It is green in a clean clone** (section 4): the quality ratchet **13/13 pass, 0 fail, 0 unmeasured**, results `7959143a08c1` and manifest `d66cb326a0dd` (both equal to layers 7 and 8), every measured value equal to its floor, **no floor changed**; the shell suite run directly: **298 passed, 0 failed, 0 skipped**.
   One verification only: the commit verified is the commit kept.
6. **My claim-time expectations, scored** (fourteen, written to a file at 20:37:44 CDT, before the cherry-pick and before any output was read). E1 the cherry-pick exits 0: **confirmed**. E2 patch-id equal: **confirmed**. E3 the five numstat pairs exactly: **confirmed**.
   E4 the layout suite still 75 and the dashboard suite still 395: **confirmed** (the 2/1 edit changes the `COPIES` list, not the test count). E5 the ratchet 13/13 with every floor unchanged: **confirmed**. E6 `bin/tests.sh` 298/0/0 with Test 15 reading `(30 == 30)`: **confirmed**, and layer 8's reason now holds in the layer's own tree (item 7a).
   E7 the scanner 14 to 10, `bin/status` 3 to 0 and `bin/check-links` 1 to 0, files with sites 4 to 2: **confirmed**; the cause I had in mind was only half right (section 3). E8 `check-links` with no flag exits 0 and `--layout both` fails at this layer: **confirmed** (35 dangling links, 13 files).
   E9 clean with `upstream/main`, tree equal to the layer's own: **confirmed** (`c8f801b08ea6`). E10 the same 5 regions with #98's head: **confirmed**. E11 the same 4 with #96's: **confirmed**. E12 the scrub regex matches some but fewer than 15% of the added lines: **confirmed**, 6 of 447.
   E13 the next commits alone: **nine of ten verdicts held; one miss**, commit 11 (`a459b8bb`) is now clean alone where I wrote that it would still conflict (item 7b). E14 (the fork's own 24 gates read 24/24 at close-out) is scored in the close-out receipt.
7. **Findings for the grouping plan.** (a) **Layer 8's reason is now measured on a real tree.** In this layer's tree a project synced with `bin/sync --mode=commit` and read with its `bin/status` prints a `layout: <name>  legacy` line above the table, and Test 15's two counts over that output are **the old assertion 31, the new one 30, for 30 manifest entries** (`pr2b-layer9-probe-output.txt`). So this layer without layer 8 would fail Test 15 (31 != 30); with it, the full suite passes. Layer 8 stays before layer 9.
   (b) **One conflict vanished once commit 9 was in.** Onto this tip, alone: **10 (`0aa1897e`), 11 (`a459b8bb`), 13 to 16 and 20 (`5afc9621`) are clean; 12 (`505541c3`: `.quality-gates.json`, `bin/tests.sh`, `tools/test_layout_resolver.py`), 17 (`18cda0f2`: `.quality-gates.json`), 18 (`2942e46c`: `tools/test_layout_resolver.py`, `tools/test_sync_layouts.py`) and 19 (`ab35e965`: `.quality-gates.json`, `bin/tests.sh`) conflict alone.**
   Commit 11 conflicted in `tools/test_layout_resolver.py` onto layer 8's tip and does not now: this layer edits the same file's `COPIES` list. Commit 20 had not been measured. Whether the four that remain survive in order is still unmeasured; every list conflict so far has vanished once the commits that append to the same lists were in.
   (c) **`bin/check-links --layout both` applies for the first time, and it is red, as a to-do list.** The legacy half reads 116 links OK; the new half reads **35 dangling links in 13 files**, all in the distributed documents (`methodology/RECOMMENDED_SKILLS.md` 14, `ITERATIVE_METHODOLOGY.md` 8, the workstreams and campaigns 8 in 7 files, `SESSION_RUNNER.md` 2, `BOOTSTRAP.md`, `CHANGELOG.md`, `HANDOFFS.md` 1 each). Those are the documents commits 13 to 16 make hold in both layouts, and commit 17 adds the test for it.
   (d) **The code in this layer is ahead of its own suite.** The sync tools' suite (`tools/test_sync_layouts.py`, +986 lines, with two gates and the scanner's scope) is commit 10, the next layer, so the new branches of `bin/sync` (`--layout new`, the three refusals, `--source=github` reading the second table) are exercised here only by the unchanged shell suite and the probe. The commit's own message says so.

## 2. What it carries

| File | Change | Why it is in the layer |
|---|---|---|
| `bin/sync` | +145 / -32 | `--layout auto\|legacy\|new`: `auto` keeps a project in the layout it has and gives an empty one the legacy layout; a legacy project asked for the new layout, a migrated one asked for the legacy, and a half-migrated one are refused before any write (exit 2) |
| `bin/status` | +85 / -21 | prints a `layout:` line per project and reads files and seeds where that layout keeps them |
| `bin/check-links` | +150 / -47 | `--layout legacy\|new\|both` simulates either tree; the default stays legacy |
| `bin/_manifest_reader.py` | +65 / -7 | reads the manifest's second table (`NEW_LAYOUT`, which layer 2 added to `bin/_manifest.py`) as data, so `--source=github` can serve either layout |
| `tools/test_layout_resolver.py` | +2 / -1 | the suite's `COPIES` list gains the three tools that now embed the resolver block |

**By reading** the plan's section 4 table: none of the five is in the "Not carried" column (theme A names the sync layers). By `git diff --name-only parent commit`: exactly these five files.

## 3. The scanner on this tree (the to-do list, not a failure)

`python3 -I bin/check-layout-literals` reads **10 sites (3 path, 7 text) over 2 files**, exit 1, on the commit; the parent read **14 (6 path, 8 text) over 4 files**. `bin/status` 3 -> 0 and `bin/check-links` 1 -> 0; `bin/check-handoff` 6 and `bin/check-ledger` 4 did not move.
**The two falls are not the same kind** (section 3b of the measure output): `bin/check-links`' one counted line is gone from the new file (rewritten), but `bin/status`' three counted lines are in the new file **verbatim** and now each carries a `layout: ok -- <reason>` marker, so the acknowledged count rose from 114 to 117 (`bin/status` 0 -> 3) and the prose count from 187 to 188. They are acknowledged, not resolved.
The scanner still scans 14 files: `bin/sync` and `bin/_manifest_reader.py` come into its scope with commit 10 (`bin/check-layout-literals` +2). What is left is the two checkers, commit 11's tools.

## 4. The checks of the PR2 row, and which of them apply here

Clean `--no-local` clone, serial, `pr2b-layer-driver.sh`: Part 1 (`layer-verify.sh`) 20:40:09 to 20:49:44, **9 min 35 s**; Part 2 (`bash bin/tests.sh` directly) 20:49:44 to 20:55:00, **5 min 16 s**; the machine's load average was 7.6 at the start and 6.2 a minute later, with another session's gate run going in a different project. The verified commit was `97425a70`.

| Check (plan section 5, PR2 row) | Result |
|---|---|
| `quality_ratchet.py --run` (`pr2b-layer9-verify-output.txt`, Part 1) | **13/13 pass, 0 fail, 0 unmeasured**; results `7959143a08c1`, manifest `d66cb326a0dd` (both equal to layers 7 and 8). Measured against floors: `tests-sh-passed` 298/298, `dashboard-unit-tests` 395/395, `context-budget-unit-tests` 163/163, `trimmer-unit-tests` 265/265, `ratchet-unit-tests` 120/120, `layout-unit-tests` 75/75; the seven zero-gates read 0 |
| `bash bin/tests.sh` run directly (Part 2) | **298 passed, 0 failed, 0 skipped**, exit 0; Test 15 reads `PASS: status: one row per manifest file (30 == 30)` (line 112 of the saved output) |
| the cheap suites, run first in the build clone | `python3 -I -B tools/test_layout_resolver.py`: 75 tests OK in 1.8 s. `python3 -I -B tools/test_methodology_dashboard.py`: 395 tests OK in 57.5 s. The commit touches the first file only by the `COPIES` list and the second not at all |
| every shipped `.verify.sh` exit histogram equal to upstream's | one tracked proof (`docs/archive/CHANGELOG-through-2026-09-30.md.verify.sh`): exit 0. **Also `--reverify` of that shard: OK, exit 0** (Part 3, trimmer v1.9.0). This layer does not change the trimmer |
| `bin/check-layout-literals` | applicable now: **10 sites, a to-do list** (section 3); the row's 0 is for the last tool-resolving layer |
| `bin/check-links --layout both` | **applicable for the first time, and red as a to-do list**: with no flag exit 0 and `--layout legacy` exit 0 (116 relative links across 23 distributed files resolve); `--layout new` exit 1; `--layout both` exit 1, the new half with **35 dangling links in 13 files** (item 7c). The `check-links` gate (no flag, 0 findings) passes |
| the changed-file list equal to section 2 | by reading (section 2) and by `git diff --numstat` in Part 1 and in the measure output |
| PR2b row: `conflicts-after-merge` reads 0 | `conflicts-after-merge.sh` is fixed on `pr2/candidate`, so it cannot measure this branch; the method is `pr2b-layer-measure.py` section 5. **With `upstream/main`: exit 0**, tree `c8f801b08ea6`, equal to the layer's own (`c8f801b0`); the branch is 9 commits ahead |
| the same merge with #98's head (`65990cda`) | **exit 1, 5 regions in 3 files** (`.quality-gates.json` 1, `starter-kit/methodology_trim.py` 3, `tools/test_methodology_trim.py` 1): **identical to the parent**, so this layer adds 0; `upstream/main` alone with #98 is clean |
| the same merge with #96's head (`ad5c980f`) | **exit 1, 4 regions in 3 files** (`.quality-gates.json` 2, `CHANGELOG.md` 1, `bin/tests.sh` 1), identical to the parent; `upstream/main` alone reads 1 (`CHANGELOG.md`), the `merge=union` display gap. So the layer adds 0 |
| the read-set budget (`context_budget.py --status`, run by `layer-verify.sh`) | nothing over budget, exit 0 |
| `.quality-gates.json` after the replay | unchanged (the numstat lists no such file); `--run` above reads every threshold back as the floor |

No threshold was touched.

## 5. The two open pull requests

Measured in section 4 and item 3 of section 1. **#98:** this layer adds no region, so the series against #98's head stays at 5 regions in 3 files, all in the trimmer, its tests and the gates file; #98 does not touch `bin/sync`, `bin/status`, `bin/check-links`, `bin/_manifest_reader.py` or the layout suite.
**#96:** the series against #96's head stays at 4 regions in 3 files; #96 touches none of the five either. The next layer will touch `.quality-gates.json` (commit 10: +17 / -2), the file both heads already conflict in, so layer 10 is where a new region is possible; that is a measurement for its record, not a claim here.

## 6. What this does not show

1. **The surface** is this machine: clean clones, serial runs, hooks **not armed** (`layer-verify.sh` unsets `core.hooksPath`). Windows is untried and no adopter was run (PR3's table is not re-run; the plan says it is, after all layers).
2. **The layer's new behaviour is barely exercised by its own checks.** `tools/test_sync_layouts.py` is commit 10. What ran here: the unchanged shell suite (which syncs and reads temporary projects, kept in the legacy layout by `--layout auto`), the probe (`bin/sync --mode=commit` then `bin/status`, legacy only), `check-links --layout` in all three values, and the layout suite's `COPIES` equality. **No run here put a project in the new layout, asked `bin/sync` for a refused combination, or ran `--source=github`.** The layer is a checkpoint; its tests are the next one.
3. **The probe is a hand-run of Test 15's own lines** (`bin/tests.sh`, Test 15), not a run of the suite; the suite's own run passed it (item 4).
4. **A slip in my own expectations:** none in numbers this time. The cause I attached to E7 (the scanner falls because the lines were resolved) was right for `bin/check-links` and wrong for `bin/status`, whose three lines are acknowledged; the counts I wrote held either way. E13's miss is item 7b.
5. **Layers 10 to 33 are untested here.** Nothing in this record claims anything about them beyond the merge-tree verdicts of item 7b, which are estimates.

## 7. Next

**Commit 10 onward** of the candidate: 24 commits remain (10 to 33; 34 is dropped as superseded). Commit 10 (`0aa1897e`, `test(sync): the sync layer's own suite, its two gates, and the scanner's scope`) is 5 files by `git show --numstat` (`.quality-gates.json` 17/2, `bin/check-layout-literals` 2/0, `bin/tests.sh` 10/0, `tools/test_layout_resolver.py` 7/1, `tools/test_sync_layouts.py` 986/0), clean alone on this tip (exit 0).
Expect on it: the ratchet's gate count to rise (the commit names two new gates, so 15 if each counts once) with the floors it sets equal to what is measured; `tests-sh-passed` to move if the 10 lines in `bin/tests.sh` add assertions; the scanner to scan more files (+2 lines of scope); and a possible new region against both open heads in `.quality-gates.json`. Check #98's and #96's heads against its five files first.
He ticked "Group commits 6-33 after layer 5" at the S381 picker; grouping is a plan edit for a later session, and a group is still verified at its boundary (gate (c) of `SESSION_RUNNER.md` §Vertical Slice Sessions), so grouping saves orientation and close-out, not verification time (about 15 minutes here). Item 6.2 is a reason to take commits 9 and 10 as one group.
Re-run this layer: fetch `pr2b/candidate` into a scratch `--no-local` clone (a branch at layer 9's tip), then
`nohup bash docs/planning/pr-composition-evidence/pr2b-layer-driver.sh 9 <repo> <build clone> <clean clone> <output file> <done file> &`, and
`python3 -I docs/planning/pr-composition-evidence/pr2b-layer-measure.py <repo> <commit> upstream/main <the open PRs' heads>`; the saved measurement was run with `upstream/main`,
`65990cda6afdff7242a63b6a47dd5a2eb120b55a` (#98) and `ad5c980f345758df3dae8276e778c0883ded833c` (#96). The next commits alone: `bash docs/planning/pr-composition-evidence/pr2b-next-alone.sh <repo> <tip> 10 20`.
Run the two cheap suites first (`tools/test_layout_resolver.py`, 2 s; `tools/test_methodology_dashboard.py`, 52 to 83 s).
