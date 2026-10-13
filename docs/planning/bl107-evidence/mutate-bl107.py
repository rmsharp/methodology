#!/usr/bin/env python3
"""Mutation round over the BL-107 change in starter-kit/quality_ratchet.py (1.5.0).

Runs ONLY in the clone it is given (argv[1]); refuses a path that is not a `--no-local` clone under ~/.cache, so it
can never touch a working tree (a runner pointed at `.` discards uncommitted work). Each mutant is one exact-string
replacement in the tool. A mutant is KILLED by the unit suite (tools/test_quality_ratchet.py, run fail-fast: the
verdict names the FIRST failing test) or by the tool's own --selftest, which is what an adopter has instead of the
suite; the two are reported separately, so a mutant only the suite kills is stated as such. A suite that does not
finish in 300 s counts as killed (hung) and the long `sleep 600` its tests start is cleaned up after every mutant.

    python3 mutate-bl107.py ~/.cache/bl107-clone [--only M3,M7]
"""
import os
import signal
import subprocess
import sys
from pathlib import Path

clone = Path(sys.argv[1]).resolve()
cache = (Path.home() / ".cache").resolve()
assert cache in clone.parents, "refusing: %s is not under ~/.cache" % clone
assert (clone / ".git").is_dir() and (clone / "starter-kit" / "quality_ratchet.py").is_file()
only = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None
target = clone / "starter-kit" / "quality_ratchet.py"
orig = target.read_text(encoding="utf-8")

MUTANTS = [
    ("M1 the command gets no session of its own",
     'shell=True, start_new_session=True)', 'shell=True)'),
    ("M2 the group is never signalled",
     '        os.killpg(proc.pid, signal.SIGKILL)\n    except OSError:', '        pass\n    except OSError:'),
    ("M3 SIGTERM, not SIGKILL, to the group",
     'os.killpg(proc.pid, signal.SIGKILL)', 'os.killpg(proc.pid, signal.SIGTERM)'),
    ("M4 the shell is not killed directly after the group call",
     '    try:\n        proc.kill()\n    except OSError:\n        pass\n    proc.wait()\n', '    proc.wait()\n'),
    ("M5 a refused killpg other than ProcessLookupError escapes",
     '    except OSError:\n        pass\n    try:\n        proc.kill()', '    except ProcessLookupError:\n        pass\n    try:\n        proc.kill()'),
    ("M6 the shell is never reaped",
     '        pass\n    proc.wait()\n', '        pass\n'),
    ("M7 a timeout does not stop the group",
     '        except subprocess.TimeoutExpired:\n            _stop_group(proc)\n            return None, "", "", True',
     '        except subprocess.TimeoutExpired:\n            return None, "", "", True'),
    ("M8 an exception out of the wait does not stop the group",
     '    except BaseException:\n        if proc is not None:\n            _stop_group(proc)\n        raise',
     '    except BaseException:\n        raise'),
    ("M9 KeyboardInterrupt and SystemExit are not caught",
     '    except BaseException:\n        if proc', '    except Exception:\n        if proc'),
    ("M10 an OSError while waiting does not stop the group",
     '    except OSError as e:\n        if proc is not None:\n            _stop_group(proc)\n        return 127',
     '    except OSError as e:\n        return 127'),
    ("M11 the signal handlers are not put back",
     '    finally:\n        restore()\n', '    finally:\n        pass\n'),
    ("M12 a hangup the caller ignores is overridden",
     '        if signal.getsignal(s) == signal.SIG_IGN:\n            continue\n', ''),
    ("M13 a call off the main thread raises",
     '        except ValueError:\n            break\n', '        except ZeroDivisionError:\n            break\n'),
    ("M14 the exit status is the bare signal number",
     'raise SystemExit(128 + signum)', 'raise SystemExit(signum)'),
    ("M15 SIGHUP is not handled",
     '    for s in (signal.SIGHUP, signal.SIGTERM):', '    for s in (signal.SIGTERM,):'),
    ("M16 SIGTERM is not handled",
     '    for s in (signal.SIGHUP, signal.SIGTERM):', '    for s in (signal.SIGHUP,):'),
    ("M17 a command that finished has its group killed too",
     '        return proc.returncode, out, err, False\n    except OSError as e:',
     '        _stop_group(proc)\n        return proc.returncode, out, err, False\n    except OSError as e:'),
    ("M18 stdout is not captured",
     'stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,\n                                shell=True',
     'stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True,\n                                shell=True'),
    ("M19 output comes back as bytes",
     'stderr=subprocess.PIPE, text=True,\n                                shell=True, start_new_session=True)',
     'stderr=subprocess.PIPE,\n                                shell=True, start_new_session=True)'),
    ("M20 the working directory is ignored",
     'subprocess.Popen(cmd, cwd=cwd,', 'subprocess.Popen(cmd,'),
    ("M21 HAS_PROCESS_GROUPS ignores the platform",
     'HAS_PROCESS_GROUPS = os.name == "posix"', 'HAS_PROCESS_GROUPS = True'),
    ("M22 the pipes are not closed",
     '            for f in (proc.stdout, proc.stderr):\n                f.close()', '            pass'),
    ("M23 a handler the caller installed is replaced by the default on the way out",
     'signal.signal(s, previous if previous is not None else signal.SIG_DFL)', 'signal.signal(s, signal.SIG_DFL)'),
    ("M24 SIGINT is handled like SIGHUP (Ctrl-C stops raising KeyboardInterrupt)",
     '    for s in (signal.SIGHUP, signal.SIGTERM):', '    for s in (signal.SIGHUP, signal.SIGTERM, signal.SIGINT):'),
    ("M25 the platform switch is inverted",
     '    if not HAS_PROCESS_GROUPS:\n        try:', '    if HAS_PROCESS_GROUPS:\n        try:'),
    # --- round 2: aimed at behaviours no test named when round 1 was written (the survivors of round 1 are re-run by tag) ---
    ("R1 only the first replaced handler is put back",
     '        for s, previous in saved:\n', '        for s, previous in saved[:1]:\n'),
    ("R2 an OSError while waiting reports the exception's class, not its message",
     '            _stop_group(proc)\n        return 127, "", str(e), False', '            _stop_group(proc)\n        return 127, "", type(e).__name__, False'),
    ("R3 a hangup or SIGTERM raises KeyboardInterrupt instead of SystemExit",
     'raise SystemExit(128 + signum)', 'raise KeyboardInterrupt'),
    ("M26 the no-process-group path reports a timeout as exit 127",
     '        except subprocess.TimeoutExpired:\n            return None, "", "", True\n        except OSError as e:\n            return 127, "", str(e), False\n        return p.returncode',
     '        except subprocess.TimeoutExpired:\n            return 127, "", "", False\n        except OSError as e:\n            return 127, "", str(e), False\n        return p.returncode'),
]


