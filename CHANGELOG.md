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

---

## 2026-09

## 2026-10

### 2026-10-20 · [BL-102] S350 close-out -- BL-102 done (quality_ratchet.py 1.5.1: install-hook resolves the tool's directory); the receipt complete; nothing sent upstream

The `HANDOFFS.md` receipt is `status: complete` (self 8, predecessor S349 scored 8). Gate run after the claim, in a clean `--no-local` clone of `8e2397b4`: 22/22 pass, 0 fail, 0 unmeasured, results `8b85fe699a30`, manifest `abeec4246a80`, 1266 s (`ratchet-unit-tests` 123, `tests-sh-passed` 523, `tests-sh-failed` 0). Also in this commit: the close-out dashboard line in `dashboard_history.jsonl` (72/100, medium, 0 high; the Phase 0 line was restored away and is not in history) and the mutation script `docs/planning/bl102-evidence/mutate-bl102.py` (6 mutants, 5 killed, 1 equivalent), so the round can be re-run. Phase 3C appended no row to `docs/FORK_LEARNINGS.md` (rule D3 not triggered; rows #23 and #57 considered). Pushing `main` to the fork's `origin` is asked at the close-out picker; nothing was sent to `KJ5HST/methodology`.

### 2026-10-20 · [BL-102] S350 -- BL-102 closed in the backlog files (row out of `BACKLOG.md`, id into its Completed list, completed row into `BACKLOG-COMPLETED.md`); open index rows 52 to 51

The three edits of a close; `BACKLOG-DETAIL.md` untouched (its proof pins the pre-split bodies). Read after the edit, each exit 0: `BACKLOG-COMPLETED.md.verify.sh`, `BACKLOG-DETAIL.md.verify.sh`, `BACKLOG-archive-2026-08-15.md.verify.sh`, `bin/check-backlog-anchors` and `bin/check-links`. The completed row records the reason for the directory-only shape, the 1.5.1 reach and the not-repaired already-installed hook; the work is in the entry below (commit `0df0bae8`).

### 2026-10-20 · [BL-102] S350 -- `quality_ratchet.py` 1.5.1: `install-hook` resolves the tool's directory, so a hook installed through a symlinked path keeps its layout twin (three tests, floor 120 to 123); fork only, nothing sent upstream

**The defect, reproduced today** (a scratch repository reached through a symlinked directory, the tool started by its absolute symlinked path): 1.5.0 wrote `for t in "../../link/proj2/quality_ratchet.py"` into the hook, with no twin in the other layout, and the first commit after `methodology/` took the files was refused with `not found ... refusing, not passing`. Run from inside the directory the hook came out right (Python's working directory is the real path), so the trigger is an absolute path through a symlink, which is what `tempfile.mkdtemp()` gives on macOS. **The fix** (`starter-kit/quality_ratchet.py`, `install_hook`, about +4 lines): the tool's DIRECTORY and git's toplevel are resolved with `realpath`, and the file keeps its own name. This differs from the backlog row's shape (`realpath` of the whole file, as `context_budget.py` does), by his approval of the plan: measured on a scratch repository, a tool file that is itself a symlink gets `../../shared/qr.py` under the row's shape (a path outside the repository, no twin) and `quality_ratchet.py` plus its twin under this one; both fix the reported case. **Held by** `TestTheHookFromASymlinkedPath` (3 tests, written first: two red on 1.5.0 for the right reasons, the third green on 1.5.0 by design; the suite reads `Ran 123 tests ... OK`, 68 s, from 120; the gate floor `ratchet-unit-tests` 120 to 123) and a mutation round of 6 mutants, 5 killed (the row's whole-file shape is killed by the symlinked-file test alone); the survivor drops `realpath` on git's toplevel, which git already reports as a real path, so it is equivalent here. `--selftest` 30 checks OK. Hand run with the final tool: a real commit through the real hook after the pure move exits 0, and a loosening from the moved location is refused (exit 1). **Not changed:** `context_budget.py` (it resolves the whole file and so has the symlinked-file edge this fix avoids), `pr2/candidate` (BL-102 reaches upstream only as one added candidate commit: his call), `.githooks/pre-commit`. **Adopter impact:** the change is the path written at install time. A hook already installed with a bad path is left alone (`install-hook` says `already installed`), so an affected adopter deletes `.git/hooks/pre-commit` (or the file under `core.hooksPath`) and re-runs `python3 quality_ratchet.py install-hook` after their next `bin/sync`. On a platform that will not create a symlink the three tests skip with the reason; that is unchecked there, not passed.

### 2026-10-20 · [BL-102] S350 claim (in progress) -- fix the ratchet's hook installer so a symlinked checkout keeps its layout twin (`quality_ratchet.py` 1.5.0 to 1.5.1); nothing sent upstream

Claimed at the operator's Phase 0 picker answer "BL-102: fix the hook installer (Recommended)", after the `HANDOFFS.md` trim (`968b403c`), its fold (`f5e16323`) and the push of `main` to the fork's `origin` (both ticked at the same picker). Phase 0: both ledger frontiers current, 0 undocumented commits, no pending receipt, `check-ledger` and `check-handoff` exit 0, dashboard 72/100 (medium, 0 high); #96, #94, #92 open and unanswered by the maintainer, #93 and #95 unchanged, `upstream/main` `f34769f3`. Phase 3F records the rest.

### 2026-10-20 · [ad hoc] S350 -- push record: fork `main` to the fork `origin` at the operator's Phase 0 picker (`fbb6ea93` to `f5e16323`), head read back

At the picker answer "Push main to your fork", `git push origin main` (`https://github.com/rmsharp/methodology.git`, the fork) moved `main` from `fbb6ea93` to `f5e16323` (3 commits: S349's push record, the `HANDOFFS.md` trim and its fold). Read back: `git ls-remote origin refs/heads/main` and the local `HEAD` both read `f5e16323d53bba1754104d8b003d0ed49d568f37`, and `git rev-list --count origin/main..HEAD` read 0. Nothing was sent to `KJ5HST/methodology` by this push.

### 2026-10-20 · [ad hoc] S350 -- the HANDOFFS trim's pointer block folded into the archive index (the trim itself is the tool's entry below, commit `968b403c`, ticked at the S350 Phase 0 picker)

The fold, in its own commit as the index's rule says: the pointer block left `HANDOFFS.md` (38,906 B to 38,450 B) and one row joined `docs/HANDOFFS_ARCHIVE_INDEX.md` (`| 1 | 2026-10-19 → 2026-10-19 | HANDOFFS-through-2026-10-19-6.md | v1.8.1 |`). Taken before the session claim, as S349's handoff asked. Read back after the edit: the shard's verify script, `check-handoff` and `check-ledger` exit 0 (results in the commit that follows this entry's).

### 2026-10-20 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-19-6.md` (1 record(s), 48,713 B → 38,906 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-19 → 2026-10-19) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-19-6.md`](docs/archive/HANDOFFS-through-2026-10-19-6.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-19-6.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-19-6.md.verify.sh)
rather than trusting a digest printed here. Live file 48,713 B → 38,906 B (−20.1%).

### 2026-10-20 · [ad hoc] S349 -- push record: fork `main` to the fork `origin` at the operator's close-out picker (`c822b6a0` to `fbb6ea93`), head read back

At the picker answer "Yes, push main to origin (Recommended)", `git push origin main` (`https://github.com/rmsharp/methodology.git`, the fork) moved `main` from `c822b6a0` to `fbb6ea93` (5 commits: the trim, its fold, the push record, the claim and the close-out). Read back: `git ls-remote origin refs/heads/main` and the local `HEAD` both read `fbb6ea93796c36cde4521d29c03c686c2bd48ab0`, and `git rev-list --count origin/main..HEAD` read 0. Nothing was sent to `KJ5HST/methodology` by this push.

### 2026-10-20 · [BL-79] S349 close-out -- BL-79 P3 delivered as upstream pull request #96 (the Phase 3G report tool, copy-it shape); the receipt complete; BL-79 stays open for the follow-up

Phase 3 of the session whose claim stands below (`CHANGELOG: pending` is resolved by this entry and the entries between). The `HANDOFFS.md` receipt is `status: complete` (self 8, predecessor S348 scored 7). Gate run, taken in a clean `--no-local` clone of the claim `480fbb22` (4 receipts in the tree): `quality_ratchet.py --run` read 22/22 pass, 0 fail, 0 unmeasured, results `6e76a92566cf`, manifest `9ce337f6c51d` (equal to S348's because this session changed no code, gate or manifest on the fork; after that clone it changed only the ledgers, the `BL-79` index row in `docs/planning/BACKLOG.md` and a status paragraph in the actuator plan, and the three backlog proofs and `check-backlog-anchors` exit 0 on the edited tree). The fork's shell suite was read through the ratchet's `tests-sh-passed` gate (523); the upstream branch's own readings (262 passed, 13/13) are in the branch entry below. Phase 3C appended no row to `docs/FORK_LEARNINGS.md`, so the retire-or-refuse rule was not triggered; rows considered: #68 (a grep inventory is line-scoped) and #78 (grep every document that already gives the instruction), neither of which states the lesson, and the runner's Evidence-Based Inventory rule, which does: the plan's P3 file list named the manifest row but had never run it, and the row fails five dashboard checks. **Open and his:** whether to follow #96 with distribution (a manifest row, the dashboard's three cross-references, a net-zero-byte section 3G edit); the adopter-facing half of BL-55; whether the third backlog proof becomes a fourth gate; BL-121, BL-122, D8's PR5 (earliest 2026-10-25) and BL-94's third run. Nothing else was sent to `KJ5HST/methodology`: pull request #96 only, recorded above.

### 2026-10-20 · [BL-79] S349 -- non-commit action: opened upstream pull request #96 (`KJ5HST/methodology`) for the Phase 3G report tool, at the operator's go-ahead

At the picker answer "Open the PR against KJ5HST/methodology", `gh pr create -R KJ5HST/methodology --base main --head rmsharp:feat/close-out-report-tool` opened [#96](https://github.com/KJ5HST/methodology/pull/96), titled "feat(close-out): print and lint the Phase 3G close-out report (canonical-only tool; copy it)". The text had been shown to him in full before the picker. Read back with `gh pr view 96 --json ...`: OPEN, not a draft, base `main`, head `ad5c980f`, MERGEABLE, nine files, and the body byte-identical to the file shown (4,748 characters; scanned beforehand for session numbers, backlog codes and fork names: none). `upstream/main` was still `f34769f3`. No comment, label or reviewer was added.

### 2026-10-20 · [BL-79] S349 -- push record: branch `feat/close-out-report-tool` to the fork `origin` at the operator's picker, head read back

At the picker answer "Push the branch to my fork's origin", `git push origin feat/close-out-report-tool:refs/heads/feat/close-out-report-tool` created the branch on `https://github.com/rmsharp/methodology.git` (the fork). Read back: `git ls-remote origin refs/heads/feat/close-out-report-tool` and the local branch both read `ad5c980f345758df3dae8276e778c0883ded833c`. Done before the pull request was opened, as the read-back rule says.

### 2026-10-20 · [BL-79] S349 -- built branch `feat/close-out-report-tool` off `upstream/main` (`f34769f3`): the Phase 3G report tool, its tests and gate (`71224c57`), the pointers (`ad5c980f`)

BL-79 P3, in a narrower shape than the plan's. Built in a `git worktree` in the session scratchpad, so the fork's `main` was never touched by it. **Layer 1, `71224c57`** (5 files): `starter-kit/close_out_report.py` is `816834cb`'s file (the version before the fork-only layout resolver) with three docstring lines reworded so none cites the plan; `tools/test_close_out_report.py` is `816834cb`'s with three kinds of edit (the receipt-count floor 100 to 30, because upstream keeps 38 complete receipts and not the fork's 250; the unscored-receipt pin keyed by session and date, not by the archive file a trim may move it to; comments that cited fork-only documents), still 68 tests; `bin/tests.sh` +7; `.quality-gates.json` gate `close-out-report-unit-tests` (min 68) and `tests-sh-passed` 261 to 262; a ledger entry. **Layer 2, `ad5c980f`** (5 files): `starter-kit/SAFEGUARDS.md` +544 B, the settings snippet in `starter-kit/BOOTSTRAP.md` Step 10 (parses as JSON), two rows each in `README.md` and `CLAUDE.md`, a ledger entry. **Measured on upstream's tree:** the new suite 68 of 68; `bash bin/tests.sh` 262 passed, 0 failed (261 before; run twice, the second after the docs layer); `quality_ratchet.py --run` in a clean `--no-local` clone 13/13, 0 unmeasured (results `eb80868f2ec2`, manifest `ecdb6798d483`); `git merge-tree` clean against #92 (`8a232bb`) and #94 (`1670c5d`), separately and together. **The distribution attempt, stated:** adding the `bin/_manifest.py` row (plus an adopter-copy block in `bin/tests.sh`) failed five checks in `tools/test_methodology_dashboard.py` (the installed-source tuple, its per-name entry and the checklist exemption); upstream's last tool addition paid about 31 lines in each dashboard twin for the same coupling. He chose "Copy-it, like check-handoff (Recommended)" at a picker, so the row was reverted (the 45-line patch was kept only in the vanished scratchpad). **Mistake, recovered:** upstream's ledger hook refused `git commit --amend` because it edited an already-committed entry; the branch was unpushed, so layer 1 was recommitted from a soft reset rather than bypassed with `--no-verify`.

### 2026-10-20 · [BL-79] S349 claim (in progress) -- prepare the Phase 3G close-out report tool as a small upstream pull request (BL-79 P3); nothing sent upstream

CHANGELOG: pending. Taken at the operator's request ("incorporate the formatted close-out report script ... Make this a small PR for upstream if not already there") and his Phase 0 picker answers "Trim HANDOFFS.md to 3 (Recommended)" and "Push main to the fork's origin" (the trim `b4e23e8b`, the fold `66c4244e` and the push record `9790eca3` done first). Phase 0 checked that the tool is not on `upstream/main` (`f34769f3`) and not in the open PR #92 (files: `CHANGELOG.md`, `CLAUDE.md`, `README.md`) or #94 (files: `.quality-gates.json`, `CHANGELOG.md`, `FRAMEWORK_APPARATUS.md`, `starter-kit/methodology_trim.py`, `tools/test_methodology_trim.py`); the fork carries it in four commits (`b34a841d` P1, `816834cb` P2, then two layout-resolver commits upstream cannot use). Opens the `status: pending` receipt; the Phase 0 dashboard line rides this commit. Nothing is pushed or opened without the operator's separate go-ahead. Phase 3F records the outcome.

### 2026-10-20 · [ad hoc] S349 -- the HANDOFFS trim's pointer block folded into the archive index (the trim itself is the tool's entry below, commit `b4e23e8b`, ticked at the S349 Phase 0 picker)

The fold, in its own commit as the index's rule says: the pointer block left `HANDOFFS.md` (37,888 B to 37,432 B) and one row joined `docs/HANDOFFS_ARCHIVE_INDEX.md` (`| 1 | 2026-10-19 → 2026-10-19 | HANDOFFS-through-2026-10-19-5.md | v1.8.1 |`). Taken before the session claim, as the retention rule says.

### 2026-10-20 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-19-5.md` (1 record(s), 47,832 B → 37,888 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-19 → 2026-10-19) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-19-5.md`](docs/archive/HANDOFFS-through-2026-10-19-5.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-19-5.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-19-5.md.verify.sh)
rather than trusting a digest printed here. Live file 47,832 B → 37,888 B (−20.8%).

### 2026-10-20 · [ad hoc] S349 -- push record: fork `main` to the fork `origin` at the operator's Phase 0 picker (`31cc13a9` to `c822b6a0`), head read back

At the picker answer "Push main to the fork's origin", `git push origin main` (`https://github.com/rmsharp/methodology.git`, the fork) moved `main` from `31cc13a9` to `c822b6a0` (one commit: the S348 correction of the Phase 3G lapse and the `self_score`). Read back: `git ls-remote origin refs/heads/main` and the local `HEAD` both read `c822b6a02c1c887044fa82e8f2bb3d8e1328b7df`, and `git rev-list --count origin/main..HEAD` read 0. The trim and its fold were committed after the push and are local. Nothing was sent to `KJ5HST/methodology`.

### 2026-10-20 · [BL-79] S348 correction -- the closing message was not the Phase 3G report; `self_score` 8 to 7 in the S348 receipt

The operator wrote "This does not look like the Phase 3 close-out report" after S348's final message. It was an unlabelled summary, and an earlier near-report had gone out before the push and its push record, so no message reported the final state in the 3G shape (heading, the four labelled items, `Session over.`). This is the fourth occurrence of the lapse BL-79 describes (S202, S218, S230, now S348), with the rule in my own notes. Corrected in the durable record: the S348 receipt's `self_score` is 7 (it was 8) and its 3B text names the lapse. The correction commit is local until the operator says to push (the push record `31cc13a9` already on the fork's `origin` carries the old score). BL-79's index row is unchanged: it already records the tool (`starter-kit/close_out_report.py`) and its P3 stays his go-ahead.

### 2026-10-20 · [ad hoc] S348 -- push record: fork `main` to the fork `origin` at the operator's close-out picker (`ad923837` to `64cc7d7f`), head read back

At the operator's close-out picker answer ("Yes, push main to origin (Recommended)"), `git push origin main` (`https://github.com/rmsharp/methodology.git`, the fork) moved `main` from `ad923837` to `64cc7d7f` (7 commits: the two trims and the fold, the claim, the work, the close and the close-out). Read back: `git ls-remote origin refs/heads/main` and `origin/main` both read `64cc7d7f381d6e3cc4318bf9a4054e346016b669`, equal to the local head. Nothing was sent to `KJ5HST/methodology`.

### 2026-10-20 · [ad hoc] S348 close-out -- BL-113 done (the candidate's `layer-verify.sh` runs the budget tool; the composition plan's 'Not carried' cell excepts the density row); the receipt complete; nothing sent upstream

The `HANDOFFS.md` receipt is `status: complete` (self 8, predecessor S347 scored 8). Readings, each in a clean `--no-local` clone: `bash bin/tests.sh` 523 passed, 0 failed, 0 skipped (clone of `55364ba1`); the fork's ratchet 22/22, 0 unmeasured, results `6e76a92566cf`, manifest `9ce337f6c51d` (clone of `1aa39e67`; no code or manifest changed since S347's run, so the hashes are equal); the whole `layer-verify.sh` at the candidate tip `3cba1e50` ends at `layer-verify done` with `budget exit 0`. Phase 3C: no row appended to `docs/FORK_LEARNINGS.md` (the retire-or-refuse rule was not triggered). Open index rows 53 to 52. The sequence this session: Phase 0 report, the two trims (`6874d33d`, fold `f60b5798`, `aadb439e`, each at his tick), the claim `499af9d2`, the work `55364ba1`, the close `1aa39e67`.

### 2026-10-20 · [BL-113] S348 -- BL-113 closed: row out of `docs/planning/BACKLOG.md`, id into its Completed list, completed row into `BACKLOG-COMPLETED.md`

The three-edit close for the work commit `55364ba1`. The three backlog proofs (`BACKLOG-COMPLETED.md.verify.sh`, `BACKLOG-DETAIL.md.verify.sh`, `BACKLOG-archive-2026-08-15.md.verify.sh`) and `bin/check-backlog-anchors` (92 links on 96 anchors) and `bin/check-links` exit 0; open index rows 53 to 52. `BACKLOG-DETAIL.md` is untouched (its proof pins the body).

### 2026-10-20 · [BL-113] S348 -- `layer-verify.sh` now runs the budget tool and prints its verdict line and exit code; the composition plan's 'Not carried' cell excepts the one `.context-budget.json` row `ced2c82` carries

Two edits, one deliverable. `docs/planning/pr-composition-evidence/layer-verify.sh` (+6 / -2) gained `python3 starter-kit/context_budget.py --status | grep -E 'over budget|exceeds'` and `echo "budget exit ${PIPESTATUS[0]}"` after the layout scanner's lines, in the same style, with the header naming the line and its pass condition (exit 0). The same lines, taken from the file, run in clean clones: at the pre-fix commit `28f99a7` they print "exceeds the 18,900-token ceiling by 21" and exit 2; at `ced2c82` and at the tip `3cba1e50` "nothing over budget" and exit 0. `docs/planning/upstream-pr-composition-plan.md` line 165 now reads `.context-budget.json` (except one row, `ced2c82`), which draft 11 already discloses (`upstream-pr-body.md:32`); the plan went 29,996 to 29,999 B, within its 30,000 B budget, by merging the two stacked S321 and S323 notes in the 'One seam to keep' paragraph without dropping a fact. The density row is KEPT (stripping it would rewrite the candidate from `ced2c82` on). No fork code, distributed file or candidate commit touched; nothing sent upstream.

### 2026-10-20 · [BL-113] S348 claim (in progress) -- add the budget tool's `--status` exit to the candidate's `layer-verify.sh` and amend the composition plan's 'Not carried' cell for the density row; nothing sent upstream

CHANGELOG: pending. Taken at the operator's Phase 0 picker answers: "BL-113: size check in the candidate's verify script (Recommended)", "Trim HANDOFFS.md (Recommended)" and "Trim CHANGELOG.md, dry run first" then "Yes, run it with --force (Recommended)" (the trims `6874d33d` and `aadb439e` and the fold `f60b5798` done first); the plan was shown and approved at "Go as written (Recommended)". Opens the `status: pending` receipt; the Phase 0 dashboard line rides this commit. Phase 3F records the outcome.

### 2026-10-20 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-10-19.md` (89 record(s), 202,864 B → 98,809 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **89** record(s) (2026-10-16 → 2026-10-19) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-10-19.md`](docs/archive/CHANGELOG-through-2026-10-19.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-10-19.md.verify.sh`](docs/archive/CHANGELOG-through-2026-10-19.md.verify.sh)
rather than trusting a digest printed here. Live file 202,864 B → 98,809 B (−51.3%).

### 2026-10-20 · [ad hoc] S348 -- the HANDOFFS trim's pointer block folded into the archive index (the trim itself is the tool's entry below, commit `6874d33d`, ticked at the S348 Phase 0 picker)

The fold, in its own commit as the index's rule says: the pointer block left `HANDOFFS.md` (37,207 B to 36,751 B) and one row joined `docs/HANDOFFS_ARCHIVE_INDEX.md` (`| 1 | 2026-10-19 → 2026-10-19 | HANDOFFS-through-2026-10-19-4.md | v1.8.1 |`). Taken before the session claim, as the retention rule says.

### 2026-10-20 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-19-4.md` (1 record(s), 46,746 B → 37,207 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-19 → 2026-10-19) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-19-4.md`](docs/archive/HANDOFFS-through-2026-10-19-4.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-19-4.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-19-4.md.verify.sh)
rather than trusting a digest printed here. Live file 46,746 B → 37,207 B (−20.4%).

### 2026-10-20 · [ad hoc] S347 -- push record: fork `main` to the fork `origin` at the operator's close-out picker (`e821a5a9` to `8c8374e8`), head read back

At the operator's close-out picker answer ("Yes, push main to origin (Recommended)"), `git push origin main` moved the fork's `main` from `e821a5a9` to `8c8374e8` (8 commits: the trim, its fold, the claim, the gate, the tests, the header line, the backlog close and the close-out). Read back: `git fetch origin` and `git ls-remote origin refs/heads/main` read `8c8374e8`, equal to local `main`. Nothing was sent to `KJ5HST/methodology`.

### 2026-10-20 · [ad hoc] S347 close-out -- BL-109, BL-111 and BL-112 done (a failing-suite gate, three checker tests, the exit-4 header line); the receipt complete; nothing sent upstream

Phase 3 of the session whose claim stands below (`CHANGELOG: pending` is resolved by this entry and the entries between). The session also ran the `HANDOFFS.md` trim at his tick before the claim (`05911d38`) and its fold (`b7760590`), recorded in their own entries. Gate run, taken in a clean `--no-local` clone of `8bbbec14` (4 receipts in the tree, after the claim, outside the trim window): `quality_ratchet.py --run` read 22/22 pass, 0 fail, 0 unmeasured, results `6e76a92566cf`, manifest `9ce337f6c51d`, 1,297 s. The receipt is complete (self-score 8, predecessor S346 scored 8). Phase 3C appended no row to `docs/FORK_LEARNINGS.md`, so the retire-or-refuse rule was not triggered; the lesson (a count gate ignores its command's exit code) is enforced by the gate this session adds; rows considered for a new lesson: #62 and #109, neither stating it. **Found, not fixed (a second deliverable):** `CHANGELOG.md` crossed its trim trigger, 199,407 B against 196,608 B before this entry (`methodology_trim.py --file CHANGELOG.md --check` prints `trigger FIRES`; it was 192,688 B at Phase 0); the next session's Phase 0 offers that trim beside the `HANDOFFS.md` one. Open and his: the adopter-facing half of BL-55; whether the third backlog proof becomes a fourth gate; BL-121, BL-122, D8's PR5 (earliest 2026-10-25) and BL-94's third run. Nothing was sent to `KJ5HST/methodology`.

### 2026-10-20 · [BL-109] S347 -- closed BL-109, BL-111 and BL-112 (the three small guards, one commit each: `aaa9787b`, `33f5ce70`, `8bbbec14`)

Each by the three-edit close: the row out of `docs/planning/BACKLOG.md`, its id into the Completed-items list, a completed row into `docs/planning/BACKLOG-COMPLETED.md`; the detail bodies are untouched (the detail proof pins them). Open index rows 56 to 53 (`grep -oE '^\| \*\*BL-[0-9]+' docs/planning/BACKLOG.md`). **Measured before this commit:** the 22-gate run in a clean `--no-local` clone of `8bbbec14` read `22/22 pass · 0 fail · 0 unmeasured`, 1,297 s, with `migrate-layout-unit-tests-failed` at 0 (the suite green), `checker-layout-unit-tests` at 18, `tests-sh-passed` at 523 (the floor, so the three commits cost the shell suite nothing); the three backlog proofs, `bin/check-backlog-anchors` (92 links on 96 anchors) and `bin/check-links` exit 0 on the working tree with the three rows closed. One correction carried into BL-112's completed row: its body said the file was the same bytes in the fork and the candidate, which is no longer so. Nothing sent upstream.

### 2026-10-20 · [BL-112] S347 -- `bin/migrate-layout`'s header now lists exit 4

Fork-side only; nothing sent upstream. The `Exit:` paragraph of the module docstring stopped at 3 while `main` returns 4 when an apply commits and its after-checks differ from its before-checks or leave the tree dirty (`return 0 if report["checks"]["ok"] else 4`, with `way_back` naming the `git revert`); `tools/test_migrate_layout.py` asserts exit 4 in four places. The two added lines are the pull request candidate's wording, checked against that code before copying. A docstring only: the file parses, `bin/check-layout-literals` reads 0 sites, `tools/test_layout_resolver.py` reads `Ran 75 tests ... OK` and the two fast classes of the migration suite `Ran 95 tests ... OK`. No test was added: the docstring is prose, and a check that every exit a tool returns is listed in its header would be a new rule that is not BL-112's.

### 2026-10-20 · [BL-111] S347 -- three checker tests ported from the pull request candidate to `tools/test_checker_layouts.py`; the gate `checker-layout-unit-tests` 15 to 18

Fork-side only; nothing sent upstream. The three tests the fork's suite lacked, copied unchanged from `pr2/candidate`: `check-ledger --file` is read where the runner does not decide (the refusal tells the user to name the ledger, and that way out has to work), `check-handoff --file` the same (and its output does not say half-migrated), and `check-ledger` with no ledger exits 2 and names the path it looked at. They test behaviour that already worked, so there was no red to see first; the proof is the mutation round instead: **5 mutants, all killed** (check-ledger ignoring `--file`; its no-ledger report omitting the path; its no-ledger exit 1 for 2; check-handoff ignoring `--file`; check-handoff's `--file` still refusing a half-migrated tree), and each of the three new tests is the only one that kills at least one of them. **Measured:** `python3 tools/test_checker_layouts.py` reads `Ran 18 tests ... OK` in 2.8 s, so the gate's floor is 18 (it was 15; `_s347_tightening_bl111` in `.quality-gates.json` holds the figures); `quality_ratchet.py --precommit` exits 0. The mutation script and its output stayed in the session scratchpad.

### 2026-10-20 · [BL-109] S347 -- the gate `migrate-layout-unit-tests-failed` (max 0, the same command as the count gate, no `extract`): a red migration suite now turns a gate red

Fork-side only; nothing sent upstream. `.quality-gates.json` gains the gate (21 to 22 gates) after `migrate-layout-unit-tests`, copied in shape from the pull request candidate's pair (`timeout_seconds` 3600, no `extract`, so the exit code is the measurement) and with the fork's own `why`. The count gate's `why` is corrected: it said "green/red is carried by tests-sh-failed", true of every other suite and not of this one, because `bin/tests.sh` runs only `TestThePureRules` and `TestUsageAndNothingToDo` of it (its comment at `bin/tests.sh:327`). **Measured, not assumed:** `docs/planning/pr-composition-evidence/layer7-pair-proof.py` run against this repository's `starter-kit/quality_ratchet.py` (1.5.0) prints `suite-count measured=5.0 status=pass`, `suite-failed measured=1.0 status=fail`, `command executions: 1`, byte-identical to the recorded output; `quality_ratchet.py --precommit` reports `1 gate(s) added` and exits 0 (adding a gate is a tightening); `config_defects` on the new file is `[]`; `--selftest` builds its own throwaway gate file, so it needs no change (BL-109's "not checked" item). No threshold moved: `tests-sh-passed` stays 523 because `bin/tests.sh` is untouched. The gate's real reading (suite green, exit 0) is taken in the close-out's 22-gate run.

### 2026-10-20 · [BL-109] S347 claim (in progress) -- port three small guards from the pull request candidate to the fork: a failing-suite gate for `migrate-layout-unit-tests` (BL-109), three missing checker tests (BL-111) and `bin/migrate-layout`'s missing exit-4 line (BL-112); nothing sent upstream

CHANGELOG: pending. Taken at the operator's Phase 0 picker answers: "Yes, trim first (Recommended)" (the trim `05911d38` and its fold `b7760590` first) and "BL-109: three small guards". Opens the `status: pending` receipt; the Phase 0 dashboard line rides this commit. Phase 3F records the outcome.

### 2026-10-20 · [ad hoc] S347 -- the HANDOFFS trim's pointer block folded into the archive index (the trim itself is the tool's entry below, commit `05911d38`, ticked at the S347 Phase 0 picker)

The fold, in its own commit as the index's rule says: the pointer block left `HANDOFFS.md` (35,981 B to 35,525 B) and one row joined `docs/HANDOFFS_ARCHIVE_INDEX.md` (`| 1 | 2026-10-19 → 2026-10-19 | HANDOFFS-through-2026-10-19-3.md | v1.8.1 |`). Taken before the session claim, as the retention rule says.

### 2026-10-20 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-19-3.md` (1 record(s), 46,040 B → 35,981 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-19 → 2026-10-19) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-19-3.md`](docs/archive/HANDOFFS-through-2026-10-19-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-19-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-19-3.md.verify.sh)
rather than trusting a digest printed here. Live file 46,040 B → 35,981 B (−21.8%).

### 2026-10-20 · [ad hoc] S346 -- push record: fork `main` to the fork `origin` at the operator's close-out picker (`0a963dbb` to `f2fb6fcb`), head read back

At the operator's close-out picker answer ("Yes, push to origin (Recommended)"), `git push origin main` moved the fork's `main` from `0a963dbb` to `f2fb6fcb` (6 commits: the trim, its fold, the claim, the checker and its test, the gates and the close-out). Read back: `git fetch origin` and `git ls-remote origin refs/heads/main` read `f2fb6fcb166671d7aea4147e9b17ecce8df70314`, equal to local `main`. Nothing was sent to `KJ5HST/methodology`.

### 2026-10-20 · [ad hoc] S346 close-out -- BL-55 fork half done (checker, Test 55, three gates, floor 523); the receipt complete; nothing sent upstream

Phase 3 of the session whose claim stands below (`CHANGELOG: pending` is resolved by this entry and the two BL-55 entries under it). The session also ran the `HANDOFFS.md` trim at his tick before the claim (`70a31eb3`) and its fold (`d6863ec7`), recorded in their own entries. Gate run, taken in a clean `--no-local` clone of `d8021922` (4 receipts in the tree, after the claim, outside the trim window): `quality_ratchet.py --run` read 21/21 pass, 0 fail, 0 unmeasured, results `885c8aa7f389`, manifest `90e0ba15e8c4`, 1200 s; the full suite in a clone of `8721f8f1` read 523 passed, 0 failed, 0 skipped, 426 s. The receipt is complete (self-score 8, predecessor S345 scored 8). Phase 3C appended no row to `docs/FORK_LEARNINGS.md`, so the retire-or-refuse rule was not triggered; rows considered: #107 (a surviving mutant means two guards cover one case: the wrong-body and duplicate cases survived because a second finding contained the wanted word) and #16 (an assertion wired to the artifact), each already stating the lesson at least as generally. Open and his: the adopter-facing half of BL-55; whether the third backlog proof (the frozen August archive's) becomes a fourth gate. Nothing was sent to `KJ5HST/methodology`.

### 2026-10-19 · [BL-55] S346 -- fork half of BL-55 wired: three gates in `.quality-gates.json` (18 to 21), the `tests-sh-passed` floor 503 to 523, and a rider on BL-55's index row

Fork-side only; nothing distributed, nothing sent upstream. The gates: `backlog-completed-proof` and `backlog-detail-proof` (the two hand-written proofs `docs/planning/BACKLOG-COMPLETED.md.verify.sh` and `BACKLOG-DETAIL.md.verify.sh`, each 0.06 s and exit 0 before this and in no gate), and `backlog-anchors` (`bin/check-backlog-anchors`, the entry below). All three are `max 0` on the exit code, the shape of the six checker gates already there; the proofs pin a base commit, so a shallow clone fails them with exit 2 by design. The floor is a measurement: `bash bin/tests.sh` read 523 passed, 0 failed, 0 skipped (exit 0, 426 s) in a clean `--no-local` clone of `8721f8f1` with 4 receipts in the tree, which is 503 plus Test 55's 20; it holds at 3 or more receipts, the window 503 held in (fork Learning #70). The note `_s346_tightening_bl55` in the manifest says so. BL-55's index row in `BACKLOG.md` gains a rider (fork half done; the adopter-facing half, a shipped `[BL-N]` join check or Signal F promoted to a gate, is open and his call); the row stays open and BL-55's body in `BACKLOG-DETAIL.md` is untouched, because the detail proof pins it byte for byte. `BACKLOG.md` grew 389 B (51,724 to 52,113, warn against 65,536). The three backlog proofs and `bin/check-backlog-anchors` exit 0 on the working tree. **Not done:** the 21-gate `quality_ratchet.py --run`, which waits for this commit; `CLAUDE.md` is not edited (137 B over its ceiling already; BL-19 owns that).

### 2026-10-19 · [BL-55] S346 -- `bin/check-backlog-anchors` and Test 55 in `bin/tests.sh`: every link from `BACKLOG.md` and `BACKLOG-COMPLETED.md` into `BACKLOG-DETAIL.md` lands on its own item

Fork-side only, canonical-only tool (not in `bin/_manifest.py`); no distributed file touched, nothing sent upstream. The check S345 left open as BL-55's half. It reads the detail file once and checks four things: every link whose target is `BACKLOG-DETAIL.md#<fragment>` (with or without a path) finds an `<a id>` line; the nearest anchor above each `**BL-N —` heading is `bl-N` (the `bl-58` shape, which a link-only check passes); an anchor holds exactly one heading and none stands above the first anchor; no anchor or heading is written twice. An empty population (no anchors, or no links) is exit 2, never a pass. **Measured:** on the live files 92 links land on 96 anchors, exit 0; on the three files as they stood before S345's repair (`fe1115ca`) it exits 1 with 23 findings: 13 headings with no anchor of their own, 9 dangling links and the one wrong anchor (BL-60 under `bl-58`), exactly S344's and S345's figures. S345's receipt says 157 `[detail]` links; that does not reproduce: the two live files hold 68 `[detail]` links (54 and 14) and 92 links to a detail anchor, 78 `[detail](` in all tracked markdown. Test 55 is 20 assertions, each asserting the message and not only the exit code: 15 were written before the tool existed and all failed with exit 127, 2 more (two links on one line, an orphan anchor mid-file) came before the mutation round and 3 after it. Mutation round, 20 mutants over the tool: the first run killed 12 and left 8 alive, 3 of them loose wanted-text (the wrong-body case wanted only 'BL-60', which a second finding also says; the two duplicate cases wanted only 'duplicate'), 3 behaviours with no named test (a case-folded fragment, an anchor line with trailing text, the heading pattern's parity with `BACKLOG-DETAIL.md.verify.sh`) and 2 that change only a message's wording; the second run killed 18, and the 2 left are the message-only ones, accepted. `bin/check-layout-literals` reads 0 sites over 19 files, `bin/check-links` and `bin/check-learnings` exit 0. **Not yet:** the three gates in `.quality-gates.json` and the `tests-sh-passed` floor, which wait for a measured suite run on this commit.

### 2026-10-19 · [BL-55] S346 claim (in progress) -- fork half of BL-55: the two backlog proofs wired into `.quality-gates.json` as gates, and a check that every `[detail]` link resolves; nothing sent upstream

CHANGELOG: pending. Taken at the operator's Phase 0 picker answers: "Yes, trim first (Recommended)" (the trim `70a31eb3` and its fold `d6863ec7` first) and "BL-55: backlog checks into the gates (Recommended)". Opens the `status: pending` receipt; the Phase 0 dashboard line rides this commit. Phase 3F records the outcome.

### 2026-10-19 · [ad hoc] S346 -- the HANDOFFS trim's pointer block folded into the archive index (the trim itself is the tool's entry below, commit `70a31eb3`, ticked at the S346 Phase 0 picker)

The fold, in its own commit as the index's rule says: the pointer block left `HANDOFFS.md` (36,233 B to 35,777 B) and one row joined `docs/HANDOFFS_ARCHIVE_INDEX.md` (`| 1 | 2026-10-19 → 2026-10-19 | HANDOFFS-through-2026-10-19-2.md | v1.8.1 |`). Taken before the session claim, as the retention rule says.

### 2026-10-19 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-19-2.md` (1 record(s), 47,317 B → 36,233 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-19 → 2026-10-19) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-19-2.md`](docs/archive/HANDOFFS-through-2026-10-19-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-19-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-19-2.md.verify.sh)
rather than trusting a digest printed here. Live file 47,317 B → 36,233 B (−23.4%).

### 2026-10-19 · [ad hoc] S345 -- push record: fork `main` to the fork `origin` at the operator's close-out picker (`221d16e3` to `47cb1da1`), head read back

At the operator's close-out picker answer ("Yes, push main to the fork (Recommended)"), `git push origin main` moved the fork's `main` from `221d16e3` to `47cb1da1` (5 commits: the trim, its fold, the claim, the BL-87 work and the close-out). Read back: `git fetch origin` and `git ls-remote origin refs/heads/main` read `47cb1da1a0cb3ff0595a5db84620f6ce0b2c01f4`, equal to local `main`. Nothing was sent to `KJ5HST/methodology`.

### 2026-10-19 · [ad hoc] S345 close-out -- BL-87 done; the receipt complete; nothing sent upstream

The close-out of the session whose deliverable was BL-87 (the work commit `9fa99210`, the claim `e43a8d8a`, the trim `eb571a7b` and its fold `fe1115ca`). The `HANDOFFS.md` receipt is `status: complete`. The full shell suite in a clean `--no-local` clone of `9fa99210` (4 receipts in the tree, S345 pending) read 503 passed, 0 failed, 0 skipped in 442 s, equal to the `tests-sh-passed` floor of 503. No code changed (the diff over `starter-kit/`, `tools/`, `bin/`, `.githooks/` and `.quality-gates.json` since `5f09130` is empty), so the 18-gate `quality_ratchet.py --run` was not re-run and the receipt cites S338's. No row appended to `docs/FORK_LEARNINGS.md`, so the retire-or-refuse rule (D3) was not triggered; rows considered: #96, #47 and #22. Nothing was sent to `KJ5HST/methodology`.

### 2026-10-19 · [BL-87] S345 -- BL-87 closed: 13 missing `<a id>` separator lines added to `BACKLOG-DETAIL.md` and `bl-58`'s moved, so every `[detail]` link in `BACKLOG.md` and `BACKLOG-COMPLETED.md` resolves

Fork-side only; no distributed file touched, nothing sent upstream. Re-measured on the working tree before any edit: 96 bodies, 83 anchors, 13 bodies with none (BL-47, 48, 49, 59, 60, 64, 65, 67, 73, 94, 96, 97, 98) and nine `[detail]` links dangling (`bl-47`, `bl-48`, `bl-49`, `bl-60`, `bl-64`, `bl-73` in `BACKLOG.md`; `bl-59`, `bl-67`, `bl-97` in `BACKLOG-COMPLETED.md`). A second defect the count did not show: the `bl-58` anchor stood above BL-60's body, so `#bl-58` landed on BL-60 and one span held three bodies. After: 96 anchors for 96 bodies, no span holds more than its own body (a scratch check flagged six spans before, none after), the three backlog proofs exit 0 before and after from the repository root, `bin/check-links` exits 0. The close is the three edits: BL-87's index row out of `BACKLOG.md` (57 rows to 56; the index and §Completed items share no id), its id into the Completed list, its pointer row into `BACKLOG-COMPLETED.md`; the body in `BACKLOG-DETAIL.md` stays and gains a DONE paragraph, and two sentences that said nine links dangle were put in the past tense. **Not done:** shape (b), the check that every `[detail]` link resolves, is BL-55's half and can now ship green; two links to `#bl-41` in the frozen shard `docs/archive/CHANGELOG-through-2026-08-24.md` still dangle (no BL-41 body was ever in the detail file). BL-93's pointer row says BL-87 was 'still open', true when written at S344, and was left as it stood.

### 2026-10-19 · [BL-87] S345 claim (in progress) -- add the missing `<a id>` separator lines to `BACKLOG-DETAIL.md` so every `[detail]` link resolves; nothing sent upstream

CHANGELOG: pending. Taken at the operator's Phase 0 picker answers: "Finish the backlog cleanup: BL-87 (Recommended)" and "Yes, trim first (Recommended)" (the trim `eb571a7b` and its fold `fe1115ca` first). Opens the `status: pending` receipt; the Phase 0 dashboard line rides this commit. Phase 3F records the outcome.

### 2026-10-19 · [ad hoc] S345 -- the HANDOFFS trim's pointer block folded into the archive index (the trim itself is the tool's entry below, commit `eb571a7b`, ticked at the S345 Phase 0 picker)

The fold, in its own commit as the index's rule says: the pointer block left `HANDOFFS.md` (37,365 B to 36,917 B) and one row joined `docs/HANDOFFS_ARCHIVE_INDEX.md` (`| 1 | 2026-10-19 → 2026-10-19 | HANDOFFS-through-2026-10-19.md | v1.8.1 |`). Taken before the session claim, as the retention rule says.

### 2026-10-19 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-19.md` (1 record(s), 47,311 B → 37,365 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-19 → 2026-10-19) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-19.md`](docs/archive/HANDOFFS-through-2026-10-19.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-19.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-19.md.verify.sh)
rather than trusting a digest printed here. Live file 47,311 B → 37,365 B (−21.0%).

### 2026-10-19 · [ad hoc] S344 -- push record: fork `main` to the fork `origin` at the operator's close-out picker (`e6f13e86` to `a6e4079f`), head read back

At the operator's close-out picker answer ("Yes, push main to the fork (Recommended)"), `git push origin main` moved the fork's `main` from `e6f13e86` to `a6e4079f` (5 commits: the trim, its fold, the claim, the BL-93 close and the close-out). Read back: `git fetch origin`, `git ls-remote origin refs/heads/main` and local `HEAD` all read `a6e4079f`, and `git rev-list --left-right --count origin/main...HEAD` reads `0 0`. Only the operator's own fork `rmsharp/methodology` was written; nothing was posted, pushed or edited in `KJ5HST/methodology`. This entry rides a ledger-only commit pushed under the standing grant for push records.

### 2026-10-19 · [ad hoc] S344 close-out -- BL-93 done; the receipt complete; nothing sent upstream

The session's one deliverable, BL-93 (the hand-kept ‘Open:’ list at the top of `docs/planning/BACKLOG.md`), is done in `8662c30c`; the trim `30328c0b` and its fold `fcabfc63` came first at the operator's Phase 0 picker answer, the claim is `8a1da586`. The `HANDOFFS.md` receipt is complete (`status: complete`, predecessor S343 scored 8, self 8). Phase 3C appended no row to `docs/FORK_LEARNINGS.md` (rows considered: #81, #23, #37), so the retire-or-refuse rule was not triggered. `bash bin/tests.sh` in a clean `--no-local` clone of `8662c30c`: 503 passed, 0 failed, 0 skipped, 422 s, equal to the tests-sh-passed floor of 503. Left open and named in the receipt: BL-87's anchors (13 headings, 9 dangling links, measured) and the sweep's relabels (no row). **Nothing was sent to `KJ5HST/methodology`.**

### 2026-10-19 · [BL-93] S344 -- BL-93 closed: the hand-kept ‘Open:’ list deleted; the open items are now derived from the index table

Closed by the three edits: the index row out of `docs/planning/BACKLOG.md`, the id kept in its ‘Completed items’ list, the pointer row into `docs/planning/BACKLOG-COMPLETED.md`. The fix, option (b) of the item's body: the hand-kept list (`BACKLOG.md:9`, 34 of the 58 open rows) is gone, and the top of the file prints `grep -oE '^\| \*\*BL-[0-9]+' docs/planning/BACKLOG.md` as the derivation (58 rows before this close, 57 after; the index table and the ‘Completed items’ id list share no id, measured with the same regex the item's body prints). **A finding on the way:** the grep the file printed beside the list, `grep -nE '^\*\*BL-[0-9]+ —' docs/planning/BACKLOG-DETAIL.md`, is not a derivation of the open set: it returns 96 headings, 40 of them closed items (39 when the session began, 40 once this item closed; each recorded in the ‘Completed items’ list and in `BACKLOG-COMPLETED.md`), because a closed item's body stays in the detail file when its index row goes. So the review's sentence ‘delete the list; the file already prints the command that derives it’ was wrong about the command; the file now says which grep to use and which not to. Also rewritten: the S343 note after the pinned routing block (it named the deleted list). BL-37's ‘half (a) done’ and BL-64's ‘residual only’, which the list carried, live on in BL-37's body and BL-64's row. Not done, and not this item's: the 13 missing anchor lines in `BACKLOG-DETAIL.md` (BL-87's, open) and the index relabels. Option (c), a gate that asserts the two populations agree, was not built. The three backlog proofs exit 0 before and after; `check-ledger` and `check-links` exit 0.

### 2026-10-19 · [BL-93] S344 claim (in progress) -- replace the hand-kept 'Open:' list at the top of the backlog with a derivation; nothing sent upstream

CHANGELOG: pending. Taken at the operator's Phase 0 picker answers: "Fix the backlog's stale 'Open:' line (Recommended)" and "Yes, trim first (Recommended)" (the trim `30328c0b` and its fold `fcabfc63` done first). The deliverable: the first part of BL-93, the hand-kept **Open:** list at `docs/planning/BACKLOG.md:9`, which names 34 of the 58 open index rows. Measured at Phase 0: the grep the file prints beside the list (`BACKLOG-DETAIL.md` headings) returns 96 headings now, 39 of them closed items whose bodies the detail proof pins, so the derivation the replacement points at is the index table itself (58 rows, no extras). NOT in this session: the 13 missing anchor lines in `BACKLOG-DETAIL.md`, bl-58's, the index relabels (the rest of BL-93, which stays open). **Nothing is sent to `KJ5HST/methodology`.** Phase 0 found PR #94 (`1670c5d`) and PR #92 unchanged, with no maintainer reply; issues #93 and #95 unchanged. The Phase 0 dashboard run (72/100, risk medium) appended its line to `dashboard_history.jsonl`, which rides this claim commit.

### 2026-10-19 · [ad hoc] S344 -- the HANDOFFS trim's pointer block folded into the archive index (the trim itself is the tool's entry below, commit `30328c0b`, ticked at the S344 Phase 0 picker)

The fold, in its own commit as the index's rule says: the pointer block left `HANDOFFS.md` (37,772 B to 37,316 B) and one row joined `docs/HANDOFFS_ARCHIVE_INDEX.md` (`| 1 | 2026-10-18 → 2026-10-18 | HANDOFFS-through-2026-10-18-3.md | v1.8.1 |`). After the fold the shard's proof exits 0, and `bin/check-handoff`, `bin/check-links` and `bin/check-learnings` exit 0. Taken before the session claim, as the retention rule says.

### 2026-10-19 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-18-3.md` (1 record(s), 47,384 B → 37,772 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-18 → 2026-10-18) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-18-3.md`](docs/archive/HANDOFFS-through-2026-10-18-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-18-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-18-3.md.verify.sh)
rather than trusting a digest printed here. Live file 47,384 B → 37,772 B (−20.3%).

The trim: `python3 starter-kit/methodology_trim.py --file HANDOFFS.md --cut 3 --force`, then `--write`: S340's receipt to `docs/archive/HANDOFFS-through-2026-10-18-3.md` (the `-3` suffix: the plain name and `-2` were taken), 4 receipts to 3 (S343, S342, S341). Taken at the operator's Phase 0 picker answer "Yes, trim first (Recommended)", before any claim. The dry run took 5.4 seconds and exited 0; the shard's own proof exits 0 (L1, L2, L3 hold) and `bin/check-handoff` and `bin/check-ledger` exit 0 after the write. The tool printed `FRONTMATTER_FIELD_ABSENT`, expected (the hand-kept receipt count is gone on purpose; see the `HANDOFFS.md` front matter). The pointer block it appended to `HANDOFFS.md` is folded into the archive index in the next commit, because inside the trim commit the shipped `.verify.sh` fails L2 (fork Learning #58).

### 2026-10-19 · [ad hoc] S343 -- push record: fork `main` to the fork `origin` at the operator's close-out tick (`624d223d` to `419eaf42`), head read back

At the operator's close-out picker answer ("Yes, push main to the fork"), `git push origin main` moved the fork's `main` from `624d223d` to `419eaf42` (11 commits: the trim, its fold, the claim, the seven sweep commits and the close-out). Read back: `git fetch origin`, `git ls-remote origin refs/heads/main` and local `HEAD` all read `419eaf42`, and `git rev-list --left-right --count origin/main...HEAD` reads `0 0`. Only the operator's own fork `rmsharp/methodology` was written; nothing was posted, pushed or edited in `KJ5HST/methodology`. This entry rides a ledger-only commit pushed under the standing grant for push records.

### 2026-10-19 · [ad hoc] S343 close-out -- the backlog sweep done: 19 rows closed in seven commits, BL-121 and BL-122 raised; the receipt complete; nothing sent upstream

The deliverable of the S343 claim above: BL-13, 14, 17, 20, 21, 22, 23, 26, 30, 31, 54, 57, 62, 63, 65, 66, 75, 80 and 85 closed (commits `a3c49f85`, `10e19265`, `ebe6f324`, `e735ef50`, `ff47932e`, `541e6d96`, `e0e6fd14`), one ledger entry each above; `docs/planning/BACKLOG.md` 63,791 B to 53,285 B and 75 to 58 index rows. Every closing fact was re-read first (12 pull requests and 2 issues with `gh`; the contents of `upstream/main`); the review's closing list held, with two wording corrections (BL-26's delivery route, BL-14's leftover). **Added by the session:** BL-121 (BOOTSTRAP.md's 'Setup with bin/sync' list, the operator's answer) and BL-122 (`bin/status` against a shallow source, measured); the BL-17 decision (fork-side check not built, by design, the operator's answer); riders in BL-46 and BL-60 and a note on BL-11's index row; dated update lines on three plans; the `.context-budget.json` sentence. **Found by the proofs, not by reading:** `BACKLOG-DETAIL.md.verify.sh` pins the routing block (C5) and the pre-split bodies (C2). **Not done:** the rest of BL-93 (the Open list, 13 anchors, relabels). Receipt complete (13 keys); `bin/check-handoff`, `bin/check-ledger`, `bin/check-links` and `bin/check-learnings` exit 0. `bash bin/tests.sh` in a clean `--no-local` clone of `e0e6fd14` (4 receipts in the tree): **503 passed, 0 failed, 0 skipped**, 513 s, equal to the `tests-sh-passed` floor of 503 (output kept only in the session scratchpad). Nothing was posted, pushed or edited in `KJ5HST/methodology`; `main` is ahead of the fork's `origin` until the operator ticks the push.

### 2026-10-19 · [BL-75] S343 -- BL-75 closed: upstream PR #86 merged; .context-budget.json's stale --status sentence rewritten

Closed by the three edits: the index row out of `docs/planning/BACKLOG.md` (and the id struck from its hand-kept 'Open:' list), the id kept in its 'Completed items' list, the pointer row into `docs/planning/BACKLOG-COMPLETED.md`. Upstream PR #86 merged 2026-10-01. The one step the plan still owed (P5) was `.context-budget.json:92`, whose note said `--status` 'does not exist and is silently ignored', false since the merge: it now tells a reader to run `--status` (writes nothing; an unknown argument exits 3) and corrects the `append_history` line reference from `:506` to `:617` (`grep -n 'def append_history' starter-kit/context_budget.py`). The edit is to prose inside one JSON string; the file still parses (`json.loads`) and no number in it changed. Checked S343: `python3 starter-kit/context_budget.py --bogus` exits 3 and `--status` exits 2 on this repository's known state and leaves `git status` clean. The plan's status line (`docs/planning/context-budget-status-plan.md`) gets a dated update in front of the old text. Both backlog proofs exit 0 before and after.

### 2026-10-19 · [BL-80] S343 -- BL-80 closed: upstream PR #86 merged; the advisory sentence follows the table

Closed by the three edits: the index row out of `docs/planning/BACKLOG.md` (and the id struck from its hand-kept 'Open:' list), the id kept in its 'Completed items' list, the pointer row into `docs/planning/BACKLOG-COMPLETED.md`. Upstream PR #86 merged 2026-10-01 (`gh pr view 86`: MERGED), the same pull request as BL-75; `starter-kit/context_budget.py` on `upstream/main` builds the advisory's second sentence from the headline's own worst status. Both backlog proofs exit 0 before and after.

### 2026-10-19 · [BL-57] S343 -- BL-57 closed: upstream PR #84 merged; all twelve phases done; the plan's status line and BL-11 updated

Closed by the three edits: the index row out of `docs/planning/BACKLOG.md` (and the id struck from its hand-kept 'Open:' list), the id kept in its 'Completed items' list, the pointer row into `docs/planning/BACKLOG-COMPLETED.md`. Upstream PR #84 merged 2026-10-01 (`gh pr view 84`: MERGED). The plan’s status line (`docs/planning/changelog-rules-contradictions-plan.md`) gets a dated update in front of the old text, which stays as it stood. The plan’s §8 follow-ons are pointed at the rows that carry them: D7 (the `HANDOFFS.md` archive rule) is in BL-47’s detail (‘The `HANDOFFS.md` half stays open (the plan’s D7)’); the four fork-only comments in distributed tools are the class BL-11 tracks, and BL-11’s index row gets a note with a grep that finds them now (the plan’s line numbers have drifted; BL-11’s detail body is byte-pinned by the detail proof, so it is not edited). Both backlog proofs exit 0 before and after.

### 2026-10-19 · [BL-62] S343 -- BL-62 closed: upstream PR #84 merged; the partition test sums only the read-set pair

Closed by the three edits: the index row out of `docs/planning/BACKLOG.md` (and the id struck from its hand-kept 'Open:' list), the id kept in its 'Completed items' list, the pointer row into `docs/planning/BACKLOG-COMPLETED.md`. `tools/test_context_budget.py` on `upstream/main` has `READ_TOGETHER_CLASSES = ("read-set",)` at line 1664 and uses it at 1679; the fix commit `5223afb6` is an ancestor of `upstream/main`. Both backlog proofs exit 0 before and after.

### 2026-10-19 · [BL-63] S343 -- BL-63 closed: upstream PR #84 merged; the paragraph and the cap sentence are live (index row out; never in the Open list)

Closed by the index row leaving `docs/planning/BACKLOG.md`, the id kept in its Completed items list and the pointer row joining `docs/planning/BACKLOG-COMPLETED.md`. BL-63 was never in the hand-kept 'Open:' list, so nothing was struck there. 'Committing a sync' is at `starter-kit/BOOTSTRAP.md` line 76 on `upstream/main` and the cap-row sentence is in `starter-kit/SAFEGUARDS.md` there (`grep -c` reads 1). Both backlog proofs exit 0 before and after.

### 2026-10-19 · [BL-54] S343 -- BL-54 closed: upstream PR #87 merged, carrying the fork-side fix

Closed by the three edits: the index row out of `docs/planning/BACKLOG.md` (and the id struck from its hand-kept 'Open:' list), the id kept in its 'Completed items' list, the pointer row into `docs/planning/BACKLOG-COMPLETED.md`. Upstream PR #87 carries the two fork-side commits (`2c4f801`, `865119f`) with BL-66's fix, as the plan's D3 (a) decided; `bin/sync` on `upstream/main` uses `--full-history` and `bin/status` counts a first-parent 'mainline'. Closed with BL-66, the sync-github plan's last step. Both backlog proofs exit 0 before and after.

### 2026-10-19 · [BL-66] S343 -- BL-66 closed: upstream PR #87 merged; plan P6 done; the verification clause run

Closed by the three edits: the index row out of `docs/planning/BACKLOG.md` (and the id struck from its hand-kept 'Open:' list), the id kept in its 'Completed items' list, the pointer row into `docs/planning/BACKLOG-COMPLETED.md`. Upstream PR #87 merged 2026-10-01 (`gh pr view 87`: MERGED); `upstream/main` is an ancestor of fork `main`. **The plan's verification clause, run:** with `METHODOLOGY_SOURCE_URL=https://github.com/rmsharp/methodology.git` (the default upstream address cannot pass it, since fork `main` differs from upstream's), `bin/status` over a clean clone of `mts-system` (`69cc272`) printed 33 lines from each of `--source=github` and `--source=local`, equal except the `source:` line. The residual the plan's decision D5 did not cover is BL-122. The plan's status line is corrected in `docs/planning/sync-github-route-plan.md` by a dated update in front of the old text. Both backlog proofs exit 0 before and after.

### 2026-10-19 · [BL-122] S343 -- BL-122 raised: bin/status says nothing about a shallow source (measured: 21 rows misread)

Raised from BL-66's close so the residual is not lost. Measured S343 with a `--depth 1` clone of this repository as the source and a clean clone of `mts-system` as the project: `bin/status` prints `locally modified` on 21 rows and never mentions history; against the full source the same 21 rows read `N versions behind`. `bin/sync --dry-run` against the same shallow source refuses and names the shallow checkout. One index row in `BACKLOG.md`, one body in `BACKLOG-DETAIL.md`; nothing built, and the fix is canonical-only, so it reaches adopters only through an upstream pull request.

### 2026-10-19 · [BL-65] S343 -- BL-65 closed: fixed upstream by the maintainer (PR #89, 229f08d9)

Closed by the three edits: the index row out of `docs/planning/BACKLOG.md` (and the id struck from its hand-kept 'Open:' list), the id kept in its 'Completed items' list, the pointer row into `docs/planning/BACKLOG-COMPLETED.md`. The maintainer fixed the test himself in the shape the body proposed (a): PR #89 merged 2026-10-01, commit `229f08d9`; `TestFitGateEndToEnd` skips when the data refuse the fit. The body's side note (the `Ran N tests` gates ignore a failing suite) is covered for the four suites it names, because `bin/tests.sh` runs them (lines 263-288) and `tests-sh-failed` reads its result; the instance it cannot cover is BL-109. Both backlog proofs exit 0 before and after.

### 2026-10-19 · [BL-85] S343 -- BL-85 closed: upstream PR #88 merged; the leftover is BL-121

Closed by the three edits: the index row out of `docs/planning/BACKLOG.md` (and the id struck from its hand-kept 'Open:' list), the id kept in its 'Completed items' list, the pointer row into `docs/planning/BACKLOG-COMPLETED.md`. Upstream PR #88 (the never-overwrite rules for an adopter's ledgers) merged 2026-10-01 (`gh pr view 88`: MERGED); `starter-kit/BOOTSTRAP.md` on `upstream/main` carries the rule at lines 376 and 382. The leftover noted in the body, the stale ‘Setup with bin/sync’ list, is BL-121. Both backlog proofs exit 0 before and after.

### 2026-10-19 · [BL-121] S343 -- BL-121 raised: BOOTSTRAP.md's ‘Setup with bin/sync’ list is stale against the manifest

Raised from BL-85's close, at the operator's S343 picker answer (‘keep it as a new small row’). The leftover was recorded at S224 and never fixed: `starter-kit/BOOTSTRAP.md:90` omits `methodology_trim.py`, `context_budget.py` and `quality_ratchet.py` from the installed operating files and `.context-budget.json` and `.quality-gates.json` from the seeds; `bin/_manifest.py` lines 61, 65, 66, 72, 73 distribute them. One index row in `BACKLOG.md`, one body in `BACKLOG-DETAIL.md`. Not started; the fix is distributed, so it is its own go-ahead.

### 2026-10-19 · [BL-21] S343 -- BL-21 closed as moot: the Phase 1B carve-out its sentences described was removed

Closed by the three edits: the index row out of `docs/planning/BACKLOG.md` (and the id struck from its hand-kept 'Open:' list), the id kept in its 'Completed items' list, the pointer row into `docs/planning/BACKLOG-COMPLETED.md`. Decision D10 (`16648604`, 2026-09-16) removed the claim exemption and its Test 27; `.githooks/pre-commit` carries no claim exemption (re-read S343), so the two seed sentences would describe a hook no one has. Both backlog proofs exit 0 before and after.

### 2026-10-19 · [BL-23] S343 -- BL-23 closed as moot: issue #65 closed, the Learnings-table move merged as PR #76

Closed by the three edits: the index row out of `docs/planning/BACKLOG.md` (and the id struck from its hand-kept 'Open:' list), the id kept in its 'Completed items' list, the pointer row into `docs/planning/BACKLOG-COMPLETED.md`. Upstream issue #65 closed 2026-08-12 and PR #76 (the Learnings-table extraction) merged 2026-09-02 (`gh issue view 65`, `gh pr view 76`); the tag `archive/bl-10-citations` still holds the parked checker (`git tag --list`). Both backlog proofs exit 0 before and after.

### 2026-10-19 · [BL-26] S343 -- BL-26 closed: PR #66 merged, issue #67 closed by the maintainer's PR #73

Closed by the three edits: the index row out of `docs/planning/BACKLOG.md` (and the id struck from its hand-kept 'Open:' list), the id kept in its 'Completed items' list, the pointer row into `docs/planning/BACKLOG-COMPLETED.md`. Upstream PR #66 merged 2026-08-11 and issue #67 closed 2026-08-12 (04:43:18Z), one second after the maintainer's PR #73 merged (`gh pr view 66`, `gh pr view 73`, `gh issue view 67`). The fork's own scoped `--sync` fix (`7d682fa`) is not upstream and the closed row says so: it ships only with the large combined pull request's dashboard lineage (composition plan D3 (a)). Both backlog proofs exit 0 before and after.

### 2026-10-19 · [BL-30] S343 -- BL-30 closed: the trimmer has fired in all three other adopters; their proofs re-run read-only

Closed by the three edits: the index row out of `docs/planning/BACKLOG.md` (and the id struck from its hand-kept 'Open:' list), the id kept in its 'Completed items' list, the pointer row into `docs/planning/BACKLOG-COMPLETED.md`. The body asked whether the trimmer fired outside `nprcgenekeepr`, and whether each run was verified by its own `.verify.sh`. It has, in `mts-system`, `vscode_quarto_ext` and `wsfct`. I cloned each project's `master` (`git clone --no-local`, into the session scratchpad, so no adopter working tree was touched) and ran every shard's proof: `mts-system` 4 of 4 exit 0, `vscode_quarto_ext` 3 of 3, `wsfct` 0 of 6 as written and 5 of 6 under `--reverify` (trimmer 1.8.1); the sixth `wsfct` proof is recorded as a rider in BL-60's detail body. Both backlog proofs exit 0 before and after.

### 2026-10-19 · [BL-14] S343 -- BL-14 closed: upstream PR #69 merged; one leftover sentence handed to BL-46

Closed by the three edits: the index row out of `docs/planning/BACKLOG.md` (and the id struck from its hand-kept 'Open:' list), the id kept in its 'Completed items' list, the pointer row into `docs/planning/BACKLOG-COMPLETED.md`. Upstream PR #69 merged 2026-08-12 and the spec's collector promise for `commit: pending` is gone (0 hits for 'until the next session' in `starter-kit/HANDOFFS.md` on `upstream/main`). One sentence at `starter-kit/HANDOFFS.md:163-165` ('was always going to be filled by a later session', identical on `upstream/main` line 164) is not covered; it is upstream's own text too, so it is not a fork-local fix. It is recorded as a rider at the end of BL-46's detail body (BL-46 changes the same file), so closing BL-14 loses nothing. BL-16 stays open. Both backlog proofs exit 0 before and after.

### 2026-10-19 · [BL-17] S343 -- BL-17 closed: upstream PR #69 merged; the fork-side check is not built, by design

Closed by the three edits: the index row out of `docs/planning/BACKLOG.md` (and the id struck from its hand-kept 'Open:' list), the id kept in its 'Completed items' list, the pointer row into `docs/planning/BACKLOG-COMPLETED.md`. The distributed half merged as upstream PR #69 on 2026-08-12 (`starter-kit/HANDOFFS.md:63` on `upstream/main` blesses the quoted-heading locator). The fork-side half, a check that every quoted ledger title still resolves, was deliberately never built; **the operator confirmed at the S343 Phase 0 picker that it is recorded as not built, by design** (the row's own reasoning: such a check goes red when an entry is retitled to correct a false claim). Both backlog proofs exit 0 before and after.

### 2026-10-19 · [BL-20] S343 -- BL-20's residual closed: the seed became a pointer (index row out only)

BL-20's defect was fixed at S79; only its option (3), documenting the bare `**Model:**` form in the receipts seed, stayed open. The text it targeted no longer exists: `starter-kit/CHANGELOG.md` is a pointer to `FRAMEWORK_APPARATUS.md` §The Action Ledger (merged upstream with PR #84) and has no `Model:` sentence (`grep -c 'Model:' starter-kit/CHANGELOG.md` reads 0). The index row is out of `BACKLOG.md` and the id struck from its 'Open:' list; the id was already in the Completed items list. **No new completed row:** the existing row (`BACKLOG-COMPLETED.md:90`) is byte-pinned by `BACKLOG-COMPLETED.md.verify.sh` and still says option (3) 'remains open', so this entry is the record that it closed. Both backlog proofs exit 0 before and after.

### 2026-10-19 · [BL-13] S343 -- BL-13 closed: upstream PR #68 merged

Closed by the three edits: the index row out of `docs/planning/BACKLOG.md` (and the id struck from its hand-kept 'Open:' list), the id kept in its 'Completed items' list, the pointer row into `docs/planning/BACKLOG-COMPLETED.md`. Upstream PR #68 (the corrected `/caveman` row) merged 2026-08-12; line 96 of `RECOMMENDED_SKILLS.md` on `upstream/main` now says the methodology constrains a handoff by content, not length. **The routing block in `BACKLOG.md` is NOT edited:** check C5 of `BACKLOG-DETAIL.md.verify.sh` pins its 1,684 B byte for byte (editing it turned the proof red, found at S343), so a note after the block says it is kept as it stood. Both backlog proofs exit 0 before and after.

### 2026-10-19 · [BL-22] S343 -- BL-22 closed: upstream PR #70 merged

Closed by the three edits: the index row out of `docs/planning/BACKLOG.md` (and the id struck from its hand-kept 'Open:' list), the id kept in its 'Completed items' list, the pointer row into `docs/planning/BACKLOG-COMPLETED.md`. Upstream PR #70 (the written reason and the pinning test for the dashboard's documentation-only thresholds) merged 2026-08-12; `test_doc_only_thresholds_are_pinned_not_left_to_drift` is on `upstream/main`. Both backlog proofs exit 0 before and after.

### 2026-10-19 · [BL-31] S343 -- BL-31 closed: upstream PR #71 merged

Closed by the three edits: the index row out of `docs/planning/BACKLOG.md` (and the id struck from its hand-kept 'Open:' list), the id kept in its 'Completed items' list, the pointer row into `docs/planning/BACKLOG-COMPLETED.md`. Upstream PR #71 (the dashboard's exclusion list for `context_budget.py`) merged 2026-08-12 (`gh pr view 71`: MERGED); `FRAMEWORK_INSTALLED_SOURCE` on `upstream/main` carries it. Both backlog proofs exit 0 before and after.

### 2026-10-19 · [ad hoc] S343 claim (in progress) -- the backlog sweep: close the 19 rows the review lists as finished or superseded; nothing sent upstream

CHANGELOG: pending. Taken at the operator's Phase 0 picker answers: "Tidy the to-do list (Recommended)" and "Yes, trim first (Recommended)" (the trim `20f06fd3` and its fold `af5abc39` done first). The deliverable: the backlog sweep: close the 19 rows of `docs/planning/BACKLOG.md` that `docs/planning/backlog-interaction-review-2026-10-18.md` section 2.1 lists as finished upstream or superseded (BL-13, 14, 17, 20, 21, 22, 23, 26, 30, 31, 54, 57, 62, 63, 65, 66, 75, 80, 85), each by the three edits the repository requires (the row out of the index, the id into the file's 'Completed items' list, the pointer row into `BACKLOG-COMPLETED.md`) plus a ledger entry, with the review's riders that keep a close from undoing itself (strike the closed ids from the hand-kept 'Open:' list and the routing text; the `.context-budget.json:92` sentence; the stale status lines of the three plans named in section 2.1). Every closing fact is re-checked first, since the review's verdicts came from subagents; a row that fails its re-check stays open and is named. NOT in this session: deleting the hand-kept 'Open:' list, the 13 missing anchor lines in `BACKLOG-DETAIL.md` and the index relabels (the rest of BL-93, which stays open). **Nothing is sent to `KJ5HST/methodology`.** The Phase 0 dashboard run (72/100, 1 high-risk flag, as before) appended its line to `dashboard_history.jsonl`, which rides this claim commit. Phase 0 found nothing to answer upstream: PR #94 (`1670c5d`) and PR #92 have no maintainer reply after ours, issues #93 and #95 no new comment, `upstream/main` still `f34769f`; `check-ledger`, `check-handoff`, `check-links` and `check-learnings` exit 0; `context_budget.py --status` exit 2 as before.

### 2026-10-19 · [ad hoc] S343 -- the HANDOFFS trim's pointer block folded into the archive index (the trim itself is the tool's entry below, commit `20f06fd3`, ticked at the S343 Phase 0 picker)

The trim: `python3 starter-kit/methodology_trim.py --file HANDOFFS.md --cut 3 --force`, then `--write`: S339's receipt to `docs/archive/HANDOFFS-through-2026-10-18-2.md` (the `-2` suffix: S342's trim took the plain name), 4 receipts to 3 (S342, S341, S340), 46,443 B to 37,325 B; the shard's own proof exit 0 before the commit, `bin/check-handoff` and `bin/check-ledger` exit 0. The dry run took 6.3 seconds. The tool printed `FRONTMATTER_FIELD_ABSENT` (expected), `CUT_STRADDLES_DAY`, `SHARD_NAME_DISAMBIGUATED` and the `SRF` refusal note that `--force` overrides. The fold, in its own commit as the index's rule says: the pointer block left `HANDOFFS.md` and one row joined `docs/HANDOFFS_ARCHIVE_INDEX.md` (`| 1 | 2026-10-18 → 2026-10-18 | HANDOFFS-through-2026-10-18-2.md | v1.8.1 |`). Taken before the session claim, as the retention rule says.

