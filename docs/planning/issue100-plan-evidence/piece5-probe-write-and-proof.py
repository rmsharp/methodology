# Evidence for piece 5 of docs/planning/issue100-fixes-plan.md. Run it from OUTSIDE the clone, on a clone that has
# tools/test_methodology_trim.py (it builds temporary git repos with that file's make_repo / make_handoff_repo and runs the
# clone's starter-kit/methodology_trim.py in them). Read-only for the project; every repo is a temp directory:
#   PYTHONDONTWRITEBYTECODE=1 python3 -I -B piece5-probe-write-and-proof.py <path-to-a-clone>
# Output before the piece: piece5-probe-before-output.txt (a clone at 4aea4eda); after: piece5-probe-after-output.txt (5563a7c8).
import subprocess, sys, tempfile
from pathlib import Path
clone = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(clone / "tools")); sys.dont_write_bytecode = True
import test_methodology_trim as T

def git(r, *a): return T.sh(r, "git", *a)

def touch(p):
    c = Path(p) / "CHANGELOG.md"
    if git(p, "ls-files", "--error-unmatch", "CHANGELOG.md").returncode == 0:
        c.write_text(c.read_text() + "\n"); git(p, "add", "CHANGELOG.md")

def go(label, repo, name):
    print("\n### %s [%s]" % (label, name))
    w = T.run_trim(repo, "--file", name, "--write")
    codes = [l[:200] for l in w.stdout.splitlines() if l.startswith("  [") and not l.startswith(("  [TRIGGER_", "  [SRF]", "  [L1", "  [L2", "  [L3"))]
    print("  --write exit=%d" % w.returncode); [print("   ", c) for c in codes]
    v = sorted(Path(repo).glob("docs/archive/*.verify.sh"))
    if not v: print("  (no verify script)"); return
    r = subprocess.run(["bash", str(v[0])], cwd=str(repo), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    tail = [l[:230] for l in r.stdout.strip().splitlines()[-4:]]
    print("  verify.sh (uncommitted, as the trimmer leaves it) exit=%d" % r.returncode); [print("   ", t) for t in tail]
    # now do what an adopter with untracked ledgers does: commit what can be committed, rerun
    git(repo, "add", "-A"); r2 = git(repo, "commit", "-qm", "trim")
    r = subprocess.run(["bash", str(v[0])], cwd=str(repo), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    tail = [l[:230] for l in r.stdout.strip().splitlines()[-4:]]
    print("  verify.sh after `git add -A && git commit` exit=%d" % r.returncode); [print("   ", t) for t in tail]
    print("  after: tracked=%s" % (git(repo, "ls-files", "--error-unmatch", name).returncode == 0))

with tempfile.TemporaryDirectory() as t:
    p = T.make_repo(t); git(p, "rm", "-q", "--cached", "CHANGELOG.md")
    (Path(p) / ".gitignore").write_text("CHANGELOG.md\n"); git(p, "add", ".gitignore"); git(p, "commit", "-qm", "untrack and ignore")
    go("E committed once, then untracked and ignored", p, "CHANGELOG.md")
with tempfile.TemporaryDirectory() as t:
    p = T.make_handoff_repo(t); git(p, "rm", "-q", "--cached", "HANDOFFS.md")
    (Path(p) / ".gitignore").write_text("HANDOFFS.md\n"); git(p, "add", ".gitignore"); touch(p); git(p, "commit", "-qam", "untrack and ignore")
    go("E committed once, then untracked and ignored", p, "HANDOFFS.md")
