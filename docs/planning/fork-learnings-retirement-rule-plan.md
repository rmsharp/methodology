# A retirement rule for `docs/FORK_LEARNINGS.md` — BL-53, costed against the file it now governs

**Status: DRAFT — decisions D1–D4 are open and belong to the operator.** Written at S199
(2026-09-20) as that session's single deliverable. **The plan is the deliverable; nothing here is
applied** (`starter-kit/SESSION_RUNNER.md` §Planning Sessions, failure mode #18). Every number below
was produced by running a command in a `--no-local` clone at `6a475b6`, not by reasoning about what
the tools would do; the commands are printed beside their results so a successor re-derives rather
than trusts.

**The question BL-53 asks, unchanged since S159:** how many learnings should the fork carry before
old ones retire? Two ceiling raises in 15 days answered *"more than we have"* twice and neither
answered the question.

---

## 1. Why this is being re-costed rather than read off BL-53

BL-53's option table was measured at S159 against `starter-kit/FRAMEWORK_LEARNINGS.md` — the
**distributed** file. Resync decision **D1** (S176, `docs/planning/upstream-resync-2026-09-plan.md`
§3) moved the fork's rows #15 onward to `docs/FORK_LEARNINGS.md`, which is fork-only: not in
`bin/_manifest.py`, not in any upstream PR. Three things changed with it, and each one moves a cost
in that table:

| | S159 (distributed file) | today (fork file) |
|---|---|---|
| Blast radius of retiring a row | every adopter's synced copy | this repository only |
| Route | an upstream change, its own go-ahead | fork-side, no go-ahead needed |
| Citations that must keep resolving | 4 distributed files | measured in §3 — **1** distributed file, and not by the mechanism anyone assumed |
| "a checker change for the numbering gap" | costed as required | **false today** — measured in §4, E2 |

So the S159 table is history, correct when written. It is not carried forward.

---

## 2. The measurement

Commands, run at `6a475b6`:

```
wc -c docs/FORK_LEARNINGS.md
grep -cE '^\| [0-9]+ \|' docs/FORK_LEARNINGS.md
bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations
```

- **83,768 B**, **68 rows**, numbered **15–82**, contiguous, checker green.
- Rows are **82,002 B** of that (97.9%); header and table frame are **1,766 B**.
- Row bytes: min 229, **median 1,233**, mean 1,205, max 1,499, against `bin/check-learnings`'s
  `ROW_BUDGET_BYTES = 1,500` — **0 rows over**.
- The warning is **81,920 B** (`.context-budget.json`, the file's entry), so the file is
  **1,848 B over**.

**The overage is widening, and its history is the argument for a rule rather than another raise:**

| receipt | file | over by |
|---|--:|--:|
| S197 close-out (as written) | 82,626 B | 706 B |
| S197 close-out (re-measured at HEAD by S198) | 82,652 B | 732 B |
| S198 close-out | 83,768 B | **1,848 B** |

Two consecutive sessions appended a row and removed none. That is the decay-term gap the runner's
own Degradation Detection table names — *"a close-out appends to a mandated-read file, and no
close-out has ever removed anything from one"* — and the second half of failure mode #28.

**Growth rate, measured from the file's own history** (`git log --follow`, byte size and row count
at each commit): 52 rows / 67,177 B at `8cfaf0d` (2026-09-16) to 68 rows / 83,768 B at `5015eb0`
(2026-09-20) — **16 rows, 16,591 B, 1,037 B per row.** At roughly one row per session that is
**~1,037 B per session**, and the median row (1,233 B) is the better figure for a *single* future row.

**Row size by age band** — this decides how much compaction can ever be worth:

| band | rows | median | sum | rows ≥ 1,400 B |
|---|--:|--:|--:|--:|
| #15–#33 | 19 | 1,450 B | 27,579 B | **19 of 19** |
| #34–#49 | 16 | 1,162 B | 17,684 B | 5 |
| #50–#66 | 17 | 1,153 B | 20,148 B | 1 |
| #67–#82 | 16 | 1,035 B | 16,591 B | 0 |

The oldest band is written **to the cap**, not padded — it is the S119 compaction band, and it is
the *densest* third of the file. Any plan that expects to recover bytes by compacting old rows is
planning against that table.

---

## 3. The inventory (mandatory — this plan removes rows)

`SESSION_RUNNER.md` §Evidence-Based Inventory requires the grep, not the architectural guess. Terms
swept: `Learning #N`, `Learnings #N`, `fork Learning #N`, the plural and slash forms
(`#N, #N`, `#N and #N`, `#N/#N`), and the file name `FORK_LEARNINGS`.

```
git grep -ohE '(fork )?[Ll]earnings? #[0-9]+(([ ,]| and )+#[0-9]+)*' -- .
git grep -cE '(fork )?[Ll]earnings? #[0-9]+' -- .
git grep -n 'FORK_LEARNINGS' -- .
```

**837 citations across 94 tracked files.** Rows #1–#16 are ambiguous (the distributed table holds
1–13, 15, 16 — `#14` is reserved), so the population that a fork retirement can strand is
**citations of #17 and above**:

