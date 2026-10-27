# PR2b layer 3: the ledger hook and the quality ratchet find the files under `methodology/`, on `upstream/main` (S379, 2026-10-27)

**Status: BUILT and verified, local, un-pushed, nothing sent to `KJ5HST/methodology`.** This is the third checkpoint of PR2b
(`../upstream-pr-composition-plan.md` section 5, the PR2b row; layers 1 and 2 are `pr2b-layer1-record.md` and `pr2b-layer2-record.md`). Every figure is
printed by a script here or by a command named beside it; the saved outputs are `pr2b-layer3-verify-output.txt` (the clean-clone run) and
`pr2b-layer3-measure-output.txt` (the scanner on the parent and on the commit, what became of the site lines, the scrub count, and the merges with `upstream/main` and the open pull requests' heads). What I read from files and what a command measured are labelled.

## 1. The answer first

1. **The layer exists.** Branch `pr2b/candidate` (a local ref with no upstream, so a bare `git push` cannot send it) now has three commits on `upstream/main`
   `d50ce290`: layers 1 and 2 (`fbcef390`, `41a1e580`, unchanged, ancestors) and layer 3 `7d87cb2b` (tree `49aa4f2b`): **6 files, +1,035 / -113**, built in a scratch
   `--no-local` clone and fetched here. `pr2/candidate` (`3cba1e50`) is kept as it was.
2. **It applied with no conflict**, as the sizing record predicted (`pr2b-sizing-record.md`): `git cherry-pick -x fd965939` onto `41a1e580`, exit 0, no marker, no
   file edited by hand. Git printed `Auto-merging .quality-gates.json`, which is a clean three-way merge, not a conflict; I read the result (section 4, last row).
   The per-file line counts equal the original commit's `git show --numstat` exactly (`pr2b-layer3-measure-output.txt`, section 2).
3. **One thing differs from the candidate's commit: its message.** It said the scanner "reads 121 sites (158 before)"; on this tree it reads **122 (159 before)**
   (section 3), so the message says that. Tree before and after the amend: `49aa4f2b`. The `-x` trailer was dropped. Every other figure the message quotes was
   re-checked on this tree (section 2, last paragraph).
4. **It is green in a clean clone** (section 4): the quality ratchet **13/13 pass, 0 fail, 0 unmeasured**, every measured value equal to its floor
   (298 and 81 are exact, so are the other four counts); the shell suite run directly: **298 passed, 0 failed, 0 skipped**.
5. **S378's expectation is confirmed by measurement:** the layer embeds the resolver in `starter-kit/quality_ratchet.py` (the layout suite, 74 tests, asserts the embedded block
   byte-identical and passes) and takes the scanner's count there from 16 to 0; it takes the hook's from 21 to 0. The other 7 of the 9 files are unchanged (section 3), and the 0
   rests partly on 17 acknowledged exemptions (section 3).
6. **No region needed his judgment**, and no gate floor needed re-deriving upward: the floors the commit declares are the numbers measured here.
7. **The open pull requests, measured per layer for the first time** (section 4, last rows; the plan's section 2.2 has the old candidate's figures): against #96's head the
   series reads the same 3 regions in 2 files the plan records for `pr2/candidate` (`.quality-gates.json` 2, `bin/tests.sh` 1), beyond the one ledger region #96 has against
   `upstream/main` alone. They are already there at layer 2, so **layer 3 adds none**. Against #98's head the series is clean so far (the old candidate read 52, in the trimmer
   and its tests, which no layer has touched yet).

## 2. What it carries

| File | Change | Plan section 1 / 4 theme | Why it is in the layer |
|---|---|---|---|
| `.githooks/pre-commit` | +246 / -63 | A ("the hook") | reads the ledger from the index at the root or under `methodology/`; refuses a ledger tracked in both places unless the runner decides; its selftest builds both layouts |
| `starter-kit/quality_ratchet.py` | +192 / -43 (1.1.0 to 1.3.0) | B | embeds the resolver block byte for byte; finds a manifest under `methodology/`; writes its results beside it; judges a manifest move |
| `tools/test_quality_ratchet.py` | +391 / -1 | B (its tests) | 81 tests (45 before) |
| `bin/tests.sh` | +202 / -2 | S, "portable blocks" | Test 37: the real hook and real git in both layouts, a control for each assertion; one assertion rewritten (line order of the chain) |
| `tools/test_layout_resolver.py` | +2 / -2 | A (its tests) | the ratchet joins the listed copies of the block; the hook and the ratchet join the scanned set, expecting 0 sites |
| `.quality-gates.json` | +2 / -2 | "gate thresholds tightened by exactly what the pull request adds" | `tests-sh-passed` 272 to 298, `ratchet-unit-tests` 45 to 81 |

