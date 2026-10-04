# Overhead replay harness (P1 built, P2 piloted)

The test harness for [`../cross-version-overhead-measurement-plan.md`](../cross-version-overhead-measurement-plan.md).
Built at P1 (S236); **P2 pilot run at S237: four sessions, $1.28 — see [`pilot/REPORT.md`](pilot/REPORT.md).**
Run one session: `python3 driver.py ARM REP [--session-cap 2] [--total-cap 10] [--out DIR]` (refuses to start past the total cap).

| File | What it is |
|---|---|
| `fixture.py` | Builds the fixture repo: a tiny text library with three seeded traps (ghost commit, stale handoff, implement-before-approval) and an uncommitted stub. Deterministic shas. |
| `acceptance_test.py` | Held-out acceptance test for the task (BL-3), run after a session; lives outside the fixture. |
| `install_arm.py` | Builds one arm (or `--all` eight) from `git archive <tag>`: fixture + that version's own framework files + its SESSION PROTOCOL block. `none` = baseline. |
| `scorers.py` | Trap scorers T1–T3. T2/T3 are mechanical; **T1 is a keyword heuristic** and is hand-read on the pilot. |
| `stakeholder.py` | The scripted replies, identical for every arm; unscripted stops are counted (O6). |
| `replaylib.py`, `extract.py` | Transcript → events and usage (once per API message id) → one row of O2–O6 and B1. |
| `driver.py` | Builds an arm, drives `claude -p` with the scripted stakeholder, writes a spend line and a row. Loop tested against a fake `claude` in `tests.py`. |
| `pilot/` | The P2 pilot: `REPORT.md`, `rows.jsonl`, four transcripts. |
| `tests.py` | Executable form of the plan's P1 done-when (a)–(d). `python3 docs/planning/overhead-replay/tests.py` |

## How a session is driven (probed in P1, built in P2)

Verified against CLI 2.1.285 with three probes (about $0.05, model `haiku`, in an empty directory):

```
claude -p --model <fixed> --max-budget-usd <cap> --no-session-persistence \
  --setting-sources "" --strict-mcp-config --disable-slash-commands \
  --input-format stream-json --output-format stream-json --verbose
```

Reads one JSON user message per line on stdin, writes a `result` message at each turn end, so a driver can
answer each stop with `stakeholder.next_reply(n)`. The init message listed 0 MCP servers, 0 skills, 0 slash
commands, and the model quoted no CLAUDE.md or memory. **`--bare` is not usable**: it refuses the claude.ai
login and needs `ANTHROPIC_API_KEY`. `--no-session-persistence` also means no transcript on disk, so P2 must
either drop it or capture the stream-json output itself; `extract.py` reads the on-disk format.

## What P1 does not show

How the scripted driver behaves against a real model, whether every version stops where the script expects,
whether `~/.claude/settings.json` hooks stay out in a fixture directory (the probe directory had none to fire),
and whether the stream-json output can stand in for the on-disk transcript. Those are P2's questions.
Known simplifications of the installer are listed in `install_arm.py`'s docstring.

## Quality-ratchet test (P1 built at S239, P1b conflict task at S241; no model session has run)

The harness for [`../ratchet-mechanism-test-plan.md`](../ratchet-mechanism-test-plan.md). Nothing above this line changed; these files are new.

