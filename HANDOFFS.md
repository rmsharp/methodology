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

**Archived 1 record(s), 2026-09-19 → 2026-09-19** into [`docs/archive/HANDOFFS-through-2026-09-19-2.md`](docs/archive/HANDOFFS-through-2026-09-19-2.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/HANDOFFS-through-2026-09-19-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-19-2.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

```handoff
session: S197
date: 2026-09-19
status: pending
self_score: pending
predecessor_score: pending
active_task: **FINISH BL-43 — the `pipefail` + `grep -q` race in `bin/tests.sh`.** Chosen by the operator after Phase 0 (picker), over BL-60's planning session, BL-53 and BL-61. Two halves: **(a) RE-DERIVE THE POPULATION BY PATTERN** — the item's six enumerated line numbers (`:2591`, `:2596`, `:2605`, `:2620`, `:2864`, `:2880`) no longer point at assertions, and Test 40 postdates the enumeration, so the set is a stale sample, not a population (S196 found a seventh site by accident); **(b) FIX EACH REMAINING SITE RED-FIRST**, starting from `bin/tests.sh:3203`, the same construct on the same 97,507-character variable, measured NOT firing today only because its probe matches at line 1,082 of 1,095. The fix shape is S196's: a here-string, not a pipe. Each site needs its own proof that it still fails when it should — a capture that silently stops asserting is the failure being fixed. **Side action, approved in the same picker:** push `08c5327`..HEAD to fork `origin` (13 commits, fast-forward onto `431279b`), fork only.
what_was_done: pending
next_steps: pending
key_files: `bin/tests.sh:5` (`set -uo pipefail`, the enabling condition), `:3083`–`:3091` (S196's fixed site and the measurement beside it — the fix shape to copy), `:3203` (the same construct, measured not firing today, one reordering away); `docs/planning/BACKLOG-DETAIL.md:1055` (BL-43's body, wrong in the two ways above), `docs/planning/BACKLOG.md:139` (its index row); `starter-kit/quality_ratchet.py` (`--run`, the build-equivalent; `tests-sh-passed` floor 331)
gotchas: pending
runtime_smoke: pending
changelog_ref: CHANGELOG.md "2026-09-19 · [ad hoc] S197 claim"
commit: pending
```

```handoff
session: S196
date: 2026-09-19
status: complete
self_score: 7
predecessor_score: 9
active_task: **`CHANGELOG.md` IS TRIMMED AND THE 2026-09-14 NO-TRIM DECISION IS DISCHARGED.** `--cut 2026-09-17`, a clean day seam, moved 126 of 185 records into `docs/archive/CHANGELOG-through-2026-09-17.md` and took the live file 258,656 B → 87,463 B (`0dfca7e`); it is 99,795 B after this session's own entries, **162,349 B under the 262,144 B hard read refusal**. The cut was chosen by the operator from three measured in a `--no-local` scratch clone, not predicted. Two approved side actions are done: the owed `HANDOFFS.md` retention trim (`108cc93`) with its fold (`c5db2a7`), and the push of S195's three commits to `origin` (`de4652c..431279b`, recorded `ef121f8`). One unplanned fix, approved mid-session after its evidence: `bin/tests.sh:3083`, a BL-43 site this trim pushed over the pipe buffer (`bb2e544`). **This session's ten commits are NOT pushed;** `origin/main` is `431279b`.
what_was_done: **Phase 0:** both frontiers = HEAD `431279b`, no gap, nothing backfilled, no pending stub; gate re-run in the clean working tree read `results 6d2ca2197aa7 · manifest 61cd292c36bd`, S195's citation exactly, 337 passed at three receipts; dashboard 76/100; PR #84 open at `77afc12` with no reviews; `context_budget.py` deliberately not run (BL-75, and its default run writes a tracked row). **`08c5327`** claim. **`0dfca7e`** the trim: three cuts dry-run in a clone of `08c5327` — the computed positional one (117 records, 99,343 B, `CUT_STRADDLES_DAY`), `--cut 2026-09-16` (57, 180,719 B) and `--cut 2026-09-17` (126, 87,463 B) — the operator chose the last; `v3.7` is tagged 2026-08-12, older than every live record, so no release frontier existed and a day cut was the only boundary. L1/L2/L3 and the shipped `.verify.sh` all OK. **`b6264c8`** the decision's end recorded and the *When to archive* paragraph rewritten. **`5587240`** repair: the claim had inserted the receipt at the first `` ```handoff `` SUBSTRING — the front matter quoting its own delimiter — so it landed at `:15` inside the retention paragraph; the trimmer caught it (`CUT_OUT_OF_RANGE`, *"must retain between 1 and 1 records"*), and `bin/check-handoff --all` reports it while the default mode printed OK. **`108cc93`** the retention trim, `--cut 2` retaining S196 and S195, 39,953 B → 16,911 B, `--force` because `SRF_RED` refuses every on-schedule retention trim, `FRONTMATTER_FIELD_ABSENT` expected. **`c5db2a7`** the fold, its own commit. **`ef121f8`** the push, by sha not branch tip. **`4e457fc`** the front matter's *"every cut boundary is POSITIONAL"* sentence made true of a dated cut. **`211cae5`** the red suite investigated. **`bb2e544`** the fix, RED-first.
next_steps: **(1) PUSH THIS SESSION'S COMMITS — `08c5327`..HEAD, stated as a RANGE because any count written here is changed by the commit that writes it** (S195's gotcha (3), and it caught this receipt once already). `origin/main` is `431279b`; the push is a fast-forward. Nothing goes upstream. **(2) PR #84 IS STILL ALL THAT REMAINS OF BL-57:** `gh pr view 84 -R KJ5HST/methodology --json state,headRefOid,reviews,comments` — OPEN at `77afc12`, MERGEABLE, no reviews or comments, unchanged since 2026-09-19T04:21Z. Every reply is its own go-ahead. **(3) NO `HANDOFFS.md` TRIM IS OWED AT THE NEXT PHASE 0** — this close-out leaves **2** receipts — but that session's own claim makes three, so the trim falls due immediately after its report, and after a claim the depth is **`--cut 2`**, not `--cut 1`: `--cut N` RETAINS N records (`starter-kit/methodology_trim.py:1044` `_explicit_retain`). **(4) `CHANGELOG.md` IS 99,795 B, 162,349 B UNDER THE REFUSAL** — roughly 17 sessions at S195's ~9,500 B, an estimate and not a measurement. The rule that now governs is in its front matter (`:116`): a trim is raised as the file approaches the refusal, never after it. **(5) BL-43 IS OPEN AND ITS ITEM BODY IS WRONG IN TWO WAYS** (not edited, per the backlog convention; corrected in the ledger): its six enumerated line numbers no longer point at assertions, and Test 40 postdates the enumeration. Re-derive by pattern. `bin/tests.sh:3203` is the same construct on the same 97,507-character variable and was measured NOT firing today (its probe matches at line 1,082 of 1,095, reporting 0/3) — it is one reordering away. **(6) BL-53 NOW HOLDS FOUR MORE WITHHELD CANDIDATES** (named in this session's close-out entry); `docs/FORK_LEARNINGS.md` is 81,721 of 81,920 B. **(7) BL-74 AND BL-75 ARE STILL UNDECIDED** — BL-74 which `README.md`, BL-75 whether the `--status` fix goes upstream (its own go-ahead). **CARRIED:** BL-73, BL-54's own PR, the `vscode_quarto_ext` relay (S191 (3)), BL-68, BL-61, BL-60, BL-65, BL-66, `model_project_constructor`'s push and its bare-`ruff` regression, `airqino`'s `HANDOFFS.md` migration in its own repository.
key_files: `CHANGELOG.md:62` (the cut-boundary sentence, now true of a dated cut), `:116` (*When to archive*, the rule that outlived the no-trim decision), `:206` (the trim's pointer block); `docs/archive/CHANGELOG-through-2026-09-17.md` and its `.verify.sh` (anchored to `0dfca7e`); `HANDOFFS.md:8` (the retention policy) and `:14` (the line that quotes the receipt delimiter — the one that ate the claim); `docs/HANDOFFS_ARCHIVE_INDEX.md:60` (the folded row); `bin/tests.sh:5` (`set -uo pipefail`), `:3083`–`:3091` (the fixed assertion and the measurement beside it), `:3203` (the same construct, not firing today); `starter-kit/methodology_trim.py:1044` (`--cut N` retains N)
gotchas: **(1) `HANDOFFS.md` QUOTES ITS OWN FENCE DELIMITER IN THE FRONT MATTER (`:30`), SO A WRITE MUST ANCHOR TO LINE START.** `str.index('```handoff')` put this session's claim receipt inside the retention paragraph. What did NOT catch it: `bin/check-handoff`, which validated S195 as newest and printed OK. What did: the trimmer's record parser, and `bin/check-handoff --all`. **Read back the region you wrote, or run `--all`, before believing a checker's OK.** **(2) A RED SUITE IS A CLAIM ABOUT AN ASSERTION AS MUCH AS ABOUT THE TREE.** Test 40's shard-set check called three real, tracked, present-in-the-report shards *"unnamed"*; the tell was that it named the ones printed EARLIEST. Re-running is not enough — it reproduced 3/3 at `211cae5` — the control is re-testing the subject without the pipe (`grep -qF … <<< "$VAR"`). **(3) THE RACE IS SHELL-SPECIFIC:** under zsh the same loop reports 0 unnamed 5/5, under bash 3 false positives 3/3. `bin/tests.sh` runs under bash; a check you run by hand in this terminal runs under zsh. **(4) `--cut N` RETAINS N RECORDS.** S195's *"`--cut 1 --force`"* was right for a trim taken BEFORE the Phase 1B claim and would have archived S195 after it. **(5) THE TRIMMER WRITES ITS OWN LEDGER ENTRY** (`P1A_OK: ledger gained exactly one entry`), so a trim commit already carries its `CHANGELOG.md` line — do not add a second. **(6) `.quality-gates-results.json` IS GITIGNORED,** so Phase 0's citation check is a `--run`, never a file read.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `quality_ratchet.py --run` IN A `--no-local` CLONE WITH HEAD ASSERTED, SUITE OUTPUT SAVED.** **Citation, clone of `bb2e544`: `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results a5197f8a439f · manifest 61cd292c36bd`**, with `bash bin/tests.sh` 331 passed / 0 failed / 6 skipped at two receipts (Test 34's six stated SKIPs), captured to a file. Before the fix, the same clone read `8/10 · results 57f06751b3b9`, 330/1/6, three times running. Both shard proofs re-run after their trims: `docs/archive/CHANGELOG-through-2026-09-17.md.verify.sh` and `…/HANDOFFS-through-2026-09-19.md.verify.sh` print L1/L2/L3 OK; `bin/check-links` 111 across 23 files; `bin/check-learnings` 15 rows contiguous 1..16. **NOT EXERCISED:** this close-out commit itself (BL-64), and PR #84's review.
changelog_ref: CHANGELOG.md "2026-09-19 · [ad hoc] S196 close-out", plus the claim, the trim, the decision's end, the repair, the retention trim, the fold, the push record, the cut-boundary correction, the BL-43 finding and the fix
commit: 08c5327 (claim) + 0dfca7e (trim) + b6264c8 (decision's end) + 5587240 (repair) + 108cc93 (retention trim) + c5db2a7 (fold) + ef121f8 (push record) + 4e457fc (boundary sentence) + 211cae5 (BL-43 finding) + bb2e544 (fix) + this close-out
```

**Self-assessment: 7/10.** Plus: every cut was run in a `--no-local` clone before a byte was written here, and the
operator chose from three measured options rather than one proposal; both trims' proofs were re-run rather than cited;
the always-read front matter was left true in two separate places instead of carrying a decision that had ended; the
approved push went by sha, so this session's commits did not ride a go-ahead given for S195's; and the red gate was
chased to a demonstrated mechanism — with a control and a RED-first proof — instead of being re-run until it passed.
**Minus:** (1) I corrupted `HANDOFFS.md` in the claim commit by writing at a substring in the one file that quotes its
own delimiter, a trap my own notes name, and then accepted `bin/check-handoff`'s OK as confirmation when it had
validated a different receipt. (2) My first attribution of the red suite — *"a flake, re-run it"* — was committed
(`211cae5`) before I had a control, and was wrong about the shape: it reproduced 3/3. The correction is in the ledger,
but a session ahead of its evidence is what the correction cost. (3) The Phase 0 gate ran in the working tree rather
than in a clone; harmless with a clean tree at HEAD, but it is not the documented build-equivalent.

