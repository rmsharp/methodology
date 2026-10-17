#!/usr/bin/env python3
"""The 33rd commit on pr2/candidate (the build session, 2026-10-17): restore two of upstream's dashboard tests that
the series dropped with their class, and raise dashboard-unit-tests 395 to 397 (his decision F1, draft4-record.md
section 5).

Run in a clone of pr2/candidate checked out at a62bfec:  python3 -I restore33-build.py REPO [UPSTREAM=f34769f]

It refuses, writing nothing, if either file is not the blob it was derived from, if the note it replaces is not found
exactly once, if upstream's class is not where and what it expects, or if its own output fails the proof below. It
does not commit; the message is restore33-message.txt. Generates no bytecode.

The proof it runs on its own output: the gate manifest parses and differs from the old one in exactly one value,
dashboard-unit-tests' threshold, 395 to 397, on a `min` gate (a tightening; every other key, threshold and command
equal); the test file parses, and its top-level statements equal the old ones with exactly one insertion, a class
TestCliRemedyProportionality whose syntax tree equals the one parsed from upstream's own lines (the class header
through the second test's last line, taken from `git show <upstream>:tools/test_methodology_dashboard.py`), with the
functions setUp, tearDown, _project and the two tests and nothing else; the file gains exactly two `def test_` lines;
no new comment line is over 100 characters.
"""
import ast
import json
import subprocess
import sys

sys.dont_write_bytecode = True

REPO = sys.argv[1]
UP = sys.argv[2] if len(sys.argv) > 2 else "f34769f"
TESTS, GATES = "tools/test_methodology_dashboard.py", ".quality-gates.json"
BEFORE = {
    TESTS: "4d61598387b2464be884c811a17f5ed9b7e49d75",   # 431,309 B at a62bfec
    GATES: "fa790fe08414819604c99c36b98fabac494ecd7c",   # 8,317 B at a62bfec
}
CLASS = "TestCliRemedyProportionality"
WANT_FUNCS = ["setUp", "tearDown", "_project",
              "test_bare_dry_run_refuses_instead_of_writing", "test_a_normal_run_still_writes"]
NOT_CARRIED = "test_stale_warning_leads_with_the_project_scoped_remedy"

NOTE_OLD = (
    "    # NOTE: `TestCliRemedyProportionality` (issue #67 / PR #73) is deliberately not carried here --\n"
    "    # the `--sync [DIR]` single-project scope took a different, more general\n"
    "    # design (not a bare `cp`), and its behavior is already\n"
    "    # covered more thoroughly by the existing Row 13/14 tests below (`test_sync_accepts_a_single_\n"
    "    # target_directory`, `test_bare_dry_run_without_sync_errors_and_writes_nothing`,\n"
    "    # `test_sync_end_to_end_via_main_writes_only_the_target`, etc.). The earlier\n"
    "    # `test_stale_warning_leads_with_the_project_scoped_remedy` asserts a literal `\"cp \"` in the\n"
    "    # stale-copy message, which the `--sync [DIR]`-based message does not contain by\n"
    "    # design -- porting that assertion would fail against a correct, already-tested design, not\n"
    "    # catch a real defect.\n"
)
NOTE_NEW = (
    "    # NOTE: upstream's third test in this class is deliberately not carried:\n"
    "    # `test_stale_warning_leads_with_the_project_scoped_remedy` asserts a literal `\"cp \"` in the\n"
    "    # stale-copy warning, and this branch's warning prints a `--sync` scoped to the one project\n"
    "    # instead, so it would fail against the design that replaced it, not catch a defect. The two\n"
    "    # tests above assert behaviour this branch keeps (a bare `--dry-run` exits 2 and writes\n"
    "    # nothing; a plain run writes dashboard.html) and are restored as upstream wrote them.\n"
)
OLD_GATE, NEW_GATE = '"threshold": 395,', '"threshold": 397,'


