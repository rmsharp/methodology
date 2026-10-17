"""Mutation check for the fifth commit of the #93 fix (the fork's BL-118): an abort before the proof's
checks exits 3, not 1.

Applies ONE textual mutant at a time to a scratch copy of the tree's starter-kit/methodology_trim.py and
runs the new test class against it. KILLED = at least one test fails; SURVIVED = none does; INVALID = the
search text does not occur exactly once in the pristine source (never scored as a kill). Where an intended
test is named the report says whether that test was among the failures. Nothing under the tree is written:
the copy lives in a temp directory.

    python3 bl118-mutants.py <worktree-root>
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
TESTS = ["TestAnAbortBeforeTheChecksIsNotAVerdict"]

CALL_IN_SHOW = '        unfinished("cannot read %s:%s" % (ref, path))\n'
EXIT3 = "    sys.exit(3)\n"
REASON = ('    sys.stderr.write("verify: %s -- the proof did not finish; this is not a verdict (exit 3)\\n"\n'
          '                     % why)\n')
NEW_READF = '''def readf(path):
    try:
        with open(path, "r", encoding="utf-8", newline="") as fh:
            return fh.read()
    except OSError as e:
        unfinished("cannot read %s (%s)" % (path, e.strerror or e))
'''
OLD_READF = '''def readf(path):
    with open(path, "r", encoding="utf-8", newline="") as fh:
        return fh.read()
'''

# (name, [(old, new), ...], intended-test fragment or None)
MUTANTS = [
    ("show() aborts with sys.exit(text) again (exit 1)",
     [(CALL_IN_SHOW, '        sys.exit("verify: cannot read %s:%s" % (ref, path))\n')], "exits_3"),
    ("unfinished() exits 1",
     [(EXIT3, "    sys.exit(1)\n")], "exits_3"),
    ("unfinished() exits 0",
     [(EXIT3, "    sys.exit(0)\n")], "exits_3"),
    ("readf() reads without the guard",
     [(NEW_READF, OLD_READF)], "shard_file_that_cannot_be_read"),
    ("the reason line is not printed",
     [(REASON, "    pass\n")], "exits_3"),
    ("'did not finish' dropped from the reason",
     [(REASON, REASON.replace(" -- the proof did not finish; this is not a verdict (exit 3)", ""))],
     "frozen_proof_exits_3"),
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
