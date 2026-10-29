#!/usr/bin/env python3
"""Why do two more files read 'refused' at the new-layout adopters than at S326? (S396, read-only)

For each (adopter, file) the adopter's committed blob is looked up in the history of the source file on four refs:
the old candidate pr2/candidate, the rebuilt pr2b/candidate, upstream/main and the fork's main. The first commit on the
old candidate that carried the blob is named. Nothing is written; adopters are read through `git rev-parse <HEAD>:<path>`.
Run from the repository root."""
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parents[3]
DEV = Path.home() / "Development"
ADOPTERS = ["model_project_constructor", "feedback-loop-comparison", "airqino", "chat_verification", "church_growth", "vscode_quarto_ext"]
FILES = [("methodology/methodology_trim.py", "starter-kit/methodology_trim.py"), ("methodology/FRAMEWORK_APPARATUS.md", "FRAMEWORK_APPARATUS.md")]
CASES = [(a, ap, sp) for a in ADOPTERS for ap, sp in FILES]
REFS = ["pr2/candidate", "pr2b/candidate", "upstream/main", "main"]


def git(repo, *a):
    r = subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def commits_with_blob(ref, path, blob):
    hits = []
    for c in git(REPO, "log", "--format=%H", ref, "--", path).split():
        if git(REPO, "rev-parse", "%s:%s" % (c, path)) == blob:
            hits.append(c)
    return hits


for adopter, apath, spath in CASES:
    repo = DEV / adopter
    blob = git(repo, "rev-parse", "HEAD:" + apath)
    print("%s %s blob %s (source %s)" % (adopter, apath, blob[:10], spath))
    for ref in REFS:
        h = commits_with_blob(ref, spath, blob)
        first = ("; oldest %s %s" % (h[-1][:8], git(REPO, "log", "-1", "--format=%s", h[-1])[:90])) if h else ""
        print("   %-15s %s%s" % (ref, ("in history at %d commit(s)" % len(h)) if h else "NOT in history", first))
