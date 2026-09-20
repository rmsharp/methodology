# Handoff Receipts — durable close-out proof

This repository dogfoods its own methodology: every session records a durable, machine-checkable
`handoff` receipt here at close-out (Phase 3D), and Phase 0 reconciles it against `git log`. See
[`starter-kit/HANDOFFS.md`](starter-kit/HANDOFFS.md) for the block format and the write points, and
`bin/check-handoff` for the checker. Newest on top; prepend-only.

**Retention policy — keep ONE receipt, trim above TWO.** Everything older is archived under
`docs/archive/` and indexed in [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md). **N=1 is an operator decision (2026-09-16, S172)
replacing S127's N=4**, taken against BL-59's measurement of what actually reads this file: the
handoff is done by the newest receipt alone. **Depth and trigger are separate on purpose:**
every trim pays a FIXED ~16 KB proof, so the trigger sits one above the depth (BL-60). **`methodology_trim.py` fires on BYTES (196,608 B),
never on a record count**, so the policy is applied by the session that notices: Phase 0 runs
`grep -c '^```handoff' HANDOFFS.md` and reports the count; **above 2**, the trim is its own action after
that report, never inside Phase 0, which is read-only apart from the reconcile backfill
(`starter-kit/SESSION_RUNNER.md` Phase 0): `--cut 1 --force`. The force is
warranted, not an override — `SRF_RED` refuses every on-schedule retention trim by construction
(BL-59). `bin/check-handoff` validates the 13-key schema on the **newest** receipt; `--all` checks
every receipt and `--archived` a frozen shard. Below three receipts Test 34 prints six named `SKIP` rows — stated, never silent.

**Two session sequences share this ledger and their numbers collide.** This fork and
`upstream/main` each run their own `S<N>` counter, so a receipt is identified by **session + date**,
never by number alone. **Every upstream receipt is now archived**; every receipt retained here is
the fork's. At a resync the two sequences stay separate and unrenumbered, each incoming receipt is
checked against ours before it is kept, and within a shared date the fork's precede the arriving
upstream ones (precedent: `fc4d297`).

