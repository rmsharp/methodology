# Per-Record Budget Reduction — Plan

**Status:** **RATIFIED 2026-08-25** — the operator chose **12,288 (12 KiB)**, §9's one blocking
decision, over the costed alternatives 10,240 and 8,192. **Phase 1 IMPLEMENTED** the same day
(session S106): the constant, its derivation comment, the remediation text, thirteen
`bin/tests.sh` couplings and the `.context-budget.json` note. **Phases 2 and 3 remain pending**
and are each a separate session. §5.2's inventory was incomplete — see the S106 correction below it.
**Author:** S105 (2026-08-25). **Origin:** operator request following S104's structural finding.
**Scope:** fork-only / canonical-only. **No distributed file is touched** — see §7.

---

## 1. The problem, stated as a measurement

`HANDOFFS.md` cannot be brought under control by trimming. Its steady-state size is fixed by two
constants set independently:

| term | value | where it comes from |
|---|---|---|
| ceiling | 65,536 B | `.context-budget.json`, `HANDOFFS.md` → `max_bytes` |
| retention floor | 3 receipts | `bin/tests.sh` Test 34 reads `ids[1]`/`ids[2]` of the live ledger |
| per-record budget | 18,432 B | `bin/check-handoff:606` `RECORD_BUDGET_BYTES` |
| header allowance | 8,000 B | the derivation comment, `bin/check-handoff:584` |

3 × 18,432 + 8,000 = **63,296 B against a 65,536 B ceiling** — **2,240 B** of structural slack, far
less than one receipt. **Two header terms are in circulation and they must not be mixed:** the
derivation uses the 8,000 B *allowance* (→ 63,296 B, slack 2,240 — the figure in the comment itself),
while S103's widely-quoted `6,016 + 3 × 18,432 = 61,312 B` uses the header as *measured then*. Today's
header measures **6,913 B** (→ 62,209 B). This plan uses the **allowance** throughout, because that is
what the constant is derived from. On any of the three readings the conclusion is identical: after
S104's trim the file stood at 57,892 B, and `--cut 3` is already the most aggressive cut the floor
permits, so **the ledger must be trimmed nearly every session, by construction.**

The budget was never chosen as a limit. It is `(65,536 − 8,000) / 3 = 19,178 → 18,432`, derived to be
*as large as will fit*. It was set to **accommodate** growth, not restrain it — and the growth is the
whole story:

| population | mean record |
|---|---|
| oldest 10 receipts | **5,043 B** |
| newest 10 receipts | **18,225 B** |
| ratio | **3.61×** (n = 111, largest ever 21,267 B) |

## 2. What a session actually pays — the number the operator asked about

**The ledger is read and gleaned, never resident.** It has no `@`-import; the only auto-loaded file
is `CLAUDE.md` (11,064 B), which merely mentions it. Measured across 81 transcripts of this repo
(recorded at `bin/check-handoff:590-597`): read **whole exactly once**, read **in part 593 times**,
median span **25 lines**, largest ever 220, against a then-452-line file.

That matches what the protocol mandates: Phase 0 step 6 takes a **frontier** (`git log -1`, no
content) and Phase 3A reads **the predecessor's receipt in full** — one record.

> **Per-session context cost = front matter + one receipt ≈ 6,913 + ~18,000 ≈ 25 KB.**
> Not the file's 57,892 B. Paid once, on demand — but once read it stays in that session's context.

So the term worth attacking is **the receipt**, not the file. Halving the receipt halves the
recurring cost; trimming the file does not touch it.

## 3. Where the bytes are — and why the cut is cheaper than it looks

Every recent receipt splits the same way:

| receipt | total | fenced fields | trailing prose | prose share |
|---|---|---|---|---|
| S104 | 18,407 B | 13,019 B | 5,388 B | 29% |
| S103 | 15,533 B | 10,920 B | 4,613 B | 30% |
| S102 | 17,039 B | 12,386 B | 4,653 B | 27% |

The trailing prose is the Phase 3A predecessor evaluation and the Phase 3B self-assessment. **These
are additive to the six mandatory handoff requirements**, which live in the fenced fields — and the
receipt already carries their conclusions as the structured `predecessor_score` and `self_score`
fields. `SESSION_RUNNER.md` Phase 3A directs the *evaluation* to `SESSION_NOTES.md`; the essay in the
receipt is a fork convention on top of that.

**Consequence: the six mandatory requirements as currently written already fit in ~12 KB**
(fenced fields mean 12,108 B). A cut to 12 KiB falls almost entirely on prose that no requirement
mandates. A cut to 8 KiB would not — it would force cutting the requirements themselves, which is
failure mode #15 (minimal handoff) territory.

