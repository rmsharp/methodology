# Changelog — Authoritative Action Ledger

The cumulative, append-only record of **actions taken in this repository** — across backlog
items, repository issues, and ad-hoc work. It is the authoritative answer to *"what was done
here, ever?"*, distinct from the release narrative in [`CLAUDE.md` §Versioning](CLAUDE.md#versioning).

This repository dogfoods its own methodology: every session records its actions here at
close-out (`starter-kit/SESSION_RUNNER.md` Phase 3F), and Phase 0 reconciles the ledger against
`git log` and backfills anything a crashed or out-of-band session missed. Taking an action — any
commit, or any non-commit action (release, tag, PR, upstream issue close, access grant, grooming
decision) — and not recording it is failure mode #27. The full close-out and reconcile rules, plus
the reusable seed, live in [`starter-kit/CHANGELOG.md`](starter-kit/CHANGELOG.md).

**Source tag — exactly one per entry.** This enumerates every logged action across the live file
and its archives, and proves all three sources landed:

```
grep -hE '^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[(issue #[0-9]+|BL-[0-9]+|ad hoc)\]' \
  CHANGELOG.md docs/archive/CHANGELOG-*.md | wc -l
```

It is anchored to the entry heading, and it reads the archives, for two separate reasons. The
unanchored single-file form published here before the v3.6 split returned **78** against 64 actions —
it also matched the three tag definitions just below and eleven in-prose mentions of a tag — and after
the split it would have stopped counting the archived entries at all.

- `[issue #<N>]` — a repository issue. Issues live in `KJ5HST/methodology`; the fork
  `rmsharp/methodology` has Issues disabled, so entries — authored from either side — cite an
  **absolute URL**, never a bare `#<N>`, and resolve identically from both.
