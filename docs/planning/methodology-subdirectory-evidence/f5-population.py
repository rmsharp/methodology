#!/usr/bin/env python3
"""BL-101 F5 verification (S289): the tool's new lists against the S286 survey, over the real adopters.

For each adopter at the revision S286 pinned: clone --no-local, check out the rev, run bin/migrate-layout as a DRY RUN
(after bin/sync in the CLONE if the tool refuses with not-current, as P7's script did), keep the JSON report, and compare
the files the tool lists under a machine-read kind with a mention on a code line against the survey's strong-name
candidates (s286-adopter-survey-output.txt). Nothing is written in a real adopter. Usage (from anywhere): python3 -I f5-population.py <an empty output directory>
The clones and one JSON report per adopter are left in that directory.
"""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
DEV = Path.home() / "Development"
OUT = Path(sys.argv[1])
PINS = {"airqino": "998cd51", "chat_verification": "107cbed", "church_growth": "3035560", "dalia_martinez_funeral": "5cd7b91",
        "feedback-loop-comparison": "cda76db", "mts-system": "d1cf54f", "nprcgenekeepr": "6302757", "Philippians": "427e634",
        "vscode_quarto_ext": "507b934", "wsfct": "adba306"}
KINDMAP = {"test": "tests", "proof": "proofs", "script": "scripts", "config": "config", "ci": "ci", "hook": "hooks"}
MACHINE = ("ci", "hooks", "tests", "proofs", "scripts", "config")
SURVEY = REPO / "docs/planning/methodology-subdirectory-evidence/s286-adopter-survey-output.txt"
TRAILER = "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"


def sh(args, cwd=None):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def survey_rows():
    rows, label = {}, None
    for line in SURVEY.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^== (\S+?)@\S+\s+rev", line)
        if m:
            label = m.group(1)
            rows[label] = set()
            continue
        if line.startswith("== "):
            label = None
            continue
        m = re.match(r"^\s+\[(\w+)\s*\]\s+S\s+(\S+)\s+strong=", line)
        if m and label:
            rows[label].add((KINDMAP[m.group(1)], m.group(2)))
    return rows


def dry_run(clone):
    code, out = sh([sys.executable, "-B", str(REPO / "bin/migrate-layout"), str(clone), "--json"])
    try:
        return code, json.loads(out)
    except ValueError:
        return code, {"status": "unreadable", "refusals": [{"code": "unreadable", "message": out[-300:]}], "not_rewritten": {}}


def one(name, rev, work):
    clone = work / name
    code, out = sh(["git", "clone", "-q", "--no-local", str(DEV / name), str(clone)])
    if code:
        return None, "clone failed: " + out[-200:], []
    sh(["git", "-C", str(clone), "checkout", "-q", rev])
    for k, v in (("user.email", "f5@example.com"), ("user.name", "F5 evidence"), ("commit.gpgsign", "false")):
        sh(["git", "-C", str(clone), "config", k, v])
    code, rep = dry_run(clone)
    notes = []
    if any(r["code"] == "not-current" for r in rep["refusals"]):
        c1, o1 = sh([sys.executable, "-B", str(REPO / "bin/sync"), str(clone)])
        if c1:
            c1, o1 = sh([sys.executable, "-B", str(REPO / "bin/sync"), str(clone), "--force"])
            notes.append("sync needed --force")
        notes.append("synced in the clone (exit %s)" % c1)
        sh(["git", "-C", str(clone), "add", "-A"])
        sh(["git", "-C", str(clone), "commit", "-q", "--no-verify", "-m", "sync\n\n" + TRAILER])
        code, rep = dry_run(clone)
    return rep, "; ".join(notes), notes


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    work = OUT / "clones"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    survey = survey_rows()
    total_missing = total_extra = 0
    for name, rev in PINS.items():
        rep, note, _ = one(name, rev, work)
        if rep is None:
            print("%-26s %s" % (name, note))
            continue
        (OUT / (name + ".json")).write_text(json.dumps(rep, indent=1), encoding="utf-8")
        if rep["status"] == "refused":
            print("%-26s REFUSED %s %s" % (name, [r["code"] for r in rep["refusals"]], note))
            continue
        nr = rep["not_rewritten"]
        tool = {(c, x["file"]) for c in MACHINE for x in nr[c]["paths"] if x["code_mentions"] > 0}
        tool_all = {(c, x["file"]) for c in MACHINE for x in nr[c]["paths"]}
        want = survey.get(name, set())
        missing = sorted(want - tool)
        extra = sorted(tool - want)
        total_missing += len(missing)
        total_extra += len(extra)
        counts = " ".join("%s=%d" % (c, nr[c]["files"]) for c in CATS(nr))
        print("%-26s status=%s survey=%d tool(code-line)=%d tool(all)=%d missing=%d extra=%d  %s %s" % (
            name, rep["status"], len(want), len(tool), len(tool_all), len(missing), len(extra), counts, note))
        for m in missing:
            print("    MISSING from the tool:", m)
        for x in extra:
            print("    EXTRA in the tool:    ", x)
    print("TOTAL missing %d, extra %d" % (total_missing, total_extra))


def CATS(nr):
    return [c for c in ("ci", "hooks", "tests", "proofs", "scripts", "config", "harness", "other") if c in nr]


if __name__ == "__main__":
    main()
