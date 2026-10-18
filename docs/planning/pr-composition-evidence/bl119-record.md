# BL-119: the same abort fix on fork `main` and on the pull request candidate, and draft 11 of the one-PR text (2026-10-18)

**Status: BUILT and measured, nothing sent.** Session S338, resumed on 2026-10-18 after the session that claimed it (2026-10-17) stopped before landing any change. Two commits carry the fix, one on fork `main` (`5f09130`) and one on the local pull request candidate `pr2/candidate` (`3cba1e5`, its 34th commit; the old tip is pinned as `refs/pr2/candidate-before-bl119`, `cfcc713`). The one-PR text (`../upstream-pr-body.md`) is now **draft 11, approved by him at the S338 close-out picker (2026-10-18)**; draft 10, which he had approved, is `git show 8d7316e:docs/planning/upstream-pr-body.md`. Every number below is printed by a command whose output is saved beside this file or in `../pr94-rewrite/evidence/` (`bl119-*`).

## 1. What was wrong, in plain words

The ledger trimmer (`methodology_trim.py`) writes a small check script, a "proof", beside each archive piece it creates; the proof checks that the trim lost nothing. If the proof cannot read something from git (for example, a shallow clone that lacks the commit before the trim), it used to stop with exit code 1, the code that means "a check failed", so a proof that had compared nothing looked like a trim that lost something. PR #94's fifth commit (`1082d3b`, trimmer 1.8.1) changed that: every such stop now prints its reason and exits 3, the code that `--reverify` documents as "the proof did not finish". Fork `main` and the candidate had the old behaviour. BL-119 carries the change onto both.

## 2. What was done

| | Fork `main` | Candidate `pr2/candidate` |
|---|---|---|
| Commit | `5f09130` | `3cba1e5` (34th; over `cfcc713`) |
| Built from | `6907c53` | `cfcc713` |
| Files, lines | 4 files, +165 / -7, plus one ledger entry | 4 files, +165 / -7 |
| Trimmer version | 1.8.0 to 1.8.1 | 1.8.0 to 1.8.1 |
| Gate `trimmer-unit-tests` | 218 to 222 | 218 to 222 |
| Hooks | armed in the build clone, passed | not armed (as for the 33rd commit) |
| Brought home | fast-forward of live `main` | fast-forward of the local ref, old tip pinned |

Both were built by `../pr94-rewrite/evidence/bl119-build.py`, which refuses unless the four files are exactly the blobs of the pinned commit, applies exact-once replacements, refuses a line over 100 characters, and writes nothing on any refusal. The new text blocks are cut out of `bl118-build.py` (the builder of `1082d3b`) as text, not retyped. The two diffs are the same line for line but for line offsets and the candidate's own, already scrubbed, 1.8.0 history line.

Two edits differ from `1082d3b`:
1. **Both trees:** the layout trimmer has a test that pins the proof template to 1.7.0's bytes, which `1082d3b`'s tree does not have. It now maps the 1.8.1 abort block back to 1.7.0's text and asserts that block is the exact one in use, so every other byte stays pinned (renamed `..._and_the_abort_hunk_only`; the test count is unchanged).
2. **Candidate only:** a test comment that `1082d3b` words "Issue #93, the abort code (the fork's BL-118)" reads "Issue #93, the abort code" here. The candidate carries no code that only the fork can resolve (`scrub-record.md` §3); an added-lines scan for `BL-`, session numbers, "the fork" and `pr2/` found this one line and none after the edit.

## 3. Measured

| Check | Fork `main` (`5f09130`) | Candidate (`3cba1e5`) |
|---|---|---|
| Trimmer suite (`python3 tools/test_methodology_trim.py`) | 222 OK, 2 skipped, 45 s | 222 OK, 2 skipped, 48 s |
| Mutation round (`bl119-mutants.py`, one at a time) | 8 of 9 killed, each by its intended test; the ninth is an equivalent change the template pin must let through, and survived | the same output, byte for byte |
| The field case (a depth-1 clone, where the trim commit's parent is absent) | frozen proof 1; `--reverify` under 1.8.0 1; under 1.8.1 **3** | the same three exits |
| `--reverify` over every archive piece, both versions | 177 pieces, the same exit under both in every one (172 at 0, 2 at 1, 2 at 3, 1 at 4) | 1 piece, 0 under both |
| Shell suite and gates in a clean clone | `tests-sh-passed` 503; gates **18/18, 0 unmeasured, results `51eb96ff6a98`, manifest `7e1f0d1576e4`**; 23 min 1 s (`bl119-main-gate-output.txt`) | `bin/tests.sh` **302 passed, 0 failed, 0 skipped**; gates **18/18, 0 unmeasured, results `668beb5fe5a2`, manifest `78150d65930f`** (`bl119-claims-output.txt`) |

The reproduction matters: the first session's saved outputs came from a scratch clone that no longer exists. Re-run today in fresh clones, its mutant output and its 177-row sweep were byte-identical, its suite output was equal but for the timing line, and its field case gave the same three exits.

The rest of `pr4-claims.sh` on `3cba1e5` (28 min 26 s), against upstream `f34769f` (261 passed, 12/12, results `10df8059439f`, as at the 33rd commit): 47 files, +19,983 / -1,105, 34 commits, the merge-base is upstream's tip; links 80 in 23 documents in each layout; the layout scanner 15 files, 0 sites; the layout suite 76 OK; the resolver block equal in all 11 files that embed it; the one archived proof exits 0 on both tips; no threshold loosens at any of the 34 commits (0 refusals, 0 warnings; gates 12 to 18; five thresholds raised, the trimmer's 124 to 222); the merge with PR #92 (`fa2bb5d`) clean. Two proofs in the fork read exit 1 in the gate run's listing (`CHANGELOG-through-2026-08-02` and `-08-09`): old frozen scripts, red before this change (`-08-02` was committed at S60 as "SRF-RED forced", `7d7c63eb`; `-08-09` by `61b48a62`), and the sweep reads both at exit 1 under 1.8.0 and 1.8.1.

