#!/usr/bin/env python3
"""What the fork carries that `upstream/main` lacks, by tree diff (S308).

Run from anywhere inside the repository:  python3 -I docs/planning/pr-composition-evidence/inventory.py

Reads git only. Why a TREE diff: upstream squash-merged earlier pull requests, so the fork's original commits are still
"ahead" by ancestry (`git rev-list --count upstream/main..HEAD` counts them); the tree difference is what a pull request
would actually carry. The BL-101 plan's base commit (`c8b9ddd`) splits the difference into the work before the
`methodology/` directory plan and the work from it on.
"""
import collections
import importlib.util
import os
import re
import subprocess
import sys

UP = "upstream/main"
BASE = "c8b9ddd"          # the BL-101 plan's base commit (fork main at S273; it contains all of upstream/main)
LEDGER = [":!docs", ":!CHANGELOG.md", ":!HANDOFFS.md", ":!dashboard_history.jsonl", ":!.context-budget-history.jsonl"]


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


ROOT = git("rev-parse", "--show-toplevel").strip()
os.chdir(ROOT)


def numstat(a, b, extra=()):
    out = git("diff", "--numstat", "-M", a, b, "--", ".", *extra)
    d = {}
    for line in out.splitlines():
        x, y, f = line.split("\t")
        d[f] = (int(x) if x != "-" else 0, int(y) if y != "-" else 0)
    return d


def klass(f):
    if f.startswith("tools/test_") or f == "bin/tests.sh":
        return "tests"
    if (f.startswith("starter-kit/") or f.startswith("workstreams/")
            or f in ("ITERATIVE_METHODOLOGY.md", "HOW_TO_USE.md", "FRAMEWORK_APPARATUS.md")):
        return "shipped (starter-kit, workstreams, the three manuals)"
    if f.startswith("bin/") or f.startswith("tools/"):
        return "canonical-only tools and fixtures"
    return "repository configuration and prose"


def table(title, d):
    c = collections.defaultdict(lambda: [0, 0, 0])
    for f, (a, r) in d.items():
        k = klass(f)
        c[k][0] += 1
        c[k][1] += a
        c[k][2] += r
    print("== %s: %d files, +%d -%d" % (title, len(d), sum(v[1] for v in c.values()), sum(v[2] for v in c.values())))
    for k in sorted(c):
        print("   %-58s files=%3d  +%6d -%5d" % (k, c[k][0], c[k][1], c[k][2]))


print("tip           %s" % git("rev-parse", "--short", "HEAD").strip())
print("upstream/main %s" % git("rev-parse", "--short", UP).strip())
print("plan base     %s (contains upstream/main: %s)" % (BASE, "yes" if subprocess.run(
    ["git", "merge-base", "--is-ancestor", UP, BASE]).returncode == 0 else "NO"))
print("commits upstream/main..HEAD: %s (merges %s); by ancestry, INFLATED by squash-merged pull requests" % (
    git("rev-list", "--count", UP + "..HEAD").strip(), git("rev-list", "--count", "--merges", UP + "..HEAD").strip()))
print("commits HEAD..upstream/main: %s" % git("rev-list", "--count", "HEAD.." + UP).strip())
print()

A = numstat(UP, BASE, LEDGER)
B = numstat(BASE, "HEAD", LEDGER)
T = numstat(UP, "HEAD", LEDGER)
table("before the methodology/ plan (upstream/main..%s)" % BASE, A)
table("from the plan on (%s..HEAD)" % BASE, B)
table("total (upstream/main..HEAD), ledgers and docs/ left out", T)
docs = git("diff", "--name-status", UP, "HEAD", "--", "docs").splitlines()
print("== docs/: %d paths differ (%d added, %d modified); fork-only planning and archives, never part of a pull request"
      % (len(docs), sum(1 for l in docs if l[0] == "A"), sum(1 for l in docs if l[0] != "A")))
print()
print("== files changed in BOTH halves (the second half builds on the first):")
for f in sorted(set(A) & set(B)):
    print("   %-46s before +%d-%d   from the plan on +%d-%d" % (f, A[f][0], A[f][1], B[f][0], B[f][1]))
print()

