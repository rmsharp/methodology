# PR2, Part 2, layer 1: the layout resolver and the literal scanner

**Status: BUILT and verified, un-pushed, nothing sent.** Session S312, 2026-10-13. This is PR2's second checkpoint of two to four
(`../upstream-pr-composition-plan.md` §3 and §5; Part 1 is [`part1-record.md`](part1-record.md)). Every figure below is printed by a
script in this directory or by a command named beside it; the saved outputs are `layer1-*-output.txt`.

## 1. The answer first

1. **The layer exists.** Local branch `pr2/candidate` is now `14ef959`, one commit on Part 1's `bbe0dc3` on `upstream/main` `f34769f`:
   **7 files, +1,225 / -2**; the candidate as a whole is 2 commits and 14 files, +8,989 / -576 (`git diff --stat upstream/main pr2/candidate`).
   It has no upstream configured (a bare `git push` cannot send it) and nothing named `pr2*` exists on `origin`.
2. **It is green on upstream's tree, in a clean `--no-local` clone** (`layer-verify.sh`, `layer1-verify-output.txt`):
   `quality_ratchet.py --run` **13/13 pass, 0 fail, 0 unmeasured** (results `3dc6075cbb35`, manifest `45c7608f36d2`); the shell suite
   **272 passed, 0 failed, 0 skipped** (Part 1: 271/0/0; the one added pass is the layout suite's line; the skipped figure is from the
   same tree's own run before its commit, `layer1-suite-output.txt`); the layout suite 74 tests; the one shipped `.verify.sh` exit 0, as at Part 1.
3. **The scanner is RED on this tree, on purpose: 158 sites over 9 of 14 files** (`layer1-scanner-output.txt`): the dashboard 79,
   `.githooks/pre-commit` 21, the trimmer 20, the ratchet 16, the budget gate 8, `bin/check-handoff` 6, `bin/check-ledger` 4, `bin/status` 3,
   `bin/check-links` 1. That list is the to-do list of the layers that follow. **The plan's §5 criterion "`bin/check-layout-literals`
   0 sites" belongs to the last layer that resolves a tool, not to this one**; the gate `layout-literals` (max 0) is therefore *not* declared
   here, and lands where the scanner first reads 0 (the sync layer: `bin/sync`, `bin/status`, `bin/check-links`).
   Two other §5 criteria are likewise not this layer's: `bin/check-links --layout both` (upstream's `check-links` takes only `--tree`),
   and the changed-file comparison with §4's not-carried sets, which here is empty (none of the 7 files is theme E, F or G).
4. **Against the two open pull requests, derived with `git merge-tree`:** the candidate conflicts with #94's head (`972eb2cd6263`) in
   exactly the two files Part 1 did (`starter-kit/methodology_trim.py`, `tools/test_methodology_trim.py`; `.quality-gates.json` merges
   clean); with #92's head (`fa2bb5d464f9`) not at all. This layer adds no conflict.

## 2. What it carries

| File | Change | Note |
|---|---|---|
| `tools/layout_resolver.py` | new, 76 | byte-identical to the fork's (blob `ac5e152`): the four-row table as one marked stdlib block, and the `embedded_block` reader |
| `tools/layout_fixtures.py` | new, 88 | byte-identical (`e4cc389`): trees in five shapes, derived from the manifest |
| `bin/check-layout-literals` | new, 299, mode 755 | byte-identical (`32a683e`): the scanner |
| `tools/test_layout_resolver.py` | new, 702 | the fork's 720-line file with 22 lines removed or changed and 4 added (§4); 74 tests |
| `bin/_manifest.py` | +43 / -1 | `NEW_LAYOUT`, the target layout as a table of literals, and two docstring sentences naming it; the file's other differences from the fork are comment and test-number churn and are not carried |
| `bin/tests.sh` | +8 | one block wiring the layout suite in, after the ratchet's |
| `.quality-gates.json` | +9 / -1 | the gate `layout-unit-tests` (74) and `tests-sh-passed` 271 to 272, tightened by exactly what is added |

