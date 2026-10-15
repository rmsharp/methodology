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

---

## 2026-09

## 2026-10

### 2026-10-15 · [BL-101] S323 claim (in progress) -- D6's small commit on `pr2/candidate`: the three unmeasured-gate hunks

CHANGELOG: pending. Operator said `go`; at the Phase 0 picker he took D6's small commit (S322's recommended next step) and skipped the HANDOFFS trim (his BL-108 rule is "trim above 3", the count is 3). Phase 0: `HEAD` `22a89d2` equals `origin/main` (`0 0`), CHANGELOG frontier `HEAD` (0 undocumented commits, 0 merges), no pending receipt, `upstream/main` still `f34769f` (fork 1,974 ahead, 0 behind), `pr2/candidate` still `ab35e96` (19 commits); #94 and #92 have 0 comments, #93's one comment is his own (2026-10-05); dashboard 72/100, one high flag (`docs/planning/BACKLOG.md`, 60,492 B against 56,750 B); the local `.quality-gates-results.json` is stale (2026-10-10), so the receipt's `d7576eaf9b5b` is checked only against S322's clean-clone ledger entry, not re-run. **This session's one deliverable is D6's commit only:** the runner's 3E sentence, `starter-kit/HANDOFFS.md`'s paragraph and `HOW_TO_USE.md`'s 3E bullet (plan §7 D6, answered (a), not re-asked), derived first and read-only, one commit of 3 files on the local ref `pr2/candidate`, un-pushed. Not this session: the scrub, PR3 to PR5, BL-108, the `BACKLOG.md` size flag. Nothing is sent upstream. Closed by a NEW close-out entry (a committed entry is never rewritten). Model: Claude Sonnet 5.5.

### 2026-10-15 · [ad hoc] S322 -- the real `CHANGELOG.md` trim (`1f4f03b`) at his go-ahead, the gate run on it, and the fork push

