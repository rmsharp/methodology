#!/usr/bin/env python3
"""PR2b layer measurements: what one layer's commit changed, by command, not by reading.

Usage:  python3 -I pr2b-layer-measure.py <candidate-repo> [<commit> [<ref> ...]]   (default commit: HEAD;
        default refs to merge against: upstream/main; pass the heads of open upstream pull requests to add them)

For the commit and its parent, in the given repository (read-only; nothing is checked out there):
  1. the commit, its parent and their trees;
  2. the changed files, as `git diff --numstat` prints them;
  3. the literal scanner (`bin/check-layout-literals`) run on an extracted copy of the parent's tree and of the
     commit's tree: the summary line and the count of sites per file, so a layer's effect on the scanner is
     a difference of two measured lists, not an expectation from the commit's subject;
  4. the count, per added line of the commit, of fork-internal references (a backlog id, a session number, a
     plan or decision label, "the fork", "he overruled"), by the regex SCRUB below. The regex is rough: it
     sizes the later scrub commit, it does not decide it. It is the one layer 2's record typed inline;
  5. the merge of the commit with each ref, as `git merge-tree --write-tree --name-only` builds it in the object
     database only, with the EMPTY tree as the attribute source: that is GitHub's server-side view, where
     `merge=union` does not apply (`conflicts-after-merge.sh` is fixed on the old candidate, `pr2/candidate`).
     Exit 0 is clean, 1 is conflicts, with the files and the count of conflict regions in each.

Standard library only. The scanner exits 1 while it still reads sites (a to-do list until the last layer that
resolves a tool); that exit code is printed, not treated as a failure here.
"""
import collections
import io
import re
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

SCRUB = re.compile(
    r"BL-\d+|\bS\d{3}\b|\bthe fork\b|[Ll]earning #\d+|plan C\d+|\(plan |decision D\d+|phase P\d+"
    r"|\bP[1-9]\b.*phase|overruled|\bhe\b (?:overruled|decided)"
)
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
SITE = re.compile(r"^  (\S+?):\d+ \[")
ROW = re.compile(r"^  (\S+?):\d+ \[\S+ \S+\] (.*?)\s+-> ")
SUMMARY = re.compile(r"^check-layout-literals: .*")


def git(repo, *args, binary=False):
    out = subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True)
    return out.stdout if binary else out.stdout.decode()


def scan(repo, rev):
    """Extract rev's tree to a temp dir and run its own scanner there (--all, so acknowledged sites are listed).
    Returns (summary, {file: sites}, {file: acknowledged sites}, exit, [(file, source text of each counted site)]).
    A site under the `acknowledged:` heading carries a same-line `layout: ok -- <reason>` marker and is not counted."""
    with tempfile.TemporaryDirectory() as tmp:
        data = git(repo, "archive", "--format=tar", rev, binary=True)
        with tarfile.open(fileobj=io.BytesIO(data)) as tf:
            tf.extractall(tmp, filter="data")
        scanner = Path(tmp) / "bin" / "check-layout-literals"
        if not scanner.exists():
            return "(no bin/check-layout-literals at this revision)", {}, {}, None, []
        run = subprocess.run([sys.executable, "-I", str(scanner), "--all"], cwd=tmp, capture_output=True, text=True)
    counts, acked, rows = collections.Counter(), collections.Counter(), []
    summary, section = "", "sites"
    for line in run.stdout.splitlines():
        if line.startswith("acknowledged:"):
            section = "acknowledged"
        elif line.startswith("prose ") or line.startswith("not scanned:"):
            section = "other"
        m = SITE.match(line)
        if m and section == "sites":
            counts[m.group(1)] += 1
            r = ROW.match(line)
            if r:
                rows.append((r.group(1), r.group(2)))
        elif m and section == "acknowledged":
            acked[m.group(1)] += 1
        elif SUMMARY.match(line):
            summary = line
    return summary, dict(sorted(counts.items())), dict(sorted(acked.items())), run.returncode, rows


