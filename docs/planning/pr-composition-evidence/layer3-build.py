#!/usr/bin/env python3
"""Build PR2 Part 2's layer 3 (the ledger trimmer 1.8.0: it resolves the layout, so a ledger under methodology/ is trimmed and proved) in a candidate clone.

    python3 layer3-build.py <source-repo> <source-rev> <candidate-clone> [--base-rev REV] [--trimmer-count N]

Reads each file from <source-rev> of <source-repo> (git show, never the working tree) and writes the
layer into <candidate-clone>, which must be on a clean checkout of `pr2/candidate` at layer 2b's commit.
It does NOT commit. Every edit is a string replacement asserted to match exactly once, so a drifted
base refuses instead of half-applying. The layer is:

  verbatim from <source-rev>          starter-kit/methodology_trim.py, tools/test_methodology_trim.py,
                                      tools/fixtures/trim-verify-template-1.7.0.sh   (new: the frozen 1.7.0 proof template the 1.8.0 tests read)
  the candidate's file, two appends   tools/test_layout_resolver.py   (COPIES and RESOLVED: the trimmer is the second tool that carries the block)
  the candidate's file, one floor     .quality-gates.json   (--trimmer-count: trimmer-unit-tests, 181 to N)

<source-rev> is the fork's tip. The two verbatim tool files differ from Part 1's state (the fork's --base-rev,
default 3616b5f, version 1.7.0) by exactly the work of two fork commits, `ee89b24` (1.8.0) and `26bc97a` (the tie
rule), which the builder PROVES before it writes: it refuses unless each of the candidate's two files equals that
revision's blob, byte for byte, and unless the candidate's `tools/layout_resolver.py` equals <source-rev>'s (so the
block the new trimmer embeds is the module's, which the layout suite then asserts). Nothing else in the candidate
changes: `git diff c8b9ddd <rev> -- bin/tests.sh` adds no line that cites the trimmer, and the shell suite's existing
blocks that run the trimmer (its test file, one `--write` over a scratch ledger) are the same text at the fork's tip.

Run it twice: once without --trimmer-count (writes the verbatim files and the layout-suite edit, all computed before
the first write, so a refusal leaves the clone untouched), run `python3 tools/test_methodology_trim.py` in the clone to
read the count, then once more with --trimmer-count N, which writes only the gates file.
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

VERBATIM = ("starter-kit/methodology_trim.py", "tools/test_methodology_trim.py", "tools/fixtures/trim-verify-template-1.7.0.sh")
BASED = VERBATIM[:2]          # the files the candidate already has, which must equal the base revision's blobs
RESOLVER = "tools/layout_resolver.py"


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
    text = once(text, '    COPIES = ("starter-kit/quality_ratchet.py",)   # the gate layer; each later layer appends the tools it carries\n',
                '    COPIES = ("starter-kit/methodology_trim.py", "starter-kit/quality_ratchet.py")   # the gate layer and the trimmer; each later layer appends the tools it carries\n',
                "COPIES")
    return once(text, '    RESOLVED = (".githooks/pre-commit", "starter-kit/quality_ratchet.py")   # the gate layer; each later layer appends the tools it resolves\n',
                '    RESOLVED = (".githooks/pre-commit", "starter-kit/quality_ratchet.py",   # the gate layer\n'
                '                "starter-kit/methodology_trim.py")   # the trimmer; each later layer appends the tools it resolves\n',
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
    ap.add_argument("--base-rev", default="3616b5f")
    ap.add_argument("--trimmer-count", type=int, help="the unit-test count the clone measured")
    args = ap.parse_args()
    dst, rev = Path(args.dst), args.rev

    if args.trimmer_count is None:
        # prove the base first: each file the layer replaces must be exactly the revision Part 1 took it from
        for rel in BASED:
            have = (dst / rel).read_text(encoding="utf-8")
            if have != show(args.src, args.base_rev, rel):
                raise SystemExit("refused: %s in the candidate is not %s's blob; this builder's premise (the whole difference "
                                 "to <rev> is 1.8.0 and the tie rule) does not hold" % (rel, args.base_rev))
        if (dst / VERBATIM[2]).exists():
            raise SystemExit("refused: %s already exists in the candidate" % VERBATIM[2])
        if (dst / RESOLVER).read_text(encoding="utf-8") != show(args.src, rev, RESOLVER):
            raise SystemExit("refused: the candidate's %s is not %s's, so the trimmer's embedded block would not equal the module's" % (RESOLVER, rev))
        files = [(rel, show(args.src, rev, rel), mode_of(args.src, rev, rel)) for rel in VERBATIM]
        layout = edit_test_layout((dst / "tools/test_layout_resolver.py").read_text(encoding="utf-8"))
        for rel, text, mode in files:
            write(dst, rel, text, mode)
        write(dst, "tools/test_layout_resolver.py", layout)
        print("layer 3 written without the gates file; run tools/test_methodology_trim.py, then pass --trimmer-count N")
    else:
        base = (dst / ".quality-gates.json").read_text(encoding="utf-8")
        write(dst, ".quality-gates.json", edit_floor(base, "trimmer-unit-tests", 181, args.trimmer_count))
        print("trimmer-unit-tests 181 -> %d" % args.trimmer_count)
    return 0


if __name__ == "__main__":
    sys.exit(main())