**Reproduced, not only built:** `layer1-build.py` run on `bbe0dc3` with the fork's `a36d9f8` as the source gives tree `e32dea7f2635`,
equal to `14ef959`'s. It asserts every edit matches once and computes every file before writing the first.

## 3. What it leaves out, and why

| Not at this layer | Why |
|---|---|
| The resolver's block in any shipped tool; the gate `layout-literals`; the dashboard twin's block test | each belongs to the layer that touches that tool (plan §3 order); the first is the gate layer |
| `close_out_report.py`, `check-overhead`, `model-report` in the lists of embedding tools | themes E and F are not carried (plan §4), so **those three entries never enter the candidate**: its final lists hold at most 10 of the fork's 13 (fewer if a later layer leaves the resolver out of `check-handoff` or `check-ledger`) |
| `.githooks/pre-commit`, the ratchet, the trimmer, the budget gate, the dashboard, `bin/sync`, `bin/status`, `bin/check-links`, `bin/migrate-layout` | later layers |

## 4. Decisions I took that the plan did not

1. **`NEW_LAYOUT` is carried here, not at the sync layer.** The fixtures build the new and tier-1 shapes from it and the layout suite
   pins it to the plan's §4.1 typed out as literals. The alternative was the fork's first-phase fixtures, which carried a mapping rule of
   their own and were replaced when the table arrived: a reviewer would read two versions of one file. Cost: the manifest is touched at
   layer 1; the sync layer then adds only its reader. Measured: upstream's reader and its Test 34 accept the extra table (suite 272/0/0).
2. **Two loops compare nothing at this layer.** `COPIES` and `RESOLVED` (the tools that embed the block, the tools scanned at zero) start
   empty, so `test_each_copy_equals_the_modules_block_and_carries_exactly_one` and `test_each_resolved_tool_reports_no_site` pass vacuously,
   and both count in the 74. `test_every_tool_that_carries_the_markers_is_listed` is not vacuous: it fails if any tool embeds the block
   unlisted. Each later layer appends the tools it touches, as the class docstring already says; the layer that does the first append is
   the first at which those two tests mean anything.
3. **The dashboard twin's block test is removed here** and returns with the dashboard layer, and `..._scans_the_five_tools_the_plan_names...`
   is renamed `..._scans_the_tools_it_names...` and drops `close_out_report.py` (absent upstream, never carried).
4. **The builder, not a hand edit, makes the layer** (as Part 1's did for `bin/tests.sh`), so layer 2 onward can be built the same way.

## 5. What this does not show

The surface is this machine at a load average near 30: clean clones, serial runs, `nohup` and a done-file. **Not shown:** Windows; a
maintainer's machine; hooks armed in another clone (none ran in the scratch clone); upstream CI (there is none); the scanner at 0 (it is
158); the two vacuous loops of §4.2; a re-run of the gate citation at Phase 0 (not done, the load read 27, and this layer's run measures
it). Added-line tokens for the scrub, by a coarse regular expression (not `fork-tokens.py`'s): 6 lines with a backlog code, 5 with a
session number, 6 with a `docs/planning/` path, 1 learning citation, about 25 plan-phase codes. The scrub is its own commit after the layers.

## 6. Next

Layer 2 is the gate layer (plan §3): `.githooks/pre-commit` and `quality_ratchet.py`. **Open design question, for that session to
measure before it builds:** the fork's ratchet is 1.5.0 (1.1.0 at upstream) and its changes arrived across the directory work (1.2.0),
the checkers (1.3.0) and the timeout repairs (1.4.0, 1.5.0); "the later ratchet changes where they belong" can mean the whole lineage at
layer 2 (as Part 1 did for the dashboard) or 1.2.0 now and the rest in later layers. Whichever is chosen, its first append to `COPIES`
and `RESOLVED` is what makes §4.2's two tests mean something. Re-run: `bash layer-verify.sh <candidate> 14ef9597c61a`.
