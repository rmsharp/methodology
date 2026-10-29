# PR2b layer 22: the documentation group, eight commits on `upstream/main` (S394, 2026-10-29)

**Status: BUILT and verified in a clean clone, green on every line the plan's PR2 row names and on the read-set budget. Local, un-pushed to `KJ5HST/methodology`, nothing sent there.** This is the twenty-second checkpoint of PR2b (`../upstream-pr-composition-plan.md` §5, the PR2b row; layers 1 to 21 are `pr2b-layer1-record.md` to `pr2b-layer21-record.md`). A *layer* is one or more commits added to the local branch `pr2b/candidate`, which re-applies the old 34-commit candidate `pr2/candidate` onto `upstream/main` in small verified steps. It is the first layer of the two that [`pr2b-grouping-plan.md`](pr2b-grouping-plan.md) §5 decides (his D1 and D2 at the S393 picker). Every figure is printed by a script here or by a command named beside it. Files: `pr2b-layer22-expectations.txt` (written **before** the first pick: 00:21:50 against 00:21:56), `pr2b-layer22-26prime-edits.py` (the edits that make 26′), `pr2b-layer22-build-output.txt`, `pr2b-layer22-verify-output.txt` (the clean-clone run), `pr2b-layer22-measure-output.txt`, `pr2b-layer22-next-alone-output.txt`.

## 1. The answer first

1. **The layer exists.** `pr2b/candidate` (a local ref with no upstream, so a bare `git push` cannot send it) is now `fd43f707`: **29 commits on `upstream/main` `d50ce290`**, the 21 of layers 1 to 21 (unchanged; layer 21 is `d818ca17`) and, new, eight commits: series numbers 21, 22, 23, 24, 25, **26′**, 27 and 32. Built in a scratch `--no-local` clone, fetched here after the verification, `d818ca17` checked to be an ancestor first; `pr2/candidate` (`3cba1e50`) untouched.
2. **Seven were replays; none needed judgment.** Each `git cherry-pick -x` exited 0 and equals its original by `git patch-id --stable` (`pr2b-layer22-build-output.txt:5-12`).
3. **26′ is the one hand-written commit** (`d9f583c3`, 2 files, +18 / −18; section 2). Series commit 26 cannot be replayed on this tip (five regions in the trimmer and its tests). He saw the whole diff before the verification and answered 'Yes, as shown (Recommended)'.
4. **Every check the plan's PR2 row names passes in a clean clone** (section 3): the ratchet **18/18, 0 fail, 0 unmeasured**, results `a2482a2d9ae3` (equal to layers 20 and 21), manifest `09a751d541b8`; the shell suite run directly **302 passed, 0 failed, 0 skipped**; the inertness proof over the whole layer **HOLDS** (27 files, +650 / −687; no code token changed); the read-set budget unchanged.
5. **Adds nothing to the two open pull requests' conflicts**: #98 reads 5 regions in 3 files and #96 4 regions in 3 files, before and after (section 4). The plan feared 26′ might add regions against #98; it added none.
6. **My claim-time expectations, scored** (fourteen): **twelve confirmed, two missed** (section 5): E4, the fork-token count, because I quoted the plan's after-everything figure for a layer that lacks the printed-text commits; E13, the timing, by 20 seconds.

## 2. 26′, and why it is not a replay

The tip's trimmer is upstream's 1.8.2 plus the fork's layout hunks, labelled 1.9.0; series commit 26 was made against the old candidate's text and conflicts in five regions (`pr2b-grouping-measure-output.txt:94-99`). 26′ is the tip's blobs plus 16 edits (`pr2b-layer22-26prime-edits.py`, which refuses to write unless every old string occurs once): `starter-kit/methodology_trim.py` 13 lines, `tools/test_methodology_trim.py` 5 lines. Rules are the old scrub's (`scrub-record.md` §3): only fork tokens go (backlog codes, `decision D5`, `plan 4.1`, `coupling C7`); a sentence meaningful only inside the fork is deleted, not reworded (the dated aside at `_ledger_resolution`).

**One of the 17 strict lines is left on purpose:** `tools/test_methodology_trim.py:4622`, `# ... no P1 finding`. `P1` is the trimmer's own finding code (commit 26's message says so; `scrub-record.md` §3 lists the same call at the old `:1660` and `:3809`). So the trimmer has **0** strict lines left and its tests **1**.

Evidence it changed text only: the proof (`build:74`) compares each Python file's tokens with strings and comments masked, across the whole range; the trimmer suite runs **265 tests OK** (`build:30`); the scrub regex finds **0 of 18** added lines carrying a fork token (`measure:138`).

## 3. Verification in a clean clone

`pr2b-layer-driver.sh 22` (unchanged), serial, hooks not armed, on `fd43f707`: Part 1 00:28:25 to 00:44:16 (15 min 51 s), Part 2 to 00:50:04 (5 min 48 s), done 00:50:05 (**21 min 40 s**). Load average 4.35 at the launch and 3.67 at the end; I did not sample it between.

