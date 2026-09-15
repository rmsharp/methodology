#!/usr/bin/env python3
"""PR #80 review F3 -- every answer measured before one was chosen (S165, 2026-09-15).

The review's F3: `python3 starter-kit/context_budget.py --status` printed OVER at the head -- the
Phase 0 pair the headline says fits, and both ledgers -- and wired as a gate it would have refused
every ledger append. It offered three answers; this fork added a fourth. Each is built here as a
variant of the ROOT `.context-budget.json` and run through `--status` and six staged commits via
`--precommit`, on two trees: the F2 branch head, and that head merged into `upstream/main`.

Reproduce (the clones are scratch; this script resets them after every variant and asserts it):

    R=/path/to/this/checkout
    git clone --no-local -q -b pr80/f2-installed-source-guard "$R" /tmp/f3-base      # 37740763
    git clone --no-local -q -b pr80/f2-installed-source-guard "$R" /tmp/f3-merge
    git -C /tmp/f3-merge fetch -q "$R" refs/remotes/upstream/main:refs/remotes/upstream/main
    git -C /tmp/f3-merge merge -q --no-edit upstream/main                              # 9fa3141
    python3 docs/planning/pr80-f3-variants.py /tmp/f3-base /tmp/f3-merge

The densities in V-i were measured by the doubled-file method (Read a multi-copy file with a
spanning `limit`; divide the refusal's token count by the copy count), on the blobs the merge
produces: runner c0550acd x2 -> 36,955 tok (2.8248 B/tok); SAFEGUARDS.md 656beae7 x7 -> 40,605
(2.8191). The same method on this branch's pair x2 gave 47,805, the figure the PR description
records, before either number was trusted.

Recorded results (exit of --status; then which staged commits --precommit refused):

    V0           current config          2 OVER, both trees  every ledger append; any read-set growth
    V-ii-literal ledgers pinned at size  2 OVER              every ledger append (the pin); any
                                                             read-set growth. The ledgers stay over
                                                             via the token arm: token_ceiling()
                                                             clamps a whole-read file to 25,000
    V-ii-reclass ledgers on-demand at    2 OVER (read-set)   read-set growth only; appends pass
                 196,608 B
    V-iv         ledgers dropped         2 OVER (read-set)   read-set growth only; appends pass
    V-i-a        read-set in tokens,     2 OVER (ledgers)    every ledger append; runner +2,100 B;
                 class ceiling removed                       SAFEGUARDS +100 B on the merge only
                                                             (pinned at 16,353 B)
    V-i-c        as V-i-a, class typed   2 OVER (ledgers)    the same, plus the typed class arm
                 at 70,587 B
    V-iii        byte ceilings kept,     2 OVER              every ledger append; any read-set
                 re-pinned for the merge                     growth; the runner's derived token
                                                             arm also reads 17 over
    R1 L1        V-i-a + V-iv  (CHOSEN)  0 OK, both trees    runner +2,100 B; SAFEGUARDS +100 B on
                                                             the merge
    R1 L2        V-i-a + V-ii-reclass    0 OK, both trees    the same

The chosen config (R1 L1) was then hand-written into the branch, preserving the file's layout, and
re-run from the edited file itself: identical results. That commit is aa36fd8b on branch
pr80/f3-read-set-token-ceilings. Record: docs/planning/pr80-review-response.md section 5.
"""
import json
import os
import re
import subprocess
import sys

ANSI = re.compile(r"\x1b\[[0-9;]*m")
LEDGERS = ("CHANGELOG.md", "HANDOFFS.md")
RUN, SAFE = "starter-kit/SESSION_RUNNER.md", "starter-kit/SAFEGUARDS.md"
SCENARIOS = [("CHANGELOG +300", "CHANGELOG.md", 300), ("HANDOFFS +300", "HANDOFFS.md", 300),
             ("runner +100", RUN, 100), ("runner +2100", RUN, 2100),
             ("safeguards +100", SAFE, 100), ("runner -100", RUN, -100)]


def sh(cmd, cwd):
    p = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
    return p.returncode, ANSI.sub("", p.stdout + p.stderr)


def v0(c, cwd):
    return c


def v2_literal(c, cwd):
    for f in c["files"]:
        if f["path"] in LEDGERS:
            f["max_bytes"] = os.path.getsize(os.path.join(cwd, f["path"]))
            f.pop("max_tokens", None)
    return c


