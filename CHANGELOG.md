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

**Archived 65 record(s), 2026-09-02 → 2026-09-14** into [`docs/archive/CHANGELOG-through-2026-09-14.md`](docs/archive/CHANGELOG-through-2026-09-14.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/CHANGELOG-through-2026-09-14.md.verify.sh`](docs/archive/CHANGELOG-through-2026-09-14.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

---

## 2026-09

### 2026-09-16 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-16.md` (6 record(s), 75,185 B → 20,820 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **6** record(s) (2026-09-15 → 2026-09-16) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-16.md`](docs/archive/HANDOFFS-through-2026-09-16.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-16.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-16.md.verify.sh)
rather than trusting a digest printed here. Live file 75,185 B → 20,820 B (−72.3%).

### 2026-09-16 · [ad hoc] S172 follow-up — fork `main` pushed to `origin`, `1d88eaa..ef83601` (non-commit action, operator go-ahead)

- **Action:** `git push origin main` on the operator's explicit go-ahead — **27 commits**,
  `1d88eaa..ef83601`, a fast-forward (0 behind before the push). To **`rmsharp/methodology`**, the
  fork. **Nothing went to `KJ5HST/methodology`;** upstream is untouched and still needs its own
  go-ahead for anything.
- **Read back from the remote, not from the push output.** `git ls-remote origin refs/heads/main`
  returns `ef836018398ee59b709a8d164b6cb3c978237d94`, identical to local `main` — the remote's own
  answer rather than a cached tracking ref or the transcript of the push.
- **What became public:** this session's whole arc — BL-57's P3 record and plan amendment, BL-59 and
  its correction, the Test 38 fixture decoupling, the `HANDOFFS.md` trim to one receipt with its
  shard and proof, the density recalibration, and three receipt corrections.
- **Still on no remote:** branch `bl57/changelog-rules` at `18962a9`, which carries P3's four
  commits. Backing it up is its own go-ahead and was not given here.
- **Commit/PR:** the push itself left no commit; this entry is its record
- **Session:** S172 · **Verified:** `git rev-list --count origin/main..main` = 0 after the fetch;
  `ls-remote` sha matches local `main` exactly.
- **Model:** Claude Opus 5

### 2026-09-16 · [ad hoc] S172 follow-up — the receipt's `NOT EXERCISED` list still named the retention trim

- **What was wrong:** S172's `runtime_smoke` listed *"the `HANDOFFS.md` retention trim"* among the
  things the session did not exercise. True when written; false from `1ec509d` onward, and this is
  the one receipt the next session reads in full.
- **Change:** the trim moves out of that list into an `EXERCISED AFTER CLOSE-OUT, NOT AT IT` clause
  naming its commit. The distinction is kept rather than erased: the trim was operator-directed
  follow-up, not part of the close-out the receipt attests to.
- **This is the third stale claim this session's own receipt has needed correcting** — the unpushed
  commit count, `next_steps` item (2), and now this. All three share a shape: a receipt states the
  world as of close-out, and work continued afterwards. The first was fixed by naming a command
  instead of a number; these two could not be, because they are statements about what happened.
- **Commit/PR:** this commit
- **Session:** S172 · **Verified:** `bin/check-handoff --all` exit 0 (1 receipt).
- **Model:** Claude Opus 5

### 2026-09-16 · [BL-59] S172 — `HANDOFFS.md`'s token density re-measured after the trim; the budget row goes green

- **Change:** `.context-budget.json`'s `HANDOFFS.md` entry moves from `bytes_per_token` **2.3648**
  (measured 2026-08-29 at **186,617 B**) to **2.2657** (measured today at **20,310 B**). The tool
  itself asked: after the trim it reported *"density ... was measured at 186,617 B; the file is now
  20,310 B (89% drift). The token figure above is provisional — re-measure before trusting it."*
- **Measured, not derived.** The quadrupled-file Read refused at **35,857 tokens**, so the live file
  is **8,964.25 tokens** at 20,310 B. The stale density would have reported 8,588 — under-reporting by
  376 tokens, about 4.4%. Neither figure changes the verdict against a 25,000-token ceiling, so this
  is precision, not rescue.
- **The row is now `ok`.** At Phase 0 it read **over by 2,446 tokens**; it is green on both arms.
  Learning #60 is why this was worth doing now rather than later: a density is a snapshot of the
  content a file held when measured, and this file's composition changed character completely — one
  receipt plus front matter, where front matter is now 35% of it.
- **Two mistakes on the way in, both caught by asserts rather than by the diff.** A first patch
  assumed six-space JSON indentation and matched nothing (the file uses three); the replacement then
  had to key on line numbers because `"measured_on": "2026-08-29"` appears three times, once per
  budgeted file. A pattern edit would have rewritten the wrong entry silently.
- **Commit/PR:** this commit
- **Session:** S172 · **Verified:** `context_budget.py --status` reports `HANDOFFS.md ... ok`; the
  config re-parses as JSON and the parsed entry is asserted to carry the new values.
- **Model:** Claude Opus 5

### 2026-09-16 · [BL-59] S172 — `HANDOFFS.md` retention is now N=1: the fold, the policy, and a header reserve that is spent

- **Change:** the trim's pointer block is folded into the archive table as one row — in its own
  commit, because inside the trim commit the shipped `.verify.sh` fails L2 (Learning #58). The
  retention paragraph now states **N=1, replacing S127's N=4**, with the measurement it rests on and
  the reason `--force` is warranted rather than an override. The live ledger holds **one receipt**,
  20,820 B against 75,185 B before.
- **The retained receipt was corrected in place.** Its `next_steps` item (2) said this file held
  *"seven receipts against a retention policy of four"* — false the moment the trim landed, and it is
  the one receipt the next session reads. It now records what happened, including the test fix N=1
  required. Precedent for correcting a receipt in a follow-up rather than editing history: `1d88eaa`.
- **A consequence the decision did not anticipate, and it is now the binding constraint.** **N=1
  means a trim EVERY session** — each close-out prepends a receipt, so the steady state is exceeded
  immediately. Each trim-and-fold adds one archive-table row, about **147 B** of the **7,168 B**
  header reserve `bin/tests.sh` Test 39 (A2) asserts on this front matter. After this fold the front
  matter is **7,107 B — 61 B of room, which is room for none.** The next trimming session must
  shorten it first; folding the archive table into a shard index of its own is the obvious cut, and
  it is recorded in BL-59 rather than left to be rediscovered.
- **Three passes were needed to write that warning, which is the finding in miniature:** every
  version long enough to explain the problem was long enough to cause it — the first pushed the front
  matter to 7,718 B (over by 550), the second to 7,220 B (over by 52). The reasoning moved to BL-59
  and the instruction stayed here, which is the same move §The Action Ledger prescribes for a rule
  that outgrows the file it is stated in.
- **Commit/PR:** this commit; the trim is `1ec509d`, the test fix `d13a165`
- **Session:** S172 · **Verified:** `bash bin/tests.sh` exit 0 — **300 passed, 0 failed, 6 skipped**;
  the six are Test 34's stated BL-40 rows, which want three receipts, and Test 38 no longer degrades
  because `d13a165` decoupled it. `bin/check-handoff --all` exit 0 (1 receipt); `bin/check-links`
  exit 0; the shard's `.verify.sh` exit 0 both before and after the trim commit.
- **Model:** Claude Opus 5

### 2026-09-16 · [BL-59] S172 — Test 38 reads a frozen fixture instead of the live ledger, and a drift guard keeps the fixture honest

- **Change:** `bin/tests.sh` Test 38 sourced its fixture from the live root `HANDOFFS.md`, which made
  its inputs a function of a **retention policy**: at one retained receipt the copy exits
  `FIXTURE SOURCE TOO SHORT` and all thirteen assertions error with *"handoff file not found"* — 14
  failures, measured. It now reads **`tools/fixtures/handoff-ledger-2-records.md`** (2,985 B), a
  frozen two-record ledger: one record to pad past the 12,288 B per-record budget so assertion (4)
  is armed, one to be the subject of every other assertion. The three comments that asserted the old
  provenance (*"the fixture is a copy of the live ledger"*) are corrected rather than left standing.
- **The live half was kept, because a frozen fixture cannot notice the format moving.** New
  assertion **(8)**, a drift guard: it reads the **live** ledger's newest receipt and the fixture's,
  and fails if the live one carries a field the fixture lacks. **Mutation-tested in both directions
  before it was trusted** — deleting `gotchas` from the fixture reports `gotchas`; deleting two
  reports both; adding a key to a live receipt reports that key; the unmutated control reports `OK`.
- **Why a split and not a move:** the budget assertions want a population the test controls; the
  format check wants the real artifact. Each now runs against the one it needs.
- **Fork-local, verified rather than assumed.** Test 38 does not exist upstream — `grep -q` on the
  branch's `bin/tests.sh` exits 1 while fork `main` exits 0, read bare — and neither `tools/` nor
  `bin/tests.sh` has a row in `bin/_manifest.py` (both appear there only inside comments, which is
  why a bare `grep -c` on the filename answers the wrong question). No adopter receives either.
- **Commit/PR:** this commit
- **Session:** S172 · **Verified:** `bash bin/tests.sh` exit 0 — **306 passed, 0 failed, 0 skipped**,
  against a 305/0/0 baseline; the one added test is the drift guard. `bin/check-handoff --file
  tools/fixtures/handoff-ledger-2-records.md --allow-pending` reports OK and
  `record budget: 0 unwritten record(s), 0 over 12,288 B` — the two strings Test 38's control greps.
- **Model:** Claude Opus 5

### 2026-09-16 · [BL-59] S172 follow-up — the operator decides N=1; measured, the reachable floor is 2, and BL-59's first draft was wrong about why

- **Decision recorded:** the operator set `HANDOFFS.md` retention to **1**. **Nothing was trimmed** —
  executing it was tried in a throwaway clone first, and the result sends the decision back.
- **What the experiment found, run rather than predicted.** Baseline 7 receipts: `bin/tests.sh`
  exit 0, 305 passed / 0 failed / 0 skipped. At **`--cut 1`: exit 1, 285 passed, 14 failed**, 6
  skipped. At **`--cut 2`: exit 1, 298 passed, 1 failed**, 6 skipped — and **after the fold the
  prescribed next step, exit 0, 299 passed, 0 failed, 6 skipped.**
- **BL-59's first draft was wrong and is corrected.** It said the only cost below three receipts was
  six stated `SKIP` rows, *"never a failure."* **The real floor is Test 38, which this item had not
  mentioned at all:** it copies the live ledger into a temp fixture and exits
  `FIXTURE SOURCE TOO SHORT: need >= 2 records, found 1` (`bin/tests.sh:2752`), after which 13
  assertions error with *"handoff file not found"*. Test 34's six skips are the tolerable part.
- **A second constraint binds at any depth.** Test 39's A2 gives the live front matter a 7,168 B
  reserve; a trim's ~448 B pointer block takes it to 7,440 B (**over by 272**) and the fold replaces
  that block with one table row at **7,139 B (under by 29)** — measured, and the fold must be its own
  commit (Learning #58). **29 B of headroom means the trim after this one overflows the reserve**,
  which S169 predicted and which argues for cutting deep once rather than shallow repeatedly.
- **The `--force` warrant, checked rather than assumed:** `--check` reports SRF 2.0244 (RED), but
  §11.1 of the SRF adjudication proves **every on-schedule retention trim is refused for any file at
  any depth** — the refusal votes with the most recent archive, an unratified addition on top of H3.
  H3 as written votes with the largest single drop, printed in the same report: **0.1016**, deep green.
- **Measured cost:** `--cut 1` takes the live file 75,185 → 20,820 B with the repo net **+17,014 B
  (1.226×)** — far cheaper per byte relieved than S171's trim-to-four estimate, because the ~16 KB
  proof is a fixed cost. `--cut 2` takes it to 30,760 B. L1/L2/L3 OK; the emitted `.verify.sh` exits 0.
- **Also confirmed by running it:** `bin/model-report` opens the live ledger **and every archived
  `HANDOFFS-*` shard**, and today finds **0 matched lines in the live file** against matches in ten
  shards — so the one consumer of historical receipt content already reads the archives, not the
  live file. Archiving costs it nothing, which was the load-bearing claim under the whole decision.
- **Commit/PR:** this commit
- **Session:** S172 · **Verified:** all four suite runs in a `--no-local` clone whose HEAD sha was
  asserted equal to the working tree's (`dd18114`); `bin/check-handoff --all` exit 0 throughout.
- **Model:** Claude Opus 5

### 2026-09-16 · [ad hoc] S172 follow-up — BL-59 raised on the operator's question: does `HANDOFFS.md` need to keep four receipts?

- **Change:** BL-59 raised in `docs/planning/BACKLOG-DETAIL.md` with an index row in
  `docs/planning/BACKLOG.md`. The operator asked why the receipt ledger grows when the handoff is
  only used between two sessions, and whether `CHANGELOG.md` or `BACKLOG.md` could take the proof
  half. **The premise holds:** the file does two jobs with opposite retention needs — the *handoff*,
  done by the newest receipt alone, and the *proof*, which is what makes it append-only.
- **All five consumers were checked rather than assumed.** Only `bin/model-report` reads the content
  of a receipt below the newest, and it discovers archive shards by glob (`bin/model-report:158`), so
  archiving costs it nothing; `bin/check-handoff --archived` validates a frozen shard, so the
  integrity scope survives too. **Nothing requires an old receipt to be in the live file.** The
  number is an operator decision, as the file's own front matter says, and the S127 warrant
  (`docs/archive/CHANGELOG-through-2026-09-02.md:2070`) justifies the trim, never the four.
- **Measured at this session's close-out:** 75,185 B across 7 receipts — front matter 9.3%, the
  newest receipt 17.8%, **spent receipts 72.9%** — and **6,793 tokens over the 25,000-token ceiling**.
  S171 costed the same decision in bytes alone, where it read as a preference; in tokens it is a
  red gate.
- **The second question answered in the item:** `BACKLOG.md` cannot take the proof job at all (it
  holds open work only, and completion *removes* an item). `CHANGELOG.md` already carries the
  *occurrence* proof and the duplication is real — but it cannot carry the `pending`→`complete` crash
  breadcrumb (the only one this repo has, having no `SESSION_NOTES.md`), the 13-key schema that makes
  the six Minimum Handoff Requirements checkable, or per-session granularity. So it proves close-out
  *happened*, never that the handoff was *complete*.
- **One citation in the item was wrong and was corrected before commit.** The fixture precedent
  `tools/fixtures/seed-CHANGELOG-ledger-format-1.md` was cited as present; `git rev-parse` finds it on
  branch `bl57/changelog-rules` only, on neither fork `main` nor `upstream/main`. The item now says so.
- **Nothing was decided and nothing distributed was touched** — the retention number, Test 34's
  fixture split and a retention mode for `methodology_trim.py` are all left to the operator, and the
  last is a distributed change needing its own go-ahead.
- **Commit/PR:** this commit
- **Session:** S172 · **Verified:** every cited destination re-read on the ref the item claims it on;
  `bin/check-handoff --all` exit 0 (7 receipts); fork-only files, no distributed file changed.
- **Model:** Claude Opus 5

### 2026-09-16 · [ad hoc] S172 follow-up — the unpushed-commit count replaced by the command that produces it

- **Why the previous entry did not settle it:** the correction from 17 to 18 was committed, and that
  commit made the answer 19. **A count of unpushed commits cannot be written into a file inside the
  repository it counts** — recording it is itself one of the commits, so every fix falsifies the
  figure it just wrote. Two sessions' worth of this is avoidable in one line.
- **Change:** the receipt's carried item now names the command,
  `git rev-list --count origin/main..main`, instead of a number, and says why. This is
  §The Action Ledger's own advice — *replace a hand-maintained count with the command that produces
  it* — applied to the file that advises it.
- **Commit/PR:** this commit
- **Session:** S172 · **Verified:** `bin/check-handoff --all` exit 0, 7 receipts; the receipt now
  contains no commit-count figure (`grep -c 'commits ahead of' HANDOFFS.md` finds none in S172's block).
- **Model:** Claude Opus 5

### 2026-09-16 · [ad hoc] S172 follow-up — the receipt's unpushed-commit count corrected, 17 to 18

- **What was wrong:** S172's receipt gave fork `main` as *"17 commits ahead of `origin/main`"* under
  its carried go-ahead items. The figure was computed before the close-out commit and stated without
  the qualifier that would have made it true, so as a description of the tree the next session finds
  it is short by one. Measured after the close-out: `git rev-list --count origin/main..main` = **18**.
- **Change:** the receipt now reads 18 and says when it was counted. Nothing else in the receipt
  moved. Precedent for correcting a receipt in a follow-up commit rather than in place: `1d88eaa`.
- **Commit/PR:** this commit
- **Session:** S172 · **Verified:** `git rev-list --count origin/main..main` re-run after this commit
  is staged returns 18; `bin/check-handoff --all` exit 0, 7 receipts.
- **Model:** Claude Opus 5

### 2026-09-16 · [BL-57] S172 close-out — P3 done, the size rule now in tokens, and a measurement three handoffs called outstanding was already taken

- **Change:** S172's receipt is completed in `HANDOFFS.md` (self 8/10, predecessor S171 8/10). The
  deliverable was BL-57's P3 on branch `bl57/changelog-rules` — four commits, not pushed — plus the
  plan amendment on fork `main` that discharges S169's instruction to restate P3's and P4's runner
  criteria in tokens.
- **The restated criterion caught its own session.** The first edit measured **+9 tokens** against a
  rule this session had just rewritten. The fix went into the edit, not the rule: two clauses
  duplicated elsewhere on the same step came out, and the runner ended **32 B and 14 tokens under
  where P3 started**. A session that restates the gate binding it is grading its own paper, and the
  only defence is to take the measurement afterwards and let it fail.
- **`b82dcff`, `upstream/main` and P3's start are one blob (`c0550acd`).** So S169's recorded control
  *"`main`'s runner 36,955"* **was** the baseline the last three handoffs each carried forward as an
  unmeasured item. Two `git rev-parse` calls closed it.
- **Two figures the plan said would be findings if they moved, both explained to the entry that
  caused them.** Four of six adopters reproduce §4.4 exactly; `airqino` 1→2 and `mts-system` 96→262
  each gained one entry dated 2026-09-15. This repo reads **556** against §4.4's 494 — and **494 is
  exactly the count of entries dated on or before 2026-09-14**, §4.4's measurement date, so the
  twelfth shard S171 wrote moved nothing out of the audit's reach. Conservation measured, not assumed.
- **One defect was found in this session's own text, at close-out, and corrected on the branch
  (`18962a9`).** §The Action Ledger attributed the *78 against 64* count to *"this framework's own
  ledger"* — but that comparison was run on the project whose ledger was split at v3.6, and the tree
  the sentence now ships in records none of it. Every gate passed it; a grep for the figure's
  provenance did not. The sentence leads with the mechanism now and names the figure for what it is.
- **No learning row, deliberately.** The candidate rule is already carried by rows #46 and #60, and
  `starter-kit/FRAMEWORK_LEARNINGS.md` is 79,483 of 81,920 B with about two rows left under BL-53's
  unresolved retirement policy.
- **`HANDOFFS.md` now holds seven receipts against a retention policy of four,** and the decision
  S171 deferred is sharper in tokens than in bytes: `context_budget.py --status` reports it
  **≈27,446 tokens against a 25,000-token ceiling, over by 2,446.** Cutting to four removes 26,140 B
  of body, leaving ≈16,393 tokens — red to 8,600 tokens of headroom. Still the operator's call.
- **Commit/PR:** this commit (fork `main`)
- **Session:** S172 · **Verified:** in `--no-local` clones with HEAD shas asserted — branch `cf20a3b`
  and again `18962a9`, `bin/tests.sh` **118/0**, `check-links` 0 (**108** links, 107 at `775ba23`),
  budget 0, `grep -F '[BL-<N>]'` exit 1 over all seven files; fork `main`
  `44a1e20` `bin/tests.sh` **305 passed / 0 failed / 0 skipped**, `check-links` 0, `check-learnings` 0,
  `check-handoff --all` 0, budget exit 2 with **0 status flips** against the Phase 0 reading.
- **Model:** Claude Opus 5

### 2026-09-16 · [BL-57] S172 — BL-57's P3 done on branch `bl57/changelog-rules` (3 commits, not pushed); the plan amended and its size rule restated in tokens

- **Change:** P3 ran on the branch as it stood — upstream PR #82 was re-checked at Phase 0 and is
  still OPEN at `c84e7d96`, so S169's merge-first amendment did not trigger. Branch commits:
  `d771439` rewrites `FRAMEWORK_APPARATUS.md` §The Action Ledger's source-tag vocabulary to
  `[BL-<id>]` and replaces the one-line audit with the anchored, shard-reading, `git ls-files` form;
  `e47ca14` drops the runner's inline audit grep at `:39` for a link to that section and moves
  `:278`, `:329`, `ITERATIVE_METHODOLOGY.md:294` and `.githooks/pre-commit:57` to `[BL-<id>]`;
  `cf20a3b` replaces the `HANDOFFS.md` seed's bare glob with `git ls-files` — the bullet P2 left to
  P3. On fork `main`: this entry, the plan's S172 amendment and BL-57's backlog row.
- **S169's amendment is discharged.** P3's and P4's runner criteria were written in bytes; both are
  now in tokens at `docs/planning/changelog-rules-contradictions-plan.md`. **The measurement came
  first and its instrument was checked first:** both published controls reproduced exactly — the
  runner doubled to **36,955** (18,477.5 tokens) and the Phase 0 pair to **48,555** (24,277.5), the
  figures S169 recorded, on the same blob `c0550acd` that is both P3's start and `b82dcff`'s file.
- **The two units disagreed, which is the point.** The link plus the id changes measured **+36 B but
  only +9 tokens** — a path runs near 4 B/token where the runner averages 2.8248. Two duplicate
  clauses on the same step then came out (the step already showed `[ad hoc]` in its own template;
  the note's closing paragraph already forbids the backfill becoming the deliverable), leaving the
  runner at **52,163 B / 18,463.5 tokens — 32 B and 14 tokens under where P3 started**, and the pair
  at 24,263.5 of the 25,000-token read cap.
- **Every DONE criterion was run, not predicted.** `grep -F '[BL-<N>]'` over the runner, the flight
  manual, `HOW_TO_USE.md`, the hook, §The Action Ledger and both seeds exits 1 (no matches). The
  audit returns the same number in zsh and bash on the branch (57, equal to its heading count), on
  this repo (556) and on all six adopters. In a throwaway repository with one entry and no shard the
  **bare glob makes the two shells disagree — zsh prints 0, bash prints 1** — while the `git ls-files`
  form prints 1 and exits 0 in both; that is the failure the fix removes, and it is a wrong number
  rather than a visible error.
- **Two §4.4 figures moved and both are explained.** Four of six adopters reproduce exactly;
  `airqino` 1→2 and `mts-system` 96→262 each gained one entry dated 2026-09-15. This repo reads 556
  against §4.4's 494 — and **494 is exactly the count of entries dated on or before 2026-09-14**, its
  measurement date, so S171's 12th shard moved nothing out of the audit's reach. Widening
  `BL-[0-9]+` to `BL-[^]]+` recovers **362 logged actions** across three adopters.
- **Commit/PR:** this commit (fork `main`); branch `d771439` + `e47ca14` + `cf20a3b`
- **Session:** S172 · **Verified:** in a `--no-local` clone whose HEAD sha was asserted equal to the
  worktree's (`cf20a3b` both sides), `bin/tests.sh` **118 passed / 0 failed**, `bin/check-links` 0
  (**108** links, 23 files — 107 at `775ba23`, the one link P3 added), `context_budget.py --status` 0.
- **Model:** Claude Opus 5

### 2026-09-16 · [BL-57] S172 claim — BL-57's P3: source tags and the audit, on the branch

**Deliverable:** BL-57's **P3** (`docs/planning/changelog-rules-contradictions-plan.md:490`) on branch
`bl57/changelog-rules` (worktree `../methodology-bl57`, at `775ba238`): `[BL-<N>]` becomes `[BL-<id>]`,
and the source-tag audit becomes the shard-reading form that gives the same count in zsh and bash — in
`FRAMEWORK_APPARATUS.md` §The Action Ledger, `starter-kit/SESSION_RUNNER.md` (`:39`, `:278`, `:329`),
`ITERATIVE_METHODOLOGY.md:294` and `.githooks/pre-commit:57`.

- **Upstream PR #82 is still OPEN at `c84e7d96`**, re-checked at Phase 0 rather than assumed, so S169's
  merge-first amendment does **not** trigger: P3 starts on the branch as it stands.
- **Two carried items ride with P3.** P2 found that the `HANDOFFS.md` seed still publishes a bare glob
  zsh refuses where no shard exists — C10's class, outside P2's lines, assigned to P3. And S169's
  amendment holds: P3's runner criterion (`:508`) and P4's (`:538`) are written in **bytes** and must be
  restated in **tokens**. That measurement has not been taken, so it comes first.
- **Riding with this claim:** the Phase 0 `dashboard_history.jsonl` and `.context-budget-history.jsonl`
  snapshots, both appended by mandatory Phase 0 instrument runs. They are recorded here and committed
  with this entry rather than left for a later `--no-verify` — S171's finding, applied at the one point
  in the session where it costs nothing.

**Ledger:** `CHANGELOG: pending` — the crash breadcrumb until Phase 3F.

### 2026-09-16 · [ad hoc] S171 follow-up — the append-only `.context-budget-history.jsonl`, dirtied by Phase 3E

A bare `context_budget.py --status` appends to its own run history, so Phase 3E left the file modified
after the close-out commit. Recorded here and committed with this entry rather than with `--no-verify`:
this session's one finding was that an unrecorded housekeeping commit is a debt the next frontier-advancing
action makes permanent, and leaving one behind in the close-out would be the same mistake twice.

### 2026-09-16 · [ad hoc] S171 close-out — `CHANGELOG.md` readable again, measured as a transfer and not a saving

- **Change:** S171's receipt is completed in `HANDOFFS.md` (self 7/10, predecessor S170 9/10). The session
  did two things on the operator's instruction: trimmed this file under approved `--force` (the tool's own
  entry below) and raised **BL-58** (the entry below that). **The trim's net was projected before the run
  and measured after: +17,928 B projected, +18,138 B actual (1.102×)** — relief 178,162 B against
  196,300 B written, so the repository grew while the read path shrank, and this ledger says so rather
  than crediting a saving. `docs/archive/` is now **42.8% of the tracked repo**, inside no ceiling.
  **The benefit is exactly one thing and is not the context budget:** `CHANGELOG.md` is a deliberate
  exclusion from the read-set, so `context_budget.py --status` is byte-for-byte unmoved by the trim
  (69,749 B, `over`, exit 2) — what changed is that a default `Read` returned **zero content** before and
  the front matter plus the newest ~51% with an announced `PARTIAL view` banner after. The file's own
  rate rule moved **−67 → +33 entries of headroom**, clearing its published *"back above 30"* stop.
- **Found, and self-inflicted:** the `chore(history)` commit `c01854f` was made `--no-verify` **before**
  the trim and tripped the trimmer's `P1_UNDOCUMENTED` guard. The guard is right — a trim advances
  `git log -1 --format=%H -- CHANGELOG.md`, so the commit would have been unrecoverable by Phase 0
  reconcile — and the usual discharge, naming such a commit in the close-out entry, comes too late.
  `f2840fc` records it instead. **S152's trim put its `chore(history)` after the trim; that precedent had
  been read minutes earlier.**
- **Not done, deliberately and with a number:** `HANDOFFS.md` holds **six** receipts against its retention
  policy of four. Its byte trigger does not fire (54,177 B of 196,608), so a retention trim would relieve
  ~18 KB and write a fixed ~16 KB proof — **roughly 1.9× net-additive**, the expensive end of the curve
  measured today. That is an operator decision, not Phase 0 housekeeping, and S172 should put it as one.
- **No learning row.** `starter-kit/FRAMEWORK_LEARNINGS.md` is 79,483 of 81,920 B with about two rows
  left and **BL-53's retirement policy still open**; the transferable content of this session is recorded
  in BL-58's eight hazards, where it is useful to adopters rather than competing for the last rows.
- **Commit/PR:** this commit (claim `ff29a8d`, history `c01854f`, reconcile `f2840fc`, trim `101fa78`,
  BL-58 `1c4e941`)
- **Session:** S171 · **Verified:** in a `--no-local` clone with HEAD asserted equal (`1c4e941` both
  sides), `bin/tests.sh` **305 passed / 0 failed / 0 skipped**, matching the S168–S170 controls; dashboard
  321 OK, trimmer 123 OK, budget 116 OK; `check-links` 0, `check-learnings` 0, `check-handoff --all` 0
  read bare; `context_budget.py --status` exit 2 with 0 status flips against the Phase 0 reading and
  exactly two rows moved, both by this session's own writes; the shard's `.verify.sh` exit 0 twice, before
  and after the trim commit. **The suite run was reported by the harness as exit 1; the chain's own
  echoed code was `tests.sh exit=0` and the 1 belonged to a trailing `grep -c` matching zero SKIP lines.**
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [ad hoc] S171 — BL-58 raised on the operator's request: should adopters be told how to trim a ledger losslessly?

**Change:** `docs/planning/BACKLOG.md` gains the index row and open-list entry; the body is in
`BACKLOG-DETAIL.md` under `<a id="bl-58"></a>`. **The gap is measured, not asserted:** `bin/_manifest.py`
installs `methodology_trim.py` at every adopter root as a **tracked** file, while `grep -ciE 'trim'`
returns **0** for `starter-kit/SESSION_RUNNER.md`, `FRAMEWORK_APPARATUS.md` and `starter-kit/SAFEGUARDS.md`
— so the only real instructions sit in the two **seeds** `bin/sync` never overwrites once they exist, and
the one file every session reads says nothing. The item lists eight operating hazards, **four of them hit
by this session**: the tool stages nothing (commit with `-a` and the shard never enters history);
`P1_UNDOCUMENTED` demands the reconcile happen *before* the trim, because the usual discharge — naming a
`--no-verify` commit at close-out — comes too late; the proof reads differently either side of the commit;
and `SRF_RED` is a property of the rule, not of the file. It is framed as a **decision first**, with three
uncosted shapes: the tracked apparatus beside BL-57's P2 section, a procedure in the runner (expensive —
the runner is 54,363 B against a 41,364 B declared ceiling), or better output from the tool itself.
**One stale figure was caught before it was published:** the *"net +144,239 B across ten archive events"*
accounting is S124's and covers only the first ten, so the entry attributes it and says to re-derive rather
than quote it.

- **Commit/PR:** this commit
- **Session:** S171 · **Verified:** the disposition and install path read from `bin/_manifest.py`
  directly; each `grep -ciE 'trim'` count run per file; the proof-cost percentages and the 40.6%
  archive share re-measured this session
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-16 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-09-14.md` (65 record(s), 276,657 B → 98,495 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **65** record(s) (2026-09-02 → 2026-09-14) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-09-14.md`](docs/archive/CHANGELOG-through-2026-09-14.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-09-14.md.verify.sh`](docs/archive/CHANGELOG-through-2026-09-14.md.verify.sh)
rather than trusting a digest printed here. Live file 276,657 B → 98,495 B (−64.4%).

### 2026-09-16 · [ad hoc] S171 — `c01854f` recorded before the trim advances the ledger frontier

A `chore(history)` commit for the two append-only `.jsonl` run series that Phase 0's dashboard and
`context_budget.py` runs appended to. It was committed `--no-verify` and so carried no ledger line of
its own, which past sessions have discharged by naming such commits in the close-out entry instead.
**That is not available here:** `methodology_trim.py`'s `P1_UNDOCUMENTED` guard refused the trim while
it stood unrecorded, and the refusal is right — a trim commit advances `git log -1 -- CHANGELOG.md`,
so `<frontier>..HEAD` would never contain `c01854f` again and Phase 0 reconcile could not recover it.
Recorded here, before the trim, rather than at close-out after it.

### 2026-09-16 · [ad hoc] S171 claim — trim `CHANGELOG.md` back under the hard read refusal, on operator go-ahead

**Deliverable:** one trim of this file, authorized by the operator at Phase 1 after the benefit and the
cost were put to him measured. **The file is 274,805 B against the 262,144 B refusal, confirmed
empirically rather than from the constant** — a default `Read` returns `File content (268.4KB) exceeds
maximum allowed size (256KB)`, zero content, front matter included. `methodology_trim.py --check` reports
the byte trigger FIRES and `SRF_RED 1.0306`, so the trim needs `--force`; the warrant is the governing
adjudication's own self-limitation to *"the middle regime, between the 25,000-token cap and the 256 KiB
refusal"*, the regime this file has now left — the same warrant as S132's and S152's forces, and no
precedent for any other file. **A second, smaller action rides with it:** a backlog item asking whether
adopters should be told how to trim a ledger losslessly. **Ledger:** `CHANGELOG: pending` — the crash
breadcrumb until Phase 3F.

### 2026-09-15 · [ad hoc] S170 close-out — the learning row, the receipt, and what the post left open

**Deliverable posted and verified; this entry closes the session.** Phase 3C: **Learning #66 appended** —
*a remedy you cannot state in one unambiguous sentence is evidence you have not located the defect* —
`starter-kit/FRAMEWORK_LEARNINGS.md` 78,103 → 79,483 B against its 81,920 B ceiling (about two rows left).
Phase 3E, in a sha-verified `--no-local` clone at `40cf1a4`: `bin/tests.sh` **305 passed / 0 failed / 0
skipped**, matching S169's control; dashboard unit 321 OK, budget 116 OK (2 skipped, honestly), trimmer 123
OK; `check-links`, `check-learnings` and `check-handoff --all --allow-pending` all exit 0 read bare;
`context_budget.py --status` exits 2, fork `main` over its declared byte ceiling — pre-existing and by
design. **One instrument trap hit and recorded:** `check-learnings` reported *"65 rows, contiguous 1..65"*
after row #66 landed, which looked like the row had not registered; the parser was run directly and does
see it (65 rows, numbers ending 64, 65, 66). The summary prints `len(rows)` for BOTH numbers, so the
reserved `#14` makes the printed range understate the true maximum. **That is BL-44, raised at S109, not a
new finding** — found by searching the backlog before calling it one. Not fixed: it is not this session's
deliverable. **`CHANGELOG.md` has now crossed the 262,144 B single-Read refusal** — 271,613 B at this
entry, so it must be read with `offset`/`limit` from here. Not trimmed: the operator's decision.

### 2026-09-15 · [ad hoc] S170 — the comment POSTED to upstream PR #82 (non-commit action, operator go-ahead)

- **Action:** one comment posted to `KJ5HST/methodology` PR #82 on the operator's explicit go-ahead, via
  `gh api repos/KJ5HST/methodology/issues/82/comments -F body=@docs/planning/pr82-comment.md`.
- **Result:** comment id **5691623656**, by `rmsharp`, created `2026-09-16T03:31:57Z`,
  <https://github.com/KJ5HST/methodology/pull/82#issuecomment-5691623656>.
- **Read back before this was recorded, byte for byte:** the posted body was fetched again and compared to
  the local file — **sha256 `9d669dc6ee90ba312937453889cf701b2bbb37d83979dc946b6db96936179b30` on both**,
  `cmp` silent. The one-byte delta in a naive `wc -c` is the newline `jq` appends when printing, and the
  API's `len: 25612` is **characters**, not bytes: the body is 25,611 characters and **25,743 bytes**.
- **Pre-flight:** `upstream` re-fetched immediately before posting; #82 still OPEN at head `c84e7d96`,
  unmoved since the review, with 0 comments and 0 reviews — so every claim in the comment was still pinned
  to the tree it was measured on. Working tree clean at `40cf1a4`.
- **Content:** ten suggested changes, ranked — a proposed rewording of the PR's purpose, approach and
  mechanism; three ways the ratchet can still turn backwards; two file budgets denominated in bytes where
  tokens is the operative unit; four smaller defects; and one note on who the mechanism actually binds.
  4,286 words, every result from a run rather than from reading the code, with a reproduction script
  linked by permalink.

### 2026-09-15 · [ad hoc] S170 — the PR #82 comment states the links its facts rested on implicitly (not posted)

**Operator challenge at the Present gate:** *"How does '`_gate_loosenings` already has a removed branch, it
just never reaches it' relate to the empty gate set?"* — two facts set side by side with the causal link
left out. **The link, verified in the source before writing it:** `_gate_map` returns `{}` for a manifest
whose gate list is empty (`methodology_dashboard.py:1931`), and `_gate_loosenings` walks the OLDER version's
gates asking whether each name still exists in the newer, appending `"removed"` when it does not. So an
empty gate set is simply the input that makes *"every gate is missing"* true — and *"a gate is missing"* is
the one case the function already handles. Representing a deleted manifest as zero gates rather than as
unreadable therefore needs **no new detection logic**, only a different answer to *"what was the manifest at
that commit?"* **Audited the rest for the same fault — asserting two facts without their connective — and
fixed three more.** (1) The `install-hook` bullet asserted that a fresh clone has no `core.hooksPath` without
saying why that matters: `install_hook` (`quality_ratchet.py:333`) uses it to choose the hooks directory, so
with it set it finds `.githooks/pre-commit`, declines and prints a chain line, while unset it writes
`.git/hooks/pre-commit` — and `HOOK` (`:325`) execs `<root>/quality_ratchet.py`, the ADOPTER layout, which
does not exist in a repo that keeps the tool under `starter-kit/`. (2) The `CLAUDE.md` bullet gave "4,800
tokens of headroom" without naming what it is headroom under (the 25,000-token ceiling the tool derives for
that file). (3) The coverage bullet said the results file is gitignored without saying the consequence —
the number earning the points was written by whoever last ran the tool locally and no reviewer saw it.
4,002 → 4,286 words. **Still nothing posted.**

