"""For each adopter's live SESSION_NOTES.md (at its root or under methodology/): every record that still
carries the Phase 1B status line, its position, and whether it also carries the `(IN PROGRESS)` tag.

usage: adopter_claim_lines.py DIR [DIR ...]      (each DIR a project root). Read-only."""
import re, sys
from pathlib import Path
START = re.compile(r"^### (?:Session \d+ Handoff Evaluation \(by Session \d+\)|What Session \d+ Did\b)")
LINE = re.compile(r"^\*\*Status:\*\* Session claimed\b.*$", re.M)
print("project\trunner_records\trecord_index\theading\tin_progress_tag\tbytes")
for d in sys.argv[1:]:
    f = Path(d) / "SESSION_NOTES.md"
    if not f.is_file():
        f = Path(d) / "methodology" / "SESSION_NOTES.md"
    if not f.is_file():
        continue
    lines = f.read_text(encoding="utf-8", errors="replace").split("\n")
    idx = [i for i, l in enumerate(lines) if START.match(l)]
    recs = ["\n".join(lines[a:b]) for a, b in zip(idx, idx[1:] + [len(lines)])]
    hits = [(k, r) for k, r in enumerate(recs) if LINE.search(r)]
    if not hits:
        print("%s\t%d\t-\t-\t-\t-" % (Path(d).name, len(recs)))
    for k, r in hits:
        print("%s\t%d\t%d\t%s\t%s\t%d" % (Path(d).name, len(recs), k, r.split("\n", 1)[0][:40],
                                          "(IN PROGRESS)" in r, len(r.encode())))
