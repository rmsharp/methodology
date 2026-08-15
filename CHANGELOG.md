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

---

## 2026-08

### 2026-08-15 · [BL-36] ANSWERED — the four failing archive proofs are not evidence of loss; the archives are intact and the fault is in the proofs

**Model:** Claude Opus 5.
One audit, no repair (FM #17 — the repair touches a distributed tool and is its own session).
Report: `docs/audits/2026-08-15-bl36-archive-losslessness.md`. Coverage 9 of 9 archives, 6 of 6
proofs, 6 of 6 trim commits.

**No records were lost.** Re-derived independently — a parser keyed on record *identity* (heading,
or `session|date`) rather than the shipped proof's *position* — giving **0 records missing** across
all six trims and **0 of 228** historical identities unreachable at HEAD across live + all 9
archives. All six trimmer-declared counts (10, 70, 68, 16, 30, 25) reproduce exactly, which is
corroboration from a different program at a different time. The detector was mutation-proved able to
fail *before* its zero was believed (Learning #16): a deleted shard record → 1 missing, an altered
one → 1 changed, a 5-record truncation → 5 missing, silent on the unmutated artifact, each mutant
asserting that it actually applied.

**Root cause: `injected = 1 if trims_the_ledger else 0`** (`starter-kit/methodology_trim.py:1715`,
`:1736`) is a 0/1 flag meaning *"does the trim write its own ledger entry"*, never a count of what
the trim commit added. The generated proof's positional identity therefore breaks by construction on
any trim bundled with other same-ledger edits — two extra records (`73≠72`), three (`77≠75`), or a
frontier receipt finalized `pending → complete` inside the trim commit (`record [0]`).

**BL-36's version correlation was a confound, and catching it changed the repair.** All four failing
shards came from *bundled* trim commits and both passing ones from *standalone* trims, so generator
version and commit shape are collinear across the shipped six. The off-diagonal cells were executed,
not argued: **v1.1.3 logic fails all four bundled trims with identical text** (plus the BL-27 `NOTE:`
on the two `HANDOFFS` cases), and **v1.1.1 logic passes the standalone `CHANGELOG` trim**. So two
independent defects had been fused into one correlation — **A: bundling**, present in every version,
causal, and deliberately retained as a loud FAIL by BL-27's own fix 2; **B: the regenerated
front-matter count line**, genuinely fixed v1.1.1 → v1.1.3. Consequence: **regenerating the four
proofs would not fix them**, which is measured rather than predicted.

**Four minor findings.** BL-27's explanatory `NOTE` is gated on `bad == [0]`, so it never fires for a
bundled `CHANGELOG` trim — the busier ledger's likeliest bundling still fails mute. 3 of 9 archives
predate the trimmer and ship no proof at all. `CHANGELOG-through-v3.6.md` is the one shard not
byte-frozen since its creating commit (S31 corrected its front matter; all 50 dated records verified
byte-identical). And the answer already existed: **BL-27** (`docs/planning/BACKLOG.md:975`) states
*"This is not evidence of historical data loss"* and predicts this exact re-raise — unfound because
that file is 1,518 lines / 134,759 B, 2.06× the budget its own ledgers are held to, with no
reduction step reaching it (**BL-32**, open). Nothing in `docs/archive/` was modified by this audit.

### 2026-08-15 · [ad hoc] S87 close-out — receipt written, self-score 8/10; see the two `Ledger trim` entries below for the substantive work

**Model:** Claude Opus 5.
Phase 3A/3B/3D. Evaluated S86's handoff (**8/10** — its `runtime_smoke` baseline of 228/229 with
Test 9 as the sole known failure is what let this session read a mid-run 227/2 as one new breakage
rather than noise; docked for closing with both mandated-read ledgers 2–4× over their declared
65,536 B budget without naming it, which is FM #28's own degradation sign, and for the FM #27 gap
backfilled here at Phase 0). Self-assessed 8/10: treated the trimmer's `P1_UNDOCUMENTED` refusal as
information rather than an obstacle, measured three cut options instead of arguing them, established
the `HANDOFFS.md` date-cut hazard by running it, and — after the suite went red immediately
following its own change — ran the pre-change tree in a detached worktree before claiming
responsibility, which is what separated one real self-inflicted breakage from four pre-existing
failures. Held back for nearly shipping a verification pass that checked only the two proofs this
session wrote (broadening it is the sole reason BL-36 exists), and for leaving BL-36's cause
excluded-but-unproven.

**This entry deliberately restores the convention that lapsed after S79.** A close-out receipt commit
is written after the ledger commit that would have to cite it, so it can never record itself; S80,
S81, S83, S84, S85 and S86 each left one unrecorded, and frontier-based reconcile can only ever see
the newest. Writing the close-out entry *with* the ledger commit — the S62–S79 shape — is one of the
two clean options (S82's bundled single commit is the other). The historical gap remains open and is
flagged in this session's `8a22608` backfill entry below.

### 2026-08-15 · [BL-36] Four of the six shipped `.verify.sh` losslessness proofs do not hold — raised, not fixed

**Model:** Claude Opus 5.
Found while re-running *every* archive verifier after this session's two trims, rather than only the
two it had just written. Four fail: both v1.1.1-generated `CHANGELOG` proofs (L1 not byte-identical;
L3 counts 73≠72 and 77≠75) and both v1.1.1-generated `HANDOFFS` proofs (L1/L2 plus record `[0]` not
byte-identical). The two this session generated with v1.1.3 pass.

**Not caused by this session — measured, not assumed.** All four fail identically in a detached
worktree at `8a22608` (S86's tip, before S87's first commit). The generator version correlates
perfectly, which points at the class BL-27/BL-28 fixed in v1.1.2/v1.1.3, but the entry asserts no
cause: the competing *"a later trim invalidated an older proof"* explanation is unlikely on
inspection — each script freezes its derivation at its own trim commit via `TRIM_SHA` and three
`git show` reads, so it is not a function of `HEAD` — and unlikely is not disproved.

**Deliberately not fixed here** (FM #17): the repair depends on an answer this session did not have
budget to establish — whether the four archives' content is genuinely intact and only the proofs are
stale, or whether records were actually lost. Those are different repairs, and regenerating the
scripts first would make a passing proof over lost content, destroying the only evidence. Full item,
reproduction command and next-session instruction: `docs/planning/BACKLOG.md` **BL-36**.

### 2026-08-15 · [ad hoc] Framework Learning #24 appended — a check keyed on the live file has a population the protocol's own reduction step can move

**Model:** Claude Opus 5.
Phase 3C. Appended row **24** to [`starter-kit/FRAMEWORK_LEARNINGS.md`](starter-kit/FRAMEWORK_LEARNINGS.md) (append-only; `#14` stays reserved, so the
table now runs 1–13, 15–24 and `bin/check-learnings` reports 23 rows, contiguous, all citations
resolving). The learning generalizes this session's own Test 29 breakage: FM #28 makes archiving a
*routine, mandated* act, which silently makes every check keyed on a live file conditional on where
its population currently lives — and such a check's empty state surfaces as "failed", not as
"nothing to check". Carries the repair (define the population as the whole ledger, live + archives)
and the constraint on it (prove the widened arm can actually fail, or it is Learning #16's tautology
in a new place). Corpus re-grepped for stale set-size claims per Learning #7: none — no document
hardcodes a learnings count, and `bin/check-learnings` derives contiguity dynamically.

### 2026-08-15 · [ad hoc] `bin/tests.sh` Test 29 now reads the archives, not only the live `CHANGELOG.md`

**Model:** Claude Opus 5.
Fixes a test the same session's own archive turned red — found by running the suite, not predicted.

- **The defect.** Test 29's budget check keyed on `CHANGELOG.md` alone, and its pass condition is
  `RECON_COUNT > 0 && RECON_VIOLATIONS == 0`. The trim above moved all **10** remaining
  `Reconcile-on-read` entries into `docs/archive/CHANGELOG-through-2026-08-11.md`, so the live count
  fell to **0** and the test failed with an *empty* violation list — reporting
  `budget violated -- ` with nothing after the dash. Nothing had eroded; the population had moved.
- **Not a new lesson.** This is the blind spot `CHANGELOG.md`'s own source-tag audit already fixed
  for itself ("after the split it would have stopped counting the archived entries at all"), and the
  same *"found nothing" vs. "could not read this"* conflation `methodology_trim.py`'s
  `classify_empty` was widened for (UAT F1). Test 29 had the identical shape and had simply never
  been trimmed past before.
- **Fix.** The check now reads `CHANGELOG.md` **plus** `docs/archive/CHANGELOG-*.md`; violation
  messages carry the shard basename. The population is the whole ledger — which is where the norm
  has to hold — not whichever shard happens to be live today. **43** entries across 4 files, 0
  violations. The pass message no longer says "live", which had become false.
- **The archive arm is a real guard, proved rather than assumed.** Appending a synthetic 20-line
  discharge entry to an *archive* shard on a scratch copy moves the check `43/0 violations` →
  `44/1 violation`. Without that, the widened arm could have inflated the count while being
  incapable of ever failing. The pre-existing scratch-copy RED proof (`bin/tests.sh:1786`) is
  unchanged and still passes.
- **Verified:** `bash bin/tests.sh` **228 passed, 1 failed** — back to the S86 baseline exactly, the
  sole failure being Test 9's pre-existing, unrelated github-source gap.

### 2026-08-15 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-08-11.md` (25 record(s), 247,188 B → 32,649 B)

**Written by:** `methodology_trim.py` v1.1.3 — a tool action, not a session's judgment.
Moved the oldest **25** record(s) (2026-08-02 → 2026-08-11) out of [`HANDOFFS.md`](HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-08-11.md`](docs/archive/HANDOFFS-through-2026-08-11.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-08-11.md.verify.sh`](docs/archive/HANDOFFS-through-2026-08-11.md.verify.sh)
rather than trusting a digest printed here. Live file 247,188 B → 32,649 B (−86.8%).

### 2026-08-15 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-08-11.md` (68 record(s), 122,600 B → 25,165 B)

**Written by:** `methodology_trim.py` v1.1.3 — a tool action, not a session's judgment.
Moved the oldest **68** record(s) (2026-08-02 → 2026-08-11) out of [`CHANGELOG.md`](CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-08-11.md`](docs/archive/CHANGELOG-through-2026-08-11.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-08-11.md.verify.sh`](docs/archive/CHANGELOG-through-2026-08-11.md.verify.sh)
rather than trusting a digest printed here. Live file 122,600 B → 25,165 B (−79.5%).

### 2026-08-15 · [ad hoc] S87 claim commit `4825586` recorded — the trimmer's P1 guard requires an empty undocumented set

**Model:** Claude Opus 5.
Records this session's own Phase 1B claim (`4825586`, the `status: pending` S87 receipt). Written
**before** Phase 3F rather than at it, because `methodology_trim.py`'s `check_P1` refused both
planned trims while the undocumented set was non-empty:

> `[P1_UNDOCUMENTED]` the undocumented set is non-empty (1 commit(s) since the ledger frontier
> `11b44dc`). A trim commit advances that frontier and would hide them PERMANENTLY. Reconcile
> first, then trim.

The refusal is correct and was **not** worked around: a trim rewrites `CHANGELOG.md`, which advances
the Phase 0 frontier past any commit never recorded, so the claim commit would have become
permanently invisible to reconcile-on-read. `--force` would not have applied anyway — it is scoped
to the SRF-RED refusal, not this one.

**The interaction is worth naming for the next session that trims:** Phase 1B mandates a claim
commit, and that commit is itself an unrecorded action until Phase 3F — so *any* session that claims
correctly and then trims will hit `P1_UNDOCUMENTED`. The order that works is claim → record the
claim → trim, not claim → trim. Recorded as an observation, not a defect: the guard is doing
precisely its job, and the tool writes its own ledger entry per trim (`build_ledger_entry`,
`starter-kit/methodology_trim.py:980`), asserted afterwards by `check_P1a`.

### 2026-08-15 · [ad hoc] Backfilled (reconcile-on-read): undocumented commit `8a22608` — S86's own close-out receipt commit

**Model:** Claude Opus 5.
Phase 0 step 6 of the next session. Frontier `git log -1 --format=%H -- CHANGELOG.md` = `f8f32ea`
(S86's ledger commit); `git rev-list --count --no-merges f8f32ea..HEAD` = **1** — `8a22608`,
`docs(handoffs): S86 close-out`, which wrote S86's `HANDOFFS.md` receipt and nothing else. It is an
action this repository took and never logged (FM #27), so it is recorded here rather than left to
`git log`. `HANDOFFS.md` needed no parallel reconcile: its own frontier **is** `8a22608`, nothing
follows it, and the receipt it carries is `status: complete` with `commit: f8f32ea` already filled —
so the `commit: pending` chicken-egg shape discharged 41 times through S69 does not apply here.

**The gap is structural, and wider than the one commit this frontier can see.** A close-out receipt
commit is written *after* the ledger commit it would have to cite, so it can never record itself;
the only two clean shapes are S82's (`62168e6` — ledger and receipt in one commit) or S62–S79's
(a pre-written `[ad hoc] S<N> close-out — receipt written, self-score …` entry riding the ledger
commit, 15 of them in this file). That convention lapsed after S79: **S80 (`ca1261e`), S81
(`0a5b723`), S83 (`bb2c8af`), S84 (`b4780ec`), S85 (`d36a61e`) and S86 (`8a22608`) each left a
close-out commit with no ledger entry** — measured, not inferred (`grep -cE '^### .*S<N> close-out'`
returns 0 for each). Frontier-based reconcile structurally cannot reach the first five: each
session's own ledger commit moves the frontier past its predecessor's close-out commit, so only the
newest is ever visible. Recorded as a finding for the operator; **not** fixed here — a backfill of
five historical commits, or a change to the close-out convention, is a deliverable that needs its
own session and its own go-ahead (FM #17).

### 2026-08-12 · [BL-34] Local `main` synced with `upstream/main` (v3.7 release + issue #67 fix) — the 4-file conflict resolved

**Model:** Claude Sonnet 5.
Operator-directed: sync local `main` with `upstream/main` now, resolving BL-34's 4-file conflict
(`[BL-34]` entry above, S85). Fetching first showed the conflict had grown past what S85 scoped —
upstream had moved from `5c59f0b` to `dcb6fc6`, three commits further: PR #73 (issue #67's own
independent stale-copy fix) and PR #74 (the v3.7 release itself). Re-derived the real shape rather
than trusting the stale snapshot (Learning #13) and resolved the full scope: `git merge
upstream/main --no-commit --no-ff`, 6 conflicting files, no strategy shortcut, real 3-way merge
`aa378ab`.

- **`CLAUDE.md` + `docs/RELEASE_HISTORY.md`:** kept this fork's own history extraction (BL-9 L3)
  over upstream's reintroduced inline version list; appended upstream's new v3.7 entry to
  `RELEASE_HISTORY.md` with a fork note — every functional item it bundles had already reached
  this fork independently before the tag (issue #65's structural tests + FM #28 via S83's earlier
  merge; BL-34's R/Quarto/RMarkdown fix; this fork's own S62 fix for issue #67), so the entry
  records the upstream release as a fact, not new functional content landing here.
- **`CHANGELOG.md`:** upstream's newer-dated entries (the v3.7 release narration, the issue #67
  fix) placed above this fork's own 2026-08-11 entries. Dropped one orphaned duplicate — upstream's
  own narration of PR #71 (`_FRAMEWORK_FILE_SIGNATURES`), the same event this fork's existing
  `[BL-31]` entries already cover from S83's earlier merge, which kept this fork's own
  `_FRAMEWORK_INSTALLED_CONTENT` design over that same PR's dict-shaped one.
- **`tools/methodology_dashboard.py` + `starter-kit/` twin (7 conflicts):** kept this fork's own
  BL-34 comments and `DASHBOARD_VERSION` (`2.15.2`) throughout — functionally identical to
  upstream's leaner, fork-vocabulary-free wording (written for the upstream-targeted branch, not
  this file). For issue #67's stale-copy remedy, kept this fork's own `--sync [DIR]` single-project
  scoping design over upstream's `cp`-based one: more general (reuses the existing sync mechanism
  rather than bypassing it), and already covered by roughly 15 existing Row 13/14 tests
  (`test_sync_accepts_a_single_target_directory`, `test_bare_dry_run_without_sync_errors_and_writes_
  nothing`, `test_sync_end_to_end_via_main_writes_only_the_target`, etc.) that upstream's simpler
  design has no equivalent for.
- **`tools/test_methodology_dashboard.py` (8 conflicts):** kept BL-34 comment flavor throughout;
  adopted upstream's new `test_rmd_analysis_repo_flips_doc_only_and_softens_the_test_risk` (genuinely
  new — it only ever existed on the separate PR #72 branch, never merged into this fork's own
  `main`). Dropped upstream's whole `TestCliRemedyProportionality` class as redundant with this
  fork's own more thorough `--sync`-target coverage — one of its assertions
  (`self.assertIn("cp ", err, ...)`) would have failed against this fork's correct, already-tested
  `--sync [DIR]` design, catching a difference in implementation shape, not a real defect.
- **`README.md` (auto-merged cleanly, no conflict):** its new "What's New in v3.7" section, inherited
  verbatim from upstream, described the `cp`-based stale-copy remedy — inaccurate against what this
  fork actually ships. Corrected the one bullet to describe the `--sync [DIR]` design instead.
- **`HANDOFFS.md` (3 conflicts):** upstream's **S11** (issue #67's fix) merged in. Dated
  2026-08-12 — later than this session's own 2026-08-11 entries — but placed BELOW this session's
  own **S86** stub rather than above it: `check-handoff --allow-pending` exempts only the file's
  literal newest block, so a later-dated but still-`pending` receipt sitting above an in-flight one
  breaks the exemption (found live — two stacked pending stubs, both flagged red even with
  `--allow-pending`). Upstream's own **S12** (the v3.6→v3.7 release-cutting session, still
  `status: pending` at `upstream/main`'s own tip) is deliberately **not** recorded here — a pending
  stub is a live claim in progress, not settled history, and belongs in this ledger once upstream
  completes or abandons it; a future sync should re-check for that rather than assume this one
  reconciled it. Receipt count corrected 24 → 28 (was already stale before this merge, per the
  section's own "unguarded" warning).

**Verified:** `python3 -m unittest tools.test_methodology_dashboard` 300/300; `bash bin/tests.sh`
228/229 (Test 9's pre-existing, unrelated github-source gap aside); `bin/check-links` OK (88/22);
`bin/check-learnings` OK (22 rows, 0 findings); `bin/check-handoff --all --allow-pending` OK (28
receipts, fences balanced, no duplicate session+date); twins byte-identical throughout.

### 2026-08-12 · [ad hoc] Released v3.7 — the artifacts Phase 0 mandates reading now have ceilings

- **Change:** release narration commit on `release/v3.7` — `README.md` §What's New in v3.7 (folding
  in the stale "Since v3.6 (unreleased)" section), `CLAUDE.md` §Versioning entry, and the
  "Current version" line 3.6 → 3.7. Cite-don't-restate: the full narrative lives in
  [`CLAUDE.md` §Versioning "v3.7"](CLAUDE.md#versioning); this entry is the action record.
- **Scope:** 38 commits and 13 ledger entries since `v3.6` (`d7a482a`). **Minor**, not patch,
  because the framework gained a failure mode (**#28**, count 27 → 28 — the first since v3.1) and a
  new distributed tool (`starter-kit/context_budget.py`, TRACKED, with a SEED config). **Not major**
  because no principle, phase, gate, or workstream changed. Learnings 12 → 13; `DASHBOARD_VERSION`
  2.10.2 → 2.10.6 across four separate fixes; `bin/tests.sh` 84 → 114; unit suite 197 → 211.
- **The "unreleased" README section was stale and is why this was worth catching.** It still ended
  *"the failure-mode count stays 27"* — written before PR #66 appended FM #28, and true when
  written. A section that describes itself as pending release is exactly the text nobody re-reads;
  it is Learning #7's cross-reference problem applied to the release notes themselves.
- **Tag and Release are recorded in a follow-up entry, not predicted here.** A tag SHA that does not
  exist yet is a forward-looking claim, and Learning #13 says to compute those rather than assert
  them — so the tag/Release facts are appended once the action has actually happened.

### 2026-08-12 · [issue #67] The stale-copy warning now names a remedy proportionate to the finding, and bare `--dry-run` no longer writes

- **Change:** `tools/methodology_dashboard.py` (+ `starter-kit/` twin, kept byte-identical) and
  `tools/test_methodology_dashboard.py`. `DASHBOARD_VERSION` 2.10.5 → 2.10.6. Closes
  [issue #67](https://github.com/KJ5HST/methodology/issues/67).
- **Defect 1 — a disproportionate remedy.** `check_stale_version()` answered "this one copy is
  old" with `Re-sync: python3 <canonical> --sync`. But `--sync` is scoped from the **canonical's
  own location**, not the working directory, so it rewrites every discovered sibling — measured at
  26 files across 25 repos, including 7 creates in repos that do not gitignore the path and 1
  where the file is git-tracked. An adopter following a one-line instruction verbatim dirtied
  eight unrelated repositories. The warning now leads with the safe per-project action
  (`cp <canonical> <this copy>`) and offers the portfolio path only as `--sync --dry-run`, with
  its scope stated. **Why it matters beyond tidiness:** a remedy nobody can safely run is one
  mechanism behind an *ignored* warning — in one adopter this line rode ~28 consecutive handoffs
  unacted-on. The measurement was never missing; the actionable remedy was.
- **Defect 2 — a flag named `--dry-run` that writes.** It was consulted only inside the `--sync`
  branch, so bare `--dry-run` fell through to a full scan and wrote `dashboard.html` *and*
  appended to `dashboard_history.jsonl`. It is now an error (exit 2) that writes nothing.
  Refusing rather than silently no-opping is deliberate: a silent no-op leaves the caller unable
  to distinguish "nothing to do" from "flag ignored" — the same unreadable-signal class as
  defect 1.
- **Tests:** new `TestCliRemedyProportionality` (3 cases, unit suite 208 → 211). Both defect
  tests were driven RED against the pre-fix scanner and the failing run read, not assumed;
  the third is a presence control (a plain run must still write `dashboard.html`), without which
  a scanner that refused *every* invocation would pass and look fixed.
- **Scope deliberately not taken:** the issue also suggests `--sync-self` and a `--yes` gate on
  `--sync`. Both change the CLI contract rather than fix a defect, so they are left for a
  separate deliverable; the `cp` line already gives the per-project remedy with no new surface.
- **Distribution:** the scanner is `bin/_manifest.py`-TRACKED, so adopters receive both fixes via
  `bin/sync`.

