# Changelog — Authoritative Action Ledger

The cumulative, append-only record of **actions taken in this repository** — across backlog
items, repository issues, and ad-hoc work. It is the authoritative answer to *"what was done
here, ever?"*, distinct from the release narrative in [`CLAUDE.md` §Versioning](CLAUDE.md#versioning).

This repository dogfoods its own methodology: every session records its actions here at
close-out (`starter-kit/SESSION_RUNNER.md` Phase 3F), and Phase 0 reconciles the ledger against
`git log` and backfills anything a crashed or out-of-band session missed. Taking an action — any
commit, or any non-commit action (release, tag, PR, upstream issue close, access grant, grooming
decision) — and not recording it is failure mode #27. The full close-out and reconcile rules, plus
the reusable seed, live in [`starter-kit/CHANGELOG.md`](starter-kit/CHANGELOG.md).

**Source tag — exactly one per entry.** This enumerates every logged action across the live file
and its archives, and proves all three sources landed:

```
grep -hE '^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[(issue #[0-9]+|BL-[0-9]+|ad hoc)\]' \
  CHANGELOG.md docs/archive/CHANGELOG-*.md | wc -l
```

It is anchored to the entry heading, and it reads the archives, for two separate reasons. The
unanchored single-file form published here before the v3.6 split returned **78** against 64 actions —
it also matched the three tag definitions just below and eleven in-prose mentions of a tag — and after
the split it would have stopped counting the archived entries at all.

- `[issue #<N>]` — a repository issue. Issues live in `KJ5HST/methodology`; the fork
  `rmsharp/methodology` has Issues disabled, so entries — authored from either side — cite an
  **absolute URL**, never a bare `#<N>`, and resolve identically from both.
