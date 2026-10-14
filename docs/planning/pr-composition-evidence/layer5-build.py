#!/usr/bin/env python3
"""Build PR2 Part 2's layer 5 (the dashboard 2.22.0: it reads either layout) in a candidate clone.

    python3 layer5-build.py <source-repo> <source-rev> <candidate-clone> [--base-rev REV] [--dashboard-count N --layout-count M]

Reads each file from <source-rev> of <source-repo> (git show, never the working tree) and writes the
layer into <candidate-clone>, which must be on a clean checkout of `pr2/candidate` at layer 4's commit.
It does NOT commit. Every edit is computed before the first write, so a refusal leaves the clone untouched.
The layer is:

  verbatim from <source-rev>        starter-kit/methodology_dashboard.py, tools/methodology_dashboard.py (the twins)
  a three-way merge                 tools/test_methodology_dashboard.py   (see below)
  the candidate's file, three edits tools/test_layout_resolver.py   (COPIES and RESOLVED gain the dashboard; the twin-block test)
  the candidate's file, two floors  .quality-gates.json   (--dashboard-count, --layout-count)

The dashboard files. The candidate's two twins are Part 1's (2.21.0) and equal the fork's blobs at --base-rev
(default `75f665e`, the commit that made them 2.21.0); the builder refuses unless both do, byte for byte, and unless
the source's two twins equal each other. From that base the fork has 13 commits that touch the three dashboard files
(`git log --first-parent --reverse 75f665e..<rev> -- <the three files>`), BL-101 P5's layers 0 to 5, its floors and
one fixtures change; the layer carries their sum.

The test file is NOT a fork blob. Part 1 made it portable to a tree that is not this repository: it removed the two
tests that read the fork-only `docs/planning/BACKLOG.md` and made the ledger-count floor of `TestS38TrimTriggerRow`
relative to the ledgers that exist. So the layer is the fork tip's file with that difference re-applied: `git
merge-file` with ours = the candidate's file, base = the file at --base-rev, theirs = the tip's. The builder refuses
unless the merge is conflict-free, unless the result differs from the tip by exactly what the candidate's file
differed from the base by (the same added and deleted line counts), and unless the two removed tests are absent from
the result and the relative floor is present once.

The layout suite is the candidate's file with three edits taken from the tip: the dashboard in COPIES (the tuple is
compared sorted, so the place is free), the test that its canonical-only `tools/` twin carries the same block (the
directory walk reads only starter-kit/ and bin/, so the twin would otherwise be tested by nothing), and the dashboard
in RESOLVED (it must read 0 sites). The rest of the tip's COPIES (the checkers, the sync layer, the migration tool,
the close-out report) is later layers' or not carried.

Run it twice: once without the counts (it writes the dashboard, the test file and the layout suite), run
`python3 tools/test_methodology_dashboard.py` and `python3 tools/test_layout_resolver.py` in the clone to read the
two counts, then once more with --dashboard-count N --layout-count M, which writes only the gates file.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

TWINS = ("starter-kit/methodology_dashboard.py", "tools/methodology_dashboard.py")
TEST = "tools/test_methodology_dashboard.py"
LAYOUT_TEST = "tools/test_layout_resolver.py"
SAME_AS_SOURCE = ("tools/layout_resolver.py", "tools/layout_fixtures.py")
REMOVED_BY_PART_1 = ("test_backlog_is_watched_but_never_given_a_trim_row",
                     "test_the_fleet_facts_the_disposition_was_decided_on_are_stated_not_assumed")
RELATIVE_FLOOR = "min(6, len(existing))"


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


def numstat(a_text, b_text):
    """(added, deleted) going from a to b, by git's own diff."""
    with tempfile.TemporaryDirectory() as d:
        a, b = Path(d, "a"), Path(d, "b")
        a.write_text(a_text, encoding="utf-8")
        b.write_text(b_text, encoding="utf-8")
        out = subprocess.run(["git", "diff", "--no-index", "--numstat", str(a), str(b)],
                             capture_output=True).stdout.decode("utf-8")
    if not out.strip():
        return (0, 0)
    added, deleted, _ = out.split("\n")[0].split("\t")
    return (int(added), int(deleted))


