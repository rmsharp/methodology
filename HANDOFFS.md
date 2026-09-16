# Handoff Receipts — durable close-out proof

This repository dogfoods its own methodology: every session records a durable, machine-checkable
`handoff` receipt here at close-out (Phase 3D), and Phase 0 reconciles it against `git log`. See
[`starter-kit/HANDOFFS.md`](starter-kit/HANDOFFS.md) for the block format and the write points, and
`bin/check-handoff` for the checker. Newest on top; prepend-only.

**Retention policy — this ledger keeps ONE receipt.** Everything older is archived under
`docs/archive/` and indexed in the table below. **N=1 is an operator decision (2026-09-16, S172)
replacing S127's N=4**, taken against BL-59's measurement: of five consumers only `bin/model-report`
reads a receipt below the newest, and it globs the shards, so archiving costs it nothing. The handoff is done by the newest receipt alone. **`methodology_trim.py` fires on BYTES
(196,608 B), never on a record count**, so the policy is applied by the session that notices: at
Phase 0 run `grep -c '^```handoff' HANDOFFS.md`; above 1, trim with `--cut 1 --force`. The force is
warranted, not an override: `SRF_RED` refuses every on-schedule retention trim by construction, and
H3's own largest-drop boundary reads green in the same report (BL-59). `bin/check-handoff` validates the 13-key schema on the **newest** receipt; `--all` checks every
receipt and `--archived` a frozen shard. Below three receipts `bin/tests.sh` Test 34 prints six
named `SKIP` rows — stated, never silent.

> **⚠ N=1 MEANS A TRIM EVERY SESSION AND THE 7,168 B HEADER RESERVE (Test 39 A2) IS SPENT.** Each
> trim-and-fold adds ~147 B of archive-table row. **The next trim reddens Test 39 unless this front
> matter is shortened first** — the table is the cut (BL-59; measured S172, not projected).

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
| 6 | 2026-09-15 → 2026-09-16 | [`HANDOFFS-through-2026-09-16.md`](docs/archive/HANDOFFS-through-2026-09-16.md) | v1.5.0 |

