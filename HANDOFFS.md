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

```handoff
session: S179
date: 2026-09-17
status: complete
self_score: 8
predecessor_score: 8
active_task: **BL-54 IS FIXED FORK-SIDE: `bin/sync` AND `bin/status` SEE VERSIONS A MERGE HID FROM GIT'S DEFAULT WALK (`2c4f801`, BATCHED IN `865119f`), SO ADOPTERS CAN SYNC FROM FORK `main` AGAIN. BL-54 STAYS OPEN ONLY FOR ITS UPSTREAM PR. P6 IS NEXT, IN `airqino`'S OWN REPOSITORY.** Chosen by the operator after Phase 0 (picker), which also gave two go-aheads: trim `CHANGELOG.md` (done) and push fork `main` to `origin` at close-out. The count rule for *N versions behind* was the operator's too (picker, option C). Nothing sent upstream.
what_was_done: **`ce8c702`** claim, with the Phase 0 snapshots. **`ca52359`** the `CHANGELOG.md` trim: 104 records to `docs/archive/CHANGELOG-through-2026-09-16.md`, 264,071 → 99,397 B, no `--force` needed. It was trialled in a clone first: proof exit 0 before and after the commit, gates 10/10, suite unchanged. **`90da3e1`** the `HANDOFFS.md` retention trim, `--cut 2 --force`: S177 and S176 to `docs/archive/HANDOFFS-through-2026-09-16-5.md`. **`f975c4b`** its fold into the index (15,945 B). **`2c4f801`** the fix. `bin/sync` walks with `--full-history`. `bin/status` walks the first-parent line and the full history, and counts the distinct versions that landed on the first-parent line, falling back to the full walk for a version that only existed on a merged branch. The operator chose that rule (C) over A (the flag alone, a raw position) and B (distinct versions over the full walk), all three measured on the six adopters first. RED-first Test 41 builds a repo with both hiding merge shapes at fixed dates: 4 failures on the old code, 11/0 after, and eight mutants killed, A and B among them. **`865119f`** one `git cat-file --batch-check` per walk instead of a `git ls-tree` per commit. The fix had taken `bin/status` over the six adopters from 3.0 s to 10.1 s and `bin/sync --dry-run` from 2.9 s to 7.5 s; now 4.0 s and 2.3 s, with status output byte-identical over 174 rows. **`a0e84d5`** `tests-sh-passed` 294 → 305, measured in a clone. **`dd11c0c`** the BL-54 row and detail, the BL-57 row, the plan's status line, fork Learning #72.
next_steps: **(1) P6, `airqino`** (`docs/planning/changelog-rules-contradictions-plan.md:729`), **run from `~/Development/airqino` as that project's own session** (the runner's session-notes boundary rule; one adopter per session). Re-derive the route first: the plan says Route A from the branch because *"from fork `main`, BL-54 refuses four files"*, but `bin/sync airqino --dry-run --source=local` from fork `main` exits 0 on both the old code and the new (S179). BL-56 folds in. **(2) BL-54's upstream route is a go-ahead:** its own PR (Test 41 and `2c4f801`, with or without `865119f`), or inside P12's PR, which already carries BL-62 and #80's F5. `CLAUDE.md` prefers one substantial PR; BL-54 is independent of BL-57, so either is allowed. **(3) Push, authorized at Phase 0:** fork `main` goes to `origin` right after this close-out commit, and its record follows under the standing grant. **CARRIED:** BL-61; BL-60 (folds BL-36); BL-62 and F5 ride P12; `README.md`'s stale cost section (plan item (15)); the runner and `SAFEGUARDS.md` stay `over`.
key_files: `bin/status:52` (`blobs_at`), `:73` (`history_walk`), `:90` (`local_history`, the two walks), `:105` (`versions_behind`), `:130` (`file_status`, the fallback); `bin/sync:55` (`local_history_blobs`), `:64` (`--full-history`), `:75` (the batch); `bin/tests.sh:3076` (Test 41); `.quality-gates.json:12` (305); `docs/planning/BACKLOG.md:149` (BL-54), `:152` (BL-57); `docs/planning/BACKLOG-DETAIL.md:1627` (BL-54's resolution); `docs/planning/changelog-rules-contradictions-plan.md:5` (status), `:729` (P6–P11); `docs/FORK_LEARNINGS.md:84` (#72); `docs/archive/CHANGELOG-through-2026-09-16.md`; `docs/archive/HANDOFFS-through-2026-09-16-5.md`; `docs/HANDOFFS_ARCHIVE_INDEX.md:52`
gotchas: **(1) THE ADOPTER PHASES RUN IN THE ADOPTERS' REPOSITORIES, NOT HERE.** Each has its own Phase 0, claim, ledger entry and receipt. **(2) *N VERSIONS BEHIND* CHANGED ON 35 ADOPTER ROWS, MOSTLY DOWNWARD** (`mts-system`'s dashboard 29 → 15): a smaller number is the new count rule, not a sync. The 3 genuine local edits (`model_project_constructor`'s runner and `SAFEGUARDS.md`, `nprcgenekeepr`'s trimmer) still refuse; they are P10's and P11's decisions. **(3) THE FIX COMMIT'S LEDGER ENTRY CITES LINE NUMBERS FROM BEFORE THE BATCHING** (`:52`, `:81`, `:96`, `:121`, true at `2c4f801`); `865119f` moved them, and key_files has the current ones. **(4) TEST 41 DEPENDS ON GIT'S WALK BEHAVIOUR:** it uses `git init -b main` (git ≥ 2.28) and fixed commit dates, because the full walk orders by date. If a git upgrade changes history simplification, its fixture row (*4 / 8 / 4 commits*) fails before any status row does. **(5) `tests-sh-passed` 305 IS THE 2-RECEIPT VALUE;** a claim makes 3 receipts and the suite reads 311. **(6) RUN SUITES ONE AT A TIME** (Test 9 and GitHub's rate limit). **(7) `CHANGELOG.md` IS UNDER THE 262,144 B REFUSAL AGAIN** (107,421 B), still past the 56,750 B one-read cap: read its top with a limit.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh` AND `quality_ratchet.py --run`, in `--no-local` clones with HEAD asserted.** **Final, clone of `dd11c0c`: `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results 330ab6a19d4b · manifest 3a87b16f1b31`**; a second suite run there exited 0 with **305 passed / 0 failed / 6 skipped** (Test 34's stated skips at 2 receipts) and all 11 Test 41 rows passing. **Per stage:** the Phase 0 re-run on `fbdd47d` matched S178's citation (`1552052a766d`); the trim trial on `8e62af6` gave 10/10 with the suite at 300/0/0, as untrimmed; `2c4f801` gave 10/10 with 305 passed (`aa1eb690b169`). **The tools on the six real adopters (read-only):** `bin/status` over 174 rows, before and after the fix: 8 state changes, all *locally modified* → *N versions behind*; 35 count-only changes; 131 unchanged; the 3 genuine edits unchanged. After `865119f` the output is byte-identical. `bin/sync --dry-run`: `mts-system`, `vscode_quarto_ext` and `wsfct` go from exit 2 to 0; `model_project_constructor` and `nprcgenekeepr` stay at 2, on genuine edits only; `airqino` stays at 0. No adopter's `git status` changed. Both new archives' proof scripts exit 0 after their commits, and the `HANDOFFS.md` one after the fold too; `check-handoff --all --allow-pending` 0; `bin/check-links` 0; `bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations` 0; `docs/planning/BACKLOG-DETAIL.md.verify.sh` 0; `.githooks/commit-msg --selftest` 0. The dashboard (clone of `dd11c0c`) reads 76/100 with no high risk; `context_budget.py --status` exits 2 with the same three `over` rows as Phase 0. **NOT EXERCISED:** a real (not dry-run) sync of any adopter, any upstream action, CI (none).
changelog_ref: CHANGELOG.md "2026-09-17 · [BL-54] S179 close-out", plus the claim, the two trims and the fold, the fix, the batching, the floor and the records entries
commit: ce8c702 (claim) + ca52359 (CHANGELOG trim) + 90da3e1 (HANDOFFS trim) + f975c4b (fold) + 2c4f801 (fix) + 865119f (batching) + a0e84d5 (floor) + dd11c0c (records) + this close-out
```

**Self-assessment: 8/10.** Plus: each option was run before it was offered. The `CHANGELOG.md` trim was
trialled in a clone with its proof and the suite, and the three count rules were computed on all six
adopters. Test 41 failed before the fix, checks its own fixture, and fails on eight mutants, including both
rejected rules. The check on the real adopters matched the measurement row for row, and it found an eighth
misread row that the handoff had not listed. The fix's slowdown was measured, then removed in a separate,
behaviour-neutral commit. **Minus:** I compared the three count rules by their output, not their run time, so
the threefold slowdown surfaced only after the fix was written, which cost an extra commit and a second
verification pass. One comparison reported every sync output as different because `HEAD` had moved between
the two runs (the version line); I read the diff before concluding anything, but the comparison was set up
carelessly. The detail paragraph first gave a sync time without naming the adopter it was measured on; I
corrected that before committing. **Reduction:** `CHANGELOG.md` 264,071 → 99,397 B at the trim; `HANDOFFS.md`
36,666 → 15,945 B. **Growth:** nine ledger entries (two written by the trimmer), this receipt, Test 41 (72
lines), about 50 lines in `bin/status`, one detail paragraph and one learning row.

**Predecessor (S178): 8/10.** Its item (1) was exact and shaped the session: the lines at `bin/status:56` and
`bin/sync:60`, the merge shape to test, the open question about the count with its *63 behind* measurement,
and the check on the six adopters. Items (3) and (4) put both go-aheads in front of the operator at Phase 0.
Gotchas (3) (run suites one at a time), (4) (set hooks in a scratch clone) and (6) (a claim stages its entry)
were each applied. **Not 9:** its list of affected rows came from scratch copies and missed
`vscode_quarto_ext`'s `context_budget.py`, which was already misread before its own merge: 8 rows, not 7. It
also did not say that the default walk's count was already inflated by merged branches' commits (that
adopter's runner read 10 behind where 3 versions had landed), which is what made the count rule a real
choice rather than a side effect of the flag. **ROI: strongly positive.**

```handoff
session: S178
date: 2026-09-16
status: complete
self_score: 7
predecessor_score: 7
active_task: **BL-57'S P5 IS DONE, BY MERGE: FORK `main` CARRIES THE ONE-HOME `CHANGELOG.md` RULES (MERGE `22ce71b` OF `bl57/changelog-rules` `83a12f0`). BL-54 IS NEXT, BEFORE P6: THE MERGE MAKES `bin/status` READ `methodology_trim.py` AS LOCALLY MODIFIED IN 3 ADOPTER COPIES.** Chosen by the operator after Phase 0 (picker). Operator decisions, each by picker: merge rather than port; D10, remove the hook's claim carve-out (explained in plain prose on request), with the `tests-sh-passed` floor lowered to the measured count; keep the merge and take BL-54 next once its rows appeared. Fork-local: nothing pushed after `29321da`, nothing sent upstream.
what_was_done: **`29321da`** records the push of `fc4fe0c` (operator go-ahead), pushed under the push-record grant. **`cba2166`** claim, with the Phase 0 snapshots. **`22ce71b`** the merge: 5 conflicts, 9 hunks, as `merge-tree` said. `CHANGELOG.md` ours; `bin/_manifest.py` and `bin/tests.sh` theirs; `CLAUDE.md` the fork row naming the ledger rules; the runner the branch's 3F bullet plus the fork's `Model:` sentence re-pointed to §The Action Ledger (−14 B). A line-multiset check found every difference from the branch is a fork change or one of those resolutions. The 8 files identical at the base equal the branch's blobs. **`6774627`** a fork-only dashboard test read the live seed's fenced examples (plan hazard 6); it reads the frozen format-1 seed now, blob asserted, and a fence-blind mutant fails it. **`1664860`** D10: the hook equals the branch's byte for byte, and Test 27 (508 lines, 34 rows) is gone. A real claim-only commit exits 1 under the new hook, 0 under the old. **`dee680c`** root `CHANGELOG.md` front matter: the pointer; the cross-shell audit (638 in zsh and bash, equal to the heading count); `[BL-<id>]`; a Claims paragraph; the no-trim decision in place of the rate rule. Plus `HANDOFFS.md`'s retention line (a trim never runs in Phase 0). **`fd611a6`** `starter-kit/BOOTSTRAP.md:383` and `README.md:413`, two fork-only sentences the rules made false. **`368b29c`** `tests-sh-passed` 327 → 294, committed with `--no-verify` after the ratchet refused it (exit 2). 294 was measured at two receipts with Test 9 green; a 293 reading with Test 9 rate-limited was not used. **`d10f9af`** `trimmer-unit-tests` 123 → 124, measured. **`fbdd47d`** plan S178 block items (12)–(15), the BL-57 and BL-54 rows, fork Learning #71. `22ce71b`–`d10f9af` were built in a scratch clone and fast-forwarded onto `main` after their suites ran. The first two ran there without hooks and were checked afterwards: `commit-msg` 0, ledger co-staged, manifest unchanged.
next_steps: **(1) BL-54** (`docs/planning/BACKLOG-DETAIL.md:1602`; row `docs/planning/BACKLOG.md:149`): add `--full-history` at `bin/status:56` and `bin/sync:60`. RED first: build a test on a merge that keeps the merged-in side's content for a path. That is `22ce71b`'s shape for `starter-kit/methodology_trim.py`: the default walk visits 3 commits, `--full-history` 25, and before the merge it was 14. Settle the detail's open question too: with the flag, *N versions behind* inflates (scratch: `mts-system`'s `FRAMEWORK_LEARNINGS.md` went from locally modified to 63 behind), because the count indexes the walk. Verify with `bin/status --source=local` on scratch copies of the six adopters, before and after. S178's copies show 3 new *locally modified* rows (the trimmer in `mts-system`, `vscode_quarto_ext`, `wsfct`) and 4 older ones (`FRAMEWORK_LEARNINGS.md`), all cleared by the flag; `model_project_constructor`'s 2 rows and `nprcgenekeepr`'s trimmer are real local changes and stay. Its upstream PR is its own go-ahead. **(2) Then P6–P11** (plan `:729`), one adopter per session. **(3) `CHANGELOG.md` passes the 262,144 B hard read refusal with this close-out.** The operator's standing decision is to raise a trim only once it does, so ask at the next Phase 0 whether to trim before BL-54. **(4) Push:** fork `main` is 26 commits ahead of `origin` after this close-out; pushing needs a go-ahead. **CARRIED:** BL-61; BL-60 (folds BL-36); BL-62 and #80's F5 ride P12; `README.md`'s stale cost section (plan item (15)); the runner and `SAFEGUARDS.md` stay `over`.
key_files: `docs/planning/changelog-rules-contradictions-plan.md:149` (S178 block), `:684` (P5), `:729` (P6–P11); `docs/planning/BACKLOG-DETAIL.md:1602` (BL-54); `docs/planning/BACKLOG.md:149`, `:152`; `bin/status:56`, `bin/sync:60` (the walks); `.quality-gates.json:5` (`_fork_loosening_d10`), `:12` (294), `:43` (124); `.githooks/pre-commit` (the branch's hook, no carve-out); `bin/tests.sh:1203` (Test 27's removal note); `tools/test_methodology_dashboard.py:4673`; `CHANGELOG.md:11`, `:19`, `:40`, `:113` (front matter); `HANDOFFS.md:13`; `starter-kit/BOOTSTRAP.md:383`; `README.md:413`; `starter-kit/methodology_trim.py:33` (F5's claim, now false here too); `docs/FORK_LEARNINGS.md:83` (#71)
gotchas: **(1) UNTIL BL-54, A MERGE HIDES HISTORY FROM `bin/status` AND `bin/sync`** (fork Learning #71). Sync no adopter from fork `main` before BL-54 lands; a refused trimmer there is this defect, not an adopter edit. **(2) `tests-sh-passed` 294 IS THE 2-RECEIPT VALUE.** This close-out leaves 3 receipts, so the suite reads 300, and the next Phase 0 trim (`--cut 1 --force`) brings it back to 294. **(3) TEST 9 AND GITHUB'S RATE LIMIT:** two suites in parallel (Test 9 makes ~29 `gh` calls each) tripped a limit that `gh api rate_limit` did not show, and it cleared in about 15 minutes. Run suites one at a time, and never take a floor from a run where Test 9 failed. **(4) A SCRATCH CLONE RUNS NO HOOKS:** run `git config core.hooksPath .githooks` in it before committing anything you will land. **(5) `--no-verify` SKIPS `commit-msg` TOO:** after an approved bypass, run `.githooks/commit-msg <msgfile>` by hand. **(6) THE HOOK NOW EXEMPTS NO CLAIM:** a claim commit must stage its *(in progress)* entry. **(7) ZSH:** an unquoted `$h` does not word-split, so `set -- $h` took one argument; use bash for that.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh` AND `quality_ratchet.py --run`, in `--no-local` clones with HEAD asserted.** **Final, clone of `fbdd47d`: `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results 1552052a766d · manifest 8d8ddc767cdc`**; suite exit 0, **300 passed / 0 failed / 0 skipped** (3 receipts). Against `6774627`, the row diff is Test 27's 34 rows gone and Test 9 FAIL → PASS, nothing else. Dashboard exit 0, v2.18.0, 76/100; gates panel *10 pass / 0 fail*, *1 loosened*. **Per stage:** the Phase 0 re-run on `fc4fe0c` matched S177's citation (`db4e547cc884`); parent `cba2166` 332/1/0; merge `22ce71b` 332/2/0; `6774627` 333/1/0; `1664860` at 2 receipts 293/1/6 with Test 9 rate-limited, then `--run` 294 passed / 0 failed (results `839fb8a9f80a`). **P5's DONE, measured:** the 5 identical distributed files equal the branch's blobs; the audit is equal in zsh and bash (635 at Phase 0, old form equal); a claim-only commit is refused (real commit, scratch repo); `bin/status` on six adopter copies reads `CHANGELOG.md` *present (stale format)* in all six, **but tracked rows are not all as before: 3 new *locally modified* (BL-54)**. `bin/check-links` 0; `bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations` 0; `bin/check-handoff --all --allow-pending` 0. `context_budget.py --status` exit 2 at Phase 0 and close-out, the same three `over` rows, runner −14 B. **NOT EXERCISED:** any push after `29321da`, adopter syncs, upstream actions, CI (none).
changelog_ref: CHANGELOG.md "2026-09-17 · [BL-57] S178 close-out", plus the claim, the push record, the merge record with the test fix, D10, the front matter, the two fork-only sentences, the floor, the tightening and the P5-recorded entries
commit: 29321da + cba2166 (claim) + 22ce71b (merge) + 6774627 + 1664860 + dee680c + fd611a6 + 368b29c + d10f9af + fbdd47d + this close-out
```

**Self-assessment: 7/10.** Plus: nothing reached live `main` until it had been verified in a scratch clone. The
merge resolution was checked by line multiset against both parents. The suite ran at every state, with
digit-masked row diffs, which isolated the fork-only test failure at once; its fix was shown to kill a
fence-blind mutant. D10 was proven with real commits under both hooks. The floor was taken at the state a
trimmed ledger returns to, and a 293 reading with Test 9 failing was refused as a floor. The rules also made
two fork-only sentences false, and the plan's own inventory, re-run on the merge, found them. **Minus:** I
recommended the merge before running P5's own `bin/status` criterion on both routes, and that criterion was
the one that told them apart (BL-54). It cost you a third decision, which should have come with the first.
My first D10 question was too dense to decide from, and you had to ask for an explanation. Two commits were
made in a clone without hooks (checked afterwards). I ran two suites in parallel and tripped GitHub's rate
limit, which cost two measurement runs. One ledger entry's wording was corrected before landing. The zsh
word-split trap recurred. **Reduction:** the root `CHANGELOG.md` front matter −959 B; the runner −14 B;
`bin/tests.sh` −504 lines. **Growth:** eleven ledger entries push `CHANGELOG.md` past 262,144 B; plus this
receipt, plan items (12)–(15) and one learning row.

**Predecessor (S177): 7/10.** Its item (1) was exact and shaped the session. The 5-file conflict set held.
*"Contains `64f23bf`, not `6b29d3d`, so decide merge vs port by measuring both"* was the right instruction,
and the pre-flight held too. Gotcha (2) (327 is the 2-receipt value; never loosen for a lone Test 9 failure)
is why the floor was measured correctly. Gotcha (7) (the ledger's headroom) was accurate. **Not 8:** it
tightened `tests-sh-passed` to 327, a floor that includes Test 27's 34 rows, one session before P5, whose
approved D10 deletes Test 27, and did not flag the collision. It named merge vs port without naming plan
hazard 11 (BL-54), which is what a merge of the branch triggers. Gotcha (1)'s *"~17 min"* gate run takes
about 3. **ROI: positive.**

