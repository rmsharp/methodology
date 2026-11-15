#!/usr/bin/env python3
"""Unit tests for starter-kit/quality_ratchet.py — the declared-threshold ratchet.

CANONICAL-ONLY. Not in bin/_manifest.py, so adopters do not receive it; they get the
tool's own --selftest. This suite imports the starter-kit module directly (the one
bin/sync distributes), so what is tested is what ships.

Every gate is observed FAILING as well as passing (Learning #12): a ratchet whose
refusal was never seen to fire is a suggestion with a hook attached.
"""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import re
import shlex
import signal
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
STARTER = REPO / "starter-kit" / "quality_ratchet.py"

_spec = importlib.util.spec_from_file_location("quality_ratchet", STARTER)
qr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(qr)

PY = sys.executable


def manifest(*gates):
    return {"version": 1, "gates": list(gates)}


def gate(name, direction="min", threshold=1, **kw):
    g = {"name": name, "direction": direction, "threshold": threshold}
    g.update(kw)
    return g


def slow(seconds, prints="''", marker=None):
    """A gate command that outlives a short budget: it records its start in `marker` (so a test can
    count runs), sleeps `seconds`, then prints the Python EXPRESSION `prints`. An expression, never the
    literal text: a literal would sit in the command line, and the tool's old timeout message quoted the
    command line, so an extract could read it back and a test would pass for the wrong reason. Tests that
    expect a timeout give a budget well under `seconds`; tests that expect completion give one well over
    it, so load cannot flip either."""
    start = f"open({marker!r}, 'a').write('x'); " if marker else ""
    return f'"{PY}" -c "{start}import time; time.sleep({seconds}); print({prints})"'


class TestCompareIsTheRatchet(unittest.TestCase):
    """compare(old, new) is pure — no git — so every rule is testable without a repo."""

    def setUp(self):
        self.base = manifest(gate("cov", "min", 80), gate("cc", "max", 10))

    def test_lowering_a_floor_is_refused(self):
        new = manifest(gate("cov", "min", 79), gate("cc", "max", 10))
        refusals, _ = qr.compare(self.base, new)
        self.assertEqual(len(refusals), 1)
        self.assertIn("floor lowered 80 -> 79", refusals[0])

    def test_raising_a_ceiling_is_refused(self):
        new = manifest(gate("cov", "min", 80), gate("cc", "max", 11))
        refusals, _ = qr.compare(self.base, new)
        self.assertEqual(len(refusals), 1)
        self.assertIn("ceiling raised 10 -> 11", refusals[0])

    def test_removing_a_gate_is_refused(self):
        refusals, _ = qr.compare(self.base, manifest(gate("cov", "min", 80)))
        self.assertEqual(len(refusals), 1)
        self.assertIn("'cc' removed", refusals[0])

    def test_flipping_a_direction_is_refused(self):
        new = manifest(gate("cov", "max", 80), gate("cc", "max", 10))
        refusals, _ = qr.compare(self.base, new)
        self.assertTrue(any("direction min -> max" in r for r in refusals))

    def test_tightening_passes(self):
        new = manifest(gate("cov", "min", 85), gate("cc", "max", 8))
        self.assertEqual(qr.compare(self.base, new), ([], []))

    def test_adding_a_gate_passes(self):
        new = manifest(*self.base["gates"], gate("links", "max", 0))
        self.assertEqual(qr.compare(self.base, new), ([], []))

    def test_unchanged_passes(self):
        self.assertEqual(qr.compare(self.base, json.loads(json.dumps(self.base))), ([], []))

    def test_a_changed_command_warns_but_does_not_refuse(self):
        old = manifest(gate("cov", "min", 80, command="a"))
        new = manifest(gate("cov", "min", 80, command="b"))
        refusals, warnings = qr.compare(old, new)
        self.assertEqual(refusals, [])
        self.assertEqual(len(warnings), 1)
        self.assertIn("`command` changed", warnings[0])

    def test_equal_threshold_written_as_string_is_not_a_loosening(self):
        # JSON hand-edits sometimes quote numbers; "80" == 80 for the ratchet's purposes.
        new = manifest(gate("cov", "min", "80"), gate("cc", "max", 10))
        self.assertEqual(qr.compare(self.base, new)[0], [])

    def test_a_changed_timeout_seconds_warns_but_never_refuses(self):
        # A budget cut far enough turns a gate into one that never measures: the same back door a
        # changed `command` opens, held the same way (warned, left to review), never refused.
        old = manifest(gate("suite", "min", 5, command="a"))
        for new_budget in (1800, 1):
            new = manifest(gate("suite", "min", 5, command="a", timeout_seconds=new_budget))
            refusals, warnings = qr.compare(old, new)
            self.assertEqual(refusals, [])
            self.assertEqual(len(warnings), 1, warnings)
            self.assertIn("`timeout_seconds` changed", warnings[0])
        both = manifest(gate("suite", "min", 5, command="a", timeout_seconds=3600))
        self.assertEqual(len(qr.compare(both, manifest(gate("suite", "min", 5, command="a",
                                                             timeout_seconds=10)))[1]), 1)
        self.assertEqual(qr.compare(both, json.loads(json.dumps(both))), ([], []))
        # Dropping the field falls back to the default budget, which may be a cut: it warns too.
        removed = qr.compare(both, manifest(gate("suite", "min", 5, command="a")))
        self.assertEqual((removed[0], len(removed[1])), ([], 1))


class TestConfigDefects(unittest.TestCase):
    def test_clean_manifest_has_no_defects(self):
        self.assertEqual(qr.config_defects(manifest(gate("a"), gate("b", "max", 0))), [])

    def test_each_defect_is_named(self):
        cfg = manifest(
            {"direction": "min", "threshold": 1},                 # no name
            gate("dup"), gate("dup"),                             # duplicate
            gate("dirn", "up", 1),                                # bad direction
            gate("num", "min", "many"),                           # non-numeric threshold
            gate("rx", "min", 1, command="x", extract="("),       # bad regex
            gate("orphan", "min", 1, extract="(\\d+)"),           # extract without command
        )
        d = "\n".join(qr.config_defects(cfg))
        for token in ("missing `name`", "duplicate name", "`direction` must be",
                      "`threshold` must be a number", "not a valid regex",
                      "`extract` without `command`"):
            self.assertIn(token, d)

    def test_gates_must_be_a_list(self):
        self.assertEqual(qr.config_defects({"gates": {}}), ["`gates` must be a list"])
        self.assertEqual(qr.config_defects("nope"), ["`gates` must be a list"])

    def test_timeout_seconds_must_be_a_positive_finite_number(self):
        for bad in (0, -5, "30", True, None, [], float("nan"), float("inf")):
            d = qr.config_defects(manifest(gate("suite", command="x", timeout_seconds=bad)))
            self.assertEqual(len(d), 1, (bad, d))
            self.assertIn("`timeout_seconds` must be a positive number", d[0])
            self.assertIn("'suite'", d[0])
        for good in (30, 0.5, 1800, 3600.0):
            self.assertEqual(qr.config_defects(manifest(gate("suite", command="x", timeout_seconds=good))),
                             [], good)
        self.assertEqual(qr.config_defects(manifest(gate("suite", command="x"))), [])


class TestMeasureGate(unittest.TestCase):
    def test_extracted_number_compared_against_a_floor(self):
        g = gate("n", "min", 3, command=f'"{PY}" -c "print(\'value 7\')"', extract=r"value (\d+)")
        r = qr.measure_gate(os.getcwd(), g, 30)
        self.assertEqual((r["measured"], r["status"]), (7.0, "pass"))
        g["threshold"] = 8
        self.assertEqual(qr.measure_gate(os.getcwd(), g, 30)["status"], "fail")

    def test_without_extract_the_exit_code_is_the_measurement(self):
        ok = gate("exit", "max", 0, command=f'"{PY}" -c "pass"')
        bad = gate("exit", "max", 0, command=f'"{PY}" -c "raise SystemExit(3)"')
        self.assertEqual(qr.measure_gate(os.getcwd(), ok, 30)["status"], "pass")
        r = qr.measure_gate(os.getcwd(), bad, 30)
        self.assertEqual((r["measured"], r["status"]), (3.0, "fail"))

    def test_no_command_is_unmeasured_never_pass(self):
        r = qr.measure_gate(os.getcwd(), gate("declared", "min", 0), 30)
        self.assertEqual(r["status"], "unmeasured")
        self.assertIsNone(r["measured"])

    def test_extract_that_matches_nothing_is_unmeasured_never_pass(self):
        g = gate("n", "min", 0, command=f'"{PY}" -c "print(\'no digits\')"', extract=r"(\d+)")
        r = qr.measure_gate(os.getcwd(), g, 30)
        self.assertEqual(r["status"], "unmeasured")
        self.assertIn("matched nothing", r["note"])

    def test_a_missing_command_is_unmeasured_not_pass(self):
        # A threshold of `max 0` with a command that cannot even start must not read as pass:
        # the shell's 127 is the measurement, and 127 > 0.
        g = gate("ghost", "max", 0, command="definitely-not-a-real-command-xyz")
        self.assertEqual(qr.measure_gate(os.getcwd(), g, 30)["status"], "fail")


class TestATimeoutIsNotAMeasurement(unittest.TestCase):
    """ITERATIVE_METHODOLOGY.md: automated checks never pass by default or by timeout. Until 1.4.0 a
    timeout was reported as exit 127: an exit-code gate read it as `fail` (`max 0`) or as `pass` (a floor
    at or under 127), and an `extract` gate could read a number out of the timeout MESSAGE."""

    def assert_timed_out(self, r, budget):
        self.assertEqual((r["status"], r["measured"]), ("unmeasured", None), r)
        self.assertEqual(r["note"], f"timeout ({budget} s)")

    def test_an_exit_code_gate_with_a_ceiling_is_unmeasured_not_fail(self):
        r = qr.measure_gate(os.getcwd(), gate("slow", "max", 0, command=slow(3)), 0.5)
        self.assert_timed_out(r, "0.5")

    def test_an_exit_code_gate_with_a_floor_is_unmeasured_not_pass(self):
        # 127 clears a floor of 100: this one read PASS.
        r = qr.measure_gate(os.getcwd(), gate("slow", "min", 100, command=slow(3)), 1)
        self.assert_timed_out(r, "1")

    def test_extract_never_reads_a_number_out_of_the_timeout_message(self):
        # The old message carried the command line, `sleep(3)` and the interpreter's path among it:
        # (\d+) matched a digit of it and the gate read PASS on a number nothing measured.
        g = gate("slow", "min", 1, command=slow(3, "5"), extract=r"(\d+)")
        self.assert_timed_out(qr.measure_gate(os.getcwd(), g, 1), "1")

    def test_a_gate_declaring_timeout_seconds_uses_it_not_the_default(self):
        g = gate("slow", "min", 1, command=slow(3, "5"), extract=r"(\d+)", timeout_seconds=0.5)
        self.assert_timed_out(qr.measure_gate(os.getcwd(), g, 60), "0.5")

    def test_the_note_prints_the_budget_the_way_a_person_wrote_it(self):
        # `1.0` and `1` are the same budget; the note a receipt may quote must not say `1.0 s`.
        g = gate("slow", "max", 0, command=slow(3), timeout_seconds=1.0)
        self.assert_timed_out(qr.measure_gate(os.getcwd(), g, 60), "1")

    def test_a_command_that_cannot_start_is_not_a_timeout(self):
        # No such directory: the OS refuses before anything runs. That is exit 127 as it always was,
        # and nothing the word `timeout` should describe.
        g = gate("ghost", "max", 0, command=slow(0.1))
        r = qr.measure_gate("/no/such/directory/for/a/gate", g, 30)
        self.assertEqual((r["status"], r["measured"]), ("fail", 127.0))
        self.assertNotIn("timeout", r["note"])

    def test_the_default_budget_is_600_seconds(self):
        # Documented in the module docstring and the seed's schema, so pinned.
        import inspect
        self.assertEqual(qr.DEFAULT_TIMEOUT, 600)
        self.assertEqual(inspect.signature(qr.run_gates).parameters["timeout"].default, 600)

    def test_a_command_inside_its_budget_is_measured_as_before(self):
        g = gate("quick", "min", 1, command=slow(0.2, "5"), extract=r"(\d+)", timeout_seconds=60)
        r = qr.measure_gate(os.getcwd(), g, 0.001)
        self.assertEqual((r["measured"], r["status"], r["note"]), (5.0, "pass", ""))


# The tool as a child process: it prints what run_gate_command returned. Signals are aimed at THIS process,
# never at the test runner, so a tool that fails to handle one fails the test instead of ending the suite.
# SIGHUP and SIGINT are set here, never inherited: `nohup` sets SIGHUP to ignore and a command started with `&` from a
# non-interactive shell has SIGINT ignored, ignored signals survive fork and exec, and Python installs no
# KeyboardInterrupt when it starts with SIGINT ignored. This repository starts its long runs (a gate, a mutation round)
# as `nohup ... &`: a driver that took the dispositions it was given failed the two hangup tests under nohup and the two
# Ctrl-C tests in the background (S306). A fourth argument asks for SIGHUP ignored, as `nohup` would.
DRIVER = ("import importlib.util, signal, sys\n"
          "s = importlib.util.spec_from_file_location('qr', sys.argv[1])\n"
          "m = importlib.util.module_from_spec(s); s.loader.exec_module(m)\n"
          "signal.signal(signal.SIGINT, signal.default_int_handler)\n"
          "signal.signal(signal.SIGHUP, signal.SIG_IGN if len(sys.argv) > 4 else signal.SIG_DFL)\n"
          "print(m.run_gate_command(sys.argv[2], '.', float(sys.argv[3])), flush=True)\n")


class _GateCommandChildren(unittest.TestCase):
    """A gate command of the shape that matters: a shell that stays alive as the PARENT of a long-running
    child and records the child's pid. A single simple command would not do: `sh -c 'prog'` execs prog, the
    shell IS the program, and killing the shell kills it -- a test of that shape passes on the old tool for
    the wrong reason. A test suite run under a shell is the shape here (BL-107)."""

    def setUp(self):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        self.pidfile = os.path.join(td.name, "pid")
        self.addCleanup(self.reap)

    def command(self, before="", record=">", first=""):
        return f"{first}sleep 600 & echo $! {record} {shlex.quote(self.pidfile)}; {before}wait"

    def recorded(self):
        try:
            return int(open(self.pidfile).read().split()[0])
        except (OSError, ValueError, IndexError):
            return None

    def wait_for_pid(self, within=30):
        end = time.time() + within
        while time.time() < end and self.recorded() is None:
            time.sleep(0.02)
        pid = self.recorded()
        if pid is None:
            self.fail(f"the gate command recorded no child pid in {within} s: it never started")
        return pid

    @staticmethod
    def alive(pid):
        try:
            os.kill(pid, 0)
        except (ProcessLookupError, PermissionError):   # macOS answers EPERM for a dead, unreaped process
            return False
        return True

    def assert_stopped(self, pid, within=5):
        end = time.time() + within
        while time.time() < end and self.alive(pid):
            time.sleep(0.05)
        self.assertFalse(self.alive(pid), f"the gate command's child {pid} is still running "
                                          f"{within} s after the tool stopped")

    def reap(self):
        pid = self.recorded()
        if pid:
            try:
                os.kill(pid, signal.SIGKILL)
            except OSError:
                pass

    def drive(self, command, budget=60):
        return subprocess.run([PY, "-c", DRIVER, str(STARTER), command, str(budget)],
                              capture_output=True, text=True, timeout=180)


