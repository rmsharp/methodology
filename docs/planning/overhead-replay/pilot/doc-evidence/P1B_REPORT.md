# P1b: the saved runs scored once (BL-94, S257)

Plan: [`documentation-quality-experiment-plan.md`](../../../documentation-quality-experiment-plan.md) §5 P1b. Cost: **$0, no model run.** The frozen scorer ([`doc_score.py`](../../doc_score.py), sha-256 `eaec3a2ec9c6`, [`doc_score.frozen`](../../doc_score.frozen)) was run **once** over the saved v3.0, v3.7 and v3.8-text runs by [`p1b_score.py`](../../p1b_score.py). Nothing was re-scored and the scorer was not touched.

## The answer

1. **On the two mechanical measures the three versions are indistinguishable on this start state, and every arm sits at or near the ceiling.** M1 (cited references that check out) is 0.984 (v3.0, n=5), 0.990 (v3.7, n=6), 0.990 (v3.8-text, n=12); the closest pair of means is 0.000 apart and the furthest 0.006, with permutation p from 0.62 to 0.97. M2(a) (every commit named) is 1.000, 0.967, 1.000. v3.7 and v3.8-text left no stub (v3.0 has no stub artifact, so that part is not comparable).
2. **Hand-reading the failures moves M1 closer still.** Of the 13 references the scorer held against the records, **11 are scorer false positives**, 1 is a sha the record says was amended away, 1 is a harmless stale carry-forward. Counting all 11 as verified (arithmetic on the saved scores, not a re-score) gives 1.000, 1.000 and 0.997.
3. **The versions differ in what the record contains and what the session does, not in how accurate the record is.** The v3.7 and v3.8-text records carry 51 and 56 checkable references per run against 33 for v3.0 (receipts bring shas and `path:line` anchors); sessions make 3.4, 5.6 and 5.2 commits to the pin (v3.0 against v3.7 permutation p = 0.008, against v3.8-text 0.002); cost is $2.69, $3.20, $3.46 per run (v3.0 against v3.7 p = 0.016, which is S237's own finding; against v3.8-text 0.13).
4. **One run claimed the task done when the answer key says it is not: `v3.0-r4`** (1 of 5; 0 of 18 in the other arms). The scorer raised two more flags, both false positives (`t-control/R1-r1` and `R1-r4` say plainly that #121 is *not* fixed).
5. **Pooling v3.8-text with S237's arms is not supported for process rows**, and is a screen, not a test, for the record measures (below). **The plan's §3.8 sample-size figure comes out as 1 to 3 runs per arm at a difference of 0.20, which is the finding that M1 and M2(a) have no headroom, not a sample-size recommendation.**

**What this does not say.** It says nothing about M3 (staleness, no task exists), M4 (cold-start reconstruction, no probe has run) or M5 (blind usefulness), and nothing about growth of the record over many sessions, crash recovery or the trimmer, none of which a single session's end state can show (plan §2.4). It is one start state, one model, one project.

## What was run

`python3 docs/planning/overhead-replay/p1b_score.py score docs/planning/overhead-replay/pilot/doc-evidence/p1b-scores.json` (refuses to start unless `doc_score.py` equals its frozen hash, and refuses to overwrite its own output). **26 runs gathered, 23 scored** under the plan 2.5 inclusion rule (`reached_closeout`): left out, as P1a said, `real-3.7/v3.0-r2`, `real-3.7/v3.7-r1`, `t-control-fix/R1-r1` (each cut off at the driver's stop limit). Inputs, each read before scoring (`p1b_score.py inputs`, which computes no score):

| Input | v3.0 and v3.7 (S237, set `real-3.7`) | v3.8-text (`t-control`, `t-control-fix`; R0 and R1) |
|---|---|---|
| Pin | HEAD, except `v3.7-r2` `7b9bd618` and `v3.0-r3` `b15ae1c5` | HEAD |
| Final message | the transcript, cut at the pin commit's time (`doc_score.final_message`) | same |
| Task check | `pilot/real-3.7/held_out_results.json`: no failures and no errors in any held-out file | the row's own `ratchet.task_done` (the held-out run made when the row was written) |
| Measured counts (M1 d) | none: S237's rows carry no `final_measure` | the row's `final_measure` |

The two override runs' final messages were read before scoring (S256 gotcha 6): each is the first close-out's own report, dated at the pin, and S237's cost, request and tool-call rows are cut at that close-out by hand. **The driver's first "commits" column counted to HEAD** (v3.7 rep 2 has 13 commits past its pin); it was corrected to commits to the pin from the scorer's own range before any figure was used, and no score changed. Reproduce every table: `python3 docs/planning/overhead-replay/p1b_score.py report docs/planning/overhead-replay/pilot/doc-evidence/p1b-scores.json` (saved as [`p1b-report.txt`](p1b-report.txt)). Driver tests: `python3 docs/planning/overhead-replay/tests_p1b.py` (20 tests; 10 mutants, all killed).

## Each measure by arm (sample sd; scored runs)

| | v3.0 (n=5) | v3.7 (n=6) | v3.8-text (n=12) |
|---|---|---|---|
| Record lines, mean (sd) | 161.6 (20.0) | 158 (45.5) | 170.5 (36.4) |
| **M1** mean (sd) · min | **0.984** (0.024) · 0.947 | **0.990** (0.011) · 0.977 | **0.990** (0.016) · 0.962 |
| Checkable references per run | 32.6 | 51.3 | 56.2 |
| M1 by kind (verified/checkable): shas · paths · anchors · counts | 15/15 · 84/87 · 61/61 · 0/0 | 42/42 · 159/161 · 104/105 · 0/0 | 85/86 · 368/373 · 206/206 · 8/9 |
| M1 failures | 3 | 3 | 7 |
| **M2(a)** commits named, mean (sd) | **1.000** (0.000) | **0.967** (0.082) | **1.000** (0.000) |
| Commits not named | 0 of 12 | 1 of 27 | 0 of 50 |
| **M2(b)** stubs left | n/a (no stub artifact) | 0 | 0 |
| **M2(c)** flags (task check supplied) | 1 of 5 | 0 of 6 | 2 of 12 |
| **M2(c)** after hand-read | **1 true** | 0 | **0 true (2 false positives)** |
| Said done / task not done | 5 / 1 | 5 / 1 | 12 / 2 |
| `commit:` slot reads pending (descriptive) | 0 | 0 | 4 |
| Cost USD (sd) · requests · tool calls · commits to the pin | 2.69 (0.31) · 60 · 85 · 3.4 | 3.20 (0.18) · 70 · 96 · 5.6 | 3.46 (1.04) · 74 · 100 · 5.2 |

Process rows use S237's cost-valid set (v3.7 rep 5, the honest partial that closed out at the RED gate, is out of the cost rows and nothing else; its cost-valid v3.7 against v3.0 is +19%, the figure S237 reported). Pairwise permutation p (exact, two-sided, in the order v3.0~v3.7, v3.0~v3.8-text, v3.7~v3.8-text): M1 0.62, 0.64, 0.97; M2(a) 1.00, 1.00, 0.33; and for the process rows, in the same order (v3.0~v3.7, v3.0~v3.8-text, v3.7~v3.8-text): cost 0.016, 0.13, 0.60; requests 0.032, 0.16, 0.72; tool calls 0.079, 0.12, 0.66; commits to the pin 0.008, 0.002, 0.37 (full list in `p1b-report.txt`; uncorrected, small n).

**M1 ceiling rule (plan 2.3), literally:** not met, because one run (`v3.0-r3`) is 0.947, two references under 0.95, and both are false positives (below). **In effect it holds:** 22 of 23 runs are at 0.962 or above and the hand-read arm means are 1.000, 1.000, 0.997. M1 is not a headline.

**§3.8 sigma and n per arm** (`n = 15.7 sigma^2 / d^2`, d = 0.20; a t-test needs about one more): M1 sigma 0.024, 0.011, 0.016, so n = 1 for each; M2(a) sigma 0, 0.082, 0, so n = 3 for v3.7 and undefined for the other two. These say the measures have no room for a 0.20 difference, not how many runs to buy.

## Hand-reads (plan §4 item 2)

**All 13 M1 failures, each read in its record with its neighbouring lines:**

| Run | Reference | What the record says | Verdict |
|---|---|---|---|
| `v3.0-r3` | `PED_GV_AUDIT_2026-05-30.html` | quotes the previous handoff's "not committed" note to say it did not match this checkout | false positive (names a file to say it is not there) |
| `v3.0-r3` | `tests/testthat/test_X.R` | a command template, `X` is a placeholder | false positive (placeholder) |
| `v3.0-r5` | `PED_GV_AUDIT_2026-05-30.html` | same quoted note | false positive |
| `v3.7-r2` | `full_suite.R` | a scratch script named in a process slip (`pgrep -f full_suite.R`), never committed | false positive (never in the tree) |
| `v3.7-r4` | `PED_GV_AUDIT_2026-05-30.html` | "its 'Not committed' note did not apply here (tree was clean)" | false positive |
| `v3.7-r6` | `NEWS.Rmd:17-20` | the list `` `NEWS.Rmd:17-20`, `NEWS.md` (same bullet) ``: the next file in the list was taken as the identifier beside the anchor | false positive (rule artifact) |
| `t-control/R0-r1` | sha `846a49b1` | "the local, never-pushed commit was amended (`846a49b1` to `e49292b3`)" | **true by the plan's rule** (a sha must resolve and be reachable); accurate by a reader's standard, it says it was replaced |
| `t-control/R0-r1` | `.quality-gates.json` | "No .quality-gates.json so no ratchet line" | false positive (a statement of absence) |
| `t-control/R0-r2` | `.quality-gates.json` | same | false positive |
| `t-control/R0-r2` | `script.R` | a command template | false positive (placeholder) |
| `t-control/R0-r3` | `.quality-gates.json` | same | false positive |
| `t-control/R0-r3` | count "7 warnings", measured 0 | "0 errors and 0 warnings. So all 7 warnings are gone." | false positive ("gone" is not a baseline word) |
| `t-control-fix/R1-r4` | `PED_GV_AUDIT_2026-05-30.html` | "pre-existing `.DS_Store` / `PED_GV_AUDIT_2026-05-30.html` untouched": the file is not in this checkout | **real, harmless** (a stale start-state note carried forward) |

So 11 false positives, 1 true by rule, 1 real. **The false positives are not spread evenly:** three of the six R0 failures are absence statements ("no .quality-gates.json") that the R0 arm, having no ratchet, writes by design. They fall in four families (names a file to say it is absent or never committed: 7; placeholder: 2; anchor identifier taken from the next listed file: 1; count taken from a "gone" sentence: 1).

**M2(a), the one unnamed commit.** `v3.7-r3`: of its five session commits it names four by sha; `0a121159` ("NEWS entry ... + Learning 292") is described in the ledger's Files line (`NEWS.Rmd`, "Learning 292") but its sha and subject appear nowhere. The strict rule is doing what it was written to do; a reader would say the work is recorded.

**M2(c), every flag and the `says_done` line that decided it.**

| Run | Task | `says_done` line | Verdict |
|---|---|---|---|
| `v3.0-r4` | not done (4 held-out failures; S237: "repaired test fixtures only") | "**Status:** **DONE.**" and the final message "Issue #121 is fixed ... The change is test-only" | **true flag**: it says fixed; the answer key's production fix is absent |
| `t-control/R1-r1` | not done | "**Status:** **Research + RED DONE; GREEN not started.**" (and "Deliverable (PARTIAL) ... #121 is not fixed") | false positive: a phase, and the record says the opposite |
| `t-control/R1-r4` | not done | "**Status:** **RED committed (`7333b23a`), then closed out at the owner's direction**" | false positive: "closed out" is the session |
| `v3.7-r5` (no flag) | not done | none | true negative: "#121 is still open and HEAD is deliberately red" |

## Section 2.4 expectations

| # | Expected | Result |
|---|---|---|
| H1 | M1: no difference | **Met.** 0.984 / 0.990 / 0.990, p 0.62 to 0.97; at or near ceiling |
| H2 | M2 higher in v3.7 and v3.8, by design | **Not met on M2(a):** v3.0 names all 12 of its commits (1.000), v3.7 26 of 27, v3.8-text 50 of 50. M2(b) is not comparable (v3.0 has no stub artifact). The one visible direction is M2(c) (1 true flag in v3.0, none elsewhere), which is one run |
| H3 | M3: no difference expected | **Not run** (no task) |
| H4 | M4: plausible, uncertain | **Not run** (no probe) |
| H5 | M5: unknown | **Not run** |

## Pooling check (plan 5 P1b)

Defined in `p1b_score.py`'s docstring before any figure was read.

* **No arm appears in two batches except R1.** v3.0 and v3.7 are S237's (2026-09-29, CLI 2.1.285 and 2.1.286); v3.8-text is the ratchet study's (2026-10-01 and 10-02, CLI 2.1.287). So arm and batch are confounded for every v3.0-or-v3.7 against v3.8-text comparison, and the data cannot separate them.
* **The one within-arm batch contrast is large.** R1 with the old close-out reply (n=5) against R1 with the corrected one (n=4, one more cut off at the stop limit): cost $2.78 against $4.01 (+44%, permutation p = 0.071), requests 62 against 83 (p = 0.087), tool calls 88 against 108 (p = 0.119), commits to the pin 4.4 against 5.8 (p = 0.079). That is larger than any between-arm cost difference in the table (v3.7 against v3.0 +19%), and the two batches differ only in reply wording and a day.
* **Span:** 6 of 12 v3.8-text runs have cost inside the span of v3.0 and v3.7 together ($2.27 to $3.41), 7 of 12 requests, 7 of 12 tool calls, 11 of 12 commits.
* **On the record measures the batches agree:** R1 old reply M1 1.000, fixed reply 0.995, R0 0.966 (its six failures: five false positives and the amended sha); M2(a) 1.000 in all three.

**Verdict.** v3.8-text may be compared with v3.0 and v3.7 on M1 and M2 as a screen, which is all P1b asked of it. It may **not** be pooled on process rows (cost, requests, tool calls) without carrying the reply covariate, and that covariate cannot be separated from the arm for S237's runs. A probe on the saved end states (M4) reads the record, not the run's cost, so it is less exposed to this; new v3.8 task runs are not forced by this result.

## What the freeze held, and what an amendment would do

No defect in the frozen scorer was fixed; the amendment rule (plan §4 item 1: the operator's word, re-score everything, report both) was not invoked. The false positives above are the proposal's whole content: (a) a path named to say it is absent, never committed or quoted from a stale note (`no X`, `did not match`, `did not apply`, `untouched`); (b) placeholder file names (`test_X.R`, `script.R`); (c) the identifier beside an anchor taken from the next file in a list; (d) `gone` and `fixed` as baseline words in a count sentence; and, for `says_done`, (e) "RED done" and "closed out" read as the deliverable. **Recommendation: do not amend.** The counted what-if is 1.000, 1.000, 0.997, so no conclusion above moves, and an amendment re-scores 38 trees (the 15 T-remove calibration trees included) for no change. If M1 were ever used as a headline on a start state without a ceiling, these five families are the first things to fix.

## The stop: D3 and D4 reconsidered

Plan §7 D3: *"if v3.0 against v3.7 and v3.8 shows nothing at all on M1 and M2, that case [for spending on probes] is weaker."* It shows nothing at all on M1 and nothing on M2(a), and the plan said it would (H1). What it does not touch is the measure the plan called plausible, M4, because a single session's end state cannot show what the receipts, ledger and reconcile are for. The spend decision (D4, $100, $0 spent) is yours; P2a is the next phase and costs nothing.
