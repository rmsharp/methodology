#!/usr/bin/env bash
# Losslessness proof for docs/planning/BACKLOG-COMPLETED.md (S223, 2026-09-26).
#
# WHAT THIS PROVES, and what it deliberately does not. BACKLOG.md's §Completed items held 33 closed
# items in two tables, 25,276 B, 43% of a file SESSION_RUNNER.md Phase 0 step 3 reads at every
# session. The rows moved to BACKLOG-COMPLETED.md. This script re-derives them from git and asserts
# five things: the identity set is the same on both sides (C1), every row is byte-identical across
# the move (C2), no moved row still stands in the live file (C3), every moved id is still reachable
# from the live file (C4), and the non-row text that shared the moved region survived (C5).
#
# It proves nothing about whether the rows are CORRECT — several are known to carry stale numbers,
# which the parent file says in as many words and which the move deliberately did not touch (FM #17).
# Byte-identity is the whole claim.
#
# THE FILE HAS TWO POPULATIONS, and since S226 this proof treats them differently. The 33 rows that moved
# are pinned: a missing one fails C1, an altered byte fails C2. Rows closed AFTER the move — this file is
# also the standing home for them, by its own editing rule and BACKLOG-DETAIL.md's — are REPORTED by C1 and
# never failed, with C6 asserting each one is still reachable from BACKLOG.md. That is the rule the sibling
# proof BACKLOG-DETAIL.md.verify.sh's C1 already states for the same kind of file. Until S226 the frozen
# reading refused the first closure after the extraction (BL-83's row, measured at S225): BL-86.
#
# Run from the repository root:  bash docs/planning/BACKLOG-COMPLETED.md.verify.sh
# Exit 0 = proved. Exit 1 = a finding. Exit 2 = the proof could not be established (worse than a
# finding: it means this script cannot see what it is for).

set -u

# The commit BEFORE the extraction. Its BACKLOG.md still holds §Completed items in full, so it is the
# only side of the comparison that can supply the "was" text. Pinned rather than resolved from HEAD:
# the derivation must not change as later commits land (BL-36's four failing proofs are the standing
# reminder that a proof whose inputs drift is not a proof).
BASE_SHA="a32f520"
LIVE="docs/planning/BACKLOG.md"
SHARD="docs/planning/BACKLOG-COMPLETED.md"

# The 33 identities, enumerated. NOT derived from the shard: a derived set cannot be asserted to
# cover its own parts — if a row vanished, a derived list would simply be shorter and C1 would pass.
ITEMS="1 2 3 4 5 6 7 8 9 10 15 20 24 25 27 28 29 33 34 35 38 40 41 43 45 53 56 59 67 72 76 78 82"

if [ ! -f "$SHARD" ]; then
  echo "verify: FAIL — $SHARD not found. Run from the repository root." >&2
  exit 2
fi
if [ ! -f "$LIVE" ]; then
  echo "verify: FAIL — $LIVE not found. Run from the repository root." >&2
  exit 2
fi
if ! git rev-parse --verify --quiet "$BASE_SHA^{commit}" >/dev/null; then
  echo "verify: FAIL — base commit $BASE_SHA is not in this clone; the pre-change text cannot be" >&2
  echo "        recovered, so losslessness cannot be established (a shallow clone does this)." >&2
  exit 2
fi

BEFORE="$(mktemp)"
trap 'rm -f "$BEFORE"' EXIT
if ! git show "${BASE_SHA}:${LIVE}" > "$BEFORE" 2>/dev/null; then
  echo "verify: FAIL — could not read ${LIVE} at ${BASE_SHA}." >&2
  exit 2
fi

BASE_SHA="$BASE_SHA" LIVE="$LIVE" SHARD="$SHARD" ITEMS="$ITEMS" BEFORE="$BEFORE" \
python3 - <<'PY'
import os, pathlib, re, sys

base   = os.environ["BASE_SHA"]
before = pathlib.Path(os.environ["BEFORE"]).read_text(encoding="utf-8")
live   = pathlib.Path(os.environ["LIVE"]).read_text(encoding="utf-8")
shard  = pathlib.Path(os.environ["SHARD"]).read_text(encoding="utf-8")
items  = [int(n) for n in os.environ["ITEMS"].split()]