| Check | Result |
|---|---|
| quality ratchet `--run` | 18/18 pass, 0 fail, 0 unmeasured, results `a2482a2d9ae3`, manifest `09a751d541b8` (`verify:18`, citation `:40`, exit `:42`) |
| each gate against its floor | every value equal to its floor and to layer 21's: `tests-sh-passed` 302, dashboard 395, context budget 163, trimmer 265, ratchet 120, layout 76, checker layouts 11, sync layouts 82, migration 280, the nine zero-ceiling gates 0 (`verify:21-38`) |
| why the manifest id moved | the id hashes the manifest's text and commit 32 rewrites two gate `why` strings; the proof shows the manifest equal with every `why` masked |
| inertness proof, layer range | HOLDS, exit 0 (`build:74`) |
| `bash bin/tests.sh` | 302 passed, 0 failed, 0 skipped (`verify:395`); Test 15 `(30 == 30)` (`:117`); both link checks PASS in Test 10 |
| scanner | 15 files, 0 sites, 138 acknowledged, **194** prose not counted (layer 21: 195; 26′ alone leaves it at 195, `measure:101,113`, so another of the seven moved one prose line; I did not trace which) |
| read-set budget | exit 0, resident 51,487 B and read-set 70,048 B, both as at layer 21 (`verify:46`, `build:15-25`) |
| tracked proof, `--reverify` | both exit 0 (`verify:47`, `:408`) |
| `check-links` (no flag, `legacy`, `new`, `both`) | all exit 0, 80 links in 23 files (`verify:411-414`) |
| cheap suites in the build clone | layout 76, checker 11, trimmer 265, sync 82, dashboard 395, migration fast classes 95, all OK (`build:28-33`) |

## 4. The two open pull requests, and the next commits

Heads read from GitHub at this session's Phase 0: #98 `65990cda`, #96 `ad5c980f`, each 0 comments, 0 reviews. The layer is **clean with `upstream/main`**, the merged tree equal to the layer's own (`788e6885f6b6`, `measure:63`). **#98:** exit 1, **5 regions in 3 files**, identical to the parent's, 0 added (`measure:65-74`); **#96:** exit 1, **4 regions in 3 files**, 0 added (`measure:76-85`). 26′ alone behaves the same (`measure:146-166`). Controls as before: `upstream/main` with #98 clean; with #96 one region in `CHANGELOG.md`, the `merge=union` gap (GitHub ignores the union driver).

**Layer 23's commits, each alone onto this tip** (`next-alone:11-17`): 28, 29, 30 and 33 are **clean**; 30 needed 22 and 33 needed 27, both now in. The original 26 still conflicts alone (`:8`), as it should, since 26′ replaces it. Applied in order in a temporary branch of the build clone (33, 28, 29, 30; deleted afterwards), all four exit 0.

**Fork tokens.** At the layer tip: **60 lines in 11 files** (`build:93`); with layer 23's four added: **17 in 5 files** (`build:144`): the frozen fixture 11, `bin/tests.sh` 2, `bin/check-layout-literals` 2, `tools/test_migrate_layout.py` 1, `tools/test_methodology_trim.py` 1 (the `P1` line). The grouping plan's "33, less 17" assumed the whole series; this layer is the part before the printed-text commits.

## 5. Expectations, scored (`pr2b-layer22-expectations.txt`)

E1 five picks exit 0, patch-ids equal: **confirmed**. E2 27 and 32 likewise: **confirmed**. E3 26′ is 2 files, 13 + 5 lines, +18 / −18: **confirmed** (`build:10`; `measure:96-98`). **E4 fork tokens 17 in 5 files at the new tip: MISSED as written** (60 in 11); the intended form, 17 in 5 after layer 23's commits, held. E5 proof exit 0: **confirmed**. E6 18/18, results digest equal, manifest digest different: **confirmed**. E7 302 / 0 / 0: **confirmed**. E8 scanner 15 / 0 / 138 and the budget unchanged: **confirmed** (the prose count moved 195 to 194, which E8 did not state). E9 `--reverify` and four link checks exit 0: **confirmed**. E10 #96 4 regions 0 added; #98 between 5 and 9, at most 7: **confirmed** (5, 0 added). E11 0 fork tokens on 26′'s added lines: **confirmed**. E12 layer 23's four clean alone: **confirmed**. **E13 the driver takes 22 to 30 minutes: MISSED** (21 min 40 s, on a quiet machine). E14 dashboard 395 and trimmer 265 OK: **confirmed**.

## 6. What this does not show

1. **That the rewritten prose reads well to the maintainer.** He (the operator) approved 26′'s diff as shown; no test reads a comment, and the eight commits' sentences are not read by anyone who maintains upstream (`scrub-record.md` §4).
2. **The surface** is this machine: clean clones, serial runs, hooks **not armed**; Windows is untried.
3. **The "alone" figures are estimates for layer 23**; the in-order try was in a temporary branch, not a verified layer.
4. **The timings** come from a quiet machine (one-minute load average about 4 at the three samples: 3.96, 4.35, 3.67), unlike S393's measurements at load 61 to 103.
5. **The scanner's 195 to 194** is explained for 26′ only (it is not the cause).

## 7. Next

**Layer 23** (`pr2b-grouping-plan.md` §5): in a scratch `--no-local` clone at `fd43f707`, `git cherry-pick -x` of `cfcc713b` (33), then `8ace51e8` (28), `ccd5620e` (29), `28f99a70` (30), patch-ids equal; expectations first; `pr2b-layer-driver.sh 23` (nohup and a done-file); `python3 tools/test_methodology_dashboard.py` prints `Ran 397 tests` and `OK`; the gate floor reads 397; `scrub-proof.py` over the B range alone exit 0 (it refuses a range holding 33, by design); `quality_ratchet.py --precommit` accepts the floor; `scrub-derive.py` reads 17 in 5 files. Then PR3's table re-run and PR4's text re-checked against the 33-commit series (composition plan §5), each its own session; PR5 is three separate go-aheads.
**Re-run this layer:** `bash` the build as in `build-output` section 1; `python3 -I pr2b-layer22-26prime-edits.py <clone>` after the five picks; `python3 -I docs/planning/pr-composition-evidence/pr2b-layer-measure.py <repo> <commit> upstream/main <#98 head> <#96 head>` **from the repository root** with full SHAs; fetch the commits into the repository **before** the ancestor check.
