#!/usr/bin/env python3
"""Build PR2 Part 2's second layer (the gate layer: the ledger hook and the quality ratchet 1.3.0) in a candidate clone.

    python3 layer2-build.py <source-repo> <source-rev> <candidate-clone> [--tests-rev REV] [--gate-counts RATCHET:TESTS]

Reads each file from <source-rev> of <source-repo> (git show, never the working tree) and writes the
layer into <candidate-clone>, which must be on a clean checkout of `pr2/candidate` at layer 1's commit.
It does NOT commit. Every edit is a string replacement asserted to match exactly once, so a drifted
base refuses instead of half-applying. The layer is:

  verbatim from <source-rev>          .githooks/pre-commit, starter-kit/quality_ratchet.py, tools/test_quality_ratchet.py
  the candidate's file, two entries   tools/test_layout_resolver.py   (COPIES and RESOLVED: the first appends)
  the candidate's file, two edits     bin/tests.sh                    (the chain assertion rewritten; the fork's Test 54 added as Test 37)
  the candidate's file, two floors    .quality-gates.json             (only with --gate-counts)

<source-rev> is the last fork commit whose ratchet is the layout lineage and nothing after it: 26bc97a, version 1.3.0,
the first state whose embedded resolver block equals tools/layout_resolver.py. The ratchet's 1.4.0 and 1.5.0 (a gate's
timeout, its process group) are not in it. The blocks of bin/tests.sh come from --tests-rev (default: <source-rev>);
the fork's later edits to the same block (a fixture guard, one more control) are layout work and belong here, so the
S313 build passes the fork's tip for them.

Run it twice: once without --gate-counts (writes every file above except the gates file, all computed before the first
write, so a refusal leaves the clone untouched), run `python3 tools/test_quality_ratchet.py` and `bash bin/tests.sh` in
the clone to read the two counts, then once more with --gate-counts RATCHET:TESTS (writes only the gates file).
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


def show(src, rev, path):
    return subprocess.run(["git", "-C", str(src), "show", "%s:%s" % (rev, path)], check=True,
                          capture_output=True).stdout.decode("utf-8")


def mode_of(src, rev, path):
    out = subprocess.run(["git", "-C", str(src), "ls-tree", rev, path], check=True,
                         capture_output=True).stdout.decode("utf-8")
    return 0o755 if out.startswith("100755") else 0o644


def once(text, old, new, what):
    n = text.count(old)
    if n != 1:
        raise SystemExit("refused: %s: expected exactly 1 match of the anchor, found %d" % (what, n))
    return text.replace(old, new)


def write(dst, rel, text, mode=None):
    p = Path(dst) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    if mode:
        os.chmod(p, mode)


def renumber(text):
    """The fork's Test 54 is this candidate's Test 37 (the next free number after Part 1's Test 36, the precedent
    Part 1 set for the two blocks it carried). Every token that is the number 54 on its own, or its suffix in an
    identifier (t54_repo, HOOK54, RC54), becomes 37; a 54 inside a longer number is left alone."""
    return re.sub(r"(?<![0-9])54(?![0-9])", "37", text)


def edit_test_layout(text):
    text = once(text, "    COPIES = ()   # no tool embeds the block at this layer; each later layer appends the tools it carries\n",
                '    COPIES = ("starter-kit/quality_ratchet.py",)   # the gate layer; each later layer appends the tools it carries\n',
                "COPIES")
    return once(text, "    RESOLVED = ()   # no tool has been worked at this layer; each later layer appends the tools it resolves\n",
                '    RESOLVED = (".githooks/pre-commit", "starter-kit/quality_ratchet.py")   # the gate layer; each later layer appends the tools it resolves\n',
                "RESOLVED")


OLD_CHAIN = '''grep -q 'quality_ratchet.py" --precommit' "$METHODOLOGY/.githooks/pre-commit" \\
    && pass ".githooks/pre-commit chains the quality ratchet before the ledger gate" \\
    || fail ".githooks/pre-commit does not run quality_ratchet.py --precommit"
'''


def fork_chain_block(fork_tests):
    """The fork's rewritten assertion: from its leading comment through the closing `|| fail ...` line."""
    a = fork_tests.index("# The chain names the tool through variables since BL-101 P2")
    marker = '|| fail ".githooks/pre-commit does not run the ratchet before the ledger gate (chain line [$CHAIN54], gate line [$GATE54])"\n'
    b = fork_tests.index(marker, a) + len(marker)
    return fork_tests[a:b]


