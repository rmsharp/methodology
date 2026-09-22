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

---

## 2026-09

### 2026-09-21 · [BL-66] S218 — the BL-66 plan ratified: D1–D8 all option (a) (operator decision)

- **Decision:** at this session's Phase 0 picker the operator ruled the eight decisions of
  [`sync-github-route-plan.md`](docs/planning/sync-github-route-plan.md) §3 all option (a), as recommended: the GitHub
  route becomes a fresh full clone plus the local path (D1, D2); one pull request with BL-54's two commits (D3); the same
  fix in `bin/status` (D4); a refusal that names a shallow or history-less source (D5); minimal document edits (D6); a
  branch from `upstream/main`, the PR opened after #84 merges (D7); `gh` dropped from both scripts (D8).
- **Recorded:** the plan's status line (DRAFT → RATIFIED); the BL-66 and BL-54 index rows in
  [`BACKLOG.md`](docs/planning/BACKLOG.md) (kept short, since that file is past its one-read budget: 57,603 → 57,611 B); one closing
  sentence each in their [`BACKLOG-DETAIL.md`](docs/planning/BACKLOG-DETAIL.md) blocks. `BACKLOG-DETAIL.md.verify.sh`
  C1–C5 OK; `./bin/check-links` OK.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] S218 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

- **What:** the trimmer's 3-line pointer block for `docs/archive/HANDOFFS-through-2026-09-21-7.md` became one row at
  the bottom of [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md) and was deleted from the ledger's
  front matter. `HANDOFFS.md` 14,582 B → 14,126 B.
- **Its own commit by design:** inside the trim commit the shipped `.verify.sh` fails L2 (fork Learning #58). The
  verifier was run against the trim commit `187374e`, in a `--no-local` clone, **before** the fold — it printed
  *"OK: L1, L2/front-matter, L3 hold"*, 3 records = 2 retained + 1 archived, 0 added by the trim commit.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-21-7.md` (1 record(s), 22,722 B → 14,582 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-21 → 2026-09-21) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-21-7.md`](docs/archive/HANDOFFS-through-2026-09-21-7.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-21-7.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-21-7.md.verify.sh)
rather than trusting a digest printed here. Live file 22,722 B → 14,582 B (−35.8%).

### 2026-09-21 · [BL-66] S218 claim — P1 of the BL-66 plan: `--source=github` becomes a fresh clone plus the local path, in `bin/sync` and `bin/status`, with red-first tests (in progress)

**Deliverable, chosen at this session's Phase 0 picker:** phase P1 of
[`docs/planning/sync-github-route-plan.md`](docs/planning/sync-github-route-plan.md) §5, on a new branch
`fix/sync-github-history` from `upstream/main` `6b29d3d`: BL-54's `2c4f801` and `865119f` cherry-picked, the GitHub
route cloning and then running the local code in both scripts, the `gh api` fetchers removed, `METHODOLOGY_SOURCE_URL`
honoured, S41's absent-source inventory re-expressed over the clone, two new tests written red first, Test 9's guard
changed. Nothing opens upstream (P5 is its own go-ahead).

**Ruling at the same picker:** the plan's eight decisions (§3), all option (a) as recommended — recorded in the plan by
its own commit. **Side actions approved:** the `HANDOFFS.md` retention trim this claim makes owed (three receipts) and
its fold; raising the backlog item for the fork-only prose-route rules (`starter-kit/BOOTSTRAP.md:364-400`); the fork
push at close-out.

**Phase 0 finding, reported, not acted on:** the dashboard (run in a clone at `63de9e0`) reads 76/100 with risk
**high** — `docs/planning/BACKLOG.md` at 57,603 B is past the 56,750 B one-read budget, crossed at `2e0fd02`
(56,502 → 57,383 B). A whole-file Read of it, measured in a subagent, returned all 228 lines untruncated, so the byte
figure is a floor for this file, not its cliff. No backlog item covers it; the operator chose P1 over archiving its
§Completed items (25,576 B).

### 2026-09-21 · [ad hoc] S217 — fork `main` pushed to `origin`, `f853edd..fbf269b` (non-commit action, operator go-ahead)

Six commits: this session's claim `90f4eca`, the `HANDOFFS.md` trim `e67c75b` and fold `f7a6c99`, BL-84 raised
`2e0fd02`, the BL-66 plan `d40f0e2`, and the close-out `fbf269b`. Guards before the push: on `main`, clean tree,
`origin/main` an ancestor of `HEAD`, no `.git/REBASE_HEAD`. Read back after a fetch: `origin/main` = `fbf269b` =
local `main`. **Nothing reached `KJ5HST/methodology`.** This record is pushed under the standing grant of
2026-09-16 (a `CHANGELOG.md`-only push record goes to fork `origin` unasked).

- **Model:** Claude Fable 5.1 (claude-fable-5-1)

### 2026-09-21 · [BL-66] S217 close-out — BL-66 planned (`d40f0e2`), the plan's deferral wording corrected, fork Learning #91, BL-84 raised as a side action

- **Deliverable:** [`docs/planning/sync-github-route-plan.md`](docs/planning/sync-github-route-plan.md), DRAFT — eight
  decisions for the operator, six phases; nothing implemented, nothing upstream-facing. This commit corrects its §1.2:
  B1 plan Decision 3 was *recommended and shipped that way in v2.8, and issue #32 closed on it* — not "ratified", which
  the `d40f0e2` entry above says and the B1 plan's own status line contradicts. `BACKLOG-DETAIL.md`'s BL-66 paragraph
  corrected the same way.
- **Phase 3C:** fork Learning #91 appended to [`docs/FORK_LEARNINGS.md`](docs/FORK_LEARNINGS.md) (1,120 B; checker OK,
  77 rows, 0 over budget): a deferral that chooses "document the limitation" is costed on one side — time the fix on a
  throwaway before choosing, and give the deferral a reopen condition. **D3:** rows #48, #71, #78, #79 considered; none
  retires (#71/#78/#79 are applied by the plan's P2/P3; #48 unrelated); S200's adjudication stands.
- **Receipt:** `HANDOFFS.md` S217 `status: complete`, `bin/check-handoff` OK; predecessor S216 scored 9 (exact on the
  trim's shard name, the ledger sizes and every gotcha; "both files are in #84's diff" was right about the files and
  not about `README.md:61`, which no open PR touches); self 8.
- **Gate citation** in the receipt: run in a `--no-local` clone at `d40f0e2`, identical to Phase 0's.
- **Session, whole:** `90f4eca` claim · `e67c75b` trim · `f7a6c99` fold · `2e0fd02` BL-84 · `d40f0e2` plan · this
  close-out. Fork `main` is pushed to `origin` after this commit (approved at the Phase 0 picker); its record follows.
- **Model:** Claude Fable 5.1 (claude-fable-5-1) from the plan on; Claude Opus 5 (claude-opus-5) for the claim and side actions.

### 2026-09-21 · [BL-66] S217 — plan written: `bin/sync --source=github` becomes a fresh clone plus the local path; the refusal names a history-less source; four documents reconciled

- **What:** [`docs/planning/sync-github-route-plan.md`](docs/planning/sync-github-route-plan.md) (37 KB, DRAFT), the
  session's one deliverable. Eight decisions for the operator (§3), six phases one session each (§5), the pull
  request at P5 as its own go-ahead. BL-66's index row and detail block point at it; BL-54's do too, because D3 proposes
  one pull request for both (the fix reuses the history walk BL-54 fixed fork-side). `BACKLOG-DETAIL.md` also gains the
  `<a id="bl-66">` anchor its index row already linked to.
- **Measured, not inferred (§1.1, §2.7):** on an adopter installed from `008d656`, never edited, updated toward
  `6b29d3d` — full clone: exit 0, 10 files, 2.2 s; shallow clone and tarball: exit 2, 9 refused; `--source=github`:
  exit 2, 9 refused, 12.3 s, an *"inspect the drift"* header with nothing under it; `bin/status --source=github`: 9
  *locally modified*, 0 behind. A full clone of upstream is 3.8 s / 2.2 MB; the route rebuilt over it runs in 4.9 s,
  exit 0. A blobless clone was tried and rejected: `cat-file --batch-check` fetched 43 blobs in 16 s for one file.
- **Provenance found (§1.2):** the gap is B1 plan Decision 3, *"Defer + document"* (issue #32), ratified by the
  maintainer; BOOTSTRAP got the sentence, `--help` never did; `README.md:61` is the maintainer's own line (`ce1ec629`).
- **Verified:** `BACKLOG-DETAIL.md.verify.sh` C1–C5 OK; `./bin/check-links` OK; every relative link and cited path in
  the plan resolves (one planned path, the P4 body file, does not exist yet by design).
- **Model:** Claude Fable 5.1 (claude-fable-5-1) — the session's claim and side actions were Claude Opus 5; the
  operator switched models before the plan.

### 2026-09-21 · [BL-84] S217 — BL-84 raised: the seed's fixed `CLAUDE.md` warn line against its mandatory purpose fence

- **What:** index row in [`BACKLOG.md`](docs/planning/BACKLOG.md) (after BL-83), BL-84 added to its `Open:` list, and a
  detail block at the end of [`BACKLOG-DETAIL.md`](docs/planning/BACKLOG-DETAIL.md#bl-84). The distributed seed
  `starter-kit/context-budget.json` gives every adopter's `CLAUDE.md` a fixed 24,000 B warn line and a fence of at least
  800 characters whose absence is `over`; a `CLAUDE.md` within about 850 B of the line cannot comply and stay `ok`.
- **Source:** relayed by the operator from `mts-system` S143 (a screenshot of that session's picker), measured
  read-only from here: 23,557 B → 24,603 B with the fence; the 495 B deletion offered there leaves 24,108 B, still
  `warn`. Four shapes, none costed; upstream-facing, its PR its own go-ahead. Approved as a side action at the Phase 0
  picker.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] S217 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

- **What:** the trimmer's 3-line pointer block for `docs/archive/HANDOFFS-through-2026-09-21-6.md` became one row at
  the bottom of [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md) and was deleted from the ledger's
  front matter. `HANDOFFS.md` 14,084 B → 13,628 B.
- **Its own commit by design:** inside the trim commit the shipped `.verify.sh` fails L2 (fork Learning #58). The
  verifier was run against the trim commit `e67c75b`, in a `--no-local` clone, **before** the fold — L1,
  L2/front-matter, L3 all OK, exit 0 (read from zsh's `pipestatus[1]`, the script's own status), 3 records = 2
  retained + 1 archived, 0 added by the trim commit.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-21-6.md` (1 record(s), 22,247 B → 14,084 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-21 → 2026-09-21) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-21-6.md`](docs/archive/HANDOFFS-through-2026-09-21-6.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-21-6.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-21-6.md.verify.sh)
rather than trusting a digest printed here. Live file 22,247 B → 14,084 B (−36.7%).

### 2026-09-21 · [BL-66] S217 claim — plan BL-66: `README.md`'s update advice (the GitHub URL route cannot update a file that is merely behind) against `starter-kit/BOOTSTRAP.md`'s opposite advice (in progress)

**Deliverable, chosen at this session's Phase 0 picker:** a plan in `docs/planning/` for BL-66 (its row in
[`BACKLOG.md`](docs/planning/BACKLOG.md), its block in [`BACKLOG-DETAIL.md`](docs/planning/BACKLOG-DETAIL.md#bl-66)). The
plan is the deliverable: no fix is made and nothing opens upstream. Upstream-bound work that can accumulate here while
#83–#86 wait; both files it names are in #84's diff, which the plan has to account for.

**Side actions approved at the same picker:** the `HANDOFFS.md` retention trim this claim makes owed (three receipts,
`--cut 2 --force`, dry run first) and its fold; raising **BL-84** — the distributed seed `starter-kit/context-budget.json`
gives every adopter's `CLAUDE.md` a fixed 24,000 B warn line *and* a mandatory purpose fence of at least 800 characters,
so a `CLAUDE.md` within about 850 B of the line cannot comply without warning (relayed by the operator from
`mts-system` S143, measured read-only there: 23,557 B before the fence, 24,603 B after); pushing fork `main` to `origin`
at close-out.

**Phase 0, for the record:** `CHANGELOG.md` frontier = HEAD `f853edd`, gap empty; `HANDOFFS.md` frontier `01116c6`,
the one commit after it being S216's announced push record. No pending stub, 2 receipts before this one; nothing
backfilled. Gate citation re-run in a `--no-local` clone at `f853edd`: `11/11 pass · 0 fail · 0 unmeasured · results
10575dac7361 · manifest 01a4ae7aa511`, S216's citation exactly (`tests-sh-passed` 343). Dashboard 76/100, medium, 0
high+, run in that clone. Upstream 0 open issues; #83 (`219fb9d`), #84 (`77afc12`), #85 (`e2501c5`), #86 (`c1167ae`)
open, 0 reviews, only our comments (`5755256040`, `5753335477`). `main` = `origin/main` = `f853edd`; `upstream/main`
`6b29d3d`. `CHANGELOG.md` 172,830 B before this entry, 23,778 B under the 196,608 B trigger: no trim owed.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] S216 — fork `main` pushed to `origin`, `68160ba..01116c6` (non-commit action, operator go-ahead)

Six commits: this session's claim `461e38b`, the `HANDOFFS.md` trim `1c1c4e3` and fold `2701247`, BL-78 closed
`2674c95`, BL-83 raised `38e4e11`, and the close-out `01116c6`. Fork remote only. Approved at this session's Phase 0
picker. Checked before: `origin/main` = `68160ba`, an ancestor of HEAD, so a fast-forward. Read back after:
`git ls-remote origin refs/heads/main` = `01116c6`, equal to local `main`. This record is pushed after it under the
standing push-record grant.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-78] S216 close-out — BL-78 closed with its record corrected (the ratchet exists, unwired); BL-83 raised; nothing upstream-facing

**Deliverable:** BL-78's closing edits, decided at S206 and chosen at this session's Phase 0 picker: `2674c95`
(row to §Completed items, closing update at [`BACKLOG-DETAIL.md`](docs/planning/BACKLOG-DETAIL.md)`:3029`,
`.context-budget.json:101` rewritten). Found on the way and recorded on the operator's choice: `38e4e11` (BL-83, fork
Learning #85's false example). Supporting: `461e38b` the claim; `1c1c4e3` + `2701247` the `HANDOFFS.md` trim and fold.
**The S206 decision was input, not output.** **Next: the maintainer's review of #83–#86 (P5 of the `context_budget.py`
plan after #86 merges); failing a reply, planning BL-66, upstream-bound, which opens nothing.**

**Phase 3A — S215's handoff scored 9/10.**
- *What helped:* every Phase 0 value held: the four heads, both comment ids, the `-5` shard name, the `CHANGELOG.md`
  estimate (~162 KB; 162,364 B). Step (2) named all three closing edits with exact lines (`BACKLOG.md:166`,
  `BACKLOG-DETAIL.md:3019-3023`, `.context-budget.json:101`), each true when opened, and its wording (*"a refusal
  nothing calls"*) was precise. Gotcha (4) (`./bin/check-links`) saved the call it cost S215.
- *What was missing:* that BL-78's own detail block contradicts that wording (S201: *"does not exist"*) and that
  S205's `files[5]._` already records the refusal. I rediscovered it from the tool, and the missing context cost one
  overstated claim to the operator.
- *What was wrong:* nothing false.
- *ROI:* clearly positive; Phase 0 to the claim needed no discovery.

**Phase 3B — self-assessment 8/10.**
- *Right:* Phase 0 in full, gate citation re-run in a clone. Before rewriting a sentence about a refusal, grepped the
  tool for the refusal rather than the field, and ran it (growth, shrink, control) instead of predicting it. The config
  edit was script-asserted to one key path, and the verdict was shown unchanged by running the tool at both commits.
  The trim's `.verify.sh` ran before the fold, and the suite after it. The two findings went into separate commits.
- *Wrong:* my second picker told the operator their S206 decision *"was costed as 'build a new check'"* before I read
  what S206 was shown. It was not. I read S205's receipt and S206's ledger entry and corrected it to the operator before
  any edit. Their answers held, but the claim should have been checked first.
- *Stakeholder corrections:* none. One self-correction, above.

**Phase 3C:** no fork-learnings row, so D3's retirement obligation does not arise. The past-decision lesson went to
agent memory. **Phase 3E:** the tool that reads the edited config ran at both commits (identical verdicts), and
`--precommit` was exercised; fork `main` clone of `38e4e11`: `quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured ·
results 10575dac7361 · manifest 01a4ae7aa511`, identical to Phase 0.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-83] S216 — BL-83 raised: fork Learning #85 teaches a false example (the ratchet it says does not exist is `context_budget.py --precommit`)

- **What:** a new open item — index row after BL-81 and `BL-83` added to the `Open:` list in
  [`docs/planning/BACKLOG.md`](docs/planning/BACKLOG.md); detail block at the end of
  [`BACKLOG-DETAIL.md`](docs/planning/BACKLOG-DETAIL.md#bl-83). Written from what was already measured while closing
  BL-78 (the `--precommit` runs: growth refused, exit 2; shrink passed, exit 0), and nothing further measured.
- **Why an item and not a fix:** `docs/FORK_LEARNINGS.md:19-20` permits only compaction as an edit to an existing
  row, and D1 (`CLAUDE.md:45`) names no false-row case. Three shapes are recorded, none costed; the decision is the
  operator's.
- **Operator, at this session's picker:** *"Raise a backlog item"*, over noting it in BL-78's closing alone.
- **Verified:** `BACKLOG-DETAIL.md.verify.sh` C1–C5 OK; `./bin/check-links` OK; the new anchor and its index link
  each appear once.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-78] S216 — BL-78 closed: the closing edits S206 left owed, and the record corrected where it said the ratchet does not exist

- **What:** BL-78's index row moved from the open table to §Completed items in
  [`docs/planning/BACKLOG.md`](docs/planning/BACKLOG.md), out of the `Open:` list and into the section heading's; a
  closing update at the end of its detail block ([`BACKLOG-DETAIL.md`](docs/planning/BACKLOG-DETAIL.md), before
  `#bl-79`); and `.context-budget.json` `files[4]._` (`starter-kit/SESSION_RUNNER.md`) rewritten in two sentences,
  the only key path changed (asserted by script, 35,090 → 35,745 B). No `max_bytes`, `max_tokens` or other key
  touched.
- **The note described the tool correctly and this clone wrongly**, as S206 said. Run in a `--no-local` clone at
  `2701247`: a staged one-line growth of `starter-kit/SESSION_RUNNER.md` made
  `python3 starter-kit/context_budget.py --precommit` print *"context-budget: REFUSED"* and exit 2; a staged shrink,
  exit 0; nothing staged, exit 0. The refusal is `def precommit` (`starter-kit/context_budget.py:1000`, byte test
  `:1037`, token arm `:1044-1051`); `.githooks/pre-commit` never calls it (its one gate call is
  `quality_ratchet.py --precommit`, `:133`), and no `.quality-gates.json` gate does. The note now says so, and
  that wiring was declined at S206 because merges skip the hook.
- **Corrected in the closing update, not in place:** BL-78's S201 paragraph (*"IT DOES NOT EXIST"*) and S203's
  *"has to build the check"* were false. S205 had already re-established that the refusal exists (`fac748f`'s
  `files[5]._`), so the S206 decision rested on §(3)'s merge finding, re-verified here by parent count. Fork
  Learning #85 carries the same false claim; raised as BL-83 in its own commit.
- **Operator, at this session's pickers:** the closing edits as the deliverable; then, told the check exists,
  *"Close, record the fix"*. The first picker framed S206's decision as made on the false premise; re-reading
  S205's receipt and S206's ledger entry showed it was not, and the operator was told before these edits.
- **Verified:** `BACKLOG-DETAIL.md.verify.sh` C1–C5 OK; `./bin/check-links` OK (111 links);
  `python3 tools/test_context_budget.py` 122 OK.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] S216 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

- **What:** the trimmer's 3-line pointer block for `docs/archive/HANDOFFS-through-2026-09-21-5.md` became one row at
  the bottom of [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md) and was deleted from the ledger's
  front matter. `HANDOFFS.md` 14,071 B → 13,615 B.
- **Its own commit by design:** inside the trim commit the shipped `.verify.sh` fails L2 (fork Learning #58). The
  verifier was run against the trim commit `1c1c4e3`, in a `--no-local` clone, **before** the fold — L1,
  L2/front-matter, L3 all OK, exit 0 (read bare, not through a pipe), 3 records = 2 retained + 1 archived, 0 added
  by the trim commit.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-21-5.md` (1 record(s), 25,815 B → 14,071 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-21 → 2026-09-21) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-21-5.md`](docs/archive/HANDOFFS-through-2026-09-21-5.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-21-5.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-21-5.md.verify.sh)
rather than trusting a digest printed here. Live file 25,815 B → 14,071 B (−45.5%).

### 2026-09-21 · [BL-78] S216 claim — BL-78's closing edits: the stale index row, the move to Completed items, and `.context-budget.json`'s unwired "refused" sentence (in progress)

**Deliverable, chosen at this session's Phase 0 picker:** the closing edits BL-78's S206 decision left owed
([`BACKLOG-DETAIL.md`](docs/planning/BACKLOG-DETAIL.md)`:3019-3023`, P3 = no enforcement, so the item closes). Rewrite
BL-78's index row ([`BACKLOG.md`](docs/planning/BACKLOG.md)`:166`, still the pre-P1 text), move it to Completed items
by the backlog's own convention, and correct `.context-budget.json:101` (`files[4]._`, `starter-kit/SESSION_RUNNER.md`),
whose *"every commit that grows it is refused"* describes a refusal nothing calls. A comment edit: no threshold
changes, and the pre-commit ratchet runs on it. Fork-local; nothing upstream-facing.

**Side actions approved at the same picker:** the `HANDOFFS.md` retention trim this claim makes owed (three receipts,
`--cut 2 --force`, dry run first) and its fold; pushing fork `main` to `origin` at close-out.

**Phase 0, for the record:** `CHANGELOG.md` frontier = HEAD `68160ba`, gap empty; `HANDOFFS.md` frontier `78cb080`,
the one commit after it being S215's announced push record. No pending stub, 2 receipts before this one; nothing
backfilled. Gate citation re-run in a `--no-local` clone at `68160ba`: `11/11 pass · results 10575dac7361 ·
manifest 01a4ae7aa511`, S215's citation exactly (`tests-sh-passed` 343). Dashboard 76/100, medium, 0 high+, run in
that clone. Upstream 0 open issues; #83 (`219fb9d`), #84 (`77afc12`), #85 (`e2501c5`), #86 (`c1167ae`) open, 0
reviews, only our comments (`5755256040`, `5753335477`). `main` = `origin/main` = `68160ba`; `upstream/main` `6b29d3d`.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] S215 — fork `main` pushed to `origin`, `58f5d34..78cb080` (non-commit action, operator go-ahead)

