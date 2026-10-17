# Upstream PR #94: the rewritten title and body, the fourth commit that closes the 8-of-54 gap, and the evidence (S334 and S335, 2026-10-16)

**Status: the text is draft 8 and the fourth commit is built on a local branch (`2308553`); NOT pushed, NOT posted.** Upstream pull request #94 (`KJ5HST/methodology`, the fix for issue #93) is unchanged: open since 2026-10-05, tip `972eb2c`, base `upstream/main` `f34769f`, no comment or review from anyone (checked again at S335's Phase 0). Pushing to its branch, editing its title or body, or commenting on it is an outward action: each one needs his explicit go-ahead (BL-98's row says so).

He asked for the rewrite on 2026-10-16 ("can PR #94 be edited to be more clear? I find it hard to read."), corrected it term by term, and then made it this session's deliverable: "Let's call the work you have done and currently finishing up serve as your deliverable. Save this rewrite for later use. In the next session, we work on improving this PR." So this directory is the deliverable of S334. S335 took his four decisions and built the fourth commit; see "Decided and built at S335" below.

## Files

| File | What it is |
|---|---|
| `title.txt` | The proposed title, one line (the old one is quoted in the section "Posting it" below); changed at S335. |
| `body.md` | The proposed body, exactly as it would be posted (draft 8, 27,328 B; draft 7 was 20,651 B). |
| `original-body.md` | The body as it stood on 2026-10-16 (5,770 B), for diffing: `diff original-body.md body.md`. |
| `evidence/` | The scripts and saved outputs behind the numbers in `body.md` and in this record. `evidence/README.md` says what each file is. |

## What was wrong with the old text, in his words and in order

1. Line 1: "What does not close what. You have two 'it' words and neither is defined." (The old line said "Refs #93; it does not close it.")
2. "What is a red proof? What is `--reverify` an argument for?" ("red" was test-suite shorthand; `--reverify` is an option of `methodology_trim.py` that takes a shard.)
3. "Why did you remove the denominator (54)?" (A shortened line 1 had "the 10 red proofs" and lost "of the 54".)
4. "You have used the general term 'ledger' but have not stated what it refers to." (In the framework "the ledger" usually means `CHANGELOG.md`; the trimmer means any file in its table.)
5. "'inside' indicates location usually." (The ledger table is a Python dictionary written in the code of `methodology_trim.py`; "inside" suggested a place.)
6. "The low byte count of the original may well be due to leaving out information that would potentially make the text more clear. Longer text is not necessarily bad." (This overrode the byte-budget habit; the text is 20,651 B against 5,770 B.)

Rules that came out of it, applied to `body.md` and worth keeping for any outward text: define every term at first use; give every count its denominator; name the subject instead of "it"; use a word in its everyday sense or define the sense; do not use a word of place for something that is not a place.

## How the text was checked

