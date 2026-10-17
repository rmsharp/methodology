#!/usr/bin/env python3
"""Build the fifth commit of the issue #93 fix (the fork's BL-118): an abort BEFORE the proof's
checks exits 3, the "did not finish" code, not 1, the FAIL code.

    python3 bl118-build.py <clone-root>

The clone must be at PR #94's head `2308553` (checked by blob: the two files this script edits must
hash to what that commit holds, or the script refuses and writes nothing). Every edit is an exact-once
text replacement, applied to text in memory and written only when all of them matched; every line this
script inserts into the trimmer is at most 100 characters. It edits four files and writes no ledger
entry (the entry carries measured numbers and is written at commit time):

  starter-kit/methodology_trim.py   TRIM_VERSION 1.8.0 -> 1.8.1 with its history paragraph; in
                                    VERIFY_TEMPLATE a shared `unfinished(why)` that prints the reason
                                    to stderr and exits 3, used by show() and readf()
  tools/test_methodology_trim.py    TestAnAbortBeforeTheChecksIsNotAVerdict (4 tests)
  .quality-gates.json               trimmer-unit-tests 199 -> 203 (a tightening)
  FRAMEWORK_APPARATUS.md            one sentence: a proof that cannot read git exits 3, no verdict
"""
import subprocess
import sys
from pathlib import Path

PINNED = "2308553"
ROOT = Path(sys.argv[1]).resolve()
TRIM = ROOT / "starter-kit" / "methodology_trim.py"
TESTS = ROOT / "tools" / "test_methodology_trim.py"
GATES = ROOT / ".quality-gates.json"
APPARATUS = ROOT / "FRAMEWORK_APPARATUS.md"


def git(*args):
    return subprocess.run(["git"] + list(args), cwd=str(ROOT), stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, text=True).stdout.strip()


def refuse(msg):
    sys.stderr.write("bl118-build: REFUSED: %s\n" % msg)
    sys.exit(2)


# --- drift check: the four files must be exactly what 2308553 holds --------------------------
for rel in ("starter-kit/methodology_trim.py", "tools/test_methodology_trim.py", ".quality-gates.json",
            "FRAMEWORK_APPARATUS.md"):
    want = git("rev-parse", "%s:%s" % (PINNED, rel))
    have = git("hash-object", rel)
    if want != have:
        refuse("%s is not the blob %s holds (%s != %s)" % (rel, PINNED, have[:12], want[:12]))

# --- 1. the trimmer -------------------------------------------------------------------------------
OLD_VERSION = ('TRIM_VERSION = "1.8.0"   # 1.8.0: issue #93, the gap the first three left -- '
               "seven of the adopter's\n")
PAD = " " * 25 + "# "
NEW_HISTORY = [
    "1.8.1: issue #93, the abort code -- a proof that could not read an",
    'artifact from git ended in `sys.exit("verify: cannot read ...")`, which',
    "prints the text and exits 1, the FAIL code, so a proof that had compared",
    "nothing read as a trim that lost something (seen once in a 54-shard",
    "`--reverify` sweep over a partial clone: one blob fetch failed and the",
    "shard read FAIL; exit 0 on the re-run). Every abort before the checks --",
    "a `git show` that fails, a live or shard file that cannot be read -- now",
    "prints its reason to stderr and exits 3: the code the shell head already",
    "uses when it cannot reach the repository root, and the code the legend",
    'of `--reverify` gives "the proof did not finish". Patch, not minor: no',
    "verdict on any readable tree changes, frozen proofs keep their bytes, and",
    "`--reverify` renders today's template, so it reads 3 where a frozen",
    "script read 1.",
]
NEW_VERSION = ('TRIM_VERSION = "1.8.1"   # ' + NEW_HISTORY[0] + "\n"
               + "".join(PAD + ln + "\n" for ln in NEW_HISTORY[1:])
               + " " * 25 + "#\n"
               + PAD + "1.8.0: issue #93, the gap the first three left -- seven of the adopter's\n")

