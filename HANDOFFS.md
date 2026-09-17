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
session: S181
date: 2026-09-17
status: pending
self_score: pending
predecessor_score: pending
active_task: **TRIM `HANDOFFS.md`, RECORD THE OPERATOR'S ANSWER TO BL-57 PLAN ITEM (18) (ONE `bin/sync` RUN IS ONE COMMIT, FOR P7–P11), AND ADD A START CHECK TO THE P7 ROW.** Chosen by the operator after Phase 0 (picker), with item (18) answered and the go-ahead to push fork `main` to `origin` at close-out in the same picker. P7 itself runs later from `~/Development/wsfct`, as that project's own session. Fork-local until the push; nothing upstream.
what_was_done: pending
next_steps: pending
key_files: `docs/planning/changelog-rules-contradictions-plan.md:5` (status), `:192` (item (18)), `:753` (P6–P11), `:785` (P7 row); `docs/planning/BACKLOG.md:151` (BL-57); `docs/HANDOFFS_ARCHIVE_INDEX.md` (the fold)
gotchas: `wsfct` is not clean: its own S629 has a claim staged (`HANDOFFS.md`, `SESSION_NOTES.md`), so P7 cannot start there until that session closes. With this claim the ledger holds 4 receipts; `--cut 2 --force` keeps this stub and S180's receipt, as S179's trim did after its claim.
runtime_smoke: pending
changelog_ref: CHANGELOG.md "2026-09-17 · [BL-57] S181 claim"
commit: pending
```

```handoff
session: S180
date: 2026-09-17
status: complete
self_score: 7
predecessor_score: 8
active_task: **BL-57'S P6 IS DONE, IN `airqino`'S OWN REPOSITORY, AND RECORDED HERE; BL-56 IS CLOSED. P7, `wsfct`, IS NEXT, AFTER ONE OPERATOR DECISION: A `bin/sync` WRITES 14–16 FILES AGAINST `SAFEGUARDS.md`'S FIVE-FILE COMMIT CAP (plan item (18)).** The operator chose P6 at Phase 0 (picker) and ran it from `~/Development/airqino` as that project's Session 6 (local branch `chore/methodology-bl57-p6`, `2b0230a`..`e947798`, not pushed). After its report, a second picker chose to record it here this session, and gave the go-ahead to push fork `main` to `origin` at close-out. Nothing sent upstream.
what_was_done: **Phase 0 in this repository:** no gap in either ledger; S179's gate citation re-run in a clone of `ff02b5c` matched (`330ab6a19d4b`). **Before P6,** fork `main`'s `bin/sync ../airqino --dry-run` exited 0 with no refusals, and the prompt handed to that session said so. **`airqino`'s claims checked from here, read-only:** its 5 commits; every tracked file `current` and all six seeds `present`; `5e4b483` removes only `CHANGELOG.md` lines 1–11; 7 headings and 7 by the audit; its tree unchanged. **`5b5a19a`** the claim, carrying the context-budget row Phase 0 wrote. **`b5a422b`** BL-56 closed: its done test re-run, `bin/status` reads `present` from the branch `83a12f0`, `upstream/main` `6b29d3d` and fork `main` `ff02b5c`, each a `--no-local` clone with HEAD asserted; row moved to §Completed items, closing paragraph in the detail file. **`04fccc5`** P6 recorded: the plan's status line, a P6 block with items (16)–(18), and the P6 row with its two stale facts struck through; the BL-57 row. Item (16) re-ran the dry runs on the five remaining adopters rather than quoting S179. **This close-out:** fork Learning #73, this receipt, the ledger entry.
next_steps: **(1) DECIDE plan item (18) BEFORE P7** (`docs/planning/changelog-rules-contradictions-plan.md:192`): split a sync's files across commits of five, or treat one `bin/sync` run as one commit. It applies to P7–P11 alike. `airqino`'s two syncs were one commit each (15 and 21 files). **(2) P7, `wsfct`** (plan `:785`), run from `~/Development/wsfct` as that project's own session. Route B: at `b5a422b` its dry run exits 0 with no refusals and would write 14 files. Re-derive the row's fixed figures at the claim (block `:13`–`196`, 5 `### ` lines, `CLAUDE.md` `:43`, `:162`, `:206`, `:218`, `:695`): they were measured 2026-09-14, and P6's went stale (item (17)). `wsfct` is on `master` at `ef04625d`, clean, and merges through PRs, so its session should branch. **(3) THIS REPOSITORY'S NEXT PHASE 0 FINDS 3 RECEIPTS:** trim `HANDOFFS.md` with `--cut 1 --force` after the report, then fold its pointer block in its own commit. **(4) Push, authorized:** fork `main` goes to `origin` right after this close-out commit, and its record follows under the standing grant. **(5) BL-54's upstream route is still a go-ahead:** its own PR, or inside P12's. **CARRIED:** BL-61; BL-60 (folds BL-36); BL-62 and #80's F5 ride P12; `README.md`'s stale cost section (plan item (15)); the runner and `SAFEGUARDS.md` stay `over`. `airqino`'s branch and its PR #1 are that project's go-aheads.
key_files: `docs/planning/changelog-rules-contradictions-plan.md:5` (status), `:175` (P6 block), `:182` (16), `:192` (18), `:753` (P6–P11), `:784` (P6 row), `:785` (P7 row); `docs/planning/BACKLOG.md:151` (BL-57), `:160` (BL-56, completed); `docs/planning/BACKLOG-DETAIL.md:1710` (BL-56's closing paragraph); `docs/FORK_LEARNINGS.md:85` (#73); in `~/Development/airqino`: `CHANGELOG.md:1`–`16` (the new header), branch `chore/methodology-bl57-p6`
gotchas: **(1) PHASE 0 WRITES TRACKED FILES HERE.** `context_budget.py --status` appends to `.context-budget-history.jsonl`, and the dashboard run at the root appends to `dashboard_history.jsonl`. Run `git status --porcelain` before reporting that nothing changed (fork Learning #73); the rows ride the claim. **(2) `tests-sh-passed` READS 311 AT 3 RECEIPTS** and 305 after the next trim; both pass the 305 floor. Never tighten from 311. **(3) P6'S COMMITS EXIST ONLY IN `airqino`'S LOCAL BRANCH:** name that repository whenever citing them. **(4) `bin/sync`'S EXIT 2 ON `nprcgenekeepr` AND `model_project_constructor` IS REAL:** it refuses their genuine local edits (the trimmer; the runner and `SAFEGUARDS.md`), which are P10's and P11's opening decisions. It is not BL-54. **(5) ZSH, TWICE AGAIN:** `echo =====` aborted a command, and `git rev-parse --short` given three refs failed. Quote the first, loop the second. **(6) RUN SUITES ONE AT A TIME** (Test 9 and GitHub's rate limit).
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `quality_ratchet.py --run` (which runs `bash bin/tests.sh`) IN A `--no-local` CLONE WITH HEAD ASSERTED.** **Final, clone of `04fccc5`: `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results c86e8ef9b42b · manifest 3a87b16f1b31`**, `tests-sh-passed` 311 at 3 receipts. The Phase 0 run on `ff02b5c` matched S179's citation (`330ab6a19d4b`, 305 at 2 receipts). After `04fccc5`, on the live tree: `bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations` 0 with row 73; `bin/check-links` 0; `docs/planning/BACKLOG-DETAIL.md.verify.sh` 0; `docs/planning/BACKLOG-archive-2026-08-15.md.verify.sh` 0. The dashboard (clone of `ff02b5c`) read 76/100 with no high risk. **The adopter tools, read-only:** `bin/status` on `airqino` from three trees; `bin/sync --dry-run` on the other five from `b5a422b`, each with its `git status` identical before and after. **NOT EXERCISED:** `airqino`'s own suite (it has none; that session parsed its Python and imported the app), any real sync from this session, any upstream action, CI (none).
changelog_ref: CHANGELOG.md "2026-09-17 · [BL-57] S180 close-out", plus the claim, the BL-56 closure and the P6-recorded entries
commit: 5b5a19a (claim) + b5a422b (BL-56 closed) + 04fccc5 (P6 recorded) + this close-out
```

**Self-assessment: 7/10.** Plus: nothing from `airqino`'s report went into this repository until it was checked
here. That meant its commits, `bin/status` from three separate trees, the migration diff and both counts. The
plan's new item (16) re-ran the dry runs on the five remaining adopters instead of repeating S179's figures. The
records split into two commits so each carries one ledger entry with one tag. Both decisions came in one picker,
recommendation first. **Minus:** my Phase 0 report told you nothing had changed in either repository while
my own `context_budget.py --status` run had already written a tracked row. I found it only when a later check
ran `git status` here, and that is fork Learning #73. Two zsh traps already in my notes recurred at Phase 0.
Neither did damage, but each cost a re-run. My Phase 0 recommendation for P6 missed the five-file cap
question, which that session then hit without asking. **Growth:** four ledger entries, this receipt, a
14-line plan block, one closing paragraph, one learning row. **Reduction:** none.

**Predecessor (S179): 8/10.** Its item (1) was exact and shaped both sessions. It said to run P6 from `airqino`
as that project's own session, and to re-derive the route because the dry run from fork `main` already exited
0. Both held. Gotcha (1) (adopter phases run in the adopters' repositories) settled the question of where the
work belonged at once. Gotcha (5) predicted the 311 reading at 3 receipts exactly. Gotcha (6) (suites one at a
time) was applied, and item (3)'s push record is `ff02b5c`, as announced. **Not 9:** it flagged the P6 row's
route reason as stale but checked none of the row's other facts. The *one entry* had been two since
`airqino`'s Session 5 (2026-09-15), before S179 ran. It also did not mention that a sync writes more files than
the commit cap allows, which the P6 session then ran into. And it did not warn that Phase 0's gate run writes
a tracked row here. **ROI: strongly positive.**

