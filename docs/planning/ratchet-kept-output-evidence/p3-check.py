#!/usr/bin/env python3
"""p3-check.py -- the declared expectations of P3 (docs/planning/ratchet-kept-output-plan.md, section 6).

Usage: python3 -I p3-check.py <work-dir> run1|run2

Reads what a finished run left in <work-dir> (<tag>.out, .err, .done) and in the clone <work-dir>/methodology, and
prints one line per expectation: `ok` or `FAIL`. Exit 0 only if every expectation holds. It changes nothing in the
clone except that `run1` writes three files into <work-dir> (run1.results.json, run1.kept.sha256, run1.kept.stat)
for `run2` to compare against.

run1: the deliberate failure was injected, then `--run` once.       (plan 6, P3, items 1 and 3)
run2: the injection was removed, then `--run` a second time.         (plan 6, P3, item 2)

The plan was written for 25 gates; the manifest holds 26 since S449 (`seed-handoffs-size`), so the counts below are
26 / 25 pass / 1 fail for the first run and 26 / 26 for the second. A reader that passes with nothing there is the
failure this file is built against: it is run once BEFORE any run (every line must read FAIL), and run2 is run against
run1's end state (it must read FAIL there too).
"""
import hashlib
import json
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True
if len(sys.argv) != 3 or sys.argv[2] not in ("run1", "run2"):
    sys.exit(__doc__)
WORK, MODE = os.path.abspath(sys.argv[1]), sys.argv[2]
CLONE = os.path.join(WORK, "methodology")
RESULTS = os.path.join(CLONE, ".quality-gates-results.json")
KEPT = os.path.join(CLONE, ".quality-gates-output")
ANSI = re.compile(r"\x1b\[[0-9;]*m")
SUITE_BYTES = 59382   # the plan's [E2]: one real suite run's stdout; the kept section must be within 5% of it
FAILS = []


def expect(ok, label, detail=""):
    print(f"  {'ok  ' if ok else 'FAIL'} {label}" + (f"  [{detail}]" if detail else ""))
    if not ok:
        FAILS.append(label)


def read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def sha256_of(path):
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return None


def git(*args):
    p = subprocess.run(["git", *args], cwd=CLONE, capture_output=True, text=True)
    return p.returncode, p.stdout


def status_output():
    p = subprocess.run([sys.executable, "-B", "starter-kit/quality_ratchet.py", "--status"], cwd=CLONE,
                       capture_output=True, text=True)
    return p.returncode, ANSI.sub("", p.stdout)


def kept_files():
    out = []
    for folder in sorted(os.listdir(KEPT)) if os.path.isdir(KEPT) else []:
        path = os.path.join(KEPT, folder)
        if os.path.isdir(path):
            out += [(folder, n) for n in sorted(os.listdir(path))]
    return out


def gates_by_name(snap):
    return {g["name"]: g for g in snap["gates"]}


tag = MODE
done = read(os.path.join(WORK, tag + ".done"))
out = ANSI.sub("", read(os.path.join(WORK, tag + ".out")) or "")
err = read(os.path.join(WORK, tag + ".err"))
snap = None
try:
    snap = json.loads(read(RESULTS) or "")
except ValueError:
    pass
print(f"p3-check {MODE}: clone {CLONE}")
rc_head, head = git("rev-parse", "--short", "HEAD")
head = head.strip()

# ---- what both runs must show -------------------------------------------------------------------------------------
expect(done is not None, "the run finished (a done-file exists)", repr(done))
expect(snap is not None and len(snap.get("gates", [])) == 26, "the results file lists 26 gates")
expect(snap is not None and snap.get("version") == "1.6.0", "the results file was written by tool 1.6.0",
       str(snap and snap.get("version")))
expect(err == "", "the run wrote nothing to stderr (no keeper warning)", repr(err)[:80] if err else "")
g = gates_by_name(snap) if snap else {}
suite_passed, suite_failed = g.get("tests-sh-passed", {}), g.get("tests-sh-failed", {})

