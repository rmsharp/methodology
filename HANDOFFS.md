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

**Archived 1 record(s), 2026-09-20 → 2026-09-20** into [`docs/archive/HANDOFFS-through-2026-09-20-12.md`](docs/archive/HANDOFFS-through-2026-09-20-12.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/HANDOFFS-through-2026-09-20-12.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-20-12.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

```handoff
session: S211
date: 2026-09-21
status: pending
active_task: **BL-80 — P2 of [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md) §5 (D3): the growth-run advisory's second sentence is chosen by `worst`, the headline's own variable, so it never says "Nothing is over a ceiling" beside a table with a row `over`.** Three tests RED first against `e859196`, the "restore the literal" mutant run. One commit on the LOCAL branch `fix/context-budget-status`, built in a `--no-local` clone of that branch and fetched back here; nothing pushed, nothing upstream-facing (P4's go-ahead). Chosen at this session's Phase 0 picker over BL-78's closing edits. **Side actions approved at the same picker:** the `HANDOFFS.md` retention trim this receipt makes owed (three receipts, `--cut 2 --force`) and its fold; pushing fork `main` to `origin` at close-out.
commit: pending
```

```handoff
session: S210
date: 2026-09-21
status: complete
self_score: 8
predecessor_score: 8
active_task: **P1 OF THE `context_budget.py` PLAN IS BUILT AND VERIFIED: ONE COMMIT, `e859196`, ON THE LOCAL BRANCH `fix/context-budget-status` (FROM `upstream/main` `6b29d3d`). IT IS NOT PUSHED, AND NOTHING IS UPSTREAM-FACING. NEXT: THE PLAN'S P2 (BL-80, the advisory), ON THE SAME BRANCH.** The plan is [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md). What changed: `--status`, with or without `--json`, is now the default run without its history append (same ledger, same exit code). An argument outside `ACCEPTED_ARGUMENTS` exits 3 before the tree is read (`-h`/`--help` still win). `VERSION` goes 1.2.0 → 1.3.0. Tool blob `b1111d92` → `131158cb`. **Three departures from the plan's text, all recorded in its new *P1 outcome* block (`:328`) and none approved in advance:** the accepted list is module-level, not *"a literal in `main()`"* (§4.1 amended); there is an eighth test; and there are four mutants, not three. The cause is a false plan claim: none of the three existing `--force` guards can see a list inside `main()`. BL-75 stays open until the PR merges. **#83, #84, #85: still no maintainer response; nothing owed upstream.** Side actions, approved at the Phase 0 picker: the `HANDOFFS.md` retention trim and its fold, and the fork push after this commit, with its record following.
what_was_done: **Phase 0:** `CHANGELOG.md` frontier = HEAD `cadd8a0`, gap empty; `HANDOFFS.md` frontier `e1795a0`, the one commit after it being S209's announced push record. No pending stub, 2 receipts; nothing backfilled. Gate citation **re-run** in a `--no-local` clone at `cadd8a0`, HEAD asserted: S209's exactly. Dashboard 76/100, medium, 0 high+. Upstream: 0 issues; #83/#84/#85 heads `219fb9d`/`77afc12`/`e2501c5`, 0 reviews, only our comments; `upstream/main` still `6b29d3d`. **`e4d7c84`** the claim. **`19d9e42`** the retention trim (`--cut 2 --force`, dry run first, 24,049 → 15,859 B, shard **-11**; SRF, CUT_STRADDLES_DAY, SHARD_NAME_DISAMBIGUATED and FRONTMATTER_FIELD_ABSENT, all expected). Its `.verify.sh` gave **L1/L2/L3 OK, exit 0** in a clone at `19d9e42`. **`f1fa0a4`** the fold; `bash bin/tests.sh` in a clone at `f1fa0a4`: **343 / 0 / 6 skipped**. **P1, in a `--no-local` clone with `core.hooksPath` set:** 7 tests and 2 shell rows written first, **RED against `b1111d92`**: 5 of 7 unit tests failed and 2 controls passed; the suite gave **138 / 3** (both rows and the unit row). Then the fix. **Mutants run:** (M1) the unconditional append was killed by 3 unit tests and row 1. (M2) Removing the rejection was killed by 2 unit tests and row 2. **(M3) `--force` added to the list was NOT caught by the selftest.** My own comment above the list named `def selftest`, so the check's `split` point moved and it read only lines 1–55. I fixed the comment and added an eighth test pinning the split point. That test first asserted `count == 1`, which is false on the fixed tool because the check's own literal is a second mention. Running the fixed baseline through the same harness showed its "kills" were spurious. It now asserts that the first mention is the definition. **Final:** 6 of 8 RED on `b1111d92`. All four mutants killed: M3 by tests 5 and 6 and the selftest; M4 (comment plus `--force`) by tests 5, 6 and 8. Neither `"--force" in args` grep catches either. `e859196` was committed with one upstream-format `CHANGELOG.md` entry (`[ad hoc]`, scanned for fork jargon: 0 hits). It was fetched back here as a local branch with no remote tracking. **Verified in a fresh `--no-local` clone of that local branch, HEAD asserted:** 126 unit tests OK (118 + 8, 2 skipped); `--selftest` 52 PASS, exit 0; the grep empty; `bin/tests.sh` **141 / 0**; upstream's ratchet `10/10 pass · results 37bbefc55e64 · manifest 97a7aab85b9a`. **`c8e5cae`** the plan's P1 outcome block, the §4.1 amendment and the status line, BL-75's S210 detail paragraph and the BL-75/BL-80 index rows; `BACKLOG-DETAIL.md.verify.sh` C1–C5 OK. **Phase 3C:** no fork-learnings row. The lesson (a `split`-on-token guard is narrowed by any earlier mention, including a comment explaining the guard) is now enforced by the eighth test, and a mechanical lesson is a gate, not a row. It went to agent memory as an update to the existing self-matching-guard entry. D3's retirement obligation does not arise.
next_steps: **(1) THE PLAN'S P2 — BL-80, THE ADVISORY (D3), ONE SESSION** (`docs/planning/context-budget-status-plan.md:357`). **Cut the clone from THIS REPOSITORY'S LOCAL BRANCH, not from `upstream/main`:** `git clone --no-local --branch fix/context-budget-status /Users/rmsharp/Development/methodology <scratch>`, assert HEAD = `e859196`, then `git config core.hooksPath .githooks` before the first commit. Line numbers on `e859196` (`:352`): the advisory is `starter-kit/context_budget.py:661-663`, `worst` is `:594-605`, and `render()` is `:591`. New tests go after `tools/test_context_budget.py:615`, before `TestTokenCeiling` (`:618`). The byte-identity witness is `:1063`. Write the three §5 P2 tests RED first. Run the "restore the literal" mutant. Add one upstream `CHANGELOG.md` entry above `CHANGELOG.md:38`, with no fork jargon. Then `git fetch <clone> fix/context-budget-status:fix/context-budget-status` here (a fast-forward), and verify in a fresh clone of that branch: unit 126 + k, `bin/tests.sh` 141 + k / 0. **(2) THEN P3** (vet: `merge-tree` against #84/#85/#83, and tighten upstream's `tests-sh-passed` and `context-budget-unit-tests` floors, currently 139 and 118, to the values measured after P2; the PR body for the operator's review), **P4** (outward: a go-ahead on the exact body AND on pushing the branch to `origin`), **P5**, each its own session. **(3) AT PHASE 0, CHECK #83/#84/#85:** #83 1 comment (ours, `5755256040`), head `219fb9d`; #84 1 comment (ours), head `77afc12`; #85 0 comments, head `e2501c5`. A reply is new work with its own go-ahead. **(4) THE NEXT CLAIM MAKES THREE `HANDOFFS.md` RECEIPTS**: trim (`--cut 2 --force`) and fold right after its Phase 0 report; this has held ten times. **(5) NO `CHANGELOG.md` TRIM OWED:** 102,035 B measured with this close-out's entry (the push record adds under 1 KB), 94,573 B under the 196,608 B trigger. **(6) STILL OWED, UNCHANGED:** BL-78's closing edits as their own session (`docs/planning/BACKLOG.md:166`, the archive move, `.context-budget.json:101` `files[4]._`); BL-81, BL-79, BL-77 and BL-74 undecided. **CARRIED:** S206's list.
key_files: **Branch `fix/context-budget-status` @ `e859196` (local only):** `starter-kit/context_budget.py` `VERSION` `:41`, `ACCEPTED_ARGUMENTS` `:51-59` (comment and literal), `print_usage` `:1300` (`--status` line `:1309`), `main` `:1327` (rejection `:1331-1336`), append guard `:1394-1397`, advisory `:661-663`, `worst` `:594-605`; `tools/test_context_budget.py` frozen set `:499`, `TestCommandLine` `:503-615`, witness `:1063`; `bin/tests.sh` new rows `:675-696`; `CHANGELOG.md:38` (the upstream entry). **Fork `main`:** `docs/planning/context-budget-status-plan.md` status `:4-6`, §4.1 `:261`, P1 outcome `:328`, P2's lines `:352`, P2 `:357`, P3 `:370`, P4 `:388`; `docs/planning/BACKLOG-DETAIL.md:2688` (BL-75's S210 paragraph); `docs/planning/BACKLOG.md:164` (BL-75), `:168` (BL-80); `docs/HANDOFFS_ARCHIVE_INDEX.md:74` (last row = shard **-11**).
gotchas: **(1) THE BRANCH EXISTS ONLY HERE:** `fix/context-budget-status` is a local branch in `/Users/rmsharp/Development/methodology`, with no remote. The scratch clone that built it is gone with this session. Do not delete the branch or `git gc --prune` its only commit, and clone P2 from it, not from `upstream/main`. **(2) A SOURCE-GREP GUARD'S `split("def selftest")` CUTS AT THE FIRST MENTION.** Never name that definition in a comment above it; the eighth test now refuses it. `def selftest` legitimately appears twice (the definition at `:1116` and the check's own literal at `:1293`, on the branch), so a count assertion is false. **(3) RUN THE FIXED BASELINE THROUGH THE MUTANT HARNESS FIRST.** A test failing on the fixed tool scores every mutant as "killed". **(4) THE TWO `"--force" in args` GREPS GUARD ONE EXPRESSION ONLY**, not a `--force` in a list. The selftest is the only existing guard that sees the list. **(5) SHELL ROW 2 COMPARES AGAINST THE TREE AFTER `--status`, NOT AGAINST EMPTY**, so a `--status` write shows in row 1 alone. Keep it so. **(6) zsh `"$B:starter-kit/…"`** (the `:s` modifier) bit again; brace it as `"${B}:path"`. **(7) `bin/check-handoff` READS EACH FIELD AS ONE LINE.** **(8) `HANDOFFS.md`'s front matter still says `--cut 1 --force`**, wrong through ten trims now. **`CHANGELOG.md` HAS NO FOLD.**
runtime_smoke: **THE APPLICATION IS THE TOOL, AND IT WAS RUN:** on the branch, in fresh `--no-local` clones with HEAD asserted by sha, through 8 subprocess unit tests and 2 `mktemp` adopter-shaped shell rows (seed config, committed project). **Citation, branch clone of `e859196` (upstream's gates):** `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results 37bbefc55e64 · manifest 97a7aab85b9a`, with `tests-sh-passed` 141 (floor 139) and `context-budget-unit-tests` 126 (floor 118). **Citation, fork `main` clone of `c8e5cae`:** `quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results 10575dac7361 · manifest 01a4ae7aa511`, identical to Phase 0 since no fork gate moved; `bash bin/tests.sh` **343 / 0 / 6 skipped** there. Also green: the trim's `.verify.sh` (L1/L2/L3, exit 0); `BACKLOG-DETAIL.md.verify.sh` C1–C5; `bin/check-links` 111 links / 23 files. **NOT EXERCISED:** a real adopter's hook or history file (P5); upstream's own clones beyond this branch (P3); the advisory (P2); this close-out commit itself (BL-64).
changelog_ref: CHANGELOG.md "2026-09-21 · [BL-75] S210 claim", the `HANDOFFS.md` trim (written by the trimmer), "[ad hoc] S210 — `HANDOFFS.md`: the trim's pointer block folded into the shard index", "[BL-75] S210 — P1 built: `e859196` on the LOCAL branch", "[BL-75] S210 — the plan's P1 outcome recorded", and this close-out
commit: e4d7c84 (claim) + 19d9e42 (HANDOFFS trim) + f1fa0a4 (fold) + e859196 (P1, local branch fix/context-budget-status) + c8e5cae (plan + backlog) + this close-out
```

