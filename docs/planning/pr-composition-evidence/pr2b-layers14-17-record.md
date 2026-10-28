# PR2b layers 14 to 17: the budget cure and the documentation group, on `upstream/main` (S390, 2026-10-28)

**Status: BUILT and verified in a clean clone, green on every line the plan's PR2 row names and on the read-set budget. Local, un-pushed to `KJ5HST/methodology`, nothing sent there.** These are the fourteenth to seventeenth checkpoints of PR2b
(`../upstream-pr-composition-plan.md` section 5, the PR2b row; layers 1 to 13 are `pr2b-layer1-record.md` to `pr2b-layer13-record.md`). They are added **as one group**, verified once at the group's tip, because he said the documentation changes are to be grouped (S389 receipt, item 7) and picked "Cure plus docs group: 31, then 14 to 16, as one group" at the S390 Phase 0 picker. Every figure is printed by a script here or by a command named beside it.
The saved outputs are `pr2b-layers14-17-build-output.txt` (the four cherry-picks, the group's numstat, the budget at the tip, the four cheap suites), `pr2b-layers14-17-verify-output.txt` (the clean-clone run, four parts), `pr2b-layers14-17-measure-output.txt` (one `pr2b-layer-measure.py` run per commit), `pr2b-layers14-17-next-alone-output.txt` (commits 17 to 33, each applied alone onto the new tip) and `pr2b-layers14-17-expectations.txt` (fourteen expectations, written **before** the first cherry-pick and **kept as written**; its modification time, 12:50:12, is earlier than the first cherry-pick's 12:50:22).

## 1. The answer first

1. **The group exists.** Branch `pr2b/candidate` (a local ref with no upstream, so a bare `git push` cannot send it) now has seventeen commits on `upstream/main` `d50ce290`: layers 1 to 13 (unchanged, ancestors; layer 13 is `09ac2846`) and, new:

   | Layer | Replay | Original (number on `pr2/candidate`) | Subject | Files, +/- |
   |---|---|---|---|---|
   | 14 | `6ce88cdf` | `ced2c823` (31) | drop the layout paragraph's duplicate example command; the runner reads under its ceiling again | 2, +4 / -4 |
   | 15 | `36660db6` | `04918ce3` (14) | the framework documents and the skills index hold in both layouts | 5, +30 / -25 |
   | 16 | `1e61fab2` | `23e6e66a` (15) | the workstreams name the runner, the skills index and the safeguards without a path (1 of 2) | 5, +6 / -6 |
   | 17 | `109375f4` | `0248ebf2` (16) | the same (2 of 2) | 2, +2 / -2 |

   The group is **14 files, +42 / -37** (tip tree `5814dafb`). It was built in a scratch `--no-local` clone and fetched here fast-forward only, after the verification, with the build's `HEAD~4` checked equal to the old tip. `pr2/candidate` (`3cba1e50`) is kept as it was.
