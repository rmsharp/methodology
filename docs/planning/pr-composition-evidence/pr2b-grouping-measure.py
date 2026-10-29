#!/usr/bin/env python3
"""PR2b grouping plan: what the twelve remaining candidate commits are and how they behave, by command (S393).

Usage:  python3 -I pr2b-grouping-measure.py <repo> <scratch-clone-dir> <tip-ref> <old-candidate-ref> <open-head-branch> [...]

READ-ONLY on <repo>. The replay happens in a --no-local clone made at <scratch-clone-dir> (it must not exist), where no hook
is armed. Numbers count from 1 along `git log --reverse upstream/main..<old-candidate-ref>`; the remaining ones are 21 to 30,
32 and 33 (31 is already in the tip as a replay, 34 is dropped as superseded). The open heads are local branch names; in the
clone they are `origin/<name>`.

  1  inventory: files, lines, and a CLASS per file proved by comparison (a Python file's syntax tree without comments and
     docstring statements; then with every string literal masked; a shell file without its full-line comments; a gate file
     with every `why` masked), not read from the commit's subject
  2  each commit alone onto the tip (merge-tree, exit and conflict regions)
  3  the twelve replayed IN ORDER onto the tip, `git cherry-pick -x`; a conflict is described (regions, sizes) and aborted,
     and the replay goes on; every clean one is compared with its original by `git patch-id --stable`
  4  scrub-proof.py over the replayed range (no code token changed anywhere)
  5  fork-token lines per file at the tip and after the replay (scrub-derive.py), and which commit touches the file
  6  the two open pull requests: files each changes (with a control), overlap with each commit, merge-tree regions at the
     tip and after the replay (attributes off, GitHub's view)
  7  the read-set budget at the tip and after the replay

Standard library only.
"""
import ast
import json
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
repo, clone, tip_ref, old_ref = sys.argv[1:5]
heads = sys.argv[5:]
NUMS = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 32, 33]
IDENT = ["-c", "user.name=S393 measure", "-c", "user.email=measure@example.invalid"]
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
RANK = {"comments and docstrings only": 0, "comments only (shell)": 0, "gate reason text only": 1,
        "string literals changed": 2, "shell lines changed (not full-line comments)": 3, "code changed": 4,
        "a gate value changed": 4, "added or removed": 4}


def run(cwd, *cmd, inp=None):
    r = subprocess.run(list(cmd), cwd=cwd, capture_output=True, text=True, input=inp)
    return r.returncode, r.stdout, r.stderr


def git(cwd, *a):
    return run(cwd, "git", *a)


def gitout(cwd, *a):
    rc, o, e = git(cwd, *a)
    if rc:
        raise SystemExit("git %s: %s" % (" ".join(a), e.strip()))
    return o


def blob(cwd, rev, path):
    rc, o, _ = git(cwd, "show", "%s:%s" % (rev, path))
    return o if rc == 0 else None


def head(title):
    print("\n==== %s ====" % title)


def clean_tree(tree, mask):
    """Drop bare string statements (docstrings); with mask, blank every string literal."""
    for node in ast.walk(tree):
        for field in ("body", "orelse", "finalbody"):
            lst = getattr(node, field, None)
            if isinstance(lst, list) and lst and all(isinstance(x, ast.stmt) for x in lst):
                new = [x for x in lst if not (isinstance(x, ast.Expr) and isinstance(x.value, ast.Constant)
                                              and isinstance(x.value.value, str))]
                if len(new) != len(lst):
                    setattr(node, field, new or [ast.Pass()])
        if mask and isinstance(node, ast.Constant) and isinstance(node.value, str):
            node.value = ""
    return tree


def classify(path, old, new):
    if old is None or new is None:
        return "added or removed"
    if path.endswith(".json"):
        def mask(o):
            if isinstance(o, dict):
                return {k: ("" if k == "why" else mask(v)) for k, v in o.items()}
            if isinstance(o, list):
                return [mask(x) for x in o]
            return o
        return "gate reason text only" if mask(json.loads(old)) == mask(json.loads(new)) else "a gate value changed"
    first = new.split("\n", 1)[0]
    if path.endswith(".py") or (first.startswith("#!") and "python" in first):
        if ast.dump(clean_tree(ast.parse(old), False)) == ast.dump(clean_tree(ast.parse(new), False)):
            return "comments and docstrings only"
        if ast.dump(clean_tree(ast.parse(old), True)) == ast.dump(clean_tree(ast.parse(new), True)):
            return "string literals changed"
        return "code changed"

    def strip(t):
        return [l.rstrip() for l in t.splitlines() if not (l.lstrip().startswith("#") and not l.startswith("#!"))]
    return "comments only (shell)" if strip(old) == strip(new) else "shell lines changed (not full-line comments)"