## 4. The one-PR text: draft 10 to draft 11

Decision 3's figures, re-derived on both tips with the method that reproduced draft 10's numbers first (`bl119-decision3.sh`, output `bl119-decision3-output.txt`; its first block is draft 10's own figures):

| Figure | Draft 10: `cfcc713` against #94 at `2308553` | Draft 11: `3cba1e5` against #94 at `1082d3b` |
|---|---|---|
| `git merge-tree` conflicts | 4 files, 22 regions (trimmer 12, tests 8, gates 1, apparatus 1) | the same |
| `bbe0dc3` taken alone | 4 files, 13 regions (5, 6, 1, 1) | the same |
| Lines #94 adds to the trimmer / absent here as exact lines | 506 / 77 | 536 / 77 |
| The same for its tests | 1,558 / 294 | 1,640 / **295** |
| `.quality-gates.json` | 1 / 1 | 1 / 1 |
| PR #92 | clean | clean |

The 295 is the candidate's one reworded comment line (§2, item 2): it is a line #94 has and this branch words differently, so it is not an identical line. Without the port, `cfcc713` against `1082d3b` would lack 100 and 353 (the second block of the output): the port closed the fifth commit's part of the gap and left the fourth's.

Seventeen exact-once edits (`bl119-draft11-build.py`, which refuses unless the file is draft 10 as `8d7316e` holds it): the heading and status paragraph (draft 11, awaiting approval, with the way back to draft 10); the tip `cfcc713` to `3cba1e5` and 33 to 34 commits (four places); decision 3 (head `1082d3b`, "its fifth commit", the new line counts, "this branch contains ... #94's fifth commit", and "both name their trimmer 1.8.1, each a different 1.8.0 plus the same abort fix"); the sizes (19,822 to 19,983 added, 1,102 to 1,105 removed, 2,959 to 2,991 and 530 to 533 reaching a project, 16,856 to 16,985 staying, and the share of earlier work 43% to 42%, because 8,461 over 19,983 is 42.3%); the sentence "the last two commits change no code path", now three commits with `3cba1e5` described in a new bullet; the sentence that says which hashes are not this branch's, now naming `1082d3b`. **The body is 21,486 B, +623 B on draft 10's 20,863 B** (the new bullet 440, decision 3 87, the commit-list sentence 64, the hashes sentence 32). `pr4-body-check.py` against `3cba1e5`: exit 0, no banned token, 14 hashes resolve, 35 paths cited, the recomputed shortstat and count equal the text's.

Left as they were, on purpose: the evidence table's other rows (all re-measured and equal); decision 3's closing question (carrying #94's *fourth* commit over is still the open part); "about 35 minutes" for `pr4-claims.sh` (this run took 28 min 26 s and the 33rd commit's 29 min, so the figure is generous; it is not about this change); the paragraph on the 12 projects (see §6).

## 5. A finding for him

**PR #94's fifth commit, already pushed, carries one code that only the fork can resolve:** `tools/test_methodology_trim.py` has "Issue #93, the abort code (the fork's BL-118)" in a comment. Its other `BL-27` and `BL-28` mentions are upstream's own (6 and 2 mentions in the trimmer at `f34769f`); `BL-118` is the only new fork code in what #94 adds (checked: `git diff f34769f origin/fix/trim-verify-false-red-issue93`, added lines). Removing it from #94 means a sixth commit or an amended fifth and a force-push to a public pull request: an outward action, his go-ahead. Raised as BL-120.

## 6. Not measured

- **The 12 projects (`pr3-adopters.py`).** Not re-run. The text's one trimmer-related claim there is "a project's own 49 added lines in `methodology_trim.py`"; checked by hand: the project's copy (`nprcgenekeepr`, `ef4fd80`) differs from the fork's trimmer before this change (`6907c53`) in 49 lines, all its own. Against the new tips it differs in more lines (84 against `5f09130`, 110 against `3cba1e5`) only because those tips gained the abort fix the project's copy lacks. The sentence is about the project's own lines and stays.
- **A cold read of draft 11.** None; draft 10's last read was before its approval. The edits are numbers, a hash and one bullet.
- **The candidate in a hooks-armed clone,** and on a maintainer's machine.

## 7. Files

`../pr94-rewrite/evidence/`: `bl119-build.py`, `bl119-mutants.py`, `bl119-field-case.sh`, `fork_shards_compare.sh` (a new optional 5th argument), and the outputs `bl119-main-*`, `bl119-candidate-*`, `bl119-main-gate-output.txt`. Here: `bl119-draft11-build.py`, `bl119-decision3.sh` and `bl119-decision3-output.txt`, `bl119-claims-output.txt` (the claims run on `3cba1e5`), this record.

## 8. Next, and his

1. **Draft 11: approved** (S338 close-out picker, 2026-10-18); it is the held text for PR5. Draft 10 described a branch that no longer exists (`cfcc713`, 33 commits) and a pull request that had moved on (`2308553`). The approval is the one hand edit to the status line; `bl119-draft11-build.py` still produces the "awaiting approval" wording.
2. **BL-120: declined** at the same picker ("Leave it"): the comment in #94 stays; reword it only if #94 gets another commit for another reason.
3. PR5 itself (the push and the opening) is still after D1 and D4, each his call.
