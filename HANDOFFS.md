# Handoff Receipts — durable close-out proof

This repository dogfoods its own methodology: every session records a durable, machine-checkable
`handoff` receipt here at close-out (Phase 3D), and Phase 0 reconciles it against `git log`. See
[`starter-kit/HANDOFFS.md`](starter-kit/HANDOFFS.md) for the block format and the write points, and
`bin/check-handoff` for the checker. Newest on top; prepend-only.

**Retention policy — this ledger keeps FOUR receipts.** This file currently holds **4**; everything
older is archived under `docs/archive/` and indexed in the table below. **A steady state by design —
but NOT yet enforced by tooling, and that distinction is load-bearing.** Held at four it rests near
43 KB. **N=4 is an operator decision, never re-derivable from the 56,750 B detector floor**
(`srf-red-refusal-adjudication.md` §11.5 (5)). **`methodology_trim.py` fires on BYTES (196,608 B), never on a
record count**, so left alone this file climbs to ~205 KB over ~14 sessions — 3.6× the one-read
cap — before the tool says anything. **Until the trimmer learns a retention mode, this policy is applied by the
session that notices: at Phase 0 run `grep -c '^```handoff' HANDOFFS.md`; if it exceeds 4, trim to 4.** Adopted at **S127 (2026-08-30)** by operator decision; the warrant — including why a retention
cap is not the periodic reset H3's RED rule forbids — is
[`docs/archive/CHANGELOG-through-2026-09-02.md`](docs/archive/CHANGELOG-through-2026-09-02.md)`:2070`. `bin/check-handoff` validates its 13-key schema on the **newest** receipt, but
two of its other scopes traverse every receipt and `--all` checks all of them. `bin/model-report` globs the shards,
so its **default** run reaches archived prose; `--handoffs <shard>` narrows to one file.

**Two session sequences share this ledger and their numbers collide.** This fork and
`upstream/main` each run their own `S<N>` counter, so a receipt is identified by **session + date**,
never by number alone. **Every upstream receipt is now archived**; all four retained here are the
fork's. At a resync the two sequences stay separate and unrenumbered, each incoming receipt is
checked against ours before it is kept, and within a shared date the fork's precede the arriving
upstream ones (precedent: `fc4d297`).

