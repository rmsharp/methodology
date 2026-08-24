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

**Everything older than 2026-08-02 is archived, across two shards.** This file holds that day forward;
the preceding spans live in
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

**`bin/model-report` is the one consumer that loses coverage, and it loses more than it looks.** Its
Source 1 matches only the seed's list form `- **Model:**` (`bin/model-report:51`). This file's bullets
are all written in a bare `**Model:**` form it cannot parse, so **every bullet Source 1 could actually
see moved into the 2026-08-01 shard at this split** — run with no arguments it now reports an empty
Source 1 against a ledger whose entries visibly carry the bullet. Reach a span with
`bin/model-report --changelog <shard>`. The parser blindness is **not a consequence of this split**:
the form drifted at `1298af7` (2026-08-02) and has held unbroken since — *every* live entry, this
file's own newest included. Raised as **BL-20**, deliberately not fixed here (FM #17). The count that
stood here ("nine entries since") was falsified by the very next entry written above it, which is the
plan's own **DELETE** sink applied on the spot: the reader can count the list, and the command below
does it. Count both dialects,
never one — a single literal is a sample, not a population:

```sh
grep -cE '^-?[[:space:]]*\*\*Model:\*\*' CHANGELOG.md docs/archive/CHANGELOG-*.md
```

**When to archive again — a rate, not a level.** Archive when the headroom to the 2,000-line agent
`Read` cap, divided by the observed growth per ledger *entry*, falls below **15 entries**; then cut
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
and was silently dropping its ten oldest entries when a `Read` truncated it.

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

---

## 2026-08

### 2026-08-23 · [BL-41] `methodology_trim.py` disambiguates a taken shard name instead of refusing

`TRIM_VERSION` 1.2.0 → **1.3.0**, one DISTRIBUTED file. The shard name was a function of a record
DATE while the cut is POSITIONAL — not injective, yet used as a unique key behind a write-once
refusal, so every admissible cut of `HANDOFFS.md` derived one taken name and the tool's own advice
(*"Disambiguate with `--cut`"*) had no solution. A taken name now resolves to `-2`, `-3`, … and is
REPORTED; nothing is ever overwritten, and past `SHARD_SUFFIX_MAX` it still refuses.

`--cut 3` — the cut BL-41 recorded as impossible — now archives to
`HANDOFFS-through-2026-08-17-2.md`, retaining Test 34's floor of three: 82,966 → **43,928 B**.
**Dry run only; no trim was run** — a second capability (FM #26), scoped out by the operator.

RED first against copied fixtures (3 failures + 2 errors, both controls green on either side);
9 mutants, **9/9 killed**; suite diffed row-for-row against the Orient baseline, **zero rows lost**;
the 9 shipped `.verify.sh` proofs unchanged at 5 green / 4 red (BL-36, pre-existing).
Detail in the [`HANDOFFS.md`](HANDOFFS.md) receipt and the BL-41 row in `docs/planning/BACKLOG.md`.

**Model:** Claude Opus 5 (1M context).

### 2026-08-23 · [BL-41] S100 claim — restore the routine `HANDOFFS.md` trim

`CHANGELOG: pending`. Measurements and the seven declarations are in the `status: pending` receipt
in [`HANDOFFS.md`](HANDOFFS.md). **Deliberately minimal: this file had 397 B of byte headroom at
claim while its gate row read `894 ln / 2,000 ln — ok`.**

**Model:** Claude Opus 5 (1M context).

### 2026-08-18 · [ad hoc] S99 close-out — receipt written, self-score 8/10, predecessor S98 scored 8/10

Phase 3D receipt in [`HANDOFFS.md`](HANDOFFS.md), within the 18,432 B per-record budget S98
introduced (`check-handoff`: `1 unwritten record(s), 0 over`). Substantive work is the entry below.

**BL-41 raised, found not fixed:** `methodology_trim.py` cannot trim `HANDOFFS.md` at all. Shards are
named `HANDOFFS-through-<date of newest archived record>.md` and an existing one is never overwritten;
retention is by count, floored at three by `bin/tests.sh` Test 34. With receipts at S96/S97
(2026-08-17) and S98/S99 (2026-08-18) and `HANDOFFS-through-2026-08-17.md` already present, `--cut 3`
and `--cut 2` derive the taken name and are refused; `--cut 1` is free but drops below the floor.
**Every admissible cut yields the taken name, so the tool's advice — "Disambiguate with `--cut`" —
has no solution.** Verified by dry run; no `--write` issued. Full write-up and three candidate fixes
in [`BACKLOG-DETAIL.md#bl-41`](docs/planning/BACKLOG-DETAIL.md#bl-41).

**So `HANDOFFS.md` closes OVER — ~79.6 KB against 65,536, stated rather than left to be found; re-derive with the gate, since the figure counts the receipt that reports it.** It was already over at
claim: a protocol-mandated receipt landing in a ledger S98 closed with 2,863 B of headroom against
receipts that run 17–20 KB. No session writing any receipt could have avoided it.

**A Learning is owed and deliberately not written** — *a losslessness proof only proves losslessness
of the population it enumerates*. `starter-kit/FRAMEWORK_LEARNINGS.md` is DISTRIBUTED and this
session's claim declared it would touch none; holding to that was worth more than the row. #36 is the
next session's.

**Model:** Claude Opus 5 (1M context).

### 2026-08-18 · [ad hoc] `docs/planning/BACKLOG.md` comes under its ceiling by SPLIT — index here, bodies in a read-on-demand sibling

**103,755 B → 26,504 B, `ok`** — the only file the FM #28 gate flagged, now green. Commit `8eb4f0e`.
The 18 open-item bodies moved **verbatim** to
[`docs/planning/BACKLOG-DETAIL.md`](docs/planning/BACKLOG-DETAIL.md); `BACKLOG.md` keeps a 19-row
index. Full detail in the S99 receipt — this entry records the decisions a future session must not
re-litigate.

**Why a split and not a trim.** Open bodies were 81,340 B — 98% of the section, **1.24× the whole
ceiling alone**. Deleting the front matter, all 11 archive pointer rows and the historical section
(20,716 B, everything not live work) still left it 17,503 B over. Because nothing was compacted or
dropped, the operator policy question at `.context-budget.json:73` — what to abandon — was never
reached and stands unanswered.

**Why the ceiling stayed on the whole-file axis.** S97 and S98 moved the two sibling ledgers *off*
it after measuring 1 whole read in 80 and 81 transcripts. Measured the same way: this file was read
**whole 23 times across 22 of 82 transcripts (27%)**, against 584 partial reads, most recently
2026-08-13 — ~22× either sibling, because Phase 0 step 3 asks it for *current priorities*. Ceiling
**retained**; the per-record remedy deliberately not copied, and the budget entry now says so.
The instrument was audited before publishing: four defects found and fixed (`git cat-file -e` read as
a `cat`; two other repos' `BACKLOG.md` swept in; a quoted `sed` script split mid-expression; the word
*cat* inside receipt prose).

**Losslessness proved, not asserted.**
[`BACKLOG-DETAIL.md.verify.sh`](docs/planning/BACKLOG-DETAIL.md.verify.sh) re-extracts each item from
git **by `BL-N` identity, never by position** — the flaw behind BL-36's four false failures. C1–C5;
**7 mutants, each verified to apply, 7/7 killed** against a passing control.

**C5 exists because C1–C4 were green while content was lost.** The first cut silently dropped the
1,684 B *"Routing — what a session can actually run today"* block — not an item body, so outside the
population the proof enumerated, and the standing record that the *"blocked on the paused channel"*
disposition **was never imposed**. Restored verbatim; now asserted. **A losslessness proof only
proves losslessness of the population it enumerates.** C1 also had to be repaired before shipping:
it failed on any *newly raised* item, which would have turned it red on correct use.

**Mechanical readers, against baselines captured before the edit:** archive proof 4/4; dashboard
`_scan_backlog_done` unchanged at `unrecognized`/0/False — the index declares **no Status column**,
which would otherwise count the completed rows' `CLOSED`/`SHIPPED`/✅ as unmigrated done-marks;
`bin/tests.sh` 279/1/0 row-for-row identical; 444/444 Python; `check-links` 88/22; health 72. The
gate's structure check was repaired to follow the split and **proven red by mutation** before being
trusted — it had correctly reported `instrument-failed`.

Carve-out verified mechanically: 26 `DISTRIBUTION` rows vs 6 changed paths, both non-empty,
**intersection NONE**.

**Model:** Claude Opus 5 (1M context).

### 2026-08-18 · [ad hoc] S99 claim — bring `docs/planning/BACKLOG.md` under its ceiling

`CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in
[`HANDOFFS.md`](HANDOFFS.md) is the durable crash breadcrumb. Both resolved at this session's
close-out above.

Two facts recorded *at claim*, before any remedy was attempted, because they bound the remedy:
**no housekeeping cut could clear the ceiling** (`## Open items` alone was 1.27× it, so deleting
everything that is not live work still left the file 17,503 B over), and **the obvious cut was
load-bearing** — the archive proof's C4 asserts reachability against the live file, so deleting
§Completed items would turn a green proof red. Baseline captured before any edit: 4/4.

**Model:** Claude Opus 5 (1M context).

### 2026-08-18 · [ad hoc] S98 close-out — receipt written, self-score 8/10, predecessor S97 scored 8/10

Phase 3D receipt in [`HANDOFFS.md`](HANDOFFS.md); the substantive work is the per-record budget entry
below and the trim entry above it. **Framework Learning #35 appended** at 1,219 B against the 1,500 B
row budget — two limits set independently on one artifact can multiply into a constraint nobody
checks, which is why this breach kept recurring while each session's trim looked correct.

**The guard was applied to its own author.** This receipt measures **17,162 B against the 18,432 B
per-record budget introduced this session** — `check-handoff` reports `1 unwritten record(s), 0 over`.
The ledger closes at **62,673 B against the 65,536 B ceiling**, 2,863 B of headroom, and the FM #28
gate reports `HANDOFFS.md` **ok** for the first time in four sessions.

Two tracked telemetry ledgers committed with it — `.context-budget-history.jsonl` and
`dashboard_history.jsonl` — which go dirty from Phase 0 alone and which no protocol step owns.

**Model:** Claude Opus 5 (1M context).

### 2026-08-18 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-08-17.md` (4 record(s), 118,534 B → 49,579 B)

**Written by:** `methodology_trim.py` v1.2.0 — a tool action, not a session's judgment.
Moved the oldest **4** record(s) (2026-08-15 → 2026-08-17) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-08-17.md`](docs/archive/HANDOFFS-through-2026-08-17.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-08-17.md.verify.sh`](docs/archive/HANDOFFS-through-2026-08-17.md.verify.sh)
rather than trusting a digest printed here. Live file 118,534 B → 49,579 B (−58.2%).

