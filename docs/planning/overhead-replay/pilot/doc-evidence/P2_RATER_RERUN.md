# P2 rater re-run: the model rater on the planted defects rebuilt at S260 (BL-94, S261, 2026-10-04)

**Cost: $1.6146 for 30 rating calls; the study's ledger is $4.0927 of its own $100, and of P2's $10 cap.** The plan is
[`documentation-quality-experiment-plan.md`](../../../documentation-quality-experiment-plan.md) §5 P2; the first run and the defects it
found are in [`P2_REPORT.md`](P2_REPORT.md) §3 and §4; the harness is in [`overhead-replay/`](../..); the results are in
[`../doc-probe/rating-s261/`](../doc-probe/rating-s261/) (`dry-run.json`, `dry-run-summary.json`). **P3 is still its own go (D4).**
**S262 rebuilt the two defects this report found standing, at $0: [`P2_DEFECTS_S262.md`](P2_DEFECTS_S262.md).** The run and its numbers below are
unchanged and describe the S260 builders.

## The answer

1. **The rebuilt `missing` and `vague` defects were MISSED again, on all 3 records in both question orders (12 of 12 calls).** The rater
   answered `next_step` yes and `where` yes every time, so its scores are the same 8 of 8 as the honest records'. The $0 check that
   S260 added passed both defects before any call was made (`next-step labels` 2, 3, 3 to 0; `location tokens` 297, 355, 413 to 0), and
   the rater's answers did not change from S259's. **The check proved removal of the labels and tokens it counts; it did not prove the
   questions' evidence was gone** (§2).
2. **`wrong` was caught on all 3 records in both orders** (6/8 and 6/8 on v3.0-r1; 6/8 and 6/8 on v3.7-r2; 7/8 and 7/8 on R1-r2).
   S259 had v3.7-r2 at 7/8 and one R1-r2 call unparsable; the rebuilt builder removes more, as S260's gotcha 2 expected. **All 30 calls
   parsed, so repair (b) of S260, which keeps a failed call's raw text, was not exercised: no real call has failed since it.**
3. **The honest records are at the ceiling again: all 3 scored 8 of 8 in both orders, with no question the orders disagreed on.** This
   is S259's result repeated; a rater that scores every honest record 8 of 8 cannot separate the arms (plan D5, P1b's null).
4. **The arm guess is unchanged from S259:** `cannot_tell` on v3.0-r1, `3.7` on v3.7-r2, `3.8` on R1-r2, in both orders. The reasons
   quote the install commit (`badc16ef`, "methodology arm v3.7") and tool names, so it reads cues in the record, not the quality of its text.

## 1. Results, beside S259's

Three records (`honest_set`), each honest plus four planted variants, both question orders; cells are the number of the 8 questions
answered yes (A / B). Verdicts are the harness's (`planted_check`, `combine_orders`).

| | v3.0-r1 | v3.7-r2 | R1-r2 (v3.8 text) | S259 (same three records) |
|---|---|---|---|---|
| honest | 8 / 8 | 8 / 8 | 8 / 8 | 8/8 on all three |
| `wrong` (should flip `consistent`, `state`) | 6 / 6, caught | 6 / 6, caught | 7 / 7, caught | caught on v3.0-r1 (6/8, 6/8) and v3.7-r2 (7/8, 7/8); on R1-r2 order B 7/8, order A unparsable |
| `missing` (should flip `next_step`) | 8 / 8, **MISSED** | 8 / 8, **MISSED** | 8 / 8, **MISSED** | 8/8, 8/8, 8/8 |
| `vague` (should flip `where`) | 8 / 8, **MISSED** | 8 / 8, **MISSED** | 8 / 8, **MISSED** | 8/8, 8/8, 8/8 |
| `fabricated` (flips nothing, reported only) | 8 / 8 | 8 / 8 | 8 / 8 | 8/8 on all three |

## 2. Why `missing` and `vague` were missed: the evidence is still in the record

Read from the rendered variants (`python3 rater.py defects --out <dir>` writes them at $0) and from the rater's own `reason` text:

