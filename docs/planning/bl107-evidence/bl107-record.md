# BL-107 record (S306, 2026-10-12): the ratchet stops a gate's command that outlives its budget

`starter-kit/quality_ratchet.py` 1.4.0 to **1.5.0**, a distributed tool. Fork only: nothing was sent to `KJ5HST/methodology`
(D8: one pull request later, each outward step his go-ahead). His picks at the S306 Phase 4 picker: build as planned; Windows
unchanged and stated; `SIGKILL` at once, not TERM then KILL.

## 1. What was measured

BL-107 (raised S305) said `subprocess.run(shell=True, timeout=t)` kills the shell, not its children, and proposed a process
group per gate command killed on a timeout, noting two costs to settle first (Ctrl-C, Windows). Four variants, each run as its
own process with a signal aimed at it, a `sleep` with a unique duration as the marker, and `ps` read after the run
(`bl107-runner.py`, `bl107-harness.py`; the output is `bl107-output.txt`; macOS, Python 3.10.12):

| scenario | 1.4.0 | new session + `killpg` on a timeout only | the same + cleanup on any exception and on SIGHUP and SIGTERM |
|---|---|---|---|
| timeout, plain command | **1 child survives** | 0 | 0 |
| timeout, a child that ignores SIGTERM | **1 survives** | 0 | 0 |
| Ctrl-C (SIGINT to the tool's group) | 0 | **1 survives** | 0 |
| hangup (SIGHUP to the tool's group) | 0 | **1 survives** | 0 |
| `kill <tool pid>` (SIGTERM) | **1 survives** (already so today) | 1 | 0 |

**The row's fix alone is a regression.** A command in a session of its own no longer receives the terminal's Ctrl-C or a closed
terminal's hangup, so the tool would orphan it on both, which 1.4.0 never did. The fix is the group kill *and* the tool turning
SIGHUP and SIGTERM into a cleanup-and-exit and re-raising `KeyboardInterrupt` after the same cleanup. SIGTERM is beyond parity.

**macOS raises `PermissionError` from `os.killpg`** when a member of the group is already dead and not yet reaped, although the
live members were signalled: a fourth variant (TERM first, then KILL) crashed on it, and a direct test shows
`killpg(pgid, 0)` on a zombie-only group raising it. `ProcessLookupError` is a group already gone. So the helper swallows both and
kills the shell itself as well. `bl107-stress.py`: 60 rounds of `SIGKILL` on a live group raised neither and left nothing.
Polling a group for liveness (a grace period before KILL) hits the same error, which is why the plan chose KILL at once and named the
cost: a git write in flight can leave `.git/index.lock`.

**Inventory (grep):** the only call site of the command runner is `run_gate_command` (`starter-kit/quality_ratchet.py`), reached by
`measure_gate` and `run_gates`; `def run_gates` is a structural signature the dashboard reads
(`tools/methodology_dashboard.py:810`) and keeps its name. Nothing under `bin/`, `tools/`, `starter-kit/` or `.githooks/` uses a
process group or a session, and none of this repository's 18 gate commands depends on a controlling terminal.

## 2. What changed

* `run_gate_command` (POSIX): `Popen(..., shell=True, start_new_session=True)`; a timeout or any exception out of the wait calls
  `_stop_group` (`SIGKILL` to the group, then `proc.kill()`, then `proc.wait()`; every `OSError` from either call swallowed);
  `_stop_on_signals` turns SIGHUP and SIGTERM into `SystemExit(128 + n)` for the duration, leaves a signal the caller ignores
  ignored (`nohup`), installs nothing off the main thread (`ValueError`), and puts back what it replaced; `KeyboardInterrupt` is
  re-raised unchanged after the cleanup. A command that finishes is left alone, background children and all.
* `HAS_PROCESS_GROUPS = os.name == "posix"`: where it is false (Windows) the 1.4.0 `subprocess.run` path runs byte for byte, and a
  timed-out command there may keep running; the module docstring says so.
* `--selftest` 28 to 30 checks (a timed-out gate's command is gone; SIGTERM to the tool, sent by the gate's own command to `$PPID`,
  exits 143 and leaves nothing). `signal` and `time` joined the stdlib set the suite allows. The seed's `_gate_schema` says the
  command is stopped with its process group (not on Windows). `VERSION` 1.5.0.

## 3. How it is held

120 tests in `tools/test_quality_ratchet.py` (100 before; the `ratchet-unit-tests` floor went to 118 and then 120, each in its own commit), written
RED first: nine failed on 1.4.0, each for its own reason (a child still running 5 s after a timeout, four times; `-1 != 129` and
`-15 != 143`; the absent constant; two selftest labels and a seed phrase). The signal tests run the tool as a child process and aim the
signal at *that* process, so a tool that fails to handle one fails a test instead of ending the suite. **The surface for Ctrl-C and a
closed terminal is a real pty** (`TestARealTerminalStopsTheCommand`: the tool is the pty's session leader, `\x03` is written to the
master, closing the master is the hangup), because `kill(1)` is only an emulation of what the terminal driver does. The `results`
hash pin (`8498441c1165`) is untouched: the result dict's shape did not change.

**A defect found in the tests, not the tool, by the first mutation run.** The round's baseline read red under `nohup` (`Ran 1 test in
30.070s`, fail-fast) and the same suite read 118 OK from a shell. `nohup` sets SIGHUP to *ignore*, ignored signals survive fork and exec, and the
tool correctly leaves an ignored SIGHUP ignored (a `nohup` run is meant to survive its terminal, and the command inherits the ignore), so the child
driver took the disposition it was given and the two hangup tests failed: `still running 30 s after`, and `0 != 129`. Reproduced with
`nohup python3 tools/test_quality_ratchet.py <the two signal classes>` (exactly those two red). This repository starts its long runs, the gate
and the mutation round, under `nohup`, so the suite would have read red in the very runs that cite it. The driver now sets SIGHUP to default or to
ignore explicitly (`DRIVER`'s fourth argument asks for ignore, which `test_a_hangup_the_caller_ignores_stays_ignored` uses); the signal tests read OK
with and without `nohup`.

**Mutation, two rounds, 29 mutants** (`mutate-bl107.py`, run only in a `--no-local` clone under `~/.cache`; output in `bl107-mutation-output.txt`; each
mutant is one exact-string replacement in the tool, killed by the unit suite or by the tool's own `--selftest`, which is all an adopter has).
*Round 1, 26 mutants: 21 killed, 5 survived.* The five were each a weakness in a test, not in the tool: **M17** (a finished command's group killed too)
survived a test that looked at the child the instant after the kill, when a `SIGKILL` had not landed; **M6** and **M22** (the shell never reaped,
the pipes never closed) cannot be seen from outside the Popen object, because CPython closes a dropped object's pipes; **M23** (a handler the
caller installed replaced by the default) had no test; **M21** (`HAS_PROCESS_GROUPS = True`) is true of POSIX either way. Four tests followed (M17's
now watches 1.5 s; a spy keeps the Popen object and asserts `returncode` and closed pipes; a caller's handler comes back; the module is read as each
platform would read it, `os.name` patched). *Round 2, aimed at behaviours no test named: the five survivors re-run and three new mutants (only the first
replaced handler put back; an `OSError`'s class instead of its message; `KeyboardInterrupt` instead of `SystemExit`): 8 of 8 killed.* Over the 29, the suite
kills 29 and the selftest 11; **18 are killed by the suite and NOT by the selftest**, which is what the selftest's two new checks do not reach (the
signal-handler behaviours, the boundary, the reaping). Not pinned, on purpose: the budget's duration (a bound tight enough to catch an off-by-one
would flake at the loads that cause a timeout), and a weakened *selftest* condition (a correct tool passes either way).

## 4. The channels

The tool is distributed (`bin/_manifest.py`): adopters get 1.5.0 at their next `bin/sync`, after the one pull request. Simulated in
scratch projects synced at the commit before the change (`273847e`, 1.4.0), then read and synced by the new commit's tools (`76f0082`):

* legacy and `--layout new`: exactly one row is not current, `quality_ratchet.py` ("1 version behind"); the dry run says `would write`
  for that one file only; it lands byte-identical in `quality_ratchet.py` and in `methodology/quality_ratchet.py`; the adopter's copy
  passes its own `--selftest` (30 checks) in both layouts, and a gate that outlives its 2 s budget reads `unmeasured`
  (`timeout (2 s)`), exit 1, with its child gone.
* **The seed is not re-sent to a project that has one** (`.quality-gates.json` reads `present (seed; left as-is)`): an adopter reads the
  new sentence only in the module docstring, or in a seed it takes new.
* `--source=github` reads upstream's `main`, which holds an older tool; the fork is ahead of it already.

## 5. Not verified, not done

Not verified: **Windows** (the 1.4.0 path is selected there by `HAS_PROCESS_GROUPS` and pinned by a test with the constant patched, but
nothing here ran on Windows), **Linux and GitHub CI** (the platform calls are POSIX, none macOS-specific except the `PermissionError`
handling, which is `OSError` and so wider than macOS), the adopters' live trees, and a load that forces the real 600 s. A command that
calls `setsid` itself leaves the group and is not stopped.

Not done, by decision: Windows tree kill (`taskkill /T /F`, not runnable here); TERM before KILL; BL-103 repair 3 (a cited run has
`0 unmeasured`); the dashboard mirror of `timeout_seconds`; whether 3600 s stays.

## 6. His calls

(1) Whether a command that calls `setsid` itself, or Windows, is worth more than this. (2) BL-103 repair 3. (3) The dashboard mirror.
(4) Whether 3600 s stays. (5) D8, the release number, any tag.
