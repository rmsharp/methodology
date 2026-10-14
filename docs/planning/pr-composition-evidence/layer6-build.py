#!/usr/bin/env python3
"""Build PR2 Part 2's layer 6 (the sync layers: bin/sync, bin/status, bin/check-links and the manifest reader
read a project in either layout) in a candidate clone, as three checkpoint commits' worth of edits.

    python3 layer6-build.py <source-repo> <source-rev> <candidate-clone> --stage prep|tools|suite
                            [--sync-count N --passed N --layout-count M]   (suite stage, second run)

Reads each file from <source-rev> of <source-repo> (git show, never the working tree) and writes the stage
into <candidate-clone>, which must hold the previous stage's commit (the first stage: layer 5's `dd581fe`).
It does NOT commit. Every edit is computed before the first write, so a refusal leaves the clone untouched.

The layer is more than the plan's five files, and each commit must leave the whole suite green, so it is three
commits of at most five files:

  prep   bin/tests.sh                      Test 15 counts the table's ROWS (lines that start with the project's name),
                                           not every line that names it. Green on the old bin/status too; it is what
                                           lets the next commit add a `layout:` line to that tool's output.
  tools  bin/sync, bin/status, bin/check-links, bin/_manifest_reader.py     verbatim from <source-rev>
         tools/test_layout_resolver.py     COPIES gains the three tools that now embed the resolver block
  suite  tools/test_sync_layouts.py        verbatim from <source-rev> except ONE assertion (below)
         tools/test_layout_resolver.py     the scan-set test names the three tools this layer resolves instead of
                                           bin/check-handoff (now not scanned), and one new test pins the two exemptions
         bin/tests.sh                      the block that runs it
         bin/check-layout-literals         two files are not scanned (the plan's D5)
         .quality-gates.json               two gates added (sync-layout-unit-tests, layout-literals) and the floors

What the candidate holds, and what this builder asserts about it before writing anything:

  The four tools are upstream's own bytes. The candidate's copy of each is the fork's blob at --base-rev (bin/sync,
  bin/status and bin/_manifest_reader.py at `2ed9262`, bin/check-links at `7aa27a0`), byte for byte, so the layer
  is those four files from the tip and nothing is merged. The builder refuses unless that holds.

  bin/_manifest.py is NOT taken: the candidate's differs from the tip's in comments and the module docstring only
  (its `Test 34` is this suite's number for the block the tip numbers 53). The builder refuses unless the two
  parse to the same code once the docstring is removed.

  tools/layout_resolver.py and tools/layout_fixtures.py equal the source's, so the embedded blocks and the fixture
  trees are the ones the tip's tools were written against.

The one edit to the tip's sync suite. `test_a_legacy_project_asked_for_the_new_layout_is_refused_and_the_migration_tool_is_named`
ends with an assertion that bin/migrate-layout is a file; that tool is the NEXT layer's. The line is removed here and
the migration layer puts it back (asserted: exactly one occurrence, exactly this text).

The scanner (plan section 7, D5, answered 2026-10-14): the layout reading of bin/check-handoff and bin/check-ledger is
NOT part of this change, so the scanner reads 10 sites in them, and a gate at 0 needs them out of its scope. They
are added to NOT_SCANNED_ALWAYS with the reason printed beside them. The fork's scanner has no such entry (its two
checkers read both layouts): this is the one place the candidate's scanner differs from the fork's, and the entry
is the line to delete if the checkers' layout reading is ever carried.

Second run of the suite stage: `python3 tools/test_sync_layouts.py`, `python3 tools/test_layout_resolver.py` and
`bash bin/tests.sh` in the clone give the three counts; `--sync-count N --passed N --layout-count M` writes only
the gates file.
"""
import argparse
import ast
import os
import re
import subprocess
import sys
from pathlib import Path

TOOLS = ("bin/sync", "bin/status", "bin/check-links", "bin/_manifest_reader.py")
BASE_REV = {"bin/sync": "2ed9262", "bin/status": "2ed9262", "bin/_manifest_reader.py": "2ed9262", "bin/check-links": "7aa27a0"}
SAME_AS_SOURCE = ("tools/layout_resolver.py", "tools/layout_fixtures.py")
SUITE = "tools/test_sync_layouts.py"
LAYOUT_TEST = "tools/test_layout_resolver.py"
TESTS_SH = "bin/tests.sh"
SCANNER = "bin/check-layout-literals"
GATES = ".quality-gates.json"

MIGRATE_ASSERT = '        self.assertTrue((REPO / "bin" / "migrate-layout").is_file())\n'

OLD_GOT = '        GOT="$(echo "$OUT" | grep -c "$(basename "$P")")"\n'
OLD_GOT_FLUSH = 'GOT="$(echo "$OUT" | grep -c "$(basename "$P")")"\n'
NEW_GOT = (
    "# A table row STARTS with the project's name; the `layout: <name>  <kind>` line P6 added before the table names it too,\n"
    "# and is not a row (counting every line that mentions the name read 31 for 30 files).\n"
    'GOT="$(echo "$OUT" | grep -c "^$(basename "$P") ")"\n')