- **`missing`.** The builder removes the labelled next-step lines. What stays is a concrete pending action stated as status: v3.0-r1's status
  says "`gh issue close 121` / a comment must be run from a checkout that has one"; v3.7-r2's `active_task` says "#121 still needs closing on
  GitHub by the owner" and its final message "You'll need to close #121 yourself"; R1-r2's status says "The owner ... must run `gh issue close 121`".
  The rater quotes it ("run `gh issue close 121`"; "the owner must close #121"). Closing the issue **is** a specific next step, so `yes`
  is a defensible answer to *"does the record state a next step specific enough that a successor could start it"*; the defect did not
  produce a record without one. This is the first case in S260's gotcha 1 (a next step implied by a status line), now observed.
- **`vague`.** The builder replaces every path, anchor and backticked span with "the relevant file" or "the relevant code", and the check
  counts none left. The question is *"names at least one file, function or location"*, and names remain that the finder does not count:
  `NEWS`, `AUDIT_WORKSTREAM`, `renv`, `roxygen`, "Age-Sex Pyramid" (v3.0-r1 and v3.7-r2 each keep several). **The rater's `reason` is one
  free-text sentence about the record as a whole and never mentions `where`, so I cannot say which name it counted.** Whether the rater
  is blind to a vague record is therefore not established by this run; what is established is that the defect is not yet a record with
  no nameable place.

## 3. What this means

- **For the rater as an instrument:** it catches a planted contradiction (`wrong`) reliably and scores every honest record 8 of 8. Both
  facts were true at S259 and are unchanged, so the open question was never whether it finds a contradiction; it is whether it can
  separate records that are honest and differ in how useful they are, and nothing in two runs shows it can.
- **For the check S260 built:** it is necessary and not sufficient. It is relative to its finders (next-step labels; place-in-code
  tokens), and a defect can pass it while leaving the evidence the question accepts. A finder for "any statement of a pending action"
  or "any file-like name" would be broader and would also degrade the record more.
- **Decisions this leaves with the operator (none made here):** (a) rebuild `missing` and `vague` once more so a reader cannot find a next
  step or a name (a $0 session, then about $1.6 for a third run, with its removal check widened to the finders in §2); (b) accept the
  model rater as report-only, with his own blind rating of the six-record packet as the measure (`rater.py score-human`, $0, not yet done);
  (c) D6 and D7 of the plan, which stay open before P3. P3 is estimated at about $9 to $11 (P2 report §5).

## 4. Spend, and how to re-sum it

Re-sum: `python3 -c "import json;print(sum(json.loads(l)['cost_usd'] for l in open('docs/planning/overhead-replay/pilot/doc-probe/spend.jsonl')))"`
prints 4.0927 over 65 rows, none zero (35 rows from S259, 30 from this run at $1.6146, mean $0.0538 a call; S259's 30-call dry run was
$1.6634). **Caps:** rating call $0.50 (`--call-cap`; the highest call here cost $0.0652, 13% of it), P2 total $10 (`--total-cap`, checked
against the whole ledger before each call), the study $100. The command: `python3 rater.py dry-run --call-cap 0.50 --total-cap 10 --out
pilot/doc-probe/rating-s261`, run from `docs/planning/overhead-replay/`; `--out` was set so S259's `rating/dry-run.json` and the operator's
rating packet beside it stayed as they were.

## 5. Verification and what is not verified

- **Checked:** the ledger re-summed (above); `EXIT=0` in the run's log and no `rater.py` process left; the $0 `rater.py defects` run before the
  first call (exit 0, the S260 figures); every verdict in §1 read from the parsed answers in `dry-run.json`, not only from the summary; the reasons in §2
  read from `dry-run.json`, and the surviving names and statements in §2 from the rendered variants.
- **Not verified:** the model and effort S259 used for its rating calls are not recorded where I could find them; this run used the code's
  defaults (`--model sonnet --effort high`), so a difference between the runs on `wrong` (v3.7-r2 7/8 to 6/8) is explained by the rebuilt
  builder only on the evidence that its label set is wider. Each cell is one call per order, and the rater is not deterministic. The names
  listed in §2 are what I found by search, not a complete list. No probe output went through the frozen scorer (`doc_score.py`, untouched);
  his own rating is not done; M3 is deferred.
