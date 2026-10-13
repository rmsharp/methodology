# BL-103 record (S305, 2026-10-12): the ratchet reads a timeout as a timeout

`starter-kit/quality_ratchet.py` 1.3.0 to **1.4.0**, a distributed tool. Fork only: nothing was sent to `KJ5HST/methodology`
(D8: one pull request later, each outward step his go-ahead). His picks at the S305 Phase 4 picker: approve the plan as
written; the orphan kill recorded as a new row ([BL-107](../BACKLOG-DETAIL.md#bl-107)), not built; version 1.4.0; 3600 s on
three of this repository's gates.

## 1. What was found

BL-103 (raised S280) said a timeout reads `unmeasured (exit 127)`. Measured, it is worse
(`measure-timeout.py`, output in `measure-timeout-output.txt`; each gate sleeps 6 to 8 s under a 1 s budget):

| gate shape | 1.3.0 reads | 1.4.0 reads |
|---|---|---|
| exit code, `max 0` ("must exit 0") | `fail`, measured 127, no note | `unmeasured`, `timeout (1 s)` |
| exit code, `min 100` | **`pass`**, measured 127 (127 clears the floor) | `unmeasured`, `timeout (1 s)` |
| `extract` `(\d+)` | **`pass`**, measured 8, read out of the timeout message | `unmeasured`, `timeout (1 s)` |

The cause is one line: `run()` returned `127, "", str(e)` for a `TimeoutExpired`, a value from the measurement's own domain, and the
message `str(e)` quotes the command line (`Command 'sleep 8; echo 5' timed out after 1 seconds`), which an `extract` regex can match.
`ITERATIVE_METHODOLOGY.md:444` says automated checks never pass by timeout; the tool broke that rule, and 7 of this repository's 18
gates (every one with no `extract`) are the exit-code shape. A first draft of one of my own tests failed to see this: its printed text sat in
the command line, so the old tool "passed" it by reading the command line back; the helper `slow()` now prints an expression, never
the literal.

**Also measured, not repaired here:** the sleeping commands are still running after `run_gates` returns (last line of the output file, for both
tools). The timeout kills the shell, not its children. That is [BL-107](../BACKLOG-DETAIL.md#bl-107).

## 2. What changed

| commit | what |
|---|---|
| `3017741` | 14 tests written first: 13 red for the intended reasons, one green pin (a five-gate run's `results` hash `8498441c1165`, computed with the 1.3.0 tool) |
| `ac85bb8` | `quality_ratchet.py` 1.4.0: `run_gate_command` returns `(rc, out, err, timed_out)`, a timeout has no exit code and no output; `measure_gate` reports `unmeasured`, `measured: null`, note `timeout (N s)`; `timeout_seconds` per gate (default 600), validated by `config_defects` (a positive finite number; not a bool, 0, a negative, a string, null, NaN or `inf`); gates sharing a command run it once under the largest budget any of them has; `compare` warns, never refuses, on a changed or removed `timeout_seconds`; `run()` no longer takes `timeout` or `shell` (the only caller that used them was the gate); `--selftest` 25 to 28 checks; the seed's `_gate_schema` names the field; floor `ratchet-unit-tests` 81 to 95 |
| `acfbefb` | mutation round 1 and the five tests it asked for (100 tests); floor 95 to 100; the mutation script |
| `5dd9a27` | `.quality-gates.json`: `timeout_seconds` 3600 on `tests-sh-passed`, `tests-sh-failed`, `migrate-layout-unit-tests` (not a threshold; its own commit so it reverts alone) |

The summary line a receipt cites keeps its format (`bin/check-handoff` and `close_out_report.py` read it); the exit code is unchanged (a
timed-out gate is `unmeasured`, exit 1).

## 3. How it is held

* **Tests:** 100 in `tools/test_quality_ratchet.py` (81 before), each of the 13 red tests seen failing with the reason it was written for
  (`('pass', 127.0)` for the floor, `('pass', 3.0)` for the extract, `('fail', 127.0)` for the ceiling), the `results` pin green before and after.
* **The old and the new tool over one manifest** (six gates: pass, pass by exit code, fail, declared-only, extract found nothing, a missing
  command): `results` `8b5ea9a786af`, `manifest` `cf277f8cb718`, the summary and every gate's dict equal.
* **Mutation, two rounds** (`mutate-bl103.py`, in a `--no-local` clone under `~/.cache`): round 1, 22 mutants, 16 killed, **6 survived**, each a
  behaviour no test named (the `:g` format of the budget in the note; a shared run's note; a command that cannot start read as a timeout; the 600 s
  default; an undeclared gate's default in a shared run; the memo's budget). Five tests added; the one for M7 I first wrote with the larger budget on the second gate,
  where the mutant gives the same note, and reordered it by reasoning about the mutant before round 2 (it was never run in the weaker form). Round 2, those six plus a new mutant on a *removed*
  `timeout_seconds`: **7 of 7 killed**, each by one test. 15 of the 23 are killed by the suite and **not** by `--selftest`, which is all an adopter
  has: the selftest is a smoke observation of the behaviour, not a second suite.
* **The real manifest:** `config_defects` reads none; `compare` against HEAD warns on exactly the three gates and refuses none (the hook printed the
  three warnings at commit `5dd9a27`).

## 4. The channels

The tool is distributed (`bin/_manifest.py`): adopters get 1.4.0 at their next `bin/sync`, after the one pull request. Simulated in scratch projects,
the old commit's `bin/sync` first, the new commit's `bin/status` and `bin/sync` after:

* legacy and `--layout new`: exactly one row is not current, `quality_ratchet.py` ("2 versions behind": the history holds the 1.4.0 commit and the later
  comment-fix commit); the dry run writes that one file (22 unchanged); the file lands byte-identical in `quality_ratchet.py` and in
  `methodology/quality_ratchet.py`, and the adopter's copy passes its own `--selftest` (28 checks) and reads a timed-out gate `unmeasured`, exit 1.
* **The seed is not distributed to a project that already has one:** `quality-gates.json` reads `present (left as-is)`, so an adopter reads about
  `timeout_seconds` only in the tool's module docstring, or from a seed it takes new.
* `--source=github` reads upstream's `main`, which holds `VERSION = "1.1.0"` of this tool (the fork is two minor versions ahead of it already);
  `upstream/main` is an ancestor of `HEAD`.

## 5. Not verified, not done

Not verified: Windows (`subprocess.run(..., timeout=)` is used as before, no new platform call; not run there), GitHub CI, any adopter's own tree, a
load of 100 or more (the timeout tests use 0.5 to 3 s sleeps; the 600 s case is what S280, S287 and S304 met and cannot be forced). The suite is about
20 s slower than before (9.7 s to 29 s: the timeout tests wait their budgets, and `--selftest` runs twice inside the suite).

Not done, by decision: BL-107, the kill of a timed-out command; repair 3 of BL-103, a Phase 0 / close-out rule that a cited gate run has
`0 unmeasured`; a mirror in the dashboard's `_gate_command_changes` (`tools/methodology_dashboard.py:3201` and its byte-identical twin) so a changed
`timeout_seconds` shows beside a changed `command`; `bin/tests.sh`.

## 6. His calls

(1) BL-107: build the kill, or leave it. (2) Repair 3: a rule in the runner's Phase 0 step 6 and Phase 3E, or a gate that counts unmeasured. (3) The
dashboard mirror. (4) Whether 3600 s stays the figure: it is a price, not a structure (a hung suite now holds a run for up to an hour before it reads
`timeout (3600 s)`). (5) D8, the release number, any tag.
