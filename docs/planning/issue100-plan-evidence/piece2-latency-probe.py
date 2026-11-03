#!/usr/bin/env python3
"""Piece 2 (S415): how long does `git ls-remote --tags --refs origin` take against a real remote?

    python3 docs/planning/issue100-plan-evidence/piece2-latency-probe.py <checkout-with-an-https-origin> [runs]

Read-only (one network read per run). It times git's default protocol (v2: two round trips)
against `-c protocol.version=0` (one round trip), `runs` times each, with GIT_TERMINAL_PROMPT=0.
The plan said only "a hard timeout of a few seconds"; this is the measurement that picked the
number. It is a measurement of ONE machine and ONE network on one afternoon, not a property of git.
"""
import os, statistics, subprocess, sys, time

repo = sys.argv[1]
runs = int(sys.argv[2]) if len(sys.argv) > 2 else 8
env = dict(os.environ, GIT_TERMINAL_PROMPT="0")


def once(extra):
    began = time.monotonic()
    p = subprocess.run(["git", "-C", repo, *extra, "ls-remote", "--tags", "--refs", "origin"],
                       capture_output=True, text=True, env=env, timeout=60)
    return time.monotonic() - began, len(p.stdout.splitlines())


for label, extra in (("default (protocol v2)", []), ("protocol v0", ["-c", "protocol.version=0"])):
    xs = [once(extra)[0] for _ in range(runs)]
    print(f"{label:24s} n={runs}  min {min(xs):.1f}  median {statistics.median(xs):.1f}  max {max(xs):.1f}"
          f"   all: {' '.join(f'{x:.1f}' for x in xs)}")
