# P2 planted defects rebuilt: `missing` and `vague` at $0 (BL-94, S262, 2026-10-04)

**Cost: $0. No rating call was made; the study's ledger stays $4.0927 of its own $100.** The plan is
[`documentation-quality-experiment-plan.md`](../../../documentation-quality-experiment-plan.md) §5 P2; the run this follows is
[`P2_RATER_RERUN.md`](P2_RATER_RERUN.md) (S261: `missing` and `vague` MISSED on all 3 records in both orders, `wrong` caught); the code is
[`rater.py`](../../rater.py), its tests [`tests_rater.py`](../../tests_rater.py), its mutants [`mutants_p2a.py`](../../mutants_p2a.py). **A third paid
run is still his go-ahead (§5), and P3, D6 and D7 stay open.**

## The answer

1. **S261's variants still held what the two questions accept, by a count the new finders make.** S261's `missing` variants still held 12, 10
   and 16 sentences the new finder calls a pending action; S261's `vague` variants still held 32, 49 and 68 place tokens (issue references 23, 29,
   40; document and environment names 6, 12, 15; ticket ids 1, 3, 8; hyphenated place names 2, 3, 2; dotted names 0, 2, 1; and two in R1-r2
   that are spans a wrapped line had mis-paired). Section 1 gives the table and where each came from.
2. **Both builders are rebuilt and the check passes at zero on all three records** (§3), with the residue it cannot count printed beside it (§4).
3. **I read all six rebuilt variants, and what still stands is hazards, caveats and observations, not a stated next step or a named place** (§4).
   That is a reading by one reader, who knows what the records say; it is not a measurement.
4. **This does not show that the rater's `next_step` and `where` answers now flip.** S261's check passed too, over variants that still held the
   evidence. The check proves removal relative to its finders, and only the instrument's own flip proves the defect (fork learning #108).

## 1. What S261's variants left standing

Counted by running the S262 finders over the S261 variants (regenerated at the start of S262 from the S261 code and kept outside the tree):

| record | `missing`: pending sentences left | `vague`: tokens left | of which |
|---|---|---|---|
| v3.0-r1 | 12 | 32 | issue refs 23, document/env names 6, hyphenated place 2, ticket 1 |
| v3.7-r2 | 10 | 49 | issue refs 29, document/env names 12, hyphenated place 3, ticket 3, dotted 2 |
| R1-r2 | 16 | 68 | issue refs 40, document/env names 15, ticket 8, hyphenated place 2, dotted 1, other 2 |

