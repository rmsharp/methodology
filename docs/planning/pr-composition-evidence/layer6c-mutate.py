#!/usr/bin/env python3
"""Mutants aimed at the prose layer: put back the candidate's own text for ONE layout hunk, and ask what notices.

    python3 layer6c-mutate.py <source-repo> <source-rev> <clone> <parent-commit> [--e2e <hunk-number>]

<parent-commit> is the commit the layer sits on (the checkers' layer, 505541c): the candidate's own copy of each document.
<clone> is a scratch `--no-local` clone checked out at the layer's last commit (NEVER a working tree you care about: each
mutant is written into the clone and restored after, and an interrupted run leaves the clone dirty). The hunks are the
ones layer6c-build.py partitions: for every document, every layout hunk, in the builder's own order (`reference` and
`layout text`). A mutant is the layer's tree with that one hunk reverted to the candidate's text, so it is what the
layer would be if the hunk had been left out. The one gate that reads the prose is `bin/check-links --layout both` (the
command Test 10's second block runs): a mutant is KILLED when it exits non-zero, SURVIVED when it does not.

A survivor is not a defect of the layer: it is a line that no check in this tree reads. The record lists them by class,
because "the check is green" is only as strong as what the check reads. A control (no mutation) must be green first.

`--e2e N` runs the whole shell suite once with mutant N applied and prints the suite's own verdict lines for Test 10:
the end-to-end proof that the block turns the suite red (about 6 minutes), not the proxy.
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True   # the import below must not leave a __pycache__ in the evidence directory
spec =importlib.util.spec_from_file_location("layer6c_build", Path(__file__).with_name("layer6c-build.py"))
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


def run(clone, args):
    return subprocess.run(args, cwd=clone, capture_output=True, text=True)


def mutants(src, rev, clone, parent):
    """(number, file, class, hunk, mutant text, layer text) for every layout hunk of every document that differs."""
    out, n = [], 0
    for rel in b.documents(src, rev):
        new = b.show(src, rev, rel)
        if rel not in b.BLOBS:
            continue
        cand = b.show(clone, parent, rel)              # the layer's parent: the candidate's own copy
        layer = (Path(clone) / rel).read_text(encoding="utf-8")
        layout, _ = b.partition(rel, cand, new)
        if b.apply(cand, [h for h, _ in layout]) != layer:
            raise SystemExit("refused: %s in the clone is not the builder's output; is the clone at the layer's last commit?" % rel)
        for i, (h, cls) in enumerate(layout):
            n += 1
            rest = [x for j, x in enumerate(layout) if j != i]
            out.append((n, rel, cls, h, b.apply(cand, [x for x, _ in rest]), layer))
    return out


def main():
    src, rev, clone, parent = sys.argv[1], sys.argv[2], Path(sys.argv[3]), sys.argv[4]
    e2e = int(sys.argv[sys.argv.index("--e2e") + 1]) if "--e2e" in sys.argv else None
    if run(clone, ["git", "status", "--short"]).stdout.strip():
        raise SystemExit("refused: the clone is dirty")
    ms = mutants(src, rev, clone, parent)
    control = run(clone, [sys.executable, "-B", "bin/check-links", "--layout", "both"]).returncode
    print("control (no mutation): bin/check-links --layout both exit %d; %d mutants (one per layout hunk)" % (control, len(ms)))
    if control:
        raise SystemExit("refused: the control is not green")
    tally = {}
    for n, rel, cls, h, text, layer in ms:
        p = clone / rel
        if e2e is not None and n != e2e:
            continue
        p.write_text(text, encoding="utf-8")
        try:
            if e2e is not None:
                print("mutant %d: %s @%d (%s) applied; running the shell suite (about 6 minutes)" % (n, rel, h.old_start, cls))
                r = run(clone, ["bash", "bin/tests.sh"])
                keep = [l for l in r.stdout.splitlines() if "check-links" in l or l.startswith("== Summary") or l.startswith("== Test 10")]
                print("\n".join("   " + l[:170] for l in keep))
                print("suite exit %d" % r.returncode)
                return 0
            rc = run(clone, [sys.executable, "-B", "bin/check-links", "--layout", "both"]).returncode
        finally:
            p.write_text(layer, encoding="utf-8")
        verdict = "KILLED" if rc else "SURVIVED"
        t = tally.setdefault(cls, [0, 0])
        t[0 if rc else 1] += 1
        print("%3d %-58s @%-4d %-11s %-8s | %s" % (n, rel, h.old_start, cls, verdict, h.removed_text().strip()[:70].replace("\n", " ")))
    for cls, (k, s) in sorted(tally.items()):
        print("%-12s %2d killed, %2d survived" % (cls, k, s))
    status = run(clone, ["git", "status", "--short"]).stdout.strip()
    print("clone clean afterwards: %s" % ("yes" if not status else "NO: " + status))
    return 0


if __name__ == "__main__":
    sys.exit(main())
