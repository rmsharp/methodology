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

**Everything below the most recent cut is archived — and that boundary is POSITIONAL, not a
calendar seam.** `2026-08-30` carries records on *both* sides of it, so a shard's dated filename is a
**span label, not a day boundary**; `methodology_trim.py` says so itself (`CUT_STRADDLES_DAY`,
design §2.3). Every shard is listed in a pointer block below, and **no count is written here** —
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
reaffirmed it at S177 (2026-09-16): `--check` keeps firing, and a trim is raised with the operator only
once the file passes the 262,144 B hard read refusal (`READ_REFUSE_BYTES`). Nothing reads this file
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

---

## 2026-09

### 2026-09-17 · [BL-54] S179 — the history walks look up blobs in one batched call, recovering the fix's run time

- **Why:** the BL-54 fix walks 732 commits across the tracked files where the default walk visited 327, and both
  tools ran one `git ls-tree` subprocess per commit, so `bin/status` over the six adopters went 3.0 s → 10.1 s and
  `bin/sync --dry-run` on `wsfct` 2.9 s → 7.5 s.
- **The change:** one `git cat-file --batch-check` per walk, fed `<commit>:<path>` lines — `bin/status` `blobs_at`
  (`:52`), used by `history_walk`; `bin/sync` `local_history_blobs` (`:55`). A separate commit from the fix, so it can be
  judged or left out of an upstream PR on its own.
- **Behaviour-neutral, measured:** `bin/status` over the six adopters is byte-identical to the fix commit's output
  (174 rows); `bin/sync --dry-run` output on each of the six is identical apart from the `version:` line (HEAD
  moved), with the same exit codes; Test 41 still 11 / 0.
- **Run time now:** `bin/status` 4.0 s (3.0 s before the fix); `bin/sync --dry-run` on `wsfct` 2.3 s (2.9 s before).
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-17 · [BL-54] S179 — `bin/status` and `bin/sync` see versions a merge hid; *N versions behind* counts main-line versions

- **The defect:** both tools listed a file's past versions with a plain `git log -- <path>`, which follows only a
  merge's TREESAME parent. A version on the side a merge did not keep was never visited, so an unmodified copy of it
  read *locally modified* and `bin/sync` refused it (exit 2).
- **The fix:** `bin/sync:64` walks with `--full-history`; it only asks whether a version is known. `bin/status` walks
  twice (`:81` `local_history`, `:52` `history_walk`, with a shared commit → blob cache): the first-parent line and
  the full history. **N counts distinct versions newer than the project's along the first-parent line**, falling
  back to the full walk for a version that only ever existed on a merged branch (`:96` `versions_behind`, `:121`
  `file_status`). **Operator decision, S179 (picker), option C** over A (the flag alone, a raw position: 63 behind for
  `mts-system`'s learnings file) and B (distinct versions over the full walk, counting each commit inside a merged
  branch), each measured on the six adopters before it was offered.
- **RED first:** `bin/tests.sh` Test 41 (`:3076`) builds a methodology repo with both hiding shapes — a merge taking a
  side branch's content (`22ce71b`'s) and one keeping main's (`213f841`'s) — at fixed commit dates, proves the
  shapes (the walks visit 4 / 8 / 4 commits), then pins 6 status rows and 3 sync outcomes. On the old code it failed
  exactly the 4 hidden-version rows; the fixture checks and the real-local-edit controls passed. After the fix,
  11 / 0. **Eight mutants, all killed:** option A, option B, the walks swapped, no fallback, no `--full-history` in
  status, no `--first-parent`, a positional rather than distinct count, and sync without the flag.
- **Runtime, on the six real adopters (read-only):** `bin/status` over 174 rows changes **8 states**, every one
  *locally modified* → *N versions behind* (`FRAMEWORK_LEARNINGS.md` in `mts-system`, `nprcgenekeepr`,
  `vscode_quarto_ext`, `wsfct`; `methodology_trim.py` in `mts-system`, `vscode_quarto_ext`, `wsfct`; and
  `vscode_quarto_ext`'s `context_budget.py`, which S178's scratch copies did not list and which was already misread
  before `22ce71b`). 35 rows change only their count; 131 are unchanged; the 3 genuine local edits
  (`model_project_constructor`'s runner and `SAFEGUARDS.md`, `nprcgenekeepr`'s trimmer) still read *locally
  modified*. `bin/sync --dry-run`: `mts-system`, `vscode_quarto_ext`, `wsfct` go from exit 2 to 0;
  `model_project_constructor` and `nprcgenekeepr` still refuse, on their genuine edits only; no adopter's
  `git status` changed.
- **Cost, stated:** `bin/status` over the six took 3.0 s before and 10.1 s after; `bin/sync --dry-run` on `wsfct`
  2.9 s → 7.5 s (732 commits walked across the tracked files, where the default walk visited 327).
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-17 · [ad hoc] S179 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

- The pointer block `90da3e1` wrote into `HANDOFFS.md`'s front matter is now one row of
  [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md) (2 records, 2026-09-16 → 2026-09-16,
  `HANDOFFS-through-2026-09-16-5.md`, v1.5.0). The block is deleted, taking the file from 16,401 to 15,945 B,
  in its own commit per the index's fold rule. `docs/archive/HANDOFFS-through-2026-09-16-5.md.verify.sh` exits
  0 after the fold, `check-handoff --all --allow-pending` passes on 2 receipts, and `bin/check-links` exits 0.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-17 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-16-5.md` (2 record(s), 36,666 B → 16,401 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-09-16 → 2026-09-16) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-16-5.md`](docs/archive/HANDOFFS-through-2026-09-16-5.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-16-5.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-16-5.md.verify.sh)
rather than trusting a digest printed here. Live file 36,666 B → 16,401 B (−55.3%).

### 2026-09-17 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-09-16.md` (104 record(s), 264,071 B → 99,397 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **104** record(s) (2026-09-14 → 2026-09-16) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-09-16.md`](docs/archive/CHANGELOG-through-2026-09-16.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-09-16.md.verify.sh`](docs/archive/CHANGELOG-through-2026-09-16.md.verify.sh)
rather than trusting a digest printed here. Live file 264,071 B → 99,397 B (−62.4%).

### 2026-09-17 · [BL-54] S179 claim — `bin/status` and `bin/sync` walk history with `--full-history` (in progress)

