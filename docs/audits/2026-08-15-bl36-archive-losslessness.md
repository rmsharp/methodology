# BL-36 audit — are the four failing archive proofs evidence of record loss?

**Date:** 2026-08-15 · **Session:** S88 · **Workstream:** `workstreams/AUDIT_WORKSTREAM.md`
**Status:** BL-36's question is **ANSWERED**. No repair is made here — the repair is a separate,
operator-gated decision on a distributed tool (see Recommendations).

---

## Audit Summary

- **Scope:** all 9 files in `docs/archive/`, the 6 shipped `.verify.sh` proofs, and the 6 trim
  commits that produced the shards. 100% coverage — nothing in scope was skipped.
- **Criteria:** D1 record preservation at each trim · D2 front-matter preservation · D3
  reachability at HEAD · D4 fault location (artifact vs. proof).
- **Finding count:** 1 critical-question **resolved negative** (no loss), 2 moderate, 4 minor.

### The answer

**The archives are intact. Nothing was lost.** Across all six trims, **0 records** present before a
trim are absent afterwards from `live ∪ shard`. At HEAD, **0 of 228** record identities that ever
existed in either ledger are unreachable. All six trimmer-declared archive counts (10, 70, 68, 16,
30, 25) reproduce exactly under an independent parser.

**The fault is entirely in the proofs**, and specifically in a design limitation that **no version
of the tool fixed** and that the current version documents as deliberate.

---

## Method — and why it is not a re-run of the failing scripts

BL-36 warned that regenerating a proof before answering the question would produce a passing proof
over possibly-lost content and destroy the evidence. Re-running the *same* proof has the mirror
problem: it re-executes the logic under suspicion and can only repeat its verdict.

So the check was rebuilt independently
(`scratchpad/rederive.py`, not committed — it is scaffolding, not a deliverable):

- Records are keyed by **identity** (`### ` heading for `CHANGELOG.md`; `session | date` for
  `HANDOFFS.md`), never by **position**. This is the decisive difference: the shipped proof compares
  record *lists* positionally, so one extra record at the top shifts every comparison.
- Link targets are normalised before hashing, because the trimmer rewrites relative link paths by
  design when a record moves into `docs/archive/`.
- The question asked is a set difference — *is this record's content still somewhere?* — not
  *does the file still concatenate to the same bytes?*

**The detector was proved able to fail before its "0 missing" result was believed** (Learning #16 —
an assertion that cannot fail is not an assertion). Against the real `CHANGELOG-through-2026-08-02`
inputs:

| Fixture | Mutation | `missing` | `changed` | Verdict |
|---|---|---|---|---|
| control | none (real artifact) | 0 | 0 | silent, as claimed |
| mutant A | one shard record **deleted** | **1** | 0 | fires |
| mutant B | one shard record **altered** | 0 | **1** | fires |
| mutant C | shard **truncated** by 5 records | **5** | 0 | fires |

Each mutant asserted that the mutation actually applied, so "did not apply" could not be mistaken
for "survived".

---

## Findings

### Finding #1 — No record loss, at any trim or at HEAD (criterion D1/D3)

- **Severity:** Critical question, **resolved negative**
- **Evidence:**

| Shard | Trim | before | after | shard | **missing** | changed | added |
|---|---|---:|---:|---:|---:|---:|---:|
| `CHANGELOG-through-2026-08-02` | `7d7c63e` | 72 | 64 | 10 | **0** | 0 | 2 |
| `CHANGELOG-through-2026-08-09` | `61b48a6` | 75 | 8 | 70 | **0** | 0 | 3 |
| `CHANGELOG-through-2026-08-11` | `3dfde94` | 73 | 6 | 68 | **0** | 0 | 1 |
| `HANDOFFS-through-2026-08-02` | `c0e6944` | 46 | 30 | 16 | **0** | 1 | 0 |
| `HANDOFFS-through-2026-08-09` | `a46f2f9` | 33 | 3 | 30 | **0** | 1 | 0 |
| `HANDOFFS-through-2026-08-11` | `721853b` | 29 | 4 | 25 | **0** | 0 | 0 |