def numstat(cwd, rev):
    out = []
    for line in gitout(cwd, "show", "--numstat", "--format=", rev).splitlines():
        a, d, p = line.split("\t")
        out.append((p, int(a), int(d)))
    return out


def regions_of(text):
    return sum(1 for l in text.splitlines() if l.startswith("<<<<<<< "))


def merge_alone(cwd, tipref, c):
    rc, o, _ = git(cwd, "merge-tree", "--write-tree", "--name-only", "--merge-base=%s^" % c, tipref, c)
    lines = o.split("\n")
    files = []
    if rc == 1:
        for l in lines[1:]:
            if l == "":
                break
            files.append(l)
    regs = {f: regions_of(git(cwd, "cat-file", "-p", lines[0] + ":" + f)[1]) for f in files}
    return rc, regs


def merge_regions(cwd, a, b):
    rc, o, _ = git(cwd, "--attr-source=" + EMPTY_TREE, "merge-tree", "--write-tree", "--name-only", a, b)
    lines = o.split("\n")
    files = []
    if rc == 1:
        for l in lines[1:]:
            if l == "":
                break
            files.append(l)
    return rc, {f: regions_of(git(cwd, "cat-file", "-p", lines[0] + ":" + f)[1]) for f in files}


def patch_id(cwd, rev):
    rc, shown, _ = run(cwd, "git", "show", rev)
    rc, out, _ = run(cwd, "git", "patch-id", "--stable", inp=shown)
    return out.split()[0][:12] if out.split() else "?"


def fmt_regs(regs):
    return ", ".join("%s %d" % (f, n) for f, n in sorted(regs.items())) or "none"


def conflict_detail(cwd, path):
    """Regions of a conflicted worktree file: line number, lines on each side, first line of each side."""
    text = open(os.path.join(cwd, path), errors="replace").read().splitlines()
    out, i = [], 0
    while i < len(text):
        if text[i].startswith("<<<<<<< "):
            j = i + 1
            while j < len(text) and not text[j].startswith("======="):
                j += 1
            k = j + 1
            while k < len(text) and not text[k].startswith(">>>>>>> "):
                k += 1
            ours, theirs = text[i + 1:j], text[j + 1:k]
            out.append("      %s:%d  ours %d lines, theirs %d lines; ours[0]=%r theirs[0]=%r" % (
                path, i + 1, len(ours), len(theirs), (ours[0] if ours else "")[:70], (theirs[0] if theirs else "")[:70]))
            i = k
        i += 1
    return out


def tokens_by_file(out):
    rows, on = {}, False
    for l in out.splitlines():
        if l.startswith("per file"):
            on = True
            continue
        if on:
            m = re.match(r"^  (\S+)\s+(\d+)\s+(\d+)\s+", l)
            if m:
                rows[m.group(1)] = int(m.group(2))
            elif not l.strip():
                break
    total = re.search(r"lines with at least one strict token: (\d+) in (\d+) files", out)
    return rows, (total.group(0) if total else "?")


def budget(cwd, label):
    rc, o, _ = run(cwd, "python3", "-I", "starter-kit/context_budget.py", "--status")
    keep = [l for l in o.splitlines() if "resident total" in l or "read-set total" in l or "context budget" in l]
    print("  %s: exit %d" % (label, rc))
    for l in keep:
        print("    " + re.sub(r"\x1b\[[0-9;]*m", "", l).replace("─", "").strip())


def try_order(label, order):
    """Cherry-pick the numbers in this order from a clean tip; stop at the first conflict."""
    gitout(clone, "checkout", "-q", "--detach", tip)
    stop = None
    for n in order:
        rc, _, e = git(clone, *IDENT, "cherry-pick", "-x", commit[n])
        if rc:
            stop = (n, gitout(clone, "diff", "--name-only", "--diff-filter=U").split())
            git(clone, "cherry-pick", "--abort")
            break
    tree = gitout(clone, "rev-parse", "HEAD^{tree}").strip()[:12]
    print("  %-34s %s  tree %s  %s" % (label, order, tree, ("CONFLICT at %d in %s" % stop) if stop else "all clean"))
    return tree


