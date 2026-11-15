#!/usr/bin/env python3
"""Mutation round for BL-103 option (c) (S452): quality_ratchet.py 1.7.0, the clause that names the unmeasured gates.

Each mutant rewrites one place in a scratch copy of starter-kit/quality_ratchet.py (every `old` text must occur in
the tool exactly once); the new class of tools/test_quality_ratchet.py, `TestTheUnmeasuredGatesAreNamed`, and the
version pin then run against that copy with `-f` (stop at the first failure). A mutant is KILLED when they do not
all pass, and SURVIVES when they do. The scratch tree also holds a copy of bin/check-handoff, which the
round-trip test loads. Run from anywhere:  python3 docs/planning/bl103-evidence/mutate-repair4.py [M05 M12 ...]

Two controls come first, so a zero from this instrument means something: M00 changes nothing and must SURVIVE
(the tests pass on the unmutated copy), and M01 makes the clause always empty and must be KILLED. The older
classes are not run: they test code this round does not touch, and four of them flake with the machine's load.
"""
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
TESTS = ["TestTheUnmeasuredGatesAreNamed", "TestToolInvariants.test_the_version_is_1_7_0"]

BLOCK = ('    print(f"  {D}cite in the receipt:{R} {summary_line(snap)}")\n'
         '    clause = unmeasured_clause(snap)\n'
         '    if clause:\n'
         '        print(f"  {D}and name them:{R}       {clause}")   # plain after the label: it is pasted, not read\n'
         '    print()\n')
RETURN = 'return "unmeasured: " + ", ".join(names) if names else ""'
SELF_CHECK = ('        # the run names it, in the form the receipt lint reads, after the citable line (1.7.0)\n'
              '        check("the unmeasured gates are named in the clause the lint reads",\n'
              '              re.search(r"and name them:\\s+unmeasured: declared-only\\s*$", '
              're.sub(r"\\033\\[[0-9;]*m", "", out), re.M)\n'
              '              is not None)\n')

