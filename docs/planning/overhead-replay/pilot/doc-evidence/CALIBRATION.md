# Calibration of `doc_score.py` on the T-remove trees (BL-94 P1a (e))

**What was run.** The scorer, built from the committed evidence bundle alone (`doc_evidence.rebuild`, no run tree read), over the 15 T-remove trees: start `402a6b5b`, where the
project's own `CLAUDE.md` already carries the ledger, reconcile and receipt rules, so every arm (v3.0 too) wrote v3.8-era records. That set is the plan's negative control and noise-floor set (P1).
**The v3.0, v3.7 and v3.8-text sets were not scored**: the smoke test over all 41 printed parse facts only (counts of lines, references, receipts), and the inclusion rule is a yes or no on whether a close-out exists.
Task check (`remove_score.task_done`), final message (the transcript, cut at the pin commit's time) and the measurement (`rows.jsonl` `final_measure`) were supplied as P1b will supply them.
Output: [`calibration-t-remove.json`](calibration-t-remove.json) (frozen scorer, every reference and every failure).

## Hand-read, three or more trees per measure (plan section 4, item 2)

| Measure | Trees read | How |
|---|---|---|
| M1 | `R1-r4`, `R1-r1` (counts); `R0-r3`, `v3.0-r5`, `R1-r3` (paths, anchors, shas); then `R1-r2`, `v3.0-r3`, `R0-r5` re-read after the changes; **every remaining failure across all 15**; every anchor in `v3.0-r1` and `R0-r2` (22) beside the file's lines at the pin | each flagged reference opened in the tree; each verified anchor compared to the real line |
| M2 | `R0-r1`, `R1-r4`, `v3.0-r2` | each session commit against how the record names it; receipts at the pin and their status; the line that made `says_done` true |
| M4 key | `R0-r1`, `R1-r4`, `v3.0-r2` | each key fact against the tree's commit subjects and receipts |
| Pin and final message | `R0-r5` (two sessions) | the final message chosen is S555's account of the deletion; no S556 text is in the record; the pin override is exactly the pin |

## What the hand-reads changed: sixteen rule changes, each with a test and, where a decision could be broken in isolation, a mutant

| # | Found in | Finding | Change |
|---|---|---|---|
| 1 | first test run | `inst/_pkgdown.yml` classed live; plan 3.4 says the config pkgdown reads, and that one is shadowed | live is the root `_pkgdown.yml` only |
| 2 | `R1-r4` | `4/4 pass · 0 fail · 0 unmeasured` (the ratchet's gate summary) read as test counts | `NOT_TEST_COUNT` |
| 3 | `R1-r1` | `passed=5562 failed=0` paired as "5562 failed" | `passed=N` pairs by its own key |
| 4 | `R1-r1` | `3 + 3 passing assertions` (two deleted files) read as a suite count | prose counts need *suite* in the sentence |
| 5 | `R1-r1` | `passed=5568` (before a deletion) was the last claim | counts come from the final message only, last of each kind; the rest is `claimed_elsewhere` |
| 6 | `R0-r3`, `v3.0-r5` | `git rm` of a path, and a record calling an anchor `stale`, were not read as saying it is gone | added to `STATED_REMOVED` |
| 7 | `R0-r3`, `R1-r3`, `v3.0-r5` | a wrapped list puts its verb ("removed") lines above the paths | the window is two lines before, one after |
| 8 | `R0-r3`, `v3.0-r5` | `SESSION_NOTES.md/HANDOFFS.md` read as a directory | split where a segment ends in a known extension |
| 9 | `v3.0-r5`, `R1-r3` | `dashboard.html` and `.quality-gates-results.json` are written by tools and never committed | listed as tool output, not checkable |
| 10 | `R1-r3`, `R1-r4` | the ratchet's `results x · manifest y` digests read as commits | a hex token after `results`/`manifest`/`sha256`... is not a sha |
| 11 | `R1-r3`, `R1-r4` | the same digest split across a wrapped line | the previous line's tail is read too |
| 12 | `R0-r2` | `assignAlleles()` at `R/assignAlleles.R:45` is the call site, 14 lines below the definition | an identifier that names the enclosing function verifies |
| 13 | `R0-r1` | "stated rather than closed (... CI status)" read as done | the task word must come **before** the done word |
| 14 | `R0-r1` | the same sentence has no negator | `rather than` negates |
| 15 | inclusion check over all 41 | claim commits that name "the pending handoff receipt" counted as close-outs, so only 1 of 3 cut-off runs was left out | a subject that says claim is not a close-out |
| 16 | writing the M4 fixtures | a later `test:` commit would have been named the deliverable | a fix, feature or refactor is the deliverable; a test or chore only if there is none |

## What the finished scorer holds against T-remove

**4 of 626 checkable references fail (622 of 626), and all four are real**: `SESSION_NOTES.md:23229` in `R1-r1` (the file has 2,011 lines); `fb30bc57` in `R1-r4`, a commit the record calls superseded and that
no longer exists (strict by the plan's rule: a sha must resolve and be reachable); and `R1-r4`'s closing message stating 5,562 passed and 0 failed against the harness's measured 5,560 and 2 (the harness's re-run may differ
from the session's by environment; not resolved here).

| Tree | Record lines | M1 ok/checkable | M1 | shas | paths | anchors | counts | M2(a) named | M2(b) left | says done / task | key complete |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `R0-r1` | 241 | 39/39 | 1.000 | 7/7 | 27/27 | 5/5 | 0/0 | 3/3 | 0 | yes / task done | yes |
| `R0-r2` | 241 | 46/46 | 1.000 | 8/8 | 27/27 | 11/11 | 0/0 | 3/3 | 0 | yes / task done | yes |
| `R0-r3` | 222 | 45/45 | 1.000 | 7/7 | 32/32 | 6/6 | 0/0 | 3/3 | 0 | yes / task done | yes |
| `R0-r4` | 222 | 47/47 | 1.000 | 9/9 | 33/33 | 5/5 | 0/0 | 3/3 | 0 | yes / task done | yes |
| `R0-r5` | 218 | 41/41 | 1.000 | 8/8 | 29/29 | 4/4 | 0/0 | 3/3 | 0 | yes / task done | yes |
| `R1-r1` | 248 | 47/48 | 0.979 | 8/8 | 32/32 | 6/7 | 1/1 | 4/4 | 0 | yes / task done | yes |
| `R1-r2` | 239 | 48/48 | 1.000 | 8/8 | 31/31 | 9/9 | 0/0 | 4/4 | 0 | yes / task done | yes |
| `R1-r3` | 299 | 61/61 | 1.000 | 11/11 | 36/36 | 11/11 | 3/3 | 4/4 | 0 | yes / task done | yes |
| `R1-r4` | 212 | 46/49 | 0.939 | 10/11 | 28/28 | 8/8 | 0/2 | 4/4 | 0 | yes / task done | yes |
| `R1-r5` | 146 | 27/27 | 1.000 | 5/5 | 17/17 | 5/5 | 0/0 | 2/2 | 0 | yes / task done | yes |
| `v3.0-r1` | 184 | 37/37 | 1.000 | 5/5 | 21/21 | 11/11 | 0/0 | 2/2 | n/a | yes / task done | yes |
| `v3.0-r2` | 188 | 28/28 | 1.000 | 6/6 | 18/18 | 4/4 | 0/0 | 3/3 | n/a | yes / task done | yes |
| `v3.0-r3` | 194 | 34/34 | 1.000 | 7/7 | 24/24 | 3/3 | 0/0 | 3/3 | n/a | yes / task done | yes |
| `v3.0-r4` | 167 | 39/39 | 1.000 | 6/6 | 23/23 | 10/10 | 0/0 | 2/2 | n/a | yes / task done | yes |
| `v3.0-r5` | 253 | 37/37 | 1.000 | 5/5 | 25/25 | 7/7 | 0/0 | 2/2 | n/a | yes / task done | yes |

**By arm** (population sd; n=5 each):

| Arm | n | M1 mean | M1 sd | M1 min | checkable per run | M2(a) coverage | M2(b) |
|---|---|---|---|---|---|---|---|
| R0 | 5 | 1.000 | 0.000 | 1.000 | 43.6 | 1.000 (all) | 0 left (all) |
| R1 | 5 | 0.984 | 0.024 | 0.939 | 46.6 | 1.000 (all) | 0 left (all) |
| v3.0 | 5 | 1.000 | 0.000 | 1.000 | 35.0 | 1.000 (all) | n/a (v3.0 has no stub) |

## What this says, and what it does not

* **The scorers do not invent defects on honest records**: after the changes above, the only failures left are ones a person would also call inaccurate. That is the calibration's claim and no more.
* **T-remove is at a ceiling, as the plan said it would be (finding 1)**: M1 is 0.939 to 1.000 with sd 0 to 0.024, M2(a) is 1.000 in all 15, M2(b) is zero left in all ten R0 and R1 trees (v3.0 has no stub artifact, so it is "not applicable"), and no done claim is flagged. The project's own
  rules carry the documentation behaviour into every arm, v3.0 included, so these trees cannot separate the versions and **this calibration cannot show that the scorers *detect* defects at realistic rates**: detection rests on the fixtures
  and the 41 mutants (`tests_doc_score.py`), and on the four real failures above. Whether M1 and M2(a) have any spread on the rule-free start state (`879503cce`) is what P1b will show.
* **No STOP condition of plan P1a fired.** The tree and base shas were all found; every bundle rebuilds its pin; the noise floor is not "so wide that no plausible difference could show": it is narrow, a ceiling.
* The anchor check is mostly a range test: of the 22 anchors read by eye, 2 had an identifier beside them.
