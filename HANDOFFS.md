# Handoff Receipts — durable close-out proof

This repository dogfoods its own methodology: every session records a durable, machine-checkable
`handoff` receipt here at close-out (Phase 3D), and Phase 0 reconciles it against `git log`. See
[`starter-kit/HANDOFFS.md`](starter-kit/HANDOFFS.md) for the block format and the write points, and
`bin/check-handoff` for the checker. Newest on top; prepend-only.

**Retention policy — this ledger keeps FOUR receipts.** This file currently holds **4**; everything
older is archived under `docs/archive/` and indexed in the table below. **A steady state by design —
but NOT yet enforced by tooling, and that distinction is load-bearing.** Held at four it rests near
43 KB. **N=4 is an operator decision, never re-derivable from the 56,750 B detector floor**
(`srf-red-refusal-adjudication.md` §11.5 (5)). **`methodology_trim.py` fires on BYTES (196,608 B), never on a
record count**, so left alone this file climbs to ~205 KB over ~14 sessions — 3.6× the one-read
cap — before the tool says anything. **Until the trimmer learns a retention mode, this policy is applied by the
session that notices: at Phase 0 run `grep -c '^```handoff' HANDOFFS.md`; if it exceeds 4, trim to 4.** Adopted at **S127 (2026-08-30)** by operator decision; the warrant — including why a retention
cap is not the periodic reset H3's RED rule forbids — is
[`docs/archive/CHANGELOG-through-2026-09-02.md`](docs/archive/CHANGELOG-through-2026-09-02.md)`:2070`,
where S152's trim moved it. `bin/check-handoff` validates its 13-key schema on the **newest** receipt, but
two of its other scopes traverse every receipt and `--all` checks all of them — it is not
newest-only. Since S133 `bin/model-report` globs the shards,
so its **default** run reaches archived prose; `--handoffs <shard>` narrows to one file.

**Two session sequences share this ledger and their numbers collide.** This fork and
`upstream/main` each run their own `S<N>` counter, so a receipt is identified by **session + date**,
never by number alone. **Every upstream receipt is now archived**; all four retained here are the
fork's. At a resync the two sequences stay separate and unrenumbered, each incoming receipt is
checked against ours before it is kept, and within a shared date the fork's precede the arriving
upstream ones (precedent: `fc4d297`).

