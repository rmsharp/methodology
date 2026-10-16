#!/usr/bin/env python3
"""The 32nd commit's edits (the build session on pr2/candidate, 2026-10-15): four statements the series left stale in text,
each re-derived on the candidate before it was written (fix32-record.md section 2). No code path and no threshold changes.

Run in a clone of pr2/candidate checked out at ced2c82:  python3 -I fix32-build.py REPO

It refuses, writing nothing, if a file is not the blob it was derived from, if an anchor is not found exactly once, if the
two dashboard copies differ before or after, or if an edit changes anything the proof below says it must not. It then writes
the four files. It does not commit; the commit message is fix32-message.txt. Generates no bytecode.

The proof it runs on its own output: the gate manifest parses and differs from the old one in exactly two `why` strings (every
other key, threshold and command equal); each of the two Python files has the same syntax tree before and after once its
docstring is set aside (a comment is not in the tree); and the two dashboard copies are still byte-identical.
"""
import ast
import json
import subprocess
import sys

sys.dont_write_bytecode = True

REPO = sys.argv[1]
GATES, DASH, TWIN, MIGRATE = ".quality-gates.json", "starter-kit/methodology_dashboard.py", "tools/methodology_dashboard.py", "bin/migrate-layout"
BEFORE = {
    GATES: "af65dccc7a32b9818b4ab5743a9b7f77dfcb0229",     # 8,289 B
    DASH: "9ab16ccc4e8b78853fdb9b78dd9da1935c6deac5",      # 279,968 B, the twin's blob too
    TWIN: "9ab16ccc4e8b78853fdb9b78dd9da1935c6deac5",
    MIGRATE: "ea2db7187c83e569703b9c8f51538dbde23d05ba",   # 78,391 B
}

# 1. layout-literals: the reason said the two ledger checkers are not scanned and do not read the layout; both are scanned
#    (the scanner takes every file in bin/ but the two it names) and both resolve their ledger through the embedded resolver.
LITERALS_OLD = ("bin/check-handoff and bin/check-ledger are not scanned: they are canonical-only checkers that adopters never run, "
                "and this change does not give them the layout reading.")
LITERALS_NEW = ("The scan covers starter-kit/*.py, bin/* and .githooks/*, so the canonical-only bin/check-handoff and "
                "bin/check-ledger are scanned like the rest; it skips bin/_manifest.py and bin/tests.sh by name.")
# 2. layout-unit-tests: the reason said 74 is measured against a floor of 76; the suite runs 76.
UNIT_OLD = "74 is measured (Ran 74 tests, OK)."
UNIT_NEW = "76 is measured (Ran 76 tests, OK)."
# 3. the comment above the stale-copy warning said the per-project remedy is one cp; the warning prints a scoped --sync.
DASH_OLD = ("        # missing part — the safe per-project action is one `cp`, and the message never printed it.\n")
DASH_NEW = ("        # missing part — the safe per-project action is a `--sync` scoped to that one project, and\n"
            "        # the message never printed it.\n")
# 4. the header's exit list stopped at 3; an apply whose after-checks differ from its before-checks returns 4 (main: line 1309).
MIGRATE_OLD = "rolled back.\n\"\"\"\nimport argparse\n"
MIGRATE_NEW = ("rolled back · 4 an apply that committed and whose after-checks differ from its before-checks, or that left the\n"
               "tree dirty (the commit stands; the report names the `git revert` that undoes it).\n\"\"\"\nimport argparse\n")


def git(*a, stdin=None):
    r = subprocess.run(["git", "-C", REPO, *a], input=stdin, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("refused: git %s: %s" % (" ".join(a), r.stderr.strip()))
    return r.stdout.strip()


def read(rel):
    with open("%s/%s" % (REPO, rel), encoding="utf-8", newline="") as f:
        return f.read()


def once(text, old, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit("refused: %s found %d times (expected 1)" % (label, n))


def code_without_docstring(source):
    tree = ast.parse(source)
    first = tree.body[0] if tree.body else None
    if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
        tree.body = tree.body[1:]
    return ast.dump(tree)


old = {rel: read(rel) for rel in BEFORE}
for rel, blob in BEFORE.items():
    if git("hash-object", "--stdin", stdin=old[rel]) != blob:
        raise SystemExit("refused: %s is not the blob this was derived from (%s)" % (rel, blob[:8]))
if old[DASH] != old[TWIN]:
    raise SystemExit("refused: the two dashboard copies differ before the edit")
for text, label, src in ((LITERALS_OLD, "the layout-literals sentence", GATES), (UNIT_OLD, "the layout-unit-tests count", GATES),
                         (DASH_OLD, "the stale-copy comment line", DASH), (MIGRATE_OLD, "the end of the exit list", MIGRATE)):
    once(old[src], text, label)
once(old[TWIN], DASH_OLD, "the stale-copy comment line in the twin")

new = {
    GATES: old[GATES].replace(LITERALS_OLD, LITERALS_NEW).replace(UNIT_OLD, UNIT_NEW),
    DASH: old[DASH].replace(DASH_OLD, DASH_NEW),
    MIGRATE: old[MIGRATE].replace(MIGRATE_OLD, MIGRATE_NEW),
}
new[TWIN] = old[TWIN].replace(DASH_OLD, DASH_NEW)

if new[DASH] != new[TWIN]:
    raise SystemExit("refused: the two dashboard copies differ after the edit")
before_g, after_g = json.loads(old[GATES]), json.loads(new[GATES])
changed = [(b["name"], k) for b, a in zip(before_g["gates"], after_g["gates"]) for k in b if b[k] != a[k]]
if len(before_g["gates"]) != len(after_g["gates"]) or sorted(changed) != [("layout-literals", "why"), ("layout-unit-tests", "why")]:
    raise SystemExit("refused: the gate manifest differs in more than the two reasons: %r" % (changed,))
if {k: v for k, v in before_g.items() if k != "gates"} != {k: v for k, v in after_g.items() if k != "gates"}:
    raise SystemExit("refused: the manifest's header keys changed")
for rel in (DASH, MIGRATE):
    if code_without_docstring(old[rel]) != code_without_docstring(new[rel]):
        raise SystemExit("refused: %s has a different syntax tree after the edit" % rel)
for line in (DASH_NEW.splitlines()):
    if len(line) > 100:
        raise SystemExit("refused: a new comment line is %d characters" % len(line))

for rel in (GATES, DASH, TWIN, MIGRATE):
    with open("%s/%s" % (REPO, rel), "w", encoding="utf-8", newline="") as f:
        f.write(new[rel])
    print("wrote %-36s %7d B -> %7d B  blob %s" % (rel, len(old[rel].encode()), len(new[rel].encode()),
                                                  git("hash-object", rel)[:8]))
print("proof: manifest differs in exactly layout-literals.why and layout-unit-tests.why; syntax trees equal (docstring set aside) "
      "for %s and %s; dashboard twins identical" % (DASH, MIGRATE))
