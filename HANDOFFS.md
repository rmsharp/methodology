# Handoff Receipts — durable close-out proof

This repository dogfoods its own methodology: every session records a durable, machine-checkable
`handoff` receipt here at close-out (Phase 3D), and Phase 0 reconciles it against `git log`. See
[`starter-kit/HANDOFFS.md`](starter-kit/HANDOFFS.md) for the block format and the write points, and
`bin/check-handoff` for the checker. Newest on top; prepend-only.

**Older receipts are archived.** This file currently holds **3** (recounted at S95's close-out,
2026-08-17 — recount with `grep -c '^```handoff' HANDOFFS.md` rather than trusting this number: it
read **3** from the S94 trim until this line was corrected, one close-out later, which is exactly the
span the note below predicts); the oldest **19**
(2026-07-08 → 2026-07-30) live in [`docs/archive/HANDOFFS-archive.md`](docs/archive/HANDOFFS-archive.md),
same format, same newest-on-top order. Archiving is safe by construction: `bin/check-handoff`
validates only the newest receipt, and Phase 0 reconcile is frontier-based, so neither reads past the
top of this file. `bin/model-report --handoffs <archive>` reaches the older prose when you need it.
Archive again — a new file, same format — when this one approaches ~1,200 lines, the trigger the
action ledger already uses.

**Two session sequences share this ledger and their numbers collide.** This fork and
`upstream/main` each run their own `S<N>` counter, so a receipt is identified by **session + date**,
never by number alone: upstream's **S7**/**S8** (both 2026-08-01) are different sessions from the
fork's **S7** (2026-07-09) / **S8** (2026-07-13) in the archive. At a resync the two sequences stay
separate and unrenumbered, each incoming receipt is checked against ours before it is kept, and
within a shared date the fork's receipts precede the arriving upstream ones (precedent: `fc4d297`).