def added_lines(repo, commit):
    """{file: [added line text]} from `git show -U0` of the commit."""
    patch = git(repo, "show", "--format=", "-U0", "--no-color", commit)
    files, current = collections.defaultdict(list), None
    for line in patch.splitlines():
        if line.startswith("+++ b/"):
            current = line[6:]
        elif line.startswith("+++ "):
            current = None
        elif line.startswith("+") and current:
            files[current].append(line[1:])
    return files


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    repo, commit = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "HEAD")
    sha = git(repo, "rev-parse", commit).strip()
    parent = git(repo, "rev-parse", sha + "~1").strip()
    tree = git(repo, "rev-parse", sha + "^{tree}").strip()
    ptree = git(repo, "rev-parse", parent + "^{tree}").strip()
    print("== 1. commit and parent")
    print(f"commit {sha[:8]} (tree {tree[:8]})   parent {parent[:8]} (tree {ptree[:8]})")
    print("subject:", git(repo, "log", "-1", "--format=%s", sha).strip())
    print("\n== 2. changed files (git diff --numstat parent commit)")
    numstat = git(repo, "diff", "--numstat", parent, sha)
    print(numstat, end="")
    print(f"files: {len(numstat.splitlines())}")

    print("\n== 3. the literal scanner on the parent's tree and on the commit's tree")
    results, acks, rows = {}, {}, {}
    for label, rev in (("parent", parent), ("commit", sha)):
        summary, counts, acked, code, found = scan(repo, rev)
        results[label], acks[label], rows[label] = counts, acked, found
        print(f"{label} {rev[:8]}: {summary}   (exit {code})")
        for f, n in counts.items():
            print(f"    {n:4d}  {f}")
        print(f"  acknowledged (a `layout: ok -- reason` marker, not counted above), by file:")
        for f, n in acked.items():
            print(f"    {n:4d}  {f}")
    for what, table in (("sites", results), ("acknowledged", acks)):
        changed = sorted(set(table["parent"]) | set(table["commit"]))
        print(f"{what} per file, parent -> commit (only files that differ):")
        differ = [f for f in changed if table["parent"].get(f, 0) != table["commit"].get(f, 0)]
        for f in differ:
            print(f"    {f}: {table['parent'].get(f, 0)} -> {table['commit'].get(f, 0)}")
        if not differ:
            print("    (none differ)")

    print("\n== 3b. what became of the parent's counted site lines in the files whose site count fell (CRUDE)")
    print("   A site line 'survives' if its first 60 characters occur verbatim in the commit's version of the file")
    print("   (as code, prose or an acknowledged line). Not a 1:1 map: a rewritten line does not survive, and a new")
    print("   acknowledged line has no parent counterpart. It shows whether the counts are the SAME lines.")
    for f in sorted(f for f in results["parent"] if results["commit"].get(f, 0) < results["parent"][f]):
        body = git(repo, "show", f"{sha}:{f}") if f in git(repo, "ls-tree", "-r", "--name-only", sha).split() else ""
        mine = [t for ff, t in rows["parent"] if ff == f]
        kept = sum(1 for t in mine if t.rstrip(".").strip()[:60] in body)
        print(f"    {f}: {len(mine)} parent site lines, {kept} verbatim in the commit's file, {len(mine) - kept} not")

    print("\n== 4. fork-internal references on the commit's added lines (regex SCRUB; rough)")
    total_added, total_hits = 0, 0
    for f, lines in sorted(added_lines(repo, sha).items()):
        hits = sum(1 for ln in lines if SCRUB.search(ln))
        total_added += len(lines)
        total_hits += hits
        print(f"    {hits:4d} of {len(lines):5d} added lines  {f}")
    print(f"    {total_hits} of {total_added} added lines in total")
    print("regex:", SCRUB.pattern)

    print("\n== 5. the merge of the commit with each ref (merge-tree, empty attribute tree = GitHub's view)")
    print("   for each ref: the commit, its parent (what the earlier layers already conflict in), and, for a ref other")
    print("   than upstream/main, upstream/main itself (what the ref conflicts in before any layer is added)")
    for ref in (sys.argv[3:] or ["upstream/main"]):
        merges = [(sha, "commit"), (parent, "parent")]
        if git(repo, "rev-parse", ref).strip() != git(repo, "rev-parse", "upstream/main").strip():
            merges.append(("upstream/main", "control"))
        for ours, label in merges:
            merge_report(repo, ours, ref, label)


def merge_report(repo, ours, ref, label):
    run = subprocess.run(
        ["git", "-C", repo, f"--attr-source={EMPTY_TREE}", "merge-tree", "--write-tree", "--name-only", ours, ref],
        capture_output=True, text=True)
    lines = run.stdout.splitlines()
    tree = lines[0] if lines else ""
    short = lambda r: git(repo, "rev-parse", "--short=8", r).strip()
    print(f"{label:8s} {short(ours)} with {short(ref)}: merge-tree exit {run.returncode} "
          f"(0 clean, 1 conflicts), tree {tree[:12]}")
    if run.returncode == 1:
        names = []
        for ln in lines[1:]:
            if not ln.strip():
                break
            names.append(ln.strip())
        regions = 0
        for name in names:
            n = sum(1 for ln in git(repo, "show", f"{tree}:{name}").splitlines() if ln.startswith("<<<<<<<"))
            regions += n
            print(f"    {name}: {n} conflict region(s)")
        print(f"    total: {regions} region(s) in {len(names)} file(s)")
    elif run.returncode != 0:
        print("    merge-tree failed:", run.stderr.strip()[:200])


if __name__ == "__main__":
    main()