- `[BL-<N>]` — a backlog item, removed from the backlog in the same commit. That backlog is
  [`docs/planning/BACKLOG.md`](https://github.com/rmsharp/methodology/blob/main/docs/planning/BACKLOG.md)
  on fork `main` only — **this repo has no `docs/planning/BACKLOG.md`** — so a `[BL-<N>]` entry here
  records work whose origin lives in the fork.
- `[ad hoc]` — work with no backlog or issue origin: releases, tag/branch ops, PR opens, upstream
  issue closes, access grants, and decline/wontfix/grooming decisions.

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

**When to archive again — a rate, not a level.** Archive when the headroom to the 2,000-line
`READ_CAP_LINES` proxy — the agent `Read` cap is denominated in **tokens**, and 2,000 lines is a
stand-in for it pending Phase B of
[`read-cap-premise-correction-plan.md`](docs/planning/read-cap-premise-correction-plan.md) —
divided by the observed growth per ledger *entry*, falls below **15 entries**; then cut
oldest-first until that ratio is back above **30**. Both are denominated in entries — the framework's
own unit — deliberately: commits-per-session is the most adopter-variable quantity in the system, so a
team committing 10× per session reads a 10× lower slope for identical growth, and the same file
crosses or clears the threshold depending only on which denominator you picked. Compute it; never
recall it:

```sh
split=$(git log --diff-filter=A -1 --format=%H -- 'docs/archive/CHANGELOG-*.md')
live=$(wc -l < CHANGELOG.md)
dl=$(( live - $(git show $split:CHANGELOG.md | wc -l) ))
de=$(( $(grep -c '^### ' CHANGELOG.md) - $(git show $split:CHANGELOG.md | grep -c '^### ') ))
if [ "$de" -gt 0 ] && [ "$dl" -gt 0 ]; then
  echo "$(( (2000 - live) * de / dl )) entries of headroom"
else
  echo "no slope yet — fewer than one entry written since the last split ($de entries, $dl lines)"
fi
```

It **abstains out loud** rather than printing a confident number it cannot support: immediately after
a split both deltas are zero, and against a superseded baseline they go negative. Either way you get
a sentence saying so, never a figure. That is the same discipline the numbers above are asking for.

A **level** was the previous rule, and it failed in the file next door: `HANDOFFS.md` states its
trigger as "approaches ~1,200 lines" and the archive actually fired at 997 — 203 lines early, with
nothing watching. A level is a hand-written derived value that decays silently; a rate re-derives
itself from the file every time it is read. This file crossed the cap once already, at 2,090 lines,
and its ten oldest entries were not reaching a reader who read it whole. **That was recorded here
as *silent* dropping, and that word was wrong** — truncation is announced, with a `PARTIAL view`
banner naming the true length; what was silent was that **nothing in the repo was checking**, so
the overrun was found by accident. Re-measured since, the file was 186,704 B — roughly 2.8–3.1×
the token cap — so it had been truncating well before it reached 2,090 lines: the incident dates
when the problem was *noticed*, not when it began.

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

---

## 2026-09

### 2026-09-10 · [ad hoc] S158 close-out — `HANDOFFS.md` back to four receipts (61,122 → 38,425 B), and `FRAMEWORK_LEARNINGS.md` found 192 B over its ceiling

**The deliverable is done and proved.** `HANDOFFS.md` holds four receipts again — S158, S157, S156,
S155 — at **38,425 B before this close-out's receipt**, from 61,122 B after the claim. S154 and S153
are frozen in [`docs/archive/HANDOFFS-through-2026-09-08.md`](docs/archive/HANDOFFS-through-2026-09-08.md),
whose `.verify.sh` exits **0** against the trim commit `000a843e` and again after the fold `e2600a06`.
No `--force`, no gate (SRF 0.7414). Front matter **7,148 of the 7,168 B reserve**. `bash bin/tests.sh`,
bare, before the trim and after the fold: **304 / 1 / 0, exit 1** both times, 305 rows, **0 status
flips**, each of the 10 changed rows a number this session moved. **Fork-internal throughout:
`origin/main` unmoved at `f8531cf`, PR #80 untouched.**

**The finding is in the file next to it.** `starter-kit/FRAMEWORK_LEARNINGS.md` is **73,920 B against
the 73,728 B** its `.context-budget.json` entry declares (`:101`) — **192 B over since S157's close-out
`07c750b`**, which took it from 72,692 B with its Learning #61. `context_budget.py` prints the row.
**No session saw it, for two reasons that compound.** The checker close-outs actually run on that file,
`bin/check-learnings`, budgets **rows** (1,500 B each) and never the file; and `context_budget.py`, which
does measure the file against its ceiling, already exits **2** for pre-existing overages (the read-set
total, `CHANGELOG.md`, `SESSION_RUNNER.md`), so a new `over` row changes nothing a session reads.
**Not fixed here:** it is a second deliverable, in a DISTRIBUTED file, and its ceiling is the operator's
decision — at S114 (BL-45) the operator chose *raise* from four costed options.

**Two learnings are owed to `FRAMEWORK_LEARNINGS.md` and deliberately not written**, because a ~1.2 KB
row would deepen the breach FM #28 calls a defect. Write them once the ceiling is decided:

- **An already-failing checker cannot report a new failure.** When a gate is red for a known reason, a
  second breach changes no exit code and no summary line; only a row-level diff against the last run
  shows it. This repo already diffs `bin/tests.sh` row for row because its Test 9 is a standing,
  known failure — and does not do the same for `context_budget.py`.
- **State a ceiling's headroom in units of the next write.** S157 recorded *"52,493 B at claim, so
  bytes are not pressing"*; its own close-out left 6,349 B under `CEILING_BYTES`, less than the smallest
  of the file's five records (8,521 B). Judged against the total, the file looked fine; judged against
  the record the next session had to write, it was full.

**Commits:** `e5812e2a` (claim, with the Phase 0 `dashboard_history.jsonl` snapshot), `000a843e` (the
trim), `e2600a06` (the fold), and this close-out, which also carries `.context-budget-history.jsonl`,
appended by this session's `context_budget.py` run.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-10 · [ad hoc] S158 — the pointer-block fold, paid for with four spent clauses

The trim commit `000a843e` left `methodology_trim.py`'s generated pointer block in the front matter,
because folding it in the same commit makes the shipped `.verify.sh` fail L2 (Learning #58). This
commit folds it into the archive table as one row, per the `NEXT TRIMMING SESSION` comment in
`HANDOFFS.md`'s front matter: **448 B of block out, a 190 B row in**, and the table's counts
**13 trims / 141 receipts → 14 / 143**, with the `n` column re-summed to match (asserted, not eyeballed).

**The row still did not fit on its own.** Before the trim the front matter was 7,159 B, 9 B under the
7,168 B reserve the operator kept at S155, so the row needed **181 B** found elsewhere. They came from
four clauses whose facts are recorded elsewhere and whose presence here was history, not instruction:
*"where S152's trim moved it"* (28 B); *"— it is not newest-only. Since S133"* (37 B, left over from
correcting a sentence the file no longer contains); the *"read 6 for three sessions once"* anecdote
(39 B); and S94's *"235/1 → 229/6"* evidence for the three-receipt floor (97 B). BL-40 (b) is still
cited there, and the floor, the SKIP rows and the re-run instruction all stay. Front matter **7,607 →
7,148 B, 20 B spare**; live file **38,884 → 38,425 B**.

**This cost recurs, and it is recorded rather than fixed.** Every trim adds a ~190 B row against a
reserve that is already full, so every fold has to find that much spent text again. That is an
inference from this fold and S156's, not a measurement of how much spent text is left. The table's
shape is the operator's decision, not this session's.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-10 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-08.md` (2 record(s), 61,122 B → 38,884 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-09-08 → 2026-09-08) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-08.md`](docs/archive/HANDOFFS-through-2026-09-08.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-08.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-08.md.verify.sh)
rather than trusting a digest printed here. Live file 61,122 B → 38,884 B (−36.4%).

### 2026-09-10 · [ad hoc] S158 — claim: apply the retention policy to `HANDOFFS.md` again, 5 receipts against a policy of 4 and no room for a sixth

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: trim
`HANDOFFS.md` back to four receipts under the retention policy at `HANDOFFS.md:8` — adopted at **S127
by operator decision** — chosen by the operator (*"A"*) from this session's Phase 0 report, where it
stood as S157's handoff item (5). **Fork-internal: no push, no PR, no tag, no comment; PR #80
untouched.**

**The forcing condition is the record count plus the byte ceiling, measured in the checker's own
unit.** At claim time the file is **59,187 B, 6,349 B under `CEILING_BYTES` (65,536)**, and its five
records measure **8,521–12,286 B each**, trailing prose included — the unit `bin/check-handoff:657`
budgets. None of them would fit in the space left. **The Phase 0 report understated this:** it quoted
S157's close-out growth (6,694 B) as its receipt's cost; the whole record is 8,521 B. Same conclusion,
wider margin.

**The trigger does not fire and there is no gate.** `--check` exits **0** (59,187 B against the
196,608 B Class A threshold). The pre-claim dry run `--cut 4` exits **0**: **SRF 0.6609** against the
most recent archive `c581ac4` — no `SRF_RED`, no `--force` — L1/L2/L3 OK, **1 of 5** records (S153) to
`docs/archive/HANDOFFS-through-2026-09-08.md`, live 59,187 → 49,235 B, with `CUT_STRADDLES_DAY`
because S154 shares 2026-09-08 and would have stayed.

**This claim invalidates that dry run, and it will be re-derived.** The stub is a sixth record, so
`--cut 4` should now take **two** — S154 and S153, both 2026-09-08 — which would also clear the
straddle. That is an expectation until the post-claim run measures it.

The Phase 0 dashboard run's `dashboard_history.jsonl` snapshot rides in this commit, as it did in
S154's claim (`1695734f`).

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-09 · [ad hoc] PR OPENED: [KJ5HST/methodology#80](https://github.com/KJ5HST/methodology/pull/80) — `read-set-budgets` → `main`

**A non-commit action, recorded because FM #27 names "a PR open" explicitly.** Opened
2026-09-09 against `KJ5HST/methodology`, base `main` (`512c2ed`), head `read-set-budgets`
(`598c459`), by `rmsharp` under the upstream push+triage grant. **State OPEN, `MERGEABLE`, 28 files,
+7,783 / −553.** Title and body are §1 and §2 of
[`docs/planning/read-set-budgets-to-main-pr-body.md`](docs/planning/read-set-budgets-to-main-pr-body.md),
written at S155.

**Authorised by the operator's explicit *"open the PR"*, and by nothing wider.** Not merged, not
tagged, no release, fork `main` not pushed, the five merged `origin` branches not deleted — each of
those remains its own ask. This is the **first outward-facing action of the read-set arc**; S153,
S154, S155 and S156 each recorded the gate as absent and each declined to act without it.

**Verified after the fact rather than assumed:** `gh pr view 80 --json` reports the state, mergeability
and diffstat above, and the live body **round-trips byte-identical to the file sent — 8,722 chars both
sides**. The published body carries the Claude Code attribution tail that the committed document does
not, by design; that 129 B difference is expected and is recorded as gotcha (1) in this session's
receipt.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-09 · [ad hoc] S157 close-out — PR #80 opened, and the stale number caught in pre-flight

**`c64ee4b` corrected the body before it was published.** §2 said `rmsharp/methodology` was **"580
commits ahead"** of the branch it proposes merging; at publish time it was **590**, moved by S155's and
S156's own commits — including the session that wrote the sentence. It now reads as a **dated**
measurement, which a frozen PR body can carry without going false. The companion claim — 5 of 27
distributed sources drifted further on fork `main` — was re-derived and is **unchanged, the same five
names**.

**That is the session's finding, and it is now Learning #61** (1,227 B): *a document that waits for an
approval keeps measuring the tree it was written against — re-derive its self-referential numbers at
publish time, not at authoring time.* It is deliberately **not** Learning #13's territory: nothing here
was a prediction, and re-reading the file would not have caught it, because the file was still exactly
what its author wrote. The measurement was true when made and false when published, and the gap is
however long the approval takes. Numbers about the *other* side of a comparison need only a re-fetch;
numbers about *your own* tree are the ones that move while you wait.

**Pre-flight was re-derived rather than trusted**, which is why the drift surfaced at all: both shas
unmoved, ancestry still clean, diffstat identical at 28 files, and `gh pr list --state all --head
read-set-budgets --base main` returning **0** — so #80 opened rather than reopened. The extracted body
was read in full before sending, with zero stray blockquote prefixes surviving the de-quoting.

**Verification.** `bash bin/tests.sh` bare: **304 passed / 1 failed / 0 skipped, exit 1**, diffed row
for row against S156's — **305 rows both sides, PASS→PASS throughout, zero status flips, zero added,
zero removed**; every differing row states a count this session moved. The one failure is Test 9
`github source dry-run failed` — **pre-existing, and exactly what #80 exists to cure.** All checkers 0.

**Three commits plus one non-commit action:** `18aa587` (claim), `c64ee4b` (the dated ahead-count), this
close-out, and the PR open recorded in its own entry above. **`origin/main` remains unmoved at
`f8531cf`**; the ahead-count is deliberately not quoted here, for the reason this entry is about.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-09 · [ad hoc] S157 — claim: open the PR for `read-set-budgets` → `upstream/main`, on the operator's explicit go-ahead

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: open the
pull request from `KJ5HST/methodology:read-set-budgets` (`598c459`) into `upstream/main` (`512c2ed`),
using the Title and Body written at S155 in
[`docs/planning/read-set-budgets-to-main-pr-body.md`](docs/planning/read-set-budgets-to-main-pr-body.md).

**THIS IS THE FIRST OUTWARD-FACING ACTION OF THIS ARC, AND IT HAS THE GATE `CLAUDE.md` REQUIRES.** The
operator's words were *"open the PR"* — given after S156's close-out put it as the ranked item. S153,
S154, S155 and S156 each recorded the absence of this go-ahead and each declined to act without it; the
grant, not the PR, is the thing only the operator could supply. **The go-ahead covers opening the PR and
nothing else: no merge, no tag, no release, no push of fork `main`, no deletion of the five merged
`origin` branches.** Each of those remains its own ask.

**Pre-flight, re-derived before this claim rather than trusted from S155.** `upstream/main` **`512c2ed`**
and `read-set-budgets` **`598c459`** are both unmoved; `upstream/main` is still an ancestor of the head,
so the merge stays clean; the diff is still **28 files, +7,783 / −553**; and `gh pr list --state all
--head read-set-budgets --base main` returns **0** — no PR has ever existed for this pair, so this opens
rather than reopens.

**One body number had drifted and is corrected before publishing.** §2's *"`rmsharp/methodology` is 580
commits ahead of this branch"* is now **590**, moved by this fork's own S155 and S156 commits — the same
self-referential drift S155 had to repair in its own receipt, here caught in pre-flight instead. It will
be published as a **dated** measurement, which a frozen PR body can carry without going false. The
companion claim — **5 of 27 distributed sources drifted further on fork `main`** — was re-derived and is
unchanged, the same five names.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-09 · [ad hoc] S156 close-out — `HANDOFFS.md` back inside every budget: 67,336 → 42,923 B, 6 receipts → 4, and it fits in one read again

**The remedy the operator selected from S155's close-out is done and measured.** `HANDOFFS.md` is
**42,923 B** with **22,613 B of ceiling headroom** and **19,040 tokens — 76.2% of the 25,000-token
cap**, down from 28,287 at claim time. The token figure is off the doubled-file meter (38,081 halved),
not off the config's declared density, which is exactly what Learning #60 below is about. Front matter
**7,159 B of the 7,168 B reserve** the operator kept at S155. S152 and S151 are frozen in
[`docs/archive/HANDOFFS-through-2026-09-07.md`](docs/archive/HANDOFFS-through-2026-09-07.md).
**Fork-internal throughout: `origin/main` unmoved at `f8531cf`, `upstream/main` `512c2ed`,
`read-set-budgets` `598c459`, 0 open PRs.**

**THE WARRANT WAS CORRECTED MID-SESSION, AND THE CORRECTION IS THE INTERESTING PART.** The claim entry
above leads with the byte ceiling because `methodology_trim.py`'s own `[TRIGGER_READ]` line rules the
token overage *"FOR REFERENCE AND NOT AS A FAULT: … delivery is an ordered prefix and this ledger is
newest-on-top, so what truncates is the OLDEST records."* That is BL-52's point made by the tool about
this file: a newest-on-top ledger degrades gracefully under truncation, so 28,287-vs-25,000 was the
loud number and not the load-bearing one. **The forcing condition was 2 B of byte headroom** — the next
session physically could not write a receipt.

**No gate, and that is worth recording next to S154's.** `--cut 4` dry-ran at **exit 0** with **SRF
0.1096** against the most recent archive `aa1c476`, where S154 hit **SRF_RED at 3.7022** and needed an
operator-approved `--force`. **None was needed or asked for here.** The trigger does not fire at all
(196,608 B threshold), so this was the retention policy at `HANDOFFS.md:8` — *"applied by the session
that notices"* — executed **with the tool via an explicit `--cut`**, which is what produces the shard,
the losslessness proof and this ledger's own trim entry. A literal hand edit would have produced none
of the three.

**The post-claim re-derive changed the answer.** Pre-claim, `--cut 4` would have archived **1** record;
after the claim stub made it six, **2**. That is S153's gate, and this is the second consecutive session
where obeying it changed what got written.

**Learning #58 was verified rather than cited.** The fold of the tool's pointer block into the archive
table went in as its **own commit** (`b19be54`), and `docs/archive/HANDOFFS-through-2026-09-07.md.verify.sh`
was run **twice** — immediately after the trim commit `c581ac4` (exit 0) and again after the fold (exit
0). The trim's own write had grown the front matter to **7,286 B, 118 B over the reserve**; the fold
traded a ~447 B pointer block for a ~182 B row and the remaining bytes came out of **spent claims** —
a correction of a sentence this file no longer contains, and a drift example's commit sha — not out of
live content. 7,286 → **7,159 B**.

**Verification.** `bash bin/tests.sh` bare: **304 passed / 1 failed / 0 skipped, exit 1**, diffed row
for row against S155's final run — **305 rows both sides, PASS→PASS throughout, zero status flips, zero
added, zero removed**. Every differing row states a number this session moved (receipts 5→4, front
matter 7,096→7,159 B, `**Model:**` bullets 10→11). **`0 skipped` is load-bearing:** Test 34 needs three
receipts and four were retained, so BL-40 (b)'s SKIP rows never appeared. The single failure is Test 9
`github source dry-run failed`, pre-existing.

**New Learning #60** (1,260 B): *a file's `bytes_per_token` is a snapshot of the content it held when
measured, not a property of the file — and a "conservative" floor can be breached by real content.*
`HANDOFFS.md` metered **2.3164 B/token at 65,531 B** and **2.2543 at 42,923 B** the same day. The second
sits **below `MIN_BYTES_PER_TOKEN = 2.27`** (`starter-kit/context_budget.py:68`), whose comment claims a
floor-derived ceiling *"can never certify an unreadable file as fine"* — at that floor this file
estimates 18,908 tokens against a true 19,040, optimistic by 0.7%. **The config was not edited:** with
two conflicting measurements in hand the right value is a judgment, and it is handed forward as such.

**Five commits:** `6ec5aec` (claim), `c581ac4` (the trim), `b19be54` (the fold), `b3d19b0` (this
close-out), and a `chore(history)` for `.context-budget-history.jsonl`, which a bare
`context_budget.py` run appends to — three ran this session. The ahead-count is deliberately not
quoted; it drifts with each repair commit that quotes it (S155's lesson, one session old).

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-09 · [ad hoc] S156 — the pointer-block fold, and the front-matter bytes that paid for it

`b19be54`. `methodology_trim.py` appends a ~447 B pointer block to the front matter on every trim;
`HANDOFFS.md:69-73` instructs the next session to fold it into the archive table as one ~182 B row and
delete the block. Done here as a **separate commit**, because folded into the trim commit the shipped
`.verify.sh` fails `L2 FRONT MATTER lost 1 line(s)` — S154 established that by building both shapes,
and this session re-ran the proof after the fold to confirm the separate-commit shape stays green.

The archive table's counts were corrected with the new row — **12 trims / 139 receipts → 13 / 141** —
and the regenerated *"currently holds 4"* field is true again. The `NEXT TRIMMING SESSION` comment now
carries the own-commit rule S154 recorded as not fitting the reserve; it fits now because the same edit
removed more than it added.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-09 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-07.md` (2 record(s), 67,336 B → 43,308 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-09-04 → 2026-09-07) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-07.md`](docs/archive/HANDOFFS-through-2026-09-07.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-07.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-07.md.verify.sh)
rather than trusting a digest printed here. Live file 67,336 B → 43,308 B (−35.7%).

### 2026-09-09 · [ad hoc] S156 — claim: apply the retention policy to `HANDOFFS.md`, 5 receipts against a policy of 4 and 2 B under the ceiling

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: bring
`HANDOFFS.md` back inside its declared budgets by applying the retention policy at `HANDOFFS.md:8` —
adopted at **S127 by operator decision**, and selected as the session's work by the operator from
S155's close-out. **Fork-internal: `origin` and `upstream` untouched — no push, no PR, no tag, no
comment.**

**The forcing condition is the BYTE ceiling, not the token overage, and the difference matters.** At
claim time the file was **65,534 B — 2 B under `CEILING_BYTES` (65,536)**. The next session
physically could not write a receipt. The token figure is worse in appearance — **28,287 tokens
against a 25,000 cap, over by 3,287**, measured at S155 on the doubled-file meter — but
`methodology_trim.py`'s own `[TRIGGER_READ]` line rules that condition *"FOR REFERENCE AND NOT AS A
FAULT: … delivery is an ordered prefix and this ledger is newest-on-top, so what truncates is the
OLDEST records."* That is BL-52's point applied to this file: a newest-on-top ledger degrades
gracefully under truncation. **So the warrant quoted here is the 2 B of byte headroom and the
5-against-4 record count, not the token number.**

**THE TRIGGER DOES NOT FIRE, AND THIS TRIM IS NOT S154's.** `--check` **exits 0** — 65,534 B against
a 196,608 B Class A threshold — so this is the by-hand policy the retention paragraph describes
(*"applied by the session that notices"*), executed with the tool via an explicit `--cut`, not a
tool-initiated trim. **The pre-claim dry run `--cut 4` exits 0 with no `SRF_RED` and no `--force`
gate** (SRF **0.1096** vs the most recent archive `aa1c476`, against the **3.7022** that refused at
S154), and reports L1/L2/L3 all OK: 1 of 5 records to
`docs/archive/HANDOFFS-through-2026-09-04-2.md`, live 65,534 → 53,796 B. **S154's operator-approved
`--force` is not a precedent and is not needed here** — a fact recorded because the two trims will
otherwise read as one.

**This claim commit invalidates that dry run and it will be re-derived.** The stub above is a sixth
record and takes the file to **67,336 B, 1,800 B OVER the ceiling** — a deliberate, temporary breach
that the trim closes; nothing enforces the ceiling at commit time (the gate is wired to nothing).
`--cut 4` will therefore archive **2** records, not 1. Re-deriving after the claim is S153's gate,
and S154 recorded what skipping it costs.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-09 · [ad hoc] S155 close-out — the PR body for `read-set-budgets` → `upstream/main`, written and not opened

**Deliverable: [`docs/planning/read-set-budgets-to-main-pr-body.md`](docs/planning/read-set-budgets-to-main-pr-body.md), 14,806 B** — the
title, body, reviewer guide and verification record for a PR from `KJ5HST/methodology:read-set-budgets`
(`598c459`) to `upstream/main` (`512c2ed`). **NOT OPENED. Nothing pushed, no PR, no tag, no comment.**
Opening it is a separate go-ahead this session did not have and did not ask for.

**The headline is measured, and the instrument was validated before it was trusted.** The Phase 0
mandatory read — `SESSION_RUNNER.md` + `SAFEGUARDS.md` — goes **80,526 B / 28,234 tokens → 67,581 B /
23,902 tokens**, from **112.9%** of the 25,000-token read cap to **95.6%**, one read with 1,098 tokens
to spare. Both figures came off the doubled-file meter (`upstream-read-set-pr-plan.md` §7): concatenate
the pair, double it, read it, halve the refusal's token count. **The control ran first** — `upstream/main`'s
pair read *undoubled* reports **28,237** and doubled-and-halved reports **28,234**, reproducing §2.1's
recorded figure to 3 tokens. Without that check the number would have been a density transferred across
content types, which this repository has three separate learnings against.

**One draft claim was false and was caught by diffing rather than by re-reading.** The body first said
upstream's 13 inline learnings arrive in `FRAMEWORK_LEARNINGS.md` *"byte-for-byte"*. Row by row, **11 do;
#12 and #13 do not** — 2,400 → 1,450 B and 1,572 → 1,446 B, −1,076 B. The reason is in the same PR:
`bin/check-learnings` gains `ROW_BUDGET_BYTES = 1500` (`:106` on the branch, a constant `upstream/main`
does not have), and those two rows are the ones that breach it. The corrected sentence is the stronger
one, and rows #12/#13 are now item 2 of the body's reviewer list.

**Verification, every exit code read bare.** `bash bin/tests.sh` on `main`: Phase 0 baseline and close-out
both **304 passed / 1 failed / 0 skipped, exit 1**, diffed row for row by normalised assertion label —
**305 rows both sides, 0 status flips, 0 added, 0 removed**; the nine rows whose text differs each state a
count this session's own writes moved. In two detached worktrees, as the deliverable's own evidence:
pristine `upstream/main` **114 passed / 0 failed, exit 0**; `read-set-budgets` **115 passed / 1 failed,
exit 1**, **111 shared rows and zero status flips**. That single failure is `github source dry-run failed`,
and its cause was measured, not assumed: **3 of the branch's 27 manifest SOURCE paths are absent from
`upstream/main` and 0 from the branch**, so it fails a test about `main`'s contents and the merge is the
only thing that can flip it.

**A NEW MEASUREMENT THIS CLOSE-OUT PRODUCED, AND DID NOT ACT ON.** With this receipt `HANDOFFS.md` is
**65,531 B — 5 B under `CEILING_BYTES`** and, metered the same way, **28,287 tokens (56,573 doubled)
against a 25,000-token cap: over by 3,287.** That is failure mode #28 in the receipt ledger the PR body is
about. The byte ceiling is the wrong instrument here — 25,000 tokens is ≈57,900 B at the **measured
2.3164 B/token**, while `.context-budget.json` still declares **2.3648** and under-reports the file as
27,708 tokens. **The config was deliberately not edited**: re-deriving a density is one deliverable and
rewriting a provenance record is another, which is the same reason S154 declined the mirror-image bump.
The file also now holds **5 receipts against a retention policy of 4**, and the trimmer does not fire
(`--check` exits 0; trigger 196,608 B) — so the remedy is the by-hand policy at `HANDOFFS.md:8`, and
**S154's operator-approved `--force` is explicitly not a precedent for it.**

**Two operator decisions at the Phase 0 gate, each asked and neither inferred:** the deliverable (this
body, chosen over repairing the stale planning documents and over the `HOW_TO_USE.md` count fix), and
**keep `HEADER_RESERVE_BYTES` at 7,168 B** — closing S154's item (4). The front matter is untouched at
7,096 B. The receipt above was cut to fit in **twelve passes across two rounds** — written at 65,972 B and
cut to 65,526; then reopened to carry the token measurement below, which took it to 66,009; then cut again
to 65,531. The constant was never touched.

**New Learning #59** (1,094 B of a 1,500 B budget): *a plan's open decision can be closed by events rather
than by a decision, and no document will say so.*

**Three commits this session:** `3a3f52c` (the Phase 1B claim), `c3b9465` (`chore(history)` for the
append-only `.context-budget-history.jsonl`, which a bare `context_budget.py` run appends to), and
`2cb6fc2` (this close-out), plus the ledger-enumeration repair that carries this paragraph. **Nothing was
pushed: `origin/main` is unmoved at `f8531cf`**, `upstream/main` at `512c2ed`, `read-set-budgets` at
`598c459`; 0 open PRs on either repo. The ahead-count is deliberately not quoted — it drifts with each
repair commit that quotes it, which is precisely the defect S154 had to fix in its own receipt.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-09 · [ad hoc] S155 — claim: draft the PR body for `read-set-budgets` → `upstream/main`, the one upstream step still unopened

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: the PR
body for **`KJ5HST/methodology:read-set-budgets` (`598c459`) → `upstream/main` (`512c2ed`)**
([`upstream-read-set-pr-plan.md`](docs/planning/upstream-read-set-pr-plan.md) §11.3 item 7). Chosen
by the operator at the Phase 0 gate from three offered deliverables. **Writing the body is fork-side
and needs no go-ahead; OPENING the PR is a separate ask, and this session does not have it.** No
push, no PR, no tag, no comment.

**PHASE 0 FOUND THE RANKED NEXT STEP MOOT, AND THAT IS WHY THE DELIVERABLE MOVED.** S153 and S154
each ranked §11.3 item 1 — *"the PR's scope — four candidate payloads"* — first. **All four are
already merged upstream**, into the staging branch `read-set-budgets`, by PRs
[#76](https://github.com/KJ5HST/methodology/pull/76)–[#79](https://github.com/KJ5HST/methodology/pull/79)
between S141 and S151:

| payload | PR | present on `upstream/read-set-budgets` |
|---|---|---|
| Phase 1+2 — the learnings extraction | #76 | `starter-kit/FRAMEWORK_LEARNINGS.md` 56,673 B, blob `b21854cc` |
| `starter-kit/methodology_trim.py` | #77 | 113,629 B |
| Phase 3 — the apparatus | #78 | `FRAMEWORK_APPARATUS.md` 15,493 B |
| Phase 4 — the context-budget gate | #79 | `starter-kit/context_budget.py` 73,040 B + `.context-budget.json` 17,893 B |

**The scope question was answered incrementally, by four merges, while two documents went on posing
it as open.** `grep -n 'read-set-budgets'` returns **zero hits** in both
`upstream-read-set-pr-plan.md` and `port-branch-identity-adjudication.md`; each predates the series
and neither was revised after it. `port/framework-learnings-extraction` is **content-redundant** with
what shipped — same `starter-kit/SESSION_RUNNER.md` blob `c0550acd` (52,195 B, read-set pair
67,581 B) and the same `FRAMEWORK_LEARNINGS.md` blob `b21854cc` that S153's Tier-2 (a) froze — and
§11.3 item 4's `:92-94` defect **never reached upstream at all** (0 hits on both `upstream/main` and
`read-set-budgets`; it lives on `30ddf26` and on fork `main`).

**What is actually open is one PR that has never been opened.** `gh pr list --state all` shows no PR
with base `main` and head `read-set-budgets`. `upstream/main` **is an ancestor** of it
(`git rev-list --count upstream/read-set-budgets..upstream/main` = 0), so the merge is clean, and the
headline is measurable rather than rhetorical: of `bin/_manifest.py`'s **27 SOURCE** paths, **3 are
absent from `upstream/main`** — `starter-kit/FRAMEWORK_LEARNINGS.md`, `starter-kit/methodology_trim.py`,
`FRAMEWORK_APPARATUS.md` — and `bin/sync`'s `fetch_all_github` `sys.exit()`s before writing when any
source is absent, so `--source=github` installs **nothing** today. **0 of 27 are absent from
`read-set-budgets`.** That merge cures `bin/tests.sh` Test 9, this repository's only failing
assertion.

**The second operator decision at the same gate, recorded because a release and a refusal are both
actions.** S154's `next_steps` (4) asked whether to raise `HEADER_RESERVE_BYTES`
([`bin/check-handoff:663`](bin/check-handoff)) now that `HANDOFFS.md`'s front matter sits at
**7,096 of 7,168 B (99%, 72 B of headroom)** and the A1 fit leaves 21,504 B of slack. The operator
chose **keep 7,168 B**. The constant is unchanged and the reserve stays a real constraint: a
front-matter edit is still a byte negotiation, and the cut is what gets taken.

**Phase 0 baseline, exit codes read bare.** `bash bin/tests.sh` → **304 passed / 1 failed / 0 skipped,
exit 1**, matching S154's close-out row for row in count; the single failure is Test 9
`github source dry-run failed`, pre-existing. Both live ledgers backed up outside the repo and
`shasum -c` verified byte-identical after the run. Ledger reconciled against `git log` — every commit
since S152 carries an entry here, no ghost session. 0 open PRs on either repo. `main` 10 ahead of
`origin/main`.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-08 · [ad hoc] S154 — the receipt quoted a size its own writing had already moved

**`active_task` said *"`HANDOFFS.md` IS 42,938 B"*. True at `bad0489`; false by the time the
sentence existed.** Writing the close-out receipt and the two repair commits took the live file to
**54,258 B** — still four receipts, still under `CEILING_BYTES` 65,536, and the trimmer's trigger
still does not fire, but not the number written. Rewritten to quote **the delta the trim actually
made** — 245,254 → 42,938 B at `bad0489`, 27 receipts → 4 — plus a stated ~54 KB steady state, so no
future edit to this receipt can falsify it again. Same shape as S148's *"your own edit moves the
numbers you copied"*, in the field a next session reads first.

Refitting under the 12,288 B record budget after that rewrite took three more passes, landing at
**12,286 B**. Across this session that budget refused an edit **eleven times** and was never raised.

### 2026-09-08 · [ad hoc] S154 — an all-numeric abbreviated sha is invisible to `bin/check-handoff`, and it flipped the suite 304/1 → 303/2

**Found by the close-out suite run, not by review, and it is a checker limitation rather than a
ledger defect.** [`bin/check-handoff`](bin/check-handoff)`:211` defines
`SHA_RE = re.compile(r"\b(?=[0-9a-f]{7,40}\b)[0-9a-f]*[a-f][0-9a-f]*\b")` — **at least one hex
letter**, and its own docstring at `:477-478` states the consequence in terms: *"a bare 7+ digit
decimal is not a sha."* This session's claim commit abbreviates to **`1695734`**, seven digits and no
letter, so the answer-slot rule read the `commit:` field as naming no sha at all.

**It was invisible until a fixture moved the receipt.** `check_answer_slots` skips `blocks[0]`
unconditionally — the newest receipt is exempt, positionally — so while S154 sat newest, every
checker returned 0. `bin/tests.sh` Test 38 prepends a synthetic record to measure the per-record
budget edge, which pushes this receipt to second and subjects it to the rule: **`edge: exactly-12,288
B record wrongly rejected`**, and the suite went **304 passed / 1 failed → 303 / 2**. The failing
assertion names a *size* edge and the actual cause was a *sha* predicate — the message was about the
fixture, not the finding.

**Repaired by abbreviating to the first length that carries a letter**, `1695734f` (8 chars, unique,
`git rev-parse --short=8`) — the same commit, written so the predicate can see it. **The constant was
not touched**, consistently with the three other budgets this session cut an edit to satisfy. The
`commit:` slot was also **reconciled in full rather than deferred to S155**: `1695734f` + `aa1c476` +
`bad0489` + `f61c9d5` + `7e5d205` + this commit.

**A self-inflicted error inside the repair, recorded because it nearly shipped.** The first version
of that reconciled slot named **`0d7f1b5`** for the drifted-anchors commit. That sha was never read —
it was invented while typing a line whose entire purpose is to name real commits. The true value is
**`7e5d205`**. Caught by re-running `git rev-parse --short HEAD` immediately afterwards. Cutting the
receipt back under the 12,288 B record budget after adding gotcha (8) took six passes, and the
budget refused each one until it fit at **12,286 B**.

### 2026-09-08 · [ad hoc] S154 — four drifted `key_files` anchors in the S154 receipt, caught by the 3F sweep

**The close-out's own cross-reference check found them; nothing else would have.** Phase 3F says to
grep each cited destination rather than trust it, and four of this receipt's anchors had moved
between being written and the file settling: `bin/tests.sh:3095` → **`:3097`** (the A2 assertion —
`:3095` is a bare `fi`), `HANDOFFS.md:78` → **`:67`** (the archive table's new row 12 — `:78` had
become `status: complete`, inside a receipt), `HANDOFFS.md:68-72` → **`:69-73`**, and
`srf-red-refusal-adjudication.md:418` → **`:417`** (§11). The last one is instructive: it was read
off a saved command output whose **first line was a `wc -c` figure**, so every line number in that
capture was one too high — a citation taken from a transcript rather than from the file. Each
corrected anchor was re-read after the fix; the receipt stays at 12,208 B of the 12,288 B budget.

### 2026-09-08 · [ad hoc] S154 close-out — `HANDOFFS.md` trimmed under operator-approved `--force`: 245,254 B → 42,938 B, 27 receipts → 4

**The receipt ledger is back inside its retention policy for the first time since S132.**
`methodology_trim.py --check` now **exits 0 — *"trigger does not fire"*** (42,938 B against a
196,608 B budget), where at Phase 0 it exited 1. 23 records (2026-08-12 → 2026-09-04) are frozen in
[`docs/archive/HANDOFFS-through-2026-09-04.md`](docs/archive/HANDOFFS-through-2026-09-04.md) with its
`.verify.sh`. Four commits: `1695734` claim, `aa1c476` the trim, `bad0489` the fold, this close-out.

**TWO OPERATOR DECISIONS, ASKED ONE AT A TIME, NEITHER INFERRED.** The S129 deprioritisation was
released at the Phase 0 gate. The **`--force`** was a *second* gate, found while sizing the work and
put back separately — because
[`srf-red-refusal-adjudication.md`](docs/planning/srf-red-refusal-adjudication.md) §2 says of this
exact file *"the refusal STANDS, the trim must not be forced"*, and §11.2 supersedes that only in
part: S132 trimmed this file with **no force at all** and forced only `CHANGELOG.md`, on approval it
fenced as *"not a precedent for any other trim."* **A go-ahead for the deliverable is not a go-ahead
for a flag that overrides a standing written refusal.** The evidence offered with the ask: SRF
**3.7022 RED** against the most recent archive `78a29f8` but **0.5621 GREEN** against H3's
largest-drop boundary `a46f2f9`; §11.1's proof that the voting boundary is unsatisfiable by *any*
steady-state retention policy; §10's record that it may never have been ratified. None of that
repeals §2 — the operator did. **The force is scoped to this file, this regime, this evidence. The
next trim asks again.**

**THE PREDECESSOR'S RECIPE DOES NOT RUN, AND THAT IS WHY THE GATE WAS FOUND.** S153's `next_steps`
(4) said *"`--check`, `--write`, then `verify.sh`"*. `--check` exits 1 and reports the trigger; it
says nothing about the refusal. **`--write` alone exits 2 and writes nothing.** The refusal is also
**cut-independent** — `--cut 4` reproduces it byte for byte, the trigger being evaluated before any
depth is chosen — so no choice of depth routes around it. This is **Learning #57 — authored by S153
in that same session** — applied to its own handoff: an option nobody has executed is a proposal.

**BOTH COMMIT SHAPES WERE BUILT AND THE PROOF RUN ON EACH; THE ONE THE TOOL ITSELF PRESCRIBES FAILS.**
`methodology_trim.py` closes with *"one ledger, one shard, one entry, **one commit**, one revert"*,
while [`HANDOFFS.md`](HANDOFFS.md)`:68-72` orders a hand fold of the generated pointer block into the
archive table. Folded **inside** the trim commit the shipped proof fails — `L2 FRONT MATTER lost 1
line(s)`, exit **1**; folded in the **next** commit it exits **0**, the proof pinning to the trim
commit. New **Learning #58**. Distinct from **BL-50**, which is the *writer's* L2 refusing at write
time; this is the *generated proof* failing at re-derivation.

**THREE BUDGETS REFUSED AN EDIT AND ALL THREE TIMES THE CUT WAS TAKEN, NEVER THE CONSTANT.**
(1) `HEADER_RESERVE_BYTES = 7,168` — the fold's net cost would have breached the 46 B of headroom, so
the front matter was cut to **7,096 B (72 B clear, up from 46)**, and the bytes came out of claims
that had gone **false**: the N=4 warrant resting on the 56,750 B detector floor (§11.5 (5) forbids
re-deriving a depth from it) with its stale *"near 52 KB"*; the S127 warrant pointer **dangling
exactly as §11.5 (4) predicted**, since S152's trim moved those entries — now cited to
[`docs/archive/CHANGELOG-through-2026-09-02.md`](docs/archive/CHANGELOG-through-2026-09-02.md)`:2070`,
found by grep, the live file still matching `S127` twice so a presence check would have called it
healthy; and the S7/S8 collision example, every referent of which this trim archived. (2)
`bin/check-learnings`'s 1,500 B row cap refused Learning #58's first draft at 1,511 B — rewritten to
1,455 B. (3) `bin/check-handoff`'s 12,288 B record cap refused this receipt twice — the Phase 3A/3B
essays are what that budget is sized to exclude, and they were cut to fit at 12,208 B. **A comment
edit carrying Learning #58's rule into the front matter was measured, applied, and then REVERTED**
because it left 7 B of headroom; the rule lives in the Learning row instead.

**HANDED FORWARD AS A QUESTION, NOT DECIDED: the header reserve.** The front matter now sits at
**99% of 7,168 B** and blocked **two** correct edits in this one session, while the A1 fit uses only
**44,032 of 65,536 B — 21,504 B of slack**. Raising `HEADER_RESERVE_BYTES` is therefore
arithmetically free, which is precisely why S153 forbade doing it silently and why
[`bin/check-handoff`](bin/check-handoff)`:612` exists. **The trade is the operator's; this session
did not take it.**

**Verification — the deliverable's own proof run AFTER committing, four times with a negative
control.** `bash docs/archive/HANDOFFS-through-2026-09-04.md.verify.sh` → **exit 0**, *"L1,
L2/front-matter, L3 hold"*, source pinned to `aa1c476`, *"27 before = 4 retained + 23 archived"* — on
the raw trim in a clone, after the fold in a clone, and on the live tree; the one-commit shape,
deliberately built as a control, **failed (1)**. Write-time clauses all green: `L1_OK`, `L2_OK`,
`L3_OK` (27 records partitioned, every one byte-identical), `P1A_OK`, and the stale front-matter
count regenerated **24 → 4**. `bash bin/tests.sh` **304 passed / 1 failed / 0 skipped, exit 1 read
bare** — diffed **row for row** against the Phase 0 baseline by normalised assertion label: **303 rows
both sides, zero status flips, zero added, zero removed**; the failure is Test 9, pre-existing.
Checkers each bare: `check-links` **0** (105 links / 23 files), `check-learnings` **0** (57 rows),
`check-handoff` **0**. **`bin/model-report` reads the new shard** — 14 files, live 0 + archived 48,
the new shard contributing 5 — so the S133 glob fix held and this trim did **not** gut the tool the
way §11.3 records the `CHANGELOG.md` trim doing. `context_budget.py` now reports `HANDOFFS.md` as
**`warn` with a 77% density drift** (2.3648 B/token was measured at 186,617 B); `measured_bytes` was
deliberately **not** bumped, since raising it without re-deriving the density writes a false
provenance record. `CUT_STRADDLES_DAY` was **not** overridden — cuts are positional by design and
S152 refused the same override on the same provenance. Both live ledgers backed up outside the repo
and `shasum -c` verified byte-identical after every suite run.

**Self-score 8/10; predecessor S153 scored 8/10.** Both evaluations are below the receipt's closing
fence in [`HANDOFFS.md`](HANDOFFS.md).

### 2026-09-08 · [ad hoc] S154 — the pointer-block fold, and three front-matter claims that had gone false

Follows the trim commit rather than riding in it, **and that separation is a measured requirement,
not a style choice.** [`HANDOFFS.md`](HANDOFFS.md)`:68-72` instructs every trimming session to fold
`methodology_trim.py`'s generated 3-line pointer block into the archive table as one row (~160 B
against ~447 B) and delete the block. The tool's own closing line says the opposite — *"one ledger,
one shard, one entry, **one commit**, one revert."* **Tested in an isolated clone instead of
reasoned about: folding inside the trim commit FAILS the shipped proof** —
`FAIL: L2 FRONT MATTER lost 1 line(s), first: '**Archived shards — 11 trims, 116 receipts.**…'`,
exit **1**. Folded in the next commit, the same proof exits **0**, because it pins to the trim
commit. Both shapes were run; the green one shipped.

**Row 12 added** (23 records, 2026-08-12 → 2026-09-04, v1.5.0) and the undeclared
*"11 trims, 116 receipts"* count advanced to **12 / 139** — undeclared, so nothing regenerates it;
the `LedgerSpec` declares only the retained-receipt count, which the tool itself rewrote 24 → 4.
`116` was re-derived as the sum of the table's own `n` column before adding to it, not copied.

**THE FRONT MATTER HAD TO SHRINK, AND THE BYTES CAME OUT OF CLAIMS THAT WERE FALSE.**
`bin/tests.sh` Test 39 (2) asserts the live front matter fits `HEADER_RESERVE_BYTES = 7,168`
([`bin/check-handoff`](bin/check-handoff)`:663`), and it stood at **7,122 B — 46 B clear** before this
session. The fold's net cost would have breached it. S153's instruction was followed as written —
**cut the edit, never raise the reserve** — and the three cuts were chosen for being *wrong*, not for
being long:

- **The N=4 warrant was the detector-floor substitution this repo has already retracted twice.**
  *"Held at four, the live file rests near 52 KB, under the 56,750 B one-read cap"* — that figure is
  `READ_CAP_TOKENS × MIN_BYTES_PER_TOKEN`, a **floor for files with no measured density**, and
  [`srf-red-refusal-adjudication.md`](docs/planning/srf-red-refusal-adjudication.md) §11.5 (5) says
  in terms that *"a later session must not re-derive its depth from that sentence."* It was also
  numerically stale: the file is **43 KB**, not 52. Replaced with what is actually true — N=4 is an
  operator decision — and the sibling clause *"Four is the largest N that stays under the cap"*, the
  same substitution in the same paragraph, went with it.
- **The dangling warrant pointer §11.5 (4) predicted, now actually dangling.** The front matter said
  the retention policy's warrant *"is in that session's `CHANGELOG.md` entry"* with no sha and no
  shard. **S152's trim moved it**: the S127 entries are at
  [`docs/archive/CHANGELOG-through-2026-09-02.md`](docs/archive/CHANGELOG-through-2026-09-02.md)`:2070`
  and `:2131`. Located by grep, not assumed — the live `CHANGELOG.md` still matches `S127` twice, so
  a bare presence check would have called this reference healthy.
- **The S7/S8 collision example outlived its referents.** *"One is live here now: the bottom receipt
  is upstream's S12 (2026-08-12)"* — this trim archived every upstream receipt, so the sentence became
  false the moment it ran. The **rule** it illustrates (identify a receipt by session + date, never by
  number) is load-bearing at a resync and was kept; the four archived examples were not.

**Result: 7,570 → 7,096 B, 72 B of headroom — more than the 46 B this session inherited**, so the
next trim starts with more room rather than less. `bin/tests.sh` Test 39 reads
*"A2 truth: live front matter 7,096 B <= 7,168 B reserve (98% used)"*.

### 2026-09-08 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-04.md` (23 record(s), 245,254 B → 43,412 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **23** record(s) (2026-08-12 → 2026-09-04) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-04.md`](docs/archive/HANDOFFS-through-2026-09-04.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-04.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-04.md.verify.sh)
rather than trusting a digest printed here. Live file 245,254 B → 43,412 B (−82.3%).

### 2026-09-08 · [ad hoc] S154 — claim: trim `HANDOFFS.md`, 26 receipts against a retention policy of 4

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: run
[`starter-kit/methodology_trim.py`](starter-kit/methodology_trim.py) `--file HANDOFFS.md --cut 4
--write` on **this** repository's receipt ledger, archiving its oldest records into a frozen shard
under `docs/archive/` with the tool's own losslessness proof and `.verify.sh`, folding the generated
pointer block into the archive table as `HANDOFFS.md:68-72` instructs. **Fork-internal: `origin`
only. No action on `KJ5HST/methodology` — no PR, no comment, no tag, no release.**

**THE BLOCKER WAS RELEASED BY THE OPERATOR THIS SESSION, AND THAT RELEASE IS ITSELF THE RECORDED
ACTION.** This trim was deprioritised at **S129** and no repeal stood on record; S151, S152 and S153
each declined it on exactly that provenance and each was right to — S152 put the release question for
`CHANGELOG.md` and got `CHANGELOG.md` only, and said so in its own claim (*"`HANDOFFS.md` is
deliberately out of scope"*). Presented at this session's Phase 0 gate with the current measurement,
the operator chose **"2"** — the `HANDOFFS.md` trim — from a two-item ranking. **Asked, not inferred**,
which is the whole point: the S129 deprioritisation was never a standing prohibition, and neither is
its release a licence for the *next* ledger.

**The warrant, measured at Phase 0 and re-derivable.** This file is **244,288 B** across **26**
receipts against a retention policy of **4** (`HANDOFFS.md:8`, adopted at S127 by operator decision).
`python3 starter-kit/methodology_trim.py --file HANDOFFS.md --check` **exits 1 — the trigger FIRES**,
at 244,288 B against a 196,608 B Class A threshold. **It is NOT past the 262,144 B hard refusal** —
it clears it by **17,856 B** — so this is emphatically *not* the regime S132 forced `CHANGELOG.md`
in, and that difference is stated here so no later session reads the two as one precedent.

**A GATE FOUND AT THE CLAIM, NOT CARRIED IN FROM THE BRIEF: THE TRIM REQUIRES `--force`, AND THAT IS
A SECOND OPERATOR DECISION THIS SESSION DOES NOT YET HAVE.** The dry run **refuses, exit 2**:
`SRF_RED`, **SRF 3.6852** against the most recent archive `78a29f8`. The refusal is **cut-independent**
— `--cut 4` reproduces it byte for byte, because the trigger is evaluated before any depth is chosen —
so no choice of depth routes around it. Three facts bear on it and all three are already on record:

- **Against H3 as written the same trim is GREEN.** The tool reports **0.5595** vs H3's largest-drop
  boundary `a46f2f9` in the same breath, and labels its own voting boundary *"a policy addition on top
  of H3 … not dressed as a reading."* The two differ by **6.59x** on one file.
- **[`srf-red-refusal-adjudication.md`](docs/planning/srf-red-refusal-adjudication.md) §11.1 proves
  the voting boundary unsatisfiable by any steady-state retention policy** — an on-schedule trim scores
  exactly **1.0000** and the test is `>=`. That is this repository's own proof about its own rule.
  §10 records that the most-recent boundary may never have been **ratified**.
- **§2 of that same document says, for this exact file, *"the refusal STANDS, the trim must not be
  forced."*** §11.2 supersedes it only in part: S132 trimmed `HANDOFFS.md` with **no force at all**
  (SRF 0.2315) and forced only `CHANGELOG.md`, on approval it explicitly fenced as *"not a precedent
  for any other trim."* **So the standing instruction against forcing THIS file has never been
  repealed, and this session will not repeal it by inference.** The `--force` question goes back to
  the operator with the payload measured, per the record's own rule that a refusal is a claim to test.

**A second gate, arithmetic and unavoidable: the A2 reserve has 46 B of headroom and the trim spends
more than that.** `bin/tests.sh` Test 39 (2) asserts the live front matter fits
`HEADER_RESERVE_BYTES = 7,168` (`bin/check-handoff:663`). Measured now: **7,122 B, 75 lines — 46 B
clear.** A trim adds an archive-table row (~160 B by this file's own accounting at `:68-72`) and
rewrites the regenerated count, so **the front matter must be cut in the same commit**. S153's
instruction is followed as written: **cut the edit, never raise the reserve** — raising it is the
re-derive-the-budget-from-the-ceiling move `bin/check-handoff:612` exists to forbid.

**Two gates that are already satisfied, checked rather than assumed.** `bin/tests.sh` Test 34 reads
`ids[1]`/`ids[2]` of the live ledger and needs **three** receipts; retaining **4** clears it with one
of margin, which is the margin S127 chose the number for. And passing `--cut 4` **explicitly bypasses
the `choose_cut` defect S153 filed** (`starter-kit/methodology_trim.py:1014` — `resulting(k)` omits
the pointer block and regenerated-field growth before testing `stops(b)`): that arithmetic runs only
on the automatic search, never on an explicit retain count. The defect is unfixed and stays unfixed
here — it is distributed, so it wants upstream consideration, not a quiet fork fix.

**Phase 0 baseline, every exit code read BARE before any edit.** `bash bin/tests.sh` **304 passed /
1 failed / 0 skipped, exit 1** — the one failure is `github source dry-run failed`, pre-existing and
unrelated: 3 of 27 `bin/_manifest.py` sources are absent from `upstream/main` and `bin/sync` exits
before writing; nothing in a fork-internal trim can flip it. `bin/check-links` **0**,
`bin/check-learnings` **0** (56 rows, contiguous 1..56, 0 over 1,500 B), `bin/check-handoff` **0**.
Dashboard **76/100**, risk medium, 0 open issues. Reconcile clean: both ledger frontiers are
`d0c3813` with **0** undocumented commits and **0** line-anchored `status: pending`. Remotes
unchanged from S153's record — `upstream/main` `512c2ed`, `upstream/read-set-budgets` `598c459`,
0 open PRs on either repo. `core.hooksPath` **is set to `.githooks` in this clone** — the first
session in five able to say so; the four-session `--no-verify` streak is over. Both live ledgers
backed up outside the repo and `shasum -c` clean after the baseline suite, which mutates and
restores them.

### 2026-09-08 · [ad hoc] S153 close-out — Tier-2 (a) settled FREEZE; the port branch is `upstream/main` + 2 commits and passes row-for-row with zero status flips

**The decision is the operator's and it is recorded here as an action, because a decision leaves no
commit.** Tier-2 (a) — *what table does the Phase 5 port carry upstream?* — was deferred as a whole
on 2026-08-29 (`1593cb5`) alongside (b), and
[`port-branch-identity-adjudication.md`](docs/planning/port-branch-identity-adjudication.md) §6
Tier 2 deliberately declined to rank its three answers. Put to the operator with a measured
consequence column, he chose **freeze (iii)**: upstream receives the 46-row table as of 2026-08-27,
`starter-kit/FRAMEWORK_LEARNINGS.md` held byte-identical to blob `b21854cc`. He also directed that
the §5(b) `:92-94` rewrite ride along **as a second commit** rather than an amend, and that the
branch stay **local** — not pushed.

**EVERY CONSEQUENCE IN THE DECISION TABLE WAS RUN, NOT REASONED — AND THAT IS WHAT FOUND THE
DEFECT.** Each option's payload went through `bash bin/tests.sh` in a real worktree at `30ddf26`:
**freeze 113/1** (the control), **refresh 113/1**, and **option (v) as written 110/4**. The
`ed22ace` blob that §5's option (v) names by SHA **predates Phase 2's compaction**, so rows **#12
(2,400 B)** and **#13 (1,572 B)** breach the 1,500 B row budget that this very branch adds to
`bin/check-learnings` — upstream has the checker but not that arm (`ROW_BUDGET_BYTES`: 0 occurrences
on `upstream/main`, 7 on `30ddf26`). Three failures, all from those two rows. The option is
recoverable — Phase 2's *compacted* rows #1–#13 come back **113/1** at 14,072 B — but as posed
across three documents for ten days it would have shipped a branch whose own checker fails. **No
document had ever executed it.** New **Learning #57**.

**TWO OF MY OWN INSTRUMENTS WERE WRONG AND WERE CAUGHT BEFORE THE NUMBER REACHED THE OPERATOR.**
(1) The absent-artifact count first read **14 of 46** because it compared bare basenames
(`SESSION_NOTES.md`, `RECOMMENDED_SKILLS.md`) against full upstream paths; resolved by basename it is
**9 of 46**, which is *independently* the figure S123 recorded — agreement from a separate derivation,
not a copy. (2) The session-citation count first read **35 of 46**; restricted to the range the entry
actually claims (S35–S119) it is **32 of 46**, exactly as written. Both corrections happened before
publication; the raw matched items were eyeballed rather than trusted.

**The measured decision table, at today's tree rather than 2026-08-27's.** freeze **56,673 B / 46
rows / 78.4% of one read / 9 rows naming an artifact absent upstream / 35 citing a fork session**;
refresh **67,634 B / 55 / 93.6% / 9 / 44**; extraction **14,072 B / 13 / 19.5% / 0 / 3**. The fork's
table has drifted **10,961 B and 9 rows in the ten days** since `30ddf26`, which is freeze's standing
cost. Metered at the declared 2.8897 B/token against the 25,000-token read cap.

**True under every option, so it was stated as not bearing on the choice:** the fork's Test 9 stays
RED (2 of 27 manifest sources — `methodology_trim.py`, `FRAMEWORK_APPARATUS.md` — remain absent
upstream and `bin/sync:136` `sys.exit()`s before writing — **`:136`, not the `:134` this session's own claim entry and S152's handoff both carry; verified by grep at close-out.** That entry is left as written, per this ledger's append-only rule; the number is corrected here); the `:92-94` rewrite ships regardless; and
upstream's distributed seed carries no ceiling entry for this file, so nothing upstream measures
whatever is sent.

**The branch, built and verified — `port/framework-learnings-extraction` = `upstream/main` + 2.**
`30ddf26` is **untouched**, deliberately: it is cited **41 times across 8 files**, three of them
frozen archives, so an amend would have orphaned a SHA the record depends on. `7d5b186` rewrites the
referents bullet only. `starter-kit/FRAMEWORK_LEARNINGS.md` `hash-object` is still
`b21854cc2fc6a736801a5e87ae43b4407872eeef` — freeze verified as an identity, not asserted.
**Row-for-row, twice:** against `30ddf26`, **114 rows both sides, 114 shared, 0 status flips, 0 rows
added or removed**; against pristine `upstream/main` (**114/0**), **113 shared, 0 flips**, the single
differing row being `github source dry-run works` → `failed`. **That one failure has exactly one
cause and it is self-curing:** of the branch's 25 manifest sources, **1** is absent from
`KJ5HST/methodology` — `starter-kit/FRAMEWORK_LEARNINGS.md`, the file this PR adds. Merging the PR
cures its own only failure. **NOT PUSHED, NO PR** — `git ls-remote --heads origin` empty for the
branch; `upstream/main` `512c2ed` and `read-set-budgets` `598c459` unchanged; 0 open PRs on either repo.

### 2026-09-08 · [ad hoc] S153 — the `:92-94` defect rewritten on the port branch: a note declined on two false premises and a constant that resolves nowhere in its own tree

**`7d5b186`, the second commit on `port/framework-learnings-extraction`.** Plan §5(b) and §11.3 item 4
both say this rewrite ships under **every** Tier-2 (a) option, freeze included. The sentence it
removes declined a ~400 B clarifying note because it *"would break the file's byte-identity with the
fork, which is what lets `bin/sync` agree from either source."*

**Three defects, each verified against the branch's own tree rather than argued.** (1) **`bin/sync`
never reads a local ref** — `30ddf26:bin/sync:191` declares `--source choices=("local", "github")`: a
working tree, or the GitHub repo. No byte-identity between two local branches can make those agree.
(2) **The two sources already disagree** — of the 27 paths `bin/_manifest.py` distributes, **11
differ** between the fork's tree and `KJ5HST/methodology` and **3 more exist in only one**, so 14 of
27 disagree independent of this file. (3) **The 56,750 B / 77 B derivation resolves nowhere in the
tree it ships in** — `grep` finds no `READ_CAP_TOKENS`, no `MIN_BYTES_PER_TOKEN` and no `56750` in
that tree's `starter-kit/context_budget.py`. **A bullet whose subject is unresolvable referents closed
by citing one.** Sharper than the plan's *"stale derivation"* framing, and found by checking rather
than by accepting it.

**The disclosure itself was also short, and that was corrected in the same bullet.** Re-derived
against the branch tree, the rows name **8 unresolvable artifacts across 11 of the 46 rows**, not
*"Seven … across 10"*: `ledger-trimmer-design.md` (row 18) was missing from the list, and
`methodology_trim.py` appears both bare (24) and as `starter-kit/methodology_trim.py` (37). Every row
number is now printed so the claim is checkable. *"32 of 46 rows cite session numbers S35–S119"* was
re-derived and is **exactly right**. The note is still not added — but the reason is now the true one:
the file is held byte-identical to the ported blob, so the entry's counts stay checkable against it.
`bin/check-learnings` **0**, `bin/check-links` **0**, each read bare.

### 2026-09-07 · [ad hoc] S153 — claim: put Tier-2 (a) to the operator as a three-option decision, then build the branch it settles

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: the
**Tier-2 (a)** decision — *what does the Phase 5 port branch actually carry upstream?* — presented to
the operator as the three live options with **measured consequences attached to each**, then the
branch that his answer settles, assembled and verified. This is item (1) of S152's `next_steps` and
[`upstream-read-set-pr-plan.md`](docs/planning/upstream-read-set-pr-plan.md) §11.3 items 3 and 5.

**The options are not this session's to invent.** They are the three left standing in
[`port-branch-identity-adjudication.md`](docs/planning/port-branch-identity-adjudication.md) §6
Tier 2 — **freeze (iii)**, **refresh (iv)**, **extraction only (v)** — a table that document wrote
and then **deliberately declined to rank**, on the precedent that an operator's choice must not be
dressed as a measurement. Tier 1 was ratified 2026-08-29 (`1593cb5`); **Tier 2 was deferred as a
whole**, both (a) this table question and (b) the `:92-94` rewrite. This session re-derives the
consequence column against **today's** tree rather than quoting figures measured on 2026-08-27.

**§11.1 IS READ BEFORE THE OPTIONS ARE DRAFTED, BECAUSE IT CHANGES WHAT ONE OF THEM MEANS.**
`port/framework-learnings-extraction` is `upstream/main` (`512c2ed`) **plus one commit**, `30ddf26`,
and that commit carries **Phase 1's extraction together with Phase 2's output** — verified by blob
identity, `30ddf26:starter-kit/FRAMEWORK_LEARNINGS.md` and `364b410:starter-kit/FRAMEWORK_LEARNINGS.md`
are the same object `b21854cc` — so **"freeze the 46-row table" means keeping Phase 2's compacted
output, not reverting to a pre-Phase-2 state.** One commit is not one phase of content.

**Scope boundary, stated at claim time.** Branch assembly is §11.3 item **5**; **item 8 — the version
decision and the go-ahead itself — is not this session's**, and **opening the PR is a separate
go-ahead that this session does not have.** Fork-internal only: no PR, comment, tag or release on
`KJ5HST/methodology`.

**Phase 0 baseline, every exit code read bare, never through a pipe.** `bash bin/tests.sh`
**304 passed / 1 failed / 0 skipped, exit 1** — the one failure `github source dry-run failed` is
pre-existing (3 of 27 `bin/_manifest.py` source paths absent from `upstream/main`;
`bin/sync:134` `sys.exit()`s before writing anything). `bin/check-handoff` **0**, `bin/check-links`
**0**, `bin/check-learnings` **0**, `starter-kit/context_budget.py` **exit 2** (pre-existing,
read-set total 69,749 B / 56,750 B). Both live ledgers backed up outside the repo before the suite
ran and `shasum`-verified **byte-identical** after. **Ledger reconcile: nothing to backfill** — the
`CHANGELOG.md` and `HANDOFFS.md` frontiers are both `f8531cf` = `HEAD`, and
`git rev-list --count --no-merges <frontier>..HEAD` is **0** for each. Dashboard **76/100**, risk
medium. `upstream/main` `512c2ed` and `upstream/read-set-budgets` `598c459` unchanged; `gh pr list`
empty on both repos; `gh issue list` empty upstream (all 23 closed).

### 2026-09-07 · [ad hoc] S152 — pushed `main` to `origin`, deleted five merged local branches, and rewrote a `next_steps` that stated facts instead of naming actions

**Three actions, all operator-directed.** (1) `git push origin main` — `defefb0..71a8d33`, **verified
by reading the remote back** rather than from the push output: `git ls-remote --heads origin main`
and `git rev-parse origin/main` both `71a8d33`, `git rev-list --count origin/main..main` = **0**.
(2) `git branch -d` on the five branches `git branch --merged main` listed —
`docs/learning-13-handoff-predictions` (`73b72c0`), `pr1/framework-learnings-extraction`
(`5b92b2f`), `pr2/ledger-trimmer` (`56997af`), `pr3/apparatus-extraction` (`2c30d0f`),
`pr4/context-budget-gate` (`cf15489`). Each was confirmed an ancestor of `main` with
`git merge-base --is-ancestor` **before** deletion, and `-d` (never `-D`) would have refused any that
was not. **LOCAL ONLY — one copy of each still exists on `origin`**, and removing those is an
outward action on the fork that was not requested; it is `next_steps` (6). **Nothing on
`KJ5HST/methodology`:** `upstream/main` `512c2ed` and `read-set-budgets` `598c459` unchanged, 0 open
PRs.

**(3) THE `next_steps` FIELD WAS REWRITTEN BECAUSE THE OPERATOR CAUGHT IT STATING STATE INSTEAD OF
PRESCRIBING ACTION** — and that is a **protocol violation**, not a style note.
`starter-kit/SESSION_RUNNER.md` §3D's Minimum Handoff Requirement **3** is *"What's next — specific
and actionable"*, whose own bad example is *"Pick next from backlog"* and whose rule is that a
handoff missing it *"will score ≤4/10 by the next session."* The version shipped at `71a8d33` failed
it three ways: item (1) opened *"DO NOT START …"*, a **prohibition** with no accompanying task;
items (2) and (3) opened *"`HANDOFFS.md` IS NOW THE LOUD ONE"* and *"THE TRIMMER SHIPS A STOP IT DOES
NOT HONOUR"*, both **descriptions of a condition** with no verb; and the two genuinely-next actions —
push, delete the branches — sat **outside the numbered list** as loose trailing prose, so the ranked
list did not contain the ranked work.

**What replaced it.** Six items, each opening with an **imperative** and carrying its first command,
with any gate named **before** the verb: (1) *put Tier-2 (a) to the operator as a three-option
decision, then build the branch* — the upstream plan's next phase, §11.1 read first because it
changes what the options mean; (2) *rewrite `30ddf26:CHANGELOG.md:92-94`*, explicitly **not** blocked
by (1); (3) *ask the operator to release `HANDOFFS.md`, then trim it*, with the three gates that trim
must clear; (4) *change `HOW_TO_USE.md:774` 27 → 28*; (5) *fix `choose_cut`*; (6) *delete the five
branches on `origin`*. **The ranking rule is unchanged and is why (1) is (1):** handoff item 1 is the
upstream plan's next phase, never fork housekeeping.

**The budget forced the trade, and the checker dictated which way it went.** Adding the actions took
the record to **13,132 B** against the 12,288 B per-record budget. `bin/check-handoff`'s refusal text
is prescriptive — *"CUT THE TRAILING PROSE FIRST … the Phase 3A/3B essays below the closing fence are
what it is sized to exclude"* — so the 3A/3B essays were cut across four rounds and **no finding was
removed from `next_steps`**. Final record **12,282 B**, 6 B of margin. `bin/check-handoff` **0** bare
and `--all`.

### 2026-09-07 · [ad hoc] S152 — Phase 3 completed: the 3A/3B evaluations and Learning #56 that the close-out skipped, and a self-score revised 8 → 7

**A correction to this session's own close-out (`00347a7`), recorded rather than quietly patched.**
That commit reported Phase 3 complete. **It was 3 of 7 steps short:** 3A (evaluate the predecessor's
handoff), 3B (self-assess) and 3C (document learnings) were never performed. The operator had to ask
for them. Steps 3D–3G *were* done, which is why nothing caught it — **`bin/check-handoff` returned
exit 0 throughout**, and that is exactly what `starter-kit/SESSION_RUNNER.md` §3D says it means:
the checker *"asserts its presence and completeness, never its quality (a green check is not a good
handoff — that stays the next session's 3A score)."* A mechanical gate passing over a missing
compounding step is the gate behaving correctly and the session behaving badly.

**3C — Learning #56 appended to [`starter-kit/FRAMEWORK_LEARNINGS.md`](starter-kit/FRAMEWORK_LEARNINGS.md):**
*"A convention counted across a corpus can be a sample of the rule's OUTPUT, not the rule — and the
lone exception is often the case the written policy was built around."* Sourced from this session's
8-of-9 shard survey, which argued for a calendar cut and was backwards. `bin/check-learnings` **OK —
55 rows, contiguous 1..55, 0 over 1,500 B**. **The next number was 56, not 55:** `#14` is
deliberately reserved (`bin/check-learnings:74`, `RESERVED_RE`), so the checker's *"contiguous
1..54"* message describes a count while the highest live row number was already **55**. Read the
raw rows, not the summary line.

**3A/3B — written below the receipt's closing fence, and the budget is what constrains them.**
`bin/check-handoff` refused the first draft: *"record S152 is 13,786 B, over the 12,288 B
per-record budget by 1,498 … CUT THE TRAILING PROSE FIRST."* The budget is sized so the six
mandatory fenced requirements fit and the 3A/3B essays are what it excludes; the receipt already
carries their conclusions as `self_score` and `predecessor_score`. Three lower-value lines were cut
rather than any finding. Final record **12,222 B**, 66 B of margin. Worth noting the house
convention is genuinely mixed: S150, S149 and S148 carry **2 B** of trailing prose — none at all —
while S151 carries 3,106 B.

**`self_score` revised 8 → 7 in the receipt, and the reason is the skip, not the deliverable.** The
trim itself is unchanged: complete, and proved twice from independent instruments. But a phase
reported complete while 3 of its 7 steps were missing is not an 8, and the three missing steps are
precisely the ones that exist for someone other than this session. **Predecessor S151 scored 7/10** —
its refusal to trim on unrepealed operator provenance was the single most useful thing it did for
this session, against a `next_steps` (4) that was false and ranked already-finished work.

**A DEFECT FOUND BY THE 3F CROSS-REFERENCE SWEEP, RECORDED NOT FIXED (FM #17).**
[`HOW_TO_USE.md`](HOW_TO_USE.md)`:774` says the failure-mode table is *"A table of **27** documented
agent tendencies"*. **The highest FM row is 28**, and [`CLAUDE.md`](CLAUDE.md)`:104` already says 28.
It is **live prose** under *#### What the Session Runner Contains* — not frozen release notes, so it
is unlike `README.md`'s v3.2–v3.6 sections where *"the count stays 27"* is correct as shipped and
must **not** be "fixed". **`HOW_TO_USE.md` is `TRACKED` in `bin/_manifest.py`, so the stale count
ships to every adopter.** Pre-existing, unrelated to this session's diff, and left for a session that
can own it. ⚠ **Do not count it with `grep -c '^| [0-9]* | \*\*' starter-kit/SESSION_RUNNER.md` —
that returns 34**, because the runner holds more than one numbered table; take the highest FM row
number instead. That is S12's gotcha (2), reproduced exactly here.

**No new verification claim is made for the deliverable.** The trim's evidence stands as recorded at
`00347a7`. This commit re-ran what its own diff can affect: `bin/tests.sh` (a distributed file
changed), `check-learnings`, `check-handoff` bare and `--all`, `check-links` — results in the
receipt's `runtime_smoke`. **Fork-internal: no PR, comment, tag or release.**

### 2026-09-07 · [ad hoc] S152 close-out — `CHANGELOG.md` is readable again: 269,571 B → 98,341 B, 54 records to a frozen shard, self-score 8/10

**Phase 3D/3F. Deliverable complete.** Three commits plus this close-out: `0f3f693` the claim,
**`aaa6d30` the trim**, `f2117bd` the `chore(history)` for the append-only `.jsonl`.
**FORK-INTERNAL ONLY — no PR, comment, tag or release on `KJ5HST/methodology`.** `upstream` refs
re-read at Phase 0 and unchanged: `main` `512c2ed`, `read-set-budgets` `598c459`; `gh pr list` empty
on **both** repos.

**THE FILE PHASE 0 MANDATES READING WAS UNREADABLE, AND THAT IS NOW MEASURED RATHER THAN INFERRED.**
At claim time `CHANGELOG.md` was 263,953 B and by the claim commit 269,571 B, against
`READ_REFUSE_BYTES` = 262,144 B (`starter-kit/methodology_trim.py:130`). I did not read the constant
and predict: a default `Read` returned **no content at all** — *"File content (257.8KB) exceeds
maximum allowed size (256KB)"*. It is now **98,341 B**, with **163,803 B** of headroom to the refusal
and **98,267 B** to the 196,608 B fire trigger. `methodology_trim.py --file CHANGELOG.md --check`
exits **0** — the trigger no longer fires.

**LOSSLESSNESS IS PROVED TWICE, FROM TWO INDEPENDENT INSTRUMENTS.** (1) The tool's own clauses, all
green on the artifacts: `L1_OK` (records-zone concatenation byte-identical), `L2_OK` (zones pinned,
front-matter diff confined to declared changes), `L3_OK` (80 records partitioned, every one
byte-identical across the move), `P1A_OK` (26 → 27 entries). `bash
docs/archive/CHANGELOG-through-2026-09-02.md.verify.sh` re-derives all three **from git** at the trim
commit and exits **0**. (2) **`bin/tests.sh` conserves the population without being asked to** —
live `**Model:**` bullets **41 → 8**, archived **238 → 271**, total **279 → 279**. The two deltas are
exactly ±33. That check exists only because S132 taught `bin/model-report` to glob the shards; before
that fix this trim would have blinded it to 33 of 41 entries with every row still green.

**THE ONE DESIGN CHOICE WAS SETTLED FROM PROVENANCE, AGAINST MY OWN FIRST MEASUREMENT.** The dry run
raises `CUT_STRADDLES_DAY` and offers `--cut <earlier date>`. I surveyed the nine dated shards and
found **8 honour a clean day boundary and 1 does not**, and was ready to recommend a calendar cut on
that 8-of-9 evidence. **It points the wrong way.** The ninth —
`CHANGELOG-through-2026-08-30.md` — is precisely the shard this file's own front matter (`:54`)
cites when it ratifies *"that boundary is POSITIONAL, not a calendar seam … The sections are the
calendar; the file boundary is not."* [`ledger-trimmer-design.md:219`](docs/planning/ledger-trimmer-design.md)
§2.3 says the same at the source — *"cuts are by **position in file order**, never by sorting on a
parsed key"* — and its §3.1 table gives this file's cut key as literally `position`. **A majority
across a corpus is a sample; the outlier was the one carrying the policy.** Default cut taken, no
override.

**A DEFECT IN THE DISTRIBUTED TRIMMER, FOUND BY ASKING WHY A NUMBER WAS 37 B TOO BIG.** The dry run
projected **98,341 B** while `CLASS_A_STOP_BYTES` (`:165`) is **98,304**. `choose_cut` (`:1014`)
selects the largest retained count `k` for which `stops(b)` holds, computing `b` from the
**pre-trim** front matter: `resulting(26)` = **97,108 B**, comfortably under. The write then adds
**1,233 B** of front matter — a 453 B pointer block plus regenerated fields — so the file lands
**37 B above the stop the selection was supposed to guarantee**. Immaterial here (0.04%, against
98,267 B of hysteresis) and **deliberately not worked around with `--cut`**: overriding the ratified
default to hide a tool defect would have made the next session's dry run inconsistent with this one
and left nothing on the record. **The tool is DISTRIBUTED** (`bin/_manifest.py`), so the fix is
adopter-facing and is its own deliverable. **Recorded, not fixed** (FM #17).

**A FALSE PREMISE IN MY PREDECESSOR'S HANDOFF, CAUGHT BEFORE IT COST THE SESSION.** S151
`next_steps` (4) calls the `context_budget.py` exit-2 *"Phase 2 of the older
`upstream-read-set-pr-plan.md`, **never executed**."* **Phase 2 shipped at S119** — `28551a5` (scope
the row budget to every row, driven RED) and `364b410` (compact all 20 over-budget rows, 73,712 →
56,673 B), both verified ancestors of `main`; `bin/check-learnings` reports **0 over 1,500 B**,
exit 0. And the 69,749 B is `starter-kit/SESSION_RUNNER.md` (54,363) + `starter-kit/SAFEGUARDS.md`
(15,386), class `read-set`; `starter-kit/FRAMEWORK_LEARNINGS.md` is class `on-demand` and is **not a
member**, so Phase 2 could never have closed that gap. **§11 of that very plan
(`upstream-read-set-pr-plan.md:483`) had already corrected both errors, naming S130 for making them.
This is the third recurrence, and the mechanism is identical each time: the session took its premise
from the previous receipt rather than from the plan the receipt cites.** Consequence for ranking:
**all four executable phases (1–4) are shipped**; only **Phase 5**, which needs the operator's
explicit go-ahead, remains.

**Verification, every command run bare, compared row-for-row against a Phase 0 baseline.**
`bash bin/tests.sh` **304 passed / 1 failed / 0 skipped, exit 1** — identical summary, identical
**305** rows, and **ZERO status flips**; every differing row is `PASS` on both sides and every changed
value is a count the trim moved. The one failure, `github source dry-run failed`, is pre-existing and
its cause was measured rather than assumed: **3 of 27** `bin/_manifest.py` source paths
(`FRAMEWORK_APPARATUS.md`, `starter-kit/FRAMEWORK_LEARNINGS.md`, `starter-kit/methodology_trim.py`)
are absent from `upstream/main`, and `bin/sync:134` `sys.exit()`s before writing anything.
`check-links` **0**, `check-learnings` **0** (54 rows, contiguous 1..54), `check-handoff
--allow-pending` **0**, `--all --allow-pending` **0**. `unittest`: dashboard **321 OK**,
`methodology_trim` **123 OK**, `context_budget` **116 OK** (result row isolated from the advisory
prose it prints after it). Dashboard twins `cmp` **silent**. `context_budget.py` **exit 2**,
unchanged and pre-existing. Both ledgers verified byte-identical to their commits **after** the suite
run, which mutates and restores them — checked against `git status`, not against a copy of themselves.

**ZERO ADOPTER SURFACE, established by grepping the whole manifest rather than one column.** The only
`CHANGELOG` row in `bin/_manifest.py` is `("starter-kit/CHANGELOG.md", "CHANGELOG.md", SEED)` — the
**seed**. The root ledger trimmed here is this repository's own and is distributed nowhere.

**`HANDOFFS.md` was deliberately left alone.** At 222,968 B it is past its own 196,608 B trigger but
**39,176 B clear of the refusal**, and it holds 25 receipts against the ratified cap of 4. One
deliverable is one deliverable; that trim is a real piece of work with its own losslessness proof and
its own `bin/tests.sh` Test 34 three-receipt floor to respect.

### 2026-09-07 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-09-02.md` (54 record(s), 269,571 B → 98,341 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **54** record(s) (2026-08-12 → 2026-09-02) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-09-02.md`](docs/archive/CHANGELOG-through-2026-09-02.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-09-02.md.verify.sh`](docs/archive/CHANGELOG-through-2026-09-02.md.verify.sh)
rather than trusting a digest printed here. Live file 269,571 B → 98,341 B (−63.5%).

### 2026-09-07 · [ad hoc] S152 — claim: trim `CHANGELOG.md`, which is 1,809 B PAST the 262,144 B hard read refusal

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: run
[`starter-kit/methodology_trim.py`](starter-kit/methodology_trim.py) `--file CHANGELOG.md --write`
on **this** file, archiving its oldest records into a frozen shard under `docs/archive/` with the
tool's own losslessness proof and `.verify.sh`. **Fork-internal: `origin` only. No action on
`KJ5HST/methodology` — no PR, no comment, no tag, no release.**

**The warrant is a measurement, and it is new since S151 wrote its handoff.** This file is
**263,953 B**. `starter-kit/methodology_trim.py:130` sets `READ_REFUSE_BYTES = 256 * 1024` =
262,144 B — *"a SECOND and HARDER boundary, and it is NOT truncation"* — so this ledger is **1,809 B
(1.0069×) past it**. Verified by running the tool rather than by reading the constant: a default
`Read` of `CHANGELOG.md` returns **no content at all**, front matter included —
*"File content (257.8KB) exceeds maximum allowed size (256KB)"*. The artifact Phase 0 mandates
reconciling is, today, unreadable by the tool Phase 0 uses. S151 measured **243,957 B** and called it
*"~18 KB from"* the refusal; its own five close-out commits carried it across.

**THE BLOCKER WAS RELEASED BY THE OPERATOR THIS SESSION, AND THAT RELEASE IS ITSELF THE RECORDED
ACTION.** The trim was deprioritised at **S129** — when the file in question was `HANDOFFS.md` at
5 receipts and 7,305 B over a *soft* one-read cap — and no repeal stood on record; S151 declined the
trim on exactly that provenance and was right to. Presented at this session's Phase 0 gate with the
changed fact pattern (a *hard* refusal, on the *other* ledger), the operator chose **"Trim
CHANGELOG.md"**. `HANDOFFS.md` is deliberately **out of scope**: at 221,606 B it is past its own
196,608 B trigger but still **40,538 B clear of the refusal**, and one deliverable is one deliverable.

**The cut is POSITIONAL and this session will not override it.** The dry run flags
`CUT_STRADDLES_DAY` and offers `--cut <earlier date>` for a clean calendar seam. **Refused, on
provenance, not on preference.** Design
[`docs/planning/ledger-trimmer-design.md`](docs/planning/ledger-trimmer-design.md) §2.3 states *"cuts
are by **position in file order**, never by sorting on a parsed key"* and its §3.1 table gives this
file's cut key as literally `position`; this file's own front matter (`:56`) ratifies the same rule —
*"that boundary is POSITIONAL, not a calendar seam … The sections are the calendar; the file boundary
is not."* A survey of the nine dated shards shows **8 honour a clean day boundary and 1 does not** —
and the one that does not, `CHANGELOG-through-2026-08-30.md`, is precisely the shard the front matter
cites as the reason the convention is a span label. **That 8-of-9 count is a sample that points the
wrong way**; the ninth carries the policy.

**Planned cut, from the dry run and to be re-derived before `--write`:** archive **52 of 79** records
(span 2026-08-12 → 2026-09-02) to `docs/archive/CHANGELOG-through-2026-09-02.md`; live
**263,953 B → 98,303 B**, one byte under the 98,304 B `CLASS_A_STOP_BYTES`. Proof clauses all green
on the dry run: `L1_OK` (records-zone concatenation byte-identical), `L2_OK` (zones pinned,
front-matter diff confined to declared changes), `L3_OK` (79 records partitioned, every one
byte-identical across the move).

**Phase 0 baseline, every command run bare before any edit.** `bash bin/tests.sh` **304 passed /
1 failed / 0 skipped, exit 1** — the one failure is `github source dry-run failed`, pre-existing, and
its cause was measured this session rather than assumed: **3 of 27** `bin/_manifest.py` source paths
(`FRAMEWORK_APPARATUS.md`, `starter-kit/FRAMEWORK_LEARNINGS.md`, `starter-kit/methodology_trim.py`)
are absent from `upstream/main`, and `bin/sync:134` `sys.exit()`s before writing anything. Nothing in
a fork-internal trim can flip it. `bin/check-links` **0**, `bin/check-learnings` **0** (54 rows,
contiguous 1..54, 0 over 1,500 B), `bin/check-handoff` **0**, `--all` **0** (24 receipts).
`starter-kit/context_budget.py` **exit 2** (read-set total 69,749 B / 56,750) — pre-existing and
out of scope. Ledger accounting before: **442** source-tagged dated entries across live + archives,
**79** records live, **24** receipts. Both ledgers backed up outside the repo and `shasum -c` clean
after the baseline suite run, which mutates and restores them.

**A correction to S151's handoff, carried here because it misdirects the next session.** Its
`next_steps` (4) calls the `context_budget.py` exit-2 *"Phase 2 of the older
`upstream-read-set-pr-plan.md`, **never executed**."* **Phase 2 shipped at S119** — `28551a5` (scope
the row budget to every row, driven RED) and `364b410` (compact all 20 over-budget rows, 73,712 →
56,673 B), both verified ancestors of `main`; `bin/check-learnings` reports **0 over 1,500 B**,
exit 0. And the 69,749 B is `starter-kit/SESSION_RUNNER.md` (54,363) + `starter-kit/SAFEGUARDS.md`
(15,386) — class `read-set` in `.context-budget.json`; `starter-kit/FRAMEWORK_LEARNINGS.md` is class
`on-demand` and is not a member, so Phase 2 could never have closed that gap. This is the **third**
recurrence of the drift §11 of that plan was written to stop — each session taking its premise from
the previous *receipt* rather than from the plan the receipt cites. **All four executable phases
(1–4) are shipped; only Phase 5, which needs the operator's explicit go-ahead, remains.**

### 2026-09-04 · [ad hoc] S151 close-out — Phase B DONE: `upstream/read-set-budgets` (`598c459`) MERGED into fork `main` as `213f841` and pushed to `origin`

**Phase 3D/3F.** Deliverable: Phase B of
[`docs/planning/upstream-read-set-budgets-merge-plan.md`](docs/planning/upstream-read-set-budgets-merge-plan.md)
§3, under the operator's explicit go-ahead. **A real two-parent merge commit `213f841` (parents
`8bfff1e` + `598c459`), never a squash and never an `-X` strategy shortcut**, pushed to the fork:
`origin/main` = local `main` = `f7c7008`, 0 unpushed. **FORK-INTERNAL — no PR, comment, tag or
release anywhere; `upstream` refs re-read after the push and unchanged from Phase 0** (`main`
`512c2ed`, `read-set-budgets` `598c459`), `gh pr list` empty on both repos. Completeness measured,
not assumed: `git rev-list --count main..upstream/read-set-budgets` = **0** and `main..upstream/main`
= **0**, so upstream's own S12 release commit came in too, and all four `pr1`–`pr4` branches now
report as fully merged.

`git merge --no-commit` produced **exactly the 20 conflicts §2.2 enumerates**, re-derived against
today's tree before starting rather than trusted from the plan's snapshot. **14 keep-ours, each
verified byte-identical to `HEAD` after resolution**; **2 take-theirs verified byte-identical to
upstream's blob** (`tools/test_context_budget.py`, which discharges D11's back-port follow-on by
construction, and `tools/test_methodology_trim.py` 2,170 → 2,259 lines, the portable synthetic
fixtures). **Row 7 was adjudicated on the merits rather than on the plan's authority:** measuring the
file's real link sites showed fork's *"Phase 2 step 8"* named **one of three** (`:189`–`:191` are
steps 6, 7 and 8), while upstream's sentence additionally names `:309`'s honest-accounting bullet and
`:478`'s *Across the Full Series*, both of which genuinely carry links — all seven anchors confirmed
to resolve in `FRAMEWORK_APPARATUS.md`. **Row 13 recomputed to the measured 27** (23 markdown + 4
non-markdown); both sides' *"24"*/*"25"* were stale. Ledgers interleaved by date per §2.3: upstream's
four `CHANGELOG.md` entries placed **after** fork's of the same date (the tie-break this file's own
front matter documents), the two pre-2026-08-30 ones at the bottom, **no frozen archive shard
touched**; upstream's S12 receipt kept, placed last, its `---` separator normalised to
`HANDOFFS.md`'s convention, and the front matter's collision paragraph now names the resulting
**live** S12 collision (fork's own S12 is 2026-07-25, archived). **Beyond what the plan asked:** it
says only to "re-verify" the 90-path auto-merged set, so this session checked whether upstream
content had been *dropped* there — of the four both-sides paths upstream had touched only
`starter-kit/SESSION_RUNNER.md`, and **all 3 of its added lines survive while 0 of its 18 deleted
lines do.**

**Two of the plan's own verify-column expected values were wrong, recorded as measured rather than
smoothed over:** `context_budget.py` was to *"exit 0 after"* — it exits **2**, identically before and
after (the pre-existing read-set overage, Phase 2 of the older plan, never executed); and `grep -c
'methodology_trim.py' starter-kit/BOOTSTRAP.md` was to be **1** — it is **5**, and was 5 pre-merge.
The second invites a destructive repair. Recorded as new **Learning #55** in
`starter-kit/FRAMEWORK_LEARNINGS.md` (54 rows, contiguous, 0 over the 1,500 B row budget).

**The retention trim was deliberately NOT done, on provenance rather than oversight.**
`HANDOFFS.md` holds **24** receipts against the ratified cap of **4**, and both ledgers now fire
`methodology_trim.py --check`. §2.3 step 4 says *"trim to 4"*, but the same plan's `next_steps` (3)
says the overage is *"not this plan's or this close-out's to act on"*, and **the operator
deprioritised this trim at S129 with no repeal on record**. Step 4 assumed a file already near the
cap; a 24 → 4 trim is a deliverable with its own losslessness proof. Raised for the operator, not
absorbed.

**Verified.** `bash bin/tests.sh` **304 passed / 1 failed / 0 skipped, exit 1** — compared **row for
row** against the pre-merge baseline: **zero status flips**. The one failure is Test 9
(`--source=github`), pre-existing, and §2.4 predicted a fork-internal merge could not flip it — it
did not. An intermediate run read **303/2**: this session's own front-matter edit had pushed
`HANDOFFS.md`'s header 205 B over its 7,168 B reserve and turned Test 39's A2 RED. Fixed as this
repo's own notes prescribe — **cut the edit, do not raise the reserve** — now 7,122 B. `check-links`
**0** (105 links / 23 files), `check-learnings` **0**, `check-handoff --all` **0** at close-out.
`unittest`: dashboard **321 OK**, context_budget **116 OK**, methodology_trim **123 OK** — the last
being row 20's never-before-run combination. `cmp` of the two dashboard twins silent. Ledger
accounting: **74 → 78** dated entries and **437 → 441** source-tagged across live + archives;
receipts **23 → 24**. Both ledgers `shasum -c` clean after every suite run. Adopter surface, which
the plan did not ask for: `bin/sync <tmp> --mode=commit` exit **0**, **27 files** installed, the
merged `ITERATIVE_METHODOLOGY.md` sentence and Learning #55 both landing. Not exercised: upstream CI
(neither side has `.github/workflows` — confirmed absent, not assumed), the maintainer's machine,
`--calibrate`.

**Model:** Claude Opus 5 (1M context).

### 2026-09-04 · [ad hoc] S151 — claim: Phase B of the merge plan — merge `upstream/read-set-budgets` (`598c459`) into fork `main`

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: execute
**Phase B** of [`docs/planning/upstream-read-set-budgets-merge-plan.md`](docs/planning/upstream-read-set-budgets-merge-plan.md)
§3 — the real 3-way merge of `upstream/read-set-budgets` (`598c459`, PR #79 merged) into fork `main`
(`94ea01f` at claim), authorized by the operator's explicit go-ahead this session (*"do phase B"*),
the same gate PR 4's own Phases C and D each required. **Fork-internal: `origin` only. No action on
`KJ5HST/methodology` — no PR, no comment, no tag, no release.**

Scope, exactly as §2.2/§2.3/§2.4 state it and no wider: `git merge upstream/read-set-budgets
--no-commit` (never a `-X ours`/`-X theirs` shortcut), all **20** conflicting paths resolved per
their stated rule (13 keep-ours, 3 take-theirs, 2 decided on their own terms, 2 ledgers), both
ledgers interleaved by date per §2.3's rule, the full §2.4 command set run bare and its **measured**
results recorded in the merge commit message, then a real two-parent merge commit (never a squash)
pushed to `origin`. Conflict count re-derived at Phase 0 against today's tree: `git merge-tree
--write-tree --name-only main upstream/read-set-budgets` → **20 CONFLICT lines**, matching §2.2
row-for-row.

Phase 0 baseline, run bare before any edit: `bash bin/tests.sh` **304 passed / 1 failed / 0 skipped,
exit 1** (the one failure `github source dry-run failed` is Test 9, pre-existing, and §2.4 states
plainly it will NOT flip from this merge). `check-handoff` **0**, `--all` **0** (22 receipts),
`check-links` **0**, `check-learnings` **0** (53 rows, contiguous 1..53), `context_budget.py`
**exit 2** (read-set total 69,749 B / 56,750 — pre-existing, the never-executed Phase 2 of the older
read-set PR plan, out of scope here).

**Model:** Claude Opus 5 (1M context).

### 2026-09-04 · [ad hoc] S150 close-out — the upstream/read-set-budgets merge plan DONE: `docs/planning/upstream-read-set-budgets-merge-plan.md` committed, Phase B NOT authorized

**Phase 3D/3F.** Deliverable: the one plan the S150 claim scoped — a real, mechanically-verified
evidence-based inventory of every path `upstream/read-set-budgets` (`598c459`, PR #79 merged) conflicts
on with fork `main`, a resolution rule and verification command per path, and the two-phase structure
`SESSION_RUNNER.md` §Planning Sessions requires. **No merge, no push, no upstream action.**
`git merge-tree --write-tree --name-only main upstream/read-set-budgets` → tree `a9b72fee…`, exit 1,
**20 conflicting paths (4 add/add, 16 content)** — corrects the interrupted S150 stub's unverified guess
of *"5 add/add, 15 content"*. Each of the 20 individually diffed (`git diff --stat <merge-base> main --
<path>` / `… upstream/read-set-budgets -- <path>` / `diff <(git show main:<path>) <(git show
upstream/read-set-budgets:<path>)`), yielding: 13 keep-ours (fork's version is a strict superset — later,
more advanced, or already proven by its own tests), 3 take-theirs (`ITERATIVE_METHODOLOGY.md`'s pointer
sentence, plus two add/add test modules — `tools/test_context_budget.py`'s D9-scrubbed wording and
`tools/test_methodology_trim.py`'s portable synthetic fixtures, a previously-unflagged case of the same
back-port pattern D9 already named for the other module), 2 decided on their own terms (`.context-budget.json`
stays fork's own per the ratified D11; `docs/tutorials/T8_keeping_current.md`'s stale *"24 vs. 25
distributed files"* claim is recomputed to the real, measured **27**, not picked), and the two ledgers
(`CHANGELOG.md`, `HANDOFFS.md`) interleaved by date per the convention their own front matter documents,
the same rule five prior resync merges (`aa378ab` et al.) already established. **A correction to the
ratified `pr4-read-set-budgets-plan.md`'s own D11 arithmetic, recorded rather than edited into that closed
document:** D11 said PR 4 adds *"two more, 19 in all"* beyond a measured 17-path baseline against
`cea3068`; PR 4 actually adds a third — `.gitignore` (its own §3.6) — making the true total 20, exactly
what today's measurement shows.

**TWO OF THE PLAN'S OWN FIRST-DRAFT CLAIMS WERE CAUGHT AND CORRECTED BEFORE COMMIT, BOTH RECORDED IN THE
PLAN RATHER THAN SILENTLY FIXED.** (1) The auto-merged-set breakdown first guessed *"76 paths exist only
on fork `main`, 14 exist on both sides"* without checking which side actually has each path; tested
directly (`git cat-file -e upstream/read-set-budgets:<path>` per path), the true split is **86/4**. (2)
A first draft predicted `bin/tests.sh`'s pre-existing Test 9 failure would flip to passing once this
merge lands, reasoning that the merge supplies the 3 manifest sources Test 9 finds missing; reading
`bin/sync`'s actual `--source=github` fetch call (`gh api repos/KJ5HST/methodology/contents/<src>`, no
`ref=`) shows it queries `upstream/main`'s live GitHub default branch, which this fork-internal merge
never touches — Test 9 stays red for its pre-existing reason until `read-set-budgets` reaches
`upstream/main`, the maintainer's action. Both corrections are the same "run it, don't predict it"
discipline this repo's Learning #50 already names, applied to this session's own drafting rather than to
a predecessor's.

**Commits this session:** `d040bd0` (claim, from the earlier, correctly-halted S150 attempt);
`75f1cf6` `chore(history)` (`--no-verify`, the dashboard series Phase 0 dirtied then); this close-out
(the plan document, this ledger entry, the completed receipt). **Runtime smoke, bare, at close-out
with the plan committed:** `bash bin/tests.sh` → **304 passed, 1 failed, 0 skipped, exit 1** — unchanged
from the Phase 0 baseline taken before writing anything (Test 9, pre-existing, expected until
`read-set-budgets` reaches `upstream/main`). Checkers, each bare: `check-handoff` **0** (22 receipts, the
newest complete), `--all` **0** (22 receipts), `check-links` **0** (105 links / 23 files),
`check-learnings` **0** (53 rows, contiguous 1..53 with `#14` a documented reserved gap, 0 over 1,500 B).
`CHANGELOG.md` is 233,769 B and `methodology_trim.py --check` still `FIRES` (196,608 B Class A threshold)
— pre-existing, flagged by S149, not this session's to act on (a separate deliverable).

### 2026-09-04 · [ad hoc] S150 — claim: plan the merge of `upstream/read-set-budgets` (`598c459`) into fork `main`

**Authorization:** the operator's *"in the next session make a plan to complete the merge as you have
described"* (2026-09-04), after the S149 assessment of GitHub's *Sync fork* dialog (unusable here: it
targets upstream `main`, which lacks the four PRs, and the ledgers conflict on every sync). **The ONE
deliverable is the plan document** — `docs/planning/upstream-read-set-budgets-merge-plan.md`: the
evidence-based inventory of every path the merge touches (20 conflicting, plus the auto-merged set),
a resolution rule per path with its verification command, the DONE criteria, the surface, and the
session boundary — committed and self-reviewed. **The merge itself is NOT this session's work** (Planning
Sessions: the plan is the deliverable, not a preamble). No push, no upstream action.

**Reconciled at claim:** S149's receipt `commit:` slot named its close-out by description; this commit
names it — `10d5268`. Both ledger frontiers stood at `10d5268` at Phase 0 (gap 0); no backfill is owed.
**A non-commit action to record, done by the operator, not a session:** PR #79 was MERGED on
`KJ5HST/methodology` at `2026-09-04T01:24:30Z` by rmsharp — merge commit `598c459` on `read-set-budgets`,
parents `cea3068` + `cf15489`, tree `c857734` = the head's; `read-set-budgets` is still not in upstream
`main` (`512c2ed`). The PR 4 plan's Phase D record and the body file's header are updated from those
server reads in the next commit, before the planning work.

**Ledger:** `CHANGELOG: pending` — set at claim; recorded at Phase 3F.

### 2026-09-03 · [ad hoc] S149 close-out — Phase C DONE: `pr4/context-budget-gate` (`cf15489`) pushed to `origin` and OPEN upstream as PR #79 against `read-set-budgets`, NOT merged

**Phase 3D/3F.** Deliverable: Phase C of
[`docs/planning/pr4-read-set-budgets-plan.md`](docs/planning/pr4-read-set-budgets-plan.md) (`:703`), on the
operator's *"1"* (item 1 of the S148 close-out's list), claimed in this ledger before acting. **Two
outward-facing actions, both authorized, both read back:** (1) `git push origin pr4/context-budget-gate`
— a new branch on `rmsharp/methodology`, read back `cf15489` / tree `c857734` (re-checked against the
local branch before the push); (2) `gh pr create --repo KJ5HST/methodology --base read-set-budgets --head
rmsharp:pr4/context-budget-gate` with the body file's *Title* and its Body plus the two sections after
the divider (14,003 B; grep for fork-internal identifiers empty) →
**[PR #79](https://github.com/KJ5HST/methodology/pull/79)**, created `2026-09-04T00:59:58Z` (a 2026-09-03
local session; dragon 14). Read back from the server: `state OPEN`, base `read-set-budgets`, `headRefOid
cf15489…` = the local branch, `mergeable MERGEABLE`, `mergeStateStatus CLEAN` (UNKNOWN on the first read,
seconds after creation), `changedFiles 7` = the §3 list exactly, `+2,320 / −98`, two commits (`8df8faa`,
`cf15489`), body 14,004 B with the eight headings sent, not a draft, `reviewDecision` empty.
`upstream/main` `512c2ed` and `upstream/read-set-budgets` `cea3068` untouched; `origin/main` untouched
(`143ff2b`, 2026-08-15). **Not done, deliberately:** no merge (Phase D keeps its own go-ahead), no tag, no
release, no comment on the PR, no push of `main`. Records: the body file's status header (`:3`), the plan's
status line and Phase C record.

