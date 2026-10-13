#!/usr/bin/env python3
"""Mutation round over the BL-103 change in starter-kit/quality_ratchet.py (1.4.0).

Runs ONLY in the clone it is given (argv[1]); refuses a path that is not a `--no-local` clone under ~/.cache, so it
can never touch a working tree. Each mutant is one exact-string replacement in the tool. A mutant is KILLED by the unit
suite (tools/test_quality_ratchet.py) or by the tool's own --selftest, which is what an adopter has instead of the
suite; the two are reported separately, so a mutant only the suite kills is stated as such.

    python3 mutate-bl103.py ~/.cache/bl103-clone [--only M3,M7]
"""
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
    ("M1 a timeout reads as exit 127 again",
     '        return None, "", "", True', '        return 127, "", "", False'),
    ("M2 the timed_out flag is ignored",
     '    if timed_out:\n        res["note"]', '    if False:\n        res["note"]'),
    ("M3 the budget in the note loses its :g format",
     'f"timeout ({used:g} s)"', 'f"timeout ({used} s)"'),
    ("M4 the gate's own timeout_seconds is ignored",
     '    return g.get("timeout_seconds", default)', '    return default'),
    ("M5 a shared command takes the SMALLEST budget",
     'max(budgets.get(g["command"], 0), gate_budget(g, timeout))',
     'min(budgets.get(g["command"], 10**9), gate_budget(g, timeout))'),
    ("M6 run_gates computes the budgets and passes none",
     'memo, budgets.get(g.get("command"))) for g in gates]', 'memo, None) for g in gates]'),
    ("M7 a shared run's note names the gate's own budget, not the run's",
     '        rc, out, err, timed_out, used = memo[cmd]\n',
     '        rc, out, err, timed_out, used = memo[cmd]; used = gate_budget(g, timeout)\n'),
    ("M8 a bool is accepted as a budget",
     'isinstance(t, bool) or not isinstance(t, (int, float))', 'not isinstance(t, (int, float))'),
    ("M9 a budget of 0 is accepted",
     'not 0 < t < float("inf")', 'not 0 <= t < float("inf")'),
    ("M10 an infinite budget is accepted",
     'not 0 < t < float("inf")', 'not 0 < t'),
    ("M11 a float budget is refused",
     'not isinstance(t, (int, float))', 'not isinstance(t, int)'),
    ("M12 an explicit null or 0 is not looked at",
     '        if "timeout_seconds" in g:\n            t = g["timeout_seconds"]',
     '        if g.get("timeout_seconds"):\n            t = g["timeout_seconds"]'),
    ("M13 compare no longer warns on timeout_seconds",
     'for k in ("command", "extract", "timeout_seconds"):', 'for k in ("command", "extract"):'),
    ("M14 compare REFUSES a changed timeout_seconds",
     '            if og.get(k) != ng.get(k):\n                warnings.append(',
     '            if og.get(k) != ng.get(k):\n                (refusals if k == "timeout_seconds" else warnings).append('),
    ("M15 the command gets no timeout at all",
     'timeout=timeout, shell=True)', 'shell=True)'),
    ("M16 a command that cannot start reads as a timeout",
     '    except OSError as e:\n        return 127, "", str(e), False', '    except OSError as e:\n        return None, "", "", True'),
    ("M17 the default budget is 60 s, not 600",
     'DEFAULT_TIMEOUT = 600', 'DEFAULT_TIMEOUT = 60'),
    ("M18 only DECLARED budgets count toward a shared run (an undeclared gate's default is dropped)",
     '        if g.get("command"):\n            budgets[', '        if g.get("command") and "timeout_seconds" in g:\n            budgets['),
    ("M19 the note has no space before the unit",
     'f"timeout ({used:g} s)"', 'f"timeout ({used:g}s)"'),
    ("M20 a timed-out gate reports a measured value of 0",
     '        res["note"] = f"timeout ({used:g} s)"\n        return res',
     '        res["note"] = f"timeout ({used:g} s)"\n        res["measured"] = 0.0\n        return res'),
    ("M21 a timed-out gate reports status fail",
     '        res["note"] = f"timeout ({used:g} s)"\n        return res',
     '        res["note"] = f"timeout ({used:g} s)"\n        res["status"] = "fail"\n        return res'),
    ("M22 the memo keeps no budget, so a repeat reads the default",
     'memo[cmd] = (rc, out, err, timed_out, used)', 'memo[cmd] = (rc, out, err, timed_out, timeout)'),
    ("M23 compare ignores a timeout_seconds that was REMOVED (round 2: a behaviour no test named)",
     '            if og.get(k) != ng.get(k):\n                warnings.append(',
     '            if (og.get(k) != ng.get(k)) and ng.get(k) is not None:\n                warnings.append('),
]


def run_suite():
    r = subprocess.run([sys.executable, "-B", "tools/test_quality_ratchet.py"], cwd=clone, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def run_selftest():
    r = subprocess.run([sys.executable, "-B", "starter-kit/quality_ratchet.py", "--selftest"], cwd=clone,
                       capture_output=True, text=True)
    return r.returncode


rc, out = run_suite()
print("baseline suite: exit %d, %s" % (rc, [l for l in out.splitlines() if l.startswith("Ran ")][-1]))
assert rc == 0 and run_selftest() == 0, "the clone is not green before any mutant"
survived, suite_only = [], []
for name, old, new in MUTANTS:
    tag = name.split()[0]
    if only and tag not in only:
        continue
    assert orig.count(old) == 1, "%s: anchor matches %d times" % (name, orig.count(old))
    target.write_text(orig.replace(old, new, 1), encoding="utf-8")
    try:
        rc, out = run_suite()
        st = run_selftest()
    finally:
        target.write_text(orig, encoding="utf-8")
    fails = [l for l in out.splitlines() if l.startswith(("FAIL:", "ERROR:"))]
    verdict = ("KILLED by suite (%d red)" % len(fails)) if rc != 0 else "SURVIVED the suite"
    verdict += "; selftest " + ("kills it" if st != 0 else "passes it")
    print("%-82s %s" % (name, verdict), flush=True)
    if rc == 0:
        survived.append(name)
    elif st == 0:
        suite_only.append(name)
print("survivors of the suite: %d of %d run" % (len(survived), len([m for m in MUTANTS if not only or m[0].split()[0] in only])))
for s in survived:
    print("  survivor:", s)
print("killed by the suite but not the selftest: %d" % len(suite_only))
for s in suite_only:
    print("  suite-only:", s)
sys.exit(1 if survived else 0)