# ---------------------------------------------------------------------------------------------------------------------
print("# PR2b grouping measurement (S393). repo %s" % repo)
print("# uptime: %s" % run(".", "uptime")[1].strip())
tip = gitout(repo, "rev-parse", tip_ref).strip()
upstream = gitout(repo, "rev-parse", "upstream/main").strip()
series = gitout(repo, "log", "--reverse", "--format=%H", "upstream/main.." + old_ref).split()
print("# tip %s (%s)  upstream/main %s  old candidate %s: %d commits" % (
    tip[:8], tip_ref, upstream[:8], old_ref, len(series)))
commit = {n: series[n - 1] for n in NUMS}
for n in (31, 34):
    print("# not in the twelve: %d %s %s" % (n, series[n - 1][:8], gitout(repo, "log", "-1", "--format=%s", series[n - 1]).strip()[:100]))

head("1. inventory and class (as each commit was authored, against its own parent)")
klass = {}
for n in NUMS:
    c = commit[n]
    subject = gitout(repo, "log", "-1", "--format=%s", c).strip()
    stat = numstat(repo, c)
    worst, rows = 0, []
    for p, a, d in stat:
        k = classify(p, blob(repo, c + "^", p), blob(repo, c, p))
        worst = max(worst, RANK[k])
        rows.append("      %-44s +%-4d -%-4d %s" % (p, a, d, k))
    klass[n] = [k for k, v in RANK.items() if v == worst][0]
    print("  %2d %s  %d files +%d/-%d  worst class: %s\n     %s" % (
        n, c[:8], len(stat), sum(s[1] for s in stat), sum(s[2] for s in stat), klass[n], subject[:110]))
    print("\n".join(rows))

head("2. each commit ALONE onto the tip (merge-tree --write-tree --merge-base=<commit>^; exit 0 clean, 1 conflicts)")
for n in NUMS:
    rc, regs = merge_alone(repo, tip, commit[n])
    print("  %2d %s exit %d  %s" % (n, commit[n][:8], rc, ("regions: " + fmt_regs(regs)) if rc else ""))

# ---------------------------------------------------------------------------------------------------------------------
head("3. the twelve IN ORDER onto the tip (git cherry-pick -x in a --no-local clone; a conflict is described, aborted, and the replay goes on)")
if os.path.exists(clone):
    raise SystemExit("scratch clone dir exists: " + clone)
run(".", "git", "clone", "-q", "--no-local", repo, clone)
gitout(clone, "checkout", "-q", "--detach", tip)
applied, milestones = [], {}
for n in NUMS:
    c = commit[n]
    rc, o, e = git(clone, *IDENT, "cherry-pick", "-x", c)
    if rc == 0:
        new = gitout(clone, "rev-parse", "HEAD").strip()
        po, pn = patch_id(clone, c), patch_id(clone, new)
        applied.append(n)
        print("  %2d %s clean -> %s; patch-id original %s replay %s %s" % (n, c[:8], new[:8], po, pn, "EQUAL" if po == pn else "DIFFERENT"))
    else:
        unmerged = gitout(clone, "diff", "--name-only", "--diff-filter=U").split()
        print("  %2d %s CONFLICT in %d file(s): %s" % (n, c[:8], len(unmerged), ", ".join(unmerged) or "(none; %s)" % (e.strip().splitlines() or ["?"])[0]))
        for p in unmerged:
            for line in conflict_detail(clone, p):
                print(line)
        git(clone, "cherry-pick", "--abort")
    milestones[n] = gitout(clone, "rev-parse", "HEAD").strip()
replayed = gitout(clone, "rev-parse", "HEAD").strip()
print("  applied clean in order: %s; conflicting: %s" % (applied, [n for n in NUMS if n not in applied]))
print("  tip -> replayed %s: %s" % (replayed[:8], gitout(clone, "diff", "--shortstat", tip, replayed).strip()))
print("  cumulative shortstat after each clean commit (tip..that commit):")
for n in applied:
    print("    after %2d: %s" % (n, gitout(clone, "diff", "--shortstat", tip, milestones[n]).strip()))

