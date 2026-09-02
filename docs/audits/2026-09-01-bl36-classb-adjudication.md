# BL-36 Class B — is `HANDOFFS-through-2026-08-25`'s L2 failure record loss?

**Session:** S134 · **Date:** 2026-09-01 · **Workstream:** `workstreams/AUDIT_WORKSTREAM.md`
**Item:** [`docs/planning/BACKLOG.md`](../planning/BACKLOG.md) BL-36 → [detail](../planning/BACKLOG-DETAIL.md#bl-36)
**Prior audit in this series:** [`2026-08-15-bl36-archive-losslessness.md`](2026-08-15-bl36-archive-losslessness.md) (S88)

---

## Audit Summary

- **Scope:** the one open question S133 left — `docs/archive/HANDOFFS-through-2026-08-25.md.verify.sh`,
  generator **v1.3.0**, failing **L2 only**, while five sibling v1.3.0 proofs pass. Context re-derived
  across all **19** shipped `docs/archive/*.verify.sh` proofs and all **11** `HANDOFFS.md` trims.
- **Criteria:** (D1) are the shard's records intact, measured independently of the failing proof?
  (D2) what exactly did L2 lose, and in which commit? (D3) is the proof correct to fail? (D4) does
  the cause recur, and what is the adopter blast radius?
- **Coverage:** 19 of 19 proofs run; 11 of 11 `HANDOFFS` trims cross-tabulated; 6 of 6 receipts at
  the trim re-derived by content identity. Nothing skipped.
- **Findings:** 0 critical · 3 moderate · 2 minor.

### The answer

**The archives are intact. This is not record loss.** Across the trim commit `9038e40`, six receipts
became four retained plus two archived, with **0 missing and 0 added**, measured by SHA-256 of each
receipt body keyed on `session:` — a different function from the one L1/L3 assert on, so it is not an
identity that cannot fail.

**But S133's stated cause is wrong, and the true cause is a trap that will recur.** The failure was
not caused by a later session's edit; it was caused **inside the trim commit itself**, by the repo's
own documented post-trim fold-in touching a front-matter count line that the ledger's spec does not
declare as regenerated. The proof is behaving correctly. Regenerating it does **not** fix it —
measured, not predicted.

---

## Method — and why it is not a re-run of the failing script

The failing script is the artifact under audit, so D1 is answered by a re-derivation that shares none
of its logic: receipts are split on **line-start** ```` ```handoff ```` fences (never `text.index`,
which stops at the code span this ledger quotes in its own prose), keyed by `session:`, and compared
as **content hashes** — a set difference over identities, not a positional concatenation. D2/D3 are
answered by reading the commit and the generator, not by inference from the failure text. D4 is
answered by executing the off-diagonal cell: the newest shipped generator's logic pointed at the old
trim. `docs/archive/` was not modified at any point (`git status --porcelain docs/archive/` empty
throughout); the substituted copy lives in the session scratchpad.

---

## Findings

### Finding #1 — No record loss at the 08-25 trim, and none at HEAD (criterion D1)

- **Severity:** — (this is the adjudication's answer, not a defect)
- **Evidence:** at `9038e40^` the live ledger held `[S110, S109, S108, S107, S106, S105]`; at
  `9038e40` it holds `[S110, S109, S108, S107]` and the shard holds `[S106, S105]`. Identity sets:
  6 before, 6 after (live + shard). **MISSING: none. ADDED: none.**
- **One anomaly, chased and explained.** A HEAD-reachability sweep across the live ledger plus all
  12 `docs/archive/HANDOFFS*.md` files finds 5 of the 6 pre-trim identities and reports **S110
  unreachable**. That is not loss: at `9038e40^` S110's receipt was its Phase 1B `status: pending`
  claim stub, and at HEAD (in `HANDOFFS-through-2026-08-29.md`) it is the finalized
  `status: complete` receipt — 3,858 B → 9,890 B, differing only in the fields close-out writes.
  S110's own `commit:` field names `9038e40 (the trim)`, so the trim was S110's own work. This is
  the crash-breadcrumb lifecycle working exactly as `SESSION_RUNNER.md` Phase 1B describes.
- **Impact:** BL-36's binding question — *are the archives genuinely intact?* — is answered **yes**
  for Class B, on evidence independent of the failing proof.

### Finding #2 — S133's stated cause is refuted by the script's own derivation (criterion D2)

- **Severity:** Moderate
- **Location:** `docs/archive/HANDOFFS-through-2026-08-25.md.verify.sh:163`
- **Description:** S133's handoff proposed that the L2 failure is *"most likely benign front-matter
  maintenance"* because *"S132 edited exactly that line in `ec87d08`"*, and flagged the hypothesis as
  unproven. It is **false**, and false by construction rather than by measurement:

  ```python
  before, after, shard = show(TRIM + "^", LIVE), show(TRIM, LIVE), show(TRIM, SHARD)
  ```

  When `TRIM_SHA` resolves, every operand is a `git show` at the trim commit or its parent. **The
  script never reads HEAD or the working tree.** Its own output says so on line 1:
  `source : the trim commit 9038e40`. No edit made after `9038e40` — S132's or anyone's — can reach
  this proof.
- **The actual cause, read from the commit:**

  ```
  -**Archived shards — 8 trims, 92 receipts.** Every shard is `docs/archive/HANDOFFS-through-<date>.md`
  +**Archived shards — 9 trims, 94 receipts.** Every shard is `docs/archive/HANDOFFS-through-<date>.md`
  ```

  That rewrite is *in* `9038e40`. It is the single lost line L2 reports.
- **Impact:** a successor acting on the handoff would have investigated HEAD-side edits and found
  nothing, because the evidence is one commit deep and three weeks earlier. S133 was right to label
  the hypothesis unproven and right to rank the item; the cause it named is the wrong one.

### Finding #3 — The proof is correct, and the repo's own instructions walk sessions into it (criterion D3/D4)

- **Severity:** Moderate — structural, and it recurs by design
- **Location:** `HANDOFFS.md:68-72` (the instruction) · `starter-kit/methodology_trim.py:336-339`
  (the declaration) · the proof's `REGEN_PATTERNS` at `:32` and its L2 clause at `:286-290`
- **Description:** L2's contract is that front matter *may gain* declared blocks but *may not lose or
  reword* anything, **unless** the change is confined to a **declared regenerated field**. The
  `HANDOFFS.md` `LedgerSpec` declares exactly one:

  ```python
  regenerated=(
      ("retained receipt count",
       re.compile(r"(This file currently holds \*\*)(\d+)(\*\*)"),
       lambda ctx: str(ctx["retained"])),
  ),
  ```

  This ledger's front matter carries **two** derived counts. `9038e40` changed both — `holds **5**`
  → `**4**` (declared, correctly excused by `field_reversible`) and `Archived shards — 8 trims, 92
  receipts` → `9 trims, 94 receipts` (**undeclared**, correctly reported as a lost line).
- **The trimmer did not write it; a session did, following this file's own instructions.**
  `apply_regenerated` (`:1117`) rewrites only declared fields and `insert_pointer` (`:1103`) appends
  a pointer block. `HANDOFFS.md:68-72` then tells the next trimming session to *"fold it into the
  table above as one row and delete the block."* Doing that fold-in — and updating the count it makes
  stale — **inside the trim commit** is what reddens the proof.
- **Precision worth keeping:** the added table row is a *gain* and is permitted; L2 reports exactly
  **one** lost line. The sole cause is the count-line **rewrite**, not the row.
- **Evidence — all 11 `HANDOFFS` trims, and the correlation is 1-to-1:**

| Shard | Trim | Proof | `holds **N**` (declared) | `Archived shards` (undeclared) | +table row |
|---|---|---|---|---|---|
| 08-02 | `c0e6944` | FAIL | 30 → 30 | line absent | 0 |
| 08-09 | `a46f2f9` | FAIL | 30 → 3 | line absent | 0 |
| 08-11 | `721853b` | OK | 28 → 4 | line absent | 0 |
| 08-15 | `17753d9` | OK | 9 → 3 | line absent | 0 |
| 08-17 | `7fee8bd` | OK | 4 → 3 | line absent | 0 |
| 08-18 | `5ec1bd2` | OK | 3 → 3 | unchanged | 0 |
| 08-23 | `470cfd4` | OK | 3 → 3 | unchanged | 0 |
| 08-24 | `9cf4ae0` | OK | 3 → 3 | unchanged | 0 |
| **08-25** | **`9038e40`** | **FAIL** | 5 → 4 | **8/92 → 9/94 CHANGED** | **1** |
| 08-29 | `59a7677` | OK | 4 → 4 | unchanged | 0 |
| 08-30 | `78a29f8` | OK | 4 → 4 | unchanged | 0 |

  (The two 08-02/08-09 failures are Class A — v1.1.1, L1/L3, already answered by S88.)

  **`9038e40` is the only trim of eleven that folded in-commit, and the only v1.3.0+ `HANDOFFS`
  proof that fails.** Every other trim left the count stale inside the trim commit and corrected it
  later, out of band — `273afff` is a recent example — and every one of those proofs is green.
- **Impact:** **the proof rewards deferring the documented fold-in and punishes doing it promptly,
  and nothing in the file says so.** A session that follows `HANDOFFS.md:68-72` conscientiously, in
  the commit where it is relevant, ships a red losslessness proof for an intact archive. That is the
  same failure mode BL-36 exists to prevent — a red proof indistinguishable, to a reader, from real
  loss.

### Finding #4 — Regenerating the proof does not fix Class B (criterion D4)

- **Severity:** Moderate — it invalidates the recommended disposition standing in BL-36
- **Description:** BL-36's open residual carries a recommended disposition: *"regenerate all four
  under v1.2.0."* Whatever its merits for Class A, **it does not apply to Class B.** Measured by
  running the newest shipped generator's logic (v1.5.0, copied from the 08-30 proof with only
  `SHARD` substituted) against the 08-25 trim:

  ```
  source : the trim commit 9038e40
  records: 6 before = 4 retained + 2 archived; added by the trim commit: 0
  checked: L1, L2/front-matter, L3
  FAIL: L2 FRONT MATTER lost 1 line(s), first: '**Archived shards — 8 trims, 92 receipts.** …'
  ```

  **exit=1**, read bare on the next line, never through a pipe. Control: the same v1.5.0 script on
  its own shard exits **0**.
- **Why:** the lost line is frozen in the commit. No generator that derives `before`/`after` from
  `show(TRIM^)`/`show(TRIM)` can un-see it, and every version since v1.1.1 does.
- **The only code fix that would work, tested rather than proposed:** declaring the line in
  `regenerated`. `field_reversible` compares the **residue** — the line minus the matched span —
  byte-for-byte, so a pattern must span **both** numbers at once. Measured against the real pair:

| Candidate `REGEN` pattern | Excuses the change? |
|---|---|
| `(Archived shards — )(\d+)( trims,)` | **False** — the other number sits in the residue |
| `(trims, )(\d+)( receipts)` | **False** — same reason |
| `(Archived shards — )(\d+ trims, \d+)( receipts)` | **True** |

  That is a change to a **distributed** file (`bin/_manifest.py:50`) and needs its own go-ahead; it
  is named here, not taken (FM #17).

### Finding #5 — S88's "Defect B is fixed" is too strong as stated (criterion D3)

- **Severity:** Minor — a record correction
- **Location:** [`2026-08-15-bl36-archive-losslessness.md`](2026-08-15-bl36-archive-losslessness.md)
  Finding #3
- **Description:** the prior audit concluded *"Defect B — the regenerated front-matter count line.
  Genuinely fixed between v1.1.1 and v1.1.3."* Class B is a **v1.3.0** proof failing with that exact
  shape. What v1.1.3 fixed is the handling of the **declared** count line; an **undeclared** derived
  line in the same front matter reproduces the failure in every version since. The claim was true of
  the population it enumerated — the six proofs then shipped, none of which had a second count line —
  and does not generalise to the population that now exists.
- **Impact:** minor on its own; it matters because it is the sentence that would have told S133 this
  class was closed.

### Finding #6 — The trim commit's own ledger entry misdescribes it (criterion D2)

- **Severity:** Minor
- **Description:** `9038e40`'s `CHANGELOG.md` entry says *"**Written by:** `methodology_trim.py`
  v1.3.0 — a tool action, not a session's judgment."* The commit also contains a session's hand-edit
  to the front matter — the fold-in, the new table row, and the count rewrite that is this whole
  finding. The entry is accurate about the archive move and silent about the rest.
- **Impact:** a reader reconstructing the failure from the ledger is told the commit is a pure tool
  action, which is exactly the assumption that makes the L2 failure look inexplicable.

---

## Items Audited

| Item | D1 records | D2 cause located | D3 proof correct | D4 recurrence | Overall |
|---|---|---|---|---|---|
| `HANDOFFS-through-2026-08-25.md` | **Pass** (6/6, 0 missing) | Pass (`9038e40`) | Pass (correct FAIL) | recurs (#3) | **Artifact intact; proof correctly red** |
| Other 10 `HANDOFFS` trims | not re-derived | n/a | 8 OK / 2 Class A | n/a | cross-tabulated only (#3) |
| 8 `CHANGELOG` proofs | not re-derived | n/a | 6 OK / 2 Class A | n/a | out of scope — Class A, answered by S88 |

**Explicit coverage limit:** this audit re-derived record identity for **one** trim — the one under
adjudication. The other ten `HANDOFFS` trims were cross-tabulated on commit shape and proof result
only. S88 covered the four Class A shards by identity; the six trims created after S88 have **never**
had an independent identity re-derivation. That is not a finding, it is a gap in coverage, and it is
stated so nobody reads this report as a whole-corpus clearance.

---

## Structural Observations

1. **A frozen proof is a claim about commit hygiene, not only about data.** S88 said this about
   bundled record additions; Class B is the same sentence one zone up. The archive is intact, the
   proof is correct, and the red is produced entirely by *what else rode in the commit*.
2. **A file's instructions and its verifier disagree, and only the verifier is mechanical.**
   `HANDOFFS.md:68-72` asks the next trimming session to fold in the pointer block. `L2` punishes
   doing so in the trim commit. Ten trims accidentally complied by being late; the one that was
   prompt is red.
3. **A carve-out list is a population, and populations drift.** `regenerated` names the derived
   front-matter fields as of the day it was written. Nothing detects a second derived line being
   added to a ledger's front matter later — which is how a fixed defect reappeared under a newer
   generator.
4. **Adopter blast radius is bounded today and not bounded structurally.** The distributed seed
   `starter-kit/HANDOFFS.md` carries **neither** count line, so no adopter inherits this trap now.
   The mechanism is generic: `methodology_trim.py` is distributed, and any adopter who keeps a
   derived line in a pinned front-matter zone and updates it in the trim commit gets the same red
   proof. `CHANGELOG.md`'s spec declares `regenerated=()` with the comment *"the live root ledger
   carries no count sentence today"* — verified still true (its front-matter zone, lines 1–208,
   contains no derived-count line), and it is a time-bound claim with no detector behind it.

---

## Comparison with Prior Audits

| Metric | S88 (2026-08-15) | S134 (2026-09-01) | Trend |
|---|---|---|---|
| Proofs in corpus | 6 | **19** | grew 3.2× |
| Failing | 4 | **5** | +1, and the new one is a new class |
| Failing classes | 1 (Defect A, bundling) | **2** (A + B, undeclared derived line) | — |
| Records re-derived by identity | 228 across 6 trims | 6 across 1 trim | narrower by design |
| Record loss found | 0 | **0** | stable |
| Prior conclusion revised | — | Finding #3's "Defect B fixed" | narrowed |

---

## Recommendations

1. **Do not regenerate the 08-25 proof.** Measured, not predicted: the newest generator fails it with
   identical text (Finding #4). Regeneration would spend the archive-freeze exception and change
   nothing. This also narrows BL-36's standing recommended disposition, which should be re-scoped to
   Class A only.
2. **Take audit rec 3 — a trim commit touches nothing but the trim.** It is the cheapest complete
   fix, it needs no code, and S88 already named it as the only thing that removes the Class A
   `HANDOFFS` residue. It removes Class B outright: ten of eleven trims already satisfy it by
   accident. Pair it with an edit to `HANDOFFS.md:68-72` saying the fold-in belongs in a **follow-up**
   commit and why — that comment is currently an instruction to break the proof.
3. **Or declare the second count line**, using the both-numbers pattern in Finding #4's table. This
   touches a distributed file and needs an operator go-ahead and an upstream route; it also requires
   the trimmer to compute the shard/receipt totals itself, which it does not today. Recommendation 2
   is strictly cheaper and I prefer it.
4. **Annotate, do not regenerate.** The 08-25 shard's front matter should say the proof is red for a
   located, non-loss reason, and point here. Same disposition as S88's rec for the Class A four, and
   the same reason: a red proof with no in-artifact explanation is indistinguishable from real loss.
5. **Correct the record in BL-36** — Class B is not a counter-example to the generator-version
   correlation, it is a second defect; and its cause is not S132's `ec87d08`.
6. **Close the coverage gap** named above: the six post-S88 trims have never had an identity
   re-derivation. One session, mechanical, no distributed file.

---

## Reproduction

```bash
# every shipped proof, as a reader would run them (5 of 19 FAIL)
for f in docs/archive/*.verify.sh; do bash "$f" >/dev/null 2>&1; echo "$? $f"; done

# the cause, one commit deep
T=9038e405921d9c6bf73300ae4fe4c00c772de1d3
git show "$T^:HANDOFFS.md" | grep 'Archived shards'
git show "$T:HANDOFFS.md"  | grep 'Archived shards'

# the off-diagonal cell: newest generator's logic, old trim (docs/archive/ untouched)
cp docs/archive/HANDOFFS-through-2026-08-30.md.verify.sh /tmp/v150.sh
sed -i '' 's|HANDOFFS-through-2026-08-30.md$|HANDOFFS-through-2026-08-25.md|' /tmp/v150.sh
bash /tmp/v150.sh; echo "exit=$?"     # 1 — read bare, not through a pipe
```
