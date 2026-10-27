# PR2b layer 5: the trimmer 1.9.0, a ledger at the root or under `methodology/`, on `upstream/main` (S381, 2026-10-27)

**Status: BUILT and verified, local, un-pushed, nothing sent to `KJ5HST/methodology`.** This is the fifth checkpoint of PR2b
(`../upstream-pr-composition-plan.md` section 5, the PR2b row; layers 1 to 4 are `pr2b-layer1-record.md` to `pr2b-layer4-record.md`). Every figure is
printed by a script here or by a command named beside it; the saved outputs are `pr2b-layer5-verify-output.txt` (the clean-clone run) and
`pr2b-layer5-measure-output.txt` (the scanner on the parent and on the commit, the scrub count, and the merges with `upstream/main` and the open pull requests' heads). What I read from files and what a command measured are labelled.

## 1. The answer first

1. **The layer exists.** Branch `pr2b/candidate` (a local ref with no upstream, so a bare `git push` cannot send it) now has five commits on `upstream/main`
   `d50ce290`: layers 1 to 4 (`fbcef390`, `41a1e580`, `7d87cb2b`, `1d93579a`, unchanged, ancestors) and layer 5 `62680cd2` (tree `c1a78f62`): **5 files, +1247 / -105**,
   built in a scratch `--no-local` clone and fetched here (fast-forward only, after the verification). `pr2/candidate` (`3cba1e50`) is kept as it was.
2. **It did NOT apply cleanly, as S380 computed.** `git cherry-pick -x 98ca7fc9` onto `1d93579a` stopped, exit 1, on the three files S380 named, **one region each**: `.quality-gates.json` (the trimmer
   test floor), `starter-kit/methodology_trim.py` (the version header: 56 lines ours against 14 theirs) and `tools/test_methodology_trim.py` (both sides add at the end of the file: 806 against 493 lines).
   The sizing and S380's "three files" were silent on two more files that applied without a marker: a new 406-line fixture and 5 lines of `tools/test_layout_resolver.py`. That is 5 files, exactly the per-commit cap.
3. **Three judgments, two put to him, one forced by the tests.** (a) The version: the fork's layout work was also called 1.8.0, upstream's own 1.8.0 to 1.8.2 already exist, so the tool is **1.9.0**, upstream's history kept beneath
   (his choice at the S381 picker, "1.9.0 (Recommended)"). (b) The pin test: it compared today's proof template with a frozen copy of **1.7.0's**, and upstream's 1.8.2 differs from that by 107 lines, so it cannot pass; it now compares with a frozen copy of
   **1.8.2's**, regenerated the way the 1.7.0 copy was made (his choice, "Re-baseline to 1.8.2 (Recommended)"). (c) Not asked, forced by two failing tests: upstream's 1.8.2 `--reverify` refuses a frozen proof whose `PREFIX` is not `"../../"`,
   a constant; a ledger under `methodology/` writes `"../"`, so the refusal fired on a correct proof (exit 3). It now asks the proof's own ledger's layout (`layout_for`). One test added for the other-depth case.
4. **The version is provisional, and I gave him an incomplete reason for it.** My recommendation compared 1.9.0 with `upstream/main`'s 1.8.2 only. #98's head (`65990cda`) declares **1.9.0, 1.9.1 and 1.10.0** (measured, section 5), so if #98 merges first this layer's 1.9.0 collides with it.
   I told him; he answered "Keep 1.9.0, settle at PR5". The plan already defers the question that decides it (stack on #98 or supersede it, plan lines 226 to 227).
5. **The first verification failed, and the failure was real.** Commit `dfa66061` read 11/13 gates and `297 passed, 1 failed`: `tools/test_layout_resolver.py` `TestToolsAlreadyResolvedStayAtZero` reported a root literal at
   `starter-kit/methodology_trim.py:2085` (`"PREFIX is not in the form methodology_trim.py writes it"`), a line **upstream's 1.8.2 added**. Its neighbours build the name from `TOOL`, the one acknowledged literal; this one did not. One line changed to use `TOOL`
   (same printed text). The gate `layout-unit-tests` read 74 even then, because it counts tests run and not tests passed; only the suite's own pass line named it. I had not run that 1.3 s suite before the 7-minute one; I do now (section 6).
6. **It is green in a clean clone** (section 4): the quality ratchet **13/13 pass, 0 fail, 0 unmeasured**, every measured value equal to its floor (265 is the new exact one; 298, 354, 148, 120 and 74 unchanged and exact);
   the shell suite run directly: **298 passed, 0 failed, 0 skipped**; the trimmer's own tests: **265 tests, OK, 2 skipped**, the same 2 that the parent skips (227 tests, 2 skipped; both need a regenerated-count field this tree's `HANDOFFS.md` lacks).
7. **My claim-time expectations, scored.** "The scanner stays at or below 122 sites": **101**, confirmed (the trimmer's 21 fall to 0, 9 acknowledged sites appear). "The trimmer-tests floor rises": **227 to 265**, confirmed.
   Not predicted: the 5-file size, the three judgments above, and a layer-5 conflict with #98 (item 8).
8. **The open pull requests, measured per layer** (section 5, last rows). Against #96's head the series reads the same 4 regions in 3 files it read at layer 3, so **layer 5 adds none**. Against **#98's head the series is no longer clean**: layers 1 to 4 merged clean, **layer 5 does not: 5 regions in 3 files**
   (`.quality-gates.json` 1, `starter-kit/methodology_trim.py` 3, `tools/test_methodology_trim.py` 1). That is the first layer to meet #98; the plan (section 2.2) says #98 edits the trimmer, its tests and the gates file, the files this layer touches. I did not read those regions.

## 2. What it carries

| File | Change | Why it is in the layer |
|---|---|---|
| `starter-kit/methodology_trim.py` | +241 / -101 (1.8.2 to 1.9.0) | by the commit's message: the shard directory and the link prefix follow the directory of the ledger being trimmed (`layout_for`); the layout resolver embedded; a half-migrated tree refused; both archive directories read by the trigger. **Of the 241, the original commit's hunks are +228 / -92: equal line for line to the original's apart from the version header, measured before my other two edits (the layout-aware `PREFIX` refusal and the one `TOOL` line)** |
| `tools/test_methodology_trim.py` | +519 / -1 | 265 tests (227 before): the commit's 37, the other-depth test (1), and the pin test re-pointed at the 1.8.2 fixture |
| `tools/fixtures/trim-verify-template-1.8.2.sh` | new, 483 lines | the frozen proof template those tests compare with. Made by loading `1d93579a`'s trimmer and calling `build_verify(LEDGERS["CHANGELOG.md"], "CHANGELOG.md", "docs/archive/CHANGELOG-through-2026-01-01.md")`; **the same call on the 1.7.0 trimmer reproduced the commit's own 1.7.0 fixture byte for byte (`cmp`), which is why I trust the method**. The 1.7.0 fixture is not carried: nothing would use it |
| `tools/test_layout_resolver.py` | +3 / -2 | the trimmer joins the layout suite's lists of embedding tools (`COPIES`) and tools held at zero sites (`RESOLVED`); the ratchet was already in both |
| `.quality-gates.json` | +1 / -1 | `trimmer-unit-tests` 227 to 265, the measured count; the commit's own number (218) belonged to the old base |

**By reading** the plan's sections 1 and 4: none of the five is in section 4's "Not carried" column.

**The message's figures, re-checked on this tree** (the replayed-message lesson of S378, which layers 3 and 4 confirmed; this time **four were wrong or stale and I changed them**): the subject's 1.8.0 became 1.9.0; "the tool (+228 / -92)" became +241 / -101 (`git diff --numstat`, final);
"its tests (218, from 181)" became 265, from 227 (`Ran 265 tests`, the parent's `Ran 227 tests`); "1.7.0's proof template" became 1.8.2's; "the first entries of the layout suite's lists" became "the trimmer's entries" (the ratchet was already there);
"floor 181 to 218" became 227 to 265. "No bin/tests.sh block changes" is true, and I reworded it to say why: the places that name the trimmer use a root ledger (`bin/tests.sh:261` runs its unit tests, `:539` prints a hint in a fixture, `:1265` to `:1273` trims a root `CHANGELOG.md` and expects a `docs/archive/` shard), whose output this layer leaves unchanged; the suite passes.

## 3. The scanner on this tree (the to-do list, not a failure)

`python3 -I bin/check-layout-literals` reads **101 sites (73 path, 28 text) over 6 files**, exit 1, on the commit; on the parent it read 122 (80, 42) over 7. The only file whose count moved is `starter-kit/methodology_trim.py`, **21 to 0**, and its acknowledged sites go 0 to 9
(`layout: ok` markers; total acknowledged 18 to 27). The remaining files, unchanged: `bin/check-handoff` 6, `bin/check-ledger` 4, `bin/check-links` 1, `bin/status` 3, `starter-kit/context_budget.py` 8, `starter-kit/methodology_dashboard.py` 79. "Prose not counted" 170 to 172.
The section 3b crude check in the measure output says 16 of the parent's 21 site lines no longer appear verbatim in the commit; that is rewriting, not a hidden site (the count is the scanner's, and the suite holds the trimmer at 0).

## 4. The checks of the PR2 row, and which of them apply here

Clean `--no-local` clone, serial, `layer-verify.sh` (14:51:31 to 14:58:48, **7 min 17 s**) and then `bash bin/tests.sh` directly (14:59:11 to 15:04:05, **4 min 54 s**); the verified commit
was `62680cd2` (message already final, so the commit verified is the commit kept). The first run, on `dfa66061`, took 8 min and is described in section 1, item 5.

| Check (plan section 5, PR2 row) | Result |
|---|---|
| `quality_ratchet.py --run` (`pr2b-layer5-verify-output.txt`, Part 1) | **13/13 pass, 0 fail, 0 unmeasured**; results `d25e6e60c0ee`, manifest `841d12be5065`. Measured against floors: `tests-sh-passed` 298/298, `dashboard-unit-tests` 354/354, `context-budget-unit-tests` 148/148, `trimmer-unit-tests` 265/265, `ratchet-unit-tests` 120/120, `layout-unit-tests` 74/74; the seven zero-gates read 0 |
| `bash bin/tests.sh` run directly (Part 2) | **298 passed, 0 failed, 0 skipped**, exit 0 |
| `python3 -I -B tools/test_methodology_trim.py` (run alone in the build clone, before the last two edits; the same file is run inside the 298) | the first run (264 tests, 62.5 s) **failed 2**, both `--reverify` in the new layout (item 3c of section 1); after the fix, **265 tests OK, 2 skipped** in 65.9 s; the parent: 227 tests, OK, 2 skipped, in 56.4 s. I did not look for the cause of the extra seconds and make no claim |
| every shipped `.verify.sh` exit histogram equal to upstream's | one tracked proof (`docs/archive/CHANGELOG-through-2026-09-30.md.verify.sh`): exit 0 on the layer; exit 0 on the parent. **Also `--reverify` of that shard with the new tool: OK, exit 0** (Part 3) |
| `bin/check-layout-literals` | applicable now: **101 sites, a to-do list** (section 3); the row's 0 is for the last tool-resolving layer |
| `bin/check-links --layout both` | **not applicable at this layer**: the flag arrives with the sync layer (commit 9) |
| the changed-file list equal to section 2 | by reading (section 2) and by `git diff --numstat` in Part 1 |
| PR2b row: `conflicts-after-merge` reads 0 | `conflicts-after-merge.sh` is fixed on `pr2/candidate`, so it cannot measure this branch; the method is `pr2b-layer-measure.py` section 5. **With `upstream/main`: exit 0**, tree `c1a78f625c34`, equal to the layer's own tree; the branch is 5 commits ahead |
| the same merge with #98's head (`65990cda`) | **exit 1, 5 regions in 3 files** (`.quality-gates.json` 1, `starter-kit/methodology_trim.py` 3, `tools/test_methodology_trim.py` 1); the parent (layers 1 to 4) is **clean** with #98, and `upstream/main` alone is clean. **New at this layer** |
| the same merge with #96's head (`ad5c980f`) | **exit 1, 4 regions in 3 files** (`.quality-gates.json` 2, `bin/tests.sh` 1, `CHANGELOG.md` 1), the same as the parent; `upstream/main` alone reads 1 (`CHANGELOG.md`), the `merge=union` display gap. So the layer adds 0 |
| the read-set budget (`context_budget.py --status`) | nothing over budget, exit 0 |
| `.quality-gates.json` after the resolution | the diff against the parent is exactly one threshold (`trimmer-unit-tests` 227 to 265), read in this session, and `--run` above reads it back as the floor |

No threshold was loosened: the one raised floor is exactly the count of the tests the layer carries.

## 5. #98 and the version: what is measured

`git show 65990cda:starter-kit/methodology_trim.py` declares `TRIM_VERSION = "1.10.0"` and, in its header, the entries 1.10.0, 1.9.1, 1.9.0, 1.8.2 and 1.8.1 (its diff against `upstream/main` is the trimmer +170 / -13, the tests +767 / -1, `.quality-gates.json` 1 / 1, and three prose files).
So the number 1.9.0 is taken in #98 by a different change. **What follows depends on his stack-or-supersede answer at PR5 (plan lines 226 to 227)**, and nothing before PR5 leaves this machine. If the series stacks on #98, this layer is rebuilt on #98's head with a version above 1.10.0 and
its 3 trimmer regions resolved by reading (the version header is one of them, by construction). A later layer pins the number in prose: the dashboard comment at `starter-kit/methodology_dashboard.py:992` and `tools/methodology_dashboard.py:992` on `pr2/candidate` says "methodology_trim.py 1.8.0", which must follow whatever number this layer ends with when that layer is replayed.

## 6. What this does not show

1. **The surface** is this machine: clean clones, serial runs, hooks **not armed** (`layer-verify.sh` unsets `core.hooksPath`). The trimmer was run on fixture repositories built by the tests (`new_repo`, `to_new_layout`) and on the one tracked legacy shard; **no real project with a ledger under `methodology/` was trimmed**, no adopter was run (PR3's table is not re-run; the plan says it is, after all layers), and Windows is untried.
2. **The `--reverify` refusal is now layout-aware, which is new behaviour no maintainer has read.** The original commit did not contain it; it exists because upstream's 1.8.2 added a constant the layout work had made a placeholder. Both depths are tested (upstream's `"../"` in a legacy proof, mine `"../../"` in a new-layout one). Its message still names both values, as upstream's tests require.
3. **Fork-internal references ride along.** 18 of the layer's 1247 added lines match the scrub regex of `pr2b-layer-measure.py` (`starter-kit/methodology_trim.py` 6 of 241, `tools/test_methodology_trim.py` 2 of 519, the fixture 10 of 483, the other two files 0; rough, section 4 of the measure output). The plan puts the scrub in its own commit later
   in the series (the candidate's commit 26, which touches the trimmer and its tests and was predicted to conflict, plan sizing row 26), so the layer carries them. The message itself carries none.
4. **The regions against #98 are counted, not read** (section 4), and the 3 trimmer regions may include lines I wrote (the header).
5. **The 1.8.2 fixture proves the legacy template unchanged by this layer, not unchanged since 1.7.0.** Upstream changed the template between those two (107 differing lines after normalising the version). The test's name and docstring say 1.8.2.
6. **Order of checks.** The layout suite (74 tests, 1.3 s) reads the trimmer and would have caught the `TOOL` line before the 7-minute run. Run it, and the trimmer's own tests, first.
7. **The gate floors will move again.** They are exact for this layer; every later layer re-derives them (tighten only).

## 7. Next

**Commit 6 onward** of the candidate: 28 commits remain (6 to 33; 34 is dropped as superseded). He ticked "Group commits 6-33 after layer 5" at the S381 picker; grouping is a plan edit for a later session, and a group is still verified at its boundary (gate (c) of `SESSION_RUNNER.md` §Vertical Slice Sessions),
so grouping saves orientation and close-out, not verification time. The old candidate's own records (`layer1` to `layer7b`, plan line 4) are the ready-made grouping to check first. Re-run this layer: fetch `pr2b/candidate` into a scratch `--no-local` clone, run
`docs/planning/pr-composition-evidence/layer-verify.sh <clone> <commit>` (7 min 17 s here, 13 gates) and `python3 -I docs/planning/pr-composition-evidence/pr2b-layer-measure.py <repo> <commit> upstream/main <the open PRs' heads>`.
The saved measurement was run with `upstream/main`, `65990cda6afdff7242a63b6a47dd5a2eb120b55a` (#98) and `ad5c980f345758df3dae8276e778c0883ded833c` (#96).
