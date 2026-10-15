#!/usr/bin/env python3
"""Backstop for layer6c-build.py's classification: does every `reference` hunk differ from the candidate's text ONLY by
link syntax and paths?

    python3 layer6c-reference-check.py <source-repo> <source-rev> <candidate-repo> <candidate-rev>

The builder classes a hunk `reference` by a rule (it removes a relative markdown link or a `docs/methodology/` path and
does not put it back). A rule can pass a hunk that also changes a word. This script normalises both sides of each
`reference` hunk (a relative link keeps its text, `docs/methodology/` and `../` and backticks and the section sign go) and
prints every hunk whose two sides still differ. A flagged hunk is read by hand: the expected ones are the three whose link
TARGET named a file (`FRAMEWORK_APPARATUS.md#the-action-ledger`) and whose replacement names the file in a code span.
Read-only: git only.
"""
import importlib.util
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True   # the import below must not leave a __pycache__ in the evidence directory
spec =importlib.util.spec_from_file_location("layer6c_build", Path(__file__).with_name("layer6c-build.py"))
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


def norm(t):
    t = re.sub(r"\[([^\]]*)\]\((?!https?://)[^)\s]*\)", r"\1", t)   # a relative link keeps its text
    t = t.replace("docs/methodology/", "").replace("`", "").replace("§", "")
    t = re.sub(r"\.\./", "", t)
    return re.sub(r"\s+", " ", t).strip()


def main():
    src, rev, cand, cand_rev = sys.argv[1:5]
    flagged = total = 0
    for rel in b.documents(src, rev):
        old, new = b.show(cand, cand_rev, rel), b.show(src, rev, rel)
        if old == new:
            continue
        layout, _ = b.partition(rel, old, new)
        for h, cls in layout:
            if cls != "reference":
                continue
            total += 1
            if norm(h.removed_text()) != norm(h.added_text()):
                flagged += 1
                print("differs after normalising: %s @%d\n   - %s\n   + %s" % (rel, h.old_start, norm(h.removed_text())[:200], norm(h.added_text())[:200]))
    print("reference hunks: %d, equal after normalising: %d, flagged: %d" % (total, total - flagged, flagged))


if __name__ == "__main__":
    main()
