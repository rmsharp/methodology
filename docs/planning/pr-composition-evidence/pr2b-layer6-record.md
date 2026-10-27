# PR2b layer 6: context_budget.py 1.4.0, the budget gate finds its config at the root or under `methodology/`, on `upstream/main` (S382, 2026-10-27)

**Status: BUILT and verified, local, un-pushed, nothing sent to `KJ5HST/methodology`.** This is the sixth checkpoint of PR2b
(`../upstream-pr-composition-plan.md` section 5, the PR2b row; layers 1 to 5 are `pr2b-layer1-record.md` to `pr2b-layer5-record.md`). Every figure is
printed by a script here or by a command named beside it; the saved outputs are `pr2b-layer6-verify-output.txt` (the clean-clone run) and
`pr2b-layer6-measure-output.txt` (the scanner on the parent and on the commit, the scrub count, and the merges with `upstream/main` and the open pull requests' heads).
What I read from files and what a command measured are labelled.

## 1. The answer first

1. **The layer exists.** Branch `pr2b/candidate` (a local ref with no upstream, so a bare `git push` cannot send it) now has six commits on `upstream/main`
   `d50ce290`: layers 1 to 5 (`fbcef390`, `41a1e580`, `7d87cb2b`, `1d93579a`, `62680cd2`, unchanged, ancestors) and layer 6 `f767ced0` (tree `d225c95a`): **4 files, +356 / -22**,
   built in a scratch `--no-local` clone and fetched here (fast-forward only, after the verification). `pr2/candidate` (`3cba1e50`) is kept as it was.
2. **It applied cleanly, and nothing was re-judged.** `git cherry-pick -x e9c5cb86` onto `62680cd2` exited 0 (git said `Auto-merging .quality-gates.json`, a three-way merge with no marker). For all four files
   the replayed hunks are **equal to the original commit's** by `git patch-id --stable` (measured per file: `starter-kit/context_budget.py` `1dd536ca7449`, `tools/test_context_budget.py` `d89e8d56afa6`,
   `tools/test_layout_resolver.py` `9c2a5bb5699d`, `.quality-gates.json` `950b74cef21d`). Layer 5 needed three judgments; this one needed none.
3. **No version collision.** The tool goes 1.3.1 to 1.4.0. `upstream/main`, the parent, **#98's head (`65990cda`) and #96's head (`ad5c980f`) all read `VERSION = "1.3.1"`** (measured with `git show <ref>:starter-kit/context_budget.py`), and
   neither open pull request changes `context_budget.py` or its tests (`git diff --stat upstream/main <head>` on both files is empty for each). Layer 5's lesson was to compare a number with every open head; this is that comparison, done before building.
4. **The replayed message's figures all held**, so none was changed: the tool +146 / -18, "163, from 148" tests, the floor 148 to 163, four files. (The same re-check changed six figures at layer 5.) Measured: `Ran 163 tests` against the parent's `Ran 148`, 2 skipped in each; `git diff --numstat`, final.
5. **It is green in a clean clone** (section 4): the quality ratchet **13/13 pass, 0 fail, 0 unmeasured**, every measured value equal to its floor (163 is the new exact one; 298, 354, 265, 120 and 74 unchanged and exact);
   the shell suite run directly: **298 passed, 0 failed, 0 skipped**. One verification only: the commit verified is the commit kept.
6. **My claim-time expectations, scored** (written to a file at 15:30:36, before any output was read). E1 the scanner falls from 101 to 93: **confirmed, 93** (`starter-kit/context_budget.py` 8 to 0, acknowledged 0 to 4).
   E2 the ratchet 13/13 with the floor exact: **confirmed**. E3 `bin/tests.sh` 298/0/0: **confirmed**. E4 clean with `upstream/main`, tree equal to the layer's own: **confirmed** (`d225c95a9a26`). E5 the same 5 regions with #98's head, none added: **confirmed**.
   E6 the same 4 regions with #96's head: **confirmed**. E7 no version collision: **confirmed**. Seven of seven; I did not predict that the next commits would apply differently on this tip (item 7).
7. **A finding for the grouping plan: the later commits' conflicts are order, not substance.** Applied alone (not in order) with `git merge-tree --write-tree --merge-base=<c>^`, commit 7 (`dd581fed`, the dashboard) **conflicted onto layer 5's tip** (`tools/test_layout_resolver.py`)
   and is **clean onto this tip** (exit 0), because this layer appended to the layout suite's lists that commit 7 appends to. Commit 8 (`4c0bdded`) clean; 9 (`261b8d36`) conflicts in `tools/test_layout_resolver.py` (alone, on either tip);
   10 (`0aa1897e`) in `.quality-gates.json`; 11 (`a459b8bb`) in `tools/test_layout_resolver.py`; 12 (`505541c3`) in `.quality-gates.json`, `bin/tests.sh` and `tools/test_layout_resolver.py`; 13 and 14 clean. **Whether 9 to 12 conflict when applied after 7 and 8, in order, is unmeasured:**
   the old candidate was built in this order, so I expect each list conflict to vanish, and that is an estimate.

