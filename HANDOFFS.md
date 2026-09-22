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

**Archived 1 record(s), 2026-09-21 → 2026-09-21** into [`docs/archive/HANDOFFS-through-2026-09-21-5.md`](docs/archive/HANDOFFS-through-2026-09-21-5.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/HANDOFFS-through-2026-09-21-5.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-21-5.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

```handoff
session: S216
date: 2026-09-21
status: pending
active_task: **BL-78's CLOSING EDITS, ONE SESSION, FORK-LOCAL** (decided S206: P3 = no enforcement, so the item closes; `docs/planning/BACKLOG-DETAIL.md:3019-3023`). Rewrite the stale index row `docs/planning/BACKLOG.md:166`, move BL-78 to Completed items per the backlog's convention, and correct `.context-budget.json:101` (`files[4]._`), whose *"every commit that grows it is refused"* describes a refusal nothing calls — a comment edit, no threshold changed. Chosen at this session's Phase 0 picker, where no maintainer reply was found on #83–#86. **Side actions approved at the same picker:** the `HANDOFFS.md` retention trim this receipt makes owed and its fold; pushing fork `main` to `origin` at close-out.
commit: pending
```

```handoff
session: S215
date: 2026-09-21
status: complete
self_score: 9
predecessor_score: 9
active_task: **P4 OF THE `context_budget.py` PLAN IS DONE: `fix/context-budget-status` IS ON FORK `origin` AT `c1167ae`, AND THE UPSTREAM PR IS OPEN AS [#86](https://github.com/KJ5HST/methodology/pull/86) WITH THE TEXT APPROVED AT S214 POSTED UNCHANGED. THE PLAN'S NEXT PHASE, P5 (fork-side adoption), WAITS FOR THE UPSTREAM MERGE; BL-75 AND BL-80 STAY OPEN UNTIL THEN.** Read back: open, not a draft, head `c1167ae`, 6 commits, 5 files, +631 / −11, the title and body equal to [`docs/planning/context-budget-status-pr-body.md`](docs/planning/context-budget-status-pr-body.md) (`:12`, `:16` onward), `mergeable_state: clean`. **Four PRs from this fork are open upstream (#83, #84, #85, #86), none reviewed, no maintainer reply: nothing owed upstream.** Side actions approved at the Phase 0 picker: the `HANDOFFS.md` trim and fold (done) and the fork push after this commit, with its record following.
what_was_done: **Phase 0:** `CHANGELOG.md` frontier = HEAD `58f5d34`, gap empty; `HANDOFFS.md` frontier `1b5365e`, the one commit after it S214's announced push record; no pending stub, 2 receipts; nothing backfilled. Gate citation re-run in a `--no-local` clone at `58f5d34`: S214's exactly. Dashboard 76/100, medium, 0 high+ (in that clone). Upstream 0 issues; #83/#84/#85 unchanged, 0 reviews. Both heads unchanged since S214 (`upstream/main` `6b29d3d`, branch `c1167ae`), and the body from `:16` `cmp`-equal to `fb324d6`'s, so no figure needed re-measuring. **Picker (multiSelect):** P4, the trim + fold, the fork push, all three approved. **`0b3e355`** the claim. **`fc1f05a`** the retention trim (`--cut 2 --force`, dry run first, 29,010 → 17,666 B, shard `HANDOFFS-through-2026-09-21-4.md`, S213's receipt; SRF, CUT_STRADDLES_DAY, SHARD_NAME_DISAMBIGUATED, FRONTMATTER_FIELD_ABSENT, as S214 predicted); its `.verify.sh` L1/L2/L3 OK, exit 0 read bare, in a clone at `fc1f05a`. **`b4d22c4`** the fold (→ 17,210 B). `bash bin/tests.sh` in a clone at `b4d22c4`: the first run 342 / 1 / 6, the one failure Test 9 (the `--source=github` dry run: 4 of 29 fetches hit `TLS handshake timeout`, the same network that timed out one `upstream` fetch this session); **re-run alone in a fresh clone: 343 / 0 / 6**, S214's figure. **P4:** the queue and both heads re-checked right before the push (unchanged). `git push -u origin fix/context-budget-status` (a new branch; `ls-remote` = `c1167ae`). The title and body were extracted by a script that asserted `:12`'s label, `:14`'s rule and `:16`'s opening words, then `cmp`-checked against `fb324d6`; `gh pr create -R KJ5HST/methodology --base main --head rmsharp:fix/context-budget-status` from those files → **#86**. Read back by `gh pr view` and the REST API: OPEN, head `c1167ae`, 6 commits, 5 files, +631 / −11; body equal apart from the trailing newline; title identical; `mergeable: true`, `maintainer_can_modify: true`. **`34011a7`** the records: the plan's status block and *P4 outcome*, the body file's preamble (kept to three lines so `:12` and `:16` hold; the body still `cmp`-equals the posted text), the BL-75/BL-80 rows and detail, two non-commit ledger entries (the push, the PR); `BACKLOG-DETAIL.md.verify.sh` C1–C5 OK, `bin/check-links` OK. **Phase 3C:** no fork-learnings row, so D3's retirement obligation does not arise.
next_steps: **(1) AT PHASE 0, CHECK ALL FOUR PRs FOR A MAINTAINER RESPONSE:** `gh pr list -R KJ5HST/methodology`; heads #83 `219fb9d`, #84 `77afc12`, #85 `e2501c5`, #86 `c1167ae`; our comments `5755256040` (#83) and `5753335477` (#84); #85 and #86 none. A reply (review, comment, merge, close) ranks first and is new work with its own go-ahead. #86 merging unlocks **P5** (`docs/planning/context-budget-status-plan.md:746`). **(2) IF NO REPLY: BL-78's CLOSING EDITS, ONE SESSION, FORK-LOCAL.** Decided at S206 (no enforcement, so the item closes; `docs/planning/BACKLOG-DETAIL.md:3019-3023`): rewrite the stale index row `docs/planning/BACKLOG.md:166`, move the item to closed per the backlog's own convention, and correct `.context-budget.json:101` (`files[4]._`, `starter-kit/SESSION_RUNNER.md`), whose *"every commit that grows it is refused"* describes a refusal nothing calls. That is a comment edit and changes no threshold, and the pre-commit ratchet runs on it. **(3) OR** have the operator decide one of BL-81, BL-79, BL-77, BL-74 (undecided; index rows in `docs/planning/BACKLOG.md`). Do not start a fifth upstream PR while four sit unreviewed without asking: the maintainer's review time is the scarce resource (`CLAUDE.md` §Contributing upstream). **(4) THE NEXT CLAIM MAKES THREE `HANDOFFS.md` RECEIPTS:** trim (`--cut 2 --force`, dry run first) and fold right after its Phase 0 report. The receipt it archives is S214's, dated 2026-09-21, so the shard name will disambiguate to `-5`. **(5) NO `CHANGELOG.md` TRIM OWED:** 161,641 B with this close-out's entry, measured; about 162 KB after the push record (an estimate), about 34 KB under 196,608 B. **CARRIED:** S206's list.
key_files: **Fork `main`:** `docs/planning/context-budget-status-plan.md` status `:4-19` (P4 at `:17`), P4 `:721`, **P4 outcome `:731`**, P5 `:746` (the `wsfct` line `:755-757`); `docs/planning/context-budget-status-pr-body.md` preamble `:8-10` (posted as #86), title `:12`, body `:16` to end (= the posted text); `docs/planning/BACKLOG.md:164` (BL-75), `:166` (BL-78), `:168` (BL-80); `docs/planning/BACKLOG-DETAIL.md:2726` (BL-75's S215 paragraph), `:3133` (BL-80's), `:2853` (BL-78), `:3019-3023` (BL-78's S206 decision); `.context-budget.json:101` (BL-78's stale sentence); `docs/HANDOFFS_ARCHIVE_INDEX.md:79` (last row = `HANDOFFS-through-2026-09-21-4.md`); `CHANGELOG.md:222` (this close-out), `:262`, `:272`, `:285` (the P4 records, the PR, the push). **Upstream:** https://github.com/KJ5HST/methodology/pull/86, head `rmsharp:fix/context-budget-status` = `c1167ae`, base `main` = `6b29d3d`.
gotchas: **(1) #86's BODY IS THE FILE FROM `:16`:** change the posted text only with `gh api -X PATCH repos/KJ5HST/methodology/pulls/86 -F body=@<file>` (`gh pr edit` fails on Projects-classic), then update the file, the plan and the ledger, and read it back. **(2) THE BRANCH IS NOW PUBLIC AND IS #86's HEAD:** do not rebase or force-push `fix/context-budget-status`. The body promises *"I will merge `main` into the branch"* after whichever open PR merges first: a merge commit, not a rebase. **(3) THE NETWORK WAS FLAKY THIS SESSION:** one `upstream` fetch and 4 of Test 9's 29 GitHub fetches timed out (TLS handshake). Treat a lone Test 9 failure as environmental and re-run the suite alone before taking a number from it. An `&&` chain stops silently at a failed fetch, so read each command's exit. **(4) `bin/check-links` IS PYTHON:** run `./bin/check-links`; `bash bin/check-links` fails with `import: command not found`. **(5) zsh:** an unquoted `echo ====` fails (`=== not found`); quote it. **(6) `bin/check-handoff` READS EACH FIELD AS ONE LINE,** and the receipt budget is 12,288 B. **(7) `HANDOFFS.md`'s front matter still says `--cut 1 --force`**, wrong through fifteen trims now. **`CHANGELOG.md` HAS NO FOLD.**
runtime_smoke: **THE DELIVERABLE IS THE OPEN PR, AND IT WAS READ BACK:** `gh pr view 86` and `GET /pulls/86` (state, head, commits, files, lines, mergeability), with the body and title compared to the files by script: equal. No byte of the branch changed since S214 verified it at `c1167ae` (upstream's gates `10/10 · results 8a465ec9a35d · manifest ca680a8b0c9f`, trial merges green), so the branch was not re-verified here. **Citation, fork `main` clone of `34011a7`:** `quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results 10575dac7361 · manifest 01a4ae7aa511`, identical to Phase 0 (`tests-sh-passed` 343). Also green: `bash bin/tests.sh` 343 / 0 / 6 skipped at `b4d22c4` (the re-run); the trim's `.verify.sh`; `BACKLOG-DETAIL.md.verify.sh` C1–C5; `bin/check-links`. **NOT EXERCISED:** GitHub's merge (upstream has no CI); the maintainer's reading; P5; this close-out commit itself (BL-64).
changelog_ref: CHANGELOG.md "2026-09-21 · [BL-75] S215 claim", the `HANDOFFS.md` trim (written by the trimmer), "[ad hoc] S215 — `HANDOFFS.md`: the trim's pointer block folded", "[BL-75] S215 — P4: `fix/context-budget-status` pushed to fork `origin`", "[BL-75] S215 — P4: upstream PR #86 opened with the approved text", "[BL-75] S215 — P4's outcome recorded", and this close-out
commit: 0b3e355 (claim) + fc1f05a (HANDOFFS trim) + b4d22c4 (fold) + 34011a7 (P4 records) + this close-out
```

