#!/usr/bin/env bash
# Losslessness proof for docs/planning/BACKLOG-DETAIL.md (the S99 split).
#
# Run from the repository root:   bash docs/planning/BACKLOG-DETAIL.md.verify.sh
# Exit 0 = every open item is byte-identical to the text it replaced. Non-zero = a real finding.
#
# WHAT THIS PROVES, AND WHY IT IS BUILT THIS WAY
# ----------------------------------------------
# It re-extracts each open item from the PRE-SPLIT BACKLOG.md in git and compares it to
# BACKLOG-DETAIL.md at the working tree, KEYED ON THE ITEM'S OWN IDENTITY (`BL-N`) -- never on its
# position in either file. It is modelled on BACKLOG-archive-2026-08-15.md.verify.sh, which is
# hand-written for the same reason: `methodology_trim.py` cannot generate it (its `LedgerSpec`
# requires a `date_of_record` and trims oldest-by-date; a backlog's axis is status, not age --
# BL-32), and its generated proofs compare BY POSITION with a 0/1 injection flag, which is why four
# of the six shipped ones report FAIL over archives that are provably intact (BL-36).
#
# The four checks below are deliberately the same four that proof uses, because the failure modes
# are the same: C1 identity set, C2 byte-exact bodies, C3 the move really happened (a COPY leaves
# the file just as large and proves nothing), C4 every item still reachable from the live file.

set -u

BASE_SHA="384b17c"                      # the claim commit: BACKLOG.md as it stood before the split
LIVE="docs/planning/BACKLOG.md"
DETAIL="docs/planning/BACKLOG-DETAIL.md"

if [ ! -f "$DETAIL" ]; then
  echo "verify: FAIL — $DETAIL not found. Run from the repository root." >&2
  exit 2
fi
if ! git cat-file -e "${BASE_SHA}:${LIVE}" 2>/dev/null; then
  echo "verify: FAIL — cannot read ${BASE_SHA}:${LIVE}. Is this the right clone?" >&2
  exit 2
fi

git show "${BASE_SHA}:${LIVE}" > "/tmp/_bl_pre.$$" || exit 2

BASE_SHA="$BASE_SHA" LIVE="$LIVE" DETAIL="$DETAIL" PRE="/tmp/_bl_pre.$$" \
python3 - <<'PY'
import os, re, sys, pathlib

pre    = pathlib.Path(os.environ["PRE"]).read_text()
detail = pathlib.Path(os.environ["DETAIL"]).read_text()
live   = pathlib.Path(os.environ["LIVE"]).read_text()
base   = os.environ["BASE_SHA"]

HEAD_RE   = re.compile(r"^\*\*BL-(\d+) —", re.M)
ANCHOR_RE = re.compile(r'^<a id="bl-(\d+)"></a>$', re.M)

def pre_bodies(text):
    """Open-item bodies in the PRE-SPLIT file: from `## Open items` to `## Completed items`,
    each body running from its own `**BL-N —` heading to the next (or the section end)."""
    start, stop = text.index("## Open items"), text.index("## Completed items")
    sec = text[start:stop]
    hits = [(m.start(), int(m.group(1))) for m in HEAD_RE.finditer(sec)]
    out = {}
    for k, (pos, n) in enumerate(hits):
        nxt = hits[k + 1][0] if k + 1 < len(hits) else len(sec)
        out[n] = sec[pos:nxt].strip("\n")
    return out

def detail_bodies(text):
    """Bodies in the detail file, split on the `<a id="bl-N">` anchors the move inserted. The
    anchor is the record separator here, exactly as the ```handoff fence is in HANDOFFS.md."""
    hits = [(m.start(), m.end(), int(m.group(1))) for m in ANCHOR_RE.finditer(text)]
    out = {}
    for k, (_s, e, n) in enumerate(hits):
        nxt = hits[k + 1][0] if k + 1 < len(hits) else len(text)
        out[n] = text[e:nxt].strip("\n")
    return out

was, now = pre_bodies(pre), detail_bodies(detail)
items = sorted(was)
fails, checks = [], []

# The population must be non-empty, or every check below passes vacuously. This is the control the
# proof needs on ITSELF: an extractor that silently matched nothing would otherwise report OK.
if not items or not now:
    print("verify: FAIL — extracted %d pre-split and %d detail item(s); a proof over an empty "
          "population asserts nothing." % (len(items), len(now)))
    sys.exit(2)