## 4. The decision

### 4.1 Recommended: `RECORD_BUDGET_BYTES` 18,432 → **12,288 (12 KiB)**

| | now | proposed |
|---|---|---|
| per-record budget | 18,432 B | **12,288 B** |
| steady state (3 × budget + 8,000) | 63,296 B | **44,864 B** |
| share of the 65,536 B ceiling | 96.6% | **68.5%** |
| slack | 2,240 B (≪ 1 receipt) | **20,672 B (> 1 receipt)** |
| per-session context cost | ~25 KB | **~19 KB** |

Rationale: 12,288 sits just above the current fenced-field mean (12,108 B), so the six mandatory
requirements survive unchanged and the reduction lands on the additive essays. Slack exceeds one full
receipt, so a trim becomes occasional instead of mandatory-every-session.

### 4.2 Costed alternatives (recorded so the choice is visible, not so both are done)

| option | steady state | verdict |
|---|---|---|
| **10,240 (10 KiB)** | 38,720 B, 59.1% | Viable but cuts into fenced fields for the two largest recent receipts. Defensible if the operator prefers a harder stop. |
| **8,192 (8 KiB)** | 32,576 B, 49.7% | **Not recommended as step 1.** Current fenced fields are 10,920–13,019 B, so this cuts the six requirements themselves. Revisit only after measuring whether fields compress — see §6, Phase 3. |
| leave at 18,432 | 63,296 B, 96.6% | Status quo: a trim nearly every session, ~25 KB per-session cost. |

### 4.3 A conceptual change this plan makes explicit

The formula `(ceiling − header allowance) / floor` is a **ceiling-fitting device, not a target.** Once
the budget is deliberately reduced it becomes a **policy number**, and the formula's role changes from
*definition* to *check that it fits*: assert `3 × budget + header_allowance ≤ 65,536`.

This matters for sequencing. Shrinking the front matter (§6 Phase 2) lowers the header allowance,
which under the old reading would *raise* the derived budget and hand the savings straight back.
**The implementing session must state the budget as policy and use the formula only as an assertion.**

## 5. Evidence-based inventory (MANDATORY — every site found by grep, not by recall)

Commands used: `git grep -n 'RECORD_BUDGET_BYTES'`, `git grep -nE '18,?432'`,
`git grep -nF '8,000'`, `git grep -nE '65,?536|max_bytes'`.

### 5.1 Must change — the constant and its derivation

| file:line | what | action |
|---|---|---|
| `bin/check-handoff:606` | `RECORD_BUDGET_BYTES = 18432` | set to the ratified number |
| `bin/check-handoff:578-604` | the derivation comment block (ceiling / header / floor table, arithmetic at `:588`) | rewrite per §4.3 — policy number + fit assertion |
| `bin/check-handoff:810` | remediation text printed to the user: `"(65,536 B ceiling − 8,000 B header allowance)"` | rewrite to match |

### 5.2 Must change — tests that hardcode the value or its arithmetic

| file:line | coupling | note |
|---|---|---|
| `bin/tests.sh:2738` | `BUDGET38, TARGET38 = 18432, 18432 + 512` | fixture arming constant |
| `bin/tests.sh:2819` | asserts the exact string `record $S38 is 20,000 B, over the 18,432 B per-record budget by 1,568` | **arithmetic changes** — the `by N` term is derived |
| `bin/tests.sh:2826, 2829-2830` | the exactly-at-budget edge case, `add_record38 18432` | edge test must move with the constant |
| `bin/tests.sh:2851, 2857` | scope check counting live records `> 18432` | |
| `bin/tests.sh:2917, 2920` | mutant asserting `record $S38 is 18,432 B` | |
| `bin/tests.sh:2956` | mutant does a **literal string replace** of `"RECORD_BUDGET_BYTES = 18432"` → `50000` | **highest-risk site.** `mutate` aborts loudly if the edit is a no-op, so this fails visibly rather than silently — but it must be updated in the same commit. |
| `bin/tests.sh:2704, 2732` | explanatory comments citing 18,432 | |

