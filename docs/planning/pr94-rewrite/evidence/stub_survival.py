"""Scratch experiment: for each failing shard, does the pre-trim stub's text survive into the finalized record?

For each shard it takes the trim commit T (the commit that added the shard), reads the ledger at T^ (before)
and at T (after), finds the record that the re-derived proof reports as MISSING (the stub) and the record
with the same identifying line in the after ledger (its successor), and lists the stub's non-blank lines that
do NOT occur as a whole line in the successor.

usage: stub_survival.py REPO_DIR SWEEP_DIR   (SWEEP_DIR holds <shard>.after.txt files from a --reverify sweep)
Read-only: runs `git log` and `git show` only.
"""
import re
import subprocess
import sys
from pathlib import Path

repo, sweep = Path(sys.argv[1]), Path(sys.argv[2])


def git(*args):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    return r.stdout


SN_START = re.compile(r"^### (?:Session \d+ Handoff Evaluation \(by Session \d+\)|What Session \d+ Did\b)")


def records(ledger, text):
    lines = text.split("\n")
    if ledger == "SESSION_NOTES.md":
        idx = [i for i, l in enumerate(lines) if SN_START.match(l)]
        return ["\n".join(lines[a:b]) for a, b in zip(idx, idx[1:] + [len(lines)])]
    # HANDOFFS.md: fenced ```handoff blocks
    out, i = [], 0
    while i < len(lines):
        if lines[i].startswith("```handoff"):
            j = i + 1
            while j < len(lines) and lines[j] != "```":
                j += 1
            out.append("\n".join(lines[i:j + 1]))
            i = j + 1
        else:
            i += 1
    return out


def anchor(ledger, rec):
    if ledger == "SESSION_NOTES.md":
        return rec.split("\n", 1)[0].strip()
    m = re.search(r"(?m)^session: .*$", rec)
    return m.group(0).strip() if m else ""


rows = []
for f in sorted(sweep.glob("*.after.txt")):
    txt = f.read_text()
    m = re.search(r"MISSING:\s*(.+)", txt)
    if not m:
        continue                                   # nothing missing: a passing shard
    shard = f.name[:-len(".after.txt")]
    ledger = shard.split("-through-")[0] + ".md"
    T = git("log", "--diff-filter=A", "-1", "--format=%H", "--", "docs/archive/" + shard).strip()
    before = git("show", T + "^:" + ledger)
    after = git("show", T + ":" + ledger)
    miss = m.group(1).strip()
    stub = next((r for r in records(ledger, before) if anchor(ledger, r).startswith(miss[:60])), None)
    succ = next((r for r in records(ledger, after) if anchor(ledger, r).startswith(miss[:60])), None)
    if stub is None or succ is None:
        rows.append((shard, T[:7], "COULD NOT LOCATE stub=%s successor=%s" % (stub is not None, succ is not None), []))
        continue
    succ_lines = set(l.rstrip() for l in succ.split("\n"))
    stub_lines = [l.rstrip() for l in stub.split("\n") if l.strip()]
    absent = [l for l in stub_lines if l not in succ_lines]
    rows.append((shard, T[:7], "%d stub lines, %d absent from the successor" % (len(stub_lines), len(absent)), absent))

for shard, t, summary, absent in rows:
    print("%-40s T=%s  %s" % (shard, t, summary))
    for l in absent[:8]:
        print("      absent:", l[:150])
    if len(absent) > 8:
        print("      ... %d more" % (len(absent) - 8))
