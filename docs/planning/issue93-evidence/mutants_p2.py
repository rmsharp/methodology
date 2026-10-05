"""Mutation check for P2 of docs/planning/issue93-trimmer-proof-false-red-plan.md (S265).

Applies ONE textual mutant at a time to a scratch copy of starter-kit/methodology_trim.py and runs the
layer's test class against it. KILLED = at least one test in the class fails; SURVIVED = none does;
INVALID = the search text does not occur exactly once in the pristine source (never scored as a kill).
Where an intended test is named the report says whether that test was among the failures. Nothing under
the repository is written: the copy lives in a temp directory.

    python3 docs/planning/issue93-evidence/mutants_p2.py [L1 | L2 | L3 | all]

L1 = the proof's stub label and exit 4        (TestVerifyShNamesAStubFinalize,            18 mutants)
L2 = the write-time guard                     (TestWriteTimeGuardForAStubFinalize,        14 mutants)
L3 = the shared wording of the timing rule    (TestTheTimingRuleIsStatedTheSameEverywhere, 5 mutants)

The mutant lists were written against the tree at S265's `1214511`; a later edit to the trimmer can make a
search text stop matching, and the runner then says INVALID rather than passing silently.
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CLASSES = {"L1": "TestVerifyShNamesAStubFinalize",
           "L2": "TestWriteTimeGuardForAStubFinalize",
           "L3": "TestTheTimingRuleIsStatedTheSameEverywhere"}

# --- L1 ------------------------------------------------------------
GATE = "stub_finalized = (not STUB.search(successor) and not other_fails and rebuilt == br[1:])"

MUTANTS_L1 = [
    # --- the label itself ------------------------------------------------------------------
    ("label never fires", GATE, "stub_finalized = False", "is_labelled_and_exits_4"),
    ("exit 1 for the label",
     "sys.exit(4 if stub_finalized else 1)", "sys.exit(1)", "is_labelled_and_exits_4"),
    ("exit 0 for the label (the D2(ii) reversal)",
     "sys.exit(4 if stub_finalized else 1)", "sys.exit(0 if stub_finalized else 1)", "is_labelled_and_exits_4"),
    ("generic L1/L3 pair kept beside the label",
     "    fails[:] = [f for f in fails if not (f.startswith(\"L1 \") or f.startswith(\"L3 \"))]\n    fails.append(\"record 0 was",
     "    fails.append(\"record 0 was", "is_labelled_and_exits_4"),
    ("other-record count off by one",
     "% (len(absent_records[0].encode(\"utf-8\")), len(br) - 1))",
     "% (len(absent_records[0].encode(\"utf-8\")), len(br) - 2))", "is_labelled_and_exits_4"),
    ("stub size reported in characters",
     "% (len(absent_records[0].encode(\"utf-8\")), len(br) - 1))",
     "% (len(absent_records[0]) + 1, len(br) - 1))", "is_labelled_and_exits_4"),
    # --- each narrowing condition of the discriminator ------------------------------------
    ("label ignores the pre-trim marker (always true)",
     "if fails and frontier_edit and STUB is not None and STUB.search(absent_records[0]):",
     "if fails and frontier_edit and STUB is not None:", "complete_record_0_edited"),
    ("label ignores that the successor is still a stub",
     GATE, "stub_finalized = (not other_fails and rebuilt == br[1:])", "still_pending_after_the_trim"),
    ("label ignores other failures (L2 etc.)",
     GATE, "stub_finalized = (not STUB.search(successor) and rebuilt == br[1:])",
     "front_matter_edit"),
    ("label ignores the order of the other records",
     GATE, "stub_finalized = (not STUB.search(successor) and not other_fails)", "reorder_of_other_records"),
    ("label ignores that the other records match as a set",
     GATE, "stub_finalized = (not STUB.search(successor) and not other_fails and sorted(rebuilt) == sorted(br[1:]))",
     "reorder_of_other_records"),
    # --- the marker and how it travels ---------------------------------------------------
    ("HANDOFFS marker matches a mid-line quote",
     'stub_marker=re.compile(r"^status: pending\\s*$", re.M),',
     'stub_marker=re.compile(r"status: pending", re.M),', "grammar_carries"),
    ("HANDOFFS marker not line-anchored at the start",
     'stub_marker=re.compile(r"^status: pending\\s*$", re.M),',
     'stub_marker=re.compile(r"status: pending\\s*$", re.M),', "grammar_carries"),
    ("CHANGELOG declares a marker",
     'seed_negation=None,\n    ),\n    "HANDOFFS.md"',
     'seed_negation=None,\n        stub_marker=re.compile(r"^### .*\\(in progress\\)", re.M),\n    ),\n    "HANDOFFS.md"',
     "grammar_carries"),
    ("marker is not carried into the proof",
     '("@@STUB@@", repr(spec.stub_marker.pattern if spec.stub_marker else ""))',
     '("@@STUB@@", repr(""))', "is_labelled_and_exits_4"),
    ("an empty pattern compiles to match-everything",
     "STUB = re.compile(STUB_PATTERN, re.M) if STUB_PATTERN else None",
     "STUB = re.compile(STUB_PATTERN, re.M)", "declares_no_stub_marker"),
    ("the no-marker sentence is dropped from the note",
     '" This ledger declares no stub marker, so a pending-stub finalize cannot be told from "\n           "any other edit of record 0."',
     '""', "declares_no_stub_marker"),
    ("the stub note's exit-4 sentence is dropped",
     '"exit 4, not 1: a recognised stub finalize is NAMED, but it is still a FAIL, because a "',
     '"a recognised stub finalize is NAMED, but it is still a FAIL, because a "', None),
]

# --- L2 ------------------------------------------------------------
B_COND = 'if marker.search(h0) and h0.replace("\\r\\n", "\\n") not in now:'

MUTANTS_L2 = [
    ("order A never fires",
     "    if marker.search(records[0]):\n        result.add(\n            \"FRONTIER_PENDING_STUB\"",
     "    if False:\n        result.add(\n            \"FRONTIER_PENDING_STUB\"", "pending_stub_at_record_0"),
    ("order A fires on any record 0",
     "    if marker.search(records[0]):\n        result.add(\n            \"FRONTIER_PENDING_STUB\"",
     "    if True:\n        result.add(\n            \"FRONTIER_PENDING_STUB\"", "clean_ledger"),
    ("order B never fires", B_COND, "if False:", "finalized_in_the_tree"),
    ("order B fires whenever HEAD's stub is not record 0 now",
     B_COND, 'if marker.search(h0) and h0.replace("\\r\\n", "\\n") != records[0].replace("\\r\\n", "\\n"):',
     "prepended_above"),
    ("order B ignores whether HEAD's record 0 was a stub",
     B_COND, 'if h0.replace("\\r\\n", "\\n") not in now:', "never_a_stub"),
    ("order B drops the CRLF fold",
     B_COND, "if marker.search(h0) and h0 not in {r for r in records}:", "converts_line_endings"),
    ("order B crashes without a HEAD version",
     "    if head is None:\n        return                      # no committed version to compare: order B cannot be judged",
     "    if False:\n        return", "untracked_ledger"),
    ("a ledger with no marker is not skipped",
     "    if marker is None or not records:\n        return",
     "    if not records:\n        return", "declares_no_stub_marker"),
    ("order A refuses (exit 2)",
     "or trim before the claim. \"\n            \"Advisory: nothing is refused.\" % (live_rel, TRIM_TIMING_RULE.capitalize()))",
     "or trim before the claim. \"\n            \"Advisory: nothing is refused.\" % (live_rel, TRIM_TIMING_RULE.capitalize()), exit_code=2)",
     "does_not_refuse"),
    ("the guard is not called at all",
     "    check_stub_frontier(repo, path, spec, records, result)\n", "", "pending_stub_at_record_0"),
    ("the guard is called before the cut is known to archive anything",
     "    check_stub_frontier(repo, path, spec, records, result)\n\n    dates =",
     "\n    dates =", "pending_stub_at_record_0"),
    ("way out 1 is dropped from the message",
     "either finalize \"\n            \"record 0 and commit that first, then trim in its own commit, or trim before the claim. ",
     "\"\n            \"", "names_both_ways_out"),
    ("way out 2 is dropped from the message",
     "then trim in its own commit, or trim before the claim. ", "then trim in its own commit. ",
     "names_both_ways_out"),
    ("the timing rule is dropped from the constant",
     "-- before the claim, or after the finalize is \"\n                    \"committed -- never in the same commit\")",
     "\"\n                    \"-- never in the same commit\")", "names_both_ways_out"),
]

# --- L3 ------------------------------------------------------------
MUTANTS_L3 = [
    ("generic note drops the rule",
     '"is complete -- before the claim, or after the finalize is committed -- never in the "\n        "same commit. This does NOT confirm',
     '"is complete. This does NOT confirm', "generic_frontier_note"),
    ("generic note restores the retired claim",
     "That bundling is not this framework's practice: trim while record 0 ",
     "This repository's own practice bundles a finalize: trim while record 0 ", "generic_frontier_note"),
    ("stub note drops the rule",
     '"To avoid it, trim while record 0 is complete -- before the claim, or after the finalize "\n        "is committed -- never in the same commit.")',
     '"To avoid it, trim while record 0 is complete.")', "stub_note"),
    ("template comment restores the retired claim",
     "# BL-27 fix 2: a same-commit close-out bundling (a session's own frontier receipt going",
     "# BL-27 fix 2: a same-commit close-out bundling (this repo's own established practice -- a session's own frontier receipt going",
     "no_longer_asserts"),
    ("writer constant drops the rule",
     "-- before the claim, or after the finalize is \"\n                    \"committed -- never in the same commit\")",
     "\"\n                    \"-- never in the same commit\")", "constant_the_writer_uses"),
]


def run_layer(layer, mutants):
    src = (REPO / "starter-kit" / "methodology_trim.py").read_text(encoding="utf-8")
    killed = survived = invalid = 0
    with tempfile.TemporaryDirectory() as td:
        tree = Path(td)
        (tree / "tools").mkdir()
        (tree / "starter-kit").mkdir()
        shutil.copy(str(REPO / "tools" / "test_methodology_trim.py"), str(tree / "tools"))
        shutil.copy(str(REPO / "FRAMEWORK_APPARATUS.md"), str(tree))
        target = tree / "starter-kit" / "methodology_trim.py"
        for name, old, new, intended in mutants:
            if src.count(old) != 1:
                print("INVALID  %-52s (search text occurs %d times)" % (name, src.count(old)))
                invalid += 1
                continue
            target.write_text(src.replace(old, new, 1), encoding="utf-8")
            p = subprocess.run([sys.executable, "tools/test_methodology_trim.py", CLASSES[layer]], cwd=str(tree),
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            failed = re.findall(r"^(?:FAIL|ERROR): (test_\w+)", p.stdout, re.M)
            if failed:
                killed += 1
                hit = ""
                if intended:
                    hit = "  intended test %s" % ("FAILED" if any(intended in f for f in failed) else "DID NOT FAIL")
                print("KILLED   %-52s by %d test(s)%s" % (name, len(failed), hit))
            else:
                survived += 1
                print("SURVIVED %-52s" % name)
    print("%s: %d killed, %d survived, %d invalid, of %d\n" % (layer, killed, survived, invalid, len(mutants)))
    return survived + invalid


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    lists = {"L1": MUTANTS_L1, "L2": MUTANTS_L2, "L3": MUTANTS_L3}
    chosen = list(lists) if which == "all" else [which]
    bad = sum(run_layer(layer, lists[layer]) for layer in chosen)
    sys.exit(1 if bad else 0)