# A judgment, not a measurement: each file goes to the theme that dominates its diff. A file two themes share (the runner,
# the shell suite) is counted once, under the heading below that names it. The assert keeps the table complete.
THEMES = collections.OrderedDict([
    ("A  the methodology/ directory (resolver, migrate-layout, sync layers, hook, prose)", [
        "bin/_manifest.py", "bin/_manifest_reader.py", "bin/check-layout-literals", "bin/migrate-layout", "bin/sync",
        "bin/status", "bin/check-links", "bin/check-ledger", ".githooks/pre-commit", "tools/layout_resolver.py",
        "tools/layout_fixtures.py", "tools/test_layout_resolver.py", "tools/test_migrate_layout.py",
        "tools/test_sync_layouts.py", "tools/test_checker_layouts.py", "starter-kit/context_budget.py",
        "tools/test_context_budget.py", "starter-kit/CLAUDE_TEMPLATE.md", "starter-kit/BOOTSTRAP.md",
        "starter-kit/RECOMMENDED_SKILLS.md", "starter-kit/SAFEGUARDS.md", "ITERATIVE_METHODOLOGY.md", "HOW_TO_USE.md",
        "starter-kit/CHANGELOG.md", "workstreams/ARCHITECTURE_WORKSTREAM.md", "workstreams/AUDIT_WORKSTREAM.md",
        "workstreams/DEVELOPMENT_WORKSTREAM.md", "workstreams/INHERITED_CODEBASE_FAMILIARIZATION_CAMPAIGN.md",
        "workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_CAMPAIGN.md", "workstreams/TEMPLATE_CAMPAIGN.md",
        "workstreams/TEMPLATE_WORKSTREAM.md"]),
    ("B  the quality ratchet 1.1 to 1.5, and the seed that cites its run", [
        "starter-kit/quality_ratchet.py", "tools/test_quality_ratchet.py", "starter-kit/quality-gates.json",
        "starter-kit/HANDOFFS.md"]),
    ("C  the ledger trimmer 1.5 to 1.8", [
        "starter-kit/methodology_trim.py", "tools/test_methodology_trim.py", "tools/fixtures/trim-verify-template-1.7.0.sh",
        "tools/fixtures/handoff-ledger-2-records.md", "FRAMEWORK_APPARATUS.md"]),
    ("D  the dashboard 2.11 to 2.22 (and its twin)", [
        "starter-kit/methodology_dashboard.py", "tools/methodology_dashboard.py", "tools/test_methodology_dashboard.py"]),
    ("E  the close-out report generator (a new tool)", [
        "starter-kit/close_out_report.py", "tools/test_close_out_report.py"]),
    ("F  canonical-only checkers and reports (two of them new)", [
        "bin/check-handoff", "bin/check-overhead", "bin/model-report", "bin/check-learnings"]),
    ("S  the shell suite and the runner (shared by every theme)", ["bin/tests.sh", "starter-kit/SESSION_RUNNER.md"]),
    ("G  this repository's own configuration and prose (mostly stays)", [
        ".context-budget.json", ".gitignore", ".quality-gates.json", "CLAUDE.md", "README.md"]),
])
assigned = {f: t for t, fs in THEMES.items() for f in fs}
missing = sorted(set(T) - set(assigned))
assert not missing, "files with no theme: %s" % missing
stale = sorted(set(assigned) - set(T))
print("== by theme (tree diff upstream/main..HEAD, ledgers and docs/ left out; %d files)" % len(T))
for t, fs in THEMES.items():
    fs = [f for f in fs if f in T]
    new = [f for f in fs if subprocess.run(["git", "cat-file", "-e", "%s:%s" % (UP, f)], capture_output=True).returncode != 0]
    print("   %-84s files=%2d +%6d -%5d  new files: %d" % (t, len(fs), sum(T[f][0] for f in fs), sum(T[f][1] for f in fs), len(new)))
if stale:
    print("   (named but unchanged: %s)" % ", ".join(stale))
print()

spec = importlib.util.spec_from_file_location("m", "bin/_manifest.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
changed = set(git("diff", "--name-only", UP, "HEAD").split())
print("== adopter impact: DISTRIBUTION entries (%d) whose source differs upstream/main -> HEAD" % len(m.DISTRIBUTION))
for kind in ("tracked", "seed"):
    sel = [s for (s, d, k) in m.DISTRIBUTION if k == kind]
    ch = [s for s in sel if s in changed]
    print("   %s: %d of %d differ" % (kind, len(ch), len(sel)))
    for s in ch:
        a, r = git("diff", "--numstat", UP, "HEAD", "--", s).split()[:2]
        print("      %-60s +%s/-%s" % (s, a, r))
print()

print("== tool versions (upstream/main -> HEAD)")
PATS = {"starter-kit/quality_ratchet.py": r'^VERSION = "([^"]+)"',
        "starter-kit/methodology_dashboard.py": r'^DASHBOARD_VERSION = "([^"]+)"',
        "starter-kit/context_budget.py": r'^VERSION = "([^"]+)"',
        "starter-kit/methodology_trim.py": r'^TRIM_VERSION = "([^"]+)"',
        "starter-kit/close_out_report.py": r'^__version__ = "([^"]+)"'}
for f, pat in PATS.items():
    def ver(text):
        mm = re.search(pat, text, re.M)
        return mm.group(1) if mm else "(absent)"
    up = subprocess.run(["git", "show", "%s:%s" % (UP, f)], capture_output=True, text=True)
    print("   %-40s %-9s -> %s" % (f, ver(up.stdout) if up.returncode == 0 else "(no file)", ver(open(f).read())))
