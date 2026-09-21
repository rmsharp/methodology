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

