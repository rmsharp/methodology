"""Mutation check for the port of PR #94's fifth commit onto the layout trimmer (the fork's BL-119).

Applies ONE textual mutant at a time to the clone's starter-kit/methodology_trim.py (in place; the
original text is restored in a `finally` and its hash checked at the end) and runs two classes against
it: the four new tests and the layout trimmer's template pin. KILLED = at least one test fails;
SURVIVED = none does; INVALID = a search text does not occur exactly once in the pristine source
(never scored as a kill). Where an intended test is named the report says whether it was among the
failures. The first six mutants are the build of `1082d3b`'s (bl118-mutants.py); the last three are
the pin's: a byte of the template OUTSIDE the abort block changes, a byte INSIDE it changes, and a line
the pin normalises away (the `indomain()` return, rewritten to an equivalent) changes (that last must
SURVIVE, and is scored as expected: it is exactly what the pin is meant to let through).

    python3 bl119-mutants.py <clone-root>
"""
import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
TRIMMER = ROOT / "starter-kit" / "methodology_trim.py"
TESTS = ["TestAnAbortBeforeTheChecksIsNotAVerdict", "TestTheLegacyLayoutIsByteForByteWhatItWas"]

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
PARAM = '    return bool(t) and not SCHEME.match(t) and not t.startswith(("#", "/") if PARENT_LINKS'

# (name, [(old, new), ...], intended-test fragment or None, expected: "killed" | "survives")
MUTANTS = [
    ("show() aborts with sys.exit(text) again (exit 1)",
     [(CALL_IN_SHOW, '        sys.exit("verify: cannot read %s:%s" % (ref, path))\n')], "exits_3", "killed"),
    ("unfinished() exits 1", [(EXIT3, "    sys.exit(1)\n")], "exits_3", "killed"),
    ("unfinished() exits 0", [(EXIT3, "    sys.exit(0)\n")], "exits_3", "killed"),
    ("readf() reads without the guard", [(NEW_READF, OLD_READF)], "shard_file_that_cannot_be_read",
     "killed"),
    ("the reason line is not printed", [(REASON, "    pass\n")], "exits_3", "killed"),
    ("'did not finish' dropped from the reason",
     [(REASON, REASON.replace(" -- the proof did not finish; this is not a verdict (exit 3)", ""))],
     "frozen_proof_exits_3", "killed"),
    # the pin's: found in the source below (see pick_outside)
    ("a template byte OUTSIDE the abort block changes", None, "abort_hunk_only", "killed"),
    ("a template byte INSIDE the abort block changes (the comment's word)",
     [("    # lost something. Exit 3 is", "    # lost something. Exit three is")], "abort_hunk_only", "killed"),
    ("the indomain() return line changes, equivalently (the pin allows it)",
     [(PARAM, PARAM.replace("not SCHEME.match(t)", "SCHEME.match(t) is None", 1))], None, "survives"),
]


def pick_outside(src):
    """A line of the template that is not in the abort block, not a parameter line, and unique."""
    t0 = src.index('VERIFY_TEMPLATE = r"""')
    t1 = src.index('"""', t0 + 25)
    block = src[t0:t1]
    for ln in block.splitlines():
        s = ln.strip()
        if s.startswith("print(") and "FAIL" in s and src.count(ln + "\n") == 1:
            return [(ln + "\n", ln.replace("FAIL", "FAIL!", 1) + "\n")]
    return None


def main():
    original = TRIMMER.read_text(encoding="utf-8")
    digest = hashlib.sha256(original.encode("utf-8")).hexdigest()
    killed = survived = invalid = surprises = 0
    try:
        for name, pairs, intended, expected in MUTANTS:
            if pairs is None:
                pairs = pick_outside(original)
                if pairs is None:
                    print("INVALID  %-66s (no unique template line found)" % name)
                    invalid += 1
                    continue
            bad = [old for old, _new in pairs if original.count(old) != 1]
            if bad:
                print("INVALID  %-66s (a search text occurs %d times)" % (name, original.count(bad[0])))
                invalid += 1
                continue
            text = original
            for old, new in pairs:
                text = text.replace(old, new, 1)
            if text == original:
                print("INVALID  %-66s (the mutant equals the source)" % name)
                invalid += 1
                continue
            TRIMMER.write_text(text, encoding="utf-8")
            p = subprocess.run([sys.executable, "tools/test_methodology_trim.py"] + TESTS, cwd=str(ROOT),
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            failed = re.findall(r"^(?:FAIL|ERROR): (test_\w+)", p.stdout, re.M)
            if failed:
                killed += 1
                hit = ""
                if intended:
                    hit = "  intended test %s" % ("FAILED" if any(intended in f for f in failed)
                                                  else "DID NOT FAIL")
                flag = "" if expected == "killed" else "  <-- UNEXPECTED: it was meant to survive"
                surprises += bool(flag) or ("DID NOT FAIL" in hit)
                print("KILLED   %-66s by %d test(s)%s%s" % (name, len(failed), hit, flag))
            else:
                survived += 1
                flag = "" if expected == "survives" else "  <-- UNEXPECTED: it was meant to be killed"
                surprises += bool(flag)
                print("SURVIVED %-66s%s" % (name, flag))
    finally:
        TRIMMER.write_text(original, encoding="utf-8")
    again = hashlib.sha256(TRIMMER.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
    print("trimmer restored byte-for-byte: %s" % (again == digest))
    print("%d killed, %d survived, %d invalid, %d unexpected, of %d"
          % (killed, survived, invalid, surprises, len(MUTANTS)))
    return 1 if (invalid or surprises or again != digest) else 0


if __name__ == "__main__":
    sys.exit(main())