### 2026-08-18 · [ad hoc] The receipt ledger gets a guard on the axis its cost is actually paid on — a per-record budget, derived from the collision it resolves

`HANDOFFS.md` stood at **114,466 B against a 65,536 B ceiling**, and the trim S97 recommended did
not clear it: re-derived, `--cut 3` gave **66,778 B**. The reason was not untrimmed backlog. Post-trim
the header is 6,017 B, leaving 59,519 B; `bin/tests.sh` Test 34 floors retention at **three**
receipts; the newest three totalled **60,761 B**. Floor × mean already exceeded ceiling − header, so
**no cut satisfied both constraints** — two limits set independently had begun to collide.

**Measured before choosing a remedy.** Across **81 transcripts** of this repo (the measuring session
excluded) the live root ledger was read **whole into a session's context exactly once** and read **in
part 593 times** — median span 25 lines, largest ever requested 220, against a 452-line file. No read
in the corpus asked for even half of it. That is what `SESSION_RUNNER.md` mandates and what
`.context-budget.json` already said in its own note: Phase 0 step 6 takes a **frontier** (`git log -1`,
no content) and Phase 3A reads **the predecessor's receipt in full**. One record.

**The instrument was wrong twice before it was right, both times flatteringly.** The first pass scored
the 4.5 KB seed `starter-kit/HANDOFFS.md` as the live ledger — 8 of its 9 "whole reads" were the seed —
and scored `awk '/^```handoff/{n++} n==1'`, which extracts *one receipt*, as a whole-file read. It
reported 9 whole reads. The answer is 1. Found by printing raw matched commands, not by re-reading the
counter.

**The fix.** `bin/check-handoff` (canonical-only) gains `RECORD_BUDGET_BYTES = 18432` and
`check_record_budget()`, scoped to the record **being written** — the newest record when its text
differs from its counterpart at git HEAD. Comparing record *text*, not "is this session id new", is
what stops a close-out from growing its own already-committed Phase 1B stub past the budget unseen.
The derivation is `(65,536 − 8,000 header allowance) / 3 = 19,178 → 18,432 B`, 2,240 B of slack, and it
is written beside the constant so a successor re-runs it rather than re-argues it. Records have grown
**3.15×** (oldest 10 mean 5,478 B; newest 10 mean 17,258 B; largest ever 21,267 B, n=104).

**The unit is the record, not the fenced block** — trailing prose below the closing fence is counted,
because the byte ceiling counts it and `methodology_trim.py` moves it as part of the record. Budgeting
the fence alone would put the guard on a different axis from the ceiling it is derived from and make
the arithmetic above false. Mutant **M5** exists to defend exactly that.

