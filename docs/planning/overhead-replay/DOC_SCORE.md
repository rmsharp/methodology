# `doc_score.py`: the definitions, fixed at the end of P1a

This is the written form of plan [`documentation-quality-experiment-plan.md`](../documentation-quality-experiment-plan.md) §2.2, §2.3, §2.5, §3.4 and
§4 item 1, as the scorer implements them. The code is the authority (every number and word list below is a named constant in
[`doc_score.py`](doc_score.py)); this file says what each rule is, why, and what it cannot see. **The scorer is frozen** (§9): after the
freeze a defect is fixed only with the operator's word, everything is re-scored, and both versions of the result are reported.

Run it: `python3 doc_score.py REPO BASE PIN [--final FILE] [--task-done true|false] [--measured JSON]`. REPO is a repository holding the run
(the evidence bundle fetched into a clone, or a saved tree), BASE the install commit, PIN the pinned end sha (both in
[`pilot/doc-evidence/manifest.json`](pilot/doc-evidence/manifest.json)). Tests: `python3 tests_doc_score.py` (126 tests, 41 of them mutants).

## 1. The record (plan 2.2)

The lines the session **added** to tracked files across `BASE..PIN`, as the net diff, plus the session's final message. Excluded by path
(`NOT_RECORD_*`): code, tests, generated output and machine configuration: `R/`, `src/`, `tests/`, `man/`, `data/`, `inst/`, `bin/`, `.githooks/`,
`NAMESPACE`, `DESCRIPTION`, `test_results_summary.md`, `renv.lock`, and any `.R .py .sh .json .jsonl .yml .csv .html .Rd ...` file. The plan lists
R sources, `man/`, `NAMESPACE`, test files and `test_results_summary.md`; the other entries are the same kinds of file in this project's tree. Included:
everything else, so `SESSION_NOTES.md`, `HANDOFFS.md`, `CHANGELOG.md`, `NEWS.*`, `docs/`, `vignettes/`.
**Moved lines are not the record:** an added line is dropped when the same line, whitespace-stripped, is deleted from *any* file in the range. **A line
copied from the base and not deleted elsewhere stays,** because carrying a stale line forward is what the measure is for. The install commit is
`BASE` and so is never in the range. The diff is read by hunk counts (`-U0`), so a content line that begins `++` is not taken for a file header.
The final message at the pin is the last assistant text between the pin commit's time and the next human turn (`final_message`).

## 2. M1: checkable-reference accuracy (plan 2.3)

Distinct references in the record, each checked against the **pin** tree. Reported by kind and pooled; `failures` names every reference that did not verify.

| Kind | Extracted | Verified when | Calibration notes |
|---|---|---|---|
| sha | 7 to 40 hex characters with a digit and a letter (or any hex token on a line that says `commit`/`sha`/`hash`/`rev`); not in a URL; not after `results`, `manifest`, `sha256`, `md5`, `digest`, `checksum` (also across a wrapped line) | resolves to a commit **and** is reachable from the pin | the ratchet's `results x · manifest y` digests were being read as commits |
| path | a token ending in a known extension (bare or backticked: receipts cite paths bare); `A.md/B.md` is two files; not absolute, `~`, `..`, a placeholder, a host name, or one of `dashboard.html`, `dashboard_history.jsonl`, `.quality-gates-results.json`, `.context-budget-history.jsonl` (tool output nobody commits) | exists at the pin (a bare file name: anywhere in the tree by basename) **or** is stated removed: `STATED_REMOVED` matches in the line, the two before it or the one after (a list follows its verb) | `git rm`, `stale`, `never had` count as saying so |
| `path:line` anchor | `path:N` or `path:N-M`; a bare `` `:28` `` is **not** an anchor | file exists (or stated removed), the line is within the file, **and, if a backticked identifier sits directly beside the anchor** (`BESIDE_GAP` = 10 characters of punctuation or at/in/of/see/near/line), that identifier occurs within `ANCHOR_WINDOW` = 5 lines of it **or is the function that encloses the line** | the enclosing-function clause was added from a hand-read: `assignAlleles()` at `R/assignAlleles.R:45` is the call site, 14 lines below the definition |
| test count | from the **final message only**: `passed=N failed=N warnings=N files=N`, the testthat `FAIL | WARN | SKIP | PASS` line, or prose `N pass/fail/warn` on a sentence that also says *suite* (or testthat, all tests); nothing from a line that speaks of another state (baseline, before, was, `->`) or of a gate summary (`4/4 pass`, `quality_ratchet`, `unmeasured`) or of R CMD check; per kind, the **last** claim | equals the supplied measurement, for a kind the measurement has | counts stated mid-record are intermediate states (`passed=5568` before a deletion); the number stated elsewhere is kept as `claimed_elsewhere` |