### 2026-10-19 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-18-2.md` (1 record(s), 46,443 B → 37,325 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-18 → 2026-10-18) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-18-2.md`](docs/archive/HANDOFFS-through-2026-10-18-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-18-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-18-2.md.verify.sh)
rather than trusting a digest printed here. Live file 46,443 B → 37,325 B (−19.6%).

### 2026-10-19 · [ad hoc] S342 -- push record: fork `main` to the fork `origin` at the operator's close-out tick (`dc9ce731` to `8ceb918e`), head read back

`git push origin main` took the 8 session commits (the trim and its fold, the claim, the package, the revised texts, the BL-118 reword, the record of the four sends, the close-out). Read back three ways: `origin/main` after a fetch, local `main` and `gh api repos/rmsharp/methodology/branches/main` all read `8ceb918e724d9736f526646d71e9fbdf3fa203c1`. Nothing on `KJ5HST/methodology` moved with it.

### 2026-10-19 · [ad hoc] S342 close-out -- the receipt complete; PR #94 answered and read back, the maintainer's reply next

The S342 claim's `CHANGELOG: pending` is closed by the entries around it. The receipt in `HANDOFFS.md` is complete (self-score 8, predecessor S341 scored 8; Phase 3C appended no row to `docs/FORK_LEARNINGS.md`, so the retire-or-refuse rule was not triggered; rows considered #109 and #24; two memory notes carry the lessons: a verdict tool needs three answers for a missing input, and splitting a change out of a ratcheted branch is a rebuild). The deliverable, `docs/planning/pr94-response-2026-10-19.md`: the maintainer's `issuecomment-6258571753` checked against the code (all nine reproduce), PR #94's branch rebuilt (head `1670c5d4`, 14 commits, trimmer 1.8.2, 227 tests, 12/12 in a clean clone), one extra fix the maintainer did not list, the separate `SESSION_NOTES.md` branch (`8de50d23`, 1.9.0), the BL-120 reword at his picker answer, and four outward steps read back (branch, separate branch, description, reply `issuecomment-6275751677`). Mistakes: a figure in an entry (the reply as 6.8 KB, it is 7,890 B), overclaiming first drafts caught by two cold reads, a bundled jargon picker he rejected, a missed revisit trigger that cost a replay, a 37-file evidence commit. Next: the maintainer's reply on PR #94 (four questions put to them in it); the second pull request is not opened; OFFER the `HANDOFFS.md` trim at the next Phase 0 (4 receipts at rest). The 18-gate run on `main` is not re-run (no code changed on `main`); the receipt cites S338's.

