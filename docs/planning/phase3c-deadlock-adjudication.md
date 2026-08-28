# The Phase 3C "deadlock" — adjudicated

**Status: ADJUDICATION. Awaiting the operator's ratification. No remedy is applied by this document.**
S121's deliverable, against the finding S120 recorded in its `HANDOFFS.md` receipt. The
Present→Implement gate holds: nothing is compacted, retired, split, or re-ceilinged until the
operator chooses. Implementation, if ratified, is a separate session.

> **Declared budget: 35,000 B.** File 34 in `docs/planning/`, which has no ceiling — the same
> instance-of-the-problem this directory always is. Stated rather than discovered.

**Method note.** Every number below is measured, and the load-bearing ones were re-measured by an
independent agent that was told to refute them. Where a figure is a *band*, it is written as a band.
**Six of my own numbers were wrong and are corrected in place, marked ⚠ — including two that repeat,
one level down, the exact error this document faults S120 for.**

---

## 1. The finding under adjudication

> *"`starter-kit/FRAMEWORK_LEARNINGS.md` is **56,673 B with 77 B of headroom** under the 56,750 B
> one-read cap; the **smallest row it has ever carried is 229 B**, so an append of *any* size
> overshoots by ≥152 B. **The framework's own mandatory close-out step cannot be performed against
> its own published budget.** … no ceiling answers the underlying policy question of how many
> learnings the framework should carry."* — S120, `HANDOFFS.md` `next_steps` (b)

**Verdict: the deadlock is not real. The arithmetic is right and the denominator is wrong.**
But S120 was not freelancing, the file *has* a real problem, and it is not the one reported.

---

## 2. Why there is no deadlock

### 2.1 Metered, the file is at 78.5% of one read

The 25,000-token `Read` cap is denominated in **tokens**. Metered by the framework's own doubled-file
method (`upstream-read-set-pr-plan.md` §7 — an over-cap explicit range is refused with an exact token
count and returns no content, so the probe costs nothing):

| probe | bytes | tokens | predicted |
|---|---:|---:|---:|
| 2× | 113,346 | 39,229 | — |
| 3× | 170,019 | 58,841 | — |
| 4× | 226,692 | 78,453 | — |
| 5× | 283,365 | **98,065** | 98,065 ✓ |
| 6× | 340,038 | **117,677** | 117,677 ✓ |
| 7× | 396,711 | **137,289** | 137,289 ✓ |

Six collinear points, **zero residual** on the three the model never saw. The concatenation seam was
*measured*, not assumed away: five 158-line windows of byte-identical content — some with one internal
seam, some with two — all report **39,229**, so the seam costs **exactly zero tokens**. The model
therefore collapses to `f(n) = 19,612n + 5`, and

> **`f(1)` = 19,617 tokens = 78.5% of the cap. Headroom: 5,383 tokens.** This is a *measurement*, not
> an extrapolation.

The counter is a pure function of the requested range's **raw bytes** — three byte-identical windows at
line numbers 1–158, 80–237 and 396–553 all report 39,229, so `cat -n` prefixes are not counted — and it
is provably the quantity the gate enforces: 126 lines (72,195 B, ~24,988 tok) is **delivered whole**;
127 lines (73,646 B) is **refused at 25,486 tok**. The flip sits exactly where the counter crosses
25,000.

### 2.2 The 56,750 B figure is applied to this file by no code path in the repo

`READ_CAP_BYTES` is `25,000 × MIN_BYTES_PER_TOKEN (2.27)` at `starter-kit/methodology_trim.py:129`,
and `:120-123` documents 2.27 as the deliberately conservative **floor** of a measured 2.2705–3.0300
band, chosen *"because a guard that must not stay silent on a truncating file has to assume the
densest content it will meet."* It is a **detector sensitivity**, not a budget. Verified:

- `methodology_trim.py --file starter-kit/FRAMEWORK_LEARNINGS.md --check` → **`[NO_CONFIG]`, exit 3**.
  Its `LEDGERS` table holds only `CHANGELOG.md` and `HANDOFFS.md`.
- Both dashboard twins' `read_cap_class()` → **`None`**, for the canonical path *and* the adopter dest.
- `bin/check-learnings` has **no whole-file arm** at all.

The governing ceiling is `.context-budget.json`'s `max_bytes` **73,728**, and `context_budget.py`
reports `starter-kit/FRAMEWORK_LEARNINGS.md 56,673 B / 73,728 B **ok**`. *(The `class` label carries no
size semantics — `max_bytes` alone imposes the ceiling.)*

⚠ **A refutation I published and now withdraw.** I argued the config "refutes itself" because
`73,728 / 2.8 = 26,331 tokens > 25,000`. **That division is unsound**: the config's own note and
`methodology_trim.py:124-126` both state `bytes_per_token` is calibrated on *opening context against
`CLAUDE.md`'s size* — a quantity the repo explicitly declares non-comparable. The sound proof is the
direct read in §4, not the arithmetic.