OLD_SHOW = '''def show(ref, path):
    p = subprocess.run(["git", "show", "%s:%s" % (ref, path)], stdout=subprocess.PIPE)
    if p.returncode:
        sys.exit("verify: cannot read %s:%s" % (ref, path))
    return p.stdout.decode("utf-8")


def readf(path):
    with open(path, "r", encoding="utf-8", newline="") as fh:
        return fh.read()
'''
NEW_SHOW = '''def unfinished(why):
    # An abort BEFORE the checks is not a verdict. `sys.exit("<text>")` prints the text and exits
    # 1, which is this script's FAIL code, so a proof that had compared nothing read as a trim that
    # lost something. Exit 3 is "the proof did not finish": the code the shell head above uses when
    # it cannot reach the repository root, and the code `--reverify`'s legend gives this case.
    sys.stderr.write("verify: %s -- the proof did not finish; this is not a verdict (exit 3)\\n"
                     % why)
    sys.exit(3)


def show(ref, path):
    p = subprocess.run(["git", "show", "%s:%s" % (ref, path)], stdout=subprocess.PIPE)
    if p.returncode:
        unfinished("cannot read %s:%s" % (ref, path))
    return p.stdout.decode("utf-8")


def readf(path):
    try:
        with open(path, "r", encoding="utf-8", newline="") as fh:
            return fh.read()
    except OSError as e:
        unfinished("cannot read %s (%s)" % (path, e.strerror or e))
'''