if MODE == "run1":
    expect((done or "").strip() == "2", "exit code 2 (a gate failed)", repr(done))
    expect(suite_failed.get("status") == "fail" and suite_failed.get("measured") == 1,
           "tests-sh-failed reads fail with 1", f"{suite_failed.get('status')} {suite_failed.get('measured')}")
    expect(suite_passed.get("status") == "pass" and suite_passed.get("measured") == 702,
           "tests-sh-passed reads pass at its floor, 702", f"{suite_passed.get('status')} {suite_passed.get('measured')}")
    s = (snap or {}).get("summary", {})
    expect(s.get("pass") == 25 and s.get("fail") == 1 and s.get("unmeasured") == 0,
           "the summary reads 25 pass, 1 fail, 0 unmeasured", json.dumps(s))
    others = {n: x for n, x in g.items() if not n.startswith("tests-sh-")}
    expect(len(others) == 24 and all(x["status"] == "pass" for x in others.values()),
           "the 24 gates that are not the suite all pass with the directory present",
           ", ".join(n for n, x in others.items() if x["status"] != "pass"))
    # the kept file
    kept = (snap or {}).get("kept")
    expect(isinstance(kept, dict) and list(kept) == ["tests-sh-failed"],
           "`kept` names exactly one gate, tests-sh-failed", json.dumps(kept))
    rel = (kept or {}).get("tests-sh-failed", "")
    m = re.match(r"^\.quality-gates-output/tests-sh-passed/(\d{8}T\d{6}Z)-([0-9a-f]+)\.txt$", rel)
    expect(bool(m), "its path is .quality-gates-output/tests-sh-passed/<UTC start>-<commit>.txt", rel)
    expect(bool(m) and m.group(2) == head, "the file name carries the clone's HEAD", f"{m and m.group(2)} vs {head}")
    path = os.path.join(CLONE, rel)
    text = read(path)
    expect(text is not None, "that file exists")
    text = text or ""
    lines = text.split("\n")
    expect(lines[:1] == ["quality-ratchet kept output"], "the header's first line")
    expect("gates: tests-sh-passed, tests-sh-failed" in lines, "the header names both gates over the shared command")
    expect("command: bash bin/tests.sh" in lines, "the header names the shared command")
    expect(any(re.match(r"^exit: 1   budget: 3600 s$", x) for x in lines), "the suite's exit status 1 and its 3600 s budget")
    mo = re.search(r"^stdout: (\d+) bytes, kept (\d+)$", text, re.M)
    n_out, k_out = (int(mo.group(1)), int(mo.group(2))) if mo else (0, 0)
    expect(bool(mo) and n_out == k_out, "stdout was kept whole (bytes equal bytes kept)", f"{n_out} / {k_out}")
    expect(bool(mo) and abs(n_out - SUITE_BYTES) <= SUITE_BYTES * 0.05,
           "stdout is within 5% of 59,382 bytes", f"{n_out} bytes, {100 * (n_out - SUITE_BYTES) / SUITE_BYTES:+.2f}%")
    expect("stderr: 0 bytes, kept 0" in lines, "stderr 0 bytes")
    expect(lines.count("  FAIL: kept-output proof: deliberate failure") == 1,
           "the injected failure line is in the kept file exactly once")
    expect(sum(1 for x in lines if x.startswith("  FAIL:")) == 1, "it is the only FAIL line in the kept file")
    expect("== Summary: 702 passed, 1 failed, 0 skipped ==" in lines, "the suite's own summary line")
    expect(text.count("=== stdout ===") == 1 and text.count("=== stderr ===") == 1, "one stdout and one stderr section")
    # the directory
    expect(read(os.path.join(KEPT, ".gitignore")) == "*\n", ".quality-gates-output/.gitignore holds `*`")
    files = kept_files()
    expect(files == [("tests-sh-passed", os.path.basename(rel))],
           "the directory holds one kept file in one gate folder, tests-sh-passed", str(files))
    # what the person sees
    base = os.path.realpath(KEPT)
    expect(f"kept output on disk: 1 file(s) in 1 gate folder(s) under {base}" in out
           or f"kept output on disk: 1 file(s) in 1 gate folder(s) under {KEPT}" in out,
           "`--run` printed the 'kept output on disk' line", "")
    expect(f"kept: tests-sh-failed  {os.path.join(KEPT, 'tests-sh-passed', os.path.basename(rel))}" in out
           or f"kept: tests-sh-failed  {os.path.join(base, 'tests-sh-passed', os.path.basename(rel))}" in out,
           "`--run` printed one 'kept:' line for tests-sh-failed with its absolute path")
    rc, st = status_output()
    expect("kept output on disk: 1 file(s) in 1 gate folder(s)" in st, "`--status` prints the 'kept output on disk' line")
    expect("kept: tests-sh-failed" in st, "`--status` prints the stored 'kept:' line")
    # the tree
    rc, por = git("status", "--porcelain")
    expect(por.splitlines() == [" M bin/tests.sh"], "git status --porcelain is only the injected edit", repr(por))
    # hand the state to run2
    if snap is not None:
        with open(os.path.join(WORK, "run1.results.json"), "w") as f:
            json.dump(snap, f, indent=1, sort_keys=True)
        if rel and os.path.isfile(path):
            with open(os.path.join(WORK, "run1.kept.sha256"), "w") as f:
                f.write(f"{sha256_of(path)}  {rel}\n")
            st_ = os.stat(path)
            with open(os.path.join(WORK, "run1.kept.stat"), "w") as f:
                f.write(f"{st_.st_size} {st_.st_mtime_ns}\n")
