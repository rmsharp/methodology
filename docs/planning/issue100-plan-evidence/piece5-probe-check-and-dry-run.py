# Evidence for piece 5 of docs/planning/issue100-fixes-plan.md. Run it from OUTSIDE the clone, on a clone that has
# tools/test_methodology_trim.py (it builds temporary git repos with that file's make_repo / make_handoff_repo and runs the
# clone's starter-kit/methodology_trim.py in them). Read-only for the project; every repo is a temp directory:
#   PYTHONDONTWRITEBYTECODE=1 python3 -I -B piece5-probe-check-and-dry-run.py <path-to-a-clone>
# Output before the piece: piece5-probe-before-output.txt (a clone at 4aea4eda); after: piece5-probe-after-output.txt (5563a7c8).
"""Probe: how does the UNEDITED trimmer behave when a ledger is outside git?

Read-only with respect to the project: every repo is a temp dir. Run from outside the clone:
    python3 -I -B probe_untracked.py <clone-dir>
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

clone = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(clone / "tools"))
sys.dont_write_bytecode = True
import test_methodology_trim as T  # noqa: E402


def git(repo, *a):
    return T.sh(repo, "git", *a)


def state(repo, name):
    ls = git(repo, "ls-files", "--error-unmatch", name).returncode
    ig = git(repo, "check-ignore", "-q", name).returncode
    fr = git(repo, "log", "-1", "--format=%h", "--", name).stdout.strip()
    return "tracked=%s ignored=%s frontier=%s" % ("yes" if ls == 0 else "no",
                                                 "yes" if ig == 0 else "no", fr or "none")


def show(label, repo, name):
    print("\n### %s  [%s: %s]" % (label, name, state(repo, name)))
    for mode, args in (("--check", ["--file", name, "--check"]), ("dry-run", ["--file", name])):
        r = T.run_trim(repo, *args)
        keep = [ln[:230] for ln in r.stdout.splitlines()
                if ln.startswith("  [") and not ln.startswith(("  [TRIGGER_", "  [SRF]", "  [L1", "  [L2", "  [L3"))]
        print("  %-8s exit=%d  %s" % (mode, r.returncode, " | ".join(keep) if keep else "(no findings printed)"))


def touch(p):
    """Record the action in CHANGELOG.md when it is tracked, so P1's undocumented set stays empty."""
    c = Path(p) / "CHANGELOG.md"
    if git(p, "ls-files", "--error-unmatch", "CHANGELOG.md").returncode == 0:
        c.write_text(c.read_text() + "\n")
        git(p, "add", "CHANGELOG.md")


def never_committed(tmp, name):
    """Repo whose first and only commit is unrelated; `name` exists but was never committed."""
    p = T.make_repo(tmp) if name == "CHANGELOG.md" else T.make_handoff_repo(tmp)
    git(p, "rm", "-q", "--cached", name)
    r = git(p, "commit", "-q", "--allow-empty", "--amend", "-m", "seed without the ledger")
    assert r.returncode == 0, r.stdout
    return p


def run():
    cases = []
    for name in ("CHANGELOG.md", "HANDOFFS.md"):
        mk = (lambda t: T.make_repo(t)) if name == "CHANGELOG.md" else (lambda t: T.make_handoff_repo(t))
        with tempfile.TemporaryDirectory() as t:
            show("A tracked (control)", mk(t), name)
        with tempfile.TemporaryDirectory() as t:
            p = never_committed(t, name)
            show("B never committed, not ignored", p, name)
        with tempfile.TemporaryDirectory() as t:
            p = never_committed(t, name)
            (Path(p) / ".gitignore").write_text(name + "\n")
            git(p, "add", ".gitignore"); touch(p); git(p, "commit", "-qam", "ignore")
            show("C never committed, ignored", p, name)
        with tempfile.TemporaryDirectory() as t:
            p = mk(t)
            git(p, "rm", "-q", "--cached", name); touch(p); git(p, "commit", "-qam", "untrack")
            show("D committed once, then untracked (not ignored)", p, name)
        with tempfile.TemporaryDirectory() as t:
            p = mk(t)
            git(p, "rm", "-q", "--cached", name)
            (Path(p) / ".gitignore").write_text(name + "\n")
            git(p, "add", ".gitignore"); touch(p); git(p, "commit", "-qam", "untrack and ignore")
            show("E committed once, then untracked and ignored", p, name)


run()
