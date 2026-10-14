# PR2, Part 2, layer 5: the dashboard 2.22.0, the dashboard reads a project that keeps its methodology files under methodology/ as it reads one that keeps them at the root

**Status: BUILT and verified, un-pushed, nothing sent.** Session S317, 2026-10-14. This is PR2's seventh checkpoint (`../upstream-pr-composition-plan.md`
§3 and §5; Part 1 is [`part1-record.md`](part1-record.md), layer 1 [`layer1-record.md`](layer1-record.md), layer 2 [`layer2-record.md`](layer2-record.md), layer 2b
[`layer2b-record.md`](layer2b-record.md), layer 3 [`layer3-record.md`](layer3-record.md), layer 4 [`layer4-record.md`](layer4-record.md), whose §7 named this layer). Every figure below is printed by a
script in this directory or by a command named beside it; the saved outputs are `layer5-*-output.txt`.

## 1. The answer first

1. **The layer exists.** Local branch `pr2/candidate` is now `dd581fe`, one commit on layer 4's `e9c5cb8`: **5 files, +1,350 / -238** (`git diff --numstat e9c5cb8 dd581fe`, summed: the two dashboard
   twins +370 / -115 each, their tests +595 / -4, the layout suite +13 / -2, the gates file +2 / -2); the candidate as a whole is 7 commits and 21 files, +13,455 / -959 (`git diff --numstat upstream/main pr2/candidate`,
   summed; the layer adds no file, every one of its five was already in the candidate). The scratch clone has no remote configured, and `git ls-remote --heads origin 'pr2*'` lists nothing.