else:
    first = None
    try:
        first = json.loads(read(os.path.join(WORK, "run1.results.json")) or "")
    except ValueError:
        pass
    expect(first is not None, "run 1's results file was saved for comparison")
    expect((done or "").strip() == "0", "exit code 0", repr(done))
    s = (snap or {}).get("summary", {})
    expect(s.get("pass") == 26 and s.get("fail") == 0 and s.get("unmeasured") == 0,
           "the summary reads 26 pass, 0 fail, 0 unmeasured", json.dumps(s))
    expect(suite_passed.get("measured") == 702 and suite_failed.get("measured") == 0,
           "tests-sh-passed 702 and tests-sh-failed 0", f"{suite_passed.get('measured')} / {suite_failed.get('measured')}")
    expect(snap is not None and "kept" not in snap, "the results file has no `kept` key")
    # the first run's file
    line = (read(os.path.join(WORK, "run1.kept.sha256")) or "").strip()
    sha1, rel1 = (line.split("  ", 1) + [""])[:2] if line else ("", "")
    p1 = os.path.join(CLONE, rel1)
    expect(bool(sha1) and os.path.isfile(p1), "run 1's kept file is still there", rel1)
    expect(bool(sha1) and sha256_of(p1) == sha1, "and it is byte-identical (sha256 equal)", sha1[:12])
    st1 = (read(os.path.join(WORK, "run1.kept.stat")) or "").split()
    try:
        now = os.stat(p1)
        expect(st1 == [str(now.st_size), str(now.st_mtime_ns)], "its size and modification time are unchanged", " ".join(st1))
    except OSError:
        expect(False, "its size and modification time are unchanged")
    files = kept_files()
    expect(bool(rel1) and files == [("tests-sh-passed", os.path.basename(rel1))],
           "the directory still holds that one kept file and nothing new", str(files))
    expect(read(os.path.join(KEPT, ".gitignore")) == "*\n", ".quality-gates-output/.gitignore still holds `*`")
    # what the person sees now
    expect("kept output on disk: 1 file(s) in 1 gate folder(s)" in out, "`--run` printed the 'kept output on disk' line")
    expect("  kept: " not in out, "`--run` printed no 'kept:' line (nothing was kept in this run)")
    rc, st = status_output()
    expect("kept output on disk: 1 file(s) in 1 gate folder(s)" in st, "`--status` still prints the 'kept output on disk' line")
    expect("  kept: " not in st, "`--status` prints no 'kept:' line (the results file names none)")
    rc, por = git("status", "--porcelain")
    expect(por.strip() == "", "git status --porcelain is empty (the injection is gone)", repr(por))
    # the 24 other gates read as in run 1
    if first is not None and snap is not None:
        a = {n: (x["status"], x["measured"]) for n, x in gates_by_name(first).items() if not n.startswith("tests-sh-")}
        b = {n: (x["status"], x["measured"]) for n, x in g.items() if not n.startswith("tests-sh-")}
        diff = {n: (a.get(n), b.get(n)) for n in set(a) | set(b) if a.get(n) != b.get(n)}
        expect(len(b) == 24 and not diff, "the 24 other gates read the same in both runs (status and value)", json.dumps(diff))

print(f"p3-check {MODE}: {len(FAILS)} expectation(s) failed" if FAILS else f"p3-check {MODE}: all expectations hold")
sys.exit(1 if FAILS else 0)