head("3b. does the ORDER matter? (each order from a clean tip, stopping at the first conflict; equal tree ids mean the same result)")
t_full = gitout(clone, "rev-parse", replayed + "^{tree}").strip()[:12]
print("  the replay of section 3 (all eleven, skipping 26): tree %s" % t_full)
try_order("A, 32, then B, then 33", [21, 22, 23, 24, 25, 27, 32, 28, 29, 30, 33])
try_order("A, 32, 33, then B", [21, 22, 23, 24, 25, 27, 32, 33, 28, 29, 30])
try_order("A, B, 33 (no 32)", [21, 22, 23, 24, 25, 27, 28, 29, 30, 33])
try_order("A, 33 (B refused)", [21, 22, 23, 24, 25, 27, 33])
try_order("A, 32 (B and 33 left)", [21, 22, 23, 24, 25, 27, 32])
try_order("A, B (32 and 33 left)", [21, 22, 23, 24, 25, 27, 28, 29, 30])
try_order("B alone on the tip", [28, 29, 30])
try_order("B without 30, on the tip", [28, 29])
try_order("33 alone on the tip", [33])
try_order("22 then 30 (what 30 needs)", [22, 30])
try_order("27 then 33 (what 33 needs)", [27, 33])
gitout(clone, "checkout", "-q", "--detach", replayed)

head("4. scrub-proof.py (no code token changed; strings and comments masked): the scrub-only range, then with commit 33")
for label, upto in (("tip..after 32 (A without 26, B, 32)", milestones[32]), ("tip..after 33 (commit 33 is code, not a scrub)", replayed)):
    rc, o, e = run(".", "python3", "-I", os.path.join(HERE, "scrub-proof.py"), clone, tip, upto)
    lines = (o + e).strip().splitlines()
    print("  %s: exit %d" % (label, rc))
    print("\n".join("    " + l for l in lines if "FAILED" in l or "CUMULATIVE" in l or "byte-identical" in l or "diff against" in l))

head("5. fork-token lines per file (scrub-derive.py: strict classes, added lines against upstream/main)")
rc1, o1, _ = run(repo, "python3", "-I", os.path.join(HERE, "scrub-derive.py"), tip, "upstream/main")
rc2, o2, _ = run(clone, "python3", "-I", os.path.join(HERE, "scrub-derive.py"), replayed, upstream)
t1, s1 = tokens_by_file(o1)
t2, s2 = tokens_by_file(o2)
print("  at the tip:        %s" % s1)
print("  after the replay:  %s" % s2)
touched = {}
for n in NUMS:
    for p, _, _ in numstat(repo, commit[n]):
        touched.setdefault(p, []).append(n)
print("  %-46s %5s %6s   touched by" % ("file", "tip", "after"))
for p in sorted(set(t1) | set(t2), key=lambda p: -t1.get(p, 0)):
    print("  %-46s %5d %6d   %s" % (p, t1.get(p, 0), t2.get(p, 0), ",".join(map(str, touched.get(p, []))) or "-"))
print("  files with token lines at the tip that none of the twelve touches: %s" % (
    ", ".join(p for p in sorted(t1) if p not in touched) or "none"))

head("6. the two open pull requests")
for h in heads:
    names = gitout(repo, "diff", "--name-only", "upstream/main..." + h).split()
    control = "starter-kit/methodology_trim.py" if "issue93" in h else "bin/tests.sh"
    print("  %s changes %d files; control %s in the list: %s" % (h, len(names), control, control in names))
    for n in NUMS:
        ov = [p for p, _, _ in numstat(repo, commit[n]) if p in names]
        if ov:
            print("    %2d overlaps by file: %s" % (n, ", ".join(ov)))
    for label, rev in (("tip", tip), ("after the replay", replayed)):
        rc, regs = merge_regions(clone, rev, "origin/" + h)
        print("    merge-tree %s with it: exit %d  %s" % (label, rc, fmt_regs(regs)))

head("7. the read-set budget (context_budget.py --status)")
gitout(clone, "checkout", "-q", "--detach", tip)
budget(clone, "at the tip")
run(clone, "git", "clean", "-fdq")
gitout(clone, "checkout", "-q", "--detach", replayed)
budget(clone, "after the replay")
run(clone, "git", "clean", "-fdq")
head("8. the dashboard suite at the replayed tip (the gate dashboard-unit-tests: floor 395 at the tip, 397 in commit 33)")
r = subprocess.run(["python3", "tools/test_methodology_dashboard.py"], cwd=clone, capture_output=True, text=True,
                   env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
tail = (r.stdout + r.stderr).strip().splitlines()[-4:]
print("  exit %d" % r.returncode)
print("\n".join("    " + l for l in tail))
print("  gate floor in the replayed tree: %s" % re.search(r'"dashboard-unit-tests"[^}]*?"threshold": (\d+)', blob(clone, replayed, ".quality-gates.json"), re.S).group(1))

run(clone, "git", "clean", "-fdq")
print("\n# clone dirty paths at the end: %d" % len(gitout(clone, "status", "--short").splitlines()))
print("# uptime: %s" % run(".", "uptime")[1].strip())