2. **It is green on upstream's tree, in a clean `--no-local` clone** (`layer-verify.sh`, `layer5-verify-output.txt`, at most 8 min 5 s): `quality_ratchet.py --run` **13/13 pass,
   0 fail, 0 unmeasured** (results `88f487475334`, manifest `4fa84819da44`; the manifest differs from layer 4's `5d02c560b035` by the two floors); the shell suite run alone
   **298 passed, 0 failed, 0 skipped in 4 min 55 s** (`layer5-suite-output.txt`; the same count as layers 3 and 4: this layer changes no block of `bin/tests.sh`, and no line of that file's diff from `c8b9ddd` to the fork tip cites the dashboard: 0 of them);
   the dashboard suite **395 tests, OK** (354 before this layer); the layout suite 75, OK (74); the budget gate's 163 and the trimmer's 218 unchanged and read by the ratchet; the one shipped `.verify.sh` exit 0, as at every layer.
3. **The new tests exercise the new behaviour** (`layer5-measure-output.txt`, section 2, made by `layer-contrast.sh` and `layer-outcomes.py`): 41 dashboard tests are added (354 to 395), none removed. Run against the old
   dashboard (2.21.0, Part 1's), **32 of the 41 fail or error**. **The 9 that pass on both hold by design**, each read: six assert what 2.21.0 already did (a copy of the dashboard at the project root is unchanged;
   a directory merely called `methodology` with no git root above it is not a project's subdirectory; a half-migrated tree is still scored for the files it has; the item
   labels are the same names in every layout; a floor lowered in place is a loosening, the control for the move-commit test beside it; a manifest deleted after the move is still a removal), one pins the absence of a row
   2.21.0 never raised (no other shape raises the half-migrated row), and two are anti-laundering and parity pins (a script that only sits in an archive directory stays source unless all three conditions hold; the docs-directory point
   belongs to the project's own `docs/`, pinned on purpose in both directions). **One old test, of the 354, fails on the old dashboard**: `TestFmtRatioAndTwins.test_dashboard_version` pins the version number and the source text, which
   this layer moves to 2.22.0: a changed pin, not an added test. The layout suite: the one added test fails on the old tree, and **3 old tests fail there** because `COPIES` and `RESOLVED` now name a tool that
   2.21.0 has no resolver block in and 79 root literals in: the lists doing their job.
4. **The new lines of the layout suite bite.** Run one at a time on the layer's dashboards, each with the files restored afterwards (section 3): one comment line added inside the embedded resolver block of the
   `starter-kit/` copy fails `test_each_copy_equals_the_modules_block_and_carries_exactly_one`; the same line in the `tools/` twin only fails `test_the_dashboards_canonical_only_twin_carries_the_same_block`, **the one test this layer adds
   to that suite, and the only one that sees that twin** (the directory walk reads `starter-kit/` and `bin/`); a root literal (`open('CHANGELOG.md')`) outside the block fails `test_each_resolved_tool_reports_no_site`.
   Each fails only its own test (`FAILED (failures=1)`).
5. **The builder reproduces the commit.** `layer5-build.py` run on `e9c5cb8` with the fork's `aec8166` as the source gives tree `cc072f493724`, equal to `dd581fe`'s. Before it writes anything it asserts that
   the candidate's two dashboard twins equal the fork's `75f665e` blobs byte for byte, that the source's two twins equal each other, and that the candidate's `tools/layout_resolver.py` and
   `tools/layout_fixtures.py` equal the source's; a one-byte drift in the base makes it refuse and write nothing (run, section 4: `refused: starter-kit/methodology_dashboard.py in the candidate is not 75f665e's blob ...`, the clone left with no dirty path).
6. **The scanner reads 14 sites over 4 of 14 files** (93 over 5 at layer 4): the dashboard's 79 are gone, and the layout suite now asserts it. Left: `bin/check-handoff` 6, `bin/check-ledger` 4, `bin/status` 3, `bin/check-links` 1
   (section 5). Still not a gate; exit 1 is the count.
7. **Against the two open pull requests, derived with `git merge-tree` (exit codes read, the first line read as a tree, section 6):** #94's head (`972eb2cd6263`) conflicts in **3 files and 15 regions**, the same as before this layer
   (the trimmer 9, its tests 5, `.quality-gates.json` 1): **the layer adds none**, though it edits two other floors in the file whose one region is already in conflict; #92's head (`fa2bb5d464f9`): exit 0, no conflict.

## 2. What it carries

| File | Change | Note |
|---|---|---|
| `starter-kit/methodology_dashboard.py` and `tools/methodology_dashboard.py` | +370 / -115 each | 2.21.0 to 2.22.0, the sum of 13 fork commits (`0d0da93` to `ffc260b`, in order): the tool embeds the layout resolver; the checklist items keep their names and are located through it; a project whose runner is under `methodology/` is still an adopter; a half-migrated tree is a high risk naming both paths; the file walk, the installed-source fingerprint, the ledger locator and the trim and read-cap rows read either layout; `--sync` resolves each target's layout, refuses a half-migrated project by name, and a copy inside `methodology/` finds its project and writes beside itself; the quality-gate read finds the manifest where it lives and follows its history across the move; the publisher's checklist follows its own moved ledgers |
| `tools/test_methodology_dashboard.py` | +595 / -4 | 395 tests (354): 41 added in classes named for the fork's phase (scrub), one re-pinned. **It is the fork tip's file with Part 1's portability edits re-applied** (section 4, decision 2), not a copy of the tip |
| `tools/test_layout_resolver.py` | +13 / -2 | the dashboard in `COPIES` and in `RESOLVED`, and `test_the_dashboards_canonical_only_twin_carries_the_same_block`; the file's other `COPIES` entries (the checkers, the sync layer, the migration tool, the close-out report) are later layers' or not carried |
| `.quality-gates.json` | +2 / -2 | `dashboard-unit-tests` 354 to 395 and `layout-unit-tests` 74 to 75, the counts the clone measured: tightened by exactly what this adds |

**What the layer does to a reader of the tool:** a project that moved its framework files under `methodology/` is scored, flagged and synced as the project it is; a project at the root gets what 2.21.0 did (the 9 tests above that hold on both).

## 3. What it leaves out, and why

| Left out | Why |
|---|---|
| The sync layers, `bin/migrate-layout`, the prose | later layers (plan §3) |
| `bin/check-handoff` (6 sites) and `bin/check-ledger` (4) | open since layer 4 (its record, §7): plan §4 does not name the layout reading of these two tools. It binds at the sync layer, where `layout-literals` is first declared at 0; this layer's tests and scanner do not need it |
| The dashboard's own mutation pass | it was the fork's (the survivors became tests in `631c87c`, `c049bdf`); it is not re-run on the candidate. The three mutants above are of this layer's new layout-suite lines only |
| The fork's `CHANGELOG.md`, `docs/planning/BACKLOG.md` and the directory plan's edits inside those 13 commits | the fork's own ledger, backlog and plan; plan §4 carries none of `CHANGELOG.md` or `docs/` except the evidence |
| `tools/layout_fixtures.py`, which `ffc260b` also changed | already the tip's in the candidate (asserted by the builder, as at layer 4) |
| A `bin/tests.sh` change | none needed: no line of `git diff c8b9ddd..aec8166 -- bin/tests.sh` cites the dashboard, and the existing blocks that run it (Test 18's unit-test line, Test 19's twin and version comparison, the sync blocks) pass unchanged |

## 4. Decisions I took that the plan did not

1. **The twins come from the fork's tip** (`aec8166`; its dashboard files are `6a31474…` at both paths, equal to each other), not from a replay of 13 commits. The base is a measurement: the candidate's twins equal the fork's blobs at `75f665e`
   (2.21.0, the commit that made them so); from there **exactly 13 commits touch the three dashboard files on both walks** (first-parent, and `--ancestry-path --full-history 75f665e..aec8166`). S316's handoff said 17 since `3616b5f` (16 on the first-parent walk); the exact count
   is 16 on both exact walks, 3 of them before `75f665e` (history the base already contains) and 13 after, so the 17 was the plain walk's figure, the gotcha S316's own receipt names. What the 13 carry beyond the dashboard: the fork's ledger, `tools/test_layout_resolver.py` (`8fac99b`, `ffc260b`), `.quality-gates.json` (`631c87c`, `c049bdf`), `tools/layout_fixtures.py` (`ffc260b`, already in the candidate), and two planning documents.
2. **The test file is a three-way merge, not a copy.** The candidate's file is not any fork blob: it is `75f665e`'s plus Part 1's portability edits (+9 / -34 as `git diff --numstat` reads it: the two tests that read the fork-only
   `docs/planning/BACKLOG.md`, `test_backlog_is_watched_but_never_given_a_trim_row` and `test_the_fleet_facts_the_disposition_was_decided_on_are_stated_not_assumed`, are removed, and `TestS38TrimTriggerRow`'s ledger floor `checked >= 6` is relative to the ledgers that exist). Copying the tip would
   put both tests back and they fail on upstream's tree. `git merge-file` (ours the candidate's, base `75f665e`'s, theirs the tip's) re-applies the difference; the builder refuses unless the merge has no conflict, unless the result
   differs from the tip by exactly +9 / -34, unless the two tests are absent from it, and unless the relative floor is in it once. This is the layer's one new risk and the suites above are its check.
3. **The floors are measured, not copied:** the fork's dashboard floor is 397 and the candidate's is 395, which is 397 less the two removed tests; the layout floor is 75 in both.
4. **No carried fixture, five files exactly:** the cap per commit (`SAFEGUARDS.md` §Blast Radius Limits). The layer needed no new file.
5. **Scrub input** (`layer5-measure-output.txt`, section 7; a coarse regular expression over the layer's added lines): the dashboard's 370 added lines, in each twin, cite a `BL-` number on 11, a phase ("P5") on 9, a session number on 2, a `docs/planning/` path on 2, a failure-mode number on 1 and a plan section on 8;
   the tests' 595 cite `BL-` on 2, a phase on 3, a session on 3 and a plan section on 5, and the new test classes carry the fork's phase in their names (`TestBL101P5*`); the layout suite and the gates file cite none.
   The commit message of the layer carries none of them. The scrub is its own commit after the layers.

## 5. Against the two pull requests, and the scanner

`layer5-measure-output.txt`, sections 6 and 5. #94 (`972eb2cd6263`) and #92 (`fa2bb5d464f9`) were the heads when this ran (`gh pr view`, 2026-10-14, no comment or review on either).
The scanner's per-file list at the layer: `bin/check-handoff` 6, `bin/check-ledger` 4, `bin/check-links` 1, `bin/status` 3; at its parent the dashboard's 79 were listed too.

## 6. What this does not show

The surface is this machine, with the load average between 5 and 23 across the session: clean clones, serial runs, `nohup` and done-files. **Not shown:** the dashboard run against a real adopter's tree under `methodology/`
(the 41 added tests build their own fixture trees in both layouts; the fork's adopter rehearsals were its own, not re-run on the candidate); `--sync` writing into a real adopter; Windows; a maintainer's machine; upstream CI (there is none);
the scanner at 0 (it is 14); the candidate merged with #94 (derived, not resolved); the dashboard's behaviours beyond the three mutants of the layout lines (the fork's mutation pass, not re-run).

## 7. Next

**The sync layers** (plan §3, sixth): DERIVED (`git diff --numstat pr2/candidate aec8166`, this session): `bin/sync` +145 / -32, `bin/status` +85 / -21, `bin/check-links` +150 / -47, `bin/_manifest_reader.py` +65 / -7 (`bin/_manifest.py` differs by two comments only),
`tools/test_sync_layouts.py` +987 (new), `bin/tests.sh` blocks, `.quality-gates.json` (the tip declares `sync-layout-unit-tests` and `layout-literals`, which the candidate lacks, among other changes), and `tools/test_layout_resolver.py` (the three tools in `COPIES` and `RESOLVED`): more than five files, so two checkpoint commits or a split.
**Decide first, or take the plan's amendment:** the 10 remaining sites of `bin/check-handoff` and `bin/check-ledger` (layout reading of upstream's two checkers; plan §4 silent): `layout-literals` (max 0) cannot be declared at the sync layer unless they are carried or the gate lists them as exempt.
Re-run this layer: `bash layer-verify.sh <candidate> dd581fe`; rebuild: `python3 layer5-build.py <fork> aec8166 <clone-at-e9c5cb8>`, then once more with `--dashboard-count 395 --layout-count 75`; the whole measurement: `bash layer5-measure.sh <fork> dd581fe e9c5cb8 aec8166`.
PR2 is now seven checkpoints spent of the plan's "two to four": the sync layers (two commits), `bin/migrate-layout`, the prose and the scrub remain.
