#!/usr/bin/env python3
"""How many relative links in the DISTRIBUTED markdown files change if every adopter-layout file
moves into one flat methodology/ directory (workstreams/ stays a subdirectory)?

The distributed files author their links for TODAY'S adopter layout (bin/check-links, B1 plan
section 4): the starter-kit root-files at the project root, the framework under docs/methodology/.
This script reads bin/_manifest.py (as data), resolves every relative markdown link of every
distributed .md file in that layout, moves every manifest destination into methodology/, and counts
the links whose text must change to stay correct. Read-only. Run from the repo root:

    python3 -I docs/planning/methodology-subdirectory-evidence/link-simulation.py
"""
import collections
import importlib.util
import posixpath
import re
import sys

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("m", "bin/_manifest.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
D = m.DISTRIBUTION
old_dests = {dest for _s, dest, _d in D}


def new_of(dest):
    if dest.startswith("docs/methodology/"):
        return "methodology/" + dest[len("docs/methodology/"):]
    return "methodology/" + dest        # every root file, dotfiles included, lands in methodology/


LINK = re.compile(r"\]\(([^)\s]+)\)")
SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.\-]*:")
rows = []
tot_links = 0
for src, dest, disp in D:
    if not dest.endswith(".md"):
        continue
    txt = open(src, encoding="utf-8").read().splitlines()
    inside = False
    changed = {"dist->dist": 0, "dist->project": 0}
    links = 0
    ndest = new_of(dest)
    odir = posixpath.dirname(dest)
    ndir = posixpath.dirname(ndest)
    for ln in txt:
        if ln.lstrip().startswith("```"):
            inside = not inside
            continue
        if inside:
            continue
        for mm in LINK.finditer(ln):
            path = mm.group(1).split("#")[0]
            if not path or SCHEME.match(path) or path.startswith("/"):
                continue
            links += 1
            tgt_old = posixpath.normpath(posixpath.join(odir, path))
            tgt_new = new_of(tgt_old) if tgt_old in old_dests else tgt_old
            newrel = posixpath.relpath(tgt_new, ndir or ".")
            if newrel != posixpath.normpath(path.rstrip("/")):
                changed["dist->dist" if tgt_old in old_dests else "dist->project"] += 1
    tot_links += links
    rows.append((dest, links, changed["dist->dist"], changed["dist->project"]))
dd = sum(r[2] for r in rows)
dp = sum(r[3] for r in rows)
print(f"distributed markdown files with links: {sum(1 for r in rows if r[1])} of {len(rows)}; relative links: {tot_links}")
print(f"links that must change under a flat methodology/ layout: {dd + dp}  "
      f"(distributed->distributed {dd}; distributed->project-owned {dp}); unchanged: {tot_links - dd - dp}")
print()
for dest, links, a, b in sorted(rows, key=lambda r: -(r[2] + r[3])):
    if a + b:
        print(f"  {a + b:4d} of {links:4d}  (dd {a:3d}, dp {b:3d})  {dest}")