def git(*a, stdin=None):
    r = subprocess.run(["git", "-C", REPO, *a], input=stdin, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("refused: git %s: %s" % (" ".join(a), r.stderr.strip()))
    return r.stdout


def read(rel):
    with open("%s/%s" % (REPO, rel), encoding="utf-8", newline="") as f:
        return f.read()


def once(text, old, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit("refused: %s found %d times (expected 1)" % (label, n))


def funcs(cls):
    return [n.name for n in cls.body if isinstance(n, ast.FunctionDef)]


old = {rel: read(rel) for rel in BEFORE}
for rel, blob in BEFORE.items():
    if git("hash-object", "--stdin", stdin=old[rel]).strip() != blob:
        raise SystemExit("refused: %s is not the blob this was derived from (%s)" % (rel, blob[:8]))
once(old[TESTS], NOTE_OLD, "the note the class replaces")
once(old[GATES], OLD_GATE, "the 395 threshold")

# upstream's class, located by its header and ended before its third test; trailing blank lines dropped
up_lines = git("show", "%s:%s" % (UP, TESTS)).split("\n")
heads = [i for i, l in enumerate(up_lines) if l.startswith("class %s(" % CLASS)]
stale = [i for i, l in enumerate(up_lines) if l.startswith("    def %s(" % NOT_CARRIED)]
if len(heads) != 1 or len(stale) != 1 or stale[0] < heads[0]:
    raise SystemExit("refused: upstream's class or its third test not found once (%r, %r)" % (heads, stale))
block = up_lines[heads[0]:stale[0]]
while block and block[-1] == "":
    block.pop()
up_cls = ast.parse("\n".join(block) + "\n").body
if len(up_cls) != 1 or not isinstance(up_cls[0], ast.ClassDef) or funcs(up_cls[0]) != WANT_FUNCS:
    raise SystemExit("refused: upstream's lines %d to %d are not the class with %r" % (heads[0] + 1, stale[0], WANT_FUNCS))
print("upstream %s:%s lines %d to %d: class %s with %s" % (UP, TESTS, heads[0] + 1, heads[0] + len(block), CLASS, ", ".join(WANT_FUNCS)))

new = {
    TESTS: old[TESTS].replace(NOTE_OLD, "\n" + "\n".join(block) + "\n\n" + NOTE_NEW),
    GATES: old[GATES].replace(OLD_GATE, NEW_GATE),
}

# proof 1: the manifest differs in exactly one threshold, on a min gate
bg, ag = json.loads(old[GATES]), json.loads(new[GATES])
changed = [(b["name"], k, b[k], a[k]) for b, a in zip(bg["gates"], ag["gates"]) for k in b if b[k] != a[k]]
if len(bg["gates"]) != len(ag["gates"]) or changed != [("dashboard-unit-tests", "threshold", 395, 397)]:
    raise SystemExit("refused: the gate manifest differs in more than the one threshold: %r" % (changed,))
if {k: v for k, v in bg.items() if k != "gates"} != {k: v for k, v in ag.items() if k != "gates"}:
    raise SystemExit("refused: the manifest's header keys changed")
gate = [g for g in ag["gates"] if g["name"] == "dashboard-unit-tests"][0]
if gate["direction"] != "min":
    raise SystemExit("refused: dashboard-unit-tests is not a min gate")

# proof 2: the test file's top-level statements gain exactly upstream's class and nothing else changes
ob = [ast.dump(n) for n in ast.parse(old[TESTS]).body]
nb = [ast.dump(n) for n in ast.parse(new[TESTS]).body]
if len(nb) != len(ob) + 1:
    raise SystemExit("refused: %d top-level statements became %d" % (len(ob), len(nb)))
i = next(k for k in range(len(nb)) if k >= len(ob) or nb[k] != ob[k])
if nb[:i] != ob[:i] or nb[i + 1:] != ob[i:]:
    raise SystemExit("refused: more than one top-level statement changed")
if nb[i] != ast.dump(up_cls[0]):
    raise SystemExit("refused: the inserted class is not upstream's syntax tree")
if new[TESTS].count("    def test_") - old[TESTS].count("    def test_") != 2:
    raise SystemExit("refused: the file does not gain exactly two test methods")
for line in NOTE_NEW.splitlines():
    if len(line) > 100:
        raise SystemExit("refused: a new comment line is %d characters" % len(line))

for rel in (TESTS, GATES):
    with open("%s/%s" % (REPO, rel), "w", encoding="utf-8", newline="") as f:
        f.write(new[rel])
    print("wrote %-36s %7d B -> %7d B  blob %s" % (rel, len(old[rel].encode()), len(new[rel].encode()),
                                                  git("hash-object", rel).strip()[:8]))
print("proof: manifest differs in exactly dashboard-unit-tests.threshold 395 -> 397 (min); the test file's top-level "
      "statements gain exactly upstream's %s (%d lines, %s) and nothing else changes" % (CLASS, len(block), ", ".join(WANT_FUNCS)))