### 2026-09-15 · [ad hoc] S170 — the PR #82 comment's remedies made precise; one had the wrong cause (not posted)

**Operator challenge at the Present gate:** *"'run the hook whenever the manifest is tracked in HEAD, not
only when it is on disk' is not clear. What does 'run the hook' mean in this context?"* — it meant nothing
coherent. **The hook script always runs;** what is conditional is the line INSIDE it that calls the tool.
Re-read on the branch: `.githooks/pre-commit` guards on `[ -f "$top/.quality-gates.json" ]`, the WORKING
TREE file, while `precommit()` reads the INDEX (`blob_text(root, ":.quality-gates.json")` → `git cat-file -p
:<path>`). **Two independent doors, each on its own sufficient to wave a deletion past** — so the remedy is
now three numbered places with that dependency stated, rather than one run-on sentence. **Audited every
other remedy for the same fault, since the operator has now flagged it twice; two more failed.** The
lockout bullet named the WRONG CAUSE: it is not that the tool exits 3 on a missing manifest inside
`precommit()` — `find_root()` (`:61`) locates the project by walking up for `.quality-gates.json` ITSELF, so
with the file gone the tool never reaches `precommit()` at all and exits at `main()` (`:473`). The remedy is
therefore to find the root via `git rev-parse --show-toplevel`, as the chained hook already does. The
dashboard bullet said "report flips as loosenings" without saying where or why they are missed:
`_gate_loosenings` compares thresholds only after confirming both versions share a direction, so a flip
falls through both branches. 3,711 → 4002 words. **Still nothing posted.**

