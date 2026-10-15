#!/usr/bin/env python3
"""Mutants aimed at CODE of the checkers' layer, run against the layer's own suites.

    python3 layer6b-mutate.py <clone> [--round 1|2]

<clone> is a scratch `--no-local` clone checked out at the layer's last commit (NEVER the working tree you care about:
each mutant is written into the clone and restored after, and an interrupted run leaves the clone dirty). For each mutant:
the one old line must occur exactly once in its file, the changed line is printed (a first-occurrence replace once landed in
a docstring and read as "survived"), then the checker suite and the layout suite run, and the mutant is KILLED when either
fails and SURVIVED when both pass. A control (no mutation) must pass both first. The scanner gate is run for the marker
mutants, which no unit suite reads (the gate `layout-literals` does).

Round 1 aims at the lines the layer carries and the suite names; round 2 at behaviours no test names, chosen after round 1.
"""
import subprocess
import sys
from pathlib import Path

LEDGER, HANDOFF = "bin/check-ledger", "bin/check-handoff"
SUITES = ("tools/test_checker_layouts.py", "tools/test_layout_resolver.py")

H_MARK = '  # layout: ok -- the receipt ledger\'s own file name: the resolver\'s anchor'

ROUND1 = [
    # check-ledger
    ("L1 a half-migrated tree is not refused", LEDGER,
     '    if kind == "half":\n        return None, found\n', '    if False:\n        return None, found\n'),
    ("L2 the ledger is always read at the root", LEDGER,
     '    return (directory if directory is not None else root) / LEDGER_NAME, found\n',
     '    return root / LEDGER_NAME, found\n'),
    ("L3 the refusal exits 0", LEDGER,
     '                  file=sys.stderr)\n            return 2\n', '                  file=sys.stderr)\n            return 0\n'),
    ("L4 a repository called methodology is taken for a project's subdirectory", LEDGER,
     '    nested = base.name == NEW_DIR and not (base / ".git").exists()\n',
     '    nested = base.name == NEW_DIR\n'),
    ("L5 the archive beside a ledger under methodology/ is not read", LEDGER,
     '    if nested:\n        dirs.append(base / ARCHIVE_PARTS[-1])\n', '    if False:\n        dirs.append(base / ARCHIVE_PARTS[-1])\n'),
    ("L6 the project's docs/archive/ is read from beside the ledger when nested", LEDGER,
     '    top = base.parent if nested else base\n', '    top = base\n'),
    ("L7 only the first archive directory is read", LEDGER,
     '        for d in shard_dirs(path):\n', '        for d in shard_dirs(path)[:1]:\n'),
    # check-handoff
    ("H1 a half-migrated tree is not refused", HANDOFF,
     '    if kind == "half":\n        raise HalfMigrated(found)\n', '    if False:\n        raise HalfMigrated(found)\n'),
    ("H2 the ledger is always read at the root", HANDOFF,
     '    if directory is not None:\n        return directory / LEDGER_NAME\n', '    if directory is not None:\n        return root / LEDGER_NAME\n'),
    ("H3 the seed is no longer the fallback", HANDOFF,
     '    return root / "starter-kit" / LEDGER_NAME\n', '    return root / LEDGER_NAME\n'),
    ("H4 the refusal exits 0", HANDOFF,
     'for f in half.found)))\n        return 1\n', 'for f in half.found)))\n        return 0\n'),
    ("H5 the refusal names neither copy", HANDOFF,
     '" and ".join(str(f) for f in half.found)))', '"")))'),
    ("H6 the anchor is the runner, not the ledger", HANDOFF,
     '    kind, directory, found = resolve_layout(root, LEDGER_NAME)\n', '    kind, directory, found = resolve_layout(root)\n'),
    ("H7 the resolver reports a tie as legacy (the block, in check-handoff only)", HANDOFF,
     '        return "half", None, found\n', '        return "legacy", root, found\n'),
]