## 2. What it carries

| File | Change | Why it is in the layer |
|---|---|---|
| `starter-kit/context_budget.py` | +146 / -18 (1.3.1 to 1.4.0) | by the commit's message: the history file lives beside the config; the pre-commit gate reads HEAD's own declaration of the class wherever HEAD kept it (root or `methodology/`); the installed hook names the tool and its twin; the project root is found by the layout resolver the tool now embeds; a repository that is itself called `methodology` stays its own project; a tree holding both configs is decided by the framework anchor or refused naming both |
| `tools/test_context_budget.py` | +206 / -1 | 163 tests (148 before) |
| `tools/test_layout_resolver.py` | +3 / -2 | the budget gate joins the layout suite's lists of embedding tools (`COPIES`) and tools held at zero sites (`RESOLVED`) |
| `.quality-gates.json` | +1 / -1 | `context-budget-unit-tests` 148 to 163, the measured count |

**By reading** the plan's sections 1 and 4: none of the four is in section 4's "Not carried" column. By `git diff --name-only parent commit`: exactly these four, nothing else.

## 3. The scanner on this tree (the to-do list, not a failure)

`python3 -I bin/check-layout-literals` reads **93 sites (70 path, 23 text) over 5 files**, exit 1, on the commit; on the parent it read 101 (73, 28). The only file whose count moved is `starter-kit/context_budget.py`, **8 to 0**, and its acknowledged sites go 0 to 4
(total acknowledged 27 to 31). The remaining files, unchanged: `bin/check-handoff` 6, `bin/check-ledger` 4, `bin/check-links` 1, `bin/status` 3, `starter-kit/methodology_dashboard.py` 79. "Prose not counted" 172 to 172.
The crude check of section 3b of the measure output says 6 of the parent's 8 site lines no longer appear verbatim: that is rewriting, and the count is the scanner's.

## 4. The checks of the PR2 row, and which of them apply here

Clean `--no-local` clone, serial, `layer-verify.sh` (15:30:15 to 15:38:23, **8 min 8 s**) and then `bash bin/tests.sh` directly (15:38:23 to 15:43:16, **4 min 53 s**); the verified commit was `f767ced0`.

| Check (plan section 5, PR2 row) | Result |
|---|---|
| `quality_ratchet.py --run` (`pr2b-layer6-verify-output.txt`, Part 1) | **13/13 pass, 0 fail, 0 unmeasured**; results `c25f6c576af3`, manifest `fc7d26b688ff`. Measured against floors: `tests-sh-passed` 298/298, `dashboard-unit-tests` 354/354, `context-budget-unit-tests` 163/163, `trimmer-unit-tests` 265/265, `ratchet-unit-tests` 120/120, `layout-unit-tests` 74/74; the seven zero-gates read 0 |
| `bash bin/tests.sh` run directly (Part 2) | **298 passed, 0 failed, 0 skipped**, exit 0 |
| the cheap suites, run first in the build clone | `python3 -I -B tools/test_layout_resolver.py`: 74 tests OK in 1.47 s (the parent 74, 1.44 s). `python3 -I -B tools/test_context_budget.py`: 163 tests OK, 2 skipped, 9.3 s (the parent 148, 2 skipped, 6.9 s). I did not look for the cause of the extra seconds and make no claim |
| every shipped `.verify.sh` exit histogram equal to upstream's | one tracked proof (`docs/archive/CHANGELOG-through-2026-09-30.md.verify.sh`): exit 0. **Also `--reverify` of that shard: OK, exit 0** (Part 3). This layer does not change the trimmer, so that run shows it left it working |
| `bin/check-layout-literals` | applicable now: **93 sites, a to-do list** (section 3); the row's 0 is for the last tool-resolving layer |
| `bin/check-links --layout both` | **not applicable at this layer**: the flag arrives with the sync layer (commit 9) |
| the changed-file list equal to section 2 | by reading (section 2) and by `git diff --numstat` in Part 1 and in the measure output |
| PR2b row: `conflicts-after-merge` reads 0 | `conflicts-after-merge.sh` is fixed on `pr2/candidate`, so it cannot measure this branch; the method is `pr2b-layer-measure.py` section 5. **With `upstream/main`: exit 0**, tree `d225c95a9a26`, equal to the layer's own; the branch is 6 commits ahead |
| the same merge with #98's head (`65990cda`) | **exit 1, 5 regions in 3 files** (`.quality-gates.json` 1, `starter-kit/methodology_trim.py` 3, `tools/test_methodology_trim.py` 1): **identical to the parent**, so this layer adds 0; `upstream/main` alone with #98 is clean |
| the same merge with #96's head (`ad5c980f`) | **exit 1, 4 regions in 3 files** (`.quality-gates.json` 2, `bin/tests.sh` 1, `CHANGELOG.md` 1), identical to the parent; `upstream/main` alone reads 1 (`CHANGELOG.md`), the `merge=union` display gap. So the layer adds 0 |
| the read-set budget (`context_budget.py --status`, run by `layer-verify.sh`) | nothing over budget, exit 0 |
| `.quality-gates.json` after the replay | the diff against the parent is exactly one threshold (`context-budget-unit-tests` 148 to 163), read in this session, and `--run` above reads it back as the floor |

