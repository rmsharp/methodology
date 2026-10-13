#!/usr/bin/env python3
"""One variant of run_gate_command, run as its own process so a signal can be aimed at it.

    bl107-runner.py <variant> <command> <timeout>

v0  = quality_ratchet.py 1.4.0 (subprocess.run, shell=True, timeout)
v1  = a new session per command, killpg on a timeout, NOTHING else
v2  = v1 + killpg on any exception + SIGHUP/SIGTERM turned into SystemExit while the command runs
v2t = v2 but SIGTERM first, SIGKILL after a 2 s grace
Prints the outcome (a timeout or an exit code) when it gets that far.
"""
import os
import signal
import subprocess
import sys
import time


def v0(cmd, timeout):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, shell=True)
    except subprocess.TimeoutExpired:
        return "timeout"
    return "rc=%s" % p.returncode


def _kill_group(pgid, grace):
    try:
        if grace:
            os.killpg(pgid, signal.SIGTERM)
            end = time.time() + grace
            while time.time() < end:
                try:
                    os.killpg(pgid, 0)
                except ProcessLookupError:
                    return
                time.sleep(0.05)
        os.killpg(pgid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def v1(cmd, timeout, cleanup=False, grace=0):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, start_new_session=True)
    old = {}
    if cleanup:
        def bail(signum, frame):
            raise SystemExit(128 + signum)
        for s in (signal.SIGHUP, signal.SIGTERM):
            old[s] = signal.signal(s, bail)
    try:
        try:
            proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            _kill_group(proc.pid, grace)
            proc.wait()
            return "timeout"
        return "rc=%s" % proc.returncode
    except BaseException:
        if cleanup:
            _kill_group(proc.pid, grace)
            proc.wait()
        raise
    finally:
        for s, h in old.items():
            signal.signal(s, h)
        for f in (proc.stdout, proc.stderr):
            f.close()


VARIANTS = {
    "v0": v0,
    "v1": v1,
    "v2": lambda c, t: v1(c, t, cleanup=True),
    "v2t": lambda c, t: v1(c, t, cleanup=True, grace=2),
}

if __name__ == "__main__":
    variant, cmd, timeout = sys.argv[1], sys.argv[2], float(sys.argv[3])
    try:
        print(VARIANTS[variant](cmd, timeout), flush=True)
    except KeyboardInterrupt:
        print("KeyboardInterrupt", flush=True)
        sys.exit(130)