def strays():
    out = subprocess.run(["ps", "-axo", "pid=,command="], capture_output=True, text=True).stdout
    return [int(l.split(None, 1)[0]) for l in out.splitlines() if l.strip().endswith(" sleep 600") or l.strip() == "sleep 600"]


def clean():
    for pid in strays():
        try:
            os.kill(pid, signal.SIGKILL)
        except OSError:
            pass


def run_suite():
    try:
        r = subprocess.run([sys.executable, "-B", "tools/test_quality_ratchet.py", "-f"], cwd=clone,
                           capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        return 99, "hung: no result in 300 s"
    return r.returncode, r.stdout + r.stderr


def run_selftest():
    try:
        r = subprocess.run([sys.executable, "-B", "starter-kit/quality_ratchet.py", "--selftest"], cwd=clone,
                           capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        return 99
    return r.returncode


rc, out = run_suite()
print("baseline suite: exit %d, %s" % (rc, [l for l in out.splitlines() if l.startswith("Ran ")][-1]))
assert rc == 0 and run_selftest() == 0, "the clone is not green before any mutant"
survived, suite_only = [], []
ran = 0
for name, old, new in MUTANTS:
    tag = name.split()[0]
    if only and tag not in only:
        continue
    ran += 1
    assert orig.count(old) == 1, "%s: anchor matches %d times" % (name, orig.count(old))
    target.write_text(orig.replace(old, new, 1), encoding="utf-8")
    try:
        rc, out = run_suite()
        clean()
        st = run_selftest()
        clean()
    finally:
        target.write_text(orig, encoding="utf-8")
    first = [l for l in out.splitlines() if l.startswith(("FAIL:", "ERROR:"))]
    if rc == 0:
        verdict = "SURVIVED the suite"
    elif rc == 99:
        verdict = "KILLED by the suite (hung)"
    else:
        verdict = "KILLED by the suite (first: %s)" % (first[0].split()[1] if first else "?")
    verdict += "; selftest " + ("kills it" if st != 0 else "passes it")
    print("%-84s %s" % (name, verdict), flush=True)
    if rc == 0:
        survived.append(name)
    elif st == 0:
        suite_only.append(name)
print("survivors of the suite: %d of %d run" % (len(survived), ran))
for s in survived:
    print("  survivor:", s)
print("killed by the suite but not the selftest: %d" % len(suite_only))
for s in suite_only:
    print("  suite-only:", s)
sys.exit(1 if survived else 0)