WIRING_START = "# The sync layer in both layouts (BL-101 P6): "
WIRING_END = "    fail \"sync layer in both layouts unit tests failed\"\nfi\n"
WIRING_ANCHOR = 'echo "== Test 19: dashboard twins byte-identical + same DASHBOARD_VERSION =="\n'

SCAN_SET_OLD = (
    '    def test_this_repository_scans_the_tools_it_names_and_parses_cleanly(self):\n'
    '        report = cll.scan_root(REPO)\n'
    '        for name in ("starter-kit/methodology_dashboard.py", "starter-kit/methodology_trim.py",\n'
    '                     ".githooks/pre-commit", "bin/check-handoff"):\n'
    '            self.assertIn(name, report["files"])\n'
    '        self.assertEqual(report["problems"], [])\n')
SCAN_SET_NEW = (
    '    def test_this_repository_scans_the_tools_it_names_and_parses_cleanly(self):\n'
    '        report = cll.scan_root(REPO)\n'
    '        for name in ("starter-kit/methodology_dashboard.py", "starter-kit/methodology_trim.py",\n'
    '                     ".githooks/pre-commit", "bin/sync", "bin/status", "bin/check-links"):\n'
    '            self.assertIn(name, report["files"])\n'
    '        self.assertEqual(report["problems"], [])\n'
    '\n'
    '    def test_the_two_checkers_that_do_not_read_the_layout_are_not_scanned_and_say_why(self):\n'
    '        report = cll.scan_root(REPO)\n'
    '        for name in ("bin/check-handoff", "bin/check-ledger"):\n'
    '            self.assertNotIn(name, report["files"])\n'
    '            self.assertIn("canonical-only", report["not_scanned"][name])\n')

SCANNER_OLD = '    "bin/tests.sh": "the suite encodes the layout and is parameterised over both (plan C13)",\n}\n'
SCANNER_NEW = (
    '    "bin/tests.sh": "the suite encodes the layout and is parameterised over both (plan C13)",\n'
    '    "bin/check-handoff": "a canonical-only checker that adopters never run; this tree does not give it the methodology/ layout reading",\n'
    '    "bin/check-ledger": "a canonical-only checker that adopters never run; this tree does not give it the methodology/ layout reading",\n'
    '}\n')

COPIES_OLD = ('    COPIES = ("starter-kit/context_budget.py", "starter-kit/methodology_dashboard.py", "starter-kit/methodology_trim.py",\n'
              '              "starter-kit/quality_ratchet.py")   # the gate layer, the trimmer, the budget gate and the dashboard (its tools/ twin is asserted below); each later layer appends the tools it carries\n')
COPIES_NEW = ('    COPIES = ("starter-kit/context_budget.py", "starter-kit/methodology_dashboard.py", "starter-kit/methodology_trim.py",\n'
              '              "starter-kit/quality_ratchet.py",   # the gate layer, the trimmer, the budget gate and the dashboard (its tools/ twin is asserted below)\n'
              '              "bin/sync", "bin/status", "bin/check-links")   # the sync layer; each later layer appends the tools it carries\n')

GATE_BEFORE = '    {\n      "name": "check-links",\n'
WHY_SYNC = ("the manifest's second table (NEW_LAYOUT) and its reader, bin/sync --layout auto|legacy|new (a legacy project is never "
            "given the new layout, seeds are not shadowed, ignore mode, --source=github), bin/status and bin/check-links in both "
            "layouts, each driven as a command in scratch projects, and the literal scanner over this repository. Count never "
            "drops; green/red is carried by tests-sh-passed. %d is measured (Ran %d tests, OK).")
WHY_LITERALS = ("exit code: no shipped tool names a methodology file by a root path (a string constant in a bin/ script, a "
                "starter-kit/ tool or a hook), so the methodology/ move cannot be passed silently by a gate that reads the wrong "
                "place. A site is acknowledged only by a same-line marker with a reason. bin/check-handoff and bin/check-ledger "
                "are not scanned: they are canonical-only checkers that adopters never run, and this change does not give them "
                "the layout reading.")


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


def code_without_docstring(text):
    tree = ast.parse(text)
    if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(getattr(tree.body[0], "value", None), ast.Constant):
        tree.body = tree.body[1:]
    return ast.dump(tree)


def stage_prep(src, rev, dst):
    sh = (dst / TESTS_SH).read_text(encoding="utf-8")
    tip = show(src, rev, TESTS_SH)
    if NEW_GOT not in tip:
        raise SystemExit("refused: the tip's Test 15 does not read as this builder expects (%s)" % rev)
    # the candidate's Test 15 line is flush left in the file or indented; accept exactly one of the two spellings
    old = OLD_GOT_FLUSH if sh.count(OLD_GOT_FLUSH) == 1 else OLD_GOT
    sh = once(sh, old, NEW_GOT, "Test 15's row count")
    return [(TESTS_SH, sh, None)]


