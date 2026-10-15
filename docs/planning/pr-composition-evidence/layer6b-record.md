# PR2, Part 2, the checkers' layer: `bin/check-ledger` and `bin/check-handoff` read a project in either layout

**Status: BUILT, verified in a clean clone, nothing sent.** Session S320, 2026-10-14. This is the tenth PR2 session
(`../upstream-pr-composition-plan.md` §3 and §5; D5 amended at S319, `layer7-record.md` §6 named this layer). The local ref `pr2/candidate` moved
`0aa1897` to **`505541c`**, two commits, 7 files, +364 / -26; the candidate is now 12 commits, 29 files, +15,279 / -1,085 against `upstream/main` (`f34769f`).
Every figure below is printed by a script in this directory or by a command named beside it; the saved outputs are `layer6b-*-output.txt`.

## 1. The answer first

1. **Two commits of at most five files, each green** (the cap is per commit; `SAFEGUARDS.md`):

   | Commit | Files | +/- | What |
   |---|---|---|---|
   | `a459b8b` `feat(checkers)` | `bin/check-ledger`, `bin/check-handoff`, `tools/test_layout_resolver.py` | +134 / -19 | both tools read the ledger at the root or under `methodology/`; `COPIES` lists both (its test fails for a tool that carries the block and is not listed) |
   | `505541c` `test(checkers)` | `tools/test_checker_layouts.py` (new), `bin/tests.sh`, `bin/check-layout-literals`, `tools/test_layout_resolver.py`, `.quality-gates.json` | +230 / -7 | the suite (11 tests), its wiring and gate, the scanner no longer exempts the two tools |

