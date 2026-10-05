"""P3 of docs/planning/issue93-trimmer-proof-false-red-plan.md (S266): sweep every frozen proof in <repo>
through the REAL `--reverify` flag of <trimmer.py> and tabulate the frozen verdict beside the re-derived one.

Unlike reverify_p2.py (which rebuilt the proof in memory), this drives the shipped CLI, one process per shard.
It also measures what the flag promises, over the whole sweep: the tree is snapshotted before and after
(every file outside .git by size and mtime, every directory, `git status --porcelain --untracked-files=all`,
HEAD, the refs and the stash list) and the two must be identical.

usage: reverify_p3.py <repo> <trimmer.py> <out.tsv>
TSV: shard, frozen-version, frozen-exit, reverify-exit, first FAIL/OK line, banner(Y/N), substituted-lines
"""
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

repo, trimmer, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])


def git(*args):
    return subprocess.run(["git", "-C", str(repo)] + list(args), capture_output=True, text=True).stdout


def snapshot():
    seen = {}
    for root, dirs, names in os.walk(str(repo)):
        dirs[:] = [d for d in dirs if d != ".git"]
        for n in dirs:
            seen[os.path.relpath(os.path.join(root, n), str(repo))] = "dir"
        for n in names:
            fp = os.path.join(root, n)
            st = os.stat(fp)
            seen[os.path.relpath(fp, str(repo))] = (st.st_size, st.st_mtime_ns)
    return (seen, git("status", "--porcelain", "--untracked-files=all"), git("rev-parse", "HEAD"),
            git("for-each-ref"), git("stash", "list"))


before = snapshot()
rows = []
for proof in sorted((repo / "docs" / "archive").glob("*.verify.sh")):
    shard = "docs/archive/" + proof.name[:-len(".verify.sh")]
    txt = proof.read_text(encoding="utf-8")
    ver = (re.search(r"methodology_trim\.py v([0-9.]*[0-9])", txt) or [None, "?"])[1]
    frozen = subprocess.run(["bash", str(proof)], cwd=str(repo), capture_output=True, text=True)
    r = subprocess.run([sys.executable, str(trimmer), "--reverify", shard], cwd=str(repo),
                       capture_output=True, text=True)
    lines = (r.stdout + r.stderr).splitlines()
    first = next((l.strip() for l in lines if l.strip().startswith(("| FAIL:", "| OK:"))), None)
    if first is None:
        first = next((l.strip() for l in lines if l.strip().startswith("[REVERIFY_")), "(no verdict line)")
    banner = "Y" if any("[REVERIFY_BANNER]" in l for l in lines) else "N"
    subs = sum(1 for l in lines if "[REVERIFY_SUBSTITUTED]" in l)
    rows.append((proof.name, ver, frozen.returncode, r.returncode, first[:150], banner, subs))

after = snapshot()
with open(str(out), "w", encoding="utf-8") as fh:
    for row in rows:
        fh.write("\t".join(str(x) for x in row) + "\n")

print("proofs=%d  frozen-red=%d  re-derived exit codes: %s" % (
    len(rows), sum(1 for r in rows if r[2] != 0), dict(sorted(Counter(r[3] for r in rows).items()))))
newly_red = [r[0] for r in rows if r[2] == 0 and r[3] != 0]
newly_green = [r[0] for r in rows if r[2] != 0 and r[3] == 0]
print("newly red (frozen exit 0, re-derived nonzero): %d %s" % (len(newly_red), newly_red[:5]))
print("newly green (frozen nonzero, re-derived 0): %d" % len(newly_green))
print("no banner: %d   shards with a substituted line: %d" % (
    sum(1 for r in rows if r[5] != "Y"), sum(1 for r in rows if r[6])))
print("WRITES NOTHING over the whole sweep: %s" % ("yes, the tree is identical" if before == after else "NO -- CHANGED"))
if before != after:
    for name in sorted(set(before[0]) | set(after[0])):
        if before[0].get(name) != after[0].get(name):
            print("  differs:", name, before[0].get(name), "->", after[0].get(name))
    for i, label in enumerate(("files", "status", "HEAD", "refs", "stash")):
        if i and before[i] != after[i]:
            print("  differs:", label)
print("tracked-modified entries present during the sweep (so the porcelain is not vacuous): %d"
      % sum(1 for l in before[1].splitlines() if l[:2].strip() and not l.startswith("??")))