2. **It applied cleanly, and nothing was re-judged.** Four `git cherry-pick -x` runs, all exit 0; each replay equals its original by `git patch-id --stable` (`79fa9e8cce3b`, `9ff36b45e5e7`, `e221cf849f0c`, `a022aff3366b`, both columns equal).
3. **The one plan edit in it is commit 31's place.** On `pr2/candidate` the budget cure is number 31; here it is layer 14, right after the layer that made the budget red (layer 13). Both commits are verbatim, so their patch-ids do not change; only their order does. He approved this at the picker (the answer's text is in the claim's ledger entry). **The plan file is not edited**: it sits at 29,992 of its 30,000 B gate, so this record and the claim entry carry the reorder, as the layer 13 record said a plan edit would have to.
4. **The budget is green again, and stays green.** `python3 starter-kit/context_budget.py --status` exits 0 at the tip: `starter-kit/SESSION_RUNNER.md` 53,100 B (84 B less than layer 13's 53,184 B), read-set total 70,048 B, resident 51,487 B unchanged, `nothing over budget`. The table prints bytes and a dash while a row is ok; the token figure is my arithmetic: 53,100 B at the 2.8130 B/token that `ced2c823` records in `.context-budget.json` is about 18,877 tokens, 23 under the 18,900 ceiling (at the old 2.8107 it would be about 18,892, 8 under). Commits 14, 15 and 16 edit none of the four files the budget tracks, so the line equals the one after layer 14.
5. **Every check the plan's PR2 row names passes in a clean clone** (section 4): the quality ratchet **16/16 pass, 0 fail, 0 unmeasured**, results `6e788a952599` and manifest `d0e1c782db6e` (**both equal to layer 13's**: the group adds no gate and moves no measured value); the shell suite run directly **300 passed, 0 failed, 0 skipped** with Test 15 `(30 == 30)`; the scanner `scanned 14 files; 0 sites (0 path, 0 text); 124 acknowledged; 189 prose not counted`; the shard's `--reverify` exit 0; the tracked proof exit 0.
6. **`check-links` is green in every layout for the first time since layer 9.** Layer 9 made `--layout both` applicable and it read 35 dangling links in 13 documents; layer 13 left 31 in 10. At this tip `bin/check-links` (no flag), `--layout legacy`, `--layout new` and `--layout both` all exit 0 with **80 links in 23 files**. **The count fell by 31, from 111, which is also how many were dangling.** The group's diff removes 41 markdown links from its lines and adds 10 (net -31; `git diff -U0 09ac2846 pr2b/candidate`, a regex over `](...)` on the `-` and `+` lines, `.context-budget.json` excluded), so the cure is mostly **plain file names in place of path links**, as the commits' subjects say ("without a path"). I did not match the 31 dangling links to the 31 net removed one by one; the equality of the two counts is measured, the identity is my reading. For an adopter the effect is that some references in the distributed documents stop being clickable and stay readable in both layouts.
7. **My claim-time expectations, scored** (fourteen, every one confirmed; the one I marked least sure came out better than forecast). E1 four cherry-picks exit 0: **confirmed**. E2 four patch-ids equal: **confirmed**. E3 the group's numstat, 14 files, +42 / -37, each pair as listed: **confirmed**. E4 budget exit 0, read-set 70,048 B, resident unchanged: **confirmed** (the token figure is derived, not printed). E5 cheap suites 76, 11, 82, 395: **confirmed** (1 s, 2 s, 34 s, 45 s; the build clone stayed clean). E6 ratchet 16/16, both digests equal to layer 13's: **confirmed**. E7 `bash bin/tests.sh` 300/0/0 and Test 15 `30 == 30`: **confirmed**. E8 `--reverify` exit 0: **confirmed**. E9 `check-links` legacy exit 0 and `new`/`both` exit 0 with 0 dangling, **sixty percent sure and marked so**: **confirmed**; not forecast: the link count, 111 to 80 (item 6). E10 the scanner's summary line unchanged: **confirmed**. E11 clean with `upstream/main` for each of the four, 5 regions with #98's head and 4 with #96's, 0 added: **confirmed**, and the reason I gave (commit 14's one hunk in the one shared file, `FRAMEWORK_APPARATUS.md`, is 43 lines from the nearest hunk of either head) was read from hunk headers, not tested. E12 the scrub matches 0 of 42 added lines: **confirmed** (0 of 4, 30, 6 and 2). E13 commits 17, 18 and 20 alone onto the new tip clean, 19 conflicts in `.quality-gates.json`: **confirmed**. E14 timing 14 to 18 minutes for the driver: **confirmed**, 15 min 16 s; its second half (the fork's own 24 gates at close-out) is scored in the close-out receipt.

## 2. What it carries

