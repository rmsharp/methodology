#!/usr/bin/env python3
"""Mutation pass for BL-101 P7 (S280), re-runnable. Needs a scratch CLONE of the commit under test (never the working
repository: `git clone --no-local . /tmp/mut`) and takes about 40 minutes for all of p7-mutants.py.
usage: python3 -B mutate-p7.py <scratch clone> p7-mutants.py [--anchors] [only-ids...]

Each mutant is (id, file, old, new, test classes). The text `old` must occur exactly once in `file`. The mutant is
applied inside the scratch clone, the named test classes of tools/test_migrate_layout.py are run there (the fast ones
first), and the clone is restored with git checkout. A mutant is KILLED when that run is not green. A mutant the named
classes do not kill is run once more against the WHOLE test file before it is called a survivor: the named classes are
a guess at where the killing test lives, and only the whole file settles it. A baseline run (no mutant) must be green
first, or nothing below is evidence. --anchors only checks that every `old` occurs once, and runs nothing.
Writes one line per mutant: id, KILLED/SURVIVED, the first failing test."""
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

args = [a for a in sys.argv[1:] if not a.startswith("--")]
anchors_only = "--anchors" in sys.argv
clone = Path(args[0])
spec = importlib.util.spec_from_file_location("mutants", args[1])
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
only = set(args[2:])


def run(classes):
    r = subprocess.run([sys.executable, "-B", "tools/test_migrate_layout.py", *classes], cwd=clone,
                       capture_output=True, text=True, timeout=1500)
    out = r.stdout + r.stderr
    failing = re.findall(r"^(?:FAIL|ERROR): (\S+)", out, re.M)
    return r.returncode, failing, out


def git(*a):
    subprocess.run(["git", "-C", str(clone), *a], check=True, capture_output=True)


git("checkout", "--", ".")
if anchors_only:
    bad = 0
    for mid, rel, old, new, classes in m.MUTANTS:
        text = (clone / rel).read_text(encoding="utf-8")
        if text.count(old) != 1:
            bad += 1
            print("%-5s BAD-ANCHOR (%d occurrences) %s: %r" % (mid, text.count(old), rel, old[:70]))
    print("%d mutants, %d bad anchors" % (len(m.MUTANTS), bad))
    sys.exit(1 if bad else 0)
rc, failing, out = run([])
print("baseline: rc=%d failing=%s" % (rc, failing[:3]), flush=True)
if rc != 0:
    print(out[-1500:])
    sys.exit("baseline is not green: no mutant result below would be evidence")
killed = survived = 0
for mid, rel, old, new, classes in m.MUTANTS:
    if only and mid not in only:
        continue
    path = clone / rel
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        print("%-5s BAD-ANCHOR (%d occurrences) %s: %r" % (mid, text.count(old), rel, old[:60]), flush=True)
        continue
    path.write_text(text.replace(old, new), encoding="utf-8")
    try:
        rc, failing, out = run(classes)
        where = "named classes"
        if rc == 0 and classes:
            rc, failing, out = run([])
            where = "the whole file"
    except subprocess.TimeoutExpired:
        rc, failing, where = 1, ["TIMEOUT"], "timeout"
    git("checkout", "--", ".")
    if rc != 0:
        killed += 1
        print("%-5s KILLED   by %s (%s)" % (mid, failing[0] if failing else "(a crash)", where), flush=True)
    else:
        survived += 1
        print("%-5s SURVIVED %s: %r -> %r" % (mid, rel, old[:60], new[:60]), flush=True)
print("killed %d, survived %d" % (killed, survived))
