#!/usr/bin/env python3
"""PR4: which of the maintainer's own lines does the candidate remove, and why?

For every file the candidate changes that upstream already has: the lines of UPSTREAM's copy that the candidate's
diff removes or rewrites (git diff -U0, old side), each attributed by `git blame` at the upstream commit to the
author of the line. A removed line written by the maintainer is sorted into four tiers against the candidate's copy
of the same file:

  moved  the exact stripped line is still in the file
  noted  a line of the candidate is that line followed only by a `#` comment
  kept   its words (whitespace collapsed) still appear in the candidate's text, inside a longer or re-wrapped line
  gone   none of these

Every GONE line is then assigned to a named reason by its file and its line number in upstream's copy (BUCKETS and
RANGES below: a judgment, written out so it can be disputed one range at a time). A gone line with no reason makes
the script exit 1. The last part lists the tests of upstream's test files that the candidate no longer has, by name.
Reads git objects only; writes nothing in the repository.

  python3 pr4-survive.py <repo> <start> <upstream> <candidate> <maintainer-regex> [--detail]

<start> is the copy the work began with (c8b9ddd): the script reports how many upstream commits there are that it
does not contain (0 when <upstream> is an ancestor of <start>, so the maintainer has changed nothing since).
"""
import re
import subprocess
import sys
from collections import Counter, OrderedDict

repo, start, up, cand, who = sys.argv[1:6]
detail = "--detail" in sys.argv[6:]
WHO = re.compile(who, re.I)

# reason -> (what it is, where the pull request's text says so)
BUCKETS = OrderedDict([
    ("layout", ("the methodology/ directory work: files found through the layout resolver, names held in constants, "
                "messages and prose reworded for either layout", "decision 1; 'What a project sees'; the commit list")),
    ("sync", ("(a) the dashboard's --sync [DIR], the --force gate on tracked or brand-new targets, the stale-copy "
              "remedy, and the help and messages that carry them", "decision 2 (a)")),
    ("excl", ("(b) 'methodology' is no longer in EXCLUDE_DIRS", "decision 2 (b)")),
    ("table", ("(c) installed-source recognition is one table; the name list is derived from it", "decision 2 (c)")),
    ("tests_e", ("(e) the four tests removed", "decision 2 (e)")),
    ("version", ("a version constant, the pin on it, or the re-recorded bytes-per-token", "decision 2; decision 4")),
    ("timeout", ("the quality ratchet's timeout_seconds (commit c8c0b21)", "the c8c0b21 bullet")),
    ("firstcommit", ("first_commit_date reads the root commits", "the bbe0dc3 bullet")),
    ("thresholds", ("gate thresholds raised (all five are min gates, so a tightening)",
                    "in part: the bbe0dc3 bullet says three; the other two are raised by later commits")),
    ("testsh", ("bin/tests.sh: the executable bit derived from the manifest; the skip count in the summary",
                "the bbe0dc3 bullet")),
    ("handoffs_rule", ("starter-kit/HANDOFFS.md: a run with unmeasured gates must be repaired or named", "the 5afc962 bullet")),
    ("runner_table", ("starter-kit/SESSION_RUNNER.md: the workstream paths in the task table made relative to the runner",
                      "in part: the text names the first paragraph only")),
    ("firstparent", ("the dashboard's gate-manifest history walk reads the first-parent line (2.21.0)",
                     "NOT ITEMISED: decision 2 says the other changes in bbe0dc3 are not itemised")),
])
DASH = [(44, 45, "excl"), (86, 86, "version"), (89, 89, "excl"), (363, 574, "table"), (652, 749, "sync"),
        (841, 844, "firstcommit"), (1091, 1091, "layout"), (1520, 1521, "layout"), (2013, 2015, "firstparent"),
        (2019, 2069, "layout"), (2091, 2091, "firstparent"), (3640, 3654, "sync"), (3661, 3737, "layout")]
