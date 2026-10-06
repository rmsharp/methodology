#!/usr/bin/env python3
"""Fold upstream's ledger records that the fork lacks into the fork's live ledgers.

Evidence tool for docs/planning/upstream-resync-2026-10-plan.md section 2.4. It performs the two
non-mechanical ledger resolutions of the resync merge, and the trial in that plan ran exactly this.

    python3 fold-ledger.py changelog [--fork-ref HEAD] [--upstream-ref upstream/main] [--dry-run]
    python3 fold-ledger.py handoffs  [--fork-ref HEAD] [--upstream-ref upstream/main] [--dry-run]

THE FORK'S SIDE IS READ FROM GIT, NOT FROM THE WORKING TREE. During `git merge --no-commit` HEAD is
still the fork's commit, so the default --fork-ref HEAD is right and no "restore ours first" step is
needed; the working tree may hold conflict markers or upstream's shard and none of it is read. (A
first version of this script read the working tree: after a plain `git merge` it folded NOTHING,
because the conflicted CHANGELOG.md and the add/add shard both read as "held". The reviewer of the
plan found it.) Run it after the merge commit instead and pass --fork-ref <the pre-merge commit>.
It writes CHANGELOG.md or HANDOFFS.md in the working tree, never commits, and touches nothing else.

changelog
    Keeps every upstream entry whose `### ` heading appears NOWHERE in the fork's corpus (live ledger
    plus every docs/archive/CHANGELOG-*.md at the fork ref) and inserts it into the live ledger by
    date: after every fork entry dated the same day or later, before the first strictly older one.
    Within a day the fork's entries precede the arriving ones (HANDOFFS.md front matter: "within a
    shared date the fork's precede the arriving upstream ones"); the arriving ones keep upstream's
    own order. Two rules the trial measured:
    * An entry that came from one of upstream's SHARDS carries links in the shard's archive-relative
      form (`](../../x)`), because the trimmer rebases them when it archives. In a root ledger that
      form points outside the repository and the fork's trimmer refuses the range
      (TRANSFORM_NOT_INVERTIBLE). The script applies the inverse (`](../../` -> `](`) to shard-sourced
      entries only; the trial found exactly one such link.
    * An entry whose heading the fork already holds is NOT folded, even where the body differs (7 of
      the 50 held headings do, links normalised). The fork's copy is kept; the script names them.
    Entry boundaries are bin/check-ledger's: from a `### ` line to the next `### `, a `## ` month
    heading, or a `---` rule.

handoffs
    Keeps the fork's front matter and receipts, in order, then appends every upstream receipt whose
    (session, date) is in no fork shard (docs/archive/HANDOFFS-*.md) and not among the fork's live
    receipts, in upstream's file order. Receipts are identified by session AND date, never by number
    alone (HANDOFFS.md front matter). The front matter ends where the first receipt fence starts.

Both modes print the figures the plan measured at fork f203159 + upstream f34769f and say plainly
whether this run matches them. A difference is not an error (upstream moves); it means "re-derive the
plan's numbers before trusting them".
"""
import argparse
import re
import subprocess
import sys

PLAN = {  # fork f203159 + upstream f34769f, plan section 2.4
    "changelog": {"folded": 118, "entries": 386, "bytes": 415398},
    "handoffs": {"arriving": 17, "receipts": 20, "bytes": 114995},
}


