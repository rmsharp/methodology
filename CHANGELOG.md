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

**Archived 26 record(s), 2026-08-15 → 2026-08-17** into [`docs/archive/CHANGELOG-through-2026-08-17.md`](docs/archive/CHANGELOG-through-2026-08-17.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-08-17.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-17.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.3.0.

**Archived 23 record(s), 2026-08-18 → 2026-08-24** into [`docs/archive/CHANGELOG-through-2026-08-24.md`](docs/archive/CHANGELOG-through-2026-08-24.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-08-24.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-24.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.3.0.

**Archived 12 record(s), 2026-08-25 → 2026-08-25** into [`docs/archive/CHANGELOG-through-2026-08-25.md`](docs/archive/CHANGELOG-through-2026-08-25.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-08-25.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-25.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.3.0.

---

## 2026-08

### 2026-08-26 · [ad hoc] S111 — Phase A (1 of 3): the false read-cap premise corrected in the three TRACKED tools

**Phase A of [`read-cap-premise-correction-plan.md`](docs/planning/read-cap-premise-correction-plan.md),
ratified by the operator at this session's Phase 1.** The claim is corrected; **no numeral moved** —
`READ_CAP_LINES` is still `2000`, `LINE_FIRE_BELOW` still `15`, `LINE_STOP_ABOVE` still `30`. Phases
B and C are explicitly not started.

**These three are `TRACKED` in `bin/_manifest.py`, so this correction reaches every existing adopter
at their next `bin/sync`** — read off the SOURCE column by importing `DISTRIBUTION`, never by
grepping the bare filename, which matches the DEST half and inverts the answer.

| file | what was false |
|---|---|
| `starter-kit/methodology_dashboard.py` | the `UNIT`/`VALUE` block, and the shipped **`high`**-severity adopter-facing risk text |
| `starter-kit/methodology_trim.py` | `READ_CAP_LINES`' own comment, and the line metric's stated raison d'être |
| `starter-kit/context_budget.py` | the docstring justifying the LINES axis *"because that is the unit an agent's read cap comes in"* |

**What replaced it — measured this session, not relayed.** Truncation is **announced, not silent**:
an over-cap read returns a `PARTIAL view` banner naming the delivered span, the true length, the
token count and the cap. It does **not** return 2,000 lines. And the cap is **token-denominated**.

**A fourth behaviour, which the plan did not know about and which settles its dragon 8.** An
explicit `limit` spanning an over-cap region **neither bypasses the cap nor truncates — it returns
an error with no content at all** (`File content (199405 tokens) exceeds maximum allowed tokens
(25000)`). The plan's stated controlled pair could not have discriminated this: it reads a file that
comes back whole either way. Run instead on a file that *does* truncate, `limit` is proved not to
bypass — so probe D's "returned whole" is **not** an artifact and §1.4's ratio range stands.

**Every corrected site names the reproduction rather than a replacement number.** §7's least
confident point is whether 25,000 tokens is stable across harness versions; a numeral would rot, the
command does not. Each site now points at Appendix A and says what it cannot prove.

**The unit argument was inverted, not deleted.** The old comment's own evidence — a ~3× B/line
spread, re-measured at **74.7** here against **227.4** next door — argues the *opposite* of what it
was written to argue, because tokens track bytes: it is a single **line** threshold that is wrong for
one ledger by 3×. Bytes are only a proxy too (2.42–2.66 B/token), so no conversion is published.

**Each site also now carries the coupling that makes the cheap fix dangerous** (BL-51): the two
thresholds are denominated in *records of headroom to this number*, so correcting it alone drives
`choose_cut` to `return 1` — one record retained at every adopter, with every test green.

**Verification.** Three Python suites **300 / 110 / 41, all OK** (4 skipped, pre-existing). Twins
**byte-identical** (`diff -q`), mirrored **last** per the plan's dragon 2. `check-links` OK (88/22).
**Seven suite assertions string-match `"read cap"` inside the risk description** and one matches
`"CHANGELOG.md is 2,090 lines"` — found *before* editing, and the replacement text was written to
keep satisfying them rather than discovered by a red suite.

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-08-25.md` (12 record(s), 65,012 B → 32,900 B)

**Written by:** `methodology_trim.py` v1.3.0 — a tool action, not a session's judgment.
Moved the oldest **12** record(s) (2026-08-25 → 2026-08-25) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-08-25.md`](docs/archive/CHANGELOG-through-2026-08-25.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-08-25.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-25.md.verify.sh)
rather than trusting a digest printed here. Live file 65,012 B → 32,900 B (−49.4%).

### 2026-08-26 · [ad hoc] S111 claim — Phase A of the read-cap premise correction

`CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in
[`HANDOFFS.md`](HANDOFFS.md). **The operator ratified `A → B → C` at Phase 1** and directed Phase A
this session; §5.4's open question is settled — *leave the design/audit records, annotate
`ledger-trimmer-design.md` only*. Deliverable: the live behaviour-claim sites in
[`read-cap-premise-correction-plan.md`](docs/planning/read-cap-premise-correction-plan.md)
§5.2/§5.3/§5.4 rewritten to state **measured behaviour and its reproduction method**, **no numeral
moved**, plus the existing-adopter remediation note §5.1 requires.

**Not in scope, each deliberately:** Phase B, Phase C, `READ_CAP_LINES`' value,
`LINE_FIRE_BELOW`/`LINE_STOP_ABOVE`, option D, the 65,536 B ceiling, `docs/archive/**` and every
frozen record (§5.5), BL-45, BL-50, issue #75's unsent PR, **and any outward-facing action**.

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [ad hoc] S110 close-out — read-cap plan delivered; self-score 8/10, predecessor S109 scored 8/10

Phase 3D receipt in [`HANDOFFS.md`](HANDOFFS.md), **12,237 B inside the 12,288 B per-record budget** —
reached in seven passes, each one run against `bin/check-handoff` rather than estimated, every cut
taken from the trailing prose where the checker says to cut. Commits: `8decf71` (1B claim) +
**`c2bc56f`** (the deliverable) + `9038e40` (the trim) + this close-out.

**Two findings this session did not set out to make, both from checking rather than reasoning.**

**BL-50 — the trimmer refuses a correct trim, and it is a distributed defect.** `insert_pointer`
(`starter-kit/methodology_trim.py:940-950`) appends `"\n" + block` when the front matter does not
already end `"\n\n"`; `L2`'s confinement proof (`:582-586`) removes only `block` and never that
injected newline, so the reversal cannot restore the original bytes and the run dies reporting a
losslessness failure **that is an artifact of its own insertion**. Reproduced in isolation — first
difference at char 6126, the tool's own number — rather than forced past. It became reachable
because S109's compaction removed the trailing pointer blocks that used to end `"\n\n"`. Worked
around with a one-byte fork-side data edit; **not** with a standalone `---`, which would trip
`[ZONE_UNCLASSIFIED]` (BL-46's failure). Learning #37 one level down.

**BL-51 — `choose_cut` makes the read-cap correction dangerous.** `stops()` has exactly one caller,
and `choose_cut` (`:876-881`) falls through to **`return 1`** when nothing satisfies it. So
correcting `READ_CAP_LINES` alone would make every adopter's next `--write` retain **one record**.
S94 measured a cut to *two* taking the suite 235/1 → 229/6 (Learning #31). Every existing test stays
green, because nothing evaluates the rate rule at a corrected cap.

**Method notes worth more than either finding.** A ratio measured on one content type does not
transfer to another — 2.419 B/token from ledger content against ≥2.62 from prose — and probe D
killed a self-consistent table this session had already drafted. **A `--check` is not a dry run:** it
returns at `:1698`, before the L1/L2/L3 machinery, so it reports a green trigger for a trim that will
refuse. And a subagent's citation is a claim: **301 reported sites, every one re-read and verified
against the file before use.**

**Phase 3C NOT discharged, and it is structural, not skipped.** `starter-kit/FRAMEWORK_LEARNINGS.md`
is **16 B** from its ceiling (BL-45) and no budget-conforming row fits. **Two learnings are earned
and owed**, both recorded in the receipt's gotchas: *a ratio is a property of its content type, not
of the corpus*, and *`--check` is not a dry run*.

**Verification.** Suite control 287 rows **286 passed / 1 failed / 0 skipped**; after the trim
287 rows, **286 / 1 / 0**; row-for-row, both populations asserted non-empty: **zero status flips,
zero skipped**, five rows differing only in a derived count the trim moved. Sole failure both sides
by name: `github source dry-run failed` (Test 9's standing 404). Trim losslessness three ways
including an independent inverter modelling the declared link-rebase transform: **6 records,
6 byte-identical, 0 unexplained**. `check-handoff` OK · `--all` OK (4) · `check-links` OK (88/22) ·
`check-learnings` OK (37) · `trim --check` silent · `context_budget.py` no file over a ceiling
(bare exit **1 = WARN**, growth run 64/10, ceiling-independent) · `BACKLOG-DETAIL.md.verify.sh` OK.

**FM #28 gate, measured after the last write.** `HANDOFFS.md` **52,808 B** (12,728 B clear), front
matter **6,362 / 7,168 B**; `CHANGELOG.md` 59,542 B *before this entry*;
`starter-kit/FRAMEWORK_LEARNINGS.md` 65,520 B (**16 B free**); `docs/planning/BACKLOG.md` 30,458 B.
`main` **61 ahead of `origin/main`**, nothing pushed.

**Carve-out re-derived by importing `DISTRIBUTION` and reading the SOURCE column** — after a first
attempt grepped the bare filename and hit the DEST half of
`("starter-kit/HANDOFFS.md", "HANDOFFS.md", SEED)`. **Nothing this session touched is a manifest
source. No adopter receives anything. No outward-facing action.**

**Open for the operator:** ratify or reject the plan's A → B → C (§7), and answer §5.4 (annotate the
design records, or leave them?). **BL-45 still blocks Phase 3C for the next session too.**

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-08-25.md` (2 record(s), 66,615 B → 44,725 B)

**Written by:** `methodology_trim.py` v1.3.0 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-08-25 → 2026-08-25) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-08-25.md`](docs/archive/HANDOFFS-through-2026-08-25.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-08-25.md.verify.sh`](docs/archive/HANDOFFS-through-2026-08-25.md.verify.sh)
rather than trusting a digest printed here. Live file 66,615 B → 44,725 B (−32.9%).

### 2026-08-26 · [ad hoc] S110 — plan delivered: correcting the read-cap premise

**The deliverable:** [`docs/planning/read-cap-premise-correction-plan.md`](docs/planning/read-cap-premise-correction-plan.md),
**DRAFT awaiting ratification.** A planning session — nothing implemented, no numeral changed, no
distributed file touched (FM #18/#19). Carve-out re-derived off `bin/_manifest.py`'s **SOURCE**
column, after a first attempt hit the DEST column and read the root ledgers as distributed: all
three files this session touched are **canonical-only**.

**Recommends A → B → C as three separate sessions, and declines the one-pass fix.**

**Three defects in one distributed constant,** separated because they have different remedies:
`READ_CAP_LINES = 2000`'s stated behaviour is false, its unit is wrong (the cap is ~25,000 **tokens**),
and its value is ~**2.9×** too permissive at this repo's ledger density.

**The finding that decided the plan's shape — no grep for `2000` reaches it.** `LINE_FIRE_BELOW = 15`
and `LINE_STOP_ABOVE = 30` are denominated in *records of headroom to the cap*. Run through the
trimmer's own `evaluate_trigger` arithmetic at both ledgers' real baselines: at a corrected cap the
rate rule **degenerates on both** — max possible headroom falls to **12** and **22** records against
a `>30` stop, so `stops()` (`byte_ok and line_ok`) can never return true. **And `stops()` has exactly
one caller.** `choose_cut` (`methodology_trim.py:876-881`) loops the retention count down and
**`return 1`** when nothing satisfies it — so the next `--write` at every adopter would retain **one
record** and archive the rest. S94 measured a cut to *two* taking `bin/tests.sh` from 235/1 to 229/6
(Learning #31); S96 corrected that to six assertions (Learning #33). **Every existing test stays
green**, because nothing evaluates the rate rule at a corrected cap.

**The structural result.** `DEFAULT_BUDGET_BYTES = 64 * 1024 = 65,536 B` sits *inside* the measured
one-read band of **60,475–66,425 B**. The framework already ships a guard on the right axis at very
nearly the right value; the line cap is a redundant second guard on the wrong axis firing ~3× late.
This answers S38's residual 1, which `methodology_dashboard.py:3001-3003` records as undecided.

**The comment's own cited basis refutes it.** `git show 3aee4e3^:CHANGELOG.md` → **2,090 lines /
186,704 B**, which is 2.8–3.1× the token cap: it had been truncating since roughly line **676–743**.
The constant records where the problem was *noticed*, not where it *starts*.

**Four probes [M], reproduction in Appendix A.** 3,000 lines returned whole; 101 lines / 199,700 B
cut at line 10 with a loud `PARTIAL view … cap 25000` banner; **2,000 lines of this repo's own
ledger content cut at line 687 of 2,001**. The fourth **falsified this session's own first draft** —
`FRAMEWORK_LEARNINGS.md` (65,520 B) returned **whole**, so the 2.419 B/token ratio does not transfer
across content types (measured range 2.42–2.66). The plan therefore prescribes the **method**, not a
new numeral.

**The inventory caught the plan itself.** Six blind search angles plus two adversarial critics;
**255 of 255 reported citations re-read and machine-verified** before use. A first draft written from
one reader's grep named 19 sites; the completed sweep found live sites in **ten further files** —
three of them **distributed seeds**, including the two that state the false claim as doctrine in a
table (`starter-kit/CHANGELOG.md:103`, `starter-kit/HANDOFFS.md:97`).

**And those two cannot be repaired by syncing.** Both are `SEED` in `bin/_manifest.py`, and
`bin/sync:225-230` writes a SEED only when the destination is absent, **never overwriting it after**.
A correction reaches **future adopters only**; every already-bootstrapped project keeps the false
doctrine permanently. That is the same defect class as BL-46/47/48 and is the substantive reason
this work batches with them.

**The surface, named per `SESSION_RUNNER.md` §Planning Sessions:** every DONE criterion is
demonstrated on the local suites — **and that surface cannot enforce the property under test.** The
three carriers are Python and cannot invoke the agent's `Read` tool; `bin/tests.sh` has **zero**
`READ_CAP` references. **No test in this repository can falsify a read-cap claim**, so each phase
requires Appendix A re-run in the implementing session, with its output in the receipt.

**Fork-side only. Nothing outward-facing.** Two open questions are left for the operator rather than
decided: whether to annotate the design records (§5.4), and ratification of A → B → C (§7).

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [ad hoc] S110 claim — plan the read-cap premise correction

`CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in
[`HANDOFFS.md`](HANDOFFS.md). **A planning session: the plan is the deliverable and nothing is
implemented** (FM #18, FM #19).

**Why now.** The operator handed over `../model_project_constructor/docs/planning/ledger-budgets-review.md`
(that repo's S248, 2026-08-26). It finds its own trim trigger's stated rationale — *"1,500 lines
(75% of the 2,000-line agent read cap)"* — false by measurement, and recommends replacing a
file-length target with a front-matter budget. **That premise is not only theirs: this repository
authors and distributes it.**

**Three probes, run here rather than relayed.** Their two reproduced exactly; the third is this
session's, and it is the one that decides whether this is a documentation defect or a real one:

| probe | file | result |
|---|---|---|
| A | 3,000 ln / 21,000 B | **returned whole** — the documented "up to 2000 lines" did not bind |
| B | 101 ln / 199,700 B | **cut at line 10**, with a `PARTIAL view … (199405 tokens, cap 25000)` banner naming the exact next call and warning not to answer from the page alone |
| C | **2,000 ln of real `CHANGELOG.md` content at this repo's own 74.8 B/line density** | **61,844 tokens against the 25,000 cap — truncated at line 687 of 2,001, 34% delivered** |

**The cap is token-denominated at 25,000, and truncation is announced, not silent.**

**The exposure is distributed, and read off `bin/_manifest.py`'s SOURCE column rather than the bare
filename.** `READ_CAP_LINES = 2000` ships to every adopter root through three TRACKED tools:
`starter-kit/methodology_trim.py:92` (headroom arithmetic at `:729`/`:809`, a refusal signal at
`:1589`), `starter-kit/methodology_dashboard.py:269` (a **high**-severity adopter-facing risk at
`:3006-3010`, the headroom metric at `:1046`), and `starter-kit/context_budget.py`'s `max_lines`
axis. Its stated justification at `starter-kit/methodology_dashboard.py:264`, republished at
`README.md:390` — *"a Read past it returns the first 2,000 lines with no error and no missing-data
marker"* — is **false in both halves**, and probe C says the number is also wrong in the unsafe
direction: at this repo's density the cliff is near line **690**, so the guard is ~**2.9×** too
permissive and a ledger at 1,999 lines passes every check while delivering a third of itself.
`tools/test_methodology_dashboard.py:3191-3193` **pins the trimmer's and the dashboard's literals to
each other**, so the two agree and are wrong together.

**Two qualifications recorded at claim so the plan cannot overstate.** (1) The practical consequence
here is **small**: truncation is *ordered* top-down and these ledgers are newest-on-top, so Phase 0's
frontier and Phase 3A's single-receipt read land inside the delivered prefix — this repo measured
whole-file reads at 1-in-81. What is wrong is the published claim and the constant's unit more than
the outcome. (2) **This repo has already arrived at the sibling document's recommendation by another
route** — S105/S109's per-record budget and `HEADER_RESERVE_BYTES` are its Options D and E, shipped.
The convergence is corroboration, not a new finding.

**Also standing at claim, neither of them this session's deliverable.** `HANDOFFS.md` is 62,717 B
with **2,819 B clear**, so this session's close-out receipt breaches the ceiling while `--check`
still reports *trigger does not fire* — confirmed silent at this Orient, exactly as S109 predicted.
The trim is **close-out housekeeping**, not a second capability. And `starter-kit/FRAMEWORK_LEARNINGS.md`
is **16 B** from its ceiling, so **Phase 3C cannot be discharged without the operator's BL-45 decision.**

**What does NOT change:** anything implemented, `RECORD_BUDGET_BYTES`, the 65,536 B ceiling, Test
34's floor of 3, and every historical statement of the 2,000-line cap in this ledger and in the
frozen shards, which are records of what was believed when written (FM #22).
**Fork-side only. Nothing outward-facing** — the fix batches with BL-46(2)/47/48/49 for one later PR.

**Model:** Claude Opus 5 (1M context).

### 2026-08-26 · [BL-46] Cross-repo: BL-46's half (1) closed by the adopter, and its remedy shown too narrow — BL-47/48/49 raised

**Written by:** a session running in `../vscode_quarto_ext` (its S254/S255), acting on that repo's
operator directive. **No distributed file in this repository was touched** — this is a backlog
filing plus this ledger entry. Nothing outward-facing; nothing pushed.

**BL-46 half (1) is DONE.** That repo deleted the blocking footer and ran both overdue trims:
`CHANGELOG.md` **831,830 → 44,190 B** (230 records archived), `HANDOFFS.md` **1,801,150 → 52,850 B**
(211 receipts). Both triggers now stand down. Losslessness established four ways — the tool's
in-process L1/L2/L3+P1A, its emitted `verify.sh`, an independent verifier sharing no code with it,
and a four-lens adversarial pass tasked with *refuting* the claim, which found none.

⚠ **BL-46's DIAGNOSIS IS RIGHT AND ITS PROPOSED DETECTOR WOULD NOT HAVE FIRED.** BL-46 says the
adopter *"never deleted"* the seed sentinel. They **had** deleted it — `METHODOLOGY-SEED-SENTINEL`
was already absent — and the trimmer refused anyway, because what blocks it is the **trailing `---`
and the comment below it**, which the seed's instruction never mentions. `starter-kit/HANDOFFS.md`
carries the sentinel at line 20 and, at line 160, an instruction reading only *"Delete the
seed-sentinel line above"*. **An adopter who follows it exactly still ends up with an inert
trimmer** — which is what happened, for 216 receipts. BL-46's proposed check keys on the sentinel;
it must key on the footer, or the seed must instruct removing both. Annotated in place.

**Three items raised, none duplicating anything here (checked before filing):**
- **BL-47** — the seed `context-budget.json` omits `CHANGELOG.md`/`HANDOFFS.md`, the two files
  `methodology_trim.py` exists to bound, at the 65,536 B constant both tools already share. This is
  BL-46 one level up: BL-46 asks why nobody read the trimmer's output; this is why. That adopter had
  the trimmer since S188 and `context_budget.py` **not at all** until S255.
- **BL-48** — the seed `HANDOFFS.md` lacks the `This file currently holds **N**` sentence its own
  `LedgerSpec.regenerated` declares, so every adopter gets `FRONTMATTER_FIELD_ABSENT` on every trim,
  forever. This repo's root copy *has* the sentence, so the mismatch is invisible from here.
- **BL-49** — `content_probe` is consulted at exactly one call site, `classify_empty`, so a
  **partial** grammar mismatch is never tested. Measured consequence: that repo's `CHANGELOG.md`
  holds 236 dated `###` headings and 230 matched records (six predate its source-tagging
  convention), so a **frozen** shard is published in four places as spanning from `2026-06-30` when
  its true oldest entry is `2026-06-27`. Every L1/L2/L3 assertion passes — nothing is lost, only the
  *description* is wrong, and the description is the index people search.

**Also confirmed from the adopter side:** **BL-27's fix works.** Syncing that repo `v1.1.1 → v1.3.0`
and regenerating its `HANDOFFS` shard proof turned `FAIL: L2 FRONT MATTER lost 1 line(s)` into `OK`.

**Verification:** `docs/planning/BACKLOG-DETAIL.md.verify.sh` **OK** — C1–C5 green, 18 split items
still byte-identical, new items correctly reported as raised-since and not a finding.

