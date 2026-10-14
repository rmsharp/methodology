#!/usr/bin/env python3
"""DRAFT, NOT YET USED TO BUILD A LAYER. Its mechanics were run once on `0aa1897` in a scratch clone (stage `tool` writes 3 files; stage `suite` 2,
then the gates file; the gates file parses); the suite stage's RESULT through the suite and the ratchet was not measured and its floors
(280, 300, 76) were placeholders for that test. `layer7-record.md` section 3 says what it has and has not shown. The layer it builds cannot be
green until the candidate carries the layout hunks of bin/check-ledger and bin/check-handoff and the prose layer (plan section 7, D5 amended):
RE-BASE this builder after those layers (the COPIES, tests.sh and gates anchors will have moved) and run `layer7-probe.sh` first.

Build PR2 Part 2's layer 7 (bin/migrate-layout: the tool that moves a legacy project's methodology files under
methodology/) in a candidate clone, as two checkpoint commits' worth of edits.

    python3 layer7-build.py <source-repo> <source-rev> <candidate-clone> --stage tool|suite
                            [--migrate-count N --passed N --layout-count M]   (suite stage, second run)

Reads each file from <source-rev> of <source-repo> (git show, never the working tree) and writes the stage into
<candidate-clone>, which must hold the previous stage's commit (the first stage: layer 6's `0aa1897`). It does NOT
commit. Every edit is computed before the first write, so a refusal leaves the clone untouched.

Two commits of three files each (the cap is five per commit, and each commit must leave the whole suite green):

  tool   bin/migrate-layout                 the tip's file, whole (new; mode 755)
         tools/test_layout_resolver.py      COPIES gains bin/migrate-layout (the block it embeds is asserted equal to the module's)
         tools/test_sync_layouts.py         the tip's file, whole: layer 6 left ONE assertion out because the tool did not exist yet
                                            (it asserts that bin/migrate-layout is a file); this puts it back
  suite  tools/test_migrate_layout.py       the tip's file, whole (new)
         bin/tests.sh                       a block that runs only its two fast classes (the rest is the gate's own command)
         .quality-gates.json                two gates over ONE command, as tests-sh-passed and tests-sh-failed are: the count
                                            (min) and the exit code (max 0), and the floors this tree measures

What this builder asserts about the candidate before writing anything (each a refusal, nothing written):

  The tool's inputs are the tip's. bin/sync, bin/status, bin/check-links and bin/_manifest_reader.py equal the source's
  blobs (layer 6 took them whole), tools/layout_resolver.py and tools/layout_fixtures.py equal the source's, and
  bin/_manifest.py parses to the same code once the docstring is dropped. The tool shells out to bin/status and reads
  bin/_manifest.py and tools/layout_fixtures.GENERATED, so a candidate whose copy of any of them differed would be
  testing the tool against tools it was not written against.

  The candidate's sync suite is the tip's with exactly the one assertion removed (the construction layer 6 used), so the
  tip's whole file is the candidate's plus one line and nothing else is overwritten.

Why two gates. measure_gate() ignores the exit code of a command that has an `extract`: a suite that prints "Ran 280
tests" and then FAILED still reads 280 and passes a min gate. For every other suite the count gate's `why` is true
("green/red is carried by tests-sh-passed") because bin/tests.sh runs the whole suite. This one is not wired in whole (its
command-level classes take minutes), so nothing carries its colour. The tip's gate says it is carried by tests-sh-failed;
for the command-level classes it is not. A second gate over the SAME command string, with no extract, measures the exit
code, and the ratchet's per-run memo runs the command once for both (the tests-sh pair's design).

Second run of the suite stage: `python3 tools/test_migrate_layout.py`, `python3 tools/test_layout_resolver.py` and
`bash bin/tests.sh` in the clone give the three counts; `--migrate-count N --passed N --layout-count M` writes only the
gates file.
"""
import argparse
import ast
import os
import re
import subprocess
import sys
from pathlib import Path

