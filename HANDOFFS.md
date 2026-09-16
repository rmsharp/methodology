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

**Archived shards — 20 trims, 154 receipts.** Every shard is `docs/archive/HANDOFFS-through-<date>.md`
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
| 2 | 2026-09-14 → 2026-09-15 | [`HANDOFFS-through-2026-09-15.md`](docs/archive/HANDOFFS-through-2026-09-15.md) | v1.5.0 |
| 2 | 2026-09-15 → 2026-09-15 | [`HANDOFFS-through-2026-09-15-2.md`](docs/archive/HANDOFFS-through-2026-09-15-2.md) | v1.5.0 |

<!-- NEXT TRIMMING SESSION: methodology_trim.py appends a 3-line pointer block here
     (starter-kit/methodology_trim.py:1093 build_pointer_block, :1103 insert_pointer). Fold it into
     the table above as one row (~125 B vs the block's ~448) and delete the block, IN ITS OWN
     COMMIT: inside the trim commit the shipped .verify.sh fails L2 (Learning #58). The generator
     is DISTRIBUTED, so teaching it this is an upstream change. -->

```handoff
session: S172
date: 2026-09-16
status: pending
self_score: pending
predecessor_score: pending
active_task: **BL-57's P3 -- SOURCE TAGS AND THE AUDIT (C6, C10) -- ON BRANCH `bl57/changelog-rules`** (`docs/planning/changelog-rules-contradictions-plan.md:490`; worktree `../methodology-bl57` at `775ba238`). `[BL-<N>]` becomes `[BL-<id>]` and the audit becomes the shard-reading form, in `FRAMEWORK_APPARATUS.md` the Action Ledger section, `starter-kit/SESSION_RUNNER.md` (`:39`, `:278`, `:329`), `ITERATIVE_METHODOLOGY.md:294` and `.githooks/pre-commit:57`. **Upstream PR #82 is still OPEN at `c84e7d96`, re-checked at Phase 0, so S169's merge-first amendment does NOT trigger** -- P3 starts on the branch as it stands. **Two carried items ride with P3:** P2's finding that the `HANDOFFS.md` seed still publishes a bare glob zsh refuses where no shard exists (C10's class, assigned to P3), and S169's amendment that P3's runner criterion (`:508`) and P4's (`:538`) are written in BYTES and must be restated in TOKENS -- that measurement is not yet taken, so it comes first.
what_was_done: pending
next_steps: pending
key_files: `docs/planning/changelog-rules-contradictions-plan.md:490` (P3), `:508` (the byte criterion to restate), `:514` (P4), `:538` (its byte criterion), `:191` (the target state), `:755` (the conformance commands), `:345` (the adopter figures); on the branch: `FRAMEWORK_APPARATUS.md` the Action Ledger section, `starter-kit/SESSION_RUNNER.md:39`, `:278`, `:329`, `ITERATIVE_METHODOLOGY.md:294`, `.githooks/pre-commit:57`, `starter-kit/HANDOFFS.md` (the bare glob).
gotchas: The token instrument is the Read tool's refusal -- double the file, Read it with a spanning `limit`, halve the count, and reproduce a recorded figure BEFORE using a new one. A byte pin is not a token pin: S169 measured a change that was -15 B and +62 tokens. zsh: brace `${r}:path`; an unmatched glob aborts the command so a count reads 0; write scripts to a file rather than chaining heredocs. The branch carries upstream's `.githooks/commit-msg`, which refuses a commit with no `Co-Authored-By` trailer. `grep -c` exits 1 on ZERO matches.
runtime_smoke: Phase 0 at `716506c`: both ledger frontiers reconciled (`CHANGELOG.md` frontier == HEAD, 0 undocumented commits; `HANDOFFS.md` frontier `1232dc6` with `716506c` after it, already in the ledger at `CHANGELOG.md:217`), no ghost session, newest receipt `status: complete`. Dashboard 76/100, risk medium (back from S171's mid-trim high), 947 commits, 0 vulns. `context_budget.py --status` exits 2 -- runner ~19,415 tokens against an 18,222-token ceiling, read-set total 69,749 B against 56,750 B, pre-existing and by design; captured as this session's baseline for diffing. Upstream PR #82 OPEN, head unmoved at `c84e7d96`, zero open upstream issues; the S170 comment `5691623656` re-fetched, unedited, and still sha256-identical (`62821afb...`) to `docs/planning/pr82-comment.md`. Suites not re-run at Phase 0.
changelog_ref: CHANGELOG.md "2026-09-16 - [BL-57] S172 claim -- BL-57's P3: source tags and the audit, on the branch"
commit: pending
```

```handoff
session: S171
date: 2026-09-16
status: complete
self_score: 7
predecessor_score: 9
active_task: **`CHANGELOG.md` TRIMMED BACK UNDER THE 262,144 B HARD READ REFUSAL UNDER OPERATOR-APPROVED `--force` — 276,657 B → 98,495 B, 65 records to `docs/archive/CHANGELOG-through-2026-09-14.md`, L1/L2/L3 re-derived by the shipped proof both before and after the commit (exit 0 each time). AND BL-58 RAISED** — should adopters be told how to trim a ledger losslessly? The operator asked for the benefit and the cost first; both were measured rather than recalled, and the trim followed his go-ahead.
what_was_done: **Fork `main`, 5 commits:** `ff29a8d` claim; `c01854f` the `chore(history)` for the two append-only `.jsonl` series; `f2840fc` the reconcile that unblocked the trim; `101fa78` the trim; `1c4e941` BL-58. **The accounting the operator asked for, every figure re-derived here:** SRF 1.0306 reproduced independently (176,464 B regrown ÷ 171,230 B relieved); the previous trim's net measured at **+17,928 B, 1.102×**; the proof script shown to be a **fixed** 15,992 B cost — 9% of a large shard, 47% of a small one, so small trims are the expensive ones; `docs/archive/` measured at 40.6% of the tracked repo, inside no ceiling. **The refusal was confirmed empirically at both ends, never from the constant:** before, a default `Read` returned `File content (268.4KB) exceeds maximum allowed size (256KB)` — zero content; after, it returns the front matter plus the newest ~51% with an announced `PARTIAL view` banner (lines 1–606 of 1,184). **The trim's own net was predicted then measured: +17,928 B projected, +18,138 B actual (1.102×)** — a transfer, not a saving, and recorded as one. The file's own rate rule went **−67 → +33 entries of headroom**, clearing its published "back above 30" stop. **One blocker was self-inflicted and is the session's real lesson:** the `chore(history)` commit was made `--no-verify` BEFORE the trim, which tripped `P1_UNDOCUMENTED` — the guard is right, since a trim advances the ledger frontier and would hide that commit permanently, and the usual discharge (naming it at close-out) comes too late. S152's precedent, which I had just read, puts that commit AFTER the trim.
next_steps: **(1) BL-57'S P3 — ITS OWN SESSION, AND IT IS NOW THE RANKED DELIVERABLE** (`docs/planning/changelog-rules-contradictions-plan.md:490`, source tags and the audit, C6/C10). #82 is still OPEN at `c84e7d96`, so the merge-first amendment does NOT trigger; P3 starts on the branch as it stands. **S169's other amendment does apply: P3's runner criterion (`:508`) and P4's (`:538`) are written in bytes and must be restated in tokens — that measurement is not done, so P3 begins with it.** Worktree `../methodology-bl57`, branch `bl57/changelog-rules` at `775ba238`. **(2) `HANDOFFS.md` NOW HOLDS SIX RECEIPTS AGAINST A RETENTION POLICY OF FOUR, AND I DID NOT TRIM IT — deliberately, with a number.** Its byte trigger does not fire (54,177 B of 196,608), so a retention trim relieves ~18 KB and writes a fixed ~16 KB proof: **roughly 1.9× net-additive, the expensive end of the curve this session measured.** That is a decision, not housekeeping — put it to the operator at Phase 0 rather than running it on sight. **(3) NO REPLY ON #82 YET** — checked at Phase 0 (`gh api repos/KJ5HST/methodology/issues/82/comments`): one comment, ours, `5691623656`, re-fetched and still sha256-identical to `docs/planning/pr82-comment.md`, `updated_at` == `created_at` so unedited. A reply is its own operator go-ahead. **(4) BL-58 IS A DECISION FIRST, NOT AN EDIT** — three shapes costed roughly, none chosen; any distributed fix is an upstream change and its own go-ahead. **CARRIED, EACH ITS OWN GO-AHEAD:** pushing fork `main` (**13 commits ahead of `origin/main`**); F5/F6 (`docs/planning/pr80-review-response.md:243`); the fork resync; BL-53; BL-54; BL-36; `choose_cut`.
key_files: `CHANGELOG.md:1` (front matter, readable again); `:105` (the rate rule, now +33); `docs/archive/CHANGELOG-through-2026-09-14.md` and its `.verify.sh` (the shard and its proof); `docs/planning/BACKLOG-DETAIL.md:1788` (BL-58, eight hazards), `docs/planning/BACKLOG.md:153` (its index row); `starter-kit/methodology_trim.py:130` (`READ_REFUSE_BYTES`), `:165` (`CLASS_A_STOP_BYTES`), `:203` (`SRF_RED`); `docs/planning/srf-red-refusal-adjudication.md:176` (the self-limitation that warrants the force), `:459` (S132's precedent), `:106` (the net-additive accounting, S124's and covering only the first ten trims).
gotchas: **(1) SEQUENCE A HOUSEKEEPING COMMIT AFTER AN ACTION THAT ADVANCES THE LEDGER FRONTIER, NEVER BEFORE IT** — see `what_was_done`; this cost an extra commit and 773 B of permanent ledger, and the precedent was on screen when I got it wrong. **(2) `grep -c` EXITS 1 WHEN IT MATCHES NOTHING** — the Phase 3E suite run was reported as *failed, exit 1* while `bin/tests.sh` itself exited **0**; the 1 was the trailing `grep -c '  SKIP:'` finding zero skips. Read the chain's own echoed exit code before believing the task status. **(3) `--force` READS AS DESTRUCTIVE TO THE HARNESS CLASSIFIER** and was refused once at Phase 0 **on a dry run**, which writes nothing; it is the operator's approval that authorizes it. **(4) THE TRIMMER STAGES AND COMMITS NOTHING** — `git add` the live file AND the shard AND the proof, or the proof certifies a file no one has. **(5) `CHANGELOG.md` IS NOT IN THE READ-SET BUDGET,** so the trim moved `context_budget.py --status` not at all: still 69,749 B, still `over`, still exit 2. The benefit was the Read refusal alone — do not credit the trim with a budget it never touched. **(6) THE ARCHIVE TIER IS NOW 42.8% OF THE TRACKED REPO** and has no ceiling anywhere.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`,** run in a `--no-local` clone whose HEAD sha was asserted equal to the working repo's (`1c4e941` both sides) before anything was measured. **`bin/tests.sh` exit 0 — `== Summary: 305 passed, 0 failed, 0 skipped ==`, identical to S168's, S169's and S170's controls.** Unit suites in the same clone: dashboard **321 OK** (4 skipped), trimmer **123 OK**, budget **116 OK** (2 skipped). `check-links` 0 (105 links, 23 files), `check-learnings` 0 (65 rows), `check-handoff --all --allow-pending` 0 (6 receipts) — all read bare. `context_budget.py --status` exits 2, **unchanged and unrelated to the trim**: diffed against the Phase 0 reading, 0 status flips and exactly two rows moved, both by this session's own writes (`HANDOFFS.md` +2,312 B, `BACKLOG.md` +379 B). The shard's `.verify.sh` exit 0 twice — pre-commit (*"HEAD vs the working tree"*) and post-commit (naming `101fa78`). **NOT EXERCISED:** any reply from the maintainer; the `HANDOFFS.md` retention trim; BL-58's remedy; the fork `main` push; CI (there is none).
changelog_ref: CHANGELOG.md "2026-09-16 · [ad hoc] S171 close-out", plus the claim, the reconcile, the tool's own trim entry and the BL-58 entry
commit: ff29a8d (claim) + c01854f (history) + f2840fc (reconcile) + 101fa78 (trim) + 1c4e941 (BL-58) + this close-out
```

**Self-assessment: 7/10.** Plus: the operator asked what a trim buys and costs, and every figure in the
answer was derived here — SRF reproduced to the fourth decimal, the previous trim's net measured at
+17,928 B, the proof script shown to be a fixed cost that makes *small* trims the expensive ones, the
archive tier's unbounded share measured. The refusal was confirmed by running into it, not by reading a
constant, at both ends. **I predicted this trim's net before running it and then measured it: +17,928 B
projected, +18,138 B actual** — the kind of check this repository keeps finding nobody ran. I caught a
stale figure before publishing it (the *"net +144,239 B"* accounting is S124's and covers only the first
ten trims), and I attributed a background task's *exit 1* to a trailing `grep -c` rather than recording a
failed suite. **Minus, and it is the session's real story: I created the only blocker I hit.** Committing
the `chore(history)` before the trim tripped `P1_UNDOCUMENTED`; the fix cost an extra commit and 773 B of
permanent ledger in a session whose entire subject was that this file grows too fast. S152's commit
sequence — history *after* the trim — was on my screen minutes earlier, and *sequence commits around the
hook that runs* is a lesson already in my own memory. Also: I left `HANDOFFS.md` at six receipts against a
policy of four. That deferral is costed and argued in the receipt rather than silent, but it hands the
same decision to the next session. **Reduction:** the deliverable is a 178,162 B reduction in the file
that had stopped being readable — and a **+18,138 B addition to the repository**, which is what a trim
actually is and is recorded as such in the ledger entry, not as a saving.

**Predecessor (S170): 9/10.** Item (1) was exact and was the first thing this session did: the command,
the comment id, the requirement to re-verify rather than assume, and the note that a reply is its own
go-ahead. **Five of its checkable claims were tested and five reproduced** — #82's state and head sha, the
posted comment's sha256, `CHANGELOG.md` at 274,805 B, `HANDOFFS.md` at five receipts,
`FRAMEWORK_LEARNINGS.md` at 79,483 B. Item (3) stated the read refusal as a fact rather than a projection
and told the next session what to do about it, which is exactly what Phase 0 needed. Its gotcha (3), *an
exit code read through a pipe is the pipe's*, has a sibling that fired here and I recognised it because
that gotcha was in hand. **Not 10:** item (2) carries S169's amendment that P3's and P4's runner criteria
are in bytes and must be restated in tokens, but not the token figures themselves — so the phase it ranks
first still opens with a measurement its two predecessors both had the instrument to take. **ROI: strongly
positive.**



```handoff
session: S170
date: 2026-09-15
status: complete
self_score: 7
predecessor_score: 9
active_task: **ONE COMMENT POSTED TO UPSTREAM PR #82 (THE QUALITY RATCHET, HEAD `c84e7d96`) WITH TEN SUGGESTED CHANGES, RANKED — `5691623656`, READ BACK BYTE FOR BYTE.** Drafted to `docs/planning/pr82-comment.md`, presented in full at the Present gate, revised through three rounds of operator critique, posted on the explicit go-ahead, then re-fetched and compared: **sha256 identical on both sides.** It uses generally recognized terminology throughout — the operator's bar, and itself the comment's lead suggestion.
what_was_done: **Fork `main`, 7 commits:** `840c5fb` claim; `24f11b3` the draft; `657b3b8` recomposed for a reader who has not read the plan; `b4bfa70` the ratchet's actual mechanism; `f64d219` a false contrast dropped; `9833c93` the remedies made precise; `40cf1a4` the implicit links stated; plus this close-out. **Nothing was relayed from S169's review — every claim re-verified first:** #82 unmoved at `c84e7d96`; `pr82-review-repro.sh` re-run end to end, all seven sections matching; all six token figures re-measured with both controls (48,555 and 36,955) reproducing exactly; `--run` re-run in a **sha-verified** `--no-local` clone giving **9/9 pass, results `74c773523dab`** — the receipt's own hash, firsthand — with `bin/tests.sh` `== Summary: 134 passed, 1 failed ==` read directly. **One would-be finding killed before it reached the draft:** an archive-and-`git init` tree measured 131 passed, an artifact of the reproduction method, not a defect. **Three operator critiques, each recomposed rather than patched, and each followed by an audit of siblings for the same fault** — which found three more, two of them errors of fact.
next_steps: **(1) CHECK FOR A REPLY ON #82 BEFORE ANYTHING ELSE** — `gh pr view 82 --repo KJ5HST/methodology --json headRefOid,state,comments,reviews`. The comment is `5691623656`; the maintainer may answer, and a reply is its own operator go-ahead. If #82's head has moved, re-run `bash docs/planning/pr82-review-repro.sh` before relying on any finding in it — every one is pinned to `c84e7d96`. **(2) BL-57'S P3 — ITS OWN SESSION** (`docs/planning/changelog-rules-contradictions-plan.md:490`), unchanged by this session and still carrying S169's two amendments: if #82 has merged, P3 starts by merging `upstream/main` into the branch (a same-line conflict at `ITERATIVE_METHODOLOGY.md:294`; `CLAUDE.md` already conflicts), and P3's runner criterion (`:508`) and P4's (`:538`) are in bytes — restate them in tokens. Worktree `../methodology-bl57`, branch `bl57/changelog-rules` at `775ba238`. **(3) `CHANGELOG.md` HAS CROSSED THE READ REFUSAL — THIS IS NOW A FACT, NOT AN ESTIMATE:** 274,805 B against the 262,144 B cap, so Phase 0 must read it with `offset`/`limit`. Not trimming it is the operator's decision — raise it at Phase 0. **(4) `HANDOFFS.md` HOLDS FIVE RECEIPTS** after this close-out: S171's Phase 0 finds five and trims to four. **(5) `FRAMEWORK_LEARNINGS.md` IS 79,483 OF 81,920 B** after Learning #66 — about two rows left; BL-53's retirement policy is still open. **CARRIED, EACH ITS OWN GO-AHEAD:** pushing fork `main` (**7 commits ahead of `origin/main`** before this close-out); F5/F6 (`docs/planning/pr80-review-response.md:243`); the fork resync; BL-54; BL-36; BL-53; `choose_cut`.
key_files: `docs/planning/pr82-comment.md:1` (the posted text, byte-identical to the comment); `:27` (§2, the three ratchet gaps), `:58` (the three-place remedy), `:92` (§3, the budgets); `docs/planning/pr82-review.md:377` (§6, the asks it was built from); `docs/planning/pr82-review-repro.sh:1`; `starter-kit/FRAMEWORK_LEARNINGS.md` row 66 (last line); on #82 at `c84e7d96`: `starter-kit/quality_ratchet.py:61` (`find_root`), `:134` (`compare`), `:176` (`precommit`), `:325` (the hook template), `:333` (`install_hook`); `starter-kit/methodology_dashboard.py:1931` (`_gate_map`), `:1938` (`_gate_loosenings`), `:2015` (the pairing loop); `.githooks/pre-commit:35`.
gotchas: **(1) A VAGUE REMEDY IS USUALLY A WRONG DIAGNOSIS, NOT A WORDING PROBLEM** — Learning #66, earned three times this session; two of the three were errors of fact, and one introduced an error into a source that had it right. **(2) `check-learnings` PRINTS A RANGE IT HAS NOT MEASURED** — it reported *"contiguous 1..65"* after row #66 landed, because it prints `len(rows)` for both numbers and `#14` is reserved. The row IS registered; run `parse_table` directly rather than believing the summary. **That is BL-44, not a new finding.** **(3) AN EXIT CODE READ THROUGH A PIPE IS THE PIPE'S** — `./bin/check-learnings | tail -3; echo $?` reported `tail`'s 0; re-run bare before believing it. **(4) THE GITHUB API'S `.body | length` IS CHARACTERS, NOT BYTES** — 25,611 characters against 25,743 bytes here; compare by sha256, not by `wc -c`, and strip the newline `jq` appends. **(5) AN ARCHIVE-AND-`git init` TREE IS NOT A CLONE** — it measured 131 passed where a real clone measures 134; assert the HEAD sha before trusting any run. **(6) #82 IS LIVE** — re-fetch and re-pin before relaying any finding.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`,** run in a `--no-local` clone whose HEAD sha was asserted equal to the working repo's, exit codes read bare. **At `40cf1a4`:** `bin/tests.sh` **305 passed / 0 failed / 0 skipped**, matching S169's control at `4c07b91`; dashboard unit **321 OK**, budget **116 OK** (2 skipped, honestly), trimmer **123 OK**; `check-links` 0, `check-learnings` 0 (65 rows, all citations resolve, 0 rows over 1,500 B), `check-handoff --all --allow-pending` 0; `context_budget.py --status` **exits 2** — fork `main` over its declared 41,364 B runner ceiling, pre-existing and by design. **The outward action was verified, not assumed:** the posted comment was re-fetched and is sha256-identical to the local file. **NOT EXERCISED:** any reply from the maintainer; the suggestions applied to #82; CI (there is none); a second reader of the comment's findings; the fork `main` push.
changelog_ref: CHANGELOG.md "2026-09-15 · [ad hoc] S170 close-out" and "2026-09-15 · [ad hoc] S170 — the comment POSTED to upstream PR #82", plus the claim, draft and four revision entries
commit: 840c5fb (claim) + 24f11b3 (draft) + 657b3b8 + b4bfa70 + f64d219 + 9833c93 + 40cf1a4 (revisions) + this close-out; the post itself left no commit (comment 5691623656)
```

**Self-assessment: 7/10.** Plus: nothing was relayed. Every figure in S169's review was re-derived before
it reached the draft, the gate run was reproduced firsthand in a clone whose HEAD sha was asserted first,
and one would-be finding — 131 passed rather than 134 — was killed as an artifact of my own reproduction
method before anyone saw it. The outward action was verified rather than assumed: the posted comment was
re-fetched and matched by sha256, and I caught that the API's `len` counts characters, not bytes. I caught
my own exit code read through a pipe, and searched the backlog before calling the `check-learnings` range a
finding — it was BL-44. **Minus, and it is the session's real story: the operator found three defects in
the draft that I should have found.** Twice they were errors of fact, not of clarity. *"Run the hook
whenever the manifest is tracked in HEAD"* described a guard that does not exist; the lockout bullet blamed
`precommit()` for an exit the tool takes in `main()`, before `precommit()` is reached — and S169's review
had that right, so I introduced an error into a correct source. Worse in kind: *"put the standard in a file
instead of in a judgment"* was my own phrase, substituted for the maintainer's correct framing, and it was
a false contrast in a repository built out of judgments stored in files. Each time the fix was a
recomposition and an audit of siblings, and each audit found more — which is itself the evidence that I was
not applying the standard the operator had to impose three times. Also: two ledger entries stated word
counts I had predicted rather than measured, both corrected before commit. **Reduction:** none — this
session added to three grow-only files and removed nothing. **Learning #66** records the transferable part.

**Predecessor (S169): 9/10.** Item (1) was exact and was used as written, start to finish: the deliverable,
the command to check #82's state, the script to re-run, the file precedent for drafting, the posting
recipe, and the read-back requirement. It carried the operator's terminology bar verbatim, which was the
constraint the whole session turned on. Every one of its seven demonstrations reproduced, all six token
figures reproduced including both controls, and its warning that #82 is live was the right first move.
Gotchas (3) and (4) both applied. **Not 10:** its runner-density finding was framed as a measurement taken
against the wrong file, which reads as an error by whoever measured it. Tracing the branch showed the
density was measured correctly and went stale two commits later — a materially fairer account, and the one
thing I needed that the handoff had not already derived. **ROI: strongly positive** — it turned a
translation task into a verification task, which is the cheaper of the two.

```handoff
session: S169
date: 2026-09-15
status: complete
self_score: 8
predecessor_score: 9
active_task: **A FORK-ONLY REVIEW OF UPSTREAM PR #82 (THE QUALITY RATCHET, HEAD `c84e7d96`) IS DONE — `docs/planning/pr82-review.md` AND ITS REPRO SCRIPT, RECORD `4ffcb253`; NOTHING POSTED UPSTREAM.** The operator's question, answered with measurements: two budgets rest on bytes where measured tokens are the better measure — `CLAUDE.md`'s 59,168 B arrival-size pin passed a **+62-token** change as −15 B, and the runner's token ceiling uses a density measured before #82 edited the file (18,897.5 of 18,900 tokens measured: 2.5 of room, not the 22 the tool reports); `context_budget.py --status` is outside the ratchet. Seven defects demonstrated (§3). BL-57's P3 waits, and #82 moves its ground (§5).
what_was_done: **Fork `main`:** `f89c0faf` claim (with the Phase 0 `dashboard_history.jsonl` snapshot); `0ccfce84` the `HANDOFFS.md` retention trim, 54,851 → 35,001 B, S165 + S164 to `docs/archive/HANDOFFS-through-2026-09-15-2.md`, no `--force` (SRF 0.8644); `da8af503` the fold (20 trims, 154 receipts); `4ffcb253` the record — the review (§2 budgets, §3 seven defects, §4 design challenges, §5 what #82 means here, §6 the asks ranked) and `docs/planning/pr82-review-repro.sh`; this close-out. **Method:** #82's suites re-run in a `--no-local` clone at `c84e7d96` (134 passed / 1 failed, Test 9 by construction; `--selftest` 17 OK; `--run` 9/9 with the S20 receipt's own results hash `74c773523dab`; no tracked file changed); tokens by the doubled-file Read, the instrument first reproducing three recorded figures exactly (48,555; 49,683; 36,955); each defect run in a throwaway repository; the saved script re-run end to end, every row as recorded; every cited anchor re-checked on its tree.
next_steps: **(1) THE OPERATOR'S DECISION, MADE AFTER THIS CLOSE-OUT: THE NEXT SESSION DEVELOPS AND POSTS A COMMENT ON #82 WITH SUGGESTED CHANGES TO IMPROVE THE PR** (the operator's words: *"for the next session, plan on developing and posting a comment for PR #82 with suggested changes to improve the PR."*). Work from `docs/planning/pr82-review.md:377` (§6, the asks ranked) and §§2–4. First `gh pr view 82 --repo KJ5HST/methodology --json headRefOid,state,comments,reviews`; then re-run `bash docs/planning/pr82-review-repro.sh` against the head of the day (and §8's token Reads if the runner or `CLAUDE.md` moved), and drop or amend any finding that moved. Draft the comment to a file (precedent: `docs/planning/pr80-reply-f2-f3.md`), present its final text before posting (the Present gate), post it with `gh api repos/KJ5HST/methodology/issues/82/comments -F body=@<file>`, and read it back byte for byte (S166's recipe). The review and its script are on this fork's `main`, pushed to `origin` at `31b574b` on the operator's go-ahead, so the comment may point at them by absolute URL (`https://github.com/rmsharp/methodology/blob/main/docs/planning/pr82-review-repro.sh`); the review itself is this fork's shorthand, so the comment carries the substance in plain terms and uses a link only as a pointer to the reproduction script. **The operator added, for the comment:** one improvement to suggest is the readability of #82's stated purpose and methods — *"Use generally recognized terminology with no jargon or private descriptors."* The comment must meet that bar itself: plan codes (D1–D10, P2a–P4c, G1), session numbers (S20, S169), backlog and finding codes (BL-57, F3) and coined names ("the ratchet, not the ruler", "doubled-file Read", "Phase 0 pair") are replaced by plain descriptions; `docs/planning/pr82-review.md` is written in this fork's shorthand and is translated, not pasted. **(2) BL-57'S P3 — ITS OWN SESSION** (`docs/planning/changelog-rules-contradictions-plan.md:490`), as S168 left it, with two changes from #82: if #82 has merged, P3 starts by merging `upstream/main` into the branch (a same-line conflict at `ITERATIVE_METHODOLOGY.md:294`; `CLAUDE.md` already conflicts); and P3's runner criterion (`:508`) and P4's (`:538`) are in bytes — restate them in tokens, measured by the doubled-file Read on the merged tree. **(3) `CHANGELOG.md` IS 256,220 B AFTER THIS CLOSE-OUT, 5,924 B UNDER THE 262,144 B READ REFUSAL** — S170 very likely crosses it — an estimate: S169 added 5,571 B and S168 6,800 B; past it, read with `offset`/`limit`. Not trimming it is the operator's decision — raise it at Phase 0. **(4) `HANDOFFS.md` HOLDS FOUR RECEIPTS** after this close-out: S170's Phase 0 finds four, no trim. **CARRIED, EACH ITS OWN GO-AHEAD:** pushing fork `main` (5 commits ahead of `origin/main` after this close-out); F5/F6 (`docs/planning/pr80-review-response.md:243`); the fork resync; BL-54; BL-36; BL-53; `choose_cut`.
key_files: `docs/planning/pr82-review.md:17` (§0), `:65` (§2 budgets), `:168` (§3.1), `:210` (§3.3), `:233` (§3.4), `:352` (§5, this fork), `:377` (§6, the asks); `docs/planning/pr82-review-repro.sh:1`; on #82 at `c84e7d96`: `.context-budget.json:36` (the pin), `:46` (the runner's ceiling and stale density), `.quality-gates.json:3`, `.githooks/pre-commit:35`, `starter-kit/quality_ratchet.py:177`, `bin/check-handoff:101`, `starter-kit/methodology_dashboard.py:1938`, `:2011`; fork: `docs/planning/changelog-rules-contradictions-plan.md:508`, `:538`; `HANDOFFS.md:15`.
gotchas: **(1) #82 IS LIVE** — pin every claim to a head sha and re-run the script before relaying one. **(2) THE TOKEN INSTRUMENT IS THE READ TOOL'S REFUSAL** — double the file, Read it with a spanning `limit`, halve the count; reproduce a recorded figure first (48,555 for `main`'s pair). **(3) A `sort`ED STAGED LIST FAILS A STRING GUARD** — locale collation; the claim commit silently did not happen until re-guarded as a set (S165's trap, now its own memory). **(4) zsh reads `$r:path` as a modifier** — hit again at this Phase 0; brace it. **(5) #82's `bin/tests.sh` LEAVES TRACKED FILES CLEAN** — the "mutates the live ledgers" caution is this fork's suite's, not #82's; do not raise it upstream. **(6) `HANDOFFS.md`'S FRONT MATTER IS 6,984 OF ITS 7,168 B RESERVE** (`bin/tests.sh` A2, 97%) — the next fold row (this one was 129 B) fits; the fold after that needs a cut first.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`,** in `--no-local` clones, exit codes read bare. **Fork, at the record `4ffcb253`:** 305 passed / 0 failed / 0 skipped, as at a same-time control at `4c07b91` — 0 status flips, no row added or removed, 10 rows differing only in numbers this session moved (the `**Model:**` bullets, now 57, and the model-report totals, now 328; receipts, now 4; the ledger, then 34,674 B, and its front matter, 6,984 B); `check-links` 105 links in 23 files and `check-learnings` OK at both; `context_budget.py --status` exits 2 at both — fork `main`'s runner over its declared 41,364 B byte ceiling, pre-existing and by design. `check-handoff --all --allow-pending` 0 after the claim, trim, fold and record; the shard's `.verify.sh` exit 0 at the trim `0ccfce84` and after the fold. **#82, at `c84e7d96`:** as `what_was_done` records; `context_budget.py --status` 0 there. **NOT EXERCISED:** any push or post; #82 in a real adopter; CI (none); a second reader of the review's findings.
changelog_ref: CHANGELOG.md "2026-09-15 · [ad hoc] S169 close-out — a fork-only review of upstream PR #82; nothing posted", plus the record, fold, trim and claim entries
commit: f89c0faf (claim) + 0ccfce84 (trim) + da8af503 (fold) + 4ffcb253 (record) + this close-out
```

**Self-assessment: 8/10.** Plus: the operator's question was answered in the unit that matters — every figure
came from the doubled-file Read, whose instrument first reproduced three recorded figures exactly — and that
turned up what a byte view hides (−15 B, +62 tokens). Every defect was run in a throwaway repository rather
than read off the code, the saved script was re-run end to end, and every cited anchor was re-checked on its
tree. #82's own claims were reproduced before any was questioned, and one would-be finding — that its suite
mutates the live ledgers — was checked and dropped. The review turned the operator's point on this fork's own
plan: BL-57's P3/P4 runner criteria are in bytes. Nothing went outward. **Minus:** the claim commit silently
failed on S165's sorted-string guard, a trap recorded where I did not look (now its own feedback memory);
zsh's `$r:path` once at Phase 0; no second reader has checked the findings, and the review runs to 24 KB —
§0 and §6 carry it. **Reduction:** `HANDOFFS.md` trimmed to four receipts; `CHANGELOG.md` grew 5,571 B
toward its read refusal. **No learning row** (BL-53 leaves about three).

**Predecessor (S168): 9/10.** Item (2) was exact and used as written: 4,065 B of room against the stub (mine
was 1,550 B), SRF re-derived after the claim, no `--force`. Item (3) put the `CHANGELOG.md` question into the
Phase 0 report, and gotcha (5)'s `rev-parse` trap was avoided this time. Item (1) went unused only because the
operator redirected the session; its P3 sites all re-derived on the branch. **Not 10:** one fact this session
needed was not in it — fork `main`'s own `.context-budget.json` still budgets the read-set in bytes (a 41,364 B
runner ceiling) while upstream moved to tokens at #80's F3 — and it bore directly on today's question. **ROI:
positive.**

```handoff
session: S168
date: 2026-09-15
status: complete
self_score: 8
predecessor_score: 9
active_task: **BL-57'S P2 IS DONE ON BRANCH `bl57/changelog-rules`: `upstream/main` MERGED IN (`9e1dfeb`), THEN `f2bcc22` AND `775ba238` — NOT PUSHED UPSTREAM; BACKED UP TO `origin`.** §The Action Ledger's archive text is now *Reading and archiving* (Q2 A); the `HANDOFFS.md` seed names no size and defers to the trimmer's trigger; the trimmer's `:186` comment drops *"context-tax"*. P2's step 4, D8 (ii), needed no commit — #80's F3 did it. **Next: P3.**
what_was_done: **Fork `main`:** `5eef31f1` claim (with the Phase 0 `dashboard_history.jsonl` snapshot); `30a96bb9` the record (the plan's header and S168 amendment, BL-57's backlog row); this close-out. **Branch**, each commit with its own entry in the branch ledger: `9e1dfeb` merges `upstream/main` `8b4dc2c3`, clean, bringing `.githooks/commit-msg`; `f2bcc22` rewrites `FRAMEWORK_APPARATUS.md` :426–:498 — three partial reads, offset and limit past `READ_REFUSE_BYTES`, archiving optional, `--check` the only trigger, conservation, never in Phase 0 — and drops two *"verbatim"* self-descriptions P2 would falsify (28,022 → 25,983 B; its entry quotes each rule with its line, as P2's DONE asks); `775ba238` rewrites `starter-kit/HANDOFFS.md` :89–:152 (heading kept, D9; rule kept, D7; 11,505 → 10,417 B) and the trimmer comment (AST identical to `b82dcff`). Instruments checked before their numbers were used: §9.1 reproduced the plan's 1,577 lines on `b82dcff`; the new shard enumeration matched a Python count in bash and zsh with no shard (55) and eleven (526).
next_steps: **(1) BL-57'S P3 — ITS OWN SESSION** (`docs/planning/changelog-rules-contradictions-plan.md:490`): the source tags and the anchored, shard-spanning audit in §The Action Ledger; runner `:39` (net ≤ 0), `:278`, `:329`; `ITERATIVE_METHODOLOGY.md:294`; `.githooks/pre-commit:57` — `b82dcff`'s numbers, so re-derive on the branch — **plus the S168 amendment's item (1)**, the `HANDOFFS.md` seed's bare glob (`:117`), which zsh refuses where no shard exists. **(2) `HANDOFFS.md` HOLDS FIVE RECEIPTS**, so S169's Phase 0 trims to four. `SRF_RED` returns at 57,366 B and the file is 53,301 B after this close-out: 4,065 B for S169's claim stub (S168's was 2,050 B). Measure; if the stub would cross, trim before the claim (S161's follow-up precedent) or ask for `--force`. **(3) `CHANGELOG.md` IS 250,649 B, 11,495 B UNDER THE 262,144 B READ REFUSAL**; not trimming it is the operator's decision — raise it at Phase 0. **(4) PUSHED TO `origin` AFTER THIS CLOSE-OUT, EACH ON THE OPERATOR'S GO-AHEAD:** fork `main` (the close-out, then each commit recording a push, so `origin/main` equals `main`), and the branch at `775ba238`, as a backup — so rewriting the branch (a rebase at P12) now needs a force-push. **CARRIED, EACH ITS OWN GO-AHEAD:** F5/F6 (`docs/planning/pr80-review-response.md:243`); the fork resync (4 conflicting files); BL-54; BL-36; BL-53; `choose_cut`.
key_files: Branch at `775ba238`: `FRAMEWORK_APPARATUS.md:426` (*Reading and archiving*), `:440`, `:476` (conservation), `:486`; `starter-kit/HANDOFFS.md:89` (heading, D9), `:91` (the rule), `:117` (the bare glob, P3); `starter-kit/methodology_trim.py:186`; the branch's `CHANGELOG.md:171` (P2's entries; P1's from `:211`). Fork: `docs/planning/changelog-rules-contradictions-plan.md:36` (S168 amendment), `:490` (P3), `:832` (§9.7); `docs/planning/BACKLOG.md:152`; `HANDOFFS.md:15`.
gotchas: **(1) THE BRANCH LEDGER'S TOP IS NOW `upstream/main`'S BLOCK** — a new branch entry goes above BL-57's (`CHANGELOG.md:171` there), below `main`'s. **(2) `git diff --quiet upstream/main <branch>` OVER THE PINNED FILES EXITS 1** — P1's `CLAUDE.md` row (−9 B), not a regression; attribute it before reading it. **(3) P3 EDITS THE RUNNER, WHICH HAS NO SPARE BYTES (K2)** — §9.7 at every boundary; no suite runs it. **(4) GATE EVERY BOUNDARY, NOT ONLY THE END:** a clean clone per commit plus a same-time control, rows compared; `bin/tests.sh` uses `mktemp`, so clones can run side by side. **(5) `git rev-parse --short a b` FAILS** — hit again at this Phase 0.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`,** in `--no-local` clones, exit codes read bare. **Branch:** 118 passed / 0 failed at `77b21a20` (control), `9e1dfeb`, `f2bcc22` and `775ba238`, 0 status flips, no row added or removed; unit suites 211 · 124 · 116 OK at each; `check-links` 107 links in 23 files; `check-learnings` 13 rows; `context_budget.py --status` 0 at each; §9.7 on `775ba238` *nothing over budget* (`CLAUDE.md` 59,159 of 59,168 B); P2's three DONE greps print nothing on `775ba238` and match on `9e1dfeb`. **Fork:** `bin/tests.sh` 305 passed / 0 failed / 0 skipped at the record `30a96bb9`, as at a same-time control at `d2347a16` — 0 status flips, 8 rows differing only in numbers this session moved (receipts, now 5; the `**Model:**` bullets, now 54, and the model-report totals, now 325; the ledger's size); unit suites 321 · 123 · 116 OK; `check-links` 105 links; `check-learnings` 64 rows; `context_budget.py --status` exits 2 at both, the runner over the 41,364 B ceiling its config declares over on arrival (2026-08-30) — by design, not S168's; `check-handoff --all --allow-pending` 0 after the record. **NOT EXERCISED:** any push; GitHub's rendering of the anchor; what *optional* does to ledger growth, which shows only across sessions.
changelog_ref: CHANGELOG.md "2026-09-15 · [BL-57] S168 close-out — BL-57's P2 done on a branch, not pushed; P3 next", plus the record and claim entries
commit: 5eef31f1 (claim) + 30a96bb9 (record) + this close-out; branch 9e1dfeb (merge) + f2bcc22 + 775ba238
```

**Self-assessment: 8/10.** Plus: P2 landed as scoped, with every DONE check run on the committed tree and every
boundary — the control, the merge, both steps — run through every gate in its own clean clone, rows compared,
0 flips. Each instrument was checked before its number was used (§9.1, the shard enumeration, the trimmer by
AST), and two things P2's line list missed were found by reading: the apparatus called the rewritten text
*verbatim* twice, and the seed's pointer described reasoning P2 removed. Minus: `git rev-parse --short a b`
at Phase 0 despite S167's gotcha; §9.1 ran mid-phase rather than at its start (still before the first P2
commit); the seed's matching glob is left to P3 — a scope judgment, not a fix. **Reduction:** none —
`HANDOFFS.md` goes to five receipts, which S169 trims; `CHANGELOG.md` stays untrimmed by the operator's
decision. **No learning row** (BL-53 leaves about three).

**Predecessor (S167): 9/10.** Item (1) was this session's plan exactly — merge first, re-run the suites and
§9.7, then P2 at `:440`, and amend D8 since F3 had done its (ii), which Phase 0 confirmed in one command.
Gotcha (1) is why §9.7 ran at every boundary; gotcha (4), *"re-check where the merged ledger puts them"*, was
the first check after the merge. Every number re-derived held. **Not 10:** the two *"verbatim"* sentences
S167 wrote into the apparatus were certain to go false at P2 and were not flagged. **ROI: strongly positive.**

```handoff
session: S167
date: 2026-09-15
status: complete
self_score: 7
predecessor_score: 9
active_task: **BL-57'S P1 IS DONE ON BRANCH `bl57/changelog-rules` — FOUR COMMITS FROM #80'S HEAD `aa36fd8b`, NOT PUSHED — AND THE MAINTAINER MERGED #80 MID-SESSION** (`4d9e2715`, 19:59 UTC; `upstream/main` `8b4dc2c3`). The seed's three `CHANGELOG.md` rule sections moved verbatim, one level down, to `FRAMEWORK_APPARATUS.md` §The Action Ledger; `starter-kit/CHANGELOG.md` is a 1,335 B pointer carrying `ledger-format: 2`; `bin/status` keys on that marker, and its advice no longer rewrites entries. Every P1 DONE check holds at the final commit `77b21a20`. BL-57's route, a new PR (D5), is open; **P2 starts by merging `upstream/main` into the branch.**
what_was_done: **Fork `main`: `6f9162f1` claim (with the Phase 0 `dashboard_history.jsonl` snapshot); `50498451` the `HANDOFFS.md` retention trim, 57,366 → 38,813 B, S163 + S162 to `docs/archive/HANDOFFS-through-2026-09-15.md`, no `--force` (SRF 0.8755 after the claim); `943059f5` the fold (19 trims, 152 receipts); `f63460e5` the record — the plan's header and S167 amendment, §9.4 corrected for zsh, BL-57's backlog row; this close-out. Branch, each commit with its own entry in the branch's ledger:** `eb06625b` the trimmer's three fence controls read `tools/fixtures/seed-CHANGELOG-ledger-format-1.md` (the pre-P1 seed, blob `47bc8485` asserted), and the dated-prose test's anchor becomes `---`, asserted once first; `b0634606` the move, the thin seed, the `HANDOFFS.md` seed's pointer, a comment-only trimmer edit (AST identical); `2d5dc6e9` `SEED_FORMAT_MARKERS` → `ledger-format: 2` and `Size, and when to archive`, the new advice in `bin/status` and `BOOTSTRAP.md:85`, Test 20 (b) with the marker and (b2) on the frozen seed; `77b21a20` `HOW_TO_USE.md:748`, `CLAUDE.md:21`, and `ITERATIVE_METHODOLOGY.md:556`, a third index the plan missed. **RED first:** the old trimmer tests fail 3 on the thin seed and a fourth passes vacuously (its anchor gone, hazard 5); (b2) fails on the title marker (116/2) and passes after (117/1); mutants of both new guards fail. **Step 4 first landed as `d4841721`, 116 B over upstream `CLAUDE.md`'s pinned 59,168 B ceiling, with every suite green** — only §9.7 saw it; amended to a row 9 B shorter than the original, unpushed. **#80's merge surfaced as Test 9 flipping to PASS**; a same-time control at `aa36fd8b` (116/0) showed it was upstream's.
next_steps: **(1) BL-57's P2 — ITS OWN SESSION** (`docs/planning/changelog-rules-contradictions-plan.md:440`). In `../methodology-bl57`, first merge `upstream/main` into the branch (`git merge-tree` clean at S167; it brings upstream's new `.githooks/commit-msg`, which the next commits must satisfy), and re-run every suite and §9.7 (`:816`) on the branch and on its merge; then P2's scope, and amend D8 (its (ii) was done inside #80 by F3). **(2) DUE NOW THAT #80 HAS MERGED — EACH ITS OWN GO-AHEAD; ASK, DON'T ACT:** F5 and F6 (`docs/planning/pr80-review-response.md:243`); the fork resync — fork `main` vs `upstream/main` conflicts in `.context-budget.json`, `CHANGELOG.md`, `HANDOFFS.md` and `starter-kit/FRAMEWORK_LEARNINGS.md` (the last a policy question: upstream ships rows 1–13). **(3) `HANDOFFS.md` HOLDS FOUR RECEIPTS** after this close-out: S168's Phase 0 finds four, no trim; its claim makes five, so S169's Phase 0 trims. **(4) `CHANGELOG.md` IS 243,849 B AFTER THIS CLOSE-OUT, 18,295 B UNDER THE 262,144 B READ REFUSAL**; S167 added 6,305 B. Not trimming it is the operator's decision (asked at S167's Phase 0; unchanged) — raise it, don't act. **(5) CARRIED:** pushing the branch (to `origin`, as a backup) and fork `main`; S161's (b)/(c), partly moot; BL-54; the two stale planning documents; `HOW_TO_USE.md:774`; BL-36; Test 31; BL-53; `choose_cut`; nine merged `origin` branches.
key_files: Branch at `77b21a20`: `FRAMEWORK_APPARATUS.md:338` (§The Action Ledger), `:9` (intro); `starter-kit/CHANGELOG.md:12` (the marker line); `bin/_manifest.py:87` (marker properties), `:105` (`SEED_FORMAT_MARKERS`); `bin/status:190` (advice); `bin/tests.sh:272` (Test 20 (b)), `:282` ((b2)); `tools/test_methodology_trim.py:62` (the fixture), `:252`, `:1844`, `:2058`; `starter-kit/methodology_trim.py:360`; the branch's `CHANGELOG.md:95`–`:145` (BL-57's four entries, above #80's). Fork `main`: `docs/planning/changelog-rules-contradictions-plan.md:21` (S167 amendment), `:440` (P2), `:787` (§9.4), `:816` (§9.7); `docs/planning/BACKLOG.md:152`; `HANDOFFS.md:15`.
gotchas: **(1) A GREEN SUITE CANNOT SEE A GATE IT NEVER RUNS** — no suite runs `context_budget.py --status` on the tree; run §9.7 at every boundary, and keep upstream `CLAUDE.md` edits net ≤ 0 (pinned at its size). **(2) THE ZSH `$c:` TRAP HID IN THE PLAN'S OWN §9.4** — it printed nothing until braced (now fixed); a check whose right answer includes a known hit must show it. **(3) UPSTREAM MOVED MID-SESSION** — a row that flips can be external; control it at the base, run at the same time. **(4) THE BRANCH'S LEDGER ENTRIES SIT ABOVE #80'S BLOCK AND BELOW `main`'S** (`CHANGELOG.md:95` there); after merging `upstream/main`, re-check where the merged ledger puts them. **(5) `bin/tests.sh` MUTATES BOTH LIVE LEDGERS** — clone only. **(6) `git rev-parse --short a b` FAILS** — hit again at this Phase 0.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`,** in `--no-local` clones, exit codes read bare. **Branch:** `aa36fd8b` 115/1 before #80's merge (Test 9) and 116/0 after, a same-time control; `eb06625b` and `b0634606` 115/1; `2d5dc6e9`, `d4841721` and `77b21a20` 118/0 — against the control, 1 row renamed, 3 added, 0 status flips; unit suites 211 · 124 · 116 OK (4 skipped); `check-links` 107 links (from 105); `check-learnings` 13 rows. `context_budget.py --status` exits 0 on `77b21a20` and on its merge into `upstream/main` (2 at `d4841721`). P1's DONE checks: §9.3 VERBATIM ×3; §9.4 (bash) only `b0634606` of nine versions; the seed 1,335 B, no `## `, `NO_RECORDS` exit 0, seeded by `bin/sync`; six adopter copies' `CHANGELOG.md` stale with the new advice, their `HANDOFFS.md` verdicts equal fork `main`'s. **Fork:** Phase 0 at `6142d538` 304/1/0 (Test 9); shard proof exit 0 at `50498451` and after the fold; `check-handoff --all` 0. **Close-out run**, on this content committed inside a clone before this sentence was written in: **305 / 0 / 0, exit 0** — Test 9 passes on fork `main` since #80's merge (a same-time control at `6142d538` also reads 305/0/0, where Phase 0 read 304/1/0); 0 status flips against that control, 11 rows differing only in numbers this session moved (receipts, now 4; the `**Model:**` bullets, now 53, and the model-report totals, now 324; the front matter, 6,855 B; the fixture's derived id, now S168; the ledger, then 45,609 B). **NOT EXERCISED:** any push; an adopter migration (P6–P11); GitHub's rendering of the anchor.
changelog_ref: CHANGELOG.md "2026-09-15 · [BL-57] S167 close-out — BL-57's P1 done on a branch, not pushed; PR #80 merged upstream; P2 next", plus the record, fold, trim and claim entries
commit: 6f9162f1 (claim) + 50498451 (trim) + 943059f5 (fold) + f63460e5 (record) + this close-out; branch eb06625b + b0634606 + 2d5dc6e9 + 77b21a20
```

**Self-assessment: 7/10.** Plus: P1 landed as the plan's four commits, each run through every suite in a clean
clone, and every DONE check was re-run on the final commit. RED came before GREEN for both behavioural
changes, and both new guards were mutation-tested. **The §9.7 budget check — run because the plan names it,
not because a suite asked — caught a real breach the suites could not see, before anything was published;
and a Test 9 flip was traced to upstream's merge with a same-time control rather than accepted.** Minus: **I
committed step 4 without running the budget gate** — K2 named the runner and `SAFEGUARDS.md`, and I did not
ask which other files the budget pins; the fix was an amend of an unpublished commit. The zsh `$c:` trap,
which my own notes name, made my Phase 0 marker check vacuous and my first post-commit run print nothing —
caught only because P1's commit had to appear. And `git rev-parse --short a b` again. Two small departures
from the plan (one fixture file rather than two literals; a third index updated) are recorded in the plan,
not asked. **Reduction:** `HANDOFFS.md` trimmed to four receipts; `CHANGELOG.md` not trimmed, by the
operator's decision. **No learning row:** it is in memory, and BL-53 leaves about three rows.

**Predecessor (S166): 9/10.** Its item (1) was exactly the Phase 0 check — the PR query, and the conditional
*"if #80 merged: measure Test 9 … (it should pass; don't assume)"*, which became this session's control run
when the merge arrived mid-session. Item (3) sent me to the plan at `:359`, exact; item (4)'s *"re-derive
the dry run after its claim (SRF against `d9ace03`)"* held, and no `--force` was needed. Gotcha (3), the
dashboard command, saved the search S166 had to make. **Not 10:** nothing warned that upstream `CLAUDE.md` is
pinned at its size — outside S166's own work, but P1's step 8 touches it; and gotcha (5) named the
`rev-parse` trap, which I then hit anyway. **ROI: strongly positive.**

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