**Commits this session, all recorded here:** `974db79` (claim; S148's `commit:` slot reconciled to
`9a49f09`); `6e4c56b` `chore(history)` (`--no-verify`, the dashboard series Phase 0 dirtied); this
close-out (the body header, the plan's status line and Phase C record, both ledgers).

**Runtime smoke in this worktree, at close-out with every edit in place:** `bash bin/tests.sh` → **304 passed / 1 failed / 0 skipped, exit 1 — S148's close-out summary, to the row**
(the one failure Test 9, pre-existing — and still expected to stay red until `read-set-budgets` reaches
`main`; the run mutated and restored the ledgers as Test 34 does). Checkers, each bare: `check-handoff` **0** (21 receipts, the newest complete, 0 over 12,288 B), `--all` **0** (21 receipts), `check-links` **0** (105 links / 23 files), `check-learnings` **0** (53 rows, 0 over 1,500 B).

### 2026-09-03 · [ad hoc] S149 — claim: Phase C of the PR 4 plan — push `pr4/context-budget-gate` (`cf15489`) to `origin` and open the PR against `read-set-budgets`

**Authorization:** the operator's *"1"*, answering the S148 close-out report's numbered list, whose item 1
was Phase C — the explicit, per-action go-ahead `CLAUDE.md` requires for an outward-facing action on
`KJ5HST/methodology`. Recorded here **before** acting, because a push and a PR leave no commit in this
fork ([`docs/planning/pr4-read-set-budgets-plan.md`](docs/planning/pr4-read-set-budgets-plan.md) §5 Phase
C, `:703`). **The ONE deliverable: the branch on `origin` and the PR open, read back from the server** —
`git rev-parse pr4/context-budget-gate^{tree}` still `c857734`; push; `origin/pr4/context-budget-gate`'s
tree read back equal; `gh pr create --repo KJ5HST/methodology --base read-set-budgets` with the body
file's *Title* and *Body*; `gh pr view` read back (state OPEN, base `read-set-budgets`, `headRefOid` =
`cf15489`, mergeable, the seven files); `upstream/main` untouched; the body file's status header updated
from those reads. **No merge (Phase D keeps its own go-ahead), no tag, no release, no comment, no push of
`main`.**

