#!/usr/bin/env python3
"""PR4: how much of the pull request reaches a project that syncs, and how much stays in this repository.

  python3 -I docs/planning/pr-composition-evidence/pr4-distribution.py <repo> <upstream> <candidate>

Reads git objects only; writes nothing. For every file the candidate changes against upstream (`git diff --numstat`),
it asks the candidate's own distribution manifest (bin/_manifest.py, read as data, never run) whether `bin/sync` copies
that file into a project: a TRACKED row (kept current), a SEED row (written once, when the project lacks it), or no row
(it stays here: tests, the repository's own tools and hooks, its gate configuration). It also derives the manifest's
row counts and the dashboard twin. Every total is asserted against `git diff --shortstat` before it is printed.
"""
import ast
import subprocess
import sys

sys.dont_write_bytecode = True
repo, up, cand = sys.argv[1:4]


def git(*a):
    r = subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("refused: git %s: %s" % (" ".join(a), r.stderr.strip()))
    return r.stdout


def distribution(rev):
    """The rows of DISTRIBUTION at <rev> as (src, dest, disposition), read with ast and never executed."""
    tree = ast.parse(git("show", "%s:bin/_manifest.py" % rev))
    for node in tree.body:
        if isinstance(node, ast.Assign) and [t.id for t in node.targets if isinstance(t, ast.Name)] == ["DISTRIBUTION"]:
            return [(ast.literal_eval(e.elts[0]), ast.literal_eval(e.elts[1]), e.elts[2].id) for e in node.value.elts]
    raise SystemExit("refused: no DISTRIBUTION at %s" % rev)


rows_up, rows_cand = distribution(up), distribution(cand)
print("== 1. the manifest (bin/_manifest.py): the rows a project is given")
print("upstream %s: %d rows; candidate %s: %d rows; same sources: %s" % (
    up[:7], len(rows_up), cand[:7], len(rows_cand), sorted(s for s, _, _ in rows_up) == sorted(s for s, _, _ in rows_cand)))
for label, test in (("at the project root", lambda d: "/" not in d), ("under docs/methodology/", lambda d: d.startswith("docs/methodology/"))):
    sel = [r for r in rows_cand if test(r[1])]
    print("  %-26s %2d rows: %2d TRACKED, %2d SEED" % (label, len(sel), sum(r[2] == "TRACKED" for r in sel), sum(r[2] == "SEED" for r in sel)))
other = [r for r in rows_cand if "/" in r[1] and not r[1].startswith("docs/methodology/")]
print("  elsewhere                  %2d rows" % len(other))
print("  all                        %2d rows: %2d TRACKED, %2d SEED" % (
    len(rows_cand), sum(r[2] == "TRACKED" for r in rows_cand), sum(r[2] == "SEED" for r in rows_cand)))

disposition = {s: d for s, _, d in rows_cand}
print("\n== 2. every file the candidate changes against upstream, by what `bin/sync` does with it")
classes = [("TRACKED", "kept current by bin/sync (a project receives it at its next sync)"),
           ("SEED", "a seed's source (a NEW project receives it once; an existing project never does)"),
           (None, "not distributed (stays in this repository)")]
by_class = {c: [] for c, _ in classes}
for line in git("diff", "--numstat", up, cand).splitlines():
    added, removed, path = line.split("\t")
    by_class[disposition.get(path)].append((int(added), int(removed), path))
files = sum(len(v) for v in by_class.values())
added = sum(a for v in by_class.values() for a, _, _ in v)
removed = sum(r for v in by_class.values() for _, r, _ in v)
shortstat = git("diff", "--shortstat", up, cand).strip()
assert shortstat == "%d files changed, %d insertions(+), %d deletions(-)" % (files, added, removed), shortstat
print("git diff --shortstat: %s   (the per-file sums below add to exactly this)" % shortstat)
for key, label in classes:
    v = by_class[key]
    a, r = sum(x[0] for x in v), sum(x[1] for x in v)
    print("  %-3d files  +%-6d -%-5d  %5.1f%% of the added lines   %s" % (len(v), a, r, 100.0 * a / added, label))
print("\n-- file by file, largest first")
for key, label in classes:
    print("[%s]" % label)
    for a, r, p in sorted(by_class[key], reverse=True):
        print("  +%-5d -%-4d %s" % (a, r, p))

print("\n== 3. the dashboard is counted twice in that diff")
t, s = "tools/methodology_dashboard.py", "starter-kit/methodology_dashboard.py"
same = git("rev-parse", "%s:%s" % (cand, t)).strip() == git("rev-parse", "%s:%s" % (cand, s)).strip()
twin = [x for x in by_class[None] if x[2] == t][0]
print("%s and %s are the same blob at %s: %s" % (t, s, cand[:7], same))
print("added lines counted once: %d - %d = %d" % (added, twin[0], added - twin[0]))