def merge_test_file(candidate, base, tip):
    """ours = the candidate's file, base = the file at the base revision, theirs = the tip's. Refuses unless clean and exact."""
    with tempfile.TemporaryDirectory() as d:
        ours, bs, theirs = (Path(d, n) for n in ("ours", "base", "theirs"))
        ours.write_text(candidate, encoding="utf-8")
        bs.write_text(base, encoding="utf-8")
        theirs.write_text(tip, encoding="utf-8")
        r = subprocess.run(["git", "merge-file", "-p", str(ours), str(bs), str(theirs)], capture_output=True)
    if r.returncode != 0:
        raise SystemExit("refused: merging %s (candidate, base, tip) left %d conflict(s); Part 1's edits and the tip's overlap, "
                         "so the layer cannot re-apply them mechanically" % (TEST, r.returncode))
    merged = r.stdout.decode("utf-8")
    part_1 = numstat(base, candidate)
    carried = numstat(tip, merged)
    if carried != part_1:
        raise SystemExit("refused: the merged %s differs from the tip by +%d/-%d, but the candidate's file differs from the base "
                         "by +%d/-%d: something other than Part 1's edits was carried" % ((TEST,) + carried + part_1))
    for name in REMOVED_BY_PART_1:
        if name in merged:
            raise SystemExit("refused: %s is back in the merged test file; Part 1 removed it (it reads the fork-only backlog)" % name)
    if merged.count(RELATIVE_FLOOR) != 1:
        raise SystemExit("refused: the relative ledger floor %r is not in the merged test file exactly once" % RELATIVE_FLOOR)
    return merged


def edit_test_layout(text, tip_text):
    start = "    def test_the_dashboards_canonical_only_twin_carries_the_same_block(self):\n"
    end = "    def test_every_tool_that_carries_the_markers_is_listed(self):\n"
    if tip_text.count(start) != 1 or tip_text.count(end) != 1:
        raise SystemExit("refused: the tip's layout suite does not hold the twin test where this builder expects it")
    twin = tip_text[tip_text.index(start):tip_text.index(end)]
    text = once(text, '    COPIES = ("starter-kit/context_budget.py", "starter-kit/methodology_trim.py", "starter-kit/quality_ratchet.py")   # the gate layer, the trimmer and the budget gate; each later layer appends the tools it carries\n',
                '    COPIES = ("starter-kit/context_budget.py", "starter-kit/methodology_dashboard.py", "starter-kit/methodology_trim.py",\n'
                '              "starter-kit/quality_ratchet.py")   # the gate layer, the trimmer, the budget gate and the dashboard (its tools/ twin is asserted below); each later layer appends the tools it carries\n',
                "COPIES")
    text = once(text, end, twin + end, "the twin test's place")
    return once(text, '                "starter-kit/context_budget.py")   # the budget gate; each later layer appends the tools it resolves\n',
                '                "starter-kit/context_budget.py",   # the budget gate\n'
                '                "starter-kit/methodology_dashboard.py")   # the dashboard: its tools/ twin is the same bytes; each later layer appends the tools it resolves\n',
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
    ap.add_argument("--base-rev", default="75f665e")
    ap.add_argument("--dashboard-count", type=int, help="the dashboard suite's test count the clone measured")
    ap.add_argument("--layout-count", type=int, help="the layout suite's test count the clone measured")
    args = ap.parse_args()
    dst, rev, base = Path(args.dst), args.rev, args.base_rev

    if args.dashboard_count is None and args.layout_count is None:
        # prove the base first: the candidate's twins are exactly the revision Part 1 took them from
        for rel in TWINS:
            if (dst / rel).read_text(encoding="utf-8") != show(args.src, base, rel):
                raise SystemExit("refused: %s in the candidate is not %s's blob; this builder's premise (the whole difference "
                                 "to <rev> is the dashboard's 2.22.0) does not hold" % (rel, base))
        for rel in SAME_AS_SOURCE:
            if (dst / rel).read_text(encoding="utf-8") != show(args.src, rev, rel):
                raise SystemExit("refused: the candidate's %s is not %s's, so the dashboard's embedded block or its test trees would not be the fork's" % (rel, rev))
        twins = [(rel, show(args.src, rev, rel), mode_of(args.src, rev, rel)) for rel in TWINS]
        if twins[0][1] != twins[1][1]:
            raise SystemExit("refused: the source's two dashboard twins differ at %s" % rev)
        merged = merge_test_file((dst / TEST).read_text(encoding="utf-8"), show(args.src, base, TEST), show(args.src, rev, TEST))
        layout = edit_test_layout((dst / LAYOUT_TEST).read_text(encoding="utf-8"), show(args.src, rev, LAYOUT_TEST))
        for rel, text, mode in twins:
            write(dst, rel, text, mode)
        write(dst, TEST, merged, mode_of(args.src, rev, TEST))
        write(dst, LAYOUT_TEST, layout)
        print("layer 5 written without the gates file; run the two suites, then pass --dashboard-count N --layout-count M")
    elif args.dashboard_count is not None and args.layout_count is not None:
        text = (dst / ".quality-gates.json").read_text(encoding="utf-8")
        text = edit_floor(text, "dashboard-unit-tests", 354, args.dashboard_count)
        text = edit_floor(text, "layout-unit-tests", 74, args.layout_count)
        write(dst, ".quality-gates.json", text)
        print("dashboard-unit-tests 354 -> %d; layout-unit-tests 74 -> %d" % (args.dashboard_count, args.layout_count))
    else:
        raise SystemExit("refused: pass both --dashboard-count and --layout-count, or neither")
    return 0


if __name__ == "__main__":
    sys.exit(main())