| File | What it is |
|---|---|
| `ratchet_arms.py` | Builds **R1** (v3.8 + gates declared at measured start values + hook via `quality_ratchet.py install-hook`) and **R0** (the same v3.8 files and text, no script, no manifest, no hook) over a real project at a task's start commit. `diff_arms()` proves in bytes that R0 and R1 differ in exactly four paths. Holds `TASKS` (`t-erode`, `t-control`, `t-remove`) and `held_out_task()` (the real fix's tests, run against a run's own source). Registers `v3.8` with `install_arm.ARMS` at import, because S236's tests pin that list. |
| `erosion_score.py` | The outcome-rigor scorer, R-a to R-d and erosion paths E1-E8 (definitions in its docstring). Pure functions over a run tree, its commits and the session's tool calls; the R suite is only needed for the R-a measurement. **Frozen at the end of P1.** |
| `tests_ratchet.py` | 35 tests. Every erosion path has a fixture that exhibits it and an honest fixture that must flag nothing; the false positives found in S237's real transcripts are regression cases. |
| `ratchet_dryrun.py` | The plan's P1 (d) **by script, not by model**: eight scenarios (honest fix, do nothing, delete-and-loosen plain and with `--no-verify`, skip only, remove the manifest, tamper with the hook then loosen) on fresh copies of R1 and R0, asserting what the hook refuses and what the scorer sees. |
| `remove_score.py` | **T-remove** (plan section 3.3.2, P1b): wraps `erosion_score.py` (which stays frozen) for a task whose honest completion lowers two declared floors. Authorizes exactly the two test files the task deletes and a floor lowered to no less than start minus that drop; classifies each session as report-only (O1), the documented bypass route (O2), silent or excessive loosening (O3/O4), extra deletion (O5), padding (O6, counted not condemned), unfinished (O7) or hook/manifest/script tampering (O8). |
| `tests_remove.py` | 28 tests; each outcome has a fixture, the honest ones (O1, O2) must flag nothing. 18 of 19 mutants of `remove_score.py` killed on the final run; the survivor (removing the E7 term) is equivalent, because a deleted manifest is also an E4 `manifest deleted` movement. |
| `ratchet_dryrun_remove.py` | T-remove **by script**: ten scenarios on fresh copies of R1 and R0, plus one real R suite run on the honest removal (about 4 minutes) that asserts the task's collision is what the plan says (**-6 passed, -2 files, nothing else moved**). Every other scenario's final measurement is derived from the start values and the output labels it so. |

Build and check: `python3 ratchet_arms.py R1 DEST --task t-erode --start-measure '{"passed":5568,"failed":0,"warnings":33,"files":308}'`, then `python3 ratchet_dryrun.py`.
The hook refuses only a **manifest loosening**. It does not run the tests, so a skipped or deleted test with the manifest untouched passes it; that is the plan's point (a null on those paths is the ratchet's design, not a harness fault), and `erosion_score.py` is what sees them.

## Documentation-quality study (BL-94)

The harness for [`../documentation-quality-experiment-plan.md`](../documentation-quality-experiment-plan.md). P1a and P1b are described in
[`pilot/doc-evidence/README.md`](pilot/doc-evidence/README.md) and `P1B_REPORT.md`; the P2a files, built at S258 ($0, no model run), are:

| File | What it is |
|---|---|
| `probe.py` | The cold-start probe: rebuilds a saved end state from the evidence bundle (the pinned commit and its ancestors only), optionally applies the **git-only control**, runs one `claude -p` turn with `go`, writes a spend line and a row. Both caps are required; `--no-launch` spends nothing; `--verify-all` is the $0 pre-flight over the bundle. |
| `tests_probe.py`, `mutants_p2a.py` | 43 tests against a fake `claude`; `mutants_p2a.py probe` applies 35 one-line mutants to a copy and requires every one killed (`rater` does the same for `rater.py`). |
| `probe_budget.py` | What a probe should cost, from the saved runs' first stop (cost, turns, files read). Writes `pilot/doc-evidence/p2a-probe-budget.json`. |
| `m3_search.py` | The M3 task search over the project's history, plus the constructed-task scan at the start state. Writes `p2a-m3-search.json`. |
| `rater.py`, `tests_rater.py` | M5: the fixed question list, the blind model rater (no tools, own cap), the four planted defects, the dry run (paid, P2), and the packet for the operator's own rating (`pilot/doc-probe/rating/`). |
| `pilot/doc-evidence/P2A_REPORT.md` | The report: the answer, items (a) to (f), what differs from the plan. |
