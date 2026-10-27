# PR2b layer 7: methodology_dashboard.py 2.22.0, the dashboard reads a project that keeps its methodology files under `methodology/`, on `upstream/main` (S383, 2026-10-27)

**Status: BUILT and verified, local, un-pushed, nothing sent to `KJ5HST/methodology`.** This is the seventh checkpoint of PR2b
(`../upstream-pr-composition-plan.md` section 5, the PR2b row; layers 1 to 6 are `pr2b-layer1-record.md` to `pr2b-layer6-record.md`). Every figure is
printed by a script here or by a command named beside it; the saved outputs are `pr2b-layer7-verify-output.txt` (the clean-clone run), `pr2b-layer7-measure-output.txt`
(the scanner on the parent and on the commit, the scrub count, and the merges with `upstream/main` and the open pull requests' heads) and `pr2b-layer7-next-alone-output.txt`
(the next twelve candidate commits, each applied alone onto this tip). What I read from files and what a command measured are labelled.

## 1. The answer first

1. **The layer exists.** Branch `pr2b/candidate` (a local ref with no upstream, so a bare `git push` cannot send it) now has seven commits on `upstream/main`
   `d50ce290`: layers 1 to 6 (`fbcef390`, `41a1e580`, `7d87cb2b`, `1d93579a`, `62680cd2`, `f767ced0`, unchanged, ancestors) and layer 7 `e5210601` (tree `d44458c2`): **5 files, +1350 / -238**,
   built in a scratch `--no-local` clone and fetched here (fast-forward only, after the verification). `pr2/candidate` (`3cba1e50`) is kept as it was.
2. **It applied cleanly, and nothing was re-judged.** `git cherry-pick -x dd581fed` onto `f767ced0` exited 0 (git said `Auto-merging .quality-gates.json`, a three-way merge with no marker). For all five files
   the replayed hunks are **equal to the original commit's** by `git patch-id --stable` (measured per file: `.quality-gates.json` `7ce6622f0049`, `starter-kit/methodology_dashboard.py` `e49913683125`,
   `tools/methodology_dashboard.py` `d6ddcd746b9a`, `tools/test_layout_resolver.py` `8f94eabc11e7`, `tools/test_methodology_dashboard.py` `7cf79d26af24`). Layer 6 also needed none; layer 5 needed three.
3. **No version collision.** The dashboard goes 2.21.0 to 2.22.0 (`DASHBOARD_VERSION`, both twins). `upstream/main`, **#98's head (`65990cda`) and #96's head (`ad5c980f`) all read 2.11.3** (measured with `git show <ref>:tools/methodology_dashboard.py`),
   and neither open pull request changes either dashboard file (`git diff --stat upstream/main <head> -- <both twins>` is empty for each). That comparison was made at Phase 0, before building.
4. **The replayed message's figures all held**, so none was changed: the twins +370 / -115 each, their tests +595 / -4, the layout suite +13 / -2, the gates file 2 / 2, "395, from 354" dashboard tests and "75, from 74" layout tests.
   Measured: `git diff --numstat` equals the original's line for line; `Ran 395 tests ... OK` (the parent's floor was 354) and `Ran 75 tests ... OK`.
5. **It is green in a clean clone** (section 4): the quality ratchet **13/13 pass, 0 fail, 0 unmeasured**, every measured value equal to its floor (395 and 75 are the two new exact ones; 298, 163, 265 and 120 unchanged and exact);
   the shell suite run directly: **298 passed, 0 failed, 0 skipped**. One verification only: the commit verified is the commit kept.
6. **My claim-time expectations, scored** (written to a file at about 16:35 CDT, before the cherry-pick at 16:36:10 and before any output was read). E1 the cherry-pick exits 0: **confirmed**. E2 all five files' hunks equal the original's: **confirmed, 5 of 5**.
   E3 the message's figures hold: **confirmed**. E4 the scanner falls from 93 to 14, the dashboard 79 to 0 and the other four files unchanged: **confirmed** (section 3). E5 the ratchet 13/13 with the two floors exact: **confirmed**.
   E6 `bin/tests.sh` 298/0/0: **confirmed**. E7 clean with `upstream/main`, tree equal to the layer's own: **confirmed** (`d44458c259de`). E8 the same 5 regions with #98's head, none added: **confirmed**.
   E9 the same 4 regions with #96's head: **confirmed**. E10 no version collision: **confirmed**. Ten of ten. The two things I did not predict are in item 7 and in section 3.