RANGES = {
    "tools/methodology_dashboard.py": DASH,
    "starter-kit/methodology_dashboard.py": DASH,
    "tools/test_methodology_dashboard.py": [(2404, 2407, "version"), (2410, 2482, "tests_e")],
    "starter-kit/quality_ratchet.py": [(19, 21, "timeout"), (50, 52, "version"), (63, 67, "timeout"), (73, 77, "layout"),
                                       (148, 159, "layout"), (180, 180, "timeout"), (202, 202, "timeout"),
                                       (209, 244, "layout"), (266, 303, "timeout"), (338, 338, "layout"),
                                       (369, 369, "layout"), (390, 400, "layout"), (421, 495, "layout"),
                                       (536, 544, "layout"), (572, 576, "layout")],
    "starter-kit/context_budget.py": [(42, 44, "version"), (323, 1368, "layout")],
    ".context-budget.json": [(50, 52, "version")],
    ".githooks/pre-commit": [(1, 400, "layout")],
    ".quality-gates.json": [(1, 400, "thresholds")],
    "starter-kit/quality-gates.json": [(6, 6, "timeout")],
    "bin/check-ledger": [(1, 400, "layout")], "bin/status": [(1, 400, "layout")], "bin/sync": [(1, 500, "layout")],
    "bin/_manifest.py": [(1, 400, "layout")], "bin/_manifest_reader.py": [(1, 400, "layout")],
    "bin/check-handoff": [(1, 600, "layout")],
    "bin/tests.sh": [(29, 29, "testsh"), (921, 923, "layout"), (1422, 1422, "testsh")],
    "HOW_TO_USE.md": [(1, 2000, "layout")], "starter-kit/BOOTSTRAP.md": [(1, 2000, "layout")],
    "starter-kit/RECOMMENDED_SKILLS.md": [(1, 2000, "layout")],
    "starter-kit/HANDOFFS.md": [(184, 184, "handoffs_rule")],
    "starter-kit/SESSION_RUNNER.md": [(61, 76, "runner_table")],
    "tools/test_quality_ratchet.py": [(448, 448, "layout")],
}


def git(*a, check=True):
    r = subprocess.run(["git", "-C", repo, *a], capture_output=True)
    if check and r.returncode:
        sys.exit("git %s failed: %s" % (" ".join(a), r.stderr.decode("utf-8", "replace")[:200]))
    return r.stdout.decode("utf-8", "replace")


def bucket_of(f, n):
    for lo, hi, b in RANGES.get(f, []):
        if lo <= n <= hi:
            return b
    return None


anc = subprocess.run(["git", "-C", repo, "merge-base", "--is-ancestor", up, start]).returncode == 0
since = git("rev-list", "--count", "%s..%s" % (start, up)).strip()
sh = lambda r: git("rev-parse", "--short=12", r).strip()
print("start %s; upstream %s; candidate %s" % (sh(start), sh(up), sh(cand)))
print("upstream is an ancestor of the start copy: %s; upstream commits the start copy lacks: %s" % (anc, since))
print("candidate over upstream: %s commits; %s" % (git("rev-list", "--count", "%s..%s" % (up, cand)).strip(),
                                                    git("diff", "--shortstat", up, cand).strip()))
print("maintainer = author matching /%s/i" % who)

names = OrderedDict()
for line in git("diff", "--name-status", "--no-renames", up, cand).splitlines():
    st, f = line.split("\t", 1)
    names[f] = st

# a file whose two blobs are identical to its twin's is counted once in the unique totals
twin_of = {}
for a, b in (("tools/methodology_dashboard.py", "starter-kit/methodology_dashboard.py"),):
    if all(git("rev-parse", "%s:%s" % (r, p)).strip() == git("rev-parse", "%s:%s" % (r, a)).strip()
           for r in (up, cand) for p in (b,)):
        twin_of[b] = a

