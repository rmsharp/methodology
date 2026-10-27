# PR2b layer 4: the quality ratchet 1.5.0, a gate that outlives its budget is unmeasured, on `upstream/main` (S380, 2026-10-27)

**Status: BUILT and verified, local, un-pushed, nothing sent to `KJ5HST/methodology`.** This is the fourth checkpoint of PR2b
(`../upstream-pr-composition-plan.md` section 5, the PR2b row; layers 1 to 3 are `pr2b-layer1-record.md`, `pr2b-layer2-record.md`, `pr2b-layer3-record.md`). Every figure is
printed by a script here or by a command named beside it; the saved outputs are `pr2b-layer4-verify-output.txt` (the clean-clone run) and
`pr2b-layer4-measure-output.txt` (the scanner on the parent and on the commit, the scrub count, and the merges with `upstream/main` and the open pull requests' heads). What I read from files and what a command measured are labelled.

## 1. The answer first

1. **The layer exists.** Branch `pr2b/candidate` (a local ref with no upstream, so a bare `git push` cannot send it) now has four commits on `upstream/main`
   `d50ce290`: layers 1 to 3 (`fbcef390`, `41a1e580`, `7d87cb2b`, unchanged, ancestors) and layer 4 `1d93579a` (tree `765d57e9`): **4 files, +696 / -20**, built in a scratch
   `--no-local` clone and fetched here. `pr2/candidate` (`3cba1e50`) is kept as it was.
2. **It applied with no conflict**, as the sizing record predicted (`pr2b-sizing-record.md`): `git cherry-pick -x c8c0b213` onto `7d87cb2b`, exit 0, no marker, no
   file edited by hand. Git printed `Auto-merging .quality-gates.json`, which is a clean three-way merge, not a conflict; I read the result (section 4, last row).
   The per-file line counts equal the original commit's `git show --numstat` exactly (`pr2b-layer4-measure-output.txt`, section 2).
3. **The commit's message needed no figure changed.** Layer 3's message had one wrong figure; this one has none that I found. I re-checked each figure it quotes on this tree
   (section 2). The only change is that the `-x` trailer was dropped by an amend; the tree is `765d57e9` before and after, and the hash moved from `6c9cf8ee` to `1d93579a`.
4. **It is green in a clean clone** (section 4): the quality ratchet **13/13 pass, 0 fail, 0 unmeasured**, every measured value equal to its floor (120 is the new exact one;
   298, 354, 148, 227 and 74 are unchanged and exact); the shell suite run directly: **298 passed, 0 failed, 0 skipped**.
5. **My expectations, scored.** I wrote at the claim that the literal scanner would stay at 122 sites and that `ratchet-unit-tests` and "perhaps `tests-sh-passed`" would rise.
   The scanner **stays at 122** with every per-file count identical and 18 acknowledged on both sides (measured, section 3): confirmed. `ratchet-unit-tests` **rises 81 to 120**: confirmed.
   `tests-sh-passed` **stays 298**: that part was wrong, and the commit's message said why (`bin/tests.sh` is not in the commit; `grep -c` for the budget and process-group terms in it reads 0).
6. **No region needed his judgment**, and no gate floor needed re-deriving upward beyond the one the commit declares.
7. **The open pull requests, measured per layer** (section 4, last rows): against #96's head the series reads the same 4 regions in 3 files it read at layer 3 (`.quality-gates.json` 2,
   `bin/tests.sh` 1, `CHANGELOG.md` 1), of which `CHANGELOG.md` is the `merge=union` display gap, so **layer 4 adds none**. Against #98's head the series is still clean.

## 2. What it carries

| File | Change | Plan section 1 / 4 theme | Why it is in the layer |
|---|---|---|---|
| `starter-kit/quality_ratchet.py` | +203 / -17 (1.3.0 to 1.5.0) | B | by the commit's message, whose behaviour the tests in section 4 exercise: 1.4.0: a command that outlives its budget (600 s, or the gate's own `timeout_seconds`) reads UNMEASURED with the note `timeout (N s)`; gates sharing a command share one run with the largest budget. 1.5.0: where the platform has process groups, the command runs in a session of its own and a timeout, an interrupt, a hangup or a SIGTERM kills its whole group |
| `tools/test_quality_ratchet.py` | +491 / -1 | B (its tests) | 120 tests (81 before) |
| `starter-kit/quality-gates.json` | +1 / -1 | B | the seed's `_gate_schema` line now documents `timeout_seconds` |
| `.quality-gates.json` | +1 / -1 | "gate thresholds tightened by exactly what the pull request adds" | `ratchet-unit-tests` 81 to 120 |