> **⚠ S106 CORRECTION (2026-08-25, written by the session that executed Phase 1): this inventory was
> incomplete by two sites, and one of them would have gone GREEN while silently ceasing to test
> anything.** The table above is left as written — this note records what it missed, and why.
>
> - **`bin/tests.sh:2832-2836` — the one-byte-OVER half of the edge test** (`add_record38 18433`,
>   and three message strings naming `18,433 B`). **Missed because the inventory's own grep pattern
>   was `18,?432`, which cannot match `18433`.** The at-budget half (`:2826`) was listed, its
>   over-by-one twin was not. **This is the dangerous one:** left at 18,433 against a 12,288 budget
>   the record is still over budget, so the assertion still matches and the row still PASSES — while
>   testing a record 6,145 B past the cap instead of one byte past it. The `>` → `>=` boundary
>   mutant (M1) would then be scored *killed* by a record that any budget catches. A green suite
>   would have reported full coverage of an edge nothing was standing on.
> - **`bin/tests.sh:2945` — M3's replacement payload**, the forged summary line
>   `"record budget: 0 unwritten record(s), 0 over 18,432 B"`. Functionally inert (M3's assertion
>   only looks for the *absence* of the `SKIPPED` marker), but the payload's whole job is to be a
>   convincing forgery of a line the code can actually emit, and at the old number it stops being
>   one. Updated for that reason, not for a behavioural one.
>
> **Generalisation for Phase 2/3:** a value's *derived neighbours* (`N+1`, `N-1`, `N + 512`, an
> overage term) do not match a grep for `N`. Enumerate the edge cases and the arithmetic, not only
> the literal. Counting `:2829-2830` and `:2832-2836` as their own rows, Phase 1 touched **thirteen**
> `bin/tests.sh` sites, not nine.


### 5.3 Documentation to update

| file:line | what |
|---|---|
| `.context-budget.json:59` | the `_` note for `HANDOFFS.md` restating the budget and its derivation |

### 5.4 Explicitly NOT to change — verified, not assumed

