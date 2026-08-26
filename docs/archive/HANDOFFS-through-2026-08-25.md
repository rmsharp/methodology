# HANDOFFS.md — archive: 2026-08-25 → 2026-08-25

Retired records from [`HANDOFFS.md`](../../HANDOFFS.md), moved here so the live ledger stays small enough to read
in one pass. Same format, same newest-on-top order — this is the same ledger, continued.

Holds **2 record(s), 2026-08-25 → 2026-08-25**. Cut key: `2026-08-25`. Counts here are computed from the file
itself, never carried forward. This shard is frozen: it states no forward-looking rule,
because the live file owns those and a copy of one was wrong a day after it was written.

---

```handoff
session: S106
date: 2026-08-25
status: complete
self_score: 8
predecessor_score: 7
active_task: **Phase 1 of [`docs/planning/record-budget-reduction-plan.md`](docs/planning/record-budget-reduction-plan.md) — `RECORD_BUDGET_BYTES` 18,432 -> 12,288. COMPLETE.** The operator ratified 12,288 over the costed 10,240 / 8,192, settling §9's one blocking decision. Four files: `bin/check-handoff`, `bin/tests.sh`, `.context-budget.json`, the plan's status header. **NOT DONE, each deliberately:** Phase 2, Phase 3, the 65,536 B ceiling, Test 34's floor of 3, and **the `HANDOFFS.md` trim, which was due when I arrived and which I did not run** (FM #26 — next_steps (a)). **NO OUTWARD-FACING ACTION. No distributed file touched:** neither `bin/` file has a row in `bin/_manifest.py`, so no adopter receives any of this.
what_was_done: Three commits — `3ecaf2e` (1B claim), **`6ebe84d` the deliverable**, this close-out. **(1) THE PLAN'S MANDATORY INVENTORY WAS INCOMPLETE BY TWO SITES, FOUND BY RE-RUNNING THE GREPS INSTEAD OF READING ITS TABLE.** §5.2 listed nine `bin/tests.sh` couplings; there are **thirteen**. **`:2833-2837` is the dangerous one — left alone it stays GREEN while testing nothing.** It is the one-byte-over half of the edge test (`add_record38 18433`), missed because the inventory's grep pattern `18,?432` **cannot match the derived neighbour `18433`**. At 18,433 against a 12,288 budget the record is still over budget, so the row still passes — while exercising a record **6,145 B** past the cap instead of one byte past it, leaving the `>` -> `>=` boundary mutant (M1) scored *killed* by a record any budget catches. Its at-budget twin `:2827` fails loudly; only this half is silent. **`:2946`** is M3's forged summary payload — inert (the assertion only looks for the absent `SKIPPED` marker), but its job is to be a convincing forgery of a line the code can emit. Both fixed, and the correction is written into the plan under §5.2 so Phase 2/3 inherit it rather than repeat it. **(2) I DECLINED TO ADD THE EXECUTABLE FIT ASSERTION** — it would make a mutant pass for the wrong reason; next_steps (b). **(3) THE DERIVED OVERAGE WAS RECOMPUTED, NOT SEARCH-REPLACED** (plan risk 3): `:2820` asserts `by 7,712` (20,000 − 12,288). The suite proves the arithmetic — that row greps for the exact string and would have reddened had I got it wrong. **(4) THE ZERO-HIT TRIPWIRE WAS KEPT REAL:** two past-tense sentences still named 18,432; rather than exempt them I rewrote them as **"18 KiB"** — identical fact, and `git grep -nE '18,?432' -- bin/` stays a live detector.
next_steps: (a) **THE `HANDOFFS.md` TRIM IS THE OBVIOUS NEXT DELIVERABLE.** It was due before I arrived. `--check` FIRES on both triggers; a `--cut 3` dry run at Orient reported **L1/L2/L3 OK, 1 of 4 records archived, 67,966 -> 51,375 B**. **Re-run it — I have prepended a record since, so that arithmetic is stale by construction.** `--cut 3` remains the floor (Test 34). **This is also why the plan's Phase 1 verification list is wrong on one line:** it requires `context_budget.py` exit 0, which Phase 1 **cannot** satisfy — the breach is the WHOLE-FILE ceiling, and the plan's own §7 puts the ceiling and the trim out of scope. The **record** budget is green. (b) **PHASE 2 MUST NOT ADD THE FIT ASSERTION NAIVELY — I HIT THIS AND BACKED OUT.** §4.3 wants `3 x budget + allowance <= 65,536` asserted and Phase 2's DONE says *asserted*. But a module-scope `assert` in `bin/check-handoff` runs at **import**, and `bin/tests.sh:2957` (M4) mutates the constant to 50,000 — `3 x 50,000 + 8,000 = 158,000`, so the mutated interpreter dies with an `AssertionError` before reaching the check. M4 greps for the *absence* of a catch; a traceback contains no catch; so **the mutant is scored killed by a crash rather than by the budget behaviour.** Any value large enough to survive M4 breaks the fit check by construction, so assertion and mutant cannot coexist unchanged: gate the check behind a flag, or resize M4's record and mutant together (14,000 B record vs 19,000 B mutant fits: `3 x 19,000 + 8,000 = 65,000`). **Decide it; do not discover it.** I left the fit rule as prose at `bin/check-handoff:602`, which meets Phase 1's stated Do (*"rewrite the derivation comment"*) and leaves nothing silently half-done. (c) Issue #75's PR still prepared, local-only (`60246e7`), **unsent**; four `FRAMEWORK_LEARNINGS.md` rows still owed against 2,410 B free. **Neither re-verified this session — inherited, not confirmed.** (d) A learning is earned and unwritten, same budget reason: *a grep for a constant does not find its derived neighbours*.
key_files: **Every line number re-derived against the working tree after my last write to that file.** `bin/check-handoff` (**canonical-only**) — `:636` the constant; `:577-634` the rewritten block, which now argues the number is **policy** and the formula only a fit check; `:602` the fit rule as prose (next_steps (b)); `:838` the rewritten remediation text, verified by triggering it. `bin/tests.sh` (**canonical-only**) — the thirteen couplings: `:2704`, `:2733`, `:2739` (`BUDGET38`), `:2820` (the recomputed `by 7,712`), `:2827/:2830/:2831`, **`:2833/:2835/:2836/:2837`** and **`:2946`** (the two the plan missed), `:2852`, `:2858`, `:2918/:2921`, `:2957` (M4's literal replace). `.context-budget.json` (**fork-only**) — the `HANDOFFS.md` `_` note. `docs/planning/record-budget-reduction-plan.md:3` status header and the **S106 correction under §5.2**.
gotchas: **A GREP FOR A CONSTANT DOES NOT FIND ITS DERIVED NEIGHBOURS, AND THE MISS IS GREEN.** `18,?432` matches neither `18433` nor `18432 + 512` nor an overage like `1,568`. Enumerate the **edge cases and the arithmetic**, not only the literal: a boundary test left at the old number keeps passing and quietly stops being one. **A MODULE-SCOPE `assert` IS A MUTATION-HARNESS HAZARD** — it runs at import, so a mutant that violates it dies before the code under test executes and is scored killed by the crash. **RUN THE FAILURE PATH:** the remediation text I rewrote is reachable only on a FAIL, so I built a throwaway git fixture and tripped it rather than trusting the format string. **`bin/check-*` ARE PYTHON; `dashboard_history.jsonl` GOES DIRTY FROM PHASE 0 ALONE — DO NOT `git reset --hard`** (inherited, held again).
runtime_smoke: **No application ships here; the build-equivalent is the suites plus the tools, RUN.** **CONTROL — a `git worktree` at the claim commit `3ecaf2e`, not the tree I edited:** `bin/tests.sh` **280 rows, 279 passed / 1 failed**, sole failure named — `github source dry-run failed`, Test 9's pre-existing `--source=github` 404, as in S102's and S104's. **AFTER: 280 rows, 279 / 1, same sole failure by name.** **ROW-FOR-ROW DIFF of the sorted rows, both populations asserted non-empty (280 / 280): ZERO lost, ZERO gained, exactly FOUR pairs differ** — the two edge rows (18,432/18,433 -> 12,288/12,289) and the two scope-control rows, whose *population count* moved **1 -> 3** because a lower budget puts more frozen receipts over it. That is a stronger control, not a weaker one — **but it is not what the plan predicted** (*"changes confined to rows whose names carry the budget number"*); those two names carry a derived count instead. **PYTHON SUITES 451/451 OK**, unchanged. **CHECKERS:** `check-handoff` OK — **`record budget: 0 unwritten record(s), 0 over 12,288 B`**, the new value live, and **this receipt is inside it**; `check-handoff --all` OK (5 receipts) — **no existing receipt reddened, the prospective-only property asserted rather than assumed**; `check-links` OK (88 links / 22 files); `check-learnings` OK (35 rows, 1..35). **FAILURE PATH EXERCISED:** a throwaway git fixture produced `record S2 is 13,215 B, over the 12,288 B per-record budget by 927`. **CARVE-OUT:** neither `bin/` file appears in `bin/_manifest.py`; `.context-budget.json` is fork-only. **FM #28 GATE, MEASURED LAST — figures in the close-out ledger entry**, including the one breach I am handing forward. **WHAT THIS DOES NOT EXERCISE:** whether 12,288 is livable beyond this one receipt, and handoff *quality* — no checker here asserts it; the only detector is the next session's 3A score, so treat one low score as signal, not noise.
changelog_ref: CHANGELOG.md "2026-08-25 · [ad hoc] S106 close-out — Phase 1 shipped, per-record budget 18,432 -> 12,288"
commit: 3ecaf2e (1B claim) + 6ebe84d (the deliverable) + this close-out
```

