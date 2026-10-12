#!/usr/bin/env python3
"""BL-105 rehearsal (S302): the markdown links to PROJECT_LEARNINGS.md in a checkout, by where each one now points.

  bl105-links.py <checkout> [<checkout> ...]

`bin/check-links --tree` read the same project-link count before and after the move in every arm, so it does not see a
link from the project's own documents to the moved file. This reads every tracked `.md`/`.Rmd`/`.qmd`, takes each
`](target)` whose target names the file, resolves it against the directory of the file that holds it, and says where it
lands: `root` (the file's old place) or `methodology` (its new one), and whether a file is there. A link to `root` with no
file there dangles because of the move; a link to `methodology` that exists is healed or correct. A ledger is a file whose
name is CHANGELOG / HANDOFFS / SESSION_NOTES (or a trimmed shard of one): a committed entry is never edited (plan C6).
"""
import os
import posixpath
import re
import subprocess
import sys

LINK = re.compile(r"\]\(([^)\s]*PROJECT_LEARNINGS\.md)(?:#[^)]*)?\)")
NAME = "PROJECT_LEARNINGS.md"
LEDGER = re.compile(r"(^|/)(CHANGELOG|HANDOFFS|SESSION_NOTES)(-through-[^/]*)?\.md$")


def tracked_docs(root):
    out = subprocess.run(["git", "-C", root, "ls-files", "-z", "--", "*.md", "*.Rmd", "*.qmd"],
                         capture_output=True, text=True).stdout
    return [p for p in out.split("\0") if p]


def measure(root):
    rows = {}
    for rel in tracked_docs(root):
        try:
            text = open(os.path.join(root, rel), encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        for m in LINK.finditer(text):
            target = m.group(1)
            if "://" in target:
                continue
            landed = posixpath.normpath(posixpath.join(posixpath.dirname(rel), target))
            if landed == NAME:
                where = "root"
            elif landed == "methodology/" + NAME:
                where = "methodology"
            else:
                where = "elsewhere"
            exists = os.path.isfile(os.path.join(root, landed))
            kind = "ledger" if LEDGER.search(rel) else ("CLAUDE.md" if rel == "CLAUDE.md" else "live")
            key = (where, exists, kind)
            rows.setdefault(key, []).append(rel)
    return rows


def main(argv):
    for root in argv[1:]:
        rows = measure(root)
        total = sum(len(v) for v in rows.values())
        dangling = sum(len(v) for (w, e, _k), v in rows.items() if not e)
        print("%s: %d link(s) to the file, %d dangling" % (os.path.basename(root.rstrip("/")), total, dangling))
        for (where, exists, kind), files in sorted(rows.items()):
            print("   lands at %-11s file there: %-5s in a %-9s file: %3d link(s) in %d file(s)" % (
                where, exists, kind, len(files), len(set(files))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
