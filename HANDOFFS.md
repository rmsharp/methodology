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

**Archived shards — 17 trims, 148 receipts.** Every shard is `docs/archive/HANDOFFS-through-<date>.md`
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

<!-- NEXT TRIMMING SESSION: methodology_trim.py appends a 3-line pointer block here
     (starter-kit/methodology_trim.py:1093 build_pointer_block, :1103 insert_pointer). Fold it into
     the table above as one row (~125 B vs the block's ~448) and delete the block, IN ITS OWN
     COMMIT: inside the trim commit the shipped .verify.sh fails L2 (Learning #58). The generator
     is DISTRIBUTED, so teaching it this is an upstream change. -->

```handoff
session: S164
date: 2026-09-15
status: pending
self_score: pending
predecessor_score: pending
active_task: **PR #80 REVIEW, F2 — GUARD THE DASHBOARD'S DOC-ONLY EXCLUSION FOR EVERY FRAMEWORK-INSTALLED FILE, RED FIRST.** The operator's choice at Phase 0 (A). Generalize `test_a_synced_repo_with_context_budget_installed_is_still_doc_only` over every `FRAMEWORK_INSTALLED_SOURCE` name using the real `starter-kit/` file, and show it fails on the maintainer's mutant (`methodology_trim.py`'s `version_re` and signatures neutralized in both twins) while the current suite stays green. On a local branch from #80's head `d4e1570`, tested in a clone. **Nothing pushed, no PR edit, no reply — each its own go-ahead**; Phase 0 suggested holding F2 locally so F2 and F3 go up in one push.
what_was_done: pending
next_steps: pending
key_files: `tools/test_methodology_dashboard.py:2666` (the test to generalize, at `d4e1570`), `tools/test_methodology_dashboard.py:2642` (the name-completeness gate), `starter-kit/methodology_dashboard.py:360` (`FRAMEWORK_INSTALLED_SOURCE`), `starter-kit/methodology_dashboard.py:484` (the `methodology_trim.py` signature entry), `docs/planning/pr80-review-response.md:79` (§4, the F2 setup).
gotchas: **F2 IS A TEST CHANGE — edit neither dashboard twin except to plant the mutant in a clone.** **`.context-budget.json` IS CONFIG, NEVER SOURCE** (`starter-kit/methodology_dashboard.py:508` at `d4e1570`): decide whether the new test covers it with a config assertion or excludes it with the reason stated. **Branch ledger entries go with #80's block, below `main`'s**; run `git merge-tree` before any push. **`bin/tests.sh` MUTATES BOTH LIVE LEDGERS** — clone only; a `--no-local` clone lacks `upstream/*` refs.
runtime_smoke: Baseline at `755ef09` in a `--no-local` clone: **304 passed / 1 failed / 0 skipped, exit 1** (Test 9, pre-existing). Dashboard 76/100 at Phase 0. Both ledger frontiers current, 0 undocumented commits; tree clean apart from the Phase 0 `dashboard_history.jsonl` snapshot. PR #80 OPEN at `d4e1570`, `MERGEABLE`/`CLEAN`, 2 comments, none new since S163's reply.
changelog_ref: CHANGELOG.md "2026-09-15 · [ad hoc] S164 claim — PR #80 review F2: guard the dashboard's doc-only exclusion for every framework-installed file, RED first"
commit: pending
```

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

```handoff
session: S161
date: 2026-09-11
status: complete
self_score: 7
predecessor_score: 8
active_task: **`read-set-budgets` CAN BE USED IN YOUR PROJECTS TODAY — ANSWERED IN [`docs/planning/read-set-budgets-local-use-routes.md`](docs/planning/read-set-budgets-local-use-routes.md), APPROVED BY THE OPERATOR AND COMMITTED (`14ffe204`).** S160's item (1), scoped by the operator at Phase 0 to part (a), *local use now*; **(b) what the maintainer's merge method does to this fork and (c) what could be sent upstream were offered and NOT chosen — still open if asked.** Route A (a full clone of the branch, `598c459`): clean for 3 of 12 projects, current once #80 merges unchanged. Route B (fork `main`): clean for 8 of 12, but 5 files per project read locally modified against upstream after the merge. GitHub route: exits 1 today and refuses all 12 even after the merge. **Claimed 2026-09-11, closed 2026-09-14**, after re-checking nothing had moved (PR #80 OPEN, `MERGEABLE`, 0 reviews, 0 comments; `upstream/main` `512c2ed`). **`CHANGELOG.md` is now past its trim trigger, by the operator's Phase 0 choice.** Fork-internal: nothing pushed, no PR, no comment.
what_was_done: **Four commits: `18957077f` claim (with the Phase 0 `dashboard_history.jsonl` snapshot), `14ffe204` the document, `0c81e399` Learning #64 and BL-54, plus this close-out.** **Every route was run, never predicted:** the 12 projects carrying a `SESSION_RUNNER.md` (11 at `~/Development/*`, plus `mpc_tests/model_project_constructor`) were copied to scratch as exactly what `bin/sync` and `bin/status` read in commit mode — `.gitignore` plus existing destinations; all 12 are commit mode. Route A ran from a fresh GitHub clone of the branch, Route B from a `--no-local` clone of fork `main`, each dry-run and then applied to fresh copies. A post-merge stand-in (`upstream/main` + `git merge --no-ff 598c459`, tree-identical to `598c459`) re-checked both, and the GitHub route after the merge ran through a harness executing the stand-in's own `bin/sync` with only the network read replaced (document §8). **Every refusal was checked against `--full-history`:** none of today's 12 outcomes is a history artifact, but a branch-then-fork sequence is — 4 files in each of 3 projects — now **BL-54** (`bin/sync:60`, `bin/status:56`). **The Phase 0 pair was metered** with PR #80's doubled-file method, validated first against its recorded 47,805 → 23,902, then on fork `main`: 49,195 → 24,598 — both fit. **Learning #64** (952 B). Also answered, read-only, the operator's mid-session question: removing completed `BACKLOG.md` items is required (`starter-kit/SESSION_RUNNER.md:284`) but nothing enforces it; the dashboard's Signal F (`starter-kit/methodology_dashboard.py:1933`) only reports, and counts 28 done-marked items in `nprcgenekeepr`'s backlog.
next_steps: **(1) HIGH PRIORITY — OPERATOR, 2026-09-14: PLAN BL-57.** Remove the contradictions in the framework's `CHANGELOG.md` rules here and roll the fix into `airqino`, `model_project_constructor`, `mts-system`, `nprcgenekeepr`, `vscode_quarto_ext` and `wsfct`, aiming at an upstream PR — new, or added to #80, each its own go-ahead. A planning session: the plan is the deliverable (`starter-kit/SESSION_RUNNER.md` §Planning Sessions); start from BL-57 in `docs/planning/BACKLOG-DETAIL.md`. **Ledgers:** `HANDOFFS.md` was trimmed back to four after close-out (`16ac3fc97`); **do NOT trim `CHANGELOG.md`** (operator, 2026-09-14): its trimmer trigger will keep firing, which is expected; past 262,144 B, read it with `offset`/`limit`. **(2) PARTS (b) AND (c) OF THE MERGE-OPTIONS REQUEST, IF THE OPERATOR WANTS THEM.** (b) is computable locally: simulate a squash and a rebase of #80 onto `upstream/main` in scratch, then run `git merge-tree --write-tree --name-only` against fork `main`. (c) is options only — every comment or PR is its own go-ahead. **(3) USING THE DOCUMENT IS THE OPERATOR'S, PROJECT BY PROJECT.** A real sync writes into that project: do it in that project's own session, after `bin/status` there, and not in `claude_work` before its methodology files are committed. **Done after close-out for `airqino` only, on the operator's request:** Route A onto a new local branch off its open PR #1; every tracked file `current`; not pushed. **(4) BL-54's FIX** — `--full-history` at two call sites, canonical-only, RED-first on a fixture whose merge drops the other side's change; decide what `bin/status`'s *N versions behind* should count. Its own session. **(5) CARRIED:** the two stale planning documents (`docs/planning/upstream-read-set-pr-plan.md:574`; `docs/planning/port-branch-identity-adjudication.md`); `HOW_TO_USE.md:774` 27 → 28 (distributed — batch it into the next upstream PR); BL-36's stale shard table; Test 31's grep (`bin/tests.sh:1968`); BL-53 (4 rows of room after #64); `choose_cut` (`starter-kit/methodology_trim.py:1014`); nine merged `origin` branches; pushing `main` (41 ahead of `origin/main` after this close-out). Each deletion and the push is its own go-ahead. **(6) RAISED AFTER CLOSE-OUT, ON THE OPERATOR'S REQUEST: BL-55** — nothing enforces removing a completed `BACKLOG.md` item; options costed in `docs/planning/BACKLOG-DETAIL.md`, none decided.
key_files: `docs/planning/read-set-budgets-local-use-routes.md:16` (§0 the answer), `:80` (§3 per-project table), `:116` (§4 after the merge), `:140` (§5 hazards), `:209` (§8 the harness). `bin/sync:25-27` (the source is the checkout), `:60` (the history walk), `:204-208` (bytes first, then history), `:283` (GitHub's empty history), `:291-307` (one modified file refuses all). `bin/status:56`, `:165`. `docs/planning/BACKLOG-DETAIL.md:1564` (BL-54). `starter-kit/FRAMEWORK_LEARNINGS.md:96` (row 64). `starter-kit/methodology_dashboard.py:1933` (Signal F).
gotchas: **(1) A DRY RUN INTO AN EMPTY PROJECT CANNOT REFUSE ANYTHING** (Learning #64) — S160's *"the local route works today"* came from one, and 9 of 12 real projects refuse that route. Test on copies holding exactly what the tool reads. **(2) NEVER UPDATE WITH `--source=github`, EVEN AFTER THE MERGE** — its history is empty (`bin/sync:283`), so every older file blocks; update from a full local clone. **(3) ZSH BIT TWICE, BOTH TRAPS ALREADY IN MY NOTES** — an unquoted `$F` is one word (it produced a false *"0 fork commits"*), and `$r:path` is a history modifier. Put loops over lists in `bash -c` or Python. **(4) `CHANGELOG.md` PAST ITS TRIGGER IS EXPECTED** — no `bin/tests.sh` row runs the trimmer on the live file. **(5) THE DATE MOVED THREE DAYS MID-SESSION** — re-verify upstream and PR state before committing anything that describes them. **(6) `bin/tests.sh` MUTATES BOTH LIVE LEDGERS** — clone only. **(7) READ EXIT CODES BARE** — the dashboard's `exit=0` at Phase 0 was `tail`'s. **(8) READ A CHECKER'S FINDING, NOT ONLY ITS EXIT, EVEN WHEN A FAILURE IS EXPECTED** — `check-handoff` exits 1 on any pending stub, and that exit hid that mine also lacked a `path:line` token in `key_files`. Write the stub's `key_files` as `file:line`, and after the claim run `bin/check-handoff --all --allow-pending` — it must exit 0.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`,** run only in fresh `--no-local` clones. Baseline at `6f3d422` (Phase 0): **304 passed / 1 failed / 0 skipped, exit 1** (Test 9 `github source dry-run failed`, pre-existing — PR #80's cure). **Intermediate run at `0c81e399`: 301 / 4 / 0, exit 1 — THREE NEW TEST 34 FAILURES, MINE:** the claim stub's `key_files` carried no `path:line` token, so `check-handoff --all --allow-pending` failed on the live ledger. Control: S160's claim-time ledger (`467d3ab`) passes it, exit 0; S161's (`18957077f`) fails with exactly that finding. The rows were red at all three S161 commits before this close-out, whose completed receipt replaces the stub: the live ledger now passes `--all`, exit 0. **The deliverable's own evidence is the scratch-copy runs** — 12 projects × 2 routes, dry and applied, then post-merge local and GitHub — every exit code read bare. Bare, live tree: `check-learnings` **0** (0 rows over 1,500 B); `BACKLOG-DETAIL.md.verify.sh` **0**; `methodology_trim.py --check` on `CHANGELOG.md` **1**, `trigger FIRES` (expected); the document's 6 links resolve; `check-handoff` **1** at the claim — for the missing token, not only the pending status — and **0** on this completed receipt, 0 records over 12,288 B. **Close-out runs, on content committed inside a clone (this sentence added after them):** with the completed receipt, before the regression was recorded, **304 / 1 / 0**; on this final content, **304 / 1 / 0, exit 1 — 305 rows, 0 status flips against the Phase 0 baseline, 10 rows differing only in numbers this session moved** (the live `**Model:**` bullets, now 32; receipts, now 5; the fixtures' derived ids, now #65 and S162; the ledger, now 58,000 B; the discovering run, now 303). **NOT EXERCISED:** any real project; the live GitHub API after a merge; squash or rebase merges; CI (none); the pushed path.
changelog_ref: CHANGELOG.md "2026-09-14 · [ad hoc] S161 close-out — local use of `read-set-budgets` answered; `CHANGELOG.md` now past its trim trigger, so S162 has both ledgers to trim", plus the Learning #64 / BL-54 entry, the deliverable entry, and the S161 claim entry
commit: 18957077f (claim) + 14ffe204 (the document) + 0c81e399 (Learning #64, BL-54) + this close-out
```

**Self-assessment: 7/10.** Plus: **every route was run against copies of every real project** — not
predicted from the code, and not tried on an empty target — which is what turned S160's *"the local
route works today"* into 3 of 12 for the branch and 8 of 12 for fork `main`. **Every refusal was checked
against full history before it was attributed**, which is how the one defect (BL-54) was separated from
twelve genuine outcomes. **The token meter was validated against PR #80's recorded figure** before it
measured anything new. **The state was re-verified after a three-day gap** before the document was
committed. The operator's mid-session question was answered with a read-only measurement and no edits.
**Minus:** two zsh traps my own notes already name each cost a call, and one produced a false *"0 fork
commits since the branch"* that I caught only because the blob comparison beside it disagreed. I nearly
reported the dashboard's exit code through a pipe. I loaded a wait tool the harness made unnecessary.
Three wording errors reached the draft and were caught in my own review, after writing rather than
before. **And my claim stub turned three `bin/tests.sh` rows red for three commits:** its `key_files`
named files and line numbers in separate code spans, so it carried no `path:line` token;
`check-handoff` said exactly that at the claim, and I read its exit 1 as the expected *pending* —
Learning #62's lesson, on a gate whose message I did not read. My own intermediate suite run caught
it; this receipt, which replaces the stub, clears it. **Reduction:** none — `CHANGELOG.md` crossed its trigger by the operator's choice and
`HANDOFFS.md` goes to five receipts; both trims fall to S162.

**Predecessor (S160): 8/10.** Its item (1) was the starting point and held: no ref option
(`bin/sync:17`, `:90-94`), the three files upstream lacks, the branch's misleading `gh auth login` hint,
the same five differing files — each re-derived exactly. Its `CHANGELOG.md` estimate was right: the
trigger fell inside S161. Gotchas (5) and (7) were used as written. **Not 9, for one claim that carried
further than its evidence:** *"The local route works today"* rested on a dry run into an empty project —
said so inside the sentence, but headlined as a conclusion — and 9 of the 12 real projects refuse that
route. It also counted 11 projects; a twelfth sits one level down, in `mpc_tests/`. **ROI: strongly
positive** — item (1) removed the first hour of discovery.

```handoff
session: S160
date: 2026-09-11
status: complete
self_score: 8
predecessor_score: 8
active_task: **`HANDOFFS.md` IS BACK TO FOUR RECEIPTS — 59,110 → 37,492 B through claim, trim and fold — AND ITS ARCHIVE TABLE NO LONGER CARRIES A `proof` COLUMN.** Retained S160, S159, S158, S157; **S156 and S155 are frozen in [`docs/archive/HANDOFFS-through-2026-09-09.md`](docs/archive/HANDOFFS-through-2026-09-09.md)**, its `.verify.sh` **exit 0, pinned to the trim commit `cd52df79`, re-run after the fold and still 0**. **Operator decision at Phase 0: pay for the fold by dropping the derivable `proof` column rather than cutting more prose** — front matter **6,351 of the 7,168 B reserve, 817 B spare**; the last two folds each had to cut ~190 B. **Fork-internal: nothing pushed, no PR, no comment, no distributed file touched.** PR #80 at Phase 0: OPEN, `MERGEABLE`, 0 reviews, 0 comments.
what_was_done: **Three commits plus this close-out: `467d3ab6` claim (with the Phase 0 `dashboard_history.jsonl` snapshot), `cd52df79` the trim, `d254adcc` the fold.** `methodology_trim.py --file HANDOFFS.md --cut 4 --write` archived **2 of 6**, no `--force` — **SRF 0.9095** vs `000a843` — L1/L2/L3/P1A OK at write, `CUT_STRADDLES_DAY` because S157 also carries 2026-09-09. **The post-claim re-derive matched the prediction written into the claim entry** (pre-claim: 1 of 5). **THE FOLD WAS BUILT IN SCRATCH AND ASSERTED BEFORE IT TOUCHED THE LEDGER:** the pointer block parsed (exactly one, 448 B); each of the 14 `[proof](…)` cells asserted equal to its own row's shard path plus `.verify.sh` — the rule `HANDOFFS.md:46` states — before the column went (922 B with header and separator); one 125 B row in; counts 14/143 → **15/145**, `n` re-summed. A second script cross-checked every row against the shard it names: 15 rows = 15 files, each `n` = that shard's `handoff` fence count, every proof present. **Then the fold was committed inside a `--no-local` clone and tested there before it was committed here** — the operator's condition. **No learning row:** the lesson (gotcha 1) is in the family of Learnings #24 and #62, and `FRAMEWORK_LEARNINGS.md` has ~4 rows of room before BL-53 must be answered.
next_steps: **(1) OPERATOR REQUEST, MADE AFTER THIS CLOSE-OUT: CLARIFY THE UPSTREAM MERGE OPTIONS — S161's deliverable unless the operator says otherwise.** Scheduled here, not started. PR #80 (`read-set-budgets` → `main`) is OPEN, `MERGEABLE`, 0 reviews, 0 comments (re-checked after close-out); merging is the maintainer's, and replying or asking him anything is outward-facing, its own go-ahead. **Measured after close-out, to start from:** `bin/sync --source=github` has **no ref option** — it reads upstream's default branch only (`bin/sync:17`, `:90-94`) — and upstream `main` lacks 3 of the 27 distributed files (`starter-kit/FRAMEWORK_LEARNINGS.md`, `starter-kit/methodology_trim.py`, `FRAMEWORK_APPARATUS.md`), so a GitHub dry run exits 1 and writes nothing (its `gh auth login` hint misnames a 404). **The local route works today:** the branch's own `bin/sync`, run from a clone at `598c459` into an empty project, dry run exits 0 — `bin/sync:25-27` syncs from whichever checkout it lives in. Fork `main` contains the branch, but **5 of the 27** distributed files differ from it (`SESSION_RUNNER.md`, `FRAMEWORK_LEARNINGS.md`, `BOOTSTRAP.md`, `methodology_dashboard.py`, `HOW_TO_USE.md`). 11 projects under `~/Development` carry a `SESSION_RUNNER.md`. **(2) `CHANGELOG.md` REACHES ITS OWN TRIM TRIGGER NEXT SESSION — an estimate from growth, not a measurement.** **191,936 B after this close-out's entry — 4,672 B under the 196,608 B** Class A threshold (measured; the follow-up entry that added item (1) takes more); S156–S159 each added **6,283–9,548 B**. **Crossing it should not flip the suite:** no `bin/tests.sh` line runs the trimmer on the live file (`:258` is its unit tests, `:295` a fixture) — `bin/tests.sh` is the only file checked. Run `python3 starter-kit/methodology_trim.py --file CHANGELOG.md --check` at Phase 0 and again after the claim. **SRF 0.5329** vs `aaa6d30` today — no `SRF_RED`; re-derive, and any `--force` is its own operator ask. A CHANGELOG trim is its own deliverable. **(3) `HANDOFFS.md` HOLDS FOUR** — the next Phase 0 does not trim; the one after does. A fold now costs a 125 B row against 817 B spare, so **no byte negotiation for ~6 folds**. **(4) REPAIR THE TWO STALE PLANNING DOCUMENTS** — `docs/planning/upstream-read-set-pr-plan.md:574` (*"Nothing exists to open a PR from today"*, refuted by #80) and `docs/planning/port-branch-identity-adjudication.md` (0 hits for `read-set-budgets`). Fork-only. **(5) `HOW_TO_USE.md:774` (27 → 28) IS A DISTRIBUTED FILE** (`bin/_manifest.py:63` → `docs/methodology/HOW_TO_USE.md`) — no earlier handoff said so. The fix reaches adopters only through upstream: batch it into the next upstream PR. **(6) BL-36's TABLE IS STALE** (`docs/planning/BACKLOG-DETAIL.md:811`): it lists six shards, and 15 `HANDOFFS` shards now exist. Three of their proofs fail (gotcha 2). Whoever works BL-36 re-runs every proof first. **(7) CARRIED:** Test 31's grep (`bin/tests.sh:1968`, its own ask); BL-53 (~4 rows); the `HANDOFFS.md` density record; `choose_cut` (`starter-kit/methodology_trim.py:1014`); nine merged `origin` branches; pushing `main` (36 ahead of `origin/main` after this close-out). Each deletion and the push is its own go-ahead.
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

