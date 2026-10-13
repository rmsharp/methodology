#!/usr/bin/env python3
"""Aim signals at bl107-runner.py variants and report what survives. (BL-107 research, S306.)"""
import os
import signal
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RUNNER = os.path.join(HERE, "bl107-runner.py")
PY = sys.executable


def survivors(marker):
    out = subprocess.run(["ps", "-axo", "pid=,command="], capture_output=True, text=True).stdout
    found = []
    for line in out.splitlines():
        pid, _, cmd = line.strip().partition(" ")
        if cmd.strip().endswith(marker) and int(pid) != os.getpid():
            found.append(int(pid))
    return found


def scenario(variant, label, command, marker, timeout, how):
    p = subprocess.Popen([PY, RUNNER, variant, command, str(timeout)], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, text=True, start_new_session=True)
    t0 = time.time()
    if how == "group-INT":
        time.sleep(1.5); os.killpg(p.pid, signal.SIGINT)
    elif how == "group-HUP":
        time.sleep(1.5); os.killpg(p.pid, signal.SIGHUP)
    elif how == "pid-TERM":
        time.sleep(1.5); os.kill(p.pid, signal.SIGTERM)
    try:
        out, err = p.communicate(timeout=30)
    except subprocess.TimeoutExpired:
        p.kill(); out, err = p.communicate(); out += " [HARNESS: runner hung >30 s]"
    took = time.time() - t0
    time.sleep(0.5)                       # let a signalled child finish dying
    left = survivors(marker)
    for pid in left:
        try: os.kill(pid, signal.SIGKILL)
        except ProcessLookupError: pass
    rc = p.returncode
    print("%-4s %-30s runner rc=%-5s out=%-18s %5.1fs  survivors=%s" % (
        variant, label, rc, out.strip().splitlines()[-1] if out.strip() else "-", took, len(left)), flush=True)


if __name__ == "__main__":
    n = 4100
    rows = [
        ("timeout, plain command", "sleep {m}; exit 0", 1, "timeout"),
        ("timeout, ignores SIGTERM", "trap '' TERM; sleep {m}; exit 0", 1, "timeout"),
        ("Ctrl-C (SIGINT to the group)", "sleep {m}; exit 0", 60, "group-INT"),
        ("hangup (SIGHUP to the group)", "sleep {m}; exit 0", 60, "group-HUP"),
        ("kill <runner pid> (SIGTERM)", "sleep {m}; exit 0", 60, "pid-TERM"),
    ]
    for label, cmd, timeout, how in rows:
        for variant in ("v0", "v1", "v2", "v2t"):
            n += 1
            marker = "sleep %d" % n
            scenario(variant, label, cmd.format(m=n), marker, timeout, how)
        print()
