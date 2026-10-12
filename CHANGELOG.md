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

---

## 2026-09

## 2026-10

### 2026-10-11 · [BL-101] S298 — P17 on `vscode_quarto_ext` at tier all, done in its own repository and recorded; findings F23 and F24

**Done in `~/Development/vscode_quarto_ext`** (a VS Code extension: 430 tracked files, 4,583 unit tests, no hook, no CI, two declared gates, a 66 GB untracked `scratchpad/` it deliberately leaves unignored; his pick, the only adopter with no live session and a clean tracked tree; at one picker after the rehearsal he chose tier all, a local exclude for the scratchpad, and the run). **Three local commits there, none pushed** (`master` is 3 ahead of `origin/master`; its push is its own go-ahead): `9a53b909` (`methodology/**` in its `.vscodeignore`, with a ledger entry in its own format), `a5b0ed9d` (the sync from this checkout at `8df554b`: 21 updated, `.gitattributes` created, 2 unchanged, nothing refused, no `--force`) and `e35d1657` (`bin/migrate-layout --tier all`: 36 renames, 33 at 100%, `.context-budget.json` 92%, `.quality-gates.json` 96%, `CHANGELOG.md` 99%, and `CLAUDE.md` 21 lines; the dry run read first, exit 0, no refusal and no warning). **The local exclude** (`/scratchpad/` in the adopter's `.git/info/exclude`) was restored from a copy afterwards: sha256 equal, `?? scratchpad/` back; the non-tracked files (`dashboard.html`, `.quality-gates-results.json`, the `.pyc`) have the same sha256 before and after. **Measured in 6 `--no-local` clones and in a fresh clone of the result** (record `p17-vscode-quarto-ext-record.md`, evidence `p17-adopter-runs/`): the tool's checks read the same before and after (status 23/23, ledger 78 findings and handoff exit 1 both the adopter's own, proofs 2 to 2, dashboard 76 to 76); `links` 0 to 18 project links at tier all (6 in ledger headers, F9) and 0 to 4 at tier 1 (F13); **as the tool leaves it the project's own `release-gate` reads 78 files against 42 (tier 1: 65) with 4,583 tests passing**, and with the one `.vscodeignore` line before the move it reads 42 files, ratchet 2/2 and a `vsce package` of 44 entries and 1,935,373 B, identical before and after; the `ledger-lag` gate follows the ledger (a later commit with no entry reads 1, with an entry 0, before and after). **Findings:** F23 (a clone under a path containing `scratchpad` makes vsce list nothing: fixed in both scripts) and F24 (the tool lists `.vscodeignore` and does not evaluate it: open, his call; plan §7.6 puts it before the next adopter unless he says otherwise). **Here:** the record, the evidence, the two scripts, register rows F23 and F24 and a dated line, plan §7.4g (recomposed to 59,997 of 60,000 B; about a dozen cuts to fit, listed in the commit message), the BL-101 row (56,717 of 56,750 B) and the BACKLOG-DETAIL P17 paragraph and Next action. Not shown: `test:integration`, `test:lsp` and a push or CI. Nothing went upstream, no tag. Model: Claude Sonnet 5.5.

### 2026-10-11 · [BL-101] S298 — P17 rehearsed in six clones of `vscode_quarto_ext`; the real run waits on his picks

`docs/planning/methodology-subdirectory-evidence/p17-rehearsal.sh` ran six `--no-local` clones of the adopter at `507b9348` (430 tracked files; no hook, no CI; its own gates `ledger-lag` and `release-gate` = `npm run check-package`), serially, outside any path containing `scratchpad` (its `.vscodeignore` line `scratchpad/**` makes vsce list nothing for a clone under such a directory: measured, `check-package` read 0 files). **Measured:** `npm test` reads 68 files and 4,583 tests passing in EVERY arm, before and after; `bin/sync` refuses nothing (no `--force`); the sync alone changes no result (`.gitattributes` is not packaged: 42 files). **As the tool leaves it, tier 1 and tier all:** `check-package` FAILS, 65 and 78 files against 42 (6.67 and 9.90 MB against 5.66 MB), `release-gate` red, ratchet 1/2, while every check the tool prints reads green; the adopter's own declared gate is what catches it (F20's shape, second instance). **With `methodology/**` added to `.vscodeignore` in its own commit before the move (arms `t1A`, `tallA`):** 42 files, ratchet 2/2, `vsce ls` identical to the base; a real `vsce package` before and after gives 44 entries and 1,935,373 B each, entry lists identical. **The tool's checks, identical across arms:** status 23/23, ledger exit 1 to 1 (78 findings, the adopter's own), handoff exit 1 to 1, proofs 2 to 2, `ledger-lag` command rewritten to the new path and passing, dashboard 76 to 76; `links` 0 to 4 at tier 1 (F13) and 0 to 18 project links at tier all (F9, by design); `CLAUDE.md` 29 replacements, none in its Learnings pointer. Run 1 (kept as `rehearsal-run1-log.txt`) carried a needless `.gitattributes` line in `.vscodeignore`; run 2 is the corrected set. **Nothing was changed in the adopter; nothing was pushed; nothing went upstream.** Evidence: `p17-adopter-runs/`. Model: Claude Sonnet 5.5.

### 2026-10-11 · [BL-101] S298 claim (in progress) — P17 on `vscode_quarto_ext`

CHANGELOG: pending. Operator said `go`; the Phase 0 report named `vscode_quarto_ext` as the only free adopter, and he picked "P17 on vscode_quarto_ext" with the go-aheads "Trim HANDOFFS.md" and "Push 0a2921d to fork" (one picker answer). Checked at the claim with `pgrep -x claude` and `lsof -a -p <pid> -d cwd`: no session in `vscode_quarto_ext` (`wsfct`, `mts-system` and `nprcgenekeepr` each have one); its tracked tree is clean, HEAD `507b9348` on `master`, level with `origin/master`, one untracked path, `scratchpad/` (66 GB, not ignored), which the tool counts as dirt. The gate citation of S297 (results `791e005997ab`, manifest `e755389a69c7`) was re-run in a clean `--no-local` clone of `0a2921d` and confirmed (18/18, 0 unmeasured). The push (`0a2921d`), the owed HANDOFFS trim (`2c64088`) and its fold (`c577437`) were done before this claim. Deliverable: one adopter session in its own repository, tier his pick after the clone rehearsal; nothing pushed upstream. Model: Claude Sonnet 5.5.

### 2026-10-11 · [ad hoc] S298 — fold the first 2026-10-11 HANDOFFS shard pointer into the archive index

The pointer block the trim (`2c64088`, 1 receipt, S295, 2026-10-11, to `HANDOFFS-through-2026-10-11.md`, the name S297 guessed and the dry run chose) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, trimmer v1.8.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S297, S296). The shard proof was run by name in the tree before the trim commit and from a `--no-local` clone of `2c64088`: `HANDOFFS-through-2026-10-11.md.verify.sh`, exit 0 both times (L1, L2/front-matter, L3). The trim ran on his go-ahead at the S298 Phase 0 (a picker answer: "Trim HANDOFFS.md"), after the push of `0a2921d` to the fork `origin`. Nothing went upstream. Model: Claude Sonnet 5.5.

### 2026-10-11 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-11.md` (1 record(s), 39,898 B → 28,465 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-11 → 2026-10-11) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-11.md`](docs/archive/HANDOFFS-through-2026-10-11.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-11.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-11.md.verify.sh)
rather than trusting a digest printed here. Live file 39,898 B → 28,465 B (−28.7%).

### 2026-10-11 · [ad hoc] S298 — pushed `0a2921d` to the fork `origin` (push record)

On his go-ahead at the S298 Phase 0 (a picker answer: "Push 0a2921d to fork"): `git push origin 0a2921d:refs/heads/main`, naming the commit and not `HEAD`; `origin` is `https://github.com/rmsharp/methodology.git`, the fork. Five commits went (`e6945f0`, `583e771`, `59887b4`, `2b65098`, `0a2921d`; `a61ec17..0a2921d`). Read back before the trim: `git rev-list --left-right --count origin/main...main` read `0 0` and `git ls-remote origin refs/heads/main` equalled `0a2921d`. Nothing went upstream (`KJ5HST/methodology`), no tag, no release. Model: Claude Sonnet 5.5.

### 2026-10-11 · [BL-101] S297 close-out — P16 on `chat_verification` at tier all (receipt complete)

Receipt S297 is `status: complete` (self 8, predecessor 9; no fork learning row appended, so no retirement is owed: the rows considered are named in the receipt, fork #57, #80 and #39). `CHANGELOG: pending` on the S297 claim entry is cleared by this statement (a committed entry is not edited). **The deliverable:** P16, the sixth adopter, at tier all in `~/Development/chat_verification` (five local commits there, none pushed: it has no remote), recorded in `p16-chat-verification-record.md`, plan §7.4f and register rows F21 and F22; the two entries above this one have the figures. **Gate run:** `quality_ratchet.py --run` in a clean `--no-local` clone of `2b65098`, 18/18 pass, 0 fail, 0 unmeasured, results `791e005997ab`, manifest `e755389a69c7` (the same hashes as S296's citation: no gate threshold moved and none was loosened). **Ledgers:** `HANDOFFS.md` holds 3 receipts (S297, S296, S295), so one trim is owed after the next Phase 0 (one record, S295); `CHANGELOG.md` is far under its 196,608 B trigger. **Local commits here:** `e6945f0`, `583e771`, `59887b4`, `2b65098` and this close-out; nothing was pushed, nothing went upstream, no tag. **Open and his:** the F21 tool fix, P17, F6, F8, F13, F14, F17, F19, D8. Model: Claude Sonnet 5.5.

### 2026-10-11 · [BL-101] S297 — P16 on `chat_verification` at tier all, rehearsed in clones and then done in its own repository (plan §7.4f)

**Done in `~/Development/chat_verification`** (a doc-only content repository: 36 tracked files, no remote, tests, CI or gate, a tracked older ledger hook, its own S9 claim still `pending`; his pick, out of plan order, with two go-aheads: the owed HANDOFFS trim and the preparation of the tree). Five local commits there, none pushed (it has no remote): its one modified tracked `dashboard_history.jsonl` committed as the F12 remedy (`b41fb8d`, with a ledger entry because its old hook demands one), the sync from this checkout at `59887b4` (`ee28226`: 19 updated, 4 created, 2 unchanged, nothing refused, no `--force`), its ledger hook replaced with this repository's (`a3174b3`), the move at `--tier all` (`ebbfabd`: 33 files, 32 renames of which 29 at 100%, `dashboard.html` moved plainly, `CLAUDE.md` 14 replacements on 8 lines) and the correction of the tool's ledger entry (`0a8ef90`; made once as `7823e31` and redone before any other step, unpushed, to correct a count in its own entry: 14 ledgers to 12). **Measured** in 6 `--no-local` clone arms (`p16-rehearsal.sh`, its second probe bug fixed and the run repeated before the real apply) and a fresh clone of the result (`p16-final-clone.sh`): **a later commit with no ledger entry exits 0 under the old hook after the move and 1 under the replaced one** (the unmoved control: 1); the tool's own checks, its `context_budget.py` (exit 2 both ways: `SESSION_NOTES.md` 1,113 lines against 400, its BL-15) and `check-ledger` (83 findings) read the same before and after; `dashboard.html` and the `__pycache__` pyc are sha256-identical; 0 links dangle (tier 1: 0 to 4, F13 again); the dashboard reads 49 before and 45 after. **Findings, register rows F21 and F22:** F21 **the tool put its own ledger entry inside an example code fence in the ledger header** (`bin/migrate-layout:362-376` inserts above the first dated heading in the file), no check of the tool saw it, and of the 12 committed ledgers on this machine it is the only one with a fence first; moved by hand there (the replaced hook accepts it, measured in a clone first), the tool fix open for him; F22 the dashboard's 4 points are the `has_docs_dir` credit plan §7.2d stated at P5, declined by design. **My post-rehearsal report to him called the dashboard drop new; it was a stated cost** (§7.2d, found while recomposing the plan). **Here:** the record `p16-chat-verification-record.md`, `p16-rehearsal.sh`, `p16-final-clone.sh` and `p16-adopter-runs/` (the evidence); the plan, register and backlog edits are the next entry. Nothing was pushed, tagged or sent upstream. Model: Claude Sonnet 5.5.

### 2026-10-11 · [BL-101] S297 — the plan, the register and the backlog record P16

`docs/planning/methodology-subdirectory-plan.md` gains §7.4f and its status line (P0 to P16 done, P17 next) and the order list names P16; **it stays under its 60,000 B budget only because I recomposed it on my own judgment, and say what went** (59,985 B to 59,986 B): the sentence "22 to 29 sessions by this table (about 25)" (it is §0 item 1), §7.1's clause about a first grep that could not be reproduced and its "a ratchet gate per new suite" clause, the "Not shown" tails of §7.2c, §7.2d, §7.3a, §7.3c and §7.3d, the "no remote, tests, CI or gates" lists of §7.4b and §7.4d, "pushed 2026-10-10" in §7.4c, and the restored-after detail of §7.4e; "tier 1 until it is surveyed (his, S285)" in the DONE list now reads "the tier is his pick (1 at P11, all after)", which is what P12 to P16 did. `findings-register.md` gains rows F21 and F22, a dated S297 line and a recomposed "Read at the next adopter session" paragraph (F21 added). `BACKLOG.md` BL-101 row (56,103 of 56,750 B) and `BACKLOG-DETAIL.md` gain P16 and the next action P17; the row's stale "nprcgenekeepr is five commits ahead" now reads pushed. Model: Claude Sonnet 5.5.

### 2026-10-11 · [BL-101] S297 claim (in progress) — P16 on `chat_verification` at tier all

CHANGELOG: pending. Operator said `go`; the Phase 0 report found no adopter that was both free and clean, and he picked "P16 on chat_verification" with the go-aheads "trim HANDOFFS" and "prepare the tree" (one picker answer, after asking what option 1 meant). Checked at the claim with `pgrep -x claude` and `lsof -a -p <pid> -d cwd`: no session in `chat_verification`; its tree has one modified file, `dashboard_history.jsonl` (one snapshot line, 2026-08-12), HEAD `107cbed` on `main`, no remote. The gate citation of S296 (results `791e005997ab`, manifest `e755389a69c7`) was re-run in a clean `--no-local` clone of `a61ec17` and confirmed (18/18, 0 unmeasured). The owed HANDOFFS trim (`e6945f0`, S294 to `HANDOFFS-through-2026-10-10-4.md`, the proof exit 0 in the tree and from a clone) and its fold (`583e771`) were done before this claim. Deliverable: one adopter session in its own repository, recorded here; nothing pushed, nothing upstream. Model: Claude Sonnet 5.5.

### 2026-10-11 · [ad hoc] S297 — fold the fourth 2026-10-10 HANDOFFS shard pointer into the archive index

The pointer block the trim (`e6945f0`, 1 receipt, S294, 2026-10-10, to `HANDOFFS-through-2026-10-10-4.md`, the name the dry run chose because `-3` was taken) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, trimmer v1.8.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S296, S295). The shard proof was run by name from a `--no-local` clone of the trim commit: `HANDOFFS-through-2026-10-10-4.md.verify.sh` at `e6945f0`, exit 0 (L1, L2/front-matter, L3). The trim ran on his go-ahead at the S297 Phase 0 (a picker answer: "trim HANDOFFS"); nothing was pushed and nothing went upstream. Model: Claude Sonnet 5.5.