### 2026-10-19 · [ad hoc] S342 -- PR #94 response: SENT, four outward steps on the operator's go-ahead for the exact texts, each read back before the next

The operator answered the picker "Yes, reword it first" (BL-118, done above), then "Include it" (the extra fix `1670c5d4` stays) and "All four, in order". (1) `git push --force-with-lease=...:1082d3b1 origin pr94-r2:fix/trim-verify-false-red-issue93`: the branch and PR #94's head read back `1670c5d4` (GitHub's `headRefOid` lagged a few seconds), 14 commits, 5 files, +2,806 -30, OPEN, one comment. (2) `git push origin pr94-sn:refs/heads/feat/trim-session-notes-ledger-issue93`: read back `8de50d23`, one commit ahead of `1670c5d4`, six files, no pull request from it. (3) PR #94's title and description replaced with `gh api -X PATCH` (the posted body was first confirmed equal to the one the new text was built from, 28,117 B, and saved beside the new one): read back equal to `pr94-new-title.txt` and `pr94-new-body.md` (32,270 B) modulo the trailing newline. (4) The reply posted as `issuecomment-6275751677` (2026-10-19T19:42:32Z, 7,890 characters), read back equal to `reply-comment.md` modulo the trailing newline. The maintainer's comment is unchanged and the pull request is open, unmerged. The second pull request is not opened. Undo for (1): `git push --force-with-lease origin 1082d3b1:refs/heads/fix/trim-verify-false-red-issue93`. `docs/planning/pr94-response-2026-10-19.md` section 7 holds the record.

