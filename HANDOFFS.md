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

```handoff
session: S186
date: 2026-09-17
status: pending
self_score: pending
predecessor_score: pending
active_task: **THE OWED `HANDOFFS.md` RETENTION TRIM, AND THE OPERATOR'S ANSWER TO BL-57 PLAN ITEM (21) RECORDED FOR P8–P11.** S185's close-out left 3 receipts; this claim makes 4, so the trim is `--cut 2 --force` (S181/S183 precedent), then the pointer block folded into `docs/HANDOFFS_ARCHIVE_INDEX.md` in its own commit. Item (21) (`docs/planning/changelog-rules-contradictions-plan.md:239`): the operator chose *carry it in P8–P11* — each adopter phase also refreshes the `HANDOFFS.md` seed where `bin/status` reads it *(stale format)*. Chosen by the operator after Phase 0 (picker), which also gave the go-ahead to push fork `main` to `origin` after close-out. P8 itself runs from `~/Development/vscode_quarto_ext` as its own session. Nothing upstream.
what_was_done: pending
next_steps: pending
key_files: `HANDOFFS.md:48` (the fold comment), `docs/HANDOFFS_ARCHIVE_INDEX.md` (the shard index and its fold rule), `starter-kit/methodology_trim.py`; `docs/planning/changelog-rules-contradictions-plan.md:7` (status line), `:239` (item (21)), `:808` (the P6–P11 procedure), `:843` (the P8 row)
gotchas: pending
runtime_smoke: pending
changelog_ref: CHANGELOG.md "2026-09-17 · [BL-57] S186 claim"
commit: pending
```

