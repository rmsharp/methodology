#!/usr/bin/env python3
"""observe-run.py -- run a clone's `quality_ratchet.py --run` and keep each gate command's output.

Usage: python3 -B observe-run.py <clone-directory> <output-directory>

A stop-gap until the ratchet keeps a failing gate's output itself (docs/planning/ratchet-kept-output-plan.md).
It imports the clone's own quality_ratchet.py, wraps ONE function, run_gate_command, with a recorder that writes
the command's stdout and stderr to <output-directory>/NN.txt AFTER the command has ended, and then calls the
tool's own main() with --run. The command line, the budget, the measurement and the result are the tool's own;
the wrapper only reads. It is NOT a wrapper over `bin/tests.sh` (BL-92's detail records that such a wrapper
contaminates the suite's self-referential tests); it sits in the harness process, outside the suite.
Run it on a SCRATCH clone: it writes the clone's results file and nothing else there.
"""
import os
import sys
import time

sys.dont_write_bytecode = True
if len(sys.argv) != 3:
    sys.exit(__doc__)
CLONE, OUT = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, os.path.join(CLONE, "starter-kit"))
import quality_ratchet as qr  # noqa: E402

original = qr.run_gate_command
count = [0]


def observed(cmd, cwd, timeout):
    started = time.time()
    rc, out, err, timed_out = original(cmd, cwd, timeout)
    count[0] += 1
    with open(os.path.join(OUT, f"{count[0]:02d}.txt"), "w", encoding="utf-8") as f:
        f.write(f"command: {cmd}\nexit: {rc}  timed_out: {timed_out}  seconds: {time.time() - started:.0f}\n")
        f.write(f"stdout: {len(out.encode())} bytes, stderr: {len(err.encode())} bytes\n")
        f.write(f"=== stdout ===\n{out}\n=== stderr ===\n{err}\n")
    return rc, out, err, timed_out


qr.run_gate_command = observed
os.chdir(CLONE)
sys.argv = ["quality_ratchet.py", "--run"]
sys.exit(qr.main())