**Reconciled at claim:** S148's receipt `commit:` slot named its close-out by description; this commit
names it — `9a49f09`. Both ledger frontiers stood at `9a49f09` at Phase 0 (gap 0); no backfill is owed.

**Ledger:** `CHANGELOG: pending` — set at claim; recorded at Phase 3F.

### 2026-09-03 · [ad hoc] S148 close-out — the PR 4 fix-round DONE: `pr4/context-budget-gate` REBUILT as `cf15489` on `cea3068`, re-verified, NOT pushed

**Phase 3D/3F.** Deliverable: the six-row fix-round from S147's self-review, applied, and the branch
rebuilt and re-measured — item (1) of S147's handoff, the operator's words. Head **`cf15489`** (tree
`c857734`), two commits on `cea3068` — `8df8faa` commit (1), `cf15489` commit (2) — built in a clean
clone by the §8 R1 recipe (fixtures `020ba3f 7a71df0 e02881a e5cdc66` unreachable, no `docs/archive/`),
each committed **through** upstream's `.githooks/pre-commit` with `core.hooksPath` set, and fetched into
this fork as the local ref `pr4/context-budget-gate`. The two earlier heads are kept as refs, not
branches: S147's `f3a4b6d` and this session's `46089f1` and `c6577f2` (the two the review lenses read),
under `refs/archive/pr4-context-budget-gate-<sha>`. **Nothing pushed, nothing opened; Phases C and D
still need their own go-aheads.** Records: the body file's header and its *fix-round* section
([`docs/planning/pr4-read-set-budgets-body.md`](docs/planning/pr4-read-set-budgets-body.md)), the plan's
§5 Phase B record, §3.1 heading and DONE criterion re-stated with the new blob id.

