#!/usr/bin/env python3
"""PR2b layer 1: what does the candidate's commit 1 conflict with on `upstream/main`, and does upstream's side lose anything?

Layer 1 of PR2b (docs/planning/upstream-pr-composition-plan.md, section 5) is Part 1 of the pull request: the candidate's
commit 1 (`bbe0dc35`) rebuilt on `upstream/main` (`d50ce290`). The sizing record read 26 of its 28 conflict regions as upstream's
own lineage (the ledger trimmer and its tests, which upstream merged as #94) and the other two as small. A reading is a claim, so
this script checks it mechanically, per file:

  1. apply the commit with `git cherry-pick -n` onto the base, in a throwaway `--no-local` clone (a working tree, so the default
     conflict markers appear: that is the unit the plan's 46 and the record's 28 are counted in);
  2. count each conflicted file's regions;
  3. resolve every region to the BASE side (upstream's) and compare the result with the base's own file, byte for byte.

Equal means upstream's side loses nothing the commit had: the commit's cleanly merged hunks in that file add nothing beyond
upstream's, so the file drops out of the layer and the layer carries it as upstream's. Unequal prints the difference, which
is exactly what the layer still adds to that file (here: two gate thresholds, which the layer's verification then re-derives).

It resolves nothing in the repository and keeps nothing: the clone is removed. Python 3 standard library only; about 10 seconds.

Run from anywhere inside the repository:
    python3 -I docs/planning/pr-composition-evidence/pr2b-layer1-resolve.py [<base> [<commit>]]
Defaults: base `d50ce290d9218dc91d9a36069b4d936868964298`, commit `bbe0dc35`.
"""
import difflib
import os
import re
import shutil
import subprocess
import sys
import tempfile

BASE_DEFAULT = "d50ce290d9218dc91d9a36069b4d936868964298"
COMMIT_DEFAULT = "bbe0dc35"
REGION = re.compile(r"^<<<<<<< [^\n]*\n(.*?)^=======\n(.*?)^>>>>>>> [^\n]*\n", re.S | re.M)


def git(*args, cwd=None, check=True):
    p = subprocess.run(["git", *args], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode != 0:
        sys.exit("git %s failed (%d): %s" % (" ".join(args), p.returncode, p.stderr.decode("utf-8", "replace")))
    return p


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else BASE_DEFAULT
    commit = sys.argv[2] if len(sys.argv) > 2 else COMMIT_DEFAULT
    top = git("rev-parse", "--show-toplevel").stdout.decode().strip()
    tmp = tempfile.mkdtemp(prefix="pr2b-layer1-")
    try:
        clone = os.path.join(tmp, "c")
        git("clone", "--no-local", "-q", top, clone)
        git("checkout", "-q", "--detach", base, cwd=clone)
        full = git("rev-parse", "HEAD", cwd=clone).stdout.decode().strip()
        git("config", "merge.conflictStyle", "merge", cwd=clone)
        p = git("cherry-pick", "-n", commit, cwd=clone, check=False)
        print("base %s; commit %s; cherry-pick -n exit %d" % (full[:8], commit, p.returncode))
        unmerged = git("diff", "--name-only", "--diff-filter=U", cwd=clone).stdout.decode().split()
        staged = [f for f in git("diff", "--cached", "--name-only", cwd=clone).stdout.decode().split() if f not in unmerged]
        total = 0
        print("\nconflicted files (regions; resolved-to-base equals the base's file):")
        for path in sorted(unmerged):
            with open(os.path.join(clone, path), encoding="utf-8", newline="") as fh:
                text = fh.read()
            n = len(REGION.findall(text))
            total += n
            resolved = REGION.sub(lambda m: m.group(1), text)
            basetext = git("show", "%s:%s" % (full, path), cwd=clone).stdout.decode("utf-8")
            same = resolved == basetext
            print("  %-40s %3d region(s)  %s" % (path, n, "EQUAL" if same else "DIFFERS"))
            if not same:
                for line in difflib.unified_diff(basetext.splitlines(), resolved.splitlines(), "base", "resolved", n=0, lineterm=""):
                    print("      " + line[:160])
        print("  total: %d region(s) in %d file(s)" % (total, len(unmerged)))
        print("\nmerged without a conflict (staged by the cherry-pick): %d file(s)" % len(staged))
        for f in sorted(staged):
            print("  " + f)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