def stage_tools(src, rev, dst):
    for rel in TOOLS:
        base = show(src, BASE_REV[rel], rel)
        if (dst / rel).read_text(encoding="utf-8") != base:
            raise SystemExit("refused: %s in the candidate is not the fork's blob at %s; this builder's premise (the layer is "
                             "the tip's file, nothing merged) does not hold" % (rel, BASE_REV[rel]))
    for rel in SAME_AS_SOURCE:
        if (dst / rel).read_text(encoding="utf-8") != show(src, rev, rel):
            raise SystemExit("refused: the candidate's %s is not %s's, so the embedded blocks would not be the ones the tools were written against" % (rel, rev))
    if code_without_docstring((dst / "bin/_manifest.py").read_text(encoding="utf-8")) != \
            code_without_docstring(show(src, rev, "bin/_manifest.py")):
        raise SystemExit("refused: bin/_manifest.py in the candidate differs from %s in more than comments and the docstring" % rev)
    out = [(rel, show(src, rev, rel), mode_of(src, rev, rel)) for rel in TOOLS]
    lt = (dst / LAYOUT_TEST).read_text(encoding="utf-8")
    out.append((LAYOUT_TEST, once(lt, COPIES_OLD, COPIES_NEW, "COPIES"), None))
    return out


def wiring_block(tip):
    start = tip.index(WIRING_START)
    end = tip.index(WIRING_END, start) + len(WIRING_END)
    block = tip[start:end]
    if block.count("Test 53") != 1:
        raise SystemExit("refused: the tip's wiring block does not name Test 53 exactly once")
    return block.replace("Test 53", "Test 34")


def stage_suite(src, rev, dst, counts):
    out = []
    if counts is None:
        suite = show(src, rev, SUITE)
        out.append((SUITE, once(suite, MIGRATE_ASSERT, "", "the migrate-layout assertion"), mode_of(src, rev, SUITE)))
        sh = (dst / TESTS_SH).read_text(encoding="utf-8")
        out.append((TESTS_SH, once(sh, WIRING_ANCHOR, wiring_block(show(src, rev, TESTS_SH)) + "\n" + WIRING_ANCHOR, "the wiring block's place"), None))
        sc = (dst / SCANNER).read_text(encoding="utf-8")
        out.append((SCANNER, once(sc, SCANNER_OLD, SCANNER_NEW, "NOT_SCANNED_ALWAYS"), None))
        lt = (dst / LAYOUT_TEST).read_text(encoding="utf-8")
        out.append((LAYOUT_TEST, once(lt, SCAN_SET_OLD, SCAN_SET_NEW, "the scan-set test"), None))
    else:
        sync_n, passed_n, layout_n = counts
        gates = (dst / GATES).read_text(encoding="utf-8")
        if '"name": "sync-layout-unit-tests"' in gates or '"name": "layout-literals"' in gates:
            raise SystemExit("refused: the gates file already declares one of the two gates")
        new = ('    {\n      "name": "sync-layout-unit-tests",\n      "direction": "min",\n      "threshold": %d,\n'
               '      "command": "python3 tools/test_sync_layouts.py",\n      "extract": "Ran (\\\\d+) tests",\n'
               '      "why": "%s"\n    },\n' % (sync_n, WHY_SYNC % (sync_n, sync_n)) +
               '    {\n      "name": "layout-literals",\n      "direction": "max",\n      "threshold": 0,\n'
               '      "command": "bin/check-layout-literals",\n      "why": "%s"\n    },\n' % WHY_LITERALS)
        gates = once(gates, GATE_BEFORE, new + GATE_BEFORE, "the gates' place")
        for name, old, now in (("tests-sh-passed", None, passed_n), ("layout-unit-tests", None, layout_n)):
            pat = re.compile(r'("name": "%s",\n\s+"direction": "min",\n\s+"threshold": )(\d+),' % re.escape(name))
            if len(pat.findall(gates)) != 1:
                raise SystemExit("refused: gate %s: expected exactly 1 match" % name)
            gates = pat.sub(lambda m: m.group(1) + "%d," % now, gates)
        out.append((GATES, gates, None))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("rev")
    ap.add_argument("dst")
    ap.add_argument("--stage", required=True, choices=("prep", "tools", "suite"))
    ap.add_argument("--sync-count", type=int)
    ap.add_argument("--passed", type=int)
    ap.add_argument("--layout-count", type=int)
    args = ap.parse_args()
    dst = Path(args.dst)
    counts = (args.sync_count, args.passed, args.layout_count)
    if any(c is not None for c in counts) and not all(c is not None for c in counts):
        raise SystemExit("refused: pass all three of --sync-count, --passed and --layout-count, or none")
    if args.stage == "prep":
        edits = stage_prep(args.src, args.rev, dst)
    elif args.stage == "tools":
        edits = stage_tools(args.src, args.rev, dst)
    else:
        edits = stage_suite(args.src, args.rev, dst, None if counts[0] is None else counts)
    for rel, text, mode in edits:
        write(dst, rel, text, mode)
    print("stage %s written: %s" % (args.stage, ", ".join(rel for rel, _, _ in edits)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
