#!/usr/bin/env python3
"""Build PR2 Part 2's checkers' layer (bin/check-ledger and bin/check-handoff read a project in either layout)
in a candidate clone, as two checkpoint commits' worth of edits.

    python3 layer6b-build.py <source-repo> <source-rev> <candidate-clone> --stage tools|suite
                             [--checker-count N --passed N]      (suite stage, second run)

Reads each file from <source-rev> of <source-repo> (git show, never the working tree) and writes the stage
into <candidate-clone>, which must hold the previous stage's commit (the first stage: layer 6's `0aa1897`).
It does NOT commit. Every edit is computed before the first write, so a refusal leaves the clone untouched.

Why this layer exists (plan section 7, D5, amended 2026-10-14): `bin/migrate-layout` runs both checkers over a
project before and after the move and compares their exit codes, so with both left legacy-only the tool reports
`CHECKS DIFFER` and exits 4 on every apply. The plan's answer: carry the layout reading of the two checkers,
hand-built as upstream's blob plus those hunks, and nothing else the tip's copies carry.

Two commits of at most five files, each leaving the whole suite green:

  tools  bin/check-ledger                  the TIP's blob (`d55209d`): its whole difference from upstream's
                                           (`a96b641`) is the layout reading (four hunks, +72 / -5, listed in the record)
         bin/check-handoff                 upstream's blob (`d314c4d`) plus SEVEN edits, each one a piece of the tip's
                                           own text (asserted: every inserted string occurs in the tip's file). The
                                           tip's file differs from upstream's by +610 / -57; everything beyond these
                                           edits is fork-only (the stub schema, the answer-slot and locator rules, the
                                           record budget, --archived, the unmeasured-gate lint) and is NOT carried
         tools/test_layout_resolver.py     COPIES gains the two tools that now embed the resolver block (the test that
                                           lists every carrier would fail without it)
  suite  tools/test_checker_layouts.py     the tip's suite cut to the two checkers the candidate has (the tip's also
                                           drives bin/check-overhead and bin/model-report, which the candidate lacks),
                                           plus THREE tests the tip's does not have (the second mutation round's survivors)
         bin/tests.sh                      the block that runs it
         bin/check-layout-literals         the two NOT_SCANNED_ALWAYS entries layer 6 added are deleted
         tools/test_layout_resolver.py     the scan-set test names the two checkers; the pin test that said they are
                                           not scanned is REPLACED (not deleted: the gate `layout-unit-tests` is a
                                           floor, and a floor cannot fall) by one that pins what is still exempt
         .quality-gates.json               one gate added (checker-layout-unit-tests) and the shell suite's floor

Second run of the suite stage: `python3 tools/test_checker_layouts.py` and `bash bin/tests.sh` in the clone give the
two counts; `--checker-count N --passed N` writes only the gates file.
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

LEDGER, HANDOFF = "bin/check-ledger", "bin/check-handoff"
BLOB = {  # (candidate = upstream's blob, tip's blob): the premises, asserted before anything is written
    LEDGER: ("a96b641", "d55209d"),
    HANDOFF: ("d314c4d", "2eaddac"),
}
LAYOUT_TEST = "tools/test_layout_resolver.py"
SUITE = "tools/test_checker_layouts.py"
TESTS_SH = "bin/tests.sh"
SCANNER = "bin/check-layout-literals"
GATES = ".quality-gates.json"

COPIES_OLD = ('              "bin/sync", "bin/status", "bin/check-links")   # the sync layer; each later layer appends the tools it carries\n')
COPIES_NEW = ('              "bin/sync", "bin/status", "bin/check-links",   # the sync layer\n'
              '              "bin/check-ledger", "bin/check-handoff")   # the checkers\' layer; each later layer appends the tools it carries\n')

SCANNER_OLD = (
    '    "bin/check-handoff": "a canonical-only checker that adopters never run; this tree does not give it the methodology/ layout reading",\n'
    '    "bin/check-ledger": "a canonical-only checker that adopters never run; this tree does not give it the methodology/ layout reading",\n')

SCAN_SET_OLD = (
    '                     ".githooks/pre-commit", "bin/sync", "bin/status", "bin/check-links"):\n')
SCAN_SET_NEW = (
    '                     ".githooks/pre-commit", "bin/sync", "bin/status", "bin/check-links",\n'
    '                     "bin/check-handoff", "bin/check-ledger"):\n')
PIN_OLD = (
    '    def test_the_two_checkers_that_do_not_read_the_layout_are_not_scanned_and_say_why(self):\n'
    '        report = cll.scan_root(REPO)\n'
    '        for name in ("bin/check-handoff", "bin/check-ledger"):\n'
    '            self.assertNotIn(name, report["files"])\n'
    '            self.assertIn("canonical-only", report["not_scanned"][name])\n')
PIN_NEW = (
    '    def test_only_the_manifest_and_the_suite_are_exempt_from_the_scan(self):\n'
    '        # The checkers read the layout and are scanned like every other shipped tool: a new exemption is a deliberate\n'
    '        # edit of this list, not a line added to NOT_SCANNED_ALWAYS on the way to a green gate.\n'
    '        self.assertEqual(sorted(cll.NOT_SCANNED_ALWAYS), ["bin/_manifest.py", "bin/tests.sh"])\n'
    '        report = cll.scan_root(REPO)\n'
    '        for name in ("bin/check-handoff", "bin/check-ledger"):\n'
    '            self.assertNotIn(name, report["not_scanned"])\n')

WIRING_ANCHOR = "\n# The sync layer in both layouts (BL-101 P6): "
WIRING_START = "# The canonical checkers in both layouts (BL-101 P4): "
WIRING_END = '    fail "canonical checkers in both layouts unit tests failed"\nfi\n'
WIRING_CUT = (
    ("check-ledger, check-handoff, check-overhead and\n# model-report, each run as a command",
     "check-ledger and check-handoff,\n# each run as a command"),
    ('pass "canonical checkers (ledger, receipts, overhead, model report) in both layouts unit tests green"',
     'pass "canonical checkers (ledger, receipts) in both layouts unit tests green"'),
)

GATE_BEFORE = '    {\n      "name": "sync-layout-unit-tests",\n'
WHY_CHECKERS = ("BL-101 P4: the canonical checkers (check-ledger and check-handoff) run as commands in both layouts, in a tie the "
                "runner decides and in a half-migrated tree. Count never drops; green/red is carried by tests-sh-passed. %d is "
                "measured (Ran %d tests, OK).")

# The suite cut: from the first class that drives a tool the candidate lacks to the module's main guard.
CUT_FROM = "class TestCheckOverhead(Project):"
CUT_TO = 'if __name__ == "__main__":'
DOC_OLD = (
    'CANONICAL-ONLY, like the checkers it drives (bin/check-handoff, bin/check-ledger, bin/check-overhead,\n'
    'bin/model-report): none is in bin/_manifest.py. bin/check-learnings is not driven here: it reads the\n')
DOC_NEW = (
    'CANONICAL-ONLY, like the checkers it drives (bin/check-handoff and bin/check-ledger): neither is in\n'
    'bin/_manifest.py. bin/check-learnings is not driven here: it reads the\n')
# Three tests the TIP's suite does not have. The second mutation round (layer6b-mutate.py, round 2) found three behaviours no test named:
# an explicit --file in each checker (the refusal message tells the person to name the ledger with it, so the way out must work) and
# check-ledger's report of where it looked when there is no ledger. Each is the mutant it kills, in the test's name.
ANCHOR_LEDGER = "    def test_all_reads_the_shards_beside_the_ledger_in_either_layout(self):\n"
TEST_LEDGER = (
    "    def test_a_named_ledger_is_read_even_where_the_runner_does_not_decide(self):\n"
    "        # the refusal says to name the ledger with --file: that is the way out, and it has to work\n"
    "        self.shape(\"half\", \"CHANGELOG.md\", LEDGER, LEDGER)\n"
    "        rc, out, err = self.run_tool(\"check-ledger\", \"--file\", \"CHANGELOG.md\")\n"
    "        self.assertEqual((rc, \"OK\" in out), (0, True), out + err)\n"
    "\n"
    "    def test_a_tree_with_no_ledger_is_reported_naming_where_it_looked(self):\n"
    "        rc, out, err = self.run_tool(\"check-ledger\")\n"
    "        self.assertEqual(rc, 2, out + err)\n"
    "        self.assertIn(os.path.join(self.root, \"CHANGELOG.md\"), err)\n"
    "\n")
ANCHOR_HANDOFF = "    def test_the_canonical_seed_is_still_the_fallback_for_a_tree_with_no_ledger(self):\n"
TEST_HANDOFF = (
    "    def test_a_named_ledger_is_read_even_where_the_runner_does_not_decide(self):\n"
    "        self.shape(\"half\", \"HANDOFFS.md\", HANDOFFS_EMPTY, HANDOFFS_EMPTY)\n"
    "        rc, out, err = self.run_tool(\"check-handoff\", \"--allow-none\", \"--file\", \"HANDOFFS.md\")\n"
    "        self.assertEqual(rc, 0, out + err)\n"
    "        self.assertNotIn(\"half-migrated\", out)\n"
    "\n")

CONSTANT_LINES = (  # used only by the two classes the cut removes
    'HANDOFFS_MODEL = ("# Handoff Receipts\\n\\n```handoff\\nsession: S1\\ndate: 2026-01-01\\nstatus: complete\\n```\\n\\n"\n'
    '                  "The model wrote it.\\n")   # free text AFTER the block is what the secondary source reads\n',
    'CONFIG = \'{"classes": {"read-set": {"total_bytes": 1000}}, "files": [{"path": "%s", "class": "read-set"}]}\'\n',
)


def git(src, *args):
    return subprocess.run(["git", "-C", str(src), *args], check=True, capture_output=True).stdout.decode("utf-8")


def show(src, rev, path):
    return git(src, "show", "%s:%s" % (rev, path))


def blob(src, rev, path):
    return git(src, "rev-parse", "--short", "%s:%s" % (rev, path)).strip()


def mode_of(src, rev, path):
    out = git(src, "ls-tree", rev, path)
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


def tip_line(tip, needle, what):
    """The one line of the tip's file that contains `needle`, newline included."""
    hits = [l for l in tip.splitlines(keepends=True) if needle in l]
    if len(hits) != 1:
        raise SystemExit("refused: the tip's %s: expected exactly 1 line holding %r, found %d" % (what, needle, len(hits)))
    return hits[0]


