# BL-36 Class B — is `HANDOFFS-through-2026-08-25`'s L2 failure record loss?

**Session:** S134 · **Date:** 2026-09-01 · **Workstream:** `workstreams/AUDIT_WORKSTREAM.md`
**Item:** [`docs/planning/BACKLOG.md`](../planning/BACKLOG.md) BL-36 → [detail](../planning/BACKLOG-DETAIL.md#bl-36)
**Prior audit in this series:** [`2026-08-15-bl36-archive-losslessness.md`](2026-08-15-bl36-archive-losslessness.md) (S88)

> **Revision note.** This report was adversarially reviewed inside its own session — 8 claim-refuters
> and 3 completeness critics against the frozen draft at `10d4fbf`. Three claims were refuted and
> nine defects found; every one is corrected below and the corrections are itemised in §Review
> corrections. **Nothing in the first draft's answer changed; a great deal of its evidence did.**

---

## Audit Summary

- **Scope:** the one open question S133 left — `docs/archive/HANDOFFS-through-2026-08-25.md.verify.sh`,
  generator **v1.3.0**, failing **L2 only**, while its six sibling v1.3.0 proofs pass.
- **Criteria:** (D1) are the shard's records intact, measured independently of the failing proof?
  (D2) what exactly did L2 lose, and in which commit? (D3) is the proof correct to fail? (D4) does
  the cause recur, and what is the adopter blast radius?
- **Coverage:** **19 of 19 shipped proofs run — but `docs/archive/` holds 22 shards, so 3 have no
  proof at all** (§Coverage, stated so this is not read as a whole-corpus clearance). 11 of 11
  proved `HANDOFFS` trims cross-tabulated. Record identity re-derived across **180 pre-trim receipt
  instances** spanning all 11 trims.
- **Findings:** 0 critical · 5 moderate · 3 minor.

### The answer

**The archives are intact. This is not record loss.** Across the trim commit `9038e40`, six receipts
became four retained plus two archived, with **0 missing and 0 added**, measured by SHA-256 of each
receipt body — a different function from the one L1/L3 assert on, so it is not an identity that
cannot fail. Widened to all 11 trims: **180 pre-trim instances, 0 unreachable at HEAD.**

**The proof is correct to fail, and the cause is a trap that recurs.** The failure was produced
**inside the trim commit itself**, by this repo's own documented post-trim fold-in rewriting a
front-matter count line that the ledger's spec does not declare as regenerated. Regenerating the
proof does **not** fix it — measured, not predicted.

**S133 named the right mechanism and the wrong corroboration.** Its receipt called the failing line
*"the regenerated shard-count line this very file documents as drifting… a trim rewrites it"* — which
is exactly the conclusion below. Only its supporting clause (*"S132 edited exactly that line in
`ec87d08`"*) is causally inert here, and S133 flagged that clause unproven itself.

---

## Method — and why it is not a re-run of the failing script

The failing script is the artifact under audit, so D1 is answered by a re-derivation sharing none of
its logic: receipts are split on **line-start** ```` ```handoff ```` fences — the live ledger contains
that string 11 times but only 6 at line start, so `text.index` would have stopped at a prose code
span — and compared as **content hashes**, a set difference over identities rather than a positional
concatenation. D2/D3 are answered by reading the commit and the generator. D4 is answered by
executing the off-diagonal cell: the newest shipped generator's logic pointed at older trims.
`docs/archive/` was not modified at any point (`git status --porcelain docs/archive/` empty
throughout); substituted copies live in the session scratchpad. **That is a statement about this
session's hygiene, not a freeze claim about the shards — see Finding #7.**

---

## Findings

### Finding #1 — No record loss at the 08-25 trim, and none across any trim (criterion D1)

- **Severity:** — (the adjudication's answer, not a defect)
- **Evidence, the trim under adjudication:** at `9038e40^` the live ledger held
  `[S110, S109, S108, S107, S106, S105]`; at `9038e40` it holds the first four and the shard holds
  `[S106, S105]`. **6 identities before, 6 after (live + shard). MISSING: none. ADDED: none.** All
  six bodies byte-identical.
- **Evidence, widened to the whole corpus.** The first draft swept 6 identities and called the one
  outlier "an anomaly." Re-run across **all 11 trims — 180 pre-trim receipt instances** against a
  HEAD universe of the live ledger plus 12 archive files (141 receipts): **0 unreachable by
  `(session, date)`**, and exactly **11 body-hash misses — one per trim, and in every case the
  trimming session's own receipt, `status: pending` before and `status: complete` at HEAD**
  (S61, S64, S87, S94, S98, S101, S104, S107, S110, S127, S132). This is an **11-of-11 structural
  invariant of the Phase 1B breadcrumb lifecycle**, not an anomaly — and the same shape BL-27 fix 2
  already documents as the frontier-receipt finalize.
- **The identity key, corrected.** The draft keyed on `session:` alone. This ledger's own front
  matter says a receipt is identified by **session + date**, because two session sequences share it:
  across 141 receipts there are only **134 distinct session ids** — S3, S5, S7, S8, S9, S10, S11 each
  name two different sessions. The sweep above uses `(session, date)`, which is 141-for-141 distinct.
  The 08-25 result is unaffected (its six ids are distinct and the content hash disambiguates), but
  the published method needed fixing before a successor applied it to the trims where the collisions
  actually live.
- **What "intact" does and does not cover.** This is a claim about the **record set**. It is not a
  claim that each shard's own front matter is correct — nothing asserts that (Finding #8).

### Finding #2 — S133's corroborating clause cannot reach this proof (criterion D2)

- **Severity:** Moderate
- **Location:** `docs/archive/HANDOFFS-through-2026-08-25.md.verify.sh:162-167`
- **What S133 got right, stated first.** Its receipt identifies the failing line as *"the regenerated
  shard-count line this very file documents as drifting (see the block above: a trim rewrites it, a
  prepend does not, 'recount before trusting it')"*, concludes *"benign front-matter maintenance, not
  record loss"*, and explicitly flags its own supporting clause: ***"VERIFY THAT BEFORE ASSUMING IT:
  it is a hypothesis I did not prove."*** **The mechanism it named — a trim rewrites it — is this
  report's conclusion, and its headline verdict is confirmed by Finding #1.**
- **What is inert:** the added clause *"S132 edited exactly that line in `ec87d08`"*. The observation
  is **factually true** — `ec87d08` did rewrite that line, `10 trims, 111 receipts` → `11 trims, 116
  receipts` — but it cannot be the cause of *this* proof's red:

  ```python
  if TRIM:
      before, after, shard = show(TRIM + "^", LIVE), show(TRIM, LIVE), show(TRIM, SHARD)   # :163
  else:
      before, after, shard = show("HEAD", LIVE), readf(LIVE), readf(SHARD)                 # :166
  ```

  At HEAD, `TRIM_SHA` resolves to `9038e40` and the `:163` branch is taken, pinning every operand to
  `git show` at `9038e40` and its parent — verified by the script's own printed
  `source : the trim commit 9038e40`. No commit after `9038e40` can enter that comparison.
- **The draft claimed more than this and was wrong to.** It asserted *"the script never reads HEAD or
  the working tree"* and called the refutation true *"by construction."* Both overstate. The `:166`
  else-branch reads HEAD **and** the working tree, and branch selection is a **runtime** condition on
  `git log --diff-filter=A -1` resolving — HEAD-dependent, not structural. Forcing `TRIM_SHA=""` on a
  scratchpad copy proves it is not merely a different label: **the else-branch prints
  `OK: L1, L2/front-matter, L3 hold` and exits 0**, against exit 1 on the shipped path. The
  conclusion survives because this shard has exactly one commit touching it, an Add, reachable from
  HEAD — a fact about this repo's history, not an invariant. See Finding #6.

### Finding #3 — The proof is correct, and the repo's own instructions walk sessions into it (D3/D4)

- **Severity:** Moderate — structural, and it recurs by design
- **Location:** `HANDOFFS.md:68-72` (the instruction) · `starter-kit/methodology_trim.py:336-339`
  (the declaration) · the proof's `REGEN_PATTERNS` at `:32` and its L2 clause at `:286-290`
- **Description:** L2's contract is that front matter *may gain* declared blocks but *may not lose or
  reword* anything, **unless** the change is confined to a **declared regenerated field**. The
  `HANDOFFS.md` `LedgerSpec` declares exactly one — `("retained receipt count", r"(This file
  currently holds \*\*)(\d+)(\*\*)", …)`. This ledger's front matter carries **two** derived counts.
  `9038e40` changed both: `holds **5**` → `**4**` (declared, correctly excused by
  `field_reversible`) and `Archived shards — 8 trims, 92 receipts` → `9 trims, 94 receipts`
  (**undeclared**, correctly reported as a lost line).
- **The trimmer did not write it; a session did, following this file's own instructions.**
  `apply_regenerated` (`:1117`) rewrites only declared fields and `insert_pointer` (`:1103`) appends
  a pointer block. `HANDOFFS.md:68-72` then tells the next trimming session to *"fold it into the
  table above as one row and delete the block."* Doing that — and recounting the aggregate it makes
  stale — **inside the trim commit** is what reddens the proof.
- **The commit is entirely transparent about it.** `9038e40`'s message says: *"FRONT MATTER: the
  generated pointer block was folded into the shard table as one row and deleted, per the standing
  instruction the front matter itself carries. The 9-trims/94-receipts heading was RECOUNTED from the
  table, not incremented."* Nothing was concealed; the proof simply cannot model it.
- **Precision:** the added table row is a permitted **gain**; L2 reports exactly **one** lost line.
  The sole cause is the count-line **rewrite**, not the row.
- **The evidence, with its real population.** The count line and the fold-in instruction were
  **both introduced by `eec1cbb` (2026-08-25)**, which lands after the 08-24 trim and before the
  08-25 trim. So the line **did not exist** at eight of the eleven trims, and the informative
  population is **three, not eleven**:

| Shard | Trim | Proof | `holds **N**` (declared) | `Archived shards` (undeclared) | Instruction present? |
|---|---|---|---|---|---|
| 08-02 | `c0e6944` | FAIL (Class A) | 30 → 30 | *line does not exist* | no |
| 08-09 | `a46f2f9` | FAIL (Class A) | 30 → 3 | *line does not exist* | no |
| 08-11 | `721853b` | OK | 28 → 4 | *line does not exist* | no |
| 08-15 | `17753d9` | OK | 9 → 3 | *line does not exist* | no |
| 08-17 | `7fee8bd` | OK | 4 → 3 | *line does not exist* | no |
| 08-18 | `5ec1bd2` | OK | 3 → 3 | *line does not exist* | no |
| 08-23 | `470cfd4` | OK | 3 → 3 | *line does not exist* | no |
| 08-24 | `9cf4ae0` | OK | 3 → 3 | *line does not exist* | no |
| **08-25** | **`9038e40`** | **FAIL (Class B)** | 5 → 4 | **8/92 → 9/94 REWRITTEN** | **yes** |
| 08-29 | `59a7677` | OK | 4 → 4 | left stale in-commit | yes |
| 08-30 | `78a29f8` | OK | 4 → 4 | left stale in-commit | yes |

  **Read honestly: one positive and two negatives.** Of the three trims where the line existed, the
  one that recounted it in-commit is red and the two that deferred are green. The other eight rows
  carry no information about this mechanism and are shown to make that explicit.
- **The out-of-band correctors, named correctly.** The deferred corrections were made later by
  `28b2361` (S127) and **`ec87d08` (S132)** — the very commit S133 cited. *(The draft cited
  `273afff` here; that commit changes four `HANDOFFS.md` lines and touches neither count line. The
  error is corrected and worth stating plainly: the report held the right commit in Finding #2 and
  cited the wrong one for the pattern its recommendation depends on.)*
- **Impact:** **within its real population, the proof rewards deferring the documented fold-in and
  punishes doing it promptly, and nothing says so.** A session that follows `HANDOFFS.md:68-72`
  conscientiously ships a red losslessness proof for an intact archive — the exact confusion BL-36
  exists to prevent.

### Finding #4 — Regenerating does not fix Class B, but it does help Class A (criterion D4)

- **Severity:** Moderate — it re-scopes BL-36's standing disposition in both directions
- **Class B — regeneration is useless.** v1.5.0 logic (copied from the 08-30 proof, only `SHARD`
  substituted) against the 08-25 trim fails with identical text: `FAIL: L2 FRONT MATTER lost 1
  line(s)`, **exit 1 read bare**. Control on its own shard: **exit 0**. The lost line is frozen in
  the commit; no generator deriving `before`/`after` from `show(TRIM^)`/`show(TRIM)` can un-see it.
- **Class A — regeneration helps, and the draft declined to measure this with the instrument in
  hand.** Same method, four Class A shards:

| Class A shard | Shipped proof | Regenerated (v1.5.0 logic) |
|---|---|---|
| `CHANGELOG-through-2026-08-02` | exit 1 | **exit 0 — GREEN** |
| `CHANGELOG-through-2026-08-09` | exit 1 | **exit 0 — GREEN** |
| `HANDOFFS-through-2026-08-02` | exit 1 | exit 1, now naming `MISSING: session: S61` |
| `HANDOFFS-through-2026-08-09` | exit 1 | exit 1, now naming `MISSING: session: S64` |

  So regenerating would take the corpus from **5 failing proofs to 3**, and convert two opaque reds
  into diagnosed ones that name the frontier receipt. BL-36's standing *"regenerate all four"*
  disposition is **better supported than the draft implied for Class A, and inapplicable to Class B.**
- **The code fix that would work for future Class B proofs, tested.** `field_reversible` compares the
  **residue** — the line minus the matched span — byte-for-byte, so a `REGEN` pattern must span
  **both** numbers at once:

| Candidate pattern | Excuses the change? |
|---|---|
| `(Archived shards — )(\d+)( trims,)` | **False** — the other number sits in the residue |
| `(trims, )(\d+)( receipts)` | **False** — same reason |
| `(Archived shards — )(\d+ trims, \d+)( receipts)` | **True** |

  **This cannot reach the 08-25 proof**, whose `REGEN_PATTERNS` is a frozen literal at `:32`. It
  helps future proofs only, requires the trimmer to compute the aggregate itself (it does not
  today), and touches a **distributed** file (`bin/_manifest.py:50`). Named, not taken (FM #17).

### Finding #5 — S88's Defect-B claim was correctly scoped; what dates it is the second count line (D3)

- **Severity:** Minor — the draft's charge is withdrawn
- **Description:** the draft said S88's *"Defect B — the regenerated front-matter count line.
  Genuinely fixed between v1.1.1 and v1.1.3"* was **"too strong as stated."** That is unfair.
  *"Regenerated"* is this codebase's term of art for a **declared** field
  (`methodology_trim.py:336` `regenerated=(…)`), so S88 scoped its claim to the declared line, and
  v1.1.3 did genuinely fix that. **The correct statement is about timing, not overreach:** the second
  count line entered `HANDOFFS.md` at `eec1cbb` on 2026-08-25, **ten days after** S88's audit. S88
  was true when written and remains true within its scope; the corpus grew a shape it had no way to
  enumerate.
- **A prior data point the draft's table hid.** `HANDOFFS-through-2026-08-09`'s shipped proof fails
  **three** ways, not two: `L1`, `L3`, **and** `FAIL: L2 FRONT MATTER lost 1 line(s), first: '**Older
  receipts are archived.** This file currently holds **30**'`. So an L2 front-matter-count failure
  already existed in the corpus — on the **declared** line, under v1.1.1, which is exactly the defect
  v1.1.3 fixed. The sharper framing of Class B is therefore *"the only L2 front-matter failure not
  excused by `field_reversible`"*, which is testable, rather than *"the only v1.3.0+ failure"*, which
  is a version coincidence.

### Finding #6 — The proof's fallback branch prints green and asserts nothing (criterion D3)

- **Severity:** Moderate — found while refuting Finding #2's own warrant
- **Location:** `…verify.sh:165-167`
- **Description:** when `TRIM_SHA` is empty the script compares `show("HEAD", LIVE)` against the
  **working tree**, and reports `OK: L1, L2/front-matter, L3 hold`, **exit 0**. On the 08-25 shard
  that fallback prints `6 before = 6 retained + 0 archived; added by the trim commit: 2` — it
  believes nothing was archived and the shard's two records are new. **It is a green verdict that
  asserts nothing about the trim it names.**
- **When `TRIM_SHA` is empty:** the trim is not yet committed (the intended case, and the label says
  so); the shard's add-commit is not reachable from the current tip — `git log --diff-filter=A -1 …`
  at any pre-trim tip returns empty, so **the same frozen script run from an older checkout prints
  green**; or the shard arrives by rename, which `--diff-filter=A` does not match.
- **Impact:** the artifact whose entire purpose is *"run it; do not trust a digest"* has a reachable
  path on which running it proves nothing, distinguished from the real verdict only by a one-line
  `source :` label a reader must notice. Not a defect in this adjudication's answer; a defect in the
  guarantee the artifact advertises.

### Finding #7 — The archive-freeze invariant is asserted by nothing, and has already failed twice (D4)

- **Severity:** Moderate
- **Description:** every proof binds `TRIM_SHA` and then reads `show(TRIM, SHARD)` — **the blob the
  creating commit wrote**. No proof reads the shard on disk or at HEAD. A shard edited after
  archiving therefore keeps a green proof forever, and the file readers see is not the file the proof
  proves.
- **Measured, the invariant has already failed twice** — and on exactly the two shards that have no
  proof at all: `docs/archive/CHANGELOG-through-v3.6.md` was edited by `020ba3f`, and
  `docs/archive/HANDOFFS-archive.md` by `7752114` (*"reconcile nine `commit:` fields that named no
  sha"*), which rewrote fields inside already-archived receipt bodies. **Unproven and unfrozen are
  the same set.** S88's Finding #7 saw the first of these; the second, and the fact that no mechanism
  could ever see either, is new here.
- **Impact:** this constrains Recommendation 4 — annotating a shard is exactly the class of edit that
  nothing detects, so it must be gated, not casual.

### Finding #8 — A shard's own front matter makes verifiable claims that nothing verifies (D1)

- **Severity:** Minor
- **Description:** in the proof, the shard's front matter `sfront` is bound at `:171` and used at
  exactly one place — `:292`, inside the `leaked` test — i.e. only to ask whether a *live*
  front-matter line travelled into the shard. The 08-25 shard's own header asserts *"Holds **2
  record(s)**, 2026-08-25 → 2026-08-25"*, *"Counts here are computed from the file itself, never
  carried forward"*, and *"This shard is frozen"*. **None of the three is checked by any L clause**,
  and Finding #7 shows the third is false for two sibling shards.
- **Impact:** "the archives are intact" is a claim about records. A reader reasonably takes it as a
  claim about the artifact. Those are not the same, and this report says which one it made.

---

## Coverage

**19 of 19 shipped proofs were run. `docs/archive/` holds 22 shard `.md` files, so three archives
have no losslessness proof at all** and could not go red if they were wrong:

| Unproven shard | Created by | Why it has no proof |
|---|---|---|
| `HANDOFFS-archive.md` (174,296 B, 19 receipts) | `7a71df0` — BL-9 L1, 216 KB → 51 KB | a **hand** archive predating the trimmer; the single archive event with the highest prior probability of loss, **and it was later edited** (`7752114`) |
| `CHANGELOG-through-v3.6.md` (50 entries) | `3aee4e3` | predates the trimmer; **later edited** (`020ba3f`) |
| `CHANGELOG-through-2026-08-01.md` (18 entries) | `020ba3f` | predates the trimmer |

Record identity was re-derived across **180 pre-trim instances spanning all 11 proved `HANDOFFS`
trims** (Finding #1). It was **not** re-derived for the 8 `CHANGELOG` trims, nor for any of the three
unproven archives above. S88 covered the corpus as it stood on 2026-08-15 by HEAD-reachability.
**This report is not a whole-corpus clearance, and the gap is larger than its first draft said.**

---

## Structural Observations

1. **A frozen proof is a claim about commit hygiene, not only about data.** S88 said this about
   bundled record additions; Class B is the same sentence one zone up. The archive is intact, the
   proof is correct, and the red is produced entirely by *what else rode in the commit*.
2. **A file's instructions and its verifier disagree, and only the verifier is mechanical.**
   `HANDOFFS.md:68-72` asks the next trimming session to fold in the pointer block; L2 punishes doing
   so in the trim commit. Both arrived in the same commit, `eec1cbb`.
3. **A carve-out list is a population, and populations drift.** `regenerated` names the derived
   fields as of the day it was written. Nothing detects a second derived line being added later —
   which is how a fixed defect reappeared under a newer generator. **This argument cuts against
   Recommendation 2 as well as for it** (see there).
4. **Adopter blast radius is bounded today and not bounded structurally.** The distributed seed
   `starter-kit/HANDOFFS.md` carries **neither** count line, so no adopter inherits this trap now.
   The mechanism is generic: `methodology_trim.py` is distributed, and any adopter keeping a derived
   line in a pinned front-matter zone and updating it in the trim commit gets the same red proof.
   `CHANGELOG.md`'s spec declares `regenerated=()` with the comment *"the live root ledger carries no
   count sentence today"* — verified still true, and a time-bound claim with no detector behind it.
5. **Detection and cleanliness are in tension here, and the report that first drafted this did not
   notice.** The only mechanism that has ever noticed this count line being rewritten is the L2
   clause that goes red. Moving the edit out of the trim commit makes the proof green by moving the
   change to where **nothing looks** — no checker, test or hook anywhere in `bin/`, `tools/`,
   `starter-kit/` or `.githooks/` validates that line.

---

## Comparison with Prior Audits

| Metric | S88 (2026-08-15) | S134 (2026-09-01) | Trend |
|---|---|---|---|
| Shipped proofs in corpus | 6 | **19** | grew 3.2× |
| Archives with **no** proof | 3 (its Finding #6) | **3** | unchanged |
| Failing proofs | 4 | **5** | +1, a new class |
| Failing classes | 1 (Defect A, bundling) | **2** (A + B, undeclared derived line) | — |
| Record loss found | 0 | **0** | stable |
| Prior conclusion revised | — | none — S88's Defect-B claim **upheld** as scoped | — |

---

## Recommendations

1. **Do not regenerate the 08-25 proof.** Measured: the newest generator fails it with identical text
   (Finding #4). Regeneration would spend the archive-freeze exception and change nothing.
2. **Delete the hand-maintained aggregate, or attach its recompute command — this is already policy,
   not new policy, and it is the cheapest fix.** The distributed seed
   `starter-kit/HANDOFFS.md:115-116` already rules that a shard pointer records how many receipts it
   holds *"with the command that recomputes those counts, **never a hand-maintained number**."*
   `HANDOFFS.md:49`'s `**Archived shards — 11 trims, 116 receipts.**` is precisely a hand-maintained
   aggregate with no recompute command — unlike its sibling `holds **N**` line, which carries one.
   Removing it removes the undeclared derived line at the root: **no protocol rule, no distributed
   code change, no operator go-ahead, no adopter-facing route.** *(This option was absent from the
   first draft, which framed the fix as a binary between recs 3 and 4 below.)*
3. **If the line stays, the rule is narrower than "a trim commit touches nothing but the trim":
   the trim commit must contain no hand edit to the ledger under proof.** State it that way. The
   broader wording is not achievable as written — `.githooks/pre-commit` refuses any commit changing
   tracked content unless `CHANGELOG.md` is co-staged, and its carve-out cannot fire for a trim
   (which stages `docs/archive/` paths). The trimmer writes that `CHANGELOG` entry itself, so the
   narrow rule is satisfiable and the broad one is not.
   **Cost this against Structural Observation 5 before adopting it:** it converts a loud, correct red
   into a silent unverified edit. It removes the detector, not the risk.
4. **Declaring the second count line** (Finding #4's both-numbers pattern) helps only *future*
   proofs, cannot reach the 08-25 artifact, and needs the trimmer to compute the aggregate. It is
   the only route with **adopter reach**, which is the mechanism Structural Observation 4 calls
   unbounded. Distributed file — **operator go-ahead required.**
5. **Annotate the 08-25 shard's front matter — and treat it as gated, not as documentation.**
   Editing a shard is a deliberate exception to the archive-freeze rule
   (`starter-kit/HANDOFFS.md:142-144`, *"Nothing else in a shard is rewritten"*), it is the one class
   of edit Finding #7 shows **nothing can detect**, and both S88 and BL-36 record it as an operator
   decision. **Needs its own go-ahead.** It is nonetheless the only recommendation that addresses the
   artifact under adjudication.
6. **Correct the record where it actually lives — S133's receipt and its `CHANGELOG.md` echo, not
   BL-36.** BL-36's detail entry contains no mention of Class B, `ec87d08`, S132 or the 08-25 shard;
   its residual disposition predates that shard's existence and was Class-A-only by construction. The
   two statements needing correction are S133's, and S133 already self-corrected the
   counter-example half.
7. **Close the coverage gap, sized honestly:** 12 proved trims have never had an identity
   re-derivation (8 `CHANGELOG` + the 4 Class A), **and three archives have no proof at all** — the
   hand-made `HANDOFFS-archive.md` first, since it is the least mechanised and was later edited.

---

## Review corrections

Nine defects the in-session adversarial review found in the frozen draft at `10d4fbf`, all corrected
above. Recorded rather than silently fixed, because a report that claims measurement discipline owes
its own error list.

| # | Defect in the draft | Correction |
|---|---|---|
| 1 | Table marked `unchanged` for 08-18/08-23/08-24; population stated as "all eleven, 1-to-1" | The line **did not exist** at 8 of 11 trims (`eec1cbb`, 2026-08-25). Informative population is **3** — 1 positive, 2 negatives |
| 2 | *"`273afff` is a recent example"* of the out-of-band correction | `273afff` touches neither count line. The correctors are `28b2361` and **`ec87d08`** |
| 3 | *"The script never reads HEAD"*; *"false by construction"* | The `:166` else-branch reads both and **flips the verdict to green**. Runtime condition, not construction → Finding #6 |
| 4 | *"five sibling v1.3.0 proofs pass"* (inherited from S133, not re-derived) | There are **7** v1.3.0 proofs; **6** siblings, all pass |
| 5 | S110 *"3,858 B → 9,890 B"* | Those are **characters**. Bytes are **3,880 → 9,988** (body excluding fences and trailing newline; other conventions give 3,881/9,989 and 3,896/10,004 — the figure is convention-sensitive and the draft named neither) |
| 6 | S110 *"differing only in the fields close-out writes"* | Only `session` and `date` survive verbatim; `active_task` and `next_steps` were **rewritten and shrank** (1,568→837 and 2,217→1,629 chars) |
| 7 | Finding #5 charged S88's claim as *"too strong as stated"* | **Withdrawn.** S88 scoped it with *"regenerated"* = declared. The issue is timing, not overreach |
| 8 | Finding #6 charged `9038e40`'s record as *"silent about the rest"* | **Withdrawn.** The commit message states the fold-in and the recount explicitly. The generic *"a tool action, not a session's judgment"* line is emitted verbatim by the distributed tool (`methodology_trim.py:1168`), not written by the session |
| 9 | *"Coverage: 19 of 19 … Nothing skipped"* | The corpus is **22 shards / 19 proofs**. Three unproven archives named in §Coverage |

Two further draft claims the review attacked and **failed** to break: the record-intactness
re-derivation (reproduced independently, including under `bin/check-handoff`'s wider
fence-to-next-fence record unit — 6 of 6 identical, 0 delta), and the measured claim that
regeneration cannot fix Class B.

---

## Reproduction

```bash
# every shipped proof (5 of 19 FAIL); note 22 shards exist, 19 proofs
for f in docs/archive/*.verify.sh; do bash "$f" >/dev/null 2>&1; echo "$? $f"; done

# the cause, one commit deep
T=9038e405921d9c6bf73300ae4fe4c00c772de1d3
git show "$T^:HANDOFFS.md" | grep 'Archived shards'   # 8 trims, 92 receipts
git show "$T:HANDOFFS.md"  | grep 'Archived shards'   # 9 trims, 94 receipts

# the real population: the line exists at only 3 of 11 trims
for T in c0e6944 a46f2f9 721853b 17753d9 7fee8bd 5ec1bd2 470cfd4 9cf4ae0 9038e40 59a7677 78a29f8; do
  printf '%s ' "$T"; git show "$T^:HANDOFFS.md" | grep -c 'Archived shards'; done

# off-diagonal: newest generator's logic on an older trim (docs/archive/ untouched)
cp docs/archive/HANDOFFS-through-2026-08-30.md.verify.sh /tmp/v150.sh
sed -i '' 's|HANDOFFS-through-2026-08-30.md$|HANDOFFS-through-2026-08-25.md|' /tmp/v150.sh
bash /tmp/v150.sh; echo "exit=$?"     # 1 — read bare, never through a pipe

# Finding #6: the fallback branch prints green
sed 's|^TRIM_SHA=.*|TRIM_SHA=""|' docs/archive/HANDOFFS-through-2026-08-25.md.verify.sh > /tmp/eb.sh
bash /tmp/eb.sh; echo "exit=$?"       # 0, "OK: ... hold"
```
