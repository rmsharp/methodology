# HANDOFFS.md — archive: 2026-09-09 → 2026-09-09

Retired records from [`HANDOFFS.md`](../../HANDOFFS.md), moved here so the live ledger stays small enough to read
in one pass. Same format, same newest-on-top order — this is the same ledger, continued.

Holds **1 record(s), 2026-09-09 → 2026-09-09**. Cut key: `2026-09-09`. Counts here are computed from the file
itself, never carried forward. This shard is frozen: it states no forward-looking rule,
because the live file owns those and a copy of one was wrong a day after it was written.

---

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

