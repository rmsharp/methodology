# PR2, Part 2, layer 6: the sync layers: bin/sync, bin/status, bin/check-links and the manifest reader read a project in either layout

**Status: BUILT and verified, un-pushed, nothing sent.** Session S318, 2026-10-14. This is PR2's eighth checkpoint (`../upstream-pr-composition-plan.md`
§3 and §5; Part 1 is [`part1-record.md`](part1-record.md), layer 1 [`layer1-record.md`](layer1-record.md), layer 2 [`layer2-record.md`](layer2-record.md), layer 2b
[`layer2b-record.md`](layer2b-record.md), layer 3 [`layer3-record.md`](layer3-record.md), layer 4 [`layer4-record.md`](layer4-record.md), layer 5 [`layer5-record.md`](layer5-record.md), whose §7 named this layer).
Every figure below is printed by a script in this directory or by a command named beside it; the saved outputs are `layer6-*-output.txt`.

## 1. The answer first

1. **The layer exists, as three commits.** Local branch `pr2/candidate` is now `0aa1897`, three commits on layer 5's `dd581fe`: **9 files, +1,472 / -112** (`git diff --numstat dd581fe 0aa1897`, summed),
   in commits of **1, 5 and 5 files** (`4c0bdde` +3 / -1; `261b8d3` +447 / -108; `0aa1897` +1,022 / -3). The candidate as a whole is **10 commits and 26 files, +14,923 / -1,067** (`git diff --numstat upstream/main pr2/candidate`, summed;
   the layer adds one file, `tools/test_sync_layouts.py`, and changes four that were upstream's own bytes). The scratch clone has no remote configured; nothing was pushed.
2. **It is green on upstream's tree, in a clean `--no-local` clone** (`layer6-verify-output.txt`, 9 min 26 s): `quality_ratchet.py --run` **15/15 pass, 0 fail, 0 unmeasured** (results `c394bd64daa1`,
   manifest `f83feda853bd`); the shell suite run alone **299 passed, 0 failed, 0 skipped in 5 min 38 s** (`layer6-suite-output.txt`; 298 before, the one added check is the block that runs the new suite);
   the sync suite **82 tests, OK** (new); the layout suite **76, OK** (75); the scanner **0 sites over 12 files, exit 0** (14 sites over 14 files at the parent); the one shipped `.verify.sh` exit 0.
   Each of the first two commits was also run alone through the shell suite in the scratch clone: `4c0bdde` 298 passed, 0 failed, 0 skipped; `261b8d3` the same.
3. **The new tests exercise the new behaviour** (`layer6-measure-output.txt`, section 2): run against the parent's tools, **70 of the 82 sync tests fail or error**, and **the 12 that pass on both hold by design**, each read.
   Five pin the manifest's second table and the fixture trees built from it, which have been in the candidate since layer 1 (the table is data; this layer's tools read it). Seven pin what a legacy project already got and must
   keep getting: the default `check-links` message, a legacy tree read as legacy, a source without the table serving a legacy project, ignore mode on a legacy project unchanged, a missing directory still a row of its own,
   an option given twice a usage error, and the checker never writing into the checkout it simulates from. No old test fails on the old tools (there are none: the file is new). The layout suite: the one test this layer adds fails
   on the old tree, and **2 old tests fail there** because `COPIES` now names tools the parent's `bin/sync`, `bin/status` and `bin/check-links` do not carry a resolver block in: the list doing its job.