Where the two new findings came from: the v3.7-r2 `vague` reason reads "names the next steps (owner closes #121, then #120, #103 or E4), the
files involved" (`rating-s261/dry-run.json`), so the issue and ticket references were visible to the rater and were not in S261's finders; and
the R1-r2 `vague` variant, line 102, reads `the relevant name relevant codethe relevant placethe relevant codeis.nathe relevant the relevant name`,
from the honest line ``binWidth` (`R/getPyramidPlot.R:55`) was dead in its `is.na` half.``: `CODE_SPAN` paired backticks within one line, a span
opened on the previous line left an odd one, and every later span on the line paired the wrong way, leaving `is.na` bare. Two spans in R1-r2 cross
a line break; v3.0-r1 and v3.7-r2 have none. S261's report §2 had already listed the pending action stated as status and the document names
(`NEWS`, `AUDIT_WORKSTREAM`) and "Age-Sex Pyramid"; the issue references and the wrapped span are what it had not.

## 2. What changed (`rater.py` unless named)

- **Units** (`units` `:119`, `unit_text` `:141`, `per_unit` `:147`): a paragraph, list item, heading or receipt field with its hard-wrapped lines;
  a blank line and a fence line are units of their own. The builders and `location_tokens` (`:240`) work on a unit, so a span or a sentence that
  wraps is seen whole. `CODE_SPAN` `:224` may now cross a line break.
- **`missing`** (`defect_missing` `:197`): drops the labelled next-step paragraphs as before, then every sentence that states a pending action
  (`PENDING` `:168`, `sentences` `:174`). A sentence that takes a receipt field's whole value takes the field with it.
  **`PENDING` was fitted to the sentences of these three records** (it lists "NOT closed", "still needs", "left alone", "Deferred", "you'll need to",
  "must run", "owner action", "couldn't close", "I left it", "say the word", "if you want" and a few more); a fourth record may say it another way,
  which is what the residue is for. A bare "decide", "must" or "leave ... alone" is guidance or a hazard and is not in it (tested both ways).
- **`vague`** (`_vague_text` `:256`): also removes issue references (`ISSUE_REF` `:234`), ticket ids of a letter and one or two digits (`TICKET`
  `:235`; `S313`, a session number, stays), upper-case document and environment names (`UPPER_NAME` `:232`: an underscore, or `NEWS`, `CHANGELOG`,
  `README`, ...; `RED`, `DONE`, `NOT`, `TDD` are emphasis and stay), hyphenated title-case places (`HYPHEN_TITLE` `:233`) and dotted function
  names (`DOTTED` `:230`). Builder and finder are one definition (`LOCATION_FINDERS` `:236`).
- **Check and report** (`next_step_evidence` `:297`, `defect_check` `:349`, `defects_report` `:382`): `missing` now counts labels plus pending
  sentences; each defect carries a `residue` (`residue_pending` `:317`, `residue_names` `:323`), the classes no builder uses, printed as
  "still standing, counted by no finder" and carried into the dry-run results and summary. It is informational and never a refusal.
- **Not changed:** `wrong`, `fabricated`, the question list, `dry_run`, `doc_score.py` (frozen), the packet (`packet.md` and `sheet.csv` regenerate
  byte-identical) and S259's and S261's saved results, which stay true of the builders that made them.

## 3. Results

`python3 docs/planning/overhead-replay/rater.py defects --out DIR` ($0, exit 0). Evidence is what the finders count, before then after:

| record | `missing` (labels + pending sentences) | S261: `missing` (labels) | `vague` (tokens) | S261: `vague` |
|---|---|---|---|---|
| v3.0-r1 | 15 to 0 | 2 to 0 | 329 to 0 | 297 to 0 |
| v3.7-r2 | 17 to 0 | 3 to 0 | 404 to 0 | 355 to 0 |
| R1-r2 | 23 to 0 | 3 to 0 | 475 to 0 | 413 to 0 |

`missing` removes 14.3%, 12.4% and 18.4% of the honest record's characters (S261's builder: 5.6%, 7.2%, 9.4%). `vague` is longer than its
honest record by 2.6%, 4.7% and 2.9%, because "the relevant place" is longer than most paths. No variant gained an unbalanced `**` (one unit of the
R1-r2 honest record has one, and its `missing` variant keeps it).

## 4. What I read in the six rebuilt variants, and what stands

Method: I printed every sentence of each `missing` variant that carries a broad cue (need, must, should, will, remain, pending, follow-up,
decide, until, owner, next) and every sentence that mentions an issue, closing, pushing or a remote, and read the final message of each; for
`vague` I listed every name-shaped token left, by class, and read the v3.7-r2 final message whole.

- **`missing`, what stands:** v3.0-r1 keeps gotcha (2), that override validation runs twice so a user sees the same warning twice (its "Not fixed
  here" sentence is gone), and "I did not re-run it at baseline HEAD". v3.7-r2 keeps "No git remote: `gh issue list/close/comment` and `git push` do
  nothing useful here" and a testthat edition-2 hazard. R1-r2 keeps five observations with no stated action: the over-0.5 advisory fires twice;
  the `tests-passed` gate sits at 3734 while the suite measures 3747; three `runGeneKeepR` processes started on Sep 28 to 29; `SESSION_NOTES.md` is
  3.85 MB; and "Keep `.quality-gates-results.json` in place: the next Phase-0 reconcile compares the receipt's cited results against it". A reader
  can infer a follow-up from several of these; none is stated as one. No "Next session", "Next steps" or SUGGESTED NEXT block remains in any.
  One orphan sentence is left where its neighbour was removed ("This is a product question." in v3.0-r1).
- **`vague`, what stands:** no file, function, issue, ticket or document name is left. Left are emphasis words (`RED`, `GREEN`, `NOT`, `TDD`),
  session numbers (`S313`, `S314`) and version strings (`v3.7`, `v3.8`), tool and package names (`Rscript`, `python3`, `Shiny`, `roxygen2`, the
  slash-separated package lists), `origin/master` (in two of the three), two cited works (Crow & Kimura 1970, Lacy 1989), headings, and **the next
  work in prose**: "citations audit" stands on 2, 3 and 3 lines and "roxygen harmonization" on 1, 2 and 1 (v3.0-r1, v3.7-r2, R1-r2). Whether a
  rater counts a prose topic as a place is the open question this leaves, and it is the one a paid run would answer. The text is also rougher
  (the replacement words stack: "the the relevant code").
- **The residue printed by the command is noisy by design**: its ALL-CAPS class lists `RED×18` and its slashed class lists `code/the×5`, the
  builder's own replacement words. It is there to be read, and the table above is what I read from it.

## 5. What this leaves, and the decisions that are his

- **Whether to spend on a third paid run.** The same command as S261's, `rater.py dry-run --call-cap 0.50 --total-cap 10 --out
  pilot/doc-probe/rating-s262`, would rate 3 records x 5 variants x 2 orders = 30 calls; **about $1.6 is an estimate** (S261's 30 calls at a mean
  $0.0538 cost $1.6146), not a measurement, and `--total-cap` is checked against the whole ledger, so `10` is P2's plan cap and not this run's.
  The model and effort S259 used are not recorded; S261 and this command use the code's defaults (`sonnet`, `high`).
- **Whether his own blind rating becomes the measure** and the model rater report-only (`sheet.csv` still has 6 rows and 0 answers), which costs
  $0 and does not depend on these defects at all.
- **D6 and D7 of the plan, and P3** (about $9 to $11, its own go-ahead), unchanged.
- **If a paid run still misses**, the readings in §4 say where to look first: the `vague` variants' prose topics, and the `missing` variants'
  observations from which a follow-up can be inferred. A miss then says the rater is lenient on those two questions, which is a finding about the
  rater and not about the defect.

## 6. Verification and what is not verified

- `python3 docs/planning/overhead-replay/tests_rater.py`: 74 tests OK (58 at the start of S262). The first 11 of the 16 new ones were written
  before the code and failed for the right reasons, the first of them reproducing the `codeis.nathe` text; the other 5 (four on the residue, one on the
  pending-sentence count) were written after it.
- `python3 docs/planning/overhead-replay/mutants_p2a.py rater`: 129 of 129 killed (72 at the start; 9 were repaired where the code moved and 57 added; no
  mutant survived the final code). Two items of my own dead code were found by asking what a mutant would change, and removed.
- `tests_probe.py` 58, `tests_doc_score.py` 130 and `tests_doc_evidence.py` 14 pass; `bin/check-links` OK.
- **Not verified:** that the rater's answers flip (a paid run); that the cue list covers a fourth record's wording; that removing sentences
  does not move the rater's answers to other questions for a reason other than the missing next step (`state` and `loose_ends` can move, and the
  harness reports them but does not require them).
