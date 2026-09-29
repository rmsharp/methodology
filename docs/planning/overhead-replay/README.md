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
