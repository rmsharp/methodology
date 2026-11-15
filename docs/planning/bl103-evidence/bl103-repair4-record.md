# BL-103 option (c) record (S452, 2026-11-15): `--run` and `--status` name the unmeasured gates

`starter-kit/quality_ratchet.py` 1.7.0 (a distributed tool) and its unit file. Fork only: nothing was sent to `KJ5HST/methodology`
(D8: one pull request later, each outward step his go-ahead). His picks at the S452 pickers: trim `HANDOFFS.md` first ("Yes: dry run,
then trim to 3"); BL-103 (c) as the deliverable; the plan approved at the Phase 4 picker as written (the clause on `--run` and
`--status`, never in `--json`).

## 1. What was found

BL-103's repair 3 (S307) made `bin/check-handoff` refuse a newest complete receipt that cites `U unmeasured` gates unless the receipt
names at least U of them as `unmeasured: <gate>, <gate>`. The tool that produces the citation printed the count and never the names, so
the person retyped them from the table. The repair-3 record left it as "his call (1): whether `--run` should print the unmeasured
names in the form the lint reads". The 2026-10-18 interaction review called it "a ratchet 1.6.0"; the kept-output plan's D3 (decided
at S450) made it a separate build, so 1.6.0 went to the keeper and this is 1.7.0.

## 2. What was built

| Where | What |
|---|---|
| `starter-kit/quality_ratchet.py:80` | `VERSION = "1.7.0"` |
| `:759` `unmeasured_clause(snap)` | the unmeasured gates in the snapshot's order, each name whole, as `unmeasured: <a>, <b>`; `""` when none |
| `:767` `render`, clause print at `:784` | one line right after `cite in the receipt:`, `and name them:` then the clause, plain text after the label; the blank line after the block is unchanged, so a run with nothing unmeasured prints what 1.6.0 printed |
| `:57` module docstring, `:1123` `--help` | 'WHAT IT NAMES' and two usage lines |
| `:998` `--selftest` | one more check (32 checks on 1.6.0, 33 now) |

`render` serves `--run` and `--status` (the stored results), so both print it. `--json`, the summary line, the results hash and the
results file's keys are untouched. The runner's 3E, the receipt seed and `HOW_TO_USE.md` are unchanged: their sentence stays true, and
the runner has about 66 B of room.

## 3. How it is held

* **Tests, written first.** `tools/test_quality_ratchet.py:2085` `TestTheUnmeasuredGatesAreNamed`: 15 tests read red on the unchanged
  1.6.0 (10 failures and 6 errors, each error "no clause line"; 4 that assert an absence passed vacuously, which is what the mutation
  round is for): `bl103-evidence/repair4-red-on-1.6.0.txt`. The version pin (`:2214`) moved to 1.7.0.
* **A mutation round, two rounds.** `mutate-repair4.py`: 29 mutants, 27 real and 2 controls (M00 changes nothing and survived, M01
  empties the clause and was killed). Round 1 killed 25 of 27; **M15** (no blank line after the clause) and **M21** (the results file
  carrying the clause) survived, each a behaviour no test named. Round 2 added `:2125` and `:2133`; both killed, M00 survived again
  (`mutate-repair4-round1-output.txt`, `-round2-output.txt`).
* **The real lint, in two ways.** A unit test loads `bin/check-handoff` by path and shows `validate_gate_citation` accepting the
  pasted pair (with and without a ` — by hand:` tail) and refusing the bare citation. `repair4-smoke.sh` does it as two processes: the
  real tool on a throwaway project (one gate passes, one times out, one has no command), the two printed lines pasted into a copy of
  the newest complete receipt, the real `bin/check-handoff` command on it: exit 0 with the clause, exit 1 without
  (`repair4-smoke-output.txt`, `SMOKE OK`).
* **The unit file and the gate.** 190 tests on 1.6.0 (102 s), 207 on 1.7.0 (95 s, `repair4-green-1.7.0-unit-file-207.txt`). The
  `ratchet-unit-tests` floor rose 190 to 207 (a tightening, measured; the pre-commit ratchet accepted it).
* **The 26 gates, through the tool's own `--run`, in a scratch clone of `b32fda08`** (named `methodology`, a clean tree, 19:08:17Z to
  19:56:03Z, 47 min 46 s, exit 0, stderr empty, no kept directory): **26/26 pass · 0 fail · 0 unmeasured · results `45bb9454357f` ·
  manifest `597970e9ef98`**; `tests-sh-passed` 702, `ratchet-unit-tests` 207 through the gate's own extract (`repair4-gate-run-26of26.txt`).

## 4. Measured

| | 1.6.0 | 1.7.0 |
|---|---|---|
| `tools/test_quality_ratchet.py` | 190 tests OK, 102 s | 207 tests OK, 95 s (a 205-test run was 127 s at load 122) |
| `--selftest` | 32 checks | 33 checks |
| `tools/test_layout_resolver.py` | | 75 OK; `bin/check-layout-literals` exit 0 |
| gate names in the lint's shape, 18 manifests | | 67 of 67 |

The four older load-sensitive BL-107 tests did not fail in the three full unit runs (load 70 to 122) or in the 26-gate run.

## 5. Not verified, not done

Not verified: Windows, a terminal without ANSI, GitHub CI, an adopter's own copy (an adopter has no `bin/check-handoff`, so there the
clause is a convenience, not a gate), a manifest whose gate name the lint cannot read. Not done, by decision: sanitizing such a name.
`config_defects` accepts any non-empty name and the lint reads `[A-Za-z0-9][A-Za-z0-9_.-]*`; no name in 18 manifests (67 names) falls outside it at S452. **That count is a reading with a time on it**: `python3 -I docs/planning/bl103-evidence/repair4-name-census.py` recomputes it.
**Correction to the plan shown at the Phase 4 picker**, which said such a name "fails closed". Measured on the lint
(`validate_gate_citation`): the lint reads such a name as its first word, so it counts as one name. A clause of two or more such names
is refused (it counts fewer than owed: `reads 2 unmeasured gate(s) and the receipt names 1`), but a lone one, or one beside readable
names, is accepted, because the lint checks structure, never truth. Not done: the dashboard mirror of `timeout_seconds` and whether 3600 s stays (BL-103's other open calls); a
change to the runner's, the seed's or `HOW_TO_USE.md`'s sentence; any route to adopters or upstream (P4 of the kept-output plan).

## 6. His calls

(1) How 1.7.0 reaches an adopter or upstream: with 1.6.0 (the kept-output plan's P4, a merge trial first), after it, or not yet.
(2) Whether a complete receipt may cite `fail` above 0 at all (four older ones did; S305 and S307's open call). (3) The dashboard
mirror and whether 3600 s stays. (4) D8, the release number, any tag.

## 7. Mistakes and corrections in the session

(1) The plan's "fails closed" for an unreadable name was too strong (section 5); found while writing this record from the lint's own
regular expression. (2) A ledger entry said the selftest went from 32 to 33 checks when only the 33 had been measured; the 32 was
measured on the previous commit afterwards and held. (3) Importing the mutation harness to check its mutants left a `__pycache__`
beside it, noticed at the next `git status` and removed.
