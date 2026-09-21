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

**Archived 1 record(s), 2026-09-20 → 2026-09-20** into [`docs/archive/HANDOFFS-through-2026-09-20-7.md`](docs/archive/HANDOFFS-through-2026-09-20-7.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/HANDOFFS-through-2026-09-20-7.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-20-7.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

```handoff
session: S206
date: 2026-09-20
status: pending
active_task: **BL-82 — draft answers to the twelve operator decisions in upstream PR #83's §8** (*"Open decisions for the operator (answer before Phase 1)"*, `docs/planning/parallel-sessions-plan.md` on `refs/pull/83/head`), as one document under `docs/planning/`. **Internal only: nothing is posted to #83** — a comment, review or edit there is outward and its own go-ahead. The document settles BL-82's four questions first (who owns which; one document or twelve answers; whether answering commits this fork to executing the plan; what re-verification each answer rests on) and separates *ratify the author's recommendation* from *decide fresh*. Chosen by the operator at this session's Phase 0 picker over a `CHANGELOG.md` trim, BL-80 and BL-79. **Also decided at that picker, recorded not executed:** BL-78 P3 = **no enforcement**, so BL-78 closes; the closing edits (index row, archive move, the `files[4]._` note that still claims a refusal) are their own later session. **Owed at this claim, its own action:** the `HANDOFFS.md` retention trim — this receipt makes **three** (`--cut 2 --force`). **Fork push approved for close-out.**
commit: pending
```

```handoff
session: S205
date: 2026-09-20
status: complete
self_score: 8
predecessor_score: 8
active_task: **BL-78 P2 IS DONE (`fac748f`).** `.context-budget.json` `files[5]` (`starter-kit/SAFEGUARDS.md`) — its `_` note now states that `max_bytes` **15,386 B is a REPORTED SERIES, NOT A NO-GROWTH PIN**, on the precedent BL-53 option C set for the 81,920 B `docs/FORK_LEARNINGS.md` figure; `over` on that row is the expected state, not a breach. **Option β**, settled by the operator at S204's Phase 0 picker; chosen as this session's deliverable at this session's picker over BL-81's, BL-80's and BL-79's costings. **Exactly one key path changed, `/files[5]/_`** — proved by walking the before/after JSON objects path by path (key set identical, every other value equal), not by eyeballing a diff. `max_bytes`, `max_tokens`, `measured_bytes` and `measured_on` are untouched, so the read-cap partition (41,364 + 15,386 = 56,750 B; 18,222 + 6,777 = 24,999 tok) is unchanged. **BL-78 is NOT closed:** P1 and P2 are done; P3 (cost an enforcement check, *"only if the operator wants enforcement"*) is undecided, and the item's index row in `docs/planning/BACKLOG.md:166` still describes the pre-P1 state.
what_was_done: **Phase 0:** `CHANGELOG.md` frontier = HEAD `2a8a76a`, gap empty; `HANDOFFS.md` frontier `7ca7b94` with `2a8a76a` above it, which **is** the fork-push ledger entry (`CHANGELOG.md` *"S204 — fork `main` pushed"*), so nothing was unrecorded and nothing was backfilled. No pending stub, **2** receipts. Gate citation **re-run, not read**, in a `--no-local` clone at `2a8a76a`: S204's citation exactly. Dashboard 76/100, medium, 0 high+. Upstream **0 open issues**; #85, #84, #83 open, **0 reviews each**, none moved since S204. **`252de09`** claim. **`219ce5b`** the owed retention trim (`--cut 2 --force`, 23,314 → 14,956 B; SRF / CUT_STRADDLES_DAY / SHARD_NAME_DISAMBIGUATED / FRONTMATTER_FIELD_ABSENT stated and expected; L1/L2/L3 OK, P1A_OK 64 → 65) and **`3288b30`** its fold, in its own commit; `bash bin/tests.sh` re-run after it: **343 passed, 0 failed, 6 skipped**. **`fac748f`** the deliverable. **`fac104a`** BL-82 opened. **`29d07c5`** fork Learning **#89** with the D3 refusal. **The rewrite corrected a provenance error in the note it replaced:** that note dated the byte pin to *"this file's size as it stood at S177"*; `git log -S '"max_bytes": 15386' -- .context-budget.json` returns exactly one commit, **`beffbd0` (2026-08-30, S129)**, and `git blame` on the two adjacent lines splits `max_tokens` (`0e8c6ac8`, S177) from `max_bytes` (`beffbd0`) by 17 days. S177 set only `max_tokens`.
next_steps: **(1) BL-78's REMAINING QUESTION IS P3, AND IT IS THE OPERATOR'S, NOT A MEASUREMENT.** Enforcement of the read-set byte figures does not exist in this clone — `.githooks/pre-commit:131-133` runs only `quality_ratchet.py --precommit`, and `context_budget.py`'s own refusal (`precommit_check`, `:1037`) is wired into nothing. Put P3 to the operator as a yes/no at the next Phase 0 picker: **no** closes BL-78 (update the index row at `docs/planning/BACKLOG.md:166` and move the item per the archive convention); **yes** makes P3 a costing session, and note BL-78 §(3) already showed a pre-commit byte gate would refuse none of `SESSION_RUNNER.md`'s growths, which were all merges. **(2) BL-82 IS OPEN — PR #83's twelve operator decisions.** The operator asked for the write-up at this session's picker; it is the natural next unit if they still want it. **Drafting is internal; posting to #83 is outward and needs its own go-ahead.** Start from §8 of `docs/planning/parallel-sessions-plan.md` on `refs/pull/83/head` (`git fetch upstream refs/pull/83/head:pr83`), and read BL-82's four settle-first questions before drafting. **(3) NO `HANDOFFS.md` TRIM IS OWED AT THE NEXT PHASE 0** — this close-out leaves **2** receipts — **but that session's claim makes three, so it falls due right after its report, at `--cut 2 --force`.** S201–S204 each predicted this and all four held; this is the fifth. **(4) `CHANGELOG.md` IS 149,652 B before this close-out's entry — 46,956 B under the 196,608 B trigger.** At S203's measured ≈22.5 KB/session that is roughly **two sessions** to the trigger (an estimate from one rate, not a measurement). Put it on the next picker; the scoped-trim recipe is S203's (`--cut <date> --force`, dry-run first). **(5) BL-81, BL-80, BL-79, BL-77, BL-74 AND BL-75 REMAIN UNDECIDED.** **(6) NOTHING OUTWARD WAS TAKEN.** S204's #85/#83 comment drafts were never persisted to any file; fresh drafts were written in this session's 3G report and posted nowhere. **CARRIED:** BL-73, BL-54's own PR, the `vscode_quarto_ext` relay, BL-68, BL-61, BL-60, BL-65, BL-66, BL-69, BL-70, BL-71, `model_project_constructor`'s push and its bare-`ruff` regression, `airqino`'s `HANDOFFS.md` migration in its own repository.
key_files: `.context-budget.json:104-110` (`files[5]` — `max_bytes` `:107` **15386**, blamed to `beffbd0`; `max_tokens` `:106` **6777**, blamed to `0e8c6ac8`; the new `_` note at `:110`, ≈5,017 B) and `:95-101` (`files[4]`, whose note still says *"every commit that grows it is refused … a ratchet, not a wall"* — **that describes an unwired path**, see gotcha (1)); `starter-kit/context_budget.py:1037` (`precommit_check`, the byte refusal nothing calls), `:398` (`measured_bytes`' only consumer); `.githooks/pre-commit:131-133` (the only budget-adjacent call — the ratchet, not the budget tool); `tools/test_context_budget.py:1258` (`TestThisRepoReadSetPartition` — tokens only); `docs/planning/BACKLOG-DETAIL.md:2866` (BL-78's costing, P1–P3 at `:2940-2960`), `:2814` (where BL-78 already says the ratchet is not wired) and its new BL-82 block at the file's end; `docs/planning/BACKLOG.md:11` (the hand-maintained `Open:` enumeration, now ending BL-82) and `:170` (BL-82's index row); `docs/FORK_LEARNINGS.md` row **#89** (1,258 B, the last line); `docs/HANDOFFS_ARCHIVE_INDEX.md` (last row = shard **-6**).
gotchas: **(1) `files[4]._` STILL CLAIMS AN ENFORCEMENT THAT DOES NOT EXIST.** Its *"every commit that grows it is refused while every commit that shrinks it passes: a ratchet, not a wall"* is true of `precommit_check` and false of this clone, which never calls it. P2's note for `files[5]` now says so plainly; `files[4]` was out of scope (FM #17) and still says the opposite. BL-78's detail block already records it at `BACKLOG-DETAIL.md:2814`, so it is **not a new item** — fold it into whatever closes BL-78. **(2) A CONFIG NOTE'S DATE IS ABOUT THE NOTE, NOT THE KEYS AROUND IT** (fork Learning #89): blame the data line, and `git log -S '"<key>": <value>'` the literal, before quoting provenance. **(3) `git blame -L "${n},${n}"` WITH AN EMPTY `$n` BLAMES THE WHOLE FILE** rather than failing — a grep that matched nothing produced a 116-line blame here instead of an error. Check the line number is non-empty first. **(4) `.quality-gates-results.json` IS STILL S195's** — eight sessions stale. Re-run in a `--no-local` clone; never read it. **(5) `--cut N` RETAINS N**, and `HANDOFFS.md`'s front matter still says `--cut 1 --force`, which `BACKLOG-DETAIL.md:1995` measured as not viable — wrong through five trims now. **(6) A DRY RUN OF `methodology_trim.py` NEEDS `--force` TOO.** **(7) `CHANGELOG.md` HAS NO FOLD** — that rule is `HANDOFFS.md`'s alone.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `starter-kit/quality_ratchet.py --run` IN A `--no-local` CLONE WITH HEAD ASSERTED BY SHA.** **Citation, clone of `29d07c5`: `quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results 10575dac7361 · manifest 01a4ae7aa511`**, `tests-sh-passed` **343 / 0 failed** at two receipts, exactly on the floor — identical digests to S199–S204, because no gate was added or moved. Also green: `tools/test_context_budget.py` **Ran 122 tests, OK** after the edit; `starter-kit/context_budget.py` exit **2** with the **same four `over` rows** as before (`docs/FORK_LEARNINGS.md`, `starter-kit/SESSION_RUNNER.md`, `starter-kit/SAFEGUARDS.md`, read-set total) — P2 changes no verdict, which is the point; the one-key-path walk (**1** changed path, `/files[5]/_`); `bash bin/tests.sh` **343/0/6 skipped** after the trim; `docs/archive/HANDOFFS-through-2026-09-20-6.md.verify.sh` **L1/L2/L3 OK** against `219ce5b`; `docs/planning/BACKLOG-DETAIL.md.verify.sh` **C1–C5 OK**; `bin/check-links` **111 links / 23 files**; `bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations` **75 rows, contiguous 15..89, 0 over 1,500 B**. **NOT EXERCISED:** this close-out commit itself (BL-64); what an adopter sees — `.context-budget.json` is this repo's own config, not the distributed seed; whether the gates are armed in any clone but this one (BL-77); any response on #85/#84/#83.
changelog_ref: CHANGELOG.md "2026-09-20 · [BL-78] S205 claim", the `HANDOFFS.md` trim (written by the trimmer), its fold, "[BL-78] S205 — P2 done", "[ad hoc] S205 — BL-82 opened", "[ad hoc] S205 — Phase 3C", and this close-out
commit: 252de09 (claim) + 219ce5b (HANDOFFS trim) + 3288b30 (fold) + fac748f (the deliverable) + fac104a (BL-82) + 29d07c5 (fork Learning #89 + D3) + this close-out
```