<!-- NEXT TRIMMING SESSION: methodology_trim.py appends a 3-line pointer block here
     (starter-kit/methodology_trim.py:1093 build_pointer_block, :1103 insert_pointer). Fold it into
     the table above as one row (~125 B vs the block's ~448) and delete the block, IN ITS OWN
     COMMIT: inside the trim commit the shipped .verify.sh fails L2 (Learning #58). The generator
     is DISTRIBUTED, so teaching it this is an upstream change. -->

```handoff
session: S172
date: 2026-09-16
status: complete
self_score: 8
predecessor_score: 8
active_task: **BL-57's P3 IS DONE ON BRANCH `bl57/changelog-rules` — THREE COMMITS, NOT PUSHED — AND S169's AMENDMENT IS DISCHARGED: P3's AND P4's RUNNER CRITERIA ARE NOW WRITTEN IN TOKENS.** `[BL-<N>]` became `[BL-<id>]` and the one-line audit became the anchored, shard-reading, `git ls-files` form, in §The Action Ledger, the runner, the flight manual and the ledger hook; the `HANDOFFS.md` seed's bare glob (P2's carried bullet) went with it. **#82 was re-checked at Phase 0 and is still OPEN at `c84e7d96`,** so the merge-first amendment did not trigger and P3 ran on the branch as it stood.
what_was_done: **Branch `bl57/changelog-rules` (from `775ba238`), 4 commits, each with its own entry in the branch ledger:** `d771439` — `FRAMEWORK_APPARATUS.md` §The Action Ledger states the vocabulary as `[issue #<N>]` / `[BL-<id>]` / `[ad hoc]` and publishes the audit as `cat CHANGELOG.md $(git ls-files 'docs/archive/CHANGELOG-*.md') | grep -cE '^### …'`, with all three of its load-bearing properties stated in place; `e47ca14` — the runner's inline audit grep at `:39` becomes a link to that section, and `:278`, `:329`, `ITERATIVE_METHODOLOGY.md:294`, `.githooks/pre-commit:57` take `[BL-<id>]`; `cf20a3b` — the `HANDOFFS.md` seed enumerates its shards with `git ls-files`; `18962a9` — a **correction I caught in my own text at close-out**: §The Action Ledger attributed the *78 against 64* count to *"this framework's own ledger"*, and this tree's root ledger records no such comparison, so the sentence now leads with the mechanism and gives the figure as a measurement on the project it came from. **Fork `main`, 2 commits:** `cee2654` claim (carrying both Phase 0 instrument snapshots, so no `--no-verify` commit was owed) and `44a1e20` the record — the plan's S172 amendment, both restated criteria, and BL-57's backlog row. **THE MEASUREMENT CAME FIRST AND ITS INSTRUMENT WAS CHECKED FIRST:** both published controls reproduced EXACTLY — the runner doubled to **36,955** (18,477.5 tok) and the Phase 0 pair to **48,555** (24,277.5 tok). **`b82dcff`, `upstream/main` and P3's start are the SAME BLOB `c0550acd`** (`git rev-parse` on all three), so one measurement served P3's start criterion and P4's `b82dcff` baseline — and S169's recorded control *was* that number all along. **The restated criterion then failed my own first edit and I fixed the edit, not the rule:** link + id changes measured **+36 B but only +9 tokens**; after two duplicate clauses came out the runner ended **52,163 B / 18,463.5 tok — 32 B and 14 tokens UNDER its start**, pair 24,263.5 of 25,000.
next_steps: **(1) BL-57's P4 — ITS OWN SESSION, AND IT IS THE RANKED DELIVERABLE** (`docs/planning/changelog-rules-contradictions-plan.md:514`): entry lifecycle and the words (C3, C7, C8, C11, C13), at least three commits. Its size criterion is now in tokens and **P4 starts 14 tokens under `b82dcff`'s figure** — doubled read must stay ≤ 36,955. Branch `bl57/changelog-rules` at `18962a9`, worktree `../methodology-bl57`, clean. Re-check #82 first: still OPEN at `c84e7d96` as of this close-out, and if it has merged P4 starts by merging `upstream/main` (a same-line conflict at `ITERATIVE_METHODOLOGY.md:294`, which P3 just edited). **P4 INHERITS ONE ITEM ITS SCOPE DOES NOT NAME:** the last live `[BL-<N>]` outside frozen history is in the branch's root `CHANGELOG.md` front-matter tag list; P4 step 5's cited `b82dcff:14` was the inline audit grep, not a definition list, because upstream's front matter has grown since. Treat the definitions as their own item. **(2) RESOLVED AFTER CLOSE-OUT, BY OPERATOR DECISION: RETENTION IS NOW N=1 AND THIS FILE HOLDS ONE RECEIPT** (75,185 → 20,820 B; six records in `docs/archive/HANDOFFS-through-2026-09-16.md`, proof exit 0). It needed a test fix first: `bin/tests.sh` Test 38 sourced its fixture from THIS file, so at one receipt the suite went **285 passed / 14 failed**; it now reads `tools/fixtures/handoff-ledger-2-records.md`, with a drift guard on the live format. **The binding constraint is no longer receipt count but the header reserve** — a trim is now owed every session and the reserve is spent, so the next trimming session must shorten this file's front matter first; see its warning. **(3) NO REPLY ON #82** — re-checked this session: comment `5691623656`, `updated_at == created_at`, body still sha256-identical (`62821afb…`) to `docs/planning/pr82-comment.md`; #82 OPEN, head unmoved. A reply is its own go-ahead. **(4) NO LEARNING ROW WAS ADDED, DELIBERATELY** — the candidate (a byte rule misprices a cross-reference) is already carried by rows #46 and #60, and `starter-kit/FRAMEWORK_LEARNINGS.md` is 79,483 of 81,920 B with about two rows left under BL-53's unresolved retirement policy; spending one to restate an existing rule would pre-empt the operator's decision. **CARRIED, EACH ITS OWN GO-AHEAD:** pushing fork `main` (**count it, never read it here: `git rev-list --count origin/main..main`** — a figure written into a file inside the repository it counts is falsified by the commit that records it; this receipt said 17, then 18, and each commit that fixed it moved it again) and backing up the branch to `origin` (P3 is on no remote); F5/F6 (`docs/planning/pr80-review-response.md:243`); the fork resync; BL-58; BL-53; BL-54; BL-36; `choose_cut`.
key_files: On the branch at `18962a9`: `FRAMEWORK_APPARATUS.md:355` (the vocabulary), `:370` (the audit command), `:374` (why each of its three properties is there); `starter-kit/SESSION_RUNNER.md:39` (the link that replaced the grep), `:278` (Phase 3F), `:329` (failure mode #27); `ITERATIVE_METHODOLOGY.md:294`; `.githooks/pre-commit:57`; `starter-kit/HANDOFFS.md:118` (the shard enumeration). On fork `main` at `44a1e20`: `docs/planning/changelog-rules-contradictions-plan.md:508` (P3's criterion, now in tokens), `:544` (P4's), the S172 amendment block above §0, `docs/planning/BACKLOG.md:152` (BL-57's row).
gotchas: **(1) THE TOKEN INSTRUMENT HAS A PRECONDITION NOBODY WROTE DOWN: THE MULTIPLE MUST CROSS 25,000 TOKENS, OR THE READ SUCCEEDS AND YOU GET THE FILE INSTEAD OF A COUNT.** I doubled `SAFEGUARDS.md` (16,353 B) and the Read returned all 492 lines — about 12,000 tokens of context spent for nothing. Sextupling it refused at 34,805, so the file is ≈5,800.8 tokens. Check `bytes / 2.8 > 25,000` before building the concatenation. **(2) A CRITERION RESTATED INTO A NEW UNIT STILL HAS TO BE MEASURED AGAINST THE WORK** — my first edit passed nothing: +9 tokens over a criterion I had just rewritten. The session that restates a gate is grading its own paper; restate first, edit second, and let the measurement fail you. **(3) `grep -c` AND `grep -F` EXIT 1 ON ZERO MATCHES** — P3's DONE check is *"prints nothing"*, so **exit 1 is the PASS**. Read the exit code against what the check means. **(4) `python3 starter-kit/context_budget.py --status` LEAVES AN UNTRACKED `.context-budget-history.jsonl` IN AN UPSTREAM TREE** — upstream neither tracks nor ignores it, where fork `main` tracks it; delete it after measuring or the next Phase 0 finds a dirty worktree. **(5) NOTHING MECHANICAL CHECKS WHERE A MEASURED NUMBER CAME FROM** — the *78 against 64* attribution passed every gate and was caught only by grepping this tree for the figure's provenance. **`bin/check-links` STRIPS THE ANCHOR AND CHECKS FILE EXISTENCE ONLY** (`bin/check-links:104`), so it did not verify `#the-action-ledger`; that was checked by hand against `FRAMEWORK_APPARATUS.md:338`. **(6) FORK `main` AND `upstream/main` DISAGREE ABOUT BUDGETING THE TWO LEDGERS** — #80's F3 moved them into `_deliberate_exclusions` upstream; fork `main` still budgets both, which is why `HANDOFFS.md` reads red here and not on the branch.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`,** run in `--no-local` clones whose HEAD sha was asserted equal to the source tree's before anything was measured, exit codes read bare. **Branch, at `cf20a3b` and again at `18962a9` (HEAD sha asserted both sides each time):** `bin/tests.sh` exit 0, **118 passed / 0 failed** — identical to S168's control; `bin/check-links` exit 0, **108** links across 23 files, against **107** measured at `775ba23` in the same clone, so the delta is exactly the one link P3 added; `context_budget.py --status` exit 0; `grep -F '[BL-<N>]'` over all seven files exits 1. **Fork `main`, at `44a1e20` (asserted both sides):** `bin/tests.sh` exit 0, **305 passed / 0 failed / 0 skipped** — identical to S169's, S170's and S171's controls; `check-links` 0 (105 links, 23 files), `check-learnings` 0 (65 rows), `check-handoff --all --allow-pending` 0 (7 receipts). `context_budget.py --status` exits 2, **diffed against the Phase 0 reading: 0 status flips**, three rows moved and all three by this session's own writes (`HANDOFFS.md` +1,314 tok from the claim stub, `BACKLOG.md` +33 B, growth run 128→129). **DONE criteria run, not predicted:** `grep -F '[BL-<N>]'` over the runner, the flight manual, `HOW_TO_USE.md`, the hook, §The Action Ledger and both seeds exits 1 (no matches); the audit returns the same number in zsh and bash on the branch (57 = its heading count), on this repo (556) and on all six adopters; in a throwaway repository with one entry and no shard the bare glob prints **0 under zsh and 1 under bash** while the `git ls-files` form prints 1 and exits 0 in both. **NOT EXERCISED:** any push; P4; any reply from the maintainer; the `HANDOFFS.md` retention trim; the six adopters' own suites (their ledgers were read, not written); CI (there is none); a second reader of P3's text.
changelog_ref: CHANGELOG.md "2026-09-16 · [BL-57] S172 close-out", plus the claim and the record entries; on the branch, one entry per commit
commit: cee2654 (claim) + 44a1e20 (record) + this close-out; branch d771439 + e47ca14 + cf20a3b + 18962a9
```

**Self-assessment: 8/10.** Plus: the instrument was checked before its numbers were used, and both
published controls reproduced to the digit. The criterion I was sent to restate then **failed my own
first edit by 9 tokens, and I fixed the edit rather than loosening the rule** — which is the whole
hazard of a session rewriting the gate that binds it. Every DONE criterion was run rather than
predicted, including the two the plan said would be findings if they moved: both §4.4 changes were
explained down to the single entry that caused each, and this repo's 556-against-494 resolved exactly
— **494 is the count of entries dated on or before §4.4's own measurement date**, so S171's twelfth
shard demonstrably moved nothing out of the audit's reach. The bare-glob defect was reproduced in a
throwaway repository and turned out worse than the plan claimed: not an error, but **two shells
returning two different counts**. I found that `b82dcff`, `upstream/main` and P3's start are one blob,
which made a measurement three handoffs had called outstanding already-taken. **Minus:** I misused the
token instrument — doubling a file too small to trip the refusal returned the whole file and burned
about 12,000 tokens of context on nothing, a precondition I could have checked with one division. And
before settling the criterion I spent a stretch shaving prose to hit a byte target, which is precisely
the instrument the session existed to replace; the right order was restate, then edit. **Reduction:**
the runner is 32 B and 14 tokens smaller than it started and the framework publishes one audit instead
of four; against that, `CHANGELOG.md` and `HANDOFFS.md` both grew, and `HANDOFFS.md` is now 2,446
tokens over a live ceiling.

**Predecessor (S171): 8/10.** Item (1) was exact and was used start to finish — the plan line, the
worktree path, the branch, the sha, and the *conditional* it turned on: *#82 still OPEN, so the
merge-first amendment does not trigger*. I re-checked rather than assumed, and it held. Item (3) gave
the command, the comment id and the requirement to re-verify by hash, all of which reproduced. Item (2)
did the right thing with a decision that was not its to make: it costed the receipt-ledger trim and
handed it over instead of running it on sight. Two of its gotchas fired: **`grep -c` exits 1 on zero
matches** arrived at the exact moment P3's *"prints nothing"* check exited 1, and reading that as the
pass it was came straight from the handoff; and its sequencing lesson meant both Phase 0 instrument
snapshots rode the claim commit, so this session owed no `--no-verify` commit at all. **Not 9:** the
item it ranked first opened with *"that measurement is not done, so P3 begins with it"* — and the
measurement was done, at S169, recorded in this fork's own review as *"`main`'s runner 36,955."* Two
`git rev-parse` calls show `b82dcff`, `upstream/main` and the branch share blob `c0550acd`, which makes
that control the P3 baseline exactly. Three consecutive handoffs carried the instruction to measure
without noticing the number was already in hand. **ROI: strongly positive** — it turned the session's
first hour into verification instead of discovery.


