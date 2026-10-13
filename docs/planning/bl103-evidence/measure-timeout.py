#!/usr/bin/env python3
"""What does a quality_ratchet.py do with a gate that outlives its budget? (BL-103, S305.)

    python3 measure-timeout.py <path to a quality_ratchet.py>

Builds three gates in a throwaway git repository, each a command that sleeps longer than the 1 s budget it is
given, and prints how the tool reads each, then which of the sleeping commands are still running when run_gates
has returned (BL-107). Run it against the 1.3.0 tool (`git show c80c5b5:starter-kit/quality_ratchet.py`) and the
1.4.0 tool (`starter-kit/quality_ratchet.py`); the output of both is in measure-timeout-output.txt.

The three shapes are the three ways a gate reads a number: an exit code against a ceiling (`max 0`, "must exit
0"), an exit code against a floor (`min 100`), and an `extract` over the command's output.
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time

tool = os.path.abspath(sys.argv[1])
spec = importlib.util.spec_from_file_location("qr", tool)
qr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qr)

cfg = {"version": 1, "gates": [
    {"name": "exit-code-ceiling", "direction": "max", "threshold": 0, "command": "sleep 6; exit 0"},
    {"name": "exit-code-floor", "direction": "min", "threshold": 100, "command": "sleep 7; exit 0"},
    {"name": "extract", "direction": "min", "threshold": 1, "command": "sleep 8; echo 5", "extract": r"(\d+)"},
]}
with tempfile.TemporaryDirectory() as d:
    subprocess.run(["git", "init", "-q", d], check=True)
    t0 = time.time()
    snap = qr.run_gates(d, cfg, timeout=1)
    took = time.time() - t0
    print("tool %s, version %s; budget 1 s; run_gates returned after %.1f s" % (tool, qr.VERSION, took))
    print("%-20s %-11s %-9s %s" % ("gate", "status", "measured", "note"))
    for g in snap["gates"]:
        print("%-20s %-11s %-9s %s" % (g["name"], g["status"], g["measured"], repr(g["note"])))
    print("summary:", json.dumps(snap["summary"], sort_keys=True))
    ps = subprocess.run(["ps", "-axo", "pid,etime,command"], capture_output=True, text=True).stdout
    left = [l.split(None, 2)[2] for l in ps.splitlines() if l.rstrip().endswith(("sleep 6", "sleep 7", "sleep 8"))]
    print("commands still running after run_gates returned:", left if left else "none")