- At HEAD, sweeping live + **all 9** archives: `CHANGELOG.md` 153 historical identities, 227
  reachable, **0 unreachable**; `HANDOFFS.md` 75 historical, 95 reachable, **0 unreachable**.
- The two `changed` records were adjudicated individually by diff, not counted and waved past. Both
  are the trimming session's **own** Phase 1B stub being completed in the same commit
  (`status: pending` → `complete`, `self_score: pending` → `7`/`8`, plus its self-assessment prose).
  The record **grew**; nothing was removed.
- The `added` records are likewise same-commit additions by the trimming session — its own ledger
  entries for the trim, a close-out entry, and at `61b48a6` a reconcile entry.

### Finding #2 — Root cause: `INJECTED` is a boolean, not a count (criterion D4)

- **Severity:** Moderate
- **Location:** `starter-kit/methodology_trim.py:1715` and `:1736` —
  `injected = 1 if trims_the_ledger else 0`
- **Description:** The generated proof asserts a **positional** identity:
  `live@T^.records == live@T.records[INJECTED:] + shard@T.records`. `INJECTED` is meant to skip the
  records the trim commit itself adds — but it is computed as a 0/1 flag meaning *"does this trim
  write its own entry into this ledger"*, never as a count of what the commit actually added. It is
  therefore structurally incapable of modelling a trim commit that lands **more than one** new
  record, or that **edits** an existing one.
- **Impact:** Every trim commit bundled with any other edit to the same ledger breaks the identity
  **by construction, with zero data loss**. That is exactly the shape of all four failures:

| Failing proof | What the commit also did | Resulting symptom |
|---|---|---|
| `CHANGELOG…08-02` | added 2 records, `INJECTED=1` | `L3 record count 73 != 72` (off by 1) |
| `CHANGELOG…08-09` | added 3 records, `INJECTED=1` | `L3 record count 77 != 75` (off by 2) |
| `HANDOFFS…08-02` | finalized its own receipt at position 0 | `L3 record [0] not byte-identical` |
| `HANDOFFS…08-09` | finalized receipt **+** front-matter count | `L3 record [0]` + `L2 lost 1 line` |

### Finding #3 — BL-36's version correlation is a confound; the 2×2 settles it

- **Severity:** Moderate (it would have misdirected the repair)
- **Description:** BL-36 records that "the generator version correlates perfectly (all four v1.1.1
  fail; both v1.1.3 pass)". That correlation is real and **not causal**. Every failing shard was
  produced by a **bundled** trim commit and every passing shard by a **standalone** one, so version
  and commit-shape are perfectly collinear across the six shipped artifacts. Running the other two
  cells of the 2×2 separates them:

| | **v1.1.1 logic** | **v1.1.3 logic** |
|---|---|---|
| **Bundled** trim (08-02, 08-09) | FAIL ×4 *(observed, shipped)* | **FAIL ×4 — identical text**, + explanatory `NOTE:` on the two `HANDOFFS` cases |
| **Standalone** trim (08-11) | `CHANGELOG` **OK**; `HANDOFFS` **FAIL** (`L2 … lost 1 line: 'This file currently holds **28**'`) | **OK ×2** *(observed, shipped)* |

  Both off-diagonal cells were executed, not reasoned about: the shipped v1.1.3 script was copied to
  the scratchpad with only its `SHARD`/`LIVE` path substituted, pointed at the older shards, and run
  — and vice versa. Nothing in `docs/archive/` was modified.
- **Conclusion:** there are **two independent defects**, which the single correlation had fused:
  - **Defect A — bundling.** Present in v1.1.1 *and* v1.1.3, causal for all four failures.
    `starter-kit/methodology_trim.py`'s generated template treats this as a **deliberate loud FAIL**:
    *"NOT an exemption — this stays a FAIL, loud, because a real loss can have this exact shape too."*
  - **Defect B — the regenerated front-matter count line.** Genuinely fixed between v1.1.1 and
    v1.1.3 (BL-27 fix 1 + BL-28). Proven by the v1.1.1-on-standalone-`HANDOFFS` cell, which fails on
    a clean trim that v1.1.3 passes.

