# P2 report: four cold probes and the rater dry run (BL-94, S259, 2026-10-04)

**Cost: $2.4781 of P2's $10 cap and of the study's own $100** (4 probes $0.7696; 31 rating calls $1.7085). No cap was hit.
The plan is [`documentation-quality-experiment-plan.md`](../../../documentation-quality-experiment-plan.md) §5 P2; the harness is in
[`overhead-replay/`](../..); the rows are in [`../doc-probe/`](../doc-probe/). **P3 is its own go (D4); §5 restates its cost.**

## The answer

1. **A probe costs $0.16 to $0.24, mean $0.19, not the plan's $1** (the git-only control $0.17). Each was one `claude -p` turn
   (sonnet 5.5, xhigh, CLI 2.1.289), 20 to 28 seconds, ended by the driver's one-stop limit as scripted. S258's estimate from the saved
   runs' first stop was $0.35; the measured cost is about half of it.
2. **A rating call costs $0.044 to $0.066, mean $0.055** (8 questions and an arm guess over a 20,000 to 31,000 character record).
3. **Every claim I could check in the four cold reports was true: 36 checked, none wrong** (§2). The reports do not separate
   the arms by accuracy; what differs is what each recommends (§2, the control).
4. **The model rater, as built, does not separate honest records and misses most planted defects** (§3): all 3 honest records scored
   8 of 8 in both orders; `wrong` was caught on 2 and, on the third, in the one order that parsed; `vague` was missed on all 3 although every path and anchor was removed;
   `missing` is inconclusive because the defect leaves a next step in place. Its arm guess matched the record's arm on 2 of 3 records
   and abstained on the third, citing the install commit and tool names.
5. **Three defects in my own harness, found by running it for real** (§4): `reads` misses Bash reads; one of 31 rating replies was
   unparsable and the raw reply was not kept; a `--no-launch` check leaves a clone that makes the real launch refuse.

## 1. Spend, and how to re-sum it

| Call | Run | Cost | Wall |
|---|---|---|---|
| probe | v3.0 `real-3.7/v3.0-r1` | $0.1950 | 19.9 s |
| probe | v3.7 `real-3.7/v3.7-r3` | $0.2444 | 27.7 s |
| probe | v3.8-text `t-control-fix/R1-r2` | $0.1599 | 21.6 s |
| probe | the same, git-only control | $0.1703 | 23.6 s |
| rating | canary (v3.0, honest, order A) | $0.0451 | 5.4 s |
| rating | dry run, 30 calls (3 records, each honest + 4 planted variants, 2 orders) | $1.6634 | 3 min 45 s |

Re-sum: `python3 -c "import json;print(sum(json.loads(l)['cost_usd'] for l in open('docs/planning/overhead-replay/pilot/doc-probe/spend.jsonl')))"`
prints 2.478064 over 35 rows, none zero; each probe row in `rows.jsonl` equals its ledger row. **Caps:** probe session $1.00 (the
highest probe used 24% of it), rating call $0.50 (the highest used 13%), P2 total $10 (25%).

## 2. The four cold reports, hand-read

Each report is `../doc-probe/<run>/report.md`; its stream log is beside it. Claims checked against the rebuilt end state in `/tmp/doc-probe/`:
v3.0 8, v3.7 12, v3.8-text 9, control 7 = **36, none wrong**. Not checked: the dashboard scores and dates each report quotes.

| Cold session | Opened (Read tool and Bash) | Recommended first |
|---|---|---|
| v3.0 | `SESSION_NOTES.md` (Bash `head -150`), `CLAUDE.md`, `SESSION_RUNNER.md`, `SAFEGUARDS.md` | none; listed four candidates, asked |
| v3.7 | `SESSION_NOTES.md`, `CLAUDE.md`, `SESSION_RUNNER.md`, `SAFEGUARDS.md` | none; five candidates, asked |
| v3.8-text | `HANDOFFS.md`, `SAFEGUARDS.md`, `SESSION_NOTES.md`, `CLAUDE.md` (Bash), an empty `memory/MEMORY.md` | the `.Rbuildignore` one-liner from the handoff |
| v3.8-text, git-only control | `HANDOFFS.md`, `CLAUDE.md`, `SAFEGUARDS.md`, `SESSION_NOTES.md` three times, `BACKLOG.md` (Bash `head -40`) | **"confirm what the HEAD revert was meant to do"** |

**The control's cold session saw the extra restore commit (`602a8b5c`, "Restore tracked documentation to its text at the install
commit") in `git log`, read it correctly, and made it its first recommendation.** That is the confound S258 named (gotcha 5),
observed: the control differs from the documented arm by the commit as well as by the missing text. It did not mislead the session
about the state. No cold session made an Edit or Write call.

## 3. The rater dry run