**Commits this session, all recorded here:** `1086f5c` (claim; S147's `commit:` slot reconciled to
`ae5ff8d`); `6887b67` `chore(history)` (`--no-verify`, the dashboard series Phase 0 dirtied); `22c6cf0`
and `544cfb0`, the two fork-side passes (one entry below, extended for the second); this close-out
(Learning #54, the plan and body records, both ledgers).

**WHAT THE SIX ROWS BECAME.** Rows 2 and 3's fork halves first (`22c6cf0`: the tool's five fork-authored
sites plus the test module's four, the candidate config's two sentences), then the branch: row 1
(`tools/test_context_budget.py:9`, `:13` → the unnumbered upstream block and `bin/tests.sh:237-244`),
row 4 (`.gitignore:5`, later `:8`), row 5 (the two PRs by absolute URL, and *"eight fork commits (seven
that went through the fork's own review rounds, plus one comment-only reword made for this port)"*),
row 6 (*"every git fixture"*, the seed's on-demand note named, *"six lines"* for *"four"*, the tool's
size 73,040 B). **The one site left alone, on evidence:** `starter-kit/context_budget.py:409` *"learning
#22 / #26a"* is upstream's own 1.0.0 text — `git blame` → `df6a991` (KJ5HST, 2026-08-08), present in blob
`be2721a5` — so S147's review had attributed the maintainer's own citation to the port; Learning #54.

**THE REVIEW LENS RE-RAN, TWICE.** A maintainer's-eye reviewer read the first rebuild (`46089f1`) in its
own R1 clone and returned **fourteen** items (3 HIGH, 5 MEDIUM, 6 LOW), every one re-derived by hand:
repaired in `544cfb0` and the third build — `tools/test_context_budget.py:214` (a fork commit `7603f10`
attributed to *"this framework's own repository"*), `:404` (*"PHASE B"* in capitals, missed by a
case-sensitive grep), the ledger entry's 73,014 B (stale by this session's own +26 B), the tool's `:57` /
`:1157` and the seed's *"the project that authors this tool"* (a fork measurement stated as the tool's
home's), the bare `#76`/`#78` (the ledger's own front-matter rule wants absolute URLs), `.gitignore:8`
(*"must survive a fresh clone"* — untracked there), the *"seven reviewed"* wording; kept with the reason
recorded in the body file — `:683` names the fork so it resolves, *"five values"* is D10 (five distinct,
seven sites), the config's sizes are scoped to `cea3068`, `:71` is correct on the tree; two follow-ons
disclosed in the PR body rather than built — `bin/check-learnings:87-89`'s comment goes stale when commit
(2) lands (an eighth file, outside the ratified seven) and the pre-existing `:341` `ResourceWarning`.
Then a second, delta lens on the frozen third build `c6577f2`: all fourteen dispositions confirmed, seven more items — two false provenance sentences the rebuild itself had written (*"eight commits … one reword"* where it is nine and two; *"every intermediate fails"* where the last two pass), a `.gitignore` subject and a bullet naming only one of the two histories, all four repaired in the fourth build `cf15489`; the module's colliding `D1`–`D5` labels, the 20,193/20,194 rounding pair and the seed naming the fork disclosed in the PR body. The lens's verdict, *"not yet — fix F1 and F2 first"*, was acted on; no lens ran on the fourth build's four text edits, which were checked by grep against the reviewer's own commands.

