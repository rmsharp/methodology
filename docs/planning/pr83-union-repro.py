#!/usr/bin/env python3
"""Re-runnable evidence for the D4 position in pr83-decisions-review.md (upstream PR #83, `merge=union`).

Question: does git's built-in `merge=union` driver keep two records prepended at one anchor WHOLE, as
the plan's D4 says ("it keeps both whole (in practice ours above theirs)")?

Every input comes from upstream's own history, so this runs in KJ5HST/methodology as well as in the
fork. The real-content cases rebuild the Shape B scenario the plan targets: sessions S23 and S24
both claiming from the same base `64f23bf`. In upstream's actual history S24 was cut from `6b29d3d`,
which already contains S23, so the two never met. Here:

    base   = 64f23bf:<ledger>
    ours   = 6b29d3d:<ledger>                                   (base + S23's inserted block)
    theirs = 219fb9d:<ledger> with S23's inserted block removed (base + S24's inserted block)

Both inserted blocks are pure insertions at the same anchor (checked below, not assumed). Each case
is merged twice, without and with the attribute, in a throwaway repository under a scratch
directory. Nothing is written into the repository this is run from.

Usage (from the repository root):
    git fetch <upstream-remote> refs/pull/83/head    # 219fb9d, if it is not already present
    python3 docs/planning/pr83-union-repro.py [SCRATCH_DIR]

Requires git and python3 only. It was written against git 2.50.1; the version in use is printed.
"""
import os
import subprocess
import sys
import tempfile

BASE, S23_TIP, S24_TIP = "64f23bf", "6b29d3d", "219fb9d"
REPO = os.getcwd()
CHECK_HANDOFF = os.path.join(REPO, "bin", "check-handoff")


def git(*args, cwd=None, check=True):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed ({r.returncode}): {r.stderr.strip()}")
    return r


def show(ref, path):
    return git("show", f"{ref}:{path}", cwd=REPO).stdout


def inserted_block(before, after):
    """The one contiguous run of lines `after` adds to `before`; fail if the change is anything else."""
    b, a = before.splitlines(keepends=True), after.splitlines(keepends=True)
    i = 0
    while i < len(b) and b[i] == a[i]:
        i += 1
    j = 0
    while j < len(b) - i and b[len(b) - 1 - j] == a[len(a) - 1 - j]:
        j += 1
    if i + j != len(b):
        sys.exit("not a pure insertion: the reconstruction below would not be faithful")
    return a[i:len(a) - j]


def remove_run(text, run):
    lines = text.splitlines(keepends=True)
    for k in range(len(lines) - len(run) + 1):
        if lines[k:k + len(run)] == run:
            return "".join(lines[:k] + lines[k + len(run):])
    sys.exit("S23's block is not contiguous in the S24 tip: the reconstruction would not be faithful")


def merge(root, name, path, base, ours, theirs, union):
    d = os.path.join(root, f"{name}-{'union' if union else 'plain'}")
    git("init", "-q", "-b", "main", d)
    for k, v in (("user.email", "repro@example.invalid"), ("user.name", "repro"),
                 ("core.hooksPath", os.devnull), ("commit.gpgsign", "false")):
        git("config", k, v, cwd=d)

    def commit(text, msg):
        with open(os.path.join(d, path), "w") as f:
            f.write(text)
        git("add", "-A", cwd=d)
        git("commit", "-q", "-m", msg, cwd=d)

    if union:
        with open(os.path.join(d, ".gitattributes"), "w") as f:
            f.write(f"{path} merge=union\n")
    commit(base, "base")
    git("checkout", "-q", "-b", "theirs", cwd=d)
    commit(theirs, "theirs")
    git("checkout", "-q", "main", cwd=d)
    commit(ours, "ours")
    rc = git("merge", "-q", "--no-edit", "theirs", cwd=d, check=False).returncode
    with open(os.path.join(d, path)) as f:
        merged = f.read()
    return d, rc, merged


def blocks(text):
    """(opener line number, [session values]) for each ```handoff block, in file order."""
    out, cur = [], None
    for n, line in enumerate(text.splitlines(), 1):
        if line == "```handoff":
            cur = (n, [])
        elif cur is not None and line.startswith("session:"):
            cur[1].append(line.split(":", 1)[1].strip())
        elif cur is not None and line == "```":
            out.append(cur)
            cur = None
    return out


def contains_run(text, run):
    lines = text.splitlines(keepends=True)
    return any(lines[k:k + len(run)] == run for k in range(len(lines) - len(run) + 1))