### 2026-10-11 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-10-4.md` (1 record(s), 40,017 B → 28,264 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-10 → 2026-10-10) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-10-4.md`](docs/archive/HANDOFFS-through-2026-10-10-4.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-10-4.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-10-4.md.verify.sh)
rather than trusting a digest printed here. Live file 40,017 B → 28,264 B (−29.4%).

### 2026-10-11 · [BL-101] S296 — push record: main pushed to the fork origin at his go-ahead (7a3e84c..3af7f9a)

At his word ("push main to origin") `git push origin main` sent one commit (a plain fast-forward, `7a3e84c..3af7f9a`) to `rmsharp/methodology`: `3af7f9a`, the correction of the S296 receipt's next steps (1)(b) and (5). After a fetch `git rev-list --left-right --count origin/main...main` read `0 0`. Nothing went to `KJ5HST/methodology`, no tag. The previous entry's line that `3af7f9a` is local and not pushed is therefore historical. This commit changes only `CHANGELOG.md` and is pushed too, under his standing grant for push records, so no further record is owed. Model: Claude Sonnet 5.5.

### 2026-10-11 · [BL-101] S296 — the close-out receipt's next steps (1)(b) and (5) corrected after the adopter push and the push of `main`

The S296 receipt in `HANDOFFS.md` was written before two pushes the entries above record, so its `next_steps` still offered the push of `nprcgenekeepr`'s commits as open (1)(b) and listed this repository's commits as local (5). Both lines now say **DONE after this receipt, on his go-ahead** and give the ranges (`a8b884c81..5a41dbbdd` in the adopter, `98056a5..1434660` and then `7a3e84c` here) and the CI result; the rest of the receipt, including its narrative lines that nothing was pushed (true when written), is unchanged. One line of `HANDOFFS.md` changed (the same correction S295 made to its own receipt); `bin/check-handoff` and `bin/check-ledger` exit 0. **This commit is local and not pushed:** it changes `HANDOFFS.md`, which the standing grant for push records does not cover, so `main` is one commit ahead of `origin/main` until he says to push. Model: Claude Sonnet 5.5.

### 2026-10-11 · [BL-101] S296 — push record: main pushed to the fork origin at his go-ahead (98056a5..1434660)

At his word ("push main to origin") `git push origin main` sent nine commits (a plain fast-forward, `98056a5..1434660`) to `rmsharp/methodology`: S295's `043a741`, `d548de5` and `6146b5f`, S296's `278b507`, `1bbf5da`, `19b9882`, `1bb690f` and `e24135e`, and the previous entry's push record `1434660`. After a fetch `git rev-list --left-right --count origin/main...main` read `0 0`. Nothing went to `KJ5HST/methodology`, no tag. The previous entry's and the S296 close-out entry's lines that these commits are local and not pushed are therefore historical: the go-ahead came after they were written. This commit changes only `CHANGELOG.md` and is pushed too, under his standing grant for push records, so no further record is owed. Model: Claude Sonnet 5.5.

### 2026-10-11 · [BL-101] S296 — push record: `nprcgenekeepr` pushed to its `origin` at his go-ahead (`a8b884c81..5a41dbbdd`), and its four CI workflows read green

At his word ("push the nprcgenekeepr commits") `git push origin master` in `~/Development/nprcgenekeepr` sent five commits to `rmsharp/nprcgenekeepr`, a plain fast-forward (`a8b884c81..5a41dbbdd`): the four from P15 (`4f67cb927` sync, `74804498a` nine of its own files edited, `0e2663642` the move at tier all, `5a41dbbdd` its trimmer addition put back) and `3004914aa`, the adopter's own earlier push record (a two-line `CHANGELOG.md` change), which was already local and cannot be left behind by a fast-forward. After a fetch `git rev-list --left-right --count master...origin/master` read `0 0`. **CI on `5a41dbbdd`, read with `gh run list` and `gh run view` (started 22:42Z, all done by 23:07Z):** `lint.yaml` (run 38181477776) success, `pkgdown.yaml` (38181477741) success, `test-coverage.yaml` (38181477746) success, `R-CMD-check.yaml` (38181477747) success in all five jobs (ubuntu-latest oldrel-1, release and devel; macos-latest release; windows-latest release). These are the adopter's first CI runs on the moved layout; the previous green runs were on `a8b884c81`. **Not done:** no commit was added in the adopter for this push (its own `CHANGELOG.md` carries no push record for it; that is its convention, his call), and nothing went to `KJ5HST/methodology`. The S296 receipt's line that the adopter's commits are not pushed is therefore historical. **This entry's commit is local and is not pushed:** the standing grant covers a push record alone, and a push of `main` would also send the eight earlier local commits (`043a741` through `e24135e`), which he has not asked for. Model: Claude Sonnet 5.5.

### 2026-10-11 · [BL-101] S296 close-out — P15 on `nprcgenekeepr` at tier all (receipt complete)

Receipt S296 is `status: complete` (self 8, predecessor 9; no fork learning row appended, so no retirement is owed: the rows considered are named in the receipt, fork #39, #57 and #58). `CHANGELOG: pending` on the S296 claim entry is cleared by this statement (a committed entry is not edited). **The deliverable:** P15, the fifth adopter, at tier all in `~/Development/nprcgenekeepr` (four local commits there, not pushed), recorded in `p15-nprcgenekeepr-record.md`, plan §7.4e and register rows F17 to F20; the entry above this one has the figures. **Gate run:** `quality_ratchet.py --run` in a clean `--no-local` clone of `1bb690f`, 18/18 pass, 0 fail, 0 unmeasured, results `791e005997ab`, manifest `e755389a69c7` (the same hashes as S295's citation: no gate threshold moved and none was loosened). **Ledgers:** `HANDOFFS.md` holds 3 receipts (S296, S295, S294), so one trim is owed after the next Phase 0 (one record, S294); `CHANGELOG.md` is far under its 196,608 B trigger. **Local commits here:** `043a741`, `d548de5`, `6146b5f`, `278b507`, `1bbf5da`, `19b9882`, `1bb690f` and this close-out; nothing was pushed, nothing went upstream, no tag. **Open and his:** the push of the adopter's four commits (its own go-ahead; its CI will run), P16, F6, F8, F13, F14, F17, F19, D8. Model: Claude Sonnet 5.5.

### 2026-10-11 · [BL-101] S296 — P15 on `nprcgenekeepr` at tier all, rehearsed in clones and then done in its own repository (plan §7.4e)

**Done in `~/Development/nprcgenekeepr`** (an R package; his pick once its session had ended; four local commits there, not pushed, `master` five ahead of `origin/master`): the sync from this checkout at `19b9882` (`4f67cb927`, 21 files updated, `--force` for the one file the sync refused), nine of the project's own files edited before the move (`74804498a`), the move at `--tier all` (`0e2663642`: 143 renames, 140 at 100%, `CLAUDE.md` 27 replacements, 4 ignored generated files moved plainly with identical sha256) and the project's own 49-line trimmer addition put back at `methodology/methodology_trim.py` (`5a41dbbdd`). The untracked per-clone hook `.git/hooks/pre-commit` was rewritten with `context_budget.py install-hook` before the apply (the old one, a root path to `context_budget.py`, rolls the apply back: exit 3). **Measured** over 7 `--no-local` clone arms (`p15-rehearsal.sh`) and a fresh clone of the result, with the project's own full R suite (`p15-r-full.R`, 5.8 minutes each) and its own gate command: unsynced, synced and tier 1 read 11,017 tests, 10,824 passed, 0 failed, 187 skipped; **tier all as the tool leaves it** 0 failed, 189 skipped, and a package tarball of 8,494,054 B against 3,775,455 B (the project's gate: 5,000,000 B), because `.Rbuildignore` covers none of the 143 moved files; **after the nine edits** 11,040 tests, 0 failed, 187 skipped, tarball 3,775,628 B, the gate `1/1 pass`, the dashboard 96 and risk 0 as before. The tool's checks read the same before and after except 110 of the project's own links dangling (4 at tier 1). **Findings, register rows F17 to F20:** F17 the `hooks` row warns about the layout-aware hook the installer itself writes (false; open), F18 an untracked per-clone hook that runs a moved tool rolls the apply back (seen, loud, fixed by design), F19 a forced sync drops a project's own addition to a distributed file (`methodology_trim.py` is canonical `d7768cbeb` plus 49 lines: `NO_CONFIG` where 38 of 39 records were planned; open), F20 tier all on a package ships the moved files and skips a test unless the project's own files are edited first (fixed there). Dated lines under F2, F7, F8, F9, F13; F12 did not arise. **This repository:** the plan (`docs/planning/methodology-subdirectory-plan.md`, 59,957 B to 59,985 B of its 60,000 B) gains §7.4e and the status line, its DONE list names per-clone hooks and the adopter's declared gates, §7.3's two bullets are folded into §7.3a and §7.3b (their one unique sentence kept) and §7.1's Boundary bullet is dropped (the scanner is a gate, not RED); `BACKLOG.md`'s BL-101 row is recomposed (its P2 to P6 narrative, which the plan's §7.2a to §7.2e carry, cut to a pointer: 56,716 B to 55,352 B) and gains P15; `BACKLOG-DETAIL.md` gains the P15 paragraph and a rewritten Next action; the record, the register rows and the raw outputs are `docs/planning/methodology-subdirectory-evidence/p15-nprcgenekeepr-record.md`, `findings-register.md` and `p15-adopter-runs/`. **Not done:** a push of the adopter's commits (its own go-ahead; CI will run), a live GitHub run of its four filters, `R CMD check`, anything upstream, D8, a tag, tier 2 on `model_project_constructor`. Model: Claude Sonnet 5.5.

### 2026-10-11 · [BL-101] S296 claim (in progress) — P15 on `nprcgenekeepr` at tier all

CHANGELOG: pending. Operator said `go`; at the Phase 0 report P15 was off the list (`nprcgenekeepr`, `mts-system`, `vscode_quarto_ext` and `wsfct` each had a live `claude` session, and `Philippians`, `dalia_martinez_funeral` and `chat_verification` were dirty). He then asked whether P15 could run if he got `nprcgenekeepr` clean and out of a session, and chose "P15 on nprcgenekeepr at tier all"; checked after that answer and again before this claim with `pgrep -x claude` and `lsof -a -p <pid> -d cwd`: no session there, its tree clean (0 files) at `3004914aa` on `master`. He also gave the go-ahead for the owed HANDOFFS trim (`278b507`) and its fold (`1bbf5da`, entries below), both done before this claim. The gate citation of S295 (results `791e005997ab`, manifest `e755389a69c7`) was re-run in a clean `--no-local` clone of `6146b5f` and confirmed (18/18, 0 unmeasured). Deliverable: one adopter session in `~/Development/nprcgenekeepr` (plan §7.4, Development workstream), recorded in a `p15-nprcgenekeepr-record.md` beside the P14 record and in the findings register. Its push, anything upstream, F6, F8, F13, F14, D8 and a push of this repository's local commits are not part of it. Phase 3F records the rest. Model: Claude Sonnet 5.5.

### 2026-10-11 · [ad hoc] S296 — fold the third 2026-10-10 HANDOFFS shard pointer into the archive index

The pointer block the trim (`278b507`, 1 receipt, S293, 2026-10-10, to `HANDOFFS-through-2026-10-10-3.md`, the name the dry run chose because `-2` was taken) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, trimmer v1.8.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S295, S294). The shard proof was run by name from a `--no-local` clone of the trim commit: `HANDOFFS-through-2026-10-10-3.md.verify.sh` at `278b507`, exit 0 (L1, L2/front-matter, L3). The trim ran on his go-ahead at the S296 Phase 0 (a picker answer: "Yes, trim, then claim and start P15"); nothing was pushed and nothing went upstream. Model: Claude Sonnet 5.5.

