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

