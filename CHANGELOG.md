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

**When to archive again — a rate, not a level.** Archive when the headroom to the 2,000-line agent
`Read` cap, divided by the observed growth per ledger *entry*, falls below **15 entries**; then cut
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
and was silently dropping its ten oldest entries when a `Read` truncated it.

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

---

## 2026-08

### 2026-08-25 · [ad hoc] S106 claim — Phase 1 of the record-budget reduction: lower the constant

`CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in
[`HANDOFFS.md`](HANDOFFS.md). **An implementation session executing a ratified plan** — Phase 1 of
[`docs/planning/record-budget-reduction-plan.md`](docs/planning/record-budget-reduction-plan.md),
one phase, one session, per that plan's own STOP.

**The blocking decision was settled at Phase 1, not assumed.** Plan §9 made ratification of the
number the one thing Phase 1 could not start without, because every site in §5.2 encodes it. The
operator ratified **12,288 (12 KiB)** — the plan's recommendation — over the costed alternatives
10,240 and 8,192. That choice is recorded here so a later session can see it was made rather than
inherited.

**What changes:** `RECORD_BUDGET_BYTES` 18,432 → 12,288 in `bin/check-handoff`, its derivation
comment rewritten from a ceiling-fitting *formula* into a **policy number plus a fit assertion**
(plan §4.3 — otherwise Phase 2's front-matter saving would be handed straight back), the
user-facing remediation text, the nine `bin/tests.sh` couplings, and the `_` note in
`.context-budget.json`.

**What does NOT change, verified rather than assumed:** no distributed file — `bin/check-handoff`
and `bin/tests.sh` are both canonical-only, so **no adopter receives anything this touches**; the
65,536 B ceiling; Test 34's floor of 3; `methodology_trim.py`, which couples only to the whole-file
budget; and every historical statement of 18,432 in this ledger, in `HANDOFFS.md`, and in the
archived shards — those are frozen records of what was true when written (FM #22).

**Why no existing receipt reddens.** `check_record_budget` is **prospective-only**: it checks the
newest record, and only when it differs from its frozen copy at git HEAD. Committed receipts are
exempt by construction. Lowering the budget therefore requires no migration and rewrites no receipt.

**Model:** Claude Opus 5 (1M context).

### 2026-08-25 · [ad hoc] S105 close-out — plan delivered, self-score 8/10, predecessor S104 scored 8/10

Phase 3D receipt in [`HANDOFFS.md`](HANDOFFS.md). **A planning session: the plan is the deliverable
and nothing was implemented** (FM #18/#19) — zero files touched under `bin/`, `tools/` or
`starter-kit/`. Claim `2cdda38`, this close-out.

**The deliverable:** [`docs/planning/record-budget-reduction-plan.md`](docs/planning/record-budget-reduction-plan.md),
DRAFT awaiting ratification. Recommends `RECORD_BUDGET_BYTES` **18,432 → 12,288**, taking the steady
state from **63,296 B (96.6% of ceiling, 2,240 B slack)** to **44,864 B (68.5%, 20,672 B slack)** and
the per-session context cost from ~25 KB to ~19 KB.

**Three measurements decided the plan's shape.** (1) The ledger is **read and gleaned, never
resident** — no `@`-import; measured across 81 transcripts as read whole **once**, in part **593**
times. So a session pays *front matter + one receipt*, and **the receipt is the only lever that
touches recurring cost.** (2) The budget is **prospective-only** — `check_record_budget` compares the
newest record against its frozen copy at HEAD — so **no existing receipt reddens and none needs
rewriting.** (3) Trailing prose is **27–30%** of a receipt while fenced fields mean **12,108 B**,
which is exactly why 12,288 preserves all six mandatory requirements and 8,192 would cut into them
(FM #15). A 17-site grep inventory is in §5, every `bin/` line number verified by re-reading it.

**Two of my own errors, caught at Phase 3F and fixed before commit.** The first draft wrote
`3 × 18,432 + 8,000 = 61,312`, mixing two header terms — the derivation's **8,000 B allowance** gives
**63,296**, while S103's quoted 61,312 uses the header **as measured then** (6,016; today 6,913). The
second: twelve `CHANGELOG.md` line citations were taken *before* this session's own claim entry and
were stale by **5**; re-derived. A line number measured before your own write fails silently.

**`HANDOFFS.md` IS OVER ITS CEILING AGAIN — 67,966 B against 65,536, over by 2,430** (`context_budget.py`
exits 2; `--check` FIRES). **Recorded, not fixed:** a trim is a second capability (FM #26) and this was
a planning session (FM #18). S104 predicted this at its close-out — the breach arrived in exactly one
session, which is the plan's own premise demonstrated rather than argued. **The next session's first
act is the trim (`--cut 3`, never the default); the plan is what stops it recurring.** This receipt was
deliberately written under the **proposed** 12,288 B budget and measures **10,074 B**, 2,214 B clear —
one worked example that the recommendation is livable.

**Model:** Claude Opus 5 (1M context).

### 2026-08-25 · [ad hoc] S105 claim — plan the per-record budget reduction

`CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in
[`HANDOFFS.md`](HANDOFFS.md). **A planning session: the plan is the deliverable and nothing is
implemented** (FM #18, FM #19).

**Why.** S104 established that `HANDOFFS.md` cannot be fixed by trimming: Test 34's retention floor
of 3 receipts × `check-handoff`'s 18,432 B per-record budget + ~6 KB of front matter = **61,312 B
against a 65,536 B ceiling**, and the file sits at 94.4% of that immediately after a trim. The
operator's concern is session context cost, so the target is the number a session actually pays.

**Two measurements that shape the plan, taken before it was written.** (1) The ledger is **read and
gleaned, never resident** — no `@`-import; measured across 81 transcripts as read whole **once** and
in part **593** times, median span 25 lines — so the per-session cost is front matter + **one**
receipt, ~25 KB, not the file. (2) **Trailing prose is 27–30% of every recent receipt** (S104 5,388 B,
S103 4,613 B, S102 4,653 B), and it is the Phase 3A/3B essays — *additive* to the six mandatory
requirements, which the receipt already summarises as the structured `predecessor_score` and
`self_score` fields.

**Model:** Claude Opus 5 (1M context).

### 2026-08-24 · [ad hoc] S104 close-out — receipt written, self-score 8/10, predecessor S103 scored 9/10

Phase 3D receipt in [`HANDOFFS.md`](HANDOFFS.md), inside the 18,432 B per-record budget — asserted by
`bin/check-handoff`, which passes, not predicted (it took **seven** trim passes to get there; the
budget counts fence-to-**next**-fence, trailing prose included). Claim `ab12b27`, deliverable
`470cfd4`, this close-out.

**The deliverable landed: `HANDOFFS.md` 96,264 B → 43,362 B at the trim commit**, and **57,892 B**
with this receipt — from OVER by 30,728 to **7,644 B clear** of the 65,536 B ceiling, with
`--check` reporting `trigger does not fire`. Three receipts archived (S101, S100, S99) to
[`docs/archive/HANDOFFS-through-2026-08-23.md`](docs/archive/HANDOFFS-through-2026-08-23.md); three
retained. The cut was **chosen, not defaulted**: `--cut 3` over the budget default, which retains
**one** receipt and would break **two** non-human consumers — Test 34's anchor floor
(`bin/tests.sh:2110`) and Test 38's fixture builder (`:2721`). `--cut 4` was rejected on a
measurement: 61,101 B, only 4,435 B clear, less than one receipt.

**Losslessness established on four axes, three of them independent of the tool's own L1/L2/L3.**
Per-record: all **6** pre-trim records byte-identical by sha256 across the move, partition disjoint,
none lost, none invented. Front matter: exactly **one diff hunk, a pure 4-line addition**. Full
reconstruction: live records zone + shard records zone is **byte-identical at 89,799 B** to the
pre-trim records zone — the trim is reversible from the two artifacts alone, without git. And the
emitted proof runs green in both its pre-commit and post-commit forms.

**Verification.** Suite **279 passed / 1 failed / 0 skipped** pre and post, the pre-change half in a
**pristine `git worktree`** at `b570389`; sorted row-set diff over **280 rows each side** shows
**zero lost, zero net added, exactly three changed**, each carrying a count in its own name. The
`0 skipped` on both sides is the direct evidence Test 34 held its `ANCHORED` arm. Proofs **9 green /
4 red of 13 → 10 green / 4 red of 14**, same four reds, zero reddened. Python **451/451**.
`check-links` 88/22 and `check-learnings` 35 **unchanged**, as predicted at claim.

**The structural finding, which outlives this trim.** Test 34's floor of 3 receipts × the 18,432 B
per-record budget + ~6 KB of front matter = **61,312 B against a 65,536 B ceiling**; this file now
sits at **94.4%** of that. The ledger's steady state is therefore ~3 receipts and a trim nearly every
session, **by construction** — `--cut 3` was already the most aggressive cut the floor permits, so
the durable remedy is a decision about the ceiling or the per-record budget, not another trim.
Raised for an operator decision; **no BL item filed** (a second capability).

**A defect of mine, caught before commit and recorded.** The first claim-stub splice anchored on
`text.index("```handoff")`, matching a **substring** in a front-matter sentence rather than the first
record fence; fence parity flipped and the trimmer correctly reported 4 records in a 6-receipt file.
Reverted byte-identical, redone line-anchored with a count assertion. **And one criticism withdrawn
after checking it:** S103's `6,016 + 3 × 18,432 = 61,312 B` is a sound steady-state bound, not an
overstatement — the 43,362 B I compared it against was a transient mid-trim state holding a pending
stub. Comparing a bound to a mid-operation measurement is a timing error.

**No outward-facing action:** no push, no PR, no comment, no tag, no issue edit. Nothing DISTRIBUTED
was touched. **A learning is owed and unwritten** — `starter-kit/FRAMEWORK_LEARNINGS.md` is at
63,126 / 65,536 with **2,410 B** free and rows costing 1,219–1,436 B; four are now queued (S99, S102,
S103, mine). Fourth consecutive deferral for the same reason, stated rather than left unsaid.

**Model:** Claude Opus 5 (1M context).

### 2026-08-24 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-08-23.md` (3 record(s), 96,264 B → 43,362 B)

**Written by:** `methodology_trim.py` v1.3.0 — a tool action, not a session's judgment.
Moved the oldest **3** record(s) (2026-08-18 → 2026-08-23) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-08-23.md`](docs/archive/HANDOFFS-through-2026-08-23.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-08-23.md.verify.sh`](docs/archive/HANDOFFS-through-2026-08-23.md.verify.sh)
rather than trusting a digest printed here. Live file 96,264 B → 43,362 B (−55.0%).