> **THE HAND-MAINTAINED RECEIPT COUNT IS GONE, DELIBERATELY.** S172's rewrite dropped *"This file
> currently holds **N**"* — the number [Learning #12](starter-kit/FRAMEWORK_LEARNINGS.md) and upstream
> [issue #65](https://github.com/KJ5HST/methodology/issues/65) both cite as always wrong by the next
> close-out. The trimmer still declares it, so **every trim now reports `FRONTMATTER_FIELD_ABSENT`**:
> stated, expected, not a failure. Removing the declaration is distributed — its own go-ahead (BL-60).
> **Count with `grep -c '^```handoff' HANDOFFS.md`.**

> **⚠ THREE is the floor the retention policy sits one above.** `bin/tests.sh` Test 34 mutates *this*
> ledger to check `check-handoff --all`'s whole-ledger invariants, reading two anchors from the live
> file — not hardcoded, so it survives *which* receipts rotate, but it needs three to exist. A short
> ledger is **stated rather than silent** (BL-40 (b)): below the floor those six assertions print as
> `SKIP` rows naming themselves, the summary carries a skip count, and a ledger with *zero* receipts
> still FAILS — corruption is not rotation. **Nothing prevents a cut below three; the policy is what
> makes it not happen.** Re-run `bash bin/tests.sh` after any trim of this file.

**The shard index is not in this front matter, on purpose.** It lived here until S174 and grew a row
with every trim against the fixed 7,168 B header reserve (Test 39 A2), so it moved out rather than the
reserve rising. A trim commit still carries the trimmer's ~448 B pointer block; the fold removes it, so a
trim-and-fold no longer grows this front matter. The fold rule is in the index.

<!-- NEXT TRIMMING SESSION: methodology_trim.py appends a 3-line pointer block here
     (starter-kit/methodology_trim.py:1093 build_pointer_block, :1103 insert_pointer). Fold it into
     docs/HANDOFFS_ARCHIVE_INDEX.md as one row and delete the block, IN ITS OWN COMMIT: inside the
     trim commit the shipped .verify.sh fails L2 (fork Learning #58). -->

**Archived 1 record(s), 2026-09-20 → 2026-09-20** into [`docs/archive/HANDOFFS-through-2026-09-20-2.md`](docs/archive/HANDOFFS-through-2026-09-20-2.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/HANDOFFS-through-2026-09-20-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-20-2.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

```handoff
session: S201
date: 2026-09-20
status: pending
active_task: **BL-53 P4 — D3 written into `CLAUDE.md`**, the steady-state obligation of [`docs/planning/fork-learnings-retirement-rule-plan.md`](docs/planning/fork-learnings-retirement-rule-plan.md) §8, fork-only and deliberately NOT in the distributed `SESSION_RUNNER.md`. Chosen by the operator after Phase 0 (picker) over BL-78's costing and BL-77's. **The remedy left open at S200 is answered in the same picker: option C — the 81,920 B ceiling on `docs/FORK_LEARNINGS.md` becomes a reported series, the per-row budget stays, B declined with its 14,502 B known.** Implementing C is P5, a separate session; this one writes the rule and records the decision. Session claimed. Work beginning.
```

```handoff
session: S200
date: 2026-09-20
status: complete
self_score: 8
predecessor_score: 9
active_task: **BL-53 P3 — THE CATCH-UP PASS RAN AND THE RATIFIED CRITERION RETIRES NOTHING.** Chosen by the operator after Phase 0 (picker) over BL-77's costing, over this session's own SAFEGUARDS finding and over BL-74. **P2 was answered in the same picker — option A + C's D3 pairing** — and is recorded in `CHANGELOG.md` and in BL-53's backlog row, which was its DONE criterion. All **69** rows of `docs/FORK_LEARNINGS.md` (15–83) were read **in full** and tested against all three D1 limbs; every row has a verdict and a basis in [`docs/planning/fork-learnings-adjudication-2026-09-20.md`](docs/planning/fork-learnings-adjudication-2026-09-20.md). **0 retirements.** **P3's DONE list also asks for "the file under 81,920 B", and that bullet is UNREACHABLE under the ratified criterion — reported unmet, not quietly dropped.** No `docs/archive/FORK_LEARNINGS-retired.md` exists, because nothing qualified to move into it. Three side actions approved in the same picker and all done: the owed trim with its fold, this close-out's push, and BL-78 filed.
what_was_done: **Phase 0:** `CHANGELOG.md` frontier = HEAD `05fc293`, gap empty; `HANDOFFS.md` frontier `1530bbc` with only the push record above it, already ledgered — nothing backfilled, no pending stub, **2** receipts. The gate was **re-run rather than read from `.quality-gates-results.json`**, which was four sessions stale (S195's, head `431279b`): in a `--no-local` clone with HEAD asserted by sha, `11/11 · results 10575dac7361 · manifest 01a4ae7aa511`, **S199's citation exactly**. `core.hooksPath` = `.githooks`, no markers (BL-77's own check). Dashboard 76/100. **`fc2dac1`** claim. **`f1f51b3`** the owed retention trim (`--cut 2 --force`, 26,597 → 16,014 B; SRF / CUT_STRADDLES_DAY / FRONTMATTER_FIELD_ABSENT all stated and expected; L1/L2/L3 OK) and **`9d30247`** its fold, in its own commit. **`d4690d8`** the adjudication. **`53ba69e`** P2 in BL-53's row, **BL-78** raised. **`c2feca4`** fork Learning **#84**. **THE TWO STRUCTURAL LIMBS WERE MEASURED, NOT ARGUED:** (b) 13 rows cite an earlier row and **every citation differentiates** (*sibling of*, *distinct from*, *the converse of*) — a session whose lesson would have superseded one wrote a narrower row citing it instead — while **8 rows are cited BY another live row or live config**, so removal is resisted at both ends; (c) 38 rows name a path, **56 mentions, all 56 resolving to a tracked file.** (a) is partial by construction, and for row `#47` unsatisfiable by the row's own content. **THE PLAN'S "AT MOST 2" WAS A BOUND FROM A TEN-ROW SAMPLE**, scored *partly*; D1 says *when, and only when, one of these holds*. Six rows are partly covered in all; the census is **0**.
next_steps: **(1) BL-53 IS BACK WITH THE OPERATOR, AND THE QUESTION HAS CHANGED.** It is no longer *"what is the rule"* — the rule is ratified and applied — but **which remedy, given that the rule recovers nothing**: **C** (demote the ceiling to a reported series, keep the per-row budget) is now the option that *matches the measurement* rather than accommodating it, and **B** (oldest-first to a depth you state) is still the only one that recovers real bytes, now costed **row by row** in §5 rather than by age. **Keep D3 either way — it is what stops future growth, and fork Learning #49 is why a steady-state rule cannot clear an existing overage.** **P4 — writing D3 into `CLAUDE.md` — is the natural next session** and needs no further decision. **(2) THE FILE IS 86,727 B, 4,807 B OVER**, because this close-out appended row #84 and retired none. That is the fourth consecutive appending session; unlike the three before it, this one **established why** and the reason is in the adjudication, not in a new estimate. D3 is satisfied in its strongest form: all 69 considered, none qualifies. **(3) BL-78 IS RAISED AND UNCOSTED** — `starter-kit/SAFEGUARDS.md` 1,743 B over a declared no-growth pin since 2026-09-14, nothing in the commit path measuring it, and the pin's *"byte-identical with upstream"* warrant **false in both halves**. The blob comparison is **already done**; the open question is only which number is right now. **(4) TWO PULL REQUESTS ARE OPEN AND STILL UNREVIEWED** — [#85](https://github.com/KJ5HST/methodology/pull/85) (`e2501c5`) and [#84](https://github.com/KJ5HST/methodology/pull/84) (`77afc12`), both MERGEABLE, **0 reviews and 0 comments**, #84 unchanged since 2026-09-19T04:21Z — now five sessions static. **Each reply is its own go-ahead.** **(5) BL-77 IS STILL OPEN AND STILL UNCOSTED.** **(6) NO `HANDOFFS.md` TRIM IS OWED AT THE NEXT PHASE 0** — this close-out leaves **2** receipts — **but that session's claim makes three, so it falls due right after its report, at `--cut 2`** (`--cut N` RETAINS N). Raise it in the Phase 0 picker. **(7) `CHANGELOG.md` IS 174,797 B AT THIS RECEIPT, 87,347 B UNDER THE 262,144 B REFUSAL** — measured after this entry was written, so the commit carrying this line does not change it; it grew **16,408 B** this session. **(8) BL-74 AND BL-75 REMAIN UNDECIDED**, and BL-75 was observed a third time (the `--status` flag still does not exist; the default run appended its history row at Phase 0). **CARRIED:** BL-73, BL-54's own PR, the `vscode_quarto_ext` relay, BL-68, BL-61, BL-60, BL-65, BL-66, BL-69, BL-70, BL-71, `model_project_constructor`'s push and its bare-`ruff` regression, `airqino`'s `HANDOFFS.md` migration in its own repository.
key_files: `docs/planning/fork-learnings-adjudication-2026-09-20.md` — §1 the result and why *partly* is not *holds*, §3 the two measured limbs **and the instrument's own failure**, §4 the options after the pass, **§5 the 69-row table (this is the durable artifact: read it before re-adjudicating anything)**; `docs/planning/BACKLOG-DETAIL.md` BL-53 (D1–D4 as ratified, above its *"What would answer it"* paragraph) and **BL-78** at the end of the file, with `docs/planning/BACKLOG.md:167` its index row; `docs/FORK_LEARNINGS.md:96` (row **#84** — line 96, and note S199's receipt cited row #83 at `:104` when that file was 95 lines long); `bin/check-learnings:76` (`RESERVED_RE`, the declared gap D2 relies on — verified exact), `ROW_BUDGET_BYTES` = 1,500 (it refused two drafts of #84 at 1,601 B and 1,508 B); `.context-budget.json:104`–`:110` (the SAFEGUARDS entry whose `_` note declares the pin and the now-false byte-identity warrant); `.quality-gates.json` (eleven gates — **none** of them reads budget status, which is half of BL-78).
gotchas: **(1) A SAMPLE SCORED *PARTLY* REPORTS A BOUND, NOT A YIELD.** The plan's *"at most 2"* was read forward as *"about 2"* for a full session; it was the optimistic edge of ten rows, and the census over 69 is 0. Adjudicate the population before costing a remedy against it. **(2) MY OWN SWEEP REPRODUCED fork Learning #83 ON ITS FIRST RUN** — in the document written to adjudicate that very row. It counted **FM #27** (rows `#52`, `#53`), upstream's quoted *"learning #22 / #26a"* (`#54`) and rad-con's `#28/#29/#30/#34` (`#83`) as citations of this table — six false hits in four rows — **while simultaneously under-counting**, because it collected two of three regex groups and dropped every bare `#28`-style reference. Wrong in both directions at once. Resolve every hit to its referent; then re-read your regex's groups. **(3) THE LOCAL `.quality-gates-results.json` IS NOT A CURRENT READING.** It was S195's, head `431279b`, four sessions stale, with ten gates and a different manifest. Phase 0 permits reading it; here it would have compared a receipt's citation against a different tree. Re-run in a clone with HEAD asserted by sha. **(4) `context_budget.py` IS NOT WIRED TO ANYTHING THAT REFUSES.** Not in `.githooks/pre-commit`, not a gate. Its output is advisory, which is exactly how a no-growth pin was breached four times unnoticed (BL-78). **(5) `--cut N` RETAINS N.** Still the easiest thing here to get backwards. **(6) zsh ate a path:** `$c:starter-kit/...` silently dropped the `:s` as a history modifier and reported *"unknown revision"* for a commit that exists. Brace it: `${c}:path`.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `starter-kit/quality_ratchet.py --run` IN A `--no-local` CLONE WITH HEAD ASSERTED BY SHA.** **Citation, clone of `c2feca4` carrying this close-out's Phase 3C row: `quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results 10575dac7361 · manifest 01a4ae7aa511`** — identical to S199's and to this session's own Phase 0 run, because no gate was added or moved. In that clone `tests-sh-passed` read **343 / 0 failed at two receipts**, exactly on the floor, and `bin/check-learnings` read **70 rows, contiguous 15..84, 0 over 1,500 B**. Also green in the working tree: the shard's shipped `HANDOFFS-through-2026-09-20.md.verify.sh` **L1/L2/L3 OK twice** — before the fold (against HEAD and the working tree) and after it (against the trim commit `f1f51b3`); `docs/planning/BACKLOG-DETAIL.md.verify.sh` **C1–C5 OK** after both backlog edits; `bin/check-links` **111 links across 23 files**, twice. **NOT EXERCISED:** this close-out commit itself (BL-64), the review of either open PR, whether the gates are armed in any clone but this one (BL-77), and **anything that would have tested a retirement** — no row was moved, so D2's mechanism is still proven only by S199's E2 experiment, not by a real retirement.
changelog_ref: CHANGELOG.md "2026-09-20 · [BL-53] S200 close-out", plus the claim, the trim (written by the trimmer), the fold, the adjudication, P2's record, BL-78 and the Phase 3C entry
commit: fc2dac1 (claim) + f1f51b3 (retention trim) + 9d30247 (fold) + d4690d8 (the adjudication) + 53ba69e (P2 recorded, BL-78 raised) + c2feca4 (fork Learning #84) + this close-out
```