| class | all | #17+ | what it means for a retirement rule |
|---|--:|--:|---|
| frozen archive (`docs/archive/`) | 586 | 371 | history, never rewritten (the file's own header says so) |
| plans / audits (`docs/planning/`, `docs/audits/`) | 158 | 74 | dated records; the checker deliberately does not sweep them |
| live ledgers (`CHANGELOG.md`, `HANDOFFS.md`) | 13 | 12 | append-only history; same treatment |
| **executables** (`bin/`, `tools/`) | 44 | **8** | see below — all prose, none load-bearing |
| **config** (`.context-budget.json`) | 5 | 4 | one `_` note naming #26, #34, #62, #63 |
| **the table itself** | 11 | 3 | rows cite rows: #43, #22, #53 |
| **distributed docs** | 27 | **0** | see below — the one apparent hit is another project's numbering |
| other live docs | 18 | 1 | `docs/HANDOFFS_ARCHIVE_INDEX.md:72` cites fork Learning #58 |

**The instrument was audited before its number was published.** Three corrections, all found by
reading the raw matches rather than the count:

- `bin/tests.sh:1714` matches `Learning #4242` — a **synthetic fixture string** planted by Test 33's
  mutation, not a citation. The executable count is **8, not 9**.
- `bin/check-learnings:36` writes `Learning #28/#30/#34`; the sweep regex used here counts the first
  number only, so slash-joined citations are **under-counted**.
- **`README.md:467` and `docs/RELEASE_HISTORY.md:53` are not citations of this table at all.** Read
  in full they say `Learnings #28/#29/#30/#34` — **rad-con's** project numbering, narrated as the
  historical defect S8 fixed by hand (`bin/check-learnings:36`–`:38` says so, and is why the sweep
  excludes `README.md`). Counting them as references to fork rows #28–#34 would have manufactured a
  constraint on two rows that nothing actually cites. **Corrected: no distributed markdown file
  cites a fork row at all** — the distributed-corpus exposure of a fork retirement is zero.

The sweep pattern is one phrasing among several, and `git grep` is line-scoped besides (fork
Learning #68: a reference wrapped across two lines is invisible to it, and comments wrap). **The
table above is a floor, not a census** — which matters in one direction only: an undercount can hide
a citation that a retirement would strand, so P3 re-runs the sweep against the rows it actually
retires rather than relying on this table.

**The 8 executable citations, read individually** (`bin/tests.sh:2780,2866`; `bin/check-learnings:36`;
`tools/methodology_dashboard.py:411`; `starter-kit/methodology_dashboard.py:411`;
`tools/test_methodology_dashboard.py:5607,5647,5693`): **every one is a comment or an assertion
*message*. No assertion's outcome depends on a row existing.** Retiring a row cannot turn a test red;
it can only orphan an explanation. That is the opposite of what a "distributed corpus" count
suggests, and it is why the inventory was run.

**Two couplings that are load-bearing**, both to the file rather than to a row:

1. `bin/tests.sh:1690`–`:1700` (Test 32) runs the checker at `--first 15`, asserts the literal string
   `contiguous 15..`, and **mutates row `#40` by number** to prove the gap check reaches this file.
   A retirement that removes `#40` makes that mutation vacuous — the test fails loudly rather than
   silently, but it fails. (*A file you shrink may be someone's fixture.*)
2. `.context-budget.json` watches the path and holds the 81,920 B warning.

**One finding, recorded not fixed.** `bin/check-learnings`'s citation sweep reads
`distributed_md_files()` — **`.md` files in `bin/_manifest.py` only**. `starter-kit/methodology_dashboard.py`
is distributed *and* cites `fork Learning #26`, a row no adopter can resolve, and the sweep cannot
see it because it is `.py`. That is a real gap adjacent to BL-11; it is **not** this plan's to fix.

---

## 4. The mechanisms, each run rather than reasoned about

All four were executed in a `--no-local` clone at `6a475b6` (`git rev-parse --short HEAD` asserted
before each), the file restored with `git checkout --` between them.

### E1 — oldest-first removal, `--first` advanced

Removed rows #15–#24 and re-ran the checker both ways.

```
bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations   # FAIL, exit 1
  error: Learning numbers are not contiguous from 15 — missing #15 … #24
bin/check-learnings --file docs/FORK_LEARNINGS.md --first 25 --no-citations   # OK, exit 0
  68 → 58 rows, contiguous 25..82
```

**14,502 B recovered; file 83,768 → 69,266 B.** Cost: `--first` must advance in **4 files, 10 sites**
— `bin/tests.sh:1686,1691,1692,1693,1700`, `bin/check-learnings:49,50,180`,
`docs/FORK_LEARNINGS.md:6,22`, `CLAUDE.md:35` — including the literal assertion string
`contiguous 15\.\.`.

### E2 — reserved-gap retirement (any row, any age) — **the finding that changes the options**

Removed row #30 (1,497 B) from the middle of the table and declared the gap in the file's own prose,
mirroring the distributed file's phrasing (``> **`#14` is reserved …**``):

```
> **`#30` is reserved — retired 2026-09-20 to the archive; never fill the gap.**

bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations   # OK, exit 0
  67 Learning row(s), contiguous 15..82
```

**The checker already tolerates a declared gap** — `RESERVED_RE = r"`#(\d+)`\s+is reserved"`,
`bin/check-learnings:76` — so **no checker change is needed, and retirement is not forced to start
at the oldest row.** Net recovery is the row minus its ~84 B declaration: **1,413 B for #30.**
S159's costing assumed this cost existed; it does not.

*Caveat measured, not assumed:* `RESERVED_RE` matches one number per occurrence, so N retired
numbers need N `` `#N` is reserved `` phrases (they may share a line or sit in a list; ~60–84 B each).

### E3 — tombstone in place

Replaced rows #15–#24 with 4-column stubs pointing at an archive (135 B each):

```
| 15 | **Retired 2026-09-20 — text in `docs/archive/FORK_LEARNINGS-retired.md`.** | — | — |
bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations   # OK, exit 0
  68 Learning row(s), contiguous 15..82
```

**13,152 B recovered; file → 70,616 B.** No checker change, no suite change, numbers stay present.
It costs 135 B per retired row against E2's ~84 B and keeps a dead row in the table's reading order.

### E4 — could `methodology_trim.py` do this?

```
python3 starter-kit/methodology_trim.py --file docs/FORK_LEARNINGS.md --check
  [NO_CONFIG] FORK_LEARNINGS.md has no entry in the config table. There is deliberately
  no generic fallback: a generic rule is what would mis-zone a differently-shaped ledger.
```

**It refuses, correctly.** The trimmer cuts newest-on-top ledgers by position; this table is
oldest-first and append-at-bottom. Teaching it this file is a change to a **distributed** tool —
its own go-ahead, and out of scope here.

### Summary

| mechanism | recovered (10 rows) | file after | checker | coupled edits |
|---|--:|--:|---|---|
| E1 oldest-first + `--first` | 14,502 B | 69,266 B | OK at `--first 25` | 4 files, 10 sites |
| E2 reserved gap, any row | ~1,413 B **per row** | — | OK, unchanged | none; one declaration line per number |
| E3 tombstone in place | 13,152 B | 70,616 B | OK, unchanged | none |
| E4 trimmer | — | — | refuses | distributed change |
| compaction | see §2 band table | — | OK | none; oldest band already at the cap |

---

## 5. Learning #26 applied to this file — sum what may NOT be removed, first

Fork Learning #26 says: before agreeing a size target is reachable, sum the part you may not remove
and compare **that** to the ceiling. Applied here, with the criterion this plan proposes
(§6, "mechanized / superseded / spent"), adjudicated **by reading the ten oldest rows**, #15–#24:

| row | lesson | mechanized, superseded or spent? |
|---|---|---|
| #15 | prove losslessness over the **partition**, not the total | **partly** — the trimmer's zone-pinned L1/L2/L3 and every shipped `.verify.sh` enforce it *for the trimmer*; the lesson is broader |
| #16 | wire the assertion to the artifact; mutate the producer | no — a review practice, still applied by name |
| #17 | a read-and-assert-equal spec is a contradiction | no |
| #18 | RUN the artifact before shipping behavioural prose | no |
| #19 | a tripwire keyed to an invariant marker cannot fire | **partly** — `SEED_FORMAT_MARKERS` now has tests |
| #20 | review the synthesis, not the candidates | no |
| #21 | "make it shorter" moves a size-correlated proxy | no — and it governs this very plan |
| #22 | deleting a completed item orphans a sibling reference | no |
| #23 | a backlog item is a claim frozen at filing time | no |
| #24 | a check keyed to the live file loses its population to archiving | no |

**Yield: at most 2 of the 10 oldest rows, ~2,900 B.** That clears today's 1,848 B overage and buys
**about one session** of headroom. It is the honest number, and it is the plan's central finding:

> **A criterion-only rule under-yields at the current overage.** Age is not a proxy for spentness —
> the oldest rows here are the densest and, by the table above, mostly still live advice. Any rule
> that promises the ceiling *and* keeps only spent rows is promising something this corpus cannot
> currently deliver, which is exactly the shape fork Learning #26 warns about: ship the reduction
> **plus the finding**, not the ceiling.

---

## 6. The proposed rule

**D1 — the criterion.** A row may retire when, and only when, one of these holds, cited in the
retiring commit:

- **(a) Mechanized** — a gate in `.quality-gates.json`, a test in `bin/tests.sh`, or a numbered
  failure mode in `SESSION_RUNNER.md` now enforces the lesson. *Cite the gate, test number or FM.*
- **(b) Superseded** — a later row states the same lesson at least as generally. *Cite the row.*
- **(c) Spent** — the artifact, tool, file or defect the row is about no longer exists. *Cite the
  commit that removed it.*

A row matching none of these does not retire, whatever its age or the file's size.

**D2 — the mechanism: reserved-gap retirement (E2).** The row's text moves **verbatim** to
`docs/archive/FORK_LEARNINGS-retired.md`; the live file gains one
`` > **`#N` is reserved — retired YYYY-MM-DD; never fill the gap.** `` line; numbers never change.
Chosen over E3 (tombstones cost 135 B and keep a dead row in reading order) and over E1 (age-based,
and it moves `--first` across four files). Measured: no checker change, ~1,413 B net per row.

**D3 — the trigger: close-out, not a byte negotiation.** A session that appends a row **either**
retires one under D1 **or states in its handoff that no row qualifies**, naming the rows it
considered. This is the decay term the runner's Degradation Detection table asks for, in the one
place that already runs every session. It is deliberately *not* keyed to the ceiling: a rule that
fires only at a threshold produces the five-week scramble this plan was written during.

**D4 — the ceiling's meaning after the rule exists.** Three sub-options; §7 costs them. The
recommendation is **(i)**: the 81,920 B warning stays exactly as it is — a *growth warning*, already
labelled one by the operator at S159 — and the rule above, not the number, is what answers BL-53.
A steady-state obligation cannot retire an existing overage (fork Learning #49: a guard refusing when regrowth ≥ relief is unsatisfiable by any steady-state policy), so it is
paired with **one catch-up pass** (§8, P3) sized to buy a stated number of sessions.

---

## 7. What the operator is choosing between

| option | recovers | keeps every live lesson | route | notes |
|---|--:|---|---|---|
| **A — D1+D2+D3 with a catch-up pass** ✅ | ~2,900 B now (2 rows), then flat | yes | fork-side | clears the overage by ~1,000 B; buys ~1 session. Honest, and small. |
| **B — A, plus oldest-first to a stated depth** | 14,502 B at 10 rows | **no** — retires live advice | fork-side | buys ~12 sessions; costs `--first` in 4 files; the depth is the operator's number, not a session's |
| **C — keep the per-row budget, demote the file ceiling to a reported series** | 0 B | yes | fork-side | defensible: this file is **read on demand**, so FM #28's *mandatory*-read failure does not strictly apply, and the cost sessions pay is per row (fork Learning #34: whole-read once, partial 243 times over 80 transcripts). But it is the third accommodation in five weeks and pays no decay term unless D3 rides with it. |
| **D — compaction pass** | low | yes | fork-side | §2's band table: #15–#33 are all ≥1,400 B, already compacted at S119. Also the one option a mechanical gate cannot verify — a compacted row can pass every check and have lost the nuance that made it worth keeping. |

**Recommended: A + C's D3 pairing, with B's depth left to the operator if ~1 session of headroom is
too thin.** A alone is honest but barely moves the number; B is the only option that buys real
headroom and it does so by retiring advice that is still live — that trade is the operator's to make,
not a session's, which is why this plan does not make it.

---

## 8. Phases

Each phase is one session and closes out (`SESSION_RUNNER.md` §Planning Sessions).

### P1 — this plan *(done at S199)*
**DONE:** this document committed.
**Verify:** `git log --oneline -1 -- docs/planning/fork-learnings-retirement-rule-plan.md`.
**Surface:** this repository. **It cannot enforce anything** — a plan's correctness is not
mechanically checkable, which is what P2 is for.

### P2 — operator ratification of D1–D4
**DONE:** the answers recorded in `CHANGELOG.md` and in BL-53's backlog row.
**Verify:** `grep -n 'D1' docs/planning/fork-learnings-retirement-rule-plan.md` resolves to a
recorded decision. **Not a session** — a picker at the head of P3's session.
**Surface:** none. **A decision has no test**; this is the gate P1 cannot substitute for.

### P3 — the catch-up pass
**DONE:** every row adjudicated against the ratified criterion (all 68, recorded — not only the ten
sampled here); the qualifying rows moved verbatim to `docs/archive/FORK_LEARNINGS-retired.md`; one
reserved-gap line per retired number; the file under 81,920 B with the headroom D4 states.
**Verify, in this order:**
```
bin/check-learnings --file docs/FORK_LEARNINGS.md --first 15 --no-citations   # OK, contiguous 15..82
git show <pre-retirement sha>:docs/FORK_LEARNINGS.md | grep -E '^\| (N|N|…) \|' \
  | diff - <(grep -E '^\| [0-9]+ \|' docs/archive/FORK_LEARNINGS-retired.md)   # byte-identical, empty diff
bash bin/tests.sh                                   # at or above the tests-sh-passed floor
python3 starter-kit/quality_ratchet.py --run        # 11/11, cite the summary line
wc -c docs/FORK_LEARNINGS.md                        # under 81,920 B
```
**Surface:** a `--no-local` clone with HEAD asserted by sha — this repo's documented
build-equivalent. **What it cannot enforce:** that a retired row's lesson is genuinely spent. No gate
sees a semantic loss; that is why D1 requires a *citation* per retirement and why P2 precedes P3.

### P4 — the steady-state obligation
**DONE:** D3 written into the fork's close-out path — `CLAUDE.md`, not the distributed
`SESSION_RUNNER.md`, since the rule is fork-only — and, if D4 chose a mechanical form, a gate that
refuses a close-out appending a row without the retire-or-state line.
**Verify:** the gate run red-first against a synthetic close-out that appends and says nothing.
**Surface:** the suite, plus one real close-out. **It cannot enforce** the quality of the "no row
qualifies" statement, only its presence.

### P5 — *(only if D4 chose a change)* the ceiling's new meaning
**DONE:** `.context-budget.json`'s entry rewritten to say what the number now means.
**Verify:** `python3 starter-kit/context_budget.py` (**not** `--status` — BL-75: the flag does not
exist, is silently ignored, and the default run appends a tracked history row).
**Surface:** this repo. Canonical-only; adopters have no budget for this file in any unit.

---

## 9. What this plan deliberately does not do

- **It does not touch `starter-kit/FRAMEWORK_LEARNINGS.md`.** That file is upstream's since D1:
  15 rows, 16,560 B, nowhere near any ceiling. BL-53's fork half is **entirely fork-side** — the
  first time that has been true.
- **It does not fix the `.py` citation-sweep gap** found in §3 (a distributed file citing a
  fork-only row, invisible to `check-learnings`). Recorded for the backlog; adjacent to BL-11.
- **It does not teach `methodology_trim.py` this file** (E4) — a distributed tool, its own go-ahead.
- **It does not retire a single row.** P3 does, after P2.
