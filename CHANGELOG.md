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

