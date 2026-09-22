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

**Archived 1 record(s), 2026-09-21 → 2026-09-21** into [`docs/archive/HANDOFFS-through-2026-09-21-6.md`](docs/archive/HANDOFFS-through-2026-09-21-6.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/HANDOFFS-through-2026-09-21-6.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-21-6.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

```handoff
session: S217
date: 2026-09-21
status: pending
active_task: **PLAN BL-66, ONE SESSION; THE PLAN IS THE DELIVERABLE.** `README.md:61` tells adopters to update from the GitHub URL, which `bin/sync --source=github` cannot do for a file that is merely behind (no history to match against), while `starter-kit/BOOTSTRAP.md` says to prefer `--source=local`; the plan goes to `docs/planning/`, fixes nothing and opens nothing upstream. Chosen at this session's Phase 0 picker, where no maintainer reply was found on #83–#86. **Side actions approved at the same picker:** the `HANDOFFS.md` retention trim this receipt makes owed and its fold; raising BL-84 (the seed's fixed `CLAUDE.md` warn line vs its mandatory purpose fence, relayed from `mts-system` S143); pushing fork `main` to `origin` at close-out.
commit: pending
```

```handoff
session: S216
date: 2026-09-21
status: complete
self_score: 8
predecessor_score: 9
active_task: **BL-78 IS CLOSED (`2674c95`) AND BL-83 IS OPEN (`38e4e11`); NOTHING UPSTREAM MOVED.** The closing edits S206 left owed are made: BL-78's row moved to §Completed items (`docs/planning/BACKLOG.md:181`), a closing update at `docs/planning/BACKLOG-DETAIL.md:3029`, and `.context-budget.json:101` (`files[4]._`) rewritten in two sentences, the only key path changed. **The ratchet that note described EXISTS and is unwired:** `python3 starter-kit/context_budget.py --precommit` refused a staged growth of `starter-kit/SESSION_RUNNER.md` (exit 2) and passed a staged shrink (exit 0) in a clone, and `.githooks/pre-commit` never calls it. So BL-78's S201 *"does not exist"* and S203's *"has to build the check"* were false (corrected in the update, not in place), and fork Learning #85 (`docs/FORK_LEARNINGS.md:97`) still teaches that false example: raised as **BL-83**, decision first. **#83–#86: no maintainer reply; the upstream plan's next phase, P5, waits for #86 to merge.** Side actions approved at the Phase 0 picker: the `HANDOFFS.md` trim and fold (done) and the fork push after this commit, with its record following.
what_was_done: **Phase 0:** `CHANGELOG.md` frontier = HEAD `68160ba`, gap empty; `HANDOFFS.md` frontier `78cb080`, the one commit after it S215's announced push record; no pending stub, 2 receipts; nothing backfilled. Gate citation re-run in a `--no-local` clone at `68160ba`: S215's exactly. Dashboard 76/100, medium, 0 high+ (in that clone). Upstream 0 issues; #83–#86 at unchanged heads, 0 reviews, only our comments. **Picker:** deliverable = BL-78's closing edits (recommended, over planning BL-66 or a decision session); go-aheads: the trim + fold, the fork push. **`461e38b`** the claim. **`1c1c4e3`** the retention trim (`--cut 2 --force`, dry run first, 25,815 → 14,071 B, shard `HANDOFFS-through-2026-09-21-5.md`, S214's receipt; SRF, CUT_STRADDLES_DAY, SHARD_NAME_DISAMBIGUATED, FRONTMATTER_FIELD_ABSENT, as S215 predicted); its `.verify.sh` L1/L2/L3 OK, exit 0, in a clone at `1c1c4e3`. **`2701247`** the fold (→ 13,615 B); `bash bin/tests.sh` 343 / 0 / 6 in a clone at `2701247`. **Found before editing:** grepping the tool for the note's refusal found `def precommit` (`starter-kit/context_budget.py:1000`); run in a clone at `2701247` it refused a growth (exit 2) and passed a shrink and a control (exit 0). **Second picker:** BL-78 still closes with the record fixed; fork Learning #85 becomes a backlog item. That picker said S206's decision was costed on the false premise. S205's receipt and S206's ledger entry showed it was not (S205 had re-established the refusal in `files[5]._`; S206's evidence was §(3)'s merge finding, re-verified here by parent count), and I told the operator before any edit. **`2674c95`** BL-78 closed: row moved, `Open:` list and heading updated, closing update, `files[4]._` rewritten (script-asserted one key path, 35,090 → 35,745 B); `BACKLOG-DETAIL.md.verify.sh` C1–C5 OK, `./bin/check-links` OK, `tools/test_context_budget.py` 122 OK; the default budget run in clones at `2701247` and `2674c95` gave identical output apart from `BACKLOG.md`'s own size (exit 2 both, the same four `over` rows, no config defect). **`38e4e11`** BL-83 raised (index row, `Open:` list, detail block; three shapes, none costed); verify C1–C5 and `check-links` OK. **Phase 3C:** no fork-learnings row, so D3's obligation does not arise; the lesson about claiming a past decision's premise went to agent memory.
next_steps: **(1) AT PHASE 0, CHECK ALL FOUR PRs FOR A MAINTAINER RESPONSE. THE UPSTREAM PLAN'S NEXT PHASE IS P5 (`docs/planning/context-budget-status-plan.md:746`), AND ONLY #86 MERGING UNLOCKS IT:** `gh pr list -R KJ5HST/methodology`; heads #83 `219fb9d`, #84 `77afc12`, #85 `e2501c5`, #86 `c1167ae`; our comments `5755256040` (#83) and `5753335477` (#84). A reply ranks first and is new work with its own go-ahead. **(2) IF NO REPLY, UPSTREAM-BOUND WORK THAT CAN ACCUMULATE HERE: PLAN BL-66** (its row in `docs/planning/BACKLOG.md`). Upstream `README.md:61` tells adopters to update from the GitHub URL, which `bin/sync --source=github` cannot do for a file that is merely behind, while `starter-kit/BOOTSTRAP.md:85` says to prefer `--source=local`; re-checked on `upstream/main` `6b29d3d` at S216. Both files are in #84's diff, so its PR waits for #84 or rides with it; a plan opens nothing. **(3) OR** have the operator decide BL-83 (three shapes, `docs/planning/BACKLOG-DETAIL.md:3289`), BL-81, BL-79, BL-77 or BL-74. Do not open a fifth upstream PR while four sit unreviewed without asking (`CLAUDE.md` §Contributing upstream). **(4) THE NEXT CLAIM MAKES THREE `HANDOFFS.md` RECEIPTS:** trim (`--cut 2 --force`, dry run first) and fold right after its Phase 0 report. The receipt it archives is S215's, dated 2026-09-21, so the shard name will be `-6`. **(5) NO `CHANGELOG.md` TRIM OWED YET:** 169,148 B before this close-out's entry, measured; about 174 KB after it and the push record (an estimate), about 22 KB under 196,608 B, so a trim may come due within a few sessions; measure at Phase 0. **CARRIED:** S206's list.
key_files: **Fork `main`:** `docs/planning/BACKLOG.md:9` (the `Open:` list: BL-78 out, BL-83 in), `:169` (BL-83's row), `:171` (the Completed heading), `:181` (BL-78's closed row); `docs/planning/BACKLOG-DETAIL.md:2853` (BL-78's block: the S201 claim at `:2900`, S203's §(3) at `:2972`), **`:3029` (the S216 closing update; read it before the body)**, `:3289` (BL-83); `.context-budget.json:101` (`files[4]._`, rewritten), `:110` (`files[5]._`, S205's, which names the function `precommit_check`); `starter-kit/context_budget.py:1000` (`def precommit`), `:1037` (the byte test), `:1044-1051` (the token arm), `:961-965` (the `HOOK` text); `.githooks/pre-commit:133` (its one gate call, `quality_ratchet.py --precommit`); `docs/FORK_LEARNINGS.md:97` (row #85), `:19-20` (append-only); `CLAUDE.md:45` (D1). **Upstream:** #83–#86 at the heads in (1).
gotchas: **(1) BL-78's DETAIL BLOCK NOW CONTRADICTS ITSELF, BY DESIGN:** the S201 paragraph (`:2900`) and §(3) (`:2972`) say the ratchet does not exist, and the S216 update at `:3029` corrects both. Read the tail first. **(2) NEVER RUN THE BARE `python3 starter-kit/context_budget.py` IN THE WORKING TREE:** on fork `main` it appends a row to the tracked `.context-budget-history.jsonl`, and `--status` does not exist here yet (it is #86). Run it in a `--no-local` clone. **(3) `files[5]._` CALLS THE FUNCTION `precommit_check`; IT IS `precommit`.** Noticed, not changed: outside the S206 scope. **(4) `install-hook` WOULD NOT WIRE THE RATCHET HERE:** `.githooks/pre-commit` exists and does not mention the tool, so it only prints a WARN; and its hook text runs `$(git rev-parse --show-toplevel)/context_budget.py`, while this repo keeps the tool under `starter-kit/`. **(5) `bin/check-links` IS PYTHON:** `./bin/check-links`. **(6) `bin/check-handoff` READS EACH FIELD AS ONE LINE,** and the receipt budget is 12,288 B. **(7) `HANDOFFS.md`'s front matter still says `--cut 1 --force`**, wrong through sixteen trims now. **`CHANGELOG.md` HAS NO FOLD.**
runtime_smoke: **THE DELIVERABLE IS A CONFIG COMMENT AND BACKLOG PROSE, AND THE TOOL THAT READS THE CONFIG WAS RUN ON BOTH SIDES OF THE EDIT:** the default `context_budget.py` run in `--no-local` clones at `2701247` and `2674c95` exited 2 both times with the same four `over` rows and no config defect, the output identical apart from `BACKLOG.md`'s own size; `--precommit` gave exit 2 with a staged growth, 0 with a staged shrink, 0 with nothing staged. **Citation, fork `main` clone of `38e4e11`:** `quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results 10575dac7361 · manifest 01a4ae7aa511`, identical to Phase 0 (`tests-sh-passed` 343). Also green: `bash bin/tests.sh` 343 / 0 / 6 at `2701247`; the trim's `.verify.sh`; `BACKLOG-DETAIL.md.verify.sh` C1–C5; `./bin/check-links`; `tools/test_context_budget.py` 122 OK. **NOT EXERCISED:** this close-out commit itself (BL-64); an adopter's view (this config is the repo's own, not the distributed seed).
changelog_ref: CHANGELOG.md "2026-09-21 · [BL-78] S216 claim", the `HANDOFFS.md` trim (written by the trimmer), "[ad hoc] S216 — `HANDOFFS.md`: the trim's pointer block folded", "[BL-78] S216 — BL-78 closed", "[BL-83] S216 — BL-83 raised", and this close-out
commit: 461e38b (claim) + 1c1c4e3 (HANDOFFS trim) + 2701247 (fold) + 2674c95 (BL-78 closed) + 38e4e11 (BL-83 raised) + this close-out
```

