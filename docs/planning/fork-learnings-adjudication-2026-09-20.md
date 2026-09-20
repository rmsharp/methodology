# BL-53 P3 — every row of `docs/FORK_LEARNINGS.md` adjudicated against the ratified criterion

**Session:** S200, 2026-09-20. **Phase:** P3 of
[`fork-learnings-retirement-rule-plan.md`](fork-learnings-retirement-rule-plan.md) §8.
**Rule in force:** D1–D4 as ratified by the operator at this session's Phase 0 picker — option **A + C's
D3 pairing** (plan §7). **Tree:** `9d30247`, file at **85,228 B, 69 rows, numbered 15–83.**

---

## 1. The result, first

**No row retires. 0 of 69.** The file stays at 85,228 B, **3,308 B above** its 81,920 B growth warning.

That is not a refusal to do the work and it is not a near miss. Every row was read in full and tested
against all three limbs of D1; the per-row verdicts are §5. **Six** rows are **partly** covered by a gate
or a test, and the plan's §5 sample had already flagged two of them (`#15`, `#19`) as the source of its
*"at most 2 … ~2,900 B"* estimate. **D1 as ratified says a row retires "when, and only when, one of
these holds."** A partly-held condition does not hold, and the ratified text leaves no room to read it
otherwise — so the honest yield is zero, and the estimate the operator chose A against was the
optimistic bound of a ten-row sample, not a measurement of the corpus.

**This corrects the plan's own central finding in the same direction it already pointed.** The plan
said a criterion-only rule under-yields at the current overage. It under-yields by more than it said.

---

## 2. Method

Each row was read in full (not its headline), then tested against D1's three limbs:

- **(a) Mechanized** — does a gate in `.quality-gates.json`, a test in `bin/tests.sh`, or a numbered
  failure mode in `SESSION_RUNNER.md` now enforce **the lesson**? The test applied is the row's own
  *When to Apply* column: would a session that never read the row still get the benefit? A mechanism
  that pins the row's **originating instance** while leaving its instruction to future work unenforced
  is recorded as **partly**, and partly is a retain.
- **(b) Superseded** — does a **later row** state the same lesson **at least as generally**?
- **(c) Spent** — does the artifact, tool, file or defect the row is about **no longer exist**?

Nothing was taken on the plan's word: the mechanism named in every *partly* verdict was grepped
(`TestThisRepoReadSetPartition`, Tests 32/34/38/39/41/42/43, `SEED_FORMAT_MARKERS`, `classify_empty`,
`RESERVED_RE`, `ROW_BUDGET_BYTES`, `RECORD_BUDGET_BYTES`), and every citation in §5 resolves.

---

## 3. Why (b) and (c) are unsatisfiable across this corpus — measured, not argued

### (b) The table differentiates; it does not restate

Resolving every intra-table reference to its referent gives **13 rows citing an earlier row**, across **6 distinct
targets** (`#16`×7, `#31`×2, `#28`, `#35`, `#43`, `#53`). Every one is a **differentiation** —
*"sibling of"*, *"distinct from"*, *"the converse of"*, *"one level up"* — each naming what the two rows
do **not** share. **Not one is a restatement.** Twenty-six of 69 rows (38%) position themselves against
an earlier row or use an explicit relation word.

That discipline is what makes (b) unsatisfiable here: a session whose lesson would have superseded an
earlier row wrote a narrower row that cites it instead. **A corpus curated this way cannot produce
supersession**, and the property that makes it readable is the same property that makes it
irreducible under (b).

It also **constrains** retirement in the opposite direction. **Eight** rows are cited **by another live
row or by live config**: `#16`, `#26`, `#28`, `#31`, `#34`, `#35`, `#43`, `#53`. Retiring any of them
strands an in-table reference — which is row `#22`'s own lesson (*a completed item's own text can be
load-bearing for a sibling's meaning*) applied to the file `#22` lives in.

**The instrument was audited before its number was published, and it failed the first time.** The naive
pattern (`Learning #N` / `#N`) returned hits in rows `#52`, `#53`, `#54`, `#68` and `#83` that are **not
citations of this table**: `#52`/`#53` say **FM #27** (a failure mode), `#54` quotes upstream's own
comment string *"learning #22 / #26a"*, and `#83` quotes rad-con's `#28/#29/#30/#34`. Six false hits in
four rows. A first pass also dropped bare `#28`-style references by collecting only two of three regex
groups, so it under-counted in the other direction at the same time. This is **fork Learning #83
reproduced by the document written to adjudicate it** — recorded here rather than quietly fixed,
because it is the third independent occurrence of that defect class in this file's own tooling.

