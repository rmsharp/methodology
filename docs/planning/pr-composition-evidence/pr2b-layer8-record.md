# PR2b layer 8: Test 15 counts the status table's rows, on `upstream/main` (S384, 2026-10-27)

**Status: BUILT and verified, local, un-pushed to `KJ5HST/methodology`, nothing sent there.** This is the eighth checkpoint of PR2b
(`../upstream-pr-composition-plan.md` section 5, the PR2b row; layers 1 to 7 are `pr2b-layer1-record.md` to `pr2b-layer7-record.md`). Every figure is
printed by a script here or by a command named beside it; the saved outputs are `pr2b-layer8-verify-output.txt` (the clean-clone run),
`pr2b-layer8-measure-output.txt` (the scanner on the parent and on the commit, the scrub count, and the merges with `upstream/main` and the open pull requests' heads) and
`pr2b-layer8-next-alone-output.txt` (the next eleven candidate commits, each applied alone onto this tip). What I read from files and what a command measured are labelled.

## 1. The answer first

1. **The layer exists.** Branch `pr2b/candidate` (a local ref with no upstream, so a bare `git push` cannot send it) now has eight commits on `upstream/main`
   `d50ce290`: layers 1 to 7 (`fbcef390`, `41a1e580`, `7d87cb2b`, `1d93579a`, `62680cd2`, `f767ced0`, `e5210601`, unchanged, ancestors) and layer 8 `07ec025b` (tree `651fa70a`): **1 file, +3 / -1**,
   built in a scratch `--no-local` clone and fetched here (fast-forward only, after the verification). `pr2/candidate` (`3cba1e50`) is kept as it was.
2. **It applied cleanly, and nothing was re-judged.** `git cherry-pick -x 4c0bdded` onto `e5210601` exited 0. The one file's replayed hunk is **equal to the original commit's** by `git patch-id --stable`
   (`a62bf095f030` for both). `git diff --numstat` is `3 1 bin/tests.sh`, the same as the original.
3. **No version to collide with.** The file is a shell test script; it carries no version number, and neither open pull request touches `bin/tests.sh` near the change
   (`git diff -U0 upstream/main 65990cda -- bin/tests.sh` is empty; #96's head adds one hunk of 7 lines at upstream's line 265, about 40 lines below Test 15 at line 225 of the candidate). That comparison was made before building.
4. **The replayed message's figures held**, so none was changed. It says the test "passes on today's bin/status unchanged (298 passed, 0 failed, 0 skipped)": measured, **298 passed, 0 failed, 0 skipped**, and Test 15's own line reads
   `PASS: status: one row per manifest file (30 == 30)` (`pr2b-layer8-verify-output.txt:107`).
5. **It is green in a clean clone** (section 4): the quality ratchet **13/13 pass, 0 fail, 0 unmeasured**, every measured value equal to its floor and **no floor changed** (298, 395, 163, 265, 120 and 75 as at layer 7);
   the shell suite run directly: **298 passed, 0 failed, 0 skipped**. One verification only: the commit verified is the commit kept.
6. **My claim-time expectations, scored** (eleven, written to a file at 17:49:36 CDT, before the cherry-pick and before any output was read). E1 the cherry-pick exits 0: **confirmed**. E2 the hunk equals the original's: **confirmed**.
   E3 numstat `3 1`: **confirmed**. E4 the layout suite still 75 and the dashboard suite still 395: **confirmed**. E5 the ratchet 13/13 with every floor unchanged and exact: **confirmed**. E6 `bin/tests.sh` 298/0/0 and Test 15's count equal to the manifest's: **confirmed**.
   E7 the scanner still 14 sites, 0 moved: **confirmed** (section 3). E8 clean with `upstream/main`, tree equal to the layer's own: **confirmed** (`651fa70a1608`). E9 the same 5 regions with #98's head: **confirmed**. E10 the same 4 regions with #96's head: **confirmed**.
   E11 the scrub regex matches nothing: **confirmed, but my count was wrong**: I wrote "4 added lines" and the commit adds **3** (`+3`), so the measure reads 0 of 3. Eleven of eleven on the outcomes, one slip in a number I typed from memory. What I did not predict is in item 7.
7. **Findings for the grouping plan.** (a) **Layer 8 has an order dependency on commit 9, and it is measured, not read.** In a probe clone (this tip plus `261b8d36`, cherry-pick exit 0), a project synced with `bin/sync --mode=commit` and read with that commit's `bin/status` prints a `layout: <name>  legacy`
   line above the table, and Test 15's two counts over that output are: **the old assertion 31, the new one 30, for 30 manifest entries** (command and output in section 6, item 2). So the sync layer without this commit would fail Test 15 (31 != 30), and this commit before it passes both ways. Apply 8 before 9, or in the same layer.
   (b) **Nothing else moved.** The next eleven commits applied alone onto the new tip (`pr2b-layer8-next-alone-output.txt`) read exactly as S383 measured them onto layer 7's tip: **9, 10 and 13 to 16 clean; 11 (`tools/test_layout_resolver.py`), 12 (`.quality-gates.json`, `bin/tests.sh`, `tools/test_layout_resolver.py`), 17 (`.quality-gates.json`), 18 (`tools/test_layout_resolver.py`, `tools/test_sync_layouts.py`) and 19 (`.quality-gates.json`, `bin/tests.sh`) conflict alone.**
   Whether any of these survive in order is still unmeasured; the only evidence is that every list conflict so far has vanished once the commits that append to the same lists were in.
   (c) **Neither open pull request touches commit 9's five files** (`bin/_manifest_reader.py`, `bin/check-links`, `bin/status`, `bin/sync`, `tools/test_layout_resolver.py`): `git diff --stat upstream/main <head> -- <the five>` is empty for #98's head and for #96's.

## 2. What it carries

| File | Change | Why it is in the layer |
|---|---|---|
| `bin/tests.sh` | +3 / -1 | Test 15 ("status emits per-file rows with a disposition column") counted every line of `bin/status`'s output that contains the project's directory name, and compares it with the manifest's entry count. It now counts the lines that START with the name followed by a space, which is what a table row is, plus a two-line comment saying why. The commit's own reason: the `layout: <name>  <kind>` line the sync layer adds before the table names the project too and is not a row |

**By reading** the plan's section 4 table: the file is not in the "Not carried" column (`CLAUDE.md`, `README.md`, the ledgers, `docs/`, `close_out_report.py`, the canonical-only checkers). By `git diff --name-only parent commit`: exactly this one file, nothing else.

## 3. The scanner on this tree (the to-do list, not a failure)

`python3 -I bin/check-layout-literals` reads **14 sites (6 path, 8 text) over 4 files**, exit 1, on the commit and on the parent: **no file's count moved and no file's acknowledged count moved** (both "differ" lists in the measure output read `(none differ)`).
The remaining counted sites are `bin/check-handoff` 6, `bin/check-ledger` 4, `bin/check-links` 1, `bin/status` 3; acknowledged 114, prose not counted 187, as at layer 7.

## 4. The checks of the PR2 row, and which of them apply here

Clean `--no-local` clone, serial, `layer-verify.sh` (17:51:49 to 18:01:58, **10 min 9 s**) and then `bash bin/tests.sh` directly (18:01:58 to 18:07:24, **5 min 26 s**); the verified commit was `07ec025b`.
The two parts ran slower than layer 7's (8 min 38 s and 4 min 53 s); nothing else of mine was running, and I do not know why.

| Check (plan section 5, PR2 row) | Result |
|---|---|
| `quality_ratchet.py --run` (`pr2b-layer8-verify-output.txt`, Part 1) | **13/13 pass, 0 fail, 0 unmeasured**; results `7959143a08c1`, manifest `d66cb326a0dd` (both equal to layer 7's). Measured against floors: `tests-sh-passed` 298/298, `dashboard-unit-tests` 395/395, `context-budget-unit-tests` 163/163, `trimmer-unit-tests` 265/265, `ratchet-unit-tests` 120/120, `layout-unit-tests` 75/75; the seven zero-gates read 0 |
| `bash bin/tests.sh` run directly (Part 2) | **298 passed, 0 failed, 0 skipped**, exit 0 |
| the cheap suites, run first in the build clone | `python3 -I -B tools/test_layout_resolver.py`: 75 tests OK in 2.08 s. `python3 -I -B tools/test_methodology_dashboard.py`: 395 tests OK in 82.6 s (layer 7 read 52 s). The commit touches neither file; they are a check that the tip still stands |
| every shipped `.verify.sh` exit histogram equal to upstream's | one tracked proof (`docs/archive/CHANGELOG-through-2026-09-30.md.verify.sh`): exit 0. **Also `--reverify` of that shard: OK, exit 0** (Part 3). This layer does not change the trimmer, so that run shows it left it working |
| `bin/check-layout-literals` | applicable now: **14 sites, a to-do list** (section 3); the row's 0 is for the last tool-resolving layer |
| `bin/check-links --layout both` | **not applicable at this layer**: the flag arrives with the sync layer (commit 9). The `check-links` gate (0 findings) passes |
| the changed-file list equal to section 2 | by reading (section 2) and by `git diff --numstat` in Part 1 and in the measure output |
| PR2b row: `conflicts-after-merge` reads 0 | `conflicts-after-merge.sh` is fixed on `pr2/candidate`, so it cannot measure this branch; the method is `pr2b-layer-measure.py` section 5. **With `upstream/main`: exit 0**, tree `651fa70a1608`, equal to the layer's own (`651fa70a`); the branch is 8 commits ahead |
| the same merge with #98's head (`65990cda`) | **exit 1, 5 regions in 3 files** (`.quality-gates.json` 1, `starter-kit/methodology_trim.py` 3, `tools/test_methodology_trim.py` 1): **identical to the parent**, so this layer adds 0; `upstream/main` alone with #98 is clean |
| the same merge with #96's head (`ad5c980f`) | **exit 1, 4 regions in 3 files** (`.quality-gates.json` 2, `CHANGELOG.md` 1, `bin/tests.sh` 1), identical to the parent; `upstream/main` alone reads 1 (`CHANGELOG.md`), the `merge=union` display gap. So the layer adds 0. **The `bin/tests.sh` region is the one the parent already had**; I did not read it, and the count is the same, so this layer's lines are not in it |
| the read-set budget (`context_budget.py --status`, run by `layer-verify.sh`) | nothing over budget, exit 0 |
| `.quality-gates.json` after the replay | unchanged (the numstat lists one file, `bin/tests.sh`); `--run` above reads every threshold back as the floor |

No threshold was touched.

## 5. The two open pull requests

Measured in section 4 and item 3 of section 1. **#98:** this layer adds no region, so the series against #98's head stays at layer 5's 5 regions in 3 files, all in the trimmer, its tests and the gates file; #98 does not touch `bin/tests.sh`.
**#96:** the series against #96's head stays at 4 regions in 3 files, the same as at layer 3; #96 does touch `bin/tests.sh` (7 lines added, far from Test 15), and the merge-tree count shows this layer did not add a region there.
Neither pull request changes Test 15, so nothing here depends on his stack-or-supersede answer at PR5 (plan lines 226 to 227).

## 6. What this does not show

1. **The surface** is this machine: clean clones, serial runs, hooks **not armed** (`layer-verify.sh` unsets `core.hooksPath`). The only behaviour this layer changes is one assertion in the shell suite; the suite ran, and Test 15 passed on this tip's `bin/status`.
   Windows is untried and no adopter was run (PR3's table is not re-run; the plan says it is, after all layers).
2. **The reason the commit gives was exercised only in a probe, not in the layer.** At this tip `bin/status` prints no `layout:` line, so the layer's run cannot distinguish the old assertion from the new one (both count 30). I checked the reason where it applies: in a scratch clone at this tip plus `261b8d36`
   (commit 9, `git cherry-pick -x` exit 0, not kept), `git init` a temporary project, `bin/sync <p> --mode=commit`, `bin/status <p>`, then Test 15's two counts over that output. The probe read:
   ```
   layout: tmp.rrosWALLv6  legacy
   manifest entries: 30; OLD assertion counts: 31; NEW assertion counts: 30
   ```
   The probe is a hand-run of Test 15's own lines (`bin/tests.sh:216-232` at this tip), not a run of the suite. The commands, in a scratch clone with `core.hooksPath` unset:
   ```
   git checkout -b probe9 origin/pr2b/candidate && git cherry-pick -x 261b8d36        # exit 0
   P="$(mktemp -d)"; git -C "$P" init -q; bin/sync "$P" --mode=commit; OUT="$(bin/status "$P")"
   N="$(basename "$P")"; echo "$OUT" | grep -c "$N"; echo "$OUT" | grep -c "^$N "      # 31, then 30
   python3 -c "import sys; sys.path.insert(0,'bin'); import _manifest; print(len(_manifest.DISTRIBUTION))"   # 30
   ```
   Only the two result lines above are saved as output; the rest is this paragraph. At the sync layer the full suite will exercise it for real.
3. **Layer 9 is untested here:** the probe's cherry-pick of commit 9 lives in a scratch clone and is not on the branch, so nothing about commit 9's own suite is claimed.
4. **A slip in my own expectations** (item 6 of section 1): the count of added lines, typed from memory (4 for 3). The outcome it was attached to held.

## 7. Next

**Commit 9 onward** of the candidate: 25 commits remain (9 to 33; 34 is dropped as superseded). Commit 9 (`261b8d36`, `feat(sync): bin/sync, bin/status, bin/check-links and the manifest reader find a project's ...`) is 5 files by `git show --numstat` (`bin/_manifest_reader.py` 65/7, `bin/check-links` 150/47, `bin/status` 85/21, `bin/sync` 145/32,
`tools/test_layout_resolver.py` 2/1), clean alone on this tip (exit 0), and neither open head touches any of the five (section 1, item 7c). Its pair in the sizing, commit 10 (`0aa1897e`, 5 files, `tools/test_sync_layouts.py` +986), is clean alone too. The sync layer is where the scanner's `bin/status` and `bin/check-links` sites should fall; expect the `check-links --layout both` row to apply for the first time.
He ticked "Group commits 6-33 after layer 5" at the S381 picker; grouping is a plan edit for a later session, and a group is still verified at its boundary (gate (c) of `SESSION_RUNNER.md` §Vertical Slice Sessions), so grouping saves orientation and close-out, not verification time (10 min plus 5.5 min here).
Re-run this layer: fetch `pr2b/candidate` into a scratch `--no-local` clone, run `docs/planning/pr-composition-evidence/layer-verify.sh <clone> <commit>` and
`python3 -I docs/planning/pr-composition-evidence/pr2b-layer-measure.py <repo> <commit> upstream/main <the open PRs' heads>`. The saved measurement was run with `upstream/main`,
`65990cda6afdff7242a63b6a47dd5a2eb120b55a` (#98) and `ad5c980f345758df3dae8276e778c0883ded833c` (#96). Run the two cheap suites first (`tools/test_layout_resolver.py`, 2 s; `tools/test_methodology_dashboard.py`, 52 to 83 s).
