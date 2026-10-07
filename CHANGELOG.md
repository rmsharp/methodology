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

---

## 2026-09

## 2026-10

### 2026-10-06 · [BL-101] S276 — evidence of P3 (1 of 2): the old proofs and the reverify verdicts did not move (`trim-reverify-differential.sh`, `frozen-proofs-after-p3-output.txt`)

Run against committed `a0dd245`'s predecessor tree (the trimmer layer, `ee89b24`). **`trim-reverify-differential.sh a9fef63`:** for each of the 119 tracked shards in `docs/archive/`, `--reverify` by the previous tool (`a9fef63`, 1.7.0) and by the current one (1.8.0): 119 of 119 give the same exit code and the same output once the version is normalised (previous exit 0 to 0 x114, 1 to 1 x2, 3 to 3 x2, 4 to 4 x1). **`frozen-proofs.sh`** (the plan's own script, unchanged) read 120 frozen proofs in each of its three trees (nothing moved, the ledgers moved, the archive moved too): **115 exit 0 and 5 exit 1 in all three, 0 differing between trees**, the five being the August shards the plan already named (`CHANGELOG-through-2026-08-02`, `-08-09`, `HANDOFFS-through-2026-08-02`, `-08-09`, `-08-25`). The plan's figure was 117 proofs (112 and 5); three shards have been trimmed since, and the criterion is that the red set does not change, which it did not. A frozen proof is a standalone script that does not import the tool, so the second result could not have moved by a tool change; the first is the one that could, and did not. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S276 — the close-out report resolves its ledger through the layout resolver (P3, layer 2; `close_out_report.py` 1.2.0)

`starter-kit/close_out_report.py` found `HANDOFFS.md` by a literal at three sites (coupling C10). It now embeds the resolver block (asserted byte-identical, scanner rows 3 to 0) and asks for the framework-anchor tiebreak: `--ledger` defaults to the project's own ledger, found from the repository's TOP so a run from a subdirectory works, `live_facts` and the Stop / SessionStart hook read the same path, and the block message's command names the resolved ledger (`--ledger <path>`). A half-migrated tree is refused by the CLI naming both copies (exit 2) and is quiet in the hook, which only ever adds a message and cannot say which ledger to read. `tools/test_close_out_report.py` 68 to 82 tests; the new ones were run against the old tool and 10 of 13 went red (the three that stayed green are the legacy controls, which must pass on both); 8 mutants killed after the one existing mutant whose anchor line this change removed was re-pointed at the new line (my first mutant run was contaminated by that red baseline, and I re-ran it clean). The install snippet (a settings.json hook command) is not in the manifest and names no path in this file. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S276 — the trimmer writes and proves a trim of a ledger under methodology/ (P3, layer 1; `methodology_trim.py` 1.8.0)

`starter-kit/methodology_trim.py` derives where a shard goes and how a link is rebased from the DIRECTORY of the ledger being trimmed (`layout_for`, coupling C7). A root ledger keeps `docs/archive/` and the two-level prefix and writes what 1.7.0 wrote: **measured**, the same trim by the old and the new tool in two `--no-local` clones differs only in the version string and the proof's two parameter lines, and four dry runs on the real ledgers are identical. A ledger under `methodology/` writes `methodology/archive/` (D5), links climb one level, and a link target that already starts with `../` is ordinary there (a project file is exactly such a link), so the rebase stays invertible; the proof template gained two parameters (`PREFIX`, `PARENT_LINKS`) and its tool and document names became placeholders. The action ledger is found by the embedded resolver with the tiebreak (the block is asserted byte-identical, scanner rows 20 to 0), a half-migrated tree is refused by name (`LAYOUT_HALF_MIGRATED`), pointer-block and ledger-entry links are written against the ledger's own directory, the trigger reads the shards of both archive directories, a shard name is never reused across them, and a ledger under `methodology/` earns the Class A arm. `--reverify` needed no new lift. `tools/test_methodology_trim.py` 181 to 218 tests (the new classes ran RED first: 30 of 31 failed), a frozen copy of the 1.7.0 proof template is the differential fixture, 22 mutants all killed (19 at once, three survivors each named a missing test: a name taken in its own directory, a `../../` link in the new layout, a footer rebased one level). Not shown: a trim at a real adopter's own history; the 117 old proofs and the reverify differential are re-run in the next entry. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S276 — the ledger hook decides a tie by the framework anchor, read from the index (P3, layer 0b)

The hook's sh form of the row in `6907f00`. With the ledger tracked at the root and under `methodology/`, a tracked `methodology/SESSION_RUNNER.md` and no tracked root runner make `methodology/CHANGELOG.md` the ledger: the root file is the project's own and is not gated, and the never-edit check applies to the ledger only. Any other tie is still refused naming both, and the message now says how to resolve it where it used to call it an open question. The runner is read from the INDEX, never the worktree. `.githooks/pre-commit --selftest` 34 → 43 checks, RED first (the two passing probes failed); 7 hook mutants killed, one (the worktree read, H7) only after a probe for a runner that is on disk but untracked was added. `bin/tests.sh` Test 54: three assertions through the real hook and real git (a tie the anchor decides passes with its ledger entry, a commit touching only the root product changelog is refused naming `methodology/CHANGELOG.md`, a tie with two runners is refused naming both), the old half-migrated control's pattern follows the changed line (it would have gone vacuous), three new controls; Test 54 alone read 21 passed, 0 failed. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S276 — the resolver's tiebreak row: the framework anchor decides a tie, on request (P3, layer 0a)

His S275 close-out decision, built in `tools/layout_resolver.py`: `resolve_layout(root, anchor, tiebreak=False)`. With `tiebreak=True`, a file found in both places resolves `new` when the runner (`SESSION_RUNNER.md`) is under `methodology/` and not at the root, and `found` still names both; every other tie stays `half`, the runner at the root or at both included. **It is opt-in on purpose:** plan section 4.1 frees only the root changelog for a project's own product file, and the ratchet's manifest does not ask, so a second `.quality-gates.json` is still refused (a stale copy, not the project's own). That reading is mine and he may overrule it. The copy embedded in `starter-kit/quality_ratchet.py` was replaced from the module, and the layout suite asserts it byte-identical. `tools/test_layout_resolver.py` 65 → 72 tests, RED first (9 errors, the keyword did not exist); a guard I first wrote (`anchor != SESSION_RUNNER.md`) was deleted as redundant before this commit, because the inner resolve already answers `half` for it; 7 mutants against the row, all killed. Quality ratchet suites: ratchet 75 OK, selftest 25 checks OK. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S276 claim (in progress) — build the trimmer and the close-out report layer: both resolve their ledger in either layout (P3)

CHANGELOG: pending. Operator said `go`; at the Phase 0 picker he chose BL-101 P3 (the plan's recommendation, S275's next step 1). The deliverable is the plan's section 7.2 row P3, built in this session, after the tiebreak row he decided at the S275 close-out (the framework anchor decides: a project whose `SESSION_RUNNER.md` is under `methodology/` keeps its ledger there whatever sits at the root), which P3 starts by adding to the resolver, its tests, the P1 block and the P2 copies (the hook's sh form included). Then: `methodology_trim.py` derives `ARCHIVE_DIR` and the rebase prefix from the ledger's directory, a trim in the new layout writes a shard and a proof that pass, all 117 old proofs keep the histogram 112 green / 5 red; `close_out_report.py` resolves its ledger and its snippet names the resolved path. No other shipped tool changes; the scanner stays RED and is not a gate until P6. Already done before this claim, each recorded below: the push and the ref deletion (two go-aheads he gave at the picker), the owed `HANDOFFS.md` trim (`83bb2a3`, S273 to `HANDOFFS-through-2026-10-06-4.md`, proof exit 0 by name from a `--no-local` clone) and its fold (`837a254`). Phase 3F records the rest. Model: Claude Sonnet 5.5.

### 2026-10-06 · [ad hoc] S276 — fold the fourth 2026-10-06 HANDOFFS shard pointer into the archive index

The pointer block the trim (`83bb2a3`, 1 receipt, S273, 2026-10-06, to `HANDOFFS-through-2026-10-06-4.md`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, trimmer v1.7.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S275, S274), both the fork's. The shard's `.verify.sh` was run by name from a `--no-local` clone of `83bb2a3`: exit 0, `records: 3 before = 2 retained + 1 archived`, L1, L2/front-matter and L3 hold. This is the trim S275's receipt named as owed after the S276 Phase 0 report, taken before the session's claim. Model: Claude Sonnet 5.5.

### 2026-10-06 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-06-4.md` (1 record(s), 36,495 B → 27,293 B)