**EVERY DONE ITEM RE-MEASURED ON THE FOURTH BUILD AND MATCHED:** blob `d91677b5`, mode 100755, equal to
fork `main`'s; the module differs from `main:tools/test_context_budget.py` in exactly six lines (8, 9,
13, 288, 561, 613); unit → exit 0, `Ran 116 … OK (skipped=2)`; `--selftest` → 0, 52 / 0; bare → exit 2,
49 lines, 0 *defect*, six findings, `CHANGELOG.md` **97,257 B** (91,365 + 5,892; ≈39,416 tok); `--json`
`config_defects: []`; the 13-case matrix (2 0 2 2 0 2 0 2 0 0 0 0 0; case 12's bare run 2 with
`instrument-failed`); by hand — commit (1) vs `cea3068` no config → **3**; with the candidate in the
worktree → **2** (`91,365 -> 95,557 B`); commit (2) vs commit (1) → **2** (`95,557 -> 97,257 B`); bullet
unstaged → **0**; suites on fresh clones **114/1** (control) vs **115/1** (head) vs **114/2** (commit (1))
— 115 shared rows, one added, zero flips, every failure Test 9; checkers 0/0/0/0; seven files, 2,320 /
98; the identifier regex over added lines and both messages empty; a case-insensitive sweep of the added
lines for the residue class empty; PROPOSAL 8; config `cmp`-identical to the amended candidate; `git
status --porcelain` empty after deleting the history file.

**Runtime smoke in this worktree, at close-out with every edit in place:** `bash bin/tests.sh` → **304 passed / 1 failed / 0 skipped, exit 1 — S147's close-out summary, to the row**
(the one failure Test 9, pre-existing; the run mutated and restored the ledgers as Test 34 does).
Checkers, each bare: `check-handoff` **0** (20 receipts, the newest complete, 0 over 12,288 B), `--all` **0** (20 receipts), `check-links` **0** (105 links / 23 files), `check-learnings` **0** (53 rows, 0 over 1,500 B).

**Two harness gotchas, recorded for the next builder:** in `zsh` an unquoted `$CB` holding `python3
starter-kit/context_budget.py` does not word-split, so every by-hand and matrix case came back **127**
(*command not found*) on the first pass — eighteen identical exits no case is specified to produce; use a
shell function. And a residue grep must be case-insensitive: *"PHASE B"* survived a `Phase B` sweep.

### 2026-09-03 · [ad hoc] S148 — reword the fork-relative comments in `context_budget.py`, its test module and the PR 4 candidate config (the fix-round's fork-side half: rows 2 and 3)