**Deliberately NOT run under `--all`:** Test 34's presence control asserts on `check-handoff`'s **exit
code** against the live ledger, and an exit code is a union over every check — routing the budget
through `--all` would turn an unrelated assertion red whenever a session's in-flight receipt ran long.
Asserted, not just intended, by assertion (7).

`bin/tests.sh` **Test 38** — 18 assertions, **5 mutants, 5 killed**, against a throwaway git repo so the
live ledger is never written to. Proven RED in situ first: an oversized record injected into the live
tracked file made the pre-change checker exit **0** and the new one exit **1**; restore verified
byte-identical by `cmp` and `git diff --quiet`. Suite **279 passed / 1 failed** (the pre-existing Test 9
`--source=github` 404), diffed row-for-row against a clean HEAD worktree: **zero rows lost**, 18 added,
both populations asserted non-empty (262 and 280).

**Two fixture defects of my own, both caught by the artifact and not by the builder.** The record
builder prepended at byte 0, absorbing the file's 5,569 B header into the record under test; and its
size check measured the string it had just constructed rather than the record as the checker parses it
— an identity, not an assertion. Corrected to insert at a **line-anchored** fence (a plain
`text.index("```handoff")` lands in front-matter prose that mentions the fence inline, leaving 86 stray
bytes inside the record) and to re-parse the written file.

Carve-out verified mechanically against the staged set: **26 manifest SOURCE rows vs 2 changed files,
both populations asserted non-empty, intersection empty** — no distributed file touched.

**Model:** Claude Opus 5 (1M context).

### 2026-08-18 · [ad hoc] Session S98 claimed — bring `HANDOFFS.md` under its ceiling durably

Phase 1B claim; receipt stub in [`HANDOFFS.md`](HANDOFFS.md) with `status: pending`. The subject is
S97's `next_steps` (b), and it is the repository's live size breach: **114,466 B against a 65,536 B
ceiling, over by 48,930**.

**One finding is recorded here at claim rather than at close-out, because it refutes the remedy the
handoff recommends.** S97 measured `--cut 3 = 49,724 B` and called it "real room". Re-derived at this
Orient, the same cut yields **66,778 B — 1,242 B over**. S97's figure was taken before its own
20,086 B receipt was appended, and it said so; that receipt is now one of the three a `--cut 3`
retains.

**The condition is a collision between two constraints set independently, not a backlog of untrimmed
bytes.** Post-trim the header is 6,017 B, leaving 59,519 B for records. `bin/tests.sh` Test 34 floors
retention at **three receipts**. The last three total **60,761 B** (mean 20,254 B). Floor × mean
already exceeds ceiling − header, so **no cut satisfies both**: `--cut 2` clears at 45,511 B only by
going below the floor, where six assertions become stated `SKIP` rows (BL-40 (b)).

Which of the three levers moves — receipt **size**, the **floor**, or the **ceiling** — is a policy
choice and goes to the operator with numbers before anything is written. Noted for that choice:
`.context-budget.json` sources this ceiling to `methodology_trim.py:69` — the trimmer's
`DEFAULT_BUDGET_BYTES`, an **inherited default**, at a line number S97 already flagged as stale — while
the same entry states the mandated read as *"Phase 0 step 6 reconciles this file's frontier and Phase
3A reads the predecessor's receipt in full."*

**Model:** Claude Opus 5 (1M context).

### 2026-08-17 · [ad hoc] S97 close-out — receipt written, self-score 7/10, predecessor S96 scored 9/10

Phase 3D receipt in [`HANDOFFS.md`](HANDOFFS.md); the substantive work is the entry below. Telemetry
committed with it rather than inherited forward, as S96 did — `.context-budget-history.jsonl` and
`dashboard_history.jsonl` accumulate rows from running Phase 0 alone and no protocol step owns them.

**Self-score is 7 rather than 8 for one specific reason, recorded here and not only in the receipt:**
the session's first access measurement was wrong — it counted `cat >> file` appends and filenames
inside `git commit` heredocs as whole-file reads — and its headline figures were shown to the
operator before the instrument was audited. Corrected one turn later by printing the raw matched
commands, and the remedy decision was taken on the corrected numbers.

**`starter-kit/FRAMEWORK_LEARNINGS.md` ends this session at 60,469 / 65,536 B** — over the ceiling it
started under, and under the one derived to replace it. That is the intended outcome and the receipt
says so plainly: this session moved the RATE lever, leaving roughly **three rows** of headroom. The
LEVEL is unfixed by the operator's deliberate choice among four costed shapes.

**Model:** Claude Opus 5 (1M context).

### 2026-08-17 · [ad hoc] The Learnings-table ceiling moves onto the axis the cost is actually paid on — a per-row budget, and a whole-file ceiling derived instead of inherited