### 2026-10-19 · [ad hoc] S342 -- PR #94 response: the private code `BL-118` reworded out of a pushed test comment, at the operator's picker answer; commits 6 to 14 replayed; nothing sent

BL-120 (declined at S338) said to revisit only if #94 got another commit for another reason; the rebuild is that reason, and the operator answered "Yes, reword it first". The comment `# Issue #93, the abort code (the fork's BL-118).` is now `# Issue #93, the abort code.`, folded into commit 6, and commits 7 to 14 were cherry-picked on top, so nine hashes changed (old to new: `909eafb` to `38419e9`, `8aa6da7` to `159e600`, `5aaebdb` to `261a7b2`, `c7785c9` to `ec4e7df`, `4d32f7e` to `ad46648`, `b0c6fa3` to `d53f68f`, `156e495` to `252613c`, `5172db2` to `5741d2e`, `c3e926b` to `1670c5d`, `895c7bd` to `8de50d2`). `git diff` of the old head against the new one is that one comment line and nothing else; the notes-entry branch was re-picked the same way. Both clean-clone gate runs repeat 12/12 with the same results and manifest digests (`b49e29a9e5ea` / `06181a10ec42` for `pr94-r2`, `e56bb08a3c66` / `c9460f6eeb2e` for `pr94-sn`). The old branches survive locally as `pr94-r2-before-reword` (`c3e926b2`) and `pr94-sn-before-reword` (`895c7bd0`). The drafted texts carry the new hashes (checked: every hash in the reply, the description and the second description resolves to a commit on the branch the text names). **Correction to the entry above:** it gives the reply as 6.8 KB; it is 7,890 B. `BACKLOG-DETAIL.md` BL-120 gets a REVISITED paragraph. Nothing sent to `KJ5HST/methodology`.

