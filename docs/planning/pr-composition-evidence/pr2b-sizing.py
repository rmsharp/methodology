#!/usr/bin/env python3
"""How big is PR2b? Apply the candidate's commits, one at a time, onto `upstream/main` and record which stop.

PR2b (docs/planning/upstream-pr-composition-plan.md, section 5) rebuilds `pr2/candidate` on `upstream/main`.
This script sizes that rebuild without doing it: it applies each of the candidate's commits in order onto the
result of the one before (the semantics of `git cherry-pick`, built with `git merge-tree --write-tree
--merge-base=<commit>^`) and records, per commit, the files in conflict, the conflict regions, and how many lines
each side of a region holds. A conflict is resolved to the commit's side ONLY so the sequence can go on; no
resolution is kept, no branch is made, and the fork is not touched.

A conflict has to be resolved somehow for the sequence to go on, and the choice changes what later commits meet, so the
sequence is run under BOTH extremes: policy A, the commit's side wins (the candidate's old trimmer survives, so later commits
find the lines they expect and look cheap), and policy B, upstream's side wins (upstream's trimmer survives, which is the
plan's resolution, "upstream's 1.8.2 plus the fork's layout hunks", so later commits must apply onto text they were not
written against). The real cost, which is a person reading each region, lies between them.

It runs in a throwaway BARE clone made with `git clone --bare --no-local` (a copy of the objects, no working tree),
so the fork's refs, index and object store are left alone. `--attr-source` is the empty tree, so `merge=union`
does not apply: that is GitHub's view, the same as `conflicts-after-merge.sh`, and the maintainer, who merges
locally, sees fewer conflicts in the ledger files (the candidate changes none, so it does not matter here).

A "region" is a unit of the marker style: the default style (GitHub's, and the 46 of the plan) splits one clash into
small regions, `zdiff3` groups the same clash into fewer, larger ones and shows the base. So every count here is the
default style's, and `zdiff3` is used for one thing only: telling a collision of two ADDITIONS (empty base; the usual
resolution is to keep both) from two CHANGES to the same lines (a person reads it). That split is the grouped view's.

Three measures, in this order (the third under two policies):
  1. CONTROL: the whole candidate against `upstream/main` in one merge. It must read what
     `conflicts-after-merge.sh` read (46 regions in 4 files at S375), or this instrument is wrong.
  2. PREDICTION, derived and not measured: a commit can stop only if it touches a file upstream changed since the
     candidate's base. (Context lines are the only way a commit meets upstream's work.)
  3. STACKED: the measurement. A commit is compared with the prediction.

Run from anywhere inside the repository:  python3 docs/planning/pr-composition-evidence/pr2b-sizing.py [--keep]
Needs network only for `git fetch upstream`. Python 3 standard library only. Takes about a minute.
"""
import os
import shutil
import subprocess
import sys
import tempfile

EMPTY = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
CAND = "pr2/candidate"
UPREF = "refs/remotes/upstream/main"
IDENT = {"GIT_AUTHOR_NAME": "sizing", "GIT_AUTHOR_EMAIL": "sizing@example.invalid",
         "GIT_COMMITTER_NAME": "sizing", "GIT_COMMITTER_EMAIL": "sizing@example.invalid",
         "GIT_AUTHOR_DATE": "2026-01-01T00:00:00Z", "GIT_COMMITTER_DATE": "2026-01-01T00:00:00Z"}


def sh(args, cwd, ok=(0,), env=None):
    e = dict(os.environ)
    e.update(env or {})
    p = subprocess.run(args, cwd=cwd, env=e, capture_output=True)
    out = p.stdout.decode("utf-8", "replace")
    if p.returncode not in ok:
        sys.exit("command failed (%d): %s\n%s" % (p.returncode, " ".join(args), p.stderr.decode("utf-8", "replace")))
    return p.returncode, out


