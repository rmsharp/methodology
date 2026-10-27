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

---

## 2026-09

## 2026-10

### 2026-10-27 · [ad hoc] S377 close-out -- PR2b layer 1 built and verified: Part 1 rebuilt on `upstream/main` `d50ce290` as local branch `pr2b/candidate` (`fbcef390`); fork `main` pushed and `CHANGELOG.md` trimmed at his go-aheads; nothing sent to `KJ5HST/methodology`

Phase 3 of the session whose claim stands below (`CHANGELOG: pending` is resolved by this entry and the entries between). **Deliverable:** PR2b layer 1 (work `b98839efabbf`, below). **Also done, each at his Phase 0 tick and each with its own entry:** the push of fork `main` (`b52d6a15..eee1e83e`) and the `--force` trim of `CHANGELOG.md` (`02d77867`, 224,389 B to 99,389 B, shard `docs/archive/CHANGELOG-through-2026-10-23.md`). **3A:** S376's handoff scored **9** (every anchor re-checked; the trim arithmetic, the forced trim, #98 and the trimmer reading held; it left 'layer 1' unspanned and did not say two rows of the PR2 check list cannot run at an early layer). **3B:** self-score **8** (the scope of 'layer 1' chosen without asking; one unneeded directory listing). **3C:** no row appended to `docs/FORK_LEARNINGS.md`, so D3's retirement duty does not fire and no row was adjudicated; the lesson (a 'take their side' reading is checked by resolving every region to that side and diffing the whole file) went to auto-memory. **3D:** the `HANDOFFS.md` receipt is complete (`status: complete`, 10,291 B, 5 receipts in the file, 56,325 B of 65,536 B); S378's Phase 0 trims two. **3E:** `quality_ratchet.py --run` in a clean `--no-local` clone of `b98839efabbf`, hooks set, serial: **24/24 pass · 0 fail · 0 unmeasured · results 32858fe46628 · manifest 102234f3acf8** (`tests-sh-passed` 692, equal to S376's run; its results file installed in the ignored `.quality-gates-results.json`). On the final tree, by hand: `check-links`, `check-backlog-anchors` and `check-learnings` exit 0, the plan 29,992 B of 30,000 B (not edited); `check-ledger` and `check-handoff` (plain and `--all`) are re-run before the close-out commit. `upstream/main` unchanged at `d50ce290`; #98 open and MERGEABLE, #96 open, each 0 comments. The auto-memory index was compacted at a hook's request (the claims section moved to `index_claims_counts_and_measurement.md`, 32 entries, no link lost). Unpushed: the trim, claim, work and this close-out (4 commits); pushing them is his go-ahead.

### 2026-10-26 · [ad hoc] S377 work -- PR2b layer 1 built and verified: Part 1 rebuilt as one commit on `upstream/main` `d50ce290` (local branch `pr2b/candidate`, `fbcef390`, 6 files, +6,187 / -552); all 28 conflict regions resolve to upstream's side; green in a clean clone; fork only, nothing sent upstream

In a scratch `--no-local` clone, `git cherry-pick -n bbe0dc35` onto `d50ce290` stopped on 28 regions in 4 files (the trimmer 13, its tests 13, `FRAMEWORK_APPARATUS.md` 1, `.quality-gates.json` 1), the figure the sizing record gave for commit 1. Each file's regions were resolved to upstream's side and the result compared with upstream's own file (`pr2b-layer1-resolve.py`): equal for the trimmer, its tests and the apparatus, so those three drop out of the layer; the gates file differs by two cleanly merged thresholds (`tests-sh-passed` 261 to 271, `dashboard-unit-tests` 229 to 354), which the verification re-derived and found exact. `trimmer-unit-tests` stays at upstream's 227. What the layer carries is the dashboard (both copies, 2.21.0) and its tests, the `bin/tests.sh` blocks, the `BOOTSTRAP.md` row and the two thresholds. Verified by `layer-verify.sh`, serial, in clean `--no-local` clones of commit `5f202458` and of the base: `bash bin/tests.sh` run directly **271 passed, 0 failed, 0 skipped**; `quality_ratchet.py --run` **12/12 pass · 0 fail · 0 unmeasured · results e658e1a02647 · manifest 84815aa7e6e5** (the base reads 12/12 at 261 and 229); the one shipped `.verify.sh` exits 0 on both; the budget gate exits 0; `git merge-tree --write-tree upstream/main pr2b/candidate` exits 0. Two checks of the PR2 row do not apply at this layer and are recorded as not applicable, not as passed: `bin/check-links --layout both` (the flag arrives with candidate commit 9; it exits 2 here) and `bin/check-layout-literals` (arrives with commit 2). The commit message was then amended (`5f202458` to `fbcef390`); the tree `aafbe533` is the same before and after. The branch ref `pr2b/candidate` was created in this repository by fetching it from the scratch clone (a branch op; no upstream is configured, so a bare `git push` cannot send it); `pr2/candidate` (`3cba1e50`) is untouched. Files: `docs/planning/pr-composition-evidence/pr2b-layer1-record.md`, `pr2b-layer1-resolve.py`, `pr2b-layer1-resolve-output.txt`, `pr2b-layer1-verify-output.txt`. The plan was not edited (29,992 B of 30,000 B). Nothing was sent to `KJ5HST/methodology`.

### 2026-10-26 · [ad hoc] S377 claim (in progress) -- PR2b layer 1: rebuild Part 1 of the pull-request branch (the candidate's commit `bbe0dc35`) on `upstream/main` `d50ce290` in a scratch clone and check it there; local only; nothing sent to `KJ5HST/methodology`

