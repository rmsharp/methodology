#!/usr/bin/env python3
"""Compare two runs of `methodology-subdirectory-evidence/migrate-12-adopters.py`, column by column, adopter by adopter.

    python3 layer7b-adopters-compare.py <rows.json of run A> <rows.json of run B>

Run A was made from a clean clone of the pull request candidate (`ab35e96`) and run B from a clean clone of the fork's tip (`91fdf8c`);
both over the same twelve adopters' committed HEADs, in `--no-local` clones, one after the other (the script's `--out` and `--work` given,
because its default `--out` is the committed output of the original run). Each adopter is synced by the run's own `bin/sync`, migrated
by the run's own `bin/migrate-layout` (a dry run, then `--apply` with the checks on), and measured with the adopter's own dashboard and
ratchet, so a difference is a difference between the two TREES of tools and documents: the tool's bytes are equal in both.

Prints, per adopter, the columns that differ, then a count of the columns that are equal in every adopter. `seconds` is not compared.
A path inside a column (the run's scratch directory) differs by construction: those cells are compared with the directory removed.
"""
import json
import re
import sys

SCRATCH = re.compile(r"/private/tmp/[^ ']*?s322-adopters-[AB]-work/")


def norm(v):
    return SCRATCH.sub("<work>/", str(v)) if v is not None else v


def main():
    a_rows = {r["adopter"]: r for r in json.load(open(sys.argv[1], encoding="utf-8"))}
    b_rows = {r["adopter"]: r for r in json.load(open(sys.argv[2], encoding="utf-8"))}
    cols = sorted({k for r in list(a_rows.values()) + list(b_rows.values()) for k in r} - {"adopter", "seconds"})
    print("adopters: A %d, B %d; columns compared: %d (%s)" % (len(a_rows), len(b_rows), len(cols), ", ".join(cols)))
    differing = {c: 0 for c in cols}
    for name in a_rows:
        a, b = a_rows[name], b_rows.get(name, {})
        ds = [c for c in cols if norm(a.get(c)) != norm(b.get(c))]
        print("\n== %s: %d differing column(s)" % (name, len(ds)))
        for c in ds:
            differing[c] += 1
            print("   %s:\n      A  %s\n      B  %s" % (c, str(norm(a.get(c)))[:210], str(norm(b.get(c)))[:210]))
    print("\ncolumns equal in all %d adopters: %s" % (len(a_rows), ", ".join(c for c in cols if not differing[c])))
    print("columns that differ in at least one: %s" % ", ".join("%s (%d)" % (c, n) for c, n in differing.items() if n))


if __name__ == "__main__":
    main()