### 2026-08-24 · [ad hoc] S104 claim — run the `HANDOFFS.md` trim, losslessly

`CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in
[`HANDOFFS.md`](HANDOFFS.md). Recorded BEFORE the trim because the trimmer's **P1 guard** refuses
otherwise: a trim commit advances this file's Phase 0 frontier and would permanently hide any commit
not yet recorded (S95's precedent, S103's shape).

**The target:** `HANDOFFS.md` arrived **92,387 B against a 65,536 B ceiling, OVER by 26,851** — the
only file over one — with `--check` firing on both triggers. `CHANGELOG.md` is **not** being trimmed:
it reports `trigger does not fire` at 41,462 B, and a second trim is a second capability (FM #26).

**The cut is `--cut 3`, chosen, and it is not the tool's default — measured, not argued.** With the
claim stub in place the file holds 6 receipts, and the three candidates dry-run as: the **default**
retains **1** (→ 10,790 B) and raises `[CUT_STRADDLES_DAY]`; **`--cut 4`** retains 4 (→ 61,101 B,
only **4,435 B** clear of the ceiling, less than one receipt — they run 15,533–18,431 B here) and
also straddles; **`--cut 3`** retains 3 (→ **43,362 B, 22,174 B clear**) and raises **neither**
`[CUT_STRADDLES_DAY]` **nor** `[SHARD_NAME_DISAMBIGUATED]` — a clean calendar seam at
2026-08-23 | 2026-08-24 and the free name `docs/archive/HANDOFFS-through-2026-08-23.md`.

**Why the default is not merely worse but wrong: it breaks two non-human consumers, read in the
code rather than assumed.** `bin/tests.sh` Test 34 derives its mutation anchors as `ids[1]`/`ids[2]`
and routes a population below 3 to the `SHORT` arm, printing **six assertions as SKIP**
(`anchor_disposition`, `bin/tests.sh:2110`); Test 38's fixture builder aborts `FIXTURE SOURCE TOO
SHORT: need >= 2 records` at `len(starts) < 3` (`bin/tests.sh:2719`) — unsatisfiable from one
retained receipt once its own code drops the leading `status: pending` record. Retaining exactly 3
sits **at** Test 34's floor; that margin is spent deliberately, for a name that means what it says
and ~22 KB instead of ~4 KB of runway.

**A defect of mine, found and fixed before it was committed, recorded because the next session will
hit the same edge.** The first splice of the claim stub anchored on `text.index("```handoff")`, which
matched the **substring** inside a front-matter sentence at line 9 — `` recount with `grep -c
'^```handoff' HANDOFFS.md` `` — not the first record fence at line 73. The stub landed mid-sentence,
fence parity flipped, and `methodology_trim.py` then reported **4** records in a 6-receipt file: two
real receipts had been swallowed as `inside=True` by `fence_scan`. The tool was right and the edit
was wrong. Reverted byte-identical to `HEAD`, redone with a **line-anchored** `(?m)^```handoff$` and
an assertion that the record count rises by exactly 1. That is S103's own gotcha — *anchor on
line-anchored fences and assert the count* — arriving one session later against a different tool.

