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
[`docs/archive/CHANGELOG-through-2026-09-02.md`](docs/archive/CHANGELOG-through-2026-09-02.md)`:2070`. `bin/check-handoff` validates its 13-key schema on the **newest** receipt, but
two of its other scopes traverse every receipt and `--all` checks all of them. `bin/model-report` globs the shards,
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
> close-out onward. That is
> [Learning #12](starter-kit/FRAMEWORK_LEARNINGS.md) pointed at this file, and it is the receipt-ledger
> half of upstream [issue #65](https://github.com/KJ5HST/methodology/issues/65). Recount before
> trusting it.

> **⚠ THREE is the floor the retention policy sits one above.** `bin/tests.sh` Test 34 mutates *this*
> ledger to check `check-handoff --all`'s whole-ledger invariants, reading two anchors from the live
> file — not hardcoded, so it survives *which* receipts rotate, but it needs three to exist. A short
> ledger is **stated rather than silent** (BL-40 (b)): below the floor those six assertions print as
> `SKIP` rows naming themselves, the summary carries a skip count, and a ledger with *zero* receipts
> still FAILS — corruption is not rotation. **Nothing prevents a cut below three; the policy is what
> makes it not happen.** Re-run `bash bin/tests.sh` after any trim of this file.

**Archived shards — 18 trims, 150 receipts.** Every shard is `docs/archive/HANDOFFS-through-<date>.md`
and its proof is that same path plus `.verify.sh`; same format, same newest-on-top order, frozen at
write. **Run the proof rather than trusting this table** — each re-derives L1/L2/L3 from git, and that
instruction is why these rows exist.

| n | span | shard | by |
|--:|---|---|---|
| 16 | 2026-07-30 → 2026-08-02 | [`HANDOFFS-through-2026-08-02.md`](docs/archive/HANDOFFS-through-2026-08-02.md) | v1.1.1 |
| 30 | 2026-08-03 → 2026-08-09 | [`HANDOFFS-through-2026-08-09.md`](docs/archive/HANDOFFS-through-2026-08-09.md) | v1.1.1 |
| 25 | 2026-08-02 → 2026-08-11 | [`HANDOFFS-through-2026-08-11.md`](docs/archive/HANDOFFS-through-2026-08-11.md) | v1.1.3 |
| 8 | 2026-08-11 → 2026-08-15 | [`HANDOFFS-through-2026-08-15.md`](docs/archive/HANDOFFS-through-2026-08-15.md) | v1.2.0 |
| 4 | 2026-08-15 → 2026-08-17 | [`HANDOFFS-through-2026-08-17.md`](docs/archive/HANDOFFS-through-2026-08-17.md) | v1.2.0 |
| 3 | 2026-08-17 → 2026-08-18 | [`HANDOFFS-through-2026-08-18.md`](docs/archive/HANDOFFS-through-2026-08-18.md) | v1.3.0 |
| 3 | 2026-08-18 → 2026-08-23 | [`HANDOFFS-through-2026-08-23.md`](docs/archive/HANDOFFS-through-2026-08-23.md) | v1.3.0 |
| 3 | 2026-08-24 → 2026-08-24 | [`HANDOFFS-through-2026-08-24.md`](docs/archive/HANDOFFS-through-2026-08-24.md) | v1.3.0 |
| 2 | 2026-08-25 → 2026-08-25 | [`HANDOFFS-through-2026-08-25.md`](docs/archive/HANDOFFS-through-2026-08-25.md) | v1.3.0 |
| 17 | 2026-08-25 → 2026-08-29 | [`HANDOFFS-through-2026-08-29.md`](docs/archive/HANDOFFS-through-2026-08-29.md) | v1.5.0 |
| 5 | 2026-08-29 → 2026-08-30 | [`HANDOFFS-through-2026-08-30.md`](docs/archive/HANDOFFS-through-2026-08-30.md) | v1.5.0 |
| 23 | 2026-08-12 → 2026-09-04 | [`HANDOFFS-through-2026-09-04.md`](docs/archive/HANDOFFS-through-2026-09-04.md) | v1.5.0 |
| 2 | 2026-09-04 → 2026-09-07 | [`HANDOFFS-through-2026-09-07.md`](docs/archive/HANDOFFS-through-2026-09-07.md) | v1.5.0 |
| 2 | 2026-09-08 → 2026-09-08 | [`HANDOFFS-through-2026-09-08.md`](docs/archive/HANDOFFS-through-2026-09-08.md) | v1.5.0 |
| 2 | 2026-09-09 → 2026-09-09 | [`HANDOFFS-through-2026-09-09.md`](docs/archive/HANDOFFS-through-2026-09-09.md) | v1.5.0 |
| 1 | 2026-09-09 → 2026-09-09 | [`HANDOFFS-through-2026-09-09-2.md`](docs/archive/HANDOFFS-through-2026-09-09-2.md) | v1.5.0 |
| 2 | 2026-09-10 → 2026-09-10 | [`HANDOFFS-through-2026-09-10.md`](docs/archive/HANDOFFS-through-2026-09-10.md) | v1.5.0 |
| 2 | 2026-09-11 → 2026-09-11 | [`HANDOFFS-through-2026-09-11.md`](docs/archive/HANDOFFS-through-2026-09-11.md) | v1.5.0 |

<!-- NEXT TRIMMING SESSION: methodology_trim.py appends a 3-line pointer block here
     (starter-kit/methodology_trim.py:1093 build_pointer_block, :1103 insert_pointer). Fold it into
     the table above as one row (~125 B vs the block's ~448) and delete the block, IN ITS OWN
     COMMIT: inside the trim commit the shipped .verify.sh fails L2 (Learning #58). The generator
     is DISTRIBUTED, so teaching it this is an upstream change. -->

```handoff
session: S167
date: 2026-09-15
status: pending
self_score: pending
predecessor_score: pending
active_task: **BL-57's P1 — STRUCTURE ONLY: THE SEED'S THREE `CHANGELOG.md` RULE SECTIONS MOVE VERBATIM TO `FRAMEWORK_APPARATUS.md` §The Action Ledger, THE SEEDS THIN, `bin/status` KEYS ON A NEW MARKER, THE STALE-SEED ADVICE STOPS REWRITING ENTRIES (C16).** The operator's "A" at Phase 0. Branch `bl57/changelog-rules` from #80's head `aa36fd8b`, worktree `../methodology-bl57`; nothing pushed. First, `HANDOFFS.md`'s retention trim (5 receipts → 4), re-derived after this claim.
what_was_done: pending
next_steps: pending
key_files: `docs/planning/changelog-rules-contradictions-plan.md:359` (P1), `:335` (§5.0, how every phase works), `:749` (§9.3, the verbatim check), `:773` (§9.4, the marker check); `HANDOFFS.md:15` (the retention rule).
gotchas: The plan's line numbers are `b82dcff`'s and P1 branches from `aa36fd8b` — re-derive each before editing. A `--no-local` clone lacks `upstream/*` refs — clone with `-b` a local branch. `bin/tests.sh` mutates both live ledgers — clone only. `git rev-parse --short a b` fails — one revision per call (hit again at this Phase 0).
runtime_smoke: Baseline at `6142d538` in a `--no-local` clone: **304 passed / 1 failed / 0 skipped, exit 1** (Test 9, pre-existing). Dashboard 76/100. Both ledger frontiers current, 0 undocumented commits. PR #80 OPEN at `aa36fd8b`, `MERGEABLE`/`CLEAN`, 3 comments; `upstream/main` `9fa3141`.
changelog_ref: CHANGELOG.md "2026-09-15 · [BL-57] S167 claim — BL-57's P1: the `CHANGELOG.md` rules to one home, thin seeds, one stale-seed rule (structure only), on a branch from #80's head"
commit: pending
```

```handoff
session: S166
date: 2026-09-15
status: complete
self_score: 8
predecessor_score: 9
active_task: **PR #80'S F2 AND F3 ARE PUBLISHED — PUSHED, DESCRIBED AND ANSWERED, ON THE OPERATOR'S "A B C" AT PHASE 0.** `KJ5HST/methodology:read-set-budgets` fast-forwarded `d4e1570..aa36fd8` (F2 `37740763`, F3 `aa36fd8b`); the description replaced from `docs/planning/pr80-body-after-f3.md`; the reply posted ([comment](https://github.com/KJ5HST/methodology/pull/80#issuecomment-5685701488)). #80 is OPEN, `MERGEABLE`/`CLEAN`, 3 comments, at `aa36fd8b`. The three findings the review asked for before the merge (F1–F3) are all answered upstream; F4 goes with F3; F5 and F6 can follow the merge. **The next move is the maintainer's.**
what_was_done: **Fork `main`: `32c90db4` claim (with the Phase 0 `dashboard_history.jsonl` snapshot); `6e109e45` the record — three action entries in `CHANGELOG.md`, and `docs/planning/pr80-review-response.md`'s header, §1 and §3 set to published, §3 noting the one lag; this close-out, which also sets §4's and §5's headings. Upstream, three outward actions, each read back through the API before the next:** (A) `git push upstream pr80/f3-read-set-token-ceilings:read-set-budgets`, run only inside a guard that re-checked #80's head (`d4e1570`), `upstream/main` (`9fa3141`) and 2 comments in the same command — `d4e1570..aa36fd8`; the remote ref and the API's branch head read `aa36fd8b`, and #80 did too on the second query (16 commits, `MERGEABLE`/`CLEAN`) — the first, seconds after the push, still read `d4e1570` and `UNKNOWN`, and B waited for it. (B) `gh api -X PATCH repos/KJ5HST/methodology/pulls/80 -F body=@docs/planning/pr80-body-after-f3.md`; the live body read back equal to the file byte for byte (10,151 B plus `--jq`'s newline). (C) `gh api repos/KJ5HST/methodology/issues/80/comments -F body=@docs/planning/pr80-reply-f2-f3.md` → comment `5685701488`, `rmsharp`, 18:21:28 UTC, equal to the file (4,871 B); 3 comments. **Phase 0 re-derived the preconditions rather than carrying them**, before offering the publish: the live description equal to `pr80-body-after-f1.md`, so the maintainer had not edited it; the push a fast-forward; `git merge-tree` against `upstream/main` clean; the diff size reproduced (+7,795 / −554 at `d4e1570`, +7,892 / −580 at `aa36fd8b`, 28 files). No trim: `HANDOFFS.md` held 4 receipts at Phase 0.
next_steps: **(1) THE MAINTAINER'S MOVE — WATCH #80; ANSWER NOTHING WITHOUT THE OPERATOR'S ASK.** At Phase 0: `gh pr view 80 --repo KJ5HST/methodology --json state,headRefOid,mergeStateStatus,comments` — OPEN at `aa36fd8b` with 3 comments unless he has acted. Bring any new comment to the operator; each reply, push or edit is its own go-ahead. If #80 merged: measure Test 9 on `upstream/main` (it should pass; don't assume), and reconcile fork `main` with `upstream/main`, which conflicts in both ledgers today (`git merge-tree --write-tree --name-only main upstream/main`). **(2) F5 AND F6** after the merge or as he asks (`docs/planning/pr80-review-response.md:243`): F5's stale citations at `aa36fd8b` are `starter-kit/methodology_trim.py:9` and `:155` (a design doc absent upstream) and `:33` (`--no-renames` in a hook that lacks it); F6 is one wording fix in the description. **(3) BL-57's P1** once #80's F-items settle, from #80's then-current head (`docs/planning/changelog-rules-contradictions-plan.md:359`); D8 (`:143`) is half done inside #80 by F3 — amend it at P2. **(4) `HANDOFFS.md` HOLDS FIVE RECEIPTS** after this close-out, so S167's Phase 0 trims to four (`HANDOFFS.md:15`); re-derive the dry run after its claim (SRF against `d9ace03`; `SRF_RED` only at 60,236 B). **(5) `CHANGELOG.md` NEARS THE 262,144 B READ REFUSAL** — 236,900 B after this close-out, 25,244 B under it; S161–S166 grew it 4.5–14.4 KB each, so it crosses in two to five sessions (an estimate). Not trimming it is the operator's 2026-09-14 decision — raise it at a Phase 0, don't act. **(6) FORK `main` IS PUSHED** — `755ef09..632f575` after this close-out, on the operator's go-ahead, then the commit recording it, so `origin/main` equals `main`. **CARRIED:** S161's merge-options (b)/(c); BL-54; the two stale planning documents; `HOW_TO_USE.md:774`; BL-36; Test 31; BL-53 (~3 rows); `choose_cut`; nine merged `origin` branches. Each push and deletion is its own go-ahead.
key_files: `docs/planning/pr80-review-response.md:1` (header, published), `:8` (the S166 paragraph), `:62` (§3, the recipe), `:80` (S166's run of it), `:243` (§6, F5 and F6); `docs/planning/pr80-body-after-f3.md:1` (the live description); `docs/planning/pr80-reply-f2-f3.md:1` (the posted reply); `CHANGELOG.md:213` (this close-out; the three action entries and the claim follow); `HANDOFFS.md:15` (the retention rule); `docs/planning/changelog-rules-contradictions-plan.md:359` (P1), `:143` (D8); at `aa36fd8b`, `starter-kit/methodology_trim.py:9`, `:33`, `:155` (F5); `starter-kit/methodology_dashboard.py:4342` (root resolution).
gotchas: **(1) A PR'S `headRefOid` LAGS A PUSH BY SECONDS** — `gh pr view` read `d4e1570` and `UNKNOWN` just after the push while `git ls-remote` and `gh api …/branches/read-set-budgets` were already current. Gate a step that names the new head on the PR's own read-back, re-queried. **(2) `HANDOFFS.md`'S RETENTION RULE COUNTS AT PHASE 0, BEFORE THE CLAIM** — S165's *"S166's claim makes five and its Phase 0 trims"* was off by one; compute the room (65,536 − size) against the largest recent record instead. **(3) THE DASHBOARD IS `python3 starter-kit/methodology_dashboard.py --no-open`**, run from the repo root (it resolves the root itself, `:4342`); it appends to the tracked `dashboard_history.jsonl`, which rides with the claim commit. No ledger entry records the command, so a grep for it finds nothing. **(4) THE REPLY WENT THROUGH `gh api …/issues/80/comments -F body=@…`**, which returns the id for the read-back; §3 still lists `gh pr comment`, not exercised here. **(5) `git rev-parse --short a b` FAILS** — I hit it at Phase 0 though S165's gotcha (7) names it. **(6) `bin/tests.sh` MUTATES BOTH LIVE LEDGERS** — clone only.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`,** in `--no-local` clones, exit codes read bare. Phase 0 at `5ce7bb2`: **304 / 1 / 0, exit 1** (Test 9, the GitHub-source dry run, pre-existing). **GitHub, the surface this session changed:** A, B and C each read back through the API as `what_was_done` records; #80 `MERGEABLE`/`CLEAN` at `aa36fd8b` after all three. `check-handoff --all --allow-pending` **0** after the claim. **Close-out run**, on this content committed inside a clone before this sentence was written in: **304 / 1 / 0, exit 1** — 305 rows, 0 status flips against Phase 0 (the counter proved on a planted flip first), 9 rows differing only in numbers this session moved (the `**Model:**` bullets, now 50, and the model-report totals, now 321, in five rows; receipts, now 5, in two; the fixture's derived id, now S167; the ledger, then 55,225 B). Dashboard 76/100 at Phase 0. **NOT EXERCISED:** the merge (the maintainer's), and with it Test 9's flip; CI (none).
changelog_ref: CHANGELOG.md "2026-09-15 · [ad hoc] S166 close-out — PR #80's F2 and F3 published (push, description, reply); the maintainer's move next", plus the three action entries and the S166 claim entry
commit: 32c90db4 (claim) + 6e109e45 (record) + this close-out
```

**Self-assessment: 8/10.** Plus: **the publish went out exactly as drafted because Phase 0 re-derived what it
depended on** — the live description compared to the f1 file (so the maintainer had not edited it), the
fast-forward, `merge-tree`, and the diff size reproduced on both heads — before offering it. **Each
outward action was gated mechanically:** the push ran only inside a guard that re-checked all three
preconditions in the same command, and B waited on A's read-back — which is what caught #80's head still
reading `d4e1570` seconds after the push, before a description naming `aa36fd8` went out. Every read-back
compared bytes, not a success line. **Minus:** at Phase 0 I hit `git rev-parse --short a b`, the trap
S165's gotcha (7) names; I spent three calls finding the dashboard command because my grep assumed a
phrasing no ledger entry uses; and my record commit left §4's and §5's headings saying *"not pushed"*,
caught only when I gathered line numbers for this receipt. **Reduction:** none — `HANDOFFS.md` goes to
five receipts (S167 trims), and `CHANGELOG.md` is not trimmed, by the operator's decision. **No learning
row:** the head lag belongs to *"a CLI's success line is not the remote's state"*; recorded in memory, and
BL-53 leaves about three rows.

**Predecessor (S165): 9/10.** Its item (1) was a publish recipe that needed no edit: the three
preconditions (`d4e1570`, `9fa3141`, 2 comments) held and became the push's guard verbatim; the anchor
`docs/planning/pr80-review-response.md:59` was exact; and the drafted description and reply went out
unchanged — every figure I re-derived reproduced (+7,892 / −580). Gotcha (6), the live body's trailing
newline, set B's read-back comparison; (7) named the `rev-parse` trap I then hit anyway. **Not 10:** item
(4)'s *"S166's claim makes five and its Phase 0 trims to four"* is off by one — the rule counts at Phase 0,
before the claim, and this session had 19,499 B of room; read literally, it would have spent a trim and
three commits on nothing. And the dashboard command is recorded nowhere a grep reaches. **ROI: strongly
positive** — the session was the recipe.

```handoff
session: S165
date: 2026-09-15
status: complete
self_score: 8
predecessor_score: 9
active_task: **PR #80'S REVIEW, F3, IS DONE ON A LOCAL BRANCH AND HELD WITH F2 — NOTHING PUSHED; THE PUBLISH IS THREE GO-AHEADS.** Branch `pr80/f3-read-set-token-ceilings` = F2's `37740763` + **`aa36fd8b`**: the branch's root `.context-budget.json` holds `SESSION_RUNNER.md` and `SAFEGUARDS.md` to the 25,000-token read cap at measured densities (19,200 + 5,800 tokens), declares no `read-set` class ceiling, and drops `CHANGELOG.md` and `HANDOFFS.md` to `_deliberate_exclusions` — the operator's **R1 L1**, chosen from nine variants measured on the branch and on its merge into `upstream/main`. `--status` exits 0 on both trees (it exited 2). Drafted: the description with every figure re-derived, and one reply for F2 + F3. Recorded in [`docs/planning/pr80-review-response.md`](docs/planning/pr80-review-response.md) §5; the publish recipe is §3.
what_was_done: **Fork `main`: `8e0a7a72` claim (with the Phase 0 `dashboard_history.jsonl` snapshot); `d9ace03` the `HANDOFFS.md` retention trim, 60,236 → 37,186 B, S161 + S160 to `docs/archive/HANDOFFS-through-2026-09-11.md`, no `--force` (SRF 0.9383 after the claim); `ef55d77` the fold (18 trims, 150 receipts); `95a4845` the record — the response plan's header, §1, §3 and §5, `docs/planning/pr80-f3-variants.py`, `docs/planning/pr80-body-after-f3.md`, `docs/planning/pr80-reply-f2-f3.md`; this close-out. Branch: `aa36fd8b` (`.context-budget.json` and the branch's `CHANGELOG.md:95`, above F2's entry, below `main`'s); the worktree `../methodology-pr80-f3` removed once clean, the branch kept.** The four `OVER` rows were split into two decisions, and every answer was built as a config and run — `--status` plus six staged `--precommit` commits — on both trees before any was offered; the saved harness reproduces every row. Two findings shaped the choice: the review's (ii) cannot work as written, because `token_ceiling()` clamps every whole-read file to 25,000 tokens; and the merge is 967 B larger than the branch (upstream S16's `SAFEGUARDS.md` paragraph), so the description's headline row was stale — the merged pair is 68,548 B / 24,278 tokens, not 67,581 / 23,902 — and `SAFEGUARDS.md` went over its pin on the merged tree. Every measurement method first reproduced the figure it replaces (the doubled pair's 47,805; `+7,795 / −554`; the corpora 658,788 and 838,416). The config was edited by a script that asserted every touched line and checked the result against `HEAD` key by key, and the edited file itself was re-run on both trees before the commit.
next_steps: **(1) PUBLISH F2 + F3 — THREE GO-AHEADS, IN §3'S ORDER** (`docs/planning/pr80-review-response.md:59`): re-fetch; #80's head must still be `d4e1570`, `main` `9fa3141`, 2 comments. Push `pr80/f3-read-set-token-ceilings:read-set-budgets` (a fast-forward), PATCH the description from `docs/planning/pr80-body-after-f3.md`, post `docs/planning/pr80-reply-f2-f3.md`, reading each back before the next. If anything moved, re-derive per §3 — the two `max_tokens` too if `main` touched the runner or `SAFEGUARDS.md`. **(2) F5 AND F6** after the merge (§6), or as the maintainer asks. **(3) BL-57's P1** after #80's F-items, from #80's then-current head; **D8 (ii) is now done inside #80** (`CHANGELOG.md` left upstream's root budget at `aa36fd8b`, and `HANDOFFS.md` with it, past D7) — amend the plan when P2 is planned. **(4) `HANDOFFS.md` HOLDS FOUR RECEIPTS** after this close-out; S166's claim makes five and its Phase 0 trims to four. The last trim's relief is 23,050 B, so `SRF_RED` returns only at 60,236 B — measure the room against the stub, as this session did. **(5) CARRIED:** pushing fork `main` (8 ahead of `origin/main` after this close-out); S161's merge-options (b)/(c); BL-54; the two stale planning documents; `HOW_TO_USE.md:774`; BL-36; Test 31; BL-53 (~3 rows); `choose_cut`; nine merged `origin` branches. Each push and deletion is its own go-ahead.
key_files: At `aa36fd8b`: `.context-budget.json:26` (the `read-set` class, no ceiling), `.context-budget.json:44` and `:46` (the runner's 19,200-token ceiling), `.context-budget.json:52` and `:54` (`SAFEGUARDS.md`'s 5,800-token pin), `.context-budget.json:72` (`_deliberate_exclusions`, the ledgers), `CHANGELOG.md:95` (the branch entry); `starter-kit/context_budget.py:112` (`token_ceiling`), `:139` (`framework_share`), `:166` (`class_ceiling`), `:1000` (`precommit`). Fork `main`: `docs/planning/pr80-review-response.md:59` (§3, the publish recipe), `:160` (§5, F3's record); `docs/planning/pr80-body-after-f3.md:17` (the headline row), `:37` (the config paragraph); `docs/planning/pr80-reply-f2-f3.md:1`; `docs/planning/pr80-f3-variants.py:132` (`VARIANTS`); `docs/planning/changelog-rules-contradictions-plan.md:143` (D8); `HANDOFFS.md:45` (18 trims, 150 receipts).
gotchas: **(1) "WITH THIS MERGE" IS A PROPERTY OF THE MERGE RESULT, NOT OF THE BRANCH** — `main` moved after the description was measured, and the merge takes its `SAFEGUARDS.md` (+967 B); measure such claims on `git merge-tree`'s tree or a merged clone. **(2) (ii) IS UNSATISFIABLE FOR A WHOLE-READ LEDGER** — `token_ceiling()` clamps to 25,000 tokens whatever `max_bytes` says; a ledger must leave the class or the budget. **(3) THE TOKEN CEILINGS ARE TYPED AGAINST 25,000 AND PINNED TO `main`'s `SAFEGUARDS.md` AT `9fa3141`** — they follow neither `read_cap_tokens` nor a later `main` edit; re-measure by the doubled-file method (a file under the cap needs more copies: `SAFEGUARDS.md` took seven). **(4) `open(p, "w").write(f(open(p).read()))` TRUNCATES BEFORE IT READS** — Python evaluates the receiver first; read, close, then write. **(5) macOS `sed -E` HAS NO `\s`** — a flip counter read 0 until a planted flip exposed it; plant a known change before trusting a zero. **(6) THE LIVE BODY IS `pr80-body-after-f1.md` PLUS ONE TRAILING NEWLINE** (verified); `pr80-body-after-f3.md` was built from the f1 file, not normalized. **(7) `git rev-parse --short a b` FAILS** — one revision per call.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`,** in `--no-local` clones, every exit code read bare. **Fork:** Phase 0 at `5235d4b` **304 / 1 / 0, exit 1** (Test 9, pre-existing); after the trim and fold, at `ef55d775`, **304 / 1 / 0, exit 1** — 305 rows, 0 status flips (the counter proved on a planted flip), 11 rows differing only in numbers the trim moved; the shard's `.verify.sh` exit 0 at `d9ace03` and after the fold; `check-handoff --all` 0. **Branch:** `37740763` (control) and `aa36fd8b` each **115 / 1, exit 1** — 116 rows, 0 status flips, 0 rows differing; unit suites 211 · 123 (2 skipped) · 116 (2 skipped) OK on both; `check-links` OK (105 / 23); `check-learnings` OK (13 rows). **The config itself:** `context_budget.py --status` **exit 0** on the branch and on its merge into `upstream/main` (it was 2); `--json` and `--selftest` exit 0; the six `--precommit` commits as recorded; `merge-tree` against `9fa3141` clean; the push a fast-forward. **Close-out run**, on this content committed inside a clone before this sentence was written in: **304 / 1 / 0, exit 1** — 305 rows, 0 status flips against Phase 0 and against the post-fold run (the counter proved on a planted flip first), 7 rows differing only in numbers this session moved (the `**Model:**` bullets, now 49; the fixture's derived id, now S166; the ledger, then 45,610 B; the model-report totals, now 320). Dashboard 76/100 at Phase 0. **NOT EXERCISED:** the budget gate wired as a hook (nothing wires it); GitHub (nothing published); CI (none).
changelog_ref: CHANGELOG.md "2026-09-15 · [ad hoc] S165 close-out — PR #80's F3 done on a local branch, held with F2 for one publish; three go-aheads next", plus the record, fold, trim and claim entries
commit: 8e0a7a72 (claim) + d9ace03 (trim) + ef55d77 (fold) + 95a4845 (record) + this close-out; branch aa36fd8b
```

**Self-assessment: 8/10.** Plus: **every answer was run before any was offered** — nine configs, both
trees, `--status` and six staged commits each — and that turned up the two findings that shaped the
choice: the maintainer's (ii) is unsatisfiable for a whole-read ledger, and the merge is 967 B larger than
the branch the description measured. **Every measurement method reproduced a recorded figure before its
new number was trusted** (the doubled pair's 47,805 exactly; `+7,795 / −554`; 658,788 and 838,416), and the
edited config was re-run from the file itself before the commit, then diffed row for row against a
same-session control. The trim needed no `--force`, as the Phase 0 measurement said. **Minus: four slips
in my own instruments**, each caught by my own checks before anything was committed or published — a
commit guard that compared a locale-sorted path list to a hand-ordered one (the trim waited a round); a
one-line read-modify-write that truncated a scratch config before reading it; a flip counter blind under
macOS `sed` until a planted flip exposed it; and a trailing-newline "normalization" that dropped a byte
of the published description. The saved harness's docstring also first omitted the ledger refusals in
two rows — caught by re-running the saved file against its own claims. **Reduction:** `HANDOFFS.md`
trimmed to four receipts; nothing else removed. **No learning row:** gotcha (1) is Learning #61's
*"re-derive at publish time"* with a sharper object — the merge result — and BL-53 leaves about three
rows; recorded in memory.

**Predecessor (S164): 9/10.** Its item (1) framed F3 exactly as this session had to take it — the
maintainer's three answers plus a fourth, *"explain in prose, take a letter"*, commit on `37740763`,
re-fetch first — and every anchor held (`docs/planning/pr80-review-response.md:145`; the branch's
`CHANGELOG.md:95`). Its gotchas paid off one by one: (2) the base commit; (3) the ledger placement; (4)
the live body's trailing newline, reproduced to the byte; (5) the `--no-local` clone without `upstream/*`
refs, which the merged clone needed; (6) the `gh api` PATCH, carried into §3. Its baselines reproduced
exactly (304/1/0; 115/1; 211 · 123 · 116). **Not 10:** §5's table measured one tree, the branch, so the
drift on the merge side was left to this session to find; and item (3) carried S163's *"`SRF_RED` will
refuse"* — correctly labelled an estimate — when S164's own close-out could have measured it (2,629 B of
room against a ~2 KB claim). **ROI: strongly positive.**

```handoff
session: S164
date: 2026-09-15
status: complete
self_score: 8
predecessor_score: 9
active_task: **PR #80'S REVIEW, F2, IS DONE ON A LOCAL BRANCH AND HELD — NOT PUSHED, SO F2 AND F3 GO UP IN ONE PUSH AND ONE REPLY.** Branch `pr80/f2-installed-source-guard` = #80's head `d4e1570` + one test-only commit, **`37740763`**: `test_a_synced_repo_with_each_installed_source_file_is_still_doc_only` writes every non-markdown file `bin/sync` installs, from its real `starter-kit/` source, into a doc-only fixture and asserts the exclusion holds, per file and all together. RED first on the review's own mutant (old suite 211 OK; new test `2181 != 0` source LOC). Recorded in [`docs/planning/pr80-review-response.md`](docs/planning/pr80-review-response.md) §4. **F3 is next and starts with an operator decision (§5).**
what_was_done: **Fork `main`: `8791a272` claim (with the Phase 0 `dashboard_history.jsonl` snapshot); `95d84cfd` the response plan's §4 and corrected header, `docs/planning/pr80-f2-mutants.py`, the preparation entry; this close-out. Branch: `37740763`, its entry in the branch's own ledger (`CHANGELOG.md:95` there), above F1's and below `main`'s; `git merge-tree` against `9fa3141` clean, and the push would fast-forward `read-set-budgets`.** The test is generalized in place, not added beside the old one. Its names come from `bin/_manifest.py`, not `FRAMEWORK_INSTALLED_SOURCE`, so a fifth name is covered without anyone adding it; a last assertion checks it covered exactly the scanner's list. `.context-budget.json` is covered, not excluded: it is `config` before the predicate runs, so a direct `is_framework_installed` call holds its signatures and its category is asserted. **Six mutants, both twins, old and new suites, run twice:** M1 (the review's), M4 (the `.json` signatures) and M6 (the one `collect_all` call site narrowed) pass the old suite and fail the new test; M2 and M5 were caught already and still are. **M3 — the scanner's own entry — is not caught by this test:** the neutralized strings land in the scanner's own signature table, so the real file matches itself; twelve stand-in tests catch it, and the docstring says so. The saved mutants script was proved to plant byte-identical mutants to the one the round ran. The worktree `../methodology-pr80-f2` was removed once clean; the branch stays.
next_steps: **(1) F3 — ITS OWN SESSION, STARTING WITH AN OPERATOR DECISION** (`docs/planning/pr80-review-response.md:145`): the maintainer's three answers — the read-set ceiling in tokens at measured density; ledger ceilings where the ledgers are; *"over at install, by design"* — plus a fourth, dropping the ledgers from the read budget as this fork did at `3c8acd5`. Explain in prose, take a letter. **Commit F3 on top of `37740763`** (branch `pr80/f2-installed-source-guard`), not on `d4e1570`. **Re-fetch first and read any new comment on #80**; if its head moved, rebase both. **(2) THEN PUBLISH F2 + F3 TOGETHER — three go-aheads, in §3's order:** push (a fast-forward), the description (F2 moves no figure in it; F3 may), one reply covering both (§4's mutant table is F2's paragraph). **(3) `HANDOFFS.md` HOLDS FIVE RECEIPTS** after this close-out, so S165's Phase 0 trims to four; S163 estimated `SRF_RED` will refuse, and any `--force` is its own ask — re-derive after the claim. **(4) BL-57's P1** after F3, from #80's then-current head. **(5) CARRIED:** S161's merge-options (b)/(c); BL-54; the two stale planning documents; `HOW_TO_USE.md:774`; BL-36; Test 31; BL-53 (~3 rows); `choose_cut`; nine merged `origin` branches; pushing fork `main` (3 ahead of `origin/main` after this close-out). Each deletion and the push is its own go-ahead. **(6) F5, F6 and the Markdown-only citation sweep** can follow the merge.
key_files: At `37740763`: `tools/test_methodology_dashboard.py:2666` (the generalized test), `tools/test_methodology_dashboard.py:2642` (the name-vs-signature gate), `tools/test_methodology_dashboard.py:2653` (`context_budget.py`'s real-artifact guard), `CHANGELOG.md:95` (the branch entry); the unchanged scanner: `starter-kit/methodology_dashboard.py:360` (`FRAMEWORK_INSTALLED_SOURCE`), `:468` (`_FRAMEWORK_FILE_SIGNATURES`), `:484` (`methodology_trim.py`), `:508` (`.context-budget.json`), `:873` (the one call site). Fork `main`: `docs/planning/pr80-review-response.md:81` (§4, F2's record), `:145` (§5, F3's decision), `:58` (§3, the publish order); `docs/planning/pr80-f2-mutants.py:1` (the six mutants and the commands); `HANDOFFS.md:45` (17 trims, 148 receipts).
gotchas: **(1) A REAL-ARTIFACT FIXTURE CANNOT FAIL A MUTATION OF A DETECTOR THE ARTIFACT CARRIES** — neutralizing `methodology_dashboard.py`'s signatures writes the new strings into its own table, so the real file still matches (M3). My first docstring claimed otherwise, written before M3 ran; the round caught it. Say which mutants a test kills only after running them. **(2) F3 BUILDS ON `37740763`**, not `d4e1570`, or the branches diverge and the push stops being a fast-forward; `pr80/f1-learnings-1-13` still equals `upstream/read-set-budgets` (`d4e1570`). **(3) BRANCH LEDGER ENTRIES GO WITH #80'S BLOCK — ABOVE F2'S AT `:95`, BELOW `main`'S**; the branch's hook refuses a commit without `CHANGELOG.md`. **(4) THE LIVE PR BODY DIFFERS FROM `docs/planning/pr80-body-after-f1.md` BY ONE TRAILING NEWLINE** that `gh api --jq` adds — compare after stripping it, not with `cmp`. **(5) A `--no-local` CLONE LACKS `upstream/*` REFS** — clone with `-b <local branch>` and check `HEAD` before running anything. **(6) `gh pr edit` FAILS** — use `gh api -X PATCH`.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`,** in `--no-local` clones, every exit code read bare. **Branch:** `d4e1570` (control) and `37740763` each **115 passed / 1 failed, exit 1** — 116 rows, 0 status flips, 0 rows differing (Test 9, pre-existing); unit suites 211 · 123 (2 skipped) · 116 (2 skipped) OK on both; `check-links` OK (105 / 23) and `check-learnings` OK (13 rows) on both. Mutation round: 14 runs, twice, identical. **Fork:** Phase 0 at `755ef09` **304 / 1 / 0, exit 1**; `check-handoff --all --allow-pending` **0** after the claim; at the record commit `95d84cfd`, **304 / 1 / 0, exit 1** — 305 rows, 0 status flips, 3 rows differing only in numbers this session moved (receipts 4 → 5, the ledger's bytes). **Close-out run**, on this content committed inside a clone before the run results were written in and two citations corrected (`:144` → `:145`): **304 / 1 / 0, exit 1** — 305 rows, 0 status flips against Phase 0, 9 rows differing only in numbers this session moved (the live `**Model:**` bullets, now 46; receipts, now 5; the fixture's derived id, now S165; the ledger, then 58,238 B; the model-report totals, now 317). **NOT EXERCISED:** a real `bin/sync` into a real adopter (the test writes the installed files itself; the scanner reads only files); CI (none); GitHub (nothing published).
changelog_ref: CHANGELOG.md "2026-09-15 · [ad hoc] S164 close-out — PR #80's F2 done on a local branch and held for one push with F3; F3 next", plus the preparation entry and the S164 claim entry
commit: 8791a272 (claim) + 95d84cfd (record) + this close-out; branch 37740763
```

**Self-assessment: 8/10.** Plus: **the review's claim was reproduced before anything was trusted** — the
old suite stays 211 OK under the maintainer's mutant — and the new test fails it with his symptom,
`2181 != 0` source LOC. **The test takes its names from the manifest**, the class's own convention for
fixtures, which answered the *"cannot enforce"* S163 left in §4 instead of carrying it forward. **Each
half of the test was shown live on its own:** M4 kills only the direct call, M6 only the end-to-end
half. The round ran twice, every mutant was asserted to apply once per file, the saved script was proved
to plant the same mutants, and the branch commit was diffed row for row against a same-session control.
The publish was held, not asked for, as Phase 0 suggested. **Minus: my first docstring claimed RED
against the neutralization of *every* name before M3 had run** — a forward claim from expectation,
caught only by my own round; the scanner carries its own signature table, which I had read this session
and not connected. The response plan still said nothing had been pushed, a staleness I found only when I
edited it. **Reduction:** none — `HANDOFFS.md` goes to five receipts (S165's Phase 0 trims), and
`CHANGELOG.md` is not trimmed, by the operator's decision. **No learning row:** M3 belongs to Learning
#12's *"ask what a fixture makes unreachable"*, and BL-53 leaves about three rows; recorded in memory.

**Predecessor (S163): 9/10.** Its item (1) put this session straight into execution: every anchor held
at `d4e1570` — `tools/test_methodology_dashboard.py:2666`, `:2642`, `:2653`;
`starter-kit/methodology_dashboard.py:360`, `:468`, `:484`, `:508` — and §4's recipe (*"plant the mutant
… in a clone, show the current suite stays green and the new parametrized test goes red"*) is what I
ran. Its question on `.context-budget.json` was the right one, and its *"cannot enforce"* line named the
gap the manifest-driven design closes. Gotcha (4) placed the branch entry first time, and the baselines
it recorded (115/1; 211 · 123 · 116, 4 skipped; 105 links) reproduced exactly at `d4e1570`. **Not 10,
for two stale statements:** the response plan's header still read *"Nothing below has been pushed,
edited on the PR, or posted"* after S163 had done all three, and its receipt still carried *"pushing fork
`main`"*, which its own follow-up discharged. Neither cost more than a minute. **ROI: strongly
positive.**

```handoff
session: S163
date: 2026-09-15
status: complete
self_score: 8
predecessor_score: 7
active_task: **PR #80'S REVIEW, F1, IS ANSWERED AND PUBLISHED — OPTION (a), THE OPERATOR'S CHOICE.** `KJ5HST/methodology:read-set-budgets` fast-forwarded `b82dcff..d4e1570`: `5c9f0f3` states the rule where eight citations of Learnings past #13 stood, then `d4e15706` cuts `starter-kit/FRAMEWORK_LEARNINGS.md` to rows 1–13 plus the reserved `#14` (56,673 → 13,983 B). The description is updated and the reply posted ([comment](https://github.com/KJ5HST/methodology/pull/80#issuecomment-5676599724)); #80 is `MERGEABLE`/`CLEAN` at `d4e15706`. **F2 and F3 are next, set up in [`docs/planning/pr80-review-response.md`](docs/planning/pr80-review-response.md) §4–§5.** `HANDOFFS.md` is back to four receipts, forced past `SRF_RED` on the operator's decision.
what_was_done: **Fork `main`: `9f66ebd9` claim (with the Phase 0 `dashboard_history.jsonl` snapshot); `42e52f9` the response document, the description and reply to publish, and the BL-57 plan amendment; `ae44dec9` the forced trim; `b9091fe` the three outward actions recorded; `49685a9` the fold; this close-out. Branch `pr80/f1-learnings-1-13`, pushed: `5c9f0f3`, `d4e15706`, each with an entry in the branch's own ledger placed with #80's block, below `main`'s — the maintainer's rule for keeping `main`'s prepends clean; `git merge-tree` against `9fa3141`: no conflicts.** Phase 0 found the review public (F1 a decision, F2/F3 fixes, F4–F6 can follow) and the trim refusing. Asked what F1 meant, I measured what (a) would break: `bin/check-learnings` sweeps only distributed Markdown, so two citations in the distributed `starter-kit/context_budget.py` would have dangled silently. The citation edits were proved comment-only — AST identical to `b82dcff` in two files, two docstrings in the third. **Publishing, on the operator's go-ahead:** the push; then `gh pr edit` failed on the Projects (classic) GraphQL deprecation and changed nothing, so the guarded reply was held; the REST `PATCH` read back equal to the file, and only then was the reply posted, and read back equal. **Trim:** `--cut 4 --force --write` archived S159 and S158 to `docs/archive/HANDOFFS-through-2026-09-10.md` (61,471 → 41,455 B). **The BL-57 plan** now says it is approved (its header read DRAFT) and that no row past #13 will exist upstream; its P1 step 5 states Learning #19's rule instead of citing it.
next_steps: **(1) F2 — ITS OWN SESSION** (`docs/planning/pr80-review-response.md:79`). Generalize `tools/test_methodology_dashboard.py:2666` (at `d4e15706`) over every `FRAMEWORK_INSTALLED_SOURCE` name (`starter-kit/methodology_dashboard.py:360`), with the real `starter-kit/` file, RED first on the maintainer's mutant: `methodology_trim.py`'s `version_re` and signatures neutralized in both twins. Decide how `.context-budget.json` (config, never source) is treated. Commit from #80's current head; the push is its own go-ahead. **Re-fetch first and read any new comment on #80.** **(2) F3 — STARTS WITH AN OPERATOR DECISION** (`docs/planning/pr80-review-response.md:102`): the maintainer's three answers, plus a fourth this fork already took — drop the ledgers from the read budget (`3c8acd5`), which BL-57's Q2 A argues anyway. Explain in prose; take a letter. **(3) BL-57's P1** after F2/F3 or when the operator chooses — from #80's current head, not `b82dcff` (`docs/planning/changelog-rules-contradictions-plan.md:15`). **(4) CARRIED:** S161's merge-options (b)/(c); BL-54; the two stale planning documents; `HOW_TO_USE.md:774`; BL-36; Test 31; BL-53 (~3 rows); `choose_cut`; nine merged `origin` branches; pushing fork `main` (59 ahead before this close-out). Each deletion and the push is its own go-ahead. **(5) F5, F6 and the Markdown-only citation sweep** can follow the merge (response document §6; the reply names the sweep).
key_files: `docs/planning/pr80-review-response.md:56` (§3 publish commands), `:79` (§4 F2), `:102` (§5 F3). `docs/planning/pr80-body-after-f1.md:1` (the description as published), `docs/planning/pr80-reply-f1.md:1` (the reply as posted). At `d4e15706`: `starter-kit/FRAMEWORK_LEARNINGS.md:20` (the reworded `#14` note), `starter-kit/context_budget.py:77`, `:378`, `:409` (the repaired citations), `bin/check-learnings:255` (`distributed_md_files`, `.md` only), `tools/test_methodology_dashboard.py:2642` (the name-completeness gate), `.context-budget.json:26` (the read-set class). `docs/planning/changelog-rules-contradictions-plan.md:15` (the S163 amendment), `:371` (P1 step 5). `HANDOFFS.md:45` (17 trims, 148 receipts).
gotchas: **(1) `gh pr edit` FAILS ON THE PROJECTS (CLASSIC) GRAPHQL DEPRECATION** (exit 1, nothing changed). Use `gh api -X PATCH repos/KJ5HST/methodology/pulls/80 -F body=@<file>`, and gate each dependent outward action on the read-back of the one before — that gate stopped a reply claiming a description update that had not happened. **(2) `bin/check-learnings` SWEEPS ONLY `.md`** — a citation in a distributed `.py` is invisible to it; `git grep -i -E 'learnings? #[0-9]+'` as well. **(3) `context_budget.py --status` WRITES AN UNTRACKED `.context-budget-history.jsonl`** into the tree it measures; never commit it. **(4) BRANCH LEDGER ENTRIES GO WITH #80'S BLOCK, BELOW `main`'S** — a top prepend re-conflicts; run `git merge-tree` before any push. **(5) `HANDOFFS.md` QUOTES ITS OWN FENCE (`:15`)** — my first front-matter measure matched it and read 1,178 B for 6,605; anchor to line start. **(6) THE NEXT TRIM MAY REFUSE AGAIN — an estimate:** this trim's relief is 20,016 B, so `SRF_RED` fires once the file regrows to 61,471 B; S164's close-out leaves ~61 KB and S165's claim stub likely crosses it. Each `--force` is its own ask (the operator chose A, not B).
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`** in `--no-local` clones, every exit code read bare. **Branch:** `b82dcff` (control), `5c9f0f3` and `d4e15706` each **115 passed / 1 failed, exit 1** — 116 rows, 0 status flips, 0 rows differing even in a number (Test 9, pre-existing); unit suites 116 + 211 + 123 OK (4 skipped) on all three; `check-links` OK (105 links, 23 files); `check-learnings` 46 → 13 rows OK, and a `Learning #20` planted in `starter-kit/SAFEGUARDS.md` is caught. **Fork:** Phase 0 at `022d40a` **304 / 1 / 0, exit 1**; at `42e52f9` **304 / 1 / 0** — 305 rows, 0 flips, 8 differing only in numbers this session moved. Shard proof exit **0** at `ae44dec9` and after `49685a9`; `check-handoff --all --allow-pending` **0** (4 receipts). **GitHub:** the push, the description and the reply each read back. **Close-out run, on this content committed inside a clone (this sentence added after it): 304 / 1 / 0, exit 1 — 305 rows, 0 status flips against the Phase 0 baseline, 11 rows differing only in numbers this session moved** (the live `**Model:**` bullets, now 45; receipts, now 4; the fixture's derived id, now S164; the front matter, 6,605 B; the ledger, then 48,732 B). **NOT EXERCISED:** any adopter (no adopter file touched); CI (none).
changelog_ref: CHANGELOG.md "2026-09-15 · [ad hoc] S163 close-out — PR #80's F1 answered and published; F2 and F3 next", plus the fold entry, the three outward-action entries, the tool's trim entry, the preparation entry and the S163 claim entry
commit: 9f66ebd9 (claim) + 42e52f9 (response, description, reply, plan) + ae44dec9 (trim) + b9091fe (outward actions) + 49685a9 (fold) + this close-out; branch 5c9f0f3 + d4e15706
```

**Self-assessment: 8/10.** Plus: **Phase 0 found the two facts S162's handoff did not carry** — the review
had been public for an hour before S162 closed, and the trim would refuse — and put both to the operator
as decisions rather than proceeding on the handoff. **F1 was explained with its costs measured**,
including the dangling citations a green check would have hidden. **Every edit was proved to be what it
claimed:** comment-only by AST, each commit green on its own, 0 flips row for row, the citation sweep
mutation-tested, the ledger placement checked with `git merge-tree` before the push. **Every outward
action was read back, and the reply was gated on the description** — which is what stopped a false *"the
description now matches"* when `gh pr edit` failed. **Minus:** my first inventory regex missed the
lowercase *"learning #22 / #26a"*; the response document carried five wrong line numbers or figures and
the plan note a wrong section, all caught by my pre-commit destination grep rather than written right;
my first front-matter measure matched a quoted fence, a trap my own notes name; and I first scoped
option B as F2 + F3 before seeing that F1 (a) is itself an edit. **Reduction:** `HANDOFFS.md` 61,471 →
41,132 B before this receipt, two receipts archived; `CHANGELOG.md` not trimmed, by the operator's
decision. **No learning row:** the Markdown-only sweep is the family of Learnings #10, #24 and #43, and
BL-53 leaves about three rows.

**Predecessor (S162): 7/10.** Its item (1) and key files were exact — P1 at the plan's `:352`, the
`b82dcff` baselines reproduced to the row (115/1, 450 unit tests, 105 links) — and gotchas (1) and (6)
were used as written. **Not 8, for two claims about state that were wrong or incomplete when written.**
Item (4) calls #80's review *"private (F1–F3)"*; it had been posted on the PR at 04:19 UTC, 59 minutes
before S162's close-out commit (05:18 UTC), with six findings, and it changed this session's
deliverable. Item (2) predicted a routine trim without saying it would refuse, though that was
computable: the last trim had archived one receipt of 8,065 B, and S162's own record was 9,106 B. The
plan's header also still read *"DRAFT awaiting the operator's approval"*. **ROI: positive** — the plan
and the key files were right; each miss cost one Phase 0 question.

```handoff
session: S162
date: 2026-09-14
status: complete
self_score: 7
predecessor_score: 8
active_task: **THE BL-57 PLAN IS WRITTEN, REVIEWED, APPROVED BY THE OPERATOR AND COMMITTED — [`docs/planning/changelog-rules-contradictions-plan.md`](docs/planning/changelog-rules-contradictions-plan.md) (`9292132e`).** It removes the contradictions in the framework's `CHANGELOG.md` rules — sixteen findings across fourteen files — here and in six adopters, through a new upstream PR once #80 merges. The operator answered four questions, all A: the rules move to one synced home (`FRAMEWORK_APPARATUS.md` §The Action Ledger) and the seed becomes a linked pointer with a format marker; archiving is optional; `[BL-<id>]` takes any backlog id; one entry per commit, never edited. D5–D10 were approved with the plan. **Claimed 2026-09-14, closed 2026-09-15. Planning only — nothing implemented; fork-internal — nothing pushed, no PR, no comment.**
what_was_done: **Four commits: `7ea7346b` claim (with the Phase 0 `dashboard_history.jsonl` snapshot), `9292132e` the plan, `64f085b2` Learning #65, and this close-out.** Phase 0 found that upstream had moved that day: PR #81 merged, the maintainer ran S13–S17, and PR #80's head went `598c459` → `b82dcff`. **The inventory** is `git grep` over three trees (`b82dcff`, `upstream/main`, fork `main`) with twelve patterns — 1,577 lines in 45 files on `b82dcff`, each classified — plus six adopters measured read-only: sizes, rules text, tag families, sync state, `CLAUDE.md` ledger rules, and a conformance count under the old and the new tag rule. **The decisions:** the operator asked for the options to be explained in chat before choosing, then chose Q4 A on a measured A-versus-B comparison (fork: 56 of 60 ledger commits were pure insertions; upstream: every S13–S17 entry was rewritten at close-out, and S16's rewrite deleted ten entries). **An independent read-only reviewer** found 4 errors, 9 risks and 6 nits in the first draft; I reproduced each before fixing it and recomposed the plan rather than patching it. My own checks then caught two line ranges I had cited from memory. The plan's checkers were mutation-tested: §9.3 caught 4 of 4 mutants, §9.8 both kinds of entry damage. **Backlog:** BL-57's row and note point at the plan; BL-47's `CHANGELOG.md` half is recorded as settled by Q2 A; BL-56 is recorded as folded into P6.
next_steps: **(1) THE PLAN'S P1 — its own session** (`docs/planning/changelog-rules-contradictions-plan.md:352`). Create branch `bl57/changelog-rules` from `b82dcff` in a worktree; move the seed's three rule sections verbatim into `FRAMEWORK_APPARATUS.md` §The Action Ledger; make the seed thin; key `CHANGELOG.md` on the new marker; fix the stale-seed advice (C16). **Re-fetch first:** if #80's head has moved past `b82dcff`, branch from the new head. The commit order and every DONE check are in the plan. **(2) `HANDOFFS.md` HOLDS FIVE RECEIPTS** after this close-out, and its headroom to the 65,536 B ceiling is less than one receipt of the usual size — its own policy (`HANDOFFS.md:15`) trims to four at the next Phase 0. That trim is its own action; re-derive its dry run after the claim. **(3) CARRIED, unchanged:** S161's merge-options parts (b) and (c); BL-54's fix; the two stale planning documents; `HOW_TO_USE.md:774`; BL-36; Test 31; BL-53 (about three rows of room after #65); `choose_cut`; the nine merged `origin` branches; pushing `main`. Each deletion and the push is its own go-ahead. **(4) UPSTREAM TO WATCH:** #80's private review (F1–F3), quality-ratchet Phase 1 and the proposed heading-count ratchet (plan C9) all touch this plan's files — compute conflicts with `git merge-tree` at P12.
key_files: `docs/planning/changelog-rules-contradictions-plan.md:17` (§0 the answer), `:40` (§1.1 the sixteen findings), `:110` (§2.1 the decisions), `:154` (§3.1 the home's outline), `:257` (§4.2 the sites that change), `:308` (§4.4 the adopters), `:352` (P1, the next session), `:591` (P12), `:697` (§9 the commands). `starter-kit/CHANGELOG.md:94` (the size section P1 moves); `starter-kit/HANDOFFS.md:89` (the heading that becomes its marker); `bin/_manifest.py:95` on `b82dcff` (the markers P1 changes); `starter-kit/FRAMEWORK_LEARNINGS.md:97` (row 65); `docs/planning/BACKLOG-DETAIL.md:1697` (BL-57).
gotchas: **(1) A `--no-local` CLONE HAS NO `upstream/*` REFS.** `git checkout b82dcff` failed in one, the `&&` chain skipped `bin/tests.sh` silently, and the next command ran the unit suite on fork `main` and printed exit 0. Fetch the ref into the clone first (plan hazard 12). **(2) zsh ABORTS ON AN UNMATCHED GLOB** — the shard-spanning audit printed 0 where bash gives 43; the plan publishes a `$(git ls-files …)` form instead (K8). **(3) THE `$R:path` TRAP BIT AGAIN**, although S161's gotchas name it: `$R:starter-kit/…` is a history modifier. **(4) AIM A MUTANT AT THE UNIT IT TESTS** — my first mutation of the §9.3 checker changed section 1 and checked section 2, so its "VERBATIM" proved nothing. **(5) EXPLAIN A HARD CHOICE IN PROSE FIRST** — the operator declined a four-question picker and asked *"chat; explain the differences among these choices"*, then answered by letter. **(6) `bin/tests.sh` MUTATES BOTH LIVE LEDGERS** — clone only.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`** in `--no-local` clones. Phase 0 baseline at `3745748`: **304 passed / 1 failed / 0 skipped, exit 1** (Test 9, pre-existing). Plan-time baseline at `b82dcff`, with the ref fetched into the clone: **115 / 1, exit 1** (Test 9); unit suites 450 tests OK (4 skipped); `check-links` OK, 105 links in 23 files. Bare, live tree at close-out: `check-learnings` **0** (64 rows, 0 over 1,500 B); `BACKLOG-DETAIL.md.verify.sh` **0**; the links the plan and the backlog add resolve. **Close-out run, on this content committed inside a clone (this sentence added after it): 304 / 1 / 0, exit 1 — 305 rows, 0 status flips against the Phase 0 baseline, 10 rows differing only in numbers this session moved** (the live `**Model:**` bullets, now 43; receipts, now 5; the fixtures' derived ids, now #66 and S163; the ledger, then 59,109 B). `check-handoff` **0** and `--all` **0** (5 receipts; this record 8,667 B of 12,288 B before this sentence). **NOT EXERCISED:** any adopter (read-only surveys and scratch copies only); the branch the plan creates; GitHub.
changelog_ref: CHANGELOG.md "2026-09-15 · [BL-57] S162 close-out — the BL-57 plan approved and committed; P1 is next", plus the Learning #65 entry, the plan entry and the S162 claim entry
commit: 7ea7346b (claim) + 9292132e (the plan) + 64f085b2 (Learning #65) + this close-out
```

**Self-assessment: 7/10.** Plus: **the inventory ran on the upstream target tree, not only on fork
`main`**, so the plan's line numbers are the ones an upstream PR will meet. It found eight findings
BL-57 did not list, among them the structural cause — rules inside a seed — that made Q1 the decision
the rest hangs on. **The four decisions are the operator's**, taken after an explanation the operator
asked for, and Q4 on a measured comparison rather than on my preference. **Every finding of the
independent review was reproduced before it was fixed**, the plan was recomposed rather than patched,
and its checkers were shown to fail on planted mutants. **Minus: the first draft carried four errors in
its own DONE criteria** — a test the thin seed breaks, a grep that could never print nothing, adopter
criteria that could not be met, and an audit that returns 0 under zsh. The reviewer found them, not I,
and each was a forward claim of the kind Learning #13 says to compute, not write. My first baseline
attempt failed silently, and I nearly took the unit suite's exit 0 on fork `main` for `b82dcff`'s. The
zsh trap S161 named still cost a call; my first mutant was aimed at the wrong section; two line ranges
I cited from memory were wrong; and my first question packed four decisions into terse options, which
cost the operator a round trip. **Reduction:** none. `HANDOFFS.md` goes to five receipts, and its policy
trims at the next Phase 0; `CHANGELOG.md` is not trimmed, by the operator's decision.

**Predecessor (S161): 8/10.** Its item (1) named the deliverable and where to start. BL-57, which it
raised after close-out, carried eight contradictions with citations and an adopter table, and every
one of the eight held when re-read on `b82dcff`. Gotcha (8) spared this session S161's own regression:
my claim stub carried `path:line` tokens and passed `check-handoff --all --allow-pending` first time.
Gotchas (6) and (7) were used as written. **Not 9, for two small inaccuracies in BL-57:** contradiction
1's dashboard clause (`starter-kit/methodology_dashboard.py:259`) rests on a premise the same file's
comment at :325–345 already rejects, and its `nprcgenekeepr` range (:3946–:3983) is the start of a
block that runs to :4065. Its zsh gotcha (3) was right; I still hit the trap. **ROI: strongly
positive** — BL-57 was most of this plan's starting inventory.