Five commits: this session's claim `0b3e355`, the `HANDOFFS.md` trim `fc1f05a` and fold `b4d22c4`, the P4 records
`34011a7`, and the close-out `78cb080`. Fork remote only. The PR branch `fix/context-budget-status` was pushed
separately under P4 and is #86's head. Approved at this session's Phase 0 picker. Checked before: `origin/main` =
`58f5d34`, an ancestor of HEAD, so a fast-forward. Read back after: `git ls-remote origin refs/heads/main` =
`78cb080`, equal to local `main`. This record is pushed after it under the standing push-record grant.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-75] S215 close-out — P4 of the `context_budget.py` plan done: the branch pushed, the upstream PR opened as #86 with the approved text

**Deliverable:** P4 of [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md)
(*P4 outcome* `:731`). `fix/context-budget-status` pushed to fork `origin` at `c1167ae`, and
[#86](https://github.com/KJ5HST/methodology/pull/86) opened into `KJ5HST/methodology:main` with the title and body
the operator approved at S214, posted unchanged and read back equal. Recorded `34011a7`. Supporting: `0b3e355` the
claim; `fc1f05a` + `b4d22c4` the `HANDOFFS.md` trim and fold. **The plan and the body were input, not output.** **Next:
the maintainer's review; P5 after the merge. Failing a reply, BL-78's closing edits (fork-local).**

**Phase 3A — S214's handoff scored 9/10.**
- *What helped:* step (1) was an exact recipe and every value held: P4 at `:719`, the pre-checks, the conditional *"if
  either moved, re-measure"* (neither had), the `gh pr create` form with `--head rmsharp:…`, and the read-back against
  `c1167ae`. Step (2)'s heads and comment ids held. Step (3) predicted the `-4` shard name. Gotcha (3) (a fork-only
  preamble; post from `:16`, the title from `:12` without its label; backticks, so pass from a file) shaped the
  extraction script.
- *What was missing:* where P4's outcome is recorded: the plan's status block, and the body file's preamble, which has
  to stay three lines so `:12` and `:16` stay true. Derived here.
- *What was wrong:* nothing false. The `CHANGELOG.md` estimate (~155 KB) was labelled as one; it measured 152,720 B.
- *ROI:* clearly positive. Phase 0 to the go-ahead needed no discovery.

**Phase 3B — self-assessment 9/10.**
- *Right:* Phase 0 in full, with the gate citation re-run in a clone. One picker for all three go-aheads, quoting the
  title and proving the body's identity with `cmp` instead of re-pasting 14 KB of approved text. The queue and both heads
  re-checked immediately before the outward action. The title and body extracted by a script that asserted their anchors,
  and posted from files. The PR read back through two APIs and compared by script. The trim's `.verify.sh` ran before the
  fold, and the suite after it. A Test 9 failure diagnosed from its output as a network timeout and re-run alone
  (343 / 0 / 6), neither accepted nor ignored. The preamble edit kept to three lines, and the posted text re-proved
  with `cmp`.
- *Wrong:* `bash bin/check-links` (the checker is Python; one wasted call). An unquoted `echo ====` in zsh, a known trap
  that recurred. An `&&` chain stopped silently after a timed-out `upstream` fetch; caught because the expected lines
  were missing, then retried. None affected a result.
- *Stakeholder corrections:* none.

**Phase 3C:** no fork-learnings row, so D3's retirement obligation does not arise. The zsh recurrence and the
`check-links` note went to agent memory. **Phase 3E:** the PR was read back; fork `main` at `34011a7`:
`quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results 10575dac7361 · manifest 01a4ae7aa511`, identical to
Phase 0.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-75] S215 — P4's outcome recorded: the plan, the body file's status, BL-75 and BL-80