| File | Change | Why it is in the group |
|---|---|---|
| `starter-kit/SESSION_RUNNER.md`, `.context-budget.json` | +1 / -1 and +3 / -3 | layer 14: the layout paragraph's duplicate example command goes; the recorded size and density follow; the budget turns green |
| `starter-kit/RECOMMENDED_SKILLS.md` | +14 / -14 | layer 15: the skills index names the methodology documents without a path that holds in one layout only |
| `ITERATIVE_METHODOLOGY.md` | +7 / -7 | layer 15: the same for the framework document |
| `HOW_TO_USE.md`, `FRAMEWORK_APPARATUS.md`, `starter-kit/CHANGELOG.md` | +4 / -3, +4 / -0, +1 / -1 | layer 15: the same; `FRAMEWORK_APPARATUS.md` gains four lines and is the one file an open head also edits |
| `workstreams/*` (five files) | +6 / -6 | layer 16: each workstream and campaign names the runner, the skills index and the safeguards without a path |
| `workstreams/TEMPLATE_CAMPAIGN.md`, `TEMPLATE_WORKSTREAM.md` | +2 / -2 | layer 17: the same for the two templates |

Read from `git diff --numstat 09ac2846 pr2b/candidate` and the commits' own messages.

## 3. The scanner

`pr2b-layers14-17-measure-output.txt` section 3 of each run: parent and commit read **14 files, 0 sites, 124 acknowledged** at every one of the four steps. No scanned file is touched.

## 4. Verification in a clean clone

`pr2b-layer-driver.sh 14-17` (unchanged since S386; the label is only printed), serial, hooks not armed, on `109375f4`: Part 1 12:52:06 to 13:01:36 (9 min 30 s), Part 2 to 13:07:21 (5 min 45 s), done 13:07:22 (15 min 16 s in all). Load average 7.2 at the launch and 12.9 at 13:01.