<!-- claim stub written at session start; completed at close-out -->
Model: Claude Opus 5 (1M context).

**Predecessor S105 scored 7/10.** **+** **Its reframing is why this session was small.** It answered the
operator's actual question first — *is the ledger resident?* — found that it is not, and concluded that
the term worth attacking is the receipt, not the file. I re-derived that rather than inheriting it. **+** **The prospective-only finding was correct and
load-bearing:** `check_record_budget` compares the newest record against its frozen copy at HEAD, so
lowering the budget reddens nothing — confirmed by reading the code and by `--all` staying green over
all five receipts. Without it this was a migration. **+** Both risks it flagged were the right two, and its
gotcha *"the formula is a ceiling-fitting device, not a target"* is what the rewritten comment is built
around. *"Do not rewrite historical prose"* held. **−** **The
MANDATORY inventory was incomplete by two sites and one fails silently green.** The plan's own §5 says
*"a plan that lists files to change without having searched for them is an assumption, not an
inventory"* — this one searched, with a pattern that could not match its target's derived neighbour.
Trusting it here would have left a boundary test passing while testing nothing. **−** **Phase 1's
verification list requires `context_budget.py` exit 0, which Phase 1 structurally cannot deliver** —
the breach is the whole-file ceiling, which its own §7 declares out of scope, so the executor must
report a false green or find the contradiction mid-session. Not an 8: two contract defects, the silent
one being the exact class this repo keeps recording. Not a 6: every substantive judgment — number,
evidence, scope, risks — survived independent re-execution.