def check_premises(src, rev, dst):
    for rel, (cand, tip) in BLOB.items():
        got = blob(src, rev, rel)
        if got != tip:
            raise SystemExit("refused: %s at %s is blob %s, this builder was written against %s" % (rel, rev, got, tip))
        have = subprocess.run(["git", "-C", str(dst), "rev-parse", "--short", "HEAD:" + rel], capture_output=True,
                              text=True).stdout.strip()
        if have != cand:
            raise SystemExit("refused: %s in the candidate is blob %s, not upstream's %s; the premise (the layer is "
                             "upstream's blob plus the tip's layout hunks) does not hold" % (rel, have, cand))


def handoff_edits(cand, tip):
    """upstream's check-handoff plus the tip's layout hunks. Every inserted string is cut from the tip's own text."""
    # 1. the resolver block, the two constants and the half-migrated exception: between `from pathlib import Path` and SEED_SENTINEL
    start = tip.index("# === LAYOUT ===\n")
    end = tip.index('SEED_SENTINEL = "METHODOLOGY-SEED-SENTINEL"\n')
    block = tip[start:end]
    out = once(cand, 'from pathlib import Path\n\nSEED_SENTINEL = "METHODOLOGY-SEED-SENTINEL"\n',
               "from pathlib import Path\n\n" + block + 'SEED_SENTINEL = "METHODOLOGY-SEED-SENTINEL"\n', "the layout block's place")
    marker = re.search(r"  # layout: ok -- message text: [^\n]*\n", tip_line(tip, "a union merge of HANDOFFS.md does this", "union-merge line")).group(0)
    # 2. the manifest's own file name
    out = once(out, 'GATES_MANIFEST = ".quality-gates.json"\n', tip_line(tip, "GATES_MANIFEST = ", "GATES_MANIFEST"), "GATES_MANIFEST")
    # 3. the repeated-key message (a conventional file name in message text)
    old = '                        "(a union merge of HANDOFFS.md does this; resolve keep-both with "\n'
    out = once(out, old, old[:-1] + marker, "the union-merge message")
    # 4. the gate-citation message
    old = '            "`quality_ratchet: N/M pass …` summary line of `quality_ratchet.py --run` into "\n'
    out = once(out, old, old[:-1] + marker, "the gate-citation message")
    # 5. default_path(): the whole function
    dp_old = cand[cand.index("def default_path() -> Path:"):cand.index("def main() -> int:")]
    dp_new = tip[tip.index("def default_path() -> Path:"):tip.index("def main() -> int:")]
    out = once(out, dp_old, dp_new, "default_path()")
    # 6. main(): the description and --file help lines
    for needle in ('description="Validate the newest `handoff` receipt block in a HANDOFFS.md ledger."',
                   'p.add_argument("--file", help="explicit HANDOFFS.md path to check (what bin/tests.sh uses)")'):
        line = tip_line(tip, needle, needle)
        plain = line.split("  # layout: ok", 1)[0] + "\n"
        out = once(out, plain, line, needle)
    # 7. main(): a half-migrated tree is refused, never guessed
    t0 = tip.index("    try:\n        path = Path(args.file) if args.file else default_path()\n")
    t1 = tip.index("    if not path.exists():", t0)
    out = once(out, "    path = Path(args.file) if args.file else default_path()\n", tip[t0:t1], "main()'s path")
    for piece in (block, dp_new, tip[t0:t1]):
        if piece not in tip:
            raise SystemExit("refused: an inserted piece is not the tip's own text")
    return out