def merge_tree(cwd, ours, theirs, base=None, x=None, style=None):
    """(exit code, tree OID, conflicted paths, messages). Exit 0 clean, 1 conflicts."""
    a = ["git"] + (["-c", "merge.conflictStyle=" + style] if style else []) + ["--attr-source=" + EMPTY, "merge-tree", "--write-tree", "--name-only", "--messages"]
    if x:
        a += ["-X", x]
    if base:
        a.append("--merge-base=" + base)
    rc, out = sh(a + [ours, theirs], cwd, ok=(0, 1))
    lines = out.split("\n")
    tree, files, i = lines[0], [], 1
    if rc == 1:
        while i < len(lines) and lines[i] != "":
            files.append(lines[i])
            i += 1
    return rc, tree, files, "\n".join(lines[i:])


def regions(cwd, tree, path):
    """(regions, lines ours, lines theirs, opening markers seen, regions whose base is empty) of a conflicted blob.
    A region with an empty base is a collision of two ADDITIONS at one spot: the usual resolution is to keep both."""
    rc, _ = sh(["git", "cat-file", "-e", "%s:%s" % (tree, path)], cwd, ok=(0, 128))
    if rc != 0:
        return 0, 0, 0, 0, 0
    _, text = sh(["git", "cat-file", "blob", "%s:%s" % (tree, path)], cwd)
    n = o = t = opens = added = base_lines = 0
    state = None
    for line in text.split("\n"):
        if line.startswith("<<<<<<< "):
            opens += 1
            state, base_lines = "ours", 0
        elif line.startswith("||||||| ") and state == "ours":
            state = "base"
        elif line.startswith("=======") and state in ("ours", "base"):
            state = "theirs"
        elif line.startswith(">>>>>>> ") and state == "theirs":
            n += 1
            added += 1 if base_lines == 0 else 0
            state = None
        elif state == "ours":
            o += 1
        elif state == "base":
            base_lines += 1
        elif state == "theirs":
            t += 1
    return n, o, t, opens, added


def measure(cwd, tree, files):
    """{path: (regions, ours lines, theirs lines, regions with an empty base)} and a flag when the marker count disagrees."""
    out, bad = {}, False
    for f in files:
        n, o, t, opens, a = regions(cwd, tree, f)
        out[f] = (n, o, t, a)
        bad = bad or opens != n
    return out, bad


