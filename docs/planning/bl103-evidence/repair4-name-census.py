#!/usr/bin/env python3
"""Census for BL-103 option (c) (S452): how many declared gate names fall outside the shape `bin/check-handoff` reads.

The lint reads a gate name as `[A-Za-z0-9][A-Za-z0-9_.-]*` (its `_GATE_NAME`, `bin/check-handoff`); `quality_ratchet.py`
accepts any non-empty string (`config_defects`). This reads every `.quality-gates.json` one level under ~/Development and
under each project's `methodology/`, never a recursive glob, and prints the counts. Read-only. At S452: 18 manifests,
67 gate names, 0 outside the shape. A count is a reading with a time on it: run this again instead of trusting that line.
    python3 -I docs/planning/bl103-evidence/repair4-name-census.py [development-directory]
"""
import glob
import json
import os
import re
import sys

root = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/Development")
shape = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
paths = sorted(glob.glob(os.path.join(root, "*", ".quality-gates.json"))
               + glob.glob(os.path.join(root, "*", "methodology", ".quality-gates.json")))
names, odd, unreadable = 0, [], []
for p in paths:
    try:
        cfg = json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError) as e:
        unreadable.append((p, str(e)))
        continue
    for g in cfg.get("gates", []):
        if isinstance(g, dict) and g.get("name"):
            names += 1
            if not shape.match(str(g["name"])):
                odd.append((os.path.relpath(p, root), g["name"]))
print(f"manifests read: {len(paths) - len(unreadable)}  unreadable: {len(unreadable)}  gate names: {names}  outside the lint's shape: {len(odd)}")
for item in odd + unreadable:
    print("  ", item)
