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

---

## 2026-09

## 2026-10

### 2026-10-19 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-17-2.md` (1 record(s), 47,564 B → 36,785 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-17 → 2026-10-17) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-17-2.md`](docs/archive/HANDOFFS-through-2026-10-17-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-17-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-17-2.md.verify.sh)
rather than trusting a digest printed here. Live file 47,564 B → 36,785 B (−22.7%).

### 2026-10-19 · [ad hoc] S340 close-out -- the receipt complete; the NEXT session's task, set by him: examine and respond to the comments on PR #92; nothing sent

The S340 claim's `CHANGELOG: pending` is closed by the entries around it. The receipt in `HANDOFFS.md` is complete (self-score 7, predecessor S339 scored 8; Phase 3C appended no row to `docs/FORK_LEARNINGS.md`, so the retire-or-refuse rule was not triggered; rows considered #21 and #106). **His instruction, recorded here and in the receipt's `next_steps` (1):** "examine and respond to comments on PR #92 in the next session". The maintainer commented once on PR #92 (`issuecomment-6257621669`, 2026-10-19T01:19:30Z, 4,462 characters) and once on PR #94 (`issuecomment-6258571753`, 02:47:56Z, 2,533 characters); this session did not read either text. The next session reads both at Phase 0 before its task picker, checks each point against the code, drafts a reply, shows the exact text, and posts only on his go-ahead on that text. The same instruction is in the memory note for the upstream pull-request route. The gate run is not re-run (no code changed since `5f09130`); the receipt cites S338's.

### 2026-10-19 · [ad hoc] S340 -- the backlog interaction review built: 75 open rows carded, 163 interactions found and tested, 96 survived, one recommended order; nothing sent