### 2026-09-15 · [ad hoc] S170 — the PR #82 comment drops a false contrast: not file vs judgment, but diffable vs not (not posted)

**Operator challenge at the Present gate, and it was fatal to the phrase:** *"Explain what is meant by 'put
the standard in a file instead of in a judgment.' Standard of what? What is the attribute of a standard
that is captured in a file that is not captured in a judgement? How do you preserve a judgment if not via
something stored in a file?"* — **the contrast was false, and the phrase was mine, not the PR's.** This
repository is judgments stored in files; storage was never the distinction. **Re-grounded in the PR's own
principle section** (`ITERATIVE_METHODOLOGY.md`, read on the branch rather than recalled): the thesis is
*"enforce quality on the artifact, not on the actor"*, and *"a more capable agent or a sharper adversarial
reviewer changes the JUDGE, not the CLASS of gate."* **Rewritten to say what a file actually adds, in two
parts:** (1) who evaluates it — a question the session asks itself is answered by whoever is running, and
the answer moves with care, haste and capability; (2) the part that matters here — **a judgment leaves no
record of how strict it was.** One session requiring 134 passing tests and the next settling for 120
changes no artifact, so there is nothing to compare and nothing to notice. A number in a committed file is
a versioned object with an author, a date and a diff. The distinction is **diffable vs not**, not stored vs
unstored: *"the handoff must be specific and actionable"* is stored in a file and still cannot reveal that
this session's "specific" was laxer than the last one's. Closing line, which is now the hinge of the whole
comment: **you can only refuse to let a standard slip if the standard is a thing that has a former self.**
3,520 → 3,711 words. **Still nothing posted.**

