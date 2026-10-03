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