2. **`bin/check-ledger` is the tip's blob whole (`d55209d`).** Its entire difference from upstream's `a96b641` is the layout reading: two hunks (`@@ -29,6 +29,37 @@` and `@@ -94,19 +125,55 @@`), +72 / -5, printed from `git diff pr2/candidate~2 HEAD -- bin/check-ledger`
   (the resolver block and three constants; `default_ledger()`, `shard_dirs()` and `main()`'s half-migrated refusal and archive walk). Nothing is hand-built there.
3. **`bin/check-handoff` is upstream's `d314c4d` plus seven edits (+60 / -13), blob `c4b6028`; the tip's is `2eaddac`, +551 / -45 further on.** The seven edits are the resolver block with `LEDGER_NAME`, `NEW_DIR` and the
   `HalfMigrated` exception; `GATES_MANIFEST`'s same-line marker; two message lines' markers; `default_path()`; the two `main()` markers; and `main()`'s refusal of a half-migrated tree (exit 1, naming both copies).
   **Every inserted string is cut from the tip's file** (the builder asserts each occurs in it before writing). **Not carried, because they are not layout:** the stub schema, the answer-slot rule, the locator-form rule, the record budget,
   `--archived`, the unmeasured-gate lint (plan §4 row F: canonical-only, the fork's).
4. **Verified: `layer-verify.sh` on `505541c` in a clean `--no-local` clone** (`layer6b-verify-output.txt`, 9 min 37 s, load average 11.95 at launch): the ratchet **16/16 pass, 0 fail, 0 unmeasured, results `e960a10e187f`, manifest `8169f9089eea`**;
   `tests-sh-passed` reads 300 (the floor, 299 plus the one new wiring block); `checker-layout-unit-tests` 11; `layout-unit-tests` 76 (unchanged: see §4.2); the scanner **14 files, 0 sites** (0 path, 0 text), 124 acknowledged;
   the one shipped `.verify.sh` proof exit 0. `a459b8b` alone: the shell suite **299 passed, 0 failed, 0 skipped** (5 min 22 s, `layer6b-commit1-suite-output.txt`).
5. **The scanner series reaches zero for these two.** `bin/check-handoff` read **6** sites and `bin/check-ledger` **4** when read by hand on the parent (`layer6b-measure-output.txt` §3); the layer reads 0, with 124 acknowledged over 14 files
   (the parent: 12 files). The only files exempt from the scan are now the manifest, the shell suite and the dashboard's byte-identical twin.
6. **The migration tool's suite needs nothing more from the checkers.** `layer6b-probe.sh` puts the layer's own commits, the tip's `bin/migrate-layout`, its suite and its sync suite together: without the prose the same **10 of 23** fail as with the
   tip's whole checker files (`layer7-probe-output.txt`, state `checkers`); with the tip's 23 framework documents added, **the whole 280-test suite runs OK in 361 s** (`layer6b-probe-output.txt`). S319's open question, *which hunks make the 280 pass*,
   is answered: these seven edits plus the prose, and nothing else the tip's two files carry.

## 2. What was measured, and how

| Check | Result | Output |
|---|---|---|
| The new tests against the PARENT's tools (`layer-contrast.sh`) | **6 of the 11 fail on the old tools**; 5 pass on both | `layer6b-contrast-output.txt` |
| Mutants aimed at code, round 1 (14 code lines, 2 markers) | **16 of 16 killed** (the 2 markers by the scanner gate, which no unit suite reads) | `layer6b-mutate-round1-output.txt` |
| Mutants, round 2, aimed at behaviours no test named | **on the 8-test tree: 3 killed, 3 SURVIVED** (`--file` ignored in each checker; `check-ledger`'s no-ledger report); after three tests were added: **6 of 6 killed** | `layer6b-mutate-round2-before-output.txt`, `layer6b-mutate-round2-output.txt` |
| A real corpus (`layer6b-realtree.sh`) | the fork's own ledgers at `fc94978` (`CHANGELOG.md` 214,849 B, `HANDOFFS.md` 27,411 B, two receipts, 24 `CHANGELOG` shards), placed legacy, under `methodology/`, and under `methodology/` with the shards still in `docs/archive/`; the OLD and the NEW tools run: **output and exit code equal old-to-new on the legacy tree, and equal across all three placements** (paths normalised), for `check-ledger`, `check-ledger --all`, `check-handoff`, `check-handoff --all` | `layer6b-realtree-output.txt` |
| The builder (`layer6b-build.py`) reproduces the tree and refuses on drift | built tree `bc9d4c00f6d5` = the layer's tree; one byte appended to the candidate's `bin/check-handoff` is refused ("blob `e4376f7`, not upstream's `d314c4d`"), 0 dirty paths | `layer6b-measure-output.txt` §2 |
| The two open pull requests (`git merge-tree`) | #94: **the same 15 regions in the same 3 files** at the parent and at the layer (1 in `.quality-gates.json`, 9 in `starter-kit/methodology_trim.py`, 5 in `tools/test_methodology_trim.py`); #92: clean at both. The layer adds no conflict | `layer6b-measure-output.txt` §4 |

**The mutation round that mattered.** The 8-test cut of the tip's suite (its other seven tests drive `bin/check-overhead` and `bin/model-report`, which the candidate lacks) killed all 16 round-1 mutants and left three behaviours unnamed by any test:
the refusal message of both checkers says *"name the file with `--file`"* and no test showed that this works, and `check-ledger`'s report of where it looked when there is no ledger. Three tests were added (the suite is 11; the tip's has none of these three). Each is
the mutant it kills, in its name. The contrast shows them passing on the OLD tools too: they pin behaviour the old tools already had and the layer must keep, which is what a regression pin is.

## 3. Decisions I took that the plan did not

1. **Two commits, not one.** The plan's list is seven files; the cap is five per commit. `COPIES` goes with the tools (its test fails otherwise); the suite, its wiring, its gate and the scanner's scope go together.
2. **The pin test was REPLACED, not deleted.** The plan says the layer "deletes the layout suite's pin test" (`test_the_two_checkers_that_do_not_read_the_layout_are_not_scanned_and_say_why`). Deleted, `layout-unit-tests` reads 75 against its floor of 76, and a floor cannot fall without plan mode
   (`SAFEGUARDS.md`). It is replaced by `test_only_the_manifest_and_the_suite_are_exempt_from_the_scan`, which pins what is still exempt: a new exemption is then a deliberate edit of that list. The count and the floor are unchanged.
3. **Three tests beyond the tip's suite** (§2). **The same three are absent from the FORK's suite** and its `checker-layout-unit-tests` gate (15): porting them is a fork change this session did not make (a candidate for his call, a backlog row if he asks).
4. **The suite is cut, not rewritten.** The tip's `tools/test_checker_layouts.py` minus `TestCheckOverhead` and `TestModelReport`, the two constants only they used, and two words in the module docstring; the builder refuses if the cut text still names either tool.
5. **`bin/check-layout-literals` is now the tip's blob (`32a683e`)**: the two lines layer 6 added were the only difference from the tip's scanner, and deleting them is the whole edit.
6. **Not touched:** `RESOLVED` in the layout suite (the `layout-literals` gate at 0 reads the same files); the checkers' own docstrings (the Usage lines still say `./HANDOFFS.md`, as the tip's do); `starter-kit/` prose (the next layer).

## 4. What this does not show

The surface is this machine (load average 3 to 12 over the runs): clean clones, serial runs, `nohup` and done-files. **Not shown:**
- the checkers on a real ADOPTER's tree under `methodology/` (the real-corpus check is the fork's own ledgers placed three ways, and the 11 tests build scratch projects); `check-handoff`'s 144 archived shards (no carried command reads a shard: `--archived` is the fork's);
- that the prose layer the pull request will carry equals the tip's 23 documents (the probe takes the tip's; the 280 are a statement about the pair, not about the prose layer's own commit);
- Windows; a maintainer's machine; upstream CI (there is none); the candidate merged with #94 (derived, not resolved);
- the first verification of this layer (on the 8-test tree, 16/16, results `593ae11339ea`) is superseded: the three tests changed the tree, and the run above is on `505541c`.
**Scrub input** (`layer6b-measure-output.txt` §5, a coarse regular expression over the 364 added lines): backlog codes on 3 lines, a phase ("P4") on 4, a plan section or decision on 5, a session number and a `docs/planning/` path on none;
the commit messages carry none. The wiring comment in `bin/tests.sh` still says "the evidence script of the P4 session": the scrub's.

