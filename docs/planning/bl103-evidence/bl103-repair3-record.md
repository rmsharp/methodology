# BL-103 repair 3 record (S307, 2026-10-12): a cited gate run that reads unmeasured gates must name them

`bin/check-handoff` (canonical-only) and three prose sentences (the runner's 3E, the seed's §Citing the gate run, `HOW_TO_USE.md`).
Fork only: nothing was sent to `KJ5HST/methodology` (D8: one pull request later, each outward step his go-ahead). His picks at the S307
Phase 0 and Phase 4 pickers: BL-103 repair 3 as the deliverable; the lint **allows a named exception** (not refuse outright, not report
only); the rule goes in the **runner and the seed**; build as planned.

## 1. What was found

BL-103 (raised S280) left one thing open after S305 (`quality_ratchet.py` 1.4.0) and S306 (1.5.0): nothing refuses a gate run that reads
`unmeasured`, so a receipt can cite one. `bin/check-handoff:266` (`GATE_CITATION_RE`) checks that a citation exists (`quality_ratchet: N/M pass`),
and `quality_ratchet.py` prints "cite in the receipt:" under every run, `17/18 pass · 1 unmeasured` included (`:564`). The tool does exit 1 on an
unmeasured gate (`:597`); the receipt is where the claim becomes durable.

* **The population** (`survey-citations.py`, output beside it). This repository: 342 receipts in 132 files (the live ledger and every shard),
  167 citations of a gate run, **one** reading unmeasured above 0: S287's `15/18 pass · 0 fail · 3 unmeasured` (the load-induced timeouts
  BL-103 was raised for; handled honestly, the three suites run by hand and the results written in the receipt, in prose). Siblings under
  `~/Development`: 13 projects scanned, 4 with declared gates, 5 with citations, 246 citations, **none** above 0. **413 citations, 1 unmeasured.**
  *(Correction: the S307 Phase 4 picker text said "this repository and 9 adopters"; the figure is 13 sibling projects scanned, 5 carrying citations.)*
  Four older citations read `fail` above 0 on a receipt marked complete; that is not repair 3 and is left alone.
* **"A gate that counts the unmeasured" cannot work** (`counting-gate-demo.sh`, output beside it). The ratchet writes the results file after every
  gate has run (`quality_ratchet.py:587-588`, `do_run`: `run_gates`, then the write), so a gate that reads it reads the previous run: in run 1 the counting gate read `0 pass` in a
  run with one unmeasured gate; in runs 2 and 3 it read run 1's count and failed on it. Dropped.
* **Where a rule can live.** `starter-kit/SESSION_RUNNER.md` is `TRACKED` (`bin/_manifest.py:48`): a sentence there reaches every adopter's runner. `starter-kit/HANDOFFS.md` is a
  `SEED` (`:70`): it reaches only a project that takes it new, and a synced project reads `present (seed; left as-is)`. `bin/check-handoff` is
  canonical-only. `HOW_TO_USE.md:766` holds a third copy of the 3E sentence (found by the grep inventory; the plan named two).

## 2. What changed

| commit | what |
|---|---|
| `9e1587b` | ten rows in the gate-citation block of `bin/tests.sh`, written RED first: the block alone read `PASS=10 FAIL=5`, the five "must be a finding" rows failing because `validate_gate_citation` reads only that a citation exists |
| `5cb11a6` | the lint: `GATE_UNMEASURED_RE` (`bin/check-handoff:273`), `UNMEASURED_CLAUSE_RE` (`:275`), `validate_gate_citation` (`:860`). For the newest complete receipt, a finding unless an `unmeasured: <gate>, <gate>` clause names at least as many gates as the largest `U unmeasured` any citation reads. Spaces and tabs only between the pieces; names are comma-separated, so the words after them (`by hand: ...`) are not names; backticks allowed; a citation with no unmeasured field is judged on its structure alone; older receipts are not re-judged |
| `95005e8` | the prose: `starter-kit/SESSION_RUNNER.md:284`, `starter-kit/HANDOFFS.md` §Citing the gate run, `HOW_TO_USE.md:766` |
| `8dab34f` | ten more rows for the mutation round's survivors (the block reads `PASS=25 FAIL=0`) |
| `60b6412` | the ten "must be a finding" rows assert the lint's own message (`unm_flag`), not only a nonzero exit: an exit code also passes on a fixture the schema rejects. The count is unchanged |
| `03f9b78`, `84eeb81` | evidence: the survey and the counting-gate demonstration; the mutation script and both rounds' output |
| `f294eb5` | `.quality-gates.json`: `tests-sh-passed` floor 477 to 503, the suite measured at 503 (a tightening) |