def stage_tools(src, rev, dst):
    check_premises(src, rev, dst)
    cand = (dst / HANDOFF).read_text(encoding="utf-8")
    out = [(LEDGER, show(src, rev, LEDGER), mode_of(src, rev, LEDGER)),
           (HANDOFF, handoff_edits(cand, show(src, rev, HANDOFF)), mode_of(src, rev, HANDOFF))]
    lt = (dst / LAYOUT_TEST).read_text(encoding="utf-8")
    out.append((LAYOUT_TEST, once(lt, COPIES_OLD, COPIES_NEW, "COPIES"), None))
    return out


def cut_suite(tip):
    out = once(tip, DOC_OLD, DOC_NEW, "the suite's docstring")
    for line in CONSTANT_LINES:
        out = once(out, line, "", "a constant the cut leaves unused")
    out = once(out, ANCHOR_LEDGER, TEST_LEDGER + ANCHOR_LEDGER, "the ledger tests' place")
    out = once(out, ANCHOR_HANDOFF, TEST_HANDOFF + ANCHOR_HANDOFF, "the receipt tests' place")
    a, b = out.index(CUT_FROM), out.index(CUT_TO)
    if not a < b:
        raise SystemExit("refused: the suite's classes are not where this builder expects")
    out = out[:a].rstrip("\n") + "\n\n\n" + out[b:]
    for name in ("check-overhead", "model-report", "TestCheckOverhead", "TestModelReport", "CONFIG", "HANDOFFS_MODEL"):
        if name in out:
            raise SystemExit("refused: the cut suite still names %r" % name)
    return out


