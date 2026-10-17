"""Mutation check for the fourth commit of the #93 fix (S335): SESSION_NOTES.md joins the ledger table,
and the proof prints the record-0 diff.

Applies ONE textual mutant at a time to a scratch copy of the tree's starter-kit/methodology_trim.py and
runs the layer's tests against it. KILLED = at least one test fails; SURVIVED = none does; INVALID = the
search text does not occur exactly once in the pristine source (never scored as a kill). Where an intended
test is named the report says whether that test was among the failures. Nothing under the tree is written:
the copy lives in a temp directory.

    python3 mutants_s335.py <worktree-root>
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
TESTS = ["TestSessionNotesIsATrimmableLedger",
         "TestReverify.test_the_stub_marker_comes_from_the_ledger_table_by_live_basename",
         "TestFixtureControls.test_seed_files_hold_zero_records_under_the_declared_grammar"]

MARKER = r'        stub_marker=re.compile(r"(?ms)\A(?=.*^\*\*Status:\*\* Session claimed\b)(?=.*\(IN PROGRESS\))", re.M),' + "\n    ),\n}\n"
START = r'            r"^### (?:Session \d+ Handoff Evaluation \(by Session \d+\)|What Session \d+ Did\b)"),' + "\n"
DATE_LABELLED = (r'    m = re.search(r"\*\*(?:Started(?:/Completed)?|Completed|Date)\s*:\*\*\s*(\d{4}-\d{2}-\d{2})", text)'
                 + "\n    if m:\n        return m.group(1)\n")
DATE_FALLBACK = r'    m = re.search(r"\d{4}-\d{2}-\d{2}", text)' + "\n    return m.group(0) if m else None\n"
SUCCESSOR = ("successor = (next(a for a in added_records if anchor(a) == anchor(absent_records[0]))\n"
             "             if frontier_edit else None)\n")
IF_FRONTIER = "if frontier_edit:\n    # Issue #93's first suggestion."
UDIFF = ("    diff = list(difflib.unified_diff(absent_records[0].splitlines(keepends=True),\n"
         "                                     successor.splitlines(keepends=True),\n")
HEADER = ('    print("DIFF: record 0, before the trim commit (-) against the record that replaced it (+), "\n'
          '          "%d line(s):" % len(diff))\n')
WRITE = ('    for ln in diff:\n        sys.stdout.write(ln if ln.endswith("\\n") else ln + "\\n")\n')
SPF = ('    spec = LEDGERS.get(Path(live_rel).name)\n'
       '    return spec.stub_marker.pattern if spec is not None and spec.stub_marker else ""')

# (name, [(old, new), ...], intended-test fragment or None)
MUTANTS = [
    ("marker needs only the status line",
     [(MARKER, MARKER.replace(r'(?ms)\A(?=.*^\*\*Status:\*\* Session claimed\b)(?=.*\(IN PROGRESS\))',
                              r'^\*\*Status:\*\* Session claimed\b.*$'))], "needs_both"),
    ("marker needs only the tag",
     [(MARKER, MARKER.replace(r'(?ms)\A(?=.*^\*\*Status:\*\* Session claimed\b)(?=.*\(IN PROGRESS\))',
                              r'\(IN PROGRESS\)'))], "needs_both"),
    ("status line not anchored at a line start",
     [(MARKER, MARKER.replace(r'(?=.*^\*\*Status', r'(?=.*\*\*Status'))], "needs_both"),
    ("no marker for SESSION_NOTES.md",
     [(MARKER, "    ),\n}\n")], "labelled_exits_4"),
    ("record grammar drops the evaluation branch",
     [(START, r'            r"^### What Session \d+ Did\b"),' + "\n")], "partitions"),
    ("record grammar drops the word boundary after Did",
     [(START, START.replace(r"Did\b)", "Did)"))], "runners_two_record_shapes"),
    ("footer declared as separator",
     [('        footer_mode="none",\n        date_of_record=_session_notes_date,\n',
       '        footer_mode="separator",\n        date_of_record=_session_notes_date,\n')], "runners_two_record_shapes"),
    ("record date: labelled date ignored",
     [(DATE_LABELLED, "")], "labelled_date"),
    ("record date: fallback dropped",
     [(DATE_FALLBACK, "    return None\n")], "labelled_date"),
    ("stub_pattern_for ignores the table",
     [(SPF, '    return ""')], "substitutes_it_from_the_table"),
    ("diff never printed",
     [(IF_FRONTIER, IF_FRONTIER.replace("if frontier_edit:", "if False:"))], "shows_the_diff"),
    ("diff printed for any missing record",
     [(SUCCESSOR, SUCCESSOR.replace("if frontier_edit else None", "if frontier_edit else (added_records[0] if added_records else \"\")")),
      (IF_FRONTIER, IF_FRONTIER.replace("if frontier_edit:", "if absent_records:"))], "other_than_the_frontier"),
    ("diff printed only for the recognised finalize",
     [(IF_FRONTIER, IF_FRONTIER.replace("if frontier_edit:", "if stub_finalized:"))], "generic_frontier_edit"),
    ("diff reversed (after against before)",
     [(UDIFF, UDIFF.replace("absent_records[0].splitlines(keepends=True),\n                                     successor.splitlines(keepends=True),",
                            "successor.splitlines(keepends=True),\n                                     absent_records[0].splitlines(keepends=True),"))], "shows_the_diff"),
    ("diff header line dropped",
     [(HEADER, "")], "shows_the_diff"),
    ("diff lines not written",
     [(WRITE, "")], "shows_the_diff"),
    ("successor is the first added record, not the one with record 0's anchor",
     [(SUCCESSOR, "successor = (added_records[0] if frontier_edit else None)\n")], "shows_the_diff"),
]


def main():
    src = (ROOT / "starter-kit" / "methodology_trim.py").read_text(encoding="utf-8")
    killed = survived = invalid = 0
    with tempfile.TemporaryDirectory() as td:
        tree = Path(td)
        (tree / "tools").mkdir()
        (tree / "starter-kit").mkdir()
        shutil.copy(str(ROOT / "tools" / "test_methodology_trim.py"), str(tree / "tools"))
        shutil.copy(str(ROOT / "FRAMEWORK_APPARATUS.md"), str(tree))
        for seed in ("SESSION_NOTES.md", "HANDOFFS.md", "CHANGELOG.md"):
            shutil.copy(str(ROOT / "starter-kit" / seed), str(tree / "starter-kit" / seed))
        target = tree / "starter-kit" / "methodology_trim.py"
        for name, pairs, intended in MUTANTS:
            text = src
            bad = [old for old, _new in pairs if src.count(old) != 1]
            if bad:
                print("INVALID  %-62s (a search text occurs %d times)" % (name, src.count(bad[0])))
                invalid += 1
                continue
            for old, new in pairs:
                text = text.replace(old, new, 1)
            if text == src:
                print("INVALID  %-62s (the mutant equals the source)" % name)
                invalid += 1
                continue
            target.write_text(text, encoding="utf-8")
            p = subprocess.run([sys.executable, "tools/test_methodology_trim.py"] + TESTS, cwd=str(tree),
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            failed = re.findall(r"^(?:FAIL|ERROR): (test_\w+)", p.stdout, re.M)
            if failed:
                killed += 1
                hit = ""
                if intended:
                    hit = "  intended test %s" % ("FAILED" if any(intended in f for f in failed) else "DID NOT FAIL")
                print("KILLED   %-62s by %d test(s)%s" % (name, len(failed), hit))
            else:
                survived += 1
                print("SURVIVED %-62s" % name)
    print("%d killed, %d survived, %d invalid, of %d" % (killed, survived, invalid, len(MUTANTS)))
    return 1 if (survived or invalid) else 0


if __name__ == "__main__":
    sys.exit(main())