Four independent cold reads, each by a fresh subagent given the text and a reader profile (the maintainer: knows git, GitHub, shell, Python and the framework's documents; has not read the trimmer's source or issue #93), asked to list every undefined term, ambiguous referent, count without a denominator, contradiction, reasoning gap and (from the third read on) loosely used word. Findings are claims: each was checked against the code, the adopter repository, a run, or the fork's ledger before any change.

| Read | Findings | Outcome |
|---|---|---|
| 1 | 21 | 20 fixed; 1 (does the #93 repository's own table entry survive `bin/sync`?) left out until tested |
| 2 | 17 | 16 fixed; the same sync question |
| 3 | 26 | all addressed; the sync question answered by a run and added to "Adopter impact" |
| 4 | 24 | all addressed (23 edits) |

**Draft 7 (`body.md`) is draft 6 plus the fourth read's edits and has had no fifth read.** Expect a few more gaps; the user's own reading found things the readers did not ("inside", the first line's two "it"s, the lost 54).

Real flaws the reads found in the drafts (not wording): the text called all 10 failures "false" and then defended 8 as correct FAILs (now reconciled); "two things keep them failing" did not follow (all 8 fail for one reason; they differ only in whether the proof recognises the pattern); the cause-3 account contradicted itself (its commit also rewrote record 0); "four steps" and "four tests" did not count what they said.

## Facts: re-measured this session, and copied unchanged

**Re-measured (2026-10-16):** the 54-proof sweep, each proof as written and then `--reverify` (10 fail as written; `--reverify` gives 46 at exit 0, 7 at exit 1, 1 at exit 4); the sort of the 10 by failure line (7 / 2 / 1, equal to #93's counts); the commit order, `TRIM_VERSION` and test floor of each PR commit (1.5.1 / 129, 1.6.0 / 154, 1.7.0 / 181); the PR branch against the fork's `3616b5f` (six places, seven lines, all comments except one assertion message); the four hostile-text tests (their names, and that the third runs once per line); what `--reverify` does with a proof that lacks `STUB_PATTERN` or `REGEN_PATTERNS`; the exit-3 reasons; that the #93 repository's trimmer is canonical 1.5.0 plus 49 added lines for `SESSION_NOTES.md`; `bin/sync` from the PR branch against a project holding that edited trimmer (exit 2, "would write" under `--force`, dry run only); the PR's 181 trimmer tests on the unmodified branch (OK, 2 skipped, 41 s).

**Copied unchanged from the old body, not re-measured:** `quality_ratchet.py --run` 12 of 12 and `bin/tests.sh` 261 passed on the branch; the throwaway-clone trims of this repository's `HANDOFFS.md` (38 receipts, 221,642 B) and the end-to-end exit 4; the byte-identical `bin/sync --source=local` check; `git merge-tree` against #92 reporting no conflict; the mutation counts (9 with 7 non-equivalent, 37, 54), which come from the fork's ledger (`docs/archive/CHANGELOG-through-2026-10-06.md`, the S264, S265 and S266 entries), not from a run today.

**Not independently established:** that the 10 failing trims lost nothing. That rests on #93's authors' hand diffs, plus the proofs' own finding that only record 0 differs. No script judges whether a replaced stub held anything of value (see the next section).

## The gap he asked about at S334: 8 of the 54 proofs still came out wrong

His question: "You still have erroneous results. Were you not able to develop a script that correctly classified all of the 54 proofs? Do you have a plan to close that gap?" The answer, with numbers:

**Current state of the PR as it stands:** `--reverify` is right on 46 of the 54 (they pass) and reports FAIL on 8 trims that #93's authors found lossless. Seven are in the #93 repository's own `SESSION_NOTES.md`, which the canonical ledger table does not list, so the proof has no stub marker and prints the generic L1/L3 failures (exit 1). One is a `HANDOFFS.md` shard, recognised as a stub finalize and reported as exit 4, which is still a FAIL **by decision D2** of `docs/planning/issue93-trimmer-proof-false-red-plan.md` §9: "(i) keep it a FAIL with its own label and exit 4, BL-27 intact; or (ii) exit 0 with the label, which reverses BL-27 for this one shape and means the proof certifies a replaced stub, including the one that carried prose (§3.5). DECIDED: (i), FAIL, labelled, exit 4." The plan predicted this outcome ("8 stay red but named").

**Prototypes, in scratch copies of the PR's trimmer, nothing in the repository changed** (`evidence/make_prototypes.py`, `evidence/sweepA.tsv`, `evidence/sweepAB.tsv`):

| Variant | exit 0 | exit 4 | exit 1 |
|---|---|---|---|
| The PR as it stands | 46 | 1 | 7 |
| A: add a stub marker for `SESSION_NOTES.md`, `^\*\*Status:\*\* Session claimed\b.*$` (the runner's Phase 1B stub line, matched as a prefix) | 46 | 8 | 0 |
| A+B: also let a recognised stub finalize exit 0 (reverses D2) | 54 | 0 | 0 |

A first marker, end-anchored (`... Work beginning\.\s*$`), caught only 3 of the 7 `SESSION_NOTES.md` shards: four sessions had appended text to the status line ("Work beginning. PRE-RED investigation already found…"). The marker has to match the line's start.

**Safety check of B:** with A+B swapped into a scratch worktree of the PR branch, 177 of the 181 trimmer tests pass. The four that fail assert exactly the D2 behaviour (`test_a_pending_stub_finalized_in_the_trim_commit_is_labelled_and_exits_4`, `test_a_proof_older_than_the_stub_label_is_rederived_with_the_label_from_the_ledger_table`, `test_the_proofs_stub_note_carries_the_rule`, `test_the_stub_marker_comes_from_the_ledger_table_by_live_basename`; `evidence/protoAB-test-failures.txt`). The real-loss shapes still pass, among them `test_a_complete_record_0_edited_in_the_trim_commit_still_exits_1_with_no_stub_label` (test file line 1492), `test_a_stub_finalize_beside_an_edit_to_another_record_is_not_labelled` (1508) and `test_a_stub_finalize_beside_a_reorder_of_other_records_is_not_labelled` (1524). This is feasibility, not a vetting: no mutation run on the prototype.

**Why D2 is not a free change:** in all 8 shards the finished record rewrites the stub's text. Apart from the identifying line or lines (the heading of a `SESSION_NOTES.md` record; the fence, `session:` and `date:` lines of a receipt), none of the stub's lines survives as a whole line in the finished record (`evidence/stub-survival-output.txt`: for example 23 of 24 stub lines are absent in the shard whose stub carried "PRE-RED investigation already found…"; in the `HANDOFFS.md` shard 11 of 15 are absent, most of them `X: pending` placeholder fields plus the reworded `active_task:` line). So no automatic "the stub's prose survives" check can certify them, and exit 0 would mean the proof certifies replaced stub prose it has not read. #93's authors judged by hand that nothing of value was lost; a proof cannot.

## Decided and built at S335 (2026-10-16): the gap is closed on a local branch, not pushed, not posted

**His four decisions, at the S335 picker (each the recommended option):** (1) D2 stays as decided at S263: a recognised stub finalize is a labelled FAIL at exit 4, never exit 0. (2) A `SESSION_NOTES.md` stub marker comes from a canonical entry in the trimmer's ledger table, not from a `--reverify` option. (3) The proof prints the whole unified diff of the stub against the record that replaced it. (4) The body keeps #93's three causes where it restates the issue and describes what remains by the one finalize pattern.

**Where the change is.** Local branch `fix/trim-verify-false-red-issue93-v2`, tip `2308553`, one commit on top of PR #94's tip `972eb2c` (so the PR's chain would read `68d8a06`, `965f136`, `972eb2c`, `2308553` on `upstream/main` `f34769f`). The branch exists only in this clone: a worktree under the session scratchpad built it, and the commit is in this repository's object store, reachable by the branch. The same commit as a patch, in case the branch is lost: [`evidence/0001-trim-1.8.0.patch`](evidence/0001-trim-1.8.0.patch) (`git am` onto `972eb2c`). PR #94 is unchanged (open, head `972eb2c`, no comment or review from anyone, checked at this session's Phase 0).

**What the commit changes** (5 files, +537 / −10 by `git diff --numstat`): `starter-kit/methodology_trim.py` (+78 / −4: `TRIM_VERSION` 1.8.0 and its history paragraph; `_session_notes_date`; the `SESSION_NOTES.md` entry in `LEDGERS` with the two-part stub marker; the proof template imports `difflib`, computes the record that replaced record 0 whenever the frontier was edited, and prints the diff after the `FAIL:` and `NOTE:` lines); `tools/test_methodology_trim.py` (+423 / −1: `TestSessionNotesIsATrimmableLedger`, 18 tests, and two existing tests moved off the old truth that `SESSION_NOTES.md` has no entry); `FRAMEWORK_APPARATUS.md` (the timing-rule paragraph names the notes stub and the diff); `.quality-gates.json` (`trimmer-unit-tests` 181 → 199); `CHANGELOG.md` (one `[issue #93]` entry in upstream's format). The tests were written first and seen red against the unchanged tool (18 tests: 9 failures, 9 errors, all `NO_CONFIG` or a missing key), then the tool was changed.

**The marker's shape was measured before it was chosen.** On the #93 repository's seven real `SESSION_NOTES.md` stubs (record 0 at each trim commit's parent), both candidate markers, the status line alone and the status line plus the `(IN PROGRESS)` tag, match every stub and none of the seven records that replaced them (`evidence/marker-measure-output.tsv`). On the live notes files of the 12 adopters, a finished record in 3 of them still carries the status line, and 2 of those 3 records dropped the tag (`evidence/adopter-claim-lines-output.tsv`): the line alone would have called those two finished records stubs. So the marker requires both. (I first told him "4 of 12" in this session; the count that distinguishes finished records from live stubs is 3, and the comments, tests, the branch's ledger entry and the body say 3.)

**Measured, at `2308553`:**

| What | Result | Where |
|---|---|---|
| `tools/test_methodology_trim.py` | 199 tests, OK, 2 skipped, 37.5 s (181 before the commit) | `evidence/trimmer-suite-1.8.0.txt` |
| `bin/tests.sh` in a clean `--no-local` clone under the branch's own hooks | 261 passed, 0 failed | `evidence/tests-sh-1.8.0.txt` |
| `quality_ratchet.py --run` in that clone (upstream's 12 gates) | 12/12 pass · 0 fail · 0 unmeasured (results `28a2fdac6745`, manifest `dfb478526806`); with `bin/tests.sh` under 6 minutes at a load of 6 to 8 | `evidence/ratchet-run-1.8.0.txt` |
| The #93 repository's 54 proofs under `--reverify` | 46 at exit 0, 8 at exit 4, 0 at exit 1 (PR tip: 46 / 1 / 7); every exit-4 output carries the label and the diff (30 to 176 diff lines) | `evidence/sweep-after-1.8.0.tsv`, `evidence/reverify-outputs-8-labelled-1.8.0.txt` |
| This fork's 174 frozen shards under 1.7.0 and 1.8.0 | every exit code the same (169 at 0, 2 at 1, 1 at 4, 2 at 3); the diff appears in the exit-4 output and in the one exit-1 output whose record 0 was edited | `evidence/fork-shards-old-vs-new.tsv` |
| `--check` on the 12 adopters' live notes files | 10 parse (3 to 85 records), 1 `NO_RECORDS` (a seed), 1 `GRAMMAR_MISMATCH` (another heading shape), 0 zone refusals | `evidence/adopter-check-output.txt` |
| Mutation round on the new layer, 17 mutants | 17 killed, 0 survived; the intended test among the failures in every case; a second round added the two tests for behaviours no test named (a grammar mismatch refused loudly; the Class A arm at the root only) | `evidence/mutants_s335.py`, `evidence/mutants-s335-output.txt` |
| `bin/sync --source local` into a fresh project | `methodology_trim.py` and `FRAMEWORK_APPARATUS.md` byte-identical, version 1.8.0; the #93 repository's edited copy still exits 2 without `--force`; after a forced sync the canonical entry reads that repository's notes file as its own entry did (42 records, same header) | `evidence/sync-test-1.8.0.txt` |
| `git merge-tree` against PR #92's branch (`fa2bb5d`) and against `upstream/main` | no conflict for either (exit 0) | this record |

**Two things to know.** (1) **The version number collides with this fork's own 1.8.0.** The fork's `starter-kit/methodology_trim.py` is already 1.8.0 (BL-101 P3, the `methodology/` directory layout, `ee89b24`), a different change that upstream does not have. The PR follows upstream's sequence (1.5.0, 1.5.1, 1.6.0, 1.7.0, 1.8.0); when the directory plan's pull request is composed on top of this one, the fork's layout change takes the next number. Not in the body: it is this fork's bookkeeping, not the maintainer's. (2) **A finding, not fixed, outside this session's scope:** the proof exits 1 when it cannot read an artifact from git (`sys.exit("verify: cannot read ...")` in the template's `show()`), the same exit code as a FAIL. The first sweep today produced exactly one such false exit 1, from a transient blob fetch failure in the partial clone ("could not fetch ... from promisor remote"); the re-run read exit 0 under both versions, and the clean re-run of all 54 is the one recorded above. A proof that did not finish should exit 3, which is what `--reverify` already promises for that case ("3: the proof did not finish"). A second small commit on the branch, or a backlog row; his call.

**The text.** [`body.md`](body.md) is draft 8 (27,328 B; draft 7 was 20,651 B): the Summary and Background, a Commit 4 paragraph, "What remains, and why the 8 stay FAILs" (with a fourth table column), the Evidence and the Adopter impact changed; the rest is draft 7's. **Draft 8 has had no cold read**; his reading is the test. [`title.txt`](title.txt) changed: the new title names the three things the PR does and the file it adds to the table.

## Posting it (his go-ahead for each step; read each back)

The body states facts at `2308553` and `upstream/main` `f34769f`. First check that #94 has not moved (`gh pr view 94 -R KJ5HST/methodology --json headRefOid,comments,reviews,updatedAt`; the head must still be `972eb2c`). Then, from the repository root:

```
git push origin fix/trim-verify-false-red-issue93-v2:fix/trim-verify-false-red-issue93   # a fast-forward of the PR's head branch; PR #94 moves to 2308553
gh pr view 94 -R KJ5HST/methodology --json headRefOid --jq .headRefOid                   # read back: 2308553764174551424be1fef971a0b93dc85aff
gh api -X PATCH repos/KJ5HST/methodology/pulls/94 \
  -f title="$(cat docs/planning/pr94-rewrite/title.txt)" \
  -F body=@docs/planning/pr94-rewrite/body.md
gh pr view 94 -R KJ5HST/methodology --json title,body --jq '.title, (.body|length)'   # read back: the title, and 27328
```

The old title was: `fix(trim): generated proofs stop reading red on lossless trims, and --reverify re-derives a frozen one (refs #93)`. Use `gh api -X PATCH`, not `gh pr edit`, and read both fields back before reporting. The push and the edit are two outward actions; each is its own go-ahead.

## Scratch-only artifacts and limits

The S334 prototypes (`trim_protoA.py`, `trim_protoAB.py`) were generated by `evidence/make_prototypes.py` and are not saved; regenerate them. The #93 repository was cloned (partial, sparse) into each session's scratchpad, not into this repository, and is gone with the session; `evidence/README.md` has the recipe. S335's build worktree (`$SCRATCH/pr94wt`) is a worktree of this repository on the local branch `fix/trim-verify-false-red-issue93-v2`; `git worktree remove` it when done, the branch and its commit stay. A partial clone fetches blobs on demand, and one such fetch failed once in S335's first sweep (see "Two things to know"); re-run a changed verdict before believing it. Nothing was pushed or posted. The `pr94` ref used at S334 to read the PR head was removed; `git fetch upstream pull/94/head` recreates the objects.