def fork_test54_block(fork_tests):
    """The fork's Test 54, from its `echo "== Test 54:` line up to (not including) the blank `echo ""` that precedes the Summary."""
    m = re.search(r'^echo "== Test \d+: the ledger hook and the ratchet chain follow the files under methodology/', fork_tests, re.M)
    if not m:
        raise SystemExit("refused: the fork's ledger-hook test block was not found")
    rest = fork_tests[m.start():]
    end = re.search(r'^echo ""\necho "== Summary:', rest, re.M)
    if not end:
        raise SystemExit("refused: the fork's ledger-hook test block does not end at the Summary")
    block = rest[:end.start()]
    if "Test 54:" not in block.splitlines()[0]:
        raise SystemExit("refused: the fork's ledger-hook test block is no longer Test 54: " + block.splitlines()[0][:60])
    return block


def edit_tests_sh(base, fork_tests):
    text = once(base, OLD_CHAIN, renumber(fork_chain_block(fork_tests)), "the chain assertion")
    block = renumber(fork_test54_block(fork_tests))
    leftover = re.findall(r"[A-Za-z_]*54[A-Za-z_]*", block)
    if leftover:
        raise SystemExit("refused: a 54 token survived the renumbering: %r" % sorted(set(leftover)))
    # The candidate's file ends `rm -f ...`, a blank line, then the Summary; the fork's block ends with its own blank line.
    return once(text, '\necho "== Summary:', "\n" + block + 'echo "== Summary:', "the suite's insertion point")


def edit_gates(text, ratchet_count, tests_count, ratchet_from=45, tests_from=272):
    def floor(text, name, old, new):
        pat = re.compile(r'("name": "%s",\n\s+"direction": "min",\n\s+"threshold": )%d,' % (re.escape(name), old))
        if len(pat.findall(text)) != 1:
            raise SystemExit("refused: gate %s at %d: expected exactly 1 match" % (name, old))
        return pat.sub(lambda m: m.group(1) + "%d," % new, text)
    text = floor(text, "ratchet-unit-tests", ratchet_from, ratchet_count)
    return floor(text, "tests-sh-passed", tests_from, tests_count)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("rev")
    ap.add_argument("dst")
    ap.add_argument("--tests-rev")
    ap.add_argument("--gate-counts", help="RATCHET:TESTS, the two numbers the clone measured")
    args = ap.parse_args()
    dst, rev = Path(args.dst), args.rev
    tests_rev = args.tests_rev or rev

    if args.gate_counts is None:
        # every edit is computed before the first write, so a refusal leaves the clone untouched
        files = []
        for rel in (".githooks/pre-commit", "starter-kit/quality_ratchet.py", "tools/test_quality_ratchet.py"):
            files.append((rel, show(args.src, rev, rel), mode_of(args.src, rev, rel)))
        files.append(("tools/test_layout_resolver.py", edit_test_layout((dst / "tools/test_layout_resolver.py").read_text(encoding="utf-8")), None))
        files.append(("bin/tests.sh", edit_tests_sh((dst / "bin/tests.sh").read_text(encoding="utf-8"),
                                                    show(args.src, tests_rev, "bin/tests.sh")), None))
        for rel, text, mode in files:
            write(dst, rel, text, mode)
        print("layer 2 written without the gates; run tools/test_quality_ratchet.py and bin/tests.sh, then pass --gate-counts RATCHET:TESTS")
    else:
        r, t = (int(x) for x in args.gate_counts.split(":"))
        base = (dst / ".quality-gates.json").read_text(encoding="utf-8")
        write(dst, ".quality-gates.json", edit_gates(base, r, t))
        print("ratchet-unit-tests 45 -> %d, tests-sh-passed 272 -> %d" % (r, t))
    return 0


if __name__ == "__main__":
    sys.exit(main())