**Model:** Claude Opus 5 (1M context).

### 2026-08-24 · [ad hoc] S103 close-out — receipt written, self-score 8/10, predecessor S102 scored 9/10

Phase 3D receipt in [`HANDOFFS.md`](HANDOFFS.md), inside the 18,432 B per-record budget — asserted by
`bin/check-handoff --all`, which passes, not predicted. Claim `dbaaa94`, deliverable `6be9388`, this
close-out.

**The deliverable landed: `CHANGELOG.md` 75,564 B → 39,148 B, back under its 65,536 B ceiling with
26,388 B of headroom** at the trim commit `6be9388` — this close-out entry then brings it to
just over 41,400 B, still more than 24,000 B clear — and `methodology_trim.py --file CHANGELOG.md --check` now reports `trigger
does not fire` on both triggers. The cut was **chosen, not defaulted**: `--cut 2026-08-17` over the
tool's budget-driven default, paying 6,260 B of headroom for a shard name that is a true day
boundary instead of a span label — the [CUT_STRADDLES_DAY] advisory the default raises. The seam is
**proved** clean rather than inferred from that advisory's absence: retained records carry only
2026-08-18/23/24, archived only 2026-08-15/16/17, no date on both sides.

**Verification, on five independent axes.** Suite **279/1 pre and post**, the pre-change half run in
a **pristine worktree** so it could not be contaminated by the writes it was controlling for; a
sorted row-set diff over **280 rows each side** shows **zero lost and exactly three changed**, all
three carrying counts in their own names. All **13** `.verify.sh` proofs re-run: **9 green / 4 red**,
the same four reds as before, **zero reddened**. Python **451/451**. `check-links` (88 / 22) and
`check-learnings` (35 rows) **byte-identical pre and post**. And the file's own documented source-tag
audit across live plus archives went **287 → 289** — exactly this session's two added entries, with
no archived record dropping out of the census.