### 2026-09-15 · [ad hoc] S170 — the PR #82 comment states the ratchet's actual mechanism, and the findings reorganize around it (not posted)

**Operator question at the Present gate:** *"What is the mechanism that makes raising or lowering a gate's
number have an effect? What is the relationship to a gate and its number?"* — a gap in the rewording, not
in the code. **Answered from the source, verified before asserting:** a gate's number is a pass/fail
boundary whose meaning depends on its `direction` AND on its `command` (the quantity measured), and **two
parts of the system read it differently.** `--run` executes the command and applies the boundary
(`quality_ratchet.py:232`). `--precommit` — the ratchet — **runs no command at all** (`compare()`, `:134`,
docstring *"Pure; no git"*): it reads the staged manifest and `HEAD`'s and compares them field by field, so
the hook sees the EDIT, not its consequences. That is why it works without measuring anything, and it is
also the boundary of the guarantee, in the code's own warning string: **it holds thresholds, not
measurements** — a changed `command` can only warn, since the tool cannot know whether the new command is
easier without running both. **The comment reorganizes around that sentence:** §1 gains three paragraphs
(what the number does / at run time / at commit time / where the guarantee stops), and §2's three findings
stop being a list and become consequences of the one design choice — (a) a comparison with no second side,
(b) thresholds guarded perfectly over a quantity that cannot see failure, (c) the record of the run checked
only for shape. 3,188 → 3,516 words. **Still nothing posted.**

### 2026-09-15 · [ad hoc] S170 — the PR #82 comment recomposed for a reader who has not read the plan (not posted)

**Operator critique at the Present gate, acted on:** the draft assumed too much knowledge — *"Deleting the
manifest is the loosest possible loosening"* carried no meaning without context, `floor 5->4` was never
defined, and the PR's own gap (no understandable statement of purpose, approach and mechanism) was
described rather than remedied. **Recomposed, not patched:** the comment now opens with a proposed
rewording of the PR's purpose/approach/mechanism, offered as liftable text — it defines a quality gate, the
manifest, a loosening, and *why the thing is called a ratchet* (teeth that let the wheel turn one way and
catch it turning back) — and every later section uses only that vocabulary. The three ratchet findings are
reframed as *ways the pawl lifts off*, each with a step-by-step table in plain language (*"at least 5"* →
*"at least 1"* in two unrefused commits); the byte/token section gains the one-sentence setup a reader
needs for why file size is budgeted at all. 2,310 → 3,188 words, deliberately: the operator asked for
clarity, not brevity. **One mechanism verified before describing it plainly:** the dashboard's history walk
skips a deletion commit *and both pairs it sits between* (`methodology_dashboard.py` `_gate_manifest_history`
returns `None` on a failed parse; the pairing loop `continue`s on either side), and `_gate_loosenings`
already carries the `removed` branch it never reaches — which is what makes the suggested fix a two-line
one. Terminology re-audited: no session, backlog or finding codes; the PR's decision codes survive on one
line only, where the comment quotes them as examples a reader cannot resolve. **Still nothing posted.**

### 2026-09-15 · [ad hoc] S170 — the comment on upstream PR #82 drafted (not posted)

**Deliverable, drafted:** `docs/planning/pr82-comment.md` — one comment on upstream PR #82 carrying ten
suggested changes, ranked: two on file budgets measured in bytes where tokens is the operative unit, three
on what the quality ratchet does not hold, four smaller ones, and one on the readability of the PR
description. **Nothing posted** — the post is its own operator go-ahead, and the text is presented in full
first. **Every claim re-verified this session before drafting, none relayed:** #82 unmoved at head
`c84e7d96` with 0 comments and 0 reviews; `docs/planning/pr82-review-repro.sh` re-run end to end, all seven
sections matching what S169 recorded; all six token figures re-measured, both controls (48,555 and 36,955)
reproducing exactly; `quality_ratchet.py --run` re-run in a **verified** `--no-local` clone at `c84e7d96`
(HEAD sha asserted before use) giving **9/9 pass, results `74c773523dab`** — the receipt's own hash,
reproduced firsthand — plus `--selftest` 17 OK, `bin/tests.sh` `== Summary: 134 passed, 1 failed ==` read
directly, and `context_budget.py --status` exit 0. **Two findings sharpened against the review:** the
runner's density 2.8248 was measured correctly in `008d656` and went stale two commits later (`628d218`
53,301 B, `b4226d3` 53,328 B), which is the fair framing and is what the comment says; and Phase 0 is
byte-unchanged by the PR (its runner diff touches only lines 220+, 271+, 316+, 359+), so the description's
"Phase 0 compares the cited counts" has nothing behind it. **One would-be finding dropped:** an
archive-and-`git init` tree measured 131 passed, not 134 — an artifact of the reproduction method, not a
defect, and it did not reach the draft. Terminology audited against the operator's bar: no session
numbers, no backlog or finding codes, no coined names; the PR's own decision codes appear only where the
comment quotes them as examples of what a reader cannot resolve.

### 2026-09-15 · [ad hoc] S170 claim — a comment on upstream PR #82 with suggested changes

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: one comment on
upstream PR #82 (the maintainer's quality ratchet, plan #81) carrying suggested changes to improve it —
drafted to a file, its full text presented before anything is posted, posted only on the operator's explicit
go-ahead, then read back. Scheduled by the operator at S169's close-out: *"for the next session, plan on
developing and posting a comment for PR #82 with suggested changes to improve the PR."* The substance comes
from S169's fork-only review (`docs/planning/pr82-review.md`, recorded at `4ffcb253`) and is **translated,
not pasted** — the operator's bar for the comment is generally recognized terminology with no jargon or
private descriptors, which is also one of the improvements it suggests. Phase 0: #82 OPEN at head
`c84e7d96`, unmoved since the review, 0 comments and 0 reviews; both ledger frontiers at `1d88eaa` with 0
undocumented commits; `HANDOFFS.md` 4 receipts, no trim owed; `CHANGELOG.md` 259,241 B, 2,903 B under the
262,144 B read refusal, not trimmed (the operator's 2026-09-14 decision). BL-57's P3 waits. Carries the
Phase 0 `dashboard_history.jsonl` snapshot.

### 2026-09-15 · [ad hoc] S169 follow-up — the receipt's "unpushed" statement corrected after the push (nothing posted)

- **Change:** S169's receipt, `next_steps` item (1), said the review and its script *"exist only on this fork's
  unpushed `main`"*. That went false when `main` reached `origin` (`4c07b91..c0d7eee`, then `c0d7eee..31b574b`),
  so the line now records the push, gives the absolute URL a comment would need, and says the comment carries
  its substance in plain terms rather than leaning on a link into this fork. A correction is a new entry here,
  never an edited one.
- **Recorded:** this commit, pushed the same way, so `origin/main` equals `main`. Nothing posted upstream.

### 2026-09-15 · [ad hoc] S169 follow-up — fork `main` pushed to `origin`, `4c07b91..c0d7eee` (non-commit action, operator go-ahead)

- **Action:** `git push origin main`, a fast-forward of S169's seven commits — claim `f89c0faf`, trim
  `0ccfce84`, fold `da8af503`, the review record `4ffcb253`, close-out `4c86987`, and the two follow-ups
  `885fd77` and `c0d7eee` — run only inside a guard that re-fetched `origin` and re-checked, in the same
  command, `origin/main` = `4c07b916`, `main` = `c0d7eee3`, 7 ahead, 0 behind, an ancestor, and a clean tree.
  Read back: `git ls-remote origin refs/heads/main` = `c0d7eee3`, equal to local `main`, 0 ahead. Nothing was
  pushed to `upstream`; no PR, comment or reply was opened. This entry's own commit is pushed the same way, so
  `origin/main` equals `main`.
- **Go-ahead:** the operator's, after S169's close-out (*"push fork main to origin"*).

### 2026-09-15 · [ad hoc] S169 follow-up — the operator adds a requirement for the PR #82 comment: generally recognized terminology (nothing posted)

- **Decision:** the operator added that one improvement to suggest on #82 is the readability of its stated
  purpose and methods: *"Use generally recognized terminology with no jargon or private descriptors."* S169's
  receipt, `next_steps` item (1), now carries it, for the suggestion and for the comment itself —
  `docs/planning/pr82-review.md` is written in this fork's shorthand and is to be translated, not pasted.
- **Recorded:** this commit. Nothing was drafted or posted in S169.

### 2026-09-15 · [ad hoc] S169 follow-up — the operator schedules the next session: a comment on PR #82 with suggested changes (nothing posted)

- **Decision:** after S169's close-out the operator directed: *"for the next session, plan on developing and
  posting a comment for PR #82 with suggested changes to improve the PR."* S169's receipt, `next_steps` item
  (1), now says so, with the recipe: re-fetch #82, re-run `docs/planning/pr82-review-repro.sh` against its head,
  draft from `docs/planning/pr82-review.md` §6, present the final text, post it through
  `gh api repos/KJ5HST/methodology/issues/82/comments`, read it back. BL-57's P3 follows it.
- **Recorded:** this commit. Nothing was drafted or posted in S169; the comment is the next session's action.

### 2026-09-15 · [ad hoc] S169 close-out — a fork-only review of upstream PR #82; nothing posted

- **Change:** S169's receipt is completed in `HANDOFFS.md` (self 8/10, predecessor S168 9/10). On the
  operator's request after Phase 0 the session reviewed upstream PR #82 at `c84e7d96` (the record entry
  below) instead of BL-57's P3, which waits; and it trimmed `HANDOFFS.md` to four receipts under its
  retention rule. Nothing was posted upstream. No learning row (BL-53 leaves about three); the lessons are in
  agent memory.
- **Commit/PR:** this commit (claim `f89c0faf`, trim `0ccfce84`, fold `da8af503`, record `4ffcb253`)
- **Session:** S169 · **Verified:** on the record `4ffcb253` in a `--no-local` clone, `bin/tests.sh` 305 passed / 0 failed / 0 skipped, as at a same-time control at `4c07b91`, with 0 status flips and 10 rows differing only in numbers this session moved; `check-links` 105 links; `check-learnings` OK; `check-handoff --all` 0; the shard's `.verify.sh` exit 0 at the trim and after the fold
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [ad hoc] S169 — a fork-only review of upstream PR #82 (the quality ratchet): its file budgets, and seven demonstrated defects

- **Change:** `docs/planning/pr82-review.md` reviews KJ5HST/methodology#82 at `c84e7d96` on the operator's
  request, and `docs/planning/pr82-review-repro.sh` re-runs its seven demonstrations (its section 8, the
  token measurements, is manual). **Budgets:** `CLAUDE.md` is held by a 59,168 B arrival-size byte pin —
  #82 closed 15 B under it yet measures 62 tokens over `main` (23,482.5 against 23,420.5, by the
  doubled-file Read), and the tool judges it at an unmeasured 2.93 B/token (measured: 2.519); the runner's
  token ceiling is applied at a density measured before #82 edited the file — 18,897.5 of 18,900 tokens
  measured, 2.5 of room where the tool reports 22; `context_budget.py --status` is outside the ratchet.
  **Defects, each run in a throwaway repository:** deleting the manifest passes the hook, and deleting then
  re-adding it lower is invisible to hook and dashboard; the count gates pass over failing and skipped
  tests; the gate-run citation lint accepts `0/9 pass`, and no Phase 0 step performs the comparison; the
  dashboard's mirror of `compare()` misses direction flips and command edits; the coverage bonus keys on a
  gate's name; the installed hook locks an adopter out after a deletion; `install-hook` in a fresh
  canonical clone breaks every commit. **Nothing posted upstream.**
- **Commit/PR:** this commit
- **Session:** S169 · **Verified:** #82's suites in a `--no-local` clone at `c84e7d96` — `bin/tests.sh`
  134 passed / 1 failed (Test 9, by construction), `--selftest` 17 OK, `--run` 9/9 with the S20
  receipt's own results hash `74c773523dab`, `context_budget.py --status` 0, no tracked file changed; the
  token instrument first reproduced three recorded figures exactly (48,555; 49,683; 36,955); the saved
  script re-run end to end, every row as the review records it
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [ad hoc] S169 — `HANDOFFS.md`: the trim's pointer block folded into the archive table (20 trims, 154 receipts)