7. **Findings for the grouping plan.** (a) **Commits 9 and 10 now apply alone with no conflict.** S382 measured them conflicting alone onto layer 5's and layer 6's tips (`tools/test_layout_resolver.py` and `.quality-gates.json`); this layer appended to those lists, and they are clean on this tip
   (`pr2b-layer7-next-alone-output.txt`). That is the order effect S382 predicted, now seen twice. **(b) 11 and 12 still conflict alone** (11 in `tools/test_layout_resolver.py`; 12 in `.quality-gates.json`, `bin/tests.sh` and `tools/test_layout_resolver.py`), and the later
   commits **17, 18 and 19** conflict alone in lists (17 in `.quality-gates.json`; 18 in `tools/test_layout_resolver.py` and `tools/test_sync_layouts.py`; 19 in `.quality-gates.json` and `bin/tests.sh`); 13 to 16 are clean. **Whether any of these conflicts survive in order is unmeasured**; the only evidence is that every list conflict so far has vanished once the commits that append to the same lists were in.

## 2. What it carries

| File | Change | Why it is in the layer |
|---|---|---|
| `starter-kit/methodology_dashboard.py` | +370 / -115 (2.21.0 to 2.22.0) | by the commit's message: the checklist items keep their names and are located through the layout resolver the tool now embeds; a project whose runner is under `methodology/` is still an adopter; a half-migrated tree (the runner at both places, or a state file at both with nothing to decide) is a high risk naming both paths; the file walk, the installed-source fingerprint, the ledger locator and the trim and read-cap rows read either layout; `--sync` resolves each target's layout, refuses a half-migrated project by name, and a copy inside `methodology/` finds its project and writes beside itself; the quality-gate read finds the manifest where it lives and follows its history across the move; the publisher's checklist follows its own moved ledgers |
| `tools/methodology_dashboard.py` | +370 / -115 | the canonical twin; the dashboard suite byte-compares it with the `starter-kit/` file, and the layout suite asserts the embedded block is the module's, byte for byte, in both |
| `tools/test_methodology_dashboard.py` | +595 / -4 | 395 tests (354 before) |
| `tools/test_layout_resolver.py` | +13 / -2 | the dashboard joins the layout suite's lists of embedding tools and of tools held at zero counted sites, and a test that the `tools/` twin carries the same block (75 tests, from 74) |
| `.quality-gates.json` | +2 / -2 | `dashboard-unit-tests` 354 to 395 and `layout-unit-tests` 74 to 75, the measured counts |

**By reading** the plan's section 4 table: none of the five is in the "Not carried" column (`CLAUDE.md`, `README.md`, the ledgers, `docs/`, `close_out_report.py`, the canonical-only checkers). By `git diff --name-only parent commit`: exactly these five, nothing else.

## 3. The scanner on this tree (the to-do list, not a failure)

`python3 -I bin/check-layout-literals` reads **14 sites (6 path, 8 text) over 4 files**, exit 1, on the commit; on the parent it read 93 (70, 23). The only file whose count moved is `starter-kit/methodology_dashboard.py`, **79 to 0**, and its acknowledged sites go **0 to 83**
(total acknowledged 31 to 114). The remaining counted sites are unchanged: `bin/check-handoff` 6, `bin/check-ledger` 4, `bin/check-links` 1, `bin/status` 3. "Prose not counted" 172 to 187.