TOOL = "bin/migrate-layout"
SAME_AS_SOURCE = ("bin/sync", "bin/status", "bin/check-links", "bin/_manifest_reader.py",
                  "tools/layout_resolver.py", "tools/layout_fixtures.py")
SYNC_SUITE = "tools/test_sync_layouts.py"
LAYOUT_TEST = "tools/test_layout_resolver.py"
MIGRATE_SUITE = "tools/test_migrate_layout.py"
TESTS_SH = "bin/tests.sh"
GATES = ".quality-gates.json"

MIGRATE_ASSERT = '        self.assertTrue((REPO / "bin" / "migrate-layout").is_file())\n'

COPIES_OLD = ('              "bin/sync", "bin/status", "bin/check-links")   # the sync layer; each later layer appends the tools it carries\n')
COPIES_NEW = ('              "bin/sync", "bin/status", "bin/check-links",   # the sync layer\n'
              '              "bin/migrate-layout")   # the migration tool; each later layer appends the tools it carries\n')

WIRING_AFTER = '    fail "sync layer in both layouts unit tests failed"\nfi\n'
WIRING = (
    "\n"
    "# The migration tool: only its FAST classes run here, the rules as functions and the usage shapes (about a second).\n"
    "# The command-level suite (bin/migrate-layout run in scratch git projects the real bin/sync wrote: %(slow)s) is the\n"
    "# gate migrate-layout-unit-tests and is NOT wired in: run here it would roughly double this suite's time and push it\n"
    "# toward the 600 s a gate is given, and a gate that times out reads \"unmeasured\", so tests-sh-passed and\n"
    "# tests-sh-failed would then measure nothing. That suite's colour is the gate migrate-layout-unit-tests-failed.\n"
    'if python3 "$METHODOLOGY/tools/test_migrate_layout.py" TestThePureRules TestUsageAndNothingToDo >/dev/null 2>&1; then\n'
    '    pass "migration tool (bin/migrate-layout) rules and usage unit tests green (the command-level suite is the gate migrate-layout-unit-tests)"\n'
    "else\n"
    '    fail "migration tool (bin/migrate-layout) rules and usage unit tests failed"\n'
    "fi\n")
SLOW = "%d s measured on this tree"   # filled from --slow-seconds; the second run does not touch tests.sh

GATE_BEFORE = '    {\n      "name": "layout-literals",\n'
WHY_COUNT = ("bin/migrate-layout run as a command in scratch git projects the real bin/sync wrote (the plan, the refusals, the "
             "one commit and its rollback, the rewrites of CLAUDE.md, .gitignore and the two configs, the one ledger entry, the "
             "hits it leaves, the shard rehearsal, the checks before and after) and its rules as functions. Count never drops. "
             "bin/tests.sh runs only the two fast classes, so this gate's colour is migrate-layout-unit-tests-failed, not "
             "tests-sh-failed. %d is measured (Ran %d tests, OK).")
WHY_FAILED = ("the colour of the suite the gate above counts: a count gate passes over a red test (it still ran), and "
              "bin/tests.sh wires in only the fast classes of this suite, so nothing else would turn red. The same command as "
              "the count gate, no extract, so the exit code is the measurement and the ratchet runs the command once for both.")


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


