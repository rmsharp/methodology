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

**Archived 101 record(s), 2026-10-20 → 2026-10-23** into [`docs/archive/CHANGELOG-through-2026-10-23.md`](docs/archive/CHANGELOG-through-2026-10-23.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-10-23.md.verify.sh`](docs/archive/CHANGELOG-through-2026-10-23.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.8.1.

**Archived 76 record(s), 2026-10-23 → 2026-10-27** into [`docs/archive/CHANGELOG-through-2026-10-27.md`](docs/archive/CHANGELOG-through-2026-10-27.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-10-27.md.verify.sh`](docs/archive/CHANGELOG-through-2026-10-27.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.8.1.

**Archived 63 record(s), 2026-10-27 → 2026-10-28** into [`docs/archive/CHANGELOG-through-2026-10-28.md`](docs/archive/CHANGELOG-through-2026-10-28.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-10-28.md.verify.sh`](docs/archive/CHANGELOG-through-2026-10-28.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.8.1.

---

## 2026-09

## 2026-10

### 2026-10-30 · [ad hoc] S405 fix -- `bin/tests.sh` Test 34's two status-keyed mutations accept a `reconciled` anchor receipt (my Phase 0 reconcile of S404 turned two assertions red); fork only, nothing sent

**What broke and why.** The first full gate run after the work commits (21:47:20 to 22:13:59, `HEAD` `d82490ce6f92`, clean tree) read `22/24 pass · 2 fail`: `tests-sh-passed` 692 against its floor 694 and `tests-sh-failed` 2 against 0 (expectation E6, 24/24, was wrong). A direct `bash bin/tests.sh > file` (22:14:18 to 22:23:39, exit 1, `== Summary: 692 passed, 2 failed, 0 skipped ==`) named them: Test 34 `key-order mutation was vacuous` and `older-pending mutation was vacuous`. Test 34 reads two older receipts from the live ledger at run time (A1 is the second newest) and mutates `status: complete`; my Phase 0 reconcile (`d445cef6`) had made the S404 receipt `status: reconciled` (a closed state the runner defines for a receipt a later session reconstructs), and S404 is now A1, so both patterns matched nothing. The test had assumed every closed receipt says `complete`. **The fix** (`bin/tests.sh`, two regexes, no assertion added or removed): the key-order mutation matches `status: (?:complete|reconciled)` and carries the status line it found into the moved position; the older-pending mutation matches the same pair. **Checked before the edit (E7):** on the live ledger (A1 = S404) the old patterns change nothing and the new ones do; and through the test's own `mutate` helper both mutants are built and `check-handoff --all --allow-pending` rejects each, while the unmutated ledger passes (exit 0). **Left:** the `reconciled` path is exercised by the live ledger only while a `reconciled` receipt sits at A1 or A2; when S404 rotates out, no fixture holds it (a gap, not a defect of the fix). The full suite and the gates run again on this commit.

### 2026-10-30 · [ad hoc] S405 work (2 of 2) -- the drafted comment on upstream issue #95 is refreshed against the fix S404 built, and its record says what each new statement rests on; BL-114's row points at it; NOT POSTED; fork only, nothing sent

`docs/planning/pr-composition-evidence/i95-comment-draft.md` (3,515 B to 4,658 B): the opening says the four files are unchanged on `main` today and that the change is built; item 1's closing lean ('I lean towards the first') became what was built, a placeholder purpose as a `warn` that keeps its size and skips the 800 floor, with the 799/800 behaviour after the placeholder is replaced and the choice between `warn` and 'unmeasured' left to the maintainer; the closing offer now describes the two commits (the tool and its tests, then the seeds, the config line and the day-zero test; the order is the reverse of the S329 draft because Test 35 asserts the warning the tool commit adds) and says the change was run on 'my own copy', not on his `main`. Items 2 and 3 and the repro block are untouched (their evidence stands: the upstream blobs are unchanged). A scan of the text for session numbers, backlog codes, 'fork', 'Learning', planning paths and adopter names found none. `i95-comment-record.md`: a refresh paragraph, six new rows in §1 (each with the file it rests on), §2's side reading corrected (the over-cap line counts moved; the totals did not), §3's items 1 and 2 reworded (the offer; the design choice, no longer a lean), §4 (the change has not been applied to upstream's `main`). `BACKLOG.md` BL-114's row: 'refreshed S405'. `check-backlog-anchors`, the DETAIL and COMPLETED proofs, `check-links` and `check-learnings` each exit 0. The comment is shown to him inline in the S405 report; posting it, pushing a branch to the fork and opening a pull request are his explicit go-aheads and none was given.

### 2026-10-30 · [ad hoc] S405 work (1 of 2) -- the evidence under the refreshed #95 comment: `i95-comment-refresh.py` with its saved output, and the adopters measurement run again; fork only, nothing sent

Three new files in `docs/planning/pr-composition-evidence/`. `i95-comment-refresh.py` (run from the repository root: `python3 -I docs/planning/pr-composition-evidence/i95-comment-refresh.py SCRATCH`) builds eight git-initialised cases and parses the tool's own `--status --json` for each: upstream's blobs at the pinned `f34769f` (`up-notes` exit 2, over=1, kinds `instrument,line_bytes`; `up-template` exit 2, over=1, kind `protected`), this tree's seeds and tool (`fork-notes` exit 1, over=0; `fork-template` exit 1, over=0, kind `placeholder`), a real `bin/sync --layout legacy` into an empty project with the template as `CLAUDE.md` (`fork-day-zero` exit 1, over=0, `CLAUDE.md=warn`, `SESSION_NOTES.md=ok`), and the floor on this tree's tool (`floor-799` exit 2, `protected`; `floor-800` exit 1, none; `floor-cjk-300`, 900 bytes, exit 1, none). Written expectations E1 (day zero exits 1 with the warning), E2 (upstream's two cases exit 2), E3 (the four upstream seed files unchanged since `f34769f`: `git diff` 0 lines) and E5 (799 over, 800 and 300 CJK characters pass) all confirmed, by hand first and then by the script; E4 (the adopter totals unchanged) confirmed by `i95-comment-adopters-output-2.txt`: 10 of 12 declare the cap, 0 lines flip, `measure_file` agrees on every file, though the per-file counts moved (two projects 64 and 44 lines over, one 7, two 1). The draft and its record are the next commit.

### 2026-10-30 · [ad hoc] S405 claim (in progress) -- refresh the drafted comment on upstream issue #95 (BL-114 route R1) against the fix S404 built; shown inline, nothing posted; fork only

Claimed at his Phase 0 picker: 'Draft the #95 comment (Recommended)' (the other options were the #99 wording note, a read-only adopter-ledger report, and closing out with no deliverable); with it 'Yes, trim now (Recommended)' (done first, as its own action: trim `f0bbf8e2`, fold `S405 fold`) and 'Yes, push main (Recommended)' (after close-out). Phase 0 found S404's receipt still `status: pending` (work and gates complete, close-out never written) and reconciled it in `d445cef6`; 0 undocumented commits, 0 merges. Premise found at the claim: the picker said 'I would write the text', but `docs/planning/pr-composition-evidence/i95-comment-draft.md` and `i95-comment-record.md` already exist (S329, against upstream `f34769f`, the BL-114 row says 'drafted, not posted'), so the work is a refresh against the built fix, not a first draft. Governing document: `ITERATIVE_METHODOLOGY.md` phases 1 to 6 (no workstream covers drafting outward text). Scope boundary: the draft and its record only; posting a comment, pushing a branch to the fork and opening a pull request are his explicit go-aheads and are not part of this session. `CHANGELOG: pending` until close-out.

### 2026-10-30 · [ad hoc] S405 fold -- the trim's pointer block leaves `HANDOFFS.md` and one row joins `docs/HANDOFFS_ARCHIVE_INDEX.md`

The block (4 lines) became the row `| 2 | 2026-10-30 → 2026-10-30 | HANDOFFS-through-2026-10-30-2.md | v1.8.1 |`. Own commit, as the index's rule says (fork Learning #58). It follows the trim `f0bbf8e2` (five receipts to three, S400 and S401 archived; the shard has a `-2` suffix because `HANDOFFS-through-2026-10-30.md` was taken; its proof `bash docs/archive/HANDOFFS-through-2026-10-30-2.md.verify.sh` exit 0 before and after that commit and after this fold), taken at his required Yes/No 'Yes, trim now (Recommended)' at the S405 Phase 0 picker. Local only; nothing sent to `KJ5HST/methodology`.

### 2026-10-30 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-30-2.md` (2 record(s), 52,819 B → 32,951 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-10-30 → 2026-10-30) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-30-2.md`](docs/archive/HANDOFFS-through-2026-10-30-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-30-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-30-2.md.verify.sh)
rather than trusting a digest printed here. Live file 52,819 B → 32,951 B (−37.6%).

### 2026-10-30 · [ad hoc] Backfilled (reconcile-on-read): S404's `HANDOFFS.md` receipt -- built and gated, never closed out; now `status: reconciled`; fork only, nothing sent to KJ5HST/methodology

S405's Phase 0 found S404's receipt still `status: pending` after S404's work commit `90493814` (the claim `a9b3f063`, the two fix commits `cadb4780` and `19a4ecb8`): no close-out commit, no close-out ledger entry, no push. The ledger itself had no gap (`check-ledger` exit 0; the frontier `90493814` is the newest commit; 0 merges since). The receipt is rewritten from `git log`, the three S404 work entries and the gate results file (24 of 24 on `HEAD` `90493814`, results `0d2914e1e18a`, manifest `1d7041808739`), marked `reconciled` with S405's reading of the scores, and lists what was never done: Phase 3A to 3G, the 3C decision, the push. No code or configuration changed.

### 2026-10-30 · [ad hoc] S404 work (additional, after 1 of 2 and 2 of 2) -- BL-114's backlog row and detail say the fork side is built; the `tests-sh-passed` floor rises 692 to 694 and `context-budget-unit-tests` 163 to 174 (tightening only)

Measured first: `bash bin/tests.sh` in a clean `--no-local` clone at `19a4ecb8` (after both work commits), 18:11:55 to 18:23:04 (11 min 9 s; load 8.46 at the start): `== Summary: 694 passed, 0 failed, 0 skipped ==`, exit 0, so the two new Test 35 assertions are the whole +2 and no existing test went red (expectation E4); `tools/test_context_budget.py` runs 174 tests OK. `.quality-gates.json` gets exactly those two numbers. `docs/planning/BACKLOG.md` BL-114's index row now leads with the fork side DONE (S404, the two commits, nothing sent) and what stays his (the route to upstream, R1 to R4, and the new-layout day-zero case); `docs/planning/BACKLOG-DETAIL.md` gets an S404 paragraph in BL-114's section: the design choice taken (A), what each commit changed, the measured results (174 tests, 6 of 6 mutants, `--selftest` exit 0, the adopters re-run: 10 of 12 declare the cap and 0 lines flip), that BL-84 (the 24,000 B warn line) is untouched, and that a fix on upstream's tip would meet the `VERSION` line. `bash docs/planning/BACKLOG-COMPLETED.md.verify.sh`, `bash docs/planning/BACKLOG-DETAIL.md.verify.sh` and `bin/check-backlog-anchors` each exit 0 from the repository root. Expectation E5 held: this repository's own `context_budget.py --status` reads the same rows and figures (`FORK_LEARNINGS.md` 119,936 B, `SESSION_RUNNER.md` 55,578 B, `SAFEGUARDS.md` 16,919 B, the read-set total 72,497 B over; exit 2), because its config declares neither `max_line_bytes` nor a fence.

### 2026-10-30 · [ad hoc] S404 work (2 of 2) -- the seeds: `starter-kit/SESSION_NOTES.md` and `CLAUDE_TEMPLATE.md` pass the seed `.context-budget.json`, and `bin/tests.sh` Test 35 holds a day-zero pass-control (upstream issue #95); fork only, nothing sent

`starter-kit/SESSION_NOTES.md`: line 5 (321 B against a 280 B cap) is three lines at sentence boundaries (a markdown paragraph, so it renders the same), and a `## Session History` heading sits above the italic history marker, which makes the seed config's `^## ` check see two headings of the two it expects; 27 to 31 lines, 1,093 B to 1,113 B. `starter-kit/CLAUDE_TEMPLATE.md`: the `## Purpose` placeholder sits between `<!-- budget:protected -->` and `<!-- /budget:protected -->`, the customise comment above it now says to keep the paragraph between the markers (3,350 B to 3,438 B). `bin/tests.sh` Test 35: `bin/sync --layout legacy` into an empty git project, the template copied to `CLAUDE.md`, then the tool's own `--status --json` parsed: no row over and the one finding is the placeholder warning (the tool exits 1, not 0: a fresh project has no `LEARNINGS.md` and no canonical checkout, so those rows read unmeasured), with a paired control in which a 400-byte line in `SESSION_NOTES.md` must be seen as a breach; run as a block it passes on this tree and fails on `cadb4780` (exit 2, `over=2 kinds=instrument,line_bytes,protected`). `tools/test_context_budget.py`: the 3 tests held out of commit 1 (the seed `SESSION_NOTES.md` passes its row; the template is a placeholder warning, never over; the config's `protected_placeholder` is the text in the template) are back, 174 tests, OK. **Left stale on purpose:** two comments say the seed is a '27-line stub' (`tools/methodology_dashboard.py` near `FRAMEWORK_ITEMS` and `tools/test_methodology_dashboard.py`'s `test_no_framework_item_is_a_distribution_seed` docstring); nothing keys on the number and both are descriptive, so they are not touched in this commit (a hand-kept count; flagged in the handoff).

### 2026-10-30 · [ad hoc] S404 work (1 of 2) -- `context_budget.py` 1.4.1: the per-line cap and the purpose-block floor count bytes, and a purpose block that still holds the template placeholder is a warning, not "emptied" (upstream issue #95); fork only, nothing sent

At his Present-gate answer 'Approve, A: placeholder = warning (Recommended)'. `starter-kit/context_budget.py`: `measure_file` measures `max_line_bytes` with `len(l.encode())` (was `len(l)`) and the `protected_min_bytes` floor with `len(body.strip().encode())` (was `len(body.strip())`), so the "B" printed beside each is bytes, as the file size beside them already was; a row that names `protected_placeholder` and whose fence body contains that text gets a `placeholder` finding and status `warn` (raised only from `ok`; a worse status stays), with its own remedy ('Write your purpose'), and a row without the key is judged exactly as before. `starter-kit/context-budget.json`: the `CLAUDE.md` row names `<project-name>`, the text `CLAUDE_TEMPLATE.md` already carries, plus a `_protected_placeholder` note. `tools/test_context_budget.py`: 8 of the 11 tests of `TestAFreshProjectPassesItsOwnBudget` (163 to 171 here; the other 3 need the seeds and ride commit 2), seen red on 1.4.0 first (7 failing, 4 passing: the fixture and three controls) and green after; a mutation round of 6 mutants (warn lowers an over row, the floor and the cap back to characters, the key alone triggering the warning, the floor still applying after the warning, the warning reusing the `protected` kind) all killed by the intended test; `--selftest` exit 0. Expectations E2, E5 and E7 of `s404-expectations.txt` (scratchpad, not committed) so far hold. The seeds and the shell pass-control are commit 2.

### 2026-10-30 · [ad hoc] S404 claim (in progress) -- BL-114: make a fresh `bin/sync` pass its own `.context-budget.json` (upstream issue #95's four findings plus the fixed-placeholder gap); fork-only, nothing sent

Claimed at his Phase 0 picker: 'BL-114: fix fresh-sync failure (Recommended)' (the other options were the #99 file-count note, a read-only report on three adopter ledgers, and closing out with no deliverable). Phase 0 found nothing to reconcile (0 undocumented commits, 0 merges, no pending receipt; `1bc80b05` is S403's ledger-only push record) and the premise unchanged: the four seed files (`starter-kit/context_budget.py`, `SESSION_NOTES.md`, `CLAUDE_TEMPLATE.md`, `context-budget.json`) are identical on `upstream/main` `d50ce290` to what they were at `f34769f`, where `i95-record.md` measured them, and the fork's `context_budget.py` (1.4.0) still compares the fence floor in characters (`:546`, `:548`). Governing document: `workstreams/DEVELOPMENT_WORKSTREAM.md`, with a Present gate before any edit. Scope boundary, from `docs/planning/pr-composition-evidence/i95-record.md` §1 and §6: the legacy-layout fresh project only; the new-layout day-zero case (§3.3) and the route to upstream (a comment, a pull request of its own, or neither: R1 to R4) are his calls and are not part of this session. `CHANGELOG: pending` until close-out.

### 2026-10-30 · [ad hoc] S403 push record -- fork `main` fast-forwarded `5933b140..0ab907a3` (5 commits); fork `origin` only, nothing sent to `KJ5HST/methodology`

At his 'Yes, push main to the fork's origin (Recommended)'. Guarded first: `origin` is `https://github.com/rmsharp/methodology.git`, its `main` was still `5933b140` and an ancestor of local `main`, five commits ahead (the S403 trim `99121212`, fold `e84a0bd0`, claim `79372223`, work `5e7065dd` and close-out `0ab907a3`). `git push origin main:main` only (never `--all` or `--mirror`); afterwards `origin/main` = `main` = `0ab907a3`, 0 ahead. The close-out commit was amended once before the push (unpushed, `--no-verify`, the ledger and receipt unchanged apart from one number) to correct the receipt's next_steps (6), which said the guarded count would be 6; it was 5. This entry's own commit goes to `origin` under his standing grant for ledger-only push records. `upstream`, #99, #98 and #96 untouched.

### 2026-10-30 · [ad hoc] S403 close-out -- `CLAUDE.md` is under its 18,600 B ceiling (18,598 B) and `overhead-ratchet-plan.md:57` no longer says P5 is owed; the fork's gates pass 24 of 24; `HANDOFFS.md` trimmed 5 to 3 receipts and folded

The `HANDOFFS.md` receipt for S403 is complete (self-score 8; S402 scored 9 by this session). One deliverable, from his Phase 0 pick 'options 1 and 2' read as one (the same stale budget text in two live documents): the work commit is `5e7065dd` (claim `79372223`); the trim `99121212` and fold `e84a0bd0` came first at his required Yes/No 'Yes, trim now (Recommended)'. `CLAUDE.md` 18,648 B to 18,598 B (a stale test count, a stale line pointer and a history parenthetical out); the plan's decision row S4 now says `.context-budget.json` 'says so too'. The fork's gates, one run on `HEAD` `5e7065dd4057` with a clean tree after all work commits, 16:41:38 to 17:06:20: quality_ratchet: 24/24 pass, 0 fail, 0 unmeasured, results `32858fe46628`, manifest `102234f3acf8` (`tests-sh-passed` 692 against its floor 692). `HANDOFFS.md` now holds FOUR receipts, so no trim is due at S404's Phase 0 and one is due after S405's. `CHANGELOG.md` is under its 196,608 B trigger. No row appended to `docs/FORK_LEARNINGS.md`, so D3's duty does not fire. Fork `main` push: at his 'Yes, push main to the fork's origin (Recommended)'; the push record is the next entry. Local to the fork; nothing sent to `KJ5HST/methodology`.

### 2026-10-30 · [ad hoc] S403 work -- `CLAUDE.md` loses a stale test count, a stale line pointer and a history parenthetical (18,648 B to 18,598 B), and `overhead-ratchet-plan.md:57` loses the stale P5 clause; five expectations, all confirmed

`CLAUDE.md` (three deletions, one occurrence each): `, 218 tests` from the trimmer's suite row (11 B; `python3 -m unittest -q tools.test_methodology_trim` runs 222 tests, OK, skipped=2; the 218 was copied from the layer-3 record of an upstream PR and has been wrong since the suite grew), ` (`:34`)` after `sys.dont_write_bytecode` in the same row (8 B; the statement is at `tools/test_methodology_trim.py:36`, so the pointer had already drifted by 2), and ` (it read 4 at the start of P6)` from the layout row (31 B; history the layout plan carries). 50 B in all: 18,648 B to 18,598 B, 157 lines before and after, under its 18,600 B ceiling by 2 B, so the next edit that adds a byte puts it over again. `docs/planning/overhead-ratchet-plan.md:57` (decision row S4, one line): `.context-budget.json` "still calls the figure a warning until BL-53's P5 rewrites it" became `.context-budget.json` "says so too (BL-53's P5 rewrote its entry)", which `.context-budget.json:92` ("IT IS A REPORTED SERIES, NOT A LIMIT") bears out. Expectations (`s403-expectations.txt`, written before either edit), scored by measurement: E1 (92%) 18,598 B and 157 lines, confirmed; E2 (90%) `context_budget.py --status` still exits 2, the `CLAUDE.md` row reads `warn` and the resident-total row is gone from the table, the read-set total stays 72,497 B and `FORK_LEARNINGS.md`, `SESSION_RUNNER.md` and `SAFEGUARDS.md` stay over, confirmed (the `HANDOFFS.md` row also fell from over to `warn`, which is the trim's doing, not this edit); E3 (95%) the plan diff is one line, confirmed; E4 (88%) the five checkers exit 0, confirmed (the 24-gate run is in the close-out); E5 (85%) a repository-wide search for the three deleted phrases finds only dated records (ledgers, receipts, archived shards, `BACKLOG-DETAIL.md:1654`, and the layer-3 evidence files, where 218 was true), confirmed. Left alone on purpose: those dated records (FM #17), and the `:25` pointer in the dashboard suite's row, which is still correct. Local only; nothing sent to `KJ5HST/methodology`.

### 2026-10-30 · [ad hoc] S403 claim (in progress) -- remove the stale budget text from `CLAUDE.md` (under its 18,600 B ceiling) and from `docs/planning/overhead-ratchet-plan.md:57`; local only

Claimed at his Phase 0 picker: 'options 1 and 2' of 'Clear CLAUDE.md's 48 B overage (Recommended)', 'Fix the same stale clause in overhead-ratchet-plan.md:57', 'Decide #99's 52 files wording' and 'Something else', read as one deliverable (the same defect, a stale statement about the context budget, in two live documents); and 'Yes, trim now (Recommended)' as the required Yes/No for `HANDOFFS.md` (five receipts, over the rule's four), which is why the trim `99121212` (S398 and S399 archived to `docs/archive/HANDOFFS-through-2026-10-30.md`, 59,198 B to 36,744 B, proof exit 0 before and after the commit) and the fold `e84a0bd0` came first. Plan: (1) `CLAUDE.md`: delete hand-kept counts and history from the tool rows until it is at or under 18,600 B, measured, not counted; known first: `:112` says '218 tests' and `python3 -m unittest -q tools.test_methodology_trim` runs 222 (OK, skipped=2); `:115` has '(it read 4 at the start of P6)'. (2) `overhead-ratchet-plan.md:57`: replace the stale clause with a true one. Expectations are written before either edit. `context_budget.py --status` will still exit 2 afterwards (the read-set total, `FORK_LEARNINGS.md`, `SESSION_RUNNER.md` and `SAFEGUARDS.md` stay over); only the `CLAUDE.md` and resident-total rows can clear. Phase 0 (read 2026-10-30 at 16:34, `uptime` load 8.84): the `CHANGELOG.md` frontier = `HEAD` `5933b140` (0 undocumented, 0 merges); the `HANDOFFS.md` frontier `5ebb43d2` is one commit behind (S402's ledger-only push record, not a session), no pending receipt; `check-ledger` and `check-handoff` exit 0; the newest receipt's gate citation (results `32858fe46628`, manifest `102234f3acf8`) equals `quality_ratchet.py --status` (gates not re-run); `upstream/main` unchanged `d50ce290` (fetched); `pr5-step2-readback.sh` exit 0, 'READ-BACK OK (0 failed)'; #99 and #98 open, MERGEABLE, CLEAN, #96 open, CONFLICTING, each 0 comments, 0 reviews; issues #93, #95, #97 quiet since 10-24; dashboard 72/100, 0 high-risk flags (its history line rides this claim); local `main` = `origin/main` `5933b140` before the trim. Local only; nothing sent to `KJ5HST/methodology`.

### 2026-10-30 · [ad hoc] S403 fold -- the trim's pointer block leaves `HANDOFFS.md` and one row joins `docs/HANDOFFS_ARCHIVE_INDEX.md`

The block (4 lines) became the row `| 2 | 2026-10-29 → 2026-10-30 | HANDOFFS-through-2026-10-30.md | v1.8.1 |`. Own commit, as the index's rule says (fork Learning #58). It follows the trim `99121212` (five receipts to three, S398 and S399 archived; its proof `bash docs/archive/HANDOFFS-through-2026-10-30.md.verify.sh` exit 0 before and after that commit and after this fold), taken at his required Yes/No 'Yes, trim now (Recommended)' at the S403 Phase 0 picker. Local only; nothing sent to `KJ5HST/methodology`.

### 2026-10-30 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-30.md` (2 record(s), 59,198 B → 36,744 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-10-29 → 2026-10-30) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-30.md`](docs/archive/HANDOFFS-through-2026-10-30.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-30.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-30.md.verify.sh)
rather than trusting a digest printed here. Live file 59,198 B → 36,744 B (−37.9%).

### 2026-10-30 · [ad hoc] S402 push record -- fork `main` fast-forwarded `e79af8c9..5ebb43d2` (3 commits); fork `origin` only, nothing sent to `KJ5HST/methodology`

Pushed `main` only (never `--all` or `--mirror`) to `https://github.com/rmsharp/methodology.git` at his 'Yes, push main to the fork's origin (Recommended)'. Guard before the push: `git ls-remote origin refs/heads/main` = `e79af8c9`, an ancestor of local `main`, `git rev-list --count` = 3 (the claim `f8ca7a78`, the work `b33b2546`, the close-out `5ebb43d2`). Read-back after: `git ls-remote origin refs/heads/main` = `5ebb43d2` = local `main`. This entry is a ledger-only commit that goes to `origin` under his standing grant; if `git rev-list --count origin/main..main` is not 0, that commit was not pushed.

### 2026-10-30 · [ad hoc] S402 close-out -- `CLAUDE.md:57` no longer says `.context-budget.json` "still calls the figure a warning until the plan's P5 rewrites it" (P5 was done the day it was written); the fork's gates pass 24 of 24

The S402 deliverable is done: the work commit is `b33b2546` (claim `f8ca7a78`). Gates (3E): one run on `HEAD` `b33b25462658` with a clean tree, 16:03:43 to 16:30:32 (26 min 49 s; load 10.95 at the start). It waited for another project's test workers to stop holding the machine (load 174 after the work commit, 322 at 15:49, 11.85 when he said 'look at load now'): quality_ratchet: 24/24 pass · 0 fail · 0 unmeasured · results 32858fe46628 · manifest 102234f3acf8 (equal to S401's citation), which scores the work entry's E3 as confirmed. Receipt: S402 `complete`, self-score 8; S401 (predecessor) scored 9. Learnings (3C): no row appended to `docs/FORK_LEARNINGS.md`, so D3's duty does not fire. `HANDOFFS.md` now holds FIVE receipts, so a trim is due after S403's Phase 0 report. One correction to the claim entry below, which stands as written: its phrase 'only dated records that say P5 was owed' was too broad; of the hits, only `docs/planning/BACKLOG-DETAIL.md:1654` is this plan's P5, and the other two (`BACKLOG-DETAIL.md:2437`, `findings.md:96`) are other plans' phases. He said 'Yes, push main to the fork's origin (Recommended)'; the push is recorded in the 'S402 push record' entry. Nothing sent to `KJ5HST/methodology`.

### 2026-10-30 · [ad hoc] S402 work -- `CLAUDE.md:57` loses the sentence that said `.context-budget.json` "still calls the figure a warning until the plan's P5 rewrites it"; one file, 89 B shorter

Deleted the clause ` `.context-budget.json` still calls the figure a warning until the plan's P5 rewrites it.` (89 B, one occurrence); the line now ends at "stays.", and the file is 157 lines before and after. `CLAUDE.md` 18,737 B to 18,648 B. The sentence before it, which stays, already says the ceiling is a reported series. Expectations written before the edit, scored: E1 (83 B, 18,654 B, 157 lines) **wrong on the figure** (I counted by eye; measured 89 B and 18,648 B; the one-occurrence and unchanged-line-count parts held); E2 (`context_budget.py --status` still exits 2) confirmed: `CLAUDE.md` is over its 18,600 B ceiling by 48 B (≈7,132 tokens against 7,114), down from 137 B, and this edit does not fix that overage (it has stood since 2026-10-08, the file's last change, and no backlog row records it); E4 (the clause gone from `CLAUDE.md`) confirmed; E3 (`bin/tests.sh` and the ratchet unchanged) is scored at close-out, after the gates run. A search after the edit finds the same clause in `docs/planning/overhead-ratchet-plan.md:57`, a decision row dated S202; left as written, because this session's deliverable is `CLAUDE.md` alone. `check-ledger` and `check-handoff --allow-pending` exit 0. Local only; nothing sent to `KJ5HST/methodology`.

### 2026-10-30 · [ad hoc] S402 claim (in progress) -- correct the stale sentence at `CLAUDE.md:57` (`.context-budget.json` "still calls the figure a warning until the plan's P5 rewrites it"); local only

Claimed at his Phase 0 picker: 'Fix stale CLAUDE.md line 57 (Recommended)' (the others offered were a drafted-not-posted note on #99 about the squash count, and no deliverable). The finding, made in Phase 0 and checked before the claim: the sentence was true when `24fe658b` (BL-53 P4, 2026-09-20) wrote it and stopped being true the same day at `9db2c181` (BL-53 P5), which rewrote the `FORK_LEARNINGS.md` entry in `.context-budget.json` to read 'IT IS A REPORTED SERIES, NOT A LIMIT' (now `:92`); the plan's §P5 says DONE. Nothing else pins the sentence (a repository-wide search finds only dated records that say P5 was owed, left standing as written). Plan: delete the sentence rather than reword it, because the sentence before it already says the ceiling is a reported series, and `CLAUDE.md` is 18,737 B against its 18,600 B ceiling (`context_budget.py --status` exits 2; reported, not gated), so the edit must not grow it. Phase 0 (read 2026-10-30 at 15:05, `uptime` load 17.94): the `CHANGELOG.md` frontier = `HEAD` `e79af8c9` (0 undocumented, 0 merges); the `HANDOFFS.md` frontier `5ae58a79` is one commit behind (S401's ledger-only push record, not a session), no pending receipt; `check-ledger` and `check-handoff` exit 0; the newest receipt's gate citation (results `32858fe46628`, manifest `102234f3acf8`) equals `.quality-gates-results.json` (gates not re-run); `upstream/main` unchanged `d50ce290` (fetched); `pr5-step2-readback.sh` exit 0, 'READ-BACK OK (0 failed)'; #99 and #98 open, MERGEABLE, CLEAN, #96 open, CONFLICTING, each 0 comments, 0 reviews; issues #93, #95, #97 quiet since 10-24; dashboard 72/100, 0 high-risk flags (its history line rides this claim); `HANDOFFS.md` holds 4 receipts (49,357 B) and `CHANGELOG.md` 114,682 B, so no trim is due; local `main` = `origin/main` `e79af8c9`. Local only; nothing sent to `KJ5HST/methodology`.

### 2026-10-30 · [ad hoc] S401 push record -- fork `main` fast-forwarded `6d5757e2..5ae58a79` (6 commits); fork `origin` only, nothing sent to `KJ5HST/methodology`

Pushed `main` only (never `--all` or `--mirror`) to `https://github.com/rmsharp/methodology.git` at his 'Yes, push main to the fork's origin (Recommended)'. Guard before the push: `git ls-remote origin refs/heads/main` = `6d5757e2`, an ancestor of local `main`, `git rev-list --count` = 6 (the trim `d7784581`, the fold `6fdfe9ac`, the claim `e66ee17d`, work `390b1893` and `14b018e3`, the close-out `5ae58a79`). Read-back after: `git ls-remote origin refs/heads/main` = `5ae58a79` = local `main`. This entry is a ledger-only commit that goes to `origin` under his standing grant; if `git rev-list --count origin/main..main` is not 0, that commit was not pushed.

### 2026-10-30 · [ad hoc] S401 close-out -- `pr4-body-check.py` fails a cited commit hash outside `<upstream>..<candidate>` unless it is upstream's tip or named as an extra argument; 7 of 7 expectations confirmed; the fork's gates pass 24 of 24; `HANDOFFS.md` trimmed 5 to 3 receipts and folded

The `HANDOFFS.md` receipt for S401 is complete (self-score 8; S400 scored 9 by this session). One deliverable: the fix, at his Phase 0 pick 'Fix pr4-body-check.py (Recommended)'; the trim `d7784581` and fold `6fdfe9ac` came first at his required Yes/No 'Yes, trim it (Recommended)'; the claim is `e66ee17d`, the work commits `390b1893` and `14b018e3`. The posted draft's command is now `pr4-body-check.py docs/planning/upstream-pr-body.md 47637be21425 d50ce290d921 65990cd c8b9ddd e7b389f` (exit 0; with no extras exit 1, naming exactly those three); `body-check-record.md` section 2 says why the older records' 'exit 0' is the old script's. The fork's gates, one run on `HEAD` `14b018e39bb5` with a clean tree after all work commits, 14:09:19 to 14:37:44: quality_ratchet: 24/24 pass, 0 fail, 0 unmeasured, results `32858fe46628`, manifest `102234f3acf8` (`tests-sh-passed` 692 against its floor 692). `HANDOFFS.md` now holds FOUR receipts, so no trim is due at S402's Phase 0 and one is due after S403's. `CHANGELOG.md` is under its 196,608 B trigger. No row appended to `docs/FORK_LEARNINGS.md`, so D3's duty does not fire (rows #16, #72, #107 and #109 already state this session's lessons). Fork `main` push: at his 'Yes, push main to the fork's origin (Recommended)'; the push record is the next entry. Local to the fork; nothing sent to `KJ5HST/methodology`.

### 2026-10-30 · [ad hoc] S401 work (2 of 2) -- the record and the two runs of `pr4-body-check.py`'s fix: 7 of 7 expectations confirmed, and 5 fail when the judge is pointed at the old script

`docs/planning/pr-composition-evidence/body-check-record.md` states the change (`pr4-body-check.py:57` to `:90`), what a reader of the older records must know (they report the OLD script's exit 0; the command for the posted draft now takes `65990cd c8b9ddd e7b389f` as extras and `d50ce29`, upstream's tip, needs none), the evidence and the scoring. `body-check-output.txt` is `body-check-run.sh` on the committed script (7 PASS, exit 0); `body-check-mutant-output.txt` is the same run with the script pointed at the old blob `7733b493f116` (E1 to E5 FAIL, exit 5), which shows the judge can fail. Nothing in #99's body, in an earlier record or on GitHub was edited. Local only; nothing sent to `KJ5HST/methodology`.

### 2026-10-30 · [ad hoc] S401 work (1 of 2) -- `pr4-body-check.py` fails a cited commit hash outside `<upstream>..<candidate>`; its seven expectations, written first, and the self-judging script that runs them

Before the edit, the committed script (blob `7733b493f116`) was run on `docs/planning/upstream-pr-body.md` (candidate `47637be21425`, upstream `d50ce290d921`): exit 0, 14 hashes `True`, four `False` (`65990cd`, `c8b9ddd`, `e7b389f`, `d50ce29`), which reproduces the hole `pr4b-record.md` item 5 describes. `body-check-expectations.txt` (E1 to E7, with confidences) was saved before the edit. The change to `docs/planning/pr-composition-evidence/pr4-body-check.py` (26 lines added, 3 removed): check 3 now fails a cited hash that is outside the range unless it is `<upstream>`'s own tip (allowed without being named) or one of the hashes given as extra arguments after `<upstream>`; an extra that does not resolve fails, an extra the body does not cite is printed and does not fail, and an in-range hash prints exactly as before. `body-check-run.sh <scratch-dir>` runs E1 to E7 from the repository root, judges each, and exits with the count that failed; it reads the old script from the committed blob. Local only; nothing sent to `KJ5HST/methodology`.

### 2026-10-30 · [ad hoc] S401 claim (in progress) -- fix `pr4-body-check.py` so a commit hash cited in a PR draft body that is outside `<upstream>..<candidate>` fails check 3 unless it is on a named allowlist; local only

Claimed at his Phase 0 picker: 'Fix pr4-body-check.py (Recommended)' (the others offered were deciding #99's 'over 52 files' sentence, another open item, and trimming only), with 'Yes, trim it (Recommended)' answered in the same picker as a required Yes/No for `HANDOFFS.md` (five receipts, 63,121 B, over the rule's four), which is why the trim `d7784581` (S396 and S397 archived to `docs/archive/HANDOFFS-through-2026-10-29-3.md`, 63,121 B to 39,521 B, proof exit 0 before and after the commit) and the fold `6fdfe9ac` came first and their entries sit below. Phase 0 (read 2026-10-30 at 14:00, `uptime` load 2.99): the `CHANGELOG.md` frontier = `HEAD` `6d5757e2` (0 undocumented, 0 merges); the `HANDOFFS.md` frontier `77ba41f9` is one commit behind (S400's ledger-only push record, not a session), no pending receipt; `check-ledger` and `check-handoff` exit 0; the newest receipt's gate citation (results `32858fe46628`, manifest `102234f3acf8`) equals `.quality-gates-results.json` (gates not re-run); `upstream/main` unchanged `d50ce290` (fetched); `pr5-step2-readback.sh` exit 0, 'READ-BACK OK (0 failed)'; #99 and #98 open, MERGEABLE, CLEAN, #96 open, CONFLICTING, each 0 comments, 0 reviews; issues #93, #95, #97 quiet; dashboard 72/100, 0 high-risk flags (its history line rides this claim); local `main` = `origin/main` `6d5757e2`. Local only; nothing sent to `KJ5HST/methodology`.

### 2026-10-30 · [ad hoc] S401 fold -- the trim's pointer block leaves `HANDOFFS.md` and one row joins `docs/HANDOFFS_ARCHIVE_INDEX.md`

The block (4 lines) became the row `| 2 | 2026-10-29 → 2026-10-29 | HANDOFFS-through-2026-10-29-3.md | v1.8.1 |`. Own commit, as the index's rule says (fork Learning #58). It follows the trim `d7784581` (five receipts to three, S396 and S397 archived; its proof `bash docs/archive/HANDOFFS-through-2026-10-29-3.md.verify.sh` exit 0 before and after that commit), taken at his Phase 0 'Yes, trim it (Recommended)'. The shard carries `-3` because `-2` was taken (the cut date is 2026-10-29 again). Local only; nothing sent to `KJ5HST/methodology`.

### 2026-10-30 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-29-3.md` (2 record(s), 63,121 B → 39,521 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-10-29 → 2026-10-29) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-29-3.md`](docs/archive/HANDOFFS-through-2026-10-29-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-29-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-29-3.md.verify.sh)
rather than trusting a digest printed here. Live file 63,121 B → 39,521 B (−37.4%).

### 2026-10-30 · [ad hoc] S400 push record -- fork `main` fast-forwarded `5f1a05e7..77ba41f9` (6 commits); the fork's `origin` only, nothing sent to `KJ5HST/methodology`

At his 'Yes, push main to the fork's origin (Recommended)' during the gate run. Guards read first, in the same script as the push: the remote's `main` equalled `5f1a05e7`, that sha was an ancestor of `main`, the count was 6 (the trim, claim, three work commits and the close-out), no merges. `git push origin refs/heads/main:refs/heads/main` exit 0 (named ref, never `--all`); after it `git ls-remote origin refs/heads/main` equals the local `main` (`77ba41f9`), `feat/methodology-directory` still `47637be21425` (the head of #99), no `pr2b/*` ref on `origin` (the squash branch stays local), `upstream/main` still `d50ce290`, and #99 still OPEN, MERGEABLE, CLEAN with 0 comments and 0 reviews. Read AFTER the push, not before it as S399 did: one author on the 6 commits, 0 hits for key shapes in the added lines, no pre-push hook, the disclosure trailer on all 6. This entry is the one commit after that push; it is pushed to `origin` under his standing grant for ledger-only push records.

### 2026-10-30 · [ad hoc] S400 close-out -- the squash-merge check for #99: a squash of the 33 commits makes `bin/sync` refuse 71 files over the same 10 of 12 adopters, against 52 for a merge or a rebase; the fork's gates pass; `CHANGELOG.md` trimmed 127 to 64 records

The `HANDOFFS.md` receipt for S400 is complete (self-score 8; S399 scored 8 by this session). One deliverable: the squash-merge check, at his Phase 0 pick 'Squash-merge check (Recommended)'; the trim `2eb43868` came first at his required Yes/No 'Yes, trim it (Recommended)'; the claim is `9232eaee`, the work commits `de5464f3`, `83aaf99b` and `c0b0fc3c`. The fork's gates, one run on `HEAD` `c0b0fc3c8d78` with a clean tree after all work commits, 13:27:15 to 13:52:40: quality_ratchet: 24/24 pass, 0 fail, 0 unmeasured, results `32858fe46628`, manifest `102234f3acf8` (`tests-sh-passed` 692 against its floor 692). `HANDOFFS.md` now holds FIVE receipts, so a trim is due after S401's Phase 0 report (the rule trims above four). `CHANGELOG.md` is under its 196,608 B trigger after the trim. No row appended to `docs/FORK_LEARNINGS.md`, so D3's duty does not fire. Fork `main` push: at his 'Yes, push main to the fork's origin (Recommended)'; its own 'S400 push record' entry follows if it happens. Nothing else was sent to `KJ5HST/methodology`: no comment, no edit to #99, #98, #96 or the issues; the branch `pr2b/squash-check` is local only.

### 2026-10-30 · [ad hoc] S400 work (3 of 3) -- the squash-merge check's answer: a squash of the 33 commits makes `bin/sync` refuse **71** files over the same 10 of 12 adopters, against 52 for a merge or a rebase (+19, four file versions); everything else is identical

`docs/planning/pr-composition-evidence/squash-record.md` is the answer and `squash-compare-output.txt` the comparison it rests on (reproduced byte for byte from the committed files). The control reproduces S396's 52 exactly (the refused set equals S396's at 12 of 12). The +19 are four file versions that an adopter holds, that are also in the fork's history, and that one of the 33 commits carries at an intermediate point: `context_budget.py` (7 adopters; `f767ced0`), `methodology_dashboard.py` (6; `e5210601`), `quality_ratchet.py` (5; `7d87cb2b`) and `quality_ratchet.py` (`vscode_quarto_ext`; `1d93579a`); none is in upstream's history of the file or the candidate's final version. The forced sync, the seeds, the sync after it and both fixtures are identical. Expectations: 12 confirmed, 1 wrong (E5: I expected the totals equal, 50%), 1 not measured (E14: no fingerprint of the real trees was taken before the runs). The posted body of #99 says 'over 52 files', true of the branch as pushed (the merge route) and 71 under a squash; whether to say so on #99 is his call, and nothing was posted. Nothing sent to `KJ5HST/methodology`.

### 2026-10-30 · [ad hoc] S400 work (2 of 3) -- the squash-merge check's comparison: `squash-compare.py` (read-only), the squash run's report, the run times and the adopters' reflogs

`squash-compare.py` reads both `rows.json` and S396's and asks git which commits of `upstream/main..pr2b/candidate` carry each version the squash newly refuses; it exits 0 when every property expectation holds (it did). `squash-adopters-output.md` is the squash run's own report (its header sentence names `pr2b/candidate` because the ref name is hard-coded in the script; the sha `ea256ad` is the squash branch's). `squash-run-times.txt`: the three timestamps and loads. `squash-reflog-output.txt`: the adopters' `HEAD` reflog entries since 13:00, read after the runs (three projects were committed to by their own sessions in or just after the window). The output and the record follow. Nothing sent to `KJ5HST/methodology`.

### 2026-10-30 · [ad hoc] S400 work (1 of 3) -- the squash-merge check's runs: the 14 expectations (saved before the squash ref was built), then `pr3b-adopters.py` over the 12 adopters against `pr2b/candidate` (the control: 52 files refused, 272 s) and against the new local `pr2b/squash-check` (71, 266 s); both `rows.json`

The local branch `pr2b/squash-check` (`ea256adbe208`, never pushed) is `upstream/main` `d50ce290d921` plus one commit holding the candidate's tree `382d305a4c27` (the same tree as `47637be21425`, one commit above upstream, 47 files each). Two runs of S396's `pr3b-adopters.py`, unchanged, back to back from the repository root, each with its own `--work` and `--out` in the scratchpad (13:12:37 to 13:17:09 and 13:17:09 to 13:21:35, load 5.0 to 7.0). Files: `squash-expectations.txt`, `squash-control-rows.json`, `squash-control-adopters-output.md`, `squash-rows.json` in `docs/planning/pr-composition-evidence/`. The comparison and the record follow in the next two commits. Nothing sent to `KJ5HST/methodology`.

### 2026-10-30 · [ad hoc] S400 claim (in progress) -- the squash-merge check for #99: a local `upstream/main`-plus-one-commit ref holding the candidate's tree, `pr3b-adopters.py` over the 12 adopters against it and against `pr2b/candidate` as a same-day control; local only

Claimed at his Phase 0 picker: 'Squash-merge check (Recommended)' (the others offered were a fix to `pr4-body-check.py` and stopping after Phase 0), with 'Yes, trim it (Recommended)' answered in the same picker as a required Yes/No for `CHANGELOG.md` (199,263 B against its 196,608 B trigger), which is why the trim `2eb43868` (63 of 127 records to `docs/archive/CHANGELOG-through-2026-10-28.md`, 99,272 B live, proof exit 0 before and after the commit) came first and its entry sits below. Phase 0 (read 2026-10-30 at 13:06, `uptime` load 5.87): the `CHANGELOG.md` frontier = `HEAD` `5f1a05e7` (0 undocumented, 0 merges); the `HANDOFFS.md` frontier `8f4b5e2a` is one commit behind (S399's ledger-only push record, not a session), no pending receipt, 4 receipts at 53,089 B; `check-ledger` and `check-handoff` exit 0; the newest receipt's gate citation (results `32858fe46628`, manifest `102234f3acf8`) equals `.quality-gates-results.json` (run on `d3f73511`, no code changed since); `upstream/main` unchanged `d50ce290` (fetched); `pr5-step2-readback.sh 99 d50ce290d921 47637be21425 feat/methodology-directory` exit 0, 'READ-BACK OK (0 failed)'; #99 open, MERGEABLE, CLEAN, 0 comments, 0 reviews; #98 open, MERGEABLE, CLEAN (`65990cda`); #96 open, CONFLICTING (`ad5c980f`); issues #93, #95, #97 no activity since 10-24; dashboard 72/100, 0 high-risk flags (its history line rides this claim). Nothing sent to `KJ5HST/methodology`.

### 2026-10-30 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-10-28.md` (63 record(s), 199,263 B → 99,272 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **63** record(s) (2026-10-27 → 2026-10-28) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-10-28.md`](docs/archive/CHANGELOG-through-2026-10-28.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-10-28.md.verify.sh`](docs/archive/CHANGELOG-through-2026-10-28.md.verify.sh)
rather than trusting a digest printed here. Live file 199,263 B → 99,272 B (−50.2%).

### 2026-10-30 · [ad hoc] S399 push record -- fork `main` fast-forwarded `194b5717..8f4b5e2a` (5 commits); the fork's `origin` only, nothing sent to `KJ5HST/methodology`

At his 'Yes, push main to the fork's origin (Recommended)' during the gate run. Guards read first, in the same script as the push: the remote's `main` equalled `origin/main` (`194b5717`), that sha was an ancestor of `main`, the count was 5 (the trim, fold, claim, work and close-out commits), no merges, one author, 0 hits for key shapes in the added lines, no pre-push hook. `git push origin main` exit 0; after it `git ls-remote origin refs/heads/main` equals the local `main` (`8f4b5e2a`), `feat/methodology-directory` still `47637be21425` (the head of #99), `upstream/main` still `d50ce290`, and #99 still OPEN, MERGEABLE, CLEAN with 0 comments and 0 reviews. This entry is the one commit after that push; it is pushed to `origin` under his standing grant for ledger-only push records.

### 2026-10-30 · [ad hoc] S399 close-out -- PR5 step 2, pull request #99 opened on `KJ5HST/methodology` from `rmsharp:feat/methodology-directory` (33 commits on `upstream/main` `d50ce290`; OPEN, MERGEABLE, CLEAN, 0 comments); the fork's gates pass 24 of 24; `HANDOFFS.md` trimmed 4 to 3 and folded

The `HANDOFFS.md` receipt for S399 is complete (self-score 8; S398 scored 9 by this session). One deliverable: the pull request, opened at his 'Yes, open it as shown (Recommended)' after the title, the exact command and the one change to his approved text (the 'Generated with Claude Code' footer) were shown, and read back by hand and by `pr5-step2-readback.sh` (exit 0; a control exits 1). The trim `2c9ee5c1` and fold `47b0373a` came first at his required Yes/No; the claim is `4eccaa4a`, the work commit `d3f73511`. The fork's gates, one run on `HEAD` `d3f73511fae8` with a clean tree after all work commits, 10:09:47 to 10:35:07: quality_ratchet: 24/24 pass, 0 fail, 0 unmeasured, results `32858fe46628`, manifest `102234f3acf8` (`tests-sh-passed` 692 against its floor 692). **`CHANGELOG.md` is now 198,300 B against its 196,608 B trim trigger, which FIRES** (`methodology_trim.py --file CHANGELOG.md --check` reads 'trigger FIRES'; hard refusal 262,144 B): the next Phase 0 reports it and asks for a go-ahead, as S389 did for `cee05064`. No row appended to `docs/FORK_LEARNINGS.md`, so D3's duty does not fire. Fork `main` push: at his 'Yes, push main to the fork's origin (Recommended)'; its own 'S399 push record' entry follows if it happens. Nothing else was sent to `KJ5HST/methodology`: no comment, no edit to #98, #96 or the issues.

### 2026-10-30 · [ad hoc] S399 work -- PR5 step 2: the read-back script `pr5-step2-readback.sh`, its saved output and the record `pr5-step2-record.md`; the draft's status line now says OPENED

Three files in `docs/planning/pr-composition-evidence/` and a one-sentence edit to line 3 of `docs/planning/upstream-pr-body.md` (the status line said 'nothing sent'; lines 7 and 9 to 105, the title and the posted body, are untouched), committed after the pull request entry just below. `pr5-step2-readback.sh <pr> <upstream> <candidate> <remote-branch>` is read-only (`gh pr view`, one `gh api` GET, `git ls-remote`, git objects) and exits 0 only when every check agrees; on `99 d50ce290d921 47637be21425 feat/methodology-directory` it printed 'READ-BACK OK (0 failed)' (`pr5-step2-readback-output.txt`). A control with a wrong candidate and a branch that does not exist printed 7 `FAIL` lines and exited 1. The record says the answer first, then what was done in order, what it does not show, and what step 3 starts from.

### 2026-10-30 · [ad hoc] S399 pull request -- #99 opened on `KJ5HST/methodology` from `rmsharp:feat/methodology-directory` (`47637be21425`, 33 commits on `upstream/main` `d50ce290d921`) into `main`

At his answer 'Yes, open it as shown (Recommended)' to the question that showed the title, the body and the exact command (the others offered: 'Yes, but without the added line', 'Show me the whole body here first', 'No, not now'). Command: `gh pr create -R KJ5HST/methodology --base main --head rmsharp:feat/methodology-directory --title "$(cat <title file>)" --body-file <body file>`; exit 0, https://github.com/KJ5HST/methodology/pull/99. Title: line 7 of `docs/planning/upstream-pr-body.md` without `**Title:** `. Body: lines 9 to 105 byte for byte (21,684 B, the text he approved as draft 12) plus a blank line and `🤖 Generated with [Claude Code](https://claude.com/claude-code)` (21,751 B in all). Guards read in the same script before the command, all held: the step-1 read-back exit 0; `upstream/main` `d50ce290d921`; #98's head `65990cda`; #96's head `ad5c980f`; 0 pull requests from the head. Read back after: OPEN, not a draft, MERGEABLE, CLEAN, base `main`, 33 commits, 47 files, +18,367 / -1,098, 0 comments, 0 reviews, title equal to the file, body equal to the text. Nothing else was sent: #98, #96 and the three open issues are untouched, and no comment was posted. Step 3 (answering comments) is not started and is his go-ahead. Undo: `gh pr close 99 -R KJ5HST/methodology` (also an outward act; the branch and commits stay).

### 2026-10-30 · [ad hoc] S399 claim (in progress) -- PR5 step 2: open the one upstream pull request from `feat/methodology-directory` into `KJ5HST/methodology` `main`, only on his second go-ahead after the exact command and text are shown

Claimed at his Phase 0 picker: 'PR5 step 2: open the PR (Recommended)' (the others offered were the squash-merge check and a fix to `pr4-body-check.py`), with 'Yes, trim 4 to 3 (Recommended)' (done first: the trim `2c9ee5c1` and the fold `47b0373a`, whose entries sit below; S395 archived to `docs/archive/HANDOFFS-through-2026-10-29-2.md`, proof exit 0, `HANDOFFS.md` 41,440 B after the fold, 24,096 B of room under 65,536). Phase 0 (read 2026-10-30 at 09:56, `uptime` load 3.12): the `CHANGELOG.md` frontier = `HEAD` `194b5717` (0 undocumented, 0 merges); the `HANDOFFS.md` frontier `32c47468` is one commit behind (S398's ledger-only push record, not a session), no pending receipt; `check-ledger` and `check-handoff` exit 0; the newest receipt's gate citation (results `32858fe46628`, manifest `102234f3acf8`) equals `.quality-gates-results.json`; `upstream/main` unchanged `d50ce290` (fetched); `pr5-step1-readback.sh d50ce290d921 47637be21425 feat/methodology-directory` exit 0, 'READ-BACK OK (0 failed)' (GitHub: ahead 33, behind 0; no pull request from that head); #98 open, MERGEABLE, CLEAN (`65990cda`); #96 open, CONFLICTING (`ad5c980f`); each 0 comments, 0 reviews; issues #93, #95, #97 no activity since 10-24; `CHANGELOG.md` trim check: trigger does not fire (190,929 B against 196,608 B); dashboard 72/100, 0 high-risk flags (its history line rides this claim). Nothing sent to `KJ5HST/methodology`.

### 2026-10-30 · [ad hoc] S399 fold -- the trim's pointer block leaves `HANDOFFS.md` and one row joins `docs/HANDOFFS_ARCHIVE_INDEX.md`

The block (4 lines, 448 B) became the row `| 1 | 2026-10-29 → 2026-10-29 | HANDOFFS-through-2026-10-29-2.md | v1.8.1 |`. Own commit, as the index's rule says (fork Learning #58). It follows the trim `2c9ee5c1` (four receipts to three, S395 archived; its proof `bash docs/archive/HANDOFFS-through-2026-10-29-2.md.verify.sh` exit 0 before this fold), taken at his Phase 0 'Yes, trim 4 to 3 (Recommended)'. The shard carries `-2` because `HANDOFFS-through-2026-10-29.md` was taken (the cut date is S395's, 2026-10-29, as S394's was). Local only; nothing sent to `KJ5HST/methodology`.

### 2026-10-30 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-29-2.md` (1 record(s), 53,484 B → 41,896 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-29 → 2026-10-29) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-29-2.md`](docs/archive/HANDOFFS-through-2026-10-29-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-29-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-29-2.md.verify.sh)
rather than trusting a digest printed here. Live file 53,484 B → 41,896 B (−21.7%).

### 2026-10-30 · [ad hoc] S398 push record -- fork `main` fast-forwarded `b063c61a..32c47468` (5 commits); the fork's `origin` only, nothing sent to `KJ5HST/methodology`

At his 'Yes, push main to the fork's origin (Recommended)' during the gate run. Guards read first: the remote's `main` equalled `origin/main` (`b063c61a`), that sha was an ancestor of `main`, the count was 5 (the trim, fold, claim, work and close-out commits), no merges, one author. `git push origin main` exit 0; after it `git ls-remote origin refs/heads/main` equals the local `main` (`32c47468`), `feat/methodology-directory` still `47637be21425`, `upstream/main` still `d50ce290`. This entry is the one commit after that push; it is pushed to `origin` under his standing grant for ledger-only push records. The pull request is unopened.

### 2026-10-30 · [ad hoc] S398 close-out -- PR5 step 1, the candidate branch pushed to the fork's `origin` as `feat/methodology-directory` and read back (33 commits on `upstream/main` `d50ce290`; GitHub: ahead 33, behind 0, 47 files); the fork's gates pass 24 of 24; `HANDOFFS.md` trimmed 4 to 3 and folded; nothing sent to `KJ5HST/methodology`

Deliverable: local `pr2b/candidate` `47637be21425` (33 commits directly on `upstream/main` `d50ce290d921`) is on the fork's `origin` as `feat/methodology-directory`, read three ways: `git ls-remote` equals the local tip; GitHub's own comparison with upstream's `main` reads ahead 33, behind 0, 47 files; no pull request exists from that head. The push entry (10-29) and the work entry (10-30: `pr5-step1-readback.sh`, its output, `pr5-step1-record.md`) sit below. At his Phase 0 picker 'PR5 step 1: push the candidate (Recommended)' and 'Yes, trim 4 to 3 (Recommended)'; the remote name, asked on its own because it shows in the pull request header, 'feat/methodology-directory (Recommended)' (the other offered was `pr2b/candidate`). Step 2 (opening the pull request on `KJ5HST/methodology`) and step 3 (answering comments) are each his go-ahead and not started. The fork's gates on `65878fb5ffee`, clean tree, one run 00:01:32 to 00:28:01 (26 min 29 s; load 32.69 at the start, 3.24 at 00:12): quality_ratchet: 24/24 pass · 0 fail · 0 unmeasured · results 32858fe46628 · manifest 102234f3acf8 (equal to S397's citation). Receipt `HANDOFFS.md` S398 complete (self 8, predecessor 8); no row appended to `docs/FORK_LEARNINGS.md`, so D3's duty does not fire and no row was considered. At his 'Yes, push main to the fork's origin (Recommended)' the fork's `main` is pushed after this commit, guarded, and recorded in an 'S398 push record' entry; nothing is sent to `KJ5HST/methodology`.

### 2026-10-30 · [ad hoc] S398 work -- PR5 step 1: the read-back script `pr5-step1-readback.sh`, its saved output and the record `pr5-step1-record.md`; nothing sent to `KJ5HST/methodology`

Three files in `docs/planning/pr-composition-evidence/`, committed after the push entry just below. `pr5-step1-readback.sh <upstream> <candidate> <remote-branch>` is read-only (git objects, `git ls-remote`, GitHub's read endpoints) and exits 0 only when every check agrees; its output on `d50ce290d921 47637be21425 feat/methodology-directory` is `pr5-step1-readback-output.txt` (exit 0, 'READ-BACK OK (0 failed)'). A control against a branch name that does not exist printed 6 `FAIL` lines and exited 1. The record says the answer first, then the guards, the push, the read-back, what it does not show, and what step 2 starts from (the title is line 7 of `docs/planning/upstream-pr-body.md`, the body lines 9 to 105, 21,684 B; the first body line `@KJ5HST:` notifies him on posting). No expectations file: one push, no prediction beyond the guards' own outcomes (stated in the record).

### 2026-10-29 · [ad hoc] S398 push -- local `pr2b/candidate` (`47637be21425`, 33 commits on `upstream/main` `d50ce290d921`) pushed to the fork's `origin` as `feat/methodology-directory`; nothing sent to `KJ5HST/methodology`

At his Phase 0 pick 'PR5 step 1: push the candidate (Recommended)', the name from his answer 'feat/methodology-directory (Recommended)' (the other offered was `pr2b/candidate`). Command: `git push origin pr2b/candidate:refs/heads/feat/methodology-directory` (no force, no `-u`); exit 0, `* [new branch]`. Guards read first: tip and count (33, no merges, merge-base equals upstream's tip), the name free on `origin`, `origin/main` still `b063c61a`, one author on all 33 commits, 0 hits for key shapes in the added lines, no pre-push hook. Read back after: `git ls-remote --heads origin` equals the local tip; GitHub's comparison with upstream's `main` reads ahead, 33 ahead, 0 behind, 47 files; no pull request from that head; #98 and #96 unchanged; `upstream/main` unchanged. Step 2 (opening the pull request on `KJ5HST/methodology`) and step 3 (answering comments) are each their own go-ahead and not started. Undo before step 2: `git push origin --delete feat/methodology-directory`.

### 2026-10-29 · [ad hoc] S398 claim (in progress) -- PR5 step 1: push `pr2b/candidate` to the fork's `origin` as `feat/methodology-directory` and read it back; nothing sent to `KJ5HST/methodology`

Claimed at his Phase 0 picker: 'PR5 step 1: push the candidate (Recommended)' (the others offered were the PR3 squash-merge check and a fix to `pr4-body-check.py`), with 'Yes, trim 4 to 3 (Recommended)' (done first: the trim `db09d8c2` and the fold `84cb3b89`, whose entries sit below; S394 archived to `docs/archive/HANDOFFS-through-2026-10-29.md`, proof exit 0, `HANDOFFS.md` 42,231 B after the fold, 23,305 B of room). Then a second question about the remote branch's name: 'feat/methodology-directory (Recommended)' (the other offered was the local name `pr2b/candidate`); the name shows in the pull request header and follows the fork's `feat/<topic>` pattern. Phase 0 (read 2026-10-29 at 20:50, `uptime` load 5.49): the `CHANGELOG.md` frontier = `HEAD` `b063c61a` (0 undocumented, 0 merges); the `HANDOFFS.md` frontier `c5b02328` is one commit behind (S397's ledger-only push record, not a session), no pending receipt; `check-ledger` and `check-handoff` exit 0; the newest receipt's gate citation (results `32858fe46628`, manifest `102234f3acf8`) equals `.quality-gates-results.json`; `upstream/main` unchanged `d50ce290` (fetched); #98 open, MERGEABLE, CLEAN (`65990cda`); #96 open, CONFLICTING (`ad5c980f`); each 0 comments, 0 reviews; issues #93, #95, #97 no new activity; dashboard 72/100, 0 high-risk flags; local `pr2b/candidate` `47637be21425` is 33 commits on `upstream/main` (merge-base equals the tip) and no `pr2*` branch is on the fork's `origin` (`ls-remote`). Deliverable: PR5 step 1 of `docs/planning/upstream-pr-composition-plan.md` (§5, line 183): guard the push (the branch's tip and its 33 commits on `d50ce290` re-read, the remote name unused on `origin`), push that one ref to `origin` only, read it back with `ls-remote`. Step 2 (opening the pull request on `KJ5HST/methodology`) and step 3 (answering comments) are each their own go-ahead and not started. Phase 3F records the rest.

### 2026-10-29 · [ad hoc] S398 fold -- the trim's pointer block leaves `HANDOFFS.md` and one row joins `docs/HANDOFFS_ARCHIVE_INDEX.md`

The block (4 lines, 448 B; `HANDOFFS.md` 42,679 B before, 42,231 B after) became the row `| 1 | 2026-10-29 → 2026-10-29 | HANDOFFS-through-2026-10-29.md | v1.8.1 |`. Own commit, as the index's rule says (fork Learning #58). It follows the trim `db09d8c2` (four receipts to three, S394 archived; its proof `bash docs/archive/HANDOFFS-through-2026-10-29.md.verify.sh` exit 0), taken at his Phase 0 'Yes, trim 4 to 3 (Recommended)'. The shard is named `-2026-10-29` (no suffix) because the cut date is S394's, 2026-10-29; the earlier trims' `-2026-10-28-N` names were of the 28th. Local only; nothing sent to `KJ5HST/methodology`.

### 2026-10-29 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-29.md` (1 record(s), 53,853 B → 42,679 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-29 → 2026-10-29) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-29.md`](docs/archive/HANDOFFS-through-2026-10-29.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-29.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-29.md.verify.sh)
rather than trusting a digest printed here. Live file 53,853 B → 42,679 B (−20.7%).

### 2026-10-29 · [ad hoc] S397 push -- fork `main` fast-forwarded `eaafc5f2..c5b02328` (10 commits); the fork's `origin` only, nothing sent to `KJ5HST/methodology`

At his 'Yes, push to the fork's origin (Recommended)'. Guarded before the push: `git remote get-url origin` was `https://github.com/rmsharp/methodology.git` (the fork), `git ls-remote origin refs/heads/main` equalled `origin/main` (`eaafc5f2`), that sha was an ancestor of `main`, and `git rev-list --count origin/main..main` read 10, as expected (the question to him said 'about 12'; it was 10). Read back after: the remote's `main` is `c5b02328`, `git rev-list --count origin/main..main` reads 0, and `pr4b-claims.sh` and `pr4b-facts.sh` are on `origin/main`, so the draft's evidence links resolve. `pr2b/candidate` and `pr2/candidate` stay local branches; the pull request is unopened.

### 2026-10-29 · [ad hoc] S397 close-out -- PR4, the text of the one upstream pull request, re-checked on the rebuilt branch `pr2b/candidate`; draft 12 approved by him as committed; nothing sent to `KJ5HST/methodology`

Deliverable: `docs/planning/upstream-pr-body.md` is draft 12 (draft 11: `git show 7d00d29:docs/planning/upstream-pr-body.md`), draft 11 checked claim by claim against `pr2b/candidate` `47637be2` (33 commits on `upstream/main` `d50ce290`) by `pr4b-draft12-build.py` (26 exact-once edits), after one serial claims run (29 min, expectations saved first), the first commit alone, the cost, the fixtures, the moved project, the merge-file and distribution re-runs and `pr4b-facts.sh`. Found wrong in draft 11: decision 3 asked about merged #94 (now #98, with #96 named); the '42%' earlier-work share cited to a script that does not print it (now 37%, `pr4b-facts.sh`); 'a separable run' of reference-removing commits (seven, two others, a tail of three); 'within 0.1 s'; 'the first paragraph of the runner changed' (the third, and 38 lines naming `docs/methodology/` become 10); the 27 cherry-pick lines undisclosed. One fresh read-only agent read the frozen draft (`357ae739`, 6 of 10); its factual findings were re-run and six fixed (`b6784956`). His approval, at the S397 picker 'Draft 12 as committed', is recorded by one hand edit of the draft's status line (above the rule; the body is unchanged at 21,802 B); the builder still writes 'awaiting'. His correction: the maintainer wants the layout (direct conversation); the plan's §8 still says unknown. The fork's gates on `b6784956a37a`, clean tree: quality_ratchet: 24/24 pass · 0 fail · 0 unmeasured · results 32858fe46628 · manifest 102234f3acf8 (31 min 53 s, load 41.58 at the start). Receipt `HANDOFFS.md` S397 complete (self 7, predecessor 8); no row appended to `docs/FORK_LEARNINGS.md`. At his 'Yes, push to the fork's origin (Recommended)' the fork's `main` is pushed after this commit, guarded, and recorded in an 'S397 push' entry; nothing is sent to `KJ5HST/methodology`, and the pull request is unopened.

### 2026-10-29 · [ad hoc] S397 work (cold read, files) -- PR4: the revised draft 12, its builder, the checker's output and the record `pr4b-record.md`, committed after the entry just below them; local only; nothing sent to `KJ5HST/methodology`

The entry headed "S397 work (cold read)" was written one commit early and rides with evidence 4's commit (`78fddc2f`), so that commit's diff carries it; this commit holds what it describes: `docs/planning/upstream-pr-body.md` (draft 12, 26 edits, 21,802 B), `pr4b-draft12-build.py`, `pr4b-body-check-output.txt` and `pr4b-record.md` (19.9 KB; sections 1 to 8, the reader's findings with what I did with each, and his seven calls). I first tried to edit that earlier entry to give this commit a ledger change; the ledger hook refused it (a committed entry is never edited) and this entry is the correction.

### 2026-10-29 · [ad hoc] S397 work (evidence 4) -- PR4: `pr4b-facts.sh` gains three sections after the cold read: where the documents say the framework files are, the cherry-pick lines, the migration suite's classes in `bin/tests.sh`; local only; nothing sent to `KJ5HST/methodology`

Section 9: the runner's "Where the files are" paragraph is at line 7 (the third paragraph) and 38 lines of the changed markdown files name `docs/methodology/` at upstream's tip against 10 on the branch (the runner 11 to 1, the skills index 14 to 0, `SAFEGUARDS.md` 1 to 0, `BOOTSTRAP.md` 9 to 8, two seed sources 1 to 0). Section 10: 27 of the 33 commits end with a `(cherry picked from commit ...)` line. Section 11: `bin/tests.sh:326` runs two classes of the migration suite (95 tests). Each was a finding of the cold reader that I re-ran before acting on it; the output is `pr4b-facts-output.txt`, replaced whole.

### 2026-10-29 · [ad hoc] S397 work (cold read) -- PR4: one fresh agent read draft 12 frozen at `357ae739` (6 of 10); I re-ran its factual findings and revised the draft to 26 edits, 21,802 B; the record `pr4b-record.md`; local only; nothing sent to `KJ5HST/methodology`

Confirmed and fixed: decision 1's "first paragraph of `SESSION_RUNNER.md` changed" (it is the third, and the documents' path mentions change with it: 38 lines to 10); "280 tests (separate from `bin/tests.sh`)" (two classes run there); decision 4's "them" and unnamed "tail of three" (now `e051462` to `8c37c28` and `1477af2` to `47637be`); the `138` is the scanner's own "acknowledged" count; 27 of 33 commits end in a cherry-pick line naming a fork-only commit (now disclosed). Removed: the `merge=union` sentence in decision 3 and the 1.9.1 / 1.10.0 aside. Confirmed and not a text edit: the evidence scripts `pr4b-claims.sh` and `pr4b-facts.sh` are not on the fork's pushed `main` (his call: the push is PR5's first step). Not acted on, with the reason in the record: the cut list, the missing "directory without the tool" option, draft 11's approved wording. The agent's discipline slipped twice, both disclosed by it (`git merge-tree --write-tree` twice; one `/tmp` redirect denied before it ran); the working tree held only my own untracked record afterwards. `pr4-body-check.py` on the revised draft: exit 0, no banned token, the only hashes outside `upstream..candidate` are #98's head, the two on the fork's `main` and upstream's tip. Record sections 1 to 7 are written; section 7 lists his calls.

### 2026-10-29 · [ad hoc] S397 work -- PR4: draft 12 of the one upstream pull request's text, draft 11 checked claim by claim against the rebuilt branch; frozen for a cold read; local only; nothing sent to `KJ5HST/methodology`

`docs/planning/upstream-pr-body.md` is now draft 12; draft 11 is `git show 7d00d29:docs/planning/upstream-pr-body.md` (approved at the S338 picker). Built by `pr4b-draft12-build.py`: 23 exact-once edits, refusing unless the file is draft 11 as `7d00d29` holds it. What changed: #92 and #94 are merged, so decision 3 asks about #98 (5 regions in 3 files; both name the trimmer 1.9.0) and names #96 (3 regions in 2); the trimmer is upstream's 1.8.2 with the layout changes on top, so the commit list is rewritten for 33 commits, the earlier work is two commits (37%, not 42%) and the whole-file bullet is about the dashboard alone; the sizes (18,367 added, 19 files reach a project, 86% stay); the 12 projects (52 files refused, 51 fork versions and 1 edit, not 39); the cost sentence (the dashboard is quicker, not "within 0.1 s"); and a claim draft 11 made that the rebuilt series falsifies: the ten reference-removing commits are no longer one run at the tip (seven, then `fd43f70` and `9848b62`, then a tail of three). The body is 21,612 B (draft 11: 21,486 B; his budget 20,000 B). `pr4-body-check.py` (`pr4b-body-check-output.txt`): exit 0, no banned token, no placeholder, every hash of the branch resolves in `upstream..candidate`; the four that do not are #98's head, the two on the fork's `main` and upstream's tip, each named as such in the text. Not yet read by anyone.

### 2026-10-29 · [ad hoc] S397 work (evidence 3 of 3) -- PR4: the first commit alone, the cost, the two fixtures and the moved project re-run on `pr2b/candidate`; local only; nothing sent to `KJ5HST/methodology`

Four serial runs after the claims run, expectations E13 to E16 appended to `pr4b-expectations.txt` before they started (18:55:28). `pr4b-first-commit-output.txt`: `fbcef390` alone on `d50ce290`, 271 passed, 0 failed, 0 skipped, gates 12/12, 0 unmeasured, results `e658e1a02647`, manifest `84815aa7e6e5`. `pr4b-cost-output.txt`: the runner and `SAFEGUARDS.md` together +244 B (+0.35%), about 87 tokens, equal to draft 11's; timings: the same at 3 commits, and on 517 commits the dashboard takes 0.66 s against upstream's 0.92 s, so draft 11's "within 0.1 s" no longer holds as worded (the candidate is quicker, by 0.26 s). `pr4b-fixture-output.txt` and `pr4b-moved-output.txt`: byte-identical to draft 11's (30 paths each, 22 differ; upstream 0 and this branch 19 with 7 seeds edited, 0 seeds changed; a moved project, upstream 30 paths outside `methodology/`, this branch 0). All four exit 0.

### 2026-10-29 · [ad hoc] S397 work (evidence 2 of 3) -- PR4: the derived facts the text states and no earlier script printed, and the two git-only re-runs; local only; nothing sent to `KJ5HST/methodology`

`pr4b-facts.sh` (new, read-only, git objects only) and `pr4b-facts-output.txt`: each of the 33 commits' files and lines (most files in one commit: 7); the ten reference-removing commits (10; they sit as 22 to 28, then `fd43f707` and `9848b62b`, then 31 to 33); the earlier-work share (`fbcef390` and `1d93579a`: 6,883 of 18,367 added lines, 37.5%); the old and the new candidate's trees differ in 9 files only; upstream's trimmer history (17 commits, 1.5.0 to 1.8.2, all with a `TRIM_VERSION` line); the two of upstream's dashboard tests the branch does not carry; #98's trimmer versions (1.9.0, 1.9.1, 1.10.0) against this branch's 1.9.0, and none of #98's content in this branch; merge-tree counts with and without the repository's attributes (#96 alone with upstream's tip conflicts in `CHANGELOG.md`, the `merge=union` gap, which is why the layer record's 4 regions in 3 files read 3 in 2 here). `pr4b-mergefile-output.txt` (`pr4-mergefile.sh` against `d50ce290`: 47 regions in 9 files, the dashboard's two copies 34, the trimmer 1 and its tests 1; draft 11's 51 in 8 had the trimmer at 6). `pr4b-distribution-output.txt` (`pr4-distribution.py`: 19 files reach a project, +2,540 / -526; 3 seed sources; 25 stay, +15,820, 86.1%). Draft 11 credited the "42%" earlier-work share to `pr4-distribution.py`, which prints no such line; the share is `pr4b-facts.sh` section 3, and the figure reproduced for the old branch by the same sum (8,461 of 19,983).

### 2026-10-29 · [ad hoc] S397 work (evidence 1 of 3) -- PR4: the claims of the plan's section 6 re-run on `pr2b/candidate` `47637be2` against `upstream/main` `d50ce290`; the expectations were saved first; local only; nothing sent to `KJ5HST/methodology`

`pr4b-expectations.txt` (twelve, written 18:25:06, before the run), `pr4b-claims.sh` (`pr4-claims.sh` with section 8's two heads and their label changed: #98 `65990cda`, #96 `ad5c980f`, not #94 and #92, which merged), `pr4b-claims-output.txt` (one serial run, exit 0, about 29 minutes, clean `--no-local` clones, 0 dirty paths) and `pr4b-up-links-output.txt` (upstream's own `bin/check-links` on a clean export: 116 links in 23 documents, so the table's "116 at your tip" stands). Result: 47 files, +18,367 / -1,098, 33 commits, merge-base is upstream's tip; shell suite 302 passed, 0 failed, 0 skipped (upstream 261 / 0); gates 18/18, 0 unmeasured, results `8c7362ca5b27`, manifest `72583325c300` (upstream 12/12); `check-links --layout both` 80 links in 23 documents in each layout; scanner 15 files, 0 sites, 138 acknowledged; layout suite 76 OK and 11 of 11 copies equal; the one tracked proof exits 0 at both tips; 33 commits compared, 0 refusals, 0 warnings, five floors raised; #98 reads 5 regions in 3 files, #96 3 regions in 2. Expectations scored in the file: ten confirmed and two half-confirmed: E6 (upstream's link count did not move, against my 55% that it would) and E11 (#96 reads 3 regions in 2 files, not the 4 in 3 I took from layer 23, whose tool counts as GitHub does, with no `merge=union`; I had not read how it counted).

### 2026-10-29 · [ad hoc] S397 claim (in progress) -- PR4, the text of the one upstream pull request, re-checked against the 33-commit candidate `pr2b/candidate`; local only; nothing sent to `KJ5HST/methodology`

Claimed at his Phase 0 picker: 'PR4: refresh the PR text (Recommended)' (the other offered was the PR3 squash-merge follow-up), with 'Yes, trim 4 to 3 (Recommended)' (done first: the trim `a019bbfd` and the fold `b51364a0`, whose entries sit below; S393 archived, proof exit 0, `HANDOFFS.md` 41,785 B after the fold). Phase 0 (read 2026-10-29, `uptime` load 5.11 at 18:18): the `CHANGELOG.md` frontier = `HEAD` `eaafc5f2` (0 undocumented, 0 merges); the `HANDOFFS.md` frontier `cb3d7fe3` is one commit behind (S396's ledger-only push record, not a session), no pending receipt; `check-ledger` and `check-handoff` exit 0; the newest receipt's gate citation (results `32858fe46628`, manifest `102234f3acf8`) equals `.quality-gates-results.json`; `upstream/main` unchanged `d50ce290` (fetched); #98 open, MERGEABLE, CLEAN (`65990cda`); #96 open, CONFLICTING (`ad5c980f`); each 0 comments, 0 reviews; issues #93, #95, #97 no new activity; dashboard 72/100, 0 high-risk flags. Deliverable: `docs/planning/upstream-pr-body.md` (draft 11, written at the old base: `:8` names `pr2/candidate` at `3cba1e5` over `f34769f`, `:34` and `:91` say 34 commits, `:79` carries S326's PR3 figures) brought to `pr2b/candidate` `47637be2` (33 commits on `upstream/main` `d50ce290`) and S396's `pr3b-record.md`; then the scan for session numbers, backlog codes and coined names; then a fresh reader on a frozen copy. Phase 3F records the rest.

### 2026-10-29 · [ad hoc] S397 fold -- the trim's pointer block leaves `HANDOFFS.md` and one row joins `docs/HANDOFFS_ARCHIVE_INDEX.md`

The block (4 lines, 456 B; `HANDOFFS.md` 42,241 B before, 41,785 B after) became the row `| 1 | 2026-10-28 → 2026-10-28 | HANDOFFS-through-2026-10-28-6.md | v1.8.1 |`. Own commit, as the index's rule says (fork Learning #58). It follows the trim `a019bbfd` (four receipts to three, S393 archived; its proof `bash docs/archive/HANDOFFS-through-2026-10-28-6.md.verify.sh` exit 0), taken at his Phase 0 'Yes, trim 4 to 3 (Recommended)'. Local only; nothing sent to `KJ5HST/methodology`.

### 2026-10-29 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-28-6.md` (1 record(s), 53,957 B → 42,241 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-28 → 2026-10-28) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-28-6.md`](docs/archive/HANDOFFS-through-2026-10-28-6.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-28-6.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-28-6.md.verify.sh)
rather than trusting a digest printed here. Live file 53,957 B → 42,241 B (−21.7%).

### 2026-10-29 · [ad hoc] S396 push -- fork `main` fast-forwarded `44911712..cb3d7fe3` (6 commits); the fork's `origin` only, nothing sent to `KJ5HST/methodology`

At his 'Yes, push to fork origin (Recommended)' (asked during the gate run). Guarded before the push: `git remote get-url origin` was `https://github.com/rmsharp/methodology.git` (the fork), `git ls-remote origin refs/heads/main` equalled `origin/main` (`44911712`), that sha was an ancestor of `main`, and `git rev-list --count origin/main..main` read 6, as expected. Read back after: the remote's `main` is `cb3d7fe3`, equal to local, 0 ahead. `pr2b/candidate` (`47637be2`) and `pr2/candidate` (`3cba1e50`) are local branches and were not pushed.

### 2026-10-29 · [ad hoc] S396 close-out -- PR3, the adopter-impact table, re-run on the rebuilt candidate `pr2b/candidate`; 10 of 12 adopters refuse a plain sync, 52 files; nothing sent to `KJ5HST/methodology`

Closed the S396 claim: the `HANDOFFS.md` receipt `status: complete` (self 8, predecessor S395 scored 9), the record `docs/planning/pr-composition-evidence/pr3b-record.md`, the evidence beneath it. Result: the rebuilt candidate `47637be2` (33 commits on `upstream/main` `d50ce290`) against upstream's tool over the 12 adopters' committed HEADs: 10 of 12 refuse a plain `bin/sync` (S326: 10), 52 files (S326: 39), 51 fork versions and 1 in no history (F19); seeds changed 0; a second plain sync writes 0 at 12 of 12; the two files added since S326 are bytes the old candidate's history carried and the rebuilt one does not. Fourteen of sixteen expectations confirmed (E1 wrong, E15 11 of 12 trees identical). The fork's gates on `0ac3c26b`, clean tree, 14:26:57 to 14:53:05: quality_ratchet: 24/24 pass · 0 fail · 0 unmeasured · results 32858fe46628 · manifest 102234f3acf8, equal to S395's. No row appended to `docs/FORK_LEARNINGS.md`, so D3's retirement duty does not fire. For PR4: `docs/planning/upstream-pr-body.md:79` is the one sentence whose figures change (39 to 52, 38 to 51). The fork's `main` goes to the fork's `origin` only, at his 'Yes, push to fork origin (Recommended)'; the push is recorded in its own entry. Nothing sent to `KJ5HST/methodology`.

### 2026-10-29 · [ad hoc] S396 work -- PR3, the adopter-impact table, re-run on the rebuilt candidate `pr2b/candidate` (`47637be2`, 33 commits on `upstream/main` `d50ce290`): record and the cause of the two added refusals; local only; nothing sent to `KJ5HST/methodology`

`docs/planning/pr-composition-evidence/pr3b-record.md` (the answer, S326's figures against these, the sixteen expectations scored, the instrument checks, what it does not show, the PR4 text and what it leaves open), `pr3b-why-six.py` and `pr3b-why-six-output.txt` (read-only: the adopters' two blobs, `methodology/methodology_trim.py` `24306a82` and `methodology/FRAMEWORK_APPARATUS.md` `7288b952`, sit at one commit each of the OLD candidate `pr2/candidate`, `98ca7fc9` and `04918ce3`, and in no commit of `pr2b/candidate` or `upstream/main`; six adopters, both files). Scored: 14 of 16 confirmed. E1 was wrong (the refused counts at the five unchanged new-layout adopters read 6, not the predicted 4: the added two files are that history effect, not a code change), and E15 read 11 of 12 trees identical (`wsfct`'s own session made a branch during the run). What it leaves for PR4: no number of refused files should be quoted (S326's 38 fork versions is now 51 and moves with the pull request's history); how upstream merges the 33 commits decides which intermediate blobs its history keeps, not measured. The plans are at their size caps, so none carries a status edit; this record does.

### 2026-10-29 · [ad hoc] S396 work (evidence 1 of 2) -- PR3 re-run on the rebuilt candidate: the sixteen expectations (file time 14:16:45, before the run's start at 14:17:12), the script, the report and the rows of one serial run; local only; nothing sent to `KJ5HST/methodology`

`docs/planning/pr-composition-evidence/`: `pr3b-expectations.txt`; `pr3b-adopters.py` (S326's `pr3-adopters.py` with the candidate ref, the output names and the report's heading changed, nothing else); `pr3b-adopters-output.md` and `pr3b-rows.json` (267 s, exit 0, the local ref `pr2b/candidate` `47637be2` against `upstream/main` `d50ce290`, the fork's `main` `6e2b5b45`, the 12 adopters' committed HEADs in `--no-local` clones). Result: 10 of the 12 refuse a plain `bin/sync` (exit 2), 52 files in all, 51 of them fork versions and 1 in no history (`nprcgenekeepr`'s `methodology/methodology_trim.py`, F19); S326's figure was 39; the audit equals the history rule at 12 of 12; seeds changed 0 and created 13 by the candidate (54 by upstream's tool, 41 of them beside a migrated adopter's own folder); a second plain sync writes 0 at 12 of 12; 72 of 72 dry runs leave the clone clean; fixture (a) 30 paths equal, fixture (b) 0 against 19. The fingerprint of the 12 real trees before and after: 11 identical; `wsfct`'s refs differ by a branch its own session created at 14:18:49 (its reflog), HEAD, status and config equal. The record is the next entry.

### 2026-10-29 · [ad hoc] S396 claim (in progress) -- re-run PR3, the adopter-impact table, from the 33-commit candidate `pr2b/candidate`; local only; nothing sent to `KJ5HST/methodology`

Claimed at his Phase 0 picker: 'PR3 adopter table (Recommended)' (the others offered were the PR4 text re-check and an open item), with 'Yes, trim 4 to 3 (Recommended)' (done first: the trim `11ea5f3d` and the fold `83f3aeed`, whose entries sit below; S392 archived, proof exit 0, `HANDOFFS.md` 41,969 B after the fold). Phase 0 (read 2026-10-29, `uptime` load 4.70 at 14:07): the `CHANGELOG.md` frontier = `HEAD` `44911712` (0 undocumented, 0 merges); the `HANDOFFS.md` frontier `37e773e3` is one commit behind (S395's ledger-only push record, not a session), no pending receipt; `check-ledger` and `check-handoff` exit 0; the newest receipt's gate citation (results `32858fe46628`, manifest `102234f3acf8`) equals `.quality-gates-results.json`; `upstream/main` unchanged `d50ce290` (fetched); #98 open, MERGEABLE, CLEAN (`65990cda`); #96 open, CONFLICTING (`ad5c980f`); each 0 comments, 0 reviews; issues #93, #95, #97 no new activity; dashboard 72/100, 0 high-risk flags. Deliverable: S326's `pr3-adopters.py` copied to `pr3b-adopters.py` (names and refs only; the original stays frozen), run once, serially, over the 12 adopters' committed HEADs in `--no-local` clones; the candidate `47637be2` against `upstream/main` `d50ce290`; expectations saved before the run; the real adopter trees fingerprinted before and after. Eight of the 12 adopters have the same HEAD as at S326; four moved (`nprcgenekeepr`, `mts-system`, `vscode_quarto_ext`, `wsfct`). Phase 3F records the rest.

### 2026-10-29 · [ad hoc] S396 fold -- the trim's pointer block leaves `HANDOFFS.md` and one row joins `docs/HANDOFFS_ARCHIVE_INDEX.md`

The block (4 lines, 456 B; `HANDOFFS.md` 42,425 B before) became the row `| 1 | 2026-10-28 → 2026-10-28 | HANDOFFS-through-2026-10-28-5.md | v1.8.1 |`. Own commit, as the index's rule says (fork Learning #58). It follows the trim `11ea5f3d` (four receipts to three, S392 archived), taken at his Phase 0 'Yes, trim 4 to 3 (Recommended)'. Local only; nothing sent to `KJ5HST/methodology`.

### 2026-10-29 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-28-5.md` (1 record(s), 53,924 B → 42,425 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-28 → 2026-10-28) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-28-5.md`](docs/archive/HANDOFFS-through-2026-10-28-5.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-28-5.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-28-5.md.verify.sh)
rather than trusting a digest printed here. Live file 53,924 B → 42,425 B (−21.3%).

### 2026-10-29 · [ad hoc] S395 push -- fork `main` fast-forwarded `7921d0ff..37e773e3` (6 commits); the fork's `origin` only, nothing sent to `KJ5HST/methodology`

At his 'Yes, push to fork origin (Recommended)' (asked during the gate run). Guarded before the push: `git remote get-url origin` was `https://github.com/rmsharp/methodology.git` (the fork), `git ls-remote origin refs/heads/main` equalled `origin/main` (`7921d0ff`), that sha was an ancestor of `main`, and `git rev-list --count origin/main..main` read 6, as expected. Read back after: the remote's `main` is `37e773e3`, equal to local, 0 ahead and 0 behind; the remote holds no `pr2*` branch. `pr2b/candidate` (`47637be2`) and `pr2/candidate` (`3cba1e50`) are local branches and were not pushed.

### 2026-10-29 · [ad hoc] S395 close-out -- PR2b layer 23 built and verified (commit 33 and the printed-text group 28, 29, 30); local `pr2b/candidate` fast-forwarded `fd43f707` to `47637be2`, 33 commits on `upstream/main`, the rebuilt candidate complete; fifteen of sixteen expectations confirmed, none missed; the fork's gates pass 24 of 24; `HANDOFFS.md` trimmed 4 to 3 and folded; nothing sent to `KJ5HST/methodology`

The close-out of the work entries beneath it. **The fork's gates** on `HEAD` `b2052776865d` with a clean tree, one run (11:48:39 to 12:14:16, 25 min 37 s; load 7.54 at its start, after waiting for it to fall from 23): `quality_ratchet: 24/24 pass · 0 fail · 0 unmeasured · results 32858fe46628 · manifest 102234f3acf8`, equal to S394's citation. Re-read at close-out (14:03): `upstream/main` unchanged `d50ce290`, #98 open, MERGEABLE, CLEAN, #96 open, CONFLICTING, each 0 comments and 0 reviews. The receipt is in `HANDOFFS.md` (S395, 53,924 B in all, 11,612 B of room). Local `main` is pushed to the fork's `origin` only, at his 'Yes, push to fork origin (Recommended)', in the entry above this one if it was made; `pr2b/candidate` and `pr2/candidate` are local branches and are not pushed.

### 2026-10-29 · [ad hoc] S395 work -- PR2b layer 23 built and verified: 33 and the printed-text group (28, 29, 30) are four commits on the local `pr2b/candidate`, `fd43f707` to `47637be2` (33 commits on `upstream/main` `d50ce290`); record `docs/planning/pr-composition-evidence/pr2b-layer23-record.md`; nothing sent to `KJ5HST/methodology`

All four were replays (patch-ids equal), 9 files, +99 / −53. Clean-clone verification (`pr2b-layer-driver.sh 23`, 22 min 3 s): ratchet 18/18, 0 unmeasured, `dashboard-unit-tests` 397 against its floor of 397, shell suite 302 / 0 / 0, the inertness proof over 28 to 30 holds (and over the whole layer refuses, as designed, because 33 adds test code), scanner and budget unchanged, `--reverify` and four `check-links` forms exit 0. Merges clean with `upstream/main`; #98 5 regions and #96 4, 0 added; fork-token lines 17 in 5 files (the plan's figure). The plan's tree criterion (`866ea59c8738` plus 26′'s edits) was checked after the fact by rebuilding that tree (`pr2b-layer23-treecheck.sh`): it holds, patch-id `97131e63dc6a` on both sides. Expectations: fifteen of sixteen confirmed and the sixteenth, the branch move, done; none missed. This entry follows the evidence commit `e1d8169e`; the close-out entry follows the fork's gate run.

### 2026-10-29 · [ad hoc] S395 work (evidence 1 of 2) -- PR2b layer 23: the sixteen expectations (file time 11:08:04, before the build script's first line at 11:08:29), the build output, the clean-clone verification output and the measurements against `upstream/main` and the two open heads, under `docs/planning/pr-composition-evidence/`; local only; nothing sent to `KJ5HST/methodology`

Four files and this entry (the 5-file cap). The layer is `pr2b/candidate` `fd43f707` to `47637be2` (33, 28, 29, 30, each `git cherry-pick -x`, patch-ids equal), already moved by `git update-ref` with the old value guarded; the record, the tree check and the work entry follow in the next commit.

### 2026-10-29 · [ad hoc] S395 claim (in progress) -- build PR2b layer 23 (series commits 33, 28, 29 and 30) in a scratch clone onto the local `pr2b/candidate`; local only; nothing sent to `KJ5HST/methodology`

Claimed at his Phase 0 picker: 'Build layer 23 (Recommended)' (the others offered were the third BL-94 paid run and the three adopter ledgers with real defects), with 'Yes, trim 4 to 3 (Recommended)' (done first: the trim `b4c303a1` and the fold `16cdc96d`, whose entries sit below; S391 archived, proof exit 0, `HANDOFFS.md` 41,880 B after the fold). Phase 0 (read 2026-10-29, `uptime` load 2.43 at 10:26): the `CHANGELOG.md` frontier = `HEAD` `7921d0ff` (0 undocumented, 0 merges); the `HANDOFFS.md` frontier `c413d0fd` is one commit behind (S394's ledger-only push record, not a session), no pending receipt; `check-ledger` and `check-handoff` exit 0; the newest receipt's gate citation (results `32858fe46628`, manifest `102234f3acf8`) equals `.quality-gates-results.json`; `upstream/main` unchanged `d50ce290` (fetched); #98 open, MERGEABLE, CLEAN (`65990cda`); #96 open, CONFLICTING (`ad5c980f`); each 0 comments, 0 reviews; issues #93, #95, #97 no new activity; dashboard 72/100, 0 high-risk flags (its one history line rides this claim); `pr2b/candidate` 29 commits on `upstream/main`. The close-out entry follows when the layer is built.

### 2026-10-29 · [ad hoc] S395 fold -- the trim's pointer block leaves `HANDOFFS.md` and one row joins `docs/HANDOFFS_ARCHIVE_INDEX.md`

The block (4 lines, 456 B; `HANDOFFS.md` 42,336 B before) became the row `| 1 | 2026-10-28 → 2026-10-28 | HANDOFFS-through-2026-10-28-4.md | v1.8.1 |`. Own commit, as the index's rule says (fork Learning #58). It follows the trim `b4c303a1` (four receipts to three, S391 archived), taken at his Phase 0 'Yes'. Local only; nothing sent to `KJ5HST/methodology`.

### 2026-10-29 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-28-4.md` (1 record(s), 53,624 B → 42,336 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-28 → 2026-10-28) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-28-4.md`](docs/archive/HANDOFFS-through-2026-10-28-4.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-28-4.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-28-4.md.verify.sh)
rather than trusting a digest printed here. Live file 53,624 B → 42,336 B (−21.1%).

### 2026-10-29 · [ad hoc] S394 push -- fork `main` fast-forwarded `d84ec98c..c413d0fd` (7 commits); the fork's `origin` only, nothing sent to `KJ5HST/methodology`

At his 'Yes, push to fork origin (Recommended)' (asked during the gate run). Guarded before the push: `git ls-remote origin refs/heads/main` equalled `origin/main` (`d84ec98c`), that sha was an ancestor of `main`, and `git rev-list --count origin/main..main` read 7, as expected. Read back after: the remote's `main` is `c413d0fd`, equal to local, 0 ahead; the remote holds no `pr2*` branch. `pr2b/candidate` (`fd43f707`) and `pr2/candidate` (`3cba1e50`) are local branches and were not pushed.

### 2026-10-29 · [ad hoc] S394 close-out -- PR2b layer 22 built and verified (the documentation group: series 21 to 25, a hand-written 26-prime, 27 and 32); local `pr2b/candidate` fast-forwarded `d818ca17` to `fd43f707`, 29 commits on `upstream/main`; twelve of fourteen expectations confirmed; the fork's gates pass 24 of 24 on the second run (the first read 22 of 24); `HANDOFFS.md` trimmed 4 to 3 and folded; nothing sent to `KJ5HST/methodology`

The close-out of the work entries beneath it. **The fork's gates** on `HEAD` `70d90331` with a clean tree: the first run (00:55:59 to 01:27:03, load 46.8 at its start) read 22/24 with one shell-suite test red (`tests-sh-passed` 691 against its floor of 692), and the ratchet keeps no output, so the test is unnamed; a direct `bash bin/tests.sh` on the same `HEAD` read 692 passed, 0 failed, 0 skipped; the re-run (01:38:27 to 02:04:56) read `quality_ratchet: 24/24 pass · 0 fail · 0 unmeasured · results 32858fe46628 · manifest 102234f3acf8`, equal to S393's citation. The first run's red is not reproduced and its cause is unproven. The receipt is in `HANDOFFS.md` (S394, 53,624 B in all). Local `main` is pushed to the fork's `origin` only, at his 'Yes, push to fork origin (Recommended)', in the entry above this one if it was made; `pr2b/candidate` and `pr2/candidate` are local branches and are not pushed.

### 2026-10-29 · [ad hoc] S394 correction -- `pr2b-grouping-plan.md` §5, layer 22's verify column, said the fork-token count would read "639 → 33 less 26-prime's reach"; it reads 60 in 11 files at that layer and 17 in 5 only after layer 23

The 33 was measured after all eleven commits, including the printed-text commits 28 to 30 that sit in layer 23. One phrase replaced (37 B for 45 B; the file is 13,989 B of its declared 14,000). Found by the layer's own measurement (`pr2b-layer22-build-output.txt:93` and `:144`). Local only; nothing sent to `KJ5HST/methodology`.

### 2026-10-29 · [ad hoc] S394 work -- PR2b layer 22 built and verified: the documentation group (series 21 to 25, a hand-written 26-prime, 27, 32) is eight commits on the local `pr2b/candidate`, `d818ca17` to `fd43f707` (29 commits on `upstream/main` `d50ce290`); record `docs/planning/pr-composition-evidence/pr2b-layer22-record.md`; nothing sent to `KJ5HST/methodology`

Built in a scratch `--no-local` clone and fetched here fast-forward only, `d818ca17` checked to be an ancestor first; `pr2/candidate` (`3cba1e50`) untouched. Seven commits are `git cherry-pick -x` replays, each patch-id equal to its original; **26-prime** (`d9f583c3`, 2 files, +18 / -18, comments and docstrings of the trimmer and its tests) is hand-written because series commit 26 conflicts in five regions on this tip; he saw its whole diff and answered 'Yes, as shown (Recommended)'; one strict line (`tools/test_methodology_trim.py:4622`, the trimmer's own `P1`) is left on purpose. **Verified in a clean clone** (`pr2b-layer-driver.sh 22`, 21 min 40 s): ratchet 18/18 pass, 0 fail, 0 unmeasured, results `a2482a2d9ae3` (equal to layers 20 and 21), manifest `09a751d541b8`; `bin/tests.sh` 302 passed; the inertness proof over the layer HOLDS (27 files, +650 / -687); budget unchanged; `check-links` four forms exit 0. **Measured:** clean with `upstream/main`; #98 5 regions in 3 files and #96 4 regions in 3, both unchanged (0 added); layer 23's commits 28, 29, 30 and 33 are each clean alone on the new tip; fork-token lines 60 in 11 files at the layer, 17 in 5 once layer 23's four are added. **Expectations:** twelve of fourteen confirmed; E4 (I quoted the whole-series token figure for a layer that lacks the printed-text commits) and E13 (21 min 40 s against 22 to 30) missed. The close-out entry follows.

### 2026-10-29 · [ad hoc] S394 work (evidence 1 of 2) -- PR2b layer 22: the fourteen expectations (file time 00:21:50, before the first pick at 00:21:56), the 26-prime edit script, the build output and the clean-clone verification output, under `docs/planning/pr-composition-evidence/`; local only; nothing sent to `KJ5HST/methodology`

Files `pr2b-layer22-expectations.txt`, `pr2b-layer22-26prime-edits.py`, `pr2b-layer22-build-output.txt` and `pr2b-layer22-verify-output.txt`. The verification (`pr2b-layer-driver.sh 22`, 00:28:25 to 00:50:05, 21 min 40 s, load about 4) read the ratchet 18/18 pass, 0 fail, 0 unmeasured, results `a2482a2d9ae3`, manifest `09a751d541b8`, and `bin/tests.sh` 302 passed, 0 failed, 0 skipped. The record and the measurements are the next commit, with its own entry above this one.

### 2026-10-29 · [ad hoc] S394 claim (in progress) -- build PR2b layer 22, the documentation group (series 21 to 25, a hand-written 26-prime, 27 and 32), in a scratch clone onto the local `pr2b/candidate`; local only; nothing sent to `KJ5HST/methodology`

Claimed at his Phase 0 picker: 'Build layer 22 (Recommended)' (the others offered were the three adopter ledgers with real defects and a local rebase of #96), with 'Yes, trim 4 to 3 (Recommended)' (done first: the trim `ac873475` and the fold `c626df26`, whose entries sit below; S390 archived, proof exit 0, `HANDOFFS.md` 42,002 B). Phase 0 (read 2026-10-29, `uptime` load 24.58 at 00:17): the `CHANGELOG.md` frontier = `HEAD` `d84ec98c` (0 undocumented, 0 merges); the `HANDOFFS.md` frontier `f72710fd` is one commit behind (S393's ledger-only push record, not a session), no pending receipt; `check-ledger` and `check-handoff` exit 0; the newest receipt's gate citation (results `32858fe46628`, manifest `102234f3acf8`) equals `.quality-gates-results.json`; `upstream/main` unchanged `d50ce290` (fetched); #98 open, MERGEABLE, CLEAN (`65990cda`); #96 open, CONFLICTING (`ad5c980f`); each 0 comments, 0 reviews; issues #93, #95, #97 no new activity; dashboard 72/100, 0 high-risk flags (its one history line rides this claim); `pr2b/candidate` `d818ca17`, `pr2/candidate` `3cba1e50`. The close-out entry follows when the layer is built.

### 2026-10-29 · [ad hoc] S394 fold -- the trim's pointer block leaves `HANDOFFS.md` and one row joins `docs/HANDOFFS_ARCHIVE_INDEX.md`

The block (4 lines, 456 B; `HANDOFFS.md` 42,458 B before) became the row `| 1 | 2026-10-28 → 2026-10-28 | HANDOFFS-through-2026-10-28-3.md | v1.8.1 |`. Own commit, as the index's rule says (fork Learning #58). It follows the trim `ac873475` (four receipts to three, S390 archived), taken at his Phase 0 'Yes'. Local only; nothing sent to `KJ5HST/methodology`.

### 2026-10-29 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-28-3.md` (1 record(s), 53,928 B → 42,458 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-28 → 2026-10-28) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-28-3.md`](docs/archive/HANDOFFS-through-2026-10-28-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-28-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-28-3.md.verify.sh)
rather than trusting a digest printed here. Live file 53,928 B → 42,458 B (−21.3%).

### 2026-10-28 · [ad hoc] S393 push -- fork `main` fast-forwarded `69d1a104..f72710fd` (7 commits); the fork's `origin` only, nothing sent to `KJ5HST/methodology`

At his Phase 0 'Yes, push to fork origin'. Guarded: `origin` is `https://github.com/rmsharp/methodology.git`, the remote's `main` read `69d1a104` by `ls-remote` and is an ancestor of `main`, the ahead count was 7 as expected; a plain `git push origin main`, no force. Read back: `ls-remote` now `f72710fd` = local `main`, ahead count 0. The seven are the two S392 receipt corrections (`6fe6bc02`, `a22e8165`) and this session's trim, fold, claim, work and close-out. This record is a `CHANGELOG.md`-only commit pushed to `origin` under his standing grant.

### 2026-10-28 · [ad hoc] S393 close-out -- PR2b grouping plan written, measured and decided (his D1, D2, D3 each as recommended: documentation group = commits 21 to 27 and 32, two layers, leftovers named in the pull request's text); nothing built, `pr2b/candidate` still `d818ca17`; the fork's gates pass 24 of 24; `HANDOFFS.md` trimmed 4 to 3 and folded; nothing sent to `KJ5HST/methodology`

Plan `docs/planning/pr-composition-evidence/pr2b-grouping-plan.md` (13,981 B of its declared 14,000; status DECIDED) with `pr2b-grouping-measure.py`, `pr2b-grouping-measure-output.txt` and `pr2b-grouping-derive-after-output.txt`; work commit `8a42e366f311`, the claim `cafc8d845b8f`, the trim `31d3abe8ff5b` and the fold `c5897b6ced0c`. Layer 22 (the documentation group: 21 to 25, a hand-written 26, 27, 32) is the next build; layer 23 is 33 then 28 to 30 (plan section 5). The fork's gates on `HEAD` `8a42e366f311` with a clean tree, 22:41:30 to 23:05:44 (24 min 14 s): quality_ratchet: 24/24 pass · 0 fail · 0 unmeasured · results 32858fe46628 · manifest 102234f3acf8, equal to S392's citation (`tests-sh-passed` 692 at its floor). Local until the close-out push, which his 'Yes, push to fork origin' covers for the fork's `origin` only.

### 2026-10-28 · [ad hoc] S393 work -- PR2b grouping plan written and measured: `docs/planning/pr-composition-evidence/pr2b-grouping-plan.md` (13,948 B, DRAFT, waiting for his answers D1 to D3), with the script `pr2b-grouping-measure.py`, its output and `pr2b-grouping-derive-after-output.txt`; nothing built, `pr2b/candidate` still `d818ca17`, nothing sent to `KJ5HST/methodology`

Measured in a throwaway `--no-local` clone (second run saved, load average 103 at its start and 61 at its end): the twelve remaining commits are, by comparison of their own before and after, **21 to 25, 27 and 32 comments, docstrings and gate-reason text only; 26 the same, but it conflicts (5 regions, the tip's trimmer is 1.9.0); 28 and 29 string literals; 30 shell lines and one gate reason; 33 code** (two upstream tests restored, gate floor 395 to 397). Alone 9 of 12 apply clean; **in order 11 of 12 apply clean, each patch-id equal to its original, only 26 conflicts**; the three orders containing all eleven give one tree, `866ea59c8738`; 30 needs 22 and 33 needs 27 (pair tests clean). `scrub-proof.py` holds over the scrub-only range and fails over a range containing 33, in exactly 33's two files. Fork-token lines **639 in 28 files at the tip, 33 in 6 after the eleven** (17 for a hand-written 26′, 11 in a frozen fixture whose ids upstream's trimmer already carries, 5 left on purpose). The eleven add no conflict regions to #98 (5 in 3 files) or #96 (4 in 3); the read-set budget is unchanged; the dashboard suite at the replayed tip runs 397 tests, OK. **Recommendation G3:** layer 22 the documentation group (21 to 25, 26′, 27, 32), layer 23 commit 33 then 28 to 30 (B last, a removable tail). Phase 0 also made the trim `31d3abe8` and fold `c5897b6c` (entries below). His decisions D1 (where the documentation line sits), D2 (one, two, three or twelve layers) and D3 (the leftovers) are asked in the close-out report.

### 2026-10-28 · [ad hoc] S393 claim (in progress) -- a planning session: the grouping plan for the candidate's twelve remaining commits (21 to 30, 32, 33), as one record under `docs/planning/pr-composition-evidence/`; nothing is built; local only; nothing sent to `KJ5HST/methodology`

Claimed at his Phase 0 picker: 'Grouping plan for commits 21-33 (Recommended)' (the others offered were one scrub layer of the nine clean commits, commit 21 alone as layer 22, and an open item), with 'Yes, trim 4 to 3 (Recommended)' (done first: the trim `31d3abe8` and the fold `c5897b6c`, whose entries sit below; S389 archived, proof exit 0, `HANDOFFS.md` 41,756 B) and 'Yes, push to fork origin (Recommended)' for the two local commits `6fe6bc02` and `a22e8165` (to be made after the close-out commit, guarded, then recorded in a `CHANGELOG.md`-only entry). Phase 0 (read 2026-10-28, `uptime` load 64.83 at 22:20, from other projects' `vitest` processes): the `CHANGELOG.md` frontier = `HANDOFFS.md` frontier = `HEAD` `a22e8165` (0 undocumented commits, 0 merges, no pending receipt); `check-ledger` and `check-handoff` exit 0; `upstream/main` unchanged at `d50ce290` (fetched); #98 open, MERGEABLE, CLEAN (head `65990cda`) and #96 open, CONFLICTING (head `ad5c980f`, the `merge=union` gap), each with 0 comments and 0 reviews; issues #93, #95 and #97 with no new activity; dashboard 72/100, 0 high-risk flags (the refresh added one snapshot line to `dashboard_history.jsonl`, committed with this claim). Order of work: measure before grouping (the 12 commits' touch sets, their pairwise overlaps, what each conflicts with at the tip and with the open heads, the read-set budget at the tip), draft the groups with the question for him, check every figure against its output, close out.

### 2026-10-28 · [ad hoc] S393 fold -- the trim's pointer block leaves `HANDOFFS.md` and one row joins `docs/HANDOFFS_ARCHIVE_INDEX.md`

The block (4 lines, 456 B; `HANDOFFS.md` 42,212 B before, 41,756 B after) became the row `| 1 | 2026-10-28 → 2026-10-28 | HANDOFFS-through-2026-10-28-2.md | v1.8.1 |` (122 B). Own commit, as the index's rule says (fork Learning #58). It follows the trim `31d3abe8` (four receipts to three, S389 archived), taken at his Phase 0 'Yes'. Local only; nothing sent to `KJ5HST/methodology`.

### 2026-10-28 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-28-2.md` (1 record(s), 53,869 B → 42,212 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-28 → 2026-10-28) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-28-2.md`](docs/archive/HANDOFFS-through-2026-10-28-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-28-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-28-2.md.verify.sh)
rather than trusting a digest printed here. Live file 53,869 B → 42,212 B (−21.6%).

### 2026-10-28 · [ad hoc] S392 receipt figures -- the room stated in the correction below is 103 B short: `HANDOFFS.md` is 53,869 B (11,667 B of room), not 53,972 B (11,564 B)

The correction entry below and the first version of next_steps (2) quoted the file size from before that same correction shortened two phrases of the receipt by 103 B. The S392 receipt now says 53,869 B and 11,667 B (`bin/check-handoff` prints the same). The entry below is left as written (a committed entry is never edited; my first attempt to amend it was refused by the ledger hook and I did not bypass the hook). Local only.

### 2026-10-28 · [ad hoc] S392 receipt correction -- next_steps (2) now says S393's receipt must fit the 11,564 B of room or a required Yes/No trims 4 to 3 first

The close-out receipt said no trim is needed at S393's Phase 0 (four receipts, the rule is above four) and left out that `HANDOFFS.md` is 53,972 B of 65,536 B, so S393's receipt (about 12,000 B at the usual size) would have passed the ceiling that `bin/check-handoff` fails. Found when writing the memory note for it. The text of next_steps (2) is replaced, and two phrases in the same receipt are shortened to keep it under the 12,288 B record budget. Local only: the commit is not pushed (the push he approved, and its record, were the two commits before this one).

### 2026-10-28 · [ad hoc] S392 push -- fork `main` fast-forwarded `b4daa23f..a2b55b34` (6 commits: S392's trim and its fold, the claim, its two work commits and its close-out); fork `origin` only

At his answer 'Yes, push to fork origin (Recommended)', asked during the gate run. Guarded before the push: `git ls-remote origin refs/heads/main` and `origin/main` both `b4daa23f`, that sha an ancestor of `main`, `main` 6 ahead and 0 behind, tree clean. After it: `git ls-remote origin refs/heads/main` = `main` = `a2b55b34`, 0 ahead and 0 behind; `git ls-remote origin 'refs/heads/pr2*'` is empty, so `pr2b/candidate` (`d818ca17`) and `pr2/candidate` (`3cba1e50`) are local branches and were not pushed. Pushed `main` only. Nothing sent to `KJ5HST/methodology`.

### 2026-10-28 · [ad hoc] S392 close-out -- PR2b layer 21 built and verified in a clean clone, green on every line including the read-set budget: the candidate's commit 20 added alone to local `pr2b/candidate` (`d818ca17`); the fork's gates pass 24 of 24; HANDOFFS.md trimmed 5 to 3 and folded; nothing sent to `KJ5HST/methodology`

Deliverable: series commit 20 `5afc9621` (the unmeasured-gate prose in `HOW_TO_USE.md` and `starter-kit/HANDOFFS.md`, 2 files, +5 / -2) replayed verbatim as `d818ca17` on `pr2b/candidate` (21 commits on `upstream/main` `d50ce290`), patch-id `7bb5a98f511f` equal to the original. Verified once at its tip in a clean clone (ratchet 18/18, 0 unmeasured, both digests equal to layer 20's; `bash bin/tests.sh` 302 / 0 / 0; `--reverify`, the tracked proof, the budget and `check-links` in four forms all exit 0); fourteen expectations written first, all confirmed. The fork's own gates on `HEAD` `204e89f7` with a clean tree: 24/24 pass, 0 fail, 0 unmeasured, results `32858fe46628`, manifest `102234f3acf8`, `tests-sh-passed` 692 at its floor, 24 min 53 s. Receipt: S392 in `HANDOFFS.md` (self 8, predecessor S391 scored 9; Phase 3C appended no row to `docs/FORK_LEARNINGS.md`, so D3's retirement duty does not fire). Next: his pick at the S393 picker (the grouping plan for commits 21 to 33, or a scrub group); the push to fork `origin` he approved follows this commit and gets its own entry. Nothing sent to `KJ5HST/methodology`.

### 2026-10-28 · [ad hoc] S392 work (2 of 2) -- PR2b layer 21 record: all fourteen expectations confirmed (the second half of E14, the fork's own gate run, is scored at close-out); the runner's 3E sentence is confirmed as a decided seam, not a finding; the next-alone run for commits 21 to 33 saved; fork only, nothing sent upstream

`docs/planning/pr-composition-evidence/pr2b-layer21-record.md` (7 sections) and `pr2b-layer21-next-alone-output.txt`. The record's one check beyond the expectations: after this layer `HOW_TO_USE.md` and `starter-kit/HANDOFFS.md` carry the unmeasured-gate rule and `starter-kit/SESSION_RUNNER.md` does not (0 hits at `d818ca17`, at `upstream/main` and at `pr2/candidate`; 1 on the fork's `main`, commit `95005e87`, in neither open pull request). It is plan decision D6 answer (a), built at S323 as two of the three hunks because the runner is over its read-set ceiling (`docs/planning/upstream-pr-composition-plan.md:243`), so it is recorded as the plan's accepted seam. One slip, caught by its own guard: the first fast-forward guard asked `git merge-base --is-ancestor` before the new commit had been fetched into the fork repository and read the missing object as "not an ancestor", so it stopped with nothing changed; the second ordering fetches to a temporary ref first (the record's section 7 says so). Nothing sent to `KJ5HST/methodology`.

### 2026-10-28 · [ad hoc] S392 work (1 of 2) -- PR2b layer 21 built and verified in a clean clone, green on every line: the candidate's commit 20 (`5afc9621`) replayed as `d818ca17` on local `pr2b/candidate`; expectations, build, clean-clone run and measure saved; fork only, nothing sent upstream

One `git cherry-pick -x` in a scratch `--no-local` clone, exit 0, equal to its original by `git patch-id --stable` (`7bb5a98f511f`); 2 files, +5 / -2 (`HOW_TO_USE.md`, `starter-kit/HANDOFFS.md`). Fourteen expectations written first (file mtime 20:10:22, cherry-pick 20:10:27). Cheap suites first (layout 76, checker 11, sync 82, dashboard 395, the migration suite's fast classes 95, all OK). Verified (`d818ca17`, clean clone, serial, hooks not armed, `pr2b-layer-driver.sh 21`, 20:12:34 to 20:35:58, 23 min 24 s): ratchet 18/18, 0 fail, 0 unmeasured, results `a2482a2d9ae3`, manifest `4669bce5b261` (both equal to layer 20's); `bash bin/tests.sh` 302 / 0 / 0, Test 15 `(30 == 30)`; `--reverify` exit 0; scanner 15 files, 0 sites, 138 acknowledged (equal to the parent's); budget exit 0; `check-links` exit 0 in all four forms, 80 links. Branch operation: `pr2b/candidate` fast-forwarded `4e07877f` to `d818ca17` (21 commits on `upstream/main` `d50ce290`) after fetching the commit in and checking the old tip is its ancestor; `pr2/candidate` (`3cba1e50`) untouched. Measured: clean with `upstream/main`, 5 regions with #98 and 4 with #96 (0 added), scrub regex 0 of 5 added lines; commits 21 to 33 alone: 10 of 13 clean (nine of the twelve real ones, 31 is already in), the same split as at layer 20. Four evidence files: `pr2b-layer21-expectations.txt`, `-build-output.txt`, `-verify-output.txt`, `-measure-output.txt`. Nothing sent to `KJ5HST/methodology`.

### 2026-10-28 · [ad hoc] S392 claim (in progress) -- PR2b layer 21: add the candidate's commit 20 (`5afc9621`, `HOW_TO_USE.md` and `starter-kit/HANDOFFS.md`) alone to the local branch `pr2b/candidate` (`4e07877f`) in a scratch clone, and check it at its tip in a clean clone; local only; nothing sent to `KJ5HST/methodology`

Claimed at his Phase 0 picker: 'Add commit 20 alone (Recommended)' (the others offered were the grouping plan for commits 21 to 33 and a scrub group), after 'Yes, trim 5 to 3 (Recommended)' for `HANDOFFS.md` (done first, as the trim `9d477fd9` and the fold `7a9ec9a7`, whose entries sit below). No push to fork `origin` was asked at this Phase 0, so none will be made without asking. Phase 0 (read 2026-10-28, `uptime` load 5.91): the `CHANGELOG.md` frontier = `HEAD` `b4daa23f` (0 undocumented commits, 0 merges); the `HANDOFFS.md` frontier `1f99d19d` one commit behind (S391's ledger-only push record, not a session); no pending receipt; `check-ledger` and `check-handoff` exit 0; the gate citation (`results 32858fe46628`, `manifest 102234f3acf8`, 24/24) equal to the local `.quality-gates-results.json` (compared, not re-run); `upstream/main` unchanged at `d50ce290` (fetched); #98 open, MERGEABLE, CLEAN (head `65990cda`) and #96 open, CONFLICTING (head `ad5c980f`, the `merge=union` gap), each with 0 comments and 0 reviews; issues #93, #95 and #97 with no new activity; fork `origin/main` = `main` at the start; dashboard 72/100, 0 high-risk flags. Order of work: read the read-set budget at the tip and the commit's real overlap with the open heads from the repository root, write the expectations with confidence before the cherry-pick, replay, run the cheap suites, verify in a clean clone with `pr2b-layer-driver.sh`, record, close out.

### 2026-10-28 · [ad hoc] S392 fold -- the trim's pointer block leaves `HANDOFFS.md` and one row joins `docs/HANDOFFS_ARCHIVE_INDEX.md`

The block (4 lines, 448 B; `HANDOFFS.md` 42,362 B before, 41,914 B after) became the row `| 2 | 2026-10-27 → 2026-10-28 | HANDOFFS-through-2026-10-28.md | v1.8.1 |` (120 B). Own commit, as the index's rule says (fork Learning #58). It follows the trim `9d477fd9` (five receipts to three, S388 and S387 archived), taken at his Phase 0 go-ahead (a required Yes/No question, 'Yes, trim 5 to 3'); the dry run named the shard `HANDOFFS-through-2026-10-28.md` and the cut size exactly (65,066 B to 42,362 B), the proof exited 0, and I ran the `--write` myself. Nothing sent to `KJ5HST/methodology`.

### 2026-10-28 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-28.md` (2 record(s), 65,066 B → 42,362 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-10-27 → 2026-10-28) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-28.md`](docs/archive/HANDOFFS-through-2026-10-28.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-28.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-28.md.verify.sh)
rather than trusting a digest printed here. Live file 65,066 B → 42,362 B (−34.9%).

### 2026-10-28 · [ad hoc] S391 push -- fork `main` fast-forwarded `85da5d21..1f99d19d` (4 commits: S391's claim, its two work commits and its close-out); fork `origin` only

At his Phase 0 answer 'Yes, push to fork origin (Recommended)'. Guarded before the push: `git ls-remote origin refs/heads/main` and `origin/main` both `85da5d21`, that sha an ancestor of `main`, `main` 4 ahead and 0 behind. After it: `git ls-remote origin refs/heads/main` = `main` = `1f99d19d`, 0 ahead and 0 behind; `git ls-remote origin 'refs/heads/pr2*'` is empty, so `pr2b/candidate` (`4e07877f`) and `pr2/candidate` (`3cba1e50`) stay local. Nothing sent to `KJ5HST/methodology`. This entry is the CHANGELOG-only push record, which goes to fork `origin` under his standing grant.

