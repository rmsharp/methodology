#!/usr/bin/env python3
"""BL-103 repair 3 (S307): how many receipts cite a gate run, and how many of those cite unmeasured gates.
Read-only. Run from the repository root:  python3 -I docs/planning/bl103-evidence/survey-citations.py
Part 1 reads this repository's live ledger and every archived shard. Part 2 reads the sibling projects under
~/Development (root, methodology/ and the three shard directories only: a recursive glob over a 3 GB tree is
how the first attempt hung)."""
import glob, json, os, re

FENCE = re.compile(r"^```handoff\n(.*?)^```$", re.S | re.M)
CITE = re.compile(r"quality_ratchet:\s*(\d+)/(\d+)\s+pass(?:\s*·\s*(\d+)\s+fail)?(?:\s*·\s*(\d+)\s+unmeasured)?")

def citations(paths):
    n, rows = 0, []
    for f in paths:
        try:
            t = open(f, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        for m in FENCE.finditer(t):
            n += 1
            sess = re.search(r"^session:\s*(\S+)", m.group(1), re.M)
            for a, b, fl, un in CITE.findall(m.group(1)):
                rows.append((os.path.basename(f), sess.group(1) if sess else "?", a, b, fl, un))
    return n, rows

files = list(dict.fromkeys(["HANDOFFS.md"] + sorted(glob.glob("docs/archive/*HANDOFFS*.md"))))
n, rows = citations(files)
print(f"this repository: {n} receipts in {len(files)} files, {len(rows)} citations of a gate run")
print("  unmeasured field:", {k: sum(1 for r in rows if (r[5] or "ABSENT") == k) for k in sorted({(r[5] or "ABSENT") for r in rows})})
print("  citations with unmeasured above 0:", [r for r in rows if r[5] not in ("", "0")])
print("  citations with fail above 0 (out of scope for repair 3):", len([r for r in rows if r[4] not in ("", "0")]))

home = os.path.expanduser("~/Development")
total = withgates = projects = 0
for d in sorted(os.listdir(home)):
    p = os.path.join(home, d)
    if not os.path.isdir(os.path.join(p, ".git")) or os.path.abspath(p) == os.getcwd():
        continue
    projects += 1
    gates = None
    for g in (".quality-gates.json", "methodology/.quality-gates.json"):
        gp = os.path.join(p, g)
        if os.path.isfile(gp):
            try:
                gates = len(json.load(open(gp)).get("gates", []))
            except ValueError:
                gates = "ERR"
    ledgers = [x for x in (os.path.join(p, "HANDOFFS.md"), os.path.join(p, "methodology", "HANDOFFS.md")) if os.path.isfile(x)]
    for sub in ("archive", "docs/archive", "methodology/archive"):
        ledgers += glob.glob(os.path.join(p, sub, "HANDOFFS-through-*.md"))
    nrec, rws = citations(ledgers)
    if gates:
        withgates += 1
    if gates is not None or rws:
        print(f"  {d}: gates={gates} receipts={nrec} citations={len(rws)} unmeasured>0={[r for r in rws if r[5] not in ('', '0')]}")
        total += len(rws)
print(f"sibling projects: {projects} scanned, {withgates} with declared gates, {total} citations")
