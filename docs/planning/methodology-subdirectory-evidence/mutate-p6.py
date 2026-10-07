#!/usr/bin/env python3
"""Mutation pass for BL-101 P6 (S279), re-runnable. Needs a scratch CLONE of the commit under test (never the working
repository: `git clone --no-local . /tmp/mut`) and takes about 25 minutes for all 55 mutants.
usage: python3 -B mutate-p6.py <scratch clone> p6-mutants.py [only-ids...]

Each mutant is (id, file, old, new, test classes). The text `old` must occur exactly once in `file`. The
mutant is applied inside the scratch clone (never the working repository), the named test classes of
tools/test_sync_layouts.py are run there, and the clone is restored with git checkout. A mutant is KILLED
when the run is not green. A baseline run (no mutant) must be green first, or nothing below is evidence.
Writes one line per mutant to stdout: id, KILLED/SURVIVED, the first failing test."""
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

clone = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("mutants", sys.argv[2])
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
only = set(sys.argv[3:])


def run(classes):
    r = subprocess.run([sys.executable, "-B", "tools/test_sync_layouts.py", *classes], cwd=clone,
                       capture_output=True, text=True, timeout=900)
    out = r.stdout + r.stderr
    failing = re.findall(r"^(?:FAIL|ERROR): (\S+)", out, re.M)
    return r.returncode, failing, out


def git(*args):
    subprocess.run(["git", "-C", str(clone), *args], check=True, capture_output=True)


git("checkout", "--", ".")
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
        print("%-4s BAD-ANCHOR (%d occurrences) %s: %r" % (mid, text.count(old), rel, old[:60]), flush=True)
        continue
    path.write_text(text.replace(old, new), encoding="utf-8")
    try:
        rc, failing, out = run(classes)
    except subprocess.TimeoutExpired:
        rc, failing = 1, ["TIMEOUT"]
    git("checkout", "--", ".")
    if rc != 0:
        killed += 1
        print("%-4s KILLED   by %s" % (mid, failing[0] if failing else "(a crash)"), flush=True)
    else:
        survived += 1
        print("%-4s SURVIVED %s: %r -> %r" % (mid, rel, old[:60], new[:60]), flush=True)
print("killed %d, survived %d" % (killed, survived))