### 2.3 The per-file axis was already adjudicated away — by a row in this very table

**Learning #34** (`starter-kit/FRAMEWORK_LEARNINGS.md:66`, S97):

> *"**A ceiling guards a cost — measure whether that cost is ever paid, and in what UNIT, before
> trusting the number.** A file-size ceiling only bites when the file is read WHOLE. Measured over 80
> transcripts, one such file was read whole once and in part 243 times, and a partial read returns
> whole ROWS. The cost was per-row; the guard was per-file. **A budget on the wrong unit is not
> conservative, it is unmeasured.**"*

The file's own front matter (`:13-18`) publishes the consequence: **the budget that governs is 1,500 B
per row.** `bin/check-learnings` exits **0** — *46 rows, contiguous, all citations resolve, 0 over
1,500 B*.

### 2.4 No tool would have refused the append

⚠ **My "63.6% of sessions appended" is real but was the wrong statistic, and it is contaminated by the
very blockage it was offered to disprove.** The distribution is **bimodal, not a base rate**:

| window | appended | note |
|---|---|---|
| S87–S98 | **12/12 (100%)** | ample headroom |
| S99–S113 | 3/15 (20%) | the file sat **16 B** under its ceiling |
| S114–S119 | **6/6 (100%)** | after the BL-45 raise |

**When the file has room, essentially every session appends.** So the textual point — Phase 3C routes
*framework-level* learnings and no gate fires when a session appends none — stands, but it does **not**
license "this rarely matters." It matters nearly every session.

The decisive precedent is **BL-45**: S120's finding almost verbatim (*"This blocks Phase 3C for the
next session … that session cannot discharge it"*), during which **S110–S114 ran and closed normally**,
resolved by raising the ceiling and backfilling four rows for five "owed" sessions.