## 5. Next

**The prose layer, then `bin/migrate-layout`** (plan §3 as amended). The prose: every Markdown file under `starter-kit/` and `workstreams/` plus the three root framework documents (the probe's 23 files, 17 differing from the candidate's, +102 / -67), which also carries `check-links --layout both`
(Test 10's block, which reads red on the candidate until then: `layer6-record.md`, the table of `bin/tests.sh` blocks) and clears the dangling links once under `methodology/` (34 on the candidate by `layer7-record.md` §1.4, 35 by S318). DERIVE first, as every layer: which of the 23 the prose layer needs and what its tests are.
**Then `bin/migrate-layout`**: `layer7-build.py` is a DRAFT and must be re-based: its `COPIES_OLD` (`layer7-build.py:70`) ends `"bin/sync", "bin/status", "bin/check-links")` and the candidate's now ends `"bin/check-ledger", "bin/check-handoff")` after the checkers' line; its gates' anchor and the paired gate stay as `layer7-record.md` §3 and `BL-109` say.
Re-run this layer: `bash layer-verify.sh <candidate> 505541c`; rebuild: `python3 layer6b-build.py <fork> 4a521e4 <clone-at-0aa1897> --stage tools`, commit, `--stage suite`, then `--stage suite --checker-count 11 --passed 300`;
the rest: `layer6b-measure.sh`, `layer6b-mutate.py <clone> --round 1|2`, `layer6b-probe.sh`, `layer6b-realtree.sh`, `layer-contrast.sh`.
