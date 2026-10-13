#!/usr/bin/env python3
"""BL-107 research: how often does killpg raise on macOS, and does anything survive when it is swallowed?

Each round starts a shell that forks three sleeps, waits 0.3 s, SIGKILLs the shell's group, and looks for the
sleeps. Counts: rounds where killpg raised PermissionError / ProcessLookupError, and rounds with survivors.
"""
import collections
import os
import signal
import subprocess
import sys
import time

N = int(sys.argv[1])
MARK = "sleep 4301"


def survivors():
    out = subprocess.run(["ps", "-axo", "pid=,command="], capture_output=True, text=True).stdout
    return [int(l.split(None, 1)[0]) for l in out.splitlines() if l.strip().endswith(MARK)]


raised = collections.Counter()
leaked = 0
for i in range(N):
    p = subprocess.Popen(f"{MARK} & {MARK} & {MARK} & wait", shell=True, start_new_session=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(0.3)
    try:
        os.killpg(p.pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError) as e:
        raised[type(e).__name__] += 1
    p.wait()
    for f in (p.stdout, p.stderr):
        f.close()
    time.sleep(0.05)
    left = survivors()
    if left:
        leaked += 1
        for pid in left:
            try: os.kill(pid, signal.SIGKILL)
            except ProcessLookupError: pass
print(f"rounds={N}  killpg raised={dict(raised) or 'never'}  rounds with survivors={leaked}")