**What the 79 to 0 means, because the layer 6 shape does not repeat.** Layer 6's `context_budget.py` went 8 to 0 mostly by rewriting (6 of 8 site lines gone). This layer is the other way: the crude check of section 3b of the measure output says **70 of the parent's 79 site lines still occur verbatim in the commit's file, 9 do not.**
The names stay, now carrying a same-line `layout: ok -- <reason>` marker, and the lookup moved to the resolver. I counted the markers and read their reasons (84 `layout: ok` lines in the file, 83 acknowledged by the scanner); I did not read all 83 sites. By the markers' own words: 48 say
*the LEGACY name of a methodology file, the key every table and the card use; where it lives is resolved by `layout_locations`*; 13 *a name printed in a message, never opened*; 3 *the legacy `docs/methodology/` prefix the new layout drops*; 3 *the ledger's own file name: the resolver's anchor*; the other 17 are one-off reasons (19 distinct wordings in all): this tool's own file name (3), the generated file's own name (2), a workstream's legacy name (2), the ledger's legacy path (2),
and one each for the manifest's name, the results file's name, the legacy shard directory, the framework anchor, the directory a migrated project keeps, the checklist's directory items, the runner's checklist key and a banner text a generated proof carries. So the scanner's 0 here is an acknowledgement that those names are keys and messages, not a claim that no path literal remains in the file. Whether each acknowledgement is right is the reviewer's, and it is the place a careful maintainer would look first.

## 4. The checks of the PR2 row, and which of them apply here

Clean `--no-local` clone, serial, `layer-verify.sh` (16:38:02 to 16:46:40, **8 min 38 s**) and then `bash bin/tests.sh` directly (16:46:40 to 16:51:33, **4 min 53 s**); the verified commit was `e5210601`.

| Check (plan section 5, PR2 row) | Result |
|---|---|
| `quality_ratchet.py --run` (`pr2b-layer7-verify-output.txt`, Part 1) | **13/13 pass, 0 fail, 0 unmeasured**; results `7959143a08c1`, manifest `d66cb326a0dd`. Measured against floors: `tests-sh-passed` 298/298, `dashboard-unit-tests` 395/395, `context-budget-unit-tests` 163/163, `trimmer-unit-tests` 265/265, `ratchet-unit-tests` 120/120, `layout-unit-tests` 75/75; the seven zero-gates read 0 |
| `bash bin/tests.sh` run directly (Part 2) | **298 passed, 0 failed, 0 skipped**, exit 0 |
| the cheap suites, run first in the build clone | `python3 -I -B tools/test_layout_resolver.py`: 75 tests OK in 1.68 s (the parent 74, 1.47 s in S382). `python3 -I -B tools/test_methodology_dashboard.py`: 395 tests OK in 52.3 s, no skipped line printed |
| every shipped `.verify.sh` exit histogram equal to upstream's | one tracked proof (`docs/archive/CHANGELOG-through-2026-09-30.md.verify.sh`): exit 0. **Also `--reverify` of that shard: OK, exit 0** (Part 3). This layer does not change the trimmer, so that run shows it left it working |
| `bin/check-layout-literals` | applicable now: **14 sites, a to-do list** (section 3); the row's 0 is for the last tool-resolving layer |
| `bin/check-links --layout both` | **not applicable at this layer**: the flag arrives with the sync layer (commit 9). The `check-links` gate (0 findings) passes |
| the changed-file list equal to section 2 | by reading (section 2) and by `git diff --numstat` in Part 1 and in the measure output |
| PR2b row: `conflicts-after-merge` reads 0 | `conflicts-after-merge.sh` is fixed on `pr2/candidate`, so it cannot measure this branch; the method is `pr2b-layer-measure.py` section 5. **With `upstream/main`: exit 0**, tree `d44458c259de`, equal to the layer's own (`d44458c2`); the branch is 7 commits ahead |
| the same merge with #98's head (`65990cda`) | **exit 1, 5 regions in 3 files** (`.quality-gates.json` 1, `starter-kit/methodology_trim.py` 3, `tools/test_methodology_trim.py` 1): **identical to the parent**, so this layer adds 0; `upstream/main` alone with #98 is clean |
| the same merge with #96's head (`ad5c980f`) | **exit 1, 4 regions in 3 files** (`.quality-gates.json` 2, `CHANGELOG.md` 1, `bin/tests.sh` 1), identical to the parent; `upstream/main` alone reads 1 (`CHANGELOG.md`), the `merge=union` display gap. So the layer adds 0 |
| the read-set budget (`context_budget.py --status`, run by `layer-verify.sh`) | nothing over budget, exit 0 |
| `.quality-gates.json` after the replay | the diff against the parent is exactly two thresholds (`dashboard-unit-tests` 354 to 395, `layout-unit-tests` 74 to 75), read in this session, and `--run` above reads them back as the floors |
| a real run of the layer's dashboard (not in the PR2 row; added here) | `python3 -I -B tools/methodology_dashboard.py --no-open` in the clean clone, a legacy-layout project: exit 0, banner `v2.22.0`, health 72/100, 0 high-or-worse risks, `dashboard.html` written beside the tool |