- **`CHANGELOG.md` and `HANDOFFS.md` historical prose** (`CHANGELOG.md:177, 193, 221, 232, 293, 351, 423, 436, 471, 507, 598, 641`; `HANDOFFS.md:81, 95, 119, 171, 239`, and every `docs/archive/HANDOFFS-*.md` hit — **re-derived after this session's own claim entry shifted them; the pre-write numbers were stale by 5**). These are **frozen records of what was true when written**. Rewriting them would falsify the ledger and break archive losslessness proofs. FM #22.
- **`starter-kit/methodology_trim.py`** — verified by grep to have **no** coupling to the per-record budget; it knows only the whole-file budget.
- **`.context-budget.json` `max_bytes: 65536`** — the ceiling is not being changed by this plan.
- **Test 34's floor of 3** — unchanged. Lowering the budget does not touch it.

### 5.5 The de-risking finding

`check_record_budget` (`bin/check-handoff:652-679`) checks **only the newest record, and only when it
differs from its frozen copy at git HEAD**. The budget is therefore **prospective-only**: committed
receipts are exempt by construction (Test 38 asserts exactly this). **Lowering the budget cannot
redden any existing receipt, and no receipt needs rewriting.** This is what makes the change small.

---

## 6. Phases — one per session, each with a STOP

### Phase 1 — Lower the constant (ONE SESSION)

**Do:** set `RECORD_BUDGET_BYTES` to the ratified number; rewrite the derivation comment per §4.3;
update `bin/check-handoff:810`; update every `bin/tests.sh` site in §5.2 and the note in §5.3.

**DONE looks like:** `bin/check-handoff` reports the new budget; `bin/tests.sh` is green with no rows
lost; the Phase 1 session's *own* receipt is written under the new budget — the guard applied to its
own author, the precedent set when the budget was introduced (`CHANGELOG.md:598`, *"This receipt
measures 17,162 B against the 18,432 B…"*).

**Verification commands:**
```
python3 bin/check-handoff                 # newest receipt within the NEW budget
python3 bin/check-handoff --all
bash bin/tests.sh                          # row-for-row diff vs a pre-change control
python3 starter-kit/context_budget.py      # exit 0
git grep -nE '18,?432' -- bin/            # must return ZERO hits under bin/
```

**Surface:** the local repo working tree and a pristine `git worktree` control at the pre-change SHA.
**What this surface cannot enforce:** nothing about adopters (no distributed file changes), and
nothing about GitHub delivery. There is no CI surface for this repo's suite.

**Control discipline:** run the pre-change `bin/tests.sh` in a `git worktree` at the claim commit, not
in the tree being edited, and diff the sorted `PASS/FAIL/SKIP` rows. Expect **zero rows lost** and
changes confined to rows whose names carry the budget number.

**STOP. Close out.**

### Phase 2 — Compact the front matter and re-derive the allowance (ONE SESSION)

**Do:** collapse the 7 archive pointer blocks (3,132 B, **45% of the 6,913 B front matter**, growing
~447 B per trim) into a single compact index; lower the header allowance to the re-measured figure and
**bank the saving as slack rather than letting the formula raise the budget** (§4.3).

**DONE looks like:** front matter measurably smaller; `3 × budget + new_allowance ≤ 65,536` asserted;
the budget constant **unchanged from Phase 1**.

**Verification commands:**
```
bash bin/tests.sh
python3 bin/check-handoff --all
bash docs/archive/*.verify.sh              # every losslessness proof still green
python3 starter-kit/context_budget.py
```

**Surface:** local working tree. **Cannot enforce:** that a future trim will not re-grow the header —
that is what the compact index format is for, and it should be checked again at the next trim.

**Note:** a predecessor already flagged this redundancy against itself and left it
(`docs/archive/HANDOFFS-through-2026-08-18.md:65`). It is a known, deliberate debt, not a new finding.

**STOP. Close out.**

### Phase 3 — OPTIONAL, only if the operator wants a harder stop (ONE SESSION)

**Do:** measure whether the fenced fields themselves compress without losing any of the six mandatory
requirements. If they do, consider 10,240 or 8,192.

**DONE looks like:** a measurement, and a recommendation — **not** a further reduction taken on
assumption. **Gate:** do not reduce below the measured fenced-field maximum. Failure mode #15 is the
risk being managed here, and it is not detectable by any checker: `bin/check-handoff` asserts a
receipt's *presence and completeness*, never its *quality*. The only detector is the next session's
3A score.

**Verification commands:**
```
# per-receipt fenced-field vs trailing-prose split across the live ledger + every shard,
# so the recommendation rests on the whole population, not the three surviving receipts
python3 - <<'EOF'
import re, glob
for f in ['HANDOFFS.md'] + sorted(glob.glob('docs/archive/HANDOFFS*.md')):
    t = open(f, encoding='utf-8').read()
    st = [m.start() for m in re.finditer(r"(?m)^```handoff$", t)] + [len(t)]
    for i in range(len(st) - 1):
        rec = t[st[i]:st[i+1]]
        close = rec.index('\n```\n', 3) + 5
        print(f, len(rec.encode()), len(rec[:close].encode()), len(rec[close:].encode()))
EOF
python3 bin/check-handoff --all      # population intact after any reformatting trial
bash bin/tests.sh                    # only if a constant actually changes
```

**Surface:** the committed ledger plus every archived shard — i.e. the full 111-receipt population,
not the 3–4 live ones, since a recommendation drawn from the survivors alone is drawn from whatever
the last trim happened to retain. **What this surface cannot enforce:** handoff *quality*.
`bin/check-handoff` asserts presence and completeness, never quality, so no command here can tell you
a smaller receipt is still a good one. If Phase 3 reduces the budget, the only real detector is the
next session's 3A score — treat one low score after the change as a signal to revert, not as noise.

**STOP. Close out.**

---

## 7. Blast radius, risks, and what is not in scope

**Distribution:** `bin/check-handoff` is **canonical-only** — confirmed against `bin/_manifest.py`,
which distributes `starter-kit/HANDOFFS.md` (the seed) and `starter-kit/context-budget.json`, and
carries **no** `check-handoff` row. `bin/tests.sh` is canonical-only. **No adopter receives any file
this plan changes.** No PR, no upstream action; this is fork-side work.

**Risks:**

1. **The quality trade is real and unmeasurable by tooling.** A smaller budget can produce a worse
   handoff, and no checker will say so. Mitigation: Phase 1 stops at a number above the current
   fenced-field mean, so the cut lands on additive prose; Phase 3 is gated on measurement.
2. **`bin/tests.sh:2956` is string-coupled to the constant's exact source text.** Missing it breaks a
   mutant. It fails loudly (`mutate` aborts on a no-op), but it must be in the same commit.
3. **The `by N` term at `bin/tests.sh:2819` is derived arithmetic**, not a constant — recompute it,
   do not search-and-replace it.
4. **Do not rewrite historical prose** (§5.4). Nine `CHANGELOG.md` sites and every archived shard
   state the old number as a fact about their own moment. They are correct as written.

**Not in scope:** the 65,536 B ceiling; Test 34's floor of 3; `methodology_trim.py`; anything
distributed; the four owed `FRAMEWORK_LEARNINGS.md` rows.

## 8. Reasoning tier

Phase 1 touches a guard and its mutation harness — cross-file invariants where an error is silent and
compounding. Recommend the **deepest available reasoning mode** for Phase 1, per
`ITERATIVE_METHODOLOGY.md` §Matching Reasoning Effort to Stakes. Phase 2 is mechanical text work at
ordinary effort.

## 9. Open question for the operator — ratify before Phase 1

**Which number?** The plan recommends **12,288 (12 KiB)** and records 10,240 and 8,192 as costed
alternatives in §4.2. Phase 1 cannot start until this is settled, because every site in §5.2 encodes
it.