4. **The new lines bite** (section 3: each mutant on the layer's tree, the suite run, files restored after; every one fails only its own tests, and the unmutated control is 82 OK). A comment line inside `bin/sync`'s embedded resolver block fails
   `test_each_copy_equals_the_modules_block_and_carries_exactly_one`; a root literal outside the block in `bin/status` fails `test_the_scanner_reads_no_site_in_this_repository`; the scanner no longer skipping the two left-out checkers fails that
   test **and** the layout suite's new `test_the_two_checkers_that_do_not_read_the_layout_are_not_scanned_and_say_why`; `bin/sync` no longer refusing a project asked for the other layout fails 3 tests, no longer refusing a half-migrated one fails 4 subtests.
   **The first version of that last mutant was inert** (it replaced the first `--layout` in `bin/sync`, which is in the docstring) and read "survived" for a reason that said nothing about the suite; read on the raw output, rewritten against the guard's own lines, the whole script re-run.
5. **The builder reproduces the layer.** `layer6-build.py` run in three stages on `dd581fe` with the fork's `d68207f` as the source gives tree `5dd9c8ea255a`, equal to `0aa1897`'s. Before it writes anything it asserts that the candidate's four tools equal the fork's blobs at
   `2ed9262` (`bin/sync`, `bin/status`, `bin/_manifest_reader.py`) and `7aa27a0` (`bin/check-links`), that `bin/_manifest.py` parses to the same code as the source's once the docstring is dropped, and that `tools/layout_resolver.py` and `tools/layout_fixtures.py` equal the source's;
   a one-byte drift in the base makes it refuse and write nothing (section 4: `refused: bin/sync in the candidate is not the fork's blob at 2ed9262 ...`, no dirty path).
6. **The scanner is a gate now.** `layout-literals` (at most 0) is declared by this layer, as the plan said it would be, and reads 0. It is 0 because `bin/check-handoff` (6 sites) and `bin/check-ledger` (4) are **not scanned**, by name, with the reason printed
   (plan §7 D5, answered 2026-10-14): the series reads 93 (layer 4), 14 (layer 5), 0 (this layer, over 12 files). Section 5.
7. **Against the two open pull requests, derived with `git merge-tree`** (exit codes read, the first line read as a tree, section 6): #94's head (`972eb2cd6263`) conflicts in **3 files and 15 regions**, the same as before this layer (the trimmer 9, its tests 5,
   `.quality-gates.json` 1): **the layer adds none**, though it edits the gates file whose one region is already in conflict; #92's head (`fa2bb5d464f9`): exit 0, no conflict.

## 2. What it carries

| File | Change | Note |
|---|---|---|
| `bin/sync` | +145 / -32 | `--layout auto\|legacy\|new`: keeps a project in the layout it has, gives an empty one the legacy layout, refuses before any write a legacy project asked for the new layout, a migrated one asked for the legacy, and a half-migrated one (exit 2); seeds and tracked files follow the layout; `--source=github` serves either layout. **Whole file from the fork's tip** |
| `bin/status` | +85 / -21 | a `layout:` line per project; files and seeds read where that layout keeps them. Whole file |
| `bin/check-links` | +150 / -47 | `--layout legacy\|new\|both`, `--tree`: simulates either tree; the default stays legacy and prints what it always did. Whole file |
| `bin/_manifest_reader.py` | +65 / -7 | `read_new_layout`: the manifest's second table read as data, so `--source=github` can serve either layout. Whole file |
| `tools/test_sync_layouts.py` | +986 | new: 82 tests in 14 test classes, each driving a tool as a command in scratch projects. **The fork tip's file less one assertion** (section 4, decision 3) |
| `bin/tests.sh` | +13 / -1 | two hunks: Test 15 counts the table's rows (`4c0bdde`), and a block that runs the new suite, numbered for this suite (the tip's text names Test 53; here it is Test 34) |
| `bin/check-layout-literals` | +2 / -0 | two names added to the files it does not scan, each with its reason (section 4, decision 2) |
| `tools/test_layout_resolver.py` | +9 / -2 | `COPIES` gains the three tools; the scan-set test names them; one new test pins the two exemptions |
| `.quality-gates.json` | +17 / -2 | two gates added (`sync-layout-unit-tests` at 82, `layout-literals` at 0), `tests-sh-passed` 298 to 299 and `layout-unit-tests` 75 to 76, the counts the clone measured; the two `why` strings are written for this tree and carry none of the fork's codes |