**`HANDOFFS.md` is now the only file over a ceiling — 92,387 B, OVER by 26,851**, this receipt being
~12 KB of that. Its trim FIRES on both triggers and was **deliberately not run**: a second trim is a
second capability (FM #26). It is the next deliverable, and its binding constraint is stated in the
receipt — **Test 34's retention floor of three receipts, so `--cut 3` or more, never the default.**

**Model:** Claude Opus 5 (1M context).

### 2026-08-24 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-08-17.md` (26 record(s), 76,774 B → 39,148 B)

**Written by:** `methodology_trim.py` v1.3.0 — a tool action, not a session's judgment.
Moved the oldest **26** record(s) (2026-08-15 → 2026-08-17) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-08-17.md`](docs/archive/CHANGELOG-through-2026-08-17.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-08-17.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-17.md.verify.sh)
rather than trusting a digest printed here. Live file 76,774 B → 39,148 B (−49.0%).

### 2026-08-24 · [ad hoc] S103 claim — run the `CHANGELOG.md` trim

`CHANGELOG: pending`. Declarations and controls are in the `status: pending` receipt in
[`HANDOFFS.md`](HANDOFFS.md). **Recorded before the trim, because the trimmer's own P1 guard refuses
otherwise** — a trim commit advances this file's Phase 0 frontier and would permanently hide any
commit not yet recorded (S95's precedent, for the same stated reason).

**This file arrived 75,564 B against its own 65,536 B ceiling — OVER by 10,028**, and the trim is
**three sessions overdue** (S102 `next_steps` (b) named it the obvious next deliverable). Bringing it
back under is this session's one deliverable. **`HANDOFFS.md` is over too and is NOT claimed here** —
a second trim is a second capability (FM #26).

Pre-change controls captured BEFORE any write, both populations non-empty: the **12** shipped
`.verify.sh` proofs at **8 green / 4 red**, re-derived independently and matching S102's census; and
the `bin/tests.sh` baseline running in a **pristine worktree at `da40bdb`**, which is what keeps it a
control — S102's own baseline overlapped its claim write and misread one row by one.

**Model:** Claude Opus 5 (1M context).

### 2026-08-24 · [ad hoc] S102 close-out — receipt written, self-score 8/10, predecessor S101 scored 7/10

Phase 3D receipt in [`HANDOFFS.md`](HANDOFFS.md), inside the 18,432 B per-record budget (asserted by
`bin/check-handoff --all`, not predicted). Claim `b300098`, deliverable `ebe69eb`, this close-out;
branch commit `60246e7` unpushed.

**S101 scored 7 for one reason worth recording here rather than only in the receipt:** its
`next_steps` (g) carried *"issue #75's answer prepared, vetted, unsent"* — a formulation S99 and
S100 carried too — which conflates the **comment** (sent 2026-08-16 on an explicit go-ahead,
recorded at `143ff2b` in this very file) with the **implementation** (never sent). Paired with a
session count that was incremented rather than derived — "ten", then "eleven", against an enumerated
**9** — it left the fork's stated purpose looking blocked when nothing blocked it. Neither claim was
marked unverified. **An unattributed status claim propagates exactly like an unattributed blocker.**

**Both mandated-read ledgers are now over their ceilings**, `CHANGELOG.md` by this session's three
owed entries and `HANDOFFS.md` by this receipt. Figures are in the receipt's FM #28 gate line,
measured after the last write. Neither trim was run: each is a session-sized deliverable (S87's
precedent, restated by S100 and S101), and running one here would be a second capability (FM #26).

**Model:** Claude Opus 5 (1M context).

### 2026-08-24 · [issue #75] Upstream PR prepared and NOT sent — branch `docs/issue75-plan-surface-upstream`, local only

**A branch op, recorded as an action; no outward-facing action was taken.** Nothing pushed, no PR,
no comment, no tag — verified with `git ls-remote --heads origin`, which returns nothing for this
branch. Branch `docs/issue75-plan-surface-upstream` = `60246e7`, based on `upstream/main` (`512c2ed`),
1 ahead, 3 files, +172/−1. Drafts: [`docs/planning/issue75-upstream-pr.md`](docs/planning/issue75-upstream-pr.md)
(what exists, decisions, how to send) and its `-body.md` sibling (the PR body, `--body-file`-ready).

**The finding that made this more than a cherry-pick.** Fork `main`'s `starter-kit/SESSION_RUNNER.md`
differs from `upstream/main` in **FIVE** hunks; only **two** are #75. The other three — Phase 3C
rerouted to `FRAMEWORK_LEARNINGS.md`, the `**Model:**` ledger bullet, and the Learnings-table
extraction — all depend on `starter-kit/FRAMEWORK_LEARNINGS.md`, **which does not exist upstream**
(nor does `starter-kit/methodology_trim.py`). A whole-file take would have carried three unshipped
changes into a one-issue PR. Built instead by applying `b1b7eaf`'s patch for that file alone;
`git apply --check` passed.

**Test numbering collides across the two repos.** The fork's Tests 32/33/34 *are* upstream's 23/24/25
(upstream `bin/tests.sh` is 650 lines against the fork's 2,981), so the fork's Test 36 ports as
**Test 26**. Fork-only references were rewritten, not carried: `BL-10` and fork session ids removed,
and the citation census stated as the commands that reproduce it rather than as drifting line numbers.

**Verified on the branch, which is the surface that matters** — the fork's suite says nothing about a
tree built from `upstream/main`. Pre-change control on a pristine tree **114/0**; RED with the test
added and the runner unpatched, **5 of Test 26's 6 rows failing** with populations non-empty; GREEN
**120/0**; row-for-row diff **+6 rows, ZERO lost**. `check-links` OK (83/21), `check-learnings` OK (13
rows). Adopter smoke: `bin/sync` delivers `SESSION_RUNNER.md` byte-identical with 7 checklist items and
both occurrences of the quoted phrase. **Not exercised: GitHub delivery, review, or merge.**

**The upstream census is cleaner than the fork's, and the PR body uses the upstream one.** On
`upstream/main`: `"Faithful verification, per surface"` **1** (its own definition), `gate (d)` **0**,
`gate d` **1** — inside gate (d)'s own section. Nothing outside §Vertical Slice Sessions referred to
it in either spelling; the fork had one such citation, in a fork-only planning file.

**Two inherited claims corrected at Orient.** The #75 **comment** was sent 2026-08-16 with the
operator's per-action go-ahead (`143ff2b`); it is the **implementation** that was unsent. And it is
**9** sessions since S92 (S93–S101, enumerated from receipts), not the eleven/twelve the receipts had
been incrementing.

**Model:** Claude Opus 5 (1M context).

### 2026-08-24 · [issue #75] S102 claim — prepare the upstream PR, send nothing

`CHANGELOG: pending`. Declarations, corrections and controls are in the `status: pending` receipt in
[`HANDOFFS.md`](HANDOFFS.md). **Compact by necessity: this file arrived 4,886 B OVER its own 65,536 B
ceiling** (S101's `next_steps` (a)); trimming it is a second capability, not claimed here. Two
inherited claims corrected at Orient: the #75 **comment** was sent (2026-08-16, `143ff2b`) — the
**implementation** is what is unsent — and it is **9** sessions since S92, derived from the receipts,
not the incremented eleven/twelve.

**Model:** Claude Opus 5 (1M context).

### 2026-08-23 · [ad hoc] S101 close-out — receipt written, self-score 8/10, predecessor S100 scored 8/10

Phase 3D receipt in [`HANDOFFS.md`](HANDOFFS.md), within the 18,432 B per-record budget, verified by
running `bin/check-handoff` rather than predicting it. Deliverable: the `HANDOFFS.md` trim
(`101,053 B → 44,845 B`). Phase 3C's `FRAMEWORK_LEARNINGS.md` row was **offered to the operator and
scoped out** — recorded in the receipt, with the row's text, rather than silently skipped.

Session crossed local midnight; ledger entries stay on the session's date, git timestamps carry the
real one.

**Model:** Claude Opus 5 (1M context).

### 2026-08-23 · [ad hoc] Test 38's frozen population is CONSTRUCTED over budget, not inherited from the live ledger

`bin/tests.sh` (canonical-only). The 2026-08-23 trim archived S97 (20,086 B) and S96 (19,408 B) —
the live ledger's only two records over `check-handoff`'s 18,432 B per-record budget — and Test 38's
assertion (4), *committed records are exempt as frozen*, went vacuous: it began asserting `0 over`
against a population of **0**. S98's scope control caught it the first time a trim took the property
away, exactly as its comment said it would.

**No cut could have avoided this.** Retaining S97 means retaining five receipts — 101,053 B against a
65,536 B ceiling — so the ceiling and that assertion's arming are mutually exclusive. The fixture
builder now pads the **oldest** record's trailing prose to 18,944 B and re-parses the artifact to
assert the frozen population really holds one over budget, failing loudly (`FIXTURE NOT ARMED`)
rather than silently if it ever does not. Suite 279/1 restored, the sole failure Test 9's
pre-existing `--source=github` 404.

Mutation-proven, each mutant verified to apply and every restore `cmp`-checked: padding to exactly
*at* budget, and padding removed, both re-redden the control.

**Model:** Claude Opus 5 (1M context).

### 2026-08-23 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-08-18.md` (3 record(s), 101,053 B → 44,845 B)

**Written by:** `methodology_trim.py` v1.3.0 — a tool action, not a session's judgment.
Moved the oldest **3** record(s) (2026-08-17 → 2026-08-18) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-08-18.md`](docs/archive/HANDOFFS-through-2026-08-18.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-08-18.md.verify.sh`](docs/archive/HANDOFFS-through-2026-08-18.md.verify.sh)
rather than trusting a digest printed here. Live file 101,053 B → 44,845 B (−55.6%).

