#!/usr/bin/env python3
"""Port PR #94's fifth commit (`1082d3b`, 1.8.1) onto a tree that carries the layout trimmer (the
fork's BL-119): an abort BEFORE the proof's checks exits 3, the "did not finish" code, not 1, the FAIL
code. Used for fork `main` and for `pr2/candidate`, both 1.8.0 -> 1.8.1.

    python3 bl119-build.py <clone-root> <pinned-commit>

The clone's four files must hash to what <pinned-commit> holds (a clean tree at that commit), or the
script refuses and writes nothing. Every edit is an exact-once text replacement, applied to text in
memory and written only when all of them matched; every line this script inserts into the trimmer or
the apparatus is at most 100 characters. It edits four files and writes no ledger entry (the fork's
`main` carries one, the candidate none; both are written at commit time):

  starter-kit/methodology_trim.py   TRIM_VERSION 1.8.0 -> 1.8.1: ONLY the version line's prefix is
                                    replaced, so each tree keeps its own 1.8.0 history text after the
                                    new 1.8.1 paragraph; in VERIFY_TEMPLATE a shared `unfinished(why)`
                                    that prints the reason to stderr and exits 3, used by show() and
                                    readf()
  tools/test_methodology_trim.py    TestAnAbortBeforeTheChecksIsNotAVerdict (4 tests), the SAME text
                                    as `1082d3b` so the two lineages add identical lines; AND the one
                                    edit `1082d3b` did not need: the layout trimmer's test that pins
                                    the proof template to 1.7.0's (`TestTheLegacyLayoutIsByteForByte-
                                    WhatItWas`) maps the 1.8.1 abort block back to 1.7.0's text and
                                    asserts the block is the exact one in use, so every other byte
                                    stays pinned (renamed `..._and_the_abort_hunk_only`; same count)
  .quality-gates.json               trimmer-unit-tests 218 -> 222 (a tightening)
  FRAMEWORK_APPARATUS.md            the same sentence as `1082d3b`

The new-text blocks are copied from `bl118-build.py` (the build of `1082d3b`) by reading its source,
not retyped, and refused if that file's blocks are not found.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
PINNED = sys.argv[2]
HERE = Path(__file__).resolve().parent
FILES = ("starter-kit/methodology_trim.py", "tools/test_methodology_trim.py", ".quality-gates.json",
         "FRAMEWORK_APPARATUS.md")
TRIM, TESTS, GATES, APPARATUS = (ROOT / f for f in FILES)


def git(*args):
    return subprocess.run(["git"] + list(args), cwd=str(ROOT), stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, text=True).stdout.strip()


def refuse(msg):
    sys.stderr.write("bl119-build: REFUSED: %s\n" % msg)
    sys.exit(2)


# --- drift check: the four files must be exactly what the pinned commit holds ---------------------
for rel in FILES:
    want = git("rev-parse", "%s:%s" % (PINNED, rel))
    have = git("hash-object", rel)
    if want != have:
        refuse("%s is not the blob %s holds (%s != %s)" % (rel, PINNED, have[:12], want[:12]))

# --- the new text, taken from the build of 1082d3b ------------------------------------------------
# bl118-build.py runs its edits at import, so its blocks are read as text, not imported: each block
# is cut out between two literal markers and evaluated as the Python string literal it is.
src = (HERE / "bl118-build.py").read_text(encoding="utf-8")


def block(start, end):
    i = src.find(start)
    j = src.find(end, i + len(start)) if i >= 0 else -1
    if i < 0 or j < 0 or src.count(start) != 1:
        refuse("bl118-build.py: block %r not found exactly once" % start)
    return src[i + len(start):j]


NEW_HISTORY = eval(block("NEW_HISTORY = ", "\nNEW_VERSION = "))
NEW_SHOW = eval("'''" + block("NEW_SHOW = '''", "'''\n\n# --- 2.") + "'''")
NEW_CLASS = eval("'''" + block("NEW_CLASS = '''", "'''\n\n# --- 3.") + "'''")
NEW_APP = eval("(" + block("NEW_APP = (", ")\n\nEDITS") + ")")

PAD = " " * 25 + "# "
OLD_VERSION = 'TRIM_VERSION = "1.8.0"   # 1.8.0: '
NEW_VERSION = ('TRIM_VERSION = "1.8.1"   # ' + NEW_HISTORY[0] + "\n"
               + "".join(PAD + ln + "\n" for ln in NEW_HISTORY[1:])
               + " " * 25 + "#\n"
               + PAD + "1.8.0: ")

OLD_SHOW = '''def show(ref, path):
    p = subprocess.run(["git", "show", "%s:%s" % (ref, path)], stdout=subprocess.PIPE)
    if p.returncode:
        sys.exit("verify: cannot read %s:%s" % (ref, path))
    return p.stdout.decode("utf-8")


def readf(path):
    with open(path, "r", encoding="utf-8", newline="") as fh:
        return fh.read()
'''
OLD_MAIN = '\nif __name__ == "__main__":\n'
OLD_GATE = '      "name": "trimmer-unit-tests",\n      "direction": "min",\n      "threshold": 218,\n'
NEW_GATE = '      "name": "trimmer-unit-tests",\n      "direction": "min",\n      "threshold": 222,\n'
OLD_APP = "that is a claim about today's logic, not about the artifact that was shipped.\n\n"

# The layout trimmer's pin on the proof template (not in `1082d3b`: PR #94 has no such test). The
# fixture stays the true 1.7.0 capture; the 1.8.1 block is mapped back to 1.7.0's text, and the exact
# block is asserted present in today's template, so every other byte stays pinned.
PIN_CLASS_OLD = "class TestTheLegacyLayoutIsByteForByteWhatItWas(unittest.TestCase):\n"
PIN_CLASS_NEW = (
    "# The one deliberate change to the proof template since 1.7.0 (issue #93, TRIM_VERSION 1.8.1):\n"
    "# an abort before the checks exits 3 through `unfinished()`, where 1.7.0 exited 1 through\n"
    "# `sys.exit(text)`. The class below maps the first back to the second and pins everything else.\n"
    "ABORT_1_7_0 = r'''" + OLD_SHOW + "'''\n"
    "ABORT_1_8_1 = r'''" + NEW_SHOW + "'''\n\n\n" + PIN_CLASS_OLD)
PIN_OLD = '''    def test_the_proof_template_differs_from_1_7_0_in_its_parameter_lines_only(self):
        old = FIXTURE_PROOF_TEMPLATE.read_text(encoding="utf-8")
        new = mod.build_verify(CL, "CHANGELOG.md", self.P)

        def norm(t):
'''
PIN_NEW = '''    def test_the_proof_template_differs_from_1_7_0_in_its_parameter_lines_and_the_abort_hunk_only(self):
        """1.8.1 (issue #93, the abort code) is the one deliberate change to the template since 1.7.0.
        It is mapped back to 1.7.0's text below, so every other byte is still pinned; the two
        assertions before the mapping prove the exception is the exact block in use and that the
        1.7.0 capture does not have it, so the mapping cannot quietly stop meaning anything."""
        old = FIXTURE_PROOF_TEMPLATE.read_text(encoding="utf-8")
        new = mod.build_verify(CL, "CHANGELOG.md", self.P)
        self.assertIn(ABORT_1_8_1, new)
        self.assertNotIn(ABORT_1_8_1, old)

        def norm(t):
            t = t.replace(ABORT_1_8_1, ABORT_1_7_0)
'''
for _blk in (OLD_SHOW, NEW_SHOW):
    if "'''" in _blk or _blk.endswith("\\"):
        refuse("a block cannot be carried in a raw triple-quoted string")

EDITS = [
    (TRIM, [(OLD_VERSION, NEW_VERSION), (OLD_SHOW, NEW_SHOW)]),
    (TESTS, [(OLD_MAIN, NEW_CLASS + OLD_MAIN), (PIN_CLASS_OLD, PIN_CLASS_NEW), (PIN_OLD, PIN_NEW)]),
    (GATES, [(OLD_GATE, NEW_GATE)]),
    (APPARATUS, [(OLD_APP, NEW_APP)]),
]

out = {}
for path, pairs in EDITS:
    text = path.read_text(encoding="utf-8")
    for old, new in pairs:
        n = text.count(old)
        if n != 1:
            refuse("%s: a search text occurs %d times, not once:\n%s" % (path.name, n, old[:120]))
        text = text.replace(old, new, 1)
    out[path] = text

for ln in (NEW_VERSION + NEW_SHOW).splitlines():
    if len(ln) > 100:
        refuse("a line this script inserts into the trimmer is %d characters:\n%s" % (len(ln), ln))
for ln in NEW_APP.splitlines():
    if len(ln) > 100:
        refuse("an apparatus line is %d characters:\n%s" % (len(ln), ln))

for path, text in out.items():
    path.write_text(text, encoding="utf-8")
    print("wrote %s" % path.relative_to(ROOT))
print("bl119-build: 4 files edited; nothing committed")
