# PR2, Part 2, layer 2: the gate layer, the ledger hook and the quality ratchet 1.3.0

**Status: BUILT and verified, un-pushed, nothing sent.** Session S313, 2026-10-13. This is PR2's third checkpoint (`../upstream-pr-composition-plan.md`
§3 and §5; Part 1 is [`part1-record.md`](part1-record.md), layer 1 is [`layer1-record.md`](layer1-record.md)). Every figure below is printed by a
script in this directory or by a command named beside it; the saved outputs are `layer2-*-output.txt`.

## 1. The answer first

1. **The layer exists.** Local branch `pr2/candidate` is now `fd96593`, one commit on layer 1's `14ef959`: **6 files, +1,035 / -113**; the candidate
   as a whole is 3 commits and 17 files, +10,021 / -686 (`git diff --stat upstream/main pr2/candidate`). It has no upstream configured and nothing
   named `pr2*` exists on `origin`.
2. **It is green on upstream's tree, in a clean `--no-local` clone** (`layer-verify.sh`, `layer2-verify-output.txt`): `quality_ratchet.py --run`
   **13/13 pass, 0 fail, 0 unmeasured** (results `fcb4bc43663f`, manifest `f43c41607f11`); the shell suite **298 passed, 0 failed, 0 skipped** (layer 1:
   272/0/0; Test 37 adds 26 passes; the skipped figure is the working clone's own run before the commit, `layer2-suite-output.txt`); the ratchet's
   suite 81 tests (45 upstream), the layout suite 74; the one shipped `.verify.sh` exit 0, as at layer 1.
3. **The open question S312 left is answered by measurement, and neither option it named is what is built** (§4.1): the whole 1.1.0 to 1.5.0 lineage is not
   needed here and 1.2.0 cannot be built. The layer carries **1.3.0**, the first state whose embedded resolver equals the module layer 1 carries;
   **1.4.0 and 1.5.0 (a gate's budget and process group) are their own commit, next.**
4. **The scanner reads 121 sites over 7 of 14 files** (158 over 9 at layer 1): the hook's 21 and the ratchet's 16 are gone, and the layout suite now
   asserts it. Left: the dashboard 79, the trimmer 20, the budget gate 8, `bin/check-handoff` 6, `bin/check-ledger` 4, `bin/status` 3, `bin/check-links` 1
   (`layer2-scanner-output.txt`). Still not a gate, for layer 1's reason.
5. **Against the two open pull requests, derived with `git merge-tree`:** #94's head (`972eb2cd6263`) conflicts in the same two files as at Part 1 and
   layer 1 (`starter-kit/methodology_trim.py`, `tools/test_methodology_trim.py`; `.quality-gates.json` merges clean); #92's head (`fa2bb5d464f9`) not at
   all. This layer adds no conflict.

## 2. What it carries

| File | Change | Note |
|---|---|---|
| `.githooks/pre-commit` | +246 / -63 | the fork's file as it stands (unchanged there since `26bc97a`): the ledger read from the index at either place, the half-migrated refusal and the runner's tie rule, the never-edit check across a move, either archive directory, the ratchet chain's guard; its selftest builds its fixtures in both layouts and reads 43 checks (17 upstream; nothing in this tree cites a count) |
| `starter-kit/quality_ratchet.py` | +192 / -43 | 1.1.0 to 1.3.0 (the fork's `26bc97a`): the resolver block embedded; `manifest_location`, `find_root`, the results file beside the manifest; `precommit` judges a move (`manifest_blobs`, a history walk over both paths); the runner's tie rule |
| `tools/test_quality_ratchet.py` | +391 / -1 | 81 tests (45 upstream) |
| `bin/tests.sh` | +202 / -2 | Test 37 (the fork's Test 54): the real hook and real git in both layouts, the move commit, a half-migrated tree, both ties, and 9 controls (26 passes); and one assertion rewritten |
| `tools/test_layout_resolver.py` | +2 / -2 | the first entries of `COPIES` (the ratchet) and `RESOLVED` (the hook and the ratchet) |
| `.quality-gates.json` | +2 / -2 | `ratchet-unit-tests` 45 to 81, `tests-sh-passed` 272 to 298: tightened by exactly what this adds |

**Reproduced, not only built:** `layer2-build.py` run on `14ef959` with the fork's `26bc97a` as the source and `f616a6c` for the test blocks, then with
`--gate-counts 81:298`, gives tree `5c11b806db7b`, equal to `fd96593`'s. It asserts every edit matches once and computes every file before the first write.

## 3. What it leaves out, and why

| Not at this layer | Why |
|---|---|
| The ratchet's 1.4.0 and 1.5.0 (fork `ac85bb8`, `76f0082`, and their tests): a gate that outlives its budget reads unmeasured, and its command stops with its whole process group | independent of the layout (§4.1): 186 more lines of tool and 450 of tests; they also carry the one changed line of `starter-kit/quality-gates.json` (`_gate_schema`) and pair with theme B's prose. **Until that commit the candidate's ratchet reads a timed-out gate as exit 127, as upstream's 1.1.0 does** |
| The resolver's block in any other tool; the gate `layout-literals` | the layers that touch those tools; the gate lands where the scanner first reads 0 (the sync layer) |
| The trimmer, the budget gate, the dashboard, the checkers, `bin/sync`, `bin/status`, `bin/check-links`, `bin/migrate-layout`, the prose | later layers |
| `close_out_report.py`, `check-overhead`, `model-report` in the two lists | themes E and F are not carried (plan §4), so those entries never enter: the final `COPIES` holds at most 10 of the fork's 13 |

## 4. Decisions I took that the plan did not

1. **The ratchet's lineage, measured** (S312's open question: the whole 1.1.0 to 1.5.0 at this layer, or 1.2.0 now). Three facts decide it.
   **(a) 1.2.0 cannot be built here:** the resolver block embedded in the ratchet at the fork's four 1.2.0 commits (`eba958a`, `215e18e`, `2fa2d34`,
   `6907f00`) differs from `tools/layout_resolver.py` as layer 1 carries it (its final form), so the layout suite's equality test would fail; the first
   fork commit whose block is equal is `26bc97a` (1.3.0), and it stays equal to the tip. **(b) 1.3.0 is a complete, tested state:** 741 lines of tool
   and 854 of tests, the last state before the timeout work, the hook unchanged since. **(c) 1.4.0 and 1.5.0 do not touch the layout:** from `26bc97a`
   to the tip the tool gains 186 lines and its tests 450, in the docstring, the imports and constants, `run`, the new gate-command functions,
   `config_defects`, `compare`, `measure_gate` and `selftest`, and none in the resolver block, `manifest_location`, `find_root` or the manifest readers
   (`git diff 26bc97a HEAD -- starter-kit/quality_ratchet.py`, read hunk by hunk). So this layer carries 1.3.0 and the two timeout releases are a
   checkpoint of their own, which a reviewer can read without the layout. **A sequencing choice, reversible and outward to no one; it is his to overrule.**
   Cost, computed from the plan's §3 order: after this layer remain the trimmer, the budget gate with the checkers, the dashboard, the sync layers,
   `migrate-layout`, the prose and the scrub, plus this split's second commit; three of the plan's "two to four sessions" for PR2 are spent (Part 1, layer 1
   and this one), so that figure wants restating at PR4.
2. **Test 54 is Test 37 here**, the precedent Part 1 set with its Tests 35 and 36: the next free number in this tree. The builder renames the number 54
   alone and as an identifier suffix (`t54_repo`, `RC54`) and refuses if a 54 token survives. The block comes from the fork's tip, not from `26bc97a`:
   its 16 later lines are a fixture guard (an unset `"$2"` under `set -u` leaves `git -C ""` acting on the current directory) and one more control (the
   shipped ratchet with its tie rule turned off must refuse the root-manifest edit the shipped tool passes); both are layout work and both pass
   against 1.3.0 (the control mutates a line 1.3.0 has).
3. **The hook is carried as the fork has it**, selftest and comments included; it is unchanged there since `26bc97a` (`git diff 26bc97a HEAD --stat --
   .githooks/pre-commit` is empty), so the one source revision serves both files.
4. **Scrub input** (a coarse regular expression, not `fork-tokens.py`'s, which reads the fork's own tip): of the layer's 1,035 added lines, 16 carry a
   backlog code, 5 a session number, 10 a plan-phase code, 23 a plan-section code or `X2`, none a `docs/planning/` path or a fork-learning
   citation. The scrub is its own commit after the layers.

## 5. What this does not show

The surface is this machine, with the load average between 4 and 66 across the session: clean clones, serial runs, `nohup` and a done-file. **Not shown:**
Windows; a maintainer's machine; a hook armed in another clone (the suite arms real hooks in scratch repos it makes, each with its own `core.hooksPath`);
upstream CI (there is none); the scanner at 0 (it is 121); the candidate merged with #94 (the conflict list is derived, not resolved); a timed-out gate
(the candidate's ratchet still reads it as exit 127 until the next commit); that the fork's own tip behaves like this tree (it differs by 1.4.0 and 1.5.0).

## 6. Next

**The ratchet's 1.4.0 and 1.5.0 as one checkpoint** (fork `ac85bb8`, `3017741`, `acfbefb`, `c037b48`, `76f0082`, `bf5d122`, `5a50de9`, `1c78a78`: the tool, its
tests, the seed line, the gate floor), built on this layer's builder; then the trimmer (the plan's third layer). Re-run: `bash layer-verify.sh <candidate>
fd965939d2e4`; rebuild: `python3 layer2-build.py <fork> 26bc97a <clone-at-14ef959> --tests-rev f616a6c [--gate-counts 81:298]`.
