# PR2b: how to add the last twelve commits of the candidate, grouped (a planning record, S393, 2026-10-28)

**Status: DRAFT, waiting for his answers (section 5). Nothing was built.** `pr2b/candidate` is still `d818ca17` (21 commits on `upstream/main` `d50ce290`), `pr2/candidate` is still `3cba1e50`, and nothing was sent to `KJ5HST/methodology`. The only other things made are the script, its output and a throwaway clone where the commits were tried.
**Declared budget: 14,000 B**, one read. This extends [`../upstream-pr-composition-plan.md`](../upstream-pr-composition-plan.md) §5 (the PR2b row); that file is at its own 30,000 B cap, so it is not edited. Every figure below is printed by [`pr2b-grouping-measure.py`](pr2b-grouping-measure.py) into [`pr2b-grouping-measure-output.txt`](pr2b-grouping-measure-output.txt) (cited as `out:LINE`), run serially and saved from the second run (load average 103 at its start and 61 at its end, other projects' test runs; 216 in the first), so no timing here is a clean measurement.

Words used: a **layer** is one or more commits added to `pr2b/candidate` and checked together in a clean clone; a **group** is a layer of several commits. **Numbers** (21 to 33) are the commit's place in the old candidate, `git log --reverse upstream/main..pr2/candidate`. **Phase A** is the scrub's first seven commits (21 to 27), **phase B** its last three (28 to 30), names from [`scrub-record.md`](scrub-record.md) §1.

---

## 1. The answer first

1. **Twelve commits remain**: numbers 21 to 30, 32 and 33 (31 `ced2c823` is already in the tip as a replay; 34 is dropped as superseded). Read by comparing each commit's before and after, not by its subject (`out:7-72`): **21 to 25, 27 and 32 change only comments, docstrings and the reason text of gates** (syntax tree equal once docstrings are dropped, shell equal once full-line comments are dropped, gate file equal once every `why` is masked); **26 is the same kind, but cannot be replayed**; **28 and 29 change string literals** (text a program prints or a test asserts on); **30 changes shell lines** (test titles, selftest labels) and one gate reason; **33 is code** (it restores two of upstream's tests and raises a gate floor).
2. **The question S389 left unasked ("do 21 to 30 count as documentation?") has a measured answer, and the decision is still his.** 21 to 27 and 32 are documentation by any reading: no code token changes. 28 to 30 are not comments, so they should not ride in the documentation group; the scrub record already says he "can accept A and refuse B" (§1, point 2). 33 is neither.
3. **Order matters far less than feared.** Alone onto the tip, 9 of 12 apply clean and 26, 30 and 33 conflict (`out:74-86`). **In order, 11 of 12 apply clean and each equals its original by `git patch-id --stable`; only 26 conflicts** (`out:89-106`). 30 conflicts alone but is clean after 22, and 33 conflicts alone but is clean after 27 (`out:84,86,132-133`). The three orders that include all eleven give the same tree, `866ea59c8738` (`out:122-124`).
4. **At the end the series is nearly clean of fork tokens.** Fork-token lines (backlog codes, session numbers, plan references and the like, by `scrub-derive.py`): **639 in 28 files at the tip, 33 in 6 files after the eleven** (`out:147-181`). The 33 are: **17 that only 26 reaches** (the trimmer 12, its tests 5, all comments and docstrings), **11 in a frozen test fixture no commit touches** (its lines copy text upstream's trimmer already carries: BL-27, BL-28 and BL-36 occur 8, 3 and 5 times in `upstream/main:starter-kit/methodology_trim.py`), **5 left on purpose** by the old scrub (scanner data, a grepped pattern, a fixture path).
5. **The eleven add nothing to the two open pull requests' conflicts**: #98 reads 5 regions in 3 files and #96 reads 4 in 3, before and after (`out:189-197`); the read-set budget is unchanged (resident 51,487 B of 59,168 B, read-set 70,048 B, `out:199-207`); and the dashboard suite at the replayed tip is **397 tests, OK**, which is the floor commit 33 sets (`out:209-215`).
6. **Recommendation: two layers, two sessions.** **Layer 22**, the documentation group: 21, 22, 23, 24, 25, **26′** (written by hand, section 3), 27, 32. **Layer 23**: 33, then 28, 29, 30, with B last so that if he refuses it, it is a tail of three commits to drop. The series is then 33 commits on `d50ce290`; PR3's table and PR4's text are re-run, then PR5.

## 2. The twelve (hash = the old candidate's; sizes from `out:7-72`)

| # | Commit | Files, lines | What it changes (proved) | Alone | In order | Edits a file an open pull request edits |
|---|---|---|---|---|---|---|
| 21 | `c933b0f9` | 5, +19/−19 | sync layer: comments, docstrings | clean | clean | no |
| 22 | `d31c25da` | 5, +40/−40 | shell suite, hook, checkers: comments | clean | clean | #96: `bin/tests.sh` |
| 23 | `c1cdc2ec` | 5, +55/−60 | resolver, fixtures, their tests: comments | clean | clean | no |
| 24 | `71e00e89` | 4, +31/−31 | ratchet, budget gate, tests: comments | clean | clean | no |
| 25 | `ea751caa` | 2, +75/−77 | migration tool and suite: comments | clean | clean | no |
| 26 | `2276f4ef` | 2, +25/−26 | trimmer and tests: comments | 5 regions | **5 regions** | #98: both files |
| 27 | `72e0c991` | 3, +404/−437 | dashboard (both copies) and tests: comments | clean | clean | no |
| 28 | `8ace51e8` | 3, +13/−13 | string literals: text the migration tool and scanner print | clean | clean | no |
| 29 | `ccd5620e` | 3, +17/−17 | string literals: dashboard output and its tests | clean | clean | no |
| 30 | `28f99a70` | 3, +13/−13 | shell lines (titles, selftest labels), one gate reason | 1 region | clean | both: `.quality-gates.json`; #96 also `bin/tests.sh` |
| 32 | `a62bfecf` | 4, +8/−5 | stale statements in two gate reasons, a header and a comment (both dashboard copies) | clean | clean | both: `.quality-gates.json` |
| 33 | `cfcc713b` | 2, +56/−10 | **code**: two tests, gate floor 395 → 397 | 1 region | clean | both: `.quality-gates.json` |

Every commit is within the 5-file cap (`SAFEGUARDS.md`), because each is replayed whole. The 11 replays together touch 25 files, +726/−717 (`out:107`).

## 3. What each measurement says

- **Why 26 cannot be replayed.** The tip's trimmer is upstream's 1.8.2 plus the fork's layout hunks, labelled 1.9.0; the commit was made against the old candidate's trimmer text (its version line still read 1.8.0). Five regions (`out:94-99`): the version line, three one- or two-line comments in the tests, and one 810-line block of upstream's tests for #93 (ours) against a one-line comment (theirs). So **26′ is a new commit, not a replay**: the tip's blobs plus edits, under the old scrub's rules (`scrub-record.md` §3: only fork tokens go; a sentence meaningful only inside the fork is deleted, not reworded). Its target is the 17 lines above, all comments, trailing comments and docstrings (`pr2b-grouping-derive-after-output.txt`: none behaviour-bearing in either file).
- **Why 33 is needed.** Upstream's `tools/test_methodology_dashboard.py` has `test_bare_dry_run_refuses_instead_of_writing` and `test_a_normal_run_still_writes`; the tip has neither (checked by grep at both refs). Without 33 the pull request deletes two upstream tests. With it, the suite runs 397 tests and the gate floor in the tree is 397 (`out:215`).
- **The inertness proof.** `scrub-proof.py` over tip → after 32 (A without 26, B, 32): **holds**, exit 0 (`out:136-139`). With 33 added it fails, in exactly two files, `.quality-gates.json` (a floor, not a `why`) and the dashboard test file (code) (`out:140-145`): the proof is right to refuse a code commit, so 33 is kept out of the scrub's range.
- **Dependencies.** 30 needs 22: alone it conflicts in `bin/tests.sh` (`out:129`), after 22 it is clean (`out:132`). 33 needs 27: alone it conflicts in the dashboard tests (`out:131`), after 27 it is clean (`out:133`), and "A, 33" is clean without B (`out:126`). 32 is clean before B (`out:123-124`) and after it (`out:104`).
- **Leftovers, by name.** `tools/fixtures/trim-verify-template-1.8.2.sh` (11 lines; 483 lines in all, added by the trimmer layer `62680cd2`, a frozen copy of what trimmer 1.8.2 wrote, read by `tools/test_methodology_trim.py:4258`): no commit of the twelve touches it, changing it changes bytes a test pins, and the backlog ids on its lines are ones upstream's own trimmer already carries (BL-27, BL-28, BL-36). It counts as "added" only because the file is new. `bin/tests.sh` 2, `bin/check-layout-literals` 2, `tools/test_migrate_layout.py` 1: left on purpose at S324. The old "his call, small" item (the trimmer's proof template, whose comment lines are written into adopters' proofs) is, on these ids, now upstream's own text rather than a choice this pull request makes; I did not diff the two templates.

## 4. Shapes considered

| | Shape | Sessions | For | Against |
|---|---|---|---|---|
| **G1** | One commit per layer, as S392 did | 12 | each verified alone | about 25 min of gate runs each for changes proved inert; against his word to group documentation |
| **G2** | All twelve as one layer | 1 | fewest | puts inert text, printed text and a code commit under one verification; 26′ unseen by him until the end; refusing B later means rebuilding and re-verifying |
| **G3 (recommended)** | **Two layers:** documentation group; then 33 + B | 2 | follows the measured line; B is a removable tail; 33 verified at the same time as the text it sits beside | refusing B later costs one more verification of the tree without it |
| **G4** | Three layers: documentation; 33; B | 3 | refusing B later costs nothing | one more session now, for a commit of +56/−10 |
| **G5** | S389's unmeasured proposal (21 to 27 \| 28 to 30 \| 33, with 32 paired with 20) | 3 | the same line as G4 | 20 was added alone (layer 21), leaving 32 unpaired; its figures were unmeasured then |

G3 is recommended because the only part he may refuse is B and G3 puts B last; G4's extra session buys only the no-rework case.

## 5. Phases (each is one session; close out in full; nothing outward)

| Phase | DONE looks like | Verify | Surface, and what it cannot show | Stop |
|---|---|---|---|---|
| **Layer 22** documentation group | `pr2b/candidate` fast-forwarded to 8 new commits (29 in all): 21, 22, 23, 24, 25 as `git cherry-pick -x` with patch-ids equal to the originals, **26′**, 27 and 32 likewise; expectations written (with confidence) before building; **26′'s diff shown to him inline before the branch moves**, since a region needing judgment goes to him (plan §5, PR2b row) | in a clean `--no-local` clone: `pr2b-layer-driver.sh` (ratchet 18/18, 0 unmeasured; `bash bin/tests.sh` 0 failed; `--reverify`; four `check-links` forms), `scrub-proof.py <clone> d818ca17 <tip>` exit 0, `scrub-derive.py` at the tip (about 639 → 33 less 26′'s reach), `pr2b-layer-measure.py` against #98 and #96 (regions not above 5 and 4, plus whatever 26′ adds), `context_budget.py --status` exit 0 | this machine, serial, hooks not armed, load stated. **Cannot show:** that the rewritten prose reads well to the maintainer (`scrub-record.md` §4), Windows, an armed hook | the branch exists locally, green, un-pushed |
| **Layer 23** 33, then B | 4 commits on top (33 in all): 33, 28, 29, 30, clean cherry-picks, patch-ids equal; the tree equals `866ea59c8738` plus 26′'s edits | the same driver; `python3 tools/test_methodology_dashboard.py` prints `Ran 397 tests` and `OK`; the gate floor reads 397; `scrub-proof.py` over the B range alone exit 0; `quality_ratchet.py --precommit` accepts the floor | as above. **Cannot show:** that no adopter reads the printed text 28 and 29 change | local, green, un-pushed; then PR3's table and PR4's text are re-run (plan §5), each its own session |