### 2026-10-11 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-10-3.md` (1 record(s), 40,819 B → 29,413 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-10 → 2026-10-10) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-10-3.md`](docs/archive/HANDOFFS-through-2026-10-10-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-10-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-10-3.md.verify.sh)
rather than trusting a digest printed here. Live file 40,819 B → 29,413 B (−27.9%).

### 2026-10-11 · [ad hoc] S295 — the close-out receipt's next steps (2) and (5) corrected after the push and the CHANGELOG trim

The receipt `status: complete` in `HANDOFFS.md` (committed in `98056a5`) was written before the entry below it: its step (2) named the `CHANGELOG.md` trim as owed and its step (5) named 5 commits as unpushed. Both were then done on his go-ahead (the push of `98056a5`; the trim `043a741`, forced past `SRF_RED`), so a successor reading only the newest receipt would start from a stale state. Step (2) now reads "ONE TRIM OWED" (the `HANDOFFS.md` trim, 3 receipts) with the changelog trim recorded as done and its rate uncut (about 13 sessions to the trigger, an estimate); step (5) names `043a741` and the entry below as the local commits. `check-handoff` exit 0 (record under its 12,288 B budget). No other field changed. Model: Claude Sonnet 5.5.

### 2026-10-11 · [ad hoc] S295 — push of the close-out to the fork, and the CHANGELOG trim forced past SRF_RED, on his go-ahead

After the close-out `98056a5`, at his go-ahead (a picker: "push 5 commits to the fork" and "CHANGELOG trim now"): **the push** of `98056a5` to the fork `origin` by name, read back `0 0` and equal by `ls-remote` (it carried the trim `4b631e7`, its fold `e0aa384`, the claim `bb7151d`, the F12 record `904e17e` and the close-out); nothing went upstream. **The trim** `043a741`: `CHANGELOG.md` had passed its trigger (199,040 B against 196,608 B), the dry run refused with `SRF_RED` (SRF 1.1183 against the last archive `40c3694`, which had left the file at 78,034 B on 2026-10-08: it grew back 121 KB in three days), and the plan's rule for RED is "do not archive again" (`framework-context-cost-plan.md` section 3.3). I ran it with `--force`, as the ledger's earlier changelog trims were (`CHANGELOG-through-2026-08-09.md`, `--cut 2026-08-02 --force`), after a forced dry run read 88 of 157 records and 199,040 B to 99,197 B: shard `docs/archive/CHANGELOG-through-2026-10-08.md` (cut key 2026-10-08 straddles a day, so the name is a span label); the proof exit 0 in the tree and from a `--no-local` clone of `043a741`. **The rate was not cut:** SRF RED says the next deliverable is a rate cut, and at this ledger's recent rate (about 7.5 KB a session, an estimate) the trigger is about 13 sessions away again. No fold is needed: a changelog shard's pointer block stays in its own front matter. The trim and this entry are local (2 commits ahead of the fork). The S295 receipt's next step (2) names this trim as owed: it is done here; the `HANDOFFS.md` trim (3 receipts) is still owed. Model: Claude Sonnet 5.5.

### 2026-10-11 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-10-08.md` (88 record(s), 199,040 B → 99,197 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **88** record(s) (2026-10-07 → 2026-10-08) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-10-08.md`](docs/archive/CHANGELOG-through-2026-10-08.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-10-08.md.verify.sh`](docs/archive/CHANGELOG-through-2026-10-08.md.verify.sh)
rather than trusting a digest printed here. Live file 199,040 B → 99,197 B (−50.2%).

### 2026-10-11 · [BL-101] S295 close-out — F12 closed with no tool change; the receipt is complete

Receipt S295 is `status: complete` (self 7, predecessor 9; no fork learning row appended, so no retirement is owed: the rows considered are named in the receipt, fork #57, #71, #80 and #60). `CHANGELOG: pending` on the S295 claim entry is cleared by this statement (a committed entry is not edited). **The deliverable:** F12, the dirty-tree refusal and generated files in `bin/migrate-layout`, settled by a measurement over the 8 adopters not yet moved (the rule the row describes clears 0 of 8; the two adopters with a generated file in their dirt carry a modified tracked `dashboard_history.jsonl`, a case the rollback would destroy, and both also fail `[not-current]`) and his choice to decline with no tool change; the record, the script, its output and the register line are in `904e17e` (the entry below). **What this commit adds:** the receipt, this entry and the BL-101 Next action in `docs/planning/BACKLOG-DETAIL.md` (F12 declined, the S295 live-session note). **One breach of my own, stated:** F12 went first in the Phase 0 picker on an estimate I labelled unmeasured and had not tested, and he picked it on that (fork #57's lesson, a second session running); the measurement reversed the estimate and is in the record and the receipt. **Gate run:** quality_ratchet: 18/18 pass · 0 fail · 0 unmeasured · results 791e005997ab · manifest e755389a69c7 (the gate run in a clean `--no-local` clone of `904e17e`, about 15 minutes at a load of about 6, so no gate reached BL-103's 600 s limit; the close-out commit adds only this receipt, its ledger entry and the BL-101 Next action in `BACKLOG-DETAIL.md`; tests-sh-passed read 483 at three receipts, floor 477; migrate-layout-unit-tests 186, floor 186) **Pushes:** `9bd6f83` went to the fork `origin` at the start of the session on his go-ahead (recorded in the fold entry below); the 5 commits after it (the trim, its fold, the claim, the F12 record and this close-out) are local, and nothing went upstream. `CHANGELOG.md` has passed its 196,608 B trim trigger (196,773 B before this entry): the trim is owed as its own action after the next Phase 0 report, with his go-ahead. Model: Claude Sonnet 5.5.

### 2026-10-11 · [BL-101] S295 — F12 measured over the adopters and declined: the dirty-tree refusal stays

Register row F12 (`docs/planning/methodology-subdirectory-evidence/findings-register.md`): should `bin/migrate-layout` count generated files it moves as not-dirt? Measured read-only over the 8 adopters not yet moved (`f12-measure-dirt.py`, output `f12-measure-output.txt`): the rule the row describes (untracked generated files) leaves **0 of 8** trees clean; the two adopters whose dirt is a generated file, `mts-system` and `chat_verification`, carry a **modified tracked** `dashboard_history.jsonl`, and a rule covering it would clear exactly those two, which the tool's dry run still refuses for `[not-current]` (11 framework files behind or missing in each). The modified file is the costly case, shown in a scratch repository: after `git mv` and the commit it reads ` M` at the new path (the tool would exit 4), and the rollback's `reset --hard HEAD` deletes the adopter's line. **My Phase 0 estimate that F12 would unblock those two was wrong for the rule as written**; he saw the correction and four options and chose to decline with no tool change. Written: the record `f12-dirty-tree-record.md`, the script and its output, a dated register line and the row's status cell. The tool did not change, no floor moved, nothing went upstream. Rows F10, F15 and F16 still read **open** in the register's last cell though their dated lines say fixed or declined: noted there, left for his triage. The BL-101 Next action in `BACKLOG-DETAIL.md` follows in the close-out commit. Model: Claude Sonnet 5.5.

### 2026-10-11 · [BL-101] S295 claim (in progress) — F12, the dirty-tree rule in `bin/migrate-layout`

CHANGELOG: pending. Operator said `go`; at the Phase 0 picker he chose F12 as the deliverable and gave two go-aheads (the owed HANDOFFS trim and a push of 5 commits to the fork; both done, entries below). P15 was not possible: `nprcgenekeepr`, `mts-system`, `vscode_quarto_ext` and `wsfct` each had a live `claude` session (checked with `pgrep -x claude` and `lsof -a -p <pid> -d cwd`), and `Philippians`, `dalia_martinez_funeral` and `chat_verification` had uncommitted changes. Deliverable: one decision and one fix for register row F12: the tool refuses a tree whose only dirt is generated files its own plan moves. The rule is his call; the first step is the options in one picker. The gate citation of S294 (results `791e005997ab`) was re-run in a clean clone of `9bd6f83` and confirmed (18/18, manifest `e755389a69c7`). Phase 3F records the rest. Model: Claude Sonnet 5.5.

### 2026-10-11 · [ad hoc] S295 — fold the second 2026-10-10 HANDOFFS shard pointer into the archive index

The pointer block the trim (`4b631e7`, 1 receipt, S292, 2026-10-10, to `HANDOFFS-through-2026-10-10-2.md`, the name the dry run chose because `HANDOFFS-through-2026-10-10.md` was taken) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, trimmer v1.8.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S294, S293). The shard proof was run by name from a `--no-local` clone of the trim commit: `HANDOFFS-through-2026-10-10-2.md.verify.sh` at `4b631e7`, exit 0 (L1, L2/front-matter, L3). Before the trim, on his go-ahead at Phase 0, `9bd6f83` was pushed to the fork `origin` by name (5 commits) and read back with `ls-remote` (`0 0`); nothing was pushed after it, and nothing went upstream. Model: Claude Sonnet 5.5.

### 2026-10-11 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-10-2.md` (1 record(s), 41,216 B → 29,394 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-10 → 2026-10-10) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-10-2.md`](docs/archive/HANDOFFS-through-2026-10-10-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-10-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-10-2.md.verify.sh)
rather than trusting a digest printed here. Live file 41,216 B → 29,394 B (−28.7%).

### 2026-10-10 · [BL-101] S294 close-out — F16 closed with no tool change; the receipt is complete