The deliverable of the S340 claim below: `docs/planning/backlog-interaction-review-2026-10-18.md` (82,522 B) and its evidence file `docs/planning/backlog-interaction-review-evidence/findings.md` (60,160 B, all 163 findings with verdicts). It proposes and edits no backlog row. **Result:** 19 of the 75 listed rows can close (15 whose fix reached upstream, every cited pull request verified merged: #66, #68 to #71, #73, #76, #84 to #88; 4 superseded or answered: BL-20, BL-21, BL-23, BL-30); the hand-kept "Open:" list names 52 of 75 rows; 13 detail bodies lack their anchor and 10 `[detail]` links dangle; `BACKLOG.md` reads about 26,793 tokens against 25,000. The interactions that change a fix: one version bump per file group (ratchet 1.6.0, dashboard 2.23.0, one trimmer release after PR #94 settles, three seed batches not one), the candidate ships BL-102's defect line unchanged, nine rows compete for about 23 tokens of runner room, `CLAUDE.md` is 137 B over, BL-109/111/112 are copies of hunks the candidate already has. Order in section 5; nine rows held on him; nine questions with recommendations in section 6. **Method:** 15 card agents, 6 lens agents, 489 skeptic agents (three per finding, a majority to refute; 96 survived, 67 refuted), then 5 orderers, 3 judges and 1 synthesis: 519 agents, about 37.6 million subagent tokens. The first run hit the Fable usage limit with 318 of the 489 skeptics failed; it was resumed from its journal after the session model changed to Sonnet 5.5 (192 results replayed, 318 re-run; which verdict came from which model was not recorded). **Checked directly by this session:** 13 pull request and 5 issue states, `context_budget.py --status` (wrote nothing), the Open-list count, the anchor and link counts, `grep -c SESSION_NOTES` on the fork's trimmer, `quality_ratchet.py:666` on fork `main` and the candidate, the candidate runner's 53,100 B and ceiling, the `-failed` migration gate on the candidate only, both plans' sizes, both backlog proofs exit 0. **The maintainer's two comments (PR #92, 4,462 characters, 2026-10-19T01:19:30Z; PR #94, 2,533 characters, 02:47:56Z) were NOT read by this session** (his instruction: examine and respond in the next session); several panel agents read them through read-only `gh` because the brief did not forbid it, their summaries were not checked and were rewritten out of the document. `bin/check-ledger` and `bin/check-links` exit 0. Nothing was posted, pushed or edited upstream.

### 2026-10-18 · [ad hoc] S340 claim (in progress) -- review the backlog: the interactions between its 75 open items, where a proposed fix should change because of a neighbour, and a recommended order; nothing sent

CHANGELOG: pending. Taken at his instruction after the Phase 0 report and a listing of further open rows: "review the backlog - examining interactions between BL items seeking to improve proposed changes and preferred BL item order." The deliverable: one review document, `docs/planning/backlog-interaction-review-2026-10-18.md`, that reads every open row of `docs/planning/BACKLOG.md` (75 rows at `3945af8f`) with its body in `BACKLOG-DETAIL.md`, names the dependencies, collisions, subsumptions and sequences between them, says where a proposed change should change because of a neighbour, flags rows whose recorded status has drifted, and ends in a recommended order with reasons. It proposes; it edits no backlog file. The trim (`c099cd28`) and its fold (`3945af8f`) were done before this claim. No upstream action: PR #94 (`1082d3b`), PR #92 (`fa2bb5d`), issues #93 and #95 and `upstream/main` (`f34769f`) were read-only at Phase 0, 0 comments, 0 reviews, no reply. The Phase 0 dashboard run (72/100, 1 high-risk flag, the same as S339) appended its line to `dashboard_history.jsonl`, which rides this claim commit.

### 2026-10-18 · [ad hoc] S340 -- the HANDOFFS trim's pointer block folded into the archive index (the trim itself is the tool's entry below, commit `c099cd28`, ticked at the S340 Phase 0 picker)

The trim: `python3 starter-kit/methodology_trim.py --file HANDOFFS.md --cut 3 --force`, then `--write`: S336's receipt to `docs/archive/HANDOFFS-through-2026-10-17.md`, 4 receipts to 3 (S339, S338, S337), 47,659 B to 37,944 B; the shard's own proof exit 0 before the commit, `bin/check-handoff` and `bin/check-ledger` exit 0. The dry run took 6.6 seconds. The tool printed `CUT_STRADDLES_DAY` (S337's receipt, also dated 2026-10-17, stays) and `FRONTMATTER_FIELD_ABSENT`, both expected. The fold, in its own commit as the index's rule says: the pointer block left `HANDOFFS.md` and one row joined `docs/HANDOFFS_ARCHIVE_INDEX.md` (`| 1 | 2026-10-17 → 2026-10-17 | HANDOFFS-through-2026-10-17.md | v1.8.1 |`). Taken before the session claim, as the retention rule says.

### 2026-10-18 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-17.md` (1 record(s), 47,659 B → 37,944 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-17 → 2026-10-17) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-17.md`](docs/archive/HANDOFFS-through-2026-10-17.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-17.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-17.md.verify.sh)
rather than trusting a digest printed here. Live file 47,659 B → 37,944 B (−20.4%).

### 2026-10-18 · [ad hoc] S339 -- push record: fork main to the fork origin at his close-out tick (`e946a101` to `87ec7d01`), head read back

`git push origin main` fast-forwarded the fork's `origin` (`rmsharp/methodology`) by six commits: the trim `37cc7717`, its fold `f2294c58`, the claim `2be18304`, the record `7d00d29e`, the close-out `2bf8c2d7` and his answers `87ec7d01`. Read back: `git ls-remote origin refs/heads/main` and `git rev-parse HEAD` both `87ec7d01`, `git rev-list --left-right --count origin/main...HEAD` `0 0`. `upstream/main` was read after the push and is still `f34769f`. Nothing was sent to `KJ5HST/methodology`.

### 2026-10-18 · [BL-101] S339 -- his close-out picker answers: D4 stands on the corrected figures, the push of fork `main` is ticked, the full gate run is declined; nothing sent upstream

Shown the corrected wait-time figures (#83 is the maintainer's own pull request; his longest wait is #84's 13.6 days; #92 at 15 days is already past it), he answered that **D4 stands: keep waiting, ask again on or after 2026-10-25** (the waiver entry above recorded the answer as first given; this entry is the confirmation, and `d1-d4-record.md` section 3 and the receipt now say so). He ticked the push of fork `main` to the fork's `origin` (five commits, `e946a101` to `2bf8c2d7`, then this entry) and declined the 18-gate run: the receipt's citation stays S338's run of `5f09130`. Nothing was posted, pushed or edited at `KJ5HST/methodology`.

### 2026-10-18 · [BL-101] S339 close-out -- D1 and D4 answered and recorded, the receipt complete; nothing sent

Deliverable: his two answers to the one-pull-request plan's remaining decisions, laid out with the facts first and recorded (commit `7d00d29e`; the waiver entry above is section 7.6's "ledger says so"). The `HANDOFFS.md` receipt is `status: complete` (`bin/check-handoff` exit 0). **Phase 3E:** no runtime behaviour changed; the fast checkers exit 0 (`check-ledger`, `check-handoff`, `check-links`, `check-learnings`, the completed-items proof, the shard's proof, `pr4-body-check.py`); **the 18-gate `quality_ratchet.py --run` was NOT run** (load 18, three other sessions open), and the receipt cites S338's run of `5f09130` and says so. **Phase 3C:** no row appended to `docs/FORK_LEARNINGS.md`; rows considered #42 and #25. A wait-time figure I stated at the picker was wrong (#83 is the maintainer's own pull request) and is corrected in the record and in the waiver entry; whether his D4 answer stands is asked at the close-out picker. Nothing was posted, pushed or edited upstream.

### 2026-10-18 · [BL-101] S339 -- D1 and D4 answered: the section 7.6 wait is WAIVED for the one upstream pull request, and the wait for the maintainer gets an end date, 2026-10-25; nothing sent

His picker answers (each the recommended option, shown the facts first): **D1, waive, the text unchanged.** This entry is the "ledger says so" that `methodology-subdirectory-plan.md` §7.6 requires of a waiver. It waives the wait for the 13 rows `register-open-rows.py` reads as open (13 of 33): F2, F4, F6, F7, F8, F13, F14, F17, F19, F25, F26, F27, F28. They stay open as rows with their dispositions; the waiver lets the pull request go while they are open and closes none. The approved text (draft 11) states 10 of them in plain words, F27 only loosely, and not F13 or F14. **D4, keep waiting, ask again on or after 2026-10-25** (then #92 is 22 days old and #94 20); a reply, a review or a merge ranks first at any Phase 0, and a merge of #94 or #92 means the claims run and decision 3 are re-measured before PR5. **A correction of mine, recorded:** at the picker I called #83 one of his pull requests and its 15-day wait the longest; #83 is the maintainer's own, his longest wait is #84's 13.6 days, and #92 (15 days) is already past it. The answer is recorded as he gave it; whether it stands is asked at the close-out picker. Written: `docs/planning/pr-composition-evidence/d1-d4-record.md` (new), `docs/planning/upstream-pr-composition-plan.md` (the status sentence and §7's header, 29,931 B to 29,996 B of its 30,000 B), a dated line in `docs/planning/methodology-subdirectory-evidence/findings-register.md`, the status line of `docs/planning/upstream-pr-body.md` (draft 11's text below the rule is unchanged; `pr4-body-check.py` exit 0). Nothing was posted, pushed or edited upstream.

### 2026-10-18 · [BL-101] S339 claim (in progress) -- settle D1 and D4, the two open decisions before the one upstream pull request; nothing sent

CHANGELOG: pending. Taken at his Phase 0 picker answers: "Settle D1 and D4 (Recommended)" and, for the side action, "Yes, trim now (Recommended)" (done first: the trim `37cc7717` and its fold `f2294c58`, both before this claim). The deliverable: his answers to the pull-request plan's two remaining decisions (`docs/planning/upstream-pr-composition-plan.md` section 7), laid out in plain language with the facts each rests on read from the sources (the open findings and what each blocks for D1; the state of PR #92 and PR #94 for D4), then recorded. No upstream action: PR #94, PR #92, issues #93 and #95 and `upstream/main` (`f34769f`) were read-only at Phase 0 and nothing was posted, pushed or edited. The Phase 0 dashboard run (72/100, 1 high-risk flag, the same as S338) appended its line to `dashboard_history.jsonl`, which rides this claim commit.

### 2026-10-18 · [ad hoc] S339 -- the HANDOFFS trim's pointer block folded into the archive index (the trim itself is the tool's entry below, commit `37cc7717`, ticked at the S339 Phase 0 picker)

The trim: `python3 starter-kit/methodology_trim.py --file HANDOFFS.md --cut 3 --force`, then `--write`: S335's receipt to `docs/archive/HANDOFFS-through-2026-10-16-4.md`, 4 receipts to 3 (S338, S337, S336), 48,829 B to 38,541 B; the shard's own proof exit 0 before the commit, `bin/check-handoff` and `bin/check-ledger` exit 0. The dry run took 5 seconds (the earlier ones took over 2 minutes). The tool printed `SHARD_NAME_DISAMBIGUATED` (the `-4` suffix) and `FRONTMATTER_FIELD_ABSENT`, both expected. The fold, in its own commit as the index's rule says: the pointer block left `HANDOFFS.md` and one row joined `docs/HANDOFFS_ARCHIVE_INDEX.md` (`| 1 | 2026-10-16 → 2026-10-16 | HANDOFFS-through-2026-10-16-4.md | v1.8.1 |`). Taken before the session claim, as the retention rule says.

### 2026-10-18 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-16-4.md` (1 record(s), 48,829 B → 38,541 B)

**Written by:** `methodology_trim.py` v1.8.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-16 → 2026-10-16) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-16-4.md`](docs/archive/HANDOFFS-through-2026-10-16-4.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-16-4.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-16-4.md.verify.sh)
rather than trusting a digest printed here. Live file 48,829 B → 38,541 B (−21.1%).

### 2026-10-18 · [BL-119] S338 -- push record: fork `main` pushed to the fork `origin` at his close-out tick (`7a0b473` to `871ce59`, 13 commits), head read back

Pre-flight: `origin` is `https://github.com/rmsharp/methodology.git` (the fork), its `main` still `7a0b473` and an ancestor of `HEAD` (a fast-forward). `git push origin main`, exit 0; `git ls-remote origin refs/heads/main` read back `871ce594ac612c3e0f52aee4e67bf24f4855cb52`, equal to local `HEAD`. Not touched: `KJ5HST/methodology` (`upstream/main` still `f34769f`; PR #94 still at `1082d3b`, 0 comments, 0 reviews), and `pr2/candidate` and `refs/pr2/candidate-before-bl119` stay local refs (no ref of that name on `origin`). This entry is the CHANGELOG-only push record his standing grant lets go to `origin` unasked.

### 2026-10-18 · [BL-120] S338 -- DECLINED by the operator at the close-out picker ("Leave it"): the fork code in PR #94's pushed test comment stays

Three edits as closing an item takes: the row out of `docs/planning/BACKLOG.md`, the id into §Completed items' list, a `DECLINED` row in `BACKLOG-COMPLETED.md` (the completed-items proof exit 0, run and read), and the detail marked declined. The reasons were given with the options: one comment in a test, no behaviour; any change is a public push to #94 that notifies the maintainer; the combined pull request may supersede #94. Revisit only if #94 gets another commit for another reason. The S338 receipt in `HANDOFFS.md` now records his three answers (draft 11 approved, BL-120 declined, the push ticked). The push of fork `main` to `origin` follows, with its own push-record entry.

### 2026-10-18 · [BL-119] S338 -- his answers at the close-out picker: draft 11 APPROVED as the held text of the one upstream pull request; nothing sent

Shown the exact new passages first (decision 3, the `3cba1e5` bullet, the commit-list sentence, the figure changes), he chose "Approve draft 11". The status line of `docs/planning/upstream-pr-body.md` now says APPROVED (S338 picker, 2026-10-18), replacing draft 10, which stays recoverable as `git show 8d7316e:docs/planning/upstream-pr-body.md`; the body is unchanged by this (21,486 B; `pr4-body-check.py` against `3cba1e5` exit 0 again). `bl119-record.md` §8 records the approval and that `bl119-draft11-build.py` still produces the "awaiting approval" wording (the approval is one hand edit). PR5 (the push and the opening) still waits on his two plan decisions, D1 and D4. His other two answers are in the next entry.

### 2026-10-18 · [BL-119] S338 close-out -- BL-119 closed, BL-120 raised, the receipt complete; nothing sent

BL-119 closed in three edits: its row out of `docs/planning/BACKLOG.md`, its id into §Completed items' list, its completed row into `BACKLOG-COMPLETED.md` (the completed-items proof exit 0, run and read), and its detail marked DONE. **BL-120 raised** (a row and a detail paragraph): PR #94's pushed fifth commit carries the fork-only code `BL-118` in one test comment; the options are his and any change to #94 is an outward action. The receipt in `HANDOFFS.md` is `complete`: self-score 8, predecessor (S337) 8, the six requirements and the gate citation (`18/18 pass · 0 fail · 0 unmeasured · results 51eb96ff6a98 · manifest 7e1f0d1576e4`, from the clean-clone run of `5f09130`). Phase 3C: no row appended to `docs/FORK_LEARNINGS.md`, so the retire-or-refuse rule (D3) was not triggered; the rows considered are named in the receipt. Open for him, asked at the close-out picker: draft 11 (approve, or keep draft 10), BL-120, and the push of fork `main` to `origin` (11 commits ahead including this one). Not pushed; `pr2/candidate` stays a local ref.

### 2026-10-18 · [BL-119] S338 -- the PR #94 record's Version note brought current, the evidence index's S338 section, and the Phase 0 dashboard row

`docs/planning/pr94-rewrite/README.md`'s Version paragraph said the fork's own trimmer and the candidate "are not fixed by this commit" and that the one-PR text says both trimmers are 1.8.0; it now says what S338 did (both at 1.8.1, `5f09130` and `3cba1e5`, the text draft 11). `evidence/README.md` gains §Added at S338: every `bl119-*` file with what it is, and a reproduce block, run once exactly as written before this commit (build exit 0, 222 tests, 8 killed and 1 survived as meant). `dashboard_history.jsonl`: the row Phase 0 step 5 appended (72/100, 1 high-risk project, 2,558 commits).

### 2026-10-18 · [BL-119] S338 -- draft 11 of the one upstream pull request's text (`docs/planning/upstream-pr-body.md`), re-measured against `1082d3b` and `3cba1e5`; NOT YET APPROVED, nothing sent

Draft 10, which he approved at the S336 picker (the file as `8d7316e` holds it), described a tip that no longer exists (`cfcc713`, 33 commits) and a pull request that has moved (`2308553`, four commits). Draft 11 is 17 exact-once edits by `bl119-draft11-build.py` (it refuses unless the file is draft 10 as `8d7316e` holds it, and refuses a second run): the status paragraph and heading (awaiting approval, with the way back), the tip and the commit count (four places), decision 3 (head `1082d3b`, "its fifth commit", 536 and 1,640 lines of which 77 and 295 are absent here, "both trimmers 1.8.1, each a different 1.8.0 plus the same abort fix"), the sizes (19,983 added, 1,105 removed, 2,991 and 533 reaching a project, 16,985 staying, the earlier work 42% and no longer 43%), the sentence about the last commits (three, with `3cba1e5` in a new bullet) and the sentence about which hashes are not this branch's. The body is 21,486 B against draft 10's 20,863 B (+623 B: the bullet 440, decision 3 87, the commit-list sentence 64, the hashes sentence 32). `pr4-body-check.py` against `3cba1e5`: exit 0, no banned token, 14 hashes resolve, 35 paths cited, the recomputed shortstat and count equal the text's. The record, `pr-composition-evidence/bl119-record.md`, lists every edit and what was left alone. **Draft 10 is not overwritten:** `git show 8d7316e:docs/planning/upstream-pr-body.md`. The 12-project paragraph was not re-run (its 49 lines hold against the fork's trimmer before this change; the record says how it was checked).

### 2026-10-18 · [BL-119] S338 -- the gate run on fork `main` (`5f09130`), the claims run on the candidate (`3cba1e5`) and decision 3's figures, saved

Three outputs and one script. **Fork `main`:** `layer-verify.sh` in a clean `--no-local` clone of `5f09130` (0 dirty paths), launched as nohup and read from a done-file: `bin/tests.sh` 503 passed through the gate `tests-sh-passed`, the ratchet **18/18 pass, 0 fail, 0 unmeasured, results `51eb96ff6a98`, manifest `7e1f0d1576e4`**, `trimmer-unit-tests` 222 against 222, the layout scanner 0 sites, 23 min 1 s at a load of 4 to 8 (`pr94-rewrite/evidence/bl119-main-gate-output.txt`; the two archive proofs that read exit 1 are old frozen scripts, red before this change). **Candidate:** `pr4-claims.sh` with `HEAD94=1082d3b HEAD92=fa2bb5d`, each tip in a clean clone, serially, 28 min 26 s: `bin/tests.sh` **302 passed, 0 failed, 0 skipped** (upstream 261), ratchet **18/18, results `668beb5fe5a2`, manifest `78150d65930f`** (upstream 12/12, `10df8059439f`), 47 files +19,983 / -1,105 in 34 commits, links 80 in 23 documents in each layout, the scanner 15 files and 0 sites, the layout suite 76 OK, the resolver block equal in 11 files, 0 refusals over 34 commits, #94 at `1082d3b` 4 files and 22 conflict regions, #92 clean (`pr-composition-evidence/bl119-claims-output.txt`). **`bl119-decision3.sh`** and its output: decision 3's figures on the old and the new tips, whose first block reproduces draft 10's published numbers (22 and 13 regions, 506/77 and 1,558/294) before the new ones are read: against `1082d3b` the conflicts are unchanged and #94 adds 536 lines to the trimmer and 1,640 to its tests, of which 77 and 295 are not here as identical lines (294 plus the candidate's one reworded comment line).

### 2026-10-18 · [BL-119] S338 -- the pull request candidate `pr2/candidate` takes the same fix: a 34th commit `3cba1e5` (`TRIM_VERSION` 1.8.0 to 1.8.1), the old tip pinned, nothing sent

Built in a clean `--no-local` clone of `pr2/candidate` at `cfcc713` with `bl119-build.py` (hooks not armed in that clone, as for the 33rd commit; no ledger entry, as the 33rd had none), then brought home as a fast-forward of the local ref; the old tip is pinned as `refs/pr2/candidate-before-bl119`. The diff is the same four files as on `main` (+165 / -7), line for line but for offsets and the candidate's already-scrubbed 1.8.0 history line. One edit differs by rule: the test comment that read "the fork's BL-118" (the same line is in PR #94's pushed `1082d3b`) reads "Issue #93, the abort code" here, because the candidate carries no fork code (the scrub, `pr-composition-evidence/scrub-record.md`); the added lines were scanned for `BL-`, session numbers, "the fork" and `pr2/`: none. Measured before the commit: 222 tests OK; 8 of 9 mutants killed (same output as `main`); on a depth-1 clone of the candidate the frozen proof exits 1, `--reverify` 1 under 1.8.0 and 3 under 1.8.1; the candidate's one archived piece reads 0 under both. Outputs: `bl119-candidate-*` beside the `main` ones. The suite, gate and claims runs on `3cba1e5` follow.

### 2026-10-18 · [BL-119] S338 -- the outputs for fork `main` (`5f09130`): the suite, the nine-mutant round, the field case, the 177-piece sweep

Four saved outputs, `bl119-main-*` under `docs/planning/pr94-rewrite/evidence/`, written by the claimed session in a scratch clone that no longer exists. Reproduced today in fresh clones of `6907c53` plus the build: the mutant output and the sweep are byte-identical to the saved files, the suite output differs from the saved one only in its timing line, and the field case gives the same three exits (frozen proof 1, `--reverify` under 1.8.0 1, under 1.8.1 3; the commit hash in the proof's message is the clone's head). The numbers: 222 tests OK (2 skipped, as before); 8 of 9 mutants killed, each by its intended test, the ninth the equivalent change the template pin must let through; 177 archived pieces, the same exit under 1.8.0 and 1.8.1 in every one (172 at 0, 2 at 1, 2 at 3, 1 at 4).

### 2026-10-18 · [BL-119] S338 -- the builder, the mutation round, a field-case script and the sweep script's one new argument, kept as evidence

Four files under `docs/planning/pr94-rewrite/evidence/`. `bl119-build.py` (ports `1082d3b`'s hunks onto a tree with the layout trimmer; refuses on drift, writes four files, no ledger entry) and `bl119-mutants.py` (nine mutants, one at a time, the trimmer restored byte for byte) were written by the claimed session before it stopped and were left untracked; both ran again today, unchanged, against fork `main` at `6907c53` and against the candidate at `cfcc713`, and refused nowhere. New: `bl119-field-case.sh`, the depth-1 clone procedure the claimed session ran by hand, as a script so it can be run for the candidate. `fork_shards_compare.sh` gains an optional 5th argument, the repository to sweep (default unchanged; arguments 1 to 4 as before), so the sweep runs in a clean clone while the live tree takes commits.

### 2026-10-18 · [BL-119] S338 -- the proof's abort exits 3, not 1, in the fork's own trimmer: PR #94's fifth commit `1082d3b` ported onto `main` (`TRIM_VERSION` 1.8.0 to 1.8.1); nothing sent

Resumed at his Phase 0 picker ("Resume BL-119") after the claimed session stopped before landing any change. In the proof template (`VERIFY_TEMPLATE`) one `unfinished(why)` prints the reason to stderr and exits 3, "the proof did not finish" (the code `--reverify`'s legend gives), where `show()` ended in `sys.exit("verify: cannot read ...")`, exit 1, the FAIL code; `show()` and `readf()` both go through it. The four tests of `1082d3b` (`TestAnAbortBeforeTheChecksIsNotAVerdict`) are carried as the same text, plus the one edit `1082d3b` did not need: this tree's test that pins the proof template to 1.7.0's text (`TestTheLegacyLayoutIsByteForByteWhatItWas`) now maps the 1.8.1 abort block back to 1.7.0's and asserts that block is the exact one in use, so every other byte stays pinned (renamed `..._and_the_abort_hunk_only`, same count). The `--reverify` sentence in `FRAMEWORK_APPARATUS.md`; the `trimmer-unit-tests` gate 218 to 222 (a tightening). Built by `docs/planning/pr94-rewrite/evidence/bl119-build.py` in a clean `--no-local` clone of `6907c53` (it refuses on drift; no inserted line is over 100 characters). Measured before this commit: the trimmer suite 222 tests OK (45 s, 2 skipped as before); `bl119-mutants.py` 8 of 9 killed, each by its intended test, the ninth a deliberate equivalent change that must survive; on a depth-1 clone, where the trim commit's parent is absent, the frozen proof exits 1 (frozen, unchanged) and `--reverify` exits 1 under 1.8.0 and 3 under 1.8.1 with the same reason text. **Not yet run at this commit:** the 177-shard sweep under both versions, and `bin/tests.sh` with the ratchet in a clean clone; both follow in the evidence commit. `pr2/candidate` is the next commit's, not this one.

### 2026-10-17 · [BL-119] S338 claim (in progress) -- the proof's abort exits 3, not 1, in the fork's own trimmer and in `pr2/candidate`; nothing sent

CHANGELOG: pending. Taken at his Phase 0 picker answers: "BL-119: same abort in the fork's trimmer (Recommended)", the `HANDOFFS.md` trim first (done: the trim `5f157fb` and its fold `7d1fae7`), and, at the scope question, "Both trees at 1.8.1 (Recommended)". The deliverable: PR #94's fifth commit `1082d3b` (the proof template's `unfinished(why)`, `show()` and `readf()` routed through it, `TestAnAbortBeforeTheChecksIsNotAVerdict`, the `--reverify` sentence in `FRAMEWORK_APPARATUS.md`, the `trimmer-unit-tests` gate) ported onto fork `main` (the layout trimmer, `TRIM_VERSION` 1.8.0 to 1.8.1, gate 218 to 222) and onto `pr2/candidate` (`cfcc713`; a 34th commit, 1.8.0 to 1.8.1), then the one upstream pull request's text (`docs/planning/upstream-pr-body.md`, decision 3: "both trimmers are 1.8.0", measured against #94's head `2308553`) re-measured against `1082d3b` with `pr4-claims.sh` (`HEAD94=1082d3b HEAD92=fa2bb5d`). Nothing is sent to `KJ5HST/methodology`; `pr2/candidate` stays a local ref. Phase 0: `HEAD` `7a0b473` equal to `origin/main`, `CHANGELOG.md` frontier at `HEAD`, 0 undocumented sessions, 0 merges, no pending receipt, S337's gate citation equal to its saved output, `check-ledger`, `check-handoff` and `check-links` exit 0, `upstream/main` `f34769f`, PR #94 at `1082d3b` and PR #92 at `fa2bb5d` with 0 comments and 0 reviews, issue #93's one comment his own, #95 unanswered, dashboard 72/100, 4 receipts at rest before the trim and 3 after.

### 2026-10-17 · [ad hoc] S338 -- the HANDOFFS trim's pointer block folded into the archive index (the trim itself is the tool's entry below, commit `5f157fb`, ticked at the S338 Phase 0 picker)

The trim: `python3 starter-kit/methodology_trim.py --file HANDOFFS.md --cut 3 --force`, then `--write`: S334's receipt to `docs/archive/HANDOFFS-through-2026-10-16-3.md`, 4 receipts to 3 (S337, S336, S335), 48,176 B to 37,465 B; the shard's own proof exit 0 before the commit, `bin/check-handoff` and `bin/check-ledger` exit 0. The tool printed `CUT_STRADDLES_DAY`, `SHARD_NAME_DISAMBIGUATED` (the `-3` suffix) and `FRONTMATTER_FIELD_ABSENT`, all expected. The fold, in its own commit as the index's rule says: the pointer block left `HANDOFFS.md` and one row joined `docs/HANDOFFS_ARCHIVE_INDEX.md` (`| 1 | 2026-10-16 → 2026-10-16 | HANDOFFS-through-2026-10-16-3.md | v1.8.0 |`). The retention rule in the front matter still says N=2 and `--cut 2`; the S322 decision (BL-108, trim above 3) is applied here as the last trims applied it, and the edit to the rule stays BL-108's. Not pushed: the trim and the fold are not ledger-only commits.

### 2026-10-17 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-16-3.md` (1 record(s), 48,176 B → 37,465 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-16 → 2026-10-16) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-16-3.md`](docs/archive/HANDOFFS-through-2026-10-16-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-16-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-16-3.md.verify.sh)
rather than trusting a digest printed here. Live file 48,176 B → 37,465 B (−22.2%).

### 2026-10-17 · [BL-118] S337 -- push record: the two post-close-out commits to the fork `origin`, under his close-out tick for this session's commits

`git push origin main`: `origin/main` b9d83c5 to `f573be2` (BL-118's closure and BL-119, the record); read back equal to `HEAD`. The fork remote only. This entry's own commit is ledger-only and is pushed under the standing grant for push records.

### 2026-10-17 · [BL-118] S337 -- the record after the push: `pr94-rewrite/README.md`'s status line, §Built at S337's heading and its push paragraph marked done, the `body.md` row (draft 9, 28,118 B); `body.md` is the posted text

Record-only, after the two outward actions above; `bin/check-links` exit 0.

### 2026-10-17 · [BL-118] S337 -- after the close-out, at his picker: the fifth commit pushed to PR #94 and its body PATCHed with the Commit 5 paragraph, both read back; BL-118 CLOSED, BL-119 raised (the same abort in the fork's own trimmer and the candidate)

Pre-flight: PR #94 at `2308553`, open, 0 comments, 0 reviews; the posted body equal to the saved `docs/planning/pr94-rewrite/body.md` (27,328 B) after one trailing newline; the local branch at `1082d3b`. **(1)** `git push origin fix/trim-verify-false-red-issue93`, a fast-forward: PR #94's head read back `1082d3b11e6073faf5f3e6154c8816e399e7d315`, five commits. **(2)** `gh api -X PATCH repos/KJ5HST/methodology/pulls/94 -F body=@<file>`: the "Commit 5" paragraph (788 B, verbatim from the record's quoted draft at `README.md:124`) inserted after Commit 4's closing paragraph, 27,328 B to 28,118 B, read back equal; the title unchanged. The saved copy `body.md` is now the posted text (draft 9). **BL-118 CLOSED** (the three edits: the index row out of `BACKLOG.md`, the id into §Completed items' list, the completed row into `BACKLOG-COMPLETED.md`; the detail's outcome paragraph). **BL-119 raised:** the fork's own `starter-kit/methodology_trim.py` on `main` and `pr2/candidate` carry the same `show()` abort; the version question (the fork's 1.8.0 against #94's 1.8.1) and PR5's decision 3 re-measure against `1082d3b` go with it. The S337 receipt's next step (3) and gotcha (1) carry a marked amendment (done after the close-out; the receipt's `commit:` slot is unchanged). Both backlog proofs, `bin/check-handoff`, `bin/check-ledger` and `bin/check-links` exit 0 (run below, before the commit).

### 2026-10-17 · [BL-118] S337 -- push record: this session's commits to the fork `origin`, his tick at the Phase 0 picker

`git push origin main`: `origin/main` 97dddaa to `73ac035`, 8 commits (the trim `787ad83`, the fold `499b436`, the claim `6a7e1ce`, the four evidence-and-record commits `a2d40db`, `2c594db`, `db96cef`, `c68d732`, the close-out `73ac035`); read back with `git ls-remote origin refs/heads/main`, equal to `HEAD`. The fork remote only; nothing to `KJ5HST/methodology`; the local branch `fix/trim-verify-false-red-issue93` (`1082d3b`) is not pushed. This entry's own commit is ledger-only and is pushed under the standing grant for push records.

### 2026-10-17 · [BL-118] S337 close-out -- BL-118 built on a local copy of PR #94's branch (`1082d3b`, 1.8.1: an abort before the proof's checks exits 3, not 1), not pushed (this entry resolves the claim `6a7e1ce`, which stays `in progress` above): receipt complete, the fork's gate run saved

Phase 3: the predecessor's handoff (S336) scored 8 and this session 8 (both in the receipt); Phase 3C appended fork learning #109 and retired no row (D3; rows considered #62 and #30; in the fourth evidence-and-record commit `c68d732`); the receipt in `HANDOFFS.md` is complete; `bin/check-handoff`, `bin/check-ledger` and `bin/check-links` exit 0 on this tree. The fork's gate run, in a clean `--no-local` clone of `c68d732` (the last work commit; this entry's commit changes `HANDOFFS.md`, this file and adds the saved output, no code): 18/18 pass · 0 fail · 0 unmeasured · results d7576eaf9b5b · manifest a690abd884d4 (1187 s, about 20 min, at a load average of 5.27, 6.19, 7.20 at the start and 5.55, 5.91, 6.38 at the end); saved as `docs/planning/pr94-rewrite/evidence/s337-fork-gate-output.txt`. The one upstream pull request's text (`upstream-pr-body.md`) is unchanged and still states both trimmers at 1.8.0 against #94's head `2308553`; it goes stale only if `1082d3b` is pushed. Nothing is sent to `KJ5HST/methodology`; the push of this session's commits to the fork `origin` (ticked at the Phase 0 picker) follows this commit and is recorded in its own entry.

### 2026-10-17 · [BL-118] S337 -- `BACKLOG.md`'s BL-118 row reads BUILT at S337, not pushed; fork learning #109 appended (an abort path inherits the language's default exit code; 1,381 B; `bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations` exit 0, 94 rows, 0 over 1,500 B)

The fourth of four. Phase 3C's retirement rule (D3 of the retirement plan): no row retired; considered #62 (a spent exit code) and #30 (facts baked into an exported check), neither enforced by a gate or restated by a later row. The completed-items proof exit 0. Nothing sent.

### 2026-10-17 · [BL-118] S337 -- the fifth commit's record: `ratchet-run-1.8.1.txt` (12/12), `pr94-rewrite/README.md` §Built at S337 (with the drafted "Commit 5" paragraph, not posted, and the status line brought current), `evidence/README.md` §Added at S337, and the BL-118 detail paragraph (BUILT, not pushed)

The third of four; `bin/check-links` exit 0 with every evidence file it names present; the detail proof exit 0. Nothing sent.

### 2026-10-17 · [BL-118] S337 -- the fifth commit's measurements saved: `trimmer-suite-1.8.1.txt` (203 tests OK), `field-case-1.8.0-vs-1.8.1.txt` (the four runs with their exit codes), `sweep-after-1.8.1.tsv` (46 at 0, 8 at 4, 0 at 1) and `tests-sh-1.8.1.txt` (261 passed) into `docs/planning/pr94-rewrite/evidence/`

The second of this session's four evidence-and-record commits (the first carries the build's entry below); the per-commit cap of five files (`SAFEGUARDS.md`) is why the drop is split. Nothing sent.

### 2026-10-17 · [BL-118] S337 -- the fifth commit `1082d3b` built on a local copy of PR #94's branch (1.8.1: an abort before the proof's checks exits 3, not 1), its tests, mutants, sweep and field case; the records, the evidence, the backlog row and fork learning #109; nothing sent

The build (`docs/planning/pr94-rewrite/README.md` §Built at S337; `evidence/README.md` §Added at S337): in a scratch `--no-local` clone at `2308553` with the hooks armed, `evidence/bl118-build.py` (refuses on drift and on a line over 100 characters; its first run refused on a 102-character line of mine, nothing written) edited four files; the trimmer suite 203 tests OK (36 s); `evidence/bl118-mutants.py` 6 of 6 killed by the intended test; the field case on a fresh partial clone of the #93 repository with the promisor remote pointed at a dead path (the frozen proof and 1.8.0's `--reverify` exit 1, 1.8.1's `--reverify` exit 3 with the same reason and no `FAIL:`; `evidence/field-case-1.8.0-vs-1.8.1.txt`); the ledger entry in the branch's `CHANGELOG.md`; the commit `1082d3b` (+139 / -6, 5 files) under the branch's own hooks; the 54-shard `--reverify` sweep with the remote alive 46 at 0 and 8 at 4, identical row by row to S335's; in a clean clone of `1082d3b` `bin/tests.sh` 261 passed, 0 failed and the ratchet 12/12 pass, 0 fail, 0 unmeasured (results `cb7ffb255deb`, manifest `072b6ca7f1a0`); `git merge-tree` clean against `upstream/main` `f34769f` and PR #92's `fa2bb5d`. The commit was fetched back and the local branch `fix/trim-verify-false-red-issue93` fast-forwarded `2308553` to `1082d3b`; `origin`'s copy, PR #94's head, is still `2308553`, and the push is his go-ahead. Fork-side, in this entry's commits: the evidence files (`0002-trim-1.8.1.patch`, the two scripts and their outputs, the suite, sweep, field-case and two gate outputs), the record's new section with a drafted "Commit 5" paragraph for the posted body (not posted) and its status line brought current, `BACKLOG.md`'s BL-118 row (BUILT, not pushed) and its detail paragraph, fork learning #109 (an abort path inherits the language's default exit code; `bin/check-learnings` exit 0, 94 rows, 0 over 1,500 B), both backlog proofs exit 0. Nothing is sent to `KJ5HST/methodology`.

### 2026-10-17 · [BL-118] S337 claim (in progress) -- the generated proof's abort exits 3, not 1: a fifth commit built on a local copy of PR #94's branch; nothing sent

CHANGELOG: pending. Taken at his Phase 0 picker answers: "BL-118: proof exits 3, not 1 (Recommended)" and, for the side actions, the `HANDOFFS.md` trim (done first: the trim `787ad83` and its fold `499b436`) and the push to the fork `origin` at close-out. The deliverable: one commit on a local copy of PR #94's branch `fix/trim-verify-false-red-issue93` (tip `2308553`, four commits over `upstream/main` `f34769f`) in which the proof template's `show()`, and any other abort before the checks, prints its message to stderr and exits 3, the code `--reverify`'s legend gives "the proof did not finish", instead of `sys.exit("<text>")`'s 1, the FAIL code, so a proof that compared nothing no longer reads as a trim that lost something (S335 saw one such false FAIL in the #93 repository's sweep, a transient blob fetch in a partial clone); with a test that plants an unreadable ref (a shallow clone, the trim commit's parent absent) and asserts exit 3, the message and no `FAIL:` line, a mutant that restores exit 1, the trimmer suite, `bin/tests.sh` and the ratchet in a clean `--no-local` clone, and the #93 repository's 54 proofs under `--reverify` again. The commit is built in a scratch clone and fetched back to the local branch; a push to #94 is outward and his go-ahead; nothing is sent to `KJ5HST/methodology`. Phase 0: `HEAD` `97dddaa` equal to `origin/main`, `CHANGELOG.md` frontier at `HEAD`, `HANDOFFS.md` frontier one commit behind (the S336 push record, not a session), 0 undocumented sessions, 0 merges, no pending receipt, S336's gate citation equal to its saved run output, the five checkers and the completed-items proof exit 0, `upstream/main` still `f34769f`, PR #94 at `2308553` (0 comments, 0 reviews), PR #92 at `fa2bb5d` (0, 0), issues #93 and #95 with no reply from anyone, dashboard 72/100, `context_budget.py --status` exit 2 (the same six rows over, none a declared gate), `HANDOFFS.md` at 4 receipts at rest before the trim, load average 5.7.

### 2026-10-17 · [ad hoc] S337 -- the HANDOFFS trim's pointer block folded into the archive index (the trim itself is the tool's entry below, commit `787ad83`, ticked at the S337 Phase 0 picker)

The trim: `python3 starter-kit/methodology_trim.py --file HANDOFFS.md --cut 3 --force`, then `--write`: S333's receipt to `docs/archive/HANDOFFS-through-2026-10-16-2.md`, 4 receipts to 3 (S336, S335, S334), 47,704 B to 37,397 B; the shard's own proof exit 0 before the commit and again after the fold, `bin/check-handoff` and `bin/check-ledger` exit 0 at each. The tool printed `CUT_STRADDLES_DAY` (S334's retained receipt is also dated 2026-10-16, so the shard name is a span label, not a day boundary), `SHARD_NAME_DISAMBIGUATED` (S336's shard took the plain name, so this one carries the `-2` suffix) and `FRONTMATTER_FIELD_ABSENT` (this file's header declares no receipt count, on purpose). The fold, in its own commit as the index's rule says: the pointer block (three lines and a blank) left `HANDOFFS.md` (37,397 B to 36,941 B) and one row joined `docs/HANDOFFS_ARCHIVE_INDEX.md` (`| 1 | 2026-10-16 → 2026-10-16 | HANDOFFS-through-2026-10-16-2.md | v1.8.0 |`). The retention rule in the front matter still says N=2 and `--cut 2`; the S322 decision (BL-108, trim above 3) is applied here as the last four trims applied it, and the edit to the rule stays BL-108's. Not pushed: the trim and the fold are not ledger-only commits, so they wait for the close-out push he ticked.

### 2026-10-17 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-16-2.md` (1 record(s), 47,704 B → 37,397 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-16 → 2026-10-16) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-16-2.md`](docs/archive/HANDOFFS-through-2026-10-16-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-16-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-16-2.md.verify.sh)
rather than trusting a digest printed here. Live file 47,704 B → 37,397 B (−21.6%).

### 2026-10-17 · [BL-101] S336 -- push record: this session's commits to the fork `origin`, his tick at the Phase 0 picker

`git push origin main`, `8f493a4..51d9065` (the trim `8c6f624`, the fold `f7edb47`, the claim `2efe2c8`, the build and draft 10 `9ecd0a8`, the claims run and the records `150e1bf`, his answers `8d7316e`, the close-out `51d9065`); read back `0 0` and `ls-remote` equal. The fork only: nothing to `KJ5HST/methodology`; `pr2/candidate` (`cfcc713`) stays local. This entry's own push follows under the standing grant for a ledger-only push record.

### 2026-10-17 · [BL-101] S336 close-out -- PR4's build session done: `cfcc713` on `pr2/candidate` and draft 10 approved and held for PR5 (this entry resolves the claim `2efe2c8`, which stays `in progress` above): receipt complete, the fork's gate run saved

Deliverable: his S333 decisions F1 and F2 carried out (the 33rd commit `cfcc713`, local; draft 10 of `docs/planning/upstream-pr-body.md`, frozen at `150e1bf` and approved at his picker, the 20,863 B body kept); nothing sent to `KJ5HST/methodology`. The `HANDOFFS.md` receipt is `status: complete` (10,162 B of 12,288; `bin/check-handoff` exit 0). **Phase 3E, the repository's own gate run** in a clean `--no-local` clone of `150e1bf` (the last work commit before his answers were recorded; `nohup` and a done-file; 1478 s at a load average of 4.85, 5.27, 6.16 to 5.73, 5.97, 5.83): `quality_ratchet: 18/18 pass · 0 fail · 0 unmeasured · results d7576eaf9b5b · manifest a690abd884d4` (the ids S333 to S335 cited: nothing under `starter-kit/` or `bin/` on `main` changed), saved as `docs/planning/pr-composition-evidence/restore33-fork-gate-output.txt`; the branch's own vetting is `restore33-claims-output.txt` (302 / 0 / 0, 18/18, results `54e8489f99ec`, manifest `88a7b6f562c4`). The commits after `150e1bf` (`8d7316e`, this close-out) change only files under `docs/planning/`, the two ledgers and the memory notes. **Phase 3C: no fork learning row appended** (D3 not triggered; rows considered: #23, which states the lesson of the moved #94 head at least as generally, #19, #31). Scores: predecessor (S335) 8, self 8. Backlog: no row closed or added (the PR4 build is a phase of `upstream-pr-composition-plan.md`, not a row); the plan's status line names the restore and the approval. The next Phase 0 offers the `HANDOFFS.md` trim (4 receipts at rest after this one). Pushed to the fork `origin` after this commit at his Phase 0 tick; the push record follows.

### 2026-10-17 · [BL-101] S336 -- his answers at the picker, the text shown inline first: draft 10 approved as PR4's text and held for PR5, the 20,863 B kept; recorded in the draft's status line, both records and the plan

Decision 1 of the picker: "Approve as PR4's text; hold for PR5" (nothing sent; PR5, the push of the branch and the opening of the pull request, comes after D1 and D4 at his go-ahead; the maintainer has answered none of #92, #93, #94 or #95). Decision 2: "Keep 20,863 B; the additions are facts" (863 B over the 20,000 B budget he set at S332). Written into `docs/planning/upstream-pr-body.md`'s status paragraph (frozen at `150e1bf`), `draft4-record.md` §4 item 1 and §6, `restore33-record.md` §5, and `upstream-pr-composition-plan.md`'s status line (29,933 B of 30,000). The fork's own gate run is of `150e1bf`, launched before this commit; this commit changes four files under `docs/planning/` and this ledger, no code.

### 2026-10-17 · [BL-101] S336 -- `pr4-claims.sh` on `cfcc713` (18/18, 302/0/0, the #94 conflict figures confirmed), the record `restore33-record.md`, `draft4-record.md` §6, the composition plan's status line; nothing sent

The claims run (`docs/planning/pr-composition-evidence/restore33-claims-output.txt`, exit 0, about 29 minutes, clean `--no-local` clones of `cfcc713` and `f34769f`): against the 32nd commit's run it differs in the shortstat (47 files, +19,822 / -1,102), the count (33), the `dashboard-unit-tests` row (`>= 397`, measured 397), both gate ids (results `54e8489f99ec`, manifest `88a7b6f562c4`: a threshold and a measured value changed), section 7's count (33 compared, 0 refusals) and section 8's #94 head (`2308553`: `.quality-gates.json` 1, `FRAMEWORK_APPARATUS.md` 1, the trimmer 12, its tests 8 conflict regions) and in nothing else; the suite 302 / 0 / 0, the gate 18/18 with 0 unmeasured, 80 links in both layouts, 0 literal sites, the resolver block equal in 11 files, #92 clean are unchanged. `restore33-record.md` (the answer, the builder's proof and its first refusal, the verification table, decision 3 re-measured against both #94 heads, draft 10's edits and the byte accounting, what none of it shows); `draft4-record.md` §4 item 2 says F1 and F2 are carried out and §6 records draft 10; `upstream-pr-composition-plan.md`'s status line names the restore and draft 10 (29,914 B of its 30,000 B). Next: the fork's own gate run on this commit, then the text shown to him inline with the post, change or hold question; nothing is sent to `KJ5HST/methodology`.

### 2026-10-17 · [BL-101] S336 -- the 33rd commit on `pr2/candidate` (`cfcc713`: two of the maintainer's dashboard tests restored, `dashboard-unit-tests` 395 to 397), its builder and message, the overlap and distribution figures on the new tip, and draft 10 of PR4's text; the claims run in progress

His S333 decision F1, carried out: in a scratch `--no-local` clone of the fork with `pr2/candidate` fetched in and checked out at `a62bfec`, `docs/planning/pr-composition-evidence/restore33-build.py` (refuses on drift: both files must be the blobs it was derived from, the note it replaces found once, upstream's class located by its header and ended before its third test; proves its output: the gate manifest differs in exactly `dashboard-unit-tests.threshold` 395 to 397 on a `min` gate, the test file's top-level statements gain exactly upstream's `TestCliRemedyProportionality` with `setUp`, `tearDown`, `_project` and the two tests, equal to the syntax tree parsed from `git show f34769f:tools/test_methodology_dashboard.py` lines 2410 to 2457, and nothing else changes; a second run refused) wrote the two files; the restored class alone `Ran 2 tests OK`, the whole dashboard suite `Ran 397 tests OK` (53.8 s), `quality_ratchet.py --precommit` exit 0 by hand (the clone runs no hooks), the commit `cfcc713` with `restore33-message.txt` (the Co-Authored-By trailer by hand), fetched back with the `+` refspec and read back equal; the old tip is pinned as `refs/pr2/candidate-before-fix33` (`a62bfec`); 33 commits over `upstream/main`, `git diff --shortstat` 47 files, +19,822 / -1,102 (was +19,826 / -1,152). The first builder run refused on its own rule (a new comment line of 101 characters) and wrote nothing; the note was reflowed. `pr4-claims.sh` launched on `cfcc713` with `HEAD94=2308553` and `HEAD92=fa2bb5d` (`nohup`, a done-file; its output goes in the next commit). Measured now, git-only: `pr4-supersede.sh` against #94's head `2308553` (`restore33-supersede-output.txt`: of the 506 lines #94 adds to the trimmer and 1,558 to its tests, 77 and 294 are absent from the branch as exact lines; against the old head `972eb2c` the same tip reads 11 and 9 of 430 and 1,136, the draft-9 figures); `git merge-tree` of `cfcc713` against `2308553`: 4 files, 22 regions (the trimmer 12, its tests 8, `.quality-gates.json` 1, `FRAMEWORK_APPARATUS.md` 1; was 3 files, 17 regions against `972eb2c`), `bbe0dc3` alone 13 regions in the same 4 files (was 6 in 2), #92 clean; `pr4-distribution.py` on the new tip (`restore33-distribution-output.txt`: 25 files, +16,856 stay here, 85.0%). Draft 10 of `docs/planning/upstream-pr-body.md`: F1 in (e) (two tests named, the restore cited), F2 as one clause in decision 2, decision 3 re-measured (the figures above; both branches name their trimmer 1.8.0 for different changes; #94's fourth commit is not in the branch), the figures on the new tip, two repeated sentences cut; `pr4-body-check.py` exit 0 against `cfcc713`; the body is 20,863 B, 863 B over the 20,000 B budget he set at S332 (draft 9 was 117 B over): F2 bought 273 B, (e) and decision 3 together 492 B, the commits paragraph 85 B, the cuts gave back 104 B. The text is shown to him after the claims run; nothing is sent to `KJ5HST/methodology`.

### 2026-10-17 · [BL-101] S336 claim (in progress) -- PR4's build session: restore two of the maintainer's dashboard tests on `pr2/candidate`, then draft 10 of the one upstream pull request's text; nothing sent

CHANGELOG: pending. Taken at his Phase 0 picker answers: "PR4 build: restore the two tests, draft 10 (Recommended)" and, for the side actions, the `HANDOFFS.md` trim (done first: the trim `8c6f624` and its fold `f7edb47`), the local branch tidy (recorded in the fold's entry) and the push to the fork `origin` at close-out. The deliverable, his two S333 decisions carried out (`docs/planning/pr-composition-evidence/draft4-record.md` §5, F1 and F2): a 33rd commit on the local ref `pr2/candidate` (tip `a62bfec`, 32 commits over `upstream/main` `f34769f`) that restores `test_bare_dry_run_refuses_instead_of_writing` and `test_a_normal_run_still_writes` from upstream's `TestCliRemedyProportionality` (`git show f34769f:tools/test_methodology_dashboard.py`, the class at 2410, its helper `_project` at 2423) in place of the candidate's "deliberately not carried" note, and raises `dashboard-unit-tests` 395 to 397 (a tightening); built in a scratch `--no-local` clone with a builder that refuses on drift, the suite run there, fetched back after the old tip is pinned as `refs/pr2/candidate-before-fix33`; then `pr4-claims.sh` on the new tip (about 35 minutes; `HEAD94` passed as `2308553`, PR #94's head since S335, so decision 3's conflict and overlap figures are re-measured, with `pr4-supersede.sh`); then `docs/planning/upstream-pr-body.md` draft 10: item (e) says two tests, decision 2 names the first-parent gate-history walk in one clause, the figures follow the new tip, `pr4-body-check.py` exit 0, the 20,000 B body budget he set at S332 held or the overrun stated; the text shown inline and his answer asked (post, change or hold). Scope: nothing is sent to `KJ5HST/methodology`; `pr2/candidate` stays local; no fifth read is bought without stating its cost. Phase 0: `HEAD` `8f493a4` equal to `origin/main`, `CHANGELOG.md` frontier at `HEAD`, `HANDOFFS.md` frontier one commit behind (the S335 push record, not a session), 0 undocumented sessions, 0 merges, no pending receipt, the five checkers and the completed-items proof exit 0, `upstream/main` still `f34769f`, PR #94 at `2308553` (0 comments, 0 reviews), PR #92 open, issues #93 and #95 with no reply from anyone, dashboard 72/100, `context_budget.py --status` exit 2 (the same six rows over, none a declared gate), `HANDOFFS.md` at 4 receipts at rest before the trim, the `methodology-bl57` worktree clean.

### 2026-10-17 · [ad hoc] S336 -- the HANDOFFS trim's pointer block folded into the archive index (the trim itself is the tool's entry below, commit `8c6f624`, ticked at the S336 Phase 0 picker)

The trim: `python3 starter-kit/methodology_trim.py --file HANDOFFS.md --cut 3 --force`, then `--write`: S332's receipt to `docs/archive/HANDOFFS-through-2026-10-16.md`, 4 receipts to 3 (S335, S334, S333), 46,967 B to 37,989 B; the shard's own proof exit 0 before the commit and again after the fold, `bin/check-handoff` and `bin/check-ledger` exit 0 at each. The tool printed `CUT_STRADDLES_DAY` (S333's retained receipt is also dated 2026-10-16, so the shard name is a span label, not a day boundary) and `FRONTMATTER_FIELD_ABSENT` (this file's header declares no receipt count, on purpose). The fold, in its own commit as the index's rule says: the pointer block (three lines and a blank) left `HANDOFFS.md` (37,989 B to 37,541 B) and one row joined `docs/HANDOFFS_ARCHIVE_INDEX.md` (`| 1 | 2026-10-16 → 2026-10-16 | HANDOFFS-through-2026-10-16.md | v1.8.0 |`). The retention rule in the front matter still says N=2 and `--cut 2`; the S322 decision (BL-108, trim above 3) is applied here as the last three trims applied it, and the edit to the rule stays BL-108's. **Also at his tick, local only, no commit:** the stale local branch `fix/trim-verify-false-red-issue93` (at `972eb2c`) was fast-forwarded to `2308553`, the tip `origin` serves as PR #94's head (`972eb2c` is its ancestor), and the local `-v2` branch that held that tip was deleted; nothing on any remote changed. Not pushed: the trim and the fold are not ledger-only commits, so they wait for the close-out push he ticked.

### 2026-10-17 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-16.md` (1 record(s), 46,967 B → 37,989 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-16 → 2026-10-16) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-16.md`](docs/archive/HANDOFFS-through-2026-10-16.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-16.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-16.md.verify.sh)
rather than trusting a digest printed here. Live file 46,967 B → 37,989 B (−19.1%).

### 2026-10-17 · [BL-116] S335 -- push record: the correction commit `acb080a` to the fork `origin`

`git push origin main`: `eff5681..acb080a`, read back with `git rev-list --left-right --count origin/main...HEAD` = `0 0`. Nothing goes to `KJ5HST/methodology`. A ledger-only push record, which his standing grant lets go to the fork unasked.

### 2026-10-17 · [BL-116] S335 -- a correction after the close-out: BL-116's id added to the §Completed items list in `BACKLOG.md`; the completed-items proof read exit 1 at `01bb954` and the script did not stop

`docs/planning/BACKLOG-COMPLETED.md.verify.sh` printed `FAIL C6 reachability since the move: no id in docs/planning/BACKLOG.md for BL-116` before the backlog commit `01bb954`; the close-out script captured the exit code into its output and went on to commit and push (`1f20fb4`, `eff5681`) because nothing gated on it. Closing an item here is three edits, not two: the index row out, the id into the hand-maintained list under §Completed items, the completed row in; the second was missing. Fixed: `**BL-116**` appended to that list after `**BL-107**`; the proof now exits 0 (C1 to C6 OK). The S335 receipt's `runtime_smoke` and `what_was_done` are amended to say so (the receipt had claimed the proof exit 0). A memory note records the rule: every checker in a scripted sequence gets an explicit stop on non-zero. Pushed after this commit with its own record; his tick for the session's commits covers it.

### 2026-10-17 · [BL-116] S335 -- push record: this session's 11 commits to the fork `origin`, his tick at the picker ("Push the fork's S335 commits to origin")

`git push origin main`: `07f00ec..1f20fb4` (the trim `a3c5c84`, its fold `9318b63`, the claim `6b3570a`, the evidence and text `9db9f98` `f9625a6` `f08b64b` `80e143a` `d274d97`, the record `616cd46`, the post and closures `01bb954`, the close-out `1f20fb4`), read back with `git rev-list --left-right --count origin/main...HEAD` = `0 0`. Nothing of this goes to `KJ5HST/methodology`; the PR branch push was recorded separately above. This entry is the ledger-only push record that his standing grant lets go to the fork unasked.

### 2026-10-17 · [BL-116] S335 -- close-out -- the fourth commit on PR #94 and the draft-8 text posted (this entry resolves the claim `6b3570a`, which stays `in progress` above): receipt complete, the fork's gate run saved

Deliverable: BL-116 done; the `HANDOFFS.md` receipt is `status: complete` (10228 B of 12,288; `bin/check-handoff` exit 0). **Phase 3E, the repository's own gate run** in a clean `--no-local` clone of `616cd46` (the last work commit; `nohup` and a done-file; 20 min 56 s at a load of 6 to 8.5): `quality_ratchet: 18/18 pass · 0 fail · 0 unmeasured · results d7576eaf9b5b · manifest a690abd884d4` (the ids S334 cited), saved as `docs/planning/pr94-rewrite/evidence/s335-fork-gate-output.txt`; the PR branch's own vetting is in `tests-sh-1.8.0.txt` and `ratchet-run-1.8.0.txt`. **Phase 3C: no fork learning row appended (D3 not triggered); rows considered: #42 (a ratio measured on one class does not transfer to the class just separated from it: my "4 of 12" before splitting live stubs from finished records), #61, #74, #88 (re-run the unchanged side: the sweep under both versions).** Two lessons went to memory (his performance question; a changed verdict in a sweep over a partial clone is re-run first). Predecessor S334 scored 8; self 8. **Sizes at close:** `HANDOFFS.md` holds 4 receipts (S335, S334, S333, S332), above his 3: the next Phase 0 offers `--cut 3 --force`; `CHANGELOG.md` 69667 B before this entry (trigger 196,608 B, not due). The push to the fork `origin` follows this commit at his tick, with its own record.

### 2026-10-17 · [BL-118] S335 -- raised: a generated proof that cannot read an artifact from git exits 1, the FAIL code, where --reverify promises 3

Found in the first 54-shard sweep of the 1.8.0 trimmer: one shard read exit 1 with `verify: cannot read 7a55e19^:SESSION_NOTES.md` after a transient promisor-remote fetch failure in the partial clone; exit 0 on re-run under both versions. `VERIFY_TEMPLATE`'s `show()` calls `sys.exit("verify: cannot read ...")`, which exits 1. Offered to him as "Hold: fix the exit-3 finding first" at the picker; he chose to post without it, so it is a row: the fix is exit 3 with the message on stderr, a test with an unreadable ref, a mutant; fork-side first, a fifth PR commit being outward.

### 2026-10-17 · [BL-117] S335 -- raised at his tick: a performance session for the fork's own tooling, with today's measured baselines

He asked twice in this session whether performance-improvement opportunities were being looked for; the answer was no, not inside one deliverable, and he ticked the row at the picker. The row and its detail carry the baselines measured today (the trimmer suite 199 tests in 37.5 s; the 54-shard sweep under 2 minutes cached and about 10 minutes cold; the fork's gate run 20 min 56 s for 18 gates; upstream's 12 gates with `bin/tests.sh` under 6 minutes) and three candidate targets, none measured as a bottleneck; the session's rule is profile first, change one thing, re-measure, and a speed-up that changes a verdict or a count is a defect.

### 2026-10-17 · [BL-116] S335 -- BL-116 closed: the index row out, the completed row in, the detail carries the closing state; BL-98's row names the fourth commit

`docs/planning/BACKLOG.md`: the BL-116 row removed (the id stays in the record); BL-98's row gains the S335 state (the fourth commit on PR #94, the draft-8 text, 46 / 8 / 0, still a watch item). `docs/planning/BACKLOG-COMPLETED.md`: one `✅ DONE 2026-10-17 (S335)` row after BL-107's. `docs/planning/BACKLOG-DETAIL.md` §BL-116: the closing paragraph (the decisions, the build, the measurements, the two outward actions, what stays open). `BACKLOG-COMPLETED.md.verify.sh` run after the edit (see the commit). `BACKLOG.md` was already over its reported 25,000-token ceiling at Phase 0 and grows by two rows here (no declared gate caps it).

### 2026-10-17 · [BL-116] S335 -- outward action, his "Post now" at the picker: PR #94's title and body set to the saved draft-8 text

`gh api -X PATCH repos/KJ5HST/methodology/pulls/94 -f title="$(cat docs/planning/pr94-rewrite/title.txt)" -F body=@docs/planning/pr94-rewrite/body.md`, exit 0, after the push had been read back. Read back with `gh pr view 94 --json title,body`: the title equals `title.txt`; the body equals `body.md` byte for byte (27,325 characters, 27,328 bytes), GitHub's `updatedAt` 2026-10-17T05:14:47Z. The old title was `fix(trim): generated proofs stop reading red on lossless trims, and --reverify re-derives a frozen one (refs #93)`; the old body is kept as `docs/planning/pr94-rewrite/original-body.md`. Draft 8 had no cold read; he read it inline, asked whether to hold it for a performance session (no: performance work is a separate commit and session), and ticked "Post now".

### 2026-10-17 · [BL-116] S335 -- outward action, his "Post now" at the picker: the fourth commit pushed onto PR #94's head branch

`git push origin fix/trim-verify-false-red-issue93-v2:fix/trim-verify-false-red-issue93`: `972eb2c..2308553`, a fast-forward (the commit's parent is the PR's old tip). Pre-flight first: PR #94 at `972eb2c` with 0 comments and 0 reviews, `origin`'s branch at `972eb2c`, `upstream/main` at `f34769f`, the local branch an ancestor-preserving descendant. Read back: `git ls-remote origin refs/heads/fix/trim-verify-false-red-issue93` = `2308553764174551424be1fef971a0b93dc85aff`, and `gh pr view 94 --json headRefOid` the same; GitHub lists the PR's four commits `68d8a06`, `965f136`, `972eb2c`, `2308553`. The local branch `fix/trim-verify-false-red-issue93` (without `-v2`) still points at `972eb2c`.

### 2026-10-16 · [BL-116] S335 -- the record: his four decisions, the fourth commit on the local branch, what was measured, the two things to know, the posting steps

`docs/planning/pr94-rewrite/README.md` recomposed: the status (draft 8; `2308553` on a local branch; not pushed, not posted), the section "Decided and built at S335" (the decisions, where the change is and the patch that keeps it, what the commit changes by `--numstat`, the marker's measured shape and my own "4 of 12" miscount corrected to 3, the measurements table with the evidence file for each row, the version-number collision with this fork's 1.8.0, and a finding not fixed: a proof that cannot read an artifact from git exits 1, the same code as a FAIL, where 3 is promised), and "Posting it" with the push of the branch (a fast-forward of the PR's head) before the title and body edit, each read back and each his go-ahead. The S334 sections stay as the record of that session.

### 2026-10-16 · [BL-116] S335 -- the PR text, draft 8 (title and body), the sync test's output and the evidence index

`docs/planning/pr94-rewrite/body.md` is draft 8 (27328 B; draft 7 was 20,651 B): the Summary and Background, a Commit 4 paragraph, "What remains, and why the 8 stay FAILs" with a fourth table column, the Evidence (tests 199, gates 12/12, `bin/tests.sh` 261/0, the 17 mutants, the sweep 46/8/0, the fork's 174 shards, the 12 adopters, sync, merge) and the Adopter impact (a third ledger, the Class A arm at the root, the edited-copy case after a forced sync, the proof's longer output) changed; his S334 rules kept (every term defined at first use, every count with its denominator, no bare "it"). `title.txt` names the three things the PR does and the file it adds to the table. **Draft 8 has had no cold read.** `evidence/sync-test-1.8.0.txt` (a fresh project receives both files byte-identical at 1.8.0; the #93 repository's edited copy still exits 2 without `--force`; after a forced sync the canonical entry reads that repository's notes file as its own entry did, 42 records). `evidence/README.md` gains the S335 table and the reproduction of the build's checks. Nothing is posted.

### 2026-10-16 · [BL-116] S335 -- saved outputs, part 2: the 8 labelled `--reverify` outputs with their diffs, the trimmer suite, `bin/tests.sh` and the gate run in the clean clone

`evidence/reverify-outputs-8-labelled-1.8.0.txt` (each of the 8 carries the specific `FAIL:` line, the `NOTE:` and a `DIFF:` block of 30 to 176 lines), `evidence/trimmer-suite-1.8.0.txt` (199 tests, OK, 2 skipped, 37.5 s), `evidence/tests-sh-1.8.0.txt` (261 passed, 0 failed, in a clean `--no-local` clone of `2308553` with `core.hooksPath .githooks`), `evidence/ratchet-run-1.8.0.txt` (12/12 pass · 0 fail · 0 unmeasured · results `28a2fdac6745` · manifest `dfb478526806`; the two runs took under 6 minutes together at a load of 6 to 8).

### 2026-10-16 · [BL-116] S335 -- saved outputs, part 1: the adopters' claim-line census and `--check`, this fork's 174 shards under both versions, the 54-proof sweep under 1.8.0

`evidence/adopter-claim-lines-output.tsv` (3 finished records in 3 of 12 adopters carry the status line, 2 without the tag; the other hits are live record-0 stubs), `evidence/adopter-check-output.txt` (10 parse, 1 `NO_RECORDS`, 1 `GRAMMAR_MISMATCH`, 0 zone refusals), `evidence/fork-shards-old-vs-new.tsv` (174 rows; every exit code equal under 1.7.0 and 1.8.0: 169 at 0, 2 at 1, 1 at 4, 2 at 3), `evidence/sweep-after-1.8.0.tsv` (54 rows: 46 at exit 0, 8 at exit 4). The first sweep read one shard at exit 1 from a transient blob fetch failure in the partial clone; the re-run of that shard read 0 under both versions and this file is the clean second sweep.

### 2026-10-16 · [BL-116] S335 -- the build commit as a patch, the mutation round and its output, the marker measurement's output

`evidence/0001-trim-1.8.0.patch` (commit `2308553` from `git format-patch`, so the change survives the loss of the local branch; `git am` onto `972eb2c`), `evidence/mutants_s335.py` and `evidence/mutants-s335-output.txt` (17 mutants on the new layer: each part of the marker, the grammar's branches and word boundary, the footer, the date function's two steps, the table lookup, seven on the diff; 17 killed, the intended test among the failures every time; a second round added two tests for behaviours no test named), `evidence/marker-measure-output.tsv` (both markers match all 7 real stubs and none of their 7 replacements).

### 2026-10-16 · [BL-116] S335 -- the evidence scripts for the fourth commit: the marker measurement, the adopters' claim-line census, the adopters' `--check`, the fork-shard comparison

`docs/planning/pr94-rewrite/evidence/`: `marker_measure.py` (the two candidate stub markers on the #93 repository's seven real stubs and their replacements), `adopter_claim_lines.py` (every record in the 12 adopters' live notes files that still carries the Phase 1B status line, and whether it keeps the tag), `adopter_check.sh` (`--check`, read-only, of a trimmer on each adopter's notes file), `fork_shards_compare.sh` (`--reverify` exit codes of two trimmer versions over this fork's frozen shards). All read-only; their outputs follow in the next commits.

### 2026-10-16 · [BL-116] S335 -- the build: commit `2308553` on the local branch `fix/trim-verify-false-red-issue93-v2` (one commit on PR #94's tip `972eb2c`), a branch operation in this clone only; not pushed

Built in a worktree under the session scratchpad after his four decisions at the picker (D2 stays exit 4; a canonical `SESSION_NOTES.md` entry; the whole record-0 diff; three causes in the report, one pattern in the result), test-first (18 new tests seen red: 9 failures, 9 errors, all `NO_CONFIG` or a missing key), then the tool. `starter-kit/methodology_trim.py` 1.8.0: `_session_notes_date`, the `SESSION_NOTES.md` entry in `LEDGERS` (the runner's two record shapes, no footer, a stub marker requiring both the `**Status:** Session claimed` line and the `(IN PROGRESS)` tag), and the proof prints a unified diff of record 0 against the record that replaced it whenever the frontier was edited in the trim commit; `tools/test_methodology_trim.py` 181 to 199 tests (`TestSessionNotesIsATrimmableLedger`, 18, and two tests moved off the old truth); `FRAMEWORK_APPARATUS.md`'s timing-rule paragraph; the branch's gate 181 to 199; one `[issue #93]` entry in upstream's ledger format. Committed under the branch's own hooks. Measured at the tip: 199 tests OK; in a clean clone `bin/tests.sh` 261/0 and `quality_ratchet.py --run` 12/12; the #93 repository's 54 proofs 46 at exit 0, 8 at exit 4, 0 at exit 1 (was 46/1/7); this fork's 174 shards unchanged under 1.7.0 and 1.8.0; 17 of 17 mutants killed. The branch is on no remote; a push to `origin`'s `fix/trim-verify-false-red-issue93` would move PR #94 and is his go-ahead. The version number collides with this fork's own 1.8.0 (BL-101 P3); recorded in `docs/planning/pr94-rewrite/README.md`.

### 2026-10-16 · [BL-116] S335 claim (in progress) -- improve upstream PR #94 (the fix for issue #93): his four decisions on the 8-of-54 gap, then the build on a local copy of the PR branch; nothing posted

CHANGELOG: pending. Taken at his Phase 0 picker answers: "BL-116: improve PR #94 (Recommended)" and, for the side action, "Trim now: --cut 3 --force (Recommended)" (done first: the trim `a3c5c84` and its fold `9318b63`, both before this claim). The deliverable: the PR branch `fix/trim-verify-false-red-issue93` (tip `972eb2c`, equal on `origin`) changed on a local copy so that the 8 of the #93 repository's 54 proofs that `--reverify` still reports wrong are classified as he decides, with tests and controls (the real-loss shapes must still fail), a mutation round on the changed layer, a vetting in a scratch clone under upstream's own hooks, the 54-proof sweep re-run, and `docs/planning/pr94-rewrite/body.md` updated and shown to him inline. His four decisions come first: D2 of `docs/planning/issue93-trimmer-proof-false-red-plan.md` §9 (a recognised stub finalize stays a FAIL at exit 4, or passes); where a `SESSION_NOTES.md` stub marker comes from (a canonical ledger-table entry, a `--reverify` option, or neither); whether the proof prints the diff of the stub against the finished record 0; the framing of what remains. Scope: nothing is sent to `KJ5HST/methodology`; a push to the branch, a body edit and a comment are each his go-ahead. Phase 0: `HEAD` `07f00ec` equal to `origin/main`, both ledger frontiers at `HEAD`, 0 undocumented sessions, 0 merges, the three checkers exit 0, `upstream/main` still `f34769f`, PR #94 at `972eb2c`, PR #92 at `fa2bb5d`, issues #93 and #95 with no reply from anyone, dashboard 72/100, `context_budget.py --status` exit 2 with six rows over their ceilings (`BACKLOG.md`, `FORK_LEARNINGS.md`, `SESSION_RUNNER.md`, `SAFEGUARDS.md`, the resident total, the read-set total; no declared gate caps them), `HANDOFFS.md` at 5 receipts at rest before the trim, the `methodology-bl57` worktree clean.

### 2026-10-16 · [ad hoc] S335 -- the HANDOFFS trim's pointer block folded into the archive index (the trim itself is the tool's entry below, commit `a3c5c84`, ticked at the S335 Phase 0 picker)

The trim: `python3 starter-kit/methodology_trim.py --file HANDOFFS.md --cut 3 --force`, then `--write`: S331's and S330's receipts to `docs/archive/HANDOFFS-through-2026-10-15-3.md`, 5 receipts to 3 (S334, S333, S332), 57,214 B to 36,679 B; the shard's own proof exit 0 before the commit and again after the fold, `bin/check-handoff` and `bin/check-ledger` exit 0 at each. The tool printed `SHARD_NAME_DISAMBIGUATED` (the third shard to end on 2026-10-15) and `FRONTMATTER_FIELD_ABSENT` (this file's header declares no receipt count, on purpose); no `CUT_STRADDLES_DAY`, since the cut falls between S332's receipt of 2026-10-16 and S331's of 2026-10-15. The fold, in its own commit as the index's rule says: the pointer block (three lines and a blank) left `HANDOFFS.md` (36,679 B to 36,223 B) and one row joined `docs/HANDOFFS_ARCHIVE_INDEX.md` (`| 2 | 2026-10-15 → 2026-10-15 | HANDOFFS-through-2026-10-15-3.md | v1.8.0 |`). The retention rule in the front matter still says N=2 and `--cut 2`; the S322 decision (BL-108, trim above 3) is applied here as the last two trims applied it, and the edit to the rule stays BL-108's. Not pushed: the trim and the fold are not ledger-only commits, so they wait for his tick.

### 2026-10-16 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-15-3.md` (2 record(s), 57,214 B → 36,679 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-10-15 → 2026-10-15) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-15-3.md`](docs/archive/HANDOFFS-through-2026-10-15-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-15-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-15-3.md.verify.sh)
rather than trusting a digest printed here. Live file 57,214 B → 36,679 B (−35.9%).

### 2026-10-16 · [BL-98] S334 close-out -- the PR #94 rewrite saved, not posted (this entry resolves the claim `88f4d9e`, which stays `in progress` above): receipt complete, BL-116 added, the fork's gate run saved

Deliverable: the rewrite of upstream PR #94's title and body, saved in `docs/planning/pr94-rewrite/` (`body.md` draft 7, `title.txt`, `original-body.md`, `README.md`, `evidence/`) at his instruction; the claim was written late, after most of the work, and the receipt says so. His question about the 8 of 54 proofs that still come out wrong is answered in `README.md` and `BACKLOG-DETAIL.md` §BL-116 with the prototype numbers (a `SESSION_NOTES.md` stub marker: all 8 exit 4; also a recognised stub finalize exiting 0: 54 of 54 exit 0, 177 of the PR's 181 trimmer tests passing) and the reason decision D2 is not free (the finished record rewrites the stub's text in all 8). Gate: 18/18, 0 unmeasured, results `d7576eaf9b5b`, manifest `a690abd884d4`, clean `--no-local` clone of `83f5dd0`, about 21 minutes, saved in `docs/planning/pr94-rewrite/evidence/s334-fork-gate-output.txt`. Scores: predecessor (S333) 8, self 7. 3C: no fork learning row (rows considered: #47, #21, #74). BL-116 (improve PR #94, the next session's work) is added to `BACKLOG.md` and `BACKLOG-DETAIL.md` and BL-98's row points at it; `BACKLOG.md` grew by about 330 tokens and was already over its reported ceiling. The `HANDOFFS.md` receipt is complete (`status: complete`); the next Phase 0 offers the `HANDOFFS.md` trim (5 receipts at rest). Nothing is posted to `KJ5HST/methodology`; PR #94 is unchanged. Not pushed at the time of this entry.

### 2026-10-16 · [BL-98] S334 -- saved outputs, part 2: `--reverify` and original-proof output for the 10 failing shards, and the `bin/sync` local-edit test (`docs/planning/pr94-rewrite/evidence/`)

`reverify-outputs-10-failing.txt` and `original-proof-outputs-10-failing.txt` hold the full output of the PR-branch `--reverify` and of the original proofs for the 10 shards that fail as written (each original prints exactly one of three distinguishing failure lines; two of them pass under `--reverify`). `sync-test-output.txt` holds `bin/sync` run from the PR branch against a scratch project with the #93 repository's edited `methodology_trim.py`: exit 2 and an error naming the file without `--force`, "would write" with it (dry runs; the scratch project was unchanged). The scratch paths are written as `$SCRATCH`.

### 2026-10-16 · [BL-98] S334 -- saved outputs, part 1: the prototype sweeps, the stub-survival check, the test run on the prototype (`docs/planning/pr94-rewrite/evidence/`)

`sweepA.tsv`: with a stub marker for `SESSION_NOTES.md` (`^\*\*Status:\*\* Session claimed\b.*$`, matched as a prefix) `--reverify` gives 46 at exit 0 and all 8 others at exit 4, none at exit 1. `sweepAB.tsv`: if a recognised stub finalize also exits 0 (reverses decision D2), 54 of 54 at exit 0. `stub-survival-output.txt`: in the 8 shards the finished record keeps only the stub's identifying lines; the rest of the stub is absent as whole lines (23 of 24 in the shard whose stub carried prose), so no check of that kind could certify them. `protoAB-test-failures.txt`: the PR's 181 trimmer tests are OK on the unmodified branch (41 s, 2 skipped) and 177 pass with prototype A+B; the 4 that fail assert exit 4 or the label (decision D2); the real-loss tests still pass. Scratch prototypes only; no mutation run on them, so this shows feasibility, not that the change is safe to ship.

### 2026-10-16 · [BL-98] S334 -- the evidence index, `audit_text.py`, the 54-proof table, and a correction to the record (`docs/planning/pr94-rewrite/`)

`evidence/README.md` says what each script and saved output is and how to reproduce the sweeps (a partial sparse clone of the #93 repository at `82433662`; the PR's trimmer from `972eb2c`). `evidence/audit_text.py` compares a rewrite of the body with the body it replaces (sizes, banned tokens, lost or new figures and code names, the word "red", first-use offsets, ambiguous-pronoun sentences). `evidence/sweep-before-after.tsv` is the 54-proof table: exit code as written and under `--reverify`. Correction in `README.md` (committed one entry earlier, `b1d95a8`): it said none of a stub's non-placeholder lines survives in the finished record, which overstated what `stub-survival-output.txt` shows. The identifying lines do survive (the heading of a `SESSION_NOTES.md` record; the fence, `session:` and `date:` lines of a receipt); the rest is absent, and in the `HANDOFFS.md` shard most of the absent lines are `X: pending` placeholder fields. The correction is made in `README.md` itself and stated here, not by editing the earlier entry.

### 2026-10-16 · [BL-98] S334 -- the evidence scripts for the PR #94 rewrite and the 8-of-54 gap (`docs/planning/pr94-rewrite/evidence/`: `sweep.sh`, `sweep_after.sh`, `stub_survival.py`, `make_prototypes.py`)

`sweep.sh` runs each of the #93 repository's 54 frozen proofs as written and then `methodology_trim.py --reverify` on the same shard, writing one exit-code row per shard; `sweep_after.sh` is the `--reverify` half alone, for a different trimmer file. `stub_survival.py` takes the 8 shards that still fail and lists which lines of the pre-trim stub (record 0 at the trim commit's parent) are absent from the finished record that replaced it; it only runs `git log` and `git show`. `make_prototypes.py` builds the two scratch prototypes the sweeps used (a stub marker for `SESSION_NOTES.md`; and, on top, a recognised stub finalize that exits 0, which reverses decision D2 of `docs/planning/issue93-trimmer-proof-false-red-plan.md`); it was run and its output compared with the prototypes the sweeps used, byte for byte. Nothing is posted; the saved outputs are the next entries.

### 2026-10-16 · [BL-98] S334 -- the rewrite of upstream PR #94's title and body saved (`docs/planning/pr94-rewrite/`: `title.txt`, `body.md`, `original-body.md`, `README.md`); not posted

`body.md` is draft 7 (20,651 B; the body it would replace is 5,770 B, kept as `original-body.md` for diffing) and `title.txt` the proposed title. He corrected the text term by term and then said longer is fine when it adds clarity, so the byte-budget habit was dropped for this text. Checked by four independent cold reads (21, 17, 26 and 24 findings, each verified against the code, the adopter repository, a run or the fork's ledger before a change; draft 7 has had no fifth read). Facts measured again by running, not copied: the 54-proof sweep (10 fail as written; `--reverify` gives 46 at exit 0, 7 at exit 1, 1 at exit 4), the sort of the 10 by failure line (7, 2, 1, equal to #93's counts), the commit order, `TRIM_VERSION` and test floor of the three PR commits, the PR branch against the fork's `3616b5f` (six places, seven lines), and `bin/sync` from the PR branch against a project holding the #93 repository's edited trimmer (exit 2; `--force` would overwrite it). `README.md` is the record the next session starts from: the status, his corrections in order, which figures were re-measured and which were copied unchanged, the gap he asked about (8 of the 54 proofs still come out wrong), the options and how to post. PR #94 is unchanged (open, tip `972eb2c`) and nothing is posted to `KJ5HST/methodology`.

### 2026-10-16 · [BL-98] S334 claim (in progress) -- the rewrite of upstream PR #94's title and body, saved for the next session (nothing posted)

CHANGELOG: pending. **Written late, and this entry says so:** the Phase 0 report was given and its picker (which deliverable; trim `HANDOFFS.md`; push at close-out) went unanswered, because he asked instead "can PR #94 be edited to be more clear?" and then corrected the text term by term (the dropped denominator 54, "ledger", "red proof", what `--reverify` is an argument for, "inside"). The Phase 1B stub that goes before technical work was not written first; that lapse is disclosed in the close-out receipt. At his instruction ("Let's call the work you have done and currently finishing up serve as your deliverable. Save this rewrite for later use. In the next session, we work on improving this PR.") the deliverable is the saved rewrite: `docs/planning/pr94-rewrite/` (title, body, the original body, a record) with its evidence scripts and saved outputs. Nothing is posted to `KJ5HST/methodology`; PR #94 is unchanged (open, tip `972eb2c`); closing the 8-proof gap is the next session's. Phase 0: `HEAD` `dc30f85` equal to `origin/main`, `CHANGELOG.md` frontier at `HEAD`, `HANDOFFS.md` frontier one commit behind (the S333 push record, not a session), 0 undocumented sessions, 0 merges, `bin/check-ledger` and `bin/check-handoff` exit 0, `upstream/main` still `f34769f`, issues #95 and #93 and pull requests #94 and #92 with no reply, dashboard 72/100, `HANDOFFS.md` at 4 receipts at rest (the trim was not offered or run; the next Phase 0 offers it).

### 2026-10-16 · [BL-101] S333 -- push record: this session's 6 commits to the fork `origin`, his tick at the close-out picker ("Push to the fork origin")

`git push origin main`: `da20178..1ee4380` (the trim `8c41f6d`, the claim `e905d65`, the scripts `5f4e880`, the record `2ac9593`, his decisions `2a806d5`, the close-out `1ee4380`), read back with `git rev-list --left-right --count origin/main...HEAD` = `0 0` and `ls-remote` equal to `HEAD`. `pr2/candidate` (`a62bfec`) is on no remote. Nothing is sent to `KJ5HST/methodology`. The earlier push this session (`4ee7e06..da20178`, S332's three commits, ticked at the Phase 0 picker) is recorded in the claim entry.

### 2026-10-16 · [BL-101] S333 close-out -- the supersede check done (this entry resolves the claim `e905d65`, which stays `in progress` above): receipt complete, the fork's gate run saved

Deliverable: the check S332 left open, answered in `draft4-record.md` section 5 with `pr4-survive.py` and `pr4-oracle.sh`. Findings F1 (the text's reason for removing two of his tests is wrong) and F2 (the first-parent walk is not itemised) and his answers (restore the two tests; name the walk) are in the receipt and the entry below; neither is done. Gate: 18/18, 0 unmeasured, results `d7576eaf9b5b`, manifest `a690abd884d4`, clean `--no-local` clone of `2ac9593`, 1,428 s, saved in `docs/planning/pr-composition-evidence/s333-fork-gate-output.txt`. Scores: predecessor (S332) 8, self 8. 3C: no fork learning row (rows considered: #50, #108, #24). The `HANDOFFS.md` receipt is complete (`status: complete`); the next Phase 0 offers the HANDOFFS trim (4 receipts at rest). Not pushed at the time of this entry; he ticked the push to the fork `origin`.

### 2026-10-16 · [BL-101] S333 -- his decisions on the check's two findings, recorded (neither carried out)

At the close-out picker: **F1, restore the two dashboard tests** (`test_bare_dry_run_refuses_instead_of_writing`, `test_a_normal_run_still_writes`) on `pr2/candidate`; **F2, name the first-parent gate-history walk in one clause** in decision 2. Both change the text, so they are one later build session and a draft 10 (the restore moves the candidate's head from `a62bfec` and means `pr4-claims.sh` again). `draft4-record.md` section 5 carries his answers and the build's design point; one sentence about the thresholds is corrected there and in `pr4-survive.py` (`bbe0dc3` raises three, later commits raise those three again and two more). The text (draft 9) and the candidate are untouched. He also ticked the push of this session's commits to the fork `origin`.

### 2026-10-16 · [BL-101] S333 -- the check's record: `draft4-record.md` section 5 (do the maintainer's own lines survive the whole files?)

The answer, in the record's words: he has changed nothing since `c8b9ddd` (`f34769f` is an ancestor of it and still `upstream/main`); of the lines of his that the 32 commits remove or rewrite, every one is accounted for by a change the text names, two of them in part, except one change to his dashboard (the gate-history walk is first-parent, 2.21.0; F2) and the text's reason for removing two of his tests is wrong (F1: `test_bare_dry_run_refuses_instead_of_writing` and `test_a_normal_run_still_writes` pass on the candidate's code; the second has no counterpart for a copy at the project root). Section 4 item 2 now points at section 5. The pull request's text is NOT changed: both findings are his to settle, and the text is at 20,117 B against its 20,000 B budget. Nothing is sent.

### 2026-10-16 · [BL-101] S333 -- the supersede check's two scripts and their saved output (`pr4-survive.py`, `pr4-oracle.sh`)

`pr4-survive.py` lists every line of upstream's copies (`f34769f`) that the candidate (`a62bfec`) removes or rewrites, attributes it by `git blame` to its author, and assigns each of the maintainer's gone lines to a named reason by file and line range (exit 1 if one has none). `pr4-oracle.sh` runs upstream's dashboard, ratchet and budget-tool unit tests against the candidate's code in a scratch tree, with one printed fixture line changed in the dashboard file. Both read git objects only. Numbers: 1,152 lines removed (equals git's count), 487 his, 359 gone, 279 with the dashboard twin once, all assigned; 417 of 422 upstream unit tests do not fail on the candidate's code; 4 of 553 tests absent by name, the four the text names. Outputs: `pr4-survive-output.txt`, `pr4-oracle-output.txt`. Nothing is sent.

### 2026-10-16 · [BL-101] S333 claim (in progress) -- the supersede check: do the maintainer's changes to the dashboard and the trimmer survive the whole files PR4 sends

CHANGELOG: pending. Taken at his Phase 0 picker answers: "Run the supersede check (Recommended)", and for the side actions "Trim CHANGELOG.md first" and "Push the 3 local commits to the fork origin". Done first, at those ticks: the push `4ee7e06..da20178` (`d58a798`, `35e8f08`, `da20178`; read back `0 0`, `ls-remote` equal), then the trim `8c41f6d` (the tool's entry is directly above; `--cut 2026-10-15`, 195,479 B to 39,455 B, no `--force` needed, shard proof exit 0 in the tree and both checkers exit 0; the suite in a clean clone of `8c41f6d` is running from the scratchpad and its result goes in the close-out). Phase 0: `HEAD` `da20178` equal to `origin/main` after the push, both ledger frontiers at `HEAD`, 0 undocumented, 0 merges, no pending receipt, `upstream/main` still `f34769f`, issues #95 and #93 and pull requests #94 and #92 with no comment from anyone but him, dashboard 72/100. Scope: the check named at `docs/planning/pr-composition-evidence/draft4-record.md:70` (upstream's `f34769f` copy of the dashboard and the trimmer against the whole files `pr2/candidate` `a62bfec` sends): a saved script, its output and a record entry; read-only on the candidate; the pull request's text changes only if the check finds a loss, and then only after it is shown to him; nothing is sent to `KJ5HST/methodology`.

### 2026-10-16 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-10-15.md` (126 record(s), 195,479 B → 39,455 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **126** record(s) (2026-10-14 → 2026-10-15) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-10-15.md`](docs/archive/CHANGELOG-through-2026-10-15.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-10-15.md.verify.sh`](docs/archive/CHANGELOG-through-2026-10-15.md.verify.sh)
rather than trusting a digest printed here. Live file 195,479 B → 39,455 B (−79.8%).

### 2026-10-16 · [BL-101] S332 -- the S332 receipt amended to say what was done after its close-out (the push, the HANDOFFS trim and its fold) and what is next (the CHANGELOG trim)

Two sentences of the `HANDOFFS.md` S332 receipt: `active_task` no longer lists the push and both trims as undone (it names the push `55a35c2..36a466a` with its ledger-only record `4ee7e06`, and the trim `d58a798` with its fold, as done at his picker ticks), and `next_steps` item (4) now offers ONE trim at the next Phase 0, `CHANGELOG.md`, which stands at 194,642 B against a 196,608 B trigger (the HANDOFFS trim's two entries took it from 191,885 B), so the next claim crosses it. HANDOFFS holds 3 receipts at rest (S332, S331, S330). Nothing else in the receipt changed. Not pushed: this amendment, the trim and its fold are not ledger-only commits.

### 2026-10-16 · [ad hoc] S332 -- the HANDOFFS trim's pointer block folded into the archive index (the trim itself is the tool's entry below, commit `d58a798`, ticked at the S332 close-out picker)

The trim: `python3 starter-kit/methodology_trim.py --file HANDOFFS.md --cut 3 --force`, then `--write` (the dry run was not denied by the auto-mode classifier): S329's, S328's, S327's and S326's receipts to `docs/archive/HANDOFFS-through-2026-10-15-2.md`, 7 receipts to 3 (S332, S331, S330), 80,594 B to 35,427 B; the shard's own proof exit 0 before the commit and again after the fold, `bin/check-handoff` and `bin/check-ledger` exit 0 at each. The tool printed the two expected notices (`CUT_STRADDLES_DAY`, `SHARD_NAME_DISAMBIGUATED`) and `FRONTMATTER_FIELD_ABSENT` (this file's header declares no receipt count, on purpose). The fold, in its own commit as the index's rule says: the pointer block (three lines and a blank) left `HANDOFFS.md` (80,594 B to 35,427 B to 34,971 B) and one row joined `docs/HANDOFFS_ARCHIVE_INDEX.md` (`| 4 | 2026-10-15 → 2026-10-15 | HANDOFFS-through-2026-10-15-2.md | v1.8.0 |`). Not pushed: the trim and the fold are not ledger-only commits, so they wait for his tick.

### 2026-10-16 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-15-2.md` (4 record(s), 80,594 B → 35,427 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **4** record(s) (2026-10-15 → 2026-10-15) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-15-2.md`](docs/archive/HANDOFFS-through-2026-10-15-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-15-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-15-2.md.verify.sh)
rather than trusting a digest printed here. Live file 80,594 B → 35,427 B (−56.0%).

### 2026-10-16 · [BL-101] S332 -- push record: S332's 4 commits to the fork `origin`, his tick at the close-out picker ("Push S332's 4 commits to fork origin")

`git push origin main`: `55a35c2..36a466a` (the claim `c854572`, draft 8 `faffc98`, draft 9 with the record `d2cc1e9`, the close-out `36a466a`), read back with `git rev-list --left-right --count origin/main...HEAD` = `0 0`. `pr2/candidate` (`a62bfec`) is on no remote (`git ls-remote origin 'refs/heads/pr2/*'` lists none); nothing was sent to `KJ5HST/methodology`. The same picker ticked "Trim HANDOFFS to 3 receipts now" (the next entries) and chose "Run the missing check first" for the text (the next session). This entry is the ledger-only push record that his standing grant lets go to the fork unasked.

### 2026-10-16 · [BL-101] S332 close-out -- receipt complete (self 7, predecessor S331 scored 9), the fork's gate run saved

The `HANDOFFS.md` receipt is `status: complete` (9,096 B of 12,288; `bin/check-handoff` and `bin/check-ledger` exit 0). **Phase 3E, the repository's own gate run** in a clean `--no-local` clone of `d2cc1e9` (the last work commit; `layer-verify.sh`, `nohup ... &` and a done-file, about 24 minutes at a load of about 4): `quality_ratchet: 18/18 pass · 0 fail · 0 unmeasured · results d7576eaf9b5b · manifest a690abd884d4` (the ids S329 to S331 cited), the layout scanner 18 files and 0 sites, 5 of 172 shard proofs exit 1, **the same five August ones as S329's, S330's and S331's runs (`diff` of the sets: identical)**; saved as `docs/planning/pr-composition-evidence/s332-fork-gate-output.txt`. Phase 3C appended no fork learning row (D3 not triggered; rows considered #20, #47, #30); the stop rule for reads went to memory. **Sizes at close:** `CHANGELOG.md` was 190,509 B before this entry (`methodology_trim.py --file CHANGELOG.md --check`: "trigger does not fire", trigger 196,608 B), so the next session's claim will probably cross it; HANDOFFS holds 7 receipts at rest, above his decided 3. Not pushed: this session's commits stay local until his tick; `pr2/candidate` (`a62bfec`) is on no remote and was not touched. Draft 9 has no read.

### 2026-10-16 · [BL-101] S332 -- PR4's text, draft 9, after the fourth reader's report on draft 8 (5 of 10 again), and the record brought to draft 9

Ratings across the four reads are 5, 5, 6 and 5 of 10, so they no longer inform; the specific failures each reader quotes still do, and each was checked against its source before it was used. **Fixed (errors or ambiguities of mine):** "I asked for it" (now "I wanted it"); which hook the ledger-hook gap means (the ledger pre-commit hook of `SAFEGUARDS.md`, in an earlier copy; the migration reports such a hook and leaves it); whose remedy rewrote 26 files; the risk rows and the removed tests unlettered (now (d) and (e)); "a backlog ... the trimmer can archive" (the trimmer archives ledgers: now "a ledger or a backlog"); the limits unsourced (now "the limits I measured for an agent's file-read tool"); "that file's own rule"; the cut had lost "if you drop the ten commits those references stay"; `pr4-` read as a pull request number; `c8b9ddd` and `e7b389f` named as commits on the fork; `--tier 1` used before it is defined; "the master" (now `tools/layout_resolver.py`); "the bin/sync on main" (now "upstream's"); a ledger too small to migrate; the 280 tests against `bin/tests.sh`; the 23 framework files per moved project lost in the cut; `bin/sync --layout`'s default stated (`bin/sync --help`: `auto` keeps the layout a project has, `legacy` for an empty one). **Paid for** by dropping the `trimmer-unit-tests` floor comparison, the layout-literals evidence row, the 56-line count and its grep, the release-version sentence and small clauses; the 56-line command is gone, and so is the number. The body is 20,117 B against the 20,000 B budget (0.6% over; stated, not shaved). `pr4-body-check.py`: exit 0, no banned token, 34 paths. **Not acted on because only he can answer:** a recommendation per decision, the reason for (b), the itemised dashboard changes, and **one check I did not do and think matters most**: whether the maintainer's own changes to the dashboard and the trimmer since `c8b9ddd` survive the whole files sent (`draft4-record.md` §3). **Draft 9 has had no read.** Nothing is sent.

### 2026-10-16 · [BL-101] S332 -- PR4's text, draft 8, FROZEN for a fourth read, cut to the byte budget (25,959 B to 19,990 B)

Draft 7 cut by 5,969 B (23%) to the budget stated in the claim (20,000 B or less). **What was cut:** the 11-row commit table (each commit's message describes it; the groups are now a reading order and one sentence), the 12-projects paragraph (two sentences), the conflict paragraph (one sentence), the evidence row for frozen proofs (a population of one, which the third reader called weak), the unit-suite sentence, timing detail, and wording throughout; the offer in decision 1 to rebuild any commit separately (not ticked at his picker). **What was kept because the cut text alone carried it:** the rewrite of your Test 15 (a change to one of the maintainer's existing tests), the change to the first paragraph of the runner for every project (now in decision 1's costs), the 3600 s gate timeouts (in the migration bullet), `NEW_LAYOUT` and `--layout` (in "Paths"), the unclosed-fence example, the 56-line residue and its command (in decision 4). **An error of mine caught on the way:** while compressing I wrote that `bin/status` takes `--layout`; `bin/status --help` shows it does not (it reads each project's layout and prints a `layout:` line); draft 7's table had it right; fixed before the freeze. The decisions are 7,283 B before the marker sentence (draft 7: 8,102 B). `pr4-body-check.py`: exit 0, no banned token, 33 paths; the figures touched in the cuts re-checked against `pr4-supersede-output.txt` and `layer7-probe-output.txt` (362.6 s for the 280 tests). **Draft 8 has had no read until the record says so.** Nothing is sent.

### 2026-10-16 · [BL-101] S332 claim (in progress) -- cut PR4's text (draft 8) to a byte budget, take out the unticked rebuild offer, then one more fresh read of the frozen result

CHANGELOG: pending. A new deliverable after S331's close-out and push, taken at his picker answers: "Cut it, then one more read (Recommended)" and, for the confirmations, only "Push S331's 9 commits" (done: `ec021d4..34366cb`, then the push record `55a35c2`, both read back `0 0`); "Keep decision 1's offer to rebuild a commit" was NOT ticked, so that sentence comes out. **Byte budget, stated before the edit (his lesson from S331's rewrite: the text grew 40% because nothing paid for each addition):** draft 7 is 25,959 B; the target is 20,000 B or less, paid for by the readers' cut list (the commit table, the 12-projects paragraph, the conflict paragraph), the resolver and migration bullets tightened, and the rebuild offer; nothing is added except one sentence that keeps a disclosure the table alone carried (the rewrite of your Test 15). The decisions (draft 7: 8,102 B) stay self-contained. Phase 0 re-check: `HEAD` `55a35c2` equals `origin/main`, both ledger frontiers at the last session, checkers exit 0, `upstream/main` still `f34769f`, `pr2/candidate` `a62bfec`, PR #94, PR #92 and issues #93 and #95 with no comment from anyone but him, dashboard 72/100; `CHANGELOG.md` is 184,935 B (trigger 196,608 B) and HANDOFFS holds 6 receipts (71,481 B), both trims offered at the next Phase 0 and not ticked. Scope: `docs/planning/upstream-pr-body.md` only as the text, its record, and one fresh read of the frozen draft with a brief that names the maintainer's vocabulary; no change to the candidate; nothing is sent to `KJ5HST/methodology`.

### 2026-10-16 · [BL-101] S331 -- push record: S331's 9 commits to the fork `origin`, his tick at the close-out picker ("Push S331's 9 commits to fork origin")

`git push origin main`: `ec021d4..34366cb` (the S330 receipt amendment `afd8551`, the claim `0ac8621`, the two scripts `e3a0b90`, drafts 4, 5 and 6 `d5bb53b`, `9becf89`, `dfc31ab`, the moved-project script `c8b2431`, draft 7 `93245dc`, the close-out `34366cb`), read back with `git rev-list --left-right --count origin/main...HEAD` = `0 0`. `pr2/candidate` (`a62bfec`) is on no remote (`git ls-remote origin 'refs/heads/pr2/*'` lists none); nothing was sent to `KJ5HST/methodology`. The same picker did NOT tick "Keep decision 1's offer to rebuild a commit", so that sentence comes out of the text (next session's work). This entry is the ledger-only push record that his standing grant lets go to the fork unasked.

### 2026-10-16 · [BL-101] S331 close-out -- receipt complete (self 7, predecessor S330 scored 8), the fork's gate run saved

The `HANDOFFS.md` receipt is `status: complete` (9,497 B of 12,288; `bin/check-handoff` and `bin/check-ledger` exit 0). **Phase 3E, the repository's own gate run** in a clean `--no-local` clone of `93245dc` (the last work commit; `layer-verify.sh`, `nohup ... &` and a done-file): `quality_ratchet: 18/18 pass · 0 fail · 0 unmeasured · results d7576eaf9b5b · manifest a690abd884d4` (the ids S329 and S330 cited), the layout scanner 18 files and 0 sites, 5 of 172 shard proofs exit 1, **the same five August ones as S329's and S330's runs (`diff` of the sets: identical)**; saved as `docs/planning/pr-composition-evidence/s331-fork-gate-output.txt`. Phase 3C appended no fork learning row (D3 not triggered; rows considered #20, #30, #47); two lessons went to memory (a cold reader's brief must name the audience's vocabulary; set a byte budget before a clarity rewrite). **Sizes at close:** `CHANGELOG.md` was 182,637 B before this session's close-out entries, about 14 KB under the 196,608 B trim trigger, and this session added about 16 KB: the next session will probably cross it. HANDOFFS holds 6 receipts at rest, above his decided 3. Not pushed: this session's commits stay local until his tick; `pr2/candidate` (`a62bfec`) is on no remote and was not touched. Draft 7 has no read.

### 2026-10-16 · [BL-101] S331 -- PR4's text, draft 7, after the third reader's report (6 of 10), and the record of drafts 4 to 7 (`draft4-record.md`)

The third reader was told the maintainer knows his own framework's vocabulary (the first two were not, so they over-counted); its findings were claims, checked before any was acted on. **Mine, found by the check and fixed:** the Test 15 rewrite (`4c0bdde`) was listed as "not about the directory" and is caused by it (`bin/status` prints a `layout:` line naming the project; the old assertion counted 31 for 30 files); "at least 56 added lines remain" is unsupportable for a pattern with false positives (now "matches 56 added lines, some may be legitimate"); "no issue on your repository asks for it" became "I found no issue ..." (a fuzzy `gh` search; none of the titles concern a `methodology/` directory). **New content, each read from a source:** the motivation (his request of 2026-10-06, `methodology-subdirectory-plan.md:9`); the limits behind the risk rows (an agent's file read: cut short past about 25,000 tokens counted at 2.27 B/token, refused past 256 KiB); what "cannot safely rewrite" means (`Unsafe`: an unclosed code fence in a ledger); `PROJECT_LEARNINGS.md` (named in upstream's own `BOOTSTRAP.md`); `bbe0dc3` alone still conflicts with #94 in 6 regions in 2 files (`git merge-tree`); all 4 trimmer commits in upstream's history carry `TRIM_VERSION`; baseline times beside "the same time"; the way back from a migration; how the 11 copies of the layout code are changed. **Structure:** decision 1 carries the size, the cost to projects, the known gap that bears on it and the "no" branch, with an offer to rebuild any commit separately (a commitment of his, flagged in the record); the dashboard detail is in decision 2. The body is 25,959 B (draft 3: 18,479 B): each clarification added words. `pr4-body-check.py`: exit 0, no banned token, 38 paths. **Draft 7 has had no read.** The record, `draft4-record.md`, lists each reader's rating and findings with what was done and what was not, my own errors in the drafts, and what is open for him. Nothing is sent.

