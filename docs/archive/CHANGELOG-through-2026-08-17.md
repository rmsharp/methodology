# CHANGELOG.md — archive: 2026-08-15 → 2026-08-17

Retired records from [`CHANGELOG.md`](../../CHANGELOG.md), moved here so the live ledger stays small enough to read
in one pass. Same format, same newest-on-top order — this is the same ledger, continued.

Holds **26 record(s), 2026-08-15 → 2026-08-17**. Cut key: `2026-08-17`. Counts here are computed from the file
itself, never carried forward. This shard is frozen: it states no forward-looking rule,
because the live file owns those and a copy of one was wrong a day after it was written.

---

### 2026-08-17 · [ad hoc] S97 close-out — receipt written, self-score 7/10, predecessor S96 scored 9/10

Phase 3D receipt in [`HANDOFFS.md`](../../HANDOFFS.md); the substantive work is the entry below. Telemetry
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

Phase 1B claim; receipt stub in [`HANDOFFS.md`](../../HANDOFFS.md) with `status: pending`. The subject is
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
(70.6% of row bytes) and no distributed citations, but [Learning #29](../../starter-kit/FRAMEWORK_LEARNINGS.md)
— ratified five sessions ago — is precisely the finding that an uncited rule is *orphaned*, not
worthless. Citation count is not an archive criterion.

**Model:** Claude Opus 5 (1M context).

### 2026-08-17 · [ad hoc] S96 close-out — receipt written, self-score 8/10, predecessor S95 scored 9/10

Phase 3D receipt in [`HANDOFFS.md`](../../HANDOFFS.md); the substantive work is the BL-40 entry below.
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
[Learning #31](../../starter-kit/FRAMEWORK_LEARNINGS.md) itself prescribes: assert the population, skip
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
derived from a stale distribution, which is [Learning #12](../../starter-kit/FRAMEWORK_LEARNINGS.md)'s shape
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

[`HANDOFFS.md:8`](../../HANDOFFS.md) read **3** while the file held **4**. Not a new defect and not a
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
[`docs/archive/CHANGELOG-through-2026-08-15.md`](../../docs/archive/CHANGELOG-through-2026-08-15.md)).

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

Appended to [`starter-kit/FRAMEWORK_LEARNINGS.md`](../../starter-kit/FRAMEWORK_LEARNINGS.md) (DISTRIBUTED;
55,193 → 57,964 B, leaving **2,036 B** under its 60,000 B ceiling — one more row of this size breaches
it). Sibling of Learning #31: #31's coupling is *dimensional* (a fixture needs at least three records,
so a count check finds it), while #32's is *content* — which records survive, not how many. A
positional trimmer has no vocabulary for "retain at least one record satisfying P", and a dry run
reports bytes and counts, the exact quantities such a floor is invisible to.

**Model:** Claude Opus 5 (1M context).

### 2026-08-17 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-08-15.md` (28 record(s), 84,765 B → 31,539 B)

**Written by:** `methodology_trim.py` v1.2.0 — a tool action, not a session's judgment.
Moved the oldest **28** record(s) (2026-08-12 → 2026-08-15) out of [`CHANGELOG.md`](../../CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-08-15.md`](../../docs/archive/CHANGELOG-through-2026-08-15.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-08-15.md.verify.sh`](../../docs/archive/CHANGELOG-through-2026-08-15.md.verify.sh)
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
Moved the oldest **8** record(s) (2026-08-11 → 2026-08-15) out of [`HANDOFFS.md`](../../HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-08-15.md`](../../docs/archive/HANDOFFS-through-2026-08-15.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-08-15.md.verify.sh`](../../docs/archive/HANDOFFS-through-2026-08-15.md.verify.sh)
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

