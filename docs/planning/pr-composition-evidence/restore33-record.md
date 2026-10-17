# The 33rd commit on the pull request candidate, and draft 10: the record (2026-10-17)

His two S333 decisions ([`draft4-record.md`](draft4-record.md) §5, F1 and F2), taken as the deliverable at the S336 Phase 0 picker ("PR4 build: restore the two tests, draft 10"). Local ref only; nothing is sent to `KJ5HST/methodology`. The edits are `restore33-build.py` (it refuses on drift), the message is `restore33-message.txt`, the re-run of the claims is `pr4-claims.sh` saved as `restore33-claims-output.txt`, the overlap with PR #94 re-measured by `pr4-supersede.sh` as `restore33-supersede-output.txt`, the distribution by `pr4-distribution.py` as `restore33-distribution-output.txt`.

## 1. The answer

One commit on top of `a62bfec`: **`cfcc713`**, now the tip of the local ref `pr2/candidate` (33 commits over `upstream/main` `f34769f`; the previous tip is pinned as `refs/pr2/candidate-before-fix33` and reads back `a62bfec`). Two files, +56 / -10 (`git diff --numstat`: `.quality-gates.json` 1/1, `tools/test_methodology_dashboard.py` 55/9). No code path changes; one threshold rises, `dashboard-unit-tests` 395 to 397 (`min`, a tightening). Against upstream the shortstat moves from 47 files, +19,826 / -1,152 to 47 files, **+19,822 / -1,102**: the 48 restored lines are upstream's own and stop counting as removed, the 10-line note stops counting as added, the 6-line note that replaces it is added, and diff alignment accounts for the rest (`pr4-distribution.py` asserts the per-file sums against the shortstat; its only changed rows are the test file, +3,827 / -65 from +3,831 / -115, and the totals).