**Ceiling rule** (`m1_at_ceiling`, `CEILING` = 0.95): if M1 is at or above 0.95 in every saved run it is reported as uninformative and is not a headline; a run
with nothing checkable cannot show a defect and does not break the ceiling. The test-count part is the only part that needs the R suite, so it is applied only
where a measurement exists (the ratchet study's rows carry `final_measure`) and the report says so.

## 3. M2: action coverage and stub resolution (plan 2.3), three parts, never summed

* **(a) commits named.** Every commit in `BASE..PIN` **except the pin commit** (it cannot name its own sha; reported apart as `pin_commit_named`) is named in the record by sha
  (a 7-or-more character prefix) or by its whole subject with the `type(scope):` prefix removed, whitespace-normalised. Strict by design: a paraphrase does not count.
* **(b) stubs left.** Defined only where the installed runner has such an artifact (`status: pending` or `CHANGELOG: pending` in its `SESSION_RUNNER.md` at `BASE`). Where it has not (v3.0)
  `b` is `None`, "not applicable", never a pass; the descriptive count is kept as `b_descriptive`. Counted: a `status: pending` receipt in `HANDOFFS.md` at the pin that is
  **not present verbatim at the base** (so the start state's own orphan stub is never the session's), and an added `Ledger: ... CHANGELOG: pending` line still present. The `commit:` slot is
  **not scored** (it may legitimately read `pending`); it is reported as `commit_slot`.
* **(c) done against the task's check.** `says_done`, the first of the two keyword rules: a task word (`task`, `deliverable`, `status`, `active_task`, `#N`, `issue N`) within 100
  characters **before** a done word (`done`, `complete(d)`, `finished`, `resolved`, `shipped`, `delivered`, `closed`, `fixed`), with no negator or qualifier (`not`, `never`, `n't`, `rather than`,
  `incomplete`, `partial`, `pending`, `in progress`, `still`, `only`, `until`, `once`, `when`, `if`, `before`) within 40 characters before it or `partial`/`except`/`but not`/`not yet` within 15 after;
  a receipt's own `status:` field is the close-out's status and is never read. The flag is `says_done and task_done is False`; with no task check supplied `c` is `None`.

## 4. M3: no target yet (plan 3.4)

Fixed now so it cannot be fitted to a result: `classify_path` (historical: `CHANGELOG.md`, `SESSION_NOTES.md`, `HANDOFFS.md`, `PROJECT_LEARNINGS.md`, `TECH_DEBT_AUDIT_2026-05-30.md`, `test_results_summary.md`,
anything under `docs/planning/` or `docs/archive/`; live: `README*`, `NEWS*`, `CLAUDE.md`, `vignettes/`, and the pkgdown config pkgdown reads: root `_pkgdown.yml`, not `inst/_pkgdown.yml`, which is shadowed), and
`discloses`, the second keyword rule: a record line names the document (path or basename, not a longer name) and `DISCLOSES` (`stale`, `out of date`, `outdated`, `obsolete`, `still lists/names/mentions...`,
`not updated/touched/edited/regenerated`, `left untouched/unchanged/as is`, `needs updating`) matches in the same two-before, one-after window. Every M3 verdict is hand-read.

## 5. Inclusion and pins (plan 2.5)

`reached_closeout`: a run is scored when it has a commit in `BASE..PIN` whose subject says close-out, hand-off or wrap-up and does **not** say claim (a claim commit may name "the pending handoff receipt"
it opens), or a `status: complete` receipt at the pin that is not at the base. No run is dropped for cost or correctness. Applied to the 41 saved runs it excludes exactly three: `real-3.7/v3.0-r2`,
`real-3.7/v3.7-r1`, `t-control-fix/R1-r1` (each cut off at the driver's stop limit), leaving v3.0 n=5, v3.7 n=6, v3.8-text n=12 and T-remove n=15. The pins are in the manifest (HEAD for 38 runs;
`real-3.7/v3.7-r2` `7b9bd618`, `real-3.7/v3.0-r3` `b15ae1c5`, `t-remove/R0-r5` `3aa6c2b9`).

## 6. M4: the key builder and the report scorer (plan 2.3)

`build_key(repo, base, pin)` takes **only** a repository, a base and a pin (a test pins the signature). **Git-derivable facts:** the session id (the most common `S<N>` in its commit subjects), the
deliverable terms (`#N` issue references and `name()` identifiers in the deliverable commit's subject), the deliverable commit (the last `fix`/`feat`/`refactor`/`perf` commit, else the last `test`/`chore`/`build`),
whether the work is complete (the pin commit says close-out and no stub is left), and no uncommitted changes (a clone is clean). **Record-only facts:** the paths and shas in the record's `Key files` and `Next steps`
parts (a labelled paragraph runs to a blank line, a heading, a fence or the next receipt field; a receipt's `key_files:` and `next_steps:` fields are parts). **The ledger-or-ghost finding** has no v3.0 counterpart: it is
reported on its own line (`ledger_finding_reported`) and is in no arm's denominator. `score_report(key, report)` scores each fact stated or not, the record-only fraction, and the ledger line apart; a cold session's
M4 is the score with the record minus the score without it (P3). The report scorer has only fixtures: no cold probe exists until P2.

## 7. What the scorer cannot see (state it beside every result)

* **M1 sits at a ceiling on the calibration set** (the 15 T-remove trees: 13 at 1.000, one at 0.979, one at 0.939) because the project's own `CLAUDE.md` carries the rules into every arm. It says nothing yet about the rule-free start.
* An anchor with **no identifier beside it is a range test**, which most anchors are (2 of the 22 hand-read anchors had one): a wrong line inside the file passes.
* A bare `` `:28` `` after a function name is not checked; neither is a commit cited only inside a URL.
* **`STATED_REMOVED` is a broad keyword list** (it includes `replac*`, `renam*`, `moved to`, `stale`) and errs toward verifying a missing path: a record that says "replaced with `R/typo.R`" verifies a path that never existed.
* **M2(b)'s `CHANGELOG: pending` check is a line shape** (`Ledger: ... CHANGELOG: pending`): a session that writes *about* the marker in that exact shape would be counted as leaving one. None did on the calibration set.
* **Subject matching in M2(a) is strict**, so a session that describes a commit in its own words and cites no sha scores as not naming it.
* `says_done` is a keyword rule over prose; it was wrong once on the calibration set ("stated rather than closed (... CI status)") and is fixed, and will be wrong again somewhere. It is hand-read wherever it decides a flag.
* The test-count part needs a measurement; the harness's own re-run may differ from a session's by environment (R1-r4 stated 5,562 passed and 0 failed against a measured 5,560 and 2).
* The cold-probe measures (M4) and the model rater (M5) are not exercised here.

## 8. What the calibration changed

See [`pilot/doc-evidence/CALIBRATION.md`](pilot/doc-evidence/CALIBRATION.md): what was run, which trees were hand-read for each measure, and the sixteen rule changes the hand-reads produced, each with its test and mutant.

## 9. The freeze

[`doc_score.frozen`](doc_score.frozen) holds the sha-256 of `doc_score.py` and the date; `test_the_scorer_is_the_frozen_one` fails if the file differs. Before P1b scores anything, run
`python3 tests_doc_score.py`. `erosion_score.py` and `remove_score.py`, the earlier frozen scorers, are untouched.