rows, tot, utot, bt, ubt, unbucketed, gone_detail = [], Counter(), Counter(), Counter(), Counter(), [], []
for f, st in names.items():
    if st == "A":
        continue
    old = git("show", "%s:%s" % (up, f), check=False).splitlines()
    new = git("show", "%s:%s" % (cand, f), check=False).splitlines() if st != "D" else []
    newset = {l.strip() for l in new}
    newflat = " ".join(" ".join(new).split())
    noted = set()
    for l in new:
        m = re.match(r"^(.*?\S)\s+#.*$", l.strip())
        if m:
            noted.add(m.group(1))
    author, cur, cmap = {}, None, {}
    for l in git("blame", "--porcelain", up, "--", f).splitlines():
        m = re.match(r"^([0-9a-f]{40}) \d+ (\d+)(?: \d+)?$", l)
        if m:
            cur = m.group(1)
            author[int(m.group(2))] = cur
        elif l.startswith("author ") and cur and cur not in cmap:
            cmap[cur] = l[7:]
    removed, hunks = [], []
    if st == "D":
        hunks.append((1, len(old), []))
        removed = [(i + 1, t, 0) for i, t in enumerate(old)]
    else:
        h = -1
        for l in git("diff", "-U0", "--no-renames", up, cand, "--", f).splitlines():
            m = re.match(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", l)
            if m:
                h += 1
                a, b = int(m.group(1)), int(m.group(2)) if m.group(2) is not None else 1
                hunks.append((a, b, []))
                removed += [(a + i, old[a + i - 1], h) for i in range(b)]
            elif l.startswith("+") and not l.startswith("+++") and h >= 0:
                hunks[h][2].append(l[1:])
    mine = [x for x in removed if WHO.search(cmap.get(author.get(x[0]), ""))]
    mine_nb = [x for x in mine if x[1].strip()]
    moved = [x for x in mine_nb if x[1].strip() in newset]
    rest = [x for x in mine_nb if x[1].strip() not in newset]
    notd = [x for x in rest if x[1].strip() in noted]
    rest = [x for x in rest if x[1].strip() not in noted]
    kept = [x for x in rest if " ".join(x[1].split()) in newflat]
    gone = [x for x in rest if " ".join(x[1].split()) not in newflat]
    twin = f in twin_of
    for n, t, h in gone:
        b = bucket_of(f, n)
        if b is None:
            unbucketed.append((f, n, t))
        else:
            bt[b] += 1
            if not twin:
                ubt[b] += 1
    rows.append((f + ("  (twin of " + twin_of[f] + ")" if twin else ""), st, len(old), len(removed), len(mine),
                 len(mine_nb), len(moved), len(notd), len(kept), len(gone)))
    for key, v in (("removed", len(removed)), ("mine", len(mine)), ("mine_nb", len(mine_nb)), ("moved", len(moved)),
                   ("noted", len(notd)), ("kept", len(kept)), ("gone", len(gone))):
        tot[key] += v
        if not twin:
            utot[key] += v
    if detail:
        by_h = OrderedDict()
        for n, t, h in gone:
            by_h.setdefault(h, []).append((n, t))
        for h, ls in by_h.items():
            a, b, plus = hunks[h]
            gone_detail.append("== %s  old lines %d-%d [%s]: %d of his lines gone; the candidate writes %d there" % (
                f, a, a + b - 1, bucket_of(f, ls[0][0]) or "NO REASON", len(ls), len(plus)))
            gone_detail += ["   - %5d | %s" % (n, t.rstrip()[:150]) for n, t in ls]
            gone_detail += ["   + %5s | %s" % ("", t.rstrip()[:150]) for t in plus[:10]]

print()
print("%-76s %2s %6s %7s %5s %6s %6s %6s %6s %6s" % ("file (the candidate changes it)", "", "lines", "removed", "his",
                                                    "his,nb", "moved", "noted", "kept", "gone"))
for f, st, n, r, m, mnb, mv, nt, kp, gn in rows:
    if r:
        print("%-76s %2s %6d %7d %5d %6d %6d %6d %6d %6d" % (f[:76], st, n, r, m, mnb, mv, nt, kp, gn))
print("-" * 118)
print("%-76s %2s %6s %7d %5d %6d %6d %6d %6d %6d" % ("TOTAL, both copies of the dashboard counted", "", "", tot["removed"],
      tot["mine"], tot["mine_nb"], tot["moved"], tot["noted"], tot["kept"], tot["gone"]))
print("%-76s %2s %6s %7d %5d %6d %6d %6d %6d %6d" % ("TOTAL, the twin counted once", "", "", utot["removed"],
      utot["mine"], utot["mine_nb"], utot["moved"], utot["noted"], utot["kept"], utot["gone"]))
m = re.search(r"(\d+) deletions?\(-\)", git("diff", "--shortstat", up, cand))
print("removed = lines of upstream's copy the candidate's diff removes or rewrites; its total (%d) %s git's own deletion count (%s)." % (
      tot["removed"], "equals" if m and int(m.group(1)) == tot["removed"] else "DOES NOT EQUAL", m.group(1) if m else "?"))
print("his = of those, written by the maintainer (blame at upstream); his,nb = non-blank; moved / noted / kept / gone as above.")

print()
print("THE REASON FOR EACH GONE LINE (the twin counted once; the range table is in this script)")
print("%-13s %5s  %s" % ("reason", "lines", "what it is  --  where the text says so"))
for k, (what, told) in BUCKETS.items():
    if ubt[k]:
        print("%-13s %5d  %s  --  %s" % (k, ubt[k], what, told))
print("%-13s %5d" % ("(no reason)", len(unbucketed)))
for f, n, t in unbucketed:
    print("      NO REASON %s:%d | %s" % (f, n, t.strip()[:120]))

print()
print("TESTS OF UPSTREAM'S TEST FILES THAT THE CANDIDATE NO LONGER HAS (by test name; a renamed class is not a loss)")
files = [f for f in git("ls-tree", "-r", "--name-only", up).split() if re.search(r"(^|/)test_[^/]*\.py$", f)]
n_up = n_gone = 0
for f in files:
    def count(ref):
        c = Counter()
        for l in git("show", "%s:%s" % (ref, f), check=False).splitlines():
            m = re.match(r"\s+def (test\w*)\(", l)
            if m:
                c[m.group(1)] += 1
        return c
    u, c = count(up), count(cand)
    lost = sorted(k for k in u if c[k] < u[k])
    n_up += sum(u.values())
    n_gone += len(lost)
    print("  %-42s %4d tests, %d absent in the candidate%s" % (f, sum(u.values()), len(lost), ": " + ", ".join(lost) if lost else ""))
print("  %-42s %4d tests, %d absent" % ("TOTAL", n_up, n_gone))

if detail:
    print()
    print("\n".join(gone_detail))
sys.exit(1 if unbucketed else 0)