### 2026-08-23 · [ad hoc] S101 claim — run the `HANDOFFS.md` trim

`CHANGELOG: pending`. Breach, cut, controls and six declarations are in the `status: pending`
receipt in [`HANDOFFS.md`](HANDOFFS.md). **Minimal by necessity: this file arrived 1,764 B OVER its
own 65,536 B ceiling** (S100's `next_steps` (c)); trimming it is a second capability, not claimed here.

**Model:** Claude Opus 5 (1M context).

### 2026-08-23 · [BL-41] S100 close-out — receipt written, self-score 8/10, predecessor S99 scored 8/10

Phase 3D receipt in [`HANDOFFS.md`](HANDOFFS.md), inside the 18,432 B per-record budget
(`check-handoff`: `1 unwritten record(s), 0 over`). Phase 3C added **Learning #36** to
`starter-kit/FRAMEWORK_LEARNINGS.md` — a second DISTRIBUTED file, which the claim's carve-out did
not anticipate; the departure is recorded in the receipt rather than quietly widened.

**Model:** Claude Opus 5 (1M context).

### 2026-08-23 · [BL-41] `methodology_trim.py` disambiguates a taken shard name instead of refusing

`TRIM_VERSION` 1.2.0 → **1.3.0**, one DISTRIBUTED file. The shard name was a function of a record
DATE while the cut is POSITIONAL — not injective, yet used as a unique key behind a write-once
refusal, so every admissible cut of `HANDOFFS.md` derived one taken name and the tool's own advice
(*"Disambiguate with `--cut`"*) had no solution. A taken name now resolves to `-2`, `-3`, … and is
REPORTED; nothing is ever overwritten, and past `SHARD_SUFFIX_MAX` it still refuses.

`--cut 3` — the cut BL-41 recorded as impossible — now archives to
`HANDOFFS-through-2026-08-17-2.md`, retaining Test 34's floor of three: 82,966 → **43,928 B**.
**Dry run only; no trim was run** — a second capability (FM #26), scoped out by the operator.

RED first against copied fixtures (3 failures + 2 errors, both controls green on either side);
9 mutants, **9/9 killed**; suite diffed row-for-row against the Orient baseline, **zero rows lost**;
the 9 shipped `.verify.sh` proofs unchanged at 5 green / 4 red (BL-36, pre-existing).
Detail in the [`HANDOFFS.md`](HANDOFFS.md) receipt and the BL-41 row in `docs/planning/BACKLOG.md`.

**Model:** Claude Opus 5 (1M context).

### 2026-08-23 · [BL-41] S100 claim — restore the routine `HANDOFFS.md` trim

`CHANGELOG: pending`. Measurements and the seven declarations are in the `status: pending` receipt
in [`HANDOFFS.md`](HANDOFFS.md). **Deliberately minimal: this file had 397 B of byte headroom at
claim while its gate row read `894 ln / 2,000 ln — ok`.**

**Model:** Claude Opus 5 (1M context).

### 2026-08-18 · [ad hoc] S99 close-out — receipt written, self-score 8/10, predecessor S98 scored 8/10

Phase 3D receipt in [`HANDOFFS.md`](HANDOFFS.md), within the 18,432 B per-record budget S98
introduced (`check-handoff`: `1 unwritten record(s), 0 over`). Substantive work is the entry below.

**BL-41 raised, found not fixed:** `methodology_trim.py` cannot trim `HANDOFFS.md` at all. Shards are
named `HANDOFFS-through-<date of newest archived record>.md` and an existing one is never overwritten;
retention is by count, floored at three by `bin/tests.sh` Test 34. With receipts at S96/S97
(2026-08-17) and S98/S99 (2026-08-18) and `HANDOFFS-through-2026-08-17.md` already present, `--cut 3`
and `--cut 2` derive the taken name and are refused; `--cut 1` is free but drops below the floor.
**Every admissible cut yields the taken name, so the tool's advice — "Disambiguate with `--cut`" —
has no solution.** Verified by dry run; no `--write` issued. Full write-up and three candidate fixes
in [`BACKLOG-DETAIL.md#bl-41`](docs/planning/BACKLOG-DETAIL.md#bl-41).

**So `HANDOFFS.md` closes OVER — ~79.6 KB against 65,536, stated rather than left to be found; re-derive with the gate, since the figure counts the receipt that reports it.** It was already over at
claim: a protocol-mandated receipt landing in a ledger S98 closed with 2,863 B of headroom against
receipts that run 17–20 KB. No session writing any receipt could have avoided it.

**A Learning is owed and deliberately not written** — *a losslessness proof only proves losslessness
of the population it enumerates*. `starter-kit/FRAMEWORK_LEARNINGS.md` is DISTRIBUTED and this
session's claim declared it would touch none; holding to that was worth more than the row. #36 is the
next session's.

**Model:** Claude Opus 5 (1M context).

### 2026-08-18 · [ad hoc] `docs/planning/BACKLOG.md` comes under its ceiling by SPLIT — index here, bodies in a read-on-demand sibling

**103,755 B → 26,504 B, `ok`** — the only file the FM #28 gate flagged, now green. Commit `8eb4f0e`.
The 18 open-item bodies moved **verbatim** to
[`docs/planning/BACKLOG-DETAIL.md`](docs/planning/BACKLOG-DETAIL.md); `BACKLOG.md` keeps a 19-row
index. Full detail in the S99 receipt — this entry records the decisions a future session must not
re-litigate.

**Why a split and not a trim.** Open bodies were 81,340 B — 98% of the section, **1.24× the whole
ceiling alone**. Deleting the front matter, all 11 archive pointer rows and the historical section
(20,716 B, everything not live work) still left it 17,503 B over. Because nothing was compacted or
dropped, the operator policy question at `.context-budget.json:73` — what to abandon — was never
reached and stands unanswered.

**Why the ceiling stayed on the whole-file axis.** S97 and S98 moved the two sibling ledgers *off*
it after measuring 1 whole read in 80 and 81 transcripts. Measured the same way: this file was read
**whole 23 times across 22 of 82 transcripts (27%)**, against 584 partial reads, most recently
2026-08-13 — ~22× either sibling, because Phase 0 step 3 asks it for *current priorities*. Ceiling
**retained**; the per-record remedy deliberately not copied, and the budget entry now says so.
The instrument was audited before publishing: four defects found and fixed (`git cat-file -e` read as
a `cat`; two other repos' `BACKLOG.md` swept in; a quoted `sed` script split mid-expression; the word
*cat* inside receipt prose).

**Losslessness proved, not asserted.**
[`BACKLOG-DETAIL.md.verify.sh`](docs/planning/BACKLOG-DETAIL.md.verify.sh) re-extracts each item from
git **by `BL-N` identity, never by position** — the flaw behind BL-36's four false failures. C1–C5;
**7 mutants, each verified to apply, 7/7 killed** against a passing control.

**C5 exists because C1–C4 were green while content was lost.** The first cut silently dropped the
1,684 B *"Routing — what a session can actually run today"* block — not an item body, so outside the
population the proof enumerated, and the standing record that the *"blocked on the paused channel"*
disposition **was never imposed**. Restored verbatim; now asserted. **A losslessness proof only
proves losslessness of the population it enumerates.** C1 also had to be repaired before shipping:
it failed on any *newly raised* item, which would have turned it red on correct use.

**Mechanical readers, against baselines captured before the edit:** archive proof 4/4; dashboard
`_scan_backlog_done` unchanged at `unrecognized`/0/False — the index declares **no Status column**,
which would otherwise count the completed rows' `CLOSED`/`SHIPPED`/✅ as unmigrated done-marks;
`bin/tests.sh` 279/1/0 row-for-row identical; 444/444 Python; `check-links` 88/22; health 72. The
gate's structure check was repaired to follow the split and **proven red by mutation** before being
trusted — it had correctly reported `instrument-failed`.

Carve-out verified mechanically: 26 `DISTRIBUTION` rows vs 6 changed paths, both non-empty,
**intersection NONE**.

**Model:** Claude Opus 5 (1M context).

### 2026-08-18 · [ad hoc] S99 claim — bring `docs/planning/BACKLOG.md` under its ceiling

`CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in
[`HANDOFFS.md`](HANDOFFS.md) is the durable crash breadcrumb. Both resolved at this session's
close-out above.

Two facts recorded *at claim*, before any remedy was attempted, because they bound the remedy:
**no housekeeping cut could clear the ceiling** (`## Open items` alone was 1.27× it, so deleting
everything that is not live work still left the file 17,503 B over), and **the obvious cut was
load-bearing** — the archive proof's C4 asserts reachability against the live file, so deleting
§Completed items would turn a green proof red. Baseline captured before any edit: 4/4.

**Model:** Claude Opus 5 (1M context).

### 2026-08-18 · [ad hoc] S98 close-out — receipt written, self-score 8/10, predecessor S97 scored 8/10

Phase 3D receipt in [`HANDOFFS.md`](HANDOFFS.md); the substantive work is the per-record budget entry
below and the trim entry above it. **Framework Learning #35 appended** at 1,219 B against the 1,500 B
row budget — two limits set independently on one artifact can multiply into a constraint nobody
checks, which is why this breach kept recurring while each session's trim looked correct.

**The guard was applied to its own author.** This receipt measures **17,162 B against the 18,432 B
per-record budget introduced this session** — `check-handoff` reports `1 unwritten record(s), 0 over`.
The ledger closes at **62,673 B against the 65,536 B ceiling**, 2,863 B of headroom, and the FM #28
gate reports `HANDOFFS.md` **ok** for the first time in four sessions.

Two tracked telemetry ledgers committed with it — `.context-budget-history.jsonl` and
`dashboard_history.jsonl` — which go dirty from Phase 0 alone and which no protocol step owns.

**Model:** Claude Opus 5 (1M context).

### 2026-08-18 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-08-17.md` (4 record(s), 118,534 B → 49,579 B)

**Written by:** `methodology_trim.py` v1.2.0 — a tool action, not a session's judgment.
Moved the oldest **4** record(s) (2026-08-15 → 2026-08-17) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-08-17.md`](docs/archive/HANDOFFS-through-2026-08-17.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-08-17.md.verify.sh`](docs/archive/HANDOFFS-through-2026-08-17.md.verify.sh)
rather than trusting a digest printed here. Live file 118,534 B → 49,579 B (−58.2%).

### 2026-08-18 · [ad hoc] The receipt ledger gets a guard on the axis its cost is actually paid on — a per-record budget, derived from the collision it resolves

`HANDOFFS.md` stood at **114,466 B against a 65,536 B ceiling**, and the trim S97 recommended did
not clear it: re-derived, `--cut 3` gave **66,778 B**. The reason was not untrimmed backlog. Post-trim
the header is 6,017 B, leaving 59,519 B; `bin/tests.sh` Test 34 floors retention at **three**
receipts; the newest three totalled **60,761 B**. Floor × mean already exceeded ceiling − header, so
**no cut satisfied both constraints** — two limits set independently had begun to collide.

**Measured before choosing a remedy.** Across **81 transcripts** of this repo (the measuring session
excluded) the live root ledger was read **whole into a session's context exactly once** and read **in
part 593 times** — median span 25 lines, largest ever requested 220, against a 452-line file. No read
in the corpus asked for even half of it. That is what `SESSION_RUNNER.md` mandates and what
`.context-budget.json` already said in its own note: Phase 0 step 6 takes a **frontier** (`git log -1`,
no content) and Phase 3A reads **the predecessor's receipt in full**. One record.

**The instrument was wrong twice before it was right, both times flatteringly.** The first pass scored
the 4.5 KB seed `starter-kit/HANDOFFS.md` as the live ledger — 8 of its 9 "whole reads" were the seed —
and scored `awk '/^```handoff/{n++} n==1'`, which extracts *one receipt*, as a whole-file read. It
reported 9 whole reads. The answer is 1. Found by printing raw matched commands, not by re-reading the
counter.

**The fix.** `bin/check-handoff` (canonical-only) gains `RECORD_BUDGET_BYTES = 18432` and
`check_record_budget()`, scoped to the record **being written** — the newest record when its text
differs from its counterpart at git HEAD. Comparing record *text*, not "is this session id new", is
what stops a close-out from growing its own already-committed Phase 1B stub past the budget unseen.
The derivation is `(65,536 − 8,000 header allowance) / 3 = 19,178 → 18,432 B`, 2,240 B of slack, and it
is written beside the constant so a successor re-runs it rather than re-argues it. Records have grown
**3.15×** (oldest 10 mean 5,478 B; newest 10 mean 17,258 B; largest ever 21,267 B, n=104).

**The unit is the record, not the fenced block** — trailing prose below the closing fence is counted,
because the byte ceiling counts it and `methodology_trim.py` moves it as part of the record. Budgeting
the fence alone would put the guard on a different axis from the ceiling it is derived from and make
the arithmetic above false. Mutant **M5** exists to defend exactly that.

**Deliberately NOT run under `--all`:** Test 34's presence control asserts on `check-handoff`'s **exit
code** against the live ledger, and an exit code is a union over every check — routing the budget
through `--all` would turn an unrelated assertion red whenever a session's in-flight receipt ran long.
Asserted, not just intended, by assertion (7).

`bin/tests.sh` **Test 38** — 18 assertions, **5 mutants, 5 killed**, against a throwaway git repo so the
live ledger is never written to. Proven RED in situ first: an oversized record injected into the live
tracked file made the pre-change checker exit **0** and the new one exit **1**; restore verified
byte-identical by `cmp` and `git diff --quiet`. Suite **279 passed / 1 failed** (the pre-existing Test 9
`--source=github` 404), diffed row-for-row against a clean HEAD worktree: **zero rows lost**, 18 added,
both populations asserted non-empty (262 and 280).

**Two fixture defects of my own, both caught by the artifact and not by the builder.** The record
builder prepended at byte 0, absorbing the file's 5,569 B header into the record under test; and its
size check measured the string it had just constructed rather than the record as the checker parses it
— an identity, not an assertion. Corrected to insert at a **line-anchored** fence (a plain
`text.index("```handoff")` lands in front-matter prose that mentions the fence inline, leaving 86 stray
bytes inside the record) and to re-parse the written file.

Carve-out verified mechanically against the staged set: **26 manifest SOURCE rows vs 2 changed files,
both populations asserted non-empty, intersection empty** — no distributed file touched.

**Model:** Claude Opus 5 (1M context).

### 2026-08-18 · [ad hoc] Session S98 claimed — bring `HANDOFFS.md` under its ceiling durably

Phase 1B claim; receipt stub in [`HANDOFFS.md`](HANDOFFS.md) with `status: pending`. The subject is
S97's `next_steps` (b), and it is the repository's live size breach: **114,466 B against a 65,536 B
ceiling, over by 48,930**.

**One finding is recorded here at claim rather than at close-out, because it refutes the remedy the
handoff recommends.** S97 measured `--cut 3 = 49,724 B` and called it "real room". Re-derived at this
Orient, the same cut yields **66,778 B — 1,242 B over**. S97's figure was taken before its own
20,086 B receipt was appended, and it said so; that receipt is now one of the three a `--cut 3`
retains.

**The condition is a collision between two constraints set independently, not a backlog of untrimmed
bytes.** Post-trim the header is 6,017 B, leaving 59,519 B for records. `bin/tests.sh` Test 34 floors
retention at **three receipts**. The last three total **60,761 B** (mean 20,254 B). Floor × mean
already exceeds ceiling − header, so **no cut satisfies both**: `--cut 2` clears at 45,511 B only by
going below the floor, where six assertions become stated `SKIP` rows (BL-40 (b)).

Which of the three levers moves — receipt **size**, the **floor**, or the **ceiling** — is a policy
choice and goes to the operator with numbers before anything is written. Noted for that choice:
`.context-budget.json` sources this ceiling to `methodology_trim.py:69` — the trimmer's
`DEFAULT_BUDGET_BYTES`, an **inherited default**, at a line number S97 already flagged as stale — while
the same entry states the mandated read as *"Phase 0 step 6 reconciles this file's frontier and Phase
3A reads the predecessor's receipt in full."*

**Model:** Claude Opus 5 (1M context).