def stage_tool(src, rev, dst):
    if (dst / TOOL).exists():
        raise SystemExit("refused: %s already exists in the candidate" % TOOL)
    for rel in SAME_AS_SOURCE:
        if (dst / rel).read_text(encoding="utf-8") != show(src, rev, rel):
            raise SystemExit("refused: the candidate's %s is not %s's, so the tool would be tested against inputs it was not written against" % (rel, rev))
    if code_without_docstring((dst / "bin/_manifest.py").read_text(encoding="utf-8")) != \
            code_without_docstring(show(src, rev, "bin/_manifest.py")):
        raise SystemExit("refused: bin/_manifest.py in the candidate differs from %s in more than the docstring" % rev)
    tip_sync = show(src, rev, SYNC_SUITE)
    if once(tip_sync, MIGRATE_ASSERT, "", "the migrate-layout assertion in the tip's sync suite") != \
            (dst / SYNC_SUITE).read_text(encoding="utf-8"):
        raise SystemExit("refused: the candidate's %s is not the tip's less the one assertion; taking the tip's file would overwrite more than that line" % SYNC_SUITE)
    lt = (dst / LAYOUT_TEST).read_text(encoding="utf-8")
    return [(TOOL, show(src, rev, TOOL), mode_of(src, rev, TOOL)),
            (LAYOUT_TEST, once(lt, COPIES_OLD, COPIES_NEW, "COPIES"), None),
            (SYNC_SUITE, tip_sync, mode_of(src, rev, SYNC_SUITE))]


def stage_suite(src, rev, dst, counts, slow):
    out = []
    if counts is None:
        if (dst / MIGRATE_SUITE).exists():
            raise SystemExit("refused: %s already exists in the candidate" % MIGRATE_SUITE)
        if not (dst / TOOL).is_file():
            raise SystemExit("refused: %s is not in the candidate; run --stage tool and commit it first" % TOOL)
        if slow is None:
            raise SystemExit("refused: pass --slow-seconds N (the measured time of the command-level suite) with the first suite run")
        out.append((MIGRATE_SUITE, show(src, rev, MIGRATE_SUITE), mode_of(src, rev, MIGRATE_SUITE)))
        sh = (dst / TESTS_SH).read_text(encoding="utf-8")
        out.append((TESTS_SH, once(sh, WIRING_AFTER, WIRING_AFTER + WIRING % {"slow": SLOW % slow}, "the wiring block's place"), None))
    else:
        migrate_n, passed_n, layout_n = counts
        gates = (dst / GATES).read_text(encoding="utf-8")
        if '"name": "migrate-layout-unit-tests"' in gates:
            raise SystemExit("refused: the gates file already declares a migrate-layout gate")
        new = ('    {\n      "name": "migrate-layout-unit-tests",\n      "direction": "min",\n      "threshold": %d,\n'
               '      "command": "python3 tools/test_migrate_layout.py",\n      "extract": "Ran (\\\\d+) tests",\n'
               '      "timeout_seconds": 3600,\n      "why": "%s"\n    },\n' % (migrate_n, WHY_COUNT % (migrate_n, migrate_n)) +
               '    {\n      "name": "migrate-layout-unit-tests-failed",\n      "direction": "max",\n      "threshold": 0,\n'
               '      "command": "python3 tools/test_migrate_layout.py",\n'
               '      "timeout_seconds": 3600,\n      "why": "%s"\n    },\n' % WHY_FAILED)
        gates = once(gates, GATE_BEFORE, new + GATE_BEFORE, "the gates' place")
        for name, now in (("tests-sh-passed", passed_n), ("layout-unit-tests", layout_n)):
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
    ap.add_argument("--stage", required=True, choices=("tool", "suite"))
    ap.add_argument("--migrate-count", type=int)
    ap.add_argument("--passed", type=int)
    ap.add_argument("--layout-count", type=int)
    ap.add_argument("--slow-seconds", type=int)
    args = ap.parse_args()
    dst = Path(args.dst)
    counts = (args.migrate_count, args.passed, args.layout_count)
    if any(c is not None for c in counts) and not all(c is not None for c in counts):
        raise SystemExit("refused: pass all three of --migrate-count, --passed and --layout-count, or none")
    if args.stage == "tool":
        edits = stage_tool(args.src, args.rev, dst)
    else:
        edits = stage_suite(args.src, args.rev, dst, None if counts[0] is None else counts, args.slow_seconds)
    for rel, text, mode in edits:
        write(dst, rel, text, mode)
    print("stage %s written: %s" % (args.stage, ", ".join(rel for rel, _, _ in edits)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
