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

---

## 2026-09

## 2026-10

### 2026-10-08 · [BL-101] S285 — close-out — P11 at tier 1: the first adopter, `model_project_constructor`

`CHANGELOG: pending` on the S285 claim entry is cleared by this statement (the never-edit gate forbids editing a committed entry). **Deliverable:** BL-101 P11 at tier 1 (plan §7.4, recorded as §7.4a; `docs/planning/methodology-subdirectory-evidence/p11-model-project-constructor-record.md`). **In the adopter, three local commits, nothing pushed:** `63cedc5` sync, `4399c60` `--tier 1`, `ec23bc7` one test constant; its own CI on the committed tree is as before the sync (ruff 0, mypy 0, 13 of 13 proofs, pytest 3,942 passed, 9 skipped, 98.34%); `bin/status` 23 of 23 current in layout `new`. **Found:** the default `--tier all` passed every check `bin/migrate-layout` runs and broke 2 of the adopter's 13 proofs and 41 tests (its `proofs` cell runs only the proofs of shards it moves), so by his choice that commit was reset and tier 1 applied; tier 2 there waits for his go-ahead. Under tier 1 alone the dashboard starts a new history in `methodology/`. **Corrections of mine:** the claim stub landed inside the `HANDOFFS.md` front-matter prose and was redone at a line-start anchor; a ledger draft miscounted the tier-1 set; a comment of mine broke the adopter's line limit. Each was fixed before anything left this machine. **3A:** S284's handoff scores 9 (its P11 facts and the 6-link split held exactly; it gave no expectation for the adopter's own CI). **3B:** self-score 7. **3C: no fork learning row appended (D3 not triggered):** considered #64, #101 and #70; the lesson is in plan §7.4's DONE list. Gates 18/18 on `3184535`. Nothing went upstream; #94, #92 and #93 are unchanged and without a maintainer reply; a push to the fork `origin` waits for his go-ahead. Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S285 — the plan and the backlog record P11 (tier 1 done; tier 2 and the tier for P12 are his)