`starter-kit/FRAMEWORK_LEARNINGS.md` had 604 B of headroom against a 60,000 B ceiling, and the
ceiling was **inherited from the seed** — `.context-budget.json` said so in its own words. Measured
before choosing a remedy: across **80 transcripts** of this repo the file was read **whole once** and
read **in part 243 times**, and it was never touched at all in 47 of the 80. A partial read returns
whole **rows**, because a row is one physical line — so the cost a session actually pays here is
per-row, and rows have grown **4.9×** (rows #1–#6 average 510 B; #24–#33 average 2,510 B).

**The guard was on the wrong axis, so the axis moved rather than the number.** `bin/check-learnings`
gains `ROW_BUDGET_BYTES = 1500`, scoped to rows **not yet frozen in git HEAD** — deliberately, because
the table is append-only, and a finding against a row nobody may edit is a gate that cannot be obeyed.
`max_bytes` is re-derived to **65,536 B**, the ceiling this repo already applies to its three other
accumulating ledgers (`starter-kit/methodology_trim.py:80`), and a whole-file read at that size
(23,406 tok, 55.7% of the measured 42,033-tok floor) sits inside the range of whole-file reads this
repo already performs routinely. **That is a raise, from a 50.5% permitted tail to 55.7%, and it is
recorded as one.** `max_line_bytes` is deliberately NOT declared: 20 of 32 rows exceed 1,500 B, so it
would be permanently red against frozen rows.

`bin/tests.sh` **Test 37** — 14 assertions, 4 mutants, all killed, against a throwaway git repo so the
live table is never written to. **Three of those four mutants were scoring themselves killed while
asserting nothing**: with `set -o pipefail`, `producer | grep -q` makes the producer take SIGPIPE when
grep short-circuits, and on a `&& fail || pass` polarity a broken pipeline lands on `pass`. Captured
into a variable first, as the rest of the suite already does, and the reason is recorded in the test.

**What this does not do: it does not make the file smaller.** Headroom is 6,140 B, about four more
rows. The two shapes that shrink it — a tighter derived ceiling forcing a shed, or a distributed
archive split — were put to the operator with numbers and deliberately not taken.

**Model:** Claude Opus 5 (1M context).

### 2026-08-17 · [ad hoc] Session S97 claimed — bring `starter-kit/FRAMEWORK_LEARNINGS.md` under its ceiling durably

Phase 1B claim; receipt stub in [`HANDOFFS.md`](HANDOFFS.md) with `status: pending`. The subject is
S96's `next_steps` (b): the file stands at **59,396 / 60,000 B — 604 B of headroom** while recent
Learning rows run 1,431–3,451 B, and it is **DISTRIBUTED**, so it is the one imminent breach an
adopter inherits.

**One finding is already established and is recorded here at claim rather than at close-out, because
it refutes the remedy a reader would assume.** Trimming oldest-first — what `methodology_trim.py`
does to `CHANGELOG.md` and `HANDOFFS.md` — is the wrong axis for this file. Re-derived with
`bin/check-learnings`'s own `CITATION_RE` over `bin/_manifest.py`'s 26-row distributed population:
**all 24 `Learning #N` tokens in the distributed corpus cite a row numbered ≤ 16.** Age here
correlates with being foundational, not with being stale.

The inverse reading is refused for cause in the same breath: the 17 rows numbered ≥ 17 hold 40,851 B
(70.6% of row bytes) and no distributed citations, but [Learning #29](starter-kit/FRAMEWORK_LEARNINGS.md)
— ratified five sessions ago — is precisely the finding that an uncited rule is *orphaned*, not
worthless. Citation count is not an archive criterion.

**Model:** Claude Opus 5 (1M context).

### 2026-08-17 · [ad hoc] S96 close-out — receipt written, self-score 8/10, predecessor S95 scored 9/10

Phase 3D receipt in [`HANDOFFS.md`](HANDOFFS.md); the substantive work is the BL-40 entry below.
Two tracked telemetry ledgers committed with it — `.context-budget-history.jsonl` and
`dashboard_history.jsonl` accumulate rows from running Phase 0 alone, and no protocol step owns
writing them. Committing rather than inheriting the dirt forward; the ownership gap itself is
recorded in the receipt's `next_steps` (f), not fixed.

**`HANDOFFS.md` ends this session at 94,380 B against a 65,536 B ceiling** — worse than the 74,683 B
it started at, and stated rather than buried. The trim this session unblocks was deliberately not
taken: it is a second capability (FM #26). The receipt hands it forward with the method for
re-deriving the numbers rather than the numbers themselves, because the last two sessions both
published headroom figures that were stale by their own close-out.

**One correction made at the final gate rather than left standing:** the self-assessment claimed this
receipt was the smallest of the last five at 13,986 B. That measured the fence block alone against
predecessor figures that include the assessment prose. On a like-for-like basis it is **18,845 B**,
the second largest (S95 21,266; S92 16,840; S94 16,135; S93 15,159). Corrected in place, and the
self-score reasoning updated to count it.

**Model:** Claude Opus 5 (1M context).

### 2026-08-17 · [BL-40] Test 34's mutation anchors become an asserted population with a stated skip — six assertions could vanish, not five

`bin/tests.sh` Test 34 read its two mutation anchors as `ids[1]`/`ids[2]` of the live `HANDOFFS.md`.
Below three receipts `ids[2]` raised `IndexError`, both anchors resolved to empty, and the
anchor-dependent assertions stopped asserting. Option **(b)** of BL-40, taken as recorded and as
[Learning #31](starter-kit/FRAMEWORK_LEARNINGS.md) itself prescribes: assert the population, skip
with a stated reason below the floor.

**Canonical-only.** `bin/_manifest.py` exposes 26 SOURCE rows (asserted non-empty) and none under
`bin/`; no adopter receives this. Option (a) — a retained-records floor in the distributed trimmer —
stays declined: the trimmer has no business knowing a test's fixture requirements.

**What changed.** `handoff_anchors` returns `<count> <A1> <A2>` and cannot raise;
`anchor_disposition` routes that count to MALFORMED / EMPTY / SHORT / ANCHORED, with the
non-numeric arm FIRST so a garbled count cannot fall through to the permissive default. The SHORT
arm emits six `SKIP` rows, each naming the assertion it replaces and the reason. A new `skip()`
primitive counts separately from `pass()`, and the summary line now reads
`N passed, M failed, K skipped` — **a format change, announced at claim**, because every receipt in
`HANDOFFS.md` compares suite output row-for-row against a predecessor baseline.

**RED first, against copied fixtures — the live ledger was never truncated.** The pre-change body,
extracted verbatim and replayed at 1/2/3/4 receipts: **2 passed / 5 failed** below the floor,
**8 / 0** at or above it. After: **11 / 0 / 6 skipped** and **17 / 0 / 0**. A 0-receipt ledger still
FAILS — corruption is not rotation.

**This item's own count was low, and the correction is the session's learning.** BL-40 and Learning
#31 both said *five* assertions stopped asserting. **Six** did. The sixth sat in the then-branch of
a failed `if mutate` guard and emitted no row at all — not a pass, not a fail. The published
arithmetic carried the discrepancy in plain sight (235 → 229 passes is six fewer, against five new
failures) and nobody subtracted. Recorded as **Learning #33**.

**Verification.** 9-mutant round on the new guards, **9/9 killed**, unmutated control green — each
mutant verified to APPLY first, so did-not-apply stayed distinct from survived. Killed mutants
include both silent-vacuum reinstatements: a renamed `SHORT)` arm (reads as 0 skip rows) and a
non-numeric count routed permissively. Full suite **247 passed / 1 failed / 0 skipped**, diffed
row-for-row against a 236-row pre-change baseline: **zero rows lost**, 13 added (12 new controls
plus Test 31's `**Model:**` equality moving 8 → 9 as this session's own entries joined the
population). Sole failure is Test 9's pre-existing `--source=github` 404, confirmed by name.

`HANDOFFS.md`'s front-matter warning said *"This is avoided here, not fixed."* That is now false and
was corrected in place; it still says `--cut 3`, because a stated skip does not restore coverage.

**Model:** Claude Opus 5 (1M context).

### 2026-08-17 · [BL-40] Session S96 claimed — Test 34's mutation anchors become an asserted population with a stated skip

Phase 1B crash breadcrumb, recorded at claim rather than at close-out so the ledger is true while the
work is in flight. Deliverable: `bin/tests.sh` Test 34, whose two mutation anchors are read at run
time as `ids[1]`/`ids[2]` of the live `HANDOFFS.md` (`:2103`). Below three receipts `ids[2]` raises
`IndexError`, both anchors come back empty, and five real assertions report `mutation was vacuous` —
a red that names the mutation rather than the cause.

**Carve-out verified at claim, not asserted:** `bin/_manifest.py` exposes **26** SOURCE rows
(population asserted non-empty) and **none** under `bin/`, so this file is canonical-only and no
adopter receives the change. One declared exception: `starter-kit/FRAMEWORK_LEARNINGS.md` is
distributed and Phase 3C is mandatory — it stands at 57,964 / 60,000 B, so the row is budgeted
against 2,036 B of headroom rather than written first and measured after.

**Announced in advance:** the suite's summary line changes shape to carry a skip count. Every receipt
here compares suite output row-for-row against a predecessor baseline, so an unannounced format
change would read as a regression.

**Model:** Claude Opus 5 (1M context).

### 2026-08-17 · [ad hoc] `HANDOFFS.md` crossed its byte ceiling this session — recorded, with the residual shown to be structural

74,683 B against 65,536 B. It entered this session at **53,272 B**, under the ceiling, so this is
S95's doing: the S95 receipt is 20,146 B, the largest of the four (S94 16,136; S92 16,840; S93 15,160).

**The residual is structural, not one session's appetite.** Four receipts now average ~17 KB, so
65,536 B cannot hold four at current sizes. S94's stated "~2 sessions of headroom" was computed from a
10–13.5 KB per-receipt distribution that its own 16,136 B receipt already exceeded — a headroom figure
derived from a stale distribution, which is [Learning #12](starter-kit/FRAMEWORK_LEARNINGS.md)'s shape
applied to a rate rather than a count.

Self-reduction was attempted and is reported honestly rather than claimed as a fix: `active_task`
compacted 2,699 → 1,660 B, then 1,313 B deliberately spent making `next_steps` (a) executable on the
breach — a net **+274 B**. Shaving prose could not have cleared 8,026 B without gutting the handoff.

**The trim that is owed has a constraint the tool's default violates:** `--cut 3`, not the default,
because `bin/tests.sh:2103` reads its mutation anchors as `ids[1]`/`ids[2]` of the live file (BL-40,
unfixed). Retaining 3 lands ≈52 KB — under the ceiling, above the ≤ ½ × budget stop condition, and **no
cut satisfies both**: retaining 2 would satisfy the stop condition and break Test 34. That tension is
BL-40's to resolve, and it is named rather than silently decided.

**Model:** Claude Opus 5 (1M context).

### 2026-08-17 · [ad hoc] A stale figure in S95's own receipt corrected — the `**Model:**` carrier count, 2 → 6

The receipt's `next_steps` (b) gave the live carrier population as **2**, measured immediately after
the trim and already wrong by close-out: this session's four close-out entries each carry a
`**Model:**` bullet, so the true figure is **6**. Caught by the final `bin/tests.sh` run, where Test
31's real-file row moved 2 → 6 and stayed green because it asserts an equality rather than a level.

This is the same defect class this session's Phase 3A deducted its predecessor for — a number that
was true when written and false when read. The corrected line now carries the command that re-derives
it rather than only the value: `grep -cE '^-?[[:space:]]*\*\*Model:\*\*' CHANGELOG.md`.

**Model:** Claude Opus 5 (1M context).

### 2026-08-17 · [ad hoc] `HANDOFFS.md`'s unguarded receipt count corrected — 3 → 4, one close-out after the trim that set it

[`HANDOFFS.md:8`](HANDOFFS.md) read **3** while the file held **4**. Not a new defect and not a
surprising one: the blockquote directly below that line predicts this exact span — the count is a
field `methodology_trim.py` regenerates at a **trim**, and nothing updates it when a session
**prepends** a receipt, so it is right immediately after a trim and wrong from the next close-out
onward. S95's own close-out was that next close-out, so this session created the drift it is
repairing. Prior occurrence: the line read **6** from `7a71df0` for three sessions.

The stale attribution went with it — the sentence credited the S94 trim for a number that trim no
longer determined. Every other figure in it was re-derived rather than carried: 19 archived receipts,
2026-07-08 → 2026-07-30, both confirmed against `docs/archive/HANDOFFS-archive.md`.

Still **not** mechanized — this is a hand correction of a hand-maintained number, which is the
half of upstream [issue #65](https://github.com/KJ5HST/methodology/issues/65) that remains open.

**Model:** Claude Opus 5 (1M context).

### 2026-08-17 · [ad hoc] The two tracked telemetry ledgers committed — 16 append-only rows that had accumulated uncommitted

`.context-budget-history.jsonl` (12 rows) and `dashboard_history.jsonl` (4 rows). Both are tracked
**deliberately** — `.gitignore` states the reason for each: they are append-only and non-regenerable,
and `context_budget.py`'s growth-run trigger *reads* the series, so it must survive a fresh clone.
Sixteen rows living only in one working tree defeats precisely that. Same action, same reasoning, as
`2026-08-15 · [ad hoc] dashboard_history.jsonl committed` (now in
[`docs/archive/CHANGELOG-through-2026-08-15.md`](docs/archive/CHANGELOG-through-2026-08-15.md)).

**Whose rows these are, stated rather than glossed:** 13 of the 16 are inherited, spanning the S87–S94
era — `HANDOFFS.md` at 21,231 B and 38,071 B, S94's two trims, are visible in the series. **3 are this
session's**, written merely by orienting and verifying: a Phase 0 dashboard snapshot and two budget
measurements, the last of which is the first row in the series to record `CHANGELOG.md` at 31,539 B.

**The underlying gap is NOT fixed.** No protocol step owns writing these files, which is why the diff
accumulated across at least four sessions and three receipts flagged it. This commits the data; it
does not assign the ownership. A session that runs the Phase 0 dashboard dirties the tree and no
close-out step tells it what to do about that.

**Model:** Claude Opus 5 (1M context).

### 2026-08-17 · [ad hoc] S95 close-out — receipt written, self-score 8/10, predecessor S94 scored 9/10; see the trim entry below for the substantive work

Also in this commit: **Framework Learning #32** (31 rows, `#14` still reserved) — *a count-based cut
cannot see a content-population floor, and whether it trips is a fact about your data's layout rather
than an invariant*.

**The deliverable, stated as a measurement:** `CHANGELOG.md` 84,765 B → **31,539 B** (−62.8%), under
both the 65,536 B ceiling and the seed's stated stop condition of ≤ ½ × budget (32,768 B). The FM #28
gate now reads this file **ok**; `docs/planning/BACKLOG.md` (104,530 B) remains the only breach and was
not touched (FM #17).

**What made the proof pass, and it is the commit shape rather than the tool.** The trim commit
`c3d68c5` contains the trim and nothing else; this receipt stayed `status: pending` across it and is
finalized only here. The frozen proof reports `added by the trim commit: 1` — the trimmer's own ledger
entry, which v1.2.0 excuses as an *added* record — and passes. This repo now holds **8** shipped
proofs, **4 passing**; the 4 reds are BL-36's untouched frozen residual, unchanged by this session.

**The audit S94 flagged as owed, done: `CHANGELOG.md` has six readers that are not human.** Two are
safe by prior hardening (`bin/tests.sh:1751` reads live **+** archives since S87; `:1788` reads the
front matter, which a trim preserves). One is **binding**: `:1886` requires a non-empty `**Model:**`
population, and the only carriers were records #4 and #13 of 41 — an unstated floor of N ≥ 4 that no
count check would surface. A second, separate floor is a count: `.context-budget.json`'s structure
guard wants ≥ 5 records. The tool's default retained 13 and cleared both, so it was taken
rather than overridden — the opposite decision from S94's, reached by the same method. One reader
*cannot* break by construction and it is worth naming: `bin/check-handoff`'s `changelog_ref` rule is a
**prohibition on line numbers**, not a resolution check — which is exactly why the field quotes
headings.

**`CUT_STRADDLES_DAY` was accepted, not overlooked.** The tool flags that the shard name is a span
label rather than a day boundary. That is unavoidable here, and it was proven so rather than assumed:
the date sequence is `08-16×4, 08-15×1, 08-16×1, 08-15×31, 08-12×3`, and the only non-straddling seam
sits at 74,753 B — over the ceiling.

**Model:** Claude Opus 5 (1M context).

### 2026-08-17 · [ad hoc] Framework Learning #32 appended — a count-based cut cannot see a content-population floor

Appended to [`starter-kit/FRAMEWORK_LEARNINGS.md`](starter-kit/FRAMEWORK_LEARNINGS.md) (DISTRIBUTED;
55,193 → 57,964 B, leaving **2,036 B** under its 60,000 B ceiling — one more row of this size breaches
it). Sibling of Learning #31: #31's coupling is *dimensional* (a fixture needs at least three records,
so a count check finds it), while #32's is *content* — which records survive, not how many. A
positional trimmer has no vocabulary for "retain at least one record satisfying P", and a dry run
reports bytes and counts, the exact quantities such a floor is invisible to.

**Model:** Claude Opus 5 (1M context).

### 2026-08-17 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-08-15.md` (28 record(s), 84,765 B → 31,539 B)

**Written by:** `methodology_trim.py` v1.2.0 — a tool action, not a session's judgment.
Moved the oldest **28** record(s) (2026-08-12 → 2026-08-15) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-08-15.md`](docs/archive/CHANGELOG-through-2026-08-15.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-08-15.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-15.md.verify.sh)
rather than trusting a digest printed here. Live file 84,765 B → 31,539 B (−62.8%).

### 2026-08-17 · [ad hoc] S95 claimed — `CHANGELOG.md` trim, recorded before the trim because the trimmer's own P1 guard refuses otherwise

Claim commit `a35a14f` (`HANDOFFS.md` receipt, `status: pending`). Recorded here as its own action
before any technical work, because `methodology_trim.py`'s P1 guard refused the trim outright while
this commit sat above the ledger frontier:

> `[P1_UNDOCUMENTED]` the undocumented set is non-empty (1 commit(s) since the ledger frontier
> `defe66a`). A trim commit advances that frontier and would hide them PERMANENTLY.

That is not an inconvenience to route around — a trim rewrites this file, so `git log -1 -- CHANGELOG.md`
would advance past the claim and Phase 0's `frontier..HEAD` set would lose it for good. The order
trimming forces is **claim → record → trim → close-out**, exactly as S94 recorded it.

**Model:** Claude Opus 5 (1M context).

### 2026-08-16 · [ad hoc] S94 close-out — receipt written, self-score 8/10, predecessor S93 scored 9/10; see the trim entry below for the substantive work

Also in this commit: **Framework Learning #31** (30 rows, `#14` still reserved) — *a test that reads
its own fixture anchors from a live artifact is coupled to that artifact's SIZE, and the tool that
shrinks the artifact cannot see the coupling* — and **BL-40** raised in
[`docs/planning/BACKLOG.md`](https://github.com/rmsharp/methodology/blob/main/docs/planning/BACKLOG.md).

**Why this trim's proof passes when the two before it do not, and it is not the tool.** Both
previously shipped `HANDOFFS` proofs are red because each of those trim commits finalized its own
frontier receipt *inside* the trim, editing a record that existed at `TRIM^` and whose pre-trim bytes
then exist nowhere. S93's v1.2.0 made a commit's **added** records tolerable and deliberately did not
excuse an **edited** one. So the commit shape was declared at claim time and held: this receipt
stayed `status: pending` across the trim commit and was finalized only afterwards, where a frozen
proof — which reads all three artifacts from the trim commit by design — cannot see it. The proof
reports `added by the trim commit: 0`. This is audit recommendation 3's discipline *followed*; the
rule itself is still unwritten.

**The trimmer's P1 guard re-ordered the session, correctly** — see the claim entry below. The order
trimming forces is **claim → record → trim → close-out**.

**The first trim was wrong, and the suite caught it — the session's other finding.** Taken at the
tool's budget-driven default it retained **2** receipts and made five of `bin/tests.sh` Test 34's
assertions vacuous (**235 passed / 1 failed → 229 / 6**). Test 34 reads its mutation anchors as
`ids[1]`/`ids[2]` of the live ledger (`bin/tests.sh:2103`), deliberately not hardcoded so it survives
*which* receipts rotate — and silent about *how many* must survive. It was visible only because the
harness reports `mutation was vacuous` as an outcome distinct from *survived*. That commit was
unwound with `git reset --soft` plus targeted `restore`/`checkout` — never `--hard`, with two
inherited dirty `.jsonl` files in the tree — and re-taken at `--cut 3`.

**Retention chosen against both constraints, with the numbers.** Receipts here run 10–13.5 KB
(S91 13,553 B; S92 13,091 B; S93 11,917 B):

| retained | live size | headroom | Test 34 |
|---|---|---|---|
| 2 (tool default) | 21,231 B | 44,305 B | **vacuous** |
| **3 (taken)** | **38,071 B** | **27,465 B** (~2 sessions) | satisfied exactly |
| 4 | 56,222 B | 9,314 B | satisfied, < 1 receipt of room |

**The coupling is avoided, not fixed** — the next default-cut trim re-breaks Test 34. Raised as
BL-40 with two candidate fixes; the recommended one (make Test 34 skip with a stated reason below
three receipts) is canonical-only and was **not** implemented or tested here. A `--cut 3` floor
warning now sits in `HANDOFFS.md`'s own front matter, whose stale retained-count attribution was also
repaired — the trim regenerates that number but left the credit reading `S92, 2026-08-15`.

Proof driven RED before committing, the only window in which it can see a working-tree change:
record deleted → `MISSING: session: S89`/`S88`; pure reorder with the record multiset asserted
identical → `L3 record(s) out of order across the move: [3, 4]`. Every restore `cmp`-verified against
backups held outside the repo. The FM #28 gate now reads `HANDOFFS.md` **ok**; `CHANGELOG.md` and
`docs/planning/BACKLOG.md` remain over and were deliberately not touched (FM #17).

**One carve-out breach, recorded rather than dressed up.** The Phase 1B claim declared **zero
distributed files**. Phase 3C is a mandatory close-out step and its only home is
`starter-kit/FRAMEWORK_LEARNINGS.md`, which `bin/_manifest.py` distributes. The learning was kept —
skipping a mandatory step to protect a self-imposed scope note is the wrong trade, and the edit is
append-only and purely local, so no operator gate is involved — but the claim should have
pre-declared the contingency, as S93's did. Verified mechanically at close-out: 26 manifest rows,
6 files changed, **one** distributed.

### 2026-08-16 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-08-15.md` (8 record(s), 141,085 B → 38,071 B)

**Written by:** `methodology_trim.py` v1.2.0 — a tool action, not a session's judgment.
Moved the oldest **8** record(s) (2026-08-11 → 2026-08-15) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-08-15.md`](docs/archive/HANDOFFS-through-2026-08-15.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-08-15.md.verify.sh`](docs/archive/HANDOFFS-through-2026-08-15.md.verify.sh)
rather than trusting a digest printed here. Live file 141,085 B → 38,071 B (−73.0%).

### 2026-08-16 · [ad hoc] S94 claimed — `HANDOFFS.md` trim, recorded before the trim because the trimmer's own P1 guard refuses otherwise

Commit `1ac90ac`, the Phase 1B claim stub. Recorded here **now, mid-session**, rather than at
close-out where a claim commit is normally folded into the session's substantive entry — because
this session's deliverable is a trim, and `methodology_trim.py`'s **P1_UNDOCUMENTED** guard refused
the dry run while this commit sat above the ledger frontier:

> the undocumented set is non-empty (1 commit(s) since the ledger frontier `5c8620c`). A trim commit
> advances that frontier and would hide them PERMANENTLY. Reconcile first, then trim.

The guard is right, and the mechanism is worth stating because it is not obvious: a trim rewrites
`CHANGELOG.md`, so `git log -1 -- CHANGELOG.md` becomes the trim commit, and Phase 0's
`frontier..HEAD` undocumented set silently loses everything that preceded it. The ordering this
forces is **claim → record → trim → close-out**, and it is a property of trimming specifically, not
a change to the general close-out rule.

Deliverable and pre-declared commit shape are in the receipt (`HANDOFFS.md`, S94). No distributed
file is touched; no outward-facing action.

### 2026-08-16 · [BL-36] The archive losslessness proof stopped inferring what the trim commit added — `methodology_trim.py` v1.2.0

Four of six shipped `.verify.sh` proofs reported FAIL over archives S88 had already measured
**intact** (0 records missing at every trim, 0 of 228 identities unreachable at HEAD). S88 located
the fault in the proof and deliberately made no repair: the file is DISTRIBUTED, so the fix needed
its own operator-gated, RED-first session. Given, and taken here.

**Root cause, restated precisely, because it decided the shape of the fix.** The generated script
identified the records the trim *commit* introduced with `INJECTED`, a constant baked in at
generation time as `1 if trims_the_ledger else 0`, and skipped that many **positions**. Inside the
tool that quantity is a fact — it performs the injection and knows the answer is 0 or 1. In the
exported script it is an **inference** about a commit that may carry a whole session's other
ledger writes. So it was right whenever the commit held only the trim, which is every case anyone
had checked, and wrong by construction otherwise.

**The repair is audit rec 2 — "make `injected` a measured count" — done by CONTENT, not by
position**, and that departure was declared at Phase 1B rather than reconciled at close-out.
Measuring it positionally would derive the operand from the very difference L1/L3 assert on: an
identity that cannot fail (Learning #16). The added set is now `after + shard` minus `before`,
by record text, removed occurrence-wise and in order before the byte comparison runs. `INJECTED`
is gone from the template. L1/L2/L3 keep their names and semantics; losses, edits and reorders
still fail. `:1736`'s in-memory twin is deliberately unchanged, with a comment saying why.

**Measured on the six real shards, replayed read-only with `docs/archive/` untouched:**
`CHANGELOG-through-2026-08-02` and `-08-09` go **FAIL → PASS**, naming the 2 and 3 records their
commits added; the two already-green proofs stay green; the two `HANDOFFS` proofs **stay red,
correctly** — each trim commit finalized its own frontier receipt, so that record's pre-trim bytes
exist nowhere afterwards — now reported as `MISSING: session: S61` / `S64` beside the added twin
instead of `L3 record [0] not byte-identical`. Audit Finding #4 is dissolved, not extended.

**Evidence.** Six RED-first tests (`tools/test_methodology_trim.py`, canonical-only), all observed
failing against the unmodified tool first; suite 97 → **103/103**. `bin/tests.sh` **235 passed / 1
failed**, compared row-for-row against the pre-change baseline with both populations asserted
non-empty (236 rows each, zero rows lost, the single delta a replay counter that now includes this
session's own claim commit); the sole failure is Test 9's pre-existing github-source 404.
Third surface, the one that matters for a distributed file: a fresh `bin/sync` adopter tree
delivers the tool byte-identical at v1.2.0, a bundled trim there proves lossless end to end, and a
pre-commit shard tamper still goes red naming its victim.

**Two narrowed controls earned their place by failing.** One caught that the new global `missing`
silently rebound L2's same-named front-matter variable three clauses above it — a flat generated
script has one namespace — so L3 read L2's usually-empty list and reported a downstream symptom
instead of its own finding. The other caught that the first reorder fixture swapped two records
the commit had *added*, which is correctly invisible, and so proved nothing.

BL-36 is narrowed to its open residual: the four already-frozen artifacts, whose disposition the
operator scheduled as a separate session.
- **Model:** Claude Opus 5 (1M context).

### 2026-08-15 · [ad hoc] `HANDOFFS.md`'s unguarded receipt count corrected — 5 → 9, and the recount command put beside it

The header's *"this file currently holds N"* is asserted by nothing and drifts every time a session
prepends; the file's own front matter warns *"Recount before trusting it."* It read **5** against an
actual **9**, having last been corrected three sessions after its previous drift (`7a71df0`). S92
prepended the ninth, so this is the Phase 3F cross-reference duty (Learning #7) on a claim this
session moved — not an adjacent cleanup. The remedy is `Compute`, not a fresh hand-count: the number
now ships with `grep -c '^```handoff' HANDOFFS.md` beside it. This is the receipt-ledger half of
upstream [issue #65](https://github.com/KJ5HST/methodology/issues/65) and remains open as a *guard*.

### 2026-08-16 · [issue #75] Comment posted upstream — the gate (d) finding handed to the maintainer, on his explicit go-ahead

**An outward-facing action, authorized by the operator for this action specifically** (comment only;
no PR, no push, nothing else — the standing rule is per-action, and PR #64's precedent stands).
Posted as `rmsharp`: <https://github.com/KJ5HST/methodology/issues/75#issuecomment-5305674268>.

Content: (1) the gap independently re-verified against `upstream/main` before anything else;
(2) **the finding — gate (d) already states the principle and no general procedure routes to it**,
with the citation count stated precisely rather than as the overstated "nothing cites it," and the
suggestion that the new requirement *quote* gate (d) instead of standing alone; (3) that his
one-line diff would create the checklist's only orphan, since all six existing items mirror a
requirement stated above them; (4) that the same gap sits in three more places he did not name
(`ITERATIVE_METHODOLOGY.md:287-288`, Quality Gate 8 at `:432`, Phase 3E at
`SESSION_RUNNER.md:272`); (5) `SAFEGUARDS.md:95` as prior art in the same species; and (6) the
honest caveat that this is a **requirement, not a gate** — nothing refuses a plan that omits its
surface, which is the Degradation table's own standard turned on the proposal.

**Every citation was re-derived against `upstream/main`, not against this fork** — line numbers here
had shifted by the local change, and `docs/planning/b1-sync-coverage-expansion-plan.md` (the plan
that had applied gate (d) at plan time) **does not exist upstream**, so it is described without a
path the maintainer cannot resolve. Closes with the implementation offered but **not** sent, and his
own stated intent to write the checklist line left as his to take.
Carries the agent-authorship disclaimer (`DEVELOPMENT_WORKSTREAM.md` §Agent-Authored Triage
Comments).

### 2026-08-15 · [ad hoc] S92's "zero inbound citations" claim corrected — the count came from grepping one spelling

The `[issue #75]` finding below was published as *"nothing cited it."* Re-checked on a direct
question and it is **wrong**: the grep behind it was `gate (d)`, which silently misses `gate d` at
`starter-kit/SESSION_RUNNER.md:176` (inside gate (d)'s own section) and the one citation from
outside that section anywhere in the fork —
`docs/planning/b1-sync-coverage-expansion-plan.md:189`, a plan that applied gate (d) as a phase
criterion. **The load-bearing claim survives and is now stated accurately: no *general procedure*
routes to gate (d)** — not the Planning Session Checklist, not Phase 3E, not the flight manual's
Phase 6 or Quality Gates. The b1 citation in fact *strengthens* the case: a session already used
gate (d) at plan time, informally, which is what #75 asks be required — but only because that
author already knew it existed.

Corrected in all four places it had been written: `starter-kit/FRAMEWORK_LEARNINGS.md:51`
(Learning #29 — **repair of a row this same session authored and had not yet shipped, not a later
session editing an earlier one; the append-only rule is unbroken**, and the row now carries the
error as part of its own lesson), `CHANGELOG.md`, `HANDOFFS.md`, and `bin/tests.sh:2252`.
The general failure has a name: **a grep count is a sample** — one phrasing is one sample, and
an honestly-computed count over the wrong population is uncatchable by any checker. State the
population, and the spelling, beside the number.

### 2026-08-15 · [ad hoc] S92's own receipt repaired — issue #75 was one day old, not "nine days"

Caught on re-reading, after the close-out commit `7f565d3`. The figure was never derived: #75 was
created `2026-08-14T04:17:48Z` and S92 ran 2026-08-15. Corrected in place to the filing date plus
its interval, so the claim carries its own arithmetic. Nothing else in the receipt depended on it —
the disposition (prepared fork-side, no outward action) turns on the standing rule, not on age.

### 2026-08-15 · [ad hoc] S92 close-out — receipt written, self-score 8/10, predecessor S91 scored 9/10; see the `[issue #75]` entry below for the substantive work

Claim commit `a744218` (Phase 1B), deliverable `b1b7eaf`, this close-out. **The claim stub was
written malformed and repaired in-session:** it filled `key_files`/`commit`/etc. with `pending`,
which trips `check-handoff`'s `path:line` lint — the 1B stub schema takes only `session`, `date`,
`status`, `active_task` (`starter-kit/HANDOFFS.md:26-28`). It cost 3 red rows until caught.

### 2026-08-15 · [ad hoc] `CHANGELOG.md` crossed its byte ceiling this session — measured, self-reduced as far as facts allow, and handed forward

At S92's Phase 0 this file was **62,853 B against the 65,536 B ceiling — 2,683 B of headroom against
a 1,540 B median entry.** One substantive entry plus its close-out entries exceeds that, so the
FM #28 gate fires on the first real session after S91 regardless of who runs it. S92 compacted its
own `[issue #75]` entry 3,556 → 3,156 B rather than only reporting the breach; further cuts would
delete facts, and a trim is a session-sized deliverable (S87's precedent), not a close-out side
effect. `methodology_trim.py --file CHANGELOG.md --check` reports **`[CHECK] trigger FIRES`** on
`TRIGGER_BYTES`; line headroom is fine (50 records, fires below 15). **The trim is now owed work.**

### 2026-08-15 · [ad hoc] Framework Learning #29 appended — a rule is only as reachable as the section it sits in, and its inbound-citation count says which sessions it binds

Generalized from the `[issue #75]` work below: slice gate (d) was correct, ratified doctrine with
**zero inbound citations**, reachable only by sessions that opted into a vertical slice and only
after a layer existed. Names the mechanical tell (grep the distinguishing phrase corpus-wide; one
hit = its own definition = orphan), the repair (**quote it, never restate it**, so the citation
count moves and a test can pin the quote to its source), and the half that gets missed — a rule can
also be scoped to the wrong **time**, firing after the decision it was meant to change.

### 2026-08-15 · [ad hoc] BL-39 raised — issue #75's two *Related* items, carrying the named surface forward into close-out

Phase 3E and the `runtime_smoke` receipt field both ask *did you verify?* and never *can this
surface fail?* Split from the plan-time fix deliberately, not deferred for cause: that line bites
without them, while these touch two further distributed files plus `ITERATIVE_METHODOLOGY.md`
(`:287-288`, Quality Gate 8 at `:432`), and the `runtime_smoke` half changes a documented field
format adopters' existing receipts were written against.

