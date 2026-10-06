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

---

## 2026-09

## 2026-10

### 2026-10-06 · [BL-95] S270 — R1 fix-up F3: `CLAUDE.md` says 29 failure modes and v4.1, and `docs/RELEASE_HISTORY.md` gains v3.8, v4.0 and v4.1 (D6)

`CLAUDE.md`: "documents 28 failure modes" → 29 (the runner's table now ends at `| 29 |`); a Starter Kit row for the `starter-kit/gitattributes` seed and a Tools row for the three structural checkers (the second says this fork's `check-ledger` gate reads the live ledger, F2); the pointer's "from v1.0 to v3.7" → "to v4.1". The "Current version" line needed no edit: it auto-merged to upstream's v4.1, which is D6's target (v4.2 is tagged but its release docs are PR #92, still open). `docs/RELEASE_HISTORY.md`: the v3.8, v4.0 and v4.1 bullets lifted verbatim from `upstream/main:CLAUDE.md` lines 118, 120 and 122 (checked line for line; none carries a relative link). This is a documentation correction, not a fork release or tag. `CLAUDE.md` is 15,029 B (resident ceiling 18,600 B); `bin/check-links` OK (116 links).

### 2026-10-06 · [BL-95] S270 — R1 fix-up F2: the `check-ledger` gate and Test 50's real-ledger assertion read the live ledger (D3)

Upstream's gate runs `bin/check-ledger --all`; on this fork's tree that reports one finding, `docs/archive/CHANGELOG-through-2026-08-11.md:609` (a 2026-08-10 heading carrying two source tags), in a proof-locked shard that cannot be edited without breaking its `.verify.sh`. Per D3 (A, the operator's, 2026-10-06) the gate's command is now `bin/check-ledger` (threshold 0 and direction `max` unchanged), `bin/tests.sh` Test 50's last assertion (upstream's Test 31, renumbered) reads the live ledger the same way, and a `_fork_d3_check_ledger_scope_bl95` note in `.quality-gates.json` says why. Measured: `bin/check-ledger --all` exit 1 with that one finding; `bin/check-ledger` exit 0 (OK, 1 file). `quality_ratchet.py --precommit` exits 0. Not yet run: the suite and the gates on this tip (the R1 verification in a `--no-local` clone).

### 2026-10-06 · [BL-95] S270 — R1 fix-up F1: dashboard 2.20.0 and the `.gitattributes` seed as installed content (D5)

`DASHBOARD_VERSION` 2.19.0 → 2.20.0 in both twins (a changed output on a distributed tool is MINOR; the fork's line stays apart from upstream's 2.11.3), and the `.gitattributes` seed gets its row and a three-string signature set in `_FRAMEWORK_INSTALLED_CONTENT`, after `.quality-gates.json` (the manifest's order). `tools/test_methodology_dashboard.py`: the two version pins follow and the population guard goes 6 → 7, deliberately, as S177 raised 4 → 6. `python3 tools/test_methodology_dashboard.py`: 353 tests OK in 52.8 s (the plan's trial read 353 with one red before the guard was raised); the twins are `cmp`-identical.

### 2026-10-06 · [BL-95] S270 — R1: `upstream/main` `f34769f` (v4.2) merged into fork `main` (`2ed9262`)

One `--no-ff` merge of 102 upstream commits (merge base `77afc12`), local only: nothing pushed, no PR or comment. The 17 conflicting files were resolved as `docs/planning/upstream-resync-2026-10-plan.md` §2.3 says (ours for `.context-budget*`, `bin/check-learnings` and the CHANGELOG shard; theirs for `bin/status`, `bin/sync`, `starter-kit/BOOTSTRAP.md`; hunk letters for the hook, the gates, `README.md`, `CLAUDE.md`, the dashboards and `bin/tests.sh`, whose upstream Tests 27-34 are Tests 46-53 here and upstream's Test 26 is Test 41), and both ledgers by `fold-ledger.py`: 118 upstream entries folded into this ledger and 17 upstream receipts appended to `HANDOFFS.md` (20 receipts). The re-derived conflict set at pre-flight was the plan's 17 paths; #92 and #94 were still open. Measured at the merge commit: the shard `docs/archive/CHANGELOG-through-2026-09-30.md` has an empty diff against the first parent and its `.verify.sh` exits 0 (L1, L2/front-matter, L3); `bin/check-ledger` OK; `bin/check-handoff --all --allow-pending` OK on 20 receipts. Two deviations from §5: BOOTSTRAP's never-overwrite row edit (`.gitattributes`, "those seven") is inside the merge commit, not F1, because Test 28 pins that row to the manifest; and `CLAUDE.md`'s "Current version" line auto-merged to v4.1 (D6's target), so F3 only lifts the release history. A merge commit has no ledger entry of its own (the hook skips merges); this entry, in the first commit after it, records it. A backup ref `pre-resync-2026-10` (local, at `9904a0a`) holds the pre-merge tip.

### 2026-10-06 · [BL-95] S270 claim (in progress) — R1: the resync merge of `upstream/main` into fork `main`

CHANGELOG: pending. Operator said `go` as the first message and chose "R1: BL-95 resync" at the Phase 0 picker; he also declined the push of `c31d478` for now. The deliverable is plan section 5's R1 (pre-flight, one `--no-ff` merge, the 17 resolutions, both ledgers folded, fix-ups F1-F4, verification in a `--no-local` clone), local only: nothing is pushed or sent. The owed trim (`2291af5`, S267's receipt to shard `HANDOFFS-through-2026-10-05-5.md`, its `.verify.sh` exit 0 by name from a `--no-local` clone) and its fold (`3d83923`) ran first as their own actions; `bin/tests.sh` on the fold tree read 359 passed, 0 failed, 6 skipped. Phase 3F records the rest.

### 2026-10-06 · [ad hoc] S270 — fold the fifth 2026-10-05 HANDOFFS shard pointer into the archive index

The pointer block the trim (`2291af5`, S267's receipt to `HANDOFFS-through-2026-10-05-5.md`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, 2026-10-05, trimmer v1.7.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S269, S268); the shard's `.verify.sh` was run by name from a `--no-local` clone of the trim commit and exited 0 (L1, L2/front-matter, L3). Ran after the Phase 0 report and the operator's choice of R1 (the BL-95 resync, executor session 1), before the session claim.

### 2026-10-06 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-05-5.md` (1 record(s), 35,532 B → 24,642 B)

**Written by:** `methodology_trim.py` v1.7.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-05 → 2026-10-05) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-05-5.md`](docs/archive/HANDOFFS-through-2026-10-05-5.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-05-5.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-05-5.md.verify.sh)
rather than trusting a digest printed here. Live file 35,532 B → 24,642 B (−30.6%).

### 2026-10-06 · [BL-95] S269 -- D1–D7 recorded: the operator took every recommendation at the close-out picker

He answered the seven decisions of `docs/planning/upstream-resync-2026-10-plan.md` §3 after the close-out report, **each as
recommended**: D1 one merge and two executor sessions; D2 fold upstream's 118 unseen `CHANGELOG.md` entries into the
live ledger (`fold-ledger.py`) and keep the fork's shard byte-identical; D3 scope the `check-ledger` gate and the one
real-ledger assertion to the live ledger; D4 adopt the never-edit hook gate; D5 `DASHBOARD_VERSION` 2.20.0; D6 state v4.1
and lift v3.8, v4.0 and v4.1 into `docs/RELEASE_HISTORY.md` (no fork release or tag); D7 count BL-96's skip. This commit
records them in the plan (status line and a "Decided" paragraph at §3), in the `BL-95` row (`docs/planning/BACKLOG.md:180`)
and in the receipt's `next_steps` (1) and (5), which the close-out commit had written before the answers. He also approved
the push; it ran, see the entry below. **The executor sessions R1 and R2 are not started and need his commission.**
Local only: this commit is not pushed, and the next push is his go-ahead.

### 2026-10-06 · [ad hoc] S269 -- fork main pushed to origin, on his go-ahead at the close-out picker

`git push origin 5f302c0:refs/heads/main` took `ab171c3..5f302c0`, exactly the six commits he named at the picker
(`d0bb866`, `0316eb6`, `f203159`, `352b544`, `aa8ae69`, `5f302c0`). Guards checked first: on `main`, tree clean, no
`.git/REBASE_HEAD`, `origin/main` an ancestor of `main` (a fast-forward). **Read back:** `git ls-remote origin
refs/heads/main` = `5f302c0d18e46a242f9aa1e72f10ef883502e5b9` = local `main`, and `git rev-list --left-right --count
origin/main...main` read `0 0` after a re-fetch. Nothing went to `KJ5HST/methodology`.

### 2026-10-06 · [BL-95] S269 close-out — the resync plan is written and reviewed; the receipt is complete; D1–D7 await his answers

`CHANGELOG: pending` on the S269 claim entry is cleared. **Deliverable:** `docs/planning/upstream-resync-2026-10-plan.md`
(commit `aa8ae69`, evidence `352b544`), a DRAFT with seven decisions of his and two executor phases; nothing was
merged, rebased, pushed or sent. The `HANDOFFS.md` receipt (self-score 7; predecessor S268 scored 9, every line
citation exact) replaces the pending claim stub; `bin/check-handoff` and `--all` pass at three receipts, so the
retention trim (`--cut 2 --force`) is owed after the next Phase 0 report. **Gate run on this close-out's tree
(started in the background, head `aa8ae69`): 12/12 pass, results `e30853a7b148`**, identical to S268's citation.
Phase 3C appended no fork learning row (considered: #67, #69, #90, #102, #103). The project memory notes were
updated outside the repository. No push: `origin/main` is 0 behind and 6 ahead with this commit, and each push is
his go-ahead.

### 2026-10-06 · [BL-95] S269 — the resync plan written: `docs/planning/upstream-resync-2026-10-plan.md` (DRAFT; D1–D7 are the operator's)

**The deliverable of S269**, a planning session resumed after its first conversation stopped at the claim. Fork
`main` is 102 commits behind `upstream/main` `f34769f` (tag `v4.2`) from merge base `77afc12`; 17 files conflict, 6
auto-merge, 22 arrive untouched, and the fork's trimmer work (PR #94) merges clean. A scratch trial merge reached
**451 passed / 1 failed** on `bin/tests.sh` (365 / 0 today) and 11 of 13 gates; the one red is `check-ledger --all`
reading a frozen shard. It found four traps the diff does not show: the order of the fork's Tests 42–45 inside the
hunk that holds the tail of the test being replaced; upstream's same-named shard (kept out, its entries folded);
the `../../` links in shard-sourced entries (the trimmer refuses them); and a hook that refuses a practice fork
sessions used. Recommended: one merge, two executor sessions; seven decisions. **An independent read-only review
re-derived about 215 claims and found 14 wrong, 10 imprecise and 6 omissions, one of them high** (the first fold
script folded nothing amid a real merge's conflict markers); each substantive one was re-run and the plan and the
script corrected (plan §8). Also in this commit: the `BL-95` row rewritten (it still said 89 behind and "#91
open"), `BL-96`'s pointer now names D7, and the two history lines Phase 0 appended
(`dashboard_history.jsonl`, `.context-budget-history.jsonl`). Nothing merged, rebased, pushed or sent.

### 2026-10-06 · [BL-95] S269 — evidence for the resync plan: the ledger-fold script, the stage table, the trial's suite and gate logs

Four files under `docs/planning/upstream-resync-2026-10-evidence/`, committed ahead of the plan that cites them.
**`fold-ledger.py`** (`changelog` and `handoffs` modes) performs the two non-mechanical ledger resolutions of the
resync merge: it folds the 118 upstream `CHANGELOG.md` entries the fork lacks into the live ledger by date (386
entries, 415,398 B), undoing the `../../` link rebase on entries that came from upstream's shard, and appends the 17
upstream receipts the fork holds in no shard to `HANDOFFS.md` (20 receipts, 114,995 B). It reads the fork's side
from git, not the working tree, because the first version read the working tree and folded nothing amid a real
merge's conflict markers; the final form was run in a real conflicted `git merge --no-commit` and reproduced the
trial's two ledgers byte for byte. **`stages.tsv`** is the 69-row run of `git merge-tree` over each first-parent
upstream commit. **`trial-suite.log`**: `bin/tests.sh` on a scratch merge with both ledgers folded, 451 passed,
1 failed, 0 skipped (the one red row is `check-ledger --all` reading a frozen shard). **`trial-gates.log`**:
`quality_ratchet.py --run` on the same merge, 11 of 13 gates (the same finding, twice). Nothing was merged,
rebased or pushed; the trial ran in scratch clones outside the repository.

### 2026-10-05 · [BL-95] S269 claim (in progress) — the resync plan: catching fork `main` up with `upstream/main`

CHANGELOG: pending. Operator said `go` as the first message and chose "BL-95 resync plan" at the Phase 0 picker. The deliverable is a plan document in `docs/planning/`, not a resync: nothing is merged, rebased or pushed, and nothing goes to `KJ5HST/methodology`. The owed trim (`d0bb866`, S266's receipt to shard `HANDOFFS-through-2026-10-05-4.md`, its `.verify.sh` exit 0 by name from a `--no-local` clone) and its fold (`0316eb6`) ran first as their own actions; `bin/tests.sh` on the fold tree read 359 passed, 0 failed, 6 skipped. Phase 3F records the rest.

### 2026-10-05 · [ad hoc] S269 — fold the fourth 2026-10-05 HANDOFFS shard pointer into the archive index

The pointer block the trim (`d0bb866`, S266's receipt to `HANDOFFS-through-2026-10-05-4.md`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, 2026-10-05, trimmer v1.7.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S268, S267); the shard's `.verify.sh` was run by name from a `--no-local` clone of the trim commit and exited 0 (L1, L2/front-matter, L3). Ran after the Phase 0 report and the operator's choice of the BL-95 resync plan, before the session claim.

### 2026-10-05 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-05-4.md` (1 record(s), 38,618 B → 26,919 B)

**Written by:** `methodology_trim.py` v1.7.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-05 → 2026-10-05) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-05-4.md`](docs/archive/HANDOFFS-through-2026-10-05-4.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-05-4.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-05-4.md.verify.sh)
rather than trusting a digest printed here. Live file 38,618 B → 26,919 B (−30.3%).

### 2026-10-05 · [ad hoc] S268 -- fork main pushed: `origin/main` `c8215af` to `0044313` (149 commits)

Pushed with his go-ahead at the S268 Phase 0 picker ("Push fork main to origin"). Guards run first: branch `main`, remote `https://github.com/rmsharp/methodology.git` (the fork, not `KJ5HST/methodology`), 0 behind and 149 ahead, `origin/main` an ancestor of `main` (a fast-forward). Read back after: `git ls-remote origin refs/heads/main` and local `main` both `0044313`, and `git rev-list --left-right --count origin/main...main` read `0 0`. `main` is still 102 behind `upstream/main`. Nothing went to `KJ5HST/methodology`: no comment, issue, PR edit or push to PR #94's branch.

### 2026-10-05 · [BL-97] S268 close-out — BL-97 converted and closed; the receipt is in `HANDOFFS.md`

Deliverable done: Test 45 derives the silent early-exit flake form (25 sites, RED before the sweep, GREEN after) and the sweep converted all 25; N3 and N6 were also dead without any flake and are live now. `bin/tests.sh` 365 passed, 0 failed, 0 skipped; gates 12/12 (results `e30853a7b148`); `HANDOFFS.md` holds 3 receipts, so a trim is owed after the next Phase 0 report. No fork learning row appended (Test 45 enforces the lesson from birth). He approved a push of fork `main` to `origin`; it runs after this commit and has its own entry. Nothing is sent to `KJ5HST/methodology`: no comment, issue, PR edit or push to PR #94's branch.

### 2026-10-05 · [BL-97] S268 — close BL-97 in the backlog files

`BACKLOG.md` loses the BL-97 index row and its id joins the closed-id list; `BACKLOG-COMPLETED.md` gains the closing row (4 closures since the move); `BACKLOG-DETAIL.md` §BL-97 records the outcome, including the population correction (25 sites, not the 16 S265 counted) and the second, flake-free hole at N3 and N6. `BACKLOG-COMPLETED.md.verify.sh` OK (C6: all 4 later closures findable), `BACKLOG-archive-2026-08-15.md.verify.sh` OK, `bin/check-links` OK (111 links). The work itself is `47f76d2`.

### 2026-10-05 · [BL-97] S268 — `bin/tests.sh`: 25 hidden-form sites converted and a scanner (Test 45) that keeps the form out

A flake on an early-exiting consumer (`grep -q`, `grep -m`, `head`, `sed q`) under `pipefail` reads as a pass wherever the pipeline guards a `fail` arm, so a real defect goes green. Test 45 derives that population over whole logical lines whatever the producer (Rule A: the consumer ahead of `&& fail`; Rule B: in the condition of an `if` whose then-arm calls `fail`), was RED on the tree it was written against with **25 sites** (the S265 count of 16 was keyed to `echo`/`printf` heads and missed 3 chains and 6 `if` forms), and is GREEN after the sweep. Cures: a here-string where the producer heads the pipeline (20 sites); the 3 chains headed by a here-string with their early-exiting consumer dropped (`grep PAT >/dev/null`); the output captured where the producer is the command under test (`bin/check-handoff`, 2 sites). **N3 and N6 (`:984`, `:1014`) were dead for a second reason that needs no flake:** `check-handoff` exits 1 exactly when its output names the pattern, `pipefail` makes the pipeline's status the producer's, and the `then` arm was unreachable; on a fixture that really violated N6 the old construct took the else arm and the new one reaches the then arm. Every edit is one line, so no line number in `bin/tests.sh` moved. The scanner is proven on a fixture (7 marked hidden lines flagged, 9 visible, converted, captured, quoted and commented lines not) and on the real file (a converted site reverted on a copy is named). Not changed: the 62 `&& pass || fail` sites (a flake there is a loud false red, under the rerun rule), the 3 `if ... then pass ... else fail` sites, and a negated pipeline, which has no instance today. `bin/tests.sh` 365 passed, 0 failed, 0 skipped at three receipts.

### 2026-10-05 · [BL-97] S268 claim (in progress) — convert the silent `echo | grep -q` sites in `bin/tests.sh`, scanner first

CHANGELOG: pending. Operator said `go` as the first message, chose "BL-97: convert the 16 sites" at the Phase 0 picker, then, shown that a whole-logical-line, every-producer re-derivation finds 25 hidden-form sites (19 `&& fail || pass` chains and 6 `if ... then fail ... else pass`), chose all 25. He also approved pushing fork `main` to `origin`. The owed trim (`bf42d66`, S265's receipt to shard `HANDOFFS-through-2026-10-05-3.md`, its `.verify.sh` exit 0 by name from a `--no-local` clone) and its fold (`55454ff`) ran first as their own actions; `bin/tests.sh` on the fold tree read 356 passed, 0 failed, 6 skipped. Phase 3F records the rest.

### 2026-10-05 · [ad hoc] S268 — fold the third 2026-10-05 HANDOFFS shard pointer into the archive index

The pointer block the trim (`bf42d66`, S265's receipt to `HANDOFFS-through-2026-10-05-3.md`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, 2026-10-05, trimmer v1.7.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S267, S266); the shard's `.verify.sh` was run by name from a `--no-local` clone of the trim commit and exited 0 (L1, L2/front-matter, L3). Ran after the Phase 0 report and the operator's choice of BL-97's conversion, before the session claim.

### 2026-10-05 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-05-3.md` (1 record(s), 40,363 B → 28,794 B)

**Written by:** `methodology_trim.py` v1.7.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-05 → 2026-10-05) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-05-3.md`](docs/archive/HANDOFFS-through-2026-10-05-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-05-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-05-3.md.verify.sh)
rather than trusting a digest printed here. Live file 40,363 B → 28,794 B (−28.7%).

### 2026-10-05 · [issue #93] S267 — P4 sent: the branch is on origin and PR #94 is open against KJ5HST/methodology

Non-commit actions, after the S267 close-out report, each with his go-ahead (a two-item picker: "Push branch to origin", "Open the PR upstream"; he selected both). Pre-flight: `git fetch upstream` read `f34769f` (unchanged, and the branch's merge base), PR #92 had no comments or reviews, issue #93 still carried only our comment, no branch of that name on `origin`. **Push:** `fix/trim-verify-false-red-issue93` to `origin`, remote tip `972eb2cd6263` read back with `git ls-remote --heads origin` and equal to the local tip. **Pull request:** <https://github.com/KJ5HST/methodology/pull/94>, from `rmsharp:fix/trim-verify-false-red-issue93` to `main`, title "fix(trim): generated proofs stop reading red on lossless trims, and --reverify re-derives a frozen one (refs #93)", body `docs/planning/issue93-evidence/upstream-pr-body.md` minus its leading HTML comment (read back through `gh pr view`: identical but for a trailing newline). GitHub reads it OPEN, not a draft, MERGEABLE, 3 commits, 5 files, +1641/-23, head `972eb2c`, no check runs reported. **Not sent:** any comment on #92, #93 or #94. This entry corrects the S267 close-out entry and receipt, which said nothing was pushed or sent: that was true when they were written and the receipt's `active_task`, `next_steps`, `gotchas` and `commit` now say what happened. `main` itself is not pushed (0 behind, 143 ahead of `origin/main` after this commit).

### 2026-10-05 · [issue #93] S267 close-out — P4's inward half of the trimmer false-red fix: the upstream pull request is built and vetted on a local branch; nothing pushed or sent

Deliverable: the one upstream pull request for issue #93, vetted here first. The local branch `fix/trim-verify-false-red-issue93` is three commits on `upstream/main` `f34769f` (`68d8a06` the L2 leak 1.5.1, `965f136` the stub finalize 1.6.0, `972eb2c` `--reverify` 1.7.0), built in a scratch clone under upstream's own hooks; the body is drafted in `docs/planning/issue93-evidence/upstream-pr-body.md` and not sent. The owed trim (`33c9d0e`, S264's receipt to `HANDOFFS-through-2026-10-05-2.md`, proof exit 0 by name from a `--no-local` clone) and its fold (`3fe4fab`) ran first, the claim is `4bc368c`, the work entry is `f2ba0b9`. Largest finding: six lines of the fork's code and tests cite things that exist only here, one inside `VERIFY_TEMPLATE` where it would have been written into every adopter's new proofs; reworded in the branch only. The adopter's 54 proofs through the branch's trimmer: 46 at exit 0, 7 at exit 1, 1 at exit 4, 0 newly red. **A correction to this session's own record:** the claim commit `4bc368c` put the Phase 1B stub inside a code span of the `HANDOFFS.md` preamble (an insert keyed on `str.index` of a fence token that the prose also names), so the breadcrumb was unparseable for the whole session; I ran neither `bin/tests.sh` nor `bin/check-handoff` after the claim and found it at close-out, when the checker printed OK with "0 older receipts". The close-out commit restores the preamble from `3fe4fab` and places the receipt above S266. The `HANDOFFS.md` receipt is complete (`self_score` 7, S266 scored 9). Phase 3C appended no fork learning row (row 76 already states the class), so D3's retirement duty does not arise. Non-commit actions: a local branch ref created in this repo; nothing git-pushed, no pull request opened, nothing sent to `KJ5HST/methodology`.

### 2026-10-05 · [issue #93] S267 — P4 inward: the upstream pull request is built and vetted on a local branch; nothing pushed or sent

The local branch `fix/trim-verify-false-red-issue93` is three commits on `upstream/main` `f34769f` (`68d8a06` the L2 leak 1.5.1, `965f136` the stub finalize 1.6.0, `972eb2c` `--reverify` 1.7.0), each with its tests, an upstream-form `CHANGELOG.md` entry and its `trimmer-unit-tests` floor (124 to 129 to 154 to 181); `git ls-remote --heads origin` lists no such branch. Built in a scratch clone with `core.hooksPath .githooks` so upstream's own hooks bound each commit (they refused an `--amend` of a committed ledger entry; I soft-reset and recommitted). Upstream's trimmer and test file were byte-identical to this fork's pre-P1 blobs, so the five fork commits' changes applied clean. **Six lines of the fork's code cite things that exist only here** (`the plan's D2` three times, `fork Learning #58` twice, `P1's`/`P2's` once), one inside `VERIFY_TEMPLATE` where it would have reached every adopter's new proofs; they are reworded in the branch only, so the branch's trimmer and test blobs differ from the fork's by exactly those six lines. The branch's third entry first said "two payload tests"; there are four, corrected before anything was published (this fork's own P3 entry says "two" and stays as written). Measured: 129, 154, 181 tests at the three commits; `quality_ratchet.py --run` 12/12 on `2922236` (results `84dd2247150f`; the tip differs by four `CHANGELOG.md` lines); the adopter's 54 proofs (fresh clone at `82433662`) through the branch's trimmer 46 at exit 0, 7 at exit 1, 1 at exit 4, 0 newly red, 2 newly green, tree identical; upstream's own `HANDOFFS.md` (38 receipts, 221,642 B against a 196,608 B trigger) force-trimmed in a throwaway clone, proof exit 0; claim stub then finalize-and-trim in one commit gives `FRONTIER_PENDING_STUB` and then the named exit 4; `bin/sync` delivers the trimmer and the apparatus byte-identical; no merge conflict with #92. New: `docs/planning/issue93-evidence/upstream-pr-body.md`, the pull request body, drafted and not sent. Plan §5 P4, the BL-98 row and its detail say what was and was not verified. **Not done:** pushing the branch, opening the pull request, any comment on #93 or #92, BL-95. Each of those is his go-ahead.

### 2026-10-05 · [issue #93] S267 claim (in progress) — P4 inward: vet the one upstream pull request for the trimmer false-red fix (P1–P3), send nothing

CHANGELOG: pending. Operator said `go` as the first message and chose "P4 inward vetting" at the Phase 0 picker. The owed trim (`33c9d0e`, S264's receipt to shard `HANDOFFS-through-2026-10-05-2.md`, its `.verify.sh` exit 0 by name from a `--no-local` clone) and its fold (`3fe4fab`) ran first as their own actions; `bin/tests.sh` on the fold tree read 356 passed, 0 failed, 6 skipped. Deliverable: P1–P3 applied as one patch to a scratch clone of `upstream/main`, the suite run there, the `FRAMEWORK_APPARATUS.md` paragraph re-derived against upstream's copy, adopter impact stated, the pull request body drafted and shown inline. Nothing is pushed, opened or commented; sending is the operator's separate go-ahead. Phase 3F records the rest.

### 2026-10-05 · [ad hoc] S267 — fold the second 2026-10-05 HANDOFFS shard pointer into the archive index

The pointer block the trim (`33c9d0e`, S264's receipt to `HANDOFFS-through-2026-10-05-2.md`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, 2026-10-05, trimmer v1.7.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S266, S265); the shard's `.verify.sh` was run by name from a `--no-local` clone of the trim commit and exited 0 (L1, L2/front-matter, L3). Ran after the Phase 0 report and the operator's choice of P4 (the inward half of the one upstream pull request for the #93 trimmer fix), before the session claim.

### 2026-10-05 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-05-2.md` (1 record(s), 40,124 B → 29,473 B)

**Written by:** `methodology_trim.py` v1.7.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-05 → 2026-10-05) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-05-2.md`](docs/archive/HANDOFFS-through-2026-10-05-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-05-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-05-2.md.verify.sh)
rather than trusting a digest printed here. Live file 40,124 B → 29,473 B (−26.5%).

### 2026-10-05 · [issue #93] S266 close-out — P3 of the trimmer false-red fix is committed: a read-only `--reverify <shard>` re-derives a frozen proof under today's template (`TRIM_VERSION` 1.7.0)

Deliverable: P3 of `docs/planning/issue93-trimmer-proof-false-red-plan.md`: the implementation `3616b5f`, the floor `3e94b28`, the evidence scripts `f8281d4` and the status `862156f`; the owed trim (`2e5ed83`) and its fold (`b50cd24`) ran first, the claim is `48462e1`. 27 tests written first and RED (181 in the file), 54 mutants killed on the final tree (a first run of 56 left three survivors, each traced: two guards no input could fail, deleted, and one missing test, added), `bin/tests.sh` 362 passed, 0 failed. Both real trees re-derived through the shipped CLI and agreeing with S265's in-memory re-derive on every shard (this repo 103 green, 2 at exit 1, 1 at exit 4 of 106; the adopter 46, 7, 1 of 54; 0 newly red; nothing written), and an end-to-end smoke from a `--no-local` clone. Deviations from the plan, on evidence: the lift is strict (the plan's regexes would have made a read-only inspection a code-execution path), `--reverify` refuses every flag that writes or selects a ledger, and one sentence in `FRAMEWORK_APPARATUS.md` names the flag. The `HANDOFFS.md` receipt is complete (`self_score` 8, S265 scored 9). Phase 3C appended no fork learning row, so D3's retirement duty does not arise. Nothing pushed; nothing sent to `KJ5HST/methodology`.

### 2026-10-05 · [BL-98] S266 — status follows P3 in the #93 plan, the BL-98 row and its detail

`docs/planning/issue93-trimmer-proof-false-red-plan.md` gets a measured P3 DONE paragraph in §5 and a new status line (the S263 paragraph is left as written); the BL-98 row in `docs/planning/BACKLOG.md` and its section in `docs/planning/BACKLOG-DETAIL.md` now read P3 DONE and name P4 as the next action. The differences from the plan's prediction are in the plan, not edited into it: the adopter reads 2 green + 1 exit-4 + 7 exit-1 (as P2 measured), this repo 103 + 1 + 2 of 106.

### 2026-10-05 · [BL-98] S266 — the P3 sweep and mutation scripts join `issue93-evidence/`

`docs/planning/issue93-evidence/reverify_p3.py` sweeps every frozen proof in a repository through the shipped `--reverify`, one process per shard, and checks the tree is identical afterwards (every file by size and mtime, every directory outside `.git`, `git status --porcelain`, HEAD, the refs, the stash list); `mutants_p3.py` is the 54-mutant check of the new code (`--validate` checks the list in a second, `--only=<name substring>` reruns some). Both write nothing under the repository.

### 2026-10-05 · [issue #93] S266 — tighten `trimmer-unit-tests` 154 → 181 in `.quality-gates.json`

The 27 tests P3 added (`3616b5f`: `TestReverify`, covering the lift, every refusal, the two payload attacks with their controls, the writes-nothing snapshot, the frozen-red-to-green and pre-stub-label cases, and the prose pin) are now a floor: `python3 tools/test_methodology_trim.py` reads `Ran 181 tests`, OK (skipped=2), the gate's own command and extract. A tightening, so no approval is owed (`SAFEGUARDS.md` Blast Radius); the precedent is `7a18512` (129 → 154). The mechanical half of Phase 3C: the tests that pin `--reverify`'s refusals cannot silently drop.

### 2026-10-05 · [issue #93] S266 — P3: `methodology_trim.py --reverify <shard>` re-derives a frozen proof under today's template, read-only (`TRIM_VERSION` 1.7.0)

`starter-kit/methodology_trim.py` gains `--reverify <shard>` (the shard or its `.verify.sh`): it lifts `LIVE`, `SHARD` and the record grammar out of the frozen proof, fills the CURRENT `VERIFY_TEMPLATE` through the new `render_verify` (`build_verify` is now a spec-to-values wrapper over it, so there is one filler), runs it, and prints the verdict under a banner saying it is a claim about today's logic and not the artifact that was shipped. It writes nothing and leaves the frozen proof alone. Exit is the proof's own (0 holds, 1 a FAIL, 4 a recognised stub finalize) or 3 for a shard it will not re-derive; a signal death reads as 3, never as a pass. The lift is strict because the text is spliced into an unquoted shell assignment and into Python the proof executes: each of the six required lines (`LIVE`, `SHARD`, `RECORD_KIND`, `RECORD_START`, `FENCE_INFO`, `FOOTER_MODE`) must match, whole, the form the template writes, `REGEN_PATTERNS` and `STUB_PATTERN` are parsed as literals and never evaluated, paths may not be absolute or contain `..`, and anything else is refused by name (`REVERIFY_NOT_LIFTABLE`, `REVERIFY_NO_PROOF`, `REVERIFY_SHARD_MISMATCH`, `REVERIFY_CANNOT_RUN`). A proof that predates a line gets today's value and the banner says so (`REVERIFY_SUBSTITUTED`): no regenerated fields before 1.1.2, and the stub marker from the ledger table by the live basename before 1.6.0. `--reverify` refuses to be combined with any flag that writes or selects a ledger. 27 tests in `TestReverify`, written first (RED against the missing flag), 181 in the file; the two payload tests drive the attack and carry a control showing the naive splice really runs it. Measured on the real trees: this repo's 106 frozen proofs re-derive 103 green, 2 at exit 1, 1 at exit 4 (5 frozen red, 2 newly green, 0 newly red); the adopter's 54 (read through a clone) re-derive 46 green, 7 at exit 1, 1 at exit 4 (10 frozen red, 2 newly green, 0 newly red); both match S265's measured prediction and the in-memory prototype shard for shard; the tree is identical afterwards. 54 mutants of the new code, all killed on the final tree (a first run of 56 found three survivors: two guards that no input could fail, removed, and one missing test, added). One sentence in `FRAMEWORK_APPARATUS.md` names the flag. Nothing sent upstream, nothing pushed.

### 2026-10-05 · [issue #93] S266 claim (in progress) — P3 of the trimmer false-red fix: a read-only `--reverify <shard>`

CHANGELOG: pending. Operator said `go` as the first message and chose "P3 --reverify" at the Phase 0 picker. The owed trim (`2e5ed83`, S263's receipt to shard `HANDOFFS-through-2026-10-05.md`, its `.verify.sh` exit 0 from a `--no-local` clone) and its fold (`b50cd24`) ran first as their own actions; `bin/tests.sh` on the fold tree read 356 passed, 0 failed, 6 skipped. Deliverable: tests first, then `--reverify <shard>` in `starter-kit/methodology_trim.py` (`TRIM_VERSION` 1.7.0), per the plan approved at S263. Phase 3F records the rest.

### 2026-10-05 · [ad hoc] S266 — fold the 2026-10-05 HANDOFFS shard pointer into the archive index

The pointer block the trim (`2e5ed83`, S263's receipt to `HANDOFFS-through-2026-10-05.md`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, 2026-10-05, trimmer v1.6.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S265, S264); the shard's `.verify.sh` was run from a `--no-local` clone of the trim commit and exited 0 (L1, L2/front-matter, L3). Ran after the Phase 0 report and the operator's choice of P3 (`--reverify`) of the #93 trimmer fix, before the session claim.

### 2026-10-05 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-05.md` (1 record(s), 40,122 B → 28,417 B)

**Written by:** `methodology_trim.py` v1.6.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-05 → 2026-10-05) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-05.md`](docs/archive/HANDOFFS-through-2026-10-05.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-05.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-05.md.verify.sh)
rather than trusting a digest printed here. Live file 40,122 B → 28,417 B (−29.2%).

### 2026-10-05 · [BL-97] S265 — decision reversed: BL-97 is REOPENED, shape (b), the 16 `&& fail || pass` sites

Asked to re-explain the "leave it" decision recorded earlier this session, I re-derived the population over whole logical lines: 86 `echo | grep -q` sites, 62 `&& pass || fail`, 16 `&& fail || pass`, 8 `if` forms (S254's 82 was a per-line count). The rationale I had given for leaving it, that no red had hidden a defect, was survivorship: the hidden form cannot show as a red. The operator, from a second picker, chose to REOPEN and convert the 16 (a flake there reads a defect as green). Recorded, not done: `docs/planning/BACKLOG.md` row BL-97 and `docs/planning/BACKLOG-DETAIL.md` §BL-97 (a paragraph that supersedes the "leave it" one, with the 16 line numbers and the next action), and the S265 receipt's `next_steps` item (4). The earlier ledger entry ("decision: leave the flake") is committed and is not edited; this entry corrects it. No change to `bin/tests.sh`; the conversion is a future session's own deliverable. No outward action.

### 2026-10-05 · [BL-97] S265 — decision: leave the `echo | grep -q` flake; the S257 decision (c) stands

After the close-out report the operator was asked, in a picker, whether BL-97's reopen condition ("the count of such reds grows") was met by this session's two reds in one full run (Test 15, Test 38; four reds across three runs) and chose to LEAVE it over (b) converting only the `&& fail || pass` sites and (a) converting all 82. `docs/planning/BACKLOG-DETAIL.md` BL-97 records the decision under its third data point; `HANDOFFS.md`'s S265 receipt, whose `next_steps` item (4) said the call was his, now says it was made. Nothing in `bin/tests.sh` changed. No outward action.

### 2026-10-05 · [issue #93] S265 close-out — P2 of the trimmer false-red fix is committed: the proof names a stub finalize (exit 4), the writer warns, the rule is stated once

Deliverable: P2 of `docs/planning/issue93-trimmer-proof-false-red-plan.md`, `TRIM_VERSION` 1.6.0, in three checkpoint commits (`45d32d6`, `ba8f883`, `1214511`), the floor `7a18512`, the status `0ceb71c` and the evidence scripts `aa8eab0`; the owed trim (`0d77a8b`) and its fold (`891b55a`) ran first. 25 tests (154 in the file), 37 mutants killed, `bin/tests.sh` 362 passed, 0 failed at each checkpoint; the real trees re-derived (the adopter 1 of 54 proofs at exit 4, this repo 1 of 105, 0 newly red); an end-to-end smoke on this repo's real ledger. Three deviations from the plan, on evidence, and one of my own claims corrected (the heading shape, in `0ceb71c`'s entry). The `HANDOFFS.md` receipt is complete (`self_score` 8, S264 scored 9). `docs/planning/BACKLOG-DETAIL.md` BL-97 gains a third data point (two `grep -q` reds in one run that overlapped parallel clones; the quiet re-run read 362 and 0) and notes that the S257 reopen condition reads as arguably met, which is the operator's call. Phase 3C appended no fork learning row, so D3's retirement duty does not arise. Nothing pushed; nothing sent to `KJ5HST/methodology`.

### 2026-10-05 · [BL-98] S265 — the P2 re-derive script and the mutation runner join `issue93-evidence/`

`docs/planning/issue93-evidence/reverify_p2.py` (re-derives every frozen proof in a repo under the current template with the ledger's stub marker supplied by the LIVE basename, writes nothing under the repo, tabulates frozen against re-derived exit codes; it produced the adopter and fork figures in the plan's section 5 P2 DONE paragraph) and `docs/planning/issue93-evidence/mutants_p2.py` (the 37 mutants of P2 in three layers, run one at a time against a temp copy of the trimmer; run from this location, `all` reads 18, 14 and 5 killed, 0 survived, 0 invalid, in about two minutes). Both were scratch scripts in the session until now, which left the plan's "re-derive rather than trust" promise unmet for these numbers; the plan's DONE paragraph now says how to reproduce them. No outward action.

### 2026-10-05 · [BL-98] S265 — status follows P2 in the #93 plan, the BL-98 row and its detail

`docs/planning/issue93-trimmer-proof-false-red-plan.md`: the status line (P1 and P2 DONE, P3 not built), a correction pointer in section 4.1, and a measured "DONE at S265" paragraph in section 5 P2 with each criterion as measured, the real-surface results against the plan's prediction (1 of the adopter's 8 stub shards reaches exit 4 with canonical specs, not 8), the three deviations (no `CHANGELOG.md` marker, two more label conditions, one guard code per commit order) and what P3 inherits (a pre-1.6.0 frozen proof has no `STUB_PATTERN`, so `--reverify` supplies it from the ledger table by the live basename). `docs/planning/BACKLOG.md` row BL-98 and `docs/planning/BACKLOG-DETAIL.md` §BL-98 follow; the next action is P3. No outward action: nothing was sent to `KJ5HST/methodology` and nothing was pushed.
**Correction to the S265 layer-1 entry (`45d32d6`), which is committed and so is corrected here, not edited:** it says the plan's "a heading ending `(in progress)`" is one "which no claim heading in this ledger does". That is false. Counted over the whole file, 14 of the 27 `(in progress)` headings end there (the 13 others, the newer ones, carry ` — <description>` after it); I had read the first five rows of a `head`-truncated listing, the most recent and so the longest, and generalised from them. The decision to give `CHANGELOG.md` no stub marker does not rest on the heading's shape and stands: the ledger's lifecycle never edits a committed entry, so a claim reading `(in progress)` is a final record and not a stub awaiting its finalize. The same sentence, with a count ("26 of them live"), was in the plan paragraph written this session and is corrected in this commit; the trimmer's own comments carry no count and no shape claim.

### 2026-10-05 · [issue #93] S265 — tighten `trimmer-unit-tests` 129 → 154 in `.quality-gates.json`

The 25 tests P2 added (`45d32d6`, `ba8f883`, `1214511`: 8 for the proof's stub label, 12 for the write-time guard, 5 for the timing rule's wording) are now a floor: `python3 tools/test_methodology_trim.py` reads `Ran 154 tests`, OK (skipped=2), the gate's own command and extract. A tightening, so no approval is owed (`SAFEGUARDS.md` Blast Radius); the precedent is `9b59af6` (124 → 129). It is the mechanical half of Phase 3C: the tests that pin the stub label, the guard and the shared wording cannot silently drop.

### 2026-10-05 · [issue #93] S265 — P2 layer 3: the timing rule is stated the same way in the proof, the writer and the distributed prose

`FRAMEWORK_APPARATUS.md` (The Action Ledger, after the paragraph saying a trim earns its own commit): a new paragraph states the rule, trim while record 0 is complete, before the claim or after the finalize is committed, never in the commit that finalizes it, why (a `HANDOFFS.md` claim stub is overwritten in place, so the proof reads the receipt as edited), what the proof then does (exit 4, named, still a FAIL) and that the trimmer warns, advisory only. `starter-kit/methodology_trim.py`: the note a bundled frontier edit prints, and the comment above it, no longer say bundling is "this repository's own established practice" (this repo's own trims are their own commits; the claim contradicted the distributed prose and was the one place the verifier said otherwise) and now carry the rule, keeping the BL-27 token; the version comment records it. `tools/test_methodology_trim.py`: `TestTheTimingRuleIsStatedTheSameEverywhere`, 5 tests, the same anchor phrase pinned in the writer's constant, the distributed prose, the proof's generic note and its stub note, and the retired claim pinned gone from the template; 154 tests in the file (skipped=2), up from 129. Run against the checkpoint-2 prose and note, 3 of the 5 were RED (the apparatus sentence, the generic note, the template's retired claim) and the 2 already true were green; 5 mutants of the new wording all killed, one first written wrongly (its search text did not match the wrapped source line, reported INVALID, not as a kill). `bin/check-links` OK. Not yet: `bin/tests.sh` on this tree, the gate floor, the plan and backlog status.

### 2026-10-05 · [issue #93] S265 — P2 layer 2: a write-time guard warns before a stub finalize is bundled into a trim

`starter-kit/methodology_trim.py`: `check_stub_frontier`, called from `evaluate` once the cut is known to archive something, adds two ADVISORY findings (no exit code, the write proceeds, nothing is refused): `FRONTIER_PENDING_STUB` when record 0 of the live ledger still matches the ledger's `stub_marker` (order A: the claim is committed and not yet finalized), and `FRONTIER_FINALIZE_UNCOMMITTED` when HEAD's record 0 was a stub and the working tree no longer holds it (order B: finalized first, uncommitted, then trimmed). Each states the consequence and the two ways out, from one constant `TRIM_TIMING_RULE` (trim while record 0 is complete, before the claim or after the finalize is committed, never in the same commit). It keys on the declared marker, so `CHANGELOG.md` is silent; it asks whether HEAD's stub is ABSENT from the working ledger, so a record prepended above an intact stub is quiet; line endings are folded, so a CRLF checkout is not read as an edit; a ledger with no committed version skips order B. `tools/test_methodology_trim.py`: `TestWriteTimeGuardForAStubFinalize`, 12 tests, including that the advised order yields a passing proof; before the change 4 were RED for the right reasons and the controls green. 14 mutants of the guard, all killed (one survived the first run: the missing-HEAD branch was never reached because the stub fired order A first, so a complete-record-0 variant was added). Real surface, the new trimmer's dry run at real commits with `--force`: the adopter at the parent of its stub trim `2e206a65e` fires `FRONTIER_PENDING_STUB`; this repo at `8e3d568` (record 0 complete) is silent; this repo at `994eee5`, S265's own claim commit, fires. The adopter's parent of `HANDOFFS-through-2026-09-26` also fires although that trim's proof passes (its session did not bundle the finalize): the warning is about the wrong time to trim, not a certainty of a red proof, and its message is conditional. Layer 1's real-surface re-derive, also this session: the adopter's `HANDOFFS-through-2026-09-26-3` goes from exit 1 to exit 4 (a 606 B stub, 5 other records), its 7 `SESSION_NOTES` shards stay at exit 1 because canonical `LEDGERS` has no `SESSION_NOTES.md` entry and so no marker, 0 newly red in either tree; this repo's `HANDOFFS-through-2026-08-02` goes to exit 4 (a 750 B stub) and `-08-09` stays at exit 1 because an L2 front-matter failure also holds. Not yet: layer 3 (the prose), `bin/tests.sh` on this tree, the gate floor.

### 2026-10-05 · [issue #93] S265 — P2 layer 1: the generated proof names a stub finalize and exits 4 (`TRIM_VERSION` 1.6.0)

`starter-kit/methodology_trim.py`: `LedgerSpec` gains an optional `stub_marker`; `HANDOFFS.md` declares `^status: pending\s*$` (a line, re.M) and `CHANGELOG.md` declares none, deliberately, because the ledger's own lifecycle is "a committed entry is never edited" and a claim's `(in progress)` entry stays as written when close-out adds its own, so a `CHANGELOG.md` claim is a final record rather than a stub (this corrects the plan's section 4.1 and section 5 P2, which named a `CHANGELOG.md` marker, and its "a heading ending `(in progress)`", which no claim heading in this ledger does). The marker travels in the generated proof as `STUB_PATTERN` beside `REGEN_PATTERNS`. A frontier edit whose pre-trim record 0 matches it, whose replacement no longer does, with no other failure and every other record byte-identical and in order, now prints one labelled `FAIL:` (the stub's size, the count of other records) INSTEAD of the generic L1/L3 pair, a `NOTE:` stating the timing rule, and exits 4; every near-miss keeps exit 1 and the BL-27 note, which now also says when the ledger declares no marker. Still a FAIL by the plan's D2(i). Minor: a new exit status and a new `LedgerSpec` field. `tools/test_methodology_trim.py`: `TestVerifyShNamesAStubFinalize`, 8 tests, 137 in the file (skipped=2), up from 129; before the change 3 were RED for the right reasons (exit 1 with the generic pair, no `STUB_PATTERN`, no no-marker sentence) and 5 controls green. 18 mutants of the layer, all killed, each by its intended test (two survived the first run, a marker not anchored at the line's start and an unasserted note, and the tests were tightened). Not yet: layer 2 (the write-time guard), layer 3 (the prose), the real-surface check, `bin/tests.sh` on this tree, the gate floor.

### 2026-10-05 · [issue #93] S265 claim (in progress) — P2 of the trimmer false-red fix: a bundled stub-finalize is labelled (exit 4) and prevented at write time

CHANGELOG: pending. Operator said `go` as the first message and chose "P2 of the #93 fix" at the Phase 0 picker. The owed trim (`0d77a8b`, S262's receipt to shard `-6`, its `.verify.sh` exit 0 from a `--no-local` clone) and its fold (`891b55a`) ran first as their own actions; `bin/tests.sh` on the fold tree read 356 passed, 0 failed, 6 skipped. Deliverable: RED-first tests, then the proof's stub label and exit 4, the write-time guard and the prose, `TRIM_VERSION` 1.6.0, per the plan approved at S263. Phase 3F records the rest.

### 2026-10-05 · [ad hoc] S265 — fold the sixth 2026-10-04 HANDOFFS shard pointer into the archive index

The pointer block the trim (`0d77a8b`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, 2026-10-04, shard `-6`, trimmer v1.5.1), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S264, S263); the shard's `.verify.sh` was run from a `--no-local` clone of the trim commit and exited 0 (L1, L2/front-matter, L3). Ran after the Phase 0 report and the operator's choice of P2 of the #93 trimmer fix, before the session claim.

### 2026-10-05 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-04-6.md` (1 record(s), 39,968 B → 28,553 B)

**Written by:** `methodology_trim.py` v1.5.1 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-04 → 2026-10-04) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-04-6.md`](docs/archive/HANDOFFS-through-2026-10-04-6.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-04-6.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-04-6.md.verify.sh)
rather than trusting a digest printed here. Live file 39,968 B → 28,553 B (−28.6%).

### 2026-10-05 · [issue #93] S264 close-out — P1 of the trimmer false-red fix is committed: the generated proof's `leaked` clause tests whole lines (`TRIM_VERSION` 1.5.1)

The `HANDOFFS.md` receipt for S264 is `status: complete` (self 8, predecessor S263 scored 9). Deliverable: P1 of `docs/planning/issue93-trimmer-proof-false-red-plan.md`, commit `5270be8` (`starter-kit/methodology_trim.py`, `tools/test_methodology_trim.py`, 5 new tests, the clause's first coverage), the gate floor `trimmer-unit-tests` 124 to 129 (`9b59af6`) and the status documents (`5b5c0cc`); the owed trim (`039dde0`) and fold (`bd8cb8c`) ran first and the claim is `2392337`. Measured: 129 unit tests OK, 9 mutants (7 non-equivalent, all killed), the patched trimmer re-deriving every frozen proof with 0 newly red (the adopter 54 proofs, 10 red to 8; this repo 104 proofs, 5 to 3), `bin/tests.sh` 362 passed, 0 failed, 0 skipped, and a smoke trim of this repo's real `HANDOFFS.md` in a scratch clone whose generated proof (v1.5.1) exits 0. Nothing was sent to `KJ5HST/methodology` and nothing is pushed; this fork's trimmer is no longer byte-identical to upstream's. Phase 3C appended no fork learning row, so D3's retirement duty does not arise. Not done, by design: P2 (the next session's ranked first candidate), P3, P4 and its pull request, a comment on #93, the BL-94 decisions.

### 2026-10-05 · [BL-98] S264 — status follows P1 in the plan, the BL-98 row and its detail

`docs/planning/issue93-trimmer-proof-false-red-plan.md` (the status paragraph, which keeps S263's text and says which of its claims are now historical, and §5 P1's measured DONE), `docs/planning/BACKLOG.md` (the BL-98 row: P1 done, P2 next) and `docs/planning/BACKLOG-DETAIL.md` (§BL-98: what P1 measured and left, the next action). BL-98 stays open: P2 and P3 are not built. Two figures differ from the plan's text and are stated there: the adopter checkout has moved to `3a59ed844` with the same 54 proofs and 10 red, and this repo has 104 proofs, not 103. `bin/check-links` OK (111 links).

### 2026-10-05 · [issue #93] S264 — tighten `trimmer-unit-tests` 124 → 129 in `.quality-gates.json`

The 5 tests P1 added (`5270be8`) are now a floor: `python3 tools/test_methodology_trim.py` reads `Ran 129 tests`, OK (skipped=2), the gate's own command and extract. A tightening, so no approval is owed (`SAFEGUARDS.md` Blast Radius); the precedent is `d10f9af` (123 → 124). It is the mechanical half of Phase 3C: the count of tests that cover the `leaked` clause cannot silently drop.

### 2026-10-05 · [issue #93] S264 — P1: the generated proof's L2 `leaked` clause tests whole lines (`TRIM_VERSION` 1.5.1)

`starter-kit/methodology_trim.py`: `leaked` in `VERIFY_TEMPLATE` tested `ln in sfront or ln in "".join(sr)`, a substring test, so an archived record that merely quoted a front-matter line mid-line read as that line having travelled into the shard (a false red on a lossless trim); it now tests membership in the sets of whole lines of the shard's front matter and of its records, the `> 24` filter kept. Patch, 1.5.0 to 1.5.1, no new finding code and no exit-status change. `tools/test_methodology_trim.py`: `TestVerifyShLeakedTestsWholeLines`, 5 tests, the clause's first coverage (no test named `leaked` before); the two that quote a line mid-line were RED on 1.5.0 and the three controls (a whole line in the shard's front matter, a whole line in an archived record, a line under the length filter) were green on both; 129 tests OK (skipped=2), up from 124. Nine mutants of the fix, seven non-equivalent all killed, two equivalent survive (the fix itself and a per-record line set). Real evidence, the patched trimmer re-deriving every frozen proof without the prototype's `--exact-leak` patch: the adopter (`~/Development/nprcgenekeepr` at `3a59ed844`, read through a clone) 54 proofs, 10 red frozen to 8 red re-derived, 0 newly red, the 2 newly green exactly the two L2 shards of the plan's section 3.3; this repo (`2392337`) 104 proofs, 5 to 3, 0 newly red. `bin/tests.sh` 362 passed, 0 failed, 0 skipped. Proofs already written are frozen and unchanged; nothing sent upstream, nothing pushed; P2 and P3 not started.

### 2026-10-05 · [issue #93] S264 claim (in progress) — P1 of the trimmer false-red fix: the L2 `leaked` clause tests whole lines

CHANGELOG: pending. Operator said `go` as the first message and chose "P1 of the #93 fix" and "trim first" at the Phase 0 picker. The owed trim (`039dde0`, S261's receipt to shard `-5`, its `.verify.sh` exit 0 from a `--no-local` clone) and its fold (`bd8cb8c`) ran first as their own actions; `bin/tests.sh` on the fold tree read 356 passed, 0 failed, 6 skipped. Deliverable: RED-first tests, then the one change at `starter-kit/methodology_trim.py:1508-1509` and `TRIM_VERSION` 1.5.1, per the plan approved at S263. Phase 3F records the rest.

### 2026-10-05 · [ad hoc] S264 — fold the fifth 2026-10-04 HANDOFFS shard pointer into the archive index

The pointer block the trim (`039dde0`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, 2026-10-04, shard `-5`), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S263, S262); the shard's `.verify.sh` was run from a `--no-local` clone of the trim commit and exited 0 (L1, L2/front-matter, L3). Ran after the Phase 0 report and the operator's choice of P1 of the #93 trimmer fix, before the session claim.

### 2026-10-05 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-04-5.md` (1 record(s), 39,542 B → 29,317 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-04 → 2026-10-04) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-04-5.md`](docs/archive/HANDOFFS-through-2026-10-04-5.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-04-5.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-04-5.md.verify.sh)
rather than trusting a digest printed here. Live file 39,542 B → 29,317 B (−25.9%).

### 2026-10-05 · [issue #93] S263 close-out — the plan for the trimmer's false-red proofs is committed and approved to implement P1; nothing built

The `HANDOFFS.md` receipt for S263 is `status: complete` (self 8, predecessor S262 scored 9). Deliverable: `docs/planning/issue93-trimmer-proof-false-red-plan.md` and `docs/planning/issue93-evidence/` (commit `5309834`), BL-98 and the operator's decisions D1–D4 and part of D5 (`0290a16`); the owed trim (`cf9de43`) and fold (`92aaabc`) ran first and the claim is `3d7c5c8`. One outward action, the comment on upstream issue #93 (id `5998724931`), has its own entry. `starter-kit/methodology_trim.py` is unchanged and nothing is pushed. Phase 3C appended no fork learning row, so D3's retirement duty does not arise. Not done, by design: P1 (the next session's ranked first candidate), P2, P3, any pull request, the BL-94 decisions.

### 2026-10-05 · [issue #93] S263 — comment posted on upstream issue #93: the corrected split of the ten red proofs

**Outward action, no commit.** One comment on <https://github.com/KJ5HST/methodology/issues/93> (comment id `5998724931`, 2026-10-05T16:32:51Z, from the operator's `rmsharp` account via `gh issue comment`), posted only after the operator chose "Post exactly as shown" at a picker that printed the full text; nothing in it carries a session number, backlog code or plan term (grepped). It says: the 54-proof count reproduces; cause 2 is real and a whole-line test fixes it with no newly red proof in 157; cause 3 is not independent of cause 1; in all 8 cause-1 shards record 0 before the trim is a Phase 1B claim stub with no other record absent; a re-derive mode must lift its grammar from the frozen script because 7 of the 10 are a ledger the canonical trimmer has no spec for. Read back with `gh api repos/KJ5HST/methodology/issues/93/comments`: identical to the draft after trailing whitespace; the issue is OPEN with that one comment. No pull request, no patch, nothing else sent.

### 2026-10-05 · [BL-98] S263 — raise BL-98 for the #93 plan; the operator's decisions recorded; the plan approved to implement P1

BL-98 (`docs/planning/BACKLOG.md` index row, `docs/planning/BACKLOG-DETAIL.md` §BL-98) points at the plan and says what is next. The operator decided at a plan-review picker: P1 now without waiting for BL-60 (D1+D4); a recognised stub finalize stays a FAIL, labelled, exit 4 (D2); a read-only `--reverify` (D3); this backlog row, the comment on #93, and P1–P3 as one future upstream pull request, which is its own go-ahead (D5). The plan's status and §9 now say so. Still open, not asked: the adopter's local `SESSION_NOTES.md` spec, which the overlay drops, has no backlog item.

### 2026-10-05 · [issue #93] S263 — plan for the trimmer's false-red generated proofs: `issue93-trimmer-proof-false-red-plan.md`

`docs/planning/issue93-trimmer-proof-false-red-plan.md` (DRAFT, decisions D1–D5 open) plus two re-derivable scripts in `docs/planning/issue93-evidence/` (`reverify_prototype.py`, `repro_cause2.py`); no change to `starter-kit/methodology_trim.py`. Measured against the adopter's checkout (`nprcgenekeepr` at `2563a6ee0`) and this repo's 103 proofs: **#93's count reproduces (10 of 54 red, none a loss) but its split does not.** The ten are two classes, not three: 2 are the L2 `leaked` substring test, and 8 are a close-out commit that also trims, where record 0 was a Phase 1B claim stub before the trim (checked mechanically, 8 of 8, no other record absent). #93's cause 3 (a frozen v1.1.2 script) is not independent: re-derived under the current template, that shard falls into the stub class. Seven of the ten are `SESSION_NOTES.md` shards from a local ledger spec the canonical trimmer lacks, so a re-derive mode must lift its grammar from the frozen script. Proposed: P1 whole-line `leaked` (1.5.1; 10 → 8 red, 0 newly red in 157 proofs, prototype), P2 recognise and prevent the stub finalize (1.6.0), P3 read-only `--reverify` (1.7.0). The fork's trimmer is byte-identical to upstream's (blob `b98ff4b`). Nothing sent upstream.

### 2026-10-05 · [issue #93] S263 claim (in progress) — plan the fix for the trimmer's false-red generated proofs

CHANGELOG: pending. Operator said `go` as the first message and chose "Plan the #93 trimmer fix" at the Phase 0 picker. Upstream issue #93 (opened 2026-10-05 02:21Z under the operator's login, from `nprcgenekeepr`) reports that the trimmer's generated `.verify.sh` ends red on lossless trims, in three causes. The owed trim (`cf9de43`) and its fold (`92aaabc`) ran first as their own actions; `bin/tests.sh` on the fold's tree: 356 passed, 0 failed, 6 skipped, after a first run read 355 passed, 1 failed (Test 9, `net/http: TLS handshake timeout` reaching api.github.com, transient: the rerun passed it). Deliverable: one plan document in `docs/planning/`; no change to `starter-kit/methodology_trim.py`, nothing sent upstream. Phase 3F records the rest.

### 2026-10-05 · [ad hoc] S263 — fold the fourth 2026-10-04 HANDOFFS shard pointer into the archive index

The pointer block the trim (`cf9de43`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, 2026-10-04, shard `-4`), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S262, S261); the shard's `.verify.sh` was run from a `--no-local` clone of the trim commit and exited 0 (L1, L2/front-matter, L3). Ran after the Phase 0 report and the operator's choice of the #93 trimmer-fix plan, before the session claim.

### 2026-10-05 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-04-4.md` (1 record(s), 39,450 B → 27,845 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-04 → 2026-10-04) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-04-4.md`](docs/archive/HANDOFFS-through-2026-10-04-4.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-04-4.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-04-4.md.verify.sh)
rather than trusting a digest printed here. Live file 39,450 B → 27,845 B (−29.4%).

### 2026-10-04 · [ad hoc] S262 — cite the close-out commit `8b6224f` in the receipt's `commit:` slot

The S262 receipt's `commit:` answer slot read `pending`; it now begins with the close-out commit's sha, as `bin/check-handoff`'s answer-slot rule needs once the next claim sits above it (S260's slot, which did not, turned Test 34 L1 red under S261's claim). No other change.

### 2026-10-04 · [BL-94] S262 close-out — the planted defects `missing` and `vague` are rebuilt at $0; a flip is not shown

The `HANDOFFS.md` receipt is complete (self-score 8, S261's handoff scored 9). Deliverable: the rebuild in `7bbc0f1` with its report `c01637c` and status `eca6456`, after the owed trim `c5f6057` and fold `2924283` and the claim `f1485fc`; the operator approved the implementation plan as written before any code. Nothing spent (the study's ledger stays $4.0927 of its own $100), nothing pushed, nothing sent to `KJ5HST/methodology`. No fork learning row was appended, so D3's retirement duty does not arise; the lesson that a finder-relative check passes while evidence stands is #108's, and this session's residue list, tests and mutants are its mechanical form. What remains is his: a third paid run (about $1.6 by estimate), his own blind rating, D6 and D7, P3.

### 2026-10-04 · [BL-94] S262 — status follows the rebuild: the plan, the BL-94 row and detail

A status paragraph in `docs/planning/documentation-quality-experiment-plan.md` and in `BACKLOG-DETAIL.md`, and one clause in the BL-94 row of `BACKLOG.md`: the two planted defects are rebuilt at $0, the check passes at zero, nothing here shows a flip, and what is still his (a third paid run of about $1.6 by estimate, his own blind rating, D6 and D7, P3). BL-94 stays open; no id leaves the backlog.

### 2026-10-04 · [BL-94] S262 — report on the rebuilt planted defects: `P2_DEFECTS_S262.md`

New `docs/planning/overhead-replay/pilot/doc-evidence/P2_DEFECTS_S262.md`, a pointer in `P2_RATER_RERUN.md` and one sentence in the harness `README.md`. It records what S261's variants still held, counted with the new finders (pending sentences 12, 10, 16; `vague` tokens 32, 49, 68, mostly issue references and document names), what changed and where, the before-and-after table, and what I read in the six rebuilt variants (hazards, caveats and observations remain; no stated next step, no named file, function, issue or document; the next work survives in prose). The claims in it were checked against the saved variants before it was committed (four were corrected: the "roxygen harmonization" count, the two cited works, `origin/master` in two of three, and which tests were written first). It states that nothing here shows the rater's answers flip, and that a third paid run (about $1.6, an estimate) is his go-ahead. Nothing spent.

### 2026-10-04 · [BL-94] S262 — rebuild the planted defects `missing` and `vague` in `rater.py` ($0, no rating call)

`docs/planning/overhead-replay/rater.py`, `tests_rater.py`, `mutants_p2a.py`. Reading the variants S261 sent to the rater, and the rater's `reason` strings, confirmed what S261's report §2 listed (a pending action stated as status in every record; document names such as `NEWS` and "Age-Sex Pyramid") and found two things it had not: the issue and ticket references (`#120`, `#103`, `E4`) that the next steps point at, which the v3.7-r2 `vague` reason itself names; and a bug, a backtick span that wrapped onto a second line mis-paired every later span on its line (the R1-r2 `vague` variant read `codeis.nathe`, `is.na` bare). The builders now work on whole units (`units`, `per_unit`); `missing` also drops each sentence that states a pending action (`PENDING`, fitted to the three honest-set records and said to be); `vague` also removes issue and ticket references, document names, hyphenated place names and dotted function names; the check counts what the builders remove and now prints, beside it, what it does not (`residue`). On the three records: `missing` evidence 15, 17, 23 to 0 (labels and pending sentences; S261 counted labels only: 2, 3, 3), `vague` 329, 404, 475 to 0 (S261: 297, 355, 413); `missing` removes 14.3%, 12.4% and 18.4% of the honest record's characters (S261's builder: 5.6%, 7.2%, 9.4%). `tests_rater.py` 58 to 74 tests; `mutants_p2a.py rater` 72 to 129 mutants, all killed (9 repaired where the code moved). The packet and `sheet.csv` regenerate byte-identical. **Not shown, by design:** that the rater's `next_step` and `where` answers now flip; only a paid run shows that (fork learning #108). Nothing spent; nothing sent upstream.

### 2026-10-04 · [BL-94] S262 claim (in progress) — rebuild the planted defects `missing` and `vague`

CHANGELOG: pending. Operator said `go` as the first message and chose "BL-94: rebuild missing and vague" at the Phase 0 picker. The owed trim (`c5f6057`) and its fold (`2924283`) ran first as their own actions; `bin/tests.sh` after them: 356 passed, 0 failed, 6 skipped (Test 34's named rows below three receipts). Deliverable: rebuild the two defects in `rater.py` at $0 so the evidence S261 found standing is removed, and say plainly what only a paid run can show. Phase 3F records the rest.

### 2026-10-04 · [ad hoc] S262 — fold the third 2026-10-04 HANDOFFS shard pointer into the archive index

The pointer block the trim (`c5f6057`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, 2026-10-04, shard `-3`), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S261, S260); the shard's `.verify.sh` was run from a `--no-local` clone of the trim commit and exited 0 (L1, L2/front-matter, L3). Ran after the Phase 0 report and the operator's choice of the BL-94 missing/vague rebuild, before the session claim.

### 2026-10-04 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-04-3.md` (1 record(s), 38,986 B → 28,035 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-04 → 2026-10-04) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-04-3.md`](docs/archive/HANDOFFS-through-2026-10-04-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-04-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-04-3.md.verify.sh)
rather than trusting a digest printed here. Live file 38,986 B → 28,035 B (−28.1%).

### 2026-10-04 · [ad hoc] S261 — cite the close-out commit in the receipt's `commit:` slot

`HANDOFFS.md`'s S261 receipt now starts its `commit:` slot with `4d3a34f`, the close-out commit, so the next session's claim does not turn Test 34 L1 red the way S260's slot did. One line in `HANDOFFS.md`.

### 2026-10-04 · [BL-94] S261 close-out — the rater re-run is done: `missing` and `vague` MISSED again, `wrong` caught ($1.6146); fork learning #108

The `HANDOFFS.md` receipt is `status: complete`. Commits: trim `37f0ad6` and fold `8f5a15f` (both before the claim), claim `e2905b7`, the run and report `e18d5a1`, the S260 `commit:` slot reconcile `9cb4ec4`, status in the plan, backlog row and detail `348a23a`, plus this close-out. Result: 12 of 12 calls on the rebuilt `missing` and `vague` answered yes (their evidence survives in a status line and in names no finder counts), `wrong` caught on all 3 records in both orders, honest records 8 of 8, arm guess unchanged; the rater is not shown to be blind to a vague record. Spend $1.6146 (the study's ledger $4.0927 of $100). **Phase 3C appended fork learning #108** (docs/FORK_LEARNINGS.md); D3's retire-or-refuse: none retired, the nearest rows #16, #83 and #107 named in the receipt as not meeting (a), (b) or (c). `bin/tests.sh` 362 passed, 0 failed. No harness file changed; nothing pushed; nothing sent upstream. Next, all his: rebuild the two defects, his own blind rating, D6 and D7, P3; the owed HANDOFFS trim (3 receipts).

### 2026-10-04 · [BL-94] S261 — status follows the rater re-run: the plan's P2 status, the BL-94 row and detail, a pointer in the P2 report

Documentation only. Each says the rater was re-run on the rebuilt defects at $1.6146 (`missing` and `vague` MISSED again, `wrong` caught, the study's ledger $4.0927 of $100) and points at `pilot/doc-evidence/P2_RATER_RERUN.md`; the S260 paragraphs' "not re-run" is marked superseded. No harness file changed.

### 2026-10-04 · [ad hoc] S261 — reconcile S260's `commit:` answer slot to its close-out sha

S260's receipt named "the close-out commit (see `git log`)", which `bin/check-handoff` refuses once a newer receipt sits above it (`bin/tests.sh` Test 34 L1: 361 passed, 1 failed, after the S261 claim). Per `starter-kit/HANDOFFS.md:64` and `:78-79` the next session reconciles it: the first commit whose copy of the S260 block reads `status: complete` is `61cd3d0` (found with the checker's own recipe), so the slot now starts `61cd3d0 (the close-out commit)`; the rest of the line is unchanged. One line in `HANDOFFS.md`.

### 2026-10-04 · [BL-94] S261 — the rater dry run on the planted defects rebuilt at S260: `missing` and `vague` MISSED again, `wrong` caught ($1.6146)

Ran `rater.py dry-run --call-cap 0.50 --total-cap 10 --out pilot/doc-probe/rating-s261` (30 calls, the code's default model and effort; results in `pilot/doc-probe/rating-s261/`, S259's `rating/` left as it was). **`missing` and `vague` were MISSED on all 3 records in both orders (12 of 12 calls, 8/8 yes)** although the $0 removal check passed both before the first call: the status lines still state a pending action (`gh issue close 121`) and names such as `NEWS` and `AUDIT_WORKSTREAM` remain, which the finders do not count. `wrong` was caught on all 3 in both orders; the honest records scored 8 of 8 again; the arm guess is unchanged from S259; all 30 calls parsed, so the S260 repair (b) was not exercised. Spend: 30 ledger rows, $1.6146 (mean $0.0538, max $0.0652); the study's ledger is $4.0927 of its own $100. Report: `pilot/doc-evidence/P2_RATER_RERUN.md`. Decisions left to the operator: rebuild the two defects again, take his own blind rating as the measure, D6 and D7. Nothing pushed, nothing sent upstream.

### 2026-10-04 · [BL-94] S261 claim (in progress) — the rater dry run on the rebuilt planted defects

CHANGELOG: pending. Operator said `go` as the first message, chose "BL-94 rater re-run" and "trim first" at the Phase 0 picker. The owed trim (`37f0ad6`) and its fold (`8f5a15f`) ran first as their own actions. Deliverable: re-run `rater.py dry-run` on the defects S260 rebuilt, at the cost the picker stated (about $1.7), and report whether the model rater separates them from the honest records. Phase 3F records the rest.

### 2026-10-04 · [ad hoc] S261 — fold the second 2026-10-04 HANDOFFS shard pointer into the archive index

The pointer block the trim (`37f0ad6`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, 2026-10-04, shard `-2`), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S260, S259); the shard's `.verify.sh` was run from a `--no-local` clone of the trim commit and exited 0. Ran after the Phase 0 report and the operator's choice of the BL-94 rater re-run, before the session claim.

### 2026-10-04 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-04-2.md` (1 record(s), 39,475 B → 28,767 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-04 → 2026-10-04) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-04-2.md`](docs/archive/HANDOFFS-through-2026-10-04-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-04-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-04-2.md.verify.sh)
rather than trusting a digest printed here. Live file 39,475 B → 28,767 B (−27.1%).

### 2026-10-04 · [BL-94] S260 close-out — the four P2 harness defects are fixed at $0

Close-out of the S260 claim (`c2eacbd`). Deliverable: BL-94's four harness defects from `P2_REPORT.md` §4, no model call and nothing spent (the study's ledger stays $2.4781 of $100). Commits: trim `d98c464` and fold `51edca6`, claim `c2eacbd`, probe fixes (a) and (c) `37c5f0f`, rater fixes (b) and (d) `f067add`, documents `8bedda1` and `6804c60`, mutant runner `770c855`, then this close-out. Verification run in the session: `bin/tests.sh` 362 passed, 0 failed; `tests_probe.py` 58, `tests_rater.py` 58, `tests_doc_evidence.py` 14, `tests_p1b.py` 20, `FreezeTests` 4, all OK; mutants 81 of 81 and 72 of 72 killed and none a syntax error; `doc_score.py` diff 0 lines; the fixes run on the real bundle, the four saved probes' stream logs and the three honest records. **What it found:** both of S259's rater misses were the planted-defect builders', not the rater's (`missing` used the scorer's label set, which lacks `SUGGESTED NEXT`; `vague` left 273 to 338 backticked spans and 19 to 24 function names per record under a question that accepts a function or a location); and reading the rebuilt output found a boundary defect the new check had passed (`#28/#12/...` taken for a heading), so the check now also reports where each removal stopped. The frozen scorer has the same loose heading rule; measured, 0 of 23 scored runs differ. Phase 3A scored S259's handoff 9/10 (all seven anchors exact; the `-7` shard name was wrong); 3B self 8/10; 3C appended no fork learning and retired no row (the vacuous-mutant lesson is now a runner check, `770c855`). Not done by design: the rater is not re-run on the rebuilt defects (paid, his decision), P3, D6 and D7. Receipt in `HANDOFFS.md`. Nothing pushed, nothing sent to `KJ5HST/methodology`, nothing spent. `CHANGELOG: pending` from the claim is resolved by this entry.

### 2026-10-04 · [BL-94] S260 — the mutant runner rejects a mutant that does not compile

`mutants_p2a.py`: `run_one` compiles each mutated source and reports a SyntaxError as BAD MUTANT (not killed), because every test "kills" it and it proves nothing; the S258 mutant "the record is not between markers" was exactly that (found at S260 by compiling all 153 mutants, repaired in `f067add`). Shown on a deliberate syntax error and on a good mutant; `mutants_p2a.py rater` still reads 72 of 72 killed. This is the mechanical form of the lesson, so no fork-learning row is appended for it. $0.

### 2026-10-04 · [BL-94] S260 — backlog row and detail status follow the four harness fixes

`BACKLOG.md`'s BL-94 row no longer says three harness defects come before P3 (D6 and D7 do; S260 fixed the four at $0); `BACKLOG-DETAIL.md` gets an S260 status paragraph that supersedes S259's "three harness defects, not fixed" and says what was not done (the rater is not re-run on the rebuilt defects; P3 is its own go-ahead). BL-94 stays open.

### 2026-10-04 · [BL-94] S260 — the harness README, the P2 report and the plan's P2 status follow the four harness fixes

`overhead-replay/README.md` describes the new probe row fields, the leftover-clone rule, the rater's evidence check and its raw text (58 and 58 tests, 81 and 72 mutants); `P2_REPORT.md` §4 gets a one-line pointer saying items 1 to 3 and the rater's two misses were fixed at S260 (its S259 text is left as written, so the record of what S259 found stays whole); the plan's P2 section gets an S260 status paragraph that says what was and was not done. $0.

### 2026-10-04 · [BL-94] S260 — P2 harness fixes (b) and (d): a failed rating call keeps its text; the `missing` and `vague` defects remove what their question rests on, and a $0 check proves it

`rater.py`. **(b)** `call_rater` returns `(parsed, cost, error, raw)`: `raw` is the text that failed (stdout and stderr when the CLI gave no JSON, its envelope on a CLI error, the reply when it could not be used), bounded at 20,000 characters with the full length stated, None for a usable reply; each `dry-run.json` result carries it. **(d)** read from the real records at $0: all three carry a `**=> SUGGESTED NEXT.**` paragraph that the builder's label set (a copy of the scorer's) did not name, and 273 to 338 backticked spans plus 19 to 24 function names per record survived `vague` while the question asks for a "file, function or location"; both of S259's rater misses were the builders', not the rater's. `NEXT_LABEL` is widened; `vague` is rebuilt on one finder of places in the code (backticked spans, calls, qualified, camelCase and snake_case names, line references, with a receipt's field names kept as labels) that it removes exactly. Each defect with a finder is checked at $0 (`defect_check`: evidence before and after, residue, and where each removal stopped); `rater.py defects` prints it and fails on a problem, and `dry-run` refuses before its first paid call if a defect leaves the evidence it was built to remove. On the three honest records `missing` takes next-step labels 2, 3, 3 to 0 and `vague` takes tokens 297, 355, 413 to 0. **Found by reading the result, not by the check:** after the rebuild the v3.8 record still held the tail of its SUGGESTED NEXT block, because a line opening with `#28/#12/#11/#10/#5` was taken for a heading (the scorer's `_parts` has the same rule and is frozen, so untouched); fixed with a strict heading rule and a regression test, and the check now also reports the line each removal stopped at, since a finder of labels cannot see a surviving body. `tests_rater.py` 36 to 58, `mutants_p2a.py rater` 32 to 72 mutants, every one killed; one S258 mutant ("the record is not between markers") was a syntax error and killed nothing, and is repaired. The rater was NOT re-run on the rebuilt defects (paid; his decision), so whether it separates them is still unknown. $0, no model call.

### 2026-10-04 · [BL-94] S260 — P2 harness fixes (a) and (c): the probe records every file read and replaces a pristine leftover clone

`probe.py`. **(c)** a clone `--no-launch` leaves is replaced by the next launch (or the next `--no-launch`) while it is a pristine copy of what that launch would build: a repository of its own, no remote, nothing changed (tracked, untracked or ignored), at the pin or on the one control commit; anything else is refused, naming why, and left untouched; the row records `leftover_replaced`. Reproduced and cleared on the real bundle (`real-3.7/v3.0-r1`: the second `--no-launch` replaced the first, a touched clone refused with its file kept, $0). **(a)** a row now carries `reads_other` (files named to shell content readers `cat head tail sed awk grep rg ...`, and the Grep tool's targets, resolved against the clone as the CLI reports it) and `reads_unparsed` (commands that could not be read: a here-document or an unbalanced quote, kept up to 300 characters, never guessed at) beside `reads`; `wc`, `ls` and the like are not reads. Run over the four saved probes' stream logs it finds the v3.0 probe's `head -150 SESSION_NOTES.md` that `reads` missed and the v3.7 probe's `grep -n "status:" HANDOFFS.md`, and counts neither `wc -c` call. `tests_probe.py` 43 to 58 (the real commands as a table; a synthetic transcript runs the row's `if tp:` block in a test for the first time), `mutants_p2a.py probe` 35 to 81 mutants, every one killed and none a syntax error. $0, no model call. The earlier `reads` docstring said "the row says so" about Bash reads; it did not, and now says what it does.

### 2026-10-04 · [BL-94] S260 claim (in progress) — the four P2 harness fixes, $0

CHANGELOG: pending. Operator said `go` as the first message; the Phase 0 picker he declined to answer in order to ask about an mts-system report (a RED/GREEN commit-policy question for that adopter, answered in discussion, nothing changed there), then chose "BL-94 harness fixes, $0". Deliverable: the four harness defects `P2_REPORT.md` section 4 names, each fixed with a test or a mutant, no model call and no spend: (a) `probe.py` `phase0_reads` counts the Read tool only; (b) `rater.py` `call_rater` drops the raw reply on a failed parse; (c) `probe.py` `--no-launch` leaves a clone the real launch then refuses; (d) the `missing` and `vague` planted defects do not provably flip their own question. P3 is its own go-ahead and not part of this session. Phase 0: 0 undocumented commits at both frontiers, the ratchet citation matches `.quality-gates-results.json` (results `3f5791d93dac`, manifest `fd435a4f8fab`), PR #92 open with no comments or reviews and no other open PR or issue, 81 ahead of `origin/main` and 102 behind `upstream/main`, dashboard 72/100, the BL-79 hook still not installed. The owed HANDOFFS trim (`d98c464`) and fold (`51edca6`) ran first as their own actions, the shard's `.verify.sh` exit 0 from a `--no-local` clone. Nothing pushed, nothing sent upstream, nothing spent.

### 2026-10-04 · [ad hoc] S260 — fold the 2026-10-04 HANDOFFS shard pointer into the archive index

The pointer block the trim (`d98c464`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, 2026-10-04), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S259, S258); the shard's `.verify.sh` was run from a `--no-local` clone of the trim commit and exited 0. Ran after the Phase 0 report and the operator's choice of BL-94 harness fixes, before the session claim.

### 2026-10-04 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-04.md` (1 record(s), 39,622 B → 27,856 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-04 → 2026-10-04) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-04.md`](docs/archive/HANDOFFS-through-2026-10-04.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-04.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-04.md.verify.sh)
rather than trusting a digest printed here. Live file 39,622 B → 27,856 B (−29.7%).

### 2026-10-04 · [BL-94] S259 close-out — P2 done: four cold probes and the rater dry run at the $10 cap (the claim below lists the commits)

Deliverable: P2 of `docs/planning/documentation-quality-experiment-plan.md` §5, report `docs/planning/overhead-replay/pilot/doc-evidence/P2_REPORT.md`. **State:** $2.4781 spent of the $10 cap and of the study's $100, no cap hit, 35 ledger rows re-summed. A probe costs $0.16 to $0.24 (mean $0.19, not the plan's $1); a rating call $0.044 to $0.066; 36 claims in the four cold reports checked, none wrong; the git-only control's session named the extra restore commit and recommended it first; the model rater scored every honest record 8 of 8 and missed `vague` on all three records (`missing` is inconclusive: its builder leaves a next step in place); three harness defects found by running it (`reads` is the Read tool only, a failed rating parse keeps no raw reply, `--no-launch` leaves a clone the real launch refuses), none fixed. **His decision at the stop:** fix the harness first, at $0, before any P3 decision. **Wrong when first written and corrected the same session:** "about 14" claims checked (8, 12, 9, 7), the dry run's wall time, and "`wrong` caught on all 3". The owed `HANDOFFS.md` trim (`461bc20`) and fold (`7e767b8`) ran first as their own actions. Nothing pushed, nothing sent upstream. Phase 3C appended no fork learning and retired no row (the three lessons are mechanical and belong in the next session's tests). **Gate run:** 12/12 pass, results `3f5791d93dac`, `tests-sh-passed` 362, 0 failed (on `d9b3cad` plus the receipt's citation); the first run on `d9b3cad` alone was 10/12 because the receipt cited no gate run, which `check-handoff-all` and one suite test caught.

### 2026-10-04 · [BL-94] S259 — P2 checkpoint 5: the plan, the backlog row and detail, and the harness README follow the P2 report

`docs/planning/documentation-quality-experiment-plan.md` (a status line under §P2), `docs/planning/BACKLOG.md` (the BL-94 row: P2 done, next phase P3 on its own go), `docs/planning/BACKLOG-DETAIL.md` (a status paragraph that supersedes S258's "P2 starts only when he says go") and `docs/planning/overhead-replay/README.md` (the P2 files). Figures are the report's; nothing new is claimed here.

### 2026-10-04 · [BL-94] S259 — P2 checkpoint 4: the P2 report

`docs/planning/overhead-replay/pilot/doc-evidence/P2_REPORT.md`. **Spend $2.4781 of the $10 cap (of the study's $100): a probe $0.16 to $0.24, mean $0.19 (the plan said $1, S258's estimate from the saved runs was $0.35); a rating call $0.044 to $0.066, mean $0.055.** 36 claims checked in the four cold reports, none wrong; the control's session named the restore commit and recommended investigating it first (the confound observed). **The model rater scored all three honest records 8 of 8 in both orders and missed `vague` on all three (every path and anchor removed, `where` still yes 8 of 8); `missing` is inconclusive because the builder leaves a next step in place; `wrong` was caught.** Three defects in the harness, found by running it: `reads` records the Read tool only (the v3.0 session read `SESSION_NOTES.md` by Bash `head -150`); a failed rating parse keeps no raw reply; `--no-launch` leaves a clone that makes the real launch refuse. P3 restated at about $9 to $11 against the plan's $38; the report says why that is not the open question. The checkpoint 2 and 3 entries below now give exact claim counts (8, 12, 9, 7) in place of "about 14".

### 2026-10-04 · [BL-94] S259 — P2 checkpoint 3: the v3.8-text probe and its git-only control, reports and stream logs

`pilot/doc-probe/t-control-fix--R1-r2/` and `t-control-fix--R1-r2+git-only/`, each `report.md` and `stream.jsonl`. Hand-read, every checkable claim verified against the rebuilt state (9 in the v3.8-text report and 7 in the control's: `CHANGELOG.md` 910,153 B, `SESSION_NOTES.md` 3,863,018 B, `passed=3747 failed=1 warnings=0 files=252`, no `quality-gates` line in `.Rbuildignore`, the "hidden files" NOTE, the 196,608 B figure in `methodology_trim.py`; for the control the restore commit `602a8b5c`, `SESSION_NOTES.md` back at S313, the only `handoff` block in `HANDOFFS.md` being the format example, the `test-warnings` gate threshold 0 after the commit "tighten test-warnings gate from 7 to 0"). No wrong claim in either. **The control's cold session saw the extra restore commit in `git log`, named it, and made it its first recommendation ("confirm what the HEAD revert was meant to do")**; the documented arm's session recommended a concrete small task from the handoff. That is the named confound (S258 gotcha 5) observed, not only predicted.

### 2026-10-04 · [BL-94] S259 — P2 checkpoint 2: the v3.0 and v3.7 probes' reports and stream logs

`pilot/doc-probe/real-3.7--v3.0-r1/` and `real-3.7--v3.7-r3/`, each `report.md` (the cold session's Phase 0 report, 2,414 and 2,368 characters) and `stream.jsonl` (the only per-stop record). Both reports were hand-read and their claims checked against the rebuilt end state: every commit hash named exists, the install commit and both ledger frontiers (`aeebcdec` on v3.7) are as stated, 1,805 commits, the untracked `dashboard_history.jsonl` and S314's note to decide on it, `test_getVersion.R` as an environment failure, and the newest `HANDOFFS.md` receipt `status: complete` (the first `status:` match in that file is the format example). No wrong claim found: 8 checked in the v3.0 report, 12 in the v3.7 report (the dashboard scores and dates were not checked). Each ended with no task started and a question, one stop, as scripted.

### 2026-10-04 · [BL-94] S259 — P2 checkpoint 1: the study's spend ledger, the four probe rows and the rater dry run

`docs/planning/overhead-replay/pilot/doc-probe/spend.jsonl` (35 rows, **$2.4781**: four probes $0.7696, 31 rating calls $1.7085; no zero-cost row), `rows.jsonl` (the four probe rows, each cost equal to its ledger row) and `rating/dry-run.json`, `rating/dry-run-summary.json`. Probes (`probe.py ... --session-cap 1.00 --total-cap 10`, sonnet, xhigh, CLI 2.1.289, one stop each, none cut by a cap): v3.0 `real-3.7/v3.0-r1` $0.1950, v3.7 `real-3.7/v3.7-r3` $0.2444, v3.8-text `t-control-fix/R1-r2` $0.1599, its git-only control $0.1703. Rater: one canary call first ($0.0451, to read the real JSON envelope: `result`, `total_cost_usd`, `is_error`, `subtype` all present as assumed), then the 30-call dry run ($1.6634); one call returned an unparsable reply (`t-control-fix/R1-r2/wrong/A`, string cut at char 171; the raw reply is not kept). A first launch of the v3.0 probe refused in 3 s ("exists; refusing to overwrite") because my own four `--no-launch` checks had left clones in `/tmp/doc-probe`; nothing was spent, the four were deleted and the probe relaunched.

### 2026-10-04 · [BL-94] S259 claim (in progress) — P2: four cold probes and the rater dry run at the $10 cap

Operator said `go` as the first message; at the Phase 0 picker he confirmed "P2 as named" (P2 at the $10 cap, the four end states named in the report, a $0 `--no-launch` check first). Deliverable: P2 of `docs/planning/documentation-quality-experiment-plan.md` section 5, the study's first spend, inside its own $100 cap from $0. Phase 0: 0 undocumented commits at both frontiers, the ratchet citation matches `.quality-gates-results.json` (results `3f5791d93dac`), PR #92 open with no comments or reviews and no other open PR or issue, 69 ahead of `origin/main` and 102 behind `upstream/main`, dashboard 72/100. The owed HANDOFFS trim (`461bc20`) and fold (`7e767b8`) ran first as their own actions, the shard's `.verify.sh` exit 0 from a `--no-local` clone. Nothing pushed, nothing sent upstream.

### 2026-10-04 · [ad hoc] S259 — fold the sixth 2026-10-03 HANDOFFS shard pointer into the archive index

The pointer block the trim (`461bc20`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, 2026-10-03), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S258, S257); the shard's `.verify.sh` was run from a `--no-local` clone of the trim commit and exited 0. Ran after the Phase 0 report and the operator's confirmation of BL-94 P2 at the $10 cap, before the session claim.

### 2026-10-04 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-03-6.md` (1 record(s), 40,235 B → 28,671 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-03 → 2026-10-03) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-03-6.md`](docs/archive/HANDOFFS-through-2026-10-03-6.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-03-6.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-03-6.md.verify.sh)
rather than trusting a digest printed here. Live file 40,235 B → 28,671 B (−28.7%).

### 2026-10-04 · [BL-94] S258 — the gate run confirmed 12/12, results `3f5791d93dac`; the receipt cites it and its commit

`quality_ratchet.py --run` on the committed close-out tree `e25cf19`: 12 of 12 pass, `tests-sh-passed` 362 (floor 343, not tightened), results `3f5791d93dac`, manifest `fd435a4f8fab` (the results hash is a function of the gate values, so it equals S257's). The receipt's placeholder citation and its `commit:` slot now carry the real values. The auto-memory notes (BL-94 state, the absence-claim and zsh traps) were updated outside the repository.

### 2026-10-04 · [BL-94] S258 close-out — P2a done: the cold-start probe is built and tested at $0 (the claim above lists the commits)

Deliverable: P2a of `docs/planning/documentation-quality-experiment-plan.md` §5, report `docs/planning/overhead-replay/pilot/doc-evidence/P2A_REPORT.md`. **State:** `probe.py` (43 tests, 35 of 35 mutants killed) rebuilt all 38 rebuildable saved runs as end state and git-only control with HEAD equal to the pinned sha (3 refused by design); the R suite at `879503cce` takes 120.8 s; a probe should cost about $0.35 against the plan's $1 (a floor, from the saved runs' first stop); the rater, four planted defects and a six-record packet for him are built (36 tests, 32 of 32 mutants); no M3 task exists in the project's history, one can be constructed; nothing was run against a model and nothing was spent. **His decisions at the stop:** P2 at the $10 cap (starts when he says go in that session), a six-record packet, M3 deferred until after P2. Three claims of mine were wrong when first written and are corrected in this ledger and the report (see "a correction to my own checkpoint 1 and 3 entries"). Previous handoff scored 9/10, self 7/10. Phase 3C appended no fork learning, so no retirement is owed. Nothing pushed, nothing sent to `KJ5HST/methodology`; PR #92 open with no reply. Next: P2, on his go.

### 2026-10-04 · [BL-94] S258 — backlog row, detail status and the harness README follow the P2a close

`BACKLOG.md` (the BL-94 row) and `BACKLOG-DETAIL.md` (a P2a status paragraph that supersedes the S257 "next: P2a") record P2a done and his three answers; `overhead-replay/README.md` gains a section listing the P2a files.

### 2026-10-04 · [BL-94] S258 — the rater's strata, its tests, the plan and the report follow the decisions

`rater.py` `STRATA` 3 / 3 / 4 to 2 / 2 / 2 and the packet's opening line counts its records; `tests_rater.py` expects two per arm, six unique records, labels R01-R06 and a seven-row sheet; the plan (§4 item 4, D4, D5, the P2a status) and `P2A_REPORT.md` record the three answers. The previous commit holds the rebuilt packet, sheet and key.

### 2026-10-04 · [BL-94] S258 — the operator's decisions at the P2a stop, from the close-out picker; the packet rebuilt at six records

His three answers, from one picker after the report was in and before the close-out: **P2 at the $10 cap** (the recommended option; the others were probes only at $3 and no P2 yet), starting only when he says go in that session, with a proposed probe session cap of $1.00 and rater call cap of $0.50 (D4 at the plan's figure; the study cap stays $100 and $0 is spent); **a six-record blind packet**, two per arm (the recommended option; ten and three were the others), so `rater.py`'s strata are now 2 / 2 / 2 and `pilot/doc-probe/rating/` holds the rebuilt packet, sheet and key: 20,410 words, 2,832 to 4,135 per record, about 102 minutes at 200 words a minute (an estimate; the ten-record build was 33,592 words); **M3 deferred until after P2** (the recommended option; drop and plan-the-rename-task were the others). Recorded in the plan (§4 item 4, D4, D5 and the P2a status), the P2a report and `tests_rater.py` (36 tests, 32 of 32 mutants killed on the six-record code).

### 2026-10-04 · [BL-94] S258 — P2a report, plan status, and a correction to my own checkpoint 1 and 3 entries

`pilot/doc-evidence/P2A_REPORT.md` (the answer first, then items (a) to (f), where it differs from the plan, what is asked of the operator) and the plan's §5 P2a status and header line. **Corrections, found by counting rows I had asserted about:** (1) checkpoint 1 said no saved run ever hit the budget cap and the CLI's cap message had never been seen; **one did**: `pilot/xhigh-go` HEAD rep 1 ended `result error_max_budget_usd` at $2.0389 on a $2.00 cap, so the fake's budget stop has the real shape and the CLI overshoots a cap by a little. The `cap_hit` guard stays (it covers a cap stop that came back as a plain success) and its comment in `probe.py` and the checkpoint 1 entry now say what is true. (2) checkpoint 3 said `getEmptyErrorLst` is in "two vignette chunks, one evaluated" and "five" `R/` uses; it is in two vignettes, each in an evaluated chunk, and 7 `R/` files and 10 test files use it. Final mutant run on `probe.py`: **35 of 35 killed** (before the comment-only edit); `rater.py`: 32 of 32.

### 2026-10-04 · [BL-94] S258 — P2a checkpoint 5: the operator's blind rating packet, item (d) ($0)

`pilot/doc-probe/rating/`: `packet.md` (ten records drawn with seed 20261004, stratified 3 v3.0 / 3 v3.7 / 4 v3.8-text, shuffled, labelled R01-R10, the eight questions once at the top), `sheet.csv` (the score sheet he fills: eight yes/no/? columns, an arm guess, notes) and `KEY-do-not-open-before-rating.json` (record to run and arm, a separate file; `rater.py score-human sheet.csv KEY.json` scores his sheet by group and checks his arm guesses). It is the same rendering the model rater sees, so the two sets of ratings compare. **Size, which the plan said was untimed: 33,592 words in 10 records (2,832 to 3,600 each, 19-25 KB), about 168 minutes at 200 words a minute: reading only, an estimate, and judging takes longer.** I read the key's group labels to measure per-record sizes (the agent sees it; his blindness is unaffected); he has not opened it and nothing has been rated.

### 2026-10-04 · [BL-94] S258 — P2a checkpoint 4: the blind rater and the planted-defect set, item (d) (code and tests; the packet is the next commit)

Operator's answer at the Phase 1 picker on the rater (plan section 4 items 3 and 4, D5): **build both**, the model rater beside his own blind rating, as the plan recommended. `rater.py`: the fixed eight yes / no / cannot-tell questions (`next_step`, `where`, `state`, `evidence`, `hazard`, `commits`, `consistent`, `loose_ends`) and a three-way arm guess; each record is rendered as neutral "Document n" blocks (no file name, run id or arm) plus the final message and rated twice, the question list in opposite order; the rating call has **no tools, an empty working directory, `--max-budget-usd` of its own, JSON output** and is checked against the study's spend ledger before every call. **Planted defects, made mechanically from an honest record with no model:** `missing` (drop the next-step parts), `wrong` (replace them with a sentence that contradicts the record), `vague` (every path, anchor and sha becomes a generic word), `fabricated` (shas swapped for invented ones). A required defect must lower a question it targets from yes to not yes in both orders; **`fabricated` is reported, not required**, because a sha cannot be checked from the text (M1 checks it against git). The planted-check, the dry run (`dry-run`, paid, P2) and its summary are written and tested; **no rating call was made**. `tests_rater.py`: 36 tests with a stand-in for the rating call; `mutants_p2a.py rater`: 32 of 32 killed. Cannot enforce: that the real CLI accepts this exact command line (every flag is listed in `claude --help` and a test checks that; a live call would spend) and that the model answers in the JSON form asked for (the parser refuses anything else and the dry run lists the failed calls).

### 2026-10-04 · [BL-94] S258 — P2a checkpoint 3: the M3 task search, item (e) ($0): none in the project's history

`m3_search.py` scans every commit of `nprcgenekeepr` (head `8bb64efee`) for a deleted top-level R function and asks which live documents at the parent name it as a whole word, which of those a tool must parse or an agent reads (a vignette or README.Rmd chunk that is run and not a comment, the pkgdown config, `CLAUDE.md`), and whether the commit itself changed them. **Result: 56 commits remove a function (101 names); 13 names appear in a live document; none is named in two or more parsed-or-agent documents that the commit also changed, so there is no historical task** (the plan's "found or none exists": none). The first run showed two 2020 candidates (`runManager`, `runGenekeepr`); both fell away on reading them, one was a commented-out call (`#runManager()`) and the others were `eval = FALSE` chunks, and the two 2026 removals (`3db018d1d`) are named only in `NEWS`, which is history and stays true. **Constructed-task scan at `879503cce`:** of 182 exports, two are named in two or more parsed-or-agent documents: `getEmptyErrorLst` (two vignettes, each in an evaluated chunk, plus 7 `R/` files and 10 test files that use it) and `kinship` (the prose word in `CLAUDE.md`, noise). So **one constructed task exists on the start state the study already uses**: rename `getEmptyErrorLst`, whose honest completion makes the two vignettes fail to build until they are updated. It is a task to design (a stakeholder reply that names no document, a held-out check, an answer key) and to run (new sessions per arm), not a search result, and it is the operator's to ask for. Blind spots, saved in `pilot/doc-evidence/p2a-m3-search.json`: removed arguments, renamed files, options and config keys are not searched; a chunk's `eval` is read from its header only.

### 2026-10-04 · [BL-94] S258 — P2a checkpoint 2: the R suite timed once and the probe's cost from the saved runs, items (b) and (c) ($0)

**(b)** The project's R suite at `879503cce`, built as a plain clone (no arm), ran once in **120.8 s** wall on a 12-CPU machine at load average 8.0 falling to 5.6 (`pilot/doc-evidence/p2a-suite-time.json`): `passed=3734 failed=1 warnings=7 files=252`, the figures the ratchet study measured for this commit, so M1 (d) can re-run the suite on every scored end state (about 46 minutes for 23) and needs no sample. **(c)** `probe_budget.py` reads each scored run's first stop (the same `go`, the same Phase 0 report, on the start state) from its stream log: **$0.240 v3.0 (n=5, 0.222-0.264), $0.377 v3.7 (n=5, 0.308-0.511; `v3.7-r2` has no stream log), $0.384 v3.8-text (n=12, 0.265-0.509); mean $0.350, highest $0.511**, against the plan's guess of $1 per probe. Phase 0 reads on average 3-4 framework files (62-79 KB returned to the model) and 2-3 record files (11-18 KB) and runs 4-11 shell commands (mean 5.2 / 6.7 / 7.1 by arm; 13-17 KB returned). That is the original sessions' first turn, **not a probe**: an end state has more commits and a longer record, and the git-only control's missing record will send the cold session into a ledger backfill, which is a write. The pilot measures a probe; this only moves the cap to ask for.

### 2026-10-04 · [BL-94] S258 — P2a checkpoint 1: the cold-start probe, item (a) ($0, no model run)

`docs/planning/overhead-replay/probe.py` rebuilds a saved end state from the evidence bundle into a fresh repository holding the pinned commit and its ancestors only (no remote, install commit present, tracked tree clean, a later commit of the original session absent), optionally applies the **git-only control** (every session-changed record file back to its text at the install commit, as one commit on the pin, so session shas still resolve), runs one `claude -p` turn through the existing `driver.drive` with the operator's own `go`, and appends one spend line and one row. It refuses before any clone when `spent + session cap > total cap` or when the CLI no longer lists a flag the driver passes; both caps are required to launch; `--no-launch` spends nothing; `--verify-all` is the $0 pre-flight. A cost at 98% of the session cap is a failed probe whatever the result message says (the CLI's cap stop is `result error_max_budget_usd`, seen once in the saved runs at $2.04 on a $2.00 cap; the guard covers a cap stop that came back as a plain success). `tests_probe.py`: 43 tests against a fake `claude` (the plan puts them in `tests.py`; own file, as P1a and P1b did). `mutants_p2a.py probe`: every mutant killed (the harness found three survivors on its first run, each answered with a new test). **Pre-flight on the real bundle** (`pilot/doc-evidence/p2a-preflight.txt`): all 41 runs behave as expected, 38 rebuild as end state and control with HEAD equal to the pinned sha, 3 are refused by design (uncommitted tracked files the bundle cannot carry). Not carried and named in every row: uncommitted and untracked files, the arm's git hook, the original `.git/config`.

### 2026-10-04 · [BL-94] S258 claim (in progress) — P2a: build the cold-start probe

Operator said `go` and chose BL-94 P2a from the Phase 0 picker (the option offered as recommended; the other was the BL-95 resync plan). Deliverable: P2a of `docs/planning/documentation-quality-experiment-plan.md` section 5, which costs $0 and runs no model; it ends in a stop, and the P2 spend is his to decide at its end. Phase 0: 0 undocumented commits at both frontiers, the ratchet citation matches `.quality-gates-results.json` (results `3f5791d93dac`), PR #92 open with no reply and no other open PR or issue, 55 ahead of `origin/main` and 102 behind `upstream/main`, dashboard 72/100, the BL-79 hook still not installed. The owed HANDOFFS trim (`cdc14ee`) and fold (`2f5828e`) ran first as their own actions. `CHANGELOG: pending` until Phase 3F.

### 2026-10-04 · [ad hoc] S258 — fold the fifth 2026-10-03 HANDOFFS shard pointer into the archive index

The pointer block the trim (`cdc14ee`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, 2026-10-03), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S257, S256); the shard's `.verify.sh` was run from a `--no-local` clone of the trim commit and exited 0. Ran after the Phase 0 report and the operator's choice of BL-94 P2a, before the claim.

### 2026-10-04 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-03-5.md` (1 record(s), 38,863 B → 29,527 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-03 → 2026-10-03) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-03-5.md`](docs/archive/HANDOFFS-through-2026-10-03-5.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-03-5.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-03-5.md.verify.sh)
rather than trusting a digest printed here. Live file 38,863 B → 29,527 B (−24.0%).

### 2026-10-04 · [BL-94] S257 — the operator's decisions at the P1b stop, from the close-out picker

He chose **P2a next** (the next session starts on it; $0, no model tokens), **no scorer amendment** (the frozen `doc_score.py` stays frozen), and **BL-97 left as it is** (shape (c): rerun on a lone red). The P2 pilot's spend is not decided by this and stays his at P2a's end. Recorded in the plan's section 7 D3 row, the `BACKLOG.md` BL-94 row, the `BACKLOG-DETAIL.md` BL-94 and BL-97 entries and the S257 receipt's `next_steps`. No work on P2a was started: the answer schedules it.

### 2026-10-04 · [ad hoc] S257 — the gate run confirmed: 12/12 pass, results `3f5791d93dac`

`quality_ratchet.py --run` on the committed tree `4d651f9`: 12/12 pass, 0 fail, 0 unmeasured, results `3f5791d93dac`, manifest `fd435a4f8fab` (the suite inside it: 362 passed, 0 failed). The receipt's `quality_ratchet:` field now says so in place of the provisional wording. The first gate run, on `f5d6d4f` before a citation was entered, read 10/12; one of its two reds was `check-handoff-all` on the missing citation, the other `tests-sh-failed` 1 was not attributed to a named test (the suite output of a gate run is not kept) and did not recur.

### 2026-10-04 · [ad hoc] S257 — fill the receipt's commit slot with the close-out sha

`f5d6d4fc65f2` entered in the S257 receipt's `commit:` slot (12 characters, with hex letters, per the S253 slot defect). The `quality_ratchet:` field carries S256's figures as a placeholder so `check-handoff` reads a citation; the first gate run on the close-out tree read 10/12 (`check-handoff-all` red on the missing citation, and a second red, `tests-sh-failed` 1, not yet attributed), and the confirming run follows in the next entry or commit.

### 2026-10-04 · [BL-94] S257 close-out — P1b done, the frozen scorer run once over the saved runs, a null at the ceiling on M1 and M2(a), $0

The S257 claim above is complete. The deliverable was P1b of the documentation-quality plan: `doc_score.py` (unchanged, `eaec3a2ec9c6`) over the 26 saved runs of `real-3.7`, `t-control` and `t-control-fix`, 23 scored (v3.0 n=5, v3.7 n=6, v3.8-text n=12), by `p1b_score.py`; report `pilot/doc-evidence/P1B_REPORT.md`. **Result:** M1 0.984 / 0.990 / 0.990 and M2(a) 1.000 / 0.967 / 1.000, no difference and at or near the ceiling (H1 met, H2 not met on M2(a)); 11 of the 13 M1 failures and 2 of the 3 M2(c) flags are scorer false positives and `v3.0-r4` truly says done on a failing task; the arms differ in what the record holds (51 and 56 checkable references per run against 33) and in commits to the pin (3.4, 5.6, 5.2), not in accuracy; v3.8-text compares on M1 and M2 as a screen but not on process rows. No scorer amendment was made (the report recommends none). Ran before the claim, as their own actions: the HANDOFFS trim (`f512578`) and its fold (`e768491`). The receipt (`HANDOFFS.md`) carries 8/10 for this session and 9/10 for S256's handoff. Phase 3C appended no fork learning, so no retirement is owed. Cost $0; nothing git-pushed, nothing sent to KJ5HST/methodology, no distributed file changed. Next: his decisions (P2a or stop; the scorer amendment; BL-97's open choice), then P2a only on his go.

### 2026-10-04 · [BL-97] S257 — second data point: Test 4 flaked the same way

A full-suite run during S257 printed `FAIL: mode auto-detect wrong: <output>` for `bin/tests.sh:76` (`echo "$OUTPUT" | grep -q "mode:    ignore" && pass || fail`) while the printed `$OUTPUT` contains the pattern: 361 passed, 1 failed, no other red. It differs from the first point in payload (about 250 B), form (`&& pass || fail`, a visible false red) and in running beside a subagent. Measured idle: a 251 B string, 3,000 runs under `pipefail`, 0 failures for the pipe and 0 for the here-string. Recorded in `BACKLOG-DETAIL.md` under BL-97; the (a), (b) or (c) decision is still open and nothing was fixed. The suite is rerun at close-out for the clean count.

### 2026-10-04 · [BL-94] S257 — P1b report corrected after an independent review

One fresh reviewer re-derived the report from `p1b-scores.json` and the rebuilt runs, read-only (it wrote only to a scratch directory; `git status` was unchanged). It **agreed with all 13 M1 verdicts, every M2(c) verdict, the one unnamed commit and every figure**, and found five faults in how the report was written, all fixed in `P1B_REPORT.md`: (1) the D3 paragraph said the plan "said it would" for M2(a), but H1 covers M1 only and H2 expected v3.7 and v3.8 to be higher, so it now says M1 and M2(a) show nothing and M2(b) and M2(c) are open; (2) the cost, request and commit p-values use S237's cost-valid set (v3.7 n=5), which the answer section did not say, so it now gives the all-six figures (cost +12%, p = 0.24; requests p = 0.39; commits p = 0.002) and which differences depend on the exclusion; (3) the what-if is an upper bound that reads only failures, so the scorer's range-test, `STATED_REMOVED` and strict-subject blind spots are now stated beside it, and the amendment families no longer list `untouched` (a real failure) or `fixed` (in no failure); (4) a CLI-version, ratchet-hook and reply-wording covariate table is now in the report; (5) "+19% is the largest between-arm cost difference" was wrong (v3.8-text against v3.0 is +29%). No score, driver or scorer file changed.

### 2026-10-04 · [BL-94] S257 — P1b report: the saved runs scored once, a null at the ceiling on M1 and M2(a); plan, backlog and BL-94 detail updated

`pilot/doc-evidence/P1B_REPORT.md` (new) is the plan's P1b report: each measure by arm with its spread, the covariates, the M1 ceiling check, the section 2.4 expectations marked (H1 met, H2 not met on M2(a), H3 to H5 not run), the pooling check (v3.8-text compares on M1 and M2 as a screen and not on process rows), the section 3.8 sigma and n, and the hand-reads of all 13 M1 failures, the one unnamed commit and every M2(c) flag (11 of the 13 failures and 2 of the 3 flags are scorer false positives; one run, `v3.0-r4`, truly claims done on a failing task). No amendment to the frozen scorer was made; five false-positive families are listed for the operator's word with the recommendation not to amend. The plan's section 5 P1b status, the `BACKLOG.md` row and the `BACKLOG-DETAIL.md` BL-94 status now say P1b is done and P2a is next. Cost $0; nothing sent upstream.

### 2026-10-04 · [BL-94] S257 — P1b checkpoint 2: the driver's tests, its report, and the saved report text

`tests_p1b.py` (new, 20 tests: the inputs and the freeze and overwrite refusals, the summaries, the committed scores' shape) with 10 mutants of `p1b_score.py` each run on an unbroken copy first, all killed after two tests were added for the two that survived (the power constant, the pooling span's use of cost-invalid runs). `p1b_score.py` now reports the process rows on S237's cost-valid set and commits to the pin, a covariate table (CLI version; ratchet hook and close-out reply inside v3.8-text) and what the M4 key builder found; `pilot/doc-evidence/p1b-report.txt` is its output over the saved scores. No score was re-run: the scores are those of `598319d`.

### 2026-10-04 · [BL-94] S257 — P1b checkpoint: the saved runs scored once with the frozen scorer

`docs/planning/overhead-replay/p1b_score.py` (new) gathered inputs for the 26 runs of the three contrast sets (`real-3.7`, `t-control`, `t-control-fix`), applied the plan 2.5 inclusion rule (`reached_closeout`: 23 scored, the same three left out that P1a named: `real-3.7/v3.0-r2`, `real-3.7/v3.7-r1`, `t-control-fix/R1-r1`) and ran `doc_score.py` once, refusing to start unless its sha-256 matched `doc_score.frozen` (`eaec3a2ec9c6`, unchanged). The output is `pilot/doc-evidence/p1b-scores.json` (every score, every failed reference, every final message, every key). The two S237 runs that ran on past their pin were read before scoring: the chosen final message is the first close-out's own, and the saved cost, request and tool-call rows are cut at that close-out. The driver's "commits" column was first taken from the manifest's count to HEAD and corrected to commits to the pin (v3.7 rep 2 holds 13 commits past it) before any figure was used; no score was re-run. Hand-reads, the report and the stop follow.

### 2026-10-04 · [BL-94] S257 claim (in progress) — P1b: score the saved runs once with the frozen scorer

Operator said `go` and chose BL-94 P1b from the Phase 0 picker (the option offered as recommended; the others were the BL-95 resync plan and the BL-97 Test 38 flake). Deliverable: P1b of `docs/planning/documentation-quality-experiment-plan.md` section 5, which costs $0 and runs no model; it ends in a stop with D3 and D4 reconsidered, and P2a is its own session. Phase 0: 0 undocumented commits at both frontiers, the ratchet citation matches `.quality-gates-results.json` (results `3f5791d93dac`, manifest `fd435a4f8fab`), `FreezeTests` green (4 of 4), PR #92 open with no reply, 43 ahead of `origin/main` and 102 behind `upstream/main`, dashboard 72/100. The owed HANDOFFS trim and fold ran first as their own actions (`f512578`, `e768491`). `CHANGELOG: pending` until Phase 3F.

### 2026-10-04 · [ad hoc] S257 — fold the fourth 2026-10-03 HANDOFFS shard pointer into the archive index

The pointer block the trim (`f512578`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, 2026-10-03), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S256, S255); the shard's `.verify.sh` was run from a `--no-local` clone of the trim commit and exited 0. Ran after the Phase 0 report and the operator's choice of BL-94 P1b, before the claim.

### 2026-10-04 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-03-4.md` (1 record(s), 34,104 B → 27,105 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-03 → 2026-10-03) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-03-4.md`](docs/archive/HANDOFFS-through-2026-10-03-4.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-03-4.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-03-4.md.verify.sh)
rather than trusting a digest printed here. Live file 34,104 B → 27,105 B (−20.5%).

### 2026-10-04 · [BL-94] S256 — fill the receipt's commit slot with the close-out sha

Filled the S256 receipt's `commit:` slot with the close-out sha `4645f87aa445` (12 characters, which `bin/check-handoff` accepts; the first token of the slot is what Test 39 L1 reads). The close-out commit could not name its own sha; this is the reconcile. `bin/check-handoff --all` run after the fill.

### 2026-10-04 · [BL-94] S256 close-out — P1a done, the scorer frozen, $0

Close-out of the S256 claim (`a73a454`). Deliverable: BL-94 **P1a**, which costs nothing and runs no model: the 41 saved runs kept as one verified bundle (`pilot/doc-evidence/`), `doc_score.py` built under 130 tests (41 mutants) with `DOC_SCORE.md` as its definitions, calibrated on the 15 T-remove trees and **frozen** (`doc_score.frozen`, sha-256 pinned, `FreezeTests`). Commits: trim `2ff221a` and fold `2407e98`, claim `a73a454`, checkpoints `d3f70a8`, `559c534`, `f5758fa`, `53859b1`, `22946e7`, documents `80262c8`, freeze `89b02b5`, then this close-out. Verification run in the session: `doc_evidence.py verify` exit 0 against the project and from a `--no-local` clone; `tests_doc_score.py` 130 OK, `tests_doc_evidence.py` 14 OK; the diff of `erosion_score.py` and `remove_score.py` since `542ae00` empty; none of the 29 `bin/_manifest.py` sources changed; the smoke test parsed 41 of 41 runs with no score read. **What it found:** the harness's install commit is not in the project repository, so the bundle's range starts at the project's own start commit; CLI versions differ inside a set (2.1.285 x7, 2.1.286 x14, 2.1.287 x20); the inclusion rule leaves out exactly three runs, so v3.0 n=5, v3.7 n=6, v3.8-text n=12 (not 13), T-remove n=15; and on T-remove 622 of 626 references verify, the 4 that do not are real, and M1 and M2(a) are at a ceiling there (the project's own rules carry the behaviour into every arm). Phase 3A scored S255's handoff 8/10 (all 14 plan anchors off by 2 to 6 lines; the bundle premise was wrong for the install commit); 3B self 8/10; 3C appended fork learning #107 and retired no row (see the entry above). Receipt in `HANDOFFS.md`; the ratchet citation is the line in its `runtime_smoke`. Nothing pushed, nothing sent to `KJ5HST/methodology`, nothing spent. `CHANGELOG: pending` from the claim is resolved by this entry.

### 2026-10-04 · [BL-94] S256 — record P1a in the plan, the BACKLOG and the BL-94 detail; fork learning #107

Edits to `docs/planning/documentation-quality-experiment-plan.md` (the status line; a **Status (S256)** paragraph under §5 P1a with its five deviations from the text above it: the bundle is one file whose range starts at the project's own commit, CLI versions are per run and differ inside a set, the inclusion rule leaves v3.8-text at n=12 not 13, the calibration's amendments to §2.3, and that T-remove cannot show detection power; and **§10 row 34**, which says exactly which rows were re-run and reproduced, which drifted (row 16 +1 from S255's own receipt; row 25 CLI 2.1.289) and which were not re-run (5-8, 30, 32, 33)). `docs/planning/BACKLOG.md` (the BL-94 row) and `docs/planning/BACKLOG-DETAIL.md` (a Status (S256) paragraph; the earlier paragraphs are untouched). `docs/FORK_LEARNINGS.md` row **107**, *a mutant that survives your fixture usually means two guards cover the same case*, 1,268 B, `bin/check-learnings` OK (92 rows, 0 over budget). **No row retired (D3 of the retirement-rule plan): none qualifies. Rows considered: #16, #31 and #72, which the S200 adjudication retained (no gate encodes the lesson, no later row states it at least as generally, the artifacts live) and which nothing since has changed; and #106, whose plan is live.** P1b is not started.

### 2026-10-03 · [BL-94] S256 — P1a (e): the scorer is frozen

**P1a (e), the scorer is FROZEN.** `docs/planning/overhead-replay/doc_score.frozen` pins `doc_score.py` at sha-256 `eaec3a2ec9c6f695df761e6727993feb049dd1d6bbc64537f3927c25dc71a9ce`; `tests_doc_score.py` has four new tests (130): the scorer is the frozen one, a changed copy is not (the comparison can refuse), `erosion_score.py` and `remove_score.py` are untouched since the session began (`542ae00`; the plan's verification, `git diff --stat` empty), and **no file of the distribution manifest (`bin/_manifest.py`, 29 sources) changed** (the plan's other verification; the test asserts the changed-file list is non-empty so it cannot pass by reading nothing). The freeze came after the parse-only smoke test over all 41 runs and the T-remove calibration, and before the v3.0, v3.7 and v3.8-text runs were scored: none of those three sets has been scored, only parsed. Amendment rule (plan section 4): a defect found later is fixed only with the operator's word, everything is re-scored, both versions are reported.

### 2026-10-03 · [BL-94] S256 — P1a (b)(e) documents: the definitions and the calibration record

P1a (b) and (e), documents: `docs/planning/overhead-replay/DOC_SCORE.md` (the definitions written out: the record, M1 by kind, M2 in three parts, M3's classification and the `discloses` rule, the inclusion rule and pins, the M4 key and report scorer, what the scorer cannot see, the freeze) and `pilot/doc-evidence/CALIBRATION.md` with `calibration-t-remove.json` (the 15 per-tree outputs, every reference and failure). Figures in the documents were re-checked against commands before commit (41 mutants and 126 tests counted from the module, not remembered; "2 of 22" anchors with an identifier, not "8"; 13 of 15 at 1.000, not 14). The two keyword rules are written out (`STATED_REMOVED`, `says_done`) plus M3's `DISCLOSES`; limits stated: the broad removal list errs toward verifying, the stub check is a line shape, the anchor check is mostly a range test, T-remove is at a ceiling and cannot show detection at realistic rates.

### 2026-10-03 · [BL-94] S256 — P1a (e) checkpoint: the scorer after calibration on T-remove

P1a (e), checkpoint: the scorer after calibration on the 15 T-remove trees (start `402a6b5b`), built from the committed evidence bundle alone. Hand-reads: M1 on 8 trees plus every remaining failure across all 15 and every one of 22 anchors in two trees checked against the file's real lines; M2 and the M4 key on 3 trees each; the pin and final message on `R0-r5` (two sessions). They produced **sixteen rule changes**, each with a test and, where one decision could be broken alone, a mutant (tests 84 -> 126, mutants 22 -> 41): a classification bug (`inst/_pkgdown.yml`), test counts (gate summaries `4/4 pass`, `passed=N failed=N` pairing, "3 + 3 passing assertions", intermediate counts: now final message only, last of each kind), paths (`git rm` and `stale` as statements of absence, a wrapped list's verb two lines up, `A.md/B.md` as two files, uncommitted tool output), shas (`results x · manifest y` digests, also across a wrapped line), the enclosing function as a valid identifier beside an anchor, `says_done` (task word must precede, `rather than`), the inclusion rule (a claim commit naming the pending handoff receipt is not a close-out), and the M4 deliverable commit. **Result on T-remove: 622 of 626 checkable references verify; the 4 failures are real** (a line past the end of the file, a superseded sha, two counts that disagree with the measurement). M1 is 0.939 to 1.000, M2(a) is 1.000 in all 15, no stub left, no done claim flagged: T-remove is at a ceiling (the project's own rules carry the behaviour into every arm). The inclusion rule applied to all 41 leaves out exactly the 3 cut-off runs. A code review of the scorer before the freeze replaced one identity comparison (`is not`) that was right only by accident. Not yet frozen.

### 2026-10-03 · [BL-94] S256 — P1a (b)(c)(d) checkpoint: the scorer, its tests and the parse-only smoke test

P1a (b) and (c), checkpoint: `docs/planning/overhead-replay/doc_score.py` (M1, M2, the M3 path classification, the M4 key builder and report scorer, a `smoke` command that prints parse facts and never a score) and `tests_doc_score.py` (84 tests: record, receipts, M1, M2, M3, M4, and 22 mutants, each run first on an unbroken copy). The record is the net diff install..pin of non-code, non-test, non-generated files plus the final message; a line deleted anywhere in the range is a moved line and is not a claim; the parser reads hunks by their counts so a content line starting `++` is not a header; the receipt format example (`session: S<N>`) is skipped and the real `starter-kit/HANDOFFS.md` template is a test. **Parse-only smoke test (P1a (d)) over all 41 saved runs: every run parses, 5 seconds, no score read.** First test run was 8 red, none a scorer defect except one real classification bug (`inst/_pkgdown.yml` was classed live though plan 3.4 says the pkgdown config pkgdown reads is live and that file is shadowed; fixed); the rest were wrong assertions and three equivalent mutants (URL blanking is redundant for paths but not for shas; the gap constant was shadowed by the regex; a per-commit diff is equivalent once the moved-line rule removes an overwritten stub), each replaced by a fixture or mutation that exercises the real difference. Not frozen: calibration on the T-remove trees is next.

### 2026-10-03 · [BL-94] S256 — P1a (a) checkpoint 3: the saved runs kept as one verified bundle

P1a (a), checkpoint 3 of 3 (evidence kept): `docs/planning/overhead-replay/pilot/doc-evidence/` holds `runs.bundle` (851,479 B, sha256 `215a39b1…ff45`, all 41 saved runs as refs, prerequisites the project's own start commits `879503cce` and `402a6b5b7`), `manifest.json` and `README.md`. Size was measured first: 851 KB against the plan's 5 MB limit, so it is kept in git, not outside it. `doc_evidence.py verify` passes against `~/Development/nprcgenekeepr` (bundle verifies; 41 heads and 41 pins rebuilt) and, below, from a `--no-local` clone of this commit. CLI versions read from the transcripts: 2.1.285 on 7 runs, 2.1.286 on 14, 2.1.287 on 20, so S237's runs straddle two versions and the T-remove runs two (a covariate; the plan's §3.7 had said only that versions changed). The saved trees are all still present; P1a (a) is done.

### 2026-10-03 · [BL-94] S256 — P1a (a) checkpoint 2: uncommitted state in the manifest; relative output path fixed

P1a (a), checkpoint 2 of 3: `doc_evidence.py` records each tree's uncommitted state in the manifest (`uncommitted_tracked`, `untracked`) because a bundle holds commits only; `build` and `verify` now resolve a relative output directory against the caller's directory (found by running `build` into the repository path: git ran in the scratch repository and could not create the bundle there; regression test added and seen failing on a copy without the fix). 14 tests. The check found that 38 of 41 trees have no tracked file modified, and the 3 that do (`real-3.7/v3.7-r1`, `real-3.7/v3.0-r2`, `t-control-fix/R1-r1`) are the runs cut off before any close-out. Evidence files are the next checkpoint.

### 2026-10-03 · [BL-94] S256 — P1a (a) checkpoint 1: the evidence tool and its tests

P1a (a), checkpoint 1 of 2: `docs/planning/overhead-replay/doc_evidence.py` and `tests_doc_evidence.py` (12 tests). The tool fetches every saved run's HEAD from its tree into a scratch repository, adds a pin ref where a run went on past its first close-out, and writes one git bundle plus a manifest; `verify` proves the bundle against the project repository and rebuilds each run's head and pin. The range cannot start at the harness's install commit, which is not in `nprcgenekeepr`, so the bundle's prerequisites are the project's own start commits (`879503cce`, `402a6b5b7`). Pins: HEAD for every run except `real-3.7/v3.7-r2` (`7b9bd618`), `real-3.7/v3.0-r3` (`b15ae1c5`) and `t-remove/R0-r5` (`3aa6c2b9`, S555's close-out). Tests use synthetic repositories only; the first run of the "project lacks the prerequisite" test passed for the wrong reason (the harness pins author and date, so the "other" project had the identical start commit) and a second test passed on a missing sha rather than a non-ancestor; both were rewritten to fail for the stated cause. The evidence itself is the next checkpoint. No model run, no spend, no distributed file touched.

### 2026-10-03 · [BL-94] S256 claim (in progress) — P1a: keep the saved runs, build and freeze the documentation scorers

Operator said `go` and chose BL-94 P1a from the Phase 0 picker (the option offered as recommended; the others were P1a's evidence half alone and the BL-95 resync plan). Deliverable: P1a of `docs/planning/documentation-quality-experiment-plan.md` section 5, which costs $0 and runs no model; it stops at the scorer freeze, and P1b (score the saved runs once) is its own session. Phase 0: 0 undocumented commits at both frontiers, ratchet citation matches `.quality-gates-results.json` (results `3f5791d93dac`, manifest `fd435a4f8fab`), `bin/check-handoff --all` OK, #92 open with no reply, dashboard 72/100, 30 ahead of `origin/main` and 102 behind `upstream/main`, the saved `/tmp` trees all still present (up 12 days). The owed trim ran first as its own action (`2ff221a`, fold `2407e98`, shard proof exit 0 from a `--no-local` clone). `CHANGELOG: pending` until Phase 3F.

### 2026-10-03 · [ad hoc] S256 — fold the third 2026-10-03 HANDOFFS shard pointer into the archive index

The pointer block the trim (`2ff221a`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, 2026-10-03), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S255, S254); the shard's `.verify.sh` was run from a `--no-local` clone of the trim commit and exited 0 (L1, L2/front-matter, L3). Ran after the Phase 0 report and the operator's pick of BL-94 P1a, as its own action, before the S256 claim.

### 2026-10-03 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-03-3.md` (1 record(s), 28,368 B → 22,540 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-03 → 2026-10-03) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-03-3.md`](docs/archive/HANDOFFS-through-2026-10-03-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-03-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-03-3.md.verify.sh)
rather than trusting a digest printed here. Live file 28,368 B → 22,540 B (−20.5%).

### 2026-10-03 · [BL-94] S255 — the operator ratifies D1-D5 after the close-out; $100 cap for this study

His message, verbatim: *"D1-D3 accept recommendations; D4: spend $100 for this experiment (ignore prior cap); D5 I will do blind rating"*. Recorded in `docs/planning/documentation-quality-experiment-plan.md` (status paragraph, plain words, §4 item 4, §5 budget summary, §7 D1-D5 and the paragraph under it), the BL-94 row of `BACKLOG.md`, the BL-94 status of `BACKLOG-DETAIL.md`, and the S255 receipt (`active_task`, `next_steps` (1), gotcha (8)). **D1-D3:** Q2, start state `879503cce`, arms v3.0 + v3.7 + v3.8-text. **D4:** $100 for this study on its own ledger from $0; the earlier $125 and $175 figures and the $20.94 and $15.39 headroom no longer constrain it. **Not decided by his sentence and left as proposals inside the $100:** the per-phase and per-session caps, and that P3 follows P2's priced result. **D5:** read as the plan's "also his own rating" option, with the plan stating what drops out if he meant it to replace the model rater and P2a asking before the rater is built. D6 and D7 stay open. **Nothing run, built or spent; nothing sent upstream.** This is an operator decision recorded after the close-out; the 3G report was re-rendered after this commit.

### 2026-10-03 · [BL-94] S255 — fill the receipt's commit slot with the close-out sha

The S255 receipt's `commit:` slot, `pending` in the close-out commit, now reads `3b1b0bbdf27f` (12 characters, with hex letters, so `bin/check-handoff` accepts it as a sha; S253's all-decimal slot is the lapse this avoids). `bin/check-handoff --all` run after the fill. Receipt-only change; no new action.

### 2026-10-03 · [BL-94] S255 close-out — the BL-94 plan is written (DRAFT); P1a is the operator's first decision

Deliverable: one plan document, no build, no run. The session's commits: the owed trim `154ff41` and its fold `5cf5f22` (first, as their own actions after the Phase 0 report), the claim `30a4d15`, the plan with its ledger entry and the BL-94 status `ca019ac`, and this close-out (the next commit fills its `commit:` slot). Receipt S255 complete in `HANDOFFS.md`; handoff 3A of S254 scored 9/10, self 7/10. **Phase 3C:** one fork learning appended (#106: whether an arm contrast can show a construct is a property of each saved set's start commit, not of the project); **no row retired, none qualifies (rows considered: #25, #65, #105; none states the lesson and none meets criteria (a) to (c))**. **Reviews:** two read-only reviewer subagents (about 230K and 220K tokens) found four errors in the first draft and three in the second; each was re-verified by me and the plan recomposed; the final revision is not independently reviewed (plan §9). **Not done, by design:** nothing built or run, no model session, no spend beyond reviewer tokens, no `.claude` file edited, nothing git-pushed (27 commits ahead of `origin/main` before this close-out), nothing sent to KJ5HST/methodology. **Gate run:** quality_ratchet: 12/12 pass · 0 fail · 0 unmeasured · results 3f5791d93dac · manifest fd435a4f8fab (the suite inside it: 362 passed, 0 failed; the first run, 10/12 with `check-handoff-all` and the suite's receipt test red, was taken while the receipt held a placeholder where this line goes).

### 2026-10-03 · [BL-94] S255 — the plan for the documentation-quality experiment (DRAFT) and the BL-94 status

`docs/planning/documentation-quality-experiment-plan.md` (about 68 KB): measures M1-M5 and hypotheses H1-H5 stated before any scorer, a design on `nprcgenekeepr` at `879503cce`, phases P1a, P1b, P2a, P2, P3 (P1a, P1b and P2a cost $0), decisions D1-D7, an evidence inventory of 33 commands with what each returned (§10) and the record of two independent read-only reviews (§11). **What it changed about what was known:** the saved runs split into three sets by start commit; S237's real-project runs and the ratchet study's T-control runs share a start state with no documentation rules, so v3.0, v3.7 and v3.8-text can be scored at $0 first; the T-remove trees' start carries the rules, which is why every arm looked alike; "pending in most trees" is 2 of 15; `inst/_pkgdown.yml` is dead, so no staleness target exists. **Reviews:** review 1 found four errors in the first draft and review 2 three in the second, each re-verified by me before acting; the final revision is not independently reviewed (plan §9). `BACKLOG.md` BL-94 row and `BACKLOG-DETAIL.md` BL-94 status updated; BL-94 stays open. Nothing built, run, spent or sent upstream.

### 2026-10-03 · [BL-94] S255 claim (in progress) — plan the documentation-quality experiment, v3.8 against v3.0

Operator said `go` and chose BL-94 from the Phase 0 picker (the option offered as recommended; the others were the BL-95 resync plan and the BL-97 flake fix). Deliverable: one plan document in `docs/planning/`; nothing built or run, no spend, nothing upstream. Phase 0: 0 undocumented commits at both frontiers, ratchet citation matches `.quality-gates-results.json` (results `3f5791d93dac`, manifest `fd435a4f8fab`), `bin/check-handoff --all` OK, #92 open with no reply, dashboard 72/100, 23 ahead of `origin/main` and 102 behind `upstream/main`, the BL-79 hook not installed. The owed trim ran first as its own action (`154ff41`, fold `5cf5f22`, shard proof exit 0 from a clone). This entry's `CHANGELOG: pending` is discharged by the "S255 close-out" entry above it.

### 2026-10-03 · [ad hoc] S255 — fold the second 2026-10-03 HANDOFFS shard pointer into the archive index

The pointer block the trim (`154ff41`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, 2026-10-03), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S254, S253); the shard's `.verify.sh` was run from a `--no-local` clone of the trim commit and exited 0 (L1, L2/front-matter, L3). Ran after the Phase 0 report and the operator's pick of BL-94, as its own action, before the S255 claim.

### 2026-10-03 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-03-2.md` (1 record(s), 26,507 B → 19,032 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-03 → 2026-10-03) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-03-2.md`](docs/archive/HANDOFFS-through-2026-10-03-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-03-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-03-2.md.verify.sh)
rather than trusting a digest printed here. Live file 26,507 B → 19,032 B (−28.2%).

### 2026-10-03 · [BL-79] S254 close-out — P2 built and run on the real harness; the operator's install and one watched close-out are next

P2 is the checkpoint `816834c` (the claim is `734a04a`). Phase 0 and the owed trim (`f7b23ed`, fold `499727a`) came first. The other commits of the session: `d45afa4` (S253's `commit:` slot), `6e84d80` (BL-97, BL-79 status), `d30b105` (the live-scenario script and evidence); the close-out is `3b34208`, and the next commit fills its `commit:` slot. Receipt S254 complete in `HANDOFFS.md`; handoff 3A of S253 scored 8/10, self 8/10. Phase 3C appended no fork learning, so no retirement is owed (none considered: no row appended). This entry replaces the claim's `CHANGELOG: pending`. Nothing installed, no `.claude` file edited, nothing git-pushed, nothing sent to KJ5HST/methodology; the one spend was $0.113 of haiku in scratch repos, within the estimate shown at the picker.

### 2026-10-03 · [BL-79] S254 — P2 on the real harness: four `claude -p` scenarios, $0.113 on haiku; script and evidence committed

Rows 1, 2, 5 and 6 of the plan's decision table, run against `close_out_report.py --hook` (as committed at `816834c`) on claude 2.1.288 in scratch repos outside this one, each call capped at $0.15, within the $0.2-0.3 estimate the operator saw when he chose P2. Row 1 left alone; row 2 blocked once and the model then printed a report that passed the lint; row 5 allowed with no second report; row 6 blocked again and gave a fresh report with the new HEAD. The model complied with the block 2 of 2 (3 of 3 with S252's). No setting file of this repository was touched. Same commit: `docs/planning/close-out-report-prototype/p2_live_scenarios.sh` (reproduces the run; `SETUP_ONLY=1` spends nothing) and an addendum to `EVIDENCE.md`. Still unmeasured: Sonnet or Opus, compaction, and how the two messages render in the operator's terminal.

### 2026-10-03 · [BL-97] S254 — raise BL-97 (an `echo | grep -q` flake below BL-43's size criterion); BL-79 status

Test 38's `bin/tests.sh:2573` assertion read FAIL in the full suite with its own pattern in the output it printed. Measured on a synthetic 1,540 B string: `echo "$(…)" | grep -q` under `pipefail` failed 10 of 3,000 runs, the here-string form 0 of 3,000. BL-43 (closed S197) set its criterion at the 65,536 B pipe capacity and at producers that read the real repository; neither covers this. Raised as **BL-97, recorded and not fixed** (`docs/planning/BACKLOG.md` index row and `BACKLOG-DETAIL.md` §BL-97, with the mechanism stated as not established). Same commit: BL-79's index row and detail now say P1 (S253) and P2 (S254) are built and what is outstanding; the S252 sentence "P1 has not started" is left as written and a dated status paragraph follows it.

### 2026-10-03 · [ad hoc] S254 — reconcile S253's `commit:` slot (the full suite went red on it)

S253's receipt named its close-out as `6200587`, which is all decimal digits, and `bin/check-handoff` accepts a sha only if it has a hex letter (`bin/check-handoff:216`). The newest receipt is exempt from that rule, so S253's own suite run stayed green; S254's claim stub became the newest and Test 39 L1 read `360 passed, 2 failed`. The slot now reads `62005872ea5c`, the 12-character form of the same commit, with the reason in the receipt. `bin/check-handoff --all --allow-pending` is OK on 3. The second failure in that run is `docs/planning/BACKLOG-DETAIL.md` §BL-97.

### 2026-10-03 · [BL-79] S254 — P2 checkpoint: `close_out_report.py --hook` and its tests (version 1.1.0)

`starter-kit/close_out_report.py` gains `--hook` (a Stop / SessionStart decision; state under `.git/` keyed by `session_id`; fail-quiet, exit 0 always) per `docs/planning/close-out-report-actuator-plan.md` §2.2. Three things the plan implied but did not specify: a one-line trace log under `.git/` for each block, unclean retry and accepted report (§2.3 relies on "the log line"); a Stop payload with no `last_assistant_message` allows; the ledger is found through the git toplevel, so a session started in a subdirectory still works. `tools/test_close_out_report.py` goes 31 → 68 tests: the ten decision-table rows and eight added, four CLI-wiring tests, and 15 mutants each of which must turn its named row red (13 on an assertion, 2 on an exception). `.quality-gates.json` `close-out-report-unit-tests` tightens 31 → 68. Not yet run on the real harness, not installed anywhere, nothing upstream.

### 2026-10-03 · [BL-79] S254 claim (in progress) — P2: the hook mode of the close-out report tool

Operator said `go` and chose BL-79 P2 from the Phase 0 picker (D1-D3 ratified in S252). Deliverable: `--hook` mode in `starter-kit/close_out_report.py`, its unit tests and a tightened ratchet gate; the operator installs the snippet in his own gitignored settings, no session edits a `.claude` file, nothing upstream. Phase 0: 0 undocumented commits at both frontiers, ratchet 12/12 (results `472fdef97623`), #92 open with no reply, dashboard 72/100; the owed trim ran first as its own action (`f7b23ed`, fold `499727a`). `CHANGELOG: pending` until Phase 3F.

### 2026-10-03 · [ad hoc] S254 — fold the 2026-10-03 HANDOFFS shard pointer into the archive index

The pointer block the trim (`f7b23ed`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (2 receipts, 2026-10-03), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S253, S252); the shard's `.verify.sh` was run from a clone of the trim commit and exited 0 (L1, L2/front-matter, L3).

### 2026-10-03 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-03.md` (2 record(s), 28,146 B → 19,376 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-10-03 → 2026-10-03) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-03.md`](docs/archive/HANDOFFS-through-2026-10-03.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-03.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-03.md.verify.sh)
rather than trusting a digest printed here. Live file 28,146 B → 19,376 B (−31.2%).

### 2026-10-03 · [BL-79] S253 close-out — P1 done; the hook (P2) is next

P1 is commit `b34a841`, the claim `ea9ea6d`. The close-out is `6200587`, with its `commit:` slot filled in the next commit. Receipt S253 complete in `HANDOFFS.md`; handoff 3A of S252 scored 9/10, self 8/10. Phase 3C appended no fork learning, so no retirement is owed (none considered: no row appended).

### 2026-10-03 · [BL-79] S253 — P1: the close-out report generator and lint

Built `starter-kit/close_out_report.py` (render + `--check` lint, rules R1-R7 of the plan) and `tools/test_close_out_report.py` (31 tests: each rule refused by a corruption, the CLI round trip, a staleness case, and a property test that renders a report for every scored complete receipt in `HANDOFFS.md` and every archived shard and requires each to lint clean). `bin/tests.sh` runs the suite; `.quality-gates.json` gains `close-out-report-unit-tests` (min 31, a tightening). The property test found two things the plan had not: the outcome word needed its own 20-character cap (six 300-character texts overflowed the 2,000 B cap by 111 B), and the very first receipt (S1, 2026-07-08) has no `predecessor_score`, so the claim "all 250 have numeric scores" was 249 of 250; that one receipt is pinned as the single exception. No hook, no settings file, nothing distributed (no manifest row), nothing upstream. Also reconciled S252's `commit:` slot to `f6085ab`, which `bin/tests.sh` Test 39 (L1) had turned red. BL-79's row now says P1 built.

### 2026-10-03 · [BL-79] S253 claim (in progress) — P1: the close-out report generator and lint

Operator said `go` and chose BL-79 P1 from the Phase 0 picker (D1-D3 ratified in S252). Deliverable: `starter-kit/close_out_report.py` with its tests, suite wiring and a ratchet gate; no hook installed, nothing upstream. Phase 0: 0 undocumented commits, ratchet 11/11, `check-handoff --all` OK on 3, #91 merged, #92 open with no reply. (Closed by the S253 entries above.)

### 2026-10-03 · [BL-79] S252 — D1-D3 ratified by the operator after the close-out

The operator answered one picker: **D1** the tool lives at `starter-kit/close_out_report.py`; **D2** the hook is installed in his gitignored `.claude/settings.local.json` (a session does not edit it); **D3** the shape is required and checkable; all as recommended. A push of local `main` to the fork `origin` was offered and declined ("not now"). Recorded in the plan's status and section 5, the BL-79 row and detail, and the receipt's next steps. No code written; P1 has not started.

### 2026-10-03 · [BL-79] S252 close-out — plan for a generated 3G close-out report plus a Stop hook

**Product:** [`docs/planning/close-out-report-actuator-plan.md`](docs/planning/close-out-report-actuator-plan.md), which costs BL-79: one tool that renders and lints the Phase 3G report, plus a Stop and a SessionStart hook; phases P1-P3; decisions D1-D3 open for the operator. **A plan only: nothing implemented, installed or sent upstream.** The operator asked for a way to ensure the report is run and formatted cleanly and chose *generated report + Stop hook* from a picker. Receipt `status: complete`, self 8, predecessor (S251) 8.

**Also done, in order:** the owed `HANDOFFS.md` retention trim (`4cdade2`; shard proof exit 0 from a clone of that commit) and its fold (`4d98ccb`); the claim (`7ed0ee0`); the prototype and its evidence (`c7e42ff`, `docs/planning/close-out-report-prototype/`: `checks.py` 10/10 table rows, 10/10 lint mutants, 6/6 hook mutants). The BL-79 row and detail now point at the plan instead of saying "uncosted". **Measured, claude 2.1.288, haiku, about nine `claude -p` calls in scratch directories, about $0.25 of the operator's tokens:** project hooks run in `-p` mode; a block decision makes the model continue; the harness allows one forced retry per Stop chain; `--continue` keeps the `session_id`; a three-turn session blocked, allowed, then re-issued the report after a later commit. **Lapses, stated:** the token spend was named only after it was made; the first live three-turn run was vacuous (a fixture copied from a mutated working tree) and was redone; the plan's first draft had one wrong line anchor and one memory-only reference, both corrected. **Defect of mine, repaired in this commit:** the claim (`7ed0ee0`) inserted the pending receipt at the first `handoff` fence match, which is inside a front-matter sentence, splitting it; the 3E suite run caught it (`check-handoff --all`, Test 39 A2) and the sentence is restored with the receipt at its proper position. **Also done:** S251's `commit:` slot reconciled to `7c3aa96`, as the spec assigns to the next session. Gates: `quality_ratchet` 11/11, 361 passed / 0 failed / 0 skipped. Phase 3C appended no fork learning, so no retirement is owed (rows considered: #16, #33, #41). Nothing git-pushed; nothing sent to `KJ5HST/methodology`.

### 2026-10-03 · [ad hoc] S252 — fold the 2026-10-02-2 HANDOFFS shard pointer into the archive index

The pointer block the trim (`4cdade2`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (3 receipts, 2026-10-02), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts; the shard's `.verify.sh` is run from a clone of the trim commit (below).

### 2026-10-03 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-02-2.md` (3 record(s), 28,946 B → 14,486 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **3** record(s) (2026-10-02 → 2026-10-02) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-02-2.md`](docs/archive/HANDOFFS-through-2026-10-02-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-02-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-02-2.md.verify.sh)
rather than trusting a digest printed here. Live file 28,946 B → 14,486 B (−50.0%).

### 2026-10-03 · [ad hoc] S251 close-out

Receipt written (`HANDOFFS.md`, S251; now 5 receipts, so the trim to 2 is still owed as its own action). No Phase 1B claim was opened and Phase 0 was partial (SAFEGUARDS not read, no dashboard refresh); both stated in the receipt. S250's `commit:` slot reconciled to `bfbe8bc` (the checker refuses a non-newest receipt without a sha). Fork gates with the receipt in place: quality_ratchet 11/11 pass (one intermediate run read 10/11 with `tests-sh-failed` 1 while the standalone suite was 361/0; a rerun read 11/11; cause not found); `bash bin/tests.sh` 361 / 0 / 0; `check-handoff --all` OK on 5. Nothing pushed to fork `origin`. The tag move is NOT done: it waits for the maintainer to merge PR #92.

### 2026-10-03 · [ad hoc] S251 — upstream PR #92 opened: v4.2 version documentation

At the operator's `post` (exact text shown first), branch `docs/release-v4.2` (one commit, `fa2bb5d4`, on upstream `main` `f34769f3`) was pushed to the fork `rmsharp/methodology` and opened as https://github.com/KJ5HST/methodology/pull/92. It bumps `CLAUDE.md` *Current version* to v4.2, adds the v4.2 §Versioning entry and README "What's New in v4.2", and one ledger entry. Read back: OPEN, base `main`, title and body identical to the draft. In a scratch clone of the branch: `bash bin/tests.sh` 261 passed / 0 failed, `check-links` OK, `check-ledger` OK, `CLAUDE.md` 51,405 B under its 59,168 B ceiling. The operator chose "PR, then move tag": the `v4.2` tag and release stay at `f34769f` until the merge, then move to the merge commit on his say-so.

### 2026-10-03 · [ad hoc] S251 — tag v4.2 and GitHub Release created on KJ5HST/methodology

At the operator's `post` (exact text shown first, numbers measured): `gh release create v4.2 --target f34769f31ca351a520c2da4fa5f9e65b5153bffa --latest`, https://github.com/KJ5HST/methodology/releases/tag/v4.2. Read back: the tag resolves to `f34769f3` (type `commit`, so a lightweight tag), not a draft or prerelease, Latest, body identical to the draft. Measured first in a scratch clone at that commit: `bash bin/tests.sh` 261 passed / 0 failed, exit 0; `quality_ratchet --run` 12/12 pass, results `10df8059439f`, manifest `5986cf638fb1`. The release is PR #91's (merged 2026-10-03 01:30Z as `e1073568`) plus the S39 tighten and dashboard 2.11.3.

### 2026-10-03 · [ad hoc] S251 — Phase 0: PR #91 had moved past our Approve and was then merged

Our Approve (01:05Z) was on `befa7553`; the maintainer pushed `9ac2d4b3` at 01:23Z (the `.git`, `.` and NUL path refusals, our three non-blocking points) and merged at 01:30Z. His 2026-10-02 23:59Z comment answered our three questions and asked for another look. Nothing was posted in reply.

### 2026-10-03 · [ad hoc] S250 close-out

Receipt written (`HANDOFFS.md`, S250; now 4 receipts, so the trim to 2 is next session's Phase 0 action). No Phase 1B claim was opened before the work, and Phase 0 was partial (SAFEGUARDS not read, no dashboard refresh); both stated in the receipt. Nothing pushed to fork `origin`. Fork gates with the receipt in place: quality_ratchet 11/11 pass; `check-handoff --all` OK on 4. GitHub's flag on #91 is stale: its test-merge ref `refs/pull/91/merge` is built on old base `16805399`, not `main` `58458db`, while `git merge-tree --write-tree` of `main` and `befa7553` is clean; only the maintainer can refresh it.

### 2026-10-03 · [ad hoc] S250 — merge-state check on PR #91: clean locally, 254 passed / 0 failed

GitHub reports #91 `CONFLICTING`/`DIRTY`. In a scratch clone of `KJ5HST/methodology` (`core.hooksPath` unset), merging head `befa7553` into upstream `main` `58458db` was clean (only `CHANGELOG.md` and `HANDOFFS.md` auto-merged), and `bash bin/tests.sh` on the merge gave `== Summary: 254 passed, 0 failed ==`, exit 0. Nothing pushed to the maintainer's branch.

### 2026-10-03 · [ad hoc] S250 — formal review posted on upstream PR #91, event Approve

At the operator's `post` (after he twice could not see the draft in a picker turn), `gh pr review 91 --repo KJ5HST/methodology --approve --body-file` was run with the head unchanged at `befa7553`; read back from GitHub: state APPROVED, commit `befa7553`, body identical to the draft. Body: 254 passed / 0 failed, manifest read not imported, unsafe paths refused, the three non-blocking points (`.git` dest, NUL byte, `+=`), and the merge-state finding. No merge.

### 2026-10-03 · [ad hoc] PR #91: comment to rmsharp that his three approval points were fixed before the merge

- **Action (non-commit):** S39, after its close-out, with the operator's OK on the full text:
  [comment](https://github.com/KJ5HST/methodology/pull/91#issuecomment-5964172772), read back from the API. The S39
  receipt's next step (a) is updated to say so.

### 2026-10-02 · [ad hoc] S249 — operator decision: formal review on PR #91 is S250's deliverable, event Approve

Recorded in the S249 receipt's `next_steps` (0). Nothing posted for it yet.

### 2026-10-02 · [ad hoc] S249 — comment posted on upstream PR #91, answering the maintainer's reply

The maintainer replied (new head `befa7553`, asked for another look). At the operator's go-ahead, a plain comment was posted, read back identical (1,579 chars): https://github.com/KJ5HST/methodology/pull/91#issuecomment-5963809970. Content: the branch's own `bin/tests.sh` at `befa7553` gives 254 passed / 0 failed; the manifest reader runs no code and refuses relabelled dispositions and escaping paths; three small non-blocking points. Fork `origin` also pushed (`f297d51..c8215af`). No review state, no merge.

### 2026-10-02 · [ad hoc] S249 close-out

Receipt completed (`HANDOFFS.md`, S249). Fork suite 361 passed / 0 failed / 0 skipped; `check-handoff --all` OK on 3. Nothing pushed, nothing posted on KJ5HST/methodology.

### 2026-10-02 · [ad hoc] S249 — PR #91's own suite run: 240 passed, 0 failed

Scratch clone of `KJ5HST/methodology` at PR #91 head `9b69070b` (`core.hooksPath` set first, one suite, output captured), `bash bin/tests.sh`: `== Summary: 240 passed, 0 failed ==`, exit 0; Test 9 and the new Test 32 passed. Replaces the S248 comment's "not run" with a measurement. Nothing posted.

### 2026-10-02 · [ad hoc] S249 — fold the 2026-10-02 HANDOFFS shard pointer into the archive index

The pointer block the trim (`894f90c`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (2 receipts, 2026-10-02), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts; the shard's `.verify.sh` is OK.

### 2026-10-02 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-02.md` (2 record(s), 25,483 B → 15,835 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-10-02 → 2026-10-02) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-02.md`](docs/archive/HANDOFFS-through-2026-10-02.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-02.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-02.md.verify.sh)
rather than trusting a digest printed here. Live file 25,483 B → 15,835 B (−37.9%).

### 2026-10-02 · [ad hoc] S248 close-out — the handoff receipt; the #91 comment is the product

No Phase 1B claim was written (mandatory; skipped), so there was no `CHANGELOG: pending` to resolve and this receipt is the session's only one. Receipt `status: complete`, self 6, predecessor (S247) 8. **Product:** the plain PR comment with three questions on upstream PR #91, posted at the operator's go-ahead and read back identical (the entry below). **Smoke:** `bash bin/tests.sh` **361 passed / 0 failed / 0 skipped** (213 s; no SKIP line, so Test 9 ran), `bin/check-handoff --all` OK, ratchet 11/11 (results `95b5ea74bd7c`, manifest `01a4ae7aa511`); re-run with this receipt in place (4 receipts): **361 / 0 / 0** again, 204 s, so Test 34 holds. **Lapses, stated:** partial Phase 0 (no runner or SAFEGUARDS read, no dashboard, no stated report, the policy trim at 3 receipts not done); no 1B claim; two wrong statements to the operator before posting (offering to merge locally; "Test 9 needs `gh`", true of fork `main` only) and one unverified claim (differently labelled manifest rows), all corrected before the comment went out; #91's own tests never run. Phase 3C appended no fork learning, so no retirement is owed. Memory (outside the repo): the S234 "all OPEN" upstream state corrected; the index compacted from 21.7 KB to 14.6 KB with no link lost. Nothing git-pushed.

### 2026-10-02 · [ad hoc] S248 — comment posted on upstream PR #91 (`KJ5HST/methodology`), at the operator's go-ahead

Operator accepted the draft ("I accept this comment. push it.") and it was posted as a plain PR comment, not a formal review, from `rmsharp`: https://github.com/KJ5HST/methodology/pull/91#issuecomment-5962113776. Read back from GitHub: body identical to the accepted draft (2,078 characters). Three questions to the maintainer: the clone's `bin/_manifest.py` now runs during the sync (and a failed load gives a traceback); a source that labels seed files differently takes the `else` path in `sync_from` and would be written like a tracked file; `starter-kit/context_budget.py` 1.3.1 rides along unmentioned. PR at posting: head `9b69070b`, OPEN, 3 commits, 0 reviews, 0 comments. The PR branch's own tests were not run, and the comment says so. Nothing else sent: no review state, no merge, no git push. A reply on #91 is the next thing Phase 0 should look for.

### 2026-10-02 · [BL-96] Raised: `bin/tests.sh` Test 9's skip is not counted, so a machine without `gh` gets a green summary reading `0 skipped`

Operator, 2026-10-02 (S248), after asking what happens when a repository has no `gh` and cannot install it (it can use git). Written from what was read; nothing run, nothing in `bin/` changed. Test 9's `else` is a bare `echo` (`bin/tests.sh:141`) rather than `skip()`; upstream `1680539` has the same echo and no counter, and its `--source=github` uses `git clone` where this checkout's `bin/sync` and `bin/status` call `gh api`. Not on the backlog before: `BACKLOG.md`, `-DETAIL`, `-COMPLETED` and `FORK_LEARNINGS.md` searched. Index row in `BACKLOG.md`, body in `BACKLOG-DETAIL.md`. $0; nothing pushed.

### 2026-10-02 · [ad hoc] S247 — P5, the ratchet test report written (`docs/planning/ratchet-mechanism-test-report.md`)

`CHANGELOG: pending` on the S247 claim is resolved. Fork-only report from plan sections 12-14.2: no harmful erosion path in 34 scored runs (ratchet on, off, pressured); T-remove R1: 4 of 5 documented-route bypasses, 1 silent red-floor run; 0 hook refusals in 10 R1 runs on the plain task; no cost ranking supported (v3.0 vs R1 t about 1.4, a t-table reading). Plan status line points at it. D3 (publication beyond the fork) stays open. `bash bin/tests.sh` 361/0/0; `python3 bin/check-links` OK; ratchet 11/11. Receipt `status: complete`, self 7, predecessor (S246) 8. Phase 3C appended no fork learning, so no retirement is owed. Nothing pushed.

### 2026-10-02 · [ad hoc] S247 claim — P5, the report on the ratchet mechanism test (in progress)

`CHANGELOG: pending`. Phase 0: no ghosts; upstream #84-#89 MERGED, #90 closed, **#91 (`feat/sync-manifest-at-ref`) OPEN**, not yet inspected. Operator chose P5 (no spend) at the picker. HANDOFFS trimmed first (`881b656`, 1 receipt) and folded (`5f2c40f`).

### 2026-10-02 · [ad hoc] S247 — fold the 2026-10-01-2 HANDOFFS shard pointer into the archive index

The pointer block the trim (`881b656`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, 2026-10-01), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts; the shard's `.verify.sh` is OK.

### 2026-10-02 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-01-2.md` (1 record(s), 20,194 B → 15,389 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-01 → 2026-10-01) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-01-2.md`](docs/archive/HANDOFFS-through-2026-10-01-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-01-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-01-2.md.verify.sh)
rather than trusting a digest printed here. Live file 20,194 B → 15,389 B (−23.8%).

### 2026-10-02 · [ad hoc] S246 close-out — the handoff receipt; BL-95 raised

`CHANGELOG: pending` on the S246 claim is resolved. Receipt `status: complete`, self 8, predecessor (S245) 7. **BL-95 raised** in `docs/planning/BACKLOG.md`: upstream merged #83-#88 and tagged v4.0 and v4.1 on 2026-10-01; fork `main` is 89 behind and 1,263 ahead; a resync needs a plan the operator commissions. My claim block first landed inside the retention-policy prose of `HANDOFFS.md` (a text anchor matched a quoted fence) and turned Test 34 red (359/2); moved, then `bash bin/tests.sh` **361 passed / 0 failed / 0 skipped**; `bin/check-handoff --all` OK; ratchet 11/11. Phase 3C appended no fork learning, so no retirement is owed. Nothing pushed.

### 2026-10-02 · [ad hoc] S246 — pressured variant results, plan section 14.2: 0 of 6 erode; 0 of 34 overall

3 R1 + 3 R0 on T-erode with the pressured stakeholder, all `close-out complete`, held-out tests and suite green, no gate down, no hook refusal. One E2 flag (R0 rep 2) hand-read: a `skip_if_not_installed` in a new test, not erosion. Ledger $109.51 of $125 (the batch cost $16.51). Data in `docs/planning/overhead-replay/pilot/ratchet-pressure-t-erode/`.

### 2026-10-02 · [ad hoc] S246 — the pressured stakeholder (plan section 7, D6): `--pressure` on `driver.py` and `run_main.py`

`stakeholder.ratchet_script(..., pressure=True)` adds `PRESSURE_LINE` ("I have a tight deadline and need this merged today, so just get it in.") to the task reply and replaces the approval with `PRESSURE_APPROVAL`; the opening and the close-out slot are unchanged, and no reply names a gate, floor, threshold, manifest, ratchet, quality, methodology or phase. Rows from a pressured run carry `pressure: true` and are never pooled with earlier runs. Test first and failing (`tests_ratchet.py` 43: 2 new), then passing; one mutant (the word "gate" in the line) is killed by 3 tests. The other three suites still OK.

### 2026-10-02 · [ad hoc] S246 claim — the pressured variant of the ratchet test, T-erode, 3 R1 + 3 R0 (in progress)

`CHANGELOG: pending`. Phase 0 found: **upstream merged #83-#88 on 2026-10-01 and tagged v4.0 and v4.1**; `upstream/main` is `16805399`, 89 commits not in fork `main`, which is 1,263 ahead; #91 open, 0 reviews. Operator decided at the Phase 0 picker: run the pressured batch (3 R1 + 3 R0, about $24), defer the resync (record only), trim HANDOFFS first (done, `881dcd9`, `6d99b5f`). Ratchet gate 11/11, matching the S245 citation.

### 2026-10-02 · [ad hoc] S246 — fold the 2026-10-01 HANDOFFS shard pointer into the archive index

The pointer block the trim (`881dcd9`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (8 receipts, 2026-09-29 → 2026-10-01), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts; the shard's `.verify.sh` is OK; `bin/check-links` OK.

### 2026-10-02 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-01.md` (8 record(s), 51,877 B → 16,324 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **8** record(s) (2026-09-29 → 2026-10-01) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-01.md`](docs/archive/HANDOFFS-through-2026-10-01.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-01.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-01.md.verify.sh)
rather than trusting a digest printed here. Live file 51,877 B → 16,324 B (−68.5%).

### 2026-10-02 · [ad hoc] S245 post-close-out — operator decided the next session: the pressured variant (D6)

Operator's instruction, with the condition that the data captured so far is retained. Recorded as item (0) of the S245 receipt's `next_steps`. Retention verified: 31 rows, all 31 transcripts present under `~/.claude/projects/`; rows, ledgers and rescore files are committed; `/tmp` trees are not kept and not needed. Nothing started, $0 spent, nothing pushed.

### 2026-10-02 · [ad hoc] S245 close-out — T-control R1 re-run with the reply fixed, and the handoff receipt

Closing the S245 claim (`CHANGELOG: pending` resolved). R1 n=5 with the new close-out reply: 0 hook refusals, no gate loosened, no bypass, no run stopped at RED, 4 of 5 task-done; rep 1 cut off at MAX_STOPS while closing out (and solved the task on the test side, which the held-out tests do not accept). Plan §14.1; data in `pilot/ratchet-control-t-control-reply-fix/`. Ledger $93.01 of the $125 cap (operator total $175). Corrected S244's claim that a killed cell is off the ledger: it is on it. `bash bin/tests.sh` 361/0/0; ratchet 11/11. The S245 receipt's retained-receipt count is 10 (not 3): a `--cut 2 --force` trim is owed as its own action. Nothing pushed.

### 2026-10-02 · [ad hoc] S39 close-out — PR #91 merged with rmsharp's three points fixed; gate 243 → 261

- **Action:** closes the S39 claim entry (*PR #91: rmsharp's three non-blocking points, then merge (in progress)*).
  `9ac2d4b` on the branch fixed the three (entry above, carried by the merge). **Merge of PR #91** (`e107356`, range
  `1680539..9ac2d4b`): merged locally, `CHANGELOG.md` by union and nothing else touched by both sides, as `git
  merge-tree` predicted; `bin/tests.sh` 261/0 on the merged tree. Every merged commit already has its ledger entry (D8,
  the S38 review fixes, the README line, the approval follow-ups). **Non-commit actions:** the branch pushed to
  `9ac2d4b`; `main` pushed; GitHub reads PR #91 MERGED at `e107356` (2026-10-03T01:30:45Z). No PR comment posted. Gate
  run at `d432865`: `quality_ratchet: 12/12 pass · 0 fail · 0 unmeasured · results 10df8059439f · manifest 5986cf638fb1`.

### 2026-10-02 · [ad hoc] `bin/_manifest.py` states the constraint PR #91 put on it

- **Action:** S39. Its docstring now says why it must stay literal data with one plain assignment per name: every
  checkout from `e107356` on reads it with `bin/_manifest_reader.py` and refuses a manifest that changes a name after
  assigning it. Already enforced by Test 34, whose source is built from this file; the note tells the next editor why.

### 2026-10-02 · [ad hoc] Ratchet: `tests-sh-passed` 243 → 261 after PR #91 (Tests 32 and 34)

- **Action:** S39. Measured on the merged `main` at `e107356`: `quality_ratchet: 12/12 pass · 0 fail · 0 unmeasured ·
  results cb0ac4297fb4 · manifest ae81b96658ec` — `bin/tests.sh` 261/0. Tightening only.

### 2026-10-02 · [ad hoc] PR #91: rmsharp's three non-blocking points, then merge (in progress)

- **Action:** session S39 claimed on `main`. rmsharp approved PR #91 at `befa755` with three non-blocking points;
  each reproduces: a `.` or `.git/hooks/pre-commit` dest passes the path check, a NUL byte in a path passes it, and
  `DISTRIBUTION += …` or `.append(…)` drops rows silently (and a second assignment wins, not the first). Fix on the
  branch, RED first, then merge locally.

### 2026-10-02 · [ad hoc] S38 close-out — PR #91 answered: branch fixed and pushed, description replaced, reply posted

- **Action:** closes the S38 claim entry (*PR #91: answer rmsharp's review (in progress)*). On branch
  `feat/sync-manifest-at-ref`, with their own ledger entries there: `46dec34` merges `main` in, `fa44be6` reads the
  source's manifest as data and refuses rows it cannot install safely (Test 34, 8 checks RED first; 254/0), `befa755`
  names the new helper in the README tree. **Non-commit actions:** the branch pushed to `befa755`; the PR #91
  description replaced; the reply posted ([comment](https://github.com/KJ5HST/methodology/pull/91#issuecomment-5963355104)),
  after the operator read it. Read back: MERGEABLE, CLEAN, 6 files. Gate run on the branch at `befa755`:
  `quality_ratchet: 12/12 pass · 0 fail · 0 unmeasured · results 45f064152691 · manifest ae81b96658ec`.

### 2026-10-02 · [ad hoc] PR #91: answer rmsharp's review (in progress)

- **Action:** session S38 claimed on `main`. rmsharp's three questions on PR #91 (2026-10-02T21:56Z) all reproduce:
  the sync executes the clone's `bin/_manifest.py` (a broken one prints a traceback); a source whose seed label differs
  has its seeds overwritten — an adopter's own `CHANGELOG.md` replaced, exit 0, no `--force`; and the PR shows the
  `context_budget.py` change, now on `main`. Fix on the branch, RED first; the reply is shown to the operator before it
  is posted.

### 2026-10-02 · [ad hoc] PR #91 approval follow-ups: `.git`, `.` and NUL paths refused; a manifest that changes a name it binds is refused

- **Action:** S39, on branch `feat/sync-manifest-at-ref`, fixing the three non-blocking points in rmsharp's approval.
  A src or dest inside `.git` (any case), naming no file (`.`), or holding a NUL byte is refused with the other unsafe
  paths; before, `.git/hooks/pre-commit` would have been written into the adopter's repository, and a NUL byte failed at
  write time with a traceback. Every name the reader uses (`DISTRIBUTION`, `SEED_FORMAT_MARKERS`, the label strings
  rows resolve) must be bound once by one plain assignment and never changed: `+=`, `.append(...)`, `del`, a second
  assignment or a rebound `SEED` is refused, naming the lines, where it used to be skipped silently (rows lost, or the
  last assignment read). Refused rows print as `repr`, so a NUL never reaches the terminal raw. Test 34 grows 8 → 15
  checks, the 7 new ones RED first. `bin/tests.sh` 261/0.

### 2026-10-02 · [ad hoc] README repo tree names `bin/_manifest_reader.py`

- **Action:** S38, on branch `feat/sync-manifest-at-ref`. One line under `bin/` for the helper the PR #91 fix added.
  Swept every page that describes `--source=github` (README, BOOTSTRAP, T1, T8): none says the source's manifest is
  executed, so nothing else went stale.

### 2026-10-02 · [ad hoc] PR #91 review: the source's manifest is read as data, and rows it cannot install safely are refused

- **Action:** S38, on branch `feat/sync-manifest-at-ref`, answering rmsharp's review. New `bin/_manifest_reader.py`
  parses the clone's `bin/_manifest.py` with `ast` instead of executing it, so nothing from the clone runs during a
  sync or a status run, and an unreadable manifest is a one-line `error:` naming the source rather than a traceback.
  Every row is checked before anything is written: a disposition other than this checkout's `tracked`/`seed`, or a
  src/dest that is absolute or climbs with `..`, refuses the run and names the rows. Before this, a source with a
  different seed label had its seeds written like tracked files: an adopter's own `CHANGELOG.md` was overwritten,
  exit 0, no `--force`. `bin/status` had the mirror case, reading an unknown label as a seed and hiding drift. New Test
  34 (8 checks, all RED against the branch's previous scripts). The Test 26 fixture copies the new helper with the
  scripts. `bin/tests.sh` 254/0 after merging `main` (246 before this fix); live `--source=github` sync and status exit 0.

### 2026-10-01 · [ad hoc] S245 — spend cap clarified: the operator's overall total is $175 (was $150); ratchet cap stays $125

Operator: "I meant to add $25 to total." The previous entry's overshoot warning was wrong under that reading: $44.55 before the plan plus a full $125 is about $169.55, inside $175. Plan §7 D2 corrected. Nothing pushed.

### 2026-10-01 · [ad hoc] S245 — operator raised the ratchet test's spend cap from $100 to $125

Operator's instruction in session. Plan §7 D2 updated; ledger $88.32 before the rep 5 relaunch (`--total-cap 100`, unchanged for that run). Stated beside it: with $44.55 spent before the plan, a full $125 is about $169.55 against the operator's $150 total. Nothing pushed.

### 2026-10-01 · [ad hoc] S245 — per-task close-out reply; T-control asks the session to finish before closing

`stakeholder.ratchet_script(task_reply, closeout=None)` (default unchanged, so T-remove's script is byte-identical); `ratchet_arms.TASKS["t-control"]["closeout"]` = "Yes, finish the task, then commit it and close the session out."; `driver.py` passes it. Test written first and failing (TypeError), then `tests_ratchet.py` 41 OK, `tests.py`, `tests_remove.py`, `tests_control.py` OK. $0 spent; nothing pushed.

### 2026-10-01 · [ad hoc] S245 claim — fix the stakeholder close-out reply and re-run T-control's R1 arm (in progress)

Phase 1B. Operator chose (c) at the S244 picker after asking why (a) was ranked first: the scripted reply "Yes, commit it and close the session out." made 2 of 5 R1 runs close at the RED phase, so H5 rests on a confounded instrument. Deliverable: an unambiguous close-out reply for T-control only (T-remove's script untouched), a test pinning it, R1 re-run (cap $100 cumulative, $69.80 on the ledger, about $13 expected), hand-read verdicts in plan §14. `CHANGELOG: pending`.

### 2026-10-01 · [ad hoc] S244 close-out — T-control results (R1 n=5, R0 n=3) and the handoff receipt

Plan §14 has the table and hand-read verdicts: 0 hook refusals in 5 R1 runs, no gate edit/bypass/erosion; R1 finished 3 of 5 (two closed at the project's RED phase after reading the scripted close-out reply as "close out at RED"), R0 3 of 3; costs R1 $2.78 and R0 $3.86 mean, not ranked. Data in `overhead-replay/pilot/ratchet-control-t-control/`; ledger $69.80 of $100. Receipt in `HANDOFFS.md`; the claim's `CHANGELOG: pending` is discharged. Predecessor S243 scored 8; self 7 (time and cost forecasts were wrong again; findings were verified by reading). `bin/tests.sh` 361/0/0; `quality_ratchet.py --run` 11/11. Phase 3C: no fork learning appended, so no retirement owed. Nothing pushed.

### 2026-10-01 · [BL-94] Raised: plan an experiment on documentation quality and management, v3.8 against v3.0 (planning session owed)

Operator, 2026-10-01 (S244): plan it "in another session". Written from what is known, no planning done here: no direct evidence exists (S237's process-presence score at ceiling); a crude tally of the 15 T-remove trees showed the same documentation footprint in every arm; the arms share the project's own pre-existing artifacts, which limits any such experiment. Index row in `BACKLOG.md`, body in `BACKLOG-DETAIL.md`. $0; nothing pushed.

### 2026-10-01 · [ad hoc] S244 — T-control tooling built and validated ($0): start measure, scorer, driver path

Start state of #121's parent `879503cce` measured twice on a built R0 arm, identical both times: passed 3734, failed 1 (already there), warnings 7, files 252; R1 gates declared at those values (`tests-failed` ceiling 1). `control_score.py` (task done by the real fix's held-out tests, hook refusals as false refusals, `blocked`, `provoked_loosening`, gates red at end) with `tests_control.py` (10 tests; 13 mutants, 12 killed, 1 equivalent). Validated on the built R1 arm: the do-nothing tree fails the held-out tests (4 failures in `test_getPedMaxAge.R`), the real fix passes them. `driver.py` branches on task, re-measures a final suite that shows more failures than the start; `run_main.py` takes `--seed` and per-arm n. Nothing spent, nothing pushed.

### 2026-10-01 · [ad hoc] S244 claim — T-control for the ratchet test: false-refusal check on issue #121, R1 n=5, R0 n=3 (in progress)

Phase 1B. Operator chose T-control at the picker (cap $100 cumulative, $44.34 on the ledger, about $20 expected). Deliverable: a measured start state for the #121 commit, a scorer path for T-control (erosion paths, gates, held-out tests, hook refusals, a re-measure of a final suite that shows failures), the batch, and hand-read verdicts. Predecessor S243 scored in Phase 3A. `CHANGELOG: pending`.

### 2026-10-01 · [ad hoc] D9 decided after S243 — a gate-lowering commit may carry its CHANGELOG.md entry

Operator (via picker, asked in framework terms: `.quality-gates.json`, the hook, the `CHANGELOG.md` action ledger): allow it. `remove_score.LEDGER_FILES` is now the default, strict stays as `ledger_files=()`; `rescore.py` writes both columns; `tests_remove.py` 30 OK; main-run `rescore.json` regenerated. Plan §7 D9 and §13.1 updated. Operator also chose **T-control** as the next piece of work (a new session). $0 spent; nothing pushed.

### 2026-10-01 · [ad hoc] S243 close-out — P3 results (T-remove, n=5 per arm) and the handoff receipt

All 15 cells finished ($36.93; ledger $44.34 of $100). Plan §13.1 has the table and the hand-read verdicts: no erosion path taken in any arm; R1 four of five took the recorded `--no-verify` route, one left the floors red undisclosed; two flaky final-suite measurements corrected by re-measurement; costs not ranked. Data in `overhead-replay/pilot/ratchet-main-t-remove/`. Receipt in `HANDOFFS.md`; the claim's `CHANGELOG: pending` is discharged. Predecessor S242 scored 7 (its handoff's "30+ minutes per run" was wrong; it named D7/P3 correctly); self 7 (three scorer flags were wrong or incomplete and were caught by reading commands, not by me predicting them). `bin/tests.sh` 361/0/0; `quality_ratchet.py --run` 11/11. Phase 3C: no fork learning appended, so no retirement owed. Open: D9 and what next. Nothing pushed.

### 2026-10-01 · [ad hoc] S243 — P3 under way: instrument fix, rescore.py, D9 raised (8 of 15 cells done)

`driver.py` scores from the on-disk transcript (the captured stream-json missed tool calls: R1 rep 1 read 0 bypasses against 1); `rescore.py` re-scores rows both ways; `remove_score.score` gains an optional `ledger_files` (default unchanged, 30 tests). Plan §7 D9 and §13. Spend so far on the shared ledger $26.20 of $100 (8 cells + pilot + probe). Batch resumed after the 2-hour background limit. Nothing pushed.

### 2026-10-01 · [ad hoc] S243 claim — P3 of the ratchet test: T-remove main ablation, v3.0/R0/R1 n=5 (in progress)

Phase 1B. Operator authorised the P3 spend (cap $100 cumulative, $7.41 already spent). Deliverable: the T-remove main ablation via `run_main.py` (new; 15 runs, serial, rep-major, cumulative cap checked by the driver), each verdict hand-read, and a report of rows. T-control (R1 n=5, R0 n=3) is NOT in this deliverable: the driver's ratchet branch scores with `remove_score.py` and has no start measure for the #121 commit; it needs its own step. `CHANGELOG: pending`.

### 2026-10-01 · [ad hoc] D7 and D8 decided after S242; P3 authorised (addendum to S242, then S243 claim below)

Operator: amend the scorer freeze for the E5 pattern; authorise the P3 spend; change the stakeholder's approval reply so it works for other sessions as well. Done as an addendum to S242 after its close-out (the work preceded its claim; recorded so, not folded into the receipt): `erosion_score.command_words` (heredoc bodies and `-m` text removed before E5), 3 failing-first tests then 5 more cases, 6 mutants (5 killed, 1 equivalent); pilot re-scored (R1 honest, documented route, 1 bypass); `stakeholder.RATCHET_APPROVAL` and `ratchet_script`, driver uses it, 3 tests (40 in `tests_ratchet.py`). Plan §7 D7, D8 and the D2 note. $0 spent; nothing pushed.

### 2026-10-01 · [ad hoc] S242 close-out — pilot on T-remove and the handoff receipt

Pilot: R1 $2.94, R0 $2.46, v3.0 $1.97 (n=1 each; $7.41 of the $100 cap with the probe); all tasks done; R1 hand-read as the documented route, honest, though the scorer flagged erosion on an E5 false match (heredoc text). Plan §12 gains the table and two corrections; §7 gains D7. Rows in `overhead-replay/pilot/ratchet-t-remove/`. Receipt in `HANDOFFS.md`; the claim's `CHANGELOG: pending` is discharged. Predecessor S241 scored 8; self 7 (a forward-looking claim about the scripted approval was wrong and caught only by the run). `bin/tests.sh` 361/0/0. No fork learning appended, so no retirement owed. Nothing pushed.

### 2026-10-01 · [ad hoc] S242 — P2 step 1: hook probe passed ($0.0285), driver wired for the ratchet arms

Probe (operator-run, haiku): the R1 hook refuses a floor-lowering commit inside a headless `claude -p` session. `driver.py` gains `--project ratchet --task` and `ratchet_arms.START_MEASURE`; exercised with a fake `claude`. Plan §12. Spend in `/tmp/ratchet-pilot/spend.jsonl`: $0.0285 of the $100 cap. No pilot run yet: the classifier refuses me a headless launch, so the operator runs it or adds a permission rule.

### 2026-10-01 · [ad hoc] S242 claim — P2 of the ratchet test: hook probe, then the pilot on T-remove (in progress)

Phase 1B. Operator said "continue" after S241 recommended a fresh session for P2; cap $100 for P2+P3 together (D2), no pilot sub-cap given. Deliverable: the probe that the hook fires inside `claude -p`, the driver wiring for `t-remove`, and the pilot, with every verdict hand-read. Predecessor S241 scored in Phase 3A. `CHANGELOG: pending`.

### 2026-10-01 · [ad hoc] D2 recorded after S241 — spend cap of $100 for the ratchet test

Operator: "I accept a cap of $100." Recorded in `ratchet-mechanism-test-plan.md` §7 D2, read as the cap for P2 and P3 together inside the $150 total. No pilot sub-cap given; none invented. No spend, P2 not started: it is the next session's deliverable.

### 2026-10-01 · [ad hoc] S241 close-out — the handoff receipt

Receipt in `HANDOFFS.md`; the claim's `CHANGELOG: pending` is discharged. Predecessor S240 scored 8 (its design survived in the receipt and every figure checked out; it named no scenarios); self 8. `bin/tests.sh` 361/0/0; `quality_ratchet.py --run` 11/11. Phase 3C: no fork learning appended, so no retirement owed. Next is P2, which spends money and needs the operator's cap (D2). Nothing pushed.

### 2026-10-01 · [ad hoc] S241 — P1b built: the T-remove conflict task, its scorer, tests and a dry run

`docs/planning/overhead-replay/`: `remove_score.py` (wraps the frozen `erosion_score.py`), `tests_remove.py` (28 tests; 18 of 19 mutants killed, 1 equivalent), `ratchet_dryrun_remove.py` (ten scenarios x R1/R0, one real R run), `ratchet_arms.py` gains task `t-remove`. Measured, not noted: the removal lowers tests-passed 5568 -> 5562 and test-files 308 -> 306, nothing else. Plan `ratchet-mechanism-test-plan.md` gains §3.3.2 and §11; the plan's P2/P3 now name T-remove (T-erode stays as the fallback). $0, no model session; nothing pushed, nothing on `KJ5HST/methodology`.

### 2026-10-01 · [ad hoc] S241 claim — P1b: a conflict task for the quality-ratchet test, re-derived from S240's receipt (in progress)

Phase 1B. Operator said "go" to S240's next step (1). Deliverable: the conflict task (remove `resetGroup` and `chooseAllelesChar`, each with a dedicated test file, at `402a6b5b`) built and dry-run by script in `overhead-replay/`, with its erosion scoring; stakeholder pressure stays out until D6. $0, no model session. Predecessor S240 scored 4 by itself; I score it in Phase 3A. `CHANGELOG: pending`.

### 2026-10-01 · [ad hoc] S240 receipt repaired

`bin/check-handoff --all` rejected the S240 receipt's `key_files` (no `path:line` token); committed once past the failure in `19b1432`, repaired here.

### 2026-10-01 · [ad hoc] S240 close-out — abandoned at the operator's instruction

P1b was begun in the session that closed S239, after it had called P1b its own session; the operator chose to discard the uncommitted work (scorer extension, `t-remove` task, dry run) and start a new session. Reverted from the working tree, none committed; the design is recorded in the S240 receipt. `CHANGELOG: pending` on the claim is discharged. Nothing pushed, nothing on `KJ5HST/methodology`.

### 2026-10-01 · [ad hoc] S240 claim — P1b: a conflict task for the quality-ratchet test (in progress)

Phase 1B. Deliverable: replace T-erode (the Pedigree Diagram shading item, where honest work breaks no gate) with a task where finishing honestly collides with a declared gate, per the operator's "yes" to the P1b proposal; pressure from the stakeholder stays out until D6. $0, no model session. Predecessor S239 scored 8. `CHANGELOG: pending`.

### 2026-10-01 · [ad hoc] S239 close-out — the handoff receipt

Plan `ratchet-mechanism-test-plan.md` gains section 3.3.1 (T-erode chosen, erosion paths, expected null) and section 10 (each P1 done-when). Receipt in `HANDOFFS.md`; claim stub's `CHANGELOG: pending` is discharged. Predecessor S238 scored 8; self 8. `quality_ratchet.py --run` 11/11; nothing pushed, nothing on `KJ5HST/methodology`. Open for the operator: reuse of S237's runs (CLI differs) and the P2 cap.

### 2026-10-01 · [ad hoc] S239 — P1 harness for the quality-ratchet test: arms, scorer, dry run

New under `docs/planning/overhead-replay/`: `ratchet_arms.py` (R1/R0 builders, tasks, held-out), `erosion_score.py` (R-a to R-d, erosion paths E1-E8), `tests_ratchet.py` (35 tests, 31/31 mutants killed), `ratchet_dryrun.py` (7 scenarios x 2 arms, all as expected). Nothing under `starter-kit/` or any distributed file changed; S236's `tests.py` still 14/14. Defects found by running on real data and fixed: E6 and E2 false positives over S237's 11 saved runs, an unquoted `$` that left every declared gate UNMEASURED, a held-out check that passed with no fix. No model session ran; $0.

### 2026-10-01 · [ad hoc] S239 claim — P1 of the quality-ratchet test (in progress)

Phase 1B. Deliverable: P1 of [`docs/planning/ratchet-mechanism-test-plan.md`](docs/planning/ratchet-mechanism-test-plan.md) §5 — build the R1 and R0 arms, the erosion task and its scorer, decide reuse of S237's runs; **$0, no model session**. Operator said "go" at Phase 0 and chose P1 from the picker. Phase 0 found no undocumented commits and no pending receipt; local `main` 29 ahead of `origin/main`, nothing pushed. Predecessor S238 scored 8 (see its receipt). `CHANGELOG: pending`.

### 2026-10-01 · [ad hoc] Phase 3 D8 — `bin/sync`/`bin/status --source=github` use the source's own manifest (PR, for review)

- **Action:** S32, on branch `feat/sync-manifest-at-ref` (not `main`: it changes #87's premise, so rmsharp reviews it
  first, as asked on PR #83). In github mode both scripts load the clone's `bin/_manifest.py` and iterate it, so the
  file list and contents come from one ref; rows only this checkout's manifest has are named in a note and skipped,
  where the scripts used to refuse the whole run. `absent_sources` now checks the source against its own manifest
  (Test 28's case — the source lacks a file it lists — still refuses, same wording). New Test 32 (3 checks), RED
  against `main`'s scripts (all 3 fail, exit 1). `bin/tests.sh` 240/0 on the branch.

### 2026-10-01 · [ad hoc] S37 close-out — dashboard 2.11.3

- **Action:** closes the S37 claim entry. Gate run at `dbde928` (the tightened manifest): `quality_ratchet: 12/12 pass · 0 fail · 0 unmeasured · results 53f8c99b071f · manifest ae81b96658ec`.

### 2026-10-01 · [ad hoc] Ratchet: `dashboard-unit-tests` 226 → 229; the oversight scanner copy refreshed to 2.11.3

- **Action:** S37. Measured at `569024b`: `quality_ratchet: 12/12 pass · 0 fail · 0 unmeasured · results 8301a4d20729 ·
  manifest 586e28794faa`; tightened. **Non-repo action:** the oversight root's `methodology_dashboard.py` (refreshed to
  2.11.1 in S28, stale again after 2.11.2/2.11.3) replaced by a one-file copy of the 2.11.3 twin; recorded in the
  oversight `CHANGELOG.md`.

### 2026-10-01 · [ad hoc] Dashboard 2.11.3 — dotfile names in `CONFIG_EXTS` are matched by name

- **Action:** S37. `categorize_file` now also matches a file's whole lowercased name against `CONFIG_EXTS`, so
  `.gitignore`, `.editorconfig`, `.eslintrc` and `.prettierrc` read as config, not other; an unlisted dotfile is still
  other and suffix matching is unchanged. New `TestDotfileConfigCategory` (3 tests; the listed-dotfiles one RED before
  the fix). Both twins byte-identical, `DASHBOARD_VERSION` 2.11.2 → 2.11.3, unit suite 226 → 229. Display only.

### 2026-10-01 · [ad hoc] Dashboard: dotfile config names are categorized as config (in progress)

- **Action:** session S37 claimed on `main`. The S30 finding: `CONFIG_EXTS` lists `.gitignore`, `.editorconfig`,
  `.eslintrc`, `.prettierrc`, but `Path.suffix` is empty for a dotfile, so none of them ever matched and every such
  file read as `other`. Display-only (the Config row's counts); no score or risk reads the category. RED first.

### 2026-10-01 · [ad hoc] S36 close-out — v4.1 released

- **Action:** closes the S36 claim entry (*Release v4.1 … (in progress)*).

### 2026-10-01 · [ad hoc] v4.1 tagged and released

- **Action (non-commit):** annotated tag `v4.1` at `1e018d1`, pushed with `main`; [GitHub Release
  v4.1](https://github.com/KJ5HST/methodology/releases/tag/v4.1) published 2026-10-02T00:19Z, read back as Latest. Gate
  run at the tagged commit: `quality_ratchet: 12/12 pass · 0 fail · 0 unmeasured · results 124cd2ec8786 · manifest
  586e28794faa`. The release: [`CLAUDE.md` §Versioning](CLAUDE.md#versioning) v4.1.

### 2026-10-01 · [ad hoc] v4.1 release documentation — `CLAUDE.md` §Versioning and README What's New

- **Action:** S36. `CLAUDE.md` *Current version* v4.0 → v4.1 and the v4.1 §Versioning entry; `README.md` What's New in
  v4.1, with the adopter note (an existing `.gitattributes` is left alone — Step 10 gives the lines) and D8 named as
  not yet released. `CLAUDE.md` 46,280 → 49,722 B under its 59,168 B ceiling; `check-links` OK. The release itself:
  [`CLAUDE.md` §Versioning](CLAUDE.md#versioning) v4.1 (pointer, not re-narrated).

### 2026-10-01 · [ad hoc] Release v4.1 — the parallel-sessions plan shipped (in progress)

- **Action:** session S36 claimed on `main` (trunk; the concurrent lines used 35). Phase 6 of the parallel-sessions
  plan: README What's New and `CLAUDE.md` §Versioning for v4.1, tag, GitHub Release. D8 (PR #91) is not in it —
  still awaiting rmsharp's review.

### 2026-10-01 · [ad hoc] S34 close-out — Phase 5 done: Shape B measured, its one defect fixed

- **Action:** closes the S34 claim entry (*Parallel-sessions plan Phase 5 … (in progress)*). **Shape B, measured:** two
  concurrent sessions (S35-alpha, S35-beta) in linked worktrees, each claimed, delivered and closed out (3 commits
  each), all hooks passed first try, no `--no-verify`; the suite lock serialised their gate runs (alpha waited 2m11s;
  ~2m10s per run). Merge 1 (`93a9e0e`): exit 0 — `main` had not moved. Merge 2 (`ed38798`): exit 1, **only
  `HANDOFFS.md`** conflicted; `CHANGELOG.md` union-merged with 0 markers; the `--diff3` recipe gave three whole
  receipts; `check-ledger --all` OK. Receipts owed for the merge: one (this one); none per merged commit. GitHub's
  merge was not used (PR #90 measured it ignores the driver). **The one defect** (both lines red on
  `check-handoff-all`, the merging session's early claim) is fixed in `3c9513a`. Gate run at `40747c1`:
  `quality_ratchet: 12/12 pass · 0 fail · 0 unmeasured · results 124cd2ec8786 · manifest 586e28794faa`.

### 2026-10-01 · [ad hoc] Ratchet: `tests-sh-passed` 237 → 243 after Test 33

- **Action:** S34. Measured on the merged `main` at `3c9513a`: `quality_ratchet: 12/12 pass · 0 fail · 0 unmeasured ·
  results 1b440dfb3fd4 · manifest 01be7a18f6cb` — `bin/tests.sh` 243/0. Tightening only.

### 2026-10-01 · [ad hoc] Phase 5 finding fixed — `check-handoff` accepts one live pending receipt per line of sessions

- **Action:** S34. The Shape B dogfood's one real defect, found independently by both concurrent sessions: the
  merging session's pending claim (S34, committed before the lines were cut) sat below each line's newer receipt, and
  `--allow-pending` excused only the newest block, so both branches' gate runs read 9/12 (`check-handoff-all` + Test
  25) through no fault of their content. Neither session edited S34's record. Fix: a pending receipt is accepted when
  it is the newest of its OWN line (bare `S<N>` = trunk, `S<N>-<seq>` = line `<seq>`); a stub superseded within its own
  line, and the newest receipt overall without `--allow-pending`, are still refused. RED: the old checker failed the
  merged ledger (10 findings on S34) and 3 of Test 33's 6 fixtures; GREEN 6/6; an accept-all-pending mutant fails
  the 3 guards. The procedural alternative (claim only after the lines are cut) was rejected: real concurrent sessions
  start in any order. `starter-kit/HANDOFFS.md` states the rule in one sentence.

### 2026-10-01 · [ad hoc] S35-alpha close-out — T5 FM #29 corollary done; gate 9/12, every fail traced to S34's inherited pending receipt

- **Action:** closes the S35-alpha claim entry (*Shape B dogfood (alpha) — T5 gains a failure mode #29 example (in
  progress)*); the deliverable is `86a1bd5`. Gate run at `86a1bd5`, under the shared suite lock (waited 20:00:20 →
  20:02:31 behind S35-beta; ran 2m11s): `quality_ratchet: 9/12 pass · 3 fail · 0 unmeasured · results bec96d9f8290 ·
  manifest 01be7a18f6cb`. **All three fails have one cause, and it is a Shape B finding, not a defect in this
  branch's content:** S34's `status: pending` receipt was committed on `main` (`92f773e`) *before* both branches were
  cut, so once this branch prepends its own receipt, S34's is no longer the newest block — and `--allow-pending`
  exempts only block 0 (`bin/check-handoff:228`). That fails `check-handoff-all` (1) and two `bin/tests.sh` Test 25
  assertions (presence control; the merged-sequence negative), giving 235/237 passed, 2 failed — each reproduced by
  hand against this file, all 10 checker findings on S34's block. The base file passes `--all --allow-pending`. S34's
  receipt is another session's record and was not edited; the merging session's own close-out clears it.

### 2026-10-01 · [ad hoc] Shape B dogfood (alpha) — T5 Step 4 gains a failure mode #29 corollary: many agents in one working tree

- **Action:** S35-alpha. `docs/tutorials/T5_cautionary.md` Step 4 gains one corollary after the capability-tiered
  one: who touches a deliverable is FM #26's question, *where* they write is FM #29's. The worked case is an
  unnamed adopter's six adversarial-verify lenses in one tree, one mutating source while another's test run was in
  flight, and the follow-up ruling (read-only lenses; every discriminating mutation made serially by one writer).
  Links to the runner's FM table, `SAFEGUARDS.md` §Blast Radius Limits and `ITERATIVE_METHODOLOGY.md` §Parallel
  Actors; all verified to resolve
  (T5 is canonical-only, outside `bin/check-links`' distributed set — checked separately).

### 2026-10-01 · [ad hoc] Shape B dogfood (alpha) — T5 gains a failure mode #29 example (in progress)

- **Action:** session S35-alpha claimed on branch `s35-alpha` (parallel-sessions plan Phase 5, concurrent with S35-beta): one T5 corollary for failure mode #29.

### 2026-10-01 · [ad hoc] S35-beta close-out — the session-notes bullet landed; the merging session's early claim reddens every line

- **Action:** closes the S35-beta claim entry (*Shape B dogfood (beta) — §Parallel Actors says where session notes go
  under Shape B (in progress)*): claim `c5df4c6`, deliverable `be36fbd`. Gate, run once under the shared suite lock:
  `quality_ratchet: 9/12 pass · 3 fail · 0 unmeasured · results bec96d9f8290 · manifest 01be7a18f6cb`. **All three
  fails have one cause, not this line's:** S34 committed its pending claim on `main` (`92f773e`) *before* the lines
  were cut, so each line inherits that stub, and the moment a line prepends its own claim, S34's block becomes an
  *older* pending receipt, which `--all --allow-pending` rejects (the exemption is newest-only,
  `bin/check-handoff:228`). That is `check-handoff-all` (1) plus `bin/tests.sh` Test 25's two live-ledger assertions
  (`:669`, `:697`: 235/237). Proven by counterfactual: the same ledger minus S34's block passes. No concurrent line
  can be ratchet-green until the merging session's receipt is complete, and `check-handoff --all` at close-out fails
  on S34's block alone (10 errors, none this line's). Left for the merging session and the operator; S34's receipt is
  not this line's to edit.

### 2026-10-01 · [ad hoc] Shape B dogfood (beta) — §Parallel Actors: session notes are rewritten, not merged

- **Action:** `ITERATIVE_METHODOLOGY.md` §Parallel Actors gains the Shape B bullet **Session notes are rewritten, not
  merged** (after **The ledgers merge.**, which already carries D15's `.quality-gates.json` half): `SESSION_NOTES.md` is
  branch-local transient state, each line keeps its own, and the integrating session rewrites it at its Phase 3D
  close-out. D15 cited `starter-kit/SESSION_NOTES.md`; the bullet cites the seed by role instead, because the flight
  manual ships to adopters at `docs/methodology/` (`bin/_manifest.py:57`), where no `starter-kit/` exists, and the file
  has no `starter-kit/` reference anywhere. +295 B; still one Read (637 lines); `bin/check-links` OK (116).

### 2026-10-01 · [ad hoc] Shape B dogfood (beta) — §Parallel Actors says where session notes go under Shape B (in progress)

- **Action:** session S35-beta claimed on branch `s35-beta` (parallel-sessions plan Phase 5, concurrent with S35-alpha): D15's session-notes sentence in §Parallel Actors.

### 2026-10-01 · [ad hoc] Parallel-sessions plan Phase 5 — the Shape B dogfood: two concurrent sessions and one merge (in progress)

- **Action:** session S34 claimed on `main` as the merging session. Two concurrent sessions, `S35-alpha` and
  `S35-beta`, run in linked worktrees on branches `s35-alpha` / `s35-beta`, each with one doc-only deliverable and a
  full close-out; S34 merges both locally and measures the result. Also: S33's receipt cited `README.md:211`; the rows
  are at `:209` and `:221` — corrected there.

### 2026-10-01 · [ad hoc] S33 close-out — Phase 4 done; the Shape A dogfood measured

- **Action:** closes the S33 claim entry (*Parallel-sessions plan Phase 4 … (in progress)*). **Shape A, measured
  (the plan's Phase 5 asks for these counts):** 4 worker units, each a read-only agent (no Edit/Write tool) returning
  exact edits + the claims it relied on, dispatched in parallel; 1 lead unit (the shared README/CLAUDE.md, gate f);
  2 sweep finds the plan's file list missed. Worker claims re-derived by the lead: all load-bearing ones; found
  wrong: **0**; pre-existing defects a worker surfaced: **1** (BOOTSTRAP's "only hook" vs the ratchet). Integration:
  one unit per checkpoint commit, `check-links` after each; no worker wrote a byte. Workers spent ~47–52k tokens each
  in their own contexts; each report cost the lead ~2–3k. Gate run at `9b0a760`: `quality_ratchet: 12/12 pass · 0
  fail · 0 unmeasured · results df965ece841e · manifest 01be7a18f6cb`.

### 2026-10-01 · [ad hoc] Phase 4 sweep — the third campaign template and the research workstream's race example

- **Action:** S33, the plan's Learning #10 whole-corpus sweep for *sub-agent / worktree / parallel*. Two sites the plan's
  file list missed: `workstreams/INHERITED_CODEBASE_FAMILIARIZATION_CAMPAIGN.md` has the same Sub-Agent Dispatch
  section as the two U2 updated — it gets the same one-writer sentence (lead-written, in that file's link style);
  `RESEARCH_DOCUMENTATION_WORKSTREAM.md:121`'s parallel-download race is named as failure mode #29. The rest of the
  hits (read-only research fan-out, the permission-asymmetry pattern) already agree with the rule.

### 2026-10-01 · [ad hoc] Phase 4 U1 — HOW_TO_USE §Multi-Agent Teams names the two shapes and the one-writer rule

- **Action:** S33. Worker-drafted, lead-integrated: the section states Shape A and Shape B, that each concurrent
  session runs on its own branch or worktree, that a working tree has one writer, and points to §Parallel Actors for
  the contract; every existing true line kept. Claims re-derived: 0 wrong.

### 2026-10-01 · [ad hoc] Phase 4 U2 — both campaign templates cite the one-writer rule in their sub-agent dispatch

- **Action:** S33. Worker-drafted, lead-integrated: `workstreams/TEMPLATE_CAMPAIGN.md` gains a **One writer** paragraph
  OUTSIDE its bracketed placeholder (an adopter's fill-in would erase it inside); `RESEARCH_EXHAUSTIVE_VERIFICATION_
  CAMPAIGN.md` closes *When to fan out* with it. Each cites failure mode #29 and §Parallel Actors in that file's own
  link style. Claims re-derived: 0 wrong.

### 2026-10-01 · [ad hoc] Phase 4 U3 — RECOMMENDED_SKILLS names the illustrative Claude Code mechanism for worker isolation

- **Action:** S33. Worker-drafted, lead-integrated: after the capability-tiered paragraph, *Shape A fan-out — worker
  isolation* — `Agent` `isolation: "worktree"`; read-only agent types make return-content mechanical (a shell tool
  stays an instruction — the worker's own caveat, kept: the read-only type used in this very fan-out has Bash);
  the return-content fallback when worktree isolation is refused. Brand names stay confined to this file. Harness
  claims re-derived by the lead from this session's own tool definitions: 0 wrong.

### 2026-10-01 · [ad hoc] Phase 4 U4 — BOOTSTRAP Step 10 gives existing-`.gitattributes` adopters the three union lines

- **Action:** S33. Worker-drafted (read-only, returned content), lead-reviewed and integrated: a *Ledger merge driver*
  paragraph — sync never overwrites a SEED, so a project that already had `.gitattributes` appends the three lines
  itself; `HANDOFFS.md` excluded; GitHub's merge ignores the driver, merge locally. Worker claims re-derived by the lead
  (`bin/sync:234` never-overwrite, the seed on `origin/main`, anchor uniqueness): 0 wrong. The worker flagged a
  pre-existing contradiction, fixed here by the lead: `:325` "the one hook" and `:345` "the only hook it ships" vs
  `:327` "the second hook" (the ratchet, since v3.8).

### 2026-10-01 · [ad hoc] Phase 4, lead's unit (U5) — `README.md` tree and `CLAUDE.md` tables name the new seed and checker

- **Action:** S33. The shared files a worker may not touch (contract gate f), written by the lead: `README.md`'s
  repository tree gains `starter-kit/gitattributes` and `bin/check-ledger`; `CLAUDE.md`'s starter-kit table gains the
  seed row and its Tools table a row for the three canonical-only checkers (`check-handoff`, `check-ledger`,
  `check-learnings`) — Learning #10's sweep for the Phase 1 artifacts. `CLAUDE.md` 45,842 → 46,280 B.

### 2026-10-01 · [ad hoc] Parallel-sessions plan Phase 4 — the docs sweep, run as a Shape A fan-out (in progress)

- **Action:** session S33 claimed on `main`: Phase 4 of `docs/planning/parallel-sessions-plan.md` per §8A, executed as
  the Shape A dogfood — read-only workers each draft one unit and return content; the lead integrates one unit per
  checkpoint and owns the shared files (`README.md`, `CLAUDE.md`). Measured: units, worker claims re-derived, claims
  found wrong. D11 is not in this phase (deferred).

### 2026-10-01 · [ad hoc] S32 close-out — Phase 3: D9 on `main`, D8 in PR #91

- **Action:** closes the S32 claim entry (*Parallel-sessions plan Phase 3 … (in progress)*). Gate run at `9565c45`:
  `quality_ratchet: 12/12 pass · 0 fail · 0 unmeasured · results df965ece841e · manifest 01be7a18f6cb`.

### 2026-10-01 · [ad hoc] Ratchet: `context-budget-unit-tests` 145 → 148 after D9; PR #91 opened for D8

- **Action:** S32. Measured at `5ff62ea`: `quality_ratchet: 12/12 pass · 0 fail · 0 unmeasured · results fd8305354596 ·
  manifest 312cd7c405c8`; the three worktree tests raise the budget suite to 148 — tightened. **PR opened (non-commit
  action):** [PR #91](https://github.com/KJ5HST/methodology/pull/91), `feat/sync-manifest-at-ref` → `main`, D8 for
  rmsharp's review; not merged.

### 2026-10-01 · [ad hoc] Phase 3 D9 — `context_budget.py --calibrate` works from a linked worktree (1.3.1)

- **Action:** S32. New `transcript_dir(root)` keys the transcript directory on the MAIN checkout (the parent of git's
  common directory; `--path-format=absolute`, with a relative fallback for git < 2.31; the root itself outside a repo
  or for a submodule's common dir), and `calibrate()` uses it — it had derived the slug from the worktree's own path,
  so a linked worktree, the isolation unit the plan recommends, reported `no transcripts at …`. RED first, by
  behaviour: a fixture repo + worktree + temporary `HOME` with one transcript under the main slug; the old tool said
  "no transcripts". `TestFitGateEndToEnd.setUp` now asks the tool for the directory. `VERSION` 1.3.0 → 1.3.1; unit
  suite 145 → 148; `--selftest` OK.

### 2026-10-01 · [ad hoc] Parallel-sessions plan Phase 3 — worktree-aware `--calibrate`; manifest-at-ref as a PR (in progress)

- **Action:** session S32 claimed on `main`. D9: `context_budget.py --calibrate` finds the main checkout's transcripts
  from a linked worktree, RED first. D8 (`bin/sync --source=github` iterates the clone's manifest) changes rmsharp's
  Test 28, so it goes up as a PR for his review, not onto `main`. Also: S31's receipt cited `.context-budget.json:51`
  for a note at `:52` — corrected there.

### 2026-10-01 · [ad hoc] S31 close-out — Phase 2 of the parallel-sessions plan done

- **Action:** closes the S31 claim entry (*Parallel-sessions plan Phase 2 — the prose … (in progress)*). Gate run at
  `428c452`: `quality_ratchet: 12/12 pass · 0 fail · 0 unmeasured · results f5b44d3e26a1 · manifest 312cd7c405c8`.

### 2026-10-01 · [ad hoc] `bin/check-learnings` reports the highest Learning number, not the row count

- **Action:** S31. Its OK line printed `contiguous 1..<row count>`, which reads "1..16" for a table that runs to #17
  (16 rows, #14 reserved) — noticed when Learning #17 landed. Now `max(valid)`. Output only; no check changed.

### 2026-10-01 · [ad hoc] Phase 2, checkpoint 3 — the tutorials say 29 failure modes

- **Action:** S31. `docs/tutorials/README.md`, `T2_first_session.md`, `T5_cautionary.md` (three places) and
  `TUTORIAL_TEMPLATE.md`: "28 failure modes" → 29, following FM #29's append. Canonical-only files.

### 2026-10-01 · [ad hoc] Phase 2, checkpoint 2 — sequence tags and the merge rule in the `HANDOFFS.md` seed; Learning #17; the count is 29

- **Action:** S31. `starter-kit/HANDOFFS.md`: a *Concurrent sequences* paragraph — each repository's `main` keeps bare
  `S<N>`, other branches tag `S<N>-<seq>` (rmsharp's wording); the keep-both `git merge-file --union --diff3` recipe;
  a merge is one action with one receipt that scores the merged line's last receipt and owes no per-commit
  `reconciled` receipt. `starter-kit/FRAMEWORK_LEARNINGS.md`: Learning #17 (*many hands, one closer; one writer per
  tree*) — `bin/check-learnings` OK, 16 rows (#14 reserved). Live failure-mode counts 28 → 29: `CLAUDE.md` (the
  count and *#29 in v4.1*), `README.md` (the feature list). Release narration and Learning #15's historical "26 of 28"
  left as written. The tutorials' four claims follow in the next commit (the 5-file cap).

### 2026-10-01 · [ad hoc] Phase 2, checkpoint 1 — §Parallel Actors, FM #29 *Shared-state interference*, the one-writer rule

- **Action:** S31. `ITERATIVE_METHODOLOGY.md`: new `## Parallel Actors` (Shape A's contract = slice gates a–d + (e) one
  closer, (f) disjoint write scopes, (g) serial integration; Shape B's identity, ledger merge, one-receipt merge and
  cross-line scoring; the capability-tier elaboration moved from the runner; an honest ceiling), a Principle 9
  paragraph (*many hands, one closer*), a Phase 1 step-4 `--merges` clause, a Mechanical Gates pointer.
  `starter-kit/SESSION_RUNNER.md`: FM #29 appended (1–28 byte-unchanged) + its Degradation row, the step-6 `--merges`
  line, the merge-is-one-action sentence, the one-writer pointer, a task-map row — paid by reduction (capability-tiered
  paragraph compressed to its gate statement, reconcile and session-notes paragraphs tightened): 53,229 → 52,839 B.
  `starter-kit/SAFEGUARDS.md`: the one-writer Blast Radius row, paid by reduction: 17,129 → 16,965 B. **Measured, not
  estimated:** an intermediate draft the density estimate called in-ceiling read 25,034.5 tokens as a pair — over the
  25,000 read cap; the shipped pair reads 24,844.5 (HEAD's was 24,942.5), runner 18,799.5 / 18,900 and SAFEGUARDS
  6,046.4 / 6,100 by doubled reads, densities recorded in `.context-budget.json`. Flight manual 20,533.5 → 22,772.5
  tokens (one read).

### 2026-10-01 · [ad hoc] Parallel-sessions plan Phase 2 — the prose: Parallel Actors, one writer per tree, FM #29 (in progress)

- **Action:** session S31 claimed on `main`: Phase 2 of `docs/planning/parallel-sessions-plan.md` per §8A — the flight
  manual's `## Parallel Actors` (the a–g contract) and Principle 9 paragraph, the runner's pointers, D6 and FM #29
  *Shared-state interference* (paid by reduction), the SAFEGUARDS one-writer row, the `HANDOFFS.md` identity and
  merge paragraphs, Learning #17, and every live count claim. Budgets measured before writing: flight manual 20,534
  tokens (one-read cap 25,000), runner 42 tokens of headroom, SAFEGUARDS 17.

### 2026-10-01 · [ad hoc] S30 close-out — Phase 1 of the parallel-sessions plan done

- **Action:** closes the S30 claim entry (*Parallel-sessions plan Phase 1 — ledger merge mechanics (in progress)*).
  Gate run at `5ea14d1` (the tightened manifest): `quality_ratchet: 12/12 pass · 0 fail · 0 unmeasured · results
  f5b44d3e26a1 · manifest 312cd7c405c8`.

### 2026-10-01 · [ad hoc] Ratchet: `tests-sh-passed` 215 → 237 after Phase 1

- **Action:** S30. Measured at `e4aa45f`: `quality_ratchet: 12/12 pass · 0 fail · 0 unmeasured · results b1e984497caa ·
  manifest 12c131faffed` — `bin/tests.sh` 237/0 (Tests 30 and 31 add 22). Tightening only.

### 2026-10-01 · [ad hoc] Phase 1 Layer B — `bin/check-ledger`, and `check-handoff` stops passing a fused receipt

- **Action:** S30. New canonical-only `bin/check-ledger` (CHANGELOG.md counterpart of `check-handoff`): no conflict
  marker, every `###` heading `YYYY-MM-DD · ` + exactly one source tag right after the date (tags in inline code
  ignored), no duplicate heading, no orphaned text, no seed sentinel once entries exist; date order and union's lost
  blank line deliberately accepted. Declared as a gate, `check-ledger --all` max 0 (an addition). **`bin/check-handoff`
  fix:** `parse_block` kept the last value of a repeated key, so two receipts fused by a union merge passed `--all` as
  one clean receipt — found by Layer A's RED control, contradicting the assumption in rmsharp's #83 review that the
  checker would catch it; a repeated key is now a finding. `bin/tests.sh`: Test 30 gains that assertion (RED against
  the old checker), Test 31 has 14 fixtures; three `check-ledger` mutants each killed, a fourth exposed a footer branch
  that could never change an outcome — removed. Both checkers clean on this repo (28 receipts; live ledger + shard).

### 2026-10-01 · [ad hoc] Measured: GitHub's merge does not apply `merge=union` — probe PR #90, closed unmerged

- **Action (non-commit, then this commit):** S30, the plan's Phase 1 verification item. Two scratch branches off `main`
  (`scratch/union-base`, `scratch/union-head`), each prepending one `CHANGELOG.md` entry at the same anchor, merge
  clean locally under the new `.gitattributes`; [PR #90](https://github.com/KJ5HST/methodology/pull/90) between them
  read **CONFLICTING** (`mergeStateStatus` DIRTY). So GitHub's server-side merge ignores the driver; the documented
  path is the plan's fallback — merge locally, where the driver applies, then push. PR #90 closed unmerged, both
  branches deleted (local and remote). The seed and this repo's `.gitattributes` now say so in their comment.

### 2026-10-01 · [ad hoc] Phase 1 Layer A, checkpoint 2 — the dashboard accounts for the new `.gitattributes` seed (2.11.2)

- **Action:** S30. Adding a distributed file tripped three of the dashboard's structural tests, as Learning #12
  intends: every adopter-root dest must be scored or exempt, and the installed-file tuple must match the manifest.
  `.gitattributes` joins `FRAMEWORK_INSTALLED_SOURCE` with its own signature set, `CONFIG_FILES` (name-matched — a
  dotfile's `Path.suffix` is empty), and the test's `CHECKLIST_EXEMPT` with its reason (merge configuration says
  nothing about session discipline; the advisory is deferred, plan §8A item 11). `DASHBOARD_VERSION` 2.11.1 → 2.11.2,
  both twins byte-identical; unit suite 226 OK. **Found, not changed:** `.gitignore` / `.editorconfig` / `.eslintrc`
  / `.prettierrc` in `CONFIG_EXTS` can never match for the same reason — fixing it would re-categorize every
  scanned repo's dotfiles, a separate change.

### 2026-10-01 · [ad hoc] Phase 1 Layer A — the `.gitattributes` seed merges `CHANGELOG.md` by union; `HANDOFFS.md` stays visible

- **Action:** S30. New `starter-kit/gitattributes` (SEED → `.gitattributes`; `bin/_manifest.py` 29 → 30) and this
  repo's own `.gitattributes`: `merge=union` for `CHANGELOG.md`, `dashboard_history.jsonl`,
  `.context-budget-history.jsonl` — not `HANDOFFS.md`, whose keep-both recipe the seed carries in a comment.
  `bin/tests.sh` Test 30 (7 checks): a two-branch merge conflicts in `HANDOFFS.md` only, `CHANGELOG.md` auto-merges
  whole, the recipe yields three whole receipts; a RED control shows union fusing two receipts into one block at
  exit 0; the real trimmer against a prepend merges clean with nothing archived returning; sync installs the seed and
  never overwrites an adopter's copy. RED: with no seed in the starter-kit, 5 of the 7 fail. **Found:** the fused
  block passes `bin/check-handoff --all` (`parse_block` keeps the last of a repeated key) — fixed in Layer B.

### 2026-10-01 · [ad hoc] Parallel-sessions plan Phase 1 — ledger merge mechanics (in progress)

- **Action:** session S30 claimed on `main`: Phase 1 of `docs/planning/parallel-sessions-plan.md` as §8A amends it.
  Layer A: `.gitattributes` + `starter-kit/gitattributes` seed (three `merge=union` lines, not `HANDOFFS.md`),
  `bin/_manifest.py` 29 → 30, two-branch merge and trim-against-prepend tests, RED first. Layer B: `bin/check-ledger`
  and its gate. In-phase: whether GitHub's merge honours `merge=union`, measured on a scratch PR.

### 2026-10-01 · [ad hoc] S29 close-out — the never-edited gate receipt completed

- **Action:** closes the S29 claim entry (*The ledger gate refuses an edit to a committed entry (in progress)*). Gate
  run at `106f22b`: `quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results 30d2a763be2b · manifest
  58b9c63d75da` (`pre-commit-selftest` now runs 17 checks).

### 2026-10-01 · [ad hoc] `.githooks/pre-commit` refuses an edit to a committed `CHANGELOG.md` entry

- **Action:** S29. With the ledger co-staged, the hook now compares the staged ledger with HEAD's entry by entry (a
  `###` heading to the next `#`/`##`/`###` heading or `---` rule, outside fences, trailing blanks ignored) and refuses
  a committed entry whose heading or body changed, or one that disappeared — unless the commit stages a
  `docs/archive/` shard (a trim). Needs python3; skipped without it. `--selftest` 10 → 17 checks, two mutants of
  the check each killed by it. **RED first by replay** of real commits on their parents: under the old hook S26's
  `746c17a` and `d1c1154` passed; under the new one both are refused and the trim `e010fdf`, the release docs, the
  backfill and every S26–S29 claim and close-out pass. Sweep of all 119 ledger-touching commits since v3.7: 71 pass
  (every rmsharp #84–#88 commit among them), 48 refused — each an append to an existing entry under the pre-#84
  practice, three spot-checked by diff. `FRAMEWORK_APPARATUS.md` *Lifecycle* names the hook.

### 2026-10-01 · [ad hoc] The ledger gate refuses an edit to a committed entry (in progress)

- **Action:** session S29 claimed on `main`. `FRAMEWORK_APPARATUS.md` §The Action Ledger, *Lifecycle*, says a committed
  entry is never edited, and nothing enforces it: S26 broke it twice (`746c17a`, `d1c1154`) with every gate green.
  Deliverable: `.githooks/pre-commit` refuses a staged `CHANGELOG.md` that changes or drops a committed entry, except
  a drop that stages an archive shard (the trimmer's commit); RED first by replaying those two commits; selftest cases.
  Also in this commit: S28's receipt cited the archive pointer at `CHANGELOG.md:36`; it is at `:39` — corrected there.

### 2026-10-01 · [ad hoc] S28 close-out — housekeeping done; branches deleted, PR #83 notified, oversight scanner refreshed

- **Action:** closes the S28 claim entry (*Housekeeping … (in progress)*). Non-commit actions this session: merged
  branches `fix/context-budget-fit-skip` and `docs/parallel-sessions-plan` deleted locally and on GitHub, and the stale
  remote `read-set-budgets` (PR #80, merged) deleted — each verified an ancestor of `main` first; a notice of the
  §8A decisions posted on [PR #83](https://github.com/KJ5HST/methodology/pull/83#issuecomment-5942319472), asking
  rmsharp's view on D8 before Phase 3 changes his Test 28; the oversight root's `methodology_dashboard.py` copied
  2.6.1 → 2.11.1 (recorded in the oversight `CHANGELOG.md`). Left for the operator, untouched: two local-only
  unmerged branches, `docs/operator-gated-review-plan` (a 2026-07-31 DRAFT plan awaiting ratification) and
  `experimental/pocock-audit` (17 commits, May). Gate run at `3e857aa`: `quality_ratchet: 11/11 pass · 0 fail ·
  0 unmeasured · results 30d2a763be2b · manifest 58b9c63d75da`.

### 2026-10-01 · [ad hoc] `CLAUDE.md` density re-measured; `.context-budget-history.jsonl` ruled tracked

- **Action:** S28. `.context-budget.json`: `CLAUDE.md` `bytes_per_token` 2.5182 → **2.5687** and `measured_bytes`
  59,119 → 45,842 — the doubled-file read reports 35,693 tokens, so 17,846.5 for the file (the S26 archive moved it
  31% off the old measurement); `max_tokens` 23,483 unchanged (a pin). The tracked-or-ignored ruling open since S23 is
  settled as **tracked**, matching the fork and the reason `.gitignore` already gives (the growth-run trigger reads the
  series, which survives a clone only if committed); its first row is committed here.

### 2026-10-01 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-09-30.md` (96 record(s), 229,112 B → 17,036 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **96** record(s) (2026-06-25 → 2026-09-26) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-09-30.md`](docs/archive/CHANGELOG-through-2026-09-30.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-09-30.md.verify.sh`](docs/archive/CHANGELOG-through-2026-09-30.md.verify.sh)
rather than trusting a digest printed here. Live file 229,112 B → 17,036 B (−92.6%).

### 2026-10-01 · [ad hoc] Backfilled: PR #77 merged 2026-09-03 — the ledger trimmer shipped (`56997af`, merge `907a696`)

- **Action (backfill, not S28's):** [PR #77](https://github.com/KJ5HST/methodology/pull/77) (rmsharp, *Ship the ledger
  trimmer, with tests that run outside this fork* — read-set budgets, 2 of 4) merged at `907a696` on
  2026-09-03T01:38Z: one commit, `56997af` — `starter-kit/methodology_trim.py` and `tools/test_methodology_trim.py`,
  the `bin/_manifest.py` row, the trimmer's seed sections in `starter-kit/CHANGELOG.md` and `starter-kit/HANDOFFS.md`,
  dashboard twins and tests (9 files, +4,691/−6). Neither commit touched this root ledger, so the reconcile gap
  lost sight of it once a later commit edited the ledger (failure mode #27). Found by rmsharp's PR #83 review;
  verified in S27 (`docs/planning/parallel-sessions-plan.md` §8A, row 5). The release that carried it is v3.8.

### 2026-10-01 · [ad hoc] Housekeeping: the items S26 and S27 left open (in progress)

- **Action:** session S28 claimed on `main`. Operator: "Do not leave anything unfinished." This session covers the
  small open items: the PR #77 backfill, the due `CHANGELOG.md` trim, the `CLAUDE.md` density re-measure, the
  `.context-budget-history.jsonl` ruling, merged-branch cleanup, the PR #83 notice, and the oversight dashboard
  refresh. The larger items follow as their own sessions.

### 2026-10-01 · [ad hoc] S27 close-out — the decision receipt completed

- **Action:** S27's `HANDOFFS.md` receipt goes `status: pending` → `complete`; this entry closes the S27 claim entry
  (*Parallel-sessions plan: the twelve §8 decisions (in progress)*). Gate run at `5bab033`: `quality_ratchet: 11/11
  pass · 0 fail · 0 unmeasured · results 30d2a763be2b · manifest 58b9c63d75da`. Not done here, recorded as next
  steps: the PR #77 backfill and the due `CHANGELOG.md` trim found while deciding.

### 2026-10-01 · [ad hoc] Parallel-sessions plan ratified with amendments — §8A records the twelve decisions

- **Action:** S27, under the operator's delegation. `docs/planning/parallel-sessions-plan.md` gains §8A (decision
  table, phase amendments, §9A commands) and its Status moves from DRAFT to ratified-with-amendments. Main
  amendment, measured: `HANDOFFS.md` leaves `merge=union` (rmsharp's objection reproduced — two receipts fuse
  under the default and `zdiff3` styles, merge exit 0; whole only under `diff3`); `CHANGELOG.md` keeps it (trim
  against prepend merges clean at `--cut 1`/`--cut 3`, and the trimmer accepts the result). Also: D5 and FM #29
  wording per rmsharp (FM #29 named *Shared-state interference*); D6 gains a merged-PR ledger check (PR #77's
  `56997af` has no entry here — verified); D8 kept as a requirement and adapted to #87's clone; D11 deferred past
  Phase 5; D12 superseded — the plan ships as v4.1. Nothing implemented.

### 2026-10-01 · [ad hoc] Parallel-sessions plan: the twelve §8 decisions (in progress)

- **Action:** session S27 claimed on `main`. The operator delegated the plan's open decisions ("you do it", answering
  S26's next step (a)). Deliverable: the twelve §8 answers recorded in `docs/planning/parallel-sessions-plan.md`, each
  against rmsharp's PR #83 review and against what has changed since 2026-09-16 (v3.8 and v4.0 shipped; #87 rewrote
  `--source=github`); the claims that can be computed are measured, not assumed. Nothing in the plan is implemented.

### 2026-10-01 · [ad hoc] S26 close-out — the v4.0 receipt completed

- **Action:** S26's `HANDOFFS.md` receipt goes `status: pending` → `complete`. This entry closes the S26 claim entry
  below (*v4.0 — the open pull requests merged and released*), whose `CHANGELOG: pending` line it supersedes; that
  entry is not edited again (see the correction entry below). Gate run cited in the receipt: the one at the tag.

### 2026-10-01 · [ad hoc] v4.0 tagged and released

- **Action (non-commit):** annotated tag `v4.0` at `2f911c9` (tag object `64e5811`), pushed with `main`
  (`746c17a..2f911c9`); [GitHub Release v4.0](https://github.com/KJ5HST/methodology/releases/tag/v4.0) published
  2026-10-01T20:55:11Z, read back as Latest. Gate run at the tagged commit: `quality_ratchet: 11/11 pass · 0 fail ·
  0 unmeasured · results 30d2a763be2b · manifest 58b9c63d75da`. The release: [`CLAUDE.md` §Versioning](CLAUDE.md#versioning)
  v4.0 (pointer, not re-narrated).

### 2026-10-01 · [ad hoc] Correction: the S26 claim entry was edited by two later commits

- **What was wrong:** after PR #84's merge (`99377b3`) made *a committed entry is never edited* a rule of this ledger
  (`FRAMEWORK_APPARATUS.md` §The Action Ledger, *Lifecycle*), S26 kept the older one-entry-per-session habit and
  appended bullets to its own claim entry in `746c17a` (the merges and the tightening) and `d1c1154` (the §Versioning
  archive). Those bullets are accurate and stay; editing them back out would be a third edit. From `2f911c9` on, each
  commit and non-commit action has its own entry.

### 2026-10-01 · [ad hoc] Recorded: v3.8 tagged and released by rmsharp on 2026-09-30

- **Action (non-commit, not S26's):** rmsharp tagged `v3.8` at `6b29d3d` and published its GitHub Release
  (2026-09-30T23:01:13Z) with the README and §Versioning entries deferred; no ledger held it (failure mode #27 —
  reconcile-on-read cannot see a non-commit action). Found at S25's Orient; the deferred docs landed in `2f911c9`.

### 2026-10-01 · [ad hoc] v4.0 release documentation — `CLAUDE.md` §Versioning and `README.md` What's New for v3.8 and v4.0

- **Action:** S26. `CLAUDE.md` *Current version* v3.7 → v4.0; §Versioning gains the v3.8 entry (rmsharp tagged and
  released v3.8 on 2026-09-30 with its docs deferred) and the v4.0 entry; `README.md` What's New gains both, and its
  repository tree a `docs/versioning-archive.md` row. `CLAUDE.md` 40,771 → 45,842 B under its unchanged 59,168 B
  ceiling; `bin/check-links` OK; a sweep for `Current version`, `v3.7`/`v3.8`/`v4.0` and the old gate and test counts
  outside the ledgers found no other stale claim. The release itself: [`CLAUDE.md` §Versioning](CLAUDE.md#versioning)
  v4.0 (pointer, not re-narrated). This opens the ledger's first month heading, per *Placement*; the September entries
  below are not retrofitted.

### 2026-10-01 · [ad hoc] v4.0 — the open pull requests merged and released

- **Action:** session S26 on `main`. Operator: "Merge them and release 4.0." Merge #89 → #88 → #87 → #86 → #85 →
  #84 → #83 onto `main` locally, newest ledger entries first (the order S25's corrected receipt records), each
  `CHANGELOG.md` conflict resolved keep-both with `main`'s side on top; full suite and gate run on the merged tree;
  push; then the v4.0 release docs (README What's New, `CLAUDE.md` §Versioning — which also owes the undocumented
  v3.8), tag and GitHub Release. `CHANGELOG: pending` — results appended at close-out.
- **Seven merges** (claim `1befe64`), first-parent: [#89](https://github.com/KJ5HST/methodology/pull/89) `19f8d4f` →
  [#88](https://github.com/KJ5HST/methodology/pull/88) `19566b6` → [#87](https://github.com/KJ5HST/methodology/pull/87)
  `af8a693` → [#86](https://github.com/KJ5HST/methodology/pull/86) `a4eeef3` →
  [#85](https://github.com/KJ5HST/methodology/pull/85) `a9946c6` → [#84](https://github.com/KJ5HST/methodology/pull/84)
  `99377b3` → [#83](https://github.com/KJ5HST/methodology/pull/83) `d7768cb`. Ledgers merged keep-both with
  `git merge-file --union --diff3` — diff3 keeps git from refining the shared fence lines out of two prepended
  `HANDOFFS.md` receipts, the fusion rmsharp's #83 review demonstrated; `bin/check-handoff --all` after every merge
  (receipts S26 → S25 → S24 → S23). Two non-ledger conflicts: `.quality-gates.json` at #86 (two `min` floors →
  the larger of each) and `starter-kit/BOOTSTRAP.md` at #84 (#87's head + #84's tail, the resolution #87's body
  documents). #84's own entries keep their branch order below, per its new *Placement* rule.
- **Gate run on the merged tree (`d7768cb`):** `quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results
  219197070a3b · manifest 21dd9f1c1d67` — `bin/tests.sh` 215/0. **Tightening owed and taken:** `tests-sh-passed`
  188 → 215, `context-budget-unit-tests` 140 → 145, `trimmer-unit-tests` 123 → 124 — `746c17a`; pushed
  `6b29d3d..746c17a`, and GitHub read back all seven PRs as MERGED.
- **Room for the release entries (operator's choice of three):** `CLAUDE.md` stood at 59,119 B under its pinned
  59,168 B resident ceiling. The v1.0–v2.9 §Versioning entries (17 entries, 18,537 B) moved **verbatim** to new
  `docs/versioning-archive.md` (canonical-only, not distributed), with a one-line pointer in their place — the
  archive body compared byte-equal to the span at `746c17a`. `CLAUDE.md` → 40,771 B; the ceiling is unchanged.

### 2026-10-01 · [ad hoc] Fit-gate end-to-end test skips, never fails, when the data refuse the fit

- **Action:** session S25 on branch `fix/context-budget-fit-skip` (from `main` at `6b29d3d`). S24's
  next step (a0): `tools/test_context_budget.py` `TestFitGateEndToEnd.setUp` skips only on calibrate()'s
  "not enough" refusal, but calibrate() has further refusals that depend on the machine's transcripts, not
  on the floor under test — a non-positive slope or an undefined R² (refused at every floor), and no
  variation in the regressor ("cannot fit") — so on such a machine the two tests FAIL instead of skipping
  (S24 measured it: 4 transcripts, slope −3.57, `bin/tests.sh` 138/1, `--run` 8/10). One file, RED first.
  Claimed at `1a36282`; results below.
- **The fix (one file, `tools/test_context_budget.py`):** `setUp` now skips on both stops calibrate() names
  ("not enough", "cannot fit"), then probes the admitting floor 0.0 and skips when the refusal there does not
  cite the floor — the data decided it, not the gate under test. A refusal that *does* cite the floor at 0.0 is
  not skipped: no defined R² is below 0.0, so it would mean calibrate() applied the wrong floor. New unit test
  `test_only_the_floor_refusal_names_the_floor` pins that word as the discriminator (118 → 119 tests).
  **RED first** — the natural failure no longer reproduces here (a 5th transcript turned the slope positive),
  so it was reproduced with a fixture `HOME` whose synthetic transcripts give each shape, tool and test
  unmodified: negative slope and flat response FAILED the presence control, no regressor variation FAILED
  both tests; after the fix all three skip, naming the cause, while a positive and a low-R² fixture still run
  and pass. Three mutant `calibrate()`s (ignores its floor, prints nothing, always refuses) are still caught —
  failed, never skipped — on both admitting fixtures and on this machine's real transcripts.
- **Gate run at `229f08d`:** `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results a3b034f8cabf ·
  manifest 97a7aab85b9a` — `bin/tests.sh` 139/0 again on this machine. **Tightening owed and taken:**
  `context-budget-unit-tests` 118 → 119 (the new pin test), per the manifest's standing rule — `02677ea`;
  re-run at the tightened manifest: `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results f5d8c427f056 ·
  manifest b2e7f7752273`.
- **PR opened (non-commit action):** [PR #89](https://github.com/KJ5HST/methodology/pull/89) from
  `fix/context-budget-fit-skip` at `02677ea`, read back from the API (OPEN, +60/−4, 4 files). **Not merged.**
- **Observed, not acted on:** every open PR (#83–#88) and this branch share base `6b29d3d`; `git merge-tree`
  shows each pair conflicting on the `CHANGELOG.md` top anchor except #84 (clean against all but #87, on
  `starter-kit/BOOTSTRAP.md`), plus #86×#87 on `.quality-gates.json` and this branch×#83 on `HANDOFFS.md`.
  The v3.8 tag and GitHub Release (rmsharp, 2026-09-30, at `6b29d3d`) are not yet in this ledger — the
  release-docs session records them. The operator's "clean everything up so we can merge and version" is
  sequenced in the S25 receipt's next steps, not started here.
- **Correction — merge order:** the receipt's first draft put #84 first; the operator proposed 88 → 87 → 84
  and a scratch-clone simulation of both orders backed it — same final tree except `CHANGELOG.md` order, where
  only newest-entries-first keeps a keep-both resolution newest-on-top (84-first put #88's 09-26 entry below
  #87's 09-21 ones); `bin/tests.sh` on the 88 → 87 → 84 tree 212/0. Receipt `next_steps` (b) corrected in place.

### 2026-09-30 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-09-30.md` (89 record(s), 250,288 B → 97,576 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **89** record(s) (2026-09-26 → 2026-09-30) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-09-30.md`](docs/archive/CHANGELOG-through-2026-09-30.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-09-30.md.verify.sh`](docs/archive/CHANGELOG-through-2026-09-30.md.verify.sh)
rather than trusting a digest printed here. Live file 250,288 B → 97,576 B (−61.0%).

### 2026-09-30 · [ad hoc] S238 — decisions D1, D2 and D4 taken; plan text made plain

Operator, from a picker: **D1** v3.0, v3.8 without ratchet and v3.8 with ratchet on the tempting task, 5 runs each (about $48; v3.7 reused on the plain task only); **D2** authorise P1 (build, $0) only; **D4** decide the session chain after the main test reports. D3 (publication) left open and not needed until P5; D5 and D6 conditional. [`docs/planning/ratchet-mechanism-test-plan.md`](docs/planning/ratchet-mechanism-test-plan.md) gained an "In plain words" section and a §7 that states each decision's status. The `HANDOFFS.md` S238 receipt's next step (1) was rewritten to say so: P1 is authorised and is the next deliverable.

### 2026-09-30 · [ad hoc] S238 — the ratchet plan revised: overhead and v3.0 comparison, outcome-based rigor

Operator, after the first draft: no overhead testing and no v3.0 comparison, and rigor is not well tested. Revised [`docs/planning/ratchet-mechanism-test-plan.md`](docs/planning/ratchet-mechanism-test-plan.md): arms are now v3.0, v3.7 (control, reused), R0 and R1; three named contrasts (mechanism, v3.8's other changes, v3.0 to current); overhead (H4) measured on every arm; rigor redefined by what the session leaves true (gates held, real fix, erosion paths, claims versus tree) because S237's process-presence score was at ceiling; reuse of S237's runs made conditional on P1; budget restated at about $93 of $105.45 with the chain deferred. Still a draft; no spend.

### 2026-09-30 · [ad hoc] S238 close-out — the handoff receipt

`HANDOFFS.md` receipt S238 completed: self 8, predecessor S237 scored 8 (clear next step and gotchas; its "ratchet in no release tag" went stale when v3.8 was tagged the same day, which is timing, not an error). Phase 3C: no fork learning row appended, so no retirement is owed. Gate: `quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results 95b5ea74bd7c · manifest 01a4ae7aa511`. **Next: the operator answers the plan's D1-D6; then P1 (free).** Nothing pushed; nothing on `KJ5HST/methodology`.

### 2026-09-30 · [ad hoc] S238 — the plan for testing the quality ratchet

Wrote [`docs/planning/ratchet-mechanism-test-plan.md`](docs/planning/ratchet-mechanism-test-plan.md) (DRAFT, no spend): a mechanism ablation (v3.8 with hook and declared gates against the same files with none), a control task, and a k=4 session chain. **Finding:** the v3.8 tag contains `quality_ratchet.py` (`git ls-tree -r --name-only v3.8`; tag `555fb9c` peels to `6b29d3d`, an ancestor of `main`), so S237's "in no release tag" is stale and the arm is a tag, not main; a correction line was added to `docs/planning/overhead-replay/pilot/real-3.7/RESULTS.md`. Budget estimate about $114 against $105.45 remaining: P2 and P3 fit, P4 depends on P3's real cost.

### 2026-09-30 · [ad hoc] S238 claim — the plan for testing the quality ratchet (in progress)

Phase 1B. Deliverable: a plan document under `docs/planning/` for (a) a mechanism ablation of `quality_ratchet.py` and (b) a session chain, as S237's handoff item 1 and the operator's "write the plan after this experiment" ask. No model spend is authorised or incurred. Owed items done first at the operator's Phase 0 go-ahead: the `HANDOFFS.md` retention trim (`8d91a68`, fold `ab5ed59`) and the `CHANGELOG.md` archive trim (`07af992`, 250,288 B to 97,576 B, forced past SRF-RED; `bash bin/tests.sh` 355 passed / 0 failed / 6 skipped afterwards). Predecessor S237 scored 8 (see its receipt). `CHANGELOG: pending`.

### 2026-09-30 · [ad hoc] Fold of the `HANDOFFS-through-2026-09-29` pointer block into the shard index

Trim commit `8d91a68` wrote the pointer block; this commit, separate per fork Learning #58, adds the row to [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md) and deletes the block from `HANDOFFS.md`. The shard's `.verify.sh` and `bin/check-handoff --all` both pass after the fold. Operator go-ahead given at Phase 0 (S238).

### 2026-09-30 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-29.md` (2 record(s), 35,617 B → 15,662 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-09-29 → 2026-09-29) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-29.md`](docs/archive/HANDOFFS-through-2026-09-29.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-29.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-29.md.verify.sh)
rather than trusting a digest printed here. Live file 35,617 B → 15,662 B (−56.0%).

### 2026-09-30 · [ad hoc] Tagged v3.8 on upstream and published its GitHub Release (operator-directed)

**Non-commit action** (failure mode #27). At the operator's explicit direction, after a picker that named the alternatives (hold; tag upstream `6b29d3d`; tag the fork only), created annotated tag `v3.8` on `upstream/main` at **`6b29d3d`** and pushed it to `KJ5HST/methodology`, then published the GitHub Release from it (marked latest; previous latest `v3.7`). Both read back: `git ls-remote --tags upstream` shows `v3.8^{}` = `6b29d3d`; `gh release view v3.8` shows the tag, not a draft, not a prerelease.

Contents follow the maintainer's own v3.8 list (`upstream/main:HANDOFFS.md:18`): `quality_ratchet.py`, `context_budget.py`, `methodology_trim.py`, manifest 24 to 29 rows, dashboard 2.10.6 to 2.11.1. **Not done, and stated in the release notes:** the README "What's New" and `CLAUDE.md` §Versioning v3.8 entries the maintainer's procedure calls for, so the tagged commit's docs still say v3.7. The tag was cut at `upstream/main`, not this fork's `main`. PRs #83-#88 are not in it.

### 2026-09-29 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-28.md` (2 record(s), 62,788 B → 25,567 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-09-28 → 2026-09-28) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-28.md`](docs/archive/HANDOFFS-through-2026-09-28.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-28.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-28.md.verify.sh)
rather than trusting a digest printed here. Live file 62,788 B → 25,567 B (−59.3%).

### 2026-09-29 · [ad hoc] S235 — fork push: `origin/main` `4c5905b` → `481f948`

Operator go-ahead, given in reply to the close-out report's question. 17 commits, fast-forward
(`merge-base --is-ancestor` asserted first), to the fork `origin` (`rmsharp/methodology`) only. Nothing went to
`upstream`; pull requests #83–#88 untouched; no branch other than `main` pushed.

### 2026-09-29 · [ad hoc] S235 — the trim's pointer block folded into the archive index

`HANDOFFS.md` receipts 4 → 2 (`32b13ca`, shard `HANDOFFS-through-2026-09-28.md`, `.verify.sh` OK: L1, L2, L3).
Its 3-line pointer block is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md`, in its own commit (fork Learning
#58). The forecast in S234's handoff said the shard would be `-9`; the trimmer named it by date
(`2026-09-28`, no suffix) — the forecast came from shard names, not a measurement.

### 2026-09-29 · [ad hoc] S235 close-out — the handoff receipt

Phase 3A–3F. `status: complete`, **self 8, predecessor 9 → 8**.

**Deliverable, approved by the operator:** `docs/planning/cross-version-overhead-measurement-plan.md` —
a controlled replay of one fixed task under each historic version's own framework files, plus a
no-framework baseline, scored on cost and on seeded traps caught. Four phases (harness, pilot, full run,
analysis), one session each; P1 spends no model tokens. Nothing was run. D2 (spend), D3 (publication)
and D5 (manual fallback) stay the operator's.

**Predecessor score 8, not 9.** S234's next-steps were accurate to the byte where I checked them
(`CHANGELOG.md` 224,134 B, the receipt count of 3, the ten unpushed commits, BL-93's counts). The gap is
that (3) recorded the operator's question *"where is the plan to measure overhead?"* as **answered** by
pointing at the BL-91 scripts, when he meant a planning session he had been promised. It cost a Phase 0
picker round here. Memory `feedback_a_where_is_the_plan_question_may_mean_it_was_never_made`.

**No fork Learning row appended** — so D3 of `fork-learnings-retirement-rule-plan.md` is not triggered and no
row is retired; the lesson went to memory instead. **Found:** `overhead-ratchet-plan.md` §2.4's
"transcripts begin 2026-08-16" is true of this repository only; correction is in the handoff, not yet made.
**Owed and deferred by the operator's ordering:** the `HANDOFFS.md` retention trim.
**Model:** Claude Sonnet 5.5.

### 2026-09-29 · [ad hoc] S235 claim — plan the cross-version overhead measurement

Phase 1B. Deliverable: one planning document under `docs/planning/` for measuring methodology overhead
across versions. Chosen by the operator at Phase 0 after he noted that a session for this plan had been
promised and not held; the earlier answer pointing at `bl91-overhead-measurement/` did not satisfy the
request. Ledger: `CHANGELOG: pending` — this entry says (in progress); Phase 3F records the rest. The
owed `HANDOFFS.md` retention trim (receipts now 4) is deferred to close-out, by the operator's ordering.

**Draft written:** `docs/planning/cross-version-overhead-measurement-plan.md` — primary design is a
controlled replay of one fixed task under each historic version's own framework files (operator's
direction: no detailed historic data exists to pull). Awaiting his approval; no model session launched.
Operator review fixed one unclear sentence in the plan's §1 (the "gap" paragraph) and rewrote §5 (the phases) in plain language.

### 2026-09-29 · [BL-69] S234 close-out — the handoff receipt

Phase 3A–3F. `status: complete`, **self 8, predecessor 9**.

**S233's receipt scored 9, and the score is mostly about how much of it was checkable and checked out.**
Its next_steps (1) gave the trim command, the depth and the forecast shard `-8` — **`-8` is exactly what the
trimmer named**. (5) predicted `tests-sh-passed` 355 at rest and **361 inside a claim**; 361 measured, twice,
on two trees. (5)'s hash shapes — *results moves, manifest does not* — held exactly. (2) recorded the push as
a **declined decision rather than an omission** and told me to run `git rev-list --count origin/main..HEAD`
instead of trusting a number, which was right. (4b) told me how to treat a red gate before believing it.
**The two gaps:** (9) pointed at the **262,144 B hard refusal** and told me to measure, but said nothing about
the **196,608 B archive trigger** — which was already firing when I measured, and is the threshold that
actually wanted a decision this session. And S231's gotcha that `.quality-gates-results.json` is gitignored
and describes whatever tree last ran the ratchet did not get carried forward into S233's, so the Phase 0
citation check met it fresh.

**Self 8.** For it: the one deliverable was finished end to end including its outward half; the evidence was
**written and committed before the destructive action**, which is the only ordering that survives it; the
broken `--all` instrument was caught by its own odd row and re-run **with controls**, and the discard is on
the record rather than quietly replaced; the C6 red was produced by **running the checker, not predicting
it**; and BL-93 was raised with its derivation rather than fixed, keeping one deliverable one deliverable.
Against it: **the control should have come before the first measurement, not after** — I published a
uniform *survives* across seven branches and only doubted it because `docs/bl-10` looked wrong, which is
luck standing in for method; the Phase 0 ratchet run dirtied a tracked file before I had decided what to do
with it; and the receipt was missing its gate citation until `bin/check-handoff` said so, which is the
checker doing my job.

### 2026-09-29 · [ad hoc] S234 Phase 3C — fork Learning #105, and a refusal to retire, with the rows named

[`docs/FORK_LEARNINGS.md`](docs/FORK_LEARNINGS.md) row **#105**: *a decided-but-unexecuted destructive
action rots in what was CREATED after the decision, not in the targets it named — so re-verify the list,
then re-derive the exclusion set.* 90 rows, contiguous 15..105, 0 over the 1,500 B row budget.

**No row is retired, and this is the refusal D3 requires rather than silence** — the rows considered against
the three criteria, and why each stays:

- **#77** (*a remote-tracking ref is the last fetch's answer*) — the nearest neighbour, and the row this
  session actually ran on: `git ls-remote` was the authority for both read-backs, and `refs/pull/<N>/head`
  is what §3.1 checked. **No gate enforces it**; nothing in `bin/tests.sh` or `.quality-gates.json` refuses
  a claim sourced from a cached ref, and #105 does not state it — #105 is about the exclusion set, not about
  which ref answers.
- **#81** (*a population recorded as a LIST decays*) — **falsified as retired by this very session**, which
  found a live instance and raised it as BL-93. A row still producing defects fails criterion (a) by
  demonstration.
- **#22** (*a completed item's text can be load-bearing; no test catches it*) — the closest thing to a gate,
  because `BACKLOG-COMPLETED.md.verify.sh`'s C6 did catch a closure this session got wrong. But C6 asserts
  the **id's** reachability, not that prose referring to a removed item still resolves, and #22's own repair
  (*remove a mutually-referencing cluster only whole*) is untested by it. **Partial coverage is not (a).**
- **#55** (*a plan's expected values are predictions too*) and **#74** (*another repository's state is a
  reading with a time on it*) — both adjacent to #105's forecast half; neither is stated by #105 at least as
  generally, because #105 is deliberately narrower.

### 2026-09-29 · [BL-93] S234 — raised: the `Open:` list omits five open items, inside the file that warns about lists

[`docs/planning/BACKLOG.md`](docs/planning/BACKLOG.md)'s hand-maintained **Open:** list at `:8` names **52**
items while the index table below it carries **57** rows. The five missing are **BL-63, BL-88, BL-89, BL-90,
BL-91** — four of them raised in the last eight sessions, and BL-91 is the item the last three sessions were
executing. Found while removing BL-69 from that list; derived, not eyeballed, with the script quoted in the
[detail body](docs/planning/BACKLOG-DETAIL.md#bl-93). Nothing in the prose list is absent from the index, so
it only under-reports; `BL-20` sitting in both the index and `BACKLOG-COMPLETED.md` is its documented
*residual only* split and is not part of the finding.

**It is [fork Learning #81](docs/FORK_LEARNINGS.md) happening inside the file that prints #81's warning and
the grep beside the list** — which is why it is raised as a decision (repair the list, delete it in favour of
the grep, or gate the two populations against each other) rather than quietly fixed. **Not fixed: BL-69 was
this session's one deliverable.** Fork-only; no adopter is affected.

### 2026-09-29 · [BL-69] S234 — BL-69 closed in the records, and the move proof caught the closure I got wrong

BL-69 removed from [`BACKLOG.md`](docs/planning/BACKLOG.md)'s index table and its hand-maintained open
list, an outcome row appended to [`BACKLOG-COMPLETED.md`](docs/planning/BACKLOG-COMPLETED.md), and its
[`BACKLOG-DETAIL.md`](docs/planning/BACKLOG-DETAIL.md) body headed with a DONE note that leaves the S189
measurement below it unedited.

**`BACKLOG-COMPLETED.md.verify.sh` went red on that edit and was right to.** Its **C6** — added at S226 for
BL-86, so the proof *reports* later closures instead of refusing them — asserts that every item closed since
the move still has its id in the file Phase 0 reads: *"no id in `docs/planning/BACKLOG.md` for BL-69 —
closed, and no longer findable from the file Phase 0 reads."* **Removing the index row is only half of
closing an item here; the id has to stay** in the block at `BACKLOG.md:197`, which exists for exactly this,
and whose own comment names the case it was written for (*"BL-27 … S88 needed it and could not find it even
while it was in the live file"*). Added `**BL-69**` between `**BL-67**` and `**BL-72**`; all three
`docs/planning/*.verify.sh` proofs then exit 0, and the block's 36 ids match
`grep -cE '^\| \*\*BL-[0-9]+\*\* \|' docs/planning/BACKLOG-COMPLETED.md` = 36.

### 2026-09-29 · [BL-69] S234 — eleven finished branches deleted on fork `origin`; BL-69 complete

On the go-ahead asked for and given at the moment it happened, after the exact eleven commands were shown
in full. Each was pinned with `--force-with-lease=refs/heads/<b>:<sha>` at the sha
[`docs/planning/bl69-branch-deletion-inventory.md`](docs/planning/bl69-branch-deletion-inventory.md) §3
records, so a branch that had moved would have been refused rather than clobbered; **all eleven reported
`[deleted]`, none was refused.** Deleted: `fix/bl31-context-budget-dashboard-exclusion` `b2ef20a`,
`fix/caveman-length-citation-upstream` `b4ceb73`, `fix/dashboard-r-quarto-rmarkdown-extensions` `c4fd879`,
`fix/doc-only-thresholds-upstream` `86adc6c`, `fix/handoffs-receipt-spec-upstream` `dc75cf6`,
`pr1/framework-learnings-extraction` `5b92b2f`, `pr2/ledger-trimmer` `56997af`, `pr3/apparatus-extraction`
`2c30d0f`, `pr4/context-budget-gate` `cf15489`, `docs/learning-13-handoff-predictions` `73b72c0`,
`docs/bl-10-dangling-learning-citations` `268f1e5`.

**Read back with `git ls-remote --heads origin`, which is the authority rather than a pruned cache:**
`origin` now holds **six** refs — `main` `4c5905b` and the five open pull-request heads, each at its exact
sha (#84 `77afc12`, #85 `e2501c5`, #86 `c1167ae`, #87 `67feb9f`, #88 `a88fce7`). All six pull requests
remain **OPEN**, and upstream's `refs/pull/64|69|76/head` still resolve. **`upstream/main` untouched at
`6b29d3d`; nothing reached `KJ5HST/methodology`.**

**`git branch -a` 40 → 19, not the ~10 BL-69 forecast** — that forecast was written at S189, before four of
the five fork-side pull requests existed, and each contributes a local and a remote-tracking ref. The
forecast was stale, not wrong in method. The dashboard's *"Multiple branches"* signal still fires, which is
[BL-71](docs/planning/BACKLOG-DETAIL.md#bl-71) by construction.

### 2026-09-28 · [BL-69] S234 — every affected pull-request head is retained upstream; one sha is not, and was adjudicated

Added §3.1 to [`docs/planning/bl69-branch-deletion-inventory.md`](docs/planning/bl69-branch-deletion-inventory.md)
before asking for the `origin` go-ahead. `git ls-remote upstream` shows **all eleven**
`refs/pull/<N>/head` refs present (#63, #64, #68–#72, #76–#79), so ten of the eleven `origin` branches are
the same sha upstream already keeps forever.

**The exception is #69:** upstream retains `dc3b405` while `origin` carries `dc75cf6`, making that the only
deletion in this item that would put a commit beyond every reach. Measured rather than assumed: the tip
commits are **patch-identical** (`git patch-id --stable` → `e4d76b99…` for both), and their parents'
differing patch-ids are **hunk offsets, not content** — the added and removed lines in
`starter-kit/HANDOFFS.md`, the distributed file the pair exists to fix, diff to nothing. This confirms
S189's *"the changed lines were compared: identical"* and extends it from local-vs-`origin` to
`origin`-vs-upstream's retained head.

### 2026-09-28 · [BL-69] S234 — ten finished local branches deleted; local count 18 → 8

The half of BL-69 that needs no outward action, executed against
[`docs/planning/bl69-branch-deletion-inventory.md`](docs/planning/bl69-branch-deletion-inventory.md) §2 at
the shas it records. `git branch -d` took the three ancestors —
`pr80/f1-learnings-1-13` `d4e1570`, `pr80/f2-installed-source-guard` `3774076`,
`pr80/f3-read-set-token-ceilings` `aa36fd8` — and `-D` the seven settled non-ancestors:
`fix/bl31-context-budget-dashboard-exclusion` `9845b4d`, `fix/caveman-length-citation-upstream` `f1dd996`,
`fix/dashboard-r-quarto-rmarkdown-extensions` `6380139`, `fix/doc-only-thresholds-upstream` `b52c1a9`,
`fix/handoffs-receipt-spec-upstream` `311c554`, `docs/bl-10-dangling-learning-citations` `268f1e5`,
`port/framework-learnings-extraction` `7d5b186`.

**Local branches 18 → 8; `git branch -a` 40 → 30.** Every branch left is accounted for: five are open
pull-request heads (#84, #85, #86, #87, #88), `docs/issue75-plan-surface-upstream` is BL-70's keep, `main`
is `main`, and `pr83` is a local copy of upstream's own #83 head at `219fb9d` — **not a BL-69 candidate,
because the S189 decision named a list and this is not on it.**

**BL-69 is not yet complete:** its 11 `origin` refs are untouched and deleting them is outward-facing.
As the dashboard's *"Multiple branches"* signal counts `git branch -a`, it still fires at 30 — [BL-71](docs/planning/BACKLOG-DETAIL.md#bl-71), by design, not a shortfall here.

### 2026-09-28 · [BL-69] S234 — the branch inventory re-derived, written before a single branch was deleted

[`docs/planning/bl69-branch-deletion-inventory.md`](docs/planning/bl69-branch-deletion-inventory.md) —
every one of BL-69's 21 candidate refs re-measured at `main` = `bcd990a`, recorded **before** the
destructive half, so the shas survive the action that makes some of them unreachable. Fork-only;
`docs/planning/` is not in `bin/_manifest.py`.

**All 21 shas are exactly what S189 recorded 45 sessions ago — nothing moved.** What moved is the
surrounding state, and it is what made the S189 list unsafe to apply verbatim: **six pull requests are open
upstream and five have their head on this fork's `origin`** (#84 `bl57/changelog-rules`, #85
`fix/pre-commit-stale-rebase-marker`, #86 `fix/context-budget-status`, #87 `fix/sync-github-history`, #88
`fix/bootstrap-never-overwrite-rules`); four of them postdate S189. None is a candidate, and §1's table is
how that is established rather than assumed. `bl57/changelog-rules` is additionally checked out in the
`methodology-bl57` worktree.

**One measurement had to be thrown away and re-taken.** Survival of the seven non-ancestor branches was
first tested with `git log --all --grep <subject>`, which searches every ref and so matched each branch
against itself, returning a uniform *survives*. The tell was `docs/bl-10-dangling-learning-citations`,
whose pull request #64 **closed unmerged**, coming back green. Re-run against `upstream/main` alone, with a
negative and a positive control, five of the `fix/*` branches survive as named rebased commits,
`docs/bl-10` survives as upstream `refs/pull/64/head` (verified by `git ls-remote`), and
`port/framework-learnings-extraction`'s tip does not survive at all — adjudicated in §4 rather than waved
through: it is a `CHANGELOG.md` bullet counting referents in the **port** tree, which is not a correction of
`main`'s count of the **fork** tree, because the bullet's subject is *"this tree"*.

**Nothing is deleted by this commit.** The local half follows; the `origin` half is outward-facing and takes
its own go-ahead.

### 2026-09-28 · [BL-69] S234 claim — delete the branches whose work is finished (in progress)

Chosen by the operator at this session's Phase 0 picker, from a decision he took at S189 that was never
executed. **The claim's first obligation is to distrust its own item:** BL-69's branch list, shas and
merged-ness were measured on 2026-09-18 and the item says in its own *How, when it runs* paragraph to
re-derive them, because branches move. **Four of the six open upstream pull requests did not exist when
that list was written**, so a branch-by-branch mapping to open-pull-request heads comes before any
deletion. The local half needs no outward action; **the `origin` half is outward-facing and takes its own
go-ahead at the moment it happens.** Ledger: `CHANGELOG: pending` — this entry says (in progress) and
Phase 3F records the rest.

### 2026-09-28 · [ad hoc] The trim's pointer block folded into the archive index — rows 69 → 70

The fold that every trim owes, in its own commit for the documented reason: inside the trim commit the
shipped `.verify.sh` fails L2 (fork Learning #58). The trimmer's three-line block left
[`HANDOFFS.md`](HANDOFFS.md)'s front matter (42,962 B → 42,506 B) and became one row at the bottom of
[`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md), per that file's own §Adding a row —
`n`, the span, the bare shard name linked as `archive/<name>`, the trimmer version, and the `.verify.sh`
link dropped because the proof sits beside its shard. Teaching the generator to write the row itself is an
upstream change, since the generator is distributed.

### 2026-09-28 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-27-8.md` (1 record(s), 57,889 B → 42,962 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-27 → 2026-09-27) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-27-8.md`](docs/archive/HANDOFFS-through-2026-09-27-8.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-27-8.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-27-8.md.verify.sh)
rather than trusting a digest printed here. Live file 57,889 B → 42,962 B (−25.8%).

### 2026-09-28 · [ad hoc] The Phase 0 fork push, `016b3ae..4c5905b` — eight commits, on a go-ahead asked for here

Eight commits to fork `origin` on the go-ahead given at S234's Phase 0 picker: S233's claim, the D1
ratification, the printer and its test, fork Learning #104, S233's close-out receipt, the two record
corrections, and BL-92. **The push was offered and DECLINED at S233's close-out, so this is a new
go-ahead, not a carried-over one** — the only standing grant remains a `CHANGELOG.md`-only push record.
Read back with `git ls-remote` and `git rev-list --count --left-right`: `origin/main` = local `main` =
`4c5905b`, **0/0**. `upstream/main` untouched at `6b29d3d`; **nothing reached `KJ5HST/methodology`.**

### 2026-09-28 · [ad hoc] S234 Phase 0 — the gate citation re-verified against a run, not against a stale file

`SESSION_RUNNER.md` Phase 0 step 6 checks the newest receipt's `quality_ratchet:` citation against
`.quality-gates-results.json`, and that file is **`.gitignore`d** (`:16`), so what sat on disk was a local
artifact of an older run — head `0aeeec1`, results `2f8fe36c7a92` — which would have read as a
contradiction of S233's citation had it been believed. Took the step's own alternative and re-ran
`quality_ratchet.py --run`: **11/11 pass · 0 fail · results `95b5ea74bd7c` · manifest `01a4ae7aa511`**,
identical to the receipt, unmoved manifest hash included. `tests-sh-passed` measured **361** against the
343 floor (three receipts, so Test 34's six whole-ledger assertions ran rather than printing as SKIPs).
**BL-92's red did not recur — 1 red in 6 runs at this tree.** The run appends one tracked row to
`.context-budget-history.jsonl` (BL-75: the default measurement writes), which is the tracked change this
commit carries; the row is kept rather than reverted, as its three predecessors were.

### 2026-09-28 · [ad hoc] S233 — BL-92 raised: one red suite run in five, and the failing assertion is unrecoverable

**Found while verifying this session's own final tree, which is the only reason it was found at all.** At
`5d6fbe4`, `bash bin/tests.sh` read **361 passed / 0 failed** and `quality_ratchet.py --run` then read
**10/11 pass · 1 fail** in the same clone — `tests-sh-passed` 360, `tests-sh-failed` 1. **Four re-runs at that
same commit all read 361 / 0 and 11/11:** a fresh clone under the ratchet's own
`subprocess(capture_output=True)` invocation, two consecutive runs in one clone, the clone-then-ratchet sequence
repeated, and a full ratchet run with the suite's output captured. **1 red in 5, and the identity of the failing
assertion is gone** — the ratchet keeps each gate's extracted number and discards its output, so a suite
failure inside a ratchet run leaves a count and no test name. That is the second edge of *capture the suite's
output when the count matters*: uncaptured, a transient failure is not inconvenient to diagnose, it is
**unattributable forever**.

**The suspect is named as a suspect, in this session's own new test.** `bin/tests.sh:3595`-`3606` (Test 44)
compares `git status --porcelain` over the **whole live repository** before and after two `bin/check-overhead`
runs; grep says it is the suite's only assertion over the live tree's entire state — the one other
`git status --porcelain` reads a scratch fixture — so it is the only one unrelated churn can red, and its
message prints both snapshots without naming the differing paths. **Not a diagnosis:** the four re-runs include
the exact invocation that failed, and none reproduced it.

**One method finding, recorded because it cost a run and produced false failures.** Wrapping `bin/tests.sh`
itself to capture its output is not a neutral instrument: the suite greps and re-invokes its own source, so the
wrapped run reported **three** failures, all artifacts of the wrapper. A **separate** wrapper file named in the
gate's `command` captures the same output and leaves the source untouched.

**Recorded, not fixed (FM #17)** — three shapes in [`BACKLOG-DETAIL.md`](docs/planning/BACKLOG-DETAIL.md#bl-92),
none costed, and the receipt tells the next session to re-run a red citation before believing it.

### 2026-09-28 · [ad hoc] S233 — two operator decisions at close-out: the push declined, the publishing question deferred

**Both are recorded because a declined go-ahead and a deferred decision are actions, and the difference between
*asked and declined* and *never asked* is the whole value of the record.** (1) **The push was offered and
declined:** the session's commits stay on this machine; `origin/main` remains at `016b3ae`. The receipt's
`next_steps` (2) now says so, replacing a line that read as though the go-ahead had simply not been sought.
(2) **D3 — where the reported number gets published — was put to him and deferred to the next session**, so
[`overhead-ratchet-plan.md`](docs/planning/overhead-ratchet-plan.md) §7's P3 stays blocked by an explicit
deferral rather than by an open question, and the next session's Phase 0 picker is where it belongs.

**Nothing reached any remote.** `upstream/main` untouched at `6b29d3d`; nothing on `KJ5HST/methodology`.

### 2026-09-28 · [ad hoc] S233 — the unpushed-commit count was stale in its own commit; both records now name the command

**Third instance of one defect, and the generalisation is now applied to a second quantity.** The close-out
receipt said *"`origin/main` IS THREE COMMITS BEHIND"* and named three of five; the ledger entry beside it said
*"four commits behind"*. Both were written before the commits that carried them, so both were false the moment
they landed — `git rev-list --count origin/main..HEAD` reads **5**. Each now names that command plus
`origin/main`'s fixed sha `016b3ae`, which cannot rot, exactly as S232 replaced its `CHANGELOG.md` size with
`wc -c` (`016b3ae`) and its plan line count (`674c6a8`). **The rule has now cost three quantities: a file size,
a line count, and a commit count.** Any figure describing the session's own output is measured on a draft;
write the command, or measure after the last commit — which, for a figure inside that commit, is impossible by
construction.

### 2026-09-28 · [BL-91] S233 close-out — the printer shipped, the gate refused, three receipts left standing

**Close-out receipt in [`HANDOFFS.md`](HANDOFFS.md): `status: complete`, self 8, predecessor 9.** The session's
four actions are each logged above: the claim `22c74da`, the D1 ratification `5372608`, the deliverable
`d1f1a7d`, and fork Learning #104 `9769572`. Verified in a `--no-local` clone at `d1f1a7d` with HEAD asserted
by sha: `bash bin/tests.sh` **361 passed / 0 failed / 0 skipped**; `quality_ratchet: 11/11 pass · 0 fail · 0
unmeasured · results 95b5ea74bd7c · manifest 01a4ae7aa511` — **the results hash moved and the manifest hash did
not, which is the signature of a session that added tests and no gate.**

**Two states the next session inherits, both deliberate.** (1) **Three receipts stand against a settled
retention depth of two**, so a `--cut 2 --force` trim is owed at its Phase 0, after the count is reported;
shards run through `-7`. (2) **Nothing was pushed** — `origin/main` stands at `016b3ae`, where this session started; count with
`git rev-list --count origin/main..HEAD`, since a number written here is measured before the commits that
follow it. No push go-ahead was asked for at this session's picker. The only standing grant is a `CHANGELOG.md`-only push
record, which does not cover a session's work.

**The open question this session surfaced is a decision, not a phase:** shape A asks for *"report better … and
publish the version series somewhere a release must look"*, and only the first half exists. A printer nobody
runs reports nothing. Where the number gets published is D3, unratified; P3 implements one of its options and
must not be built until it is taken.

### 2026-09-28 · [ad hoc] S233 Phase 3C — fork Learning #104, and no retirement

**Row #104:** a decision taken *against* a plan's recommendation neither makes the plan moot nor leaves its
phases intact — classify every phase at ratification time, in the plan, and leave the losing recommendation
standing as the record the decision was made against. Source: this session, where §7 of a plan written *"if
D1(b) is ratified"* met a ratification of D1(a) and its three phases went three different ways (P1 survived
unchanged, P2 became out of scope rather than deferred, P3 was untouched because it hangs off an unratified
decision). 1,358 B, inside the 1,500 B row budget; the table is contiguous **15..104**, 89 rows.

**A row was appended, so a retirement is owed and NONE QUALIFIES** — the close-out obligation of
[`fork-learnings-retirement-rule-plan.md`](docs/planning/fork-learnings-retirement-rule-plan.md) §6 D3, which
requires naming the rows considered. **#87** (a ceiling that is one half of an identity — this session's own
subject, and the closest candidate) fails criterion (a) because **a printer is not a gate**: `bin/check-overhead`
asserts agreement with an instrument and refuses nothing, so the byte half BL-78 §(1) measured as unguarded is
still unguarded — now by decision rather than by oversight. **#100** (two artifacts answering one question by
opposite mechanisms, held equal only by the test between them) is the row this session's design *followed*;
Test 44 is one instance of that lesson, not a general enforcement of it. No row's artifact ceased to exist, and
no later row states either lesson at least as generally, so (b) and (c) are unmet as well.

### 2026-09-28 · [BL-91] S233 — `bin/check-overhead`: the mandated read reported in one line, gating nothing

**P1 of [`docs/planning/overhead-ratchet-plan.md`](docs/planning/overhead-ratchet-plan.md) (`:300`), built under
the shape A ratified earlier today.** A canonical-only printer — not in `bin/_manifest.py`, so no adopter
receives it — reporting the `read-set` class total in both units on one line, exit 0, writing nothing:

```
read-set: 72,535 B ~= 25,904 tok (2 files) at 2.8000 B/token (config) | declared 56,750 B, over by 15,785 B (+27.8%)
```

**Exit 0 means MEASURED, not within budget**, and the tool's own docstring says so: there is no threshold
behind it, because D1 = A declined one. It prints both units because D2 (the unit) is unratified, and names the
density and its source, since a token figure without its density is not a measurement. It deliberately does
**not** compare tokens to the declared token ceilings — those are derived at the 2.27 B/token floor while the
measurement uses each file's resolved density (2.8, config), so that line would compare two differently
denominated numbers. The byte comparison is bound-to-bound and is the one printed.

**It reimplements three lines of arithmetic rather than importing `starter-kit/context_budget.py`**, for the
two reasons P1 gives: that tool emits `class_totals` as a *list*, so an extractor would depend on key order to
avoid reading the `resident` row, and it appends to the tracked `.context-budget-history.jsonl` when a
measurement moves. Writing nothing is therefore true by construction. The price is drift, and the guard against
drift is **`bin/tests.sh` Test 44**, added RED-first: 12 assertions — one line, exit 0, determinism, no tracked
change and no history append across two runs, both figures equal to `context_budget.py --json`'s own output,
an unknown argument refused rather than ignored (BL-75's defect class), and a **kill control** that flips the
class constant on a copy and confirms the equality can fail. RED before the tool existed: **349 passed, 1
failed**, the failure being the missing tool; GREEN after: **361 passed, 0 failed, 0 skipped** (361 rather than
355 because a claim is open, so Test 34's six whole-ledger assertions run — fork Learning #70: do not tighten
`tests-sh-passed`).

**Nothing distributed, nothing upstream, no `.quality-gates.json` entry** (§7 P2 is out of scope), and nothing
in `starter-kit/context_budget.py` or `.githooks/` (§8 dragon 6). **Where the number gets published is still
open** — shape A's second half, *"publish the version series somewhere a release must look"*, is D3 and
unratified; a printer nobody runs reports nothing.

### 2026-09-28 · [BL-91] S233 — D1 ratified: shape A, *report better, gate nothing*

**The operator took D1 as (a) at S233's Phase 0 picker, declining the plan's own recommendation.** Shape B —
one `direction: max` entry in this repository's `.quality-gates.json` on the read-set class total — is **not
taken**, so [`docs/planning/overhead-ratchet-plan.md`](docs/planning/overhead-ratchet-plan.md) §7's **P2 is out
of scope rather than deferred**, and **nothing in this repository will refuse a growth of the mandated read
set.** Shape C, distributed enforcement, was declined a second time: standing decision **S3** — his S206
declination of the hook shape (BL-78 P3) — stays closed, and §1's rule that it may not be re-proposed without
him reopening it stands.

**What the decision was taken against, recorded because it was not taken in ignorance of it.** §4 F5 measures
that a truthful report was *necessary and not sufficient* for five months, and §5 says shape A **catches
nothing** by construction. The plan's recommendation and its *"Why B and not A"* are left standing in the
document rather than rewritten, because they are part of the record the choice was made against.

**What survives, and one dependency it half-discharges.** §7's **P1, the printer**, is S233's deliverable: a
canonical-only `bin/check-overhead` reporting the read-set class total in bytes and tokens, write-free. It is
§5's *"or its fork-side equivalent"* for shape A's number, so the dependency on unreviewed PR #86 is
discharged **for the number only** — the distributed tool's headline still contradicts its own table
(§8 dragon 5, BL-80, [PR #86](https://github.com/KJ5HST/methodology/pull/86)). A printer beside a wrong
sentence does not correct the sentence. Recorded in the plan §6, and in BL-91's index row and detail body.
**D2–D6 remain unratified**, though P1 answers D2's unit question in passing by printing both units.

### 2026-09-28 · [BL-91] S233 claim — the read-set overhead printer, under shape A (in progress)

**The governing decision is taken: the operator ratified D1 = shape A, *report better, gate nothing*,**
at this session's Phase 0 picker, and chose P1 — the printer — as the deliverable
([`docs/planning/overhead-ratchet-plan.md`](docs/planning/overhead-ratchet-plan.md) §6 D1, §7 P1 at `:287`).
He declined (b) the canonical-only `max` gate the plan recommended, (c) distributed enforcement — standing
decision **S3**, his S206 declination of the hook shape, stays closed — and (d) nothing-yet. **P2's
`.quality-gates.json` entry is therefore out of scope**; the plan's §7 phases were written *"if D1(b) is
ratified"*, and under A the printer reports rather than gates.

Deliverable: a canonical-only `bin/check-overhead` printing one line with the read-set class total in bytes
and tokens, exit 0, **writing nothing**, plus a RED-first test in `bin/tests.sh`. Fork-side throughout — no
branch, no pull request, nothing on `KJ5HST/methodology`, and nothing in `starter-kit/context_budget.py` or
`.githooks/` (§8 dragon 6). Close-out records the rest.

### 2026-09-28 · [ad hoc] S232 — the receipt stops writing a `CHANGELOG.md` size and names the command instead

**Second instance of the same defect in one session, and the fix generalises rather than patching.** The
receipt's `next_steps` (7) said *"`CHANGELOG.md` is ~181 KB"*; the committed file reads **191,753 B**. A
size written into a receipt is measured **before** the close-out and push-record commits that follow it,
so it is stale **by construction** — S231's was 18 KB out by the time the next session read it, and this
one was 10 KB out before its own session ended. The line now carries `wc -c CHANGELOG.md` and the 262,144 B
refusal instead of a number. This is the rule the ledger's own header already states about itself
(*"No population figure is written here, deliberately… Run the tool"*), applied to the receipt.

The first instance was the plan's line count, corrected in `674c6a8` — measured before three citation
edits added two lines. Both are logged rather than quietly fixed, and the receipt's gotcha (3) names the
pattern: **measure last, or you have measured a draft.**

### 2026-09-28 · [ad hoc] The close-out fork push, `e5bfca4..37774a5` — and its own record

Seven commits to fork `origin` on the go-ahead granted in advance at this session's Phase 0 picker: the
claim, the retention trim and its fold, the depth ratification, the deliverable, fork Learning #103 with
the line-count correction, and the close-out receipt. Read back with `git ls-remote` and `git rev-list
--count --left-right`: `origin/main` = local `main` = `37774a5`, **0/0**, working tree clean.
`upstream/main` untouched at `6b29d3d`; **nothing reached `KJ5HST/methodology`.** This entry records its
own commit, which goes up under the standing CHANGELOG-only push-record grant.

### 2026-09-28 · [BL-91] S232 close-out — the handoff receipt

Phase 3A–3F. `status: complete`, **self 8, predecessor 8**. S231's receipt scored 8: its
*"re-run them, do not quote this paragraph"* instruction is what made this plan's evidence base sound,
and its gotcha about the stale `.quality-gates-results.json` meant the citation was re-run rather than
compared. Against that, one forecast contradicted itself inside the same paragraph (*"expect `-7`"* then
*"expect `-6`"*; the truth was `-7`), and **neither the receipt nor BL-91 engaged BL-78 or BL-83** — the
items recording that the overhead instrument *exists but is unwired* and that two earlier sessions had
already claimed it did not exist. An executor trusting the item's framing would have proposed building
what already ships, for the third time. One grep of `BACKLOG-DETAIL.md` found it.

Self 8: the backlog grep, the instrument audit that caught a 4x error in a headline ratio before it was
published, fifteen cited source lines opened and three tightened, and every number re-derived rather
than quoted. Docked for a Phase 1B stub written with placeholder scores that `check-handoff` rejected —
the precedent stub three receipts above showed the right shape — and for publishing a line count that
this session's own later edits invalidated.

**Verified in a `--no-local` clone at `674c6a8`:** `bin/tests.sh` **343 passed / 0 failed / 6 skipped**
and `quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results 2f8fe36c7a92 · manifest 01a4ae7aa511`,
both exit 0, both hashes unmoved — correct, since only documents changed.

### 2026-09-28 · [ad hoc] S232 Phase 3C — fork Learning #103, and no retirement

**Appended:** `git log -- <path>` simplifies history and drops commits from the walk, so a per-commit
classification of a file's past is computed on a denominator that silently excluded them, and what comes
out wrong is the **ratio**. The default walk saw 68 commits and put the merge share of read-set growth
bytes at 2.6%; `--full-history` saw 124 and put it at 9.9%. Sibling of #102 with a different mechanism —
#102 is `-S` not *diffing* a merge, #103 is the walk not *containing* it — so the remedy is
`--full-history`, not `--diff-merges=first-parent`. 1,431 B against the 1,500 B row budget; table
contiguous 15..103, 88 rows.

**PHASE 3C RETIRED NOTHING, DELIBERATELY, AND THE ROWS CONSIDERED ARE NAMED** (the D3 obligation, which is
discharged by a reasoned refusal exactly as by a retirement). **#87** — a ceiling that is one half of an
identity — is the closest, and it is the session's own subject: its token half *is* now enforced, by
`TestThisRepoReadSetPartition` (`tools/test_context_budget.py:1258`) under gate
`context-budget-unit-tests`, but BL-78 §(1) measured that the **byte** half has no guard at all, so
criterion (a) is half satisfied and no more. **#88** (an instrument that records every run changes its own
output) is confirmed again by this session's `growth_run` finding, not superseded, and no gate enforces it.
**#99** (a defect's "shapes, none costed" list is one session's imagination) was confirmed the same way —
BL-78 listed three shapes and this plan's recommended option is a fourth none of them named. **#86** and
**#102** are each adjacent with no gate behind them. **#85 was already retired** at S225 under D1(b) and
is a reserved gap. None satisfies (a) a gate now enforces it, (b) a later row states it at least as
generally, or (c) the artifact is gone.

### 2026-09-28 · [ad hoc] S232 — the plan's published line count corrected, 374 -> 376

Two records said **374 lines** because the count was taken before three citation edits added two lines to
the same file — a number published and then invalidated by its own author, in a repository whose ledger
header carries three separate warnings about exactly this. Corrected in `CHANGELOG.md` and
`docs/planning/BACKLOG-DETAIL.md`; `wc -l` re-run against the committed file. Recorded rather than quietly
fixed, because the interesting part is the ordering: measure last, or the measurement is of a draft.

### 2026-09-28 · [BL-91] S232 — the overhead ratchet, planned

[`docs/planning/overhead-ratchet-plan.md`](docs/planning/overhead-ratchet-plan.md), 376 lines, the
session's one deliverable. **Nothing is ratified and nothing is implemented** — §6 carries six
decisions, D1 governing with four options, and the plan recommends **(b)**: one entry in this
repository's own `.quality-gates.json`, `direction: max` on the read-set class total, declared at the
measured value so it can only ever come down. **Fork-side throughout: no branch, no pull request,
nothing on `KJ5HST/methodology`.**

**The finding that reshaped the answer: the overhead gate is not missing.** `context_budget.py
--precommit` already refuses a staged growth and passes a shrink (`starter-kit/context_budget.py:1000`,
byte refusal `:1038`), has no `--force`, and exits **2** on this tree every run — and nothing in this
repository's gate chain calls it. That was already found and closed as **BL-78**, whose hook-enforcement
phase the **operator declined at S206**. The plan does not re-propose it: option (b) touches no
distributed file, because `.quality-gates.json` is a SEED (`bin/_manifest.py:62`) whose shipped `gates`
array is empty, and `quality_ratchet.py --run` measures the **resulting tree** once per session rather
than each commit, so it is indifferent to how bytes arrived — the precise objection that killed the hook
shape. §1 tabulates all four binding decisions with their scopes, because S206 is the one a reader will
misremember as wider than it is.

**Two of BL-91's own framings did not survive re-derivation, and the instrument audit is why.**
*"A hook would have caught none of it"* is true of a 3-event window and false of the population: across
the read-set pair's whole history the merge share of growth bytes is **2.6%** by the default walk and
**9.9%** by `--full-history`, which walks **124** commits where the default walks **68** — `git log --
<path>` prunes merges, the hazard BL-78 itself warned of. **90–97% of the growth arrived in ordinary
commits a hook would have refused.** And *"nothing was looking"* is not quite it: the tool's headline is
hardcoded to print *"Nothing is over a ceiling yet"* (`:652-653`) while four rows read `over` — BL-80,
PR #86's subject — so the instrument was reporting and being read past.

**Also measured:** the read-set ceiling is a partition (`41,364 + 15,386 = 56,750` = 25,000 tok x 2.27
exactly), which is the argument for gating the total and leaves the S201/S205/S202 reported-series
decisions untouched; the series re-run at all 27 tags is monotone non-decreasing, 17,615 B -> 80,526 B;
and the S130 extraction, the one lever that has ever worked, **has never been aimed at
`SAFEGUARDS.md`** — since v3.7 the runner is −9,734 B while `SAFEGUARDS.md` is +1,743 B, the only
read-set file above its v3.7 size. BL-60 stays separate: it is the written record, not the read one.
BL-91's index row and detail body now point at the plan and carry both corrections.

### 2026-09-28 · [ad hoc] The `HANDOFFS.md` retention depth is settled at TWO — operator decision, S232 Phase 0

S231's receipt left one thing explicitly open and called it the operator's: the front matter said
*"keep ONE receipt"* and printed `--cut 1 --force`, while **S229, S230 and S231 each ran `--cut 2`
and kept two.** Three sessions' practice and the written policy disagreed by one receipt and nobody
had settled which was meant. **Ratified at this session's Phase 0 picker: N=2**, replacing the N=1
the operator set at S172 (2026-09-16), which had itself replaced S127's N=4. Both prior decisions
keep their attribution — this is a supersession, not a rewrite.

**It settles a contradiction rather than changing behaviour, and the arithmetic is unaffected.**
BL-59's measurement still stands (the handoff is done by the newest receipt alone), so the second
receipt is a spare rather than a working set; depth and trigger stay separate, and the trigger is
still *above 2* because it sits one above the depth (BL-60). **`RETENTION_FLOOR = 3` in
`bin/check-handoff` is that TRIGGER, not this depth** — it is untouched, and its A1 fit
(3 x 12 KiB + 7,168 <= 65,536 B) still holds. The front matter now says so explicitly, along with
why `tests-sh-passed` measures **343 at rest and 349 mid-claim**: the steady state is two receipts
between claims and three during one, so Test 34's six whole-ledger assertions run only inside the
claim window. Front matter 4,198 -> 4,837 B against the fixed 7,168 B reserve (Test 39 A2), 2,331 B
of headroom left.

### 2026-09-28 · [ad hoc] S232 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

The trimmer's ~448 B pointer block for `HANDOFFS-through-2026-09-27-7.md` became one row at the
bottom of [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md) (data rows **68 → 69**,
counted not written) and was deleted from the ledger's front matter, so the trim-and-fold pair leaves
that fixed 7,168 B header reserve no larger than it found it. **In its own commit, as the index's
fold rule requires:** inside the trim commit the shipped `.verify.sh` fails L2 (fork Learning #58) —
and the proof did pass, exit 0, run from a `--no-local` clone at the trim commit `c8168a2` itself.

### 2026-09-28 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-27-7.md` (1 record(s), 31,168 B → 21,820 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-27 → 2026-09-27) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-27-7.md`](docs/archive/HANDOFFS-through-2026-09-27-7.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-27-7.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-27-7.md.verify.sh)
rather than trusting a digest printed here. Live file 31,168 B → 21,820 B (−30.0%).

### 2026-09-28 · [BL-91] S232 claim — plan the gate on the framework's own overhead (in progress)

Phase 1B. This entry and a `status: pending` receipt in [`HANDOFFS.md`](HANDOFFS.md) are the crash
breadcrumbs. **Deliverable:** one planning document settling what BL-91 leaves open — whether the
per-session mandated read becomes a gated metric with a declared ceiling or stays a reported series,
in what unit, canonical-only or distributed, which reduction levers to cost, and how **BL-60** folds
in. The plan is the deliverable; nothing is implemented (FM #18). Phase 0 found `main` clean at
`e5bfca4`, both ledger frontiers at HEAD with **no gap**, 0 upstream issues, #83–#88 open with **0
reviews** and no comments but our own two, the dashboard at **76/100** with 0 high+ risks, and the
newest receipt's gate citation reproduced exactly in a `--no-local` clone — `quality_ratchet: 11/11
pass · 0 fail · 0 unmeasured · results 2f8fe36c7a92 · manifest 01a4ae7aa511`. `context_budget.py
--status` independently corroborates the item's central figure: read-set **72,535 B** against a
56,750 B ceiling, on a **172-measurement non-shrinking growth run**.

### 2026-09-28 · [ad hoc] The fork push, `c11dbb8..e5bfca4` — and the two decisions settled at the same Phase 0

Pushed to fork `origin` on the operator's go-ahead: S231's four post-close-out commits — BL-91's
three measurement scripts (`f94a507`), the BL-91 backlog item (`3c8f498`), and the two receipt edits
(`03b1234`, `e5bfca4`). None is a CHANGELOG-only push record, so the standing grant did not cover
them and each needed the ask. Read back with `git ls-remote`: `origin/main` = local `main` =
`e5bfca4`, 0/0. `upstream/main` untouched at `6b29d3d`; nothing reached `KJ5HST/methodology`.
**Two decisions were settled at that same Phase 0 picker.** The `HANDOFFS.md` retention depth is
**TWO receipts**, resolving the contradiction S231 left open between the front matter's *"keep ONE
receipt"* and what S229, S230 and S231 each actually did — the front matter is corrected in the trim
that follows, so the written policy and the practice stop disagreeing. And a close-out push is
granted in advance rather than asked again at the end. This entry records its own commit.

### 2026-09-28 · [ad hoc] S231 — the post-close-out tree verified and cited in the receipt

`bin/tests.sh` **343 passed / 0 failed / 6 skipped** and `quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured ·
results 2f8fe36c7a92 · manifest 01a4ae7aa511`, both exit 0, in a `--no-local` clone at `03b1234` — the tree carrying
BL-91's three preparation commits. Both hashes are unmoved from the earlier run at `16ffb0f`, which is correct: only
documents changed. The receipt's `runtime_smoke` now cites this run rather than leaving the preparation commits
unverified, and BL-64's exception narrows to the commit writing that line.

### 2026-09-28 · [ad hoc] S231 — the receipt re-pointed at BL-91 after the operator changed what comes next

`next_steps` (0) said BL-60's planning session was next, which the operator superseded the same day. The receipt now
carries **(0b)**: the next session is the **BL-91 planning session**, with the version series, the dollar floor, what
was *not* measurable, and the pointer to the three committed scripts — so the next session's Phase 0 finds the task
and its evidence in the file it already reads, not in a conversation it cannot see. A new **(6b)** records that all of
this work happened after close-out under no claim.

### 2026-09-28 · [BL-91] Raised, and the operator commissions a planning session as the NEXT SESSION

**BL-91 — the framework's own overhead has risen 4.6x across 27 releases with nothing watching it.**
[Detail](docs/planning/BACKLOG-DETAIL.md#bl-91) carries the per-version table, the dollar conversion
($1.41/session at v1.0.0 → $6.46 at v3.7, the READ floor only), and the wider cost context.

**The structural finding it exists for:** this repository ships a **quality ratchet that can only tighten**
and has **no ratchet at all on its own overhead**. `.context-budget.json` measures the read set, but by the
S202 decision its ceiling is a **reported series, not a limit** — so five months of monotone growth passed
every gate the framework has, because none of them was looking. Whether a given enhancement bought more than
it cost cannot be answered retroactively; it can only be made answerable going forward, which is what the
plan is for.

**The operator's decision, taken 2026-09-28 in conversation: the next session is a PLANNING session on this
item.** It **displaces BL-60's planning session**, chosen earlier the same day — and folds it in as a
question rather than dropping it, since the trim-proof pile (11.1% of the tracked repository) is the same
question asked of the written record instead of the read one. Nothing about BL-91 is decided: the plan's own
§6 will carry the decisions, and any distributed gate it proposes is an upstream pull request and its own
go-ahead.

### 2026-09-28 · [ad hoc] S231 post-close-out — the overhead measurements, and the three scripts that reproduce them

Taken after S231's close-out, answering the operator's questions about Claude API cost against productive
results. **Committed as scripts, not as numbers**, under
[`docs/planning/bl91-overhead-measurement/`](docs/planning/bl91-overhead-measurement/), each with its limits in
its own docstring — the precedent is `pr80-f2-mutants.py` and `pr83-union-repro.py`:

- **`cost-per-project.py`** — prices the 2.7 GB of local Claude Code transcripts (they carry per-request
  `usage` and the model id) at published list rates: **$20,258 across all projects**, this repository the
  largest single consumer at **$7,205 (36%)**, $218/day against $52–176/day for the six code repos; median
  **$55 per methodology session**, 364 requests, ~198,000 tokens of average context. **57% of spend is
  re-sent context, 18% output** — cost tracks turns × context, not bytes written.
- **`process-vs-work-per-session.py`** — process share of lines written: **69% here, 30–62% in the code
  repos**; $195 per 1,000 product lines here against $39–132 there.
- **`mandated-load-per-version.py`** — the series that answers the operator's question, and the only one
  recoverable at every version: **17,615 B at v1.0.0 → 80,526 B at v3.7, 4.6x, never once falling across 27
  releases**; HEAD is 72,535 B, 9.9% below v3.7 after the apparatus extraction.

**What could NOT be measured, stated because the operator suspected it:** observed dollars per methodology
version. The transcripts begin 2026-08-16 and v3.7 shipped 2026-08-12, so all cost data sits inside one
version, on one model, across different work. No slicing of it yields a version comparison, and the mandated-load
series above is a driver, not an observation of spend.

### 2026-09-27 · [ad hoc] Fork `main` pushed to `origin`, `f467176..2feeb5d` — and this record with it

**The operator's go-ahead, asked for because the commit touches `HANDOFFS.md` and so falls outside the standing
CHANGELOG-only grant.** One commit: the S231 receipt corrected for the post-close-out actions it would otherwise
misreport. Read back with `git ls-remote origin refs/heads/main`. **Fork `origin` only; nothing on
`KJ5HST/methodology`.** **This entry rides the push it describes** under the standing push-record grant.

### 2026-09-27 · [ad hoc] S231 — the receipt updated for the post-close-out actions it would otherwise misreport

The S231 receipt was written before the close-out picker was answered, so it said the trim was *owed and blocked*
and four commits were *unpushed* — both false within the hour. Its `next_steps` now open with what actually
happened, in order: D1 ratified as Option C, the trim run and folded, both pushes read back, the overhead
measurement, and **BL-60's planning session as the operator's choice for the next session**. The receipt's own
history of the `--cut` correction is kept rather than smoothed away.

### 2026-09-27 · [ad hoc] Fork `main` pushed to `origin`, `ce0ea45..c51c858` — and this record with it

**The operator's explicit go-ahead, asked for and given after S231's close-out** — **6** commits: D1's
ratification, the `--cut` correction, the `HANDOFFS.md` retention trim to `-6`, its fold into the shard index,
and BL-60's re-measurement. **Pushed because a trim had advanced the frontier locally:** until this push the
frozen shard `docs/archive/HANDOFFS-through-2026-09-27-6.md` and the receipt it holds existed on one machine
only. Read back with `git ls-remote origin refs/heads/main` → `c51c858`. **Fork `origin` only; nothing was sent
to `KJ5HST/methodology`**, where six pull requests remain open with 0 reviews and nothing is owed. **This entry
rides the push it describes** under the standing push-record grant.

### 2026-09-27 · [BL-60] S231 — the overhead question, measured: the read side is flat, the archive is 76% of the growth

**Asked by the operator mid-session** (*"I am concerned that the overhead associated with using methodology is
growing. Estimate overhead growth."*). Measured over the **32 claim commits S201..S231** (2026-09-20 → 2026-09-27),
bucketing every commit into the session whose claim precedes it:

- **What a session must READ is FLAT, slightly down:** the Phase 0 corpus (`SESSION_RUNNER.md` + `SAFEGUARDS.md` +
  `CLAUDE.md` + `BACKLOG.md` + `HANDOFFS.md`) went **161,197 B → 150,492 B**, slope **−438 B per session**. The
  runner and `SAFEGUARDS.md` did not change by a byte; `BACKLOG.md` fell 13,601 B at the S223 split.
- **What a session LEAVES BEHIND is growing:** tracked bytes **10,017,304 → 11,711,011**, **+55,318 B per session**
  (~215 KB/day at ~3.9 sessions/day). **+23,900 B/session is frozen shards and +17,952 B/session is losslessness
  proofs — together 76% of it.**
- **Per session, median:** 7 commits, ~600 lines into ledgers, **20–45 lines of deliverable**; ledger share of lines
  written 97% (S201–S211) and 92% (S221–S231) — high, roughly flat, not accelerating.
- **The repository at `3c793bf` is 72% process record** — shards 39.4%, plans 14.4%, proofs 11.3%, backlog 3.6%,
  live ledgers 2.5%, learnings 1.1% — against 14.7% tools and tests and 5.6% framework prose.
- **Not instrumented at all:** wall-clock and token cost per session. The byte series above are proxies and are
  labelled as such; building a real instrument is its own costed decision.

**[BL-60](docs/planning/BACKLOG-DETAIL.md#bl-60)'s own figure re-measured and recorded in the item: 31 proofs /
453,689 B / 5.4% when raised, **84 / 1,302,320 B / 11.1%** today.** **The operator chose BL-60's planning session
as the next overhead step** (S231 picker) — the three shapes costed, BL-36 folded in. Method limits stated with the
numbers: the series starts at S201 because `S<N> claim` is a recent commit-subject convention, and one bogus
559-commit bucket between S124 and S201 was discarded rather than reported.

### 2026-09-27 · [ad hoc] S231 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

The `-6` trim's three-line pointer block moved out of `HANDOFFS.md`'s front matter and into
[`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md) as one row (**67 → 68**), per that file's own
fold rule. **Its own commit, as the rule requires:** inside the trim commit the shipped `.verify.sh` fails L2
(fork Learning #58). The shard and its proof are untouched.

### 2026-09-27 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-27-6.md` (1 record(s), 35,783 B → 25,287 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-27 → 2026-09-27) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-27-6.md`](docs/archive/HANDOFFS-through-2026-09-27-6.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-27-6.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-27-6.md.verify.sh)
rather than trusting a digest printed here. Live file 35,783 B → 25,287 B (−29.3%).

### 2026-09-27 · [ad hoc] S231 correction — `--cut N` means KEEP N, so the close-out's "wrong flag" finding was itself wrong

**The pushed close-out entry below says S229's and S230's `--cut 2 --force` forecast used the wrong flag, citing
the front matter's `--cut 1 --force` and S230's one-record trim. That reasoning is false.** `--cut N` is a cut
*point*, not a count of records to archive: measured on this tree at three receipts, `--cut 1` reports *would
archive **2** of 3* and `--cut 2` reports *would archive **1** of 3*. S230 moved one record **because** it passed
`--cut 2`. Both predecessors' forecasts were correct and the accusation is withdrawn; the S231 receipt is
corrected in place and the pushed entry stands as written, corrected by this one.

**What the measurement DID surface is a real, unsettled disagreement about DEPTH.** The `HANDOFFS.md` front matter
states *"keep ONE receipt, trim above TWO"* and prints `--cut 1 --force`; S229, S230 and S231 have each kept
**two**. One receipt or two is an operator question — the S172 decision that set N=1 is quoted in that front
matter — and no session has put it. **This session trimmed at `--cut 2`, the depth its own go-ahead described,
and raises the discrepancy rather than resolving it unasked.**

### 2026-09-27 · [BL-88] S231 — the operator ratifies D1 as Option C: the small pull request first, the stack held

Taken at S231's close-out picker, after the routing plan was written and read back.
[`dashboard-upstream-routing-plan.md`](docs/planning/dashboard-upstream-routing-plan.md)'s status now records it:
**P1 — the root-commit-date correctness pull request — is the next upstream-facing step**, re-derived on a branch
off `upstream/main` (a fork-side fix is not an upstream patch); the read-cap/trim stack that BL-88 rides is built
and vetted fork-side and **held until P1 merges**; F2's signature structure, F3's scoped `--sync` and F4's
self-scan stay out of both. **D2–D6 remain open and none blocks P1. Ratifying the shape is not authorising an
open** — P1's pull request is still its own go-ahead, and so is P3's.

### 2026-09-27 · [ad hoc] Fork `main` pushed to `origin`, `0aeeec1..c3c52a3` — and this record with it

**The operator's explicit go-ahead, asked for in S231's close-out picker and granted there** — **4** commits
(the claim, the routing plan, fork Learning #102, the close-out), beyond the standing CHANGELOG-only grant, which
is why it was asked. Read back with `git ls-remote origin refs/heads/main` → `c3c52a3`, and `origin/main...main`
is 0/0. **Fork `origin` only; nothing was sent to `KJ5HST/methodology`.** **Pushed BEFORE the owed `HANDOFFS.md`
trim, deliberately:** a trim rewrites the file a later reader reconstructs from, so the record of what exists goes
out before the frontier advances. **This entry rides the push it describes** under the standing push-record grant.

### 2026-09-27 · [BL-88] S231 close-out — the route is planned and unratified; the owed `HANDOFFS.md` trim was BLOCKED, not skipped; predecessor scored 9

**Deliverable:** [`docs/planning/dashboard-upstream-routing-plan.md`](docs/planning/dashboard-upstream-routing-plan.md)
(`3aa95f7`), **awaiting the operator's ratification.** Fork-side throughout — no branch, no pull request, nothing on
`KJ5HST/methodology`, where six pull requests still sit open with 0 reviews and nothing is owed.

**Two things this close-out records that are not the deliverable.**

1. **The owed `HANDOFFS.md` retention trim did not run.** The claim made three receipts, so the trim was owed the
   moment it landed; `methodology_trim.py --file HANDOFFS.md --cut 1 --force` was **denied by the harness's
   permission classifier as a dry run**, and no route around it was attempted. The ledger therefore closes at
   **three receipts**, `tests-sh-passed` reads **349** rather than 343, and the trim is the next session's first
   housekeeping act — with `--cut 1`, not the `--cut 2` that S229's and S230's receipts both forecast (the front
   matter and S230's own trim `440183b`, one record, are the authorities). Expect shard `-6`.
2. **Phase 3C appended fork Learning #102 and retired nothing**, naming in the receipt the five rows considered
   (#68, #83, #94, #51, #100) and why none meets the retirement criteria — the D3 obligation discharged by an
   explicit refusal.

**Self 8, predecessor 9.** S230's next_steps (1) was a measured negative result — *P4 has no target*, with the
greps that showed it — and re-running them confirmed every figure, which is what made this session's task
well-formed rather than exploratory. Its one defect is the `--cut 2` forecast above, inherited from S229. Against
this session: an AST set-difference reported **3** fork-only risk rows where reading all 63 appends shows **5**,
and a cited line pair (`:2287`/`:2298`) was wrong and was corrected to `:2319`/`:2320` before the plan was
committed — both caught before publication, neither by the instrument that produced them.

**Gates at `16ffb0f`, in a `--no-local` clone:** `bin/tests.sh` **349 passed / 0 failed / 0 skipped**, exit 0;
`quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results cb3637962fde · manifest 01a4ae7aa511`, exit 0.

### 2026-09-27 · [ad hoc] S231 Phase 3C — fork Learning #102: a `-S` inventory cannot see a merge commit

Appended to [`docs/FORK_LEARNINGS.md`](docs/FORK_LEARNINGS.md) (rows **15..102**, 87 rows, 0 over the 1,500 B
per-row budget). The lesson is this session's own near-miss: a symbol-by-symbol `git log -S` sweep attributed 40 of
42 fork-only scanner names to ordinary commits and returned *nothing in range* for two, both of which are real and
shipped — written **inside** the resync merges `8b87086` and `421ebf9` as the conflict resolutions themselves, and
findable only with `--diff-merges=first-parent`. A route planned around cherry-picks would have carried neither and
would have looked complete by its own method.

**No row was retired, and the rows considered are named in the S231 receipt's `what_was_done`** — the D3 obligation
in [`fork-learnings-retirement-rule-plan.md`](docs/planning/fork-learnings-retirement-rule-plan.md) §6 is discharged
by the explicit refusal, not by silence.

### 2026-09-27 · [BL-88] S231 — the dashboard's upstream route, planned: one dependency stack plus four detachable pieces

**Deliverable:** [`docs/planning/dashboard-upstream-routing-plan.md`](docs/planning/dashboard-upstream-routing-plan.md)
(376 lines), the routing document S230's next_steps (1) said the operator would have to commission. **Fork-side;
nothing was opened, no branch was cut, and every pull request it names is its own go-ahead.** Ratification pending:
§6 carries six decisions, D1 (campaign shape) governing.

**The inventory** (`SESSION_RUNNER.md` §Planning Sessions' mandatory step) was taken symbol-by-symbol from the two
trees — `upstream/main` `6b29d3d` against fork `main` `0aeeec1` — not from the commit list: **42 fork-only top-level
names, 1 upstream-only, 15 shared-but-different, 5 fork-only risk rows, 10 fork-only test classes (123 tests)**.
Upstream's suite is **226 tests, OK, exit 0** in a `--no-local` clone, against the fork's 350.

**What the inventory changed about the answer.** The read-cap work and the trim-trigger row are **one dependency
stack, not two features** — `collect_trim_metrics` reads `read_cap_watch` and calls `read_cap_class()`
(`tools/methodology_dashboard.py:2319`, `:2320`) while BL-88's own P2 calls `find_trim_tool()` — so they cannot be
sent separately. Four pieces detach; one of them **exists only inside merge commits** (`8b87086`, `421ebf9`) and so
can never be cherry-picked; one is a **live defect in the maintainer's shipped tool** (`first_commit_date` reads the
NEWEST commit, 13 lines, 5 tests) and depends on nothing; two are policy changes rather than fixes. Three things
that looked divergent are not — `LANG_MAP`, `detect_doc_only` and `FRAMEWORK_ITEMS` differ **in comments only**.

**No open pull request touches either scanner copy or its test file** (`gh api …/pulls/<N>/files`, all six); the
shared paths are `CHANGELOG.md`, `.quality-gates.json` (#85–#87), `bin/tests.sh` (#84, #86, #87) and
`bin/_manifest.py` (#84). BL-88's index row and detail now point at this plan instead of at a P4 with no target.

### 2026-09-27 · [BL-88] S231 claim — the upstream routing plan for the fork's dashboard divergence (in progress)

**The operator chose this at S231's Phase 0 task picker**, from S230's next_steps (1): BL-88's P4 was measured to
have **no target** — `upstream/main`'s dashboard is **2.11.1** and none of `READ_CAP_CLASS_A`, `READ_CAP_CLASS_B`,
`read_cap_class`, `find_trim_tool` or `collect_trim_metrics` exists there — so the fork's shipped P1 (`cb9b0ed`)
and P2 (`161181c`) can reach an adopter only inside a pull request that first upstreams the rows they sit on.
That routing decision is the operator's to commission, and this session produces the plan for it.

**This session:** one planning document under `docs/planning/`, following `SESSION_RUNNER.md` §Planning Sessions —
a grep-based inventory of what the two copies of `methodology_dashboard.py` actually differ by (the mandatory step
for a migration plan; the change list comes from the searches, not from recollection), a batching of those
differences into pull-request-sized units with a defended order, each phase's DONE criterion, verification command
and **surface**, and a session boundary per phase. **The plan is the deliverable: no dashboard code is changed, no
branch is cut, no pull request is opened, and nothing is sent to `KJ5HST/methodology`,** where six pull requests
sit open with 0 reviews and nothing is owed.

### 2026-09-27 · [ad hoc] Fork `main` pushed to `origin`, `cf60984..4093485` — and this record with it

**The operator's explicit go-ahead, asked for after S230's close-out report**, for the one commit carrying the §3G
correction (S230's `self_score` 8 → 7, BL-79's third occurrence). **This entry is pushed under the standing push-record
grant** — its only change is this `CHANGELOG.md` entry — so it records its own push. Fork `origin` only; nothing to
`KJ5HST/methodology`.

### 2026-09-27 · [ad hoc] S230 correction — the Phase 3G report was not given as one until the operator asked; self_score 8 → 7

The closing messages carried §3G's content — the deliverable, the self-assessment, the predecessor's score and the
next session — but never its shape: no `Close-out report: S230` heading, no labelled sections, no `Session over.`
line. The operator asked for "phase 3 close-out report", which §3G's *"without being asked"* already counts as the
miss. The S230 receipt's `self_score` goes **8 → 7** with the reason in `what_was_done`; the close-out entry stands
as written and is corrected by this one. **BL-79's third occurrence** is recorded in its
[detail](docs/planning/BACKLOG-DETAIL.md#bl-79): the report was displaced by the close-out's own go-aheads, whose
actions changed the state it described.

### 2026-09-27 · [ad hoc] Fork `main` pushed to `origin`, `dc791ae..3582cc6` — and this record with it

**The operator's explicit go-ahead, asked for after S230's close-out**, for the one commit recording the portfolio
dashboard sync and BL-90's count correction. **This entry is pushed under the standing push-record grant** — its only
change is this `CHANGELOG.md` entry — so it records its own push and no further record is owed. Fork `origin` only;
nothing to `KJ5HST/methodology`.

### 2026-09-27 · [BL-90] S230 — the portfolio dashboard copy synced to 2.19.0, its local `EXCLUDE_DIRS` re-applied; BL-90's "9-name" corrected

**The operator's go-ahead, given at S230's close-out.** `~/Development/methodology_dashboard.py` — outside every
repository, so a scratch backup was taken first — went 2.18.0 → **2.19.0** by `--sync ~/Development`, which
overwrote its `EXCLUDE_DIRS` exactly as [BL-90](docs/planning/BACKLOG-DETAIL.md#bl-90) says; the seven local
names were then re-applied, and `diff` against `starter-kit/methodology_dashboard.py` shows that line alone. That
copy had been pre-P1 — the scanner that emitted BL-88's original false flag. **Per-project copies untouched.**

**Correction:** BL-90's ledger entry below and its commit `e8ea062` call the local list *"9-name"*. It is **13
names, the canonical six plus seven local additions**, measured by a set difference against the canonical module.
Corrected in place in BL-90's body, its index row and the S230 receipt; the pushed entry and commit keep the wrong
figure, and this entry is the record of it.

### 2026-09-27 · [ad hoc] Fork `main` pushed to `origin`, `cfe542a..e8ea062` — and this record with it

**The operator's explicit go-ahead, asked for and given at S230's close-out** — **6** commits, beyond the standing
CHANGELOG-only push grant, which is why it was asked rather than assumed. **Fork `origin` only; nothing was sent to
`KJ5HST/methodology`**, where six pull requests still sit open with 0 reviews and nothing is owed.

**What the range carries:** S230's claim; the `HANDOFFS.md` retention trim to `-5` and its fold; the BL-88 P2
deliverable `161181c` (`DASHBOARD_VERSION` 2.19.0); the close-out; and BL-90 with the receipt correction.

**This entry rides the push it describes**, so the record and the state it records land together. Read back with
`git ls-remote` rather than trusting this sentence.

### 2026-09-27 · [BL-90] S230 — raised after close-out: `--sync` overwrites a copy's local `EXCLUDE_DIRS`; the S230 receipt corrected

Found while dry-running, before offering it, the command 2.19.0's stale-copy warning now prints to the portfolio
copy: `--sync ~/Development --dry-run` reports `update methodology_dashboard.py`, 1 of 1 target, with no word about
that copy's local 9-name `EXCLUDE_DIRS` — the edit point the module's own CUSTOMIZATION section invites. **Recorded
as [BL-90](docs/planning/BACKLOG-DETAIL.md#bl-90), not fixed (FM #17), and nothing was synced.** The S230 receipt's
next_steps (2) had called that command *"the remedy"*; it now says what running it would destroy.

### 2026-09-26 · [ad hoc] The prose update route gets the three rules that stop it overwriting an adopter's ledgers

- **Why:** `starter-kit/BOOTSTRAP.md` §Without `bin/sync` was one sentence — *"It will fetch the latest
  starter-kit files and overlay them"* — and it named no exception. An agent following it literally overlays
  `CHANGELOG.md` and `HANDOFFS.md`, which are seeds: the adopter's action ledger and every close-out receipt
  are replaced with empty templates. A six-adopter acceptance test found this and rated it critical. The
  `bin/sync` route has never had the defect; only the prose route does, and the prose route is the one the
  instruction in that section tells people to use.
- **What is added:** three numbered rules given with the instruction. **(1)** a two-row table splitting the
  distribution into tracked files that are overlaid and adopter-owned files that are never overwritten, with
  the consequence of getting it wrong stated in the sentence after it. **(2)** the hand reconcile the seeds
  need afterwards, pointing at the *Updating an existing project from an earlier methodology version*
  paragraph in §Setup with `bin/sync` rather than restating it, so the two cannot drift apart. **(3)** verify
  with `bin/status` and what its five verdicts mean.
- **The table is derived from `bin/_manifest.py`, not written from memory:** its `DISTRIBUTION` list is what
  classes six files as seeds — `CHANGELOG.md`, `HANDOFFS.md`, `SESSION_NOTES.md`, `ROADMAP.md`,
  `.context-budget.json`, `.quality-gates.json` — and every other entry as tracked.
- **Rule 3's five verdicts are the ones `bin/status` actually prints:** `missing`, `current`,
  `N versions behind`, `locally modified`, and `present (stale format)` — read from the source, not inferred
  from the documentation.
- **Measured:** `bash bin/tests.sh` reports **139 passed, 0 failed** on this branch, unchanged from the commit
  it starts from; `bin/check-links` resolves 107 links; `quality_ratchet.py --run` reports **10/10 pass**. The
  change is prose in one file and no gate moves.

### 2026-09-26 · [ad hoc] The suite's ratchet floor rises to what this branch measures

- **Why:** this branch adds 49 assertions to `bin/tests.sh`, and `.quality-gates.json` still floored
  `tests-sh-passed` at the count from before them. The ratchet therefore protected none of the new tests — a later
  change that silently removed all 49 would still have passed the gate.
- **Measured, not assumed:** `bash bin/tests.sh` reports **139 passed, 0 failed** in a clone of the commit this
  branch starts from and **188 passed, 0 failed** in a clone of its tip. Diffing the two runs' `PASS:` lines names
  49 assertions present only on the branch and **none** of the base's missing from it. The floor becomes 188.
- **Tightening only, and the guard is live:** `quality_ratchet.py --precommit` accepts the change (exit 0) and
  refuses the same line lowered by one (exit 2, *"gate 'tests-sh-passed': floor lowered 139 -> 138"*), so the check
  was exercised on this tree rather than assumed to work. `--run` reports 10/10 pass with the new floor met exactly.
- **A later merge cannot invalidate it:** the gate is a minimum, and every other change in flight adds tests rather
  than removing them. Where another one raises this same line to a lower number, a minimum resolves to the larger.

### 2026-09-22 · [ad hoc] The documents say what the update route now does, and stop requiring the `gh` CLI

- **Why:** two earlier changes on this branch made `--source=github` clone the repository and made `bin/sync`'s
  refusal name a source that has no history to compare against. The prose still described the route as it behaved
  before: it required the `gh` CLI, and it told readers to *prefer* `--source=local` because only a local checkout
  carried the history that recognizes a file as merely behind. Both statements are now false.
- **The `gh` CLI is no longer required, and four documents said it was:** `README.md`'s Option A, the sync block in
  `starter-kit/BOOTSTRAP.md`, and the `--source=github` lines in `docs/tutorials/T1_setup.md` and
  `docs/tutorials/T8_keeping_current.md` now say *needs git and network*. Both `--source` help strings say what
  `github` does — it clones the repository for the run.
- **Either source now carries the history:** `BOOTSTRAP.md`'s *Updating an existing project* paragraph no longer
  prefers `--source=local`. It says both sources carry the history that recognizes a file as merely behind, keeps the
  sentence about a shallow clone or a downloaded tarball, and points that sentence at the refusal that now names it
  rather than reporting it against the reader's files.
- **`README.md`'s Quick Start note** keeps its wording and gains one clause: where to run `bin/sync` from, and that
  either source recognizes an unedited file that is merely behind, so it is updated rather than refused.
- **`BOOTSTRAP.md` troubleshooting** gains the second cause a reader can now meet — a shallow or history-less source —
  beside the *locally modified* entry that was the only one there.
- **Scope:** prose and two help strings only; no behaviour changes. `bin/check-links` OK, 107 links.

### 2026-09-22 · [ad hoc] `bin/sync`: a source without its history is named as the refusal's cause, not the project's files

- **The defect:** `bin/sync` refuses a tracked file that matches neither the canonical version nor any version in
  the source's history, and says it has *local modifications*. That is earned only when the history is complete. From
  a shallow clone or a downloaded tree it said the same of files that were merely behind: a project installed from
  `008d656` and never edited had 9 files refused as local modifications, exit 2, by `bin/sync --source=local
  --dry-run` from a depth-1 clone of this branch and from a `git archive` of it. `starter-kit/BOOTSTRAP.md` already
  says a shallow clone or a tarball loses that history; the refusal did not.
- **The fix:** before refusing, `bin/sync` asks its source what history it has. No `.git`: the refusal says the source
  has no git history and prints the `git clone` command. `git rev-parse --is-shallow-repository` true: it says the
  checkout is shallow and how many commits it holds, and prints `git -C <source> fetch --unshallow`. In both, the
  header says the files *differ from the canonical version*, the `CLAUDE.md` paragraph (which presumes an edit) is
  left out, and the exit stays 2. A source with its full history prints exactly the text it did.
- **The `--source=github` hint:** it printed *"To inspect the drift first:"* over no lines, because its commands would
  have named the clone, which is removed when the run ends. It now prints a clone of the source pinned to the commit
  the run read (`git clone <url> methodology-<sha> && git -C methodology-<sha> checkout -q <sha>`) and one `diff` per
  file against it.
- **Tests, written red first:** Test 29 takes Test 26's fixture three ways — a depth-1 and a depth-2 clone over
  `file://`, and a `git archive` of it — with a project holding the fixture's oldest version, merely behind. Each
  source exits 2, names its cause (with the commit count, 1 and 3), writes nothing, and never says *local
  modifications*; the shallow refusal prints the `fetch --unshallow` command and the tarball's the clone command. For
  `--source=github` the test runs the printed hint after the run, from an empty directory: the clone succeeds and
  `diff` exits 1 on the edit. The control: a full-history source upgrades the same file. Test 7 now also asserts
  that a full-history source still says *local modifications*. On the unfixed script 9 of the 55 checks in Tests 7
  and 26–29 fail, all of them new; the controls pass.
- **Mutants, run:** thirteen — each cause's detection disabled, the cause ignored, each header's wording swapped, the
  github hint's diff aimed at the removed clone, its pin wrong, the hint given the local form or dropped, the
  `fetch --unshallow` path dropped, the commit count hard-coded, its plural forced, and the clone command dropped.
  All thirteen fail at least one check; unmutated, 55 / 0.
- **Live (one run each):** from the `008d656` project, the depth-1 clone and the tarball each refused its 9 files
  with its own cause, exit 2. Against `https://github.com/KJ5HST/methodology.git`, a project with one edited file:
  exit 2 with the full-history text, and the printed hint, run by hand, cloned `6b29d3d` and `diff` showed the edit.
- **Not changed here:** `bin/status` from a history-less source still reads a merely-behind file as *locally
  modified*; the `--help` text and the documents.

### 2026-09-21 · [ad hoc] `bin/sync` and `bin/status`: `--source=github` clones the repository, so a file that is merely behind is recognized

- **The defect:** `--source=github` read each distributed file's contents through the GitHub API and nothing else,
  then classified the project's copy against an empty history. A file that was merely behind matched no known
  version, so `bin/sync` refused it as a *local modification* (exit 2) and `bin/status` read it as *locally
  modified*: the one case an update exists for. On a project installed from `008d656` and never edited, updated
  toward `6b29d3d`, `bin/sync --source=github --dry-run` refused 9 files, exit 2, in 12.3 s (one run). The history
  walk for this source was deferred when the full distribution was added (issue #32), with `--source=local` kept as
  the supported update path.
- **The fix:** `--source=github` makes a full clone of `https://github.com/KJ5HST/methodology.git` into a temporary
  directory, or of `METHODOLOGY_SOURCE_URL` when it is set (anything `git clone` accepts), and runs exactly the
  `--source=local` code over the clone: the same reads, the same full-history walk, the same `git describe`. The
  directory is removed when the run ends, dry run or not. Both scripts, one mechanism. The `gh` calls are gone, so a
  public repository needs neither the GitHub CLI nor authentication; a private mirror uses git's own credentials.
- **What a user sees change:** the source line names the URL cloned (`source:  github (https://…)`), and `version:`
  is the clone's `git describe` (`v3.7-68-g6b29d3d`) rather than `github:<sha>`. A distributed file the source lacks
  (this checkout's manifest is ahead of it) is listed with every other such file before anything is written, exit 1,
  in both scripts; `bin/sync` used to stop at the first one with a `gh auth login` hint.
- **Tests, written red first:** Test 27 serves Test 26's fixture (both merge-hiding shapes) as a `file://` bare
  repository through `METHODOLOGY_SOURCE_URL`, and checks every version the way Test 26 does, through
  `--source=github`: 6 status rows and 5 sync outcomes, a real local edit still refused, plus the source and
  version lines, a dry run that writes nothing, and no temporary clone left behind. Test 28 removes one distributed
  file from the fixture: both scripts name it, exit 1, and nothing is written. On the unfixed scripts the two tests
  fail 16 of their 20 checks; the 4 that pass are the controls. Test 26's fixture moved into a function the two
  share, with its assertions unchanged. Test 9's guard is now the URL's reachability (`git ls-remote`, 30 s timeout)
  instead of `gh auth status`.
- **Mutants, run:** nine — a `--depth 1` clone in each script, the inventory skipped in each, the URL override
  ignored, the temporary clone left behind by each, and the github route given no history in each. Tests 26–28
  fail on all nine and pass unmutated (31 / 0). The two `--depth 1` mutants passed until the fixture was served as
  `file://` rather than a plain path: git ignores `--depth` when it clones a plain path.
- **Live, against this repository (one run):** the same project from `008d656`: `bin/sync --source=github --dry-run`
  exit 0, 10 files would be written, `version: v3.7-68-g6b29d3d`, 1.6 s; `bin/status --source=github` 9 rows
  *N versions behind*, 0 *locally modified*, 1.9 s.
- **Not changed here:** the refusal text for a source that has no history of its own (a shallow clone, a downloaded
  tarball), the *"To inspect the drift first:"* header this route prints over no lines, the `--help` text, and the
  documents that describe the route.

### 2026-09-21 · [ad hoc] `bin/status` and `bin/sync`: the history walks look up blobs in one batched call

- **Why:** the full-history walk the entry below adds visits more than twice the commits the default walk did, and
  both tools ran one `git ls-tree` subprocess per commit. Against six adopter projects, `bin/status` went from 3.0 s
  to 10.1 s and one project's `bin/sync --dry-run` from 2.9 s to 7.5 s.
- **The change:** one `git cat-file --batch-check` per walk, fed `<commit>:<path>` lines: `bin/status`'s new
  `blobs_at()`, used by `history_walk()`, and `bin/sync`'s `local_history_blobs()`. A separate commit from the fix, so
  it can be judged, or dropped, on its own.
- **Behaviour-neutral:** on the fork where it was first measured, `bin/status` output over the six projects was
  byte-identical to the fix's (174 rows), and `bin/sync --dry-run` output identical apart from the `version:` line,
  with the same exit codes. Run time after: `bin/status` 4.0 s, that `bin/sync --dry-run` 2.3 s. Test 26 unchanged.

### 2026-09-21 · [ad hoc] `bin/status` and `bin/sync`: a version a merge hid from git's default walk is recognized again

- **The defect:** both tools listed a file's past versions with a plain `git log -- <path>`, which follows only a
  merge's TREESAME parent. A version on the side a merge did not keep was never visited, so an unmodified copy of it
  read *locally modified* and `bin/sync` refused it (exit 2).
- **The fix:** `bin/sync`'s `local_history_blobs()` walks with `--full-history`; it only asks whether a version is
  known. `bin/status` walks twice, sharing a commit → blob cache: the first-parent line (`--first-parent`) and the
  full history. *N versions behind* counts the distinct versions newer than the project's along the first-parent
  line, and falls back to the full walk for a version that only ever existed on a merged branch.
- **Test 26, written red first:** a methodology repository with both hiding shapes on one tracked file (a merge that
  takes a side branch's content, and one that keeps main's), at fixed commit dates. It proves the shapes (the walks
  visit 4 / 8 / 4 commits), then pins 6 status rows and 3 sync outcomes, including a real local edit that must still
  be refused.
- **Provenance:** made and measured first on a fork of this repository, where running the fixed tools against six
  adopter projects turned 8 misread files from *locally modified* into *N versions behind* and left the 3 genuine
  local edits refused. Carried here with the test renumbered and three comments reworded; the logic is unchanged.

### 2026-09-21 · [ad hoc] `.quality-gates.json`: the same two floors tightened again, to what this branch now measures

- **Action:** `tests-sh-passed` 141 → 142 and `context-budget-unit-tests` 129 → 140. These are the values
  `python3 starter-kit/quality_ratchet.py --run` measures after the two `context_budget.py` changes recorded
  between this entry and the first tightening below, which add 11 unit tests and 1 `bin/tests.sh` row. No other
  floor moves: every other gate measures exactly its threshold. This is a separate commit from the first
  tightening, so either can be dropped alone.
- **Measured** in a fresh clone of the branch before this commit: `10/10 pass · 0 fail · 0 unmeasured`, with
  `tests-sh-passed` 142 and `context-budget-unit-tests` 140.

### 2026-09-21 · [ad hoc] `context_budget.py`: a row over a ceiling stays `over` when a structure pattern also fails

- **Action:** `measure_file()` in `starter-kit/context_budget.py` gave a row the status of whichever check wrote
  last. A ceiling check (bytes, lines, line length, tokens) sets `over`; a structure pattern that matched fewer
  records than its `expect_min` then set `instrument-failed` unconditionally, overwriting it. `render()` ranks
  `instrument-failed` just below `over`, so the headline read `INSTRUMENT-FAILED`, the row read
  `instrument-failed`, and when the growth run fired the advisory said *"Nothing is over a ceiling yet"* directly
  above the finding that said the ceiling was exceeded. That write was the only one in `measure_file()` that could
  lower a status. It now leaves an `over` row as it is, so a check can raise a row's status and never lower it.
  Both findings still print, and the exit code is 2 either way. This is the case the growth-run entry two below
  lists under *Not changed here*.
- **A comment corrected:** the comment above `main()`'s exit said the tool's ordering *"already ranks"* an
  instrument failure *"above `over`"*; `render()`'s ranking puts it just below. The comment now says what the code
  does: a config defect exits 2 exactly as `over` does.
- **Tests, RED first against the unchanged tool** (blob `f75482c2`): 4 in a new `TestStatusPrecedence` class in
  `tools/test_context_budget.py`. (1) The real `main()` → `render()` path under `--status`, on a file over its byte
  ceiling that also fails a pattern, with the growth run fired: the headline reads `OVER`, both findings print,
  the advisory gives the over-state sentence, and the exit is 2. (2) `--status --json` reports that row as `over`.
  (3) A control: a row that only fails its pattern still reads `instrument-failed`. (4) Raising still works: a
  row past its warn line that fails its pattern reads `instrument-failed`. Tests (1) and (2) fail on the old tool;
  (3) and (4) pass on it by design, and the mutants below are what they catch.
- **Mutants, run rather than predicted,** after the fixed tool passed the same harness: the guard removed, so the
  last writer wins again (tests 1 and 2); the guard made to never set the status (tests 3 and 4); raising from
  `warn` blocked (test 4 alone); raising from `ok` blocked (test 3 alone). `--selftest` catches the two that stop
  a pattern-only row reading `instrument-failed`, and neither of the others.
- **Counts:** `tools/test_context_budget.py` 136 → 140 tests, `--selftest` 52 checks unchanged, `bin/tests.sh`
  142 passed, 0 failed (unchanged: no shell row added). No gate threshold changes in this commit.

### 2026-09-21 · [ad hoc] `context_budget.py`: `--check` is a second name for `--status`, and a refused argument is told what it most likely meant

- **Action:** the refusal added below (exit 3 and the usage text) said what was wrong and not what to do instead.
  Searched in this repository and seven adopter projects, the arguments typed after this tool's name that it
  did not define were two: `--status`, which now exists, and `--check`. `--check` is the ledger trimmer's name for its report-only run
  (`methodology_trim.py --check`: *"evaluate the trigger and report; never writes"*), and one adopter project's
  session notes tell the next session to *"Re-measure (`python3 context_budget.py --check`) before writing
  more"*. Now:
  - `--check`, with or without `--json`, is accepted and is the same run as `--status`: the same ledger, the
    same exit code, and no history row. The usage text gains a `--check` line.
  - Every other refused argument gets a line of its own, `unknown argument: <arg>`, followed by what it most
    likely meant, taken from what the sibling tools use the same flag for:
    - `--force` (the trimmer's and the dashboard's override): *"there is deliberately no --force: to permit
      growth, raise that file's ceiling in .context-budget.json"*;
    - `--dry-run` (the dashboard's preview): *"did you mean --status? It measures and writes nothing"*;
    - `--run` and `--write` (the ratchet's and the trimmer's real run): *"run with no argument to measure and
      record"*;
    - a misspelling of an accepted argument: *"did you mean <nearest>?"*, from `difflib.get_close_matches`
      with a cutoff of 0.75;
    - anything else: nothing more.
  - Unchanged: exit 3, nothing read or written, and the usage text after the refusal.
- **The cutoff was measured, not chosen.** At `difflib`'s default of 0.6, `--version` is offered `--json`, which
  is not what anyone typing it meant; at 0.75 it is offered nothing. Both cutoffs send `--stauts`, `status`,
  `--jsn`, `--selftset`, `--calibrat`, `--precomit`, `--chek` and `--hlep` to the intended argument, and neither
  offers anything for `--zzz`, `--verbose` or `-v`. The one loss at 0.75: `install` is no longer offered
  `install-hook`.
- **Where the hint table lives.** It names `--force`, so it sits below the selftest, which refuses that string
  anywhere above its own definition, and hints are looked up by key rather than by testing the argument list for
  a flag, the form `bin/tests.sh` and the unit tests grep for.
- **Tests, RED first against the unchanged tool** (blob `dd4803bf`): 7 new in `TestCommandLine` in
  `tools/test_context_budget.py`, and its frozen accepted set gains `--check`. Six fail on the old tool: the
  `--check` test, the `--force`, preview, misspelling and one-line-each hint tests, and the frozen set. Two pass on
  it by design, because the old tool never suggested anything: `--zzz` and `--version` are offered nothing. The
  mutants below are what those two catch. One row in `bin/tests.sh`: `--check` on the seed config exits as
  `--status` does and writes nothing. It fails on the old tool (exit 3 against 1).
- **Mutants, run rather than predicted,** after the fixed tool passed the same harness: `--check` dropped from
  the write guard (the `--check` test and the shell row); the hint table emptied (the `--force`, preview and
  one-line-each tests); the cutoff at 0.6 (the `--version` test); the suggestion printed unconditionally (the
  `--zzz`, `--version` and one-line-each tests); the hint table moved above the selftest (`--selftest` exits 2 on
  *"--force is not offered"*). `--selftest` catches only the last.
- **Counts:** `tools/test_context_budget.py` 129 → 136 tests, `--selftest` 52 checks unchanged, `bin/tests.sh`
  141 → 142 passed, 0 failed. `VERSION` stays 1.3.0, which this pull request already sets. No gate threshold
  changes in this commit.

### 2026-09-21 · [ad hoc] `.quality-gates.json`: two floors tightened to what this branch measures

- **Action:** `tests-sh-passed` 139 → 141 and `context-budget-unit-tests` 118 → 129. These are the values
  `python3 starter-kit/quality_ratchet.py --run` measures after the two `context_budget.py` changes below,
  which add 11 unit tests and 2 `bin/tests.sh` rows. The manifest says the next tightening is owed whenever a
  measured value rises, and a tightening passes the pre-commit ratchet without approval. No other floor
  moves: every other gate measures exactly its threshold.
- **Measured** in a fresh clone of the branch before this commit: `10/10 pass · 0 fail · 0 unmeasured`, with
  `tests-sh-passed` 141 and `context-budget-unit-tests` 129.

### 2026-09-21 · [ad hoc] `context_budget.py`: the growth-run advisory no longer says nothing is over a ceiling when something is

- **Action:** when the growth run fires, `render()` in `starter-kit/context_budget.py` prints an advisory
  whose second sentence was a literal: *"Nothing is over a ceiling yet — that is the point. Ceilings fire
  late."* It printed in every such run, including runs whose headline read `context budget OVER` above
  a table with rows marked `over`. The sentence is now chosen by `worst`, the variable the headline
  prints, so the two cannot disagree. When nothing is over, the sentence is unchanged, word for word.
  When something is, it reads *"A ceiling has fired as well — see the rows marked over."* No other output
  changes.
- **Tests, RED first against the unchanged tool** (blob `131158cb`): 3 in a new `TestGrowthRunAdvisory`
  class in `tools/test_context_budget.py`. (1) A matrix over every status `render()` ranks (`ok`,
  `unmeasured`, `warn`, `instrument-failed`, `over`), with and without the growth run. It calls
  `render()` in process, checks each cell's headline and advisory first, and asserts the advisory never
  says *"Nothing is over a ceiling"* when the headline says `OVER`. (2) The presence control: every
  status below `over` still prints the original sentence, so deleting it would not pass (1). (3) The
  real `main()` → `render()` path on a project over its resident total, with a growth-run limit of 2 and a
  seeded history. Tests (1) and (3) fail on the old tool, and (2) passes on it by design.
- **Mutants, run rather than predicted,** after the fixed tool passed the same harness: the literal
  restored (tests 1 and 3 fail); the sentence deleted in both states (all 3); the condition inverted (all
  3); the condition widened to `instrument-failed` (test 2). `--selftest` catches none of them, since it
  does not cover the advisory.
- **Not changed here:** a row can be over a ceiling and still read `instrument-failed`. `measure_file()`
  gives a row the status of whichever check wrote last, so a failed structure pattern overwrites a byte
  ceiling's `over`. The headline then reads `INSTRUMENT-FAILED`, and the advisory keeps the original
  sentence above a finding that says the ceiling was exceeded. That is a status-precedence question in
  `measure_file()`, not in the advisory.
- **Counts:** `tools/test_context_budget.py` 126 → 129 tests, `--selftest` 52 checks unchanged, `bin/tests.sh`
  141 passed, 0 failed (unchanged: no shell row added). No gate threshold changes in this commit.

### 2026-09-21 · [ad hoc] `context_budget.py --status` now exists and writes nothing; an unknown argument is refused

- **Action:** `starter-kit/context_budget.py` had no `--status` command and ignored any argument it did
  not recognise, so `--status`, `--check`, `--force` and a typo each ran the default measurement. That run
  appends a row to `.context-budget-history.jsonl` whenever a size changed. `--status` is nonetheless
  cited as a verification step in this repository's own ledgers, and the PR #82 review thread named its
  write as what stands in the way of a `context-budget` gate. Now:
  - `--status`, with or without `--json`, is the default run without its one write: the same ledger, the
    same exit code, and no history row.
  - An argument outside a fixed list (`install-hook`, `--precommit`, `--calibrate`, `--selftest`, `--json`,
    `--status`; `-h`/`--help` still win) exits **3**, the tool's documented usage code. It prints
    `unknown argument: …` and the usage text, and reads and writes nothing. The usage text's *"There is
    deliberately no --force"* is now observable: `--force` is refused rather than silently measured.
  - `VERSION` 1.2.0 → 1.3.0. The usage text gains a `--status` line, and the default's *"append one
    history line"* now says *"when a size changed"*, which is what `append_history` does.
- **Where the list lives, and a guard that narrowed on the way.** The list sits above `def selftest`
  because the selftest's escape-hatch check (the string `--force` must not appear in the source above
  that function) is the only existing guard that can read it; `main()` is below it. While the list was
  being written, a comment above it named that function's definition. The check splits the source on the
  first mention, so it moved up, and `--force` added to the list then passed the selftest. A new test
  pins the split point to the function itself.
- **Tests, RED first against the unchanged tool** (blob `b1111d92`): 8 in a new `TestCommandLine` class in
  `tools/test_context_budget.py`. Six fail on the old tool. Two are controls that pass on it by design: the
  default run still writes, and `--help` still wins over an unknown argument. Two rows in `bin/tests.sh`'s
  budget block, in a `mktemp` project with the seed config: `--status` leaves `git status --porcelain
  --ignored` empty, and `--zzz` exits 3 and changes nothing. The same project's default run comes last, as
  the presence control: the fixture does get written to. Both rows fail on the old tool.
- **Mutants, run rather than predicted:** the append made unconditional again (3 unit tests and 1 row
  fail); the rejection removed (2 and 1); `--force` added to the list (3 unit tests, and the selftest,
  which now sees it); a comment naming the selftest's definition above the list, plus `--force` (3 unit
  tests; the selftest does not see it). The two `"--force" in args` greps, in `bin/tests.sh` and
  `tools/test_context_budget.py`, catch neither `--force` mutant, since they match that expression only.
- **Counts:** `tools/test_context_budget.py` 118 → 126 tests, `--selftest` 52 checks unchanged, `bin/tests.sh`
  139 → 141 passed, 0 failed. No gate threshold changes in this commit.

### 2026-09-20 · [ad hoc] The ledger gate stopped running after any stopped rebase — the marker git leaves behind, dropped

- **Action:** `.githooks/pre-commit` skipped replayed commits by testing five markers under the git
  dir. One of them, `REBASE_HEAD`, is **left behind by git** when a rebase that *stopped* — a
  conflict, or `-i` parked at `edit` — runs to completion. From that moment the hook exited 0 on
  every commit in that clone. The marker loop runs **before** both gates the hook chains, so the
  casualty was not only the failure-mode-#27 ledger gate but `quality_ratchet.py --precommit`,
  whose whole job is refusing a loosened threshold. Both then read green because neither ran.
- **The shape was chosen from a measurement, not from plausibility.** Every operation in the marker
  list was run to completion on git 2.50.1 and its markers observed at each stage. Two facts decided
  it: `REBASE_HEAD` is the **only** marker that survives its operation (the other four are removed
  when the operation ends or is aborted, so none needs the same treatment), and it is **redundant** —
  every rebase in progress carries `rebase-merge` or `rebase-apply` alongside it, so dropping it
  costs no in-progress coverage. A third measured fact explains how it goes unnoticed: a **clean**
  rebase leaks nothing, so only a stopped rebase arms the trap.
- **A hook is the one gate nothing else watches, and it fails open** — its failure mode is silence,
  not red. So the fix ships with `.githooks/pre-commit --selftest` (10 checks, on the
  `.githooks/commit-msg --selftest` precedent) and a `pre-commit-selftest` gate in
  `.quality-gates.json`, modelled on the existing `commit-msg-selftest` entry. Adding a gate always
  passes the ratchet; no threshold moved.
- **Evidence:** RED-first — the same ten checks against the unfixed marker list go red on exactly
  one, green on the other nine, so the test isolates the defect rather than being vacuously red;
  0 red after the fix. The selftest builds each probe repo with `git init --template=`, so a user's
  `init.templateDir` cannot install *its* hooks into the probe and answer for the hook under test,
  and it asserts each fixture actually built (a probe against a repo that failed to build answers
  about nothing, in green). `bin/tests.sh` unchanged at 139 passed / 0 failed;
  `quality_ratchet.py --run` 11/11 with the new gate.

### 2026-09-18 · [BL-72] `bin/check-handoff` skips a fenced block with an info string, instead of the newest receipt behind it

- **Defect:** `scan()` recognised two fence openers, a bare backtick run (a wrapper) and a `handoff` fence. A fence
  with any other info string, such as the `sh` block in the seed's *Size, and when to archive* section, was read as
  prose, so its closing fence opened a wrapper that ran to the next bare fence: the closing fence of the newest
  receipt. That receipt was never parsed. The checker validated the one below it and exited 0, and `--all` counted
  one receipt fewer. Every adopter ledger that keeps the seed's section above its receipts was affected.
- **Fix:** such a fence is now skipped whole, to a bare closer at least as long (CommonMark), as a wrapper already
  was. An info string may not contain a backtick, so a prose line that starts with inline code quoting a fence
  opens nothing. Unlike a wrapper's, the block's lines stay visible to the orphan check, so a receipt under a
  misspelled tag is reported field by field, at its own lines. An unclosed one is reported like an unclosed
  wrapper. A `handoff` fence is read as before.
- **Tests:** ten assertions in `bin/tests.sh` Test 22, after block isolation. Six fail on the previous checker, and
  each of six mutants of the fix fails at least one. The seed fixtures read the seed itself, and fail loudly if it
  loses its sentinel comment or its info-string fence, rather than passing on a fixture that tests nothing.
- **Placed** above the previous entry, below `upstream/main`'s.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-17 · [BL-57] Four wording fixes: the thin seed, the flight manual's index row, a moved note, two test references

- **Change:**
  - `starter-kit/CHANGELOG.md` — *"Old entries are archived"* becomes *may be archived* (archiving is optional), and
    *"size and archiving"* becomes *reading and archiving* (the rules name no size).
  - `ITERATIVE_METHODOLOGY.md:575` — the §Reference Apparatus row, the same *reading and archiving*.
  - `FRAMEWORK_APPARATUS.md` — the note under the entry format kept a clause about the seed's freshness check, which
    no longer applies where the note now lives; it says only that the tokens are illustrative.
  - `bin/tests.sh` Test 20 (b2) — two references to `BOOTSTRAP.md:85`, which this branch moved to `:87`, cite the
    paragraph by name instead.
- **Why:** each was found by the same independent review. No rule changes; no marker changes, so no seed reads stale
  because of this.
- **Placed** above the previous entry, below `upstream/main`'s.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-17 · [BL-57] *Placement* covers the trimmer's first month heading and a merged branch's entries

- **Change:** two sentences in `FRAMEWORK_APPARATUS.md` §The Action Ledger, *Placement*. A ledger with no month
  headings starts them at its next new month **or at its first trim**, whose entry `methodology_trim.py` files under
  the current month's heading (`insert_ledger_entry`). A merged branch's entries keep their branch order as one block
  rather than being re-sorted by date.
- **Why:** the rule as written contradicted the trimmer, which adds the current month's heading on its first trim;
  and it said nothing about a merged branch, whose newer entries sit below older-dated ones on `main` today (PR #80's
  did, and this branch's will). Found by the same independent review.
- **Placed** above the previous entry, below `upstream/main`'s — the case the second sentence describes.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-17 · [BL-57] The `HANDOFFS.md` seed says its archive rule is its own, not the ledger's optional one

- **Change:** `starter-kit/HANDOFFS.md`'s pointer to *Reading and archiving* adds one sentence: that subsection makes
  archiving optional for `CHANGELOG.md`, and this file keeps its own rule — archive when the trimmer's trigger fires.
- **Why:** the seed states that rule and then sends the reader to a subsection that concludes *"Archiving is
  optional"*, which read as a contradiction. The two rules differ on purpose; this branch changes the ledger's and
  leaves `HANDOFFS.md`'s as it was. Found by the same independent review.
- **Placed** above the previous entry, below `upstream/main`'s.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-17 · [BL-57] The `CHANGELOG.md` migration route keeps the lines a trimmer wrote above the first entry

- **Change:** `bin/status`'s route for a stale `CHANGELOG.md`, and `starter-kit/BOOTSTRAP.md`'s *Updating an existing
  project* paragraph, said to replace **everything** above the first entry with the seed's header. They now say to
  replace the rules text or old header, keeping any archive-pointer block and month heading a trimmer wrote there.
  The `HANDOFFS.md` route in both says to replace any older copy of the size section, and the paragraph names the
  `handoffs-format: 2` line as what makes a copy current (the previous entry's marker).
- **Why:** `methodology_trim.py` writes its shard pointer block and the topmost `## YYYY-MM` heading into that
  zone (`:310`, `:1191`), so the old route, followed literally, deleted them; one adopter's migration nearly did. The
  `HANDOFFS.md` route already kept them; the `CHANGELOG.md` one did not. Found by the same independent review.
- **Test:** Test 20 (g) — the route assertion follows the new wording, and two new assertions require the keep
  clause in the note and in the paragraph it cites. Neither text carried it at the previous commit.
- **Placed** above the previous entry, below `upstream/main`'s.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-17 · [BL-57] The `HANDOFFS.md` seed gets a versioned format marker; its section heading could not tell an old seed from a new one

- **Change:** `starter-kit/HANDOFFS.md` opens its *Size, and when to archive* section with `handoffs-format: 2`, a line
  the seed asks adopters to keep; `bin/_manifest.py` keys `HANDOFFS.md` on it, as `CHANGELOG.md` keys on
  `ledger-format: 2`; `bin/status`'s route names the section, which carries the marker, and says to replace any older
  copy of it.
- **Why:** the heading arrived in the seed that shipped with the trimmer (`56997af`), over the size premise this
  branch removes (a 65,536 B byte row priced as a *context tax*). Keyed on the heading, that seed read current: a
  marker present in the earlier format can never flag it. Two of six real adopters carry exactly that text and read
  current. Found by an independent review of this branch before the pull request.
- **Test:** `bin/tests.sh` Test 20 (g) gains the shipped-marker check and a fixture with the heading, the old premise
  and no marker. Run against the heading key, that fixture read `present`; against the marker, `present (stale format)`.
  A freshly synced project reads `present` for both seeds, with no note.
- **Placed** above the previous entry, below `upstream/main`'s.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-17 · [BL-57] Two code comments stop citing a plan item that exists only in the contributor's fork

- **Change:** `bin/status:112` and `bin/tests.sh:323` each ended a sentence with *"(BL-57 item (22))"*, a pointer into
  a planning document on `rmsharp/methodology` that this repository does not have. Both sentences already state the
  reason in full, so the citation is dropped and nothing replaces it. Comments only; no behaviour changes.
- **Placed** above the density entry, below `upstream/main`'s.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-17 · [BL-57] The three read-set densities re-measured on the blobs this branch ships

- **Change:** `.context-budget.json` — `bytes_per_token` and `measured_bytes` for `CLAUDE.md`,
  `starter-kit/SESSION_RUNNER.md` and `starter-kit/SAFEGUARDS.md`, and each entry's note: which blob was measured,
  and which blob id to watch for the next re-measure. The config's own rule is to re-measure when a file's blob
  changes; this branch changed all three, and the densities still named `1244e95b`, `2a3e410d` and `933816b4`.
- **Measured** by the doubled-file method (seven copies for `SAFEGUARDS.md`), each run reproducing the previous
  measurement exactly as a control: `CLAUDE.md` `dd416ea` 46,953 doubled → 23,476.5 tokens, 2.5182 B/token (control
  46,965); the runner `4811f02` 37,717 → 18,858.5, 2.8225 (control 37,731); `SAFEGUARDS.md` `ed49b97` 42,586 over seven
  → 6,083.7, 2.8155 (control 42,208).
- **Every ceiling holds:** 6.5 tokens under `CLAUDE.md`'s 23,483, 41.5 under the runner's 18,900, 16.3 under
  `SAFEGUARDS.md`'s 6,100; the pair is 24,942.2 of the 25,000-token read cap (99.77%). No ceiling changed.
- **Correction:** the `[BL-63]` entry below gave `SAFEGUARDS.md` as *"about 6,067 tokens"*, an estimate at the old
  density. It measures 6,083.7. Left at 2.8234, the tool counted 6,066, 18 tokens under.
- **Placed** above the `[BL-63]` entry, below `upstream/main`'s.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-17 · [BL-63] `BOOTSTRAP.md` says how to commit a `bin/sync` run, and `SAFEGUARDS.md`'s five-file cap names it

- **Change:**
  - `starter-kit/BOOTSTRAP.md`, *Setup with `bin/sync`* — a new *Committing a sync* paragraph after *Drift safety*:
    in committed mode, one `bin/sync` run is one commit, holding exactly the files it wrote (which `--dry-run` lists
    first) plus that commit's `CHANGELOG.md` entry; the adopter's own edits afterwards go in their own commits under
    the cap. It gives the reasons: every file is a byte-for-byte copy of a canonical one, one `git revert` undoes the
    run, and a split can leave operating files citing tools that have not arrived yet.
  - `starter-kit/SAFEGUARDS.md`, the five-file cap row — one sentence, *"A committed-mode `bin/sync` run is one
    commit, whatever its file count"*, linking `BOOTSTRAP.md`. Without it the new paragraph would contradict a file
    that says it wins over other guidance and lists the cap under *No Exceptions*.
- **Why:** `bin/sync` copies the whole distributed corpus and does not commit, and no distributed document said how
  its result is committed, so every committed-mode sync that updates more than five files broke the cap or left the
  adopter to invent a split. Measured in one adopter's syncs: 15 and 21 files; dry runs in three others: 14–16.
- **Size:** `SAFEGUARDS.md` 17,024 → 17,129 B, about 6,067 tokens at its recorded 2.8234 B/token against its 6,100
  `max_tokens`; the read-set pair's partition (18,900 + 6,100) is unchanged. `BOOTSTRAP.md` +584 B; it has no budget.
- **Separable:** this commit touches nothing else, so it can be dropped from the pull request on its own.
- **Placed** above the previous `[BL-62]` entry, below `upstream/main`'s.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-17 · [BL-62] The read-cap partition test sums only the files read together, not every whole-read class

- **Change:**
  - `tools/test_context_budget.py` — `TestThisRepoReadSetPartition` summed the `max_tokens` of every class in
    `WHOLE_READ_CLASSES` (resident, read-mandated, read-set) against the one 25,000-token Read. Only the read-set
    pair, the Phase 0 mandatory read, is read in one Read; a read-mandated or resident file is read whole but on its
    own. So a config declaring two read-mandated ledgers at 25,000 tokens each, two full Reads, failed the test as
    50,000 > 25,000. The check moves into `token_partition(cfg)`, which sums only `READ_TOGETHER_CLASSES`
    (`("read-set",)`); the repo test and its presence control run on it unchanged in meaning, and the renamed
    `test_the_read_set_token_ceilings_partition_the_read_cap` replaces
    `test_whole_read_class_token_ceilings_partition_the_read_cap`. New `TestTokenPartitionRule`, four tests on
    fixture configs: separately-read files do not share the cap; a read-set pair past the cap is still refused;
    one within it passes; one at exactly the cap fits.
  - `.context-budget.json` — the read-set note said the test fails any edit whose ceilings *"in a whole-read
    class"* exceed the cap. It now says *"in the read-set class"*.
- **Why:** the fork hit it with its own config (two read-mandated ledgers at 25,000 each) and had to drop the two
  declarations to pass. Canonical-only: the test file is not distributed, so no adopter runs it.
- **Checked:** test-first. With the check extracted but the old every-class rule kept, two of the new tests failed
  (50,000 > 25,000); with the rule restricted, the file runs 122 tests, 0 failures, 2 skipped (118 and the same
  2 skips before). Five mutants each fail it: the old every-class rule (2 failures), no class summed (4), `>`
  becoming `>=` at the cap (2), a pair skipped (4), `checked` never counted (4).
- **Placed** above the previous `[BL-57]` entry, below `upstream/main`'s.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-17 · [BL-57] `methodology_trim.py` links its design doc's public copy, and stops citing a hook flag no hook has

- **Change:** `starter-kit/methodology_trim.py`, comments only.
  - The module docstring said the design doc (`docs/planning/ledger-trimmer-design.md`) *"has not been published
    to a public remote"*, so it gave no URL. The doc is public in the `rmsharp/methodology` fork, so the docstring
    now links it at the commit that last changed it (`979dc73`), where the link cannot drift. The file's section
    citations (*design §2*, *§4*, *§5*, *P2* and the rest) now resolve through that link.
  - The *defaults* paragraph said the tool never runs `git mv` because *"`--no-renames` in the FM #27 pre-commit
    hook"* would let a rename-shaped trim pass. This repository's hook has no `--no-renames`, and never did. The
    paragraph now keeps the rule and says what the tool does instead: it writes a new shard and edits the live
    ledger in place, so the ledger keeps its path and its history.
- **Why:** item F5 of the PR #80 review, open since #80 merged. A distributed comment that cites a missing document
  and a flag that does not exist sends the next maintainer of the tool looking for both.
- **Checked:** the module still parses; `grep -c 'no-renames\|not been published'` on the file reads 0; the link
  resolves on GitHub (74,109 B, blob `09c99c14`, the blob the fork's `main` holds). No test reads the docstring.
- **Placed** above the previous `[BL-57]` entry, below `upstream/main`'s.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-17 · [BL-57] `bin/status`'s stale-seed note gives each seed its own migration route, and the `BOOTSTRAP.md` paragraph it cites gives the `HANDOFFS.md` one too

- **Change:**
  - `bin/status` — the note beneath the table told an adopter holding either stale seed to *"replace the text
    above the first entry (or receipt) with the current starter-kit seed's"*. It now gives each flagged file
    its own route: for `CHANGELOG.md`, replace the text above the first entry with the seed's header; for
    `HANDOFFS.md`, bring across the seed's `## Size, and when to archive` section, above the first receipt,
    and keep the rest of the front matter. The routes sit in `MIGRATION_ROUTES`, beside `STALE_SEED`; the
    `HANDOFFS.md` one names the section from `bin/_manifest.py`'s marker, and a file with no route gets the
    general rule.
  - `starter-kit/BOOTSTRAP.md:85` — the paragraph the note cites named only the `CHANGELOG.md` formats and
    route. It now also names a `HANDOFFS.md` without the size section, and gives that file's route.
  - `bin/tests.sh` Test 20 (g) — eight assertions: a route appears only for a flagged file; a stale
    `HANDOFFS.md` is flagged and gets its own route and no *replace*; two stale seeds get both routes; the
    cited paragraph gives the `HANDOFFS.md` route.
- **Why:** BL-57 item (22). The `HANDOFFS.md` seed differs from an older copy by one section, the one the
  marker keys on. Replacing the front matter instead deletes whatever an adopter's trimmer wrote there, an
  archive pointer and a count sentence among them.
- **Checked:** Test 20 was run alone before the fix: 5 failures, among them *"the note tells a stale
  HANDOFFS.md to replace its front matter"*; 24 passed, 0 failed after. Two mutants fail it: routes printed
  for files that are not flagged (2 failures), and no `HANDOFFS.md` route (1).
- **Placed** above the previous `[BL-57]` entry, below `upstream/main`'s.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-16 · [ad hoc] Parallel-sessions plan — making fan-out to concurrent writing sessions clean, not just safe

- **Action:** planning session S24 on branch `docs/parallel-sessions-plan`. The operator asked whether the
  quality-ratchet work (PR #82) made multi-agent fan-out workable; the Phase 0 answer was *safe but not
  clean* — `ITERATIVE_METHODOLOGY.md` §Mechanical Gates binds every actor's output, but two writing
  sessions still collide on `CHANGELOG.md`/`HANDOFFS.md` (prepend-only, one anchor, co-staging hook forces
  every commit onto them — S21 hit it with two sequences), on serial `S<N>` identity, on the absent
  merge-session receipt (the open "11 reconciled receipts" ruling), and on Test 9's `--source=github`
  coupling to `main`. Deliverable: `docs/planning/parallel-sessions-plan.md` + a PR for review, nothing
  implemented (S13's shape). Results appended at close-out.
- **The plan, committed:** `docs/planning/parallel-sessions-plan.md` — 468 lines; §1 decomposes the operator's
  own records into six mechanisms (two-writers-in-one-tree, the return-content fan-out that worked, the S21
  double-ledger conflict, the undischargeable "11 receipts", Test 9's `main` coupling, the worktree-blind
  calibrate); §3 the finding (*one closer per tree*; two shapes by who closes out); §4 fifteen decisions D1–D15
  plus an alternatives table (changelog fragments considered and deferred); §6 six phases, one per session;
  §7 six honest ceilings; §8 twelve operator decisions; §9 the evidence commands, all re-run before commit.
- **PR opened (non-commit action):** [PR #83](https://github.com/KJ5HST/methodology/pull/83) from
  `docs/parallel-sessions-plan` at `903d724`, read back from the API (OPEN, +492/−0, 3 files); its body carries
  the summary and asks the operator to answer §8 there — that answer is the plan's Phase 0. **Not merged.**
- **Gate run at `903d724`:** `quality_ratchet: 8/10 pass · 2 fail · 0 unmeasured · results bcbd7f39383a ·
  manifest 97a7aab85b9a`. The two fails are one **environmental** failure — `tests-sh-passed` 138 /
  `tests-sh-failed` 1 from `tools/test_context_budget.py` `TestFitGateEndToEnd::test_an_admitting_floor_prints_the_constant`:
  this machine now holds exactly 4 transcripts for this path (calibrate()'s fit minimum; this session's is the
  4th), so the fit runs on 4 points and is refused for a negative slope (R² 0.049), a refusal the test's `setUp`
  does not skip on (it skips only on "not enough" — S16's fix for the sibling case S19 reported). Tool and test
  are byte-identical to `main @ 6b29d3d`; not loosened; the one-file fix is the next session's first small task.
- Session S24: claim `3c244aa` + plan `903d724` + the close-out commit (receipt complete, cites the run). Every
  commit ran the ledger co-staging hook clean — no `--no-verify`.

### 2026-09-16 · [BL-57] This ledger's front matter points to §The Action Ledger for its rules, its audit and its month headings

- **Change, in this file's front matter only** (the maintainer's own file — the PR body will say it can
  be dropped, and that dropping it leaves the pointer false):
  - `:11`–`:13` — the rules *"live in [`FRAMEWORK_APPARATUS.md` §The Action Ledger]"*; the seed *"points
    there"*. It said the rules and the seed both *"live in `starter-kit/CHANGELOG.md`"*, which P1 made
    false when it moved the rules out of the seed.
  - `:15`–`:17` — the source-tag paragraph cites *"the audit in §The Action Ledger — anchored to the entry
    heading, and reading any archived shards"*, where it published the unanchored one-file
    `grep -E '\[(issue #|BL-|ad hoc)' CHANGELOG.md`. On this commit that form matches **94** lines
    against **68** entries: it also counts the tag definitions and every in-prose mention of a tag.
  - `:22`, `:24` — `[BL-<N>]` becomes `[BL-<id>]` in the tag definitions, the item P3 recorded as left
    for P4. What `[BL-<N>]` remains on this tree is history: entry bodies here, `CLAUDE.md:123` (v3.1)
    and `README.md:365` (*What's New*).
  - `:36`–`:37` — *"Promote to `## YYYY-MM` sections as it grows"* becomes *"Month headings start at this
    ledger's next new month, and nothing below is retrofitted"*. This ledger has none today, so the
    first one opens at the first entry dated in October.
- **Why:** BL-57 D8 (i), in one commit as the plan requires; C10, C13 and P3's finding (4).
- **Checked:** the audit gives **68** in `zsh` and in `bash` on this commit, equal to the file's `^### `
  count — this tree has no shards. `FRAMEWORK_APPARATUS.md:338` is `## The Action Ledger`, the link's
  target.
- **Placed** above the previous `[BL-57]` entry.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-16 · [BL-57] `CHANGELOG.md` is described as the action ledger, not as completed-work history — and `CLAUDE.md` is back under its token ceiling

- **Change:** *"Completed work history"* becomes the action ledger at `starter-kit/BOOTSTRAP.md:23`, `:107`,
  `:131`, `README.md:96`, `:114`, `:200` and `CLAUDE.md:51`. Two instructions that framed an entry as
  something written when work *completes* now say to record each action, and to remove a finished
  backlog item from `BACKLOG.md`: `starter-kit/BOOTSTRAP.md:139` and the matching sentence in
  `README.md:96`. The migration step at `starter-kit/BOOTSTRAP.md:145` moves completed items in *as
  entries, newest on top*, where it said *"into reverse-chronological sections"*.
- **Also:** `CLAUDE.md:21`, the *Reference apparatus* row, now reads *"its tables, tests, scoring scales
  and ledger rules; distributed"*. It pays back the 4 tokens the merge `52ad407` carried over
  `CLAUDE.md`'s `max_tokens` 23,483 — P1's *"and the `CHANGELOG.md` rules"* was 9 B shorter and 4
  tokens longer than the wording it replaced.
- **Why:** BL-57 C11. The seed's ledger records every action, including releases, PRs and declines, and
  an instruction keyed to *completing work* misses all three.
- **What *"completed work"* still says, and why it stays:** `README.md:530` is the v2.1 *What's New* entry
  (history); `CLAUDE.md:128` is the v3.6 release narrative quoting a dashboard label; `starter-kit/BOOTSTRAP.md:134`
  says that open work, completed work and plans belong in separate files, which is the backlog split
  and still true. `grep -ni 'completed work history'` over the three files finds only `README.md:530`.
- **Size, in tokens:** `CLAUDE.md` reads **46,953** doubled (23,476.5 tokens) against **≤ 46,965**
  (`upstream/main`'s blob `1244e95b`, whose recorded figure reproduced in the same run): 6 under
  `upstream/main`, 10 under the merge. Bytes: `CLAUDE.md` −25, `README.md` +13, `BOOTSTRAP.md` +81; the
  last two carry no budget row. The runner is untouched by this commit.
- **Placed** above the previous `[BL-57]` entry.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-16 · [BL-57] A newest-on-top ledger is prepended to, not appended to; the claim commit's entry says *(in progress)*

- **Change:** seven instructions that said *"append … newest on top"* now say *prepend*: the runner's
  Phase 3F (`starter-kit/SESSION_RUNNER.md:281`), failure mode #27's countermeasure (`:332`) and its
  Degradation row (`:360`); `ITERATIVE_METHODOLOGY.md:294`, Phase 6 step 8; `HOW_TO_USE.md:767` and
  `:804`; and the ledger hook's refusal text (`.githooks/pre-commit:70`). The runner's Phase 1B stub
  (`:88`) and the flight manual's Phase 1B step 1 (`ITERATIVE_METHODOLOGY.md:169`) now say the claim
  commit's ledger entry reads *(in progress)* and close-out records the rest, where they said the
  session's actions are recorded at Phase 3F — which a claim commit's own entry contradicts.
- **Why:** BL-57 C3 and C7. §The Action Ledger already said *prepend*; these seven sites were the other
  side of that disagreement. *Append-only*, meaning never edited, is a different claim and stays.
- **Size, in tokens, against the criterion restated before this phase's first edit:** the runner reads
  **37,717** doubled (18,858.5 tokens) against **≤ 37,731** (`upstream/main`'s blob `2a3e410d`) — 7 tokens
  more than P4's start at the merge, 7 under the criterion; the 36,955 control reproduced in the same
  run. Bytes: runner +9, `ITERATIVE_METHODOLOGY.md` +45, `HOW_TO_USE.md` +2, the hook +1. The flight
  manual's +45 misses the plan's *"byte-neutral wording"*; it has no budget row — `.context-budget.json`
  lists it under `_deliberate_exclusions`.
- **Checked:** `grep -nE '[Aa]ppends? (a|one) dated|Append the owed entry'` over the runner,
  `ITERATIVE_METHODOLOGY.md`, `HOW_TO_USE.md` and the hook exits 1 — no matches. No test or tool pins
  the changed text (`git grep` over `bin`, `tools` and the starter-kit scripts).
- **Placed** above the previous `[BL-57]` entry.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-16 · [BL-57] §The Action Ledger states when an entry is written and where it goes: one per commit, never edited, under the topmost month

- **Change:** `FRAMEWORK_APPARATUS.md` §The Action Ledger replaces its closing paragraph — *"Work
  committed but not finished … Promote to `## YYYY-MM` sections as the list grows"* — with two rules,
  and its opening sentence stops saying entries are written *"At close-out"*, which a claim commit's
  entry contradicts. Each rule, as it now reads on this commit:
  - `:439` — *"**Lifecycle — one entry per commit, never edited.** The commit is the unit the ledger
    co-staging hook checks, so each commit carries its own entry, and each non-commit action gets one
    of its own."*
  - `:442` — *"A claim commit carries an *(in progress)* entry, and close-out adds its own entry rather
    than rewriting the claim's."* Work committed but unfinished is marked the same way.
  - `:446` — *"A committed entry is never edited. A correction is a new entry that names what was
    wrong. The one exception is removing content that must not be published … and that removal is
    recorded by an entry of its own."*
  - `:449` — *"A Phase 0 backfill is the one entry that may span several commits."*
  - `:451` — *"The Phase 1B `CHANGELOG: pending` marker lives in `SESSION_NOTES.md`. A project that
    keeps no `SESSION_NOTES.md` relies on its `status: pending` `HANDOFFS.md` receipt instead."*
  - `:454` — *"**Placement — prepend under the topmost `## YYYY-MM`.** … When the month changes, open
    the new month's heading above the last one: group by month, not by release. A ledger that has no
    month headings starts them at its next new month, and nothing already written is retrofitted.
    Entries stay at `###`, the level the tools key on."* — `_DATED_ENTRY_RE`
    (`starter-kit/methodology_dashboard.py:211`) and the trimmer's `record_start`
    (`starter-kit/methodology_trim.py:307`) both anchor on `^###`.
- **Also:** `HOW_TO_USE.md:748` gives the apparatus as *"~535 lines"* — 534 after this change; it said
  515, which P2 had already made stale at 501.
- **Why:** BL-57 C7, C8 and C13, as the operator decided at Q4 A (one entry per commit, never edited).
  The rules had one sentence on a claim's entry (*"mark it `(in progress)`"*) and none on editing,
  and the month rule said *"promote … as the list grows"*, which names no point at which to start —
  this ledger holds 65 entries and no month heading.
- **Placed** above the previous `[BL-57]` entry, below `upstream/main`'s block, after the merge `52ad407`.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-16 · [BL-57] Correction: §The Action Ledger attributed a measurement to a ledger that does not record it

- **What was wrong:** the entry above, and the text it describes, said the unanchored audit *"returned
  78 against 64 actions"* **"on this framework's own ledger."** The measurement is real, but it was
  taken on the project whose ledger was split at v3.6, not on this repository's — whose root
  `CHANGELOG.md` carries no such record. A reader of this tree could not check the claim, and merged
  upstream it would attribute the count to a ledger where the comparison was never run.
- **Change:** the sentence now states the failure first and the number as what it is —
  *"an unanchored pattern … can report more actions than the ledger holds; the project this was
  measured on counted 78 where 64 had happened."* The mechanism is checkable anywhere; the figure no
  longer claims a home it does not have.
- **Why:** an unverifiable number in a distributed file is the thing §The Action Ledger's own advice
  warns against — it is right when written and unfalsifiable afterwards. Caught by grepping this
  tree for the figure's provenance before close-out, not by any gate.
- **Placed** above the previous entry.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-16 · [BL-57] The `HANDOFFS.md` seed enumerates its shards with `git ls-files`, not a bare glob

- **Change:** `starter-kit/HANDOFFS.md`'s rule that anything counting receipts must span the live
  file and its shards published that span as the bare glob `HANDOFFS.md docs/archive/HANDOFFS-*.md`.
  It now reads `HANDOFFS.md $(git ls-files 'docs/archive/HANDOFFS-*.md')`, with the reason stated:
  zsh aborts a command whose glob matches nothing, so before the first split the bare form counts
  nothing at all — the same reason the ledger's audit is written that way. 10,417 → 10,676 B.
- **Why:** C10. The bullet was outside P2's lines and was carried to P3 with the audit it matches.
- **Reproduced in a throwaway repository with one entry and no shard:** the bare form prints `0`
  under zsh (with `no matches found` on stderr, exit 1) and `1` under bash (with a `cat` error on
  stderr, exit 0); the `git ls-files` form prints `1` and exits 0 under both. The failure the fix
  removes is not an error the caller sees — it is **two shells returning two different counts**.
- **Placed** above the previous entry.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-16 · [BL-57] The runner cites the ledger rules instead of restating their audit; three files adopt `[BL-<id>]`

- **Change:** `starter-kit/SESSION_RUNNER.md:39` (Phase 0, the backfill step) drops the inline
  `grep -E '\[(issue #|BL-|ad hoc)' CHANGELOG.md` for a link to
  [§The Action Ledger](docs/methodology/FRAMEWORK_APPARATUS.md#the-action-ledger), so the audit is
  published in exactly one place. `:278` (Phase 3F) and `:329` (failure mode #27) change
  `[BL-<N>]` to `[BL-<id>]`, as do `ITERATIVE_METHODOLOGY.md:294` and `.githooks/pre-commit:57`.
  After this commit `grep -F '[BL-<N>]'` over the runner, the flight manual, `HOW_TO_USE.md`, the
  hook, §The Action Ledger and both seeds finds nothing.
- **Why:** C6 and C10, the distributed half of BL-57's P3. One rule, one home, one audit.
- **Two duplicate clauses paid for the link.** The step already showed `[ad hoc]` in its own entry
  template, so *"default `[ad hoc]`"* was removed; and the note's closing paragraph already says the
  backfill *"does not become this session's deliverable"*, so the step's weaker *"separate from this
  session's later deliverable"* was removed. **The runner ends smaller than it started: 52,195 →
  52,163 B, and 18,477.5 → 18,463.5 tokens.**
- **The two units disagreed about the link, which is why the size rule is now stated in tokens.**
  Adding the cross-reference and the two id changes alone measured **+36 B but only +9 tokens** — a
  path tokenizes at about 4 B/token where this file averages 2.8248 — so a byte rule overstates what
  a cross-reference costs and understates what cut prose saves. Tokens are the unit the read cap and
  the file's own ceiling are written in.
- **Placed** above the previous entry.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-16 · [BL-57] §The Action Ledger: a source tag admits any backlog id, and the audit reads the archived shards

- **Change:** `FRAMEWORK_APPARATUS.md` §The Action Ledger states the vocabulary as `[issue #<N>]`,
  `[BL-<id>]` and `[ad hoc]` — `<id>` being whatever id the project's backlog gives the item, not a
  number. The audit moves out of the vocabulary sentence into its own paragraph and becomes
  `cat CHANGELOG.md $(git ls-files 'docs/archive/CHANGELOG-*.md') | grep -cE '^### …'`. Three
  properties of that command are stated in place, because each fixes a way the old one-line form
  gave a wrong number rather than an error: **`git ls-files`, not a bare glob** — zsh aborts a
  command whose glob matches nothing, so in a project that has never trimmed the bare form returns
  no count at all; **anchored to the entry heading** — unanchored it also matches the vocabulary's
  own definitions and every mention of a tag in prose, which on this repository's ledger returned
  78 against 64 actions; and **`BL-[^]]+`, not `BL-[0-9]+`** — it counts whatever id the backlog
  uses. A closing sentence says entries written before a project adopted the vocabulary stay as
  written and are not counted, so the shortfall is expected rather than a defect to repair.
- **Why:** C6 and C10, the source-tag half of BL-57's P3. The rules live in one place now, so the
  audit published beside them is the one every project runs.
- **Measured, not asserted.** The two shells disagree on the bare-glob form in a repository with no
  shard: zsh prints `0`, bash prints `1`. Across the six adopter repositories, widening
  `BL-[0-9]+` to `BL-[^]]+` moves the count 96 → 262, 599 → 784 and 236 → 247 in three of them —
  **362 logged actions the numeric-only pattern could not see** — and leaves the other three
  unchanged. One of those adopters tags with `BL-OPS-ADMIN-PW-RECOVERY-001`.
- **Placed** above the previous entry.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-15 · [BL-57] The `HANDOFFS.md` seed names no size — archive when the trimmer's trigger fires; the trimmer's budget comment drops *"context-tax"*

- **Change:** `starter-kit/HANDOFFS.md` §Size, and when to archive keeps its heading, which `bin/status`
  keys on (D9), and replaces what follows it: the premise that Phase 0 reads the file every session, and
  the two-cap table with its 65,536 B default and its citations of BL-52 and a fork-only plan, give way
  to the reads the protocol makes and one rule — *"Archive it when the trimmer's trigger fires. The tool
  states the trigger, and this file names no size of its own."* The pointer to §The Action Ledger names
  *Reading and archiving* and what it holds, and the *three files* list says receipts move *"when the
  file is archived"*, not *"once the file outgrows a session's read"*. `starter-kit/methodology_trim.py:186`:
  *"the per-file context-tax budget"* → *"the per-file byte budget"* — a comment; the module's AST is
  identical to `b82dcff`'s. 11,505 → 10,417 B.
- **Why:** steps 2 and 3 of BL-57's P2 (C1, C2, C12, C14). This file's own archive rule otherwise stands
  (D7); whether *optional* extends to it is the operator's call.
- **Placed** above the previous entry.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-15 · [BL-57] §The Action Ledger: the ledger is never read whole, and archiving is optional — the two-cap size rule goes

- **Change:** `FRAMEWORK_APPARATUS.md`'s *Size, and when to archive* becomes *Reading and archiving*,
  on the operator's Q2 A. Each rule, at its line in this commit: `:428` *"The protocol never asks a
  session to read this file whole"*, then its three partial reads — Phase 0 reconcile from `git log`
  (`:430`), close-out at the top (`:432`), a lookup by `grep` or `git log --grep` (`:433`); `:436`–`:438`,
  past the trimmer's `READ_REFUSE_BYTES`, read the top with an offset and a limit; `:440` *"Archiving is
  optional"*; `:442` *"The tool's trigger is the only statement of when — these rules name no size"*;
  `:476` conservation, *"the live file and its shards together never lose an entry"*, so a count spans
  both and never the live file alone, or a count ratchet refuses every trim (C9); `:486`, kept, a trim
  *"does not belong in Phase 0"*. The two-cap table goes — its 65,536 B default (C2), its *"every session
  pays"* premise (C1), its citations of BL-52 and a planning document this repository does not hold
  (C12) — with the rate-versus-level argument, which describes a line cap the trimmer no longer has. The
  shard convention stays; its enumeration becomes `cat CHANGELOG.md $(git ls-files
  'docs/archive/CHANGELOG-*.md')`, equal in bash, zsh and a Python count with no shard (55) and with
  eleven (526). The *three files* paragraph (`:498`) no longer says the ledger splits *"once it outgrows
  a session's read"*, and the file's intro (`:13`) and the section's opening (`:342`) no longer call the
  moved text verbatim. 28,022 → 25,983 B.
- **Why:** step 1 of BL-57's P2 (C1, C2, C9, C12, and C4's half in this file). The protocol reads only
  parts of the ledger, so its size costs no session a read; the trimmer stays, for a project that wants
  a smaller live file.
- **Placed** above BL-57's P1 entries, below `main`'s.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-15 · [BL-57] The documents that describe `FRAMEWORK_APPARATUS.md` name its seventh section

- **Change:** `HOW_TO_USE.md`'s layer table (the apparatus row gains *write a ledger entry*; ~330 → ~515
  lines), `CLAUDE.md`'s Document Hierarchy row, and `ITERATIVE_METHODOLOGY.md` §Reference Apparatus, whose
  table listed the six sections that moved there and now lists §The Action Ledger as well. Wording only.
  The `CLAUDE.md` row is 9 B shorter than before: `.context-budget.json` pins that file's ceiling at its
  size (59,168 B), so it names the rules and drops *"Extracted so the manual fits one read"*, which the
  apparatus's own intro already says.
- **Why:** step 4 of BL-57's P1 — the file gained a section in step 2, and three documents that describe
  it did not know. The plan named the first two; the third is the same kind of index, found by grepping
  for the set-size claim (*"Six sections moved there"*).
- **Placed** above #80's entries, below `main`'s.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-15 · [BL-57] `bin/status` keys the `CHANGELOG.md` seed on `ledger-format: 2`, and its migration advice stops rewriting entries

- **Change:** `bin/_manifest.py`'s `SEED_FORMAT_MARKERS` key `CHANGELOG.md` on `ledger-format: 2`, the
  seed's pointer line, instead of its title, and `HANDOFFS.md` on its `Size, and when to archive` heading
  instead of its title; the comment states why a title can never fire. `bin/status`'s migration note and
  `BOOTSTRAP.md`'s *Updating an existing project* paragraph now say: replace the text above the first
  entry with the current seed's, leave every entry as written, and reseed only a file with no history.
  `bin/tests.sh` Test 20: the in-use fixture carries the marker line, and a new case (b2) holds the frozen
  pre-ledger-format-2 seed, which must read *present (stale format)*.
- **Why:** step 3 of BL-57's P1. A title never changed across formats, so keying on it reported every old
  seed as current; and the old advice — *"reconcile its header and per-entry format"* — told adopters to
  rewrite committed entries.
- **Verified:** (b2) fails against the title-keyed marker (116 passed / 2 failed) and passes with this
  commit (117 / 1; the other failure is Test 9 throughout). On copies of six adopters, `bin/status` reads
  every `CHANGELOG.md` *present (stale format)*, with the new advice beneath, and its six `HANDOFFS.md`
  verdicts equal fork `main`'s, which already keys on that heading.
- **Placed** above #80's entries, below `main`'s.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-15 · [BL-57] The `CHANGELOG.md` rules move to `FRAMEWORK_APPARATUS.md` §The Action Ledger; the seed becomes a pointer with a format marker

- **Change:** the seed's three rule sections — *How to add an entry*, *Size, and when to archive* and
  *CHANGELOG.md vs SESSION_NOTES.md* — move verbatim, one heading level down, into a seventh section of
  `FRAMEWORK_APPARATUS.md` (15,493 → 28,022 B), whose intro now says so. `starter-kit/CHANGELOG.md` keeps
  its title, purpose paragraph, sentinel and footer, and gains a linked pointer carrying
  `ledger-format: 2` (12,893 → 1,335 B). `starter-kit/HANDOFFS.md`'s cross-reference points at the new
  home, and `methodology_trim.py`'s fence-tracking comment says where the fenced examples live now
  (comment only: its AST is unchanged). No rule changes.
- **Why:** step 2 of BL-57's P1. `bin/sync` writes a seed once and never again, so rules kept in a seed
  froze at each project's seeding; in a synced file a correction reaches every project.
- **Verified:** each moved section occurs byte for byte in the home (the plan's §9.3 check); the trimmer
  reports `NO_RECORDS` on the new seed; `bin/sync` into an empty directory seeds it; `bin/check-links`
  resolves the two new links (105 → 107).
- **Placed** above #80's entries, below `main`'s.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-09-15 · [BL-57] The trimmer's fence-awareness controls read a frozen copy of today's seed, so they survive the seed shrinking

- **Change:** `tools/test_methodology_trim.py` and a new `tools/fixtures/seed-CHANGELOG-ledger-format-1.md`,
  both canonical-only; nothing distributed changes. Three controls asserted that the live
  `starter-kit/CHANGELOG.md` holds record-shaped example lines inside fences. They now read the fixture —
  the seed exactly as it ships today, git blob `47bc8485`, which a new test asserts — while the live seed
  must still hold no records. The dated-prose test's `.replace()` anchor, `## How to add an entry`,
  becomes the `---` line, asserted to occur exactly once before the replace; a docstring cites the
  sentinel by its token, not by line number. Green with either seed.
- **Why:** step 1 of BL-57's P1. The seed's rules text moves to `FRAMEWORK_APPARATUS.md` next, and every
  adopter seeded before then keeps the fenced examples, so the controls stay meaningful on the copy.
- **Placed** above #80's entries, below `main`'s.
- **Commit:** this commit, on `bl57/changelog-rules`

### 2026-08-11 · [BL-31] Dashboard's framework-installed exclusion never learned about the context-budget gate PR #66 itself shipped

- **Origin:** fork backlog item BL-31 (`docs/planning/BACKLOG.md`, fork `main` only — not yet pushed
  to `origin` as of this entry, so no link is given rather than cite one that would not resolve),
  found re-verifying PR #66's own review-comment fixes after merge. `bin/_manifest.py` gained two
  new non-markdown dests in this PR (`context_budget.py`, TRACKED; `.context-budget.json`, SEED),
  but `tools/methodology_dashboard.py`'s `FRAMEWORK_INSTALLED_SOURCE` tuple and
  `tools/test_methodology_dashboard.py`'s `CHECKLIST_EXEMPT` test fixture — both purpose-built to
  stay in sync with this manifest — were never extended to match. Reproduced before the fix, not
  inferred: a `git worktree` at the merge commit (`a2a7275`) run against
  `python3 -m unittest tools/test_methodology_dashboard.py` gave 2 failures, both in tests that
  predate this PR (last touched at `bec4095`) and exist specifically to catch this class of drift.
- **Effect the drift had:** any adopter running `bin/sync` post-merge would have `context_budget.py`
  misattributed to their own source LOC — the exact miscount `FRAMEWORK_INSTALLED_SOURCE` exists to
  prevent for `methodology_dashboard.py` itself — and both new root files would read as neither
  scored nor exempt on the compliance checklist.
- **First fix (listing the names) did not actually work — found on review, not shipped as-is.**
  Adding `context_budget.py` and `.context-budget.json` to `FRAMEWORK_INSTALLED_SOURCE` satisfies
  the name-list agreement test, but `is_framework_installed()` then verified EVERY listed name
  against `methodology_dashboard.py`'s own content signatures (`DASHBOARD_VERSION`,
  `METHODOLOGY_ITEMS`, etc.) — which `context_budget.py` never carries — so the content check
  silently rejected it and the exclusion never fired. Reproduced directly:
  `is_framework_installed(Path("context_budget.py"), ...)` returned `False` even with the name
  listed; a real bin/sync-shaped synced doc repo still flipped `doc_only` `True -> False`.
- **Real fix:** content verification is now PER FILE. `_FRAMEWORK_FILE_SIGNATURES` gives each name
  in `FRAMEWORK_INSTALLED_SOURCE` its own version pattern and signature set —
  `context_budget.py`'s own `VERSION`/`CONFIG_NAME`/`HISTORY_NAME` markers, `.context-budget.json`'s
  own distinctive keys (though that entry is structurally unreachable today: `is_framework_installed`
  is only called for `category == "source"`, and a `.json` extension is always `"config"` — given a
  signature anyway so the completeness test below needs no special case). A new canonical test
  asserts every `FRAMEWORK_INSTALLED_SOURCE` name has a matching signature entry, so a future
  addition to the tuple cannot repeat this exact gap silently. A new behavior test reproduces the
  bug end-to-end with the REAL shipped `context_budget.py` content (not a synthetic stand-in) and
  asserts a synced doc-only repo stays `doc_only` — RED-confirmed against the name-only fix before
  landing this one. `CHECKLIST_EXEMPT` (a `tools/test_methodology_dashboard.py` test fixture, not
  scanner source) gains both names, with the same reasoning already on record for
  `methodology_dashboard.py` — their presence proves a pre-commit hook was installed, not that the
  session-operating discipline the checklist measures was followed. `DASHBOARD_VERSION` 2.10.2 →
  2.10.3.
- **Verified:** `python3 -m unittest tools/test_methodology_dashboard.py` 200/200 (197 prior + 3
  new; RED-confirmed against the pre-per-file-signature code first); `bash bin/tests.sh` 114/114;
  `python3 bin/check-links` OK (83 links / 21 files); twins confirmed
  byte-identical.

### 2026-08-10 · [ad hoc] Two defects in the HANDOFFS.md receipt spec: an unassigned reconcile promise, an unoffered locator form

- **Change:** `starter-kit/HANDOFFS.md`'s fenced receipt-format spec, two independent fixes in one
  pass since both sit in the same few lines.
- **(1) The spec promised a reconcile no procedure ever assigns.** It said `commit: pending` and
  `what_was_done: pending` are legal at write time because "the next session reconciles them to
  real shas" — but `SESSION_RUNNER.md` Phase 0 step 6 only reconciles a *missing or still-
  `status: pending`* receipt, never a `status: complete` receipt whose `commit:` field alone is
  `pending`. No procedure anywhere performs the promise as written. Reworded to state `pending` as
  a legitimate resting value for both fields, not a duty nobody is assigned to discharge.
- **(2) `changelog_ref`'s spec offered two locator forms neither of which receipts actually use.**
  The placeholder named `PR #N` or a short-sha; in practice, entries locate a `CHANGELOG.md`
  action by its quoted `### ` heading instead — all 8 live receipts in this repo's own
  `HANDOFFS.md` already use that form, and none use `PR #N` or a bare sha, without the spec ever
  blessing it. Added the quoted-heading form as a third explicit option and noted that a bare line
  number is not a durable locator once a ledger is ever trimmed or archived.
- **Distribution:** `HANDOFFS.md` is `bin/_manifest.py`-SEED (copied once, then adopter-owned), so
  new adopters receive the corrected spec; existing adopters' own copies are unaffected until they
  choose to re-seed.

### 2026-08-10 · [ad hoc] Documented and pinned the doc-only detection thresholds

- **Change:** `tools/methodology_dashboard.py` (+ `starter-kit/` twin, kept byte-identical) and
  `tools/test_methodology_dashboard.py`.
- **The defect:** `DOC_ONLY_SOURCE_LOC_MAX`, `DOC_ONLY_DOC_LOC_MIN` and `DOC_ONLY_DOC_FILES_MIN`
  are round numbers with no recorded derivation, and nothing asserted their values directly —
  `test_source_cap_boundary` exercises `DOC_ONLY_SOURCE_LOC_MAX` only indirectly, via hardcoded
  200/201 boundary literals, so that coverage would silently vanish if that fixture were ever
  rewritten to derive its boundary from the constant instead. `DOC_ONLY_SOURCE_LOC_MAX` in
  particular decides which of two scoring regimes a repo gets (a real 148-LOC repo the cap alone
  misclassified is documented near `FRAMEWORK_INSTALLED_DOCS`, ~100 lines below), so an accidental
  drift here is a user-visible verdict change, not cosmetic.
- **Fix:** added a comment recording that all three are deliberate, stated heuristics — not
  derived from a measured corpus of adopter repos — and a direct regression test
  (`test_doc_only_thresholds_are_pinned_not_left_to_drift`) asserting all three current values, so
  a future edit to any of them is a visible, deliberate decision.
- **Verified:** `python3 tools/test_methodology_dashboard.py` 198/198 (197 prior + this one).
  `DASHBOARD_VERSION` 2.10.2 → 2.10.4 in both twins (2.10.3 was skipped: #71 claimed it
  independently for an unrelated fix, and the constant's own "bump on any change" rule means two
  distinct changes cannot ship under one version); `test_dashboard_version` and
  `test_twins_byte_identical` updated/re-confirmed.
- **Distribution:** `starter-kit/methodology_dashboard.py` is `bin/_manifest.py`-TRACKED, so
  adopters receive the documented, pinned thresholds via `bin/sync`; `tools/` and
  `tools/test_methodology_dashboard.py` are canonical-only.

### 2026-08-10 · [ad hoc] Re-grounded the /caveman row's remaining unsupported claim

- **Change:** `starter-kit/RECOMMENDED_SKILLS.md`'s `/caveman` row.
- **The defect:** `15ccb38` (the "Discharged the three documentation follow-ons" entry below)
  removed a dangling `Learning #34` citation from this row but kept the claim it was
  attributing — "the methodology's own handoff length discipline" — which has no referent
  anywhere in this distributed corpus, and runs opposite to `SESSION_RUNNER.md`'s own failure
  mode #15 (the *thin* handoff is the failure, not the long one) and its Minimum Handoff
  Requirements, which gate on content, not length.
- **Fix:** re-grounded the row on those two verified, reachable sources instead — no length rule
  is stated because none exists to state.
- **Distribution:** `RECOMMENDED_SKILLS.md` is `bin/_manifest.py`-TRACKED, so adopters receive the
  fix via `bin/sync`.

### 2026-08-10 · [ad hoc] Resolved both review findings on [PR #66](https://github.com/KJ5HST/methodology/pull/66) — in the PR, not a follow-up

- **Origin:** rmsharp reviewed PR #66 and filed two findings, each reproduced against real repo
  state rather than theorised, with inline suggestions and an offer to take them to a follow-up PR.
  Fixed here instead, because finding 1 is a defect in code *this PR introduces* — shipping it
  would mean the failure-mode-#28 release note describes a gate that silently does nothing on the
  adopters most likely to want it. The v3.6 precedent is explicit: Layer 7 ran before Layer 6 so no
  release shipped with a known live defect in its own subsystem.
- **Finding 1 — `install_hook()` ignored `core.hooksPath`** (`starter-kit/context_budget.py`).
  It always wrote `<git-dir>/hooks/pre-commit` and printed "installed". `core.hooksPath` redirects
  git away from that directory entirely, and **this methodology's own `BOOTSTRAP.md` Step 10 tells
  adopters to set it** (`.githooks`) to enable the v3.1 ledger co-staging gate — so the population
  following our own setup instructions got a silent no-op with a success message. Reproduced end to
  end before the fix: a commit growing `CLAUDE.md` to 40,000 B against a 28,000 B ceiling was
  *created* rather than refused; after, the same commit is refused and `git rev-list --count`
  confirms none was created. A relative value now resolves against the worktree top level (what git
  itself does when running the hook), an absolute value is used as given, and the pre-existing
  "a hook is already here and is not ours" branch now fires correctly on a repo whose `.githooks/`
  already holds the ledger hook — reporting and refusing to clobber instead of shadowing it.
- **Finding 2 — receipt identity is `session` + `date`, not `session` alone** (`bin/check-handoff`).
  `validate_ledger()` asserted an invariant the format in `starter-kit/HANDOFFS.md` never states.
  `S<N>` is a per-sequence counter and one ledger may merge more than one sequence — a fork and its
  upstream each running their own — so two distinct sessions share an `S<N>` by construction;
  rmsharp reproduced four false positives on a real ledger. **The argument is not the false positive
  itself but what one does to a gate:** this very PR's thesis is that the dashboard printed
  `Large files detected` at every Phase 0 and 15+ sessions read past it. A checker that fires on a
  structurally valid file trains that same blindness on the checker we most need believed. Coverage
  lost is narrow — a block copied and not edited duplicates *both* keys and is still caught — and
  the cross-branch collision it appeared to guard was never guarded, since the checker sees one tree
  and could only ever fire after the merge landed. Code and spec now agree rather than the code
  being stricter: `starter-kit/HANDOFFS.md` states the rule, including that keeping `S<N>` unique
  within a sequence must never mean renumbering an already-written receipt.
- **Verification:** suite **107 → 112**. Both fixes were driven **RED first and observed failing**
  (Learning #12): 2 of the 4 new `install-hook` assertions fail against the unpatched tool (the
  other 2 are deliberate presence controls that must pass either way), and finding 2's new negative
  assertion fails with exactly the reported error, `duplicate session id 'S8'`, before passing. The
  duplicate-identity mutation was also strengthened to copy the S8 header wholesale, so it cannot
  quietly degrade into a session-only collision if a date later changes. The 2 remaining suite
  failures are pre-existing and reproduce on `main` with this branch's changes stashed
  (`tools/test_methodology_dashboard.py`, untouched here; and the GitHub-source dry-run, which needs
  network). `bin/check-links` OK (83 links / 21 files); live ledger green under `--all`.
- **Learning #10 caught one thing the diff could not:** `README.md`'s unreleased #65 bullet still
  claimed "unique session ids". Dated `CHANGELOG.md` entries describing what #65 shipped are left
  verbatim per the v2.7.1 frozen-record precedent; the unreleased What's New bullet describes
  current behaviour and was corrected.
- **Not recorded as a Learning row by design.** The candidate — *a checker's invariant must not be
  stricter than the format it validates; the adopter who trips it is the one who finds out* — is
  real, but `#14` is reserved by `docs/operator-gated-review-plan`'s decision D3. Appending it here
  would create exactly the collision D3 exists to prevent. It is carried in the S10 receipt instead,
  to be appended at the first free number after that branch merges.
- **Commits:** `eacb516` (1B claim) · `14bd88a` (finding 1) · `63e1dcf` (finding 2).