### 2026-10-19 · [ad hoc] S342 -- PR #94 response: the reply and the new description revised after one cold read each; nothing sent

Two fresh readers (told the maintainer's vocabulary and forbidden to touch anything) read the reply and PR #94's new description. Real defects, checked before use and fixed: the reply opened by saying all nine points each had a commit (point 3 is the split, point 4's second half goes with the notes entry); it said "nine fixes" where commits 6 to 14 are eight fixes and the extra; the description said the same, called the exit-code changes against `1.8.1` where adopters hold 1.5.0, said projects with their own notes entry are "unaffected" (true only until a forced `bin/sync`), lacked an orientation block (old head `1082d3b`, new head `c3e926b`, which commits are unchanged, that commits 4 and 5 keep their version numbers with different content), and left digests and the notes pull request unidentified. Answered by running: a CRLF-converted proof was already refused at its `LIVE` line before and after; the fork has 181 shards of which 179 have a proof, the other 2 early hand-made ones read exit 3 under both trimmers (the old count of 174 with 2 at exit 3 was the same two). The reply is 6.8 KB and the description 32,271 B (was 28,118 B). `make_pr94_body.py` now carries the second pass. Not sent.

### 2026-10-19 · [ad hoc] S342 -- PR #94 response: the fixes on two local branches, the evidence, the package and the drafted texts; nothing sent

`docs/planning/pr94-response-2026-10-19.md` is the package; `docs/planning/pr94-response-evidence/` holds the scripts, their outputs and the texts. The maintainer's comment (`issuecomment-6258571753`) was checked point by point against `starter-kit/methodology_trim.py` at `1082d3b`: all nine reproduce on throwaway repositories. **Two local branches, not pushed:** `pr94-r2` (14 commits on `upstream/main`: commits 1 to 3 unchanged, 4 and 5 rebuilt without the `SESSION_NOTES.md` entry as `e88d1fd` and `9a4bf79`, then one commit per point, head `c3e926b`; trimmer 1.8.2, 227 tests; `quality_ratchet.py --run` in a clean clone 12/12, results `b49e29a9e5ea`) and `pr94-sn` (`pr94-r2` plus the entry as `895c7bd`, 1.9.0, 245 tests, 12/12, results `e56bb08a3c66`). Every fix has its tests written first and a mutation round (all killed except one equivalent mutant). One finding is not on the maintainer's list: a failed `git log` walk made the proof compare a ledger with itself and print `OK` (present since 1.5.0; `c3e926b`, separable). The fixes change none of the 54 verdicts of the adopter repository's proofs (`--reverify` 46 at exit 0 and 8 at exit 4 under `1082d3b` and under `pr94-sn`; 46, 1 at exit 4 and 7 at exit 1 under `pr94-r2`, the cost of the split). Drafted, not sent: the reply, PR #94's new title and description (29,477 B), the second pull request's title and description. No push, no comment, no edit of PR #94, no second pull request: each waits for the operator's go-ahead on the exact text, in the order in section 7 of the package.

### 2026-10-19 · [ad hoc] S342 claim (in progress) -- respond to the maintainer's comment on PR #94 (the trimmer fix): check each point against the code and draft the changes and the reply; nothing sent

CHANGELOG: pending. Taken at the operator's Phase 0 picker answers: "PR #94: check the maintainer's nine points (Recommended)" and "Yes, trim first (Recommended)" (the trim `50846c11` and its fold `ab6a86c0` done first). The deliverable: one response package to the maintainer's comment on PR #94 (`issuecomment-6258571753`, 2026-10-19T02:47:56Z, 2,533 characters, requesting changes to `starter-kit/methodology_trim.py` at `1082d3b`), in `docs/planning/pr94-response-2026-10-19.md`: each point checked against the code, the requested changes drafted on a local branch cut from the PR's head, and the exact text of the reply shown to the operator before anything is sent. Nothing sent to `KJ5HST/methodology`: no push to the PR branch, no comment, no edit of the PR description. The Phase 0 dashboard run (72/100, 1 high-risk flag, as before) appended its line to `dashboard_history.jsonl`, which rides this claim commit.

### 2026-10-19 · [ad hoc] S342 -- the HANDOFFS trim's pointer block folded into the archive index (the trim itself is the tool's entry below, commit `50846c11`, ticked at the S342 Phase 0 picker)

The trim: `python3 starter-kit/methodology_trim.py --file HANDOFFS.md --cut 3 --force`, then `--write`: S338's receipt to `docs/archive/HANDOFFS-through-2026-10-18.md`, 4 receipts to 3 (S341, S340, S339), 46,723 B to 35,351 B; the shard's own proof exit 0 before the commit, `bin/check-handoff`, `bin/check-ledger` and `bin/check-links` exit 0. The dry run took 6.4 seconds. The tool printed `FRONTMATTER_FIELD_ABSENT` (also printed at S341), `CUT_STRADDLES_DAY` and the `SRF` refusal note that `--force` overrides. The fold, in its own commit as the index's rule says: the pointer block left `HANDOFFS.md` and one row joined `docs/HANDOFFS_ARCHIVE_INDEX.md` (`| 1 | 2026-10-18 → 2026-10-18 | HANDOFFS-through-2026-10-18.md | v1.8.1 |`). Taken before the session claim, as the retention rule says.

### 2026-10-19 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-18.md` (1 record(s), 46,723 B → 35,351 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-18 → 2026-10-18) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-18.md`](docs/archive/HANDOFFS-through-2026-10-18.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-18.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-18.md.verify.sh)
rather than trusting a digest printed here. Live file 46,723 B → 35,351 B (−24.3%).

### 2026-10-19 · [ad hoc] S341 -- push record: fork `main` to the fork `origin` at the operator's close-out tick (`d257f721` to `1b0b5e45`), head read back

Non-commit action, on the operator's close-out tick ("Yes, push main"): `git push origin main:main`, a fast-forward of 13 commits (S340's five and S341's eight: the trim, its fold, the claim, three evidence commits, the record of the four PR #92 steps, the close-out). Read back: `git ls-remote origin refs/heads/main` `1b0b5e45` equal to the local head, and `git rev-list --left-right --count origin/main...main` read `0 0`. It reaches the operator's fork only; nothing went to `KJ5HST/methodology` except the four PR #92 steps recorded above. This record's own commit is pushed under the standing grant for a changelog-only push record.

### 2026-10-19 · [ad hoc] S341 close-out -- the maintainer's comment on PR #92 answered: the edit pushed, the description and Release body replaced, the reply posted; PR #94's comment not answered

The S341 claim's `CHANGELOG: pending` is closed by the entries around it. The receipt in `HANDOFFS.md` is complete (self-score 8, predecessor S340 scored 8; Phase 3C appended no row to `docs/FORK_LEARNINGS.md`, so the retire-or-refuse rule was not triggered; rows considered #95 and #50). The deliverable, `docs/planning/pr92-response-2026-10-19.md`: the maintainer's `issuecomment-6257621669` checked against git (every claim holds), the three requested edits and three small fixes pushed as `8a232bb7` to `origin` `docs/release-v4.2`, the PR description and the Release v4.2 body replaced (the tag stays at `f34769f`), and the reply posted as `issuecomment-6272223306`; each step on the operator's go-ahead for the exact text and read back before the next (entries above). Mistakes: an unquoted heredoc ran `bin/tests.sh` by accident (stopped, no tracked file changed); a wrong byte figure in a commit message (amended before any push). Next: wait on PR #92; PR #94's comment (`issuecomment-6258571753`, nine requested changes to the trimmer) is next in line. The 18-gate run on `main` is not re-run (no code changed since `5f09130`); the receipt cites S338's.

### 2026-10-19 · [ad hoc] S341 -- PR #92: reply comment posted (`issuecomment-6272223306`), on the operator's go-ahead for the exact text

Non-commit action, `gh pr comment 92 -R KJ5HST/methodology --body-file docs/planning/pr92-response-evidence/reply-comment.md`, 2026-10-19T16:39:50Z. It answers the maintainer's comment `issuecomment-6257621669`: the three changes made, the tag left at `f34769f`, the Release body edited, the gate result. Read back: equal to the draft. The comment on PR #94 (`issuecomment-6258571753`) is not answered.

### 2026-10-19 · [ad hoc] S341 -- Release v4.2 (published by the operator on 2026-10-03): body replaced, tag untouched

Non-commit action, `gh release edit v4.2 -R KJ5HST/methodology --notes-file docs/planning/pr92-response-evidence/release-v4.2-new.md`, on the operator's go-ahead for the exact text: the manifest bullet, the unsafe-rows bullet, the path-check line and the Updating line, as the maintainer asked. Read back: body equal to the draft; the tag still points at `f34769f` (`git ls-remote upstream refs/tags/v4.2*`); published time 2026-10-03T02:55:21Z and the draft and prerelease flags unchanged. The previous body is saved as `release-v4.2-current.md`.

### 2026-10-19 · [ad hoc] S341 -- PR #92: description replaced (the tag now stays at `f34769f`; two ledger entries; the review-changes paragraph)

Non-commit action, `gh api -X PATCH repos/KJ5HST/methodology/pulls/92 -F body=@docs/planning/pr92-response-evidence/pr92-body-new.md`, on the operator's go-ahead for the exact text. Read back: equal to the draft once the trailing newline the channel adds is ignored (1,396 B sent, 1,397 B read). The previous body is saved as `pr92-body-current.md`.

### 2026-10-19 · [ad hoc] S341 -- PR #92: pushed `8a232bb7` to the PR branch (`origin` `docs/release-v4.2`), on the operator's go-ahead for the exact text

Non-commit action. A fast-forward of one commit, `fa2bb5d4..8a232bb7` (`CHANGELOG.md`, `CLAUDE.md`, `README.md`, +14 -5): the maintainer's three requested edits and three small wording fixes. Read back: `git ls-remote origin refs/heads/docs/release-v4.2` and the PR's `headRefOid` both read `8a232bb76b1d`. The commit's own gate run (clean `--no-local` clone): 12/12 pass, results `10df8059439f`, manifest `5986cf638fb1`.

### 2026-10-19 · [ad hoc] S341 -- PR #92 response, evidence 3 of 3: the response document and the Release body, before and after; nothing sent

`docs/planning/pr92-response-2026-10-19.md` holds the checks, the change, the order of the four outward steps (push, description, Release body, comment; each read back before the next) and what is open (PR #94's comment). `release-v4.2-current.md` is the published Release body and `release-v4.2-new.md` replaces the three sentences, the path-check line and the Updating line; the tag is untouched. Nothing sent.

### 2026-10-19 · [ad hoc] S341 -- PR #92 response, evidence 2 of 3: the reply comment and the PR description, before and after; nothing sent

`reply-comment.md` is the text to post; `pr92-body-current.md` is the PR description as published (read-only fetch) and `pr92-body-new.md` replaces its tag paragraph (the tag stays at `f34769f`), its ledger-entry count and its review-changes paragraph. Both outward texts were scanned for fork-only terms (BL-, session numbers, the fork): none. Nothing sent.

### 2026-10-19 · [ad hoc] S341 -- PR #92 response, evidence 1 of 3: the patch of the local edit commit, the claim-check script and its output, the gate output; nothing sent

The maintainer's comment on PR #92 asked for three edits and a tag answer. `8a232bb7` (local branch `docs/release-v4.2`, cut from `origin/docs/release-v4.2` `fa2bb5d`, NOT pushed) makes them; its patch is saved here. `verify-claims.sh` re-derives each factual claim of the comment from git alone (read-only): all hold. The gate on `8a232bb7` in a clean `--no-local` clone: 12/12 pass, results `10df8059439f`, manifest `5986cf638fb1` (the pair the maintainer reports), `bin/tests.sh` 261 passed / 0 failed. Nothing sent to `KJ5HST/methodology`.

### 2026-10-19 · [ad hoc] S341 claim (in progress) -- answer the maintainer's comment on PR #92 (the v4.2 version notes): fix the text on a local copy of the PR branch and draft the reply; nothing sent

CHANGELOG: pending. Taken at the operator's Phase 0 picker answers: "Answer PR 92 (Recommended)" and "Yes, trim first (Recommended)" (the trim `74054ce2` and its fold `557be7ee` done first). The deliverable: one response package to the maintainer's comment on PR #92 (`issuecomment-6257621669`, 2026-10-19T01:19:30Z), in `docs/planning/pr92-response-2026-10-19.md`: each of the maintainer's points checked against the code (done at Phase 0; every one holds), the three requested edits and the three small ones made on a local branch cut from `origin/docs/release-v4.2` (`fa2bb5d`) and checked there, and the exact text of the reply comment, the edited PR description and the edited Release body, shown to the operator before anything is sent. The comment on PR #94 (`issuecomment-6258571753`) was read in full at Phase 0 and is not this session's task. Nothing sent to `KJ5HST/methodology`: no push to the PR branch, no comment, no edit of the PR description or the published Release, no tag change. The Phase 0 dashboard run (72/100, 1 high-risk flag, as before) appended its line to `dashboard_history.jsonl`, which rides this claim commit.

### 2026-10-19 · [ad hoc] S341 -- the HANDOFFS trim's pointer block folded into the archive index (the trim itself is the tool's entry below, commit `74054ce2`, ticked at the S341 Phase 0 picker)

The trim: `python3 starter-kit/methodology_trim.py --file HANDOFFS.md --cut 3 --force`, then `--write`: S337's receipt to `docs/archive/HANDOFFS-through-2026-10-17-2.md`, 4 receipts to 3 (S340, S339, S338), 47,564 B to 36,785 B; the shard's own proof exit 0 before the commit, `bin/check-handoff` and `bin/check-ledger` exit 0. The dry run took 6.5 seconds. The tool printed `SHARD_NAME_DISAMBIGUATED` (S336's shard already had the plain name) and `FRONTMATTER_FIELD_ABSENT`, both expected. The fold, in its own commit as the index's rule says: the pointer block left `HANDOFFS.md` and one row joined `docs/HANDOFFS_ARCHIVE_INDEX.md` (`| 1 | 2026-10-17 → 2026-10-17 | HANDOFFS-through-2026-10-17-2.md | v1.8.1 |`). Taken before the session claim, as the retention rule says.

### 2026-10-19 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-17-2.md` (1 record(s), 47,564 B → 36,785 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-17 → 2026-10-17) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-17-2.md`](docs/archive/HANDOFFS-through-2026-10-17-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-17-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-17-2.md.verify.sh)
rather than trusting a digest printed here. Live file 47,564 B → 36,785 B (−22.7%).

### 2026-10-19 · [ad hoc] S340 close-out -- the receipt complete; the NEXT session's task, set by him: examine and respond to the comments on PR #92; nothing sent

The S340 claim's `CHANGELOG: pending` is closed by the entries around it. The receipt in `HANDOFFS.md` is complete (self-score 7, predecessor S339 scored 8; Phase 3C appended no row to `docs/FORK_LEARNINGS.md`, so the retire-or-refuse rule was not triggered; rows considered #21 and #106). **His instruction, recorded here and in the receipt's `next_steps` (1):** "examine and respond to comments on PR #92 in the next session". The maintainer commented once on PR #92 (`issuecomment-6257621669`, 2026-10-19T01:19:30Z, 4,462 characters) and once on PR #94 (`issuecomment-6258571753`, 02:47:56Z, 2,533 characters); this session did not read either text. The next session reads both at Phase 0 before its task picker, checks each point against the code, drafts a reply, shows the exact text, and posts only on his go-ahead on that text. The same instruction is in the memory note for the upstream pull-request route. The gate run is not re-run (no code changed since `5f09130`); the receipt cites S338's.

