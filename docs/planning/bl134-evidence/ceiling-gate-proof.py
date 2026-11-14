#!/usr/bin/env python3
"""BL-134 (S449): prove the `seed-handoffs-size` gate before it is declared, and again after.

What it checks, in order (exit 0 only when every expectation reads as stated; 1 otherwise):

 0. The gate is DECLARED in the manifest (.quality-gates.json) with direction `max`, threshold 16384 and a
    command that reads starter-kit/HANDOFFS.md. Run BEFORE the gate is added, this is the RED: nothing in the
    manifest caps the seed, so the harness says so and stops.
 1. The ratchet's own measure_gate (quality_ratchet.py, imported, not re-implemented) reads the gate on a
    scratch tree whose starter-kit/HANDOFFS.md is: the real seed (pass), the real seed grown to exactly the
    ceiling (pass: the boundary), one byte over (fail: the flip), 20,000 B (fail), and absent (unmeasured,
    never pass: the digits-only extract matches nothing).
 2. The reason the number is 16,384: the pipeline at bin/tests.sh:5533, `tr -s '\\n ' '  ' < seed`, run into
    a reader that is ALREADY WAITING (piece-reader.py; a reader that starts with its producer read 0 of 600 on
    a known positive at S448). A seed at the ceiling reaches the reader in ONE read; a seed of 32,768 B reaches
    it in TWO, which is the positive control: the instrument can see a split. Just over the edge a split can be
    HIDDEN when the second write lands before the reader's read (a 16,385 B stream read as one piece 10 of 10
    at S448; 18,000 B split 10 of 10 on two runs and 8 of 10 on a third, S449), so the control sits where the
    second write cannot land first: a 16 KiB pipe is full after the first write. The edge itself is `tr`'s
    16,384 B write size, read from the large sizes (32,768 B: [16384, rest]; 65,536 B: four 16,384 B reads).

Usage: python3 ceiling-gate-proof.py [REPO_ROOT]     (default: the repository this file sits in; about 20 s)
Python 3 standard library only. Writes only inside a temporary directory it removes.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True  # importing quality_ratchet must not leave starter-kit/__pycache__ behind

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
GATE = "seed-handoffs-size"
CEILING = 16384
SEED = os.path.join(ROOT, "starter-kit", "HANDOFFS.md")
READER = os.path.join(HERE, "piece-reader.py")
RUNS = 10

failed = []


def say(ok, text):
    print(("  ok     " if ok else "  WRONG  ") + text)
    if not ok:
        failed.append(text)


def load_ratchet():
    spec = importlib.util.spec_from_file_location("quality_ratchet_under_proof", os.path.join(ROOT, "starter-kit", "quality_ratchet.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def grown(seed_bytes, size):
    """The real seed text padded with single-spaced words (which `tr -s` cannot squeeze away) to exactly `size` bytes."""
    return seed_bytes[:size] if size <= len(seed_bytes) else (seed_bytes + b"word " * (size // 5 + 2))[:size]


def pieces(path):
    """The distinct read patterns, with counts, of `tr -s` over `path` into a reader that is already waiting."""
    seen = {}
    for _ in range(RUNS):
        cmd = "{ sleep 0.06; tr -s '\\n ' '  ' < %s; } | python3 -I %s" % (path, READER)
        out = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True).stdout.strip()
        seen[out] = seen.get(out, 0) + 1
    return seen


print("== 0. the gate is declared")
cfg = json.load(open(os.path.join(ROOT, ".quality-gates.json")))
gate = next((g for g in cfg["gates"] if g["name"] == GATE), None)
capping = [g["name"] for g in cfg["gates"] if "starter-kit/HANDOFFS.md" in (g.get("command") or "")]
if gate is None:
    print("  RED    no gate named %r is declared; gates whose command reads starter-kit/HANDOFFS.md: %s" % (GATE, capping or "none"))
    print("         so nothing caps the seed that bin/tests.sh:5533 feeds to `tr`. Declare the gate, then re-run.")
    sys.exit(1)
say(gate["direction"] == "max", "direction is 'max' (a ceiling): %r" % gate["direction"])
say(float(gate["threshold"]) == CEILING, "threshold is %d: %r" % (CEILING, gate["threshold"]))
say("starter-kit/HANDOFFS.md" in gate.get("command", ""), "the command reads starter-kit/HANDOFFS.md: %r" % gate.get("command"))

print("== 1. the ratchet's own measure_gate on scratch trees")
qr = load_ratchet()
seed = open(SEED, "rb").read()
tmp = tempfile.mkdtemp(prefix="bl134-ceiling-")
try:
    cases = [("the real seed (%d B)" % len(seed), len(seed), "pass"),
             ("grown to the ceiling, %d B" % CEILING, CEILING, "pass"),
             ("one byte over, %d B" % (CEILING + 1), CEILING + 1, "fail"),
             ("20,000 B", 20000, "fail"),
             ("absent", None, "unmeasured")]
    for label, size, want in cases:
        root = os.path.join(tmp, "case-%s" % (size if size is not None else "absent"))
        os.makedirs(os.path.join(root, "starter-kit"))
        if size is not None:
            open(os.path.join(root, "starter-kit", "HANDOFFS.md"), "wb").write(grown(seed, size))
        res = qr.measure_gate(root, gate, 30)
        say(res["status"] == want, "%-34s -> %-10s measured %s%s (wanted %s)" % (
            label, res["status"], res["measured"], (" note: " + res["note"]) if res["note"] else "", want))

    print("== 2. why 16,384: `tr -s` into a waiting reader (%d runs each; the piece sizes are the reads)" % RUNS)
    for label, size, want_n in (("the ceiling, %d B" % CEILING, CEILING, 1),
                                ("32,768 B (the positive control)", 32768, 2)):
        p = os.path.join(tmp, "tr-%d.in" % size)
        open(p, "wb").write(grown(seed, size))
        seen = pieces(p)
        shown = " ".join("[%s]x%d" % (k, v) for k, v in sorted(seen.items()))
        every = all(len(k.split(",")) == want_n for k in seen)
        say(every, "%-34s %s (wanted %d read%s in every run)" % (label, shown, want_n, "" if want_n == 1 else "s"))
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("== result: %s" % ("every expectation held" if not failed else "%d expectation(s) did NOT hold" % len(failed)))
sys.exit(1 if failed else 0)