Three records (`honest_set`), each honest plus four planted variants, both question orders (`rating/dry-run-summary.json`):

| | v3.0-r1 | v3.7-r2 | R1-r2 (v3.8-text) |
|---|---|---|---|
| honest, order A / B | 8/8, 8/8 | 8/8, 8/8 | 8/8, 8/8 |
| `wrong` (should flip `consistent`, `state`) | caught (6/8, 6/8) | caught (7/8, 7/8) | B 7/8 (flipped); A unparsable, so the summary lists no verdict |
| `missing` (should flip `next_step`) | 8/8 | 8/8 | 8/8 |
| `vague` (should flip `where`) | 8/8 | 8/8 | 8/8 |
| `fabricated` (flips nothing, reported only) | 8/8 | 8/8 | 8/8 |
| arm guess (A, B) | cannot_tell, cannot_tell | 3.7, 3.7 | 3.8, 3.8 |

**`vague` is a real miss.** The defect removed every path (82, 90, 129) and every `file:line` anchor (19, 21, 26) from the
records (`doc_score.PATH_RE`, `ANCHOR_RE`), and the rater still answered `where` yes 8 of 8. **`missing` is inconclusive:** the
builder removes only part of the next-step text (`SUGGESTED NEXT` survives in all three records and the rater quotes
`gh issue close 121`), so the question can truthfully stay yes. **The arm guess is a cue, not a measurement of the text:** the guess
for the v3.8 record cites the install commit `badc16ef` and `quality_ratchet`, `methodology_trim` and the receipt ledger by name.
Reading the guess as correct is my comparison of the label to the record's arm. **Consequence for D5:** at the ceiling every honest
record scores 8 of 8, which is P1b's null again; this rater would not separate the arms, and a rater that sees tool names is not blind.

## 4. Defects found in my own harness (not fixed this session)

**Fixed at S260 ($0, no model call):** items 1 to 3 below, and the rater's two misses in §3 (`missing` and `vague` were built from too narrow a definition of their question's evidence; the builders and a $0 check that each defect removed its evidence are in `rater.py`, described in `../../README.md`). Item 4 is not a harness defect and is unchanged.

**Re-run at S261 ($1.6146):** the rater was run again on the rebuilt defects; `missing` and `vague` were still missed and `wrong` caught. See [`P2_RATER_RERUN.md`](P2_RATER_RERUN.md).

1. **`probe.py` `reads` records the Read tool only.** The v3.0 session read `SESSION_NOTES.md` through Bash `head -150` and `reads`
   lists three files without it. P3 must take reads from the stream log's Bash commands too.
2. **`rater.call_rater` discards the raw reply when parsing fails.** One call (`t-control-fix/R1-r2/wrong/A`, "Unterminated string
   starting at ... char 171") cost $0.0635 and left only the error text; the cause is unknown.
3. **`probe.py --no-launch` leaves its clone and a real launch then refuses** ("exists; refusing to overwrite"), after 3 seconds and
   $0 spent. The four clones were mine, clean, minutes old; I deleted them by name and relaunched.
4. **The cold sessions run with auto-memory on** and three of the four look for it (`ls memory`, once a `Read` of `MEMORY.md`). The directory for each
   throwaway clone path was empty, so nothing of the operator's memory reached a probe; whether the saved sessions had it on is not known.

## 5. What this means for P3 (D4: the figure is his)

Plan §P3 (3a) estimated 21 probes and about 6 controls at $1 each, a 25% margin and about $4 of rating: **about $38.** Restated from
P2's measured cost: 21 probes at $0.192 and 6 controls at $0.170 = $5.06 (all 27 at the highest, $0.244, = $6.60); with the plan's 25%
margin $6.3 to $8.3; model rating of 27 records in both orders, 54 calls at $0.055 = $2.98. **About $9 to $11, an estimate from four
probes and 31 rating calls.** The probe is cheap enough; the open question is not cost. All four cold reports were accurate, so the
documented and undocumented arms differ so far only in what they recommend, and the rater cannot separate honest records. P3 would
buy more probes of a measure that has shown no separation at n=4; that is a reason to decide D6/D7 and the rater's defects (§3, §4)
before P3, not after.

## 6. Verification and what is not verified

- Ledger re-summed (§1); rows equal ledger; the 36 claims (§2); `git diff db8d765..HEAD --name-only` (db8d765 is S258's last
  commit) shows only files under `docs/` and `HANDOFFS.md` and `CHANGELOG.md`: the pilot's own rows, this report, the trim's shard and index.
- **Not done:** no probe output was run through the frozen scorer (`doc_score.py`, untouched; P3's job); the operator's own six-record
  rating is not done; M3 is deferred. **Not verified:** that probes on CLI 2.1.289 behave like the saved runs on 2.1.285 to 2.1.287;
  that four probes predict the main run.