⚠ Also corrected: **S112 contributed zero rows** (I said three); the multi-row session is **S114**, with
four (#39–#42). And **the string "append a Learning row" is not a quotation from Phase 3C** — it appears
nowhere in the protocol. I introduced it into the record in my own claim commit `43387e1` by quoting
S120's paraphrase as if it were the protocol's words.

---

## 3. What S120 got right, and what the record should say instead

**S120 was applying its own ratified plan's standard.** `upstream-read-set-pr-plan.md` sets 56,750 B as
this file's acceptance standard at `:95`, `:106` and `:123`. **The defect is in the plan, not in
S120's arithmetic.** The honest restatement of the finding is not *"cannot be performed"* but
*"would breach the standard this plan sets."*

**S120's second reason is real, was never refuted, and this document must answer it.** The receipt gives
*two* grounds: the cap, **and** *"it would break the byte-identity that lets `bin/sync` agree from either
source."* Verified — `HEAD` and `port/framework-learnings-extraction` carry the **identical blob
`b21854cc`**. The instrument correction dissolves the first ground and leaves the second untouched. See
§6(4).

**S119's compaction was not wasted, and `364b410` must not be reverted.** It had two authorising legs.
**Leg 1 — the published 1,500 B row budget — justifies every row it touched**: 20 real violators, the
checker driven RED in its own commit (`28551a5`), and decisively, the 18-row option leaves #12 (1,451 B)
and #13 (1,447 B) in breach, so **only** the 20-row option turns the checker green. Reverting would
restore 20 violations. **Leg 2 — the file-level 55,930 B arithmetic — does not survive**: the
*pre-compaction* file (74,171 B) meters **24,363 tok = 97.45% of one read**. It fit. Nothing was ever
over.

**The operator chose on a mis-scaled column, and is entitled to be told.** `CHANGELOG.md:456`'s decision
table scored the options in a *"vs the 56,750 B one-read cap"* column, marking the 18-row option
*"401 B OVER"* and the 20-row option *"571 B UNDER"*. At the true cliff for that content (~76,111 B)
**both options were ~19,000 B under** — the deciding margin was mis-scaled by roughly 19 KB. The same
choice is independently correct on the row budget (Leg 1), so **the outcome does not change** — but that
is a finding to report, not an assumption an agent may make on the operator's behalf.

---

## 4. The real defect — the ceiling now certifies a file that does not fit

BL-45 (`b26bb63`, two days before S120) set the ceiling from four costed options and stated its rule:

> *"MEASURED THREE TIMES … 3.0300 B/token and a one-read cliff at 75,751 B. **73,728 IS DELIBERATELY
> 2,023 B UNDER THE CLIFF** … **A ceiling must sit below where the file stops fitting, not on it.**"*

S119 then compacted the file, and **compaction is precisely the operation that lowers bytes-per-token**
— Learning #46's own mechanism. Density fell 3.0444 → 2.8897. Measured, not modelled:

> **73,646 B of this content — 82 B *under* the declared 73,728 B ceiling — is refused at 25,486
> tokens.** A bare read of it returns a `PARTIAL view` banner delivering 106 of 128 lines.
> **The ceiling certifies as `ok` a size at which the file provably does not fit in one read.**

BL-45's deliberate safety margin is consumed and inverted. **Root cause: a byte ceiling is
`tokens × density`, density is a property of content, and compaction changes it — so the ceiling rots
silently, and nothing goes red.** The framework's most recent remedy committed the error its own
Learning #46 records.

**The recurrence, which is the finding that actually matters.** Row size correlates near-deterministically
with headroom *available at write time*:

| headroom at write | 604 | 5,067 | 3,847 | 2,410 | 997 | 4,045 | 2,546 | 1,082 | 245 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| row written | **#34 = 604** | #35 = 1,220 | #36 = 1,437 | #37 = 1,413 | **#38 = 981** | #43 = 1,499 | #44 = 1,464 | **#45 = 837** | **#46 = 229** |

**Whenever headroom falls below ~1,500 B, the row written equals the headroom minus a few bytes.** The
file has saturated against its ceiling **four times** (S97, S109, S118, S120). The defect is not a
blocked append — it is a **silent quality tax on the append**. That also makes the 229 B row circular
evidence: it is 229 B *because* S118 squeezed it into 245 B of headroom, not because rows can be that
small. Before the extraction the all-time minimum was **419 B**, and the table's pre-extraction history
lives in `SESSION_RUNNER.md` (born `a706558f`, moved at `ed22ace`) — a population S120's "smallest it has
ever carried" did not search.

---

## 5. Corrected capacity — and the unit it must be stated in

⚠ **My headroom figures were wrong twice, both times by converting tokens to bytes at the whole-file
density. That is Learning #46/#42 committed one level down, by me, in a document faulting S120 for it.**

Measured marginal cost of **real** learning rows (#39–#42 duplicated; x2 = 41,833 tok, x3 = 62,747 tok):

> **4,163 B of rows = 1,302 tokens → 3.1974 B/token.** Rows are **less dense** than the whole file
> (2.8897), so converting headroom at the file's density **understates** capacity.

| statement | value |
|---|---|
| **Headroom, in the only safe unit** | **5,383 tokens** |
| at a budget-filling 1,500 B row (~469 tok) | **11.5 rows** |
| at the #39–#42 mean 1,041 B row (~325 tok) | **16.5 rows** |

Superseded: my "~11 rows", "8–13 rows", and the steelman's "6.7–10.7" — all low, all computed from a
byte figure rather than a measured per-row token cost. **State the headroom in tokens.**

---

## 6. Recommendation

**Primary: fix the instrument, not the file. No size remedy.** Five of six candidates were evaluated and
rejected — a second compaction (**there is no breach to remedy**; `check-learnings` is green, so every
byte removed is discretionary against the file's own *"said shorter without saying less"* rule, the
criterion S119's adversarial pass already found violated 33 times), retirement with tombstones, a
shard split, and raising the ceiling (**moves 0 B of content**, and the ceiling is the defect). A growth
policy is **viable but not now** — it answers the recurrence, not today.

Four parts, in order. **(1)–(3) need the operator's choice; (4) is a precondition.**

1. **Correct `.context-budget.json`'s 73,728 B to a satisfiable value, and prefer a token
   denomination.** `73,728 → 69,632` was tested on a scratch clone: **nothing breaks** — all three
   suites green, `check-learnings` exit 0 — and `73728` is pinned by **zero** tests or code. But a byte
   ceiling will rot again at the next compaction. **The only form that does not rot is
   `max_tokens: 25000`**, which the config has no field for and `context_budget.py:122` (a bare byte
   comparison) cannot evaluate. Its `_` note also carries **five now-false statements**, including the
   derivation *"the one-read cliff is 25,000 × 3.0300 = 75,751 B."*
2. **Stop publishing the detector floor as a budget.** `starter-kit/methodology_dashboard.py:3215` and
   `:3230` ship *"56,750 B one-read **budget**"* to every adopter; the trimmer's own wording is already
   right. Cost: fleet-visible, and **2 of 321** dashboard tests assert the current wording.
3. **Add a check that reads the live artifact, not one that compares constants.** A
   `max_bytes / bytes_per_token` assertion is documentation, not a limit (Learning #38). The measured
   form — concatenate the live file and assert `f(1) < 25,000` — is the only check that would have caught
   both the BL-45 drift and today's.
4. **Decide the port-branch question before unblocking Phase 3C.** Appending breaks the `b21854cc`
   byte-identity with the unpushed PR-ready branch. Three uncosted options: (i) append on both and keep
   them identical; (ii) hold Phase 3C until Phase 5 ships or is abandoned; (iii) accept divergence and
   re-run the port's end-to-end `bin/sync` check.

**This is an answer to two open operator decisions, not an agent's correction.**
`file-management-system-plan.md:287` registers **D5** (*"are ceilings denominated in the conservative
2.27 floor or each file's measured density?"*) and **D4** (*"is 'undeliverable in one Read' a fault or an
accepted operating state?"*), under a heading stating *"Phase 1 does not start until these are answered"*
and *"none is derivable from measurement."* §6 proposes answers to both; it does not settle them.

**Consequence for the queue: Phase 3 must not ship as specified.** It would hard-wire 56,750 B into a
gate. *(One correction to the steelman: §3.4 and §5's Phase 3 DONE criterion cover only the Phase 0
pair, not this file — the claim that Phase 3 would gate this specific append is **not supported by the
plan**.)*

---

## 7. The record to repair — and the boundary nobody has drawn

Repairing a defect falsifies every record that described it (**Learning #28**), and none of these goes
red on its own. **But ~29 of the ~45 sites are `CHANGELOG.md` / `HANDOFFS.md` / `docs/archive` entries,
which the repo's own doctrine makes append-only records of what a session *found*.** Applied literally,
#28 would rewrite the ledgers and destroy the evidence that the error happened. **The framework has no
rule for this boundary. Proposed test: does the sentence tell a future session what to DO (repair it),
or record what a past session FOUND (leave it; correct it with a new dated entry that cites it)?**

**Live instructions — repair:**

| site | what is wrong |
|---|---|
| `.context-budget.json` (this file's `_` note) | the ceiling itself, plus five falsified statements |
| `starter-kit/methodology_dashboard.py:3215,:3230` + twin | floor published as a "budget", **distributed** |
| `upstream-read-set-pr-plan.md:95` | **wrong in sign** — 73,483 B was ~96.5% of one read, never over-cap |
| `upstream-read-set-pr-plan.md:106` | the 55,930 B target; *"the only measured remedy"* — no remedy was required |
| `upstream-read-set-pr-plan.md:233` (§5) | Phase 2 is headed **SHIPPED** while its own DONE criterion (`≤ 55,930 B`) is unmet at 56,673 B; **its second criterion — "Test 32's four anchors updated in the same commit" — was never performed** (`364b410` touched only two files, neither `bin/tests.sh`; the anchors survived by luck of preservation) |
| `upstream-read-set-pr-plan.md:159` (§3.4c) | `total_bytes = 56,750` first ship must be re-derived |
| `bin/check-learnings:89` | the row budget's basis (b) — *"a quarter of the file's headroom against its ceiling"* — is partly derived from the number being corrected. Basis (a) is independent and survives |

**Frozen records — do not rewrite; cite:** `CHANGELOG.md:303/338/354/456`, `HANDOFFS.md` S118/S119/S120
receipts, and the archives.

**Where the correction must live so it actually fires.** Not a Learning row — **#46 has zero inbound
citations and fired on nobody**. Not a handoff gotcha — that channel expires in one session. Not only at
the constant's definition, which **already** warns *"a value that predicts `FRAMEWORK_LEARNINGS.md`
truncates when a probe shows it comes back whole"* and which S120 never opened. **The one channel with
measured reach is this file's own front matter** — distributed, and read on 243 of 244 reads.

---

## 8. Reproduction

```sh
# the meter — returns NO content, costs nothing
for n in 2 3 4; do : ; done   # cat the file n times, then Read with an explicit over-cap line range
# f(n) = 19,612n + 5  =>  f(1) = 19,617 tok = 78.5% of the 25,000-token cap

# the cliff, measured rather than multiplied
#   126 lines / 72,195 B -> delivered whole ; 127 lines / 73,646 B -> refused at 25,486 tok

# marginal row cost — the unit that governs an append
#   file + rows #39-#42 duplicated: x2 = 41,833 tok, x3 = 62,747 tok
#   => 4,163 B of rows = 1,302 tok = 3.1974 B/token, NOT the file's 2.8897

# what actually governs this file
python3 starter-kit/context_budget.py | grep FRAMEWORK_LEARNINGS   # 56,673 / 73,728 ok
python3 starter-kit/methodology_trim.py --file starter-kit/FRAMEWORK_LEARNINGS.md --check; echo $?  # [NO_CONFIG] 3
bin/check-learnings; echo $?                                        # 0 -- run bare, never through a pipe

# the port-branch identity S120 also cited
git rev-parse port/framework-learnings-extraction:starter-kit/FRAMEWORK_LEARNINGS.md \
               HEAD:starter-kit/FRAMEWORK_LEARNINGS.md              # same blob b21854cc
```
