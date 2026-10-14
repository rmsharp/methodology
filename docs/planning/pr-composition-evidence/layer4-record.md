# PR2, Part 2, layer 4: the context-budget gate 1.4.0, the gate finds its config, its history file and its tool at the root or under methodology/

**Status: BUILT and verified, un-pushed, nothing sent.** Session S316, 2026-10-14. This is PR2's sixth checkpoint (`../upstream-pr-composition-plan.md`
§3 and §5; Part 1 is [`part1-record.md`](part1-record.md), layer 1 [`layer1-record.md`](layer1-record.md), layer 2 [`layer2-record.md`](layer2-record.md), layer 2b
[`layer2b-record.md`](layer2b-record.md), layer 3 [`layer3-record.md`](layer3-record.md), whose §6 named this layer). Every figure below is printed by a script in this
directory or by a command named beside it; the saved outputs are `layer4-*-output.txt`.

## 1. The answer first

1. **The layer exists.** Local branch `pr2/candidate` is now `e9c5cb8`, one commit on layer 3's `98ca7fc`: **4 files, +356 / -22** (`git diff --numstat 98ca7fc e9c5cb8`: the tool
   +146 / -18, its tests +206 / -1, the layout suite +3 / -2, the gates file +1 / -1); the candidate as a whole is 6 commits and 21 files, +12,191 / -807
   (`git diff --shortstat upstream/main pr2/candidate`; layer 3 left it at 19 files, +11,837 / -787, and the two new files are the tool and its tests, which were upstream's own).
   The scratch clone has no remote configured, and `git ls-remote --heads origin 'pr2*'` lists nothing.
2. **It is green on upstream's tree, in a clean `--no-local` clone** (`layer-verify.sh`, `layer4-verify-output.txt`, 7 min 55 s): `quality_ratchet.py --run` **13/13 pass,
   0 fail, 0 unmeasured** (results `989163398659`, manifest `5d02c560b035`; the manifest differs from layer 3's `576e8ab5d8d1` by the one floor); the shell suite run alone
   **298 passed, 0 failed, 0 skipped in 289 s** (`layer4-suite-output.txt`; the same count as layer 3: this layer changes no block of `bin/tests.sh`); the budget gate's suite **163 tests, OK, 2 skipped** (148, 2 skipped before this
   layer); the layout suite 74, OK; the dashboard suite 354 and the trimmer's 218, both unchanged and read by the ratchet; the one shipped `.verify.sh` exit 0, as at every layer.
3. **The new tests exercise the new behaviour** (`layer4-measure-output.txt`, section 2, made by `layer-contrast.sh` and `layer-outcomes.py`): 15 tests are added (148 to 163), none
   removed. Run against the old tool (1.3.1, upstream's), **10 of the 15 fail or error**. **The 5 that pass on both tools hold by design**, each read: they assert what the old tool
   already did correctly in the new layout or in the old one (a repository merely called `methodology` stays its own project; the legacy layout still writes its history at the
   root; growth is still refused with the config under `methodology/`; a commit that moves the config takes its baseline from HEAD's pre-move declaration; a HEAD holding both
   configs and both runners decides nothing and is refused). **One old test, of the 148, fails on the old tool**: `TestPrecommitClassArm.test_the_head_baseline_comes_from_heads_config_not_the_staged_one`
   pins the mechanism by source text, and 1.4.0's commit re-pointed that text (`head_config_text(root)` where it read `f"HEAD:{CONFIG_NAME}"`). It is a changed test, not an added one.
4. **The two new lines of the layout suite bite.** Run one at a time on the layer's tool, each with the file restored afterwards (section 3): one comment line added inside the
   embedded resolver block fails `test_each_copy_equals_the_modules_block_and_carries_exactly_one`; a root literal (`open('CHANGELOG.md')`) outside the block fails
   `test_each_resolved_tool_reports_no_site`. Each fails only its own test (`FAILED (failures=1)`).
5. **The builder reproduces the commit.** `layer4-build.py` run on `98ca7fc` with the fork's `7d16bc8` as the source gives tree `c00fbaf1f581`, equal to `e9c5cb8`'s. Before it writes
   anything it asserts that the candidate's two budget-gate files equal the fork's `517ebf6^` blobs byte for byte, and that the candidate's `tools/layout_resolver.py` and
   `tools/layout_fixtures.py` equal the source's; a one-byte drift in the base makes it refuse and write nothing (run: `refused: starter-kit/context_budget.py in the candidate is not 517ebf6^'s blob ...`, the clone left with only the edit that was made).
6. **The scanner reads 93 sites over 5 of 14 files** (101 over 6 at layer 3): the budget gate's 8 are gone, and the layout suite now asserts it. Left: the dashboard 79,
   `bin/check-handoff` 6, `bin/check-ledger` 4, `bin/status` 3, `bin/check-links` 1 (section 4). Still not a gate; exit 1 is the count.
7. **Against the two open pull requests, derived with `git merge-tree` (exit codes read, section 5):** #94's head (`972eb2cd6263`) conflicts in **3 files and 15 regions**, the same
   as before this layer (the trimmer 9, its tests 5, `.quality-gates.json` 1): **the layer adds none**, as derived. #92's head (`fa2bb5d464f9`): exit 0, no conflict.

## 2. What it carries

| File | Change | Note |
|---|---|---|
| `starter-kit/context_budget.py` | +146 / -18 | 1.3.1 to 1.4.0: the history file lives beside the config; the pre-commit gate reads HEAD's own declaration of the class wherever HEAD kept it (`head_config_text`); the installed hook names the tool and its twin; the project root is found by the embedded layout resolver; a repository that is itself called `methodology` stays its own project; a tree holding both configs is decided by the framework anchor or refused naming both |
| `tools/test_context_budget.py` | +206 / -1 | 163 tests (148): `TestTheConfigMayLiveInEitherLayout` (15 tests, all new), one re-pointed old test |
| `tools/test_layout_resolver.py` | +3 / -2 | `COPIES` and `RESOLVED` gain the budget gate: it is the third tool that carries the block and the third that must read 0 sites |
| `.quality-gates.json` | +1 / -1 | `context-budget-unit-tests` 148 to 163, the count the clone measured: tightened by exactly what this adds |

**What the layer does to a reader of the tool:** a project that moved its framework files under `methodology/` keeps its budget gate (config, history file, hook); a project with its
config at the root gets what 1.3.1 did (the 5 tests above that hold on both tools).

## 3. What it leaves out, and why

| Not at this layer | Why |
|---|---|
| The dashboard (79 sites), the sync layers, `bin/migrate-layout`, the prose | later layers (plan §3) |
| `bin/check-handoff` (6 sites) and `bin/check-ledger` (4) | plan §4 names `check-handoff`'s new lints (theme F) as not carried and says nothing of the layout reading of these two tools; whether the pull request carries that reading is open (section 7) |
| A `bin/tests.sh` change | none needed: of the lines `git diff c8b9ddd..7d16bc8 -- bin/tests.sh` adds or removes, none cites the budget gate, and the candidate's existing block that runs it (its selftest, `install-hook`, `--status` and `sync` lines) passes unchanged |
| The 15 lines `tools/test_checker_layouts.py` gained in `c0d1e09` | that file is the fork's (`check-ledger`, `check-handoff`, `check-overhead`, `model-report` run as commands in both layouts; the candidate does not carry it); `c0d1e09`'s other 9 lines, in the budget gate's own tests, are carried |

## 4. Decisions I took that the plan did not

1. **The two files come from the fork's tip** (`7d16bc8`), not from a replay of three commits. The base is a measurement: the candidate's two files equal the fork's blobs at `517ebf6^`
   (and at `5ff62ea`, upstream's 1.3.1 commit); from there **exactly three commits touch them on both walks** (first-parent, and `--ancestry-path --full-history`): `517ebf6` (the tests, written
   red), `4959e7a` (1.4.0) and `c0d1e09` (one more test). The plain `5ff62ea..7d16bc8` walk lists 19 (six merges that all change the files against their first parent): they are history the base already
   contains. The first draft of the builder's docstring said the builder proves the three-commit difference; it proves the base blobs and nothing about the commits between, and the docstring now says so.
2. **The floor is measured, not copied:** the fork's is 163 too, but the builder takes `--budget-count` from a run of the suite in the clone, as 2b and 3 did.
3. **No carried fixture.** Layer 3 needed a new file; this layer reads only what the candidate already has (`tools/layout_fixtures.py` equals the source's, asserted).
4. **Scrub input** (a coarse regular expression over the layer's 356 added lines): 2 lines cite a `BL-` number (1 in the tool, 1 in the tests), 3 cite a phase as "P4" or "P7" (1 in the tool, 2 in
   the tests), 1 cites a session number (`S276`, in the tests); none cites a `docs/planning/` path, a fork learning or a failure-mode number; one test docstring also names plan sections ("plan 4.3, C9, 7.2b").
   The commit message of the layer carries none of them. The scrub is its own commit after the layers.

## 5. Against the two pull requests, and the scanner

`layer4-measure-output.txt`, sections 5 and 4. #94 (`972eb2cd6263`) and #92 (`fa2bb5d464f9`) were the heads when this ran (`gh pr view`, 2026-10-14, no comment or review on either).

## 6. What this does not show

The surface is this machine, with the load average between 5 and 27 across the session: clean clones, serial runs, `nohup` and done-files. **Not shown:** a budget-gate run in a real adopter's
tree under `methodology/` (the 163 tests build their own repositories in both layouts); the installed hook after a real `bin/migrate-layout` (the test moves the files with `git mv` and commits);
Windows; a maintainer's machine; upstream CI (there is none); the scanner at 0 (it is 93); the candidate merged with #94 (derived, not resolved).

## 7. Next

**The dashboard** (plan §3, fifth; the largest layer, 79 of the scanner's 93 sites, and the one D3 overrides the fork's own hold for). Decide first, with the plan §4: `bin/check-handoff` (6 sites) and
`bin/check-ledger` (4) are upstream's tools that the fork's layout reading edits; plan §4 does not name that reading, so the pull request either carries those 10 sites' fix (the scanner cannot read 0 without
it) or the scanner's gate lists them as exempt on the candidate. His call, or the plan's amendment. Re-run this layer: `bash layer-verify.sh <candidate> e9c5cb8`; rebuild: `python3 layer4-build.py <fork> 7d16bc8 <clone-at-98ca7fc>`, then once more
with `--budget-count 163`. PR2 is now six checkpoints spent of the plan's "two to four": the dashboard, the sync layers, `bin/migrate-layout`, the prose and the scrub remain.