**What the layer does to a user of the tools:** a legacy project gets what it always got (the 7 tests above that hold on both); a project that moved under `methodology/` is synced, listed and link-checked as the project it is.

## 3. What it leaves out, and why

| Left out | Why |
|---|---|
| The layout reading of `bin/check-handoff` (6 sites) and `bin/check-ledger` (4), and `tools/test_checker_layouts.py` | plan §7 D5, answered at the S317 close-out picker: canonical-only checkers adopters never run; the plan's §4 row F. The scanner does not scan them (decision 2) |
| `bin/migrate-layout` and its suite | the next layer. `bin/sync`'s refusal names it (`MIGRATE_TOOL = "bin/migrate-layout"`): **at this checkpoint the refusal names a tool that is not in the tree yet** |
| Test 10's `check-links --layout both` block | it reads red on this tree: `--layout legacy` is green (116 links), `--layout new` and `both` read **35 dangling links** in the new layout (`methodology/SESSION_RUNNER.md:39 -> docs/methodology/FRAMEWORK_APPARATUS.md#the-action-ledger` and 34 more). The documents are the prose layer's. The sync suite's `check-links` classes use fixture trees and are green |
| `bin/_manifest.py` | the candidate's differs from the tip's in comments and the docstring only (`git diff` +9 / -1; the builder asserts equal code); its `Test 34` is this suite's number for the block the tip numbers 53 |
| The tip's other `bin/tests.sh` differences | `layer6-blocks.py` (output `layer6-blocks-output.txt`), blocks paired by title with the numbers normalised: after this layer **19 of the candidate's 37 blocks are byte-identical to the tip's**; of the 18 that differ, one is Test 10's `--layout both` block (left out, above), one is the unit-suite block (Test 18: the tip also wires the checkers' layout suite, the close-out report and the migration tool; this layer's wiring is in it), four are canonical-only checkers' blocks (`check-handoff` and `check-learnings`: plan §4 row F), one is the fork's own scope of the ledger check, and eleven differ in a block number or a variable name and the comments that cite it. Of the 14 blocks the tip has and the candidate does not pair, only two call `bin/sync`: the context-budget block, which the candidate carries unnumbered (`== Test: context_budget.py ==`, which the splitter does not read as a block start), and a `model-report` block that uses it to set up a scratch project. **Test 15 is the one block this layer changed that is now identical to the tip's** |
| The fork's mutation pass of the sync suite (55 mutants) | the fork's, not re-run here. The five mutants above are of this layer's new lines and the guards |

## 4. Decisions I took that the plan did not

1. **Three commits, not two.** S317's next step said two checkpoint commits; the cap is 5 files and every commit must leave the suite green. The tools, the layout suite's `COPIES` (its test fails when a tool carries the block and is not listed), the sync suite, the wiring
   block, the gates and the scanner's scope do not fit two. Test 15 is why a third exists: it counted every line naming the project, and the tool's new `layout:` line makes it 31 for 30 files. Counting only the lines that start with the name passes on the old tool too (298, 0, 0),
   so it goes first as its own commit and the tools commit stays at 5.
