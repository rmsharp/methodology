#!/usr/bin/env python3
"""Build PR2 Part 2's layer 2b (the quality ratchet's 1.4.0 and 1.5.0: a gate's budget and process group) in a candidate clone.

    python3 layer2b-build.py <source-repo> <source-rev> <candidate-clone> [--base-rev REV] [--ratchet-count N] [--suite-budget SECONDS]

Reads each file from <source-rev> of <source-repo> (git show, never the working tree) and writes the
layer into <candidate-clone>, which must be on a clean checkout of `pr2/candidate` at layer 2's commit.
It does NOT commit. Every edit is a string replacement asserted to match exactly once, so a drifted
base refuses instead of half-applying. The layer is:

  verbatim from <source-rev>          starter-kit/quality_ratchet.py, tools/test_quality_ratchet.py, starter-kit/quality-gates.json
  the candidate's file, one floor     .quality-gates.json   (--ratchet-count: ratchet-unit-tests, 81 to N)
  the candidate's file, two budgets   .quality-gates.json   (--suite-budget: timeout_seconds on the two gates that run bin/tests.sh)

<source-rev> is the fork's tip: the three verbatim files differ from their layer-2 state (the fork's 26bc97a, version
1.3.0) by exactly the work of 1.4.0 and 1.5.0, which the builder PROVES before it writes: with --base-rev (default
26bc97a) it refuses unless each of the candidate's three files equals that revision's blob, byte for byte. Nothing
else in the candidate changes: bin/tests.sh has no block that cites a gate's budget or process group (measured:
`git diff 26bc97a <rev> -- bin/tests.sh` names neither), and the hook is unchanged since 26bc97a.

Run it twice: once without --ratchet-count (writes the three verbatim files, all computed before the first write, so a
refusal leaves the clone untouched), run `python3 tools/test_quality_ratchet.py` in the clone to read the count, then
once more with --ratchet-count N (and --suite-budget S, if the layer declares one), which writes only the gates file.
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

VERBATIM = ("starter-kit/quality_ratchet.py", "tools/test_quality_ratchet.py", "starter-kit/quality-gates.json")
SUITE_GATES = ("tests-sh-passed", "tests-sh-failed")


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


def edit_floor(text, name, old, new):
    pat = re.compile(r'("name": "%s",\n\s+"direction": "min",\n\s+"threshold": )%d,' % (re.escape(name), old))
    if len(pat.findall(text)) != 1:
        raise SystemExit("refused: gate %s at %d: expected exactly 1 match" % (name, old))
    return pat.sub(lambda m: m.group(1) + "%d," % new, text)


def edit_budget(text, name, seconds):
    """Add `"timeout_seconds": N` to the gate, on the line before its `why` (the fork's layout: command, extract, timeout_seconds, why)."""
    anchor = '"name": "%s",' % name
    if text.count(anchor) != 1:
        raise SystemExit("refused: gate %s: expected exactly 1 declaration, found %d" % (name, text.count(anchor)))
    start = text.index(anchor)
    end = text.index("\n    }", start)
    why = text.index('\n      "why":', start)
    if why > end:
        raise SystemExit("refused: gate %s has no `why` line before its closing brace" % name)
    if '"timeout_seconds"' in text[start:end]:
        raise SystemExit("refused: gate %s already declares timeout_seconds" % name)
    return text[:why] + '\n      "timeout_seconds": %d,' % seconds + text[why:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("rev")
    ap.add_argument("dst")
    ap.add_argument("--base-rev", default="26bc97a")
    ap.add_argument("--ratchet-count", type=int, help="the unit-test count the clone measured")
    ap.add_argument("--suite-budget", type=int, help="timeout_seconds for the two gates that run bin/tests.sh")
    args = ap.parse_args()
    dst, rev = Path(args.dst), args.rev

    if args.ratchet_count is None:
        # prove the base first: each file the layer replaces must be exactly the revision layer 2 was built from
        for rel in VERBATIM:
            have = (dst / rel).read_text(encoding="utf-8")
            if have != show(args.src, args.base_rev, rel):
                raise SystemExit("refused: %s in the candidate is not %s's blob; this builder's premise (the whole difference "
                                 "to <rev> is 1.4.0 and 1.5.0) does not hold" % (rel, args.base_rev))
        files = [(rel, show(args.src, rev, rel), mode_of(args.src, rev, rel)) for rel in VERBATIM]
        for rel, text, mode in files:
            write(dst, rel, text, mode)
        print("layer 2b written without the gates; run tools/test_quality_ratchet.py, then pass --ratchet-count N")
    else:
        base = (dst / ".quality-gates.json").read_text(encoding="utf-8")
        text = edit_floor(base, "ratchet-unit-tests", 81, args.ratchet_count)
        said = "ratchet-unit-tests 81 -> %d" % args.ratchet_count
        if args.suite_budget is not None:
            for name in SUITE_GATES:
                text = edit_budget(text, name, args.suite_budget)
            said += ", timeout_seconds %d on %s" % (args.suite_budget, " and ".join(SUITE_GATES))
        write(dst, ".quality-gates.json", text)
        print(said)
    return 0


if __name__ == "__main__":
    sys.exit(main())