def report_receipts(root, results):
    path = "HANDOFFS.md"
    base, ours = show(BASE, path), show(S23_TIP, path)
    s23 = inserted_block(base, ours)
    theirs = remove_run(show(S24_TIP, path), s23)
    s24 = inserted_block(base, theirs)
    print(f"\n[1] receipts: {path}, S23 ({len(s23)} lines) and S24 ({len(s24)} lines) inserted at one anchor")
    for union in (False, True):
        d, rc, merged = merge(root, "receipts", path, base, ours, theirs, union)
        markers = merged.count("\n<<<<<<< ")
        bl = [f"L{n}:{'+'.join(s) or '?'}" for n, s in blocks(merged)[:3]]
        whole = contains_run(merged, s23) and contains_run(merged, s24)
        line = (f"    {'union' if union else 'plain'}: merge exit {rc}, conflict markers {markers}, "
                f"first blocks {bl}, both receipts whole: {whole}")
        if union and os.path.exists(CHECK_HANDOFF):
            ch = subprocess.run([sys.executable, CHECK_HANDOFF, "--all", "--file", os.path.join(d, path)],
                                capture_output=True, text=True)
            first_error = next((l.strip() for l in ch.stdout.splitlines() if "error:" in l), "none")
            line += f"\n           check-handoff --all exit {ch.returncode}; first error: {first_error}"
        print(line)
        results[("receipts", union)] = (rc, whole)


def report_ledger(root, results):
    path = "CHANGELOG.md"
    base, ours = show(BASE, path), show(S23_TIP, path)
    s23 = inserted_block(base, ours)
    theirs = remove_run(show(S24_TIP, path), s23)
    s24 = inserted_block(base, theirs)
    print(f"\n[2] ledger entries: {path}, S23 ({len(s23)} lines) and S24 ({len(s24)} lines) inserted at one anchor")
    from collections import Counter

    def nonblank(lines):
        return [l for l in lines if l.strip()]
    for union in (False, True):
        _, rc, merged = merge(root, "ledger", path, base, ours, theirs, union)
        markers = merged.count("\n<<<<<<< ")
        whole = contains_run(merged, s23) and contains_run(merged, s24)
        # Wholeness ignoring blank lines: each inserted entry's non-blank lines, contiguous and in order.
        m_nb = nonblank(merged.splitlines(keepends=True))
        whole_nb = all(any(m_nb[k:k + len(r)] == r for k in range(len(m_nb) - len(r) + 1))
                       for r in (nonblank(s23), nonblank(s24)))
        want = Counter(base.splitlines()) + Counter(l.rstrip("\n") for l in s23 + s24)
        missing = want - Counter(merged.splitlines())
        expected = sum(want.values())
        print(f"    {'union' if union else 'plain'}: merge exit {rc}, conflict markers {markers}, "
              f"lines {len(merged.splitlines())} of {expected} expected, missing {dict(missing) or 'none'}; "
              f"whole byte-for-byte: {whole}, whole ignoring blank lines: {whole_nb}")
        results[("ledger", union)] = (rc, whole_nb)


def report_fences_only(root, results):
    path = "HANDOFFS.md"
    base = "# H\n\n```handoff\nsession: S1\ndate: 2026-01-01\n```\n"
    ours = "# H\n\n```handoff\nsession: A\ndate: 2026-03-03\nstatus: complete\n```\n\n" + base[4:]
    theirs = "# H\n\n```handoff\nsession: B\ndate: 2026-02-02\nstatus: pending\n```\n\n" + base[4:]
    print("\n[3] synthetic: two receipts that share NO line except their fences")
    _, rc, merged = merge(root, "fences", path, base, ours, theirs, True)
    print(f"    union: merge exit {rc}, blocks {[(n, s) for n, s in blocks(merged)]} (3 blocks = whole)")
    results[("fences", True)] = (rc, len(blocks(merged)) == 3)


def report_trim(root, results):
    path = "HANDOFFS.md"

    def blk(s):
        return f"```handoff\nsession: {s}\nstatus: complete\nbody: {s} one\nbody2: {s} two\n```\n\n"
    base = "# Receipts\n\nfront matter\n\n" + blk("S21") + blk("S19")
    ours = "# Receipts\n\nfront matter\npointer: S21 and S19 archived to a shard\n\n" + blk("F1")
    theirs = "# Receipts\n\nfront matter\n\n" + blk("S22") + blk("S21") + blk("S19")
    print("\n[4] synthetic: ours retention-trimmed S21+S19 into a shard; theirs prepended S22 against them")
    for union in (False, True):
        _, rc, merged = merge(root, "trim", path, base, ours, theirs, union)
        print(f"    {'union' if union else 'plain'}: merge exit {rc}, conflict markers {merged.count(chr(10) + '<<<<<<< ')}, "
              f"blocks {[(n, s) for n, s in blocks(merged)]}")
        results[("trim", union)] = (rc, "S21" not in merged)


def main():
    for ref in (BASE, S23_TIP, S24_TIP):
        if git("cat-file", "-e", f"{ref}^{{commit}}", cwd=REPO, check=False).returncode:
            sys.exit(f"{ref} is not in this repository; fetch it first (see the docstring)")
    root = sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp(prefix="pr83-union-")
    os.makedirs(root, exist_ok=True)
    print(git("--version").stdout.strip(), f"| scratch: {root}")
    results = {}
    report_receipts(root, results)
    report_ledger(root, results)
    report_fences_only(root, results)
    report_trim(root, results)
    print("\nSummary (union rows):")
    print(f"    receipts whole: {results[('receipts', True)][1]}   ledger entries whole: {results[('ledger', True)][1]}"
          f"   fences-only whole: {results[('fences', True)][1]}   trimmed record stays archived: {results[('trim', True)][1]}")


if __name__ == "__main__":
    main()