ROW_RE = re.compile(r"(?m)^\| \*\*BL-(\d+)\*\* \|.*$")


def rows(text, start=None, stop=None):
    """Every `| **BL-N** | ... |` row in text, keyed by N, as one physical line each.

    A row is ONE line by construction in both files, so the record boundary is the newline and
    needs no lookahead. Slicing by section is done by the caller, because the pre-change file has
    two BL-row populations (§Open items and §Completed items) and only the second one moved.
    """
    seg = text
    if start is not None:
        if start not in text:
            return None
        seg = text[text.index(start):]
    if stop is not None:
        if stop not in seg:
            return None
        seg = seg[:seg.index(stop)]
    out = {}
    for m in ROW_RE.finditer(seg):
        n = int(m.group(1))
        if n in out:
            return ("DUP", n)
        out[n] = m.group(0)
    return out


fails, checks = [], []

# The pre-change §Completed items region. Asserted, not assumed: if either delimiter is missing the
# proof stops at exit 2 rather than silently comparing the wrong slice.
COMP = "## Completed items"
HIST = "## Historical context"
if COMP not in before or HIST not in before:
    print("verify: FAIL — §Completed items or §Historical context is absent from %s at %s; the "
          "moved region cannot be delimited the same way the move delimited it." % (os.environ["LIVE"], base))
    sys.exit(2)

was = rows(before, start=COMP, stop=HIST)
now = rows(shard)
for label, r in (("pre-change file", was), ("shard", now)):
    if isinstance(r, tuple):
        print("verify: FAIL — BL-%d appears twice in the %s; identity is not unique, so a byte "
              "comparison per identity is meaningless." % (r[1], label))
        sys.exit(2)

# C1 — identity set. Every expected id was there before and is in the shard. Checked before any byte
# comparison, so a missing row is a named finding rather than a silently shorter loop.
#
# IDS CLOSED SINCE THE MOVE ARE REPORTED, NEVER FAILED. This proof asks whether anything was LOST in the
# move, and a registry that can never gain a row would be a proof that FAILS ON CORRECT USE — the
# false-positive class BL-36 is about, and the rule the sibling proof BACKLOG-DETAIL.md.verify.sh's C1
# already applies to the same kind of file. The frozen literal above stays frozen and stays the loss
# detector: it is `missing_shard` that needs a literal nobody derived, never the growth line.
missing_before = [n for n in items if n not in was]
missing_shard  = [n for n in items if n not in now]
since_move     = sorted(set(now) - set(items))
if missing_before or missing_shard:
    fails.append("C1 identity set: missing from %s at %s: %s; missing from shard: %s"
                 % (os.environ["LIVE"], base, missing_before, missing_shard))
else:
    checks.append("C1 identity set: %d moved item(s), exactly the expected set, present on both sides%s"
                  % (len(items),
                     "" if not since_move else "; %d closed since the move (not a finding): BL-%s"
                     % (len(since_move), ", BL-".join(str(n) for n in since_move))))

# C2 — byte-exact rows, per identity.
bad, total = [], 0
for n in items:
    a = was.get(n, "")
    b = now.get(n, "")
    total += len(a.encode())
    if a.encode() != b.encode():
        bad.append(n)
if bad:
    fails.append("C2 bodies: not byte-identical to %s for BL-%s"
                 % (base, ", BL-".join(str(n) for n in bad)))
else:
    checks.append("C2 bodies: %d row(s) byte-identical to %s, %d B total" % (len(items), base, total))

# C3 — the move happened. No moved row may still stand in the live file. This is what separates a
# MOVE from a COPY: a copy leaves the file just as large and proves nothing about the reduction.
still = [n for n in items if was.get(n, "") and was[n] in live]
if still:
    fails.append("C3 move: row still present verbatim in the live file for BL-%s (archived but not "
                 "removed — the file did not shrink)" % ", BL-".join(str(n) for n in still))
