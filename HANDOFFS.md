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

**Archived 1 record(s), 2026-09-20 → 2026-09-20** into [`docs/archive/HANDOFFS-through-2026-09-20-4.md`](docs/archive/HANDOFFS-through-2026-09-20-4.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/HANDOFFS-through-2026-09-20-4.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-20-4.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

```handoff
session: S203
date: 2026-09-20
status: pending
active_task: **BL-78 costing** — settle *"which number is right now"* for the two read-set pins, `starter-kit/SAFEGUARDS.md` (17,129 B against a declared 15,386 B) and `starter-kit/SESSION_RUNNER.md` (55,406 B against a declared 54,363 B), by costing the item's three named shapes: re-pin, wire a gate, or treat the rows as a reported series. **Planning session — the costed decision in [`docs/planning/BACKLOG-DETAIL.md`](docs/planning/BACKLOG-DETAIL.md) is the deliverable; `.context-budget.json` is not edited.** Chosen by the operator at this session's Phase 0 picker over BL-79's costing and BL-77's. Side actions approved in the same picker: the owed retention trim of this file with its fold, and a scoping-only costing of the approaching `CHANGELOG.md` trim.
commit: pending
```

```handoff
session: S202
date: 2026-09-20
status: complete
self_score: 8
predecessor_score: 9
active_task: **BL-53 P5 IS DONE AND BL-53 IS CLOSED.** `.context-budget.json`'s `docs/FORK_LEARNINGS.md` entry (`files[3]._`) now states ratified option C in the one artifact still calling the 81,920 B figure a warning to be answered: **a reported series, not a limit** (`9db2c18`). Chosen by the operator after Phase 0 (picker) over BL-78's costing and BL-77's. **P1–P5 are all done, so the backlog row moved to Completed items** (`fc4a006`) with its own limits stated. Three side actions approved in the same picker and all done: the owed retention trim with its fold, the Phase 3C row with its D3 statement, and the fork push.
what_was_done: **Phase 0:** `CHANGELOG.md` frontier = HEAD `13ed767`, gap empty; `HANDOFFS.md` frontier `b0cc32b` with only the push record above it, already ledgered — nothing backfilled, no pending stub, **2** receipts. **The gate was re-run, not read:** `.quality-gates-results.json` was still S195's (head `431279b`, manifest `61cd292c36bd`, **ten** gates, six sessions stale), so a `--no-local` clone with HEAD asserted by sha gave `11/11 · results 10575dac7361 · manifest 01a4ae7aa511`, **S201's citation exactly**. Dashboard 76/100, medium, 0 high+. Upstream has **0 open issues**; #85, #84, #83 open and unreviewed. **`2faff89`** claim (carrying `dashboard_history.jsonl`, per S201's gotcha — no amend was needed). **`1273a90`** the owed trim (`--cut 2 --force`, 24,511 → 15,074 B; SRF / CUT_STRADDLES_DAY / SHARD_NAME_DISAMBIGUATED / FRONTMATTER_FIELD_ABSENT all stated and expected; L1/L2/L3 OK) and **`eb3576d`** its fold in its own commit. **`9db2c18`** the deliverable. **`fc4a006`** BL-53 closed. **`7bdc97e`** fork Learning **#86**. **`4504996`** a correction to the deliverable, found by measurement. **TWO CLAIMS IN THE OLD NOTE FAILED VERIFICATION AND WERE CORRECTED RATHER THAN CARRIED FORWARD.** `bin/_manifest.py` has **no** row for `docs/FORK_LEARNINGS.md` (`grep -c` = 0); its `:38` distributes `starter-kit/FRAMEWORK_LEARNINGS.md`, so the note's *"adopters … receive the file itself"* entered **true** at `a51d848` (S159, about the distributed file) and became **false** at `8cfaf0d` (S176), the re-point that never touched it — 26 sessions. And *"no `.quality-gates.json` gate reads budget status"* needed narrowing: four `budget` hits exist there, three prose and one the gate `context-budget-unit-tests`, which runs the tool's **unit suite**, not this repo's measurement. **A THIRD CLAUSE WAS WRONG IN MY OWN DRAFT AND IS FIXED IN `4504996`:** BL-75's *"the default run appends a tracked history row"* is true only when a measured size **changed** (`append_history`, `starter-kit/context_budget.py:506`) — three runs this session left **one** row. BL-75's detail records the narrowing, nothing above it edited.
next_steps: **(1) BL-53 IS CLOSED; DO NOT RE-OPEN IT TO TIDY IT.** What is deliberately unfinished is named in the closure block: **no row has ever been retired**, so D2's mechanism rests on S199's E2 experiment rather than on use; option **B** stays declined and **not foreclosed**; and **D3 is held by prose and close-out discipline, not by a gate** (P4's gate half was conditional on a *mechanical* D4, and C is not one). If a close-out is ever seen appending a row without the retire-or-state line, that is the first thing to revisit. **(2) THE TWO UNCOSTED ITEMS ARE BL-78 AND BL-77, AND BL-78 IS THE BIGGER ONE.** Both read-set files now exceed the sizes their own entries declare (`SAFEGUARDS.md` 17,129 / 15,386 B; `SESSION_RUNNER.md` 55,406 / 54,363 B) and **there is no per-file growth check to wire** — shape (2) must build one. BL-77 (are the hooks armed in *this* clone) is three shapes, none costed. **(3) `context_budget.py` EXITS 2 ON THIS TREE AND NOTHING CONSUMES THAT EXIT CODE** — measured bare this session. That is BL-78's whole point in one sentence, and it is now written into the config note. **(4) PR #84's BALL IS WITH THE MAINTAINER** and its comment offers to split it into three; accepting is a **new go-ahead** and a session of its own. **#85 (`e2501c5`) AND #83 REMAIN UNREVIEWED AND UNCHASED** — each its own go-ahead. Upstream has **0 open issues**. **(5) BL-74 AND BL-75 REMAIN UNDECIDED**; BL-75 is now *narrower* than it read, not larger. **(6) NO `HANDOFFS.md` TRIM IS OWED AT THE NEXT PHASE 0** — this close-out leaves **2** receipts — **but that session's claim makes three, so it falls due right after its report, at `--cut 2`** (`--cut N` RETAINS N). Raise it in the Phase 0 picker. This prediction is the one S201 made and it held exactly. **(7) `CHANGELOG.md` IS 204,924 B BEFORE THIS ENTRY, 57,220 B UNDER THE 262,144 B REFUSAL**; it grew **12,736 B** this session. At that rate the refusal is roughly four sessions away — **a `CHANGELOG.md` trim is the thing most likely to fall due next.** **(8) `docs/FORK_LEARNINGS.md` IS 89,603 B / 72 ROWS**, above a figure that is now a reported series and no longer a breach of anything. **CARRIED:** BL-73, BL-54's own PR, the `vscode_quarto_ext` relay, BL-68, BL-61, BL-60, BL-65, BL-66, BL-69, BL-70, BL-71, `model_project_constructor`'s push and its bare-`ruff` regression, `airqino`'s `HANDOFFS.md` migration in its own repository.
key_files: `.context-budget.json:92` (`files[3]._` — **the deliverable**; read it before re-deriving what the number means, and note `max_bytes` on `:81` is still **81920** by design); `docs/planning/BACKLOG.md:172` (BL-53's row, now in **Completed items**, not Open) and `:169` (the heading list it was added to); `docs/planning/BACKLOG-DETAIL.md:1651` (the closure block and its stated limits) and BL-75's tail (the measured narrowing); `docs/FORK_LEARNINGS.md:98` (row **#86**, 1,405 B); `CLAUDE.md:38`/`:45`/`:52` (D3, D1's limbs, the ceiling's standing — unchanged this session); `starter-kit/context_budget.py:506` (`append_history`, which writes only on change), `:398` (`measured_bytes`, its only use); `bin/_manifest.py:38` (the row that distributes **upstream's** file, not this fork's).
gotchas: **(1) A PIPED `$?` REPORTS THE PIPE'S LAST COMMAND, AND I READ ONE WRONG BEFORE CATCHING IT.** `python3 starter-kit/context_budget.py | head -40; echo $?` printed **0**; run bare, the tool exits **2**. I nearly wrote "exit 0" into the deliverable's own verify line. Redirect to a file and read `$?` on the next line. **(2) `bin/check-learnings` WITH NO ARGUMENTS CHECKS THE DISTRIBUTED FILE, NOT THIS ONE.** Use `--file docs/FORK_LEARNINGS.md --first 15 --no-citations`; the bare form is what the gate runs and it is green for a different table. **(3) `--cut N` RETAINS N.** **(4) EDIT `.context-budget.json` BY REPLACING THE ENCODED STRING, NEVER BY `json.dump`** — a round-trip reformats all 30 KB and buries the one changed key. `json.dumps(old_value)` appears exactly once in the raw text; replace that, re-parse, then walk the new object against the old and print the changed key paths. It reported `['/files[3]/_']` three times this session and would have caught a stray edit instantly. **(5) THE BACKLOG'S "Open:" LIST IS HAND-MAINTAINED IN THREE PLACES** — the enumeration, the `## Completed items (…)` heading, and the row itself. Closing an item touches all three; the file says so itself and has been wrong before. **(6) `git log -S '<clause>' -- <path>` DATES A SILENT INVERSION** that blame and position cannot: it found the commit where the false sentence entered (true then) and the one where its subject changed underneath it.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `starter-kit/quality_ratchet.py --run` IN A `--no-local` CLONE WITH HEAD ASSERTED BY SHA.** **Citation, clone of `4504996` — the final tree, re-run after a commit landed past the first measurement rather than citing the earlier one: `quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results 10575dac7361 · manifest 01a4ae7aa511`**, bare exit **0**, `tests-sh-passed` **343 / 0 failed** at two receipts, exactly on the floor — identical digests to S199–S201, because no gate was added or moved. Also green in the working tree: `docs/archive/HANDOFFS-through-2026-09-20-3.md.verify.sh` **L1/L2/L3 OK** against the trim commit `1273a90`; `docs/planning/BACKLOG-DETAIL.md.verify.sh` **C1–C5 OK**, twice (after the closure, and after BL-75's narrowing); `bin/check-links` **111 links across 23 files**; `bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations` **72 rows, contiguous 15..86, 0 over 1,500 B**; `tools/test_context_budget.py` **122 tests, OK**; `python3 starter-kit/context_budget.py` **exit 2**, the pre-existing OVER state unchanged by the edit. **NOT EXERCISED:** this close-out commit itself (BL-64), whether the gates are armed in any clone but this one (BL-77), any response on #84/#85/#83, and **the D3 obligation, which no gate holds** — its second consecutive honouring is recorded here and in the ledger, by prose.
changelog_ref: CHANGELOG.md "2026-09-20 · [BL-53] S202 close-out", plus the claim, the trim (written by the trimmer), the fold, P5, BL-53's closure, the Phase 3C entry and the BL-75 correction
commit: 2faff89 (claim) + 1273a90 (retention trim) + eb3576d (fold) + 9db2c18 (P5, the deliverable) + fc4a006 (BL-53 closed) + 7bdc97e (fork Learning #86) + 4504996 (the BL-75 correction) + this close-out
```

