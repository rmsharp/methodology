#!/usr/bin/env python3
"""BL-91 evidence: per-session PROCESS vs WORK lines, bucketed by session claim commit.

    python3 docs/planning/bl91-overhead-measurement/process-vs-work-per-session.py

Every commit between one `S<N> claim` commit and the next is attributed to that session, and
its added lines are split into ledger/process files and everything else.

LIMITS: `S<N> claim` as a commit subject is a recent convention, so the series only means
anything from S201 on -- earlier, one bucket swallows hundreds of commits and must be
discarded, not reported. Lines are a crude unit: a trim session writes a ~16 KB proof and
dominates its bucket (quote medians, never means), and a refactor that deletes code scores
zero work. The file classifier below is this repository's; an adopter's process files differ.
"""
import subprocess, re
def sh(*a): return subprocess.run(["git"]+list(a), capture_output=True, text=True, check=True).stdout
log = sh("log", "--reverse", "--format=%H\t%ad\t%s", "--date=short", "main").splitlines()
claims = [(i, l.split("\t")) for i, l in enumerate(log) if re.search(r"\bS(\d+)'? claim\b", l.split("\t")[2])]
def is_ledger(p):
    return (p in ("CHANGELOG.md", "HANDOFFS.md", "docs/HANDOFFS_ARCHIVE_INDEX.md",
                  "docs/FORK_LEARNINGS.md", "starter-kit/FRAMEWORK_LEARNINGS.md", "SESSION_NOTES.md")
            or p.startswith("docs/archive/") or p.endswith(".jsonl")
            or re.match(r"docs/planning/BACKLOG", p))
print(f"{'session':>8} {'date':>11} {'commits':>8} {'ledger+':>9} {'work+':>8} {'ledger share':>13}")
tot = []
for k, (idx, (h, d, s)) in enumerate(claims):
    n = re.search(r"\bS(\d+)'? claim\b", s).group(1)
    end = claims[k+1][0] if k+1 < len(claims) else len(log)
    shas = [log[j].split("\t")[0] for j in range(idx, end)]
    led = work = 0
    for sha in shas:
        for line in sh("show", "--numstat", "--format=", sha).splitlines():
            p = line.split("\t")
            if len(p) == 3 and p[0].isdigit():
                (led := led) if False else None
                if is_ledger(p[2]): led += int(p[0])
                else: work += int(p[0])
    share = led/(led+work)*100 if led+work else 0
    tot.append((int(n), d, len(shas), led, work, share))
    print(f"{'S'+n:>8} {d:>11} {len(shas):>8} {led:>9,} {work:>8,} {share:>12.0f}%")
import statistics as st
early = tot[:11]; late = tot[-11:]
for lab, g in (("first 11 sessions", early), ("last 11 sessions", late)):
    print(f"\n{lab}: median commits/session {st.median(x[2] for x in g):.0f}, "
          f"median ledger+ {st.median(x[3] for x in g):,.0f} lines, "
          f"median work+ {st.median(x[4] for x in g):,.0f} lines, "
          f"median ledger share {st.median(x[5] for x in g):.0f}%")
