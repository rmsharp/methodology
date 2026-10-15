#!/usr/bin/env python3
"""i95-adopters.py -- upstream issue #95, finding 4: what would measuring `max_line_bytes` in bytes change
for the 12 adopters?

Usage:  python3 i95-adopters.py SCRATCH_DIR

Read-only on every adopter: each file is read with `git show HEAD:<path>` (the committed state, which is
what the 12 adopters' own checks run on after a pull), never from a working tree, so a live session in an
adopter cannot move the numbers while this runs. The HEAD it read is printed with each row.

For each adopter that declares `max_line_bytes` on a file, three counts of lines over the cap:
  chars   what the tool does today: decode with errors replaced, split on "\\n", len() in code points
  bytes   the exact byte length of each line (the raw bytes split on b"\\n")
  encode  the issue's suggested `len(l.encode("utf-8"))` on the decoded line
`flips` is bytes minus chars: lines that pass today and would fail after the fix. The two differ only
when a file has invalid UTF-8 (a replacement character is 1 character, 3 bytes encoded, 1 byte raw).

The instrument is audited against the tool itself: `measure_file` from the fork's starter-kit is run on a
copy of each file with the same cap, and its "N line(s) exceed" count must equal `chars`; a mismatch stops
the run.
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
REPO = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(REPO, ".git")):
    REPO = os.path.dirname(REPO)
DEV = os.path.expanduser("~/Development")

src = open(os.path.join(REPO, "docs/planning/pr-composition-evidence/pr3-adopters.py")).read()
ADOPTERS = re.findall(r'"([^"]+)"', re.search(r"ADOPTERS = \[(.*?)\]", src, re.S).group(1))
assert len(ADOPTERS) == 12, ADOPTERS


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    return p.returncode, p.stdout


def load_tool():
    spec = importlib.util.spec_from_file_location("cb", os.path.join(REPO, "starter-kit", "context_budget.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    scratch = os.path.abspath(sys.argv[1])
    if os.path.exists(scratch):
        shutil.rmtree(scratch)
    os.makedirs(scratch)
    cb = load_tool()
    print("i95-adopters.py: lines over `max_line_bytes`, characters (today) against bytes (the fix)\n")
    hdr = f"{'adopter':27} {'HEAD':8} {'file':36} {'cap':>5} {'chars':>6} {'bytes':>6} {'encode':>6} {'flips':>5}"
    print(hdr)
    print("-" * len(hdr))
    tot = {"declared": 0, "with_flips": 0, "flips": 0, "adopters": 0, "none": []}
    detail = []
    for name in ADOPTERS:
        repo = os.path.join(DEV, name)
        rc, head = git(repo, "rev-parse", "--short", "HEAD")
        if rc != 0:
            print(f"{name:27} {'-':8} (no commits yet: nothing at HEAD to read)")
            tot["none"].append(name + " (no commits)")
            continue
        head = head.decode().strip()
        cfg = None
        for p in (".context-budget.json", "methodology/.context-budget.json"):
            rc, b = git(repo, "show", f"HEAD:{p}")
            if rc == 0:
                cfg = json.loads(b)
                break
        rows = [(f["path"], f["max_line_bytes"]) for f in (cfg or {}).get("files", []) if "max_line_bytes" in f]
        if not rows:
            print(f"{name:27} {head:8} (no max_line_bytes declared at HEAD)")
            tot["none"].append(name)
            continue
        tot["adopters"] += 1
        for path, cap in rows:
            rc, data = git(repo, "show", f"HEAD:{path}")
            if rc != 0:
                print(f"{name:27} {head:8} {path:36} {cap:>5} (file not at HEAD)")
                continue
            text = data.decode("utf-8", "replace")
            tl = text.split("\n")
            chars = [i for i, l in enumerate(tl) if len(l) > cap]
            enc = [i for i, l in enumerate(tl) if len(l.encode("utf-8")) > cap]
            byt = [i for i, l in enumerate(data.split(b"\n")) if len(l) > cap]
            # audit against the tool's own measure_file, on a copy at the same relative path
            troot = os.path.join(scratch, name)
            dest = os.path.join(troot, path)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            open(dest, "wb").write(data)
            r = cb.measure_file(troot, {"path": path, "max_line_bytes": cap})
            m = [re.match(r"(\d+) line\(s\) exceed", f["msg"]) for f in r["findings"] if f["kind"] == "line_bytes"]
            tool_n = int(m[0].group(1)) if m and m[0] else 0
            if tool_n != len(chars):
                sys.exit(f"INSTRUMENT MISMATCH {name} {path}: tool says {tool_n} lines over, this script counts {len(chars)}")
            flips = sorted(set(byt) - set(chars))
            tot["declared"] += 1
            tot["flips"] += len(flips)
            tot["with_flips"] += 1 if flips else 0
            print(f"{name:27} {head:8} {path:36} {cap:>5} {len(chars):>6} {len(byt):>6} {len(enc):>6} {len(flips):>5}")
            for i in flips:
                l = tl[i]
                detail.append((name, path, i + 1, len(l), len(data.split(b"\n")[i]), sum(1 for ch in l if ord(ch) > 127)))
    print("\nRows where the fix would turn a passing line into an over-cap line (line, characters, bytes, non-ASCII characters):")
    if not detail:
        print("  none")
    for name, path, ln, c, b, na in detail:
        print(f"  {name}: {path}:{ln}  {c} chars -> {b} B  ({na} non-ASCII)")
    print(f"\nTotals: {tot['adopters']} of 12 adopters declare the cap ({', '.join(tot['none'])} do not); "
          f"{tot['declared']} files measured; {tot['with_flips']} would gain at least one over-cap line; "
          f"{tot['flips']} lines would flip. The tool's own measure_file agreed with the character count on every file.")


if __name__ == "__main__":
    main()