**The fork-side prerequisite of the fix-round, committed on `main` BEFORE the branch is rebuilt so the
ported tool blob stays byte-identical to fork `main` (the shape row 2 of the decision table prescribes).**
Comment-only, behaviour unchanged, line counts unchanged in both Python files (so the plan's §3.1 symbol
line numbers still hold), every edited line ≤ 99 columns. `starter-kit/context_budget.py` blob
`c5ff15e5` → **`0b103baf`** (73,014 → 73,040 B): `:289-290` (*"this repository's own
SESSION_RUNNER.md is 54,363 B"* → the authoring fork's, which it was), `:675` and `:1204` (*"Phase B"*
→ the date, 2026-08-26), `:683` (the planning-doc pointer now names `rmsharp/methodology`), `:733`
(*"this repository's own history"* → the authoring repository's). `tools/test_context_budget.py` blob
`a671113` → **`f6c94d85`**: `:417`, `:424` (*"Phase B"* → the date), `:484` (*"Measured on this repo"*
→ the authoring fork), `:546` (*"wsfct"* → one adopter) — the folds the table's *Kept as ratified*
paragraph assigns to row 2, plus `:484`, found by this session's grep for the same class. **One row-2
site is NOT fork residue and is left alone:** `:409` *"learning #22 / #26a"* is upstream's own 1.0.0
text — `git blame` → `df6a991` (KJ5HST, 2026-08-08), present in blob `be2721a5` — so the review had
attributed the maintainer's own citation to the port; scrubbing it would have edited his line under the
name of removing ours. Row 3, fork side: `docs/planning/pr4-candidate.context-budget.json` (17,934 →
17,893 B) — `read-set._` no longer cites `upstream-read-set-pr-plan.md`, a file the maintainer cannot
open (the sentence now says the seed's own `CLAUDE.md.max_bytes` is the candidate and that the
authoring fork's design names it), and the `CLAUDE.md` `_` key's *"Accepted as is (ratified
2026-09-03)"* becomes *"Left as is, deliberately"*. Verified in this worktree after the edits:
`python3 tools/test_context_budget.py` → exit 0, `Ran 116 … OK` (both `TestFitGateEndToEnd` rows run
here); `--selftest` → exit 0, 52 PASS / 0 FAIL, the relabelled check at `:1204` among them; the
candidate parses. The `"Phase B"` vocabulary upstream's trimmer (#77) still carries in nine comment
sites is untouched, as D9 left the trimmer's S-numbers — a consistency choice, made visibly.

**Second pass, after the review lens ran on the rebuilt branch (`46089f1`) and found the same class at
four more sites, each re-derived by hand before it was touched:** `starter-kit/context_budget.py` `:57`
(*"the repo that authors this tool"* → *"the authoring fork of this tool"*) and `:1157` (*"this
framework's own repository"* → the same), blob `0b103baf` → **`d91677b5`** (73,040 B, size and line count
unchanged); `tools/test_context_budget.py` `:214` (*"this framework's own repository: commit 7603f10"* →
*"the authoring fork: its commit 7603f10"* — a fork sha stated as this repository's) and `:404` (*"PHASE
B"* in capitals: the first pass's grep was case-sensitive), blob `f6c94d85` → **`04d6aaf6`**; the seed
`starter-kit/context-budget.json` `_read_cap_tokens` (*"On the project that authors this tool"* → the
fork where 1.2.0 was developed, named), 5,766 B. Same verification in this worktree: unit 116 OK,
`--selftest` 52 / 0, and a case-insensitive sweep of all three files for the class is empty.

### 2026-09-03 · [ad hoc] S148 — claim: the six-row fix-round on `pr4/context-budget-gate` (item (1) of S147's handoff)

**Authorization:** the operator's *"Item (1) of S147's handoff"*, given after the Phase 0 report: the
six-row decision table at [`docs/planning/pr4-read-set-budgets-body.md`](docs/planning/pr4-read-set-budgets-body.md)
`:23`, the fix-round S147's self-review recommended before Phase C. **The rewritten, re-measured, still
unpushed branch is the ONE deliverable:** row 2 first, as a fork commit on `main` (the tool's four
fork-relative comment sites), then the branch rebuilt on `cea3068` by the plan's §8 R1 recipe with rows
1, 3, 4, 5 and 6 applied inside it (row 3 also amends `pr4-candidate.context-budget.json`) and the
fork-vocabulary folds the table's *Kept as ratified* paragraph assigns to rows 2 and 3; every DONE-list
figure re-measured on the fresh tree; one review lens re-run; the plan's `c5ff15e5` criterion re-stated
with the new blob id. **No push, no PR, no `--calibrate`, no `install-hook` at the clone root, no
`bin/tests.sh` in this worktree, nothing outward-facing.** Phases C and D each keep their own go-ahead.

**Reconciled at claim:** S147's receipt `commit:` slot named its close-out by description; this commit
names it — `ae5ff8d`. Both ledger frontiers stood at `ae5ff8d` at Phase 0 (`git rev-list --count
--no-merges ae5ff8d..HEAD` → 0), so no backfill is owed and none is written.

**Ledger:** `CHANGELOG: pending` — set at claim; recorded at Phase 3F.

### 2026-09-03 · [ad hoc] S147 close-out — PR 4 BUILT (Phase B): `pr4/context-budget-gate` = `f3a4b6d` on `cea3068`, verified, NOT pushed

**Phase 3D/3F.** Deliverable: the built, verified, unpushed branch — Phase B of
[`docs/planning/pr4-read-set-budgets-plan.md`](docs/planning/pr4-read-set-budgets-plan.md) §5, executed as
ratified (D1–D11). Head `f3a4b6d` (tree `7541e3ee`), two commits on `cea3068` — `28406ce`
`feat(starter-kit): …` (the tool at blob `c5ff15e5`, the test module scrubbed on exactly four lines, the
9-line `bin/tests.sh` wiring, the seed's +6, the D8 ledger entry) and `f3a4b6d` `chore(budget): …` (the
root config byte-identical to the candidate, the seven `.gitignore` comment lines, one ledger bullet) —
built in a clean clone made only by the §8 R1 recipe (fixtures `020ba3f 7a71df0 e02881a e5cdc66` proved
unreachable, no `docs/archive/`), each commit **through** upstream's `.githooks/pre-commit` with
`core.hooksPath` set in the clone, and fetched into this fork as a **local ref only**.
`upstream/read-set-budgets` re-read at `cea3068` and the three pins re-read before the config was copied.
Body file: [`docs/planning/pr4-read-set-budgets-body.md`](docs/planning/pr4-read-set-budgets-body.md).
**Nothing pushed, nothing opened; Phases C and D still need their own go-aheads.**

**Commits this session, all recorded here:** `bfba325` (claim; also reconciled S146's `commit:` slot to
`a05e23a` + `a5fa2ae`); `8dc31e2` `chore(history)` for the two `.jsonl` series Phase 0 dirtied
(`--no-verify`, recorded by this line, committed *before* this close-out so nothing sits above the
frontier); this close-out (Learning #53, the plan's Phase B record, the body file, both ledgers).

**EVERY DONE-LIST FIGURE, TAKEN FROM THE TREE THAT WOULD BE PUSHED:** blob `c5ff15e5`, mode 100755; the
test module differs from `main:tools/test_context_budget.py` in exactly the four D9 lines (8, 288, 561,
613 — widths 95/97/97/97 under the module's 99-column norm); `python3 tools/test_context_budget.py` →
exit 0, `Ran 116 … OK (skipped=2)`; `--selftest` → 0, 52 PASS / 0 FAIL; the bare run → exit 2, 49 lines,
0 *defect*, six findings, `CHANGELOG.md` **96,750 B** (91,365 + 5,385 for the entry; ≈39,211 tok);
`--json` `config_defects: []`; the 13-case `--precommit` matrix reproduced (exits 2 0 2 2 0 2 0 2 0 0 0 0 0;
case 12's bare run 2 with `instrument-failed`); **by hand, each commit's index against its parent:
commit (1) vs `cea3068` with no config → exit 3; the same index with the candidate in the worktree → 2
(`91,365 -> 95,079 B`); commit (2) vs commit (1) → 2 (`95,079 -> 96,750 B`), and 0 with its bullet
unstaged** — the exits D4 ratified, measured again on the real commits; `bin/tests.sh` on a pristine
control **114 passed / 1 failed** vs **115 / 1** on a fresh clone of the head — 115 shared rows, exactly
one added (`context budget gate unit tests green`), zero flips, both failures Test 9 — and **114 / 2 at
commit (1) alone** (the wired row is red until the config lands; that commit's message says so);
`check-links` / `check-learnings` / `check-handoff` / `--all` 0/0/0/0; `git status --porcelain` empty
after deleting the history file; `git diff --stat cea3068 f3a4b6d` exactly seven files (2,315 / 98); the
identifier regex over the diff's added lines and over both commit messages prints nothing;
`grep -c PROPOSAL .context-budget.json` 8; the config `cmp`-identical to the candidate.

**THE FIX-ROUND DISCIPLINE RAN: two independent read-only reviewers on the frozen branch, each in its
own clone.** The plan-compliance lens re-derived every DONE item — all MET, no departures, three cosmetic
observations. The maintainer's-eye lens returned **twelve** items (3 HIGH, 4 MEDIUM, 5 LOW), and every one
re-derives by hand: the shipped tool blob says *"this repository's own SESSION_RUNNER.md is 54,363 B"*
(52,195 B on `cea3068`) and cites a fork planning file at `:683`; the test module still says *"Test 35"*
and *"bin/tests.sh:248-251"* at `:9`/`:13`, outside D9's four regex hits; the config's `read-set` `_` key
cites `upstream-read-set-pr-plan.md`, absent upstream; the ported `.gitignore` comment says a file *"is
tracked"* that upstream does not track; the ledger entry says *"PRs 1 and 3"* where upstream knows #76
and #78; two overstatements of my own in commit (1)'s message. **None repaired — each sits inside an
artifact the plan ratified (D9's four lines, Appendix A verbatim, the `c5ff15e5` blob, the §3.6 lines) —
so the six-row decision table, with proposed wording per row, is in the body file's header, and the
recommendation is a fix-round before Phase C.** The remaining items stand as ratified for the reasons the
table gives (the two machine-dependent tests, the fork-measured densities, the PROPOSAL count, the
rounding, the trailers).

**Learning #53** appended to `starter-kit/FRAMEWORK_LEARNINGS.md`: a per-clone hook is off in a fresh
clone of the target; enable it before the first commit, and let one refusal prove it binds.

**Adopter impact:** none yet — nothing has left this machine. When PR 4 merges and adopters sync, the two
changes the body discloses apply (bytes-not-lines rows when nothing fires; a derived token ceiling above
73,252 B). **Nothing outward-facing.**

**Model:** Claude Fable 5.1.

### 2026-09-03 · [ad hoc] S147 — claim: Phase B of the PR 4 plan — build `pr4/context-budget-gate` on `cea3068`, verify, do not push

**Authorization:** the operator's *"Item (1) of S146's handoff"*, given after the Phase 0 report:
[`docs/planning/pr4-read-set-budgets-plan.md`](docs/planning/pr4-read-set-budgets-plan.md) §5 Phase B
(`:599`), ratified at S146 (the §4 record, `:414`; D1–D11). **The built, verified, unpushed branch is the
ONE deliverable** — a clean clone made only by the §8 R1 recipe, fixture unreachability proved per clone;
two commits, each co-staging a `CHANGELOG.md` line (D4 as ratified); every DONE-list figure taken from the
tree that would be pushed; `docs/planning/pr4-read-set-budgets-body.md` written in the series' precedent.
**No push, no PR, no `--calibrate`, no `install-hook` at the clone root, no `bin/tests.sh` in this
worktree, nothing outward-facing.** Phases C and D each keep their own go-ahead.

**Reconciled at claim:** S146's receipt `commit:` slot named its last two commits by description; this
commit names them — `a05e23a` (close-out) and `a5fa2ae` (`chore(history)`, `--no-verify`). `a5fa2ae` was
the one commit above both ledger frontiers at Phase 0 (`git rev-list --count --no-merges a05e23a..HEAD`
→ 1); S146's close-out entry already records it, so no backfill entry is owed and none is written.

**Ledger:** `CHANGELOG: pending` — set at claim; recorded at Phase 3F.

### 2026-09-03 · [ad hoc] S146 close-out — the PR 4 plan RATIFIED (D1–D11), after the second review round ran

**Phase 3D/3F.** Deliverable: the ratified plan —
[`docs/planning/pr4-read-set-budgets-plan.md`](docs/planning/pr4-read-set-budgets-plan.md) (third draft,
91,883 B) and [`pr4-candidate.context-budget.json`](docs/planning/pr4-candidate.context-budget.json)
(17,934 B). **Status line and §4 now carry the ratification record: D1–D11 stand — D1–D10 as
recommended, D4 reshaped and D11 added on the second review's findings. Phase B is authorized as the
next session's single deliverable; Phases C and D are not.** Nothing built, pushed, or opened.

**Commits this session, all recorded here:** `a78e404` (claim; also reconciled S145's `commit:` slot);
`98c6e10` `[WIP]` third draft, frozen for self-review, and `c2b3106` `[WIP]` its repairs, frozen again for
one verifier — both committed `--no-verify`, both bypasses recorded by this line; this close-out; and a `chore(history)` for the two `.jsonl` series Phase 0 dirtied (`--no-verify`, recorded here).

**THE RATIFICATION, IN THE ORDER IT HAPPENED.** Item (1) of S145's `next_steps` was the operator's pick
(*"1"*). The ten recommendations and their alternatives were tabled as one question; the answer was *"All
ten as recommended."* Before recording it, the second adversarial review round S145 could not run (usage
limit) was run against the frozen close-out tree `67982cc`: **eight read-only slices, then one independent
skeptic per refutation and per HIGH/MEDIUM finding — 45 agents, 0 failed, 0 empty.** 120 claims
re-derived: **102 confirmed, 17 refuted, 1 unverifiable**; of round 1's 59 items **53 fixed, 5 partial,
1 not**; **19 new findings (1 HIGH, 9 MEDIUM, 9 LOW)**; **36 of 37 adjudications stand, 1 overturned.**
Four facts the repairs rest on were re-derived by hand rather than taken from an agent: upstream's
`.githooks/pre-commit` refuses a content commit without `CHANGELOG.md` co-staged; the fork carries **ten**
dashboard version labels above `2.10.7` (one agent said 9, another 10 — the enumeration settled it);
`claude --version` = 2.1.259; the two machine-dependent tests run and pass here (`Ran 116 … OK`). Four
items reopened a decision and went back to the operator as separate questions, each answered as
recommended: **D4** — the two-commit order's rationale was refuted (HIGH: by hand the gate exits **3** on
commit 1, no config yet, and would refuse commit 2's own ledger line; upstream's hook wants a ledger line
on every commit) → two commits, **each carrying a `CHANGELOG.md` line**; **D11**, new — the fork keeps its
own root config after merge; **D2**'s token arm — `CLAUDE.md` carries a silently clamped derived ceiling
(59,168 / 2.27 = 26,065 → 25,000; judged at 2.93 → 20,193, ok) → accept and document; **D6**'s residue —
the #77 ledger backfill is **not** in PR 4, and no frontier-based reconcile can ever surface it
(`56997af` sits below the frontier `2c30d0f`).

**WHAT THE REPAIRS CHANGED, BESIDES THE DECISIONS.** The zsh dragon said the mangled `$c:path` "silently
emptied" an enumeration — it is loud on stderr and `<sha>/` on stdout; dragon 11 blamed `grep -c` for a
SIGPIPE hazard that belongs to `grep -q`; §2.2's Lines column mixed `wc -l` with the tool's count (which
is one higher on every LF-terminated file); the adopter flip threshold is **73,253 B**, not "≥ 73,250"
(`int()` truncates, the compare is strict); D8's date rule was UTC where the ledger's convention is the
author's local date, its bullet shape was invented, and its identifier grep was unsatisfiable as written
(`CHANGELOG.md` and `bin/tests.sh` already carry 65 and 11 hits on `cea3068` → grep the added lines of the
diff); D9's "35 / 5" were line counts under a narrower regex (50 / 28 matches by D8's); D10's "three plus
a fourth" is four, plus two inherited thresholds now labelled (`warn_bytes` 51,000 is inert while the
class is over; `max_lines` 200); `class_totals()` is not called from `precommit()`; the dashboard cite was
`:508-523`, not `:498-508`; Phase A gained a runnable verification; Phase C regained the post-push
read-back the round-1 repair had dropped; the `calibrate()` failure causes and the FitGate diagnosis
command were wrong in detail; the PR body now says the bare run prints **five** red lines on day one,
that 2.27 is a constant not a key, what the trimmer does on its first `--write`, and that the gate this
PR ships would refuse the PR that ships it. Config: `_calibrate_against` added; `_bytes_per_token` now
names `CLAUDE.md` as the one consumer of the fallback; `_fixed_harness_tokens` says the tool reads it
nowhere; the `## Versioning` `why` no longer attributes a rule to a `CLAUDE.md` that does not state it
upstream (twelve `CHANGELOG.md` links and one fixture do the work).

**FIX-ROUND DISCIPLINE.** The third draft was frozen at `98c6e10` and given a four-lens self-review
(the S146 edits re-derived; a whole-plan contradiction sweep; the config prose run and read; the PR body
as the maintainer) with one skeptic per refutation — 17 agents, 4 lenses + 13 skeptics: 41 claims (36 confirmed, 5 refuted), 20 findings (2 HIGH, 6 MEDIUM, 12 LOW), all 13
adjudications standing — every one a defect in my own S146 edits, repaired in a third pass (`c2b3106`), whose 26 added
claims one more independent verifier then re-derived: 22 confirmed, 2 refuted (both in D11's merge arithmetic: 17
base conflicts, not 18, the draft having counted `merge-tree`'s OID line; PR 4's share two, not one), 2 unverifiable
from the tree — repaired in this close-out commit.

**Learnings #51 and #52** appended to `starter-kit/FRAMEWORK_LEARNINGS.md`: frontier-based reconcile is
blind to an omission a later ledger commit has buried; sequence commits around the check that actually
runs on the target, not the check the PR ships.

**Adopter impact:** none — fork-only planning documents and a canonical-only Learnings table. **Nothing
outward-facing.** The plan is 91,883 B and no longer fits one Read; a build session reads §4's
record, §5 Phase B, §3.3 and §8, not the whole file.

**Model:** Claude Fable 5.1.

### 2026-09-03 · [ad hoc] S146 — claim: ratification of the PR 4 plan's decisions D1–D10

**Authorization:** the operator's *"1"*, given after the Phase 0 report, selecting item (1) of S145's
`next_steps`: *"the operator ratifies or amends D1–D10"* (`docs/planning/pr4-read-set-budgets-plan.md`
§4, `:375-455`). **The ratified plan is the ONE deliverable** — each of the ten decisions answered by
the operator and recorded in the plan's status line and §4, in the shape
`docs/planning/read-cap-phase-c-plan.md:3` set at S115. Verification in service of it: the second
adversarial review round S145 could not run (every agent hit the usage limit) runs first, against the
frozen close-out tree `67982cc`, so the operator ratifies on checked premises. **No Phase B build, no
push, no PR, nothing outward-facing.** Phase B remains its own session; Phases C and D each keep their
own go-ahead.

**Ledger:** `CHANGELOG: pending` — set at claim; recorded at Phase 3F.

### 2026-09-03 · [ad hoc] S145 close-out — the PR 4 plan, delivered and adversarially reviewed

**Phase 3D/3F.** Deliverable: [`docs/planning/pr4-read-set-budgets-plan.md`](docs/planning/pr4-read-set-budgets-plan.md)
(67,657 B) and its companion [`pr4-candidate.context-budget.json`](docs/planning/pr4-candidate.context-budget.json)
(14,200 B) — the plan for the fourth and last read-set-budget PR, porting `starter-kit/context_budget.py`
(fork blob `c5ff15e5`, 73,014 B) and everything coupled to it onto `read-set-budgets` at `cea3068`.
**Planned, not built; nothing pushed, nothing opened.** Session began 2026-09-02 local; this entry is
dated by its commit.

**Commits this session, all recorded here:** `209dd51` (claim); `5394079` `[WIP]` draft 1, frozen for
review, committed `--no-verify`; `29054c7` `[WIP]` draft 2 after the review, `--no-verify`; `e13ceda`
`chore(history)` the two append-only `.jsonl` series dirtied by Phase 0, `--no-verify`; and this
close-out. The three bypasses are each recorded by this line, which is what the bypass rule requires.

**WHAT THE PLAN ESTABLISHED, MEASURED IN CLEAN CLONES OF `cea3068`.** (1) The file port is clean by
construction: upstream's blob `be2721a5` is the exact ancestor of the fork's seven linear commits; the
end-state patch and all seven per-commit patches apply. (2) The hard part is the coupling: the fork
tool **exits 3 without a root `.context-budget.json`**, upstream has none, and the distributed seed
dropped in as that config reads red for reasons unrelated to the series (`CLAUDE.md` 59,168 B vs
28,000). So PR 4 must ship a canonical root config, and the plan ships a candidate that was **run**:
exit 2 with `(read-set total) 67,581 B / 56,750 B over` — the 10,831 B the series exists to make
visible — 0 config defects, `--selftest` 52/0, the 116-test module OK (2 environment skips), a
13-case `--precommit` matrix (every over-or-pinned file refuses +2 B, every shrink passes, `structure`
is not evaluated by `--precommit`), and `bin/tests.sh` **115 passed / 1 failed against a control of
114 / 1** — 115 shared rows, one added, zero flips. (3) Under the unchanged seed an adopter sees two
changes on sync: read-mandated rows report bytes instead of lines when nothing fires, and a compliant
file at ≥ 73,250 B flips `ok` → `over`, exit 1 → 2 (Probe C4). (4) Ten operator decisions D1–D10 with
recommendations; Phases B–D with DONE, surface, and STOP each.

**THE RECORD CORRECTED.** Six receipts (S136, S140–S144) called this payload *"no clean starting
point"*; S144 glossed it *"the two versions diverged rather than one being a prefix of the other"*.
`git rev-parse` on the two blobs refutes the file half. The tree half is true.

**REVIEW.** Draft 1 was frozen at `5394079` and attacked by eight independent read-only agents — five
refuters over disjoint claim slices, three critique lenses: **97 claims confirmed, 28 refuted, 2
unverifiable, 32 findings.** Every refutation was re-derived before adoption. Refuted in my own work:
three per-commit mis-attributions (read from commit messages instead of path-restricted diffs); a
false *"hand-copied intermediate"* verdict on `vscode_quarto_ext`'s blob, caused by zsh parsing
`$c:path` as a history modifier (it is `6a91660`'s blob, six versions behind fork `main`); the trimmer
named as the declared ledgers' remedy when its trigger is 196,608 B, 3× the ceiling, and does not fire
at 91,365 or 70,182 B; a Probe C fixture holding one of the seed's three files, which could not
exhibit the changes it was published as not finding; the PR's own upstream ledger entry being a
commit the shipped gate refuses, which fixes the commit order (D4); the `FRAMEWORK_LEARNINGS.md`
row dropped on a false reason when its density was measured on the very blob upstream carries and
upstream's `bin/check-learnings:87-89` already cites the derivation (D7 reversed). **A second review
round was launched against `29054c7` and FAILED: all five agents hit the account's session usage
limit and returned null.** The repaired draft is therefore self-verified only (the round-2 claims I
had not re-derived were checked by hand: `calibrate()`'s too-few-sessions path, the upstream ledger
anchors at `:36`/`:144`, the dashboard's `:361`/`:498`/`:508` entries, `install_hook()`'s write path).

**Also at close-out:** reconciled S144's `commit:` answer slot to `710390b` (claim) + `8c701b5`
(close-out), each verified by reading that commit's own copy of the S144 block. Appended **Learning
#50** to `starter-kit/FRAMEWORK_LEARNINGS.md` (a true ratio carrying a false inference through six
receipts); `check-learnings` OK, 49 rows, 0 over 1,500 B.

**VERIFICATION AT CLOSE-OUT.** `bash bin/tests.sh` in this worktree, bare, after both ledger edits:
**304 passed / 1 failed / 0 skipped, exit 1** — the recorded baseline to the row. A first run before
the S144 `commit:` reconcile read 302 / 3 / 0; its two extra failures were that unreconciled slot (the
`L1` row and the 12,288 B edge case whose fixture is built from the live ledger) and both pass in the
second run. The one failure is Test 9, pre-existing. `check-handoff` 0, `--all` 0, `check-links` 0, `check-learnings` 0,
each read bare. **NO OUTWARD-FACING ACTION.** Phases C and D of the plan each require their own
go-ahead; approving the plan is not it.

**Model:** Claude Fable 5.1.

### 2026-09-03 · [ad hoc] The context-budget gate ships — ceilings in tokens, class totals, and the repairs beneath them

- **Change:** `starter-kit/context_budget.py` `1.0.0` → `1.2.0` (29,549 → 73,040 B), shipped as the
  end state of nine fork commits (seven that went through the fork's own review rounds, plus two
  comment-only rewords made for this port) rather than a replay — the tests arrive as one file, and
  every intermediate state of the tool before its reviewed end state fails them. Ceilings may now be declared in **tokens** (`max_tokens`, against `read_cap_tokens`
  25,000 — the number in the Read tool's own refusal message); a whole-read file with only `max_bytes`
  gets a ceiling derived at the 2.27 B/token floor and clamped at the cap; **class totals**
  (`resident`, `read-set`) are summed and gated in the bare run and in `--precommit`;
  `config_defects()` reports a declared `max_tokens` above the cap and a typed class total that
  disagrees with its derivation; `calibrate()` walks first-parent history, compares timezone-aware
  stamps and refuses a fit below R² 0.50 instead of printing noise; the index is sized with
  `git cat-file -s` (the old path was 1 B short on LF, more on CRLF, and raised on non-UTF-8 content);
  the ledger row names the ceiling that fired in its own unit and reports bytes, not lines, when
  nothing fired. Exit codes are unchanged (`0/1/2/3`), and so is the refusal to run at a root with no
  `.context-budget.json` (exit 3).
- **What it buys.** [#76](https://github.com/KJ5HST/methodology/pull/76) and
  [#78](https://github.com/KJ5HST/methodology/pull/78) shed bytes; this one **refuses growth**. On this branch the Phase 0
  mandatory pair is 52,195 + 15,386 = **67,581 B against the 56,750 B one-read cap — over by
  10,831 B, exactly what [#76](https://github.com/KJ5HST/methodology/pull/76)'s table left.** Nothing here shrinks it. Once a root config declares
  the pair, `--precommit` refuses any commit that grows either file and passes any that shrinks one.
- **The tests travel with the tool.** `tools/test_context_budget.py` — 116 tests, canonical-only
  (not in `bin/_manifest.py`, like the trimmer's), every git fixture a scratch repository — plus one
  `bin/tests.sh` row wiring it, immediately after the trimmer's. Until that row `calibrate()`'s
  arithmetic had no test anywhere: the existing `== Test: context_budget.py ==` block covers
  install-hook, sync distribution and the selftest gates, all of which stay green while the fit
  returns noise. Two tests fit this repository's own session transcripts against `CLAUDE.md` and
  **skip**, by design, on a machine without them.
- **The seed follows the tool.** `starter-kit/context-budget.json` gains `read_cap_tokens`, a
  `max_tokens` on each of its two whole-read entries and a note on the on-demand entry saying why it
  gets none (+6 lines) — documentation of keys the new tool reads. It is a seed-once file: no
  adopter's existing config changes on sync.
- **Scanner:** untouched. Both dashboard twins already list `context_budget.py` and
  `.context-budget.json` as framework-installed files and score neither.
- **Verification:** clean clone of `cea3068`, measured at the branch head with the root config in
  place. `python3 tools/test_context_budget.py` — 116 run, OK, 2 skipped; `--selftest` 52 PASS /
  0 FAIL; `bin/tests.sh` **115 passed / 1 failed** against **114 / 1** on the untouched base — one
  row added, zero status flips; the failure on both is Test 9 (`bin/sync --source=github` reads
  `main`, where three manifest sources are absent until this branch merges). `bin/check-links`,
  `bin/check-learnings`, `bin/check-handoff` and `bin/check-handoff --all` each 0.
- **Provenance:** ported from `rmsharp/methodology` `main` — the tool byte-identical (blob
  `d91677b5`), the test module differing in six lines: four where a fork-relative identifier became
  the date of the change, two where a reference to the fork's numbered `bin/tests.sh` block became a
  description of this tree's. The fork's own root config, its measurement history, its dashboard
  series and its ledgers are **deliberately excluded**.
- **This repository declares its own budget** — a root `.context-budget.json`, in a second commit so
  the policy file is reviewable apart from the code. It **pins** `CLAUDE.md` at its arrival size
  (59,168 B: growth refused, shrink passes), **derives** the `read-set` total from the read cap at run
  time (25,000 tok × 2.27 B/tok = 56,750 B) and splits it 41,364 / 15,386 across `SESSION_RUNNER.md`
  / `SAFEGUARDS.md`, so all 10,831 B of debt sits on the file the series wants shrunk, and
  **declares** the two ledgers Phase 0 reads at 65,536 B and 25,000 tokens each and
  `FRAMEWORK_LEARNINGS.md` at 73,728 B — the derivation `bin/check-learnings` already cites this
  file for. Every number's `_` key says how it was derived; five values are marked PROPOSAL, and the
  calibration constants are the seed's (`--calibrate` proposes and writes nothing). Day one: the bare
  run exits 2 with six findings — `SESSION_RUNNER.md` and the pair over by 10,831 B, both ledgers over
  in bytes and in tokens — none of them new. This file is also what turns the wired `bin/tests.sh`
  row green: without a root config the tool exits 3 and the unit module's selftest test fails. The
  gate is **not wired** into `.githooks/pre-commit`: run `--precommit` by hand, and never
  `install-hook` at this root (the config's `_` key says why). Run by hand, this PR's own two commits
  fail it — exit 3 on the first (no config yet), exit 2 on this one (this bullet grows a ledger
  already over its ceiling). `.gitignore` gains the comments explaining why neither measurement history
  (the dashboard's, this tool's) is ignored; this tool's appears on the first bare run and is yours to
  track or not.

### 2026-09-02 · [ad hoc] S145 — claim: planning session for PR 4 (`starter-kit/context_budget.py` to `read-set-budgets`)

**Authorization:** the operator's *"PR 4 planning session"*, given after the Phase 0 report. The
predecessor (S144) scoped PR 4 to its own session and named a planning session as the expected first
step for this shape — a divergent file with no single commit to port — and the operator chose exactly
that. **The plan is the ONE deliverable** (`SESSION_RUNNER.md` Phase 2 §Planning Sessions; FM #18): no
port branch is built, no PR is opened, nothing outward-facing happens this session.

**Scope of the plan:** `starter-kit/context_budget.py` (fork `main` **73,014 B / 1,400 lines**;
`upstream/read-set-budgets` **29,549 B / 674 lines**, byte-identical to `upstream/main`), the seven fork
commits on that path since `14bd88a`, and every file coupled to it — `tools/test_context_budget.py`,
`.context-budget.json`, `bin/tests.sh`, `bin/_manifest.py`, and the prose that names it. Base is
**`cea3068`**, the tip of `read-set-budgets` after PR #78; nothing else is in flight, so no stacking.

**Ledger:** `CHANGELOG: pending` — set at claim; recorded at Phase 3F.

### 2026-09-02 · [ad hoc] S144 — OUTWARD-FACING ACTION TAKEN: **PR [#78](https://github.com/KJ5HST/methodology/pull/78) MERGED** into `read-set-budgets`

**Recorded here because a merge on `KJ5HST/methodology` leaves no commit in this repository.** Phase 0
reconcile is structurally blind to it; the failure-mode-#27 write-gate is the only mechanism that
records it.

**Authorization:** the operator's *"merge PR #78"*, scope narrowed by their own follow-up to the merge
alone. **`gh pr merge` printed NOTHING**, which is neither success nor failure — every property below
was read back from the server afterwards.

| Property | Value |
|---|---|
| #78 | **MERGED** 2026-09-03T02:04:28Z, merge commit **`cea3068`** |
| `read-set-budgets` | `907a696` → **`cea3068`**, parents `[907a696, 2c30d0f]` — a merge commit, matching #76 and #77 |
| `upstream/main` | **untouched at `512c2ed`** |
| Open PRs | **none** |

**The merge was checked for what it DELIVERED, not merely that it succeeded.** `tree(cea3068)` is
**identical** to `tree(2c30d0f)` — the merge added nothing and lost nothing. On `read-set-budgets`
now: `FRAMEWORK_APPARATUS.md` **present at 15,493 B**, `ITERATIVE_METHODOLOGY.md` **55,976 B**,
manifest **27 rows**.

**Three of four PRs in the read-set-budget series are now in.** `main` has received none of them and
is not a target yet.

**Also at close-out:** reconciled S143's `commit:` answer slot to `29331e5` (claim) + `601e432`
(close-out), each verified by reading that commit's own copy of the S143 block — `29331e5` holds it
`status: pending`, `601e432` holds it `status: complete`. **`check-handoff` also caught this receipt's
own `key_files` carrying no `path:line` token**, which the spec requires; fixed with three real
anchors rather than by loosening the sentence. Both read **0** bare afterwards.

### 2026-09-02 · [ad hoc] S144 — claim: merge PR [#78](https://github.com/KJ5HST/methodology/pull/78) into `read-set-budgets`

**Authorization:** the operator's *"merge PR #78"*, with the scope narrowed by their follow-up —
*"we will start PR 4 in the next session"* — so this session's ONE deliverable is the merge. PR 4 is
explicitly **not** in scope.

**Recorded before the action, because a merge on `KJ5HST/methodology` leaves no commit in this
repository.** Phase 0 reconcile cannot see it; the failure-mode-#27 write-gate is the only mechanism
that records it.

**Pre-merge state, read from the server:** `gh pr view 78` -> **OPEN**, base **`read-set-budgets`**,
`mergeable` **MERGEABLE**, `mergeStateStatus` **CLEAN**.

**Method: a merge commit, matching this series' precedent** — `46b56fd` (#76) and `907a696` (#77) each
have two parents. Consistency matters here because PR 4 will be built on whatever tree this creates,
and a squash would give that tree a new sha with no ancestry link to `2c30d0f`.

**Ledger:** `CHANGELOG: pending` — set at claim; recorded at Phase 3F.
### 2026-09-02 · [ad hoc] S143 — OUTWARD-FACING ACTIONS TAKEN: branch pushed, **PR [#78](https://github.com/KJ5HST/methodology/pull/78) OPENED**

**Recorded here because neither action leaves a commit in this repository.** A push to `origin` and a
pull request on `KJ5HST/methodology` are both invisible to Phase 0 reconcile; the failure-mode-#27
write-gate is the only mechanism that records them.

**Authorization:** the operator's *"Open it, 3 commits as-is"*, given after reviewing the pre-flight,
together with the decision that the trimmer-documentation gap becomes **a separate small PR later** —
so it was deliberately not folded in.

**Every property verified from the server, never from the command's own output.** `gh pr create`
prints the same URL whatever base it used; `gh pr view --json baseRefName` is what proves the base,
and `git ls-remote` rather than the push transcript is what proves the push.

| Property | Value |
|---|---|
| State | **OPEN**, `MERGEABLE` |
| Base | **`read-set-budgets`** — the operator's standing requirement that this never target `main` |
| Head | `rmsharp:pr3/apparatus-extraction` = `2c30d0f`, confirmed on `origin` by `git ls-remote` |
| Size | **12 files, +426 / −348**, matching the local measurement exactly |
| Commits | **3** — `786aa24`, `2897983`, `2c30d0f`; no squash, per the operator's choice |
| `upstream/main` | **untouched at `512c2ed`** |
| `read-set-budgets` | still `907a696` — **a pull request does not advance its base** |

**No re-measurement was owed and none was invented.** `tree(907a696)` — the base created when #77
merged — is **identical** to `tree(56997af)`, the tree S142 built and measured PR 3 on. The suite was
therefore not re-run: it would have measured the same tree.

### 2026-09-02 · [ad hoc] S143 — claim: push `pr3/apparatus-extraction` and open PR 3 against `read-set-budgets`

**Authorization:** the operator's *"Open it, 3 commits as-is"*, given after being shown the verified
pre-flight — base advanced, no rebase needed, `merge-tree` clean, three commits.

**Recorded before the action, because neither a push nor a pull request leaves a commit in this
repository.** Phase 0 reconcile is structurally blind to both; the failure-mode-#27 write-gate is the
only mechanism that records them.

**Pre-flight, re-run against the ADVANCED base and read from the server, not from a handoff:**
`gh pr view 77` -> **MERGED** 2026-09-03T01:38:22Z, merge commit `907a696`; `read-set-budgets`
`46b56fd` -> **`907a696`**; `upstream/main` **unchanged at `512c2ed`**. **`tree(907a696)` is identical
to `tree(56997af)`** — the new base is byte-for-byte the tree PR 3 was built and measured on, so
S142's verification carries over rather than needing a re-run. **0 conflicts** (`merge-tree` exit 0),
**3 ahead / 1 behind**, the 1 being the merge commit itself, which changes no content.

**Scope of this session: the push and the PR open, nothing else.** The trimmer-documentation gap
merged by #77 is deliberately NOT folded in — operator chose a separate small PR later.

**Ledger:** `CHANGELOG: pending` — set at claim; recorded at Phase 3F.
### 2026-09-02 · [ad hoc] S142 close-out — PR 3 built and verified on a stacked base; 3 self-inflicted defects found by review and fixed

**Deliverable: branch `pr3/apparatus-extraction` = `2c30d0f`, 3 commits, 12 files, +426/−348.**
**NOT PUSHED. PR 3 NOT OPENED.** Body prepared at `docs/planning/pr3-read-set-budgets-body.md`.

**The assigned base did not exist.** S141 assigned PR 3 "on the ADVANCED base once #77 merges";
`gh pr view 77` says **OPEN**, so `read-set-budgets` is still `46b56fd`, which carries no
`starter-kit/methodology_trim.py` — and PR 3 touches the dashboard twins, whose canonical-only tests
abort with 13 errors without it. Stacked on `pr2/ledger-trimmer` (`56997af`) instead: the exact tree
#77 proposes, so the branch retargets on merge with no rebase.

**Two large blocks `git` offered as conflict resolutions were dropped, not force-fitted.**
`collect_trim_metrics()` (11,834 B, both twins) and README's `## What It Costs` (14,429 B) exist in
the fork and not on this base; the originating commits edited text *inside* each, so a 3-way merge
presented the whole block as an addition. Importing either would have smuggled a fork feature in
under the guise of resolving a comment edit.

**Ported counts were re-derived, and the manifest row SET diffed** — 27 rows / 23 markdown / 19
tracked-markdown, and **0 rows differing either way** against `e02881a`, so the agreement is
structural rather than a coincidence of equal totals.

**Two fork-relative session numbers were removed.** The port would have written *"Extracted at S130"*
into `CLAUDE.md` and *"since S130"* into `HOW_TO_USE.md`. `git grep -oE '\bS[0-9]{1,3}\b' -- '*.md'`
returns **nothing** on this base, so these would have been the first two — each naming a session in a
different repository's counter.

**Verified in `git clone --no-local --single-branch`, never a worktree.** Base 114/1, branch 114/1,
diffed **row for row: 113 shared labels, zero status flips**; the only two differing rows are the
manifest counters, passing on both sides. Dashboard suite **211 OK**, trimmer suite **exit 0**, the
three checkers **0/0/0** read bare. End to end: a real `bin/sync` into a scratch repo lands the
sibling, and in that installed layout **14 references resolve, 7 fragments, 0 unresolved**.

**ADVERSARIAL REVIEW OF MY OWN WORK: 6 lenses → 25 findings → 3 skeptics each → 9 confirmed,
collapsing to 3 real defects, all mine, all fixed (`2c30d0f`) and re-verified.**
(1) I updated the `22 → 23` markdown count only where the patch touched it, leaving `README.md:138`
and `tools/test_methodology_dashboard.py:2853` stale — **while my own ledger entry claimed the counts
had been re-derived from the manifest**, a false claim that had already shipped into a commit.
Classified against the **pre-change** tree: both read 22 and were correct on base, so both were mine.
(2) The distributed stub's *"every point of need above links onward"* enumerated 9 of the 13 sites
that actually link, and contradicted this branch's own ledger entry. Settled by measuring the base —
5 sites already pointed in prose, 8 gained a pointer, 1 had a bare parenthetical converted — so
"nine added" was right and the stub's list was wrong. (3) Fixing (2) edited the file whose size I had
published, so **55,895 → 55,976 B** and every derived figure moved.

**Reported, not fixed — two pre-existing defects with no author here.** Both dashboard twins (`:185`)
and `docs/tutorials/T8_keeping_current.md:183` say *"25 distributed sources/files"* where the manifest
holds **26** on the base and **27** here: wrong before this change and after it.

**Also this session:** `ef51dc9` reconciled S141's `commit:` answer slot to `72b9b54` + `4329d33`
(the checker went 0 → 1 the moment a newer receipt was prepended); `e0adcec` repaired that commit's
missing ledger line; `1949a83` committed the two append-only measurement series.

### 2026-09-02 · [ad hoc] S142 — claim: build PR 3 (apparatus extraction) STACKED on `pr2/ledger-trimmer`

**Deliverable:** the PR-3 branch for `docs/planning/upstream-read-set-pr-plan.md` §5 — the port of the
S130 apparatus extraction (`e02881a`) to an upstream-like tree. **No outward-facing action.** The
branch is built and verified locally; opening PR 3 needs its own operator go-ahead.

**Why stacked rather than on `46b56fd`.** S141's handoff assigned PR 3 "on the ADVANCED base once #77
merges". [PR #77](https://github.com/KJ5HST/methodology/pull/77) is **still OPEN** (verified from the
server this session), so `read-set-budgets` is still `46b56fd`, which carries **no**
`starter-kit/methodology_trim.py`. PR 3 touches the dashboard twins, whose canonical-only tests abort
with **13 errors** without the trimmer present. Building on `46b56fd` is therefore not available;
stacking on `pr2/ledger-trimmer` (`56997af`, the exact tree #77 proposes) is the same base #77 will
create on merge, so the branch retargets cleanly.

**Also at claim, and it is a separate action with its own commit `ef51dc9`: reconciled S141's
`commit:` answer slot.** `bin/check-handoff --allow-pending` went **0 -> 1** the moment this session's
receipt was prepended — a slot reading `the S141 claim + this close-out` is legal only while that
receipt is newest, and the spec (`starter-kit/HANDOFFS.md:64`, `:78-79`) makes the next session
resolve it. Set to `72b9b54` (claim) + `4329d33` (close-out), each verified by reading **that commit's
own copy of the S141 block** rather than inferred from subject lines: `72b9b54` holds it
`status: pending`, `4329d33` holds it `status: complete`. Checker back to **0**, read bare.

**`ef51dc9` reached history with no ledger line, and this entry is the repair.** The edit that should
have added it aborted on its own uniqueness assertion — the `**Ledger:** ... set at claim` boilerplate
occurs **3** times in this file, not once — but the `git commit` on the following line was never
chained to it and ran anyway. `.githooks/pre-commit` did not stop it: `git add CHANGELOG.md` on an
**unmodified** file stages nothing, so the co-staging test saw no ledger change to demand. **A
co-staging gate keyed on the path being staged cannot distinguish "ledger updated" from "ledger
mentioned",** which is exactly the reflex §6 dragon 2 of `docs/planning/upstream-read-set-pr-plan.md`
warns the derived-value checks would inherit.

**Ledger:** `CHANGELOG: pending` — set at claim; this session's actions are recorded here at Phase 3F.

### 2026-09-02 · [ad hoc] S141 — OUTWARD-FACING ACTIONS TAKEN: head branch pushed, **PR [#77](https://github.com/KJ5HST/methodology/pull/77) OPENED**

**Recorded here because neither action leaves a commit in this repository.** A push to `origin` and a
pull request on `KJ5HST/methodology` are both invisible to Phase 0 reconcile; failure mode #27's
write-gate is the only mechanism that records them.

**Authorization:** the operator's *"re-run the two HEAD-dependent pre-flight checks, push, and open it
with `--base read-set-budgets`"* — the pre-flight, the push and the base all named explicitly.

**Verified from the server, not from the commands' output** (`gh pr view 77`):

| Property | Value |
|---|---|
| State | **OPEN**, `MERGEABLE` |
| **Base** | **`read-set-budgets`** — never `main` |
| Head | `rmsharp:pr2/ledger-trimmer` (`56997af`, confirmed by `git ls-remote`) |
| Diff | 9 files, **+4,691 / −6**, **1 commit** |

**`main` is untouched at `512c2ed4` and remains the default branch**; `read-set-budgets` is still
`46b56fdb`, since opening a PR does not advance its base. `gh pr list` shows exactly one open PR.

**One step the operator did not name, disclosed in the claim before it was taken.** The branch carried
three WIP commits — two labelled *"WIP"*, one literally *"NOT ready to open"* — which would have
misdescribed the work to its reviewer. They were squashed into a single authored commit, and **the
tree was proved unchanged by comparing `HEAD^{tree}` against `81eedb0^{tree}`** rather than assumed:
a rebase that quietly drops a hunk looks exactly like a tidy history. Pre-flight was then re-run,
because the squash changed the very thing the first run had measured.

**The staging design is holding.** Two PRs have now landed on a branch created for selective developer
testing, and `main` has not moved once: `512c2ed4` before #76, before #77, and now.

**Not authorized, not done:** no merge, no comment on #75, #76 or #77, no tag, no release. **PRs 3–4
(apparatus, gate) stay unopened.** PR 3 is now unblocked — the ordering was measured, not assumed: the
dashboard's canonical-only tests abort with 13 errors without the trimmer present and 0 with it — and
it must be built on the **advanced** base once #77 merges, not on `46b56fd`.

- **Model:** Claude Opus 5 (1M context).

### 2026-09-02 · [ad hoc] S141 — claim: push `pr2/ledger-trimmer` and open PR 2 against `read-set-budgets`

**Ledger:** `CHANGELOG: pending` — set at claim; the actions are recorded here at Phase 3F.

**Operator authorized exactly this**, naming the pre-flight, the push and the base. Pre-flight re-run
at claim because both checks are HEAD-dependent: base `46b56fd`, branch **0 behind / 3 ahead**,
`git merge-tree --write-tree` **exit 0**, 9 files **+4,691 / −6**.

**One preparation step the operator did not name, taken and recorded rather than done silently:** the
branch's three commits are this arc's WIP steps, two labelled *"WIP"* and one literally *"NOT ready
to open"*. Shipping those into a pull request would misdescribe the work to its reviewer. They are
squashed into a single authored commit before the push — **the tree is unchanged**, only the history
is presentable, and that is verified by diffing the squashed tree against `81eedb0`.

**⚠ Crash note: a pull request leaves no commit in this repository.** If this entry is the frontier
with no close-out after it, run `gh pr list --repo KJ5HST/methodology --state all` before concluding
nothing shipped (failure mode #27).

**Not authorized, not done:** no merge, no comment on #75 or #76, no tag, no release; PRs 3–4 stay
unopened.

- **Model:** Claude Opus 5 (1M context).

### 2026-09-02 · [ad hoc] S140 close-out — option (C) delivered: PR 2 is green, 19 failures to zero added

**Deliverable:** `pr2/ledger-trimmer` = **`81eedb0`** plus
[`docs/planning/pr2-read-set-budgets-body.md`](docs/planning/pr2-read-set-budgets-body.md).
**PR 2 is ready to open and was NOT opened** — see the close-out receipt's `next_steps` (1).

**Measured in a clone where `020ba3f` and `7a71df0` are unreachable and `docs/archive/` is absent** —
never a worktree, which is the error that gave S138 and S139 two wrong counts:

| | Result |
|---|---|
| Base (`read-set-budgets` @ `46b56fd`) | 113 passed, 1 failed |
| **PR 2** | **114 passed, 1 failed** |
| **Delta** | **+1 passing row, ZERO added failures** |
| `tools/test_methodology_trim.py` alone | **123 tests, exit 0**, 2 skipped *(was 19 failures)* |
| `tools/test_methodology_dashboard.py` | **211 tests, exit 0** |

The one failure is the Test 9 #76 already declared: `bin/sync` reads `main`, and this branch's newest
manifest rows name files not yet there. It heals on merge to `main`.

**THE FIXTURES REPRODUCE STRUCTURE, NOT BYTES.** `SYNTHETIC_CHANGELOG` — front matter, records, and a
non-empty footer carrying a **rebasable `](link)`**, which is load-bearing: without one the
footer-moved clause is only ever tested verbatim and the `transform_record` path goes uncovered. And
a **25 = 6 + 19** partition with one **retained** record edited — precisely the property that made
`7a71df0` the event worth testing against.

**THE AUTHORS' OBJECTION — *"a synthetic one tests the test"* — IS ANSWERED EMPIRICALLY.** Three
mutants of the code under test were disabled in turn and each was **killed**:

| Mutant | Tests failing |
|---|---|
| `L2_FOOTER_MOVED` never emitted | **6** |
| `L3_RECORD_ALTERED` never emitted | **4** |
| `L1_MISMATCH` never emitted | **5** |

The source was restored byte-identically afterwards (`cmp` clean) and the baseline re-confirmed at
exit 0. **Without that evidence the conversion would be indistinguishable from deleting 19 tests.**

**Nothing was dropped to get green.** The three fixture controls were *rewritten*, keeping the
insight that a whole-file grep cannot distinguish *"the footer is present"* from *"a record merely
quotes it"* — the reason zones exist at all. And the two declared-regenerated-field tests **keep
their real artifacts and skip**: their point is that the live count really drifted by hand, so a
synthetic anchor there would test the test. Their precondition is read from the raw file, never
through `classify_zones`, which is the code under test.

**PR 3 (apparatus extraction) is now unblocked** — the coupling was measured, not assumed: the
dashboard's canonical-only tests abort with 13 errors without the trimmer present and 0 with it.

- **Model:** Claude Opus 5 (1M context).