**Self-assessment: 8/10.** **+** **I ran the inventory greps myself rather than trusting a table
labelled mandatory, which is the whole reason the edge test still tests an edge.**
**+** **I backed out a change I wanted to make** — the executable fit assertion — once I traced that it
would kill M4 by crashing the interpreter at import rather than by the budget behaviour, and I handed
the analysis and two concrete fixes forward instead of leaving Phase 2 to discover it. **+** The control was
uncontaminated **by construction** (a worktree at the claim SHA), not by my care; I recomputed the
derived overage rather than search-replacing it, and **ran the failure path** on a fixture instead of
trusting a format string. **+** I refused to blunt the zero-hit criterion by exempting two sentences,
rewriting them to "18 KiB" so the tripwire stays live. **+** This receipt is
written under the new 12,288 B budget — the guard applied to its own author.
**−** **I declared no falsifiable predictions at claim time.** My predecessor's single best practice
was recording four derived predictions in its claim commit; I read that receipt, scored it, and did
not carry the practice forward. Everything I verified, I verified *after* the fact. **−** **I leave `HANDOFFS.md`
over its whole-file ceiling and larger than I found it** — structurally forced (FM #26) and handed
forward with its arithmetic, but the debt is now mine as much as inherited. **−** I did not re-verify
the issue-#75 and owed-learnings state; labelling it inherited is honest but is not the same as
checked. Not a 9 because the prediction miss was avoidable and I had just finished praising that very
practice in someone else's work; not a 7 because the deliverable is complete, every in-scope DONE
criterion is met, the one that is not is named with its reason, and two defects in the contract I was
handed were caught rather than propagated.

```handoff
session: S105
date: 2026-08-25
status: complete
self_score: 8
predecessor_score: 8
active_task: **Plan the per-record budget reduction. COMPLETE — the PLAN is the deliverable and nothing was implemented** (FM #18/#19). Deliverable: [`docs/planning/record-budget-reduction-plan.md`](docs/planning/record-budget-reduction-plan.md), DRAFT awaiting operator ratification. **Zero changes to `bin/check-handoff`, `bin/tests.sh`, `.context-budget.json` or the front matter.** **NO OUTWARD-FACING ACTION.**
what_was_done: Two commits — `2cdda38` (1B claim), this close-out carrying the plan. **(1) THE OPERATOR'S ACTUAL QUESTION WAS ANSWERED FIRST, BECAUSE IT DECIDES WHETHER THE REST MATTERS:** is the ledger resident? **No** — no `@`-import, and the repo's own measurement across 81 transcripts (`bin/check-handoff:590-597`) is read-whole **once**, read-in-part **593** times, median span 25 lines. So the per-session cost is **front matter + ONE receipt ≈ 25 KB**, not the file's 57,892 B. **The receipt is the term worth attacking; trimming the file never touches it.** (2) **THE CUT IS CHEAPER THAN IT LOOKS, AND THAT IS A MEASUREMENT:** trailing prose is **27–30%** of every recent receipt (S104 5,388 B, S103 4,613 B, S102 4,653 B) and is *additive* to the six mandatory requirements, whose conclusions the receipt already carries as `predecessor_score`/`self_score`. Fenced-field mean is **12,108 B**, so **12,288 B leaves all six intact** and the cut lands on essays. (3) **RECOMMENDED 18,432 → 12,288**: steady state 63,296 → **44,864 B** (96.6% → 68.5% of ceiling), slack 2,240 → **20,672 B**, per-session cost ~25 KB → **~19 KB**. 10,240 and 8,192 costed and recorded; 8,192 rejected *as step 1* because current fenced fields are 10,920–13,019 B and it would cut the requirements themselves (FM #15). (4) **THE DE-RISKING FINDING:** `check_record_budget` (`bin/check-handoff:652+`) checks only the newest record and only when it differs from its frozen copy at HEAD — the budget is **prospective-only**, so **no existing receipt reddens and none needs rewriting.** (5) Grep inventory of all 17 sites, each line number verified by re-reading it.
next_steps: (a) **RATIFY THE NUMBER BEFORE PHASE 1 — that is the one blocking decision** (plan §9). Every site in §5.2 encodes it. Recommendation 12,288; alternatives costed in §4.2. (b) **PHASE 1 IS ONE SESSION** and its riskiest site is `bin/tests.sh:2956`, which does a **literal string replace** of `"RECORD_BUDGET_BYTES = 18432"`; `:2819` asserts derived arithmetic (`by 1,568`) that must be **recomputed, not search-replaced**. Run the pre-change suite in a `git worktree`, diff sorted rows, expect zero lost. **Deepest reasoning mode** for Phase 1 (plan §8). (c) **PHASE 2 MUST NOT LET THE FORMULA UNDO PHASE 1** (§4.3): shrinking the front matter lowers the header allowance, which under the old reading *raises* the derived budget. State the budget as **policy**, use the formula only as the assertion `3 × budget + allowance ≤ 65,536`. (d) `HANDOFFS.md` is **57,892 B → now larger with this receipt**; measured last, in `runtime_smoke`. The trim will be due again soon — `--cut 3` remains the floor. (e) Issue #75 PR still prepared, unsent, local (`60246e7`); four owed `FRAMEWORK_LEARNINGS.md` rows still owed (2,410 B free). Both unchanged, **not re-verified this session.**
key_files: **Every line number verified by re-reading the cited line, and the `CHANGELOG.md` ones re-derived AFTER this session's own write.** [`docs/planning/record-budget-reduction-plan.md`](docs/planning/record-budget-reduction-plan.md) — the deliverable. `bin/check-handoff:606` the constant; `:578-604` the derivation comment; `:584` the 8,000 B allowance; `:588` the arithmetic; `:810` the user-facing remediation text; `:590-597` the 81-transcript measurement; `:652+` `check_record_budget`, the prospective-only scope. `bin/tests.sh:2738, 2819, 2826, 2829-2830, 2851, 2857, 2917, 2920, 2956` — the nine test couplings; `:2704, 2732` comments. `.context-budget.json:59` the `_` note. `CHANGELOG.md:598` the guard-applied-to-its-own-author precedent.
gotchas: **A LINE NUMBER MEASURED BEFORE YOUR OWN WRITE IS STALE, AND IT FAILS SILENTLY.** I greppped `CHANGELOG.md` for the budget's sites, then prepended my claim entry, then wrote those numbers into the plan — every one was off by **5**. Nothing complained; the plan simply cited the wrong lines. **Re-derive after your last write to the file**, or cite against a named SHA. **TWO HEADER TERMS ARE IN CIRCULATION AND MIXING THEM CORRUPTS THE ARITHMETIC:** the derivation's **8,000 B allowance** gives 63,296 B (slack 2,240 — the comment's own figure), while S103's widely-quoted `6,016 + 3 × 18,432 = 61,312 B` uses the header **as measured then**; today it measures 6,913 B. My first draft wrote `3 × 18,432 + 8,000 = 61,312`, which is neither. **State which header term you are using.** **THE FORMULA IS A CEILING-FITTING DEVICE, NOT A TARGET** — it was built to make the budget as LARGE as would fit, so re-deriving it after any reduction hands the saving straight back. **DO NOT REWRITE HISTORICAL PROSE:** twelve `CHANGELOG.md` sites and every archived shard state 18,432 as a fact about their own moment and are correct as written (FM #22).
runtime_smoke: **PLANNING SESSION — NO RUNTIME BEHAVIOUR CHANGED AND NO CODE WAS TOUCHED; the build-equivalent here is the checkers plus citation verification.** `git status` shows the diff confined to `HANDOFFS.md`, `CHANGELOG.md`, the new plan, and the two tracked telemetry ledgers — **zero files under `bin/`, `tools/` or `starter-kit/`.** **CITATIONS:** all **14** `bin/` line citations verified by re-reading each cited line against a regex of what I claimed it says — 14/14 OK; the `CHANGELOG.md`/`HANDOFFS.md` sites re-derived after my own write (see gotchas). **ARITHMETIC:** every figure in §4.1/§4.2 recomputed from `C=65536, H=8000, F=3` rather than carried — 63,296/96.6%/2,240 and 44,864/68.5%/20,672 confirmed. **CHECKERS:** `check-links` OK (88 links / 22 files), `check-handoff` OK, `check-handoff --all` OK. **`bin/tests.sh` NOT RUN — stated, not skipped silently:** no file it exercises was modified, so it could only reproduce S104's 279/1. **Phase 1 must run it**, with a worktree control. **FM #28 GATE, MEASURED LAST:** figures in the close-out ledger entry. **WHAT THIS DOES NOT EXERCISE:** the budget change itself — nothing here proves 12,288 is livable beyond this receipt being written under it.
changelog_ref: CHANGELOG.md "2026-08-25 · [ad hoc] S105 claim — plan the per-record budget reduction" and "2026-08-25 · [ad hoc] S105 close-out"
commit: 2cdda38 (1B claim) + this close-out
```

<!-- claim stub written at session start; completed at close-out -->
Model: Claude Opus 5 (1M context).

**Predecessor S104 scored 8/10 — and the score is worth less than usual, because I wrote it.** The
bidirectional accountability that makes this step work is absent when author and evaluator are the
same session; recording that is more honest than performing the evaluation as though it held. **+**
**Its `next_steps` (a) is this plan's §1, pre-derived** — the floor, the budget, the arithmetic, and
the conclusion that *"the durable remedy is a decision about the ceiling or the per-record budget, not
another trim."* The planning session had a premise instead of a research problem. **+** Its
`key_files` named `bin/tests.sh:2110` and `:2721` and pointed at `bin/check-handoff`, which is where
the whole inventory started. **+** Its telemetry-dirty and `check-*`-are-Python warnings held again.
**−** **It left a number ambiguous and that ambiguity produced a real error in my first draft.** It
quoted `61,312 B` without flagging that the figure uses the header **as measured** (6,016) while the
derivation uses the **8,000 B allowance** (63,296). I wrote `3 × 18,432 + 8,000 = 61,312`, which is
neither, and only caught it by recomputing. **−** **It gave line numbers with no warning that they go
stale the moment the next session writes to those files** — I cited twelve `CHANGELOG.md` lines that
my own claim entry had already shifted by 5. Both gaps are mine.

**Self-assessment: 8/10.** **+** **I answered the operator's real question first — is this file
resident? — because it decides whether the rest matters.** It is not; the cost is one receipt, ~25 KB,
not the file's 57,892 B. That reframed the deliverable from *shrink the file* to *shrink the record*,
which is the only lever that touches recurring cost. **+** **Two findings made the plan small and safe
rather than sweeping.** The budget is **prospective-only** (`check_record_budget` compares against the
frozen copy at HEAD), so no existing receipt reddens and none needs rewriting — without that the plan
would have proposed a migration. And trailing prose is **27–30%** of a receipt while fenced fields mean
**12,108 B**, which is what makes 12,288 safe for all six mandatory requirements and 8,192 unsafe. Both
were measured, not assumed. **+** I ran a real grep inventory and **verified all 14 `bin/` citations by
re-reading each cited line**, not by trusting the grep that produced them. **+** I wrote this receipt
under the **proposed** 12,288 B budget rather than the current 18,432, so the recommendation carries at
least one worked example. **−** **The stale line numbers were entirely avoidable.** I hold the lesson —
measure against the pre-change tree, or re-derive after your last write — and still cited numbers taken
before my own claim commit. Caught at Phase 3F only because the protocol makes citation-checking
mandatory; without that step the plan would have shipped wrong. **−** **I propagated an inherited figure
without asking which state it was derived for**, one session after recording a memory about exactly that
failure. **−** `bin/tests.sh` was not run. Justified — no file it exercises was modified — but it is a
gap stated rather than a box ticked, and Phase 1 must not inherit the assumption.


