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

**Archived shards — 15 trims, 145 receipts.** Every shard is `docs/archive/HANDOFFS-through-<date>.md`
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

<!-- NEXT TRIMMING SESSION: methodology_trim.py appends a 3-line pointer block here
     (starter-kit/methodology_trim.py:1093 build_pointer_block, :1103 insert_pointer). Fold it into
     the table above as one row (~125 B vs the block's ~448) and delete the block, IN ITS OWN
     COMMIT: inside the trim commit the shipped .verify.sh fails L2 (Learning #58). The generator
     is DISTRIBUTED, so teaching it this is an upstream change. -->

```handoff
session: S160
date: 2026-09-11
status: complete
self_score: 8
predecessor_score: 8
active_task: **`HANDOFFS.md` IS BACK TO FOUR RECEIPTS — 59,110 → 37,492 B through claim, trim and fold — AND ITS ARCHIVE TABLE NO LONGER CARRIES A `proof` COLUMN.** Retained S160, S159, S158, S157; **S156 and S155 are frozen in [`docs/archive/HANDOFFS-through-2026-09-09.md`](docs/archive/HANDOFFS-through-2026-09-09.md)**, its `.verify.sh` **exit 0, pinned to the trim commit `cd52df79`, re-run after the fold and still 0**. **Operator decision at Phase 0: pay for the fold by dropping the derivable `proof` column rather than cutting more prose** — front matter **6,351 of the 7,168 B reserve, 817 B spare**; the last two folds each had to cut ~190 B. **Fork-internal: nothing pushed, no PR, no comment, no distributed file touched.** PR #80 at Phase 0: OPEN, `MERGEABLE`, 0 reviews, 0 comments.
what_was_done: **Three commits plus this close-out: `467d3ab6` claim (with the Phase 0 `dashboard_history.jsonl` snapshot), `cd52df79` the trim, `d254adcc` the fold.** `methodology_trim.py --file HANDOFFS.md --cut 4 --write` archived **2 of 6**, no `--force` — **SRF 0.9095** vs `000a843` — L1/L2/L3/P1A OK at write, `CUT_STRADDLES_DAY` because S157 also carries 2026-09-09. **The post-claim re-derive matched the prediction written into the claim entry** (pre-claim: 1 of 5). **THE FOLD WAS BUILT IN SCRATCH AND ASSERTED BEFORE IT TOUCHED THE LEDGER:** the pointer block parsed (exactly one, 448 B); each of the 14 `[proof](…)` cells asserted equal to its own row's shard path plus `.verify.sh` — the rule `HANDOFFS.md:46` states — before the column went (922 B with header and separator); one 125 B row in; counts 14/143 → **15/145**, `n` re-summed. A second script cross-checked every row against the shard it names: 15 rows = 15 files, each `n` = that shard's `handoff` fence count, every proof present. **Then the fold was committed inside a `--no-local` clone and tested there before it was committed here** — the operator's condition. **No learning row:** the lesson (gotcha 1) is in the family of Learnings #24 and #62, and `FRAMEWORK_LEARNINGS.md` has ~4 rows of room before BL-53 must be answered.
next_steps: **(1) PR #80 IS THE MAINTAINER'S — DO NOT MERGE IT.** `gh pr view 80 --repo KJ5HST/methodology --json state,reviews,comments`; replying is outward-facing and needs its own ask. **(2) `CHANGELOG.md` REACHES ITS OWN TRIM TRIGGER NEXT SESSION — an estimate from growth, not a measurement.** **191,936 B after this close-out's entry — 4,672 B under the 196,608 B** Class A threshold (measured); S156–S159 each added **6,283–9,548 B**. Run `python3 starter-kit/methodology_trim.py --file CHANGELOG.md --check` at Phase 0 and again after the claim. **SRF 0.5329** vs `aaa6d30` today — no `SRF_RED`; re-derive, and any `--force` is its own operator ask. A CHANGELOG trim is its own deliverable. **(3) `HANDOFFS.md` HOLDS FOUR** — the next Phase 0 does not trim; the one after does. A fold now costs a 125 B row against 817 B spare, so **no byte negotiation for ~6 folds**. **(4) REPAIR THE TWO STALE PLANNING DOCUMENTS** — `docs/planning/upstream-read-set-pr-plan.md:574` (*"Nothing exists to open a PR from today"*, refuted by #80) and `docs/planning/port-branch-identity-adjudication.md` (0 hits for `read-set-budgets`). Fork-only. **(5) `HOW_TO_USE.md:774` (27 → 28) IS A DISTRIBUTED FILE** (`bin/_manifest.py:63` → `docs/methodology/HOW_TO_USE.md`) — no earlier handoff said so. The fix reaches adopters only through upstream: batch it into the next upstream PR. **(6) BL-36's TABLE IS STALE** (`docs/planning/BACKLOG-DETAIL.md:811`): it lists six shards, and 15 `HANDOFFS` shards now exist. Three of their proofs fail (gotcha 2). Whoever works BL-36 re-runs every proof first. **(7) CARRIED:** Test 31's grep (`bin/tests.sh:1968`, its own ask); BL-53 (~4 rows); the `HANDOFFS.md` density record; `choose_cut` (`starter-kit/methodology_trim.py:1014`); nine merged `origin` branches; pushing `main` (36 ahead of `origin/main` after this close-out). Each deletion and the push is its own go-ahead.
key_files: `HANDOFFS.md:8` (retention paragraph), `:45-48` (archive heading and the one sentence that now carries each proof's path), `:50-66` (the table: four columns, 15 rows), `:68-72` (`NEXT TRIMMING SESSION` comment, figures now ~125 B vs ~448). `docs/archive/HANDOFFS-through-2026-09-09.md.verify.sh` (pins `cd52df7`). `bin/check-links:2-12` (its population: distributed files only). `bin/check-handoff:662-665`. `docs/planning/BACKLOG-DETAIL.md:811` (BL-36). `docs/archive/CHANGELOG-through-2026-09-02.md:590` (`9038e40`'s verdict: no record loss). `docs/planning/file-management-system-plan.md:243` (the `-08-25` proof failure, recorded). `starter-kit/methodology_trim.py:1093`, `:1103`.
gotchas: **(1) `bin/check-links` CANNOT SEE `HANDOFFS.md`.** It validates the 23 distributed files in a simulated adopter tree (`bin/check-links:2-12`), and I named it in the operator's condition without reading that. Its exit 0 is not evidence for a root ledger; resolve the file's links directly (19 relative, 0 unresolved here). **(2) THREE SHARD PROOFS FAIL AND NONE IS YOURS** — `HANDOFFS-through-2026-08-02` and `-08-09` (BL-36), `-08-25` (`9038e40` folded in-commit). Before calling a proof failure new, run it in a control clone of the pre-change commit and `cmp` the output; here all three were byte-identical at `7a6ea4b`. **(3) `grep -h` HIDES THE FILE NAME** — it cost me a wrong citation (a line number put on the wrong file), caught before this receipt. Cite from `grep -n -H`. **(4) RE-DERIVE THE DRY RUN AFTER THE CLAIM.** **(5) `bin/tests.sh` MUTATES BOTH LIVE LEDGERS** — run it in a `git clone --no-local`; to test an uncommitted change, commit it inside the clone. **(6) THE FOLD IS STILL ITS OWN COMMIT** (Learning #58). **(7) READ EXIT CODES BARE.**
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`,** run only in fresh `--no-local` clones. Baseline at the claim `467d3ab6`: **304 passed / 1 failed / 0 skipped, exit 1** (Test 9 `github source dry-run failed`, pre-existing — PR #80's cure). **Post-fold** (committed inside a clone first): **304 / 1 / 0, exit 1 — 305 rows both sides, 0 status flips, 10 rows differing only in numbers this session moved** (receipts 6→4, front matter 7,148→6,351 B, ledger 59,110→37,492 B, A2 99%→88% of reserve, live `**Model:**` bullets 25→26, discovering run 296→297). **All 15 shard proofs on the committed fold: 12 exit 0, 3 exit 1 with output byte-identical to a control clone of `7a6ea4b`.** The new shard's proof exits **0** at `cd52df7` and again after the fold, on this tree. Bare, live tree: `check-learnings` **0**; `methodology_trim.py --check` **0** for both ledgers; `check-links` **0** (not evidence — gotcha 1); `check-handoff` **1** while this receipt was pending. **Close-out re-run, on this content committed inside a clone (this sentence added after it): 304 / 1 / 0, exit 1 — 305 rows, 0 flips vs the post-fold run, 7 rows differing only in this close-out's own numbers** (live `**Model:**` bullets 26→27, the fixture's derived id S160→S161, ledger 37,492→45,132 B, discovering run 297→298); `check-handoff` **0**, 0 records over 12,288 B. **NOT EXERCISED:** any adopter tree (no distributed file changed), CI (none), the pushed path.
changelog_ref: CHANGELOG.md "2026-09-11 · [ad hoc] S160 close-out — `HANDOFFS.md` back to four receipts (59,110 → 37,492 B), its archive table's `proof` column dropped, and `CHANGELOG.md` one session from its own trim trigger", plus the fold entry, the trimmer's own "Ledger trim" entry, and the S160 claim entry
commit: 467d3ab6 (claim) + cd52df79 (the trim) + d254adcc (the fold) + this close-out
```

**Self-assessment: 8/10.** Plus: **the fold was proven lossless before it touched the ledger** — every
dropped `proof` cell asserted equal to its row's derivation, every row cross-checked against the shard
it names — and **tested as a commit in a clone** before it was committed here, as the operator's
condition required. **Ran all fifteen shard proofs**, which no trim session had done (S158: *"NOT
EXERCISED: … the thirteen older shard proofs"*), and **settled the three failures with a control clone
and `cmp`** rather than by reasoning about pinned commits — then searched the record before calling
the third new, and it was not. The prediction written into the claim entry was **measured and
matched**. **Minus:** **I proposed a guard that could not fire.** My Phase 0 option made
`bin/check-links` half of the operator's condition; its summary line says it reads distributed files
only, and I read that line after it exited 0. Caught before it counted as evidence — but the operator
approved a condition I had not checked. **And I told the operator a line number on the wrong file**
(`grep -h`), corrected here and in the close-out report. The option I marked *Recommended* was also
unrun when offered — labelled so, still ahead of its evidence. **Reduction:** `HANDOFFS.md` 56,954 B at
Phase 0 → 37,492 B before this receipt; front matter 7,148 → 6,351 B.

**Predecessor (S159): 8/10.** Its item (2) was the procedure, and every figure in it re-derived to the
byte: 8,521 B the smallest record, 9,796 B the typical, 20 B of front-matter spare, *"trim first,
whatever the task"*. Its suite result reproduced exactly at my baseline (304/1/0), every `key_files`
anchor I checked resolved, and items (3)–(5) and (9) were still true at Phase 0 — nine merged branches,
32 commits ahead. **Not 9, for two misses.** It did not see that **`CHANGELOG.md` was 11,964 B from its
own trim trigger** at its close-out — about 1.5 sessions at the rate its own entries were adding —
which is now the next session's forcing item. And item (5) handed `HOW_TO_USE.md:774` forward as a
one-line fix without noticing the file is distributed. It offered only *"paid in cut text"* for the
fold, though S158's still-retained receipt had already priced the column drop this session used.
**ROI: strongly positive** — item (2) put this session straight into execution.

```handoff
session: S159
date: 2026-09-10
status: complete
self_score: 7
predecessor_score: 8
active_task: **`starter-kit/FRAMEWORK_LEARNINGS.md`'S LIMIT NOW GUARDS GROWTH ONLY — 81,920 B — AND THE TWO OWED LEARNINGS ARE WRITTEN.** Operator decision *"A, reworded as a growth warning"*, taken after all four remedies were run in `--no-local` clones and after the operator asked why the limit was in bytes rather than tokens. The file is **76,007 B = 26,189 tokens**, past one Read by design now rather than by drift: it is on-demand, so `context_budget.py` gives it no token verdict (`starter-kit/context_budget.py:77-83`). `context_budget.py` still exits 2, for the three known rows only (read-set total, `CHANGELOG.md`, `SESSION_RUNNER.md`). **The question no limit answers — how many learnings before old ones retire — is BL-53.** **Fork-internal: nothing pushed, no PR, no comment; PR #80 untouched** (OPEN, `MERGEABLE`, 0 reviews, 0 comments at Phase 0).
what_was_done: **Four commits: `867087b` claim (with the Phase 0 `dashboard_history.jsonl` snapshot), `a51d848` the decision, `cd0ac72` the learnings, and this close-out.** **`a51d848`:** `.context-budget.json:99-112` — `max_bytes` 73,728 → **81,920**, density re-metered (**2.9051 B/token at 73,920 B**, doubled-file method, replacing 2.8897 at 56,673 B), and the note **recomposed, 4,452 → 2,120 B**, to claim only a growth signal; the old text is cited as `git show 867087b:.context-budget.json`. **BL-53** raised with the full S159 cost table. **`cd0ac72`:** rows **#62** (a gate red for a known reason cannot report a new failure, 1,067 B) and **#63** (state headroom in units of the next write, 1,018 B), every figure re-checked first; the file is **byte-identical to the scratch copy that was token-metered**. **THE COSTING, EACH OPTION RUN WITH BOTH ROWS APPENDED:** raise 304/1, 0 flips; tombstone 1–10 304/1 but 2 rows of room; archive 1–10 **295/10** (9 new failures, 7 citations to missing rows in 4 distributed files, a contiguity checker change); archive 1–5 295/10 with 301 B of room; compact estimated from a 3-row trial (−880 B, 20%) — the one option not run in full. **THE FINDING THAT REFRAMED IT:** at 73,920 B the file already measured **25,445 tokens**; 73,728 was a token limit in bytes (S114, 3.03 B/token) that S119's compaction had silently invalidated. **No new learning row from S159:** its lesson is Learning #34 applied, and a near-duplicate would spend one of the four rows of room.
next_steps: **(1) PR #80 IS THE MAINTAINER'S — DO NOT MERGE IT.** Watch with `gh pr view 80 --repo KJ5HST/methodology --json state,reviews,comments`; replying is outward-facing and needs its own ask. **(2) TRIM `HANDOFFS.md` AT PHASE 0 — this close-out leaves FIVE receipts against the policy of four** (`HANDOFFS.md:8`), and after it the file has room under `CEILING_BYTES` for **at most one record the size of the smallest here (8,521 B) and none of the typical (9,796 B)** — so trim first, whatever the task. `methodology_trim.py --file HANDOFFS.md --cut 4`, re-derived after the claim commit; fold the pointer block in its own commit (Learning #58), paid in cut text — the front matter has 20 B spare. **(3) ANCHOR TEST 31'S GREP, OR NEVER PUT THE WORD IN A `CHANGELOG.md` HEADING.** `bin/tests.sh:1968` runs `grep -qi "WARNING"` over all of `bin/model-report`'s output, which echoes every heading; the tool's own line starts `WARNING:` (`bin/model-report:541`). A one-line, canonical-only fix — but a test change, so its own ask. **BL-53's firing will tempt exactly that word.** **(4) REPAIR THE TWO STALE PLANNING DOCUMENTS** — `docs/planning/upstream-read-set-pr-plan.md:574` still says *"Nothing exists to open a PR from today"* (refuted by #80); `docs/planning/port-branch-identity-adjudication.md` has zero hits for `read-set-budgets`. **(5) `HOW_TO_USE.md:774`: 27 → 28** — re-verified at S159's Phase 0. **(6) BL-53 BEFORE THE LIMIT FIRES AGAIN** — ~4 rows, ~10 sessions at 583 B per session. It needs a retirement rule (which rows retire), not another byte negotiation; no option needs re-costing. **(7) IF ADOPTER READABILITY OF THIS FILE MATTERS:** a token limit for on-demand files in the distributed `context_budget.py` — upstream, its own session; offered to the operator, not pursued. **(8) CARRIED FROM S158:** the `HANDOFFS.md` density record (its item 6); `choose_cut`, `starter-kit/methodology_trim.py:1014`. **(9) NINE MERGED `origin` BRANCHES, NOT FIVE** (`git branch -r --merged main`); deleting any, and pushing `main` (32 commits ahead of `origin/main` after this close-out), is each its own go-ahead.
key_files: `.context-budget.json:99` (the entry), `:101` (`max_bytes` 81,920), `:112` (the note). `starter-kit/FRAMEWORK_LEARNINGS.md:94-95` (rows #62, #63). `docs/planning/BACKLOG-DETAIL.md:1527` (BL-53; cost table after it, policy paragraph at `:1558`). `docs/planning/BACKLOG.md:11`, `:148`. `starter-kit/context_budget.py:51-60` (why a readability limit belongs in tokens), `:77-83` and `:377-382` (why on-demand files get no token verdict), `:386` (tokens = bytes ÷ declared density). `bin/check-learnings:86-104` (the 1,500 B row budget — the guard actually paid). `bin/_manifest.py:38` (the file ships to adopters), `:54`, `:60`. `bin/tests.sh:1968`, `bin/model-report:541`.
gotchas: **(1) EVERY "TOKEN" FIGURE IN THIS TOOLING EXCEPT THE READ REFUSAL IS BYTES ÷ A DECLARED DENSITY** (`context_budget.py:386`). To meter a file: `cat F F > x`, Read x with a spanning `limit`, halve the refused count. **(2) STATE A LIMIT'S ENFORCED UNIT AND ITS DERIVATION BEFORE COSTING IT.** I costed in the config's bytes after measuring tokens, and the operator had to ask. **(3) PROSE IN A LEDGER HEADING IS TEST INPUT** — next_steps (3); my decision entry's heading was reworded after commit for exactly that. **(4) ZSH DOES NOT WORD-SPLIT `set -- $v`** — my first variant run applied nothing and printed a clean "control"; call a function with explicit arguments. **(5) RUN `bin/tests.sh` IN A `git clone --no-local`, NOT THE LIVE TREE** — ~210 s each, four in parallel were fine, and the live ledgers are never at risk; better than backing them up. **(6) THE CLAIM ENTRY STILL SAYS `CHANGELOG: pending`** by convention; this close-out's entry closes it. **(7) READ EXIT CODES BARE.**
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`,** run only in fresh `--no-local` clones. Baseline at `867087b`: **304 passed / 1 failed / 0 skipped, exit 1** (Test 9 `github source dry-run failed`, pre-existing — PR #80's cure). **At `cd0ac72` it went 303 / 2 — A REGRESSION THIS SESSION CAUSED, CAUGHT BY RE-RUNNING AFTER THE LAST COMMIT, FIXED BEFORE CLOSE-OUT:** Test 31 (`bin/tests.sh:1968`) greps `bin/model-report`'s whole output case-insensitively, and my decision entry's heading carried the word it looks for. The tool parsed every heading and exited 0; the heading was reworded. **Final, on this close-out's exact content: 304 / 1 / 0, exit 1 — 305 rows, 0 flips, 0 new vs baseline;** the 8 changed rows are numbers this session moved (`**Model:**` bullets 23→24, derived ids `#64`/`S160`, ledger size). Checkers on the live tree, bare: `check-learnings` **0** (62 rows, 0 over 1,500 B), `check-links` **0** (105 links / 23 files), `BACKLOG-DETAIL.md.verify.sh` **0** (18 split items byte-identical), `context_budget.py` **2** before and after — **rows diffed, exactly one status change: `FRAMEWORK_LEARNINGS.md` `over` → `ok` (76,007 / 81,920 B)**. `check-handoff` **0** on the completed receipt, 0 records over 12,288 B. **NOT EXERCISED:** any adopter tree (the rows reach adopters at their next `bin/sync`), CI (none), the pushed path.
changelog_ref: CHANGELOG.md "2026-09-10 · [ad hoc] S159 close-out — `FRAMEWORK_LEARNINGS.md`'s limit now guards growth only (81,920 B), Learnings #62 and #63 written, BL-53 raised", plus the learnings entry, the decision entry, and the S159 claim entry
commit: 867087b (claim) + a51d848 (decision, BL-53) + cd0ac72 (Learnings #62, #63) + this close-out
```

**Self-assessment: 7/10.** Plus: **ran every option's full payload before offering it** — four clones,
four full suites — the only reason the archive options reached the operator priced in broken tests
and dangling citations rather than bytes. **Metered tokens instead of estimating them**, which found the
file already past one Read and reframed the question. **Re-checked each owed learning's figures before
writing it**, fixed a cited destination in the new note before committing it, and tied the token
measurement to the committed file by byte identity. Diffed `context_budget.py`'s rows, not its exit
code — Learning #62 applied to its own gate. And **re-ran the suite after the last commit**, the only
reason the regression below was caught here rather than by S160. **Minus:** **I costed and recommended
in bytes after measuring in tokens.** I had read the tool header that says a readability limit belongs
in tokens, mentioned it once in passing, and still framed option A as a byte raise; the operator had to
ask *why bytes*, and the answer changed the deliverable's wording. That is Learning #34's question,
asked by the stakeholder instead of by me. **My own ledger heading broke the suite** (304/1 → 303/2) —
a trap my notes already describe: grep the tool's row, not its prose. The zsh word-split trap, also in
my notes, cost a run and printed a misleading clean "control". Compaction reached the operator as an
estimate, the one option not run in full. **Reduction:** the budget note shrank 2,332 B; the learnings
file grew 2,087 B inside the limit the operator set.

**Predecessor (S158): 8/10.** Its item (2) was the procedure this session followed: exact figures
(73,920 vs 73,728; 72,692 before S157's row), the BL-45 precedent, and *"cost each option by running it
… the file is DISTRIBUTED"* — which is why the archive options came back priced in broken tests and
citations. The two owed learnings were written out in its CHANGELOG entry, ready to use, and every
figure in them checked out. Gotcha (5), *diff an already-red checker's rows*, was used as written.
**Not 9, for one gap and one inherited error.** It framed the breach entirely in bytes and never noticed
that the limit was a token limit in disguise the file had already outgrown (25,445 tokens), though
`starter-kit/context_budget.py:57` names this very file — and I carried that framing to the operator.
Item (8)'s *"five merged `origin` branches"* is nine. **ROI: strongly positive** — item (2) meant no time
went to deciding how to cost the options, only to running them.

```handoff
session: S158
date: 2026-09-10
status: complete
self_score: 8
predecessor_score: 7
active_task: **`HANDOFFS.md` IS BACK TO FOUR RECEIPTS — 61,122 → 38,425 B through claim, trim and fold, before this receipt landed.** Retained S158, S157, S156, S155; **S154 and S153 are frozen in [`docs/archive/HANDOFFS-through-2026-09-08.md`](docs/archive/HANDOFFS-through-2026-09-08.md)** with its `.verify.sh`, **exit 0, pinned to the trim commit `000a843e`, re-run after the fold and still 0**. Front matter **7,148 of the 7,168 B reserve**. **ONE FILE OVER, A BREACH NO SESSION SAW: `starter-kit/FRAMEWORK_LEARNINGS.md` is 73,920 B against its declared 73,728 B (`.context-budget.json:101`) — 192 B over since S157's close-out.** Found and measured, not fixed. **Fork-internal: nothing pushed, no PR, no comment.** PR #80 at Phase 0: OPEN, `MERGEABLE`, 0 reviews, 0 comments; `origin/main` unmoved at `f8531cf`.
what_was_done: **Three commits plus this close-out: `e5812e2a` claim (carrying the Phase 0 `dashboard_history.jsonl` snapshot), `000a843e` the trim, `e2600a06` the fold.** `methodology_trim.py --file HANDOFFS.md --cut 4 --write` archived **2 of 6 records with no `--force` and no gate — SRF 0.7414 vs `c581ac4`** — L1/L2/L3/P1A OK at write. **THE POST-CLAIM RE-DERIVE CHANGED THE ANSWER FOR THE THIRD TRIM RUNNING:** pre-claim it took 1 of 5 and warned `CUT_STRADDLES_DAY`; post-claim 2 of 6, both 2026-09-08, and the straddle was gone. **THE FOLD WAS PAID FOR, NOT SQUEEZED:** 448 B of pointer block out, a 190 B row in, table 13/141 → 14/143 with the `n` sum asserted, and **201 B of spent clauses cut** because the reserve had 9 B spare — front matter 7,607 → 7,148 B. **A second instrument checked conservation:** `bin/model-report`'s section headers match before and after except the new shard's own line (0 matched lines). **TWO LEARNINGS ARE OWED AND DELIBERATELY NOT WRITTEN** — `FRAMEWORK_LEARNINGS.md` is already over its ceiling, and a ~1.2 KB row would deepen the breach FM #28 calls a defect. Their text is in this session's CHANGELOG close-out entry.
next_steps: **(1) PR #80 IS THE MAINTAINER'S — DO NOT MERGE IT.** Watch with `gh pr view 80 --repo KJ5HST/methodology --json state,reviews,comments`; replying to a review is outward-facing and needs its own ask. **(2) PUT `FRAMEWORK_LEARNINGS.md`'s CEILING BREACH TO THE OPERATOR — it gates Phase 3C for every session.** 73,920 B vs 73,728 B; S157's row 61 took it from 72,692 B. BL-45 is the precedent: at S114 the operator chose *raise* from four costed options. Cost each option by running it (raise, archive older rows to a shard, compact) before offering it — the file is DISTRIBUTED, so its shape matters to adopters. Then write the two owed learnings from this session's CHANGELOG close-out entry. **(3) REPAIR THE TWO STALE PLANNING DOCUMENTS** — `docs/planning/upstream-read-set-pr-plan.md:1` and `:555` (§11.3; its item 5 says *"Nothing exists to open a PR from today"*, refuted by #80), plus `docs/planning/port-branch-identity-adjudication.md`. Both unchanged since `16fbba0`. Fork-side. **(4) `HOW_TO_USE.md:774`: 27 → 28** — re-verified today against the runner's 28 FM rows. **(5) THE FOLD'S COST RECURS:** each trim adds a ~190 B row against a reserve now 20 B from full. The table's `proof` column is derivable (`HANDOFFS.md:46` says a proof is the shard path plus `.verify.sh`) and costs **910 B over 14 rows, 65 B each** — measured. Dropping it or collapsing old rows is the operator's call; S155 kept the reserve at 7,168 B. **(6) THE DENSITY RECORD** — `context_budget.py` warns `HANDOFFS.md` 2.3648 B/token at 79% drift; S156 costed three options. **(7) `choose_cut`**, `starter-kit/methodology_trim.py:1014` — distributed, upstream. **(8) DELETE THE FIVE MERGED `origin` BRANCHES; PUSH `main`** — each its own go-ahead. **Retention:** four receipts after this close-out, so the next Phase 0 should find 4 and not trim; the session after should find 5.
key_files: `HANDOFFS.md:8` (retention paragraph), `:45` (archive table; row 14 at `:65`), `:67-71` (`NEXT TRIMMING SESSION` comment). `docs/archive/HANDOFFS-through-2026-09-08.md.verify.sh` (run it; pins to `000a843e`). `.context-budget.json:99-101` (`FRAMEWORK_LEARNINGS.md`, `max_bytes` 73,728). `starter-kit/methodology_trim.py:1014` (`choose_cut`), `:1093` (`build_pointer_block`), `:1103` (`insert_pointer`). `bin/check-handoff:662` (`CEILING_BYTES`), `:663` (`HEADER_RESERVE_BYTES`), `:665` (`RECORD_BUDGET_BYTES`, 12,288). `docs/planning/upstream-read-set-pr-plan.md:555`. `HOW_TO_USE.md:774`.
gotchas: **(1) RE-DERIVE THE DRY RUN AFTER THE CLAIM COMMIT** — it changed the answer at S154, S156 and here. **(2) A FOLD'S ROW IS PAID IN CUT TEXT, AND 20 B IS ALL THAT IS LEFT** — the next fold needs ~190 B, and this fold already took the obvious spent clauses. **(3) BLOCKQUOTED PROSE CARRIES `> ` ON EVERY WRAPPED LINE.** My cut string lacked it, matched nothing, and my byte calculator still summed its 95 B into the total. Assert each match count is exactly 1 before summing or writing. **(4) THE FOLD MOVES FRONT-MATTER LINE NUMBERS** — the stub's `:48`/`:69-73` went stale; re-grep before citing. **(5) AN ALREADY-RED CHECKER CANNOT SHOW A NEW BREACH.** `context_budget.py` exits 2 for pre-existing reasons, so a new `over` row changes nothing a session watches, and `bin/check-learnings` budgets rows (1,500 B), never the file. Diff its rows against the last run. **(6) `bin/tests.sh` MUTATES BOTH LIVE LEDGERS** — back up outside the repo; `shasum -c` from the repo root. **(7) zsh: `${PIPESTATUS[0]}` IS EMPTY AND `$c:path` IS A HISTORY MODIFIER** — both cost a call here. Read exit codes bare; brace a variable before a colon.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`.** Baseline after the claim (before the trim) and again after the fold, both bare: **304 passed / 1 failed / 0 skipped, exit 1** — **305 rows both sides, 0 status flips, 10 changed rows, each a number this session moved** (receipts 6→4, front matter 7,159→7,148 B, ledger 61,122→38,425 B, live `**Model:**` bullets 17→18, the discovering run 288→289). The failure is Test 9 `github source dry-run failed`, pre-existing — PR #80's cure. **The deliverable's own proof** exits **0** after the trim commit and again after the fold. Bare: `methodology_trim.py --check` **0** (38,425 of 196,608 B), `check-links` **0**, `check-learnings` **0** (60 rows numbered to 61; #14 is skipped), `check-handoff` **1** while this receipt was pending, `context_budget.py` **2** (`FRAMEWORK_LEARNINGS.md` over — NEW since S157; `CHANGELOG.md`, `SESSION_RUNNER.md` and the read-set total over — pre-existing). **Close-out re-run with this receipt complete, bare:** 304 / 1 / 0, exit 1; 305 rows, **0 flips** vs the post-fold run, its 7 changed rows all this close-out's own numbers (live `**Model:**` bullets 18→19, the fixture's derived id S158→S159, the ledger's size, the discovering run 289→290); `check-handoff` **0**, 0 records over 12,288 B. With this receipt the file has room for the next session's receipt (records here run 8,521–12,286 B), and the count policy trims at the session after that. **NOT EXERCISED:** any adopter tree, CI (none exists), the pushed path, the thirteen older shard proofs.
changelog_ref: CHANGELOG.md "2026-09-10 · [ad hoc] S158 close-out — `HANDOFFS.md` back to four receipts (61,122 → 38,425 B), and `FRAMEWORK_LEARNINGS.md` found 192 B over its ceiling", plus the fold entry, the trimmer's own "Ledger trim" entry, and the S158 claim entry
commit: e5812e2a (claim) + 000a843e (the trim) + e2600a06 (the fold) + this close-out
```

**Self-assessment: 8/10.** Plus: **re-derived the dry run after the claim**, and it changed the answer
from 1 record to 2. **Took a baseline test run before the trim**, which is what made a clean
row-for-row diff possible — 0 flips, all 10 changes explained. **The fold script asserted before it
wrote**: each replacement unique, the `n` column summing to 143, the front matter inside the reserve.
**Corrected my own Phase 0 understatement** in the claim entry rather than letting it stand. And I
**followed a small discrepancy** — 61 learnings, 60 rows — far enough to find a real breach, measured
it with the checker that sees it, and declined to deepen it. **Minus:** my Phase 0 report priced a
receipt in the wrong unit (6,694 B of close-out growth, not the 8,521 B record) — the same kind of
error I score S157 down for below. My byte calculator summed a zero-match cut into its total; the
per-cut count exposed it, but the total line was wrong. Two zsh traps I already had notes for each
cost a call. And my own fold invalidated the anchors my stub had cited.

**Predecessor (S157): 7/10.** Its item (5) was exactly the procedure — `--cut 4`, tool not hand, fold
in its own commit, and *"none should be assumed"* about `--force`, which was right: SRF 0.7414 needed
none. Gotchas (5) and (6) were used as written, every PR #80 fact re-verified exactly, and
`HOW_TO_USE.md:774` was still wrong as claimed. **Not 8, for two misses, both about sizes it wrote
itself.** *"52,493 B at claim, so bytes are not pressing"* — its own close-out took the file to
59,187 B, leaving 6,349 B, smaller than any record in it (8,521–12,286 B), so the next session could
not close out without a trim whatever it chose. That is the class of error its own Learning #61 names.
And its row 61 took `FRAMEWORK_LEARNINGS.md` 192 B past its ceiling while its receipt reported
`check-learnings` **0**, without noting that that checker never measures the file. **ROI: positive** —
item (5) took this session straight to execution, and the one claim it got wrong cost a single
measurement to correct.

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