**By reading** the plan's sections 1 and 4 (lines 55 to 83 and 157 to 172) in this session: none of the six is in section 4's "Not carried" column, and Test 37 is none of the
nine blocks of section 2.3 (18, 25, 26, 29, 30, 32, 34, 39, 40). The ratchet's 1.4.0 and 1.5.0 (a gate's own timeout and process group) are not in this layer; they are commit 4.

**The message's other figures, re-checked on this tree** (the replayed-message lesson of S378): the ratchet `VERSION` is `"1.1.0"` on the parent and `"1.3.0"` on the commit
(`grep -n '^VERSION'`); `python3 tools/test_quality_ratchet.py` prints `Ran 81 tests`, exit 0; `python3 tools/test_layout_resolver.py` prints `Ran 74 tests`, `OK` (unchanged);
the gates file's diff is exactly the two thresholds above; `bin/tests.sh` names `== Test 37: the ledger hook and the ratchet chain follow the files under methodology/ ... ==`
at line 1656; the suite count is section 4's. The one figure that differed is the scanner's.

## 3. The scanner on this tree (the to-do list, not a failure)

`python3 -I bin/check-layout-literals` reads **122 sites (80 path, 42 text) over 7 files**, exit 1, against **159 (102 path, 57 text) over 9 files** on the parent (the figures
layer 2's record gives, reproduced here by `pr2b-layer-measure.py`, which is the instrument-check). The two files that left the list:
`.githooks/pre-commit` 21 to 0 and `starter-kit/quality_ratchet.py` 16 to 0. The other seven are unchanged: `bin/check-handoff` 6, `bin/check-ledger` 4, `bin/check-links` 1,
`bin/status` 3, `starter-kit/context_budget.py` 8, `starter-kit/methodology_dashboard.py` 79, `starter-kit/methodology_trim.py` 21 (sum 122).

**Two numbers move together here, and they are not one split of 37.** Counted sites in the two files fall from 37 to 0. Separately, the scanner's *acknowledged* count (a site with a
same-line `# layout: ok -- <reason>` marker, the scanner's own mechanism, the reason in the source; `--all` lists them) rises from 1 to 18: 12 in the hook, 5 in the ratchet, none there
before. I first read these as "17 of the 37 became acknowledged"; the crude check of `pr2b-layer-measure.py` section 3b says otherwise: of the 37 parent site lines, **3 occur verbatim
in the new files (hook 1 of 21, ratchet 2 of 16) and 34 do not**, so the acknowledged lines are mostly new or rewritten code, not the old sites with a marker added. What became of the
34 I did not read line by line (the commit's message says the ratchet embeds the resolver and the hook reads the ledger from the index, so I expect most were replaced by the resolver's
or the index's answer; an expectation, not a measurement). What follows: "0 sites" for these two files rests on rewritten code **plus 17 acknowledged exemptions**; the plan's criterion
(0 sites, at the last layer that resolves a tool) counts sites, and an acknowledged site is not one. I did not judge the 17 reasons; they are the commit's, and the fresh-reader review of
PR4 is where the maintainer's view of them belongs.

## 4. The checks of the PR2 row, and which of them apply here

Clean `--no-local` clone, serial, `layer-verify.sh` (09:27:11 to 09:32:27, 5 min 16 s) and then `bash bin/tests.sh` directly (09:33:22 to 09:36:50, 3 min 28 s); the verified commit
was `7d87cb2b` (message already amended, so the commit verified is the commit kept; the clean clone's `HEAD` equals the build clone's and, after the fast-forward, the ref).

| Check (plan section 5, PR2 row) | Result |
|---|---|
| `quality_ratchet.py --run` (`pr2b-layer3-verify-output.txt`, Part 1) | **13/13 pass, 0 fail, 0 unmeasured**; results `e27bdec7fa29`, manifest `804d7f762278`. Measured against floors: `tests-sh-passed` 298/298, `dashboard-unit-tests` 354/354, `context-budget-unit-tests` 148/148, `trimmer-unit-tests` 227/227, `ratchet-unit-tests` 81/81, `layout-unit-tests` 74/74; the seven zero-gates (failures, links, learnings, handoff, ledger, the two hook selftests) read 0 |
| `bash bin/tests.sh` run directly (Part 2 of the same file, complete) | **298 passed, 0 failed, 0 skipped**, exit 0. Test 37 is 26 PASS lines (298 - 272): 17 assertions (the real hook, the ratchet and real git, in both layouts) and 9 mutant controls. Test 9 (the `--source=github` row) needs the network and passed, so the network was reachable; I did not run it offline |
| every shipped `.verify.sh` exit histogram equal to upstream's | one tracked proof (`docs/archive/CHANGELOG-through-2026-09-30.md.verify.sh`): exit 0 on the layer; exit 0 on the parent (`pr2b-layer2-verify-output.txt:39`) |
| `bin/check-layout-literals` | applicable now: **122 sites, a to-do list** (section 3); the row's 0 is for the last tool-resolving layer |
| `bin/check-links --layout both` | **not applicable at this layer**: the flag arrives with the sync layer (commit 9) |
| the changed-file list equal to section 4 | by reading (section 2) |
| PR2b row: `conflicts-after-merge` reads 0 | `conflicts-after-merge.sh` is fixed on `pr2/candidate`, so it cannot measure this branch; its method (merge-tree, empty attribute tree) is `pr2b-layer-measure.py` section 5. **With `upstream/main`: exit 0**, tree `49aa4f2b0719`, equal to the layer's own tree; `upstream/main` is an ancestor; the branch is 3 commits ahead |
| the same merge with #98's head (`65990cda`) | **exit 0, clean**; also clean for the parent and for `upstream/main` alone |
| the same merge with #96's head (`ad5c980f`) | **exit 1, 4 regions in 3 files** (`.quality-gates.json` 2, `bin/tests.sh` 1, `CHANGELOG.md` 1). The parent reads the same 4; `upstream/main` alone against #96 reads 1 (`CHANGELOG.md`): with this repository's attributes on (`CHANGELOG.md merge=union`) that merge is clean, exit 0, and with the empty attribute tree it conflicts, exit 1, measured here, so it is the `merge=union` display gap. So the layer adds 0, and the series carries the 3 regions of the plan's section 2.2 |
| the read-set budget (`context_budget.py --status`) | nothing over budget, exit 0 |
| `.quality-gates.json` after git's auto-merge | the diff against the parent is exactly two thresholds (`tests-sh-passed` 272 to 298, `ratchet-unit-tests` 45 to 81), read in this session, and the ratchet's `--run` above reads them back as the floors |

No threshold was loosened: the two raised floors are exactly what the layer adds.

## 5. What this does not show

1. **The surface** is this machine: clean clones, serial runs, hooks **not armed** (`layer-verify.sh` unsets `core.hooksPath`). That matters more for this layer than for the
   last: the layer *is* the hook, and what ran was Test 37 (the real hook and real git in scratch repositories, in both layouts, with a mutated-copy control for each assertion) and
   the gate `pre-commit-selftest` (the hook's own `--selftest`, read 0), not the hook armed on a commit to this branch. It cannot show Windows, the maintainer's machine or upstream's CI (there is none).
2. **The hook and the ratchet find `methodology/` files; nothing else does yet.** The resolver is embedded in one tool (the ratchet). The hook carries its own logic in shell; the
   other tools' sites are the 122 above. Green here is green for the gate pair, not for a migrated project end to end (that needs the later layers and `bin/migrate-layout`).
3. **Fork-internal references ride along.** 26 of the layer's 1,035 added lines match the scrub regex of `pr2b-layer-measure.py` (`.githooks/pre-commit` 14 of 246, `bin/tests.sh` 4 of 202,
   `starter-kit/quality_ratchet.py` 3 of 192, `tools/test_quality_ratchet.py` 5 of 391, the other two files 0; rough, and saved this time, not typed inline as in layer 2). Test 37's
   own title carries a backlog id and plan labels. The plan puts the scrub in its own commit later in the series (the candidate's commit 26), so the layer carries them. The message's own opening, "Part 2, layer 2", is the
   candidate's numbering (this is PR2b's third layer); layer 2's message says "Part 2, layer 1" the same way.
4. **PR3's table and PR4's text** are not re-run (the plan's PR2b row says they are, after all layers).
5. **The gate floors will move again.** They are exact for this layer; every later layer re-derives them (tighten only).

## 6. Next

**Commit 4** of the candidate, `c8c0b213` (the ratchet 1.5.0: a gate that outlives its budget is unmeasured and its command is stopped with its whole process group; 4 files by `git show --numstat`, read this session:
`.quality-gates.json`, `starter-kit/quality-gates.json`, `starter-kit/quality_ratchet.py`, `tools/test_quality_ratchet.py`), which the sizing found applies with no conflict; then **commit 5** by reading (the layout hunks of the trimmer, the only new judgment). One layer per session, a
claim first. Re-run this layer: fetch `pr2b/candidate` into a scratch `--no-local` clone, run `docs/planning/pr-composition-evidence/layer-verify.sh <clone> <commit>` (5 min 16 s here,
13 gates; the fork's 24-gate run is 20 to 30 minutes) and `python3 -I docs/planning/pr-composition-evidence/pr2b-layer-measure.py <repo> <commit> upstream/main <the open PRs' heads>`.
The saved measurement was run with `upstream/main`, `65990cda6afdff7242a63b6a47dd5a2eb120b55a` (#98) and `ad5c980f345758df3dae8276e778c0883ded833c` (#96).
