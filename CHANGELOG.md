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

- `[issue #<N>]` — a repository issue. Issues for this repo live in the **upstream** parent
  `KJ5HST/methodology` (this fork has Issues disabled), so entries cite an **absolute URL**, never
  a bare `#<N>`.
- `[BL-<N>]` — a `docs/planning/BACKLOG.md` item, removed from the backlog in the same commit.
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

---

## 2026-08

### 2026-08-10 · [ad hoc] S63 close-out — receipt written, self-score 7/10; see the ledger-trim and reconcile entries below for the substantive work

**Model:** Claude Sonnet 5.
`HANDOFFS.md`'s S63 stub overwritten in place to `status: complete` with all six Minimum Handoff
Requirements. No separate substantive action beyond the receipt itself — the trim and the collateral
`commit:` reconcile it triggered are described in the sibling entries immediately below, all three
landed together in this same commit.

### 2026-08-10 · [ad hoc] Reconcile-on-read: S62's `commit:` field → `d7712ca` — 34th discharge, found via `bin/tests.sh`

**Model:** Claude Sonnet 5.
Reconciled `d7712ca` (claim stub `575a9ba`) — 34th discharge. Same mechanical shape as the 33rd:
prepending S63's own pending stub moved S62 out of "newest," so its still-`pending` `commit:` field
(the usual chicken-egg) started failing `bin/tests.sh`'s Test 25 (184/186, not the 185/186 baseline).
Found by running the full suite mid-session rather than immediately at claim — a gap against the
established S58→S59→S60→S61→S62 precedent of checking right after claiming.

### 2026-08-10 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-08-09.md` (70 record(s), 161,878 B → 15,002 B)

**Written by:** `methodology_trim.py` v1.1.1 — a tool action, not a session's judgment.
Moved the oldest **70** record(s) (2026-08-03 → 2026-08-09) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-08-09.md`](docs/archive/CHANGELOG-through-2026-08-09.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-08-09.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-09.md.verify.sh)
rather than trusting a digest printed here. Live file 161,878 B → 15,002 B (−90.7%).

### 2026-08-10 · [ad hoc] Claim S63 — lossless trim of `CHANGELOG.md` (operator-directed)

**Model:** Claude Sonnet 5.
`HANDOFFS.md`'s S63 stub prepended (`status: pending`) — Phase 1B claim, no substantive work yet.
Commit `efe5ee0`.

### 2026-08-10 · [ad hoc] S62 close-out — receipt written, self-score 8/10; see the `[issue #67]`/`[BL-26]` entries below for the substantive work

**Model:** Claude Sonnet 5.
`HANDOFFS.md`'s S62 stub overwritten in place to `status: complete` with all six Minimum Handoff
Requirements. No new substantive action in this commit beyond the receipt itself — the fix, its
ledger entry, and the BACKLOG.md update all landed in prior commits this session (`7d682fa`,
`f53f47c`), cited below.

### 2026-08-10 · [BL-26] S62 — issue #67 thread updated: IMPLEMENTED fork-side, PR #66 thread untouched

**Model:** Claude Sonnet 5.
`docs/planning/BACKLOG.md` BL-26 updated in place (not closed — this is the fork-side half only,
upstream issue #67 stays open and no PR was opened against `KJ5HST/methodology`; PR #66's own
collisions remain unaddressed and its thread is untouched). See the `[issue #67]` entry immediately
below for the implementation itself.

### 2026-08-10 · [issue #67] S62 — fork-side fix: scoped `--sync [DIR]`, `.gitignore`-aware `--force` gate, bare `--dry-run` now errors

**Model:** Claude Sonnet 5.
Implemented the ratified fork-side fix plan (`docs/planning/issue67-fork-side-fix-plan.md`, S57
proposed / S58 ratified) in full — all four fixes issue #67 names, in both
`tools/methodology_dashboard.py` and its `starter-kit/` twin (byte-identical, `diff -q` verified).
`check_stale_version()` now recommends a scoped `--sync <dir>` first; `sync_dashboards()` gained a
`target=` scope via a new order-independent `--sync [DIR]` form; a `.gitignore`-aware `--force` gate
now blocks silent overwrites of git-tracked or brand-new targets (computed before `dry_run`
branches, so `--dry-run` previews it honestly); a bare `--dry-run` is now `sys.exit(2)` instead of
a silent full scan-and-write. `DASHBOARD_VERSION` 2.13.0 → 2.14.0. 17 RED-first tests
(`TestIssue67ScopedSync`, 16 new + `test_dashboard_version` updated) — each confirmed failing
against pre-fix code before the fix landed, all green after; `bin/tests.sh` 185/186 (Test 9's
expected upstream 404, unchanged). Live-portfolio dry-run smoke test against this machine's real
13 targets confirmed the gate would have caught 11 of them previously writing unconditionally.
Fork-side only, per the plan's own §9 — no PR opened against `KJ5HST/methodology`.

### 2026-08-10 · [ad hoc] Reconcile-on-read: S61's `commit:` field → `c0e6944` — 33rd discharge, taken at Phase 0/claim

**Model:** Claude Sonnet 5.
Reconciled `c0e6944` (claim stub `6f62787`) — 33rd discharge. Surfaced by `bin/check-handoff`'s
positional exemption: prepending S62's own pending stub moved S61 out of "newest," so its
still-`pending` `commit:` field (the usual chicken-egg — the receipt ships in the commit whose sha
it would name) started failing `bin/tests.sh`. Reconciled before further work, per this repo's own
established S58→S59→S60→S61 precedent.

