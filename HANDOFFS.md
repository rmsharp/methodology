# Handoff Receipts — durable close-out proof

This repository dogfoods its own methodology: every session records a durable, machine-checkable
`handoff` receipt here at close-out (Phase 3D), and Phase 0 reconciles it against `git log`. See
[`starter-kit/HANDOFFS.md`](starter-kit/HANDOFFS.md) for the block format and the write points, and
`bin/check-handoff` for the checker. Newest on top; prepend-only.

**Retention policy — keep ONE receipt, trim above TWO.** Everything older is archived under
`docs/archive/` and indexed in the table below. **N=1 is an operator decision (2026-09-16, S172)
replacing S127's N=4**, taken against BL-59's measurement of what actually reads this file: the
handoff is done by the newest receipt alone. **Depth and trigger are separate on purpose:**
every trim pays a FIXED ~16 KB proof, so the trigger sits one above the depth (BL-60). **`methodology_trim.py` fires on BYTES (196,608 B),
never on a record count**, so the policy is applied by the session that notices: at Phase 0 run
`grep -c '^```handoff' HANDOFFS.md`; **above 2**, trim with `--cut 1 --force`. The force is
warranted, not an override — `SRF_RED` refuses every on-schedule retention trim by construction
(BL-59). `bin/check-handoff` validates the 13-key schema on the **newest** receipt; `--all` checks
every receipt and `--archived` a frozen shard. Below three receipts Test 34 prints six named `SKIP` rows — stated, never silent.

> **⚠ THE 7,168 B HEADER RESERVE (Test 39 A2) IS SPENT.** Each trim-and-fold adds ~147 B of
> archive-table row and only ~60 B remain. **The next trim reddens Test 39 unless this front matter
> is shortened first** — the table is the cut. The trigger at 2 halves the rate, not the debt
> (BL-59; measured S172, not projected).