def git(*args, check=True):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if r.returncode != 0 and check:
        sys.exit(f"fold-ledger: git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout


def show(ref, path):
    return git("show", f"{ref}:{path}")


def archive_paths(ref, prefix):
    out = git("ls-tree", "-r", "--name-only", ref, "docs/archive")
    return [p for p in out.splitlines() if p.startswith(f"docs/archive/{prefix}") and p.endswith(".md")]


def split_entries(text):
    out, cur = [], None
    for ln in text.splitlines(keepends=True):
        if ln.startswith("### "):
            if cur:
                out.append(cur)
            cur = [ln]
        elif cur is not None:
            if ln.startswith("## ") or ln.rstrip() == "---":
                out.append(cur)
                cur = None
            else:
                cur.append(ln)
    if cur:
        out.append(cur)
    return ["".join(e) for e in out]


def entry_date(entry):
    m = re.match(r"### (\d{4}-\d{2}-\d{2})", entry)
    if not m:
        sys.exit(f"fold-ledger: entry without a leading date: {entry.splitlines()[0][:80]!r}")
    return m.group(1)


def verdict(got, want):
    same = all(got[k] == want[k] for k in want)
    print("  result: " + ", ".join(f"{k} {got[k]:,}" for k in want))
    print("  " + ("matches the plan's trial figures." if same else
                  "DIFFERS from the plan's trial figures (" + ", ".join(f"{k} {want[k]:,}" for k in want) +
                  "): upstream or the fork moved; re-derive the plan's numbers before trusting them."))


def changelog(a):
    fork_text = show(a.fork_ref, "CHANGELOG.md")
    first = fork_text.index("\n### ") + 1
    head, body = fork_text[:first], fork_text[first:]
    fork_entries = split_entries(body)

    # heading -> body over the fork's whole corpus (live ledger + every shard), all at the fork ref.
    # Bodies are compared with the shard-relative link form undone, so a rebased link is not a difference.
    norm = lambda s: s.replace("](../../", "](")
    held = {e.splitlines()[0].rstrip("\n"): norm(e) for e in fork_entries}
    for p in archive_paths(a.fork_ref, "CHANGELOG-"):
        for e in split_entries(show(a.fork_ref, p)):
            held.setdefault(e.splitlines()[0].rstrip("\n"), norm(e))

    live = [(e, False) for e in split_entries(show(a.upstream_ref, "CHANGELOG.md"))]
    shards = [(e, True) for p in archive_paths(a.upstream_ref, "CHANGELOG-")
              for e in split_entries(show(a.upstream_ref, p))]

    fold, skipped = [], []
    for e, from_shard in live + shards:
        h = e.splitlines()[0].rstrip("\n")
        if h in held:
            skipped.append((h, norm(e).rstrip() != held[h].rstrip()))
            continue
        if from_shard:
            e = e.replace("](../../", "](")
        fold.append(e if e.endswith("\n\n") else e.rstrip("\n") + "\n\n")

    merged = list(fork_entries)
    for e in sorted(fold, key=entry_date, reverse=True):  # stable: upstream's order within a day
        d, at = entry_date(e), len(merged)
        for i, f in enumerate(merged):
            if entry_date(f) < d:
                at = i
                break
        merged.insert(at, e)
    out = head + "".join(x if x.endswith("\n") else x + "\n" for x in merged)

    print(f"CHANGELOG.md: the fork has {len(fork_entries)} live entries; upstream entries already held and "
          f"skipped: {len(skipped)}")
    differ = [h for h, d in skipped if d]
    print(f"  of the skipped, {len(differ)} differ in body from the fork's copy (the fork's copy is kept):")
    for h in differ:
        print("    body differs:", h[:110])
    verdict({"folded": len(fold), "entries": len(merged), "bytes": len(out.encode())}, PLAN["changelog"])
    return "CHANGELOG.md", out


def blocks(text):
    return re.findall(r"^```handoff\n.*?^```\n", text, re.M | re.S)


def key(block):
    return (re.search(r"^session: (.+)$", block, re.M).group(1), re.search(r"^date: (.+)$", block, re.M).group(1))


def handoffs(a):
    fork_text = show(a.fork_ref, "HANDOFFS.md")
    fork_blocks = blocks(fork_text)
    seen = {key(b) for b in fork_blocks}
    for p in archive_paths(a.fork_ref, "HANDOFFS-"):
        seen |= {key(b) for b in blocks(show(a.fork_ref, p))}
    arriving = [b for b in blocks(show(a.upstream_ref, "HANDOFFS.md")) if key(b) not in seen]
    start = re.search(r"^```handoff\nsession:", fork_text, re.M).start()  # a fence AT A LINE START
    out = fork_text[:start] + "\n".join(fork_blocks + arriving) + "\n"
    print(f"HANDOFFS.md: the fork has {len(fork_blocks)} live receipts; arriving: {[key(b)[0] for b in arriving]}")
    verdict({"arriving": len(arriving), "receipts": len(fork_blocks) + len(arriving), "bytes": len(out.encode())},
            PLAN["handoffs"])
    return "HANDOFFS.md", out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("mode", choices=["changelog", "handoffs"])
    ap.add_argument("--fork-ref", default="HEAD")
    ap.add_argument("--upstream-ref", default="upstream/main")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    print(f"fork ref {a.fork_ref} = {git('rev-parse', '--short', a.fork_ref).strip()}; "
          f"upstream ref {a.upstream_ref} = {git('rev-parse', '--short', a.upstream_ref).strip()}")
    path, out = (changelog if a.mode == "changelog" else handoffs)(a)
    if a.dry_run:
        print(f"--dry-run: {path} not written")
        return
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(out)
    print(f"wrote {path} in the working tree (not staged, not committed)")


if __name__ == "__main__":
    main()