# --- 2. the tests -----------------------------------------------------------------------------------
OLD_MAIN = '\nif __name__ == "__main__":\n'
NEW_CLASS = '''
# =============================================================================================
# Issue #93, the abort code (the fork's BL-118). An abort BEFORE the checks is not a verdict. The
# proof's `show()` ended in `sys.exit("verify: cannot read ...")`, which prints the text and exits
# 1 -- the FAIL code -- so a proof that had compared nothing read as a trim that lost something.
# Seen once in a 54-shard `--reverify` sweep over a partial clone: one blob fetch failed, the shard
# read FAIL, and the re-run read 0. The fixture plants the field case rather than mocking it: a
# depth-1 clone of a trimmed repository holds the trim commit and not its parent, so
# `git show <trim>^:<ledger>` cannot be answered there and can everywhere else.
# =============================================================================================

class TestAnAbortBeforeTheChecksIsNotAVerdict(unittest.TestCase):

    def _trimmed_and_shallow(self, tmp):
        """TestReverify's fixture (make_handoff_repo, trimmed at --cut 2, committed), plus a depth-1
        clone of it in which the trim commit is the only commit. Returns (source repo, clone, shard
        path relative to either root, as the proof names it)."""
        src = make_handoff_repo(str(Path(tmp) / "src"))
        r = run_trim(src, "--file", "HANDOFFS.md", "--cut", "2", "--write", "--today", "2026-02-01")
        self.assertIn("[WROTE]", r.stdout, r.stdout)
        sh(src, "git", "add", "-A")
        sh(src, "git", "commit", "-qm", "trim")
        shard = sorted((src / "docs" / "archive").glob("HANDOFFS-through-*.md"))[0]
        shard = shard.relative_to(src).as_posix()
        clone = Path(tmp) / "shallow"
        c = sh(Path(tmp), "git", "clone", "-q", "--depth", "1", "file://" + str(src.resolve()),
               str(clone))
        self.assertEqual(c.returncode, 0, c.stdout)
        return src, clone, shard

    def test_control_the_fixture_is_the_field_case(self):
        """Prove the fixture first: the clone holds exactly the trim commit, names it as the shard's
        adding commit and cannot show its parent -- and the SAME proof holds in the full repository,
        so the missing parent is the only difference the other tests see."""
        with tempfile.TemporaryDirectory() as tmp:
            src, clone, shard = self._trimmed_and_shallow(tmp)
            self.assertEqual(sh(clone, "git", "rev-list", "--count", "HEAD").stdout.strip(), "1")
            trim = sh(clone, "git", "log", "--diff-filter=A", "-1", "--format=%H", "--", shard)
            self.assertEqual(trim.stdout.strip(), sh(clone, "git", "rev-parse", "HEAD").stdout.strip())
            self.assertNotEqual(sh(clone, "git", "show", "HEAD^:HANDOFFS.md").returncode, 0,
                                "the parent must be unreadable here, or the fixture proves nothing")
            full = sh(src, "bash", shard + ".verify.sh")
            self.assertEqual(full.returncode, 0, full.stdout)
            self.assertIn("OK:", full.stdout)

    def test_the_frozen_proof_exits_3_with_its_reason_and_no_verdict(self):
        with tempfile.TemporaryDirectory() as tmp:
            _src, clone, shard = self._trimmed_and_shallow(tmp)
            r = sh(clone, "bash", shard + ".verify.sh")
            self.assertEqual(r.returncode, 3, r.stdout)
            self.assertIn("verify: cannot read", r.stdout)
            self.assertIn("did not finish", r.stdout)
            self.assertNotIn("FAIL:", r.stdout, "a proof that compared nothing has no FAIL to report")
            self.assertNotIn("OK:", r.stdout, "and no OK either: it is not a verdict")

    def test_reverify_reports_the_abort_as_exit_3_not_as_a_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            _src, clone, shard = self._trimmed_and_shallow(tmp)
            r = run_trim(clone, "--reverify", shard)
            self.assertEqual(r.returncode, 3, r.stdout)
            self.assertIn("[REVERIFY_VERDICT]", r.stdout)
            self.assertIn("exit 3 (0:", r.stdout, "the legend's own 3: the proof did not finish")
            self.assertIn("verify: cannot read", r.stdout)
            self.assertNotIn("FAIL:", r.stdout)

    def test_a_shard_file_that_cannot_be_read_is_the_same_abort(self):
        """The other read before the checks: with the trim uncommitted the proof reads the live file
        and the shard from the working tree, and a shard that is not there is an abort, not a FAIL."""
        with tempfile.TemporaryDirectory() as tmp:
            p = make_handoff_repo(tmp)
            r = run_trim(p, "--file", "HANDOFFS.md", "--cut", "2", "--write", "--today", "2026-02-01")
            self.assertIn("[WROTE]", r.stdout, r.stdout)
            shard = sorted((p / "docs" / "archive").glob("HANDOFFS-through-*.md"))[0]
            ok = sh(p, "bash", str(shard) + ".verify.sh")
            self.assertEqual(ok.returncode, 0, "control: the uncommitted trim's proof holds\\n" + ok.stdout)
            shard.unlink()
            r = sh(p, "bash", str(shard) + ".verify.sh")
            self.assertEqual(r.returncode, 3, r.stdout)
            self.assertIn("verify: cannot read", r.stdout)
            self.assertIn(shard.name, r.stdout)
            self.assertNotIn("FAIL:", r.stdout)

'''

# --- 3. the gate ----------------------------------------------------------------------------------
OLD_GATE = '      "name": "trimmer-unit-tests",\n      "direction": "min",\n      "threshold": 199,\n'
NEW_GATE = '      "name": "trimmer-unit-tests",\n      "direction": "min",\n      "threshold": 203,\n'

# --- 4. the apparatus -----------------------------------------------------------------------------
OLD_APP = "that is a claim about today's logic, not about the artifact that was shipped.\n\n"
NEW_APP = ("that is a claim about today's logic, not about the artifact that was shipped. A proof that cannot\n"
           "read an artifact from git (a shallow or partial clone without the trim commit's parent) exits 3\n"
           "and prints no verdict, never a `FAIL:` line; run it where the history is present.\n\n")

EDITS = [
    (TRIM, [(OLD_VERSION, NEW_VERSION), (OLD_SHOW, NEW_SHOW)]),
    (TESTS, [(OLD_MAIN, NEW_CLASS + OLD_MAIN)]),
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
print("bl118-build: 4 files edited; nothing committed")