**Written by:** `methodology_trim.py` v1.7.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-06 → 2026-10-06) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-06-4.md`](docs/archive/HANDOFFS-through-2026-10-06-4.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-06-4.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-06-4.md.verify.sh)
rather than trusting a digest printed here. Live file 36,495 B → 27,293 B (−25.2%).

### 2026-10-06 · [ad hoc] S276 — fork `main` pushed to `origin` (`ecbde74`) and the local backup ref `pre-resync-2026-10` deleted

At the S276 Phase 0 picker he granted both, as two selections. **Push:** `git push origin main` sent exactly one commit, `58bb713..ecbde74` (the S275 decision record, five files); `origin/main...main` read `0 1` before and `0 0` after a fresh fetch. **Ref:** `git branch -d pre-resync-2026-10` (was `9904a0a`, the S270 claim of the BL-95 resync); that commit is an ancestor of both `main` and `origin/main`, so no commit was lost, and the safe form of the delete refuses an unmerged branch. Nothing went upstream. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S275 — the framework anchor decides: his decision at the close-out picker, recorded (plan section 7.2a, BL-101, the receipt)

Asked at the close-out picker how the resolver should break the tie when a project's own product changelog sits at the root beside a moved ledger (the hook and the ratchet read that tree as half-migrated and refuse until `--no-verify`), he chose **the framework anchor decides** (the recommendation): a project whose `SESSION_RUNNER.md` is under `methodology/` keeps its ledger there whatever sits at the root; both ledgers tracked with no runner under `methodology/` stays refused. **Recorded, not built:** `docs/planning/methodology-subdirectory-plan.md` section 7.2a now reads *Decided* (59,561 B of 60,000 B), `BACKLOG.md` BL-101's row and `BACKLOG-DETAIL.md` read the same and name the build as P3's first step (the resolver's table, its tests, the P1 block, the P2 copies of it in the ratchet, and the hook's sh form), and the S275 receipt's next-steps (2) and (4) now say decided and pushed. The decision changes nothing that ships today: the hook and the ratchet still refuse both-tracked, which is the safe state until P3. This commit is local (the plan and backlog are outside the push-record grant), so `git rev-list --left-right --count origin/main...main` should read `0 1`; its push is his go-ahead. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S275 — fork `main` pushed to `origin`: the twelve S275 commits

On his go-ahead at the close-out picker ("Push main now"), `git push origin main` took `rmsharp/methodology` `main` from `51be1a5` to `63d4a16`: a plain fast-forward (`origin/main` an ancestor of `main`, 0 behind, exactly twelve ahead, a clean tree, each re-measured after a fresh fetch immediately before sending), no force, no other ref; nothing went to `KJ5HST/methodology`. **Read back** after a fresh fetch: `git rev-list --left-right --count origin/main...main` = `0 0`, `git ls-remote origin refs/heads/main` = `63d4a16`. The twelve commits: the `HANDOFFS.md` trim and its fold, the claim, the four P2 layers (the ratchet's resolution, the ratchet's move handling, the ledger hook, the scanner rows), the assertion fix, the floors, the plan, backlog and CLAUDE.md update, the runtime check, the close-out. The S275 receipt's next-step (4) predicted `0 12`; it read `0 12` before this push and reads `0 0` now. This recording commit, a `CHANGELOG.md`-only change, is pushed too under the standing grant for push records, so no further record is owed. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S275 close-out — P2: the ledger hook and the ratchet accept either layout, and X2 is a permanent test

The deliverable (the plan's section 7.2 row P2, a build session) is done and recorded in the entries above, one per action: the owed `HANDOFFS.md` trim (`d20af5d`) and its fold (`6f85b46`), the claim (`0c4de80`), four layers (`eba958a`, `215e18e`, `42a1084`, `2fa2d34`), the fix to the one assertion layer 3 left red (`6249ed9`), the raised floors (`c535b11`), the plan, backlog and `CLAUDE.md` (`3f29589`) and the runtime check (`884bd28`). The `HANDOFFS.md` receipt is complete (self 8, predecessor 9: all 23 of S274's cited lines held; its one stale item was the push, already done after its close-out). Final gate run on `884bd28` at three receipts: **14/14**, results `58667908a831`, manifest `62db6db9ee88`, `tests-sh-passed` 468 against the floor 462. No fork learning row appended, so the retirement duty of D3 does not arise; rows considered: #12, #58, #68, #70, #81, #107. **Next:** P3 (the trimmer and the close-out report), a build session; the open decision of plan section 7.2a is his, before P7; the push of these twelve commits is his go-ahead; a `HANDOFFS.md` trim is owed after the next Phase 0 report (3 receipts). Nothing was sent upstream and no adopter was touched. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S275 — runtime check of P2: the plan's own X2 script, re-run at `3f29589`, refuses the later commit it used to pass

Phase 3E for a change to a hook. `bash docs/planning/methodology-subdirectory-evidence/hook-after-move.sh` (two throwaway `--no-local` clones of HEAD with `core.hooksPath .githooks`, the real hook, real git, nothing in this tree touched) read: **C** (unmoved ledger, a later commit) exit 1, refused; **X1** (the move commit itself) exit 0, passes, as before; **X2** (a later commit after the move) **exit 1, refused, `✗ methodology/CHANGELOG.md not staged`**, where S273 recorded exit 0 ("the ledger gate fails open"). The output is kept as `hook-after-move-after-p2-output.txt` beside the original; the plan's section 11 row says both. Every commit of this session since `42a1084` also passed through the new hook live (the ledger gate and the ratchet chain). Not verified: a hook armed in a real adopter's clone, which is P7's and each adopter session's. Nothing outward. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S275 — the plan records P2; BL-101 reads P2 done, P3 next; CLAUDE.md's tools row

`docs/planning/methodology-subdirectory-plan.md` gains §7.2a (59,304 B of its 60,000 B budget: 696 B left, so P3 onward must cut before it adds): what P2 built, what was measured red before it (11 of Test 54's 15 against the old hook), the corrected counts, the one defect of mine the measure caught (the hook layer left a `bin/tests.sh` assertion red; no commit hook runs the suite), what P2 settled for the operator to overrule (both ledgers tracked is refused, as §4.3 says; both archive directories accepted now), and **one open decision**: §4.1 promises a project's root `CHANGELOG.md` is free for a product changelog, but the table anchored on `CHANGELOG.md` reads that project as half-migrated, so its hook would refuse every commit until `--no-verify`; the recommended fix is a tiebreak the P1 resolver does not have (the framework anchor decides); to be settled before P7. The plan's status line reads P0-P2 done, P3 next. `BACKLOG.md` BL-101's row and `BACKLOG-DETAIL.md`'s body read P2 done and name P3 as the next action (the trimmer and the close-out report, with the two test lists each phase appends to). `CLAUDE.md`'s tools row says the scanner reads 140 sites and that the hook and the ratchet read 0. Mutant tally corrected in the plan before it was committed (44, not the 30 I first wrote). No tool changed. Nothing outward. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S275 — the floors raised after P2: `tests-sh-passed` 447 → 462, `ratchet-unit-tests` 45 → 75, `layout-unit-tests` 62 → 65

Measured, not derived, in a `--no-local` clone of `6f85b46` (two receipts, the at-rest state) with the session's code files overlaid: `quality_ratchet.py --run` read 75 and 65 for the two unit suites, and `bash bin/tests.sh` captured to a file read **462 passed, 0 failed, 6 skipped** after `6249ed9` (its first run read `tests-sh-failed` 1, named and fixed above). Tightening only; the ratchet's own `--precommit` read the staged change exit 0. The three-receipt reading, which is what the tree shows mid-claim, is 468 / 0 / 0, so a floor is never taken from a three-receipt run. The note key `_s275_tightening_bl101_p2` in the manifest carries the same account. Nothing outward. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S275 — fix the one assertion the hook layer left red: the hook is no longer greppable as one literal line

`bin/tests.sh` asserted `.githooks/pre-commit chains the quality ratchet before the ledger gate` by grepping the hook for the literal `quality_ratchet.py" --precommit`. The hook layer (`42a1084`) builds that path from variables now (the tool is found under `starter-kit/`, under `methodology/` or at the root), so the grep failed: **`42a1084` and `2fa2d34` left the suite at 1 failed.** The commit hooks do not run the suite, and none of the suites I ran in the working tree (ratchet, layout, the hook's selftest, Test 54 extracted alone) contains this assertion; the two-receipt clone's gate run found it (`tests-sh-failed` 1) and a captured re-run named it (`FAIL: .githooks/pre-commit does not run quality_ratchet.py --precommit`). The assertion now says what its label always claimed and its grep never checked: the chain line exists, the tool is named, and the chain comes **before** the ledger gate (line 264 against 267). Test 54 runs the chain for real in both layouts. Measured in a `--no-local` clone of `6f85b46` (two receipts) with the five code files overlaid: **462 passed, 0 failed, 6 skipped** (447 + Test 54's 15). Nothing outward. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S275 — the ratchet's scanner rows worked to zero, and a test that keeps the resolved tools there (P2, 4 of 4: the scanner)