def wiring_block(tip):
    start = tip.index(WIRING_START)
    end = tip.index(WIRING_END, start) + len(WIRING_END)
    block = tip[start:end]
    for old, new in WIRING_CUT:
        block = once(block, old, new, "the wiring block's wording")
    return block


def stage_suite(src, rev, dst, counts):
    out = []
    if counts is None:
        out.append((SUITE, cut_suite(show(src, rev, SUITE)), mode_of(src, rev, SUITE)))
        sh = (dst / TESTS_SH).read_text(encoding="utf-8")
        out.append((TESTS_SH, once(sh, WIRING_ANCHOR, "\n" + wiring_block(show(src, rev, TESTS_SH)) + WIRING_ANCHOR, "the wiring block's place"), None))
        sc = (dst / SCANNER).read_text(encoding="utf-8")
        out.append((SCANNER, once(sc, SCANNER_OLD, "", "the two NOT_SCANNED_ALWAYS entries"), None))
        lt = (dst / LAYOUT_TEST).read_text(encoding="utf-8")
        lt = once(lt, SCAN_SET_OLD, SCAN_SET_NEW, "the scan-set test")
        lt = once(lt, PIN_OLD, PIN_NEW, "the pin test")
        out.append((LAYOUT_TEST, lt, None))
    else:
        checker_n, passed_n = counts
        gates = (dst / GATES).read_text(encoding="utf-8")
        if '"name": "checker-layout-unit-tests"' in gates:
            raise SystemExit("refused: the gates file already declares the checker gate")
        new = ('    {\n      "name": "checker-layout-unit-tests",\n      "direction": "min",\n      "threshold": %d,\n'
               '      "command": "python3 tools/test_checker_layouts.py",\n      "extract": "Ran (\\\\d+) tests",\n'
               '      "why": "%s"\n    },\n' % (checker_n, WHY_CHECKERS % (checker_n, checker_n)))
        gates = once(gates, GATE_BEFORE, new + GATE_BEFORE, "the gates' place")
        pat = re.compile(r'("name": "tests-sh-passed",\n\s+"direction": "min",\n\s+"threshold": )(\d+),')
        if len(pat.findall(gates)) != 1:
            raise SystemExit("refused: gate tests-sh-passed: expected exactly 1 match")
        gates = pat.sub(lambda m: m.group(1) + "%d," % passed_n, gates)
        out.append((GATES, gates, None))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("rev")
    ap.add_argument("dst")
    ap.add_argument("--stage", required=True, choices=("tools", "suite"))
    ap.add_argument("--checker-count", type=int)
    ap.add_argument("--passed", type=int)
    args = ap.parse_args()
    dst = Path(args.dst)
    counts = (args.checker_count, args.passed)
    if any(c is not None for c in counts) and not all(c is not None for c in counts):
        raise SystemExit("refused: pass both of --checker-count and --passed, or neither")
    if args.stage == "tools":
        edits = stage_tools(args.src, args.rev, dst)
    else:
        edits = stage_suite(args.src, args.rev, dst, None if counts[0] is None else counts)
    for rel, text, mode in edits:
        write(dst, rel, text, mode)
    print("stage %s written: %s" % (args.stage, ", ".join(rel for rel, _, _ in edits)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