### Finding #4 — The explanatory `NOTE` never fires for a bundled `CHANGELOG` trim

- **Severity:** Minor
- **Location:** `docs/archive/CHANGELOG-through-2026-08-11.md.verify.sh:251` — `if fails and bad == [0]`
- **Description:** BL-27's fix 2 prints a `NOTE:` naming the bundled-commit pattern, but it is gated
  on `bad == [0]` — the *record-altered* shape. A bundled `CHANGELOG` trim produces a **count
  mismatch**, so `bad` is `None` and the note is skipped. Confirmed in the experiment above: both
  v1.1.3-on-bundled-`CHANGELOG` runs failed with no `NOTE`.
- **Impact:** even under the current tool, the most likely bundling on the busier ledger fails with
  no explanation at all — which is the precise condition that produced BL-36.

### Finding #5 — The answer was already on record, twice, and was not found

- **Severity:** Minor (process), high explanatory value
- **Evidence:** **BL-27** (`docs/planning/BACKLOG.md:975`, raised S64, closed S65) documents both
  triggers exactly, states of this one *"This is not evidence of historical data loss — S61's actual
  archive move is intact"*, and **predicts this session**: *"a future re-run of that same frozen
  script, done for due diligence, will misread as a fresh finding of loss unless the reader already
  knows this pattern."* S64's own receipt (now in
  `docs/archive/HANDOFFS-through-2026-08-09.md`) records the same conclusion.
- **Why it was missed:** `docs/planning/BACKLOG.md` is **1,518 lines / 134,759 bytes** — 2.06× the
  65,536 B budget the two mandated-read ledgers are held to, and 76% of the 2,000-line agent `Read`
  cap. BL-27 sits at `:975`; BL-36 was appended to the same file at `:1446`. The backlog is not
  covered by `methodology_trim.py` (its `LEDGERS` table is `CHANGELOG.md`/`HANDOFFS.md` only — that
  is **BL-32**, still open), so no reduction step reaches it.

### Finding #6 — 3 of 9 archives ship no proof at all

- **Severity:** Minor
- **Evidence:** `CHANGELOG-through-2026-08-01.md`, `CHANGELOG-through-v3.6.md`,
  `HANDOFFS-archive.md` predate the trimmer and have no `.verify.sh`. Their contents were covered by
  this audit's HEAD reachability sweep (0 unreachable) but by **identity only**, not by a
  re-derivation from a trim commit — there is no trim commit to re-derive from.

### Finding #7 — "Frozen" means records frozen, not file frozen

- **Severity:** Minor (documentation precision)
- **Evidence:** 7 of 8 `*-through-*` shards are byte-identical to their creating commit.
  `CHANGELOG-through-v3.6.md` is not: `020ba3f` (S31) rewrote its front matter. Re-derived — all
  **50 dated records are byte-identical**; only front matter changed, and the change is a
  self-documenting correction that says so. Benign, but a reader running `git diff` against the
  add-commit sees a modified "frozen" file.

---

## Items Audited