- **Change:** the 3-line pointer block `methodology_trim.py` appended for
  `docs/archive/HANDOFFS-through-2026-09-15-2.md` (trim `0ccfce84`) becomes one table row (n = 2, the
  shard's own fence count), and the table header moves 19 trims / 152 receipts → 20 / 154. Its own
  commit, after the trim (Learning #58). No `--force` was needed: SRF 0.8644 after the claim.
- **Commit/PR:** this commit
- **Session:** S169 · **Verified:** the shard's `.verify.sh` exit 0 at the trim commit `0ccfce84`
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-15-2.md` (2 record(s), 54,851 B → 35,001 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-09-15 → 2026-09-15) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-15-2.md`](docs/archive/HANDOFFS-through-2026-09-15-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-15-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-15-2.md.verify.sh)
rather than trusting a digest printed here. Live file 54,851 B → 35,001 B (−36.2%).

### 2026-09-15 · [ad hoc] S169 claim — a review of upstream PR #82's file budgets and other challenges

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: one fork-only
review of upstream PR #82 — the maintainer's quality ratchet (plan #81), head `c84e7d96`, OPEN and CLEAN
with 0 comments at Phase 0 — written to `docs/planning/pr82-review.md`. The operator's request after Phase
0: *"Look at PR #82 and the way it manages file budgets. Some look to be using bytes in a way we have
recently replaced with better measures of size"* — and any other challenge to what it proposes. Nothing is
posted upstream; a comment on #82 is its own go-ahead. BL-57's P3 waits. Phase 0: both ledger frontiers at
`4c07b91`, 0 undocumented commits; `HANDOFFS.md` 5 receipts, so this session trims to four after this
claim; `CHANGELOG.md` 250,649 B, 11,495 B under the 262,144 B read refusal, not trimmed (the operator's
2026-09-14 decision). Carries the Phase 0 `dashboard_history.jsonl` snapshot.

### 2026-09-15 · [ad hoc] S168 follow-up — fork `main` pushed to `origin` again, `a6520fe..bc7d1e9` (non-commit action, operator go-ahead)

- **Action:** `git push origin main`, a fast-forward of the one commit that records the branch push
  (`bc7d1e9`), inside a guard that re-fetched `origin` and re-checked, in the same command, `origin/main` =
  `a6520fe9`, `main` = `bc7d1e91`, 1 ahead, an ancestor, a clean tree. Read back: `git ls-remote origin
  refs/heads/main` = `bc7d1e91`. This entry's own commit is pushed the same way, so `origin/main` equals
  `main`; S168's receipt, item (4), says so without naming a final sha.
- **Go-ahead:** the operator's (*"push fork main to origin"*).

### 2026-09-15 · [BL-57] S168 follow-up — branch `bl57/changelog-rules` pushed to `origin` as a backup, at `775ba238` (non-commit action, operator go-ahead)

- **Action:** `git push origin bl57/changelog-rules`, creating the branch on the fork — run only inside a
  guard that re-fetched `origin` and re-checked, in the same command, the local branch at `775ba238`, its
  worktree clean, and no branch of that name on `origin`, so nothing could be overwritten. Read back:
  `git ls-remote origin refs/heads/bl57/changelog-rules` = `775ba238`, equal to local. Nothing upstream,
  and no PR — GitHub's *create a pull request* hint was not followed. Rewriting the branch from here — a
  rebase at P12 — needs a force-push of the backup. The plan's header, BL-57's backlog row and S168's
  receipt (`active_task`, item (4)) now say so. This entry's own commit is not pushed.
- **Go-ahead:** the operator's, after S168's close-out (*"push the branch to origin as a backup"*).

### 2026-09-15 · [ad hoc] S168 follow-up — fork `main` pushed to `origin`, `6142d53..2d1bcc3` (non-commit action, operator go-ahead)

- **Action:** `git push origin main` after the close-out, a fast-forward of 8 commits — S167's five and
  S168's three — run only inside a guard that re-fetched `origin` and re-checked, in the same command,
  `origin/main` = `6142d538`, `main` = `2d1bcc30`, 8 ahead, an ancestor, a clean tree. Read back:
  `git ls-remote origin refs/heads/main` = `2d1bcc30`, equal to local `main`, 0 ahead. This entry's own
  commit is pushed the same way, so `origin/main` equals `main` again; S168's receipt says so at item (4).
- **Go-ahead:** the operator's, after S168's close-out (*"push fork main to origin (8 commits)"*).

### 2026-09-15 · [BL-57] S168 close-out — BL-57's P2 done on a branch, not pushed; P3 next

- **Change:** S168's receipt is completed in `HANDOFFS.md` (self 8/10, predecessor S167 9/10). The session
  did BL-57's P2 on branch `bl57/changelog-rules` — a merge of `upstream/main` and two commits, not pushed
  (the entry below). No trim: `HANDOFFS.md` held four receipts at Phase 0 and holds five now, so S169's
  Phase 0 trims. No learning row (BL-53 leaves about three).
- **Commit/PR:** this commit (claim `5eef31f1`, record `30a96bb9`)
- **Session:** S168 · **Verified:** on the record `30a96bb9` in a `--no-local` clone, `bin/tests.sh` 305 passed / 0 failed / 0 skipped, as at a same-time control at `d2347a16`, with 0 status flips and 8 rows differing only in numbers this session moved; unit suites 321 · 123 · 116 OK; the branch as the entry below records; `check-handoff --all` 0
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [BL-57] S168 — BL-57's P2 done on branch `bl57/changelog-rules` (a merge of `upstream/main` and two commits, not pushed); the plan amended

- **Change:** in the worktree `../methodology-bl57`, the branch merged `upstream/main` `8b4dc2c3`
  (`9e1dfeb`, clean; it brings upstream's `.githooks/commit-msg` and the maintainer's S17–S19 records),
  then took P2 in two commits, each with its own entry in the branch's ledger. `f2bcc22`:
  `FRAMEWORK_APPARATUS.md`'s *Size, and when to archive* becomes *Reading and archiving* — the protocol's
  three reads are each partial; past `READ_REFUSE_BYTES`, read with an offset and a limit; archiving is
  optional and the tool's `--check` the only trigger, no size named; conservation across the live file and
  its shards; a trim never in Phase 0 — and the two-cap table and its rate-versus-level argument go,
  28,022 → 25,983 B. `775ba238`: the `HANDOFFS.md` seed's premise and two-cap table give way to *"Archive
  it when the trimmer's trigger fires … this file names no size of its own"* (heading kept, D9; its rule
  otherwise stands, D7), and the trimmer's `:186` comment drops *"context-tax"* (AST identical to
  `b82dcff`). P2's step 4, D8 (ii), needed no commit: #80's F3 did it. **Not pushed; no PR.** Here: the
  plan's header and S168 amendment (`docs/planning/changelog-rules-contradictions-plan.md:3`, `:36`), and
  BL-57's backlog row.
