# PR2, Part 2, layer 3: the ledger trimmer 1.8.0, a ledger under methodology/ is trimmed and proved

**Status: BUILT and verified, un-pushed, nothing sent.** Session S315, 2026-10-14. This is PR2's fifth checkpoint (`../upstream-pr-composition-plan.md`
§3 and §5; Part 1 is [`part1-record.md`](part1-record.md), layer 1 [`layer1-record.md`](layer1-record.md), layer 2 [`layer2-record.md`](layer2-record.md), layer 2b
[`layer2b-record.md`](layer2b-record.md), whose §6 named this layer). Every figure below is printed by a script in this directory or by a command named beside
it; the saved outputs are `layer3-*-output.txt`.

## 1. The answer first

1. **The layer exists.** Local branch `pr2/candidate` is now `98ca7fc`, one commit on layer 2b's `c8c0b21`: **5 files, +1,135 / -96**; the candidate as a whole is
   5 commits and 19 files, +11,837 / -787 (`git diff --shortstat upstream/main pr2/candidate`). No upstream is configured and nothing named `pr2*` exists on `origin`.
2. **It is green on upstream's tree, in a clean `--no-local` clone** (`layer-verify.sh`, `layer3-verify-output.txt`, 8 min 20 s): `quality_ratchet.py --run` **13/13 pass,
   0 fail, 0 unmeasured** (results `6f2d2151afb9`, manifest `576e8ab5d8d1`; the manifest differs from layer 2b's `116324e9d629` by the one floor); the shell suite run alone
   **298 passed, 0 failed, 0 skipped in 342 s** (`layer3-suite-output.txt`; the same count as layer 2b: this layer changes no block of `bin/tests.sh`); the trimmer's suite
   **218 tests, OK, 2 skipped** (the same two, with the same reason, that the 181 skip before this layer); the layout suite 74 and the dashboard suite 354, both OK (the
   dashboard's tests load the trimmer for its trim-row couplings); the one shipped `.verify.sh` exit 0, as at every layer.
3. **The new tests exercise the new behaviour** (`layer3-measure-output.txt`, section 1): 37 tests are added (181 to 218), none removed. Run against the old tool
   (1.7.0, Part 1's), **33 of the 37 fail or error and none of the 181 old tests does**. The 4 that pass on both tools hold by design: they assert that a trim in the layout
   every adopter has today writes what it always wrote (the ledger entry, the pointer block's links, the legacy directory untouched, a legacy shard re-derived with the legacy
   prefix).
4. **The two new lines of the layout suite bite.** Run one at a time on a scratch copy, each with the file restored afterwards: one comment line added inside the embedded
   resolver block fails `test_each_copy_equals_the_modules_block_and_carries_exactly_one`; a root literal (`open('CHANGELOG.md')`) outside the block fails
   `test_each_resolved_tool_reports_no_site`. Each fails only its own test.
5. **The builder reproduces the commit.** `layer3-build.py` run on `c8c0b21` with the fork's `3ebe97d` as the source gives tree `c5c67cfff7cd`, equal to `98ca7fc`'s. Before it
   writes anything it asserts that the candidate's two trimmer files equal the fork's `3616b5f` blobs byte for byte, that the fixture is absent, and that the candidate's
   `tools/layout_resolver.py` equals the source's; a one-byte drift in the base makes it refuse and write nothing.
6. **The scanner reads 101 sites over 6 of 14 files** (121 over 7 at layer 2b): the trimmer's 20 are gone, and the layout suite now asserts it. Left: the dashboard 79, the
   budget gate 8, `bin/check-handoff` 6, `bin/check-ledger` 4, `bin/status` 3, `bin/check-links` 1 (`layer3-measure-output.txt`, section 3). Still not a gate.
7. **Against the two open pull requests, derived with `git merge-tree` (exit codes read, section 2 of the measure file):** #94's head (`972eb2cd6263`) now conflicts in **3
   files and 15 regions**: the trimmer 9, its tests 5, `.quality-gates.json` 1. Before this layer it was 2 files and 6 regions (the trimmer 1, the tests 5). Fifteen in three
   files is the count the plan derived for the fork's own tip (`../upstream-pr-composition-plan.md` §2.2), so the layer brings the candidate to the fork's divergence from #94 and
   no further. #92's head (`fa2bb5d464f9`): exit 0, no conflict. **The six regions outside the trimmer were read:** the gates region is the trimmer floor, 218 here against
   #94's own 181 (the candidate's floor before this layer), and the larger wins; the five test regions are one- or two-line comments that cite fork-internal things on the
   candidate's side ("fork Learning #58", "the plan's D2", "D2(i)", "P1's", "P2's") and say the same sentence without them on #94's side. They are Part 1's wording, not this
   layer's (the same five conflicted before it), and the scrub commit is where they go.

## 2. What it carries

| File | Change | Note |
|---|---|---|
| `starter-kit/methodology_trim.py` | +228 / -92 | 1.7.0 to 1.8.0: the shard directory and the link prefix follow the directory of the ledger being trimmed (`layout_for`); the action ledger comes from the embedded resolver; a half-migrated tree is refused; both archive directories are the trigger's history; the resolver block, byte for byte the module's; the tie rule, which takes no request (the framework anchor decides) |
| `tools/test_methodology_trim.py` | +497 / -1 | 218 tests (181): a ledger under `methodology/`, the proof across both layouts, the history across two archive directories, the legacy layout byte for byte what it was |
| `tools/fixtures/trim-verify-template-1.7.0.sh` | +406 | new: 1.7.0's own proof script, frozen; the test `test_the_proof_template_differs_from_1_7_0_in_its_parameter_lines_only` requires the 1.8.0 template to equal it modulo the version and three parameter lines |
| `tools/test_layout_resolver.py` | +3 / -2 | `COPIES` and `RESOLVED` gain the trimmer: it is the second tool that carries the block and the second that must read 0 sites |
| `.quality-gates.json` | +1 / -1 | `trimmer-unit-tests` 181 to 218, the count the clone measured: tightened by exactly what this adds |

**What the layer does to a reader of the tool:** a project that moved its ledgers under `methodology/` keeps trimming them, the shard lands in `methodology/archive/` and its
links climb one level; a project with the ledger at the root gets what 1.7.0 wrote (the 4 tests above), the version and three proof parameter lines aside.

## 3. What it leaves out, and why

| Not at this layer | Why |
|---|---|
| The context-budget gate (8 sites), the checkers' layout reading (`bin/check-handoff` 6, `bin/check-ledger` 4), the dashboard (79), `bin/status`, `bin/check-links`, `bin/sync`, `bin/migrate-layout`, the prose | later layers (plan §3) |
| A `bin/tests.sh` change | none needed: of the 341 lines `git diff c8b9ddd..3ebe97d -- bin/tests.sh` adds or removes, none cites the trimmer, and the candidate's three existing lines that cite it pass unchanged (suite 298/0/0) |
| `tools/fixtures/handoff-ledger-2-records.md` | the fork's, read by its `bin/tests.sh` Test 38 (`bin/check-handoff`'s per-record budget, a canonical-only checker: themes E and F stay on the fork); the trimmer's tests read only the one fixture carried here and the seed fixture Part 1 carried |

## 4. Decisions I took that the plan did not

1. **The two files come from the fork's tip** (`3ebe97d`), not from a replay of two commits: the builder's base assertion makes the result the same as replaying `ee89b24`
   (1.8.0) and `26bc97a` (the tie rule) onto `3616b5f`, and `git log 3616b5f..3ebe97d -- <the two files>` names those two and no more. `3616b5f` is the one fork commit whose blobs
   equal Part 1's two files (found by comparing blobs over the last 30 commits touching them), so the base is a measurement, not a recollection.
2. **The fixture is carried, verbatim, as a new file.** The 1.8.0 tests read it, so a layer without it fails the test that reads it (its path is a constant; the file is read when that test runs). Its 10 lines that cite a
   `BL-` number are inside 1.7.0's own proof script. **The scrub must not edit the fixture alone:** the test compares the 1.8.0 template to it,
   so a comment changed in the template is changed in the fixture the same way, or the test goes red.
3. **No `ResourceWarning` lines.** Layer 2b's verbatim test file printed 83; this one prints 0 under unittest's default warnings (counted from the output of the run behind section 1 of the measure file; the file saves that run's tail, not the count). Nothing to scrub there.
4. **The floor is measured, not copied:** the fork's is 218 too, but the builder takes `--trimmer-count` from a run of the suite in the clone, as 2b did.
5. **Scrub input** (a coarse regular expression over the layer's added lines): 14 lines cite a `BL-` number (3 in the tool, 10 in the fixture, 1 in the tests) and 5 cite a phase as "P1", "P2"
   or "P3" (3 in the tool, 2 in the tests). None cites a session number, a `docs/planning/` path, a fork learning or a failure-mode number. The commit message of the layer carries none of them. The
   scrub is its own commit after the layers.

## 5. What this does not show

The surface is this machine, with the load average between 6 and 42 across the session: clean clones, serial runs, `nohup` and done-files. **Not shown:** a trim of a real adopter's ledger
under `methodology/` (the 218 tests build their own repositories in both layouts; the migration tool's rehearsal over real adopters is a later layer); Windows; a maintainer's machine; upstream
CI (there is none); the scanner at 0 (it is 101); the candidate merged with #94 (the conflict list is derived and its non-trimmer regions read, not resolved); that the shipped proofs written by
upstream's older trimmers still verify under this one (the one tracked proof, `docs/archive/CHANGELOG-through-2026-09-30.md.verify.sh`, exits 0, which is one shard, not a population).

## 6. Next

**The context-budget gate** (plan §3, fourth): `starter-kit/context_budget.py`, its tests and its layout reading, with the 8 sites the scanner still reads there. First read plan §3 and §4 for which of
the fork's checkers (`bin/check-handoff` 6 sites, `bin/check-ledger` 4) the pull request carries and which stay on the fork as themes E and F, and measure what the layer does to #94's three conflicted
files (a budget-gate change touches none of them). Re-run this layer: `bash layer-verify.sh <candidate> 98ca7fc9744104875c409c96274e24dcf4e989c7`; rebuild: `python3 layer3-build.py <fork> 3ebe97d
<clone-at-c8c0b21>`, then once more with `--trimmer-count 218`. PR2 is now five checkpoints spent of the plan's "two to four" and the budget gate, the dashboard, the sync layers, `bin/migrate-layout`,
the prose and the scrub remain, so that figure wants restating at PR4.
