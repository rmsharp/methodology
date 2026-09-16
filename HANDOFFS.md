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
never on a record count**, so the policy is applied by the session that notices: at Phase 0 run
`grep -c '^```handoff' HANDOFFS.md`; **above 2**, trim with `--cut 1 --force`. The force is
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
     trim commit the shipped .verify.sh fails L2 (Learning #58). -->

**Archived 9 record(s), 2026-09-14 → 2026-09-16** into [`docs/archive/HANDOFFS-through-2026-09-16-3.md`](docs/archive/HANDOFFS-through-2026-09-16-3.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/HANDOFFS-through-2026-09-16-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-16-3.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

```handoff
session: S176
date: 2026-09-16
status: pending
self_score: pending
predecessor_score: pending
active_task: **R1 OF THE RATIFIED RESYNC PLAN (`docs/planning/upstream-resync-2026-09-plan.md` §5): MERGE STAGE M1, `0fd003a`, INTO FORK `main`, AND CARRY OUT D1 (A), CHOSEN BY THE OPERATOR AFTER PHASE 0 (picker).** Pre-flight re-derived at Phase 0: `upstream/main` still `6b29d3d`, PR #83 still open at `219fb9d`, and `git merge-tree --write-tree --name-only main 0fd003a` lists the same 4 files as §2.1. D1 (A): the distributed learnings file becomes upstream's; fork rows #15–#66 move verbatim to `docs/FORK_LEARNINGS.md`. Fork-local; nothing pushed.
what_was_done: pending
next_steps: pending
key_files: `docs/planning/upstream-resync-2026-09-plan.md:127` (§2.3 row 1), `:136` (row 10), `:141` (§2.4 ledgers), `:193` (D1), `:216` (D1's trial, three failures), `:285` (R1); `bin/tests.sh:1281` (Test 27.N1b's commit), `:2561` (`add_row37`); `tools/test_methodology_dashboard.py:5359` (the Learning #26 pin); `bin/check-learnings:123` (the fixed path)
gotchas: `CLAUDECODE=1` and `core.hooksPath` = `.githooks` here, so the arriving `.githooks/commit-msg` refuses any commit without a `Co-Authored-By:` trailer from M1 on, including the suite's own fixture commit (Test 27.N1b). The merge commit skips the hooks; its ledger entry rides the next ordinary commit. Run the suite in a `--no-local` clone of a committed state.
runtime_smoke: pending
changelog_ref: CHANGELOG.md "2026-09-16 · [BL-57] S176 claim"
commit: pending
```

```handoff
session: S175
date: 2026-09-16
status: complete
self_score: 7
predecessor_score: 8
active_task: **THE FORK RESYNC IS PLANNED, NOT MERGED: `docs/planning/upstream-resync-2026-09-plan.md` (DRAFT) MERGES `upstream/main` `6b29d3d` INTO FORK `main` IN FOUR STAGES OVER TWO SESSIONS, R1 AND R2, AND WAITS ON THE OPERATOR'S D1–D4.** The operator chose "Trim, then resync" after Phase 0, then re-scoped to "Write the merge plan" (picker) once `merge-tree` showed about two dozen conflict hunks in 13 files, with resolutions only the operator can decide. The `HANDOFFS.md` trim and fold are done. Fork-local: nothing pushed, nothing sent upstream.
what_was_done: **`88e40f5`** -- claim, with the two Phase 0 instrument snapshots. **`4679cca`** -- `HANDOFFS.md` trimmed, S173 and S172 to `docs/archive/HANDOFFS-through-2026-09-16-2.md`, 40,816 -> 15,874 B, `--cut 2 --force`: the claim stub was a fourth record, so `--cut 2` removed the same 24,942 B a Phase 0 `--cut 1` would have. Proof exit 0 before and after the commit. **`1f34e75`** -- the pointer block folded into `docs/HANDOFFS_ARCHIVE_INDEX.md` as one 124 B row; front matter 4,475 B inside the trim commit, back to 4,019 B. **`e3bc12c`** -- the plan, with the operator's re-scope decision recorded. It rests on: per-commit `merge-tree` conflict sets that cut four stages at `0fd003a` / `cca7941` / `64f23bf` / `6b29d3d` (4 / 4 / 5 / 0 newly conflicting files); a resolution and a verification for each of the 13 files; the 33 upstream-changed paths split 13 / 6 / 14; upstream's 11 receipts passing the fork's `check-handoff` (`--all`, `--archived`); the merge taking `CHANGELOG.md` over the trimmer's 196,608 B trigger; the ten arriving gates against the fork's measured values; and **a trial of D1's recommendation** (stage 1 merged in a throwaway clone): 297 / 3 / 6 against 300 / 0 / 6, exactly three flips. Two are D1's cost. **The third is not: upstream's `commit-msg` hook refuses Test 27.N1b's trailer-less fixture commit under an agent harness, whatever D1 decides.** A read-only claims review (an opus subagent, ~150 claims) found 15 wrong claims in the draft; each was re-run and corrected before `e3bc12c`. Also found at Phase 0: upstream PR #83 (the maintainer's parallel-sessions plan) conflicts with fork `main` in the same 13 files, so the resync gains no conflicts from it.
next_steps: **DECIDED BY THE OPERATOR AFTER THIS CLOSE-OUT (picker): D1 (A), D2 (a), D3 (a), D4 (a) — every recommendation; the plan is RATIFIED, so R1 is next.** **(1) THE OPERATOR RATIFIES OR REVERSES D1–D4** (`docs/planning/upstream-resync-2026-09-plan.md:187`). One picker, recommendations first: D1 (A) the distributed learnings file becomes upstream's and the fork's rows #15–#66 move verbatim to `docs/FORK_LEARNINGS.md`; D2 (a) adopt the ratchet and tighten it to the fork's values after stage 4; D3 (a) `DASHBOARD_VERSION` 2.18.0; D4 (a) R1 = stage 1, R2 = stages 2–4. If the operator answers after this close-out, record it in a follow-up entry, as S173/S174 did. **(2) R1** (`:285`): pre-flight re-derives §2.1 (`git fetch upstream`; if `upstream/main` moved or #83 merged, add a stage to R2); `git merge --no-ff --no-commit 0fd003a`; resolve rows 1, 3, 5, 10; commit; then Test 27.N1b's one-line override, then D1's follow-through in commits of at most 5 files. **R1's own claim makes 3 receipts; this close-out leaves 2** (`grep -c '^```handoff$' HANDOFFS.md`), so R1's Phase 0 does not trim. The merge brings 8 upstream receipts, so the retention trim is due at R1's end: `--cut 2` keeps R1's stub and the newest fork receipt. **(3) R2** (`:310`), **(4) BL-57's P5** (`changelog-rules-contradictions-plan.md:659`) -- after stage 3 its port may reduce to merging `bl57/changelog-rules`, a prediction for P5. **CARRIED:** BL-61 (header reserve), BL-60 (folds BL-36), BL-54 after P5, `choose_cut`. **No `FRAMEWORK_LEARNINGS.md` row was written:** that file's fate is D1, and it is 2,437 B under its growth warning. The session's learning (an arriving enforcement hook binds the test suite's own fixture commits, not only the session's) goes to whichever file D1 names.
key_files: `docs/planning/upstream-resync-2026-09-plan.md:41` (§2.1 stages and the re-conflict caveat), `:76` (§2.2, the arriving hooks and lint), `:120` (§2.3 the 13 rows), `:141` (§2.4 ledgers), `:166` (§2.5 gates), `:187` (D1–D4), `:216` (D1's trial, the three failures), `:285` (R1), `:310` (R2), `:335` (measured vs predicted); `bin/tests.sh:1281` (Test 27.N1b's commit), `:1211`, `:1692` (tests pointing `core.hooksPath` at the live hooks), `:2561` (`add_row37`'s `max + 1`); `tools/test_methodology_dashboard.py:5359` (the Learning #26 pin); `bin/check-learnings:36` (NOT a fork citation: another project's numbers); `docs/HANDOFFS_ARCHIVE_INDEX.md:51` (the fold rule, moved from `:50` by this session's row); `docs/planning/BACKLOG.md:148` (BL-53), `:152` (BL-57)
gotchas: **(1) A POSITIONAL `--cut N` DEPENDS ON WHEN IT RUNS.** S174 wrote `--cut 1` for a Phase 0 trim; after the claim stub, `--cut 1` would have archived S174's own receipt. Compare the dry run's removed bytes against the intended records (24,942 B both ways here) before `--write`. **(2) A CONFLICT SET COMPUTED AGAINST `main` IS NOT THE SET AGAINST THE PREVIOUS STAGE.** The draft guessed M3 for `.context-budget.json`'s re-conflict; `merge-tree` against the trial's M1 result showed M2. Compute against a committed stage result in a clone. **(3) A `--no-local` CLONE SEES ONLY COMMITS:** commit a resolution before testing it there (the trial did; the draft's R2 order did not). **(4) THE LIVE CHECKOUT FAILS ONE CONTEXT-BUDGET UNIT TEST THAT A CLONE PASSES** (`TestFitGateEndToEnd`, via `bin/tests.sh:267`; it reads this path's session transcripts), and Test 9 failed once on GitHub, then passed standalone and on re-run. Run gates in clones and re-run a lone Test 9 failure; never waive it. **(5) BL-57's P5 REMOVES TEST 27** with the hook's claim carve-out (`changelog-rules-contradictions-plan.md:278`, `:683`), so R1's fix to it should stay one line. **(6) ZSH AGAIN:** `$c:starter-kit/...` is a history modifier (use `${c}:`), `echo =====` is `=cmd` expansion, and `git rev-parse --short` takes one ref -- all three hit this session. A stray `cd docs/planning` also moved the session's working directory.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`,** run in `--no-local` clones with HEAD asserted equal to the source commit. **`1f34e75` (after trim and fold):** first run exit 1, 299 passed / 1 failed / 6 skipped, the failure Test 9 (`bin/sync --source=github --dry-run`); the same command standalone exit 0; **re-run exit 0, 300 passed / 0 failed / 6 skipped**, matching S174's prediction -- the 6 skips are Test 34's stated rows at 2 receipts. **`e3bc12c` (the plan):** exit 0, **300 passed / 0 failed / 6 skipped**, and a digit-masked diff of its assertion rows against `1f34e75`'s re-run is empty. **Trial (D1 (A), stage 1, throwaway clone `e856970`):** 297 / 3 / 6, and a digit-masked diff against `1f34e75`'s run shows exactly three pass->fail flips. **Other gates on fork `main`:** the shard's `.verify.sh` exit 0 at `4679cca` and after `1f34e75`; `bin/check-handoff --all --allow-pending` exit 0; `bin/check-links` exit 0 (105 links); `bin/check-learnings` exit 0 (65 rows); `methodology_trim.py --file CHANGELOG.md --check`: 165,082 B, does not fire; `context_budget.py --status` exit 2 as at Phase 0, and the one row flip is `HANDOFFS.md` warn -> ok from the trim. No `.quality-gates.json` on fork `main` yet, so no ratchet run is owed. **NOT EXERCISED:** any merge on fork `main`, the ratchet, any push or outward action, CI (none).
changelog_ref: CHANGELOG.md "2026-09-16 · [BL-57] S175 close-out", plus the claim, the trim, the fold, the re-scope decision and the plan entries
commit: 88e40f5 (claim) + 4679cca (trim) + 1f34e75 (fold) + e3bc12c (plan) + this close-out
```

**Self-assessment: 7/10.** Plus: Phase 0 computed where it could have predicted. PR #83's conflict set
and the manifest subset answered the operator's question with commands, not reasoning. I noticed the
claim stub shifts the trim's cut before running it. A failed Test 9 got a standalone reproduction and a
re-run instead of a waiver. When `merge-tree` showed a resync bigger than one session, I put that to
the operator with the precedent (`213f841` carried out a ratified plan) rather than starting to merge.
The trial of D1's recommendation found a failure no decision avoids (the arriving `commit-msg` hook
against Test 27), which R1 would otherwise have met cold. Every reviewer finding was re-run before it was
fixed. **Minus:** the draft carried 15 wrong claims to review. The worst were stage re-conflicts I
guessed at M3 when the trial clone could have computed them, a `--no-renames` count stated without a
grep, merge-result line numbers passed off as fork line numbers, and two DONE criteria that could not
pass as written. My first answer to the operator ("the planned order stays") was right about PR #83 but
did not look at the resync's own size, which changed the plan within the hour. Three zsh traps already in
memory recurred, and a stray `cd` moved the session's directory. **Reduction:** `HANDOFFS.md` 40,816 ->
15,874 B at the trim (warn -> ok). Growth: this receipt, about 9 KB of ledger entries, two backlog-row
additions, and a 31 KB plan outside any mandated read.

**Predecessor (S174): 8/10.** Its item (1) was exact: the command, the fold rule's location, and a
prediction of 300 / 0 / 6 that the re-run matched. Its 13-conflict count held, and its gotchas (2) and
(3), the anchored fence and the `docs/archive/` glob hazard, were both used here. **Not 9:** it wrote
`--cut 1` for a "Phase 0" trim without saying which receipts the cut keeps. Phase 0 is read-only apart
from the ledger backfill, and after the claim the same command would have archived S174's own receipt. It
also framed the resync as one merge session, with no sign of what `213f841`'s precedent and a look at
the hunks showed. The Learning #15/#16 collision (`pr82-review.md:369`) and the arriving hooks were
already on record, and neither reached its gotchas. Its P5 citation (`:655`) is now `:659`. **ROI:
positive.**