- **Found:** the `HANDOFFS.md` seed's shard bullet still publishes a bare glob that zsh refuses where no
  shard exists (C10's class, recorded for P3); `HOW_TO_USE.md:748`'s *"~515 lines"* is now 501 (P4).
- **Commit/PR:** this commit; branch `9e1dfeb` (merge), `f2bcc22`, `775ba238`
- **Session:** S168 · **Verified:** in `--no-local` clones, `bin/tests.sh` 118 passed / 0 failed at
  `77b21a20` (the control), `9e1dfeb`, `f2bcc22` and `775ba238`, with 0 status flips and no row added or
  removed; unit suites 211 · 124 · 116 OK at each; `check-links` 107 links in 23 files; `check-learnings`
  13 rows; `context_budget.py --status` 0 at each, and §9.7 on `775ba238` — its merge with `upstream/main`
  is its own tree — *nothing over budget*, `CLAUDE.md` 59,159 of 59,168 B; P2's three DONE greps print
  nothing on `775ba238`
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [BL-57] S168 claim — BL-57's P2: reading and archiving, on the branch after merging `upstream/main`

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: P2 of the
approved BL-57 plan (`docs/planning/changelog-rules-contradictions-plan.md:440`), the operator's *"A"* at
this session's Phase 0. In the worktree `../methodology-bl57`, branch `bl57/changelog-rules` (`77b21a20`,
S167's P1) first merges `upstream/main` `8b4dc2c3` (#80 merged at `4d9e2715`), then takes P2's scope;
nothing is pushed. P2's item 4 — D8 (ii), drop `CHANGELOG.md` from upstream's root `.context-budget.json`
— is already done: #80's F3 moved both ledgers to `_deliberate_exclusions`, verified on `upstream/main` at
Phase 0, so the plan records it rather than redoing it. Phase 0: both ledger frontiers at `d2347a16`, 0
undocumented commits; `HANDOFFS.md` 4 receipts, no trim; `CHANGELOG.md` 243,849 B, 18,295 B under the
262,144 B read refusal, not trimmed (the operator's 2026-09-14 decision); no open upstream issues or PRs.
Carries the Phase 0 `dashboard_history.jsonl` snapshot.

### 2026-09-15 · [BL-57] S167 close-out — BL-57's P1 done on a branch, not pushed; PR #80 merged upstream; P2 next

- **Change:** S167's receipt is completed in `HANDOFFS.md` (self 7/10, predecessor S166 9/10). The session
  did BL-57's P1 on branch `bl57/changelog-rules` (four commits, not pushed; the entry below), trimmed
  `HANDOFFS.md` to four receipts, and recorded #80's merge (`4d9e2715`), which landed mid-session. No
  learning row: the one candidate, *a green suite cannot see a gate it never runs*, is in memory, and BL-53
  leaves about three rows.
- **Commit/PR:** this commit (claim `6f9162f1`, trim `50498451`, fold `943059f5`, record `f63460e5`)
- **Session:** S167 · **Verified:** on this content committed inside a `--no-local` clone, `bin/tests.sh`
  305 passed / 0 failed / 0 skipped, as is a same-time control at `6142d538` — Test 9 passes on fork `main`
  too since #80's merge — with 0 status flips and 11 rows differing only in numbers this session moved;
  unit suites 321 · 123 · 116 OK; `check-handoff --all` 0
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [BL-57] S167 — BL-57's P1 done on branch `bl57/changelog-rules` (4 commits, not pushed); the plan amended; PR #80 merged upstream the same day

- **Change:** branch `bl57/changelog-rules` created from PR #80's head `aa36fd8b` in the worktree
  `../methodology-bl57` (a branch operation), and P1 of the approved plan committed on it — four commits,
  each with its own entry in the branch's own `CHANGELOG.md`: `eb06625b` the trimmer's fence controls read
  a frozen copy of today's seed (`tools/fixtures/seed-CHANGELOG-ledger-format-1.md`); `b0634606` the seed's
  three rule sections move verbatim to `FRAMEWORK_APPARATUS.md` §The Action Ledger, and the seed becomes a
  1,335 B pointer carrying `ledger-format: 2`; `2d5dc6e9` `bin/status` keys on that marker and its advice
  stops rewriting entries; `77b21a20` the three documents that describe the apparatus name its seventh
  section. **Not pushed; no PR** — each is its own go-ahead. In this repo: the plan's header and an S167
  amendment (`docs/planning/changelog-rules-contradictions-plan.md:3`, `:21`), its §9.4 command corrected
  for zsh, and BL-57's backlog row.
- **Found:** (1) step 4 first landed as `d4841721`, 116 B over upstream `CLAUDE.md`'s pinned 59,168 B
  ceiling, with all four suites green — none runs `context_budget.py --status` on the tree. The plan's §9.7
  check caught it, and the commit was amended to `77b21a20` (the row is now 9 B shorter than before;
  unpushed, so nothing published was rewritten). (2) The plan's §9.4 command printed nothing under zsh:
  `"$c:…"` is a history modifier. (3) **PR #80 merged** at 19:59 UTC (`4d9e2715`; `upstream/main`
  `8b4dc2c3`), which is why Test 9 now passes on every tree.
- **Commit/PR:** this commit (the record); branch `eb06625b`, `b0634606`, `2d5dc6e9`, `77b21a20`
- **Session:** S167 · **Verified:** at `77b21a20`, in a `--no-local` clone: `bin/tests.sh` 118 passed / 0
  failed, against 116 / 0 at `aa36fd8b` run at the same time — 1 row renamed, 3 added, 0 status flips; unit
  suites 211 · 124 · 116 OK (4 skipped); `check-links` 107 links (from 105); `check-learnings` 13 rows.
  `context_budget.py --status` exits 0 on the branch and on its merge into `upstream/main`. The plan's P1
  DONE checks: §9.3 VERBATIM ×3; §9.4 prints only `b0634606`; the seed ≤ 1,600 B with no `## `, `NO_RECORDS`
  exit 0, seeded by `bin/sync`; all six adopters' `CHANGELOG.md` copies read stale with the new advice, and
  their `HANDOFFS.md` verdicts equal fork `main`'s.
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [ad hoc] S167 — `HANDOFFS.md`: the trim's pointer block folded into the archive table (19 trims, 152 receipts)

- **Change:** the 3-line pointer block `methodology_trim.py` appended for
  `docs/archive/HANDOFFS-through-2026-09-15.md` (trim `50498451`) becomes one table row (n = 2, the
  shard's own fence count), and the table header moves 18 trims / 150 receipts → 19 / 152. Its own
  commit, after the trim (Learning #58). No `--force` was needed: SRF 0.8755 after the claim.
- **Commit/PR:** this commit
- **Session:** S167 · **Verified:** the shard's `.verify.sh` exit 0 at the trim commit `50498451`
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-15.md` (2 record(s), 57,366 B → 38,813 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-09-14 → 2026-09-15) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-15.md`](docs/archive/HANDOFFS-through-2026-09-15.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-15.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-15.md.verify.sh)
rather than trusting a digest printed here. Live file 57,366 B → 38,813 B (−32.3%).

### 2026-09-15 · [BL-57] S167 claim — BL-57's P1: the `CHANGELOG.md` rules to one home, thin seeds, one stale-seed rule (structure only), on a branch from #80's head

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: P1 of the
approved BL-57 plan (`docs/planning/changelog-rules-contradictions-plan.md:359`), the operator's *"A"* at
this session's Phase 0. Branch `bl57/changelog-rules` from PR #80's current head `aa36fd8b` (the plan was
written at `b82dcff`; its hazard 1), in a worktree at `../methodology-bl57`; nothing is pushed. Phase 0:
#80 OPEN at `aa36fd8b`, `MERGEABLE`/`CLEAN`, 3 comments, nothing from the maintainer since S166's reply;
`upstream/main` `9fa3141`; both ledger frontiers current; `bin/tests.sh` 304 / 1 / 0 at `6142d538` (Test
9). `HANDOFFS.md` holds 5 receipts, so this session trims it to 4 after this claim (dry run: S162 to
`docs/archive/HANDOFFS-through-2026-09-14.md`, SRF 0.8013, no `SRF_RED`). `CHANGELOG.md` is 237,544 B,
24,600 B under the 262,144 B read refusal; not trimmed — the operator's 2026-09-14 decision, asked about
at Phase 0 and not changed. Carries the Phase 0 `dashboard_history.jsonl` snapshot.

### 2026-09-15 · [ad hoc] S166 follow-up — fork `main` pushed to `origin`, `755ef09..632f575` (non-commit action, operator go-ahead)

- **Action:** `git push origin main` after the close-out, a fast-forward of 11 commits — S164's three,
  S165's five and S166's three — run only after checking that `origin/main` was an ancestor of `main`, 0
  commits behind, with a clean tree. Read back: `git ls-remote origin refs/heads/main` = `632f5758`, equal
  to local `main`. This entry's own commit is pushed the same way, so `origin/main` equals `main` again.
- **Go-ahead:** the operator's, after S166's close-out (*"push main to origin"*).

### 2026-09-15 · [ad hoc] S166 close-out — PR #80's F2 and F3 published (push, description, reply); the maintainer's move next

- **Change:** S166's receipt is completed in `HANDOFFS.md` (self 8/10, predecessor S165 9/10). The session
  published F2 (`37740763`) and F3 (`aa36fd8b`) of the maintainer's #80 review on the operator's go-ahead
  for all three actions — the push `d4e1570..aa36fd8`, the description, the reply — each read back before
  the next (the three entries below). The response plan's §4 and §5 headings now say published too. No
  trim: `HANDOFFS.md` held 4 receipts at Phase 0, and holds 5 after this commit, so S167's Phase 0 trims.
- **Commit/PR:** this commit (claim `32c90db4`, record `6e109e45`)
- **Session:** S166 · **Verified:** A, B and C each read back through the GitHub API; `check-handoff --all`
  0 (5 receipts); `bin/tests.sh` 304/1/0 at Phase 0 (`5ce7bb2`) and again on this close-out content
  committed inside a clone — 305 rows, 0 status flips (the counter proved on a planted flip), 9 rows
  differing only in numbers this session moved
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [ad hoc] S166 — PR #80: the reply for F2 and F3 posted (non-commit action, operator go-ahead)

- **Action:** one comment on [PR #80](https://github.com/KJ5HST/methodology/pull/80#issuecomment-5685701488),
  author `rmsharp`, 2026-09-15 18:21:28 UTC, body `docs/planning/pr80-reply-f2-f3.md`, posted through the
  REST API (`gh api repos/KJ5HST/methodology/issues/80/comments -F body=@…`): F2's generalized test and its
  six-mutant table; F3 as (i) for the pair with the ledgers dropped, (ii) shown unworkable as written, F4
  answered as framed; the corrected headline (68,548 B / 24,278 tokens on the merge); F5 and F6 after the
  merge. Read back through the API: equal to the file. #80 now has 3 comments.
- **Go-ahead:** the operator's, at S166 (*"A B C"*), gated on B's read-back.

### 2026-09-15 · [ad hoc] S166 — PR #80: the description updated to the F3 head (non-commit action, operator go-ahead)

- **Action:** the PR body replaced with `docs/planning/pr80-body-after-f3.md` through `gh api -X PATCH
  repos/KJ5HST/methodology/pulls/80 -F body=@…` — the head `aa36fd8`, 28 files +7,892 / −580 (re-derived at
  Phase 0, after reproducing +7,795 / −554 at `d4e1570`), the headline table re-measured on the merge
  (68,548 B / 24,278 tokens, 97.1%; `main` 81,493 B / 28,610), the paragraph on the root
  `.context-budget.json`, the corpus 659,755 → 839,383 B, and the F2 and F3 verification rows. Before it,
  the live body was checked equal to `pr80-body-after-f1.md`, so the maintainer had not edited it. Read
  back after: equal to the file, byte for byte.
- **Go-ahead:** the operator's, at S166, gated on A's read-back.

### 2026-09-15 · [ad hoc] S166 — PR #80: F2 + F3 pushed, `read-set-budgets` fast-forwarded `d4e1570..aa36fd8` (non-commit action, operator go-ahead)

- **Action:** `git push upstream pr80/f3-read-set-token-ceilings:read-set-budgets`, run only when the same
  command had re-checked #80's head (`d4e1570`), `upstream/main` (`9fa3141`) and its 2 comments. It carries
  F2 (`37740763`) and F3 (`aa36fd8b`), each with its entry in the branch's own ledger. Read back: the remote
  ref and the API's branch head both `aa36fd8b`; #80's head `aa36fd8b`, 16 commits, `MERGEABLE`/`CLEAN` —
  on the second read: the first, seconds after the push, still showed `d4e1570` and `UNKNOWN`. The three
  local `pr80/*` branches stay until #80 merges.
- **Go-ahead:** the operator's, at S166.

### 2026-09-15 · [ad hoc] S166 claim — PR #80: publish F2 + F3 (push, description, reply) on the operator's go-ahead for all three

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: S165's next
step (1) — publish F2 (`37740763`) and F3 (`aa36fd8b`) of the maintainer's #80 review, by
`docs/planning/pr80-review-response.md` §3. The operator approved all three outward actions at this
session's Phase 0 (*"A B C"*): A, push `pr80/f3-read-set-token-ceilings:read-set-budgets` (a fast-forward
from `d4e1570`); B, the description from `docs/planning/pr80-body-after-f3.md`; C, the reply
`docs/planning/pr80-reply-f2-f3.md`. Each is read back before the next, and any mismatch stops the
sequence. Phase 0: #80 still at `d4e1570`, `upstream/main` at `9fa3141`, 2 comments; `HANDOFFS.md` at 4
receipts, so no trim. Carries the Phase 0 `dashboard_history.jsonl` snapshot.

### 2026-09-15 · [ad hoc] S165 close-out — PR #80's F3 done on a local branch, held with F2 for one publish; three go-aheads next

- **Change:** S165's receipt is completed in `HANDOFFS.md` (self 8/10, predecessor S164 9/10). The session
  answered F3 of the maintainer's #80 review on local branch `pr80/f3-read-set-token-ceilings`
  (`aa36fd8b`, on top of F2's `37740763`) with the operator's R1 L1, and recorded it in
  `docs/planning/pr80-review-response.md` §5, with the description re-derived and one reply drafted. It
  also trimmed `HANDOFFS.md` to four receipts without `--force`. The worktree `../methodology-pr80-f3` was
  removed once clean (local housekeeping); the branch stays. Nothing was pushed.
- **Commit/PR:** this commit (claim `8e0a7a72`, trim `d9ace03`, fold `ef55d77`, record `95a4845`; branch
  `aa36fd8b`, not pushed)
- **Session:** S165 · **Verified:** `check-handoff --all` 0 (4 receipts); branch suites 115/1 at `37740763`
  and `aa36fd8b` with 0 status flips; `--status` exit 0 on both trees; fork `bin/tests.sh` 304/1/0 at
  `ef55d775` with 0 status flips against Phase 0, and 304/1/0 again on this close-out content committed
  inside a clone — 0 status flips, 7 rows differing only in numbers this session moved
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [ad hoc] S165 — PR #80 review F3 done on a local branch, not pushed: the root `.context-budget.json` reports OK on the branch and on its merge into `main`

- **Change:** local branch `pr80/f3-read-set-token-ceilings` (worktree `../methodology-pr80-f3`) from F2's
  `37740763`, one commit, **`aa36fd8b`**: the branch's root `.context-budget.json` gives
  `SESSION_RUNNER.md` and `SAFEGUARDS.md` token ceilings at measured densities (19,200 + 5,800 tokens,
  partitioning the 25,000-token cap), declares no `read-set` class ceiling, and moves `CHANGELOG.md` and
  `HANDOFFS.md` to `_deliberate_exclusions`; its entry sits in the branch's own ledger above F2's.
  Canonical-only. The operator chose **R1 L1** at this session's Present gate, from nine variants measured
  first on the branch and on its merge into `upstream/main` (`docs/planning/pr80-f3-variants.py`). Record:
  `docs/planning/pr80-review-response.md` §5 (header, §1 and §3 updated); drafted for the publish, the
  description with every figure re-derived (`docs/planning/pr80-body-after-f3.md`) and one reply for F2 and
  F3 (`docs/planning/pr80-reply-f2-f3.md`). **Nothing pushed, no description edit, no reply** — three
  go-aheads, in §3's order.
- **Found:** the merge is 967 B larger than the branch (upstream S16's paragraph in `SAFEGUARDS.md`), so
  the description's headline row was stale — the merged pair is 68,548 B / 24,278 tokens, not
  67,581 / 23,902; and the review's answer (ii) cannot work as written, because `token_ceiling()` clamps
  every whole-read file to the 25,000-token cap.
- **Commit/PR:** this commit (branch `aa36fd8b`, not pushed)
- **Session:** S165 · **Verified:** `--status` exit 0 on both trees from the committed config; branch
  `bin/tests.sh` 115/1 at `37740763` and `aa36fd8b` — 116 rows, 0 status flips, 0 rows differing; unit
  suites 211 · 123 · 116 OK; `check-links` and `check-learnings` OK; `merge-tree` against `9fa3141` clean;
  the push is a fast-forward
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [ad hoc] S165 — `HANDOFFS.md`: the trim's pointer block folded into the archive table (18 trims, 150 receipts)

- **Change:** the 3-line pointer block `methodology_trim.py` appended for
  `docs/archive/HANDOFFS-through-2026-09-11.md` (trim `d9ace03`) becomes one table row (n = 2, the
  shard's own fence count), and the table header moves 17 trims / 148 receipts → 18 / 150. Its own
  commit, after the trim (Learning #58). No `--force` was needed: SRF 0.9383 after the claim.
- **Commit/PR:** this commit
- **Session:** S165 · **Verified:** the shard's `.verify.sh` exit 0 at the trim commit `d9ace03`
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-11.md` (2 record(s), 60,236 B → 37,186 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-09-11 → 2026-09-11) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-11.md`](docs/archive/HANDOFFS-through-2026-09-11.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-11.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-11.md.verify.sh)
rather than trusting a digest printed here. Live file 60,236 B → 37,186 B (−38.3%).

### 2026-09-15 · [ad hoc] S165 claim — PR #80 review F3: the root `.context-budget.json` reports the PR's own headline as OVER

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: F3 of the
maintainer's PR #80 review ([comment](https://github.com/KJ5HST/methodology/pull/80#issuecomment-5674670153)),
chosen by the operator at this session's Phase 0 (A). Measure the four answers — (i) the read-set ceiling
in tokens at measured density; (ii) the ledger ceilings set where the ledgers are; (iii) *"over at install,
by design"*, stated; (iv) the ledgers dropped from the read budget, as this fork did at `3c8acd5` — on
branch `pr80/f2-installed-source-guard`, bring them to the operator in prose, and commit the chosen one on
top of `37740763`, tested in a `--no-local` clone. First, `HANDOFFS.md`'s retention trim to four (5
receipts at Phase 0, SRF 0.8687: no `--force` needed if this stub keeps the file under 61,471 B —
re-derived after this commit). **Nothing pushed, no PR edit, no reply** — each is its own go-ahead.
Carries the Phase 0 `dashboard_history.jsonl` snapshot.

### 2026-09-15 · [ad hoc] S164 close-out — PR #80's F2 done on a local branch and held for one push with F3; F3 next

- **Change:** S164's receipt is completed in `HANDOFFS.md` (self 8/10, predecessor S163 9/10). The session
  answered F2 of the maintainer's #80 review on local branch `pr80/f2-installed-source-guard` (`37740763`,
  test-only), RED first on the review's mutant, and recorded it in `docs/planning/pr80-review-response.md`
  §4. Nothing was pushed: F2 is held so F2 and F3 go up in one push and one reply. The worktree
  `../methodology-pr80-f2` was removed once clean (local housekeeping); the branch stays. F3 starts with
  an operator decision (§5).
- **Commit/PR:** this commit (claim `8791a272`, record `95d84cfd`; branch `37740763`, not pushed)
- **Session:** S164 · **Verified:** `check-handoff --all` 0 (5 receipts); branch suites 115/1 at
  `d4e1570` and `37740763` with 0 status flips; fork `bin/tests.sh` on this content in a `--no-local`
  clone 304/1/0, exit 1, 0 status flips against the Phase 0 baseline (the one failure is Test 9,
  pre-existing)
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [ad hoc] S164 — PR #80 review F2 done on a local branch, not pushed: every non-markdown file `bin/sync` installs is now tested, RED first

- **Change:** local branch `pr80/f2-installed-source-guard` (worktree `../methodology-pr80-f2`) from #80's
  head `d4e1570`, one commit, **`37740763`**: `tools/test_methodology_dashboard.py:2666` generalizes
  `test_a_synced_repo_with_context_budget_installed_is_still_doc_only` in place as
  `test_a_synced_repo_with_each_installed_source_file_is_still_doc_only` — every non-markdown dest in
  `bin/_manifest.py`, written from its real `starter-kit/` source into a doc-only fixture, alone and all
  together, plus a direct `is_framework_installed` call per file. Its entry sits in the branch's own ledger
  (`CHANGELOG.md:95` there), above F1's and below `main`'s. Test-only and canonical-only: neither scanner
  twin changes. On fork `main`: `docs/planning/pr80-review-response.md` §4 records the branch and its
  evidence, and its header now says F1 was published at S163 (it still read *"Nothing below has been
  pushed"*); new `docs/planning/pr80-f2-mutants.py` plants the six mutants.
- **RED first:** the review's mutant (M1), `.context-budget.json`'s signatures (M4) and a narrowing of the
  one `collect_all` call site (M6) pass the old suite (211 OK) and fail the new test. The scanner's own
  entry (M3) is not caught by this test — its neutralized strings sit in its own signature table, so the
  real file matches itself — and the docstring says so.
- **Verified**, in `--no-local` clones, every exit code read bare: `bin/tests.sh` 115 / 1, exit 1 at
  `d4e1570` and at `37740763` — 116 rows, 0 status flips, 0 rows differing (Test 9, pre-existing); unit
  suites 211, 123 (2 skipped) and 116 (2 skipped) OK on both; `check-links` OK (105 / 23) and
  `check-learnings` OK (13 rows) on both. `git merge-tree` against `upstream/main` `9fa3141`: no
  conflicts; the push would fast-forward `read-set-budgets`.
- **Not pushed, no description edit, no reply** — held so F2 and F3 go up in one push and one reply;
  each is its own go-ahead.
- **Commit/PR:** this commit; branch `37740763`

### 2026-09-15 · [ad hoc] S164 claim — PR #80 review F2: guard the dashboard's doc-only exclusion for every framework-installed file, RED first

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: F2 of the
maintainer's PR #80 review ([comment](https://github.com/KJ5HST/methodology/pull/80#issuecomment-5674670153)),
chosen by the operator at this session's Phase 0 (A). On a local branch from #80's head `d4e1570`:
generalize `test_a_synced_repo_with_context_budget_installed_is_still_doc_only`
(`tools/test_methodology_dashboard.py:2666`) over every `FRAMEWORK_INSTALLED_SOURCE` name
(`starter-kit/methodology_dashboard.py:360`) using the real `starter-kit/` file, RED first on the
maintainer's mutant — `methodology_trim.py`'s `version_re` and signatures (`:484`–`:496`) neutralized in
both twins — while the current suite stays green. A test change: neither dashboard twin is edited except
to plant the mutant in a clone. Tested in a `--no-local` clone. **Nothing pushed, no PR edit, no reply** —
each is its own go-ahead; Phase 0 suggested holding F2 locally so F2 and F3 go up in one push. Carries
the Phase 0 `dashboard_history.jsonl` snapshot.

### 2026-09-15 · [ad hoc] S163 follow-up — fork `main` pushed to `origin`, `f8531cf..6007db3` (non-commit action, operator go-ahead)

- **Action:** `git push origin main` on the operator's *"push main"*, after S163's close-out: a
  fast-forward of 60 commits (`origin/main` was `f8531cf`; no commit on `origin` was missing from
  `main`; the tree was clean). `origin/main` read back as `6007db3`. This entry's own commit is pushed
  the same way, so the two stay equal. Nothing else was pushed — the local branch
  `pr80/f1-learnings-1-13` already matches upstream's `read-set-budgets`.
- **Go-ahead:** the operator's, after S163's close-out. It discharges the S163 receipt's carried item
  *"pushing fork `main`"*.

### 2026-09-15 · [ad hoc] S163 close-out — PR #80's F1 answered and published; F2 and F3 next

- **Change:** S163's receipt is completed in `HANDOFFS.md` (self 8/10, predecessor S162 7/10). The
  session answered F1 of the maintainer's #80 review with option (a) — two commits on
  `read-set-budgets`, pushed; the description updated; the reply posted — and trimmed `HANDOFFS.md` to
  four receipts, forced past `SRF_RED` on the operator's decision. F2 and F3 are set up in
  `docs/planning/pr80-review-response.md` §4–§5; F3 starts with an operator decision.
- **Commit/PR:** this commit (claim `9f66ebd9`, preparation `42e52f9`, trim `ae44dec9`, outward actions
  `b9091fe`, fold `49685a9`; branch `5c9f0f3`, `d4e15706` on
  [PR #80](https://github.com/KJ5HST/methodology/pull/80))
- **Session:** S163 · **Verified:** `check-handoff --all` 0 (4 receipts); the shard proof 0 after the
  fold; branch suites 115/1 at `b82dcff`, `5c9f0f3` and `d4e15706` with 0 status flips; `bin/tests.sh`
  on this content in a `--no-local` clone 304/1/0, exit 1, 0 status flips against the Phase 0 baseline
  (the one failure is Test 9, pre-existing)
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [ad hoc] S163 — `HANDOFFS.md`: the trim's pointer block folded into the archive table

- **Change:** the three-line pointer block `methodology_trim.py` appended for
  `docs/archive/HANDOFFS-through-2026-09-10.md` becomes one table row (n = 2, the shard's own fence
  count), and the heading now reads 17 trims, 148 receipts. Its own commit, after the trim, because
  folding inside the trim commit fails the shipped proof's L2 (Learning #58).
- **Verified:** the table has 17 rows summing to 148; each edit matched exactly once.
- **Commit/PR:** this commit

### 2026-09-15 · [ad hoc] S163 — PR #80: the reply to the maintainer's review posted (non-commit action, operator go-ahead)

- **Action:** one comment on [PR #80](https://github.com/KJ5HST/methodology/pull/80#issuecomment-5676599724),
  author `rmsharp`, 2026-09-15 07:42:05 UTC, body `docs/planning/pr80-reply-f1.md`: F1 answered with (a)
  and its two commits; F2 and F3 next; F4 left to the BL-57 plan's own PR after #80 merges; F5 and F6 can
  follow. Read back through the API: equal to the file.
- **Go-ahead:** the operator's, at S163 (*"push edit reply"*).

### 2026-09-15 · [ad hoc] S163 — PR #80: the description updated to the F1 head (non-commit action, operator go-ahead)

- **Action:** the PR body replaced with `docs/planning/pr80-body-after-f1.md` — the head and diff size,
  the corpus total (658,788 → 838,416 B), the `FRAMEWORK_LEARNINGS.md` and `context_budget.py` rows, a
  verification row, and one sentence saying the file holds rows 1–13 and the reserved `#14`. **`gh pr
  edit` failed** (exit 1, a GraphQL error about the deprecated Projects (classic) API) and changed nothing
  — the description read back as the original, so the reply was held back. The edit then went through
  the REST API (`gh api -X PATCH repos/KJ5HST/methodology/pulls/80 -F body=@…`) and read back equal to the
  file.
- **Go-ahead:** the operator's, at S163.

### 2026-09-15 · [ad hoc] S163 — PR #80: F1 (a) pushed, `read-set-budgets` fast-forwarded `b82dcff..d4e1570` (non-commit action, operator go-ahead)

- **Action:** `git push upstream pr80/f1-learnings-1-13:read-set-budgets`, after re-checking that #80's
  head was still `b82dcff`, upstream `main` still `9fa3141`, one comment, and `git merge-tree` clean.
  After: head `d4e15706`, `MERGEABLE`, `CLEAN`. The two commits carry their entries in the branch's own
  ledger. The worktree `../methodology-pr80` was removed once clean and pushed; the local branch stays
  until #80 merges.
- **Go-ahead:** the operator's, at S163.

### 2026-09-15 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-10.md` (2 record(s), 61,471 B → 41,455 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **2** record(s) (2026-09-10 → 2026-09-10) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-10.md`](docs/archive/HANDOFFS-through-2026-09-10.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-10.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-10.md.verify.sh)
rather than trusting a digest printed here. Live file 61,471 B → 41,455 B (−32.6%).

### 2026-09-15 · [ad hoc] S163 — PR #80 review F1 (a) prepared on a local branch, not pushed; the updated description and the reply drafted; the BL-57 plan amended

- **Change:** local branch `pr80/f1-learnings-1-13` (worktree `../methodology-pr80`) from #80's head
  `b82dcff`, two commits: `5c9f0f3` states the rule where eight citations of Learnings past #13 stood
  (`starter-kit/context_budget.py:77`, `:378`, `:409`, and five in the canonical-only tests), then
  `d4e15706` cuts `starter-kit/FRAMEWORK_LEARNINGS.md` to rows 1–13 plus the reserved `#14` (56,673 →
  13,983 B). Their entries sit in the branch's own ledger, with #80's block, below `main`'s. New
  fork-only files: `docs/planning/pr80-review-response.md` (the review, what was done, the publish
  commands, and F2 and F3 set up for the next session), `docs/planning/pr80-body-after-f1.md` (the PR
  description to publish) and `docs/planning/pr80-reply-f1.md` (the reply). The BL-57 plan's header
  now says it is approved and that no row past #13 will exist upstream; its P1 step 5 states Learning
  #19's rule instead of citing it.
- **Why:** the operator chose F1 option (a) at S163's Phase 0. Pushing, editing the PR description and
  replying are each the operator's go-ahead; none is done.
- **Verified:** in `--no-local` clones, `bin/tests.sh` 115/1 at `b82dcff`, `5c9f0f3` and `d4e15706` —
  116 rows each, 0 status flips (Test 9, pre-existing); unit suites 450 OK (4 skipped) at all three;
  `check-links` OK (105/23); `check-learnings` 13 rows, contiguous, citations resolve, and a planted
  `Learning #20` is caught; `git merge-tree` against upstream `main` `9fa3141`: no conflicts
- **Commit/PR:** this commit (fork `main`); the two branch commits are recorded in the branch's ledger
- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-15 · [ad hoc] S163 claim — PR #80 review F1 (a): trim the branch's `FRAMEWORK_LEARNINGS.md` to rows 1–13 and repair the citations the cut breaks

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: F1 of the
maintainer's PR #80 review ([comment](https://github.com/KJ5HST/methodology/pull/80#issuecomment-5674670153),
2026-09-15 04:19 UTC), option (a), chosen by the operator at this session's Phase 0. On a local branch
from #80's head `b82dcff`: cut `starter-kit/FRAMEWORK_LEARNINGS.md` to rows 1–13 plus the reserved-`#14`
note; repair every citation the cut leaves dangling — `starter-kit/context_budget.py:77` and `:378` cite
Learning #34, and `bin/check-learnings` scans Markdown only, so it would not see them; draft the
replacement for the PR description; amend the BL-57 plan's P1 step 5
(`docs/planning/changelog-rules-contradictions-plan.md:363`, which cites Learning #19). Tested in a
clone. **Nothing pushed, no PR edit, no reply** — each is its own go-ahead. F2 and F3 are set up for the
next session. `HANDOFFS.md` holds five receipts and its trim refuses with `SRF_RED` (SRF 1.0925 vs
`16ac3fc`); the operator's decision on `--force` is pending. Carries the Phase 0
`dashboard_history.jsonl` snapshot.

### 2026-09-15 · [BL-57] S162 close-out — the BL-57 plan approved and committed; P1 is next

- **Change:** S162's receipt is completed in `HANDOFFS.md` (self 7/10, predecessor S161 8/10). BL-57's
  row and note in `docs/planning/BACKLOG.md` and `BACKLOG-DETAIL.md` point at the plan; BL-47's
  `CHANGELOG.md` half is recorded as settled by Q2 A, and BL-56 as folded into the plan's P6.
  `HANDOFFS.md` now holds five receipts, and its own policy trims to four at the next Phase 0.
- **Commit/PR:** this commit (claim `7ea7346b`, plan `9292132e`, Learning #65 `64f085b2`)
- **Session:** S162 · **Verified:** `check-learnings` 0; `BACKLOG-DETAIL.md.verify.sh` 0;
  `check-handoff --all` 0 (5 receipts); `bin/tests.sh` on this content in a `--no-local` clone 304/1/0,
  exit 1, with 0 status flips against the Phase 0 baseline (the one failure is Test 9, pre-existing)
- **Model:** Claude Opus 5, 1M context (claude-opus-5[1m])

### 2026-09-15 · [BL-57] S162 — Learning #65: procedure written into a seed-once file cannot be corrected by the framework

- **Change:** `starter-kit/FRAMEWORK_LEARNINGS.md` gains row 65, the structural cause the BL-57 plan
  found (§1.2). Rules shipped inside a seed are frozen at each adopter's seeding, so every correction
  strands a copy: the two adopters whose ledgers still carry the rules both teach the pre-correction
  *silent* truncation, and their fenced examples inflate a line-based audit. The row is fork-only; the
  upstream PR adds none (plan K4).
- **Commit/PR:** this commit
- **Session:** S162 · **Verified:** `bin/check-learnings` exit 0 — 64 rows, contiguous, 0 over 1,500 B.
  Row 65 is 1,144 B; the file is 78,103 B, 3,817 B under the 81,920 B growth warning — about three more
  rows of this size
- **Model:** Claude Opus 5, 1M context (claude-opus-5[1m])

### 2026-09-15 · [BL-57] S162 — the BL-57 plan: one set of `CHANGELOG.md` rules, kept in one place (operator-approved)

- **Change:** `docs/planning/changelog-rules-contradictions-plan.md` (812 lines) plans the removal of
  the contradictions in the framework's `CHANGELOG.md` rules, here and in six adopters, through a new
  upstream PR once #80 merges. It inventories sixteen findings across fourteen files on three trees
  (`b82dcff`, `upstream/main`, fork `main`; 1,577 matching lines in 45 files on `b82dcff`) and six
  adopters, and sets twelve one-session phases, each with DONE criteria, verification commands, its
  surface and what that surface cannot enforce. **The operator's decisions (S162):** Q1 A, the rules
  move to one synced home, `FRAMEWORK_APPARATUS.md` §The Action Ledger, and the seed becomes a linked
  pointer with a format marker; Q2 A, archiving is optional; Q3 A, `[BL-<id>]` takes any backlog id;
  Q4 A, one entry per commit, never edited. Recommendations D5–D10 were approved with the plan.
  Planning only: nothing implemented, nothing outward-facing.
- **Commit/PR:** this commit
- **Session:** S162 · **Verified:** an independent read-only review found 4 errors, 9 risks and 6 nits
  in the first draft, each reproduced before it was fixed; §9.1 and §9.2 reproduce; the §9.3 and §9.8
  checkers catch every planted mutant; the links resolve; baselines at `b82dcff` (`bin/tests.sh` 115/1,
  450 unit tests OK, `check-links` OK) and fork `main` (304/1)
- **Model:** Claude Opus 5, 1M context (claude-opus-5[1m])

### 2026-09-14 · [BL-57] S162 claim — plan BL-57: remove the contradictions in the framework's `CHANGELOG.md` rules, here and in six adopters, aiming at an upstream PR

**Phase 1B claim stub. `CHANGELOG: pending` until this session's close-out.** Deliverable: a plan in
`docs/planning/` for BL-57 (`docs/planning/BACKLOG-DETAIL.md`, anchor `bl-57`) — a grep inventory taken
on the upstream target tree as well as fork `main`, per-phase DONE criteria naming each phase's surface,
one session per phase — presented to the operator for approval before it is committed. The operator
chose it at this session's Phase 0 (option A of three) and set the deepest reasoning mode. **Nothing is
implemented, and nothing is outward-facing: no push, no PR, no comment.** Upstream moved today and the
plan starts from it: PR #80's head is `b82dcff` (the maintainer merged `main` into it to clear a
`CHANGELOG.md` conflict), its review is private and pending (F1–F3), and upstream's S16 receipt proposes
a `CHANGELOG.md` heading-count ratchet that would refuse every trim (`aaa6d30` took the headings
80 → 27). Fork `main` now conflicts with `upstream/main` in `CHANGELOG.md` and `HANDOFFS.md`. Carries
the Phase 0 `dashboard_history.jsonl` snapshot.

### 2026-09-14 · [ad hoc] Operator decision: do not trim `CHANGELOG.md`

The operator decided not to trim this ledger, although `methodology_trim.py --check` fires — the file
is past the tool's 196,608 B Class A trigger. It follows the same day's decision that sessions reach the
ledger through git and never read it whole (`3c8acd5`), and S112's precedent of declining a trim that
buys nothing (BL-52). **Expected from now on:** `--check` keeps exiting 1 and the dashboard keeps
showing the trigger; past 262,144 B a default `Read` returns nothing, so read the file with
`offset`/`limit` — verified today on `nprcgenekeepr`'s 413,383 B ledger. Recorded in the S161 receipt's
item (1), in BL-57 (whose plan settles the archive rule), and in memory. Nothing was trimmed.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-14 · [ad hoc] S161 follow-up — BL-57 raised as HIGH PRIORITY on the operator's request: the `CHANGELOG.md` rules contradict each other; a planning session comes next, aiming at an upstream PR

The operator asked for the contradictions to be logged, and for a high-priority future session to plan
removing them in this repo and in `airqino`, `model_project_constructor`, `mts-system`,
`nprcgenekeepr`, `vscode_quarto_ext` and `wsfct`, with the intent of an upstream PR or adding to one.
**BL-57** (`docs/planning/BACKLOG-DETAIL.md`, index row in `docs/planning/BACKLOG.md`, marked HIGH
PRIORITY) records eight contradictions with every cited line re-read today, and a per-repo table of what
the rollout will meet, measured read-only: `nprcgenekeepr` and `wsfct` carry copies of the seed's rules
text, which `bin/sync` never rewrites; three adopter ledgers are already past the 262,144 B default-Read
refusal; four adopters use their own tag styles. A first survey counted "65,536" anywhere in each file
and a second stopped at the seed's example headings, so the table was taken from raw match positions.
The S161 receipt's item (1) now names the planning session first. No plan was written and no other
repository changed.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-14 · [ad hoc] S161 follow-up — `HANDOFFS.md` back to four receipts: the pointer block folded into the archive table

On the operator's request (*"trim HANDOFFS"*), under the retention policy at `HANDOFFS.md:8` (5
receipts against 4). The trim itself is the tool's own entry below (`16ac3fc97`: S157 to
`docs/archive/HANDOFFS-through-2026-09-09-2.md`, 58,802 → 50,737 B, SRF 0.9849 vs `cd52df7` — no
`SRF_RED`, no `--force`). Nothing was added to the ledger before trimming: about 308 B more would have
taken SRF past 1.0 and into the refusal. This commit folds the generated pointer block into the archive
table as one row — in its own commit, since inside the trim commit the shard's proof fails L2 (Learning
#58) — so the table reads 16 trims and 146 receipts, each row cross-checked against the fence count of
the shard it names. The S161 receipt's item (1) now says the `HANDOFFS.md` half is done;
`CHANGELOG.md`'s trim remains the operator's decision.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-14 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-09-09-2.md` (1 record(s), 58,802 B → 50,737 B)

**Written by:** `methodology_trim.py` v1.5.0 — a tool action, not a session's judgment.
Moved the oldest **1** record(s) (2026-09-09 → 2026-09-09) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-09-09-2.md`](docs/archive/HANDOFFS-through-2026-09-09-2.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-09-09-2.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-09-2.md.verify.sh)
rather than trusting a digest printed here. Live file 58,802 B → 50,737 B (−13.7%).

### 2026-09-14 · [ad hoc] S161 follow-up — BL-47 and BL-52 updated now that `CHANGELOG.md` has left the read budget; one false clause in the exclusion note corrected

On the operator's request. **BL-52** gains a fourth addendum: the operator has now decided its byte
half for this repo's `CHANGELOG.md` (`3c8acd5`), on the reasoning its own S98/S112 measurements
supplied (one whole-file read per root ledger in 85 transcripts). It records what stays open: the
trimmer's 196,608 B Class A trigger, which lives in the distributed tool and still fires; the
262,144 B default-Read refusal, the boundary BL-52 says actually bites, about 58 KB away;
`HANDOFFS.md`, still in the budget; and this ledger's own archive rule, still stated against the
2,000-line read-cap proxy. **BL-47** gains a note that its premise moved twice: this repo's config no
longer lists `CHANGELOG.md`, and the trimmer has budgeted to 196,608 B since S116, not 65,536 B.
**Corrected:** the exclusion note said `HANDOFFS.md`'s 65,536 B "backs" `bin/check-handoff`'s
`CEILING_BYTES`; that checker has its own constant and never reads the config, so the entry only
mirrors it. `BACKLOG-DETAIL.md.verify.sh` covers only BL-32 and BL-36, so neither backlog edit touches
its proof.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-14 · [ad hoc] S161 follow-up — `CHANGELOG.md` removed from this repo's read budget on the operator's decision: sessions reach it through git, never read it whole

The operator's rationale: a session looking for something in `CHANGELOG.md` greps it or runs git, so
only those results enter its context — the file is never read whole. The runner agrees: Phase 0 step 6
takes the reconcile's frontier and gap from `git log`, and Phase 3F prepends under the topmost month
heading. So `.context-budget.json` no longer declares it `read-mandated`: its entry (65,536 B, 2,000
lines, 25,000 tokens, plus a heading-shape check) is removed, the reason recorded in
`_deliberate_exclusions`, the old entry recoverable with `git show bb6eb72:.context-budget.json`.
Asserted before writing: the file parses, `files[]` went 7 → 6, and nothing else changed.
`context_budget.py` still exits 2 — rows diffed against the run before the edit: only `CHANGELOG.md`'s
row left, findings 24 → 15, and the reds that remain are the known ones (`SESSION_RUNNER.md` and the
Phase 0 read-set total). **Its size is still bounded:** `methodology_trim.py`'s own 196,608 B trigger
still fires, so S162's trim stands. `HANDOFFS.md` keeps its entry. Canonical-only config; no test reads
it. The checker's two runs, before and after, are appended to `.context-budget-history.jsonl`,
committed here as that append-only history always has been.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-14 · [ad hoc] S161 follow-up — BL-56 raised on the operator's request: rewrite `airqino`'s `CHANGELOG.md` to the current ledger format

The operator asked for a backlog item, not the rewrite. **BL-56** (`docs/planning/BACKLOG-DETAIL.md`,
index row in `docs/planning/BACKLOG.md`): `airqino`'s `CHANGELOG.md` (1,309 B) reads *present (stale
format)* under both `bin/status` versions — it lacks both markers the current seed carries — and the
Route A sync (`dfe26fd17` in `airqino`) left it as it was, since `bin/sync` never rewrites a seed. It
holds one dated entry, the sync's own, so reseeding and carrying that entry across is the cheap remedy
(`starter-kit/BOOTSTRAP.md:86`). Nothing in `airqino` was changed.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-14 · [ad hoc] S161 follow-up — `airqino` synced by Route A on the operator's request: every tracked file current, on a new local branch

Using the S161 document's Route A (`docs/planning/read-set-budgets-local-use-routes.md` §6), from a
pristine full clone of `upstream/read-set-budgets` at `598c459`. The operator chose a new branch,
`chore/methodology-read-set-budgets`, off `airqino`'s open PR #1 branch
(`chore/methodology-pr2527-remediation`, `0c59e5e9`) — the only branch whose files sync without
`--force`, since `main`'s `SESSION_RUNNER.md` and `SAFEGUARDS.md` match no published version. A dry
run against the real project first matched the scratch-copy result exactly. The sync updated 10
files, added 8 and created 2 seeds; `bin/status` now reads every tracked file `current`. Committed in
`airqino` as `dfe26fd17` — 21 files, one commit for one tool-generated sync, with an entry in
`airqino`'s own `CHANGELOG.md`; its two pre-existing untracked files were left untouched. **Not
pushed; PR #1 and `main` unchanged.** The S161 receipt's item (3) records it.

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-14 · [ad hoc] S161 follow-up — BL-55 raised on the operator's request: nothing enforces removing a completed `BACKLOG.md` item

After S161's close-out (`a5ba9ea`) the operator asked for the backlog item its receipt had offered.
**BL-55** (`docs/planning/BACKLOG-DETAIL.md`, index row in `docs/planning/BACKLOG.md`): the removal
rule is required in five places, `starter-kit/SESSION_RUNNER.md:284` first, and checked by none; the
dashboard's Signal F only reports done-marked items. Measured with Signal F, `nprcgenekeepr` went from
28 done-marks (2026-09-11) to 0 after its S687 removed them by hand on 2026-09-14, and its `BACKLOG.md`
from 218,350 B to 102,069 B. A gate keyed on the `[BL-N]` tag would miss that project: its backlog
names no `BL-` id, and 5 of its 322 tagged ledger entries carry one. Options are costed in the item,
none decided; the S161 receipt's item (6) now points to it. The operator's other question — could
Route A run on six named projects — was answered with no change made: re-checked on fresh copies, it
is clean only for `airqino`, identical to 2026-09-11. **Fork-internal; no project was written to.**

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-14 · [ad hoc] S161 close-out — local use of `read-set-budgets` answered; `CHANGELOG.md` now past its trim trigger, so S162 has both ledgers to trim

**The deliverable is done, approved and committed** (`14ffe204`); Learning #64 and BL-54 followed
(`0c81e399`). The S161 receipt carries the verification record, and this entry closes the claim's
`CHANGELOG: pending`. **This entry keeps `CHANGELOG.md` past its 196,608 B trigger, as the operator
chose at Phase 0** — it was 197,584 B before this entry — and `HANDOFFS.md` now holds five receipts
against its policy of four, so **S162 opens with both ledgers to trim.** **One regression, mine,
caught before this close-out:** the claim stub's `key_files` carried no `path:line` token, so
`bin/tests.sh` Test 34 read three extra failures at `18957077f`, `14ffe204` and `0c81e399` (301/4 at
`0c81e399`, found by an intermediate run; S160's claim-time ledger, as a control, passes). This
close-out's receipt replaces the stub, and the live ledger passes `check-handoff --all`. Claimed 2026-09-11 and closed
2026-09-14; before committing the document the session re-checked that nothing it measured had moved
(PR #80 OPEN, 0 reviews, 0 comments; `upstream/main` `512c2ed`; `origin/main` `f8531cf`). It also
answered the operator's mid-session question, read-only: completed `BACKLOG.md` items must be removed
(`starter-kit/SESSION_RUNNER.md:284`), but nothing enforces it — the dashboard's Signal F only reports,
and on `nprcgenekeepr` it counts 28 done-marked items. **Fork-internal: nothing pushed, no PR, no
comment.**

- **Model:** Claude Opus 5 (claude-opus-5)

### 2026-09-14 · [ad hoc] S161 — Learning #64 (a dry run into an empty target cannot exercise a refusal), and BL-54 raised (`bin/sync`'s history walk misses a merge's other side)

Two records of what the deliverable found. **Learning #64** (`starter-kit/FRAMEWORK_LEARNINGS.md`,
952 B): S160 recorded the branch route as working from a dry run into an empty project; run against
copies of the twelve real projects it synced 3 and refused 9. `bin/check-learnings` exit 0, 0 rows over
1,500 B. The file is 76,959 B against its 81,920 B growth warning — **4 rows of room** at BL-53's
1,239 B median. The row is distributed: it reaches projects that sync from fork `main`. **BL-54, raised
on the operator's go-ahead** (`docs/planning/BACKLOG-DETAIL.md`, index row in
`docs/planning/BACKLOG.md`): `bin/sync:60` and `bin/status:56` walk history without `--full-history`, so
a version that exists only on the merged-in side of `213f841` reads as locally modified — measured on 4
files for each of the 3 projects synced from the branch and then from fork `main`. Recorded, not fixed;
neither file is distributed. `BACKLOG-DETAIL.md.verify.sh` exit 0.

- **Model:** Claude Opus 5 (claude-opus-5)