**Two session sequences share this ledger and their numbers collide.** This fork and
`upstream/main` each run their own `S<N>` counter, so a receipt is identified by **session + date**,
never by number alone. **Every upstream receipt is now archived**; all four retained here are the
fork's. At a resync the two sequences stay separate and unrenumbered, each incoming receipt is
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
session: S173
date: 2026-09-16
status: complete
self_score: 8
predecessor_score: 8
active_task: **BL-57's P4 IS DONE ON BRANCH `bl57/changelog-rules` -- FIVE COMMITS AFTER A MERGE OF #82, NOT PUSHED -- AND P5 NOW OPENS WITH AN OPERATOR DECISION.** Upstream PR #82 merged at `64f23bf` (verified at Phase 0), so S169's merge-first amendment triggered: the branch took `upstream/main` first (`52ad407`), P4's size criterion was restated on that base and committed on fork `main` (`1d05e4b`) BEFORE any P4 edit, and P4 then met it -- runner 18,858.5 tokens against <= 18,865.5, `CLAUDE.md` 23,476.5 against <= 23,482.5. **P5's port command, as the plan writes it, now carries #80's and #82's upstream changes along with BL-57's** (34 files against BL-57's own 16), so the operator chose: resync fork `main` first, then port.
what_was_done: **Branch `bl57/changelog-rules`, `18962a9` -> `83a12f0`:** `52ad407` merges `upstream/main` `64f23bf` -- two one-line conflicts, both predicted at Phase 0: `ITERATIVE_METHODOLOGY.md:294` keeps upstream's new step (c) with P3's `[BL-<id>]`, and `CLAUDE.md:21` keeps upstream's shortened row with P1's change. Then P4, one ledger entry per commit: `0c20022` -- §The Action Ledger's *Lifecycle* (`FRAMEWORK_APPARATUS.md:439`: one entry per commit, never edited; the claim commit's *(in progress)* entry; the unpublishable-content exception; a backfill may span commits; where the Phase 1B marker lives) and *Placement* (`:454`: prepend under the topmost `## YYYY-MM`, start month headings at the next new month, retrofit nothing); `f235db3` -- *append* becomes *prepend* at seven sites (runner `:281`, `:332`, `:360`; `ITERATIVE_METHODOLOGY.md:294`; `HOW_TO_USE.md:767`, `:804`; `.githooks/pre-commit:70`), and runner `:88` plus `ITERATIVE_METHODOLOGY.md:169` say the claim commit's entry reads *(in progress)*; `836e0d2` -- *completed work history* becomes the action ledger in `BOOTSTRAP.md`, `README.md` and `CLAUDE.md`, and `CLAUDE.md:21` becomes *"tables, tests, scoring scales and ledger rules"*; `83a12f0` -- upstream's root `CHANGELOG.md` front matter (D8 i): the rules pointer, the audit, `[BL-<id>]`, month headings. **Fork `main`:** `d7d12ee` claim; `1d05e4b` the plan's S173 amendment and the restated criterion; this close-out records P4 done and findings (6)-(10). **MEASURED, NOT PREDICTED, AND THE MEASUREMENTS FOUND TWO THINGS:** (a) the merge alone put `CLAUDE.md` **4 tokens over its 23,483 ceiling** -- P1's row wording was 9 B shorter and 4 tokens longer, and `context_budget.py` reported it ok because it prices the file at 2.519 B/token; `836e0d2` repays it and 6 more; (b) **the token instrument changed** -- the Read no longer refuses past 25,000 tokens, it returns a 25,000-token page with the count in its notice, so the last three readings ran in a subagent that reproduced a control in the same run.
next_steps: **THE OPERATOR DECIDED BY PICKER AFTER THIS CLOSE-OUT (2026-09-16): S174 does the `HANDOFFS.md` header cut; then resync fork `main` with `upstream/main`; then P5.** **(1) S174 -- THE `HANDOFFS.md` HEADER CUT** (BL-59): 140 B of the 7,168 B reserve is left, one archive-table row. S174's claim makes 3 receipts, so S175's Phase 0 calls the trim, and the cut must land first. Folding the archive table into its own shard index is the identified cut. **(2) THEN THE FORK RESYNC:** merge `upstream/main` into fork `main` -- 53 commits; `git merge-tree --write-tree --name-only main upstream/main` lists 12 conflicting files (re-run it, upstream may move). **(3) THEN BL-57's P5** (`docs/planning/changelog-rules-contradictions-plan.md:655`; finding (9) and the decision at `:129`): port BL-57's own change, `git diff 64f23bf bl57/changelog-rules -- . ':!CHANGELOG.md' ':!HANDOFFS.md' ':!.context-budget.json'` (16 files, +532/-252), NOT the plan's `b82dcff` form (34 files, carries #80 and #82). P5's *"494"* audit figure is stale (556 at S172). **(4) FOR P12, NOT NOW:** re-measure the runner (branch blob `4811f02f`) and `CLAUDE.md` (`dd416ea0`) and update their `bytes_per_token`/`measured_bytes` in the branch's `.context-budget.json` (finding (10), `:139`). **PUSHED ON THE OPERATOR'S GO-AHEAD:** the branch (`775ba23..83a12f0`) and fork `main`, both to `origin`. **DECIDED AFTER CLOSE-OUT (picker):** F5 rides BL-57's P12 PR, F6 closed; BL-53's retirement rule is decided inside the resync; BL-54 is fixed after P5, before P6; BL-60 gets one planning session that folds BL-36 in. **CARRIED:** `choose_cut`.
key_files: Fork `main`: `docs/planning/changelog-rules-contradictions-plan.md:84` (S173 amendment: the merge, the instrument, the +4-token finding, both trees' gates), `:114` (P4 done; findings (6)-(10)), `:129` (finding 9 and the decision), `:637` (P4's restated criterion), `:655` (P5); `docs/planning/BACKLOG.md:152` (BL-57's row). Branch at `83a12f0`: `FRAMEWORK_APPARATUS.md:439` (*Lifecycle*), `:454` (*Placement*); `starter-kit/SESSION_RUNNER.md:88`, `:281`, `:332`, `:360`; `ITERATIVE_METHODOLOGY.md:169`, `:294`; `HOW_TO_USE.md:748` (~535 lines), `:767`, `:804`; `.githooks/pre-commit:70`; `starter-kit/BOOTSTRAP.md:23`, `:107`, `:131`, `:139`, `:145`; `README.md:96`, `:114`, `:200`; `CLAUDE.md:21`, `:51`; root `CHANGELOG.md:11` (rules pointer), `:15` (audit), `:22` (`[BL-<id>]`), `:36` (month headings); `.context-budget.json` (the densities P12 re-measures).
gotchas: **(1) THE DOUBLED-FILE TOKEN METER NOW COSTS A 25,000-TOKEN PAGE.** Above 25,000 tokens the Read returns the first page and prints *"(N tokens, cap 25000)"*; a one-line `limit` prints no count. My first two direct readings spent ~50,000 tokens of context before I saw it. Build the N-fold file in the scratchpad, dispatch a `general-purpose` agent with `model: opus` whose only job is to Read with no offset/limit and copy each notice verbatim, put a recorded control in the SAME run (`c0550acd` doubled = 36,955; `64f23bf`'s runner = 37,731; its `CLAUDE.md` = 46,965), and `cmp` the measured file against `git show <commit>:<path>` doubled afterwards. **(2) `context_budget.py` CANNOT SEE TOKEN GROWTH IN A BYTE-SHRINKING EDIT** -- it prices a file at its recorded density, so P1's row read 23,479 in the tool and 23,486.5 in fact. Any `CLAUDE.md` or runner edit gets a doubled read, not only the tool. **(3) A MERGE COMMIT HAS NO BRANCH LEDGER ENTRY** -- the pre-commit hook skips merges, and `9e1dfeb` set the precedent; fork `main`'s entry records it. **(4) THE PLAN'S LINE NUMBERS ARE `b82dcff`'s** -- three of P4's had moved; P5's are older still. Grep every site. **(5) `git rev-parse --short` TAKES ONE REF** -- hit again this session, as at S165-S168's Phase 0s; loop over refs. And in zsh, `echo ======` is `=cmd` expansion and errors. **(6) THE ORDER THAT HELD:** measure the base, restate the criterion, commit the restatement on fork `main`, THEN edit -- `1d05e4b` predates `0c20022`, which is what makes the criterion evidence rather than a target I drew around my own result.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bin/tests.sh` PLUS #82's DECLARED GATES,** run in `--no-local` clones whose HEAD sha was asserted equal to the source tree's before anything ran, exit codes read bare, the clone reset between runs. **`upstream/main` `64f23bf` (the base):** `bin/tests.sh` exit 0, 139 passed / 0 failed; `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results 15c73dda424f · manifest 08423c179055`; `bin/check-links` 107; `context_budget.py --status` exit 0. **The merge `52ad407`:** 141 / 0; `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results c5fca86e4674 · manifest 08423c179055`; 110 links; exit 0, no status flips against upstream's output. **P4's head `83a12f0`:** `bin/tests.sh` exit 0, **141 passed / 0 failed**; `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results c5fca86e4674 · manifest 08423c179055` (the merge's hash: every measured value unchanged); `bin/check-links` exit 0, 110 links; `context_budget.py --status` exit 0, and diffed row by row against `upstream/main`'s output **no status flips**, read-set total **70,253 B against upstream's 70,276 B** (+9 B over the merge, the runner's). **Fork `main` budget:** exit 2 as at Phase 0; one flip, `HANDOFFS.md` ok→warn (density drift from this receipt; see the ledger entry). **DONE criteria run, not predicted:** `grep -nE '[Aa]ppends? (a|one) dated|Append the owed entry'` over the runner, the flight manual, `HOW_TO_USE.md` and the hook exits 1; `grep -ni 'completed work history'` over `BOOTSTRAP.md`, `README.md`, `CLAUDE.md` finds only `README.md:530` (v2.1 *What's New*); P3's `[BL-<N>]` grep still exits 1; the audit gives 68 in zsh and bash, equal to the heading count (the old unanchored form: 94); runner doubled **37,717** (<= 37,731), `CLAUDE.md` doubled **46,953** (<= 46,965), each beside a reproduced control and `cmp`-identical to the committed blob; `SAFEGUARDS.md` blob `933816b4` = upstream's. **NOT EXERCISED:** any push or other outward action; P5; the six adopters (untouched); CI (none); a second reader of P4's text; `bin/model-report` (absent on this tree).
changelog_ref: CHANGELOG.md "2026-09-16 · [BL-57] S173 close-out", plus the claim and the restated-criterion entries; on the branch, one entry per P4 commit
commit: d7d12ee (claim) + 1d05e4b (restated criterion) + this close-out; branch 52ad407 (merge) + 0c20022 + f235db3 + 836e0d2 + 83a12f0
```

**Self-assessment: 8/10.** Plus: the order held. I measured the base, restated the criterion, and
committed the restatement (`1d05e4b`) before the first P4 edit (`0c20022`), so the numbers P4 is judged
by were fixed before P4 existed. Every reading ran beside a control that reproduced exactly, and every
measured file was `cmp`-tied to its committed blob. The measurement caught something no gate could: the
merge alone put `CLAUDE.md` 4 tokens over its ceiling while `context_budget.py` said ok. P4 repaid that
and 6 more, and kept the runner 7 tokens inside its limit. I computed P5's problem instead of passing
the plan's port command along: 34 files where BL-57 owns 16. **Minus:** I read two doubled files directly before
noticing that the Read now returns a page instead of refusing, and spent ~50,000 tokens of context. A
one-line test, or a subagent from the start, would have cost nothing. `ITERATIVE_METHODOLOGY.md` grew
45 B against the plan's *"byte-neutral wording"*. I
hit `rev-parse --short` with two refs again, and a zsh `=` expansion. **Reduction:** nothing was removed
from a mandated-read file. The runner is 7 tokens larger than at P4's start, still under `upstream/main`'s.
`CLAUDE.md` is 10 tokens smaller than the merge. `HANDOFFS.md` grew by this receipt.

**Predecessor (S172): 8/10.** Its item (2) was the deliverable and carried what P4 needed. It named the
one vocabulary item P4's scope left out, the root front matter's `[BL-<N>]`, which became part of
`83a12f0`. Its gotchas paid: *`grep -c` exits 1 on zero matches* read every DONE grep correctly, and the
untracked `.context-budget-history.jsonl` stayed in throwaway clones. Its header-reserve deadline was
computed, not guessed, and still holds. **Not 9, for two errors of its own.** (1) Its plan citations
were stale when it wrote them: P4 at `:514` and its criterion at `:544`, where `e50fd60` — the receipt's
own commit — has them at `:551` and `:575`. S172's amendment block had moved them, and the receipt kept
the older numbers. (2) It stated P4's criterion as *"doubled read ≤ 36,955"* without saying that the
event S169 made P4's trigger — #82 merging — would void that blob as a baseline. #82 merged six minutes
after S172's last commit (`c509190`, 17:59:51 UTC; merge 18:05:47 UTC). **ROI: positive.**

```handoff
session: S172
date: 2026-09-16
status: complete
self_score: 8
predecessor_score: 8
active_task: **BL-57's P3 IS DONE ON BRANCH `bl57/changelog-rules` — THREE COMMITS, NOT PUSHED — AND S169's AMENDMENT IS DISCHARGED: P3's AND P4's RUNNER CRITERIA ARE NOW WRITTEN IN TOKENS.** `[BL-<N>]` became `[BL-<id>]` and the one-line audit became the anchored, shard-reading, `git ls-files` form, in §The Action Ledger, the runner, the flight manual and the ledger hook; the `HANDOFFS.md` seed's bare glob (P2's carried bullet) went with it. **#82 was re-checked at Phase 0 and is still OPEN at `c84e7d96`,** so the merge-first amendment did not trigger and P3 ran on the branch as it stood.
what_was_done: **Branch `bl57/changelog-rules` (from `775ba238`), 4 commits, each with its own entry in the branch ledger:** `d771439` — `FRAMEWORK_APPARATUS.md` §The Action Ledger states the vocabulary as `[issue #<N>]` / `[BL-<id>]` / `[ad hoc]` and publishes the audit as `cat CHANGELOG.md $(git ls-files 'docs/archive/CHANGELOG-*.md') | grep -cE '^### …'`, with all three of its load-bearing properties stated in place; `e47ca14` — the runner's inline audit grep at `:39` becomes a link to that section, and `:278`, `:329`, `ITERATIVE_METHODOLOGY.md:294`, `.githooks/pre-commit:57` take `[BL-<id>]`; `cf20a3b` — the `HANDOFFS.md` seed enumerates its shards with `git ls-files`; `18962a9` — a **correction I caught in my own text at close-out**: §The Action Ledger attributed the *78 against 64* count to *"this framework's own ledger"*, and this tree's root ledger records no such comparison, so the sentence now leads with the mechanism and gives the figure as a measurement on the project it came from. **Fork `main`, 2 commits:** `cee2654` claim (carrying both Phase 0 instrument snapshots, so no `--no-verify` commit was owed) and `44a1e20` the record — the plan's S172 amendment, both restated criteria, and BL-57's backlog row. **THE MEASUREMENT CAME FIRST AND ITS INSTRUMENT WAS CHECKED FIRST:** both published controls reproduced EXACTLY — the runner doubled to **36,955** (18,477.5 tok) and the Phase 0 pair to **48,555** (24,277.5 tok). **`b82dcff`, `upstream/main` and P3's start are the SAME BLOB `c0550acd`** (`git rev-parse` on all three), so one measurement served P3's start criterion and P4's `b82dcff` baseline — and S169's recorded control *was* that number all along. **The restated criterion then failed my own first edit and I fixed the edit, not the rule:** link + id changes measured **+36 B but only +9 tokens**; after two duplicate clauses came out the runner ended **52,163 B / 18,463.5 tok — 32 B and 14 tokens UNDER its start**, pair 24,263.5 of 25,000.
next_steps: **(1) THE MAINTAINER REPLIED ON #82 — THIS IS THE RANKED ITEM AND IT ARRIVED AFTER CLOSE-OUT.** Comment `5701463025` (KJ5HST, 2026-09-16T17:09:39Z), saved verbatim to `docs/planning/pr82-maintainer-reply.md`. **He reproduced everything:** all seven sections of `pr82-review-repro.sh`, every exit code and dashboard line, all four token figures by the same doubled-file Read, and `--run` `9/9 pass · results 74c773523dab` — *"three-for-three"* on that hash. He takes our §1 rewording as the base for the PR description. **He then gives SIX corrections and TWO further findings of his own class, and says *"Fixes next, in the order above."*** Four corrections say specific claims of ours were wrong — read them first and check each before relying on any of our text again: (1) fix 1 alone DOES refuse an ordinary `git rm`, so `find_root` is a prerequisite, not a sibling; (2) the dashboard fix is unreachable while the manifest is absent, so the walk must key on `git log`, and "compare against HEAD" should be "against the newest *parseable* committed version"; (3) our one-passing-offsets-one-failing claim holds only at the tests.sh-check level; (4) the gate-run comparison IS specified in the distributed seed — what is missing is the runner's Phase 0 carrying it. **⚠ #82's HEAD HAS MOVED, `c84e7d96` → `5c9d3b40`**, so every finding we pinned is stale until re-run; `upstream/main` has moved to `0fd003a`. **ANY REPLY IS AN OUTWARD ACTION AND NEEDS THE OPERATOR'S EXPLICIT GO-AHEAD, EVERY TIME.** **(2) BL-57's P4** (`docs/planning/changelog-rules-contradictions-plan.md:514`), the plan's next phase and the deliverable if the operator does not redirect to #82: entry lifecycle and the words (C3, C7, C8, C11, C13), at least three commits, size criterion now in tokens — doubled read ≤ 36,955. Branch `bl57/changelog-rules` at `18962a9`, worktree `../methodology-bl57`, clean. It inherits one item its scope does not name: the last live `[BL-<N>]` is in the branch's root `CHANGELOG.md` front-matter tag list. **(3) THE `HANDOFFS.md` FRONT-MATTER CUT HAS A DEADLINE, NOT A PREFERENCE** (BL-59). The header reserve is 7,028 of 7,168 B — **140 B, one trim-and-fold row**. With the trigger at "above 2" the next trim lands at **S175's Phase 0** (S173 closes at 2 receipts, S174 at 3), so the cut must land in S173 or S174. Folding the archive table into its own shard index is the identified cut. **(4) EVERY TRIM FROM NOW ON REPORTS `FRONTMATTER_FIELD_ABSENT`** — expected, stated, not a failure; S172 deliberately removed the hand-maintained receipt count the trimmer declares. Dropping the declaration is distributed and its own go-ahead. **(5) BL-60** — 31 proof scripts, 453,689 B, 5.4% of the tracked repo, 97.9% duplicate; three shapes costed, none chosen, and any fix is distributed. **CARRIED, EACH ITS OWN GO-AHEAD:** **`origin` holds the branch at `775ba238` (P2's head) — P3's four commits exist ONLY in the local worktree**; pushing fork `main` (count with `git rev-list --count origin/main..main`); F5/F6 (`docs/planning/pr80-review-response.md:243`); the fork resync; BL-53; BL-54; BL-36; `choose_cut`.

key_files: On the branch at `18962a9`: `FRAMEWORK_APPARATUS.md:355` (the vocabulary), `:370` (the audit command), `:374` (why each of its three properties is there); `starter-kit/SESSION_RUNNER.md:39` (the link that replaced the grep), `:278` (Phase 3F), `:329` (failure mode #27); `ITERATIVE_METHODOLOGY.md:294`; `.githooks/pre-commit:57`; `starter-kit/HANDOFFS.md:118` (the shard enumeration). On fork `main` at `44a1e20`: `docs/planning/changelog-rules-contradictions-plan.md:508` (P3's criterion, now in tokens), `:544` (P4's), the S172 amendment block above §0, `docs/planning/BACKLOG.md:152` (BL-57's row).
gotchas: **(1) THE TOKEN INSTRUMENT HAS A PRECONDITION NOBODY WROTE DOWN: THE MULTIPLE MUST CROSS 25,000 TOKENS, OR THE READ SUCCEEDS AND YOU GET THE FILE INSTEAD OF A COUNT.** I doubled `SAFEGUARDS.md` (16,353 B) and the Read returned all 492 lines — about 12,000 tokens of context spent for nothing. Sextupling it refused at 34,805, so the file is ≈5,800.8 tokens. Check `bytes / 2.8 > 25,000` before building the concatenation. **(2) A CRITERION RESTATED INTO A NEW UNIT STILL HAS TO BE MEASURED AGAINST THE WORK** — my first edit passed nothing: +9 tokens over a criterion I had just rewritten. The session that restates a gate is grading its own paper; restate first, edit second, and let the measurement fail you. **(3) `grep -c` AND `grep -F` EXIT 1 ON ZERO MATCHES** — P3's DONE check is *"prints nothing"*, so **exit 1 is the PASS**. Read the exit code against what the check means. **(4) `python3 starter-kit/context_budget.py --status` LEAVES AN UNTRACKED `.context-budget-history.jsonl` IN AN UPSTREAM TREE** — upstream neither tracks nor ignores it, where fork `main` tracks it; delete it after measuring or the next Phase 0 finds a dirty worktree. **(5) NOTHING MECHANICAL CHECKS WHERE A MEASURED NUMBER CAME FROM** — the *78 against 64* attribution passed every gate and was caught only by grepping this tree for the figure's provenance. **`bin/check-links` STRIPS THE ANCHOR AND CHECKS FILE EXISTENCE ONLY** (`bin/check-links:104`), so it did not verify `#the-action-ledger`; that was checked by hand against `FRAMEWORK_APPARATUS.md:338`. **(6) FORK `main` AND `upstream/main` DISAGREE ABOUT BUDGETING THE TWO LEDGERS** — #80's F3 moved them into `_deliberate_exclusions` upstream; fork `main` still budgets both, which is why `HANDOFFS.md` reads red here and not on the branch.
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `bash bin/tests.sh`,** run in `--no-local` clones whose HEAD sha was asserted equal to the source tree's before anything was measured, exit codes read bare. **Branch, at `cf20a3b` and again at `18962a9` (HEAD sha asserted both sides each time):** `bin/tests.sh` exit 0, **118 passed / 0 failed** — identical to S168's control; `bin/check-links` exit 0, **108** links across 23 files, against **107** measured at `775ba23` in the same clone, so the delta is exactly the one link P3 added; `context_budget.py --status` exit 0; `grep -F '[BL-<N>]'` over all seven files exits 1. **Fork `main`, at `44a1e20` (asserted both sides):** `bin/tests.sh` exit 0, **305 passed / 0 failed / 0 skipped** — identical to S169's, S170's and S171's controls; `check-links` 0 (105 links, 23 files), `check-learnings` 0 (65 rows), `check-handoff --all --allow-pending` 0 (7 receipts). `context_budget.py --status` exits 2, **diffed against the Phase 0 reading: 0 status flips**, three rows moved and all three by this session's own writes (`HANDOFFS.md` +1,314 tok from the claim stub, `BACKLOG.md` +33 B, growth run 128→129). **DONE criteria run, not predicted:** `grep -F '[BL-<N>]'` over the runner, the flight manual, `HOW_TO_USE.md`, the hook, §The Action Ledger and both seeds exits 1 (no matches); the audit returns the same number in zsh and bash on the branch (57 = its heading count), on this repo (556) and on all six adopters; in a throwaway repository with one entry and no shard the bare glob prints **0 under zsh and 1 under bash** while the `git ls-files` form prints 1 and exits 0 in both. **EXERCISED AFTER CLOSE-OUT, NOT AT IT:** the `HANDOFFS.md` retention trim — see item (2) and `1ec509d`. **NOT EXERCISED:** any push; P4; any reply from the maintainer; the six adopters' own suites (their ledgers were read, not written); CI (there is none); a second reader of P3's text.
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