## 6. Decisions for him (the first two decide the next session's deliverable)

1. **D1: is the line drawn in the right place?** (a) **Documentation group = 21 to 25, 26′, 27 and 32; B (28 to 30) and 33 are not documentation** *(recommended: the line is measured, no code token changes in the first group, and B changes text that programs print)*; (b) treat B as documentation too: one group for 21 to 30 and 32, then 33.
2. **D2: how many layers?** (a) **G3, two** *(recommended, section 4)*; (b) G4, three; (c) G2, one; (d) G1, twelve.
3. **D3: the leftovers.** (a) **Leave the fixture's 11 lines and the 5 on purpose; the pull request's text names them** *(recommended: scrubbing the fixture changes bytes a test pins, and its ids are ones upstream's trimmer already carries)*; (b) scrub the fixture and regenerate it, which also means changing the template in the trimmer that writes it.

## 7. What this does not show

1. **That the replay equals the final series.** The 11 were tried in a throwaway clone with 26 skipped; layers 22 and 23 are built and verified in the sessions above. A figure here is "alone or in this order", not a prediction of a verified layer.
2. **Nothing about 26′ itself.** It does not exist yet; its size is the 17 lines' neighbourhood, and it may add conflict regions against #98 (26 is the only commit touching #98's source files).
3. **Timings.** The saved run was under load 61 to 103; the dashboard suite took 92.2 s (about 45 s on a quiet machine).
4. **The classification is by syntax, not by meaning.** A comment that is now wrong is still "documentation" (32 exists because four statements went stale). No test reads the prose.
5. **Adopters** were not scanned for dependence on the text 28 and 29 change.

## 8. Re-run

`python3 -I docs/planning/pr-composition-evidence/pr2b-grouping-measure.py <repo> <a directory that does not exist> pr2b/candidate pr2/candidate feat/trim-session-notes-ledger-issue93 feat/close-out-report-tool` from the repository root (about 2 minutes loaded; read-only on the repository; makes the clone). It reuses `scrub-proof.py` and `scrub-derive.py`.
