#!/usr/bin/env python3
"""Mutation round for BL-102 (S350): quality_ratchet.py 1.5.1, install_hook's tool-path expression.

Each mutant rewrites that one expression in a scratch copy of starter-kit/quality_ratchet.py; the three tests of
TestTheHookFromASymlinkedPath (tools/test_quality_ratchet.py) then run against it. A mutant is KILLED when that
class does not pass. Run from anywhere: python3 docs/planning/bl102-evidence/mutate-bl102.py

Recorded result (S350): M1 to M5 killed, M6 survives and is equivalent (git already reports its toplevel as a
real path, so resolving it again changes nothing on this platform). M2, the backlog row's whole-file realpath,
is killed by the symlinked-tool-file test alone.
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
FIXED = ("    tool = os.path.relpath(os.path.join(os.path.realpath(os.path.dirname(here)), os.path.basename(here)),\n"
         "                           os.path.realpath(top))\n")
MUTANTS = {
    "M1 back to abspath (1.5.0)":
        "    tool = os.path.relpath(os.path.abspath(__file__), top)\n",
    "M2 realpath of the whole file (the backlog row's shape)":
        "    tool = os.path.relpath(os.path.realpath(__file__), os.path.realpath(top))\n",
    "M3 directory resolved via the resolved file":
        "    tool = os.path.relpath(os.path.join(os.path.dirname(os.path.realpath(here)), os.path.basename(here)), os.path.realpath(top))\n",
    "M4 file name taken from the resolved file":
        "    tool = os.path.relpath(os.path.join(os.path.realpath(os.path.dirname(here)), os.path.basename(os.path.realpath(here))), os.path.realpath(top))\n",
    "M5 toplevel resolved, tool not":
        "    tool = os.path.relpath(here, os.path.realpath(top))\n",
    "M6 toplevel not resolved (equivalent: git already reports the real path)":
        "    tool = os.path.relpath(os.path.join(os.path.realpath(os.path.dirname(here)), os.path.basename(here)), top)\n",
}


def main():
    src = (REPO / "starter-kit" / "quality_ratchet.py").read_text(encoding="utf-8")
    if src.count(FIXED) != 1:
        sys.exit("the fixed expression is not in starter-kit/quality_ratchet.py exactly once")
    for name, body in MUTANTS.items():
        with tempfile.TemporaryDirectory() as t:
            (Path(t) / "starter-kit").mkdir()
            (Path(t) / "tools").mkdir()
            (Path(t) / "starter-kit" / "quality_ratchet.py").write_text(src.replace(FIXED, body), encoding="utf-8")
            shutil.copy(REPO / "tools" / "test_quality_ratchet.py", Path(t) / "tools")
            p = subprocess.run([sys.executable, str(Path(t) / "tools" / "test_quality_ratchet.py"),
                                "TestTheHookFromASymlinkedPath"], capture_output=True, text=True, cwd=t)
            killers = [m.group(1) for m in re.finditer(r"^(?:FAIL|ERROR): (\w+)", p.stderr, re.M)]
            print(f"{'KILLED' if p.returncode else 'SURVIVED':8} {name}")
            for k in killers:
                print(f"           by {k}")


if __name__ == "__main__":
    main()
