"""Apply one textual mutation at a time to a file, run the named test classes, restore the file.

Usage: python3 -I mutate.py <worktree> <spec.json>
spec.json: {"file": "starter-kit/methodology_trim.py", "tests": ["ClassA", "ClassB"],
            "mutants": [{"name": "...", "old": "...", "new": "..."}, ...]}
A mutant is KILLED when the targeted tests fail (exit != 0) and SURVIVED when they pass. Each `old`
must occur exactly once. The file is restored byte for byte after every mutant, and a final check
asserts that.
"""
import json
import pathlib
import subprocess
import sys

wt = pathlib.Path(sys.argv[1])
spec = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"))
target = wt / spec["file"]
original = target.read_bytes()
text = original.decode("utf-8")
results = []
try:
    for m in spec["mutants"]:
        assert text.count(m["old"]) == 1, "%s: expected one match, found %d" % (m["name"], text.count(m["old"]))
        target.write_text(text.replace(m["old"], m["new"]), encoding="utf-8")
        r = subprocess.run([sys.executable, "-B", "tools/test_methodology_trim.py"] + spec["tests"],
                           cwd=str(wt), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        killed = r.returncode != 0
        first = next((ln for ln in r.stdout.splitlines() if ln.startswith(("FAIL:", "ERROR:"))), "")
        results.append((m["name"], killed, first[:150]))
        print("%-9s %s   %s" % ("KILLED" if killed else "SURVIVED", m["name"], first[:150]), flush=True)
finally:
    target.write_bytes(original)
assert target.read_bytes() == original, "the file was not restored"
print("restored; %d mutants, %d killed, %d survived" % (
    len(results), sum(1 for r in results if r[1]), sum(1 for r in results if not r[1])))