| Check | Result |
|---|---|
| quality ratchet `--run` | 16/16 pass, 0 fail, 0 unmeasured, results `6e788a952599`, manifest `d0e1c782db6e` (both equal to layer 13's) |
| each gate against its floor | every value equal to its floor (`tests-sh-passed` 300, `dashboard-unit-tests` 395, `context-budget-unit-tests` 163, `trimmer-unit-tests` 265, `ratchet-unit-tests` 120, `layout-unit-tests` 76, `checker-layout-unit-tests` 11, `sync-layout-unit-tests` 82, the eight zero-ceiling gates 0) |
| scanner | 14 files, 0 sites, 124 acknowledged |
| **read-set budget** | **exit 0** |
| tracked proof `docs/archive/CHANGELOG-through-2026-09-30.md.verify.sh` | exit 0 |
| `bash bin/tests.sh` | 300 passed, 0 failed, 0 skipped; Test 15 `(30 == 30)` |
| `--reverify` on that shard | exit 0 |
| `check-links` (no flag), `--layout legacy`, `--layout new`, `--layout both` | all exit 0, 80 links in 23 files |
| cheap suites in the build clone | layout 76, checker 11, sync 82, dashboard 395, all OK |

The layer 13 column of the same table, for comparison: budget exit 2; `check-links` exit 0 in the legacy layout (111 links) and exit 1 in `new` and `both` (31 dangling in 10 files).

## 5. The two open pull requests

Measured in `pr2b-layers14-17-measure-output.txt` section 5 of each run (merge-tree with the empty attribute tree, GitHub's view), heads read from GitHub at this session: #98 `65990cda`, #96 `ad5c980f`, both unchanged since S389 (each 0 comments, 0 reviews). For **each of the four commits**: clean with `upstream/main`, the merged tree equal to the commit's own (`8700524020e1`, `96f96a284d37`, `1ca9f960d2e6`, `5814dafb37db`; checked by comparing the tree ids). **#98:** exit 1, **5 regions in 3 files**, identical to layer 13's. **#96:** exit 1, **4 regions in 3 files**, identical to layer 13's. The group adds 0 regions to either. The one shared file is `FRAMEWORK_APPARATUS.md` (#98 `15 5`, #96 `0 17` by `git diff --numstat upstream/main <head>`, positive control `.quality-gates.json` `1 1` and `9 2`): the group inserts 4 lines after old line 486 and the heads' hunks start at 528 and 529. The count of regions is measured; **their lengths are not.**

## 6. What this does not show

1. **The surface** is this machine: clean clones, serial runs, hooks **not armed**. Windows is untried and no adopter was run (PR3's table is not re-run; the plan says it is, after all layers).
2. **The runner's token count is the tool's estimate** at the config's recorded density, not a doubled-read measure; the table does not print it while the row is ok, so the 18,877 above is my arithmetic.
3. **The 31-for-31 reading in section 1 item 6** is a counted equality, not a link-by-link match.
4. **"Alone, not in order"** (section 7): the verdicts for commits 21 to 33 are estimates; several conflict alone because an earlier commit in the series is not in the tip, and they may clear in order.
5. **The group was verified once, at its tip.** Layers 14, 15 and 16 were not each run through the ratchet and the shell suite; the budget and the cheap suites were read at the tip only, and the budget at layer 14 is argued from the byte sizes (no other tracked file changes after it), not run.
6. **Layers 18 to 33 are untested here.**

## 7. Next

**Sixteen commits remain** of the candidate (numbers 17 to 20, 21 to 30, 32 and 33 on `pr2/candidate`; 31 is in, 34 is dropped as superseded).
**Each alone onto this tip** (`pr2b-layers14-17-next-alone-output.txt`; alone, not in order; 31 (`ced2c823`) reads clean only because it is already in the tip):
- **clean:** 17 (`18cda0f2`), 18 (`2942e46c`), 20 (`5afc9621`), 21 (`c933b0f9`), 22 (`d31c25da`), 24 (`71e00e89`), 27 (`72e0c991`), 29 (`ccd5620e`);
- **conflicting:** 19 (`ab35e965`, `.quality-gates.json`; unchanged, commit 17 is not in the tip), 23 (`c1cdc2ec`, `tools/test_sync_layouts.py`), 25 (`ea751caa`, `bin/migrate-layout` and `tools/test_migrate_layout.py`), 26 (`2276f4ef`, `starter-kit/methodology_trim.py` and `tools/test_methodology_trim.py`), 28 (`8ace51e8`, the same two as 25), 30 (`28f99a70`, `bin/tests.sh`), 32 (`a62bfecf`, `bin/migrate-layout`), 33 (`cfcc713b`, `tools/test_methodology_dashboard.py`).
**What that says for the grouping, as an estimate:** the conflicts of 25, 28 and 32 name `bin/migrate-layout` and its suite, which commits 18 and 19 introduce; a scrub commit cannot go before the commit that adds the file it scrubs. I did not trace why 23, 26, 30 and 33 conflict alone (a sync suite, the trimmer and its suite, the shell suite, the dashboard suite); they are not the files commits 18 and 19 add. So the Markdown-only steps are now done (14 to 16 and 31) except 20 (`5afc9621`: `HOW_TO_USE.md` 1/1 and `starter-kit/HANDOFFS.md` 4/1), and the next group in the series' order is **17 to 19** (the test that the distributed documents resolve in both layouts, the migration tool, and its suite: code, not documents). The order for 20 and 32 as one group, which S389 proposed, needs 18 first.
**Re-run this group:** fetch `pr2b/candidate` into a scratch `--no-local` clone (a branch at `109375f4`), then `nohup bash docs/planning/pr-composition-evidence/pr2b-layer-driver.sh 14-17 <repo> <build clone> <clean clone> <output file> <done file> &`; `python3 -I docs/planning/pr-composition-evidence/pr2b-layer-measure.py <repo> <commit> upstream/main <the open PRs' heads>` **from the repository root** with full SHAs (#98 `65990cda6afdff7242a63b6a47dd5a2eb120b55a`, #96 `ad5c980f345758df3dae8276e778c0883ded833c`); the next commits alone: `bash docs/planning/pr-composition-evidence/pr2b-next-alone.sh <repo> pr2b/candidate 17 33`. Run the cheap suites first and read `python3 starter-kit/context_budget.py --status` at the tip **before** predicting, turning the runner's bytes into tokens (bytes / 2.8130 now).
