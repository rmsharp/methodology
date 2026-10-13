#!/usr/bin/env python3
"""Fork-internal tokens on the lines the fork added to files that would go upstream (S308).

Run from anywhere inside the repository:  python3 -I docs/planning/pr-composition-evidence/fork-tokens.py

Counts, over the ADDED lines of the shipped, tool, test and hook files (upstream/main..HEAD), the lines that carry a backlog
code (BL-nnn), a session number (S###), a fork-learning citation, a path under docs/planning/, or a plan-phase code (P1..P23);
and lists every docs/ path those lines cite that `upstream/main` does not hold. A reader of the upstream repository cannot
follow such a path. The baseline row says how many lines of the same files upstream already carries: it is a precedent for
a token, not a defence of a dangling path. A plain regular-expression count: eyeball a sample before quoting a figure.
"""
import collections
import os
import re
import subprocess

UP = "upstream/main"


def sh(*a, check=True):
    r = subprocess.run(a, capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit("git failed: %s" % " ".join(a))
    return r.stdout if r.returncode == 0 else ""


os.chdir(sh("git", "rev-parse", "--show-toplevel").strip())
SCOPE = ["starter-kit", "workstreams", "bin", "tools", ".githooks", "HOW_TO_USE.md", "ITERATIVE_METHODOLOGY.md",
         "FRAMEWORK_APPARATUS.md"]
files = sh("git", "diff", "--name-only", UP, "HEAD", "--", *SCOPE).split()
PATS = collections.OrderedDict([
    ("backlog code (BL-nnn)", r"\bBL-\d+"),
    ("session number (S###)", r"\bS\d{2,3}\b"),
    ("fork Learning citation", r"fork Learning|fork learning"),
    ("path under docs/planning/", r"docs/planning/"),
    ("plan-phase code (P1..P23)", r"\bP\d{1,2}\b(?= |\)|,|:|\.)"),
])
tot = collections.Counter()
per = collections.defaultdict(collections.Counter)
cites = {}
for f in files:
    for ln in sh("git", "diff", "-U0", UP, "HEAD", "--", f).splitlines():
        if not ln.startswith("+") or ln.startswith("+++"):
            continue
        for k, p in PATS.items():
            if re.search(p, ln):
                tot[k] += 1
                per[f][k] += 1
        for m in re.findall(r"docs/(?:planning|archive)/[A-Za-z0-9_./\-]+?\.(?:md|py|sh|txt|json)", ln):
            cites.setdefault(m, set()).add(f)
print("ADDED lines in %d changed shipped/tool/test/hook files that carry a token:" % len(files))
for k in PATS:
    print("  %-30s %4d" % (k, tot[k]))
print("\nmost affected files:")
for f, c in sorted(per.items(), key=lambda kv: -sum(kv[1].values()))[:10]:
    print("  %-44s %s" % (f, "  ".join("%s=%d" % (k.split()[0], v) for k, v in c.items())))
base = collections.Counter()
for f in files:
    text = sh("git", "show", "%s:%s" % (UP, f), check=False)
    for ln in text.splitlines():
        for k, p in PATS.items():
            if re.search(p, ln):
                base[k] += 1
print("\nBASELINE, upstream/main's copies of the same files (lines):", dict(base))
missing = sorted(p for p in cites if subprocess.run(["git", "cat-file", "-e", "%s:%s" % (UP, p)], capture_output=True).returncode)
plans = [p for p in missing if p.startswith("docs/planning/")]
print("\n%d distinct docs/ paths cited on added lines; %d are not in upstream/main:" % (len(cites), len(missing)))
print("  docs/planning/ documents a reader cannot open (%d):" % len(plans))
for p in plans:
    print("    %-62s <- %s" % (p, ", ".join(sorted(cites[p]))[:80]))
print("  docs/archive/ names (%d), nearly all fixture names a test builds in a scratch repository, not real citations" % (len(missing) - len(plans)))
