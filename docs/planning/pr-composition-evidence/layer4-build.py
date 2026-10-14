#!/usr/bin/env python3
"""Build PR2 Part 2's layer 4 (the context-budget gate 1.4.0: it finds its config, its history file and its tool at the root or under methodology/) in a candidate clone.

    python3 layer4-build.py <source-repo> <source-rev> <candidate-clone> [--base-rev REV] [--budget-count N]

Reads each file from <source-rev> of <source-repo> (git show, never the working tree) and writes the
layer into <candidate-clone>, which must be on a clean checkout of `pr2/candidate` at layer 3's commit.
It does NOT commit. Every edit is a string replacement asserted to match exactly once, so a drifted
base refuses instead of half-applying. The layer is:

  verbatim from <source-rev>          starter-kit/context_budget.py, tools/test_context_budget.py
  the candidate's file, two appends   tools/test_layout_resolver.py   (COPIES and RESOLVED: the budget gate is the third tool that carries the block)
  the candidate's file, one floor     .quality-gates.json   (--budget-count: context-budget-unit-tests, 148 to N)

<source-rev> is the fork's tip. The candidate's two files are upstream's (version 1.3.1) and equal the fork's blobs at
--base-rev (default `517ebf6^`, the parent of the first of three fork commits that touch them: `517ebf6`, the tests
written red, `4959e7a`, 1.4.0, and `c0d1e09`, one more test; `git log --ancestry-path --full-history 517ebf6^..<rev> -- <the
two files>` lists exactly those three, and so does the first-parent walk: the plain `5ff62ea..<rev>` walk lists 19, the
older ones being history the base already contains). What the builder PROVES before it writes is the base: it refuses
unless each of the candidate's two files equals that revision's blob, byte for byte, and unless the candidate's
`tools/layout_resolver.py` and `tools/layout_fixtures.py` equal <source-rev>'s (so the block the new tool embeds is the
module's, which the layout suite then asserts, and the fixtures the new tests build trees from are the fork's). Nothing
else in the candidate changes: `git diff c8b9ddd <rev> -- bin/tests.sh` adds no line that cites the budget gate, and the
shell suite's existing blocks that run it (Test 35's selftest, install-hook, --status and sync lines) are the same text
at the fork's tip.

Run it twice: once without --budget-count (writes the verbatim files and the layout-suite edit, all computed before
the first write, so a refusal leaves the clone untouched), run `python3 tools/test_context_budget.py` in the clone to
read the count, then once more with --budget-count N, which writes only the gates file.
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

VERBATIM = ("starter-kit/context_budget.py", "tools/test_context_budget.py")
BASED = VERBATIM              # the files the candidate already has, which must equal the base revision's blobs
SAME_AS_SOURCE = ("tools/layout_resolver.py", "tools/layout_fixtures.py")


def show(src, rev, path):
    return subprocess.run(["git", "-C", str(src), "show", "%s:%s" % (rev, path)], check=True,
                          capture_output=True).stdout.decode("utf-8")


def mode_of(src, rev, path):
    out = subprocess.run(["git", "-C", str(src), "ls-tree", rev, path], check=True,
                         capture_output=True).stdout.decode("utf-8")
    return 0o755 if out.startswith("100755") else 0o644


def write(dst, rel, text, mode=None):
    p = Path(dst) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    if mode:
        os.chmod(p, mode)


def once(text, old, new, what):
    if text.count(old) != 1:
        raise SystemExit("refused: %s: expected exactly 1 match, found %d" % (what, text.count(old)))
    return text.replace(old, new)


def edit_test_layout(text):
    text = once(text, '    COPIES = ("starter-kit/methodology_trim.py", "starter-kit/quality_ratchet.py")   # the gate layer and the trimmer; each later layer appends the tools it carries\n',
                '    COPIES = ("starter-kit/context_budget.py", "starter-kit/methodology_trim.py", "starter-kit/quality_ratchet.py")   # the gate layer, the trimmer and the budget gate; each later layer appends the tools it carries\n',
                "COPIES")
    return once(text, '                "starter-kit/methodology_trim.py")   # the trimmer; each later layer appends the tools it resolves\n',
                '                "starter-kit/methodology_trim.py",   # the trimmer\n'
                '                "starter-kit/context_budget.py")   # the budget gate; each later layer appends the tools it resolves\n',
                "RESOLVED")


def edit_floor(text, name, old, new):
    pat = re.compile(r'("name": "%s",\n\s+"direction": "min",\n\s+"threshold": )%d,' % (re.escape(name), old))
    if len(pat.findall(text)) != 1:
        raise SystemExit("refused: gate %s at %d: expected exactly 1 match" % (name, old))
    return pat.sub(lambda m: m.group(1) + "%d," % new, text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("rev")
    ap.add_argument("dst")
    ap.add_argument("--base-rev", default="517ebf6^")
    ap.add_argument("--budget-count", type=int, help="the unit-test count the clone measured")
    args = ap.parse_args()
    dst, rev = Path(args.dst), args.rev

    if args.budget_count is None:
        # prove the base first: each file the layer replaces must be exactly the revision the candidate took it from
        for rel in BASED:
            have = (dst / rel).read_text(encoding="utf-8")
            if have != show(args.src, args.base_rev, rel):
                raise SystemExit("refused: %s in the candidate is not %s's blob; this builder's premise (the whole difference "
                                 "to <rev> is 1.4.0 and its tests) does not hold" % (rel, args.base_rev))
        for rel in SAME_AS_SOURCE:
            if (dst / rel).read_text(encoding="utf-8") != show(args.src, rev, rel):
                raise SystemExit("refused: the candidate's %s is not %s's, so the budget gate's embedded block or its test trees would not be the fork's" % (rel, rev))
        files = [(rel, show(args.src, rev, rel), mode_of(args.src, rev, rel)) for rel in VERBATIM]
        layout = edit_test_layout((dst / "tools/test_layout_resolver.py").read_text(encoding="utf-8"))
        for rel, text, mode in files:
            write(dst, rel, text, mode)
        write(dst, "tools/test_layout_resolver.py", layout)
        print("layer 4 written without the gates file; run tools/test_context_budget.py, then pass --budget-count N")
    else:
        base = (dst / ".quality-gates.json").read_text(encoding="utf-8")
        write(dst, ".quality-gates.json", edit_floor(base, "context-budget-unit-tests", 148, args.budget_count))
        print("context-budget-unit-tests 148 -> %d" % args.budget_count)
    return 0


if __name__ == "__main__":
    sys.exit(main())