def main():
    keep = "--keep" in sys.argv
    _, root = sh(["git", "rev-parse", "--show-toplevel"], os.getcwd())
    root = root.strip()
    sh(["git", "fetch", "-q", "upstream"], root)
    _, gv = sh(["git", "--version"], root)
    _, up = sh(["git", "rev-parse", UPREF], root)
    _, cand = sh(["git", "rev-parse", CAND], root)
    up, cand = up.strip(), cand.strip()
    _, base = sh(["git", "merge-base", cand, up], root)
    base = base.strip()
    _, rl = sh(["git", "rev-list", "--reverse", "--no-merges", base + ".." + cand], root)
    commits = rl.split()
    _, nm = sh(["git", "rev-list", "--merges", "--count", base + ".." + cand], root)
    print("== inputs")
    print("%s" % gv.strip())
    print("upstream/main %s; %s %s; base (merge-base) %s" % (up[:8], CAND, cand[:8], base[:8]))
    print("commits to apply: %d (merges among them: %s); upstream is %s commits past the base" % (
        len(commits), nm.strip(), sh(["git", "rev-list", "--count", base + ".." + up], root)[1].strip()))
    _, uf = sh(["git", "diff", "--name-only", base, up], root)
    ufiles = set(uf.split())
    print("files upstream changed since the base (%d): %s" % (len(ufiles), " ".join(sorted(ufiles))))

    tmp = tempfile.mkdtemp(prefix="pr2b-sizing-")
    s = os.path.join(tmp, "scratch.git")
    try:
        sh(["git", "clone", "--bare", "--no-local", "-q", root, s], root)
        sh(["git", "fetch", "-q", root, UPREF + ":refs/heads/up-main"], s)

        print("\n== 1. control: the whole candidate against upstream/main in one merge (S375 read 46 regions in 4 files)")
        rc, tree, files, _ = merge_tree(s, cand, up)
        m, bad = measure(s, tree, files)
        tot = sum(v[0] for v in m.values())
        _, tree3, files3, _ = merge_tree(s, cand, up, style="zdiff3")
        g, _ = measure(s, tree3, files3)
        print("merge-tree exit %d; %d region(s) in %d file(s)%s" % (rc, tot, len(files), "  [MARKER COUNT DISAGREES WITH PARSE]" if bad else ""))
        print("grouped view (zdiff3): %d region(s), %d of them with an empty base" % (sum(v[0] for v in g.values()), sum(v[3] for v in g.values())))
        for f in files:
            print("   %-40s %3d region(s); grouped %d (%d empty-base); %4d lines ours / %4d lines theirs" % (
                f, m[f][0], g.get(f, (0,) * 4)[0], g.get(f, (0,) * 4)[3], m[f][1], m[f][2]))
        control_total = tot

        print("\n== 2. prediction (derived, not measured): a commit can stop only if it touches a file upstream changed")
        touch = {}
        for c in commits:
            _, names = sh(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", c], s)
            touch[c] = sorted(set(names.split()) & ufiles)
        pred = [c for c in commits if touch[c]]
        print("%d of %d commits touch at least one of those files: %s" % (len(pred), len(commits), " ".join(str(commits.index(c) + 1) for c in pred)))

        POL = (("A", "theirs", "the commit's side wins"), ("B", "ours", "upstream's side wins"))
        res = {}
        for tag, xopt, what in POL:
            tip, rows, detail, per_file = up, [], [], {}
            for i, c in enumerate(commits, 1):
                rc, tree, files, msgs = merge_tree(s, tip, c, base=c + "^")
                m, bad = measure(s, tree, files) if rc == 1 else ({}, False)
                g = {}
                if rc == 1:
                    _, tree3, files3, _ = merge_tree(s, tip, c, base=c + "^", style="zdiff3")
                    g, _ = measure(s, tree3, files3)
                resid = ""
                if rc == 1:
                    rc2, tree2, files2, _ = merge_tree(s, tip, c, base=c + "^", x=xopt)
                    if rc2 != 0:
                        resid = "residual after -X %s: %s" % (xopt, ", ".join(files2))
                    tree = tree2
                regs = sum(v[0] for v in m.values())
                rows.append((i, c[:8], rc, regs, bad, resid))
                for f, v in m.items():
                    gv = g.get(f, (0, 0, 0, 0))
                    detail.append((i, c[:8], f, (v[0], v[1], v[2], gv[0], gv[3])))
                    pf = per_file.setdefault(f, [0, 0, 0, 0, 0])
                    pf[0] += v[0]
                    pf[1] += v[1]
                    pf[2] += v[2]
                    pf[3] += gv[0]
                    pf[4] += gv[3]
                _, tip = sh(["git", "commit-tree", tree, "-p", tip, "-m", "pick %s" % c[:8]], s, env=IDENT)
                tip = tip.strip()
            res[tag] = (rows, detail, per_file, tip)

        print("\n== 3. stacked: commit i is applied onto the result of commit i-1")
        print("policy A: a conflict is resolved to the commit's side; policy B: to upstream's side. Either is only to go on; neither is a resolution.")
        print(" #  commit    A: stop regions   B: stop regions   touches-upstream-file  subject")
        for k, c in enumerate(commits):
            ra, rb = res["A"][0][k], res["B"][0][k]
            _, subj = sh(["git", "log", "-1", "--format=%s", c], s)
            flag = ("  [MARKER COUNT DISAGREES]" if (ra[4] or rb[4]) else "") + ("  [A %s]" % ra[5] if ra[5] else "") + ("  [B %s]" % rb[5] if rb[5] else "")
            print("%2d  %s  %s %7s        %s %7s        %-21s  %s%s" % (
                k + 1, c[:8], "STOP" if ra[2] else " -  ", ra[3] if ra[2] else "-", "STOP" if rb[2] else " -  ",
                rb[3] if rb[2] else "-", "yes" if c in pred else "no", subj[:60], flag))
        for tag, xopt, what in POL:
            rows, detail, per_file, tip = res[tag]
            stops = [r for r in rows if r[2] == 1]
            print("\n-- policy %s (%s): %d of %d commits stop; %d region(s) in all (the one-shot control reads %d); grouped view: %d region(s), %d with an empty base" % (
                tag, what, len(stops), len(rows), sum(r[3] for r in rows), control_total, sum(d[3][3] for d in detail), sum(d[3][4] for d in detail)))
            ok = all(commits[r[0] - 1] in pred for r in stops)
            print("   prediction check: %s" % ("every stopper touches an upstream-changed file (as derived)" if ok else "A STOPPER WAS NOT PREDICTED"))
            print("    #  commit    file                                      regions  grouped (empty-base)  lines ours / theirs")
            for (i, c8, f, v) in detail:
                print("   %2d  %s  %-40s  %7d  %7d (%d)%s  %5d / %d" % (i, c8, f, v[0], v[3], v[4], " " * 8, v[1], v[2]))
            print("   by file:")
            for f in sorted(per_file, key=lambda k: -per_file[k][0]):
                print("     %-40s %3d region(s); grouped %d (%d empty-base); %4d lines ours / %4d lines theirs" % (
                    f, per_file[f][0], per_file[f][3], per_file[f][4], per_file[f][1], per_file[f][2]))
            _, v = sh(["git", "show", "%s:starter-kit/methodology_trim.py" % tip], s)
            tv = [l for l in v.split("\n") if l.startswith("TRIM_VERSION")][:1]
            _, d = sh(["git", "diff", "--numstat", tip, cand], s)
            print("   TRIM_VERSION on this tip: %s; files where this tip differs from the candidate (added, removed):" % (tv[0][:32] if tv else "(none)"))
            print("\n".join("     " + l for l in d.rstrip().split("\n")) if d.strip() else "     (identical)")
        print("\n== 4. the trimmer lineage in numbers: is upstream's copy the candidate's lineage, edited? (added / removed lines between two versions of a file)")
        c1, c5 = commits[0], commits[4]
        for path in ("starter-kit/methodology_trim.py", "tools/test_methodology_trim.py"):
            def nstat(a, b):
                _, o = sh(["git", "diff", "--numstat", a, b, "--", path], s)
                f = o.split()
                return "+%s / -%s" % (f[0], f[1]) if f else "identical"
            _, wc = sh(["git", "show", "%s:%s" % (up, path)], s)
            print("%s (%d lines on upstream/main)" % (path, wc.count("\n")))
            print("   base -> upstream/main            %-16s what upstream did to it since the base (#94's lineage and the maintainer's fixes)" % nstat(base, up))
            print("   base -> candidate, commit 1      %-16s the lineage as the candidate carries it (to 1.7.0)" % nstat(base, c1))
            print("   candidate commit 1 -> upstream   %-16s how far apart the two copies of that lineage are now" % nstat(c1, up))
            print("   commit 5's own change            %-16s the layout hunks (1.8.0), the fork's real addition to the trimmer" % nstat(c5 + "^", c5))
            print("   commit 1 -> candidate tip        %-16s everything the candidate adds after the lineage (1.8.0, the scrub, 1.8.1)" % nstat(c1, cand))
            print("   upstream -> candidate tip        %-16s the two final copies" % nstat(up, cand))
        for r, ref in (("upstream/main", up), (CAND, cand)):
            _, v = sh(["git", "show", "%s:starter-kit/methodology_trim.py" % ref], s)
            tv = [l for l in v.split("\n") if l.startswith("TRIM_VERSION")][:1]
            print("   TRIM_VERSION on %-14s %s" % (r, tv[0][:32] if tv else "(none)"))
    finally:
        if keep:
            print("\nscratch kept at %s" % s)
        else:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