> **The count above drifts between trims.** `methodology_trim.py` declares it a regenerated field
> (`starter-kit/methodology_trim.py`, the `HANDOFFS.md` `LedgerSpec`), so a **trim** rewrites it and
> the proof's L2 clause excuses that one span — but nothing updates it when a session **prepends** a
> receipt, which is most sessions. So it is right immediately after a trim and wrong from the next
> close-out onward: it read **6** for three sessions once. That is
> [Learning #12](starter-kit/FRAMEWORK_LEARNINGS.md) pointed at this file, and it is the receipt-ledger
> half of upstream [issue #65](https://github.com/KJ5HST/methodology/issues/65). Recount before
> trusting it.

> **⚠ THREE is the floor the retention policy sits one above.** `bin/tests.sh` Test 34 mutates *this*
> ledger to check `check-handoff --all`'s whole-ledger invariants, reading two anchors from the live
> file — not hardcoded, so it survives *which* receipts rotate, but it needs three to exist. S94
> retained **2** on the tool's default cut and the suite went 235/1 → **229/6**. Since S96 a short
> ledger is **stated rather than silent** (BL-40 (b)): below the floor those six assertions print as
> `SKIP` rows naming themselves, the summary carries a skip count, and a ledger with *zero* receipts
> still FAILS — corruption is not rotation. **Nothing prevents a cut below three; the policy is what
> makes it not happen.** Re-run `bash bin/tests.sh` after any trim of this file.

**Archived shards — 13 trims, 141 receipts.** Every shard is `docs/archive/HANDOFFS-through-<date>.md`
and its proof is that same path plus `.verify.sh`; same format, same newest-on-top order, frozen at
write. **Run the proof rather than trusting this table** — each re-derives L1/L2/L3 from git, and that
instruction is why these rows exist.

| n | span | shard | proof | by |
|--:|---|---|---|---|
| 16 | 2026-07-30 → 2026-08-02 | [`HANDOFFS-through-2026-08-02.md`](docs/archive/HANDOFFS-through-2026-08-02.md) | [proof](docs/archive/HANDOFFS-through-2026-08-02.md.verify.sh) | v1.1.1 |
| 30 | 2026-08-03 → 2026-08-09 | [`HANDOFFS-through-2026-08-09.md`](docs/archive/HANDOFFS-through-2026-08-09.md) | [proof](docs/archive/HANDOFFS-through-2026-08-09.md.verify.sh) | v1.1.1 |
| 25 | 2026-08-02 → 2026-08-11 | [`HANDOFFS-through-2026-08-11.md`](docs/archive/HANDOFFS-through-2026-08-11.md) | [proof](docs/archive/HANDOFFS-through-2026-08-11.md.verify.sh) | v1.1.3 |
| 8 | 2026-08-11 → 2026-08-15 | [`HANDOFFS-through-2026-08-15.md`](docs/archive/HANDOFFS-through-2026-08-15.md) | [proof](docs/archive/HANDOFFS-through-2026-08-15.md.verify.sh) | v1.2.0 |
| 4 | 2026-08-15 → 2026-08-17 | [`HANDOFFS-through-2026-08-17.md`](docs/archive/HANDOFFS-through-2026-08-17.md) | [proof](docs/archive/HANDOFFS-through-2026-08-17.md.verify.sh) | v1.2.0 |
| 3 | 2026-08-17 → 2026-08-18 | [`HANDOFFS-through-2026-08-18.md`](docs/archive/HANDOFFS-through-2026-08-18.md) | [proof](docs/archive/HANDOFFS-through-2026-08-18.md.verify.sh) | v1.3.0 |
| 3 | 2026-08-18 → 2026-08-23 | [`HANDOFFS-through-2026-08-23.md`](docs/archive/HANDOFFS-through-2026-08-23.md) | [proof](docs/archive/HANDOFFS-through-2026-08-23.md.verify.sh) | v1.3.0 |
| 3 | 2026-08-24 → 2026-08-24 | [`HANDOFFS-through-2026-08-24.md`](docs/archive/HANDOFFS-through-2026-08-24.md) | [proof](docs/archive/HANDOFFS-through-2026-08-24.md.verify.sh) | v1.3.0 |
| 2 | 2026-08-25 → 2026-08-25 | [`HANDOFFS-through-2026-08-25.md`](docs/archive/HANDOFFS-through-2026-08-25.md) | [proof](docs/archive/HANDOFFS-through-2026-08-25.md.verify.sh) | v1.3.0 |
| 17 | 2026-08-25 → 2026-08-29 | [`HANDOFFS-through-2026-08-29.md`](docs/archive/HANDOFFS-through-2026-08-29.md) | [proof](docs/archive/HANDOFFS-through-2026-08-29.md.verify.sh) | v1.5.0 |
| 5 | 2026-08-29 → 2026-08-30 | [`HANDOFFS-through-2026-08-30.md`](docs/archive/HANDOFFS-through-2026-08-30.md) | [proof](docs/archive/HANDOFFS-through-2026-08-30.md.verify.sh) | v1.5.0 |
| 23 | 2026-08-12 → 2026-09-04 | [`HANDOFFS-through-2026-09-04.md`](docs/archive/HANDOFFS-through-2026-09-04.md) | [proof](docs/archive/HANDOFFS-through-2026-09-04.md.verify.sh) | v1.5.0 |
| 2 | 2026-09-04 → 2026-09-07 | [`HANDOFFS-through-2026-09-07.md`](docs/archive/HANDOFFS-through-2026-09-07.md) | [proof](docs/archive/HANDOFFS-through-2026-09-07.md.verify.sh) | v1.5.0 |

<!-- NEXT TRIMMING SESSION: methodology_trim.py appends a 3-line pointer block here
     (starter-kit/methodology_trim.py:1093 build_pointer_block, :1103 insert_pointer). Fold it into
     the table above as one row (~182 B vs the block's ~447) and delete the block, IN ITS OWN
     COMMIT: inside the trim commit the shipped .verify.sh fails L2 (Learning #58). The generator
     is DISTRIBUTED, so teaching it this is an upstream change. -->

**Archived 2 record(s), 2026-09-08 → 2026-09-08** into [`docs/archive/HANDOFFS-through-2026-09-08.md`](docs/archive/HANDOFFS-through-2026-09-08.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/HANDOFFS-through-2026-09-08.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-08.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

```handoff
session: S158
date: 2026-09-10
status: pending
self_score: pending
predecessor_score: pending
active_task: **TRIM `HANDOFFS.md` BACK TO FOUR RECEIPTS** under the retention policy at `HANDOFFS.md:8` (operator decision, S127), chosen by the operator from this session's Phase 0 report. **59,187 B at claim, 6,349 B under `CEILING_BYTES`, and every record it holds is 8,521–12,286 B** — no room for this session's own. With the tool (`methodology_trim.py --file HANDOFFS.md --cut 4 --write`), never by hand; the fold in its own commit. **Fork-internal: no push, no PR, no comment; PR #80 untouched.**
what_was_done: pending
next_steps: pending
key_files: `HANDOFFS.md:8` (the retention paragraph), `:48` (the archive table), `:69-73` (the `NEXT TRIMMING SESSION` comment — its `:1093`/`:1103` anchors re-verified). `starter-kit/methodology_trim.py:1014` (`choose_cut`), `:1093` (`build_pointer_block`). `bin/check-handoff:662` (`CEILING_BYTES`), `:663` (`HEADER_RESERVE_BYTES`, 7,168).
gotchas: **THE PRE-CLAIM DRY RUN IS ALREADY STALE:** exit 0, SRF 0.6609 vs `c581ac4`, no gate, **1 of 5** (S153) to `docs/archive/HANDOFFS-through-2026-09-08.md` — but this stub is a sixth record, so the post-claim run should take **2**. Re-derive before writing. **FRONT MATTER 7,159 of 7,168 B, 9 B spare** — the fold's new row must be paid for in cut text, never by raising the constant.
runtime_smoke: S157 close-out suite **304 passed / 1 failed / 0 skipped, exit 1** (Test 9, pre-existing); `check-handoff` **0** and `methodology_trim.py --check` **0** at Phase 0; tree clean at `07c750b` apart from the Phase 0 `dashboard_history.jsonl` snapshot.
changelog_ref: CHANGELOG.md "2026-09-10 · [ad hoc] S158 — claim: apply the retention policy to `HANDOFFS.md` again, 5 receipts against a policy of 4 and no room for a sixth"
commit: pending
```
*(Phase 1B stub — the crash breadcrumb. Overwritten in place at close-out.)*

```handoff
session: S157
date: 2026-09-09
status: complete
self_score: 8
predecessor_score: 8
active_task: **THE PR IS OPEN: [KJ5HST/methodology#80](https://github.com/KJ5HST/methodology/pull/80), `read-set-budgets` (`598c459`) → `main` (`512c2ed`), state OPEN, `MERGEABLE`, 28 files, +7,783 / −553.** Opened on the operator's explicit *"open the PR"* — **the first outward-facing action of this arc**, after four sessions each recorded that gate as absent. **The grant covered opening and nothing else: NOT merged, no tag, no release, fork `main` not pushed, the five merged `origin` branches not deleted.** `origin/main` still `f8531cf`. **The next move is the maintainer's**, and the body hands him the version question on his own precedent (#74 `release/v3.7` shipped after the feature PRs it covered).
what_was_done: **Three commits: `18aa587` claim, `c64ee4b` the body correction, plus this close-out — and one non-commit action, the PR open, which is why FM #27 counts it.** **PRE-FLIGHT RE-DERIVED, NOT TRUSTED, AND IT CAUGHT A STALE NUMBER.** The body written at S155 said the fork was *"580 commits ahead"* of the branch; at publish time it was **590**, moved by S155's and S156's own commits. Corrected to a **dated** measurement — a frozen artifact can carry that without going false — and it is now **Learning #61** (1,227 B). The companion claim, 5 of 27 distributed sources drifted further on fork `main`, re-derived **unchanged, same five names**. Also verified before sending: both shas unmoved, ancestry still clean, diffstat identical, and **`gh pr list --state all --head read-set-budgets --base main` = 0**, so this opened rather than reopened. **THE PUBLISHED BODY WAS READ IN FULL BEFORE SENDING AND ROUND-TRIPPED AFTER:** `gh pr view 80 --json body` is **byte-identical to the file sent, 8,722 chars both sides**.
next_steps: **(1) THE PR IS THE MAINTAINER'S NOW — DO NOT MERGE IT.** Merging is a separate action and a separate go-ahead, and on `KJ5HST/methodology` it is his call, not this fork's. Watch it with `gh pr view 80 --repo KJ5HST/methodology --json state,reviews,comments`; **answering a review comment is itself outward-facing and needs its own ask.** **(2) REPAIR THE TWO STALE PLANNING DOCUMENTS — now the ranked fork-side item, and more wrong than before.** `docs/planning/upstream-read-set-pr-plan.md:1` (header) and `:555` (§11.3 — item 5 literally reads *"Nothing exists to open a PR from today"*, which #80 now refutes), plus `port-branch-identity-adjudication.md`. Neither knows `read-set-budgets` exists. Fork-side, no go-ahead needed. **(3) FIX `HOW_TO_USE.md:774`: 27 → 28.** Unblocked, verified four times now. **(4) DECIDE THE DENSITY RECORD** — `.context-budget.json` declares `HANDOFFS.md` at 2.3648 B/token; metered 2.3164 at 65,531 B and 2.2543 at 42,923 B. Learning #60 argues no single value is right; the three options are costed in S156's receipt. **(5) `HANDOFFS.md` IS BACK TO 5 RECEIPTS AGAINST A POLICY OF 4** — 52,493 B at claim, so bytes are not pressing, but the count is over. `--cut 4`, tool not hand, fold in its own commit; **no `--force` was needed at S156 and none should be assumed for the next one.** **(6) FIX `starter-kit/methodology_trim.py:1014` `choose_cut`.** Distributed: wants upstream consideration. **(7) DELETE THE FIVE MERGED `origin` BRANCHES** and **(8) PUSH `main`.** Both outward-facing on the fork: confirm first, each separately.
key_files: `docs/planning/read-set-budgets-to-main-pr-body.md:43` (§1 the title, as published), `:49` (§2 the body), `:122` (the dated ahead-count this session corrected), `:180` (§5, the command behind every number). `docs/planning/upstream-read-set-pr-plan.md:555` (§11.3 — **item 5 is now factually refuted by PR #80; fix it before quoting anything in §11.3**). `starter-kit/FRAMEWORK_LEARNINGS.md` row 61 (last). `bin/check-handoff:662` (`CEILING_BYTES`), `:663` (`HEADER_RESERVE_BYTES`, 7,168, kept by operator decision at S155).
gotchas: **(1) THE PUBLISHED BODY AND THE COMMITTED BODY DOCUMENT ARE NOT IDENTICAL, BY DESIGN.** The attribution block (`🤖 Generated with Claude Code` + the session URL) was appended to the extracted body **after** it was cut from the document, so PR #80's body carries it and `docs/planning/read-set-budgets-to-main-pr-body.md` does not. Anyone diffing the two will find a 129 B tail; that is expected, not drift. **(2) A DOCUMENT AWAITING APPROVAL KEEPS MEASURING THE TREE IT WAS WRITTEN AGAINST** — Learning #61. Re-derive every self-referential number at publish time. Numbers about the *other* side need only a re-fetch; numbers about *your own* tree are what move while you wait. **(3) THE GRANT WAS FOR ONE VERB.** *"Open the PR"* is not merge, tag, release, push, or reply-to-review. Each is its own ask, and this repository has ten sessions of history behind that rule. **(4) THE BODY EXTRACTION IS SCRIPTED DE-BLOCKQUOTING** — §2 is stored as a `>` block. Verify zero stray `>` prefixes survive (this session did: 0) and read the result before sending. **(5) `bin/tests.sh` MUTATES BOTH LIVE LEDGERS** — backed up outside the repo, `shasum -c` clean after. **(6) READ EXIT CODES BARE.**
runtime_smoke: **THIS REPO SHIPS NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`.** Close-out run, bare: **304 passed / 1 failed / 0 skipped, exit 1**, diffed **ROW FOR ROW** against S156's — **305 rows both sides, PASS→PASS throughout, ZERO status flips, zero added, zero removed**; every differing row states a number this session moved (receipts 4→5, live `**Model:**` bullets 11→14, the fixture's derived `#62`/`S157`). The one failure is Test 9 `github source dry-run failed`, **pre-existing — and it is precisely what PR #80 exists to cure**, since 3 of 27 manifest sources are absent from `main` and 0 from the branch. Checkers each bare: `check-links` **0**, `check-learnings` **0** (row 61, 0 over 1,500 B), `check-handoff` **1** while this receipt read `status: pending`, then **0**. **THE OUTWARD ACTION ITSELF WAS VERIFIED, NOT ASSUMED:** `gh pr view 80` reports `OPEN`, `MERGEABLE`, 28 files, +7,783/−553, base `main`, head `read-set-budgets`, and the live body **byte-identical to the file sent**. **NOT EXERCISED:** the merge itself, upstream CI (neither side has `.github/workflows`), any adopter tree, and `bin/sync --source=github` against a merged `main` — which still cannot exist until #80 lands.
changelog_ref: CHANGELOG.md "2026-09-09 · [ad hoc] S157 close-out — PR #80 OPENED: `read-set-budgets` → `upstream/main`, the first outward-facing action of this arc", plus the PR-open action entry, the body-correction entry, and the S157 claim entry
commit: 18aa587 (claim) + c64ee4b (the dated ahead-count) + this close-out
```

**Self-assessment: 8/10.** Plus: **re-derived the pre-flight facts instead of trusting the body I was
handed**, which is the only reason the stale 580 was caught before it went public rather than after.
**Read the exact extracted body in full before sending it and round-tripped the published version
against it** — 8,722 chars both sides — so the thing on GitHub is the thing that was reviewed.
Confirmed no PR had ever existed for this head/base, so *open* was the right verb. And stayed strictly
inside a one-verb grant with six adjacent actions sitting right there. **Minus:** I appended the
attribution block after extracting the body, which leaves the published PR and the committed document
differing by a 129 B tail — harmless, but it is a divergence I created rather than inherited, and it
needed a gotcha to explain. A cleaner order would have put the attribution in the document.

**Predecessor (S156): 8/10.** Its item (1) was ranked correctly, named the exact command and the exact
body sections, and stated the grant's boundary — so the moment the go-ahead arrived this session could
act without re-deriving what to do. Its trim also left the ledger with 13,043 B of headroom, which is
why the claim stub fit without a second byte negotiation. **Not 9: it handed forward an artifact for
publication without sweeping it for the very defect it had just fixed twice.** S155 had to repair a
drifting ahead-count in its own receipt, and S156's own close-out repeated the caution — yet neither
looked at the PR body sitting in `docs/planning/` carrying *"580 commits ahead"* of a tree they were
both adding commits to. The gap is now Learning #61, which is the right outcome, but the sweep should
have happened at the handoff.

```handoff
session: S156
date: 2026-09-09
status: complete
self_score: 8
predecessor_score: 8
active_task: **`HANDOFFS.md` IS BACK INSIDE EVERY BUDGET AND FITS IN ONE READ: 67,336 → 42,923 B, 6 receipts → 4.** Measured on the doubled-file meter, not inferred: **19,040 tokens (38,081 doubled), 76.2% of the 25,000-token cap**, from 28,287 at claim time. Front matter **7,159 B of the 7,168 B reserve**; the file has 22,613 B of ceiling headroom, so the next session can write a receipt — which at claim time it could not. S152 and S151 are frozen in [`docs/archive/HANDOFFS-through-2026-09-07.md`](docs/archive/HANDOFFS-through-2026-09-07.md) with its `.verify.sh`, **exit 0, pinned to the trim commit `c581ac4`, re-run after the fold and still 0**. **Fork-internal: nothing pushed, no PR, no tag, no comment.** `origin/main` unmoved at `f8531cf`, `upstream/main` `512c2ed`, `read-set-budgets` `598c459`; 0 open PRs.
what_was_done: **Five commits: `6ec5aec` claim, `c581ac4` the trim, `b19be54` the fold, `b3d19b0` close-out, plus a `chore(history)` for the append-only `.jsonl`.** **NO `--force` AND NO GATE THIS TIME** — SRF **0.1096** vs `aa1c476` against the **3.7022** that refused at S154, and the dry run exits 0. **THE TRIGGER NEVER FIRES AT THIS SIZE** (196,608 B threshold), so the warrant is the retention policy plus the byte ceiling, and **the warrant was corrected mid-session**: I had taken the 28,287-token overage as the reason until `methodology_trim.py`'s own `[TRIGGER_READ]` line ruled it *"FOR REFERENCE AND NOT AS A FAULT … delivery is an ordered prefix and this ledger is newest-on-top, so what truncates is the OLDEST records"* — BL-52's point. **The real forcing condition was 2 B of byte headroom.** **THE POST-CLAIM RE-DERIVE CHANGED THE ANSWER** (S153's gate): pre-claim `--cut 4` archived **1** record, post-claim **2**, because the stub is a sixth. **THE FOLD IS ITS OWN COMMIT AND THE PROOF WAS RE-RUN TO CONFIRM IT** — Learning #58 asserted, then tested. New **Learning #60** (1,260 B).
next_steps: **(1) ASK FOR THE GO-AHEAD TO OPEN THE PR — unchanged from S155 and still the ranked item.** The body is written and waiting: `docs/planning/read-set-budgets-to-main-pr-body.md`, §1 Title and §2 Body. When granted: `gh pr create --repo KJ5HST/methodology --base main --head read-set-budgets`. **Opening it and pushing are each a separate go-ahead.** **(2) REPAIR THE TWO STALE PLANNING DOCUMENTS.** `docs/planning/upstream-read-set-pr-plan.md:1` (header) and `:555` (§11.3 items 1, 2, 4), plus `port-branch-identity-adjudication.md` — neither knows `read-set-budgets` exists. Fork-side, no go-ahead. **(3) FIX `HOW_TO_USE.md:774`: 27 → 28.** Unblocked, verified three times. **(4) DECIDE THE DENSITY RECORD — BOTH MEASUREMENTS NOW EXIST, SO IT IS A JUDGMENT, NOT A MEASUREMENT TASK.** `.context-budget.json` declares `HANDOFFS.md` at **2.3648 B/token**, measured at 186,617 B; the file metered **2.3164 at 65,531 B** and **2.2543 at 42,923 B** today. The gate will keep printing a drift warning until someone writes a value in, and **Learning #60 is the argument that no single value is right** — so the honest options are (a) write 2.2543 with its provenance, (b) drop `bytes_per_token` and let the 2.27 floor derive it, accepting that this content meters *below* the floor, or (c) leave it and treat the warning as a standing re-meter instruction. **(5) FIX `starter-kit/methodology_trim.py:1014` `choose_cut`** so `resulting(k)` counts the pointer block and regenerated-field growth. Distributed: wants upstream consideration. **(6) DELETE THE FIVE MERGED `origin` BRANCHES** and **(7) PUSH `main`.** Both outward-facing on the fork: confirm first.
key_files: `HANDOFFS.md:8` (the retention paragraph — *"applied by the session that notices"*, executed here), `:49` (the archive table, row 13 added; the `n` column sums to **141**), `:69-73` (the `NEXT TRIMMING SESSION` comment — **it now carries the own-commit rule S154 could not fit**). `docs/archive/HANDOFFS-through-2026-09-07.md.verify.sh` (run it; it pins to `c581ac4`). `starter-kit/context_budget.py:68` (`MIN_BYTES_PER_TOKEN = 2.27` — Learning #60's subject; its comment claims a floor-derived ceiling *"can never certify an unreadable file as fine"*). `bin/check-handoff:662` (`CEILING_BYTES`), `:663` (`HEADER_RESERVE_BYTES`, kept at 7,168 by operator decision at S155). `starter-kit/FRAMEWORK_LEARNINGS.md` row 60 (last).
gotchas: **(1) REWRAPPING IS NOT CUTTING.** Fighting the 7,168 B reserve I reflowed three passages and saved **zero bytes** each time, and my first "compression" of the trimming comment came out **13 B LARGER** than the original — written without measuring it. Only words count; measure the replacement before pasting it. **(2) THE FOLD MUST BE ITS OWN COMMIT** (Learning #58) — and this session **verified** rather than assumed it: `.verify.sh` exits 0 both immediately after `c581ac4` and again after the fold `b19be54`. **(3) A TRIM'S OWN WRITE GROWS THE FRONT MATTER PAST THE RESERVE.** The pointer block plus regenerated fields took it 7,096 → 7,286 B, **118 B over**, before the fold traded the block for a 182 B row. Budget for that: the fold is a *net* saving only after the block is deleted. **(4) THE DRY RUN GOES STALE AT THE CLAIM COMMIT** — 1 record before, 2 after. Re-derive after claiming, never before. **(5) `--force` IS STILL NOT A PRECEDENT.** This trim needed none; S154's approval was for its file, regime and evidence, and the next trim asks again. **(6) `bin/tests.sh` MUTATES BOTH LIVE LEDGERS** — backed up outside the repo, `shasum -c` clean after the run. **(7) READ EXIT CODES BARE.**
runtime_smoke: **THIS REPO SHIPS NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`.** Post-trim, bare: **304 passed / 1 failed / 0 skipped, exit 1**, diffed **ROW FOR ROW** against S155's final run — **305 rows both sides, PASS→PASS throughout, ZERO status flips, zero added, zero removed.** Every differing row states a number this session moved: receipts **5 → 4**, front matter **7,096 → 7,159 B** (A2 reads *"99% used"*, 9 B spare), live `**Model:**` bullets **10 → 11**. **`0 skipped` is the load-bearing word** — Test 34 needs three receipts and four were retained, so BL-40 (b)'s SKIP rows never appeared. **The deliverable's own proof, run after committing as the procedure requires:** `bash docs/archive/HANDOFFS-through-2026-09-07.md.verify.sh` → **exit 0**, *"L1, L2/front-matter, L3 hold"*, *"6 before = 4 retained + 2 archived"*, source pinned to `c581ac4`; re-run after the fold commit, still **0**. Checkers each bare: `check-links` **0**, `check-learnings` **0** (row 60, 0 over 1,500 B), `check-handoff` **1** while this receipt read `status: pending` — the breadcrumb working — then **0**. `methodology_trim.py --check` **0**, and its `[TRIGGER_READ]` line no longer carries the one-read-cap note, because 42,923 B is under 56,750. `context_budget.py` **exit 2**, pre-existing (read-set class total); `HANDOFFS.md` now reads `warn` on density drift rather than `over`. **NOT EXERCISED:** any adopter tree, CI, the pushed path, the twelve older shard proofs, the maintainer's machine.
changelog_ref: CHANGELOG.md "2026-09-09 · [ad hoc] S156 close-out — `HANDOFFS.md` back inside every budget: 67,336 → 42,923 B, 6 receipts → 4, and it fits in one read again", plus the trimmer's own "Ledger trim" entry, the fold entry, and the S156 claim entry
commit: 6ec5aec (claim) + c581ac4 (the trim) + b19be54 (the fold) + b3d19b0 (close-out) + this chore(history)
```

**Self-assessment: 8/10.** Plus: **re-derived the dry run after the claim commit** rather than trusting
the pre-claim one, which is the difference between archiving 1 record and the correct 2. **Corrected my
own warrant mid-session** — I had taken the token overage as the reason to trim until the tool's own
`[TRIGGER_READ]` line ruled it not a fault, leaving the 2 B of byte headroom as the real forcing
condition; the claim entry records both. **Verified Learning #58 instead of citing it**, re-running the
frozen proof after the fold. And when the fold pushed the front matter 118 B over the reserve, the bytes
came out of **claims that had gone spent** — a correction of a sentence this file no longer contains —
not out of live content. **Minus:** three passes reflowing text that saved zero bytes, and a
"compression" that came out 13 B larger because I wrote it before measuring it. That is a byte
negotiation I already knew was tight, and I wasted four passes on it.

**Predecessor (S155): 8/10.** Its item (4) is why this session existed and why it could start
immediately: the measurement was exact and re-derived here to the byte (65,531 B, 2 B under
`CEILING_BYTES`; 28,287 tokens on the meter), the record count was right, and it named the S127
provenance so the policy did not have to be re-argued. It also said plainly that S154's `--force` was
not a precedent — correct, and it cost nothing when no gate appeared. **Not 9: *"the remedy is the
by-hand policy"* is a mis-steer.** Read literally it invites a hand edit of the ledger, which would
have produced no shard, no `.verify.sh` and no ledger entry; the actual remedy is the tool with an
explicit `--cut`, and I found that by running it rather than by reading the handoff. It also did not
carry forward the fold's own-commit rule — this session took that from S154's receipt, which happened
to still be retained, and would have lost it had the trim gone one record deeper.

```handoff
session: S155
date: 2026-09-09
status: complete
self_score: 8
predecessor_score: 7
active_task: **THE PR BODY EXISTS AND IS NOT OPENED: [`read-set-budgets-to-main-pr-body.md`](docs/planning/read-set-budgets-to-main-pr-body.md), 14,806 B.** The body for `read-set-budgets` (`598c459`) → `upstream/main` (`512c2ed`): title, body, reviewer guide, and the verification record behind every number. **Fork-internal: nothing pushed, no PR, no tag, no comment.** **Nothing pushed: `origin/main` unmoved at `f8531cf`**, `upstream/main` `512c2ed`, `read-set-budgets` `598c459`; 0 open PRs either repo. (An ahead-count drifts with the repairs that quote it — S154's lesson; a sha does not.) **Two operator calls at the Phase 0 gate:** the deliverable (the body, over two other offers), and **KEEP `HEADER_RESERVE_BYTES` at 7,168 B** — S154 item (4) closed; front matter still 7,096 B, untouched.
what_was_done: **PHASE 0 FOUND THE RANKED NEXT STEP MOOT — THE SESSION'S REAL FINDING.** S153 and S154 both ranked §11.3 item 1 — *"the PR's scope, four candidate payloads"* — first. **All four were already merged into `upstream/read-set-budgets` by PRs #76–#79 (2026-09-02 → 09-04)**, six days before S154 ran. Verified against the world, not the document: `gh pr list --state all` (no PR has ever had base `main`, head `read-set-budgets`), `git ls-tree` (all four artifacts present), and blob identity — the branch carries `c0550acd` and `b21854cc`, **the same `FRAMEWORK_LEARNINGS.md` blob S153 spent a session freezing**. Neither `upstream-read-set-pr-plan.md` nor `port-branch-identity-adjudication.md` contains the string `read-set-budgets` — **zero hits, both files.** So item (2), *"BLOCKED BY (1)"*, was never blocked, and became this deliverable. **THE HEADLINE WAS MEASURED, NOT A TRANSFERRED DENSITY.** The Phase 0 pair goes **80,526 B / 28,234 tok → 67,581 B / 23,902 tok**, 112.9% of the 25,000-token read cap to **95.6%**. Both came off the doubled-file meter (`upstream-read-set-pr-plan.md` §7), **validated before it was trusted**: `main`'s pair read undoubled reports **28,237**, doubled-and-halved **28,234** — §2.1's recorded figure to 3 tokens. New **Learning #59** (1,094 B of 1,500).
next_steps: **(1) ASK FOR THE GO-AHEAD TO OPEN THE PR — the body is written; nothing else blocks it.** When granted: `gh pr create --repo KJ5HST/methodology --base main --head read-set-budgets`, Title (§1) and Body (§2) from `docs/planning/read-set-budgets-to-main-pr-body.md`. **Opening it and pushing anything are each a SEPARATE go-ahead.** The version question (§11.3 item 8) is handed to the maintainer inside the body, on his own precedent — v3.7 shipped as its own `release/v3.7` PR (#74) **after** the feature PRs it covered. **(2) REPAIR THE TWO STALE PLANNING DOCUMENTS — the defect that cost two sessions.** `docs/planning/upstream-read-set-pr-plan.md:1` (header still reads *"PHASES 1–4 SHIPPED (fork-side, unpushed)"*) and `:555` (§11.3 items 1, 2, 4, 5), plus `port-branch-identity-adjudication.md`. Both must learn `read-set-budgets` exists. Decide there what happens to `port/framework-learnings-extraction` — redundant with #76 by blob identity, local, never pushed. Fork-side, no go-ahead. **(3) FIX `HOW_TO_USE.md:774`: 27 → 28. UNBLOCKED.** Re-verified a third time: the line reads *"A table of 27 documented agent tendencies"*; the highest FM row in `starter-kit/SESSION_RUNNER.md` is **28**, and `CLAUDE.md` says 28. Count by highest row, never `grep -c`. **Do NOT touch `README.md`'s v3.2–v3.6 sections.** **(4) THIS FILE NO LONGER FITS IN ONE READ — MEASURED, AND IT IS THE SHARPEST ITEM HERE.** At **65,526 B** it is 10 B under `CEILING_BYTES` but **28,287 tokens** on the doubled-file meter (56,573 halved) against a 25,000 cap — **over by 3,287**. That is FM #28 in the ledger the PR body is about. The byte ceiling is the wrong instrument: the binding one is 25,000 tok, ≈57,900 B at the **measured 2.3164 B/token** (65,526/28,287), and `.context-budget.json` still declares **2.3648**, which under-reports it as 27,708. **Re-derived here, deliberately NOT written into the config** — that is its own deliverable, and S154 declined the mirror-image edit for the same reason. It also holds **5 receipts against a policy of 4** (`HANDOFFS.md:8`). The trimmer does **not** fire (`--check` exits 0; trigger 196,608 B), so the remedy is the by-hand policy — **and S154's `--force` is explicitly not a precedent. ASK.** **(5) FIX `starter-kit/methodology_trim.py:1014` `choose_cut`** so `resulting(k)` counts the pointer block and regenerated-field growth before testing `stops(b)`. Distributed: wants upstream consideration. **(6) DELETE THE FIVE MERGED `origin` BRANCHES** (`docs/learning-13-handoff-predictions`, `pr1/…`–`pr4/…`, named in full in S154's receipt) and **(7) PUSH `main`.** Both outward-facing on the fork: confirm first.
key_files: `docs/planning/read-set-budgets-to-main-pr-body.md:43` (§1 the title), `:49` (§2 the body — paste this), `:180` (§5, every number with the command that produced it). `docs/planning/upstream-read-set-pr-plan.md:555` (§11.3 — **items 1, 2, 4 now stale; read §0 of the new body first**), `:278` (§6 dragons 1, 2, 4, answered inside the body). `bin/sync:89` on the branch (the `sys.exit` in `read_github`) with `:217` (the read loop filling `entries` for every row before the first `write_bytes` at `:164`) — why one absent source writes **nothing**. `bin/check-learnings:104` (`ROW_BUDGET_BYTES = 1500`; `:106` on the branch). `bin/check-handoff:663` (`HEADER_RESERVE_BYTES = 7168`, **kept — operator decision**). `starter-kit/FRAMEWORK_LEARNINGS.md` row 59 (last).
gotchas: **(1) A DOCUMENTED OPEN DECISION MAY HAVE BEEN CLOSED BY EVENTS.** Learning #59. Re-derive that it is still open from branches, merged PRs and blobs — never from the document posing it. **(2) `grep` IS LINE-BASED AND YOUR PHRASE MAY WRAP.** I called the *"trained reflex"* sentence absent from `.githooks/pre-commit`; it breaks across a comment line and sits at `:59-62` of the **fork's** 8,915 B hook (upstream's is 2,807 B, byte-identical on both refs). `tr '\n' ' '` first. **(3) ZSH READS `"$ref:starter-kit/…"` AS A HISTORY MODIFIER** (`:s` = substitute), returning empty **silently** — twice here. Write `"${ref}:…"`. **(4) A "MOVED, NOT CHANGED" CLAIM IS PER-ROW.** My draft said the 13 learnings arrive *"byte-for-byte"*; diffed row by row, **11 do, #12/#13 do not** (2,400→1,450, 1,572→1,446 B) — both breach the 1,500 B budget the same PR adds. The true sentence is the better one; it is in the body. **(5) `check-learnings` SAYS `contiguous 1..58` WITH ROW 59 PRESENT — BL-44, NOT A DEFECT.** Exit 0 right, sentence wrong; S154's warning worked. **(6) `bin/tests.sh` MUTATES BOTH LIVE LEDGERS** — backed up outside the repo, `shasum -c` after all three runs. **(7) READ EXIT CODES BARE**; all of the below were. **(8) `.context-budget-history.jsonl` GOES DIRTY FROM PHASE 0** — a bare `context_budget.py` run appends. Never `git reset --hard`.
runtime_smoke: **THIS REPO SHIPS NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`.** **Three full suites, every exit code read bare.** On `main`: Phase 0 baseline and close-out both **304 passed / 1 failed / 0 skipped, exit 1**, diffed **ROW FOR ROW** by normalised label — **305 rows both sides, 0 status flips, 0 added, 0 removed**; the nine rows whose text differs each state a count this session's own writes moved (a receipt, a `**Model:**` entry, a learning row, ledger 54,258 → 55,827 B); `front matter is 7096 B` is identical on both sides. The one failure is Test 9 `github source dry-run failed`, pre-existing. **In two detached worktrees, for the deliverable's evidence:** pristine `upstream/main` (`512c2ed`) **114 passed / 0 failed, exit 0**; `upstream/read-set-budgets` (`598c459`) **115/1, exit 1** — **111 shared rows, zero status flips**, two new assertions (the trimmer's and the gate's unit tests), three rows differing only in a number the change moves (`24`→`27` twice, `works`→`failed`). **THAT FAILURE'S CAUSE WAS MEASURED:** of the branch's 27 manifest **SOURCE** paths, **3 are absent from `upstream/main`, 0 from the branch** — it fails a test about `main`'s contents, and **merging it is the only thing that can flip the row**. Checkers on `main`, bare: `check-links` **0** (105 links / 23 files), `check-learnings` **0** (row 59 added, 0 over 1,500 B), `check-handoff` **1** while this receipt read `status: pending` — the breadcrumb working — then **0**. `context_budget.py` exit **2**, pre-existing (read-set total). **NOT EXERCISED:** any adopter tree, CI (neither side has `.github/workflows`), the pushed path, the maintainer's machine, and `bin/sync --source=github` against a *merged* `main`, which cannot exist until the PR does.
changelog_ref: CHANGELOG.md "2026-09-09 · [ad hoc] S155 close-out — the PR body for `read-set-budgets` → `upstream/main`, written and not opened", plus the 2026-09-09 S155 claim entry above it
commit: 3a3f52c (claim) + c3b9465 (chore/history) + 2cb6fc2 (close-out) + this repair
```

**Self-assessment: 8/10.** Plus: **checked the world before executing the instruction** — `gh pr list`,
`git ls-tree`, blob identity — the only reason this session did not spend itself building four payloads
for a decision four merges had already made. **Validated the token meter against a recorded figure
before trusting it** (28,237 undoubled vs 28,234 doubled-and-halved), so the body's headline is a
measurement, not a density carried across content types. **Caught my own false claim in the draft**:
the 13 learnings rows do *not* all arrive byte-for-byte. Ran the suite on both trees and did the row-for-row diff §11.3 item 6 asks for.
**Minus:** I called a sentence missing from a file on a line-based grep when it wrapped across a line
break — a population-vs-sample error I have been warned about. Two silent zsh history-modifier
failures before switching to `${ref}`. And I sized this receipt against the ceiling only after
drafting it, then had to cut 436 B back out.

**Predecessor (S154): 7/10.** Its mechanics were excellent and its gotchas paid out:
*"READ EXIT CODES BARE"* shaped every measurement here; gotcha (2) — that `check-learnings`'
`contiguous 1..N` sentence is BL-44, not a defect — **stopped a false finding the moment I hit it**,
row 59 present and the checker saying 58; the ledger-backup warning was followed three times; and
`bin/check-handoff:663`/`:662` were exact, so the header-reserve trade reached the operator as
arithmetic rather than opinion. Item (4)'s *"ASK, DO NOT RAISE IT"* worked exactly as
designed — the answer is now on record. **Not 8: the item it ranked FIRST did not exist.** Item (1)
asked for a four-payload scope decision whose four payloads had been merged upstream six days
earlier; item (2) was marked *"BLOCKED BY (1)"* and was not blocked. Executed literally, that is a whole session
rebuilding branches to re-decide a settled question — and S153 handed the same instruction forward
before it. Neither asked `gh pr list`. Both receipts were faithful to their predecessor and
unfaithful to the repository: Learning #59.