**By reading** the plan's sections 1 and 4 in this session: none of the four is in section 4's "Not carried" column, and the commit is independent of the layout work before it (its own message says so; the 12 lines the scrub
regex matches are section 5, item 3).

**The message's figures, re-checked on this tree** (the replayed-message lesson of S378, which layer 3 confirmed): the ratchet `VERSION` is `"1.3.0"` on the parent and `"1.5.0"` on the commit (`grep -m1 '^VERSION'`);
`python3 -I tools/test_quality_ratchet.py` prints `Ran 120 tests in 67.627s` and `OK`, exit 0 (run once alone in the build clone; that output is not kept here, and the same 120 is the ratchet's own reading in section 4); the tool's diff is `+203 / -17` and the tests' `+491 / -1` (`git diff --numstat`);
the default budget is `DEFAULT_TIMEOUT = 600` (`quality_ratchet.py:63`); the gates files' diffs are exactly the two lines above (`git diff` read in full); and "no `bin/tests.sh` block changes" is true twice over: the commit does not touch the file, and the file names none of
`timeout_seconds`, `process group`, `start_new_session`, `killpg` or `DEFAULT_TIMEOUT` (`grep -cE` reads 0).

## 3. The scanner on this tree (the to-do list, not a failure)

`python3 -I bin/check-layout-literals` reads **122 sites (80 path, 42 text) over 7 files**, exit 1, on the parent and on the commit alike, with the same per-file counts: `bin/check-handoff` 6, `bin/check-ledger` 4, `bin/check-links` 1,
`bin/status` 3, `starter-kit/context_budget.py` 8, `starter-kit/methodology_dashboard.py` 79, `starter-kit/methodology_trim.py` 21. Acknowledged sites: 18 on both (12 in the hook, 5 in the ratchet, 1 in the scanner).
The one number that moved is "prose not counted", **169 to 170**: a full listing of both trees (`--all`, line numbers dropped, diffed) shows one added line, a comment in `starter-kit/quality_ratchet.py` that names `ITERATIVE_METHODOLOGY.md`,
which the scanner classes as prose. It is not a counted site.

## 4. The checks of the PR2 row, and which of them apply here

Clean `--no-local` clone, serial, `layer-verify.sh` (12:12:52 to 12:21:10, **8 min 18 s**) and then `bash bin/tests.sh` directly (12:21:28 to 12:26:56, **5 min 28 s**); the verified commit
was `1d93579a` (message already amended, so the commit verified is the commit kept; the clean clone's `HEAD` equals the build clone's and, after the fast-forward, the ref). Both runs were slower than layer 3's (5 min 16 s and 3 min 28 s);
I started nothing beside them and did not look for the cause, so I do not give one.

| Check (plan section 5, PR2 row) | Result |
|---|---|
| `quality_ratchet.py --run` (`pr2b-layer4-verify-output.txt`, Part 1) | **13/13 pass, 0 fail, 0 unmeasured**; results `6bdecc626c64`, manifest `2dc4981e9937`. Measured against floors: `tests-sh-passed` 298/298, `dashboard-unit-tests` 354/354, `context-budget-unit-tests` 148/148, `trimmer-unit-tests` 227/227, `ratchet-unit-tests` 120/120, `layout-unit-tests` 74/74; the seven zero-gates (failures, links, learnings, handoff, ledger, the two hook selftests) read 0 |
| `bash bin/tests.sh` run directly (Part 2 of the same file, complete) | **298 passed, 0 failed, 0 skipped**, exit 0 |
| every shipped `.verify.sh` exit histogram equal to upstream's | one tracked proof (`docs/archive/CHANGELOG-through-2026-09-30.md.verify.sh`): exit 0 on the layer; exit 0 on the parent (`pr2b-layer3-verify-output.txt`) |
| `bin/check-layout-literals` | applicable now: **122 sites, a to-do list** (section 3); the row's 0 is for the last tool-resolving layer |
| `bin/check-links --layout both` | **not applicable at this layer**: the flag arrives with the sync layer (commit 9) |
| the changed-file list equal to section 4 | by reading (section 2) |
| PR2b row: `conflicts-after-merge` reads 0 | `conflicts-after-merge.sh` is fixed on `pr2/candidate`, so it cannot measure this branch; its method (merge-tree, empty attribute tree) is `pr2b-layer-measure.py` section 5. **With `upstream/main`: exit 0**, tree `765d57e926d1`, equal to the layer's own tree; `upstream/main` is an ancestor; the branch is 4 commits ahead |
| the same merge with #98's head (`65990cda`) | **exit 0, clean**; also clean for the parent and for `upstream/main` alone |
| the same merge with #96's head (`ad5c980f`) | **exit 1, 4 regions in 3 files** (`.quality-gates.json` 2, `bin/tests.sh` 1, `CHANGELOG.md` 1), the same as the parent; `upstream/main` alone against #96 reads 1 (`CHANGELOG.md`), the `merge=union` display gap measured at layer 3. So the layer adds 0 |
| the read-set budget (`context_budget.py --status`) | nothing over budget, exit 0 |
| `.quality-gates.json` after git's auto-merge | the diff against the parent is exactly one threshold (`ratchet-unit-tests` 81 to 120), read in this session, and the ratchet's `--run` above reads it back as the floor |

No threshold was loosened: the one raised floor is exactly what the layer adds.

## 5. What this does not show

1. **The surface** is this machine: clean clones, serial runs, hooks **not armed** (`layer-verify.sh` unsets `core.hooksPath`). The layer changes the ratchet that the hook chains to, and what ran was
   the ratchet's 120 unit tests, Test 37 (the real hook and the ratchet in scratch repositories, in both layouts) inside the 298, and the two hook selftests (read 0), not the hook armed on a commit to this branch.
   It cannot show Windows (the process-group stop is documented as absent there, and no test here ran on it), the maintainer's machine or upstream's CI (there is none).
2. **The process-group stop is shown on macOS only, by tests and the tool's own selftest, not by a gate that times out in `--run`.** The unit tests (`_GateCommandChildren`, `tools/test_quality_ratchet.py:262` on) start a shell that
   stays alive as the parent of a real `sleep 600` and record its pid; the tool's `--selftest` does the same through the real code path and was run in the clean clone: **OK, 30 checks, exit 0, 7 s**
   (`pr2b-layer4-verify-output.txt`, Part 3), including "a timed-out gate's command is stopped, not left running" and "SIGTERM to the tool stops a gate's command and the tool exits 143". After the runs
   `pgrep -f 'sleep 600'` read 0 stray processes. The no-process-groups path is tested by setting `HAS_PROCESS_GROUPS` false in a mock, not on a platform that lacks them. No declared gate times out, so `--run` never took that branch.
3. **Fork-internal references ride along.** 12 of the layer's 696 added lines match the scrub regex of `pr2b-layer-measure.py` (`starter-kit/quality_ratchet.py` 5 of 203, `tools/test_quality_ratchet.py` 7 of 491,
   the two gates files 0; rough, saved in section 4 of the measure output). The plan puts the scrub in its own commit later in the series (the candidate's commit 26), so the layer carries them. The message itself carries none.
4. **The ratchet's 120 unit tests ran in 67.6 s alone (one run).** I did not time the 81 before them or the other unit suites, so I make no comparison and do not say how much of that is new.
5. **PR3's table and PR4's text** are not re-run (the plan's PR2b row says they are, after all layers).
6. **The gate floors will move again.** They are exact for this layer; every later layer re-derives them (tighten only).

## 6. Next

**Commit 5** of the candidate, by reading: the layout hunks of the trimmer, the only new judgment in PR2b (the plan's PR2b row; the sizing record `pr2b-sizing-record.md:31` gives the order). Claim first; one layer per session. Re-run this layer: fetch `pr2b/candidate` into a scratch
`--no-local` clone, run `docs/planning/pr-composition-evidence/layer-verify.sh <clone> <commit>` (8 min 18 s here, 13 gates; the fork's 24-gate run is 20 to 30 minutes) and
`python3 -I docs/planning/pr-composition-evidence/pr2b-layer-measure.py <repo> <commit> upstream/main <the open PRs' heads>`.
The saved measurement was run with `upstream/main`, `65990cda6afdff7242a63b6a47dd5a2eb120b55a` (#98) and `ad5c980f345758df3dae8276e778c0883ded833c` (#96).