> **The count above drifts between trims.** `methodology_trim.py` declares it a regenerated field
> (`starter-kit/methodology_trim.py`, the `HANDOFFS.md` `LedgerSpec`), so a **trim** rewrites it and
> the proof's L2 clause excuses that one span — but nothing updates it when a session **prepends** a
> receipt, which is most sessions. So it is right immediately after a trim and wrong from the next
> close-out onward: it read **6** from `7a71df0` until corrected three sessions later. That is
> [Learning #12](starter-kit/FRAMEWORK_LEARNINGS.md) pointed at this file, and it is the receipt-ledger
> half of upstream [issue #65](https://github.com/KJ5HST/methodology/issues/65). Recount before
> trusting it.

> **⚠ A trim of this file should retain at least THREE receipts — the tool's default cut does not
> know that.** `bin/tests.sh` Test 34 mutates *this* ledger to check `check-handoff --all`'s
> whole-ledger invariants, reading two mutation anchors from the live file: not hardcoded, so it
> survives *which* receipts rotate, but it needs three to exist. S94's first attempt took the
> budget-driven default, retained **2**, and the suite went 235/1 → **229/6**. Pass `--cut 3` (or
> more) explicitly, and re-run `bash bin/tests.sh` after any trim of this file.
>
> **Since S96 (2026-08-17) a short ledger is STATED rather than silent — which is not the same as
> fixed** (BL-40 (b)). The anchors are an asserted population: below the floor those six assertions
> print as `SKIP` rows naming themselves and the reason, the summary line carries a skip count, and
> a ledger with *zero* receipts still FAILS, because corruption is not rotation. A cut to two no
> longer reads as a checker regression, and it still leaves six invariants unexercised. **Nothing
> prevents that cut** — judging it worth the coverage is the reader's call, which is why the count
> is on the summary line.
**Archived 16 record(s), 2026-07-30 → 2026-08-02** into [`docs/archive/HANDOFFS-through-2026-08-02.md`](docs/archive/HANDOFFS-through-2026-08-02.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/HANDOFFS-through-2026-08-02.md.verify.sh`](docs/archive/HANDOFFS-through-2026-08-02.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.1.1.

**Archived 30 record(s), 2026-08-03 → 2026-08-09** into [`docs/archive/HANDOFFS-through-2026-08-09.md`](docs/archive/HANDOFFS-through-2026-08-09.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/HANDOFFS-through-2026-08-09.md.verify.sh`](docs/archive/HANDOFFS-through-2026-08-09.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.1.1.

**Archived 25 record(s), 2026-08-02 → 2026-08-11** into [`docs/archive/HANDOFFS-through-2026-08-11.md`](docs/archive/HANDOFFS-through-2026-08-11.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/HANDOFFS-through-2026-08-11.md.verify.sh`](docs/archive/HANDOFFS-through-2026-08-11.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.1.3.

**Archived 8 record(s), 2026-08-11 → 2026-08-15** into [`docs/archive/HANDOFFS-through-2026-08-15.md`](docs/archive/HANDOFFS-through-2026-08-15.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/HANDOFFS-through-2026-08-15.md.verify.sh`](docs/archive/HANDOFFS-through-2026-08-15.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.2.0.

**Archived 4 record(s), 2026-08-15 → 2026-08-17** into [`docs/archive/HANDOFFS-through-2026-08-17.md`](docs/archive/HANDOFFS-through-2026-08-17.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/HANDOFFS-through-2026-08-17.md.verify.sh`](docs/archive/HANDOFFS-through-2026-08-17.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.2.0.

**Archived 3 record(s), 2026-08-17 → 2026-08-18** into [`docs/archive/HANDOFFS-through-2026-08-18.md`](docs/archive/HANDOFFS-through-2026-08-18.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/HANDOFFS-through-2026-08-18.md.verify.sh`](docs/archive/HANDOFFS-through-2026-08-18.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.3.0.

**Archived 3 record(s), 2026-08-18 → 2026-08-23** into [`docs/archive/HANDOFFS-through-2026-08-23.md`](docs/archive/HANDOFFS-through-2026-08-23.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/HANDOFFS-through-2026-08-23.md.verify.sh`](docs/archive/HANDOFFS-through-2026-08-23.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.3.0.

```handoff
session: S106
date: 2026-08-25
status: pending
active_task: **Phase 1 of [`docs/planning/record-budget-reduction-plan.md`](docs/planning/record-budget-reduction-plan.md) — lower `RECORD_BUDGET_BYTES` 18,432 -> 12,288.** The number was RATIFIED by the operator at Phase 1 (plan §9's one blocking decision), choosing the plan's recommendation over the costed 10,240 / 8,192. Sites: `bin/check-handoff` (the constant, its derivation comment, the user-facing remediation text), the nine `bin/tests.sh` couplings in plan §5.2, and the `_` note at `.context-budget.json:59`. **NOT claimed:** Phase 2 (front-matter compaction), Phase 3 (further reduction), the 65,536 B ceiling, Test 34's floor of 3, `methodology_trim.py`, any distributed file, and the `HANDOFFS.md` trim that is due (it is a second capability — FM #26). **NO OUTWARD-FACING ACTION.**
next_steps: DONE = `bin/check-handoff` reports the new budget, `bin/tests.sh` green with ZERO rows lost against a pre-change control run in a `git worktree` at this claim commit, `git grep -nE '18,?432' -- bin/` returns zero hits, `context_budget.py` exits 0, and this session's own receipt is written under the NEW 12,288 B budget — the guard applied to its own author (precedent: `CHANGELOG.md` "This receipt measures 17,162 B against the 18,432 B..."). Highest-risk site is `bin/tests.sh:2956`, a literal string replace of `"RECORD_BUDGET_BYTES = 18432"`; `:2819` asserts DERIVED arithmetic (`by 1,568`) that must be recomputed, never search-replaced. Historical prose in `CHANGELOG.md`, `HANDOFFS.md` and every `docs/archive/` shard states 18,432 as a fact about its own moment and is correct as written — DO NOT REWRITE IT (FM #22, plan §5.4).
```

<!-- claim stub written at session start; completed at close-out -->


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


```handoff
session: S104
date: 2026-08-24
status: complete
self_score: 8
predecessor_score: 9
active_task: **Run the `HANDOFFS.md` trim, losslessly. COMPLETE.** The file arrived **92,387 B against a 65,536 B ceiling, OVER by 26,851** — the only file over one — and 96,264 B after my claim stub. It stood at **43,362 B at the trim commit `470cfd4`, 22,174 B clear**; **this receipt brings the file to 57,892 B, 7,644 B clear** — figures stated at named points, because this receipt and the ledger entry each move a file the other reports. `--check` reports **`trigger does not fire`** at that final size — run it rather than trusting this sentence. **NOT DONE, DELIBERATELY:** no second trim (`CHANGELOG.md` does not fire), and **NO OUTWARD-FACING ACTION** — no push, no PR, no comment, no tag, no issue edit; the issue #75 branch is untouched and still local.
what_was_done: Three commits — `ab12b27` (1B claim), `470cfd4` (THE DELIVERABLE, the trim alone), this close-out. **(1) THE CUT WAS CHOSEN AGAINST TWO COSTED ALTERNATIVES, ALL THREE DRY-RUN MEASURED WITH THE CLAIM STUB IN PLACE.** The budget default retains **1** (→ 10,790 B) and straddles the day; **`--cut 4`** retains 4 (→ 61,101 B, **4,435 B** clear — less than one receipt, which run 15,533–18,431 B here) and also straddles; **`--cut 3`** retains 3 (→ **43,362 B, 22,174 B clear**) and raised **neither** `[CUT_STRADDLES_DAY]` **nor** `[SHARD_NAME_DISAMBIGUATED]`. **(2) THE FLOOR WAS GROUNDED IN THE CODE, NOT IN MY PREDECESSOR'S PROSE — AND THAT FOUND A SECOND CONSUMER NOBODY HAD NAMED FOR THIS DECISION.** S103 named Test 34. Reading it (`bin/tests.sh:2110`, `anchor_disposition`) confirmed a population below 3 routes to the `SHORT` arm and prints six assertions as SKIP. Reading further found **Test 38**, whose fixture builder aborts `FIXTURE SOURCE TOO SHORT: need >= 2 records` at `len(starts) < 3` (**`bin/tests.sh:2721`** — my claim commit cited `:2719`, eyeballed from a `sed` window rather than grepped; corrected here). The default would have broken **two** consumers, not one. **(3) THE SEAM IS PROVED, NOT INFERRED FROM THE ADVISORIES' SILENCE.** Retained receipts carry only **2026-08-24**; archived carry **2026-08-18** and **2026-08-23**; the intersection is **empty**. **(4) LOSSLESSNESS WAS ESTABLISHED THREE WAYS INDEPENDENT OF THE TOOL'S OWN L1/L2/L3.** Per-record: all **6** pre-trim records accounted for, each **byte-identical** by sha256 across the move, partition **disjoint**, none lost, none invented. Front matter: a `difflib` diff shows **exactly one hunk, a pure 4-line addition** — zero deletions, zero modifications. And a **full reconstruction** — the live records zone concatenated with the shard's is **byte-identical (89,799 B)** to the pre-trim records zone, so the trim is reversible from the two artifacts alone, without git.
next_steps: (a) **NO LEDGER IS OVER A CEILING — BUT EXPECT TO TRIM AGAIN NEXT SESSION, AND THE REAL FINDING IS THAT THIS IS STRUCTURAL.** `context_budget.py` exits **0**: `HANDOFFS.md` **57,892 / 65,536** and `CHANGELOG.md` 45,284 / 65,536. The 7,644 B left is **less than one receipt** — mine cost 17,356 B, S102's 17,039, S103's 15,533 — so a successor's stub plus receipt breaches the ceiling, and `--check` should fire at their close-out. **That is not a bad cut; no cut could have done better.** `--cut 3` was already the most aggressive cut that preserves Test 34's floor, and the floor is what sets capacity: 3 records at the 18,432 B per-record budget plus ~6 KB of front matter is **61,312 B against a 65,536 B ceiling** — S103's arithmetic, and this file now sits at **94.4%** of it. **The ledger's steady state is therefore ~3 receipts and a trim nearly every session, by construction.** Trimming harder is unavailable (the floor); so the durable options are a decision about the **ceiling** or the **per-record budget**, not another trim. Worth an operator decision; I raised neither (a second capability). When the next trim comes, `--cut 3` is again the floor, and the shard name derives from the newest ARCHIVED record's date, not from today. (b) **`starter-kit/FRAMEWORK_LEARNINGS.md` IS NOW THE MOST IMMINENT CEILING AND THE OWED-LEARNING QUEUE IS AT FOUR.** 63,126 / 65,536 — **2,410 B**, unchanged this session; rows #35 and #36 cost 1,219 B and 1,436 B, so **one ordinary row does not reliably fit and two certainly do not**. S99's, S102's, S103's and now mine are owed. **This is the fourth consecutive session to defer for the same reason, which by this repo's own Degradation-Detection table is the tell that the signal is not missing — nothing gates on it.** The remedy is a decision (archive/split that file, or raise its ceiling) on a **DISTRIBUTED** file, so it needs a go-ahead and is a session of its own. (c) **THE ISSUE #75 PR IS STILL PREPARED AND STILL UNSENT.** Branch `docs/issue75-plan-surface-upstream` = `60246e7`, **local only — re-verified this session** with `git ls-remote --heads origin`, which returns nothing for it. Send commands are in [`docs/planning/issue75-upstream-pr.md`](docs/planning/issue75-upstream-pr.md); push to **`origin`**, never `upstream`. Upstream #75 remains the only open upstream issue, no maintainer reply since 2026-08-16. (d) **A FINDING RAISED AND DELIBERATELY NOT FIXED (FM #8/#17):** the new shard carries **1 relative link that no longer resolves** — `docs/archive/HANDOFFS-through-2026-08-18.md`, root-relative inside S101's `active_task`. This is **inherent to the design, not a regression**: records move **byte-identically** (that IS L3), so intra-record links are never rewritten; only the header the tool authors gets the `../../` prefix. Six earlier shards carry the same condition (2, 3, 1, 1, 1 unresolved). `bin/check-links` never sees any of it — it walks the **DISTRIBUTED** set and these are canonical-only. Candidate BL item, not raised (a second capability). (e) `upstream/main` is **1 behind** (`512c2ed`); the fork is **383 ahead** at this close-out's parent. `git merge-tree --write-tree --name-only HEAD upstream/main` was **not** re-derived after this receipt — re-derive it; the two ledgers are the historical conflict set and I wrote to both. (f) BL-37 (b), BL-39 and the long tail unchanged, **NOT re-verified**. **BL-16 has no heading by design.**
key_files: **Every path, figure and line number re-derived against the committed tree at close-out.** [`HANDOFFS.md`](HANDOFFS.md) — 43,362 B at the trim commit `470cfd4`, **57,892 B with this receipt**, 3 receipts; the new pointer block at `:73`; the regenerated count sentence at `:8`, which now reads **3** and is **correct** (it read 3 before the trim while the file held 5 — the documented drift; the trim's `regenerated` field made it true rather than changing it, which is why no `[FRONTMATTER_FIELD_REGENERATED]` fired). [`docs/archive/HANDOFFS-through-2026-08-23.md`](docs/archive/HANDOFFS-through-2026-08-23.md) — the frozen shard, 53,905 B, **3 records (S101, S100, S99)**. [`docs/archive/HANDOFFS-through-2026-08-23.md.verify.sh`](docs/archive/HANDOFFS-through-2026-08-23.md.verify.sh) — the proof; **run it, do not trust a digest**. [`CHANGELOG.md`](CHANGELOG.md) — 45,284 B; the tool's trim entry at `:170`, my claim entry at `:178`. `bin/tests.sh:2110` `anchor_disposition` — Test 34's floor; `:2721` Test 38's `len(starts) < 3` abort; `:2299` the `LIVE_N` grep-vs-python population control whose row text moved `(5)` → `(3)`. `starter-kit/methodology_trim.py` — v1.3.0; `SRF_RED = 1.00` at `:97` (this run measured **0.9148**, so no refusal and no `--force`).
gotchas: **THE SHARP EDGE OF THIS FILE, AND I HIT IT: `text.index("```handoff")` IS NOT A RECORD ANCHOR.** The front matter contains the literal string ```` ```handoff ```` inside a sentence at `:9` — `` recount with `grep -c '^```handoff' HANDOFFS.md` `` — so the first **substring** match is 64 lines above the first **record**. My first claim splice landed mid-sentence, flipped fence parity, and `methodology_trim.py` then reported **4 records in a 6-receipt file**: two real receipts were swallowed as `inside=True` by `fence_scan`, which skips fences nested in an open fence. Use `(?m)^```handoff$` and **assert the count changes by exactly what you intend**. Reverted byte-identical to HEAD and redone; nothing broken reached a commit. **META-LESSON: WHEN A TOOL AND YOUR FRESH EDIT DISAGREE ABOUT A FILE YOU JUST EDITED, THE EDIT IS THE SUSPECT.** My first framing was that the tool had a discrepancy. It did not. **THE WARNING THAT WOULD HAVE PREVENTED THIS WAS IN THE LEDGER AND NOT WHERE I LOOKED** — *"anchor on LINE-ANCHORED fences and assert the COUNT"* appears exactly once, inside S103's **praise of S102**, never in S103's own `gotchas` field. Phase 3A points a successor at the receipt's fields. **Put the warning that saved you in `gotchas`, not only in the paragraph thanking your predecessor.** **AN ADVISORY THAT STAYS SILENT IS NOT EVIDENCE** — `[CUT_STRADDLES_DAY]`'s absence is cheap to corroborate: `grep '^date:'` both artifacts and intersect them. **A LOSSLESSNESS PROOF THAT ONLY RUNS THE TOOL'S OWN CHECK IS THE TOOL GRADING ITSELF** — reconstruct the pre-trim records zone from live + shard and compare bytes; it is four lines of Python and it is the assertion that actually means "nothing was lost". **RUN THE CONTROL IN A `git worktree`, NOT IN THE TREE YOU ARE EDITING** (S103's, and it held). **`bin/check-*` ARE PYTHON, and BOTH `dashboard_history.jsonl` AND `.context-budget-history.jsonl` go dirty from Phase 0 alone — DO NOT `git reset --hard`.**
runtime_smoke: **THIS REPO SHIPS NO APPLICATION; THE BUILD-EQUIVALENT IS THE SUITES PLUS THE TOOLS, RUN — AND THE PRE-CHANGE HALF RAN IN A PRISTINE `git worktree` AT `b570389` SO IT COULD NOT BE CONTAMINATED BY THE WRITES IT WAS CONTROLLING FOR.** **SUITE, ROW-FOR-ROW.** Control **279 passed / 1 failed / 0 skipped**; post-change on the committed tree **279 / 1 / 0**. Both populations asserted non-empty (**280 rows each**). Sorted row-set diff: **ZERO rows lost, ZERO net added, EXACTLY THREE rows changed**, every one carrying a count in its own name — `live ledger receipt-id population is non-empty (5)→(3)`, `handoff_anchors agrees with an independent grep (5)→(3)`, and Test 31's `Source 1's entry count (17) matches the raw anchored **Model:** grep (17)` → **`(18)` matches `(18)`**. **The `0 skipped` on both sides is the direct evidence Test 34 stayed in its `ANCHORED` arm** — the default cut would have shown 6 skips. Test 31's two operands **moved together**, which is the proof it is a same-file self-consistency check: the trim contributed **0** (Source 2's rows are `S<N>`-prefixed, not date-prefixed, so `TOOL_COUNT`'s `^2026-` grep cannot see a receipt) and my claim entry contributed **+1 to both sides**. Sole failure **BOTH** times, confirmed **BY NAME** not by count: `github source dry-run failed` (Test 9's pre-existing `--source=github` 404). **PROOFS.** All shipped `.verify.sh` re-run: **pre-trim 9 green / 4 red of 13**, **post-trim 10 green / 4 red of 14** — the same four reds (`*-2026-08-02` and `*-2026-08-09` on both ledgers), **zero reddened**, one new green. The new proof is green in **both** forms: pre-commit (`source: HEAD vs the working tree`) and post-commit (`source: the trim commit 470cfd4`), reporting *"6 before = 3 retained + 3 archived; added by the trim commit: 0"*. **TRIM INTERNALS:** `L1_OK`, `L2_OK`, `L3_OK` (6 partitioned), `P1A_OK` (ledger 21 → 22). **INDEPENDENT OF THE TOOL:** per-record sha256 byte-identity across the move, disjoint 3+3=6 partition, single-hunk pure-addition front-matter diff, and full records-zone reconstruction byte-identical at 89,799 B. **RETRIEVAL, NOT JUST STRUCTURE:** `bin/model-report --handoffs docs/archive/HANDOFFS-through-2026-08-23.md` reaches S101/S100/S99's prose, so the archive is usable and not merely present. **PYTHON:** **451/451** (`OK (skipped=4)`), matching S103. **CHECKERS:** `check-links` **88 links / 22 files** and `check-learnings` **35 rows, contiguous 1..35** — both **byte-identical pre and post**, as predicted at claim; `check-handoff --all` OK on the live ledger (3 receipts) and on the shard under `--archived` (3 receipts). **FM #28 GATE:** `context_budget.py` exits **0** — `HANDOFFS.md` ok, `CHANGELOG.md` ok, `CLAUDE.md` 11,064 ok, `BACKLOG.md` ok, `FRAMEWORK_LEARNINGS.md` 63,126 / 65,536 ok but **2,410 B from its ceiling**. Dashboard **72/100**, medium risk, 0 high+ risk. **WHAT NONE OF THIS EXERCISES:** GitHub delivery, review, or merge. No network path was tested, because none can be without sending something.
changelog_ref: CHANGELOG.md "2026-08-24 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-08-23.md` (3 record(s), 96,264 B → 43,362 B)", plus "[ad hoc] S104 claim — run the `HANDOFFS.md` trim, losslessly" and "[ad hoc] S104 close-out"
commit: ab12b27 (1B claim) + 470cfd4 (the trim) + this close-out
```

<!-- claim stub written at session start; completed at close-out -->
Model: Claude Opus 5 (1M context).

**Predecessor S103 scored 8/10.** **+** **Its `next_steps` (a) named the deliverable, its exact
overage, and the one constraint that actually binds this ledger — Test 34's retention floor of three
receipts, `--cut 3` or more, never the budget default.** I verified that in the code rather than
inheriting it, and it was right; it is the reason the default was never a candidate. **+** **It gave
the failure's shape, not just its name** — S94's default cut took the suite 235/1 → 229/6, so I knew
what a wrong cut looks like before I could cause one. **+** **Its
gotchas were load-bearing and changed what I did.** *Run the control in a `git worktree`, not in the
tree you are editing* — I did, and it is why my 280-row baseline is trustworthy rather than merely
careful. *`[CUT_STRADDLES_DAY]`'s absence is evidence only if you also check the dates on both sides* — I
checked, and reported the intersection rather than the silence. *`bin/check-*` are Python and the
telemetry ledgers go dirty from Phase 0 alone* — both true, and both would have cost me a
`git reset --hard`. **+** Its branch re-verification (`60246e7`, local only) reproduced
exactly. **+** **A criticism I drafted and then withdrew, because I checked it.** I had written that its
*"at the 18,432 B budget a 3-receipt ledger measures 6,016 + 3 × 18,432 = 61,312 B"* overstated the
result by ~18 KB, since the trim landed at 43,362 B. That was **my** error: 43,362 B was a transient
mid-trim state in which one of the three records was a 3,877 B *pending stub*, not a completed
receipt. With this receipt finished the file is **57,892 B — 94.4% of that bound**, and the bound is
explicitly labelled *"at the … budget"*. It is a sound steady-state capacity figure and the most
useful number in the handoff: it is what shows the ledger's steady state is ~3 receipts and a trim
nearly every session. **Comparing a steady-state bound against a mid-operation measurement is a
timing error, and I nearly shipped it as a defect in someone else's work.** **−** *"No name collision …
so a cut today derives a free name"* — the name derives from the **cut key**, the newest ARCHIVED
record's date, not from today. True for the cut I took; false for a plausible one, as I saw live
when an intermediate run produced `[SHARD_NAME_DISAMBIGUATED] → HANDOFFS-through-2026-08-18-2.md`.
**−** *"fork 380 ahead"* — it was **381**, and that was computable.
**−** **Structural, and it cost me the one defect of this session: the warning that would have
prevented it is in S103's *praise of S102*, not in its own `gotchas` field.** *"Anchor on
LINE-ANCHORED fences and assert the COUNT"* appears exactly once in the whole ledger, in that
paragraph. Phase 3A points a successor at the receipt's fields; I read them, acted, and made
precisely that mistake. Not a 10, because the name-derivation claim was imprecise reasoning that happened to land
right, and the most useful warning in the whole ledger was filed where Phase 3A does not point a
successor. Not an 8, because every claim that gated the deliverable was accurate and reproduced,
and the one figure I set out to fault turned out to be the sharpest number it gave me.

**Self-assessment: 8/10.** **+** **I recorded six declarations at claim time, derived rather than
guessed, and every one held exactly** — the clean seam with neither advisory firing, the free shard
name, Test 31 staying green with both operands moving together, Test 34's rows changing text `(5)`
→ `(3)` while keeping their verdict, `check-links` at 88/22 and `check-learnings` at 35 unchanged,
and zero rows lost. Writing them into the claim commit is what made them falsifiable instead of
retrospective. **+** **I priced the alternatives rather than asserting the
choice** — `--cut 4` was rejected on a number, not on taste. **+** **I grounded the floor in the code and found a second consumer my
predecessor had not named** — Test 38's abort — so "the default is wrong" became a two-consumer fact
rather than an inheritance. **+** **I proved
losslessness three ways the tool cannot grade itself on**, the strongest being a full reconstruction
of the pre-trim records zone from live + shard, byte-identical at 89,799 B — the trim is reversible
from the artifacts alone. **+** I checked the archive is *usable*, not merely present. **−** **I committed the exact error
my predecessor's ledger documents.** `text.index("```handoff")` matched
a substring in the front matter and my claim stub landed mid-sentence. It never reached a commit and the revert was
byte-identical, but the ledger held the countermeasure and I had read the page it was on. **−** **My first framing blamed the tool.** I wrote that the tool "sees 4 records
where the file has 6 — a discrepancy I must not build on." I did investigate rather than conclude,
which is why it took minutes and not longer, but the instinct pointed outward first. **When a tool
and a fresh edit disagree about a file you just edited, the edit is the suspect** — recorded in
`gotchas`. **−** A learning is owed and unwritten, the fourth in a row; I have stated the queue and
the reason rather than leaving it unsaid, which is the minimum the Degradation-Detection table asks,
not a substitute for the fix.


```handoff
session: S103
date: 2026-08-24
status: complete
self_score: 8
predecessor_score: 9
active_task: **Run the `CHANGELOG.md` trim. COMPLETE.** The file was **75,564 B against a 65,536 B ceiling, OVER by 10,028**, three sessions overdue (S102 `next_steps` (b)). It now stands at **39,148 B with 26,388 B of headroom**, and `methodology_trim.py --file CHANGELOG.md --check` reports **`trigger does not fire`** on both triggers — run it rather than trusting this sentence. **NOT DONE, DELIBERATELY: the `HANDOFFS.md` trim**, which still FIRES (79,884 B before this receipt, and this receipt adds to it). A second trim is a second capability (FM #26). **NO OUTWARD-FACING ACTION:** no push, no PR, no comment, no tag, no issue edit; the issue #75 branch is untouched and still local.
what_was_done: Three commits — `dbaaa94` (1B claim), `6be9388` (THE DELIVERABLE), this close-out. **(1) THE CUT WAS CHOSEN, NOT DEFAULTED, AND IT IS NOT THE TOOL'S DEFAULT.** The budget-driven default archives **28** to `CHANGELOG-through-2026-08-18.md` (→ 31,678 B) and raises **[CUT_STRADDLES_DAY]**: the cut key 2026-08-18 also names a RETAINED record, so that shard name would be a **span label, not a day boundary**. `--cut 2026-08-17` archives **26** and lands at 39,148 B. I paid **6,260 B of headroom** for a name that means what it says, because S100 was spent fixing a bug whose root was exactly *a name derived from a record DATE, while the cut is POSITIONAL, is not injective* (BL-41). Both figures are dry-run measurements, not estimates. **(2) THE SEAM IS PROVED CLEAN, NOT INFERRED FROM THE ADVISORY'S ABSENCE.** Retained records carry only **2026-08-18/23/24**; archived only **2026-08-15/16/17** — **no date on both sides**. **(3) I CHECKED WHAT READS THE LIVE LEDGER THAT IS NOT A HUMAN, BEFORE TRIMMING.** That is the hazard that disarmed five assertions when a live artifact was shrunk once before. Findings: `bin/check-handoff` only **PROHIBITS** `CHANGELOG.md:<N>` line anchors and never resolves a title, so archiving cannot break it; every `$P`-fixture test builds its own ledger; and Test 31 compares `model-report`'s Source 1 count against a raw anchored grep **on the same live file** — two derivations of one artifact, so shrinking moves the row's TEXT and cannot move its VERDICT. **(4) EVERY EXISTING PROOF WAS ARGUED INVARIANT FROM THE CODE FIRST**, then measured: each frozen proof reads `LIVE` through `git show TRIM^:` / `git show TRIM:`, pinning it to its own trim commit, so new history cannot reach it.
next_steps: (a) **`HANDOFFS.md` IS NOW THE ONLY FILE OVER A CEILING, AND IT IS THE OBVIOUS NEXT DELIVERABLE.** It was 76,854 B at Orient, 79,884 B after my claim stub, and this receipt adds more; `--check` FIRES on both triggers. **No name collision:** the most recent shard is `HANDOFFS-through-2026-08-18.md`, so a cut today derives a free name. **The constraint that does bind it is Test 34's retention floor of THREE receipts** — pass `--cut 3` or more explicitly, never the budget default, and re-run `bash bin/tests.sh` after (S94 took the default, retained 2, and the suite went 235/1 → 229/6). S101's per-record arithmetic still governs: at the 18,432 B budget a 3-receipt ledger measures `6,016 + 3 × 18,432 = 61,312 B`. (b) **THE ISSUE #75 PR IS STILL PREPARED AND STILL UNSENT, AND NEEDS A GO-AHEAD RATHER THAN MORE WORK.** Branch `docs/issue75-plan-surface-upstream` = `60246e7`, **local only — re-verified this session** with `git ls-remote --heads origin`, which returns nothing for it. Send commands are in [`docs/planning/issue75-upstream-pr.md`](docs/planning/issue75-upstream-pr.md); push to **`origin`**, never `upstream`. Upstream #75 is still the only open upstream issue, **no maintainer reply** since the 2026-08-16 comment. (c) **TWO LEARNINGS ARE OWED AND ONLY ONE FITS.** `starter-kit/FRAMEWORK_LEARNINGS.md` is at **63,126 / 65,536 — 2,410 B**, unchanged this session and unmeasured against any new row. S99's is now five sessions old; S102's is four. Mine would be *a cut whose derived name is a span label is a name that will be misread later — pay bytes for a clean seam.* All three need a go-ahead; the file is DISTRIBUTED. (d) `upstream/main` is **1 ahead** (`512c2ed`), fork **380 ahead** after this session; `git merge-tree --write-tree --name-only HEAD upstream/main` conflicted in exactly `CHANGELOG.md` and `HANDOFFS.md` — **computed at Orient, and I have written to both since, so RE-DERIVE.** (e) BL-37 (b), BL-39 and the long tail unchanged and **NOT re-verified**. **BL-16 has no heading of its own by design.**
key_files: **Every path and figure re-derived against the committed tree at close-out.** [`CHANGELOG.md`](CHANGELOG.md) — 39,148 B, **19 records** (18 retained + the tool's own entry); the new pointer block is at `:162`, the tool's trim entry at `:170`, my claim entry at `:178`. [`docs/archive/CHANGELOG-through-2026-08-17.md`](docs/archive/CHANGELOG-through-2026-08-17.md) — the frozen shard, 26 records, links rewritten to the `../../` prefix. [`docs/archive/CHANGELOG-through-2026-08-17.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-17.md.verify.sh) — the proof; **run it, do not trust a digest**. `starter-kit/methodology_trim.py` — v1.3.0, the tool; its `LEDGERS["CHANGELOG.md"]` spec at `:187` declares `regenerated=()`, which is why this file has **no count sentence to drift** the way `HANDOFFS.md`'s does. `bin/tests.sh:1958` Test 31, the `**Model:**` census that reads the live root ledger; `:1962` the raw grep it compares against. `bin/check-handoff:535` the locator-form regex — the reason a `changelog_ref` cites a TITLE and never a line number, and therefore the reason archiving is safe.
gotchas: **A GREEDY `sed` IN A DISPLAY FILTER CAN MANUFACTURE A DEFECT THAT IS NOT THERE.** Listing records through `sed 's/·.*\[/ [/'` matched to the **LAST** `[` on each line, so a perfectly well-formed heading — `S92 close-out … see the \`[issue #75]\` entry below` — rendered as a truncated, malformed one. I went looking for a corrupt record in the ledger and found the corruption was in my own pipe. **A transform used only for display is still an instrument; if it disagrees with the file, suspect it first.** **THE PROOFS READ `LIVE` FROM GIT, NOT FROM THE WORKING TREE** — `git show TRIM^:` / `git show TRIM:` — so a frozen proof is pinned to its own commit and later trims cannot redden it. Read that branch in the script before predicting a census; the else-branch (working tree) applies only *before* the trim is committed, which is why the same script prints `source: HEAD vs the working tree` pre-commit and `source: the trim commit 6be9388` after. **THE `[CUT_STRADDLES_DAY]` ADVISORY IS A NAMING WARNING, NOT AN ERROR** — the tool writes correctly either way. Its absence after `--cut` is evidence the seam is clean only if you also check the dates on both sides, which is cheap: `grep -oE '^### [0-9]{4}-[0-9]{2}-[0-9]{2}' | sort -u` on the live file and the shard. **A CONTROL RUN IN THE TREE YOU ARE EDITING IS NOT A CONTROL.** I ran the pre-change suite in a **`git worktree` at `da40bdb`**, so it was immune to my writes by construction rather than by my remembering not to write — S102 tried the discipline version and its baseline still misread one row by one. `git worktree add <scratch> <sha>`; it costs seconds. **`bin/check-*` ARE PYTHON, and `dashboard_history.jsonl` goes dirty from Phase 0 alone — DO NOT `git reset --hard`.**
runtime_smoke: **THIS REPO SHIPS NO APPLICATION; THE BUILD-EQUIVALENT IS THE SUITES PLUS THE TOOLS, RUN — AND THE PRE-CHANGE HALF RAN IN A PRISTINE WORKTREE SO IT COULD NOT BE CONTAMINATED.** **SUITE, ROW-FOR-ROW.** Pre-change control at `da40bdb` in a separate checkout: **279 passed / 1 failed**. Post-change on the committed tree: **279 / 1**. Both populations asserted non-empty (**280 rows each**). Sorted row-set diff: **ZERO rows lost, ZERO net added, EXACTLY THREE rows changed**, and all three carry a count in their own name — `handoff_anchors … (4)→(5)` and `receipt-id population … (4)→(5)` (my claim stub, expected), and Test 31's `Source 1's entry count (29) matches the raw anchored grep (29)` → **`(16)` matches `(16)`**. That **16 was predicted at claim time and derived, not guessed**: 29 + 1 (claim entry) + 0 (the tool's entry carries `**Written by:**`, no Model bullet) − 14 (Model bullets inside the archived region, counted). Both sides of that assertion moved together, which is the proof it is a same-file self-consistency check. Sole failure **BOTH** times: Test 9's pre-existing `--source=github` 404, confirmed **BY NAME**, not by count. **PROOFS.** All **13** `.verify.sh` re-run: **9 green / 4 red**. Predicted at claim as *"the same 8 green / 4 red, plus one new green"* — **exact**; the four reds are the same four as before, **zero reddened**. The new proof runs green in both forms, pre-commit (`HEAD vs the working tree`) and post-commit (`the trim commit 6be9388`). **TRIM INTERNALS:** `L1_OK`, `L2_OK`, `L3_OK`, `P1A_OK` (18 → 19), and the emitted proof run directly: *"44 before = 18 retained + 26 archived; added by the trim commit: 1"*. **AN INDEPENDENT CROSS-CHECK AT A DIFFERENT LEVEL THAN L1/L2/L3** — the file's OWN documented source-tag audit across live **plus** archives: **287 → 289**, i.e. **+2 = exactly this session's two added entries, and not one archived record dropped out of the census.** **PYTHON:** **451/451** (300 + 110 + 41), matching S102. **CHECKERS:** `check-links` **88 links / 22 files** and `check-learnings` **35 rows, contiguous 1..35** — both measured on the pristine worktree too and **byte-identical pre and post**, so neither moved (S102's `83 / 21` was its upstream-based BRANCH, a different tree, not a regression here). `check-handoff --all` clean. **FM #28 GATE:** `CHANGELOG.md` **ok — 39,148 / 65,536 at the trim commit `6be9388`, 26,388 B free; the close-out entry written after this receipt brings it to just over 41,400 B, still more than 24,000 B clear** (stated at a NAMED point rather than as "after the last write", because this receipt and that entry each move the other's file and no single figure can be last for both); `CLAUDE.md` ok (11,064); `docs/planning/BACKLOG.md` ok (183 ln); `starter-kit/FRAMEWORK_LEARNINGS.md` ok (63,126 / 65,536, 2,410 B left); **`HANDOFFS.md` OVER** — figure in the close-out entry, measured last. **WHAT NONE OF THIS EXERCISES:** GitHub delivery, review, or merge. No network path was tested, because none can be without sending something.
changelog_ref: CHANGELOG.md "2026-08-24 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-08-17.md` (26 record(s), 76,774 B → 39,148 B)", plus "[ad hoc] S103 claim — run the `CHANGELOG.md` trim" and "[ad hoc] S103 close-out"
commit: dbaaa94 (1B claim) + 6be9388 (the trim) + this close-out
```

<!-- claim stub written at session start; completed at close-out -->
Model: Claude Opus 5 (1M context).

**Predecessor S102 scored 9/10.** **+** **Every operational claim it handed me reproduced exactly,
and I checked each rather than inheriting it:** the suite baseline (279/1, sole failure named by
name), the proof census (8 green / 4 red), the `merge-tree` conflict set, the branch state (`60246e7`,
local only), and — the ones this session actually stood on — *"`--check` FIRES"*, *"no name
collision"*, and *"no Test-34-style retention floor binds this ledger."* I re-derived that last one
independently by grepping for live-root consumers, and it was right. **+** **Its `next_steps` (b) is
the reason this session was one afternoon and not two.** It named the deliverable, its exact
overage, its overdue-ness, and it pre-cleared the two blockers that would otherwise have had to be
discovered — that is what a handoff is for. **+** **Its gotchas were load-bearing and changed what I
did.** *Anchor on LINE-ANCHORED fences and assert the COUNT* — both my splices worked first time
because of it. *Do not launch a pre-change baseline and then write while it runs* — I went further
and ran the control in a separate worktree, an idea I had only because it had named the failure
precisely enough to fix structurally rather than by care. **+** It disclosed costs it had imposed
rather than burying them, including making `CHANGELOG.md` worse and being unable to fit an owed
learning. **−** **The one thing that cost me time: `check-links: OK (83 links / 21 files)` in its
`runtime_smoke` does not carry its surface.** Four surfaces are reported in that field and the
figure appears once; on the fork it is **88 / 22**. Its Surface-1 heading does scope it to the
branch, so a careful reader can attribute it — but I had to re-measure in the pristine worktree to
prove I had not caused a regression. **State the tree beside the figure**, the same way this repo
already insists on stating the population beside the number. Not a 10 because of that; not an 8
because I could not find a single claim in it that was wrong, and this is the first receipt in
several where the successor had nothing to correct.

**Self-assessment: 8/10.** **+** **I recorded four predictions at claim time, derived rather than
guessed, and all four held exactly** — the `**Model:**` census 29 → **16** (from a counted 14, not an
estimate), the proof census **9 green / 4 red of 13**, the frozen proofs' invariance (argued from
`git show TRIM^:`/`TRIM:` in the script *before* measuring), and Test 31 staying green while its row
text moved. Writing them into the claim commit is what made them falsifiable instead of
retrospective. **+** **I chose the cut instead of taking the default, and priced the alternative in
bytes**: 6,260 B of headroom for a shard name that is a true day boundary rather than a span label.
**+** **I proved the seam clean rather than reading the advisory's absence as proof** — dates on both
sides, disjoint. An absent warning is not evidence. **+** **I asked what reads this file that is not
a human, before shrinking it**, which is the exact hazard that silently disarmed five assertions the
last time a live artifact was shrunk here. **+** The control was uncontaminated **by construction** —
a worktree — not by my discipline. **+** I cross-checked losslessness at a level the tool's own
L1/L2/L3 does not cover, using the file's own documented audit: 287 → 289, +2 and no record lost.
**−** **I manufactured a defect that did not exist** with a greedy `sed` in a display filter, and
chased a "malformed heading" in the ledger before recognising the corruption was in my own pipe. I
caught it in one step and it changed nothing, but I had published the mangled listing in my own
reasoning first. **−** **I left `HANDOFFS.md` further over its ceiling than I found it** — 76,854 B
in, and this receipt adds to that. Structurally forced (FM #26 makes the second trim a second
capability) and handed forward as (a) with its binding constraint stated, but the debt is real and
it is now mine as much as inherited. **−** I discovered the `83/21` vs `88/22` discrepancy by
tripping over it rather than by measuring `check-links` on both surfaces from the start; a
30-second pre-change measurement would have cost nothing. Not a 9 because of the self-inflicted
false alarm and because the file I was least asked about ends the session worse; not a 7 because the
deliverable is complete, verified on five independent axes, and every prediction I committed to in
advance survived.

```handoff
session: S102
date: 2026-08-24
status: complete
self_score: 8
predecessor_score: 7
active_task: **Prepare the upstream PR for [issue #75](https://github.com/KJ5HST/methodology/issues/75) and send nothing. COMPLETE.** Branch `docs/issue75-plan-surface-upstream` = `60246e7`, based on `upstream/main` (`512c2ed`), 1 ahead, 3 files, +172/−1, **LOCAL ONLY** — proved by `git ls-remote --heads origin`, which returns nothing for it, not by my own recollection of not having typed `push`. **NO OUTWARD-FACING ACTION: no push, no PR, no comment, no tag, no issue edit.** **TWO INHERITED CLAIMS WERE CORRECTED AT ORIENT AND ONE OF THEM RESHAPED THE TASK.** (1) *"Issue #75's prepared answer remains unsent"* — carried verbatim by S99, S100 and S101 — is **wrong about the comment**: it was posted 2026-08-16 with the operator's explicit per-action go-ahead (`issuecomment-5305674268`, recorded at `143ff2b` in the very ledger those receipts were writing to). What was never sent is the **implementation**. (2) *"Eleven sessions"* is not derivable from any population I could find; enumerating receipts across `HANDOFFS.md` + the archives gives S93–S101 = **9**. I repeated the inherited figure once in my own Phase 0 report before deriving it. **THE GAP ITSELF IS REAL AND WAS RE-VERIFIED IN BOTH TREES:** fork `main` checklist **7** items / quote **2x**; `upstream/main` **6** / **1x**. ALL SIX CLAIM DECLARATIONS HELD.
what_was_done: Three commits — `b300098` (1B claim), `ebe69eb` (THE DELIVERABLE), this close-out; plus `60246e7` on the unpushed branch. **(1) THE FINDING THAT MADE THIS MORE THAN A CHERRY-PICK.** Fork `main`'s `starter-kit/SESSION_RUNNER.md` differs from `upstream/main` in **FIVE** hunks; only **TWO** are #75. The other three — Phase 3C rerouted to `FRAMEWORK_LEARNINGS.md`, the `**Model:**` ledger bullet, and the Learnings-table extraction — **all depend on `starter-kit/FRAMEWORK_LEARNINGS.md`, which does not exist upstream** (nor does `starter-kit/methodology_trim.py`). A whole-file take would have carried three unshipped changes into a one-issue PR. Built instead by applying `b1b7eaf`'s patch for that file alone; `git apply --check` passed first. **(2) THE TEST NUMBERING COLLIDES ACROSS THE TWO REPOS.** The fork's Tests 32/33/34 **are** upstream's 23/24/25 — upstream `bin/tests.sh` is 650 lines against the fork's 2,981 — so the fork's Test 36 ports as **Test 26**. Fork-only references were rewritten, not carried: `BL-10` and the fork session ids are gone, and the citation census is stated as **the commands that reproduce it** rather than as line numbers that will drift. **(3) THE UPSTREAM CENSUS IS CLEANER THAN THE FORK'S, AND THE PR BODY USES UPSTREAM'S.** On `upstream/main`: `"Faithful verification, per surface"` **1** (its own definition), `gate (d)` **0**, `gate d` **1** — inside gate (d)'s own section. Nothing outside §Vertical Slice Sessions referred to it in **either** spelling; the fork had one such citation, in a fork-only planning file that does not exist there. **(4) LEARNING #29 DELIBERATELY EXCLUDED FROM THE PR**, with the reason written into the draft rather than left implicit: upstream has no `FRAMEWORK_LEARNINGS.md`, so the row would be **#14** in the 13-row table inside `SESSION_RUNNER.md` — a numbered set upstream's own Tests 23/24 pin — inside a PR about something else. Offered as a follow-up.
next_steps: (a) **THE PR IS READY AND SENDING IT IS ONE COMMAND AWAY — IT NEEDS A GO-AHEAD, NOT MORE WORK.** [`docs/planning/issue75-upstream-pr.md`](docs/planning/issue75-upstream-pr.md) carries the exact `git push origin …` + `gh pr create …` pair; the body is its `-body.md` sibling, `--body-file`-ready and unedited. Push to **`origin`**, never `upstream`. **The most likely pushback is the two-site shape** rather than the issue's one-line diff — that argument is in the draft and in the 2026-08-16 comment, and the six-item mirror check behind it is re-runnable. (b) **`CHANGELOG.md` IS THE ONLY FILE OVER A CEILING AND I MADE IT WORSE, KNOWINGLY.** It arrived **70,422 B** (over by 4,886) and leaves at **75,564 B — over by 10,028** — because FM #27 owed it three entries and its trim is a second capability (FM #26). `methodology_trim.py --file CHANGELOG.md --check` **FIRES** on both triggers; **no name collision** (most recent shard `CHANGELOG-through-2026-08-15.md`, so a cut today derives a free `2026-08` name) and **no Test-34-style retention floor binds this ledger** — the constraint that bound S101 does not bind here. This is now **three sessions overdue** and is the obvious next deliverable if the operator does not send the PR. (c) **`HANDOFFS.md` HAS LITTLE HEADROOM LEFT.** It arrived 59,815 B and leaves at **76,854 B — OVER by 11,318**, this receipt being ~17 KB of that. S101's durable arithmetic still governs: per-record budget 18,432 B, Test 34's floor 3 receipts, so a post-trim ledger at that budget measures `6,016 + 3 × 18,432 = 61,312 B`. **Trim every session or the breach returns.** (d) **TWO LEARNINGS ARE NOW OWED AND ONLY ONE FITS.** `starter-kit/FRAMEWORK_LEARNINGS.md` is at **63,126 / 65,536 — 2,410 B**, one ordinary row. S99's is now **four** sessions old (*a losslessness proof only proves losslessness of the population it enumerates*); mine would be *a change prepared in a fork is not a change prepared for upstream — the file's other differences travel with a whole-file take*. **Raised to the operator at close-out and scoped out, exactly as S101's was — not silently skipped.** Both need a go-ahead; the file is DISTRIBUTED. (e) `upstream/main` is **1 ahead** (`512c2ed`), fork **376 ahead**; `git merge-tree --write-tree --name-only HEAD upstream/main` conflicts in exactly `CHANGELOG.md` and `HANDOFFS.md` — computed at Orient, and **I wrote to both since, so RE-DERIVE.** (f) Upstream #75 is still the only open upstream issue, **no maintainer reply since our 2026-08-16 comment**. (g) BL-37 (b), BL-39 and the long tail unchanged and NOT re-verified. **BL-16 has no heading of its own by design.**
key_files: **Every path re-derived against the committed tree at close-out.** [`docs/planning/issue75-upstream-pr.md`](docs/planning/issue75-upstream-pr.md) — fork-only; the send commands, the three decisions, and the "what is deliberately NOT in the branch" section that carries the five-hunk finding. [`docs/planning/issue75-upstream-pr-body.md`](docs/planning/issue75-upstream-pr-body.md) — fork-only; the PR body, ending in the agent-authorship disclaimer (`workstreams/DEVELOPMENT_WORKSTREAM.md:50` states the recommended form). On the **branch** `docs/issue75-plan-surface-upstream` (`git checkout` it; the worktree it was built in is gone, the branch is not): `starter-kit/SESSION_RUNNER.md:133` the **The surface** bullet, `:138` the paragraph quoting gate (d), `:150` the checklist line, `:163` gate (d) itself — **cited, never moved**; `bin/tests.sh:565` Test 26, `:695` the `context_budget.py` block it was inserted before. On `main`: `starter-kit/SESSION_RUNNER.md:133`/`:150` the same two sites, already present since `b1b7eaf`; `bin/tests.sh:2398` Test 36, the fork original. `bin/_manifest.py` — the carve-out population, **26** rows.
gotchas: **A CONTENT ANCHOR IS NOT UNIQUE JUST BECAUSE IT LOOKS LIKE MARKUP.** My first `HANDOFFS.md` splice anchored on the receipt fence as a bare substring and landed in the FRONT MATTER, because the header documents its own recount command — a `grep -c` for that very fence — in prose. My assert (*the prefix contains no earlier fence*) was true and useless — it asserted about the wrong thing. **Anchor on LINE-ANCHORED fences (`l.startswith(...)`) and assert the COUNT equals the known receipt count**; `check-handoff` caught it in one run and `git checkout HANDOFFS.md` undid it. **A HEREDOC WHOSE TERMINATOR YOU NEVER EMIT SWALLOWS THE REST OF THE SCRIPT SILENTLY** — my first stub payload ended with `FENCEEOF` while the terminator was `STUBEOF`, so the following `sed` and `wc` lines were written INTO the payload and the command printed nothing at all. **A command that produces no output is a symptom, not a success.** **DO NOT LAUNCH A "PRE-CHANGE" BASELINE AND THEN WRITE WHILE IT RUNS.** My Orient `bin/tests.sh` was still executing when I committed the claim, so the one row that names a count read **27** where the true pre-change value was **26**. The assertion compares two derivations of the SAME live file, so it could not have failed — but a control that overlaps the change is not a control. **A FILTER IN A CARVE-OUT CHECK IS PART OF THE POPULATION.** My first manifest extraction required `"/" in path` and silently dropped `HOW_TO_USE.md` and `ITERATIVE_METHODOLOGY.md` — two DISTRIBUTED root-level files. Caught only because 24 disagreed with the 26 prior receipts report. **RUN A CHECKER'S OWN PATTERN, NEVER YOUR RECOLLECTION OF IT:** the `**Model:**` census is `^-?[[:space:]]*\*\*Model:\*\*` (optional leading `- `), and my `^\*\*Model:\*\*` was off by one. **`bin/check-*` ARE PYTHON. DO NOT `git reset --hard`** — `dashboard_history.jsonl` goes dirty from Phase 0 alone.
runtime_smoke: **FOUR SURFACES, AND THE ONE THAT MATTERS IS THE BRANCH — running the fork's suite says nothing about a tree built from `upstream/main`.** That is the requirement #75 itself adds, applied to its own PR. This repo ships no application; the build-equivalent is the suites plus the tools, RUN. **SURFACE 1 — THE BRANCH, RED FIRST.** Pre-change control on a pristine `upstream/main` tree: **114 passed / 0 failed**, exit 0. RED with Test 26 added and the runner unpatched: **5 of its 6 rows FAIL**, populations non-empty (`POP crit=390 items=6 slice=5469`); the 6th is the population-guard control, which must pass either way. GREEN at final branch state: **120 / 0**, exit 0. Row-for-row diff of the two runs, both populations asserted non-empty (114 / 120): **exactly 6 rows added, ZERO lost.** `check-links` OK (83 links / 21 files), `check-learnings` OK (13 rows, contiguous 1..13), `check-handoff --all` OK. **SURFACE 2 — A REAL ADOPTER TREE, which surface 1 cannot speak for.** `bin/sync` from the branch into a fresh `git init`: delivered `SESSION_RUNNER.md` **byte-identical** (`diff -q` clean), **7** checklist items, and **2** occurrences of the quoted phrase — the citation's referent travels in the same file, so it cannot dangle at an adopter merely by being synced. **SURFACE 3 — THE FORK, unchanged as declared.** `bash bin/tests.sh` **280 rows, 279 / 1**, the sole failure Test 9's pre-existing `--source=github` 404 confirmed **BY NAME**; the single differing row against the Orient run carries a count in its own name (`**Model:**` 27 → 28) and moves to **29** when this close-out's entry lands — a derived prediction, not an estimate. Python suites **451/451** (300 + 110 + 41). All 12 shipped `.verify.sh` proofs re-run and `diff`ed against the pre-change census: **8 green / 4 red, IDENTICAL** — zero reddened. **SURFACE 4 — THE OUTWARD CHANNEL, PROVED SHUT.** `git ls-remote --heads origin <branch>` returns nothing; `git worktree list` shows only the main checkout. **CARVE-OUT, verified mechanically and then re-verified after I found my own filter bug:** **26** `bin/_manifest.py` DISTRIBUTION rows against **5** changed paths on `main`, both populations asserted non-empty, and a fixture control proving `starter-kit/SESSION_RUNNER.md` and `starter-kit/FRAMEWORK_LEARNINGS.md` are IN the population so the test cannot pass for the wrong reason — **INTERSECTION NONE.** **FM #28 GATE:** `CLAUDE.md` ok (11,064); `docs/planning/BACKLOG.md` ok (183 ln); `starter-kit/FRAMEWORK_LEARNINGS.md` ok (63,126 / 65,536, **2,410 B left**, unchanged); **`HANDOFFS.md` OVER by 11,318** (76,854) and **`CHANGELOG.md` OVER by 10,028** (75,564) — both measured after the last write, both knowingly, both `next_steps` (b)/(c). **WHAT NONE OF THIS EXERCISES:** GitHub delivery, review, or merge. No network path was tested, because none can be without sending something.
changelog_ref: CHANGELOG.md "2026-08-24 · [issue #75] Upstream PR prepared and NOT sent — branch `docs/issue75-plan-surface-upstream`, local only", plus "[issue #75] S102 claim" and "[ad hoc] S102 close-out"
commit: b300098 (1B claim) + ebe69eb (the deliverable) + this close-out; branch commit 60246e7, unpushed
```
<!-- claim stub written at session start; completed at close-out -->
Model: Claude Opus 5 (1M context).

**Predecessor S101 scored 7/10.** **+** Everything operational it handed me reproduced exactly: the
suite baseline (280 rows, 279/1, sole failure named), the proof census (8 green / 4 red), the
`merge-tree` conflict set, and the `CHANGELOG.md` trim state down to *"no name collision, `--check`
FIRES."* I verified each rather than inheriting it, and found nothing wrong. **+** Its gotchas were
load-bearing rather than decorative — *anchor on CONTENT and assert the match count*, *do not put a
fence inside a heredoc*, *the suite takes 10+ minutes, run it in the background*, *do not `git reset
--hard`* — and all four changed what I did. Two of them I then violated in a *new* way and caught
instantly **because** it had told me what class of thing to watch. **+** It disclosed its own costs
plainly, including the `CHANGELOG.md` breach it made worse. **−** **The one claim the operator acted
on this session was wrong, and had been wrong for three consecutive receipts.** Its `next_steps` (g)
— *"Upstream issue #75 remains the only open upstream issue; S92's answer prepared, vetted,
unsent"* — conflates the **comment** with the **implementation**. The comment was sent on
2026-08-16, on an explicit go-ahead, and is recorded at `143ff2b` in the very ledger S101 was
writing to. This was not flagged as unverified; (i) explicitly scopes the "not re-verified" label to
BL-37 (b), BL-39 and the long tail, and (g) is not in that set. **−** **Its "eleven sessions" is not
derivable from any population I could find.** S100 wrote "ten", S101 wrote "eleven"; the receipts
enumerate to **9**. A number that is incremented rather than derived is this repo's own named
failure — *state the population beside the number* — arriving in the field the operator reads first.
Not an 8, because a status claim about the repository's stated purpose propagated unchecked across
three sessions and cost the fork ten sessions of ambiguity about whether the channel was open. Not a
6, because its deliverable survived independent re-execution and every warning it wrote earned its
place.

**Self-assessment: 8/10.** **+** **I re-derived the two inherited claims before doing anything, and
one of them changed the shape of the task** — "prepare the PR" is a different job from "send the
answer," and I would have done the wrong one. **+** **The five-hunk finding is the session's real
value.** A whole-file take would have carried three unshipped fork changes into a one-issue PR, all
of them depending on a file that does not exist upstream. I found it by diffing the two trees rather
than by trusting that `b1b7eaf` was the whole story — and then applied `b1b7eaf`'s patch for that
file alone, `git apply --check` first. **+** **I verified on the branch, not the fork**, with a
pristine pre-change control (114/0), a RED round proving 5 of 6 rows fail unpatched with populations
non-empty, and a row-for-row diff showing +6 / −0. That is the requirement #75 adds, applied to its
own PR. **+** I proved the outward channel shut with `git ls-remote` rather than asserting it. **+**
When my carve-out population read 24 against the 26 prior receipts report, I chased the disagreement
instead of publishing my number — and found my own filter had silently dropped two DISTRIBUTED
root-level files. **−** **My "pre-change" baseline overlapped my own claim write.** The Orient suite
was still running when I committed, so the one row naming a count read 27 where the true pre-change
value was 26. No verdict moved and the assertion could not have failed, but a control that overlaps
the change is not a control, and I know that. **−** **Two splices went wrong before one went
right**: a fence anchor that was not unique because the file documents its own recount command, and
a heredoc terminator I never emitted, which silently wrote script text into a payload and printed
nothing. I read the gotcha warning about exactly this class an hour earlier. **−** I left
`CHANGELOG.md` further over its ceiling — structurally forced by FM #27, but three entries' worth.
**−** Two learnings are now owed and only one fits in the budget; I raised that rather than deciding
it alone, which is right, but it means the debt is now four sessions old. Not a 9 because two of my
own edit mechanics failed on first attempt and one of my controls was contaminated by my own writes;
not a 7 because every one of those was caught in-session by a check I had chosen to run, and the
deliverable was verified on the surface it will actually be judged on.