MARKERS = [  # no unit suite reads a marker; the scanner gate does
    ("M1 a marker removed from check-handoff's ledger-name constant", HANDOFF,
     'LEDGER_NAME = "HANDOFFS.md"' + H_MARK, 'LEDGER_NAME = "HANDOFFS.md"'),
    ("M2 a marker removed from check-ledger's ledger-name constant", LEDGER,
     'LEDGER_NAME = "CHANGELOG.md"  # layout: ok -- the ledger\'s own file name: the resolver\'s anchor',
     'LEDGER_NAME = "CHANGELOG.md"'),
]

ROUND2 = [
    # behaviours no test named after round 1: the promise the refusal message makes, the no-ledger path, the tie rule in check-ledger
    ("R2-1 check-ledger ignores an explicit --file (the refusal message says to name the ledger with it)", LEDGER,
     '    if args.file:\n        path = Path(args.file)\n', '    if False:\n        path = Path(args.file)\n'),
    ("R2-2 check-ledger finds no ledger anywhere and reads from the wrong directory", LEDGER,
     '    return (directory if directory is not None else root) / LEDGER_NAME, found\n',
     '    return (directory if directory is not None else root.parent) / LEDGER_NAME, found\n'),
    ("R2-3 check-ledger's resolver reports a tie as legacy (the block, in check-ledger only)", LEDGER,
     '        return "half", None, found\n', '        return "legacy", root, found\n'),
    ("R2-4 check-ledger lets a runner at the root decide a tie as well", LEDGER,
     ' and not _os.path.isfile(root / "SESSION_RUNNER.md"):\n', ':\n'),
    ("R2-5 check-handoff lets a runner at the root decide a tie as well", HANDOFF,
     ' and not _os.path.isfile(root / "SESSION_RUNNER.md"):\n', ':\n'),
    ("R2-6 check-handoff ignores an explicit --file", HANDOFF,
     '        path = Path(args.file) if args.file else default_path()\n', '        path = default_path()\n'),
]


def run(clone, args):
    return subprocess.run([sys.executable, "-B"] + args, cwd=clone, capture_output=True, text=True)


def suites(clone):
    return [(s, run(clone, [s]).returncode) for s in SUITES]


def main():
    clone = Path(sys.argv[1])
    rnd = 1
    if "--round" in sys.argv:
        rnd = int(sys.argv[sys.argv.index("--round") + 1])
    mutants = ROUND1 if rnd == 1 else ROUND2
    if subprocess.run(["git", "-C", str(clone), "status", "--short"], capture_output=True, text=True).stdout.strip():
        raise SystemExit("refused: the clone is dirty")
    base = suites(clone)
    print("control (no mutation):", ", ".join("%s exit %d" % (Path(s).name, rc) for s, rc in base))
    if any(rc for _, rc in base):
        raise SystemExit("refused: the control is not green")
    killed = survived = 0
    for name, rel, old, new in mutants + (MARKERS if rnd == 1 else []):
        p = clone / rel
        text = p.read_text(encoding="utf-8")
        if text.count(old) != 1:
            raise SystemExit("refused: %s: the old line occurs %d times in %s" % (name, text.count(old), rel))
        changed = text.replace(old, new)
        assert changed != text
        p.write_text(changed, encoding="utf-8")
        try:
            before = text.splitlines()
            line = " | ".join(l.strip() for l in changed.splitlines() if l not in before)
            if name.startswith("M"):
                gate = run(clone, ["bin/check-layout-literals"])
                results = [("check-layout-literals", gate.returncode)]
            else:
                results = suites(clone)
        finally:
            p.write_text(text, encoding="utf-8")
        dead = [Path(s).name for s, rc in results if rc]
        verdict = "KILLED by " + ", ".join(dead) if dead else "SURVIVED"
        killed += bool(dead)
        survived += not dead
        print("%-82s %s\n      changed line: %s" % (name, verdict, line[:150]))
    status = subprocess.run(["git", "-C", str(clone), "status", "--short"], capture_output=True, text=True).stdout.strip()
    print("round %d: %d killed, %d survived; clone clean afterwards: %s" % (rnd, killed, survived, "yes" if not status else "NO: " + status))
    return 0


if __name__ == "__main__":
    sys.exit(main())