No threshold was loosened: the two raised floors are exactly the counts of the tests the layer carries.

## 5. The two open pull requests

Measured in section 4 and item 3 of section 1. **#98:** this layer adds no region, so the series against #98's head stays at layer 5's 5 regions in 3 files, all in the trimmer, its tests and the gates file; **#98 does not touch this layer's files**, and the version 2.22.0
is free there. **#96:** the series against #96's head stays at 4 regions in 3 files, the same as at layer 3. Neither pull request changes the tool this layer carries, so nothing here depends on his stack-or-supersede answer at PR5 (plan lines 226 to 227).

## 6. What this does not show

1. **The surface** is this machine: clean clones, serial runs, hooks **not armed** (`layer-verify.sh` unsets `core.hooksPath`). The dashboard was exercised by its 395 unit tests, which build fixture trees in both layouts, and by one real run on a legacy-layout project (section 4).
   **No real project with its methodology files under `methodology/` was run through the layer's dashboard**, no adopter was run (PR3's table is not re-run; the plan says it is, after all layers), and Windows is untried.
2. **`--sync` writing into `methodology/`, and its refusal of a half-migrated project by name,** are covered by the suite's fixtures, not by a sync of a real project; the sync layer proper arrives at commit 9.
3. **The scanner's 0 is mostly acknowledgement** (section 3): 83 sites carry a marker whose reason I read in aggregate, not site by site.
4. **Fork-internal references ride along.** 54 of the layer's 1350 added lines match the scrub regex of `pr2b-layer-measure.py` (`starter-kit/methodology_dashboard.py` 24 of 370, `tools/methodology_dashboard.py` 24 of 370 (the twin carries the same lines), `tools/test_methodology_dashboard.py` 6 of 595; rough, section 4 of the measure output).
   The plan puts the scrub in its own commits later in the series (candidate commits 21 to 30), so the layer carries them. The message itself carries none beyond "Part 2, layer 5", the old candidate's own name for this layer.
5. **The regions against #98 and #96 are counted, not read** (section 4); this layer adds none, so nothing new was left unread.

## 7. Next

**Commit 8 onward** of the candidate: 26 commits remain (8 to 33; 34 is dropped as superseded). Commit 8 (`4c0bdded`, `bin/tests.sh`, 3 / 1, "Test 15 counts the status table's rows") is clean alone and is layer 7's pair in the sizing (7+8); commit 9 (`261b8d36`, the sync layer) is now clean alone too (section 1, item 7).
He ticked "Group commits 6-33 after layer 5" at the S381 picker; grouping is a plan edit for a later session, and a group is still verified at its boundary (gate (c) of `SESSION_RUNNER.md` §Vertical Slice Sessions), so grouping saves orientation and close-out, not verification time (8 to 9 min plus 5 here).
Re-run this layer: fetch `pr2b/candidate` into a scratch `--no-local` clone, run `docs/planning/pr-composition-evidence/layer-verify.sh <clone> <commit>` and
`python3 -I docs/planning/pr-composition-evidence/pr2b-layer-measure.py <repo> <commit> upstream/main <the open PRs' heads>`. The saved measurement was run with `upstream/main`,
`65990cda6afdff7242a63b6a47dd5a2eb120b55a` (#98) and `ad5c980f345758df3dae8276e778c0883ded833c` (#96). Run the two cheap suites first (`tools/test_layout_resolver.py`, 1.7 s; `tools/test_methodology_dashboard.py`, 52 s).