[`context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md): the status block says P4 is done,
with a *P4 outcome* under §5 P4. [`context-budget-status-pr-body.md`](docs/planning/context-budget-status-pr-body.md):
the fork-only preamble now says the text was posted unchanged as #86. It stays three lines, so the title stays at
`:12` and the body at `:16`, and the body still `cmp`-equals what was posted. The BL-75 and BL-80 index rows and
detail each gained an S215 paragraph (nothing above them edited). Both items stay open until the PR merges.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-75] S215 — P4: upstream PR [#86](https://github.com/KJ5HST/methodology/pull/86) opened with the approved text (non-commit action, operator go-ahead)

`gh pr create -R KJ5HST/methodology --base main --head rmsharp:fix/context-budget-status`, with the title from
`docs/planning/context-budget-status-pr-body.md:12` (label dropped) and the body from `:16`, both passed from files.
Both are the text the operator approved at S214, and the body is byte-identical to `fb324d6`'s. Go-ahead at S215's
Phase 0 picker. **Checked before:** `upstream/main` `6b29d3d` and the branch `c1167ae`, both unchanged since S214,
so the figures stand as measured; #83/#84/#85 unchanged, 0 reviews. **Read back after:** open, not a draft, head
`c1167ae`, base `main`, 6 commits, 5 files, +631 / −11. The body equals the file apart from the trailing newline,
and the title is identical. `mergeable_state: clean`. The maintainer now has four open PRs from this fork (#83,
#84, #85, #86), none reviewed.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-75] S215 — P4: `fix/context-budget-status` pushed to fork `origin` (non-commit action, operator go-ahead)

`git push -u origin fix/context-budget-status`, a new branch on `rmsharp/methodology` at `c1167ae` (six commits on
`upstream/main` `6b29d3d`). Go-ahead at S215's Phase 0 picker. Read back after: `git ls-remote origin
refs/heads/fix/context-budget-status` = `c1167ae`. The branch is now tracked; it is the head of #86.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] S215 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

- **What:** the trimmer's 3-line pointer block for `docs/archive/HANDOFFS-through-2026-09-21-4.md` became one row at
  the bottom of [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md) and was deleted from the ledger's
  front matter. `HANDOFFS.md` 17,666 B → 17,210 B.
- **Its own commit by design:** inside the trim commit the shipped `.verify.sh` fails L2 (fork Learning #58). The
  verifier was run against the trim commit `fc1f05a`, in a `--no-local` clone, **before** the fold — L1,
  L2/front-matter, L3 all OK, exit 0 (read bare, not through a pipe), 3 records = 2 retained + 1 archived, 0 added
  by the trim commit.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-21-4.md` (1 record(s), 29,010 B → 17,666 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-21 → 2026-09-21) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-21-4.md`](docs/archive/HANDOFFS-through-2026-09-21-4.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-21-4.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-21-4.md.verify.sh)
rather than trusting a digest printed here. Live file 29,010 B → 17,666 B (−39.1%).

### 2026-09-21 · [BL-75] S215 claim — P4 of the `context_budget.py` plan: push the branch to fork `origin` and open the upstream PR with the approved text (in progress)

**Deliverable:** P4 of [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md)
§5 (`:719`): push the local branch `fix/context-budget-status` (`c1167ae`) to fork `origin`, then open the pull
request into `KJ5HST/methodology:main` with the title at
[`context-budget-status-pr-body.md`](docs/planning/context-budget-status-pr-body.md)`:12` (label dropped) and the
body from `:16`, approved as written at S214. Read back after: body equal to the file, head `c1167ae`. **Both are
outward actions; the operator gave the go-ahead at this session's Phase 0 picker.** Neither head moved since S214
(`upstream/main` `6b29d3d`, branch `c1167ae`), so the body's figures stand unre-measured; its text from `:16` is
byte-identical to `fb324d6`'s (`cmp`).

**Side actions approved at the same picker:** the `HANDOFFS.md` retention trim this claim makes owed (three
receipts, `--cut 2 --force`, dry run first) and its fold; pushing fork `main` to `origin` at close-out.

**Phase 0, for the record:** `CHANGELOG.md` frontier = HEAD `58f5d34`, gap empty; `HANDOFFS.md` frontier `1b5365e`,
the one commit after it being S214's announced push record. No pending stub, 2 receipts before this one; nothing
backfilled. Gate citation re-run in a `--no-local` clone at `58f5d34`: `11/11 pass · results 10575dac7361 ·
manifest 01a4ae7aa511`, S214's citation exactly. Dashboard 76/100, medium, 0 high+, run in that clone. Upstream 0
open issues; #83 (`219fb9d`), #84 (`77afc12`), #85 (`e2501c5`) open, 0 reviews, only our comments (`5755256040`,
`5753335477`). `main` = `origin/main` = `58f5d34`; `fix/context-budget-status` not on `origin`.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] S214 — fork `main` pushed to `origin`, `8089df7..1b5365e` (non-commit action, operator go-ahead)

Eight commits: S213's post-close-out decision record `2c711ab`, then this session's claim through its close-out. Fork
remote only — **nothing upstream-facing**, and the local branch `fix/context-budget-status` (`c1167ae`) was **not**
pushed (P4's go-ahead). Approved at this session's Phase 0 picker. Checked before: HEAD = `1b5365e`, `origin/main` =
`8089df7`, a fast-forward. Read back after: `git ls-remote origin refs/heads/main` = `1b5365e`, equal to local `main`;
no `fix/context-budget-status` on `origin`. This record is pushed after it under the standing push-record grant.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-75] S214 close-out — P2c and P3′ of the `context_budget.py` plan done in one session; the PR body approved as written; nothing upstream-facing

**Deliverable:** P2c then P3′ of [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md),
one session under the operator's rules at `:603`. **P2c** = `2f73733` on the local branch `fix/context-budget-status`
(a check may raise a row's status, never lower it), verified in a fresh clone before fetch-back; recorded `afb5be7`
(*P2c outcome* `:635`). **P3′** = `c1167ae` (floors 142/140), trial merges with #84/#85/#83 green, the body rewritten
(`fb324d6`, *P3′ outcome* `:682`), **approved as written** at the review picker, recorded `e12cf47`. Supporting:
`949d952` claim; `3740ec2` + `bc2a85b` the `HANDOFFS.md` trim and fold. **The plan and D7 were input, not output;**
this session built them, and added two mutants beyond the plan's two. **Next: P4 (push the branch, open the PR), its
own session and go-ahead.**

**Phase 3A — S213's handoff scored 9/10.**
- *What helped:* step (1) was an exact recipe and every value held: the clone command, HEAD `612570b`, blob
  `f75482c2`, the guard at `:430` (not `:427`), `order` `:598`, the ranking comment `:1452-1454`, the two test classes.
  Step (2)'s *"141/129 against measured 142/136 plus P2c's"* was right (142/140). Step (4) predicted the `-3` shard
  name. Gotcha (4) (guard a scratch path; build runners in Python) shaped every runner this session.
- *What was missing:* the plan's P5 line still said `--check` *"now exits 3"*, though S212 had corrected the §6 row
  beside it; caught at Phase 0. Gotcha (7) had dropped S212's zsh `:r` warning, and this session hit it once. The
  plan's test 1 did not anticipate that a resident fixture also trips its derived token ceiling.
- *What was wrong:* nothing false. The ~138 KB `CHANGELOG.md` estimate was labelled as one.
- *ROI:* clearly positive.

**Phase 3B — self-assessment 9/10.**
- *Right:* Phase 0 in full, with the gate citation re-run in a clone. One picker for the deliverable and all side actions.
  The trim's `.verify.sh` ran before the fold, and `bin/tests.sh` after it. RED first, each failure read at the assertion
  under test after the fixture assertions passed. A fixed baseline before four mutants, with two added so each control is
  shown load-bearing alone. P2c verified in a fresh clone **before** fetch-back, so a wrong upstream count could still be
  amended. P3′'s gate honoured. Every figure in the body re-measured, the merge-result ratchets run serially. The body
  pasted inline before the picker, and the approval recorded as approval of the text, not as P4's go-ahead. Every line
  the records cite was grepped on its own tree.
- *Wrong:* `pr$n:refs` in zsh fetched nothing (the `:r` modifier). It was caught at once because `rev-parse` printed empty,
  and redone braced; no result depended on it. Two self-caught record errors before commit: a status-line citation
  (`:12-15` → `:12-16`) and an ambiguous *"above the first tightening"* in the floors entry. The first receipt draft was
  368 B over the per-record budget; cut to 12,200 B by pointing at the plan instead of repeating it.
- *Stakeholder corrections:* none; the body was approved as written on first review.

**Phase 3C:** no fork-learnings row, so D3's retirement obligation does not arise. The zsh recurrence went to agent memory.
**Phase 3E:** the tool was run (`behaviour.py`, `cases.py`); citations are in the receipt: branch `10/10 · 8a465ec9a35d`,
fork `main` at `e12cf47` `11/11 · 10575dac7361`, identical to Phase 0.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-75] S214 — the operator's review of the P3′ body: approved as written (decision; recorded)

- **What:** the rewritten body (`docs/planning/context-budget-status-pr-body.md` at `fb324d6`) was pasted inline in
  full, then put to the operator at a review picker. **Answer: "Approve as written."** Recorded in the plan (status
  line and *P3′ outcome*), the body file's preamble, BL-75's and BL-80's index rows and detail paragraphs. **Not a
  go-ahead for P4:** pushing `fix/context-budget-status` to fork `origin` and opening the PR remain their own
  session and their own go-ahead. Nothing posted, nothing pushed. `BACKLOG-DETAIL.md.verify.sh` C1–C5 OK;
  `bin/check-links` OK.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-75] S214 — P3′: the PR body rewritten, the plan's P3′ outcome recorded, and P5's stale `--check` line corrected

- **What:** [`docs/planning/context-budget-status-pr-body.md`](docs/planning/context-budget-status-pr-body.md)
  rewritten on the tip `c1167ae`, recomposed from the draft reviewed at S212 rather than patched (that draft stays
  readable as `git show e4ad63d:docs/planning/context-budget-status-pr-body.md`). It now covers three defects (the
  missing `--status` and ignored arguments, the advisory, and status precedence). Every figure in it was re-measured
  this session: the before/after behaviour in clean clones of `6b29d3d` and `c1167ae`, the two contradictions in
  `mktemp` projects, the trial merges and the ratchet on each merge result, the citation counts, the adopter flag
  inventory, and the diff. Jargon scan 0 hits; `bin/check-links` OK. **Not posted; nothing pushed.**
- **Also:** [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md) status line
  (`:12-17`) and a *P3′ outcome* block under §5 P3′; and P5's *"`wsfct` … must be told that `--check` now exits 3"*,
  false since D6, now says `--check` measures and reports without a history row (approved at this session's Phase 0
  picker).
- **Trial merges from `c1167ae`, each merged for real in a scratch clone:** #84 clean (tree equal to `merge-tree`'s),
  `10/10 · results e1b3029504e8`, `bin/tests.sh` 166 / 0; #85 `CHANGELOG.md` only, `11/11 · results 91e29f97f572`;
  #83 `CHANGELOG.md` only, `10/10 · results 8a465ec9a35d`. Every `CHANGELOG.md` entry kept and counted.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-75] S214 — P3′: upstream's two floors tightened again, `c1167ae` on the LOCAL branch (commit + fast-forward; not pushed)

- **What:** `.quality-gates.json:10` `tests-sh-passed` 141 → 142 and `:34` `context-budget-unit-tests` 129 → 140, the
  values measured on `2f73733` in a fresh clone, plus one upstream `CHANGELOG.md` entry (the branch's new top, `:38`;
  jargon scan 0 hits). A new commit: `d4dbc26` stays, so the two floor commits drop together. Built in the same
  `--no-local` clone with `core.hooksPath` set; the pre-commit ratchet accepted the tightening. Fetched back as a
  fast-forward `2f73733..c1167ae`.
- **Evidence:** a fresh clone at `c1167ae`, HEAD asserted: `--selftest` 52 PASS, the `--force` grep empty, upstream's
  ratchet `10/10 · results 8a465ec9a35d · manifest ca680a8b0c9f`, the new floors met exactly.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-80] S214 — the plan's P2c outcome recorded

- **What:** [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md) status line
  (`:12-16`) and a *P2c outcome* block (`:633`) under §5 P2c: the change, the RED record, the four mutants, the upstream entry,
  and the fresh-clone verification. Every line it cites on `2f73733` was grepped on that tree. BL-75's and BL-80's
  backlog rows move with P3′'s records, at the end of this session.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-80] S214 — P2c built: `2f73733` on the LOCAL branch `fix/context-budget-status` (commit + fast-forward; not pushed)

- **What:** the plan's D7 in `starter-kit/context_budget.py`, built in a `--no-local` clone of the local branch (HEAD
  asserted `612570b`, tool blob asserted `f75482c2`, `core.hooksPath` set, both hooks passing on the commit), then
  fetched back as a fast-forward `612570b..2f73733`, with no remote tracking. In `measure_file()`, a structure pattern
  below its `expect_min` no longer overwrites a ceiling's `over` with `instrument-failed` (the guard at `:434` on
  `2f73733`), so a check can raise a row's status and never lower it. The comment above `main()`'s exit, which said
  the ordering ranks an instrument failure above `over`, now says what the code does. Tool blob `f75482c2` →
  `ea68573e`. Three files: the tool, `tools/test_context_budget.py` (a new `TestStatusPrecedence`, 4 tests) and the
  branch's `CHANGELOG.md` (one upstream entry at `:38`, jargon scan 0 hits).
- **Evidence:** the end-to-end and `--json` tests are red on `f75482c2` at the assertion under test; the two controls
  pass there by design. Four mutants were killed after the fixed baseline passed the harness, each test killing one
  the others miss. In a fresh clone at `2f73733`: 140 unit tests OK, `--selftest` 52 PASS, the `--force` grep empty,
  `bin/tests.sh` 142 / 0, upstream's ratchet `10/10 · results 43c4abce5653 · manifest ba1ef0894ed2`.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] S214 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

- **What:** the trimmer's 3-line pointer block for `docs/archive/HANDOFFS-through-2026-09-21-3.md` became one row at
  the bottom of [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md) and was deleted from the ledger's
  front matter. `HANDOFFS.md` 17,555 B → 17,099 B.
- **Its own commit by design:** inside the trim commit the shipped `.verify.sh` fails L2 (fork Learning #58). The
  verifier was run against the trim commit `3740ec2`, in a `--no-local` clone, **before** the fold — L1,
  L2/front-matter, L3 all OK, exit 0 (read bare, not through a pipe), 3 records = 2 retained + 1 archived, 0 added
  by the trim commit.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-21-3.md` (1 record(s), 28,320 B → 17,555 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-21 → 2026-09-21) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-21-3.md`](docs/archive/HANDOFFS-through-2026-09-21-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-21-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-21-3.md.verify.sh)
rather than trusting a digest printed here. Live file 28,320 B → 17,555 B (−38.0%).

### 2026-09-21 · [BL-75] S214 claim — P2c and P3′ of the `context_budget.py` plan, one session: D7, then re-vet and re-package (in progress)

**Deliverable:** P2c then P3′ of [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md)
§5, under the one-session rules at `:600` (the operator's decision, `2c711ab`). **P2c** (`:615`): D7 on the **local**
branch `fix/context-budget-status` from `612570b`, built in a `--no-local` clone and fetched back as a fast-forward:
a check may raise a row's status, never lower it, so a byte ceiling's `over` survives a failed structure pattern.
Four tests written to fail first against tool blob `f75482c2`, two mutants. **P3′** (`:632`), only if P2c's
fresh-clone verification is green: re-measure, a new floors commit, trial merges against #83/#84/#85 with the ratchet
on each merge result, and the PR body rewritten from the frozen draft. The session ends on the operator's review of
that body, pasted inline. **Nothing pushed to upstream, nothing opened.** Chosen at this session's Phase 0 picker
over P2c alone and BL-78's closing edits.

**Side actions approved at the same picker, each its own commit or record:** the `HANDOFFS.md` retention trim this
claim makes owed (three receipts, `--cut 2 --force`) and its fold; correcting the plan's stale P5 sentence (`:668`,
*"`--check` now exits 3"*, false since D6) in P3′'s records commit; pushing fork `main` to `origin` at close-out
(including `2c711ab`, not yet pushed).

**Phase 0, for the record:** `CHANGELOG.md` and `HANDOFFS.md` frontiers both = HEAD `2c711ab`, gap empty. No pending
stub, 2 receipts before this one; nothing backfilled. Gate citation re-run in a `--no-local` clone at `2c711ab`:
`11/11 pass · results 10575dac7361 · manifest 01a4ae7aa511`, S213's citation exactly. Dashboard 76/100, medium,
0 high+, run in that clone. Upstream 0 open issues; #83 (`219fb9d`), #84 (`77afc12`), #85 (`e2501c5`) open,
0 reviews, only our comments. `main` 1 ahead of `origin/main` (`8089df7`); `upstream/main` still `6b29d3d`;
`fix/context-budget-status` = `612570b`.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-75] S213 — operator decision after close-out: P2c and P3′ of the `context_budget.py` plan combined into one session

The operator, after S213's close-out: *"add combining P2c and P3' into one session"*. S213 proposed it when asked
what the work is for, on cost grounds: most of each session goes on re-orienting and re-verifying the same tree, and
P3′'s first step is to re-measure the tip P2c has just verified. **Scheduled, not started.** Recorded in:
- [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md): the status line
  (`:12-15`), §5's heading, the P2c and P3′ headings, and a new block just above §5 P2c (`:600`) that keeps the
  boundary as a gate inside the session. P2c comes completely first. P3′ starts only if P2c's fresh-clone
  verification is green; otherwise the session closes out at P2c. The two keep separate commits, and the session
  ends on the operator's review of the rewritten body. P4 stays its own session and its own go-ahead.
- S213's `HANDOFFS.md` receipt: `active_task`, `next_steps` (1)–(2), and the plan line numbers in `key_files` and
  `next_steps`, which the status line's extra line moved by one. Each was grepped on the tree.
- BL-75's detail (a paragraph appended) and the BL-75/BL-80 index rows (`docs/planning/BACKLOG.md:164`, `:168`).

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] S213 — fork `main` pushed to `origin`, `00b8685..6010083` (non-commit action, operator go-ahead)

Five commits, this session's claim through its close-out. Fork remote only — **nothing upstream-facing**, and the
local branch `fix/context-budget-status` (`612570b`) was **not** pushed (P4's go-ahead). Approved at this session's
Phase 0 picker. Checked before: HEAD = `6010083`, `origin/main` = `00b8685`, a fast-forward; pushed by sha. Read back
after: `git ls-remote origin refs/heads/main` = `6010083`, equal to local `main`; no `fix/context-budget-status` on
`origin`. This record is pushed after it under the standing push-record grant.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-75] S213 close-out — P2b of the `context_budget.py` plan built on `612570b` (D6: `--check` = `--status`, a hint per refused argument); nothing upstream-facing

**Deliverable:** P2b of [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md)
(`:514`), built as specified on the local branch `fix/context-budget-status`: `612570b`, fetched back as a
fast-forward from `d4dbc26`, not pushed. Verified in a fresh clone. Recorded in `0ab32fe` (the plan's *P2b outcome*
at `:554`, P2c's lines on `612570b` at `:586`). Supporting commits: `cd34113` claim; `aec024f` + `b0aeaee` the
`HANDOFFS.md` trim and fold. **The plan and D6 were input, not output;** this session built them, added one test the
plan's list missed (one line per unknown argument), and added the optional shell row. **Next: P2c (D7).**

**Phase 3A — S212's handoff scored 9/10.**
- *What helped:*
  - Next step (1) was an exact recipe, and every value in it held: the clone command, HEAD `d4dbc26`, blob
    `dd4803bf`, the entry position `CHANGELOG.md:38`.
  - Every branch line citation this session used held on `d4dbc26`, and those in the tool and the test file that
    moved did so by exactly this session's insertions. `.quality-gates.json:10`/`:34` were not used and not checked.
  - Gotcha (3) (the hint table below `def selftest`, keyed lookups, no `def selftest` in a comment above the list)
    is what mutant M5 now proves: moved above, `--selftest` exits 2.
  - Gotcha (4) (0.75, measured) held when re-measured with `--check` in the candidate list.
  - Steps (3) and (4) (the PR checks, and the trim at three receipts) were right.
- *What was missing:* the plan's seven tests did not cover the one-line-per-argument change the same phase specifies.
  An eighth test was added, and it went red on the old tool. It said nothing about `VERSION` (it stays 1.3.0, P1's bump).
- *What was wrong:* nothing false. Gotcha (5) (*"update `:580` and `:583` for the new format"*) was unneeded rather than
  wrong: a single refusal still contains `unknown argument: <arg>`, so neither changed. The `CHANGELOG.md` estimate
  (~130 KB) was labelled an estimate; 127,234 B was measured at Phase 0.
- *ROI:* clearly positive.

**Phase 3B — self-assessment 8/10.**
- *Right:*
  - Phase 0 in full, with the gate citation re-run in a clone.
  - One picker for the deliverable and both side actions.
  - The trim's `.verify.sh` run before the fold, and `bin/tests.sh` after it.
  - RED first, with each failure read at the assertion under test.
  - The fixed baseline through the mutant harness before the five mutants, each test run by name; M5 run, not reasoned.
  - The `difflib` table and the flag inventory re-measured at today's heads before either went into outward text.
    Checking it tightened one sentence of the upstream entry to say where it was measured.
  - Every line cited on `612570b` grepped on that tree; the verification done in a fresh clone.
- *Wrong:* a throwaway runner for the shell row, built by filtering `bin/tests.sh` through a nested BSD `sed`
  expression, came out with an empty header. `$P` was empty, and `(cd "$P" && git add -A && git commit …)` ran in the
  work clone. The ledger hook refused the commit. The three intended files were left staged and were unstaged
  before going on. A second `sed` attempt failed on its own delimiter and ran nothing. The rebuild used Python with a
  guard on `$P`. That cost two round trips and was contained by a hook, not by care.
- *Operator corrections:* none.

**Phase 3C:** no fork-learnings row, so D3's retirement obligation does not arise. The lesson is shell-specific:
guard a scratch path before any mutating command that `cd`s into it, and never build a harness by `sed`-filtering a
script. It went to agent memory.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-75] S213 — the plan's P2b outcome recorded; BL-75's and BL-80's rows moved on

- **What:** [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md) status line
  (`:12-14`) and a *P2b outcome* block under §5 P2b. It gives what was built, the re-measurements, the RED record, the
  mutant table, the fresh-clone verification, and **P2c's line numbers on `612570b`**. Also BL-75's S213 paragraph
  (`docs/planning/BACKLOG-DETAIL.md`, end of the BL-75 section) and the BL-75 and BL-80 index rows
  (`docs/planning/BACKLOG.md:164`, `:168`). Every line cited on `612570b` was grepped on that tree before commit.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-75] S213 — P2b built: `612570b` on the LOCAL branch `fix/context-budget-status` (commit + fast-forward; not pushed)

- **What:** the plan's D6 in `starter-kit/context_budget.py`, built in a `--no-local` clone of the local branch (HEAD
  asserted `d4dbc26`, `core.hooksPath` set, both hooks passing on the commit), then fetched back as a fast-forward
  `d4dbc26..612570b`, with no remote tracking. `--check` is accepted as the `--status` run. Each refused argument gets
  its own line and a hint (`--force` → `.context-budget.json`; `--dry-run` → `--status`; `--run`/`--write` → run with no
  argument; a misspelling → the nearest accepted argument at `difflib` cutoff 0.75; anything else → nothing). Tool
  blob `dd4803bf` → `f75482c2`. Four files: the tool, `tools/test_context_budget.py`, `bin/tests.sh` (one row) and the
  branch's `CHANGELOG.md` (one upstream entry at `:38`, jargon scan 0 hits).
- **Evidence:** 6 of 7 new tests plus the frozen set are red on `dd4803bf`; the two controls pass there by design. The
  new shell row is red there too (exit 3 against 1), run standalone. Five mutants were killed after the fixed baseline
  passed the harness. In a fresh clone at `612570b`: 136 unit tests OK, `--selftest` 52 PASS, both `--force` greps
  empty, `bin/tests.sh` 142 / 0, upstream's ratchet `10/10 · results c52d62cd50a4 · manifest ba1ef0894ed2`.
- **One mistake, contained:** a first standalone runner for the shell row was built with a BSD `sed` filter that
  produced an empty header. So `$P` was empty, and `(cd "$P" && git add -A && git commit …)` ran inside the work clone. The
  ledger hook refused the commit. The only effect was staging the three intended files there, and they were
  unstaged (`git reset -q`) and checked before going on. The runner was rebuilt in Python with a guard on `$P`.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] S213 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

- **What:** the trimmer's 3-line pointer block for `docs/archive/HANDOFFS-through-2026-09-21-2.md` became one row at
  the bottom of [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md) and was deleted from the ledger's
  front matter. `HANDOFFS.md` 16,745 B → 16,289 B.
- **Its own commit by design:** inside the trim commit the shipped `.verify.sh` fails L2 (fork Learning #58). The
  verifier was run against the trim commit `aec024f`, in a `--no-local` clone, **before** the fold — L1,
  L2/front-matter, L3 all OK, exit 0 (read bare, not through a pipe), 3 records = 2 retained + 1 archived, 0 added
  by the trim commit.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-21-2.md` (1 record(s), 28,033 B → 16,745 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-21 → 2026-09-21) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-21-2.md`](docs/archive/HANDOFFS-through-2026-09-21-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-21-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-21-2.md.verify.sh)
rather than trusting a digest printed here. Live file 28,033 B → 16,745 B (−40.3%).

### 2026-09-21 · [BL-75] S213 claim — P2b of the `context_budget.py` plan: D6, the argument messages and `--check` (in progress)

**Deliverable:** P2b of [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md)
§5 (`:513`), on the **local** branch `fix/context-budget-status` from `d4dbc26`, built in a `--no-local` clone and
fetched back as a fast-forward. `--check` becomes a second name for `--status`; every other refused argument's line
names what the user most likely meant (D6's table, `:282`). Seven tests written to fail first against blob
`dd4803bf`, five mutants run. **Nothing pushed, nothing upstream-facing.** Chosen at this session's Phase 0 picker
over BL-78's closing edits.

**Side actions approved at the same picker, each its own commit or record:** the `HANDOFFS.md` retention trim this
claim makes owed (three receipts, `--cut 2 --force`) and its fold; pushing fork `main` to `origin` at close-out.

**Phase 0, for the record:** `CHANGELOG.md` frontier = HEAD `00b8685`, gap empty; `HANDOFFS.md` frontier `b3b1f3a`,
the one commit after it (`00b8685`) is S212's announced push record. No pending stub, 2 receipts before this one;
nothing backfilled. Gate citation re-run in a `--no-local` clone at `00b8685`: `11/11 pass · results 10575dac7361 ·
manifest 01a4ae7aa511`, S212's citation exactly. Dashboard 76/100, medium, 0 high+, run in that clone (so no
`dashboard_history.jsonl` row here). Upstream 0 open issues; #83 (`219fb9d`), #84 (`77afc12`), #85 (`e2501c5`) open,
0 reviews, only our comments. `main` = `origin/main` = `00b8685`; `upstream/main` still `6b29d3d`;
`fix/context-budget-status` = `d4dbc26`.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] S212 — fork `main` pushed to `origin`, `304084d..b3b1f3a` (non-commit action, operator go-ahead)

Six commits, this session's claim through its close-out. Fork remote only — **nothing upstream-facing**, and the
local branch `fix/context-budget-status` (`d4dbc26`) was **not** pushed (P4's go-ahead). Approved at this session's
Phase 0 picker. Checked before: tree clean, `origin/main` = `304084d`, a fast-forward. Read back after: `git
ls-remote origin refs/heads/main` = `b3b1f3a`, equal to local `main`; no `fix/context-budget-status` on `origin`.
This record is pushed after it under the standing push-record grant.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-75] S212 close-out — P3 of the `context_budget.py` plan done on `d4dbc26` and amended by the operator's review (D6, D7); nothing upstream-facing

**Deliverable:** P3 of [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md)
(vet and package).
- **Vetting:** the branch was measured, upstream's floors tightened (`d4dbc26`, local branch, not pushed), and trial
  merges against #83, #84 and #85 run through the ratchet on each merge result, all green.
- **Packaging:** the PR body was drafted and frozen (`e4ad63d`). **The operator's review did not approve it and
  amended the design:** D6 (refused arguments' messages answer the intent; `--check` = `--status`) and D7 (status
  precedence), both in the same PR. `b6814a2` writes them into the plan as P2b, P2c and P3′.
- **Next: P2b.** Supporting commits: `3268e87` claim, `d899bd0` + `351c847` the `HANDOFFS.md` trim and fold.
- **The plan was input, not output;** D6 and D7 are the operator's decisions on options this session developed.
  This commit also fixes an unbalanced `**` that `b6814a2` introduced in BL-80's index row (`docs/planning/BACKLOG.md:168`).

**Phase 3A — S211's handoff scored 9/10.**
- *What helped:*
  - Next step (1) was an exact recipe, and every value in it was right: the clone command, HEAD `c299c30`, the
    measured 141/129, `.quality-gates.json:10`/`:34`, `CHANGELOG.md:38`, and the PR-ref refspec.
  - Gotcha (3) (take the floors from the measured table) was followed.
  - Gotcha (6) (the ranking comment against `render()`'s `order`) became D7's evidence.
  - Gotcha (9) (the trim's notice set varies) was borne out: CUT_STRADDLES_DAY came back.
  - Steps (3)–(5) were right: the PR state on all three, three receipts a twelfth time, and the `CHANGELOG.md`
    estimate (~115 KB; 113,139 B measured).
- *What was missing:* nothing S211 could have computed. Its recommendation (list the edge, don't fix it) was a
  recommendation, and the operator chose otherwise. The refusal-only argument design the operator objected to is the
  plan's (S209), not the handoff's.
- *What was wrong:* nothing found.
- *ROI:* clearly positive.

**Phase 3B — self-assessment 7/10.**
- *Right:*
  - Phase 0 in full, with the gate citation re-run.
  - The trim verified in a clone, and the suite run after the fold.
  - Measured before tightening; `merge-tree` first, then real merges with the ratchet on each merge result, run
    serially.
  - The union resolution sanity-checked (entry counts; the tree equal to `merge-tree`'s).
  - Every figure in the body measured this session; one wrong cell found by running it.
  - When asked for fixes: an inventory, sibling meanings and a measured `difflib` cutoff, not opinions.
  - The design change planned as three sessions, not built inside P3.
- *Wrong:*
  - **The drafted body named problems without fixes.** The operator had to ask for solutions derived from the
    arguments' purposes, which is work the plan and this session should have offered unprompted.
  - **The approval picker named a file path instead of showing the text**, and the operator had to ask where to read
    it.
  - Two zsh traps my memory warns about (`$n:refs`, an unquoted `======`), one exit code read through a pipe (caught
    and re-run), and an unbalanced `**` in a backlog row (caught before close-out).
  - Two stakeholder corrections.

**Phase 3C:** no `docs/FORK_LEARNINGS.md` row, so D3's retirement obligation does not arise. Both lessons are about
this agent's conduct, and they went to agent memory: *a refusal is not a fix* (a second instance on the
sibling-flag entry) and *show the text before asking for its review* (new).

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-75] S212 — the operator's review of the P3 body: two changes added to the PR (D6, D7); the plan amended with P2b, P2c and P3′

- **The decision (non-commit action, the operator's):** the frozen body (`e4ad63d`) was **not approved**, because it
  named problems without fixes: for three of the four ignored arguments people typed, the only remedy was exit 3 and
  the usage text. Asked for fixes derived from what those arguments were meant to do, the session inventoried every
  flag typed after the tool's name in fork `main`, `upstream/main` and seven adopter clones. Only `--status` and
  `--check` are undefined arguments anyone typed; the three `-v` hits are `test_context_budget.py -v`. It then read
  each flag's meaning in the sibling tools' `--help` and ran `difflib` at two cutoffs over 20 inputs. At the picker
  the operator chose, each as recommended:
  - **D6, "answer the intent":** `--check` is accepted as a second name for `--status`, which is
    `methodology_trim.py --check`'s meaning. Every other refused argument keeps exit 3, with a message naming what
    the user most likely meant: `--force` → raise the ceiling in `.context-budget.json`; `--dry-run` → `--status`;
    `--run`/`--write` → no argument; a misspelling → the nearest match at cutoff 0.75, where the default 0.6 offers
    `--json` for `--version`.
  - **D7, "fix it in this PR":** the status-precedence edge. In `measure_file()` a check may raise a status but
    never lower it. Of the status writes, only `:427` can lower one, so the fix is one guard there.
- **What (`docs/planning/context-budget-status-plan.md`):** the status line; D6 and D7 in §3 with their evidence;
  §4.1's table (a `--check` row, the hint on refusal); the *P3 outcome* block, with the line numbers on `d4dbc26` for
  the next two phases; **three new phases**, P2b (D6), P2c (D7) and P3′ (re-vet, and the body rewritten from the
  frozen draft rather than patched), each with its files, guards, tests RED first, mutants, DONE, verification and
  surface; §6's `wsfct` row, since under D6 its `--check` works. **The draft body** gains a *superseded — do not
  post* notice above its rule. **Backlog:** S212 paragraphs on BL-75 and BL-80 (nothing above them edited) and both
  index rows. `BACKLOG-DETAIL.md.verify.sh` C1–C5 OK, exit 0; `bin/check-links` exit 0.
- **Gotcha carried into P2b:** the hint table names `--force`, so it must sit below `def selftest`. It must be read
  by key, never by `"--force" in args`, which `bin/tests.sh:622` and `tools/test_context_budget.py:487` grep for.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-75] S212 — P3: the PR body drafted and frozen for the operator's review (not posted)

- **What:** [`docs/planning/context-budget-status-pr-body.md`](docs/planning/context-budget-status-pr-body.md), new,
  fork-only: a header (fork notes, **not posted**) and the title and body as they would be posted, 10.8 KB. It opens on
  the two defects, answers the maintainer's point 6 on #82 by link (comment `5701463025`, verified by `gh api`: author
  `KJ5HST`, the quoted sentence at its line 17), and states what it does not change, the status-precedence edge
  included, pending the operator's decision. **Every figure in it was measured this session**, none carried from the
  plan: the 12 upstream citations (`git grep` on `6b29d3d`: 5 `CHANGELOG.md`, 7 `HANDOFFS.md`); #84's body citation
  (`gh pr view`, line 143); the before/after table (each command run in a clean clone of `6b29d3d` and of `d4dbc26`);
  the one adopter with a live `--check` instruction (seven local adopter clones grepped at their current heads); the
  ranking-comment contradiction (`:1417-1419` against `render()`'s `order`). A first draft said `--status --json` on
  `main` was *"same as bare"*; run, it is the `--json` run and writes, and the cell was corrected before freezing.
  **Jargon scan of the outward text** (session numbers, backlog codes, plan decision and phase codes, *fork*,
  *operator*, *plan*): 0 hits. `bin/check-links` OK.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-75] S212 — P3: upstream's two floors tightened, `d4dbc26` on the LOCAL branch `fix/context-budget-status` (commit + fast-forward; not pushed); trial merges against #83, #84, #85 all green

- **Measured first**, in a fresh `--no-local` clone of the branch at `c299c30`, HEAD asserted: upstream's ratchet
  `10/10 pass · results 43e25ddcd120 · manifest 97a7aab85b9a`, S211's figure exactly. Only the two gates this PR moves
  had risen: `tests-sh-passed` 141 (floor 139), `context-budget-unit-tests` 129 (floor 118); every other gate
  measured exactly its threshold.
- **The commit:** `d4dbc26`, `.quality-gates.json:10` 139 → 141 and `:34` 118 → 129, plus one upstream-format
  `CHANGELOG.md` entry (`[ad hoc]`, jargon scan 0 hits), built in that clone with `core.hooksPath` set, then fetched
  back here as a fast-forward `c299c30..d4dbc26`, still with no remote tracking.
- **Overlap, computed:** `git merge-tree --write-tree --name-only` from `d4dbc26`: #84 (`77afc12`) clean,
  `CHANGELOG.md` included; #85 (`e2501c5`) and #83 (`219fb9d`) conflict in `CHANGELOG.md` only, and
  `.quality-gates.json` auto-merges with #85's new gate. **Then each merged for real** in its own scratch clone,
  `CHANGELOG.md` resolved by `git merge-file --union` with a marker grep before `git add`, entry counts checked
  (59 = 58 + 56 − 55 on both), and #84's merge tree equal to `merge-tree`'s (`7c0fae9`). **The ratchet on each merge
  result, serially:** #84 `10/10 · results 03f9f21f348d · manifest ba1ef0894ed2` (`bin/tests.sh` 165 / 0, budget
  units 133); #85 `11/11 · results 2bfa474023b7 · manifest 39ec63ebe022` (its `pre-commit-selftest` included, 141 /
  0); #83 `10/10 · results 02f2b08c7697 · manifest ba1ef0894ed2` (141 / 0).
- **Verified in a fresh `--no-local` clone at `d4dbc26`, HEAD asserted:** `--selftest` 52 PASS, exit 0; the
  `"--force" in args` grep empty; upstream's ratchet `10/10 pass · results 02f2b08c7697 · manifest ba1ef0894ed2`,
  with the new floors met exactly (141, 129). **Nothing upstream-facing:** pushing the branch and opening the PR are
  P4's go-ahead.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] S212 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

- **What:** the trimmer's 3-line pointer block for `docs/archive/HANDOFFS-through-2026-09-21.md` became one row at
  the bottom of [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md) and was deleted from the ledger's
  front matter. `HANDOFFS.md` 17,369 B → 16,921 B.
- **Its own commit by design:** inside the trim commit the shipped `.verify.sh` fails L2 (fork Learning #58). The
  verifier was run against the trim commit `d899bd0`, in a `--no-local` clone, **before** the fold — L1,
  L2/front-matter, L3 all OK, exit 0 (read bare, not through a pipe), 3 records = 2 retained + 1 archived, 0 added
  by the trim commit.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-21.md` (1 record(s), 27,240 B → 17,369 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-21 → 2026-09-21) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-21.md`](docs/archive/HANDOFFS-through-2026-09-21.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-21.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-21.md.verify.sh)
rather than trusting a digest printed here. Live file 27,240 B → 17,369 B (−36.2%).

### 2026-09-21 · [BL-75] S212 claim — P3 of the `context_budget.py` plan: vet and package (in progress)

**Deliverable:** P3 of [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md)
§5 (`:407`). Measure the branch tip `c299c30` in a fresh clone; tighten upstream's two floors (D5) in their own
commit on the **local** branch `fix/context-budget-status`; trial-merge the branch against #83, #84 and #85 and run
the suites on each clean merge result; draft the PR body to `docs/planning/context-budget-status-pr-body.md`. It
ends on the operator's review of that body and the status-precedence decision (plan `:388`). **Nothing pushed,
nothing upstream-facing**: pushing the branch and opening the PR are P4's go-ahead. Chosen at this session's Phase 0
picker over BL-78's closing edits and the undecided items.

**Side actions approved at the same picker, each its own commit or record:** the `HANDOFFS.md` retention trim this
claim makes owed (three receipts, `--cut 2 --force`) and its fold; pushing fork `main` to `origin` at close-out.

**Phase 0, for the record:** `CHANGELOG.md` frontier = HEAD `304084d`, gap empty; `HANDOFFS.md` frontier `68fd86d`,
the one commit after it (`304084d`) is S211's announced push record. No pending stub, 2 receipts before this one;
nothing backfilled. Gate citation re-run in a `--no-local` clone with HEAD asserted by sha: `11/11 pass · results
10575dac7361 · manifest 01a4ae7aa511`, S211's citation exactly. Dashboard 76/100, medium, 0 high+. Upstream 0 open
issues; #83 (`219fb9d`), #84 (`77afc12`), #85 (`e2501c5`) open, 0 reviews, only our comments. `main` =
`origin/main` = `304084d`; `upstream/main` still `6b29d3d`; `fix/context-budget-status` = `c299c30`.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] S211 — fork `main` pushed to `origin`, `36044bb..68fd86d` (non-commit action, operator go-ahead)

Five commits, this session's claim through its close-out. Fork remote only — **nothing upstream-facing**, and the
local branch `fix/context-budget-status` was **not** pushed (P4's go-ahead). Approved at this session's Phase 0
picker. Checked before: tree clean, `origin/main` = `36044bb`, a fast-forward. Read back after: `git ls-remote origin
refs/heads/main` = `68fd86d`, equal to local `main`; no `fix/context-budget-status` on `origin`. This record is pushed
after it under the standing push-record grant.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-80] S211 close-out — P2 of the `context_budget.py` plan built and verified on the local branch; nothing upstream-facing

**Deliverable:** P2 of [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md),
one commit, `c299c30`, on the **local** branch `fix/context-budget-status` after P1's `e859196` (not pushed). The
growth-run advisory's second sentence is now chosen by `worst`, so it no longer says nothing is over a ceiling beside
rows marked over. It is verified in a fresh clone: 129 unit tests, `bin/tests.sh` 141 / 0, upstream's ratchet
10/10. **Next: P3**, which also owes the operator one decision on the status-precedence edge found here (plan
`:388`). Supporting commits: `520f972` claim, `03194df` + `4542465` the `HANDOFFS.md` trim and fold, and `8a0455c`
the plan's P2 outcome and the backlog. **The plan was input, not output.**

**Phase 3A — S210's handoff scored 9/10.**
- *What helped:*
  - Next step (1) was an exact recipe: clone from the local branch, assert `e859196`, set `core.hooksPath`. Every line
    it cited on the branch was right: the advisory `:661-663`, `worst` `:594-605`, the insertion point `:615`/`:618`,
    the witness `:1063`, and `CHANGELOG.md:38`.
  - Gotcha (3), *run the fixed baseline through the mutant harness first*, was followed and showed a clean baseline.
  - Gotcha (1) said where the branch lives, which the S209 handoff had been missing.
  - Steps (3)–(5) were right: the PR state on all three, the three-receipts prediction (an eleventh time), and the
    `CHANGELOG.md` figure (102,035 B plus the push record read 102,737 B).
- *What was wrong:* *"`bin/tests.sh` 141 + k"* assumed the shell count moves with the unit tests. The unit suite is
  one row there, so P2 gave unit +3 and shell +0. The error was computable, and minor.
- *What was missing:* nothing S210 could have known. The edge sits in `measure_file()`, which neither the plan nor
  P1 read.
- *ROI:* clearly positive.

**Phase 3B — self-assessment 8/10.**
- *Right:*
  - Phase 0 in full, with the gate citation re-run.
  - Read the producers (`measure_file()`'s status writes), not only the reducer. That found the edge, and it was run
    on the fixed tool rather than predicted.
  - RED with fixture proofs in every cell; the failures landed at the assertion under test.
  - The baseline was run through the mutant harness before the four mutants.
  - The ratified contract was kept rather than widened. The edge is recorded for P3 and named in the upstream entry.
  - Final verification from a fresh clone of the fetched-back branch; the outward entry scanned for jargon.
  - Zero stakeholder corrections.
- *Wrong:*
  - My first mutant table garbled its per-test verdicts under subtests and had to be re-run test by test.
  - A test docstring claimed the original sentence is *"true of the table"* under `instrument-failed`. It was
    written before the edge was run and corrected before commit.
  - One plan citation came from diff arithmetic (`:1418`); a grep before commit corrected it to `:1417`.
  - One pointless no-op monitor call.

**Phase 3C:** no `docs/FORK_LEARNINGS.md` row. The lesson is code-specific, and its defect is P3's decision. It
went to agent memory as a second instance of an existing entry. D3's retirement obligation does not arise.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-80] S211 — the plan's P2 outcome recorded; BL-75 and BL-80 index rows and BL-80's detail updated

- **What:** [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md): status line
  (P2 done, P3 next) and a *P2 outcome* block under §5 P2. It records the verification, the RED record, the mutants,
  one extension (the matrix covers `instrument-failed` too), the status-precedence edge found and not fixed, and
  P3's line numbers on the branch. `docs/planning/BACKLOG-DETAIL.md` BL-80 gains an S211 paragraph (nothing above
  it edited). The BL-75 and BL-80 index rows in `docs/planning/BACKLOG.md` now say P2 is done. Both items stay open
  until the PR merges. `BACKLOG-DETAIL.md.verify.sh` C1–C5 OK, exit 0.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-80] S211 — P2 built: `c299c30` on the LOCAL branch `fix/context-budget-status` (commit + fast-forward; not pushed)

- **What:** one commit, `c299c30`, after P1's `e859196`, built in a `--no-local` clone of the local branch with
  `core.hooksPath` set, then fetched back here as a fast-forward (`e859196..c299c30`), still with no remote tracking.
  The growth-run advisory's second sentence is chosen by `worst`, the headline's variable. When nothing is over it is
  unchanged. When something is, it reads *"A ceiling has fired as well — see the rows marked over."* The commit adds
  3 tests (`TestGrowthRunAdvisory`) and one upstream-format `CHANGELOG.md` entry (`[ad hoc]`, scanned for fork
  jargon: 0 hits). Tool blob `131158cb` → `dd4803bf`.
- **RED first on `131158cb`:** 2 of 3 tests fail, each at the assertion under test (only the `over` × run-hit cell
  of the matrix); the third is the presence control and passes by design. **Mutants, run after the fixed tool
  passed the same harness:** literal restored (tests 1 and 3), sentence deleted (all three), condition inverted
  (all three), condition widened to `instrument-failed` (test 2). All killed; `--selftest` catches none.
- **Found while building, NOT fixed:** a row over its byte ceiling that also fails a structure pattern reads
  `instrument-failed` (`measure_file()`'s last writer wins, `:366` then `:427`). Run on the fixed tool, the advisory
  keeps *"Nothing is over a ceiling yet"* above *"1,500 B exceeds the 1,000 B ceiling by 500"*. It is outside D3 and
  is recorded for P3. The upstream entry names it under *"Not changed here"*.
- **Verified in a fresh `--no-local` clone at `c299c30`, HEAD asserted:** 129 unit tests OK; `--selftest` 52 PASS,
  exit 0; the `"--force" in args` grep empty; `bin/tests.sh` **141 passed, 0 failed**; upstream's ratchet `10/10
  pass · results 43e25ddcd120 · manifest 97a7aab85b9a`. The tool was also run on an over and a not-over project with
  the run fired. **Nothing upstream-facing:** pushing the branch and opening the PR are P4's go-ahead.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] S211 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

- **What:** the trimmer's 3-line pointer block for `docs/archive/HANDOFFS-through-2026-09-20-12.md` became one row at
  the bottom of [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md) and was deleted from the ledger's
  front matter. `HANDOFFS.md` 15,895 B → 15,435 B.
- **Its own commit by design:** inside the trim commit the shipped `.verify.sh` fails L2 (fork Learning #58). The
  verifier was run against the trim commit `03194df`, in a `--no-local` clone, **before** the fold — L1,
  L2/front-matter, L3 all OK, exit 0 (read bare, not through a pipe), 3 records = 2 retained + 1 archived, 0 added
  by the trim commit.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-20-12.md` (1 record(s), 25,742 B → 15,895 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-20 → 2026-09-20) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-20-12.md`](docs/archive/HANDOFFS-through-2026-09-20-12.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-20-12.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-20-12.md.verify.sh)
rather than trusting a digest printed here. Live file 25,742 B → 15,895 B (−38.3%).

### 2026-09-21 · [BL-80] S211 claim — P2 of the `context_budget.py` plan: the growth-run advisory agrees with its table (in progress)

**Deliverable:** P2 of [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md)
§5, decision D3: the advisory's second sentence is chosen by `worst`, the variable the headline already reads, so
a run whose table shows a row `over` no longer prints *"Nothing is over a ceiling yet"*. Three tests written RED
first against `e859196`, and the "restore the literal" mutant run. One commit on the **local** branch
`fix/context-budget-status`, built in a `--no-local` clone of that branch and fetched back here. **Nothing pushed,
nothing upstream-facing**: pushing the branch and opening the PR are P4's go-ahead. Chosen at this session's Phase 0
picker over BL-78's closing edits.

**Side actions approved at the same picker, each its own commit or record:** the `HANDOFFS.md` retention trim this
claim makes owed (three receipts, `--cut 2 --force`) and its fold; pushing fork `main` to `origin` at close-out.

**Phase 0, for the record:** `CHANGELOG.md` frontier = HEAD `36044bb`, gap empty; `HANDOFFS.md` frontier `1e1cd18`,
the one commit after it (`36044bb`) is S210's announced push record. No pending stub, 2 receipts before this one;
nothing backfilled. Gate citation re-run in a `--no-local` clone with HEAD asserted by sha: `11/11 pass · results
10575dac7361 · manifest 01a4ae7aa511`, S210's citation exactly. Dashboard 76/100, medium, 0 high+. Upstream 0 open
issues; #83 (`219fb9d`), #84 (`77afc12`), #85 (`e2501c5`) open, 0 reviews, no maintainer comment. `main` =
`origin/main` = `36044bb`; `upstream/main` still `6b29d3d`; `fix/context-budget-status` = `e859196`.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] S210 — fork `main` pushed to `origin`, `cadd8a0..1e1cd18` (non-commit action, operator go-ahead)

Five commits, this session's claim through its close-out. Fork remote only — **nothing upstream-facing**, and the
local branch `fix/context-budget-status` was **not** pushed (P4's go-ahead). Approved at this session's Phase 0
picker. Checked before: tree clean, `origin/main` = `cadd8a0`, a fast-forward. Read back after: `git ls-remote origin
refs/heads/main` = `1e1cd18`, equal to local `main`, ahead/behind 0/0; no `fix/context-budget-status` on `origin`. This
record is pushed after it under the standing push-record grant.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-75] S210 close-out — P1 of the `context_budget.py` plan built and verified on a local branch; nothing upstream-facing

**Deliverable:** P1 of [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md),
one commit, `e859196`, on the **local** branch `fix/context-budget-status` (from `upstream/main` `6b29d3d`, not pushed):
a write-free `--status`, unknown arguments refused with exit 3, and `VERSION` 1.3.0. It is verified in a fresh clone:
126 unit tests, `bin/tests.sh` 141 / 0, upstream's ratchet 10/10. **Next: P2.** Supporting commits: `e4d7c84` claim,
`19d9e42` + `f1fa0a4` the `HANDOFFS.md` trim and fold, and `c8e5cae` the plan's P1 outcome and the backlog. **The plan
was input, not output**, and its P1 text was departed from in three recorded ways (see the P1 entry below).

**Phase 3A — S209's handoff scored 8/10.**
- *What helped:*
  - Next step (1) was an exact recipe: re-check the branch base, use a `--no-local` clone, set `core.hooksPath`
    before the first commit, go RED against `b1111d92`. Every code line it cited was right in the blob.
  - Gotcha (1), *run `--status` FIRST*, became test 1's ordering.
  - Gotcha (3), the dashboard fingerprint, kept the docstring and constants untouched.
  - Step (3)'s PR state was right on all three. Step (4)'s three-receipts prediction held a tenth time, and step
    (5)'s `CHANGELOG.md` estimate (about 92 KB) read 92,462 B.
- *What was wrong:* the plan's P1 said a `--force` added to the accepted list *"must be caught by the three
  existing guards"*, and §4.1 put that list *"in `main()`"*. `main()` is below `def selftest`, so none of the three
  could see it. This was computable at planning time, not a prediction. Trusted, it would have left one test
  standing where four guards were believed to stand. Gotcha (2)'s *"guarded three times"* carried the same
  overstatement.
- *What was missing:* where the branch lives between sessions. P1–P3 span sessions, and a scratch clone does not
  survive one. This session fetched it back as a local branch.
- *ROI:* clearly positive.

**Phase 3B — self-assessment 8/10.**
- *Right:*
  - Phase 0 in full, with the gate citation re-run.
  - RED recorded for both unit and shell before the fix.
  - Mutants run rather than predicted, which found both the plan's false guard claim and my own defect.
  - The fixed baseline run through the same harness, which exposed a false-premise test.
  - The outward entry scanned for fork jargon.
  - Final verification from a fresh clone of the fetched-back branch, not the working clone.
  - Zero stakeholder corrections.
- *Wrong:*
  - I introduced the defect mutant 3 found: a comment naming `def selftest` above the list narrowed the selftest's
    check to lines 1–55.
  - My first pinning test asserted `count == 1`, which is false on the fixed tool, and the first mutant table I
    printed carried spurious kills.
  - Two receipt citations were written from memory (`:1302`, `:675-697`). A re-check before commit corrected them
    to `:1293` and `:675-696`.
  - The three departures from the plan were decided in-session, not put to the operator first. They are recorded in
    the plan with reasons.

**Phase 3C:** no `docs/FORK_LEARNINGS.md` row. The lesson is enforced by the eighth test, so it is a gate and not a
row; the rest went to agent memory. D3's retirement obligation does not arise.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-75] S210 — the plan's P1 outcome recorded; BL-75 and BL-80 index rows and BL-75's detail updated

- **What:** [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md): status line
  (P1 done, P2 next), §4.1's contract sentence (the accepted list is module-level, not in `main()`), and a *P1
  outcome* block under §5 P1 recording the verification, the RED record, three departures from the plan's text,
  and P2's line numbers on the branch. `docs/planning/BACKLOG-DETAIL.md` BL-75 gains an S210 paragraph (nothing above
  it edited); the BL-75 and BL-80 index rows in `docs/planning/BACKLOG.md` now say P1 is done. BL-75 stays open
  until the PR merges. `BACKLOG-DETAIL.md.verify.sh` C1–C5 OK, exit 0.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-75] S210 — P1 built: `e859196` on the LOCAL branch `fix/context-budget-status` (branch op + commit; not pushed)

- **What:** the local branch `fix/context-budget-status` was created, cut from `upstream/main` `6b29d3d` and
  fetched back from a `--no-local` scratch clone, with no remote tracking. It holds one commit, `e859196`: `--status`
  becomes the default run without its history append, an argument outside `ACCEPTED_ARGUMENTS` exits 3 before
  the tree is read (`-h`/`--help` still win), and `VERSION` goes 1.2.0 → 1.3.0. The commit adds 8 tests
  (`TestCommandLine`), 2 `bin/tests.sh` rows and one upstream-format `CHANGELOG.md` entry (`[ad hoc]`, no fork
  jargon). Tool blob `b1111d92` → `131158cb`.
- **RED first on `b1111d92`:** 6 of 8 tests fail, and 2 are controls that pass by design. The suite gave 138
  passed, 3 failed: both new rows, plus the unit-test row. **Mutants, run:** unconditional append, rejection
  removed, `--force` accepted, and a comment moving the selftest check's split point plus `--force`. All four
  were killed. Neither `"--force" in args` grep catches either `--force` mutant.
- **Found while building:** the plan's claim that the three existing guards catch `--force` in the list was
  false for a list in `main()` (below `def selftest`). A comment written above the new list first named the
  selftest's definition, which narrowed the selftest's check to lines 1–55. It was caught by running mutant 3,
  fixed, and pinned by the eighth test.
- **Verified in a fresh `--no-local` clone at `e859196`, HEAD asserted:** 126 unit tests OK; `--selftest` 52 PASS,
  exit 0; `bin/tests.sh` **141 passed, 0 failed**; upstream's ratchet `10/10 pass · results 37bbefc55e64 · manifest
  97a7aab85b9a`. **Nothing upstream-facing:** pushing the branch and opening the PR are P4's go-ahead.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] S210 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

- **What:** the trimmer's 3-line pointer block for `docs/archive/HANDOFFS-through-2026-09-20-11.md` became one row at
  the bottom of [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md) and was deleted from the ledger's
  front matter. `HANDOFFS.md` 15,859 B → 15,399 B.
- **Its own commit by design:** inside the trim commit the shipped `.verify.sh` fails L2 (fork Learning #58). The
  verifier was run against the trim commit `19d9e42`, in a `--no-local` clone, **before** the fold — L1,
  L2/front-matter, L3 all OK, exit 0, 3 records = 2 retained + 1 archived, 0 added by the trim commit.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-20-11.md` (1 record(s), 24,049 B → 15,859 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-20 → 2026-09-20) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-20-11.md`](docs/archive/HANDOFFS-through-2026-09-20-11.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-20-11.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-20-11.md.verify.sh)
rather than trusting a digest printed here. Live file 24,049 B → 15,859 B (−34.1%).

### 2026-09-21 · [BL-75] S210 claim — P1 of the `context_budget.py` plan: a write-free `--status`, unknown arguments refused (in progress)

**Deliverable:** P1 of [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md)
§5, decisions D1 + D2 + D4: `--status` becomes the default measurement with no history append, an unrecognised
argument exits 3 with usage and touches nothing, and `VERSION` goes 1.2.0 → 1.3.0. Seven tests written RED first
against the unchanged blob `b1111d92`, two `bin/tests.sh` rows, three named mutants run. Built on a branch
`fix/context-budget-status` cut from `upstream/main` `6b29d3d` in a `--no-local` clone, then fetched back into this
repository as a **local** branch so it outlives the scratch clone. **Nothing pushed, nothing upstream-facing**:
pushing the branch and opening the PR are P4's go-ahead. Chosen at this session's Phase 0 picker over BL-78's
closing edits.

**Side actions approved at the same picker, each its own commit or record:** the `HANDOFFS.md` retention trim this
claim makes owed (three receipts, `--cut 2 --force`) and its fold; pushing fork `main` to `origin` at close-out.

**Phase 0, for the record:** `CHANGELOG.md` frontier = HEAD `cadd8a0`, gap empty; `HANDOFFS.md` frontier `e1795a0`,
the one commit after it (`cadd8a0`) is S209's announced push record. No pending stub, 2 receipts before this one;
nothing backfilled. Gate citation re-run in a `--no-local` clone with HEAD asserted by sha: `11/11 pass · results
10575dac7361 · manifest 01a4ae7aa511`, S209's citation exactly. Dashboard 76/100, medium, 0 high+. Upstream 0 open
issues; #83 (`219fb9d`), #84 (`77afc12`), #85 (`e2501c5`) open, 0 reviews, no maintainer comment. `main` =
`origin/main` = `cadd8a0`; `upstream/main` still `6b29d3d`.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [ad hoc] S209 — fork `main` pushed to `origin`, `73b9536..e1795a0` (non-commit action, operator go-ahead)

Seven commits, this session's claim through its close-out. Fork remote only — **nothing upstream-facing.**
Approved at this session's Phase 0 picker. Checked before: tree clean, `origin/main` = `73b9536`, a fast-forward.
Read back after: `git ls-remote origin refs/heads/main` = `e1795a0`, equal to local `main`, ahead/behind 0/0. This
record is pushed after it under the standing push-record grant.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-75] S209 close-out — one upstream PR for `context_budget.py` planned and ratified; nothing built

**Deliverable:** [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md), the plan for
**one** upstream PR fixing BL-75 and BL-80 in the distributed `starter-kit/context_budget.py`. The operator decided all
five decisions at this session's picker, each as recommended (`a39cf1c`):
- a write-free `--status`;
- unknown arguments refused with exit 3;
- the advisory chosen by `worst`;
- `VERSION` 1.3.0;
- upstream's floors tightened in the PR.

Five phases, one session each. **Next: P1.** Supporting commits: `366dfc4` claim, `adb9d8f` + `d473719` the
`HANDOFFS.md` trim and fold, `84c75e0` the PR #83 review's §4.2 fix, `87857ba` the draft. **Plan was output, not
input.** Close-out also names the tree beside the plan's `wsfct` citations: a parallel `wsfct` session committed
`ef3eade3` mid-session and moved the cited line.

**Phase 3A — S208's handoff scored 9/10.**
- *What helped:*
  - Next step (1)'s exact PR-check commands and expected state were right on all three PRs, so "nothing owed
    upstream" was a two-minute confirmation.
  - Step (2) named the third false claim with both line citations, and both held (`pr83-decisions-review.md:194`,
    `HANDOFFS-through-2026-08-29.md:285`), which made the fix a single approved sentence.
  - Step (4)'s three-receipts prediction held a ninth time.
  - `key_files` located BL-78's owed edits exactly (`BACKLOG.md:166`; `.context-budget.json:101` is `files[4]._`).
- *What was wrong:* step (5)'s "about 77 KB after this close-out" read 81,106 B at Phase 0. It was labelled an
  estimate.
- *What was missing:* nothing for this session's task; BL-75's and BL-80's detail blocks carried what it needed.
- *ROI:* clearly positive.

**Phase 3B — self-assessment 8/10.**
- *Right:*
  - Read the implementation before shaping anything.
  - Tested the premise on a throwaway patch before offering the options, so the picker offered measured
    behaviour, not predictions.
  - Found the three facts that reshaped the design:
    - the sibling tool's read-only `--status`;
    - the maintainer's own #82 objection, verified on GitHub rather than trusted from the fork copy;
    - `wsfct`'s second phantom flag.
  - Counted citations across fork, upstream, adopters and posted PR bodies.
  - Froze the draft before the decisions picker, and kept every suite run in clones.
  - Zero stakeholder corrections.
- *Wrong:*
  - The first draft carried four citation errors, caught by re-verification before commit: a test line; the
    `.gitignore` claim; #84's hunk ranges, taken from the PR side; and "documented only in `print_usage`".
  - An archive count was stated in lines, where the rest of the inventory counts occurrences.
  - The receipt was first written with multi-line fields, which `bin/check-handoff` refused.
  - The zsh `"$r:path"` trap recurred.
  - The plan is long, 425 lines. Its §0 summary is what makes it usable.

**Phase 3C:** no fork-learnings row, so D3's retirement obligation does not arise. The lesson (a cited-but-missing
flag usually comes from a sibling tool, so match the sibling's meaning) went to agent memory. **Phase 3E:**
`quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results 10575dac7361 · manifest 01a4ae7aa511`, in a clone of
`a39cf1c`.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-21 · [BL-75] S209 — the plan's five decisions taken by the operator; the plan is RATIFIED

- **Decided at S209's decision picker, each as recommended:** D1 (b) a **write-free `--status`**; D2 (a) **unknown
  arguments refused, exit 3**; D3 (a) the advisory's second sentence **chosen by the headline's `worst`**; D4
  `VERSION` **1.3.0**; D5 upstream's `context-budget-unit-tests` and `tests-sh-passed` floors **tightened in the
  PR**. Recorded in [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md)
  (status line and §3), and as dated S209 updates under BL-75 and BL-80 in `docs/planning/BACKLOG-DETAIL.md` and
  their index rows in `docs/planning/BACKLOG.md`. Both items stay **open** until the fix lands (the plan's P5).
  `BACKLOG-DETAIL.md.verify.sh` C1–C5 OK, exit 0.
- **Next:** the plan's P1 (BL-75, the CLI), one session, on a branch cut from `upstream/main`.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [BL-75] S209 — plan drafted: one upstream PR for `context_budget.py`'s `--status` and advisory (decisions pending)

- **What:** [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md), frozen as
  a draft before its five decisions go to the operator. Recommends a **write-free `--status`** (D1 b), **refusing
  unknown arguments with exit 3** (D2 a), and **choosing the growth-run advisory's second sentence by the
  headline's own `worst`** (D3 a), with `VERSION` 1.3.0 (D4) and upstream's two floors tightened in the PR (D5).
  Five phases, one session each; P4 (open the PR) is outward and its own go-ahead.
- **Evidence gathered:** the tool is one blob (`b1111d92`) on fork `main`, `upstream/main` and all three open PR
  heads. `context_budget.py --status` is cited 122 times here (34 live, 88 archived), 12 times in upstream's
  ledgers (receipts S19–S23, the maintainer's sessions), once in open PR #84's body, and in the maintainer's
  own PR #82 reply ([#issuecomment-5701463025](https://github.com/KJ5HST/methodology/pull/82#issuecomment-5701463025),
  point 6), which names the history write as what blocks a context-budget gate. `wsfct` cites a second
  non-existent flag, `--check`, including one live instruction (`SESSION_NOTES.md:797`). The sibling
  `quality_ratchet.py` has a real, read-only `--status` (`starter-kit/quality_ratchet.py:543`).
- **Premise tested, not committed:** a throwaway three-edit patch in a scratch clone kept `--selftest` (exit 0),
  the 122 unit tests and the `bin/tests.sh` `--force` source-grep green. `--status` wrote nothing and printed
  output byte-identical to the bare run after it; `--zzz`, `--force` and `--check` exited 3 and wrote nothing.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [ad hoc] S209 — the PR #83 review's third false "agent memory" claim corrected (§4.2)

- **What:** §4.2 of [`docs/planning/pr83-decisions-review.md`](docs/planning/pr83-decisions-review.md) said S115's
  `git status --porcelain` / `--ignored` finding was *"again recorded only in agent memory"*. S115's own receipt
  records it, in its gotchas, at `docs/archive/HANDOFFS-through-2026-08-29.md:285` (*"A GITIGNORED ARTIFACT IS
  INVISIBLE TO `git status --porcelain`"* … *"Use `--ignored` when policing agents"*). The sentence now cites that
  receipt, as S208 did for §4.1 (S44) and §4.7 (S178). Raised by S208's handoff; approved at this session's Phase 0
  picker as its own sentence.
- **Not outward:** §4.2 is not part of §6, so the comment posted to #83 (`#issuecomment-5755256040`) does not
  contain this text and nothing upstream changes. The review's status line (*"byte-identical to §6 at `f7fc621`"*)
  stays true: §6 is untouched. BL-82 stays closed.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [ad hoc] S209 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

- **What:** the trimmer's 3-line pointer block for `docs/archive/HANDOFFS-through-2026-09-20-10.md` became one row at
  the bottom of [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md) and was deleted from the ledger's
  front matter. `HANDOFFS.md` 14,362 B → 13,902 B.
- **Its own commit by design:** inside the trim commit the shipped `.verify.sh` fails L2 (fork Learning #58). The
  verifier was run against the trim commit `adb9d8f`, in a `--no-local` clone, **before** the fold — L1,
  L2/front-matter, L3 all OK, exit 0, 3 records = 2 retained + 1 archived, 0 added by the trim commit.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-20-10.md` (1 record(s), 22,946 B → 14,362 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-20 → 2026-09-20) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-20-10.md`](docs/archive/HANDOFFS-through-2026-09-20-10.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-20-10.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-20-10.md.verify.sh)
rather than trusting a digest printed here. Live file 22,946 B → 14,362 B (−37.4%).

### 2026-09-20 · [BL-75] S209 claim — plan one upstream PR fixing `context_budget.py` (BL-75 + BL-80) (in progress)

**Deliverable:** a plan in `docs/planning/` for **one** upstream-bound pull request fixing two defects in the
distributed `starter-kit/context_budget.py`: BL-75 (no `--status` command exists and an unknown argument is silently
ignored, so every cited *"`--status`"* run was the default measurement — including a gate command proposed to the
maintainer in a PR comment) and BL-80 (*"Nothing is over a ceiling yet"* printed in the same run whose table shows
rows `over`). Planning session: grep inventory of every citation, shapes presented for the operator's choice,
per-phase criteria; **no code, nothing upstream-facing.** Chosen at this session's Phase 0 picker over BL-78's
closing edits, BL-79 and BL-74.

**Side actions approved at the same picker, each its own commit or record:** the `HANDOFFS.md` retention trim this
claim makes owed (three receipts, `--cut 2 --force`); the one-sentence fix of §4.2 of the PR #83 review, whose
*"again recorded only in agent memory"* (`docs/planning/pr83-decisions-review.md:194`) is refuted by S115's receipt
(`docs/archive/HANDOFFS-through-2026-08-29.md:285`) — fork copy only, not in the posted comment; and pushing fork
`main` to `origin` at close-out.

**Phase 0, for the record:** `CHANGELOG.md` frontier = HEAD `73b9536`, gap empty; `HANDOFFS.md` frontier `1c56948`,
the one commit after it (`73b9536`) is S208's announced push record. No pending stub, 2 receipts before this one;
nothing backfilled. Gate citation re-run in a `--no-local` clone with HEAD asserted by sha: `11/11 pass · results
10575dac7361 · manifest 01a4ae7aa511`, S208's citation exactly. Dashboard 76/100, medium, 0 high+. Upstream 0 open
issues; #83 (`219fb9d`), #84 (`77afc12`), #85 (`e2501c5`) open, 0 reviews, no maintainer comment. `main` =
`origin/main`; `upstream/main` still `6b29d3d`.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [ad hoc] S208 — fork `main` pushed to `origin`, `0dcc291..1c56948` (non-commit action, operator go-ahead)

Fourteen commits: S206's post-close-out direction and S207's six, unpushed since S207 had no go-ahead, plus this
session's seven. Fork remote only — **nothing upstream-facing.** Approved at this session's Phase 0 picker. Checked
before: tree clean, `origin/main` = `0dcc291`, a fast-forward. Read back after: `git ls-remote origin refs/heads/main` =
`1c56948`, equal to local `main`, ahead/behind 0/0. This record is pushed after it under the standing push-record grant.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [BL-82] S208 close-out — the review posted to #83, and BL-82 closed

**Deliverable: §6 of [`docs/planning/pr83-decisions-review.md`](docs/planning/pr83-decisions-review.md) posted to
upstream PR #83** as [#issuecomment-5755256040](https://github.com/KJ5HST/methodology/pull/83#issuecomment-5755256040),
the approved text plus one sentence, read back and checked as rendered. BL-82 closed (`18fc1c2`). Supporting commits:
`d43ec14` claim, `c9853b8` + `b613ecc` the `HANDOFFS.md` trim and fold, `b6a7133` the `CHANGELOG.md` trim, `f7fc621`
the final text with §4.1 and §4.7 corrected.

**Phase 3A — S207's handoff scored 8/10.**
- *What helped, concretely:*
  - Next step (2) gave the pre-checks and the exact extraction command
    (`awk '/^> Thanks/,/^> above theirs/' … | sed -E 's/^> ?//'`). It worked verbatim and made the approved-vs-final
    `diff` a one-liner.
  - It named both open considerations for the posting picker instead of deciding them. One of them became the
    picker's second question.
  - Gotcha (1), that the `pr83` ref gets pruned, was true (the ref was gone, the object present). Gotcha (5),
    `--file`, and "a dry run needs `--force`" were used and right. The three-receipts prediction held an eighth time.
- *What was wrong:*
  - Gotcha (3), that item 10's example *"rests on evidence found only in agent memory"*, was false. S44's receipt
    records it (`docs/archive/HANDOFFS-through-2026-08-09.md:411`). The review made the same false claim twice
    more (§4.2, §4.7), and S206 carried it too.
  - Next step (4)'s *"S203's recipe, `--cut <date>`"* could not be used, because every live record carried one
    date. That was computable at S207.
- *What was missing:* nothing material.
- *ROI:* clearly positive.

**Phase 3B — self-assessment 8/10.**
- *Right:*
  - Tested the second consideration's premise at Phase 0 instead of carrying it. It fell in one `git grep`, and
    the search turned up two more instances.
  - Showed the operator the exact delta and confirmed the rest was byte-identical by `diff`, not by eye.
  - Re-ran the pre-checks immediately before posting.
  - Read the comment back by `cmp` and checked GitHub's own rendering through `body_html`, the case S207 could not
    exercise.
  - Dry-ran the `CHANGELOG.md` trim four ways before writing it, and verified both new proofs in clones.
  - Kept tracked-file edits out of the working tree while the suite ran.
- *Wrong:*
  - Chose the `CHANGELOG.md` trim depth (retain 35) myself, with rationale but without offering the four options.
  - Found the third false claim (§4.2) only at close-out, after the approved scope was fixed, so it is owed rather
    than done.
  - Hit two zsh traps again (`echo =====`, an unquoted `--include=*.md`).
  - First wrote the receipt's shell pipe as `\|` and had to fix it.
- *Stakeholder corrections:* 0.

**Reduction (FM #28 close-out term):** one `HANDOFFS.md` receipt archived (trim + fold) and 54 `CHANGELOG.md` records
archived. No fork-learnings row was appended, so no retirement is owed. The lesson (an absence claim needs a search
of the archive shards) is failure mode #28's harder form and went to agent memory.

**Phase 3E — the build-equivalent, in a `--no-local` clone of `18fc1c2` with HEAD asserted by sha:**
`quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results 10575dac7361 · manifest 01a4ae7aa511`, with
`tests-sh-passed` 343 at two receipts. `bash bin/tests.sh` after the `HANDOFFS.md` trim: 343 / 0 / 6 skipped.
`bin/check-handoff` and `--all` OK after the receipt. Not exercised: this close-out commit (BL-64), GitHub's handling
of `merge=union`, and a `CHANGELOG.md` trim merged against a new entry under union.

**Fork push:** approved at the Phase 0 picker; taken after this commit, and recorded in its own push-record entry.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [BL-82] S208 — §6 of the PR #83 review POSTED to #83 (non-commit action, operator go-ahead); BL-82 closed

**Posted as one comment on upstream PR [#83](https://github.com/KJ5HST/methodology/pull/83):
[#issuecomment-5755256040](https://github.com/KJ5HST/methodology/pull/83#issuecomment-5755256040)**, author
`rmsharp`, 2026-09-21T04:08:24Z, on the operator's go-ahead at S208's second picker, given on the exact text
shown. **Pre-checks, run immediately before:** #83 still `OPEN` at head `219fb9d`, 0 comments, 0 reviews; the
repro link (`c3a096b` on `rmsharp/methodology`) returned HTTP 200; the body, extracted from §6 of
[`docs/planning/pr83-decisions-review.md`](docs/planning/pr83-decisions-review.md) at `f7fc621`, `cmp`-equal to
the text shown. **Read back** with `gh pr view 83 --json comments`: byte-identical to the posted body, apart from
the one trailing newline `jq` adds. **Rendered** (`gh api …/issues/comments/5755256040`, `body_html`): one table of
5 rows, both triple-backtick code spans intact, 11 list items, no stray code block — the rendering S207 could not
exercise.

**BL-82 closed:** its row moved to §Completed items in [`docs/planning/BACKLOG.md`](docs/planning/BACKLOG.md), the
open list updated, a closing update at the end of its detail block, and the review's status line, §6 heading and
§7 now say what was posted. `BACKLOG-DETAIL.md.verify.sh` C1–C5 OK. A reply on #83 is the maintainer's to make;
answering one would be new work and its own go-ahead.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [BL-82] S208 — the PR #83 review's final text, and two false "agent memory" claims corrected

In [`docs/planning/pr83-decisions-review.md`](docs/planning/pr83-decisions-review.md), before posting (operator,
S208 pickers):

- **§6, the comment:** one sentence added after the third bullet of *"What this changes in the plan"* — *"I ran
  that case on `HANDOFFS.md` only; a `CHANGELOG.md` trim against a new entry is untested."* The comment extracted
  from this commit differs from the text the operator approved after S207 by that sentence alone (`diff` of the
  two extractions); 1,091 words; renders under `pandoc -f gfm` with one table of 5 rows. **§7** lists the same
  untested case beside the others.
- **§4.1:** said S44's review-agent incident was *"recorded only in the operator's agent memory, not in a tracked
  file"*. False: S44's own receipt records it, [`docs/archive/HANDOFFS-through-2026-08-09.md:411`](docs/archive/HANDOFFS-through-2026-08-09.md),
  gotcha (1). Now cited, and it says the session reverted the edit.
- **§4.7:** said the Test 9 rate-limit details *"are in agent memory"*. Also false: S178's receipt records them,
  [`docs/archive/HANDOFFS-through-2026-09-17.md:62`](docs/archive/HANDOFFS-through-2026-09-17.md), gotcha (3).
  Now cited. S206's gotcha (4) and S207's gotcha (3) carried the first claim; their receipts are left as written.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-09-20.md` (54 record(s), 179,924 B → 73,573 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **54** record(s) (2026-09-20 → 2026-09-20) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-09-20.md`](docs/archive/CHANGELOG-through-2026-09-20.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-09-20.md.verify.sh`](docs/archive/CHANGELOG-through-2026-09-20.md.verify.sh)
rather than trusting a digest printed here. Live file 179,924 B → 73,573 B (−59.1%).

### 2026-09-20 · [ad hoc] S208 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

- **What:** the trimmer's 3-line pointer block for `docs/archive/HANDOFFS-through-2026-09-20-9.md` became one row at
  the bottom of [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md) and was deleted from the ledger's
  front matter. `HANDOFFS.md` 14,504 B → 14,048 B.
- **Its own commit by design:** inside the trim commit the shipped `.verify.sh` fails L2 (fork Learning #58). The
  verifier was run against the trim commit `c9853b8`, in a `--no-local` clone, **before** the fold — L1,
  L2/front-matter, L3 all OK, exit 0, 3 records = 2 retained + 1 archived, 0 added by the trim commit.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-20-9.md` (1 record(s), 24,374 B → 14,504 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-20 → 2026-09-20) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-20-9.md`](docs/archive/HANDOFFS-through-2026-09-20-9.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-20-9.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-20-9.md.verify.sh)
rather than trusting a digest printed here. Live file 24,374 B → 14,504 B (−40.5%).

### 2026-09-20 · [BL-82] S208 claim — post §6 of the PR #83 review to #83 (in progress)

**Deliverable:** the comment in §6 of [`docs/planning/pr83-decisions-review.md`](docs/planning/pr83-decisions-review.md),
posted to upstream PR [#83](https://github.com/KJ5HST/methodology/pull/83) as one comment and read back. Chosen at
this session's Phase 0 picker. The operator approved the text after S207's close-out; the picker adds **one
sentence** first, after the third bullet of *"What this changes in the plan"*: the trim-against-new-entry case was
run on `HANDOFFS.md` only, so a `CHANGELOG.md` trim against a new entry is stated as untested. The final text is
shown to the operator before posting.

**Side actions approved at the same picker, each its own commit or record:** the `HANDOFFS.md` retention trim this
claim makes owed; a scoped `CHANGELOG.md` trim (20,008 B under the 196,608 B trigger at Phase 0), dry run first;
correcting §4.1 of the review, which says S44's review-agent incident is *"recorded only in the operator's agent
memory, not in a tracked file"* — S44's own receipt records it, `docs/archive/HANDOFFS-through-2026-08-09.md:411`,
gotcha (1); and pushing fork `main` to `origin`.

**Phase 0, for the record:** both ledger frontiers = HEAD `5bb10c5`, gaps empty, no pending stub, 2 receipts before
this one. Gate citation re-run in a `--no-local` clone with HEAD asserted by sha: `11/11 pass · results
10575dac7361 · manifest 01a4ae7aa511`, S207's citation exactly. Dashboard 76/100, medium, 0 high+. Upstream 0 open
issues; #83 head `219fb9d`, 0 comments, 0 reviews; #84 one comment (the fork's own); #85 unchanged. Local `main` 7
ahead of `origin/main` (`0dcc291`), 0 behind `upstream/main` (`6b29d3d`).

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [BL-82] S207 — operator review after close-out: the rewritten §6 approved

The operator, on the §6 text shown in S207's close-out report: *"Those look fine."* Recorded as **approval of
the rewritten comment** in [`docs/planning/pr83-decisions-review.md`](docs/planning/pr83-decisions-review.md) §6,
which is unchanged. **It is not a go-ahead to post:** posting to PR #83 is outward and needs its own go-ahead on
the exact text. The words do not settle whether *"those"* also covered the two pre-posting considerations the
report raised: the untested `CHANGELOG.md` trim-against-prepend case under union, and item 10's example resting
on agent memory only. The posting picker asks. Recorded in S207's receipt (next step (1)), BL-82's index row and
its detail block.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [BL-82] S207 close-out — §6 recomposed for the operator's review; nothing posted

**Deliverable: BL-82's §6 rewritten** (`1259287`). The proposed comment for upstream PR #83 in
[`docs/planning/pr83-decisions-review.md`](docs/planning/pr83-decisions-review.md) was recomposed against the three
defects the operator named: too dense, undefined terms, poor structure. **Nothing posted.** BL-82 stays open on
that one outward step, after the operator's review. Supporting commits: `555bbce` claim, `003a243` + `7f77925`
the owed `HANDOFFS.md` trim and its fold.

**Phase 3A — S206's handoff scored 8/10.**
- *What helped, concretely:*
  - Next step (0) quoted the operator's words and said *"recompose … rather than appending"*. It also said to ask
    what "clarification" should cover, which became the picker's second question. The answer (three defects)
    turned a vague brief into three checkable targets.
  - `key_files` put §6 at `:278`, which was exact, and pointed to the plan's §8 at `:414`.
  - Gotchas (6) and (7) (`--cut N` retains N; a dry run needs `--force`) were used and right. The
    three-receipts prediction held a seventh time.
- *What was missing:* nothing flagged that §6 used ten of the plan's own codes ("D4", "Shape B", …) against the
  operator's recognized-terms rule. Its preface certified only part of that rule, so it read as compliant.
- *What was wrong:* nothing material. *"#85, #84, #83 open, 0 reviews each"* was true; #84's one comment is the
  fork's own check-in, posted and recorded at S201.
- *ROI:* clearly positive.

**Phase 3B — self-assessment 8/10.**
- *Right:*
  - Asked what "hard to read" meant before drafting, so the rewrite answers named defects rather than a guess.
  - Recomposed §6 whole; §0–§5 needed no change.
  - Re-ran the repro and read the fused block before describing it.
  - Checked the one new claim (*"GitHub's merge button runs no checker"*) against upstream's tree.
  - Rendered the extracted comment with `pandoc -f gfm`, so the code spans and the table are checked, not assumed.
  - Drafted in the scratchpad while the suite ran on the live tree.
  - Stated the length cost instead of hiding it.
- *Wrong:*
  - The first pass ran to 1,269 words and needed a cut; the result is still twice the original's length, which
    may not be what "too dense" asked for.
  - Hit the zsh `echo =====` trap at Phase 0 despite the memory warning, and called the trimmer with a
    positional path once (both harmless).
  - The comment's carried figures (17/71 tokens, ~29 API calls, `56997af`) were taken from S206, not re-run.
  - The untested `CHANGELOG.md` trim-against-prepend case was found, not measured; it is flagged for the
    posting decision.
- *Stakeholder corrections:* 0.

**Reduction (FM #28 close-out term):** a `HANDOFFS.md` receipt was archived (trim + fold). No fork-learnings row was
appended, so no retirement is owed; the session's lesson is an operator preference for outward text and went to
agent memory.

**Phase 3E — the build-equivalent, in a `--no-local` clone of `1259287` with HEAD asserted by sha:** `quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results 10575dac7361 · manifest 01a4ae7aa511`,
with `tests-sh-passed` 343 at two receipts. `bash bin/tests.sh` after the trim: 343 / 0 / 6 skipped.
Not exercised: this close-out commit (BL-64), GitHub's rendering of the comment (only pandoc's), GitHub's handling of
`merge=union`, and a `CHANGELOG.md` trim merged against a prepend under union.

**Fork push:** not taken. Local `main` is 6 ahead of `origin/main`, and no go-ahead was given this session.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [BL-82] S207 — §6 of the PR #83 review recomposed for readability (not posted)

- **What:** §6 of [`docs/planning/pr83-decisions-review.md`](docs/planning/pr83-decisions-review.md), the proposed
  comment for upstream PR #83, rewritten against the three defects the operator named at this session's picker:
  **too dense, undefined terms, poor structure.** It now leads with the one suggested change (leave
  `HANDOFFS.md` out of `merge=union`). *What goes wrong*, *why* and *how it was checked* are separate short
  paragraphs, with the repro's four cases as a table. Each smaller note is named by its §8 item and subject
  instead of a bare plan code such as "D5". Recomposed, not appended to; §0–§5 needed no change.
- **Evidence behind the wording:** `docs/planning/pr83-union-repro.py` re-run, exit 0, output identical to
  S206's. The fused `HANDOFFS.md` block was read to describe it: two `session:` lines, the shared fields once,
  then both receipts' other fields. Upstream has no `.github/` workflows at `6b29d3d` or `219fb9d`, so
  *"GitHub's merge button runs no checker"* holds. The comment, extracted with its `>` markers stripped,
  renders under `pandoc -f gfm`: one table of 5 rows, both triple-backtick code spans intact.
- **Cost, stated:** about 1,075 words when pasted, against 523 before. The definitions cost words.
- **BL-82:** index row (`docs/planning/BACKLOG.md:170`) and an S207 update at the end of its detail block.
  `BACKLOG-DETAIL.md.verify.sh` C1–C5 OK. **Open on one step: posting, after the operator's review — outward.**
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [ad hoc] S207 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

- **What:** the trimmer's 3-line pointer block for `docs/archive/HANDOFFS-through-2026-09-20-8.md` became one row at
  the bottom of [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md) and was deleted from the ledger's
  front matter. `HANDOFFS.md` 15,670 B → 15,214 B.
- **Its own commit by design:** inside the trim commit the shipped `.verify.sh` fails L2 (fork Learning #58). The
  verifier was run against the trim commit `003a243`, in a `--no-local` clone, **before** the fold — L1,
  L2/front-matter, L3 all OK, exit 0, 3 records = 2 retained + 1 archived, 0 added by the trim commit.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-20-8.md` (1 record(s), 24,443 B → 15,670 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-20 → 2026-09-20) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-20-8.md`](docs/archive/HANDOFFS-through-2026-09-20-8.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-20-8.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-20-8.md.verify.sh)
rather than trusting a digest printed here. Live file 24,443 B → 15,670 B (−35.9%).

### 2026-09-20 · [BL-82] S207 claim — rewrite §6 of the PR #83 review for readability (in progress)

**Deliverable:** a recomposed §6 (*"Proposed comment for #83"*) of
[`docs/planning/pr83-decisions-review.md`](docs/planning/pr83-decisions-review.md), presented to the operator
for review. Chosen at this session's Phase 0 picker, per S206's next step (0). The operator named three
defects at that picker: **too dense, undefined terms, poor structure.** So the rewrite leads with the one
suggestion, defines or drops every term a reader of the plan might not share, and gives the comment
labelled parts that name each note by the plan's own item title.

**Scope, stated so the close-out can be checked against it.** Only §6 changes, plus whatever in §0–§5 cites
§6's wording. **Nothing is posted to #83**; posting stays a separate outward go-ahead on the exact text. No
framework file is edited. The comment's findings are not re-derived unless the rewrite changes a claim.

**Phase 0, for the record:** both ledger frontiers = HEAD `8f5bbb7`, gaps empty, no pending stub,
2 receipts before this one. Gate citation re-run in a `--no-local` clone with HEAD asserted by sha:
`11/11 pass · results 10575dac7361 · manifest 01a4ae7aa511`, S206's citation exactly. Dashboard 76/100,
medium, 0 high+. Upstream 0 open issues; #83 head `219fb9d`, 0 comments, 0 reviews; #84's one comment is
the fork's own check-in (already recorded); #85 unchanged. Local `main` 1 ahead of `origin/main`.

**Also owed at this claim, its own action:** the `HANDOFFS.md` retention trim — this claim's receipt
makes **three** (`--cut 2 --force`).

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [BL-82] S206 — operator direction after close-out: rewrite §6 for readability before its review

The operator, after S206's close-out report: *"I find the section 6 comment hard to read. Add clarification of the comment prior to review in the next session."* **Scheduled, not started** (one deliverable per
session). The next session's deliverable is a clearer §6 of
[`docs/planning/pr83-decisions-review.md`](docs/planning/pr83-decisions-review.md), presented for review. It
precedes any decision to post, which stays a separate outward go-ahead. Recorded in S206's receipt as next step
(0), in BL-82's detail block, and in its index row. Nothing in §6 was changed here.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [ad hoc] S206 — fork `main` pushed to `origin`, `2a8a76a..dec85c6` (non-commit action, operator go-ahead)

Fourteen commits: S205's seven, unpushed since that session requested no push, plus this session's seven. Fork
remote only — **nothing upstream-facing.** Approved at this session's Phase 0 picker for the close-out. Read back after
the push: `origin/main` = `dec85c6` = local `main`, ahead/behind 0/0. The review's pinned repro link now resolves
(`gh api` on `c3a096b`'s `docs/planning/pr83-union-repro.py`: blob `092314853d29`, equal to the local blob). This
record is pushed after it under the standing push-record grant.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [BL-82] S206 close-out — the twelve decisions were the maintainer's, and union fuses receipts

**Deliverable: BL-82 drafted** (`15be6ec`) — [`docs/planning/pr83-decisions-review.md`](docs/planning/pr83-decisions-review.md),
a collaborator's positions on upstream PR #83's twelve §8 decisions, with a proposed comment in its §6. **Nothing
posted.** BL-82 stays open on that one outward step. Supporting commit: `c3a096b`, a re-runnable repro built from
upstream's own history.

**Phase 3A — S205's handoff scored 8/10.**
- *What helped, concretely:*
  - Next-step (2) named the source and the fetch command (`git fetch upstream refs/pull/83/head`) and said *"read
    BL-82's four settle-first questions before drafting"*. Those four questions became the review's §1, and
    question (a) is what overturned the item's premise.
  - Next-step (1) framed BL-78 P3 as a yes/no with its evidence attached. It went into the picker unchanged and
    was answered in one line.
  - The retention-trim prediction held for the **sixth** consecutive session.
  - Gotchas (5) and (6) (`--cut N` retains N; a dry run needs `--force`) were both used and both right.
- *What was missing:* the hypothesis S204 recorded — *"the operator there may be him"* — was not carried into
  BL-82 or the handoff, so the item's headline asserted the opposite.
- *What was wrong:* BL-82's headline *"waiting on TWELVE OPERATOR DECISIONS, not on a review"* was half wrong.
  The decisions are the maintainer's, and a review is what the fork can give. Everything else checked out: the
  PR states, the byte figures and the key-file lines.
- *ROI:* clearly positive.

**Phase 3B — self-assessment 8/10.**
- *Right:*
  - Settled whose decisions they were from the maintainer's own receipts before taking a single position.
  - Measured D4 rather than reviewing its prose.
  - Made the measurement re-runnable from upstream history alone, so the maintainer can run it without fork
    commits.
  - Caught an unfair fixture of my own (two copies of one receipt) and re-ran with two different receipts before
    believing the result.
  - Surfaced integration facts the maintainer cannot see from his side: #84 leaves `SAFEGUARDS.md` 17 tokens of
    headroom, #85 moves the hook lines the plan cites, and PR #80's 11 commits are the fork's and already recorded
    here.
- *Wrong:*
  - Hit the zsh `$r:` modifier trap again, despite the memory warning (one failed command, no harm).
  - Wrote one temporary file to `/tmp` rather than the scratchpad, and removed it.
  - My first wholeness check for `CHANGELOG.md` was byte-strict and briefly read "not whole" for what was one lost
    blank line. It was refined before any claim was written.
  - Two pieces of the review's evidence (S44, S115) live only in agent memory; the review says so.
- *Stakeholder corrections:* 0.

**Reduction (FM #28 close-out term):** a `HANDOFFS.md` receipt was archived (trim + fold). No fork-learnings row
was retired: D3 was refused explicitly, with five rows named.

**Phase 3E — the build-equivalent, in a `--no-local` clone of `5c6e642` with HEAD asserted by sha:** `quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results 10575dac7361 · manifest 01a4ae7aa511`, with `tests-sh-passed` 343 at two receipts. Not exercised: this close-out commit (BL-64), GitHub's handling of `merge=union`, and the JSONL histories under union.

**Fork push:** approved at the Phase 0 picker for this close-out, `main` → `origin`. It is recorded in its own
push-record entry once read back.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [ad hoc] S206 — Phase 3C: fork Learning #90, and the D3 retirement obligation discharged by refusal

- **What:** [`docs/FORK_LEARNINGS.md`](docs/FORK_LEARNINGS.md) row **#90**, 1,142 B — *a line-level merge driver
  keeps lines, not records, so a claim that a merge keeps records "whole" must be tested on the records' real
  format.* It comes from this session's D4 measurement. Real ledger entries survived `merge=union`, but two
  real receipts fused into one block with two `session:` lines, and the merge exited 0. The receipts' shared
  fence lines are enough to cause it.
- **D3 discharged by explicit refusal. No row is retired; the rows considered are named** (`CLAUDE.md`
  §*Where this fork's learnings go*): **#31** (fixture anchors from a live artifact couple a test to its size),
  **#33** (a failure count undercounts coverage loss), **#41** (a live-repository fixture is green as a function
  of size), **#58** (build both shapes to break a scope tie) and **#82** (a hook fails open, silently).
  - **(a) fails for all five.** Test 34's named `SKIP` rows mechanize #33's shape for one test only, and
    `pre-commit-selftest` tests the hook's logic, not whether it is armed (BL-77, open). No gate, test or
    numbered failure mode enforces the general lesson of any of them.
  - **(b) fails.** #90 is a merge-semantics lesson and restates none of theirs.
  - **(c) fails.** Test 34, the trimmer and `.githooks/pre-commit` all still exist.
  - Age and file size are never grounds.
- **Verified:** `bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations` → **76 rows,
  contiguous 15..90, 0 over 1,500 B**. The file is 94,774 B, against the 81,920 B reported series (not a limit).
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [BL-82] S206 — PR #83's twelve decisions drafted: a collaborator's positions, and one finding that changes D4

- **What:** [`docs/planning/pr83-decisions-review.md`](docs/planning/pr83-decisions-review.md), the BL-82 deliverable.
  It is internal: **nothing is posted to #83**, and its §6 carries a proposed comment text for a separate go-ahead.
- **BL-82's four questions, settled first (§1).** **(a)** The twelve are the **maintainer's** decisions, not
  this fork's. His S24 receipt's next step (a) is *"OPERATOR: answer the twelve §8 decisions on PR #83"*, the
  plan's field evidence is in his agent memory, and S22 names `rmsharp` beside "the operator". So BL-82's
  *"not on a review"* was the wrong half, and the document offers review positions, not rulings. **(b)** The
  document first, the comment separately. **(c)** No commitment, but a stake in D4 and D5. **(d)** A
  re-run-vs-taken table. The plan's budget figures reproduce exactly at `6b29d3d` (runner 18,865/18,900,
  `SAFEGUARDS.md` 6,029/6,100).
- **Positions:** agree with eight of the twelve as recommended; reword item 12 (the plan does edit Principle 9 and
  flight-manual Phase 1 step 4); clarify D5 for a fork's own trunk; leave D12 to the maintainer; D11 not now.
  **Change D4:** per `c3a096b`, keep `merge=union` for `CHANGELOG.md` and the JSONL histories, and leave
  `HANDOFFS.md` unattributed. Evidence added: PR #80's 11 commits are the fork's and all are in the fork's
  ledger; `SAFEGUARDS.md` headroom falls 71 → 17 tokens at #84's head; #85 moves the hook lines the plan cites.
- **BL-82 stays open on one outward step only:** posting §6. Its index row is rewritten, since the old one
  carried the half-wrong framing, and its detail block gains an S206 update.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [BL-82] S206 — a re-runnable test of PR #83's `merge=union` premise, from upstream's own history

- **What:** [`docs/planning/pr83-union-repro.py`](docs/planning/pr83-union-repro.py), stdlib Python, scratch
  repositories only. It rebuilds the plan's Shape B case from upstream commits alone — S23 and S24 both
  claiming from `64f23bf` (base `64f23bf`, ours `6b29d3d`, theirs `219fb9d` minus S23's block, each a checked
  pure insertion at one anchor) — and merges each ledger without and with `merge=union`.
- **Result, git 2.50.1:** `CHANGELOG.md` — union exit 0, both entries whole except **one blank separator line**
  (1,592 of 1,593 lines). `HANDOFFS.md` — union exit 0 and the two receipts **fuse into one block** (two
  `session:` lines); `bin/check-handoff --all` exit 1. Two receipts that share no line but their fences fuse
  too, and a synthetic retention-trim case brings an archived receipt back into the live file. The plan's D4
  says union *"keeps both whole"*; for receipts it does not.
- **Its own commit** so the review document can cite it by sha. Nothing outward.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [ad hoc] S206 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

- **What:** the trimmer's 3-line pointer block for `docs/archive/HANDOFFS-through-2026-09-20-7.md` became one row at
  the bottom of [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md) and was deleted from the ledger's
  front matter. `HANDOFFS.md` 15,110 B → 14,654 B.
- **Its own commit by design:** inside the trim commit the shipped `.verify.sh` fails L2 (fork Learning #58). The
  verifier was run against the trim commit `d387bca`, in a `--no-local` clone, **before** the fold — L1,
  L2/front-matter, L3 all OK, 3 records = 2 retained + 1 archived, 0 added by the trim commit.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-20-7.md` (1 record(s), 23,765 B → 15,110 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-20 → 2026-09-20) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-20-7.md`](docs/archive/HANDOFFS-through-2026-09-20-7.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-20-7.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-20-7.md.verify.sh)
rather than trusting a digest printed here. Live file 23,765 B → 15,110 B (−36.4%).

### 2026-09-20 · [BL-82] S206 claim — draft answers to PR #83's twelve operator decisions (in progress)

**Deliverable:** a document under `docs/planning/` drafting answers to the twelve items in §8 of upstream
PR [#83](https://github.com/KJ5HST/methodology/pull/83)'s `docs/planning/parallel-sessions-plan.md`
(*"Open decisions for the operator (answer before Phase 1)"*), per
[`docs/planning/BACKLOG-DETAIL.md`](docs/planning/BACKLOG-DETAIL.md) §BL-82. Chosen by the operator at
this session's Phase 0 picker over a scoped `CHANGELOG.md` trim, BL-80's fix and BL-79's plan.

**Scope, stated so the close-out can be checked against it.** The draft settles BL-82's four questions
before answering anything, and marks each of the twelve as *ratify the author's recommendation* or *decide
fresh*. **It is internal.** Nothing is posted to #83 — a comment, review or edit there is an outward
action and needs its own go-ahead. No framework file is edited.

**Phase 0, for the record:** both ledger frontiers = HEAD `c77aa65`, gaps empty, no pending stub,
2 receipts before this one. Gate citation re-run in a `--no-local` clone with HEAD asserted by sha:
`11/11 pass · results 10575dac7361 · manifest 01a4ae7aa511`, S205's citation exactly. Dashboard 76/100,
medium, 0 high+. Upstream 0 open issues; #85, #84, #83 open, 0 reviews each, nothing moved since S205.

**Also owed at this claim, its own action:** the `HANDOFFS.md` retention trim — this claim's receipt
makes **three**, one above the policy's depth of two (`--cut 2 --force`). **Fork push:** approved at
the picker for close-out, `main` → `origin` (S205's seven commits and this session's).

### 2026-09-20 · [BL-78] S206 — P3 decided by the operator: no enforcement, so BL-78 closes

At this session's Phase 0 picker the operator answered BL-78 P3 (*"only if the operator wants
enforcement: cost the check itself"*) **no**. The evidence offered with the question was BL-78 §(3): a
pre-commit byte check would have caught 4 of 7 recent growths and none of `SESSION_RUNNER.md`'s, which
all arrived by merge. P1 (`6ddfdb7`) and P2 (`fac748f`) are done, so **nothing is left to execute and
BL-78 closes.** **The closing edits are not made here** and are their own short session: the index row
at `docs/planning/BACKLOG.md:166` (still the pre-P1 description), the move per the archive convention,
and `.context-budget.json` `files[4]._`, whose *"every commit that grows it is refused"* describes a
refusal nothing in this clone calls (S205 gotcha (1)). Recorded in BL-78's detail block too.

### 2026-09-20 · [ad hoc] S205 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

- **What:** the trimmer's 3-line pointer block for `docs/archive/HANDOFFS-through-2026-09-20-6.md` became one row at
  the bottom of [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md) and was deleted from the ledger's
  front matter. `HANDOFFS.md` 14,956 B → 14,500 B.
- **Its own commit by design:** inside the trim commit the shipped `.verify.sh` fails L2 (fork Learning #58). The
  verifier was run against the trim commit `219ce5b` **before** the fold — L1, L2/front-matter, L3 all OK, 3 records
  = 2 retained + 1 archived, 0 added by the trim commit.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-20-6.md` (1 record(s), 23,314 B → 14,956 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-20 → 2026-09-20) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-20-6.md`](docs/archive/HANDOFFS-through-2026-09-20-6.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-20-6.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-20-6.md.verify.sh)
rather than trusting a digest printed here. Live file 23,314 B → 14,956 B (−35.8%).

### 2026-09-20 · [BL-78] S205 close-out — a pin demoted to a report, and the note that dated it to the wrong session

**Deliverable: BL-78 P2, done** (`fac748f`). `.context-budget.json` `files[5]` (`starter-kit/SAFEGUARDS.md`) —
the `_` note now states that `max_bytes` **15,386 B is a reported series, not a no-growth pin** (option β, BL-53
option C's precedent). Exactly **one** changed key path, `/files[5]/_`, walked object-to-object; no number moved.
**BL-78 stays open** on P3 alone, which is an operator yes/no, not a measurement.

**Phase 3A — S204's handoff scored 8/10.** *What helped, concretely:* next-step (1) named P2 as *"ratified and
unexecuted — the next unit"* with its DONE criterion and both verify commands, so Phase 1 was a one-line
decision. The retention-trim prediction held for the **fourth** consecutive session. Gotcha (1) (*`CHANGELOG.md`
has no fold*) saved a repeat of S204's own amend; (3) and (4) (`--cut N` retains N; a dry run needs `--force`)
were both used and both right; (6) (`check-learnings` needs `--file`) and (7) (measure the row before appending)
meant #89 passed the 1,500 B budget first time at 1,258 B. Next-step (2) — **#84's split offer is ours; #83 is the
maintainer's own PR waiting on twelve answers** — was re-checked with `gh pr view` and held, and it is what BL-82
is built on. *What was missing:* next-step (3) said the #85/#83 drafts *"were put in the 3G report and posted
nowhere"* but not that they were therefore **gone** — the operator asked this session to re-show them, and the
honest answer was that no file holds them. *What was wrong:* nothing in the handoff. Every number re-derived at
Phase 0 matched. *ROI:* strongly positive.

**Phase 3B — self-assessment 8/10.** *Went well:* every enforcement claim in the new note was read from the
source, not inherited — `.githooks/pre-commit:131-133`, `precommit_check` at `context_budget.py:1037`, the gate
list in `.quality-gates.json`. **The rewrite caught a provenance error its two predecessors read past:** the
replaced note dated the byte pin to S177; `git blame` and `git log -S` put it at **`beffbd0` (S129, 2026-08-30)**,
17 days earlier, where it was the file's measured size, stable 53 days — which also inverts the old note's
*"not a measurement dressed as a budget"*. Now fork Learning #89. The operator's picker asked for the #83
write-up **alongside** the deliverable; it was opened as BL-82 rather than done, and that was stated before
acting, not after. *Went badly:* one `git blame -L "${n},${n}"` ran with an empty `$n` and blamed the whole file
instead of failing — harmless here, recorded as a gotcha. *Not done:* `files[4]._` still claims *"every commit
that grows it is refused"*, which is false in this clone; it was out of P2's one-key scope, and BL-78's own detail
block (`BACKLOG-DETAIL.md:2814`) already records it, so it was left and flagged rather than fixed.

**Verified:** `quality_ratchet.py --run` in a `--no-local` clone of `29d07c5` with HEAD asserted by sha —
`11/11 pass · 0 fail · 0 unmeasured · results 10575dac7361 · manifest 01a4ae7aa511`; `bash bin/tests.sh`
**343 / 0 / 6 skipped** after the trim; the shard's `.verify.sh` **L1/L2/L3 OK**; `tools/test_context_budget.py`
**122 OK**; `context_budget.py` exit 2, same four `over` rows; `BACKLOG-DETAIL.md.verify.sh` **C1–C5 OK**;
`bin/check-links` **111/23**; `bin/check-learnings` **75 rows, 0 over**; `bin/check-handoff` **OK**.

**Nothing upstream-facing was taken.** The operator authorized no outward action this session. Fresh #85/#83
comment drafts go into the close-out report only.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [ad hoc] S205 — Phase 3C: fork Learning #89, and the D3 retirement obligation discharged by refusal

- **What:** [`docs/FORK_LEARNINGS.md`](docs/FORK_LEARNINGS.md) row **#89**, 1,258 B — *a config row is one object
  but many lines in git, and a note that opens by dating one key carries that date onto its neighbours.* Drawn
  from this session's own near-miss: the note P2 replaced dated the **byte** pin to S177, which set only the
  `max_tokens` beside it. `git blame` splits the two adjacent lines by **17 days** (`0e8c6ac8` 2026-09-16 vs
  `beffbd0` 2026-08-30), and the misdating inverted the note's own characterization of the figure.
- **D3 discharged by explicit refusal — no row retired, and the rows considered are named** (`CLAUDE.md`
  §*Where this fork's learnings go*): **#86** (re-pointing a note inverts its clauses), **#87** (a ceiling that is
  half of an identity), **#88** (a self-recording instrument diffs against itself), **#54** (`git blame` before
  scrubbing a site a review calls residue) and **#56** (settle a rule from its written provenance). None meets
  criterion (a) — no `.quality-gates.json` gate, `bin/tests.sh` test or numbered failure mode enforces any of
  their lessons, and the byte half of the read-set partition is still unguarded (BL-78 shape (2), uncosted).
  None meets (b): #89 **narrows** #54's and #56's provenance lesson to config keys rather than restating it more
  generally, and it does not state #86's subject-change lesson at all. None meets (c): `.context-budget.json`,
  `starter-kit/context_budget.py` and the archive shards all still exist. Age and file size are never grounds.
- **Verified:** `bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations` → **75 rows,
  contiguous 15..89, 0 over 1,500 B**.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [ad hoc] S205 — BL-82 opened: PR #83 is waiting on twelve operator decisions, not on a review

- **What:** [`docs/planning/BACKLOG-DETAIL.md`](docs/planning/BACKLOG-DETAIL.md) §BL-82, with its index row in
  [`docs/planning/BACKLOG.md`](docs/planning/BACKLOG.md) and the `Open:` enumeration extended. Opened at the
  operator's request in this session's Phase 0 picker, where a write-up of the twelve was also asked for —
  **that write-up is a second deliverable and was NOT executed**, which is what the item is for.
- **The correction it records:** [#83](https://github.com/KJ5HST/methodology/pull/83) is the **maintainer's own**
  pull request (author `KJ5HST`, opened 2026-09-16, branch `docs/parallel-sessions-plan`), it has **0 reviews and
  0 comments**, and its §8 — *"Open decisions for the operator (answer before Phase 1)"* — puts **twelve** items to
  the operator, eleven of them with the author's own recommendation and a twelfth that is a scope boundary to
  confirm. Recent handoffs carried it as *"unreviewed and unchased"*, framing the blocker as ours to clear by
  reviewing. It is not; the plan names answering §8 as its own Phase 0.
- **Route:** drafting the answers is fork-side and internal; **posting them to #83 is outward and its own
  go-ahead.** Nothing was posted, commented, reviewed or edited upstream in this session.
- **Checked, not relayed:** `gh pr view 83 --repo KJ5HST/methodology` for the author, review and comment counts;
  the §8 list read from `refs/pull/83/head`, not from a summary.
- **Verified:** `docs/planning/BACKLOG-DETAIL.md.verify.sh` C1–C5 OK; `bin/check-links` 111 links / 23 files.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [BL-78] S205 — P2 done: `SAFEGUARDS.md`'s pin becomes a reported series, and no number moved

- **What:** `.context-budget.json` `files[5]` (`starter-kit/SAFEGUARDS.md`) — the `_` note rewritten so the row's
  `max_bytes` **15,386 B** is stated as a **reported series, not a no-growth pin**, on the precedent BL-53 option C
  set for the 81,920 B `docs/FORK_LEARNINGS.md` figure. **Option β**, settled by the operator at S204's Phase 0
  picker; option α (re-pin at 17,129 and re-partition the sibling to 39,621 B / 17,455 tok) was declined.
- **Exactly one key path changed: `/files[5]/_`** — proved by walking the before/after objects path-by-path rather
  than by eyeballing the diff; the key **set** is identical and every other value is byte-equal. `max_bytes`,
  `max_tokens`, `measured_bytes` and `measured_on` are untouched, so the read-cap partition
  (41,364 + 15,386 = 56,750 B; 18,222 + 6,777 = 24,999 tok) is unchanged.
- **Why the demotion is cheap, measured rather than argued:** the partition's **token** half is asserted
  (`tools/test_context_budget.py:1258`, which S203 showed fails at 25,767 > 25,000 when both keys move) and its
  **byte** half is asserted **nowhere** — S203 moved `max_bytes` alone and the suite stayed 122 OK with the row
  printing `ok`. Demoting the byte figure to a report costs no assertion; editing it would have cost one.
- **A provenance error corrected in the same note.** The text replaced said the ceiling is *"this file's size as it
  stood at S177"*. It is not: `git log -S '"max_bytes": 15386' -- .context-budget.json` returns exactly one commit,
  `beffbd0` (2026-08-30, S129), where 15,386 B was the size of blob `f0964195` — a size `SAFEGUARDS.md` had carried
  unchanged since `719a41d` (2026-07-08), 53 days. S177 added only `max_tokens` 6,777 and re-measured nothing.
- **Verification:** `python3 tools/test_context_budget.py` → **Ran 122 tests, OK**; `python3 starter-kit/context_budget.py`
  → exit **2** with the same four `over` rows (`docs/FORK_LEARNINGS.md`, `starter-kit/SESSION_RUNNER.md`,
  `starter-kit/SAFEGUARDS.md`, read-set total) — this step changes no verdict, which is the point.
- **Surface:** this repository's working tree. It cannot show what an adopter sees: `.context-budget.json` here is
  this repo's own config, not the distributed seed `starter-kit/context-budget.json`, which budgets different files.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [BL-78] S205 claim — P2: `SAFEGUARDS.md`'s row becomes a reported series (in progress)

**Deliverable:** **BL-78 phase P2, option β**, settled by the operator at S204's Phase 0 picker and
recorded in `.context-budget.json` `files[5]._` itself — convert the `starter-kit/SAFEGUARDS.md`
read-set row from a no-growth **pin** to a **reported series**, on BL-53 option C's precedent
([`docs/planning/BACKLOG-DETAIL.md`](docs/planning/BACKLOG-DETAIL.md) §BL-78, *RECOMMENDATION* P2).
Chosen by the operator after this session's Phase 0 (picker) over BL-81's costing, BL-80's and BL-79's.

**Scope, stated so the close-out can be checked against it.** Exactly one key path: `/files[5]/_`.
**`max_bytes` 15,386 and `max_tokens` 6,777 are not touched** — the two per-file ceilings partition
the read cap (41,364 + 15,386 = 56,750 = 25,000 tok × 2.27), so re-pinning one re-partitions both.
That is option α, which the operator did not take.

**Also owed at this claim, its own action:** the `HANDOFFS.md` retention trim — this claim's receipt
makes **three**, one above the policy's depth of two (`--cut 2 --force`), exactly as S204's handoff
predicted.

**Nothing upstream-facing is approved.** #85, #84 and #83 are untouched. A write-up of PR #83's
twelve operator decisions was asked for in the same picker and is **opened as a backlog item**, not
executed here — it is a second deliverable, and S204's #85/#83 comment drafts were never persisted
to any tracked file, so there is nothing to re-show.

### 2026-09-20 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-09-19.md` (79 record(s), 233,183 B → 130,149 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **79** record(s) (2026-09-18 → 2026-09-19) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-09-19.md`](docs/archive/CHANGELOG-through-2026-09-19.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-09-19.md.verify.sh`](docs/archive/CHANGELOG-through-2026-09-19.md.verify.sh)
rather than trusting a digest printed here. Live file 233,183 B → 130,149 B (−44.2%).

### 2026-09-20 · [ad hoc] S204 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

- **What:** the trimmer's 3-line pointer block for `docs/archive/HANDOFFS-through-2026-09-20-5.md` became one row at
  the bottom of [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md) and was deleted from the ledger's
  front matter. `HANDOFFS.md` 14,602 B → 14,146 B.
- **Its own commit by design:** inside the trim commit the shipped `.verify.sh` fails L2 (fork Learning #58). The
  verifier was run against the trim commit `a533938` **before** the fold — L1, L2/front-matter, L3 all OK, 3 records
  = 2 retained + 1 archived, 0 added by the trim commit.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-20-5.md` (1 record(s), 23,553 B → 14,602 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-20 → 2026-09-20) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-20-5.md`](docs/archive/HANDOFFS-through-2026-09-20-5.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-20-5.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-20-5.md.verify.sh)
rather than trusting a digest printed here. Live file 23,553 B → 14,602 B (−38.0%).

### 2026-09-20 · [ad hoc] S204 — fork `main` pushed to `origin`, `6a56261..7ca7b94` (non-commit action, operator go-ahead)

Sixteen commits: S203's eight, unpushed since that session's picker did not include the push, plus this
session's eight. Fork remote only — **nothing upstream-facing.** Approved at this session's Phase 0 picker.
Read back after the push: `origin/main` = `7ca7b94` = local `main`, 0 commits behind.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [BL-78] S204 close-out — a key that decides nothing, said so in the one place it is read

**Deliverable: BL-78 P1, done** (`6ddfdb7`). `.context-budget.json` `files[4].measured_bytes` 54,363 →
**55,406**, `files[5].measured_bytes` 15,386 → **17,129**, both `measured_on` **2026-09-20**, and both `_`
notes state that `measured_bytes` is a **record, not a ceiling**. `max_bytes` / `max_tokens` untouched;
exactly six changed key paths, walked object-to-object.

**Phase 3A — S203's handoff scored 8/10.** *What helped, concretely:* the costing block at
`BACKLOG-DETAIL.md:2866` was directly executable — P1's DONE criterion, its two verify commands and its
surface were all stated, and no part of the deliverable needed re-deriving. Gotcha (4) (*`measured_bytes` is
not a ceiling*) **is** the deliverable's premise. Gotcha (2) (the results file is stale, re-run in a clone)
stopped a false citation. Gotchas (3) and (6) — `--cut N` retains N, a dry run needs `--force` — were both
used, both correct. The prediction that the retention trim would fall due right after the Phase 0 report
held exactly, for the third consecutive session, and the *"fixed 15,992 B proof"* came in at **15,992 B**.
*What was wrong:* the `CHANGELOG.md` trim instruction ended *"then its fold, in its own commit."* **There is
no fold for this ledger** — the fold rule is `HANDOFFS.md`'s, created by a fixed 7,168 B header reserve this
file does not have; `ls docs/ | grep -i index` returns one file. The instruction was followed into a commit
message that promised a fold no session can perform, and had to be amended. *What was missing:* nothing in
the handoff or the costing block noted that `.context-budget.json` records the same two sizes in **three**
places, which P1 hit immediately — now BL-81. *ROI:* strongly positive; the block saved most of a session.

**Phase 3B — self-assessment 8/10.** *Went well:* the central claim was **tested and the first test said the
opposite** — the A/B diff came back non-empty on a run counter, and a control run of the unchanged side is
what established byte-identity. Both trims were dry-run before writing and both proofs re-run after the
amend. The out-of-scope finding was **opened as BL-81, not fixed**, on S203's own BL-80 precedent. *Went
badly:* the fold error above was mine to catch before writing, not after — the handoff said it, but
`ls docs/` is one command and I ran it only when the commit was already made. *Not done:* P2 is ratified and
unexecuted; BL-81 leaves the config disagreeing with itself in two `_` notes, which is stated in the receipt
rather than hidden.

**Verified:** `quality_ratchet.py --run` in a `--no-local` clone of `43bed33` with HEAD asserted by sha —
`11/11 pass · 0 fail · 0 unmeasured · results 10575dac7361 · manifest 01a4ae7aa511`; `bash bin/tests.sh`
**343 / 0 / 6 skipped**; both shard `.verify.sh` **L1/L2/L3 OK**; `tools/test_context_budget.py` **122 OK**;
`BACKLOG-DETAIL.md.verify.sh` **C1–C5 OK**; `bin/check-links` **111/23**; `bin/check-handoff` **OK**.

**Nothing upstream-facing was taken.** The operator asked to see the proposed comment text for the two
unreviewed pull requests before deciding; drafts went into the close-out report and nowhere else.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [ad hoc] S204 — Phase 3C: fork Learning #88, and the D3 retirement obligation discharged by refusal

- **Appended:** fork Learning **#88** to [`docs/FORK_LEARNINGS.md`](docs/FORK_LEARNINGS.md) — *an instrument
  that records every run changes its own output, so a before/after diff of it carries the instrument's delta
  as well as yours; re-run the UNCHANGED side to tell them apart.* 1,497 B after two trims; the first draft
  was 1,636 B and the second 1,509 B, **both refused by the per-row budget and shortened rather than waived**.
  74 rows, contiguous 15..88.
- **Why this row and not the obvious one:** the session's own near-miss was that P1's central A/B diff came
  back **non-empty** — a growth-run counter reading 166 against 167 — which read once says *the edit changed
  the output*, the exact opposite of what P1 was there to establish. The control run is what settled it.
- **D3 DISCHARGED BY EXPLICIT REFUSAL — no row qualifies, and here are the ones considered**
  ([`CLAUDE.md:38`](CLAUDE.md)). **#82** (a hook fails open) is the only live candidate under criterion (a):
  its lesson *is* mechanized, by `pre-commit-selftest` and `commit-msg-selftest` in `.quality-gates.json` and
  `bin/tests.sh` Test 43. It still does not qualify, on **S200's own adjudicated reasoning** — *"a gate pins
  the instance a lesson came from; the row exists for the next, which has no gate yet"* — and BL-77 is open
  precisely because nothing yet checks a hook is **armed** in a given clone, which is #82's unmechanized
  residual. **#85** (a note describing an enforcement that does not exist) was re-examined directly, since
  BL-78 P1 rewrote the very note it is about: P1 wrote **prose**, not a gate, and the *"a ratchet, not a
  wall"* clause it indicts is still in `files[4]._` — criterion (a) unmet, (c) unmet. **#86** and **#87** are
  one and two sessions old with no gate; **#83** and **#84** are inventory and adjudication lessons no gate
  can hold. Age and file size are not grounds and were not used.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [ad hoc] S204 — BL-81 opened: the config states the same two sizes three times, and P1 could refresh one

- **What:** `.context-budget.json` records `starter-kit/SESSION_RUNNER.md` and `starter-kit/SAFEGUARDS.md`
  sizes in `files[]` **and** in the `_synced` and `_deliberate_exclusions` notes. BL-78 P1's declared scope
  covered the first only, so the file now reads 55,406/17,129 in one place and 54,363/15,386 *(wc -c,
  2026-08-30)* fifteen lines below. Opened rather than fixed, on S203's BL-80 precedent (FM #17).
- **The finding, not the tidying:** `_deliberate_exclusions` exists **because** a prose size went stale, and
  closes with *"Never derive a ceiling from a size written in prose."* The size in that sentence is now
  1,043 B stale, by the identical mechanism, in the identical file. The note carries the lesson and
  reproduces the defect in one breath.
- **No behaviour depends on it** — both are `_` comment keys; `check_synced()` is drift-only by its own
  docstring and `_deliberate_exclusions` is inert prose. What depends on it is the next session that greps:
  `grep 54,363` is how three sessions reached *"over its declared size"*, and after P1 it still hits.
- **Fork-only** — this repository's `.context-budget.json` is its own config, not the distributed seed, so
  nothing reaches an adopter and no upstream PR is involved.
- **Uncosted and unshaped.** A costing session settles whether to refresh the copies (stale again within a
  week — this is the third time) or delete the sizes and cite `files[]`, and whether a guard against a `_`
  note contradicting the key beside it is worth building — the same shape as BL-80's.
- **Verified:** `BACKLOG-DETAIL.md.verify.sh` C1–C5 OK; `bin/check-links` green.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [BL-78] S204 — P1 done: both read-set `measured_bytes` re-measured, and the key now says what it is

- **What:** `.context-budget.json` `files[4]` (`starter-kit/SESSION_RUNNER.md`) and `files[5]`
  (`starter-kit/SAFEGUARDS.md`) carried `measured_bytes` 54,363 and 15,386 with `measured_on` 2026-08-30.
  Both are now **55,406** and **17,129**, `measured_on` **2026-09-20**, and both `_` notes state in terms
  that cannot be misread that **`measured_bytes` is a RECORD, NOT A CEILING** — its only consumer is the
  density-drift warning at `starter-kit/context_budget.py:398`, gated on `status == "ok"`, which neither
  file is. This is P1 of the recommendation in [BL-78's costing block](docs/planning/BACKLOG-DETAIL.md),
  ratified by the operator at this session's Phase 0 picker.
- **Why it was worth a session:** three successive sessions read `SESSION_RUNNER.md` 55,406 / 54,363 as a
  **second breach**. It never was one. The ceiling that refuses anything is `max_bytes` **41,364**, and
  the file is 14,042 B over it **by design** (*"being over on arrival is the POINT"* — a ratchet, not a
  wall). The stale record was manufacturing a breach out of a note to self.
- **Measured two ways, not once:** `wc -c` and `git cat-file -s` on the blobs at HEAD — `9a24b9e`
  55,406 B, `ed49b977` 17,129 B. Agreement of the two is what the entry records, not either alone.
- **THE CLAIM WAS TESTED, NOT ASSERTED.** A `--no-local` clone at `bce7790` (old config) was run against
  the working tree (new config) on an otherwise identical tree: `diff` of the two `--status` outputs is
  **empty** once the growth-run counter is held at the same sequence number by a control run. Every row,
  every status, every advisory, exit 2 both sides. Changing `measured_bytes` by 1,043 B and 1,743 B
  changed **nothing the tool decides** — which is the note's claim, demonstrated rather than argued.
- **Deliberately NOT done:** `max_bytes` and `max_tokens` are untouched on both rows. They **partition**
  the read cap (41,364 + 15,386 = 56,750 = 25,000 tok x 2.27), so re-pinning one re-partitions both; that
  is **P2**, settled by the operator in the same picker as **option β (reported series)** and left for its
  own session. `git diff` shows exactly six changed key paths: `/files[4]/_`, `/files[4]/measured_bytes`,
  `/files[4]/measured_on` and the three matching `files[5]` paths — walked object-to-object, not eyeballed.
- **Verified:** `python3 tools/test_context_budget.py` **Ran 122 tests, OK**; `python3
  starter-kit/context_budget.py` exit **2** with the same four `over` rows — the verdict is unchanged,
  which is what P1 predicted it would be.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-20 · [BL-78] S204 claim — P1: re-measure both `measured_bytes`, and say what that key is (in progress)

**Deliverable:** **BL-78 phase P1**, as recommended by S203's costing block
([`docs/planning/BACKLOG-DETAIL.md:2866`](docs/planning/BACKLOG-DETAIL.md)) — re-measure both read-set
`measured_bytes` keys in `.context-budget.json` and state in each `_` note that `measured_bytes` is a
**record, not a ceiling** (its only consumer is the density-drift warning at
`starter-kit/context_budget.py:398`, gated on `status == "ok"`). Chosen by the operator after Phase 0
(picker) over BL-78 P2, BL-77's costing and BL-80's.

**Scope, stated so the close-out can be checked against it.** Two `measured_bytes` values, their two
`measured_on` dates, and the record-vs-ceiling clause in their two `_` notes. **`max_bytes` and
`max_tokens` are not touched** — they are the partition (41,364 + 15,386 = 56,750), and re-partitioning
is P2, which the operator has settled as **β (reported series)** but which is a separate session.

**Operator decision recorded in the same picker:** BL-78 **P2 = option β** — convert
`starter-kit/SAFEGUARDS.md`'s row to a reported series on BL-53 option C's precedent, rather than α's
re-pin-and-re-partition. Not executed here.

**Also approved in the picker, each its own action:** the scoped `CHANGELOG.md` trim
(`--cut 2026-09-19`), the owed `HANDOFFS.md` retention trim (`--cut 2`), and the fork `origin` push.
**Nothing upstream-facing was approved** — the operator asked to see the proposed #85/#83 comment text
before deciding.