# (name, [(old, new), ...])
MUTANTS = [
    ("M00 CONTROL: nothing changed (must SURVIVE)", []),
    ("M01 CONTROL: the clause is always empty (must be KILLED)", [(RETURN, "return ''")]),
    ("M02 only the first unmeasured gate is named", [('", ".join(names)', '", ".join(names[:1])')]),
    ("M03 the names are sorted", [('", ".join(names)', '", ".join(sorted(names))')]),
    ("M04 the names are joined with a comma and no space", [('", ".join(names)', '",".join(names)')]),
    ("M05 the names are joined with ' and '", [('", ".join(names)', '" and ".join(names)')]),
    ("M06 a failed gate is named too", [('if r["status"] == "unmeasured"]', 'if r["status"] in ("unmeasured", "fail")]')]),
    ("M07 a passed gate is named too", [('if r["status"] == "unmeasured"]', 'if r["status"] != "fail"]')]),
    ("M08 a name is cut to the table's 30 columns", [('names = [r["name"] for', 'names = [r["name"][:30] for')]),
    ("M09 the clause has no colon", [(RETURN, RETURN.replace('"unmeasured: "', '"unmeasured "'))]),
    ("M10 the clause starts with a capital", [(RETURN, RETURN.replace('"unmeasured: "', '"Unmeasured: "'))]),
    ("M11 an empty clause is 'unmeasured: ' and not ''", [(RETURN, 'return "unmeasured: " + ", ".join(names)')]),
    ("M12 the label is printed even with no clause",
     [("    if clause:\n        print(f\"  {D}and name them:", "    if True:\n        print(f\"  {D}and name them:")]),
    ("M13 the clause is printed before the citation",
     [(BLOCK, '    clause = unmeasured_clause(snap)\n'
              '    if clause:\n'
              '        print(f"  {D}and name them:{R}       {clause}")   # plain after the label: it is pasted, not read\n'
              '    print(f"  {D}cite in the receipt:{R} {summary_line(snap)}")\n'
              '    print()\n')]),
    ("M14 a blank line sits between the citation and the clause",
     [('{summary_line(snap)}")\n    clause = unmeasured_clause(snap)', '{summary_line(snap)}")\n    print()\n    clause = unmeasured_clause(snap)')]),
    ("M15 no blank line follows the clause",
     [('{clause}")   # plain after the label: it is pasted, not read\n    print()\n',
       '{clause}")   # plain after the label: it is pasted, not read\n    if not clause:\n        print()\n')]),
    ("M16 the label reads 'names:'", [("and name them:{R}       {clause}", "names:{R}       {clause}")]),
    ("M17 the clause is coloured", [("       {clause}\")   # plain", "       {YEL}{clause}{R}\")   # plain")]),
    ("M18 --status does not print the clause",
     [("    if clause:\n        print(f\"  {D}and name them:", "    if clause and title.startswith(\"quality gates \u2014 run\"):\n        print(f\"  {D}and name them:")]),
    ("M19 --run does not print the clause",
     [("    if clause:\n        print(f\"  {D}and name them:", "    if clause and not title.startswith(\"quality gates \u2014 run\"):\n        print(f\"  {D}and name them:")]),
    ("M20 --json carries the clause",
     [('        print(json.dumps(snap, indent=1, sort_keys=True))\n    else:\n        render(snap, "quality gates \u2014 run")',
       '        print(json.dumps(snap, indent=1, sort_keys=True))\n        print(unmeasured_clause(snap))\n    else:\n        render(snap, "quality gates \u2014 run")')]),
    ("M21 the results file carries the clause",
     [('    with open(results_path(root, cfg), "w") as f:\n        json.dump(snap, f, indent=1, sort_keys=True)',
       '    snap["named"] = unmeasured_clause(snap)\n    with open(results_path(root, cfg), "w") as f:\n        json.dump(snap, f, indent=1, sort_keys=True)')]),
    ("M22 the version stays 1.6.0", [('VERSION = "1.7.0"', 'VERSION = "1.6.0"')]),
    ("M23 --help does not show the clause",
     [("also prints `unmeasured: <gate>, <gate>`, the", "also prints a clause, the")]),
    ("M24 the docstring does not show the clause",
     [("`unmeasured: <gate>, <gate>`: the unmeasured gates in the manifest's order", "the unmeasured gates in the manifest's order")]),
    ("M25 the selftest does not observe the clause", [(SELF_CHECK, "")]),
    ("M30 the notes are named, not the gates", [('names = [r["name"] for', 'names = [(r.get("note") or r["name"]) for')]),
    ("M31 each name is in backticks", [('names = [r["name"] for', 'names = ["`" + r["name"] + "`" for')]),
    ("M32 the names are reversed", [('", ".join(names)', '", ".join(reversed(names))')]),
]


def run_one(src, edits):
    out = src
    for old, new in edits:
        if out.count(old) != 1:
            return "BAD", f"the old text occurs {out.count(old)} times: {old[:60]!r}", 0.0
        out = out.replace(old, new)
    with tempfile.TemporaryDirectory() as t:
        for sub in ("starter-kit", "tools", "bin"):
            (Path(t) / sub).mkdir()
        (Path(t) / "starter-kit" / "quality_ratchet.py").write_text(out, encoding="utf-8")
        shutil.copy(REPO / "tools" / "test_quality_ratchet.py", Path(t) / "tools")
        shutil.copy(REPO / "bin" / "check-handoff", Path(t) / "bin")
        started = time.time()
        p = subprocess.run([sys.executable, str(Path(t) / "tools" / "test_quality_ratchet.py"), "-f", *TESTS],
                           capture_output=True, text=True, cwd=t)
        killers = [m.group(1) for m in re.finditer(r"^(?:FAIL|ERROR): (\w+)", p.stderr, re.M)]
        return ("KILLED" if p.returncode else "SURVIVED"), (killers[0] if killers else ""), time.time() - started


def main():
    src = (REPO / "starter-kit" / "quality_ratchet.py").read_text(encoding="utf-8")
    ids = [a for a in sys.argv[1:] if a.startswith("M")]          # e.g. M12 M26: only those mutants
    for name, edits in MUTANTS:
        if ids and name.split()[0] not in ids:
            continue
        verdict, by, secs = run_one(src, edits)
        print(f"{verdict:8} {name}  ({secs:.0f} s)", flush=True)
        if by:
            print(f"           {'by' if verdict == 'KILLED' else '!'} {by}", flush=True)


if __name__ == "__main__":
    main()
