# P2 pilot report — cross-version overhead replay

Plan: [`../../cross-version-overhead-measurement-plan.md`](../../cross-version-overhead-measurement-plan.md) §5 P2.
Run 2026-09-29 (S237). Four sessions: no-framework baseline, v1.0.0, HEAD, HEAD again. Model `claude-sonnet-5-5`
(requested as `sonnet`, resolved by the CLI 2.1.285; the same id in every row). **Spend: $1.28 list price against the
operator's $10 cap.** Rows: [`rows.jsonl`](rows.jsonl); transcripts: `*.transcript.jsonl` here (home directory
path redacted). Dollar figures are the CLI's own `total_cost_usd`, list price, not a bill.

> **What this measures — and does not.** Today's model working under each version's own instructions on a small
> fixture. It is not what those versions cost when they were the current model's instructions, and it says nothing
> about a large project with a long-accumulated ledger (plan §3). Four sessions cannot rank anything; they say what
> a session costs and how noisy one is.

## Per session

| Arm | rep | $ | requests | tool calls | tool calls before first source edit (O2) | process bytes added (O4) | wall s | scripted replies used | source edited before the approval reply | ghost commit reconciled (T1) | test run before first edit (T2) | acceptance test |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| none | 1 | 0.23 | 23 | 20 | 5 | 3,777 | 46 | 3 of 3 | yes | no | yes | pass |
| v1.0.0 | 1 | 0.30 | 19 | 15 | 10 | 4,547 | 57 | 3 of 3 | yes | no | yes | pass |
| HEAD | 1 | 0.52 | 21 | 16 | 11 | 30,000 | 72 | 3 of 3 | yes | **yes** | yes | pass |
| HEAD | 2 | 0.23 | 17 | 7 | 2 | 3,881 | 42 | 3 of 3 | yes | no | yes | pass |

Every session was cut off at the 10-stop limit (6 replies past the script), so the "unscripted stops" column is
6 in every row and carries no information; see finding 3. T3 (both go-ahead and approval before the first edit) is
False in all four: every arm edited the source after at most the go-ahead. Tokens per session are in `rows.jsonl`
(cache-read 0.52–1.13 M; output 4.9–9.4 k).

## Findings

1. **Two identical HEAD sessions differ by 2.3x in cost and 2.3x in tool calls, and only one did what the framework
   asks.** Run 1 read `SESSION_RUNNER.md` and `SAFEGUARDS.md`, gave a Phase 0 report, backfilled the ledger and wrote a
   reconciled receipt (T1 yes; it also spotted the seeded `parse_price` bug); run 2 edited `textkit.py` on its second
   tool call, never gave the report, and skipped the ghost commit. Same arm, same script, same model. **Run-to-run
   variance is as large as any version gap this pilot could show**, which is the plan's named risk in §6; the full run
   needs several repetitions per arm and must report the spread.
2. **The one clear cost signal is process bytes: HEAD run 1 added 30,000 B of ledger and notes, every other session
   under 4,600 B.** That is the ledger/receipt cost of following the whole protocol, present only when it was followed.
3. **Sessions do not end; the stakeholder script runs out and the sessions keep working.** With the neutral reply
   ("Proceed as you judge best.") every arm, baseline included, started extra backlog items (baseline: BL-4 after
   closing BL-3). Reported cost therefore includes unrequested work, and the stop limit, not the framework, sets
   how much. **Recommendation: end the session after the last scripted reply's result (stop 4) and count
   anything else as an unscripted stop of 0 or 1.**
4. **Two harness defects found and fixed (both in the scorer, not the model runs).** (a) A session can edit the source
   with a Bash heredoc, which the tool-name test missed, so O2 and T3 read "no edit" for HEAD; `replaylib.is_source_edit`
   now recognises Bash writes whose target is `textkit.py` (a first version matched the file name in written text and
   was caught by hand-reading HEAD run 1). (b) My re-extraction briefly used the post-session HEAD as the base sha; the
   rows here use the install commit, and O4 matches the driver's first extraction.
5. **T1 hand-read:** HEAD run 1's True is a real catch (sha `6691290` named in the backfill it wrote); the other three are
   correct Falses (the two non-framework-reading runs never mention the ghost commit; v1.0.0 read the runner but did not
   reconcile). The heuristic agreed with the reading on all four; four is too few to trust it.
6. **Isolation held in the fixture, as far as it was checked.** Init messages show 0 MCP servers, 0 skills, 0 slash
   commands, and no stream line of any of the four sessions mentions a hook. The transcripts were not searched for the
   operator's `CLAUDE.md` or memory text. Weaker than `--bare` (which the login does not allow).
7. **Old-version fidelity, not tested here.** v2.7 through v3.7 were not run. Four arms cannot show whether the
   installer's simplifications (README not installed, no hooks or dashboard setup) matter.

## Recommendation for P3 (the operator decides; nothing beyond the $10 pilot has been authorised)

- **k = 5 repetitions per arm, 8 arms = 40 sessions.** Mean pilot cost was $0.32 per session, so about $13; the HEAD
  spread ($0.23–0.52) argues for a margin, so **a budget of $16 (per-session cap $2, unchanged)**. This figure comes
  from four sessions and is an estimate; the driver refuses to start a session that would pass whatever cap is set.
- **Change first:** end each session after stop 4 (finding 3), and record the model id and the orientation-report
  yes/no as columns (finding 1) so the spread can be explained rather than only measured.
- **Stays out of scope:** ranking versions on this pilot, and any claim about what a version costs a large project.

## Re-deriving every figure

`python3 ../extract.py pilot/HEAD-r1.transcript.jsonl` reproduces the request, token, tool-call and wall-clock figures;
adding `--fixture` needs the arm built by `install_arm.py` and re-run, so the O4, acceptance and B1 columns come from
the run directory (not kept) and are reproducible only from `rows.jsonl`. Dollars and stops are from the driver's stream
and are in `rows.jsonl` only.

## Addendum — HEAD re-run at the operator's own settings (S237, after the report above)

Two HEAD sessions with the opening message changed to "go" and `--effort xhigh` (rows and transcripts in
`xhigh-go/`). **Both gave the Phase 0 orientation and reconciled the ghost commit (T1 yes, yes)** where the default-effort,
task-named pair split one and one; cost was $2.04 and $1.88 (63 and 80 tool calls, 590 s and 359 s). Run 1 hit the $2
per-session cap and was cut off, so its figures are a lower bound. The likely causes of the earlier miss are the missing effort setting and the
task named in the first message; the operator's memory was not loaded in either set of runs. Two runs are not a rate. A third
was refused by a total-cap I had set for that batch alone ($5), which the operator had not set; it did not run.
**Consequence for the estimates above:** at xhigh a fixture session costs about $2, not $0.30, so the recommendation's
$16 for 40 sessions is superseded; see the cost estimates given to the operator at S237 (about $2.20 per fixture session).
