"""The mutants of the BL-101 F21 pass (S300), for mutate-p7.py (the runner is not specific to P7). Each is (id, file, old, new,
test classes): `old` occurs exactly once in `file`; the classes are where the killing test is expected to live (the fast ones
first). Written from the new code, one mutant per behaviour `first_heading` and `insert_entry` gained: what opens a fence, what
closes one, how the offset is kept, when the tool refuses, and where the entry goes once the heading is found. The lesson of F5's
first round (7 of 30 survived, each a behaviour no test pinned) and of F24's (two real gaps) is to write the tests for a named
behaviour BEFORE the round, and to aim round 2 at the behaviours round 1 did not name.
Usage: mutate-p7.py <scratch clone of the commit under test> f21-mutants.py [ids...]"""
T = "bin/migrate-layout"
PURE = ["TestThePureRules"]
CMD = ["TestTheLedgerEntry"]
BOTH = PURE + CMD
FENCE_OLD = 'FENCE_RE = re.compile(r"^(`{3,}|~{3,})(.*)$")'
CLOSE_OLD = "        elif f and f.group(1)[0] == fence[0] and len(f.group(1)) >= fence[1] and not f.group(2).strip():\n"

MUTANTS = [
    # --- what opens a fence
    ("F01", T, FENCE_OLD, 'FENCE_RE = re.compile(r"^(`{3,})(.*)$")', PURE),                    # no tilde fence
    ("F02", T, FENCE_OLD, 'FENCE_RE = re.compile(r"^(`{4,}|~{3,})(.*)$")', PURE),               # three backticks no longer open
    ("F03", T, FENCE_OLD, 'FENCE_RE = re.compile(r"^(`{2,}|~{3,})(.*)$")', PURE),               # two backticks open
    ("F04", T, FENCE_OLD, 'FENCE_RE = re.compile(r"^(`{3,}|~{4,})(.*)$")', PURE),               # three tildes no longer open
    # F05 (the `^` of FENCE_RE dropped) is an EQUIVALENT mutant and not run: the pattern is only used with `.match`, which anchors
    # at the start of the line whether or not the pattern says so.
    ("F06", T, 'fence = (f.group(1)[0], len(f.group(1)))', 'fence = (f.group(1)[0], 3)', PURE),  # the opener's length forgotten
    ("F07", T, 'fence = (f.group(1)[0], len(f.group(1)))', 'fence = ("`", len(f.group(1)))', PURE),  # the opener's character forgotten
    # --- what closes one
    ("C01", T, CLOSE_OLD, "        elif f and len(f.group(1)) >= fence[1] and not f.group(2).strip():\n", PURE),        # any character closes
    ("C02", T, CLOSE_OLD, "        elif f and f.group(1)[0] == fence[0] and len(f.group(1)) == fence[1] and not f.group(2).strip():\n", PURE),  # only an equal length
    ("C03", T, CLOSE_OLD, "        elif f and f.group(1)[0] == fence[0] and not f.group(2).strip():\n", PURE),          # any length closes
    ("C04", T, CLOSE_OLD, "        elif f and f.group(1)[0] == fence[0] and len(f.group(1)) >= fence[1]:\n", PURE),     # an info string closes
    ("C05", T, CLOSE_OLD, "        if f and f.group(1)[0] == fence[0] and len(f.group(1)) >= fence[1] and not f.group(2).strip():\n", PURE),  # the opener closes itself
    ("C06", T, CLOSE_OLD, "        elif False:\n", PURE),                                                                 # nothing closes
    # --- where a heading counts
    ("H01", T, "        if fence is None:\n            if f:", "        if True:\n            if f:", PURE),                  # a heading counts inside a fence
    ("H02", T, "        offset += len(line) + 1\n", "        offset += len(line)\n", PURE),                                    # the offset drifts a byte a line
    ("H03", T, 'for line in text.split("\\n"):', 'for line in text.splitlines():', PURE),                                      # DOS line endings shift the offset
    # --- the refusal
    ("R01", T, "    if fence is not None:\n        raise Unsafe(", "    if False:\n        raise Unsafe(", BOTH),
    ("R02", T, "    if fence is not None:\n        raise Unsafe(", "    if fence is None:\n        raise Unsafe(", BOTH),
    ("R03", T, 'raise Unsafe("the ledger has a code fence that never closes, so its entry cannot be placed outside it")', 'raise ValueError("the ledger has a code fence that never closes, so its entry cannot be placed outside it")', CMD),  # not the refusal path
    # --- the placement once the heading is found
    ("P01", T, "        return text[:start] + block + text[start:]\n    if m.group(1) == ", "        return text[:m.start()] + block + text[m.start():]\n    if m.group(1) == ", PURE),
    ("P02", T, 'i = text.index("\\n", start) + 1', 'i = text.index("\\n", m.start()) + 1', PURE),
    ("P03", T, 'return text[:start] + "## " + month', 'return text[:m.start()] + "## " + month', PURE),
    ("P04", T, "    if found is None:\n        return SENTINEL_RE", "    if found is None and False:\n        return SENTINEL_RE", PURE),
]

# Round 2: the two survivors of round 1 (F06 and C03: the nested-fence fixture closed its own fence by coincidence; the fixture
# was changed to an unbalanced inner line, so both are re-run) and the behaviours round 1 did not name (where the scan starts,
# trailing blanks on a closer, the offset returned, an opener that carries an info string). Run with F21_ROUND=2.
OPEN_OLD = "            if f:\n                fence = (f.group(1)[0], len(f.group(1)))"
ROUND2 = [m for m in MUTANTS if m[0] in ("F06", "C03")] + [
    ("S01", T, "    fence, offset = None, 0\n", "    fence, offset = None, 1\n", PURE),
    ("S02", T, "and not f.group(2).strip():\n            fence = None", "and not f.group(2):\n            fence = None", PURE),
    ("S06", T, "                    return offset, m\n", "                    return offset + 1, m\n", PURE),
    ("S11", T, OPEN_OLD, "            if f and not f.group(2).strip():\n                fence = (f.group(1)[0], len(f.group(1)))", PURE),
]
import os
if os.environ.get("F21_ROUND") == "2":
    MUTANTS = ROUND2