### (c) Nothing this file is about has gone away

Across the 69 rows, **38 name at least one file path — 56 path mentions, and every one resolves to a
tracked file.** The only non-resolving strings are three bare `.verify.sh` suffixes, which are a generic
name for shards' proof scripts; two of those scripts were executed by this session. Six named constants
were checked individually and all exist: `SEED_FORMAT_MARKERS`, `MIN_BYTES_PER_TOKEN`, `classify_empty`,
`RESERVED_RE`, `ROW_BUDGET_BYTES`, `RECORD_BUDGET_BYTES`.

**This is what a fork that dogfoods its own framework looks like:** the tools these lessons were learned
on are the tools still in daily use, so *spent* has no population. Several rows are not merely live but
**were applied during this session** — `#39` (adjudicate a remedy before costing its depth: the trim),
`#58` (fold in its own commit), `#62` (diff a red checker's rows: how the SAFEGUARDS breach surfaced),
`#73` (`git status` before a read-only claim), `#83` (§3 above).

### (a) is partial by construction for a table of review practices

Every row here teaches a **practice a reader performs**, not a property a tool can check. A gate can pin
the instance a lesson was learned on — and seven do — but the row exists for the *next* instance, which
by definition has no gate yet. Row `#47` states the general case outright: a transform can pass every
mechanical gate and destroy the thing the artifact exists for. **For `#47`, limb (a) is unsatisfiable by
the row's own content.**

---

## 4. What this means for BL-53

**D1, as ratified, is inert against the existing overage.** It is not useless — as a *steady-state*
rule (D3) it is exactly right, and it costs nothing to keep. But it recovers nothing today, and fork
Learning `#49` already establishes why: **a steady-state obligation cannot retire an existing
overage**; the catch-up pass was supposed to be the paired remedy, and the criterion left it with
nothing to cut.

So the live options are unchanged from plan §7, minus A's catch-up half:

| option | status after this pass |
|---|---|
| **A (ratified)** | **D3 kept** — it stops future growth. Its catch-up half yields 0 B and is now complete. |
| **B — oldest-first to a stated depth** | The only option that recovers real bytes (14,502 B at ten rows). It retires **live advice**; §5 now says row by row exactly which advice, which is what B was missing when it was offered. |
| **C — demote the ceiling to a reported series** | Recovers 0 B, and after this pass it is the option that *matches the measurement*: the file's cost is per row (`#34`), every row is live, and no row is over the 1,500 B row budget. |
| **D — compaction** | `#47` and `#21` both govern it; §2's band table says the oldest rows are already at the cap. |

**Recommendation: C, with D3 retained from A.** After this pass the argument for C is no longer an
accommodation — it is what the corpus measures to. Every row is live, the per-row guard
(`ROW_BUDGET_BYTES` = 1,500) is green at 0 violations, and the whole-file number is guarding a read that
fork Learning `#34` measured as happening once in 80 transcripts. **B remains the operator's to take
if headroom is wanted anyway**, and it is now costed row by row rather than by age.

**This is a recommendation, not a decision.** Nothing in this document changes a ceiling, a gate or a
row.

---

## 5. The adjudication — all 69 rows

`partly` names the mechanism and the half it does not reach. `cited by` marks a row another live row or
live config depends on.

| row | verdict | basis |
|---|---|---|
| 15 | RETAIN — partly | (a) the trimmer's zone-pinned L1/L2/L3 and each shard's shipped `.verify.sh` enforce partition-scoped losslessness **for moves the trimmer makes**; the row governs any hand-run split — this session's own pointer-block fold was one. (b) none. (c) live |
| 16 | RETAIN — live, **cited by 7 rows** | (a) *mutate the producer, not only the checker* is a review practice; no gate. (b) `#17`, `#18`, `#24`, `#25`, `#30`, `#38`, `#43` all cite it as sibling or *one level up*, none restates it. (c) live |
| 17 | RETAIN — live | (a) no gate reads a spec for a tautology. (b) none. (c) the agreement test still exists |
| 18 | RETAIN — live | (a) no gate runs an artifact to check its prose. (c) `methodology_trim.py` live |
| 19 | RETAIN — partly | (a) `SEED_FORMAT_MARKERS` (`bin/_manifest.py`, `bin/status`) exists and is tested, so **this** marker is pinned; nothing asserts a **future** marker is absent from the versions it must detect. (c) live |
| 20 | RETAIN — live | (a) no gate reviews a synthesis. (c) live |
| 21 | RETAIN — live | (a) no gate counts the unit the consumer reads; it governs BL-53's own option D. (c) live |
| 22 | RETAIN — live | (a) no gate greps for orphaned sibling references — §3 applies this row by hand. (c) live |
| 23 | RETAIN — live | (a) no gate re-derives a backlog claim against current code. (c) live |
| 24 | RETAIN — partly | (a) *empty ≠ nothing to check* **is** mechanized — Test 34's six named SKIP rows and `methodology_trim.py`'s `classify_empty`; *enumerate the consumers and re-point each at the whole ledger* is practice. (c) live |
| 25 | RETAIN — live | (a) no gate builds the missing off-diagonal cell. (c) live |
| 26 | RETAIN — live, **cited by live config** | (a) no gate sums what may not be removed — §1 of this document did it by hand. (c) `starter-kit/methodology_dashboard.py`'s comment cites it (plan §3); retiring it strands that comment |
| 27 | RETAIN — live | (a) no gate reads a fit statistic before the number beside it. (c) live |
| 28 | RETAIN — live, **cited by `#54`** | (a) no gate greps a repaired defect's own identifiers at close-out. (c) live |
| 29 | RETAIN — live | (a) no gate counts inbound citations to a section. (c) §Vertical Slice Sessions live |
| 30 | RETAIN — live | (a) no gate classifies an exported check's operands as fact or inference. (c) the shipped proof scripts live |
| 31 | RETAIN — live, **cited by `#32`, `#33`** | (a) Test 34's ≥3 floor and stated skips pin **that** fixture; *grep the test tree before shrinking any artifact* is practice |
| 32 | RETAIN — live | (a) no gate simulates a cut against each reader's predicate. (c) live |
| 33 | RETAIN — live | (a) no gate diffs row **sets** across fixture sizes. (c) live |
| 34 | RETAIN — live, **cited by `.context-budget.json`** | (a) no gate derives a ceiling from measured read behaviour. (c) the config's own `_` note names it |
| 35 | RETAIN — live, **cited by `#36`** | (a) no gate multiplies two independently-set limits. (c) live |
| 36 | RETAIN — live | (a) no gate runs the remedy a refusal advises. (c) the write-once shard-name guard still refuses |
| 37 | RETAIN — live | (a) L3 asserts identity modulo the **declared** transform for the trimmer; *invert the transform with your own implementation* is practice |
| 38 | RETAIN — partly | (a) the 7,168 B header reserve is now a constant with an assertion (Test 39 A2, cited in `HANDOFFS.md`'s front matter); *a limit that lives only in a comment is not a limit* is general |
| 39 | RETAIN — live | (a) no gate adjudicates a remedy's value before its depth — **re-applied this session** on the owed trim. (c) live |
| 40 | RETAIN — live | (a) no gate asks whether a deleted state can still occur. (c) live |
| 41 | RETAIN — live | (a) no gate re-runs a suite after the close-out writes. (b) `#75` states the structural version but is **narrower** (close-out artifacts only), so it does not supersede |
| 42 | RETAIN — live | (a) no gate re-measures a ratio on each side of a split. (c) live |
| 43 | RETAIN — live, **cited by `#44`** | (a) no gate freezes an operand outside the module that derives it |
| 44 | RETAIN — live | (a) no gate asserts a remedy's **resting** value as well as its trigger. (c) live |
| 45 | RETAIN — partly | (a) *sum the set* **is** mechanized — the read-set class total and `tools/test_context_budget.py` `TestThisRepoReadSetPartition`; the **order** half (a truncated read returns a prefix, and an oldest-first artifact loses its newest) is not |
| 46 | RETAIN — live | (a) no gate meters tokens instead of converting bytes. At **229 B** it is the smallest row in the file — retiring it would recover less than the reserved-gap line costs |
| 47 | RETAIN — live | **(a) is unsatisfiable by the row's own content:** its claim is that a mechanical gate cannot see the loss it describes. Governs option D |
| 48 | RETAIN — live | (a) no gate makes a blocker name its consumer. (c) live |
| 49 | RETAIN — live, **cited by `HANDOFFS.md` and the plan's D4** | (a) `SRF_RED` still refuses every on-schedule trim by construction — **this session forced past it**, which is the row being applied, not retired |
| 50 | RETAIN — live | (a) no gate re-derives a relationship with the instrument that measures relationships. (c) live |
| 51 | RETAIN — live | (a) Phase 0's reconcile is **still** frontier-based; the row is the standing warning about a live mechanism, not a repaired defect |
| 52 | RETAIN — live | (a) no gate lists what actually fires on a target tree. (c) live |
| 53 | RETAIN — live, **cited by `#67`** | (a) `core.hooksPath` is still per-clone and opt-in — **BL-77 is this row's open half** |
| 54 | RETAIN — live | (a) no gate settles a residue call by provenance. (c) `starter-kit/context_budget.py` live |
| 55 | RETAIN — live | (a) no gate re-derives a plan's expected values against the pre-change tree. (c) live |
| 56 | RETAIN — live | (a) no gate reads the exception before enforcing the majority. (c) live |
| 57 | RETAIN — live | (a) no gate runs each option's payload before it is offered. (c) live |
| 58 | RETAIN — live, **cited by `docs/HANDOFFS_ARCHIVE_INDEX.md` and `HANDOFFS.md`** | both citations were read **and obeyed** this session — the fold went in its own commit |
| 59 | RETAIN — live | (a) no gate re-derives whether a documented decision is still open. (c) live |
| 60 | RETAIN — live | (a) no gate re-meters density after a content change. (c) `MIN_BYTES_PER_TOKEN` live |
| 61 | RETAIN — live | (a) no gate re-runs a PR body's self-referential numbers at publish time. (c) **PRs #84 and #85 are open right now** — the row's exact condition |
| 62 | RETAIN — live | (a) no gate diffs a red checker's rows — done by hand this session, and it is **how the SAFEGUARDS breach surfaced** |
| 63 | RETAIN — live | (a) no gate divides headroom by the size of the next write. (c) live |
| 64 | RETAIN — live | (a) no gate runs a route against copies of the population it will meet. (c) live |
| 65 | RETAIN — live | (a) no gate keeps procedure out of a seed-once file; **PR #84, its remaining half, is open** |
| 66 | RETAIN — live | (a) no gate tests whether a remedy fits one unambiguous sentence. (c) live |
| 67 | RETAIN — live | (a) no gate trial-merges a hook and runs the suite under the harness. (c) live |
| 68 | RETAIN — live | (a) `bin/check-learnings`'s sweep is **still** line-scoped; the plan §3 cites this row as the reason its own count is a floor |
| 69 | RETAIN — live | (a) no gate greps arriving tests for reads of a kept config. (c) `TestThisRepoReadSetPartition` live |
| 70 | RETAIN — live | (a) `tests-sh-passed` is measured at two receipts **by this practice**; no gate enforces the state it is measured at — **re-applied this session** |
| 71 | RETAIN — live | (a) no gate runs a phase's DONE criteria on each candidate route. (c) live |
| 72 | RETAIN — live | (a) Test 41 encodes **that** decision; no gate turns a future rejected option into a mutant |
| 73 | RETAIN — live | (a) no gate runs `git status` before a read-only claim — **re-applied this session**, and it named two instrument rows |
| 74 | RETAIN — live | (a) no gate re-checks another repository at the moment of writing. (c) live |
| 75 | RETAIN — live | (a) Test 38 pins the specific guard; **BL-64's residual is open**, which is this row's own subject |
| 76 | RETAIN — live | (a) Test 38 (8b)/(8d) pins that control; *ask a structural question structurally* is practice |
| 77 | RETAIN — live | (a) no gate asks the remote instead of a mirror ref. (c) live |
| 78 | RETAIN — live | (a) no gate reconciles a written instruction against a tool's printed advice. (c) `bin/status` live |
| 79 | RETAIN — live | (a) no gate follows a message's own pointer to the section it cites. (c) live |
| 80 | RETAIN — live | (a) no gate greps neighbours for *wins* / *no exceptions* — and its subject, `starter-kit/SAFEGUARDS.md`, is the file this session found **1,743 B over its declared no-growth pin** |
| 81 | RETAIN — live | (a) Test 42 ships **that** derivation; *ask what recomputes this population* is practice — this document is an instance of it |
| 82 | RETAIN — partly | (a) `pre-commit-selftest` and `commit-msg-selftest`, with Test 43's control, cover the **two hooks that exist**; whether a hook is **armed** is BL-77, open |
| 83 | RETAIN — live | (a) no gate resolves a pattern hit to its referent — **this document's own instrument reproduced the defect on its first run** (§3) |

---

## 6. What this document deliberately does not do

- **It retires nothing and changes no row.** The file is untouched by this pass.
- **It does not raise, lower or demote the 81,920 B ceiling.** D4 kept it as a growth warning; §4's
  recommendation is for the operator, and changing it would be P5, which D4 did not authorise.
- **It does not write D3 into the close-out path.** That is P4, a separate session.
- **It does not re-open D1.** The criterion was ratified and applied as written; that it yields zero is
  a finding about the corpus, not an argument to reword the rule mid-pass.