> **The count above drifts between trims.** `methodology_trim.py` declares it a regenerated field
> (`starter-kit/methodology_trim.py`, the `HANDOFFS.md` `LedgerSpec`), so a **trim** rewrites it and
> the proof's L2 clause excuses that one span — but nothing updates it when a session **prepends** a
> receipt, which is most sessions. So it is right immediately after a trim and wrong from the next
> close-out onward. That is
> [Learning #12](starter-kit/FRAMEWORK_LEARNINGS.md) pointed at this file, and it is the receipt-ledger
> half of upstream [issue #65](https://github.com/KJ5HST/methodology/issues/65). Recount before
> trusting it.

> **⚠ THREE is the floor the retention policy sits one above.** `bin/tests.sh` Test 34 mutates *this*
> ledger to check `check-handoff --all`'s whole-ledger invariants, reading two anchors from the live
> file — not hardcoded, so it survives *which* receipts rotate, but it needs three to exist. A short
> ledger is **stated rather than silent** (BL-40 (b)): below the floor those six assertions print as
> `SKIP` rows naming themselves, the summary carries a skip count, and a ledger with *zero* receipts
> still FAILS — corruption is not rotation. **Nothing prevents a cut below three; the policy is what
> makes it not happen.** Re-run `bash bin/tests.sh` after any trim of this file.

**Archived shards — 19 trims, 152 receipts.** Every shard is `docs/archive/HANDOFFS-through-<date>.md`
and its proof is that same path plus `.verify.sh`; same format, same newest-on-top order, frozen at
write. **Run the proof rather than trusting this table** — each re-derives L1/L2/L3 from git, and that
instruction is why these rows exist.

| n | span | shard | by |
|--:|---|---|---|
| 16 | 2026-07-30 → 2026-08-02 | [`HANDOFFS-through-2026-08-02.md`](docs/archive/HANDOFFS-through-2026-08-02.md) | v1.1.1 |
| 30 | 2026-08-03 → 2026-08-09 | [`HANDOFFS-through-2026-08-09.md`](docs/archive/HANDOFFS-through-2026-08-09.md) | v1.1.1 |
| 25 | 2026-08-02 → 2026-08-11 | [`HANDOFFS-through-2026-08-11.md`](docs/archive/HANDOFFS-through-2026-08-11.md) | v1.1.3 |
| 8 | 2026-08-11 → 2026-08-15 | [`HANDOFFS-through-2026-08-15.md`](docs/archive/HANDOFFS-through-2026-08-15.md) | v1.2.0 |
| 4 | 2026-08-15 → 2026-08-17 | [`HANDOFFS-through-2026-08-17.md`](docs/archive/HANDOFFS-through-2026-08-17.md) | v1.2.0 |
| 3 | 2026-08-17 → 2026-08-18 | [`HANDOFFS-through-2026-08-18.md`](docs/archive/HANDOFFS-through-2026-08-18.md) | v1.3.0 |
| 3 | 2026-08-18 → 2026-08-23 | [`HANDOFFS-through-2026-08-23.md`](docs/archive/HANDOFFS-through-2026-08-23.md) | v1.3.0 |
| 3 | 2026-08-24 → 2026-08-24 | [`HANDOFFS-through-2026-08-24.md`](docs/archive/HANDOFFS-through-2026-08-24.md) | v1.3.0 |
| 2 | 2026-08-25 → 2026-08-25 | [`HANDOFFS-through-2026-08-25.md`](docs/archive/HANDOFFS-through-2026-08-25.md) | v1.3.0 |
| 17 | 2026-08-25 → 2026-08-29 | [`HANDOFFS-through-2026-08-29.md`](docs/archive/HANDOFFS-through-2026-08-29.md) | v1.5.0 |
| 5 | 2026-08-29 → 2026-08-30 | [`HANDOFFS-through-2026-08-30.md`](docs/archive/HANDOFFS-through-2026-08-30.md) | v1.5.0 |
| 23 | 2026-08-12 → 2026-09-04 | [`HANDOFFS-through-2026-09-04.md`](docs/archive/HANDOFFS-through-2026-09-04.md) | v1.5.0 |
| 2 | 2026-09-04 → 2026-09-07 | [`HANDOFFS-through-2026-09-07.md`](docs/archive/HANDOFFS-through-2026-09-07.md) | v1.5.0 |
| 2 | 2026-09-08 → 2026-09-08 | [`HANDOFFS-through-2026-09-08.md`](docs/archive/HANDOFFS-through-2026-09-08.md) | v1.5.0 |
| 2 | 2026-09-09 → 2026-09-09 | [`HANDOFFS-through-2026-09-09.md`](docs/archive/HANDOFFS-through-2026-09-09.md) | v1.5.0 |
| 1 | 2026-09-09 → 2026-09-09 | [`HANDOFFS-through-2026-09-09-2.md`](docs/archive/HANDOFFS-through-2026-09-09-2.md) | v1.5.0 |
| 2 | 2026-09-10 → 2026-09-10 | [`HANDOFFS-through-2026-09-10.md`](docs/archive/HANDOFFS-through-2026-09-10.md) | v1.5.0 |
| 2 | 2026-09-11 → 2026-09-11 | [`HANDOFFS-through-2026-09-11.md`](docs/archive/HANDOFFS-through-2026-09-11.md) | v1.5.0 |
| 2 | 2026-09-14 → 2026-09-15 | [`HANDOFFS-through-2026-09-15.md`](docs/archive/HANDOFFS-through-2026-09-15.md) | v1.5.0 |

<!-- NEXT TRIMMING SESSION: methodology_trim.py appends a 3-line pointer block here
     (starter-kit/methodology_trim.py:1093 build_pointer_block, :1103 insert_pointer). Fold it into
     the table above as one row (~125 B vs the block's ~448) and delete the block, IN ITS OWN
     COMMIT: inside the trim commit the shipped .verify.sh fails L2 (Learning #58). The generator
     is DISTRIBUTED, so teaching it this is an upstream change. -->

```handoff
session: S168
date: 2026-09-15
status: complete
self_score: 8
predecessor_score: 9
active_task: **BL-57'S P2 IS DONE ON BRANCH `bl57/changelog-rules`: `upstream/main` MERGED IN (`9e1dfeb`), THEN `f2bcc22` AND `775ba238` — NOT PUSHED.** §The Action Ledger's archive text is now *Reading and archiving* (Q2 A); the `HANDOFFS.md` seed names no size and defers to the trimmer's trigger; the trimmer's `:186` comment drops *"context-tax"*. P2's step 4, D8 (ii), needed no commit — #80's F3 did it. **Next: P3.**
what_was_done: **Fork `main`:** `5eef31f1` claim (with the Phase 0 `dashboard_history.jsonl` snapshot); `30a96bb9` the record (the plan's header and S168 amendment, BL-57's backlog row); this close-out. **Branch**, each commit with its own entry in the branch ledger: `9e1dfeb` merges `upstream/main` `8b4dc2c3`, clean, bringing `.githooks/commit-msg`; `f2bcc22` rewrites `FRAMEWORK_APPARATUS.md` :426–:498 — three partial reads, offset and limit past `READ_REFUSE_BYTES`, archiving optional, `--check` the only trigger, conservation, never in Phase 0 — and drops two *"verbatim"* self-descriptions P2 would falsify (28,022 → 25,983 B; its entry quotes each rule with its line, as P2's DONE asks); `775ba238` rewrites `starter-kit/HANDOFFS.md` :89–:152 (heading kept, D9; rule kept, D7; 11,505 → 10,417 B) and the trimmer comment (AST identical to `b82dcff`). Instruments checked before their numbers were used: §9.1 reproduced the plan's 1,577 lines on `b82dcff`; the new shard enumeration matched a Python count in bash and zsh with no shard (55) and eleven (526).
next_steps: **(1) BL-57'S P3 — ITS OWN SESSION** (`docs/planning/changelog-rules-contradictions-plan.md:490`): the source tags and the anchored, shard-spanning audit in §The Action Ledger; runner `:39` (net ≤ 0), `:278`, `:329`; `ITERATIVE_METHODOLOGY.md:294`; `.githooks/pre-commit:57` — `b82dcff`'s numbers, so re-derive on the branch — **plus the S168 amendment's item (1)**, the `HANDOFFS.md` seed's bare glob (`:117`), which zsh refuses where no shard exists. **(2) `HANDOFFS.md` HOLDS FIVE RECEIPTS**, so S169's Phase 0 trims to four. `SRF_RED` returns at 57,366 B and the file is 53,073 B after this close-out: 4,293 B for S169's claim stub (S168's was 2,050 B). Measure; if the stub would cross, trim before the claim (S161's follow-up precedent) or ask for `--force`. **(3) `CHANGELOG.md` IS 248,213 B, 13,931 B UNDER THE 262,144 B READ REFUSAL**; not trimming it is the operator's decision — raise it at Phase 0. **(4) CARRIED, EACH ITS OWN GO-AHEAD:** pushing the branch (to `origin`, as a backup) and fork `main` (8 ahead of `origin/main`); F5/F6 (`docs/planning/pr80-review-response.md:243`); the fork resync (4 conflicting files); BL-54; BL-36; BL-53; `choose_cut`.
key_files: Branch at `775ba238`: `FRAMEWORK_APPARATUS.md:426` (*Reading and archiving*), `:440`, `:476` (conservation), `:486`; `starter-kit/HANDOFFS.md:89` (heading, D9), `:91` (the rule), `:117` (the bare glob, P3); `starter-kit/methodology_trim.py:186`; the branch's `CHANGELOG.md:171` (P2's entries; P1's from `:211`). Fork: `docs/planning/changelog-rules-contradictions-plan.md:36` (S168 amendment), `:490` (P3), `:832` (§9.7); `docs/planning/BACKLOG.md:152`; `HANDOFFS.md:15`.
gotchas: **(1) THE BRANCH LEDGER'S TOP IS NOW `upstream/main`'S BLOCK** — a new branch entry goes above BL-57's (`CHANGELOG.md:171` there), below `main`'s. **(2) `git diff --quiet upstream/main <branch>` OVER THE PINNED FILES EXITS 1** — P1's `CLAUDE.md` row (−9 B), not a regression; attribute it before reading it. **(3) P3 EDITS THE RUNNER, WHICH HAS NO SPARE BYTES (K2)** — §9.7 at every boundary; no suite runs it. **(4) GATE EVERY BOUNDARY, NOT ONLY THE END:** a clean clone per commit plus a same-time control, rows compared; `bin/tests.sh` uses `mktemp`, so clones can run side by side. **(5) `git rev-parse --short a b` FAILS** — hit again at this Phase 0.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`,** in `--no-local` clones, exit codes read bare. **Branch:** 118 passed / 0 failed at `77b21a20` (control), `9e1dfeb`, `f2bcc22` and `775ba238`, 0 status flips, no row added or removed; unit suites 211 · 124 · 116 OK at each; `check-links` 107 links in 23 files; `check-learnings` 13 rows; `context_budget.py --status` 0 at each; §9.7 on `775ba238` *nothing over budget* (`CLAUDE.md` 59,159 of 59,168 B); P2's three DONE greps print nothing on `775ba238` and match on `9e1dfeb`. **Fork:** `bin/tests.sh` 305 passed / 0 failed / 0 skipped at the record `30a96bb9`, as at a same-time control at `d2347a16` — 0 status flips, 8 rows differing only in numbers this session moved (receipts, now 5; the `**Model:**` bullets, now 54, and the model-report totals, now 325; the ledger's size); unit suites 321 · 123 · 116 OK; `check-links` 105 links; `check-learnings` 64 rows; `context_budget.py --status` exits 2 at both, the runner over the 41,364 B ceiling its config declares over on arrival (2026-08-30) — by design, not S168's; `check-handoff --all --allow-pending` 0 after the record. **NOT EXERCISED:** any push; GitHub's rendering of the anchor; what *optional* does to ledger growth, which shows only across sessions.
changelog_ref: CHANGELOG.md "2026-09-15 · [BL-57] S168 close-out — BL-57's P2 done on a branch, not pushed; P3 next", plus the record and claim entries
commit: 5eef31f1 (claim) + 30a96bb9 (record) + this close-out; branch 9e1dfeb (merge) + f2bcc22 + 775ba238
```

**Self-assessment: 8/10.** Plus: P2 landed as scoped, with every DONE check run on the committed tree and every
boundary — the control, the merge, both steps — run through every gate in its own clean clone, rows compared,
0 flips. Each instrument was checked before its number was used (§9.1, the shard enumeration, the trimmer by
AST), and two things P2's line list missed were found by reading: the apparatus called the rewritten text
*verbatim* twice, and the seed's pointer described reasoning P2 removed. Minus: `git rev-parse --short a b`
at Phase 0 despite S167's gotcha; §9.1 ran mid-phase rather than at its start (still before the first P2
commit); the seed's matching glob is left to P3 — a scope judgment, not a fix. **Reduction:** none —
`HANDOFFS.md` goes to five receipts, which S169 trims; `CHANGELOG.md` stays untrimmed by the operator's
decision. **No learning row** (BL-53 leaves about three).

**Predecessor (S167): 9/10.** Item (1) was this session's plan exactly — merge first, re-run the suites and
§9.7, then P2 at `:440`, and amend D8 since F3 had done its (ii), which Phase 0 confirmed in one command.
Gotcha (1) is why §9.7 ran at every boundary; gotcha (4), *"re-check where the merged ledger puts them"*, was
the first check after the merge. Every number re-derived held. **Not 10:** the two *"verbatim"* sentences
S167 wrote into the apparatus were certain to go false at P2 and were not flagged. **ROI: strongly positive.**

```handoff
session: S167
date: 2026-09-15
status: complete
self_score: 7
predecessor_score: 9
active_task: **BL-57'S P1 IS DONE ON BRANCH `bl57/changelog-rules` — FOUR COMMITS FROM #80'S HEAD `aa36fd8b`, NOT PUSHED — AND THE MAINTAINER MERGED #80 MID-SESSION** (`4d9e2715`, 19:59 UTC; `upstream/main` `8b4dc2c3`). The seed's three `CHANGELOG.md` rule sections moved verbatim, one level down, to `FRAMEWORK_APPARATUS.md` §The Action Ledger; `starter-kit/CHANGELOG.md` is a 1,335 B pointer carrying `ledger-format: 2`; `bin/status` keys on that marker, and its advice no longer rewrites entries. Every P1 DONE check holds at the final commit `77b21a20`. BL-57's route, a new PR (D5), is open; **P2 starts by merging `upstream/main` into the branch.**
what_was_done: **Fork `main`: `6f9162f1` claim (with the Phase 0 `dashboard_history.jsonl` snapshot); `50498451` the `HANDOFFS.md` retention trim, 57,366 → 38,813 B, S163 + S162 to `docs/archive/HANDOFFS-through-2026-09-15.md`, no `--force` (SRF 0.8755 after the claim); `943059f5` the fold (19 trims, 152 receipts); `f63460e5` the record — the plan's header and S167 amendment, §9.4 corrected for zsh, BL-57's backlog row; this close-out. Branch, each commit with its own entry in the branch's ledger:** `eb06625b` the trimmer's three fence controls read `tools/fixtures/seed-CHANGELOG-ledger-format-1.md` (the pre-P1 seed, blob `47bc8485` asserted), and the dated-prose test's anchor becomes `---`, asserted once first; `b0634606` the move, the thin seed, the `HANDOFFS.md` seed's pointer, a comment-only trimmer edit (AST identical); `2d5dc6e9` `SEED_FORMAT_MARKERS` → `ledger-format: 2` and `Size, and when to archive`, the new advice in `bin/status` and `BOOTSTRAP.md:85`, Test 20 (b) with the marker and (b2) on the frozen seed; `77b21a20` `HOW_TO_USE.md:748`, `CLAUDE.md:21`, and `ITERATIVE_METHODOLOGY.md:556`, a third index the plan missed. **RED first:** the old trimmer tests fail 3 on the thin seed and a fourth passes vacuously (its anchor gone, hazard 5); (b2) fails on the title marker (116/2) and passes after (117/1); mutants of both new guards fail. **Step 4 first landed as `d4841721`, 116 B over upstream `CLAUDE.md`'s pinned 59,168 B ceiling, with every suite green** — only §9.7 saw it; amended to a row 9 B shorter than the original, unpushed. **#80's merge surfaced as Test 9 flipping to PASS**; a same-time control at `aa36fd8b` (116/0) showed it was upstream's.
next_steps: **(1) BL-57's P2 — ITS OWN SESSION** (`docs/planning/changelog-rules-contradictions-plan.md:440`). In `../methodology-bl57`, first merge `upstream/main` into the branch (`git merge-tree` clean at S167; it brings upstream's new `.githooks/commit-msg`, which the next commits must satisfy), and re-run every suite and §9.7 (`:816`) on the branch and on its merge; then P2's scope, and amend D8 (its (ii) was done inside #80 by F3). **(2) DUE NOW THAT #80 HAS MERGED — EACH ITS OWN GO-AHEAD; ASK, DON'T ACT:** F5 and F6 (`docs/planning/pr80-review-response.md:243`); the fork resync — fork `main` vs `upstream/main` conflicts in `.context-budget.json`, `CHANGELOG.md`, `HANDOFFS.md` and `starter-kit/FRAMEWORK_LEARNINGS.md` (the last a policy question: upstream ships rows 1–13). **(3) `HANDOFFS.md` HOLDS FOUR RECEIPTS** after this close-out: S168's Phase 0 finds four, no trim; its claim makes five, so S169's Phase 0 trims. **(4) `CHANGELOG.md` IS 243,849 B AFTER THIS CLOSE-OUT, 18,295 B UNDER THE 262,144 B READ REFUSAL**; S167 added 6,305 B. Not trimming it is the operator's decision (asked at S167's Phase 0; unchanged) — raise it, don't act. **(5) CARRIED:** pushing the branch (to `origin`, as a backup) and fork `main`; S161's (b)/(c), partly moot; BL-54; the two stale planning documents; `HOW_TO_USE.md:774`; BL-36; Test 31; BL-53; `choose_cut`; nine merged `origin` branches.
key_files: Branch at `77b21a20`: `FRAMEWORK_APPARATUS.md:338` (§The Action Ledger), `:9` (intro); `starter-kit/CHANGELOG.md:12` (the marker line); `bin/_manifest.py:87` (marker properties), `:105` (`SEED_FORMAT_MARKERS`); `bin/status:190` (advice); `bin/tests.sh:272` (Test 20 (b)), `:282` ((b2)); `tools/test_methodology_trim.py:62` (the fixture), `:252`, `:1844`, `:2058`; `starter-kit/methodology_trim.py:360`; the branch's `CHANGELOG.md:95`–`:145` (BL-57's four entries, above #80's). Fork `main`: `docs/planning/changelog-rules-contradictions-plan.md:21` (S167 amendment), `:440` (P2), `:787` (§9.4), `:816` (§9.7); `docs/planning/BACKLOG.md:152`; `HANDOFFS.md:15`.
gotchas: **(1) A GREEN SUITE CANNOT SEE A GATE IT NEVER RUNS** — no suite runs `context_budget.py --status` on the tree; run §9.7 at every boundary, and keep upstream `CLAUDE.md` edits net ≤ 0 (pinned at its size). **(2) THE ZSH `$c:` TRAP HID IN THE PLAN'S OWN §9.4** — it printed nothing until braced (now fixed); a check whose right answer includes a known hit must show it. **(3) UPSTREAM MOVED MID-SESSION** — a row that flips can be external; control it at the base, run at the same time. **(4) THE BRANCH'S LEDGER ENTRIES SIT ABOVE #80'S BLOCK AND BELOW `main`'S** (`CHANGELOG.md:95` there); after merging `upstream/main`, re-check where the merged ledger puts them. **(5) `bin/tests.sh` MUTATES BOTH LIVE LEDGERS** — clone only. **(6) `git rev-parse --short a b` FAILS** — hit again at this Phase 0.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`,** in `--no-local` clones, exit codes read bare. **Branch:** `aa36fd8b` 115/1 before #80's merge (Test 9) and 116/0 after, a same-time control; `eb06625b` and `b0634606` 115/1; `2d5dc6e9`, `d4841721` and `77b21a20` 118/0 — against the control, 1 row renamed, 3 added, 0 status flips; unit suites 211 · 124 · 116 OK (4 skipped); `check-links` 107 links (from 105); `check-learnings` 13 rows. `context_budget.py --status` exits 0 on `77b21a20` and on its merge into `upstream/main` (2 at `d4841721`). P1's DONE checks: §9.3 VERBATIM ×3; §9.4 (bash) only `b0634606` of nine versions; the seed 1,335 B, no `## `, `NO_RECORDS` exit 0, seeded by `bin/sync`; six adopter copies' `CHANGELOG.md` stale with the new advice, their `HANDOFFS.md` verdicts equal fork `main`'s. **Fork:** Phase 0 at `6142d538` 304/1/0 (Test 9); shard proof exit 0 at `50498451` and after the fold; `check-handoff --all` 0. **Close-out run**, on this content committed inside a clone before this sentence was written in: **305 / 0 / 0, exit 0** — Test 9 passes on fork `main` since #80's merge (a same-time control at `6142d538` also reads 305/0/0, where Phase 0 read 304/1/0); 0 status flips against that control, 11 rows differing only in numbers this session moved (receipts, now 4; the `**Model:**` bullets, now 53, and the model-report totals, now 324; the front matter, 6,855 B; the fixture's derived id, now S168; the ledger, then 45,609 B). **NOT EXERCISED:** any push; an adopter migration (P6–P11); GitHub's rendering of the anchor.
changelog_ref: CHANGELOG.md "2026-09-15 · [BL-57] S167 close-out — BL-57's P1 done on a branch, not pushed; PR #80 merged upstream; P2 next", plus the record, fold, trim and claim entries
commit: 6f9162f1 (claim) + 50498451 (trim) + 943059f5 (fold) + f63460e5 (record) + this close-out; branch eb06625b + b0634606 + 2d5dc6e9 + 77b21a20
```

**Self-assessment: 7/10.** Plus: P1 landed as the plan's four commits, each run through every suite in a clean
clone, and every DONE check was re-run on the final commit. RED came before GREEN for both behavioural
changes, and both new guards were mutation-tested. **The §9.7 budget check — run because the plan names it,
not because a suite asked — caught a real breach the suites could not see, before anything was published;
and a Test 9 flip was traced to upstream's merge with a same-time control rather than accepted.** Minus: **I
committed step 4 without running the budget gate** — K2 named the runner and `SAFEGUARDS.md`, and I did not
ask which other files the budget pins; the fix was an amend of an unpublished commit. The zsh `$c:` trap,
which my own notes name, made my Phase 0 marker check vacuous and my first post-commit run print nothing —
caught only because P1's commit had to appear. And `git rev-parse --short a b` again. Two small departures
from the plan (one fixture file rather than two literals; a third index updated) are recorded in the plan,
not asked. **Reduction:** `HANDOFFS.md` trimmed to four receipts; `CHANGELOG.md` not trimmed, by the
operator's decision. **No learning row:** it is in memory, and BL-53 leaves about three rows.

**Predecessor (S166): 9/10.** Its item (1) was exactly the Phase 0 check — the PR query, and the conditional
*"if #80 merged: measure Test 9 … (it should pass; don't assume)"*, which became this session's control run
when the merge arrived mid-session. Item (3) sent me to the plan at `:359`, exact; item (4)'s *"re-derive
the dry run after its claim (SRF against `d9ace03`)"* held, and no `--force` was needed. Gotcha (3), the
dashboard command, saved the search S166 had to make. **Not 10:** nothing warned that upstream `CLAUDE.md` is
pinned at its size — outside S166's own work, but P1's step 8 touches it; and gotcha (5) named the
`rev-parse` trap, which I then hit anyway. **ROI: strongly positive.**

```handoff
session: S166
date: 2026-09-15
status: complete
self_score: 8
predecessor_score: 9
active_task: **PR #80'S F2 AND F3 ARE PUBLISHED — PUSHED, DESCRIBED AND ANSWERED, ON THE OPERATOR'S "A B C" AT PHASE 0.** `KJ5HST/methodology:read-set-budgets` fast-forwarded `d4e1570..aa36fd8` (F2 `37740763`, F3 `aa36fd8b`); the description replaced from `docs/planning/pr80-body-after-f3.md`; the reply posted ([comment](https://github.com/KJ5HST/methodology/pull/80#issuecomment-5685701488)). #80 is OPEN, `MERGEABLE`/`CLEAN`, 3 comments, at `aa36fd8b`. The three findings the review asked for before the merge (F1–F3) are all answered upstream; F4 goes with F3; F5 and F6 can follow the merge. **The next move is the maintainer's.**
what_was_done: **Fork `main`: `32c90db4` claim (with the Phase 0 `dashboard_history.jsonl` snapshot); `6e109e45` the record — three action entries in `CHANGELOG.md`, and `docs/planning/pr80-review-response.md`'s header, §1 and §3 set to published, §3 noting the one lag; this close-out, which also sets §4's and §5's headings. Upstream, three outward actions, each read back through the API before the next:** (A) `git push upstream pr80/f3-read-set-token-ceilings:read-set-budgets`, run only inside a guard that re-checked #80's head (`d4e1570`), `upstream/main` (`9fa3141`) and 2 comments in the same command — `d4e1570..aa36fd8`; the remote ref and the API's branch head read `aa36fd8b`, and #80 did too on the second query (16 commits, `MERGEABLE`/`CLEAN`) — the first, seconds after the push, still read `d4e1570` and `UNKNOWN`, and B waited for it. (B) `gh api -X PATCH repos/KJ5HST/methodology/pulls/80 -F body=@docs/planning/pr80-body-after-f3.md`; the live body read back equal to the file byte for byte (10,151 B plus `--jq`'s newline). (C) `gh api repos/KJ5HST/methodology/issues/80/comments -F body=@docs/planning/pr80-reply-f2-f3.md` → comment `5685701488`, `rmsharp`, 18:21:28 UTC, equal to the file (4,871 B); 3 comments. **Phase 0 re-derived the preconditions rather than carrying them**, before offering the publish: the live description equal to `pr80-body-after-f1.md`, so the maintainer had not edited it; the push a fast-forward; `git merge-tree` against `upstream/main` clean; the diff size reproduced (+7,795 / −554 at `d4e1570`, +7,892 / −580 at `aa36fd8b`, 28 files). No trim: `HANDOFFS.md` held 4 receipts at Phase 0.
next_steps: **(1) THE MAINTAINER'S MOVE — WATCH #80; ANSWER NOTHING WITHOUT THE OPERATOR'S ASK.** At Phase 0: `gh pr view 80 --repo KJ5HST/methodology --json state,headRefOid,mergeStateStatus,comments` — OPEN at `aa36fd8b` with 3 comments unless he has acted. Bring any new comment to the operator; each reply, push or edit is its own go-ahead. If #80 merged: measure Test 9 on `upstream/main` (it should pass; don't assume), and reconcile fork `main` with `upstream/main`, which conflicts in both ledgers today (`git merge-tree --write-tree --name-only main upstream/main`). **(2) F5 AND F6** after the merge or as he asks (`docs/planning/pr80-review-response.md:243`): F5's stale citations at `aa36fd8b` are `starter-kit/methodology_trim.py:9` and `:155` (a design doc absent upstream) and `:33` (`--no-renames` in a hook that lacks it); F6 is one wording fix in the description. **(3) BL-57's P1** once #80's F-items settle, from #80's then-current head (`docs/planning/changelog-rules-contradictions-plan.md:359`); D8 (`:143`) is half done inside #80 by F3 — amend it at P2. **(4) `HANDOFFS.md` HOLDS FIVE RECEIPTS** after this close-out, so S167's Phase 0 trims to four (`HANDOFFS.md:15`); re-derive the dry run after its claim (SRF against `d9ace03`; `SRF_RED` only at 60,236 B). **(5) `CHANGELOG.md` NEARS THE 262,144 B READ REFUSAL** — 236,900 B after this close-out, 25,244 B under it; S161–S166 grew it 4.5–14.4 KB each, so it crosses in two to five sessions (an estimate). Not trimming it is the operator's 2026-09-14 decision — raise it at a Phase 0, don't act. **(6) FORK `main` IS PUSHED** — `755ef09..632f575` after this close-out, on the operator's go-ahead, then the commit recording it, so `origin/main` equals `main`. **CARRIED:** S161's merge-options (b)/(c); BL-54; the two stale planning documents; `HOW_TO_USE.md:774`; BL-36; Test 31; BL-53 (~3 rows); `choose_cut`; nine merged `origin` branches. Each push and deletion is its own go-ahead.
key_files: `docs/planning/pr80-review-response.md:1` (header, published), `:8` (the S166 paragraph), `:62` (§3, the recipe), `:80` (S166's run of it), `:243` (§6, F5 and F6); `docs/planning/pr80-body-after-f3.md:1` (the live description); `docs/planning/pr80-reply-f2-f3.md:1` (the posted reply); `CHANGELOG.md:213` (this close-out; the three action entries and the claim follow); `HANDOFFS.md:15` (the retention rule); `docs/planning/changelog-rules-contradictions-plan.md:359` (P1), `:143` (D8); at `aa36fd8b`, `starter-kit/methodology_trim.py:9`, `:33`, `:155` (F5); `starter-kit/methodology_dashboard.py:4342` (root resolution).
gotchas: **(1) A PR'S `headRefOid` LAGS A PUSH BY SECONDS** — `gh pr view` read `d4e1570` and `UNKNOWN` just after the push while `git ls-remote` and `gh api …/branches/read-set-budgets` were already current. Gate a step that names the new head on the PR's own read-back, re-queried. **(2) `HANDOFFS.md`'S RETENTION RULE COUNTS AT PHASE 0, BEFORE THE CLAIM** — S165's *"S166's claim makes five and its Phase 0 trims"* was off by one; compute the room (65,536 − size) against the largest recent record instead. **(3) THE DASHBOARD IS `python3 starter-kit/methodology_dashboard.py --no-open`**, run from the repo root (it resolves the root itself, `:4342`); it appends to the tracked `dashboard_history.jsonl`, which rides with the claim commit. No ledger entry records the command, so a grep for it finds nothing. **(4) THE REPLY WENT THROUGH `gh api …/issues/80/comments -F body=@…`**, which returns the id for the read-back; §3 still lists `gh pr comment`, not exercised here. **(5) `git rev-parse --short a b` FAILS** — I hit it at Phase 0 though S165's gotcha (7) names it. **(6) `bin/tests.sh` MUTATES BOTH LIVE LEDGERS** — clone only.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`,** in `--no-local` clones, exit codes read bare. Phase 0 at `5ce7bb2`: **304 / 1 / 0, exit 1** (Test 9, the GitHub-source dry run, pre-existing). **GitHub, the surface this session changed:** A, B and C each read back through the API as `what_was_done` records; #80 `MERGEABLE`/`CLEAN` at `aa36fd8b` after all three. `check-handoff --all --allow-pending` **0** after the claim. **Close-out run**, on this content committed inside a clone before this sentence was written in: **304 / 1 / 0, exit 1** — 305 rows, 0 status flips against Phase 0 (the counter proved on a planted flip first), 9 rows differing only in numbers this session moved (the `**Model:**` bullets, now 50, and the model-report totals, now 321, in five rows; receipts, now 5, in two; the fixture's derived id, now S167; the ledger, then 55,225 B). Dashboard 76/100 at Phase 0. **NOT EXERCISED:** the merge (the maintainer's), and with it Test 9's flip; CI (none).
changelog_ref: CHANGELOG.md "2026-09-15 · [ad hoc] S166 close-out — PR #80's F2 and F3 published (push, description, reply); the maintainer's move next", plus the three action entries and the S166 claim entry
commit: 32c90db4 (claim) + 6e109e45 (record) + this close-out
```

**Self-assessment: 8/10.** Plus: **the publish went out exactly as drafted because Phase 0 re-derived what it
depended on** — the live description compared to the f1 file (so the maintainer had not edited it), the
fast-forward, `merge-tree`, and the diff size reproduced on both heads — before offering it. **Each
outward action was gated mechanically:** the push ran only inside a guard that re-checked all three
preconditions in the same command, and B waited on A's read-back — which is what caught #80's head still
reading `d4e1570` seconds after the push, before a description naming `aa36fd8` went out. Every read-back
compared bytes, not a success line. **Minus:** at Phase 0 I hit `git rev-parse --short a b`, the trap
S165's gotcha (7) names; I spent three calls finding the dashboard command because my grep assumed a
phrasing no ledger entry uses; and my record commit left §4's and §5's headings saying *"not pushed"*,
caught only when I gathered line numbers for this receipt. **Reduction:** none — `HANDOFFS.md` goes to
five receipts (S167 trims), and `CHANGELOG.md` is not trimmed, by the operator's decision. **No learning
row:** the head lag belongs to *"a CLI's success line is not the remote's state"*; recorded in memory, and
BL-53 leaves about three rows.

**Predecessor (S165): 9/10.** Its item (1) was a publish recipe that needed no edit: the three
preconditions (`d4e1570`, `9fa3141`, 2 comments) held and became the push's guard verbatim; the anchor
`docs/planning/pr80-review-response.md:59` was exact; and the drafted description and reply went out
unchanged — every figure I re-derived reproduced (+7,892 / −580). Gotcha (6), the live body's trailing
newline, set B's read-back comparison; (7) named the `rev-parse` trap I then hit anyway. **Not 10:** item
(4)'s *"S166's claim makes five and its Phase 0 trims to four"* is off by one — the rule counts at Phase 0,
before the claim, and this session had 19,499 B of room; read literally, it would have spent a trim and
three commits on nothing. And the dashboard command is recorded nowhere a grep reaches. **ROI: strongly
positive** — the session was the recipe.

```handoff
session: S165
date: 2026-09-15
status: complete
self_score: 8
predecessor_score: 9
active_task: **PR #80'S REVIEW, F3, IS DONE ON A LOCAL BRANCH AND HELD WITH F2 — NOTHING PUSHED; THE PUBLISH IS THREE GO-AHEADS.** Branch `pr80/f3-read-set-token-ceilings` = F2's `37740763` + **`aa36fd8b`**: the branch's root `.context-budget.json` holds `SESSION_RUNNER.md` and `SAFEGUARDS.md` to the 25,000-token read cap at measured densities (19,200 + 5,800 tokens), declares no `read-set` class ceiling, and drops `CHANGELOG.md` and `HANDOFFS.md` to `_deliberate_exclusions` — the operator's **R1 L1**, chosen from nine variants measured on the branch and on its merge into `upstream/main`. `--status` exits 0 on both trees (it exited 2). Drafted: the description with every figure re-derived, and one reply for F2 + F3. Recorded in [`docs/planning/pr80-review-response.md`](docs/planning/pr80-review-response.md) §5; the publish recipe is §3.
what_was_done: **Fork `main`: `8e0a7a72` claim (with the Phase 0 `dashboard_history.jsonl` snapshot); `d9ace03` the `HANDOFFS.md` retention trim, 60,236 → 37,186 B, S161 + S160 to `docs/archive/HANDOFFS-through-2026-09-11.md`, no `--force` (SRF 0.9383 after the claim); `ef55d77` the fold (18 trims, 150 receipts); `95a4845` the record — the response plan's header, §1, §3 and §5, `docs/planning/pr80-f3-variants.py`, `docs/planning/pr80-body-after-f3.md`, `docs/planning/pr80-reply-f2-f3.md`; this close-out. Branch: `aa36fd8b` (`.context-budget.json` and the branch's `CHANGELOG.md:95`, above F2's entry, below `main`'s); the worktree `../methodology-pr80-f3` removed once clean, the branch kept.** The four `OVER` rows were split into two decisions, and every answer was built as a config and run — `--status` plus six staged `--precommit` commits — on both trees before any was offered; the saved harness reproduces every row. Two findings shaped the choice: the review's (ii) cannot work as written, because `token_ceiling()` clamps every whole-read file to 25,000 tokens; and the merge is 967 B larger than the branch (upstream S16's `SAFEGUARDS.md` paragraph), so the description's headline row was stale — the merged pair is 68,548 B / 24,278 tokens, not 67,581 / 23,902 — and `SAFEGUARDS.md` went over its pin on the merged tree. Every measurement method first reproduced the figure it replaces (the doubled pair's 47,805; `+7,795 / −554`; the corpora 658,788 and 838,416). The config was edited by a script that asserted every touched line and checked the result against `HEAD` key by key, and the edited file itself was re-run on both trees before the commit.
next_steps: **(1) PUBLISH F2 + F3 — THREE GO-AHEADS, IN §3'S ORDER** (`docs/planning/pr80-review-response.md:59`): re-fetch; #80's head must still be `d4e1570`, `main` `9fa3141`, 2 comments. Push `pr80/f3-read-set-token-ceilings:read-set-budgets` (a fast-forward), PATCH the description from `docs/planning/pr80-body-after-f3.md`, post `docs/planning/pr80-reply-f2-f3.md`, reading each back before the next. If anything moved, re-derive per §3 — the two `max_tokens` too if `main` touched the runner or `SAFEGUARDS.md`. **(2) F5 AND F6** after the merge (§6), or as the maintainer asks. **(3) BL-57's P1** after #80's F-items, from #80's then-current head; **D8 (ii) is now done inside #80** (`CHANGELOG.md` left upstream's root budget at `aa36fd8b`, and `HANDOFFS.md` with it, past D7) — amend the plan when P2 is planned. **(4) `HANDOFFS.md` HOLDS FOUR RECEIPTS** after this close-out; S166's claim makes five and its Phase 0 trims to four. The last trim's relief is 23,050 B, so `SRF_RED` returns only at 60,236 B — measure the room against the stub, as this session did. **(5) CARRIED:** pushing fork `main` (8 ahead of `origin/main` after this close-out); S161's merge-options (b)/(c); BL-54; the two stale planning documents; `HOW_TO_USE.md:774`; BL-36; Test 31; BL-53 (~3 rows); `choose_cut`; nine merged `origin` branches. Each push and deletion is its own go-ahead.
key_files: At `aa36fd8b`: `.context-budget.json:26` (the `read-set` class, no ceiling), `.context-budget.json:44` and `:46` (the runner's 19,200-token ceiling), `.context-budget.json:52` and `:54` (`SAFEGUARDS.md`'s 5,800-token pin), `.context-budget.json:72` (`_deliberate_exclusions`, the ledgers), `CHANGELOG.md:95` (the branch entry); `starter-kit/context_budget.py:112` (`token_ceiling`), `:139` (`framework_share`), `:166` (`class_ceiling`), `:1000` (`precommit`). Fork `main`: `docs/planning/pr80-review-response.md:59` (§3, the publish recipe), `:160` (§5, F3's record); `docs/planning/pr80-body-after-f3.md:17` (the headline row), `:37` (the config paragraph); `docs/planning/pr80-reply-f2-f3.md:1`; `docs/planning/pr80-f3-variants.py:132` (`VARIANTS`); `docs/planning/changelog-rules-contradictions-plan.md:143` (D8); `HANDOFFS.md:45` (18 trims, 150 receipts).
gotchas: **(1) "WITH THIS MERGE" IS A PROPERTY OF THE MERGE RESULT, NOT OF THE BRANCH** — `main` moved after the description was measured, and the merge takes its `SAFEGUARDS.md` (+967 B); measure such claims on `git merge-tree`'s tree or a merged clone. **(2) (ii) IS UNSATISFIABLE FOR A WHOLE-READ LEDGER** — `token_ceiling()` clamps to 25,000 tokens whatever `max_bytes` says; a ledger must leave the class or the budget. **(3) THE TOKEN CEILINGS ARE TYPED AGAINST 25,000 AND PINNED TO `main`'s `SAFEGUARDS.md` AT `9fa3141`** — they follow neither `read_cap_tokens` nor a later `main` edit; re-measure by the doubled-file method (a file under the cap needs more copies: `SAFEGUARDS.md` took seven). **(4) `open(p, "w").write(f(open(p).read()))` TRUNCATES BEFORE IT READS** — Python evaluates the receiver first; read, close, then write. **(5) macOS `sed -E` HAS NO `\s`** — a flip counter read 0 until a planted flip exposed it; plant a known change before trusting a zero. **(6) THE LIVE BODY IS `pr80-body-after-f1.md` PLUS ONE TRAILING NEWLINE** (verified); `pr80-body-after-f3.md` was built from the f1 file, not normalized. **(7) `git rev-parse --short a b` FAILS** — one revision per call.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`,** in `--no-local` clones, every exit code read bare. **Fork:** Phase 0 at `5235d4b` **304 / 1 / 0, exit 1** (Test 9, pre-existing); after the trim and fold, at `ef55d775`, **304 / 1 / 0, exit 1** — 305 rows, 0 status flips (the counter proved on a planted flip), 11 rows differing only in numbers the trim moved; the shard's `.verify.sh` exit 0 at `d9ace03` and after the fold; `check-handoff --all` 0. **Branch:** `37740763` (control) and `aa36fd8b` each **115 / 1, exit 1** — 116 rows, 0 status flips, 0 rows differing; unit suites 211 · 123 (2 skipped) · 116 (2 skipped) OK on both; `check-links` OK (105 / 23); `check-learnings` OK (13 rows). **The config itself:** `context_budget.py --status` **exit 0** on the branch and on its merge into `upstream/main` (it was 2); `--json` and `--selftest` exit 0; the six `--precommit` commits as recorded; `merge-tree` against `9fa3141` clean; the push a fast-forward. **Close-out run**, on this content committed inside a clone before this sentence was written in: **304 / 1 / 0, exit 1** — 305 rows, 0 status flips against Phase 0 and against the post-fold run (the counter proved on a planted flip first), 7 rows differing only in numbers this session moved (the `**Model:**` bullets, now 49; the fixture's derived id, now S166; the ledger, then 45,610 B; the model-report totals, now 320). Dashboard 76/100 at Phase 0. **NOT EXERCISED:** the budget gate wired as a hook (nothing wires it); GitHub (nothing published); CI (none).
changelog_ref: CHANGELOG.md "2026-09-15 · [ad hoc] S165 close-out — PR #80's F3 done on a local branch, held with F2 for one publish; three go-aheads next", plus the record, fold, trim and claim entries
commit: 8e0a7a72 (claim) + d9ace03 (trim) + ef55d77 (fold) + 95a4845 (record) + this close-out; branch aa36fd8b
```

**Self-assessment: 8/10.** Plus: **every answer was run before any was offered** — nine configs, both
trees, `--status` and six staged commits each — and that turned up the two findings that shaped the
choice: the maintainer's (ii) is unsatisfiable for a whole-read ledger, and the merge is 967 B larger than
the branch the description measured. **Every measurement method reproduced a recorded figure before its
new number was trusted** (the doubled pair's 47,805 exactly; `+7,795 / −554`; 658,788 and 838,416), and the
edited config was re-run from the file itself before the commit, then diffed row for row against a
same-session control. The trim needed no `--force`, as the Phase 0 measurement said. **Minus: four slips
in my own instruments**, each caught by my own checks before anything was committed or published — a
commit guard that compared a locale-sorted path list to a hand-ordered one (the trim waited a round); a
one-line read-modify-write that truncated a scratch config before reading it; a flip counter blind under
macOS `sed` until a planted flip exposed it; and a trailing-newline "normalization" that dropped a byte
of the published description. The saved harness's docstring also first omitted the ledger refusals in
two rows — caught by re-running the saved file against its own claims. **Reduction:** `HANDOFFS.md`
trimmed to four receipts; nothing else removed. **No learning row:** gotcha (1) is Learning #61's
*"re-derive at publish time"* with a sharper object — the merge result — and BL-53 leaves about three
rows; recorded in memory.

**Predecessor (S164): 9/10.** Its item (1) framed F3 exactly as this session had to take it — the
maintainer's three answers plus a fourth, *"explain in prose, take a letter"*, commit on `37740763`,
re-fetch first — and every anchor held (`docs/planning/pr80-review-response.md:145`; the branch's
`CHANGELOG.md:95`). Its gotchas paid off one by one: (2) the base commit; (3) the ledger placement; (4)
the live body's trailing newline, reproduced to the byte; (5) the `--no-local` clone without `upstream/*`
refs, which the merged clone needed; (6) the `gh api` PATCH, carried into §3. Its baselines reproduced
exactly (304/1/0; 115/1; 211 · 123 · 116). **Not 10:** §5's table measured one tree, the branch, so the
drift on the merge side was left to this session to find; and item (3) carried S163's *"`SRF_RED` will
refuse"* — correctly labelled an estimate — when S164's own close-out could have measured it (2,629 B of
room against a ~2 KB claim). **ROI: strongly positive.**

```handoff
session: S164
date: 2026-09-15
status: complete
self_score: 8
predecessor_score: 9
active_task: **PR #80'S REVIEW, F2, IS DONE ON A LOCAL BRANCH AND HELD — NOT PUSHED, SO F2 AND F3 GO UP IN ONE PUSH AND ONE REPLY.** Branch `pr80/f2-installed-source-guard` = #80's head `d4e1570` + one test-only commit, **`37740763`**: `test_a_synced_repo_with_each_installed_source_file_is_still_doc_only` writes every non-markdown file `bin/sync` installs, from its real `starter-kit/` source, into a doc-only fixture and asserts the exclusion holds, per file and all together. RED first on the review's own mutant (old suite 211 OK; new test `2181 != 0` source LOC). Recorded in [`docs/planning/pr80-review-response.md`](docs/planning/pr80-review-response.md) §4. **F3 is next and starts with an operator decision (§5).**
what_was_done: **Fork `main`: `8791a272` claim (with the Phase 0 `dashboard_history.jsonl` snapshot); `95d84cfd` the response plan's §4 and corrected header, `docs/planning/pr80-f2-mutants.py`, the preparation entry; this close-out. Branch: `37740763`, its entry in the branch's own ledger (`CHANGELOG.md:95` there), above F1's and below `main`'s; `git merge-tree` against `9fa3141` clean, and the push would fast-forward `read-set-budgets`.** The test is generalized in place, not added beside the old one. Its names come from `bin/_manifest.py`, not `FRAMEWORK_INSTALLED_SOURCE`, so a fifth name is covered without anyone adding it; a last assertion checks it covered exactly the scanner's list. `.context-budget.json` is covered, not excluded: it is `config` before the predicate runs, so a direct `is_framework_installed` call holds its signatures and its category is asserted. **Six mutants, both twins, old and new suites, run twice:** M1 (the review's), M4 (the `.json` signatures) and M6 (the one `collect_all` call site narrowed) pass the old suite and fail the new test; M2 and M5 were caught already and still are. **M3 — the scanner's own entry — is not caught by this test:** the neutralized strings land in the scanner's own signature table, so the real file matches itself; twelve stand-in tests catch it, and the docstring says so. The saved mutants script was proved to plant byte-identical mutants to the one the round ran. The worktree `../methodology-pr80-f2` was removed once clean; the branch stays.
next_steps: **(1) F3 — ITS OWN SESSION, STARTING WITH AN OPERATOR DECISION** (`docs/planning/pr80-review-response.md:145`): the maintainer's three answers — the read-set ceiling in tokens at measured density; ledger ceilings where the ledgers are; *"over at install, by design"* — plus a fourth, dropping the ledgers from the read budget as this fork did at `3c8acd5`. Explain in prose, take a letter. **Commit F3 on top of `37740763`** (branch `pr80/f2-installed-source-guard`), not on `d4e1570`. **Re-fetch first and read any new comment on #80**; if its head moved, rebase both. **(2) THEN PUBLISH F2 + F3 TOGETHER — three go-aheads, in §3's order:** push (a fast-forward), the description (F2 moves no figure in it; F3 may), one reply covering both (§4's mutant table is F2's paragraph). **(3) `HANDOFFS.md` HOLDS FIVE RECEIPTS** after this close-out, so S165's Phase 0 trims to four; S163 estimated `SRF_RED` will refuse, and any `--force` is its own ask — re-derive after the claim. **(4) BL-57's P1** after F3, from #80's then-current head. **(5) CARRIED:** S161's merge-options (b)/(c); BL-54; the two stale planning documents; `HOW_TO_USE.md:774`; BL-36; Test 31; BL-53 (~3 rows); `choose_cut`; nine merged `origin` branches; pushing fork `main` (3 ahead of `origin/main` after this close-out). Each deletion and the push is its own go-ahead. **(6) F5, F6 and the Markdown-only citation sweep** can follow the merge.
key_files: At `37740763`: `tools/test_methodology_dashboard.py:2666` (the generalized test), `tools/test_methodology_dashboard.py:2642` (the name-vs-signature gate), `tools/test_methodology_dashboard.py:2653` (`context_budget.py`'s real-artifact guard), `CHANGELOG.md:95` (the branch entry); the unchanged scanner: `starter-kit/methodology_dashboard.py:360` (`FRAMEWORK_INSTALLED_SOURCE`), `:468` (`_FRAMEWORK_FILE_SIGNATURES`), `:484` (`methodology_trim.py`), `:508` (`.context-budget.json`), `:873` (the one call site). Fork `main`: `docs/planning/pr80-review-response.md:81` (§4, F2's record), `:145` (§5, F3's decision), `:58` (§3, the publish order); `docs/planning/pr80-f2-mutants.py:1` (the six mutants and the commands); `HANDOFFS.md:45` (17 trims, 148 receipts).
gotchas: **(1) A REAL-ARTIFACT FIXTURE CANNOT FAIL A MUTATION OF A DETECTOR THE ARTIFACT CARRIES** — neutralizing `methodology_dashboard.py`'s signatures writes the new strings into its own table, so the real file still matches (M3). My first docstring claimed otherwise, written before M3 ran; the round caught it. Say which mutants a test kills only after running them. **(2) F3 BUILDS ON `37740763`**, not `d4e1570`, or the branches diverge and the push stops being a fast-forward; `pr80/f1-learnings-1-13` still equals `upstream/read-set-budgets` (`d4e1570`). **(3) BRANCH LEDGER ENTRIES GO WITH #80'S BLOCK — ABOVE F2'S AT `:95`, BELOW `main`'S**; the branch's hook refuses a commit without `CHANGELOG.md`. **(4) THE LIVE PR BODY DIFFERS FROM `docs/planning/pr80-body-after-f1.md` BY ONE TRAILING NEWLINE** that `gh api --jq` adds — compare after stripping it, not with `cmp`. **(5) A `--no-local` CLONE LACKS `upstream/*` REFS** — clone with `-b <local branch>` and check `HEAD` before running anything. **(6) `gh pr edit` FAILS** — use `gh api -X PATCH`.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`,** in `--no-local` clones, every exit code read bare. **Branch:** `d4e1570` (control) and `37740763` each **115 passed / 1 failed, exit 1** — 116 rows, 0 status flips, 0 rows differing (Test 9, pre-existing); unit suites 211 · 123 (2 skipped) · 116 (2 skipped) OK on both; `check-links` OK (105 / 23) and `check-learnings` OK (13 rows) on both. Mutation round: 14 runs, twice, identical. **Fork:** Phase 0 at `755ef09` **304 / 1 / 0, exit 1**; `check-handoff --all --allow-pending` **0** after the claim; at the record commit `95d84cfd`, **304 / 1 / 0, exit 1** — 305 rows, 0 status flips, 3 rows differing only in numbers this session moved (receipts 4 → 5, the ledger's bytes). **Close-out run**, on this content committed inside a clone before the run results were written in and two citations corrected (`:144` → `:145`): **304 / 1 / 0, exit 1** — 305 rows, 0 status flips against Phase 0, 9 rows differing only in numbers this session moved (the live `**Model:**` bullets, now 46; receipts, now 5; the fixture's derived id, now S165; the ledger, then 58,238 B; the model-report totals, now 317). **NOT EXERCISED:** a real `bin/sync` into a real adopter (the test writes the installed files itself; the scanner reads only files); CI (none); GitHub (nothing published).
changelog_ref: CHANGELOG.md "2026-09-15 · [ad hoc] S164 close-out — PR #80's F2 done on a local branch and held for one push with F3; F3 next", plus the preparation entry and the S164 claim entry
commit: 8791a272 (claim) + 95d84cfd (record) + this close-out; branch 37740763
```

**Self-assessment: 8/10.** Plus: **the review's claim was reproduced before anything was trusted** — the
old suite stays 211 OK under the maintainer's mutant — and the new test fails it with his symptom,
`2181 != 0` source LOC. **The test takes its names from the manifest**, the class's own convention for
fixtures, which answered the *"cannot enforce"* S163 left in §4 instead of carrying it forward. **Each
half of the test was shown live on its own:** M4 kills only the direct call, M6 only the end-to-end
half. The round ran twice, every mutant was asserted to apply once per file, the saved script was proved
to plant the same mutants, and the branch commit was diffed row for row against a same-session control.
The publish was held, not asked for, as Phase 0 suggested. **Minus: my first docstring claimed RED
against the neutralization of *every* name before M3 had run** — a forward claim from expectation,
caught only by my own round; the scanner carries its own signature table, which I had read this session
and not connected. The response plan still said nothing had been pushed, a staleness I found only when I
edited it. **Reduction:** none — `HANDOFFS.md` goes to five receipts (S165's Phase 0 trims), and
`CHANGELOG.md` is not trimmed, by the operator's decision. **No learning row:** M3 belongs to Learning
#12's *"ask what a fixture makes unreachable"*, and BL-53 leaves about three rows; recorded in memory.

**Predecessor (S163): 9/10.** Its item (1) put this session straight into execution: every anchor held
at `d4e1570` — `tools/test_methodology_dashboard.py:2666`, `:2642`, `:2653`;
`starter-kit/methodology_dashboard.py:360`, `:468`, `:484`, `:508` — and §4's recipe (*"plant the mutant
… in a clone, show the current suite stays green and the new parametrized test goes red"*) is what I
ran. Its question on `.context-budget.json` was the right one, and its *"cannot enforce"* line named the
gap the manifest-driven design closes. Gotcha (4) placed the branch entry first time, and the baselines
it recorded (115/1; 211 · 123 · 116, 4 skipped; 105 links) reproduced exactly at `d4e1570`. **Not 10,
for two stale statements:** the response plan's header still read *"Nothing below has been pushed,
edited on the PR, or posted"* after S163 had done all three, and its receipt still carried *"pushing fork
`main`"*, which its own follow-up discharged. Neither cost more than a minute. **ROI: strongly
positive.**

