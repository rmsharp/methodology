# The rewrite of upstream PR #94's title and body — saved text, evidence, and what to improve next (S334, 2026-10-16)

**Status: saved, NOT posted.** Upstream pull request #94 (`KJ5HST/methodology`, the fix for issue #93) is unchanged: open since 2026-10-05, tip `972eb2c`, base `upstream/main` `f34769f`, no comment or review from anyone. Editing its title or body, pushing to its branch, or commenting on it is an outward action: each one needs his explicit go-ahead (BL-98's row says so).

He asked for the rewrite on 2026-10-16 ("can PR #94 be edited to be more clear? I find it hard to read."), corrected it term by term, and then made it this session's deliverable: "Let's call the work you have done and currently finishing up serve as your deliverable. Save this rewrite for later use. In the next session, we work on improving this PR." So this directory is the deliverable of S334. The improvement is S335's.

## Files

| File | What it is |
|---|---|
| `title.txt` | The proposed title, one line (the old one is quoted in the section "Posting it" below). |
| `body.md` | The proposed body, exactly as it would be posted (draft 7, 20,651 B). |
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

## The gap he asked about: 8 of the 54 proofs still come out wrong

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

**Why D2 is not a free change:** in all 8 shards the finished record rewrites the stub's text; none of the stub's non-placeholder lines survives as a whole line (`evidence/stub-survival-output.txt`: for example 23 of 24 stub lines absent in the shard whose stub carried "PRE-RED investigation already found…"). So no automatic "the stub's prose survives" check can certify them, and exit 0 would mean the proof certifies replaced stub prose it has not read. #93's authors judged by hand that nothing of value was lost; a proof cannot.

## What to decide and build next (S335)

Decisions that are his (each changes what the PR means):

1. **D2.** Keep a recognised stub finalize a FAIL (exit 4), or let it pass (exit 0 with the note). #93's own suggestion allowed "an OK line with the note". The prototype says it is feasible; the cost is that the proof then certifies a replaced stub it has not read.
2. **Where a `SESSION_NOTES.md` stub marker comes from.** (a) A `SESSION_NOTES.md` entry in the canonical ledger table (the #93 repository's own entry, `methodology_trim.py:377` at its commit `82433662`, is the starting point; this widens the canonical trimmer to a third ledger); (b) a `--stub-marker REGEX` option on `--reverify` (narrow; helps existing shards only, a trim of the file still needs a table entry); (c) neither.
3. **Whether the proof should print the unified diff of the stub against the finished record 0.** This is the first suggestion in #93 and the PR did not implement it. With it, keeping D2 (i) still lets a reviewer confirm each of the 8 in seconds. It is independent of 1 and 2.
4. **Framing.** BL-98's row says "Two classes, not #93's three" (2 are the L2 substring test; 8 are a close-out commit that also trims, checked mechanically). `body.md` keeps #93's three causes and explains that the cause-3 shard has the finalize pattern too. The two-class framing would shorten "What still fails".

Then the build, one session, only after the decisions: change the trimmer on a local copy of the PR branch `fix/trim-verify-false-red-issue93` (tip `972eb2c`; also on `origin`), with tests and controls (the real-loss shapes above must still fail); a mutation round on the changed layer (the fork's `docs/planning/issue93-evidence/mutants_p2.py`, layer 1, is the model); vet in a scratch clone under upstream's own hooks; re-run `evidence/sweep_after.sh` (target: all 54 as decided); update `body.md` (the "What still fails" and Summary text change); show the text to him inline before any post.

## Posting it (needs his go-ahead; read each back)

Check first that #94 has not moved (`gh pr view 94 -R KJ5HST/methodology --json headRefOid,comments,reviews,updatedAt`): the text states facts about tip `972eb2c` and `upstream/main` `f34769f`. Then, from the repository root:

```
gh api -X PATCH repos/KJ5HST/methodology/pulls/94 \
  -f title="$(cat docs/planning/pr94-rewrite/title.txt)" \
  -F body=@docs/planning/pr94-rewrite/body.md
gh pr view 94 -R KJ5HST/methodology --json title,body --jq '.title, (.body|length)'   # read back
```

The old title was: `fix(trim): generated proofs stop reading red on lossless trims, and --reverify re-derives a frozen one (refs #93)`. Use `gh api -X PATCH`, not `gh pr edit`, and read both fields back before reporting.

## Scratch-only artifacts and limits

The prototypes (`trim_protoA.py`, `trim_protoAB.py`) were generated by `evidence/make_prototypes.py` and are not saved; regenerate them. The #93 repository was cloned (partial, sparse) into the session scratchpad, not into this repository. Nothing was pushed or posted. The `pr94` ref used to read the PR head was removed; `git fetch upstream pull/94/head` recreates the objects.
