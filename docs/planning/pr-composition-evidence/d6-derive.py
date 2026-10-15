#!/usr/bin/env python3
"""S323 D6 derivation, read-only: the candidate's three documents against the fork tip's, hunk by hunk.

    python3 d6-derive.py <fork> <fork-rev> <candidate-clone> [<candidate-rev>, default HEAD]

Reuses layer6c-build.py's hunks() and NOT_LAYOUT (imported, not copied). Prints, per file: the blobs, every
remaining hunk of the candidate -> tip diff with its class, and the hunks that carry the unmeasured-gate clause.
Writes nothing.
"""
import importlib.util
import re
import sys

sys.dont_write_bytecode = True
from pathlib import Path

fork, rev, cand = sys.argv[1], sys.argv[2], Path(sys.argv[3])
crev = sys.argv[4] if len(sys.argv) > 4 else "HEAD"
spec = importlib.util.spec_from_file_location(
    "b6c", Path(fork) / "docs/planning/pr-composition-evidence/layer6c-build.py")
b6c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b6c)

FILES = ["starter-kit/SESSION_RUNNER.md", "starter-kit/HANDOFFS.md", "HOW_TO_USE.md"]
TOKENS = re.compile(r"\bBL-\d+|\bS\d{2,3}\b|docs/planning|\bfork\b|\boperator\b|\bhis\b|Learning #\d+|"
                    r"upstream|\bplan\b|PR\d|P\d\b|issue #\d+", re.I)
tot_plus = tot_minus = 0
for f in FILES:
    cand_text = b6c.show(cand, crev, f)
    tip_text = b6c.show(fork, rev, f)
    hs = b6c.hunks(cand_text, tip_text)
    print("=" * 100)
    print("%s: candidate %s, tip %s, %d remaining hunk(s) candidate->tip" % (
        f, b6c.git(cand, "rev-parse", "--short=7", "%s:%s" % (crev, f)).strip(),
        b6c.blob(fork, rev, f), len(hs)))
    keys = b6c.NOT_LAYOUT.get(f, [])
    for i, h in enumerate(hs, 1):
        cls = b6c.layout_class(h)
        why = [w for k, w in keys if k in h.added_text()]
        unm = [w for w in why if w == b6c.UNMEASURED]
        print("-- hunk %d  old@%d  +%d/-%d  layout-class=%s  named-not-layout=%s%s" % (
            i, h.old_start, h.plus, h.minus, cls, bool(why), "  <== UNMEASURED" if unm else ""))
        if unm:
            tot_plus += h.plus
            tot_minus += h.minus
            for l in h.removed:
                print("   - " + l.rstrip("\n"))
            for l in h.added:
                print("   + " + l.rstrip("\n"))
            hits = sorted(set(m.group(0) for m in TOKENS.finditer(h.added_text())))
            print("   tokens in ADDED lines: %s" % (hits or "none"))
print("=" * 100)
print("UNMEASURED hunks total: +%d / -%d" % (tot_plus, tot_minus))