- `[BL-<N>]` — a backlog item, removed from the backlog in the same commit. That backlog is
  [`docs/planning/BACKLOG.md`](https://github.com/rmsharp/methodology/blob/main/docs/planning/BACKLOG.md)
  on fork `main` only — **this repo has no `docs/planning/BACKLOG.md`** — so a `[BL-<N>]` entry here
  records work whose origin lives in the fork.
- `[ad hoc]` — work with no backlog or issue origin: releases, tag/branch ops, PR opens, upstream
  issue closes, access grants, and decline/wontfix/grooming decisions.

**Boundary vs. `CLAUDE.md` §Versioning — so the two ledgers cannot diverge.** §Versioning owns
*released-version semantics* (one narrated entry per shipped version); `README.md` §What's New is
its public restatement. This ledger is the *per-action operational timeline*, including
non-release work (housekeeping, doc-only PRs, adopter coordination, backlog grooming) that
otherwise has no home but raw `git log`. Where the two overlap — a release — this ledger carries a
**one-line pointer** into §Versioning, never a re-narration (cite, don't restate). §Versioning still
owns that semantics and still answers at the `CLAUDE.md#versioning` anchor every entry below cites;
as of BL-9 L3 its **narrated per-version list** lives one hop further on, in
[`docs/RELEASE_HISTORY.md`](docs/RELEASE_HISTORY.md), so the always-loaded `CLAUDE.md` stays lean.
The boundary itself is unchanged — the pointer moved, not the ownership.

Reverse-chronological, newest on top; prepend-only; grouped into `## YYYY-MM` sections. Prepend
under the topmost `## YYYY-MM`, and when the month changes open a new one above it. Entries stay at
`###`: never demote them beneath the month headings, because `_DATED_ENTRY_RE`
(`starter-kit/methodology_dashboard.py`) and `CHANGELOG_ENTRY_RE` (`bin/model-report`) both key on
exactly that level.

**Everything older than 2026-08-02 is archived, across two shards.** This file holds that day forward;
the preceding spans live in
[`docs/archive/CHANGELOG-through-2026-08-01.md`](docs/archive/CHANGELOG-through-2026-08-01.md)
(2026-07-27 → 2026-08-01) and
[`docs/archive/CHANGELOG-through-v3.6.md`](docs/archive/CHANGELOG-through-v3.6.md)
(2026-06-25 → 2026-07-26) — same format, same `## YYYY-MM` grouping, same newest-on-top order, frozen
at write. **The sections are the calendar; the file boundary is not.** The v3.6 shard was cut at a
release frontier, a cut nothing can ever be written back into. The 2026-08-01 shard was cut at a
**day**, because no release had shipped since v3.6 and the next calendar seam was measured and bought
5 entries; that shard's own front matter labels the departure and says when to prefer a release
again. Archiving is safe by construction: the FM #27 pre-commit gate matches the literal staged path
`CHANGELOG.md`, Phase 0 reconcile is frontier-based (`git log -1 --format=%H -- CHANGELOG.md`), the
dashboard's `_find_action_ledger` resolves the root file only, and `_find_changelog` scans only
`(<root>, <root>/docs)` — so no shard in `docs/archive/` can shadow this file by sort order.

**`bin/model-report` is the one consumer that loses coverage, and it loses more than it looks.** Its
Source 1 matches only the seed's list form `- **Model:**` (`bin/model-report:51`). This file's bullets
are all written in a bare `**Model:**` form it cannot parse, so **every bullet Source 1 could actually
see moved into the 2026-08-01 shard at this split** — run with no arguments it now reports an empty
Source 1 against a ledger whose entries visibly carry the bullet. Reach a span with
`bin/model-report --changelog <shard>`. The parser blindness is **not a consequence of this split**:
the form drifted at `1298af7` (2026-08-02) and has held unbroken since — *every* live entry, this
file's own newest included. Raised as **BL-20**, deliberately not fixed here (FM #17). The count that
stood here ("nine entries since") was falsified by the very next entry written above it, which is the
plan's own **DELETE** sink applied on the spot: the reader can count the list, and the command below
does it. Count both dialects,
never one — a single literal is a sample, not a population:

```sh
grep -cE '^-?[[:space:]]*\*\*Model:\*\*' CHANGELOG.md docs/archive/CHANGELOG-*.md
```

**When to archive again — a rate, not a level.** Archive when the headroom to the 2,000-line
`READ_CAP_LINES` proxy — the agent `Read` cap is denominated in **tokens**, and 2,000 lines is a
stand-in for it pending Phase B of
[`read-cap-premise-correction-plan.md`](docs/planning/read-cap-premise-correction-plan.md) —
divided by the observed growth per ledger *entry*, falls below **15 entries**; then cut
oldest-first until that ratio is back above **30**. Both are denominated in entries — the framework's
own unit — deliberately: commits-per-session is the most adopter-variable quantity in the system, so a
team committing 10× per session reads a 10× lower slope for identical growth, and the same file
crosses or clears the threshold depending only on which denominator you picked. Compute it; never
recall it:

```sh
split=$(git log --diff-filter=A -1 --format=%H -- 'docs/archive/CHANGELOG-*.md')
live=$(wc -l < CHANGELOG.md)
dl=$(( live - $(git show $split:CHANGELOG.md | wc -l) ))
de=$(( $(grep -c '^### ' CHANGELOG.md) - $(git show $split:CHANGELOG.md | grep -c '^### ') ))
if [ "$de" -gt 0 ] && [ "$dl" -gt 0 ]; then
  echo "$(( (2000 - live) * de / dl )) entries of headroom"
else
  echo "no slope yet — fewer than one entry written since the last split ($de entries, $dl lines)"
fi
```

It **abstains out loud** rather than printing a confident number it cannot support: immediately after
a split both deltas are zero, and against a superseded baseline they go negative. Either way you get
a sentence saying so, never a figure. That is the same discipline the numbers above are asking for.

A **level** was the previous rule, and it failed in the file next door: `HANDOFFS.md` states its
trigger as "approaches ~1,200 lines" and the archive actually fired at 997 — 203 lines early, with
nothing watching. A level is a hand-written derived value that decays silently; a rate re-derives
itself from the file every time it is read. This file crossed the cap once already, at 2,090 lines,
and its ten oldest entries were not reaching a reader who read it whole. **That was recorded here
as *silent* dropping, and that word was wrong** — truncation is announced, with a `PARTIAL view`
banner naming the true length; what was silent was that **nothing in the repo was checking**, so
the overrun was found by accident. Re-measured since, the file was 186,704 B — roughly 2.8–3.1×
the token cap — so it had been truncating well before it reached 2,090 lines: the incident dates
when the problem was *noticed*, not when it began.

**Reconcile-on-read entries below — the compact form, and the method stated once.** Each
`[ad hoc] Reconcile-on-read` entry records one Phase 0 discharge of BL-14's shipped half
(`starter-kit/SESSION_RUNNER.md:39`/`:42`): the predecessor session's `HANDOFFS.md` receipt shipped
with `commit: pending`, and the very next session named the real sha, always before its own Phase 1B
claim unless the entry says otherwise. **The derivation method is identical in every entry below and
is stated here, once, not per entry:** the target sha is the first commit — walking
`git log --all --full-history -- HANDOFFS.md` (all refs), read with `bin/check-handoff`'s own
`extract_blocks`/`parse_block` — whose named session's block reads `status: complete`; the claim stub
is the analogous first commit reading `status: pending`; the two are always distinct commits (S29's
gotcha 3, true in every case below); `git rev-list --count --no-merges <target-sha>..HEAD`, taken at
the time of reconcile, is `0` unless an entry says otherwise (no ghost session, no backfill owed).
**Precedents are not restated per entry** — in this prepend-ordered file, every Reconcile-on-read
heading *below* a given entry already is that entry's precedent list; nothing is lost by not
repeating it. The ordinal is reproducible, not incremented on faith:

```sh
grep -cE '^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[ad hoc\] Reconcile-on-read' CHANGELOG.md docs/archive/CHANGELOG-*.md
```

counts every discharge below plus the one bulk repair; subtract the repair to get the discharge
ordinal. **Each entry below states only what the method above cannot supply:** the two shas, whether
the order was taken before or after the discharging session's own claim, and any adjudication or
measurement unique to that reconcile (a two-answer derivation, a frontier disagreement, a G2/SRF
reading). Nothing quantitative recurs on purpose — the `HANDOFFS.md` SRF/byte-size series that runs
through several entries is the same kind of point-in-time reading the paragraph above already asks
you to re-run, never recall. **This is the norm new entries must stay inside** — `bin/tests.sh`
Test 29 fails a new discharge entry whose body exceeds a fixed line budget, so this cannot silently
erode back into prose the way it did before this compaction. The before/after figures for that
compaction are recorded in the action ledger entry below that performed it, not restated here.

**Archived 10 record(s), 2026-08-02 → 2026-08-02** into [`docs/archive/CHANGELOG-through-2026-08-02.md`](docs/archive/CHANGELOG-through-2026-08-02.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-08-02.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-02.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.1.1.

**Archived 70 record(s), 2026-08-03 → 2026-08-09** into [`docs/archive/CHANGELOG-through-2026-08-09.md`](docs/archive/CHANGELOG-through-2026-08-09.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-08-09.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-09.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.1.1.

**Archived 68 record(s), 2026-08-02 → 2026-08-11** into [`docs/archive/CHANGELOG-through-2026-08-11.md`](docs/archive/CHANGELOG-through-2026-08-11.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-08-11.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-11.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.1.3.

**Archived 28 record(s), 2026-08-12 → 2026-08-15** into [`docs/archive/CHANGELOG-through-2026-08-15.md`](docs/archive/CHANGELOG-through-2026-08-15.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-08-15.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-15.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.2.0.

**Archived 26 record(s), 2026-08-15 → 2026-08-17** into [`docs/archive/CHANGELOG-through-2026-08-17.md`](docs/archive/CHANGELOG-through-2026-08-17.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-08-17.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-17.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.3.0.

**Archived 23 record(s), 2026-08-18 → 2026-08-24** into [`docs/archive/CHANGELOG-through-2026-08-24.md`](docs/archive/CHANGELOG-through-2026-08-24.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-08-24.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-24.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.3.0.

**Archived 12 record(s), 2026-08-25 → 2026-08-25** into [`docs/archive/CHANGELOG-through-2026-08-25.md`](docs/archive/CHANGELOG-through-2026-08-25.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-08-25.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-25.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.3.0.

---

## 2026-08

### 2026-08-30 · [ad hoc] S126 close-out — record-budget Phase 3 measured, recommendation DO NOT REDUCE

**Phase 3D/3F.** Deliverable: the gate measurement, appended inline to
[`record-budget-reduction-plan.md`](docs/planning/record-budget-reduction-plan.md) §6 Phase 3
(`:325-437`), following S109's Phase 2 precedent — **no new `docs/planning/` file**, in a session
about file growth. Two commits: `1501783` (claim) + the deliverable + this close-out.

**THE PHASE'S `Do` CLAUSE, ANSWERED: THE FENCED FIELDS DO NOT COMPRESS.** Deflate-9 on the fenced
block, n=132 receipts, **0.484**, against size-matched controls cut from this repo's own prose —
`ITERATIVE_METHODOLOGY.md` 0.435, `SESSION_RUNNER.md` 0.448, `README.md` 0.445. **Receipts are
measurably less redundant than the documentation this framework ships.** Named removable slack in
the six: 3.03% markup + 2.41% cross-record boilerplate + 0.00% cross-field overlap ≈ **1–3%**,
against **16.7%** (10,240) and **33.3%** (8,192). §4.2 made this the condition — *"Revisit only
after measuring whether fields compress"* — and it is not met.

**RECOMMENDATION: do not reduce `RECORD_BUDGET_BYTES`.** The whole benefit available is **one
session** (breach moves S128 → S129), invariant across every utilization estimator 89.2%–100%.

**A NEGATIVE RESULT DELIVERED HONESTLY.** A frozen draft was attacked by six independent read-only
lenses; **all six returned PARTIALLY_REFUTED** and their corrections were verified against the source
and adopted. They overturned the cohort boundary (S105 wrote under 18,432, not 12,288 — its receipt
completed 45 min before `6ebe84d`), the "~94.6% utilization across two regimes" law (really 89.2%
and 95.7%), the −24.1% figure (**−18.6%** corrected), the confound's sign (**−4.5%**, not +1.1%), the
"sharp step at S98" in the 3A scores (a **smooth** 8.25→7.75 drift, no discontinuity), a citation
(`check-handoff:632-640`'s *"10,920–13,019 B"* is S103/S104, written by the cut commit itself), an
invented 11,264 B candidate, a `check-handoff --all` result that exists on no tree, and a
cross-check that was **self-confirmation** (record extents and file deltas agree to 0.1 B because
they are the same measurement). **The recommendation is the only part of the first draft that
survived unchanged.**

**NOT DONE, each deliberately.** No constant changed — §9 reserves the number for the operator and
Phase 3 asks for a recommendation, not a reduction. No historical receipt or shard edited
(prepend-only; §7 risk 4). `methodology_trim.py`, the 65,536 B ceiling, Test 34's floor and every
distributed file untouched. `bin/tests.sh` deliberately not re-run — this phase scopes it *"only if a
constant actually changes"*. **NO OUTWARD-FACING ACTION.**

**Model:** Claude Opus 5 (1M context).

### 2026-08-30 · [ad hoc] S126 — claim: Phase 3 of the record-budget plan, the gate measurement

**Phase 1B claim.** The operator selected
[`record-budget-reduction-plan.md`](docs/planning/record-budget-reduction-plan.md) **Phase 3**
(`:289-326`) from four options put at Phase 0. Phase 3 is the only one of the three phases never
started, and its gate measurement has never been run — three receipts say so, and
`git log --all -- docs/planning/record-budget-reduction-plan.md` returns exactly three commits
(`a3242ff`, `6ebe84d`, `eec1cbb`), none after 2026-08-25.

**The deliverable is a measurement and a recommendation — explicitly NOT a constant change.** The
plan says so twice: *"a measurement, and a recommendation — **not** a further reduction taken on
assumption"*, under a **Gate: do not reduce below the measured fenced-field maximum.** §9 already
establishes that the number itself is the operator's to ratify, so a session that lowered
`RECORD_BUDGET_BYTES` on its own findings would be taking a decision this plan reserves.

**Why it was selected, stated as arithmetic rather than as a preference.** `HANDOFFS.md` is
**229,270 B** against `READ_REFUSE_BYTES` **262,144 B** — **32,874 B**, and at the measured
**11,475 B/session** (n=8, close-out to close-out) the hard refusal lands on **S128's close-out**.
The only automated remedy — archiving — is refused (`SRF 8.3447` against `SRF_RED 1.00`) and that
refusal is a standing adjudication (S112, S124, BL-52). The rate cut is what the record prescribes
instead, and it does not exist. This session measures whether it can.

**The surface figure in the plan is stale and is re-derived here.** Phase 3 names *"the full
111-receipt population"*; the population today is **132 receipts** across `HANDOFFS.md` (19) and ten
`docs/archive/HANDOFFS*.md` shards. The recommendation rests on 132, not on the 19 survivors — a
figure drawn from the survivors alone is drawn from whatever the last trim happened to retain.

**What this session will NOT do:** change `RECORD_BUDGET_BYTES` or any other constant; edit any
historical receipt or shard (prepend-only, and §7 risk 4 says the old number is correct as written in
every site that states it); touch `methodology_trim.py`, the 65,536 B ceiling, Test 34's floor, or
anything distributed. **NO OUTWARD-FACING ACTION.**

**Control at this claim, run bare with `$?` read on the next line:** `bin/tests.sh`
**287 passed / 2 failed / 0 skipped**, both failures pre-existing and named (Test 9's `--source=github`
404 — two of 26 distributed files still 404 upstream; Test 18's two `TestS38TrimTriggerRow`
assertions, bisected this session to `ccfbe1c`, the commit at which `HANDOFFS.md` crossed
`CLASS_A_FIRE_BYTES`). All four checkers exit 0. `context_budget.py` exits **2** (BREACH), expected.

**Ledger:** `CHANGELOG: pending` — set at claim; superseded by this session's close-out entry.

### 2026-08-29 · [ad hoc] S125 close-out — the three misplaced 3A/3B prose blocks restored, self-score 8/10

**Phase 3D/3F.** Receipt in [`HANDOFFS.md`](HANDOFFS.md), `status: complete`, **12,150 B against the
12,288 B per-record budget, 138 B spare** — measured by running `bin/check-handoff`, which refused the first draft at
13,104 B and named the remedy ("cut the trailing prose first"). Four trim passes, which is one more than
the discipline this repo already records.

**Result.** `bash bin/tests.sh` **287 passed / 2 failed / 0 skipped**, against a pre-change control of
**286 / 3 / 0**; row-for-row over 289 rows each side, **0 status flips, 0 skips**, and all 14 changed
rows are the same assertions carrying a derived number the change moved. Every checker exits 0;
`context_budget.py` exits 2 as expected per S113 (d). **18 of 19 records now carry prose in their own
slot with 0 mismatches** — the exception is S107, whose prose was never authored.

**The half-fix, and what caught it.** The first pass moved three prose blocks and left two lines of a
four-part block behind, where they read as S118's metadata. An adversarial pass (7 claims, 10 read-only
agents; 4 held, 3 refuted, 0 refutations overturned) found it; `git blame` — one command, never run
until an agent ran it — settles the ownership. **A refutation is a claim too, so each of the three was
re-verified by hand before any of them changed the deliverable.** The one that did was worth the whole
exercise: `bin/model-report` had been filing S117's model self-report under S118.

**Corrections this session owes.** (1) The front-matter figures published in the claim entry above,
**9,040 → 6,361 B**, are in a unit `fmbytes39` does not use; it counts the terminating newline, so the
figures are **9,041 → 6,362 B**. The suite printed the right number before the wrong one was written.
(2) **`bin/tests.sh` does not mutate the live ledger** — `mutate()` reads `src` and writes a separate
`dst`, and no call passes `$LEDGER` as a destination. That claim was inherited from S107's receipt and
repeated unchecked in this session's own claim stub.

**Carried forward.** The `READ_REFUSE_BYTES` clock is **3.8 sessions** before this receipt (220,586 B
against 262,144 B, mean growth 11,082 B over the last five) and shortens every session — **re-derive it,
never quote it.** Two records (S119, S117) now read over the per-record budget; that is **revealed, not
created**, and receipts are prepend-only, so it is not to be "fixed" by editing them. Three pre-existing
prose gaps were found and deliberately not fixed (FM #17): S116's missing self-assessment, S107's
unjustified `predecessor_score: 9`, and an S104 score contradiction inside a frozen archive shard. The
governing rule is **fork-only** — absent from `upstream/main`'s stale seed — which is a real contribution
gap needing the operator's go-ahead. **NO OUTWARD-FACING ACTION.**

### 2026-08-29 · [ad hoc] S125 — the three misplaced Phase 3A/3B prose blocks restored to their own records

**Deliverable:** a pure relocation inside [`HANDOFFS.md`](HANDOFFS.md). **Zero bytes authored, zero text
reworded, one file.** The governing rule is [`starter-kit/HANDOFFS.md:128-130`](starter-kit/HANDOFFS.md):
*"A record is a `handoff` block **plus the prose beneath it**, not the fence alone. The self-score and
predecessor-score paragraphs sit outside the fence and belong to the receipt **above** them."*

**What moved.** S119's prose (stranded in the front matter above every fence) → S119's slot; the prose
occupying S119's slot, which is **S118's**, → S118's slot; the prose occupying S118's slot, which is
**S117's**, → S117's slot, which was empty. A closed three-cycle. Provenance rather than inference:
`git log -S` returns `2b4dcc6` (S119), `f48d860` (S118), `9491cb6` (S117), and each of those three diffs
shows the same signature — the commit deleted the claim-stub comment sitting *above* its own fence,
wrote its prose there, and in the same diff flipped its own fence from `self_score: pending`. **The
misplacement is three consecutive close-outs caught in the act, and it stopped at S120.**

**The rotation was incomplete on the first pass, and an adversarial review caught it.** S117's close-out
added **four** contiguous parts above its fence — the stub comment, `Model: Claude Opus 5 (1M context).`,
and the two prose paragraphs. The first pass moved parts 3 and 4 and left parts 1 and 2 behind, where
they read as S118's metadata — plausible, because S118 was *also* re-aimed mid-session. `git blame`
settles it: both lines are `9491cb6`, and `git show f48d860` shows S118's close-out **deleted** its own
(differently worded) comment and wrote no `Model:` line. **The consequence was live:** `bin/model-report`
Source 2 filed S117's model self-report under S118, leaving S117 the only gap in the S108–S118 run. After
the second pass the attribution reads `S117 Model: …` and S118 correctly carries none.

**Losslessness, proved on four axes over the whole session** (`BEFORE` = `git show e6d8442:HANDOFFS.md`):
the multiset of non-blank lines is **identical** (653 = 653); non-blank content bytes are **219,854 on
both sides, delta 0**; the relative order of all **559 unmoved** non-blank lines is preserved exactly;
each moved block is contiguous and byte-identical. **The only authored change in the entire file is one
blank line** (79 → 80).

**Result — measured, not predicted.** `bash bin/tests.sh` **287 passed / 2 failed / 0 skipped**, against
a pre-change control of **286 / 3 / 0**. Row-for-row over both populations (289 rows each, both asserted
non-empty): **0 status flips, 0 skips, 7 rows lost and 7 gained — every one the same assertion carrying a
derived number the change legitimately moved** (receipt population 18 → 19 from this session's own claim;
front matter 9,041 → 6,362 B; the frozen over-budget scope control 1 → 3). The one real change is
`A2 truth VIOLATED` → **`A2 truth: live front matter 6362 B <= 7168 B reserve (88% used)`**. The two
remaining failures are named and pre-existing: Test 9 `github source dry-run` and Test 18 dashboard unit
tests (onset `ccfbe1c`); neither is touched by this change.

**Stated in the unit the tool measures, correcting this session's own claim entry.** `fmbytes39`
(`bin/tests.sh:3047`) computes `len(t[:m.start()])` against the first `^```handoff$`, so the measured
prefix **includes the newline terminating the last front-matter line**: the figures are **9,041 → 6,362 B**,
not the 9,040 → 6,361 published at claim. 806 B of headroom, so the off-by-one is not decision-changing —
but it was wrong, and the claim entry above it stands uncorrected by design (prepend-only).

**The cost, stated rather than left to be discovered.** Measured with `check-handoff`'s own
`record_extents`: S119 **12,281 → 12,462 B** and S117 **10,828 → 13,805 B** now exceed the
`RECORD_BUDGET_BYTES = 12288` (`bin/check-handoff:665`); S118 falls to 11,778 B. **The rotation reveals
this breach rather than creating it.** Replaying the gate on the three historical trees with the
checker's own `scan()` + `record_extents()`, the newest-record extent it measured was S117 10,828 B,
S118 11,831 B, S119 12,281 B — all under budget, **all passing precisely because each had filed its prose
outside its own fence.** Two of the three receipts never actually fit the budget. Nothing reddens:
`check_record_budget` (`:711`) scores `extents[0]` only and only when unwritten, deliberately — the
docstring's reason is that a whole-ledger budget "would be permanently red against records nobody may
touch". `bin/tests.sh` does report the count, as `3 record(s) over budget … exempt as frozen`, on a
fixture whose builder self-arms one record.

**Blast radius: none.** Parsed by column, root `HANDOFFS.md` is a manifest **DEST** (`bin/_manifest.py`,
from the `starter-kit/HANDOFFS.md` **SEED** row) and **never a SOURCE** — `bin/sync` installs the seed, not
this file, so no adopter receives the rotation. Only `HANDOFFS.md` was modified. **NO OUTWARD-FACING ACTION.**

### 2026-08-29 · [ad hoc] S125 — claim: restore the three misplaced Phase 3A/3B prose blocks in `HANDOFFS.md`

**Phase 1B claim.** The operator selected this over S124's `next_steps` **(b)**, which named the same
defect one third of its actual size. S124 found **2,678 B of S119's prose stranded in the front
matter** at `HANDOFFS.md:73-101` and prescribed relocating it below S119's block, to clear Test 39's
red `A2 truth VIOLATED` row. Re-derived at this claim, the defect is **three blocks, and S124's
minimal fix would have made one number worse.**

**The rule is distributed and explicit, so this is a repair and not a policy choice.**
[`starter-kit/HANDOFFS.md:129-130`](starter-kit/HANDOFFS.md) — a manifest SOURCE, so it reaches every
adopter — states: *"A record is a `handoff` block **plus the prose beneath it**, not the fence alone.
The self-score and predecessor-score paragraphs sit outside the fence and belong to the receipt
**above** them."* Matching each fence's `self_score` / `predecessor_score` against the prose actually
occupying its slot, **15 of 18 records agree**. The three that do not form a closed rotation:
S119's slot holds **S118's** prose (`Predecessor S117 … Self 7/10`, matching S118's `pred: 8` /
`self: 7`), S118's slot holds **S117's** (`Predecessor S116 … Self 8/10`), S117's slot is **empty** —
and the element missing from the cycle is exactly the stranded front-matter block.

**Provenance, not inference.** `git log -S` returns `2b4dcc6` (S119 close-out), `f48d860` (S118) and
`9491cb6` (S117); all three hunks land at line ~70, each replacing the claim-stub comment *above* its
own fence. S117's and S118's prose stayed adjacent to their records and are misattributed only;
S119's was orphaned when S120's prepend anchor landed below it, and has accreted into the front
matter ever since.

**Why the minimal fix is the worse one.** `bin/check-handoff` measures a record fence-to-**next**-fence.
S119's record is **12,280 B against the 12,288 B budget — 8 B of margin**. Inserting S119's prose
there while S118's prose still occupies the same extent takes it to ~14,959 B. The full rotation is
the only variant that does not inflate it.

**Scope: one file, pure relocation, zero bytes authored.** Expected: front matter **9,040 B → 6,361 B**
against a 7,168 B reserve, `bin/tests.sh` **286/3 → 287/2**. Control run at this claim, exit read bare:
**286 passed / 3 failed / 0 skipped**; all four checkers exit 0; `context_budget.py` exit 2
(`HANDOFFS.md` 217,119 B / ≈91,812 tok — expected, per S113 (d)). **NO OUTWARD-FACING ACTION.**

### 2026-08-29 · [ad hoc] S124 close-out — the `SRF_RED` refusal adjudicated, self-score 8/10

**Phase 3D/3F.** Receipt in [`HANDOFFS.md`](HANDOFFS.md), `status: complete`, measured at **11,414 B against the 12,288 B record budget before it was written** — 874 B spare, not resized after the fact. **Predecessor S123 scored 7/10:** its instruction to run `--check` rather than trust its numbers is what produced this session's finding, but its `next_steps` (c) called the trim *"the obvious next deliverable"* while a standing instruction not to trim this file on sight sat four receipts below in the ledger it was writing into — one grep away, and finding it was the whole job.

**`bash bin/tests.sh` was run — the first receipt in six to say so.** `TESTS_EXIT=1`, **286 passed / 3 failed / 0 skipped**, each failure attributed to its onset commit rather than lumped: Test 39's `A2 truth VIOLATED` (`2b4dcc6`, the stranded prose, red six sessions), Test 18's two dashboard failures (`ccfbe1c`, the trigger crossing), and the long-standing Test 9 upstream 404. `check-links` 88/22 exit 0; `check-handoff` exit 0 both modes — **blind to the stranded prose, which is the point**. `context_budget.py` exit 2, expected per S113 (d).

**Two method faults worth carrying.** A cross-document section reference needs its document named — the tool's *"see plan §3.3"* resolves to the campaign plan, not the design doc that also has a §3.3, and I shipped that error in my own claim (`5637383` corrects it). And **a subagent's quotation is a claim, not a quote**: a critic reported S113 as saying *"DO NOT TRIM HANDOFFS.md ON SIGHT … SRF_RED refuses; honour it"*; that string is nowhere in the tree. The finding was real, the quotation invented, and it nearly reached this ledger.

### 2026-08-29 · [ad hoc] S124 — the `SRF_RED` refusal adjudicated: the trim was already declined, and the adjudication expires in ~4.6 sessions

**Deliverable:** [`docs/planning/srf-red-refusal-adjudication.md`](docs/planning/srf-red-refusal-adjudication.md). **Verdict: the refusal STANDS, the trim must not be forced, and the reason is not the one the tool gives.** Nothing was trimmed or forced; `HANDOFFS.md` was touched only by this session's claim stub and close-out receipt.

**The question was already settled, twelve sessions ago, and the predecessor's brief did not cite it.** [`BACKLOG-DETAIL.md:1474`](docs/planning/BACKLOG-DETAIL.md) — BL-52's third addendum (S112) — reads *"BL-52 IS NOW ADJUDICATED FOR THIS REPO'S `HANDOFFS.md`, ON MEASUREMENT, AND THE ANSWER IS THAT THE TRIM BUYS NOTHING… the tool's refusal was right, and right for a STRONGER reason than the one it gave."* S113 `next_steps` (d) made it standing: *"OVER BOTH ITS CEILINGS BY ADJUDICATION, NOT NEGLECT — **do not trim it on sight**."* An **attributed** constraint with a dated warrant and a named record — not the unattributed kind Learning #48 exists to catch. S123 called the trim *"the obvious next deliverable"* and cited neither; this session's own claim inherited that framing before checking.

**The number the tool refuses on is outside its own domain, and this is new.** `git merge-base --is-ancestor 9038e40 0afe9d6` confirms the last trim **predates** Phase C2. So SRF's denominator (22,146 B removed under a **65,536 B** trigger) and its numerator (164,184 B regrown under a **196,608 B** trigger) come from opposite sides of a deliberate **3.00×** policy change. H3 exists to detect *"big again, on schedule, for the same reason"*; a 3× ceiling raise is not the same reason. **H3 documents one limit — undefined before a first archive — and needs a second: undefined across a trigger change.** This also refutes the decaying-mechanism reading: removals shrank (19→16→30→25→8→4→3→3→3→**2** records) because a tight trigger fired constantly.

**Executed rather than predicted.** A real trim in a scratch clone writes four files, leaves `HANDOFFS.md` at **91,796 B** — still **26,260 B over** the ceiling, `context_budget.py` still exit 2 — and is **net +17,788 B (1.152×)**. Across all ten archives, adjusted for two bundled commits: relief **1,304,337 B** vs additions **1,448,576 B** = **net +144,239 B**. Every trim is net-additive; the archive now holds **more bytes than the relief it bought**. A trim relocates bytes at a ~17.8 KB toll — a real service, but a transfer, never a saving.

**The settlement expires, and S112 named the trigger.** It bounded itself to *"this file, at this size"* and predicted **~16 sessions** to `READ_REFUSE_BYTES` (262,144 B, where a default read returns **zero content, front matter included**). Twelve sessions later the actual is **16.6**. Stated in the unit S121 ruled this must carry: **88,232 tokens against a 25,000-token ceiling, 22,620 tokens of headroom, 4,959 per session — ~4.6 sessions.** The remedy BL-52 named (the record budget) has never been built, and the failure mode has already occurred once: `docs/archive/HANDOFFS-through-2026-08-09.md` is 382,071 B, past the refusal.

**An independent defect, found while locating the insertion point and currently RED.** `HANDOFFS.md:73-101` holds **2,678 B** of S119's prose stranded above the first fence — S119's close-out (`2b4dcc6`) replaced its stub's HTML comment, which sat above the prepend anchor, so every session since inserts below it and the front matter has measured **exactly 9,041 B** across ten commits. **`bash bin/tests.sh` → exit 1, 286 passed / 3 failed**: `A2 truth VIOLATED: live front matter 9041 B exceeds the 7168 B header reserve by 1873`, red for six sessions. S121/S122 both recorded 287/2; the suite went **287/2 → 286/3** at `ccfbe1c`, S123's claim, the commit that measured the trigger flip and did not run the suite. Nothing is lost, no proof passed over it, and **no trim can ever remove it** — L2 pins the front matter.

**Method notes.** The H3 citation in this session's own claim was wrong and is corrected in `5637383` — H3 lives in `framework-context-cost-plan.md:246-247`, not the design doc, whose §3.3 is about `BACKLOG.md`. Manifest facts were parsed from the SOURCE column, never grepped by filename: `methodology_trim.py` **is** adopter-facing; `bin/check-handoff` — the one mechanism that actually caps a receipt — **is in neither column**, so no adopter has ever received it.

### 2026-08-29 · [ad hoc] S124 — claim: adjudicate the trimmer's SRF-RED refusal of the `HANDOFFS.md` trim

**Phase 1B claim.** The operator selected S123's `next_steps` **(c)** — but not as the mechanical chore that receipt described. S123 called the `HANDOFFS.md` trim *"the obvious next deliverable"* and said to run `--check` rather than trust its numbers. Both were run at this claim. `--check` **FIRES** (205,704 B against a 196,608 B Class A threshold, exit 1). A dry run at `--cut 3` **REFUSES**: exit 2, `SRF_RED` — *"the last archive has been entirely given back; archiving again resets the LEVEL and not the RATE."* The deliverable is **the adjudication of that refusal**, not the trim.

**Why a refusal is worth a session.** A refusal is a claim, and this one is boundary-dependent in a way the tool itself flags: SRF is **7.2806** against the most recent archive `9038e40`, but **0.4550** against H3's own largest-drop boundary `a46f2f9` — a **16× spread on one file**, where H3 — [`framework-context-cost-plan.md`](docs/planning/framework-context-cost-plan.md) §3.3, at `:246-247`, **not** the design doc, whose own §3.3 is about `BACKLOG.md` and contains no SRF text — states *"the largest single size drop in the file's history"*, and `starter-kit/methodology_trim.py:985` uses `events[-1]`, the most recent. The tool labels that choice a policy addition rather than a reading. One of the two boundaries governs; nothing on record says which, and the answer flips the verdict.

**Measured at this claim, and it is the fact that reframes the session.** All ten archive events were enumerated with their own pre/post sizes. `9038e40` removed **22,146 B** — the **smallest removal in the file's entire history**, against a maximum of 369,255 B (`a46f2f9`) and a run of 171,441 / 169,853 / 214,539 / 103,014 / 68,955 / 56,208 / 52,902 / 50,531. SRF divides regrowth by that removal, so the most recent boundary supplies the **smallest denominator ever recorded** and 7.2806 is substantially an artifact of it. **That does not vacate the refusal** — the removals are monotonically shrinking while the file returns to ~200 KB each cycle, which is the decay-rate claim with independent support.

**What must be established, none of it on record.** Which boundary governs, decided from the plan's provenance rather than by reading the sentence harder. What a trim would actually **deliver** — this ledger is newest-on-top and delivered as an ordered prefix, so what a one-read cap truncates is the OLDEST records, and archiving records nobody reads may free bytes that were never costing anything. What the remedy's **net** cost is: the `9038e40` trim freed 22,146 B and the same operation's shard and proof added more than it freed. And whether `--force` is warranted, or whether the correct remedy is not a trim at all.

**NOT IN SCOPE:** running the trim, `--force`, or any write to `HANDOFFS.md` beyond this claim and the close-out receipt; the `check-learnings:314-315` range misreport; the `cfg["classes"]` KeyError at `starter-kit/context_budget.py:1025`; the dashboard twins' *"budget"* wording; the 229→228 B floor correction; Tier 2 of the read-set PR plan (the operator's, at Phase 5); and **any outward-facing action whatsoever**.

**Ledger:** `CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in [`HANDOFFS.md`](HANDOFFS.md).

### 2026-08-29 · [ad hoc] S123 close-out — the port-branch blocker refuted, Phase 3C resumed

Operator selected S122's `next_steps` **(a)**. Self-score **8/10**; predecessor **S122 scored 8/10**. Commits `ccfbe1c` (claim) → **`136fb34`** (the adjudication) → **`dd6ee0f`** (Learning #48) → `1593cb5` (planning docs) → this close-out.

**THE DELIVERABLE REFUTED ITS OWN PREMISE.** The task was to cost three options. All three — plus two added here — defend a property nothing in the repository reads. S120 declined to append a Learning row on two grounds; S121 refuted the cap and upheld the second at `CHANGELOG.md:261` as *"correct, load-bearing, and unrefuted."* **Three independent measurements kill it, any one sufficient.** **(1) No consumer:** `grep` for the branch name and blob `b21854cc` across `bin/ tools/ .githooks/ starter-kit/ workstreams/` **exits 1**; all four mentions are prose; there is **no CI**; `bin/tests.sh` contains **zero** `git show`; and `30ddf26` is not an ancestor of `main`, so no `git log`-based classifier can see it. **(2) The named mechanism does not exist:** `bin/sync --source` is `local` (the working tree) or `github` (`KJ5HST/methodology`) — **never a local ref** — and the branch is unpushed; the file is **absent from `upstream/main` entirely**, so the port *adds* it. **(3) The property is already false:** classifying five real adopters exactly as `bin/sync` does, `--source=github` yields **7–8 MODIFIED tracked files each and exit 2, today**, before this decision and after it.

**WHERE THE CONFUSION CAME FROM — the finding that stops it recurring.** Phase 3C *does* carry a byte-identity rule, at [`starter-kit/SESSION_RUNNER.md`](starter-kit/SESSION_RUNNER.md)`:227` and mirrored in the disputed file's own front matter. It is correct and mechanically enforced — one `modified` TRACKED file aborts an adopter's entire sync. But it binds **adopter ↔ canonical**, not fork ↔ port. **Five sessions reasoned about "the byte-identity" without opening either copy of that sentence.** And the blocker's warrant was never evidence: *"six refutation lenses missed it; a critic found it"* is a fact about six lenses, promoted to a fact about the world, with no consumer ever named. `CLAUDE.md` already says *an unattributed blocker is a defect*; this one was attributed, and absence of disagreement was its whole warrant.

**WHAT THE HOLD COST, AND WHAT WAS BLOCKED.** **Four sessions, not two** — S120 abstained as well, and S123-as-scoped was the fourth. Precedent for the deferred debt: `b26bb63` wrote **4 rows for 5 owed sessions**. The value of the blocked artifact was attacked hardest and survived: over the whole working tree, excluding the announcing ledgers, **29 of 46 rows have a genuine non-ledger citer and 12 of 46 fire from code, tests or config**. S121's *"#46 has zero inbound citations and fired on nobody"* is true of **one** row and does not generalise.

**THE GATE HELD.** The adjudication was written and presented **before** any remedy; the operator ratified Tier 1 and deferred Tier 2; **only then** was Learning #48 appended. An adversarial lens argued the adjudication was itself a fourth abstention — the answer was to ask, not to act first and justify afterwards.

**WHAT SHIPPED.** **Learning #48** — *a blocker's warrant has to name a consumer; "nobody has refuted it" is an argument from absence wearing the clothes of a finding.* Measured **before** writing at 1,445 B against the 1,500 B budget. `starter-kit/FRAMEWORK_LEARNINGS.md` is a manifest **SOURCE** (`tracked`, verified on the source column), so it reaches every adopter who syncs; 56,673 → 58,119 B against a 73,728 B ceiling, `ok`. The three planning docs reach no adopter by any route.

**TIER 2 IS DEFERRED AND DELIBERATELY UNRANKED**, written into [`upstream-read-set-pr-plan.md`](docs/planning/upstream-read-set-pr-plan.md) §5 as two named line items: what table the port carries at Phase 5 (**freeze** the 46-row / **refresh** from `main` / **extraction only** — the 13,894 B 13-row blob `ed22ace` created, after which the PR would match its own title, since it currently carries 42,779 B, **75.5%**, that is not the extraction), and the rewrite of `30ddf26:CHANGELOG.md:92-93`, **a standing defect that ships upstream under every option including freeze**.

**FOUND, NOT FIXED (FM #17).** [`bin/check-learnings`](bin/check-learnings)`:314-315` prints `"contiguous 1..%d"` using `len(rows)` twice, so it reports **1..47** for a range it correctly validated as **1..48** — understating by `len(reserved)`. A session reading that line for the next number gets **47**, a duplicate; that is very likely the origin of the #47/#48 trap. Canonical-only, no adopter impact, one line. Also: the published **229 B** smallest-row floor is **228 B** — it counted the trailing newline against a gate that does not.

**⚠ `HANDOFFS.md` IS PAST THE TRIMMER'S BUDGET AND THE TRIGGER NOW FIRES** — measured, not predicted: the Phase 1B stub alone took it 194,369 → 196,768 B against 196,608 B, and `--check` flipped from *does not fire* to **FIRES**. That trim is the obvious next deliverable; re-run `--check` rather than trusting these figures, and pass `--cut 3` explicitly — it is a floor, not a default.

**TWO ERRORS RECORDED AGAINST MYSELF.** I reported `origin`/`upstream` divergence **backwards** in the Phase 0 report — *"0 ahead / 115 behind"* for a tree that is **115 ahead, 0 behind** — and the operator read it before I caught it; `git rev-list --left-right --count` does not label its columns. And **my own claim stub asserted the pre-commit hook would refuse and require `--no-verify`; it refused nothing.** I published a tool's behaviour without running it, in the claim for a session whose deliverable is that exact error.

**NO OUTWARD-FACING ACTION** — nothing pushed, no PR, no adopter repo written to, and `30ddf26` is untouched (still blob `b21854cc`; `main`'s is now `516c9a26`, and that divergence is accepted by design).

### 2026-08-29 · [ad hoc] S123 — claim: cost the three port-branch options and adjudicate

**Phase 1B claim.** The operator selected S122's `next_steps` **(a)**. Both [`phase3c-deadlock-adjudication.md`](docs/planning/phase3c-deadlock-adjudication.md) §6(4) and S122's receipt record the three options as **uncosted** — and that single omission has now cost **two consecutive sessions their Learning row**: S121 and S122 each appended none, each citing this decision. The deliverable is **the costing and an adjudication**, not the remedy.

**The finding under adjudication.** `HEAD:starter-kit/FRAMEWORK_LEARNINGS.md` and `port/framework-learnings-extraction:starter-kit/FRAMEWORK_LEARNINGS.md` carry the identical blob **`b21854cc`** (re-verified at this claim). Appending a Learning row to `main` breaks that identity with the unpushed, PR-ready port branch S120 cut from `upstream/main` (`512c2ed`) as the single commit `30ddf26` over 18 files. The three options on record: **(i)** append on both and keep them identical; **(ii)** hold Phase 3C until Phase 5 ships or is abandoned; **(iii)** accept divergence and re-run the port's end-to-end `bin/sync` check.

**What has to be established before any of them can be ranked, none of it on record.** Whether the byte-identity is **load-bearing or incidental** — does any test, checker, manifest row, or `bin/sync` path actually read it, or is it an artifact of how S120 happened to build the branch? What each option costs **per future session**, since option (ii) is the status quo and its cost is unbounded. And whether the three options **span the space** — a derived branch that is rebuilt at PR time would make divergence a non-event, and no record considers it.

**NOT IN SCOPE:** appending any Learning row (that is the remedy, and it waits on ratification), the `cfg["classes"]` KeyError at `starter-kit/context_budget.py:1025`, the dashboard *"budget"* wording, the live-artifact check, the `HANDOFFS.md` trim, and **any outward-facing action whatsoever**.

**Ledger:** `CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in [`HANDOFFS.md`](HANDOFFS.md).

### 2026-08-29 · [ad hoc] S122 close-out — the size ceiling denominated in tokens, gated by read class

Operator directive after S121's adjudication: *"express the limit in tokens instead of bytes."* Self-score **8/10**; predecessor **S121 scored 8/10**. Commits `99cedc0` (claim) → **`0d3e3a6` (RED)** → **`28a02a6` (GREEN)** → **`97c8066`** (configs) → this close-out. `starter-kit/context_budget.py` **1.1.0 → 1.2.0**, and it is **DISTRIBUTED**, so this reaches every adopter who syncs.

**THE DEFECT WAS SYSTEMIC, NOT SINGULAR.** S121 found one ceiling permitting an unreadable file. Metering all five showed **four of five** do: 65,536 B is **26,561 / 27,714 / 27,527 tokens** for the three ledgers at their real densities, and 73,728 B is **25,514**. Measured densities span **2.3648–2.8897 B/token**, so the config's single global `2.8` was wrong for four of the five — per-file measurement is the point, not a refinement. The method is trustworthy because the arithmetic **intercept came out exactly 5.0 on all five files**, across very different content.

**AND IT IS NOT CONFINED TO THIS REPO.** Read-only inspection of three real adopters found **five `read-mandated` files that exceed the read cap** — `chat_verification/SESSION_NOTES.md` (**29,739 tok**, metered) and `vscode_quarto_ext/CHANGELOG.md` (**30,311 tok**, metered), plus that repo's `HANDOFFS.md` and `BACKLOG.md` and `wsfct/SESSION_NOTES.md`. The protocol orders those files read; they cannot be read whole. **That is failure mode #28 detected in the wild for the first time.** Nothing in any adopter repo was touched — `SAFEGUARDS.md:38` governs; these are findings, not work.

**WHAT SHIPPED.** `READ_CAP_TOKENS`, `MIN_BYTES_PER_TOKEN`, `WHOLE_READ_CLASSES`, `DENSITY_DRIFT_WARN`; `file_density()` (per-file measured → config → floor, **returning its source**, so a derived number and a measured one never speak in the same voice); `token_ceiling()`; `config_defects()`, which **reports** a `max_tokens` above the cap rather than silently clamping it — a clamp fixes the symptom and leaves the operator believing a number that is not in force; and `ledger_dimension()` extended to report tokens when a token ceiling fires, in the function whose own docstring already argued the cap is token-denominated and bytes were the best available proxy.

**THE CLASS GATE IS THE LOAD-BEARING PART, AND IT WAS THE OPERATOR'S CHOICE** from three costed options. The cap binds a file read **whole**; a file read **in part** is not bound by it (Learning #34 — read whole once, in part 243 times). So `on-demand` files get **no token verdict at all**. Judging them would be a budget on the wrong unit, which is *"not conservative, it is unmeasured"* — the per-file-vs-per-row error this entire arc was about, committed in the opposite direction.

**ADOPTERS NEED DO NOTHING.** `bin/sync` overwrites the **tool** (`tracked`) but never the **config** (`seed`: *"never overwrite an existing file, even with `--force`"*), so an un-migrated config is the normal case, not an edge case. Every adopter entry inspected declares `max_bytes` alone; all of them gain the guard by derivation at the 2.27 floor, which **maximises** the token estimate and therefore can never certify an unreadable file as fine.

**BOTH ENFORCEMENT SITES MOVED TOGETHER.** `precommit()` gates on tokens too, keeping the relative rule so a commit that *shrinks* an over-budget file is never refused — the gate can never prevent its own remedy. A gate that reports in one unit and refuses in another is half a gate; that is the plan's own `KeyError`-at-both-sites lesson applied before it could bite.

**A WIRING GAP THE TESTS COULD NOT SEE.** `main()` called `measure_file` without `cfg`, so the new arm would have run at the floor and **silently discarded every per-file measured density** while 61 tests stayed green — the *measured-but-never-voted* shape. Fixed at `:1009`, and pinned by a test that fails if it regresses.

**VERIFICATION.** Red committed on its own, so red-before-green is checkable with `git show 0d3e3a6` rather than asserted: 15 failing assertions, the 42 pre-existing ones untouched. After: `tools/` **505 tests OK** (4 skipped), `test_context_budget.py` **61 OK**, tool `--selftest` **35 PASS / 0 FAIL**. **`bin/tests.sh` 287 passed / 2 failed / 0 skipped, exit 1 — identical to the S121 baseline with ZERO status flips across 283 shared assertion texts**; both failures pre-existing. **End to end at a fresh adopter, not merely unit-green:** a real `bin/sync --source local` into a scratch git repo, after which the shipped seed alone reports **`SESSION_NOTES.md ≈30,695 tok / 25,000 tok over`** for a file **under** its 120,000 B byte ceiling, while a 400,000 B `on-demand` file beside it reports in bytes and gets no token verdict. **The migration is 26 insertions, zero deletions, both configs still parse, and no verdict changed** (ok/over/over/ok/ok, exit 2 before and after) — the same limits in the honest unit, not new policy.

**NOT DONE, each deliberately.** **No Learning row appended** — `HEAD` and `port/framework-learnings-extraction` still carry the identical blob `b21854cc`, and that decision is the operator's, unchanged from S121. `cfg["classes"]` **KeyError reproduced live** at `starter-kit/context_budget.py:1025` and left alone — out of scope, already scheduled in the read-set plan's §3.4(d) beside `precommit()`'s one-byte undercount. The other two §6 items remain: the distributed dashboard twins still publish the 2.27 floor as a *"one-read **budget**"*, and there is still no check that reads the **live artifact** (Learning #38). **NO OUTWARD-FACING ACTION** — nothing pushed, no PR, no adopter repo written to.

**One error worth recording against myself.** I inverted the floor's direction and briefly published the five adopter findings on the anti-conservative basis; metering rescued two, and one had genuinely flipped to *under*. That is the **third** instance of this same bytes-versus-tokens confusion in two sessions, which is the argument that the countermeasure has to be mechanical rather than vigilance — and is precisely what this session shipped.

### 2026-08-29 · [ad hoc] S122 — claim: express the size ceiling in tokens instead of bytes

**Phase 1B claim.** Operator directive, given verbatim after S121's adjudication: *"express the limit in tokens instead of bytes."* It is the durable half of that document's §6(1) — lowering `73,728 → 69,632` was measured to break nothing, but a byte ceiling rots again at the next compaction, and only a token denomination does not.

**The defect being fixed.** `.context-budget.json` declares `max_bytes` only, and [`starter-kit/context_budget.py`](starter-kit/context_budget.py)`:122` enforces it with a bare byte comparison. So every ceiling silently encodes a bytes-per-token density fixed at the moment it was set. S121 measured the consequence: the declared 73,728 B ceiling for `starter-kit/FRAMEWORK_LEARNINGS.md` certifies `ok` a size that the read tool **refuses at 25,486 tokens**.

**⚠ DISTRIBUTED — this reaches the fleet.** `starter-kit/context_budget.py` is a manifest SOURCE with disposition `tracked`, verified on the SOURCE column rather than a bare-filename grep. Every adopter who runs `bin/sync` receives the change.

**⚠ THE DESIGN PROBLEM IS REAL AND IS SOLVED BEFORE ANY CODE IS WRITTEN.** This repo is Python-3-stdlib-only and cross-platform, so the script **cannot invoke the agent's tokenizer** and cannot measure tokens itself. A `max_tokens` evaluated as `bytes ÷ bytes_per_token` would merely **move the rot into the density field**. The design must make density an explicit, dated, re-derivable **input** whose staleness is visible, or it reproduces the defect it is fixing. The design is presented for approval before implementation — the file is distributed and the schema is public.

**NOT IN SCOPE:** the other three §6 items (the dashboard's *"budget"* wording, the live-artifact check, the port-branch decision), the `73,728` value itself, BL-44, BL-52, and **any outward-facing action whatsoever**.

**Ledger:** `CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in [`HANDOFFS.md`](HANDOFFS.md).

### 2026-08-29 · [ad hoc] S121 close-out — the Phase 3C deadlock adjudicated: not real, and the ceiling is inverted

**Session claimed 2026-08-28 and closed 2026-08-29**; the receipt in [`HANDOFFS.md`](HANDOFFS.md) keys on `S121` + **2026-08-28**, its claim date, so the two ledgers name the same session rather than drifting apart. Self-score **8/10**; predecessor **S120 scored 6/10**.

**Deliverable: [`docs/planning/phase3c-deadlock-adjudication.md`](docs/planning/phase3c-deadlock-adjudication.md)** (19,104 B), commits `43387e1` (1B claim) + **`4b7224e`** (the deliverable) + this close-out.

**VERDICT: S120's *"the framework's own mandatory close-out step cannot be performed against its own published budget"* is FALSE AS WRITTEN.** The arithmetic is right and the denominator is wrong. Four independent refutations, each handed to an agent instructed to break it; all six lenses returned SURVIVES_WITH_CORRECTION.

1. **Metered, the file is at 78.5% of one read.** Six collinear probe points with **zero residual** on the three the model never saw (5×/6×/7× predicted and actual 98,065 / 117,677 / 137,289). The concatenation seam was **measured at exactly zero tokens** across five one- and two-seam windows, so `f(n) = 19,612n + 5` gives `f(1) = 19,617 tok` as a **measurement, not an extrapolation**. Headroom **5,383 tokens**.
2. **56,750 B reaches this file through no code path.** `methodology_trim.py --check` → `[NO_CONFIG]`, exit 3; both dashboard twins' `read_cap_class()` → `None` for the canonical path *and* the adopter dest; `bin/check-learnings` has no whole-file arm. It is a **detector floor** (`MIN_BYTES_PER_TOKEN = 2.27`, the conservative end of a measured band), not a budget.
3. **Learning #34 — in this very table, at S97 — already moved the guard off the per-file axis:** read whole once, in part 243 times. The file's real published budget is **1,500 B per row**, and all 46 rows comply.
4. **BL-45 is the precedent:** S110–S114 ran through an identical declared deadlock and closed normally.

**THE REAL DEFECT RUNS THE OTHER WAY AND IT IS MEASURED, NOT MODELLED.** **73,646 B of this content — 82 B *under* the declared 73,728 B ceiling — is refused at 25,486 tokens** (a bare read returns a `PARTIAL view` banner delivering 106 of 128 lines). BL-45 deliberately set that ceiling **2,023 B under** the then-cliff, stating *"a ceiling must sit below where the file stops fitting, not on it."* S119's compaction lowered density **3.0444 → 2.8897** and inverted the margin. **A byte ceiling is `tokens × density`, and compaction is the operation that changes density — so it rots silently, and nothing goes red.** That is Learning #46's own mechanism, committed by the framework's most recent remedy.

**THE FINDING THAT ACTUALLY MATTERS — a quality tax, not a blocked append.** Whenever headroom falls below ~1,500 B, the row written **equals the headroom minus a few bytes**: #34 = 604 B at 604 B available, #38 = 981 at 997, #45 = 837 at 1,082, #46 = 229 at 245. The file has saturated against its ceiling **four times** (S97, S109, S118, S120). That also makes the 229 B row **circular evidence** — it is that small *because* it was squeezed. Before the extraction the all-time minimum was **419 B**, in a population (`SESSION_RUNNER.md`'s history) that S120's *"smallest it has ever carried"* never searched.

**SIX OF MY OWN NUMBERS WERE WRONG AND ARE CORRECTED IN PLACE, marked ⚠ in the document. Two repeat, one level down, the exact error the document faults S120 for.**

- **I converted token headroom to bytes at the WHOLE-FILE density (2.8897) when the headroom is consumed by ROWS**, which meter **3.1974 B/token** (measured: rows #39–#42 = 4,163 B / 1,302 tok). Every byte-denominated capacity figure I published — *"~11 rows"*, *"8–13 rows"* — was **low**. Corrected: **11.5–16.5 rows, and the only safe unit is tokens (5,383)**.
- **I withdrew a refutation I had already published to the operator.** *"The config refutes itself: 73,728 / 2.8 = 26,331 tok"* is **unsound** — `bytes_per_token` is explicitly declared non-comparable, being calibrated on opening context against `CLAUDE.md`. The sound proof is the direct read.
- **I put a fabricated quotation into the record** in claim `43387e1`: *"append a Learning row"* appears **nowhere** in the protocol; I quoted S120's paraphrase as if it were Phase 3C's own words.
- **The 63.6% append rate is bimodal, not a base rate** — 12/12, then 3/15 while the file sat 16 B under its ceiling, then 6/6. **When the file has room, essentially every session appends.**
- **S112 contributed zero rows** (I said three); the multi-row session is **S114**, with four.

**WHAT S120 GOT RIGHT.** It was applying **its own ratified plan's standard** — `upstream-read-set-pr-plan.md` sets 56,750 B as this file's acceptance standard at `:95`, `:106` and `:123`. **The defect is in the plan.** And **its second reason was correct, load-bearing, and unrefuted**: appending breaks the byte-identity that lets `bin/sync` agree from either source — `HEAD` and `port/framework-learnings-extraction` carry the **identical blob `b21854cc`**. Six refutation lenses missed it; a critic found it. **That, not the cap, is why this session appended no Learning row.**

**S119's COMPACTION MUST NOT BE REVERTED.** It had two authorising legs, and **leg 1 — the 1,500 B row budget — independently justifies every row it touched**: 20 real violators, the checker driven RED in its own commit (`28551a5`), and decisively, the 18-row option leaves #12 (1,451 B) and #13 (1,447 B) in breach, so **only** the 20-row option turns the checker green. Reverting restores 20 violations. Leg 2 — the file-level arithmetic — does not survive: the **pre-compaction** file metered **24,363 tok = 97.45% of one read**. It fit. Nothing was ever over.

**THE OPERATOR CHOSE ON A MIS-SCALED COLUMN.** `CHANGELOG.md`'s S119 decision table scored the options in a *"vs the 56,750 B one-read cap"* column, marking the 18-row option *"401 B OVER"* and the 20-row option *"571 B UNDER"*. At the true cliff for that content (~76,111 B) **both were ~19,000 B under** — mis-scaled by roughly 19 KB. The outcome is unchanged (leg 1 settles it), **but that is a finding the operator is entitled to be told, not one an agent may assume on his behalf.**

**NOT DONE, each deliberately.** No remedy applied — **the Present→Implement gate holds**, and §6 is an answer *proposed* to the open decisions **D4/D5** (`file-management-system-plan.md:287`, whose own heading says *"none is derivable from measurement"*), not a correction an agent may apply. No Learning row appended (see the port-branch reason above). No ceiling edited, no file compacted, retired or split. Phase 3/4/5 untouched — and **Phase 3 must not ship as specified**, since it would hard-wire 56,750 B into a gate. BL-44, BL-52 and the pre-existing `A2 truth VIOLATED` front-matter failure recorded, not fixed. **NO OUTWARD-FACING ACTION WHATSOEVER.**

**Build-equivalent, run against a control worktree at the pre-claim commit `a4c4420`:** control **287 passed / 2 failed / 0 skipped, exit 1**; live **identical**, with **zero status flips across 284 shared assertion texts**. The three differing rows pair exactly and are all this session's own receipt increment. **Both failures are pre-existing and neither is this session's** — the known Test 9 upstream-404, and `A2 truth VIOLATED` on a front matter that is **byte-identical at both commits**. `check-links` **0**, `check-learnings` **0**, `check-handoff` **0**, `context_budget.py` **2** (the adjudicated BL-52 breach, untouched).

### 2026-08-28 · [ad hoc] S121 — claim: adjudicate the Phase 3C deadlock

**Phase 1B claim.** Deliverable: **one adjudication document in `docs/planning/`** settling what to do about the finding S120 raised — that `starter-kit/FRAMEWORK_LEARNINGS.md` sits at **56,673 B with 77 B of headroom** under the 56,750 B one-read cap, while the smallest row the table has ever carried is **229 B**, so `starter-kit/SESSION_RUNNER.md:223` Phase 3C's mandatory *"append a Learning row"* step overshoots the cap by ≥152 B no matter how short the row is.

**The deliverable is a decision, not its execution.** The Present→Implement gate holds: nothing is compacted, retired, split, or re-ceilinged this session without the operator's ratification. Implementation, if ratified, is a separate session.

**The premise is itself a claim and is tested before any remedy is ranked.** S120 asserted three things in one breath, and they are separable: (1) that 56,750 B is the binding constraint on *this* file, (2) that Phase 3C's append is per-session mandatory for a canonical session, and (3) that 229 B is the correct floor for a new row. Each is checked against its own authority — the runner's own text, `bin/check-learnings:104`, and the table's measured row distribution — before the remedy set is ranked. A refusal is a claim to test, not an obstacle to route around.

**NOT IN SCOPE:** Phase 3 (the gate) and its two `starter-kit/context_budget.py` defects, Phase 4, Phase 5 (the PR — which needs the operator's explicit go-ahead), BL-44, BL-52, trimming either ledger, and **any outward-facing action whatsoever**.

**Ledger:** `CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in [`HANDOFFS.md`](HANDOFFS.md).

### 2026-08-28 · [ad hoc] S120 close-out — Phase 1 (the port) shipped, self-score 8/10, predecessor S119 scored 9/10

**Deliverable complete: Phase 1 of the upstream read-set PR plan.** The S34 learnings extraction is
ported onto **`port/framework-learnings-extraction`**, cut from **`upstream/main` (`512c2ed`)** — one
commit, **18 files, 352 insertions / 113 deletions**, local only. **No PR opened, nothing pushed.**

**What it delivers, measured on the branch and metered, not quoted.** Upstream's Phase 0 mandatory
read (`SESSION_RUNNER.md` + `SAFEGUARDS.md`) goes **80,526 → 67,581 B (−12,945, −16.1%)**, which
reproduces `ed22ace`'s own reported runner delta to the byte. **Metered by the plan's §7 doubled-file
method: 28,234 tok = 112.9% of one read → 23,902 tok = 95.6% — the mandatory read now FITS**, with
1,098 tokens spare. The upstream figure reproduces the plan's §2.1 measurement **exactly**. On the
deliberately conservative 56,750 B floor the pair is still over — 23,776 → **10,831 B, a 54.4% cut**
— and both numbers are reported because that floor's 2.27 B/token is ~26% conservative for this
content (metered: 2.852 and 2.827).

**Four of the plan's own figures were superseded, all favourably; §8 of the plan now records them.**
The plan predicted 69,749 B because it equated *"ported runner"* with *"the fork's runner"* — but the
fork's also carries issue #75's additions (+1,977 B) and the Phase 3F `Model:` bullet (+191 B),
**2,168 B this port does not take**. Its 45.3% became **54.4%**. And its §2.2 byte-identity claim is
now **11 of 13**: S119 compacted #12 and #13, so the port **replaces 1,076 B of text upstream can see
today** — disclosed rather than presented as purely additive. All nine load-bearing ideas of row #12
were checked present after compaction.

**Three scope facts the plan did not have, each found by reading.** (1) **Upstream already ships
`bin/check-learnings`**, pointed at `SESSION_RUNNER.md` — the plan never mentions it, and S119's
`next_steps` (c) reasoned from the premise that it does not exist. (2) The fork-vs-upstream runner
diff **is not the patch**; `ed22ace` itself touched **18 files**, of which 12 `git apply --check`
clean, four are fork-only ledgers that must not port (their failure is *correct*), and three needed
hand-porting. (3) `context_budget.py` lives in `starter-kit/`, not `bin/`.

**The whole checker had to go, and the file's own front matter is why.** It publishes *"1,500 B,
checked by `bin/check-learnings`"* and declares the `#14` reservation. Shipping the file without the
budget arm and the reserved-number handling would ship two false claims and report the deliberate
gap as a missing row — proved by running upstream's checker against the ported file: exit 1,
*"missing #14"*.

**Verification.** `bin/tests.sh` row-for-row against a **pristine `upstream/main` control in its own
worktree**: control **114 passed / 0 failed, exit 0**; branch **113 / 1, exit 1**. Both populations
114, **zero skips, zero status flips across 111 shared assertion texts**, and all six differing rows
pair exactly (`24 → 25` manifest counts twice, plus the one regression). **That regression is this
change's own precondition and self-resolves on merge** — Test 9 dry-runs `--source=github` and the
error names the cause: *"gh api failed for starter-kit/FRAMEWORK_LEARNINGS.md: 404"*. Do not weaken
Test 9. Also: `tools/test_methodology_dashboard.py` **211 passed**, and the new `CHECKLIST_EXEMPT`
entry was **driven RED first** — removed, it fails on exactly `['FRAMEWORK_LEARNINGS.md']`.
`check-learnings` **0**, `check-links` **0** (83/21 → **88/22**, matching `ed22ace`'s own figure),
`check-handoff` **0**, twins byte-identical, and a real `bin/sync` into a scratch adopter delivers
`FRAMEWORK_LEARNINGS.md` byte-identical to canonical.

**Two defects I introduced and caught, disclosed rather than quietly fixed.** I applied `ed22ace`'s
count edits where they applied cleanly — and *cleanly* is not *correctly*: its arithmetic was computed
on a 22-row `DISTRIBUTION` and upstream's is 24. `T8_keeping_current.md` shipped **"23 distributed
files"** and the dashboard test **"21 installed markdown files"**. My first sweep had corrected the
dashboard twins' four counts and missed these two, because it enumerated the constant and not its
derived neighbours. All **eight** count claims across four files are now derived from the manifest
and asserted: 8 correct, 0 wrong.

**PHASE 3C IS NOW UNSATISFIABLE, AND THAT IS THE MOST IMPORTANT THING THIS SESSION FOUND.**
`FRAMEWORK_LEARNINGS.md` is **56,673 B with 77 B of headroom** under the 56,750 B one-read cap. The
**smallest row the file has ever carried is 229 B**, so an append of any size overshoots by at least
152 B. The framework's own mandatory close-out step therefore cannot be performed against its own
published budget. **This session did not append a Learning row** — doing so would breach the cap and
break the byte-identity that lets `bin/sync` agree from either source. The learning is recorded in
the `HANDOFFS.md` receipt instead, and the collision is the next session's headline.

**Disclosed, deliberately unfixed:** seven backticked artifacts named inside the rows do not exist
upstream, across 10 of 46 rows, and **32 of 46 rows cite session numbers S35–S119** from a sequence
that runs separately from upstream's **and collides with it**. None is a broken hyperlink —
`bin/check-links` strips inline code spans, so its green says nothing about them. A clarifying
front-matter note would cost ~400 B against 77 B of headroom.

**NO OUTWARD-FACING ACTION.** Nothing pushed; the port branch exists on neither remote. `main` is
**447 ahead of `upstream/main`** (1 behind), 106 ahead of `origin/main`. Issue #75's PR remains
local-only and unsent.

### 2026-08-28 · [ad hoc] S120 — claim: Phase 1 of the read-set PR plan, the port

**Phase 1B claim.** Deliverable: **Phase 1 of [`docs/planning/upstream-read-set-pr-plan.md`](docs/planning/upstream-read-set-pr-plan.md)** — port the S34 learnings extraction (`ed22ace`) onto a branch cut from **`upstream/main` (`512c2ed`)**, carrying today's compacted `starter-kit/FRAMEWORK_LEARNINGS.md`, so upstream's Phase 0 mandatory read drops from **80,526 B to 69,749 B**.

**Re-derived at this claim, not quoted from the plan.** S119's `next_steps` (a) required both.

- **The three-section diff still holds to the byte.** `## Learnings (added by sessions)` **−12,980**, `## Phase 2: Execute` **+1,977**, `## Phase 3: Close Out` **+226** = **−10,777**, reconciling exactly to the file delta. Heading sets are symmetric-difference empty in both directions; `SAFEGUARDS.md` is the same blob (`f096419…`) on both sides.
- **The plan's byte-identity claim no longer holds, exactly as predicted.** §2.2 says upstream's 13 inline learnings are byte-for-byte the fork's rows #1–#13. Today it is **11/13**: S119 compacted **#12 (2,401 → 1,451 B)** and **#13 (1,573 → 1,447 B)**. The port therefore **replaces 1,076 B of text upstream can see today**, engaging the file's own *"append only; do not edit existing rows"* rule on exactly the two rows the plan predicted, and the PR body must disclose it rather than present the port as purely additive.

**Three corrections to the inherited scope, each found by reading rather than assuming.**

1. **`starter-kit/context_budget.py` is not in `bin/`.** The plan §3.4 and S119's `next_steps` (d) both cite it without a path.
2. **Upstream already has `bin/check-learnings`** — S119's `next_steps` (c) reasoned about the port on the premise it does not. Upstream's copy (247 lines) reads `starter-kit/SESSION_RUNNER.md`; the fork's (320 lines) reads `starter-kit/FRAMEWORK_LEARNINGS.md`. **The port must repoint it, or upstream ships a checker aimed at a table that is no longer there.**
3. **`git diff upstream/main HEAD -- starter-kit/SESSION_RUNNER.md` is NOT the port's patch.** It bundles three unrelated changes: the extraction, issue #75's *name the surface* additions (already prepared separately at [`docs/planning/issue75-upstream-pr.md`](docs/planning/issue75-upstream-pr.md)), and the Phase 3F `Model:` bullet. **The originating commit `ed22ace` touched 18 files**, including `README.md`, `HOW_TO_USE.md`, `ITERATIVE_METHODOLOGY.md`, `starter-kit/BOOTSTRAP.md`, `starter-kit/CLAUDE_TEMPLATE.md`, two tutorials and the dashboard twin — cross-references that dangle if they do not ship together.

**Also found at Phase 0, recorded rather than fixed.** `starter-kit/FRAMEWORK_LEARNINGS.md` numbers **1..47 with #14 deliberately reserved** (46 rows), yet `bin/check-learnings` prints *"contiguous 1..46"* — the span is 1..47. That is **BL-44** observed live, not a new defect, and it is **not this session's deliverable**; it ports as-is.

**NOT IN SCOPE:** Phase 3 (the gate), Phase 4 (`ITERATIVE_METHODOLOGY.md`), Phase 5 (the PR itself), D1/D2/D3/D4/D6, issue #75's unsent PR, BL-36's failing proofs, BL-44's repair, trimming either ledger, and **any outward-facing action whatsoever** — the branch is local, nothing is pushed, no PR is opened.

**Ledger:** `CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in [`HANDOFFS.md`](HANDOFFS.md).

### 2026-08-27 · [ad hoc] S119 close-out — Phase 2 shipped, self-score 8/10, predecessor S118 scored 8/10

**Deliverable complete: Phase 2 of the upstream read-set PR plan.** The row-budget scope repaired
and driven RED (20 violators), then all 20 compacted to compliance. Full receipt in
[`HANDOFFS.md`](HANDOFFS.md).

**Commits:** `c28f788` (1B claim + the operator's decision) · `28551a5` (scope repair, committed
RED) · `364b410` (the compaction) · this close-out.

**Final state, measured last.** `starter-kit/FRAMEWORK_LEARNINGS.md` **56,673 B**: `ok` against its
73,728 B ceiling with **17,055 B free**, and **77 B under** the 56,750 B one-read cap. 46 rows,
median 1,436 B, max 1,498 B, **none over budget**. `bin/tests.sh` **289 rows, 288/1/0, exit 1**
against a control of 287, 286/1/0 — zero status flips across 279 shared assertions, zero skips, sole
failure by name `github source dry-run failed` both sides. `check-learnings` **0**, `check-links`
**0**, `check-handoff` **0**, `context_budget.py` **2** (the adjudicated BL-52 ledger breach,
unchanged).

**Predecessor S118 scored 8/10.** Its inversion of the plan's phase order (compact before port) was
right and shaped this session; its costed split reproduced to within the line terminator. **It
missed Test 37 entirely** — Phase 2's largest cost, built end-to-end on the scoping this phase
inverts — and described Test 32's anchors as line numbers when they are content substrings, counting
three where there are four.

**Self-scored 8/10.** RED committed separately so the sequence is verifiable rather than asserted.
**The adversarial pass refuted my own mechanical gate**: 20/20 through it, 19/20 judged DEGRADED by
an independent reader. Against that: I wrote Learning #47 before measuring the room and resized it
four times, and spent 459 front-matter bytes before accounting for them.

**NO OUTWARD-FACING ACTION.** Nothing pushed. `main` is **445 ahead of `upstream/main`** (1 behind)
and 104 ahead of `origin/main`. Issue #75's PR remains local-only and unsent.

**Next session: Phase 1, the port** — branch from `upstream/main` (`512c2ed`), never `origin/main`.
Upstream has no `FRAMEWORK_LEARNINGS.md`, so it is an ADD; **re-derive S118's section diff, which was
measured against a file 17,039 B larger**, and re-check the claimed byte-identity of upstream's
inline rows #1–#13 now that #12/#13 are compacted.

### 2026-08-27 · [ad hoc] S119 — all 20 over-budget Learning rows compacted; 73,712 B → 56,673 B

**Phase 2, part 2 — the deliverable.** Every row of `starter-kit/FRAMEWORK_LEARNINGS.md` is now
within the 1,500 B budget the file's own front matter publishes. `check-learnings` goes RED(1, 20
issues) → **GREEN(0)**: *"46 Learning row(s), contiguous 1..46; all citations resolve; row budget:
46 row(s), 0 over 1,500 B."*

**THE BLOCKER IS CLEARED, AND BY A WIDE MARGIN.** It was *"73,712 / 73,728 — 16 B of headroom, and
NO ROW OF ANY SIZE FITS"* (the smallest row this file has ever carried is 419 B). It is now
**56,673 / 73,728 — 17,055 B of headroom**, roughly eleven more rows. `context_budget.py` reports
`ok` for this file.

**MEASURED AGAINST BOTH TARGETS, AND THEY DISAGREE — the distinction matters to the next session:**

| | bytes | vs plan's 55,930 B target | vs 56,750 B one-read cap |
|---|--:|--:|--:|
| compaction alone (Phase 2 proper) | **55,498** | **432 B under** | 1,252 B under |
| + this session's mandatory Learning #47 | **56,673** | 743 B over | **77 B under** |

**The compaction beat the plan's target by 432 B. Writing the row the protocol requires then put it
743 B over.** The plan's figure was computed as *"73,483 − 17,553"* — full budget compliance and
nothing else — and **never budgeted for the Phase 3C row every session must write.** That is a
defect in the target, not in the compaction, and it is recorded here rather than left for the next
executor to trip over.

**77 B OF MARGIN AGAINST THE ONE-READ CAP MEANS THE NEXT ROW OF ANY SIZE BREACHES IT.** The plan
predicted this — *"820 B is thin … it re-crosses within a session or two"* — and it arrives
immediately. **Compaction is a one-time payment against a recurring cost; only §3.4's gate makes it
durable.** Do not read *"all rows compliant"* as *"the file fits"*.

**HOW THE COMPACTION WAS DONE, AND WHY THE METHOD IS THE FINDING.** 20 rows, one agent each,
followed by an independent adversarial reader per row asked only *what was lost*. **The first pass
cleared every mechanical gate — byte budget, column count, row number, full citation set, both live
`bin/tests.sh` anchors — and the adversarial pass found 33 blocking losses across 16 of the 20
rows**: dropped causal mechanisms, deleted counter-examples, quantifiers softened from "every" to a
bare plural. A repair round restored them; **19 of 20 came back FAITHFUL, 0 non-transferable.**
Row #30's last residual — *"assert on the SPECIFIC finding's wording rather than on the exit code,
which is a union over every clause"* — was restored by hand, paid for by compressing the same row.
Recorded as **Learning #47**.

**TOTALS:** 20 rows, **47,533 B → 29,025 B, shed 18,508 B**. Largest cut #29 (3,451 → 1,474);
smallest #13 (1,572 → 1,446). No row number changed; no citation lost — `check-learnings`'
distributed-corpus sweep proves every `Learning #N` still resolves.

**SUITE, run on the final tree and diffed row-for-row against the control at the claim commit:**
**289 rows, 288 passed / 1 failed / 0 skipped, exit 1** (control: 287, 286/1/0, exit 1 — the suite
exits 1 even when green). Sole failure **by name** both sides: `github source dry-run failed`,
Test 9's standing `--source=github` 404. **Zero status flips across 279 shared assertion texts;
zero skips**, which is what proves Test 34 stayed in its ANCHORED arm. The population changed by
**+2**, and every one of the 18 differing rows is accounted for: **8 lost** are the old Test 37's
frozen-exemption and skip-arm assertions, deliberately removed with the behaviour they described;
**10 gained** are the inverted scope assertion and its frozen-ness control, the two untracked-file
checks, the new domain mutant and its control, and one renamed row. The last difference is a derived
number — the fixture's appended row moves `#47 → #48` because this session added Learning #47, which
is exactly the staleness Test 37's `max+1` derivation exists to absorb.

**CARVE-OUT, parsed on `bin/_manifest.py`'s SOURCE column (a bare-filename grep matches DEST and
inverts the answer):** `starter-kit/FRAMEWORK_LEARNINGS.md` **IS** a manifest source, so the new
front-matter rule **and all 20 compacted rows reach every adopter at their next `bin/sync`.**
`bin/check-learnings` and `bin/tests.sh` are **canonical-only** — adopters receive the compacted file
and the rule, but **not** the checker that enforces it.

### 2026-08-27 · [ad hoc] S119 — the row-budget scope repaired and driven RED: 0 violators → 20

**Phase 2, part 1 of [`docs/planning/upstream-read-set-pr-plan.md`](docs/planning/upstream-read-set-pr-plan.md).**
The guard now fires on its own population. **Committed RED deliberately**, before any row is
compacted, so *"drive the new assertion RED against unpatched code and watch it fail"* — the file's
own Learning #12 — is a matter of record rather than a claim made afterwards.

**BEFORE:** `check-learnings` exit **0**, `row budget: 0 unfrozen row(s), 0 over 1,500 B`.
**AFTER:** exit **1**, `FAIL — 20 issue(s)`, naming every violator and its overage — #12 (+900),
#13 (+72), #15 (+607), #16 (+534), #17 (+470), #18 (+875), #19 (+750), #20 (+1,049), #21 (+1,100),
#22 (+390), #23 (+620), #24 (+1,375), #25 (+1,445), #26 (+637), #27 (+1,248), #28 (+492),
#29 (+1,951), #30 (+989), #31 (+759), #32 (+1,270). The same 20 rows and the same byte counts an
independent measurement found at Phase 0.

**THIS IS NOT A BUG FIX, AND RECORDING IT AS ONE WOULD BE WRONG.** The exemption was *correct while
it held*: its docstring said so — holding frozen rows to a budget *"nobody is permitted to edit"*
would emit *"a permanently red finding with no legal remedy, which is a gate that cannot be obeyed
rather than a gate that works."* That reasoning was sound. What changed is its **premise**: the
operator's decision (entry above) supplied the missing remedy. **A constraint's release is an action
too**, and this entry is that action's record.

**WHAT CHANGED**
- `bin/check-learnings` — `check_row_budget` now scopes over every row. `frozen_rows()` deleted: it
  existed only to compute the exemption. **The SKIP arm went with it**, and that is a
  strengthening — a row's size is a property of its own bytes and needs no history, so a file with
  no git HEAD is now fully checked instead of stated-but-unchecked. Disposition changes from
  `N unfrozen row(s)` to `N row(s)`.
- `bin/tests.sh` Test 37 — **rewritten, not patched.** Its assertion (3) asserted the *opposite*
  property (*"the 20 committed rows already over 1,500 B are exempt as frozen"*) and it drew its
  subject from the live table's incidental content. **The same session that inverts the scope also
  compacts all 20 of those rows away**, so leaving it would have left an assertion passing over an
  empty subject — green, proving nothing. The over-budget frozen row is now **constructed and
  committed inside the fixture**, with a control asserting it really is frozen. The fixture control
  (0) now demands a **positive** row count beside the zero, so `0 rows, 0 over` cannot read as a
  pass. Mutant M3 (the skip arm) is gone with the arm; a new **M2 narrows the budget's domain to
  the newest row only** — the pre-decision behaviour — and asserts an earlier violation is missed.
- `starter-kit/FRAMEWORK_LEARNINGS.md` front matter — **distributed**, so this reaches adopters.
  *"append only; do not edit existing rows"* → *"append only; never renumber"*, with the permitted
  edit named: content may be **compacted**, numbers never change. The scope sentence *"covers only
  rows not yet frozen in git HEAD"* is now *"covers every row"*.

**THE PLAN UNDER-COSTED THIS PHASE.** Its Phase 2 DONE criteria name *"Test 32's four anchors"* and
say nothing about **Test 37**, which is the larger cost by far — Test 32's anchors are content
substrings that survive if the compaction preserves them, while Test 37 is built end-to-end on the
scoping this phase inverts. Cost recorded here rather than discovered by the next executor.

**NOT YET DONE at this commit:** the compaction itself. `bin/tests.sh` Test 37 (0) is expected RED
until it lands.

### 2026-08-27 · [ad hoc] S119 DECISION (operator) — compaction of existing `FRAMEWORK_LEARNINGS.md` rows is PERMITTED, all 20

**Decided by the operator (rmsharp) at S119's Phase 0 report. This is the operator's answer, not an
agent's recommendation** — recorded so a successor cannot read it as a ratified suggestion.

**The question**, put by S118's `next_steps` (a): may a session compact the over-budget rows of
`starter-kit/FRAMEWORK_LEARNINGS.md`? The file's own front matter says *"append only; do not edit
existing rows"*, but the harm that rule names is **renumbering** — *"Renumbering would break every
existing `Learning #N` citation"*. Compaction changes row **content**, not row **numbers**, so it
does not cause the named harm; and the same front matter already says *"Say it shorter rather than
raising the budget."* The rule as literally written still forbids it, which is why it was the
operator's call and not an agent's reading.

**The answer: YES — all 20 over-budget rows, including #12 and #13.** The operator was shown both
costed options and chose the wider one:

| option | rows | excess shed | file after | vs the 56,750 B one-read cap |
|---|--:|--:|--:|---|
| the 18 upstream has never seen | #15–#32 | 16,561 B | 57,151 B | **401 B OVER** |
| **all 20** (chosen) | +#12, #13 | **17,533 B** | **56,179 B** | **571 B UNDER** |

*(Excess measured excluding each row's line terminator. The plan's 17,553 B counts it — same
measurement, two units.)*

**What the wider option costs, stated before it was chosen:** rows #12 and #13 are the only two
upstream already holds, so they are the only two where *"do not edit existing rows"* is genuinely
engaged; and they carry Test 32's live anchors. **The 18 carry none.**

**Explicitly NOT the answer: raising the ceiling a third time** (60,000 → 65,536 → 73,728). That is
the *"every raise is defensible"* failure D1 exists to stop, and S118 named it as the wrong route
before the question was asked.

### 2026-08-27 · [ad hoc] S119 — claim: Phase 2 of the upstream read-set PR plan (repair the scope, then compact)

**Phase 1B claim.** Deliverable: **Phase 2 of
[`docs/planning/upstream-read-set-pr-plan.md`](docs/planning/upstream-read-set-pr-plan.md)** — repair
`bin/check-learnings`'s row-budget scope, drive it RED against today's 20 violators, then compact all
20 rows of `starter-kit/FRAMEWORK_LEARNINGS.md` to under the published 1,500 B budget.

**WHY PHASE 2 BEFORE PHASE 1, against the plan's own ordering.** S118's `next_steps` (b) inverted
them and gave the reason: compacting first means upstream receives a file **already under the cap**,
rather than inheriting one 16,733 B over and needing a second change to fix it. Phase 2 also clears
the blocker in S118's (c).

**THE BLOCKER THIS CLEARS, re-measured at this claim rather than inherited:**
`starter-kit/FRAMEWORK_LEARNINGS.md` is **73,712 B against a 73,728 B ceiling — 16 B of headroom**,
and the smallest row the file has ever carried is 419 B. **No learning row of any size fits.** Every
session that reaches Phase 3C before this lands must record that it wrote no learning, and why.

**THE GUARD THAT CANNOT FIRE, verified live at this claim.** `bin/check-learnings` exits **0** and
prints `row budget: 0 unfrozen row(s), 0 over 1,500 B` — **with 20 violators present**. Its
`check_row_budget` scopes the budget to rows whose text differs from git HEAD, so every frozen row is
permanently exempt. That is the *"unkillable guard"* shape this repo has deleted before. Repairing
the scope is part of the deliverable, and **it must be seen to report 20 before anything is
compacted** — a guard never watched to fail is not a guard.

**MEASURED AT THIS CLAIM, not quoted from the plan.** The plan's `≤ 55,930 B` target was computed
against a **73,483 B** file; S118's own Learning #46 added 229 B afterwards, so the file is now
73,712 B and the equivalent target moves with it. Re-derived, not inherited — which is the same
discipline S118 applied to S117's figures.

**NOT IN SCOPE:** Phase 1 (the port to `upstream/main`), Phase 3 (the size gate and the two shipped
`context_budget.py` defects), decisions D1/D2/D3/D4/D6, BL-45's remedy, issue #75's unsent PR,
trimming `CHANGELOG.md` or `HANDOFFS.md`, the `upstream/main` resync, and **any outward-facing action
whatsoever.** No outward-facing action is approved, implied, or taken.

### 2026-08-27 · [ad hoc] S118 close-out amended — the ordered next-action plan the first report omitted

- **Model:** Claude Opus 5 (1M context).
- **The operator rejected the first close-out report: *"That does not look like a phase 3 close-out report. For one thing it does not propose next actions."*** Correct — `SESSION_RUNNER.md` Phase 3G requires *"What the next session should do"* and the report gave a state dump instead. The receipt's `next_steps` is rewritten as an **ordered critical path**, because a next-step that lives only in chat is unreadable to the next session (Phase 3D: *"Write to files FIRST"*).
- **The sharper finding that came out of writing it: PHASE 2 SHOULD PRECEDE PHASE 1, and the plan lists them the other way round.** Compact before porting, so upstream receives a file already under the cap rather than inheriting one 16,733 B over. Phase 2 also clears the blocker below.
- **The compaction cost is now split and measured. 18 of the 20 over-budget rows are ones upstream has NEVER SEEN — 16,579 B, ZERO test anchors, ZERO edits to content upstream holds.** The other 2 (#12, #13, 974 B) cost three `bin/tests.sh` Test 32 anchor updates (`:2033`, `:2040`, `:2058`) *and* edit rows upstream already has. The 18 alone give **57,133 B — 383 B still over**; all 20 give **56,159 B, 591 B under**. That trade is the whole of Phase 2.
- **The append-only question is narrower than it looks.** The front matter's stated harm is *renumbering* — *"Renumbering would break every existing `Learning #N` citation, which is exactly what 'append only, never renumber' exists to prevent."* Compaction changes row **content**, not row **numbers**. The same front matter already says *"Say it shorter rather than raising the budget."* Still the operator's call; **and a third ceiling raise is the `every raise is defensible` failure D1 exists to stop.**
- **A method failure worth recording: I trimmed the wrong prose first.** A record here is **fence-to-NEXT-fence**, so S118's record carries **S117's** trailing prose (2,978 B), not its own — cutting my own 3A/3B essays moved the number not at all. Four rounds of nibbling followed because I drafted replacements without measuring them; two were *longer* than what they replaced. Fixed by verifying the resulting record size in-script before writing. **Final: 12,256 / 12,288 B, 32 B under.** This is [Learning #46]'s sibling and the reason `bin/check-handoff` exists: run the checker, never predict it.

### 2026-08-27 · [ad hoc] S118 close-out — product-scoped PR plan delivered; self-score 7/10, predecessor S117 scored 8/10

- **Model:** Claude Opus 5 (1M context).
- Phase 3 close-out. Receipt in [`HANDOFFS.md`](HANDOFFS.md); **Learning #46 appended** to `starter-kit/FRAMEWORK_LEARNINGS.md` (**229 B**, measured against 245 B of headroom before writing it, per S117's instruction — it fit with 16 B spare).
- **`FRAMEWORK_LEARNINGS.md` IS NOW 73,712 / 73,728 B — 16 B OF HEADROOM, AND NO ROW OF ANY SIZE FITS.** Not an inference: the smallest row the file has ever carried is 419 B. The next session must raise the fork-local ceiling, compact, or record explicitly that it wrote no learning and why.
- **Self-score 7/10.** The verification discipline held — the tombstone scheme, the row budget and the `run()`-strip byte defect were each settled by **running** the code rather than reasoning about it, and a refutation-of-a-refutation was caught before publication. **Against that: I stated nine current-implementation limits as structural ones and the operator caught it, not me**; I conflated the fork with the product for most of the session when `bin/_manifest.py` is the definition of the product and I had already read it; and I published *"`docs/planning/`, `CHANGELOG.md`, `HANDOFFS.md` and `bin/` are fork-only"*, which is **wrong** — upstream has all four.
- **Predecessor S117 scored 8/10.** Its gotchas were exceptional and changed this session's method — the stale-figure warning, the *"2.27 is a FLOOR, not a density"* line that the 4.13× abbreviation finding descends from, and *"measure the row you intend to write"*. Against that: **§6 scopes every decision to the fork with no column separating what ships**, **D7's stated ground is false** (`.context-budget.json` ships nowhere and is absent from `upstream/main`), and **F4's *"nothing has ever tested otherwise"* over-reaches** — 113 receipts and 11 backlog rows have been retired with a semantic event, a retention floor and a losslessness proof.
- **Verification:** `bin/tests.sh` **287 rows, 286/1/0, exit 1**, row-for-row identical to S117's control, sole failure by name `github source dry-run failed`; `check-links` 0; `check-learnings` 0 (45 rows, contiguous 1..45); `check-handoff` 0; `context_budget.py` exit 2 (the adjudicated BL-52 ledger breach). `git fetch upstream` exit 0 — the one network call, authorised and read-only.
- **Nothing pushed; no PR, issue, comment or tag. `origin/main` was not fetched.**

### 2026-08-27 · [ad hoc] S118 — the upstream read-set PR plan: port, compact, gate (DRAFT)

- **Model:** Claude Opus 5 (1M context).
- **Deliverable: [`docs/planning/upstream-read-set-pr-plan.md`](docs/planning/upstream-read-set-pr-plan.md), 18,279 B against a declared 45,000 B budget.** Planning session; nothing implemented (FM #18).
- **`git fetch upstream` was run with explicit operator permission** and is a read. `upstream/main` is unmoved at **`512c2ed`** (2026-08-11); `main` is **439 ahead, 1 behind**. **No outward-facing action: no push, no PR, no issue, no comment.**
- **THE BASELINE THE WHOLE PLAN RESTS ON — the problem is worse in the product than in this fork.** Upstream's Phase 0 pair is `SESSION_RUNNER.md` **65,140** + `SAFEGUARDS.md` **15,386** = **80,526 B = 28,234 metered tokens = 112.9% of one read**, and **23,776 B over** the 56,750 B floor cap. **Over on BOTH denominators, so no density choice rescues it.** The fork's pair is 69,749 B / 24,597 tok / 98.4%, which *fits* when metered — so every figure measured against this fork was measured against the wrong tree.
- **NOTHING IS LOST BY PORTING; the fork is a strict superset.** `SAFEGUARDS.md` is **byte-identical** (blob `f0964195…`); `SESSION_RUNNER.md` has **identical heading structure** (empty symmetric difference both ways); **exactly three sections differ** and account for the −10,777 B to the byte — Learnings 13,422→442 (**−12,980**, the `ed22ace` extraction), Phase 2 **+1,977**, Phase 3 **+226**. Upstream's 13 inline learnings are **byte-for-byte the fork's rows #1–#13**. **Upstream lacks two whole product files:** `starter-kit/FRAMEWORK_LEARNINGS.md` and `starter-kit/methodology_trim.py`.
- **THE LARGEST WIN IS ALREADY BUILT AND UNSHIPPED.** Porting `ed22ace` takes upstream 80,526 → 69,749 B, overage 23,776 → 12,999 B — **a 45.3% cut with zero new authoring.**
- **THE REMEDY THAT CLOSES THE GAP IS THE FRAMEWORK'S OWN PUBLISHED ROW BUDGET.** 20 of `FRAMEWORK_LEARNINGS.md`'s 44 rows exceed the 1,500 B budget by **17,553 B**; compliance gives **55,930 B, 820 B UNDER the cap**. **Upstream has only 2 of those 20 rows** (#12/#13, 972 B), so the append-only rule is engaged by two rows, not twenty. **And `bin/check-learnings` cannot see any of it** — it scopes the budget to rows not frozen in git HEAD, so all 44 are permanently exempt and it prints `0 unfrozen row(s), 0 over 1,500 B` against 20 violators. Repairing that scope is part of the PR.
- **THREE AVENUES REFUTED, recorded so nobody re-runs them.** **(1) Removing rarely-used learnings yields ZERO** — every candidate died; deleting #39–#42 fails contiguity AND turns `bin/tests.sh` Test 32 red, which carries **four hardcoded anchors into the live distributed file**. **(2) Abbreviation does not pay, and the measurement is the point:** at the 2.27 floor its 1,593 B would be credited as **702 tokens** and delivers **170** — **the floor overstates abbreviation by 4.13× while overstating plain deletion by only 1.23×**, because abbreviation is the one operation that lowers B/token. Whole-corpus upper bound **1,203 B = 0.849%**. Also not injective. **(3) Example-list truncation is right in kind and 22× short** — truncating *every* 3+-member comma series in both files recovers 10,484 B = 37% of the gap.
- **The #7/#8 merge is genuine but nets 303 B**, and the enabling decision is disposal of the vacated number: **reservation breaks 4 checker-gating citations** (`main()` builds `valid` from existing rows and never adds the reserved set); **a ~250 B tombstone keeps contiguity AND citations green** — proven by running the checker on scratchpad copies, not reasoned.
- **TWO SHIPPED DEFECTS FOUND IN `context_budget.py`, both verified by running the code.** `precommit()` **measures one byte short** — `run()` returns `p.stdout.strip()`, giving 54,362 for a 54,363 B file; a size gate that miscounts bytes is the wrong foundation. And `cfg["classes"]["resident"]` is a **direct key access at `:339` and `:892`**, so a config without that key raises `KeyError`.
- **The gate's weakest link is stated rather than hidden:** `core.hooksPath` is **local git config, never in the repo**, there is **no CI**, and `.githooks/` is in neither manifest — so **the gate binds only someone who chooses to be bound**. `.githooks/pre-commit` already warns about exactly this design: *"32 of 32 … shipped with `--no-verify` … the derived-value checks planned for this same hook inherit that reflex unless it is removed first."*
- **Evidence base: two workflows, 28 agents, 0 errors** — 7 decision censuses + 7 verifiers, then 5 shrink censuses + 5 verifiers + 3 gate designs + 1 judge. The verifiers refuted a great deal, including **one refutation of a refutation** that would otherwise have shipped: an agent claimed R1's membership was wrong because Phase 0 mandates `BACKLOG.md`; its verifier established that step 3 says *"fall back … if no repo exists"* and this repo has one. Read-only throughout; `git status --porcelain` stayed the two telemetry `.jsonl` only.

### 2026-08-27 · [ad hoc] S118 RE-AIM — the deliverable becomes a product-scoped shrink plan plus a size gate, aimed at one upstream PR

- **Model:** Claude Opus 5 (1M context).
- **The operator re-scoped the session mid-flight, and the re-scoping is the substance, not a detail.**
  In their words: *"much of my problem in understanding you is that you are solving two problems and,
  presently, I am only concerned with one … 1) fixing the `methodology` repository's customized files.
  2) fixing the files and code that goes to adopters. The problem that is most important is to fix the
  files and code that goes to adopters via https://github.com/KJ5HST/methodology.git"* — and then:
  *"Our goal is to create a PR for upstream that addresses the file management problem we are working on."*
- **The re-scoping was earned by a defect in how S118 was presenting the decisions.** Every option in §6
  had been costed without sorting Problem 1 from Problem 2, so fork-only work (`.context-budget.json`,
  `docs/planning/`, `docs/archive/`, the root ledgers) was priced beside product work as though both
  reached adopters. **The product is exactly `bin/_manifest.py`'s DISTRIBUTION list: 26 rows / 936,867 B**
  — 21 TRACKED (906,419 B) + 5 SEED (30,448 B). Nothing else reaches an adopter by any route.
- **THE THREE ASSIGNED DELIVERABLES**, all planning-mode (FM #18: nothing implemented this session):
  **(1)** analyse `starter-kit/FRAMEWORK_LEARNINGS.md` and `ITERATIVE_METHODOLOGY.md` for shortening —
  duplication removal, merging near-identical learnings (the operator named **#7/#8** as a candidate pair,
  and row 8 says of itself *"This is Learning #7 applied to procedure summaries rather than citations"*),
  abbreviations for frequent phrases, removal of rarely-used learnings, and truncation of example lists
  that enumerate every instance from the original finding. **(2)** design a gate preventing
  `SESSION_RUNNER.md` + `SAFEGUARDS.md` from becoming undeliverable. **(3)** aim both at one upstream PR.
- **The premise was checked before the work started, and it is conditionally true — the condition matters.**
  At the 2.27 floor (decision D5 below) one read is 56,750 B, so `FRAMEWORK_LEARNINGS.md` (73,483 B) is over
  by **16,733 B** and `ITERATIVE_METHODOLOGY.md` (68,240 B) by **11,490 B**. **Metered directly, both still
  fit** — 24,110 and 23,432 tokens against the 25,000 cap. `FRAMEWORK_LEARNINGS.md`'s true runway is
  **2,714 B ≈ one to two rows**, so the shortening buys headroom that is nearly gone rather than recovering
  headroom already lost. Recorded this way so no successor inherits the stronger claim.
- **The load-bearing number for the whole effort:** the framework's *own* shipped Phase 0 read —
  `starter-kit/SESSION_RUNNER.md` (54,363 B) + `starter-kit/SAFEGUARDS.md` (15,386 B) = **69,749 B =
  24,597 metered tokens = 98.4% of one 25,000-token read**, before the adopter's `CLAUDE.md` — which the
  framework does **not** own (`CLAUDE_TEMPLATE.md` is the manifest dest, never `CLAUDE.md`) — contributes a
  byte. Across 11 real adopters that file runs 2,725–43,956 B.
- **Superseded, not abandoned:** the claim entry above stands. D1/D2/D3/D4 and D6 remain unanswered and are
  now re-posed against the product rather than against this fork.
- **No outward-facing action taken.** No fetch, no push, no PR, no issue, no comment. `main` is 97 ahead of
  `origin/main` and **438 ahead of `upstream/main`** (1 behind, `512c2ed`), measured against refs last fetched
  2026-08-15 / 2026-08-11 and therefore **stale**; the operator asked about resyncing as a *question* and it
  was answered, not executed (FM #23).

### 2026-08-27 · [ad hoc] S118 DECISIONS (3 of 7) — the density floor, the fork-local ceiling, and the fleet instrument

- **Model:** Claude Opus 5 (1M context).
- Three **operator decisions** from §6, recorded per FM #27 before any carrier is edited. Four remain open
  (D1, D2, D3, D4, D6 — re-posed against the product after the re-aim above).
- **(1) D5 — CEILINGS ARE DENOMINATED IN THE CONSERVATIVE `MIN_BYTES_PER_TOKEN = 2.27` FLOOR**, giving
  `READ_CAP_BYTES = 56,750`. Chosen over per-file measured density, a per-class denominator, and two
  labelled denominators. **This ratifies what already ships** — the floor is already the constant in
  `starter-kit/methodology_trim.py:120` and both dashboard twins, all TRACKED. Two consequences were put to
  the operator before the choice was recorded: it leaves `SESSION_RUNNER.md` **2,387 B** of headroom against
  a floor-denominated ceiling, when that file's four largest single commits are **+8,084 / +5,325 / +5,101 /
  +4,436 B**; and it disagrees with the 73,728 B ceiling S114 derived for `FRAMEWORK_LEARNINGS.md` at that
  file's *measured* 3.03 density. **Both collisions are Problem 1** — they live in the fork-only
  `.context-budget.json` — so neither blocks the product work. **The in-scope residue is a product defect:**
  the SEED `starter-kit/context-budget.json` declares `bytes_per_token: 2.93`, a *fourth* denominator that
  contradicts the floor and ships to every future adopter.
- **(2) D7(a) — YES, the canonical repo may hold itself to a ceiling on `SESSION_RUNNER.md` and
  `SAFEGUARDS.md`.** **Problem 1**, and the plan's stated ground for fencing it was measured and **refuted**:
  §6's *"Adding them … ships upstream"* and dragon 3 are false for the edit the decision actually requires.
  `.context-budget.json` is **never a manifest SOURCE** (only ever a DEST, from the SEED
  `starter-kit/context-budget.json`) and **does not exist in `upstream/main`** — `git cat-file -e
  upstream/main:.context-budget.json` exits 128 while `origin/main` exits 0. The *other* half of the ground
  stands: a ceiling constrains what future canonical sessions may write into a TRACKED file.
- **(3) D7(b) — NO, the fleet-wide instrument must not flag those two files.** **This ratifies shipped
  behaviour**: `starter-kit/methodology_dashboard.py:420-425` already excludes them from `READ_CAP_WATCHED`,
  and `:350-356` states the reason — *"one canonical breach would light up every adopter at once over a file
  they cannot edit."* **No product change; the value is that the exclusion is now a decision on record with
  a reason, so no future session re-opens it as an oversight.** The two declines rest on *different* grounds
  and only the first was affected by the refutation above.
- **The distinction the decision turns on, from the manifest's own header:** `SAFEGUARDS.md` is protected at
  an adopter (TRACKED — `bin/sync`'s `classify_target()` marks a locally edited copy `modified` and declines
  to overwrite) and **editable here**, where it is the original — 8 commits, 7,850 → 15,386 B. So a ceiling
  here is actionable and a fleet flag is not, which is exactly what `.context-budget.json`'s `_synced` key
  already argues.

### 2026-08-27 · [ad hoc] S118 claim — answer the six operator decisions gating Phase 1 of the file-management plan

- **Model:** Claude Opus 5 (1M context).
- Phase 1B claim. **Deliverable: the six operator decisions in
  [`docs/planning/file-management-system-plan.md`](docs/planning/file-management-system-plan.md) §6,
  asked and RECORDED** — each as its own entry in this ledger, the way S116 recorded its three.
  Assigned by the operator at this claim from a Phase 0 report that put it beside BL-51 Phase C3,
  issue #75's unsent PR, and the 1-commit `upstream/main` resync. **None of those is authorized.**
- **Why this is a session and not a preamble.** §6 states the gate in its own words — *"Phase 1 does
  not start until these are answered"* — and states why the gate cannot be dissolved by working
  harder: *"None is derivable from measurement — that is why they are here and not in §4."* The plan
  is **DRAFT** until they are answered; six of its seven phases depend on the vocabulary D1–D6 fix.
- **THE ANSWERS ARE THE OPERATOR'S. A RECOMMENDATION IS NOT AN ANSWER.** This session's work is to
  re-verify each decision's load-bearing evidence **against today's tree**, put concrete costed
  options with their consequences, and record what is chosen — attributed, so a successor cannot
  read a recommendation as a ratification.
- **The six, in §6's order:** **D1** target cost per session · **D2** how many of each thing the
  framework carries · **D3** the semantic event on which an artifact retires · **D4** whether
  *undeliverable in one `Read`* is a fault or an accepted operating state · **D5** whether ceilings
  are denominated in the conservative floor or measured density · **D6** whether the framework has
  jurisdiction over adopter-owned files, and by what delivery mechanism. **A seventh rides with
  Phase 1** — whether `SESSION_RUNNER.md` and `SAFEGUARDS.md` get ceilings at all; it is recorded
  with the six because `.context-budget.json`'s `_deliberate_exclusions` declined it once already.
- **RE-MEASUREMENT IS PART OF THE WORK, NOT A COURTESY.** Every figure in §6 was measured during
  S117 and some were stale before that session closed: `FRAMEWORK_LEARNINGS.md`'s 73,483 B is the
  size *after* S117's own Learning #45, and both root ledgers grew again at its close-out. Figures
  quoted to the operator are re-derived here and the command is shown beside each.
- **Not in scope, explicitly:** Phase 1 itself (teaching `context_budget.py` to total any declared
  class), any edit to `.context-budget.json`, BL-45's remedy, BL-51 Phase C3,
  BL-42/43/44/46/47/48/49/50/52, issue #75's unsent PR, trimming `CHANGELOG.md` or `HANDOFFS.md`,
  the `upstream/main` resync, **and any outward-facing action whatsoever.**
- **State at claim, measured:** `main` clean but for the two telemetry `.jsonl`; **96 ahead of
  `origin/main`, 437 ahead / 1 behind `upstream/main`**. `check-handoff` **0**, `check-learnings`
  **0** (44 rows), `check-links` **0**, each run bare. `context_budget.py` exits **2** — the
  adjudicated BL-52 ledger breach, unchanged, **not** a regression; `methodology_trim.py --check`
  fires on **neither** ledger (run per file — bare it exits **3** on a *usage* error, which is not a
  signal about either ledger). Dashboard **76/100**, medium risk, 694 commits.

### 2026-08-27 · [ad hoc] S117 close-out — full-scope file-management plan shipped, self-score 8/10

- **Model:** Claude Opus 5 (1M context).
- Close-out receipt written to [`HANDOFFS.md`](HANDOFFS.md); **predecessor S116 scored 8/10**.
- **Build-equivalent RUN:** `bin/tests.sh` **287 rows — 286 passed / 1 failed / 0 skipped, exit 1**,
  identical row-for-row to S116's control; sole failure by name `github source dry-run failed`
  (Test 9's standing 404). **Zero skips**, so Test 34 stayed in its anchored arm. Tests 34/37 mutate
  the live `HANDOFFS.md` and `FRAMEWORK_LEARNINGS.md` and **the tree restored cleanly.**
  `check-links` 0, `check-learnings` 0, `check-handoff` 0, all run bare. `context_budget.py` exits
  **2** — the adjudicated BL-52 ledger breach, unchanged, not a regression.
- **Phase 3C discharged: Learning #45 appended** (836 B) — *a budget made of per-file ceilings
  cannot see the cost that is actually paid, the aggregate.* `starter-kit/FRAMEWORK_LEARNINGS.md`
  72,646 → **73,483 B against 73,728: `ok`, 245 B headroom.** **This corrects a claim this session
  itself repeated from S116:** the file did **not** block a learning row. A *median* row (1,464 B)
  does not fit; a terse one does. Measure the row you intend to write.
- **`starter-kit/FRAMEWORK_LEARNINGS.md` is a TRACKED manifest source, so Learning #45 reaches every
  adopter at their next `bin/sync`.** Re-derived on the manifest's source column at close-out. The
  plan itself (`docs/planning/`) and the two root ledgers are **not** distributed.
- **FIVE DEFECTS FOUND AND DELIBERATELY NOT FIXED**, recorded here so they are not lost and each
  needing a backlog item a future session raises: (1) a **new current-generation v1.3.0 losslessness
  proof failure** — `docs/archive/HANDOFFS-through-2026-08-25.md.verify.sh` exits 1 with
  `L2 FRONT MATTER lost 1 line(s)`, caused by the hand-maintained *"Archived shards — N trims, M
  receipts"* sentence that is not in `spec.regenerated` and that the next trim edited — making
  **5 of 16** shipped proofs red, not BL-36's four; (2) **`bin/check-learnings` is silently disarmed
  by a single blank line** inside the table — it prints `OK — 21 Learning row(s), contiguous 1..21;
  all citations resolve` at **exit 0** with 43 rows present, and on today's file only an *incidental*
  citation catches it; (3) its **"out of ascending order" guard is dead code**, nested inside the
  contiguity-failure branch — reversing all 43 rows returns exit 0; (4) **four `[[N]]`
  cross-references** in rows #32/#33/#36/#38 are invisible to `CITATION_RE`; (5) the seed
  `starter-kit/context-budget.json` declares **`LEARNINGS.md`**, a filename no manifest dest installs.
- **Two self-corrections on the record, both of which reached the operator before they were
  measured:** `ITERATIVE_METHODOLOGY.md` was asserted past its one-read limit from an *estimated*
  density and in fact reads whole with **1,568 tokens spare**; and this session's own claim commit
  `fd44454` said *"every figure in [BL-45] is stale"* when **both its byte columns reproduce
  byte-exactly** — only its baseline, row count, median and citation figure are wrong.
- **No outward-facing action taken, and none authorized.** `main` is **95 ahead of `origin/main`**;
  nothing pushed. Issue #75's PR remains local-only and unsent.

### 2026-08-27 · [ad hoc] S117 — a full-scope file-management plan for the framework (DRAFT)

- **Model:** Claude Opus 5 (1M context).
- **Deliverable:** [`docs/planning/file-management-system-plan.md`](docs/planning/file-management-system-plan.md)
  (31,643 B, against a **declared 65,000 B budget** stated in its own header — the plan is file 32
  in an ungoverned directory and says so). **Planning session: nothing is implemented.**
- **Evidence base:** a 6-census / 12-verifier / 1-critic read-only workflow, plus direct measurement
  with the no-content token meter. Every figure was reproduced by a command; §10 carries the
  reproductions. Tree asserted clean throughout — no agent wrote to this repo or to any adopter.
- **THE CENTRAL FINDING, metered rather than estimated:** the mandatory Phase 0 read set —
  `CLAUDE.md` + `starter-kit/SESSION_RUNNER.md` + `starter-kit/SAFEGUARDS.md` — is **80,813 B =
  28,832 tokens = 115.3% of the 25,000-token single-read limit.** It cannot be delivered in one
  read and would have to shed 10,741 B to fit. **No per-file ceiling can catch it: the failure is a
  sum nothing sums.** `starter-kit/context_budget.py:888-898` totals exactly one class and hardcodes
  which (`cfg["classes"]["resident"]`), and that class has one member.
- **Six more structural findings, each reproduced:** (F2) the ceilings sit on the files that can
  afford to grow — `CHANGELOG.md`/`HANDOFFS.md` are frontier-read and newest-first, so truncation
  costs them their *oldest* records, while the unwatched oldest-first files lose their *newest*;
  (F3) **the only automated decay mechanism is net-additive by 1.79×** — trim `9038e40` relieved
  22,146 B and added 39,672 B for a **net +17,526 B**, the proof script being 70% of the shard it
  certifies, and `docs/archive/` is now 35.0% of the tracked repo with no ceiling and no deletion
  ever; (F4) **in 693 commits exactly one tracked file has ever been deleted** (`LICENSE`, `d207d1c`,
  re-added as a mistake) — the framework has a create verb and no retire verb; (F5) nothing
  mechanically enforces any ceiling, and the one hook that *is* installed forces growth; (F6)
  `docs/planning/` and the archive tier are ungoverned, and `git log --oneline` is **56,856 B**, a
  read artifact with zero possible decay; (F7) three live ceilings, two densities differing by 25%,
  and **20 copies of the literal `65536` across 8 files** with nothing keeping them consistent.
- **Fleet evidence, measured read-only across 11 real adopters:** **8 of 11 exceed the single-read
  limit** on mandatory Phase 0 reading — robust at both the measured mix density and the most
  token-sparse density in the repo — while only **3 of 11** hold any size instrument, and 10 files
  across 5 adopters are already past the 262,144 B hard refusal.
- **SIX OPERATOR DECISIONS (§6) GATE PHASE 1 and are not derivable from measurement:** the target
  cost per session; how many of each thing the framework should carry; the semantic retirement
  event; whether "undeliverable in one read" is a fault or an accepted state; conservative floor vs
  measured density; and whether the framework has jurisdiction over adopter-owned files.
- **BL-45 is absorbed, not closed.** Its remedy becomes Phase 4's first instance. Its byte columns
  were re-derived and **still reproduce exactly**; its citation figure does not — *"five, in two
  files"* at N=10 is **9, in 4 files**, measured by running the checker. **This session's own claim
  commit (`fd44454`) was wrong to say every figure in it is stale, and that is corrected here.**
- **Defects found and deliberately NOT fixed** (handed forward, out of a planning session's scope):
  a **new current-generation `.verify.sh` failure** (`HANDOFFS-through-2026-08-25`, `L2 FRONT MATTER
  lost 1 line(s)`) making **5 of 16** shipped proofs red; `bin/check-learnings` **silently disarmed
  by a single blank line** (prints `OK — 21 rows` at exit 0 with 43 present); its dead
  ascending-order guard; four `[[N]]` citations invisible to its sweep; and the seed budget
  declaring `LEARNINGS.md`, a filename no manifest dest installs.
- **Not in scope / not taken:** implementing any phase, BL-51 Phase C3, `RECORD_BUDGET_BYTES`,
  trimming either ledger, and **any outward-facing action whatsoever.** Phase 6 (upstream PR)
  explicitly requires the operator's go-ahead and is **not** implied by approving this plan.

### 2026-08-27 · [ad hoc] S117 RE-AIM — the deliverable becomes a full-scope file-management plan

- **Model:** Claude Opus 5 (1M context).
- **Operator decision, taken mid-session, and it supersedes this session's own claim entry below
  rather than abandoning it.** The session was claimed for BL-45's `FRAMEWORK_LEARNINGS.md` remedy;
  the BL-45 research ran to completion and its findings stand (recorded in the two entries below).
  Presented with the re-costed options, the operator asked instead for
  *"a full scope plan … because we have been solving localized problems and not solving for making
  methodology as efficient and effective as possible from the standpoint of file management."*
- **THE RECORD SUPPORTS THAT CHARACTERISATION, which is why the re-aim is recorded as a decision
  and not as scope drift.** Every prior effort in this space is a point fix on one artifact:
  BL-19, BL-22, BL-37, BL-42, BL-43, BL-44, BL-45, BL-46, BL-47, BL-48, BL-49, BL-50, BL-51, BL-52,
  [`read-cap-phase-c-plan.md`](docs/planning/read-cap-phase-c-plan.md) Phases A–C,
  [`record-budget-reduction-plan.md`](docs/planning/record-budget-reduction-plan.md),
  [`ledger-trimmer-design.md`](docs/planning/ledger-trimmer-design.md) and
  [`framework-context-cost-plan.md`](docs/planning/framework-context-cost-plan.md).
  **No document in this repository has ever asked what the whole file-management system should be**,
  which is why the two largest per-session reads have no ceiling and nobody noticed (see below).
- **THE DELIVERABLE IS A PLAN AND NOTHING IS IMPLEMENTED THIS SESSION** — Planning-session rules,
  `SESSION_RUNNER.md` §Planning Sessions and failure modes #18/#19. The plan is written to
  `docs/planning/`, with the mandatory grep-based evidence inventory, per-phase DONE criteria,
  verification commands, and the **surface** each criterion is demonstrated on. Implementation is
  a separate session per phase.
- **BL-45's own remedy is deliberately NOT taken here.** Its four options are re-costed inside the
  plan and put to the operator there. Closing it by a point fix is precisely the pattern the re-aim
  rejects.
- **THE FINDING THAT MOTIVATED THE RE-AIM, measured this session:** `.context-budget.json` declares
  ceilings for five paths, and **neither of the two files every session must read in full is among
  them** — `starter-kit/SESSION_RUNNER.md` (54,363 B, ~18,100 tok, the largest recurring context
  cost in the repository) and `starter-kit/SAFEGUARDS.md` (15,386 B, which Phase 0 step 1 requires
  *"in full, not skimmed"*). Meanwhile the two files that **are** red — `CHANGELOG.md` and
  `HANDOFFS.md` — are read only at a frontier, are newest-first, and so lose their **oldest**
  records to truncation, which is the harmless end. **The guards are on the files that can afford
  to grow, and absent from the files that cannot.**
- **Not in scope:** implementing any phase of the plan, BL-51 Phase C3, `RECORD_BUDGET_BYTES`,
  issue #75's unsent PR, and **any outward-facing action whatsoever.**

### 2026-08-27 · [BL-45] S117 claim — BL-45 re-opened: the `FRAMEWORK_LEARNINGS.md` size remedy

- **Model:** Claude Opus 5 (1M context).
- Phase 1B claim. Deliverable: **BL-45's remedy**, re-opened on BL-45's own closing instruction —
  *"Re-open when the ~3 remaining rows are spent."* They are spent. `starter-kit/FRAMEWORK_LEARNINGS.md`
  is **72,646 B against a 73,728 B ceiling — 1,082 B free**, and `ROW_BUDGET_BYTES` is **1,500**, so
  **no conforming Phase 3C learning row fits.** S116's close-out named this the binding constraint on
  its successor rather than a note, and it binds this session too.
- Authorized by the operator at this claim, from a Phase 0 report that put it beside BL-51 Phase C3
  and issue #75's unsent PR. **Phase C3 stays unstarted. No outward-facing action is approved,
  implied, or taken.**
- **THE OPTION CHOICE IS THE OPERATOR'S.** BL-45's own table says so outright (*"the choice is the
  operator's"*). Its four options — (a) archive oldest rows, (b) raise the ceiling **[taken at S114,
  now spent]**, (c) compact the over-budget frozen rows, (d) split by theme **[BL-45 advises
  against]** — are put to them **re-derived against today's tree**, not quoted: the costed table was
  measured at **65,520 B / 37 rows** and the file is now **72,646 B / 43 rows**, so every figure in
  it is stale. Whichever way it falls is recorded here as its own ledger entry before any row moves.
- **TWO FACTS FOUND AT ORIENT ALREADY FALSIFY THAT TABLE, and both are recorded now rather than at
  close-out, because a successor who reads BL-45 without them will act on a wrong premise:**
  1. **The carrier is a DISTRIBUTED manifest source.** `bin/_manifest.py:38` is
     `("starter-kit/FRAMEWORK_LEARNINGS.md", "FRAMEWORK_LEARNINGS.md", TRACKED)` — read on the
     **source** column, not by grepping the bare filename — so any change reaches **every adopter at
     their next `bin/sync`**. BL-45's closure note says *"The change is canonical-only … so no
     adopter is affected"*; that is true of the **ceiling in `.context-budget.json`**, which is what
     S114 actually moved, and **not** of the file. Left standing in BL-45 per FM #17; corrected here.
  2. **Option (a) needs checker work at EVERY N, not only at large N.** BL-45's correction (i)
     retired the *citation* objection on measurement — archiving the oldest 5 orphans **zero**
     distributed citations. It never reached `bin/check-learnings:197`,
     `expected = list(range(1, len(numbers) + len(reserved) + 1))`: the numbered set is asserted
     contiguous **from 1**. Archiving the oldest row fails the checker at **N = 1** with
     *"not contiguous from 1 — missing #1"*. The table's *"needs no checker work at small N"* is a
     claim about citations that reads as a claim about the checker.
- **Not in scope:** BL-51 Phase C3 (A3/B1/B2), `RECORD_BUDGET_BYTES` and the record-budget campaign,
  BL-42/43/44/46/47/48/49/50/52, issue #75's unsent PR, and **any outward-facing action whatsoever.**
- **State at claim, recorded because a successor will misread it:** `CHANGELOG.md` (92,346 B) and
  `HANDOFFS.md` (123,667 B) are over their fork-local ceilings **by adjudication, not neglect**
  (BL-52) — `context_budget.py` exits **2**, while `methodology_trim.py --check` fires on
  **neither**, which is the intended post-Phase-C2 state. **This session does not trim them.**

### 2026-08-26 · [BL-51] S116 — Phase C2: the Class A archive threshold, bundled with `DEFAULT_BUDGET_BYTES`

- **Model:** Claude Opus 5 (1M context).
- **Phase C2 of [`read-cap-phase-c-plan.md`](docs/planning/read-cap-phase-c-plan.md) §9, complete**
  — option **A2** and option **C1** in one commit (`0afe9d6`), as §8 requires and §10 dragon 1
  explains. New `CLASS_A_FIRE_BYTES = 192*1024` / `CLASS_A_STOP_BYTES = 96*1024`;
  `DEFAULT_BUDGET_BYTES` **65,536 → 196,608**; `Trigger.read_fire_at` / `read_stop_at` per class;
  new `is_root_class_a()`. `methodology_trim.py` **1.4.0 → 1.5.0**, `methodology_dashboard.py`
  **2.16.1 → 2.17.0** with its twin.
- **THE FINDING THAT CHANGED THE PHASE'S SHAPE: §7's *"replace the read arm's threshold"* is TWO
  SITES.** `Trigger.stops()` compares each candidate cut to its own constant, and before C2 the
  fire and the stop were both `READ_CAP_BYTES`. **Moving only the fire leaves `choose_cut` cutting
  to 56,750 B — three times deeper than intended — with the whole suite green**, because every
  assertion was about what *fires* and none about what a remedy *converges to*. Found by reading
  `stops()` before writing anything, and pinned by an end-to-end test on the resting size: a real
  `--write` on a 213,704 B fixture lands at **93,909 B**, inside
  `(READ_CAP_BYTES, CLASS_A_STOP_BYTES]`. Recorded as **Learning #44**.
- **§9's DONE criterion, each half demonstrated:** `--check` **fires on neither ledger** at today's
  sizes (exit 0, was 1); **fires** on a synthetic 256,037 B root ledger; `choose_cut` returns a
  **real cut at both densities** (`CHANGELOG.md` 26 of 27 → 85,052 B; `HANDOFFS.md` 8 of 10 →
  91,906 B), not the `return 1` fall-through; **no ledger can stop above `READ_REFUSE_BYTES` at any
  budget**, asserted to 4 MiB — the read arm caps the byte arm, which is the `--budget-bytes` guard
  restated at the new value.
- **The widened half — the dashboard — was TWO unowned sites, not the one §6 names**, and that
  section's `:3045-3072` citation is pre-C1 (true range `:3135-3169`). The second is
  `collect_trim_metrics:2197`, which **re-implements** the trimmer's read arm; left behind it would
  have emitted *"the archive trigger fires; … run `--check`"* beside a `--check` reporting that it
  does not. **A1's deferred *buys* are now delivered:** the two rows are *different* rather than
  deduplicated (§7's own wording), and the effect is fleet-visible — a Class A ledger over the
  one-read cap drops **`high` → `low`**, worst risk `high` → `medium`.
- **`READ_CAP_BYTES` did not move and must not** — it is a measured harness fact, not a policy
  knob. It still reports, and it is still Class B's threshold.
- **VERIFIED, NOT ARGUED.** `bin/tests.sh` row-for-row against a worktree control at `b80f1a8`,
  run **twice** (after the deliverable, and again after the prose repairs rather than assumed),
  both populations asserted non-empty: **287/287, zero lost, zero gained, zero status flips, zero
  skipped**; sole failure both sides by name, Test 9's standing `--source=github` 404. Python
  suites **111/313/42 → 123/321/42**. **Mutation: 12 mutants, 12 killed, 0 survived, 0 failed to
  apply** — and the half-application mutant was re-run alone to list **all four** objecting tests,
  three of them this session's, because the harness reports only the first.
- **A guard written to gate this phase stayed green through it.** S115's
  `test_phase_c1_moved_no_threshold` promised a namespace check *"which no per-class threshold can
  slip past whatever it is called"*; it greps one prefix, and `CLASS_A_FIRE_BYTES` is not that
  prefix. Its successor sweeps by **substring** and asserts the exact expected set.
- **Not done, each deliberately:** all of **Phase C3** (A3, B1, B2), `RECORD_BUDGET_BYTES`,
  BL-42/43/44/46/47/48/49, issue #75's unsent PR, and **any outward-facing action whatsoever.**

### 2026-08-26 · [BL-51] Phase C2 DECISIONS — `DEFAULT_BUDGET_BYTES` raised, C2 widened to the dashboard, the Class A threshold scoped to root

- **Model:** Claude Opus 5 (1M context).
- Three non-commit **operator decisions**, recorded per FM #27 before any carrier is edited. The
  plan states of the first *"This plan does not decide it"*; S115 fenced the second as needing the
  operator; the third neither the plan nor S115 anticipated and it was found by measurement this
  session.
- **(1) OPTION C1 — `DEFAULT_BUDGET_BYTES`: RAISE to `192 * 1024` (196,608).** Chosen over retiring
  it and over keeping it.
  - Keeping it is not viable *if C2 is to close*: both ledgers `byte_fire` at today's sizes
    (81,070 B and 111,388 B against 65,536), so §9's C2 criterion — *"`--check` fires on neither
    ledger at today's sizes"* — is **unsatisfiable** with the constant where it is.
  - Retiring it is a `NameError` at import from the `LedgerSpec` default parameter
    (`starter-kit/methodology_trim.py:218`) unless the whole per-file budget machinery goes with
    it, which would delete the `--budget-bytes` knob §8 gives a reason to keep. It also removes the
    **only** byte guard adopters have on these two files: the seed
    `starter-kit/context-budget.json` governs `CLAUDE.md`, `SESSION_NOTES.md` and `LEARNINGS.md`
    and **not** the two ledgers (BL-47, re-verified this session by parsing the seed).
  - Raising costs nothing extra in machinery: `BYTE_STOP_FRACTION` is already 0.5, so
    `int(196,608 × 0.5)` is **98,304 = 96 KiB exactly**, which is option A2's stated stop.
- **(2) THE C2 HOLE — WIDEN C2 rather than raise a fourth phase.** C2's DONE criterion now also
  covers the dashboard. **The hole is TWO sites, not the one §6 names**, and the plan's
  `:3045-3072` citation is pre-C1 — the true D4(b) range on this tree is
  `starter-kit/methodology_dashboard.py:3135-3169`. The second site is the sharp one:
  `collect_trim_metrics:2197` **re-implements** `read_fires = size_bytes > READ_CAP_BYTES` and
  emits *"the archive trigger fires; … run `--check` for the full report"*. Moving the trimmer's
  trigger without it would have the dashboard name a command whose output contradicts the row —
  the exact misdirection the comment at `:2240` says that wording exists to avoid.
- **(3) THE CLASS A THRESHOLD IS SCOPED TO THE REPO ROOT.** Found by measurement, not anticipated:
  the trimmer resolves its config by **basename at any depth** (`methodology_trim.py:1674`,
  `LEDGERS.get(path.name)`), while the dashboard's class is a **repo-relative path** lookup
  (`methodology_dashboard.py:407`). Unscoped, the relaxed threshold would apply to any
  `*/CHANGELOG.md` or `*/HANDOFFS.md` — **3.38× today's 56,750 B** — for a file that was never
  classified. Harmless today (the only non-root instances in 13 portfolio repos are this repo's own
  two ~12 KB seeds) and a trap tomorrow. The relaxed pair applies only where the file sits at the
  repo root; a nested one keeps the tighter one-read threshold.
- **Two costs of (1) are accepted with eyes open, and neither goes red on its own.** Moving the
  constant silently falsifies three `.context-budget.json` `_` keys that name it as their ceiling's
  source (*"max_bytes 65,536 is NOT chosen here — it is starter-kit/methodology_trim.py:69
  `DEFAULT_BUDGET_BYTES`"*) and the comment at `bin/check-handoff:596` (*"still the trigger
  `methodology_trim.py` keys on"*). That is Learning #28's shape — repairing a defect falsifies the
  records that described it — so the repair is part of this session's scope, not left to be found.
- **One argument in the plan's §5 does not survive re-derivation, and it argued against the option
  chosen.** *"the number BL-9/BL-32/BL-36/S87/S89 have all measured against"* is **impossible for
  BL-9**: BL-9 closed **2026-08-01** and `DEFAULT_BUDGET_BYTES` was first written **2026-08-03**
  (`df381ea`, S36). The relation is the reverse — design §5.4 calibrates the constant on three
  sizes, and 52,927 B is BL-9's own L1 output commit `7a71df0`, so **BL-9 is the constant's input,
  not a measurement against it.** Only BL-9 was re-derived; the other four names are **not**
  re-checked and are not claimed either way. The sentence originates in `.context-budget.json`'s
  `_` key and the plan inherited it.

### 2026-08-26 · [BL-51] S116 claim — Phase C2: the Class A trigger, bundled with `DEFAULT_BUDGET_BYTES`

- **Model:** Claude Opus 5 (1M context).
- Phase 1B claim. Deliverable: **Phase C2** of [`read-cap-phase-c-plan.md`](docs/planning/read-cap-phase-c-plan.md)
  §9 — option **A2** (the Class A fire/stop pair) shipped in **one commit** with option **C1**
  (`DEFAULT_BUDGET_BYTES`), which §8 requires be bundled and §10 dragon 1 explains: `Trigger.fires`
  is `read_fires or byte_fires`, and the 65,536 B byte arm fires first, so **A2 alone ships a
  trigger that can never fire.**
- Authorized by the operator at this claim. The plan itself was **RATIFIED 2026-08-26** at S115's
  claim; that ratification approved §8's sequence but authorized **only Phase C1**, so C2 needed
  its own go-ahead and now has it. **Phase C3 stays unstarted.**
- **TWO DECISIONS BELONG TO THE OPERATOR AND ARE NOT DERIVABLE FROM THE PLAN.** Both are put to
  them with measured evidence **before any carrier is edited**, and whichever way each falls is
  recorded here as its own ledger entry:
  1. **Option C1's disposition** — retire `DEFAULT_BUDGET_BYTES`, raise it, or keep it and accept
     A2 is inert. §5 states the evidence on both sides and §7's C1 row says plainly
     *"Judgment, not derivation"*; the plan closes the point with *"This plan does not decide it."*
     Retiring it orphans the baseline BL-9/BL-32/BL-36/S87/S89 all measured against.
  2. **The C2 hole**, fenced at the plan's top by S115 and not resolved there. §6's inventory puts
     option A1's **per-class dashboard thresholds** at `starter-kit/methodology_dashboard.py:3045-3072`,
     but §9's Phase C2 DONE criterion names only `--check`, `choose_cut` and `READ_REFUSE_BYTES` —
     all **trimmer**-side. Those risk rows fall between C2's and C3's criteria and are owned by
     **neither phase**. The operator either widens C2's criterion or raises a fourth phase.
- **Carriers are DISTRIBUTED** — `starter-kit/methodology_trim.py` and
  `starter-kit/methodology_dashboard.py` are both TRACKED manifest SOURCEs (the dashboard with a
  byte-identical `tools/` twin), so this reaches every adopter at their next `bin/sync`. To be
  re-derived off the manifest's **SOURCE** column at close-out, never by grepping a bare filename.
- **State at claim, recorded because §10 dragon 8 says a successor will misread it:** `CHANGELOG.md`
  (81,070 B) and `HANDOFFS.md` (111,388 B) are over both ceilings **by adjudication, not neglect**;
  `context_budget.py` exits **2** and `methodology_trim.py --check` **FIRES** on both. That is the
  expected state. **This session does not trim them.**
- **Not in scope:** the prefix invariant (A3), the Class B remedy and `BOOTSTRAP.md` (B1/B2),
  `RECORD_BUDGET_BYTES` and the record-budget campaign, `HEADER_RESERVE_BYTES`, Test 34's retention
  floor, BL-42/43/44/46/47/48/49, issue #75's unsent PR, and **any outward-facing action whatsoever.**

### 2026-08-26 · [BL-51] S115 — Phase C1: the read-cap population split into two classes, pinned to the trimmer

- **Model:** Claude Opus 5 (1M context).
- **Phase C1 of [`read-cap-phase-c-plan.md`](docs/planning/read-cap-phase-c-plan.md) §9, complete.**
  `READ_CAP_WATCHED`'s six names become **Class A** (`CHANGELOG.md`, `HANDOFFS.md` — the trimmer has
  a `LEDGERS` entry) and **Class B** (`SESSION_NOTES.md` + three `BACKLOG.md` locations — the trimmer
  answers `NO_CONFIG`). Both classes are **declared literals**; `READ_CAP_WATCHED` is **derived** from
  their union, so *"the population did not change"* is provable rather than asserted. New public
  `read_cap_class(rel_posix)` → `"A"` / `"B"` / `None`.
- **It changes no behaviour, and that is measured, not argued.** The pre-change module (`git show
  HEAD:tools/methodology_dashboard.py`) and the post-change module were both run against the same
  live tree: watched rows, trim ledger rows, trim signals, **all** risk rows and the health total are
  **identical**, with a control confirming the two modules really differ. Phase C1 is deliberately
  fleet-invisible; §7's A1 row promises otherwise and §§8–9 do not — see the plan's new note.
- **Dragon 6 is satisfied by DECLARING the class, not deriving it.** Deriving class from `LEDGERS`
  would let a widened trimmer silently reassign a file. `test_class_a_is_pinned_to_the_trimmers_ledgers_table`
  fails instead — that is §9's second DONE criterion.
- **The two `docs/**` backlog locations: KEPT, decided on evidence** (§9's third criterion).
  Neither is named as a file to read in `SESSION_RUNNER.md` or `SAFEGUARDS.md`; across the whole
  22-file distributed `.md` corpus `docs/BACKLOG.md` appears **0** times and `docs/planning/BACKLOG.md`
  **once**, in Learning #26 as a worked example. Kept for §7's reason for rejecting option D — the row
  reports a real property — and because keeping costs nothing measurable: `docs/BACKLOG.md` matches no
  file in the fleet, `docs/planning/BACKLOG.md` matches only this repo's, at 0.54× the cap. A canonical
  test pins the "no protocol basis" half so the reasoning cannot quietly go stale.
- **`DASHBOARD_VERSION` 2.16.0 → 2.16.1.** Not cosmetic: `check_stale_version()` (`:928`) compares an
  adopter copy's constant against the canonical's and warns only when the canonical is **newer**, so
  without a bump every synced adopter would run diverged content and be told nothing. (`bin/status`
  is unaffected either way — it keys on a content blob SHA, `bin/status:95-98`. A review finding and
  its refutation both named that tool; the real consequence runs through the other one.)
- **10 new canonical tests, 12-mutant round, 12/12 killed**, each verified to APPLY, both twins mutated
  together, control green before and after, every restore `cmp`-verified.
- **A review found a defect in text this session shipped into a DISTRIBUTED file, and it is fixed.**
  The Class B warrant said flatly *"there is no record ordering that puts the needed part at the top"*
  — false of `SESSION_NOTES.md`, whose `ACTIVE TASK` the runner puts at the top. The plan's own wording
  is *"no record ordering that **guarantees** that"*; the qualifier had been dropped. Restored, with the
  fleet measured **first-hand** (11 repos: offsets 132–23,013, inside the cap in all 10 that have the
  heading; `mts-system` has **no** such heading at all — a fact the review's 6-repo sample missed).
- **Learning #43** appended (1,498 B): *deriving a set from its own parts is usually right, and it
  disarms the assertion that those parts still cover it.* Earned in-session — the first mutation round
  scored 8/10 and both survivors traced to one tautological line.
- **Carve-out, re-derived off `bin/_manifest.py`'s SOURCE column:** `starter-kit/methodology_dashboard.py`
  is **TRACKED/distributed** → reaches every adopter at their next `bin/sync`;
  `starter-kit/FRAMEWORK_LEARNINGS.md` is a **SOURCE** too → Learning #43 ships with it.
  `tools/methodology_dashboard.py` and `tools/test_methodology_dashboard.py` are **canonical-only**.
- **Verification:** `bin/tests.sh` **287 rows, 286 passed / 1 failed / 0 skipped**, row-for-row against
  a worktree control at `757fed2` — **0 status flips**, exactly one row differs and it is a derived
  count this session's own Learning #43 moved (`#43`→`#44`). Sole failure both sides by name:
  `github source dry-run failed` (Test 9's standing `--source=github` 404). Python suites **111 / 313 /
  42 OK** from a foreign CWD. `check-links` OK (88/22) · `check-learnings` OK (42 rows, 1..42, 0 over
  budget). Twins byte-identical, **mirrored last**. `context_budget.py` exit **2** — `CHANGELOG.md` and
  `HANDOFFS.md` only, both adjudicated (BL-52), expected.
- **Commits:** `757fed2` (1B claim + the ratification) + **`596a602`** (the deliverable) + this close-out.
- **NOT DONE, each deliberately:** every threshold (Phase C2 / option C1 `DEFAULT_BUDGET_BYTES`), the
  prefix invariant (A3), the Class B remedy and `BOOTSTRAP.md` (B1/B2), `RECORD_BUDGET_BYTES`,
  BL-42/43/44/46/47/48/49, issue #75's unsent PR, **any outward-facing action**. Nothing pushed.

### 2026-08-26 · [BL-51] S115 claim — Phase C1 of the read-cap correction: split the watched population by class

- **Model:** Claude Opus 5 (1M context).
- Phase 1B claim. Deliverable: **Phase C1** of [`read-cap-phase-c-plan.md`](docs/planning/read-cap-phase-c-plan.md)
  §9 — `READ_CAP_WATCHED` becomes class-aware, with membership **declared** in
  `starter-kit/methodology_dashboard.py` and **pinned by a canonical test** against
  `starter-kit/methodology_trim.py`'s `LEDGERS` table.
- **THIS PHASE CHANGES NO THRESHOLD.** §8 states A1 *"changes no threshold and cannot degenerate
  anything"* and §9's Phase C1 criterion names none; §7's A1 mechanism cell, which reads as if two
  thresholds move, is the summary that drifted. The threshold move is **Phase C2** (option A2),
  which §8 requires be bundled with option C1 (`DEFAULT_BUDGET_BYTES`) or it is inert.
- **The class must be DECLARED, not derived from the trimmer.** §10 dragon 6 requires that widening
  `LEDGERS` **fail** rather than silently reassign a file's class, and §9's DONE criterion asks for
  a test that fails when a name is added to `LEDGERS` without moving class. Deriving the class
  would satisfy neither. The model is the existing `test_grammars_agree_with_the_trimmer_config_table`.
- **Carriers are DISTRIBUTED** — `starter-kit/methodology_dashboard.py` is a TRACKED manifest
  SOURCE, with a byte-identical `tools/` twin — so this reaches every adopter at their next
  `bin/sync`. To be re-derived off the manifest's SOURCE column at close-out.
- **Not in scope:** every threshold, the Class A fire/stop pair, the prefix invariant (A3), the
  Class B remedy and `BOOTSTRAP.md` (B1/B2), `RECORD_BUDGET_BYTES`, BL-42/43/44/46/47/48/49,
  issue #75's unsent PR, and **any outward-facing action**.

### 2026-08-26 · [BL-51] Phase C plan RATIFIED — §8's three-session sequence approved, Phase C1 authorized

- **Model:** Claude Opus 5 (1M context).
- Non-commit **operator decision**, recorded per FM #27. S113 wrote
  [`read-cap-phase-c-plan.md`](docs/planning/read-cap-phase-c-plan.md) as a DRAFT awaiting
  ratification (`9a71c8e`); the operator ratified it at S115's Orient, selecting it over the
  record-budget campaign and over issue #75's unsent PR.
- **What was approved:** §8's recommendation `A1 → (A2 + C1 together) → A3 → (B1 + B2)`, as **three
  sessions**. **Phase C1 alone is authorized as S115's deliverable.** Phases C2 and C3 stay
  unstarted and are **not** authorized by this ratification.
- **What was NOT approved, and is not implied:** any outward-facing action. The plan's own Scope
  line already says so; the ratification does not relax it. The carriers are distributed, so the
  eventual upstream landing batches with BL-46(2)/47/48/49 — and still needs an explicit go-ahead,
  each time.
- The plan's Status line was rewritten in place from DRAFT to RATIFIED, and **two ambiguities a
  successor would otherwise have hit were fenced in the same edit**: `C1` names both an option
  (§7, `DEFAULT_BUDGET_BYTES`) and a phase (§9, the class split, which is option A1), so §9's
  *"Do: A2 and C1 in one commit"* means the **option**; and §7's A1 row reads as if Phase C1 moves
  two thresholds when §8 and §9 both say it moves none.

### 2026-08-26 · [BL-45] S114 — the learnings ceiling re-derived, and five sessions of owed learnings written

**BL-45 CLOSED** by the operator's choice of option (b) from four costed alternatives.
`starter-kit/FRAMEWORK_LEARNINGS.md`'s ceiling **65,536 → 73,728 B (72 KiB)**, and the backlog it had
been blocking is discharged: **rows #39–#42**, 968–1,148 B each, all inside the 1,500 B row budget.
The file is **69,683 B against 73,728 — `ok`**, and `context_budget.py` no longer reports it over.
**Canonical-only:** the distributed seed declares `CLAUDE.md`, `SESSION_NOTES.md`, `LEARNINGS.md` and
**not** this file. *(The rows themselves are a different matter — `FRAMEWORK_LEARNINGS.md` **is** a
manifest source, so #39–#42 reach every adopter at their next `bin/sync`.)*

**The number was re-derived, and the old one's justification was wrong twice.** 65,536 was borrowed
from the ledgers' `DEFAULT_BUDGET_BYTES`; the note defending it converted bytes to tokens at
`bytes_per_token` 2.80 and compared the result to an **opening-context** floor. That estimator
answers a different question, and the limit that bites a read is the **25,000-token Read cap**. Its
arithmetic gave 23,406 tok for a 65,536 B file where the measured figure is **21,623** — 8% over, in
the direction that made the ceiling look tighter than it was.

**Measured three times, including after the write** — x2 = 43,247 tok, x3 = 64,868 against 64,870
predicted (**linear to 0.004%**), giving **3.0300 B/token** and a cliff at **75,751 B**; re-measured
after appending the four rows, **3.0396**, so the margin held. **73,728 is deliberately 2,023 B under
that cliff**: a ceiling must sit below where the file stops fitting, not on it, and this is the value
at which the file stays inside one read even if every future byte is 20% denser. The margin is
judgment and is labelled as such in the config note.

**What it buys, and what it does not.** 8,192 B gained, 4,159 B spent on the owed rows, **~3 rows
left**. The 37 pre-existing rows are 97% of the file and may not be edited, so the untouchable
remainder **is** the file — **Learning #26's own shape, arriving in the file that records it**. The
question underneath is policy, not arithmetic. BL-45's other three options stay open and are now
**costed in the item** so nobody re-derives them.

**A correction to BL-45's own text, left standing per FM #17.** It warns that archiving breaks every
citation to a row. The checker's sweep covers the **distributed corpus only** — **8 citations to 5
rows across 4 files**, not the 471 overall — so archiving the oldest **5** rows would orphan
**none**, and the oldest **10** just **five, in two files**.

**Verification.** `bin/tests.sh` **287 rows, 286 / 1 / 0**, zero status flips, zero skips, sole
failure by name Test 9's standing `--source=github` 404. **Test 37 was watched specifically** — it
copies the live learnings file as its fixture, so four new rows enter its population; 9 assertions,
4 mutants, green. Python suites **111 / 303 / 42 OK**. `check-learnings` OK — **41 rows, contiguous
1..41** (`#14` remains deliberately reserved), 4 unfrozen, 0 over budget. `check-links` OK (88/22),
`check-handoff` + `--all` OK, `BACKLOG-DETAIL` verify OK, twins byte-identical and untouched.
`context_budget.py` exits **2**, and the composition is the point: the learnings file is now `ok`;
the two remaining breaches are `CHANGELOG.md` and `HANDOFFS.md`, **both adjudicated** (BL-52 third
addendum) — do not trim either on sight.

**Model:** Claude Opus 5 (1M context).


### 2026-08-26 · [BL-45] S114 claim — raise the learnings ceiling to the file's real one-read limit

`CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in
[`HANDOFFS.md`](HANDOFFS.md). **Operator's decision**, taken from four costed options: raise the
ceiling rather than archive, compact or split. **One deliverable in two halves** — the raise is only
worth making because Phase 3C has been blocked for five sessions, so the owed learnings are written
in the same session or the defect survives the fix.

**Canonical-only, checked rather than assumed:** `.context-budget.json` governs this file; the
distributed seed declares only `CLAUDE.md`, `SESSION_NOTES.md` and `LEARNINGS.md`. **No adopter is
affected.**

**The number will be re-derived, not carried.** 65,536 was borrowed from the ledgers'
`DEFAULT_BUDGET_BYTES`, and the note defending it converts bytes to tokens at `bytes_per_token`
2.80 — an estimator S112 measured as wrong for this purpose. S97's own note invited the re-opening:
*"Re-open that choice when the four rows are spent, not before."* They are spent.

**Model:** Claude Opus 5 (1M context).


### 2026-08-26 · [BL-51] S113 — Phase C planned: what each guard watches, and what it claims; self-score 8/10

Commits `f06b6f7` (claim) and **`9a71c8e`** (the deliverable),
[`docs/planning/read-cap-phase-c-plan.md`](docs/planning/read-cap-phase-c-plan.md), **DRAFT awaiting
ratification**. A planning session: **nothing implemented, no numeral moved** (FM #18/#19). The
predecessor plan's Phase C stub is **annotated in place** to point here.

**The operator's proposal, answered.** *"Only worry about the 256 KB limit for trimming"* is **right
for the two ledgers the trimmer can act on and wrong as a blanket rule.** The six watched names are
**two classes**, evidenced per name off two independent facts — membership of the trimmer's `LEDGERS`
table, and what `SESSION_RUNNER.md` actually instructs. **Class A** (`CHANGELOG.md`, `HANDOFFS.md`):
records, newest-on-top, read by frontier and one record; 9 files, 8 over the cap. **Class B**
(`SESSION_NOTES.md`, three `BACKLOG.md` locations): prose, no delimiter, **read in full**; the
trimmer refuses them by design; **9 files, seven over the cap**. Truncation is only harmless when the
part you need is at the top, and a backlog's bottom items are as live as its top ones.

**The finding the plan did not go looking for and could not avoid: Class B has no reachable remedy.**
`SESSION_NOTES.md` has **none documented anywhere in the distributed corpus**. `BACKLOG.md` has one —
`BOOTSTRAP.md:144-151` — and **Learning #26, earned on this repo's own backlog at S89, proves it
insufficient in general**: archiving everything finished recovered 33% and still left the file at
1.40× its yardstick, because the **open** items alone exceeded it. The remedy that actually worked
here (index + detail split with a runnable losslessness proof) is **fork-only**. **A guard whose
remedy cannot reach is the misdirection [`ledger-trimmer-design.md`](docs/planning/ledger-trimmer-design.md)
§7.3 exists to prevent, and it is shipping.**

**And the proposal is inert without a second decision.** `Trigger.fires` is `read_fires or
byte_fires`, so a 256 KB read trigger changes nothing while `DEFAULT_BUDGET_BYTES` = 65,536 fires
first — **Phase B's §3 coupling recurring one level over.** The plan requires the two ship in the same
session and **deliberately does not decide the second**, laying out the evidence both ways and marking
it a decision rather than a derivation.

**A correction the plan makes to its own first draft, recorded because it is this campaign's lesson
landing on the plan that states it.** Class B's *"× the cap"* column was drafted by carrying a
**Class A** ratio (2.4 B/token, measured on ledger content) onto Class B files. Measured directly,
Class B is **less** dense — 2.5472–2.9096 against Class A's 2.2705–2.5150 — so the draft
**overstated every multiple by 6–20%**, in the direction that flattered the argument. The finding is
unchanged; the numbers were wrong. Corrected before ratification.

**Verification.** No code changed, and the suites were run to prove exactly that: `bin/tests.sh`
**287 rows, 286 / 1 / 0**, sole failure by name Test 9's standing `--source=github` 404 — identical in
shape to S112's control. Python suites **111 / 303 / 42 OK** from a foreign CWD. `check-links` OK
(88/22), `check-learnings` OK (37), `check-handoff` + `--all` OK, `BACKLOG-DETAIL` verify OK (C1–C5),
twins byte-identical and untouched. **20 of 20 load-bearing citations machine-verified** by re-reading
the cited line. `context_budget.py` exits **2**, expected — `HANDOFFS.md` is over its ceiling **by
adjudication, not neglect** (BL-52 third addendum); do not trim it on sight.

**BL-45 now blocks Phase 3C for a fifth consecutive session** — `starter-kit/FRAMEWORK_LEARNINGS.md`
is 16 B from its ceiling and four learnings are earned and unwritten across S112–S113. It is the
longest-standing unaddressed blocker here and needs an operator decision.

**Model:** Claude Opus 5 (1M context).


### 2026-08-26 · [ad hoc] S113 claim — plan Phase C of the read-cap correction

`CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in
[`HANDOFFS.md`](HANDOFFS.md). **A planning session: the plan is the deliverable, nothing is
implemented** (FM #18/#19). Origin: the operator's proposal at S112's close-out — *only worry about
the 256 KB limit for trimming*. That is right for the two ledgers the trimmer can act on and wrong as
a blanket rule, because the six watched names are **two classes**, and the four the trimmer refuses
are the ones the protocol genuinely reads in full. Phase C therefore grows from *"two rows or one"*
into **what population and what claim each guard carries** — and must decide `DEFAULT_BUDGET_BYTES`,
which fires first and would render a 256 KB trigger inert.

**Not in scope:** implementing any of it, `RECORD_BUDGET_BYTES`, BL-45, issue #75's unsent PR, the
§11.2 adopter remediation, **and any outward-facing action**.

**Model:** Claude Opus 5 (1M context).


### 2026-08-26 · [BL-52] S112 close-out — the trim was DECLINED on evidence; self-score 7/10, predecessor S111 scored 8/10

Phase 3D receipt in [`HANDOFFS.md`](HANDOFFS.md), **12,288 B inside the 12,288 B per-record budget**
— four trim passes, and `bin/check-handoff` was **run** rather than predicted each time (it counts
the opening fence through the **next** opening fence, trailing prose included).

**A trim was due as close-out housekeeping and was not performed, and that is the entry.**
`methodology_trim.py` refused it (`[SRF_RED]` 1.1198). This session was about to `--force` past the
refusal, **not having asked BL-52's own question** — whether the trim remedies anything. Asked, and
measured by the free over-cap error path: a whole-file read of the untrimmed ledger delivers the
front matter and the **four newest receipts** (55,342 B = **23,370 tok measured**, against 23,409
predicted; the five-receipt prefix is **28,611 tok**, over). The cut on offer would have archived
**S108 and S107 — both already outside the delivered prefix.** Phase 3A reads **one** receipt;
Phase 0 step 6 takes the frontier from `git log` and **greps**; whole-file reads run **1 in 85**.
The context-tax claim does not rescue it either: that cost is per read-span and is already guarded
per record by `RECORD_BUDGET_BYTES`. **The tool's refusal was right for a stronger reason than it
gave** — it diagnosed a level remedy on a rate problem; the measurement adds that the level is not
costing anything yet.

**Deliberately left red, and it is a finding rather than an oversight:** `context_budget.py` exits
**2 (BREACH)** and this repo's own dashboard carries **one high-severity read-cap row**, both on
`HANDOFFS.md`. Both are literally true and, on this measurement, not worth acting on — **a guard can
be correct and not worth acting on**, which enlarges Phase C's question from *two rows or one* to
*what population and what claim each row carries*. The threshold that will actually bite is
`READ_REFUSE_BYTES` = **262,144 B**, roughly **16 sessions** out, where the front matter itself stops
being delivered; the remedy between here and there is
[`record-budget-reduction-plan.md`](docs/planning/record-budget-reduction-plan.md) Phase 2/3.

**Sizes, measured last — and this entry moved one of them, which is worth recording rather than
hiding.** `HANDOFFS.md` **77,238 B / 305 ln**, over its 65,536 B ceiling, declined above.
`CHANGELOG.md` was **58,843 B / 807 ln** before this entry; adding it takes the file to **61,574 B**,
which crosses the new **56,750 B** one-read cap, so **its read arm now fires too.** Measured before
asserting anything about it: at this file's own density it is **24,530 tokens — still inside the
25,000 cap by 470.** So the firing is **early, not wrong**: `MIN_BYTES_PER_TOKEN` is deliberately the
measured *floor* (2.27) rather than this content's 2.51, because a guard that must not stay silent
on a truncating file has to assume the densest content it will meet. The cost of that choice, now
quantified on a real file: it fires about **9.6% early** here (56,750 B against a true cliff near
62,754 B). **That is the designed trade, stated with its price rather than discovered later.**
**And the margin is closing, so do not inherit the word "early":** this file is now within a few
hundred bytes of its own measured cliff, and the next close-out will take it past. Re-run the
doubling probe (concatenate the file with itself, `Read` it with a spanning `limit`, halve the
reported token count) rather than trusting either figure here — the *threshold vs cliff* ratio is a
property of the content type and holds; the file's position against it does not.
`starter-kit/FRAMEWORK_LEARNINGS.md` **65,520 B, 16 B free** — **BL-45 blocked Phase 3C for a fourth
consecutive session**; three learnings are earned and unwritten. `main` is **77 ahead of
`origin/main`**; nothing pushed, no outward-facing action taken.

**Model:** Claude Opus 5 (1M context).


### 2026-08-26 · [BL-51] S112 — Phase B shipped: the read cap is re-denominated onto bytes, and the line rate is deleted

Commits `9e71f83` (the deliverable) and `b5c1357` (the record). Scope was the operator's **"B-min"**
at Phase 1: re-denominate, delete the line rate, rename J3, correct the false justification — and
present the design before any distributed constant moved.

**`READ_CAP_LINES = 2000` is gone from both distributed tools.** In its place, derived at import so
that no opaque boundary is published: `READ_CAP_TOKENS = 25_000` (stated verbatim by the tool's own
error) × `MIN_BYTES_PER_TOKEN = 2.27` (the measured **floor** of 2.2705–3.0300 over nine real
markdown files in five repos) = **`READ_CAP_BYTES` 56,750 B**. Plus a second measured boundary,
`READ_REFUSE_BYTES = 262,144`.

**The axis change is a dominance result, not a calibration argument.** Over 18 watched ledgers in 5
repos the 2,000-line threshold fires on **3** and stays silent on **8** that a byte threshold at
*any* point in the measured band catches — and it catches **nothing** a byte threshold misses.
B/line spread over that population is **8.6×**; B/token is **1.33×**. Measured on the file that
motivated it: this repo's own `HANDOFFS.md` is **29,300 tokens, 1.17× the cap, truncating today**,
and the shipped guard reported no risk because it is 268 lines.

**A third delivery mode nobody had costed.** Past **262,144 B** a default `Read` is **refused
outright with zero content** — `File content (256.1KB) exceeds maximum allowed size (256KB)` — not
truncated. So *"truncation is ordered top-down, so the front matter still arrives"* holds only
**between** the two boundaries. **Five of the eighteen** fleet ledgers are already past it. It gets
its own risk row and its own edge test: a different failure, not a worse degree of one.

**`LINE_FIRE_BELOW`/`LINE_STOP_ABOVE` were removed, not re-tuned.** The plan's §3 said a *corrected*
cap degenerates the rule; measured, it is degenerate at **every** honest cap. A one-read
`CHANGELOG.md` holds **20.9** records and a one-read `HANDOFFS.md` **4.3**, against a rule demanding
**30** of headroom — satisfiable only because 2,000 lines granted them 2.32× and 8.75× more capacity
than a real read. [`ledger-trimmer-design.md`](docs/planning/ledger-trimmer-design.md) §5.2 already
held the reason: units-of-headroom is well-formed only while the cap *"sits far above normal
operating size"*, and at operating size it prescribes *"a level with hysteresis, not a rate — the
form that terminates"*. Removal was the design's own prescription. Recomputed through the shipped
code, `stops()` is satisfiable at **k ∈ [8..1]** for `CHANGELOG.md` and **[2,1]** for `HANDOFFS.md`
— a real cut exists for both, where every corrected *line* cap gave nothing for either.

**A second distributed copy of the rate rule was found and removed** — `TRIM_LINE_FIRE_BELOW` in
`methodology_dashboard.py`, absent from every plan, backlog and ledger text — along with its
reimplementation `trim_line_headroom()`. **J3 keeps its value under its own name**
(`SEED_PLAUSIBLE_MAX_LINES = 2000`): it asks whether a file is plausibly a fresh seed, which has
nothing to do with truncation, and sharing the name meant a correction made for the reporter's
reasons would silently widen a **refusal** population.

**`READ_CAP_WATCHED`'s justification is corrected; the set is unchanged.** It claimed the two
ledgers are read *in full* at Phase 0 step 6. `SESSION_RUNNER.md:37` **is** step 6 and is
frontier-based on `git log`. Re-derived over **85 transcripts**, each root ledger is read whole
**once** and in part **1,696 / 1,797** times. Narrowing the population is fleet-visible and is
sequenced after this (Phase C / BL-52).

**Fleet effect, measured read-only against all four adopters plus this repo:** read-cap risk rows
**3 → 14**, spreading from one repo to five, five of them the zero-content refusal. No adopter file
was written; `collect_all` reaches no writer, verified by call-graph.

Versions, both **minor**: trim `1.3.0 → 1.4.0` (CLI finding codes change), dashboard
`2.15.2 → 2.16.0`.

**The surface cannot enforce the property under test, and that is stated rather than implied.**
`bin/tests.sh` 287 rows both sides, **286 passed / 1 failed / 0 skipped, zero rows lost, gained or
flipped**; sole failure by name on both sides is Test 9's standing `--source=github` 404. Python
suites **111 / 302 / 42** OK (was 110 / 300 / 41). Twins byte-identical, mirrored last. **No test in
this repository can falsify a read-cap claim** — nothing here invokes the agent's `Read` tool — so a
green suite is evidence that nothing *else* broke. Appendix A was re-run first-hand this session.

**Not done, each deliberately:** Phase C, option D, narrowing `READ_CAP_WATCHED`,
`DEFAULT_BUDGET_BYTES`, the prefix guard (measured this session and handed to Phase C in plan
§12.4), `RECORD_BUDGET_BYTES`, BL-45, issue #75's unsent PR, and **any outward-facing action**.

**Model:** Claude Opus 5 (1M context).


### 2026-08-26 · [ad hoc] S112 claim — Phase B of the read-cap premise correction

`CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in
[`HANDOFFS.md`](HANDOFFS.md). **Operator's decision at Phase 1: take Phase B as ratified, but settle
BL-52's precondition question inside it, as act 1.** The two are one question — `methodology_dashboard.py:295`
justifies watching the two ledgers by crediting Phase 0 step 6 with a whole-file read, and
`starter-kit/SESSION_RUNNER.md:37`, which *is* step 6, reads `git log`. Whether the guard should be
**re-denominated**, **narrowed**, or **removed** for those two files cannot be answered without it,
and this session's own Phase 0 read neither ledger whole.

**The design is presented for approval before any distributed constant moves** — the operator's gate,
recorded at claim. `LINE_FIRE_BELOW`/`LINE_STOP_ABOVE` must be re-derived in the **same commit** as
any cap change ([plan §3](docs/planning/read-cap-premise-correction-plan.md)): `choose_cut` falls
through to `return 1`, so a corrected cap alone ships a trim that retains **one** record to every
adopter, with every test green.

**Not in scope, each deliberately:** Phase C, option D as a decision, the 65,536 B ceiling,
`RECORD_BUDGET_BYTES`, BL-42/43/44, **BL-45**, BL-46(2)/47/48/49, BL-50, issue #75's unsent PR, the
cross-repo §11.2 adopter remediation, **and any outward-facing action**.

**Known at claim, measured:** `HANDOFFS.md` 64,977 B against 65,536 B — **559 B clear**, both trim
triggers silent. The trim this session is close-out housekeeping (FM #26), due because this
session's own receipt breaches, not because the trigger fired.

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [BL-52] Post-close-out addendum: the read-cap premise's PRECONDITION fails for the two ledgers

**Recorded after S111's close-out, at the operator's direction, and logged here so Phase 0's
reconcile finds a ledger entry rather than a gap.** The S111 receipt in `HANDOFFS.md` names its own
commits and is left as written; this is a separate action.

**The finding.** `starter-kit/methodology_dashboard.py:295` justifies `READ_CAP_WATCHED` (`:311`) as
*"the files a session is instructed to read **IN FULL** to establish state"*, citing
`SESSION_RUNNER.md` Phase 0 **step 6** for `CHANGELOG.md` and `HANDOFFS.md`. But step 6
(`SESSION_RUNNER.md:37`) is **frontier-based** — `git log -1 --format=%H -- CHANGELOG.md`, then the
commits after it. **It reads git history, not the file.** Phase 3A reads **one receipt**, not the
ledger.

**The premise holds for three of the five watched names and fails for exactly the two the trimmer
exists to bound.** Steps 1–3 genuinely do say *read*. Step 6 does not. The comment's
SEED-vs-TRACKED population logic is careful and is **not** what is wrong; the sentence saying why the
two ledgers are in the set is.

**Observed:** S111's own Phase 0 followed step 6 exactly and never read `CHANGELOG.md` whole.

**It strengthens BL-52 without settling it.** The missing measurement is how often anything reads
these files whole — put near 1-in-81 by an earlier session, **not re-run**, and a count of exactly
this kind was once wrong by **13×**. Re-derive before using. Says nothing about the byte metric.

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [ad hoc] S111 close-out — Phase A shipped; self-score 8/10, predecessor S110 scored 8/10

Phase 3D receipt in [`HANDOFFS.md`](HANDOFFS.md), **inside the 12,288 B per-record budget** — over by
546 B on the first pass and cut from the **trailing prose**, which is where `bin/check-handoff` says
to cut, because a record is the opening fence through the **next** opening fence. Commits: `d5a4fb4`
(claim) · `730a309` (trim) · **`84abc60` / `86037bd` / `85a2158`** (Phase A) · `b8ecccf` · `979dc73` ·
`90d9b76` · this close-out.

**Phase A is complete and the plan is RATIFIED.** Six distributed carriers corrected — **3 `TRACKED`**
(reach every existing adopter at their next `bin/sync`) and **2 `SEED`** (future adopters only).
**No numeral moved.** Phases B and C are not started.

**Three findings, each from running rather than reading.**

**Dragon 8 settled, and the plan's own test could not have settled it.** An explicit `limit` spanning
an over-cap region **neither bypasses the cap nor truncates — it errors and returns no content at
all.** Three delivery modes, not two. Probe D's "returned whole" is therefore not an artifact.

**Phase A's DONE criterion was unsatisfiable as written** — it matches a live, distributed, *correct*
sentence about `$(...)`. The corrected command returns **0** (§11.3).

**I shipped a benefit claim I had not established, and an operator relay caught it.** Replacing
*"protects against silent truncation"* with *"protects against an unread tail"* substituted one
unverified benefit for another — the exact move Phase A exists to stop. Corrected in the seeds **and**
in the two TRACKED tools; **BL-52** raised, then narrowed by measuring that the argument is
**regime-dependent** and does not reach this repo.

**Verification.** Control 287 rows **286 / 1 / 0**; after **286 / 1 / 0**; row-for-row, both
populations asserted non-empty: **zero status flips, zero skipped**, one pair differing only in a
derived count this session's trim moved. Sole failure both sides by name: `github source dry-run
failed`. Python suites **300 / 110 / 41 OK**, re-run **after** the mirror. Twins `diff -q`
byte-identical. Trim losslessness three ways including an independent inverter: **12/12
byte-identical, 0 lost, 0 unexplained.** `check-links` OK (88/22) · `check-learnings` OK (37) ·
`check-handoff` + `--all` OK · `trim --check` silent on both · `BACKLOG-DETAIL.md.verify.sh` OK.

**The surface cannot enforce the property under test, and that is stated rather than glossed:** no
test here can invoke the agent's `Read` tool. A green suite proves nothing *else* broke — Appendix A
is the only instrument, and it must be re-run every phase.

**FM #28 gate, measured after the last write.** `HANDOFFS.md` **64,977 B** / 225 ln;
`CHANGELOG.md` **47,207 B** *before this entry*; `starter-kit/FRAMEWORK_LEARNINGS.md`
65,520 B (**16 B free — BL-45 still blocks Phase 3C, third session running**);
`docs/planning/BACKLOG.md` 30,915 B. **`main` 69 ahead of `origin/main`, nothing pushed.**

**Carve-out re-derived by importing `DISTRIBUTION` and reading the SOURCE column:** 3 TRACKED,
2 SEED, 10 canonical. **No outward-facing action.**

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [BL-52] S111 — the relayed critique measured: it is regime-dependent, and this repo is in the other regime

**BL-52 addendum.** The critique's load-bearing premise — *"the tail costs nothing, because nothing
reads it"* — is true **only once a file is already well past the cap**. Below it the whole file is
delivered and every byte is paid for; **at** the boundary, a trim moves a file from *truncated* to
*fully delivered*, which is not cosmetic.

Measured by the free error path (an over-cap `limit` reports the span's token count and returns no
content): this file was **26,723 tokens before this session's trim — OVER the 25,000 cap** `[M]`, and
is ~18,800 after `[D]`. **This repo's ledgers hover at the cap boundary**; the relaying repo's is
reported at 25,578 lines, ~**40×** the cap `[C]`. Their conclusion may be right for them and **does
not transfer here** — the same failure shape this repo keeps recording, a figure measured in one
regime carried into another.

**So the trim run earlier in this session did real work on both axes**, which I could not have
asserted when I ran it: I ran it because the ceiling forced it, and only measured afterwards that the
file had actually been over the read cap too.

**BL-52's scope narrowed accordingly:** what is in question is the **line metric's remedy**. The byte
metric is **not**, and BL-52 must not be closed by retiring both.

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [BL-52] S111 — BL-52 raised; the design record annotated; the plan RATIFIED and Phase A closed

**The plan's status moves `DRAFT` → `RATIFIED`** (operator, this session's Phase 1: A → B → C as
three separate sessions; the one-pass fix stays declined, option D stays deferred-on-evidence).
**Phase A is shipped; B and C are not started.** A new **§11** records what shipped, what existing
adopters still need by hand, and two findings Phase A produced that the plan did not anticipate.

**§5.4 settled and executed:** *leave the design and audit records, annotate
[`ledger-trimmer-design.md`](docs/planning/ledger-trimmer-design.md) only* — it is the document a
future session reads to re-derive the rate rule, which is what earns it the annotation the others do
not get. Its false table cell is struck through in place, not rewritten (FM #22), with a block note
carrying the measurement, the reproduction, and both consequences.

**BL-52 raised** — *the line metric measures a condition trimming may not remedy.* From the critique
the operator relayed mid-session, but **argued from this session's own probes**: truncation is
ordered top-down, these ledgers are newest-on-top, so a cut removes records a whole-file read was not
delivering anyway. **Phase A did not fix this — it exposed it.** While truncation was believed
*silent*, trimming was the only way to avoid an undetectable gap and the rationale held; once it is
known to be **announced**, the rationale has to be re-argued rather than inherited.

**What BL-52 deliberately does NOT claim**, because S111 did not measure it: anything about the
**byte** metric (a different claim — context tax), and anything resembling *"stop trimming"*, which
is an operator decision with fleet-wide blast radius. The relayed figures are marked `[C]` — that
repo's, not re-run here.

**Measured here, since the same shape was asserted about this repo:** `CHANGELOG.md` front matter is
**14,295 B / 185 ln = 39% of the file** and is read first, so the front-matter point is directionally
right here too; `HANDOFFS.md` front matter is **6,362 B / 72 ln = 11%**, because **S109 already
shipped that compaction** — the relayed critique's option E, arrived at independently.

**Dragon 8 settled, and Appendix A's probe D found unsound as specified** — it names a file that
returns whole either way, so it cannot discriminate. §11.3 records the corrected form.
**Phase A's §8 DONE criterion found unsatisfiable as written** — one live, distributed, *correct*
sentence about `$(...)` matches it. §11.3 records the corrected command, which returns **0**.

**Verification.** `BACKLOG-DETAIL.md.verify.sh` **OK** — C1–C5 green, 18 items byte-identical,
BL-52 correctly reported as raised-since and **not** a finding.

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [ad hoc] S111 — the detector reworded rather than exempted, so it stays a zero-hit tripwire

Phase A's verify grep still returned one row after the corrections, and the row was **`README.md`
quoting the false phrase in order to disclose that it was false**. Quoting-to-correct is not
asserting — but a detector that returns a permanent row is a detector nobody will ever read again.

**S106's precedent applies and was followed** (§5.5): *rewrite the live sentence rather than exempt
it, keeping the zero-hit grep a live detector without falsifying history.* The disclosure stays and
now names the old claim without reproducing its exact words. **An exemption list would have retired
the detector instead** — which is the failure mode, not the fix.

`git grep -nE 'no (error|missing-data) marker|silently truncat' -- starter-kit bin tools README.md`
now returns **0 rows** across every live path, with one documented carve-out: eleven shipped
`.verify.sh` files and `starter-kit/methodology_trim.py` carry *"command substitution strips trailing
newlines, which silently truncates the LAST record"* — a **correct** sentence about `$(...)`, with no
connection to the read cap. **Repairing it would be a defect.**

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [ad hoc] S111 — Phase A (3 of 3): the same unearned-remedy caveat pushed into the two TRACKED tools

The correction made to the SEED tables in the entry below, carried into the two files that are
**`TRACKED`** — so unlike the seeds, **this half does reach every existing adopter** at their next
`bin/sync`. `starter-kit/methodology_trim.py`'s two-metric header and
`starter-kit/methodology_dashboard.py`'s shipped **`high`**-severity risk text both told the reader
what the line metric *protects against*; neither had ever established that archiving *remedies* it.

Both now state the measured mechanism, then the caveat, then the boundary: **the byte metric is a
separate claim — context tax, not read delivery — and is explicitly excluded**, so the caveat cannot
be read as retiring both metrics at once. The dashboard's risk row previously ended with the bare
imperative *"Archive it"*; it now says archiving's effect here is open, because the row fires on a
file whose unreachable records a cut would not make reachable.

**The mirror was re-taken and re-verified after this edit** (dragon 2): `diff -q` byte-identical,
suites re-run **after** the mirror rather than before — S37's failure was recording numbers taken
before a mirror that then moved.

**Verification.** `tools.test_methodology_dashboard` **300 OK** (4 skipped, pre-existing) ·
`tools.test_methodology_trim` **110 OK** · both re-run against the final tree. The seven suite
assertions that string-match `"read cap"` inside the risk description still pass — the replacement
text was written to keep satisfying them.

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [ad hoc] S111 — Phase A (2 of 3): the two SEED doctrine tables, `README.md`, and this file's own front matter

**The `SEED` half of Phase A, and the half that cannot be delivered by syncing.**
`bin/_manifest.py` marks `starter-kit/CHANGELOG.md` and `starter-kit/HANDOFFS.md` as **SEED**, and
`bin/sync:225-230` writes a SEED **only when the destination is absent and never overwrites it
afterward**. So this correction reaches **future adopters only**; every already-bootstrapped project
keeps the false doctrine table until someone edits it **by hand, per repo**. Same defect class as
BL-46/47/48. The remediation note that has to accompany it is a separate commit.

**A mid-session critique from the operator changed this text after it was first written, and the
change is the substantive part of this entry.** Relayed from a `../model_project_constructor`
session: *if the ledgers are newest-on-top and reads are ordered top-down, what is the rationale for
trimming?* The first draft of these rows had replaced *"protects against **silent truncation**"*
with *"protects against **an unread tail**"* — **which is substituting one unverified benefit claim
for another, the exact move Phase A exists to stop.**

**The deduction follows from this session's own measurements, not from the relay.** Probe B
delivered lines 1–10 of 101; probe C's prefix was lines 1–700 of 2,000 — truncation is **ordered
top-down**. These ledgers are **newest-on-top**. Therefore the records a cut removes are ones a
whole-file read **was not delivering anyway**: the delivered prefix is the same before and after the
trim, and what changes is that the reader stops being **warned**. The rows now say the metric
**measures** an unread tail and **does not, on its own, establish a remedy**, and point at **BL-52**.

**What was NOT decided here, deliberately.** Whether to stop trimming, whether the byte metric
survives the same argument, and the dedup between the two dashboard rows — that last is **Phase C**,
and the seeds' *"neither subsumes the other"* sentence is therefore **left standing untouched**.

**`README.md:390`** republished the false rationale as the framework's own; rewritten to state
measured behaviour, to name what it cannot prove, and to say plainly that the earlier claim was
false. **This file's front matter** carried the same claim twice — the rate rule's *"2,000-line agent
`Read` cap"* and the incident line's *"silently dropping its ten oldest entries"*. The second is
corrected with its own diagnosis: truncation was announced; **what was silent was that nothing in the
repo was checking**, which is why the overrun was found by accident.

**No numeral moved.** **Frozen records untouched** — `docs/archive/**`, and every historical
statement inside this file's own records (FM #22, §5.5).

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [ad hoc] S111 — Phase A (1 of 3): the false read-cap premise corrected in the three TRACKED tools

**Phase A of [`read-cap-premise-correction-plan.md`](docs/planning/read-cap-premise-correction-plan.md),
ratified by the operator at this session's Phase 1.** The claim is corrected; **no numeral moved** —
`READ_CAP_LINES` is still `2000`, `LINE_FIRE_BELOW` still `15`, `LINE_STOP_ABOVE` still `30`. Phases
B and C are explicitly not started.

**These three are `TRACKED` in `bin/_manifest.py`, so this correction reaches every existing adopter
at their next `bin/sync`** — read off the SOURCE column by importing `DISTRIBUTION`, never by
grepping the bare filename, which matches the DEST half and inverts the answer.

| file | what was false |
|---|---|
| `starter-kit/methodology_dashboard.py` | the `UNIT`/`VALUE` block, and the shipped **`high`**-severity adopter-facing risk text |
| `starter-kit/methodology_trim.py` | `READ_CAP_LINES`' own comment, and the line metric's stated raison d'être |
| `starter-kit/context_budget.py` | the docstring justifying the LINES axis *"because that is the unit an agent's read cap comes in"* |

**What replaced it — measured this session, not relayed.** Truncation is **announced, not silent**:
an over-cap read returns a `PARTIAL view` banner naming the delivered span, the true length, the
token count and the cap. It does **not** return 2,000 lines. And the cap is **token-denominated**.

**A fourth behaviour, which the plan did not know about and which settles its dragon 8.** An
explicit `limit` spanning an over-cap region **neither bypasses the cap nor truncates — it returns
an error with no content at all** (`File content (199405 tokens) exceeds maximum allowed tokens
(25000)`). The plan's stated controlled pair could not have discriminated this: it reads a file that
comes back whole either way. Run instead on a file that *does* truncate, `limit` is proved not to
bypass — so probe D's "returned whole" is **not** an artifact and §1.4's ratio range stands.

**Every corrected site names the reproduction rather than a replacement number.** §7's least
confident point is whether 25,000 tokens is stable across harness versions; a numeral would rot, the
command does not. Each site now points at Appendix A and says what it cannot prove.

**The unit argument was inverted, not deleted.** The old comment's own evidence — a ~3× B/line
spread, re-measured at **74.7** here against **227.4** next door — argues the *opposite* of what it
was written to argue, because tokens track bytes: it is a single **line** threshold that is wrong for
one ledger by 3×. Bytes are only a proxy too (2.42–2.66 B/token), so no conversion is published.

**Each site also now carries the coupling that makes the cheap fix dangerous** (BL-51): the two
thresholds are denominated in *records of headroom to this number*, so correcting it alone drives
`choose_cut` to `return 1` — one record retained at every adopter, with every test green.

**Verification.** Three Python suites **300 / 110 / 41, all OK** (4 skipped, pre-existing). Twins
**byte-identical** (`diff -q`), mirrored **last** per the plan's dragon 2. `check-links` OK (88/22).
**Seven suite assertions string-match `"read cap"` inside the risk description** and one matches
`"CHANGELOG.md is 2,090 lines"` — found *before* editing, and the replacement text was written to
keep satisfying them rather than discovered by a red suite.

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-08-25.md` (12 record(s), 65,012 B → 32,900 B)

**Written by:** `methodology_trim.py` v1.3.0 — a tool action, not a session's judgment.
Moved the oldest **12** record(s) (2026-08-25 → 2026-08-25) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-08-25.md`](docs/archive/CHANGELOG-through-2026-08-25.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-08-25.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-25.md.verify.sh)
rather than trusting a digest printed here. Live file 65,012 B → 32,900 B (−49.4%).

### 2026-08-26 · [ad hoc] S111 claim — Phase A of the read-cap premise correction

`CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in
[`HANDOFFS.md`](HANDOFFS.md). **The operator ratified `A → B → C` at Phase 1** and directed Phase A
this session; §5.4's open question is settled — *leave the design/audit records, annotate
`ledger-trimmer-design.md` only*. Deliverable: the live behaviour-claim sites in
[`read-cap-premise-correction-plan.md`](docs/planning/read-cap-premise-correction-plan.md)
§5.2/§5.3/§5.4 rewritten to state **measured behaviour and its reproduction method**, **no numeral
moved**, plus the existing-adopter remediation note §5.1 requires.

**Not in scope, each deliberately:** Phase B, Phase C, `READ_CAP_LINES`' value,
`LINE_FIRE_BELOW`/`LINE_STOP_ABOVE`, option D, the 65,536 B ceiling, `docs/archive/**` and every
frozen record (§5.5), BL-45, BL-50, issue #75's unsent PR, **and any outward-facing action**.

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [ad hoc] S110 close-out — read-cap plan delivered; self-score 8/10, predecessor S109 scored 8/10

Phase 3D receipt in [`HANDOFFS.md`](HANDOFFS.md), **12,237 B inside the 12,288 B per-record budget** —
reached in seven passes, each one run against `bin/check-handoff` rather than estimated, every cut
taken from the trailing prose where the checker says to cut. Commits: `8decf71` (1B claim) +
**`c2bc56f`** (the deliverable) + `9038e40` (the trim) + this close-out.

**Two findings this session did not set out to make, both from checking rather than reasoning.**

**BL-50 — the trimmer refuses a correct trim, and it is a distributed defect.** `insert_pointer`
(`starter-kit/methodology_trim.py:940-950`) appends `"\n" + block` when the front matter does not
already end `"\n\n"`; `L2`'s confinement proof (`:582-586`) removes only `block` and never that
injected newline, so the reversal cannot restore the original bytes and the run dies reporting a
losslessness failure **that is an artifact of its own insertion**. Reproduced in isolation — first
difference at char 6126, the tool's own number — rather than forced past. It became reachable
because S109's compaction removed the trailing pointer blocks that used to end `"\n\n"`. Worked
around with a one-byte fork-side data edit; **not** with a standalone `---`, which would trip
`[ZONE_UNCLASSIFIED]` (BL-46's failure). Learning #37 one level down.

**BL-51 — `choose_cut` makes the read-cap correction dangerous.** `stops()` has exactly one caller,
and `choose_cut` (`:876-881`) falls through to **`return 1`** when nothing satisfies it. So
correcting `READ_CAP_LINES` alone would make every adopter's next `--write` retain **one record**.
S94 measured a cut to *two* taking the suite 235/1 → 229/6 (Learning #31). Every existing test stays
green, because nothing evaluates the rate rule at a corrected cap.

**Method notes worth more than either finding.** A ratio measured on one content type does not
transfer to another — 2.419 B/token from ledger content against ≥2.62 from prose — and probe D
killed a self-consistent table this session had already drafted. **A `--check` is not a dry run:** it
returns at `:1698`, before the L1/L2/L3 machinery, so it reports a green trigger for a trim that will
refuse. And a subagent's citation is a claim: **301 reported sites, every one re-read and verified
against the file before use.**

**Phase 3C NOT discharged, and it is structural, not skipped.** `starter-kit/FRAMEWORK_LEARNINGS.md`
is **16 B** from its ceiling (BL-45) and no budget-conforming row fits. **Two learnings are earned
and owed**, both recorded in the receipt's gotchas: *a ratio is a property of its content type, not
of the corpus*, and *`--check` is not a dry run*.

**Verification.** Suite control 287 rows **286 passed / 1 failed / 0 skipped**; after the trim
287 rows, **286 / 1 / 0**; row-for-row, both populations asserted non-empty: **zero status flips,
zero skipped**, five rows differing only in a derived count the trim moved. Sole failure both sides
by name: `github source dry-run failed` (Test 9's standing 404). Trim losslessness three ways
including an independent inverter modelling the declared link-rebase transform: **6 records,
6 byte-identical, 0 unexplained**. `check-handoff` OK · `--all` OK (4) · `check-links` OK (88/22) ·
`check-learnings` OK (37) · `trim --check` silent · `context_budget.py` no file over a ceiling
(bare exit **1 = WARN**, growth run 64/10, ceiling-independent) · `BACKLOG-DETAIL.md.verify.sh` OK.

**FM #28 gate, measured after the last write.** `HANDOFFS.md` **52,808 B** (12,728 B clear), front
matter **6,362 / 7,168 B**; `CHANGELOG.md` 59,542 B *before this entry*;
`starter-kit/FRAMEWORK_LEARNINGS.md` 65,520 B (**16 B free**); `docs/planning/BACKLOG.md` 30,458 B.
`main` **61 ahead of `origin/main`**, nothing pushed.

**Carve-out re-derived by importing `DISTRIBUTION` and reading the SOURCE column** — after a first
attempt grepped the bare filename and hit the DEST half of
`("starter-kit/HANDOFFS.md", "HANDOFFS.md", SEED)`. **Nothing this session touched is a manifest
source. No adopter receives anything. No outward-facing action.**

**Open for the operator:** ratify or reject the plan's A → B → C (§7), and answer §5.4 (annotate the
design records, or leave them?). **BL-45 still blocks Phase 3C for the next session too.**

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-08-25.md` (2 record(s), 66,615 B → 44,725 B)

**Written by:** `methodology_trim.py` v1.3.0 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-08-25 → 2026-08-25) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-08-25.md`](docs/archive/HANDOFFS-through-2026-08-25.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-08-25.md.verify.sh`](docs/archive/HANDOFFS-through-2026-08-25.md.verify.sh)
rather than trusting a digest printed here. Live file 66,615 B → 44,725 B (−32.9%).

### 2026-08-26 · [ad hoc] S110 — plan delivered: correcting the read-cap premise

**The deliverable:** [`docs/planning/read-cap-premise-correction-plan.md`](docs/planning/read-cap-premise-correction-plan.md),
**DRAFT awaiting ratification.** A planning session — nothing implemented, no numeral changed, no
distributed file touched (FM #18/#19). Carve-out re-derived off `bin/_manifest.py`'s **SOURCE**
column, after a first attempt hit the DEST column and read the root ledgers as distributed: all
three files this session touched are **canonical-only**.

**Recommends A → B → C as three separate sessions, and declines the one-pass fix.**

**Three defects in one distributed constant,** separated because they have different remedies:
`READ_CAP_LINES = 2000`'s stated behaviour is false, its unit is wrong (the cap is ~25,000 **tokens**),
and its value is ~**2.9×** too permissive at this repo's ledger density.

**The finding that decided the plan's shape — no grep for `2000` reaches it.** `LINE_FIRE_BELOW = 15`
and `LINE_STOP_ABOVE = 30` are denominated in *records of headroom to the cap*. Run through the
trimmer's own `evaluate_trigger` arithmetic at both ledgers' real baselines: at a corrected cap the
rate rule **degenerates on both** — max possible headroom falls to **12** and **22** records against
a `>30` stop, so `stops()` (`byte_ok and line_ok`) can never return true. **And `stops()` has exactly
one caller.** `choose_cut` (`methodology_trim.py:876-881`) loops the retention count down and
**`return 1`** when nothing satisfies it — so the next `--write` at every adopter would retain **one
record** and archive the rest. S94 measured a cut to *two* taking `bin/tests.sh` from 235/1 to 229/6
(Learning #31); S96 corrected that to six assertions (Learning #33). **Every existing test stays
green**, because nothing evaluates the rate rule at a corrected cap.

**The structural result.** `DEFAULT_BUDGET_BYTES = 64 * 1024 = 65,536 B` sits *inside* the measured
one-read band of **60,475–66,425 B**. The framework already ships a guard on the right axis at very
nearly the right value; the line cap is a redundant second guard on the wrong axis firing ~3× late.
This answers S38's residual 1, which `methodology_dashboard.py:3001-3003` records as undecided.

**The comment's own cited basis refutes it.** `git show 3aee4e3^:CHANGELOG.md` → **2,090 lines /
186,704 B**, which is 2.8–3.1× the token cap: it had been truncating since roughly line **676–743**.
The constant records where the problem was *noticed*, not where it *starts*.

**Four probes [M], reproduction in Appendix A.** 3,000 lines returned whole; 101 lines / 199,700 B
cut at line 10 with a loud `PARTIAL view … cap 25000` banner; **2,000 lines of this repo's own
ledger content cut at line 687 of 2,001**. The fourth **falsified this session's own first draft** —
`FRAMEWORK_LEARNINGS.md` (65,520 B) returned **whole**, so the 2.419 B/token ratio does not transfer
across content types (measured range 2.42–2.66). The plan therefore prescribes the **method**, not a
new numeral.

**The inventory caught the plan itself.** Six blind search angles plus two adversarial critics;
**255 of 255 reported citations re-read and machine-verified** before use. A first draft written from
one reader's grep named 19 sites; the completed sweep found live sites in **ten further files** —
three of them **distributed seeds**, including the two that state the false claim as doctrine in a
table (`starter-kit/CHANGELOG.md:103`, `starter-kit/HANDOFFS.md:97`).

**And those two cannot be repaired by syncing.** Both are `SEED` in `bin/_manifest.py`, and
`bin/sync:225-230` writes a SEED only when the destination is absent, **never overwriting it after**.
A correction reaches **future adopters only**; every already-bootstrapped project keeps the false
doctrine permanently. That is the same defect class as BL-46/47/48 and is the substantive reason
this work batches with them.

**The surface, named per `SESSION_RUNNER.md` §Planning Sessions:** every DONE criterion is
demonstrated on the local suites — **and that surface cannot enforce the property under test.** The
three carriers are Python and cannot invoke the agent's `Read` tool; `bin/tests.sh` has **zero**
`READ_CAP` references. **No test in this repository can falsify a read-cap claim**, so each phase
requires Appendix A re-run in the implementing session, with its output in the receipt.

**Fork-side only. Nothing outward-facing.** Two open questions are left for the operator rather than
decided: whether to annotate the design records (§5.4), and ratification of A → B → C (§7).

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [ad hoc] S110 claim — plan the read-cap premise correction

`CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in
[`HANDOFFS.md`](HANDOFFS.md). **A planning session: the plan is the deliverable and nothing is
implemented** (FM #18, FM #19).

**Why now.** The operator handed over `../model_project_constructor/docs/planning/ledger-budgets-review.md`
(that repo's S248, 2026-08-26). It finds its own trim trigger's stated rationale — *"1,500 lines
(75% of the 2,000-line agent read cap)"* — false by measurement, and recommends replacing a
file-length target with a front-matter budget. **That premise is not only theirs: this repository
authors and distributes it.**

**Three probes, run here rather than relayed.** Their two reproduced exactly; the third is this
session's, and it is the one that decides whether this is a documentation defect or a real one:

| probe | file | result |
|---|---|---|
| A | 3,000 ln / 21,000 B | **returned whole** — the documented "up to 2000 lines" did not bind |
| B | 101 ln / 199,700 B | **cut at line 10**, with a `PARTIAL view … (199405 tokens, cap 25000)` banner naming the exact next call and warning not to answer from the page alone |
| C | **2,000 ln of real `CHANGELOG.md` content at this repo's own 74.8 B/line density** | **61,844 tokens against the 25,000 cap — truncated at line 687 of 2,001, 34% delivered** |

**The cap is token-denominated at 25,000, and truncation is announced, not silent.**

**The exposure is distributed, and read off `bin/_manifest.py`'s SOURCE column rather than the bare
filename.** `READ_CAP_LINES = 2000` ships to every adopter root through three TRACKED tools:
`starter-kit/methodology_trim.py:92` (headroom arithmetic at `:729`/`:809`, a refusal signal at
`:1589`), `starter-kit/methodology_dashboard.py:269` (a **high**-severity adopter-facing risk at
`:3006-3010`, the headroom metric at `:1046`), and `starter-kit/context_budget.py`'s `max_lines`
axis. Its stated justification at `starter-kit/methodology_dashboard.py:264`, republished at
`README.md:390` — *"a Read past it returns the first 2,000 lines with no error and no missing-data
marker"* — is **false in both halves**, and probe C says the number is also wrong in the unsafe
direction: at this repo's density the cliff is near line **690**, so the guard is ~**2.9×** too
permissive and a ledger at 1,999 lines passes every check while delivering a third of itself.
`tools/test_methodology_dashboard.py:3191-3193` **pins the trimmer's and the dashboard's literals to
each other**, so the two agree and are wrong together.

**Two qualifications recorded at claim so the plan cannot overstate.** (1) The practical consequence
here is **small**: truncation is *ordered* top-down and these ledgers are newest-on-top, so Phase 0's
frontier and Phase 3A's single-receipt read land inside the delivered prefix — this repo measured
whole-file reads at 1-in-81. What is wrong is the published claim and the constant's unit more than
the outcome. (2) **This repo has already arrived at the sibling document's recommendation by another
route** — S105/S109's per-record budget and `HEADER_RESERVE_BYTES` are its Options D and E, shipped.
The convergence is corroboration, not a new finding.

**Also standing at claim, neither of them this session's deliverable.** `HANDOFFS.md` is 62,717 B
with **2,819 B clear**, so this session's close-out receipt breaches the ceiling while `--check`
still reports *trigger does not fire* — confirmed silent at this Orient, exactly as S109 predicted.
The trim is **close-out housekeeping**, not a second capability. And `starter-kit/FRAMEWORK_LEARNINGS.md`
is **16 B** from its ceiling, so **Phase 3C cannot be discharged without the operator's BL-45 decision.**

**What does NOT change:** anything implemented, `RECORD_BUDGET_BYTES`, the 65,536 B ceiling, Test
34's floor of 3, and every historical statement of the 2,000-line cap in this ledger and in the
frozen shards, which are records of what was believed when written (FM #22).
**Fork-side only. Nothing outward-facing** — the fix batches with BL-46(2)/47/48/49 for one later PR.

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [BL-46] Cross-repo: BL-46's half (1) closed by the adopter, and its remedy shown too narrow — BL-47/48/49 raised

**Written by:** a session running in `../vscode_quarto_ext` (its S254/S255), acting on that repo's
operator directive. **No distributed file in this repository was touched** — this is a backlog
filing plus this ledger entry. Nothing outward-facing; nothing pushed.

**BL-46 half (1) is DONE.** That repo deleted the blocking footer and ran both overdue trims:
`CHANGELOG.md` **831,830 → 44,190 B** (230 records archived), `HANDOFFS.md` **1,801,150 → 52,850 B**
(211 receipts). Both triggers now stand down. Losslessness established four ways — the tool's
in-process L1/L2/L3+P1A, its emitted `verify.sh`, an independent verifier sharing no code with it,
and a four-lens adversarial pass tasked with *refuting* the claim, which found none.

⚠ **BL-46's DIAGNOSIS IS RIGHT AND ITS PROPOSED DETECTOR WOULD NOT HAVE FIRED.** BL-46 says the
adopter *"never deleted"* the seed sentinel. They **had** deleted it — `METHODOLOGY-SEED-SENTINEL`
was already absent — and the trimmer refused anyway, because what blocks it is the **trailing `---`
and the comment below it**, which the seed's instruction never mentions. `starter-kit/HANDOFFS.md`
carries the sentinel at line 20 and, at line 160, an instruction reading only *"Delete the
seed-sentinel line above"*. **An adopter who follows it exactly still ends up with an inert
trimmer** — which is what happened, for 216 receipts. BL-46's proposed check keys on the sentinel;
it must key on the footer, or the seed must instruct removing both. Annotated in place.

**Three items raised, none duplicating anything here (checked before filing):**
- **BL-47** — the seed `context-budget.json` omits `CHANGELOG.md`/`HANDOFFS.md`, the two files
  `methodology_trim.py` exists to bound, at the 65,536 B constant both tools already share. This is
  BL-46 one level up: BL-46 asks why nobody read the trimmer's output; this is why. That adopter had
  the trimmer since S188 and `context_budget.py` **not at all** until S255.
- **BL-48** — the seed `HANDOFFS.md` lacks the `This file currently holds **N**` sentence its own
  `LedgerSpec.regenerated` declares, so every adopter gets `FRONTMATTER_FIELD_ABSENT` on every trim,
  forever. This repo's root copy *has* the sentence, so the mismatch is invisible from here.
- **BL-49** — `content_probe` is consulted at exactly one call site, `classify_empty`, so a
  **partial** grammar mismatch is never tested. Measured consequence: that repo's `CHANGELOG.md`
  holds 236 dated `###` headings and 230 matched records (six predate its source-tagging
  convention), so a **frozen** shard is published in four places as spanning from `2026-06-30` when
  its true oldest entry is `2026-06-27`. Every L1/L2/L3 assertion passes — nothing is lost, only the
  *description* is wrong, and the description is the index people search.

**Also confirmed from the adopter side:** **BL-27's fix works.** Syncing that repo `v1.1.1 → v1.3.0`
and regenerating its `HANDOFFS` shard proof turned `FAIL: L2 FRONT MATTER lost 1 line(s)` into `OK`.

**Verification:** `docs/planning/BACKLOG-DETAIL.md.verify.sh` **OK** — C1–C5 green, 18 split items
still byte-identical, new items correctly reported as raised-since and not a finding.