The rule, as written: a run that reads unmeasured gates is not a clean one; repair the gate (its command, or `timeout_seconds` if it is only slow) and run
again, or name each one in the receipt as `unmeasured: <gate>, … — by hand: <result>`. The lint checks the **structure** of the clause. A name typed by hand
proves nothing; the next Phase 0 reconcile compares counts to results where it can, as `starter-kit/HANDOFFS.md` already says of every citation.

## 3. How it is held

* **Tests:** 20 new rows in `bin/tests.sh` (25 in the block, 5 before), the five RED rows each seen failing for the reason written, a unit of behaviour per
  row: unnamed, named, too few names, backticked names, no names, the words after the names, no unmeasured field, `--all`, an older receipt, several
  citations, several clauses, a clause at a field's end, a two-digit count, a digit-led name, a citation or clause in `what_was_done`, a pending receipt.
* **The rule over the real population:** the new function over all 342 receipts flags **one**, S287 (named in prose, in a frozen shard that is never
  judged), and the live ledger passes `check-handoff --all`.
* **Mutation, two rounds** (`mutate-repair3.py`; outputs `mutate-repair3-round1-output.txt` and `-round2-output.txt`, regenerated from the committed
  script, round 1 against the tests as of `5cb11a6`): round 1, 18 mutants, 9 killed, **9 survived**, each a behaviour no test named (the most over several
  citations, the most over several clauses, the first citation only, `\s` across a field boundary, a citation or clause in `what_was_done`, a one-digit
  count, a digit-led name, a pending receipt judged). Ten rows added. Round 2: **18 of 18 killed**. In the session, round 1 ran 14 mutants (5 killed, 9
  survived: the same nine; M20 to M23 were added for round 2 and for the re-run below). Two mutants judged equivalent and not run: splitting a clause on `,`, and counting words
  instead of names, give the same count for any clause the regex matches.
* **Two defects in my own rows, found before the commit:** `$CLEAN1` was unset under `set -u`, and three rows put a citation in `what_was_done` without the commit
  sha the schema demands, so the "must be a finding" rows would have passed on the schema's error and not the lint's. Read the message, not the exit code.

## 4. The channels

* **Sync, simulated** (a project synced from a clone of `e8188a3`, then `bin/sync --dry-run` from this tree), legacy and `--layout new`: exactly two files would be
  written, the runner and `HOW_TO_USE.md`; the seed `HANDOFFS.md` reads `present (seed; left as-is)`, so an existing adopter never gets the seed's paragraph.
  So **the rule reaches an existing adopter only through the runner's one sentence** (+224 B on a file already over its 41,364 B ceiling, a reported series:
  55,361 B to 55,585 B, the read-set total 72,309 B to 72,533 B). The lint reaches an adopter only by copying `bin/check-handoff`.
* **The two open pull requests:** `git merge-tree --write-tree --name-only` of this tree against the heads of #94 (`972eb2c`) and #92 (`fa2bb5d`) lists the
  conflicts it listed before this change, and none of the files this change touches is among them (#94: `.quality-gates.json`, `starter-kit/methodology_trim.py`,
  `tools/test_methodology_trim.py`; #92: `CLAUDE.md`). The floor commit edits `.quality-gates.json`, which #94 already conflicts in.
* **This repository's own receipts:** `check-handoff-all` is a declared gate; the newest receipt cites a run that reads `0 unmeasured`, so it passes by the rule.

## 5. Not verified, not done

Not verified: Windows, GitHub CI, an adopter's own copy of `bin/check-handoff` (none is distributed), a falsified citation (the lint cannot see one), the lint on a
receipt written in another session's hand. Not done, by decision: a `quality_ratchet.py` change so `--run` prints the unmeasured gate names ready to paste
(a distributed tool change, 1.6.0, its own session if wanted); a lint on `fail` above 0, which four older complete receipts cite; the dashboard mirror of
`timeout_seconds` (BL-103's other open item).

## 6. His calls

(1) Whether `--run` should print the unmeasured names in the form the lint reads (1.6.0). (2) Whether a complete receipt may cite `fail` above 0 at all
(four did). (3) The dashboard mirror and whether 3600 s stays (S305's calls, still open). (4) D8, the release number, any tag.