Claimed at his Phase 0 picker: the recommended option, 'PR2b layer 1' (the others offered were BL-114, the fix for the maintainer's issue #95, and waiting on #98 and #96), with two go-aheads ticked, both already done and logged: the push of fork `main` (`b52d6a15..eee1e83e`, entry below) and a `--force` trim of `CHANGELOG.md` (commit `02d77867`: 101 of 158 records, 2026-10-20 to 2026-10-23, into `docs/archive/CHANGELOG-through-2026-10-23.md`, 224,389 B to 99,389 B; the trimmer's SRF_RED at 1.1921 forced past; the shard proof and `check-ledger` exit 0; its own entry is the trimmer's, below the push entry). Phase 0 (read 2026-10-26) found both frontiers at `eee1e83e`, which is `HEAD` (0 undocumented commits, 0 merges, no pending receipt), `check-ledger` and `check-handoff` exit 0, S376's gate citation (`results 32858fe46628`) equal to the local `.quality-gates-results.json`, `upstream/main` unchanged at `d50ce290`, #98 open and CLEAN (head `65990cda`) and #96 open (CONFLICTING is the `merge=union` gap), each with 0 comments and 0 reviews, issues #93, #95 and #97 open and unchanged, dashboard 72/100 with 0 high-risk flags, and `HANDOFFS.md` at 4 receipts (so no handoff trim this session; this claim makes five, and S378's Phase 0 trims two). The deliverable is plan row PR2b's first layer, which I read as the plan's Part 1: commit 1 of the candidate, `bbe0dc35` (9 files), rebuilt as one commit on `d50ce290` in a scratch `--no-local` clone, the candidate `pr2/candidate` (`3cba1e50`) kept. Commits 2 to 4 are Part 2 layers and each is its own session. S376's sizing record reads the trimmer and its tests as upstream's already (their 26 regions) and the `FRAMEWORK_APPARATUS.md` and `.quality-gates.json` hunks as the two to read; this session reads each region before relying on that. Then the PR2 row's checks run on that commit in a clean clone, serially (the shell suite, `quality_ratchet.py --run`, `bin/check-links --layout both`, `bin/check-layout-literals`, the `.verify.sh` exit histogram, the changed-file list against plan section 4), and a record goes under `docs/planning/pr-composition-evidence/`. The branch is un-pushed.

### 2026-10-26 · [ad hoc] S377 push -- fork `main` fast-forwarded `b52d6a15..eee1e83e` (5 commits of S376: trim, fold, claim, work, close-out); fork `origin` only

His go-ahead at the Phase 0 picker ('Push main to fork'). After `git push origin main` (exit 0, `b52d6a15..eee1e83e`), `git ls-remote origin refs/heads/main` and the local `main` both read `eee1e83e`. Nothing was pushed to `KJ5HST/methodology`.

### 2026-10-26 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-10-23.md` (101 record(s), 224,389 B → 99,389 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **101** record(s) (2026-10-20 → 2026-10-23) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-10-23.md`](docs/archive/CHANGELOG-through-2026-10-23.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-10-23.md.verify.sh`](docs/archive/CHANGELOG-through-2026-10-23.md.verify.sh)
rather than trusting a digest printed here. Live file 224,389 B → 99,389 B (−55.7%).

### 2026-10-26 · [ad hoc] S376 close-out -- PR2b sized: 4 of the candidate's 34 commits stop on a conflict against `upstream/main` `d50ce290`; `HANDOFFS.md` trimmed 5 to 3 and the fork pushed at his go-aheads; nothing sent to `KJ5HST/methodology`

Phase 3 of the session whose claim stands below (`CHANGELOG: pending` is resolved by this entry and the entries between). **Deliverable:** the PR2b sizing (work `228aef5ab9ab`, below). **Also done, each at his Phase 0 tick and each with its own entry:** the push of fork `main` (`2dab0e6e..b52d6a15`), the trim `5f191acb` and its fold `8de31be0`. **Offered and not ticked:** a `--force` trim of `CHANGELOG.md`, which stood at 217,197 B at Phase 0, past its 196,608 B trigger; it is offered again at the next picker with its cost. **Receipt:** `HANDOFFS.md` S376 `status: complete`, self-score 8, predecessor (S375) scored 8; gates `quality_ratchet: 24/24 pass · 0 fail · 0 unmeasured · results 32858fe46628 · manifest 102234f3acf8` in a clean clone. **3C:** no row appended to `docs/FORK_LEARNINGS.md`, so D3's retirement duty does not fire and no row was adjudicated; the lessons went to auto-memory (his rule not to ask him to run a command I may run; the sizing bracket). **Unpushed:** this session's five commits. Nothing sent to `KJ5HST/methodology`.

### 2026-10-26 · [ad hoc] S376 work -- PR2b sized: 4 of the candidate's 34 commits stop on a conflict against `upstream/main` `d50ce290` (policy B: 46 regions in 4 files, equal to the one-shot control; policy A: 3 commits, 32 regions); script, output and record added; the plan's PR2b estimate line points at them; fork only; nothing sent to `KJ5HST/methodology`

**Added** under `docs/planning/pr-composition-evidence/`: `pr2b-sizing.py` (applies the 34 commits one at a time, each onto the result of the one before, in a throwaway bare `--no-local` clone; keeps nothing; two runs byte-equal), `pr2b-sizing-output.txt` and `pr2b-sizing-record.md`. **Measured:** the control (the whole candidate against `upstream/main` in one merge) reads 46 regions in 4 files, S375's figure, so the counting agrees; commits 1 (`bbe0dc35`), 5 (`98ca7fc9`), 26 (`2276f4ef`) and 34 (`3cba1e50`) stop when upstream's side is kept (46 regions), commits 1, 5 and 34 when the commit's side is kept (32 regions); every stopper touches one of the 8 files upstream changed, as derived before measuring; all stops are in the trimmer, its tests, `FRAMEWORK_APPARATUS.md` and `.quality-gates.json`. **Read from the files, labelled readings in the record:** commit 1's 26 trimmer and test regions are the lineage upstream already merged as #94 (candidate's copy to upstream's: +198 / -30 of 2,757 lines, +832 / -20 of 4,239); commit 5 (+228 / -92 trimmer, +497 / -1 tests) is the only new judgment; commit 26 is a scrub to redo; commit 34's fix is in upstream's trimmer already (`unfinished(`, 5 of its 6 tests by name or reworded). **Plan:** one line (`:188`) now points at the record, 29,980 B to 29,992 B of its 30,000 B gate, measured in the command that wrote it; section 9's script table has no row for the new script (8 B of room). **Not done and not claimed:** applying a commit without a conflict is not green; none of the PR2 row's clean-clone checks was run on a rebuilt branch, and "two to three sessions" is still a guess. Nothing sent to `KJ5HST/methodology`.

### 2026-10-26 · [ad hoc] S376 claim (in progress) -- size PR2b: apply the candidate's 34 commits to `upstream/main` `d50ce290` in a scratch clone and record which commits stop on a conflict; fork only; nothing sent to `KJ5HST/methodology`

Claimed at his Phase 0 picker: the recommended option, 'PR2b: size the rebuild' (the others offered were BL-114, the fix for the maintainer's issue #95, and housekeeping only), with two go-aheads ticked, both already done and logged: the trim of `HANDOFFS.md` (`5f191acb`, fold `8de31be0`) and the push of fork `main`. A third, a `--force` trim of `CHANGELOG.md`, was offered and not ticked: it stood at 217,197 B at Phase 0, past the trimmer's 196,608 B trigger, and the trimmer refuses without `--force` (SRF 1.1238, RED). Phase 0 (read 2026-10-26) found both frontiers at `b52d6a15`, which is `HEAD` (0 undocumented commits, 0 merges, no pending receipt), `check-ledger` and `check-handoff` exit 0, the S375 receipt's gate citation (`results 007cf11d653a`, `manifest 102234f3acf8`) equal to the local `.quality-gates-results.json`, `upstream/main` unchanged at `d50ce290`, PR #98 open and CLEAN (head `65990cda`) and PR #96 open (CONFLICTING is the `merge=union` gap), each with 0 comments and 0 reviews, issues #93, #95 and #97 open and unchanged, dashboard 72/100 with 0 high-risk flags. The deliverable is a sizing record (a script, its saved output and a short record under `docs/planning/pr-composition-evidence/`); PR2b proper, with each region resolved and each layer green in a clean clone, is later sessions, one layer each. Standing instruction from him this session: do not ask him to run a command I am authorised to run (saved to auto-memory). Nothing goes to `KJ5HST/methodology`.

### 2026-10-26 · [ad hoc] S376 fold -- the trim's pointer block leaves `HANDOFFS.md` and one row joins `docs/HANDOFFS_ARCHIVE_INDEX.md`

The block (4 lines, 456 B; `HANDOFFS.md` 36,090 B before, 35,634 B after) became the row `| 2 | 2026-10-23 → 2026-10-23 | HANDOFFS-through-2026-10-23-3.md | v1.8.1 |`. Own commit, as the index's rule says (fork Learning #58); the shard's verify script, `bin/check-handoff` and `bin/check-ledger` are run after it. It follows the trim `5f191acb` (five receipts to three, S372 and S371 archived, on his keep-three rule, trim above four), taken at his Phase 0 go-ahead; I ran the `--write` myself (sessions 354 and 355 had recorded a classifier refusal, and later trims were left to him with `!` without retrying) and the classifier raised no refusal. Nothing sent to `KJ5HST/methodology`.

### 2026-10-26 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-23-3.md` (2 record(s), 58,899 B → 36,090 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-10-23 → 2026-10-23) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-23-3.md`](docs/archive/HANDOFFS-through-2026-10-23-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-23-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-23-3.md.verify.sh)
rather than trusting a digest printed here. Live file 58,899 B → 36,090 B (−38.7%).

### 2026-10-26 · [ad hoc] S376 push -- fork `main` fast-forwarded `2dab0e6e..b52d6a15` (6 commits of S375: claim, work, pointers, decision, correction, close-out); fork `origin` only

His go-ahead at the Phase 0 picker ('Push main to fork'). `git merge-base --is-ancestor origin/main main` held (0 behind, 6 ahead) before it, and after it `git ls-remote origin refs/heads/main` and the local `main` both read `b52d6a15` (0 ahead, 0 behind). Nothing was pushed to `KJ5HST/methodology`.

### 2026-10-26 · [ad hoc] S375 close-out -- the one-upstream-PR plan refreshed for upstream's move (candidate 28 commits behind, 46 conflict regions); PR2b approved as the next phase; the predecessor's 11 commits pushed to the fork; nothing sent to `KJ5HST/methodology`

Phase 3 of the session whose claim stands below (`CHANGELOG: pending` is resolved by this entry and the entries between). **Deliverable:** `docs/planning/upstream-pr-composition-plan.md` refreshed (work `0f227522ef7b`; 29,999 B to 29,980 B of its 30,000 B gate after the correction below), with a new phase PR2b that he approved at a picker ('Rebuild now'). **Also done:** two evidence records' line citations corrected (`c3ef634a7c4b`), his answer recorded (`d5c4da8df126`), the correction of my own byte figure (`b3d2550ffccb`), and the push of the predecessor's 11 commits to the fork's `origin` (its own entry below). **Corrections, by entry:** the decision entry says '29,972 B'; the plan read 30,002 B (see 'S375 correction'). **Predecessor (3A):** S374 scored 8; every cited anchor held in the tree, and what was missing is that #94's merge left the candidate 28 commits behind in 46 conflict regions. **Self-assessment (3B):** 7; the byte figure written before it was measured, four passes over the byte budget, a draft with a guessed line span, and the dashboard snapshot left out of the claim commit (it rides in this commit). **Learnings (3C):** no row appended to `docs/FORK_LEARNINGS.md`, so D3's retirement duty does not fire; the lesson (measure before writing a number into an entry that cannot be edited) went to auto-memory. **Gate run (3E):** 24/24 pass, 0 fail, 0 unmeasured, results `007cf11d653a`, manifest `102234f3acf8`, in a clean `--no-local` clone of `c3ef634a7c4b`; `tests-sh-passed` 692, the floor; the plan-size gate re-read by hand on the final tree (29,980 B). **Next session:** S376's Phase 0 counts 5 receipts and trims two; the approved deliverable is PR2b, beginning with a sizing cherry-pick; PR5 stays three separate go-aheads. `dashboard_history.jsonl` (the Phase 0 snapshot) is committed here. Nothing sent to `KJ5HST/methodology`.

### 2026-10-26 · [ad hoc] S375 push -- the fork's `origin/main` fast-forwarded `03685ed4` to `2dab0e6e` (the 11 commits of S373 and S374); nothing sent to `KJ5HST/methodology`

At his Phase 0 go-ahead ('Push main to fork', described to him as the 11 local commits of S373 and S374). `git merge-base --is-ancestor origin/main 2dab0e6e` confirmed a fast-forward; then `git push origin 2dab0e6e:refs/heads/main`. Read back: `git ls-remote origin refs/heads/main` and `origin/main` after a fetch both read `2dab0e6e`; `upstream/main` still `d50ce290`. S375's own commits were not part of that go-ahead and stay local. Nothing sent to `KJ5HST/methodology`.

### 2026-10-26 · [ad hoc] S375 correction -- the plan was 30,002 B after the decision entry below (not the 29,972 B that entry says); cut to 29,980 B

**What was wrong:** the entry headed 'S375 decision -- PR2b ... is the next phase' (commit `d5c4da8d`) states the plan went 'from 29,941 B to 29,972 B of 30,000 B'. I wrote 29,972 B before measuring it; `wc -c` printed in the same command read **30,002 B**, 2 B over the `plan-size-pr-composition` gate (30,000 B), and the commit went through because the pre-commit hook guards only a loosened threshold, not a value over one. The 29,941 B in the work entries below was measured and is right. **Fixed:** two of the markers I had just added were shortened ('(added S375; next phase, his picker 2026-10-26)' to '(added S375; next, his picker 2026-10-26)'; the quoted option name in D4 dropped), measured at **29,980 B**. The committed decision entry is left as written, as the ledger rule requires. The gate run in a clean clone (exit 0, below) was of `c3ef634a`, when the plan stood at 29,941 B, so it did not see the 2 B; the gate is re-read on the final tree at close-out. Nothing sent to `KJ5HST/methodology`.

### 2026-10-26 · [ad hoc] S375 decision -- PR2b (rebuild the candidate on `upstream/main` `d50ce290`) is the next phase of the one-pull-request plan; his picker answer recorded in the plan; fork `main` only; nothing sent to `KJ5HST/methodology`

Asked in one picker (one question, three options) after the plan refresh showed the candidate conflicts with the merged trimmer in 46 regions: **'Rebuild now (Recommended)'**, over 'Wait for #98' and 'Not yet'. That answer also settles my D4 extension: at PR5, if #98 is still open, the session asks whether to stack on its head or state supersession. The plan's PR2b row and D4 item now say 'his picker 2026-10-26' where they said 'added S375' and 'not yet his' (29,941 B to 29,972 B of 30,000 B). It starts nothing: PR2b is a later session, with its own claim, and PR5 still needs three separate go-aheads. Nothing sent to `KJ5HST/methodology`.

### 2026-10-26 · [ad hoc] S375 work (pointers) -- two evidence records' line citations into the refreshed plan corrected; fork `main` only; nothing sent to `KJ5HST/methodology`

The plan refresh above moved text, so the cross-reference check (Phase 3F) searched the tree for line citations into `docs/planning/upstream-pr-composition-plan.md`. Four were found. **Corrected:** `pr-composition-evidence/d1-d4-record.md` section 5 said D4 sat at 'section 7, line 223' (it is item 4, at line 225 now, and reworded, so the record says it quotes the original); `pr-composition-evidence/i95-record.md` cited `:251-252` for the 'separate decision' bullet (now `:254-255`, re-read). **Left, on purpose:** `BACKLOG-COMPLETED.md` (BL-122 row, 'line 63', now 64) and `BACKLOG-DETAIL.md` (`:251-252`, now `:254-255`), whose bodies are pinned by their `.verify.sh` proofs and whose item prose is deliberately not edited; both still point within a few lines of the right text. Two files touched, in their own commit so the first holds the 5-file cap. Nothing sent to `KJ5HST/methodology`.

### 2026-10-26 · [ad hoc] S375 work -- `docs/planning/upstream-pr-composition-plan.md` refreshed for upstream's move (#92 and #94 merged; the candidate is 28 commits behind and conflicts in 46 regions); fork `main` only; nothing sent to `KJ5HST/methodology`

**Found, by a new script (`docs/planning/pr-composition-evidence/conflicts-after-merge.sh`, output beside it):** `upstream/main` is `d50ce290`, 28 commits past the plan's base `f34769f3`; #92 and #94 merged on 2026-10-24 (the maintainer, locally, 5 days after the fork answered his 2026-10-19 change requests); the trimmer there is 1.8.2 (227 unit tests, 124 before), the candidate `pr2/candidate` (`3cba1e50`, 34 commits) has 1.8.1. `git merge-tree` with attributes off (GitHub's view) puts the candidate in **46 conflict regions in 4 files** against `upstream/main` (trimmer 25, its tests 18, `FRAMEWORK_APPARATUS.md` 2, `.quality-gates.json` 1), 52 against #98's head, 3 against #96's. The plan's old reading, that the fork's side wins in the trimmer's regions, was made at #94's 1.7.0 head and no longer holds. His own words on #94 (read in full): he asked that the `SESSION_NOTES.md` entry go in its own pull request, and he merges locally because GitHub's button ignores `merge=union`.

**Changed in the plan (29,999 B to 29,941 B of its 30,000 B gate, so it cut before it added):** the status line and the 'measured at' line (the figures of sections 0, 1, 2.1, 2.3, 2.4 are stated as the old base's and not re-run); 0.5, 0.7 and the whole of 2.2 rewritten to the measurement above; a new phase **PR2b** (rebuild the candidate on `upstream/main`, with its DONE criterion, checks, surface and stop; its two-to-three-sessions size is labelled a guess); D4 now records that its wait ended on 2026-10-25 (his S369 answer) and that the stack-or-supersede question about #92 and #94 is moot; two bullets in section 8 and one row in section 9. **Added by me, marked 'not yet his' in D4:** the same stack-or-supersede question applies to #98 at PR5. **Cuts to fit:** the status line's per-layer hash list (all 19 hashes re-checked in their records), the section 4 seam paragraph's tail (D6 says it), three versions the section 1 table already carries, a code-comment quotation that D3 and the status line already cover, two derived figures. **Not done:** no figure outside section 2.2 was re-measured; no region was read; nothing was rebuilt.

`dashboard_history.jsonl` (changed by the Phase 0 dashboard run) is left uncommitted. Nothing sent to `KJ5HST/methodology`.

### 2026-10-26 · [ad hoc] S375 claim (in progress) -- refresh `docs/planning/upstream-pr-composition-plan.md` now that #94 merged and D4's date gate (2026-10-25) has passed; fork `main` only; nothing sent to `KJ5HST/methodology`

Claimed at his Phase 0 picker: the recommended option (refresh the PR5 plan) and, as a separate go-ahead, the push of fork `main` (11 commits, S373 and S374) to the fork's `origin`; nothing goes to `KJ5HST/methodology`. The other options offered were BL-114 (the fix for the maintainer's issue #95) and stopping. Phase 0 (read 2026-10-26) found both frontiers at `2dab0e6e`, which is `HEAD` (0 undocumented commits, 0 merges, no pending receipt), `check-ledger` and `check-handoff` exit 0 with 4 receipts (49,134 B of 65,536 B, so no trim is owed), the S374 receipt's gate citation (`results 1ccb82be98d6`, `manifest 102234f3acf8`) equal to the local `.quality-gates-results.json`, `upstream/main` unchanged at `d50ce290`, PR #98 open and MERGEABLE/CLEAN with 0 comments and 0 reviews, PR #96 open (CONFLICTING is the `merge=union` gap), issues #93, #95 and #97 open and unchanged, dashboard 72/100 with 0 high-risk flags, 40 open backlog rows. The dashboard run modified `dashboard_history.jsonl` (tracked), left uncommitted at Phase 0. The plan is 29,999 B against its 30,000 B gate (`plan-size-pr-composition`), so an edit cuts before it adds. `CHANGELOG: pending` until the close-out entry. Nothing sent to `KJ5HST/methodology`.

### 2026-10-26 · [BL-98] S374 close-out -- the second upstream pull request opened as #98 (read back equal); the HANDOFFS trim and fold ran first; nothing else sent upstream

Deliverable: the second upstream pull request, from prepared to opened (https://github.com/KJ5HST/methodology/pull/98). Done at his word step by step: the Phase 0 picker (first 'Rebase PR #96', then, once I showed its CONFLICTING label is GitHub's `merge=union` gap and that it is independent of the second PR, 'Open the second PR'), the trim, the body reworded and approved, the branch pushed to the fork, the PR opened. The `HANDOFFS.md` trim (`ab3130e7`, S370 and S369 to `HANDOFFS-through-2026-10-23-2.md`) and its fold (`ca1f29dd`) ran before the claim. The receipt is complete (self 8, predecessor 7); `HANDOFFS.md` rests at four receipts, so the next Phase 0 does not trim. Gates 24/24 in a clean clone of `70960971` (results `1ccb82be98d6`, manifest `102234f3acf8`). No row was appended to `docs/FORK_LEARNINGS.md`. Fork `main` was not pushed. Nothing was sent to `KJ5HST/methodology` except pull request #98.

### 2026-10-26 · [BL-98] S374 -- pull request #98 opened on `KJ5HST/methodology` (the trimmer's `SESSION_NOTES.md` entry, his follow-ups and the front-matter warning)

https://github.com/KJ5HST/methodology/pull/98, opened on his explicit go-ahead ('Yes, open it'), the last of the steps he took one at a time (draft shown and reworded, body approved, branch pushed to the fork, then this). `gh pr create -R KJ5HST/methodology --base main --head rmsharp:feat/trim-session-notes-ledger-issue93`, title from `second-pr-title.txt` and body from `second-pr-body.md` (14,915 B), not a draft. Read back from GitHub: state OPEN, base `main`, head `rmsharp:feat/trim-session-notes-ledger-issue93` at `65990cda`, title and body byte-identical to the files, 3 commits (`39825279`, `3df5b0cd`, `65990cda`), 6 files, +1020 -21, `MERGEABLE`/`CLEAN`. No comment, label, assignment or review request was added. It is the second pull request on the trimmer's `SESSION_NOTES.md` work, after #94 (merged); PR #96 (the close-out report tool) is a separate, independent pull request and was not touched.

### 2026-10-26 · [BL-98] S374 push -- `feat/trim-session-notes-ledger-issue93` force-pushed to the fork's `origin` (`8de50d23` to `65990cda`); nothing sent to `KJ5HST/methodology`

His go-ahead, given together with his approval of the recomposed body ('Approve; push to fork'). `origin` is `rmsharp/methodology` (`git remote get-url origin`). Guards ran in one script that stopped on any miss: `origin/feat/trim-session-notes-ledger-issue93` was exactly `8de50d23` after a fresh fetch, the local tip exactly `65990cda`, `upstream/main` an ancestor of the tip, no rebase marker, nothing staged, and the old tip not an ancestor (so the force was needed). Pushed by sha with `--force-with-lease=<branch>:8de50d23`; read back: `git ls-remote origin` and `origin/<branch>` both `65990cda6afd`, ahead/behind `0 0`. Only this branch was pushed: fork `main` stays ahead of `origin/main` by the S373 and S374 commits. Opening the pull request on `KJ5HST/methodology` is a separate go-ahead and has not been taken.

### 2026-10-26 · [BL-98] S374 work -- the second pull request's body recomposed so each open question stands alone; approved by him; nothing sent upstream

At his Phase 0 pick (open the second PR) the first step was showing the draft body. He kept all three open questions but said their descriptions leaned on shorthand from PR #94 and needed full recall of it. `docs/planning/second-pr-evidence/second-pr-body.md` was rewritten, not patched (9,370 B to 14,921 B): each question now states the situation, the numbers, how it was reproduced (questions 1 and 2 on throwaway files built to his figures, question 3 on a real project's file) and the choices; his own #94 words are quoted where the draft said 'your answer (b)'; exit codes, `PREFIX`, the one-read cap and `--cut` are defined. A cold reader given only the file restated all four decisions correctly and its jargon list was worked through. Checks that changed the text: the claim that a notes file with unmatched headings is 'refused by name' held only for dated headings (`GRAMMAR_MISMATCH`, exit 3; undated ones read `NO_RECORDS`); 'the other two commits do not depend on the first' is false (commit 2 conflicts in `methodology_trim.py` and `.quality-gates.json` on `upstream/main` without commit 1); 'hundreds of records' became the counts; a private project's name was removed. His question about `nprcgenekeepr` led to a survey of 13 notes files: 3 are over the seed's 120,000 B ceiling (largest 577,539 B, 97 records), and `nprcgenekeepr` was 6,370,574 B (620 records) at its first trim on 2026-08-12, so the 'Underneath' section now rests on the runner's own Phase 1B and 3A steps rather than on one project. He approved the text and the push of the branch to the fork. Nothing sent to `KJ5HST/methodology`.

### 2026-10-26 · [BL-98] S374 claim (in progress) -- send the second upstream pull request (`feat/trim-session-notes-ledger-issue93`, tip `65990cda`); nothing outward without his go-aheads

Claimed at his Phase 0 picker. He first chose 'Rebase PR #96'; I then showed him, from `git merge-tree` against `upstream/main` and the scratch PR #90's measurement, that #96's CONFLICTING label is GitHub's server-side merge not applying `merge=union` to `CHANGELOG.md` (the only conflicting file with attributes off; clean with upstream's own), and that #96 and the second PR are independent (shared files `.quality-gates.json`, `CHANGELOG.md`, `README.md`, on different lines; the two branches merge clean together). He switched to the recommended option, opening the second PR. Phase 0 found: both ledger frontiers at `8194b070`, 0 undocumented commits, 0 merges, no pending receipt; `upstream/main` still `d50ce290`; #96 open with 0 comments; #97 and #95 open with 0 comments, #93 open with 1. Before this claim, at his go-ahead, the `HANDOFFS.md` trim (five receipts to three, `ab3130e7`) and its fold (`ca1f29dd`) ran. Nothing sent to `KJ5HST/methodology`.

### 2026-10-26 · [ad hoc] S374 fold -- the trim's pointer block leaves `HANDOFFS.md` and one row joins `docs/HANDOFFS_ARCHIVE_INDEX.md`

The block (4 lines, 456 B; `HANDOFFS.md` 40,571 B before, 40,115 B after) became the row `| 2 | 2026-10-23 → 2026-10-23 | HANDOFFS-through-2026-10-23-2.md | v1.8.1 |`. Own commit, as the index's rule says (fork Learning #58); the shard's verify script, `bin/check-handoff` and `bin/check-ledger` are run after it. It follows the trim `ab3130e7`, taken at the operator's Phase 0 answer (five receipts to three, on his keep-three rule, trim above four); he ran the `--write` with `!`. Nothing sent to `KJ5HST/methodology`.

### 2026-10-26 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-23-2.md` (2 record(s), 60,224 B → 40,571 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-10-23 → 2026-10-23) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-23-2.md`](docs/archive/HANDOFFS-through-2026-10-23-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-23-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-23-2.md.verify.sh)
rather than trusting a digest printed here. Live file 60,224 B → 40,571 B (−32.6%).

### 2026-10-26 · [BL-98] S373 close-out -- the second upstream pull request prepared (local branch `feat/trim-session-notes-ledger-issue93`, tip `65990cda`); S372's 7 commits pushed to the fork; the receipt complete; nothing sent upstream

The deliverable was the second upstream pull request, prepared and not sent, chosen at his Phase 0 picker (the recommended option; the others offered were the fix for upstream issue #97, a resync of the fork's `main`, and a rebase of PR #96). The same picker took the push of S372's 7 commits (`S373 push` below). Phase 0 found both frontiers current at `03685ed4` and, after S372's receipt was written, that the maintainer had merged PR #92 and PR #94 on 2026-10-24, answered the four calls on #94 and asked for the second PR now, rebased on `main`; the work is in `S373 work`. The close-out found one more thing worth a line here: running the notes-file entry over real notes files showed that `mts-system`'s cannot be dry-run trimmed at `--cut 3` (`ARTIFACT_UNPARSEABLE`, a standalone `---` inside the oldest retained record; the same at 1.9.0; a refusal, not a loss), now item 3 in the draft body and a clause on the BL-98 rider. `docs/planning/second-pr-evidence/` gained its repro (`notes_rule_in_last_record.sh`) and the README and body were corrected after a fact-check. `HANDOFFS.md` now holds five receipts (S373 complete, 60,185 B of 65,536 B), so S374's Phase 0 trims two. `docs/FORK_LEARNINGS.md` gained no row (rows #76, #16 and #33 considered), so the retirement duty does not fire. Checks on the final tree: `check-handoff`, `check-ledger`, `check-links` and `check-backlog-anchors` exit 0; `bash bin/tests.sh` read 692 passed, 0 failed twice: on the tree with the pending receipt, and again with the completed receipt (before the `S373 evidence` entry was added). Open for him: the push of the branch to `origin` (a force-push) and the opening of the pull request, each a separate go-ahead. Nothing sent to `KJ5HST/methodology`.

### 2026-10-26 · [BL-98] S373 evidence -- item 3 of the draft body (a `---` rule inside the oldest retained record makes `mts-system`'s notes file unclassifiable after a trim), its repro, and the README and body corrected after a fact-check; nothing sent upstream

Running the first commit's notes-file entry over real notes files (the dry run reported in `S373 work`) showed `mts-system`'s `SESSION_NOTES.md` refused at `--cut 3` with `ARTIFACT_UNPARSEABLE`: a standalone `---` at line 31 sits inside the record that would become the last one, and with `footer_mode='none'` the trimmed text no longer classifies. Version 1.9.0 and 1.10.0 behave the same; `--cut 2` plans the trim, and removing that one line makes `--cut 3` plan it. A refusal, not a loss. Added under `docs/planning/second-pr-evidence/`: `notes_rule_in_last_record.sh` and its output. The draft body gains item 3 under 'Not settled' and a clause under 'Measured' (of the 5 notes files whose dry run reaches the plan, 4 plan and 1 is refused); the README gains a row. The fact-check of the draft changed three claims: '12 projects' became 11 with ledgers (a twelfth repository is empty), the 'reached' count of 14 became 15, and an unverified 'each commit leaves the gates green' was cut. The `S373 work` entry is not edited (a committed entry is never edited); this one adds to it. Nothing sent to `KJ5HST/methodology`.

### 2026-10-26 · [BL-98] S373 work -- the second upstream pull request prepared: local branch `feat/trim-session-notes-ledger-issue93`, tip `65990cda`, three commits on `upstream/main` `d50ce290`; nothing sent upstream

Built in a scratch clone of `upstream/main` with upstream's own hooks on, after a plan shown to him and his two answers at the picker (scope: rebase plus the three follow-ups plus the warning; for the entry-less file, 'say so' rather than refuse). **`39825279`** is `8de50d23` replayed (the cherry-pick applied without a conflict; trimmer 1.9.0). **`3df5b0cd`** is his three follow-ups (1.9.1): `--reverify` says 'has no entry for <file>' or 'the entry for <file> declares no stub marker' where it said 'declares none' for both; the `PREFIX` refusal says 'written for a different layout'; the `unfinished` comment, the `--reverify` legend and `FRAMEWORK_APPARATUS.md` name every case that exits 3 and say a proof written before 1.8.1 exits 1 where git cannot read the commit or object (measured: proofs written by 1.8.0, 1.8.1 and 1.10.0 run in a depth-1 clone exit 1, 3, 3). **`65990cda`** is `FRONTIER_FRONT_MATTER_UNCOMMITTED` (1.10.0), his answer (b): an advisory warning that runs the proof's own L2 test against HEAD's copy at write time. Every behaviour has a test that was run red first; the trimmer's suite goes 245 (the rebased first commit alone) to 270 and the gate floor 227 to 270. Verified on a fresh clone of the final tip: `quality_ratchet.py --run` 12 of 12 (results `1b096f787d67`, manifest `9f6dc2ebeb91`); the 54 proofs of his #93 repository still 46 at exit 0 and 8 at exit 4 (54 of 54 rows equal the saved column); the dry run over 33 ledger files of 11 projects fired on none of 33 clean trees, on 15 of 15 after a one-line synthetic edit that reaches the check, and on none of the live trees, which a `git status` before and after showed unchanged; the 22 `CHANGELOG.md` and `HANDOFFS.md` exit codes equal `main`'s trimmer's; mutation: 12 mutants of the new check (11 killed, 1 equivalent) and 4 of the follow-up code (4 killed, one only after a stronger assertion). Two history rebuilds by cherry-pick replay, not an interactive rebase: a ledger sentence that said 'he asked' became 'the maintainer asked', and the one-line assertion folded into the follow-ups commit; the tested tip is the final tip. The draft body's fact-check changed three claims (12 projects became 11 with ledgers; the 'reached' count of 14 became 15 after `mts-system`'s notes file showed the warning runs before a later refusal; an unverified 'each commit leaves the gates green' was cut). Title, body and every measurement are in `docs/planning/second-pr-evidence/` (`README.md` lists them); the branch is saved here as a local branch because the scratch clone is session-local. `origin` still holds the old `8de50d23` on `1670c5d4`, so putting the new branch there is a force-push, and opening the pull request is a second step: each is his go-ahead. The BL-98 index row carries a rider for the state. Nothing sent to `KJ5HST/methodology`.

### 2026-10-26 · [BL-98] S373 claim (in progress) -- prepare the second upstream pull request (the trimmer's `SESSION_NOTES.md` entry, rebased on `upstream/main`); preparation only, nothing sent upstream

Claimed at his Phase 0 picker, the recommended deliverable (the others offered were the fix for upstream issue #97, a resync of the fork's `main` with `upstream/main`, and a rebase of PR #96). Why now: the maintainer merged PR #92 (`2e9cad5`) and PR #94 (`d32c6c0`) locally on 2026-10-24, answered the four calls on #94 and wrote 'Open the second PR now, rebased on `main`', with three small follow-ups for it (the `SESSION_NOTES` shard's 'ledger table declares none' wording, the `PREFIX` refusal's reason, and three incomplete exit-3 statements at `methodology_trim.py:1525`, the `--reverify` help and `FRAMEWORK_APPARATUS.md:539`). The branch is `origin/feat/trim-session-notes-ledger-issue93`, one commit (`8de50d23`, trimmer 1.9.0) on `1670c5d4`, which is PR #94's head and now an ancestor of `upstream/main` `d50ce290`. The deliverable is the prepared branch, the verification and the draft text, shown to him; opening the pull request, force-pushing a branch and posting a comment are each a separate go-ahead. Phase 0 (read 2026-10-26) found both frontiers current (`CHANGELOG.md` and `HANDOFFS.md` at `03685ed4`, which was `HEAD`; 0 undocumented commits, 0 merges, no pending receipt), `check-ledger` and `check-handoff` exit 0 with 4 receipts (49,505 B of 65,536 B, no trim owed until S374), pull request #96 open at `ad5c980` with 0 comments and now reported conflicting, #92 and #94 merged, issues #93 (1 comment), #95 (0) and #97 (0, opened by him 2026-10-24) open, `upstream/main` `d50ce290`, dashboard 72/100 with 0 high-risk flags. Nothing sent to `KJ5HST/methodology`.

### 2026-10-26 · [ad hoc] S373 push -- the 7 commits that were ahead of the fork's `origin` (`a0ec04cf..03685ed4`) pushed to `origin`; nothing sent upstream

His go-ahead at the Phase 0 picker (the option 'Yes, push them'), one set: S372's trim `c3309007`, fold `6389122f`, claim `859dd7f3`, work `e77b8bda`, closure `9ee3e390`, floor `d5796447` and close-out `03685ed4`. `origin` is `rmsharp/methodology`, the fork (`git remote get-url origin`); guards run in one script before the push, each failing it: `origin/main` equal to the expected `a0ec04cf` after a fresh fetch, `merge-base --is-ancestor` true, ahead/behind `0 7`, no rebase marker, nothing staged. Pushed by sha (`03685ed4…:refs/heads/main`), read back: `git ls-remote origin refs/heads/main` and `origin/main` both `03685ed42548`, ahead/behind `0 0`. Nothing sent to `KJ5HST/methodology`.

### 2026-10-24 · [BL-122] S372 close-out -- BL-122 closed (`bin/status` says when its source has no history; Test 61); receipts trimmed 5 to 3 and folded; S371's 4 commits pushed to the fork; the receipt complete; nothing sent upstream

Phase 3 of the session whose claim stands below (`CHANGELOG: pending` is resolved by this entry and the entries between). **Deliverable:** BL-122 closed (work `e77b8bda`, closure `9ee3e390`, floor `d5796447`; open index rows 41 to 40). **Also done:** the receipt trim `c3309007` and its fold `6389122f`, and the push of S371's 4 commits (`7a5e5815..a0ec04cf`) to the fork's `origin` (its own entry below). **Corrections, by entry, because a committed entry is never edited:** the work entry says the 11 assertions that passed on the red run were 'the fixture, the controls and `bin/sync`'s wording'; read from the kept output they were the fixture (1), the two full-history controls (2), `bin/sync`'s wording on the three sources (3), 'every other row reads as against the full source' on the three (3) and the two rows the history can still answer (2). The closure entry and the closing row said the later carry is a re-apply 'onto upstream's `bin/status`'; `pr2/candidate` holds a third `bin/status` (blob `c74b77b269ab`) and the composition plan lists `bin/status` in its group A, so BL-122 is not in the plan's composition. The closing row in `docs/planning/BACKLOG-COMPLETED.md` is widened in this commit (the three `BACKLOG*.verify.sh` and `check-backlog-anchors` exit 0 after it); this entry carries the correction of the closure entry. **Predecessor (3A):** S371 scored 9; every cited anchor re-read in the tree it left, nothing wrong found. **Self-assessment (3B):** 8; the slips (a stray `/tmp/null` from a mistyped redirect, a first harness with a cut line range, a placeholder in the plan picker, a carry note first written too narrowly) and a loose sentence in the work entry. **Learnings (3C):** no row appended to `docs/FORK_LEARNINGS.md`; rows #16 and #81 considered, both read in full, and #16 already states the lesson applied (mutate the producer), so D3's retirement duty does not fire. **Gate run (3E):** 24/24 pass, 0 fail, 0 unmeasured, results `64559ac8d8c6`, manifest `98c8c8024d0e`, in a clean `--no-local` clone of `9ee3e390` (00:36 to 01:00); `tests-sh-passed` 692, now the floor. **Next session:** S373's Phase 0 does not trim (4 receipts) and S374's trims two; PR5 only on or after 2026-10-25 and then by his S369 ruling; `main` is 7 commits ahead of the fork's `origin`. Nothing sent to `KJ5HST/methodology`.

### 2026-10-24 · [BL-122] S372 tightening -- `tests-sh-passed` floor 660 to 692 (Test 61's 32 assertions); the 24-gate run

`quality_ratchet.py --run` in a clean `--no-local` clone of the closure commit `9ee3e390` (4 receipts in the tree: the claim stub and three complete ones, the state S366 read 660 in) read 24/24 pass, 0 fail, 0 unmeasured, results `64559ac8d8c6`, manifest `98c8c8024d0e` (the manifest before this move), `tests-sh-passed` 692; the run took from 00:36 to 01:00 on 2026-10-24 under a load of about 7 from other sessions. The floor in `.quality-gates.json` moves 660 to 692, with a dated note `_s372_tightening_bl122` in the file's existing style. 660 + 32 agrees with the measurement; the measurement is what the floor takes. A tightening: `quality_ratchet.py --precommit` accepts it. The only floor that moved; no gate was added. Fork `main` only; nothing sent to `KJ5HST/methodology`.

### 2026-10-24 · [BL-122] S372 -- close BL-122 (`bin/status` says when its source has no history; Test 61)

The index row out of `docs/planning/BACKLOG.md` (41 to 40 open rows), `BL-122` into its Completed id list (87 to 88 ids, recomputed against 88 closing rows), and its closing row appended to `docs/planning/BACKLOG-COMPLETED.md`; the `bl-122` anchor in `BACKLOG-DETAIL.md` is untouched, as the detail proof pins it. The closing row records what the work did (work `e77b8bda`), that a tree with no `.git` was covered although the row measured only the shallow case, and that the later carry to upstream is a re-apply onto upstream's different `bin/status` (blob `a3659766f5a4` against the fork's `0c3436ebd7ba`), untested, with its own go-ahead. Fork `main` only; nothing sent to `KJ5HST/methodology`.

### 2026-10-24 · [BL-122] S372 work -- `bin/status` reads a file that matches nothing in an incomplete source as `unknown (source history incomplete)` and prints one note before the table; Test 61 (32 assertions, red first)

His answer at the plan picker: 'Note plus 'unknown' rows, code and test only' (the recommended one of three). **Re-measured before the plan, by script:** a depth-1 clone of this repository as the source and a clean clone of `mts-system` (`69cc272`) as the project give 21 `locally modified` rows and no mention of history in the output; a full clone gives 0 `locally modified` and the same 21 rows as `N versions behind` (1, 2, 3, 4, 5, 6, 8, 9 and 10 behind); the live tree and the full clone agree row for row. **`bin/status`** (+58 -5 lines, 19,358 B to 22,781 B): `history_gap` makes the two tests `bin/sync`'s `history_gap` makes (no `.git`; `rev-parse --is-shallow-repository`) in its own words, `history_note` builds the note, `file_status` takes `incomplete` and returns `UNKNOWN` where it returned `locally modified`, and `report` prints the note after the `layout:` lines and before the table, only when at least one row is unknown. **`bin/tests.sh`** Test 61 (+87 lines), on Test 41's fixture and Test 48's three sources (a depth-1 clone, a depth-2 clone, a tree with no `.git`), a full-history control, the rows the shallow history can still answer, and a `--source=github` run over a shallow `file://` URL (git 2.56 clones a shallow repository shallow, so that branch is exercised). Its cause sentences are pinned against `bin/sync`'s own output, since the two tools carry separate copies of the test. **Red first:** 18 of 29 assertions failed on `HEAD` (the six new behaviours on each of the three sources), the 11 that passed being the fixture, the controls and `bin/sync`'s wording; green after, 32 of 32 once the github and singular assertions were added. **Mutation round:** 11 mutants of `bin/status` on a scratch copy of `bin/`, 10 killed; the eleventh added dead code after a `return` and is equivalent. **Neighbours, each alone:** `tools/test_sync_layouts.py` 89 OK, `bin/check-layout-literals` 0 sites, `bin/check-links` and `--layout both` exit 0. **Not changed:** `bin/sync`, the manifest, `README.md` line 730, `BOOTSTRAP.md` lines 103, 105, 418 and 495 (they list `bin/status`'s states or `bin/sync`'s refusal and do not name the new one; the third scope option would have added two sentences, and he did not choose it) and `CLAUDE.md`'s row for `bin/status`. **Reach:** `bin/status` is canonical-only, so an adopter gets the change only by updating their checkout of the canonical repository, which for fork work means a merged upstream pull request; nothing was sent to `KJ5HST/methodology`.

### 2026-10-23 · [BL-122] S372 claim (in progress) -- BL-122 (`bin/status` does not tell its reader that the methodology source has no git history); fork `main` only; nothing sent upstream

Claimed at his Phase 0 picker: BL-122, the recommended option (the other candidate offered was a test beside Test 28 pinning `BOOTSTRAP.md` lines 90 and 399 to the manifest, which needs a backlog row first). The same picker took the `HANDOFFS.md` trim (`c3309007`, five receipts to three; he ran the `--write` with `!`), its fold (`6389122f`, own commit) and the push of S371's 4 commits, all done before this claim. Phase 0 (read 2026-10-23) found both frontiers current (`CHANGELOG.md` and `HANDOFFS.md` at `a0ec04cf`, which was `HEAD`; 0 undocumented commits, 0 merges, no pending receipt), `check-ledger` and `check-handoff` exit 0 with 5 receipts (59,826 B of 65,536 B, so the trim was owed), pull requests #96 (`ad5c980`, 0 comments), #94 (`1670c5d`, 2) and #92 (`8a232bb`, 2) and issues #93 (1) and #95 (0) open and unchanged, `upstream/main` `f34769f3`, dashboard 72/100 with 0 high-risk flags. The local `.quality-gates-results.json` is still the 2026-10-10 file (18 gates against 24 declared), so S371's 24/24 citation is neither confirmed nor contradicted by it; no re-run was made at Phase 0. The row is re-measured before any edit. `CHANGELOG: pending` until the close-out entry. Nothing sent to `KJ5HST/methodology`.

### 2026-10-23 · [ad hoc] S372 push -- the 4 commits that were ahead of the fork's `origin` (`7a5e5815..a0ec04cf`) pushed to `origin`; nothing sent upstream

His go-ahead at the Phase 0 picker (the option 'Push S371's 4 commits to the fork'), one set: S371's claim `8281b209`, work `60772eb2`, closure `acd1805c` and close-out `a0ec04cf`. `origin` is `rmsharp/methodology`, the fork (`git remote get-url origin`); guards run in one script before the push, each failing it: `origin/main` equal to the expected `7a5e5815` after a fresh fetch, `merge-base --is-ancestor` true, ahead/behind `4 0`, no rebase marker, nothing staged. Pushed by sha (`a0ec04cfaa31:refs/heads/main`), read back: `git ls-remote origin refs/heads/main` and `origin/main` both `a0ec04cfaa31`, ahead/behind `0 0`. Nothing sent to `KJ5HST/methodology`.

### 2026-10-23 · [ad hoc] S372 fold -- the trim's pointer block leaves `HANDOFFS.md` and one row joins `docs/HANDOFFS_ARCHIVE_INDEX.md`

The block (4 lines, 448 B; `HANDOFFS.md` 38,552 B before, 38,104 B after) became the row `| 2 | 2026-10-23 → 2026-10-23 | HANDOFFS-through-2026-10-23.md | v1.8.1 |`. Own commit, as the index's rule says (fork Learning #58); the shard's verify script, `bin/check-handoff` and `bin/check-ledger` are run after it. It follows the trim `c3309007`, taken at the operator's Phase 0 picker answer to trim `HANDOFFS.md` (five receipts to three, on his keep-three rule, trim above four); he ran the `--write` with `!`. Nothing sent to `KJ5HST/methodology`.

### 2026-10-23 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-23.md` (2 record(s), 59,826 B → 38,552 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-10-23 → 2026-10-23) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-23.md`](docs/archive/HANDOFFS-through-2026-10-23.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-23.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-23.md.verify.sh)
rather than trusting a digest printed here. Live file 59,826 B → 38,552 B (−35.6%).

### 2026-10-23 · [BL-121] S371 close-out -- BL-121 closed (BOOTSTRAP lines 90 and 399 name every root file the manifest distributes; the row undercounted: 7 names, not 5); S370's 6 commits pushed to the fork; the receipt complete; nothing sent upstream

Phase 3 of the session whose claim stands below (`CHANGELOG: pending` is resolved by this entry and the entries between). **Deliverable:** BL-121 closed (work `60772eb2`, closure `acd1805cea6d`; open index rows 42 to 41). **Also done:** the push of S370's 6 commits (`66efb971..7a5e5815`) to the fork's `origin` (its own entry below). **Predecessor (3A):** S370 scored 9; every cited anchor re-read in the files, nothing wrong found. **Self-assessment (3B):** 8; the work entry's false 'adopters receive' sentence (corrected in the closure entry, not edited), a wrong 21 B figure in the plan picker (23 B), and a 'no existing word changes' said before the moved 'and' was counted. **Learnings (3C):** no row appended to `docs/FORK_LEARNINGS.md`; rows #81 and #100 considered, both read in full, and #100 already states the lesson at least as generally, so D3's retirement duty does not fire. **Gate run (3E):** 24/24 pass, 0 fail, 0 unmeasured, results `873329624aaf`, manifest `98c8c8024d0e`, in a clean `--no-local` clone of `acd1805cea6d` (1,427 s); `tests-sh-passed` 660 against its floor of 660. **Next session:** S372's Phase 0 trims two receipts (S368 and S367); PR5 only on or after 2026-10-25. Nothing sent to `KJ5HST/methodology`.

### 2026-10-23 · [BL-121] S371 -- close BL-121 (lines 90 and 399 of `starter-kit/BOOTSTRAP.md` fixed; the row undercounted: 7 names were missing, not 5); open index rows 42 to 41; fork `main` only; nothing sent upstream

The index row out of `docs/planning/BACKLOG.md`, `BL-121` into its Completed id list (86 to 87 ids, recomputed against the 87 closing rows), its closing row appended to `BACKLOG-COMPLETED.md`; the body in `BACKLOG-DETAIL.md` is untouched (the detail proof pins it). Work `60772eb2`. **A correction to the entry below it, which is not edited (a committed entry never is):** the S371 work entry ends 'Adopters receive the lines at their next `bin/sync`'; that is wrong. Fork work reaches adopters only through a merged upstream pull request (`CLAUDE.md`, *Contributing upstream*), so this commit reaches none. The same sentence stands in S370's work entry for `382e524c` ('Adopters receive the line at their next `bin/sync`'), for the same reason. What the carry needs is in the closing row: `close_out_report.py` has no manifest row on `upstream/main` or `pr2/candidate`, so its two insertions must not travel yet.

### 2026-10-23 · [BL-121] S371 work -- `starter-kit/BOOTSTRAP.md` lines 90 and 399 now name every file `bin/_manifest.py` distributes at the project root; fork `main` only; nothing sent upstream

His answer at the plan picker: 'Lines 90 and 399, insertions only'. Re-measured before the plan, against `bin/_manifest.py` (`DISTRIBUTION`: 31 rows, 24 tracked and 7 seeds; 12 tracked files land at the project root): **the row undercounted twice.** It said 3 tools and 2 seed configs were missing from line 90; the manifest has **4** tools beyond the dashboard (`methodology_trim.py`, `context_budget.py`, `quality_ratchet.py` and `close_out_report.py`, the fifth executable, added with BL-79 after the row's count) and **3** seeds beyond the four named (`.context-budget.json`, `.quality-gates.json` and `.gitattributes`), so 7 names were missing, not 5, and the row's own 'grep each name' proof would have passed with `close_out_report.py` still absent. **The class scan:** over the 23 shipped documents, the only other line that lists the tools is the Tracked row at `BOOTSTRAP.md:399` (4 of the 5), also missing `close_out_report.py`; the other lines that name three or more seeds (`SESSION_RUNNER.md:20`, `BOOTSTRAP.md:105`, `:296`, `:459`, `ITERATIVE_METHODOLOGY.md:150`, `:388`, `:399`) are incidental mentions, not lists of what `bin/sync` installs. `BOOTSTRAP.md:400` (the Adopter-owned row) already names all seven seeds because Test 28 in `bin/tests.sh` pins it to the manifest; nothing pins lines 90 and 399, which is why they decayed, and no pin was added (the third option at the picker, not chosen). **The edit:** line 90 gains the 4 tools after `methodology_dashboard.py` and the 3 seeds after `ROADMAP.md` (the word 'and' moves from before `ROADMAP.md` to before `.gitattributes`); line 399 gains `close_out_report.py` after `quality_ratchet.py`. 2 of 497 lines changed, 40,068 B to 40,244 B (+176 B), no `docs/methodology` string added (still 9, so `LEGACY_PATH_ALLOWANCE` in `bin/check-links` did not move). **Proofs, each exit 0 alone:** a script that reads the manifest and asks that every root-level tracked file and every seed appear in line 90 and every root-level tracked file in line 399, red on `HEAD` before the edit (7 missing from line 90, 1 from line 399) and green after, and that strips the insertions from the new lines and gets the old lines back exactly; `bin/check-links` and `bin/check-links --layout both` (80 links, 23 documents); `tools/test_sync_layouts.py` (89 tests OK). The proof script is not committed (it lives in the session's scratchpad); the lists are re-derivable from `DISTRIBUTION` in a line. Adopters receive the lines at their next `bin/sync`; the upstream candidate's copy of them is a later, separate go-ahead.

### 2026-10-23 · [BL-121] S371 claim (in progress) -- BL-121 (the 'Setup with `bin/sync`' prose in `starter-kit/BOOTSTRAP.md` is stale against `bin/_manifest.py`); fork `main` only; nothing sent upstream

Claimed at his Phase 0 picker: BL-121, the recommended option (the other candidates offered were BL-122, settling two of his open calls, and a task of his own). Phase 0 (read 2026-10-23) found both frontiers current (`CHANGELOG.md` and `HANDOFFS.md` at `7a5e5815`; 0 undocumented commits, 0 merges, no pending receipt), `check-ledger` and `check-handoff` exit 0 with 4 receipts (47,962 B of 65,536 B, room for 1 more, so no trim is owed now and S372's Phase 0 trims two), pull requests #96 (`ad5c980`, 0 comments), #94 (`1670c5d`, 2) and #92 (`8a232bb`, 2) and issues #93 (1) and #95 (0) open and unchanged, `upstream/main` `f34769f3`, dashboard 72/100 with 0 high-risk flags. The local `.quality-gates-results.json` is still the 2026-10-10 file (18 gates against 24 declared), so S370's 24/24 citation is neither confirmed nor contradicted by it; no re-run was made at Phase 0. The row is re-measured before any edit. `CHANGELOG: pending` until the close-out entry. Nothing sent to `KJ5HST/methodology`.

### 2026-10-23 · [ad hoc] S371 push -- the 6 commits that were ahead of the fork's `origin` (`66efb971..7a5e5815`) pushed to `origin`; nothing sent upstream

His go-ahead at the Phase 0 picker (the option 'Yes, push now'), one set: S370's trim `64ef4966`, fold `6abe24cc`, claim `7c47696c`, work `382e524c`, closure `7db362d4874e` and close-out `7a5e5815`. `origin` is `rmsharp/methodology`, the fork (`git remote get-url origin`); guards run in one script before the push, each failing it: `origin/main` equal to the expected `66efb971` after a fresh fetch, `merge-base --is-ancestor` true, ahead/behind `0 6`, no rebase marker, nothing staged; the pushed set touched 9 files. Pushed by sha (`7a5e5815f235:refs/heads/main`), read back: `git ls-remote origin refs/heads/main` and `origin/main` both `7a5e5815f235`, ahead/behind `0 0`. Nothing sent to `KJ5HST/methodology`.

### 2026-10-23 · [BL-123] S370 close-out -- BL-123 closed (BOOTSTRAP line 399 now names its layout; the row was wrong about line 28 and the allowance); receipts trimmed 5 to 3 and folded; S369's push record pushed to the fork; the receipt complete; nothing sent upstream

Phase 3 of the session whose claim stands below (`CHANGELOG: pending` is resolved by this entry and the entries between). **Deliverable:** BL-123 closed (work `382e524c`, closure `7db362d4874e`; open index rows 43 to 42). **Also at his Phase 0 picker:** the `HANDOFFS.md` trim (`64ef4966`, 57,796 B to 37,407 B, he ran the `--write` with `!`) and its fold (`6abe24cc`), and the push of S369's push record to the fork's `origin` (`650a7ca4..66efb971`, read back by `git ls-remote`). The `HANDOFFS.md` receipt is `status: complete` (self 8, predecessor S369 scored 9); S372's Phase 0 trims two receipts (four at rest after this close-out). **Quality checks:** `quality_ratchet.py --run` in a clean `--no-local` clone of the closure commit `7db362d4874e` (1,518 s): `24/24 pass · 0 fail · 0 unmeasured · results 873329624aaf · manifest 98c8c8024d0e`, with `tests-sh-passed` measuring 660 against its floor of 660 (identical to S369's citation, as expected for a text change). **Phase 3C:** no row appended to `docs/FORK_LEARNINGS.md`, so the retire-or-refuse rule (D3) did not trigger and no row retires; rows considered: #81, #98. **Not done, by design:** the same line 399 insertion on `pr2/candidate` (a later separate go-ahead with the candidate rebuild); a same-line label on line 28 (his choice); PR5 (not before 2026-10-25); nothing sent upstream. `main` is 6 commits ahead of `origin` (the trim, the fold, the claim, the work, the closure and this close-out); no push until he says so.

### 2026-10-23 · [BL-123] S370 -- close BL-123 (line 399 of `starter-kit/BOOTSTRAP.md` fixed; the row was wrong about line 28 and about the allowance); open index rows 43 to 42; fork `main` only; nothing sent upstream

The index row out of `docs/planning/BACKLOG.md`, `BL-123` into its Completed id list (85 to 86 ids, recomputed against the 86 closing rows), its closing row appended to `BACKLOG-COMPLETED.md`; the body in `BACKLOG-DETAIL.md` is untouched (the detail proof pins it). Work `382e524c`; the closing row carries the two corrections and what was left undone on purpose.

### 2026-10-23 · [BL-123] S370 work -- `starter-kit/BOOTSTRAP.md` line 399 now says which layout its "everything under `docs/methodology/`" means; line 28 left alone; fork `main` only; nothing sent upstream

His answer at the plan picker: 'Line 399 only'. Re-measured before the plan: of the 11 `docs/methodology` strings in the 23 shipped documents (BOOTSTRAP 9, `SESSION_RUNNER.md` 1, `HOW_TO_USE.md` 1), exactly two do not name their layout on their own line, BOOTSTRAP lines 28 and 399, as the row said. **The row was wrong about line 28:** the drawing is the legacy tree, and the sentence after its fenced block (line 39, 'This tree shows the legacy layout. The `methodology/` layout is described under *Two layouts* below.') labels it; that sentence came in at S282 (2026-10-08, `2d84e92d`), twelve days before the row was raised, so line 28 was left as it is. **The row was wrong about the allowance:** the fix adds `; `methodology/` in the `methodology/` layout` inside the existing parenthesis, and no `docs/methodology` string, so the count stays 9 and `LEGACY_PATH_ALLOWANCE` in `bin/check-links` did not move. The edit is a pure insertion on one line (1 of 497 changed, 40,023 B to 40,068 B, +45 B), proved against `HEAD`. Proofs, each exit 0 alone: `bin/check-links` and `bin/check-links --layout both` (80 links, 23 documents), `tools/test_sync_layouts.py` (89 tests OK, the gate's floor is 89). Adopters receive the line at their next `bin/sync`; the upstream candidate's copy of the same line is a later, separate go-ahead.

### 2026-10-23 · [BL-123] S370 claim (in progress) -- BL-123 (two lines of `starter-kit/BOOTSTRAP.md`, 28 and 399, name `docs/methodology/` without saying which layout); fork `main` only; nothing sent upstream

Claimed at his Phase 0 picker: BL-123, the recommended option. The same picker took the `HANDOFFS.md` trim (`64ef4966`, five receipts to three; he ran the `--write` with `!`), its fold (`6abe24cc`, own commit) and the push of S369's push record, all done before this claim. Phase 0 (read 2026-10-23) found both frontiers current (`CHANGELOG.md` and `HANDOFFS.md` at `66efb971`/`650a7ca4`; 0 undocumented commits, 0 merges, no pending receipt), `check-ledger` and `check-handoff` exit 0 with 5 receipts (57,796 B of 65,536 B, so the trim was owed on his keep-three, trim-above-four rule), pull requests #96 (`ad5c980`, 0 comments), #94 (`1670c5d`, 2) and #92 (`8a232bb`, 2) and issues #93 (1) and #95 (0) open and unchanged, `upstream/main` `f34769f3`, dashboard 72/100 with 0 high-risk flags. The local `.quality-gates-results.json` is from 2026-10-10 (18 gates), so S369's 24/24 citation is neither contradicted nor confirmed by it; no `--run` this Phase 0. The dashboard refresh's one `dashboard_history.jsonl` line rides this claim, as in S364 to S369.

### 2026-10-23 · [ad hoc] S370 fold -- the trim's pointer block leaves `HANDOFFS.md` and one row joins `docs/HANDOFFS_ARCHIVE_INDEX.md`

The block (4 lines, 456 B; `HANDOFFS.md` 37,407 B before, 36,951 B after) became the row `| 2 | 2026-10-22 → 2026-10-22 | HANDOFFS-through-2026-10-22-3.md | v1.8.1 |`. Own commit, as the index's rule says (fork Learning #58); the shard's verify script, `bin/check-handoff` and `bin/check-ledger` are run after it. It follows the trim `64ef4966`, taken at the operator's Phase 0 picker answer to trim `HANDOFFS.md` (five receipts to three, on his keep-three rule, trim above four); he ran the `--write` with `!`. Nothing sent upstream.

### 2026-10-23 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-22-3.md` (2 record(s), 57,796 B → 37,407 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-10-22 → 2026-10-22) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-22-3.md`](docs/archive/HANDOFFS-through-2026-10-22-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-22-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-22-3.md.verify.sh)
rather than trusting a digest printed here. Live file 57,796 B → 37,407 B (−35.3%).

### 2026-10-23 · [ad hoc] S370 push -- the 1 commit that was ahead of the fork's `origin` (`650a7ca4..66efb971`) pushed to `origin`; nothing sent upstream

His go-ahead at the Phase 0 picker (the option 'Push 66efb971 to fork origin'): S369's push record `66efb971`, a CHANGELOG-only commit. `origin` is `rmsharp/methodology`, the fork (`git remote get-url origin`); guards run in one script before the push, each failing it: `origin/main` equal to the expected `650a7ca4` after a fresh fetch, `merge-base --is-ancestor` true, ahead/behind `0 1`, no rebase marker, the pushed set exactly `CHANGELOG.md`, nothing staged. The tree was not clean: `dashboard_history.jsonl` carried the dashboard run's line, unrelated to the push and left for the claim. Pushed by sha (`66efb9710010f71c5fb3b06b9799901584d1d38e:refs/heads/main`), read back: `git ls-remote origin refs/heads/main` and `origin/main` both `66efb9710010`, ahead/behind `0 0`. Nothing sent to `KJ5HST/methodology`.

### 2026-10-23 · [ad hoc] S369 push -- the 4 commits that were ahead of the fork's `origin` (`c2be6a0b..650a7ca4`) pushed to `origin`; nothing sent upstream

His go-ahead after the close-out report ('push'), one set: S368's push record `5fd05af6`, then S369's claim `e17e350a`, work `df7ee124` and close-out `650a7ca4`. `origin` is `rmsharp/methodology`, the fork (`git remote -v`); fast-forward checked against a freshly fetched `origin/main` (`merge-base --is-ancestor`, ahead/behind `0 4`, clean tree, no rebase marker), pushed by sha (`650a7ca4561f:refs/heads/main`), read back: `origin/main` and `git ls-remote` both `650a7ca4561f`, ahead/behind `0 0`. Nothing sent to `KJ5HST/methodology`

### 2026-10-23 · [ad hoc] S369 close-out -- decision D4's wait settled: it ends on 2026-10-25 whatever #92 and #94 do, recorded in the D4 record; the receipt complete; nothing sent upstream

The one deliverable (a decision record) is done: `docs/planning/pr-composition-evidence/d1-d4-record.md` section 5, commit `df7ee124fc00`, claim `e17e350a91ec`. The `HANDOFFS.md` receipt is `status: complete` (self 8, predecessor S368 scored 9); S370's Phase 0 trims two receipts (five at rest). Gates 24/24 pass, 0 unmeasured, results `873329624aaf`, manifest `98c8c8024d0e` in a clean clone of the work commit (1,474 s; identical to S368's citation, as expected for a text change). No row appended to `docs/FORK_LEARNINGS.md` (rows considered: #28, #48), so D3's retirement duty does not fire. Memory notes outside the repository updated. `main` is 4 commits ahead of `origin` (S368's push record, then S369's claim, work and this close-out). Nothing sent upstream

### 2026-10-23 · [ad hoc] S369 -- decision D4's wait is clarified and recorded: it ends on 2026-10-25 whatever #92 and #94 do (`docs/planning/pr-composition-evidence/d1-d4-record.md` section 5); fork `main` only; nothing sent upstream

Asked at his S369 picker because S368's receipt (gotcha 4) found that what ends the wait was not written down: the plan's section 7 (line 223) says '#94 and #92 to merge or be answered', his 2026-10-18 answer (the record's line 12) names only a date. Three readings offered; his answer: **the date alone**. The maintainer's replies of 2026-10-19 (#92 `6257621669`, #94 `6258571753`) and the fork's answers (`6272223306`, `6275751677`) were read first; both pull requests are open, 2 comments each. The record gained section 5 (23 lines) and one cross-reference at section 4 item 1; no earlier line was changed, and the plan (at its 30,000 B gate) was not touched. It starts nothing and authorises nothing outward: on or after 2026-10-25 a session asks the plan's follow-up (stack on #94's head or state that PR5 supersedes it, if #94 is still open), and each outward step keeps its own go-ahead. `check-links`, `check-backlog-anchors` and `check-ledger` exit 0

### 2026-10-23 · [ad hoc] S369 claim (in progress) -- settle what ends decision D4's wait before PR5 and record his answer in `docs/planning/pr-composition-evidence/d1-d4-record.md`; fork `main` only; nothing sent upstream

Claimed at his Phase 0 picker: the recommended deliverable, taken from S368's receipt (gotcha 4). Phase 0 (read 2026-10-23) found both frontiers current (`CHANGELOG.md` at `5fd05af6`, `HANDOFFS.md` at `c2be6a0b` with one ledger-only push record after it, which owes no receipt; 0 undocumented commits, 0 merges, no pending receipt), `check-ledger` and `check-handoff` exit 0 with 4 receipts (48,698 B of 65,536 B, so no trim this session), pull requests #96 (`ad5c980`, 0 comments), #94 (`1670c5d`, 2) and #92 (`8a232bb`, 2) and issues #93 (1) and #95 (0) open and unchanged, `upstream/main` `f34769f3`, dashboard 72/100 with 0 high-risk flags. The local `.quality-gates-results.json` is from 2026-10-10 (18 gates), so S368's 24/24 citation is neither contradicted nor confirmed by it; no `--run` this Phase 0. `main` is one commit ahead of `origin` (S368's push record). The dashboard refresh's one `dashboard_history.jsonl` line rides this claim, as in S364 to S368

### 2026-10-23 · [ad hoc] S368 push -- the 9 commits that were ahead of the fork's `origin` (`e9c266b1..c2be6a0b`) pushed to `origin`; nothing sent upstream

His go-ahead after the close-out report ('push'), one set: S367's claim, work, closure and close-out, then S368's trim, fold, claim, work and close-out. Fast-forward checked against a freshly fetched `origin/main` (`merge-base --is-ancestor`, ahead/behind `0 9`), `origin` confirmed to be `rmsharp/methodology` and not `KJ5HST/methodology`, pushed by sha, then read back: `git ls-remote origin refs/heads/main`, `origin/main` and the local branch all read `c2be6a0b`, ahead/behind `0 0`; `upstream/main` still `f34769f3`. This entry's own commit is not pushed (the standing grant would allow it, but pushing a push record needs another record); it rides the next push. The S368 receipt's 'nine commits ahead of `origin`' (next_steps 6) was true when written and is now `0`.

### 2026-10-23 · [ad hoc] S368 close-out -- the S340 review's three 'D4's date is superseded' sentences corrected in place; the receipt trimmed 5 to 3 and folded; the receipt complete; nothing sent upstream

Fork `main` only. The session's actions, each with its own entry below: the receipt trim `aa4cdb60` (he ran the `--write`), its fold `ad9490c9`, the claim `fb8f2134` and the correction `6466f492`. Gate run: 24/24 pass, 0 fail, 0 unmeasured (results `873329624aaf`, manifest `98c8c8024d0e`) in a clean `--no-local` clone of `6466f492`, 1,476 s; `tests-sh-passed` 660 against its floor of 660. The predecessor (S367) scored 9; this session's self-score is 8. No row was appended to `docs/FORK_LEARNINGS.md` (rows #81, #28 and #97 already state the lesson), so the retirement duty does not fire. `HANDOFFS.md` now holds four receipts (S368, S367, S366, S365): no trim at the next Phase 0, a trim of two at the one after. Nothing was pushed: `main` is 9 commits ahead of the fork's `origin` (`e9c266b1`), and the standing grant covers a ledger-only push record, nothing wider.

### 2026-10-23 · [ad hoc] S368 -- the S340 review's three 'D4's date is superseded' sentences corrected in place (`docs/planning/backlog-interaction-review-2026-10-18.md` lines 203, 286, 449) and one dated correction note added to its Status line (line 3); fork `main` only; nothing sent upstream

Each sentence said decision D4's 2026-10-25 date was superseded because the maintainer's replies had arrived. His answers say otherwise: D4 itself (`docs/planning/pr-composition-evidence/d1-d4-record.md:12`, `:80`: 'no earlier than 2026-10-25 unless he changes D4'), given 2026-10-18, and 'Yes, D4 stands' at S367's picker on 2026-10-23, asked after the replies were known. The replacement text says only what the sources show, each re-read in this session: the maintainer's first replies came on 2026-10-19 (#92 at 01:19Z, 'three things I'd like changed'; #94 at 02:47Z, 'Requesting changes'), the fork answered the same day (#92 at 16:39Z, head `8a232bb`; #94 at 19:42Z, head `1670c5d`), and both pull requests were still open and unmerged on 2026-10-23. The class scan found the claim in three places, not the two S367's receipt named (the third, line 286, is the same sentence in other words); no other file in the repository states it (the evidence file `backlog-interaction-review-evidence/findings.md` and `upstream-pr-body.md` give the date without calling it superseded). No line was added or removed (452 lines before and after; 82,522 B to 83,141 B), every change is one contiguous substitution inside its sentence (checked by comparing each changed line with `HEAD`'s), line 203's trailing `…` and the rest of the review are untouched, and no gate or test names the review file. `check-links`, `check-backlog-anchors` and `check-ledger` exit 0.

### 2026-10-23 · [ad hoc] S368 claim (in progress) -- correct the S340 review's 'D4's date is superseded' lines (203, 449, and a third instance at 286); fork `main` only; nothing sent upstream

Claimed at his Phase 0 picker: the recommended deliverable, one of the open calls S367's receipt listed. Phase 0 (read 2026-10-23) found both frontiers at `e056ee17` (0 undocumented commits, 0 merges, no pending receipt), `check-ledger` and `check-handoff` exit 0, pull requests #96 (head `ad5c980`, 0 comments), #94 (`1670c5d`, 2) and #92 (`8a232bb`, 2) and issues #93 (1) and #95 (0) open and unchanged, `upstream/main` `f34769f3`, dashboard 72/100 with 0 high-risk flags. The local `.quality-gates-results.json` is from 2026-10-10 (18 gates), so S367's 24/24 citation is neither contradicted nor confirmed by it; no `--run` this Phase 0. The class scan for the deliverable found the claim in three places in the review, not two; the third (line 286) is the same defect and is fixed with the other two. The dashboard refresh's one `dashboard_history.jsonl` line rides this claim, as in S364 to S367.

### 2026-10-23 · [ad hoc] S368 fold -- the trim's pointer block leaves `HANDOFFS.md` and one row joins `docs/HANDOFFS_ARCHIVE_INDEX.md`

The block (4 lines, 456 B; `HANDOFFS.md` 38,650 B before, 38,194 B after) became the row `| 2 | 2026-10-22 → 2026-10-22 | HANDOFFS-through-2026-10-22-2.md | v1.8.1 |`. Own commit, as the index's rule says (fork Learning #58); the shard's verify script, `bin/check-handoff` and `bin/check-ledger` are run after it. It follows the trim `aa4cdb60`, taken at the operator's Phase 0 picker answer to trim `HANDOFFS.md` (five receipts to three, on his keep-three rule, trim above four); he ran the `--write` with `!`. Nothing sent upstream.

### 2026-10-23 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-22-2.md` (2 record(s), 57,176 B → 38,650 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-10-22 → 2026-10-22) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-22-2.md`](docs/archive/HANDOFFS-through-2026-10-22-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-22-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-22-2.md.verify.sh)
rather than trusting a digest printed here. Live file 57,176 B → 38,650 B (−32.4%).

### 2026-10-23 · [BL-125] S367 close-out -- BL-125 closed by decision (the five plans inside their budgets stay ungated; the sixth's header records its 451 B overage); S366's 7 commits pushed to the fork; D4's 2026-10-25 date confirmed to stand; the receipt complete; nothing sent upstream

Phase 3, in order. **3A:** S366's handoff scored **9** (every cited anchor re-read in the files, not from memory: `bin/check-handoff:933`, `:1011`, `:1234`, `:101`, `:1297`, `:1312`, Test 60 at `bin/tests.sh:5202`, `.quality-gates.json:43` and `:36`, BL-126's closing row at `BACKLOG-COMPLETED.md:150`; its `gh` states for all five upstream threads, '4 receipts, no trim' and '7 ahead' were each exact). Missing, small: it did not say the 2026-10-25 date it repeats is called superseded by the S340 review, and BL-125's row gives last-change dates from the default `git log` walk without saying the full-history walk lists 10 more commits (resync merges; the file hashes settle it). **3B:** self **8**. **3C:** no row appended to `docs/FORK_LEARNINGS.md`, so D3's retirement duty does not fire; rows considered: #59 (a plan's open decision closed by events; the nearest, this session's date conflict is its mirror), #103 (`git log -- <path>` drops merges; applied: both walks, then file hashes), #34 (a ceiling guards a cost; the reason the five are not gated); none is retired, because none meets (a), (b) or (c). **3E:** `quality_ratchet.py --run` in a clean `--no-local` clone of the closure commit `2e095672e785` (5 receipts in the tree): **24/24 pass · 0 fail · 0 unmeasured · results `873329624aaf` · manifest `98c8c8024d0e`**, 1,351 s, load about 9; identical to S366's citation, as expected when no test and no gate changed, which also settles Phase 0 step 6's check of that citation. **A conflict found and put to him:** his D4 answer (S339, 2026-10-18: 'keep waiting, ask again on or after 2026-10-25'; `pr-composition-evidence/d1-d4-record.md:12`) against the S340 review's lines 203 and 449 ('the date no longer governs': the maintainer replied on #92 and #94 on 2026-10-19, after his answer). His answer at the S367 picker (2026-10-23): **'Yes, D4 stands'**, so the date governs and PR5 still needs the maintainer's outcome on #92 and #94 and his three separate go-aheads. The review's two lines are wrong and are not edited this session (outside BL-125). The claim entry's 'D8's PR5 cannot start before 2026-10-25' stands as written. Memory notes updated (outside the repository).

### 2026-10-23 · [BL-125] S367 -- close BL-125 (decided: the five plans inside their budgets stay ungated; the sixth's header records its 451 B overage); fork `main` only; nothing sent upstream

The three edits of a closure, run by one guarded script (each step asserts its match count): BL-125's index row out of `docs/planning/BACKLOG.md` (44 open rows to 43), `BL-125` into the Completed id list between `BL-124` and `BL-126` (84 ids to 85, recomputed against the rows of `BACKLOG-COMPLETED.md`: 85 and 85, no difference), and its closing row appended to `BACKLOG-COMPLETED.md` (its rows run in closing-date order; BL-126's was last). The body in `BACKLOG-DETAIL.md` under `bl-125` is untouched, because the detail proof pins it. Each proof run alone from the repository root, exit 0: the three `.verify.sh` (`BACKLOG-COMPLETED.md`, `BACKLOG-DETAIL.md`, `BACKLOG-archive-2026-08-15.md`), `check-backlog-anchors` (84 links on 102 anchors), `check-links` and `check-ledger`. No test and no gate changed, so the `tests-sh-passed` floor (660) stays. Work commit `709fa1f0`.

