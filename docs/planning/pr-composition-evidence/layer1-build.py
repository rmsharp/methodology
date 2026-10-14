#!/usr/bin/env python3
"""Build PR2 Part 2's first layer (the layout resolver and the literal scanner) in a candidate clone.

    python3 layer1-build.py <source-repo> <source-rev> <candidate-clone> [--gate-count N]

Reads each file from <source-rev> of <source-repo> (git show, never the working tree) and writes the
layer into <candidate-clone>, which must be on a clean checkout of `pr2/candidate` at Part 1's commit.
It does NOT commit. Every edit is a string replacement asserted to match exactly once, so a drifted
base refuses instead of half-applying. The layer is:

  new, verbatim from <source-rev>     tools/layout_resolver.py, tools/layout_fixtures.py, bin/check-layout-literals
  new, edited                         tools/test_layout_resolver.py   (the lists of embedding tools start empty)
  upstream's file plus one table      bin/_manifest.py                (NEW_LAYOUT, the target layout as data)
  upstream's file plus one block      bin/tests.sh                    (the layout suite, wired in)
  upstream's file plus one gate       .quality-gates.json             (only with --gate-count)

Run it twice: once without --gate-count (writes every file above except the gates file, all computed before
the first write, so a refusal leaves the clone untouched), run `python3 tools/test_layout_resolver.py` in the
clone to read the test count, then once more with --gate-count N (writes only the gates file).
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


def edit_test(text):
    # The lists of tools that embed the resolver's block start empty at this layer: no tool carries it yet.
    # Each later layer appends the tools it carries, which is the mechanism the class docstring describes.
    start = text.index("    COPIES = (")
    end = text.index("    def test_each_copy_equals_the_modules_block_and_carries_exactly_one")
    text = text[:start] + (
        "    COPIES = ()   # no tool embeds the block at this layer; each later layer appends the tools it carries\n\n"
    ) + text[end:]
    # The dashboard twin's test belongs with the dashboard layer: the twin carries no block here.
    a = text.index("    def test_the_dashboards_canonical_only_twin_carries_the_same_block")
    b = text.index("    def test_every_tool_that_carries_the_markers_is_listed")
    text = text[:a] + text[b:]
    start = text.index("    RESOLVED = (")
    end = text.index("    def test_each_resolved_tool_reports_no_site")
    text = text[:start] + (
        "    RESOLVED = ()   # no tool has been worked at this layer; each later layer appends the tools it resolves\n\n"
    ) + text[end:]
    text = once(text, '''    def test_this_repository_scans_the_five_tools_the_plan_names_and_parses_cleanly(self):
        report = cll.scan_root(REPO)
        for name in ("starter-kit/methodology_dashboard.py", "starter-kit/methodology_trim.py",
                     ".githooks/pre-commit", "bin/check-handoff", "starter-kit/close_out_report.py"):''',
                '''    def test_this_repository_scans_the_tools_it_names_and_parses_cleanly(self):
        report = cll.scan_root(REPO)
        for name in ("starter-kit/methodology_dashboard.py", "starter-kit/methodology_trim.py",
                     ".githooks/pre-commit", "bin/check-handoff"):''', "the scan-set test")
    return text


NEW_LAYOUT_PARAGRAPH = '''A project keeps its methodology files either where ``dest`` puts them (the legacy layout above) or one
level down in ``methodology/`` (the new layout, BL-101). NEW_LAYOUT is the second table: for each ``src`` the
``dest`` it takes in the new layout, flat under ``methodology/`` with ``workstreams/`` the one subdirectory
(plan section 4.1). It is a table of literals, not a function, for the reason below.

'''


def edit_manifest(base, head_text):
    text = once(base, "Python 3 stdlib only; data-only module (no imports, no side effects).\n",
                NEW_LAYOUT_PARAGRAPH + "Python 3 stdlib only; data-only module (no imports, no side effects).\n",
                "manifest docstring paragraph")
    text = once(text, "So rows stay literals, and every name it binds (DISTRIBUTION,\nSEED_FORMAT_MARKERS, TRACKED, SEED)",
                "So rows stay literals, and every name it binds (DISTRIBUTION, NEW_LAYOUT,\nSEED_FORMAT_MARKERS, TRACKED, SEED)",
                "manifest docstring names")
    a = head_text.index("# The new layout (BL-101): where each file above lands")
    b = head_text.index("# Optional \"current-format\" markers for SEED dests")
    table = head_text[a:b]
    text = once(text, "# Optional \"current-format\" markers for SEED dests", table + "# Optional \"current-format\" markers for SEED dests",
                "manifest table")
    return text


SUITE_BLOCK = '''# The methodology/ directory move: the layout resolver, the fixture trees in both layouts and the literal
# scanner's own behaviour, on scratch trees. Canonical-only. It tests the scanner; it does NOT run the
# scanner over this repository.
if python3 "$METHODOLOGY/tools/test_layout_resolver.py" >/dev/null 2>&1; then
    pass "layout resolver, fixture trees and literal scanner unit tests green"
else
    fail "layout resolver, fixture trees and literal scanner unit tests failed"
fi
'''

RATCHET_BLOCK_END = '''    fail "quality ratchet unit tests failed"
fi
'''


def edit_gates(text, count, floor_from, floor_to):
    gate = '''    {
      "name": "layout-unit-tests",
      "direction": "min",
      "threshold": %d,
      "command": "python3 tools/test_layout_resolver.py",
      "extract": "Ran (\\\\d+) tests",
      "why": "the layout resolver, the fixture trees in both layouts and the literal scanner's own behaviour on scratch trees. Count never drops; green/red is carried by tests-sh-passed. %d is measured (Ran %d tests, OK)."
    },
''' % (count, count, count)
    text = once(text, '''    {
      "name": "check-links",''', gate + '''    {
      "name": "check-links",''', "gate insertion point")
    return once(text, re.search(r'"name": "tests-sh-passed",\n\s+"direction": "min",\n\s+"threshold": %d' % floor_from, text).group(0),
                re.search(r'"name": "tests-sh-passed",\n\s+"direction": "min",\n\s+"threshold": %d' % floor_from, text).group(0)
                .replace(str(floor_from), str(floor_to)), "tests-sh-passed floor")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("rev")
    ap.add_argument("dst")
    ap.add_argument("--gate-count", type=int)
    ap.add_argument("--floor-from", type=int, default=271)
    ap.add_argument("--floor-to", type=int, default=272)
    args = ap.parse_args()
    dst = Path(args.dst)

    if args.gate_count is None:
        # every edit is computed before the first write, so a refusal leaves the clone untouched
        files = [
            ("tools/layout_resolver.py", show(args.src, args.rev, "tools/layout_resolver.py"), 0o644),
            ("tools/layout_fixtures.py", show(args.src, args.rev, "tools/layout_fixtures.py"), 0o644),
            ("bin/check-layout-literals", show(args.src, args.rev, "bin/check-layout-literals"), 0o755),
            ("tools/test_layout_resolver.py", edit_test(show(args.src, args.rev, "tools/test_layout_resolver.py")), 0o644),
            ("bin/_manifest.py", edit_manifest((dst / "bin/_manifest.py").read_text(encoding="utf-8"),
                                               show(args.src, args.rev, "bin/_manifest.py")), None),
            ("bin/tests.sh", once((dst / "bin/tests.sh").read_text(encoding="utf-8"), RATCHET_BLOCK_END,
                                  RATCHET_BLOCK_END + SUITE_BLOCK, "the suite's insertion point"), None),
        ]
        for rel, text, mode in files:
            write(dst, rel, text, mode)
        print("layer 1 written without the gate; run tools/test_layout_resolver.py and pass --gate-count N")
    else:
        base = (dst / ".quality-gates.json").read_text(encoding="utf-8")
        write(dst, ".quality-gates.json", edit_gates(base, args.gate_count, args.floor_from, args.floor_to))
        print("gate layout-unit-tests = %d, tests-sh-passed %d -> %d" % (args.gate_count, args.floor_from, args.floor_to))
    return 0


if __name__ == "__main__":
    sys.exit(main())