class TestATimedOutCommandIsStopped(_GateCommandChildren):
    """BL-107. `subprocess.run(shell=True, timeout=t)` kills the shell, not the shell's children: a test
    suite that outlived its budget ran on to its end, with its result discarded, through every gate after
    it (failure mode #29). 1.4.0 reported the timeout truthfully and did not stop the command."""

    def test_the_child_of_a_timed_out_command_is_stopped(self):
        r = qr.run_gate_command(self.command(), os.getcwd(), 5)
        self.assertEqual(r, (None, "", "", True))
        self.assert_stopped(self.wait_for_pid())

    def test_two_gates_over_one_command_run_it_once_and_stop_it_once(self):
        cfg = manifest(gate("passed", "min", 1, command=self.command(record=">>"), extract=r"(\d+)"),
                       gate("failed", "max", 0, command=self.command(record=">>"), extract=r"(\d+)"))
        snap = qr.run_gates(os.getcwd(), cfg, timeout=5)
        self.assertEqual([(g["status"], g["note"]) for g in snap["gates"]], [("unmeasured", "timeout (5 s)")] * 2)
        self.assertEqual(len(open(self.pidfile).read().split()), 1, "the shared command ran more than once")
        self.assert_stopped(self.wait_for_pid())

    def test_a_timed_out_command_leaves_its_shell_reaped_and_its_pipes_closed(self):
        # Observed on the Popen object itself, kept by a spy: CPython closes a dropped object's pipes and a later
        # Popen reaps a zombie, so nothing outside the object shows either lapse for long.
        made, real = [], subprocess.Popen

        def spy(*a, **k):
            made.append(real(*a, **k))
            return made[-1]
        with mock.patch.object(qr.subprocess, "Popen", side_effect=spy):
            self.assertEqual(qr.run_gate_command(self.command(), os.getcwd(), 5), (None, "", "", True))
        proc = made[0]
        self.assertIsNotNone(proc.returncode, "the shell of a timed-out command was left unreaped")
        self.assertTrue(proc.stdout.closed and proc.stderr.closed, "the pipes of a timed-out command were left open")
        self.assert_stopped(self.wait_for_pid())

    def test_a_child_that_ignores_sigterm_is_stopped_too(self):
        # Ignored signals are inherited: the child of this shell cannot be asked to stop, only made to.
        self.assertEqual(qr.run_gate_command(self.command(first="trap '' TERM; "), os.getcwd(), 5),
                         (None, "", "", True))
        self.assert_stopped(self.wait_for_pid())

    def test_an_oserror_while_waiting_reads_as_127_and_still_stops_the_command(self):
        def boom(*a, **k):
            self.wait_for_pid()
            raise OSError("the pipe went away")
        with mock.patch.object(qr.subprocess.Popen, "communicate", side_effect=boom):
            r = qr.run_gate_command(self.command(), os.getcwd(), 30)
        self.assertEqual(r, (127, "", "the pipe went away", False))
        self.assert_stopped(self.wait_for_pid())

    def test_a_command_that_exits_is_not_followed_by_a_group_kill(self):
        # The boundary, pinned: only a command that outlives its budget (or a signal) stops its group. One that
        # finishes and leaves a background child behind keeps doing exactly what it did in 1.4.0.
        cmd = f"sleep 600 >/dev/null 2>&1 & echo $! > {shlex.quote(self.pidfile)}"
        self.assertEqual(qr.run_gate_command(cmd, os.getcwd(), 30), (0, "", "", False))
        pid = self.wait_for_pid()
        end = time.time() + 1.5   # a SIGKILL lands in milliseconds: look right after it AND for long enough to see it
        while time.time() < end:
            self.assertTrue(self.alive(pid), "a finished command's background child was killed")
            time.sleep(0.05)

    def test_a_refused_group_kill_does_not_escape(self):
        # macOS raises PermissionError from killpg when a member of the group is already dead and unreaped
        # (measured, S306); ProcessLookupError is a group already gone. Neither is a failure of the gate.
        for exc in (ProcessLookupError, PermissionError):
            with self.subTest(exc=exc.__name__), mock.patch.object(qr.os, "killpg", side_effect=exc):
                t0 = time.time()
                r = qr.run_gate_command(slow(40), os.getcwd(), 0.5)
                self.assertEqual(r, (None, "", "", True))
                self.assertLess(time.time() - t0, 20, "the shell itself was not stopped when killpg refused")

    def test_where_there_are_no_process_groups_the_command_runs_as_it_did_in_1_4_0(self):
        with mock.patch.object(qr, "HAS_PROCESS_GROUPS", False), \
                mock.patch.object(qr.os, "killpg") as killpg, \
                mock.patch.object(qr.subprocess, "Popen", wraps=subprocess.Popen) as popen:
            done = qr.run_gate_command(f'"{PY}" -c "print(7)"', os.getcwd(), 30)
            late = qr.run_gate_command(slow(3), os.getcwd(), 0.5)
        self.assertEqual(done, (0, "7\n", "", False))
        self.assertEqual(late, (None, "", "", True))
        killpg.assert_not_called()
        self.assertTrue(popen.called)
        for call in popen.call_args_list:
            self.assertNotIn("start_new_session", call.kwargs)


@unittest.skipUnless(os.name == "posix", "process groups and POSIX signals")
class TestASignalToTheToolStopsTheCommand(_GateCommandChildren):
    """The command now runs in its own session, so the terminal's Ctrl-C and a closed terminal's hangup no
    longer reach it: the tool must stop it itself, or the fix for a timeout orphans it the other way round
    (measured, S306: one child left after SIGINT and after SIGHUP to the tool's group)."""

    def test_sigterm_stops_the_child_and_the_tool_exits_143(self):
        r = self.drive(self.command(before="kill -TERM $PPID; "))
        self.assertEqual(r.returncode, 143, r.stderr)
        self.assert_stopped(self.wait_for_pid())

    def test_sighup_stops_the_child_and_the_tool_exits_129(self):
        r = self.drive(self.command(before="kill -HUP $PPID; "))
        self.assertEqual(r.returncode, 129, r.stderr)
        self.assert_stopped(self.wait_for_pid())

    def test_ctrl_c_stops_the_child_and_still_raises_keyboard_interrupt(self):
        r = self.drive(self.command(before="kill -INT $PPID; "))
        self.assertIn("KeyboardInterrupt", r.stderr)
        self.assertIn(r.returncode, (130, -signal.SIGINT), r.stderr)
        self.assert_stopped(self.wait_for_pid())

    def test_a_handler_the_caller_installed_is_put_back(self):
        mine = {s: (lambda signum, frame: None) for s in (signal.SIGHUP, signal.SIGTERM)}
        old = {s: signal.signal(s, h) for s, h in mine.items()}
        self.addCleanup(lambda: [signal.signal(s, h) for s, h in old.items()])
        qr.run_gate_command("exit 0", os.getcwd(), 30)
        for s, h in mine.items():
            self.assertIs(signal.getsignal(s), h, f"{signal.Signals(s).name}: the caller's handler was not put back")

    def test_a_hangup_the_caller_ignores_stays_ignored(self):
        # `nohup` sets SIGHUP to ignore on purpose, so a run survives its terminal: the tool must not turn it
        # into an exit. The command inherits the ignore, so it survives too -- as it always did.
        r = subprocess.run([PY, "-c", DRIVER, str(STARTER), "kill -HUP $PPID; echo survived", "60", "nohup"],
                           capture_output=True, text=True, timeout=180)
        self.assertEqual((r.returncode, r.stdout.strip()), (0, "(0, 'survived\\n', '', False)"), r.stderr)

    def test_the_signal_handlers_are_put_back(self):
        names = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
        before = {s: signal.getsignal(s) for s in names}
        qr.run_gate_command("exit 0", os.getcwd(), 30)
        self.assertEqual({s: signal.getsignal(s) for s in names}, before, "after a command that finished")
        qr.run_gate_command(slow(3), os.getcwd(), 0.5)
        self.assertEqual({s: signal.getsignal(s) for s in names}, before, "after a timeout")

        def boom(*a, **k):
            self.wait_for_pid()
            raise RuntimeError("boom")
        with mock.patch.object(qr.subprocess.Popen, "communicate", side_effect=boom):
            with self.assertRaises(RuntimeError):
                qr.run_gate_command(self.command(), os.getcwd(), 30)
        self.assertEqual({s: signal.getsignal(s) for s in names}, before, "after an exception")
        self.assert_stopped(self.wait_for_pid())   # an exception out of the wait stops the group too

    def test_a_call_from_another_thread_runs_and_leaves_the_signals_alone(self):
        names = (signal.SIGHUP, signal.SIGTERM)
        before = {s: signal.getsignal(s) for s in names}
        got = []
        t = threading.Thread(target=lambda: got.append(qr.run_gate_command(f'"{PY}" -c "print(3)"', os.getcwd(), 60)))
        t.start()
        t.join(90)
        self.assertEqual(got, [(0, "3\n", "", False)])
        self.assertEqual({s: signal.getsignal(s) for s in names}, before)


@unittest.skipUnless(os.name == "posix", "a pty and POSIX signals")
class TestARealTerminalStopsTheCommand(_GateCommandChildren):
    """Ctrl-C and a closed terminal reach a program through the terminal DRIVER, not through kill(1): the
    surface this has to be true on. Here the driver is a pty -- the tool is its session leader, ^C is written
    to its master, and closing the master is the hangup."""

    def in_a_terminal(self, act):
        import pty
        import select
        try:
            pid, fd = pty.fork()
        except OSError as e:
            self.skipTest(f"no pty here: {e}")
        if pid == 0:
            try:
                os.execv(PY, [PY, "-c", DRIVER, str(STARTER), self.command(), "60"])
            finally:
                os._exit(127)
        out, status = b"", None
        try:
            self.wait_for_pid()
            fd = act(fd)
            deadline = time.time() + 30
            while status is None and time.time() < deadline:
                done, st = os.waitpid(pid, os.WNOHANG)
                if done:
                    status = st
                if fd is not None and select.select([fd], [], [], 0.05)[0]:
                    try:
                        out += os.read(fd, 65536)
                    except OSError:
                        fd = None
            if status is None:
                os.kill(pid, signal.SIGKILL)
                os.waitpid(pid, 0)
                self.fail("the tool was still running 30 s after the terminal signalled it")
            return status, out.decode(errors="replace")
        finally:
            if fd is not None:
                os.close(fd)

    def test_ctrl_c_typed_at_the_terminal_stops_the_child(self):
        def type_ctrl_c(fd):
            os.write(fd, b"\x03")
            return fd
        status, out = self.in_a_terminal(type_ctrl_c)
        self.assertIn("KeyboardInterrupt", out)
        self.assert_stopped(self.wait_for_pid())

    def test_a_hangup_of_the_terminal_stops_the_child(self):
        def close_the_terminal(fd):
            os.close(fd)
            return None
        status, out = self.in_a_terminal(close_the_terminal)
        self.assertTrue((os.WIFEXITED(status) and os.WEXITSTATUS(status) == 129)
                        or (os.WIFSIGNALED(status) and os.WTERMSIG(status) == signal.SIGHUP), status)
        self.assert_stopped(self.wait_for_pid())


