#!/usr/bin/env python3
"""BL-103 repair 3 (S307): mutate bin/check-handoff's new gate-citation lint and run the gate-citation block of
bin/tests.sh against each mutant. Usage, from the repository root:
    python3 -I docs/planning/bl103-evidence/mutate-repair3.py <tests-ref> [M-ids...]
<tests-ref> is the commit whose bin/tests.sh supplies the block (round 1: 5cb11a6; round 2: HEAD), or WORKTREE for the file on disk. The mutants are
applied to a copy of bin/check-handoff at HEAD, in a temporary directory; nothing in the working tree changes."""
import os, shutil, subprocess, sys, tempfile

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
REF = sys.argv[1]
ONLY = sys.argv[2:]

def block(ref):
    if ref == "WORKTREE":
        t = open(os.path.join(ROOT, "bin", "tests.sh"), encoding="utf-8").read().split("\n")
    else:
        t = subprocess.run(["git", "show", f"{ref}:bin/tests.sh"], capture_output=True, text=True, cwd=ROOT, check=True).stdout.split("\n")
    def idx(prefix, start=0):
        return next(i for i in range(start, len(t)) if t[i].startswith(prefix))
    s = idx("# D9: check-handoff")
    e = idx('rm -rf "$P"', s)
    gh = idx("good_handoff() {")
    rc = idx("receipt() {")
    head = ["#!/usr/bin/env bash", "set -uo pipefail",
            f'BIN="$BIN_OVERRIDE"; METHODOLOGY={ROOT}; STARTER=$METHODOLOGY/starter-kit', "PASS=0; FAIL=0; SKIP=0"]
    head += [l for l in t[:40] if l.startswith(("pass()", "fail()", "skip()"))]
    return "\n".join(head + t[gh:gh + 21] + t[rc:rc + 3] + t[s:e + 1] + ['echo "PASS=$PASS FAIL=$FAIL"']) + "\n"

SRC = open(os.path.join(ROOT, "bin", "check-handoff"), encoding="utf-8").read()
M = [
 ("M1", ">= instead of >", "    if owed > named:", "    if owed >= named:"),
 ("M2", "slack of one name", "    if owed > named:", "    if owed > named + 1:"),
 ("M3", "min over citations", "owed = max((int(n)", "owed = min((int(n)"),
 ("M4", "min over clauses", "named = max((len(re.split", "named = min((len(re.split"),
 ("M6", "\\s across fields (clause)", 'UNMEASURED_CLAUSE_RE = re.compile(r"unmeasured:[ \\t]*("', 'UNMEASURED_CLAUSE_RE = re.compile(r"unmeasured:\\s*("'),
 ("M7", "drop the fail group", '(?:[ \\t]*·[ \\t]*\\d+[ \\t]+fail)?[ \\t]*·[ \\t]*(\\d+)', '[ \\t]*·[ \\t]*(\\d+)'),
 ("M8", "no backticks in names", '_GATE_NAME = r"`?[A-Za-z0-9][A-Za-z0-9_.-]*`?"', '_GATE_NAME = r"[A-Za-z0-9][A-Za-z0-9_.-]*"'),
 ("M12", "any name satisfies", "    if owed > named:", "    if owed > 0 and named == 0:"),
 ("M13", "citation count from runtime_smoke only", "owed = max((int(n) for n in GATE_UNMEASURED_RE.findall(haystack)), default=0)", 'owed = max((int(n) for n in GATE_UNMEASURED_RE.findall(fields.get("runtime_smoke", ""))), default=0)'),
 ("M14", "first citation only", "GATE_UNMEASURED_RE.findall(haystack)), default=0)", "GATE_UNMEASURED_RE.findall(haystack)[:1]), default=0)"),
 ("M15", "one-digit count", "[ \\t]*·[ \\t]*(\\d+)[ \\t]+unmeasured\")", "[ \\t]*·[ \\t]*(\\d)[ \\t]+unmeasured\")"),
 ("M16", "clause search in runtime_smoke only", "for names in UNMEASURED_CLAUSE_RE.findall(haystack)", 'for names in UNMEASURED_CLAUSE_RE.findall(fields.get("runtime_smoke", ""))'),
 ("M17", "name must start with a letter", '_GATE_NAME = r"`?[A-Za-z0-9]', '_GATE_NAME = r"`?[A-Za-z]'),
 ("M18", "pending receipt judged", '    if declared <= 0 or fields.get("status", "").strip() != "complete":', "    if declared <= 0:"),
 ("M20", "declared guard off by one", '    if declared <= 0 or fields.get("status", "").strip() != "complete":', '    if declared < 0 or fields.get("status", "").strip() != "complete":'),
 ("M21", "a missing clause counts as one name", "default=0)\n    if owed > named:", "default=1)\n    if owed > named:"),
 ("M23", "the lint is off", "    if owed > named:", "    if False:"),
 ("M22", "a clause always counts one name", 'len(re.split(r"[ \\t]*,[ \\t]*", names))', "1"),
]
work = tempfile.mkdtemp(prefix="mut-repair3-")
open(os.path.join(work, "block.sh"), "w", encoding="utf-8").write(block(REF))
killed = survived = 0
for mid, name, a, b in M:
    if ONLY and mid not in ONLY:
        continue
    if SRC.count(a) < 1:
        print(mid, name, "ANCHOR-MISSING"); continue
    d = os.path.join(work, "bin"); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    for f in os.listdir(os.path.join(ROOT, "bin")):
        p = os.path.join(ROOT, "bin", f)
        if os.path.isfile(p):
            shutil.copy2(p, os.path.join(d, f))
    open(os.path.join(d, "check-handoff"), "w", encoding="utf-8").write(SRC.replace(a, b, 1))
    r = subprocess.run(["bash", os.path.join(work, "block.sh")], capture_output=True, text=True, env=dict(os.environ, BIN_OVERRIDE=d))
    fails = sum(1 for l in r.stdout.splitlines() if "FAIL:" in l)
    ok = fails == 0 and any(l.startswith("PASS=") and l.endswith("FAIL=0") for l in r.stdout.splitlines())
    killed += (not ok); survived += ok
    print(mid, name, "SURVIVED" if ok else f"KILLED by {fails} row(s)")
base = subprocess.run(["bash", os.path.join(work, "block.sh")], capture_output=True, text=True, env=dict(os.environ, BIN_OVERRIDE=os.path.join(ROOT, "bin")))
print("unmutated block at", REF + ":", [l for l in base.stdout.splitlines() if l.startswith("PASS=")][-1])
print(f"killed {killed}, survived {survived}, of {killed + survived}")
shutil.rmtree(work, ignore_errors=True)
