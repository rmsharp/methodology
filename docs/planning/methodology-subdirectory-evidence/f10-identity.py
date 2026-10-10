#!/usr/bin/env python3
"""BL-101 F10 and F11 verification (S290): the scan did not change, only what it files and one file it now reads.

For each clone that f5-population.py left, run the tool as it was before F10 (a revision, given as the second argument) and as it
is now, and compare. Allowed to differ, and only in these two ways:
  F11  a file moved from `other` to `config` (a dot-file that ends in `ignore`, `.gitignore` apart): then `ledger`, `harness`,
       `ci`, `hooks`, `tests`, `proofs` and `scripts` are identical in mentions and files, and `config + other` is identical
       in mentions and files.
  F10  a `.Rbuildignore` row gained `patterns` (and, when it had no row, appeared in `config`): nothing else changes.
Anything else is printed as DIFFERENT and the exit code is 1. Read-only on the clones (a dry run writes nothing).
Usage: python3 -I f10-identity.py <the directory f5-population.py wrote> <the revision of the tool before F10>
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
pop = Path(sys.argv[1]) / "clones"
rev = sys.argv[2]
SAME = ("ledger", "harness", "ci", "hooks", "tests", "proofs", "scripts")
KINDMAP = {"test": "tests", "proof": "proofs", "script": "scripts", "config": "config", "ci": "ci", "hook": "hooks"}
SURVEY = REPO / "docs/planning/methodology-subdirectory-evidence/s286-adopter-survey-output.txt"


def survey_rows():
    """The S286 survey's strong-name candidates, by adopter: the same parse f5-population.py makes."""
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

old_home = Path(tempfile.mkdtemp(prefix="f10-oldtool-"))
(old_home / "bin").mkdir()
old = subprocess.run(["git", "-C", str(REPO), "show", rev + ":bin/migrate-layout"], capture_output=True, text=True, check=True).stdout
(old_home / "bin" / "migrate-layout").write_text(old, encoding="utf-8")
for name in ("_manifest.py", "_manifest_reader.py", "status", "sync", "check-links", "check-ledger", "check-handoff"):
    if (REPO / "bin" / name).exists():
        (old_home / "bin" / name).symlink_to(REPO / "bin" / name)
for name in ("starter-kit", "tools", "docs"):
    (old_home / name).symlink_to(REPO / name)


def report(tool, clone):
    r = subprocess.run([sys.executable, "-B", str(tool), str(clone), "--json"], capture_output=True, text=True)
    return json.loads(r.stdout)


def files(nr, cat):
    return {x["file"] for x in nr[cat]["paths"]}


bad = 0
patterned = moved = 0
survey = survey_rows()
want_all = got_all = 0
for clone in sorted(pop.iterdir()):
    o, n = report(old_home / "bin" / "migrate-layout", clone), report(REPO / "bin" / "migrate-layout", clone)
    if o["status"] == "refused" or n["status"] == "refused":
        print("%-26s refused (old %s, new %s)" % (clone.name, o["status"], n["status"]))
        continue
    o, n = o["not_rewritten"], n["not_rewritten"]
    same = all((o[c]["mentions"], o[c]["files"]) == (n[c]["mentions"], n[c]["files"]) for c in SAME)
    # every row of the unchanged kinds is identical too, not only their totals
    rows = all(o[c]["paths"] == n[c]["paths"] and o[c]["sites"] == n[c]["sites"] for c in SAME)
    mentions = {x["file"]: x["mentions"] for x in n["config"]["paths"]}
    to_config = sorted(f for f in files(n, "config") - files(o, "config") if mentions[f] > 0)
    pattern_rows = [x["file"] for x in n["config"]["paths"] if "patterns" in x]
    pattern_only = [x["file"] for x in n["config"]["paths"] if x["mentions"] == 0 and x["file"] not in files(o, "config")]
    both = (n["config"]["mentions"] + n["other"]["mentions"], n["config"]["files"] + n["other"]["files"] - len(pattern_only))
    was = (o["config"]["mentions"] + o["other"]["mentions"], o["config"]["files"] + o["other"]["files"])
    ok = same and rows and both == was
    bad += not ok
    patterned += len(pattern_rows)
    moved += len(to_config)
    # the S286 candidates: a file is listed when it has a mention on a code line or its patterns stop matching
    listed = {(c, x["file"]) for c in ("ci", "hooks", "tests", "proofs", "scripts", "config") for x in n[c]["paths"]
              if x["code_mentions"] > 0 or x.get("patterns")}
    want = survey.get(clone.name, set())
    want_all += len(want)
    got_all += len(want & listed)
    extra = "  S286 candidates %d, listed %d" % (len(want), len(want & listed))
    for gone in sorted(want - listed):
        extra += "  MISSING %s" % (gone,)
    if pattern_rows:
        p = next(x for x in n["config"]["paths"] if "patterns" in x)["patterns"]
        extra += "  patterns: %s %d line(s), %d moved file(s), %d unread" % (pattern_rows, len(p["lines"]), len(p["exposed"]), p["unread"])
    if to_config:
        extra += "  other->config: %s" % to_config
    print("%-26s unchanged kinds same=%s rows same=%s  config+other %s -> %s  %s%s" % (
        clone.name, same, rows, was, both, "OK" if ok else "DIFFERENT", extra))
print("clones that differ: %d; clones with a patterns row: %d; files moved other->config: %d; S286 candidates listed: %d of %d"
      % (bad, patterned, moved, got_all, want_all))
sys.exit(1 if bad else 0)
