# Changelog — Authoritative Action Ledger

The cumulative, append-only record of **actions taken in this repository** — across backlog
items, repository issues, and ad-hoc work. It is the authoritative answer to *"what was done
here, ever?"*, distinct from the release narrative in [`CLAUDE.md` §Versioning](CLAUDE.md#versioning).

This repository dogfoods its own methodology: every session records its actions here at
close-out (`starter-kit/SESSION_RUNNER.md` Phase 3F), and Phase 0 reconciles the ledger against
`git log` and backfills anything a crashed or out-of-band session missed. Taking an action — any
commit, or any non-commit action (release, tag, PR, upstream issue close, access grant, grooming
decision) — and not recording it is failure mode #27. The rules for this file live in
[`FRAMEWORK_APPARATUS.md` §The Action Ledger](FRAMEWORK_APPARATUS.md#the-action-ledger); the reusable
seed, [`starter-kit/CHANGELOG.md`](starter-kit/CHANGELOG.md), points there.

**Source tag — exactly one per entry.** This enumerates every logged action across the live file
and its archives, and proves all three sources landed:

```
cat CHANGELOG.md $(git ls-files 'docs/archive/CHANGELOG-*.md') \
  | grep -cE '^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[(issue #[0-9]+|BL-[^]]+|ad hoc)\]'
```

It is anchored to the entry heading, and it reads the archives, for two separate reasons. The
unanchored single-file form published here before the v3.6 split returned **78** against 64 actions —
it also matched the three tag definitions just below and eleven in-prose mentions of a tag — and after
the split it would have stopped counting the archived entries at all. It lists the shards with
`git ls-files`, not a bare glob, because zsh aborts a glob that matches nothing; it is the audit in
§The Action Ledger, which counts the same in zsh and bash.

- `[issue #<N>]` — a repository issue. Issues live in `KJ5HST/methodology`; the fork
  `rmsharp/methodology` has Issues disabled, so entries — authored from either side — cite an
  **absolute URL**, never a bare `#<N>`, and resolve identically from both.
- `[BL-<id>]` — a backlog item, removed from the backlog in the same commit. That backlog is
  [`docs/planning/BACKLOG.md`](https://github.com/rmsharp/methodology/blob/main/docs/planning/BACKLOG.md)
  on fork `main` only — **upstream has no `docs/planning/BACKLOG.md`** — so a `[BL-<id>]` entry
  records work whose origin lives in the fork.
- `[ad hoc]` — work with no backlog or issue origin: releases, tag/branch ops, PR opens, upstream
  issue closes, access grants, and decline/wontfix/grooming decisions.

**Claims.** A session's claim commit carries an *(in progress)* entry here, and its close-out adds its
own (§The Action Ledger, *Lifecycle*). This repo keeps no `SESSION_NOTES.md`, so the Phase 1B crash
breadcrumb is the claim's `status: pending` receipt in [`HANDOFFS.md`](HANDOFFS.md). The pre-commit hook
exempts no claim: one that stages no entry is refused like any other commit.

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

**Everything below the most recent cut is archived, and a cut boundary is POSITIONAL unless the cut
was given a date.** The trimmer's computed cut is positional, not a calendar seam: `2026-08-30`
carries records on *both* sides of it, so a shard's dated filename is in general a **span label, not
a day boundary**; `methodology_trim.py` says so itself (`CUT_STRADDLES_DAY`, design §2.3). **The
newest cut is the other kind** — `--cut 2026-09-17` (S196) took a clean day seam, so that shard's
name *is* a boundary and this file holds 2026-09-18 onward. Read the shard's own front matter, or
the row in the entry that made it, rather than inferring which kind a name is. Every shard is listed in a pointer block below, and **no count is written here** —
the one that was (*"across two shards"*, plus *"this file holds that day forward"*) went stale
eight trims and 24 days ago and was still being read as current at S132. The two earliest spans are
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

**`bin/model-report` used to be the one consumer that lost coverage here. Since S133 (2026-08-31)
it does not.** Its Sources 1 and 2 now read the live ledger **plus every `docs/archive/` shard** by
default, so a split no longer shrinks what it sees. `bin/model-report --changelog <shard>` still
narrows to one file — an **explicit path means exactly that file** and discovers nothing.

**No population figure is written here, deliberately.** A first draft of this paragraph published
*"247 entries across 11 files (live 9 + archived 238)"* in the present tense. It was **already
false when committed**: 247/live-9 was the tree *before* the fix, and the fix commit and this one
each add an entry carrying a `**Model:**` bullet, so the tool reported **249/live-11** at the
moment the sentence was written. An always-read file, a number that rots on the next commit —
the exact defect the rest of this paragraph is about, reintroduced by the session fixing it. **Run
the tool, or the command below.**

**Two claims that stood in this paragraph were stale, and both are recorded rather than quietly
deleted.** It said Source 1 *"matches only the seed's list form `- **Model:**`"* and *"cannot parse"*
this file's bare form, and that a bare run *"reports an empty Source 1"*. Both were true when written
(`020ba3f0`, 2026-08-02) and **false from 2026-08-11**, when `b434183` fixed **BL-20** by widening
`CHANGELOG_MODEL_RE` to accept either dialect. It stood false for **20 days**, during which
**61 receipts** were written (`cat HANDOFFS.md docs/archive/HANDOFFS-*.md | grep -cE '^date: 2026-08-(1[1-9]|2[0-9]|3[01])'`).
The 2026-08-31 entry below says *"roughly ten sessions"* — a guess, stated as a fact, wrong by
6x, in the very entry that criticises an unchecked sentence. It stands there (this ledger is
append-only) and is corrected here and in the entry that follows it. Measured, not recalled. Its cited `bin/model-report:51` had drifted too. **BL-20's residual option
(3) remains open**; only the parser defect closed. The form itself did drift at `1298af7`
(2026-08-02) and has held unbroken since. Count both dialects, never one — a single literal is a
sample, not a population, and the command below is the independent check on the tool's own number
(it counts *lines*, where the tool counts *entries carrying* a bullet; `bin/tests.sh` Test 40 votes
the two against each other rather than merely computing them):

```sh
grep -cE '^-?[[:space:]]*\*\*Model:\*\*' CHANGELOG.md docs/archive/CHANGELOG-*.md
```

**When to archive — the operator's decision, not a rate.** Archiving is optional (§The Action Ledger,
*Archiving is optional*), and `methodology_trim.py --file CHANGELOG.md --check` is the only statement of a
trigger. **The operator decided on 2026-09-14 not to trim this file at that trigger** (`3745748`) and
reaffirmed it at S177 (2026-09-16); **that decision ran to its stated end on 2026-09-19 (S196), and the trim
it deferred was taken** (`0dfca7e`, the entry below). It held until the file came within less than one
session's writing of the 262,144 B hard read refusal (`READ_REFUSE_BYTES`) — 6,284 B at that session's
Phase 0 — and the trim was raised there rather than after the refusal. **What it leaves behind is the same
rule, not a rate:** `--check` firing is not by itself a reason to trim, and a trim is raised with the
operator as this file approaches the refusal — never later than it, since past that line a default read
returns no content at all. Nothing reads this file
whole: Phase 0 takes its frontier from `git log`, close-out prepends under the topmost month, and a
lookup greps; past the refusal, read the top with an offset and a limit. The rate rule that stood here
(archive below 15 entries of headroom to a 2,000-line `READ_CAP_LINES` proxy) went with the seed's
two-cap rule at BL-57's P2; `git show cba2166:CHANGELOG.md` recovers it, with the 2,090-line overrun it
recorded.

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

**Archived 58 record(s), 2026-08-26 → 2026-08-30** into [`docs/archive/CHANGELOG-through-2026-08-30.md`](docs/archive/CHANGELOG-through-2026-08-30.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-08-30.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-30.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

**Archived 54 record(s), 2026-08-12 → 2026-09-02** into [`docs/archive/CHANGELOG-through-2026-09-02.md`](docs/archive/CHANGELOG-through-2026-09-02.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-09-02.md.verify.sh`](docs/archive/CHANGELOG-through-2026-09-02.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

**Archived 65 record(s), 2026-09-02 → 2026-09-14** into [`docs/archive/CHANGELOG-through-2026-09-14.md`](docs/archive/CHANGELOG-through-2026-09-14.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-09-14.md.verify.sh`](docs/archive/CHANGELOG-through-2026-09-14.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

**Archived 104 record(s), 2026-09-14 → 2026-09-16** into [`docs/archive/CHANGELOG-through-2026-09-16.md`](docs/archive/CHANGELOG-through-2026-09-16.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-09-16.md.verify.sh`](docs/archive/CHANGELOG-through-2026-09-16.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

**Archived 126 record(s), 2026-09-16 → 2026-09-17** into [`docs/archive/CHANGELOG-through-2026-09-17.md`](docs/archive/CHANGELOG-through-2026-09-17.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-09-17.md.verify.sh`](docs/archive/CHANGELOG-through-2026-09-17.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

**Archived 79 record(s), 2026-09-18 → 2026-09-19** into [`docs/archive/CHANGELOG-through-2026-09-19.md`](docs/archive/CHANGELOG-through-2026-09-19.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-09-19.md.verify.sh`](docs/archive/CHANGELOG-through-2026-09-19.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

**Archived 54 record(s), 2026-09-20 → 2026-09-20** into [`docs/archive/CHANGELOG-through-2026-09-20.md`](docs/archive/CHANGELOG-through-2026-09-20.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-09-20.md.verify.sh`](docs/archive/CHANGELOG-through-2026-09-20.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

**Archived 48 record(s), 2026-09-20 → 2026-09-21** into [`docs/archive/CHANGELOG-through-2026-09-21.md`](docs/archive/CHANGELOG-through-2026-09-21.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-09-21.md.verify.sh`](docs/archive/CHANGELOG-through-2026-09-21.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

**Archived 85 record(s), 2026-09-21 → 2026-09-22** into [`docs/archive/CHANGELOG-through-2026-09-22.md`](docs/archive/CHANGELOG-through-2026-09-22.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-09-22.md.verify.sh`](docs/archive/CHANGELOG-through-2026-09-22.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

---

## 2026-09

### 2026-09-27 · [BL-60] S231 — the overhead question, measured: the read side is flat, the archive is 76% of the growth

**Asked by the operator mid-session** (*"I am concerned that the overhead associated with using methodology is
growing. Estimate overhead growth."*). Measured over the **32 claim commits S201..S231** (2026-09-20 → 2026-09-27),
bucketing every commit into the session whose claim precedes it:

- **What a session must READ is FLAT, slightly down:** the Phase 0 corpus (`SESSION_RUNNER.md` + `SAFEGUARDS.md` +
  `CLAUDE.md` + `BACKLOG.md` + `HANDOFFS.md`) went **161,197 B → 150,492 B**, slope **−438 B per session**. The
  runner and `SAFEGUARDS.md` did not change by a byte; `BACKLOG.md` fell 13,601 B at the S223 split.
- **What a session LEAVES BEHIND is growing:** tracked bytes **10,017,304 → 11,711,011**, **+55,318 B per session**
  (~215 KB/day at ~3.9 sessions/day). **+23,900 B/session is frozen shards and +17,952 B/session is losslessness
  proofs — together 76% of it.**
- **Per session, median:** 7 commits, ~600 lines into ledgers, **20–45 lines of deliverable**; ledger share of lines
  written 97% (S201–S211) and 92% (S221–S231) — high, roughly flat, not accelerating.
- **The repository at `3c793bf` is 72% process record** — shards 39.4%, plans 14.4%, proofs 11.3%, backlog 3.6%,
  live ledgers 2.5%, learnings 1.1% — against 14.7% tools and tests and 5.6% framework prose.
- **Not instrumented at all:** wall-clock and token cost per session. The byte series above are proxies and are
  labelled as such; building a real instrument is its own costed decision.

**[BL-60](docs/planning/BACKLOG-DETAIL.md#bl-60)'s own figure re-measured and recorded in the item: 31 proofs /
453,689 B / 5.4% when raised, **84 / 1,302,320 B / 11.1%** today.** **The operator chose BL-60's planning session
as the next overhead step** (S231 picker) — the three shapes costed, BL-36 folded in. Method limits stated with the
numbers: the series starts at S201 because `S<N> claim` is a recent commit-subject convention, and one bogus
559-commit bucket between S124 and S201 was discarded rather than reported.

### 2026-09-27 · [ad hoc] S231 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

The `-6` trim's three-line pointer block moved out of `HANDOFFS.md`'s front matter and into
[`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md) as one row (**67 → 68**), per that file's own
fold rule. **Its own commit, as the rule requires:** inside the trim commit the shipped `.verify.sh` fails L2
(fork Learning #58). The shard and its proof are untouched.

### 2026-09-27 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-27-6.md` (1 record(s), 35,783 B → 25,287 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-27 → 2026-09-27) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-27-6.md`](docs/archive/HANDOFFS-through-2026-09-27-6.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-27-6.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-27-6.md.verify.sh)
rather than trusting a digest printed here. Live file 35,783 B → 25,287 B (−29.3%).

### 2026-09-27 · [ad hoc] S231 correction — `--cut N` means KEEP N, so the close-out's "wrong flag" finding was itself wrong

**The pushed close-out entry below says S229's and S230's `--cut 2 --force` forecast used the wrong flag, citing
the front matter's `--cut 1 --force` and S230's one-record trim. That reasoning is false.** `--cut N` is a cut
*point*, not a count of records to archive: measured on this tree at three receipts, `--cut 1` reports *would
archive **2** of 3* and `--cut 2` reports *would archive **1** of 3*. S230 moved one record **because** it passed
`--cut 2`. Both predecessors' forecasts were correct and the accusation is withdrawn; the S231 receipt is
corrected in place and the pushed entry stands as written, corrected by this one.

**What the measurement DID surface is a real, unsettled disagreement about DEPTH.** The `HANDOFFS.md` front matter
states *"keep ONE receipt, trim above TWO"* and prints `--cut 1 --force`; S229, S230 and S231 have each kept
**two**. One receipt or two is an operator question — the S172 decision that set N=1 is quoted in that front
matter — and no session has put it. **This session trimmed at `--cut 2`, the depth its own go-ahead described,
and raises the discrepancy rather than resolving it unasked.**

### 2026-09-27 · [BL-88] S231 — the operator ratifies D1 as Option C: the small pull request first, the stack held

Taken at S231's close-out picker, after the routing plan was written and read back.
[`dashboard-upstream-routing-plan.md`](docs/planning/dashboard-upstream-routing-plan.md)'s status now records it:
**P1 — the root-commit-date correctness pull request — is the next upstream-facing step**, re-derived on a branch
off `upstream/main` (a fork-side fix is not an upstream patch); the read-cap/trim stack that BL-88 rides is built
and vetted fork-side and **held until P1 merges**; F2's signature structure, F3's scoped `--sync` and F4's
self-scan stay out of both. **D2–D6 remain open and none blocks P1. Ratifying the shape is not authorising an
open** — P1's pull request is still its own go-ahead, and so is P3's.

### 2026-09-27 · [ad hoc] Fork `main` pushed to `origin`, `0aeeec1..c3c52a3` — and this record with it

**The operator's explicit go-ahead, asked for in S231's close-out picker and granted there** — **4** commits
(the claim, the routing plan, fork Learning #102, the close-out), beyond the standing CHANGELOG-only grant, which
is why it was asked. Read back with `git ls-remote origin refs/heads/main` → `c3c52a3`, and `origin/main...main`
is 0/0. **Fork `origin` only; nothing was sent to `KJ5HST/methodology`.** **Pushed BEFORE the owed `HANDOFFS.md`
trim, deliberately:** a trim rewrites the file a later reader reconstructs from, so the record of what exists goes
out before the frontier advances. **This entry rides the push it describes** under the standing push-record grant.

### 2026-09-27 · [BL-88] S231 close-out — the route is planned and unratified; the owed `HANDOFFS.md` trim was BLOCKED, not skipped; predecessor scored 9

**Deliverable:** [`docs/planning/dashboard-upstream-routing-plan.md`](docs/planning/dashboard-upstream-routing-plan.md)
(`3aa95f7`), **awaiting the operator's ratification.** Fork-side throughout — no branch, no pull request, nothing on
`KJ5HST/methodology`, where six pull requests still sit open with 0 reviews and nothing is owed.

**Two things this close-out records that are not the deliverable.**

1. **The owed `HANDOFFS.md` retention trim did not run.** The claim made three receipts, so the trim was owed the
   moment it landed; `methodology_trim.py --file HANDOFFS.md --cut 1 --force` was **denied by the harness's
   permission classifier as a dry run**, and no route around it was attempted. The ledger therefore closes at
   **three receipts**, `tests-sh-passed` reads **349** rather than 343, and the trim is the next session's first
   housekeeping act — with `--cut 1`, not the `--cut 2` that S229's and S230's receipts both forecast (the front
   matter and S230's own trim `440183b`, one record, are the authorities). Expect shard `-6`.
2. **Phase 3C appended fork Learning #102 and retired nothing**, naming in the receipt the five rows considered
   (#68, #83, #94, #51, #100) and why none meets the retirement criteria — the D3 obligation discharged by an
   explicit refusal.

**Self 8, predecessor 9.** S230's next_steps (1) was a measured negative result — *P4 has no target*, with the
greps that showed it — and re-running them confirmed every figure, which is what made this session's task
well-formed rather than exploratory. Its one defect is the `--cut 2` forecast above, inherited from S229. Against
this session: an AST set-difference reported **3** fork-only risk rows where reading all 63 appends shows **5**,
and a cited line pair (`:2287`/`:2298`) was wrong and was corrected to `:2319`/`:2320` before the plan was
committed — both caught before publication, neither by the instrument that produced them.

**Gates at `16ffb0f`, in a `--no-local` clone:** `bin/tests.sh` **349 passed / 0 failed / 0 skipped**, exit 0;
`quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results cb3637962fde · manifest 01a4ae7aa511`, exit 0.

### 2026-09-27 · [ad hoc] S231 Phase 3C — fork Learning #102: a `-S` inventory cannot see a merge commit

Appended to [`docs/FORK_LEARNINGS.md`](docs/FORK_LEARNINGS.md) (rows **15..102**, 87 rows, 0 over the 1,500 B
per-row budget). The lesson is this session's own near-miss: a symbol-by-symbol `git log -S` sweep attributed 40 of
42 fork-only scanner names to ordinary commits and returned *nothing in range* for two, both of which are real and
shipped — written **inside** the resync merges `8b87086` and `421ebf9` as the conflict resolutions themselves, and
findable only with `--diff-merges=first-parent`. A route planned around cherry-picks would have carried neither and
would have looked complete by its own method.

**No row was retired, and the rows considered are named in the S231 receipt's `what_was_done`** — the D3 obligation
in [`fork-learnings-retirement-rule-plan.md`](docs/planning/fork-learnings-retirement-rule-plan.md) §6 is discharged
by the explicit refusal, not by silence.

### 2026-09-27 · [BL-88] S231 — the dashboard's upstream route, planned: one dependency stack plus four detachable pieces

**Deliverable:** [`docs/planning/dashboard-upstream-routing-plan.md`](docs/planning/dashboard-upstream-routing-plan.md)
(376 lines), the routing document S230's next_steps (1) said the operator would have to commission. **Fork-side;
nothing was opened, no branch was cut, and every pull request it names is its own go-ahead.** Ratification pending:
§6 carries six decisions, D1 (campaign shape) governing.

**The inventory** (`SESSION_RUNNER.md` §Planning Sessions' mandatory step) was taken symbol-by-symbol from the two
trees — `upstream/main` `6b29d3d` against fork `main` `0aeeec1` — not from the commit list: **42 fork-only top-level
names, 1 upstream-only, 15 shared-but-different, 5 fork-only risk rows, 10 fork-only test classes (123 tests)**.
Upstream's suite is **226 tests, OK, exit 0** in a `--no-local` clone, against the fork's 350.

**What the inventory changed about the answer.** The read-cap work and the trim-trigger row are **one dependency
stack, not two features** — `collect_trim_metrics` reads `read_cap_watch` and calls `read_cap_class()`
(`tools/methodology_dashboard.py:2319`, `:2320`) while BL-88's own P2 calls `find_trim_tool()` — so they cannot be
sent separately. Four pieces detach; one of them **exists only inside merge commits** (`8b87086`, `421ebf9`) and so
can never be cherry-picked; one is a **live defect in the maintainer's shipped tool** (`first_commit_date` reads the
NEWEST commit, 13 lines, 5 tests) and depends on nothing; two are policy changes rather than fixes. Three things
that looked divergent are not — `LANG_MAP`, `detect_doc_only` and `FRAMEWORK_ITEMS` differ **in comments only**.

**No open pull request touches either scanner copy or its test file** (`gh api …/pulls/<N>/files`, all six); the
shared paths are `CHANGELOG.md`, `.quality-gates.json` (#85–#87), `bin/tests.sh` (#84, #86, #87) and
`bin/_manifest.py` (#84). BL-88's index row and detail now point at this plan instead of at a P4 with no target.

### 2026-09-27 · [BL-88] S231 claim — the upstream routing plan for the fork's dashboard divergence (in progress)

**The operator chose this at S231's Phase 0 task picker**, from S230's next_steps (1): BL-88's P4 was measured to
have **no target** — `upstream/main`'s dashboard is **2.11.1** and none of `READ_CAP_CLASS_A`, `READ_CAP_CLASS_B`,
`read_cap_class`, `find_trim_tool` or `collect_trim_metrics` exists there — so the fork's shipped P1 (`cb9b0ed`)
and P2 (`161181c`) can reach an adopter only inside a pull request that first upstreams the rows they sit on.
That routing decision is the operator's to commission, and this session produces the plan for it.

**This session:** one planning document under `docs/planning/`, following `SESSION_RUNNER.md` §Planning Sessions —
a grep-based inventory of what the two copies of `methodology_dashboard.py` actually differ by (the mandatory step
for a migration plan; the change list comes from the searches, not from recollection), a batching of those
differences into pull-request-sized units with a defended order, each phase's DONE criterion, verification command
and **surface**, and a session boundary per phase. **The plan is the deliverable: no dashboard code is changed, no
branch is cut, no pull request is opened, and nothing is sent to `KJ5HST/methodology`,** where six pull requests
sit open with 0 reviews and nothing is owed.

### 2026-09-27 · [ad hoc] Fork `main` pushed to `origin`, `cf60984..4093485` — and this record with it

**The operator's explicit go-ahead, asked for after S230's close-out report**, for the one commit carrying the §3G
correction (S230's `self_score` 8 → 7, BL-79's third occurrence). **This entry is pushed under the standing push-record
grant** — its only change is this `CHANGELOG.md` entry — so it records its own push. Fork `origin` only; nothing to
`KJ5HST/methodology`.

### 2026-09-27 · [ad hoc] S230 correction — the Phase 3G report was not given as one until the operator asked; self_score 8 → 7

The closing messages carried §3G's content — the deliverable, the self-assessment, the predecessor's score and the
next session — but never its shape: no `Close-out report: S230` heading, no labelled sections, no `Session over.`
line. The operator asked for "phase 3 close-out report", which §3G's *"without being asked"* already counts as the
miss. The S230 receipt's `self_score` goes **8 → 7** with the reason in `what_was_done`; the close-out entry stands
as written and is corrected by this one. **BL-79's third occurrence** is recorded in its
[detail](docs/planning/BACKLOG-DETAIL.md#bl-79): the report was displaced by the close-out's own go-aheads, whose
actions changed the state it described.

### 2026-09-27 · [ad hoc] Fork `main` pushed to `origin`, `dc791ae..3582cc6` — and this record with it

**The operator's explicit go-ahead, asked for after S230's close-out**, for the one commit recording the portfolio
dashboard sync and BL-90's count correction. **This entry is pushed under the standing push-record grant** — its only
change is this `CHANGELOG.md` entry — so it records its own push and no further record is owed. Fork `origin` only;
nothing to `KJ5HST/methodology`.

### 2026-09-27 · [BL-90] S230 — the portfolio dashboard copy synced to 2.19.0, its local `EXCLUDE_DIRS` re-applied; BL-90's "9-name" corrected

**The operator's go-ahead, given at S230's close-out.** `~/Development/methodology_dashboard.py` — outside every
repository, so a scratch backup was taken first — went 2.18.0 → **2.19.0** by `--sync ~/Development`, which
overwrote its `EXCLUDE_DIRS` exactly as [BL-90](docs/planning/BACKLOG-DETAIL.md#bl-90) says; the seven local
names were then re-applied, and `diff` against `starter-kit/methodology_dashboard.py` shows that line alone. That
copy had been pre-P1 — the scanner that emitted BL-88's original false flag. **Per-project copies untouched.**

**Correction:** BL-90's ledger entry below and its commit `e8ea062` call the local list *"9-name"*. It is **13
names, the canonical six plus seven local additions**, measured by a set difference against the canonical module.
Corrected in place in BL-90's body, its index row and the S230 receipt; the pushed entry and commit keep the wrong
figure, and this entry is the record of it.

### 2026-09-27 · [ad hoc] Fork `main` pushed to `origin`, `cfe542a..e8ea062` — and this record with it

**The operator's explicit go-ahead, asked for and given at S230's close-out** — **6** commits, beyond the standing
CHANGELOG-only push grant, which is why it was asked rather than assumed. **Fork `origin` only; nothing was sent to
`KJ5HST/methodology`**, where six pull requests still sit open with 0 reviews and nothing is owed.

**What the range carries:** S230's claim; the `HANDOFFS.md` retention trim to `-5` and its fold; the BL-88 P2
deliverable `161181c` (`DASHBOARD_VERSION` 2.19.0); the close-out; and BL-90 with the receipt correction.

**This entry rides the push it describes**, so the record and the state it records land together. Read back with
`git ls-remote` rather than trusting this sentence.

### 2026-09-27 · [BL-90] S230 — raised after close-out: `--sync` overwrites a copy's local `EXCLUDE_DIRS`; the S230 receipt corrected

Found while dry-running, before offering it, the command 2.19.0's stale-copy warning now prints to the portfolio
copy: `--sync ~/Development --dry-run` reports `update methodology_dashboard.py`, 1 of 1 target, with no word about
that copy's local 9-name `EXCLUDE_DIRS` — the edit point the module's own CUSTOMIZATION section invites. **Recorded
as [BL-90](docs/planning/BACKLOG-DETAIL.md#bl-90), not fixed (FM #17), and nothing was synced.** The S230 receipt's
next_steps (2) had called that command *"the remedy"*; it now says what running it would destroy.

### 2026-09-27 · [BL-88] S230 close-out — P2 shipped, 2.19.0; P4 has no upstream target; Phase 3C appended nothing, deliberately; predecessor scored 9

**Deliverable:** `161181c` — the Class B read-cap row names a remedy only where the project's own trimmer source
declares the file. **Fork-side only; no upstream pull request was granted and none was opened.**
**Predecessor 9:** S229's handoff said P2 had no decisions left, and it had none; its `-5` shard forecast and
`--cut 2 --force` were exact; its *mirror last, read the failures as a checklist* gotcha fired twice here (the twin
test, then the version test); its 343/349 floor note told me in advance why `tests-sh-passed` would read 343. **What
it missed:** P1 had left `DASHBOARD_VERSION` unbumped against the file's own rule, which cost a mid-session question,
and P4's premise was carried from the plan unverified. **Self 8:** RED first, P1's rows frozen from the unchanged
module as the independent operand, 26 mutants, 9/9 real trimmers, a real adopter tree including the named remedy
run, and P4's premise measured. Against it: a count written from recollection into code and a test (caught before
commit), a first fleet diff taken across a live session, and a status guard that could not name its failing repo.

**P4 HAS NO TARGET, MEASURED.** `upstream/main`'s dashboard is 2.11.1 and carries none of the read-cap class code P1
and P2 change (`READ_CAP_CLASS_A`, `READ_CAP_CLASS_B`, `read_cap_class`, `find_trim_tool`, `collect_trim_metrics`:
0 each), and none of the six open PRs touches either dashboard copy. Recorded in BL-88's
[detail](docs/planning/BACKLOG-DETAIL.md#bl-88), its index row, and a note under the
[plan](docs/planning/dashboard-read-cap-class-adopter-drift-plan.md)'s P4; not costed. All three `docs/planning/`
proofs exit 0 after the edit.

**Verification at the deliverable commit**, in a `--no-local` clone at `161181c`: `quality_ratchet: 11/11 pass · 0 fail ·
0 unmeasured · results 2f8fe36c7a92 · manifest 01a4ae7aa511`, exit 0 — `tests-sh-passed` 343, dashboard 350.

**PHASE 3C APPENDED NO ROW AND THAT IS THE RESULT, NOT AN OMISSION.** The candidates — a plan phase that presupposes
code the other tree lacks, a fleet before/after taken across a live session, a count written from recollection —
are stated at least as generally by fork Learnings **#57** (an option nobody has executed is a proposal), **#79**
(read each text on the tree that ships it), **#74** (another repository's state is a reading with a time on it) and
**#18** (run the artifact; name the command). Appending would restate them less generally, so nothing was appended
and **no retirement is owed** — D3 is keyed to appending. Rows considered: #57, #79, #74, #18, #59.

### 2026-09-27 · [BL-88] S230 — P2: the Class B read-cap row names a remedy only where the project's own trimmer source declares the file; `DASHBOARD_VERSION` 2.19.0

**What changed** (`tools/methodology_dashboard.py`; the `starter-kit/` twin mirrored last, `cmp` identical):
`_parse_trim_ledgers()` reads the basenames a trimmer's `LEDGERS` table declares **from its source**, with
`ast.parse` — a parse that runs nothing, per the operator's *source-text read, never an execution* — and returns
`None` whenever the source alone cannot vouch for the table (no single module-level dict display, a computed or
non-string key, `**` unpacking, any other binding of the name, a subscript store or delete, a non-reading method).
`find_trim_tool()` carries it as `ledgers`, `collect_trim_metrics()` as `tool_ledgers`. Where that reading lists a
Class B file's **basename** — the key the trimmer itself looks up — the over-cap row appends *"BUT THIS PROJECT HAS
A REMEDY: … run `python3 <tool> --file <path> --check` …"* and drops HIGH → **LOW**, Class A's severity (plan §8 P2).
Anything else leaves P1's row **byte for byte**. **The class does not move:** `READ_CAP_CLASS_A`/`_B`,
`read_cap_class()`, both pins and the trim row's Class A population are untouched — dragon 6 not engaged.

**A judgment inside the decided option, stated:** a parse rather than a grep, because a grep cannot tell an entry
from a mention — `nprcgenekeepr`'s trimmer spells `SESSION_NOTES.md` on three lines and one is a key.
**`DASHBOARD_VERSION` 2.18.0 → 2.19.0 is the operator's choice this session**, per the file's own *"bump on any
change"*; it covers P1 too, which shipped without one, and it is what makes older fleet copies say they are stale.

**Verified:** RED first — the 12 new tests, as first written, failed **5 times and errored 22** before the edit,
each for the expected reason; the abstention cases added after the fix are proved by mutation instead. After, `python3 tools/test_methodology_dashboard.py` **350 tests OK (skipped=4)**. **Mutation: 26 mutants,
25 killed; the survivor is equivalent** (`getattr(t, "id", None)` for an `isinstance` check only `ast.Name`
satisfies), and dropping that check outright is killed. **Faithfulness on real trimmers:** the source reading
equals the keys each trimmer defines when imported — in a verification subprocess, never the scanner — on
**9 of 9** (the 8 fleet trimmers and canonical), `nprcgenekeepr`'s widened one included. **On a real adopter
tree:** a `--no-local` clone of `nprcgenekeepr` with `SESSION_NOTES.md` padded to 94,669 B — P1 **HIGH**, P2 **LOW**
with the remedy, and the named `--check` runs there, exit 0, a full report and no `NO_CONFIG`. **Fleet diff,
back to back per project:** **0 of 49 rows changed** across 8 projects and 31 watched files — the right answer
today, since no declared Class B file is over the cap (`nprcgenekeepr/SESSION_NOTES.md` is ~33 KB); the reading
itself lists `SESSION_NOTES.md` for `nprcgenekeepr` alone. Scanned in-process, so nothing was written to
`~/Development/dashboard.html`. One repo's `git status` differed after the scan; the script did not name it, and
the only files modified in that window were `nprcgenekeepr`'s R sources and man pages (a live session there) and
this repo's own edits — so it is attributed, by that reconstruction, to `nprcgenekeepr`.
Fork-only; **no PR granted, nothing on `KJ5HST/methodology`.**

### 2026-09-27 · [ad hoc] S230 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

**456 B of front matter becomes a 124 B row** in [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md); rows **66 → 67**.
Its own commit, per the index's fold rule and fork Learning #58. `HANDOFFS.md` 16,689 → 16,233 B.

### 2026-09-27 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-27-5.md` (1 record(s), 26,017 B → 16,689 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-27 → 2026-09-27) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-27-5.md`](docs/archive/HANDOFFS-through-2026-09-27-5.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-27-5.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-27-5.md.verify.sh)
rather than trusting a digest printed here. Live file 26,017 B → 16,689 B (−35.9%).

### 2026-09-27 · [BL-88] S230 claim — P2: the read-cap row reads each project's trimmer source before it names a remedy (in progress)

**The operator chose this at S230's Phase 0 task picker** — the plan's next phase,
[`dashboard-read-cap-class-adopter-drift-plan.md`](docs/planning/dashboard-read-cap-class-adopter-drift-plan.md) §8 P2.
**Its one sub-decision was taken at S228's report: a SOURCE-TEXT read, never an execution** — no adopter code runs
inside the scanner. P1 (`cb9b0ed`) is on fork `main`, which under the operator's fork-only choice is the "merged"
the phase's precondition asks for.

**This session:** the Class B over-cap row (`tools/methodology_dashboard.py:3510-3556`) gains a remedy sentence and
drops to the Class A severity **only** where the scanned project's own `methodology_trim.py` source declares a
`LEDGERS` entry for that file. **The failure path is the criterion:** no trimmer, no entry, or a source that cannot
be read or parsed leaves the row **byte-identical** to P1's. The class stays declared — `READ_CAP_CLASS_A`/`_B`
(`:423-428`) and both pins (`tools/test_methodology_dashboard.py:5464`, `:5485`) untouched, so dragon 6 is not
engaged. RED-first tests for all three outcomes, the load-failure arm on a deliberately broken fixture trimmer;
`starter-kit/` twin mirrored **last**; the plan's P3 fleet diff re-run read-only. Fork-only — **no PR granted,
nothing on `KJ5HST/methodology`.**

### 2026-09-27 · [ad hoc] Fork `main` pushed to `origin`, `ab73d31..c82431d` — and this record with it

**The operator's explicit go-ahead, asked for and given at S229's close-out** — **21** commits, well beyond the standing
CHANGELOG-only push grant, which is why it was asked rather than assumed. **Fork `origin` only; nothing was sent to
`KJ5HST/methodology`, where six pull requests still sit open with 0 reviews and nothing is owed.**

**What the range carries:** S227's decision on BL-88 and fork Learning #100; S228's `CHANGELOG.md` archive at the
2026-09-22 seam (85 records, 249,268 → 130,729 B) and fork Learning #101; S229's shipped fix to the read-cap row and
BL-89; three `HANDOFFS.md` retention trims with their folds (`-2`, `-3`, `-4`); and the repair of the duplicated
S227 receipt.

**This entry rides the push it describes**, so the record and the state it records land together — the one-behind
regress S219–S224 carried, ended at S225 and kept ended here. Read back with `git ls-remote` rather than trusting
this sentence.

### 2026-09-27 · [BL-89] S229 — BL-89 raised: `bin/check-handoff` passed three differently-broken ledgers in three sessions

**Raised at the operator's request after S229's close-out report, written from what is already known and NOT
investigated** — the post-close-out discipline for new information (fork Learning #17's family).

`bin/check-handoff` validates the **newest receipt's 13-key schema** and that older blocks name a sha. **Nothing
asserts the ledger's record structure**, so two shapes passed at **exit 0**: (a) a receipt spliced into the front
matter's own `` `grep -c '^```handoff' HANDOFFS.md` `` example, where the checker found one block and reported
*"all **0** older receipt(s)"* — its own count contradicting the file it had just validated; and (b) a duplicated
`session:` number, once shipped (S227, repaired at `3815b83`) and twice caught by hand before committing (S228,
S229).

**The stake is the archive:** the retention trim freezes the oldest receipt into a shard with a losslessness proof,
so a duplicate that survives one more session becomes a permanent record that the proof correctly certifies.
Adjacent to **BL-73** — whether this is a distinct item or BL-73's second and third shapes is itself open.
Canonical-only. **Nothing costed; the three obvious checks are named as starting points, not as a decision.**

### 2026-09-27 · [BL-88] S229 close-out — P1 shipped; Phase 3C appended nothing, deliberately; predecessor scored 9

**Deliverable:** `cb9b0ed` — the read-cap row asserts only what it evaluated. **Fork-side only; no upstream pull
request was granted and none was opened.** **Self 8, predecessor 9:** S228's `-4` shard forecast was exact, its
numbers were re-derived rather than quoted at three separate readings, and **the `grep -c '^session: '` check it
wrote into its gotchas caught this session's own duplicated receipt before it committed** — twice, counting S228's.
A handoff that prevents its successor's error is doing the job the scoring exists to reward.

**Verification, RED first.** Two new tests failed **5 times** across the four Class B names before the edit; after
it, `tools/test_methodology_dashboard.py` is **338 tests OK**, with both class pins unchanged. In a `--no-local`
clone at the final tree `d34bd5b`: `bin/tests.sh` **343 passed / 0 failed / 6 skipped** — the `>= 343` floor exactly
— and `quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results 22227e3813bb · manifest 01a4ae7aa511`.
**Fleet diff, read-only, both module versions, real sizes: 3 rows changed, 29 identical, 32 watched files, no
severity moved anywhere.**

**PHASE 3C APPENDED NO ROW AND THAT IS THE RESULT, NOT AN OMISSION.** The candidate lesson — *a ratchet floor
measured mid-session can be tightened to a number the next close-out refuses* — **is already stated more generally,
with this exact mechanism, by fork Learning #70**, which names `bin/tests.sh` Test 34, its six stated skips and the
two-versus-three receipt population. It earned its keep here: `tests-sh-passed` read **349** at the fix and **343**
at the final tree, and tightening to 349 would have gone red at the next trim. Appending would have restated #70
less generally, so nothing was appended and **no retirement is owed** — D3 is keyed to appending. Rows considered:
**#70** (the match), **#41**, **#32**, **#30**.

### 2026-09-27 · [ad hoc] S229 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

**452 B of front matter becomes a 122 B row** in [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md); rows **65 → 66**.
Its own commit, per the index's fold rule and fork Learning #58. `HANDOFFS.md` 15,732 → 15,276 B.

### 2026-09-27 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-27-4.md` (1 record(s), 27,548 B → 15,732 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-27 → 2026-09-27) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-27-4.md`](docs/archive/HANDOFFS-through-2026-09-27-4.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-27-4.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-27-4.md.verify.sh)
rather than trusting a digest printed here. Live file 27,548 B → 15,732 B (−42.9%).

### 2026-09-27 · [BL-88] S229 — the read-cap row asserts only what it evaluated: the trimmer claim is gone, the backlog reason is per-name

**P1 of [`dashboard-read-cap-class-adopter-drift-plan.md`](docs/planning/dashboard-read-cap-class-adopter-drift-plan.md)
§8, the operator's decision at S228's report. Fork-side only — no upstream pull request was granted.**

**Two false things left the Class B over-cap row** (`tools/methodology_dashboard.py:3511`, now `:3511-3556`):

1. ***"the trimmer answers `NO_CONFIG` for it"*** — a fact about a **neighbouring tool's config table**, read from
   nothing. True in this repository only because `LEDGERS` and the declared classes coincide, and **false in any tree
   that widened `LEDGERS`** — which is where this module is *distributed* and its suite is not.
2. ***"a backlog's bottom items are as live as its top ones"*** printed for `SESSION_NOTES.md`. **The comment eleven
   lines above `READ_CAP_CLASS_B` already recorded that as a caught over-generalisation and stated the weaker true
   form; the correction reached the comment and never the row.** The reason is now selected per name: backlogs keep
   theirs, and a session-notes file gets *"nothing ENFORCES that the part you need is inside that prefix"*.

**Nothing about the classification changed.** `READ_CAP_CLASS_A`/`_B` are still declared literals, `READ_CAP_WATCHED`
is still derived from them, no name moved class, and **both pinning tests at `:5464` and `:5485` pass unchanged** —
§10 dragon 6 is not engaged, because the row now asserts *less*, not differently.

**RED first, and the one test that pinned the false claim was RE-POINTED, not deleted.**
`test_a_class_B_file_over_the_cap_is_still_HIGH_and_says_why` asserted `"NO_CONFIG"` was present; its purpose — the
row exists, is HIGH, and says why — survives, so it now pins *"the instructed access path IS the file"* and its
docstring records the change and why. Two new tests were written first and **both failed before the edit** (5
failures across the four Class B names): `test_the_class_B_row_makes_NO_CLAIM_about_any_trimmer_config` forbids any
mention of the trimmer, and `test_the_backlog_justification_is_printed_ONLY_for_the_backlogs` pins the split both
ways. The `starter-kit/` twin was mirrored **last** and `cmp`s identical.

**FLEET DIFF, read-only, against the real portfolio: 3 rows changed, 29 identical, 32 watched files.** No severity
moved anywhere. `model_project_constructor/BACKLOG.md` (98,284 B) and `wsfct/BACKLOG.md` (157,351 B) lose only the
trimmer claim; `model_project_constructor/SESSION_NOTES.md` (91,593 B) gets the weaker form.
**`nprcgenekeepr/SESSION_NOTES.md` no longer appears at all** — it fell to 19,719 B when a live session there
archived it, so the flag that prompted BL-88 is currently dormant, and this fix is why it will not come back false.

### 2026-09-27 · [BL-88] S229 claim — the read-cap row stops asserting what it never checked (in progress)

**The operator's decision, taken at S228's report:** fix the warning text, **fork-side only — no upstream pull
request**, and add the trimmer probe as a **source-text read**, not an execution. The probe is the plan's P2 and is
**not this session** ([`dashboard-read-cap-class-adopter-drift-plan.md`](docs/planning/dashboard-read-cap-class-adopter-drift-plan.md) §8);
it now carries zero open decisions.

**This session is P1 only:** the Class B over-cap row at `tools/methodology_dashboard.py:3511-3528` drops
*"the trimmer answers `NO_CONFIG` for it"* — a claim about another tool's configuration that the dashboard never
reads — and stops printing the **backlog-specific** *"a backlog's bottom items are as live as its top ones"* for
`SESSION_NOTES.md`, which the module comment at `:381-396` already corrected in prose and never in the row.

**RED first, and one existing test must change deliberately rather than be deleted:**
`tools/test_methodology_dashboard.py:5800` asserts `"NO_CONFIG" in rows[0]["description"]`. Its purpose — *Class B
rows STAY and say why* — survives; only the *why* changes. The two class pins at `:5464` and `:5485` are **untouched**:
no name moves between classes and nothing becomes derived. The `starter-kit/` twin is mirrored **last**.

### 2026-09-27 · [ad hoc] S228 close-out — `CHANGELOG.md` archived at the 2026-09-22 seam; predecessor scored 8

**Deliverable:** `d23c811` — 85 of 137 records to `docs/archive/CHANGELOG-through-2026-09-22.md`, live
**249,268 → 130,729 B**, headroom against the 262,144 B refusal from about **13,000 B to 131,415 B**. **Self 8,
predecessor 8.** S227 earns the 8 on two forecasts that proved exact — the `-3` shard name and its contents — and on
a decision document that made this session's choice mechanical; against that, **its close-out left a duplicated
`session: S227` receipt** that this session had to repair before claiming (`3815b83`), and `bin/check-handoff`
passed it.

**And the same defect recurred here, caught by the gotcha S227's repair produced.** The S228 close-out receipt was
prepended over its own pending stub, giving two `session: S228` blocks; the `grep -c '^session: '` check written into
gotcha (1) found it immediately and the stub was removed before this commit. **A checker that validates the newest
record's schema does not validate the file's record structure** — two differently-broken trees have now passed
`bin/check-handoff` in two sessions.

**Verification at `c72ad24` in a `--no-local` clone:** `bin/tests.sh` **343/0/6** — the floor exactly, which matters
because Test 34 mutates `HANDOFFS.md` and this session trimmed it; `quality_ratchet: 11/11 pass · 0 fail · 0
unmeasured · results 10575dac7361 · manifest 01a4ae7aa511`, identical to S227's. **Both shard proofs exit 0, each
read from a clone of its own trim commit.**

**On the adopter question the operator asked:** answered from that project's own contract, which **overturned this
session's first reading** — `nprcgenekeepr/CLAUDE.md:256` ratifies `--budget-bytes 65536` on every run, and its
`SESSION_NOTES.md` fell 57,871 → 19,719 B mid-session when a live session there archived it with the local patch
under investigation. **Nothing is owed in that project**; the canonical prose defect BL-88 decided is untouched and
recurs when that file re-crosses the cap. Fork Learning **#101** carries the method lesson.

### 2026-09-27 · [ad hoc] S228 — Phase 3C: fork Learning #101, and D3 discharged by an explicit refusal

**Row #101** (1,419 B, inside the 1,500 B `ROW_BUDGET_BYTES`): running another project's tool with **your** default
invocation measures the **tool**, not that project — and its tree can move under you while you reason about it. Both
halves were earned this session: `nprcgenekeepr`'s `CLAUDE.md` ratifies `--budget-bytes 65536` **on every run,
`--check` included**, and my bare `--check` read the 196,608 B default instead; then the file I had measured at
57,871 B read **19,719 B** forty minutes later, because a live session there archived it with the very local patch
under investigation. `check-learnings` → **OK, 86 rows, contiguous 15..101, 0 over budget.**

**D3 discharged by an explicit REFUSAL; the rows considered were #100, #61, #23 and #12.** **#100** (this session's
predecessor row) is the cross-artifact *declared vs derived* lesson and is not about invocation or staleness.
**#61** — *a document waiting for approval keeps measuring the tree it was written against* — is the closest
neighbour and is what #101 leans on, but it is about **your own** tree at publish time; #101 is about **someone
else's** tree and their documented invocation, which #61 does not reach. **#23** (an item's defect claim is frozen
at filing time) and **#12** (a hand-maintained count is stale by the next close-out) are the same staleness family
one step further out. None meets D1(a) — no gate, test or numbered failure mode enforces their lessons; none meets
D1(b); none meets D1(c). Per `fork-learnings-adjudication-2026-09-20.md` §5 the table was tested at S200 and none
retired; this refusal does not re-adjudicate it.

### 2026-09-27 · [ad hoc] S228 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

**452 B of front matter becomes a 122 B row** in [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md);
rows **64 → 65**. Its own commit, per the index's fold rule and fork Learning #58 — inside the trim commit the
shipped `.verify.sh` fails L2. `HANDOFFS.md` 18,138 → 17,682 B.

### 2026-09-27 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-27-3.md` (1 record(s), 29,818 B → 18,138 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-27 → 2026-09-27) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-27-3.md`](docs/archive/HANDOFFS-through-2026-09-27-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-27-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-27-3.md.verify.sh)
rather than trusting a digest printed here. Live file 29,818 B → 18,138 B (−39.2%).

### 2026-09-27 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-09-22.md` (85 record(s), 249,268 B → 130,729 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **85** record(s) (2026-09-21 → 2026-09-22) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-09-22.md`](docs/archive/CHANGELOG-through-2026-09-22.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-09-22.md.verify.sh`](docs/archive/CHANGELOG-through-2026-09-22.md.verify.sh)
rather than trusting a digest printed here. Live file 249,268 B → 130,729 B (−47.6%).

### 2026-09-27 · [ad hoc] S228 claim — archive this file at the clean 2026-09-22 calendar seam (in progress)

**The operator chose the cut: `--cut 2026-09-22`, the clean calendar seam** — one of three options costed by forced
dry runs at S227's Phase 0 and raised there on the refusal, not on `--check`, per this file's own rule since S196.

**Re-derived at claim time rather than quoted** (fork Learning #61): the file is **248,167 B** and holds **137**
records, not the 236,905 B / 130 the options were costed against — S227 added seven entries, all dated 2026-09-27
and therefore all on the RETAINED side. The cut still archives **85 of 137** (2026-09-21 → 2026-09-22) into
`docs/archive/CHANGELOG-through-2026-09-22.md`, a name no shard has taken, and leaves the live file at
**129,628 B** — not the 118,366 B quoted at S227, because the retained side grew.

**`SRF_RED` refuses this trim by construction and `--force` is warranted, not an override.** There is **no fold**
for this file, and the trim pays the same fixed ~16 KB losslessness proof, read from a clone of its own commit.

### 2026-09-27 · [ad hoc] S227 correction — the close-out left the Phase 1B stub in place beside its own receipt

**Phase 3D says the claim stub is OVERWRITTEN by the close-out receipt; mine was PRECEDED by it,** so `HANDOFFS.md`
carried **two `session: S227` blocks** — the complete receipt at `:53` and the stale `status: pending` stub at `:69`.
Cause: the close-out did `git checkout -- HANDOFFS.md` to undo an over-budget draft, which restored the committed
stub, and then prepended the finished receipt instead of replacing it. The stub is removed here (1,500 B), leaving
**2 receipts**.

**`bin/check-handoff` reported OK, exit 0, on both trees** — it validates the newest receipt's schema and that older
ones name a sha, and **nothing checks that a session number appears once.** A duplicate is invisible to it. This is
the same blind spot family as **BL-73** (a receipt begun twice reads as one block); recorded here, not fixed, and it
is now the second `check-handoff` gap this session found.

**Caught before it could be frozen:** the next retention trim archives the oldest receipt, which would have written
the duplicate into a shard and into that shard's losslessness proof.

### 2026-09-27 · [ad hoc] S227 close-out — the read-cap class decision is recorded; predecessor scored 9

**Deliverable:** the decision on BL-88, `cd7d422`, with fork Learning #100 at `a2885d5`. **Self 8, predecessor 9.**
S226 earns the 9 on verified predictions rather than on tone: its forecast of the retention trim was **exact** (the
`-2` suffix, S225's receipt, the shard name), its gate citation reproduced **hash for hash**, and four of its
gotchas were load-bearing for this session. Against that, it left a rendering defect its own commit introduced —
the blank line orphaning BL-87's index row — while its receipt reported that file's byte count as an improvement.

**Verification at `a2885d5` and in a clone at `cd7d422`:** `bin/tests.sh` **343/0/6**;
`quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results 10575dac7361 · manifest 01a4ae7aa511`, identical to
Phase 0's; all three `docs/planning/` proofs exit 0; `bin/check-links` OK 111 links; `check-learnings` OK 85 rows
contiguous 15..100; `context_budget.py --precommit` exit 0; `bin/check-handoff` OK.

**`CHANGELOG.md` at this close-out is the one thing the next session must read first.** It is now within about one
session's writing of the 262,144 B hard read refusal, three cuts are costed, and the choice is the operator's.

### 2026-09-27 · [ad hoc] S227 — Phase 3C: fork Learning #100, and D3 discharged by an explicit refusal

**Row #100** (1,484 B, inside the 1,500 B `ROW_BUDGET_BYTES`; recomposed twice from 1,617 B rather than trimmed
at the edges): two artifacts can answer the same question by **opposite mechanisms** — one deriving, one
declaring — and only the test comparing them holds them equal; ship one without the test and the coupling
exists nowhere it matters. `bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations` →
**OK, 85 rows, contiguous 15..100, 0 over budget.**

**D3 discharged by an explicit REFUSAL: no row qualifies for retirement, and these are the ones considered.**
**#96** — *a prior reduction's losslessness proof becomes a constraint on the next reduction; fix the reduction,
not the proof* — is the row this session's F7 would have restated **less** generally, so F7 was **not written as
a row at all**; #96 is the general statement and retiring it would lose the lesson it states. **#43** — a
derived set's coverage is uncheckable against itself — is #100's sibling *inside one module* and is cited by it;
#100 is the cross-artifact form, so neither subsumes the other. **#24** is qualified by #96 rather than
superseded (#96 says its remedy is wrong in the reachability case). **#28** and **#61** are about records going
stale, adjacent to BL-32's falsified sentence but not about it. None meets D1(a) — no gate in
`.quality-gates.json`, test in `bin/tests.sh` or numbered failure mode now enforces any of their lessons; none
meets D1(b); none meets D1(c) — every artifact they name still exists. Per
[`fork-learnings-adjudication-2026-09-20.md`](docs/planning/fork-learnings-adjudication-2026-09-20.md) §5, the
whole table was tested against the criterion at S200 and **none** retired; this refusal does not re-adjudicate
it, and re-adjudication remains its own deliverable.

### 2026-09-27 · [BL-88] S227 — DECIDED: the dashboard's row will assert only what it has checked; BL-88 raised

**The relayed drift is real and it is the symptom.** `methodology_trim.py` **derives** a file's read-cap
class (`is_root_class_a()`, `starter-kit/methodology_trim.py:947`, assigned `:971`) from its own `LEDGERS`
table plus root position; `methodology_dashboard.py` **declares** it (`tools/methodology_dashboard.py:423-424`),
deliberately, because deriving would let a widened `LEDGERS` silently reassign a class
(`docs/planning/read-cap-phase-c-plan.md:381`, dragon 6). The two pins that couple them
(`tools/test_methodology_dashboard.py:5464`, `:5485`) both load **this** repo's trimmer, and that suite is
**absent from `bin/_manifest.py`** — so dragon 6 holds only where a test runs, and `nprcgenekeepr`'s widening
was invisible rather than caught.

**But the false clause is one sentence of prose, and the larger defect is canonical.** The Class B row asserts
*"the trimmer answers `NO_CONFIG` for it"* — a claim about another tool's config in a tree it never inspects,
false in `nprcgenekeepr` — and it imports the **backlog-specific** justification onto all four Class B names
including `SESSION_NOTES.md`, which the module comment at `:381-396` **already records as a caught
over-generalisation** and states in a weaker form the row never received. That second defect is in every
adopter tree and owes nothing to any local patch; it is what justifies changing anything.

**Decision, awaiting ratification** ([`dashboard-read-cap-class-adopter-drift-plan.md`](docs/planning/dashboard-read-cap-class-adopter-drift-plan.md)):
**Part 1** — the row asserts only what it has checked; no new mechanism, no derivation, both pins untouched.
**Part 2, optional** — a per-project trimmer probe that may only *add* a remedy and lower a severity, never
select a class, so dragon 6 is not engaged; measured feasible at **3.6 ms per project** across 12. Distributing
the pins and adopter-side-only documentation **rejected** with reasons; an adopter class-override config
**superseded** by the finding that the flag came from the **portfolio** copy, one declared partition over N
projects with N trimmers. `starter-kit/methodology_dashboard.py` is DISTRIBUTED, so **Part 1 is upstream-facing
and its PR is its own go-ahead**. Nothing implemented; no adopter edited.

**Verified, not taken on trust:** the adopter's dashboard is byte-identical to both canonical copies (v2.18.0);
its trimmer carries a documented 51-line local `SESSION_NOTES.md` `LedgerSpec` since 2026-08-11; its `--check`
returns a Class-A reading and *"trigger does not fire"*; the relay's 56,752 B is now **57,871 B**, 1,121 B over
the cap. `nprcgenekeepr` is the **only** one of 8 trimmer-carrying fleet projects ever to widen `LEDGERS`, so
exactly one flag is affected — which **falsifies BL-32's** *"No project … has ever extended `LEDGERS`"*, on the
day BL-32 was raised.

**That correction could not be written where the false sentence is, and the checker said so.** BL-32's body is
among `BACKLOG-DETAIL.md.verify.sh` C2's frozen 18: the in-place edit was written, run — `FAIL C2 BL-32: body
differs — 5820 B at 384b17c, 6391 B in detail` — and **reverted**, the proof re-run green. Editing the proof to
admit the edit would be a loosening (`SAFEGUARDS.md`). The correction lives in **BL-88's** body instead. **A
frozen body cannot receive a factual correction in place.**

**One repair rides this commit and is disclosed rather than bundled quietly:** the stray blank line S226's
`9cf85f2` left above BL-87's index row is removed. It orphaned the row into a headerless table fragment, and
BL-88's own row lands directly beneath it, so the index could not render correctly without it. No go-ahead was
given for it; it is a prerequisite of this commit's own edit, not an extra.

### 2026-09-27 · [ad hoc] S227 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

**The trim's own 452 B pointer block removed from `HANDOFFS.md`'s front matter and rewritten as one 122 B row
in [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md)** — the index's rows went **63 → 64**
(`git show HEAD:` for the before, so the count excludes this change). Its own commit, per the index's fold
rule and fork Learning #58: inside the trim commit the shipped `.verify.sh` fails L2. `HANDOFFS.md`
18,290 → 17,834 B. The proof was read from a clone of the trim commit `525c9aa` first — **exit 0**, L1, L2 and
L3 all holding, 3 records = 2 retained + 1 archived.

### 2026-09-27 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-27-2.md` (1 record(s), 30,038 B → 18,290 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-27 → 2026-09-27) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-27-2.md`](docs/archive/HANDOFFS-through-2026-09-27-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-27-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-27-2.md.verify.sh)
rather than trusting a digest printed here. Live file 30,038 B → 18,290 B (−39.1%).

### 2026-09-27 · [ad hoc] S227 claim — the dashboard's declared read-cap Class A/B vs an adopter's locally patched trimmer (in progress)

**Relayed by the operator from `nprcgenekeepr`, and assigned as a design decision, not a prescribed fix.**
`tools/methodology_dashboard.py` declares `READ_CAP_CLASS_A` and `READ_CAP_CLASS_B` rather than deriving them
from `methodology_trim.py`'s `LEDGERS` — deliberately, so a widened `LEDGERS` cannot silently reassign a file's
class (module comment; `docs/planning/read-cap-phase-c-plan.md` §10 dragon 6). Two canonical tests pin the
invariant from both sides, and **both load this repo's own trimmer**, so they pin consistency *here* and say
nothing about an adopter's copy. `nprcgenekeepr` carries a documented, deliberately unsynced `LedgerSpec` for
`SESSION_NOTES.md` while running a byte-identical dashboard, so the dashboard asserts `NO_CONFIG` for a file
whose trimmer now answers with a full Class-A reading — the failure mode the Class B test's own docstring names,
in a tree no test suite reaches.

**The deliverable is ONE decision document, not an implementation:** the investigation, every shape costed
against measurements, and the decision. Five candidate shapes arrived with the relay; none is costed, and the
relay explicitly invites a sixth. Nothing is implemented without a go-ahead at the Present gate. The adopter's
report is treated as a **claim to verify**, not as a measurement.

### 2026-09-27 · [ad hoc] S226 — this file re-measured AFTER its own close-out entries: 235,768 B, ~1.6 sessions

**The figure in S226's receipt is correctly scoped and its conclusion is now stale, which is the whole point of
re-measuring.** The receipt says **230,783 B** *"immediately before this close-out's entries"* and tells the reader
to re-measure rather than quote it (fork Learning #61). Measured after them, and after the push record: **235,768 B**
(`wc -c`), leaving **26,376 B** to the 262,144 B `READ_REFUSE_BYTES`.

**The rate, re-derived over two whole sessions rather than one partial span:** 203,621 → 235,768 = **32,147 B across
S225 and S226**, or **16,074 B per session**, which puts the refusal **about 1.6 sessions away** — not the ~2 the
receipt derived and not the ~4 S225's did. Each estimate was honest about its own basis; only the span changed.
**The next session raises the trim at its Phase 0 report** — on the refusal, which is this file's own rule since
S196, and not on `--check`, which fires and will keep firing. There is no fold for this file and its trim pays the
same fixed ~16 KB proof.

### 2026-09-27 · [ad hoc] S226 — fork `main` pushed to `origin`, `31e16e4..849ae4a` (non-commit action, operator go-ahead)

**Six commits, a clean fast-forward, every guard measured immediately before the push and the result read back
after.** `origin/main` was at the expected **`31e16e4`**, `git rev-list --count main..origin/main` **0** (nothing to
rebase onto), `git rev-list --count origin/main..main` **6**, `git merge-base --is-ancestor origin/main main`
**YES**, tree clean with 0 uncommitted files. After: `git ls-remote --heads origin main` reads **`849ae4a`**, and a
re-fetch puts `origin/main` level with local `main` (0 ahead, 0 behind). **`upstream/main` was re-read and is
unchanged at `6b29d3d`** — nothing was sent to `KJ5HST/methodology`, and no branch was pushed.

**The count was measured, not carried.** `git log --oneline --no-merges origin/main..main` enumerated the six: the
S226 claim (`7e48608`), the owed `HANDOFFS.md` retention trim (`6a85d20`) and its fold (`1201b12`), BL-86's fix with
BL-83 closed and BL-87 raised (`9cf85f2`), fork Learning #99 (`86713df`), and the close-out (`849ae4a`). Eleven
files across them, listed by `git diff --name-only origin/main main`.

**This entry is pushed with the tip it records, under the operator's standing grant of 2026-09-16** — *a commit
whose only change is the `CHANGELOG.md` entry recording an authorized push is pushed to `origin` without asking,
and records its own push in the same entry.* Its guards are re-measured and the result read back with
`git ls-remote` immediately after. S219–S224 each left the recording commit behind; `d7b3be8` ended that regress
and keeping it ended is what this paragraph is for.

### 2026-09-27 · [BL-86] S226 close-out — the closure rule is executable again; predecessor scored 8

**Deliverable complete and verified.** BL-86 fixed and closed, BL-83 closed with it and its owed pointer row
written, BL-87 raised, fork Learning **#99** appended with D3 discharged by explicit refusal. `7e48608` (claim),
`6a85d20` (retention trim), `1201b12` (fold), `9cf85f2` (deliverable), `86713df` (#99), and this close-out.
**Fork-only; nothing was pushed and nothing on `KJ5HST/methodology` was touched.**

**Gate and suite in a `--no-local` clone at `86713df`, exit codes read outside a pipe:** `bash bin/tests.sh`
**343 passed / 0 failed / 6 skipped**, exit 0 — the `tests-sh-passed >= 343` floor exactly; `quality_ratchet:
11/11 pass · 0 fail · 0 unmeasured · results 10575dac7361 · manifest 01a4ae7aa511`, exit 0 — the same hashes as
Phase 0's at `31e16e4` and S225's at `2f17170`, right for doc-only edits. All three `docs/planning/` proofs exit 0,
and **six negative controls fire on the shipped proof** with the control green after every revert.

**Phase 3A — S225's handoff scored 8/10.** Its trim forecast was exact and its gotchas were measurements, not
impressions: the shard name and missing `-N` came true, `unexpected in shard: [83]` reproduced with the error text
it quoted, and gotcha (4) on `bin/check-learnings --file` saved a false defect report. Its next-step (3) told the
next session to **re-derive** the `CHANGELOG.md` rate rather than quote it, which is the instruction that caught
its own estimate being 4 sessions where the measurement says 2.5. Against that, one substantive miss: **it framed
BL-86 as a choice among four recorded shapes, and the answer was in neither the item nor the four** — the rule was
already in the sibling proof's C1 and in fork Learnings #37 and #96, and a session that followed the handoff
literally would have implemented one of four worse shapes. That is what #99 records. Not a defect of honesty —
every shape was labelled uncosted — but a shape list presented as the decision space.

**Phase 3B — self-assessed 8/10.** Five shapes built and measured before the operator was asked, negative controls
on the shipped artifact rather than the harness, and the ratified answer found before implementing. Against that:
**I published a false claim inside the session and had to withdraw it** — that the rule's *"removing it from here"*
clause had cost two dangling links — because I grepped for an anchor string in the file I had just written that
string into. It never reached a commit (my own link checker caught it by missing `bl-59` while flagging `bl-67`),
the population was re-measured from `git show HEAD:`, the passages were recomposed rather than patched, and the
self-matching literal was removed so the next such grep is not fooled. A measurement I trusted for one step too
long is the cost; catching it before the commit is the reason the score is not lower.

**What the next session inherits, stated plainly:** `CHANGELOG.md` is the first item and no longer a forecast —
**230,783 B** immediately before this entry, **31,361 B** from the 262,144 B read refusal, two sessions having
added 13,581 B each. **Raise the trim at the Phase 0 report, on the refusal and not on `--check`.**

### 2026-09-27 · [ad hoc] S226 — Phase 3C: fork Learning #99, and D3 discharged by an explicit refusal

**#99: a defect's recorded "shapes, none costed" list is one session's imagination, not a survey of the option
space — and where the failing artifact has a sibling of its own class, the answer is often already ratified there.**
1,427 B against the 1,500 B per-row budget; `check-learnings --file docs/FORK_LEARNINGS.md --first 15
--no-citations` reads **84 rows, contiguous 15..99**. The citations-enabled form is red before and after with an
identical error set (only its *"83 row(s)"* parenthetical moves to 84) — the standing condition from running the
fork's table, which starts at #15, against corpus citations aimed at the distributed one.

**D3 is discharged by refusal, not by retirement: no row qualifies, and these are the ones considered.** **#37**
(model the permitted transform; *"losses fail, growth is reported"*) and **#96** (a prior reduction's proof
constrains the next change to the same file) both **state the lesson #99 builds on and neither is superseded by
it** — #99 is about where to look for a remedy, not how to build a proof. **#78** (grep every document that
already states a procedure) is the nearest relative and its object is different: a procedure being written, not a
defect's remedy being chosen. **#22** (a closed item's text is load-bearing) is adjacent to this session's rule
change and is **not** mechanized by it: D1(a) wants a gate in `.quality-gates.json`, a test in `bin/tests.sh` or a
numbered failure mode, and C6 is in a proof `bin/tests.sh` does not schedule. D1(c) reaches none of them — every
artifact they are about still exists.

### 2026-09-27 · [BL-86] S226 — closing an item by the book is possible again: losses fail, growth is reported

**BL-86 and BL-83 are both CLOSED, and their pointer rows are the first two written under the fixed rule.** The
shard's losslessness proof was a **move** proof given a **destination**'s job: C1 pinned the 33 ids that moved and
flagged anything else, so appending BL-83's row turned it RED (`unexpected in shard: [83]`, measured at S225) and
**no item could be closed by the book at all.** It now pins the 33 as the loss detector — a missing row still fails
C1, an altered byte still fails C2 — and **reports** the rows closed since: `33 moved item(s), exactly the expected
set, present on both sides; 2 closed since the move (not a finding): BL-83, BL-86`.

**The shape chosen was a FIFTH one, and this repository had already ratified it twice.**
[`BACKLOG-DETAIL.md.verify.sh`](docs/planning/BACKLOG-DETAIL.md.verify.sh)'s C1 — written at S99 for the same kind
of file — has always reported added ids and never failed them, *"because a backlog that can never gain an item
would be a proof that fails on correct use, which is precisely the false-positive class BL-36 is about."* Fork
Learning **#37** states it in the table and calls it *"sibling of losses FAIL, growth is REPORTED"*; **#96** states
the constraint BL-86 ran into. None of the four shapes recorded when BL-86 was raised proposed it, and the item
cites neither row — which is this session's Phase 3C row **#99**.

**It is not the loosening it resembles, and that distinction was the decision.** `:31`'s comment defends the frozen
33 as the *loss* detector (*"if a row vanished, a derived list would simply be shorter and C1 would pass"*) — an
argument about `missing_shard`, kept byte for byte. Only *"and nothing else"* relaxes, and new **C6** replaces it
with something the old reading never had: every id closed since the move must still be findable in `BACKLOG.md`,
so the closure rule's third step is checked instead of assumed.

**Five shapes built and measured on throwaway clones at `1201b12` before the operator was asked** — none costed
when the item was raised: the chosen one, proof **+1,765 B / +24 lines**, shard +339 B; a boundary marker with two
extra checks, +2,665 B / +46 lines and +1,344 B; the marker alone, +961 B, **but it passes a duplicate pointer row
at exit 0**; a hand-maintained `ADDED` list, +296 B, where every future closure must edit the proof or C1 reddens
(measured with a second closure: `unexpected in shard: [87]`); a third file, proof +0 B and **read by no proof at
all**. (d) stayed declined. **Five negative controls fire on the shipped proof:** a dropped row (C1), one altered
byte (C2), a copy left in the live file (C3), the same id twice (**exit 2**, via the DUP check already there) and a
closure whose id never reached `BACKLOG.md` (C6).

**A second defect in the same rule, fixed with it.** The rule also said closing an item means *"removing it from
`BACKLOG-DETAIL.md`"* while the pointer row it prescribes links straight back there. **Ten of the 33 rows carry
that `[detail]` cell and all ten still have their body**, so nobody followed the clause and anyone who had would
have broken their own link. Both statements of the rule — in the shard and in `BACKLOG-DETAIL.md` — now say the
body stays. The hand-maintained count also left the shard's `## Completed items (33)` heading, which the first
closure after the extraction would have falsified in the same commit that added the row.

**A claim made and withdrawn inside this session, recorded because the withdrawal is the finding.** I first
reported that the *"removing it from here"* clause had already cost two dangling links (BL-59, BL-67). It had not:
both bodies are present. The first measurement was `grep -c` for an anchor string **in a file into which I had just
written that same string**, so it matched my own prose. Re-measured from `git show HEAD:`, the real population is
**nine of 63 `[detail]` links** — BL-47, 48, 49, 59, 60, 64, 65, 67, 73, seven open and two closed — all missing
only the `<a id>` separator line. Raised as **BL-87** and **recorded, not fixed** (FM #17): the obvious check for it
is red on arrival, and a proof that ships red is a proof nobody runs. The self-matching literal was then removed
from the prose so the next such grep is not fooled the same way.

### 2026-09-27 · [ad hoc] S226 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

**One row in [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md), and the 448 B block deleted from
the live ledger's front matter** — `| 1 | 2026-09-27 → 2026-09-27 | HANDOFFS-through-2026-09-27.md | v1.5.0 |`,
the 64th row. **In its own commit, as the index's fold rule requires:** inside the trim commit the shipped
`.verify.sh` fails L2 (fork Learning #58). `HANDOFFS.md` 17,673 B → **17,225 B**, the exact 448 B the block
occupied, so a trim-and-fold leaves this front matter no larger than it was.

The block's `.verify.sh` link is dropped by the rule, since the proof sits beside its shard; the shard's own
proof was run from a `--no-local` clone of the trim commit `6a85d20` before this fold — **exit 0, read bare**,
*"3 before = 2 retained + 1 archived; added by the trim commit: 0"*. Writing the row from the generator itself
is an upstream change, since `methodology_trim.py` is distributed.

### 2026-09-27 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-27.md` (1 record(s), 29,439 B → 17,673 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-27 → 2026-09-27) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-27.md`](docs/archive/HANDOFFS-through-2026-09-27.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-27.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-27.md.verify.sh)
rather than trusting a digest printed here. Live file 29,439 B → 17,673 B (−40.0%).

### 2026-09-27 · [BL-86] S226 claim — the closure rule and the shard's move proof, decided before either is edited (in progress)

**Phase 1B claim.** This entry, a `status: pending` receipt in `HANDOFFS.md`, and Phase 0's
`dashboard_history.jsonl` row (single-project mode: **76/100, MEDIUM, High+ 0, 0 vulns, 1,469 commits**).
Deliverable chosen at the Phase 0 task picker over the `CHANGELOG.md` trim, BL-84 (the seed's fixed warn line
versus its mandatory purpose fence) and the FM #17 recorded-not-fixed list. **P6 of the BL-66 plan is still
blocked on #87's merge**, so it was stated as blocked rather than offered.

**Three things measured at Phase 0 rather than carried from the receipts:**

- **The `CHANGELOG.md` trim ground is ~2.5 sessions away, not four.** The file is **220,220 B**; the rule's
  trigger is the **262,144 B** read refusal, **41,924 B** off. S225 moved it **203,621 → 220,220 = 16,599 B**
  end to end (`git cat-file -s` at each ledger commit). Its receipt's *"roughly four sessions"* came from an
  11,620 B **partial** span measured before its own close-out and push-record entries landed — its own next-step
  said to re-derive rather than quote it, and re-derived it is 2.5. `--check` **fires** and is still not the reason.
- **`context_budget.py --status` wrote one row into the tracked `.context-budget-history.jsonl` during a
  read-only phase; it was reverted** (`git checkout --`, diff kept in the session scratchpad, tree re-read clean).
  That is **BL-75's documented behaviour** — the first run after a measured change appends, an identical re-run
  appends nothing, which is what the second run did — and the defect open PR
  [#86](https://github.com/KJ5HST/methodology/pull/86) fixes. Not a new finding.
- **The gate at `31e16e4`, in a `--no-local` clone, exit codes read outside a pipe:** `bash bin/tests.sh`
  **343 passed / 0 failed / 6 skipped**, exit 0; `quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results
  10575dac7361 · manifest 01a4ae7aa511`, exit 0 — the same hashes S225 cited at `2f17170`, right for a doc-only
  tip. The untracked `.quality-gates-results.json` records **`head 6b29d3d`** (an *upstream* tree), so it is not
  the evidence for this one either way.

**Reconcile:** `CHANGELOG.md` frontier = HEAD, gap **0**; `HANDOFFS.md` frontier `fdb273a`, its one gap commit
the CHANGELOG-only push record `31e16e4` — the shape S219–S225 each recorded, nothing backfilled. Upstream: **0
issues**, #83–#88 open at unchanged heads, `MERGEABLE`, **0 reviews between them**, only our own two comments.
**Receipts go 2 → 3, so the retention trim is owed as its own next action.**

### 2026-09-27 · [ad hoc] S225 — fork `main` pushed to `origin`, `d7b3be8..fdb273a` (non-commit action, operator go-ahead)

**Six commits, a clean fast-forward, every guard measured before anything was sent and the result read back after.**
`origin/main` was at the expected **`d7b3be8`**, `git rev-list --count main..origin/main` **0** (nothing to rebase
onto), `git rev-list --count origin/main..main` **6**, `git merge-base --is-ancestor origin/main main` **YES**, tree
clean. After: `git ls-remote --heads origin main` reads **`fdb273a`**, and a re-fetch puts `origin/main` level with
local `main` (0 ahead, 0 behind). **`upstream/main` was re-read and is unchanged at `6b29d3d`** — nothing was sent
to `KJ5HST/methodology`, and no branch was pushed.

**The count was measured, not carried.** `git log --oneline --no-merges origin/main..main` enumerated the six: the
S225 claim (`095d20d`), the owed `HANDOFFS.md` retention trim (`0b68b04`) and its fold (`28c24d3`), BL-83's fix —
fork Learning #98 and #85's retirement (`18d4034`), BL-83's outcome with BL-86 raised (`2f17170`), and the close-out
(`fdb273a`). Ten files across them, listed by `git diff --name-only origin/main main`. S224's own push record had to
note that its stated count was never measured; this one was, at the point of use.

**This entry is pushed with the tip it records, not left above it, under the operator's standing grant of
2026-09-16** — *a commit whose only change is the `CHANGELOG.md` entry recording an authorized push is pushed to
`origin` without asking, and records its own push in the same entry.* Its guards are re-measured and the result read
back with `git ls-remote` immediately after; a mismatch would be recorded below as a correction, not left implicit.
**S219–S224 each left the recording commit behind**, which is the regress the grant exists to end and which
`d7b3be8` closed earlier today; keeping it closed is what this paragraph is for.

### 2026-09-27 · [BL-83] S225 close-out — BL-83 fixed, #85 retired, BL-86 raised; predecessor scored 7

**Deliverable complete and verified.** Fork Learning **#98** corrects #85 and **#85 is retired under D1(b)** —
the **first row ever retired** and the first use of D2's reserved-gap mechanism (`18d4034`). **D3 is satisfied by
the retirement itself**, so the four consecutive refusals of S221–S224 end here and #98 is both the deliverable
and this session's Phase 3C row. **BL-83 is not closed in the backlog and that is BL-86**, not an omission.

**Gate and suite in a `--no-local` clone at `2f17170`, exit codes read outside a pipe:** `bash bin/tests.sh`
**343 passed / 0 failed / 6 skipped**, exit 0 — exactly the `tests-sh-passed >= 343` floor, the six skips being
Test 34's named SKIPs at two receipts; `quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results
10575dac7361 · manifest 01a4ae7aa511`, exit 0 — the same hashes as Phase 0's at `9e56f0a` and S224's at
`c5e311d`, which is the right answer for doc-only edits.

**Phase 3A — S224's handoff scored 7/10.** Its trim forecast was exact and saved real time (`--cut 2 --force`,
positional cut, S223's receipt, the `-3` suffix, *read the dry run*). Against that: **its top two next steps
asked for an action a standing rule forbids** — the `CHANGELOG.md` trim, recommended on `--check` firing, where
the rule recorded in that very file since S196 makes the 262,144 B read refusal the trigger and `--check`
explicitly not a reason. Following the handoff would have spent the session on it. Two further inaccuracies:
`.quality-gates-results.json` is **untracked**, not *"stale at `431279b`"*; and the `bin/check-learnings`
invocation both S223 and S224 cite omits `--file docs/FORK_LEARNINGS.md`, so it reads the distributed file and
fails — carried forward twice, and I ran it that way at Phase 0 before correcting it. ROI still clearly positive.

**Phase 3B — self 8.** Right: catching the forbidden trim at Phase 0 rather than executing it; re-measuring the
ratchet claim in a clone instead of inheriting S216's; running D2's mechanism **and its negative control** on a
throwaway copy *before* offering the shape, so the picker's numbers were measured; recomposing #98 from 1,614 B
to 1,473 B rather than shaving it; finding the #86 coupling by grepping #85's citers; and finding BL-86 by
**running** the documented closure rule instead of assuming it works — then not editing the proof to make it
pass. Wrong: the `check-learnings` misinvocation at Phase 0, the same class of error the session was fixing; and
five of sixteen line numbers in the first draft of this receipt were wrong, caught by resolving every one.

**Measured, and not a reduction:** `docs/FORK_LEARNINGS.md` **104,339 → 104,875 B, +536 B**. **`CHANGELOG.md` is
215,241 B before this entry** — 46,903 B from the read refusal, and this session added 11,620 B, so the trim is
roughly four sessions out **on the refusal**, which is the ground the rule names.

### 2026-09-27 · [BL-86] S225 — BL-86 raised: the documented way to close a backlog item turns `BACKLOG-COMPLETED.md.verify.sh` RED

**Found by trying to close BL-83 by the book, and stopped there rather than fixed.** The editing rule at
[`docs/planning/BACKLOG-DETAIL.md`](docs/planning/BACKLOG-DETAIL.md)`:15-21`, rewritten at S223, says closing an
item means adding its pointer row to [`docs/planning/BACKLOG-COMPLETED.md`](docs/planning/BACKLOG-COMPLETED.md).
That file's own losslessness proof refuses it: `BACKLOG-COMPLETED.md.verify.sh` pins the **33 ids that moved** as
a frozen literal (`:31`, deliberately not derived) and C1 computes `extra_shard = set(rows(shard)) - set(items)`,
where `rows()` matches **every** `| **BL-N** |` row in the whole file (`:103-104`). **Any id beyond the 33 fails.**

**Measured, not predicted, and the file restored afterwards.** Control: **exit 0**, *"C1 identity set: 33 item(s),
exactly the expected set, present on both sides"*. With BL-83's pointer row appended: **exit 1**, `FAIL C1
identity set: … unexpected in shard: [83]`. Control re-run green after restoring.

**Why it could not surface earlier.** The proof is a **move** proof — the shard is *exactly* what left
`BACKLOG.md` at `a32f520` — which is right for an extraction and wrong for a destination. S223 gave the file a
second job in the same session that froze its contents. The `docs/planning/` proofs run **by hand**;
`bin/tests.sh` does not schedule them and `bin/check-links` reads distributed files only. So the first closure
after S223 was always going to be the detector, and this is it.

**Not fixed, and deliberately: editing a proof so a change passes is a loosening** (`SAFEGUARDS.md`'s
blast-radius table), so it is a decision, not a session's judgment. Four shapes recorded, **(d) retire the proof
declined on sight** — C2–C5 still guard real couplings and C4 is what stops the 33 ids in `BACKLOG.md` being
tidied away. **BL-83 therefore stays in §Open items for its pointer row alone**, its fix delivered at `18d4034`
and its outcome recorded in both the index row and the detail block. Fork-only: neither file nor proof is in
`bin/_manifest.py`.

**All three `docs/planning/` proofs re-run green after these edits** (`BACKLOG-COMPLETED` C1–C5,
`BACKLOG-DETAIL` C1–C5, `BACKLOG-archive-2026-08-15` C1–C4), and `bin/check-links` OK 111.

### 2026-09-27 · [BL-83] S225 — fork Learning #85 corrected by #98, and #85 retired: the FIRST retirement under D1(b)

**Row #85 said the `.context-budget.json` ratchet *"does not exist"*. It does.** `def precommit`
(`starter-kit/context_budget.py:1000`, byte arm `:1037`) implements it; it is merely unwired in this clone —
neither `.githooks/pre-commit` nor any `.quality-gates.json` gate calls it. **Re-measured rather than inherited
from S216**, in a `--no-local` clone at `28c24d3`: nothing staged → **exit 0**; a staged growth of
`starter-kit/SESSION_RUNNER.md` → `context-budget: REFUSED`, **exit 2**; a staged shrink → **exit 0**.

**Shape (1) of BL-83's three, chosen by the operator at a picker after all three were costed against
measurements.** Row **#98** appended (1,473 B, 27 B inside the 1,500 B per-row budget, after one recomposition
from 1,614 B), stating the lesson at least as generally: *grep for the BEHAVIOUR a note asserts, not the fields
it happens to name, and separate absent from present-but-unwired.* That is the correction #85 needed and the
generalization D1(b) requires — #85's own *Repair* says to grep every field the note names, and S201 did, and
still got the opposite answer, because the claim rests on `max_bytes`, which the note never names.

**This is the first row ever retired, and the first exercise of D2's reserved-gap mechanism.**
[`docs/archive/FORK_LEARNINGS-retired.md`](docs/archive/FORK_LEARNINGS-retired.md) did not exist before this
commit — `git log --all` on it was empty and the live file carried 0 reserved lines. S200 adjudicated all 69
then-existing rows and retired none; S221–S224 each appended and refused under D3. **D3 is satisfied here by
the retirement itself**, and #98 is both the deliverable and this session's Phase 3C learning — one row, one
retirement, no fifth consecutive refusal.

**A coupling found by grepping #85's citers, which is itself half of what #98 teaches: row #86 asserts #85's
false premise in its own text** — *"Distinct from fork Learning #85, where the prose described a mechanism that
never existed"* — written the day after #85. **#86 stays live:** its own lesson is sound and it matches none of
D1's three criteria. #98 names the inheritance instead, so the record is corrected without a second retirement.

**Measured, and it is not a reduction.** `docs/FORK_LEARNINGS.md` **104,339 → 104,875 B, net +536 B**: #98 in
(1,474 B), #85 out (1,470 B), the reserved-gap block in (~532 B). The mechanism recovers 1,401 B when it retires
without appending — measured on a throwaway copy before the shape was offered — but this application appends
too, so it buys correctness, not headroom. Stated rather than presented as relief.

**Proof, every check run bare and its exit code read outside a pipe.** #85 **byte-identical** across the move
(`git show HEAD:docs/FORK_LEARNINGS.md | grep '^| 85 |'` vs the archive, `cmp` clean, 1,470 B). Every retained
row unchanged: the pre-change row set minus #85 diffs **empty** against the post-change set minus #98.
`check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations` **OK, 83 rows, contiguous 15..98** —
the declared gap is tolerated by `RESERVED_RE` (`bin/check-learnings:76`), with **no checker change**, and the
**negative control fires**: removing #85 without the reserved line fails with `missing #85`. The bare gate form
is green on the distributed file (15 rows, 1..16). `bin/check-links` OK, 111 links; the new file's three
relative links and the gap block's two were resolved by hand, since `check-links` reads distributed files only.

### 2026-09-27 · [ad hoc] S225 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

**One row, and the block deleted — in its own commit, because inside the trim commit the shipped
`.verify.sh` fails L2** (fork Learning #58, and the rule stated at the foot of
[`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md)). The index goes **61 → 62 rows**,
counted with `grep -cE '^\| [0-9]+ \| 2026'` on both sides rather than carried from a receipt — S224's own
fold entry had to be corrected for stating a predicted count, and its gotcha (10) records the 28 that was
wrong. `HANDOFFS.md` 17,814 B → **17,358 B**; the front matter no longer grows per trim, which is what the
fold is for. `check-handoff --allow-pending` OK, `bin/check-links` OK 111 links.

### 2026-09-27 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-26-3.md` (1 record(s), 29,641 B → 17,814 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-26 → 2026-09-26) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-26-3.md`](docs/archive/HANDOFFS-through-2026-09-26-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-26-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-26-3.md.verify.sh)
rather than trusting a digest printed here. Live file 29,641 B → 17,814 B (−39.9%).

### 2026-09-27 · [BL-83] S225 claim — correct fork Learning #85's false example (in progress)

**Phase 1B claim.** This entry plus a `status: pending` receipt in `HANDOFFS.md`, and Phase 0's
`dashboard_history.jsonl` row. Deliverable chosen at the Phase 0 task picker over BL-84 (the seed's fixed warn
line versus its mandatory purpose fence), the two carried findings recorded under FM #17, and a decision pass on
BL-81/BL-79/BL-77/BL-74. P6 of the BL-66 plan is that plan's next phase and is **still blocked on #87's merge**,
so it was stated as blocked rather than offered.

**Scope, stated explicitly.** One decision among BL-83's three shapes, then that shape carried out in
[`docs/FORK_LEARNINGS.md`](docs/FORK_LEARNINGS.md) and — if shape (1) is chosen — in a
`docs/archive/FORK_LEARNINGS-retired.md` that does not yet exist. Fork-only: the file is not distributed
(`bin/_manifest.py` ships `starter-kit/FRAMEWORK_LEARNINGS.md`, not this one), so **no upstream action is in
scope and none is owed.** Six pull requests already sit open with 0 reviews.

**Measured before claiming, not predicted.**

- **The trim trigger fires on `CHANGELOG.md` and the standing rule says that is not a reason to trim.**
  `methodology_trim.py --file CHANGELOG.md --check` reports `[CHECK] trigger FIRES` at **203,621 B** against
  196,608 B. The rule that replaced the 2026-09-14 no-trim decision when it ran out at S196 is recorded above
  in this file: *"`--check` firing is not by itself a reason to trim, and a trim is raised with the operator as
  this file approaches the refusal"* — the 262,144 B `READ_REFUSE_BYTES`, which is **58,523 B away**. S224's
  next steps (0) and (9) called the trim *"deliverable-sized, pick it soon"* on the trigger alone; that is the
  reasoning fork Learning #39 was written against. Not taken, and reported at Phase 0 rather than acted on.
  **BL-57's index row is stale in the same area** — it still records *"no `CHANGELOG.md` trim at its trigger
  (2026-09-14, reaffirmed S177)"* with no mention of the S196 end. Recorded, not edited (FM #17).
- **Two of S224's gotchas are wrong as written, and both were re-run rather than read.**
  `.quality-gates-results.json` is **untracked** — `git log -1 -- .quality-gates-results.json` is empty and
  `git ls-files --error-unmatch` errors — not *"stale at `431279b`"*; its mtime is 2026-09-26 23:55, so *cite
  from a clone* still holds for a different reason. And `bin/check-learnings` needs `--file
  docs/FORK_LEARNINGS.md`: the bare `--no-citations --first 15` form both receipts cite reads the **distributed**
  file and fails it on contiguity. With the path, **83 rows, contiguous 15..97, 0 over the 1,500 B budget.**
- **Gate at Phase 0, in a `--no-local` clone at `9e56f0a`:** `11/11 pass · 0 fail · 0 unmeasured · results
  10575dac7361 · manifest 01a4ae7aa511` — byte-identical to S224's citation at `c5e311d`, five commits later.
  Dashboard 76/100, risk MEDIUM, High+ **0**. Upstream **0 issues**; #83–#88 all open at unchanged heads,
  `MERGEABLE`/`CLEAN`, **0 reviews**, comments only our own two — nothing owed, so nothing outranked the picker.

### 2026-09-26 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-26-2.md` (1 record(s), 28,071 B → 17,642 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-26 → 2026-09-26) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-26-2.md`](docs/archive/HANDOFFS-through-2026-09-26-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-26-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-26-2.md.verify.sh)
rather than trusting a digest printed here. Live file 28,071 B → 17,642 B (−37.2%).

### 2026-09-27 · [ad hoc] S224 — fork `main` pushed to `origin`, `c5e311d..1c521e0` (non-commit action, operator go-ahead)

**Eleven commits, a clean fast-forward, read back after the push.** `git merge-base --is-ancestor origin/main main`
confirmed the fast-forward and `git rev-list --count main..origin/main` was **0** (nothing to rebase onto) before
anything was sent; `git ls-remote --heads origin main` reads back **`1c521e0`** after it, and a re-fetch puts
`origin/main` level with local `main`.

**The count in the report that prompted this was wrong — eleven, not the thirteen stated.** The figure was never
measured; it was carried forward from an earlier *"9 ahead"* that was correct when taken and then guessed upward.
**That is the third unmeasured figure this session** (after the archive-index row count and the body's *"four"* of
six), and the third to be caught only by measuring at the point of use. The operator's instruction was unambiguous
as to intent, so the push proceeded at the measured count.

The commits: the S224 claim, the owed `HANDOFFS.md` trim and its fold, the row-count correction, the BL-85
deliverable and its body recompose, the close-out, two receipt re-measurements, the *Delivery routes* rename, and
the record of #88.

**This entry does not sit above the pushed tip; it is pushed with the tip, under the operator's standing grant.**
S219–S224 each left the recording commit unpushed, so fork `origin` was permanently one commit behind and the next
push needed a fresh ask for a ledger-only commit — the regress the grant (2026-09-16, after S177) exists to end:
*a commit whose only change is the `CHANGELOG.md` entry recording an authorized push is pushed to `origin` without
asking, and records its own push in the same entry.* S225 rewrote this paragraph to do that. Guards measured before
anything was sent: tree clean but for the Phase 0 dashboard row (unstaged, not in this commit), `origin/main` **0**
ahead of local `main`, local **1** ahead, `git diff --name-only origin/main main` = `CHANGELOG.md` alone, and the
push a fast-forward. **The `git ls-remote` read-back is recorded in S225's close-out receipt**, where every other
outward action of this session's is; nothing further is owed for either push.

### 2026-09-27 · [BL-85] S224 — delivery route (a) taken: branch pushed to fork `origin`, upstream pull request #88 opened (two non-commit actions, operator go-ahead)

**The operator chose route (a), standalone, after the session had already closed out.** Both actions are
outward-facing and both were explicitly authorized; each was read back before the next was taken.

- **Re-verified first, nothing assumed.** `upstream/main` re-fetched and **unmoved at `6b29d3d`**; `git merge-base
  --is-ancestor` confirms it is still the branch's base; all five previously open heads unchanged. The branch
  re-run in a `--no-local` clone **at the exact commit being sent**: `bin/tests.sh` **139 passed / 0 failed**,
  `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results 6542e640a956 · manifest 97a7aab85b9a`.
- **Action 1 — branch pushed** to fork `origin` as a new ref, `fix/bootstrap-never-overwrite-rules`, and read back
  with `git ls-remote`: **`a88fce7`**.
- **Action 2 — [KJ5HST/methodology#88](https://github.com/KJ5HST/methodology/pull/88) opened** against
  `KJ5HST/methodology` `main` from `rmsharp:fix/bootstrap-never-overwrite-rules`. Read back with `gh pr view`:
  state `OPEN`, head **`a88fce7`**, base `main`, cross-repository, **`MERGEABLE` / `CLEAN`** on the first check.
- **The body test that can actually fail.** The channel appends an attribution line the approved file does not
  contain (fork Learning #95), so *sent unchanged* and *byte-identical read-back* are different tests. Both prior
  bodies (#86, #87) were read first to confirm the convention rather than recall it; the line was appended on
  purpose; and the read-back **minus exactly that line** compares **equal** to the approved text — 3,849 B each
  side, 3,918 B as published.
- **Title sent:** *The prose update route can wipe an adopter's ledgers: give the instruction the three rules that
  stop it.*

**BL-85 is discharged by #88's existence; the merge is the maintainer's.** Six pull requests are now open
(#83–#88) with **0 reviews between them**. The S224 receipt, the body file's status line, BL-85's detail and its
index row are all corrected in this commit — the receipt had said *nothing outward happened*, which stopped being
true.

### 2026-09-27 · [BL-85] S224 — BL-85's *"Shapes"* become *"Delivery routes"*, and two of them are un-staled

**On the operator's instruction, who reported the phrase carried no meaning for them.** *"Shape"* is this backlog's
house word (≈60 uses: *fix shape*, *three shapes*, *deliberately not shaped*) and is **left alone everywhere else** —
renaming it repo-wide would be a second, larger deliverable. Only the place where it labelled a **decision the
operator has to make** is renamed: BL-85's paragraph, and the S224 receipt's two references. The routes are
unchanged; they are now called what they are — *how the fix reaches upstream, not what it says*.

**Two routes were written at S218 and had gone stale, corrected in the same pass.** **(a)** said it *"would be a
fifth while four sit unreviewed"*; #87 opened 2026-09-26, so it would be the **sixth while five sit unreviewed**.
**(b)** said *"fold it into BL-66's pull request at its docs phase (P3)"*; that pull request **is #87 and is already
open**, so (b) now means pushing a further commit onto an open pull request's branch — a materially different act
from adding a phase to unshipped work.

**This paragraph is a deliberate exception to `BACKLOG.md`'s *"the items themselves are deliberately NOT edited
(FM #17)"* convention**, taken on instruction and recorded here, which is where that convention says corrections
belong. The exception is one paragraph of one item; the convention stands.

**Re-run after the edit:** all three `docs/planning/` proofs green, `./bin/check-links` OK, `check-handoff` and
`--all` OK with the receipt 0 over its 12,288 B budget.

### 2026-09-27 · [ad hoc] S224 — the trim trigger now FIRES, and the receipt stops quoting a figure that moves

**The correcting entry below pushed the file past the threshold it was correcting for.** `CHANGELOG.md` went
193,218 → 196,328 → past **196,608 B**, each step caused by an entry written to restate the previous one. Chasing
the number is the defect, so the receipt's gotcha (9) now states the **derivation** — run
`methodology_trim.py --file CHANGELOG.md --check` — and no figure. A third numeric correction would have moved it a
third time.

**The trim is owed and is deliberately NOT taken here.** It is not the `HANDOFFS.md` shape: this ledger has never
been trimmed in this repo, it has **no fold**, and the archive-plus-proof is deliverable-sized work. Taking it at
close-out would be a second deliverable (FM #17). Recorded as next_steps item (0) with the command, so the next
session picks it deliberately rather than discovering it mid-Phase-0. `--force` will be needed: `SRF` is structural
on this file (0.9770 against the most recent archive `4e73d20`).

### 2026-09-27 · [ad hoc] S224 — the receipt's `CHANGELOG.md` figure re-measured after close-out, not before

The S224 receipt's gotcha (9) said **193,218 B**, *3,390 B away* from the 196,608 B trim trigger. That was true when
it was written and false when it was committed: the close-out entry itself added 3,110 B, and the file is
**196,328 B** — **280 B** from the trigger. `methodology_trim.py --file CHANGELOG.md --check` still prints *trigger
does not fire*, and `SRF 0.9770` against the most recent archive `4e73d20`, so the refusal is structural as expected.
**This is fork Learning #61 landing on the session that wrote the figure** — a document keeps measuring the tree it
was written against, and a close-out's own commit is exactly such a change. Corrected in the receipt, because that is
the live artifact the next session reads and *3,390 B away* would let it defer a trim that one entry will now trigger.

### 2026-09-27 · [BL-85] S224 close-out — the port is built and unsent; fork Learning #97; D3 refused a fourth time

**Deliverable complete and nothing outward happened.** Branch `fix/bootstrap-never-overwrite-rules` (`a88fce7`,
**local only**), body drafted, BL-85's four shapes still open and still the operator's.

**Phase 3A — predecessor S223 scored 9/10.** Its shard-name prediction was exactly right (`-2`, via
`SHARD_NAME_DISAMBIGUATED`) *and* it still said to read the dry run; gotcha (5) *draft the learning short* landed
row #97 at 1,492 B first try; gotcha (3) *run all three `docs/planning/` proofs* caught nothing but was cheap and
correct; gotcha (7) kept the gate citation off the stale results file. **The one inaccuracy cost this session a
commit:** its *"index 28 rows"* is wrong — the table holds **61** — and this session incremented it to 29 and
published that before measuring. Not 10 because of that; not lower because everything else it predicted held.

**Phase 3B — self 8/10.** The deliverable is complete and every claim in it was measured on a tree that was
actually built: three suites (branch 139/0, merged-with-#84 163/0, merged-with-#87 188/0), the counterparty's
gate run on the merge rather than a grep. Against that: **two accuracy defects in one session**, both
self-inflicted and both caught here rather than downstream — the inherited row count published as a measurement,
and a body paragraph that said *"four"* of six and inferred a claim the acceptance test does not make. One
reached a commit; one was caught while showing the draft. A session that logs its predecessor's unmeasured figure
and then produces two of its own does not score above 8.

**Phase 3C — fork Learning #97 appended** (1,492 B): *an item's own "before it goes up" warnings are a sample of
what will not port, never a partition of it.* **D3's retirement is owed and is REFUSED — the FOURTH CONSECUTIVE
REFUSAL, which is now a standing signal about the rule rather than an incident.** Rows tested, not asserted:
**#22** is the nearest miss — the two `.verify.sh` C4 reachability checks *do* mechanize its lesson for the
backlog, but criterion (a) names a `.quality-gates.json` gate, a `bin/tests.sh` test or a numbered failure mode,
and `grep -c 'verify.sh' bin/tests.sh` is **0**; #22 was also observed in two adopter repos that have no such
proof. **#55** — cited by #97, which does not state it as generally (values versus population). **#94** — obeyed
by this session, enforced by nothing. **#61, #58, #24** — no gate, artifacts live. **#85** — known false (BL-83);
wrongness is not a ground. The eleven declared gates are all suite and checker counts; none reaches these rows.

**Verification.** Branch and both merged trees green (see the receipt for the four gate citations). Fork `main`:
all three `docs/planning/` proofs, `check-links` 111, `check-learnings` both forms, `context_budget --precommit`
exit 0, `check-handoff` and `--all` OK with the receipt 0 over its 12,288 B budget. **Not exercised:** anything on
GitHub; the merged trees with #83, #85, #86.

### 2026-09-27 · [BL-85] S224 — the pull-request body's §The defect recomposed against the acceptance-test record

The drafted body said *"four of the files ... plus"* two more, which is six, and claimed *"every one of the six
had received the one-sentence instruction"* — an inference, not something the acceptance test records. Recomposed
(not appended to) against `uat-2026-08-04-six-adopters.md:133-157`, which states the protection **reached 0 of 6**
and gives three inspected adopters' ledger pairs: 42 KB / 70 KB, 150 KB / 112 KB, 474 KB / 1.1 MB. It also carries
the finding's own strongest point, which the draft had dropped: for an adopter with no sibling checkout the prose
route is the **only** route, so the fix is delivered by the instruction that is broken. Body 3,529 B → 3,851 B;
recognized-terms check still **0 hits**. Caught while showing the draft for approval, before any approval was
given and before anything was sent.

### 2026-09-27 · [BL-85] S224 — the upstream port of the ledger-overwrite rules is built and measured, not sent

**The deliverable.** Branch **`fix/bootstrap-never-overwrite-rules`**, tip **`a88fce7`**, based on `upstream/main`
`6b29d3d`, carrying the three rules of `starter-kit/BOOTSTRAP.md` §Without `bin/sync` **re-derived against upstream
rather than cherry-picked from `12463dd`** — plus upstream's own ledger entry, the convention every open fork
pull request follows. The body is [`bootstrap-never-overwrite-rules-pr-body.md`](docs/planning/bootstrap-never-overwrite-rules-pr-body.md),
3,529 B below its rule, recognized-terms check **0 hits**. **Nothing outward was done: no push, no pull request, no
comment.** BL-85's four shapes are still open and still the operator's, and the branch serves (a) and (c) equally.

**Two of BL-85's own three "before it goes up" warnings came back different from what it predicted.**

- **Rule 1's table needs no re-derivation.** BL-85 says the manifests differ, so re-derive it. They do differ — in
  comments and in `STALE_FORMAT_MARKERS` — but `bin/_manifest.py`'s `DISTRIBUTION` list is **identical** on the two
  trees: the same 11 tracked `starter-kit/` entries, the same 6 seeds, the same `docs/methodology/` set, in the same
  order. The table ports unchanged, and the finding is that no change was needed.
- **The half that could not port is rule 2, which BL-85 does not flag.** It cites `ledger-format: 2` and
  `FRAMEWORK_APPARATUS.md` §The Action Ledger; `upstream/main` has neither (**0** occurrences of *Action Ledger* in
  that file). Both arrive with #84 (`77afc12` adds the heading at `:338`). Rewritten to **point at** the existing
  *Updating an existing project from an earlier methodology version* paragraph in §Setup with `bin/sync` instead of
  restating the migration — which is also what makes it survive #84 untouched.
- **Rule 3 ports verbatim, checked against the source:** `upstream/main`'s `bin/status` prints exactly the five
  verdicts the rule names — `missing` `:95`, `current` `:98`, `N versions behind` `:102`, `locally modified` `:103`,
  `STALE_SEED = "present (stale format)"` `:106`.
- **The `--source=github` note was excluded**, as BL-85 says: it describes the route #87 changes.

**Conflicts measured, not predicted** (`git merge-tree --write-tree`, then the suite on the merged tree):
**#84 `77afc12` merges CLEAN, `BOOTSTRAP.md` included** — merged tree **163 passed / 0 failed**, gates 10/10
`results 93ea168d093e`. #83, #85, #86 and #87 collide in **`CHANGELOG.md` only** — the prepend-only ledger's
ordinary collision, resolved by keeping both entries; #87's `BOOTSTRAP.md` auto-merges, and its merged tree runs
**188 passed / 0 failed** with its own raised floor of 188 met exactly, gates 10/10 `results 2162213f5332` — the
hashes #87 itself cites. **This branch adds no tests, so it moves no floor.**

**On the branch:** `bin/tests.sh` **139 passed, 0 failed**, identical to the base commit's own measured count;
`bin/check-links` OK 107 links; `context_budget.py --precommit` exit 0; `quality_ratchet.py --run` **10/10 pass**,
`results 6542e640a956 · manifest 97a7aab85b9a` — the hashes `6b29d3d`'s receipt cites.

**Recorded and NOT fixed (FM #17).** §Setup with `bin/sync`'s prose at `:74` lists the installed operating files but
omits `methodology_trim.py`, `context_budget.py` and `quality_ratchet.py`, and its seed list omits
`.context-budget.json` and `.quality-gates.json` — both stale against the manifest this branch's table is derived
from. Named in the body's *Deliberately not in this pull request*; fixing it here would put a second, larger edit in
a pull request whose point is one section.

**Fork-side bookkeeping:** BL-85's detail gains an S224 status paragraph and its index row a pointer; all three
`docs/planning/` proofs re-run green (`BACKLOG-COMPLETED`, `BACKLOG-archive-2026-08-15`, `BACKLOG-DETAIL`), and
`check-links` is OK at 111 on this tree.

### 2026-09-26 · [ad hoc] S224 — correction: the fold entry's index row count was predicted, not measured

**The defect.** The entry below says *"the index's table is 29 rows"*. It is **61**. The figure was never
measured: it was carried from S223's receipt (*"index 28 rows"*) and incremented by one for this fold. That
predecessor number is wrong too, and inheriting it is how a wrong figure survives a session boundary.

**Measured.** `awk '/^\| *[0-9]+ *\|/ {c++}' docs/HANDOFFS_ARCHIVE_INDEX.md` → **61** data rows.
Cross-checked against the shards themselves: `git ls-files 'docs/archive/HANDOFFS-*.md'` → **62** files, and
the index's own front matter says one shard predates the trimmer and deliberately has no row
(`HANDOFFS-archive.md`). 61 + 1 = 62, so the two agree. 240 receipts are archived across them.

**What is corrected and what is not.** This entry corrects the number; the entry below is **left as written**,
the same append-only treatment `c5e311d` gave the 8,946 B figure one session ago — for the same reason, that
rewriting it would erase the record that the claim was made. Nothing else in the fold is affected: the row,
the byte figures and `check-links` were all measured.

### 2026-09-26 · [ad hoc] S224 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

The `82c3148` trim left `methodology_trim.py`'s ~448 B pointer block in `HANDOFFS.md`'s front matter.
Folded to one row at the bottom of [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md) —
`n` 1, span 2026-09-26 → 2026-09-26, shard `HANDOFFS-through-2026-09-26-2.md`, `by` v1.5.0 — and the block
deleted, **in its own commit** as the index's fold rule and [fork Learning #58](docs/FORK_LEARNINGS.md)
require: inside the trim commit the shipped `.verify.sh` fails L2. The `.verify.sh` link is dropped per that
rule, since the proof sits beside its shard. `HANDOFFS.md` 17,642 B → 17,186 B; the index's table is 29 rows.
`./bin/check-links` OK, 111 links.

### 2026-09-26 · [ad hoc] S224 claim — BL-85: port the three ledger-overwrite rules upstream (in progress)

**Phase 1B claim.** This entry plus a `status: pending` receipt in `HANDOFFS.md`, and Phase 0's
`dashboard_history.jsonl` row. Deliverable chosen at the Phase 0 task picker over BL-83 (correct fork
Learning #85's false example), BL-84 (the seed's warn line versus its mandatory fence) and BL-81
(`.context-budget.json`'s three-places stale sizes). P6 of the BL-66 plan is that plan's next phase and is
still blocked on #87's merge, so it was stated as blocked rather than offered.

**Scope, stated explicitly.** One branch based on `upstream/main`, carrying the re-derived §Without `bin/sync`
rules, plus a drafted pull-request body under `docs/planning/`. **Opening the pull request is not in scope and
is its own go-ahead** — BL-85's own record says *"Outward-facing in every shape but (d): its own go-ahead.
Decision first."* Five pull requests already sit unreviewed with 0 reviews, and `CLAUDE.md` §Contributing
upstream prefers one substantial batched pull request over several small ones, so this session builds the
branch and stops.

**Measured before claiming, not predicted.**

- `grep -c 'never overwrite' starter-kit/BOOTSTRAP.md` — **2** on fork `main` and on `origin/main`; **0** on
  `upstream/main` (`6b29d3d`) and on all five open pull-request heads (`219fb9d`, `77afc12`, `e2501c5`,
  `c1167ae`, `67feb9f`). BL-85's S218 measurement re-confirmed, now including #87's head, which did not exist
  when it was taken.
- **BL-85 warns that rule 1's table must be re-derived because the manifests differ. They differ, but not
  there.** `diff` of `bin/_manifest.py` between the two trees: the `DISTRIBUTION` list is **identical** —
  the same 11 tracked `starter-kit/` entries, the same 6 seeds (`SESSION_NOTES.md`, `CHANGELOG.md`,
  `HANDOFFS.md`, `ROADMAP.md`, `.context-budget.json`, `.quality-gates.json`), the same `docs/methodology/`
  set, in the same order. Every difference is in comments or in `STALE_FORMAT_MARKERS`. **So rule 1's table
  ports unchanged**, and the re-derivation's finding is that no change is needed.
- **Rule 2 is the half that cannot port verbatim.** It cites `ledger-format: 2` and the seed's pointer to
  `FRAMEWORK_APPARATUS.md` §The Action Ledger. On `upstream/main` the markers are `Authoritative Action
  Ledger` / `Handoff Receipts`, and `FRAMEWORK_APPARATUS.md` contains **0** occurrences of *Action Ledger* —
  the section does not exist there. Both arrive with **#84** (`77afc12` adds `## The Action Ledger` at `:338`
  and both `-format: 2` markers), so rule 2's fork wording becomes portable only after #84 merges.
- **Rule 3 ports unchanged.** `upstream/main`'s `bin/status` emits exactly the five strings the rule names:
  `missing` (`:95`), `current` (`:98`), `N versions behind` / `1 version behind` (`:102`), `locally modified`
  (`:103`), and `STALE_SEED = "present (stale format)"` (`:106`).
- **#84 does not touch §Without `bin/sync`.** Its `starter-kit/BOOTSTRAP.md` hunks are the tree diagram, the
  `bin/sync` commit note (`:73`), the *Updating an existing project* paragraph (`:84`) and two file tables —
  a different region of the same file. Conflict to be measured with `git merge-tree`, not predicted.

**Phase 0.** `CHANGELOG.md` frontier = `HANDOFFS.md` frontier = HEAD `c5e311d`; both gaps **empty**. 2 receipts
before this one, none pending; nothing backfilled. Gate re-run in a `--no-local` clone at `c5e311d`:
`11/11 pass · 0 fail · 0 unmeasured · results 10575dac7361 · manifest 01a4ae7aa511` — S223's citation exactly,
one commit later; `tests-sh-passed` 343, `tests-sh-failed` 0. `context_budget.py --precommit` exit 0. Dashboard
**76/100, risk MEDIUM, High+ 0** — S223's backlog extraction held. Upstream **0 open issues; #83–#87 all open at
unchanged heads, all `MERGEABLE`/`CLEAN`, 0 reviews, and the only comments are our own two** (#83, #84) — nothing
owed there. `main` level with `origin/main`; `.git/REBASE_HEAD` absent and `core.hooksPath` is `.githooks`, so the
hooks are armed.

**Side action owed by the retention policy, not a picker item:** this claim makes three receipts, so the
`HANDOFFS.md` trim and its fold follow the Phase 0 report.

### 2026-09-26 · [ad hoc] S223 — correction: this session stated an unmeasured byte figure as a measurement

**The defect.** Two entries above — the `27b1c33` extraction entry and this session's `HANDOFFS.md` receipt,
gotcha (4) — gave the new losslessness proof's size as **8,946 B**. It is **9,752 B**, and always was:
`git cat-file -s 27b1c33:docs/planning/BACKLOG-COMPLETED.md.verify.sh` returns 9,752 and the file is byte-identical
at HEAD. **The figure was never measured.** Its two neighbours in the same sentence, 6,947 B and 8,181 B for the
sibling proofs, *were* measured and are correct — which is what made the third read as one of them. 806 B, 9% low.

**What is corrected and what is not.** The receipt's gotcha (4) is corrected in place: it is the live artifact the
next session reads, and its whole purpose is to stop a successor carrying BL-60's ~16 KB complaint onto this
population, which a wrong size undercuts. **The `27b1c33` entry above is left exactly as written** — this ledger is
append-only, and rewriting an entry would erase the record that the claim was made. The same precedent the
`.context-budget.json` note sets for a drifted citation (*"deliberately NOT corrected in the `CHANGELOG.md`
entry's copy of it"*).

**Found by re-measuring at the close-out report rather than restating.** The rule that caught it is this repo's
own: re-read the file that confirms a claim before repeating it. It had two chances to be caught earlier and was
not — the figure went into a commit message and a receipt field between them.

**One related imprecision, stated rather than corrected.** `BACKLOG.md:175`'s pointer block says the moved rows
were **25,276 B** where the ledger and receipt say **25,187 B**. Both are right for what they measure: 25,276 B is
the whole §Completed items slice including its blank lines and the second table's header, 25,187 B is the 33 rows
alone, which is what C2 byte-compares. Neither is wrong; the two are not distinguished where they are used.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-26 · [ad hoc] S223 — fork `main` pushed to `origin`, `73157d0..61081e1` (non-commit action, operator go-ahead)

Five commits, all fork-only documentation: the claim `109ba7b`, the `HANDOFFS.md` retention trim `36060f0` and
its fold `a32f520`, the §Completed items extraction `27b1c33`, and the close-out `61081e1`. A fast-forward from
the sha `origin` held (`73157d0`), checked with `git merge-base --is-ancestor` **before** the push and read back
with `git ls-remote` **after** — `refs/heads/main` = `61081e1`, equal to local HEAD.

**Nothing on `KJ5HST/methodology` was touched.** No branch was pushed, no pull request opened or edited, no
comment posted; `#83`–`#87` remain open at the heads Phase 0 recorded (`219fb9d`, `77afc12`, `e2501c5`,
`c1167ae`, `67feb9f`) with 0 reviews. The go-ahead was given at this session's close-out picker; the standing
grant covers only a CHANGELOG-only push record, which this was not.

Pushed with the push it records, under the standing grant for push records.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-26 · [ad hoc] S223 close-out — the backlog breach is closed; fork Learning #96; D3 refused, rows named

**Deliverable complete and verified.** `docs/planning/BACKLOG.md` 58,727 → 35,296 B; dashboard risk `HIGH` →
`MEDIUM`, High+ count 1 → 0. Commits: `109ba7b` claim, `36060f0` the owed `HANDOFFS.md` trim, `a32f520` its fold,
`27b1c33` the extraction, and this close-out. **No outward action was taken and none was asked for** — nothing
was pushed, no branch touched, and `#83`–`#87` are exactly as Phase 0 found them.

**Phase 3A — S222's handoff scored 9/10.** *What helped, specifically:* its item (7) named the owed trim with the
exact invocation and the instruction *"read the dry run's shard name rather than predicting it"* — which is the
trap S221 had fallen into, and following it produced the right answer plus a diagnostic
(`CUT_STRADDLES_DAY`) nobody had seen before. Its item (1) listed all five pull-request heads, so the upstream
check was one command. Gotchas (4) and (5) — the stale `.quality-gates-results.json`, and *"the 1 loosened is
historical, do not re-investigate"* — each saved a wrong turn. Its item (6) carried the byte figure
(58,727 B, 1,977 B over) that became this session's deliverable **and** its acceptance criterion; both
re-measured exactly. *What was missing:* nothing about the **fixture coupling** — that §Completed items' rows are
load-bearing for an older proof's C4. That was this session's largest hazard and it was found by grep, not by
the handoff; item (6) was one line in a list of options rather than a scoped task, which makes it a mild miss
rather than a defect. *What was wrong:* one figure — *"`CHANGELOG.md` IS ~155 KB"* against 161,678 B measured at
Phase 0, ~7 KB low. Hedged with a tilde and it misled nothing (the conclusion, that the trigger does not fire,
held), but it is the kind of number this repo's own rule says to re-derive rather than carry. *ROI:* strongly
positive — the trim, the upstream check and the deliverable's premise all came straight from it.

**Phase 3B — self-assessed 9/10.** Went right: the proof shape was **decided from measurement**, not from the
worry the claim recorded — and that worry's premise turned out false, which is stated rather than quietly
dropped; every referrer was enumerated before editing, which is what found the C4 coupling and improved the
design; all five checks were proved killable, including catching and redoing an invalid mutation of my own; the
reduction was made **durable** by moving the editing rule, so it is not a one-shot. Went wrong, all self-caught
and none reaching the artifacts: a memory-file `[[wiki]]` link written into the receipt stub and removed; a
`grep -c '^PASS:'` that returned 0 against indented rows, caught by reading the Summary line; a `git checkout --`
cleanup that invalidated one mutation run; and the claim's unverified premise about BL-36's population. Operator
corrections to the work: **0**. One instruction added — provide a task picker at Phase 0 — applied in the same
session it was given.

**Phase 3C — fork Learning #96 appended** (`docs/FORK_LEARNINGS.md:108`, 1,497 B; 82 rows, contiguous 15..96):
*a prior reduction's losslessness proof becomes a constraint on the next reduction of the same file, and where
its check is a reachability assertion, "fix the check" inverts what it exists to assert.* **D3's retirement is
owed and is REFUSED, with the rows named and the criterion actually tested against them — and this is the THIRD
CONSECUTIVE REFUSAL (S221, S222, S223), which is itself the pattern D3 was written against and is flagged here
rather than left to be noticed.** #24 — criterion (a) tested rather than assumed: `bin/tests.sh` Test 29 **was**
rewired to read live + archives at S87, but that mechanizes one instance, not the rule *enumerate consumers
before archiving*; this session enumerated by hand and found a consumer no test covers, which is what #96
records. #26 — its worked example is now falsified for this very file, but a stale example is never a ground and
its method (*sum what you may not remove before agreeing a target is reachable*) is ungated. #31 and #41 — Test
34's named SKIPs make one instance loud; the tool that shrinks a file still cannot see the coupling. #15 —
implemented BY this session's proof, which is not the same as enforced by a gate. #78 — heeded again here,
ungated. #58 — held by prose in the shard index. #85 — known FALSE (BL-83), and wrongness is not a retirement
ground; retiring it would hide the defect rather than fix it. No later row states any of these at least as
generally; every row's artifact still exists.

**Phase 3E — gate citation, `--no-local` clone of `27b1c33`:** `quality_ratchet: 11/11 pass · 0 fail · 0
unmeasured · results 10575dac7361 · manifest 01a4ae7aa511`, exit 0, identical to Phase 0's at `73157d0`.
`bin/tests.sh` **343 passed / 0 failed / 6 skipped** three times — Phase 0, post-extraction, and with row #96
present. `bin/check-handoff` and `--all` both OK; the receipt was refused **four times** on the 12,288 B
per-record budget before it fit, and row #96 three times on the 1,500 B row budget — both cut shorter rather than
raised.

**Two findings recorded, neither fixed (FM #17):** the `## Completed items (…)` heading this session replaced
named **19 of the 33** rows present; and `.context-budget.json:73`'s `structure.why` claims its pattern matches
*"the 19 open-item rows and NOT the §Completed items pointer table"* where today it matched **53** and **10** —
it passes for a different reason than its rationale gives, and still passes.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-26 · [ad hoc] S223 — `BACKLOG.md`'s §Completed items moved to a read-on-demand sibling; the one-read breach is closed

**What:** the 33 closed-item pointer rows that stood in [`docs/planning/BACKLOG.md`](docs/planning/BACKLOG.md)
§Completed items — **25,187 B in two tables** — moved **verbatim** to
[`docs/planning/BACKLOG-COMPLETED.md`](docs/planning/BACKLOG-COMPLETED.md), and the section became a pointer block.
`58,727 B → 35,296 B`, so the file is **21,454 B under** the 56,750 B one-read budget it was 1,977 B over.
**The dashboard's only HIGH risk factor is gone: risk `HIGH` → `MEDIUM`, High+ count 1 → 0**, health 76/100
unchanged. The three remaining factors are all pre-existing MEDIUMs — no CI/CD, the historical `368b29c`
threshold loosening, and `tools/test_methodology_dashboard.py`'s 5,867 lines (BL-68).

**Same shape and same argument as the two extractions before it** — `BACKLOG.md` → `BACKLOG-DETAIL.md` (S99)
and `CLAUDE.md` → `docs/RELEASE_HISTORY.md` (v3.7): the always-read file stays scannable, the accumulated
record moves to a sibling read on demand. The closed rows were the half no session needs in order to run.

**The proof is hand-authored and its shape was CHOSEN, not assumed — the claim's stated open question.**
[`BACKLOG-COMPLETED.md.verify.sh`](docs/planning/BACKLOG-COMPLETED.md.verify.sh), 5 checks, exit 0: C1 identity
set (33 ids, enumerated as a frozen literal rather than derived from the shard), C2 rows byte-identical to
`a32f520` (25,187 B), C3 no moved row left in the live file, C4 every id still findable there, C5 the region's
retained note verbatim. **Every check was proved killable** by mutation in a throwaway copy against a green
control — delete a row (C1), flip one byte (C2), copy a row back (C3), drop one id (C4), delete the note (C5).
C4's first mutation run was **discarded as invalid**: a cleanup step had reverted the live file, so C4 fired on
its *shard-not-named* branch instead of the branch under test; it was redone from a clean copy and the intended
branch fired by name. **BL-60 and BL-36 were checked and neither applies to this population:** their ~16 KB,
97.9%-identical, four-of-six-failing proofs are all `methodology_trim.py`-GENERATED shard proofs, whereas the
two hand-written `docs/planning/` proofs are 6,947 B and 8,181 B and **both pass today** — re-run this session.
This one is 8,946 B and sits in a directory no phase mandates reading, so it costs no per-session context.

**A fixture hazard found by checking rather than assuming, and it improved the design.** Moving the rows as-is
would have **broken C4 of [`BACKLOG-archive-2026-08-15.md.verify.sh`](docs/planning/BACKLOG-archive-2026-08-15.md.verify.sh)**,
which asserts each of *its* eleven items keeps a `**BL-N**` mention in `BACKLOG.md` — and eleven of those
mentions were rows being moved. So the pointer block carries **all 33 ids in the `**BL-N**` form**, which
satisfies that check's stated purpose rather than its regex: its own comment names the case, *"BL-27 is the
named case: S88 needed it and could not find it even while it was in the live file."* Both sibling proofs were
re-run after the change and are green.

**Two findings recorded, neither fixed (FM #17).** (1) The heading this block replaces, `## Completed items
(BL-1 – BL-7, …)`, named **19 of the 33** rows present — BL-8, BL-15, BL-20, BL-24, BL-25, BL-27, BL-28,
BL-29, BL-33, BL-34, BL-35, BL-38, BL-40 and BL-41 were in the table and absent from its own list. That is this
file's *"do not trust a number in this file without re-deriving it"* warning landing on its own section
headings; the replacement count and id list are derived. (2) `.context-budget.json`'s `structure.why` for this
file claims its pattern *"matches the 19 open-item rows and NOT the §Completed items pointer table beside
them"* — measured today it matched **53** open rows and **10** completed ones, because the newer closures kept
their `[detail]` links. The check passed for a different reason than its rationale gives, and it still passes
(53 ≥ `expect_min` 5), confirmed by `context_budget.py --precommit` exit 0 and the table's
`docs/planning/BACKLOG.md 35,296 B / 65,536 B ok`.

**Durability, not a one-shot reduction.** The editing rule moved with the rows: closing an item now appends its
pointer row to `BACKLOG-COMPLETED.md`, not to `BACKLOG.md`
([`BACKLOG-DETAIL.md`](docs/planning/BACKLOG-DETAIL.md)`:16-19`, rewritten), so the file Phase 0 reads no longer
grows by a narrative row per closure. Without that, the next 33 closures rebuild the breach.

**Verified:** `bin/tests.sh` **343 passed / 0 failed / 6 skipped**, identical to this session's Phase 0 run, so
no assertion was disarmed by the shrink; `./bin/check-links` OK (111 links); all **140** relative links in the
three touched planning files resolve; both sibling `.verify.sh` proofs green; `context_budget.py --precommit`
exit 0. **Not exercised:** this commit itself (BL-64), and the `git grep` for `BACKLOG.md#` anchors returned
nothing, so no anchor link depended on the renamed heading.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-26 · [ad hoc] S223 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

The `2026-09-26` shard's four-line pointer block written by `methodology_trim.py` into `HANDOFFS.md`'s front matter
becomes one row at the bottom of [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md)'s table — now 28
rows — and is deleted from the ledger, the `.verify.sh` link dropped since the proof sits beside its shard. **Its own
commit, as the index's fold rule requires:** inside the trim commit the shipped `.verify.sh` fails L2 (fork Learning
#58), and that proof was run from a `--no-local` clone of the trim commit `36060f0` and exits **0** on L1,
L2/front-matter and L3. `HANDOFFS.md` 17,565 B → 17,117 B. This shard name carries **no** `-N` suffix — read from the
dry run, not predicted — because no shard of that date existed; the tool did print `CUT_STRADDLES_DAY`, since all
three receipts share the date `2026-09-26`, so the name is a span label rather than a day seam. `./bin/check-links` OK
(111 links); `bin/check-handoff` reports the newest receipt still pending, which is this session's own claim stub.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-26 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-26.md` (1 record(s), 29,054 B → 17,565 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-26 → 2026-09-26) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-26.md`](docs/archive/HANDOFFS-through-2026-09-26.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-26.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-26.md.verify.sh)
rather than trusting a digest printed here. Live file 29,054 B → 17,565 B (−39.5%).

### 2026-09-26 · [ad hoc] S223 claim — archive `docs/planning/BACKLOG.md`'s §Completed items to clear the one-read breach (in progress)

Phase 1B claim. Deliverable chosen at the Phase 0 task picker over three alternatives (BL-85 upstream prep,
BL-84 upstream prep, a decision pass on BL-83/81/79/77/74). `[ad hoc]` rather than `[BL-N]`: the breach is
a standing dashboard risk factor carried in the last several handoffs' `next_steps`, not a numbered backlog
item. Searched before claiming — all 62 items parsed out of `BACKLOG-DETAIL.md` and their bodies matched for
this file's own size and both ceilings; the three near-58 KB figures the sweep returned are unrelated
(a `358,377 B` adopter ledger, a regression intercept, a partition sum). **One item is adjacent and neither
owns nor blocks this work: BL-37.** Its half two — the DISTRIBUTED seed `starter-kit/context-budget.json`
carries no `BACKLOG.md` ceiling entry — is still open and is a distributed change, not this reduction. Its
half one is done: this repo now has a root `.context-budget.json` and it classes the file `read-mandated`.
**BL-37 also carries a claim this session contradicts, and it is stale rather than wrong:** *"its excess
cannot be archived away — after moving every closed item out, the open items alone are 68,195 B."* True on
2026-08-15 (S89), when item bodies still lived in this file; the S99 split moved them to
`BACKLOG-DETAIL.md`, and the open-items section measures **25,971 B** today. Not edited (FM #17).

Measured before the claim, at HEAD `73157d0`: `docs/planning/BACKLOG.md` is **58,727 B / 229 lines** against
the dashboard's derived **56,750 B** one-read budget (25,000-token read cap × 2.27 B/token) — **1,977 B over**,
and the single risk factor behind 76/100 / HIGH. §Completed items is lines 173–214, **25,576 B, 43.5% of the
file**; removing it leaves **33,151 B**. The two ceilings differ and only one is red: `.context-budget.json`
classes the file `read-mandated` at `max_bytes: 65536`, which it is under.

Phase 0: `CHANGELOG.md` frontier = HEAD `73157d0`, gap empty; `HANDOFFS.md` frontier `7026512`, the one later
commit `73157d0` the push record, which carries its own entry — the shape S219–S222 each recorded. 2 receipts
before this one, none pending; nothing backfilled. Gate citation re-run in a `--no-local` clone at `73157d0`:
`11/11 pass · 0 fail · 0 unmeasured · results 10575dac7361 · manifest 01a4ae7aa511`, S222's citation exactly,
four commits later; suite 343 passed / 0 failed. The tracked `.quality-gates-results.json` is still stale
(head `431279b`, 2026-09-19), which is why the citation came from the clone. Upstream **0 open issues**;
**#83–#87 all open at unchanged heads** (`219fb9d`, `77afc12`, `e2501c5`, `c1167ae`, `67feb9f`), **0 reviews and
no maintainer comment on any** — so nothing upstream outranked the picker, and P6 of the BL-66 plan stays
blocked on #87's merge. `main` in sync with `origin/main`; `.git/REBASE_HEAD` absent and `core.hooksPath` is
`.githooks`, so the hooks are armed.

Open at claim time, to be decided and stated rather than assumed: what proves the extraction lossless. The
precedent is a sibling `.verify.sh` (eleven earlier closed items, `BACKLOG-archive-2026-08-15.md`), but BL-60
measures those proofs at ~16 KB each, 97.9% identical, 31 of them holding 5.4% of the tracked repo, and BL-36
found four of six do not hold.

Side action owed by the retention policy, not a picker item: this claim makes three receipts, so the
`HANDOFFS.md` trim and its fold follow the Phase 0 report.

### 2026-09-26 · [ad hoc] S222 — fork `main` pushed to `origin`, `43cf345..7026512` (non-commit action, operator go-ahead)

Ten commits: S221's five, which had not been pushed, and this session's five — the claim `e25211c`, the
`HANDOFFS.md` trim `4b36803` and fold `d280e04`, the P5 record `651a207` and the close-out `7026512`. A fast-forward
from the sha `origin` held (`43cf345`), checked with `git merge-base --is-ancestor` before the push and read back
with `git ls-remote` after. The branch `fix/sync-github-history` was pushed separately and earlier, and has its own
entry above with the pull request it was opened as. **Nothing else on `KJ5HST/methodology` moved:** `upstream/main`
is still `6b29d3d`, and #83–#86 still sit at `219fb9d`, `77afc12`, `e2501c5`, `c1167ae`. This recording commit is
pushed with it under the standing grant for push records (2026-09-16), so no further record is owed.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-26 · [BL-66] S222 close-out — P5 of the BL-66 plan done: the pull request is open; one ledger trimmed

- **Deliverable:** P5 of [`sync-github-route-plan.md`](docs/planning/sync-github-route-plan.md) — **the pull request
  is open, [KJ5HST/methodology#87](https://github.com/KJ5HST/methodology/pull/87)**, head `67feb9f`, base `main`,
  `MERGEABLE` / `CLEAN`. The plan's outward phase is finished; **P6 (fork-side adoption) remains and waits on the
  merge**, and nothing further is owed upstream.
- **Every step was read back before the next one, which is what this phase is for.** `upstream/main` re-fetched and
  still `6b29d3d`, `git merge-base --is-ancestor` exit 0 — no rebase pending. Suite re-run on the tip in a
  `--no-local` clone: **188 passed, 0 failed**; `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results
  2162213f5332 · manifest 24be12b693f1`, the hashes P4 cited, from an independent clone. Branch pushed to fork
  `origin` `9f42c0f..67feb9f` and `git ls-remote` read back `67feb9f`. Body extracted as everything after the file's
  first standalone rule (7,306 B), scoped recognized-terms grep **0 hits**. Read-back diffed in Python: byte-identical
  to that text once the attribution line is removed. `mergeable` `MERGEABLE`, `mergeStateStatus` `CLEAN`.
- **The one departure, decided by the operator at this session's Phase 0 picker: the PR was opened NOW.** D7 offers
  waiting for #84 or pre-resolving the `starter-kit/BOOTSTRAP.md` paragraph; the third path was taken on three
  grounds — #84 has had 0 reviews for six days, the merge is a fast-forward today, and the approved body already
  discloses both collisions with their built-and-run resolutions. Pre-resolving was declined because it would import
  unmerged wording and falsify that section of the approved body. **The cost is stated:** if #84 merges first, #87
  shows conflicting until P4's measured head+tail resolution (212/0) is pushed.
- **One addition to the approved text, and it is the house standard:** the attribution line every prior pull request
  from this fork carries, checked on #84 and #86 before sending. Nothing else added, removed or reflowed.
- **Side action, owed by the retention policy:** the `HANDOFFS.md` trim the claim made owed (`4b36803`, 3 receipts →
  2, 27,996 → 18,688 B) and its fold (`d280e04`, → 18,232 B). The shard is
  [`docs/archive/HANDOFFS-through-2026-09-22-2.md`](docs/archive/HANDOFFS-through-2026-09-22-2.md) — **the `-N`
  suffix the predecessor handoff predicted would not be needed.** The cut is positional and oldest-first, so the
  record that left was S220's, dated `2026-09-22`, and that shard name was already taken. The tool said so itself,
  in the dry run, before anything was written. `.verify.sh` exit 0 from a clone of the trim commit.
- **Phase 3A — the predecessor handoff scores 8/10.** Everything actionable in it held and was used: the four PR
  heads, `upstream/main` at `6b29d3d`, the fast-forward, the 188/0 and `2162213f5332` citation, the body-scaffolding
  boundary, the stale `.quality-gates-results.json`, and the `check-learnings --no-citations` form. Its item (2) —
  *"the D7 choice is the first thing P5 needs"* — was exactly right and shaped the picker. The deduction is one
  falsifiable prediction that was wrong in both halves: *"it archives **this** receipt, dated 2026-09-26 — a new
  date, so again expect no `-N` suffix."* The trim is positional and oldest-first, which the file it was predicting
  about states in its own front matter. It cost nothing only because the same handoff prescribed the dry run.
- **Phase 3C, D3:** fork Learning **#95** appended — *"send it unchanged"* and *"the read-back is byte-identical"*
  are different tests once the channel adds a line of its own, and what the channel adds is discoverable only from
  what it has already published. A retirement is therefore owed and **is refused, with the rows named:** #55, #64,
  #78 and #94 were each considered and each keeps its basis. This session added no gate, no test and no failure
  mode — the only mechanical artifact it produced is a pull request — so nothing moved any of those lessons into
  enforcement; no later row states any of them at least as generally; every row's artifact still exists.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-26 · [ad hoc] S222 — `fix/sync-github-history` pushed to fork `origin`, and pull request #87 opened upstream (non-commit actions, operator go-ahead)

Two outward actions, each authorized separately at this session's Phase 0 picker, each read back before the next.
**The push:** `9f42c0f..67feb9f` on fork `origin`, one commit (the ratchet tightening), a fast-forward checked with
`git merge-base --is-ancestor` before and `git ls-remote` after. **The open:**
[KJ5HST/methodology#87](https://github.com/KJ5HST/methodology/pull/87), base `main`, head `rmsharp:67feb9f`, title
and body from [`sync-github-route-pr-body.md`](docs/planning/sync-github-route-pr-body.md) — the body being
everything after that file's first standalone rule, sent unchanged, plus the attribution line every pull request from
this fork carries. `gh pr view 87 --json body,headRefOid,mergeable,mergeStateStatus` reads back head `67feb9f`,
`MERGEABLE`, `CLEAN`, and a body byte-identical to the file modulo that line. **This is the first thing this fork has
opened on `KJ5HST/methodology` since 2026-09-21**; #83–#86 are untouched and still sit at `219fb9d`, `77afc12`,
`e2501c5`, `c1167ae` with 0 reviews. Nothing else upstream moved: `upstream/main` is still `6b29d3d`.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-26 · [ad hoc] S222 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

The `2026-09-22-2` shard's three-line pointer block written by `methodology_trim.py` into `HANDOFFS.md`'s front matter
becomes one row at the bottom of [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md)'s table and is
deleted from the ledger — the `.verify.sh` link dropped, since the proof sits beside its shard. **Its own commit, as the
index's fold rule requires:** inside the trim commit the shipped `.verify.sh` fails L2 (fork Learning #58), and that
proof was run from a `--no-local` clone of the trim commit `4b36803` and exits **0** on L1, L2/front-matter and L3.
`HANDOFFS.md` 18,688 B → 18,232 B; the front matter does not grow with this trim. Unlike the previous shard, this
name **does** carry an `-N` suffix: the record that left is the oldest of the three, dated `2026-09-22`, and that
shard name was already taken — the opposite of what the predecessor handoff predicted. `./bin/check-links` OK
(111 links).

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-26 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-22-2.md` (1 record(s), 27,996 B → 18,688 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-22 → 2026-09-22) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-22-2.md`](docs/archive/HANDOFFS-through-2026-09-22-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-22-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-22-2.md.verify.sh)
rather than trusting a digest printed here. Live file 27,996 B → 18,688 B (−33.2%).

### 2026-09-26 · [BL-66] S222 claim — P5 of the BL-66 plan: open the pull request (in progress)

**Deliverable, chosen at this session's Phase 0 picker:** phase P5 of
[`docs/planning/sync-github-route-plan.md`](docs/planning/sync-github-route-plan.md) §5 — the one outward phase of
this plan. `fix/sync-github-history` (`67feb9f`) is pushed to fork `origin` and a pull request is opened against
`KJ5HST/methodology` with [`sync-github-route-pr-body.md`](docs/planning/sync-github-route-pr-body.md) sent
**unchanged** from below its first standalone `---`, then read back with `gh pr view --json body,headRefOid`, diffed
against the file, and its `mergeable` state checked. No rebase is pending: `upstream/main` is unmoved at `6b29d3d`
and is an ancestor of the branch, so the merge is a fast-forward.

**D7's sequencing was decided at the same picker — open now, body unchanged.** This is a stated departure from D7's
*"P5 opens the PR after #84 merges and the branch is rebased"*, taken on three grounds: #84 has had **0 reviews for
six days**, so waiting has no date; the merge is a fast-forward today; and the approved body already discloses both
cross-PR collisions and their built-and-run resolutions (`starter-kit/BOOTSTRAP.md` with #84, 212/0 including #84's
two phrase pins; `.quality-gates.json` with #86, 191/0). D7's other fallback — pre-resolving the `BOOTSTRAP.md`
paragraph toward #84's text — was declined at the picker because it would import wording from an unmerged pull
request into this branch and falsify that section of the approved body, breaking P5's *"sends that text unchanged"*.

**Three outward go-aheads, each given separately:** the branch push to fork `origin`; the pull-request open upstream;
and a push of fork `main` (`43cf345..22bbbc3`, five fork-only doc commits, nothing upstream sees).
**Side action, owed by the retention policy rather than chosen:** this claim makes three receipts, so the
`HANDOFFS.md` trim and its fold follow the Phase 0 report.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-26 · [BL-66] S221 close-out — P4 of the BL-66 plan done, the PR body approved; one ledger trimmed; nothing upstream-facing

- **Deliverable:** P4 of [`sync-github-route-plan.md`](docs/planning/sync-github-route-plan.md) on
  `fix/sync-github-history` (`67feb9f`) — the branch vetted and packaged, and
  [`sync-github-route-pr-body.md`](docs/planning/sync-github-route-pr-body.md) **approved as drafted** by the operator
  after being shown inline. Recorded on `main` at `f79960e`. **P5 — open the pull request — is next and is its own
  go-ahead.**
- **What P4 measured rather than predicted:** the trial merge into `upstream/main` is a **fast-forward** (merge base =
  `upstream/main` = `6b29d3d`; `merge-tree --write-tree` returns the tip's own tree `dee697f`), so the phase's two
  suite clauses are one measurement. Both cross-PR conflicts were **built and run**: with #84 only
  `starter-kit/BOOTSTRAP.md` conflicts and the head+tail resolution runs **212/0 with both of #84's phrase pins
  passing**; with #86 it is `.quality-gates.json` (188 vs 142) plus `CHANGELOG.md`, and that merge measures **191/0**.
  Six adopters, twelve `--dry-run` runs: two flip refused → clean (10 → 15 written, 8 → 16), four refuse the
  **identical file sets** (7, 8, 8, 7) member for member.
- **One commit on the branch:** `tests-sh-passed` floored at the measured **188**. `upstream/main` measures **139/0**,
  so the old floor was exact and the branch adds **49 assertions, removing none**. The ratchet was exercised both
  ways — `--precommit` exit 0 at 188, exit 2 at 138.
- **Side actions, both approved at the Phase 0 picker:** the `HANDOFFS.md` retention trim the claim made owed
  (`9103089`, 3 receipts → 2, S219's to `docs/archive/HANDOFFS-through-2026-09-22.md` — a new shard date, so no `-N`
  suffix, exactly as the predecessor handoff predicted; 25,140 → 16,345 B) and its fold (`6424f37`, → 15,897 B). The
  shard's `.verify.sh` re-derives L1/L2/L3 from git in a clone of the trim commit: exit 0.
- **Phase 3A — the predecessor handoff scores 9/10.** Every checkable claim in it held: the four PR heads, the 139/188
  floor pair, #86's 142, the *"new date, so expect no `-N` suffix"* shard prediction, and above all its two inherited
  items — #84's tail against this branch's head, and the two pinned phrases living only in #84's text (verified: fork
  `main` 2, #84's head 1, this branch 0). Those two are what made the #84 conflict cheap to settle. The one deduction:
  *"tighten in P4, not before … only after the rebase"* is internally ambiguous, since the rebase belongs to P5; it
  cost one measurement to resolve, and the answer was that no rebase is pending.
- **Phase 3C, D3:** fork Learning **#94** appended — a predicted *mechanical* conflict resolution is a claim about
  three trees, and the counterparty's own tests are its only oracle. A retirement is therefore owed and **is refused,
  with the rows named:** #55, #64, #69, #78 and #90 were each considered. Each keeps exactly the basis the 2026-09-20
  adjudication recorded; the only mechanical change this session made was a **threshold**, which enforces a count and
  not a lesson; no later row states any of theirs at least as generally; and every one's artifact still exists.
- **Gate:** `quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results 10575dac7361 · manifest 01a4ae7aa511` in a
  `--no-local` clone of `f79960e` — identical to Phase 0's at `43cf345`; suite 343/0. On the branch, in a clone of
  `67feb9f`: `10/10 · results 2162213f5332 · manifest 24be12b693f1`, suite **188 passed, 0 failed, 0 SKIP**.
- **Three Phase 0 findings, all carried into the receipt:** the tracked `.quality-gates-results.json` is stale (head
  `431279b`, 2026-09-19), which is why the dashboard reads *10 pass … (stale)* and why the citation was confirmed from
  a clone; the dashboard's *"1 loosened"* is historical and single, `tests-sh-passed` 327 → 294 at `368b29cd`, the
  operator-approved BL-57 D10 change and the only loosening in the manifest's whole history; and the hooks are armed
  in this clone (`core.hooksPath=.githooks`, no stale rebase marker).
- **Nothing was pushed anywhere.** `KJ5HST/methodology` is untouched, and fork `origin` has not been pushed this
  session — `main` is ahead of `origin/main` by this session's commits, and the branch is ahead of
  `origin/fix/sync-github-history` by `67feb9f`.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-26 · [BL-66] S221 — P4 of the BL-66 plan done: the branch is vetted and the PR body is approved

**Phase P4 of [`docs/planning/sync-github-route-plan.md`](docs/planning/sync-github-route-plan.md) §5 is DONE on
`fix/sync-github-history`, tip `67feb9f`; nothing is upstream.** The branch gained one commit — `tests-sh-passed`
139 → **188** — and the rest of the phase is measurement plus an approved pull-request body. **P5, which opens the
PR, is next and is its own go-ahead.**

- **The trial merge into `upstream/main` is a fast-forward, so P4's two suite clauses are one measurement.** Merge base
  = `upstream/main` = `6b29d3d`, and `git merge-tree --write-tree upstream/main fix/sync-github-history` exits 0
  returning tree `dee697f`, which is also `fix/sync-github-history^{tree}` — measured, not inferred. Suite in a
  `--no-local` clone of `67feb9f`: **188 passed, 0 failed, 0 SKIP**; `quality_ratchet: 10/10 pass · 0 fail ·
  0 unmeasured · results 2162213f5332 · manifest 24be12b693f1`.
- **Four `merge-tree` probes, re-run at `67feb9f` after the tightening moved the tip:** #83 → `CHANGELOG.md`; #84 →
  `starter-kit/BOOTSTRAP.md` **only** (§2.5 also predicted `CHANGELOG.md`, which auto-merges — a departure);
  #85 → `CHANGELOG.md`; #86 → `.quality-gates.json` **and** `CHANGELOG.md`, the first of those new this phase and the
  tightening's own cost.
- **Both conflicts were resolved, BUILT and RUN, not predicted.** #84: each side's untouched half is byte-identical to
  the merge base, so the head+tail resolution is a fact rather than a reading of one very long line; the merged tree
  runs **212 passed, 0 failed** and **both of #84's phrase pins** (`bin/tests.sh:360`, `:361`) pass — which discharges
  the obligation P3's departure (b) handed to the rebase. #86: one line, 188 vs 142, a minimum resolving upward; the
  merged tree measures **191 passed, 0 failed**, the floor for whoever merges second.
- **The tightening is the measured value, and the guard was exercised.** `upstream/main` measures **139 passed, 0
  failed**, so the old floor was exact rather than slack, and the branch adds **49 assertions and removes none**
  (`comm` over both runs' sorted `PASS:` lines). `--precommit` accepts 188 (exit 0) and, as a control, refuses the
  same line at 138 (exit 2). Done now rather than at P5 because there is no rebase pending — the branch's base *is*
  `upstream/main` — and a `min` gate cannot be invalidated by a merge that only adds tests.
- **Six adopters, twelve `--dry-run` runs, fork `main` `6424f37` versus the branch:** two flip from refused to a clean
  update (10 refused → **15 would write**; 8 → **16**), with every refused file inside the branch's would-write set,
  checked per file; four refuse the **identical file sets** (7, 8, 8, 7) member for member, because those edits are
  real. Measured incidentally: the old route issues 29 HTTPS calls per run at 12–15 s and had **4 of 29 time out** in
  one of the twelve (exit 1, 52 s, nothing read); the clone route ran 1.7–2.7 s.
- **The body is [`docs/planning/sync-github-route-pr-body.md`](docs/planning/sync-github-route-pr-body.md), APPROVED
  AS DRAFTED** by the operator at this session's picker, shown inline first; the two editorial trims offered were both
  declined, so P5 sends the text unchanged. Both quotations verified verbatim (issue #32's Scope list and #84's body);
  the `--source` help string verbatim at `upstream:191`/`upstream:144`; 0 hits on the recognized-terms grep, which the
  file now scopes to the body because the whole-file form matches its own scaffolding — a departure from the phase's
  third verification command. The body names **no adopter project**, by choice: they are private repositories and the
  evidence needs only their counts.
- **Not exercised:** anything on GitHub; the maintainer's merge order or environment; `bin/status` from a history-less
  source, still the recorded open point.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-26 · [ad hoc] S221 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

The `2026-09-22` shard's three-line pointer block written by `methodology_trim.py` into `HANDOFFS.md`'s front matter
becomes one row at the bottom of [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md)'s table and is
deleted from the ledger — the `.verify.sh` link dropped, since the proof sits beside its shard. **Its own commit, as the
index's fold rule requires:** inside the trim commit the shipped `.verify.sh` fails L2 (fork Learning #58), and that
proof was run from a `--no-local` clone of the trim commit `9103089` and exits **0** on L1, L2/front-matter and L3.
`HANDOFFS.md` 16,345 B → 15,897 B; the front matter does not grow with this trim. This is the first shard whose name
carries **no `-N` suffix since `2026-09-21`** — a new date, exactly as the predecessor handoff predicted.
`./bin/check-links` OK (111 links).

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-26 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-22.md` (1 record(s), 25,140 B → 16,345 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-22 → 2026-09-22) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-22.md`](docs/archive/HANDOFFS-through-2026-09-22.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-22.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-22.md.verify.sh)
rather than trusting a digest printed here. Live file 25,140 B → 16,345 B (−35.0%).

### 2026-09-26 · [BL-66] S221 claim — P4 of the BL-66 plan: vet and package the branch (in progress)

**Deliverable, chosen at this session's Phase 0 picker:** phase P4 of
[`docs/planning/sync-github-route-plan.md`](docs/planning/sync-github-route-plan.md) §5, on `fix/sync-github-history`
at `9f42c0f` — the last phase before the pull request, which is P5 and its own go-ahead. Four things: the suite green in
a `--no-local` clone of the branch tip **and** of its trial merge into `upstream/main`; `git merge-tree --write-tree
--name-only` against each of the four open PR heads with the conflicting paths **measured** and recorded in the plan,
against §2.5's prediction of `starter-kit/BOOTSTRAP.md` + `CHANGELOG.md` with #84 and `CHANGELOG.md` with the other
three; a `--source=github --dry-run` of the branch's `bin/sync` against each of the six adopters, recorded as
before/after row counts against fork `main`'s copy; and the pull-request body drafted in
`docs/planning/sync-github-route-pr-body.md` in recognized terms, shown to the operator inline before any review picker.
`tests-sh-passed` is tightened on the branch in this phase and not before — its floor is 139 and it measures 188, and
PR #86 moves the same line to 142, so the tightening follows the trial merges. Nothing opens or is pushed upstream.
**Side actions approved:** the `HANDOFFS.md` retention trim this claim makes owed, and its fold.

- **Model:** Claude Opus 5 (claude-opus-5)