def v2_reclass(c, cwd):
    for f in c["files"]:
        if f["path"] in LEDGERS:
            f["class"] = "on-demand"
            f["max_bytes"] = 196608
            f.pop("max_tokens", None)
    return c


def v4(c, cwd):
    c["files"] = [f for f in c["files"] if f["path"] not in LEDGERS]
    return c


def _tokens_per_file(c):
    for f in c["files"]:
        if f["path"] == RUN:
            f.pop("max_bytes", None)
            f.update(max_tokens=19200, bytes_per_token=2.8248, measured_bytes=52195)
        if f["path"] == SAFE:
            f.pop("max_bytes", None)
            f.update(max_tokens=5800, bytes_per_token=2.8191, measured_bytes=16353)
    return c


def v1_a(c, cwd):
    c = _tokens_per_file(c)
    for k in ("total_bytes", "derive_from_read_cap", "warn_bytes"):
        c["classes"]["read-set"].pop(k, None)
    return c


def v1_c(c, cwd):
    c = _tokens_per_file(c)
    rs = c["classes"]["read-set"]
    rs.pop("derive_from_read_cap", None)
    rs.pop("warn_bytes", None)
    rs["total_bytes"] = int(25000 * 2.8235)   # the merged pair's measured density
    return c


def v3_repinned(c, cwd):
    for f in c["files"]:
        if f["path"] == SAFE:
            f["max_bytes"] = 16353
        if f["path"] == RUN:
            f["max_bytes"] = 56750 - 16353
    return c


VARIANTS = [("V0", v0), ("V-ii-literal", v2_literal), ("V-ii-reclass", v2_reclass), ("V-iv", v4),
            ("V-i-a", v1_a), ("V-i-c", v1_c), ("V-iii", v3_repinned),
            ("R1 L1 (chosen)", lambda c, cwd: v4(v1_a(c, cwd), cwd)),
            ("R1 L2", lambda c, cwd: v2_reclass(v1_a(c, cwd), cwd))]


def run(label, cwd, name, fn):
    sh("git reset -q --hard HEAD && git clean -fdq", cwd)
    base = sh("git rev-parse --short=8 HEAD", cwd)[1].strip()
    cfgp = os.path.join(cwd, ".context-budget.json")
    with open(cfgp, encoding="utf-8") as fh:          # read, THEN open for writing
        cfg = json.load(fh)
    with open(cfgp, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(fn(cfg, cwd), indent=2, ensure_ascii=False) + "\n")
    changed = sh("git add .context-budget.json && git commit -q --no-verify -m variant", cwd)[0] == 0
    rc, out = sh("python3 starter-kit/context_budget.py --status", cwd)
    head = re.search(r"context budget\s+(\S+)", out)
    print(f"\n=== {name} on {label} ({base}) -- --status exit {rc}, {head.group(1) if head else '?'}")
    for line in out.splitlines():
        if re.search(r"\b(ok|over|warn)\s*$", line) or "read-set total" in line:
            print("   " + line.rstrip())
    sh("rm -f .context-budget-history.jsonl", cwd)
    for slabel, path, delta in SCENARIOS:
        p = os.path.join(cwd, path)
        with open(p, "rb") as fh:
            data = fh.read()
        with open(p, "wb") as fh:
            fh.write(data + b"x" * (delta - 1) + b"\n" if delta > 0 else data[:delta])
        sh(f"git add {path}", cwd)
        prc, pout = sh("python3 starter-kit/context_budget.py --precommit", cwd)
        print(f"   precommit {slabel:16s} exit {prc}  {'REFUSED' if 'REFUSED' in pout else 'passed'}")
        sh("git reset -q --hard HEAD", cwd)
    if changed:
        sh("git reset -q --hard HEAD~1", cwd)
    sh("git clean -fdq", cwd)
    assert sh("git rev-parse --short=8 HEAD", cwd)[1].strip() == base, "clone left off its base"


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    for label, cwd in (("branch", sys.argv[1]), ("merged", sys.argv[2])):
        for name, fn in VARIANTS:
            run(label, cwd, name, fn)
    return 0


if __name__ == "__main__":
    sys.exit(main())