**Deliverable:** BL-54 ([`docs/planning/BACKLOG-DETAIL.md`](docs/planning/BACKLOG-DETAIL.md#bl-54)): add
`--full-history` to the history walks at `bin/status:56` and `bin/sync:60`, test first on a merge that keeps
one side's content for a path, and settle what *N versions behind* counts. Chosen by the operator after
Phase 0 (picker), as S178 recommended.

- **Operator go-aheads, same picker:** trim `CHANGELOG.md` now, the file being past the 262,144 B refusal
  (the 2026-09-14 decision's condition); push fork `main` to `origin` at this session's close-out.
- Phase 0 ledger reconcile: `CHANGELOG.md` and `HANDOFFS.md` frontiers both at `HEAD` `8e62af6`, no gap,
  nothing backfilled. 3 receipts, so the retention trim (`--cut 2 --force`, after this claim) is owed.
  S178's gate citation re-run in a `--no-local` clone of `fbdd47d`: `quality_ratchet: 10/10 pass · 0 fail ·
  0 unmeasured · results 1552052a766d · manifest 8d8ddc767cdc`, identical to the receipt. `upstream/main`
  still `6b29d3d`; PR #83 still open at `219fb9d`; no open upstream issues. Dashboard 76/100, high risk (the
  ledger past the refusal). `context_budget.py --status` exit 2 with S178's rows (runner 55,406 B,
  `SAFEGUARDS.md` 17,024 B, read-set total 72,430 B). The two Phase 0 instrument snapshots ride with this claim.
- **The trim was trialled before it was offered,** in a `--no-local` clone of `8e62af6`: 103 of 162 records
  to `docs/archive/CHANGELOG-through-2026-09-16.md`, live 262,253 → 98,347 B, the shard's `.verify.sh` exit 0
  before and after the commit, gates 10/10 with the suite at 300 / 0 / 0 as untrimmed, and the dashboard's
  high risk gone.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-17 · [BL-57] S178 close-out — P5 done by merge; BL-54 next, before P6

- `HANDOFFS.md`: S178's receipt is complete (self 7, S177 scored 7), with the Phase 3A evaluation and
  self-assessment beneath it. The gate citation comes from a `--no-local` clone of `fbdd47d`:
  `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results 1552052a766d · manifest 8d8ddc767cdc`; the
  suite read 300 / 0 / 0.
- This close-out takes `CHANGELOG.md` past the 262,144 B hard read refusal. Under the operator's standing
  decision a trim is now raised with the operator, not taken; the receipt's next steps ask it.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S178 — P5 recorded: plan S178 block, BL-57 and BL-54 rows, fork Learning #71

- `docs/planning/changelog-rules-contradictions-plan.md`: the status line says P5 is done by merge and BL-54
  comes before P6. The S178 block, items (12)–(15), covers BL-54 now biting, the fork-only test, F5's claim
  now false on fork `main`, and `README.md`'s stale cost section.
- `docs/planning/BACKLOG.md`: the BL-57 row is rewritten, not extended (P5 done, next BL-54 then P6–P11), and
  the BL-54 row is marked NEXT with the measured cause. `docs/FORK_LEARNINGS.md` #71: run the phase's DONE
  checks on every route before recommending one; routes to the same tree differ in history.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S178 — `trimmer-unit-tests` floor tightened 123 → 124, the count measured after the merge

- The merge brought `bl57/changelog-rules`' trimmer tests. `quality_ratchet.py --run` measured **124** in a
  `--no-local` clone of `1664860` (results `839fb8a9f80a`), above the 123 floor. The manifest says a tightening
  is owed whenever a measured value rises. The ratchet's `--precommit` passes it: a tightening needs no
  approval.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S178 — `tests-sh-passed` floor lowered 327 → 294: Test 27 left with the carve-out (operator-approved loosening, `--no-verify`)

- **Approval:** the operator's D10 answer (S178, picker) approved lowering this floor to the count measured
  after the removal. This is the loosening itself, in its own commit, with its reason here, as
  `.quality-gates.json` and `SAFEGUARDS.md` §Blast Radius Limits require. The hook's ratchet refused it when
  staged (*"floor lowered 327 -> 294"*, exit 2), so it is committed with `--no-verify`. The manifest's
  history records the bypass, and the dashboard reports it.
- **The figure is measured:** `quality_ratchet.py --run` in a `--no-local` clone of `1664860`, with
  `HANDOFFS.md` cut to two receipts (the state a trimmed ledger returns to, fork Learning #70), read
  **294 passed, 0 failed** (results `839fb8a9f80a`). That is 327 − 34 (Test 27) + 1 (Test 20 (b2)). An
  earlier run read 293 with Test 9 failing on GitHub's API rate limit; that value was not used, because a
  floor must not absorb a Test 9 failure.
- A new `_fork_loosening_d10` note in the manifest carries the same record.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S178 — two fork-only sentences the one-home rules made false: `BOOTSTRAP.md`'s seed-migration step and `README.md`'s archive budget

- **Found by re-running plan §9.1's inventory on the merge and diffing it against the branch's:** 1,128
  matching lines exist only on fork `main`, in 22 files. Most are code or measured history. Two present-tense
  rules contradicted §The Action Ledger:
  - `starter-kit/BOOTSTRAP.md:383` (distributed; the fork's S41 text, `12463dd`) told an adopter to bring
    *"the `## Size, and when to archive` section in both files"* into its ledgers. The `CHANGELOG.md` seed
    no longer has that section. The step now says: for `CHANGELOG.md` since `ledger-format: 2`, replace the
    text above the first entry with the seed's header, as `:85` already says; for `HANDOFFS.md`, the section.
  - `README.md:413` (the fork's S42 text, `8804635`) gave *"64 KB per ledger"* as the trimmer's default
    budget (`DEFAULT_BUDGET_BYTES` is 196,608 B) and said both seeds carry the size section. It now names
    the constant without a figure, calls archiving `CHANGELOG.md` optional, and says only the `HANDOFFS.md`
    seed has the section.
- **Found, not fixed (scope):** `README.md`'s cost section (`:374`–`:404`) still describes a 2,000-line cap
  and seed doctrine sizes measured on 2026-08-04. It is fork-only measured history and needs its own
  rewrite. Recorded for P12 in the plan.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S178 — P5 step 2: this ledger's front matter and `HANDOFFS.md`'s retention line follow the one-home rules

- **`CHANGELOG.md` front matter, five changes:**
  - The rules *"live in [`FRAMEWORK_APPARATUS.md` §The Action Ledger]"*, and the seed *"points there"*. It
    said the rules and the seed both *"live in `starter-kit/CHANGELOG.md`"*, which the merge made false.
  - The audit takes any backlog id (`BL-[^]]+`) and lists shards with `git ls-files`, the home's cross-shell
    form. It reads **638 in zsh and bash alike, equal to the heading count**. At Phase 0 the old form, the
    new form in each shell and the heading count all read 635, so widening the id changed nothing here.
  - `[BL-<N>]` becomes `[BL-<id>]` in the tag definitions, and *"this repo has no
    `docs/planning/BACKLOG.md`"* (upstream's wording, false here) becomes *"upstream has no …"*.
  - A new **Claims** paragraph (C7): a claim commit carries an *(in progress)* entry; the crash breadcrumb is
    the pending receipt, since this repo keeps no `SESSION_NOTES.md`; the hook exempts no claim (D10).
  - *When to archive again — a rate, not a level* (the 2,000-line `READ_CAP_LINES` rate rule) becomes the
    operator's decision: archiving optional, `--check` the only trigger statement, no trim at it
    (`3745748`, reaffirmed at S177), a trim raised only past 262,144 B. `git show cba2166:CHANGELOG.md`
    recovers the old text. Net −959 B before this entry.
- **`HANDOFFS.md` front matter (C4):** Phase 0 counts receipts and reports; a trim above 2 is its own action
  after that report, never inside Phase 0.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S178 — D10: the pre-commit hook's Phase 1B claim carve-out and its Test 27 are removed (operator decision)

- **Decision (operator, S178, picker, after a plain-language explanation):** remove the carve-out. It was
  added at S32 (`a56dff8`, 2026-08-03), when claims wrote no ledger entry and every claim shipped with
  `--no-verify`. 61 claims used it, the last S95 (`a35a14f`, 2026-08-17); all 94 claims since carry an
  *(in progress)* entry, which Q4 A (S162) makes the rule. Upstream's hook never had it.
- **Change:** `.githooks/pre-commit` is now byte-identical to `bl57/changelog-rules`' hook (blob `a2457774`):
  the carve-out, its `--no-renames` (which only guarded the carve-out) and the refusal text's exemption
  paragraph go. `bin/tests.sh` Test 27 (508 lines, 34 rows) is replaced by a three-line comment; nothing
  outside it used its helpers. Canonical-only: no adopter receives the hook.
- **Shown in a scratch repository with a real `git commit`:** a claim commit staging only `HANDOFFS.md` exits 1
  with *"failure mode #27"* under the new hook and 0 under the old one; with a `CHANGELOG.md` entry
  co-staged it exits 0 under both.
- **Owed next, in its own commit:** the suite loses 34 rows, so `tests-sh-passed` (327) must come down to the
  measured count, on the same operator approval.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S178 — a fork-only dashboard test read the live `CHANGELOG.md` seed's fenced examples, which P1 moved; it reads the frozen format-1 seed now

- **Change:** `tools/test_methodology_dashboard.py` `test_fenced_records_are_not_counted` (`TestS38TrimTriggerRow`,
  fork-only). Its fixture control asserted that `starter-kit/CHANGELOG.md` holds fenced dated headings; the
  ledger-format-2 seed holds none, so the merge below failed Test 18 with *"0 not greater than 0"*. This is the
  plan's hazard 6 in a test the branch never had. The control now reads
  `tools/fixtures/seed-CHANGELOG-ledger-format-1.md` with its blob id asserted, as
  `tools/test_methodology_trim.py` does, and the live thin seed is asserted to hold 0 records.
- **Verified:** the dashboard suite runs 336 tests, OK. A fence-blind record-counter mutant fails the test.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S178 — P5: fork `main` merges `bl57/changelog-rules` (`83a12f0`), adopting the one-home `CHANGELOG.md` rules (merge `22ce71b`)

- **Operator decisions (S178, picker):** merge the branch rather than port it (plan §P5 wrote a port), so the
  branch's P1–P4 commits enter fork history and the resync after the upstream PR merges does not re-resolve
  them (#80 and #82 were merged upstream as real merge commits). And D10: remove the hook's claim carve-out,
  including lowering the `tests-sh-passed` floor once Test 27 goes; both come in later commits.
- **The merge** (base `64f23bf`; the branch's net change is 16 files): 5 conflicts, 9 hunks, as
  `git merge-tree` predicted. `CHANGELOG.md` ours (the branch's file is upstream's ledger, and its BL-57
  entries record work this ledger already records); `bin/_manifest.py` and `bin/tests.sh` theirs (the fork's
  S41 marker design, which BL-57 replaces for `CHANGELOG.md`); `CLAUDE.md` the fork's row naming the ledger
  rules; `starter-kit/SESSION_RUNNER.md` the branch's Phase 3F bullet plus the fork's `Model:` sentence,
  re-pointed from the seed's format section to `FRAMEWORK_APPARATUS.md` §The Action Ledger (runner −14 B).
- **Checked on the merge:** the 8 files identical between `main` and the base equal the branch's blobs; in the
  8 files where `main` differs from the base, and in both ledgers and the budget config, the differences
  from the branch are exactly the fork's own changes plus the resolutions above (a line-multiset comparison). Suite in a `--no-local` clone: 332 passed / 2 failed / 0
  skipped against the parent's 332 / 1 / 0. The row diff is Test 20 (b2) swapped for the branch's
  frozen-seed pair (+1) and Test 18 failing (fixed above). Test 9 fails on both from GitHub API rate limiting.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S178 claim — P5 of the `CHANGELOG.md` rules plan: fork `main` adopts the one-home rules (in progress)

**Deliverable:** P5 of [`docs/planning/changelog-rules-contradictions-plan.md`](docs/planning/changelog-rules-contradictions-plan.md)
(§P5, with the S173 block overriding its port command): bring BL-57's own change from branch
`bl57/changelog-rules` (`83a12f0`) onto fork `main`, including this repo's own ledger front matter and the
D10 decision on the pre-commit hook's claim carve-out. Chosen by the operator after Phase 0 (picker).

- **Pre-flight, re-derived at Phase 0:** `upstream/main` is still `6b29d3d`, 0 commits ahead of fork `main`;
  PR #83 is still open at `219fb9d`. `git merge-tree --write-tree --name-only main bl57/changelog-rules`
  lists 5 files (`CHANGELOG.md`, `CLAUDE.md`, `bin/_manifest.py`, `bin/tests.sh`,
  `starter-kit/SESSION_RUNNER.md`), the set S177 computed. Merge vs port is measured before choosing.
- Phase 0 ledger reconcile: `CHANGELOG.md` and `HANDOFFS.md` frontiers both at `HEAD` `fc4fe0c`, no gap,
  nothing backfilled. 2 receipts, so no Phase 0 trim. S177's gate citation re-run in a `--no-local` clone of
  `fc4fe0c`: `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results db4e547cc884 · manifest
  c09d7e7f9109`, identical to the receipt. Dashboard 76/100, medium risk. `context_budget.py --status`
  exit 2 with the rows S177 recorded (runner 55,420 B, `SAFEGUARDS.md` 17,024 B, read-set total 72,444 B).
  `methodology_trim.py --file CHANGELOG.md --check` fires at 251,064 B; not trimmed, by the operator's
  standing decision. The two Phase 0 instrument snapshots ride with this claim.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [ad hoc] S178 — fork `main` pushed to `origin`, `c857e50..fc4fe0c` (non-commit action, operator go-ahead)

- **Action:** `git push origin fc4fe0c:refs/heads/main`, `c857e50..fc4fe0c`, a fast-forward of 1 commit: `fc4fe0c`
  (S177's receipt updated with what followed its close-out). Before the push, a guard confirmed a clean tree, that
  `origin/main` still read `c857e50`, and that exactly that one commit was ahead in a fast-forward. Afterwards
  `git ls-remote origin refs/heads/main` read `fc4fe0c07a0ecdcf4dc691013ba53c100908927e`. The go-ahead was the
  operator's S178 Phase 0 picker answer *"Push it now"*. Fork only; nothing sent upstream.
- **This recording commit is pushed too**, under the standing push-record grant, so it records its own push.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [ad hoc] S177 follow-up — the S177 receipt's next steps updated for what happened after close-out

- `HANDOFFS.md`, S177's receipt only. `next_steps` items (2) and (3) are replaced by their outcomes: fork `main` was
  pushed (`9b96ac1..7b55ee3`, `7b55ee3..70265f3`, then `c857e50` under the push-record grant), and the upstream
  test finding is BL-62, riding BL-57's P12 PR. Gotcha (7) carries the ledger's size at this update and the
  grant is named. Item (1)'s P5 conflict set was recomputed against `c857e50`: still the same 5 files. The same
  edit was made after S175's close-out (its receipt opens `next_steps` with the operator's later decision).
- Prepared for a new session: tree clean, `main` level with `origin`, 0 commits behind `upstream/main`
  (`6b29d3d`), PR #83 still open at `219fb9d`, 2 receipts (the next claim makes 3, no Phase 0 trim).
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [ad hoc] Operator decision: push records are pushed to `origin` without asking (standing grant)

- **Decision (operator, after S177, in their own words):** *"yes, push the push records without asking"*.
- **Scope, and nothing wider:** a commit whose only change is the `CHANGELOG.md` entry recording a push the operator
  already authorized goes to fork `origin` `main` without a separate ask. It must be a guarded fast-forward, read
  back with `git ls-remote`. Such a commit records its own push in that same entry, so no further record is owed
  and the chain ends there. Every other push still needs its own go-ahead, and so does every upstream action.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [ad hoc] S177 follow-up — fork `main` pushed to `origin`, `7b55ee3..70265f3` (non-commit action, operator go-ahead)

- **Action:** `git push origin 70265f3:refs/heads/main`, `7b55ee3..70265f3`, a fast-forward of 2 commits: `80f0eef`
  (the record of the previous push) and `70265f3` (BL-62). Before the push, a guard confirmed a clean tree, that
  `origin/main` still read `7b55ee3`, and that exactly those two commits were ahead in a fast-forward. Afterwards
  `git ls-remote origin refs/heads/main` read `70265f390acfd3c5cdb2c762feb573677fb0fc14`. The go-ahead was the
  operator's *"push the two local commits to origin"*. Fork only; nothing sent upstream.
- **This recording commit is pushed too**, under the standing grant recorded in the entry above.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-62] S177 follow-up — BL-62 raised: upstream's partition test sums every whole-read class as one Read; it rides BL-57's P12 PR (operator decision)

- **Raised on the operator's request** after S177's explanation. **Decision (operator): carry it in BL-57's P12 pull
  request, not as a standalone upstream issue.** `tools/test_context_budget.py:1256`
  (`test_whole_read_class_token_ceilings_partition_the_read_cap`, upstream `008d656`) applies the one-Read token
  sum to every class in `WHOLE_READ_CLASSES`, where only the read-set pair is read together. It fired at resync
  M2 against the fork's two read-mandated ledgers and was worked around at `0e8c6ac`.
- **Checked before writing:** no existing backlog item covers it (the test name and *"whole-read class"* grep
  empty in `BACKLOG.md` and `BACKLOG-DETAIL.md`). Upstream's root config gives token ceilings only to its
  read-set pair and one resident file, so upstream cannot see it. No test file has a `bin/_manifest.py` row,
  so no adopter is affected.
- **Files:** `docs/planning/BACKLOG-DETAIL.md` gains `#bl-62` (the proof `BACKLOG-DETAIL.md.verify.sh` still
  exits 0); `docs/planning/BACKLOG.md` gains its index row, the open list gains BL-62, and the BL-57 row says
  P12 carries it. Nothing outward.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [ad hoc] S177 follow-up — fork `main` pushed to `origin`, `9b96ac1..7b55ee3` (non-commit action, operator go-ahead)

- **Action:** `git push origin 7b55ee3:refs/heads/main`, `9b96ac1..7b55ee3`, a fast-forward of 41 commits: S177's
  claim, the three resync merges `421ebf9`, `7245f79`, `d4ac950` with the upstream commits they bring, the M2
  fixes, the config restatement, D3, the `HANDOFFS.md` trim and fold, D2, plan §8 and the close-out. Before the
  push, a guard confirmed that `origin/main` still read `9b96ac1`, that local `main` read `7b55ee3`, and that the
  push was a fast-forward. Afterwards `git ls-remote origin refs/heads/main` read
  `7b55ee30b5814c04214ada57c8ab722e0832f539`. The go-ahead was the operator's message after S177's close-out
  (*"push fork main (9b96ac1..7b55ee3) to origin"*). Fork only; nothing sent upstream.
- **Not pushed:** this recording commit, which is outside the range the go-ahead named.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S177 close-out — resync R2 done: fork `main` contains `upstream/main`; D2, D3 carried out; BL-57's P5 is next

- **Deliverable:** R2 of [`upstream-resync-2026-09-plan.md`](docs/planning/upstream-resync-2026-09-plan.md), recorded in its
  §8. Merges `421ebf9` (M2), `7245f79` (M3), `d4ac950` (M4); `git rev-list --count main..upstream/main` = 0.
  D3 `e1b6bdf` (2.18.0), D2 `e55f204` (`tests-sh-passed` 327, `dashboard-unit-tests` 336), `HANDOFFS.md` trim
  `75056a9` and fold `f4a8ec6`. Two operator decisions: the config restatement `0e8c6ac`, and no
  `CHANGELOG.md` trim (`d23d1a3`).
- **Final, in a `--no-local` clone of `b4c3a45`:** `quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results
  db4e547cc884 · manifest c09d7e7f9109`; `bash bin/tests.sh` exit 0, **327 passed / 0 failed / 6 skipped** (Test 34's
  six rows, stated skips at 2 receipts, the only rows that differ from M4's run); `python3
  starter-kit/methodology_dashboard.py` exit 0, v2.18.0, 76/100, gates panel *"10 declared • 10 pass / 0 fail / 0
  unmeasured"*.
- **This commit:** S177's `HANDOFFS.md` receipt completed with that citation (the D9 lint now binds every
  close-out), the self-assessment (8/10) and S176's evaluation (7/10).
- **Not taken:** pushing fork `main` to `origin` (its own go-ahead); raising upstream's
  `TestThisRepoReadSetPartition` finding (outward, its own go-ahead).
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S177 — resync plan §8 (R2 as carried out), the BL-57 row, and fork Learnings #69–#70

- [`upstream-resync-2026-09-plan.md`](docs/planning/upstream-resync-2026-09-plan.md) §8 records R2 as carried out
  and overrides §2–§5 and §7 where they differ: per-stage suite results, the measured conflict sets (7 / 11 / 1),
  M2's three unpredicted red rows and the operator's config decision, the `HANDOFFS.md` deviation at M2, the
  whole-file `CLAUDE.md` resolution, the operator's no-trim decision, D2's values and why 327, D3, and the
  `context_budget.py --status` diff (exit 2 at both ends, no row changes status). Its status line now reads
  carried out. **Next, computed:** `git merge-tree --write-tree --name-only main bl57/changelog-rules` lists 5
  conflicting files for P5.
- `docs/planning/BACKLOG.md` BL-57 row: R2 done, P5 next.
- `docs/FORK_LEARNINGS.md` gains **#69**: an arriving test that reads the repository's own config binds
  whichever config a merge keeps. It also gains **#70**: a count floor holds only if it is measured at the
  state every close-out leaves. `bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15
  --no-citations` passes: 56 rows, contiguous 15..70, none over 1,500 B.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S177 — D2: this repository's quality gates tightened to the fork's measured values (`tests-sh-passed` 327, `dashboard-unit-tests` 336)

- **Measured:** `python3 starter-kit/quality_ratchet.py --run` in a `--no-local` clone of `f4a8ec6`, after the
  `HANDOFFS.md` trim and fold, gave **`quality_ratchet: 10/10 pass · 0 fail · 0 unmeasured · results
  508b2b5489f3 · manifest 97a7aab85b9a`**. The measured values: `tests-sh-passed` 327, `tests-sh-failed` 0,
  `dashboard-unit-tests` 336, `context-budget-unit-tests` 118, `trimmer-unit-tests` 123,
  `ratchet-unit-tests` 45, and 0 on each of the four exit-code gates.
- **Change, `.quality-gates.json`:** `tests-sh-passed` 139 → **327** and `dashboard-unit-tests` 226 →
  **336**. The other three count gates already sat at their measured values, and every max-gate sits at 0.
  Both changes tighten, which the manifest's own rule lets through without approval, and the chained
  `--precommit` passed on this commit. A fork-only note key `_fork_tightening` records the values and why.
  Every gate's name, direction, command and extract pattern still equals `upstream/main`'s, and
  `config_defects` is `[]`.
- **Why 327 and not 333:** `bin/tests.sh` Test 34 turns six rows into stated skips when `HANDOFFS.md` holds
  fewer than three receipts. Every close-out leaves two and every claim makes three, so the same tree reads
  333 at M4 (6 receipts) and 327 here. A floor taken at 333 would refuse every close-out's gate run.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [ad hoc] S177 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

- The pointer block `75056a9` wrote into `HANDOFFS.md`'s front matter is now one row of
  [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md) (4 records, 2026-09-15 → 2026-09-16,
  `HANDOFFS-through-2026-09-16-4.md`, v1.5.0). The block is deleted, taking the file from 16,224 to 15,768 B,
  in its own commit per the index's fold rule. `docs/archive/HANDOFFS-through-2026-09-16-4.md.verify.sh` exits
  0 after the fold, `check-handoff --all --allow-pending` passes on 2 receipts, and `bin/check-links` exits 0.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-16-4.md` (4 record(s), 47,200 B → 16,224 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **4** record(s) (2026-09-15 → 2026-09-16) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-16-4.md`](docs/archive/HANDOFFS-through-2026-09-16-4.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-16-4.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-16-4.md.verify.sh)
rather than trusting a digest printed here. Live file 47,200 B → 16,224 B (−65.6%).

### 2026-09-16 · [BL-57] S177 — resync stage M4 merged (`d4ac950`), fork `main` now contains `upstream/main`; D3: `DASHBOARD_VERSION` 2.18.0

- **Merge `d4ac950`** (parents `d23d1a3`, `6b29d3d`), the last of the four stages. One file conflicted,
  `CHANGELOG.md`: upstream's one new entry (*"PR #82 merged — post-merge verification on main and the first
  tightening"*) now sits above its upstream neighbour, after the fork's 2026-09-16 entries. `HANDOFFS.md`
  merged cleanly and was rebuilt by the same rule: upstream's S23 sits above S22, after the fork's receipts,
  and `check-handoff --all` passes on 6 receipts. `.quality-gates.json` is upstream's (`fb81c4b`:
  `tests-sh-failed` max 0, `tests-sh-passed` min 139) until D2's commit. `git rev-list --count
  main..upstream/main` is **0**. The plan's M3 and M4 were predicted against a pre-M2 tree and are now
  measured: 11 conflicting files at M3 and 1 at M4, against the 12 and 12 computed at `9b96ac1`.
- **Measured on the merge, in a `--no-local` clone at `d4ac950`:** `bash bin/tests.sh` exit 0, **333 passed / 0 failed / 0
  skipped**, and its digit-masked rows are identical to M3's.
- **D3, this commit:** `DASHBOARD_VERSION` 2.17.0 → **2.18.0** in both twins. It is the next minor version
  above both numbering lines, because the merge brings upstream's 2.11.0 gates panel (changed output) and
  2.11.1 history walk. The comment above the constant now describes 2.18.0 and points to git for 2.17.0,
  following `0afe9d6`'s pattern. Both pins in `tools/test_methodology_dashboard.py` (the module attribute
  and the starter-kit source text) and the test's docstring follow. A whole-file search (fork Learning #68)
  found exactly those sites. The only remaining `2.17.0` text is in the two new comments, which name the
  prior version on purpose. The dashboard suite: 336 tests OK in the live checkout.
  `python3 starter-kit/methodology_dashboard.py` exits 0, reports `v2.18.0` at 76/100, and `dashboard.html`
  shows the gates panel (*"Quality Gates: 10 declared, never run"*).
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S177 — resync stage M3 merged (`7245f79`): PR #82 whole, the repository's own gates, and the ratchet chained into `pre-commit`; `CHANGELOG.md` stays untrimmed (operator decision)

- **Merge `7245f79`** (parents `0e8c6ac`, `64f23bf`). There were 11 conflicting files, not the 12 computed
  against `9b96ac1`: M2 had already taken upstream's `bin/tests.sh` block. **`.context-budget.json`:** ours.
  **`.githooks/pre-commit`:** upstream's ratchet block, then the fork's `--no-renames` comment and
  staged-path line, which appears exactly once. **`CLAUDE.md`:** the fork's whole file, which also refuses
  upstream's shortened rows in hunks git would have merged cleanly. It gains starter-kit rows for
  `context_budget.py` and `quality_ratchet.py` and a Tools row for their test suites, taking it from
  11,808 to 12,667 B. **`README.md`, `docs/tutorials/T1_setup.md`:** upstream's lists; every name on the
  fork's side is on upstream's. **`bin/check-handoff`:** the fork's block, then upstream's
  `declared_gate_count` and `validate_gate_citation`. Every line either side added is present in order
  (528 and 40). **Dashboard twins and their test file:** `DASHBOARD_VERSION` pins stay 2.17.0.
  **`CHANGELOG.md`:** upstream's quality-ratchet entry is replaced in place by its completed text (heading
  *"PR opened, not merged"*), and its one new entry sits above its upstream neighbour. **`HANDOFFS.md`:**
  upstream's S22 and its completed S20 follow the fork's receipts, and S21 stays in its shard.
  `check-handoff --all` passes on 5 receipts. Every upstream-only path equals `64f23bf`'s, and so does
  `starter-kit/FRAMEWORK_LEARNINGS.md` (D1). `SAFEGUARDS.md` is 17,024 B and the runner 55,420 B, both as
  plan §2.2 measured. `DISTRIBUTION` has 29 rows, and `.githooks/commit-msg --selftest` exits 0.
- **Measured on the merge, in a `--no-local` clone at `7245f79`:** `bash bin/tests.sh` exit 0, **333 passed / 0 failed / 0 skipped**.
  The digit-masked row diff against the M2 checkpoint shows upstream's 11 new rows passing (the manifest-removal
  cases, this repository's gates, the hook chain, and `check-handoff`'s D9 lint) and no flips.
- **The M2 checkpoint, in a clone at `0e8c6ac`:** exit 0, **322 passed / 0 failed / 0 skipped**. Its rows are
  identical to the trial that preceded the config commit.
- **This commit is the first the ratchet's `--precommit` checks:** the hook M3 merged runs it before the
  ledger gate, and it passed.
- **Decision (operator, picker, during M3's suite run): no `CHANGELOG.md` trim in R2.** The resync plan's R2
  step 3 and §7 item 4 schedule one at the trimmer's 196,608 B trigger. They do not cite the operator's
  2026-09-14 decision not to trim this file at that trigger (`3745748`; `BACKLOG-DETAIL.md`, BL-57), and that
  decision governs. `--check` keeps firing, and that is stated. As S171 did, a trim is raised with the
  operator only if the file passes the 262,144 B hard read refusal. It is 232,771 B after M3's merge.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S177 — `.context-budget.json` restates its token ceilings so upstream's partition test passes, every verdict unchanged (operator decision, an exception to D11)

- **Decision (operator, picker, after `8c429ed`):** *"Restate the config"*, chosen over patching the fork's copy
  of `tools/test_context_budget.py` and over stopping R2 after M2. It is an exception to D11 and to plan §4's
  *"no ceiling changes"*, taken because both limits in effect stay as they were.
- **Change, `.context-budget.json` only:** `starter-kit/SESSION_RUNNER.md` declares `max_tokens` 18,222 and
  `starter-kit/SAFEGUARDS.md` declares 6,777. These are `int(41,364 / 2.27)` and `int(15,386 / 2.27)`, the
  ceilings the tool already derived from their byte ceilings; they sum to 24,999, inside the 25,000-token
  read cap. `HANDOFFS.md` and `docs/planning/BACKLOG.md` drop the `max_tokens` 25,000 declared at `97c8066`,
  which the tool derives anyway by clamping `max_bytes / 2.27` to the cap. Each of the four entries' notes
  says so in its first sentence. Upstream's test file is untouched.
- **Measured:** `context_budget.py --json` before and after on the live tree: every row keeps its status,
  sizes, class totals and finding text (aside from the *"derived from max_bytes"* suffix), `config_defects`
  stays `[]`, and only `ceiling_derived` flips on the four rows. `tools/test_context_budget.py`: 118 tests
  OK. **The whole suite, in a throwaway `--no-local` clone of `8c429ed` with these values committed: exit 0,
  322 passed / 0 failed / 0 skipped**, and a digit-masked row diff against M2's run shows exactly its three
  FAIL→PASS flips (this change plus `8c429ed`'s two fixes).
- **Left for later, outward:** upstream's `TestThisRepoReadSetPartition` sums *every* whole-read class against
  one Read, but a class of separately-read ledgers is not one Read. Raising that upstream is its own go-ahead.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S177 — resync stage M2 merged (`421ebf9`); two of its three red rows fixed, the third waits on the operator

- **Merge `421ebf9`** (parents `374bd8c`, `cca7941`): stage M2 of
  [`upstream-resync-2026-09-plan.md`](docs/planning/upstream-resync-2026-09-plan.md) §5 R2, PR #82 through
  its P3. The 7 conflicting files were resolved per §2.3. `.context-budget.json` keeps ours (D11).
  **`CHANGELOG.md`:** upstream's one new entry (the quality-ratchet slice, still headed
  `CHANGELOG: pending` here) sits after the fork's entries for 2026-09-15, above upstream's
  "Merged PR #80". Removing it gives back ours byte for byte. **`HANDOFFS.md`: ours, unchanged — a deviation
  from §7 item 3.** Upstream's only new receipt at this stage is S20, a `status: pending` stub. Below the
  fork's receipts it fails `check-handoff --all --allow-pending`, because only the newest receipt may be
  pending. Test 34's presence control runs exactly that check on the live ledger, and upstream completes S20
  at M3, so the completed S20 is kept there instead (§2.4: an incoming receipt is checked against ours
  before it is kept). **`bin/tests.sh`:** the fork's Tests 36–40, then upstream's ratchet block; additions
  only. **Dashboard twins:** `DASHBOARD_VERSION` stays 2.17.0 until D3's own commit. The fork's
  `_FRAMEWORK_INSTALLED_CONTENT` gains `quality_ratchet.py` and `.quality-gates.json` in manifest order,
  with upstream's patterns and signatures, checked equal by evaluating both modules. Upstream's
  `_FRAMEWORK_FILE_SIGNATURES` dict is dropped, and the docstring's *"no tool's constant satisfies
  another's"* now names the one pair that does (both name theirs `VERSION`). **Test file:** both imports,
  2.17.0 pins, and two pre-existing mentions of the dropped dict renamed.
- **Measured on the merge, in a `--no-local` clone at `421ebf9`:** `bash bin/tests.sh` exit 1, **319 passed /
  3 failed / 0 skipped**, against 309 / 0 / 0 at the claim `374bd8c`. A digit-masked row diff shows upstream's
  11 new ratchet rows passing and exactly three pass→fail flips:
  1. **The dashboard suite:** `test_every_shipped_executable_is_recognized_from_its_real_source` pins 4
     installed files and the table now holds 6. **Fixed in this commit** (`tools/test_methodology_dashboard.py`,
     4 → 6). The guard's loop checks each file against its real shipped source, so it is what proves the two
     new table entries. With `quality_ratchet.py`'s rule neutralized the test fails, and the same holds for
     `.quality-gates.json`; with neither neutralized it passes. The suite: 332 tests OK.
  2. **Test 28:** the fork's never-overwrite row in `starter-kit/BOOTSTRAP.md` did not name the arriving
     seed. **Fixed in this commit:** the Adopter-owned row names `.quality-gates.json` and the Tracked row
     names `quality_ratchet.py`. The row is fork-only (upstream's `BOOTSTRAP.md` has no such table), and its
     converse check still finds no tracked file in it.
  3. **The context-budget suite: not fixed, operator decision pending.** Upstream's new
     `TestThisRepoReadSetPartition` (P0, `008d656`) asserts two properties of this repository's root
     `.context-budget.json`, which D11 keeps as the fork's. First, the read-set pair declares `max_tokens`:
     the fork's declares byte ceilings only. Second, every whole-read class's token ceilings sum within one
     25,000-token Read: the fork's `read-mandated` class declares 25,000 on each of `HANDOFFS.md` and
     `docs/planning/BACKLOG.md`, 50,000 in total. Three ratified constraints cannot all hold: D11 with §4
     (no ceiling changes), R2's DONE (`tools/test_context_budget.py` identical to upstream's), and a green
     suite.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S177 claim — R2 of the resync plan: merge stages M2–M4 (`cca7941`, `64f23bf`, `6b29d3d`), D2, D3 and the trims (in progress)

**Deliverable:** R2 of [`docs/planning/upstream-resync-2026-09-plan.md`](docs/planning/upstream-resync-2026-09-plan.md)
(§5, with §7 overriding): merge the three remaining stages into fork `main`, resolving each per §2.3 and
§7 item 3, then D2's tightening commit, D3's 2.18.0, the `CHANGELOG.md` trim and the `HANDOFFS.md`
retention trim and fold. Chosen by the operator after Phase 0 (picker), over a read-only review of
upstream PR #83.

- **Pre-flight, re-derived at Phase 0:** `upstream/main` is still `6b29d3d`, so R2 gains no stage. PR #83
  is still open at `219fb9d`. `git merge-tree --write-tree --name-only HEAD <target>` against `9b96ac1`
  lists 7 files for `cca7941` and 12 for each of `64f23bf` and `6b29d3d`, the same sets as §7 item 2.
- Phase 0 ledger reconcile: `CHANGELOG.md` frontier at `HEAD` `9b96ac1`, no gap; `HANDOFFS.md` frontier
  `4a0a5a7`, and its two later commits are S176's recorded follow-ups. Nothing backfilled. 2 receipts, so
  no Phase 0 trim. `methodology_trim.py --file CHANGELOG.md --check` FIRES at 204,886 B (owed in R2).
  Dashboard 76/100, medium risk. `context_budget.py --status` exit 2; its `over` rows are the runner (54,363 B),
  `SAFEGUARDS.md` (16,353 B, as §7 item 7 recorded) and the read-set total (70,716 B).
  The two Phase 0 instrument snapshots ride with this claim.

### 2026-09-16 · [ad hoc] S176 follow-up — fork `main` pushed to `origin`, `f1ae291..9aa1eb9`; BL-44 kept open (non-commit action and a grooming decision, operator go-ahead)

- **Action:** `git push origin main`, `f1ae291..9aa1eb9`, a fast-forward of 38 commits: S176's claim, the
  stage-M1 merge `5c2bd59` with the 28 upstream commits it brings, D1's four commits, the `HANDOFFS.md` trim
  and fold, the close-out and the BL-44 note. Before the push, a guard confirmed `origin` still read `f1ae291`
  and that it was an ancestor of `main`. Afterwards `git ls-remote` read
  `9aa1eb9304773f3987a2566186420145b2f468e7`, equal to local `main`. The go-ahead was given by picker after
  S176's close-out (*"Push fork main to origin"*), and this recording commit is pushed under it. Fork only;
  nothing sent upstream.
- **Decision (same picker):** **BL-44 stays open.** `8cfaf0d` fixed its span half; naming the reserved gap
  in the message remains. The backlog row records the decision.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-44] S176 follow-up — the check-learnings span fix in `8cfaf0d` was BL-44, not a new finding

- **Correction to the record:** `8cfaf0d`'s commit message, its ledger entry and the S176 receipt describe
  the `contiguous 1..65` message as a defect found this session. It is **BL-44**, raised at S109
  (`docs/planning/BACKLOG-DETAIL.md` §BL-44), and my Phase 0 backlog read did not reach it. The fix reads the span
  off the parsed rows, which is BL-44's core defect. BL-44's proposed fix also names the reserved gap in the
  message (*"#1..#38, 1 reserved (#14)"*), and `8cfaf0d` does not. **BL-44 stays open**; its row now says so, and
  closing it is the operator's decision.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S176 close-out — resync R1 done: stage M1 merged, D1 carried out, suite green; R2 is next

- **Deliverable, done:** R1 of [`upstream-resync-2026-09-plan.md`](docs/planning/upstream-resync-2026-09-plan.md). Merge
  `5c2bd59`, then `8c35872`, `8cfaf0d`, `82f0d3a`, `4ef6390`, the retention trim `084ba1b` and its fold
  `28ae585`, each with its own entry below. R1's DONE criteria, run bare on `28ae585`: `0fd003a` is an
  ancestor of `main`; no unmerged paths; the distributed learnings file equals `0fd003a`'s; the fork file's
  rows equal `1f34e75`'s 15–66; `check-learnings` (both tables), `check-handoff --all --allow-pending`,
  `check-links` and `commit-msg --selftest` all exit 0. **Suite in a `--no-local` clone of `28ae585`: exit 0,
  303 passed / 0 failed / 6 skipped**, the six being Test 34's stated rows at 2 receipts (digit-masked
  row diff against `4ef6390`'s 309 / 0 / 0).
- **This commit:** the `HANDOFFS.md` receipt (`status: complete`, self 8, predecessor S175 8); the plan's
  new **§7, *R1 as carried out — what R2 inherits***, and its status line. §7 holds the conflict sets
  computed against `28ae585` (M2 7 files, M3 and M4 12). It records that R1's trim makes `HANDOFFS.md`
  conflict at every later stage, that `cca7941` does not contain `0fd003a`, that the `CHANGELOG.md`
  trigger already fires (200,985 B), and the 26 citation sites against D1's 23. It also diffs
  `context_budget.py --status`: `SAFEGUARDS.md` ok -> over at 16,353 B, recorded, not remedied. Also here:
  BL-53's and BL-57's backlog rows, and **fork Learnings #67** (S175's deferred learning: an arriving hook
  binds the suite's own fixture commits) and **#68** (a grep inventory is line-scoped; wrapped references
  are invisible to it), 1,175 B and 1,043 B, checked from #15.
- **Not done, and not this session's:** R2; the `CHANGELOG.md` trim (R2 step 3); any push. Fork `main` is
  ahead of `origin/main` by 37 commits with this one: 9 of this session's and the 28 upstream commits the merge brought. Pushing
  needs the operator's go-ahead.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [ad hoc] S176 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

- **Fold** of `084ba1b`'s pointer block by the index's rule (`docs/HANDOFFS_ARCHIVE_INDEX.md:51`): one
  124 B row at the bottom of the table, `| 9 | 2026-09-14 → 2026-09-16 | HANDOFFS-through-2026-09-16-3.md |
  v1.5.0 |`, and the block deleted from `HANDOFFS.md`, in its own commit as the rule requires (fork Learning #58).
  The shard holds S174 and upstream's S21, S19–S13, the receipts the M1 merge brought.
- **Also in `HANDOFFS.md`'s front matter:** the fold comment's `Learning #58` now reads *fork Learning #58*.
  Commit `82f0d3a`'s inventory skipped the two ledgers as history, but this comment is a live
  instruction; an anchored-fence search of both ledgers' front matter found no other citation past #13.
- **Front matter:** 4,475 B inside the trim commit, 4,024 B after the fold (4,019 B at S175, plus 5 B
  for *fork* ), against Test 39 A2's 7,168 B reserve. `bin/check-handoff --all --allow-pending` exit 0 on
  2 receipts.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-16-3.md` (9 record(s), 68,571 B → 16,296 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **9** record(s) (2026-09-14 → 2026-09-16) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-16-3.md`](docs/archive/HANDOFFS-through-2026-09-16-3.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-16-3.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-16-3.md.verify.sh)
rather than trusting a digest printed here. Live file 68,571 B → 16,296 B (−76.2%).

### 2026-09-16 · [BL-53] S176 — `CLAUDE.md` routes this fork's Phase 3C learnings to `docs/FORK_LEARNINGS.md`

- **`CLAUDE.md`, new subsection *Where this fork's learnings go*** (7 lines, in the fork-only part of
  *What This Repository Is*): the runner's Phase 3C (`starter-kit/SESSION_RUNNER.md:228`) sends a
  canonical-repo session to the distributed file. On this fork that file is upstream's, so fork
  learnings append to `docs/FORK_LEARNINGS.md`, cited as *fork Learning #N*. This is the one line D1 (A)
  owed (plan §3). It sits outside the table row that upstream rewrites at M3, so it adds no conflict hunk
  there. `CLAUDE.md` is 11,808 B against the 18,600 B resident ceiling.
- **`docs/HANDOFFS_ARCHIVE_INDEX.md:58`:** the fold rule's `Learning #58` link now reads
  *fork Learning #58* and points at `FORK_LEARNINGS.md`. That was the last of the plan's 23 live
  citation sites, 25 with the two wrapped ones.
- **Correction to the entry below, made in place:** its test-file breakdown read *#16 ×9, #26, #43*; the
  sites are #16 ×8, #26 ×2 (the pin's docstring and its message) and #43. The 11 and 18 totals were right.
- **Verified:** every relative link in `CLAUDE.md`, the index and `docs/FORK_LEARNINGS.md` resolves
  (Python); `bin/check-links` exit 0 (105 links, the distributed corpus).
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-53] S176 — live code cites *fork* Learnings, and the two suite rows D1 turned red pass again

- **Citations, following D1 (A):** 18 sites in 5 files now read *fork Learning #N*: both dashboard twins
  `:452` (#16) and the `archiv` result line (#15); `tools/test_methodology_dashboard.py`, 11 sites (#16 ×8,
  #26 ×2, #43); `bin/tests.sh:1713`, `:3003`, `:3089` (#16, #34 ×2). **Two more that the plan's count of 23
  missed:** in both twins the text `Learning`/`#26` wraps across two comment lines (`:409`), which a per-line grep cannot
  see (found with a multi-line Python search). The `archiv` result line also says its #15 row has since
  left the distributed corpus. Ledgers, plans, audits and `README.md` stay as written. `docs/audits/`
  cites several numbers past #13, most of them another project's.
- **Test 18's pin, rewritten as its docstring asks:** `docs/planning/BACKLOG.md` now appears in no
  distributed `.md` file, so the assertion is `[]`. Because `[]` is also what a net that reads nothing returns,
  a presence control first asserts that the root basename's hits include `SESSION_RUNNER.md`. A mutant
  whose net reads `""` fails on that control. The dashboard's disposition comment beside
  `READ_CAP_CLASS_A` is rewritten to match: both locations appear ZERO times. Its corpus count is
  corrected from 22 to 23, measured off `bin/_manifest.py`. The KEEP decision and its warrant are unchanged.
- **Test 37's `add_row37`:** skips any number the fixture's prose reserves (check-learnings'
  `RESERVED_RE` form). At M1 max+1 landed on the reserved `#14`. Measured on a copy of the live
  table: the helper now appends #15 and check-learnings reads OK. A mutant without the skip appends #14
  and fails with *"missing #15"*, the trial's failure.
- **Verified:** `TestPhaseC1ReadCapClasses` 10 OK; the twins `cmp` equal; `py_compile` clean; no added
  line over 102 characters.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-53] S176 — the fork's Learnings #15–#66 move verbatim to `docs/FORK_LEARNINGS.md`, checked from #15

- **Decision carried out:** D1 (A) of the resync plan (§3), ratified after S175. The merge `5c2bd59` made
  the distributed `starter-kit/FRAMEWORK_LEARNINGS.md` upstream's copy (rows 1–13 and the reserved `#14`). This commit gives
  the fork's 52 rows a home.
- **`docs/FORK_LEARNINGS.md` (new, 67,177 B):** a front matter (why the file exists, *fork Learning #N*
  as the citation form, append here from #67, the same append-only and 1,500 B rules), then the table
  header and rows #15–#66. **A Python comparison shows every row byte-identical to rows 15–66 of
  `git show b85851f:starter-kit/FRAMEWORK_LEARNINGS.md`**, in order, with the header row and separator
  identical too. It sits in `docs/`, not `docs/archive/`, because a dashboard test reads every
  `docs/archive/*.md` as a ledger. It is not in `bin/_manifest.py`, so it is not distributed.
- **`bin/check-learnings`:** `--first N` (default 1): rows must be contiguous from N. The default path's
  behaviour is unchanged. The OK line now reads its span off the rows (`min..max`). The count-derived form
  printed `1..65` for the old 65-row table ending at #66, because the reserved `#14` sits inside the span.
- **`bin/tests.sh` Test 32, three new rows:** the fork file is clean from #15; without `--first` it
  reports #1 missing, which proves the flag is read; a deleted row #40 is caught. The three use
  here-strings, not `echo | grep -q`, which can score a match as failed under pipefail. Run standalone:
  9/9 pass. A checker mutant that ignores `first` fails two of the three new rows.
- **`.context-budget.json`:** the on-demand entry is re-pointed from `starter-kit/FRAMEWORK_LEARNINGS.md`
  to `docs/FORK_LEARNINGS.md` (measured 67,177 B, 2026-09-16), and its notes cite *fork* Learnings #26,
  #34, #62/#63 and #16. **The 81,920 B ceiling did not move** (the plan's §4), so this file has 14,743 B
  of headroom where the whole table had 2,437 B. The note says so: BL-53's pressure eased because rows moved,
  not because the retirement question was answered. `context_budget.py --status`: the row reads `ok`.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S176 — resync stage M1 merged (`5c2bd59`), and Test 27.N1b passes the arriving `commit-msg` hook

- **Merge `5c2bd59`** (parents `b85851f`, `0fd003a`): the first of the resync plan's four stages
  ([`upstream-resync-2026-09-plan.md`](docs/planning/upstream-resync-2026-09-plan.md) §5 R1). It is a real
  3-way merge, resolved per §2.3. `.context-budget.json` keeps ours, by D11 (`git diff HEAD` empty).
  `starter-kit/FRAMEWORK_LEARNINGS.md` takes upstream's copy, by D1 (A): byte-identical to `0fd003a`'s, rows 1–13
  and the reserved `#14`. **`CHANGELOG.md`:** upstream's 12 new entries are interleaved by date, and on a
  shared date the fork's come first. A Python check shows each upstream entry verbatim in the result, and
  removing them gives back the fork's file byte for byte. **`HANDOFFS.md`:** upstream's S21 and S19–S13
  follow the fork's receipts. There is no session+date collision, and `check-handoff --all` exits 0 on
  11 receipts. The hooks skip merge commits, so the merge is recorded here, in the next ordinary commit.
- **Measured on the merge, in a `--no-local` clone at `5c2bd59`:** `bash bin/tests.sh` gave **303 passed / 3
  failed / 0 skipped**. The three failures are the ones the plan's D1 trial found (§3): Test 18's Learning
  #26 pin, Test 37's `add_row37` numbering onto the reserved `#14`, and Test 27.N1b. Run on their own:
  the dashboard suite, 321 tests with 1 failure (that pin, and nothing else behind the row); the
  context-budget suite 116 OK; the trimmer suite 123 OK; `bin/check-learnings` exit 0 (13 rows);
  `.githooks/commit-msg --selftest` OK (7 checks).
- **This commit, `bin/tests.sh:1283`:** Test 27.N1b's real fixture commit runs with
  `METHODOLOGY_REQUIRE_COAUTHOR=0`, the documented override of the disclosure gate that arrived with M1
  (`ad7bd37`). The test points `core.hooksPath` at the live hooks and makes a real commit with no trailer,
  so the gate refused the commit before the test could observe `pre-commit`'s claim carve-out. It stays a
  one-line change (plus a comment), because BL-57's P5 removes Test 27 with the carve-out.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [BL-57] S176 claim — R1 of the resync plan: merge stage M1 (`0fd003a`) and carry out D1 (in progress)

**Deliverable:** R1 of [`docs/planning/upstream-resync-2026-09-plan.md`](docs/planning/upstream-resync-2026-09-plan.md)
(§5): merge `0fd003a` into fork `main`, resolve its four conflicts per §2.3, apply Test 27.N1b's one-line
override, and carry out D1 (A). Chosen by the operator after Phase 0 (picker), over BL-61 and a comment on
upstream PR #83.

- **Pre-flight, re-derived at Phase 0:** `upstream/main` is still `6b29d3d`, so R2 gains no stage. PR #83
  is still open at `219fb9d`, with no reviews or comments. `git merge-tree --write-tree --name-only main
  0fd003a` lists `.context-budget.json`, `CHANGELOG.md`, `HANDOFFS.md`,
  `starter-kit/FRAMEWORK_LEARNINGS.md`, the same four as §2.1. The full merge still conflicts in 13 files.
- Phase 0 ledger reconcile: `CHANGELOG.md` frontier at `HEAD` `f1ae291`, no gap; `HANDOFFS.md` frontier
  `a614a89`, and the one later commit only records S175's push. Nothing backfilled. 2 receipts, so no
  Phase 0 trim. Dashboard 76/100, medium risk. `context_budget.py --status` exit 2, as at S175. The two
  Phase 0 instrument snapshots ride with this claim.

### 2026-09-16 · [ad hoc] S175 follow-up — fork `main` pushed to `origin`, `4735c6c..a614a89` (non-commit action, operator go-ahead)

- **Action:** `git push origin main`, `4735c6c..a614a89`, a fast-forward of 6 commits: S175's claim, the
  `HANDOFFS.md` trim and fold, the resync plan, the close-out, and the ratification record. Before the
  push, a guard confirmed that `origin` still read `4735c6c` and that it was an ancestor of `main`.
  Afterwards `git ls-remote` read `a614a89358a3dbaa2436eb2a6d1bec5926bfb880`, equal to local `main`. The
  go-ahead was the operator's message *"push fork main to origin"*, and this recording commit is pushed
  under the same go-ahead. Fork only; nothing sent upstream.

### 2026-09-16 · [BL-57] S175 follow-up — the operator ratifies the resync plan: every recommendation (picker)

- **Decisions, taken by picker after S175's close-out:**
  - **D1 (A), BL-53:** the distributed `starter-kit/FRAMEWORK_LEARNINGS.md` becomes upstream's at each
    merge stage, and the fork's rows #15–#66 move verbatim, numbers kept, to `docs/FORK_LEARNINGS.md`,
    where new fork learnings are appended. Carried out in R1.
  - **D2 (a):** adopt upstream's quality ratchet, then tighten its thresholds to the fork's measured
    values in R2, after stage 4.
  - **D3 (a):** `DASHBOARD_VERSION` 2.18.0 for the merged dashboard.
  - **D4 (a):** R1 merges stage 1 (`0fd003a`); R2 merges stages 2–4.
- **Recorded in:** the plan's status line and §3, BL-53's and BL-57's backlog rows, and S175's receipt
  (`next_steps`). Nothing outward; no push.

### 2026-09-16 · [BL-57] S175 close-out — the resync is planned, not merged; D1–D4 wait on the operator

- **Deliverable:** the resync plan (`e3bc12c`), after the operator re-scoped the session from merging to
  planning. Preceded by the retention trim of `HANDOFFS.md` (`4679cca`) and its fold (`1f34e75`).
- **Close-out commit:** S175's receipt (self 7/10, S174 scored 8/10). BL-53's and BL-57's backlog rows
  point to the plan. One sentence is added to R1's step 3: keep Test 27.N1b's fix to one line, because
  BL-57's P5 removes Test 27 with the hook's claim carve-out. The instrument snapshot from the close-out's
  `context_budget.py --status` rides along.
- **No `FRAMEWORK_LEARNINGS.md` row:** the file's fate is decision D1, and it is 2,437 B under its growth
  warning. The session's learning (an arriving enforcement hook binds the test suite's own fixture
  commits) is in the plan's D1 trial and the receipt, to be written into whichever file D1 names.
- **Next:** the operator's D1–D4, then R1. S175's close-out leaves 2 receipts, so R1's Phase 0 does not
  trim. **Nothing outward;** fork `main` is 5 commits ahead of `origin/main` after this close-out (`git rev-list --count origin/main..main`), and
  pushing it is its own go-ahead.

### 2026-09-16 · [BL-57] S175 — the fork resync planned: four merge stages over two sessions, four decisions for the operator

- **Deliverable:** [`docs/planning/upstream-resync-2026-09-plan.md`](docs/planning/upstream-resync-2026-09-plan.md),
  a DRAFT for ratification. It merges `upstream/main` `6b29d3d` into fork `main` in four stages cut where
  upstream's commits introduce the conflicts (`0fd003a`, `cca7941`, `64f23bf`, `6b29d3d`: 4, 4, 5 and 0
  newly conflicting files). Each of the 13 conflicting files gets a resolution and a verification, and the
  execution runs in R1 (stage 1) and R2 (stages 2–4).
- **Decisions put to the operator:** D1, the fork's Learnings #15–#66 now that upstream has its own #15
  and #16 (BL-53; recommended: the distributed file becomes upstream's, the fork's 52 rows move verbatim
  to a fork-only file); D2, adopting upstream's quality ratchet and tightening it to the fork's measured
  values; D3, the dashboard's version across two numbering lines (2.18.0 recommended); D4, the session
  split.
- **Measured, not predicted:** a trial of D1's recommendation, merging stage 1 in a throwaway clone:
  297 passed / 3 failed / 6 skipped against 300 / 0 / 6, exactly three flips. Two are D1's cost (a
  dashboard test pinned to Learning #26; Test 37's helper numbering a row with the reserved #14). **One
  is not D1's:** the `commit-msg` hook stage 1 brings refuses Test 27.N1b's trailer-less fixture commit
  under an agent harness, whatever D1 decides. Also measured: upstream's 11 receipts pass the fork's
  `check-handoff` (`--all`, `--archived`), and the merge takes `CHANGELOG.md` to ~206,596 B, over the
  trimmer's 196,608 B trigger.
- **Reviewed:** a read-only claims review by an independent subagent checked ~150 claims and found 15
  wrong in the draft. The author re-ran each one and corrected them before this commit: the stage 2 and 3
  re-conflicts, where upstream's #15 and S20 arrive, two DONE criteria that could not pass as written,
  and several counts and citations.
- **Session:** S175 · **Model:** Claude Opus 5 (claude-opus-5) · Nothing outward.

### 2026-09-16 · [BL-57] S175 — the operator re-scopes the session: plan the resync first, merge in later sessions (picker)

- **Decision, taken by picker during S175:** *"Write the merge plan"*, chosen over merging in this
  session or merging stage 1 only. The claim entry below named the merge itself as the deliverable;
  the deliverable is now the plan, and the merge runs in the sessions it defines.
- **Why it was put to the operator:** `git merge-tree` on `main` against `upstream/main` gave about two
  dozen conflict hunks in 13 files, only 4 of them insertions on both sides. Several resolutions are the
  operator's to decide: the Learning #15/#16 numbering collision (BL-53), adopting upstream's quality
  ratchet, and the dashboard's two numbering lines. And the previous resync, `213f841`, carried out a
  plan ratified first (`docs/planning/upstream-read-set-budgets-merge-plan.md`).
- **Recorded in:** this entry and S175's receipt. Nothing outward.

### 2026-09-16 · [ad hoc] S175 — `HANDOFFS.md`: the trim's pointer block folded into the shard index

- **Change:** the 3-line pointer block `methodology_trim.py` wrote for
  `docs/archive/HANDOFFS-through-2026-09-16-2.md` (trim `4679cca`) becomes one row at the bottom of
  `docs/HANDOFFS_ARCHIVE_INDEX.md` (n = 2, the shard's own fence count; 124 B) and leaves `HANDOFFS.md`.
  The first fold into the index S174 created: the front matter goes 4,475 B inside the trim commit back
  to 4,019 B, S174's size, so the trim-and-fold did not grow it. Its own commit, after the trim
  (Learning #58).
- **Commit/PR:** this commit
- **Session:** S175 · **Verified:** the shard's `.verify.sh` exit 0 at the trim commit `4679cca`
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-16-2.md` (2 record(s), 40,816 B → 15,874 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-09-16 → 2026-09-16) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-16-2.md`](docs/archive/HANDOFFS-through-2026-09-16-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-16-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-16-2.md.verify.sh)
rather than trusting a digest printed here. Live file 40,816 B → 15,874 B (−61.1%).

### 2026-09-16 · [BL-57] S175 claim — trim `HANDOFFS.md`, then resync fork `main` with `upstream/main` (in progress)

**Deliverable:** the fork resync, merging `upstream/main` `6b29d3d` into fork `main`, preceded by the
retention trim `HANDOFFS.md`'s policy calls. Chosen by the operator after Phase 0 (picker, *"Trim, then
resync"*), in the order decided after S173: the header cut (done at S174), this resync, then BL-57's P5.
BL-53's retirement rule is decided inside the resync (operator, S173).

- **Measured at Phase 0:** 3 receipts, above 2. Fork `main` is 56 commits behind `upstream/main` (25
  first-parent) from merge base `598c459`; `git merge-tree --write-tree --name-only main upstream/main`
  lists 13 conflicting files, the same 13 as at S174. `upstream/main` has not moved since S174.
- **The trim runs after this claim with `--cut 2`, not the `--cut 1` S174's receipt names.** That
  `--cut 1` was written for a Phase 0 trim, before a claim exists; this claim's stub is a fourth record,
  so `--cut 2` archives the same two receipts (S173, S172) and keeps S174's beside this stub.
- **Observed, not acted on:** upstream PR #83 opened (the maintainer's parallel-sessions plan, planning
  only: `docs/planning/parallel-sessions-plan.md`, `CHANGELOG.md`, `HANDOFFS.md`). Its head `219fb9d`
  conflicts with fork `main` in the same 13 files, so it adds none to the resync. No open upstream issues.
- Phase 0 ledger reconcile: `CHANGELOG.md` frontier at `HEAD` `4735c6c`, no gap; `HANDOFFS.md` frontier
  `9b8a438`, and the one later commit only records the push S174's follow-up names. Nothing backfilled.
  Dashboard 76/100, medium risk. The two Phase 0 instrument snapshots ride with this claim.

### 2026-09-16 · [ad hoc] S174 follow-up — fork `main` pushed to `origin`, `f2c49f7..9b8a438` (non-commit action, operator go-ahead)

- **Action:** `git push origin main`, `f2c49f7..9b8a438` — 6 commits (S174's claim, `e8bd62d`, `ad3479a`,
  `67ac209`, the close-out `df235dc` and the decisions commit), a fast-forward, run behind a guard that
  confirmed the remote still read `f2c49f7` and was an ancestor of `main`. Read back with
  `git ls-remote`: `9b8a4382455be1769312269406c75d7f10c771f8`, equal to local `main`. The go-ahead was
  the operator's picker answer *"Push fork main now"*. This recording commit follows under the same
  go-ahead. Fork only; nothing sent upstream.

### 2026-09-16 · [BL-59] S174 follow-up — the operator closes BL-59 and schedules BL-61; fork `main` push approved (picker)

- **Decisions, taken by picker after the close-out:**
  - **BL-59 is CLOSED.** The retention it set (N=1, S172) is now measured reachable: Test 38 reads a
    frozen fixture (`d13a165`), and a `--cut 1 --force` trim plus its fold on `ad3479a` ran 300 passed /
    0 failed / 6 stated skips. The front-matter cut it left owed is done. What stays undone is teaching
    `methodology_trim.py` a retention mode, which ships to adopters and needs its own go-ahead. The row
    moves to §Completed items; the detail body stays, as BL-45's did.
  - **BL-61 is raised and scheduled:** lower `HEADER_RESERVE_BYTES` (`bin/check-handoff:663`) now that
    the front matter is 4,019 B and no longer grows per trim, banking the freed ~3 KB as S109 did. It
    runs as a later small session, not ahead of S175's trim, the fork resync or BL-57's P5.
    Canonical-only.
  - **Push fork `main` to `origin`:** approved. Recorded in the next entry once it is done.
- **Recorded in:** `docs/planning/BACKLOG.md` (the open list, the BL-61 row, BL-59's completed row),
  `docs/planning/BACKLOG-DETAIL.md` (BL-61's body), and the S174 receipt's `next_steps`.

### 2026-09-16 · [BL-59] S174 close-out — the header cut is done; S175's Phase 0 trims and folds into the new index

- **Change (this commit):** the S174 receipt in `HANDOFFS.md` goes from `pending` to `complete`
  (self 7, S173 scored 8). The context-budget reading taken at close-out rides with it.
- **Deliverable, on fork `main`, local and not pushed:** `e8bd62d` (Test 39's M2 literal 4096 → 2048),
  `ad3479a` (the shard table moves to `docs/HANDOFFS_ARCHIVE_INDEX.md`; front matter 7,028 → 3,929 B)
  and `67ac209` (corrections from a claims review, front matter 4,019 B). Each has its own entry below.
- **Verified, not predicted:** `bin/tests.sh` in `--no-local` clones, each asserted to be at its commit —
  306 passed / 0 failed at `be405b3`, `e8bd62d`, `ad3479a` and `67ac209`, with the same assertion set;
  305 / 1 for the cut without the M2 fix; 300 / 0 / 6 stated skips after a simulated S175 trim and fold.
  All 21 handoff-shard proofs gave the same exit codes before and after (18 pass, 3 pre-existing BL-36
  failures). `context_budget.py --status` shows no status flips against Phase 0.
- **For S175:** 3 receipts, so its Phase 0 trims with `--cut 1 --force` and then folds the pointer block
  into the index by the rule at `docs/HANDOFFS_ARCHIVE_INDEX.md:50`, in its own commit. Then comes the
  fork resync (`upstream/main` is now `6b29d3d`, 56 commits, 13 conflicting files), then BL-57's P5.
- **Raised for the operator, not acted on:** whether to lower `HEADER_RESERVE_BYTES` to bank the freed
  ~3 KB (the S109 precedent), and whether BL-59 closes now that N=1 is measured reachable.

### 2026-09-16 · [BL-59] S174 — corrections to `e8bd62d` and `ad3479a`, found by a claims review before close-out

- **Wrong number, and the urgency it carried:** both earlier entries and `ad3479a`'s message say a fold
  adds **~147 B** and that the trim S175's Phase 0 calls *"would have failed A2"*. Measured in bytes, the 21
  table rows are **125–129 B**, and the last fold added **123 B** (6,984 → 7,107 B, `1ec509d^` →
  `1266282`). With 140 B left the next fold would have landed at ~7,157 B and passed. Only the trim
  commit itself would have exceeded the reserve before its fold, as `5049845` (7,178 B), `0ccfce8`
  (7,311 B) and `1ec509d` (7,432 B) already did. **The cut was due one trim later than stated.** The
  ~147 B figure came from the spent-reserve callout `ad3479a` removed, which also said ~60 B remained.
- **Also overstated in `ad3479a`'s entry:** *"a file added there"* would not be read as a shard; only
  a `HANDOFFS-*.md` name in `docs/archive/` would, and `tools/test_methodology_dashboard.py:4426` would pick
  up any `*.md` there. The index's own warning already said it precisely.
- **Text corrected in this commit:** the index said its rows were *"unchanged"* (their links changed),
  that *"the next row would have overflowed"*, and that every shard is `HANDOFFS-through-<date>.md` (two
  carry `-2`). Its fold rule now says where the trimmer inserts the block, that the shard cell takes the
  bare name, and that the proof link is dropped. The front matter now says a trim *commit* still carries
  the ~448 B block until the fold. `bin/tests.sh`'s M2 comment no longer says the mutant survived at
  a commit where the move had not happened. BL-59's row no longer says N=1 is unreachable next to the
  commit that made it reachable, and records the measurement: a `--cut 1 --force` trim plus its fold on
  `ad3479a` ran **300 passed / 0 failed / 6 stated skips**.
- **Front matter after this commit: 4,019 B** of 7,168 B.
- **Left as written:** `docs/planning/BACKLOG-DETAIL.md` BL-60 (*"`HANDOFFS.md`'s own archive table says
  exactly that"*) and BL-59's detail (the fold *"replaces that block with one table row"*; *"What remains
  for N=1: give Test 38 a frozen fixture"*). Item bodies are deliberately not edited, and
  `BACKLOG-DETAIL.md.verify.sh` proves them byte-identical.

### 2026-09-16 · [BL-59] S174 — `HANDOFFS.md`'s shard index moves out of its front matter, so a trim no longer grows it

- **Change:** the archive table (21 rows), its intro and the fold rule move from `HANDOFFS.md`'s front
  matter to a new [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md). The rows are unchanged
  except for their links (`docs/archive/…` → `archive/…`). Front matter **7,028 B → 3,929 B** against
  the 7,168 B header reserve (`bin/check-handoff:663`, Test 39 A2): **3,239 B left**, where 140 B
  remained and each trim-and-fold row cost ~147 B. The trimmer's ~448 B pointer block now fits even
  inside the trim commit, before the fold.
- **Why not `docs/archive/`:** `bin/model-report:158`, `starter-kit/methodology_trim.py:921` and
  `starter-kit/methodology_dashboard.py:1135` find shards by the glob `docs/archive/HANDOFFS-*.md`. The
  trimmer would even have read this commit as an archive event (a file added there, `HANDOFFS.md`
  shrinking). `tools/test_methodology_dashboard.py:4426` treats every `docs/archive/*.md` as a ledger.
  Nothing globs `docs/*.md`.
- **Corrected in the move, each checked:** the table intro's *"20 trims, 154 receipts"* was stale
  (21 and 160; every row's `n` equals its shard's fence count). Its *"every shard is
  `HANDOFFS-through-<date>.md`"* skipped `HANDOFFS-archive.md` (19 receipts, 2026-07-08 → 2026-07-30,
  no proof), which the index now names. The index gives commands to derive the totals instead of
  writing them (22 files, 179 receipts). In the front matter, *"indexed in the table below"* and
  *"all four retained here"* (stale since N=1) are rewritten, and the spent-reserve callout goes. It
  also said ~60 B remained, where 140 B did.
- **Not changed:** the trimmer (distributed), `HEADER_RESERVE_BYTES`, and the shipped `.verify.sh`
  proofs, each of which compares its own trim commit with that commit's parent
  (`docs/archive/HANDOFFS-through-2026-09-16.md.verify.sh:163`).
- **Depends on `e8bd62d`,** which moved Test 39's M2 mutant under the smaller front matter first.

### 2026-09-16 · [BL-59] S174 — Test 39's M2 mutant moves below the front matter the header cut leaves

- **Change:** `bin/tests.sh` Test 39's M2 plants `HEADER_RESERVE_BYTES = 2048` instead of `4096`. M2 counts
  as killed only when the planted reserve is under the **live** `HANDOFFS.md` front matter, which it
  measures, so the live file was the mutant's unstated fixture. The header cut, run first in a
  throwaway clone, took the front matter from 7,028 B to 3,929 B, under 4,096 B, and the suite went from
  306 passed / 0 failed to 305 / 1 on exactly this row:
  `MUTANT SURVIVED: reserve 4096 B vs front matter 3929 B (fits ceiling: 1)`.
- **Landed before the cut, so every commit stays green:** 2,048 B is under both 7,028 B and 3,929 B,
  and A1 still fits (3 × 12,288 + 2,048 = 38,912 B ≤ 65,536 B). The block's comment now states the
  constraint and what happens if the front matter is ever cut below it.

### 2026-09-16 · [BL-59] S174 claim — the `HANDOFFS.md` header cut (in progress)

**Deliverable:** shorten `HANDOFFS.md`'s front matter so the retention trim S175's Phase 0 will call
does not break Test 39 A2 (`bin/tests.sh:3047`). Chosen by the operator at Phase 0 (picker), in the
order decided after S173: this cut, then the fork resync, then BL-57's P5.

- **Measured at Phase 0:** front matter 7,028 B against `HEADER_RESERVE_BYTES` 7,168 B
  (`bin/check-handoff:663`) — 140 B left; one trim-and-fold row is ~147 B. The file's own callout says
  ~60 B, which is wrong.
- **Observed, not acted on:** `upstream/main` moved `64f23bf` → `6b29d3d` — three maintainer commits,
  the first ratchet tightening after #82 (`.quality-gates.json`: tests-sh-failed max 0, tests-sh-passed
  min 139) and his receipts. Fork `main` is 56 behind, not 53. No open upstream PRs or issues.
- Phase 0 ledger reconcile: `CHANGELOG.md` frontier at `HEAD` `f2c49f7`, no gap; `HANDOFFS.md` frontier
  `d5ea5c4`, and the one later commit only records a push S173's receipt already names. Nothing
  backfilled. Dashboard 76/100, medium risk. The two Phase 0 instrument snapshots ride with this claim.

### 2026-09-16 · [ad hoc] S173 follow-up — fork `main` pushed to `origin`, `3f9210c..d5ea5c4` (non-commit action, operator go-ahead)

- **Action:** `git push origin main`, `3f9210c..d5ea5c4` — 1 commit, a fast-forward, run behind a guard
  that confirmed the remote still read `3f9210c`. Read back with `git ls-remote`:
  `d5ea5c412e57a26ab3ba7a5ad4afd8045d6ee870`, equal to local `main`. Go-ahead: the operator's picker answer
  *"Push now"*. This recording commit follows under the same go-ahead.

### 2026-09-16 · [ad hoc] S173 follow-up — grooming decisions on F5/F6, BL-53, BL-54, BL-36 and BL-60 (operator, picker)

- **Decisions,** each re-checked against current state before the operator was asked:
  - **F5 rides BL-57's upstream PR (P12); F6 is closed.** On `upstream/main` `64f23bf`,
    `starter-kit/methodology_trim.py:33` still says the ledger hook runs `--no-renames` (upstream's hook
    has 0), and `:9`/`:155` still cite a design doc upstream lacks. BL-57 already edits that file. F6 was
    wording in #80's description, and #80 merged on 2026-09-15.
  - **BL-53: the retirement rule is decided inside the fork resync.** Fork `main`'s file is 79,483 of
    81,920 B (about 2 rows); upstream's is 16,560 B (13 rows); the file is one of the resync's 12 conflicts.
  - **BL-54: fixed after BL-57's P5, before P6** — when the adopters first sync from the resynced fork
    `main`, the merge shape the bug breaks. `bin/sync:60` and `bin/status:56` are unchanged upstream.
  - **BL-60: one planning session costs its three shapes and folds BL-36 in**, so the four frozen
    proofs that report FAIL over intact archives are decided inside the new scheme, not rewritten twice.
    31 proofs, 453,689 B, re-counted.
- **Recorded in:** `docs/planning/BACKLOG.md` (the four index rows);
  `docs/planning/pr80-review-response.md` §6; the BL-57 plan's finding (11); the S173 receipt's
  `next_steps`.

### 2026-09-16 · [ad hoc] S173 follow-up — fork `main` pushed to `origin`, `ef83601..22a78b3` (non-commit action, operator go-ahead)

- **Action:** `git push origin main`, `ef83601..22a78b3` — 8 commits, a fast-forward, run behind a guard
  that confirmed the remote head was an ancestor of `main`. Read back with `git ls-remote`:
  `22a78b3c0d6c64d6310ba9466a89aca2c53caa6f`, equal to local `main`. The go-ahead was the operator's
  picker answer *"Push fork main"*. The commit carrying this entry follows it to `origin` under the
  same go-ahead, as S168's recording commit did.

### 2026-09-16 · [BL-57] S173 follow-up — the operator's two decisions, and the branch pushed to `origin` (non-commit actions)

- **Decisions, taken by picker after the close-out:** (1) P5 starts from a **resync of fork `main` with
  `upstream/main`**, then ports BL-57's own change from `64f23bf`, not the plan's `b82dcff` form.
  (2) **S174 does the `HANDOFFS.md` header cut** first, because the trim S175's Phase 0 calls needs
  it. Recorded in the plan (finding (9), `docs/planning/changelog-rules-contradictions-plan.md:129`),
  BL-57's backlog row, and the S173 receipt's `next_steps`, which is rewritten around them.
- **Action:** `git push origin bl57/changelog-rules`, `775ba23..83a12f0` — a fast-forward, run behind a
  guard that confirmed the remote still read `775ba238` and was an ancestor. Read back with
  `git ls-remote`: `83a12f0380b7d23c9a2e339a38fffc49314c7ad2`. P3, P4 and both upstream merges are now
  backed up; fork only, nothing sent upstream.
- **Also:** the operator asked that requests for input come as a picker, to reduce typing. That is a
  change in how I ask, recorded in agent memory; no repository file changed for it.

### 2026-09-16 · [BL-57] S173 close-out — BL-57's P4 done on the branch, not pushed; P5 opens with an operator decision about its base

- **Change (branch `bl57/changelog-rules`, `83a12f0`, not pushed):** P4's four commits after the merge
  `52ad407`. `0c20022` gives §The Action Ledger its *Lifecycle* and *Placement* rules; `f235db3` turns
  *append* into *prepend* at seven sites and records the claim commit's *(in progress)* entry; `836e0d2`
  replaces *completed work history* with the action ledger and brings `CLAUDE.md` back under its ceiling;
  `83a12f0` rewrites upstream's root `CHANGELOG.md` front matter (D8 i). Each commit has its own branch
  ledger entry.
- **Change (fork `main`, this commit):** the plan records P4 done, with findings (6)–(10) for P5–P12
  (`docs/planning/changelog-rules-contradictions-plan.md:114`) and a status-line warning about P5's port.
  BL-57's backlog row reads *P4 at S173, next P5*. The S173 receipt is completed in `HANDOFFS.md`.
- **Found, for the next session:** P5's port command as the plan writes it is **34 files, +3,015/−358**,
  because the branch now carries #80's fixes and #82's ratchet; BL-57's own net change on `64f23bf` is
  **16 files, +532/−252**. Fork `main` is 53 commits behind `upstream/main`, and merging the two conflicts
  in 12 files. So P5 starts with the operator's choice: port from `64f23bf`, or resync fork `main` first.
- **No learning row:** `starter-kit/FRAMEWORK_LEARNINGS.md` is within about two rows of its ceiling, and
  neither finding is new at the framework level. That a recorded density can hide token growth is already
  stated in upstream's `.context-budget.json`, in the runner's entry: *"A DENSITY IS TIED TO THE BLOB IT
  WAS MEASURED ON"*. The instrument change is a harness behaviour,
  recorded in the plan and in the receipt's gotchas.
- **Session:** S173 · **Verified:** see the receipt's `runtime_smoke` — the branch head `83a12f0`, in a
  `--no-local` clone with HEAD asserted: `bin/tests.sh` 141 / 0; ratchet 10/10 (`c5fca86e4674`);
  `bin/check-links` 110; `context_budget.py --status` exit 0, no status flips against `upstream/main`, read-set
  total 70,253 B against 70,276 B.
- **One status flip on fork `main`, caused by this session and left as it is:** `context_budget.py --status`
  (exit 2 at Phase 0 and now, the runner's standing breach) moves `HANDOFFS.md` from ok to **warn** — not
  a ceiling: its density was measured at 20,310 B and the file is 32,800 B after this session's claim stub
  and receipt, a 61% drift that marks its ≈14,500-token figure provisional. Re-measuring is a budget
  commit of its own, as `24d9645` was. An estimate, not a measurement: the next retention trim should take
  the file back near the measured size.
  Runner doubled 37,717 (≤ 37,731) and `CLAUDE.md` 46,953 (≤ 46,965), each beside a reproduced control.

### 2026-09-16 · [BL-57] S173 — #82 merged into BL-57's branch; P4's size criterion restated on the new base before any P4 edit

- **Change:** `docs/planning/changelog-rules-contradictions-plan.md` gains the S173 amendment (above §0)
  and P4's DONE criterion is restated against `upstream/main` `64f23bf` instead of `b82dcff`: the runner
  no larger than **18,865.5 tokens (doubled ≤ 37,731)**, `CLAUDE.md` no larger than **23,482.5 tokens
  (doubled ≤ 46,965)** — newly a criterion, since #82 gave it a token ceiling — `SAFEGUARDS.md` at blob
  `933816b4`, no `context_budget.py` status flip, and `quality_ratchet.py --run` passing.
- **The branch action it rests on:** `52ad407` on `bl57/changelog-rules` merges `upstream/main`; two
  one-line conflicts, both predicted at Phase 0 (`CLAUDE.md`, `ITERATIVE_METHODOLOGY.md`). A merge skips
  the ledger hook, so the branch carries no entry of its own for it — as `9e1dfeb` did at S168.
- **Found:** the merge is **4 tokens over `CLAUDE.md`'s ceiling** (46,973 doubled) — P1's row wording is
  9 B shorter and 4 tokens longer, and `context_budget.py` prices it at 2.519 B/token and reports it ok.
  P4's `CLAUDE.md` edit pays it back. P3's 14-token runner saving survived the merge exactly (37,703).
- **Found:** the Read tool no longer refuses a file over 25,000 tokens — it returns a 25,000-token page and
  prints the count in the truncation notice — so each doubled-file reading costs a page of context.
  Readings were taken in a subagent that reproduced the 36,955 control in the same run.
- **Session:** S173 · **Verified:** upstream 139/0, ratchet 10/10, links 107, budget exit 0; merge 141/0,
  10/10 (`c5fca86e4674`), 110, exit 0 with no status flips — both in `--no-local` clones, HEAD asserted.

### 2026-09-16 · [BL-57] S173 claim — BL-57's P4: merge #82 into the branch first, then entry lifecycle and the words

**Deliverable:** BL-57's **P4** (`docs/planning/changelog-rules-contradictions-plan.md:551`) on branch
`bl57/changelog-rules` (worktree `../methodology-bl57`, at `18962a9`): the lifecycle and placement rules
in §The Action Ledger, "append" becomes "prepend" where the file is newest-on-top, the claim commit's
*(in progress)* entry, "completed work history" becomes the action ledger, and upstream's root
`CHANGELOG.md` front matter.

- **Observed, not taken by this fork: upstream PR #82 MERGED** at 2026-09-16T18:05:47Z — merge commit
  `64f23bf`, head `5c9d3b40`, merged by `rmsharp` — six minutes after S172's last commit. Before it
  merged, the maintainer answered this fork's comment (`5701463025`) and pushed his fixes F1b–F6.
  Verified at Phase 0 with `gh pr view 82`. No open upstream PRs or issues remain.
- **So S169's merge-first amendment triggers.** P4 starts by merging `upstream/main` `64f23bf` into the
  branch. `git merge-tree` at Phase 0: conflicts in `CLAUDE.md` and `ITERATIVE_METHODOLOGY.md` only.
- **P4's token criterion predates #82** (`:575`, doubled read ≤ 36,955 on blob `c0550acd`): the merged
  runner is 53,220 B against the branch's 52,163 B. It is re-measured on the merge result and restated
  before any P4 edit.
- Phase 0 ledger reconcile: both frontiers at `HEAD` `c509190`, no gap, nothing backfilled. The two Phase 0
  instrument snapshots ride with this claim.