No threshold was loosened: the one raised floor is exactly the count of the tests the layer carries.

## 5. The two open pull requests

Measured in section 4 and item 3 of section 1. **#98:** this layer adds no region, so the series against #98's head stays at layer 5's 5 regions in 3 files, all in the trimmer, its tests and the gates file; **#98 does not touch this layer's files**, and the version 1.4.0
is free there. **#96:** the series against #96's head stays at 4 regions in 3 files, the same as at layer 3. Neither pull request changes the tool this layer carries, so nothing here depends on his stack-or-supersede answer at PR5 (plan lines 226 to 227).

## 6. What this does not show

1. **The surface** is this machine: clean clones, serial runs, hooks **not armed** (`layer-verify.sh` unsets `core.hooksPath`). The budget gate was run on fixture trees the tests build in both layouts and on this repository's own config;
   **no real project with its config under `methodology/` was run**, no adopter was run (PR3's table is not re-run; the plan says it is, after all layers), and Windows is untried.
2. **The installed pre-commit hook is the part with the least reach.** The commit says the hook now names the tool and its twin; the suite and `--selftest` exercise it in a fixture. Whether a real adopter's hook installs and refuses as described is not shown here.
3. **Fork-internal references ride along.** 4 of the layer's 356 added lines match the scrub regex of `pr2b-layer-measure.py` (`starter-kit/context_budget.py` 2 of 146, `tools/test_context_budget.py` 2 of 206; rough, section 4 of the measure output): the version comment
   (`1.4.0: BL-101 P4 -- ...`) and docstrings that cite `plan 7.2b`, `C9` and a session's picker. The plan puts the scrub in its own commit later in the series, so the layer carries them. The message itself carries none beyond "Part 2, layer 4", the old candidate's own name for this layer.
4. **The regions against #98 and #96 are counted, not read** (section 4); this layer adds none, so nothing new was left unread.
5. **Item 7 of section 1 is alone-not-in-order.** A conflict that reads exit 1 alone may vanish in order, and one that reads exit 0 alone may conflict after another commit lands; I applied none of commits 7 to 14.
6. **The gate floors will move again.** They are exact for this layer; every later layer re-derives them (tighten only).

## 7. Next

**Commit 7 onward** of the candidate: 27 commits remain (7 to 33; 34 is dropped as superseded). Commit 7 (`dd581fed`, the dashboard 2.22.0, 5 files) now applies alone with no conflict and is the natural next layer; 8 (`4c0bdded`, `bin/tests.sh`, 3 / 1) is clean alone and pairs with it
in the sizing's grouping (7+8). He ticked "Group commits 6-33 after layer 5" at the S381 picker; grouping is a plan edit for a later session, and a group is still verified at its boundary (gate (c) of `SESSION_RUNNER.md` §Vertical Slice Sessions), so grouping saves orientation and close-out, not verification time (8 min plus 5 here).
Re-run this layer: fetch `pr2b/candidate` into a scratch `--no-local` clone, run `docs/planning/pr-composition-evidence/layer-verify.sh <clone> <commit>` and
`python3 -I docs/planning/pr-composition-evidence/pr2b-layer-measure.py <repo> <commit> upstream/main <the open PRs' heads>`. The saved measurement was run with `upstream/main`,
`65990cda6afdff7242a63b6a47dd5a2eb120b55a` (#98) and `ad5c980f345758df3dae8276e778c0883ded833c` (#96). Run the two cheap suites first (`tools/test_layout_resolver.py`, 1.5 s; the layer's own unit suite).
