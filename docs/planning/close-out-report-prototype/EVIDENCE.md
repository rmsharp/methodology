# Evidence for `close-out-report-actuator-plan.md` (S252, 2026-10-03)

Everything here was run, on this machine, against `claude` **2.1.288**. Where a claim comes only from a
document or a subagent's report it is listed under *Not measured*. The scripts in this directory are
**prototypes for the plan, not shipped tools**: nothing here is in `bin/_manifest.py`, `bin/tests.sh` or any
hook configuration, and no settings file was edited.

## Reproduce

```
python3 docs/planning/close-out-report-prototype/checks.py     # exit 0 = every row passes, every mutant caught
```

| Group | Result |
|---|---|
| Hook decision table (10 rows, payload shape copied from the real harness) | 10 of 10 pass |
| Report-lint mutants (10 corruptions of a good report) | 10 of 10 refused |
| Hook mutants (6 single-defect copies of `hook_proto.py`) | 6 of 6 turn the table red |

## Measured on the real harness (`claude -p`, scratch directories outside the repo, haiku)

| Question | Answer | How |
|---|---|---|
| Does a project `Stop` hook run in `-p` mode? | Yes | spike: payload log written |
| Stop payload fields | `session_id`, `transcript_path`, `cwd`, `prompt_id`, `permission_mode`, `hook_event_name`, `stop_hook_active`, `last_assistant_message`, `background_tasks`, `session_crons` | payload logged |
| Does `{"decision":"block","reason":...}` make the model continue? | Yes; it reprinted its answer with the required last line | spike |
| Is the block repeatable? | **No.** The second Stop in the chain carried `stop_hook_active: true`; the hook honours it and allows | spike, two Stop payloads |
| `SessionStart` payload | `session_id`, `transcript_path`, `cwd`, `hook_event_name`, `source: "startup"` | payload logged |
| Does `--continue` keep the `session_id`? | **Yes**, and `SessionStart` fires again with `source: "resume"` | two fresh runs, then `--continue`: same id on the 2nd and 3rd |
| Session with no close-out | Hook fired once, `owed: false`, did not interfere | run A |
| Close-out done, final message "Done." | Blocked once; model ran the generator; report passed the lint | run B, 5 turns, 15 s |
| Three-turn session (`--continue` twice) | Turn 1 blocked once then a clean report (HEAD `0f0256f` = repo HEAD). Turn 2, a follow-up question: allowed, no second report. Turn 3, after a commit moved HEAD to `f8c1412`: the plain reply was blocked and a **fresh report with the new HEAD** was issued | `e2e3` |

**Cost, measured:** a blocked-and-continued one-turn run $0.0064; the close-out loop (run B) $0.045;
the three-turn session $0.081. All haiku. Cumulative `total_cost_usd` per session as reported by the CLI.
Not measured at Sonnet or Opus rates.

## Measured on the repository

* **Receipt field sizes, 250 complete receipts (live + every archived shard).** Medians: `what_was_done`
  1,753 B, `next_steps` 1,647 B, `gotchas` 1,422 B, `runtime_smoke` 1,195 B, `active_task` 703 B; maxima 3-6 KB.
  250 of 250 carry numeric `self_score` and `predecessor_score`. So a report cannot be built by pasting
  receipt fields (that is the "wall of prose" BL-79 describes), but its scores can be read from the receipt
  with no failure on the existing data.
* **`starter-kit/SESSION_RUNNER.md` is already over its declared ceiling:** 55,406 B against 41,364 B
  (`python3 starter-kit/context_budget.py --status`). Its §3G block (lines 293-302) is **252 B**. A
  replacement that carries the four items and a pointer is 595 B (+343 B); the net-zero candidate in the plan
  is 239 B (-13 B).

## Two errors in my own instruments, caught before they reached the plan

1. **A mutant that tested nothing.** "Treat a missing baseline as owed" first crashed on `b["id"]` when the
   baseline was `None`; the fail-quiet wrapper turned the crash into an allow, so decision-table row 9 passed
   *for the wrong reason* and the mutant was reported missed. Rebuilt as `b is None or ...`, row 9 catches it.
2. **A fixture copied from a mutated tree.** The first three-turn run copied `HANDOFFS.md` out of an earlier
   run's *working tree*, where the receipt was already `complete`; the session therefore started with a
   finished close-out and the hook, correctly, never fired. It proved nothing about blocking. Redone from the
   committed `pending` ledger (`git show HEAD:HANDOFFS.md`), which is the run in the table above.

## Not measured (documented, or unknown) — the plan treats each as such

* `SubagentStop` is a separate event, so a subagent finishing does not fire the main `Stop` hook: **from a
  subagent's summary of the hooks page, not run.**
* Whether `session_id` survives **compaction** (`source: "compact"`) is **not stated and not measured.** The
  design fails quiet if it changes (no baseline for the new id, so no firing).
* The `fork` `source` value, and `/clear`: listed in the docs' `SessionStart` table, not run.
* How the two messages (the first reply and the forced report) **render in the interactive terminal UI.** `-p`
  mode prints only the last. This is the one thing only the operator watching a real close-out can check.
* Any model other than haiku; any harness other than Claude Code 2.1.288.
* **Report quality.** The lint checks shape and agreement with the receipt. In the runs above the model wrote
  "did not: None" and "Task was straightforward" and the lint passed them; it cannot do otherwise.

## P2: the shipped `--hook` on the real harness (S254, 2026-10-03)

The tool is no longer the prototype: `starter-kit/close_out_report.py --hook` (v1.1.0), 68 unit tests, 15 mutants each
caught by its named row. Reproduce the live part with `bash docs/planning/close-out-report-prototype/p2_live_scenarios.sh`
(`SETUP_ONLY=1` builds the fixtures and spends nothing). Same harness version as above, claude **2.1.288**, haiku, scratch
repos outside this one, the plan's snippet in the scratch repo's own `.claude/settings.local.json`, each call capped at $0.15.

| Row | Prompt | Result |
|---|---|---|
| 1 | receipt left pending; "Reply with exactly one word: hello" | `hello`; no log line; baseline file written by `SessionStart` |
| 2 | run a script that completes the receipt and commits; "reply with exactly: Done." | log `blocked R1,R2,R3,R4,R5`, then `reported`; final message was the report, HEAD = the repo's HEAD at the time |
| 5 | `--continue`, "Reply with exactly: thanks" | `thanks`; no new log line, no second report |
| 6 | `--continue`, run a script that commits; "reply with exactly: Pushed." | log `blocked`, then `reported`; the report's HEAD is the new commit |

**Independent check:** the last report passes `close_out_report.py --check` against the scratch repo's HEAD (`OK`); the first
report fails it with `R5` (HEAD moved after it was printed), which is the staleness rule seen on a real report; the "thanks"
reply is not a report, as it should not be. **Cost:** $0.0196 + $0.0935 = **$0.113** (`total_cost_usd` is cumulative per
session, so only each session's last figure is added; summing every turn would double-count to $0.234). **The model complied
with the block 2 of 2 this run, 3 of 3 with S252's, all on haiku.**

Seen again: the five judgment texts the model supplied were thin (`Predecessor handoff (S1): 7/10 — S1`; `Next session: Ready for
next session`) and the lint passed them, which is the limit the plan states (§2.3, item 4). Still **not measured:** Sonnet or Opus;
compaction; and how the first reply and the forced report render in the operator's interactive terminal.