Plan: new §7.4a, the header and the §7.4 order and DONE list updated (an adopter's own proofs, tests and CI rehearsed at each tier in clones first, a rise in skips counted as a failure), §7.3a to §7.3c recomposed to make room (59,995 of 60,000 B; the displaced detail is in `p7-adopter-runs/summary.md` and `p8-rehearsal-output.txt`). Backlog: BL-101's paragraph and index row say P11 is done at tier 1, what `--tier all` broke, and that the next action is his call on tier 2. A follow-up for `bin/migrate-layout` (list project code that names a moved file) is recorded, not built. Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S285 — P11: `model_project_constructor` synced and moved to tier 1, in its own repository (3 local commits there, 1 attempt reset)

In `~/Development/model_project_constructor` (clean `master`, `0dc3051`), from this checkout at `ea82c0c` (the distributed files of `add55f1`): `bin/sync` gave `63cedc5` (21 files rewritten, `.gitattributes` created, no `--force`). `bin/migrate-layout --apply` at its default `--tier all` gave `972b84f`; the adopter's own CI was red on it (2 of its 13 proofs, 32 failed and 9 errors) although every check the tool runs held. At his choice (the mid-session picker) that unpushed commit was reset away (`git reset --hard 63cedc5`, after moving the three ignored generated files back to the root and saving a patch in scratch), and `--tier 1 --apply` gave `4399c60` (23 renames at 100%). One constant in its `tests/test_read_budget.py` gave `ec23bc7`. Its CI on the committed tree: ruff 0, mypy 0, 13 of 13 proofs plain and `--self-test`, pytest 3,942 passed, 9 skipped, 98.34%, as before the sync. `bin/status` reads layout `new`, 23 of 23 tracked files current. A Phase 0 ran there in the new layout. **Nothing was pushed**; its push is his go-ahead. Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S285 — the P11 record and its evidence

`docs/planning/methodology-subdirectory-evidence/p11-model-project-constructor-record.md` and `p11-adopter-runs/` (three files: the adopter's CI runs S1 to S4, the scratch-clone rehearsal with the 41 failures, the `migrate-layout` dry-run heads and apply checks). It states the CI at each state, the 41 tests and 2 proofs that tier 2 breaks, why the tool's `proofs` cell reads 0 for them, the dashboard history that forks under tier 1 alone, and what is his. Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S285 claim (in progress) — P11, the first adopter: `model_project_constructor`

CHANGELOG: pending. Operator said `go`; at the Phase 0 picker he chose P11 as the one deliverable and the owed HANDOFFS trim first (done before this claim: trim `9d59ad4`, fold `aa7bfdf`, shard proof exit 0 from a `--no-local` clone). Deliverable: the first real adopter moved to the `methodology/` layout by `bin/sync` then `bin/migrate-layout`, in that repository, each as its own commit there, with its own tests and CI green and one Phase 0 in the new layout. Nothing pushed, nothing sent upstream. Model: Claude Sonnet 5.5.

### 2026-10-08 · [ad hoc] S285 — fold the 2026-10-08 HANDOFFS shard pointer into the archive index

The pointer block the trim (`9d59ad4`, 1 receipt, S282, 2026-10-08, to `HANDOFFS-through-2026-10-08.md`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, trimmer v1.8.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S284, S283). The shard proof was run by name from a `--no-local` clone of the trim commit: `HANDOFFS-through-2026-10-08.md.verify.sh` at `9d59ad4`, exit 0. Model: Claude Sonnet 5.5.

### 2026-10-08 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-08.md` (1 record(s), 40,552 B → 28,763 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-08 → 2026-10-08) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-08.md`](docs/archive/HANDOFFS-through-2026-10-08.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-08.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-08.md.verify.sh)
rather than trusting a digest printed here. Live file 40,552 B → 28,763 B (−29.1%).

### 2026-10-08 · [BL-101] S284 — fork `main` pushed to `origin`: the 9 commits `e8e9868..e0123f3`

At his go-ahead at the close-out picker, `git push origin main` (the fork, `https://github.com/rmsharp/methodology.git`) took `e8e9868` to `e0123f3`: the S283 push record, the HANDOFFS trim and its fold, the claim, the tool change, the measurement, the acceptance run, the backlog and plan edit, and the close-out. A fast-forward (`origin/main` an ancestor, 0 behind, 9 ahead). **Read back after:** `git fetch origin` then `git rev-list --left-right --count origin/main...main` reads `0 0`, and `upstream/main` is still `f34769f`. Nothing went to `upstream`. This record is a CHANGELOG-only commit and stays local (standing grant), so the count then reads `0 1`. Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S284 — close-out — `bin/migrate-layout` judges the framework documents' links

`CHANGELOG: pending` on the S284 claim entry is cleared by this statement (the never-edit gate forbids editing a committed entry). **Deliverable:** the apply's `check-links` cell counts dangling links by whose file they sit in (a TRACKED framework document is judged, a project file reported), `bin/migrate-layout` and `tools/test_migrate_layout.py` (`7c377c2`), record `docs/planning/methodology-subdirectory-evidence/s284-links-judged-record.md`. **Verified:** the rule chosen from a measurement over the 12 adopters in `--no-local` clones (0 dangling in any framework document; 185 in three project files for 8 of 11 that migrate); 136 tests OK, 15 of 15 mutants killed; the changed tool run over the same 12 from a clean clone of `7c377c2`: 11 `checks ok`; the gate run on `81a0bd0` reads 18/18, results `64b22c42cc89`, manifest `93aff6c93dbc`; `bash bin/tests.sh` in a clean clone of `1630e1b` 477 / 0 / 6. **Corrections of mine:** I wrote the adopter figures of the first ledger entry from memory; recomputing from `rows.json` gave 1 to 108, 8 of 11 and 7 flagged by a plain rule, and I replaced my own unpushed commit (`b22c6e8` became `7c377c2`) before anything left this machine. **3A:** S283's handoff scores 9. **3B:** self-score 7. **3C: no fork learning row appended (D3 not triggered):** considered #97, #100, #101 and #70. Nothing went to upstream; #94, #92 and #93 are unchanged and without a maintainer reply; a push to the fork `origin` waits for his go-ahead. Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S284 — the backlog and the plan record the links check as judged, no longer carried

`docs/planning/BACKLOG-DETAIL.md` BL-101 gains the S284 paragraph (the rule, the measurement, the acceptance run, the record) and drops the two statements that `bin/migrate-layout` still calls its links check informational (the P9 record's "Left" and the next-action "Carried"); the plan's 7.3c "Left" sentence now reads "closed S284" (59,990 of 60,000 B, one byte under where it stood). Next action stays P11. Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S284 — the acceptance run of the changed tool and the record of the links rule

`migrate-12-adopters.py` (P7's script, checks on, adopters' hooks armed as in the real clone) run from a clean `--no-local` clone of `7c377c2`, the commit holding the changed `bin/migrate-layout`: **11 of 12 migrate with `checks ok` and no difference**; the links cell reads 0 framework dangling before and after in all eleven, and the project-file counts of the design measurement (6, 23 from 4, 108, 15, 18, 2, 1, 12). `claude_work` rolls back for the too-small-ledger rename gate (1,305 bytes, 67%) as at P7; `wsfct`'s own hook refuses the commit until its `context_budget.py` path is updated, as at P7, and it applies with its hooks off. Kept in `s284-adopter-runs/`: `rows.json`, `summary.md` and `links-cells.json` (the cells and the rollback causes extracted from the run's 988 KB `reports.json`, which is not committed; P10 kept only its rows too). The record, `s284-links-judged-record.md`: the obvious rule and why it fails, the measurement, the rule, the tests and mutants, what is not verified. Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S284 — the measurement behind the links rule: `links-after-move-12-adopters.py` and its rows

`docs/planning/methodology-subdirectory-evidence/links-after-move-12-adopters.py` (loads P10's helpers) clones each of the 12 adopters with `--no-local`, syncs from `15c7e3c`, runs that sha's `check-links --tree`, `bin/migrate-layout --apply --skip-checks`, and `check-links --tree` again, and sorts every dangling link by the manifest disposition of its file. Its output, `links-after-move-runs/rows.json` and `summary.md`: 11 migrated, `claude_work` rolled back; 0 dangling in any `tracked` framework document before or after; 185 in three project files (`CHANGELOG.md` 63, `SESSION_NOTES.md` 76, `HANDOFFS.md` 46) for 8 of the 11. Hooks off in the clones, as in the P10 differential. Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S284 — `bin/migrate-layout` judges the framework documents' links and reports the project's own

The apply's check-links cell was `INFORMATIONAL` "until P9" (`bin/migrate-layout`, tests `tools/test_migrate_layout.py`). It is now a cell of counts: `links_cell` parses check-links' own lines and counts each dangling link by whether its file is a TRACKED framework document (either layout's name; `framework`, judged by `check_differences`: the count must not change) or a file the project owns (`project`, reported only). An exit 1 whose lines cannot be read, or a run that did not decide (exit 2, timeout), has no counts (`None`) and so differs from a clean before: it never reads as zero. The report loses its `informational` key; the text row reads `exit 0; 0 framework, 0 project dangling -> exit 1; 0 framework, 6 project dangling`. **Why not a plain exit-code comparison:** the test fixture's own ledger holds a committed entry that links `docs/methodology/HOW_TO_USE.md`, which dangles after the ledger moves (a committed entry is never edited), and the measurement over the 12 adopters in `--no-local` clones synced from `15c7e3c` (`docs/planning/methodology-subdirectory-evidence/links-after-move-12-adopters.py`) found 0 dangling links in any framework document, before or after, and 1 to 108 in the adopter's own seed files for 8 of the 11 that migrated (7 had none before, so a plain exit comparison would have flagged 7 of 11 and the framework count flags 0; the eighth, `feedback-loop-comparison`, read 4 before and 23 after; `claude_work` rolls back for the known too-small-ledger rename gate). **Tests (written first):** `tools/test_migrate_layout.py` 128 to 136, the new ones failing against the old tool (4 failures and 1 error in the 10 selected) and passing after; a 15-mutant round on the new lines killed 15 of 15 (M4, the `code in (0, 1)` guard, survived the first round and is pinned by a case that gives an exit 2 a dangling-shaped line). The gate `migrate-layout-unit-tests` is tightened 128 to 136 (`_s284_tightening_bl101_links`). Model: Claude Sonnet 5.5.

### 2026-10-08 · [ad hoc] S284 claim (in progress) — `bin/migrate-layout` judges its check-links cell

CHANGELOG: pending. Operator said `go`; at the Phase 0 picker he ticked the HANDOFFS trim, P11, the links clause and the backlog close-check, and at the follow-up picker chose the links clause as this session's deliverable with P11 next (done before this claim: trim `d89e3e5`, fold `1630e1b`, suite 477 / 0 / 6). Deliverable: the `bin/migrate-layout` apply checks count a links difference, with the rule chosen from a measurement over the 12 adopters in clones; tests first. Nothing outward. Model: Claude Sonnet 5.5.

### 2026-10-08 · [ad hoc] S284 — fold the fifth 2026-10-07 HANDOFFS shard pointer into the archive index

The pointer block the trim (`d89e3e5`, 1 receipt, S281, 2026-10-07, to `HANDOFFS-through-2026-10-07-5.md`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, trimmer v1.8.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S283, S282). The shard proof was run by name from a `--no-local` clone of the trim commit: `HANDOFFS-through-2026-10-07-5.md.verify.sh` at `d89e3e5`, exit 0. Model: Claude Sonnet 5.5.

### 2026-10-08 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-07-5.md` (1 record(s), 39,236 B → 28,790 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-07 → 2026-10-07) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-07-5.md`](docs/archive/HANDOFFS-through-2026-10-07-5.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-07-5.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-07-5.md.verify.sh)
rather than trusting a digest printed here. Live file 39,236 B → 28,790 B (−26.6%).

### 2026-10-08 · [BL-101] S283 — fork `main` pushed to `origin`: the 10 commits `a9f8b01..e8e9868`

At his go-ahead at the close-out picker, `git push origin main` (the fork, `https://github.com/rmsharp/methodology.git`) took `a9f8b01` to `e8e9868`: the S282 push record, the trim and its fold, the claim, the differential, the controls and hybrid script, the two run outputs, the P10 record, the correction and the close-out. A fast-forward (`origin/main` was an ancestor, 0 behind, 10 ahead). **Read back after:** `git fetch origin` then `git rev-list --left-right --count origin/main...main` reads `0 0`, and `upstream/main` is still `f34769f`. **Same picker, D8:** he chose to decide later; nothing is recorded as the route. Nothing went to `upstream`. This record is a CHANGELOG-only commit and stays local under the standing grant (the next read should be `0 1`). Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S283 — close-out — P10: adopters may sync from `add55f1`

`CHANGELOG: pending` on the S283 claim entry is cleared by this statement (the never-edit gate forbids editing a committed entry). **Deliverable:** BL-101 P10, a record (`docs/planning/methodology-subdirectory-evidence/p10-expand-release-record.md`, plan §7.3d). **Verified:** 12 adopters, each synced in two `--no-local` clones from the base `078a6cc` and from `add55f1` and compared: paths identical 12 of 12, nothing under `methodology/`, layout `legacy`, 23 of 23 `current`, health and `check-links` identical; two controls; `sync-in-both-layouts.sh` reads 25 failed checks as it stands (P9 changed the documents it reads) and ALL CHECKS HELD with P6's tools on the candidate's files; the gate run on `1e7d9af` reads 18/18, results `5f5bd400b633`. **Found:** the D8 pull request is a port (34 of 81 commits replay; 13 conflicting files in the set) and D8 does not gate P11. **Corrections of mine:** the entry 'the P10 record' says `inventory-output.txt` holds the plan's dropped line numbers; the plan's git history does (corrected by the entry after it). **3A:** S282's handoff scores 8 (it missed that the P6 evidence script would read red after P9, and says the fork carries #94's changes where it carries the same #93 work as its own commits). **3B:** self-score 7. **3C: no fork learning row appended (D3 not triggered):** considered #106, #101, #100 and #70. Nothing went to upstream; #94, #92 and #93 are unchanged and without a maintainer reply; a push to the fork `origin` waits for his go-ahead. Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S283 — correction to the entry before it (the P10 record)

That entry says the line numbers dropped from the plan's rows for P2 to P6 are held by `inventory-output.txt`. They are not (the file has none of them). They are in the plan's git history: `git show 724aeed:docs/planning/methodology-subdirectory-plan.md` (the last version before this session's edit) carries every one. The never-edit gate forbids editing the committed entry, so this entry is the correction. Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S283 — the P10 record: the sha adopters may sync from, and what a pull request would carry

`docs/planning/methodology-subdirectory-evidence/p10-expand-release-record.md`: adopters may sync from `add55f1` (the last commit to change a distributed file or anything under `bin/`, `tools/`, `starter-kit/`, `.githooks/`); the expand stage changes no path, layout or health of an adopter that only syncs (12 of 12 in clones); the D8 pull request is a port, measured at 51 files, +9,915 -661 for BL-101 alone, 34 of 81 code-touching commits replaying onto `upstream/main`, and D8 does not gate P11. The plan gains §7.3d and stays at 59,991 of 60,000 B by dropping line numbers from the rows of finished phases (P2 to P6; `inventory-output.txt` holds them) and a duplicate P7 bullet; the backlog index and detail name P11 as next. Nothing was sent, tagged or pushed; D8, the release number and any tag stay his. Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S283 — sync-in-both-layouts.sh at the candidate: red as it stands, green with the content held equal (P10)

Run as it stands at the candidate it reads `25 CHECK(S) FAILED`, all in parts A and B, every one a 'versions behind' or 'would write' difference: P9 changed the documents its two sides read (`p10-sync-in-both-layouts-at-candidate.txt`). With P6's tools on the candidate's files it reads ALL CHECKS HELD: 12 of 12 identical in part A, five moved adopters equal in part B, 11 of 11 in part C (`p10-sync-in-both-layouts-hybrid-output.txt`). The script is a snapshot, not a gate; `sync-layout-unit-tests` is the gate. Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S283 — two controls for the differential, and the hybrid script (P10)

Candidate = base finds 0 differing files and still reads CHECK ROW (the base's `bin/status` prints no `layout:` line); `--tamper` moves a file under `methodology/` and reads one rename, paths DIFFER, CHECK ROW (`control-candidate-equals-base.json`, `control-tamper.json`). `p10-sync-hybrid.sh` builds the candidate's files with P6's tools on a side branch of a scratch clone and runs `sync-in-both-layouts.sh` there, so only the tools differ. Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S283 — the 12-adopter sync differential, its script and its rows (P10)

`p10-sync-12-adopters.py` clones each of the 12 adopters twice (`--no-local`), syncs one with the `bin/sync` of the base `078a6cc` and one with that of `add55f1`, and compares the two trees. Rows (`p10-adopter-runs/rows.json`, `summary.md`): paths identical in 12 of 12, nothing under `methodology/`, layout `legacy`, 23 of 23 tracked files `current`, 19 content files differ (20 and 21 where a ledger seed is written), health and `check-links` exits identical; `--force` was needed for two adopters in both trees. Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S283 claim (in progress) — P10, the readiness record for the expand stage

CHANGELOG: pending. Operator said `go`; at the Phase 0 picker he chose P10 prep and the owed HANDOFFS trim (done before this claim: `025bccf`, fold `05a42a0`, suite 477 / 0 / 6). Deliverable: one record in the evidence directory naming the sha adopters may sync from, the clone evidence over the 12 adopters, and the measured contents of the D8 pull request. Nothing outward. Model: Claude Sonnet 5.5.

### 2026-10-08 · [ad hoc] S283 — fold the fourth 2026-10-07 HANDOFFS shard pointer into the archive index

The pointer block the trim (`025bccf`, 1 receipt, S280, 2026-10-07, to `HANDOFFS-through-2026-10-07-4.md`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, trimmer v1.8.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S282, S281). The shard proof was run by name from a `--no-local` clone of the trim commit: `HANDOFFS-through-2026-10-07-4.md.verify.sh` at `025bccf`, exit 0. Model: Claude Sonnet 5.5.

### 2026-10-08 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-07-4.md` (1 record(s), 40,217 B → 28,462 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-07 → 2026-10-07) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-07-4.md`](docs/archive/HANDOFFS-through-2026-10-07-4.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-07-4.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-07-4.md.verify.sh)
rather than trusting a digest printed here. Live file 40,217 B → 28,462 B (−29.2%).

### 2026-10-08 · [BL-101] S282 — fork `main` pushed to `origin`: the 16 commits `334e31d..a9f8b01`

At his go-ahead at the close-out picker, `git push origin main` (the fork, `https://github.com/rmsharp/methodology.git`) took `334e31d` to `a9f8b01`: the S281 push record, the three ledger-trim commits, the claim, the seven P9 document steps, the test and plan, the backlog, the floor and the close-out. A fast-forward (`origin/main` an ancestor, 0 behind, 16 ahead). **Read back after:** `git fetch origin` then `git rev-list --left-right --count origin/main...main` reads `0 0`, and `upstream/main` is still `f34769f`. Nothing went to `upstream`. This record is a CHANGELOG-only commit and stays local (standing grant), so the count then reads `0 1`.  Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S282 close-out — P9: the documents name files by bare name and say where they are; `check-links --layout both` exits 0; receipt complete

BL-101 P9 is done (plan 7.3c). `bin/check-links --layout both` went from exit 1 (36 of 116 links dangling in the new layout) to exit 0 (80 links in 23 files per layout) and `bin/tests.sh` Test 10 holds it. The 36 became bare names in code spans because no one relative link spans the legacy and the `methodology/` layout; the runner says once where files are and `BOOTSTRAP.md` gained "Two layouts" with the C14 sentence. The ledgers were trimmed first on his go-ahead (HANDOFFS to `-3`, CHANGELOG 186,236 B to 78,034 B). **Gate run on `8e214c5`:** 18/18 pass, 0 unmeasured, results `5f5bd400b633`, manifest `a58181b6d58b`; the suite 483 / 0 / 0 at three receipts and 477 / 0 / 6 at two; `tests-sh-passed` floor 477. **3A:** S281's handoff scores 8. **3B:** self-score 8. **3C:** no fork learning row appended and none retired (D3), rows considered in the receipt. **Left:** `bin/migrate-layout` still prints its links check as "informational until P9"; P10 and its upstream route are his call; trim of HANDOFFS owed at the next Phase 0. His go-ahead at the close-out picker: push fork `main` to `origin` after this commit; `upstream` is not touched.  Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S282 — the floor: `tests-sh-passed` 476 to 477, measured at both receipt states

`bash bin/tests.sh` in clean `--no-local` clones of `724aeed`, output captured: **483 / 0 / 0** at three receipts and **477 / 0 / 6** with the S282 stub removed in a scratch commit (two receipts); Test 40 compared 666 with 666 in both. The one new pass is Test 10's `check-links --layout both` assertion. A mutant with one legacy-style `docs/methodology/` link in `RECOMMENDED_SKILLS.md` leaves the legacy-only check at exit 0 and takes `--layout both` to exit 1, so the new assertion is not redundant. No gate added; the hook accepts a tightening.  Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S282 — P9 step 7: two `BOOTSTRAP.md` statements that read as universal now say they are about the legacy layout

The manual-copy table's closing sentence ("the framework under `docs/methodology/`") now says "in the legacy layout; the `methodology/` layout has its own table", and Step 8's `mkdir -p docs/methodology/sessions` gains a comment naming `methodology/sessions` for the other layout. Found by re-listing what still names `docs/methodology/` after the conversions: 38 lines in the distributed documents at the claim, 10 now (the runner's convention paragraph, `HOW_TO_USE.md` once, `BOOTSTRAP.md` eight times, each saying which layout it describes).  Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S282 — the backlog records P8 and P9: BL-101's index row and detail now name P10 as next

`docs/planning/BACKLOG.md` (the BL-101 row) and `BACKLOG-DETAIL.md` (its detail) said "Next: P8". Both now record P8 (the rehearsal failed the section 3.1 criterion; BL-104) and P9 (36 links became bare names, `--layout both` exit 0, Test 10 holds it) and name P10 as next; the detail also keeps the one thing P9 left, the `bin/migrate-layout` links check that still prints "informational until P9" (`:695`, `:882`; test `tools/test_migrate_layout.py:1354`).  Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S282 — P9 step 6: Test 10 holds `--layout both` green, two stale statements are corrected, and the plan records P9

`bin/tests.sh` Test 10 gains one assertion, `check-links --layout both` exit 0 (it read exit 1 with 36 dangling at this session's claim). `bin/check-links`'s docstring and this repository's `CLAUDE.md` no longer say `both` is P9's future criterion (`CLAUDE.md` 18,767 B to 18,737 B). The plan's new §7.3c records P9; to stay inside its 60,000 B declared budget (now exactly 60,000) §7.3a and §7.3b were recomposed, their per-adopter detail pointing at `p7-adopter-runs/summary.md` where it is kept, and the P6 sentence "For P9" removed as resolved. **Left, not done (a tool change, not documentation):** `bin/migrate-layout` (`:695`, `:882`) still prints its links check as informational "until P9".  Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S282 — P9 step 5: `BOOTSTRAP.md` gains "Two layouts" and the README points at it; `bin/check-links --layout both` exits 0

`starter-kit/BOOTSTRAP.md` (36,737 B to 39,555 B): a new section "Two layouts" (the table of where files sit, what `--layout auto|new` does, what `bin/migrate-layout` refuses and reports, the plan's C14 sentence that two things are called `methodology`, and that names are bare); the setup tree, the adoption-mode sentence, the `bin/sync` copy sentence, manual-copy step 1, the update route's table and the customization row each say which layout they describe; its two links that could not resolve in both layouts (`PROJECT_LEARNINGS.md`, `ITERATIVE_METHODOLOGY.md`) are bare names. `README.md`: one paragraph before Option B. **Measured:** `bin/check-links` legacy OK, `--layout new` OK, `--layout both` exit 0, 80 links in 23 files in each layout (36 dangling at the start of the session). `bin/sync --layout auto` on an empty repository chose legacy and `--layout new` wrote under `methodology/` (dry runs), which is what the section says.  Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S282 — P9 step 4: the two ledger seeds name the framework document by bare name, and the CLAUDE.md template says where the runner may sit

`starter-kit/CHANGELOG.md` and `starter-kit/HANDOFFS.md` (seeds, written once into a new project) turn their `docs/methodology/FRAMEWORK_APPARATUS.md#the-action-ledger` link into `` `FRAMEWORK_APPARATUS.md` §The Action Ledger ``. `starter-kit/CLAUDE_TEMPLATE.md` gains one HTML comment under the SESSION PROTOCOL line telling a `methodology/` project to write `methodology/SESSION_RUNNER.md` there, written as an HTML comment like the template's other "Customize" notes (whether a loaded `CLAUDE.md` drops it was not checked here). `bin/check-links`: legacy OK (84 to 82 links), `--layout new` 4 to 2 dangling (both in `BOOTSTRAP.md`).  Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S282 — P9 step 3b: the three campaign templates and `SAFEGUARDS.md` name files by bare name

The three `*_CAMPAIGN.md` files turn their one `../../../SESSION_RUNNER.md` link into its own text; `SAFEGUARDS.md` names `workstreams/RESEARCH_DOCUMENTATION_WORKSTREAM.md` without the `docs/methodology/` prefix. `bin/check-links`: legacy OK (87 to 84 links), `--layout new` 7 to 4 dangling.  Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S282 — P9 step 3a: four workstream documents name the operating files by bare name

`ARCHITECTURE_WORKSTREAM.md` (2 links), `DEVELOPMENT_WORKSTREAM.md`, `AUDIT_WORKSTREAM.md` and `TEMPLATE_WORKSTREAM.md` (1 each) turn their `../../../` links to `SAFEGUARDS.md` and `RECOMMENDED_SKILLS.md` into their own text. `bin/check-links`: legacy OK (92 to 87 links), `--layout new` 12 to 7 dangling.  Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S282 — P9 step 2: the three framework documents name files by bare name and know the second layout

`ITERATIVE_METHODOLOGY.md` turns its 8 `../../` links to the operating files into their own text. `FRAMEWORK_APPARATUS.md` adds one sentence under its trim command giving the `methodology/` form (`python3 methodology/methodology_trim.py --file methodology/CHANGELOG.md --check`) and pointing at the runner's paragraph. `HOW_TO_USE.md` says in three places that the runner may sit in `methodology/` (the table row, step 1 of the integration list with its CLAUDE.md example, and the "known location" step). `bin/check-links`: legacy OK (100 to 92 links), `--layout new` 20 to 12 dangling.  Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S282 — P9 step 1: the runner says where the files are, and it and `RECOMMENDED_SKILLS.md` stop linking across layouts

With his approval of the design at the picker (links that cannot resolve in both layouts become bare names in code spans; one convention paragraph in the runner). `starter-kit/SESSION_RUNNER.md` gains the paragraph "Where the files are" before Phase 0 and names the 6 workstream rows, 3 `ITERATIVE_METHODOLOGY.md` mentions and 2 anchored links by bare name: 55,016 B to 55,361 B (+345, under the 56,750 B one-read cap). The paragraph widens his approved draft in one place: a tool and any methodology file it takes get `methodology/` in front, because `methodology_trim.py --file` needs the path. `starter-kit/RECOMMENDED_SKILLS.md` turns its 14 `docs/methodology/` links into their own text (18,501 B to 17,762 B). `bin/check-links`: legacy OK (116 to 100 links), `--layout new` 36 dangling to 20.  Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S282 claim (in progress) — P9, the documentation for the `methodology/` layout

CHANGELOG: pending. Operator said `go`; at the Phase 0 picker he chose BL-101 P9 and both ledger trims. Deliverable: the plan's section 7 row P9 and C14, done when `bin/check-links --layout both` exits 0 with the suite criterion held. Baseline at this claim: `--layout legacy` OK (116 links), `--layout new` 36 dangling in 13 files, `both` exit 1, 38 distributed lines name `docs/methodology`, suite 476 / 0 / 6 at two receipts (`40c3694`, Test 40 666 = 666). Done before this claim: the HANDOFFS trim `ae8d846` and fold `3efcd4f`, the CHANGELOG trim `40c3694`. Phase 0: 0 undocumented commits, 0 merges, gate citation matches, #94 #92 #93 without a reply. Model: Claude Sonnet 5.5.

### 2026-10-08 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-10-07.md` (66 record(s), 186,236 B → 78,034 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **66** record(s) (2026-10-07 → 2026-10-07) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-10-07.md`](docs/archive/CHANGELOG-through-2026-10-07.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-10-07.md.verify.sh`](docs/archive/CHANGELOG-through-2026-10-07.md.verify.sh)
rather than trusting a digest printed here. Live file 186,236 B → 78,034 B (−58.1%).

### 2026-10-08 · [ad hoc] S282 — fold the third 2026-10-07 HANDOFFS shard pointer into the archive index

The pointer block the trim (`ae8d846`, 1 receipt, S279, 2026-10-07, to `HANDOFFS-through-2026-10-07-3.md`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, trimmer v1.8.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S281, S280). The shard proof was run by name from a `--no-local` clone of the trim commit: `HANDOFFS-through-2026-10-07-3.md.verify.sh` at `ae8d846`, exit 0. Model: Claude Sonnet 5.5.

### 2026-10-08 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-07-3.md` (1 record(s), 39,546 B → 28,436 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-07 → 2026-10-07) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-07-3.md`](docs/archive/HANDOFFS-through-2026-10-07-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-07-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-07-3.md.verify.sh)
rather than trusting a digest printed here. Live file 39,546 B → 28,436 B (−28.1%).

### 2026-10-07 · [BL-101] S281 — fork `main` pushed to `origin`: the 9 commits `d9cdd52..334e31d`

At his go-ahead at the close-out picker, `git push origin main` (the fork, `https://github.com/rmsharp/methodology.git`) took `d9cdd52` to `334e31d`: the S280 push record `fe62950`, the HANDOFFS trim `01b6947` and its fold `9d8baf0`, the claim, the P8 script and its two repairs, the record of P8 with BL-104, and the close-out. A fast-forward (`origin/main` was an ancestor, 0 behind, 9 ahead). **Read back after:** `git fetch origin` then `git rev-list --left-right --count origin/main...main` reads `0 0`, and `upstream/main` is still `f34769f`. Nothing went to `upstream`. This record is a CHANGELOG-only commit and stays local under the standing grant (the next read should be `0 1`). Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S281 close-out — P8: the rehearsal of this repository's own move, and the answer is no

**Deliverable done** (a rehearsal; nothing shipped): `docs/planning/methodology-subdirectory-evidence/p8-rehearsal.sh`, `p8-apply-tool.py` and `p8-rehearsal-output.txt` (the fourth run, at `ffe5512`). **Result:** the plan's section 3.1 criterion FAILS for this repository's own move (unmoved `bin/tests.sh` 482 / 0 / 0, moved by `bin/migrate-layout` 445 / 11 / 4; gates 18/18 against 16/18), and the tool refuses the canonical repository as built (`[not-current]`, plus `[tier-order]` at tier 2). With that one precondition suppressed its apply is clean (255 renames, lowest similarity 99%, its checks agree); the proofs (126 tracked, 121 / 5), both ledger trims in `methodology/archive/` with the hooks on, X2 and the never-edit gate all held. Plan section 7.3b records it (59,979 of 60,000 B); **BL-104** carries the four defects and the known cost. **His decisions at the close-out picker:** leave BL-104 open and do P9 next (B2 stays his call, D6 and D8); push to fork `origin` after this commit. Before the claim, on his go-ahead at the Phase 0 picker: the owed HANDOFFS trim (`01b6947`) and its fold (`9d8baf0`). Gate run on `1136d7e`: 18/18 pass, 0 fail, 0 unmeasured, results `f6685334c4b6`. **3A:** S280's handoff scores 8. **3B:** self-score 7 (the instrument printed `exit 0` for an 11-failure suite, a script edited while it ran, a table-row patch that overwrote four plan rows and was caught by `git diff`). **3C:** no fork learning row appended and none retired (D3); considered #70, #100 and #101. Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S281 -- P8 recorded: the plan's 7.3b, the run's output and BL-104

`docs/planning/methodology-subdirectory-evidence/p8-rehearsal-output.txt` is the repaired script's complete run at `ffe5512` (exit codes read bare; 196 lines). The plan's section 7.3b holds the result and its header now reads P1 to P8 built, P9 next; to make room the P5 to P7 records and two table rows were recomposed (59,767 to 59,979 of 60,000 B). **BL-104 raised** with its detail entry: moving this repository's own instance files (B2) is blocked by four measured defects (the tool refuses the canonical, the dashboard's changelog probe, 11 FAILs and 4 SKIPs in canonical-only tests, a silent shard misplacement at resync) and one known cost; whether B2 is wanted at all is his decision (D6, D8). Read back against the output: 482 / 0 / 0 unmoved against 445 / 11 / 4 moved, gates 18/18 against 16/18, 126 proofs 121 / 5 in both trees, both ledgers proved in `methodology/archive/` with the hooks on. Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S281 -- the first complete P8 run, and the script defects it showed in its own output (checkpoint)

**The criterion FAILS for this repository's own move (plan 3.1):** the unmoved clone reads 482 passed / 0 failed / 0 skipped, the clone moved by `bin/migrate-layout` reads **445 / 11 / 4**, and the gate run reads 18/18 unmoved and **16/18 moved** (2 fail). The 11 FAILs and 4 SKIPs are Tests 29, 38, 39, 40, the ratchet test and the close-out and dashboard unit suites reading this repository's own root ledgers and manifest by path. Also measured: the dashboard reads the moved changelog as absent (health 76 to 74, `has_changelog` the only metric that differs); the resync re-run gives 4 modify/delete conflicts and **no** file-location conflict, because the tool leaves two files in `docs/archive/`, so upstream's new shard lands silently there. Defects of my script, in that run's own output: the exit codes of the suites and the ratchet were read after a command substitution (a suite with 11 failures printed `exit 0`), the not-a-pass gate rows were filtered with a pattern the table does not match, and git's detached-HEAD advice filled the output. All three fixed; the run is repeated from the repaired script. Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S281 -- the P8 script, repaired by its first runs (checkpoint)

Two partial runs found my own defects, none in the tool: `mk` cloned every scratch tree from the real repository, which lacks the migration commit (it now takes a source), and I edited the script while bash was executing it, which shifted its read offset (so a run is made from a copy). Added from what the runs showed: where upstream's new shard lands in each merge, the dashboard stage run in throwaway copies of the clones with every metric that differs listed, and a clean-tree check before the suites. Read so far: the hook stage (control and moved tree both refuse a later commit with no ledger; a commit that co-stages the moved ledger passes; an edit to a committed entry is refused), the trim stage (both ledgers trim and prove in `methodology/archive/` with the hooks on) and the proofs (126 tracked, 121 / 5 in both trees, none differ). Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S281 -- the P8 rehearsal script and its tool driver (checkpoint)

`docs/planning/methodology-subdirectory-evidence/p8-rehearsal.sh` (eight stages, two `--no-local` clones of one commit, the real repository only cloned) and `p8-apply-tool.py` (loads the clone's `bin/migrate-layout` and runs its own `main()` with ONE suppression, `read_status`). **First finding, measured:** the tool as written REFUSES this repository, `--tier all` on `[not-current]` (23 distributed files read `missing`, since the canonical holds them under `starter-kit/` and `workstreams/`, not at adopter locations) and `--tier 2` also on `[tier-order]`. With that one precondition suppressed, the tool plans 255 moves (7 instance files, 248 shard files), leaves 2 files in `docs/archive/` in place, rewrites `CLAUDE.md` (18), `.context-budget.json` (1) and `.quality-gates.json` (1), rehearses 123 proofs (0 excluded), and its apply lands as one commit through the hooks: 255 renames, lowest similarity 99%, its checks agree, proof histogram 118 / 5 before and after, root 22 to 16 entries. The other seven stages are not run yet. Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S281 claim (in progress) — P8, the rehearsal of this repository's own move in a scratch clone

CHANGELOG: pending. Operator said `go`; at the Phase 0 picker he chose BL-101 P8 and the owed HANDOFFS trim. Deliverable: the plan's section 7.3 row P8 and section 5A.4 (C17), in a scratch clone and shipping nothing: `bin/migrate-layout` on the instance files, the section 3.1 criterion at the measured baseline, the proofs' histogram, a real trim in the new layout, the X2 hook test, the resync simulation against `upstream/main`. Done before this claim: the trim `01b6947` and its fold `9d8baf0`. Phase 0: 0 undocumented commits, 0 merges, gate citation matches, #94 #92 #93 without a reply, `CHANGELOG.md` 176,567 B (the 196,608 B trigger does not fire). Model: Claude Sonnet 5.5.

### 2026-10-07 · [ad hoc] S281 — fold the second 2026-10-07 HANDOFFS shard pointer into the archive index

The pointer block the trim (`01b6947`, 1 receipt, S278, 2026-10-07, to `HANDOFFS-through-2026-10-07-2.md`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, trimmer v1.8.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S280, S279). The shard proof was run by name from a `--no-local` clone of its own trim commit: `HANDOFFS-through-2026-10-07-2.md.verify.sh` at `01b6947`, exit 0. Model: Claude Sonnet 5.5.

### 2026-10-07 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-07-2.md` (1 record(s), 40,880 B → 29,100 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-07 → 2026-10-07) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-07-2.md`](docs/archive/HANDOFFS-through-2026-10-07-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-07-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-07-2.md.verify.sh)
rather than trusting a digest printed here. Live file 40,880 B → 29,100 B (−28.8%).

### 2026-10-07 · [BL-101] S280 — fork `main` pushed to `origin`: the 25 commits `a364f40..d9cdd52`

At his go-ahead at the close-out picker, `git push origin main` (the fork, `https://github.com/rmsharp/methodology.git`) took `a364f40` to `d9cdd52`: the S279 push record `4eac83f`, the S280 trims and fold, the claim, the eight layers of `bin/migrate-layout` with their RED checkpoints, the mutation tests, the evidence over the 12 adopters, the documents, the wiring and floors, the repair of the shell suite's run time (BL-103) and the close-out. **Read back after:** `git fetch origin` then `git rev-list --left-right --count origin/main...main` reads `0 0`, and `upstream/main` is still `f34769f`. Nothing went to `upstream`. This record is a CHANGELOG-only commit and stays local under the standing grant, so the next session reads `0 1`. Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S280 close-out — P7: `bin/migrate-layout`, run over the 12 adopters in clones (11 migrate, `claude_work` is refused); receipt complete

`CHANGELOG: pending` on the S280 claim entry is cleared by this statement (the never-edit gate forbids editing a committed entry). **Deliverable:** BL-101 P7, plan section 7.3, recorded as 7.3a. `bin/migrate-layout` is a dry run unless `--apply`; it refuses a dirty, half-migrated, ignore-mode or not-`current` tree and a destination that exists, every reason at once; plans from the manifest's two tables after rehearsing the shard proofs in a throwaway clone; rewrites `CLAUDE.md`, anchored `.gitignore` entries and the configs' paths as text; adds one ledger entry; reports every hit it leaves; applies as ONE commit through the project's hooks, every tracked move a rename at 90% or better, rolled back on any failure and checked before and after. Before the claim, on his go-ahead at the Phase 0 picker: the CHANGELOG trim (the file was 279,349 B, past the 262,144 B hard refusal), the owed HANDOFFS trim and its fold. **Verified:** 128 tests, each of eight layers RED first; 78 mutants (round 1, 67 from the new code, 64 killed; round 2, 11 aimed at behaviours with no named test, 0 killed, all 11 became tests; 78 of 78 at the end); `bin/tests.sh` in clean clones 482 / 0 / 0 at three receipts, 476 / 0 / 6 at two, 377 s after the repair; the gate run on `8428c31` reads **18/18 pass, 0 fail, 0 unmeasured**, results `f6685334c4b6`, manifest `5115eb732421`; **on real data** the tool ran over the 12 adopters in `--no-local` clones (four runs, 12 rows, no blank cell; committed in `p7-adopter-runs/`): 11 migrate at R92 to R97 with proof histograms, `bin/status`, ledger checkers and health unchanged but `chat_verification` 48 to 45 (the pinned `has_docs_dir`), `claude_work` refused (a ledger that is only the seed falls to 68%), `wsfct` rolled back by its own untracked hook until that clone's hooks are off, `vscode_quarto_ext` keeping the one shard whose older-format proof reads its shard by working-tree path (which corrects plan C7). **Corrections of mine, disclosed where they happened and here:** the evidence entry says `check-links` reads exit 0 to 1 for nine adopters, and the table has ten (`feedback-loop-comparison` reads 1 to 1 on both sides); wiring the 265 s suite into `bin/tests.sh` took that suite from 5.5 to 10.7 minutes, past the gate runner's 600 s, so `tests-sh-passed` and `tests-sh-failed` read `unmeasured (exit 127)` until a full gate run showed it (repaired, BL-103); several of my tests were wrong before the tool was (8 replacements for 6, 11 TRACKED files for 23, a filter that matched `.githooks/` too, a key `note`); and the entries of this session are long, so the ledger grew 39 KB to 171 KB and the 196,608 B trim trigger is about 20 KB away. **For him, decided at the close-out picker:** push the session's commits to the fork `origin` after this one; keep the 90% refusal of a ledger that is only the seed (no plan change). **3A:** S279's handoff scores 8 (the trim, the baselines, the gate citation and the plan sections held; it missed that `CHANGELOG.md` had passed the hard refusal and that the shell suite was already 5.5 of a 10 minute gate limit). **3B:** self-score 8. **3C: no fork learning row appended and none retired (D3 of `docs/planning/fork-learnings-retirement-rule-plan.md`):** considered #107 (a surviving mutant becomes a test: applied 14 times), #72, #16, #12 and #70; none is newly enforced by a gate this session added, none superseded, none's artifact gone. Nothing went to upstream; #94, #92 and #93 are unchanged and without a maintainer reply. Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S280 — a defect of mine found by the full gate run: wiring the 265 s suite into `bin/tests.sh` silently disarmed `tests-sh-passed` and `tests-sh-failed`; only the fast classes are wired now (BL-103)

`python3 starter-kit/quality_ratchet.py --run` at `13e80d3` read `16/18 pass · 0 fail · 2 unmeasured`: `tests-sh-passed` and `tests-sh-failed` were `unmeasured`, note `extract matched nothing (exit 127)`. **Cause, measured:** the gate runner gives each gate 600 s and `run()` maps a `TimeoutExpired` to the exit code 127, so a timeout reads as a missing command. `bash bin/tests.sh` took **5.5 minutes** before the previous two commits wired `tools/test_migrate_layout.py` in (S280's first run, a clean clone) and **10.7 minutes** after (the three-receipt and two-receipt runs); the 482 and 476 I measured and recorded were true and the suite was then too slow to be measured by the gate that holds it. I wired it in by the convention of the sibling layout suites without timing it. **The pre-commit hook does not refuse an unmeasured gate**, so this was found only because the run's summary line was read. **Repair, no loosening:** `bin/tests.sh` now runs only `TestThePureRules` and `TestUsageAndNothingToDo` of the migration suite (39 tests, 0.7 s), under the same PASS row, so the count stays 476 and 482; the 128-test command-level suite is the gate `migrate-layout-unit-tests` and is not wired in (the note in `.quality-gates.json` and the comment in `bin/tests.sh` say why). The shell suite is back to about 5.5 minutes, to be re-measured below the limit in a clean clone. **BL-103** records what the repair does not do (a distributed tool, its own session): report a timeout as a timeout, let a gate declare its own limit, and refuse a cited run that has an unmeasured gate. Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S280 — the floors after BL-101 P7: `tests-sh-passed` 475 to 476 and a new gate, `migrate-layout-unit-tests` at 128

Both are measured. `bash bin/tests.sh` in a clean `--no-local` clone of `c159e59` (captured to a file, nothing else running): **482 passed, 0 failed, 0 skipped at three receipts, and 476 passed, 0 failed, 6 skipped at two** (the S280 stub removed in the clone; Test 40 still compares 666 with 666), against S279's 481 and 475: the one new pass is the wired migration-tool suite. The floor is stated at two receipts, the at-rest state after the next trim (fork Learning #70). `migrate-layout-unit-tests` is `python3 tools/test_migrate_layout.py`, `Ran 128 tests`, about 265 s. The shell suite is about 4.5 minutes slower for it. `.quality-gates.json` carries the note (`_s280_tightening_bl101_p7`). Adding a gate and raising a floor are tightenings; the pre-commit ratchet accepts them. Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S280 — `bin/tests.sh` runs the migration tool's suite (128 tests, about 4.5 minutes of the shell suite)

`bin/tests.sh` now runs `tools/test_migrate_layout.py` beside the other layout suites, after the sync layer, and passes or fails on its exit code (one new PASS row: "migration tool (bin/migrate-layout) unit tests green"). Canonical-only, like the tool. The floors for it (the shell suite's `tests-sh-passed` and a new gate `migrate-layout-unit-tests`) follow in the next commit, measured in a clean clone of this one. Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S280 — the plan, the backlog and `CLAUDE.md` record BL-101 P7 (the plan at 59,767 of its declared 60,000 B)

BL-101 P7 is recorded where the next session reads. **The plan:** a new section 7.3a (what was built and measured), the P7 bullet of 7.3 shortened to its criterion and its surface, the status lines say P1 to P7 are built and P8 is next, and sections 7.2a to 7.2e were recomposed (4,781 B to 2,630 B, every figure and every "not shown" kept) to make the room; the file is 59,767 B of a declared 60,000. **The backlog:** the BL-101 row and its detail entry say P7 is done, give the measured result over the 12 adopters (11 migrate, `claude_work` refused, `wsfct` rolled back by its own hook until it is updated), put the one open choice for the operator (a ledger that is only the seed cannot take its entry and stay a rename at 90%: keep the refusal, require additions-only and a 50% rename for the ledger alone, or commit the entry second) and make P8 the next action. **`CLAUDE.md`:** a row for `bin/migrate-layout` and `tools/test_migrate_layout.py` in the tools table, and P7 named among the tools that embed the resolver. Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S280 — evidence of BL-101 P7 on real data: `bin/migrate-layout` over the 12 adopters in `--no-local` clones (11 migrate, `claude_work` is refused)

The last of four runs of `docs/planning/methodology-subdirectory-evidence/migrate-12-adopters.py` (it clones each adopter's committed `HEAD` with `--no-local`, arms the hooks path the real clone has, runs `bin/sync` as its own commit when a TRACKED file is not `current` (plan 5A.2; with `--no-verify` when the adopter's own armed hook refuses the sync commit, and with `--force` when the sync alone refuses), measures the project's own dashboard and ratchet on a copy, then runs the tool as a dry run and with `--apply`, and re-runs a migration that the adopter's own hook rolled back with that clone's hooks off). Output committed: `p7-adopter-runs/summary.md` (the 12-row table, 24 columns, no blank cell), `rows.json` and `reports.json` (the raw dry-run and apply reports). **Read back after: the 11 real repositories that were idle are unchanged; `nprcgenekeepr` took the operator\'s own S936 commits during the session, which are not this run\'s (a clone only reads).** **Result: 11 of 12 migrate.** Moves 30 to 139 files, renames R92 to R97 (`vscode_quarto_ext`\'s `.context-budget.json` is nearest the bar), the tree clean after, `bin/status` 23 of 23 TRACKED `current` before and after, both ledger checkers\' exit codes and every proof histogram unchanged (`nprcgenekeepr` `{0: 45, 1: 10}` both sides, `wsfct` `{1: 6}` both sides: pre-existing reds), the ledger\'s history reached across the move (one commit more), project health unchanged except `chat_verification` 48 to 45 (the pinned `has_docs_dir` decision: it has no `docs/` of its own once `docs/methodology/` empties) and two at +1; `check-links --tree` reads exit 0 to exit 1 for nine of them, which is the 36 of 116 dangling links P9 owns. **Four things the fixtures could not show, found by the first runs and fixed and tested: (1)** `vscode_quarto_ext`\'s older-format `SESSION_NOTES-through-S253` proof reads its shard by working-tree path and exited 0 to 2 (this corrects plan C7: equal proof exit codes held for this repository\'s 117, not for every adopter\'s); the tool now rehearses the shard moves in a throwaway clone and keeps such a shard with its proof; **(2)** `wsfct`\'s own pre-commit hook, written by `context_budget.py install-hook` into `.git/hooks/` (untracked, per clone) and execing the tool from the root, refused the migration commit and the tool rolled back and said why (right), but the dry run had not warned: the scan now reads the directory git runs hooks from and names it; **(3)** `claude_work`: a ledger that is only the seed falls to 68% with its entry and is refused with its size and the reason; **(4)** `chat_verification` and `church_growth` have older armed ledger hooks that refused the evidence script\'s own sync commit and **accepted the migration commit**, because it carries a ledger entry. `claude_work` is the one row not migrated, and has no history to move. Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S280 — the mutation pass of P7: 78 mutants, 64 killed, 14 survived and became 9 new tests and 2 tightened ones; the suite is 128 tests

The mutation pass of BL-101 P7 (`docs/planning/methodology-subdirectory-evidence/mutate-p7.py` and `p7-mutants.py`, re-runnable, in a scratch clone of the commit under test; a mutant the named classes do not kill is re-run against the whole test file before it counts as a survivor). **Round 1, 67 mutants written from the new code: 64 killed, 3 survived.** `M07` drops the `~` from the standing-alone rule's lookbehind (nothing put `~` directly before a name; `~/X` is stopped by the `/`), `M10` removes the empty-map shortcut (my test text never contained two non-word characters in a row, where an empty alternation matches), `M17` makes the JSON rewrite escape non-ASCII (no test changed a command that held one). **Round 2, 11 mutants aimed at behaviours I could not name a test for: 0 killed, all 11 survived**, which is what that round is for: `R01` the rule that `bin/status` must read every TRACKED file current AFTER the move, whatever it read before; `R02` the cleanup removing the project root when a move empties it; `R03` and `R04` the half-migrated tree's layout label and that the runner's collision is not listed a second time; `R05` the branch where git sees no rename at all; `R06` a tree the commit leaves dirty; `R07` the 25-site cap; `R08` a binary file naming a moved file; `R09` the blank line that makes trailers trailers; `R10` the count of files moved without git in the message; `R11` a tier-1 run naming what it leaves of an archive it does not touch. **Nine new tests and two tightened ones, each seen failing first as a mutant**, and one change to the tool they found: the "too small to take its entry" hint was skipped when git saw no rename at all (a ledger of 12 bytes), which is the case that needs it most. Equivalent mutants (a sort whose order never decides, a `half-migrated` status row that is not a TRACKED row anyway) were not written. Round 1 mostly killed because the tests were written from the same lines; round 2 is where the gaps were, as in S279. Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S280 — layer 8 of P7: the scan reads the hooks git runs, not only the ones it tracks (119 tests)

Layer 8 of BL-101 P7, from the second run over the 12 adopters (11 of 12 migrated, `claude_work` refused for a ledger that is only the seed, `wsfct` rolled back by its own hook and migrated with that clone's hooks off). **The dry run had not warned about `wsfct`'s hook, and the reason was a gap in the scan:** the hook that refused is the one `context_budget.py install-hook` writes into `.git/hooks/pre-commit`, which git does not track and which execs `$(git rev-parse --show-toplevel)/context_budget.py`, so a scan of tracked files saw nothing and a name behind `)/` is, everywhere else, a name behind a directory. The scan now also reads the directory git actually runs hooks from (`git rev-parse --git-path hooks`, so `core.hooksPath` is honoured, absolute or relative; `.sample` files are not hooks), marks each such site `untracked` (the text says `[not tracked: per clone]`), does not count a tracked hook directory twice, and in a hook reads a name behind `)/`, `}/` or `$var/` as the project root's. **A comment is not a command:** the first version flagged `# installed by context_budget.py` as running the tool; a hook line that starts with `#` never sets `runs_tool`. Two tests, one failing first (the other, not counting a tracked hook directory twice, passed on arrival); one test of mine filtered `startswith(".git")` and matched `.githooks/` too. What the 12 runs also showed, for the record: `chat_verification` and `church_growth` have older armed ledger hooks that refused the evidence script's sync commit and **accepted the migration commit**, because it carries a ledger entry; the health scores move by +1 or 0 except `chat_verification` at 48 to 45, which is the pinned `has_docs_dir` decision (it has no `docs/` of its own once `docs/methodology/` empties). Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S280 — layer 7 of P7: the tool rehearses the shard moves, flags a hook that runs a moved tool, reports a directory named in prose, and says why a small ledger is refused (117 tests pass)

Layer 7 of BL-101 P7, the code for the 11 command tests and the 36 pure-rule tests of the checkpoint before it (all 117 tests pass in about 250 s). **The rehearsal:** before the plan is shown, the tool clones the project into a throwaway directory (`git clone --no-local`), runs every shard proof there, moves all the shards and commits (`--no-verify`, a throwaway identity), runs the proofs again, and deletes the clone. A shard whose proof changes its exit code at the new place stays where it is with its proof, and the plan says so (`its proof exits 2 at the new place (0 here)`); the report carries `rehearsal: {ran, proofs, excluded}`, a project with no proofs is not rehearsed, and the rehearsal is skipped when the plan is already refused. This is what `vscode_quarto_ext`'s older-format `SESSION_NOTES-through-S253` proof needed. **A hook that runs a moved tool** (a hook line naming a moved `.py`) is marked `runs_tool`, counted in `hooks.runs_moved_tool` and warned about in the text ("will refuse the migration commit and the run will roll back; update the hook first"); the rollback on such a refusal already worked (`wsfct`) and is now a test. **A directory named in prose** (`docs/methodology/`, `docs/archive`) is a hit in `other`, including in a CLAUDE.md the tool has rewritten (read as it will be rewritten, so a path it rewrote is not counted and a directory it left is) and a CI filter on the directory; a full path is not counted twice. **A ledger too small to take its entry** is refused with its size and the reason (`the ledger is too small to take its entry and stay a rename at 90% (it holds 1341 bytes); migrate after it has more entries`). Three tests changed because behaviour changed on purpose: the CI fixture's `docs/methodology/**` filter is now a third mention, and the exit-4 test needed a proof the rehearsal cannot predict (one that depends on the newest commit's subject). The evidence script now commits the sync with `--no-verify` when an adopter's own hook refuses it, and re-runs a migration that its hook rolled back with that clone's hooks off. Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S280 checkpoint, RED on purpose — layer 7 of P7: 11 tests from what the 12 adopters showed, and 36 fast tests of the pure rules

The first run of `bin/migrate-layout` over the 12 adopters in `--no-local` clones (`docs/planning/methodology-subdirectory-evidence/migrate-12-adopters.py`; nothing in a real tree, read back after: the 11 repositories that were idle are unchanged, and `nprcgenekeepr` took the operator's own S936 commits at 17:08 to 17:17, which are not this run's) applied 8 of 12 and showed four things the fixtures could not. **(1) `vscode_quarto_ext`: one proof changes exit code (0 to 2) after the move.** `SESSION_NOTES-through-S253.md.verify.sh` is an older-format proof that reads its shard by its working-tree path (`docs/archive/...`), so it cannot find the shard at `methodology/archive/`, while the trimmer's current proofs read git history and hold; the plan's "117 of 117 proofs give the same exit codes" was measured on this repository's proofs only. The tool reported it (exit 4, `DIFFER: proofs`) and left the commit standing, as designed; the better behaviour is not to move such a shard. **(2) `wsfct`: its own pre-commit hook runs `context_budget.py` from the root, so the migration commit was refused and the tool rolled back and said why** (right, but the dry run should have warned). **(3) `claude_work`: a ledger that is only the seed (1.3 KB) falls to 68% with its entry and is rolled back.** **(4) `chat_verification` and `church_growth`: their armed hooks refused the evidence script's own sync commit** (a script fault, fixed in the script). Also seen: a prose mention of the directory `docs/methodology/` in `CLAUDE.md` stays stale after the paths in it are rewritten. **Tests, tests first and RED:** `TestTheShardRehearsal` (6: a shard whose proof would regress in a throwaway clone stays with its proof and the plan says why; the apply leaves them and the histogram is unchanged; a proof that failed before and fails the same after still moves; the rehearsal leaves no trace; none without proofs; it says how many it ran), `TestWhatTheHitsSayAboutHooksAndDirectories` (4: a hook that runs a moved tool is flagged and the text says it will refuse the commit; the rollback names the tool; a directory named in a rewritten file, and in one the tool does not edit, is reported once and a full path is not counted twice), `TestASmallLedgerIsRefusedWithAReason` (1), and `TestThePureRules` (35 fast tests of the rules as functions: `.gitignore` entries, the standing-alone rule, JSON rewriting, the entry's placement in every shape of ledger, what a check difference is, the categories, the shard names, the `.gitattributes` rule, ignore mode, what each tier plans, the directories a move empties, a staged rename) plus one on a subdirectory of a repository. **Measured RED against the layer-5 tool: 9 of the 11 new command tests fail**; the two that pass pin behaviour that already works (the rollback on a hook refusal, the case `wsfct` showed, and the rehearsal leaving no trace); the 36 pure-rule tests passed on arrival because they test existing rules, found two mistakes of mine in the tests (a key `note` with exactly a moved path IS rewritten by the rule, and an escape error) and no defect in the tool. Red between this commit and the next, on purpose. Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S280 — layer 6a of P7: `bin/sync` names `bin/migrate-layout` without the "not built yet" caveat, and the tool joins the byte-identical resolver copies

Layer 6, first part, of BL-101 P7. **`bin/sync`'s refusal of a legacy project asked for `--layout new` now says `Move the project with bin/migrate-layout (a dry run until --apply)`;** the clause "(not built yet: BL-101 phase P7)" is deleted, as S279 said P7 must, and so is the assertion that pinned it: `test_a_legacy_project_asked_for_the_new_layout_is_refused_and_the_migration_tool_is_named` in `tools/test_sync_layouts.py` now asserts the caveat is gone and that `bin/migrate-layout` exists. **`bin/migrate-layout` is added to `COPIES`** in `tools/test_layout_resolver.py`, so a drift in its embedded resolver block is a failure (the block was copied by a script and is byte-identical). Re-run: `tools/test_layout_resolver.py` Ran 75 OK, `tools/test_sync_layouts.py` Ran 81 OK, `bin/check-layout-literals` 0 sites. Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S280 — layer 5 of P7: `bin/migrate-layout --apply` verifies itself before and after, and exits 4 when a check differs (74 tests pass)

Layer 5 of BL-101 P7, the code for the 8 RED tests of the checkpoint before it (all 74 tests pass in 199 s). An apply runs the read-only checks of plan 4.7.4 on the tree before it touches anything and again after the commit: `bin/status` (TRACKED files read `current`, counted), `check-ledger` and `check-handoff` (their exit codes), `check-links --tree`, every moved shard's `.verify.sh` (the exit histogram), and how many commits `git log --follow` reaches from the ledger. **What must not change:** `status` all current, the two checkers' exit codes, the proofs' histogram, the ledger's history reaching every older commit and the move, and a clean tree. **`check-links` is reported and called informational**, because the distributed documents are authored for the old layout until P9 and a tree in the new layout reads 36 of 116 links dangling. A difference does not undo a commit that was made: the report says so, names `git revert <sha>` as the way back, and the exit is 4 (3 is a rollback, 1 a refusal, 0 clean). `--skip-checks` runs none and says so; a dry run runs none. The test helper skips the checks for every test but `TestTheChecks`, since they take about 8 s an apply. Tried first by hand: a shard the project's own trimmer wrote proves out (exit 0) before the move and at its new path after it. Two expectations of mine were wrong and fixed: the manifest has 23 TRACKED files, not 11, and the text heading reads `checks (before -> after):`. The tool's four remaining root literals are acknowledged with a reason, so `bin/check-layout-literals` reads 0 sites (154 acknowledged). Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S280 checkpoint, RED on purpose — layer 5 of P7: 8 tests for the checks an apply runs before and after

Layer 5 of BL-101 P7, tests first, `TestTheChecks` in `tools/test_migrate_layout.py` (plan 4.7.4): every check run before and after with no cell blank (`status`, `ledger`, `handoff`, `links`, `proofs`, `history`; `bin/status` reading 11 of 11 TRACKED files current on both sides, the tree clean, `ok`); the proofs of the moved shards giving the same exit histogram, one of them a real one written by the project's own trimmer and re-run at its new path; a proof that stops holding after the move (a script that reads its shard by the old path) reported with exit 4, the commit left standing and `git revert <sha>` named as the way back; the ledger's history reached across the move (`git log --follow` finds every older commit and the move's parent); `check-links` reported and called informational, since the distributed documents are authored for the old layout until P9 and a tree in the new one is expected to read differently; `--skip-checks` running none; a dry run running none; the text a person reads. Tried by hand first: the project's own `methodology_trim.py` trims the fixture's ledger, and its shard's proof exits 0 before the move and holds at the new path after it. **Measured RED against the layer-4 tool: 7 of 8 fail**; the one that passes, a dry run runs no check, is a guard that something is not done. Red between this commit and the next, on purpose. Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S280 — layer 4 of P7: `bin/migrate-layout` reports every hit it will not rewrite, by category (66 tests pass)

Layer 4 of BL-101 P7, the code for the 6 RED tests added with layer 3 (6 of 6 now pass; all 66 pass in 162 s). The report's `not_rewritten` has five categories, always all five (a category with no hit prints zero, so no cell is blank): `ci` (`.github/`, `.circleci/` and the named CI files), `harness` (`.claude/`), `hooks` (`.githooks/`), `ledger` and `other`. Each carries the count of mentions, the count of files and the sites (file, line, the line's text, the names found; the first 25 per category). **A ledger's links are counted and never listed**, since a committed entry is never rewritten and a link in one is relative to where the ledger sat when it was written; the ledger set is `CHANGELOG.md`, `HANDOFFS.md`, `SESSION_NOTES.md` and the shards, moved or not. The scan uses `git grep -F` over the tracked files for the moved names, then the same standing-alone rule as the rewrite, so a framework document the tool moves unedited and a file it rewrites are not hits. One regular expression now serves the rewrite and the scan (`token_pattern`). One test of mine passed vacuously (it asserted that files were absent from an empty list) and now asserts that the scan found the workflow first. Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S280 — layer 3 of P7: `bin/migrate-layout` rewrites the paths that follow a move and adds the one ledger entry; layer 4's tests (6) are added RED on purpose

Layer 3 of BL-101 P7, the code for the 20 tests of the checkpoint before it; the 60 tests of layers 1 to 3 pass. **Rewrites**, each shown as a diff in the dry run: `CLAUDE.md` gets every standing-alone path of a moved file rewritten (a name behind a directory, a URL, `X.mdx`, `MY_X.md`, `NOTES-X.md` and `X.bak` are not the project's file and are left); `.gitignore` gets an anchored entry that is exactly a moved path moved with it and keeps an unanchored one, which still matches; the two JSON configs are rewritten as TEXT, so every other byte is what it was: a value that is exactly a moved path (`files[].path`, `synced[].path`, `results_file`) and the tokens of a gate's `command`, never a prose key (leading underscore) and never `canonical`, the path to the sibling checkout, which does not move; after the rewrite the file is parsed and must equal the structure the rule predicts, or the migration is REFUSED (`rewrite-unsafe`) and not left half done; a config that is not JSON is moved and not edited. The map covers the generated files whether or not they are on disk, so a fresh clone still gets its `results_file` and its `/dashboard.html` entry moved. **The ledger entry:** one `### date · [ad hoc] Layout migration` entry at the top of the records zone of the ledger (under the current month's heading, with a new heading above the older month when the month has turned, above the first entry when there is no month heading, at the end with the seed sentinel dropped when there is no entry yet), in the moved ledger or, in tier 1, the root one; no ledger, no entry; check-ledger reads it clean and no line of the ledger is removed. **The 90% guard did its job on my own fixture:** a 640-byte stub `.quality-gates.json` fell to 71% on two rewritten lines and the run rolled back; the real seed carries pages of prose and a rewritten one scores R097 or R098, so the fixture is now built from the real seed. The guard's message said `90%%` and the test's `assertIn("90%")` passed anyway; both fixed. Two layer-2 tests compared the bytes of every moved file and now exclude the ledger, and a test of mine counted 8 replacements where the fixture holds 6. **Layer 4's tests, `TestTheHitsItWillNotRewrite` (6), are in this commit and RED on purpose: 6 of 6 fail** (CI, `.claude/`, `.githooks/` and README mentions, ledger links counted and never listed, none edited by an apply, every category printed when there is no hit, the text a person reads); the fixture gains a workflow, a harness rule, a hook, a README and a ledger entry that link to moved files. Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S280 checkpoint, RED on purpose — layer 3 of P7: 20 tests for the rewrites of `CLAUDE.md` and the two configs and for the one ledger entry

Layer 3 of BL-101 P7, tests first, in `tools/test_migrate_layout.py`: `TestTheRewriteOfClaudeMd` (5: a moved path or bare name rewritten and the exact expected text typed out, with a path that has a directory in front of it, a URL, `SESSION_RUNNER.mdx`, `MY_CHANGELOG.md` and `NOTES-CHANGELOG.md` left; the report's count and diff; a dry run writing nothing; tier 1 rewriting only the files it moved; a project with no `CLAUDE.md`), `TestTheRewriteOfTheConfigs` (8: the budget's `path` values following while `canonical` and the prose keys stay, as an exact expected text; the gates' `results_file` and `command` following while the `why` stays; the rewritten command still counting from the ledger's newest commit; the report naming old and new place; a fresh clone with no generated files still getting the results file and the ignore entry moved; tier 1 leaving the configs at the root; a config that is not JSON moved and not rewritten) and `TestTheLedgerEntry` (7: one entry prepended, every older line untouched, no line removed from the ledger's diff; the entry above the first entry and `bin/check-ledger` exit 0; what it says; a dry run showing it; tier 1 putting it in the root ledger; no ledger, no entry; a heading for the current month, or a new one when the month has turned; a ledger too small to take an entry and stay a rename refused and rolled back). **A test I wrote passed for the wrong reason and was rewritten before the code:** "the rewritten gate command still measures the ledger" read 0 both before and after, because right after the move the move commit is the newest commit to touch either path; it now makes a commit that touches the moved ledger and one that does not, and expects 1 (the old path would give 2). **Measured RED against the layer-2 tool: 16 of 20 fail**; the four that pass are guards that something is NOT done (a dry run does not write `CLAUDE.md`; no `CLAUDE.md`; a config that is not JSON; no ledger), which the mutation pass will aim at. Red between this commit and the next, on purpose. Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S280 — layer 2 of P7: `bin/migrate-layout --apply` moves the files in ONE commit git can follow, and rolls back what it cannot commit

Layer 2 of BL-101 P7, the code for the 19 tests of the checkpoint before it (40 of 40 now pass, about 107 s). `--apply` does the plan: `git mv` for a tracked file and a plain rename for one git does not track (a generated file `.gitignore` keeps out), the directories the moves emptied removed (never the project root, never one that still holds a file of the project's own), the anchored `.gitignore` entries that name a moved file following it (`/dashboard.html` becomes `/methodology/dashboard.html`; an unanchored `.quality-gates-results.json` still matches under `methodology/` and is left; a comment is never touched), then ONE commit through the project's own hooks (no bypass: a test hook proves it ran). **Before the commit the tool asks git for the renames of the index (`git diff --cached -M`) and refuses any tracked move that is not a rename at 90% or better**; the report carries each one's score. **A failure at any point rolls back:** `git reset --hard HEAD`, the untracked files moved home, the directories the run created removed, exit 3 and status `rolled-back` with git's own words; a test proves the tree is byte for byte what it was, the files git does not track included. The message names the tool, the tier, the canonical checkout's sha (and says when that checkout has uncommitted changes) and ends with every `--trailer`. Tier 1 moves the TRACKED rows and none of the project's state, tier 1 then tier 2 reaches the same tree as all at once, and a second run of any of them finds nothing to do and adds no commit. **Found by reading a real apply, not by a test:** the message said `90%% similarity` (a `%%` in a string that is not formatted); fixed and pinned. One test of mine indexed a dictionary by the wrong key and was fixed. Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S280 checkpoint, RED on purpose — layer 2 of P7: 19 tests for the apply (one commit, the renames git follows, the tiers, a rollback)

Layer 2 of BL-101 P7, tests first, in `tools/test_migrate_layout.py`: `TestApply` (10 tests: exactly one commit on top of `HEAD` with a clean tree after; every planned move done and a file that is not rewritten keeping its bytes; git reading each tracked move as a rename at 90% or better, the report and git agreeing; an ignored generated file moved without git and still ignored; an anchored `.gitignore` entry following its file and an unanchored one left alone, a comment undisturbed; what the tool leaves staying and only the directories it emptied going; the message naming the tool, the tier, the canonical sha and carrying every `--trailer`; `bin/status` then reading every TRACKED file `current` at its new place; a second run finding nothing to do), `TestTheTiers` (5: tier 1 moves the TRACKED files and nothing of the project's state; tier 2 alone is refused; tier 1 then tier 2 reaches the tree of all at once; all after tier 1 moves only what is left; a second tier-1 run finds nothing), `TestTheGitattributesSeed` (2: the seed moves, a file with a rule of the project's own stays and is named) and `TestARefusedCommitRollsBack` (2: a refusing hook restores the tree exactly, files git does not track included, exit 3; the hook ran, so the tool does not bypass it). The base project now carries a local git identity, as a real adopter's repository does. **Measured RED against the layer-1 tool: 18 of 19 fail**; the one that passes, `tier 2 alone is refused`, pins a layer-1 behaviour that had no test. Red between this commit and the next, on purpose. Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S280 — layer 1 of P7: `bin/migrate-layout` plans a migration as data and refuses what it must, and writes nothing

Layer 1 of BL-101 P7, the code for the 21 tests of the checkpoint before it (21 of 21 now pass, about 45 s). `bin/migrate-layout <project>` is a dry run: it checks the project, then prints the plan as text or, with `--json`, as data. **Refusals, all reported together:** not the top of a git repository, no commit, a dirty tree (any tracked change or untracked file, listed), a runner at the root and under `methodology/` (the resolver's `half`, naming both paths), a destination that exists (named), ignore mode (`.gitignore` lists a TRACKED destination, as `bin/sync` reads it), `--tier 2` before tier 1, and a tree where `bin/status` does not read every TRACKED file `current` (parsed from the table by the header's column positions, so a name with a space does not shift them; a stale-format seed is advice and not a refusal). **The plan:** one move per manifest file the project holds, from the manifest's two tables; the generated files (tracked ones and ignored ones, the latter marked a plain move); the ledger shards, only the names the trimmer writes (`CHANGELOG`, `HANDOFFS`, `SESSION_NOTES` `-through-`) and their `.verify.sh`; and what it leaves, named with a reason (a file under `docs/methodology/` that is not in the manifest, a file under `docs/archive/` that is not a shard, a `.gitattributes` that holds rules beyond the seed's, which is the project's own). Tier 1 is the TRACKED rows, tier 2 the SEED rows, the generated files and the shards. **`--apply` is not built:** with no refusal it prints an error and exits 2, so it cannot read as a pass. **Found by reading the output, not by a test:** the fixture's own `.gitignore` ignored the two history files, so the "tracked" ones were not tracked and the test asserted too little; the fixture and the test are fixed (both now assert the files are tracked). **Real data behind the rules** (a read of the 12 adopters at their `HEAD`): `nprcgenekeepr`'s `.gitattributes` is its own eol rule and not the seed, 46 of its 111 archive files are `SESSION_NOTES` shards, `model_project_constructor` keeps `PROJECT_CONVENTIONS.md` and `airqino` a nested copy of the methodology under `docs/methodology/`, five adopters track one or both of `dashboard_history.jsonl` and `.context-budget-history.jsonl`, and a rewritten config scores R091 to R098 as a rename (`vscode_quarto_ext`'s `.context-budget.json` is nearest the 90% bar at R091). Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S280 checkpoint, RED on purpose — layer 1 of P7: `bin/migrate-layout` as a skeleton and 21 tests for its usage, its dry run and its refusals

Layer 1 of BL-101 P7, tests first. `bin/migrate-layout` is a skeleton (arguments parsed, the resolver block embedded byte for byte, `{"status": "not-implemented"}`, exit 2) and `tools/test_migrate_layout.py` holds 21 tests that drive it as a command in a scratch git project the real `bin/sync` wrote and that was then committed with a ledger, a `CLAUDE.md`, both configs, a `.gitignore`, generated files, two ledger shards and two project-owned files beside the methodology ones. They cover: a missing directory (usage), a directory that is not a repository, a repository with no commits, a project with nothing to migrate (exit 0, nothing written even under `--apply`); the dry run (writes nothing, one move for each of the 30 manifest files, the two tracked history files, the ignored generated files and the ledger shards, nothing else, what it leaves named, the text a person reads); and the refusals (a modified tracked file, an untracked file, a runner in both places, a destination that exists, a locally modified and a missing TRACKED file, ignore mode, all reported together, each under a dry run and under `--apply` with the tree unchanged, and a stale-format seed as advice and not a refusal). **Measured RED against the skeleton: 21 of 21 fail (14 failures, 7 errors), each for a missing behaviour (a wrong exit code or a missing key).** The suite is red between this commit and the next, on purpose; the next commit is the tool. Model: Claude Sonnet 5.5.

### 2026-10-07 · [BL-101] S280 claim (in progress) — build the migration tool: `bin/migrate-layout` and a dry run and an apply over the 12 adopters in clones

CHANGELOG: pending. Operator said `go` as the first message; at the Phase 0 picker he approved two trims and chose BL-101 P7 (the plan's recommendation, S279's next step 1). The deliverable is the plan's section 4.7 and section 7.3 row P7 (C9, C11): `bin/migrate-layout`, canonical-only and a dry run by default, refuses a dirty tree, a half-migrated tree, a destination that exists and a tree where `bin/status` does not read every TRACKED file `current`; it prints every `git mv` from the manifest, every path rewrite in `.context-budget.json`, `.quality-gates.json`, `CLAUDE.md` and `.gitignore` as a diff, and every hit it will not rewrite; the apply is one commit with every moved file at 90% similarity or better and no committed ledger entry or frozen shard rewritten; then a dry run and an apply in a `--no-local` clone of each of the 12 adopters, one report row each. Already done before this claim, each recorded above: the `CHANGELOG.md` trim (`00f0807`, 132 records to `CHANGELOG-through-2026-10-06.md`, 279,349 B to 131,647 B because the file had passed the 262,144 B hard refusal, which made the dashboard's risk HIGH), the owed `HANDOFFS.md` trim (`8d327c6`, S277 to `HANDOFFS-through-2026-10-07.md`) and its fold (`114ea92`), both shard proofs exit 0 from `--no-local` clones of their own commits, and `bin/tests.sh` in a clean clone of `114ea92`: 475 passed, 0 failed, 6 skipped at two receipts (S279's baseline exactly), Test 30 and Test 31 non-vacuous, Test 40 666 = 666. Phase 0: 0 undocumented commits at the `CHANGELOG.md` frontier, `HANDOFFS.md` one commit past its frontier (the CHANGELOG-only push record), 0 merges; #94, #92 and #93 without a maintainer reply; gate run 17/17, results `664fb7d88e19`, manifest `082ea8d9aad8` (S279's citation exactly); dashboard health 72. Phase 3F records the rest. Model: Claude Sonnet 5.5.

### 2026-10-07 · [ad hoc] S280 — fold the 2026-10-07 HANDOFFS shard pointer into the archive index

The pointer block the trim (`8d327c6`, 1 receipt, S277, 2026-10-07, to `HANDOFFS-through-2026-10-07.md`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, trimmer v1.8.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S279, S278). Both shard proofs were run by name from `--no-local` clones of their own trim commits: `CHANGELOG-through-2026-10-06.md.verify.sh` at `00f0807` and `HANDOFFS-through-2026-10-07.md.verify.sh` at `8d327c6`, each exit 0. Model: Claude Sonnet 5.5.

### 2026-10-07 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-07.md` (1 record(s), 40,433 B → 29,117 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-07 → 2026-10-07) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-07.md`](docs/archive/HANDOFFS-through-2026-10-07.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-07.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-07.md.verify.sh)
rather than trusting a digest printed here. Live file 40,433 B → 29,117 B (−28.0%).

### 2026-10-07 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-10-06.md` (132 record(s), 279,349 B → 131,647 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **132** record(s) (2026-10-05 → 2026-10-06) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-10-06.md`](docs/archive/CHANGELOG-through-2026-10-06.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-10-06.md.verify.sh`](docs/archive/CHANGELOG-through-2026-10-06.md.verify.sh)
rather than trusting a digest printed here. Live file 279,349 B → 131,647 B (−52.9%).

