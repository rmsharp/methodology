#!/usr/bin/env python3
"""Which blocks of bin/tests.sh differ between the candidate and the fork's tip, and which of them touch bin/sync,
bin/status or bin/check-links (PR2 layer 6; the layer's `bin/tests.sh` hunks are the answer's first rows).

    python3 layer6-blocks.py <repo> <candidate-rev> <tip-rev>

Reads `bin/tests.sh` at each revision with `git show` and splits it at its `echo "== Test ..."` lines. Blocks are
paired by title once `Test <number>` references are normalised, so a block that only changed number (the tip's
numbering runs ahead of the candidate's by the blocks the candidate does not carry) pairs. A block the candidate
carries under a DIFFERENT title (the context-budget block, the `--source=github` clone block) is listed on both sides
as unpaired: a title match is not a pairing, and the two are named in the record. Prints, per differing pair, the
added and removed line counts; per unpaired block, its size and how many lines call the three tools.
"""
import re
import subprocess
import sys

TOOLS = re.compile(r'\$BIN/(sync|status|check-links)\b|bin/(sync|status|check-links)\b')


def blocks(repo, rev):
    text = subprocess.run(["git", "-C", repo, "show", "%s:bin/tests.sh" % rev], check=True,
                          capture_output=True).stdout.decode("utf-8").split("\n")
    idx = [i for i, s in enumerate(text) if re.match(r'^echo "== Test ', s)]
    out = {}
    for k, i in enumerate(idx):
        j = idx[k + 1] if k + 1 < len(idx) else len(text)
        m = re.match(r'^echo "== Test ([0-9a-z\']*):? ?(.*?) =="', text[i])
        title = re.sub(r"Test \d+", "Test N", m.group(2))
        out[title] = (m.group(1) or "-", text[i:j])
    return out


def churn(a, b):
    import difflib
    added = removed = 0
    for line in difflib.unified_diff(a, b, n=0, lineterm=""):
        if line.startswith("+") and not line.startswith("+++"):
            added += 1
        elif line.startswith("-") and not line.startswith("---"):
            removed += 1
    return added, removed


def main():
    repo, cand_rev, tip_rev = sys.argv[1:4]
    cand, tip = blocks(repo, cand_rev), blocks(repo, tip_rev)
    print("candidate %s: %d blocks; tip %s: %d blocks" % (cand_rev, len(cand), tip_rev, len(tip)))
    paired = [t for t in tip if t in cand]
    print("\npaired by title: %d; identical: %d" % (len(paired), sum(1 for t in paired if cand[t][1] == tip[t][1])))
    print("\ndiffering pairs (candidate no. / tip no.: +added -removed, lines calling bin/sync, bin/status, bin/check-links in the tip's block)")
    for t in paired:
        if cand[t][1] != tip[t][1]:
            a, r = churn(cand[t][1], tip[t][1])
            calls = sum(1 for line in tip[t][1] if TOOLS.search(line))
            print("  %-4s/ %-4s +%-4d -%-4d calls %-3d %s" % (cand[t][0], tip[t][0], a, r, calls, t[:88]))
    print("\nunpaired, in the tip only (tip no.: lines, lines calling the three tools)")
    for t in tip:
        if t not in cand:
            calls = sum(1 for line in tip[t][1] if TOOLS.search(line))
            print("  %-4s %4d lines, calls %-3d %s" % (tip[t][0], len(tip[t][1]), calls, t[:88]))
    print("\nunpaired, in the candidate only (candidate no.: lines)")
    for t in cand:
        if t not in tip:
            print("  %-4s %4d lines  %s" % (cand[t][0], len(cand[t][1]), t[:88]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
