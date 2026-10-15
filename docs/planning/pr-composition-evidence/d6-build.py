#!/usr/bin/env python3
"""S323 D6 builder: apply the unmeasured-gate hunks (plan 7 D6) to the candidate's documents, as he decided them.

Two decisions of the S323 Phase 2 picker (2026-10-15), each recorded in the record:
  runner   starter-kit/SESSION_RUNNER.md's 3E sentence is NOT carried: the runner already reads over its read-set
           ceiling on the candidate (context_budget.py --status), and the sentence adds 224 B to it.
  lint     starter-kit/HANDOFFS.md's hunk is carried without its last changed line: the fork's text says the checker lints
           "that token and clause" and the candidate's bin/check-handoff has no clause lint; upstream's own sentence stays.

    python3 d6-build.py <fork> <fork-rev> <candidate-clone>            dry run: prints, writes nothing
    python3 d6-build.py <fork> <fork-rev> <candidate-clone> --write    writes the three files (does NOT commit)

Reuses layer6c-build.py (hunks, apply, NOT_LAYOUT, UNMEASURED). Refuses unless every premise holds: the fork tip's blobs
are the ones layer6c-build.py recorded, the candidate's are the post-layer ones, each file has exactly one UNMEASURED
hunk, and after the apply what is left of the difference to the tip is exactly the other NOT_LAYOUT hunks.
"""
import importlib.util
import sys

sys.dont_write_bytecode = True
from pathlib import Path

fork, rev, cand = sys.argv[1], sys.argv[2], Path(sys.argv[3])
write = "--write" in sys.argv[4:]
spec = importlib.util.spec_from_file_location("b6c", Path(fork) / "docs/planning/pr-composition-evidence/layer6c-build.py")
b6c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b6c)

CAND_BLOBS = {"starter-kit/HANDOFFS.md": "4a3b1a1", "HOW_TO_USE.md": "a28fcc9"}  # the runner is read, never written
RUNNER = ("starter-kit/SESSION_RUNNER.md", "3d09a4a")
LINT_FORK = "`bin/check-handoff` lints the **newest** receipt for that token and clause when a manifest with gates is present;\n"
LINT_UPSTREAM = "`bin/check-handoff` lints the **newest** receipt for that token when a manifest with gates is present;\n"
got = b6c.git(cand, "rev-parse", "--short=7", "HEAD:" + RUNNER[0]).strip()
if got != RUNNER[1]:
    raise SystemExit("refused: %s: the candidate's blob is %s, not %s" % (RUNNER[0], got, RUNNER[1]))
out = {}
for f, cb in CAND_BLOBS.items():
    got = b6c.git(cand, "rev-parse", "--short=7", "HEAD:" + f).strip()
    if got != cb:
        raise SystemExit("refused: %s: the candidate's blob is %s, not %s" % (f, got, cb))
    tb = b6c.blob(fork, rev, f)
    if tb != b6c.BLOBS[f][1]:
        raise SystemExit("refused: %s: the fork's blob is %s, not %s" % (f, tb, b6c.BLOBS[f][1]))
    old, tip = (cand / f).read_text(encoding="utf-8"), b6c.show(fork, rev, f)
    keys = [k for k, w in b6c.NOT_LAYOUT[f] if w == b6c.UNMEASURED]
    hs = b6c.hunks(old, tip)
    mine = [h for h in hs if any(k in h.added_text() for k in keys)]
    if len(mine) != 1:
        raise SystemExit("refused: %s: expected exactly 1 unmeasured hunk, found %d" % (f, len(mine)))
    if f == "starter-kit/HANDOFFS.md":
        h = mine[0]  # keep the four added rule lines, put upstream's checker sentence back on the last
        if h.added[-1] != LINT_FORK or h.removed[-1] != LINT_UPSTREAM or len(h.removed) != 2 or len(h.added) != 5:
            raise SystemExit("refused: %s: the hunk is not the shape the lint decision was taken on" % f)
        mine = [b6c.Hunk(h.old_start, 1, h.removed[:1], h.added[:4])]
    new = b6c.apply(old, mine)
    left = b6c.hunks(new, tip)
    others = [h for h in hs if not any(k in h.added_text() for k in keys)]
    if f == "starter-kit/HANDOFFS.md":
        others = [b6c.Hunk(0, 1, [LINT_UPSTREAM], [LINT_FORK])]
    if len(left) != len(others) or [h.added_text() for h in left] != [h.added_text() for h in others]:  # the rest is as decided
        raise SystemExit("refused: %s: what is left to the tip is not exactly the other hunks" % f)
    out[f] = new
    print("%-32s +%d/-%d hunk, %d B -> %d B (%+d B), %d other non-layout hunk(s) remain to the tip" % (
        f, mine[0].plus, mine[0].minus, len(old.encode()), len(new.encode()),
        len(new.encode()) - len(old.encode()), len(left)))
if write:
    for f, t in out.items():
        (cand / f).write_text(t, encoding="utf-8")
    print("written (not committed)")
else:
    print("dry run: nothing written")
