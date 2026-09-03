**Base: `read-set-budgets`, not `main`.** Second of four PRs staged there for selective testing.
It follows #76 and must land before the `FRAMEWORK_APPARATUS.md` extraction, for a measured reason
given at the end.

## What this does

Ships the ledger trimmer — `starter-kit/methodology_trim.py`, the tool that bounds `CHANGELOG.md`
and `HANDOFFS.md` growth by archiving the oldest records into a frozen shard and proving the move
lossless (L1 records-zone concatenation, L2 zone pinning, L3 record partition).

| Item | Class |
|---|---|
| `starter-kit/methodology_trim.py` (+ its `bin/_manifest.py` row, 25 → 26) | **distributed** |
| `tools/test_methodology_trim.py` (123 tests) + the `bin/tests.sh` line that runs them | canonical-only |
| `starter-kit/CHANGELOG.md`, `starter-kit/HANDOFFS.md` | **distributed** seeds — the trimmer's contract is stated there |
| dashboard exclusion + signature entries, both twins | canonical + distributed twin |

The manifest row lands **with** its file, so sources-listed equals files-present at every step.

## The part worth reviewing: the tests were coupled to my fork's history

`tools/test_methodology_trim.py` drove L1/L2/L3 from two commits in the fork's own history —
`020ba3f` (a CHANGELOG archive that carried the scope footer out of the live file) and `7a71df0`
(a HANDOFFS archive that bundled a record edit with the move). **Neither is reachable in any other
clone.** Ported unchanged, 19 of 123 tests fail here — including *all* of `TestL2` and *all* of
`TestL3`. An adopter who installs the trimmer could never run its tests either.

I replaced them with fixtures reproducing the **structural properties**, not the bytes:

- **`SYNTHETIC_CHANGELOG`** — front matter, records, and a non-empty footer carrying a rebasable
  `](link)`. The link is load-bearing: without one, the footer-moved clause is only ever tested in
  its verbatim form and the `transform_record` path goes uncovered.
- **`SYNTHETIC_BEFORE/_AFTER/_SHARD`** — a **25 = 6 + 19** partition in which one *retained* record
  was edited. Counts partition; content does not. That is exactly what made `7a71df0` the event
  worth testing against.

**The original docstrings warned that "a synthetic one tests the test", and that objection is
answered rather than waved away.** Three mutants of the code under test were run against the new
fixtures and each was killed:

| Mutant | Tests failing |
|---|---|
| `L2_FOOTER_MOVED` never emitted | **6** |
| `L3_RECORD_ALTERED` never emitted | **4** |
| `L1_MISMATCH` never emitted | **5** |

The three fixture-control tests were rewritten to assert the synthetic fixtures genuinely carry the
properties the suite relies on — including a control that a whole-file grep cannot distinguish "the
footer is present" from "a record merely quotes it", which is the insight the fork-history version
carried and the reason zones exist at all.

**Two tests remain guarded and skip here, deliberately.** The declared-regenerated-field tests use
the *real* count in the live root `HANDOFFS.md`, and their whole point is that the count really
drifted by hand. A synthetic anchor there would test the test. They skip on a repository that
declares no retention policy, and the precondition is read from the raw file — never through
`classify_zones`, which is the code under test.

## Verification

Run in `git clone --no-local --single-branch`, with `020ba3f` and `7a71df0` unreachable and
`docs/archive/` absent — i.e. genuinely upstream-like, not a worktree that would resolve them.

| | Result |
|---|---|
| Base (`read-set-budgets`) | **113 passed, 1 failed** |
| This branch | **114 passed, 1 failed** |
| Delta | **+1 passing, zero added failures** |
| `tools/test_methodology_trim.py` alone | **123 tests, exit 0**, 2 skipped |
| `tools/test_methodology_dashboard.py` | **211 tests, exit 0** |
| Manifest self-consistency | **26 listed, 26 present** |

The one failure is the same `Test 9` #76 declared: `bin/sync --source=github` reads `main`, and this
branch's newest manifest rows name files not yet there. It heals when the branch merges to `main`.

## ⚠ For anyone testing this branch

**Do not verify with `bin/sync --source=github`** — it is pinned to `main` (`bin/sync:93` sends no
`?ref=`; `:162` is literally `commits/main`), so it syncs `main`'s files, looks clean, and has tested
nothing. Use `--source=local`.

## Why this must precede the apparatus extraction

Measured, not assumed: the dashboard's canonical-only tests abort with **13 errors** when
`methodology_trim.py` is absent — *"the canonical repo must locate its own trimmer, or the present
branch is not under test at all"* — and **0** with it.

## Disclosures

- The dashboard's `_FRAMEWORK_FILE_SIGNATURES` entry carries its **own** `TRIM_VERSION` pattern. The
  shared `_VERSION_RE` matches `DASHBOARD_VERSION` only; reusing it would fall through to the
  signature path on every scan, which is the silent-skip defect that table's own comment describes.
- `CHECKLIST_EXEMPT` gains the trimmer with the rationale used in the fork: sync installs it
  automatically, so its presence measures sync rather than adoption, and scoring it would re-cut
  `METHODOLOGY_MAX` and move every already-compliant adopter's percentage for a change they did not
  make.
- The two distributed seeds grow substantially (`HANDOFFS.md` 5,314 → 11,442 B, `CHANGELOG.md`
  3,622 → 12,893 B). They state the trimmer's contract, and the suite asserts against them.

---

_Authored by an AI agent under the operator's direction; every figure re-derived in a clean clone.
Review before relying on it for human-facing work._
