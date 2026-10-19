"""Point 3 of the maintainer's comment on PR #94: what the `SESSION_NOTES.md` table entry does.

Usage: python3 -I point3_session_notes.py <worktree-of-the-PR-head>

The worktree supplies the trimmer, the context-budget tool and its seed config, the seed notes file
and the test fixtures' helpers. Two fixtures, each a throwaway repository:

  A  a notes file of 123,325 B of runner-shaped records (the maintainer's figure): does
     `context_budget.py --status` fail it while `methodology_trim.py --check` says no trim is due?
  B  a notes file over the byte cap whose NEWEST records use a lowercase `did` in the heading
     (`### What Session N did`), which the entry's pattern does not match: what does a trim say?
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

wt = pathlib.Path(sys.argv[1])
TRIM = wt / "starter-kit" / "methodology_trim.py"
BUDGET = wt / "starter-kit" / "context_budget.py"
SEED_BUDGET = wt / "starter-kit" / "context-budget.json"
SEED_NOTES = (wt / "starter-kit" / "SESSION_NOTES.md").read_text(encoding="utf-8")
TARGET = 123325 + 160        # the pad is exact up to the 160 B of record heads; lands on 123,325 B


def run(cwd, *args):
    return subprocess.run(list(args), cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          text=True)


def record(n, heading_did, filler):
    return ("### What Session %d %s\n**Deliverable:** task %d\n**Started:** 2026-01-%02d\n"
            "**Status:** done\n%s\n\n" % (n, heading_did, n, n % 28 + 1, filler))


def notes_text(n_new_lower, n_total, target):
    """Seed front matter, then newest-first records; the first `n_new_lower` use a lowercase did."""
    body = seed = SEED_NOTES.rstrip("\n") + "\n\n"
    recs = [record(n_total - i, "did" if i < n_new_lower else "Did", "") for i in range(n_total)]
    fixed = len((seed + "".join(recs)).encode("utf-8"))
    pad_total = target - fixed
    per, extra = divmod(pad_total, n_total)
    out = []
    for i in range(n_total):
        pad = per + (1 if i < extra else 0)
        # filler lines of at most 270 bytes so that the per-line cap is not what trips
        lines, left = [], max(pad - 1, 0)
        while left > 0:
            k = min(270, left)
            lines.append("w" * k)
            left -= k + 1
        out.append(record(n_total - i, "did" if i < n_new_lower else "Did", "\n".join(lines)))
    text = seed + "".join(out)
    return text


def repo_with(tmp, notes):
    p = pathlib.Path(tmp)
    (p / "docs" / "archive").mkdir(parents=True)
    (p / "SESSION_NOTES.md").write_text(notes, encoding="utf-8")
    (p / "CHANGELOG.md").write_text("# Changelog\n\nFront matter.\nRetained entries: **0**.\n\n---\n\n"
                                    "## 2026-01\n\n### 2026-01-01 · [ad hoc] seed\n\nbody\n\n", encoding="utf-8")
    shutil.copy(str(SEED_BUDGET), str(p / ".context-budget.json"))
    shutil.copy(str(BUDGET), str(p / "context_budget.py"))
    for c in (("git", "init", "-q", "."), ("git", "config", "user.email", "t@t"),
              ("git", "config", "user.name", "T"), ("git", "add", "-A"), ("git", "commit", "-qm", "seed")):
        run(p, *c)
    return p


def lines(out, *needles):
    return [ln[:230] for ln in out.splitlines() if any(n in ln for n in needles)]


print("trimmer:", TRIM)
with tempfile.TemporaryDirectory() as tmp:
    text = notes_text(0, 160, TARGET)
    p = repo_with(tmp, text)
    print("\n== A  runner-shaped notes file, %d B, %d lines" % (len((p / 'SESSION_NOTES.md').read_bytes()),
                                                                  len(text.splitlines())))
    b = run(p, sys.executable, "-I", "context_budget.py", "--status")
    print("   context_budget --status: exit %d" % b.returncode)
    for ln in lines(b.stdout, "SESSION_NOTES.md"):
        print("      " + ln)
    c = run(p, sys.executable, str(TRIM), "--file", "SESSION_NOTES.md", "--check")
    print("   methodology_trim --check: exit %d" % c.returncode)
    for ln in c.stdout.splitlines():
        print("      " + ln[:230])

with tempfile.TemporaryDirectory() as tmp:
    text = notes_text(135, 160, 250000)
    p = repo_with(tmp, text)
    print("\n== B  %d B; the newest 135 of 160 records say `did` (lowercase), the other 25 say `Did`"
          % len((p / 'SESSION_NOTES.md').read_bytes()))
    c = run(p, sys.executable, str(TRIM), "--file", "SESSION_NOTES.md", "--force")
    print("   methodology_trim dry run: exit %d" % c.returncode)
    for ln in c.stdout.splitlines():
        print("      " + ln[:230])
