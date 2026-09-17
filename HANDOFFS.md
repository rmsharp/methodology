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
session: S182
date: 2026-09-17
status: pending
self_score: pending
predecessor_score: pending
active_task: **REPAIR `bin/tests.sh` TEST 38'S DRIFT GUARD, WHICH ITS OWN RECORD EXTENT TURNED RED ON `main`.** The guard measures the newest receipt as opening fence → next record's opening fence, so it reads the self-assessment prose between records as receipt fields; `HANDOFFS.md:85` wraps onto `applied: `, and the frozen fixture has no such field. Chosen by the operator after Phase 0 (picker), with the go-ahead to push fork `main` to `origin` at close-out and to raise a backlog item for what Phase 0 found. Fork-local until the push; nothing upstream.
what_was_done: pending
next_steps: pending
key_files: `bin/tests.sh:2472` (the guard's comment), `:2475` (the extent), `:2495` (the failing assertion); `bin/check-handoff:269` (`scan`, the fence-bounded parser the checker already uses), `:359` (`parse_block`, whose docstring names this exact hazard); `tools/fixtures/handoff-ledger-2-records.md:10` (the frozen fixture); `HANDOFFS.md:85` (the prose line that fires it)
gotchas: The gate is red BEFORE this session touches anything — `8/10 pass · 2 fail · results 9ccbc3cb49b6 · manifest 3a87b16f1b31` at `29b0feb`, against S181's `10/10 · results 330ab6a19d4b` measured a commit earlier at `755fe0d`. Do not read the red as this session's doing, and do not tighten or loosen a threshold to clear it: the manifest digest is unchanged and the fix belongs in the guard. `tests-sh-passed` reads 304 at 2 receipts; with this claim making 3, Test 34's six stated skips become assertions and the same broken tree reads 310.
runtime_smoke: pending
changelog_ref: CHANGELOG.md "2026-09-17 · [BL-64] S182 claim"
commit: pending
```

```handoff
session: S181
date: 2026-09-17
status: complete
self_score: 7
predecessor_score: 8
active_task: **BL-57 PLAN ITEM (18) IS DECIDED: ONE `bin/sync` RUN IS ONE COMMIT, FOR P7–P11 (operator, picker). `HANDOFFS.md` IS TRIMMED AND FOLDED. P7, `wsfct`, IS NEXT, BUT ONLY AFTER `wsfct`'S OWN S629 CLOSES; THAT SESSION WAS OPEN WHILE THIS ONE RAN.** The same picker gave the go-ahead to push fork `main` to `origin` after this close-out. Before choosing, the operator asked whether waiting for the `wsfct` or `nprcgenekeepr` sessions to end would change this session's options. It would not: adopter phases run in the adopters' own repositories. Nothing sent upstream.
what_was_done: **Phase 0:** no gap in either ledger. S180's gate citation, re-run in a clone of `b0bf91f`, matched (`c86e8ef9b42b`). Dashboard (second clone) 76/100, no high risk. `context_budget.py --status` exit 2 with the same three `over` rows; its row rode the claim, and the report said so. **`74cee65`** claim. **`89cbf05`** retention trim, `--cut 2 --force`: S179 and S178 to `docs/archive/HANDOFFS-through-2026-09-17.md`, 33,267 → 13,883 B; its proof exits 0 before and after the commit. **`2784cc4`** fold into the index, 13,435 B. **`82a0b3b`** item (18) recorded (a decision paragraph, step 2 of P6–P11, the status line, the BL-57 row) and P7's start check. Every claim was checked before the picker: `wsfct`'s dry run at `b0bf91f` (exit 0, 14 files, its `git status` the same before and after); its current `SESSION_RUNNER.md` and `SAFEGUARDS.md` mention neither `quality_ratchet.py` nor `.quality-gates.json`, and neither file exists there; `airqino`'s `28022fe` holds its 14 synced files plus its entry. **`755fe0d`** BL-63 raised, with its own `[BL-63]` entry, as BL-62's raising had: no distributed document says how to commit a sync, so every adopter meets the cap. **This close-out:** fork Learning #74, this receipt, the ledger entry.
next_steps: **(1) P7, `wsfct`** (plan `docs/planning/changelog-rules-contradictions-plan.md:799`), run from `~/Development/wsfct` as that project's own session, **and only once `git status --porcelain` there is empty and its S629 (claim `94dd56ae`, Dependabot PR #901) has closed out.** Route B from fork `main`: re-run the dry run at the claim (14 files at `b0bf91f`). Commit the sync as ONE commit: exactly the files the run wrote plus its ledger entry, nothing else (step 2, `:772`; decision `:198`). The header migration and the `CLAUDE.md` wording go in their own commits. The block is still `CHANGELOG.md:13`–`196` (`## 2026-09` at `:197`, checked at S181), but re-derive the `CLAUDE.md` lines. `wsfct` merges through PRs, so branch there. **(2) After P7 reports, a session here records it,** as S180 recorded P6: its claims checked read-only from here, then the plan block, row and BL-57 row. **(3) Push, authorized:** fork `main` goes to `origin` right after this close-out commit; its record follows under the standing grant. **(4) The next Phase 0 here finds 2 receipts: no trim.** **(5) Upstream go-aheads, still pending:** BL-54's PR, and now BL-63 (whether `SAFEGUARDS.md` or `BOOTSTRAP.md` tells every adopter how to commit a sync); both fit P12. **CARRIED:** BL-61; BL-60 (folds BL-36); BL-62 and #80's F5 ride P12; `README.md`'s stale cost section (plan item (15)); the runner and `SAFEGUARDS.md` stay `over`. P10 (`nprcgenekeepr`) opens with a decision this repository can prepare while its S696 runs: its 49 added lines register `SESSION_NOTES.md` as a third trimmer ledger, which is BL-32.
key_files: `docs/planning/changelog-rules-contradictions-plan.md:7` (status line), `:192` (item (18)), `:198` (the decision), `:772` (step 2), `:799` (P7 row); `docs/planning/BACKLOG.md:151` (BL-57), `:156` (BL-63); `docs/planning/BACKLOG-DETAIL.md:2130` (BL-63); `docs/FORK_LEARNINGS.md:86` (#74); `docs/HANDOFFS_ARCHIVE_INDEX.md:53` (the new row); `docs/archive/HANDOFFS-through-2026-09-17.md` and its `.verify.sh`; in `~/Development/wsfct`: `CHANGELOG.md:13`–`196` (the block)
gotchas: **(1) `wsfct` HAS A SESSION OPEN.** Its S629 claimed while this session ran: clean at Phase 0, then staged, then committed as `94dd56ae`. Check `git status --porcelain` and its newest receipt at P7's claim, not before (fork Learning #74). **(2) A TRIM AFTER A CLAIM IS `--cut 2`, NOT `--cut 1`.** `HANDOFFS.md`'s header and S180's item (3) say `--cut 1`, which fits only a trim made before any claim; the claim is a fourth record. S175 and S179 met the same mismatch. **(3) `tests-sh-passed` READS 305 AT 2 RECEIPTS** (this close-out) and 311 once the next claim makes 3. Never tighten from 311. **(4) PHASE 0 STILL WRITES A TRACKED ROW** (`context_budget.py --status` → `.context-budget-history.jsonl`); it rides the claim. **(5) NO `git add -p` HERE:** to commit one hunk of a file, write the partial version, stage it, then restore the full file (used for `BACKLOG.md` between `82a0b3b` and `755fe0d`). **(6) RUN SUITES ONE AT A TIME** (Test 9 and GitHub's rate limit). **(7) `git fetch upstream origin` FETCHES A REF NAMED `origin` FROM `upstream`** and fails; fetch each remote separately.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `quality_ratchet.py --run` (which runs `bash bin/tests.sh`) IN A `--no-local` CLONE WITH HEAD ASSERTED.** **Final, clone of `755fe0d`: `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results 330ab6a19d4b · manifest 3a87b16f1b31`**, `tests-sh-passed` 305 at 2 receipts, the same results digest as S179's 2-receipt run. The Phase 0 run on `b0bf91f` matched S180's citation (`c86e8ef9b42b`, 311 at 3 receipts). On the live tree after the commits: `docs/archive/HANDOFFS-through-2026-09-17.md.verify.sh` 0 (after the trim and after the fold); `bin/check-handoff --all --allow-pending` 0 on 2 receipts, `--archived --file` the shard 0; `bin/check-links` 0; `docs/planning/BACKLOG-DETAIL.md.verify.sh` 0; `docs/planning/BACKLOG-archive-2026-08-15.md.verify.sh` 0; `bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations` 0 with row 74. **Adopters, read-only:** `bin/sync ../wsfct --source=local --dry-run` exit 0, 14 files; `airqino` `28022fe`, `dfe26fd`, `5e4b483`, `9f150a5` by `git show --stat`; `nprcgenekeepr`'s trimmer diffed against the closest fork version (`c43e7ee`, 49 lines). **NOT EXERCISED:** any real sync, any upstream action, CI (none).
changelog_ref: CHANGELOG.md "2026-09-17 · [BL-57] S181 close-out", plus the claim, the trim and fold, the item-(18) and BL-63 entries
commit: 74cee65 (claim) + 89cbf05 (trim) + 2784cc4 (fold) + 82a0b3b (item (18)) + 755fe0d (BL-63) + this close-out
```

**Self-assessment: 7/10.** Plus: I checked each claim before it reached the picker. That covered `wsfct`'s dry run, the
claim that split commits would cite missing files (in `wsfct` itself), and the makeup of `airqino`'s sync commit. Re-running
that check with `git status` before and after is what caught another session opening in `wsfct` while this one ran,
which became the P7 start check and fork Learning #74. The operator's two follow-up questions were answered with
measurements (PR #901's files, where the block sits against the newest entry, the 49 lines in `nprcgenekeepr`'s
trimmer), not with the rule alone. The trim's proof ran before and after its commit and after the fold. The records
were split so each ledger entry carries one tag. **Minus:** my Phase 0 picker did not say that no option here depended on
other repositories' sessions, or that P10's opening decision could be prepared from here, so it took the operator two
questions to reach the choice. I had `--cut 1` in mind from memory and S180's handoff until S179's commits showed
`--cut 2`. I told the operator I would not record S629's details in the P7 row, then added a dated parenthetical about it.
**Growth:** six ledger entries (one written by the trimmer), the plan's decision paragraph and edits (+17 −3 lines),
BL-63's row and a 30-line detail, fork Learning #74, this receipt. **Reduction:** `HANDOFFS.md` 33,267 → 13,435 B
before this receipt.

**Predecessor (S180): 8/10.** Its item (1) put the right decision first and named both options exactly, and its
figures held when re-run (14 files for `wsfct`, `ef04625d`). Gotcha (1), that Phase 0 writes tracked files, was
applied: my report named the row. Gotcha (2), 311 at 3 receipts, matched the Phase 0 run exactly. Gotcha (6),
suites one at a time, was followed. **Not 9:** item (3) gave `--cut 1` for a trim that follows a claim, where
`--cut 2` is right, a mismatch two earlier sessions had already recorded. Item (1) posed the decision without the
cost of either option: under the synced rules each split commit carries its own entry, and a split leaves the
framework citing missing tools. Nor did it note that the question applies to every adopter, not only this plan
(now BL-63). Its *"`wsfct` … clean"* was true when written and went stale within this session, and that is not
something it could have known. **ROI: strongly positive.**

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