class TestRunStatusAndResultsFile(unittest.TestCase):
    def setUp(self):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        self.d = td.name
        subprocess.run(["git", "init", "-q", self.d], check=True)
        self.cfg = manifest(
            gate("three", "min", 3, command=f'"{PY}" -c "print(3)"', extract=r"(\d+)"),
            gate("exit", "max", 0, command=f'"{PY}" -c "pass"'))
        json.dump(self.cfg, open(os.path.join(self.d, qr.CONFIG_NAME), "w"))

    def test_run_writes_results_and_returns_clean(self):
        rc = qr.do_run(self.d, self.cfg, as_json=True)
        self.assertEqual(rc, qr.CLEAN)
        snap = json.load(open(os.path.join(self.d, qr.DEFAULT_RESULTS)))
        self.assertEqual(snap["summary"], {"pass": 2, "fail": 0, "unmeasured": 0})
        self.assertEqual(len(snap["results"]), 12)
        self.assertEqual(snap["manifest"], qr.sha12(self.cfg["gates"]))

    def test_results_hash_is_stable_across_runs_and_independent_of_time(self):
        qr.do_run(self.d, self.cfg, as_json=True)
        a = json.load(open(os.path.join(self.d, qr.DEFAULT_RESULTS)))
        qr.do_run(self.d, self.cfg, as_json=True)
        b = json.load(open(os.path.join(self.d, qr.DEFAULT_RESULTS)))
        self.assertEqual(a["results"], b["results"])

    def test_summary_line_is_citable(self):
        snap = qr.run_gates(self.d, self.cfg)
        line = qr.summary_line(snap)
        self.assertTrue(line.startswith("quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results "))
        self.assertIn("· manifest ", line)

    def test_status_before_any_run_says_never_run(self):
        import contextlib, io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = qr.do_status(self.d, self.cfg, as_json=True)
        self.assertEqual(rc, qr.WARN)
        self.assertIn("never run here", buf.getvalue())

    def test_status_flags_a_stale_manifest(self):
        qr.do_run(self.d, self.cfg, as_json=True)
        import contextlib, io
        buf = io.StringIO()
        changed = manifest(*self.cfg["gates"], gate("new", "max", 0))
        with contextlib.redirect_stdout(buf):
            rc = qr.do_status(self.d, changed, as_json=True)
        self.assertEqual(rc, qr.WARN)
        self.assertTrue(json.loads(buf.getvalue())["stale"])

    def test_two_gates_over_one_command_run_it_once(self):
        # Two extracts over the same suite (passed count, failed count) must not run it twice:
        # a --run that takes bin/tests.sh twice is a --run nobody cites.
        marker = os.path.join(self.d, "runs.txt")
        cmd = f'"{PY}" -c "open({marker!r}, \'a\').write(\'x\'); print(\'7 passed, 1 failed\')"'
        cfg = manifest(gate("passed", "min", 7, command=cmd, extract=r"(\d+) passed"),
                       gate("failed", "max", 1, command=cmd, extract=r"passed, (\d+) failed"))
        snap = qr.run_gates(self.d, cfg)
        self.assertEqual([r["status"] for r in snap["gates"]], ["pass", "pass"])
        self.assertEqual(open(marker).read(), "x", "the shared command ran more than once")

    def test_a_failing_gate_exits_refused_and_an_unmeasured_one_warns(self):
        failing = manifest(gate("three", "min", 4, command=f'"{PY}" -c "print(3)"', extract=r"(\d+)"))
        self.assertEqual(qr.do_run(self.d, failing, as_json=True), qr.REFUSED)
        unm = manifest(gate("declared", "min", 1))
        self.assertEqual(qr.do_run(self.d, unm, as_json=True), qr.WARN)

    def test_a_run_with_no_timeout_hashes_as_1_3_0_did(self):
        # The `results` hash is what a receipt cites. This pin was computed with the 1.3.0 tool, over
        # one gate of each outcome (pass, pass by exit code, fail, declared-only, extract found nothing):
        # a tool that changes how a gate is measured must leave every run that did not time out equal.
        cfg = manifest(
            gate("three", "min", 3, command=f'"{PY}" -c "print(3)"', extract=r"(\d+)"),
            gate("exit", "max", 0, command=f'"{PY}" -c "pass"'),
            gate("short", "min", 4, command=f'"{PY}" -c "print(3)"', extract=r"(\d+)"),
            gate("declared", "min", 1),
            gate("nodigits", "min", 0, command=f'"{PY}" -c "print(\'none\')"', extract=r"(\d+)"))
        snap = qr.run_gates(self.d, cfg)
        self.assertEqual(snap["summary"], {"pass": 2, "fail": 1, "unmeasured": 2})
        self.assertEqual(snap["results"], "8498441c1165")
        self.assertEqual([r["note"] for r in snap["gates"]],
                         ["", "", "", "declared, no command", "extract matched nothing (exit 0)"])

    def test_a_declared_budget_lets_a_slow_gate_finish_and_an_undeclared_one_time_out(self):
        cfg = manifest(
            gate("declared", "min", 5, command=slow(1.5, "7"), extract=r"(\d+)", timeout_seconds=60),
            gate("undeclared", "min", 5, command=slow(3, "7"), extract=r"(\d+)"))
        snap = qr.run_gates(self.d, cfg, timeout=0.5)
        a, b = snap["gates"]
        self.assertEqual((a["status"], a["measured"], a["note"]), ("pass", 7.0, ""))
        self.assertEqual((b["status"], b["measured"], b["note"]), ("unmeasured", None, "timeout (0.5 s)"))
        self.assertEqual(snap["summary"], {"pass": 1, "fail": 0, "unmeasured": 1})

    def test_a_timed_out_command_shared_by_two_gates_runs_once_and_leaves_both_unmeasured(self):
        marker = os.path.join(self.d, "runs.txt")
        cmd = slow(3, "f'{3+4} passed, {2-1} failed'", marker)
        cfg = manifest(gate("passed", "min", 7, command=cmd, extract=r"(\d+) passed"),
                       gate("failed", "max", 1, command=cmd, extract=r"passed, (\d+) failed"))
        snap = qr.run_gates(self.d, cfg, timeout=0.5)
        self.assertEqual([(r["status"], r["note"]) for r in snap["gates"]],
                         [("unmeasured", "timeout (0.5 s)")] * 2)
        self.assertEqual(open(marker).read(), "x", "the shared command ran more than once")

    def test_gates_sharing_a_command_run_it_once_under_the_largest_declared_budget(self):
        # Neither gate may be cut short by the other's smaller budget: the run is one run.
        marker = os.path.join(self.d, "runs.txt")
        cmd = slow(1.5, "f'{3+4} passed, {2-1} failed'", marker)
        cfg = manifest(gate("passed", "min", 7, command=cmd, extract=r"(\d+) passed", timeout_seconds=0.5),
                       gate("failed", "max", 1, command=cmd, extract=r"passed, (\d+) failed",
                            timeout_seconds=60))
        snap = qr.run_gates(self.d, cfg, timeout=0.5)
        self.assertEqual([r["status"] for r in snap["gates"]], ["pass", "pass"])
        self.assertEqual(open(marker).read(), "x", "the shared command ran more than once")

    def test_a_shared_run_that_times_out_names_the_budget_it_had(self):
        # One run, one budget (the larger): both gates must say the budget the run really had.
        cmd = slow(3, "f'{3+4} passed, {2-1} failed'")
        # The larger budget sits on the FIRST gate: the second reads the run from the memo, and must say
        # the run's budget, not its own smaller one.
        cfg = manifest(gate("passed", "min", 7, command=cmd, extract=r"(\d+) passed", timeout_seconds=0.8),
                       gate("failed", "max", 1, command=cmd, extract=r"passed, (\d+) failed",
                            timeout_seconds=0.5))
        snap = qr.run_gates(self.d, cfg)
        self.assertEqual([r["note"] for r in snap["gates"]], ["timeout (0.8 s)"] * 2)

    def test_an_undeclared_gate_keeps_the_default_beside_a_shorter_declared_one(self):
        # The default is the undeclared gate's budget, so the shared run is not cut at its sibling's
        # smaller declared one: the largest budget any of them HAS wins, declared or not.
        cmd = slow(1.5, "f'{3+4} passed, {2-1} failed'")
        cfg = manifest(gate("passed", "min", 7, command=cmd, extract=r"(\d+) passed", timeout_seconds=0.5),
                       gate("failed", "max", 1, command=cmd, extract=r"passed, (\d+) failed"))
        snap = qr.run_gates(self.d, cfg, timeout=60)
        self.assertEqual([r["status"] for r in snap["gates"]], ["pass", "pass"])

    def test_a_timed_out_run_exits_warn_through_the_cli_and_says_why(self):
        json.dump(manifest(gate("slow", "max", 0, command=slow(3), timeout_seconds=0.5)),
                  open(os.path.join(self.d, qr.CONFIG_NAME), "w"))
        p = subprocess.run([PY, str(STARTER), "--run"], cwd=self.d, capture_output=True, text=True)
        self.assertEqual(p.returncode, qr.WARN, p.stdout + p.stderr)
        self.assertIn("timeout (0.5 s)", p.stdout)
        self.assertIn("0/1 pass · 0 fail · 1 unmeasured", p.stdout)
        snap = json.load(open(os.path.join(self.d, qr.DEFAULT_RESULTS)))
        self.assertEqual((snap["gates"][0]["status"], snap["gates"][0]["measured"]), ("unmeasured", None))


class TestPrecommitThroughGit(unittest.TestCase):
    """The ratchet as git sees it: the INDEX vs HEAD, never the worktree."""

    def setUp(self):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        self.d = td.name
        for argv in (["git", "init", "-q", self.d],
                     ["git", "-C", self.d, "config", "user.email", "t@t"],
                     ["git", "-C", self.d, "config", "user.name", "t"]):
            subprocess.run(argv, check=True)
        self.base = manifest(gate("cov", "min", 80))
        self._write(self.base)
        subprocess.run(["git", "-C", self.d, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.d, "commit", "-q", "-m", "base"], check=True)

    def _write(self, cfg):
        json.dump(cfg, open(os.path.join(self.d, qr.CONFIG_NAME), "w"))

    def _stage(self, cfg):
        self._write(cfg)
        subprocess.run(["git", "-C", self.d, "add", qr.CONFIG_NAME], check=True)

    def _precommit(self):
        import contextlib, io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = qr.precommit(self.d)
        return rc, buf.getvalue()

    def test_manifest_not_in_the_commit_passes(self):
        self.assertEqual(self._precommit()[0], qr.CLEAN)

    def test_staged_loosening_is_refused(self):
        self._stage(manifest(gate("cov", "min", 70)))
        rc, out = self._precommit()
        self.assertEqual(rc, qr.REFUSED)
        self.assertIn("REFUSED", out)
        self.assertIn("--no-verify", out)  # the cost of bypass is printed, never hidden

    def test_staged_tightening_passes(self):
        self._stage(manifest(gate("cov", "min", 90)))
        self.assertEqual(self._precommit()[0], qr.CLEAN)

    def test_no_base_note_when_head_holds_the_base(self):
        # An unrelated commit after the manifest's last change: HEAD still holds the base, and
        # `git log -- manifest` naming an older commit is not "HEAD has none".
        open(os.path.join(self.d, "unrelated.txt"), "w").write("x\n")
        subprocess.run(["git", "-C", self.d, "add", "unrelated.txt"], check=True)
        subprocess.run(["git", "-C", self.d, "commit", "-q", "-m", "unrelated"], check=True)
        self._stage(manifest(gate("cov", "min", 90)))
        rc, out = self._precommit()
        self.assertEqual(rc, qr.CLEAN)
        self.assertNotIn("comparing against", out)

    def test_the_index_not_the_worktree_is_what_is_ratcheted(self):
        # Stage a tightening, then loosen only the worktree copy: the commit is the index.
        self._stage(manifest(gate("cov", "min", 90)))
        self._write(manifest(gate("cov", "min", 10)))
        self.assertEqual(self._precommit()[0], qr.CLEAN)
        # And the mirror: stage a loosening, then "fix" only the worktree — still refused.
        self._stage(manifest(gate("cov", "min", 10)))
        self._write(manifest(gate("cov", "min", 90)))
        self.assertEqual(self._precommit()[0], qr.REFUSED)

    def test_a_staged_manifest_with_defects_is_refused(self):
        self._stage(manifest(gate("cov", "sideways", 80)))
        rc, out = self._precommit()
        self.assertEqual(rc, qr.REFUSED)
        self.assertIn("config defect", out)

    def test_first_manifest_commit_has_nothing_to_compare(self):
        # "First" means never committed on this branch's history -- not "absent at HEAD".
        fresh = tempfile.TemporaryDirectory(); self.addCleanup(fresh.cleanup)
        for argv in (["git", "init", "-q", fresh.name],
                     ["git", "-C", fresh.name, "config", "user.email", "t@t"],
                     ["git", "-C", fresh.name, "config", "user.name", "t"]):
            subprocess.run(argv, check=True)
        open(os.path.join(fresh.name, "README"), "w").write("x\n")
        subprocess.run(["git", "-C", fresh.name, "add", "-A"], check=True)
        subprocess.run(["git", "-C", fresh.name, "commit", "-q", "-m", "base"], check=True)
        json.dump(manifest(gate("cov", "min", 1)), open(os.path.join(fresh.name, qr.CONFIG_NAME), "w"))
        subprocess.run(["git", "-C", fresh.name, "add", qr.CONFIG_NAME], check=True)
        import contextlib, io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = qr.precommit(fresh.name)
        self.assertEqual(rc, qr.CLEAN)
        self.assertIn("first manifest commit", buf.getvalue())

    # --- the deletion hole (PR #82 review, section 2a): a comparison needs two sides ---

    def _commit_removal(self):
        """Commit the manifest's removal as `--no-verify` would: index has none, HEAD keeps history."""
        subprocess.run(["git", "-C", self.d, "rm", "-q", "--cached", qr.CONFIG_NAME], check=True)
        subprocess.run(["git", "-C", self.d, "commit", "-q", "-m", "drop"], check=True)

    def test_removing_the_manifest_is_refused_as_the_loosest_loosening(self):
        subprocess.run(["git", "-C", self.d, "rm", "-q", "--cached", qr.CONFIG_NAME], check=True)
        rc, out = self._precommit()
        self.assertEqual(rc, qr.REFUSED)
        self.assertIn("manifest removed", out)
        self.assertIn("--no-verify", out)

    def test_readding_lower_after_a_committed_removal_is_refused(self):
        self._commit_removal()
        self._stage(manifest(gate("cov", "min", 1)))
        rc, out = self._precommit()
        self.assertEqual(rc, qr.REFUSED)       # 80 -> 1 via delete + re-add is still 80 -> 1
        self.assertIn("floor lowered", out)
        self._stage(manifest(gate("cov", "min", 80)))
        self.assertEqual(self._precommit()[0], qr.CLEAN)

    def test_an_already_removed_manifest_does_not_lock_the_repo(self):
        self._commit_removal()
        open(os.path.join(self.d, "unrelated.txt"), "w").write("x\n")
        subprocess.run(["git", "-C", self.d, "add", "unrelated.txt"], check=True)
        self.assertEqual(self._precommit()[0], qr.CLEAN)

    def test_an_unparseable_head_copy_is_skipped_for_the_newest_parseable(self):
        open(os.path.join(self.d, qr.CONFIG_NAME), "w").write("not json")
        subprocess.run(["git", "-C", self.d, "add", qr.CONFIG_NAME], check=True)
        subprocess.run(["git", "-C", self.d, "commit", "-q", "-m", "corrupt"], check=True)
        self._stage(manifest(gate("cov", "min", 70)))
        rc, out = self._precommit()
        self.assertEqual(rc, qr.REFUSED)       # compared against the 80 two commits back
        self.assertIn("floor lowered", out)
        self._stage(manifest(gate("cov", "min", 80)))
        self.assertEqual(self._precommit()[0], qr.CLEAN)

    def test_an_emptied_manifest_is_not_a_comparison_base(self):
        # Emptying the gate list is refused like a removal; bypassed, it must not become the
        # base that lets a later re-declaration land lower than what was declared before.
        self._stage(manifest())
        rc, out = self._precommit()
        self.assertEqual(rc, qr.REFUSED)
        subprocess.run(["git", "-C", self.d, "commit", "-q", "--no-verify", "-m", "empty anyway"], check=True)
        self._stage(manifest(gate("cov", "min", 1)))
        rc, out = self._precommit()
        self.assertEqual(rc, qr.REFUSED)       # 80 -> 1, with an empty manifest in between
        self.assertIn("floor lowered", out)

    def test_a_synced_empty_seed_is_not_a_comparison_base_either(self):
        # The seed adopters receive is empty; the first real declaration is a first commit.
        fresh = tempfile.TemporaryDirectory(); self.addCleanup(fresh.cleanup)
        for argv in (["git", "init", "-q", fresh.name],
                     ["git", "-C", fresh.name, "config", "user.email", "t@t"],
                     ["git", "-C", fresh.name, "config", "user.name", "t"]):
            subprocess.run(argv, check=True)
        json.dump(manifest(), open(os.path.join(fresh.name, qr.CONFIG_NAME), "w"))
        subprocess.run(["git", "-C", fresh.name, "add", "-A"], check=True)
        subprocess.run(["git", "-C", fresh.name, "commit", "-q", "-m", "seed"], check=True)
        json.dump(manifest(gate("cov", "min", 50)), open(os.path.join(fresh.name, qr.CONFIG_NAME), "w"))
        subprocess.run(["git", "-C", fresh.name, "add", qr.CONFIG_NAME], check=True)
        import contextlib, io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = qr.precommit(fresh.name)
        self.assertEqual(rc, qr.CLEAN)
        self.assertIn("first manifest commit", buf.getvalue())

    def test_precommit_cli_survives_a_manifest_missing_from_the_worktree(self):
        # Through the CLI: an ordinary `git rm` empties the worktree copy too. The tool must
        # still find the repo (git toplevel) and judge the removal, not exit 3 "refuses to invent".
        subprocess.run(["git", "-C", self.d, "rm", "-q", qr.CONFIG_NAME], check=True)
        p = subprocess.run([PY, str(STARTER), "--precommit"], cwd=self.d, capture_output=True, text=True)
        self.assertEqual(p.returncode, qr.REFUSED, p.stdout + p.stderr)
        self.assertIn("manifest removed", p.stdout)


