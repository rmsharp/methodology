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

**Archived 89 record(s), 2026-09-26 → 2026-09-30** into [`docs/archive/CHANGELOG-through-2026-09-30.md`](docs/archive/CHANGELOG-through-2026-09-30.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-09-30.md.verify.sh`](docs/archive/CHANGELOG-through-2026-09-30.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

**Archived 336 record(s), 2026-08-10 → 2026-10-04** into [`docs/archive/CHANGELOG-through-2026-10-04.md`](docs/archive/CHANGELOG-through-2026-10-04.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-10-04.md.verify.sh`](docs/archive/CHANGELOG-through-2026-10-04.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.7.0.

**Archived 132 record(s), 2026-10-05 → 2026-10-06** into [`docs/archive/CHANGELOG-through-2026-10-06.md`](docs/archive/CHANGELOG-through-2026-10-06.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-10-06.md.verify.sh`](docs/archive/CHANGELOG-through-2026-10-06.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.8.0.

**Archived 66 record(s), 2026-10-07 → 2026-10-07** into [`docs/archive/CHANGELOG-through-2026-10-07.md`](docs/archive/CHANGELOG-through-2026-10-07.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-10-07.md.verify.sh`](docs/archive/CHANGELOG-through-2026-10-07.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.8.0.

**Archived 88 record(s), 2026-10-07 → 2026-10-08** into [`docs/archive/CHANGELOG-through-2026-10-08.md`](docs/archive/CHANGELOG-through-2026-10-08.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-10-08.md.verify.sh`](docs/archive/CHANGELOG-through-2026-10-08.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.8.0.

**Archived 101 record(s), 2026-10-08 → 2026-10-11** into [`docs/archive/CHANGELOG-through-2026-10-11.md`](docs/archive/CHANGELOG-through-2026-10-11.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-10-11.md.verify.sh`](docs/archive/CHANGELOG-through-2026-10-11.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.8.0.

**Archived 167 record(s), 2026-10-12 → 2026-10-14** into [`docs/archive/CHANGELOG-through-2026-10-14.md`](docs/archive/CHANGELOG-through-2026-10-14.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-10-14.md.verify.sh`](docs/archive/CHANGELOG-through-2026-10-14.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.8.0.

**Archived 126 record(s), 2026-10-14 → 2026-10-15** into [`docs/archive/CHANGELOG-through-2026-10-15.md`](docs/archive/CHANGELOG-through-2026-10-15.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-10-15.md.verify.sh`](docs/archive/CHANGELOG-through-2026-10-15.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.8.0.

**Archived 89 record(s), 2026-10-16 → 2026-10-19** into [`docs/archive/CHANGELOG-through-2026-10-19.md`](docs/archive/CHANGELOG-through-2026-10-19.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-10-19.md.verify.sh`](docs/archive/CHANGELOG-through-2026-10-19.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.8.1.

**Archived 110 record(s), 2026-10-19 → 2026-10-20** into [`docs/archive/CHANGELOG-through-2026-10-20.md`](docs/archive/CHANGELOG-through-2026-10-20.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-10-20.md.verify.sh`](docs/archive/CHANGELOG-through-2026-10-20.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.8.1.

---

## 2026-09

## 2026-10

### 2026-10-22 · [BL-108] S361 close-out -- the `HANDOFFS.md` retention rule now trims above four receipts (depth three); BL-126 raised; the receipt complete; nothing sent upstream

Phase 3 of the session whose claim stands below (`CHANGELOG: pending` is resolved by this entry and the entries between). The work is `94375552` (the retention paragraph in the root `HANDOFFS.md` front matter: trigger above four, depth three, the reason in bytes) and the follow-up `2e5688c8` (BL-126 raised, four figures in the work entry named as 13 B off). Before the claim, at his Phase 0 picker: the push (`820e4eea` to `18943b46`). The trim he was offered was not run, by his own later answer. Gate run, taken in a clean `--no-local` clone of `2e5688c8` (5 receipts in the tree, after the claim): `quality_ratchet: 24/24 pass · 0 fail · 0 unmeasured · results 5b1b7d2357d2 · manifest 969de61a8185`, 1,375 s, `tests-sh-passed` 580 against its floor of 580; identical to S360's citation, as a text-only change should be. Handoff receipt: `HANDOFFS.md`, S361, scores 7 (self) and 9 (S360's handoff, re-read before scoring). No row appended to `docs/FORK_LEARNINGS.md`, so the retire-or-refuse rule (D3) was not triggered; rows considered: #34, #32, #70, #81 (the receipt says why none is retired or needed). **Not done, by design:** BL-124's second half (the manual's token count, his S358 decision; it is next), BL-126 itself (raised, his call), the `HANDOFFS.md` trim (due by the new rule at the next Phase 0: 5 receipts at rest), and any push of this session's 4 commits (his call). Nothing was sent to `KJ5HST/methodology`.

### 2026-10-22 · [BL-126] S361 follow-up -- BL-126 raised: nothing fails when `HANDOFFS.md` passes its 65,536 B ceiling, and the new trim-above-four rule lets it close a session at about 59 KB; not started; fork `main` only; nothing sent upstream

Found while changing the rule (the work entry below). Raised, not fixed: a gate is a second deliverable and his call. One index row in `docs/planning/BACKLOG.md` (open index rows 45 to 46) and one body in `docs/planning/BACKLOG-DETAIL.md` with its `<a id>`; the row and body record what holds the ceiling today (a status line that already exits 2 for four other files, no `.quality-gates.json` entry naming `HANDOFFS` or 65,536, Test 39's A1 covering only three receipts) and two options (a `max` gate reading `max_bytes` from `.context-budget.json`, or leave it; the worst case is bounded at 1,898 B over, five receipts at the 12,288 B record limit). **A correction to my own work entry, which stays as committed (a committed entry is never edited):** its byte figures were computed with a front matter of 5,981 B and the final edit made it 5,994 B, so four figures there are 13 B off and should read 59,404 (not 59,394), 70,086 (not 70,076), 67,434 and 1,898 over (not 67,421 and 1,885) and 64,794 and 742 under (not 64,781 and 755); the backlog row and body carry the corrected figures, and the paragraph in `HANDOFFS.md` rounds to the nearest KB and is unaffected. **Checked after:** the three backlog proofs (`BACKLOG-DETAIL.md`, `BACKLOG-COMPLETED.md`, the 2026-08-15 archive), `check-backlog-anchors` (87 links on 100 anchors), `check-ledger` and `check-links` all exit 0. Nothing was sent to `KJ5HST/methodology`.

### 2026-10-22 · [BL-108] S361 work -- `HANDOFFS.md`'s retention paragraph now triggers a trim above FOUR receipts, not above three; the depth stays three, `--cut 3 --force`; text only, fork `main` only; nothing sent upstream

His choice, "Trigger above four (Recommended)", from a picker of four (that, keep the cadence and state its reason, trim at close-out, leave it). Edited the front matter of `HANDOFFS.md` in five spans: the heading (`trim above FOUR`), the attribution (a sentence saying the trigger moved on 2026-10-22, S361, and the depth stayed three), the depth-and-trigger sentences (the trigger sits two above the depth, a trim archives two receipts, a trim falls at every second Phase 0), the count step (`above 4`) and the floor sentence (the file holds three to five receipts). **The paragraph now gives the reason in bytes, measured this session:** receipts run 9,876 to 11,760 B (mean 10,682 B, S357 to S360), so five complete receipts are about 59 KB (59,394 B at the mean) under the 65,536 B ceiling and six about 70 KB (70,076 B) over it; five is over the one-read cap (about 56.7 KB, 25,000 tokens at the status tool's own density of 2.2657 B/token, which it calls provisional), so every second close-out reads OVER in `context_budget.py --status`, and no gate reads that. **It also states what the rule rests on:** at the 12,288 B record budget five receipts would be 67,421 B, 1,885 B over the ceiling, so the trigger holds only while receipts stay near their measured size; five of the largest measured (11,760 B) would be 64,781 B, 755 B under. **Replaced reason:** the old text argued a fixed ~16 KB proof per trim for a trigger one above the depth, which saves nothing when each trim removes one receipt. Front matter 5,241 B to 5,994 B (83% of Test 39 A2's 7,168 B reserve, measured with the test's own split). **Checked after:** `check-ledger` and `check-links` exit 0; `check-handoff` printed only the pending-receipt error (S361's own); the trimmer's dry run (`--cut 3 --force`) still reads L1, L2 and L3 OK against the new front matter (it would archive 2 of 5 records, 49,460 B to 27,470 B; nothing written); a search outside the archives and the ledgers finds no other live text that says 'trim above three'. **Unchanged:** `RETENTION_FLOOR` (3), the A1 fit, the trimmer, the runner, every test, `BACKLOG-COMPLETED.md`'s BL-108 row (a dated record of S359: it still says 'trim above THREE', true of its day). The S360 trim offer for S357 was not run, by his answer. Nothing was sent to `KJ5HST/methodology`.

### 2026-10-22 · [BL-108] S361 claim (in progress) -- revisit the `HANDOFFS.md` retention rule (keep three, trim above three) that BL-108 wrote down at S359; fork `main` only; nothing sent upstream

Claimed at the operator's answer "Revisit the rule now" to a picker offering three ways forward, after he asked "perhaps my rule should be revisited. What is it's justification?" (he had asked "why is this a recommended action" about the trim first). His Phase 0 picker had chosen BL-124's second half plus two go-aheads; the deliverable moved to the rule when he made that answer, and BL-124's second half (count the manual's tokens) waits for the next session. **Before the claim, one go-ahead was done:** the push of `main` to the fork's `origin` (`820e4eea` to `18943b46`, 7 commits; `git ls-remote` equal to `HEAD`, `0 0` apart). **The other go-ahead, the `HANDOFFS.md` trim, was not done:** his later answer skips it, so the file holds 4 receipts and 5 with the claim; the dry run (S357 to `docs/archive/HANDOFFS-through-2026-10-21-2.md`, 47,971 B to 36,667 B, all three lossless checks passing) wrote nothing. **The justification, read from the sources before he chose:** the depth of three rests on `RETENTION_FLOOR = 3` in `bin/check-handoff` and Test 34 (below three, six assertions print `SKIP`), and on S358's decision to write down what 23 trims (2026-10-17 to 2026-10-21) had done, each from 4 receipts to 3; BL-59's measurement (the newest receipt alone does the handoff) gives no reader reason for it; the trigger 'one above the depth' saves nothing when each trim removes one receipt, so a trim falls due at every Phase 0, the cadence his S313 question was about. Phase 0: both ledger frontiers current (`18943b46`), 0 undocumented commits, 0 merges, no pending receipt, `check-ledger` and `check-handoff` exit 0; dashboard 72/100 (its run added one line to `dashboard_history.jsonl`, carried by this claim); #96 (`ad5c980`, 0 comments), #94 (`1670c5d`, 2), #92 (`8a232bb`, 2), #93 (1) and #95 (0) open and unchanged, `upstream/main` `f34769f`. The local `.quality-gates-results.json` is gitignored and dates from 2026-10-10, so it neither confirms nor contradicts S360's gate citation (made in a clean clone).

### 2026-10-22 · [BL-124] S360 close-out -- BL-124's first half done (the four stale sizes are gone from the note); the receipt complete; nothing sent upstream

Phase 3 of the session whose claim stands below (`CHANGELOG: pending` is resolved by this entry and the entries between). The work is `afa1e29f` (the four stale sizes out of `.context-budget.json`'s `_deliberate_exclusions` note, which now says to read sizes with `wc -c`) and the closure `9d8fac9d` (BL-124's index row records the first half; the row stays open for the token measurement). Before the claim, at his Phase 0 picker: the push (`8f26f2ed` to `820e4eea`), the `HANDOFFS.md` trim `a0e00250` with its fold `c89581b8`, and the `CHANGELOG.md` trim `96dc6f9d` (forced past `SRF_RED` at his second tick). Gate run, taken in a clean `--no-local` clone of `9d8fac9d` (4 receipts in the tree, after the claim): `quality_ratchet: 24/24 pass · 0 fail · 0 unmeasured · results 5b1b7d2357d2 · manifest 969de61a8185`, under 1,420 s, `tests-sh-passed` 580 against its floor of 580; identical to S359's citation, as a change to a note and the ledgers should be. Handoff receipt: `HANDOFFS.md`, S360, scores 8 (self) and 8 (S359's handoff, re-read before scoring). No row appended to `docs/FORK_LEARNINGS.md`, so the retire-or-refuse rule (D3) was not triggered; the one lesson (a dry run's verdict belongs to the file's size at that moment) went to a memory, not a row. **Not done, by design:** the manual's token measurement (his S358 decision), the ledger regrowth rate as a backlog row (his tick was 'Force the trim'), and any push of this session's 7 commits (his call). Nothing was sent to `KJ5HST/methodology`.

### 2026-10-22 · [BL-124] S360 closure -- BL-124's index row records its first half as done (`afa1e29f`); the row stays open for the second half; nothing sent upstream

`docs/planning/BACKLOG.md`: the row's head now reads 'quoted four stale file sizes (deleted at S360)' and its tail 'First half DONE S360 (`afa1e29f`) ... Second half not started'. 1 insertion, 1 deletion. Open index rows stay 45 (nothing closed, so no `BACKLOG-COMPLETED.md` row and no detail edit; the detail proof pins the detail body, and decisions ride the index row). The three backlog proofs, `bin/check-backlog-anchors` and `bin/check-links` each exit 0 run alone from the repo root.

### 2026-10-22 · [BL-124] S360 work -- the four stale file sizes are gone from `.context-budget.json`'s `_deliberate_exclusions` note, replaced by a pointer to `wc -c`; text only; fork `main` only; nothing sent upstream

Deleted `90,453 B (wc -c, 2026-08-30)` (`README.md`), `55,895 B` (`ITERATIVE_METHODOLOGY.md`), `(15,493 B, ` (`FRAMEWORK_APPARATUS.md`) and `116,749 B` (`docs/planning/BACKLOG-DETAIL.md`); the list now opens "STILL EXCLUDED (read their sizes with `wc -c`; none is written here)". One line changed (the note is one JSON string): 1 insertion, 1 deletion. Measured today with `wc -c`: `README.md` 99,793 B, `ITERATIVE_METHODOLOGY.md` 66,331 B, `FRAMEWORK_APPARATUS.md` 30,083 B, `BACKLOG-DETAIL.md` 484,666 B (S356 read 479,525 B, so the last one had already moved on again). **Kept on purpose:** the dated 68,240 B before-figure for S130's move, the 196,608 B and 65,536 B figures (constants that live in code), and the sentence 'Both now fit one read, which is why neither needs a ceiling'. That sentence is the part BL-124 says may no longer be true of the manual (66,331 B is about 25,400 to 29,200 tokens by two estimates against the 25,000-token read cap); its token measurement is the second half, his S358 decision (a later session, token meter in a subagent with a control), so the row stays open. **Checked:** the file parses; `grep -c -E '90,453|55,895|15,493|116,749'` reads 0; only the `_deliberate_exclusions` key differs from the pre-edit copy; `context_budget.py --status` output is byte-identical before and after (exit 2 both: the standing exit); `tools/test_context_budget.py` 163 tests OK.

### 2026-10-22 · [BL-124] S360 claim (in progress) -- delete the four stale file sizes from `.context-budget.json`'s `_deliberate_exclusions` note (BL-124's first half); fork `main` only; nothing sent upstream

Claimed at the operator's Phase 0 picker answer "BL-124 first half (Recommended)". The picker also took three go-aheads, all done before this claim. **The push** of S359's four commits to the fork's `origin` (`8f26f2ed` to `820e4eea`; `origin/main` equal to `HEAD`, `0 0` apart). **The `HANDOFFS.md` trim** (`a0e00250`, 5 receipts to 3, S356 and S355 to the `2026-10-21` shard, 60,074 B to 38,543 B; `--check` said the byte trigger does not fire, so it took `--cut 3 --force` on his keep-three rule; he ran the `--write` with `!`) and its fold (`c89581b8`, 38,095 B). **The `CHANGELOG.md` trim** (`96dc6f9d`, 110 of 170 records, 2026-10-19 to 2026-10-20, to the `-2026-10-20` shard, 204,168 B to 98,901 B; he ran the `--write --force` with `!`). **A correction to my own dry run:** the first `CHANGELOG.md` dry run (202,531 B, regrowth ratio 0.9968) showed no refusal, and I told him no override was needed; the fold and trim entries then added 1,637 B and the ratio read 1.0125, `SRF_RED` ("do not archive again"), so I asked again and he chose "Force the trim". The ratio is the regrowth since the last archive (`aadb439`, S348, 2026-10-20, 104,055 B removed) over what it removed: 105,359 B grew back in two days. The shard proofs, `check-ledger` and `check-handoff` exit 0 after each. Phase 0: both ledger frontiers current (`820e4eea`), 0 undocumented commits, 0 merges, no pending receipt; dashboard 72/100 (its run added one line to `dashboard_history.jsonl`, carried by this claim); #96 (`ad5c980`, 0 comments), #94 (`1670c5d`, 2), #92 (`8a232bb`, 2), #93 (1) and #95 (0) open and unchanged, `upstream/main` `f34769f` unchanged since 2 October; the S359 receipt's gate citation (24/24) could not be checked against the stale local results file (10 October, gitignored) and the gates file last changed at `1ed1d2c1`, before the cited run. Scope: the four sizes in the note, replaced by a pointer to `wc -c`. Not taken: the manual's token measurement (his S358 decision), any ceiling, the note's 'fifth, softer hit'.

### 2026-10-22 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-10-20.md` (110 record(s), 204,168 B → 98,901 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **110** record(s) (2026-10-19 → 2026-10-20) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-10-20.md`](docs/archive/CHANGELOG-through-2026-10-20.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-10-20.md.verify.sh`](docs/archive/CHANGELOG-through-2026-10-20.md.verify.sh)
rather than trusting a digest printed here. Live file 204,168 B → 98,901 B (−51.6%).

### 2026-10-22 · [ad hoc] S360 fold -- the trim's pointer block leaves `HANDOFFS.md` and one row joins `docs/HANDOFFS_ARCHIVE_INDEX.md`

The block (4 lines, 38,543 B to 38,095 B) became the row `| 2 | 2026-10-21 → 2026-10-21 | HANDOFFS-through-2026-10-21.md | v1.8.1 |`. Own commit, as the index's rule says (fork Learning #58); the shard's verify script, `bin/check-handoff` and `bin/check-ledger` exit 0 after it. Taken at the operator's Phase 0 picker answer to trim `HANDOFFS.md` (five receipts to three, on his keep-three rule; the trimmer's `--check` said its byte trigger did not fire, so the cut took `--cut 3 --force`); he ran the `--write` himself with the `!` prefix, and the trim is `a0e00250`. The same picker also took the push of S359's four commits to the fork's `origin` (`8f26f2ed` to `820e4eea`, read back equal, 0 apart; nothing went upstream).

### 2026-10-22 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-21.md` (2 record(s), 60,074 B → 38,543 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-10-21 → 2026-10-21) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-21.md`](docs/archive/HANDOFFS-through-2026-10-21.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-21.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-21.md.verify.sh)
rather than trusting a digest printed here. Live file 60,074 B → 38,543 B (−35.8%).

### 2026-10-22 · [BL-108] S359 close-out -- BL-108 done (the retention paragraph states keep three, trim above three); the receipt complete; nothing sent upstream

Phase 3 of the session whose claim stands below (`CHANGELOG: pending` is resolved by this entry and the entries between). The work is `dc665e30` (`HANDOFFS.md`'s front-matter retention paragraph: keep THREE, trim above THREE, `--cut 3 --force`, and what the rule costs: a trim at every Phase 0), the closure `2b00451e` (BL-108 closed, open index rows 46 to 45). Gate run, taken in a clean `--no-local` clone of `2b00451e` (5 receipts in the tree, after the claim): `quality_ratchet: 24/24 pass · 0 fail · 0 unmeasured · results 5b1b7d2357d2 · manifest 969de61a8185`, 1,375 s, identical to S358's citation as a text-only change should be. The fork's `origin` was pushed at the Phase 0 picker (`a0a34c4b` to `8f26f2ed`, read back equal); the three commits since (claim, work, closure) and this one are local, and a push of them is his call. Two things were offered and not done: the `HANDOFFS.md` trim (not ticked; the file holds 5 receipts, so the next trim archives two, and with this receipt the file is 59,699 B, which `context_budget.py --status` reads at about 26,349 tokens against its 25,000-token ceiling, newly OVER; the tool's exit 2 was already standing and it is not one of the 24 gates) and the `CHANGELOG.md` trim (ticked, then skipped by his answer after the trimmer said `NOTHING_TO_DO`; the file is now past its trigger, so the next Phase 0's `--check` fires with no override). Handoff receipt: `HANDOFFS.md`, S359, scores 7 (self) and 8 (S358's handoff). Nothing was sent upstream; no Learnings row appended, so no retirement or refusal is owed (row 70 considered: its premise is stale, its lesson stands).

### 2026-10-21 · [BL-108] S359 closure -- BL-108 closed (work commit `dc665e30`); open index rows 46 to 45; fork `main` only; nothing sent upstream

The backlog's three edits: BL-108's index row out of `docs/planning/BACKLOG.md`, its id into the Completed list between BL-107 and BL-109, its row into `docs/planning/BACKLOG-COMPLETED.md`. Its body in `BACKLOG-DETAIL.md` is untouched (the detail proof pins it). The Completed row records what the stated rule costs (a trim at every Phase 0, by construction) and the two ways he could change that, so the decision is not read as having fixed the cadence. All of these exit 0 after the edit, each run on its own: the completed, detail and archive proofs, `bin/check-backlog-anchors`, `bin/check-ledger`, `bin/check-links`.

### 2026-10-21 · [BL-108] S359 work -- `HANDOFFS.md`'s retention paragraph now states the practice: keep THREE, trim above THREE, `--cut 3 --force`; text only, fork `main` only; nothing sent upstream

Edited the front matter of `HANDOFFS.md` (13 insertions, 12 deletions; 4,895 B to 5,241 B against Test 39 A2's 7,168 B reserve). Four hunks: the rule and its attribution (N=3, his S358 picker of 2026-10-21, replacing N=2 of S232 and the S322 'trim above 3, cut to 2'); the trigger (`above 3`, `--cut 3 --force`); the `RETENTION_FLOOR` sentence (it now equals the depth, so the file holds three after a Phase 0 trim and four after the claim, Test 34's six SKIP rows never print, and the old 'six lower at rest' is named as the N=2 behaviour); and the callout's heading (the floor, which the depth now sits on). **One sentence is new and says what the rule costs:** a session adds one receipt and removes none, so every Phase 0 counts four and archives one, the cadence his S313 question was about. **Checked before writing it:** the commits that touched `HANDOFFS.md` since 2026-10-17, receipt fences counted before and after each, show 23 trims, S332 to S354, every one 4 to 3 (the backlog row's 'since S325' and the review's 'since session 330' were both imprecise). **Checked after:** no test, tool or gate reads the paragraph's wording (grep over `bin/`, `tools/`, `starter-kit/`, `.quality-gates.json`, `.context-budget.json`); the only live text that said 'keep two' was this paragraph; `bin/check-ledger` exit 0; `bin/check-handoff` reports only the pending-receipt error, as it must until close-out. Not changed: `RETENTION_FLOOR` (3), the A1 fit, the trimmer, the runner, any test. Not done: the `HANDOFFS.md` trim (not ticked at the picker), so the file holds 5 receipts, not 3.

### 2026-10-21 · [BL-108] S359 claim (in progress) -- state the `HANDOFFS.md` retention practice (trim above 3, keep 3); fork `main` only; nothing sent upstream

Claimed at the operator's Phase 0 picker answer "BL-108: state the retention rule (Recommended)". The picker also took two go-aheads: the push of `main` to the fork's `origin` (`a0a34c4b` to `8f26f2ed`, 7 commits, S358's work and close-out; `git ls-remote` equal to `HEAD`, `0 0` apart) and a `CHANGELOG.md` trim. **The trim was not done:** the trigger did not fire (196,505 B against 196,608 B; `--check` and the dry run both said `NOTHING_TO_DO`), a lowered `--budget-bytes` would have forced it, he asked why the file needed trimming when the trimmer said nothing was due, and answered "skip" to the explanation that it did not. Nothing was written; the first entry past the trigger lets the next Phase 0's `--check` fire without an override. The `HANDOFFS.md` trim (4 receipts, due under trim-above-3) and a gate re-run were offered and not ticked. Phase 0: both ledger frontiers current (`8f26f2ed`), 0 undocumented commits, 0 merges, no pending receipt, `check-ledger` and `check-handoff` exit 0, dashboard 72/100 (its run added one line to `dashboard_history.jsonl`, carried by this claim); #96 (`ad5c980`, 0 comments), #94 (`1670c5d`, 2), #92 (`8a232bb`, 2), #93 (1) and #95 (0) open and unchanged, `upstream/main` unchanged since 2 October. The newest receipt's 24/24 gate citation was not re-checked (the results file on disk is from 10 October). Scope: the front matter's 'Retention policy' paragraph in `HANDOFFS.md` and the backlog closure. BL-124, BL-125 and BL-92 shape (c) are not taken.

### 2026-10-21 · [BL-106] S358 close-out -- BL-106 done (two size gates for the plan files that declare a byte budget); BL-125 raised; the receipt complete; nothing sent upstream

S358's one deliverable: `plan-size-directory-move` (60,000 B) and `plan-size-pr-composition` (30,000 B) in `.quality-gates.json`, 22 gates to 24, work commit `1ed1d2c1`, closure `8c29ffd1`. The full 24-gate run in a clean `--no-local` clone of `8c29ffd1` (1,381 s): `24/24 pass · 0 fail · 0 unmeasured · results 5b1b7d2357d2 · manifest 969de61a8185`. Predecessor (S357) scored 9; self-score 8. No Learnings row appended, so no retirement or refusal is owed. Nothing sent upstream and nothing written to any sibling repository; local `main` is 7 commits ahead of the fork's `origin` after this close-out (nothing pushed since `a0a34c4b`). `CHANGELOG.md` is 196,505 B after this entry, 103 B under the 196,608 B trigger (`--check` says the trigger does not fire), so the next session's first entry crosses it: offer a CHANGELOG trim at the next Phase 0 beside the HANDOFFS trim, before any claim.

### 2026-10-21 · [ad hoc] S358 decisions -- three carried calls answered at the operator's picker, each as recommended: BL-124 (measure the manual's tokens first), BL-108 (state the practice: trim above 3, keep 3), sibling sync (not yet, wait for PR #96); fork `main` only; nothing sent upstream

S357's handoff asked that its calls (a) to (c) be put to him at the Phase 0 picker; they were not (only the deliverable and three go-aheads were), so they were put at the close-out instead, with the gate run still going. **BL-124:** "Measure it first": a later session counts `ITERATIVE_METHODOLOGY.md`'s tokens (66,331 B; about 25,400 to 29,200 by two estimates against the 25,000-token cap) with the token meter before any ceiling or cut. **BL-108:** "State the practice: cut to 3": the rule in `HANDOFFS.md`'s front matter is to say trim above 3, keep 3, which is what every trim since S325 did, superseding his S322 'cut to 2'; the edit to that text is not made. **Sibling sync:** "Not yet: wait for PR #96"; nothing was synced, nothing written to any sibling. Recorded as riders on the BL-108 and BL-124 index rows in `docs/planning/BACKLOG.md` (the detail bodies stay as they were, since the detail proof pins them). S357's call (d), whether BL-92's shape (c) rides ratchet 1.6.0, was not asked: it needs BL-103's option (c) read first.

### 2026-10-21 · [BL-106] S358 closure -- BL-106 closed (two size gates, work commit `1ed1d2c1`); BL-125 raised (six plan files declare a budget nothing gates, one 451 B over); fork `main` only; nothing sent upstream

Three backlog edits: BL-106's index row left `docs/planning/BACKLOG.md` and its id joined the Completed list; its row joined `docs/planning/BACKLOG-COMPLETED.md`; BL-125 was raised with an index row in `BACKLOG.md` and a body in `docs/planning/BACKLOG-DETAIL.md` (BL-106's own body stays there as the record, since the detail proof pins it). BL-125 comes from the work's inventory: `grep -i 'declared budget' docs/planning/*.md` found eight declaring files, the six not gated last changed between 2026-08-27 and 2026-09-14 (the two gated plans, 2026-10-20), and `upstream-read-set-pr-plan.md` stands at 45,451 B against its declared 45,000 B. No plan file was edited. The two backlog proofs, `bin/check-backlog-anchors`, `bin/check-ledger` and `bin/check-links` were run from the repository root after the edits (results in the S358 close-out receipt).

### 2026-10-21 · [BL-106] S358 work -- two size gates for the plan files that declare a byte budget (`plan-size-directory-move` 60,000 B, `plan-size-pr-composition` 30,000 B); fork `main` only; nothing sent upstream

`.quality-gates.json` gains two `max` gates (22 to 24), each `wc -c < <plan>` with a digits-only extract, the ceiling the figure the plan's own header declares. They read pass at 59,977 B and 29,999 B. **Measured** in a throwaway fixture repository (the tool, the two entries, copies of the plans): exactly 60,000 B passes, 60,001 B fails (exit 2), the composition plan at 30,001 B fails (exit 2), a missing plan reads `unmeasured` (exit 1), never pass; `quality_ratchet.py --precommit` on the staged manifest says "2 gate(s) added" and exits 0. The extract is anchored because, measured under `dash` (the usual `/bin/sh` on Linux), a failed `< file` redirect prints `dash: 1: cannot open ...`, whose `1` an unanchored `(\d+)` reads as a size of 1 B; this Mac's `/bin/sh` prints no digit, so on this machine the anchor guards nothing. **The inventory** (`grep -i 'declared budget' docs/planning/*.md`) found eight plan files that declare a budget, not the two the review named: six are not gated, and `upstream-read-set-pr-plan.md` is already 451 B over its declared 45,000 B; raised as BL-125, none touched. Scope kept: no plan file was edited. The review's question (is 60,000 B a hard limit or a price he set) was not asked; the gate treats it as the ratchet treats every threshold.

### 2026-10-21 · [BL-106] S358 claim (in progress) -- put a size gate on each plan file that declares a byte budget nothing enforces; fork `main` only; nothing sent upstream

Claimed at the operator's Phase 0 picker answer "BL-106 size gates (Recommended)". The picker also took three go-aheads, all done before this claim: the push below, the `HANDOFFS.md` trim (`47994ee3`, 4 receipts to 3, S354 archived to the `-8` shard, 50,900 B to 39,090 B, run by him with `!`, shard proof exit 0) and its fold (`7c062fc6`, 38,634 B), and a re-run of the 22 quality checks in a clean `--no-local` clone of `a0a34c4b` (1,422 s): `22/22 pass · 0 fail · 0 unmeasured · results ccd48215f346 · manifest 26d37cb455c3`, identical to S357's citation, which the stale local results file (10 October) could not confirm. Phase 0: both ledger frontiers current (`a0a34c4b`), 0 undocumented commits, 0 merges, no pending receipt, `check-ledger` and `check-handoff` exit 0, dashboard 72/100 (its run added one line to `dashboard_history.jsonl`, carried by this claim); #96 (`ad5c980`, 0 comments), #94 (`1670c5d`, 2), #92 (`8a232bb`, 2), #93 (1) and #95 (0) open and unchanged, `upstream/main` unchanged since 2 October; `CHANGELOG.md` 187,827 B before this session's entries against the 196,608 B trigger (`--check`: does not fire). Scope: `.quality-gates.json` gates for the plan files that declare a byte budget, plus the backlog closure. Shape (c) of BL-92, BL-124 and BL-108 are not taken.

### 2026-10-21 · [ad hoc] S358 fold -- the trim's pointer block leaves `HANDOFFS.md` and one row joins `docs/HANDOFFS_ARCHIVE_INDEX.md`

The block (4 lines, 39,090 B to 38,634 B) became the row `| 1 | 2026-10-20 → 2026-10-20 | HANDOFFS-through-2026-10-20-8.md | v1.8.1 |`. Own commit, as the index's rule says (fork Learning #58); the shard's verify script, `bin/check-handoff` and `bin/check-ledger` exit 0 after it. Taken before the S358 claim, at the operator's Phase 0 picker answer to trim `HANDOFFS.md`; he ran the dry run and the `--write` himself with the `!` prefix, and the trim is `47994ee3`.

### 2026-10-21 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-20-8.md` (1 record(s), 50,900 B → 39,090 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-20 → 2026-10-20) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-20-8.md`](docs/archive/HANDOFFS-through-2026-10-20-8.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-20-8.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-20-8.md.verify.sh)
rather than trusting a digest printed here. Live file 50,900 B → 39,090 B (−23.2%).

### 2026-10-21 · [ad hoc] S358 push record -- the fork's `main` pushed to the fork `origin` (`dbba3715` to `a0a34c4b`, 6 commits), head read back

At the operator's Phase 0 picker answer "Push main to fork": `git push origin main` (`https://github.com/rmsharp/methodology.git`, his fork, not `upstream`), then `git ls-remote origin refs/heads/main` read `a0a34c4b9dbf8701a0e0fc76b95bf7efafd654a2`, equal to the local `HEAD` at that moment, and `git rev-list --left-right --count origin/main...HEAD` read `0 0`. The six were S357's trim (`279f0b95`), its fold (`3b57b02a`), the claim (`06c4092c`), the Test 44 work (`59ba1066`), the closure (`23603741`) and the close-out (`a0a34c4b`). Pushed before this session's trim, so the trim and fold (`47994ee3`, `7c062fc6`) and this claim are local until a later push.

### 2026-10-21 · [BL-92] S357 close-out -- BL-92 shapes (a) and (b) done, shape (c) open; the receipt complete; nothing sent upstream

Phase 3 of the session whose claim stands below (`CHANGELOG: pending` is resolved by this entry and the entries between). The `HANDOFFS.md` receipt is `status: complete` (self 8, predecessor S356 9, scored after re-reading its next steps and gotchas: every state, the `-7` shard guess, the CHANGELOG size and the six-commit count matched). **Quality checks:** `quality_ratchet.py --run` in a clean `--no-local` clone of the closure commit `23603741` (1,438 s): `22/22 pass · 0 fail · 0 unmeasured · results ccd48215f346 · manifest 26d37cb455c3`, with `tests-sh-passed` measuring 580 against the new floor of 580. **Phase 3C:** no row appended to `docs/FORK_LEARNINGS.md`, so the retire-or-refuse rule (D3) was not triggered and no row retires; rows considered: #41, #16, #107, #81, #31. **Not done, by design:** the original flake's writer is unidentified (the new assertion cannot see it); BL-92's shape (c) is open; no push (this session's 6 commits are local, and a push waits for his go-ahead); nothing sent upstream.

### 2026-10-21 · [BL-92] S357 closure -- BL-92's row records shapes (a) and (b) done and shape (c) open; the `tests-sh-passed` floor tightened 574 to 580; the Phase 0 re-run of the 22 checks read 22/22

BL-92 is NOT closed: its index row (`docs/planning/BACKLOG.md`) now opens with a rider saying shapes (a) and (b) are done and shape (c), the ratchet keeping a failing gate's output, is open (a distributed-tool change that waits for a ratchet release, and also BL-103's option (c)). The rider rides the INDEX row only, because the detail proof pins the bodies; the open index rows stay 46. `.quality-gates.json`: `tests-sh-passed` 574 to 580, MEASURED by `bash bin/tests.sh` reading `== Summary: 580 passed, 0 failed, 0 skipped ==` (467 s) in a clean `--no-local` clone of the work commit `59ba1066` with 4 receipts in `HANDOFFS.md`, with a `_s357_tightening_bl92` note; `quality_ratchet.py --precommit` exit 0. Both backlog proofs, `bin/check-backlog-anchors` and `bin/check-ledger` exit 0. **The re-run the operator ticked at Phase 0** (22 quality checks in a clean `--no-local` clone of `dbba3715`, 1,474 s): `22/22 pass · 0 fail · 0 unmeasured · results e9c5a438be68 · manifest 195ad2eb1d65`, identical to the figure S356's receipt cited, which the stale local results file (Oct 10) could not confirm. Nothing sent upstream.

### 2026-10-21 · [BL-92] S357 -- Test 44 asserts that `bin/check-overhead` writes nothing in a throwaway fixture repository, and a failure names the paths that moved (shapes a and b); fork `main` only; nothing sent upstream

`bin/tests.sh` only (one file). The assertion compared `git status --porcelain` of the WHOLE live repository before and after two printer runs; it now runs the printer twice inside a fixture (a git repository holding a copy of `bin/check-overhead`, this repository's `.context-budget.json`, its two read-set files and its history file) and compares that tree and the history file's hash. Three helpers, all in Test 44: `snapshot_delta` (the lines that differ between two porcelain snapshots, so a failure prints `> ?? stray.txt` and not two whole snapshots), `build_overhead_fixture`, and `fixture_writes`, which the real assertion and the three kill controls all go through (a copy of the printer that writes a stray file at the fixture root, one that appends to the history file, one that writes beside itself). The printer itself cannot be what changed the live tree (it opens one file for reading and sizes two more), so the old assertion could only ever fail on someone else's write. **Measured, not argued:** in a throwaway clone, with an unrelated process creating and removing an untracked file in it, the old Test 44 read red 7 times in 60 runs (and 1 in 30 earlier), the new one 0 in 60. Test 44 went from 12 to 18 assertions. Written red first (both helpers undefined: red; builder only: 2 red; both: green); the first version's 'equal snapshots give nothing' assertion passed vacuously while `snapshot_delta` was undefined, so it now requires the function to exist. A mutation round of 12 mutants on the new code killed 9; the 3 survivors are equivalent today (a second guard behind another one's message, the exit check that the output-prefix check already implies, and running the live printer instead of the copy, which only matters once the printer writes beside itself). Test 45, which scans `bin/tests.sh` for early-exiting consumers, passes against the changed file. Shape (c), the ratchet keeping a failing gate's output, is a distributed-tool change and is not taken.

### 2026-10-21 · [BL-92] S357 claim (in progress) -- make Test 44 say what failed and stop depending on the live tree (shapes a and b); fork `main` only; nothing sent upstream

Claimed at the operator's Phase 0 picker answer "BL-92: make a flaky test failure say what failed (Recommended)". The picker also took three go-aheads, two done before this claim and one running: the push below, the `HANDOFFS.md` trim (`279f0b95`, 4 receipts to 3, S353 archived to the `-7` shard, 50,933 B to 39,596 B, run by him with `!`, shard proof exit 0) and its fold (`3b57b02a`, 39,140 B), and a re-run of the 22 quality checks in a clean `--no-local` clone of `dbba3715` (running; Phase 3F records the result). Phase 0: both ledger frontiers current (`dbba3715`), 0 undocumented commits, 0 merges, no pending receipt, `check-ledger` and `check-handoff` exit 0, dashboard 72/100 (its run added one line to `dashboard_history.jsonl`, carried by this claim); #96 (`ad5c980`, 0 comments), #94 (`1670c5d`, 2), #92 (`8a232bb`, 2), #93 (1) and #95 (0) open and unchanged; `CHANGELOG.md` 179,561 B before this session's entries, `--check` says the trigger does not fire. Scope: Test 44's no-write assertion (`bin/tests.sh:3871`-`3886`). Shape (c), the ratchet keeping a failing gate's output, is a distributed-tool change and is not taken.

### 2026-10-21 · [ad hoc] S357 push record -- the fork's `main` pushed to the fork `origin` (`0c1802bd` to `dbba3715`, 6 commits), head read back

At the operator's Phase 0 picker answer "Push main to the fork's origin (6 commits)": `git push origin main` (`https://github.com/rmsharp/methodology.git`, his fork, not `upstream`), then `git fetch origin` and `git ls-remote origin refs/heads/main` both read `dbba3715ec349118383cc3a80b6f78b3997ecce4`, equal to the local `HEAD`; `git rev-list --left-right --count HEAD...origin/main` read `0 0`. The six were S356's work (the trim `a73e5e5a`, its fold `9bb4a319`, the claim `e8ab4bb5`, the BL-81 edit `d2708ba0`, the closure `6c62d09f` and the close-out `dbba3715`). Pushed before this session's trim, so the trim and fold (`279f0b95`, `3b57b02a`) and this claim are local until a later push.

### 2026-10-21 · [ad hoc] S357 fold -- the trim's pointer block leaves `HANDOFFS.md` and one row joins `docs/HANDOFFS_ARCHIVE_INDEX.md`

The block (4 lines, 39,596 B to 39,140 B) became the row `| 1 | 2026-10-20 → 2026-10-20 | HANDOFFS-through-2026-10-20-7.md | v1.8.1 |`. Own commit, as the index's rule says (fork Learning #58); the shard's verify script, `bin/check-handoff` and `bin/check-ledger` exit 0 after it. Taken before the S357 claim, at the operator's Phase 0 picker answer to trim `HANDOFFS.md`; he ran the dry run and the `--write` himself with the `!` prefix, and the trim is `279f0b95`.

### 2026-10-21 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-20-7.md` (1 record(s), 50,933 B → 39,596 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-20 → 2026-10-20) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-20-7.md`](docs/archive/HANDOFFS-through-2026-10-20-7.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-20-7.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-20-7.md.verify.sh)
rather than trusting a digest printed here. Live file 50,933 B → 39,596 B (−22.3%).

### 2026-10-21 · [BL-81] S356 close-out -- BL-81 done (the stale prose sizes leave .context-budget.json's notes); BL-124 raised; the receipt complete; nothing sent upstream

Phase 3, in order. **3A:** S355's handoff scored **9** (re-read before scoring; every checked claim held: the `gh pr view` command and the state it expected for all five upstream threads; the trim offer with `--cut 3 --force`, S352 and the `-6` shard it flagged as a guess, which the dry run printed exactly; "7 commits ahead of origin"; the `CHANGELOG.md` size; the review's order putting BL-81 first; wrong: "three stale size notes" for BL-81, which was two stale prose sentences and one tool-watched field). **3B:** self-score **8** (plain-language Phase 0 report and one picker; the push read back; the trim and fold as ticked, in separate commits; S355's 22-gate citation confirmed by a re-run instead of assumed; the tool read before the wording was chosen, which corrected the row's premise; every surviving hit classified; before/after tool output identical; the backlog searched before BL-124; minus a first edit that grew the file, a classified hit written down only at close-out, a wrong dashboard path, an over-broad "all four are small" in the picker, and a no-op wait). **3C:** appended no row to `docs/FORK_LEARNINGS.md`, so the retire-or-refuse rule (D3) was not triggered; rows considered: #61, #74, #58, #73. **Gate run (3E), taken in a clean `--no-local` clone of the closure commit `6c62d09f`** (after the claim, 4 receipts in the tree, 1,387 s): `quality_ratchet.py --run` read `22/22 pass · 0 fail · 0 unmeasured · results e9c5a438be68 · manifest 195ad2eb1d65`; the earlier run at `0c1802bd` (1,320 s) read the same, which confirms S355's citation. The BL-124 body gained one sentence naming a fifth, softer hit (`.context-budget.json:21`, classified at work time and left on purpose). The receipt is complete (self-score 8, predecessor S355 scored 9). Nothing was sent upstream, no sibling repository was written, and no spend cap was touched.

### 2026-10-21 · [BL-81] S356 -- close BL-81 (the stale prose sizes leave `.context-budget.json`'s notes); BL-124 raised

The three-edit close: the BL-81 row left the open index of `docs/planning/BACKLOG.md`, its id joined the Completed list between BL-80 and BL-82, and its completed row went into `docs/planning/BACKLOG-COMPLETED.md` after BL-44's; the body in `BACKLOG-DETAIL.md` stays as the record. Open index rows 46 to 46: BL-81 out, BL-124 in. **BL-124 raised** (row plus body, `BACKLOG-DETAIL.md#bl-124`): the same note quotes four more stale sizes (`README.md`, `ITERATIVE_METHODOLOGY.md`, `FRAMEWORK_APPARATUS.md`, `BACKLOG-DETAIL.md`) and argues the manual and the apparatus "fit one read", which the manual's 66,331 B (about 25,400 to 29,200 tokens by two density estimates, against a 25,000-token cap) may no longer do; searched first (no row, gate or budget entry names it). Both backlog proofs, the archive proof, `bin/check-backlog-anchors`, `bin/check-links` and `bin/check-ledger` exit 0.

### 2026-10-21 · [BL-81] S356 work -- the two stale prose sizes leave `.context-budget.json`'s notes (`_synced`, `_deliberate_exclusions`); fork `main` only

`.context-budget.json` (35,757 B to 35,738 B, 2 lines). The sentence in `_synced` that gave SESSION_RUNNER.md 54,363 B and SAFEGUARDS.md 15,386 B (`wc -c`, 2026-08-30; today 55,578 B and 16,919 B) now says no size is written there and names `python3 starter-kit/context_budget.py --status`, which prints both live against their ceilings; the matching sentence in `_deliberate_exclusions` (the 52,386 B and 54,363 B pair) says the same and keeps its closing rule, *never derive a ceiling from a size written in prose*. **Verified:** `context_budget.py --status` text and `--json` byte-identical before and after (both exit 2, the expected `over` state: the notes are inert); the file still parses as JSON; each replaced sentence matched exactly once; `tools/test_context_budget.py` 163 OK (its gate's floor); the three backlog checks green with the new row below; a grep of `bin`, `tools`, `starter-kit`, `.quality-gates.json` and `.githooks` found nothing that reads the notes' text. **Left on purpose** (classified, not missed): `max_bytes 15,386` and `56,750 - 15,386 = 41,364` are the declared ceilings; the lines that say what stood where (`The 54,363 B / 2026-08-30 that stood here`, and the S205 provenance paragraph) are history; `files[].measured_bytes` (55,406 and 17,129) is a dated reference the tool drift-checks and reads 0.31% and 1.23% off today's sizes against a 25% warning (`DENSITY_DRIFT_WARN`), so the row's premise that `files[]` cannot go stale was half right: it can, and the tool is what watches it. **Found, not fixed:** the same note quotes four more stale sizes (README, the manual, the apparatus, BACKLOG-DETAIL) and argues the manual and the apparatus "fit one read", which the manual's 66,331 B may no longer do: raised as BL-124 in the closure commit.

### 2026-10-21 · [BL-81] S356 claim (in progress) -- delete the stale prose file sizes from `.context-budget.json`'s notes; fork `main` only; nothing sent upstream

Claimed at the operator's Phase 0 picker answer "BL-81 (Recommended)". The picker also took three go-aheads, all three done before this claim or running: the `HANDOFFS.md` trim (`a73e5e5a`, 4 receipts to 3, S352 archived to the `-6` shard, 51,486 B to 40,301 B, run by him with `!`, shard proof exit 0) and its fold (`9bb4a319`, 39,845 B), the push below, and a re-run of the 22 quality checks in a clean `--no-local` clone of `0c1802bd` (running; Phase 3F records the result). Phase 0: both ledger frontiers current (`0c1802bd`), 0 undocumented commits, 0 merges, no pending receipt, `check-ledger` and `check-handoff` exit 0, dashboard 72/100 (medium, 0 high-risk, 0 vulnerabilities; its run added one line to `dashboard_history.jsonl`, carried by this claim); #96 (`ad5c980`, 0 comments), #94 (`1670c5d`, 2), #92 (`8a232bb`, 2) open, #93 (1) and #95 (0) open, all unchanged from S355. The local gate-results file is still the Oct 10 one (head `4afc0d6`), so S355's 22-gate citation was neither contradicted nor confirmed before the re-run. Phase 3F records the rest.

### 2026-10-21 · [ad hoc] S356 push record -- the fork's `main` pushed to the fork `origin` (`7c54aeab` to `0c1802bd`, 7 commits), head read back

At the operator's Phase 0 picker answer "Push the 7 commits to your fork's origin": `git push origin main` (`https://github.com/rmsharp/methodology.git`, his fork, not `upstream`), then `git fetch origin` and `git ls-remote origin refs/heads/main` both read `0c1802bd43c170ae651c5ebb1d7f931cf980e27d`, equal to the local `HEAD`; `git rev-list --left-right --count origin/main...main` read `0 0`. The seven were S355's work (the trim and its fold, the claim, the BL-44 fix, the floor, the backlog closure and the close-out). Pushed before the trim, so the trim and fold (`a73e5e5a`, `9bb4a319`) and this claim are not yet on `origin`. Nothing was pushed to or opened on `upstream`.

### 2026-10-21 · [ad hoc] S356 fold -- the trim's pointer block leaves `HANDOFFS.md` and one row joins `docs/HANDOFFS_ARCHIVE_INDEX.md`

The block (4 lines, 40,301 B to 39,845 B) became the row `| 1 | 2026-10-20 → 2026-10-20 | HANDOFFS-through-2026-10-20-6.md | v1.8.1 |`. Own commit, as the index's rule says (fork Learning #58); the shard's verify script, `bin/check-handoff` and `bin/check-ledger` exit 0 after it. Taken before the S356 claim, at the operator's Phase 0 picker answer "Trim HANDOFFS.md before the claim"; he ran the dry run and the `--write` himself with the `!` prefix, because the permission classifier refuses both for the agent.

### 2026-10-21 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-20-6.md` (1 record(s), 51,486 B → 40,301 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-20 → 2026-10-20) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-20-6.md`](docs/archive/HANDOFFS-through-2026-10-20-6.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-20-6.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-20-6.md.verify.sh)
rather than trusting a digest printed here. Live file 51,486 B → 40,301 B (−21.7%).

### 2026-10-21 · [BL-44] S355 close-out -- BL-44 done (bin/check-learnings prints the observed span and names the reserved gap); the receipt complete; nothing sent upstream

Deliverable: BL-44, fork `main` only. The OK line of `bin/check-learnings` now reads `16 Learning row(s), #1..#17, 1 reserved (#14)`, and the fork's table `94 Learning row(s), #15..#109, 1 reserved (#85)`; Test 32 holds it (9 to 17 assertions), driven RED against the previous checker (8 of 17 failed) and mutation-tested twice. Evidence: the full suite `574 passed, 0 failed, 0 skipped` on committed `e168dae` (floor 566 to 574 in `cd159af`); the three backlog proofs, `check-backlog-anchors`, `check-links` and `check-ledger` exit 0 (closure `a49f203`); `quality_ratchet.py --run` in a clean `--no-local` clone of `a49f203`: 22/22 pass, 0 fail, 0 unmeasured, results `e9c5a438be68`, manifest `195ad2eb1d65` (1,249 s; output kept only in the scratchpad). Also taken at the operator's Phase 0 picker: the `HANDOFFS.md` trim (`5a9828e`, fold `2bd0c7e`), the push of `main` to the fork `origin` (recorded in its own entry), and his answer that the manifest follow-up stays on the fork. The predecessor's handoff (S354) scored 9. No Learnings row appended, so the retire-or-refuse rule was not triggered. `main` is 7 commits ahead of `origin` after this entry; nothing on `upstream`.

### 2026-10-21 · [BL-44] S355 -- close BL-44 (`bin/check-learnings` prints the observed span and names the reserved gap)

Three-edit close: the open row out of `docs/planning/BACKLOG.md` (open index rows 47 to 46), `BL-44` into its Completed list in numeric order (between BL-43 and BL-45), and the completed row appended to `docs/planning/BACKLOG-COMPLETED.md`. The detail block in `BACKLOG-DETAIL.md` stays as the record, as for BL-18. The two `.verify.sh` backlog proofs, `bin/check-backlog-anchors` and `bin/check-links` exit 0. Stated in the completed row, not done: `upstream/main`'s checker (read at `f34769f3`) still prints `contiguous 1..%d`. Nothing sent upstream.

### 2026-10-21 · [BL-44] S355 floor -- `tests-sh-passed` 566 to 574 (`.quality-gates.json`)

Measured, not derived: `bash bin/tests.sh` read `== Summary: 574 passed, 0 failed, 0 skipped ==` on the committed tree `e168dae` (clean status before and after), with 4 receipts in `HANDOFFS.md` (the claim stub and three complete receipts), the state S354 read 566 in; 566 plus the 8 new Test 32 assertions. The threshold only tightens, so the hook accepts it without approval; the note `_s355_tightening_bl44` records the figures beside the earlier ones. Nothing sent upstream.

### 2026-10-21 · [BL-44] S355 `bin/check-learnings` prints the span it observed and names the reserved gap; Test 32 pins it (8 new assertions)

The OK line read `16 Learning row(s), contiguous 1..17` over `starter-kit/FRAMEWORK_LEARNINGS.md` (S176 had already fixed the span to `min..max`), which is still false of a table with a reserved number: 16 rows cannot be 'contiguous' over 17 numbers, and the reader is left to find the missing one. It now reads `16 Learning row(s), #1..#17, 1 reserved (#14)` (and `none reserved` when the table has none; `2 reserved (#2, #9)` sorted), so rows plus reserved equals the span and can be checked by eye. `bin/check-learnings`: `reserved` is computed once and handed to both `check_table` and the message (+8 B net of the comment). The fork's own table reads `94 Learning row(s), #15..#109, 1 reserved (#85)`. `bin/tests.sh` Test 32 (9 to 17 assertions): the fork-table row now matches `#15..#N,` instead of `contiguous 15..`; one row names every reserved number the fork table declares (DERIVED from the file, with a population guard); one reads the canonical table's highest row from the file and expects `#1..#17, 1 reserved (#14)`; three synthetic tables pin none, one and two reserved numbers; three mutants (span from `len(rows)`, gap not named, `sorted()` dropped) each verified to apply. **Driven RED:** against the previous checker 8 of the 17 fail (6 on the old `contiguous` text, 2 mutation rows on `DID NOT APPLY`). **Second mutation round, aimed at behaviour no named test covers:** the reserved count hardcoded to 1, the `#` dropped from the names, `max(valid)` replaced by `len(valid)`, `min(valid)` replaced by 1 and the none-text reworded were each killed (1, 4, 4, 2, 2 failing assertions); a first attempt at the `#` mutant landed on the earlier duplicate-number message by an unanchored `replace` and passed, so it was re-aimed at the new line and killed. Test 32 alone, in a scratch harness: 17 passed, 0 failed. The full suite is run next and its figure is in the close-out entry. Canonical-only (`bin/check-learnings` has no manifest row); nothing sent upstream.

### 2026-10-21 · [BL-44] S355 claim (in progress) -- `bin/check-learnings` names a reserved gap in its message; fork `main` only; nothing sent upstream

Claimed at the operator's Phase 0 picker answer "BL-44 checker message (Recommended)". The picker also took, before this claim, the `HANDOFFS.md` trim (`5a9828e`, run by him because the permission classifier held both my dry run and the write; 4 receipts to 3, S351 archived to the `-5` shard, 52,327 B to 41,051 B, shard proof exit 0) and its fold (`2bd0c7e`, 40,595 B), the push recorded above, and his answer that the manifest follow-up stays on the fork. Phase 0: both ledger frontiers current (`7c54aeab`), 0 undocumented commits, 0 merges, no pending receipt, `check-ledger` and `check-handoff` exit 0, dashboard 72/100 (medium, 0 high-risk, 0 vulnerabilities; its run added one line to `dashboard_history.jsonl`, carried by this claim); #96 (`ad5c980`, 0 comments), #94 (`1670c5d`, 2), #92 (`8a232bb`, 2) open, #93 (1) and #95 (0) open, all unchanged from S354; `upstream/main` `f34769f3` (no new commits). Gate-run citation: the local results file is still the Oct 10 one (head `4afc0d6`), so S354's 22-gate numbers were neither re-run nor contradicted. Phase 3F records the rest.

### 2026-10-21 · [ad hoc] S355 push record -- the fork's `main` pushed to the fork `origin` (`e2871a35` to `7c54aeab`, 10 commits), head read back

At the operator's Phase 0 picker answer "Push 10 commits to origin": `git push origin main` (`https://github.com/rmsharp/methodology.git`, his fork, not `upstream`), then `git fetch origin` and `git ls-remote origin refs/heads/main` both read `7c54aeab55fec0c581ed14e0b0869c1cd922b227`, equal to the local `HEAD`; `git rev-list --left-right --count origin/main...HEAD` read `0 0`. The ten were S354's work (the claim, the trim and fold, the three work layers, the floor, the gate-found fix and the close-out). Nothing was pushed to or opened on `upstream`.

### 2026-10-21 · [ad hoc] S355 fold -- the trim's pointer block leaves `HANDOFFS.md` and one row joins `docs/HANDOFFS_ARCHIVE_INDEX.md`

The block (4 lines, 41,051 B to 40,595 B) became the row `| 1 | 2026-10-20 → 2026-10-20 | HANDOFFS-through-2026-10-20-5.md | v1.8.1 |`. Own commit, as the index's rule says (fork Learning #58); the shard's verify script, `bin/check-handoff` and `bin/check-ledger` exit 0 after it. Taken before the S355 claim, at the operator's Phase 0 picker answer "Trim HANDOFFS.md first".

### 2026-10-21 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-20-5.md` (1 record(s), 52,327 B → 41,051 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-20 → 2026-10-20) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-20-5.md`](docs/archive/HANDOFFS-through-2026-10-20-5.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-20-5.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-20-5.md.verify.sh)
rather than trusting a digest printed here. Live file 52,327 B → 41,051 B (−21.5%).

### 2026-10-20 · [BL-79] S354 close-out -- the close-out report tool is distributed through the sync manifest (fork main only); the receipt complete; nothing sent upstream

The session's one deliverable, closed out. At his Phase 0 picker the operator chose "Distribute via the manifest (Recommended)" over copying the tool by hand into the 13 sibling repositories (his first ask), after correcting my assumption: he had thought the tool was already in `bin/_manifest.py`; the plan's P3 had the row and S349 left it out of PR #96 at his word "make this a small PR". **Commits:** the trim `43b38a91` and fold `0df0fd9f` (he ran the trimmer's `--write` himself, the permission classifier having refused mine), the claim `95722e70`, layer 1 `56bf6d1f` (a `[WIP]` checkpoint under the 5-file cap, red by construction) and `4c08a600`, layer 2 `8f63492b` (section 3G and the `SAFEGUARDS.md` sentence, exact text approved at his picker), the floor and the BL-79 row `ba8f1333`, and the gate-found fix `18cd8118`; the close-out commit follows. **Gate run:** `quality_ratchet.py --run` in a clean `--no-local` clone of `18cd8118`, taken after the claim with 4 receipts in the tree: `22/22 pass · 0 fail · 0 unmeasured · results 666e056cd262 · manifest 7adc7e1d3a29` (1,242 s); the first run, of `ba8f1333`, read `21/22` (`migrate-layout-unit-tests-failed` 1, results `919f3570e17f`: two pinned file counts in `tools/test_migrate_layout.py`, a suite only the gate runs). `tests-sh-passed` measured 566 (floor raised 565 to 566). **Predecessor (3A):** S353's handoff scored 9 (the Phase 0 command and every state it expected held; the trim offer's shard name, timing and file list held; its list of his calls named this session's deliverable; missing: the sixth failing dashboard method and the three more suites that pin the file count). **Phase 3C:** no row appended to `docs/FORK_LEARNINGS.md`, so the retire-or-refuse rule (D3) was not triggered; rows considered: #61, #74, #58, #56 and #73. **What is not done, for him:** nothing is pushed or sent upstream (adding the follow-up to #96, or a pull request after #96 merges, is his call; recomputed with `git merge-tree`, a resync after #96 merges conflicts in six files); the 13 sibling repositories are not synced and none was written (each is 5 to 23 tracked files behind, `nprcgenekeepr` has a locally modified `methodology_trim.py`, 8 had uncommitted changes at Phase 0); the `HOW_TO_USE.md`, `README.md` and worked-transcript phrases and BOOTSTRAP Step 10's settings snippet are not done.

### 2026-10-20 · [BL-79] S354 the migration tool's suite takes the new file's count (found by the gate run, not by `bin/tests.sh`); a stale sentence in the BL-101 plan corrected

The first 22-gate run, in a clean `--no-local` clone of `ba8f1333` (1,245 s), read `21/22 pass · 1 fail · 0 unmeasured · results 919f3570e17f`: `migrate-layout-unit-tests-failed` measured 1 against a limit of 0, while `migrate-layout-unit-tests` read 280. The ratchet keeps only numbers, so I re-ran `python3 tools/test_migrate_layout.py` in that clone with its output captured (549 s): `Ran 280 tests, FAILED (failures=2)`, both pinned file counts in the migration's ledger entry, which now says 40 and 39 files (one more than before, the new distributed file): `test_the_ledger_entry_counts_it_among_the_files_it_moved` (39 to 40) and `test_the_entry_says_what_moved_what_was_rewritten_and_by_which_tool` (38 to 39). `tools/test_migrate_layout.py` is edited accordingly (two lines) and the two tests pass alone (5 s). That suite is run by the gate only, not by `bin/tests.sh`, which is why my two 566-pass shell-suite readings never saw it: my pre-run grep looked for 30 and 34, not 38 and 39. The gate read 1 failure where the direct run read 2; I did not chase that difference. Also corrected: line 78 of `docs/planning/methodology-subdirectory-plan.md` said `close_out_report.py` was "not in the manifest, so not delivered" (true when written, false since `56bf6d1f`); the sentence now says it joined at S354, 59,994 B to 59,977 B of the plan's 60,000 B budget; `check-links` and `check-backlog-anchors` exit 0. A full 22-gate re-run on this commit follows.

### 2026-10-20 · [BL-79] S354 the floor tightened (`tests-sh-passed` 565 to 566), the BL-79 row and the plan's status brought up to date

`.quality-gates.json`: `tests-sh-passed` 565 to 566 with a `_s354_tightening_bl79` note. MEASURED: `bash bin/tests.sh` read `566 passed, 0 failed, 0 skipped` on both committed trees of this work (after layer 1 and after layer 2), in 4-receipt state, the same state S353 read 565 in; the one extra is Test 1's per-executable assertion `close_out_report.py is executable`, so no test was added. `docs/planning/BACKLOG.md` BL-79 row (index row only, as the detail proof requires): the follow-up is done on the fork, with the commits, the scratch-adopter result, the unchanged upstream position and the sibling drift. `docs/planning/close-out-report-actuator-plan.md`: an S354 status paragraph after S349's, naming what is not done. The three backlog proofs, `check-backlog-anchors`, `check-links` and `check-ledger` exit 0. **Scratch-adopter check (the plan's P3 verify):** `bin/sync --source=local` into a throwaway project in each layout exits 0; `close_out_report.py` arrives byte-identical to the canonical file (at the project root in the legacy layout, under `methodology/` in the new), the runner's new 3G sentence arrives with it, the tool prints a report from a real complete receipt and `--check` passes it in both layouts. **Read-only preview of the real siblings:** `bin/status` over the 13 repositories that carry a runner reports the new file `tracked / missing` in each, at its own layout's path; every one is also behind on other tracked files (5 to 23 each, runners 1 to 14 versions behind) and `nprcgenekeepr` has a locally modified `methodology_trim.py`, so a sync brings much more than this file. Nothing was written in any sibling repository.

### 2026-10-20 · [BL-79] S354 layer 2: `SESSION_RUNNER.md` section 3G tells a session to run the report tool; `SAFEGUARDS.md` stops saying no hook is shipped

Shown to the operator as exact before/after text with measured sizes, applied at his picker answer "Apply both as shown". `starter-kit/SESSION_RUNNER.md` 3G is now one sentence (`Run python3 close_out_report.py (--help lists its inputs) and print its output as your last message: deliverable, self-assessment, predecessor's score and findings, next session.`) above the unchanged `**Then STOP. The session is over.**`: 55,585 B to 55,578 B (-7). `starter-kit/SAFEGUARDS.md` "Close-Out Completeness Hook": the sentence "a recommendation, not a shipped mechanism" (untrue once the tool syncs) now says the methodology ships one script for it and installs nothing; the `How to check` bullet is tightened and dropped its aside "exactly as you copy `.githooks/pre-commit`": 16,948 B to 16,919 B (-29). `context_budget.py --status`: read-set 72,533 B to 72,497 B (-36), every ceiling still exceeded exactly as before, no new breach. Nothing else pins the old 3G bullets (grepped); `bin/check-links` exits 0 in both layouts. Not done, and recorded for him: the plan also names one phrase each in `HOW_TO_USE.md` (about line 765) and `README.md` (about line 428) and the worked transcript `docs/tutorials/T2_worked_transcript.md` (about line 266); the BOOTSTRAP Step 10 settings snippet from PR #96 is not on this branch.

### 2026-10-20 · [BL-79] S354 the two suites that pin the distributed-file count take the Phase 3G report tool (layer 1, second of two commits)

`tools/test_layout_resolver.py` types the new file into its section-4.1 list (`S41_FRAMEWORK`, 34 files to 35, with a comment that the BL-101 plan's own table is not amended: that plan is 59,994 B of a 60,000 B budget) and `tools/test_sync_layouts.py` moves its three counts, 30 to 31. Direct runs: `test_layout_resolver.py` 75 tests OK (2 s), `test_sync_layouts.py` 89 tests OK (59 s), `bin/check-layout-literals` 0 sites. Closes the red the previous checkpoint (`56bf6d1f`) left by construction. The full shell suite on this committed tree is the next step.

### 2026-10-20 · [BL-79] S354 [WIP] checkpoint -- the sync manifest and the dashboard learn the Phase 3G report tool (layer 1, first of two commits); the suite is red at this commit by construction

`bin/_manifest.py` gains the `TRACKED` row for `starter-kit/close_out_report.py` and its `NEW_LAYOUT` twin (`methodology/close_out_report.py`), appended after `quality_ratchet.py`. The dashboard (`tools/` and its `starter-kit/` twin, byte-identical, `DASHBOARD_VERSION` 2.22.0 to 2.23.0) gains the tool's installed-content entry: its own `__version__` pattern and four structural signatures, so a synced copy is not counted as the adopter's own source. `tools/test_methodology_dashboard.py` takes the checklist exemption, the population guard (7 to 8), the version pin, the fixture body and the destination count (30 to 31). Before these edits the dashboard suite read 6 failing methods (11 failure lines; S349 counted five on the PR branch, the fork has one more table test); after them it reads `397 tests, OK (skipped=4)`, 78 s. A checkpoint commit under the 5-file cap (`SAFEGUARDS.md` Blast Radius): the 7 files this layer touches would break it, so the two suites that pin the file count (`tools/test_layout_resolver.py`, `tools/test_sync_layouts.py`) follow in the next commit; the first `bin/tests.sh` run of this layer read 564 passed, 2 failed (those two suites, 5 assertions). Nothing pushed; nothing sent upstream.

### 2026-10-20 · [BL-79] S354 claim (in progress) -- distribute the close-out report tool through the sync manifest (fork `main` only); nothing sent upstream

Claimed at the operator's Phase 0 picker answer "Distribute via the manifest (Recommended)", after his correction that he thought the tool was already in the manifest (it is not: the plan's P3 had the row, and S349 left it out of PR #96 at his word "make this a small PR"). The trim (`43b38a91`) and its fold (`0df0fd9f`) came first, as S353 asked; the write step was run by him because the permission classifier held it. Phase 0: both ledger frontiers current, 0 undocumented commits, 0 merges, no pending receipt, `check-ledger` and `check-handoff` exit 0, dashboard 72/100 (medium, 0 high); #96, #94, #92 open and unanswered by the maintainer (0, 2, 2 comments), #93 (1) and #95 (0) open and unchanged, `upstream/main` `f34769f3`. Gate-run citation: the local results file is the Oct 10 one, so S353's cited 22-gate numbers were neither re-run nor contradicted. A read-only survey of the 13 sibling repositories that carry a runner (6 legacy layout, 7 under `methodology/`) found 8 with uncommitted changes and `nprcgenekeepr` with files changed in the last hour; nothing was written in any of them. Phase 3F records the rest.

### 2026-10-20 · [ad hoc] S354 -- the HANDOFFS trim's pointer block folded into the archive index (the trim itself is the tool's entry above it, commit `43b38a91`, ticked at the S354 Phase 0 picker and run by the operator)

The fold, in its own commit as the index's rule says: the pointer block left `HANDOFFS.md` (40,517 B to 40,061 B) and one row joined `docs/HANDOFFS_ARCHIVE_INDEX.md` (`| 1 | 2026-10-20 → 2026-10-20 | HANDOFFS-through-2026-10-20-4.md | v1.8.1 |`). Taken before the session claim, as S353's handoff asked. The trim kept 3 receipts (S353, S352, S351) and archived S350. Its dry run named the `-4` shard as predicted and took 8.0 s. The permission classifier held the write step in this session (reason given: irreversible local destruction), so the operator ran `--cut 3 --force --write` himself at the prompt; the shard's verify script exited 0 (L1, L2, L3) before and after the fold, and `check-handoff` and `check-ledger` exit 0. Nothing was sent upstream.

### 2026-10-20 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-20-4.md` (1 record(s), 51,390 B → 40,517 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-20 → 2026-10-20) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-20-4.md`](docs/archive/HANDOFFS-through-2026-10-20-4.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-20-4.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-20-4.md.verify.sh)
rather than trusting a digest printed here. Live file 51,390 B → 40,517 B (−21.2%).

### 2026-10-20 · [ad hoc] S353 -- push record: fork `main` to the fork `origin` at the operator's Phase 0 picker (`7cdb0753` to `e2871a35`), head read back

At the picker tick "Push main to the fork's origin at close-out", `git push origin main` (`https://github.com/rmsharp/methodology.git`, the fork) moved `main` from `7cdb0753` to `e2871a35` (7 commits: S352's push record `5944d779`, the `HANDOFFS.md` trim `8b640b0d` and its fold `0515b2a3`, the claim `16492595`, the BL-18 work `47e55d28`, the backlog close `62bf452e` and the close-out `e2871a35`; the picker text listed the push as the fork only, never upstream). Read back: `git ls-remote origin refs/heads/main` and the local `HEAD` both read `e2871a3557485f69e5ca7a6ea3e7548886a9173a` before this entry, and `git rev-list --count origin/main..HEAD` read 0. This push record is committed locally and not pushed, so `main` is one commit ahead of `origin` at rest. Nothing was sent to `KJ5HST/methodology` by this push.

### 2026-10-20 · [BL-18] S353 close-out -- BL-18 done (bin/check-handoff refuses a bare ledger line number in the newest receipt's key_files); the receipt complete; nothing sent upstream

The session's one deliverable, closed out: the work `47e55d28`, the backlog close `62bf452e`, the claim `16492595`, and before the claim the `HANDOFFS.md` trim `8b640b0d` and its fold `0515b2a3`, which the operator ticked at the Phase 0 picker. **Gate run:** `quality_ratchet.py --run` in a clean `--no-local` clone of `47e55d28`, taken after the claim with 4 receipts in the tree: `22/22 pass · 0 fail · 0 unmeasured · results dc315d2ed377 · manifest e7366a004f0a`, `tests-sh-passed` measured at 565. **Predecessor (3A):** S352's handoff scored 9 (every state, shard name, timing and file count it predicted held; missing: that the two older live receipts, S351 and S350, already carry the anchor, so a rule on every receipt would have turned the live ledger red at once, and that the review's anchor count of 113 had grown to 167). **Phase 3C:** no row appended to `docs/FORK_LEARNINGS.md`, so the retire-or-refuse rule (D3) was not triggered; rows considered: #56 (the exemption's lone case was weighed against the corpus: 7 receipts, none since 2026-09-16), #59, #61 and #74 (the review's carried count was re-derived, not quoted: 113 became 167), #73 (the Phase 0 report named the one write the dashboard run made); the mechanical lesson, that a rule scoped to the record being written is forward-only without a cutoff date, is Test 57, a test and not a row. The operator's third tick (push `main` to the fork's `origin`) follows this commit; its push record is its own entry.

### 2026-10-20 · [BL-18] S353 -- close BL-18 (`bin/check-handoff` refuses a bare ledger line number in the newest receipt's `key_files`)

The three-edit close: the index row left `docs/planning/BACKLOG.md` (open index rows 48 to 47), `BL-18` joined its completed-items id list between `BL-17` and `BL-20`, and its completed row joined `docs/planning/BACKLOG-COMPLETED.md` (commit `47e55d28` named in it). `BACKLOG-DETAIL.md` is untouched: a closed item's body stays there and its anchor still resolves. The three backlog proofs, `check-backlog-anchors`, `check-links` and `check-ledger` exit 0. The routing block's prose mentions of BL-18 (lines 34 and 92) stay as they were, because the detail proof pins that block byte for byte.

### 2026-10-20 · [BL-18] S353 work -- `bin/check-handoff` refuses a bare `CHANGELOG.md:N` or `HANDOFFS.md:N` in the NEWEST receipt's `key_files`, forward only; canonical-only, nothing sent upstream

The rule, approved at one picker with no exemption (the review's row 14 had exempted a receipt whose only `path:line` token is the anchor; the operator took the recommended option to drop it): `key_files_anchors()` reuses `LIVE_LEDGER_ANCHOR_RE` (prefix-aware, so `starter-kit/CHANGELOG.md:92` and a shard path stay legal) and is applied to the newest receipt only, in the everyday run and in `--all`, skipping a `status: pending` stub and skipping both modes under `--archived`. Forward-only is a property of scope, not of a date: an older receipt is never re-judged. The finding begins `key_files`, so Tests 25's and 33's counters cannot absorb it. The module docstring's 'Scope is `changelog_ref` ONLY' paragraph is rewritten with the rule and its two stated limits (a `./CHANGELOG.md:N` spelling passes, 0 occurrences; the other keys are not scanned, 17 newest receipts carried an anchor only there against 123 for `key_files`). **Measured before the design:** 167 bare anchors in `key_files` (165 in the 167 frozen shards, 2 in older live receipts; a plain `grep` gave the same 167, so the review's '113' was an earlier or differently scoped count); a replay of all 1288 committed versions of `HANDOFFS.md` found 123 of 386 receipts carried one while they were the newest, every session from S339 to S351 but S352, and 7 had the anchor as their only `path:line` token, none since 2026-09-16. **Verified:** Test 57 (22 assertions) written first, 9 of the first 21 red for the right reasons; the suite reads `565 passed, 0 failed, 0 skipped` (543 before; `tests-sh-passed` raised to 565, note `_s353_tightening_bl18`); a mutation round of 19 killed 19; a before/after replay of both tools over all 1288 versions: 1085 byte-identical, 203 differ by exactly the new block in both modes, the 123 receipts flagged equal an independent replay's set, and all 167 shards read byte-identically under `--archived`; `bin/check-layout-literals` reads 0 sites. Files: `bin/check-handoff` (64,873 B to 68,593 B), `bin/tests.sh`, `.quality-gates.json`. The gate run (`quality_ratchet.py --run`) and the backlog close follow.

### 2026-10-20 · [BL-18] S353 claim (in progress) -- a forward-only rule in `bin/check-handoff` against root-relative ledger anchors in a new receipt's `key_files`; nothing sent upstream

Claimed at the operator's Phase 0 picker answer "BL-18 (Recommended)", after the `HANDOFFS.md` trim (`8b640b0d`) and its fold (`0515b2a3`) he ticked at the same picker (his third tick, to push `main` to the fork's `origin` at close-out, is still owed). Phase 0: both ledger frontiers current, 0 undocumented commits, 0 merges, no pending receipt, `check-ledger` and `check-handoff` exit 0, dashboard 72/100 (medium, 0 high); #96, #94, #92 open and unanswered by the maintainer (0, 2, 2 comments), #93 (1) and #95 (0) open and unchanged, `upstream/main` `f34769f3`. Gate-run citation: the local results file is the Oct 10 one, so S352's cited 22-gate numbers were neither re-run nor contradicted. Phase 3F records the rest.

### 2026-10-20 · [ad hoc] S353 -- the HANDOFFS trim's pointer block folded into the archive index (the trim itself is the tool's entry below, commit `8b640b0d`, ticked at the S353 Phase 0 picker)

The fold, in its own commit as the index's rule says: the pointer block left `HANDOFFS.md` (40,053 B to 39,597 B) and one row joined `docs/HANDOFFS_ARCHIVE_INDEX.md` (`| 1 | 2026-10-20 → 2026-10-20 | HANDOFFS-through-2026-10-20-3.md | v1.8.1 |`). Taken before the session claim, as S352's handoff asked. The trim kept 3 receipts (S352, S351, S350) and archived S349; its dry run named the suffixed shard (`-3`, as predicted) because `HANDOFFS-through-2026-10-20.md` and `-2` were taken, took 7.1 s, and the shard's verify script exited 0 (L1, L2, L3) before the trim commit. Nothing was sent upstream.

### 2026-10-20 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-20-3.md` (1 record(s), 50,878 B → 40,053 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-20 → 2026-10-20) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-20-3.md`](docs/archive/HANDOFFS-through-2026-10-20-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-20-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-20-3.md.verify.sh)
rather than trusting a digest printed here. Live file 50,878 B → 40,053 B (−21.3%).

### 2026-10-20 · [ad hoc] S352 -- push record: fork `main` to the fork `origin` at the operator's close-out picker (`8229f6cd` to `7cdb0753`), head read back

At the picker answer "Push main to origin (Recommended)", `git push origin main` (`https://github.com/rmsharp/methodology.git`, the fork) moved `main` from `8229f6cd` to `7cdb0753` (5 commits: the Phase 0 push record `16e20201`, the claim `f6344b8c`, the work `918cce11`, the backlog close `8f5a5a4c` and the close-out `7cdb0753`). Read back: `git ls-remote origin refs/heads/main` and the local `HEAD` both read `7cdb07535d240f48367fb9b400c4d4c111960ee8` before this entry, and `git rev-list --count origin/main..HEAD` read 0. Nothing was sent to `KJ5HST/methodology` by this push. This entry is the one commit `main` stays ahead by.

### 2026-10-20 · [BL-89] S352 close-out -- BL-89 done (bin/check-handoff reads the ledger's structure in its everyday run); BL-73 and BL-16 folded in; the receipt complete; nothing sent upstream

Phase 3, in order. **3A:** S351's handoff scored **8** (re-read before scoring; every checked claim held: the `gh pr view` command and the state it expected for #96, #94, #92, #93 and #95; the trim offer with its suffixed shard name, dry-run time and four files; the BL-89-first ranking and the zsh warning; missing: it did not say the interaction review folds BL-73 and BL-16 into BL-89). **3B:** self-score **8**: the gap was measured on seven broken shapes, a prototype and a replay over 1,283 committed versions, 166 shards and 14 other ledgers before a plan was shown; tests first and red for the right reasons; a mutation round whose survivors became assertions; against a loose figure in the plan (a stray fence hid a receipt in 17 committed versions in one day, not 'about 20 commits'), a wrong size in the work's ledger entry (corrected here: `bin/check-handoff` is 64,873 B, not 64,831 B), a `git stash` while a background run read the tool, an unquoted zsh heredoc at close-out whose backticked `git stash` ran for real and stashed the uncommitted `CHANGELOG.md` and receipt (found from the errors; `CHANGELOG.md` restored from the stash after checking the tree matched it, stash dropped, nothing lost), and long silent stretches. **3C:** no row appended to `docs/FORK_LEARNINGS.md`, so the retire-or-refuse rule (D3) was not triggered; rows considered: #57, #33, #38, each already stating what this session confirmed; the mechanical lesson (a computed finding must be printed) is Test 56. **3D:** `HANDOFFS.md` S352 `pending` to `complete`. **3E:** the final tool on the live ledger (no flags and `--all`, exit 0), the 14 other ledgers, the 166 shards, the seed and the 1,283 versions; the 22-gate run in a clean `--no-local` clone of `918cce11` is cited in the receipt. Open for him: the three other projects' ledgers with real defects (`church_growth`, `mts-system`, `vscode_quarto_ext`; none edited), BL-123, and the calls S351 left. Memory notes updated. Whether `main` is pushed to the fork is the push-record entry's to say.

### 2026-10-20 · [BL-89] S352 -- close BL-89, and BL-73 and BL-16 with it (the interaction review folded both into BL-89); BL-18 no longer waits

The three-edit close for each: the row out of `docs/planning/BACKLOG.md`, the id into its completed-items list (in numeric order), the completed row into `docs/planning/BACKLOG-COMPLETED.md`; the detail bodies stay (`BACKLOG-DETAIL.md` is untouched, and the three completed rows link to nothing there that moved). Open index rows 51 to 48, completed rows 72 to 75 (`grep -oE '^\| \*\*BL-[0-9]+' docs/planning/BACKLOG.md | wc -l` and `grep -cE '^\| \*\*BL-[0-9]+\*\* \|' docs/planning/BACKLOG-COMPLETED.md`). The index's header sentence that BL-16 is the one open item with no heading of its own now says it closed. All three backlog proofs, `check-backlog-anchors`, `check-links` and `check-ledger` exit 0. The work is `918cce11`.

### 2026-10-20 · [BL-89] S352 -- `bin/check-handoff`'s everyday run reads the ledger's structure, so a hidden, doubled, duplicated or stranded receipt fails it (BL-89, BL-73, BL-16; fork only, canonical-only tool, nothing sent upstream)

**The problem, measured on the unchanged tool.** Seven broken `HANDOFFS.md` shapes built from BL-89's and BL-73's descriptions: the everyday run exited 0 on five (a claim stub spliced into the front matter's own code span, one session and date twice, an older receipt left pending, a receipt begun twice with nothing between the openers, a stray bare three-backtick line above the receipts) and `--all` on two (the bare doubled opener and the stray line, which silently skips the newest receipt: the file reads one receipt short and the next one is validated as the newest). The everyday run computed `scan()`'s structural findings and never printed them.

**The change** (`bin/check-handoff`, 60,049 B to 64,831 B; `bin/tests.sh`, `HANDOFFS.md` front matter one sentence, `.quality-gates.json`). (1) `scan()` accounts for every line-start `` ```handoff `` opener: it opens a receipt, or sits inside a wrapper of four or more backticks (the seed's documentation example, legal), or is a finding, in two new places: inside a receipt still open (BL-73: begun twice) and inside a three-backtick fence (what a stray bare fence does to the receipt below it). That is the per-opener reading of the backlog row's "block count that tolerates the format example", chosen because a bare count cannot tell the example from a hidden receipt. (2) The everyday run prints `scan()`'s findings and two ledger-wide checks lifted out of `validate_ledger()` into `ledger_structure_findings()` (an older receipt left pending, the newest receipt of another line excepted; one session and date twice), as their own block, "ledger-structure issue(s)"; `--all` calls the same function. The 13-key schema stays newest-only. (3) BL-16: `default_path()`'s docstring no longer says the repository has no root-level receipt ledger. Limit stated in the docstring: a stray fence of four or more backticks still hides what it wraps.

**Measured before the change was shown, on a prototype in a scratch copy, then again on the final tool.** This ledger's 1,283 committed versions of `HANDOFFS.md`: 22 newly flagged and every one real (in 21 the file held more receipts than the tool read: 17 committed versions on 2026-08-11 carry a stray fence that hid a receipt, and 4 carry a claim stub spliced into the front matter, at S196, S246, S252 and S267; the 22nd is a duplicate session beside a stale stub, `9cffac0b` of 2026-09-27); 191 failed before and after; the final tool and the prototype agree on every version (0 differences). The 166 archive shards: 0 changes. The 14 other projects' ledgers on this machine: 11 unchanged, 3 gain real findings (`church_growth` S4 twice on 2026-07-11; `mts-system` S195 begun twice and twice on one date; `vscode_quarto_ext` S284 stranded outside its fence with a hidden opener at line 705), none edited. `--all` prints the same error lines before and after the refactor on 350 files (24 fixtures, ledgers and the live one; 166 shards; a 160-version sample), apart from the two new rules.

**Tests.** `bin/tests.sh` Test 56 (20 assertions, each broken shape by exit code and message text, with line numbers; controls for a clean ledger, another line's newest pending receipt, a repeated id on a different date, a 4-backtick example and an indented quoted opener; `--all` and `--archived` read the same way), written first: 11 of the first 15 red against the unchanged tool. Test 34's row that pinned the gap ("default mode still green on a destroyed older receipt (documents the gap)") was flipped on purpose. Mutation round of 18: 13 killed at once, 4 survivors each exposed an assertion no test named (now added), 1 equivalent (`idx != 0` was redundant, removed); second round 17 of 17 live mutants killed. Whole suite `bash bin/tests.sh`: `543 passed, 0 failed, 0 skipped` (406 s) against `523 passed` at the claim commit; `tests-sh-passed` tightened 523 to 543 (note `_s352_tightening_bl89`); `quality_ratchet.py --precommit` accepts it; `bin/check-layout-literals` exit 0.

**Adopter impact:** none, the checker is canonical-only (not in `bin/_manifest.py`). **Candidate branch:** the pull-request candidate carries upstream's checker plus layout hunks only, so this change is not on it and nothing was ported. Backlog close and the receipt follow in their own commits.

### 2026-10-20 · [BL-89] S352 claim (in progress) -- make `bin/check-handoff` catch a structurally broken `HANDOFFS.md` in its default run; nothing sent upstream

Claimed at the operator's Phase 0 picker answer "BL-89 (Recommended)", after the `HANDOFFS.md` trim (`40321173`), its fold (`8229f6cd`) and the push of `main` to the fork's `origin` (both ticked at the same picker; push record `16e20201`). Phase 0: both ledger frontiers current, 0 undocumented commits, 0 merges, no pending receipt, `check-ledger` and `check-handoff` exit 0, dashboard 72/100 (medium, 0 high); #96, #94, #92 open and unanswered by the maintainer, #93 and #95 unchanged, `upstream/main` `f34769f3`. Gate-run citation: the local results file is the Oct 10 one (18 gates, manifest `c7eae109fc87`) and `--status` says the manifest has changed since, so S351's cited 22-gate numbers were neither re-run nor contradicted. Phase 3F records the rest.

### 2026-10-20 · [ad hoc] S352 -- push record: fork `main` to the fork `origin` at the operator's Phase 0 picker (`3d9975cd` to `8229f6cd`), head read back

At the picker answer "Push fork main", `git push origin main` (`https://github.com/rmsharp/methodology.git`, the fork) moved `main` from `3d9975cd` to `8229f6cd` (3 commits: S351's push record `e6efb052`, the `HANDOFFS.md` trim `40321173` and its fold `8229f6cd`). Read back: `git ls-remote origin refs/heads/main` and the local `HEAD` both read `8229f6cde1321c6ee20096653134517f2f524f66` before this entry, and `git rev-list --count origin/main..HEAD` read 0. Nothing was sent to `KJ5HST/methodology` by this push.

### 2026-10-20 · [ad hoc] S352 -- the HANDOFFS trim's pointer block folded into the archive index (the trim itself is the tool's entry below, commit `40321173`, ticked at the S352 Phase 0 picker)

The fold, in its own commit as the index's rule says: the pointer block left `HANDOFFS.md` (39,665 B to 39,209 B) and one row joined `docs/HANDOFFS_ARCHIVE_INDEX.md` (`| 1 | 2026-10-20 → 2026-10-20 | HANDOFFS-through-2026-10-20-2.md | v1.8.1 |`). Taken before the session claim, as S351's handoff asked. The trim kept 3 receipts (S351, S350, S349) and archived S348; its dry run named the suffixed shard (`-2`) because `HANDOFFS-through-2026-10-20.md` was taken, and the shard's verify script exited 0 before the trim commit. Nothing was sent upstream.

### 2026-10-20 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-20-2.md` (1 record(s), 50,290 B → 39,665 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-20 → 2026-10-20) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-20-2.md`](docs/archive/HANDOFFS-through-2026-10-20-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-20-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-20-2.md.verify.sh)
rather than trusting a digest printed here. Live file 50,290 B → 39,665 B (−21.1%).