```handoff
session: S185
date: 2026-09-17
status: complete
self_score: 8
predecessor_score: 8
active_task: **BL-57's P7 (`wsfct`) IS RECORDED HERE (`313459c`) AND BL-67 IS CLOSED (`aee4771`). THE RECORDING WAS RE-VERIFIED FROM `wsfct`'s GIT OBJECTS, NOT RE-APPLIED FROM THE REVERTED `a6320ae`, AND ONE OF ITS CITATIONS TURNED OUT TO HAVE BEEN FALSE WHEN IT WAS WRITTEN.** It named `origin/chore/s630-methodology-bl57-p7` as where the six commits survive. GitHub deleted that branch at 00:36:55Z, two seconds after PR #903 merged and eight minutes before `a6320ae` was committed; what resolved was `wsfct`'s local remote-tracking ref. The commits live at `refs/pull/903/head` (`3a257097`), and plan item (20) now says to cite that ref (fork Learning #77). Chosen by the operator after Phase 0 (picker). Nothing sent upstream, nothing written in `wsfct`. **Next: P8 (`vscode_quarto_ext`), run from that project as its own session.**
what_was_done: **Phase 0:** `CHANGELOG.md` frontier `19eb19b` = HEAD, no gap; `HANDOFFS.md` frontier `61eb9ab`, one behind, and that commit (BL-67 raised) carries its own ledger entry and no receipt by design — nothing backfilled. 2 receipts, no trim owed. Gate in a `--no-local` clone of `19eb19b`: `10/10 pass · results 8e12f40caec1`, the digest S183 cited. Dashboard 76/100, no high flags. Numbered S185 because the reverted claim used S184. **`4cb67c6`** claim, carrying Phase 0's two tracked rows. **Re-verification**, `wsfct` `git status --porcelain` empty before and after, reading git objects only: six commits `790c77d1`..`3a257097`; PR #903 `MERGED` 2026-09-18T00:36:53Z as `66e14daa`, parent `55c293f7`; `git diff 3a257097 66e14daa` empty; `8a41741c` holds 15 files, its `CHANGELOG.md` change only its 7-line entry; the plan's own §9.8 script on `12fb758e` prints *only the block changed* for 8–182 and names `(8, 1), (10, 172)` for the row's 13–196; the block holds 5 `### ` lines and 3 audit matches, and the commit adds 1; headings 75 → 71; audit 72 → 70 live and 132 → 130 with the three shards; `bin/status ../wsfct` `present`, every tracked file `current`; `bin/sync --dry-run` exit 0, 23 unchanged; the six adopters' seed verdicts identical to S184's. **Added from S630's receipt and checked here:** the row's 13–196 would have deleted three archive-pointer blocks (item (19)); `wsfct`'s three shard proofs fail — all v1.1.2-generated, L1/L3 record counts 12/8, 37/35, 29/28, identical at `55c293f7` before P7 and `66e14daa` after — BL-36's class, noted in the P7 block, no new item. **`313459c`** the recording: status line, the P7 block, the P7 row with its range struck, the procedure's stale `130 → 127` struck for `132 → 130`, the BL-57 row naming P8. **`aee4771`** BL-67 closed: row to §Completed items, closing note in `BACKLOG-DETAIL.md`. **This close-out:** item (20)'s wording corrected (it said *"by S185 GitHub had deleted it"*, as if it went stale; the PR's event timeline says it was never true), fork Learning #77, this receipt, the ledger entry.
next_steps: **(1) P8 — `vscode_quarto_ext`, from that project, as its own session** (plan `docs/planning/changelog-rules-contradictions-plan.md:843`, procedure `:808`, §9.8 `:1058`). Measured read-only at this close-out, labelled as readings with a time on them (fork Learning #74): on `master` `58f7bcbd`; `git status --porcelain` shows only an untracked `scratchpad/`, no staged claim; it has no merged PRs, so it commits straight to `master` and item (20) does not apply unless that changes; `bin/sync ../vscode_quarto_ext --source=local --dry-run` exits 0 and would write 14 files; `CHANGELOG.md` has the Keep-a-Changelog header at :1–8 (through `## [Unreleased]`), a v1.1.1 trimmer pointer block at :10–12, and 21 `### ` lines; `.context-budget.json:49` lists `CHANGELOG.md` (the row says drop it, Q2 A, the project's call). **Re-derive the block by content at the claim** (item (19)); re-run `git status --porcelain` there first. **(2) THE NEXT PHASE 0 OWES A `HANDOFFS.md` TRIM:** this close-out leaves 3 receipts (S185, S183, S182). **(3) ITEM (21) IS THE OPERATOR'S CALL:** the `HANDOFFS.md` seed that P6/P7 leave *(stale format)* and no item owns — carry it in P8–P11, raise it as its own item, or leave it. **(4) OUTWARD, EACH ITS OWN GO-AHEAD:** fork `main` is 13 commits ahead of `origin` before this close-out — 15 once it and its post-close-out gate record land — unpushed; BL-66's upstream PR; P12 (BL-62, BL-63, #80's F5). **(5) SMALL AND FOUND, NOT FIXED:** `docs/planning/BACKLOG.md:9`–`11`'s hand-maintained open list omits BL-63, whose row is at `:156`; `bin/tests.sh:2752`'s six stale line numbers (carried from S183). **CARRIED:** BL-61 (scheduled small session), BL-60 (folds BL-36), BL-65, BL-54's PR, `README.md`'s stale cost section (plan item (15)); the runner and `SAFEGUARDS.md` stay `over` budget.
key_files: `docs/planning/changelog-rules-contradictions-plan.md:7` (status line), `:212` (the P7 block), `:226` (19), `:231` (20, corrected at this close-out), `:239` (21), `:247` (the BL-36-class note), `:831` (the struck `130 → 127`), `:842` (the P7 row), `:843` (the P8 row), `:808` (the P6–P11 procedure), `:1058` (§9.8); `docs/planning/BACKLOG.md:151` (BL-57), `:166` (BL-67, completed); `docs/planning/BACKLOG-DETAIL.md:2347` (BL-67's closing note); `docs/FORK_LEARNINGS.md:89` (#77); in `~/Development/wsfct`: `66e14daa` (the squash on `master`), `refs/pull/903/head` = `3a257097` (the six commits), `12fb758e` (the header migration)
gotchas: **(1) ASK THE REMOTE, NOT A LOCAL REF.** In `wsfct`, `git branch -a` still lists `remotes/origin/chore/s630-methodology-bl57-p7` and `git rev-parse` resolves it; `git ls-remote origin` and GitHub say the branch does not exist. `wsfct` has `delete_branch_on_merge` on; `vscode_quarto_ext` has it off. **(2) THE PLAN'S LINE NUMBERS MOVED:** +2 above the P7 block (the status line grew; the P6 block `:175` → `:177`) and +43 below it (the P7 row `:799` → `:842`, §9.8 `:1015` → `:1058`); S183's handoff and the pre-S185 receipts cite the old ones. **(3) THE AUDIT HAS TWO FORMS** — the live file alone (72 → 70) and live plus shards (§9.2's form, 132 → 130); the procedure's figure is the second. Name the form beside the number. **(4) 3 RECEIPTS NOW, SO `tests-sh-passed` READS 315, NOT 309** — six stated skips become assertions at three receipts; never tighten the floor (305) from this reading. **(5) `vscode_quarto_ext`'s SHARD PROOF WAS WRITTEN BY TRIMMER v1.1.1**, older than `wsfct`'s — an estimate, not run: expect it to fail as BL-36's class, and check it before P8 rather than attribute it to P8. **(6) PHASE 0 WRITES TWO TRACKED ROWS** (`.context-budget-history.jsonl`, `dashboard_history.jsonl`); they rode `4cb67c6`.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `quality_ratchet.py --run` (which runs `bash bin/tests.sh`) IN A `--no-local` CLONE WITH HEAD ASSERTED.** **Citation, clone of `aee4771`: `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results 4433567c1f55 · manifest 3a87b16f1b31`**, `tests-sh-passed` 315 at 3 receipts. The close-out commit is not covered by that run (BL-64), so it is re-measured in a clone of itself after it lands and recorded as its own ledger entry, as S183 did. On the live tree: `bin/check-links` 0 (110 links, 23 files) after each commit; `BACKLOG-DETAIL.md.verify.sh` 0 after the append; `bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations` 0 with row 77; `bin/check-handoff --allow-pending` 0 on the claim. In `wsfct`, read-only: the §9.8 script, `bin/status`, the sync dry run and the three shard proofs (these in a `--no-local` clone, at two commits). **NOT EXERCISED:** `wsfct`'s own build (the DONE item rests on S630's receipt: no `web/` code touched); any adopter write; any upstream action; CI (none).
changelog_ref: CHANGELOG.md "2026-09-17 · [BL-67] S185 close-out", plus the claim, the P7 recording and the BL-67 closure entries
commit: 4cb67c6 (claim) + 313459c (P7 recorded) + aee4771 (BL-67 closed) + this close-out
```

**Self-assessment: 8/10.** Plus: I treated the reverted recording as a list of claims to re-check rather than a patch
to re-apply, and re-ran every one from `wsfct`'s git objects with its tree clean before and after — including the
plan's own §9.8 script, run verbatim with only the revision pair substituted, on both ranges, so the row's 13–196 is
shown to fail rather than asserted to. The one claim that did not hold was found by asking the remote instead of
re-reading the same local ref, and then pinned with the PR's event timeline, which turned *"stale"* into *"never
true"*. The audit is stated in both of its forms, and the procedure's stale figure is struck beside the measured one.
S630's report of failing shard proofs was re-run at two commits and matched to BL-36 after searching the backlog,
instead of being raised as a new item. **Minus:** I first called the branch citation *stale* — to the operator
mid-session and in `313459c`'s item (20) (*"by S185 GitHub had deleted it"*) — before looking at when the deletion
happened. That is a derived claim about time published as a measured one, in the exact shape Learning #77 now
names; the close-out commit corrects the plan, and the `313459c` ledger entry stands as written. I also found
`BACKLOG.md`'s open list missing BL-63 while editing that very line and left it, correctly for scope, but it is
one more hand-maintained list known to be wrong. **Growth:** four ledger entries plus this one, the P7 block
(~40 lines), a detail note, a learnings row (+1,158 B). **Reduction:** none this session, stated rather than left
unsaid; the trim this close-out makes owed falls to the next Phase 0.

**Predecessor (S183): 8/10.** Its item (1) named exactly this task, with the plan's P6 block (`:175`) and P7 row
(`:799`) and the BL-57 row (`BACKLOG.md:151`) — all three resolved at my Phase 0 tree — and it said the DONE checks
*"still want running from here"*, which is the instruction that caught the one false claim. Its gotchas (3), (6) and
(7) were right: no trim owed, the two tracked Phase 0 rows, suites one at a time. Its gotcha (2) predicted the
`tests-sh-passed` jump to 315 at three receipts exactly. Its six commit hashes and the 15-file count for `8a41741c`
all held. **Not 9:** it described `wsfct` as *"not merged"*, which was already false a few hours later. It did
say that state was a reading from its own Phase 0, and fork Learning #74 anticipates this, so it was not careless.
But its `key_files` for the item were all on this side, with no `wsfct` ref named to re-check.
BL-67's body, written after S183's close-out, added the verification commands with their expected readings and the
instruction to re-verify rather than trust; every reading held except the one inherited from `a6320ae`.
**ROI: strongly positive** — no time spent rediscovering the task's shape.

```handoff
session: S183
date: 2026-09-17
status: complete
self_score: 8
predecessor_score: 7
active_task: **`bin/tests.sh` TEST 38'S PLANT-LANDING CHECK NOW ASKS ABOUT POSITION, NOT ABOUT TEXT (`1cb4e44`), AND THE QUALITY GATE IS GREEN AGAIN ON `main`: `10/10 pass · 0 fail · 0 unmeasured · results 8e12f40caec1 · manifest 3a87b16f1b31` in a `--no-local` clone.** The planter decided which side of a record's closing fence its plant had landed on by searching that record for the planted name; S182's receipt quoted this guard's own failure line — `phantom_drift` and all — so every plant below the fence reported itself as inside and assertion (8b) refused to run. Chosen by the operator after Phase 0 (picker), which also authorized the `HANDOFFS.md` retention trim as its own action. Nothing sent upstream. **P7 (`wsfct`) is still owed a recording here: it is item (1) below, unchanged from S182's handoff and verified read-only from here at this Phase 0.**
what_was_done: **Phase 0:** `CHANGELOG.md` frontier `5ae7902` = HEAD, no gap; `HANDOFFS.md` frontier `93656a1`, one commit behind and that commit is S182's authorized push record, so nothing backfilled. 3 receipts, so a trim was owed. **S182's gate citation did NOT re-run:** `9/10 pass · 1 fail · results aff8a2e08e15 · manifest 3a87b16f1b31` in a `--no-local` clone of `5ae7902`, against its cited `10/10 pass · results 83c5e3fed6f3` at `b25fc19`. Same manifest digest, so no threshold moved. The one failing assertion was Test 38 (8b), pinned before anything was touched by replaying the planter through `bin/check-handoff`'s `scan()` against `git show <rev>:HANDOFFS.md`: pass at `b25fc19`, fail at `93656a1` and at `5ae7902` — the flip is S182's own close-out commit. Dashboard 76/100, medium risk, 0 high-or-above flags. **`f85dc75`** claim, carrying Phase 0's two tracked rows. **`128efa4`** retention trim, `--cut 2 --force`: S181 and S180 to `docs/archive/HANDOFFS-through-2026-09-17-2.md` — the `-2` because S181's trim took today's plain name — 34,289 → 17,712 B, its proof exiting 0 before the commit. **`94031ed`** the fold into `docs/HANDOFFS_ARCHIVE_INDEX.md`, 17,712 → 17,256 B. **`1cb4e44`** the fix: the landing check now asks whether the index the plant was inserted at falls inside the newest record's extent, which `scan()` already returns, and its failure message names the planted line and the span. Two assertions added, (8d)/(8e), planting into a doctored copy of `tools/fixtures/handoff-ledger-2-records.md` whose newest record quotes the marker in `what_was_done` — the exact shape S182's receipt has — so the case cannot be cleared by rotating a receipt. Written RED first and RUN red in their final home: `307 passed, 2 failed, 6 skipped` with the substring form, `309 passed, 0 failed, 6 skipped` with the positional one. **This close-out:** the comment claiming (8b) did not depend on the live ledger is struck, because it plants into it; fork Learning #76; this receipt; the ledger entry.
next_steps: **(1) RECORD P7 HERE**, as S180 recorded P6 (plan `docs/planning/changelog-rules-contradictions-plan.md:799`, the P6 block at `:175` as the model, `docs/planning/BACKLOG.md:151` for the BL-57 row). Verified read-only at this Phase 0, so it does not need re-deriving from scratch: `~/Development/wsfct` is on branch `chore/s630-methodology-bl57-p7`, tree clean, in sync with its own `origin`, not merged; six commits `790c77d1`..`3a257097`; the sync commit `8a41741c` holds 15 files — the 14 framework files its dry run listed plus its own ledger entry — which is plan item (18) applied exactly. Its own DONE checks (`bin/status` reads `present`, only the recorded block changed, the heading and audit counts moved as predicted) still want running from here. **(2) THEN P8, `vscode_quarto_ext`** (plan `:800`), run from that project as its own session; re-derive its line numbers at the claim. **(3) BL-66 STILL WANTS AN UPSTREAM PR AND IS THE FIRST THING A NEW ADOPTER READS** — outward, so its own go-ahead. **(4) BL-61** is the scheduled small session (`bin/check-handoff:663`). **(5) SMALL AND FOUND, NOT FIXED:** `bin/tests.sh:2752` lists six line numbers as carrying the `producer | grep -q` form; all six were already stale at `94031ed` (2591 is `else`, 2596 a comment, 2620 an assert), and this session's insertions moved them again. Re-derive them or drop the numbers. **CARRIED:** BL-61; BL-60 (folds BL-36); BL-62, BL-63 and #80's F5 ride P12; BL-54's PR; `README.md`'s stale cost section (plan item (15)); the runner and `SAFEGUARDS.md` stay `over` budget.
key_files: `bin/tests.sh:2546` (the insertion index, now named), `:2558` (the landing check), `:2567` (`plant38`, which gained an optional source), `:2496` (the struck claim), `:2596` ((8d)), `:2628` ((8e)), `:2752` (the six stale citations); `bin/check-handoff:227` (`scan`, whose `line` and `content` give the extent); `tools/fixtures/handoff-ledger-2-records.md:17` (the `what_was_done` the doctored copy edits); `docs/FORK_LEARNINGS.md:88` (#76); `docs/HANDOFFS_ARCHIVE_INDEX.md:54` (the new shard row); `docs/archive/HANDOFFS-through-2026-09-17-2.md` and its `.verify.sh`; `docs/planning/changelog-rules-contradictions-plan.md:175` (the P6 block), `:799` (the P7 row)
gotchas: **(1) A RECEIPT MAY NOW QUOTE `phantom_drift` SAFELY, AND THIS ONE DOES, DELIBERATELY.** Before `1cb4e44` that string anywhere in the newest receipt turned the suite red; after it, the gate ran green on a tree whose newest record contains it three times. **(2) `tests-sh-passed` READS 309 AT 2 RECEIPTS** on this tree (floor 305). A claim makes three receipts and six stated skips become assertions, so the same tree reads higher mid-session — never tighten a floor from a post-claim run. **(3) 2 RECEIPTS NOW: NO TRIM IS OWED at the next Phase 0.** **(4) A SECOND TRIM IN ONE DAY COLLIDES ON THE SHARD NAME** — `methodology_trim.py` disambiguates to `-2` and says so; the date in a shard name is a span label, not a key. **(5) RED-FIRST WITHOUT REWRITING THE LIVE LEDGERS: `cp -a` THE WORKING TREE TO SCRATCH AND RUN `bin/tests.sh` THERE.** A `--no-local` clone cannot see uncommitted work, and the suite rewrites both live ledgers in the tree it runs in (BL-57 plan hazard 7). **(6) PHASE 0 WRITES TWO TRACKED ROWS** — `.context-budget-history.jsonl` and `dashboard_history.jsonl`; both rode `f85dc75`. **(7) RUN SUITES ONE AT A TIME** (Test 9, GitHub rate limit). **(8) `tools/test_context_budget.py`'s FIT-GATE TEST STILL FAILS ON THIS MACHINE AND SKIPS IN EVERY CLONE (BL-65)**, and the four `*-unit-tests` gates extract `Ran (\d+) tests`, so none of them can see it. **(9) A CORRECTION TO `94031ed`'s LEDGER ENTRY:** it says the fold left `HANDOFFS.md` at 17,264 B; `wc -c` reads **17,256**. The entry stands as written (this ledger is append-only) and the close-out entry records the correction.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `quality_ratchet.py --run` (which runs `bash bin/tests.sh`) IN A `--no-local` CLONE WITH HEAD ASSERTED.** **Citation, clone of `1cb4e44`: `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results 8e12f40caec1 · manifest 3a87b16f1b31`**, `tests-sh-passed` 309 at 2 receipts. The Phase 0 run on `5ae7902` was `9/10 pass · 1 fail · results aff8a2e08e15`, which is the defect this session fixed. **BL-64's hole is narrowed here rather than left open:** the close-out commit is re-measured in a clone of itself immediately after it lands, and the result is recorded as its own `CHANGELOG.md` entry — a citation that covers the commit carrying this receipt. On `cp -a` copies of the working tree, which is where the RED-first runs were made: `307 passed, 2 failed, 6 skipped` before the fix, `309 passed, 0 failed, 6 skipped` after. On the live tree: `bin/check-handoff --all --allow-pending` 0 on 2 receipts and `--archived` 0 on the new shard; `bin/check-links` 0 (110 links, 23 files); `docs/archive/HANDOFFS-through-2026-09-17-2.md.verify.sh` 0 before the trim commit and after the fold; `bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations` 0 with row 76. **NOT EXERCISED:** any adopter sync, any upstream action, `tools/test_context_budget.py`'s fit-gate test in a clone (it skips there), CI (none).
changelog_ref: CHANGELOG.md "2026-09-17 · [BL-64] S183 close-out", plus the claim, the trim, the fold and the fix entries
commit: f85dc75 (claim) + 128efa4 (trim) + 94031ed (fold) + 1cb4e44 (the fix) + this close-out
```

**Self-assessment: 8/10.** Plus: Phase 0 re-ran the predecessor's citation instead of trusting it, found the gate red,
and pinned the flip to one commit and one line by replaying the planter through `bin/check-handoff`'s own `scan()`
against three trees — no suite re-run, no guessing. The two new assertions went in with the broken landing check still
in place and were RUN red in their final home, so RED-first is a log line rather than a claim. The frozen input is the
part that matters: (8b) plants into the live ledger and therefore rides the very window it documents, while (8d) plants
into a doctored fixture and stays armed whatever the ledger rotates to — which is why the comment asserting (8b) was
already independent had to be struck rather than kept. I said in the file what the new pair does *not* do (it does not
kill a landing check rewritten into a tautology) instead of letting the comment overclaim. And the close-out commit is
measured in a clone of itself, so this session's citation covers the commit carrying its own receipt — the hole BL-64
names, narrowed by practice rather than by argument. **Minus:** I wrote `17,264 B` into `94031ed`'s ledger entry by
subtracting a documented ~448 B pointer block instead of running `wc -c`, which reads 17,256 — a derived number
published as a measured one, in a repository whose whole discipline is the opposite, and it is now a correction rather
than a fact. I also carried the retention trim and the fix in one session; both were authorized, but the trim's four
commits make the close-out's diff wider than one deliverable's should be. **Growth:** four ledger entries plus the
close-out's, ~80 net lines in `bin/tests.sh`, one learnings row, one archive shard and its proof. **Reduction:**
`HANDOFFS.md` 34,289 → 17,256 B.

**Predecessor (S182): 7/10.** Its gotchas were load-bearing and every one that applied held. Gotcha (2) — *the clone is
the citation, and the clone can never cover the close-out commit* — is what told me where to look before I had run
anything, and gotcha (4) predicted both the receipt count and that the trim would be `--cut 2 --force` after the claim;
both were exactly right. Its `key_files` resolved: `bin/tests.sh:2469` is the guard's comment and `:2523` the planter,
at the tree it left. Its item (1) was specific enough to check `wsfct` read-only in three commands, and every claim in
it held. **Not 8:** its `runtime_smoke` cites `10/10 pass · 0 fail` for a tree that was already red — measured at
`b25fc19`, one commit before the close-out it certifies — which is the defect it had just written up as BL-64 and as
fork Learning #75, shipped one commit later in a new shape. And its fix introduced the control this session had to
repair: the planter it added decided a question about position by searching text, and the text it searched was the
live ledger, whose newest record is written by the close-out that cites the run. Its own comment claimed that
assertion did not depend on what the live ledger says today; the code beside it read the live ledger. **ROI: strongly
positive** — I spent no time rediscovering the shape of the guard, and the miss was the thing this session was assigned
to find.

```handoff
session: S182
date: 2026-09-17
status: complete
self_score: 7
predecessor_score: 7
active_task: **`bin/tests.sh` TEST 38'S DRIFT GUARD IS REPAIRED (`4c6da50`); THE QUALITY GATE IS GREEN AGAIN ON `main`. THREE FINDINGS RAISED: BL-64, BL-65, BL-66 — THE LAST IS UPSTREAM-FACING AND SITS IN `README.md`'s QUICK START.** Phase 0 found the gate red at `29b0feb` although S181's receipt cited `10/10 pass`: the guard measured a receipt from its opening fence to the NEXT receipt's, so the close-out prose between them read as receipt fields. Chosen by the operator after Phase 0 (picker), which also authorized the push to `origin` and the raising of backlog items. Nothing sent upstream. **P7 (`wsfct`) was done by `wsfct`'s own S630 while this session ran; recording it here is the next session's item (1).**
what_was_done: **Phase 0:** `CHANGELOG.md` frontier `29b0feb` = HEAD, no gap; `HANDOFFS.md` frontier `473c83d`, one commit behind and that commit is S181's authorized push record, so nothing backfilled. 2 receipts, no trim owed. **S181's gate citation did NOT re-run:** `8/10 pass · 2 fail · results 9ccbc3cb49b6 · manifest 3a87b16f1b31` in a `--no-local` clone of `29b0feb`, against its cited `10/10 pass · results 330ab6a19d4b` at `755fe0d`. Same manifest digest, so no threshold moved. Single failing assertion, Test 38's drift guard, bisected on the guard's own logic: `OK` at `755fe0d`/`b0bf91f`, `['applied']` at `473c83d`/`29b0feb`, `OK` again at `45bf347`. The dashboard read 76/100 with one HIGH flag naming both breached gates — a second instrument, same reading. **`45bf347`** claim. **`4c6da50`** the fix: the guard loads `bin/check-handoff` and calls its `scan()`, fence-bounded and fence-nesting aware; two assertions added, written RED first and RUN red in their final home (`FAIL: drift guard: prose below the closing fence reached the comparison as: phantom_drift`), and the planter re-reads the artifact through `scan()` to refuse a plant that landed on the wrong side of the fence. **`0f03f0e`** BL-64, **`89ef2ab`** BL-65, **`b25fc19`** BL-66, each with its own tagged ledger entry. **BL-66 was measured, not reasoned:** a scratch `git init` adopter installed from upstream `008d656` and never edited got exit 2 and nine false *"local modifications"* from the route `README.md:61` prescribes, and exit 0 with 10 files written from `--source=local`. **This close-out:** fork Learning #75, this receipt, the ledger entry.
next_steps: **(1) RECORD P7 HERE**, as S180 recorded P6 (plan `docs/planning/changelog-rules-contradictions-plan.md:799`). `wsfct`'s S630 did it today on branch `chore/s630-methodology-bl57-p7`, `790c77d1`..`3a257097`, six commits, tree clean, pushed to that project's `origin`, not merged; the sync is ONE commit (`8a41741c`, 14 files from fork `main` `29b0feb`), which is decision (18) applied. Check its claims read-only from here first, then write the plan status line, a P7 block and the BL-57 row. Verified from here at this close-out: `bin/sync ../wsfct --source=local --dry-run` exits 0 with all 23 files `unchanged`. **(2) THEN P8, `vscode_quarto_ext`** (plan `:800`), run from that project as its own session; re-derive its line numbers at the claim, since P6's went stale (item (17)). **(3) BL-66 WANTS AN UPSTREAM PR AND IS THE FIRST THING A NEW ADOPTER READS** — it is also P10's opening decision in disguise: `nprcgenekeepr`'s sync is blocked by one locally modified file, and option (a) there is to send the extension upstream. **(4) Push, authorized:** fork `main` goes to `origin` right after this close-out commit; its record follows under the standing grant. **(5) The next Phase 0 finds 3 receipts, so a retention trim IS owed** after the report — `--cut 2 --force` once this session's claim makes four (gotcha (2) of S181; `HANDOFFS.md`'s header still says `--cut 1`, which fits only a trim before any claim). **CARRIED:** BL-61; BL-60 (folds BL-36); BL-62 and #80's F5 ride P12; BL-54's PR; BL-63; `README.md`'s stale cost section (plan item (15)); the runner and `SAFEGUARDS.md` stay `over` budget.
key_files: `bin/tests.sh:2469` (the guard's comment, rewritten), `:2502` (the fence-bounded parser), `:2523` (the planter), `:2555`/`:2561`/`:2572` ((8a)/(8b)/(8c)); `bin/check-handoff:227` (`scan`, the borrowed parser), `:360` (`parse_block`, whose docstring named this hazard first); `tools/fixtures/handoff-ledger-2-records.md:10`; `docs/planning/BACKLOG.md:157` (BL-64), `:158` (BL-65), `:159` (BL-66); `docs/planning/BACKLOG-DETAIL.md` §BL-64/65/66; `docs/FORK_LEARNINGS.md:87` (#75); `README.md:61` (BL-66's sentence); `bin/sync:100` (the historyless GitHub fetch), `:117`–`:130` (the precedent for fixing this class); `starter-kit/BOOTSTRAP.md:86` (the contradicting advice); `tools/test_context_budget.py:340` (the transcript slug), `:355` (the narrow skip probe), `:372` (the failing test)
gotchas: **(1) `bash bin/tests.sh` IN THIS WORKING TREE READS `312 passed, 1 failed`; A `--no-local` CLONE READS `10/10 pass · 0 fail`. BOTH ARE HONEST.** The failure is `tools/test_context_budget.py`'s fit-gate presence control, which reads this machine's Claude Code transcripts and so SKIPS in every clone (BL-65). Do not read the live-tree red as a regression, and do not chase it while doing something else. **(2) THE CLONE IS THE CITATION, BY `HANDOFFS.md` §Citing the gate run** — and BL-64 records that the clone can never cover the close-out commit itself. **(3) A BARE GREP FOR `tests.sh` IN `bin/_manifest.py` RETURNS A MATCH THAT IS A COMMENT** (`:109`). The distributed set is the tuple list at `:37` onward; `bin/tests.sh` is not in it. **(4) 3 RECEIPTS NOW, SO A TRIM IS OWED NEXT PHASE 0** — and it is `--cut 2 --force` after the claim, not `--cut 1`. **(5) `tests-sh-passed` READS 313 AT 3 RECEIPTS** on the fixed tree (305 floor). Never tighten from a working-tree run. **(6) PHASE 0 WRITES A TRACKED ROW** (`context_budget.py --status` → `.context-budget-history.jsonl`); it rode `45bf347`. **(7) RUN SUITES ONE AT A TIME** (Test 9, GitHub rate limit; `gh api rate_limit` read 5000/5000 before the final run). **(8) `git fetch upstream origin` FETCHES A REF NAMED `origin` FROM `upstream` AND FAILS;** fetch each remote separately. **(9) NO `git add -p` HERE:** the three backlog commits were kept separate by writing one item at a time, not by partial staging.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `quality_ratchet.py --run` (which runs `bash bin/tests.sh`) IN A `--no-local` CLONE WITH HEAD ASSERTED.** **Final, clone of `b25fc19`: `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results 83c5e3fed6f3 · manifest 3a87b16f1b31`**, `tests-sh-passed` 313 at 3 receipts. The Phase 0 run on `29b0feb` was `8/10 pass · 2 fail · results 9ccbc3cb49b6`, which is the defect this session fixed; the clone of `4c6da50` already read `83c5e3fed6f3`. On the live tree after the commits: `bin/check-handoff --all --allow-pending` 0 on 3 receipts; `bin/check-links` 0; `docs/planning/BACKLOG-DETAIL.md.verify.sh` 0; `docs/planning/BACKLOG-archive-2026-08-15.md.verify.sh` 0; `docs/archive/HANDOFFS-through-2026-09-17.md.verify.sh` 0; `bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations` 0 with row 75. **Adopters, read-only, each with `git status --porcelain` identical before and after:** `bin/sync ../wsfct --source=local --dry-run` exit 0, 23 unchanged; `bin/sync ../nprcgenekeepr --source=local --dry-run` exit 2 on `methodology_trim.py` alone; the same two on `--source=github` exit 2 on 7 and 10 files; `bin/status ../nprcgenekeepr`. **A scratch adopter was built and synced in the scratchpad for BL-66** (upstream `008d656` → `6b29d3d`), outside every tracked repository. **NOT EXERCISED:** any real sync, any upstream action, `tools/test_context_budget.py`'s fit-gate test in a clone (it skips there), CI (none).
changelog_ref: CHANGELOG.md "2026-09-17 · [BL-64] S182 close-out", plus the claim, the fix, and the three raising entries
commit: 45bf347 (claim) + 4c6da50 (the fix) + 0f03f0e (BL-64) + 89ef2ab (BL-65) + b25fc19 (BL-66) + this close-out
```

**Self-assessment: 7/10.** Plus: Phase 0 caught a gate the previous close-out had certified green, and pinned it to
one commit and one line before anything was touched, on the guard's own logic rather than by re-running a suite four
times. The new assertions went in with the broken parser still in place and were RUN red in their final home, so the
RED-first claim is a log line, not an argument. The fix borrows `bin/check-handoff`'s `scan()` instead of re-deriving
a third record-extent rule, which is what makes the class fixed rather than the instance, and the mutant assertion
keeps the guard killable. When the operator asked whether the sync routes were broken, I built a clean-room adopter
instead of reasoning from the documents, which turned a plausible "both fail" into a measured upstream defect with a
control. I also caught my own bare-grep false positive on `bin/_manifest.py` before it reached a claim.
**Minus:** my Phase 0 report was written in this repository's private shorthand — *frontier*, *gap 0*, *standing
grant*, *receipt*, *citation*, *manifest digest* — and cost the operator two rounds of decoding before any work
could proceed. One of those sentences was also garbled. The instruction to name files and documented practices
instead is now recorded, but the cost was already paid, and it is the same reader-side reachability failure this
repository files against its own corpus. **Growth:** six ledger entries, three backlog items with detail bodies,
fork Learning #75, this receipt, ~103 net lines in `bin/tests.sh`. **Reduction:** none.

**Predecessor (S181): 7/10.** Its gotchas were the useful part and every one that applied held. Gotcha (4) predicted
that Phase 0 writes a tracked row, and it did — named in the report and ridden by the claim. Gotcha (6) (suites one
at a time) and gotcha (7) (`git fetch upstream origin` fails) were both applied without rediscovery. Item (4), *"the
next Phase 0 here finds 2 receipts: no trim"*, was exactly right. Item (1)'s start check for `wsfct` was the right
instruction for the right reason, and its `git status` discipline is what let this session confirm P7 cleanly.
**Not 8:** its `runtime_smoke` asserted `10/10 pass · 0 fail` for a tree that was already red, and gotcha (3)
predicted *"`tests-sh-passed` READS 305 AT 2 RECEIPTS"* when the tree it shipped read 304. Both were measured before
the close-out commit existed, which is structural and is now BL-64 — but `SESSION_RUNNER.md` 3D already requires a
forward-looking claim to be derived or labelled a guess, and gotcha (3) was stated as fact about a tree that did not
yet exist. Its item (1) also assumed P7 would need a session here to start it; `wsfct` ran it itself the same day,
which S181 could not have known and did not claim. **ROI: strongly positive** — the gotchas alone saved more than
the miss cost, because the miss was the thing this session was assigned to find.


