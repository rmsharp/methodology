#!/usr/bin/env python3
"""PR2b layer 22: the edits that make commit 26' (S394). Writes ONLY the two files named below, in the repository you name.

Usage:  python3 -I pr2b-layer22-26prime-edits.py <repo directory>      (run in the scratch build clone, at the tip after series commit 25)

Why a new commit and not a replay of series commit 26 (2276f4ef): the tip's trimmer is upstream's 1.8.2 plus the fork's layout hunks, labelled 1.9.0,
and the commit was made against the old candidate's trimmer text; replayed it conflicts in five regions (pr2b-grouping-measure-output.txt:94-99).
The target is the 17 lines scrub-derive.py lists at the tip (pr2b-grouping-derive-after-output.txt), all comments, trailing comments and
docstrings. The rules are the old scrub's (scrub-record.md section 3): only fork tokens go; a sentence meaningful only inside the fork is deleted,
not reworded. The 17th line, tools/test_methodology_trim.py:4622 ("no P1 finding"), is left on purpose: P1 is the trimmer's own finding code
(commit 26's message: 'The trimmer's own "P1" check and every string it emits are untouched').

Every old string must occur exactly once, or nothing is written. Whether a token stream changed is NOT decided here: scrub-proof.py decides that.
"""
import os
import sys

sys.dont_write_bytecode = True

TRIM = "starter-kit/methodology_trim.py"
TEST = "tools/test_methodology_trim.py"

EDITS = [
    # ---- the trimmer: 12 flagged lines (13 changed lines, since the last one spans two) ----
    (TRIM,
     'TRIM_VERSION = "1.9.0"   # 1.9.0: BL-101 P3 (the methodology/ directory plan, section 7.2, coupling C7) -- a ledger\n',
     'TRIM_VERSION = "1.9.0"   # 1.9.0: a ledger\n'),
    (TRIM,
     '                         # ledger under methodology/ writes methodology/archive/ (decision D5) and climbs one\n',
     '                         # ledger under methodology/ writes methodology/archive/ and climbs one\n'),
    (TRIM,
     '                         # directories, since D5 moves the archive last, and a shard name is never reused\n',
     '                         # directories, since the archive moves last, and a shard name is never reused\n'),
    (TRIM,
     'NEW_DIR = "methodology"        # layout: ok -- the directory a migrated project keeps its framework files in (plan 4.1)\n',
     'NEW_DIR = "methodology"        # layout: ok -- the directory a migrated project keeps its framework files in\n'),
    (TRIM,
     'NEW_ARCHIVE_DIR = NEW_DIR + "/archive"   # decision D5: the archive moves with the ledgers\n',
     'NEW_ARCHIVE_DIR = NEW_DIR + "/archive"   # the archive moves with the ledgers\n'),
    (TRIM,
     "a document cited by bare name inside the proof (names are relative to the runner's directory, plan 4.4)\n",
     "a document cited by bare name inside the proof (names are relative to the runner's directory)\n"),
    (TRIM,
     "# A ledger sits at its project's root (legacy) or under methodology/ (new): the plan's section 4.3. The\n",
     "# A ledger sits at its project's root (legacy) or under methodology/ (new). The\n"),
    (TRIM,
     "    still holds the shards its legacy trims wrote under docs/archive/ (D5 moves the archive last), and\n",
     "    still holds the shards its legacy trims wrote under docs/archive/ (the archive moves last), and\n"),
    (TRIM,
     "    the shards its legacy trims wrote are its history, since the archive moves last (D5).\n",
     "    the shards its legacy trims wrote are its history, since the archive moves last.\n"),
    (TRIM,
     "    BL-101 P3: a ledger a project moved under methodology/ is the same ledger at its new address, the\n",
     "    A ledger a project moved under methodology/ is the same ledger at its new address, the\n"),
    (TRIM,
     "    # BL-101 P3. Every trim writes an entry into the ACTION ledger, wherever the trimmed file sits, so\n",
     "    # Every trim writes an entry into the ACTION ledger, wherever the trimmed file sits, so\n"),
    (TRIM,
     "    resolver calls half-migrated. The framework anchor decides a tie without being asked (decided\n"
     "    2026-10-06 and 2026-10-07, plan 7.2a and 7.2b): a project's own product changelog may sit at the root beside the ledger. A tree with no\n",
     "    resolver calls half-migrated. The framework anchor decides a tie without being asked:\n"
     "    a project's own product changelog may sit at the root beside the ledger. A tree with no\n"),
    # ---- its tests: 4 flagged lines (5 changed lines); the fifth flagged line (:4622, P1) stays ----
    (TEST,
     "# BL-101 P3 -- a ledger under methodology/ (plan sections 4.3, 4.8, 7.2 row P3; coupling C7).\n",
     "# A ledger under methodology/.\n"),
    (TEST,
     "# ledger under methodology/): shards in methodology/archive/ (decision D5), links climb one, and a\n",
     "# ledger under methodology/): shards in methodology/archive/, links climb one, and a\n"),
    (TEST,
     '    """Add one entry-level link that climbs out of methodology/ -- the convention the plan gives a new\n'
     '    ledger for a link to a project file (C6) -- to EVERY record, in a commit of its own."""\n',
     '    """Add one entry-level link that climbs out of methodology/ -- the convention for a new\n'
     "    ledger's link to a project file -- to EVERY record, in a commit of its own.\"\"\"\n"),
    (TEST,
     '    """D5 moves the archive LAST: a project whose ledger already moved still holds the shards its legacy\n',
     '    """The archive moves LAST: a project whose ledger already moved still holds the shards its legacy\n'),
]


def main():
    repo = sys.argv[1]
    texts = {}
    for path in (TRIM, TEST):
        with open(os.path.join(repo, path), encoding="utf-8", newline="") as f:
            texts[path] = f.read()
    for path, old, new in EDITS:
        n = texts[path].count(old)
        if n != 1:
            raise SystemExit("REFUSED, nothing written: %d occurrences (need 1) in %s of: %r" % (n, path, old[:90]))
        texts[path] = texts[path].replace(old, new)
    for path in (TRIM, TEST):
        with open(os.path.join(repo, path), "w", encoding="utf-8", newline="") as f:
            f.write(texts[path])
    print("wrote %d edits to %d files" % (len(EDITS), 2))


main()
