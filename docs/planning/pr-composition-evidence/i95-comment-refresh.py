#!/usr/bin/env python3
"""i95-comment-refresh.py -- upstream issue #95: re-derive, before and after the fix built on this tree,
every figure the refreshed comment (`i95-comment-draft.md`) states about what the change does.

Usage:  python3 -I docs/planning/pr-composition-evidence/i95-comment-refresh.py SCRATCH_DIR     (run from the repository root;
        SCRATCH_DIR is created, an existing one is removed)

Each case is a git-initialised directory holding a copy of the tool, the seed config and the files named; the
tool's own `--status --json` is parsed (never read by eye) and one line is printed per case: the exit code, each
row's status, and the finding kinds. Read-only on the repository: upstream's blobs come from `git show` at the
pinned commit, this tree's from `starter-kit/`.

Cases:
  up-notes, up-template   the issue's two repros on upstream's blobs at the pinned commit (exit 2 each)
  fork-notes, fork-template   the same two cases on this tree's seeds and tool (exit 1 each; no row over)
  fork-day-zero           `bin/sync --layout legacy` into an empty project, the template copied to CLAUDE.md
  floor-799, floor-800    this tree's tool, a fenced purpose of exactly 799 and 800 ASCII bytes
  floor-cjk-300           a fenced purpose of 300 CJK characters (900 bytes)
"""
import json
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
UPSTREAM = "f34769f31ca351a520c2da4fa5f9e65b5153bffa"
SEEDS = ("starter-kit/context_budget.py", "starter-kit/context-budget.json",
         "starter-kit/CLAUDE_TEMPLATE.md", "starter-kit/SESSION_NOTES.md")
FENCE = ("<!-- budget:protected -->\n", "\n<!-- /budget:protected -->")


def sh(args, cwd=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


def blob(rev, path):
    if rev is None:
        return open(path, encoding="utf-8").read()
    return sh(["git", "show", f"{rev}:{path}"]).stdout


def project(root, name, rev, files):
    """A fresh git directory with the tool, the seed config and `files` ({dest: seed path})."""
    d = os.path.join(root, name)
    os.makedirs(d)
    sh(["git", "init", "-q", "."], cwd=d)
    for src, dest in (("starter-kit/context_budget.py", "context_budget.py"),
                      ("starter-kit/context-budget.json", ".context-budget.json")):
        open(os.path.join(d, dest), "w", encoding="utf-8").write(blob(rev, src))
    for dest, src in files.items():
        open(os.path.join(d, dest), "w", encoding="utf-8").write(blob(rev, src))
    return d


def measure(d):
    r = sh([sys.executable, "-I", "context_budget.py", "--status", "--json"], cwd=d)
    j = json.loads(r.stdout)
    rows = " ".join(f"{x['path']}={x['status']}" for x in j["files"])
    kinds = ",".join(sorted(f["kind"] for x in j["files"] for f in x["findings"])) or "none"
    over = sum(x["status"] == "over" for x in j["files"])
    return f"exit={r.returncode} over={over} kinds={kinds} | {rows}"


def fenced(d, body):
    """Replace the template's fenced purpose in d/CLAUDE.md with `body`."""
    t = open(os.path.join(d, "CLAUDE.md"), encoding="utf-8").read()
    a = t.index(FENCE[0]) + len(FENCE[0])
    b = t.index(FENCE[1])
    open(os.path.join(d, "CLAUDE.md"), "w", encoding="utf-8").write(t[:a] + body + t[b:])


def main():
    root = os.path.abspath(sys.argv[1])
    if os.path.exists(root):
        shutil.rmtree(root)
    os.makedirs(root)
    print(f"upstream pinned commit {UPSTREAM[:7]}; this tree HEAD {sh(['git', 'rev-parse', '--short=12', 'HEAD']).stdout.strip()}")
    for rev, tag in ((UPSTREAM, "up"), (None, "fork")):
        print(f"{tag}-notes      {measure(project(root, tag + '-notes', rev, {'SESSION_NOTES.md': SEEDS[3]}))}")
        print(f"{tag}-template   {measure(project(root, tag + '-template', rev, {'CLAUDE.md': SEEDS[2]}))}")
    day0 = os.path.join(root, "fork-day-zero")
    os.makedirs(day0)
    sh(["git", "init", "-q", "."], cwd=day0)
    sh(["bin/sync", day0, "--layout", "legacy"])
    shutil.copy("starter-kit/CLAUDE_TEMPLATE.md", os.path.join(day0, "CLAUDE.md"))
    print(f"fork-day-zero   {measure(day0)}")
    for name, body in (("floor-799", "x" * 799), ("floor-800", "x" * 800), ("floor-cjk-300", "目" * 300)):
        d = project(root, name, None, {"CLAUDE.md": SEEDS[2]})
        fenced(d, body)
        print(f"{name:15} {measure(d)}   (body: {len(body)} chars, {len(body.encode())} bytes)")


main()