Receipt S294 is `status: complete` (self 8, predecessor 9; no fork learning row appended, so no retirement is owed: the rows considered are named in the receipt, fork #57, #80, #39 and #71). **The deliverable:** F16, the `CLAUDE.md` text rewrite of `bin/migrate-layout`, settled by a measurement over the 11 adopters with a `CLAUDE.md` (17 of 152 changed lines inside a Learnings region, none made false, one a runnable command) and his choice to keep the rule; the record, the script, its output and the register line are in `25ed0ea` (the entry below). **What this commit adds:** the receipt, this entry and the BL-101 Next action in `docs/planning/BACKLOG-DETAIL.md` (F16 declined, the S294 live-session note). **One breach of my own, stated:** at the first picker I recommended listing the Learnings lines instead of rewriting them, which I had not run; the measurement showed the opposite (fork #57's lesson), cost a second picker and is in the record and the receipt. **Gate run:** quality_ratchet: 18/18 pass · 0 fail · 0 unmeasured · results 791e005997ab · manifest e755389a69c7 (the gate run in a clean `--no-local` clone of `25ed0ea`, about 16 minutes at a load of about 6 to 8, so no gate reached BL-103's 600 s limit; the close-out commit adds only this receipt, its ledger entry and the BL-101 Next action in `BACKLOG-DETAIL.md`; tests-sh-passed read 483 at three receipts, floor 477; migrate-layout-unit-tests 186, floor 186) **Pushes:** `6ca1037` went to the fork `origin` at the start of the session on his go-ahead (recorded in the fold entry below); the 5 commits after it (the trim, its fold, the claim, the F16 record and this close-out) are local. Model: Claude Sonnet 5.5.

### 2026-10-10 · [BL-101] S294 — F16 measured and closed: the `CLAUDE.md` rewrite in `bin/migrate-layout` stays (declined, by his choice and by the measurement)

Register row F16 (`docs/planning/methodology-subdirectory-evidence/findings-register.md`): the tool rewrites a project's `CLAUDE.md` as text and cannot tell a live pointer from a past-tense account in the project's own Learnings. **Measured, read-only** (`f16-measure-claude-md.py`, output `f16-measure-output.txt`; committed `CLAUDE.md` text read with `git show`, the tool's own `token_rewriter` over the manifest's whole table, tier all): the P14 count reproduced (16 changed lines at `church_growth`, 9 inside Learnings); across the 11 adopters that have a `CLAUDE.md`, **152 lines change and 17 (11%) sit inside a Learnings region, in 6 adopters, 9 of them `church_growth`'s**. Every one of the 17 was read: in each the changed path names a file that exists at its new place, **none is made false**, and one (`Philippians` P8) is the command `python3 quality_ratchet.py --run`, which skipping the section would have left failing. **At the decision picker I had suggested listing those lines instead of rewriting them (my first recommendation); the measurement says the opposite, and I said so.** Three options were put to him; he chose to keep the rewrite and close F16. **The tool did not change; no test, gate floor or adopter was touched; nothing went upstream.** Written: the record `f16-learnings-lines-record.md` (the method, the 17 lines, the limits, what would reopen F16), the script, its output, and a dated line under the row in the register. Limits stated in the record: n is 17, the section test is a heading containing "earning", "none is false" is a reading and not a test. **Phase 0 gate citation, confirmed:** S293's receipt cites 18/18, results `791e005997ab`, manifest `e755389a69c7`; the local `.quality-gates-results.json` held S292's run (results `20d9937f9bf7`), so the check was a re-run of `quality_ratchet.py --run` in a clean `--no-local` clone of `6ca1037` (started at Phase 0, exit 0): 18/18 pass, 0 fail, 0 unmeasured, the same two hashes. Model: Claude Sonnet 5.5.

### 2026-10-10 · [BL-101] S294 claim (in progress) — F16, the `CLAUDE.md` rewrite in `bin/migrate-layout`

CHANGELOG: pending. Operator said `go`; at the Phase 0 picker he chose F16 as the deliverable and gave two go-aheads (the owed HANDOFFS trim and a push of the 6 local commits to the fork; both done, entries below). P15 was not possible: `nprcgenekeepr`, `mts-system`, `vscode_quarto_ext` and `wsfct` each had a live `claude` session at Phase 0 (checked with `pgrep -x claude` and `lsof -a -p <pid> -d cwd`), and `Philippians`, `dalia_martinez_funeral` and `chat_verification` had uncommitted changes. Deliverable: one decision and one fix for register row F16 (`docs/planning/methodology-subdirectory-evidence/findings-register.md`): `bin/migrate-layout` rewrites a project's `CLAUDE.md` as text and cannot tell a live pointer from a past-tense account in the project's own Learnings. The rule is his call; the first step is the options in one picker. Phase 3F records the rest. Model: Claude Sonnet 5.5.

### 2026-10-10 · [ad hoc] S294 — fold the 2026-10-10 HANDOFFS shard pointer into the archive index

The pointer block the trim (`0da40b0`, 1 receipt, S291, 2026-10-10, to `HANDOFFS-through-2026-10-10.md`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, trimmer v1.8.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S293, S292). The shard proof was run by name from a `--no-local` clone of the trim commit: `HANDOFFS-through-2026-10-10.md.verify.sh` at `0da40b0`, exit 0 (L1, L2/front-matter, L3). Before the trim, on his go-ahead at Phase 0, `6ca1037` was pushed to the fork `origin` by name and read back with `ls-remote` (`0 0`); nothing was pushed after it, and nothing went upstream. Model: Claude Sonnet 5.5.

### 2026-10-10 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-10.md` (1 record(s), 40,881 B → 29,455 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-10 → 2026-10-10) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-10.md`](docs/archive/HANDOFFS-through-2026-10-10.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-10.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-10.md.verify.sh)
rather than trusting a digest printed here. Live file 40,881 B → 29,455 B (−27.9%).

### 2026-10-10 · [BL-101] S293 — close-out: the F15 fix done, P15 not started (no adopter was free); the receipt is complete; the gate run read 18/18

Receipt S293 is `status: complete` (self 8, predecessor 9; no fork learning row appended, so no retirement is owed: the rows considered are named in the receipt, fork #28, #16, #64 and #82). **Gate run:** `quality_ratchet.py --run` in a clean `--no-local` clone of `548ae9a`, 18/18 pass, 0 fail, 0 unmeasured, results `791e005997ab`, manifest `e755389a69c7`, 893 s (no gate near BL-103's 600 s limit); `migrate-layout-unit-tests` read 186 against its new floor 186. **Real-data smoke (Phase 3E):** a `--no-local` clone of `~/Development/church_growth` at `4cdf70a`, dry run `--tier all`: the tool from before the fix printed the `WARNING: 1 hook line(s) run a moved tool ...` line, the fixed tool printed none, both exited 0 with 15 hook mentions in 1 file, and the adopter's tree was unchanged. **One correction of my own:** the register's F15 line, committed in `548ae9a`, said a run over an adopter carrying the layout-aware hook was "Not shown"; the smoke above was run after it was written and shows it for a dry run, so the register line is corrected in this commit; the one thing still not shown is an apply. The close-out commit adds this entry, the receipt and that register edit; nothing was pushed after the fork's `8580d81`, so 6 commits are local after it. Model: Claude Sonnet 5.5.

### 2026-10-10 · [BL-101] S293 — the record of the F15 fix: the register's dated line, and the Next action says P15 was blocked

`docs/planning/methodology-subdirectory-evidence/findings-register.md` gains a dated line, "F15: fixed in `35d6a03`", and its "Read at the next adopter session" tail now reads F10, F11 and F15 as fixed; `docs/planning/BACKLOG-DETAIL.md`'s BL-101 Next action says the same and records why P15 was not started: at S293's Phase 0 `nprcgenekeepr`, `mts-system`, `vscode_quarto_ext` and `wsfct` each had a live `claude` session (`nprcgenekeepr`'s S957 claim commit was minutes old at 16:38) and `Philippians`, `dalia_martinez_funeral`, `chat_verification` and `claude_work` were dirty or without a commit. `docs/planning/BACKLOG.md`'s BL-101 row is unchanged (34 B of headroom, and its "Next: P15" is still true); the P14 record and plan section 7.4d, which state F15 as raised at S292, are not rewritten. Model: Claude Sonnet 5.5.

### 2026-10-10 · [BL-101] S293 — the F15 fix: `bin/migrate-layout`'s `hooks` row no longer counts a line marked `# layout: ok -- <reason>` as a run of a moved tool

`bin/migrate-layout` gains `MARKER_RE` (the grammar `bin/check-layout-literals` reads: `# layout: ok`, and ` -- <reason>` or it acknowledges nothing), and `scan_hits` no longer sets a hook site's `runs_tool` when the line carries a marker with a reason, so `runs_moved_tool` stays 0 for the layout-aware ledger hook (`.githooks/pre-commit:303`, `rtool=quality_ratchet.py    # layout: ok -- ...`), which tries three places for the tool and which the apply never refused (it exited 0 in both `church_growth` arms that carried the hook and on the real tree). The site is still listed. A marker with no reason still warns (`python3 context_budget.py --status    # layout: ok`). Four tests in `TestWhatTheHitsSayAboutHooksAndDirectories` (`tools/test_migrate_layout.py`): a marked line is not flagged, a bare marker is, this repository's own `.githooks/pre-commit` copied into a project raises no warning (the F15 reproduction), and the two tools' `MARKER_RE` patterns are equal. **Red first:** 3 of the class's 10 tests failed before the fix (the grammar test with `AttributeError`, the marked line `runs_tool` True, the real hook `runs_moved_tool` 1 where 0 was expected); the bare-marker test passed before and after, and a mutant that honours a bare marker fails exactly that one. **Green:** the class 10 of 10; the whole `tools/test_migrate_layout.py` 186 of 186 in 340 s in a clean `--no-local` clone carrying the two files (182 before); `bin/check-layout-literals` 0 sites. The `migrate-layout-unit-tests` floor in `.quality-gates.json` tightens 182 → 186 (tightening needs no approval). The tool is canonical-only (not in `bin/_manifest.py`): no adopter receives it and nothing is released. Not done in this commit: the register row and the Next action (the next commit), the full `bin/tests.sh` and the gate run (close-out). Model: Claude Sonnet 5.5.

### 2026-10-10 · [BL-101] S293 claim (in progress) — the F15 fix in `bin/migrate-layout`

CHANGELOG: pending. Operator said `go`; at the Phase 0 picker he chose P15 on `nprcgenekeepr` at tier all and gave two go-aheads (the owed HANDOFFS trim and a push of 10 commits to the fork, entries below). P15 was then not possible: at the check before any claim, `nprcgenekeepr` had a live `claude` session (pid 64241, started 16:34 that day, its repository's newest commit "S957 claim" at 16:38), `mts-system`, `vscode_quarto_ext` and `wsfct` each had one, and `Philippians`, `dalia_martinez_funeral`, `chat_verification` and `claude_work` were dirty or without a commit. At a second picker he chose the F15 fix in this repository. Deliverable: one fix to `bin/migrate-layout`'s `hooks` row (`findings-register.md` row F15: a false warning on the layout-aware hook, `.githooks/pre-commit:303`) with its test, Development workstream. P15, F6, F8, F12 to F14 and F16, anything upstream and D8 are not part of it. Model: Claude Sonnet 5.5.

### 2026-10-10 · [ad hoc] S293 — push of this repository's 10 commits to the fork `origin` (`rmsharp/methodology`)

Non-commit action, on his explicit go-ahead at the S293 Phase 0 picker ("Push 10 commits to fork origin"). `git push origin 8580d81:refs/heads/main` moved the fork's `main` from `fc01ccb` to `8580d81` (S292's close-out commit; the 10 commits are S292's, from `9ccf08c` through `8580d81`). The ref named the commit, not `HEAD`, because the trim `45a7e12` and its fold `bae66fe` had been committed first and were not part of the go-ahead; they are local. Read back after the push: `git ls-remote origin refs/heads/main` and `git rev-parse 8580d81` both read `8580d811ac3586e4e3c4e27af1089cf71dd6dc2f`, and `git rev-list --left-right --count origin/main...8580d81` read `0 0` after a fetch. Upstream `KJ5HST/methodology` was not touched: no pull request, issue, comment or tag. Model: Claude Sonnet 5.5.

### 2026-10-10 · [ad hoc] S293 — fold the third 2026-10-09 HANDOFFS shard pointer into the archive index

The pointer block the trim (`45a7e12`, 1 receipt, S290, 2026-10-09, to `HANDOFFS-through-2026-10-09-3.md`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, trimmer v1.8.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S292, S291). The shard proof was run by name from a `--no-local` clone of the trim commit: `HANDOFFS-through-2026-10-09-3.md.verify.sh` at `45a7e12`, exit 0 (L1, L2/front-matter, L3). Model: Claude Sonnet 5.5.

### 2026-10-10 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-09-3.md` (1 record(s), 41,173 B → 29,475 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-09 → 2026-10-09) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-09-3.md`](docs/archive/HANDOFFS-through-2026-10-09-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-09-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-09-3.md.verify.sh)
rather than trusting a digest printed here. Live file 41,173 B → 29,475 B (−28.4%).

### 2026-10-10 · [BL-101] S292 — close-out: P14 done at tier all on `church_growth`; the receipt is complete; the gate run read 18/18

Receipt S292 is `status: complete` (self 8, predecessor 9; no fork learning row appended, so no retirement is owed: the rows considered are named in the receipt, fork #82, #53, #58 and distributed Learning #12). `CHANGELOG: pending` on the S292 claim entry is cleared by this statement (a committed entry is not edited). Deliverable: P14 (plan §7.4d, register rows F15 and F16, record `p14-church-growth-record.md`); the sync `2f1389c`, the hook replacement `4cdf70a` and the move `62f7d8a` are in `~/Development/church_growth`, local (it has no remote). **The gate run on `4afc0d6` read `18/18 pass · 0 fail · 0 unmeasured`** (results `20d9937f9bf7`, manifest `c7eae109fc87`, the S291 hashes: no threshold moved; `tests-sh-passed` 483 at four receipts), 17.5 minutes (1,048 s) at a load of about 4 to 7, so BL-103's 600 s limit was not hit. **Three loose statements in this session's entries, corrected here:** the entry of `d981009` says 'Three dated lines' were added under the register's rows (two); the entry of `e3e267e` describes `rehearsal-hook-probes.txt` as showing the exit codes (the file holds the hook's own words, empty where a commit passed; the codes are the `probe ... exit=` lines of `rehearsal-log.txt`, and a header added in `78eaa2e` says so); the entry of `78eaa2e` says the file was 'committed two entries below' (it first landed in `e3e267e`). **For him, at the next Phase 0:** the adopter and tier for P15 (or the F6, F8, F12 to F16 triage); whether `church_growth` ignores `__pycache__/` and migrates its two stale seeds; D8, the release number and any tag. The HANDOFFS trim is owed after that report (3 receipts). Pushes done this session, each on his go-ahead: this repository's 20 commits to the fork and `airqino`'s 2 commits (entries above); this session's 10 commits are local, and nothing was sent upstream. Plan 59,957 of 60,000 B, BACKLOG.md 56,716 of 56,750 B. Model: Claude Sonnet 5.5.

### 2026-10-10 · [BL-101] S292 — the BL-101 row and Next action: P14 done, P15 next

`docs/planning/BACKLOG.md` BL-101 row and `docs/planning/BACKLOG-DETAIL.md` BL-101: the row gains P14 done (the hook replaced first, 0 links, F15 and F16) and now reads **Next: P15**, with `airqino` marked pushed (S292) and `church_growth` marked remote-less; the detail gains a P14 paragraph after P13's and a rewritten **Next action** (the adopter and tier for P15; F2 first for an adopter with a ledger hook, `chat_verification`'s next; F6, F8 and F12 to F16 await his triage; which adopters had a session running at S292's Phase 0). `BACKLOG.md` is 56,716 of 56,750 B (34 B headroom): the next edit of the row recomposes. Model: Claude Sonnet 5.5.

### 2026-10-10 · [BL-101] S292 — P14 done at tier all: church_growth synced, its hook replaced and moved in its own repository; the record, plan 7.4d, register rows F15 and F16

P14 on `church_growth` is done at tier all, in its own repository and local (the project has no remote): the sync `2f1389c` (16 files updated, 8 created, no `--force`), its older ledger hook replaced with this repository's layout-aware one `4cdf70a`, and the move `62f7d8a` (`--tier all`: 30 renames, 27 at 100%, `CLAUDE.md` 21 replacements on 16 lines, 2 ignored generated files moved plainly), each through the project's hook with its own ledger entry. His Phase 0 pick, out of plan order because a session was running in `nprcgenekeepr` and in `mts-system`. **The case this adopter added:** after the move a later commit with no ledger entry exits 0 under the old hook and 1 under the replaced one (the unmoved control: 1), so the hook is part of the move (register row F2, plan C5). **Identical before and after:** `bin/status` 23 of 23 `current`, the dashboard 49 and risk high with the same doc-only line, `check-ledger` and `check-handoff` exit 1 (stale-format seeds: 29 and 7 findings, the same), the three non-tracked files by sha256, `.git/info/exclude` restored by `cmp`. **Cost of tier 2:** 0 links. **Findings, register rows F15 and F16:** the tool's `hooks` warning fires on the layout-aware hook itself though the apply exits 0 (`.githooks/pre-commit:303`); the `CLAUDE.md` rewrite changes 9 lines of the project's own past-tense learnings. Three dated lines under F2, F12, F13, F7, F8 and F9. Record: `p14-church-growth-record.md`. Plan §7.4d added and the plan recomposed to stay under its own budget (59,957 of 60,000 B: §0 item 9 shortened, two closed sentences dropped, §7.4a to §7.4c shortened, `airqino` marked pushed, the status line now P0 to P14 done, the DONE list gains the hook step). Nothing was sent upstream. Model: Claude Sonnet 5.5.

### 2026-10-10 · [BL-101] S292 — the P14 final check: Phase 0 in the new layout, the later-commit probes and the checkers before and after

The P14 final check (`p14-final-clone.sh`, 11 seconds, fresh `--no-local` clones of the real adopter's `62f7d8a` and of `4cdf70a`, the commit before the move), in `p14-adopter-runs/`: `final-clone-log.txt` (Phase 0 in the new layout: the runner and safeguards byte-identical to canonical, `## ACTIVE TASK` at `methodology/SESSION_NOTES.md:9`, 0 status lines, both frontiers `62f7d8a`; dashboard 49 and risk high in both clones with the same doc-only line; gates `0/0`; `bin/status` `layout: new`, 23 current; `check-links` exit 0; the committed hook's `--selftest` OK, 43 checks; and three later commits through it: no entry exit 1, an entry at `methodology/CHANGELOG.md` exit 0, an edited committed entry exit 1), `check-ledger-handoff-before-after.txt` (the stale-format seeds: 29 ledger findings and 2 + 5 handoff findings, the same before and after) and `hook-warning-sites.json` (the tool's own JSON for the `hooks` row: 15 sites, one `runs_tool`, `.githooks/pre-commit:303`). A header line was added to `rehearsal-hook-probes.txt`, committed two entries below, which says that the exit codes sit in `rehearsal-log.txt` and an empty section is a commit that passed. Model: Claude Sonnet 5.5.

### 2026-10-10 · [BL-101] S292 — the P14 real-run reports: the sync, the dry run, the apply and the non-tracked files' hashes

The raw outputs of the P14 real run in `~/Development/church_growth` (`p14-adopter-runs/`): `real-sync-output.txt` (`bin/sync` without `--force`: 16 updated, 8 created, 2 unchanged, no refusal; the adopter's commit `2f1389c`), `real-dry-run-report.txt` (the dry run on the real tree after the sync and the hook replacement `4cdf70a`: exit 0, 32 moves, identical to the rehearsal's tier-all dry run except the ledger mention count, 306 against 290, from the two real entries), `real-apply-report.txt` (the apply, the adopter's commit `62f7d8a`: 23/23 `current`, ledger and handoff exit 1 before and after, 0 project links dangling, history 36 to 37, clean tree) and `real-untracked-hashes.txt` (sha256 of the stray pyc and the two ignored generated files before and after: identical; the `.git/info/exclude` the sync and the apply needed was restored and `cmp` read it identical). Model: Claude Sonnet 5.5.

### 2026-10-10 · [BL-101] S292 — the P14 rehearsal reports: tier 1, tier all, the sync dry run and the hook probes

The raw outputs of the P14 rehearsal (`p14-adopter-runs/`): `rehearsal-tier-1-report.txt` (the apply report at tier 1: `links` 0 to 4 project dangling, register row F13 again), `rehearsal-tier-all-report.txt` (the apply at tier all in the arm that carries the real tree's non-tracked files: 32 moves, `CLAUDE.md` 21 replacements, checks 23/23, ledger and handoff exit 1 before and after, 0 links, history 36 to 37, clean tree, and the `hooks` WARNING that is register row F15), `rehearsal-sync-dry-run.txt` and `rehearsal-hook-probes.txt` (the later-commit probes in each arm: control 1 then 0, old hook after the move 0 then 0, layout-aware hook 1 then 0; and the `--selftest` line). Model: Claude Sonnet 5.5.

### 2026-10-10 · [BL-101] S292 — the P14 rehearsal: its two scripts, its log and its dashboards

The rehearsal for P14 on `~/Development/church_growth`, run before any change to the adopter: `p14-rehearsal.sh` over 6 `--no-local` clones with the project's `core.hooksPath` set in each (a clone does not inherit it; fork Learning #53), 69 seconds, one log. Arms: `base` (unsynced), `ctrl` (synced), `t1` (tier 1), `tall` (tier all, the adopter's old hook kept), `tallh` (tier all, this repository's layout-aware hook replacing it in its own commit) and `tallx` (as `tallh`, with the real tree's non-tracked files copied in and `/__pycache__/` excluded locally). Results: `bin/sync` without `--force` exit 0 in all five synced arms; every `bin/migrate-layout --apply` exit 0 with a clean tree; **a later commit with no ledger entry is refused (exit 1) in the unmoved control, passes (exit 0) after the move under the old hook, and is refused (exit 1) under the layout-aware hook**; the hook's `--selftest` reads OK, 43 checks. Dashboards: `base` 34/100 (the adopter's own copy, 39 versions behind), every other arm 49/100, risk high. The second script, `p14-final-clone.sh`, ran after the real move. Evidence: `docs/planning/methodology-subdirectory-evidence/p14-rehearsal.sh`, `p14-final-clone.sh`, `p14-adopter-runs/rehearsal-log.txt`, `p14-adopter-runs/rehearsal-dashboards.txt`. Model: Claude Sonnet 5.5.

### 2026-10-10 · [BL-101] S292 claim (in progress) — P14 on `church_growth` at tier all

CHANGELOG: pending. Operator said `go`; at the Phase 0 picker he chose P14 on `church_growth` (out of plan order: `nprcgenekeepr` and `mts-system` each had a Claude session running at Phase 0, `church_growth` none), and gave three go-aheads: the owed HANDOFFS trim (`2761657`, S289's receipt to `HANDOFFS-through-2026-10-09-2.md`, shard proof exit 0 from a `--no-local` clone) and its fold (`b71bda1`), a push of this repository's 20 local commits to the fork `origin`, and a push of `airqino`'s 2 commits (entries below). Deliverable: one adopter session in `~/Development/church_growth` (plan section 7.4, Development workstream), recorded in a `p14-church-growth-record.md` beside the P13 record and in the findings register. Its push, anything upstream, F6, F8, F12 to F14 and D8 are not part of it. Model: Claude Sonnet 5.5.

### 2026-10-10 · [ad hoc] S292 — fold the second 2026-10-09 HANDOFFS shard pointer into the archive index

The pointer block the trim (`2761657`, 1 receipt, S289, 2026-10-09, to `HANDOFFS-through-2026-10-09-2.md`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, trimmer v1.8.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S291, S290). The shard proof was run by name from a `--no-local` clone of the trim commit: `HANDOFFS-through-2026-10-09-2.md.verify.sh` at `2761657`, exit 0 (L1, L2/front-matter, L3). Model: Claude Sonnet 5.5.

### 2026-10-10 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-09-2.md` (1 record(s), 40,385 B → 29,351 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-09 → 2026-10-09) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-09-2.md`](docs/archive/HANDOFFS-through-2026-10-09-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-09-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-09-2.md.verify.sh)
rather than trusting a digest printed here. Live file 40,385 B → 29,351 B (−27.3%).

### 2026-10-10 · [BL-101] S292 — push of `~/Development/airqino` (P13's sync `da595cb` and move `f7a0194`) to `rmsharp/airqinodashboard`

Non-commit action, on his explicit go-ahead at the S292 Phase 0 picker ("Push airqino's 2 commits"). `git push origin main` in `~/Development/airqino` moved its `origin/main` from `998cd51` to `f7a0194` (2 commits: the sync, then the tier-all move). Read back after the push: `git ls-remote origin refs/heads/main` returned `f7a01943d6ab82fb36e2f76e3ae20080985f390d`, equal to its local HEAD, and `git rev-list --left-right --count HEAD...origin/main` read `0 0`. The project has no CI, so nothing ran on the push. Not sent anywhere else. Model: Claude Sonnet 5.5.

### 2026-10-10 · [ad hoc] S292 — push of this repository's 20 local commits to the fork `origin` (`rmsharp/methodology`)

Non-commit action, on his explicit go-ahead at the S292 Phase 0 picker ("Push 20 commits to fork origin"). `git push origin main` moved the fork's `main` from `f0770dc` to `fc01ccb` (S291's close-out commit; the 20 commits are S290's and S291's, from the HANDOFFS trim `b0cad40` through `fc01ccb`). Read back after the push: `git ls-remote origin refs/heads/main` and `git rev-parse HEAD` both read `fc01ccb94ecb063da87439b512e6f724c6500591`, and `git rev-list --left-right --count HEAD...origin/main` read `0 0` after a fetch. Upstream `KJ5HST/methodology` was not touched: no pull request, issue, comment or tag. The three commits this session adds after `fc01ccb` (trim, fold, claim) were not part of that go-ahead and are local. Model: Claude Sonnet 5.5.

### 2026-10-10 · [BL-101] S291 — close-out: P13 done at tier all on `airqino`; the receipt is complete; the gate run read 18/18

Receipt S291 is `status: complete` (self 8, predecessor 9; no fork learning row appended, so no retirement is owed: the rows considered are named in the receipt). `CHANGELOG: pending` on the S291 claim entry is cleared by this statement (a committed entry is not edited). Deliverable: P13 (plan §7.4c, register rows F12 to F14, record `p13-airqino-record.md`); the sync `da595cb` and the move `f7a0194` are in `~/Development/airqino`, local, 2 ahead of its `origin/main`. **The gate run on `5dd513a` read `18/18 pass · 0 fail · 0 unmeasured`** (results `20d9937f9bf7`, manifest `c7eae109fc87`, the S290 hashes: no threshold moved; `tests-sh-passed` 483 at three receipts), 16.8 minutes at a load of about 2 to 3, so BL-103's 600 s limit was not hit. **Two loose counts in this session's entries, corrected here:** `c3e6d48` says 'all 8 states' (10; corrected once already in `b97313a`) and `952497f` says 'four names, then seven' (seven at once). **For him, at the next Phase 0:** the adopter and tier for P14 (or the F6, F8, F12, F13, F14 triage); whether `airqino` is pushed, its nested copy deleted and its generated files ignored; D8, the release number and any tag. The HANDOFFS trim is owed after that report (3 receipts). Nothing was pushed or sent upstream; this repository's `origin/main` is 20 commits behind after this one (his go-ahead). Plan 59,879 of 60,000 B, BACKLOG.md 56,358 of 56,750 B. Model: Claude Sonnet 5.5.

### 2026-10-10 · [BL-101] S291 — the BL-101 row and Next action: P13 done, P14 next; the real tree's pytest after the sync

`docs/planning/BACKLOG.md` (the BL-101 row's tail: P13 done at tier all, **Next: P14**; 56,358 B against the 56,750 B budget, 392 B of headroom) and `docs/planning/BACKLOG-DETAIL.md` (a P13 DONE paragraph, and the Next action rewritten for P14: F5, F10 and F11 fixed; F6, F8, F12, F13 and F14 await his triage; `airqino` is not pushed, its nested copy and its untracked generated files are his calls). Added `docs/planning/methodology-subdirectory-evidence/p13-adopter-runs/real-pytest-after-sync.txt`, the project's suite in the real tree after the sync and before the move (144 passed, 2 xfailed). Model: Claude Sonnet 5.5.

### 2026-10-10 · [BL-101] S291 — P13 done at tier all: `airqino` synced and moved in its own repository; the record, plan 7.4c, register rows F12 to F14

Two commits in `~/Development/airqino` (origin `rmsharp/airqinodashboard`, fetched first, level at `998cd51`; **not pushed**, 2 ahead of `origin/main`): the sync from this checkout at `41296a1` (`da595cb`: `bin/sync` without `--force`, 21 files updated, `.gitattributes` created, with a hand-written ledger entry under a new `## 2026-10` heading) and the move (`f7a0194`: `bin/migrate-layout --tier all --apply`, 30 renames, `CLAUDE.md` and `.gitignore` edited, 4 untracked files moved plainly, exit 0). The tool refused the tree as dirty (four untracked files), so four names, then seven, went into the real repository's local `.git/info/exclude` for the apply and the file was restored byte-for-byte after; no file of the project's was edited, deleted or committed other than by the two commits. **Held:** `python3 -m pytest -q` 144 passed, 2 xfailed before and after; the two gates 2/2, results `2993256f954d`; `bin/status` 23/23 `current`; the dashboard 68 and risk 0; the four untracked files' sha256 identical. **Cost of tier 2:** 1 link dangling in the ledger header. Added: `docs/planning/methodology-subdirectory-evidence/p13-airqino-record.md`, `docs/planning/methodology-subdirectory-evidence/p13-adopter-runs/final-clone-log.txt`, plan §7.4c (and §7.1, §7.3a, §7.4a, §7.4b shortened to make room: 59,879 of 60,000 B), and register rows **F12** (the tool refuses a tree whose only dirt is generated files it would move, and exits 4 unless the new names are excluded too), **F13** (tier 1's links row counts four unmoved seeds as dangling) and **F14** (the adopter's nested older copy of this repository, 19 files, stays; the plan named it at §2.2), all open and untracked. F9 and the F7/F2 notes are dated lines under the register. His calls are in the record's section 8 and the BL-101 Next action. Model: Claude Sonnet 5.5.

### 2026-10-10 · [BL-101] S291 — the P13 real-run reports: the sync, the dry run, the apply and the untracked files' hashes

Added to `docs/planning/methodology-subdirectory-evidence/p13-adopter-runs/`: `real-sync-output.txt` (`bin/sync` on the real `airqino`: 21 files updated, `.gitattributes` created, no `--force`; in `airqino` it is `da595cb`), `real-dry-run-report.txt` (the migration's dry run after the sync: no refusal, 34 moves, 19 files left in place), `real-apply-report.txt` (the apply, `f7a0194`: status 23/23 to 23/23, ledger exit 0 to 0, history 76 to 77, `clean tree: yes`, exit 0) and `real-untracked-hashes.txt` (sha256 of the four untracked files before and after: identical). Two commits in `~/Development/airqino`, not pushed; its `.git/info/exclude` was added to for the apply and restored byte-for-byte after. Model: Claude Sonnet 5.5.

### 2026-10-10 · [BL-101] S291 — the P13 rehearsal reports: tier all, the two untracked-file arms and the adopter's check-handoff

Added to `docs/planning/methodology-subdirectory-evidence/p13-adopter-runs/`: `rehearsal-tier-all-report.txt` (the apply report of the tier-all arm: 30 moves, 19 files left in place, the four rewrites, the not-rewritten rows, the checks), `rehearsal-tallx-checks.txt` and `rehearsal-tallm-checks.txt` (the checks of the two arms with the real tree's untracked files: the first exits 4, `CHECKS DIFFER (tree not clean)`, the commit made, because the three generated files sit untracked at `methodology/`; the second, with their new names excluded too, exits 0 and reads `clean tree: yes`), and `check-handoff-before-after.txt` (the adopter's own 6 unusable `commit:` slots, the same before and after the move). **A correction of the entry above (`c3e6d48`):** it says the suite read 144 passed and 2 xfailed 'in all 8 states'; the count is 10 (the 6 rehearsal arms, the real tree after the sync and after the move, and the 2 final-check clones), each 144 and 2. A committed entry is not edited, so it is corrected here. Model: Claude Sonnet 5.5.

### 2026-10-10 · [BL-101] S291 — the P13 rehearsal: its two scripts, its log and its tier-1 report

`docs/planning/methodology-subdirectory-evidence/p13-rehearsal.sh` clones `airqino` (`998cd51`) six times with `git clone --no-local` and never writes to the real repository: base (unsynced), ctrl (synced), t1 (synced, `--tier 1`), tall (synced, `--tier all`), tallx and tallm (as tall, with the real tree's four untracked files copied in and excluded locally, tallm excluding the three generated files' new names as well). Each arm runs the adopter's own `python3 -m pytest -q` (144 passed, 2 xfailed in all 8 states) and its gates. `p13-final-clone.sh` is Phase 0 in the new layout from a fresh clone of the real result and a clone of the sync commit as control. Added: the two scripts, `p13-adopter-runs/rehearsal-log.txt` and `p13-adopter-runs/rehearsal-tier-1-report.txt`. The rest of the outputs follow in their own commits. Model: Claude Sonnet 5.5.

### 2026-10-10 · [BL-101] S291 claim (in progress) — P13 on `airqino` at tier all

CHANGELOG: pending. Operator said `go`; at the Phase 0 picker he chose P13 on `airqino` at tier all (recommended), BACKLOG.md recomposed in its own commit before the claim (`912d8c7`), and no push of the 10 local commits. The owed HANDOFFS trim (`0ba86c5`, S288's receipt to `HANDOFFS-through-2026-10-09.md`, shard proof exit 0 from a `--no-local` clone) and its fold (`9000d21`) ran before this claim. Deliverable: one adopter session in `~/Development/airqino` (plan section 7.4, Development workstream), recorded in `p13-airqino-record.md` and the findings register. Its push, anything upstream, F6, F8 and D8 are not part of it. Model: Claude Sonnet 5.5.

### 2026-10-10 · [BL-101] S291 — `docs/planning/BACKLOG.md` recomposed under the dashboard's one-read budget (57,294 B to 56,064 B)

S290's last edit of the BL-101 row (`2508bd9`) took `docs/planning/BACKLOG.md` from 56,505 B to 57,294 B, 544 B past the 56,750 B budget the dashboard measures, and the dashboard's risk read HIGH at this session's Phase 0 (it read medium at S290's). The row's tail (P11, P12, the survey, F5, F10 and F11: 3,123 B) is one segment of 1,893 B now; each fact it dropped is in `BACKLOG-DETAIL.md` (P11 DONE, P12 DONE, F5 DONE, F10 and F11 DONE) or in the records the segment names. Nothing else in the file changed. The headroom is 686 B, so the next edit of the row must recompose too. Chosen by him at the S291 Phase 0 picker (own commit before the claim). Model: Claude Sonnet 5.5.

### 2026-10-10 · [ad hoc] S291 — fold the 2026-10-09 HANDOFFS shard pointer into the archive index

The pointer block the trim (`0ba86c5`, 1 receipt, S288, 2026-10-09, to `HANDOFFS-through-2026-10-09.md`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, trimmer v1.8.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S290, S289). The shard proof was run by name from a `--no-local` clone of the trim commit: `HANDOFFS-through-2026-10-09.md.verify.sh` at `0ba86c5`, exit 0 (L1, L2/front-matter, L3). Model: Claude Sonnet 5.5.

### 2026-10-10 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-09.md` (1 record(s), 38,712 B → 28,959 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-09 → 2026-10-09) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-09.md`](docs/archive/HANDOFFS-through-2026-10-09.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-09.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-09.md.verify.sh)
rather than trusting a digest printed here. Live file 38,712 B → 28,959 B (−25.2%).

### 2026-10-10 · [BL-101] S290 close-out — F10 and F11 done: the tool reads a root `.Rbuildignore` for what its patterns cover, and files a packager's ignore list as config; the receipt is complete

CHANGELOG: recorded. The session's actions, each with its own entry above: the owed HANDOFFS trim `b0cad40` and its fold `c2c52a5`, the claim `aae6c22`, the change `ec8a38d` and its test `b06f8d1`, the evidence `dee8aac`, `a4866c6` and `65862cb`, and the record, register and backlog `2508bd9`. No upstream action, no push (10 commits ahead of the fork `origin` after this one), nothing in an adopter. The gate run on `2508bd9`: 18/18 pass · 0 fail · 0 unmeasured · results 20d9937f9bf7 · manifest c7eae109fc87. Phase 3C appended no fork learning row (D3 not triggered): the rows considered were fork #81, #107 and distributed Learning #12. The receipt scores S289's handoff 9 and this session 7: four figures stated at the design gate were wrong and are corrected forward in the record, the ledger and the BL-101 paragraph. Next: P13 (his S290 pick `airqino` at tier all, to confirm), after the HANDOFFS trim that is owed. Model: Claude Sonnet 5.5.

### 2026-10-09 · [BL-101] S290 — F10 and F11 recorded: the record, register rows F10 fixed and F11 added and fixed, the BL-101 row and Next action

`f10-pattern-rule-record.md` (what the rules would add, measured before building, with the three wrong figures corrected; what R 4.6.1 and vsce 3.6.0 do; the change; what was measured after; what the list cannot show; how to reproduce), `findings-register.md` (F11 added, dated lines for F10 and F11 under "Changes of disposition", the pointer to the next adopter session), the BL-101 row in `BACKLOG.md` and the S290 paragraph and Next action in `BACKLOG-DETAIL.md` (the P13 default is his S290 pick, `airqino` at tier all, given in an answer the picker said to ignore unless he chose P13, so the next session confirms it). BL-101 stays open: P13 onward. Nothing in an adopter, nothing upstream, no push. Model: Claude Sonnet 5.5.

### 2026-10-09 · [BL-101] S290 — F10's probes of R 4.6.1 and vsce 3.6.0 as a script, and two corrections of my own wording in committed text

`f10-probes.sh` (output `f10-probes-output.txt`) rebuilds the toy R package and the toy extension the record's section 3 rests on, and prints what each program packaged: R left `FOO.txt` out under `^foo\.txt$` (case-insensitive), left `docsdir/inner.txt` out under `^docsdir$`, left `ALPHA.md` out under the single line `# |ALPHA`, packaged `methodology/SESSION_RUNNER.md` once `SESSION_RUNNER.md` moved there under `^SESSION_RUNNER.*\.md$`, and packaged 0 `methodology/` entries once `^methodology$` was added; vsce 3.6.0 listed `methodology/SESSION_RUNNER.md` for packaging under a bare `SESSION_RUNNER.md` line and did not once `methodology/**` was added. **Corrected in committed text:** the F11 test's docstring said `.vscodeignore` named 26 moved files; it carries 26 mentions of moved names, 21 on code lines (`tools/test_migrate_layout.py`, docstring only, no test changed); and `f10-mutants.py` now says its G05 is round 2's, so round 1's output reads SURVIVED where a re-run reads KILLED. Model: Claude Sonnet 5.5.

### 2026-10-09 · [BL-101] S290 — F10's second mutation round: 2 of 2 killed, 39 of 40 in all, and the evidence of both rounds

`f10-mutants.py` (40 mutants, one per behaviour F10 and F11 added), `f10-mutation-round-1.txt` and `f10-mutation-round-2.txt`, run by `mutate-p7.py` in `--no-local` clones, baseline green first each time. Round 1 (clone of `ec8a38d`, 181 tests): 37 killed, 3 survived: G05 (my mutant was equivalent: `low` is the basename), P03 (skipping whitespace-only lines: equivalent over this tool's domain, since no moved path contains a space), P13 (a real gap, pinned in `b06f8d1`). Round 2 (clone of `b06f8d1`, 182 tests; G05 replaced by a mutant that passes the whole path to `is_pattern_list`, and P13): **2 of 2 killed**. In all 39 of 40 killed, and the one survivor, P03, is stated as equivalent in the record, not pinned. Model: Claude Sonnet 5.5.

### 2026-10-09 · [BL-101] S290 — F10 and F11 evidence: the rules measured before building, and the old tool against the new on 10 adopters

`f10-rules.py` (output `f10-rules-output.txt`) measured four rules over the 10 adopter clones `f5-population.py` leaves (the S286 pins, synced in the clone, tier all), with the tool as it was before F10 (`aae6c22`); `f10-identity.py` (output `f10-identity-output.txt`, identical on a second run) compares that tool with the new one. The stem rule: 78 files and 256 lines, 68 files new to F5's list, **none real** (the one real file among the 78, `nprcgenekeepr`'s `.Rbuildignore`, was already listed, for its comment lines). The module rule: 4 lines, all `.Rbuildignore` regexes. The pattern rule: 22 lines covering 143 entries of the map (139 moves and 4 generated names). The ignore-style file under `other`: `.vscodeignore`, one. Old against new: the 7 other kinds identical in rows and totals in 10 of 10, `config + other` identical in mentions and files, the two differences the two intended ones, and the S286 candidates listed 25 of 25 by the code-line test (24 before). **Corrected forward:** the ledger entry for `ec8a38d` says the stem rule's 68 new files held 1 real one (it held none), and its 24 of 25 is by the code-line test (the 25th was listed before, for 3 comment lines); and three figures in the design message to him were wrong: 21 lines (22), 34 non-comment lines (99, a figure I had not measured), and "all 21 CI entries are literal names" (20 are, the 21st is `docs/**`). Model: Claude Sonnet 5.5.

### 2026-10-09 · [BL-101] S290 — F10's first mutation round: 40 mutants, 37 killed, 3 survived, one test added

`f10-mutants.py` aims one mutant at each behaviour F10 and F11 added (the pattern-list name rule, the rule as a function, the wiring in `scan_hits`, the text), run by `mutate-p7.py` in a `--no-local` clone of `ec8a38d` (baseline green first). 37 killed by the named classes. The 3 survivors, each run once more against the whole test file as the runner does: **G05** (`low` is the basename, so a `/` test on it is equivalent: my mutant was wrong, replaced by one that passes the whole path to `is_pattern_list`); **P03** (skipping whitespace-only lines: equivalent over this tool's domain, since no moved path contains a space for such a line to match; not pinned, and said so in the record); **P13** (the files of one line unsorted: a real gap, since no test had a line covering two files in an order that differs from the map's). `test_the_files_of_a_line_come_in_name_order` pins P13; `tools/test_migrate_layout.py` 181 to 182 tests, floor 181 to 182 (a tightening), `Ran 182 tests` OK in 367 s. Round 2 follows. Model: Claude Sonnet 5.5.

### 2026-10-09 · [BL-101] S290 — F10 and F11: `bin/migrate-layout` reads a root `.Rbuildignore` for what its patterns cover, and files a packager's ignore list as config

`pattern_exposure` (new) reads the root `.Rbuildignore` as R reads it, measured on R 4.6.1 with a probe package: every non-empty line is a case-insensitive regular expression (a line that starts with `#` included: `# |ALPHA` left `ALPHA.md` out of the build), a line that matches a path or a directory above it covers it (`^docsdir$` left `docsdir/inner.txt` out), and a moved file is exposed when a line covers it where it is and none covers it where it goes (the probe packaged `methodology/SESSION_RUNNER.md`; one more line, `^methodology$`, stopped it). That file's row gains `patterns`: the lines, the files, and the lines not evaluated (a regex Python cannot compile, or a POSIX class, which Python reads as a different set). F11: a dot-file whose name ends in `ignore`, `.gitignore` apart, is `config` and no longer `other` (vsce 3.6.0, read and run: a bare name in `.vscodeignore` is the root's, so `methodology/SESSION_RUNNER.md` is packaged; a `.gitignore` stays prose because git matches a bare name at any depth). Measured over the 10 adopters at the S286 pins, tier all, in `--no-local` clones (`f10-identity.py`): the old tool (`aae6c22`) and the new agree on every other kind, in rows and in totals; the two differences are `nprcgenekeepr`'s `.Rbuildignore` (22 lines cover 143 moved files, 0 not evaluated) and `vscode_quarto_ext`'s `.vscodeignore` (other to config); the S286 candidates the tool lists: 25 of 25, 24 of 25 before. The register's stem rule was measured and not built: 78 files and 256 lines, 68 files new to the list, 1 of them real. `tools/test_migrate_layout.py` 150 to 181 tests, floor 150 to 181 (a tightening), `Ran 181 tests` OK in 393 s; `bin/check-layout-literals` 0 sites. Not verified: that an adopter read the row and acted on it; R's own engine on any line (Python's `re` is the approximation, and the text says so). Model: Claude Sonnet 5.5.

### 2026-10-09 · [BL-101] S290 claim (in progress) — the tool follow-up, F10: `bin/migrate-layout` sees a pattern that names a moved file by stem

CHANGELOG: pending. Operator said `go`; at the Phase 0 picker he chose F10 as the deliverable (the recommended option; the P13 adopter question was left unanswered by design) and left F6 and F8 open. The owed HANDOFFS trim (`b0cad40`, S287's receipt to `HANDOFFS-through-2026-10-08-6.md`, shard proof exit 0 from a `--no-local` clone) and its fold (`c2c52a5`) ran before this claim. Deliverable: register row F10 (plan section 7.6), Development workstream; the rule and its measured noise are presented to him before code. P13 is not started and nothing goes upstream. Model: Claude Sonnet 5.5.

### 2026-10-09 · [ad hoc] S290 — fold the sixth 2026-10-08 HANDOFFS shard pointer into the archive index

The pointer block the trim (`b0cad40`, 1 receipt, S287, 2026-10-08, to `HANDOFFS-through-2026-10-08-6.md`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, trimmer v1.8.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S289, S288). The shard proof was run by name from a `--no-local` clone of the trim commit: `HANDOFFS-through-2026-10-08-6.md.verify.sh` at `b0cad40`, exit 0 (L1, L2/front-matter, L3). Model: Claude Sonnet 5.5.

### 2026-10-09 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-08-6.md` (1 record(s), 38,628 B → 27,014 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-08 → 2026-10-08) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-08-6.md`](docs/archive/HANDOFFS-through-2026-10-08-6.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-08-6.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-08-6.md.verify.sh)
rather than trusting a digest printed here. Live file 38,628 B → 27,014 B (−30.1%).

### 2026-10-09 · [BL-101] S289 — push record: main pushed to the fork origin at his go-ahead (b518e63..db9afc3), and the F10 decision left to Phase 0

At the S289 close-out picker he chose to push; `git push origin main` sent S289's 9 commits (a plain fast-forward, `b518e63..db9afc3`) to `rmsharp/methodology` and `git rev-list --left-right --count origin/main...main` read `0 0` after a fetch. Nothing went to `KJ5HST/methodology`. **Also decided at that picker, by him:** whether F10 (a pattern that names a moved file by stem is not seen) is built before P13, or waived, is decided at the next session's Phase 0 picker; section 7.6's default (F10 first) stands until then. The receipt's line that a push waits for his go-ahead is therefore historical: the go-ahead came after it was written. This commit changes only `CHANGELOG.md` and is pushed too, under his standing grant for push records, so no further record is owed. Model: Claude Sonnet 5.5.

### 2026-10-09 · [BL-101] S289 close-out — F5 done: the tool lists the machine-read files a move relocates; the receipt is complete; the gate run read 18/18

Receipt S289 is `status: complete` (self 8, predecessor 9; no fork learning row appended, so no retirement is owed: the rows considered are named in the receipt). `CHANGELOG: pending` on the S289 claim entry is cleared by this statement (the never-edit gate forbids editing a committed entry). Deliverable: the tool follow-up, F5 (plan section 7.6, register row F5), in `fb71d55` and `4b80afe`; the owed HANDOFFS trim (`4da0243`) and its fold (`753cae7`) ran before the claim (`1da0b40`). **The gate run on `abb3e8b` read `18/18 pass · 0 fail · 0 unmeasured`** (results `ed289bd4e021`, manifest `b486cb7b19b5`, which moved because the `migrate-layout-unit-tests` floor rose 136 to 150; `tests-sh-passed` 483 at three receipts), at a load of about 11 in about 17 minutes, so BL-103's 600 s limit was not hit. **For him, at the next Phase 0:** whether F10 (a pattern that names a moved file by stem is not seen) is built before P13, as section 7.6 says by default, or waived; the adopter and tier if P13; F6 and F8 triage (left open); D8. Nothing was run in an adopter, pushed or sent upstream; this repository's `origin/main` is 9 commits behind after this one (his go-ahead). Model: Claude Sonnet 5.5.

### 2026-10-09 · [BL-101] S289 — F5 recorded: the record, register row F5 fixed and F10 opened, the BL-101 row and Next action

`f5-machine-read-list-record.md` (the problem reproduced first, the change, what was measured, what the list cannot show, how to reproduce). `findings-register.md`: a dated line under F5 (**fixed**, `fb71d55`, held by nine tests and one table test, `migrate-layout-unit-tests` 136 to 150) and a new open row **F10** (a pattern that names a moved file by stem is not seen: `nprcgenekeepr`'s `.Rbuildignore` has 16 such regex lines and the tool lists the file only for 3 comment mentions; not seen by the tool's own checks, untracked, his call). `BACKLOG.md` BL-101 row and `BACKLOG-DETAIL.md` (an S289 paragraph; the Next action no longer offers F5, which is done, and offers F10 instead). Not done and not started: P13, F10, F6, F8, anything in an adopter, anything upstream. Model: Claude Sonnet 5.5.

### 2026-10-09 · [BL-101] S289 — F5's second mutation round: the seven survivors, 7 of 7 killed; both rounds kept as evidence

`f5-mutants.py` (30 mutants, one per behaviour F5 added) and the output of both rounds, `f5-mutation-round-1.txt` (23 killed, 7 survived, about 49 minutes) and `f5-mutation-round-2.txt` (the seven against `4b80afe`, which adds the four tests and three table rows written for them: **7 killed, 0 survived**, baseline green at 150 tests). The runner is `mutate-p7.py`, unchanged, run in a scratch clone and never in this working tree. A round proves the tests would notice a wrong change to the new code, not that the code is right: the real-tree comparisons are in the entry above. Model: Claude Sonnet 5.5.

### 2026-10-09 · [BL-101] S289 — F5 evidence: the population comparison and the old-against-new identity check, with their output

`f5-population.py` (the tool's dry run on 10 adopters at the S286 pinned revisions, in `--no-local` clones, after a sync in the clone where the tool asked for one; compared with the survey's 25 strong-name candidates: **24 of 25 listed with the matching kind**, the 25th a `.gitattributes` hit that migration leaves in place, 5 extras in `airqino`'s nested `docs/methodology/` copy; output `f5-population-output.txt`, identical on a second run) and `f5-identity.py` (the tool before F5, `fb71d55~1`, against the tool now on the same clones: `ledger`, `harness`, `ci` and `hooks` identical and the old `other` equal to `tests + proofs + scripts + config + other` in mentions and files, **10 of 10**; output `f5-identity-output.txt`). Nothing was written in an adopter's real tree. Model: Claude Sonnet 5.5.

### 2026-10-09 · [BL-101] S289 — F5's first mutation round: 30 mutants, 23 killed, 7 survived; four tests and three table rows added for the seven

One mutant per behaviour F5 added (`f5-mutants.py`, run by `mutate-p7.py` in a scratch clone of `fb71d55`, baseline green first). **Survived:** F17 (`code += 1` for `code += len(names)`: no test had two moved names on one line), F18 (the final sort of `paths`: the hook git does not track is read last and sorts first, and no test looked at order), F20 (the `(N mentions, M on code lines)` text), F22 (the `[not tracked: per clone]` marker on a row: the old assertion `assertIn("not tracked", text)` was satisfied by the moves list's own `(not tracked: a plain move)`, so it proved nothing about the hook), F23 (comment-only rows printed after the code-line rows) and F27 and F28 (`tests?` and `specs?` in the directory rule: every fixture file was named `test_*`). **Added:** `test_two_names_on_one_line_are_two_mentions_on_code_lines`, `test_a_comment_only_file_is_printed_after_the_files_that_name_a_moved_path_on_a_code_line`, `test_a_file_with_several_mentions_says_how_many_are_on_code_lines`, `test_a_hook_git_does_not_track_is_marked_on_its_own_row`, an order assertion in the hook test, and three rows in the pure table (`tests/helpers.py`, `test/fixtures/data.json`, `spec/models/user.rb`). 54 of 54 pass on the real code in the two affected classes; the suite counts 150 tests; `.quality-gates.json` `migrate-layout-unit-tests` floor 146 to 150 (a tightening). Round 2 (the seven again, against these tests) is run next and is not yet shown. Model: Claude Sonnet 5.5.

### 2026-10-09 · [BL-101] S289 — the tool follow-up, F5: `bin/migrate-layout` lists the machine-read files a move relocates, apart from prose, every one

At the design gate he chose list only, the split of `other` into kinds, and to implement. `hit_category` (now `hit_category(path, text)`) sorts a file that names a moved path into `tests`, `proofs`, `scripts` or `config` beside the existing `ci`, `hooks`, `harness`, `ledger` and `other` (nine categories, was five; `.husky/` and `.pre-commit-config.yaml` are hooks; a prose extension under `tests/` stays prose; a `#!` first line makes an extensionless file a script). `scan_hits` keeps its matching rule and adds `paths` to each machine-read category: one row per file, uncapped, with its mentions, its mentions on non-comment lines, the names it carries and its first code-line mention; the 25-site cap stays. The text prints the rows under a sentence saying they are candidates the tool does not run, that a name on a code line is necessary and not sufficient, and what to rehearse. Reproduced first on the P11 adopter at `63cedc5` (tier all): `other` 2,647 mentions in 73 files, 25 sites shown, none of the 4 files that broke among them. Tests first (12 red), then the change: `tools/test_migrate_layout.py` 136 to 146 tests, the full suite `Ran 146 tests in 373.158s, OK` (load 4 to 6); `.quality-gates.json` `migrate-layout-unit-tests` floor 136 to 146 (a tightening); plan section 4.7 item 1 names the new kinds (59,890 of 60,000 B). `bin/check-layout-literals` 0 sites. Not yet run: the 10 adopters at their S286 pins, the mutation round, the gate run. Nothing distributed changed (the tool is canonical-only) and nothing went upstream. Model: Claude Sonnet 5.5.

### 2026-10-09 · [BL-101] S289 claim (in progress) — the tool follow-up, F5: `bin/migrate-layout` lists the machine-read files a move relocates

CHANGELOG: pending. Operator said `go`; at the Phase 0 picker he chose F5 as the deliverable (as decided at the S288 close-out) and left F6 and F8 open. The owed HANDOFFS trim (`4da0243`, S286's receipt to `HANDOFFS-through-2026-10-08-5.md`, shard proof exit 0 from a `--no-local` clone) and its fold (`753cae7`) ran before this claim. Deliverable: the tool follow-up (plan section 7.6, register row F5), Development workstream, design presented to him before code. P13 is not started and nothing goes upstream. Model: Claude Sonnet 5.5.

### 2026-10-09 · [ad hoc] S289 — fold the fifth 2026-10-08 HANDOFFS shard pointer into the archive index

The pointer block the trim (`4da0243`, 1 receipt, S286, 2026-10-08, to `HANDOFFS-through-2026-10-08-5.md`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, trimmer v1.8.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S288, S287). The shard proof was run by name from a `--no-local` clone of the trim commit: `HANDOFFS-through-2026-10-08-5.md.verify.sh` at `4da0243`, exit 0 (L1, L2/front-matter, L3). Model: Claude Sonnet 5.5.

### 2026-10-09 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-08-5.md` (1 record(s), 39,185 B → 27,594 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-08 → 2026-10-08) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-08-5.md`](docs/archive/HANDOFFS-through-2026-10-08-5.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-08-5.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-08-5.md.verify.sh)
rather than trusting a digest printed here. Live file 39,185 B → 27,594 B (−29.6%).

### 2026-10-09 · [BL-101] S288 — push record: main pushed to the fork origin at his go-ahead (793c7a1..0c5665a), and the F5-first decision

At the S288 close-out picker he chose to push; `git push origin main` sent S288's 5 commits (a plain fast-forward, `793c7a1..0c5665a`) to `rmsharp/methodology` and `git rev-list --left-right --count origin/main...main` read `0 0` after a fetch. Nothing went to `KJ5HST/methodology`. **Also decided at that picker, by him: F5 (the tool follow-up, plan section 7.6 and `findings-register.md`) comes BEFORE P13**, so the next session's deliverable is the tool follow-up (list a project's tests, scripts, proofs, CI and hooks that read a moved path, apart from prose; prototype `kind_of` in `s286-adopter-survey.py`); P13 follows it. This commit changes only `CHANGELOG.md` and is pushed too, under his standing grant for push records, so no further record is owed. Model: Claude Sonnet 5.5.

### 2026-10-09 · [BL-101] S288 close-out — the plan's learning loop is in; the receipt is complete; the gate run read 18/18

Receipt S288 is `status: complete` (self 8, predecessor 9; no fork learning row appended, so no retirement is owed: the rows considered are named in the receipt). `CHANGELOG: pending` on the S288 claim entry is cleared by this statement (the never-edit gate forbids editing a committed entry). Deliverable: the BL-101 plan amended at his instruction (section 0 item 9, section 7.6, `findings-register.md`, the D8 row and section 7.4's DONE list; the BL-101 row and Next action), within its 60,000 B budget (59,867 B), in `64d6730`; the owed HANDOFFS trim (`6b577fa`) and its fold (`de72073`) ran before the claim (`b19df50`). **The gate run on `64d6730` read `18/18 pass · 0 fail · 0 unmeasured`** (results `64b22c42cc89`, manifest `93aff6c93dbc`; `tests-sh-passed` 483 at three receipts, `migrate-layout-unit-tests` 136), at a load average of 5 to 9 in about 16 minutes, so BL-103's 600 s limit was not hit. Outside the repository: the memory index was compacted (22.6 KB to 17.5 KB) and the shell practice changed to `bash <<'EOF'` after he asked about zsh. **For him, at the next Phase 0:** whether F5 (the tool follow-up) precedes P13, as section 7.6 now says by default. Nothing was run in an adopter, pushed or sent upstream; this repository's `origin/main` is 5 commits behind after this one (his go-ahead). Model: Claude Sonnet 5.5.

### 2026-10-09 · [BL-101] S288 — the BL-101 plan amended: the adopter runs harden the sync route, and the plan learns from experience (§7.6, the findings register)

At his instruction after the Phase 0 report ("add to the goal to make the upstream sync process robust via what is learned when performing these local syncs"; "The plan must include learning from experience to be useful"). `docs/planning/methodology-subdirectory-plan.md`: a §0 item 9 marked as his addition; a new §7.6 (read the register before an adopter session; every finding of a run becomes a row, fixed with its test, open where tracked, or declined; a finding the tool's own checks did not see is fixed in its own session before the next adopter unless he chooses otherwise; D8's pull request carries the register); D8's text and §7.4's per-adopter DONE list name it. Held to the 60,000 B declared budget by recomposing (59,986 B to 59,867 B): cut text that restated §4.1, the DONE column of the finished P2-P6 rows (§7.2a-e carry it), §5A.3's duplicated bullets, the stale P5 cost and the stop conditions of three finished phases (the last now a pointer to the plan at `b19df50`). New: `docs/planning/methodology-subdirectory-evidence/findings-register.md`, nine findings seeded from the records of P7, S284, P11, S286 and P12, each re-read this session and each figure the record's; five are open, F5 (P11: the tool's checks did not see the 41 tests and 2 proofs that broke) first. The BL-101 index row and *Next action* say so. **Consequence, his to confirm:** under §7.6 the tool follow-up (F5) comes before P13 unless he chooses otherwise. Nothing was run in an adopter and nothing goes upstream; D8 is untouched. `bin/check-links --layout both` OK (80 links), `check-layout-literals` 0 sites, `check-ledger` OK, `check-learnings` OK; `context_budget.py --status` reads over its ceilings, identically on the pre-change commit. Model: Claude Sonnet 5.5.

### 2026-10-09 · [BL-101] S288 claim (in progress) — the BL-101 plan amended: the adopter runs harden the sync path, and the plan learns from experience

CHANGELOG: pending. Operator said `go`; the Phase 0 picker was declined for questions, and he then asked that the plan's goal include making the upstream sync process robust from what the local syncs teach, and that the plan include learning from experience. The owed HANDOFFS trim (`6b577fa`) and its fold (`de72073`) ran before this claim, the shard proof exit 0 from a `--no-local` clone. Deliverable: the plan amended (goal, per-adopter DONE criterion, re-read of the remaining phases against the findings), within its 60,000 B budget. P13 is not started and nothing goes upstream. Model: Claude Sonnet 5.5.

### 2026-10-09 · [ad hoc] S288 — fold the fourth 2026-10-08 HANDOFFS shard pointer into the archive index

The pointer block the trim (`6b577fa`, 1 receipt, S285, 2026-10-08, to `HANDOFFS-through-2026-10-08-4.md`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, trimmer v1.8.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S287, S286). The shard proof was run by name from a `--no-local` clone of the trim commit: `HANDOFFS-through-2026-10-08-4.md.verify.sh` at `6b577fa`, exit 0. Model: Claude Sonnet 5.5.

### 2026-10-09 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-08-4.md` (1 record(s), 41,067 B → 29,440 B)

**Written by:** `methodology_trim.py` v1.8.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-08 → 2026-10-08) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-08-4.md`](docs/archive/HANDOFFS-through-2026-10-08-4.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-08-4.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-08-4.md.verify.sh)
rather than trusting a digest printed here. Live file 41,067 B → 29,440 B (−28.3%).

### 2026-10-09 · [ad hoc] S287 — pushed `main` to the fork origin at his go-ahead (`a446fbf..211d3fc`, 14 commits), and this record with it

At the S287 close-out picker he chose to push; `git push origin main` sent S286's 7 commits and S287's 7 (a plain fast-forward) and `git rev-list --left-right --count origin/main...main` read `0 0` after a fetch. Nothing went to `KJ5HST/methodology`. This commit changes only `CHANGELOG.md` and is pushed too, under his standing grant for push records, so no further record is owed. Model: Claude Sonnet 5.5.

### 2026-10-09 · [BL-101] S287 close-out — P12 done at tier all; the receipt is complete; the gate run read 15/18 under load

Receipt S287 is `status: complete` (self 8, predecessor 9; no fork learning row appended, so no retirement is owed: the rows considered are named in the receipt). Deliverable: `feedback-loop-comparison` synced and moved at `--tier all` in its own repository (`8ce4ed6`, `40d2b74`, `2e77a73`; no remote, nothing pushed), with the record, plan §7.4b, and the BL-101 row and Next action. **The gate run on `f195c4a` read `15/18 pass · 0 fail · 3 unmeasured`:** `tests-sh-passed`, `tests-sh-failed` and `migrate-layout-unit-tests` hit the ratchet's 600 s limit at a machine load average of 15 to 21 (BL-103, whose backlog detail now records the second occurrence). They were run by hand on the same commit: `bash bin/tests.sh` 483 passed, 0 failed, 0 skipped (1,835 s) and `tools/test_migrate_layout.py` 136 tests OK (794 s). This repository's `origin/main` is 14 commits behind after this one (his go-ahead); the next Phase 0 owes the HANDOFFS trim (3 receipts). Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S287 — P12 done at tier all: `feedback-loop-comparison` synced and moved in its own repository; the record, plan §7.4b, and the BL-101 row and Next action

In `~/Development/feedback-loop-comparison` (a Quarto paper; no remote, tests, CI or hooks, so nothing was pushed): `8ce4ed6` `bin/sync --force` from this checkout at `c2cdbfd` (11 files updated, 16 created; the two files it refused without `--force` are older canonical copies, matched to `274dcd4` and `b1ba27e` by `diff` first), `40d2b74` `bin/migrate-layout --tier all` (30 renames, 27 at 100%), and `2e77a73` a correction of my own line count in the sync's ledger entry (10 by `diff`, not 9; a new entry, since a committed entry is not edited). The adopter's build (`quarto render index.qmd`, HTML and PDF) gives the same HTML and PDF text before and after, in clones; dashboard health 59, risk 0, before and after. The cost of tier 2: 23 relative links in its own `methodology/SESSION_NOTES.md` (0 before). `p12-feedback-loop-comparison-record.md` says what was and was not shown; plan §7.4b is added within the 60,000 B budget (59,986 B; §0 items 4 and 6, §2.2's footer, the header and §7.3c recomposed, no figure dropped); the BL-101 row and `Next action` say P13 is next and what is his. Nothing sent upstream. Model: Claude Sonnet 5.5.

### 2026-10-08 · [BL-101] S287 — the P12 reports: the tier-all rehearsal, the real dry run and apply, and the final clone's log

The `bin/migrate-layout --tier all` report on the rehearsal clone; the dry run on the real adopter (31 moves, one more than the clone's 30: the adopter's untracked, ignored `dashboard.html` moves plainly) and its apply (`40d2b74`, `checks (before -> after)` read in the record); and the log of the checks on a fresh clone of that commit: the paper renders with 0 warnings and the HTML and PDF text are identical to the original's, dashboard health 59 and risk 0 (the same as on the synced tree before the move), and Phase 0 reads in the new layout with 0 undocumented commits. Quoted prose and diff hunks removed. Model: Claude Sonnet 5.5.