# C1 -- identity set. Every item open at the split must still be in the detail file. Items ADDED
# since are reported, NEVER failed: this proof asks "was anything lost in the move", and a backlog
# that can never gain an item would be a proof that fails on correct use -- which is precisely the
# false-positive class BL-36 is about. Losses fail; growth is reported.
missing = [n for n in items if n not in now]
added   = sorted(set(now) - set(items))
if missing:
    fails.append("C1 identity set: item(s) open at %s missing from the detail file: %s" % (base, missing))
else:
    checks.append("C1 identity set: all %d item(s) open at %s still present%s"
                  % (len(items), base,
                     "" if not added else "; %d raised since (not a finding): BL-%s"
                     % (len(added), ", BL-".join(str(n) for n in added))))

# C2 -- byte-exact bodies, per identity.
bad = [(n, len(was[n].encode()), len(now[n].encode())) for n in items
       if n in now and was[n].encode() != now[n].encode()]
if bad:
    for n, la, lb in bad:
        fails.append("C2 BL-%d: body differs — %d B at %s, %d B in detail" % (n, la, base, lb))
else:
    total = sum(len(was[n].encode()) for n in items)
    checks.append("C2 bodies: %d item(s) byte-identical to %s, %d B total" % (len(items), base, total))

# C3 -- the move actually happened. No moved body may still stand in the live file.
still = [n for n in items if was[n] in live]
if still:
    fails.append("C3 move: body still present verbatim in the live file for BL-%s (moved but not "
                 "removed — the file did not shrink)" % ", BL-".join(str(n) for n in still))
else:
    checks.append("C3 move: no moved body remains in %s" % os.environ["LIVE"])

# C4 -- reachability. The detail file must be named in the live file, and every item must keep an
# index row there. Without this the reduction has HIDDEN the work rather than relocated it.
name = os.environ["DETAIL"].split("/")[-1]
if name not in live:
    fails.append("C4 reachability: %s is never named in %s — the moved items have no path back"
                 % (name, os.environ["LIVE"]))
else:
    unrow = [n for n in items if not re.search(r"\*\*BL-%d\*\*" % n, live)]
    if unrow:
        fails.append("C4 reachability: no index row in the live file for BL-%s"
                     % ", BL-".join(str(n) for n in unrow))
    else:
        checks.append("C4 reachability: detail file named in the live file; all %d item(s) keep an "
                      "index row" % len(items))

# C5 -- the section PREAMBLE. C1-C4 enumerate ITEM BODIES, so they are all four green while any
# non-item text in the moved region silently disappears -- and one did: the first cut of this split
# dropped the 1,684 B "Routing — what a session can actually run today" block, which is the record
# that the "blocked on the paused channel" disposition was NEVER IMPOSED (CLAUDE.md's own rule about
# unattributed blockers). A losslessness proof only proves losslessness of the population it
# enumerates; this check exists because that population was drawn too narrowly once already.
pre_open = pre[pre.index("## Open items"):pre.index("## Completed items")]
first    = HEAD_RE.search(pre_open)
preamble = pre_open[len("## Open items\n\n"):first.start()] if first else ""
if not preamble.strip():
    fails.append("C5 preamble: no non-item text found between the section heading and the first "
                 "item at %s — the check cannot confirm what it is for" % base)
elif preamble not in live:
    fails.append("C5 preamble: the %d B of section text that stood above the first item at %s is "
                 "not present verbatim in the live file (moved region, not an item body)"
                 % (len(preamble.encode()), base))
else:
    checks.append("C5 preamble: the %d B routing block above the first item is verbatim in %s"
                  % (len(preamble.encode()), os.environ["LIVE"]))

for c in checks: print("  OK   " + c)
for f in fails: print("  FAIL " + f)
print()
if fails:
    print("verify: FAIL — %d finding(s). The split is NOT proved lossless." % len(fails))
    sys.exit(1)
print("verify: OK — BACKLOG-DETAIL.md is byte-identical to the open-item text it replaced, that "
      "text is gone from the live file, and every item is reachable from it.")
PY
rc=$?
rm -f "/tmp/_bl_pre.$$"
exit $rc
