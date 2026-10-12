#!/usr/bin/env python3
"""Mutation round over the BL-105 phase 3 change in bin/check-links.

Runs ONLY in the clone it is given (argv[1]); refuses a path that is not a `--no-local` clone of the canonical repo
under ~/.cache, so it can never touch a working tree. Each mutant is one exact-string replacement in bin/check-links;
the two check-links classes of tools/test_sync_layouts.py run against it; a mutant is killed if either fails.
"""
import os, subprocess, sys
from pathlib import Path

clone = Path(sys.argv[1]).resolve()
cache = (Path.home() / ".cache").resolve()
assert cache in clone.parents, "refusing: %s is not under ~/.cache" % clone
assert (clone / ".git").is_dir() and (clone / "bin" / "check-links").is_file()
target = clone / "bin" / "check-links"
orig = target.read_text(encoding="utf-8")

MUTANTS = [
    ("M1 companions_in returns nothing",
     "    return [beside_in(layout, COMPANION_NEIGHBOUR, name) for name in COMPANION_FILES]",
     "    return []"),
    ("M2 companions_in ignores the layout (root name only)",
     "    return [beside_in(layout, COMPANION_NEIGHBOUR, name) for name in COMPANION_FILES]",
     "    return list(COMPANION_FILES)"),
    ("M3 companions_in allows the root AND the neighbour's directory",
     "    return [beside_in(layout, COMPANION_NEIGHBOUR, name) for name in COMPANION_FILES]",
     "    return list(COMPANION_FILES) + [beside_in(layout, COMPANION_NEIGHBOUR, name) for name in COMPANION_FILES]"),
    ("M4 beside_in always uses the legacy destination",
     "return os.path.join(os.path.dirname(dest_in(layout, src, dest)), name)",
     "return os.path.join(os.path.dirname(dest), name)"),
    ("M5 the neighbour is a file in another directory",
     'COMPANION_NEIGHBOUR = "starter-kit/FRAMEWORK_LEARNINGS.md"',
     'COMPANION_NEIGHBOUR = "workstreams/DESIGN_WORKSTREAM.md"'),
    ("M6 allowed_absent drops the companions",
     "ADOPTER_LOCAL_FILES + companions_in(layout) + [placeholder_in(layout)]",
     "ADOPTER_LOCAL_FILES + [placeholder_in(layout)]"),
    ("M7 the old behaviour comes back: the file is a root file in the other list",
     '    "BACKLOG.md",            # adopter-created task list\n]',
     '    "BACKLOG.md",            # adopter-created task list\n    "PROJECT_LEARNINGS.md",\n]'),
    ("M8 placeholder_in loses the shared helper's layout",
     "    return beside_in(layout, template, name)",
     "    return beside_in('legacy', template, name)"),
    ("M9 the companion list is empty",
     '    "PROJECT_LEARNINGS.md",  # CLAUDE.md overflow valve (BOOTSTRAP.md)\n]\nCOMPANION_NEIGHBOUR',
     ']\nCOMPANION_NEIGHBOUR'),
]

CLASSES = ["TestCheckLinksSimulatesBothLayouts", "TestCheckLinksTreeModeReadsTheTreesLayout"]


def run_tests():
    r = subprocess.run([sys.executable, "-B", "tools/test_sync_layouts.py", *CLASSES], cwd=clone,
                       capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)


rc, out = run_tests()
print("baseline: exit %d, %s" % (rc, out.strip().splitlines()[-1]))
assert rc == 0, out[-800:]
survived = []
for name, old, new in MUTANTS:
    assert orig.count(old) == 1, "%s: anchor matches %d times" % (name, orig.count(old))
    target.write_text(orig.replace(old, new, 1), encoding="utf-8")
    try:
        rc, out = run_tests()
    finally:
        target.write_text(orig, encoding="utf-8")
    fails = [l for l in out.splitlines() if l.startswith(("FAIL:", "ERROR:"))]
    print("%-70s %s" % (name, "KILLED (%d red)" % len(fails) if rc != 0 else "SURVIVED"))
    if rc == 0:
        survived.append(name)
print("survivors: %d of %d" % (len(survived), len(MUTANTS)))
for s in survived:
    print("  survivor:", s)
sys.exit(1 if survived else 0)