| Item | D1 records | D2 front matter | D3 reachable @HEAD | D4 fault located | Overall |
|---|---|---|---|---|---|
| `CHANGELOG-through-2026-08-01.md` | n/a (no trim proof) | n/a | Pass | n/a | Pass (#6) |
| `CHANGELOG-through-2026-08-02.md` | **Pass** | Pass | Pass | proof (Defect A) | Artifact OK |
| `CHANGELOG-through-2026-08-09.md` | **Pass** | Pass | Pass | proof (Defect A) | Artifact OK |
| `CHANGELOG-through-2026-08-11.md` | **Pass** | Pass | Pass | — | Pass |
| `CHANGELOG-through-v3.6.md` | **Pass** (50/50) | changed, benign | Pass | n/a | Pass (#7) |
| `HANDOFFS-archive.md` | n/a (no trim proof) | n/a | Pass | n/a | Pass (#6) |
| `HANDOFFS-through-2026-08-02.md` | **Pass** | Pass | Pass | proof (Defect A) | Artifact OK |
| `HANDOFFS-through-2026-08-09.md` | **Pass** | Pass | Pass | proof (A + B) | Artifact OK |
| `HANDOFFS-through-2026-08-11.md` | **Pass** | Pass | Pass | — | Pass |

---

## Structural Observations

1. **A positional proof is a claim about the commit that produced the artifact, not only about the
   artifact.** The trimmer's own losslessness logic is content-based and correct; the *exported*
   proof re-expresses it positionally, and that re-expression silently imports a dependency on
   commit hygiene. The data never moved — the frame of reference did.
2. **A deliberately-loud FAIL with no in-artifact explanation is indistinguishable from a real
   failure.** BL-27 chose "stay red, add a NOTE" over an exemption — defensible, since a real loss
   can share the shape. But the NOTE was added to the *generator*, and the four affected proofs are
   **frozen artifacts generated before it existed**. A fix that only reaches future artifacts leaves
   the existing ones saying `FAIL` forever, to every future reader.
3. **The reduction discipline moved the answer out of the read window.** FM #28 predicts precisely
   this: what size hides is not the false claim but *the evidence that would refute it*. Here the
   refuting evidence was BL-27, alive and correct in a 134 KB file nobody reads in full, while the
   contradicting claim was appended 471 lines below it.

---

## Recommendations

1. **Do not regenerate the four proofs as the repair — it would not work.** This is measured, not
   predicted: v1.1.3 logic run against all four bundled trims **still fails**, with identical text.
   Regeneration alone changes nothing except the version stamp.
2. **The real repair is Defect A: make `injected` a measured count** of the records the trim commit
   adds (and account for an edited frontier record), rather than a 0/1 flag. That is a change to
   `starter-kit/methodology_trim.py`, an adopter-distributed tool, and needs its own RED-first
   session against `tools/test_methodology_trim.py` — **not** folded into this audit (FM #17).
3. **Cheaper alternative worth costing first:** make the bundling *impossible* rather than
   modelled — require a trim commit to touch nothing but the trim, which is what S87 did and why its
   two proofs pass. This is a protocol rule, not a code change, and it fixes the cause rather than
   teaching the proof to tolerate it.
4. **Either way, the four frozen proofs need a disposition** — they cannot be made to pass by any
   change to the generator, because they are frozen. Options: annotate the shards' front matter with
   a pointer to this audit; or regenerate them under a fixed tool and accept that the new proof is
   no longer the artifact that was shipped. This is an operator decision.
5. **Extend Finding #4's note to the count-mismatch shape**, so a bundled `CHANGELOG` trim explains
   itself the way a bundled `HANDOFFS` trim now does.
6. **BL-32 is now load-bearing.** `docs/planning/BACKLOG.md` at 134,759 B is the artifact that hid
   BL-27. Bringing it under the trimmer, or under a declared ceiling, is what prevents the next
   re-raise of an already-answered question.

---

## Reproduction

```sh
# the six shipped proofs, as a reader would run them (4 FAIL, 2 OK)
for f in docs/archive/*.verify.sh; do echo "== $f"; bash "$f"; done

# the counterfactual that separates version from commit-shape: v1.1.3 logic, older shard
sed 's|CHANGELOG-through-2026-08-11.md|CHANGELOG-through-2026-08-02.md|g' \
    docs/archive/CHANGELOG-through-2026-08-11.md.verify.sh > /tmp/x.sh && bash /tmp/x.sh   # still FAILs

# every shard's freeze status since its own creating commit
for s in docs/archive/*-through-*.md; do t=$(git log --diff-filter=A -1 --format=%H -- "$s"); \
  git diff --quiet "$t" HEAD -- "$s" && echo "FROZEN $s" || echo "MODIFIED $s"; done
```