`bin/check-layout-literals` read `starter-kit/quality_ratchet.py` at 16 sites at the start of P2 and 12 after its behaviour changed; the remaining 12 were the tool's own file name and the manifest's, in messages, in the installer's check and in the selftest's copy. They are now two constants carrying a reasoned `# layout: ok` marker (`TOOL`, and `SAFEGUARDS` for the one document a message cites by bare name, which the runner's convention of section 4.4 keeps true) and the messages use them, so the tool scans at **0** sites and the hook at 0 (it read 21). The scanner's total is **140 sites in 17 files** (was 177 at P1), the rest in the dashboard, the trimmer, `check-handoff`, `close_out_report.py`, `context_budget.py` and `bin/sync`, which are P3-P6's. `tools/test_layout_resolver.py` gains `TestToolsAlreadyResolvedStayAtZero` (65 tests): the scanner is not a gate until P6, so this is what stops a later edit putting a root literal back, and each phase appends the tools it resolves. **Mutants:** 2, both killed (a marker that loses its reason acknowledges nothing; a bare literal back in a message); the first mutant I wrote was wrong (the marker pattern tolerates extra spaces) and survived, and was replaced, not counted. No behaviour change: the ratchet suite reads 75 OK and `--selftest` 25 checks. Nothing outward. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S275 — the ledger hook follows the ledger under `methodology/`: X2 is a permanent test (P2, 3 of 4: the hook)

`.githooks/pre-commit` reads where the ledger is from the **index** with git (the resolver's four-row table anchored on the ledger; the hook is sh and cannot call the Python block): a ledger at the root or under `methodology/` is the gate, both tracked is refused naming both (exit 1; the message says that a product changelog beside a moved ledger reads as this state too, which is an open question of the plan, not a mistake of the committer), neither tracked keeps the old 'no ledger, never block' branch. The never-edit check crosses a move (HEAD's copy is read from wherever HEAD kept the ledger, so a commit that renames the ledger and rewrites an entry is refused), a trim may stage its shard under `docs/archive/` **or** `methodology/archive/` (D5 moves it with the ledgers; P3 will write there), and the ratchet chain finds the tool at `starter-kit/`, `methodology/` or the root and the manifest at the root or under `methodology/`, in the worktree or at HEAD. Measured before the change (the old hook against the new Test 54): X2 passes in the new layout (exit 0, wanted 1), a loosened floor passes in the new layout, a move that lowers a floor passes, a move that rewrites a ledger entry passes, a half-migrated tree passes. **The selftest** goes from 17 to 34 checks and now counts them (its summary line said 17 as a literal): the new-layout X2 and its co-staged pair, tier 1 (framework files moved, ledger still at the root), a ledger in both places, a same-named file elsewhere, the ledger deleted from the index (the documented opt-out), the very first commit of a repository, the lifecycle probes in the new layout, a trim under either archive directory, and four move commits. **`bin/tests.sh` Test 54** (15 assertions, new) runs X2, the loosened floor and the move through the real hook and real git in both layouts, with 5 controls: four hook mutants that must turn the selftest red on a named probe, and a chain guard that names the root manifest only, which PASSES the loosened floor. **Mutants:** 14 over the hook's gate, 13 killed at first and the survivor (no ledger at HEAD falls through to `git show HEAD:`, which fails only when there is no HEAD) named the first-commit probe; all 14 killed. The scanner reads the hook at 0 sites (was 21). Not done: the floors, the scanner's rows for the ratchet, the plan's record, the documents that name the hook's behaviour (`SAFEGUARDS.md`, `BOOTSTRAP.md`, P9). Nothing outward. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S275 — the ratchet judges a move, in git and through its own hook (P2, 2 of 4: the comparison across the move)

`quality_ratchet.py --precommit` reads the manifest from the index and HEAD at **either** path (`manifest_blobs`) and walks the history of **both** (`newest_committed`), so a pure move passes (it read as 'manifest removed' and was refused), a threshold lowered **inside** the move commit is refused with its own reason (`floor lowered 80 -> 70`), a loosening at the new path after the move is refused (it **passed**: C4's fail-open, measured by `test_a_loosening_at_the_new_path_after_the_move_commit_is_refused`), the base is the newest declaration at either path, and a tree that holds the manifest in both places is refused naming both (exit 2; `--run`, `--status` and `install-hook` already stop at exit 3 for it). A history commit that holds both layouts is skipped as an unparseable one is, and HEAD's copy is not trusted when it holds both (the note says so). The installed hook now execs the tool where it was installed **and at its twin in the other layout** (root <-> `methodology/`; `starter-kit/` has none), and a hook whose tool is nowhere prints what is missing and refuses (exit 2) instead of a Python 'can't open file'. `--selftest` gains three checks (25). **RED first:** 16 of 19 new tests failed against the layer-1 code (the three that passed were two controls and one that passed for the wrong reason, tightened to assert the gate's name and then red). **Mutants:** 16 over this layer, 13 killed at first; the 3 survivors named three missing tests (the walk over the new path alone, a both-layouts commit in the history, an ambiguous HEAD copy), two tests were added, and all 16 are killed. `tools/test_quality_ratchet.py` 53 -> 75. **Still owed:** the `.githooks/pre-commit` ledger gate in the new layout (X2), the floors raised after measuring, the scanner's rows for the two files, and the plan's record of P2. Nothing outward. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S275 — the ratchet reads its manifest in either layout (P2, 1 of 3: the resolution)

`starter-kit/quality_ratchet.py` 1.1.0 → 1.2.0 embeds the resolver block (byte-identical to `tools/layout_resolver.py`, asserted by the new `TestEveryEmbeddedCopyIsByteIdentical`, which also fails if any other shipped tool carries the markers without being listed) and resolves the manifest with itself as the anchor: `manifest_location` reads the four-row table, `find_root` finds a manifest under `methodology/` and returns the project above it (a repository that is merely *named* `methodology`, like this one, stays its own root: git names the toplevel), `--run` and `--status` write and read the results file beside the manifest wherever it lives (an explicit `results_file` is still relative to the root), and a half-migrated tree is a usage error (exit 3) that names both paths and runs nothing. **RED first:** 6 of the 8 new tests failed against 1.1.0 and the other 2 are the controls (legacy results at the root, a repository named `methodology`). **Mutants:** 12 over the resolution layer, 12 killed (one anchor missed on the first try and was re-run). `tools/test_quality_ratchet.py` 45 → 53, `tools/test_layout_resolver.py` 62 → 64, the stdlib allow-list gains `pathlib` (the block's import). **Not in this entry, owed by the next two layers:** the pre-commit comparison across a move (the base walk over both paths, a move that loosens, a pure rename, the hook text), the `.githooks/pre-commit` ledger gate in the new layout, the raised floors. Nothing outward. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S275 claim (in progress) — build the gate layer: the hook and the ratchet accept either layout (P2)

CHANGELOG: pending. Operator said `go` as the first message; at the Phase 0 picker he chose BL-101 P2 (the plan's recommendation, S274's next step 1). The deliverable is the plan's section 7.2 row P2, built in this session: the pre-commit hook and `quality_ratchet.py` resolve the layout through the embedded resolver block, a later content commit with no ledger entry is refused in the new layout (X2, a permanent test), a move commit that lowers a threshold is refused, a pure rename passes. No other shipped tool changes and the scanner is not wired into the gate (P6). Already done before this claim, each recorded above: the owed `HANDOFFS.md` trim (`d20af5d`, S272 to `HANDOFFS-through-2026-10-06-3.md`, proof exit 0 by name from a `--no-local` clone) and its fold (`6f85b46`). Phase 0: 0 undocumented commits at both frontiers, 0 merges; #94, #92 and #93 without a maintainer reply; `quality_ratchet.py --run` 14/14, results `b6257eb2d9a8`, manifest `f6fc74380013` (S274's citation exactly); dashboard health 72 (read through `collect_all`, nothing written); `origin/main` = `main` (`0 0`) before the trim. Phase 3F records the rest. Model: Claude Sonnet 5.5.

### 2026-10-06 · [ad hoc] S275 — fold the third 2026-10-06 HANDOFFS shard pointer into the archive index

The pointer block the trim (`d20af5d`, 1 receipt, S272, 2026-10-06, to `HANDOFFS-through-2026-10-06-3.md`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, trimmer v1.7.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S274, S273), both the fork's. The shard's `.verify.sh` was run by name from a `--no-local` clone of `d20af5d`: exit 0, `records: 3 before = 2 retained + 1 archived`, L1, L2/front-matter and L3 hold. This is the trim S274's receipt named as owed after the S275 Phase 0 report, taken before the session's claim. Model: Claude Sonnet 5.5.

### 2026-10-06 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-06-3.md` (1 record(s), 36,151 B → 25,945 B)

**Written by:** `methodology_trim.py` v1.7.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-06 → 2026-10-06) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-06-3.md`](docs/archive/HANDOFFS-through-2026-10-06-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-06-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-06-3.md.verify.sh)
rather than trusting a digest printed here. Live file 36,151 B → 25,945 B (−28.2%).

### 2026-10-06 · [BL-101] S274 — fork `main` pushed to `origin`: the ten S274 commits

On his go-ahead at the close-out picker ("Push main to origin now"), `git push origin main` took `rmsharp/methodology` `main` from `d0f2775` to `ad5fd82`: a plain fast-forward (`origin/main` an ancestor of `main`, 0 behind, exactly ten ahead, a clean tree, each re-measured immediately before sending), no force, no other ref; nothing went to `KJ5HST/methodology`. **Read back** after a fresh fetch: `git rev-list --left-right --count origin/main...main` = `0 0`, `git ls-remote origin refs/heads/main` = `ad5fd82`. The ten commits: the `HANDOFFS.md` trim and its fold, the claim, the four P1 layers (resolver, fixtures, scanner, wiring and gate), the plan with its evidence, the backlog and CLAUDE.md update, the close-out. The S274 receipt's next-step (3) predicted `0 10` before this push; it now reads `0 0`. This recording commit, a `CHANGELOG.md`-only change, is pushed too under the standing grant for push records, so no further record is owed. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S274 close-out — P1: the layout resolver, the fixture trees in both layouts and the RED literal scanner

`CHANGELOG: pending` on the S274 claim entry is cleared (by this statement: the never-edit gate forbids editing a committed entry). **Deliverable:** BL-101 P1, plan §7.1: `tools/layout_resolver.py`, `tools/layout_fixtures.py`, `bin/check-layout-literals` and `tools/test_layout_resolver.py` (62 tests, 40 mutants killed, wired into `bin/tests.sh`, gate `layout-unit-tests` at 62, `tests-sh-passed` 446 to 447), with the plan's, the backlog's and CLAUDE.md's updates. No shipped tool changed; the scanner is RED on purpose (177 sites in 12 files) and is not a gate until P6. **Gate:** `quality_ratchet.py --run` on `b14a1c8`: 14/14, `tests-sh-passed` 453 at three receipts against the floor 447, results `b6257eb2d9a8`, manifest `f6fc74380013`, identical to the run on `2ea5d68`. **Receipt:** `HANDOFFS.md` S274 complete (self 8, predecessor 8; 10,964 B against the 12,288 B record budget: the first draft was 14,099 B, `bin/check-handoff` refused it in default mode, and it was cut before this commit). **Commits this session:** the push of `b162866` and its record `d0f2775` (both on `origin`), the owed trim `e04c5e0` and its fold `078a6cc`, the claim `db1f1ef`, the four P1 layers `71e0d30` `6d2b5cb` `cbf674c` `2ea5d68`, the plan and evidence `8614b87`, the backlog and CLAUDE.md `b14a1c8`. **Waiting on the operator:** the push of this session's nine work commits and this close-out (they carry code, so each push is his go-ahead); PR #94, PR #92 and issue #93 have no maintainer reply (a reply ranks above everything). Nothing else was sent outward. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S274 — BL-101 reads P1 done, P2 next; CLAUDE.md's tools table lists the new files

BL-101's index row in `docs/planning/BACKLOG.md` and its body in `BACKLOG-DETAIL.md` now say P1 is done (the resolver, the fixtures, the scanner at 177 sites, 62 tests, 40 mutants killed) and name P2 as the next action with its first steps (embed the resolver's block and assert it with `embedded_block`; the hook's and the ratchet's rows come from the scanner's list; X2, a later commit with no ledger entry refused in the new layout, is a permanent test). The item stays open: 22 to 29 sessions by the plan, P1 is one. `CLAUDE.md`'s Tools table gains one row for `tools/layout_resolver.py`, `tools/layout_fixtures.py`, `bin/check-layout-literals` and `tools/test_layout_resolver.py` (canonical-only; the scanner RED on purpose and not a gate until P6), +518 B, 15,547 B against the file's 16,000 B warn line and its 18,600 B ceiling. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S274 — the plan records P1: the resolver's anchor, the scanner's real counts, and a suite criterion that names its receipt state

`docs/planning/methodology-subdirectory-plan.md` (56,447 B against its 60,000 B budget) is brought to what P1 measured. **(1) The anchor:** §4.3 now says the four-row table is keyed on a caller-supplied anchor file, `SESSION_RUNNER.md` by default and `CHANGELOG.md` for a state file, because §4.6 calls a tier-1-only adopter (framework files moved, ledgers still at the root) a coherent end state and a tool that found the ledger through the runner's directory would look for a file that is not there (C5 again). **(2) The counts:** the first per-tool figures (51 in the dashboard, 13, 6, 7, 3) came from one grep that could not be reproduced; C8, §7.1 and §10 now carry the scanner's (79, 20, 21, 8, 3; 177 in all over 12 files). **(3) The suite criterion:** §3.1, §7 and §8 stated `passed ≥ 452, failed 0, skipped 0` as absolutes, but that triple is the **three-receipt** baseline: Test 34 prints six stated SKIPs below three receipts, so the unmoved tree reads **447 / 0 / 6 at two receipts and 453 / 0 / 0 at three** (both measured this session). A phase that starts just after a trim, which is every session that follows a close-out, would have read the six skips as a move's silent skips, or taken the wrong baseline; the criterion is now the unmoved tree's own triple compared in the same receipt state (fork Learning #70 is this lesson, which the plan had not applied to itself). **(4)** P1 is marked done, P2 next, and §11 lists the new evidence file. `docs/planning/methodology-subdirectory-evidence/layout-literals-output.txt` is the scanner's recorded RED output at `2ea5d68`: 177 site rows, exit 1 read bare, re-run with `python3 -B bin/check-layout-literals`. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S274 — the suite wired into `bin/tests.sh` and its gate declared (P1, 4 of 4): `tests-sh-passed` 446 -> 447, `layout-unit-tests` 62

`bin/tests.sh` runs `tools/test_layout_resolver.py` beside the other unit suites (one pass or one fail, like its neighbours), and `.quality-gates.json` gains the gate `layout-unit-tests` (a floor of 62, extracted from `Ran 62 tests`) and the floor `tests-sh-passed` 446 -> 447, with a note (`_s274_tightening_bl101_p1`) in the file's own convention. **The 447 is measured, not derived:** `bash bin/tests.sh`, output captured to a file, in a `--no-local` clone of `078a6cc` (the commit after the trim and fold, `HANDOFFS.md` at the two receipts this floor is set in) with this session's five code files overlaid: `447 passed, 0 failed, 6 skipped`, exit 0 (the six are Test 34's stated SKIPs), the new row passes, and Test 31 compared 666 with 666, so it is not vacuous. The one new pass is the wired suite; a three-receipt tree reads six higher, so the next gate run on this tree should read 453. **The scanner is deliberately not a gate**: it is RED on this repository (177 sites) until P6 wires it at zero, and the wired suite tests the scanner on scratch trees, never over the live tree (a test asserting that the repository is RED would block the phases whose job is to turn it green). A gate added is a tightening, which the ratchet hook accepts. No shipped tool changed. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S274 — the literal scanner `bin/check-layout-literals` (P1, 3 of 4): RED on this tree, 177 sites in 12 of 17 files, 62 tests, 22 mutants killed

**What it is.** `bin/check-layout-literals` (canonical-only, executable, not a declared gate) lists every line of a shipped tool that names a methodology file at a root path: starter-kit/*.py, every script in `bin/`, `.githooks/*`, and the dashboard twin when it differs. A *site* is a string constant in code (Python, read with `ast`) or the non-comment part of a shell line holding a methodology file name (the 30 manifest destinations plus the 4 generated files) or the directories `docs/methodology`, `docs/archive` and a hard-coded `methodology/<name>`; each is shaped `path` (a constant with no whitespace) or `text` (a message or command), a triage hint. **Not sites:** prose (a name in a comment or docstring: counted, listed with `--all`), the resolver's marked block, a name behind a canonical-source directory (`starter-kit/`, `tools/`, `workstreams/`, `docs/planning/`, also written as a join, `/ "starter-kit" / "NAME"`), a URL, a longer name that merely contains one, and a site acknowledged by a same-line `# layout: ok -- <reason>` marker (a marker with no reason acknowledges nothing). Exit 0 none, 1 sites, 2 nothing scanned or a file that does not parse, so a wrong `--root` cannot read green. `bin/_manifest.py` (the table) and `bin/tests.sh` are not scanned, and say so.

**The RED run (the plan's verify step):** `python3 bin/check-layout-literals` exits 1: scanned 17 files, **177 sites** (109 path, 68 text), 1 acknowledged (the scanner's own search pattern), 202 prose lines not counted. By file: dashboard 79, pre-commit hook 21, trimmer 20, ratchet 16, `bin/model-report` 13, `bin/check-handoff` 8, `context_budget.py` 8, `bin/check-ledger` 4, `bin/status` 3, `close_out_report.py` 3, `bin/check-links` 1, `bin/check-overhead` 1. **The plan's figures were not reproduced:** it gave 51, 13, 6, 7 and 3 for the dashboard, trimmer, hook, `check-handoff` and `close_out_report.py` from "one grep"; no pattern I tried returns them (a plain name grep gives 153 lines in the dashboard), and the scanner's definition gives 79, 20, 21, 8 and 3, so only `close_out_report.py` agrees. The scanner's count, with its definition written in its docstring, replaces the plan's. **Not in the list, correctly:** `bin/sync` and `bin/_manifest_reader.py` hold no literal (they read the manifest).

**How it was checked.** RED first (the suite failed on the absent script), then 62 tests over synthetic trees. **Reading the first real run found three flaws in the instrument before anything was committed:** a join like `repo_root() / "starter-kit" / "FRAMEWORK_LEARNINGS.md"` was flagged because the directory is its own constant; shell text such as `methodology_trim.py's job` read as a `path`; and `docs/archive` was excluded as canonical although every adopter's trim writes shards there (plan C7). The first scan of the dashboard also took 90 seconds (`ast.get_source_segment` re-splits the file on every call) and now takes about a second. **Mutants:** 22 of 22 killed, after two survived and gained tests (a URL naming a methodology file; a longer name such as `BACKUP-CHANGELOG.md`). **Known limit:** the shape of a shell site is a heuristic, and a name inside a heredoc is a site because the scanner does not model heredocs. Nothing wired: P6 puts it in `.quality-gates.json` at zero. No shipped tool changed. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S274 — the fixture trees in both layouts (P1, 2 of 4): five shapes built from the manifest, 12 more tests, 10 mutants killed

`tools/layout_fixtures.py` (canonical-only) writes one of five shapes into an empty directory: `legacy` (the manifest's destinations as they are), `new` (the plan's §4.1: every methodology file one level down in `methodology/`, `workstreams/` the one subdirectory), `tier1` (the manifest's TRACKED rows moved, the SEED rows, generated files and archive still at the root: §4.6's coherent end state, the shape that needs the second anchor), `half` (legacy plus a second runner under `methodology/`) and `empty`. It derives from `bin/_manifest.py`, so a file the manifest gains reaches the legacy shape by itself, while `tools/test_layout_resolver.py` holds §4.1 typed out as literals (34 files, none at the root) so a manifest change cannot also reshape the target silently. **Faithfulness (gate d), measured:** `bin/sync --source=local` into a scratch git project writes exactly the 30 manifest destinations, and a permanent test compares the legacy fixture with what the real `bin/sync` writes. Files only: a git repository, hooks or a real ledger are for the phase that needs them, which passes `contents`. Phase P6 turns the new destinations into a second literal table in the manifest and this module then reads it. **RED first:** the suite failed on the absent module. **Mutants:** 10 of 10 killed (`new_path` keeping `docs/methodology`, tier 1 moving the seeds, no second runner in the half tree, the new archive or generated files left at the old place, a non-empty root or an unknown layout accepted, `contents` ignored, a manifest row dropped, the empty tree not empty). The suite is now 28 tests. No shipped tool changed. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S274 — the layout resolver (P1, 1 of 4): the plan's four-row table as one embeddable block, 16 tests, 8 mutants killed

`tools/layout_resolver.py` (canonical-only, not in `bin/_manifest.py`) holds `resolve_layout(root, anchor)`, which returns `(kind, directory, found)` by the plan's §4.3 table: `new` (the anchor under `methodology/`), `legacy` (at the root), `half` (both: no directory, so no tool can guess), `none` (neither). The function sits between two markers so P2-P6 can embed it byte for byte in each shipped tool and assert the copy with `embedded_block`, which refuses unbalanced or repeated markers. **One refinement of §4.3, recorded for the plan:** the table is keyed on a caller-supplied anchor, default `SESSION_RUNNER.md`. The plan's resolver returns one directory, but its own §4.6 calls a tier-1-only adopter a coherent end state (framework files moved, ledgers still at the root), and a tool that reads the ledger through the runner's directory would look for a file that is not there, which is the silent fail-open its C5 measured; a ledger tool resolves with `CHANGELOG.md`. `tools/test_layout_resolver.py`: 16 tests, one per row, the anchor cases, the block running alone, agreeing with the module on every tree shape and importing only `os` and `pathlib`, and the canonical-only check. **RED first:** the suite failed with `FileNotFoundError` on the absent module before the module was written. **Mutants:** 8 of 8 killed (a half tree handing back a directory, new and legacy swapped, a directory counting as the anchor, the default anchor changed, any hit read as half, the `methodology/` join dropped, unbalanced markers accepted, none reported as legacy). No shipped tool changed. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S274 claim (in progress) — build the layout resolver, the both-layout fixtures and the RED literal scanner (P1)

CHANGELOG: pending. Operator said `go` as the first message; at the Phase 0 picker he chose BL-101 P1 (the plan's recommendation) and gave the go-ahead to push `main`. The deliverable is the plan's §7.1, built in this session: the layout resolver (one canonical-only module, the four-row table of §4.3 as its unit tests), a `tools/test_layout_resolver.py` suite wired into `bin/tests.sh`, fixture trees in both layouts, the literal scanner run RED against the shipped tools, and a ratchet gate for each new suite. No shipped tool changes behaviour and the scanner is not wired into the gate (that is P6). Already done before this claim, each recorded above: the push of `main` (`b162866` then its record `d0f2775`, read back `0 0`) and the owed `HANDOFFS.md` trim (`e04c5e0`, S271 to `HANDOFFS-through-2026-10-06-2.md`, proof exit 0 by name from a `--no-local` clone) with its fold `078a6cc`. Phase 0 read: 0 undocumented commits at both frontiers, #94 #92 #93 without a maintainer reply, `quality_ratchet.py --run` 13/13 with results `2343fdc5ea84` and manifest `910259fb65a6` (S273's citation exactly), dashboard health 72. The plan's contract was re-verified at Orient: no file under `bin/`, `tools/`, `starter-kit/` or `.githooks/`, and neither gate config, differs from the plan's base `c8b9ddd`. Phase 3F records the rest. Model: Claude Sonnet 5.5.

### 2026-10-06 · [ad hoc] S274 — fold the second 2026-10-06 HANDOFFS shard pointer into the archive index

The pointer block the trim (`e04c5e0`, 1 receipt, S271, 2026-10-06, to `HANDOFFS-through-2026-10-06-2.md`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, trimmer v1.7.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S273, S272), both the fork's. The shard's `.verify.sh` was run by name from a `--no-local` clone of `e04c5e0`: exit 0, `records: 3 before = 2 retained + 1 archived`, L1, L2/front-matter and L3 hold. This is the trim S273's receipt named as owed after the S274 Phase 0 report, taken before the session's claim. Model: Claude Sonnet 5.5.

### 2026-10-06 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-06-2.md` (1 record(s), 34,869 B → 25,643 B)

**Written by:** `methodology_trim.py` v1.7.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-06 → 2026-10-06) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-06-2.md`](docs/archive/HANDOFFS-through-2026-10-06-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-06-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-06-2.md.verify.sh)
rather than trusting a digest printed here. Live file 34,869 B → 25,643 B (−26.5%).

### 2026-10-06 · [BL-101] S274 — fork `main` pushed to `origin`: the S273 decisions record `b162866`

On his go-ahead at the S274 Phase 0 picker ("Push main to origin"), `git push origin main` took `rmsharp/methodology` `main` from `b9f27f9` to `b162866`: a plain fast-forward (`origin/main` an ancestor of `main`, exactly one commit ahead, a clean tree), no force, no other ref; nothing went to `KJ5HST/methodology`. The one commit is S273's record of his close-out decisions (every recommendation of the BL-101 plan's §9). **Read back** after a fresh fetch: `git rev-list --left-right --count origin/main...main` = `0 0`, `git ls-remote origin refs/heads/main` = `b162866`. This recording commit, a `CHANGELOG.md`-only change, is pushed too under the standing grant for push records, so no further record is owed. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S273 — the operator's close-out decisions recorded: every recommendation of the plan's §9

At the close-out picker he took every recommendation: **D1** all the methodology files, in two tiers, the framework's own files first; **D6** this repository's real files stay put and the move is rehearsed in a scratch clone; **D8** the layout is built and proved on the fork and the adopters first, then offered upstream as one vetted pull request, each outward step his go-ahead at the time; **D2, D3, D4, D5, D7, D9** as the plan wrote them (flat `methodology/` with `workstreams/` below it; every filename kept; `.githooks/` and `CLAUDE.md` at the root and `.gitattributes` nested; the ledger archive last; expand then contract with `--layout auto` and sync before migrate; one adopter per session). He also gave the go-ahead to push `main` (recorded in its own entry above). Recorded in [`methodology-subdirectory-plan.md`](docs/planning/methodology-subdirectory-plan.md) (status line, §7 P0, §9), BL-101's index row and body, and the S273 receipt's next steps. **Next: P1.** Local, not pushed: its push is his go-ahead. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S273 — fork `main` pushed to `origin`: 9 commits, the `methodology/` directory plan reaches the fork

On his go-ahead at the close-out picker ("Push main to origin now"), `git push origin main` took `rmsharp/methodology` `main` from `9d5f22c` to `026122d`: a plain fast-forward (`origin/main` an ancestor of `main`, 0 behind after a fresh fetch, a clean tree), no force, no other ref; nothing went to `KJ5HST/methodology`. **Read back** after a fresh fetch: `git rev-list --left-right --count origin/main...main` = `0 0`, `git ls-remote origin refs/heads/main` = `026122d`. The nine commits: the `HANDOFFS.md` trim and its fold, the claim, four evidence commits, the plan with BL-101, the close-out. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S273 close-out — the `methodology/` directory plan, with syncing

`CHANGELOG: pending` on the S273 claim entry is cleared (by this statement: the never-edit gate forbids editing a committed entry). **Deliverable:** the plan for moving the methodology files into one `methodology/` directory, with syncing (BL-101): [`methodology-subdirectory-plan.md`](docs/planning/methodology-subdirectory-plan.md), DRAFT, plus `docs/planning/methodology-subdirectory-evidence/`. Nothing implemented, nothing sent, no adopter touched. **Gate:** `quality_ratchet.py --run` on `a47232b`: 13/13, `tests-sh-passed` 452, results `2343fdc5ea84`, manifest `910259fb65a6`. **Receipt:** `HANDOFFS.md` S273 complete (self 8, predecessor 9). **Commits this session:** the owed trim `d8a3024` and its fold `ef766f7`, the claim `c8b9ddd`, evidence `6127202` `143f05f` `049a4c8` `5b6ebed`, the plan with BL-101 `a47232b`. **Waiting on the operator:** D1, D2, D6 and D8 (plan §9); the push of this session's commits. No fork learning row appended (D3's retirement duty does not arise; considered #19, #71, #81, #103, #108). Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S273 — the plan for moving the methodology files into `methodology/`, with syncing, and its backlog item

Added [`methodology-subdirectory-plan.md`](docs/planning/methodology-subdirectory-plan.md) (DRAFT, 54 KB, nothing implemented) and recorded BL-101 (an index row in `docs/planning/BACKLOG.md`, a body in `BACKLOG-DETAIL.md`). The plan: feasible, 22 to 29 sessions, 17 couplings with file and line, an expand/migrate/contract route with a layout resolver, a `--layout auto` sync and a sync-before-migrate rule, and nine decisions (§9). Its two sharpest findings were measured on clones, not argued: after the ledger moves the pre-commit ledger gate passes a ledger-less commit (it fails open), and moving this repository's own instance files turns the next resync from `upstream` into modify/delete conflicts because git pairs none of them. The operator's mid-session instruction to account for syncing the adopters and this repository is §5A. Local only: nothing pushed, no pull request, no comment on `KJ5HST/methodology`, no adopter touched. The first four decisions wait on the operator. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S273 — evidence for the `methodology/` move, 4 of 4: the frozen proofs and the suite's blast radius

Added `docs/planning/methodology-subdirectory-evidence/frozen-proofs.sh` with its recorded output and `suite-blast-radius.txt`. All 117 tracked `.verify.sh` proofs give the same exit codes in three clones: nothing moved, the two ledgers moved, the ledgers and `docs/archive` moved (112 exit 0 and 5 exit 1 in each; the 5 are the August shards, BL-36's class). `bin/tests.sh` in the same three clones, serial: 452 passed / 0 failed / 0 skipped, 418 / 12 / 3, 414 / 11 / 5; the failing assertions and the skipped checks are listed in the text file. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S273 — evidence for the `methodology/` move, 3 of 4: the hook and the resync after a move

Added `docs/planning/methodology-subdirectory-evidence/hook-after-move.sh` and `resync-after-move.sh` with recorded outputs, both on throwaway clones. The hook script: with hooks on, an unmoved ledger refuses a ledger-less commit (exit 1), but after `git mv CHANGELOG.md methodology/CHANGELOG.md` the move commit passes (exit 0) and so does a later content commit with no ledger entry (exit 0): the co-staging gate fails open. The resync script: against the merge base `f34769f` git pairs only `.gitattributes` with its moved copy; one synthetic upstream edit merged into the fork gives 4 modify/delete conflicts and a file-location conflict when the instance files and archive have moved, 3 text conflicts when they have not. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S273 — evidence for the `methodology/` move, 2 of 4: the adopter survey and the git behaviours

Added `docs/planning/methodology-subdirectory-evidence/adopter-survey.sh` and `git-behaviour.sh` with recorded outputs. The survey reads the 12 sibling projects (all in committed mode; 18 methodology files at the root and up to 12 under `docs/methodology/`; the zsh run of the first draft counted 0 root files because zsh does not word-split, so the script is bash with arrays). The git script measures a nested `methodology/.gitattributes` (clean union merge, exit 0, against a conflict, exit 1, without it) and what a `git mv` does to `git log` by path (stops at the move; `--follow` reaches the earlier commits). Throwaway repositories only. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-101] S273 — evidence for the `methodology/` move, 1 of 4: the reference inventory and the link simulation

Added `docs/planning/methodology-subdirectory-evidence/inventory.py` and `link-simulation.py` with their recorded outputs (tracked files at `c8b9ddd`): 31 code and config files, 23 distributed docs and 3 canonical-only docs name a methodology file, plus 420 history files that are never rewritten; 118 relative links in the distributed docs, 40 of which change under a flat `methodology/`. Read-only scripts; nothing in the tree they measure changed. Model: Claude Sonnet 5.5.

### 2026-10-06 · [ad hoc] S273 claim (in progress) — plan the `methodology/` subdirectory move

CHANGELOG: pending. Operator said `go` as the first message; at the Phase 0 picker he asked instead for a plain statement of the backlog (given in the Phase 0 follow-up: 60 open index rows, only BL-98 waiting on an open upstream PR, seven rows stale after the 2026-10-01 merges) and set this session's deliverable: analyze, and if possible write a detailed implementation plan for, moving the methodology files from a repository's root into one `methodology/` directory one level below root, for adopters and perhaps for this repository. The deliverable is the plan document in `docs/planning/`; implementing it is a separate session, and nothing outward-facing is done (no push, no PR, no comment, no change in any adopter). The owed `HANDOFFS.md` trim (`d8a3024`, one receipt, S270, to `HANDOFFS-through-2026-10-06.md`, proof exit 0 by name from a `--no-local` clone) and its fold (`ef766f7`) ran first as their own actions. Phase 3F records the rest.

### 2026-10-06 · [ad hoc] S273 — fold the 2026-10-06 HANDOFFS shard pointer into the archive index

The pointer block the trim (`d8a3024`, 1 receipt, S270, 2026-10-06, to `HANDOFFS-through-2026-10-06.md`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, trimmer v1.7.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S272, S271), both the fork's. The shard's `.verify.sh` was run by name from a `--no-local` clone of `d8a3024`: exit 0, `records: 3 before = 2 retained + 1 archived`, L1, L2/front-matter and L3 hold. This is the trim S272's receipt named as owed after the S273 Phase 0 report, taken before the session's claim. Model: Claude Sonnet 5.5.

### 2026-10-06 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-06.md` (1 record(s), 35,187 B → 25,659 B)

**Written by:** `methodology_trim.py` v1.7.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-06 → 2026-10-06) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-06.md`](docs/archive/HANDOFFS-through-2026-10-06.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-06.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-06.md.verify.sh)
rather than trusting a digest printed here. Live file 35,187 B → 25,659 B (−27.1%).

### 2026-10-06 · [BL-99] S272 — fork `main` pushed to `origin`: 7 commits, the first-parent dashboard fix reaches the adopters' source

On his go-ahead at the close-out picker ("Push main now", the recommended option), `git push origin main` took `rmsharp/methodology` `main` from `fcdfa4d` to `4e53675`: a plain fast-forward (`origin/main` an ancestor of `main` and 0 behind after a fresh fetch, a clean tree), no force, no other ref, the local backup ref `pre-resync-2026-10` not pushed (`git ls-remote origin 'refs/heads/pre-resync*'` finds none). **Read back, not inferred:** `git rev-list --left-right --count origin/main...main` reads `0 0`; `git ls-remote origin refs/heads/main` and the GitHub API's `branches/main` both read `4e53675`; `upstream` is untouched at `f34769f`. The 7 commits are the `HANDOFFS.md` trim and its fold, the S272 claim, the BL-99 fix (dashboard 2.21.0), the raised `dashboard-unit-tests` floor, BL-99's closure and the close-out; the S272 close-out entry's "nothing outward" was true when written and this is the one action after it. The adopters sync from this branch (`bin/status` then `bin/sync`), and none was synced. This entry is the push's own record and goes out under his standing grant for a ledger-only push record.

### 2026-10-06 · [BL-99] S272 close-out — the dashboard's manifest-history walk is first-parent; BL-99 closed

`CHANGELOG: pending` on the S272 claim entry is cleared (by this statement: the never-edit gate forbids editing a committed entry). **Deliverable:** BL-99. `_gate_manifest_history` and `_manifest_has_history` read `git log --first-parent` in both dashboard twins, `DASHBOARD_VERSION` 2.21.0 (`75f665e`); three tests, RED against 2.20.0 and green after; the `dashboard-unit-tests` floor 353 → 356 (`2d0a78a`); BL-99 closed (`274203a`). The owed `HANDOFFS.md` trim (`c53a4e0`, one receipt to `HANDOFFS-through-2026-10-05-7.md`, proof exit 0 by name from a `--no-local` clone) and its fold (`ff89230`) ran first. **Measured:** 9 of the 10 loosening rows the fork's scan printed (5 of 6 commits) loosen nothing against their own parent; the plain walk also read a real loosening as nothing when a merge resolved to the lower of two floors; the fixed scan prints the one real row (`368b29c`, 327 → 294); seven other repos here with a manifest scan identically. **Verified in `--no-local` clones:** `quality_ratchet.py --run` 13/13 at `274203a` (results `2343fdc5ea84`, manifest `910259fb65a6`; `dashboard-unit-tests` 356, `tests-sh-passed` 452 at three receipts); the dashboard CLI end to end in a scratch portfolio (exit 0, the HTML shows the one real row and no phantom). **Nothing outward:** no push, no PR, no comment; `upstream/main` has the same plain walk (2.11.3) and a patch there is his go-ahead. **3A:** S271's handoff scores 9. **3C:** no fork learning row appended, so D3's retirement duty does not arise; rows considered are named in the receipt. **Next:** watch #94, #92 and #93, then the push decision; the `HANDOFFS.md` trim is owed after the next Phase 0 report (expect S270 to `HANDOFFS-through-2026-10-06.md`). Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-99] S272 — BL-99 closed (index row out, id kept, completed row in)

BL-99's index row is out of `docs/planning/BACKLOG.md`, its id is in the closed-ids list there (between BL-97 and BL-100), and its closure row is the last row of `docs/planning/BACKLOG-COMPLETED.md`; `bash docs/planning/BACKLOG-COMPLETED.md.verify.sh` exits 0 (C1-C6). The fork-side fix is `75f665e` and the floor `2d0a78a`. **What stays open, as a decision of his and not a backlog item of mine:** `upstream/main` has the same plain walk (2.11.3, a separate lineage), so an upstream patch is re-derived against that file; per the contribution rule it waits to be batched into one vetted pull request and needs his go-ahead each time. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-99] S272 — the floor re-measured after the fix: `dashboard-unit-tests` 353 → 356

A tightening in `.quality-gates.json` (the hook accepts it; only a loosening needs plan mode), with a note key `_s272_tightening_bl99` in the S271 convention. **356 is measured, not derived from the +3:** `quality_ratchet.py --run` in a `--no-local` clone of `75f665e` read 13/13 pass, results `fa1343d019ab`, manifest `387dea198c3f`, `dashboard-unit-tests` 356 and `tests-sh-passed` 452 (at three receipts, the state mid-claim; the floor 446 is the at-rest value and is unchanged). Without it the three new tests could be deleted with the gate still green. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-99] S272 — the dashboard's manifest-history walk is first-parent (2.21.0)

`_gate_manifest_history` and `_manifest_has_history` (`tools/methodology_dashboard.py`, byte-identical twin `starter-kit/methodology_dashboard.py`) now run `git log --first-parent -- .quality-gates.json`, so each manifest version is compared with the line it landed on, a merge included, instead of with the next older row of two interleaved lineages. **Measured, not inferred:** the scan on this fork printed 10 loosening rows over 6 commits; each commit's manifest was compared with its own parent, and 5 of the 6 (9 of the 10 rows: `b34a841`, `02677ea`, `67feb9f`, `d4dbc26`, `e2501c5`) loosen nothing against it. The sixth, `368b29c` (`tests-sh-passed` 327 → 294, a deliberate lowering on the first-parent line), is real, and it is the only loosening row the fixed scan prints, beside the unchanged `check-ledger` command advisory (`c333475`). **The walk was wrong in both directions**, not only the phantoms: a merge that resolves to the lower of two floors matches the side branch, git then follows only that parent, and a real loosening of the line merged into read as nothing. **Tests:** +3 in `TestQualityGateSignals` (`test_a_merged_lineage_is_not_read_as_one_line`, `test_a_loosening_a_merge_resolves_to_is_reported_at_the_merge`, `test_a_loosening_a_side_branch_carried_in_is_attributed_to_the_merge`), RED against 2.20.0 for the stated reasons (the first reproduces BL-99's two phantom rows in a toy repo; a first draft passed against the old code because its merge matched one parent, so git never interleaved, and was rebuilt), GREEN after; the file reads 356 OK with the same 4 by-design skips as the 353 before. **Adopter impact:** the seven other repos under `~/Development` that carry a manifest produce identical scans under the old and new walk (none has a merge touching the manifest); the price is that a loosening made on a side branch is now reported at the merge that carried it in (`git diff <sha>^1 <sha> -- .quality-gates.json` shows it). `DASHBOARD_VERSION` 2.20.0 → 2.21.0, both pins in `test_dashboard_version` (a changed output on a distributed tool is MINOR). **Upstream has the same plain walk** (`upstream/main` `starter-kit/methodology_dashboard.py:2007`-`:2015`, 2.11.3, a separate lineage of 3,758 lines), so a fix there is a patch re-derived against that file and his go-ahead; nothing was pushed, opened or commented. Model: Claude Sonnet 5.5.

### 2026-10-06 · [BL-99] S272 claim (in progress) — the dashboard's manifest-history walk

CHANGELOG: pending. Operator said `go` as the first message and chose "BL-99: first-parent manifest walk" at the Phase 0 picker (and "keep" for the local backup ref `pre-resync-2026-10`). The deliverable is BL-99: settle with evidence whether `_gate_manifest_history` should walk the manifest `--first-parent`, and if so fix it and its twin with tests so a merged lineage stops printing "floor lowered" and "gate removed" rows nobody caused; the eight older rows S271 did not examine are examined too. Local only: nothing is pushed or sent; an upstream PR for a distributed change is a separate go-ahead. The owed `HANDOFFS.md` trim (`c53a4e0`, one receipt to `HANDOFFS-through-2026-10-05-7.md`, proof exit 0 by name from a `--no-local` clone) and its fold (`ff89230`) ran first as their own actions. Phase 3F records the rest.

### 2026-10-06 · [ad hoc] S272 — fold the seventh 2026-10-05 HANDOFFS shard pointer into the archive index

The pointer block the trim (`c53a4e0`, 1 receipt, S269, 2026-10-05, to `HANDOFFS-through-2026-10-05-7.md`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (1 receipt, trimmer v1.7.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S271, S270), both the fork's. The shard's `.verify.sh` was run by name from a `--no-local` clone of `c53a4e0`: exit 0, `records: 3 before = 2 retained + 1 archived`, L1, L2/front-matter and L3 hold. This is the trim S271's receipt named as owed after the S272 Phase 0 report, taken before the session's claim. Model: Claude Sonnet 5.5.

### 2026-10-06 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-05-7.md` (1 record(s), 33,594 B → 24,981 B)

**Written by:** `methodology_trim.py` v1.7.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-10-05 → 2026-10-05) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-05-7.md`](docs/archive/HANDOFFS-through-2026-10-05-7.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-05-7.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-05-7.md.verify.sh)
rather than trusting a digest printed here. Live file 33,594 B → 24,981 B (−25.6%).

### 2026-10-06 · [BL-95] S271 — fork `main` pushed to `origin`: 124 commits, the resync reaches the adopters' source

On his go-ahead at the close-out picker ("Push main now"), `git push origin main` took `rmsharp/methodology` `main` from `a4c5587` to `e9afd73`: a plain fast-forward (`origin/main` an ancestor of `main`, 0 behind after a fresh fetch), no force, no other ref, the local backup ref `pre-resync-2026-10` not pushed. **Read back, not inferred:** `git rev-list --left-right --count origin/main...main` reads `0 0`; `origin/main`, `git ls-remote origin refs/heads/main` and the GitHub API's `branches/main` all read `e9afd73`; `upstream` is untouched at `f34769f`. The 124 commits are the merge of `upstream/main` (v4.2) with its fix-ups, both ledger trims and this session's records; the adopters sync from this branch (`bin/status` then `bin/sync`), and none was synced here. This entry is the push's own record and goes out under his standing grant for a ledger-only push record.

### 2026-10-06 · [ad hoc] S271 — the operator's decisions at close-out: push `main` now; the burndown-chart idea declined (BL-100)

At the S271 close-out picker he chose **"Push main now"** (the recommended option) and, of two follow-ups, ticked the first with the instruction *"Record burndown idea and explain that your explanation was sufficient to reject it"*; he did not tick deleting the backup ref `pre-resync-2026-10`, so it stays. **The idea** came from his mid-session question whether a burndown chart makes sense for most repositories and could be an optional `methodology_dashboard.py` panel. It is recorded as `BL-100`, **declined**: a closed row in `docs/planning/BACKLOG-COMPLETED.md` and its id in `docs/planning/BACKLOG.md`'s closed-ids list, with the reasons (no finite scope in an open-ended backlog; the history file keeps no open count; the GitHub source needs the network; a scored chart invites gaming) and what was feasible (an off-by-default profile-token panel, display only, a distributed change needing an upstream pull request). Nothing was built. The receipt's push wording is rewritten so it is true whatever `origin/main...main` reads; the push itself is the next entry.

### 2026-10-06 · [BL-95] S271 close-out — R2 done: both ledgers trimmed and proved, the floors tightened, BL-95 closed

`CHANGELOG: pending` on the S271 claim entry is cleared (by this statement: the never-edit gate forbids editing a committed entry). **Deliverable:** R2 of `docs/planning/upstream-resync-2026-10-plan.md` §5 — `HANDOFFS.md` 121,640 → 24,339 B (`2ee009c`, fold `12ec2d1`), `CHANGELOG.md` 433,654 → 91,688 B (`79506ca`), each shard's `.verify.sh` exit 0 by name from a `--no-local` clone; Test 30 and Test 31 repaired after the trim emptied them (`4ae8b5d`, `f0d4ccb`); floors `tests-sh-passed` 446 and `dashboard-unit-tests` 353 (`603de86`); BL-95 closed (`0e598b8`); BL-99 recorded (`3e881c8`). **Verified in `--no-local` clones:** `quality_ratchet.py --run` 13/13 at `f0d4ccb` (results `cba502fadfae`, manifest `387dea198c3f`; `tests-sh-passed` measured 452 at three receipts), the two-receipt suite 446 / 0 / 6. **Adopter impact measured:** 16 of 30 distributed sources differ from the pre-merge `main`; a scratch `bin/sync --source=local` created all 30; no real adopter synced. **Nothing outward:** no push, no PR, no comment; the push is his go-ahead, asked at the close-out picker. **3A:** S270's handoff scores 9. **3C:** no fork learning row appended, so D3's retirement duty does not arise. **Next:** the push decision, then watch #94, #92 and #93; the `HANDOFFS.md` trim is owed after the next Phase 0 report.

### 2026-10-06 · [ad hoc] S271 — BL-99 recorded: the dashboard reads a merged manifest history as one line

A finding from Phase 0, recorded as `BL-99` in `docs/planning/BACKLOG.md` (upstream-facing candidate; not planned, not built). The scan's `context-budget-unit-tests` "floor lowered 148 → 122 in `b34a841`" and `check-ledger` "removed" rows are not loosenings: `_gate_manifest_history` (`tools/methodology_dashboard.py:2976`) runs `git log -- .quality-gates.json` without `--first-parent`, so after the BL-95 merge it interleaves the two lineages by date and compares the fork's `b34a841` (122, 11 gates) with upstream's `d432865` (148, `check-ledger` present). Checked with `git show <sha>:.quality-gates.json` on `d432865`, `b34a841^`, `b34a841` and `816834c`; the tip holds 148 and 13 gates. Eight older rows in the same detail were not examined. Whether the walk should be first-parent is the open question; a fix would be an upstream pull request and needs his go-ahead.

### 2026-10-06 · [BL-95] S271 — Test 31's real-ledger rows read the ledger and its shards: a pass that compared 0 with 0

The same cause as Test 30's red row, in its silent twin. After R2's trim the live `CHANGELOG.md` holds no `**Model:**` bullet, so `bin/tests.sh` Test 31's real-file proof printed `PASS: Source 1's entry count (0) matches the raw anchored **Model:** grep (0)` — green in the 446-passed run, and proving nothing; the WARNING row beside it passed vacuously too. Both now read the live file plus its shards, as Test 30 does since `4ae8b5d`: the count row compares **666 with 666** and no WARNING fires (checked directly before the edit: `TOOL_COUNT` 666, `RAW_COUNT` 666, 0 WARNING lines). The labels say "ledger (live file and shards)". Test 40, which sits beside them, was written trim-invariant (it asserts the default run sees more than the live file alone, with a control first) and needed nothing. **Correction to the Test 30 entry above (`4ae8b5d`):** it cites the temp-file block as `bin/tests.sh:1515`-`:1520`; at that commit it is `:1519`-`:1522` (a committed entry is never edited, so the correction is this one).

### 2026-10-06 · [BL-95] S271 — BL-95 closed: the resync's two executor sessions are done

BL-95's index row is out of `docs/planning/BACKLOG.md`, its id is in the closed-ids list there (between BL-86 and BL-96), and its closure row is in `docs/planning/BACKLOG-COMPLETED.md` — the two edits plus the row the C6 proof asks for; `bash docs/planning/BACKLOG-COMPLETED.md.verify.sh` exits 0 (C1–C6, 6 later closures findable) and `bin/check-links` is OK (116). The row records R1 (S270: merge `2ed9262`, fix-ups F1–F4) and R2 (S271: `HANDOFFS.md` 121,640 → 24,339 B at `2ee009c`, `CHANGELOG.md` 433,654 → 91,688 B at `79506ca`, Test 30 at `4ae8b5d`, the floors 446 and 353 at `603de86`) and the adopter measurement: 16 of the 30 distributed sources differ from the pre-merge `main` (15 changed, one new seed), a scratch `bin/sync --source=local` created all 30 and `bin/status` read them current; no real adopter was synced. Nothing pushed: the push is his go-ahead.

### 2026-10-06 · [BL-95] S271 — the floors re-measured after the resync: `tests-sh-passed` 343 → 446, `dashboard-unit-tests` 336 → 353

R2 step 3 of `docs/planning/upstream-resync-2026-10-plan.md` §5, a tightening in `.quality-gates.json` (the hook accepts it; only a loosening needs plan mode). **`tests-sh-passed` 446** is `bash bin/tests.sh` read in a `--no-local` clone of `4ae8b5d` with `HANDOFFS.md` reduced to the two receipts the gate is measured in (the pending S271 stub removed), output captured to a file: `446 passed, 0 failed, 6 skipped`, the six skips Test 34's. The first read of that state, at `79506ca`, was 445 passed / 1 failed (Test 30's real-ledger row, fixed at `4ae8b5d`), so 446 is measured after the fix. **`dashboard-unit-tests` 353** is `python3 tools/test_methodology_dashboard.py` at the same tip (`Ran 353 tests`, OK, 4 skipped). The other count gates already sit at their measured values (trimmer 181, context budget 148, close-out report 68, ratchet 45). The manifest's new note `_s271_tightening_bl95_r2` records the conditions and says the floor is the online value. `HANDOFFS.md`'s front matter said `tests-sh-passed` "measures 343 at rest and 349 mid-claim"; both numbers were false after this change, so the sentence now says only that it reads six lower at rest than mid-claim and that the floor is set at rest — no hand-maintained count to decay.

### 2026-10-06 · [BL-95] S271 — Test 30's real-ledger row reads the ledger and its shards, not the live file alone

R2's `CHANGELOG.md` trim (`79506ca`) took the last `**Model:**` bullet out of the live file (1 at `dc019b6`, 0 after; the shard holds it), so `bin/tests.sh` Test 30's real-file row — "Source 1 reports a non-empty population against this repo's own live CHANGELOG.md" — went red on a correct trim: **445 passed, 1 failed, 6 skipped** in a two-receipt `--no-local` clone of `79506ca`, the one failure that row. `bin/model-report` over the live file alone prints its empty-population sentinel; over the live file plus the shards (`cat CHANGELOG.md $(git ls-files 'docs/archive/CHANGELOG-*.md')`, the source-tag audit's own idiom) it reads 666 entries. The row now builds that union in a temp file (`bin/tests.sh:1515`-`:1520`) and its two labels say "ledger (live file and shards)"; a shard is frozen, so a later trim cannot empty the proof again. The BL-20 regression it guards is still caught: a parser that prints the sentinel against a file carrying bullets still fails it. Upstream's `bin/tests.sh` has no such row, so this is fork-only.

### 2026-10-06 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-10-04.md` (336 record(s), 433,654 B → 91,688 B)

**Written by:** `methodology_trim.py` v1.7.0 — a tool action, not a session's judgment.
Moved the oldest **336** record(s) (2026-08-10 → 2026-10-04) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-10-04.md`](docs/archive/CHANGELOG-through-2026-10-04.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-10-04.md.verify.sh`](docs/archive/CHANGELOG-through-2026-10-04.md.verify.sh)
rather than trusting a digest printed here. Live file 433,654 B → 91,688 B (−78.9%).

### 2026-10-06 · [BL-95] S271 claim (in progress) — R2: the ledger trims, the floors and the adopter measurement

CHANGELOG: pending. Operator said `go` as the first message and chose "R2: ledger trims + floors" at the Phase 0 picker. The deliverable is plan section 5's R2 (`docs/planning/upstream-resync-2026-10-plan.md:379`): the `CHANGELOG.md` trim, the floors re-measured at two receipts and tightened, the adopter measurement by `bin/sync --source=local` into a scratch project, and BL-95's closure, local only: nothing is pushed or sent, and the report asks for the push go-ahead. The owed `HANDOFFS.md` trim (`2ee009c`, 18 receipts to `HANDOFFS-through-2026-10-05-6.md`, its `.verify.sh` exit 0 by name from a `--no-local` clone) and its fold (`12ec2d1`) ran first as their own actions, which is R2 step 2. Phase 3F records the rest.

### 2026-10-06 · [ad hoc] S271 — fold the sixth 2026-10-05 HANDOFFS shard pointer into the archive index

The pointer block the trim (`2ee009c`, 18 receipts, 2026-09-16 → 2026-10-05, to `HANDOFFS-through-2026-10-05-6.md`) wrote into `HANDOFFS.md` is now one row in `docs/HANDOFFS_ARCHIVE_INDEX.md` (18 receipts, trimmer v1.7.0), in its own commit as the fold procedure requires. `HANDOFFS.md` holds 2 receipts (S270, S269), both the fork's, so its front matter's "every receipt retained here is the fork's" is true again. The shard's `.verify.sh` was run by name from a `--no-local` clone of `2ee009c`: exit 0, `records: 20 before = 2 retained + 18 archived`, L1, L2/front-matter and L3 hold. This is R2 step 2 of `docs/planning/upstream-resync-2026-10-plan.md` §5, taken before the session's claim because the trim was owed after the Phase 0 report.

### 2026-10-06 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-10-05-6.md` (18 record(s), 121,640 B → 24,339 B)

**Written by:** `methodology_trim.py` v1.7.0 — a tool action, not a session's judgment.
Moved the oldest **18** record(s) (2026-09-16 → 2026-10-05) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-10-05-6.md`](docs/archive/HANDOFFS-through-2026-10-05-6.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-10-05-6.md.verify.sh`](docs/archive/HANDOFFS-through-2026-10-05-6.md.verify.sh)
rather than trusting a digest printed here. Live file 121,640 B → 24,339 B (−80.0%).

### 2026-10-06 · [BL-95] S270 — the operator's push decision: fork `main` stays local until R2

Asked at the S270 close-out picker whether to push fork `main` (112 commits: the merge `2ed9262`, fixes F1-F4 and this session's records) to `origin/main`, he chose **"Not yet, after R2"** (the recommended option): the adopters sync from fork `main`, R2 measures the adopter impact first (plan §5 R2 step 4), and R2's report asks again (step 5). Nothing was pushed; `origin/main...main` reads `0 112` before this entry's commit. The decision is recorded in the S270 receipt's next steps (3) and the BL-95 row already says R2 is next. No other action.

### 2026-10-06 · [BL-95] S270 close-out — R1 is done: `upstream/main` is merged into fork `main`, verified in a clean clone, local; the receipt is complete

`CHANGELOG: pending` on the S270 claim entry is cleared (by this statement: the never-edit gate forbids editing a committed entry). **Deliverable:** R1 of `docs/planning/upstream-resync-2026-10-plan.md` §5 — the merge `2ed9262` (17 resolutions, both ledgers folded) and fix-ups F1 `b7ded00`, F2 `c333475`, F3 `3b67019`, F4 `d7c44ea`; the owed HANDOFFS trim (`2291af5`) and its fold (`3d83923`) ran first, the claim is `9904a0a`. **Verified in a `--no-local` clone of `d7c44ea`:** `bin/tests.sh` 452 passed, 0 failed, 0 skipped (exit 0); `quality_ratchet.py --run` 13/13 pass, 0 fail, 0 unmeasured, results `1d86b9c13d21`, manifest `bb610573f2dd`; `bin/check-links`, `bin/check-learnings`, `bin/check-ledger`, `bin/check-handoff --all --allow-pending` (20 receipts) and both hook selftests exit 0; the dashboard twins are `cmp` equal; the 22 upstream-only paths are byte-identical to `upstream/main`; the CHANGELOG shard's diff against the first parent is empty and its proof exits 0; `bin/sync --source=local` into a scratch project created all 30 files. **One flip against Phase 0:** `HANDOFFS.md` went from ok to over its 65,536 B context ceiling (25,008 B to 112,486 B) because 17 upstream receipts arrived; R2's trim repairs it. **Nothing outward:** no push (`origin/main...main` reads `0 111`), no PR, no comment; the local backup ref `pre-resync-2026-10` holds the pre-merge tip. **3A:** S269's handoff scores 9. **3C:** no fork learning row appended, so D3's retirement duty does not arise. **Next:** watch #94, #92 and #93, then R2 (plan §5; the HANDOFFS trim is owed after the next Phase 0 report whichever task is chosen).

### 2026-10-06 · [BL-96] S270 — R1 fix-up F4: Test 9's skip is counted, and BL-96 is closed (D7)

`bin/tests.sh:145` is now `skip "$URL unreachable"` where it was a bare `echo "  SKIP: …"` that the Summary's skip count never saw. D7 (A, the operator's, 2026-10-06): count it, no gate (shape (b) not chosen). Measured: the Test 9 block run alone against `file:///nonexistent/never` printed `SKIP: … unreachable` with `SKIP=1`; `grep` finds no `gh api`, `gh CLI` or `"gh"` in `bin/sync` or `bin/status` (the merge replaced the `gh` route with a git clone). BL-96 left the `BACKLOG.md` index (its id stays on the closed list), gained a `BACKLOG-COMPLETED.md` row and a DONE paragraph in `BACKLOG-DETAIL.md`. One line now differs from upstream, whose Test 9 has no counter. The full suite on the R1 tip is not yet run.

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

