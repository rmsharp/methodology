#!/usr/bin/env python3
"""Which rows of the BL-101 findings register are still open, and which of those the tool's own checks did not see (S308).

Run from anywhere inside the repository:  python3 -I docs/planning/pr-composition-evidence/register-open-rows.py

The plan's section 7.6 says the pull request "carries the register and waits while such a row is open, unless he waives it
and the ledger says so", where "such a row" is a finding the tool's checks did not see. The register's table rows are not
rewritten when a disposition changes: a dated line under the table says so. So this reads the table, then applies the dated
lines of the form "- **YYYY-MM-DD (S###), F##: fixed|declined" over it. Anything else it prints as the row says it.

It does NOT decide what "did not see" means; it prints each open row's Seen cell and a first-pass reading, for a person to
judge. The first-pass reading is a plain substring test and is labelled as such.
"""
import os
import re
import subprocess

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
PATH = os.path.join(ROOT, "docs/planning/methodology-subdirectory-evidence/findings-register.md")
text = open(PATH, encoding="utf-8").read()

rows = {}
for line in text.splitlines():
    m = re.match(r"\| (F\d+) \|", line)
    if not m:
        continue
    cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
    rows[m.group(1)] = {"phase": cells[1], "seen": cells[3], "disp": cells[-1]}

override = {}
for line in text.splitlines():
    m = re.match(r"- \*\*(\d{4}-\d\d-\d\d) \(S(\d+)\), (F\d+)[^*]*?: (fixed|declined)", line)
    if m:
        override[m.group(3)] = (m.group(4), m.group(1), "S" + m.group(2))


def state(fid):
    if fid in override:
        return override[fid][0] + " (dated line %s, %s)" % (override[fid][1], override[fid][2])
    d = rows[fid]["disp"].lower()
    for word in ("fixed", "declined"):
        if d.startswith("**" + word) or d.startswith("**" + word + " "):
            return word
    return "open" if "**open**" in d else "?"


def first_pass(seen):
    s = seen.lower()
    if s.startswith("**no**") or s == "no" or "no (" in s[:6] or s.startswith("not stated"):
        return "NOT SEEN"
    if ", and false" in s or "no check" in s:
        return "not seen (its own warning is false / no check reads it)"
    if re.search(r"\bno\b", s) and "yes" not in s:
        return "probably not seen"
    return "seen, at least in part"


print("%d rows; %d carry a dated change of disposition" % (len(rows), len(override)))
print()
n_open = 0
for fid in sorted(rows, key=lambda x: int(x[1:])):
    st = state(fid)
    if not st.startswith("open"):
        continue
    n_open += 1
    r = rows[fid]
    print("%-4s %-28s %s" % (fid, r["phase"][:28], first_pass(r["seen"])))
    print("       Seen: %s" % r["seen"][:150])
    print("       Disposition: %s" % r["disp"][:200])
print()
print("%d open of %d; fixed or declined: %s" % (
    n_open, len(rows), ", ".join("%s %s" % (f, state(f).split(" ")[0]) for f in sorted(rows, key=lambda x: int(x[1:])) if not state(f).startswith("open"))))
