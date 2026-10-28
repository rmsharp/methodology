# PR2b layer 13: the operating files say where the methodology files sit, on `upstream/main` (S389, 2026-10-28)

**Status: BUILT, verified in a clean clone, and RED on one line: the read-set budget (exit 2). Local, un-pushed to `KJ5HST/methodology`, nothing sent there.** This is the thirteenth checkpoint of PR2b
(`../upstream-pr-composition-plan.md` section 5, the PR2b row; layers 1 to 12 are `pr2b-layer1-record.md` to `pr2b-layer12-record.md`). Every figure is printed by a script here or by a command named beside it.
The saved outputs are `pr2b-layer13-verify-output.txt` (the clean-clone run, four parts), `pr2b-layer13-measure-output.txt` (the scanner on the parent and on the commit, the scrub count, the merges with `upstream/main` and the open pull requests' heads),
`pr2b-layer13-next-alone-output.txt` (commits 14 to 20, each applied alone onto this tip), `pr2b-layer13-check-links-both-output.txt` (the 31 dangling links), `pr2b-layer13-budget-probe-output.txt` (the budget red and the probe of its fix)
and `pr2b-layer13-expectations.txt` (fourteen expectations, written **before** the cherry-pick and **kept as written**; its modification time, 11:11:48, is earlier than the cherry-pick's 11:11:55).

## 1. The answer first

1. **The layer exists.** Branch `pr2b/candidate` (a local ref with no upstream, so a bare `git push` cannot send it) now has thirteen commits on `upstream/main` `d50ce290`: layers 1 to 12 (unchanged, ancestors; layer 12 is `19a5769b`) and layer 13 `09ac2846` (tree `6f1718e3`):
   **5 files, +48 / -27**, built in a scratch `--no-local` clone and fetched here (fast-forward only, after the verification, with the parent checked equal to the old tip first). `pr2/candidate` (`3cba1e50`) is kept as it was.
2. **It applied cleanly, and nothing was re-judged.** `git cherry-pick -x c8d43754` onto `19a5769b` exited 0. The replayed commit is **equal to the original by `git patch-id --stable`** (`3d29026203bb` for both),
   and `git diff --numstat` is the original's: `30 12 starter-kit/BOOTSTRAP.md`, `3 2 starter-kit/CLAUDE_TEMPLATE.md`, `1 1 starter-kit/HANDOFFS.md`, `1 1 starter-kit/SAFEGUARDS.md`, `13 11 starter-kit/SESSION_RUNNER.md`.
3. **It is green on everything the plan's PR2 row names, in a clean clone** (section 4): the quality ratchet **16/16 pass, 0 fail, 0 unmeasured**, results `6e788a952599` and manifest `d0e1c782db6e` (both **equal to layer 12's**: the commit adds no gate and moves no measured value);
   the shell suite run directly **300 passed, 0 failed, 0 skipped** with Test 15 `(30 == 30)`; the scanner `scanned 14 files; 0 sites (0 path, 0 text); 124 acknowledged; 189 prose not counted`; the shard's `--reverify` exit 0; the tracked proof exit 0.
4. **It is RED on the read-set budget.** `python3 starter-kit/context_budget.py --status` exits **2**: `starter-kit/SESSION_RUNNER.md - about 18,921 tokens exceeds the 18,900-token ceiling by 21 - at 2.8107 B/token (measured)`.
   The commit adds 345 B to the runner (52,839 B to 53,184 B); at the tool's density that is 18,799 tokens before (my arithmetic: 52,839 / 2.8107, 101 under the ceiling, which the "ok" row did not print) and 18,921 after. The ratchet's 16 gates and the shell suite do not read this tool, so they stay green; **the budget is a line `layer-verify.sh` prints with the criterion "budget exit 0", not a check the PR2 row names.**
5. **The series already knows this red and fixes it late.** Its own commit `ced2c823` (number 31 of the 34 on `pr2/candidate`: "drop the layout paragraph's duplicate example command; the runner reads under its ceiling again", 2 files: `.context-budget.json` 3/3, `starter-kit/SESSION_RUNNER.md` 1/1) is the cure, and its message says the runner "before the cut read 18,911.5 tokens, 11.5 over" by the doubled-read measure (the tool's own estimate says 21 over; both are over).
   **I probed it** (`pr2b-layer13-budget-probe-output.txt`): `ced2c823` alone onto this tip is clean (`git merge-tree` exit 0), cherry-picks with exit 0, and the budget then reads `53,100 B ... ok`, `nothing over budget`, exit 0. The probe ran the budget only; no suite or ratchet was run on it. The runner file at commit 13 on `pr2/candidate` is byte-identical to this build's (`git diff --stat c8d43754 HEAD -- starter-kit/SESSION_RUNNER.md .context-budget.json` was empty), so the original series was over its ceiling at commit 13 too.
6. **What that means for the next 17 layers is a decision of his, not mine** (section 7): left in the series' order, every layer from 13 to 30 prints `budget exit 2`; moved to follow this layer, each prints 0. I advanced the local branch to this layer anyway because the replay is exact, every check the PR2 row names passes, and the branch is local and resettable (`git branch -f pr2b/candidate 19a5769b`).
7. **My claim-time expectations, scored** (fourteen). E1 the cherry-pick exits 0: **confirmed**. E2 patch-id equal: **confirmed**. E3 the five numstat pairs: **confirmed**. E4 layout suite 76, checker 11, sync 82, dashboard 395: **confirmed** (2 s, 1 s, 35 s, 45 s; the build clone stayed clean).
   E5 ratchet 16/16, every floor met, **both digests equal to layer 12's**: **confirmed** (the digest half I had marked least sure). E6 `bash bin/tests.sh` 300/0/0 and Test 15 `30 == 30`: **confirmed**. E7 the scanner's summary line exactly: **confirmed**. E10 clean with `upstream/main`, tree equal to the layer's own, 5 regions with #98's head and 4 with #96's, 0 added: **confirmed**, including the reason (#96's two insertions sit 17 and 70 or more lines from this commit's hunks). E11 the scrub matches 0 to 3 of 48 added lines: **confirmed at the low edge**, 0 of 48.
   E12 the commits alone onto this tip: **confirmed**, 14 to 18 and 20 clean, 19 (`ab35e965`) conflicts in `.quality-gates.json`, the layer 12 verdicts. E14 (the fork's own 24 gates at close-out) is scored in the close-out receipt.
   **E8 was wrong in its verdict.** I predicted `budget exit 0, nothing over budget` and a runner growth of 500 to 2,500 B. The growth was 345 B, smaller than I said, and it crossed anyway: I read the budget at the tip, saw `ok`, and did not turn 52,839 B into tokens before predicting (101 tokens of headroom). Its second half held: the shard's `--reverify` exit 0 and the tracked proof exit 0.
   **E9 was half wrong.** Right: `check-links` with no flag and with `--layout legacy` exit 0 (111 links in 23 files, down from 116), and `--layout new` and `--layout both` exit 1 with **31** dangling links (35 before). Wrong: I said 12 or 13 files; it is **10**, because `methodology/BOOTSTRAP.md`, `methodology/HANDOFFS.md` and `methodology/SESSION_RUNNER.md` left the list entirely (checked by running the same count over layer 12's saved list: 35 links in 13 files).
   **E13 fell just outside its range:** the ratchet part took 9 min 27 s (predicted 10 to 14) and `bin/tests.sh` 5 min 53 s (predicted 6 to 8), at a load average of 2.7 before the launch and 6.3 half a minute in.

## 2. What it carries

| File | Change | Why it is in the layer |
|---|---|---|
| `starter-kit/SESSION_RUNNER.md` | +13 / -11 | opens with where the files are (bare names found beside the runner; the legacy and half-moved cases; the `methodology/` prefix for a migrated project); references that held only in the legacy layout become bare names |
| `starter-kit/BOOTSTRAP.md` | +30 / -12 | a "Two layouts" section (what each is, what `bin/sync --layout` does with each, how a project moves, that the guide's commands are written for the legacy layout); the steps that name a directory or command say what changes |
| `starter-kit/CLAUDE_TEMPLATE.md` | +3 / -2 | says where the runner and the extracted learnings file sit in a migrated project |
| `starter-kit/HANDOFFS.md`, `starter-kit/SAFEGUARDS.md` | +1 / -1 each | a reference that held only in the legacy layout |

Read from the commit's own message and `git show --stat c8d43754`; the figures come from the commands in section 4. The commit message's own claim, "31 dangling links after, 35 before; the legacy layout reads none", **held** (31 and 35 measured; legacy reads none).

## 3. The scanner

`pr2b-layer13-measure-output.txt` section 3: parent `19a5769b` **14 files, 0 sites, 124 acknowledged**; commit **14 files, 0 sites, 124 acknowledged**; sites and acknowledged per file: none differ. The commit edits no scanned file.

## 4. Verification in a clean clone

`pr2b-layer-driver.sh 13` (unchanged since S386), serial, hooks not armed, on `09ac2846`: Part 1 11:14:47 to 11:24:14, Part 2 to 11:30:07, done 11:30:08 (15 min 21 s in all).

| Check | Result |
|---|---|
| quality ratchet `--run` | 16/16 pass, 0 fail, 0 unmeasured, results `6e788a952599`, manifest `d0e1c782db6e` (both equal to layer 12's) |
| each gate against its floor | every value equal to its floor, as at layer 12 (`tests-sh-passed` 300, `dashboard-unit-tests` 395, `layout-unit-tests` 76, `checker-layout-unit-tests` 11, `sync-layout-unit-tests` 82, `layout-literals` 0, the rest 0) |
| scanner | 14 files, 0 sites, 124 acknowledged |
| **read-set budget** | **exit 2: the runner about 18,921 tokens against 18,900** (the one red line; section 1 items 4 to 6) |
| tracked proof `docs/archive/CHANGELOG-through-2026-09-30.md.verify.sh` | exit 0 |
| `bash bin/tests.sh` | 300 passed, 0 failed, 0 skipped |
| `--reverify` on that shard | exit 0 |
| `check-links` (no flag) and `--layout legacy` | exit 0, 111 links in 23 files |
| `check-links --layout new` and `both` | exit 1, **31 dangling links in 10 files** (35 in 13 before) |
| cheap suites in the build clone | layout 76, checker 11, sync 82, dashboard 395, all OK |

## 5. The two open pull requests

Measured in `pr2b-layer13-measure-output.txt` section 5 (merge-tree with the empty attribute tree, GitHub's view), heads read from GitHub at this session: #98 `65990cda`, #96 `ad5c980f`. **#98:** exit 1, **5 regions in 3 files** (`.quality-gates.json` 1, `starter-kit/methodology_trim.py` 3, `tools/test_methodology_trim.py` 1), **identical to the parent's**. **#96:** exit 1, **4 regions in 3 files** (`.quality-gates.json` 2, `CHANGELOG.md` 1, `bin/tests.sh` 1), identical to the parent's. The layer adds 0 regions to either.
**This commit edits two files #96 also edits** (`git diff --numstat upstream/main <head> -- <the five files>` from the repository root, `.quality-gates.json` as the positive control: #98 `1 1` on `.quality-gates.json` only; #96 `9 2` there, `9 0` on `starter-kit/BOOTSTRAP.md` and `1 0` on `starter-kit/SAFEGUARDS.md`). They did not clash: #96's insertions come after old lines 344 (BOOTSTRAP.md) and 179 (SAFEGUARDS.md); the commit's hunks in BOOTSTRAP.md run from old line 38 to 423 and the nearest to 344 are 327 and 381 (17 and 37 lines away), and its one hunk in SAFEGUARDS.md is at old line 108 (71 lines away). The count of regions is measured; **their lengths are not.**

## 6. What this does not show

1. **The surface** is this machine: clean clones, serial runs, hooks **not armed** (`layer-verify.sh` unsets `core.hooksPath`). Windows is untried and no adopter was run (PR3's table is not re-run; the plan says it is, after all layers).
2. **The runner's token count is the tool's estimate** at the config's recorded density (2.8107 B/token, measured on an earlier blob), not a doubled-read measure; I did not run one. The series' own commit message gives the doubled-read figure (11.5 over). Both say over; the size of the excess differs.
3. **The probe of `ced2c823` is a budget reading only.** No suite and no ratchet was run on the probed tree, and I did not apply commits 14 to 30 after a reorder. What I did read (`git log upstream/main..pr2/candidate -- <path>`): only commits 13 and 31 edit `starter-kit/SESSION_RUNNER.md`, and only 31 edits `.context-budget.json`, so a reorder cannot clash with 14 to 30 on those two files; a later commit that touches a file 31 also touches is not excluded by that reading.
4. **The region lengths** in section 5, and **the forecast that 19 clears once 17 is in**, are not measured.
5. **Layers 14 to 33 are untested here.** Nothing in this record claims anything about them beyond the merge-tree verdicts of section 7, which are estimates.

## 7. Next

**Commit 14 onward** of the candidate: 20 commits remain (14 to 33; 34 is dropped as superseded). **The decision this layer hands him:** the runner budget is red from here to commit 31 in the series' order. Options, none taken: (a) keep the order and print the red on every layer from 13 to 30 (one sentence in each record); (b) **move `ced2c823` to follow this layer** (both commits stay verbatim, patch-ids unchanged; it is the series' own cure; it needs re-measuring against 14 to 30 and is a plan edit nobody has made); (c) fold its two hunks into commit 13 (a judgment edit; the replay would stop being equal to the original). I would take (b), tested by the same alone-onto-tip measurement. It is a planning step, so it fits the "grouping plan for commits 13 to 33" candidate.
**The next commits alone, measured here** (`pr2b-layer13-next-alone-output.txt`): clean: 14 (`04918ce3`), 15 (`23e6e66a`), 16 (`0248ebf2`), 17 (`18cda0f2`), 18 (`2942e46c`), 20 (`5afc9621`); conflicting: 19 (`ab35e965`, `.quality-gates.json`). Alone, not in order. Commit 14 edits `FRAMEWORK_APPARATUS.md`, `HOW_TO_USE.md`, `ITERATIVE_METHODOLOGY.md`, `starter-kit/CHANGELOG.md` and `RECOMMENDED_SKILLS.md`, none of which commit 13 touches.
Re-run this layer: fetch `pr2b/candidate` into a scratch `--no-local` clone (a branch at layer 13's tip), then
`nohup bash docs/planning/pr-composition-evidence/pr2b-layer-driver.sh 13 <repo> <build clone> <clean clone> <output file> <done file> &`, and
`python3 -I docs/planning/pr-composition-evidence/pr2b-layer-measure.py <repo> <commit> upstream/main <the open PRs' heads>` **from the repository root** with the heads as full SHAs: the saved measurement used `upstream/main`,
`65990cda6afdff7242a63b6a47dd5a2eb120b55a` (#98) and `ad5c980f345758df3dae8276e778c0883ded833c` (#96). The next commits alone: `bash docs/planning/pr-composition-evidence/pr2b-next-alone.sh <repo> pr2b/candidate 14 20`.
Run the cheap suites first (`tools/test_layout_resolver.py`, 2 s; `tools/test_checker_layouts.py`, 1 s; `tools/test_sync_layouts.py`, 35 s; `tools/test_methodology_dashboard.py`, 45 s), read `python3 starter-kit/context_budget.py --status` at the tip **before** predicting and turn the runner's bytes into tokens (bytes / 2.8107), and `cd` to the repository before any `git diff -- <path>`.