**The trim:** 167 records (2026-10-12 to 2026-10-14) to `docs/archive/CHANGELOG-through-2026-10-14.md`, 246,020 B to 98,501 B, shard proof exit 0, `bin/check-ledger` and `bin/check-handoff` exit 0; it ran with `--force` (SRF-RED: plan 3.3 says do not archive again, and the level resets, not the rate) because his picker ticked it against my recommendation; the headroom under the 262,144 B refusal is now about 163,600 B and the file grows 7 to 10 KB a session. `check-ledger --all` reads the same one finding as before (an old shard's entry with two source tags). **The gate run** on `1f4f03b` in a clean `--no-local` clone (3 receipts, load 2.5, 1,124 s): 18/18, 0 unmeasured, results `d7576eaf9b5b`, manifest `a690abd884d4`, equal to every earlier run today. **The push,** his tick: `git push origin "<the sha of this recording commit>:refs/heads/main"`, a fast-forward from `2daa9f8` of 11 commits (the S322 work, the close-out, his answers, the trim and this record), read back with `git ls-remote origin refs/heads/main` (equal to local `HEAD`) and `git rev-list --left-right --count origin/main...HEAD` (`0 0`); the fork only, nothing sent to `KJ5HST/methodology`; `pr2/candidate` stays a local ref. This commit changes only `CHANGELOG.md` and is pushed with the rest under his standing grant for push records. Model: Claude Sonnet 5.5.

### 2026-10-15 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-10-14.md` (167 record(s), 246,020 B → 98,501 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **167** record(s) (2026-10-12 → 2026-10-14) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-10-14.md`](docs/archive/CHANGELOG-through-2026-10-14.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-10-14.md.verify.sh`](docs/archive/CHANGELOG-through-2026-10-14.md.verify.sh)
rather than trusting a digest printed here. Live file 246,020 B → 98,501 B (−60.0%).

### 2026-10-15 · [BL-108] S322 -- his close-out answers: BL-108 decided (trim above 3, not built), BL-112 added, the receipt's mistake count corrected

His picker ticked all three go-aheads and chose option (b) for BL-108. **BL-108:** the HANDOFFS rule becomes "keep 2, trim at 4 with `--cut 2`", recorded in the row and its detail; the rule's edit, `RETENTION_FLOOR`, Test 34 and the A1 fit are for a later session. **BL-112 (new):** `bin/migrate-layout`'s docstring lists exits 0 to 3 and `main` returns 4 (`:26` against `:1311`), with its detail; not started. **The S322 receipt:** its mistake (5) read "one `echo ====`" and is now "two" (same length: the receipt stays 12,272 B against 12,288 B). The push and the real `CHANGELOG.md` trim, his other two ticks, follow in their own entries. Model: Claude Sonnet 5.5.

### 2026-10-15 · [BL-101] S322 close-out -- PR2's last layer built on pr2/candidate (ab35e96): the HANDOFFS receipt complete, the claim closed by a new entry

Closes the S322 claim entry (`CHANGELOG: pending`; a committed entry is never rewritten). **The deliverable:** `bin/migrate-layout` and its suite, the tenth and last Part 2 layer: `pr2/candidate` `18cda0f` to `ab35e96`, two commits, 6 files, +4,483 / -2, three of them the fork tip's bytes whole; the candidate is 19 commits, 46 files, +19,854 / -1,145 over `upstream/main`; clean-clone ratchet 18/18, 0 unmeasured, shell suite 302 / 0 / 0, the tool's 280 tests OK; the paired gate reads a red command-level suite as 280 pass and 1 fail from one run; over the 12 adopters the migration columns equal the fork tip's and the candidate's `bin/sync` needs `--force` for 9 of 12 (PR3's first row). **The gate run on the last work commit `8af565b`** (clean clone, 1,130 s): 18/18, results `d7576eaf9b5b`, manifest `a690abd884d4`, equal to the Phase 0 run and to S321's. The receipt is complete (`self_score` 8, `predecessor_score` 9); no fork learning row appended (rows considered: #55, #64, #16); `CHANGELOG.md` stands at 243,789 B before this entry, `BACKLOG.md` at 60,046 B. Nothing sent to `KJ5HST/methodology`; the 8 commits since `origin/main` (`2daa9f8`) are unpushed. Next: D6's small commit, then the scrub, then PR3. Model: Claude Sonnet 5.5.

### 2026-10-15 · [BL-101] S322 -- the BL-101 row and its detail record the last layer (`ab35e96`); next D6's small commit, then the scrub

`docs/planning/BACKLOG.md` (+80 B) and `BACKLOG-DETAIL.md`: all ten Part 2 layers are built; PR3's first row is the candidate's `bin/sync` needing `--force` for 9 of 12 adopters. Model: Claude Sonnet 5.5.

### 2026-10-15 · [BL-101] S322 -- PR2's last layer, `bin/migrate-layout`, built on `pr2/candidate` (`18cda0f` to `ab35e96`): the measurements, the 12-adopter comparison, the record, the plan's status line

The local ref moved by `git fetch <scratch clone> '+refs/heads/pr2/candidate:refs/heads/pr2/candidate'` and was read back equal (the ref, the clone's HEAD and the verified commit are one sha); two commits, 6 files, +4,483 / -2, three of the files the fork tip's bytes whole; the candidate is 19 commits over `upstream/main` (`f34769f`). **Over the 12 adopters, the candidate's tree against the fork tip's:** the migration columns equal in all twelve (24 of 27 columns), and the candidate's `bin/sync` needs `--force` for 9 of 12 where the fork's does not (the adopters hold earlier fork versions: PR3's first row). #94 still 3 files and 15 regions, #92 clean. Nothing sent to `KJ5HST/methodology`. Model: Claude Sonnet 5.5.

### 2026-10-15 · [BL-101] S322 -- the last layer's run outputs, 1 of 2: the suites, the clean-clone ratchet and the mutants

The shell suite on the tool's commit alone 301 / 0 / 0 (305 s); on the suite stage 302 / 0 / 0 (341 s) and the whole migration suite 280 OK (364.5 s, load 85 at launch); the layer's last commit in a clean `--no-local` clone: ratchet 18/18, 0 unmeasured, results `23481eb88ba1`, manifest `66cce597ef4a`, scanner 15 files and 0 sites; mutants L1 to L4 and W1 killed, G1 shows the paired gate reading a red suite as 280 pass and 1 fail from one run. Outputs only. Model: Claude Sonnet 5.5.

### 2026-10-15 · [BL-101] S322 -- the last layer's scripts (the builder re-based, the mutants, the measure script, the adopters' comparison)

`layer7b-build.py` is the S319 draft with one change in code, the `COPIES` text (the checkers' layer appended two entries); `layer7b-mutate.py` aims mutants at what the layer adds and runs the real two gates over a red suite; `layer7b-measure.sh` prints the other measurements; `layer7b-adopters-compare.py` compares two runs of `migrate-12-adopters.py`. Scripts only: their outputs and the record follow. Model: Claude Sonnet 5.5.

### 2026-10-15 · [BL-101] S322 claim (in progress) -- PR2 Part 2's last layer, `bin/migrate-layout`, on `pr2/candidate`

CHANGELOG: pending. Operator said `go`, picked `bin/migrate-layout` at the Phase 0 picker (S321's recommended next step) and ticked all four go-aheads (done and read back in the entry below; the gate re-run read 18/18). Phase 0: CHANGELOG frontier `2daa9f8` (HEAD at the time), 0 undocumented commits, 0 merges, no pending receipt, `bin/check-ledger` and `bin/check-handoff` exit 0 (read bare); `upstream/main` still `f34769f`; #94 and #92 have 0 comments and 0 reviews, #93's one comment is his own (2026-10-05); dashboard 72/100, one high flag (`docs/planning/BACKLOG.md`, 60,014 B against 56,750 B). **This session's one deliverable is the `bin/migrate-layout` layer only:** the tool and its suite on the local ref `pr2/candidate` (`18cda0f`), derived first and read-only (the builder's `COPIES`, the paired gate over one command string, `timeout_seconds`, the file count and commit split, cap 5), built in a scratch clone as checkpoint commits, un-pushed. Not this session: D6's unmeasured-gate commit, the scrub, the `CHANGELOG.md` trim (his word), PR3 to PR5. Nothing is sent upstream. Closed by a NEW close-out entry (a committed entry is never rewritten). Model: Claude Sonnet 5.5.

### 2026-10-15 · [ad hoc] S322 -- the Phase 0 go-aheads: the fork push (`20d5e94..2daa9f8`), the gate re-run, the CHANGELOG dry run, the HANDOFFS trim (`65f93e6`) and its shard pointer folded into the archive index

His answers at the S322 Phase 0 picker ticked all four go-aheads and added a question ("why does HANDOFFS trim keep coming up"), answered in the report: it is BL-108, which he raised at S313, not started. **The push:** `git push origin 2daa9f8...:refs/heads/main`, a fast-forward of 1 commit, read back with `git ls-remote origin refs/heads/main` (equal) and `git rev-list --left-right --count origin/main...2daa9f8` (`0 0`); the fork only. **The gate re-run:** a clean `--no-local` clone of `2daa9f8` (4 receipts), launched as `nohup`, 1,135 s, load 2.4 at launch: 18/18 pass, 0 fail, 0 unmeasured, results `d7576eaf9b5b`, manifest `a690abd884d4`, equal to S321's citation. **The `CHANGELOG.md` dry run, nothing written:** `--check` exits 1 (the trigger fires, 237,511 B against 196,608 B); alone it exits 2, refused SRF-RED (1.3984 against `21cf425`; plan §3.3: "do not archive again"); with `--force` and no `--write` it would archive 161 of 215 records to `docs/archive/CHANGELOG-through-2026-10-14.md`, 237,511 B to 97,696 B. The real trim stays his word. **The trim** (`65f93e6`, the tool's entry below): S319's and S318's receipts to `HANDOFFS-through-2026-10-14-5.md` (the shard S321 guessed), 4 receipts to 2, 50,752 B to 28,664 B, shard proof exit 0, `bin/check-handoff` and `bin/check-ledger` exit 0. **The fold,** this commit: the trimmer's pointer block out of `HANDOFFS.md`, one row into `docs/HANDOFFS_ARCHIVE_INDEX.md`. Nothing sent to `KJ5HST/methodology`. Model: Claude Sonnet 5.5.

### 2026-10-15 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-14-5.md` (2 record(s), 50,752 B → 28,664 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-10-14 → 2026-10-14) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-14-5.md`](docs/archive/HANDOFFS-through-2026-10-14-5.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-14-5.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-14-5.md.verify.sh)
rather than trusting a digest printed here. Live file 50,752 B → 28,664 B (−43.5%).

### 2026-10-14 · [BL-101] S321 -- D6 answered (a); backlog rows BL-110 and BL-111 added at his close-out go-ahead

His answers to the S321 close-out picker. **D6 (plan §7), the unmeasured-gate prose: (a), his recommended option, a small commit after `bin/migrate-layout` carrying the 3 hunks (+7 / -4) with the pull request's text stating that the lint stays on the fork:** recorded in the plan (§4's seam and §7), not built; do not re-ask. **BL-110** (no check reads a distributed document's path-spelled references or its layout prose: the 26 prose-layer hunks that survived the mutants) and **BL-111** (S320's three added tests are absent from the fork's checker suite), each written from what is known, not started, with a detail entry. Not pushed: the push he authorized named `3322639`. Model: Claude Sonnet 5.5.

### 2026-10-14 · [ad hoc] S321 -- the fork push `8ee1b15..3322639` on his close-out go-ahead, read back; this recording commit is pushed with it under the standing grant

His answer to the S321 close-out picker ticked the push and two backlog rows and chose D6 (a). **The push, first:** `git push origin "3322639...:refs/heads/main"`, a fast-forward of 7 commits (the claim, five evidence and plan commits, the close-out), read back with `git ls-remote origin refs/heads/main` (equal to local `HEAD`) and `git rev-list --left-right --count origin/main...HEAD` (`0 0`); the fork only, nothing sent to `KJ5HST/methodology`; `pr2/candidate` stays a local ref. This commit changes only `CHANGELOG.md` and is pushed under his standing grant for push records, so no further record is owed. D6's answer and the two backlog rows follow in their own commits and are not pushed. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S321 close-out -- PR2's prose layer built on pr2/candidate (18cda0f): the HANDOFFS receipt complete, the claim closed by a new entry

**Resolves the claim's `CHANGELOG: pending`** (a committed entry is never rewritten, so this entry closes it). The one deliverable is done: PR2's prose layer on the local ref `pr2/candidate`, `505541c` to **`18cda0f`** (five commits, 19 files, +95 / -61: the layout hunks only of the 17 differing framework documents, 54 of 62 hunks, 8 left out as not layout; Test 10's `--layout both` block), verified in a clean `--no-local` clone (ratchet 16/16, 0 unmeasured, results `7a4736a489ee`), probed against the migration tool (280 tests pass on the layer, 10 of 23 fail at the parent), mutated (28 of 35 reference hunks killed; the 19 layout-text hunks are read by no check). Recorded in `layer6c-record.md`; nothing is sent to `KJ5HST/methodology`.
**Close-out:** 3A scored S320's handoff 9 (its figures exact, its NOT CHECKED labels each answered here, nothing wrong); 3B scored this session 8; 3C appended no fork learning row (D3 not triggered, no retirement owed; rows considered #15, #18, #68); 3D the receipt, complete, 12,247 B against its 12,288 B record budget; 3E the gate run in a clean clone of `764d805` (1,133 s): **18/18 pass, 0 fail, 0 unmeasured, results `d7576eaf9b5b`, manifest `a690abd884d4`**, equal to the Phase 0 run and to S320's citation. **For the next Phase 0:** HANDOFFS holds 4 receipts (S321, S320, S319, S318), so one trim is due (two records, S319 and S318; shard a guess `HANDOFFS-through-2026-10-14-5.md`) with a gate re-run before it or after the claim; `CHANGELOG.md` is 233,426 B before this entry against its 196,608 B trigger and the 262,144 B hard refusal (this session added 6,574 B in seven entries), so the refusal is two to three sessions away and its real trim is his word; `origin/main` is `8ee1b15` and the count unpushed is computed at Phase 0; plan D6 (where the unmeasured-gate prose goes) is asked at the close-out picker. **Mistakes, in full** (receipt, `what_was_done`): a typo redirect that created `/tmp/null`, a saved output overwritten after the ref moved, a figure false on the candidate cut from the tip's text (caught before the commit), a record sentence written before the run it described, and the silent stretches. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S321 -- the plan, the BL-101 row and its detail record the prose layer; decision D6 (the unmeasured-gate prose) added; next `bin/migrate-layout`

The plan's status line reads "first nine layers" and names `18cda0f`; its §4 seam says the prose layer left the unmeasured-gate sentences out as not layout; §7 gains D6 (three options, (a) a small commit after `bin/migrate-layout` recommended; asked at the S321 close-out picker, unanswered). The BL-101 row and its detail say the same and that the migration tool's 280 tests pass on the layer. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S321 -- the prose layer's evidence, 3 of 3: the end-to-end mutant, the migration-suite probe and the layer's record

`layer6c-record.md` (the answer first, what was measured, the decisions taken, what is not shown, the next layer and one decision for him: the unmeasured-gate prose). The end-to-end mutant: with one link put back, Test 10's first block passes and the new block fails, 300 passed, 1 failed. The probe: the migration tool's suite at the parent, 10 of 23 failed; at the layer, **280 tests OK in 329 s**. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S321 -- the prose layer's evidence, 2 of 3: the verification and mutation outputs

The clean-clone verification of `18cda0f` (8 min 26 s: 16/16, 0 unmeasured, results `7a4736a489ee`, manifest `682c7e6d2333`), the shell suite on the tests stage (301 passed, 0 failed, 0 skipped) and on `c8d4375` alone (300 / 0 / 0), and the mutants over the 54 layout hunks: **reference 28 killed, 7 survived (six are `docs/methodology/` paths spelled in a code span, one is a link to a project-owned file); layout text 0 of 19 killed**, the control green and the clone clean afterwards. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S321 -- the prose layer's evidence, 1 of 3: the probe script and the report, reference-check and measure outputs

`layer6c-probe.sh` and three saved outputs. The report: 23 documents, 17 differ, 62 hunks, 54 layout and 8 not. The reference check: 35 `reference` hunks, 32 equal to the old text after link syntax and paths are normalised, 3 name the file the link target named. The measure: dangling links in the `methodology/` layout 35, 31, 8, 2, 0, 0 after the parent and each commit; #94 conflicts in the same 15 regions at the parent and at the layer, #92 clean; no backlog code, session number or plan section in the 95 added lines or the five messages. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S321 -- PR2 Part 2's prose layer built on `pr2/candidate` (`505541c` to `18cda0f`): the layout hunks of the 17 differing framework documents, five commits, verified in a clean clone; the builder and three scripts

The local ref moved by a forced fetch from a scratch clone (read back equal); five commits `c8d4375`, `04918ce`, `23e6e66`, `0248ebf` (documents, 5/5/5/2 files) and `18cda0f` (Test 10's `bin/check-links --layout both` block, `tests-sh-passed` 300 to 301); 19 files, +95 / -61; the candidate is 17 commits, 44 files, +15,373 / -1,145 against `upstream/main`. **Layout hunks only:** of the tip's 62 differing hunks (+102 / -67) 54 (+86 / -60) are layout and 8 (+16 / -7) are not and stay out (the unmeasured-gate clause in 3 files, issue #75's rule, a model-tag sentence, a session number): S320's open question, answered. **Verified:** clean-clone `layer-verify.sh` on `18cda0f`, ratchet **16/16, 0 unmeasured, results `7a4736a489ee`, manifest `682c7e6d2333`**, scanner 14 files 0 sites; shell suite 301/0/0 on the final tree and 300/0/0 on `c8d4375` alone; the migration tool's suite on the layer **280 OK (329 s)** against 10 of 23 failing at the parent; mutants: 28 of 35 reference hunks killed, 0 of 19 layout-text hunks (no check reads them); legacy relative links 116 to 80. Nothing sent. This commit: `layer6c-build.py`, `-reference-check.py`, `-measure.sh`, `-mutate.py`; the rest of the evidence follows. Model: Claude Sonnet 5.5.

### 2026-10-14 · [ad hoc] S321 -- the Phase 0 gate re-run result (closes the claim's "launched")

`quality_ratchet.py --run` in a clean `--no-local` clone of `8ee1b15`, launched 02:40:10Z, finished 03:05:59Z (1,549 s, exit 0, load average 4 to 54 from another project's browser tests): **18/18 pass, 0 fail, 0 unmeasured, results `d7576eaf9b5b`, manifest `a690abd884d4`**, equal to S320's citation, so the Phase 0 check of the newest receipt's `quality_ratchet:` line is discharged; `pgrep` after the done-file found no gate process. The push `615a5c7..8ee1b15` was read back in the claim entry. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S321 claim (in progress) -- PR2 Part 2's prose layer (the framework documents' layout text) on `pr2/candidate`

CHANGELOG: pending. Operator said `go`, picked the prose layer at the Phase 0 picker (S320's recommended next step) and ticked two go-aheads: the push and the gate re-run; he did not tick the HANDOFFS trim. **The push, done and read back:** `git push origin "8ee1b15:refs/heads/main"`, a fast-forward `615a5c7..8ee1b15` (9 commits), `ls-remote` equal and `rev-list --left-right --count origin/main...HEAD` `0 0`; the fork only, nothing sent to `KJ5HST/methodology`. **The gate re-run:** launched `nohup ... &` with a done-file at 02:40:10Z in a clean `--no-local` clone of `8ee1b15` (scratchpad `s321-gate`, load average 4.38 at launch); its result goes in a NEW entry, not here. Phase 0: CHANGELOG and HANDOFFS frontiers both `8ee1b15`, 0 undocumented commits, 0 merges, no pending receipt; `bin/check-ledger` and `bin/check-handoff` exit 0 (read bare); `upstream/main` still `f34769f`; #94 and #92 have 0 comments and 0 reviews, #93's one comment is his own (2026-10-05), no new PR or issue from anyone else. Dashboard 72/100, one high flag (`docs/planning/BACKLOG.md`, 58,982 B against 56,750 B); `CHANGELOG.md --check` fires (226,852 B before this entry against 196,608 B; the hard refusal is 262,144 B) and the real trim is not taken (his word). **This session's one deliverable is the prose layer only:** the framework documents' layout text on the local ref `pr2/candidate` (`505541c`), derived first and read-only (which of the probe's 17 differing documents are layout, Test 10's `--layout both` block, the layer's tests), built in a scratch clone as checkpoint commits of at most 5 files, un-pushed. Not this session: `bin/migrate-layout`, the scrub, the `CHANGELOG.md` trim, PR3 to PR5. Nothing is sent upstream. Closed by a NEW close-out entry (a committed entry is never rewritten). Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S320 close-out -- PR2's checkers' layer built on pr2/candidate (505541c): the HANDOFFS receipt complete, the claim closed by a new entry

**Resolves the claim's `CHANGELOG: pending`** (a committed entry is never rewritten, so this entry closes it). The one deliverable is done: PR2's checkers' layer on the local ref `pr2/candidate`, `0aa1897` to **`505541c`** (two commits, 7 files, +364 / -26; `bin/check-ledger` is the tip's blob whole and `bin/check-handoff` is upstream's plus seven edits cut from the tip's text; the 11-test suite, its gate and the scanner's scope), verified in a clean `--no-local` clone (ratchet 16/16, 0 unmeasured, results `e960a10e187f`), contrasted (6 of 11 new tests fail on the parent's tools), mutated in two rounds (the second round's three survivors became tests; 22 of 22 killed), run over the fork's own ledgers in both layouts (output and exit equal), and probed against the tool it exists for (the migration tool's 280 tests pass once the prose is in). Recorded in `layer6b-record.md`; nothing is sent to `KJ5HST/methodology`.
**Close-out:** 3A scored S319's handoff 9 (its figures exact, its NOT CHECKED labels each measured here; it said the layer deletes the pin test, which would have dropped a floor, so it was replaced); 3B scored this session 8; 3C appended no fork learning row (D3 not triggered, no retirement owed; rows considered #16, #70, #107); 3D the receipt, complete, 11,092 B against its 12,288 B record budget; 3E the gate run in a clean clone of `fc6c174` (1,282 s): **18/18 pass, 0 fail, 0 unmeasured, results `d7576eaf9b5b`, manifest `a690abd884d4`**, equal to the Phase 0 run and to S319's citation. **For the next Phase 0:** HANDOFFS holds 3 receipts (S320, S319, S318), so one trim is due (one record, S318; shard a guess `HANDOFFS-through-2026-10-14-5.md`) with a gate re-run before it or after the claim; `CHANGELOG.md` is 224,284 B before this entry against its 196,608 B trigger and the 262,144 B hard refusal (this session added 12,240 B in eight entries), so its real trim is nearer to due than at S319: his word; `origin/main` is `615a5c7` and the count unpushed is computed at Phase 0. **Mistakes, in full** (receipt, `what_was_done`): the first full verification ran before the second mutation round and was superseded, the first real-corpus run compared a pending stub, a stray `cat > /tmp/...` line swallowed one script (nothing ran), a claim-side numbering ("eighth layer") that S319's records number differently, and the silent stretches. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S320 -- the plan, the BL-101 row and its detail record the checkers' layer; next the prose, then bin/migrate-layout

The plan, the BL-101 row and its detail record the checkers' layer. `docs/planning/upstream-pr-composition-plan.md` status line: Part 2's first **eight** layers are built (S320: `505541c`, the layout reading of the two checkers, two commits), the later layers are the prose and then `bin/migrate-layout`, which passes its 280 tests once the prose is in (`layer6b-probe-output.txt`). The BL-101 row in `docs/planning/BACKLOG.md` (58,982 B, 5 B under what S319 left; still over its 56,750 B budget) reads Part 1, layers 1 to 6 and the checkers' layer done, next the prose then `bin/migrate-layout`; the detail in `docs/planning/BACKLOG-DETAIL.md` gains the S320 sentence with the same figures the record carries, and says the three tests added to the candidate's suite are absent from the fork's own (his call). Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S320 -- the checkers' layer's real-corpus check, the migration-suite probe (280 pass with the prose) and the layer's record

The checkers' layer's real-corpus and probe outputs, and its record. **`layer6b-realtree-output.txt`:** this fork's own ledgers at `fc94978` (`CHANGELOG.md` 214,849 B with 24 shards, `HANDOFFS.md` 27,411 B with two receipts) placed legacy, under `methodology/`, and under `methodology/` with the shards left in `docs/archive/`, and read by the parent's tools and the layer's: **output and exit code are equal old-to-new on the legacy tree and equal across the three placements** (paths normalised) for `check-ledger`, `check-ledger --all` (one finding in an archived shard, the same in all four runs), `check-handoff` and `check-handoff --all` (both OK). A first run at `4a521e4` compared the stub's findings (the newest receipt was this session's pending claim) and is replaced by this one. **`layer6b-probe-output.txt`:** the layer's own commits with the tip's `bin/migrate-layout`, its suite and its sync suite: without the prose the same 10 of 23 tests fail as with the tip's whole checker files (S319's `checkers` state), and **with the tip's 23 framework documents added the whole 280-test suite runs OK in 361 s**, so these seven edits are all the checkers owe the tool (S319's NOT CHECKED, answered). **`layer6b-record.md`:** the answer, the measurements, the decisions the plan did not take (the pin test replaced, not deleted, so `layout-unit-tests` keeps its floor of 76; three tests beyond the tip's suite), what this does not show, and the next step. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S320 -- the checkers' layer's contrast and the two mutation rounds (22 of 22 killed after the second round's three survivors became tests)

The checkers' layer's contrast and mutation outputs. **`layer6b-contrast-output.txt`** (`layer-contrast.sh`): of the 11 new tests, 6 fail on the parent's tools; the 5 that pass on both pin behaviour the old tools had and the layer must keep (the repository called `methodology` reading `docs/archive/`, the seed fallback, `--file` in each checker, `check-ledger`'s no-ledger report). **`layer6b-mutate-round1-output.txt`:** 14 mutants over the lines the layer carries and 2 over the same-line markers: **16 of 16 killed** (the markers by the scanner gate, which no unit suite reads). **Round 2 aimed at behaviours no test named:** `layer6b-mutate-round2-before-output.txt` is the run on the 8-test tree (`5c33383`, regenerated from the commit): **3 killed, 3 SURVIVED**: an explicit `--file` ignored in `check-ledger` and in `check-handoff` (the refusal message of both says to name the file with it, and no test showed that works), and `check-ledger` looking in the wrong directory when it finds no ledger. Three tests were added (the tip's suite has none of them) and `layer6b-mutate-round2-output.txt` is the run on the final tree: **6 of 6 killed**; round 1 re-run there reads 16 of 16. The changed line of each mutant is printed beside its verdict (a first-occurrence replace once landed in a docstring and read as "survived"). Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S320 -- the checkers' layer's verification and measurement: the clean-clone gate run (16/16, 0 unmeasured), the first commit's shell suite, the measurement script and its output

The checkers' layer's verification and measurement, as saved outputs. **`layer6b-verify-output.txt`:** `layer-verify.sh` on `505541c` in a clean `--no-local` clone (9 min 37 s, load average 11.95 at launch, exit 0): ratchet **16/16 pass, 0 fail, 0 unmeasured, results `e960a10e187f`, manifest `8169f9089eea`**, `tests-sh-passed` 300 (its floor), `checker-layout-unit-tests` 11, `layout-unit-tests` 76, the scanner 14 files and 0 sites, the one shipped `.verify.sh` exit 0. **`layer6b-commit1-suite-output.txt`:** the shell suite on `a459b8b` alone, 299 passed, 0 failed, 0 skipped (5 min 22 s). An earlier verification of the same layer on the 8-test tree (16/16, results `593ae11339ea`) is superseded and not saved: three tests were added afterwards. **`layer6b-measure.sh` and its output:** the checkers' suite 11 tests OK, the layout suite 76 OK on the layer and on the parent; the builder reproduces tree `bc9d4c00f6d5` (the layer's) and refuses on one byte of drift in the candidate's `bin/check-handoff` with 0 dirty paths; the scanner read 6 sites in `bin/check-handoff` and 4 in `bin/check-ledger` on the parent and reads 0 in 14 files on the layer; **#94 conflicts in the same 3 files and 15 regions at the parent and at the layer, #92 clean at both**; the scrub input is 3 backlog-code lines, 4 phase lines and 5 plan lines over the 364 added lines, no session number; the layer is 7 files, +364 / -26, and the candidate is 12 commits, 29 files, +15,279 / -1,085 against `upstream/main`. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S320 -- PR2's checkers' layer built on pr2/candidate (a459b8b, 505541c): the builder, the mutation script, the probe and the real-corpus script

PR2's checkers' layer is built on the local ref `pr2/candidate`: `0aa1897` to **`505541c`**, two commits (`a459b8b`: `bin/check-ledger`, `bin/check-handoff` and the layout suite's `COPIES`, 3 files, +134 / -19; `505541c`: `tools/test_checker_layouts.py`, its `bin/tests.sh` block, the gate `checker-layout-unit-tests` (11), the scanner's scope and the pin test replaced, 5 files, +230 / -7), built in a scratch clone with the builder below and fetched back with `+refs/heads/pr2/candidate:refs/heads/pr2/candidate` (read back: equal to the verified commit). `bin/check-ledger` is the tip's blob whole (`d55209d`: its two hunks are all layout); `bin/check-handoff` is upstream's `d314c4d` plus seven edits cut from the tip's text (+60 / -13, blob `c4b6028`; the tip's is `2eaddac`, +551 / -45 further on, all fork-only lints). Nothing is sent to `KJ5HST/methodology`.
This commit adds four scripts to `docs/planning/pr-composition-evidence/`: `layer6b-build.py` (the builder: every premise asserted before the first write, every inserted string asserted to be the tip's own text), `layer6b-mutate.py` (22 mutants over the layer's code, two rounds), `layer6b-probe.sh` (the layer plus the tip's migration tool and suite, with and without the prose) and `layer6b-realtree.sh` (the fork's own ledgers placed three ways and read by the old and new tools). Their outputs, the measurement script and the record follow in the next commits. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S320 claim (in progress) -- PR2 Part 2's checkers' layer (the layout hunks of `bin/check-ledger` and `bin/check-handoff`) on `pr2/candidate`

CHANGELOG: pending. Operator said `go`, picked PR2's checkers' layer at the Phase 0 picker (S319's recommended next step) and gave three go-aheads there: the push of `615a5c7`, the gate re-run and the HANDOFFS trim then fold (entry below, each done and read back). Phase 0: CHANGELOG frontier `615a5c7` (HEAD at the start), 0 undocumented commits, 0 merges; `HANDOFFS.md` frontier `60d1148` with one later commit (S319's push-and-BL-109 commit, which owes no receipt); no pending receipt; `bin/check-ledger` and `bin/check-handoff` exit 0; `origin/main` was `60d1148` (`0 1`) and reads `0 0` after the push; `upstream/main` still `f34769f`; #94 and #92 clean with 0 comments and 0 reviews, #93's one comment is his own (2026-10-05); live sessions in `nprcgenekeepr`, `vscode_quarto_ext`, `wsfct` and `mts-system` (each process's working directory read with `lsof`), none in this repository, so BL-105 phase 4 stays blocked. The dashboard run (72/100, one high flag, S319 traced it to `docs/planning/BACKLOG.md`, now 58,987 B against its 56,750 B budget; not re-derived here) left one snapshot line, committed with this claim; `CLAUDE.md` reads 18,737 B against its 18,600 B resident ceiling (reported, not this session's deliverable); `CHANGELOG.md --check` fires (212,044 B before this session's entries against 196,608 B) and the real trim is not taken (his word). **This session's one deliverable is the checkers' layer only:** the layout hunks of `bin/check-ledger` and `bin/check-handoff` and the suite for them, as checkpoint commits of at most 5 files on `pr2/candidate`, built and verified in scratch clones, un-pushed. Nothing is sent upstream. Closed by a NEW close-out entry (a committed entry is never rewritten). Model: Claude Sonnet 5.5.

### 2026-10-14 · [ad hoc] S320 -- the Phase 0 go-aheads: the fork push (`60d1148..615a5c7`), the gate re-run, the HANDOFFS trim (`32a0c58`) and its shard pointer folded into the archive index

His answer to the S320 Phase 0 picker ticked all three go-aheads (the gate re-run, the HANDOFFS trim then fold, the push of `615a5c7`) and picked PR2's checkers' layer as the deliverable. **The push, first (it touches no tree):** `git push origin "${SHA}:refs/heads/main"`, a fast-forward `60d1148..615a5c7`, read back with `ls-remote` (equal) and `rev-list --left-right --count origin/main...HEAD` (`0 0`); the fork only, nothing sent to `KJ5HST/methodology`. **The gate re-run:** `python3 starter-kit/quality_ratchet.py --run` in a clean `--no-local` clone of `615a5c7` under the scratchpad (`s320-gate`), launched `nohup ... &` with a done-file at 23:47:01Z (load average 13.86 at launch), finished 00:08:17Z (1,276 s, exit 0): **18/18 pass, 0 fail, 0 unmeasured, results `d7576eaf9b5b`, manifest `a690abd884d4`**, equal to S319's citation, so the Phase 0 check of the newest receipt's `quality_ratchet:` line is discharged (3 receipts in the clone: `tests-sh-passed` read 503); a `pgrep` read after the done-file found no gate process. **The trim** (`32a0c58`, the tool's own entry below): the dry run named `docs/archive/HANDOFFS-through-2026-10-14-4.md` as S319 had guessed; `methodology_trim.py --file HANDOFFS.md --cut 2 --force --write` moved S317's receipt (3 receipts to 2, 39,659 B to 27,867 B), L1, L2 and L3 held, the shard's `.verify.sh`, `bin/check-handoff` and `bin/check-ledger` exit 0; 4 files in the commit, the dashboard's appended snapshot line left unstaged for the claim. **The fold** (this commit): the tool's pointer block out of `HANDOFFS.md`, one row for the shard added to `docs/HANDOFFS_ARCHIVE_INDEX.md`. Not done: the `CHANGELOG.md` trim (his word; its trigger fires and its dry run is RED-refused without `--force`). No session is claimed at this entry; the claim follows. Model: Claude Sonnet 5.5.

### 2026-10-14 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-14-4.md` (1 record(s), 39,659 B → 27,867 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-14 → 2026-10-14) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-14-4.md`](docs/archive/HANDOFFS-through-2026-10-14-4.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-14-4.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-14-4.md.verify.sh)
rather than trusting a digest printed here. Live file 39,659 B → 27,867 B (−29.7%).

### 2026-10-14 · [BL-109] S319 -- his close-out picker: a backlog row for the fork's `migrate-layout-unit-tests` gate, which passes over a red command-level suite

BL-109 in `docs/planning/BACKLOG.md` (one compact row, +346 B: the file is 58,987 B against its 56,750 B budget, still the dashboard's one high flag) and its detail at the end of `docs/planning/BACKLOG-DETAIL.md`. Written from what S319 measured: the fork's `measure_gate()` (1.5.0, `:483`) is byte-identical to the candidate's and ignores the exit code of a gate with an `extract`; `bin/tests.sh` runs only two fast classes of that suite; a script over `.quality-gates.json` and `bin/tests.sh` found it the only extract gate whose suite is run in part (the other eight are run whole). The fix shape (a second gate over the same command, no `extract`, max 0) is recorded as an option, **not built and no gate changed**; the pull request's candidate gets the pair when its layer is built. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S319 -- his close-out picker: the push of `60d1148` to the fork, read back

He ticked both close-out go-aheads (the push, and a backlog row for the fork's gate; the push was done first, the row is the entry above this one). **The push:** `git push origin "${SHA}:refs/heads/main"` with SHA `60d1148d6bfa64f6957b98666baed6c6ca0c63d5` (named, not `HEAD`), a fast-forward `238c158..60d1148` of the 7 S319 commits, to the FORK `rmsharp/methodology` only. **Read back:** `ls-remote origin refs/heads/main` equal to the local commit, `git rev-list --left-right --count origin/main...HEAD` read `0 0`, no `pr2*` branch on the remote (`pr2/candidate` is still local). Nothing was sent to `KJ5HST/methodology`. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S319 close-out -- PR2 Part 2's seventh layer, `bin/migrate-layout`: not built (a finding and a decision, D5 amended)

**Resolves the claim's `CHANGELOG: pending`.** The picked deliverable, the `bin/migrate-layout` layer, was not built: the tool's own suite fails 10 of 280 tests on the candidate until the checkers' layout hunks and the prose exist (`12cdb87`, `3362f22` and `01d1d51`, the entries below); his picker amended D5 to option (b) and reordered PR2. `pr2/candidate` is unchanged, `0aa1897`, local, nothing sent. **Closed out in full:** the `HANDOFFS.md` receipt (`status: complete`, scores 7 and 7) and the gate run of `01d1d51` in a clean `--no-local` clone: 1,142 s, load average 11.70 at launch, ratchet 18/18 pass, 0 fail, 0 unmeasured, results `d7576eaf9b5b`, manifest `a690abd884d4`, the shell suite at 503 passed and 0 failed (3 receipts in the clone). **A correction to the claim entry below:** it says "Phase 3F rewrites this entry"; the ledger refuses an edit of a committed entry (the pre-commit hook did, at this close-out), so the claim stands as written and this entry closes it. No fork learning row appended (rows considered: #16, #62 and the distributed #13). Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S319 -- his picker: D5 amended to option (b) and PR2's layers reordered (the checkers' layout hunks, the prose, then `bin/migrate-layout`); the layer 7 record, the plan, and the BL-101 row and detail

I stopped the build at the probe's finding and asked, with three ways on (amend D5 and reorder; keep D5 and edit the 1,458-line tool; build the prose layer now). **He picked the first, the recommended one:** carry the layout hunks of `bin/check-ledger` and `bin/check-handoff` (10 scanner sites), hand-built as upstream's blob plus those hunks, then the prose, then `bin/migrate-layout` last. That is plan section 7's own option (b) for D5, which the S317 picker had declined in favour of (a). Written: `docs/planning/pr-composition-evidence/layer7-record.md` (the answer first, the two causes measured by adding each alone, what the probe and the draft builder do and do not show, what is not known, the checkers' layer as the next one); `docs/planning/upstream-pr-composition-plan.md` (the status line, section 3's order, section 4's row F, section 7's header and an "Amended" paragraph under D5; 26,302 B against its 30,000 B declared budget); `docs/planning/BACKLOG.md` (the BL-101 row's next-layer phrase, +68 B; the file is 58,641 B against its 56,750 B budget, still the dashboard's one high flag) and `docs/planning/BACKLOG-DETAIL.md` (one sentence on the finding and the amendment). The fork tip's `migrate-layout-unit-tests` gate has the same hole the draft repairs for the candidate; **not changed, his call.** `bin/check-links` exit 0 (80 links); the added links each resolved by hand. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S319 -- PR2 layer 7's draft builder and the paired-gate proof

`layer7-build.py` follows layer 6's pattern (every precondition asserted before the first write). It is a DRAFT and says so in its docstring: its mechanics were run once on `0aa1897` in a scratch clone (stage `tool` 3 files, stage `suite` 2 files then the gates file, the gates file parses); no layer was committed, so the suite stage's result and its floors were not measured, and it must be re-based after the checkers' and the prose layers. `layer7-pair-proof.py` runs the candidate's own `run_gates()` over a stand-in suite that prints `Ran 5 tests` and exits 1: a gate with an `extract` reads 5 and **passes**, a second gate over the same command with no `extract` reads 1 and **fails**, and the command ran once. That is why the tip's `migrate-layout-unit-tests` gate cannot see a red command-level suite (`bin/tests.sh` runs only two of its fast classes, and a gate with an `extract` ignores the exit code), and why the draft writes a pair of gates where the tip has one. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S319 -- PR2 layer 7's probe: the fork tip's `bin/migrate-layout` and its 280-test suite, put whole into a clean clone of `pr2/candidate` (`0aa1897`), fail 10 tests

A build attempt stopped at its first finding: no layer built, `pr2/candidate` still `0aa1897`, nothing sent. `layer7-probe.sh` clones the candidate four times (under `~/.cache`) and runs the suite serially. **As the candidate is, 10 of 280 fail (363 s, exit 1).** Adding only the tip's `bin/check-ledger` and `bin/check-handoff`, 10 of the 23 tests in the two classes that hold the failures still fail; adding only the tip's 23 framework documents, 9 fail; **adding both, all 280 pass (361 s, exit 0).** So all 10 need the prose layer and 9 of them also need the two checkers, which the candidate carries as upstream's legacy-only blobs (`a96b641`, `d314c4d`; plan section 7, D5) while the tool's own after-check runs them over the migrated project. Saved in `docs/planning/pr-composition-evidence/`: `layer7-probe.sh`, `layer7-probe-output.txt`, `layer7-probe-failure-lines.txt` (the assertion each failing test stopped on, per state). The probe's `sed` that shortens test names is a no-op under BSD sed, so those lines print as unittest prints them. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S319 claim (in progress) -- PR2 Part 2's seventh layer, `bin/migrate-layout`, on `pr2/candidate`

CHANGELOG: pending. Operator said `go`, picked PR2's `bin/migrate-layout` layer at the Phase 0 picker (S318's recommended next step) and gave three go-aheads there: the gate re-run, the HANDOFFS trim and fold, and the `CHANGELOG.md` trim as a dry run only (entry below). Phase 0: CHANGELOG frontier `238c158` (HEAD at the start), 0 undocumented commits, 0 merges; `HANDOFFS.md` frontier `f897d93` with one later commit (S318's push record, which owes no receipt); no pending receipt; `bin/check-ledger` and `bin/check-handoff` exit 0; `origin/main` equal to HEAD (`0 0`), so nothing to push; `upstream/main` still `f34769f`; #94 and #92 `mergeable_state` clean with 0 comments and 0 reviews, #93's one comment is his own (2026-10-05); live sessions in `nprcgenekeepr`, `vscode_quarto_ext`, `wsfct` and `mts-system` (each process's working directory read with `lsof`), none in this repository, so BL-105 phase 4 stays blocked. The dashboard run (72/100, one high flag, S318 traced it to `docs/planning/BACKLOG.md` at 58,573 B against its 56,750 B budget; not re-derived here) left one snapshot line, committed with this claim. **The `CHANGELOG.md` dry run (his third go-ahead, nothing written):** `methodology_trim.py --file CHANGELOG.md` alone exits 2, refused SRF-RED (SRF 1.0968 against the most recent archive `21cf425`: the last archive has been given back entirely, and the plan's rule for RED is "do not archive again"); with `--force` and still no `--write` it exits 0 and would archive 131 of 189 records (2026-10-12 to 2026-10-13) to `docs/archive/CHANGELOG-through-2026-10-13.md`, 202,897 B to 98,979 B, L1, L2 and L3 held. **The real trim is his second word and is not taken.** **This session's one deliverable is the `bin/migrate-layout` layer only:** the migration tool, its suite, its gate and wiring, as checkpoint commits of at most 5 files on `pr2/candidate`, built and verified in scratch clones, un-pushed; nothing is sent to `KJ5HST/methodology`. Phase 3F rewrites this entry. Model: Claude Sonnet 5.5.

### 2026-10-14 · [ad hoc] S319 -- the Phase 0 go-aheads: the gate re-run, the HANDOFFS trim (`b1f1f9d`) and its shard pointer folded into the archive index

His answer to the S319 Phase 0 picker picked PR2's `bin/migrate-layout` layer as the deliverable and ticked all three go-aheads (the gate re-run, the HANDOFFS trim, the `CHANGELOG.md` trim as a dry run only). **The gate re-run, first (3 receipts in the tree, so it reads 18/18):** `python3 starter-kit/quality_ratchet.py --run` in a clean `--no-local` clone of `238c158` under `~/.cache/s319-gate`, launched `nohup ... &` with a done-file (load 11.39 at launch), 1,278 s, exit 0: **18/18 pass, 0 fail, 0 unmeasured, results `d7576eaf9b5b`, manifest `a690abd884d4`**, equal to S318's citation, so the Phase 0 check of the newest receipt's `quality_ratchet:` line is discharged; no process was left running (`pgrep` read after the notice). **The trim** (`b1f1f9d`, the tool's own entry below): `methodology_trim.py --file HANDOFFS.md --cut 2 --force`, dry run first (1 of 3 records, 40,360 B to 29,643 B, shard `-3` as S318 guessed), then `--write`; L1, L2 and L3 held, the shard's `.verify.sh`, `check-handoff` and `check-ledger` exit 0; 4 files in the commit, the dashboard's appended snapshot line left unstaged for the claim. **The fold** (this commit): the tool's pointer block out of `HANDOFFS.md`, one row for the shard in `docs/HANDOFFS_ARCHIVE_INDEX.md`. Not yet done: the `CHANGELOG.md` dry run (its trigger fires: 200,581 B against 196,608 B). Model: Claude Sonnet 5.5.

### 2026-10-14 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-14-3.md` (1 record(s), 40,360 B → 29,643 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-14 → 2026-10-14) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-14-3.md`](docs/archive/HANDOFFS-through-2026-10-14-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-14-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-14-3.md.verify.sh)
rather than trusting a digest printed here. Live file 40,360 B → 29,643 B (−26.6%).

### 2026-10-14 · [BL-101] S318 -- his close-out picker: the push of `f897d93` to the fork (read back)

His answer to the S318 close-out picker was to push. `git push origin "${SHA}:refs/heads/main"` under `bash`, a fast-forward `3dd4bc0..f897d93` (7 commits), read back with `ls-remote` (equal to `f897d93`) and `rev-list --left-right --count origin/main...HEAD` (`0 0`); `git ls-remote --heads origin 'pr2*'` lists nothing, so `pr2/candidate` is still local. The fork only; nothing is sent to `KJ5HST/methodology`. **This supersedes item (5) of the S318 receipt's `next_steps`** ("`origin/main` is `3dd4bc0`, 7 unpushed"): the receipt is complete and is not edited. This entry's own commit is a CHANGELOG-only push record and goes to the fork's `origin` under the standing grant for such records. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S318 close-out -- PR2 layer 6 (the sync layers) built and verified on pr2/candidate (0aa1897), un-pushed; the HANDOFFS receipt complete

**Resolves the claim's `CHANGELOG: pending`.** The one deliverable is done: layer 6 on the local ref `pr2/candidate` (`0aa1897`, three commits, 9 files, +1,472 / -112; the candidate 10 commits, 26 files), verified in a clean `--no-local` clone and recorded in `layer6-record.md`; nothing is sent to `KJ5HST/methodology`. **Close-out:** 3A scored S317's handoff 8 (the four numstat figures exact; it missed that Test 15 and `COPIES` couple to the tools, so "two commits" was three); 3B scored this session 8; 3C appended no fork learning row (D3 not triggered; rows considered #16, #107, #72); 3D the receipt, complete, 12,071 B; 3E the gate run in a clean clone of `f4cd4cf` (1,271 s): **18/18 pass, 0 fail, 0 unmeasured, results `d7576eaf9b5b`, manifest `a690abd884d4`**, equal to the Phase 0 run and to S317's citation. **For the next Phase 0:** `CHANGELOG.md` crossed its 196,608 B trigger inside this session (197,984 B before this entry: `methodology_trim.py --file CHANGELOG.md --check` says it fires) and HANDOFFS holds 3 receipts, so TWO trims are due, each its own action, a gate re-run before them or after the claim; `origin/main` is `3dd4bc0`, seven commits are unpushed after this one (a push is his go-ahead). **Mistakes, in full** (receipt, `what_was_done`): the Phase 0 count of live sessions (one, from a cut list; four), an inert mutant, one failing layout-suite test found before any commit, four unmeasured figures in the first draft of the record, one zsh trap. The memory notes for the composition plan, the trim state and the instrument audit were updated. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S318 -- the PR2 layer 6 record, the plan's status line, and the BL-101 row and detail

`layer6-record.md`: §1 the answer, §2 what the layer carries, §3 what it leaves out, §4 the decisions the plan did not take, §5 against #94, #92 and the scanner, §6 what it does not show, §7 next (`bin/migrate-layout`, six files so two commits; the removed sync-suite assertion goes back there). The plan's status line names `0aa1897` and seven layers, the BL-101 row reads "layers 1 to 6 done, `bin/migrate-layout` next" (shorter than before: `BACKLOG.md` is over its budget and does not grow), and its detail gets the layer's summary. **Before this commit every figure in the record was re-checked against the repository and four were corrected:** the scanner series (it read 93 at layer 4 and 14 at layer 5, not 93 at layer 3), the `bin/tests.sh` block comparison (it had no saved script and its "14 blocks only the tip has" paired two blocks wrongly: now `layer6-blocks.py`), an attribution of three acknowledged markers to the tip's tools (not derivable, removed) and a load-average range (one reading was taken, now stated as that). Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S318 -- PR2 layer 6 built and verified on `pr2/candidate` (`0aa1897`, un-pushed): the sync layers, three commits, and their four saved outputs

**The layer:** the local ref `pr2/candidate` is `0aa1897`, three commits on layer 5's `dd581fe`: `4c0bdde` (Test 15 counts rows, 1 file), `261b8d3` (`bin/sync`, `bin/status`, `bin/check-links`, `bin/_manifest_reader.py` and the layout suite's `COPIES`, 5 files) and `0aa1897` (`tools/test_sync_layouts.py`, the wiring block, the scanner's scope, the gates and the layout suite's scan-set test, 5 files): **9 files, +1,472 / -112**; the candidate is 10 commits and 26 files, +14,923 / -1,067. Built in a scratch clone (`~/.cache/s318-build`), fetched into a temporary ref, and `pr2/candidate` moved to it with `git update-ref` only after the verification below. **Verified in a clean `--no-local` clone** (9 min 26 s): the ratchet 15/15 pass, 0 fail, 0 unmeasured (results `c394bd64daa1`, manifest `f83feda853bd`); the shell suite alone 299 passed, 0 failed, 0 skipped in 5 min 38 s; the sync suite 82, the layout suite 76, the scanner 0 sites over 12 files. 70 of the 82 sync tests fail on the parent's tools (the other 12 each read); five mutants each fail only their own tests; the builder reproduces tree `5dd9c8ea255a`; #94 still 3 files and 15 regions, #92 clean. **Decisions the plan did not take:** three commits, not two (the cap and a green suite at each); the scanner skips exactly `bin/check-handoff` and `bin/check-ledger` by name (D5), the one place the candidate's scanner differs from the fork's, which a later resync must not carry back unseen; one assertion of the sync suite (that `bin/migrate-layout` is a file) waits for the next layer. **Finding:** `check-links --layout new` reads 35 dangling links on the candidate's documents (the prose layer's), so Test 10's `--layout both` block is not carried. Outputs: `layer6-verify-output.txt`, `layer6-suite-output.txt`, `layer6-measure-output.txt`, `layer6-blocks-output.txt`. Nothing is sent to `KJ5HST/methodology`. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S318 -- PR2 layer 6's builder (three stages, the base blobs asserted first), its one-run measurement script and the test-block comparison

`layer6-build.py` builds the sync layers in a candidate clone as three stages (`prep`, `tools`, `suite`; the suite stage runs twice, the second time with the three measured counts). It asserts first that the candidate's four tools equal the fork's blobs at `2ed9262` and `7aa27a0`, that `bin/_manifest.py` parses to the same code as the source's once the docstring is dropped, and that the two resolver files equal the source's; it computes every edit before the first write and refuses with nothing written. `layer6-measure.sh` is the whole measurement in one saved run (the unit suites, the contrast, five mutants, the builder's reproduction and its drift refusal, the scanner, #94 and #92, the scrub input, the changed files); `layer6-blocks.py` compares the candidate's `bin/tests.sh` blocks with the tip's, paired by title with the block numbers normalised. **The measure script's first run read one mutant as surviving; it was inert** (it replaced the first `--layout` in `bin/sync`, which is in the docstring), so it was rewritten as two mutants of the guard's own lines and the whole script re-run. Nothing is sent. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S318 claim (in progress) -- PR2 Part 2's sixth layer, the sync layers, on `pr2/candidate`

CHANGELOG: pending. Operator said `go`, picked PR2's sync layers at the Phase 0 picker (S317's recommended next step) and gave three go-aheads there: the gate re-run, the HANDOFFS trim and fold, and the push of `3dd4bc0` (entry below, each done and read back). Phase 0: CHANGELOG frontier `3dd4bc0` (HEAD), 0 undocumented commits, 0 merges, no pending receipt, `bin/check-handoff` and `bin/check-ledger` exit 0; #94 and #92 no comment or review, #93's one comment unchanged since 2026-10-05, `upstream/main` still `f34769f`; live sessions in `nprcgenekeepr`, `wsfct`, `mts-system` and `vscode_quarto_ext` (read from each process's working directory with `lsof`), none in this repository (the Phase 0 report said one session, from a process list cut by `head -10`; corrected here); the dashboard run (72/100, one high flag) left one snapshot line, committed here, and its high flag is now examined: `docs/planning/BACKLOG.md` at 58,582 B against its 56,750 B one-read budget (the medium flags: no CI/CD; the `tests-sh-passed` floor lowered 327 to 294 in `368b29c`, 2026-09-16); `CLAUDE.md` reads 18,737 B against its 18,600 B resident ceiling and the read-set 72,533 B against 56,750 B (reported, not this session's deliverable). **This session's one deliverable is the sync layers only:** the fork's `bin/sync`, `bin/status`, `bin/check-links`, the manifest and its reader, `tools/test_sync_layouts.py` and the gates and test lists they bring, as checkpoint commits on `pr2/candidate` (at most 5 files each), un-pushed. Nothing is sent upstream. Model: Claude Sonnet 5.5.

### 2026-10-14 · [ad hoc] S318 -- the Phase 0 go-aheads: the fork push (`324e947..3dd4bc0`), the gate re-run, the HANDOFFS trim (`2971180`) and its shard pointer folded into the archive index

His answer to the S318 Phase 0 picker ticked all three go-aheads (the gate re-run, the HANDOFFS trim then fold, the push of `3dd4bc0`) and picked PR2's sync layers as the deliverable. **The push, first (it touches no tree):** `git push origin "${SHA}:refs/heads/main"`, a fast-forward `324e947..3dd4bc0`, read back with `ls-remote` (equal) and `rev-list --left-right --count origin/main...HEAD` (`0 0`); the fork only, nothing sent to `KJ5HST/methodology`. **The gate re-run:** `python3 starter-kit/quality_ratchet.py --run` in a clean `--no-local` clone of `3dd4bc0` under `~/.cache/s318-gate`, launched `nohup ... &` with a done-file at 13:40:00, finished 14:01:21 (1,281 s, exit 0): **18/18 pass, 0 fail, 0 unmeasured, results `d7576eaf9b5b`, manifest `a690abd884d4`**, equal to S317's citation, so the Phase 0 check of the newest receipt's `quality_ratchet:` line is discharged (3 receipts in the clone: `tests-sh-passed` read 503). **The trim:** the dry run named `docs/archive/HANDOFFS-through-2026-10-14-2.md` as S317 had guessed; `--cut 2 --force --write` moved S315's receipt (3 receipts to 2, 40,239 B to 28,744 B), the shard's `.verify.sh` exit 0, `bin/check-handoff` and `bin/check-ledger` exit 0, committed as `2971180` (the tool wrote its own entry below this one). **The fold,** in its own commit as the file's note requires: the tool's pointer block and its blank line out of `HANDOFFS.md`, one row for the shard added to `docs/HANDOFFS_ARCHIVE_INDEX.md`. No session is claimed at this entry; the claim follows. Model: Claude Sonnet 5.5.

### 2026-10-14 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-14-2.md` (1 record(s), 40,239 B → 28,744 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-14 → 2026-10-14) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-14-2.md`](docs/archive/HANDOFFS-through-2026-10-14-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-14-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-14-2.md.verify.sh)
rather than trusting a digest printed here. Live file 40,239 B → 28,744 B (−28.6%).

### 2026-10-14 · [BL-101] S317 -- his close-out picker: the push of `324e947` to the fork (read back), and the checker call answered (leave `bin/check-handoff` and `bin/check-ledger` out; plan section 7, D5)

He ticked both recommended options. **The push:** `git push origin 324e94703fd9...:refs/heads/main`, a fast-forward `2bc74b9..324e947`, read back with `ls-remote` (equal) and `rev-list --left-right --count origin/main...HEAD` (`0 0`); no `pr2*` branch exists on `origin`; the fork only, nothing sent to `KJ5HST/methodology`. **The decision** (asked because the S317 receipt named it as binding at the sync layer): the pull request does not carry the layout reading of `bin/check-handoff` (6 scanner sites) or `bin/check-ledger` (4); the candidate's scanner is scoped to the tools adopters receive plus the hook, so `layout-literals` (max 0) can be declared at the sync layer without them. Both checkers are canonical-only, which matches D2 and plan section 4's row F; the fork's own move of its instance files (BL-104) will need the reading later, on the fork. Recorded as **D5** in `docs/planning/upstream-pr-composition-plan.md` section 7 (and in section 4's row F), and in the BL-101 detail. The S317 receipt still says the call is "now binding" and `origin/main..HEAD` "reads 7": both were true when it was written and are superseded by this entry. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S317 close-out -- PR2 layer 5 (the dashboard 2.22.0) built and verified on pr2/candidate (dd581fe), un-pushed; the HANDOFFS receipt complete

The `HANDOFFS.md` receipt is `status: complete` (self 8, predecessor S316 scored 8). The deliverable was PR2's seventh checkpoint: the dashboard 2.22.0 and its 395 tests as one commit on `e9c5cb8` (5 files, +1,350 / -238), green in a clean clone (ratchet 13/13, 0 unmeasured; suite 298/0/0 in 4 min 55 s), its builder reproducing tree `cc072f493724` and refusing on one byte of drift, its 41 added tests shown red on the 2.21.0 dashboard (32 of 41; the 9 that hold on both each read), three mutants each failing only their own layout test. **The finding:** the candidate's dashboard test file is neither a fork blob nor the tip, so the layer builds it with a three-way merge of Part 1's +9 / -34 portability edits and refuses unless the accounting is exact. **Corrected by measurement:** S316's "17 commits since `3616b5f`" (16 on both exact walks, 13 after the base `75f665e`) and its floor "354 to 397" (395: the two tests Part 1 removed). **The fork's own gate run** (clean clone of `a276aa6`, 1,307 s): 18/18 pass, 0 unmeasured, results `d7576eaf9b5b`, manifest `a690abd884d4`. No fork learning row appended (D3 not triggered); rows considered: #94, #16, #70. Open for him: the layout reading of `bin/check-handoff` and `bin/check-ledger` (now binding at the sync layer). Pushed this session: `990cf34..2bc74b9` to the fork's `origin` only, at his go-ahead; nothing sent to `KJ5HST/methodology`. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S317 -- the PR2 layer 5 record, the plan's status line, and the BL-101 row and detail

`docs/planning/pr-composition-evidence/layer5-record.md`: the answer first (the layer, the clean-clone verification, the contrast, the mutants, the builder's reproduction, the scanner at 14, #94 and #92), what the layer carries and leaves out, the five decisions the plan did not take (the test file is a three-way merge of Part 1's portability edits onto the tip's; the floors are measured; five files exactly; the 13 commits after `75f665e`, which corrects S316's "17"; the scrub input), what it does not show, and the next layer, the sync layers (derived: more than five files, so two commits). The plan's status line now names six layers and the sync layers next; the BL-101 row says layers 1, 2, 2b, 3, 4 and 5 done; its detail gains the S317 sentence. The open call (does the pull request carry the layout reading of `bin/check-handoff`, 6 sites, and `bin/check-ledger`, 4?) is unchanged and binds at the sync layer, where `layout-literals` is first declared at 0. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S317 -- PR2 layer 5 built and verified on `pr2/candidate` (`dd581fe`, un-pushed): the dashboard 2.22.0 and its three saved outputs

**The layer:** local ref `pr2/candidate` is `dd581fe`, ONE commit on layer 4's `e9c5cb8`, **5 files, +1,350 / -238** (`git diff --numstat`, summed): the two dashboard twins +370 / -115 each, their tests +595 / -4, the layout suite +13 / -2, the gates file +2 / -2; the candidate is 7 commits and 21 files, +13,455 / -959. Built in a scratch clone (`~/.cache/s317-build`), fetched back with the `+` refspec; **nothing pushed to `origin`, nothing sent to `KJ5HST/methodology`.** **Verified** in a clean `--no-local` clone: `quality_ratchet.py --run` 13/13 pass, 0 unmeasured (results `88f487475334`, manifest `4fa84819da44`); the shell suite alone 298 passed, 0 failed, 0 skipped in 4 min 55 s; dashboard suite 395 (354), layout suite 75 (74); the scanner reads 14 sites (93). **Contrast:** 41 tests added, 32 fail on the 2.21.0 dashboard, 9 hold on both by design (each read), one old test (the version pin) fails there; the layout suite's one added test fails on the old tree and 3 old tests fail there; three mutants each fail only their own test. The builder reproduces tree `cc072f493724` and refuses on one byte of drift. #94 still conflicts in 3 files and 15 regions (the layer adds none), #92 is clean. The outputs: `layer5-measure-output.txt`, `layer5-verify-output.txt`, `layer5-suite-output.txt` in `docs/planning/pr-composition-evidence/`. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S317 -- PR2 layer 5's builder (the base blobs asserted first, a three-way merge for the dashboard's test file) and its one-run measurement script

`docs/planning/pr-composition-evidence/layer5-build.py` writes the dashboard layer into a clone of `pr2/candidate` at layer 4: the two twins verbatim from the fork tip, the layout suite's three edits, the two floors. Before the first write it asserts that the candidate's twins equal the fork's `75f665e` blobs (2.21.0), that the source's twins equal each other, and that `tools/layout_resolver.py` and `tools/layout_fixtures.py` equal the source's. The dashboard's test file is **not** a fork blob (Part 1 removed the two tests that read the fork-only backlog and made a ledger floor relative to the ledgers that exist: +9 / -34), so the builder re-applies that difference with `git merge-file` (ours the candidate's, base `75f665e`'s, theirs the tip's) and refuses unless the merge is conflict-free and differs from the tip by exactly +9 / -34. `layer5-measure.sh` makes every measurement the record cites in one run: the suites, the contrast against the parent's tools, three mutants, the reproduction and the refusal on one byte of drift, the scanner, #94 and #92, the scrub input. The build itself lives on the local ref `pr2/candidate` (`dd581fe`), outside this repository's history, un-pushed. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S317 claim (in progress) -- PR2 Part 2's layer 5, the dashboard, on `pr2/candidate`

CHANGELOG: pending. Operator said `go`, picked PR2 layer 5 (the dashboard) at the Phase 0 picker (S316's recommended next step) and gave three go-aheads there: the gate re-run, the HANDOFFS trim and fold, and the push of `2bc74b9` (entries below, each done and read back). Phase 0: CHANGELOG frontier `2bc74b9` (HEAD), 0 undocumented commits, 0 merges, no pending receipt, `bin/check-handoff` and `bin/check-ledger` exit 0; #94 and #92 no comment or review, #93's one comment unchanged since 2026-10-05, `upstream/main` still `f34769f`; live sessions in `wsfct`, `mts-system`, `nprcgenekeepr` and `vscode_quarto_ext` (read from each process's working directory), none in this repository; the dashboard run (72/100, one high flag) left one snapshot line, committed here; `CLAUDE.md` reads 18,737 B against its 18,600 B resident ceiling and the read-set 72,533 B against 56,750 B (reported, not this session's deliverable). **This session's one deliverable is layer 5 only:** the fork's dashboard (2.22.0) and its tests as checkpoint commits on `pr2/candidate` (at most 5 files per commit), un-pushed; the dashboard test file is rebuilt from the tip with Part 1's portability edits re-applied (receipt, `active_task`). Nothing is sent upstream. Model: Claude Sonnet 5.5.

### 2026-10-14 · [ad hoc] S317 -- the Phase 0 go-aheads: the fork push (`990cf34..2bc74b9`), the gate re-run, the HANDOFFS trim (`35005d8`) and its shard pointer folded into the archive index

His answer to the S317 Phase 0 picker ticked all three go-aheads (the gate re-run, the HANDOFFS trim then fold, the push of `2bc74b9`) and picked PR2 layer 5, the dashboard, as the deliverable. **The push, first (it touches no tree):** `git push origin 2bc74b990a1d...:refs/heads/main`, a fast-forward `990cf34..2bc74b9`, read back with `ls-remote` (equal) and `rev-list --left-right --count origin/main...HEAD` (`0 0`); the fork only, nothing sent to `KJ5HST/methodology`. **The gate re-run:** `python3 starter-kit/quality_ratchet.py --run` in a clean `--no-local` clone of `2bc74b9` under `~/.cache/s317-gate`, launched `nohup ... &` with a done-file at 11:38:23, finished 11:59:16 (1,253 s, exit 0): **18/18 pass, 0 fail, 0 unmeasured, results `d7576eaf9b5b`, manifest `a690abd884d4`**, equal to S316's citation, so the Phase 0 check of the newest receipt's `quality_ratchet:` line is discharged (3 receipts in the clone: `tests-sh-passed` read 503). **The trim:** the dry run named `docs/archive/HANDOFFS-through-2026-10-14.md` as S316 had guessed; `--cut 2 --force --write` moved S314's receipt (3 receipts to 2, 39,486 B to 28,439 B), the shard's `.verify.sh` exit 0, `bin/check-handoff` and `bin/check-ledger` exit 0, committed as `35005d8` (the tool wrote its own entry below this one). **The fold,** in its own commit as the file's note requires: the tool's pointer block and its blank line out of `HANDOFFS.md`, one row for the shard added to `docs/HANDOFFS_ARCHIVE_INDEX.md`. No session is claimed at this entry; the claim follows. Model: Claude Sonnet 5.5.

### 2026-10-14 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-14.md` (1 record(s), 39,486 B → 28,439 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-14 → 2026-10-14) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-14.md`](docs/archive/HANDOFFS-through-2026-10-14.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-14.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-14.md.verify.sh)
rather than trusting a digest printed here. Live file 39,486 B → 28,439 B (−28.0%).

### 2026-10-14 · [BL-101] S316 close-out -- PR2 layer 4 (the context-budget gate 1.4.0) built and verified on pr2/candidate (e9c5cb8), un-pushed; the HANDOFFS receipt complete

The `HANDOFFS.md` receipt is `status: complete` (self 8, predecessor S315 scored 9). The deliverable was PR2's sixth checkpoint: the budget gate 1.4.0 and its 163 tests as one commit on `98ca7fc` (4 files, +356 / -22), green in a clean clone (ratchet 13/13, 0 unmeasured; suite 298/0/0 in 289 s), its builder reproducing the tree and refusing on drift, its 15 added tests shown red on the 1.3.1 tool (10 of 15, five by design on both), #94 still at 3 files and 15 regions. **Gate:** `quality_ratchet.py --run` in a clean `--no-local` clone of `a95a1f0`, the last work commit, read 18/18, 0 unmeasured, results `d7576eaf9b5b`, manifest `a690abd884d4` (1,275 s), equal to the Phase 0 run on `990cf34` and to S315's citation; the close-out commit adds only this entry and the receipt. **Phase 3C: no fork learning row appended** (D3 not triggered, no retirement owed); rows considered: #70, #62, #98. The one new lesson (write `+X / -Y` from `--numstat`, not the stat total, which S314 and S316 each got wrong in a commit message) went to the operator's memory, not to a framework row. **Scratch:** the session's files under `~/.cache` (`s316-*`) were deleted after looking; the older `s310-*` and `s311-*` are not mine and were left. **Nothing sent upstream**; `origin/main` is `990cf34` and 7 commits are unpushed after this one (a push only on his go-ahead). **Offered next:** the HANDOFFS trim (3 receipts: S316, S315, S314; ONE record, S314) as its own action at the next Phase 0, with any gate re-run before it or after the claim. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S316 -- the PR2 layer 4 record, the plan's status line, and the BL-101 row and detail

`docs/planning/pr-composition-evidence/layer4-record.md` (sections: the answer first, what it carries, what it leaves out, decisions taken that the plan did not, the two pull requests and the scanner, what it does not show, next). **The plan's status line** now reads Part 2's first five layers (S316: `e9c5cb8`) with the dashboard first. **The BL-101 row** reads "Part 1 and layers 1, 2, 2b, 3 and 4 done, the dashboard next"; its detail gains a sentence for layer 4. **Three corrections made while re-reading the record against the clone before this commit:** the record first put the session number `S276` and the plan-section citation in the tool's added lines, and both are in the tests (found by grepping each file's added lines); a "15-line test" was 15 lines of another file; and "nothing named `pr2*` exists on `origin`", inherited from layer 3's record, was never read at `origin` until now (`git ls-remote --heads origin 'pr2*'` lists nothing). **The open question the record hands on:** `bin/check-handoff` (6 scanner sites) and `bin/check-ledger` (4) are upstream's tools that the fork's layout reading edits, and plan §4 does not say whether the pull request carries that reading. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S316 -- PR2 layer 4 built and verified on pr2/candidate (e9c5cb8, un-pushed): the context-budget gate 1.4.0; the saved outputs

A non-commit action plus its saved outputs (`docs/planning/pr-composition-evidence/layer4-*-output.txt`); un-pushed, nothing sent to `KJ5HST/methodology`. **The layer:** the local ref `pr2/candidate` is `e9c5cb8`, ONE commit on layer 3's `98ca7fc`, 4 files, +356 / -22 (the candidate: 6 commits, 21 files, +12,191 / -807), built in a scratch clone under `~/.cache/s316-pr2` with its remote removed and fetched back with the `+` refspec. It carries the fork's `starter-kit/context_budget.py` (1.4.0) and `tools/test_context_budget.py` from `7d16bc8` (the candidate's two files were upstream's 1.3.1 and equal the fork's `517ebf6^` blobs; three fork commits touch them from there, on both log walks), the tool's entries in the layout suite's `COPIES` and `RESOLVED`, and the floor `context-budget-unit-tests` 148 to 163. No `bin/tests.sh` change: none of the lines the fork added to it cites the budget gate. **Verified in a clean `--no-local` clone** (`layer-verify.sh`, 7 min 55 s): ratchet 13/13, 0 unmeasured (results `989163398659`, manifest `5d02c560b035`), the shell suite alone 298 passed, 0 failed, 0 skipped in 289 s, the budget gate's suite 163 (OK, 2 skipped, the two that skip at 148 for the same reason), the layout suite 74, the one shipped `.verify.sh` exit 0, the scanner 93 sites (101 at layer 3: the budget gate's 8 are gone). **Contrast:** 15 tests added, 10 fail on the 1.3.1 tool, 5 hold on both by design (each read), and one OLD test fails there because it pins the mechanism by source text and 1.4.0 re-pointed it; two mutants of the layout suite each fail only their own test. **The builder reproduces the commit's tree** (`c00fbaf1f581`) and refuses on one byte of drift. **Against the open pull requests:** #94 still conflicts in 3 files and 15 regions (the layer adds none), #92 clean (`git merge-tree`, exit codes read). **A slip, caught before it left the scratch clone:** the commit message first said the tool changed `+164 / -20`, which is the diffstat's total column; `--numstat` says `+146 / -18`; amended. Model: Claude Sonnet 5.5.

### 2026-10-14 · [BL-101] S316 -- PR2 layer 4's builder and the two contrast scripts, in the evidence directory

A non-commit build plus its scripts, un-pushed, nothing sent upstream. **`layer4-build.py`** builds PR2 Part 2's layer 4 (the context-budget gate 1.4.0) in a candidate clone: it reads the fork's `starter-kit/context_budget.py` and `tools/test_context_budget.py` from a revision (`7d16bc8`), asserts first that the candidate's two files equal the fork's `517ebf6^` blobs and that its `tools/layout_resolver.py` and `tools/layout_fixtures.py` equal the source's (a drifted base makes it refuse and write nothing), then writes the two files, the budget gate's entries in the layout suite's `COPIES` and `RESOLVED`, and, on a second run, the `context-budget-unit-tests` floor 148 to the measured count (163). **`layer-outcomes.py`** prints one outcome line per test of a unittest file, counting a failing subtest against its parent test and silencing what the tools print in-process (its first draft counted 197 tests where the file has 163, because the tools' own stdout was read as outcomes: caught by the count, fixed before any figure was kept). **`layer-contrast.sh`** runs a layer's new test file against the layer's parent tool and reports how many added tests fail there; it is the method behind layer 3's contrast, which had no saved script. Model: Claude Sonnet 5.5.

