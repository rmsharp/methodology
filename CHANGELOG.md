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

---

## 2026-09

## 2026-10

### 2026-10-13 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-13-3.md` (1 record(s), 36,337 B → 26,892 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-13 → 2026-10-13) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-13-3.md`](docs/archive/HANDOFFS-through-2026-10-13-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-13-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-13-3.md.verify.sh)
rather than trusting a digest printed here. Live file 36,337 B → 26,892 B (−26.0%).

### 2026-10-13 · [ad hoc] S312 -- the push of `8ab29a9` to the fork's `origin/main`, at his close-out picker

His go-ahead at the S312 close-out picker (`Push 8ab29a9`), by name and not `HEAD`: `f8ef5f2..8ab29a9` to `https://github.com/rmsharp/methodology.git` (the fork, not `KJ5HST/methodology`), 8 commits (the Phase 0 picker's trim `3c1ba2c` and fold `4b49224`, the claim, the two scripts, the saved outputs, the record, the close-out), a fast-forward checked with `merge-base --is-ancestor` first. **Read back:** `git rev-list --left-right --count origin/main...8ab29a9` read `0 0`, `ls-remote` returns `8ab29a95c4a3` for `refs/heads/main`, equal to the local commit, and `ls-remote --heads origin` holds no head naming `pr2`: the candidate branch is still local only. This entry is the one commit after the push and stays local until the next one.

### 2026-10-13 · [BL-101] S312 close-out -- PR2 Part 2's first layer built (`pr2/candidate` is `14ef959`, un-pushed), the HANDOFFS trim and fold done, the gate run read 18/18

The deliverable was PR2's second checkpoint: the layout resolver, the fixture trees and the literal scanner as one commit on Part 1's `bbe0dc3` (7 files, +1,225 / -2), green in a clean clone (ratchet 13/13, 0 unmeasured; suite 272/0/0 against Part 1's 271/0/0), the scanner reading 158 sites over 9 files on purpose, so its gate is not declared yet. **The gate citation** (the one Phase 0 step I did not do under a load average of 27 to 40) was run at close-out in a clean `--no-local` clone of the last work commit `e8a815b`: **18/18 pass, 0 unmeasured, results `d7576eaf9b5b`, manifest `a690abd884d4`, 1,419 s, equal to S311's.** Predecessor (S311) scored 9: helped (each checked) by the trim command and its guessed shard name, the `origin/main` count, the live-session list, the `part1-verify.sh` route and the `+` refspec; missing the layer's file list and that the fixtures need `NEW_LAYOUT`; wrong nothing found. Self-score 8: a complete Phase 0 with each skipped step stated, the claim before technical work, all four files read before any edit, a builder that reproduces the commit, every fork commit at most 5 files; minus three repeats of known traps (a `/tmp` file, an unquoted `echo ====` under zsh, a builder that wrote before it had checked every anchor), the Phase 0 gate re-run left to close-out, and about ten silent stretches the harness nudged. **No fork learning row appended** (D3 not triggered, no retirement owed; rows considered #24, #31, #97). The receipt is in `HANDOFFS.md` (S312, complete); `HANDOFFS.md` holds 3 receipts, so its trim is offered at the next Phase 0. Nothing is sent upstream.

### 2026-10-13 · [BL-101] S312 -- the PR2 Part 2 layer-1 record, the plan's status line, and the `BL-101` row and detail

`pr-composition-evidence/layer1-record.md` (the answer first: `pr2/candidate` is `14ef959`, 7 files, +1,225 / -2, clean-clone ratchet 13/13 with 0 unmeasured, suite 272/0/0; what it carries and leaves out; four decisions the plan did not take; what it does not show; the open design question for layer 2). The plan's status paragraph and the `BL-101` row (`BACKLOG.md`) and its detail (`BACKLOG-DETAIL.md`) now read Part 1 and layer 1 done, layer 2 next. The row grew by 13 B (the file is over its 56,750 B budget either way). No claim in the record is carried over from a sub-agent or from memory: each figure is in `layer1-*-output.txt` or was printed by a command run this session.

### 2026-10-13 · [BL-101] S312 -- the saved outputs of PR2 Part 2's first layer

Three files under `docs/planning/pr-composition-evidence/`, each headed by the command that printed it: `layer1-verify-output.txt` (`layer-verify.sh` over a clean `--no-local` clone of `14ef959`: ratchet 13/13 pass, 0 fail, 0 unmeasured, results `3dc6075cbb35`, manifest `45c7608f36d2`, 259 s, the scanner's line, the one proof's exit 0), `layer1-suite-output.txt` (`bash bin/tests.sh` on the layer's tree before its commit: 272 passed, 0 failed, 0 skipped, 165 s; the committed tree is byte-equal, `git status` was clean after the commit) and `layer1-scanner-output.txt` (`bin/check-layout-literals` over the layer-1 tree: exit 1, 158 sites over 9 of 14 files scanned, the to-do list of the layers that follow).

### 2026-10-13 · [BL-101] S312 -- PR2 Part 2's first layer built in a scratch clone: local branch `pr2/candidate` is now `14ef959` (un-pushed), and its two scripts added

A non-commit action plus its scripts. **The build** (plan `upstream-pr-composition-plan.md` §3 and §5, PR2's second checkpoint of two to four): a scratch clone under `~/.cache/s312-pr2` with its remote removed (a bare `git push` cannot send it), one commit `14ef959` on `bbe0dc3`, **7 files, +1,225 / -2**: the layout resolver, the fixture trees in both layouts and the literal scanner, byte-identical to this repository's `a36d9f8`; `tools/test_layout_resolver.py` edited (the lists of embedding tools start empty, the dashboard twin's test left for the dashboard layer, close-out report out of the scan list); `bin/_manifest.py` gains `NEW_LAYOUT` and nothing else of the fork's (its other differences are comment and test-number churn); one suite block in `bin/tests.sh`; the gate `layout-unit-tests` (74) and `tests-sh-passed` 271 to 272. Fetched into this repository with a forced refspec and read back: `pr2/candidate` = `14ef959`, its parent `bbe0dc3`, 2 commits above `upstream/main` `f34769f`, 14 files, +8,989 / -576, no upstream configured, nothing on `origin`. **The scripts:** `layer1-build.py` (reads each file from a named revision, every edit asserted to match once, all computed before the first write; run on `bbe0dc3` it reproduces `14ef959`'s tree, `e32dea7f2635`) and `layer-verify.sh` (the clean-clone check for any layer: changed files against the parent, the ratchet run, the scanner's line, every tracked proof's exit). Nothing is sent upstream.

### 2026-10-13 · [BL-101] S312 claim (in progress) -- PR2 Part 2's first layer, the resolver and the literal scanner, on `pr2/candidate`

CHANGELOG: pending. Operator said `go` to the S311 close-out pick (PR2 Part 2, first layer) and answered the S312 Phase 0 picker `Trim, then Part 2 layer 1`; the trim (`3c1ba2c`) and its fold (`4b49224`) are done and entered above. Phase 0: both ledger frontiers `9258dd0`, 0 undocumented commits, 0 merges, no pending receipt, `bin/check-handoff` and `bin/check-ledger` exit 0; the local `.quality-gates-results.json` is the 2026-10-10 run (head `4afc0d6`), so it neither confirms nor contradicts S311's cited run, and the only commits since the cited `51e13c6` touch the two ledgers; the gate re-run is NOT done at Phase 0 because the machine's load average read 27 (a `--run` at that load risks `unmeasured` on the 600 s timeout), and the layer's own clean-clone run measures it; #94 and #92 have no comment or review, #93's one comment is his own; live sessions are in `vscode_quarto_ext`, `nprcgenekeepr`, `wsfct` and `mts-system`; the dashboard run (76/100, one high flag) left one snapshot line, committed here. **This session's one deliverable is the first Part 2 layer only:** the plan's P1 content (`methodology-subdirectory-plan.md` §7.1) as one checkpoint commit on `pr2/candidate`, un-pushed. Nothing is sent upstream.

### 2026-10-13 · [ad hoc] S312 -- the HANDOFFS trim (`3c1ba2c`) at his Phase 0 go-ahead, and its shard pointer folded into the archive index

His answer to the S312 Phase 0 picker (`Trim, then Part 2 layer 1`, as recommended) covered this trim and the build that follows. **The trim:** a dry run first, which named `docs/archive/HANDOFFS-through-2026-10-13-2.md` as S311 had guessed; then `--cut 2 --force --write`: S309's receipt moved, 3 receipts to 2, 38,029 B to 27,072 B, the shard's `.verify.sh` exit 0, `bin/check-handoff` and `bin/check-ledger` exit 0 (the tool wrote its own entry above). **The fold,** in its own commit as the file's note requires: the tool's pointer block and its blank line out of `HANDOFFS.md`, one row into [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md). `HANDOFFS.md` holds 2 receipts (S311, S310) until the claim.

### 2026-10-13 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-13-2.md` (1 record(s), 38,029 B → 27,072 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-13 → 2026-10-13) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-13-2.md`](docs/archive/HANDOFFS-through-2026-10-13-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-13-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-13-2.md.verify.sh)
rather than trusting a digest printed here. Live file 38,029 B → 27,072 B (−28.8%).

### 2026-10-13 · [BL-101] S311 -- his close-out picker answers recorded: the push of `f8ef5f2` read back, PR2 Part 2's first layer next, and the `vscode_quarto_ext` line left alone

His answers at the S311 close-out picker: push `f8ef5f2` to the fork's `main` (`177dc79..f8ef5f2`, `git rev-list --left-right --count origin/main...f8ef5f2` read `0 0`, `ls-remote` equal, no `pr2` branch on the remote; the first attempt failed with no effect because zsh read `"$SHA:refs/..."` as a history modifier, and it was re-run under `bash` with braces); and the next deliverable, **PR2 Part 2's first layer** (the resolver and scanner, plan §3 order). **`vscode_quarto_ext`:** before proposing a restore of the line my dashboard run appended, I re-read the project: a live session is now in that tree (pid 10754), `test/integration/suite/crossref.test.ts` is modified, and `methodology/dashboard_history.jsonl` holds two added lines (18:21:45 and 18:25:40, version 2.22.0), only one of them mine, so nothing was restored and nothing was asked; the receipt's gotcha (7) says so and warns against a `git checkout --` of that file. Fork only; nothing sent to `KJ5HST/methodology`. Model: Claude Sonnet 5.5.

### 2026-10-13 · [BL-101] S311 close-out — PR2 Part 1 built on upstream's tree (`pr2/candidate`, `bbe0dc3`, un-pushed), the push of `177dc79` and the HANDOFFS trim done, and the gate run read 18/18

The deliverable was PR2's first checkpoint: one commit on `upstream/main` `f34769f`, 9 files, +7,765 / −575, green in clean clones (ratchet 12/12, suite 271 passed, 0 failed, 0 skipped against upstream's own 261/0/0; the literal §3 Part 1 had read 433/14/2). The plan's §3 and §4 disagree about what Part 1 holds; §4's reading was built and the record says so (`pr-composition-evidence/part1-record.md`). Before the claim, on his two Phase 0 go-aheads: the push of `177dc79` (`2d2fe53..177dc79`, `0 0`) and the HANDOFFS trim `77bb319` with its fold `d51d315`. His mid-turn question about `vscode_quarto_ext` was answered from git and `bin/status`; **one side effect of mine there is disclosed above and in the receipt:** I ran that project's dashboard in its tree, one line was appended to its `methodology/dashboard_history.jsonl`, and the restore was refused by the auto-mode classifier. The `HANDOFFS.md` receipt is complete (`self_score` 8, `predecessor_score` 9); no fork learning row appended (D3 not triggered). Gate citation: 18/18 pass, results `d7576eaf9b5b`, manifest `a690abd884d4`, in a clean clone of `51e13c6`. Fork only; nothing sent to `KJ5HST/methodology`. Model: Claude Sonnet 5.5.

### 2026-10-13 · [BL-101] S311 -- the PR2 Part 1 record, the plan's status line, and the `BL-101` row and detail

`pr-composition-evidence/part1-record.md` (what Part 1 carries and leaves out, file by file, with the diff that decided each; the decisions the plan did not make; what it cannot show; one mistake of this session's kept in it: a first draft said the pipeline lint could not be carried, and measuring its scanner, 10 sites in upstream's file and 0 after the three converted blocks, showed it could, so it is carried as Test 36). `upstream-pr-composition-plan.md`'s status paragraph now says Part 1 is built and Part 2's layers are next, and names the §3/§4 disagreement about what Part 1 holds. `docs/planning/BACKLOG.md`'s `BL-101` row reads "Part 1 done, Part 2 next" (+8 B, 58,195 B against its 56,750 B read budget; the dashboard's one high flag stands), its detail carries the figures. Fork only. Model: Claude Sonnet 5.5.

### 2026-10-13 · [BL-101] S311 -- the saved outputs of PR2 Part 1's measurements

Three files under `docs/planning/pr-composition-evidence/`, each printed by a command named at its top: `part1-literal-output.txt` (the literal Part 1 over upstream's tree: 433 passed, 14 failed, 2 skipped, the nine blocks, and the dashboard suite's 3 failures of 356), `part1-verify-output.txt` (the clean-clone ratchet run of `bbe0dc3`, the suite alone at 271 passed, 0 failed, 0 skipped, and every shipped `.verify.sh`'s exit code in upstream's tree and the candidate's, equal) and `part1-files-and-tokens-output.txt` (the nine changed files, their empty intersection with plan §4's not-carried sets, and the token counts of the added lines: 88 with a backlog code, 80 with a session number, 33 naming a `docs/planning/` path, seven of those documents absent upstream). Fork only. Model: Claude Sonnet 5.5.

### 2026-10-13 · [BL-101] S311 -- PR2 Part 1 built in a scratch clone: local branch `pr2/candidate`, commit `bbe0dc3`, un-pushed; its three scripts added

A non-commit action plus its scripts. **The build** (plan `upstream-pr-composition-plan.md` §5, PR2's first checkpoint of two to four): a scratch clone under `~/.cache/s311-pr2` with no remote, one commit `bbe0dc3` on `upstream/main` `f34769f`, **9 files, +7,765 / −575** (dashboard 2.11.3 to 2.21.0 both copies and its suite, trimmer 1.5.0 to 1.7.0 and its suite, one apparatus paragraph, `BOOTSTRAP.md`'s row, `bin/tests.sh`, three gate floors), fetched into this repository as the local ref `pr2/candidate` (no upstream configured). **First measurement, which the plan named its first unknown:** the literal Part 1 of §3 (the 25 files of `upstream/main..c8b9ddd` over upstream's tree) runs the suite to 433 passed, 14 failed, 2 skipped, in the HEAD probe's nine blocks; Part 1 as §4 reads it (E, F and G left on the fork, comment-only files left out) reads, in a clean `--no-local` clone of `bbe0dc3`: `quality_ratchet: 12/12 pass · 0 fail · 0 unmeasured · results 3d7518cbbfea · manifest 0ca43ccb57ba`, the suite 271 passed, 0 failed, 0 skipped (upstream's own 261/0/0), and the one shipped `.verify.sh` exits 0 in both trees. **Added here:** `pr-composition-evidence/part1-literal.sh`, `part1-verify.sh` and `part1-build-tests-sh.py`. Nothing pushed, nothing sent to `KJ5HST/methodology`. Model: Claude Sonnet 5.5.

### 2026-10-13 · [BL-101] S311 claim (in progress) -- PR2 Part 1, the earlier lineage built on upstream's tree

CHANGELOG: pending. Operator said `go`, picked PR2, the candidate build (`docs/planning/upstream-pr-composition-plan.md` §5), at the Phase 0 picker, and gave two go-aheads there, each read back before this claim: the push of `177dc79` (`2d2fe53..177dc79`, `0 0`) and the HANDOFFS trim `77bb319` with its fold `d51d315` (entries below). The gate citation re-run at Phase 0 (clean `--no-local` clone of `177dc79`) read 18/18, results `d7576eaf9b5b`, manifest `a690abd884d4`, equal to S310's; `bin/check-handoff` and `bin/check-ledger` exit 0; 0 undocumented commits, 0 merges, no pending receipt; #94, #92, #93 no maintainer reply; the dashboard run left one snapshot line, committed here. **This session's one deliverable is PR2's first checkpoint only** (the plan puts PR2 at two to four sessions): Part 1, the earlier lineage, as one commit on a local branch in a scratch clone of `upstream/main` `f34769f` under `~/.cache`, the suite run on it, nothing pushed. Nothing sent to `KJ5HST/methodology`. Model: Claude Sonnet 5.5.

### 2026-10-13 · [ad hoc] S311 -- the push of `177dc79` to the fork, and the S311 HANDOFFS shard pointer folded into the archive index

His go-aheads at the S311 Phase 0 picker, each read back. **The push:** `177dc79` (named, not `HEAD`) to the fork's `main`, `2d2fe53..177dc79`; `git rev-list --left-right --count origin/main...177dc79` read `0 0` and `ls-remote` equal. **The trim** (`77bb319`, the entry above): S308's receipt to `HANDOFFS-through-2026-10-13.md`, the shard name S310 guessed; dry run first, shard proof exit 0, `check-handoff` and `check-ledger` exit 0, 2 receipts left. **The fold,** in its own commit: the trimmer's three-line pointer block and its blank line out of `HANDOFFS.md`, one row into [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md). **A side effect in another repository, disclosed:** answering his mid-turn question whether `vscode_quarto_ext` is ready, I ran that project's own `methodology/methodology_dashboard.py` inside its tree, which appended one snapshot line to its `methodology/dashboard_history.jsonl` (1 insertion, 0 deletions, uncommitted there). Restoring it with `git checkout --` was refused by the auto-mode classifier and I did not work around that; the line is still there for him to keep or discard. Nothing sent to `KJ5HST/methodology`. Model: Claude Sonnet 5.5.

### 2026-10-13 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-13.md` (1 record(s), 37,744 B → 26,629 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-13 → 2026-10-13) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-13.md`](docs/archive/HANDOFFS-through-2026-10-13.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-13.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-13.md.verify.sh)
rather than trusting a digest printed here. Live file 37,744 B → 26,629 B (−29.4%).

### 2026-10-13 · [BL-101] S310 — after the close-out: his picker answers, the push, and the label scope decided

At the S310 close-out picker he decided the `UNREHEARSED` label **stays on every refused list that has moves**, shard or not (simple and always true; the refinement that sets the marker only when a shard proof is in the list is declined, and F32 owes nothing more). He also gave the go-ahead to push `2d2fe53` to the fork's `main`: `origin/main` went `ee12007..2d2fe53` (6 commits), naming the commit and not `HEAD`; read back: `ls-remote` equals `2d2fe53`, `rev-list --left-right --count 2d2fe53...origin/main` read `0 0`. Fork only, nothing sent to `KJ5HST/methodology`.

### 2026-10-13 · [BL-101] S310 close-out — F32 fixed in `bin/migrate-layout`, the HANDOFFS trim and both pushes done, and the gate run read 18/18

The deliverable was F32: a refused run's move list is headed `moves (N, UNREHEARSED):` and carries `rehearsal.skipped` (`51e0259`, five tests first, 280 green, mutation round 7 of 8 killed, the floor 275 to 280; closed in the register and the BL-105 rows at `c50b6f6`). Smoked at the real refused `nprcgenekeepr`, which showed the one thing fixtures did not: the label also appears on a refused list that holds no shard, where it is true and idle (his call, asked at the close-out picker). Before the claim, on his three Phase 0 go-aheads: the fork push of `ee12007`, the push of `82e6049e` to `rmsharp/vscode_quarto_ext`, and the HANDOFFS trim `f50216d` with its fold `a3a8e76`. The `HANDOFFS.md` receipt is complete (`self_score` 8, `predecessor_score` 9); no fork learning row appended (D3 not triggered). Gate citation: 18/18 pass, results `d7576eaf9b5b`, manifest `a690abd884d4`, in a clean clone of `c50b6f6`. Fork only; nothing sent to `KJ5HST/methodology`.

### 2026-10-13 · [BL-101] S310 — F32 closed in the register and the BL-105 rows

The register's F32 row reads **fixed** (`51e0259`, the five tests, the mutation round: 7 of 8 killed, the 8th equivalent because a report whose `rehearsal` is `None` has no moves) and carries a dated S310 line; the BL-105 row in `BACKLOG.md` and its paragraph in `BACKLOG-DETAIL.md` say F32 is fixed, not next (`BACKLOG.md` 58,198 B to 58,187 B). BL-105 itself stays open: phase 4 is done at one adopter of the five that carry the file.

### 2026-10-13 · [BL-101] S310 — F32 fixed: `bin/migrate-layout` labels a refused run's move list UNREHEARSED

The shard proofs run only on a run that can go on, so the list a REFUSED run printed was the plan before them: at `vscode_quarto_ext` 3 moves listed refused, 1 once the sync cleared the refusal. `build_report` now sets `rehearsal.skipped: "refused"` when a run has moves and a refusal stands (`ran` alone could not say so: it is also False when there was nothing to rehearse), and `render_text` heads the list `moves (N, UNREHEARSED):` with one line saying why, in both dry-run and `--apply`. A refusal that comes after the rehearsal (`rewrite-unsafe`) leaves the list unlabelled, because it was rehearsed; the JSON carries the marker for a consumer that reads `moves` as data. **Not chosen:** rehearsing before refusing would rehearse a tree the sync is about to change. Five tests written first (red first: the heading read `moves (38):`, the marker was absent), two of them pin the unlabelled cases; `tools/test_migrate_layout.py` reads 280 tests (275 before), 781 s, OK; `check-layout-literals` 0 sites. The `migrate-layout-unit-tests` floor in `.quality-gates.json` is tightened 275 to 280 (tightening needs no approval). Canonical-only; fork only; nothing sent to `KJ5HST/methodology`. Closing the F32 row in the register and the BL-105 row follows in its own commit.


### 2026-10-13 · [BL-101] S310 claim (in progress) — the F32 fix in `bin/migrate-layout`

CHANGELOG: pending. Operator said `go`, picked F32 at the Phase 0 picker (his pick at the S309 close-out, confirmed), and gave three go-aheads there, each read back before this claim: the push of `ee12007` to the fork, the push of `82e6049e` to `rmsharp/vscode_quarto_ext`, and the HANDOFFS trim `f50216d` with its fold `a3a8e76` (entries below). The gate citation re-run at Phase 0 (clean `--no-local` clone of `ee12007`) read 18/18, results `076e9131026f`, manifest `e0f946c5bfe3`, equal to S309's. Deliverable: label a refused dry run's move list as unrehearsed (`bin/migrate-layout:1065`), test first, red first; canonical-only. Fork only, nothing outward to `KJ5HST/methodology`. Phase 3F records the rest.

### 2026-10-13 · [ad hoc] S310 — fold the eighth 2026-10-12 HANDOFFS shard pointer into the archive index

The pointer block the trim (`f50216d`, 1 receipt, S307, to `HANDOFFS-through-2026-10-12-8.md`, the name S309 guessed and the dry run chose) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md`, in its own commit. `HANDOFFS.md` holds 2 receipts (S309, S308). The trim ran on his go-ahead at the S310 Phase 0 picker: dry run first, proof exit 0, `check-handoff` and `check-ledger` exit 0.

### 2026-10-13 · [ad hoc] S310 — pushed `82e6049e` to `rmsharp/vscode_quarto_ext`'s `master`

His own project's remote went `2057838c..82e6049e` (1 commit, the ledger line recording the exclude removed) on his go-ahead at the S310 Phase 0 picker, naming the commit and not `HEAD`; no session had its working directory in that project at the push. Read back: `ls-remote` equals `82e6049e`, `rev-list --left-right --count 82e6049e...origin/master` read `0 0`. Nothing sent to `KJ5HST/methodology`.

### 2026-10-13 · [ad hoc] S310 — pushed `ee12007` to the fork's `main`

`origin/main` went `146efb9..ee12007` (1 commit) on his go-ahead at the S310 Phase 0 picker, naming the commit and not `HEAD`; five files, so outside the CHANGELOG-only standing grant. Read back: `ls-remote` equals `ee12007`, `rev-list --left-right --count ee12007...origin/main` read `0 0`. Fork only, nothing sent to `KJ5HST/methodology`.

### 2026-10-13 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-12-8.md` (1 record(s), 39,979 B → 28,299 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-12 → 2026-10-12) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-12-8.md`](docs/archive/HANDOFFS-through-2026-10-12-8.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-12-8.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-12-8.md.verify.sh)
rather than trusting a digest printed here. Live file 39,979 B → 28,299 B (−29.2%).

### 2026-10-13 · [BL-101] S309 — after the close-out: his picker answers, the two pushes, and the exclude removed in `vscode_quarto_ext`

His answers at the S309 close-out picker, each action read back before the next. **Pushed (named commits, not `HEAD`):** `2057838c` to `rmsharp/vscode_quarto_ext` `master` (`e35d1657..2057838c`, `ls-remote` equal, `0 0`; the push carried that project's own 73 earlier commits since 2026-10-12, which the picker's option text said) and `146efb9` to this fork's `main` (`c7e89c0..146efb9`, `0 0`). Nothing to `KJ5HST/methodology`. **Non-commit action there:** the three lines Session 302 had appended to that clone's `.git/info/exclude` (the `scratchpad/` exclude) removed, as its own note asked after the migration; `git status` reads `?? scratchpad/` again; a copy of the file before is at `~/.cache/s309-exclude.before`; recorded by a ledger entry in that project (`82e6049e`, local, 1 ahead of `origin/master`, not pushed). **Decisions:** F32 is to be fixed as the NEXT deliverable (his pick); F16 stays declined (his). The receipt's `next_steps`, the BL-105 row and detail, and the register (a dated line) were corrected to say so. Fork only otherwise.

### 2026-10-13 · [BL-101] S309 close-out — BL-105 build phase 4 at `vscode_quarto_ext`: the companion top-up is applied there (local), recorded, and the gate run read 18/18

The session's receipt is complete in `HANDOFFS.md` (S309, `status: complete`, self-score 8, predecessor S308 scored 8). **Deliverable (fork, plus three local commits in his project; nothing sent to `KJ5HST/methodology`, the project's own push is its own go-ahead):** `bin/sync` (`f89ac407` there), one phrase of its `CLAUDE.md` (`741f8aad`, F33) and `bin/migrate-layout --apply` (`2057838c`, **one file** moved, not the three a refused dry run listed: F32); rehearsed in four clones first and checked in a fresh clone of the result (70 files and 5,155 tests, `check-package` 42 files, the ratchet 2/2, `vsce ls` 0 lines different, `vsce package` 44 entries and 1,940,709 B in base and result). Here: the evidence `5d35ba2`, the record, F32, F33 and the BL-105 row `2cc7bab`; before them his go-aheads at the Phase 0 picker, the push of `c7e89c0` to the fork and the HANDOFFS trim `aaa9d40` with its fold `debc793`. The gate in a clean `--no-local` clone of `2cc7bab`, launched `nohup ... &`: 18/18, results `076e9131026f`, manifest `e0f946c5bfe3`, equal to S308's (S308's own citation, re-run at Phase 0 on `c7e89c0`, read the same). Phase 3C: no fork learning row appended (D3 not triggered); rows considered #64, #39, #50. Left for him: the push of the three adopter commits, F32, whether F33 reopens F16, and the local `scratchpad/` exclude in that clone (left in place).

### 2026-10-13 · [BL-101] BL-105 build phase 4: the record, findings F32 and F33, and the BL-105 row

`docs/planning/methodology-subdirectory-evidence/bl105-phase4-vscode-quarto-ext-record.md` (what was done in the adopter, the four rehearsal arms, the final clone's reads, what was not shown, his calls); `findings-register.md` rows **F32** (a refused dry run lists moves the run after the refusal drops: `bin/migrate-layout:1065` rehearses the shard proofs only `if moves and not refusals`; open, his call) and **F33** (the text rewrite left "(project root, committed)" false in the adopter's auto-loaded file; fixed there by its own commit; F16 stays declined, a data point against its premise) and one dated line; the BL-105 row in `BACKLOG.md` (phase 4 started, `vscode_quarto_ext` done, +178 B, 58,111 B of 65,536 B) and its detail paragraph. The plan `methodology-subdirectory-plan.md` was NOT edited: it reads 59,994 B against its own declared 60,000 B (BL-106) and the status belongs in the row and the register. Both backlog proofs exit 0 after the edits. Fork only.

### 2026-10-13 · [BL-101] BL-105 build phase 4 at `vscode_quarto_ext`: the companion top-up applied (three local commits there, not pushed) and checked

An action in another repository, on his pick at the S309 Phase 0 picker. Rehearsed first in clones under `~/.cache/s309-rehearsal` (base, synced, tool alone, tool after one phrase of its `CLAUDE.md`), then applied in `~/Development/vscode_quarto_ext` with no session in it (`pgrep` and `lsof` before each commit): `bin/sync` (`f89ac407`, 5 files updated, seeds untouched, no `--force`), one phrase of its `CLAUDE.md` (`741f8aad`, `(project root, committed)` to `(committed)`, F33), `bin/migrate-layout --apply --trailer` (`2057838c`: **1 file**, `PROJECT_LEARNINGS.md` renamed at 100%, the shard and its proof stay because their proof exits 2 at the new place; the tool's before-and-after checks equal). `master` there is 76 ahead of `origin/master`; nothing pushed. A fresh `--no-local` clone of the result reads 70 test files and 5,155 tests, `check-package` 42 files, the ratchet 2/2, `vsce ls` 0 lines different from the base, `vsce package` 44 entries and 1,940,709 B in base and result, dashboard 76/100. Evidence added here: three scripts (`bl105-p4-vscode-rehearsal.sh`, `-rehearsal-edit.sh`, `-final-clone.sh`) and `bl105-p4-vscode-runs/` (the rehearsal, the edit arm, the real apply report and the final clone's log) under `docs/planning/methodology-subdirectory-evidence/`; the final-clone script was corrected once after its first run assumed the shard would move (it stays) and re-run. Fork only; nothing sent to `KJ5HST/methodology`.

### 2026-10-13 · [BL-101] S309 claim (in progress) — BL-105 build phase 4 on `vscode_quarto_ext`

CHANGELOG: pending. Operator said `go`, picked the BL-105 phase 4 move on `vscode_quarto_ext` at the Phase 0 picker, and gave two go-aheads there, each read back before this claim: the push of `c7e89c0` (`ec24116..c7e89c0`, `0 0`, `ls-remote` equal) and the HANDOFFS trim `aaa9d40` with its fold `debc793`. S308's gate citation re-run at Phase 0 (clean `--no-local` clone of `c7e89c0`) read 18/18, results `076e9131026f`, manifest `e0f946c5bfe3`, equal to S308's. Deliverable: `bin/sync` as its own commit in `vscode_quarto_ext`, then `bin/migrate-layout --apply` for the 3 companion moves, rehearsed in clones first; its project push is its own go-ahead. Fork-side only; nothing outward to `KJ5HST/methodology`.

### 2026-10-13 · [ad hoc] S309 — fold the seventh 2026-10-12 HANDOFFS shard pointer into the archive index

The pointer block the trim (`aaa9d40`, 1 receipt, S306, to `HANDOFFS-through-2026-10-12-7.md`, the name S308 guessed and the dry run chose) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md`, in its own commit. `HANDOFFS.md` holds 2 receipts (S308, S307). The trim ran on his go-ahead at the S309 Phase 0 picker.

### 2026-10-13 · [ad hoc] S309 — pushed `c7e89c0` to the fork's `main`

`origin/main` went `ec24116..c7e89c0` (9 commits) on his go-ahead at the S309 Phase 0 picker, naming the commit and not `HEAD`; read back: `ls-remote` equals `c7e89c0`, `rev-list --left-right --count origin/main...c7e89c0` read `0 0`. Fork only, nothing sent to `KJ5HST/methodology`.

### 2026-10-13 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-12-7.md` (1 record(s), 40,789 B → 29,022 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-12 → 2026-10-12) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-12-7.md`](docs/archive/HANDOFFS-through-2026-10-12-7.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-12-7.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-12-7.md.verify.sh)
rather than trusting a digest printed here. Live file 40,789 B → 29,022 B (−28.8%).

### 2026-10-13 · [BL-101] S308 close-out — the plan for the one upstream pull request is written and decided; the gate run read 18/18

The session's receipt is complete in `HANDOFFS.md` (S308, `status: complete`, self-score 8, predecessor S307 scored 9). **Deliverable (fork only, nothing outward beyond the push of `ec24116` to the fork):** `docs/planning/upstream-pr-composition-plan.md` and `docs/planning/pr-composition-evidence/` (five scripts and their outputs): the fork differs from `upstream/main` by 56 files, +25,804 / −1,409 outside `docs/` and the ledgers, about half from before the directory plan and never sent; upstream's tree with the fork's shipped files over it runs the shell suite to 484 passed, 14 failed, 2 skipped; D8's two gates and the two open pull requests stand in front of it. His four answers (build now, a two-part series, the whole dashboard lineage, the defaults) are recorded; PR2, the candidate build, is next. **The gate run on the last work commit `31025c0`, in a clean `--no-local` clone:** `quality_ratchet: 18/18 pass · 0 fail · 0 unmeasured · results 076e9131026f · manifest e0f946c5bfe3`; S307's citation re-run at Phase 0 (`ec24116`) read the same. **Phase 3C:** no fork learning row appended, so the D3 retirement rule is not triggered; rows considered: fork #97, #71, #50. **His two messages at the end:** `vscode_quarto_ext` is ready for the BL-105 top-up and he is cleaning it up (its `scratchpad/` trimmed by that project's own session); ranked first for the next picker. **Next:** his picker (that top-up, PR2, BL-106, his triage, BL-94's third run, BL-103's three calls), the HANDOFFS trim offer (3 receipts), a push on his go-ahead (9 commits ahead of `origin/main`), watch #94, #92, #93. Model: Claude Sonnet 5.5.

### 2026-10-13 · [BL-101] the upstream pull request plan is DECIDED: his four answers

His picker at the S308 close-out, each as recommended: D1 build the candidate now and decide the `methodology-subdirectory-plan.md` §7.6 waiver at the final approval; D2 one pull request as a two-part series of commits (themes A to D); D3 send the whole dashboard lineage, which overrides the hold ratified on 2026-09-27 (`dashboard-upstream-routing-plan.md` now says so at its top); D4 the defaults (wait for #94 and #92, scrub tokens and dangling paths in a separate commit, carry the register, plan and records, tighten gates by what is added). `BACKLOG.md` BL-101 row and its detail say PR2, the candidate build, is next; `BACKLOG.md` is 57,933 B (+156 B on the standing flag). Nothing built, nothing sent.

### 2026-10-13 · [BL-101] the plan for the one upstream pull request, DRAFT for his approval

`docs/planning/upstream-pr-composition-plan.md` (22,692 B): the fork's tree differs from `upstream/main` by 56 files, +25,804 / −1,409 outside `docs/` and the ledgers, about half of it work from before the directory plan that was never sent; porting only the directory hunks is 52 hand-resolved conflicts in 16 files; upstream's tree with the shipped files laid over it runs the shell suite to 484 passed, 14 failed, 2 skipped, all 14 fixtures of this repository's own history or a stricter checker meeting upstream's ledger; D8's gates (5 adopters, 13 open register rows) and the two open pull requests (#94 in 3 files, #92 in 1) are in front of it. Recommends one pull request as a two-part series of commits, built fork-side now, the waiver decided at the final approval. Four decisions (D1 to D4) go to his picker. `inventory.py` moves the `HANDOFFS.md` seed from the checkers' theme to the ratchet's, which is where it ships. Nothing built, nothing sent.

### 2026-10-13 · [BL-101] evidence for the upstream pull request plan: upstream's tree with the fork's shipped files laid over it

`candidate-probe.sh`, run twice (by hand, then the script): `bin/tests.sh` reads 484 passed, 14 failed, 2 skipped on `upstream/main` plus the overlay (upstream's own suite 261/0/0, the fork's 503/0/0); the 14 sit in 9 of 54 test blocks, all fixtures of this repository's own ledgers or a stricter checker meeting upstream's live ledger; the trimmer, context-budget, ratchet, layout, sync and `migrate-layout` unit suites passed. The two unit suites that fail inside it, run alone, are in `candidate-probe-unit-failures-output.txt`. Fork only, nothing sent.

### 2026-10-13 · [BL-101] evidence for the upstream pull request plan: the two open pull requests and the fork-internal tokens

`conflicts.sh` (#94 conflicts with the fork tip in 3 files, 15 regions; #92 in 1 file, 1 region, `CLAUDE.md`) and `fork-tokens.py` (282 backlog codes, 199 session numbers, 63 `docs/planning/` paths and 25 fork-learning citations on added lines; 14 plan documents they cite are not in `upstream/main`), each with its saved output. Fork only, nothing sent.

### 2026-10-13 · [BL-101] evidence for the upstream pull request plan: the difference and the register's open rows

`docs/planning/pr-composition-evidence/inventory.py` (the fork's tree against `upstream/main`: 56 files, +25,804 / −1,409 outside `docs/` and the ledgers, split at the directory plan's base `c8b9ddd`, by theme, with the adopter impact and the tool versions) and `register-open-rows.py` (13 of the register's 31 rows open, the dated changes applied), each with its saved output. Read git only. Fork only, nothing sent.

### 2026-10-13 · [ad hoc] S308 claim (in progress) — composing the one upstream pull request

CHANGELOG: pending. Operator said `go` and picked composing the one pull request with two go-aheads, each read back before this claim: the push of `ec24116` (`e8188a3..ec24116`, `0 0`, `ls-remote` equal) and the HANDOFFS trim `8e9eaf6` with its fold `2334f25`. S307's gate citation re-run at Phase 0 (clean `--no-local` clone of `ec24116`) read 18/18, results `076e9131026f`, manifest `e0f946c5bfe3`, equal to S307's. Deliverable: a plan in `docs/planning/` presented for his approval first; fork only, nothing sent to `KJ5HST/methodology`. Phase 3F records the rest.

### 2026-10-13 · [ad hoc] S308 — fold the sixth 2026-10-12 HANDOFFS shard pointer into the archive index

The pointer block the trim (`8e9eaf6`, 1 receipt, S305, to `HANDOFFS-through-2026-10-12-6.md`, the name S307 guessed and the dry run chose) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md`, in its own commit. `HANDOFFS.md` holds 2 receipts (S307, S306). The trim ran on his go-ahead at the S308 Phase 0 picker.

### 2026-10-13 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-12-6.md` (1 record(s), 41,372 B → 29,682 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-12 → 2026-10-12) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-12-6.md`](docs/archive/HANDOFFS-through-2026-10-12-6.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-12-6.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-12-6.md.verify.sh)
rather than trusting a digest printed here. Live file 41,372 B → 29,682 B (−28.3%).

### 2026-10-13 · [ad hoc] S308 — pushed `ec24116` to the fork's `main`

`origin/main` went `e8188a3..ec24116` (13 commits) on his go-ahead at the S308 Phase 0 picker, naming the commit and not `HEAD`; read back: `ls-remote` equals `ec24116`, `rev-list --left-right --count origin/main...ec24116` read `0 0`. Fork only, nothing sent to `KJ5HST/methodology`.

### 2026-10-13 · [BL-103] S307 close-out — repair 3 done: a cited gate run that reads unmeasured gates must name them; the gate run read 18/18

The session's receipt is complete in `HANDOFFS.md` (S307, `status: complete`, self-score 8, predecessor S306 scored 9). **Deliverable (fork only, nothing outward beyond the push of `e8188a3` to the fork):** `bin/check-handoff` refuses a newest complete receipt that cites `U` unmeasured gates unless an `unmeasured: <gate>, <gate>` clause names at least `U`; one sentence in the runner's 3E, the seed's §Citing the gate run and `HOW_TO_USE.md`; 20 new rows in the gate-citation block of `bin/tests.sh` (`tests-sh-passed` floor 477 to 503); 18 mutants in two rounds (9 survived round 1, 18 of 18 killed round 2). **The gate run on the last work commit `7f790b3`, in a clean `--no-local` clone:** `quality_ratchet: 18/18 pass · 0 fail · 0 unmeasured · results 076e9131026f · manifest e0f946c5bfe3`; S306's citation re-run at Phase 0 (`08f1ef6`) read 18/18, results `75a345496ff4`, manifest `18a872e7eb40`, equal to S306's. **Phase 3C:** no fork learning row appended, so the D3 retirement rule is not triggered; rows considered: fork #16, #107, #62. **Two committed ledger sentences are wrong and not amended:** the lint's entry cites `:271` and `:273` (the regexes are at `:273` and `:275`; corrected in the prose-rule entry) and the floor's entry says each suite run took 20 to 60 minutes (the shell suite took 9 minutes, the ratchet 47 and 22). The plan's "9 adopters" was 13 sibling projects scanned, 5 with citations (corrected in the evidence entry). **Next:** his picker (the one pull request, BL-105 phase 4 if an adopter is free, BL-106, his triage, BL-94's third run, BL-103's three calls), the HANDOFFS trim offer (3 receipts), a push on his go-ahead. Model: Claude Sonnet 5.5.

### 2026-10-13 · [BL-103] repair 3 recorded; the backlog row says repairs 1, 2 and 3 are done and keeps the three open calls

The record [`docs/planning/bl103-evidence/bl103-repair3-record.md`](docs/planning/bl103-evidence/bl103-repair3-record.md) (what was found, what changed by commit, how it is held, the channels, what was not done, his calls). `docs/planning/BACKLOG.md` row BL-103 is **not closed**: three of his calls remain (the dashboard's mirror of `timeout_seconds`, whether 3600 s stays, whether `--run` should print the unmeasured names in the lint's form), so the row stays in the open table, shorter (57,796 B to 57,777 B; the standing flag is the dashboard's 56,750 B) and `docs/planning/BACKLOG-DETAIL.md` gains the S307 paragraph. Closing it would have dropped the three from the backlog. Fork only.

### 2026-10-13 · [BL-103] `.quality-gates.json`: `tests-sh-passed` floor 477 to 503 (a tightening)

Measured, not derived: `bash bin/tests.sh > file` in a clean `--no-local` clone of `8dab34f` (launched `nohup ... &`, at a load average of 35 to 212) read `== Summary: 503 passed, 0 failed, 0 skipped ==` (483 at S306's last work commit); the 20 added are the repair's rows in the gate-citation block. `60b6412` changed ten rows to assert the lint's message and left the count. The whole suite ran once, after layers 1 to 3 and the first mutation round, not after each layer as the plan said: the machine's load made each run 20 to 60 minutes. Fork only.

### 2026-10-12 · [BL-103] evidence: the mutation script and both rounds' output, regenerated from it

`docs/planning/bl103-evidence/mutate-repair3.py <tests-ref>` (a ref, or `WORKTREE`) mutates a copy of `bin/check-handoff` and runs the gate-citation block of `bin/tests.sh` at that ref. Round 1 against the tests at `5cb11a6`: 18 mutants, 9 killed, 9 survived. Round 2 against `60b6412`: 18 of 18 killed. The first session run used 14 mutants; the script adds M20 to M23 (M23 turns the lint off and is killed by exactly the ten finding rows once they assert the message). Fork only.

### 2026-10-12 · [BL-103] evidence: the population survey and the counting-gate demonstration

`docs/planning/bl103-evidence/survey-citations.py` (this repository: 342 receipts, 167 citations of a gate run, one reading unmeasured above 0, S287's; 13 sibling projects scanned, 4 with declared gates, 5 with citations, 246 citations, none above 0) and `counting-gate-demo.sh` (a gate that counts the unmeasured reads `0 pass` in a run with one, then the previous run's count: it cannot see its own run), each with its output beside it. **Correction to the Phase 4 text of this session:** it said "this repository and 9 adopters"; the figure is 13 sibling projects scanned, 5 carrying citations. Fork only.

### 2026-10-12 · [BL-103] the ten "must be a finding" rows assert the lint's own message, not only a nonzero exit

An exit code also passes on a fixture the schema rejects, which is how three of round 2's `what_was_done` rows would have passed for the wrong reason (no commit sha). `unm_flag` captures the output first (under pipefail `| grep -q` reports the SIGPIPE it causes) and the ten finding rows now require `the cited gate run reads` in it; the 15 "must pass" rows are unchanged (exit 0 means no finding at all). The row count is unchanged (the block reads `PASS=25 FAIL=0`), so the `tests-sh-passed` figure measured at `8dab34f` still holds. **Mutation, re-run on the edited block:** 18 of 18 killed (a mutant that turns the lint off, M23, is killed by exactly the ten finding rows). This is the S307 learning held mechanically, so no fork learning row is appended for it. Fork only.

### 2026-10-12 · [BL-103] mutation rounds on the new lint: 9 of 14 mutants survived round 1, ten tests for them, round 2 kills 17 of 17

**Round 1** (14 mutants of `validate_gate_citation` and its two regexes, run against the extracted gate-citation block of `bin/tests.sh`): 5 killed, 9 survived, each a behaviour no test named: the most unmeasured over several citations (`min` for `max`), the most names over several clauses, only the first citation judged, a clause at a field's end borrowing the next field's first word (`\s` for `[ \t]`), a citation or its clause in `what_was_done` (the search restricted to `runtime_smoke`), a count of ten or more (`\d` for `\d+`), a digit-led gate name, and a pending receipt (the Phase 1B stub) judged for its citation. **Ten rows added** (the block reads `PASS=25 FAIL=0`; 5 before this lint, 15 at the lint's commit). **Two defects in my own rows, found before the commit and fixed:** `$CLEAN1` was unset under `set -u`, and three rows put a citation in `what_was_done` without the commit sha the schema demands, so the "must be a finding" rows would have passed on the schema's error, not the lint's (read the message to tell them apart). **Round 2** (the 14 and three new, 17 in all): 17 killed, 0 survived. Two mutants judged equivalent and not run: splitting a clause on `,` instead of `[ \t]*,[ \t]*` and counting words instead of names give the same count for a clause that matches the regex. Fork only.

### 2026-10-12 · [BL-103] the prose rule: a run that reads unmeasured gates is repaired and repeated, or each gate is named

One sentence in each of three places that state the step: `starter-kit/SESSION_RUNNER.md:284` (3E; TRACKED, so it reaches every adopter's runner through `bin/sync`), `starter-kit/HANDOFFS.md` §Citing the gate run (a SEED: new adopters only) and `HOW_TO_USE.md:766` (the third copy of the 3E sentence, found by the grep inventory; the plan named two). The rule: repair the gate (its command, or `timeout_seconds` if it is only slow) and run again, or name each one as `unmeasured: <gate>, … — by hand: <result>`; the seed also says `bin/check-handoff` lints that clause. **Cost:** the runner goes 55,361 B to 55,585 B (+224 B) on a file already over its 41,364 B ceiling (a reported series, not a gate), the read-set total 72,309 B to 72,533 B. `check-links`, `check-layout-literals`, `check-learnings` and `check-handoff --all` exit 0. **Correction to the entry above:** the two regexes are at `bin/check-handoff:273` and `:275` (that entry says `:271` and `:273`; a committed entry is not amended). No session numbers in the distributed text. Fork only.

### 2026-10-12 · [BL-103] `bin/check-handoff`: a cited gate run that reads unmeasured gates must name them

`validate_gate_citation` (`bin/check-handoff:860`) now reads the cited `U unmeasured` (`GATE_UNMEASURED_RE`, `:271`) and, for the newest complete receipt, reports a finding unless an `unmeasured: <gate>, <gate>` clause (`UNMEASURED_CLAUSE_RE`, `:273`) names at least `U` gates; the message starts "the cited gate run reads", never "receipt" (the answer-slot counter greps that prefix). Spaces and tabs only between the pieces, so a clause at a field's end cannot borrow the next field's first word. **GREEN:** the block alone reads `PASS=15 FAIL=0` (10 and 5 before), and the live ledger passes `--all`. **Run over the real population:** the new function over all 342 receipts in `HANDOFFS.md` and the archives flags exactly one, S287 (3 unmeasured, named in prose, in a frozen shard), and archived receipts are never judged. Canonical-only: adopters get this only if they copy `bin/check-handoff`. Fork only.

### 2026-10-12 · [BL-103] tests: a cited gate run that reads unmeasured gates must name them, written RED first

Ten rows added to the `check-handoff` gate-citation block of `bin/tests.sh` (`# D9:` / `# BL-103 repair 3`): a cited run with `U` unmeasured gates needs an `unmeasured: <gate>, ...` clause naming at least `U` (backticks allowed; only comma-separated names count), a citation with no unmeasured field is judged on its structure alone, `--all` judges the newest receipt the same way, and an older receipt is not re-judged. **RED:** the block run alone reads `PASS=10 FAIL=5`; the five that fail are the five "must be a finding" rows (an unnamed gate, two names for three, a clause naming none, the words after the names counted as a gate, and `--all`), each because `validate_gate_citation` reads only that a citation exists (`bin/check-handoff:851`); the five "must pass" rows already pass. The design, his answers at the S307 Phase 0 picker: the named exception is allowed (not refused outright, not report-only), and the rule goes in the runner and the seed. Fork only.

### 2026-10-12 · [BL-103] S307 claim (in progress) — a gate run that reads `unmeasured` can still be cited

CHANGELOG: pending. Operator said `go`; the Phase 0 report found no free adopter for BL-105 phase 4 and he picked BL-103 repair 3 with two go-aheads, each read back before this claim: the push of `e8188a3` (`a2a856f..e8188a3`, `0 0`, `ls-remote` equal) and the HANDOFFS trim `125c8aa` with its fold `03f1171`. The gate citation re-run (clean `--no-local` clone of `08f1ef6`) was still running at this claim: its result goes in the close-out receipt. Deliverable: research and a plan for repair 3 presented for his approval first; fork only, nothing outward. Phase 3F records the rest.

### 2026-10-12 · [ad hoc] S307 — fold the fifth 2026-10-12 HANDOFFS shard pointer into the archive index

The pointer block the trim (`125c8aa`, 1 receipt, S304, to `HANDOFFS-through-2026-10-12-5.md`, the name S306 guessed and the dry run chose) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md`, in its own commit. `HANDOFFS.md` holds 2 receipts (S306, S305). The trim ran on his go-ahead at the S307 Phase 0 picker.

### 2026-10-12 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-12-5.md` (1 record(s), 41,192 B → 29,692 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-12 → 2026-10-12) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-12-5.md`](docs/archive/HANDOFFS-through-2026-10-12-5.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-12-5.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-12-5.md.verify.sh)
rather than trusting a digest printed here. Live file 41,192 B → 29,692 B (−27.9%).

### 2026-10-12 · [ad hoc] S307 — pushed `e8188a3` to the fork's `main`

`origin/main` went `a2a856f..e8188a3` (15 commits) on his go-ahead at the S307 Phase 0 picker, naming the commit and not `HEAD`; read back: `ls-remote` equals `e8188a3`, `rev-list --left-right --count origin/main...e8188a3` read `0 0`. Fork only, nothing sent to `KJ5HST/methodology`.

### 2026-10-12 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-10-11.md` (101 record(s), 191,782 B → 77,005 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **101** record(s) (2026-10-08 → 2026-10-11) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-10-11.md`](docs/archive/CHANGELOG-through-2026-10-11.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-10-11.md.verify.sh`](docs/archive/CHANGELOG-through-2026-10-11.md.verify.sh)
rather than trusting a digest printed here. Live file 191,782 B → 77,005 B (−59.8%).

### 2026-10-12 · [BL-107] S306 close-out — BL-107 done: `quality_ratchet.py` 1.5.0; the receipt is complete; the gate run read 18/18

A gate's command runs in a session of its own and is stopped with its whole process group on a timeout, Ctrl-C, SIGHUP or SIGTERM; measured first, the row's own fix alone orphaned it on Ctrl-C and on a hangup. Done on the fork and sent nowhere. The gate in a clean `--no-local` clone of `08f1ef6`, launched as `nohup ... &`: 18/18, results `75a345496ff4`, manifest `18a872e7eb40`; S305's citation re-run at Phase 0 equal. `HANDOFFS.md` holds 3 receipts (S306, S305, S304): one trim is owed after the next Phase 0 report. `origin/main` is `a2a856f`, 15 commits behind `HEAD`. The `HANDOFFS.md` receipt carries the rest; Phase 3C appended no fork learning row.

### 2026-10-12 · [BL-107] BL-107 closed: `quality_ratchet.py` 1.5.0 stops a timed-out gate's command

The index row is out of `BACKLOG.md` and the id is in its closed list, the completed row is in `BACKLOG-COMPLETED.md`, `BACKLOG-DETAIL.md` carries the closure, and BL-103's row now says 1.5.0 and that BL-107 is closed. Both `.verify.sh` proofs exit 0. `BACKLOG.md` 58,222 B to 57,796 B (still past the 56,750 B budget the dashboard flags). Fork only, nothing sent to `KJ5HST/methodology`.

### 2026-10-12 · [BL-107] `docs/planning/bl107-evidence/`: the record and the mutation round

`bl107-record.md` (what was measured, what changed, how it is held, the channels, what is not verified, his calls), `mutate-bl107.py` and `bl107-mutation-output.txt`: 29 mutants over `quality_ratchet.py` 1.5.0 in two rounds; round 1 killed 21 of 26, and its five survivors (each a weakness in a test) plus three new mutants were all killed in round 2. The suite kills 29 of 29, the selftest 11. Nothing outward.

### 2026-10-12 · [BL-107] `docs/planning/bl107-evidence/`: the measurement scripts and their output

`bl107-runner.py` (four variants of the command runner, each a process a signal can be aimed at), `bl107-harness.py` (five scenarios by four variants, survivors counted with `ps`), `bl107-stress.py` (60 rounds of `killpg`) and `bl107-output.txt`. Measured before the plan, S306: the fix the row proposed alone orphans the command on Ctrl-C and on a hangup; macOS raises `PermissionError` from `killpg` for a group with a dead, unreaped member. Nothing outward.

### 2026-10-12 · [BL-107] `.quality-gates.json`: `ratchet-unit-tests` floor 118 to 120

A tightening, in its own commit. Measured: `Ran 120 tests`, OK, in a clean `--no-local` clone after round 1 (the same count the mutation baseline printed in round 2). Mutation round 2 killed 8 of 8: the five survivors of round 1 and three new mutants aimed at behaviours no test named (a partial restore of the handlers, an `OSError` message, `SystemExit` against `KeyboardInterrupt`).

### 2026-10-12 · [BL-107] `tools/test_quality_ratchet.py`: four tests for the five survivors of mutation round 1

Round 1, 26 mutants over `quality_ratchet.py` 1.5.0: 21 killed, 5 survived. M17 (a finished command's group killed too) survived a test that looked at the child the instant after the kill; it now watches 1.5 s. M6 and M22 (the shell not reaped, the pipes not closed) were unobservable outside the Popen object; a spy keeps it and asserts `returncode` and closed pipes. M23 (a handler the caller installed is replaced by the default) had no test. M21 (`HAS_PROCESS_GROUPS = True`) is true of POSIX either way; the module is now read as each platform would read it (`os.name` patched), which kills it here. Round 2 (the five and three new mutants) follows.

### 2026-10-12 · [BL-107] `tools/test_quality_ratchet.py`: the driver sets SIGINT too; the Ctrl-C tests failed in a backgrounded run

The same cause as the SIGHUP entry below, one signal further, found by the rerun of the mutation round's baseline (`Ran 2 tests in 30.167s`): a command started with `&` from a non-interactive shell has SIGINT ignored, `nohup` adds SIGHUP, both survive fork and exec (measured: `nohup bash -c 'python3 -c ...' &` prints `SIG_IGN` for both), and Python installs no `KeyboardInterrupt` when it starts with SIGINT ignored, so the two Ctrl-C tests waited 30 s and failed. The driver now installs `signal.default_int_handler` and sets SIGHUP itself. Verified in the launch pattern this repository uses for long runs (`nohup bash -c '...' &`): the whole suite reads 118 OK and the selftest 30/30; the eight signal tests read OK in the foreground and there.

### 2026-10-12 · [BL-107] `tools/test_quality_ratchet.py`: the signal tests set SIGHUP themselves; two of them failed under `nohup`

Found when the mutation round's baseline read red (`Ran 1 test in 30.070s`, fail-fast) and the same suite read 118 OK from a shell. `nohup` sets SIGHUP to ignore and ignored signals survive fork and exec, so the child driver inherited the ignore: the tool correctly left it ignored (by design, `nohup` is why) and `test_a_hangup_of_the_terminal_stops_the_child` and `test_sighup_stops_the_child_and_the_tool_exits_129` failed (`still running 30 s after`, `0 != 129`). Reproduced with `nohup python3 tools/test_quality_ratchet.py <the two classes>`: exactly those two red. The driver now sets SIGHUP default or ignore explicitly; the eight signal tests read OK with and without `nohup`. This repository starts its long runs under `nohup`, so a suite that failed there would have read red in the very runs that cite it.

### 2026-10-12 · [BL-107] `.quality-gates.json`: `ratchet-unit-tests` floor 100 to 118

A tightening, in its own commit and reverting alone. Measured, not derived: `tools/test_quality_ratchet.py` reads `Ran 118 tests`, OK, in the working tree (output captured) and in a clean `--no-local` clone of `76f0082`; the 18 added tests are BL-107's.

### 2026-10-12 · [BL-107] `quality_ratchet.py` 1.5.0 — a gate's command runs in a session of its own and is stopped with its whole group

`run_gate_command` starts the command with `start_new_session=True` and `SIGKILL`s its process group on a timeout and on any exception out of the wait; SIGHUP and SIGTERM become `SystemExit(128+n)` while it runs (a signal the caller ignores stays ignored, as under `nohup`; off the main thread nothing is installed; handlers are put back); a refused `killpg` (macOS `PermissionError`, measured) is swallowed and the shell is killed directly; where there are no process groups (Windows) the 1.4.0 path runs unchanged. `--selftest` 28 to 30 checks; the seed's schema and the docstring say so. Held by 118 tests (100 before), the nine RED tests now green, a real-pty Ctrl-C and hangup. Fork only; the module is distributed, so a sync carries it.

### 2026-10-12 · [BL-107] `tools/test_quality_ratchet.py`: tests for a timed-out gate command that keeps running, written RED first

After his approval at the S306 Phase 4 picker (build as planned; Windows unchanged and stated; `SIGKILL` at once). Twenty tests in three classes: nine fail on 1.4.0, each for its own reason, read: an orphaned child still running 5 s after a timeout (four tests), `-1 != 129` and `-15 != 143` (the tool itself dies of SIGHUP and SIGTERM), a missing `HAS_PROCESS_GROUPS`, two selftest labels and a seed phrase that are absent. The 11 that pass on 1.4.0 are parity and boundary guards (a real pty Ctrl-C and hangup, a finished command left alone, a refused `killpg`, a thread call, the stdlib set now admitting `signal`). Nothing outward.

### 2026-10-12 · [BL-107] S306 claim (in progress) — the timed-out gate command that keeps running

CHANGELOG: pending. Operator said `go`; the Phase 0 report found no free adopter for BL-105 phase 4 and he picked BL-107 with three go-aheads, each read back before this claim: the push of `a2a856f` (`c80c5b5..a2a856f`, `0 0`, `ls-remote` equal), the HANDOFFS trim `c6abae0` with its fold `f0385b0`, and the CHANGELOG trim `21cf425` (not due: 190,194 B against 196,608 B; his go-ahead; 191,782 B to 77,005 B). The gate citation re-run (clean `--no-local` clone of `a2a856f`) was still running at this claim: its result goes in the close-out receipt. Deliverable: research and a plan for BL-107 presented for his approval first; fork only, nothing outward. Phase 3F records the rest.

### 2026-10-12 · [ad hoc] S306 — fold the fourth 2026-10-12 HANDOFFS shard pointer into the archive index

The pointer block the trim (`c6abae0`, 1 receipt, S303, to `HANDOFFS-through-2026-10-12-4.md`, the name S305 guessed and the dry run chose) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md`, in its own commit. `HANDOFFS.md` holds 2 receipts (S305, S304). The trim ran on his go-ahead at the S306 Phase 0 picker.

### 2026-10-12 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-12-4.md` (1 record(s), 41,280 B → 29,425 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-12 → 2026-10-12) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-12-4.md`](docs/archive/HANDOFFS-through-2026-10-12-4.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-12-4.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-12-4.md.verify.sh)
rather than trusting a digest printed here. Live file 41,280 B → 29,425 B (−28.7%).

### 2026-10-12 · [ad hoc] S306 — pushed `a2a856f` to the fork's `main`

`origin/main` went `c80c5b5..a2a856f` (10 commits) on his go-ahead at the S306 Phase 0 picker, naming the commit and not `HEAD`; read back: `ls-remote` equals `a2a856f`, `rev-list --left-right --count origin/main...a2a856f` read `0 0`. Fork only, nothing sent to `KJ5HST/methodology`.

### 2026-10-12 · [BL-103] S305 close-out — BL-103 repairs 1 and 2 done: `quality_ratchet.py` 1.4.0; the receipt is complete; the gate run read 18/18

A gate that outlives its budget reads `unmeasured` with `timeout (N s)` and may declare `timeout_seconds`; 1.3.0 read a timeout as `fail`, as `pass` or as a number read out of the timeout message. Done on the fork and sent nowhere. The gate in a clean `--no-local` clone of `3bcb63c`: 18/18, results `703856fabafb`, manifest `4ce1c4131646`. BL-107 opened (the timed-out command keeps running). `HANDOFFS.md` holds 3 receipts (S305, S304, S303) and `CHANGELOG.md` is near its trigger: offer both trims at the next Phase 0. The `HANDOFFS.md` receipt carries the rest; Phase 3C appended no fork learning row.

### 2026-10-12 · [BL-103] `BACKLOG.md`: BL-103 rewritten to what is open (repair 3); BL-107 opened, the timed-out command keeps running

Measured S305: the timeout kills the shell, not its children (`sleep 6`, `7` and `8` survive `run_gates` on both tools). `BACKLOG-DETAIL.md` carries both sections. Nothing sent upstream.

### 2026-10-12 · [BL-103] BL-103's record and the measurement script, with its output on the 1.3.0 and the 1.4.0 tool

`docs/planning/bl103-evidence/`: `bl103-record.md`, `measure-timeout.py` and `measure-timeout-output.txt`. The defect read `fail`, `pass` or a number read out of the timeout message, not only `exit 127`; the sync channels simulated (one file, byte-identical, legacy and `--layout new`); the old and the new tool equal over one manifest; the mutation rounds. Nothing sent upstream.

### 2026-10-12 · [BL-103] `.quality-gates.json`: `timeout_seconds` 3600 on `tests-sh-passed`, `tests-sh-failed` and `migrate-layout-unit-tests`

Not a threshold (none moved; `quality_ratchet.py` 1.4.0 warns on the three, refuses none, and `config_defects` reads none): the three gates that read `unmeasured` under load (S280, S287, S304) get an hour instead of the 600 s default. S287 measured 1,835 s (shell suite) and 794 s (migration suite); the price is that a suite that HANGS now holds a run for up to an hour. His figure, picked at the S305 Phase 4 picker. A separate commit so it reverts alone.

### 2026-10-12 · [BL-103] BL-103: a mutation round over `quality_ratchet.py` 1.4.0 and the tests it asked for; `ratchet-unit-tests` floor 95 to 100

22 mutants, `docs/planning/bl103-evidence/mutate-bl103.py` (run in a `--no-local` clone under `~/.cache`): 16 killed by the suite, 6 survived (the budget's `:g` format, a shared run's note, a command that cannot start, the 600 s default, an undeclared gate's default in a shared run, the memo's budget): each a behaviour no test named. Five tests added (100 OK, 95 before); round 2, with a 23rd mutant on a removed `timeout_seconds`, is recorded with the work.

### 2026-10-12 · [BL-103] `quality_ratchet.py` 1.4.0: a gate that outlives its budget is unmeasured, and a gate may declare `timeout_seconds`

`starter-kit/quality_ratchet.py` (distributed) 1.3.0 to 1.4.0: gate commands run through `run_gate_command`, which reports a timeout apart from an exit code, so a gate that outlives its budget is `unmeasured`, `measured: null`, note `timeout (N s)` in every shape (it read fail or pass at 127, or a number out of the timeout message); `timeout_seconds` per gate (validated, default 600; gates sharing a command run it once under the largest); `compare` warns, never refuses, on a changed one; `--selftest` observes it (25 to 28 checks); the seed's `_gate_schema` names it. 95 tests OK (81 before), the 1.3.0 `results` hash pin unchanged, `ratchet-unit-tests` floor 81 to 95. Fork only, nothing sent upstream. Not done: the kill of the timed-out command (a new row), repair 3 of BL-103.

### 2026-10-12 · [BL-103] BL-103: the ratchet's timeout, tests written RED first

`tools/test_quality_ratchet.py` gains 14 tests (81 to 95): 13 red for the intended reasons, one green pin by design (a five-gate run's `results` hash, `8498441c1165`, computed with the 1.3.0 tool). They show what the tool does today to a gate that outlives its budget: an exit-code floor of 100 reads **pass** at measured 127, a ceiling reads **fail** at 127, and an `extract` reads a number out of the timeout message (**pass**, measured 3, from the command line quoted in it); `ITERATIVE_METHODOLOGY.md:444` says checks never pass by timeout. His go-ahead at the S305 Phase 4 picker: repairs 1 and 2, orphan kill out (a new row), version 1.4.0, 3600 s on three of this repository's gates.

### 2026-10-12 · [BL-103] S305 claim (in progress) — the ratchet's timeout

CHANGELOG: pending. Operator said `go`; the Phase 0 report found no free adopter for BL-105 phase 4 and he picked BL-103 with two go-aheads, both done before this claim: the push of `c80c5b5` (`2c62927..c80c5b5`, `0 0`, `ls-remote` equal) and the HANDOFFS trim (`cd170f7`) with its fold (`c135916`). The gate citation re-run (clean `--no-local` clone of `c80c5b5`): 18/18, results `0ca51b2444cc`, manifest `5ba29f982c78`, equal to S304's. Deliverable: `quality_ratchet.py` reports a timeout as a timeout and a gate may declare `timeout_seconds` (repairs 1 and 2; repair 3 is not in it); fork only, nothing outward. Phase 3F records the rest.

### 2026-10-12 · [ad hoc] S305 — fold the third 2026-10-12 HANDOFFS shard pointer into the archive index

The pointer block the trim (`cd170f7`, 1 receipt, S302, to `HANDOFFS-through-2026-10-12-3.md`, the name S304 guessed and the dry run chose) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md`, in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S304, S303). The trim ran on his go-ahead at the S305 Phase 0 picker.

### 2026-10-12 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-12-3.md` (1 record(s), 40,834 B → 29,590 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-12 → 2026-10-12) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-12-3.md`](docs/archive/HANDOFFS-through-2026-10-12-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-12-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-12-3.md.verify.sh)
rather than trusting a digest printed here. Live file 40,834 B → 29,590 B (−27.5%).

### 2026-10-12 · [ad hoc] S305 — pushed `c80c5b5` to the fork's `main`

`origin/main` went `2c62927..c80c5b5` (10 commits) on his go-ahead at the S305 Phase 0 picker, naming the commit and not `HEAD`; read back: `ls-remote` equals `c80c5b5`, `rev-list --left-right --count origin/main...HEAD` read `0 0`. Fork only, nothing sent to `KJ5HST/methodology`.

### 2026-10-12 · [BL-101] S304 close-out — BL-105 build phase 3 done: the prose; the receipt is complete; the gate run read 18/18

Phase 3 of BL-105 is done on the fork and sent nowhere: `BOOTSTRAP.md` 218 and 222 and `CLAUDE_TEMPLATE.md` 83-84 say where `PROJECT_LEARNINGS.md` lives in either layout, and `bin/check-links:84`, which was code (F31), allows it beside `FRAMEWORK_LEARNINGS.md`. The gate in a clean `--no-local` clone of `35459ca`: 18/18, results `0ca51b2444cc`, manifest `5ba29f982c78`. `HANDOFFS.md` holds 3 receipts (S304, S303, S302): one trim is owed after the next Phase 0 report. The `HANDOFFS.md` receipt carries the rest; Phase 3C appended no fork learning row.

### 2026-10-12 · [BL-101] BL-105's state in the plan, the backlog row and its detail: the prose is written, phase 4 is not

`methodology-subdirectory-plan.md` status line (same byte count, 59,994 of 60,000 B), `BACKLOG.md` row BL-105 and a new S304 paragraph in `BACKLOG-DETAIL.md`: build phase 3 done on the fork (`BOOTSTRAP.md` 218 and 222, `CLAUDE_TEMPLATE.md` 83-84, `bin/check-links` as code, F31), nothing sent; the next phase is the adopters (phase 4). The row stays open: phase 4 is not started.

### 2026-10-12 · [BL-101] BL-105 build phase 3: the record, the mutation script and the register

`docs/planning/methodology-subdirectory-evidence/bl105-phase3-record.md` (the inventory and what each of the six sites became, the sync channels, what was not run), `mutate-bl105-phase3.py` (9 mutants of the `bin/check-links` change, 9 killed; refuses a path outside `~/.cache`) and the findings register: row F31 (`bin/check-links:84` was code), F29 and F30 set to fixed (S303 built them; the rows still read open), and the S304 log line. Gate run in a clean `--no-local` clone of `69fe69a`: 18/18, results `0ca51b2444cc`, manifest `5ba29f982c78`.

### 2026-10-12 · [BL-101] BL-105 build phase 3: the distributed prose says where `PROJECT_LEARNINGS.md` lives in either layout

`starter-kit/BOOTSTRAP.md` (the Step 5 paragraph, lines 218 and 222) and `starter-kit/CLAUDE_TEMPLATE.md` (the comment at 83-84) said the file sits "at your project root" and "needs no tooling changes": both false for a project in the `methodology/` layout, where `bin/migrate-layout` moves it with the methodology files and rewrites the `CLAUDE.md` pointer (275 tests). They now say "beside `FRAMEWORK_LEARNINGS.md`" (the project root, or `methodology/`), that the pointer names the file where it lives, and what the tool does. No line count changes in either file. Lines 220 and 439 name the file bare and stay (the bare-name rule, `BOOTSTRAP.md:68`). Fork only; nothing sent to `KJ5HST/methodology`.

### 2026-10-12 · [BL-101] BL-105 build phase 3: `bin/check-links` allows the companion where the layout keeps it

`bin/check-links` listed `PROJECT_LEARNINGS.md` among the project's files at its root "in either layout", which plan D10 made false: the file moves with the project. It is now `COMPANION_FILES`, allowed-absent beside `FRAMEWORK_LEARNINGS.md` (`beside_in`, one helper that `placeholder_in` now shares), the root in the legacy layout and `methodology/` in the new one; a link up to the root dangles there. The RED test (`4ea9ce9`) is green, `tools/test_sync_layouts.py` reads 82 tests OK in 95 s, `check-links --layout both` and `check-layout-literals` exit 0, and the gate floor `sync-layout-unit-tests` rises 81 to 82. No link to the file exists in a distributed document today, so no output changed.

### 2026-10-12 · [BL-101] BL-105 build phase 3: `bin/check-links`' test, written RED first

`tools/test_sync_layouts.py` gains `test_a_companion_of_the_move_is_allowed_absent_beside_the_runner_in_each_layout` (class `TestCheckLinksSimulatesBothLayouts`): a link to `PROJECT_LEARNINGS.md` beside the runner passes in the legacy layout and, per plan D10, in the new one, where a link up to the root does not. It fails today at the new-layout sibling link (exit 1, not 0): `bin/check-links` allows the file at the project root only. The floor `sync-layout-unit-tests` (81) rises with the fix, not here.

### 2026-10-12 · [ad hoc] S304 — reconcile S303's receipt `commit:` slot to a sha `check-handoff` accepts

S303 wrote `6583022`, all decimal digits, which `bin/check-handoff` does not read as a sha (no hex letter). The check exempts the newest receipt, so Phase 0 read OK and the claim stub of S304 turned it red. The slot now reads `65830220967e`, the same commit (`git rev-parse --short=12`), as S254 did for S253 (`d45afa4`); `HANDOFFS.md` is the only file changed besides this entry.

### 2026-10-12 · [BL-101] S304 claim (in progress) — BL-105 build phase 3, the distributed prose

CHANGELOG: pending. Operator said `go`; the Phase 0 report found no free adopter for P18 and he picked BL-105 phase 3 with two go-aheads, both done before this claim: the push of `2c62927` to the fork `origin` (`ed1bd64..2c62927`, `0 0`, `ls-remote` equal) and the HANDOFFS trim (`f40a8a7`) with its fold (`14ebfee`). The gate citation re-run (clean `--no-local` clone of `2c62927`): 17/18 pass, 0 fail, 1 unmeasured, the migrate-layout suite past the ratchet's 600 s under a load average of about 180 (BL-103); by hand it read 275 tests OK in 675.9 s. Deliverable: the prose in `starter-kit/BOOTSTRAP.md`, `starter-kit/CLAUDE_TEMPLATE.md` and `bin/check-links`; fork only, nothing outward. Phase 3F records the rest.

### 2026-10-12 · [ad hoc] S304 — fold the second 2026-10-12 HANDOFFS shard pointer into the archive index

The pointer block the trim (`f40a8a7`, 1 receipt, S301, to `HANDOFFS-through-2026-10-12-2.md`, the name S303 guessed and the dry run chose) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (trimmer v1.8.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S303, S302). The push of `2c62927` to the fork and the trim ran on his go-aheads at the S304 Phase 0 picker; `origin/main` read back equal.

### 2026-10-12 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-12-2.md` (1 record(s), 40,012 B → 29,200 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-12 → 2026-10-12) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-12-2.md`](docs/archive/HANDOFFS-through-2026-10-12-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-12-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-12-2.md.verify.sh)
rather than trusting a digest printed here. Live file 40,012 B → 29,200 B (−27.0%).

### 2026-10-12 · [BL-101] S303 close-out — BL-105 build phase 2 done; the receipt is complete

Phase 3 done: S302's handoff scored 9 (3A), this session 8 (3B); no fork learning row appended (3C: considered fork #64, #39, #57 and #94, so no retirement is owed). The `HANDOFFS.md` receipt is `complete`; the gate run in a clean `--no-local` clone of `6583022` read 18/18, results `101c83d0550f`, manifest `ab44a53d126c` (the floor rose, so the hashes differ from S302's). Operator actions this session, each read back: the push of `ed1bd64` to the fork, the HANDOFFS trim. Next: phase 3 (the distributed prose) or P18, and one trim owed after the next Phase 0 (3 receipts).

### 2026-10-12 · [BL-101] S303 — BL-105's state in the plan, the backlog row and its detail: the tool is built (phase 2)

The plan's status line reads "BL-105: B stands, tool built (D10, S303)" (59,994 of its declared 60,000 B, 1 B under); the BL-105 row and its detail gain the S303 paragraph (the tool, the 39 tests, the five clones, the one call left: a top-up at a tree with a locally modified TRACKED file). BL-105 stays open: phases 3 (the distributed prose) and 4 (the adopters) are not started.

### 2026-10-12 · [BL-101] S303 — BL-105 build phase 2: the record, the five adopters' results, the mutation script and the register line

`docs/planning/methodology-subdirectory-evidence/bl105-phase2-record.md` (what was built, the five `--no-local` clones, what the run found, his one call), `bl105-phase2-runs.json` (the five results as data), `mutate-bl105-phase2.py` (32 distinct mutants; refuses to run in the tree it mutates) and a dated S303 line in `findings-register.md` (F29 fixed, F30 answered and built, F7 and F19 seen again at the live `nprcgenekeepr`).

### 2026-10-12 · [BL-101] S303 — BL-105 build phase 2: `bin/migrate-layout` takes the companion, tops up a migrated tree, reads the configs where the layout puts them and lists the live links (F29, F30)

`PROJECT_LEARNINGS.md` moves with tier 2 and `all` when git tracks it; a run whose only move is that file is a top-up (its own ledger heading and commit subject); the two configs are read under `methodology/` in a migrated tree; every link in a live Markdown document to a file the run moves is listed in `live_links` and none is rewritten (his call, F30). `tools/test_migrate_layout.py` reads 275 tests (236 before; the 39 new were written RED first) and passes in full; `.quality-gates.json` `migrate-layout-unit-tests` floor 236 to 275 (a tightening, `quality_ratchet.py --precommit` exits 0); `bin/check-layout-literals` reads 0 sites. A mutation round (32 distinct mutants): 31 killed on the first run, 1 after a tier-1 test. The built tool run in `--no-local` clones of the five adopters that track the file: all five apply, the tool's own checks read no difference. Record: `docs/planning/methodology-subdirectory-evidence/bl105-phase2-record.md` (next commit).

### 2026-10-12 · [BL-101] S303 — BL-105 build phase 2: the tests, written RED first

`tools/test_migrate_layout.py` gains 35 tests in five classes (the companion rule, a top-up on a migrated tree, the pure link rules, F30's live-link list, a project with no methodology), seen failing for the intended reasons before any code: 27 red (no companion move, no `live_links` key, the configs not read under `methodology/`), 8 already green because they pin behavior that must stay (tier 1 leaves the file, a dirty tree refuses, nothing to do without the file). The tool is not yet changed.

### 2026-10-12 · [BL-101] S303 claim (in progress) — BL-105 build phase 2, the tool

CHANGELOG: pending. Operator said `go`; the Phase 0 report found no free adopter for P18 (`wsfct` and `mts-system`, the two left, both have a live session) and he picked BL-105 phase 2 with F30 answered LIST ONLY and two go-aheads, both done before this claim: the push of `ed1bd64` to the fork `origin` (`e5d88a5..ed1bd64`, `0 0`, `ls-remote` equal) and the HANDOFFS trim (`882a7bd`) with its fold (`85ac33d`). The gate citation re-run (clean `--no-local` clone of `ed1bd64`, `~/.cache/s303-gate`) was still running at this claim: its result goes in the close-out receipt. Deliverable: the tool, tests first; nothing distributed, no adopter touched. Phase 3F records the rest.

### 2026-10-12 · [ad hoc] S303 — fold the 2026-10-12 HANDOFFS shard pointer into the archive index

The pointer block the trim (`882a7bd`, 1 receipt, S300, to `HANDOFFS-through-2026-10-12.md`, the name S301 and S302 guessed and the dry run chose) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (trimmer v1.8.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S302, S301). The push of `ed1bd64` to the fork and the trim ran on his go-aheads at the S303 Phase 0 picker.

### 2026-10-12 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-12.md` (1 record(s), 39,402 B → 28,283 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-12 → 2026-10-12) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-12.md`](docs/archive/HANDOFFS-through-2026-10-12.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-12.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-12.md.verify.sh)
rather than trusting a digest printed here. Live file 39,402 B → 28,283 B (−28.2%).

### 2026-10-12 · [BL-101] S302 close-out — BL-105 rehearsed (build phase 1): B stands; the receipt is complete; the gate run read 18/18

The `HANDOFFS.md` receipt is `status: complete` (self 8, predecessor S301 scored 9). Gate: `quality_ratchet.py --run` in a clean `--no-local` clone of `de05df7` read 18/18, results `8c209fa9806e`, manifest `440ab037cfe1`, S301's own figures (this session changed no code, test or gate). No fork learning row appended (D3: considered fork #57, #94, #16, #23). Nothing built; nothing pushed beyond the granted `e5d88a5`; BL-105 stays open at build phases 2 to 4; register rows F25 to F30 open.

### 2026-10-12 · [BL-101] S302 — BL-105's state in the plan (D10, status line: 59,995 of its 60,000 B), the backlog row and its detail

Plan status line and D10 row say rehearsed S302, B stands (net +3 B, so no cut was owed; no gate holds the budget, BL-106); `BACKLOG.md` row BL-105 and a new S302 paragraph in `BACKLOG-DETAIL.md`. BL-105 stays open: build phases 2 to 4 are not started.

### 2026-10-12 · [BL-101] S302 — BL-105 rehearsed (build phase 1): the record, and register rows F25 to F30

`bl105-rehearsal-record.md`: the companion move simulated with `bin/migrate-layout`'s own rewrite and check functions in `--no-local` clones of `nprcgenekeepr`, `mts-system` and `model_project_constructor`; **B stands**. `nprcgenekeepr` unchanged (11,163 tests equal, tarball 3,784,543 B to 3,784,545 B) but for one uncovered script; `mts-system`'s archiver fails on the real tree with its tests green; `model_project_constructor` 2 tests red and 26 skipped until 3 lines are edited. 6 files edited in 3 adopters, against the census's 5. Register rows F25 to F30, all open, and a dated line. Nothing built, no real tree written, nothing outward.

### 2026-10-12 · [BL-101] S302 — BL-105 rehearsal: the raw outputs and driver results of model_project_constructor

`mpc-driver.json` and `mpc-raw.txt` in `bl105-runs/`, clones at `ec23bc7`. The `mpc-full-*` sections are the first full-suite attempts, aborted by `-x` on a missing `sqlalchemy` in the system Python (the same in base and edit); the `mpc-all-*` ones are the runs that count, with the project's own `.venv` and `PYTHONPATH` set to the clone's `src` (without it the venv imports the real tree).

### 2026-10-12 · [BL-101] S302 — BL-105 rehearsal: the raw outputs and driver results of nprcgenekeepr and mts-system

Each adopter's driver run (the tool's own list for the move, the tool's checks before and after, the rewrites) is one JSON and its raw outputs (hand-edit patch, queue script, test and gate outputs) one text, in `bl105-runs/`: `npr-driver.json` and `npr-raw.txt`, `mts-driver.json` and `mts-raw.txt`. The clones were under `~/.cache/bl105-rehearsal` (F23), at `5cacf61` and `d1cf54f`; nothing in either real tree was touched.

### 2026-10-12 · [BL-101] S302 — BL-105 rehearsal: the two scratch drivers and the link count

`bl105-companion.py` applies the one companion mapping (`PROJECT_LEARNINGS.md` to `methodology/PROJECT_LEARNINGS.md`) through `bin/migrate-layout`'s own rewrite and check functions in a clone it is given (it builds nothing in the tool and commits nothing); `bl105-links.py` counts the markdown links to the file by where each lands, which `check-links` does not (it read the same project-link count before and after in every arm). `links-by-arm.txt` is its output over the six control and move clones.

### 2026-10-12 · [BL-101] S302 claim (in progress) — BL-105 build phase 1, the rehearsal

CHANGELOG: pending. Operator said `go`; the Phase 0 report found no free adopter for P18 (four live sessions; `Philippians`, `dalia_martinez_funeral`, `claude_work` dirty) and he picked the BL-105 rehearsal with two go-aheads, both done before this claim: the push of `e5d88a5` to the fork `origin` (`1dfc8b2..e5d88a5`, `0 0`, `ls-remote` equal) and the HANDOFFS trim (`1edb038`) with its fold (`f00e563`). S301's gate citation re-run in a clean `--no-local` clone of `e5d88a5`: 18/18, results `8c209fa9806e`, manifest `440ab037cfe1`, the citation's own figures. Deliverable: one rehearsal record, nothing built. Phase 3F records the rest.

### 2026-10-12 · [ad hoc] S302 — fold the fifth 2026-10-11 HANDOFFS shard pointer into the archive index

The pointer block the trim (`1edb038`, 1 receipt, S299, to `HANDOFFS-through-2026-10-11-5.md`, the name S301's handoff guessed and the dry run chose) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (trimmer v1.8.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S301, S300). The trim ran on his go-ahead at the S302 Phase 0 picker.

### 2026-10-12 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-11-5.md` (1 record(s), 37,904 B → 28,158 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-11 → 2026-10-11) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-11-5.md`](docs/archive/HANDOFFS-through-2026-10-11-5.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-11-5.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-11-5.md.verify.sh)
rather than trusting a digest printed here. Live file 37,904 B → 28,158 B (−25.7%).

### 2026-10-12 · [BL-101] S301 close-out — BL-105 decided (option B); the receipt is complete; the gate run read 18/18

Phase 3 done: S300's handoff scored 9 (3A), this session 8 (3B); no fork learning row appended (3C: considered fork #34, #57, #23 and the distributed #12; the lesson is BL-106, a gate). The `HANDOFFS.md` receipt is `complete` and `check-handoff` exits 0; the gate run in a clean `--no-local` clone of `0b496b8` read 18/18, 0 fail, 0 unmeasured, results `8c209fa9806e`, manifest `440ab037cfe1` (equal to S300's, as no code, test or gate changed). A HANDOFFS trim is owed again after the next Phase 0 (3 receipts: S301, S300, S299). Pushed this session: `1dfc8b2` to the fork only; 7 commits ahead of `origin/main` after this one, a push is his call.

### 2026-10-12 · [BL-106] S301 — the plan's declared 60,000 B has no gate: a backlog row

Found while amending the plan for D10: the declared budget is held by hand (S300 cut it back in `1dfc8b2` after a gate run that read 18/18 with the plan at 60,107 B). `BL-106` in `BACKLOG.md` and `BACKLOG-DETAIL.md` names the two shapes (a byte-count gate, or the file in `.context-budget.json`) and builds neither; the choice, and whether the figure is a limit or a price, is his. Not a fork learning row: a mechanical invariant is a gate (runner Phase 3C).

### 2026-10-12 · [BL-101] S301 — BL-105 decided: option B, `PROJECT_LEARNINGS.md` joins the `methodology/` set as a companion of the move (plan D10)

His pick at the S301 Phase 0 picker, the recommended one; A (stay at the root) and C (also `BACKLOG.md`, `CONTEXT.md`) not taken. Plan §1 and a new D10 row say so, shortened elsewhere to stay under its declared 60,000 B (59,992 B); `bl105-record.md` §5 holds his answer and four build phases (a rehearsal first, which can withdraw B); the backlog row BL-105 reads DECIDED with the build open, and BL-101's row no longer calls BL-105 his open call. Nothing built; no tool, distributed document or adopter touched; D8 untouched; nothing outward.

### 2026-10-12 · [BL-101] S301 — BL-105 evidence record written (the answer is his, next)

`docs/planning/methodology-subdirectory-evidence/bl105-record.md`: the census of `PROJECT_LEARNINGS.md` over the 12 adopters (5 carry it; 14 path literals: 3 config rewrites, 6 already hold, 5 hand edits), his two questions answered with evidence, four costed options (A keep, B companion of the move, B-manifest, C wider), and what was not run (no rehearsal). Read-only: no tool, distributed document or adopter changed. His answer is §5, recorded after the picker.

### 2026-10-12 · [BL-101] S301 claim (in progress) — BL-105, whether `PROJECT_LEARNINGS.md` joins the `methodology/` set

CHANGELOG: pending. Operator said `go`; the Phase 0 report found no free adopter for P18 (`wsfct`, `mts-system` and `nprcgenekeepr` have a live session; `Philippians` 4 dirty lines, `dalia_martinez_funeral` 6, `claude_work` no commit) and he picked the BL-105 decision with two go-aheads, both done before this claim: the push of `1dfc8b2` to the fork `origin` (`0 0`, `ls-remote` equal) and the HANDOFFS trim (`b578fd8`) with its fold (`c76af16`). S300's gate citation re-run in a clean `--no-local` clone of `608c7b9`: 18/18, results `8c209fa9806e`, manifest `440ab037cfe1`, the citation's own figures. Deliverable: one decision record, nothing built. Phase 3F records the rest.

### 2026-10-12 · [ad hoc] S301 — fold the fourth 2026-10-11 HANDOFFS shard pointer into the archive index

The pointer block the trim (`b578fd8`, 1 receipt, S298, to `HANDOFFS-through-2026-10-11-4.md`, the name S300's handoff guessed and the dry run chose) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (trimmer v1.8.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S300, S299). Both ran on his go-ahead at the S301 Phase 0 picker; the push of `1dfc8b2` to the fork came first and was read back (`0 0`, `ls-remote` equal).

### 2026-10-12 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-11-4.md` (1 record(s), 38,821 B → 27,092 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-11 → 2026-10-11) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-11-4.md`](docs/archive/HANDOFFS-through-2026-10-11-4.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-11-4.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-11-4.md.verify.sh)
rather than trusting a digest printed here. Live file 38,821 B → 27,092 B (−30.2%).

### 2026-10-12 · [BL-101] S300 — the plan back under its declared budget

`methodology-subdirectory-plan.md` declares 60,000 B (its header); the F21 edits of `c053cac` took it from 59,973 to 60,107 B. The two edits are shortened (the status line and the P16 text: F21 is fixed, the record is named in the register), 59,998 B. No gate reads this figure; the plan's own header does. Found by `context_budget.py --status` and a `wc`, after the close-out. Model: Claude Sonnet 5.5.

### 2026-10-12 · [BL-101] S300 close-out — F21 done and recorded; the receipt is complete; the gate run read 18/18

The S300 receipt in `HANDOFFS.md` is `status: complete` (self 7, predecessor 9): F21 is fixed in `bin/migrate-layout` (`72a5921`), 16 tests and the floor at 236, the rule agrees with markdown-it over 6,367 committed ledger texts, the old tool put the entry inside the fence on the real adopter and the new one does not, two mutation rounds (28 runs of 26 mutants, none alive at the end). Gate run in a clean `--no-local` clone of `608c7b9`: 18/18, 0 unmeasured, results `8c209fa9806e`, manifest `440ab037cfe1`. Phase 3C appended no fork learning row (D3 not triggered; #16, #57 and #94 considered). The receipt owns three mistakes: the mutation runner pointed at the working repository, a wrong test count in `72a5921`'s entry, three runs of one script. Nothing went upstream; `origin/main` is `ca2a653`, 12 commits behind `HEAD`. Model: Claude Sonnet 5.5.

### 2026-10-12 · [BL-101] S300 — F21: the floor of `migrate-layout-unit-tests` 220 → 236

`.quality-gates.json`: the suite reads `Ran 236 tests` (220 before; 16 new: 14 on the pure rule, 2 on the command), counted by loading the module and then taken from the gate run in a clean clone (cited in the receipt). A tightening: the hook accepts it. `tests-sh-passed` is not raised: `bin/tests.sh` runs two classes of this file as one pre-check test. Model: Claude Sonnet 5.5.

### 2026-10-12 · [BL-101] S300 — F21: recorded in the plan and the backlog

`methodology-subdirectory-plan.md` (status line and the P16 text now say the tool is fixed), `BACKLOG.md` (the BL-101 index row: F21 off the triage list), `BACKLOG-DETAIL.md` (Next action: F21 fixed, the clause that sent a session to read a ledger header for it removed, the S300 Phase 0 state of the adopters added: none free). Model: Claude Sonnet 5.5.

### 2026-10-12 · [BL-101] S300 — F21: the record and the register row

`f21-fenced-example-record.md` (the problem, the rule and the sibling readers it was read from, the change, what was measured, what it does not show, how to reproduce) and `findings-register.md`: row F21 now reads fixed with its evidence, a dated S300 line, and the read-at-next-session paragraph no longer sends a session to move an entry by hand. The row and the record state the test accounting as it was (ten tests before the code, six after). Model: Claude Sonnet 5.5.

### 2026-10-12 · [BL-101] S300 — F21: the red run and the outputs of two mutation rounds

`f21-red-run-output.txt` (the first ten tests, run before the code: 9 red, 1 green by design), `f21-mutation-round-1.txt` (22 mutants of `first_heading` and `insert_entry` in a scratch clone of `72a5921`: 20 killed, 2 alive, F06 and C03 with one cause, a nested-fence fixture that closed its own fence by coincidence) and `f21-mutation-round-2.txt` (a scratch clone of `3b2390e`: the two re-run and four behaviours round 1 did not name, 6 of 6 killed). F05, the `^` of the fence pattern, is an equivalent mutant (`re.match` anchors) and was not run. Model: Claude Sonnet 5.5.

### 2026-10-12 · [BL-101] S300 — F21: the output of the differential and of the adopter check, from a clean clone

`f21-differential-output.txt` and `f21-adopter-check-output.txt`, both run from a `--no-local` clone of `0010021` (the tool under test). **Differential:** 6,361 distinct committed versions of a ledger in 14 repositories and 6 seed blobs, **0 disagreements with markdown-it**; the old rule landed inside a block in `chat_verification` (35 of 35 versions), `wsfct` (106 of 625, none at its `HEAD`) and 1 of the 6 seed blobs; no header region holds a tilde fence, a fence of four backticks, an indented fence, a fence in a quote or list, or a heading in an HTML comment, and none holds a fence that never closes; 20,000 random texts: 19,465 agree, 535 disagree and each holds an out-of-scope construct, 0 in scope, 512 of 512 fence-free texts give the old answer. **Adopter check:** `chat_verification` at `a3174b3`, the tool before the change (`ca2a653`): entry at line 48, inside a fence; the tool under test: line 183, marker at 181, outside; `check-ledger` 83 findings in both and in the hand-corrected ledger. Model: Claude Sonnet 5.5.

### 2026-10-12 · [BL-101] S300 — F21: the scripts of the evidence (differential, mutants, adopter check)

`f21-differential.py` (the rule against markdown-it over every committed ledger version on this machine and 20,000 random texts), `f21-mutants.py` (22 mutants of round 1; `F21_ROUND=2` selects round 2, six) and `f21-adopter-check.sh` (the tool before and after the change, a real `--apply`, in clones of `chat_verification`). **A correction to the entry of `72a5921` above:** it says "15 new, 14 red before the code"; ten tests were written before the code (9 red, 1 green by design) and six after it. The outputs follow in their own commits. Model: Claude Sonnet 5.5.

### 2026-10-12 · [BL-101] S300 — F21: two tests after the first mutation round

Round 1 (22 mutants of `first_heading` and `insert_entry`, run in a scratch clone of `72a5921`) killed 20 and left two alive, F06 (the opener's length forgotten) and C03 (any length closes): the nested-fence test closed its own fence by coincidence, because its inner pair of 3-backtick lines re-opened one over the heading. Its fixture now holds an unbalanced inner line, so a shorter line closing a longer fence is seen; one test added for an opener that carries an info string (round 2 names it). `test_migrate_layout.py`: 16 tests in the fence group. Model: Claude Sonnet 5.5.

### 2026-10-12 · [BL-101] S300 — F21: `bin/migrate-layout` places its ledger entry above the first heading outside a fenced block

`insert_entry` now takes its position from `first_heading`, which reads fences as `methodology_trim.py`'s `fence_scan` does (three or more backticks or tildes at the start of a line open one; only the same character, at least as long and bare, closes it), so an example heading in a ledger header's fence is no longer taken for the first entry (register row F21: `chat_verification`, entry at line 48 inside the fence). A fence that never closes before any heading outside one is refused as `rewrite-unsafe` (nothing written). Tests first: 15 new (13 on the pure rule, 2 on the command), 14 red before the code and 1 green by design. Not yet: the evidence scripts, the mutation rounds, the floor, the register row. Model: Claude Sonnet 5.5.

### 2026-10-12 · [BL-101] S300 claim (in progress) — F21, `bin/migrate-layout` skips fenced code when it places its ledger entry

CHANGELOG: pending. Operator said `go`; the Phase 0 report found no free adopter for P18 (`wsfct`, `mts-system` and `nprcgenekeepr` have a live session; `Philippians` has 4 dirty lines, `dalia_martinez_funeral` 6, `claude_work` 16), and he picked "F21 tool fix" with two go-aheads (one picker answer): "Run the owed HANDOFFS trim" and "Push ca2a653 to the fork"; both were done before this claim (trim `9b03629`, fold `973e366`, push below). The gate citation of S299 (results `9926bd8b4a1b`, manifest `af0d6dc16337`) was re-run in a clean `--no-local` clone of `ca2a653` and confirmed (18/18, 0 unmeasured). Deliverable: ONE change to `bin/migrate-layout` (canonical-only), tests first, following `workstreams/DEVELOPMENT_WORKSTREAM.md`: `insert_entry` places the tool's one ledger entry above the first dated heading outside a fenced code block (register row F21: chat_verification's ledger header holds an example heading in a fence and the entry landed inside it). Not in scope: P18, BL-105, F6, F8, F13, F14, F17, F19, anything upstream. Model: Claude Sonnet 5.5.

### 2026-10-12 · [ad hoc] S300 — pushed `ca2a653` to the fork `origin` (push record)

On his go-ahead at the S300 Phase 0 (a picker answer: "Push ca2a653 to the fork"): `git push origin ca2a653:refs/heads/main`, naming the commit and not `HEAD`; `origin` is `https://github.com/rmsharp/methodology.git`, the fork. Eleven commits went (`799ecc1`, `ffbfbc5`, `f2978a3`, `e00b2b2`, `e48a9f5`, `08349d8`, `4aaecd0`, `49880e1`, `15be71a`, `280f0ca`, `ca2a653`; `0a3558c..ca2a653`). Checked first: `ca2a653` is a fast-forward of `origin/main`. Read back after: `git rev-list --left-right --count origin/main...ca2a653` read `0 0` and `git ls-remote origin refs/heads/main` equalled `ca2a653`. The two later local commits (`9b03629` trim, `973e366` fold) were not pushed: the go-ahead named `ca2a653`. Nothing went upstream (`KJ5HST/methodology`), no tag, no release. Model: Claude Sonnet 5.5.

### 2026-10-12 · [ad hoc] S300 — fold the third 2026-10-11 HANDOFFS shard pointer into the archive index

The pointer block the trim (`9b03629`, 1 receipt, S297, to `HANDOFFS-through-2026-10-11-3.md`, the name S299's handoff guessed and the dry run chose) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (trimmer v1.8.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S299, S298). The shard proof exits 0 in the tree and from a `--no-local` clone of `9b03629`.

### 2026-10-12 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-11-3.md` (1 record(s), 39,344 B → 27,710 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-11 → 2026-10-11) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-11-3.md`](docs/archive/HANDOFFS-through-2026-10-11-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-11-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-11-3.md.verify.sh)
rather than trusting a digest printed here. Live file 39,344 B → 27,710 B (−29.6%).

### 2026-10-12 · [BL-101] S299 close-out — F24 done and recorded (receipt complete)

Receipt S299 is `status: complete` (self 8, predecessor 9; no fork learning row appended, so no retirement is owed: the rows considered are named in the receipt, fork #57, #94 and #16). `CHANGELOG: pending` on the S299 claim entry is cleared by this statement (a committed entry is not edited). **The deliverable:** F24, `bin/migrate-layout` reads a tracked root `.vscodeignore` as vsce 3.9.2 reads it; the entries above this one have the figures. **Gate run:** `quality_ratchet.py --run` in a clean `--no-local` clone of `280f0ca`, 18/18 pass, 0 fail, 0 unmeasured, results `9926bd8b4a1b`, manifest `af0d6dc16337` (the manifest moved because the floor of `migrate-layout-unit-tests` rose to 220, which it reads); `tests-sh-passed` 483, failed 0. **Ledgers:** `HANDOFFS.md` holds 3 receipts (S299, S298, S297), so one trim is owed after the next Phase 0 (one record, S297); `CHANGELOG.md` is 148,817 B before this entry against its 196,608 B trigger. **Pushed at his go-ahead before the claim:** `0a3558c` to the fork `origin` and `vscode_quarto_ext`'s three commits to its own `origin/master`; **local commits here, not pushed:** `799ecc1`, `ffbfbc5`, `f2978a3`, `e00b2b2`, `e48a9f5`, `08349d8`, `4aaecd0`, `49880e1`, `15be71a`, `280f0ca` and this close-out; nothing went upstream, no tag. **Open and his:** BL-105, P18 (no free adopter; read `wsfct`'s `.vercelignore` dialect first), whether the tool should refuse, the F21 tool fix, F6, F8, F13, F14, F17, F19, D8. Model: Claude Sonnet 5.5.

### 2026-10-12 · [BL-101] S299 — F24 recorded in the plan and the backlog

Plan `docs/planning/methodology-subdirectory-plan.md`: the status line now says P18 is next and F24 is fixed (it said F24 first unless he said otherwise), §7.4g's findings line says F24 fixed; the plan is 59,973 of 60,000 B. `docs/planning/BACKLOG.md` BL-101 row: the P17 clause says F24 was found and is fixed (S299), a new clause says what the tool names (36 of 36 files at tier all, 23 at tier 1, none once the adopter's line is in, the same as real `vsce ls`), the Next clause says that at S299's Phase 0 no adopter was free (three had a session, three were dirty or empty) and that `vscode_quarto_ext`'s three commits were pushed; the file is 56,711 of 56,750 B. `docs/planning/BACKLOG-DETAIL.md`: a paragraph for F24 FIXED with the measurements, the Next action without F24 and without the push as a call of his, and without the F24 call. BL-101 stays open (P18 and the rest). Nothing in the tool changed. Model: Claude Sonnet 5.5.

### 2026-10-12 · [BL-101] S299 — F24: the record, and the register row closed

The record `docs/planning/methodology-subdirectory-evidence/f24-vscodeignore-record.md` (what vsce does, read and run; the change; what was measured; what the list cannot show; how to reproduce) and the register: row F24 now reads **fixed** (S299), a dated line says what the tool now names (36 of 36 at tier all, 23 of 23 at tier 1, 0 once the adopter's line is in) and what stays open, and the read-first paragraph lists F24 among the fixed rows. **What stays open, named in both:** the rule is for one repository (only `vscode_quarto_ext` tracks a root `.vscodeignore` here); `wsfct` tracks a `.vercelignore` that the tool lists and never judges, so the next adopter with a pattern list of its own is this finding's second instance unless its dialect is read first; a refusal was not built (F10 listed; changing that is his). Nothing in the tool changed. Model: Claude Sonnet 5.5.

### 2026-10-12 · [BL-101] S299 — F24: the mutants and the two rounds' outputs (evidence, no tool change)

`docs/planning/methodology-subdirectory-evidence/f24-mutants.py` holds 49 mutants of `bin/migrate-layout`, one per behaviour F24 added (brace lists, one segment, a whole glob, vsce's list, the exposure, the wiring and the text), and `ROUND2`, 14 aimed at behaviours round 1 did not name; it runs under `mutate-p7.py` against a scratch clone, with the baseline green first. The outputs are `f24-mutation-round-1.txt` (written in two parts, and S10 run alone because I left it out of both id lists by mistake; its header says what each part found) and `f24-mutation-round-2.txt`. **62 of 63 distinct mutants killed**; the survivor, L16, is equivalent. Two things round 1 found and fixed in the tests: no test used a list of three braces (B04) and none used a file that a `#` line would cover if it were read as a pattern (L01, killed in round 2). The same commit rewrites `f24-adopter-check-tall-dry-run.txt`, which the previous commit saved with its last line cut at 400 characters by a `cut` I left in; the file now holds the whole line. Nothing in the tool changed. Model: Claude Sonnet 5.5.

### 2026-10-12 · [BL-101] S299 — F24: the check on the adopter it came from (script and output, no tool change)

`docs/planning/methodology-subdirectory-evidence/f24-adopter-check.sh` clones `vscode_quarto_ext` at `507b9348` (the commit before P17) three times with `--no-local` under a path without the word `scratchpad` (F23), syncs each without `--force`, then for each: `vsce ls` before, the tool's dry run as JSON, a real `--apply`, `vsce ls` after, and the comparison of the files the tool names against the moved files vsce did not list at their old place and lists at the new one (`f24-adopter-check-output.txt`; the dry run's text for the `.vscodeignore` row is `f24-adopter-check-tall-dry-run.txt`). **Tier 1: 42 paths before, 65 after, the tool names 23 and vsce 23, the same 23. Tier all: 42 before, 78 after, 36 and 36, the same 36. With the adopter's own `methodology/**` line committed first (tier all): 42 and 42, 0 and 0.** The 42, 65 and 78 are the figures P17 read from the project's own `check-package`. `.gitattributes`, which vsce's default list ignores at the root, is one of the 36 and appears as `vsce's default list: .gitattributes`. The count in the text (`23 line(s) cover 38 moved file(s)`) is the tool's map, not the disk: `dashboard.html` and `.quality-gates-results.json` are in it and not in a clone (F10's limit 6). Nothing was run in the real tree, nothing pushed. Model: Claude Sonnet 5.5.

### 2026-10-12 · [BL-101] S299 — F24: the oracle and the differential, the scripts and their outputs (evidence, no tool change)

`docs/planning/methodology-subdirectory-evidence/f24-oracle.py` runs the 67 pinned `(pattern, path, answer)` rows of the test table through the real minimatch 10.2.5 with `{ dot: true }` (the call vsce 3.9.2 makes): 67 of 67 agree (`f24-oracle-output.txt`). `f24-differential.py` has three parts and ran at seeds 24, 7 and 99, 300 random files each (`f24-differential-output.txt`): **A** the glob matcher against minimatch over about 6,100 generated patterns (the adopter's own lines and vsce's default list among them) times 260 paths plus about 41,000 pattern-built paths per seed, 4.76 million pairs in all, 0 differ; the 16 patterns it does not read are all of the named shapes; **B** the whole list handling against `vsce ls --no-dependencies` for 900 random `.vscodeignore` files over a 41-file tree (comments, blanks, padding, `\r\n` and lone `\r`, a byte order mark, negations before and after the line they undo, directory names, brace lists, bracket classes), 0 differ; **C** the tool's 32-entry default list and its two appended negations against vsce's source, identical in order. A first run of B differed on one file: my test tree held `DOCS/a.md` beside `docs/`, which this case-insensitive filesystem folds into one directory, so vsce listed `docs/a.md`; the entry was removed from the tree and the run repeated (a defect of the instrument, not of the tool). A first run of A's pattern-built paths differed on paths with a `.` or `..` segment, which no listing holds and minimatch treats specially; the generator was restricted. Nothing in the tool changed. Model: Claude Sonnet 5.5.

### 2026-10-12 · [BL-101] S299 — F24: two mutation rounds, four more tests and the floor at 220 (corrects the entry below)

The entry below (commit `e00b2b2`) says 32 new tests and a floor of 218; both were true when it was written and are not the end state. **Mutation, 63 distinct mutants** (`f24-mutants.py`, a scratch `--no-local` clone, `f24-mutation-round-1.txt` and `-2.txt`): round 1 ran 49 and killed 47; **L01** (a `#` line read as a pattern) survived because no test used a file such a line would cover, and **L16** survived and is equivalent (`search` already reads "the last segment has a star", so the `(^|/)` copied from vsce's source changes nothing); **B04** (a list of three braces) and **S07, S08** (equivalent as first written) survived in a first, stopped part and were corrected; S09 and the `.*` and `.` forms were set aside as equivalent, unrun. Round 2, aimed at behaviours round 1 did not name (14 new mutants and L01 again): **15 of 15 killed**. In all 62 killed, 1 equivalent survivor. **Tests:** 34 new in all (21 on the rules, 13 as the command, F11's one changed), `tools/test_migrate_layout.py` 186 to **220**, and the gate `migrate-layout-unit-tests` floor 186 to **220** (218 in `e00b2b2`); the table of pinned glob answers has 67 rows, **67 of 67 agree with minimatch 10.2.5** (it had 64). **Evidence, final runs against the committed tool:** `f24-differential.py` at seeds 24, 7 and 99: **4.76 million glob pairs and about 124,000 pattern-built ones, 0 differ**; **900 random `.vscodeignore` files against real `vsce ls`, 0 differ**; the 32-entry default list identical to vsce's source; `f24-adopter-check.sh`: `vscode_quarto_ext` at `507b9348` synced and moved in clones, **tier 1 23 of 23 and tier all 36 of 36 moved files named, the same files `vsce ls` stops ignoring (42 to 65 and 42 to 78), and 0 of 0 after the adopter's own `methodology/**` line (42 to 42)**. The first attempt to fold these into `e00b2b2` by an amend edited its entry and the ledger check refused it; the entry stands as written and this one corrects it. Model: Claude Sonnet 5.5.

### 2026-10-12 · [BL-101] S299 — F24: `bin/migrate-layout` reads a tracked root `.vscodeignore` as vsce reads it (the tool and its tests)

**Tests first:** 26 of the new tests failed or errored before any code (no `vsce_glob`, no `patterns` row); the table of 64 pinned `(pattern, path, answer)` rows was checked against minimatch 10.2.5 `{ dot: true }` before it was trusted (64 of 64, `f24-oracle.py`). **The change** (`bin/migrate-layout`): `vsce_glob` (this tool's translation of minimatch's matching for `*`, `?`, `**`, `[...]` and `{a,b}`; extended globs, brace ranges, backslashes, POSIX classes, `a//b` and a lone brace are not read and counted), `vsce_ignore_list` (what `collectFiles` of `@vscode/vsce` 3.9.2 makes of the file: lines split at `\n` and `\r`, trimmed, `#` lines dropped, `/**` added to a directory name and to a negation, vsce's 32-entry default list and `!package.json`, `!README.md`, a file kept when any negation matches it) and `vscodeignore_exposure` (a moved file is exposed when it is ignored where it is and packaged where it goes; vsce's default list is line 0), wired into `scan_hits` beside F10's `.Rbuildignore` (the row a file already has gains `patterns`; listed, never edited, no refusal, no new exit code) and into the text (`line 9: docs/**  stops covering ...`, `vsce's default list: .gitattributes ...`, then the sentence with `methodology/**`, the pinned versions and "a candidate, not a verdict"). **Tests:** 32 new (21 on the rules, 11 as the command), F11's changed (a `.npmignore` now carries its "listed, never judged" assertion); `tools/test_migrate_layout.py` 186 to 218 and the gate `migrate-layout-unit-tests` floor 186 to 218. The full file ran green before the last two tests (216, 463 s); `bin/check-layout-literals` 0 sites (one marker, `.gitattributes` in vsce's own default list). The evidence scripts, the record and the register, plan and backlog edits are the next commits. Nothing in an adopter changed; nothing went upstream. Model: Claude Sonnet 5.5.

