#!/bin/bash
# Evidence [E1] for docs/planning/ratchet-kept-output-plan.md: the five recorded gate reds whose failing
# assertion was lost because the ratchet keeps no output. Each row is found by SEARCHING the named file for
# a phrase plus a second token that must be on the same line, so a ledger that grows at its top (new entries
# are prepended) does not make a stored line number wrong. Prints the line number found and the words around
# the phrase. Read-only. Run from the repository root.
python3 - <<'PY'
rows = [
 # tag, file, phrase, a second token the same line must also hold
 ("S192 2026-09-18", "docs/archive/CHANGELOG-through-2026-09-19.md", "one unnamed failure", "4c96234"),
 ("S233 2026-09-28", "docs/planning/BACKLOG-DETAIL.md", "read **361 passed", "5d6fbe4"),
 ("S257 2026-10-04", "docs/archive/CHANGELOG-through-2026-10-04.md", "not attributed to a named test", "f5d6d4f"),
 ("S384 2026-10-27", "docs/planning/BACKLOG.md", "S384 (2026-10-27)", "9507e0f6"),
 ("S430 2026-11-07", "CHANGELOG.md", "which test failed is unknown", "52adbb9f"),
]
for tag, path, phrase, also in rows:
    hit = None
    for no, line in enumerate(open(path, encoding="utf-8").read().split("\n"), 1):
        if phrase in line and also in line:
            hit = (no, line); break
    if hit is None:
        print(f"{tag}: {path}: NOT FOUND ({phrase!r} with {also!r})"); continue
    no, line = hit
    i = line.find(phrase)
    a, b = max(0, i - 170), min(len(line), i + len(phrase) + 230)
    print(f"{tag}: {path}:{no}\n    ...{line[a:b]}...\n")
PY
