#!/usr/bin/env python3
"""Mutation round for BL-110 (S351): bin/check-links counts `docs/methodology` strings per shipped document.

Each mutant rewrites one expression of the counting code in a scratch clone of this repository (the working tree's
bin/check-links and tools/test_sync_layouts.py are copied over the clone's, so the round runs on uncommitted work).
Two things then run against it: the new class TestCheckLinksCountsTheLegacyDirectory (tools/test_sync_layouts.py)
and the real-tree command bin/check-links (what the shell suite's Test 10 and the `check-links` gate run). A
mutant is KILLED when either fails. Run from anywhere: python3 docs/planning/bl110-evidence/mutate-bl110.py
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CLASS = "TestCheckLinksCountsTheLegacyDirectory"
MD_FILTER = '        if not src.endswith(".md"):\n            continue\n'
TREE_RETURN = '        return report(checked, failures, n_files, "the tree at %s%s" % (tree, " (new layout)" if layout == "new" else ""))\n'
TREE_COUNT = (
    "        for _s, _d, _x in DISTRIBUTION:\n"
    "            _p = os.path.join(tree, dest_in(layout, _s, _d))\n"
    "            if _d.endswith('.md') and os.path.exists(_p) and \\\n"
    "                    open(_p, encoding='utf-8').read().count(LEGACY_PATH) > LEGACY_PATH_ALLOWANCE.get(_s, 0):\n"
    "                return 1\n")
# (name, old text that occurs exactly once, new text, whether the real tree is expected to catch it too)
MUTANTS = [
    ("M1 at the allowance already fails", "if len(lines) > allowed:", "if len(lines) >= allowed:"),
    ("M2 an unlisted document may carry one", "LEGACY_PATH_ALLOWANCE.get(src, 0)", "LEGACY_PATH_ALLOWANCE.get(src, 1)"),
    ("M3 lines are counted, not strings",
     "lines = [n for n, line in enumerate(fh, 1) for _ in range(line.count(LEGACY_PATH))]",
     "lines = [n for n, line in enumerate(fh, 1) if LEGACY_PATH in line]"),
    ("M4 every distributed source is read, not only the markdown", MD_FILTER, "        if False:\n            continue\n"),
    ("M5 the finding is reported once per layout run",
     "    if over:\n        results.append(report_legacy_paths(over))\n",
     "    for _ in results[:]:\n        if over:\n            results.append(report_legacy_paths(over))\n"),
    ("M6 --tree counts the tree's copies", TREE_RETURN, TREE_COUNT + TREE_RETURN),
    ("M7 line numbers start at 0", "for n, line in enumerate(fh, 1) for _ in", "for n, line in enumerate(fh) for _ in"),
    ("M8 the finding does not fail the run", "    return 1\n\n\n# Markdown inline link target", "    return 0\n\n\n# Markdown inline link target"),
    ("M9 a line with two strings is listed twice", "where = sorted(set(lines))", "where = lines"),
    ("M10 BOOTSTRAP's allowance one below its count", '"starter-kit/BOOTSTRAP.md": 9,', '"starter-kit/BOOTSTRAP.md": 8,'),
    ("M11 BOOTSTRAP's allowance one above its count (a table edit a reviewer sees; a ceiling survives it by design)",
     '"starter-kit/BOOTSTRAP.md": 9,', '"starter-kit/BOOTSTRAP.md": 10,'),
]


def run(args, cwd):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


def main():
    src = (REPO / "bin" / "check-links").read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as t:
        clone = Path(t) / "clone"
        run(["git", "clone", "-q", "--no-local", str(REPO), str(clone)], t)
        shutil.copy(REPO / "tools" / "test_sync_layouts.py", clone / "tools" / "test_sync_layouts.py")
        script = clone / "bin" / "check-links"
        script.write_text(src, encoding="utf-8")
        control = (run([sys.executable, "-B", str(script)], clone).returncode,
                   run([sys.executable, "-B", "tools/test_sync_layouts.py", CLASS], clone).returncode)
        print("control (no mutation): real tree exit %d, class exit %d" % control)
        if control != (0, 0):
            sys.exit("refused: the control is not green")
        for name, old, new in MUTANTS:
            if src.count(old) != 1:
                sys.exit("%s: the old text occurs %d times, not once" % (name, src.count(old)))
            script.write_text(src.replace(old, new), encoding="utf-8")
            real = run([sys.executable, "-B", str(script)], clone)
            unit = run([sys.executable, "-B", "tools/test_sync_layouts.py", CLASS], clone)
            killers = [m.group(1) for m in re.finditer(r"^(?:FAIL|ERROR): (\w+)", unit.stderr, re.M)]
            if real.returncode:
                killers.append("the real-tree command (exit %d)" % real.returncode)
            print("%-8s %s" % ("KILLED" if killers else "SURVIVED", name))
            for k in killers:
                print("           by " + k)
        script.write_text(src, encoding="utf-8")


if __name__ == "__main__":
    main()