class TestFindRootAndHookPath(unittest.TestCase):
    def setUp(self):
        td = tempfile.TemporaryDirectory(); self.addCleanup(td.cleanup)
        self.d = td.name
        for argv in (["git", "init", "-q", self.d],
                     ["git", "-C", self.d, "config", "user.email", "t@t"],
                     ["git", "-C", self.d, "config", "user.name", "t"]):
            subprocess.run(argv, check=True)

    def test_find_root_is_the_git_toplevel_even_without_a_manifest(self):
        sub = os.path.join(self.d, "a", "b"); os.makedirs(sub)
        self.assertEqual(os.path.realpath(qr.find_root(sub)), os.path.realpath(self.d))

    def test_find_root_walks_up_to_a_manifest_outside_git(self):
        td = tempfile.TemporaryDirectory(); self.addCleanup(td.cleanup)
        json.dump(manifest(), open(os.path.join(td.name, qr.CONFIG_NAME), "w"))
        sub = os.path.join(td.name, "x"); os.makedirs(sub)
        self.assertEqual(os.path.realpath(qr.find_root(sub)), os.path.realpath(td.name))

    def test_install_hook_writes_the_path_of_the_file_that_is_running(self):
        # The canonical repo keeps the tool under starter-kit/; an adopter at the root. The hook
        # must exec whichever copy installed it, or every commit fails "can't open file".
        tools = os.path.join(self.d, "tools"); os.makedirs(tools)
        import shutil; shutil.copy(STARTER, os.path.join(tools, "quality_ratchet.py"))
        json.dump(manifest(gate("g", "min", 1, command="true")), open(os.path.join(self.d, qr.CONFIG_NAME), "w"))
        subprocess.run(["git", "-C", self.d, "add", "-A"], check=True)
        subprocess.run(["git", "-C", self.d, "commit", "-q", "-m", "base"], check=True)
        p = subprocess.run([PY, os.path.join(tools, "quality_ratchet.py"), "install-hook"],
                           cwd=self.d, capture_output=True, text=True)
        self.assertEqual(p.returncode, qr.CLEAN, p.stdout + p.stderr)
        hook = open(os.path.join(self.d, ".git", "hooks", "pre-commit")).read()
        self.assertIn("tools/quality_ratchet.py", hook)
        open(os.path.join(self.d, "unrelated.txt"), "w").write("x\n")
        subprocess.run(["git", "-C", self.d, "add", "unrelated.txt"], check=True)
        p = subprocess.run(["git", "-C", self.d, "commit", "-q", "-m", "after install"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)


def _git(d, *args, check=True):
    return subprocess.run(["git", "-C", d, *args], check=check, capture_output=True, text=True)


def _put(d, rel, text="x\n"):
    p = os.path.join(d, *rel.split("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(text if isinstance(text, str) else json.dumps(text))
    return p


NEW_CONFIG = "methodology/" + qr.CONFIG_NAME   # layout: the new layout's path of the manifest
LEGACY_CONFIG = qr.CONFIG_NAME


class TestTheManifestMayLiveInEitherLayout(unittest.TestCase):
    """BL-101 P2 (plan section 4.3): a project keeps its manifest at its root (legacy) or under
    methodology/ (new). The ratchet reads the four-row table with the manifest as the anchor."""

    def setUp(self):
        td = tempfile.TemporaryDirectory(); self.addCleanup(td.cleanup)
        self.d = os.path.realpath(td.name)

    def _cli(self, *args, cwd=None):
        return subprocess.run([PY, str(STARTER), *args], cwd=cwd or self.d, capture_output=True, text=True)

    def test_manifest_location_reads_the_four_rows(self):
        self.assertEqual(qr.manifest_location(self.d), ("none", None))
        _put(self.d, LEGACY_CONFIG, manifest())
        self.assertEqual(qr.manifest_location(self.d), ("legacy", LEGACY_CONFIG))
        os.remove(os.path.join(self.d, LEGACY_CONFIG))
        _put(self.d, NEW_CONFIG, manifest())
        self.assertEqual(qr.manifest_location(self.d), ("new", NEW_CONFIG))
        _put(self.d, LEGACY_CONFIG, manifest())
        self.assertEqual(qr.manifest_location(self.d), ("half", None))

    def test_find_root_finds_a_manifest_that_lives_under_methodology(self):
        _put(self.d, NEW_CONFIG, manifest())
        sub = os.path.join(self.d, "src", "deep"); os.makedirs(sub)
        self.assertEqual(os.path.realpath(qr.find_root(self.d)), self.d)
        self.assertEqual(os.path.realpath(qr.find_root(sub)), self.d)

    def test_find_root_from_inside_methodology_is_the_project_not_that_directory(self):
        _git(self.d, "init", "-q")
        _put(self.d, NEW_CONFIG, manifest())
        self.assertEqual(os.path.realpath(qr.find_root(os.path.join(self.d, "methodology"))), self.d)

    def test_a_repository_that_is_itself_named_methodology_keeps_its_own_root(self):
        # This very repository is a directory called methodology/ whose manifest sits at its root.
        # Reading "a manifest in a directory named methodology" as the new layout would move its
        # root one level up, to a directory that is not a project.
        repo = os.path.join(self.d, "methodology")
        os.makedirs(repo); _git(repo, "init", "-q")
        _put(repo, LEGACY_CONFIG, manifest())
        sub = os.path.join(repo, "tools"); os.makedirs(sub)
        self.assertEqual(os.path.realpath(qr.find_root(repo)), os.path.realpath(repo))
        self.assertEqual(os.path.realpath(qr.find_root(sub)), os.path.realpath(repo))

    def test_run_in_the_new_layout_writes_its_results_beside_the_manifest(self):
        _put(self.d, NEW_CONFIG, manifest(gate("marker", "max", 0, command=f'"{PY}" -c "import os,sys; sys.exit(0 if os.path.exists(\'marker.txt\') else 1)"')))
        _put(self.d, "marker.txt")
        p = self._cli("--run")
        self.assertEqual(p.returncode, qr.CLEAN, p.stdout + p.stderr)
        self.assertTrue(os.path.exists(os.path.join(self.d, "methodology", qr.DEFAULT_RESULTS)))
        self.assertFalse(os.path.exists(os.path.join(self.d, qr.DEFAULT_RESULTS)), "no results file at the root")
        # the gate's command ran from the project root, not from methodology/
        self.assertIn("1/1 pass", p.stdout)
        s = self._cli("--status")
        self.assertEqual(s.returncode, qr.CLEAN, s.stdout + s.stderr)
        self.assertIn("1/1 pass", s.stdout)

    def test_run_in_the_legacy_layout_still_writes_its_results_at_the_root(self):
        _put(self.d, LEGACY_CONFIG, manifest(gate("ok", "max", 0, command=f'"{PY}" -c "pass"')))
        self.assertEqual(self._cli("--run").returncode, qr.CLEAN)
        self.assertTrue(os.path.exists(os.path.join(self.d, qr.DEFAULT_RESULTS)))
        self.assertFalse(os.path.exists(os.path.join(self.d, "methodology")))

    def test_an_explicit_results_file_is_relative_to_the_root_in_either_layout(self):
        cfg = manifest(gate("ok", "max", 0, command=f'"{PY}" -c "pass"')); cfg["results_file"] = "out/r.json"
        _put(self.d, NEW_CONFIG, cfg)
        os.makedirs(os.path.join(self.d, "out"))   # the tool writes the file, it does not make the directory
        self.assertEqual(self._cli("--run").returncode, qr.CLEAN)
        self.assertTrue(os.path.exists(os.path.join(self.d, "out", "r.json")))

    def test_a_half_migrated_tree_is_a_usage_error_that_names_both_and_runs_nothing(self):
        _put(self.d, LEGACY_CONFIG, manifest(gate("ok", "max", 0, command=f'"{PY}" -c "pass"')))
        _put(self.d, NEW_CONFIG, manifest(gate("ok", "max", 0, command=f'"{PY}" -c "pass"')))
        for args in (["--run"], ["--status"], ["install-hook"]):
            p = self._cli(*args)
            self.assertEqual(p.returncode, qr.USAGE, (args, p.stdout + p.stderr))
            self.assertIn(LEGACY_CONFIG, p.stdout); self.assertIn(NEW_CONFIG, p.stdout)
        self.assertFalse(os.path.exists(os.path.join(self.d, qr.DEFAULT_RESULTS)))
        self.assertFalse(os.path.exists(os.path.join(self.d, "methodology", qr.DEFAULT_RESULTS)))

    def test_manifest_location_decides_a_tie_by_the_framework_anchor(self):
        # S276's picker (plan 7.2b): a project whose runner is under methodology/ keeps its manifest
        # there, and a manifest at the root is the project's own, which the ratchet does not read.
        _put(self.d, LEGACY_CONFIG, manifest()); _put(self.d, NEW_CONFIG, manifest())
        self.assertEqual(qr.manifest_location(self.d), ("half", None))        # no runner: still refused
        _put(self.d, "methodology/SESSION_RUNNER.md", "runner\n")
        self.assertEqual(qr.manifest_location(self.d), ("new", NEW_CONFIG))
        _put(self.d, "SESSION_RUNNER.md", "runner\n")
        self.assertEqual(qr.manifest_location(self.d), ("half", None))        # a runner in both places decides nothing

    def test_a_tie_the_anchor_decides_runs_the_methodology_manifest_and_leaves_the_root_one_alone(self):
        _put(self.d, LEGACY_CONFIG, manifest(gate("users-own", "max", 0, command=f'"{PY}" -c "raise SystemExit(1)"')))
        _put(self.d, NEW_CONFIG, manifest(gate("ok", "max", 0, command=f'"{PY}" -c "pass"')))
        _put(self.d, "methodology/SESSION_RUNNER.md", "runner\n")
        p = self._cli("--run")
        self.assertEqual(p.returncode, qr.CLEAN, p.stdout + p.stderr)
        self.assertNotIn("users-own", p.stdout)
        self.assertTrue(os.path.exists(os.path.join(self.d, "methodology", qr.DEFAULT_RESULTS)))
        self.assertFalse(os.path.exists(os.path.join(self.d, qr.DEFAULT_RESULTS)), "nothing is written beside the user's file")


class _Repo(unittest.TestCase):
    """A throwaway repository holding a legacy manifest (cov >= 80) at its root, committed."""

    def setUp(self):
        td = tempfile.TemporaryDirectory(); self.addCleanup(td.cleanup)
        self.d = os.path.realpath(td.name)
        _git(self.d, "init", "-q")
        _git(self.d, "config", "user.email", "t@t")
        _git(self.d, "config", "user.name", "t")
        _put(self.d, LEGACY_CONFIG, manifest(gate("cov", "min", 80)))
        _git(self.d, "add", "-A"); _git(self.d, "commit", "-q", "-m", "base")

    def _commit(self, msg="c"):
        _git(self.d, "add", "-A"); _git(self.d, "commit", "-q", "--no-verify", "-m", msg)

    def _move(self, cfg=None):
        """git mv the manifest under methodology/, optionally rewriting it, all staged."""
        os.makedirs(os.path.join(self.d, "methodology"), exist_ok=True)
        _git(self.d, "mv", LEGACY_CONFIG, NEW_CONFIG)
        if cfg is not None:
            _put(self.d, NEW_CONFIG, cfg)
            _git(self.d, "add", NEW_CONFIG)

    def _precommit(self):
        import contextlib, io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = qr.precommit(self.d)
        return rc, buf.getvalue()


class TestPrecommitAcrossTheMove(_Repo):
    """BL-101 P2, plan C4. A move that reads as 'manifest removed' is refused for the wrong reason,
    a base search that stops at the move cannot see a loosening made inside it, and a manifest at
    the new path that nothing looks for is a ratchet that fails OPEN."""

    def test_a_pure_move_of_the_manifest_passes(self):
        self._move()
        rc, out = self._precommit()
        self.assertEqual(rc, qr.CLEAN, out)

    def test_a_move_that_lowers_a_floor_is_refused_and_names_the_change(self):
        self._move(manifest(gate("cov", "min", 70)))
        rc, out = self._precommit()
        self.assertEqual(rc, qr.REFUSED, out)
        self.assertIn("floor lowered 80 -> 70", out)

    def test_a_move_that_tightens_passes(self):
        self._move(manifest(gate("cov", "min", 90)))
        self.assertEqual(self._precommit()[0], qr.CLEAN)

    def test_a_move_that_adds_a_gate_passes(self):
        self._move(manifest(gate("cov", "min", 80), gate("new", "max", 0)))
        self.assertEqual(self._precommit()[0], qr.CLEAN)

    def test_a_move_that_drops_a_gate_is_refused(self):
        self._move(manifest(gate("other", "min", 1)))
        rc, out = self._precommit()
        self.assertEqual(rc, qr.REFUSED, out)
        self.assertIn("gate 'cov' removed", out)   # the gate, not 'manifest removed': the file moved

    def test_a_loosening_at_the_new_path_after_the_move_commit_is_refused(self):
        # The fail-open C4 measured: once the manifest is under methodology/ a ratchet that looks
        # only at the root finds nothing staged and nothing at HEAD, and passes every loosening.
        self._move(); self._commit("move")
        _put(self.d, NEW_CONFIG, manifest(gate("cov", "min", 70))); _git(self.d, "add", NEW_CONFIG)
        rc, out = self._precommit()
        self.assertEqual(rc, qr.REFUSED, out)
        self.assertIn("floor lowered 80 -> 70", out)

    def test_a_tightening_at_the_new_path_after_the_move_commit_passes(self):
        self._move(); self._commit("move")
        _put(self.d, NEW_CONFIG, manifest(gate("cov", "min", 95))); _git(self.d, "add", NEW_CONFIG)
        self.assertEqual(self._precommit()[0], qr.CLEAN)

    def test_the_base_is_found_across_the_move_when_the_head_copy_is_unusable(self):
        # The history walk must not stop at the move: A declared 90 at the root, the move commit
        # (bypassed) emptied the gates at the new path, and re-adding 80 is a loosening against A.
        _put(self.d, LEGACY_CONFIG, manifest(gate("cov", "min", 90))); self._commit("tighten to 90")
        self._move(manifest()); self._commit("move and empty")
        _put(self.d, NEW_CONFIG, manifest(gate("cov", "min", 80))); _git(self.d, "add", NEW_CONFIG)
        rc, out = self._precommit()
        self.assertEqual(rc, qr.REFUSED, out)
        self.assertIn("floor lowered 90 -> 80", out)
        self.assertIn("comparing against", out)   # the base came from further back than HEAD, and says so

    def test_the_base_is_the_newest_declaration_at_either_path(self):
        # After the move the history of the OLD path ends at the move. A walk that names only that
        # path never sees the tightening made later at the new one, so a loosening back to a value
        # between the two would pass.
        self._move(); self._commit("move")
        _put(self.d, NEW_CONFIG, manifest(gate("cov", "min", 95))); self._commit("tighten at the new path")
        _put(self.d, NEW_CONFIG, manifest()); self._commit("empty it (bypassed)")
        _put(self.d, NEW_CONFIG, manifest(gate("cov", "min", 92))); _git(self.d, "add", NEW_CONFIG)
        rc, out = self._precommit()
        self.assertEqual(rc, qr.REFUSED, out)
        self.assertIn("floor lowered 95 -> 92", out)

    def test_a_commit_that_held_both_layouts_is_neither_a_base_nor_a_head_copy(self):
        # A bypassed commit left the manifest in both places, the legacy copy lower than the truth.
        # Reading either copy as "the" manifest would hand the ratchet a weaker base; the commit is
        # skipped like an unparseable one, and HEAD's copy is not trusted either (the note says so).
        _put(self.d, LEGACY_CONFIG, manifest(gate("cov", "min", 60)))
        _put(self.d, NEW_CONFIG, manifest(gate("cov", "min", 70))); self._commit("both, bypassed")
        _git(self.d, "rm", "-q", LEGACY_CONFIG)
        rc, out = self._precommit()
        self.assertEqual(rc, qr.REFUSED, out)
        self.assertIn("floor lowered 80 -> 70", out)   # the base is the last unambiguous declaration
        self.assertIn("comparing against", out)

    def test_removing_the_manifest_at_the_new_path_is_refused(self):
        self._move(); self._commit("move")
        _git(self.d, "rm", "-q", NEW_CONFIG)
        rc, out = self._precommit()
        self.assertEqual(rc, qr.REFUSED, out)
        self.assertIn("manifest removed", out)

    def test_both_locations_in_the_index_is_half_migrated_and_refused_naming_both(self):
        _put(self.d, NEW_CONFIG, manifest(gate("cov", "min", 80))); _git(self.d, "add", NEW_CONFIG)
        rc, out = self._precommit()
        self.assertEqual(rc, qr.REFUSED, out)
        self.assertIn("half-migrated", out)
        self.assertIn(LEGACY_CONFIG, out); self.assertIn(NEW_CONFIG, out)

    def _tie(self, root_floor=10, new_floor=80, runner="methodology"):
        """Commit a manifest at BOTH paths (the root one is lower: it is somebody else's) and a runner
        tracked under methodology/, at the root, at both, or nowhere."""
        _put(self.d, LEGACY_CONFIG, manifest(gate("cov", "min", root_floor)))
        _put(self.d, NEW_CONFIG, manifest(gate("cov", "min", new_floor)))
        if runner in ("methodology", "both"):
            _put(self.d, "methodology/SESSION_RUNNER.md", "runner\n")
        if runner in ("root", "both"):
            _put(self.d, "SESSION_RUNNER.md", "runner\n")
        self._commit("a manifest in both places")

    def test_a_tie_the_runner_decides_judges_the_methodology_manifest_and_not_the_root_one(self):
        # S276's picker: the ratchet works inside methodology/. A loosening there is refused for the
        # loosening (not as "half-migrated"); a change to the root file, which is the user's, is not judged.
        self._tie()
        _put(self.d, NEW_CONFIG, manifest(gate("cov", "min", 70))); _git(self.d, "add", NEW_CONFIG)
        rc, out = self._precommit()
        self.assertEqual(rc, qr.REFUSED, out)
        self.assertIn("floor lowered 80 -> 70", out)
        self.assertNotIn("half-migrated", out)
        _git(self.d, "reset", "-q", "--", NEW_CONFIG); _put(self.d, NEW_CONFIG, manifest(gate("cov", "min", 80)))
        _put(self.d, LEGACY_CONFIG, manifest(gate("cov", "min", 1))); _git(self.d, "add", LEGACY_CONFIG)
        rc, out = self._precommit()
        self.assertEqual(rc, qr.CLEAN, out)

    def test_a_tie_the_runner_decides_takes_its_base_from_the_methodology_copy(self):
        self._tie(root_floor=95, new_floor=90)
        _put(self.d, NEW_CONFIG, manifest(gate("cov", "min", 85))); _git(self.d, "add", NEW_CONFIG)
        rc, out = self._precommit()
        self.assertEqual(rc, qr.REFUSED, out)
        self.assertIn("floor lowered 90 -> 85", out)   # not against the root file's 95

    def test_a_tie_the_runner_cannot_decide_is_still_refused_naming_both(self):
        for runner in ("root", "both", None):
            with self.subTest(runner=runner):
                self.setUp()
                self._tie(runner=runner)
                _put(self.d, NEW_CONFIG, manifest(gate("cov", "min", 85))); _git(self.d, "add", NEW_CONFIG)
                rc, out = self._precommit()
                self.assertEqual(rc, qr.REFUSED, out)
                self.assertIn("half-migrated", out)
                self.assertIn(LEGACY_CONFIG, out); self.assertIn(NEW_CONFIG, out)

    def test_a_runner_that_is_on_disk_but_not_tracked_decides_nothing(self):
        # The hook reads the INDEX; so does this. A runner in the worktree that was never added is not an anchor.
        self._tie(runner=None)
        _put(self.d, "methodology/SESSION_RUNNER.md", "runner\n")
        _put(self.d, NEW_CONFIG, manifest(gate("cov", "min", 85))); _git(self.d, "add", NEW_CONFIG)
        rc, out = self._precommit()
        self.assertEqual(rc, qr.REFUSED, out)
        self.assertIn("half-migrated", out)

    def test_a_manifest_first_committed_under_methodology_has_nothing_to_compare(self):
        td = tempfile.TemporaryDirectory(); self.addCleanup(td.cleanup)
        d = os.path.realpath(td.name)
        _git(d, "init", "-q"); _git(d, "config", "user.email", "t@t"); _git(d, "config", "user.name", "t")
        _put(d, NEW_CONFIG, manifest(gate("cov", "min", 80))); _git(d, "add", "-A")
        import contextlib, io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = qr.precommit(d)
        self.assertEqual(rc, qr.CLEAN)
        self.assertIn("first manifest commit", buf.getvalue())

    def test_a_defective_manifest_at_the_new_path_is_refused(self):
        self._move(); self._commit("move")
        _put(self.d, NEW_CONFIG, '{"gates": "nope"}'); _git(self.d, "add", NEW_CONFIG)
        self.assertEqual(self._precommit()[0], qr.REFUSED)

    def test_the_cli_judges_a_move_from_a_subdirectory_by_the_index(self):
        self._move(manifest(gate("cov", "min", 70)))
        sub = os.path.join(self.d, "src"); os.makedirs(sub)
        p = subprocess.run([PY, str(STARTER), "--precommit"], cwd=sub, capture_output=True, text=True)
        self.assertEqual(p.returncode, qr.REFUSED, p.stdout + p.stderr)
        self.assertIn("floor lowered 80 -> 70", p.stdout)


class TestTheInstalledHookAcrossTheMove(_Repo):
    """The hook install-hook writes execs the tool by path. After a move that path is wrong, which
    refuses every commit loudly (C4); the hook now also looks for the tool in the other layout."""

    def _install(self, tool_rel):
        import shutil
        dst = os.path.join(self.d, *tool_rel.split("/"))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(STARTER, dst)
        _git(self.d, "add", "-A"); _git(self.d, "commit", "-q", "--no-verify", "-m", "add the tool")
        p = subprocess.run([PY, dst, "install-hook"], cwd=self.d, capture_output=True, text=True)
        self.assertEqual(p.returncode, qr.CLEAN, p.stdout + p.stderr)
        return open(os.path.join(self.d, ".git", "hooks", "pre-commit")).read()

    def _commit_hooked(self, msg="c"):
        _git(self.d, "add", "-A")
        return subprocess.run(["git", "-C", self.d, "commit", "-q", "-m", msg], capture_output=True, text=True)

    def test_install_from_the_new_layout_names_that_copy_and_its_twin(self):
        self._move(); self._commit("move the manifest")
        hook = self._install("methodology/quality_ratchet.py")
        self.assertIn("methodology/quality_ratchet.py", hook)
        self.assertIn('"quality_ratchet.py"', hook, "the twin in the other layout")

    def test_a_canonical_style_path_has_no_twin(self):
        loop = [l for l in qr.hook_text("starter-kit/quality_ratchet.py").splitlines() if l.startswith("for t in ")]
        self.assertEqual(loop, ['for t in "starter-kit/quality_ratchet.py"; do'])

    def test_each_layout_names_the_other_as_its_twin(self):
        self.assertEqual(qr.layout_twin("quality_ratchet.py"), "methodology/quality_ratchet.py")
        self.assertEqual(qr.layout_twin("methodology/quality_ratchet.py"), "quality_ratchet.py")
        self.assertIsNone(qr.layout_twin("starter-kit/quality_ratchet.py"))
        self.assertIsNone(qr.layout_twin("tools/methodology/quality_ratchet.py"))

    def test_the_hook_from_the_new_layout_refuses_a_loosening_and_passes_a_tightening(self):
        self._move(); self._commit("move the manifest")
        self._install("methodology/quality_ratchet.py")
        _put(self.d, NEW_CONFIG, manifest(gate("cov", "min", 70)))
        p = self._commit_hooked("loosen")
        self.assertNotEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("floor lowered 80 -> 70", p.stdout + p.stderr)
        _put(self.d, NEW_CONFIG, manifest(gate("cov", "min", 85)))
        self.assertEqual(self._commit_hooked("tighten").returncode, 0)

    def test_the_hook_finds_the_tool_after_it_moves_to_the_other_layout(self):
        self._install("quality_ratchet.py")
        os.makedirs(os.path.join(self.d, "methodology"))
        _git(self.d, "mv", LEGACY_CONFIG, NEW_CONFIG)
        _git(self.d, "mv", "quality_ratchet.py", "methodology/quality_ratchet.py")
        p = self._commit_hooked("the pure move")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_a_move_that_loosens_is_refused_end_to_end_by_the_moved_tool(self):
        self._install("quality_ratchet.py")
        os.makedirs(os.path.join(self.d, "methodology"))
        _git(self.d, "mv", LEGACY_CONFIG, NEW_CONFIG)
        _git(self.d, "mv", "quality_ratchet.py", "methodology/quality_ratchet.py")
        _put(self.d, NEW_CONFIG, manifest(gate("cov", "min", 70)))
        p = self._commit_hooked("the move that loosens")
        self.assertNotEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("floor lowered 80 -> 70", p.stdout + p.stderr)

    def test_a_hook_whose_tool_is_nowhere_fails_loudly_and_says_what_to_do(self):
        self._install("quality_ratchet.py")
        os.remove(os.path.join(self.d, "quality_ratchet.py"))
        _put(self.d, "unrelated.txt")
        p = self._commit_hooked("no tool")
        self.assertNotEqual(p.returncode, 0, "a missing tool must refuse, never pass silently")
        self.assertIn("not found", p.stdout + p.stderr)
        self.assertIn("install-hook", p.stdout + p.stderr)


class TestTheHookFromASymlinkedPath(_Repo):
    """git names the toplevel by its real path, so a tool reached through a symlinked directory (macOS's
    /var -> /private/var is the everyday one) must be resolved before its place is written into the hook.
    These tests make their own symlink, so they hold wherever the temp directory is. Where the platform
    will not create one they skip and say so: the property is then unchecked there, not passed."""

    LOOP = 'for t in "quality_ratchet.py" "methodology/quality_ratchet.py"; do'

    def _symlink(self, target, link, **kw):
        try:
            os.symlink(target, link, **kw)
        except (OSError, NotImplementedError) as e:
            self.skipTest(f"this platform will not create a symlink here ({e}): the symlinked-path property is unchecked")

    def _tracked_tool(self):
        import shutil
        shutil.copy(STARTER, os.path.join(self.d, "quality_ratchet.py"))
        _git(self.d, "add", "-A"); _git(self.d, "commit", "-q", "--no-verify", "-m", "add the tool")

    def _linked_repo(self):
        td = tempfile.TemporaryDirectory(); self.addCleanup(td.cleanup)
        link = os.path.join(os.path.realpath(td.name), "via-link")
        self._symlink(self.d, link, target_is_directory=True)
        return link

    def _install_via(self, tool_path):
        p = subprocess.run([PY, tool_path, "install-hook"], cwd=self.d, capture_output=True, text=True)
        self.assertEqual(p.returncode, qr.CLEAN, p.stdout + p.stderr)
        hook = open(os.path.join(self.d, ".git", "hooks", "pre-commit")).read()
        return [l for l in hook.splitlines() if l.startswith("for t in ")]

    def test_a_tool_reached_through_a_symlinked_directory_is_named_by_its_place_in_the_repository(self):
        self._tracked_tool()
        link = self._linked_repo()
        self.assertEqual(self._install_via(os.path.join(link, "quality_ratchet.py")), [self.LOOP])

    def test_that_hook_still_finds_the_tool_after_the_layout_move(self):
        self._tracked_tool()
        link = self._linked_repo()
        self._install_via(os.path.join(link, "quality_ratchet.py"))
        os.makedirs(os.path.join(self.d, "methodology"))
        _git(self.d, "mv", LEGACY_CONFIG, NEW_CONFIG)
        _git(self.d, "mv", "quality_ratchet.py", "methodology/quality_ratchet.py")
        _git(self.d, "add", "-A")
        p = subprocess.run(["git", "-C", self.d, "commit", "-q", "-m", "the pure move"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_a_tool_file_that_is_itself_a_symlink_keeps_its_name_in_the_repository(self):
        # Only the directory is resolved. Resolving the file would write a path out of the repository
        # (../../elsewhere/quality_ratchet.py) with no twin in the other layout.
        import shutil
        td = tempfile.TemporaryDirectory(); self.addCleanup(td.cleanup)
        real = os.path.join(os.path.realpath(td.name), "shared-ratchet.py")
        shutil.copy(STARTER, real)
        self._symlink(real, os.path.join(self.d, "quality_ratchet.py"))
        _git(self.d, "add", "-A"); _git(self.d, "commit", "-q", "--no-verify", "-m", "add the tool as a symlink")
        self.assertEqual(self._install_via(os.path.join(self.d, "quality_ratchet.py")), [self.LOOP])


# === 1.6.0: a gate that did not pass keeps its output (docs/planning/ratchet-kept-output-plan.md, P2) ===
# Written first, against the plan's sections 3 and 5, and read red on 1.5.1 before the tool changed.
# Every test below builds its own throwaway tree; none runs a gate against this repository.

KEEP = ".quality-gates-output"   # plan 3.2: the directory beside the results file
STAMPED = re.compile(r"^\d{8}T\d{6}Z-[0-9a-z]+(-\d+)?\.txt$")   # plan 3.2: one file per run
ANSI = re.compile(r"\x1b\[[0-9;]*m")


def at(minutes=0):
    """The instant a run starts, for a test that fixes the clock: 2026-11-14 12:00:00 UTC plus `minutes`."""
    return datetime(2026, 11, 14, 12, 0, 0, tzinfo=timezone.utc) + timedelta(minutes=minutes)


def stamp(minutes=0):
    return at(minutes).strftime("%Y%m%dT%H%M%SZ")


class _Clock:
    """Stands in for the module's `datetime` class: now() is one fixed instant, so a test can give two
    runs the same start time, or ordered ones, without sleeping."""

    def __init__(self, instant):
        self.instant = instant

    def now(self, tz=None):
        return self.instant


def _exit_cmd(text="boom", code=3, err=""):
    """A command that prints `text` to stdout and `err` to stderr and exits `code`: as an exit-code gate
    against a ceiling of 0 it reads `fail`."""
    return f'"{PY}" -c "import sys; print({text!r}); sys.stderr.write({err!r}); sys.exit({code})"'


def _flag_cmd(flag, text="no flag yet"):
    """Exits 1 until the file `flag` exists and then 0: a gate that reads fail once and pass after."""
    return f'"{PY}" -c "import os, sys; print({text!r}); sys.exit(0 if os.path.exists({flag!r}) else 1)"'


def _emit_cmd(out_bytes, err_bytes=0, wide=False):
    """A command that prints exactly this many bytes of 'x' (or, wide, of two-byte characters)."""
    ch = "chr(233)" if wide else "'x'"
    pre = "PYTHONIOENCODING=utf-8 " if wide and os.name == "posix" else ""
    return (f'{pre}"{PY}" -c "import sys; sys.stdout.write({ch} * {out_bytes // (2 if wide else 1)}); '
            f'sys.stderr.write(\'x\' * {err_bytes}); sys.exit(3)"')


class _KeptCase(unittest.TestCase):
    def setUp(self):
        td = tempfile.TemporaryDirectory(); self.addCleanup(td.cleanup)
        self.d = os.path.realpath(td.name)
        subprocess.run(["git", "init", "-q", self.d], check=True)

    def run_it(self, *gates, when=None, results_file=None, **extra):
        """do_run through the module, quiet. Returns (exit code, stdout, stderr), colour stripped."""
        cfg = manifest(*gates)
        if results_file:
            cfg["results_file"] = results_file
        out, err = io.StringIO(), io.StringIO()
        clock = mock.patch.object(qr, "datetime", _Clock(when)) if when else contextlib.nullcontext()
        with clock, contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = qr.do_run(self.d, cfg, **extra)
        return rc, ANSI.sub("", out.getvalue()), ANSI.sub("", err.getvalue())

    def status(self, *gates):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            qr.do_status(self.d, manifest(*gates))
        return ANSI.sub("", out.getvalue())

    def results(self):
        with open(os.path.join(self.d, qr.DEFAULT_RESULTS)) as f:
            return json.load(f)

    def folder(self, name):
        return os.path.join(self.d, KEEP, name)

    def files(self, name):
        return sorted(f for f in os.listdir(self.folder(name)) if STAMPED.match(f))

    def read(self, name, fname):
        with open(os.path.join(self.folder(name), fname), encoding="utf-8") as f:
            return f.read()

    def tree(self):
        """Every file under the keeper's directory and its bytes: what a later run must leave alone."""
        found = {}
        for base, _dirs, names in os.walk(os.path.join(self.d, KEEP)):
            for n in names:
                p = os.path.join(base, n)
                with open(p, "rb") as f:
                    found[os.path.relpath(p, self.d)] = f.read()
        return found


class TestAGateThatDidNotPassKeepsItsOutput(_KeptCase):
    """Plan 3.1, 3.2 and 3.3: what is saved, when, where and in what form."""

    def test_a_failing_gate_keeps_what_it_printed_in_a_file_named_by_start_and_commit(self):
        rc, _, _ = self.run_it(gate("suite", "max", 0, command=_exit_cmd("two things broke", 3, "stderr too")),
                               when=at(0))
        self.assertEqual(rc, qr.REFUSED)
        self.assertEqual(self.files("suite"), [f"{stamp(0)}-nohead.txt"])
        text = self.read("suite", self.files("suite")[0])
        self.assertIn("two things broke", text)
        self.assertIn("stderr too", text)

    def test_the_file_name_carries_the_short_commit_when_there_is_one(self):
        _git(self.d, "config", "user.email", "t@t"); _git(self.d, "config", "user.name", "t")
        _git(self.d, "commit", "-q", "--allow-empty", "-m", "c")
        short = _git(self.d, "rev-parse", "--short", "HEAD").stdout.strip()
        self.run_it(gate("suite", "max", 0, command=_exit_cmd()), when=at(0))
        self.assertEqual(self.files("suite"), [f"{stamp(0)}-{short}.txt"])

    def test_the_file_has_exactly_the_form_the_plan_gives(self):
        cmd = f'"{PY}" -c "import sys; print(\'7 passed, 2 failed\'); sys.stderr.write(\'warn\')"'
        self.run_it(gate("passed", "min", 8, command=cmd, extract=r"(\d+) passed"),
                    gate("failed", "max", 1, command=cmd, extract=r", (\d+) failed"), when=at(0))
        want = ("quality-ratchet kept output\n"
                "gates: passed, failed\n"
                f"command: {cmd}\n"
                "exit: 0   budget: 600 s\n"
                "commit: nohead   started: 2026-11-14T12:00:00Z\n"
                "stdout: 19 bytes, kept 19\n"
                "stderr: 4 bytes, kept 4\n"
                "=== stdout ===\n"
                "7 passed, 2 failed\n"
                "=== stderr ===\n"
                "warn\n")
        self.assertEqual(self.read("passed", self.files("passed")[0]), want)

    def test_a_command_of_several_lines_keeps_the_header_one_line_per_field(self):
        cmd = f'"{PY}" -c "pass"\n"{PY}" -c "import sys; print(\'last\'); sys.exit(3)"'
        self.run_it(gate("multi", "max", 0, command=cmd), when=at(0))
        lines = self.read("multi", self.files("multi")[0]).split("\n")
        self.assertEqual(lines.index("=== stdout ==="), 7, lines[:10])
        self.assertTrue(lines[2].startswith("command: ") and "\\n" in lines[2], lines[2])

    def test_the_start_in_the_file_is_the_runs_not_the_moment_the_file_is_written(self):
        # ran_at is stamped at the END of a run (about 34 minutes after its start on the real suite); the file
        # is named by the START. This clock reads 12:00 until the first gate's command has run, 12:10 after.
        marker = os.path.join(self.d, "started.marker")

        class Late:
            def now(self, tz=None):
                return at(10) if os.path.exists(marker) else at(0)
        cmd = f'"{PY}" -c "import sys; open({marker!r}, \'w\').close(); sys.exit(3)"'
        with mock.patch.object(qr, "datetime", Late()), contextlib.redirect_stdout(io.StringIO()):
            qr.do_run(self.d, manifest(gate("suite", "max", 0, command=cmd)))
        self.assertEqual(self.files("suite"), [f"{stamp(0)}-nohead.txt"])
        self.assertIn("started: 2026-11-14T12:00:00Z\n", self.read("suite", self.files("suite")[0]))

    def test_an_unmeasured_gate_whose_command_ran_keeps_its_output_too(self):
        cmd = f'"{PY}" -c "import sys; print(\'no digits here\'); sys.exit(7)"'
        rc, _, _ = self.run_it(gate("nomatch", "min", 1, command=cmd, extract=r"(\d+)"), when=at(0))
        self.assertEqual(rc, qr.WARN)
        text = self.read("nomatch", self.files("nomatch")[0])
        self.assertIn("exit: 7", text)
        self.assertIn("no digits here", text)

    def test_a_gate_with_no_command_keeps_nothing(self):
        rc, _, _ = self.run_it(gate("declared", "min", 1), when=at(0))
        self.assertEqual(rc, qr.WARN)
        self.assertFalse(os.path.exists(os.path.join(self.d, KEEP)))

    def test_a_command_that_outlived_its_budget_keeps_nothing(self):
        rc, _, _ = self.run_it(gate("slow", "max", 0, command=slow(3, "'late'"), timeout_seconds=0.5), when=at(0))
        self.assertEqual(rc, qr.WARN)
        self.assertEqual(self.results()["gates"][0]["note"], "timeout (0.5 s)")
        self.assertFalse(os.path.exists(os.path.join(self.d, KEEP)))
        self.assertNotIn("kept", self.results())

    def test_a_run_in_which_every_gate_passes_writes_nothing_at_all(self):
        rc, out, _ = self.run_it(gate("ok", "max", 0, command=f'"{PY}" -c "pass"'), when=at(0))
        self.assertEqual(rc, qr.CLEAN)
        self.assertFalse(os.path.exists(os.path.join(self.d, KEEP)))
        self.assertNotIn("kept", out)

    def test_a_green_run_after_a_red_one_deletes_nothing_and_adds_nothing(self):
        # The whole point of the design (3.1): S384 and S430 were red once and green after. A cleanup on
        # green would erase the evidence the way the results file does.
        flag = os.path.join(self.d, "flag")
        g = gate("suite", "max", 0, command=_flag_cmd(flag))
        self.assertEqual(self.run_it(g, when=at(0))[0], qr.REFUSED)
        before = self.tree()
        self.assertTrue(before)
        open(flag, "w").close()
        self.assertEqual(self.run_it(g, when=at(1))[0], qr.CLEAN)
        self.assertEqual(self.tree(), before)

    def test_two_gates_over_one_command_share_one_file_in_the_first_gates_folder(self):
        cmd = f'"{PY}" -c "print(\'7 passed, 2 failed\')"'
        self.run_it(gate("passed", "min", 8, command=cmd, extract=r"(\d+) passed"),
                    gate("failed", "max", 1, command=cmd, extract=r", (\d+) failed"), when=at(0))
        self.assertEqual(len(self.files("passed")), 1)
        self.assertFalse(os.path.exists(self.folder("failed")))
        kept = self.results()["kept"]
        self.assertEqual(set(kept), {"passed", "failed"})
        self.assertEqual(kept["passed"], kept["failed"])

    def test_a_shared_command_is_kept_when_only_the_second_gate_fails(self):
        cmd = f'"{PY}" -c "print(\'7 passed, 2 failed\')"'
        self.run_it(gate("passed", "min", 7, command=cmd, extract=r"(\d+) passed"),
                    gate("failed", "max", 1, command=cmd, extract=r", (\d+) failed"), when=at(0))
        self.assertEqual(len(self.files("passed")), 1)   # the folder is the FIRST gate over the command
        self.assertEqual(list(self.results()["kept"]), ["failed"])
        self.assertIn("gates: passed, failed\n", self.read("passed", self.files("passed")[0]))

    def test_the_kept_map_names_only_the_gates_kept_in_this_run(self):
        flag = os.path.join(self.d, "flag")
        first = gate("first", "max", 0, command=_flag_cmd(flag))
        second = gate("second", "max", 0, command=_exit_cmd("always"))
        self.run_it(first, second, when=at(0))
        self.assertEqual(set(self.results()["kept"]), {"first", "second"})
        open(flag, "w").close()
        self.run_it(first, second, when=at(1))
        self.assertEqual(set(self.results()["kept"]), {"second"})

    def test_kept_paths_are_relative_to_the_results_file_with_forward_slashes(self):
        self.run_it(gate("suite", "max", 0, command=_exit_cmd()), when=at(0))
        rel = self.results()["kept"]["suite"]
        self.assertEqual(rel, f"{KEEP}/suite/{stamp(0)}-nohead.txt")
        self.assertTrue(os.path.isfile(os.path.join(self.d, *rel.split("/"))))

    def test_a_run_that_kept_nothing_has_no_kept_key(self):
        self.run_it(gate("ok", "max", 0, command=f'"{PY}" -c "pass"'), when=at(0))
        self.assertNotIn("kept", self.results())

    def test_the_results_hash_and_the_gate_records_are_what_1_5_1_wrote(self):
        # The `results` hash is what a receipt cites, and the dashboards read `gates`. The literal below was
        # produced by the UNMODIFIED 1.5.1 tool over this manifest (a pass, a fail, an unmeasured gate whose
        # command ran, a gate with no command); through do_run, with the keeper on, 1.6.0 must equal it.
        gates = [gate("ok", "min", 3, command=f'"{PY}" -c "print(3)"', extract=r"(\d+)"),
                 gate("bad", "max", 0, command=f'"{PY}" -c "import sys; print(\'x\'); sys.exit(3)"'),
                 gate("nomatch", "min", 1, command=f'"{PY}" -c "import sys; print(\'none\'); sys.exit(7)"',
                      extract=r"(\d+)"),
                 gate("declared", "min", 1)]
        self.run_it(*gates, when=at(0))
        snap = self.results()
        self.assertEqual(snap["results"], "418ad3de2bbd")
        self.assertEqual(snap["summary"], {"pass": 1, "fail": 1, "unmeasured": 2})
        for r in snap["gates"]:
            self.assertEqual(sorted(r), ["direction", "measured", "name", "note", "status", "threshold"])

    def test_the_gates_that_did_not_pass_and_whose_command_ran_are_the_ones_kept(self):
        # the same manifest as above: `bad` failed, `nomatch` is unmeasured with an exit code; `ok` passed and
        # `declared` has no command
        gates = [gate("ok", "min", 3, command=f'"{PY}" -c "print(3)"', extract=r"(\d+)"),
                 gate("bad", "max", 0, command=f'"{PY}" -c "import sys; print(\'x\'); sys.exit(3)"'),
                 gate("nomatch", "min", 1, command=f'"{PY}" -c "import sys; print(\'none\'); sys.exit(7)"',
                      extract=r"(\d+)"),
                 gate("declared", "min", 1)]
        self.run_it(*gates, when=at(0))
        self.assertEqual(set(self.results()["kept"]), {"bad", "nomatch"})

    def test_exit_codes_do_not_change_when_output_is_kept(self):
        self.assertEqual(self.run_it(gate("f", "max", 0, command=_exit_cmd()))[0], qr.REFUSED)
        self.assertEqual(self.run_it(gate("u", "min", 1, command=_exit_cmd(), extract=r"(\d+)"))[0], qr.WARN)


class TestWhereTheOutputGoesAndHowLongItStays(_KeptCase):
    """Plan 3.2 (where, names) and 3.4 (how long)."""

    def test_the_directory_sits_beside_the_results_file_in_the_legacy_layout(self):
        self.run_it(gate("suite", "max", 0, command=_exit_cmd()), when=at(0))
        self.assertTrue(os.path.isdir(os.path.join(self.d, KEEP)))
        self.assertTrue(os.path.isfile(os.path.join(self.d, qr.DEFAULT_RESULTS)))

    def test_the_directory_sits_beside_the_results_file_in_the_new_layout(self):
        _put(self.d, NEW_CONFIG, manifest())
        self.run_it(gate("suite", "max", 0, command=_exit_cmd()), when=at(0))
        self.assertTrue(os.path.isfile(os.path.join(self.d, "methodology", qr.DEFAULT_RESULTS)))
        self.assertTrue(os.path.isdir(os.path.join(self.d, "methodology", KEEP)))
        self.assertFalse(os.path.exists(os.path.join(self.d, KEEP)), "nothing at the root")

    def test_an_explicit_results_file_decides_where_the_directory_goes(self):
        os.makedirs(os.path.join(self.d, "out"))
        self.run_it(gate("suite", "max", 0, command=_exit_cmd()), when=at(0), results_file="out/r.json")
        self.assertTrue(os.path.isdir(os.path.join(self.d, "out", KEEP)))
        self.assertFalse(os.path.exists(os.path.join(self.d, KEEP)))
        rel = json.load(open(os.path.join(self.d, "out", "r.json")))["kept"]["suite"]
        self.assertEqual(rel, f"{KEEP}/suite/{stamp(0)}-nohead.txt")   # relative to the results file's directory

    def test_the_directory_is_invisible_to_git_and_the_projects_gitignore_is_not_touched(self):
        self.run_it(gate("suite", "max", 0, command=_exit_cmd()), when=at(0))
        self.assertEqual(open(os.path.join(self.d, KEEP, ".gitignore")).read(), "*\n")
        listing = _git(self.d, "status", "--porcelain", "--untracked-files=all").stdout
        self.assertNotIn(KEEP, listing)
        self.assertFalse(os.path.exists(os.path.join(self.d, ".gitignore")))

    def test_the_gitignore_is_written_again_on_every_write(self):
        g = gate("suite", "max", 0, command=_exit_cmd())
        self.run_it(g, when=at(0))
        os.remove(os.path.join(self.d, KEEP, ".gitignore"))
        self.run_it(g, when=at(1))
        self.assertEqual(open(os.path.join(self.d, KEEP, ".gitignore")).read(), "*\n")

    def test_a_gate_name_becomes_a_safe_folder_name_and_never_escapes(self):
        # config_defects accepts any non-empty string as a gate name, so these must not escape the
        # directory or collide (one folder on APFS for 'Tests' and 'tests').
        plain = ["suite", "tests-sh-passed", "a.b_c", "0lead"]
        odd = ["a/b", "..", ".hidden", "Tests", "has space", "x" * 300, "y" * 65, "-lead", "café", "back\\slash", "a:b*c"]
        for name in plain + odd:
            with self.subTest(name=name[:20]):
                self.setUp()
                self.run_it(gate(name, "max", 0, command=_exit_cmd()), when=at(0))
                rel = self.results()["kept"][name]
                parts = rel.split("/")
                self.assertEqual((len(parts), parts[0]), (3, KEEP), rel)
                folder = parts[1]
                self.assertRegex(folder, r"^[a-z0-9_][a-z0-9._-]*$")
                self.assertLessEqual(len(folder), 64)
                self.assertTrue(os.path.isfile(os.path.join(self.d, *parts)))
                self.assertLessEqual(set(os.listdir(self.d)), {".git", KEEP, qr.DEFAULT_RESULTS})
                if name in plain:
                    self.assertEqual(folder, name)
                else:
                    self.assertTrue(folder.endswith("-" + hashlib.sha256(name.encode()).hexdigest()[:6]), folder)

    def test_two_names_that_differ_only_in_case_get_two_folders(self):
        self.run_it(gate("tests", "max", 0, command=_exit_cmd("lower")),
                    gate("Tests", "max", 0, command=_exit_cmd("upper")), when=at(0))
        kept = self.results()["kept"]
        self.assertNotEqual(kept["tests"], kept["Tests"])
        self.assertTrue(kept["Tests"].split("/")[1].startswith("tests-"), kept["Tests"])   # lowercased, then the hash
        self.assertEqual(len([e for e in os.listdir(os.path.join(self.d, KEEP)) if e != ".gitignore"]), 2)

    def test_the_newest_five_files_per_gate_are_kept_and_the_rest_removed(self):
        g = gate("suite", "max", 0, command=_exit_cmd())
        for n in range(8):
            self.run_it(g, when=at(n))
        self.assertEqual(self.files("suite"), [f"{stamp(n)}-nohead.txt" for n in range(3, 8)])

    def test_retention_is_per_gate_so_a_gate_that_never_measures_cannot_evict_the_suites_red(self):
        flag = os.path.join(self.d, "flag")
        suite = gate("suite", "max", 0, command=_flag_cmd(flag))
        broken = gate("broken", "min", 1, command=_exit_cmd("no number", 0), extract=r"(\d+)")
        self.run_it(suite, broken, when=at(0))     # the suite is red once
        open(flag, "w").close()
        for n in range(1, 8):                       # then seven runs in which only `broken` is not passing
            self.run_it(suite, broken, when=at(n))
        self.assertEqual(self.files("suite"), [f"{stamp(0)}-nohead.txt"])
        self.assertEqual(len(self.files("broken")), 5)

    def test_two_runs_with_one_start_and_commit_do_not_overwrite_each_other(self):
        g = gate("suite", "max", 0, command=_exit_cmd("first"))
        self.run_it(g, when=at(0))
        first = self.read("suite", f"{stamp(0)}-nohead.txt")
        self.run_it(gate("suite", "max", 0, command=_exit_cmd("second")), when=at(0))
        self.run_it(gate("suite", "max", 0, command=_exit_cmd("third")), when=at(0))
        self.assertEqual(self.files("suite"),
                         [f"{stamp(0)}-nohead-2.txt", f"{stamp(0)}-nohead-3.txt", f"{stamp(0)}-nohead.txt"])
        self.assertEqual(self.read("suite", f"{stamp(0)}-nohead.txt"), first)
        self.assertIn("second", self.read("suite", f"{stamp(0)}-nohead-2.txt"))

    def test_files_of_one_second_are_ordered_by_their_number_when_the_newest_five_are_kept(self):
        # four files already hold this second (the plain name, -2, -3, -4); two more runs make six, and the
        # one to go is the oldest of them: the plain name, not the one that happens to sort lowest as text
        os.makedirs(self.folder("suite"))
        base = f"{stamp(0)}-nohead"
        for name in (f"{base}.txt", f"{base}-2.txt", f"{base}-3.txt", f"{base}-4.txt"):
            open(os.path.join(self.folder("suite"), name), "w").write("planted\n")
        g = gate("suite", "max", 0, command=_exit_cmd())
        self.run_it(g, when=at(0))
        self.run_it(g, when=at(0))
        self.assertEqual(self.files("suite"), sorted(f"{base}-{n}.txt" for n in range(2, 7)))

    def test_a_future_dated_stray_file_cannot_make_the_file_just_written_the_oldest(self):
        os.makedirs(self.folder("suite"))
        for i in range(1, 7):
            open(os.path.join(self.folder("suite"), f"2999010{i}T000000Z-abcdef0.txt"), "w").write("old\n")
        self.run_it(gate("suite", "max", 0, command=_exit_cmd("new")), when=at(0))
        self.assertEqual(self.files("suite"),
                         sorted([f"{stamp(0)}-nohead.txt"] + [f"2999010{i}T000000Z-abcdef0.txt" for i in range(3, 7)]))

    @unittest.skipUnless(os.name == "posix", "symlinks: POSIX only")
    def test_pruning_never_follows_a_link_and_never_removes_a_name_of_another_form(self):
        os.makedirs(self.folder("suite"))
        outside = os.path.join(self.d, "outside.txt")
        open(outside, "w").write("precious\n")
        link = os.path.join(self.folder("suite"), "20200101T000000Z-aaaaaaa.txt")
        os.symlink(outside, link)
        stray = os.path.join(self.folder("suite"), "notes.txt")
        open(stray, "w").write("mine\n")
        g = gate("suite", "max", 0, command=_exit_cmd())
        for n in range(7):
            self.run_it(g, when=at(n))
        self.assertTrue(os.path.islink(link))
        self.assertEqual(open(outside).read(), "precious\n")
        self.assertEqual(open(stray).read(), "mine\n")
        regular = [f for f in self.files("suite") if not os.path.islink(os.path.join(self.folder("suite"), f))]
        self.assertEqual(len(regular), 5)

    @unittest.skipUnless(os.name == "posix", "symlinks: POSIX only")
    def test_a_link_where_a_directory_should_be_is_not_written_through(self):
        outside = os.path.join(self.d, "elsewhere")
        os.makedirs(outside)
        os.symlink(outside, os.path.join(self.d, KEEP))
        rc, _, err = self.run_it(gate("suite", "max", 0, command=_exit_cmd()), when=at(0))
        self.assertEqual(rc, qr.REFUSED)
        self.assertEqual(os.listdir(outside), [], "a link is never written through")
        self.assertEqual(err.count("could not keep"), 1, err)


class TestKeepingNeverChangesTheRun(_KeptCase):
    """Plan 3.6: a failure to keep is one warning on stderr and nothing else."""

    def _unkept(self, *gates):
        """What the same run says with nothing kept: the exit code and the results hash."""
        snap = qr.run_gates(self.d, manifest(*gates))
        return snap["results"]

    @unittest.skipUnless(os.name == "posix" and (not hasattr(os, "geteuid") or os.geteuid() != 0),
                         "permissions: POSIX, not root")
    def test_an_unwritable_directory_is_one_warning_and_the_run_is_otherwise_the_same(self):
        os.mkdir(os.path.join(self.d, KEEP)); os.chmod(os.path.join(self.d, KEEP), 0o500)
        self.addCleanup(os.chmod, os.path.join(self.d, KEEP), 0o700)
        g = gate("suite", "max", 0, command=_exit_cmd())
        rc, _, err = self.run_it(g, when=at(0))
        self.assertEqual(rc, qr.REFUSED)
        self.assertEqual(self.results()["results"], self._unkept(g))
        self.assertNotIn("kept", self.results())
        self.assertEqual(err.count("could not keep"), 1, err)

    def test_a_keeper_that_fails_with_something_other_than_an_oserror_is_a_warning_too(self):
        # an encoding error, say: it must not escape as a traceback with exit 1 where exit 2 was owed
        g = gate("suite", "max", 0, command=_exit_cmd())
        with mock.patch("os.mkdir", side_effect=ValueError("boom")):
            rc, _, err = self.run_it(g, when=at(0))
        self.assertEqual(rc, qr.REFUSED)
        self.assertIn("could not keep", err)
        self.assertIn("boom", err)
        self.assertEqual(self.results()["results"], self._unkept(g))

    def test_however_many_gates_fail_to_keep_the_run_warns_once(self):
        gates = [gate(f"g{i}", "max", 0, command=_exit_cmd(str(i))) for i in range(3)]
        with mock.patch("os.mkdir", side_effect=ValueError("boom")):
            _, _, err = self.run_it(*gates, when=at(0))
        self.assertEqual(err.count("could not keep"), 1, err)

    def test_a_file_where_the_directory_should_be_is_a_warning_and_stays_untouched(self):
        open(os.path.join(self.d, KEEP), "w").write("mine\n")
        rc, _, err = self.run_it(gate("suite", "max", 0, command=_exit_cmd()), when=at(0))
        self.assertEqual(rc, qr.REFUSED)
        self.assertEqual(open(os.path.join(self.d, KEEP)).read(), "mine\n")
        self.assertEqual(err.count("could not keep"), 1, err)

    def test_a_results_folder_that_does_not_exist_fails_as_it_does_today_and_makes_nothing(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(FileNotFoundError):
                qr.do_run(self.d, dict(manifest(gate("suite", "max", 0, command=_exit_cmd())),
                                       results_file="nowhere/r.json"))
        self.assertFalse(os.path.exists(os.path.join(self.d, "nowhere")))

    def test_a_keeper_that_cannot_be_built_is_a_warning_and_the_run_goes_on(self):
        real, calls = qr.head_sha, []

        def flaky(root):
            calls.append(1)
            if len(calls) == 1:               # the keeper reads the commit first, before any gate
                raise ValueError("no git here")
            return real(root)
        g = gate("suite", "max", 0, command=_exit_cmd())
        with mock.patch.object(qr, "head_sha", flaky):
            rc, _, err = self.run_it(g, when=at(0))
        self.assertEqual(rc, qr.REFUSED)
        self.assertIn("could not keep the output of this run", err)
        self.assertIn("no git here", err)
        self.assertEqual(self.results()["results"], self._unkept(g))
        self.assertFalse(os.path.exists(os.path.join(self.d, KEEP)))

    def test_a_run_cut_short_keeps_what_its_finished_gates_had_saved(self):
        real, calls = qr.measure_gate, []

        def cut_short(root, g, timeout, memo=None, budget=None):
            calls.append(g["name"])
            if len(calls) == 2:
                raise SystemExit(143)
            return real(root, g, timeout, memo, budget)
        cfg = manifest(gate("first", "max", 0, command=_exit_cmd("kept me")),
                       gate("second", "max", 0, command=_exit_cmd("never run")))
        with mock.patch.object(qr, "measure_gate", cut_short), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit):
                qr.do_run(self.d, cfg)
        self.assertEqual(len(self.files("first")), 1)
        self.assertIn("kept me", self.read("first", self.files("first")[0]))
        self.assertFalse(os.path.exists(self.folder("second")))


class TestWhatIsKeptOfALongStream(_KeptCase):
    """Plan 3.3 and D2: each stream is kept whole up to a cap, then cut in the middle."""

    def test_the_numbers_are_the_operators(self):
        self.assertEqual(qr.KEEP_HEAD, 64 * 1024)
        self.assertEqual(qr.KEEP_TAIL, 192 * 1024)
        self.assertEqual(qr.KEEP_FILES, 5)

    def test_the_whole_suite_sized_output_is_kept_whole(self):
        # E2: one real run of bin/tests.sh printed 59,382 bytes. The cap sits far above it.
        self.run_it(gate("suite", "max", 0, command=_emit_cmd(59382)), when=at(0))
        text = self.read("suite", self.files("suite")[0])
        self.assertIn("stdout: 59382 bytes, kept 59382\n", text)
        self.assertIn("x" * 59382, text)
        self.assertNotIn("omitted", text)

    def test_a_stream_over_the_cap_is_cut_in_the_middle_and_says_how_much_went(self):
        cmd = (f'"{PY}" -c "import sys; sys.stdout.write(\'a\' * 10 + \'b\' * 100 + \'c\' * 20); sys.exit(3)"')
        with mock.patch.object(qr, "KEEP_HEAD", 10), mock.patch.object(qr, "KEEP_TAIL", 20):
            self.run_it(gate("suite", "max", 0, command=cmd), when=at(0))
        text = self.read("suite", self.files("suite")[0])
        self.assertIn("stdout: 130 bytes, kept 30\n", text)
        self.assertIn("=== stdout ===\n" + "a" * 10 + "\n... [100 bytes omitted] ...\n" + "c" * 20 + "\n", text)

    def test_a_cut_never_leaves_half_a_character(self):
        # 80 bytes of two-byte characters; a head of 11 and a tail of 21 both split one
        with mock.patch.object(qr, "KEEP_HEAD", 11), mock.patch.object(qr, "KEEP_TAIL", 21):
            self.run_it(gate("suite", "max", 0, command=_emit_cmd(80, wide=True)), when=at(0))
        text = self.read("suite", self.files("suite")[0])      # strict UTF-8: a split character would raise
        self.assertNotIn("�", text)
        self.assertIn("stdout: 80 bytes, kept 30\n", text)
        self.assertIn("[50 bytes omitted]", text)

    def test_a_long_stream_is_cut_at_the_real_caps(self):
        self.run_it(gate("suite", "max", 0, command=_emit_cmd(300000)), when=at(0))
        text = self.read("suite", self.files("suite")[0])
        self.assertIn("stdout: 300000 bytes, kept 262144\n", text)
        self.assertIn(f"[{300000 - 262144} bytes omitted]", text)

    def test_a_stream_of_exactly_the_cap_is_kept_whole_and_one_byte_more_is_cut(self):
        cap = 64 * 1024 + 192 * 1024
        self.run_it(gate("exact", "max", 0, command=_emit_cmd(cap)), when=at(0))
        text = self.read("exact", self.files("exact")[0])
        self.assertIn(f"stdout: {cap} bytes, kept {cap}\n", text)
        self.assertNotIn("omitted", text)
        self.run_it(gate("over", "max", 0, command=_emit_cmd(cap + 1)), when=at(0))
        text = self.read("over", self.files("over")[0])
        self.assertIn(f"stdout: {cap + 1} bytes, kept {cap}\n", text)
        self.assertIn("[1 bytes omitted]", text)

    def test_a_file_is_bounded_by_its_two_caps_plus_a_header(self):
        self.run_it(gate("suite", "max", 0, command=_emit_cmd(300000, 300000)), when=at(0))
        size = os.path.getsize(os.path.join(self.folder("suite"), self.files("suite")[0]))
        self.assertLessEqual(size, 2 * (64 * 1024 + 192 * 1024) + 2048)
        self.assertIn("stderr: 300000 bytes, kept 262144\n", self.read("suite", self.files("suite")[0]))


class TestWhatThePersonSees(_KeptCase):
    """Plan 3.5: a line after the table, from the directory itself, in --run and in --status."""

    def _on_disk(self, n_files, n_folders, newest, gate_name):
        return (f"kept output on disk: {n_files} file(s) in {n_folders} gate folder(s) under "
                f"{os.path.join(self.d, KEEP)}; newest {newest} ({gate_name})")

    def test_run_prints_the_on_disk_line_and_one_line_for_each_gate_kept(self):
        _, out, _ = self.run_it(gate("suite", "max", 0, command=_exit_cmd()), when=at(0))
        self.assertIn(self._on_disk(1, 1, f"{stamp(0)}-nohead.txt", "suite"), out)
        mine = [ln for ln in out.splitlines() if ln.strip().startswith("kept:")]
        self.assertEqual(len(mine), 1, out)
        self.assertIn("suite", mine[0])
        self.assertIn(os.path.join(self.d, KEEP, "suite", f"{stamp(0)}-nohead.txt"), mine[0])

    def test_run_prints_nothing_about_kept_output_when_there_is_none(self):
        _, out, _ = self.run_it(gate("ok", "max", 0, command=f'"{PY}" -c "pass"'), when=at(0))
        self.assertNotIn("kept", out)

    def test_status_after_a_later_green_run_still_points_at_the_red_runs_file(self):
        flag = os.path.join(self.d, "flag")
        g = gate("suite", "max", 0, command=_flag_cmd(flag))
        self.run_it(g, when=at(0))
        before = self.tree()
        open(flag, "w").close()
        self.run_it(g, when=at(1))
        self.assertNotIn("kept", self.results(), "a green snapshot carries no kept key")
        out = self.status(g)
        self.assertIn(self._on_disk(1, 1, f"{stamp(0)}-nohead.txt", "suite"), out)
        self.assertEqual(self.tree(), before)

    def test_status_prints_a_line_for_each_stored_gate_whose_file_still_exists(self):
        a, b = gate("a", "max", 0, command=_exit_cmd("aa")), gate("b", "max", 0, command=_exit_cmd("bb"))
        self.run_it(a, b, when=at(0))
        lines = [ln for ln in self.status(a, b).splitlines() if ln.strip().startswith("kept:")]
        self.assertEqual(len(lines), 2, lines)
        os.remove(os.path.join(self.folder("b"), f"{stamp(0)}-nohead.txt"))
        lines = [ln for ln in self.status(a, b).splitlines() if ln.strip().startswith("kept:")]
        self.assertEqual(len(lines), 1, lines)
        self.assertIn(os.path.join(self.d, KEEP, "a"), lines[0])

    def test_status_with_a_stored_kept_that_means_nothing_here_does_not_crash(self):
        g = gate("ok", "max", 0, command=f'"{PY}" -c "pass"')
        self.run_it(g, when=at(0))
        snap = self.results()
        for junk in (5, [1, 2], {"ok": 7}, {"ok": "../../etc/passwd"}, None):
            with self.subTest(junk=junk):
                snap["kept"] = junk
                with open(os.path.join(self.d, qr.DEFAULT_RESULTS), "w") as f:
                    json.dump(snap, f)
                out = self.status(g)
                self.assertIn("1/1 pass", out)
                self.assertNotIn("passwd", out, "a stored path that leaves the directory is never followed")

    NAME = f"{stamp(0)}-nohead.txt"

    def _stored(self, rel):
        """--status over a results file whose `kept` names `rel`: the `kept:` lines it prints."""
        g = gate("ok", "max", 0, command=f'"{PY}" -c "pass"')
        self.run_it(g, when=at(0))
        snap = self.results()
        snap["kept"] = {"ok": rel}
        with open(os.path.join(self.d, qr.DEFAULT_RESULTS), "w") as f:
            json.dump(snap, f)
        return [ln for ln in self.status(g).splitlines() if ln.strip().startswith("kept:")]

    def test_a_stored_path_that_climbs_out_of_the_directory_is_not_printed(self):
        os.mkdir(os.path.join(self.d, KEEP))
        open(os.path.join(self.d, self.NAME), "w").write("outside\n")      # where ../NAME would lead
        self.assertEqual(self._stored(f"{KEEP}/../{self.NAME}"), [])

    def test_a_stored_path_that_does_not_start_with_the_directory_is_not_printed(self):
        os.makedirs(self.folder("suite"))
        open(os.path.join(self.folder("suite"), self.NAME), "w").write("real\n")
        self.assertEqual(self._stored(f"elsewhere/suite/{self.NAME}"), [])
        self.assertEqual(len(self._stored(f"{KEEP}/suite/{self.NAME}")), 1)   # the same file by its true path

    def test_a_stored_path_that_is_not_a_kept_files_name_is_not_printed(self):
        os.makedirs(self.folder("suite"))
        open(os.path.join(self.folder("suite"), "notes.txt"), "w").write("mine\n")
        self.assertEqual(self._stored(f"{KEEP}/suite/notes.txt"), [])

    @unittest.skipUnless(os.name == "posix", "symlinks: POSIX only")
    def test_a_stored_path_that_is_a_link_is_not_printed(self):
        os.makedirs(self.folder("suite"))
        outside = os.path.join(self.d, "outside.txt")
        open(outside, "w").write("precious\n")
        os.symlink(outside, os.path.join(self.folder("suite"), self.NAME))
        self.assertEqual(self._stored(f"{KEEP}/suite/{self.NAME}"), [])

    @unittest.skipUnless(os.name == "posix", "symlinks: POSIX only")
    def test_a_gate_folder_that_is_a_link_is_not_counted(self):
        os.makedirs(self.folder("real"))
        open(os.path.join(self.folder("real"), self.NAME), "w").write("one\n")
        ext = os.path.join(self.d, "ext")
        os.makedirs(ext)
        for n in (1, 2):
            open(os.path.join(ext, f"{stamp(n)}-nohead.txt"), "w").write("two\n")
        os.symlink(ext, self.folder("linked"))
        g = gate("ok", "max", 0, command=f'"{PY}" -c "pass"')
        _, out, _ = self.run_it(g, when=at(0))
        self.assertIn("kept output on disk: 1 file(s) in 1 gate folder(s)", out)

    @unittest.skipUnless(os.name == "posix", "symlinks: POSIX only")
    def test_a_directory_that_is_a_link_is_not_scanned(self):
        os.makedirs(os.path.join(self.d, "elsewhere", "suite"))
        open(os.path.join(self.d, "elsewhere", "suite", self.NAME), "w").write("x\n")
        os.symlink(os.path.join(self.d, "elsewhere"), os.path.join(self.d, KEEP))
        _, out, _ = self.run_it(gate("ok", "max", 0, command=f'"{PY}" -c "pass"'), when=at(0))
        self.assertNotIn("kept output on disk", out)

    def test_the_on_disk_line_names_the_newest_file_across_all_gate_folders(self):
        self.run_it(gate("b", "max", 0, command=_exit_cmd("old")), when=at(1))
        _, out, _ = self.run_it(gate("a", "max", 0, command=_exit_cmd("new")), when=at(5))
        self.assertIn(f"in 2 gate folder(s) under {os.path.join(self.d, KEEP)}; newest {stamp(5)}-nohead.txt (a)", out)

    def _cli(self, *args):
        return subprocess.run([PY, str(STARTER), *args], cwd=self.d, capture_output=True, text=True)

    def test_the_command_line_run_prints_the_lines_and_exits_as_before(self):
        json.dump(manifest(gate("suite", "max", 0, command=_exit_cmd("on the CLI"))),
                  open(os.path.join(self.d, qr.CONFIG_NAME), "w"))
        p = self._cli("--run")
        out = ANSI.sub("", p.stdout)
        self.assertEqual(p.returncode, qr.REFUSED, out + p.stderr)
        self.assertIn("kept output on disk: 1 file(s) in 1 gate folder(s) under ", out)
        self.assertEqual(self._cli("--status").returncode, qr.REFUSED)
        self.assertIn("kept output on disk: 1 file(s)", ANSI.sub("", self._cli("--status").stdout))

    def test_under_json_stdout_is_still_one_document_and_carries_kept(self):
        json.dump(manifest(gate("suite", "max", 0, command=_exit_cmd())),
                  open(os.path.join(self.d, qr.CONFIG_NAME), "w"))
        p = self._cli("--run", "--json")
        self.assertEqual(p.returncode, qr.REFUSED, p.stderr)
        doc = json.loads(p.stdout)                      # a caller that parses stdout still can
        self.assertEqual(list(doc["kept"]), ["suite"])
        self.assertEqual(self._cli("--status", "--json").returncode, qr.REFUSED)
        self.assertEqual(list(json.loads(self._cli("--status", "--json").stdout)["kept"]), ["suite"])

    def test_a_warning_under_json_goes_to_stderr_and_stdout_still_parses(self):
        json.dump(manifest(gate("suite", "max", 0, command=_exit_cmd())),
                  open(os.path.join(self.d, qr.CONFIG_NAME), "w"))
        open(os.path.join(self.d, KEEP), "w").write("a file where the directory goes\n")
        p = self._cli("--run", "--json")
        self.assertEqual(p.returncode, qr.REFUSED)
        json.loads(p.stdout)
        self.assertIn("could not keep", p.stderr)


class TestRunGatesHandsEachResultToTheKeeper(_KeptCase):
    """Plan 3.7: run_gates(root, cfg, timeout, keep=None); keep(result, raw) after each gate."""

    def test_keep_is_called_after_each_gate_with_its_result_and_the_commands_raw_output(self):
        record = []
        seen, calls = os.path.join(self.d, "seen.txt"), os.path.join(self.d, "calls.txt")

        def keep(res, raw):
            record.append((res["name"], res["status"], raw))
            open(calls, "a").write(res["name"])
        cmd_a = _exit_cmd("aaa", 3)
        cmd_b = f'"{PY}" -c "import os; open({seen!r}, \'w\').write(str(os.path.exists({calls!r})))"'
        snap = qr.run_gates(self.d, manifest(gate("a", "max", 0, command=cmd_a),
                                              gate("b", "max", 0, command=cmd_b),
                                              gate("c", "max", 5, command=cmd_a),
                                              gate("d", "min", 1)), keep=keep)
        self.assertEqual([r[0] for r in record], ["a", "b", "c", "d"])
        self.assertEqual([r[1] for r in record], ["fail", "pass", "pass", "unmeasured"])
        self.assertEqual(record[0][2], (3, "aaa\n", "", False, 600))
        self.assertEqual(record[2][2], record[0][2], "a shared command hands the same run to both gates")
        self.assertIsNone(record[3][2], "a gate with no command has no raw output")
        self.assertEqual(open(seen).read(), "True", "gate a was handed over before gate b's command started")
        self.assertNotIn("kept", snap, "the keeper's map is do_run's to attach, not run_gates'")

    def test_without_keep_run_gates_returns_what_it_always_did_and_writes_nothing(self):
        cfg = manifest(gate("suite", "max", 0, command=_exit_cmd()))
        snap = qr.run_gates(self.d, cfg)
        self.assertEqual(snap["summary"], {"pass": 0, "fail": 1, "unmeasured": 0})
        self.assertEqual(sorted(snap), ["gates", "head", "manifest", "ran_at", "results", "summary", "version"])
        self.assertFalse(os.path.exists(os.path.join(self.d, KEEP)))


class TestToolInvariants(unittest.TestCase):
    def test_the_version_is_1_6_0(self):
        self.assertEqual(qr.VERSION, "1.6.0")

    def test_help_and_the_module_docstring_say_what_is_kept_where_and_that_it_is_not_for_git(self):
        p = subprocess.run([PY, str(STARTER), "--help"], capture_output=True, text=True)
        for where, text in (("--help", p.stdout), ("docstring", qr.__doc__)):
            with self.subTest(where=where):
                self.assertIn(KEEP, text)
                self.assertIn("do not commit", text.lower())

    def test_selftest_observes_a_failing_gate_keeping_its_output_and_a_green_run_leaving_it(self):
        p = subprocess.run([PY, str(STARTER), "--selftest"], capture_output=True, text=True)
        for label in ("a failing gate keeps its output", "a later passing run leaves it"):
            self.assertRegex(p.stdout, r"PASS\x1b\[0m  " + label, p.stdout)

    def test_no_force_escape_hatch(self):
        src = STARTER.read_text(encoding="utf-8")
        self.assertNotIn('"--force" in args and', src)
        rc = subprocess.run([PY, str(STARTER), "--force"], capture_output=True, text=True)
        self.assertEqual(rc.returncode, qr.USAGE)
        self.assertIn("no --force", rc.stdout)

    def test_a_gate_command_gets_its_own_session_wherever_there_are_process_groups(self):
        self.assertEqual(qr.HAS_PROCESS_GROUPS, os.name == "posix")
        # On a POSIX machine that alone cannot tell the constant from a literal True: read the module as each platform would.
        for name, want in (("posix", True), ("nt", False)):
            with mock.patch.object(os, "name", name):
                spec = importlib.util.spec_from_file_location(f"quality_ratchet_as_{name}", STARTER)
                m = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(m)
            self.assertEqual(m.HAS_PROCESS_GROUPS, want, name)

    def test_stdlib_only(self):
        import ast
        tree = ast.parse(STARTER.read_text(encoding="utf-8"))
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names |= {a.name.split(".")[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom) and node.module:
                names.add(node.module.split(".")[0])
        # sys.stdlib_module_names is 3.10+; pin the allowed set so the test runs on older
        # interpreters too, which is where a stray third-party import would bite first.
        allowed = {"hashlib", "json", "os", "re", "subprocess", "sys", "tempfile", "datetime",
                   "shutil", "signal", "time",   # signal, time: a gate's command is stopped when the tool is (BL-107)
                   "pathlib"}   # the embedded layout-resolver block (BL-101 P2) imports it
        self.assertTrue(names <= allowed, names - allowed)

    def test_selftest_is_green(self):
        rc = subprocess.run([PY, str(STARTER), "--selftest"], capture_output=True, text=True)
        self.assertEqual(rc.returncode, 0, rc.stdout + rc.stderr)

    def test_selftest_observes_a_timeout_in_both_directions(self):
        # The selftest is what an adopter has instead of this suite: it must SEE a gate outlive its
        # budget and read unmeasured, for the ceiling and for the floor that used to read pass.
        p = subprocess.run([PY, str(STARTER), "--selftest"], capture_output=True, text=True)
        for label in ("a gate that outlives its timeout is UNMEASURED, never fail",
                      "a floor on an exit code is UNMEASURED on a timeout, never pass",
                      "a declared timeout_seconds outlasts the default budget"):
            self.assertRegex(p.stdout, r"PASS\x1b\[0m  " + label, p.stdout)

    def test_selftest_observes_a_command_being_stopped(self):
        # An adopter has the selftest and not this suite: it must SEE the command stopped, on a timeout
        # and on a signal to the tool (BL-107). Run only where the platform has process groups.
        p = subprocess.run([PY, str(STARTER), "--selftest"], capture_output=True, text=True)
        for label in ("a timed-out gate's command is stopped, not left running",
                      "SIGTERM to the tool stops a gate's command and the tool exits 143"):
            self.assertRegex(p.stdout, r"PASS\x1b\[0m  " + label, p.stdout)

    def test_the_seed_names_timeout_seconds_in_its_schema(self):
        seed = json.load(open(REPO / "starter-kit" / "quality-gates.json"))
        self.assertIn("`timeout_seconds`", seed["_gate_schema"])

    def test_the_seed_says_what_becomes_of_a_command_that_outlives_it(self):
        seed = json.load(open(REPO / "starter-kit" / "quality-gates.json"))
        self.assertIn("process group", seed["_gate_schema"])

    def test_seed_manifest_is_valid_and_empty(self):
        seed = json.load(open(REPO / "starter-kit" / "quality-gates.json"))
        self.assertEqual(seed["gates"], [], "the seed starts empty by decision (plan §8.4)")
        self.assertEqual(qr.config_defects(seed), [])
        # The example gate must itself be a valid gate, or it teaches a broken schema.
        self.assertEqual(qr.config_defects({"gates": [seed["_example"]]}), [])


if __name__ == "__main__":
    unittest.main()