else:
    checks.append("C3 move: no moved row remains in %s" % os.environ["LIVE"])

# C4 — reachability, and it is the check this extraction was redesigned around. The sibling proof
# BACKLOG-archive-2026-08-15.md.verify.sh asserts each of ITS eleven items keeps a `**BL-N**`
# mention in the live file, and eleven of those mentions were the very rows moved here. So the
# pointer block left behind carries every id: the shard must be named, and each id must still be
# findable from the file Phase 0 reads.
shard_name = os.environ["SHARD"].split("/")[-1]
if shard_name not in live:
    fails.append("C4 reachability: %s is never named in %s — a moved row has no path back"
                 % (shard_name, os.environ["LIVE"]))
else:
    unref = [n for n in items if not re.search(r"\*\*BL-%d\*\*" % n, live)]
    if unref:
        fails.append("C4 reachability: no id in the live file for BL-%s — the sibling proof's C4 "
                     "depends on this for its own eleven"
                     % ", BL-".join(str(n) for n in unref))
    else:
        checks.append("C4 reachability: shard named in the live file; all %d id(s) still findable "
                      "there" % len(items))

# C5 — the non-row text that shared the moved region. C1-C4 enumerate ROWS, so all four are green
# while any non-row text in the region silently disappears. The sibling split learned this the hard
# way: its first cut dropped a 1,684 B routing block, and its C5 exists because the enumerated
# population had been drawn too narrowly once already. Here the region's non-row text is the
# `**Not in this backlog:**` note about upstream PR #44 — a LIVE scope fact, not a closed record, so
# the move deliberately left it in the live file rather than archiving it.
NOTE = "**Not in this backlog:**"
i = before.index(COMP)
region = before[i:before.index(HIST)]
if NOTE not in region:
    print("verify: FAIL — the '%s' note is not in the moved region at %s, so this check cannot "
          "confirm what it is for." % (NOTE, base))
    sys.exit(2)
note_start = region.index(NOTE)
note_text = region[note_start:].rstrip("\n")
if note_text not in live:
    fails.append("C5 retained note: the %d B '%s' note that stood in the moved region at %s is not "
                 "present verbatim in the live file (it is a live scope fact, not a closed record)"
                 % (len(note_text.encode()), NOTE, base))
else:
    checks.append("C5 retained note: the %d B '%s' note is verbatim in %s"
                  % (len(note_text.encode()), NOTE, os.environ["LIVE"]))

# C6 — reachability for the rows closed SINCE the move, the same property C4 asserts for the 33. The
# editing rule's third step puts the bare id in BACKLOG.md's §Completed items pointer block, so a closed
# item stays findable from the file Phase 0 reads. Without this, that step is the one step nothing checks,
# and C1's growth line would report an unfindable row as health. A row here with no id there is an item
# that was closed by deleting it.
if since_move:
    unref_since = [n for n in since_move if not re.search(r"\*\*BL-%d\*\*" % n, live)]
    if unref_since:
        fails.append("C6 reachability since the move: no id in %s for BL-%s — closed, and no longer "
                     "findable from the file Phase 0 reads"
                     % (os.environ["LIVE"], ", BL-".join(str(n) for n in unref_since)))
    else:
        checks.append("C6 reachability since the move: all %d later closure(s) findable in %s"
                      % (len(since_move), os.environ["LIVE"]))

for c in checks:
    print("  OK   " + c)
for f in fails:
    print("  FAIL " + f)
print()
print("source : the commit before the extraction, %s" % base)
print("rows   : %d moved, %d closed since; live file %d B, shard %d B"
      % (len(items), len(since_move), len(live.encode()), len(shard.encode())))
print("checked: C1, C2, C3, C4, C5" + (", C6" if since_move else " (C6: no closures since the move)"))
if fails:
    print("verify: FAIL — %d finding(s). The move is NOT proved lossless." % len(fails))
    sys.exit(1)
print("verify: OK — BACKLOG-COMPLETED.md is byte-identical to the rows it replaced, the rows are "
      "gone from the live file, every id is still findable there, and the region's live note stayed.")
PY
exit $?