What was restored, as upstream wrote it (`git show f34769f:tools/test_methodology_dashboard.py` lines 2410 to 2457, the class header through the second test's last line): `TestCliRemedyProportionality` with `setUp`, `tearDown`, `_project`, `test_bare_dry_run_refuses_instead_of_writing` and `test_a_normal_run_still_writes`. Not restored, on purpose and now said in the note that follows the two tests: `test_stale_warning_leads_with_the_project_scoped_remedy`, which asserts a literal `"cp "` the branch's `--sync`-scoped warning does not print (decision 2 (a) of the text). The two tests pass on the branch's code unchanged: `Ran 2 tests OK` alone, `Ran 397 tests OK` in the whole dashboard suite (53.8 s in the clone).

## 2. What the builder proves

`restore33-build.py` refuses, writing nothing, on a file that is not the blob it was derived from (`4d61598` and `fa790fe` at `a62bfec`), a note not found exactly once, or an upstream class not found once by its header and its third test; it then checks its own output: the gate manifest differs from the old one in exactly one value (`dashboard-unit-tests.threshold`, 395 to 397, on a `min` gate; every other key, threshold and command equal), the test file's top-level statements equal the old ones with exactly one insertion whose syntax tree equals the one parsed from upstream's own lines, the file gains exactly two `def test_` lines, and no new comment line is over 100 characters. **The first run refused on that last rule** (one line of the new note was 101 characters) and wrote nothing; the note was reflowed (longest line 96) and the second run wrote both files. A third run, on the edited tree, refused ("not the blob this was derived from"). The commit ran `python3 starter-kit/quality_ratchet.py --precommit` by hand with the two files staged (exit 0); the scratch clone runs no hooks, as for the 32nd commit, so the `Co-Authored-By` trailer is in the message by hand.

## 3. Verification: `pr4-claims.sh` on `cfcc713`

Clean `--no-local` clones, serial, exits read bare (`restore33-claims-output.txt`, 107 lines, exit 0, colour codes stripped as in the earlier saved runs; launched 01:03, done 01:32, about 29 minutes at a load average of 5 to 11 from foreign processes; `HEAD94` passed as `2308553`, `HEAD92` as `fa2bb5d`). Against the 32nd commit's run on `a62bfec` (`fix32-claims-output.txt`) the output differs in exactly these places and no other (`diff` of the two):

| Line | `a62bfec` | `cfcc713` |
|------|-----------|-----------|
| shortstat | 47 files, +19,826 / -1,152 | 47 files, +19,822 / -1,102 |
| commits over upstream | 32 | 33 |
| the gate `dashboard-unit-tests` | `>= 395`, measured 395 | `>= 397`, measured 397 |
| gate results id / manifest id | `23481eb88ba1` / `c7b9257ea110` | `54e8489f99ec` / `88a7b6f562c4` |
| section 7, commits compared against their parents | 32 | 33 (0 refusals, 0 warnings, 0 manifest defects); the dashboard threshold row reads 229 to 397 |
| section 8, #94's head | `972eb2c`: 3 files, 17 regions | `2308553`: 4 files, 22 regions (gates 1, apparatus 1, trimmer 12, tests 8) |
| (a timing, not a figure) layout suite | 19.865 s | 2.348 s |

Unchanged: the suite **302 / 0 / 0** (upstream 261 / 0), the gate **18/18, 0 unmeasured** (upstream 12/12, results `10df8059439f`), 80 links resolve in both layouts, the scanner 15 files and 0 sites, the resolver block equal in all 11 files that embed it, the one tracked proof exit 0 on both tips, #92 clean. Both gate ids moved this time, as expected: `manifest` hashes the gate definitions (a threshold changed) and `results` hashes the per-gate measured values (397 where 395 was); the 32nd commit moved only the first, which is the lesson `fix32-record.md` §3 recorded.

## 4. Decision 3 re-measured: PR #94 moved

PR #94's head moved from `972eb2c` (three commits) to `2308553` (four; the fourth, 2026-10-17: `SESSION_NOTES.md` joins the trimmer's ledger table and the proof prints the record-0 diff, as 1.8.0) between draft 9 and this build, so decision 3's figures were re-derived on the new tip against both heads (git objects only; `HEAD94` passed to `pr4-claims.sh` as `2308553`):

| Figure, on `cfcc713` | against `972eb2c` (draft 9's head) | against `2308553` (today's head) |
|---|---|---|
| `git merge-tree --write-tree` conflicts | 3 files, 17 regions (trimmer 10, tests 6, gates 1): the draft-9 figures, so the restore moved nothing here | 4 files, 22 regions (trimmer 12, tests 8, gates 1, `FRAMEWORK_APPARATUS.md` 1) |
| `bbe0dc3` taken alone | 2 files, 6 regions (draft 9) | 4 files, 13 regions (trimmer 5, tests 6, gates 1, apparatus 1) |
| lines #94 adds to `starter-kit/methodology_trim.py` / absent from the branch as exact lines | 430 / 11 | 506 / 77 |
| the same for `tools/test_methodology_trim.py` | 1,136 / 9 | 1,558 / 294 |
| the same for `.quality-gates.json` | 1 / 1 | 1 / 1 |
| PR #92 (`fa2bb5d`) | clean | clean |

What the branch lacks of #94's fourth commit, by grep of the two trimmers: `SESSION_NOTES` 0 mentions against 4, `_session_notes_date` 0 against 2, the proof's `DIFF:` block 0 against 1; `reverify` 11 against 11 (the branch has the fix as #94's first three commits had it, inside `bbe0dc3`). Both trimmers declare `TRIM_VERSION = "1.8.0"`, the branch's for the `methodology/` layout and #94's for issue #93's fourth step (upstream's is 1.5.0); the text now says so, and that whichever lands second takes the next number (S335's gotcha, now a sentence the maintainer reads).

## 5. The draft text: draft 10

Ten edits on draft 9 (`d2cc1e9`), each an exact-once replacement, then three cuts; `pr4-body-check.py` exit 0 against `cfcc713` (no banned token, 35 paths cited, every hash resolves, the recomputed shortstat and count equal to the text's). The changes: the status paragraph above the rule (draft 10, tip `cfcc713`, 33 commits, no read); decision 1's size sentence; decision 2's opening sentence gains F2 (the first-parent walk of the gate manifest's history since 2.21.0, one clause); (e) names the two removed tests and cites the restore (F1); decision 3 is re-measured against `2308553` (§4) and says both trimmers are 1.8.0 and that #94's fourth commit is not in the branch; decision 4's hook sentence says 33 commits; the Size paragraph (19,822 / 1,102; 16,856 of the added lines stay here); the commits paragraph names `cfcc713` beside `a62bfec`; the evidence table's last row says 33 commits. Cuts, no fact lost: decision 1's known-gap sentence no longer repeats the "Known gaps" bullet, the F2 clause was tightened, and the signpost sentence before the sections was shortened.

**Size.** The body is **20,863 B** against the 20,000 B budget he set at S332, 863 B over (draft 9 was 117 B over). What bought it, by diff hunk against draft 9: decision 2's opening +273 B (F2), (e) and decision 3 together +492 B, the commits paragraph +85 B, the cuts -104 B. Further cuts remove facts; the two least costly to lose are decision 3's `bbe0dc3`-alone sentence (88 B) and decision 4's merge-or-squash sentence (101 B). No read of draft 10 was bought (four reads rated 5, 5, 6 and 5 of 10; S333's note stands: a fifth is not recommended, and one costs about 85,000 subagent tokens).

## 6. What none of it shows

- The restored tests ran in the scratch clone and in `pr4-claims.sh`'s clean clone (§3); not under a hooks-armed clone and not on the maintainer's machine.
- `pr4-supersede.sh` counts stripped exact lines: a reworded line counts as absent and a moved one as present. It is the measure draft 9 already cited, re-run, not a better one.
- The conflicts are counted, not resolved; the two 1.8.0 trimmers are named, not reconciled.
- `pr4-cost.sh` and `pr4-moved.sh` were not re-run: the restore changes a test file and a threshold, which neither script reads, so the text's 244 B and 0 paths stand from `a62bfec`.
- No fresh reader of draft 10; his reading is the test.