2. **The scanner's scope is exactly the two checkers, by name.** D5 says "scope the scanner to the tools adopters receive plus the hook". Read literally that also drops `bin/sync`, `bin/status` and `bin/check-links`, which this layer resolves and which a gate at 0 should cover.
   So `NOT_SCANNED_ALWAYS` gains `bin/check-handoff` and `bin/check-ledger`, each with the reason the scanner prints. **This is the one place the candidate's scanner differs from the fork's** (the fork's two checkers read both layouts and are scanned): if the pull request merges and the
   fork re-syncs from upstream, the entry comes with it, and the fork's checkers would stop being scanned **silently** unless the entry is removed there. A resync-time note, not a defect of the layer.
3. **One assertion of the sync suite is left out.** `test_a_legacy_project_asked_for_the_new_layout_is_refused_and_the_migration_tool_is_named` ends with `assertTrue((REPO / "bin" / "migrate-layout").is_file())`, which fails here because the tool is the next layer's.
   The builder removes that one line (asserted: exactly one occurrence) and the migration layer puts it back. The test keeps its other assertions, including that the refusal names `migrate-layout` and does not say "not built".
4. **The floors are measured, not copied:** the fork's are 503 and 75 and 82; this tree's are 299 (298 plus the one new block), 76 (75 plus the pin test) and 82.
5. **The two new gates' `why` text is written for this tree.** The fork's carries session and backlog codes and a mutation claim (55 mutants) this tree did not re-run.

## 5. Against the two pull requests, and the scanner

`layer6-measure-output.txt`, sections 6 and 5. #94 (`972eb2cd6263`) and #92 (`fa2bb5d464f9`) were the heads when this ran (`gh pr view`, 2026-10-14, no comment or review on either).
The scanner's per-file list: parent `bin/check-handoff` 6, `bin/check-ledger` 4, `bin/status` 3, `bin/check-links` 1 (14 sites, 14 files, 114 acknowledged); layer 0 sites, 12 files, 117 acknowledged (over two fewer files).
The scrub input (section 7, a coarse regular expression over the 1,472 added lines): backlog codes on 7 lines, a phase ("P6") on 12, a `docs/planning/` path on 3, a learning citation on 1, a plan section or decision on 14, a session number on none, a failure-mode number on none; the new test names carry no phase.
The commit messages of the layer carry none. **`bin/sync`'s docstring cites `docs/planning/methodology-subdirectory-plan.md`, a document upstream does not have** (plan §2.4): the scrub's.

## 6. What this does not show

The surface is this machine (one load-average reading was taken, 5.96, 10.18 and 20.69 over 1, 5 and 15 minutes, during the first gate run): clean clones, serial runs, `nohup` and done-files. **Not shown:** the tools against a real adopter's tree (the 82 tests build scratch projects; the fork's adopter rehearsals were its own and are not re-run here);
`--source=github` against the network (the suite's sources are local fixtures); Windows; a maintainer's machine; upstream CI (there is none); the candidate merged with #94 (derived, not resolved); the sync suite's own behaviours beyond the five mutants above (the fork's mutation pass is not re-run);
the refusal's pointer at `bin/migrate-layout` resolving (the tool is the next layer's).

## 7. Next

**`bin/migrate-layout`** (plan §3, seventh): DERIVED (`git diff --numstat pr2/candidate d68207f`): `bin/migrate-layout` +1,458 (new), `tools/test_migrate_layout.py` +2,993 (new), the gates file (`migrate-layout-unit-tests` at 280, `timeout_seconds` 3600: its command-level suite takes about 265 s),
`tools/test_layout_resolver.py` (`bin/migrate-layout` in `COPIES`), `tools/test_sync_layouts.py` (**put the removed assertion back**: asserted absent first), and a `bin/tests.sh` block that runs only its two fast classes: six files, so two commits. Its inputs, read from the tip: it calls
`bin/status`, `bin/sync` and `bin/check-layout-literals`, reads `bin/_manifest.py` and `tools/layout_fixtures.GENERATED`: all in the candidate now. NOT CHECKED: whether it reads 0 sites under the scanner here, what its suite needs from the `tools/` tree beyond those, and its time on this machine
(the tip's own comment says the whole suite took 10.7 minutes before the split). **Then the prose** (it carries Test 10's `--layout both` block and clears the 35 dangling links), **and the scrub**.
Re-run this layer: `bash layer-verify.sh <candidate> 0aa1897`; rebuild: the three stages of `python3 layer6-build.py <fork> d68207f <clone-at-dd581fe> --stage prep|tools|suite`, then once more with `--stage suite --sync-count 82 --passed 299 --layout-count 76`;
the whole measurement: `bash layer6-measure.sh <fork> 0aa1897 dd581fe d68207f`. PR2 is now ten commits spent of the plan's "two to four sessions" (eight checkpoint sessions): `bin/migrate-layout`, the prose and the scrub remain.
