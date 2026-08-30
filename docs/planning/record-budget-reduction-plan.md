# Per-Record Budget Reduction — Plan

**Status:** **RATIFIED 2026-08-25** — the operator chose **12,288 (12 KiB)**, §9's one blocking
decision, over the costed alternatives 10,240 and 8,192. **Phase 1 IMPLEMENTED** the same day
(session S106): the constant, its derivation comment, the remediation text, thirteen
`bin/tests.sh` couplings and the `.context-budget.json` note. **PHASE 2 IMPLEMENTED 2026-08-25 (session S109)** — the front-matter
compaction and, beyond the sketch, the header reserve turned into a named constant with two
executable assertions; see the S109 note in §6. **Phase 3 remains pending** and is a separate
session. §5.2's inventory was incomplete — see the S106 correction below it.
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

**IMPLEMENTED 2026-08-25 (S109).** What was done, and where it departed from this sketch:

- **The pointer blocks were 8, not 7.** Re-measured at Orient rather than inherited: **3,587 B =
  48.6%** of a **7,361 B** front matter, against this section's 3,132 B / 45% / 6,913 B. The drift
  is exactly one block at the ~447 B this section predicts, so the growth model is confirmed by its
  own error. Collapsed to one table: front matter **7,361 → 6,170 B (−16.2%)**, and the per-trim
  growth term **~447 → ~190 B**, which is the half that compounds.
- **Losslessness was proved, not asserted.** All 7 facts × 8 shards (count, first/last date, shard
  path, proof path, basename, generator version) re-parsed from the written artifact and compared
  against the pre-change blocks re-derived from `git show HEAD:HANDOFFS.md`; record total 92 = 92;
  parse completeness asserted (`rows parsed == row-shaped lines == source blocks`) so an empty
  match could not read as success; and a **tamper control** (one version string altered) confirmed
  the detector reports a mismatch.
- **The reserve got a name, and that is the part this sketch understated.** `HEADER_RESERVE_BYTES`
  did not exist — 8,000 B lived only in `bin/check-handoff`'s derivation comment, so the term this
  phase was told to "re-derive" had nothing to re-derive it *in*. Now `CEILING_BYTES = 65536`,
  `HEADER_RESERVE_BYTES = 7168`, `RETENTION_FLOOR = 3` sit beside the per-record constant.
  **7 KiB** is below the old 8,000 (so the saving is banked, per §4.3) and above the measured
  6,170 B with ~5 trims of headroom.
- **Two assertions, not one — and A1 alone would have caught nothing.** `bin/tests.sh` **Test 39**:
  **A1** is the fit this section asked for (`3 × 12,288 + 7,168 = 44,032 ≤ 65,536`); **A2** holds
  the **live** front matter under the reserve. The front matter had already crept to **92.0%** of a
  reserve nothing checked, two trims from a silent breach — and every byte of that creep satisfies
  A1. A2 was observed **RED two independent ways** (reserve lowered under the front matter, with A1
  still green; and front matter grown ~1,500 B with the reserve intact), then restored.
- **The fit assertion is a TEST, never a module-scope `assert`** — decided at claim, not
  discovered. A module-scope assert runs at import, so a mutant violating it dies with a traceback
  before the code under test executes and is scored killed by the crash rather than by behaviour.
- **`RECORD_BUDGET_BYTES` is unchanged at 12,288**, as §4.3 requires.
- **Verification:** `bin/tests.sh` **286 passed / 1 failed / 0 skipped** against a **279/1/0**
  control, row-for-row diffed — **7 new rows (Test 39), 0 status flips, 0 regressions**; the 3
  rows whose text changed are the same assertions carrying a derived count this session's own
  claim moved (`**Model:**` 8→9, receipts 4→5), PASS on both sides. The sole failure is Test 9's
  standing `--source=github` 404. All **16** shipped `.verify.sh` proofs unchanged from control
  (12 OK / 4 FAIL — BL-36's four). `check-links` 88/22, `check-handoff`, `--all`,
  `check-learnings` OK. `context_budget.py`: no file over ceiling.

**SCOPE COLLISION FOUND IN THIS PLAN, recorded rather than worked around.** §7 puts
`methodology_trim.py` and "anything distributed" out of scope, but the pointer blocks are
**generated** by `starter-kit/methodology_trim.py:935` (`build_pointer_block`) and placed by `:944`
(`insert_pointer`), and that file **is** distributed. So the compaction is a data edit that is in
scope, and it is durable only until the next trim appends a fresh ~447 B block in the old format.
An HTML comment in the front matter tells the next trimming session to fold it into the table.
Teaching the generator the compact format is an upstream change and was **not** taken here.

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

**MEASURED 2026-08-30 (S126) — the gate measurement, RUN. Recommendation: DO NOT REDUCE.**

**Method, and the verification heredoc above is not what produced these numbers.** Its split,
`rec.index('\n```\n', 3)`, is sound only if no receipt holds a second bare fence — which it never
checks, in a file that documents its own format. Probed: across 11 files every one of the **132**
receipts holds exactly one bare ` ``` ` line. The parse was then *asserted*, not trusted: `fenced +
prose == extent` on all 132; `front matter + Σ extents == wc -c` on every file; `Σ field bytes + 2
fence lines == fenced` on all 132. Baseline is **`41b27fb`**, the pre-claim tree, so S126's own stub
is outside its own population. **This phase's stated surface of *"111 receipts"* is stale — it is 132.**

**1. THE `Do` CLAUSE, ANSWERED: THE FENCED FIELDS DO NOT COMPRESS.** Deflate-9 ratio of the fenced
block, n=132, unit compressed/raw bytes: **0.484** (min 0.435, max 0.594). Size-matched controls cut
from this repo's own prose at the 9,116 B mean block size: `ITERATIVE_METHODOLOGY.md` **0.435**,
`starter-kit/SESSION_RUNNER.md` **0.448**, `README.md` **0.445**. A higher ratio is *less* redundancy,
so **receipts are measurably less redundant than the documentation this framework ships.** Named,
removable slack inside the six (cohort E, n=20): `**` emphasis **3.03%**, cross-record boilerplate
(8-word shingles shared with any other receipt) **2.41%**, within-record cross-field overlap
**0.00%**. Total identifiable ≈ **1–3%**, against the **16.7%** that 10,240 requires and the **33.3%**
that 8,192 requires. *(De-shouting recovers nothing: lowercase costs the same bytes.)*

**This is decisive because §4.2 made it the condition.** Its 8,192 row reads *"Revisit only after
measuring whether fields compress — see §6, Phase 3."* Measured: they do not. **The revisit does not
open.** Its 10,240 row already read *"cuts into fenced fields for the two largest recent receipts"* —
still true, `max(fenced)` in the current cohort is **10,827 B** (S117). Phase 3 adds no new permission
for either number; it closes the one door §4.2 left ajar.

**2. WHAT A REDUCTION WOULD BUY: ONE SESSION.** `HANDOFFS.md` at the baseline is 229,270 B with
**32,874 B** to `READ_REFUSE_BYTES` *(at `HEAD` after S126's claim it is 233,147 B / 28,997 B / 20
records — the projection is unchanged, since a stub becomes part of its own session's record)*.
Measured close-out-to-close-out growth **11,432 B/session** (n=7) → breach at **S128's close-out**.
10,240 → **S129**. 8,192 → **S130**. **Invariant across every utilization estimator from 89.2% to
100%.** ⚠ The record-extent and file-delta series agree to **0.1 B** because they are the *same*
measurement — each close-out appends one record and the front matter barely moves. That is not
corroboration, and an earlier draft of this block wrongly presented it as such.

**3. GROWTH IS MONOTONE ONLY UNDER THE STANDING REFUSAL TO TRIM — not structurally.** This file has
shrunk twice inside the current cohort (82,406 → 31,875 B at `9cf4ae0`; 66,614 → 44,468 B at
`9038e40`). Archiving is the only mechanism that removes bytes and it is presently refused
(`SRF 8.3447` vs `SRF_RED 1.00`; S112, S124, BL-52). **So a rate cut defers the date and never
resolves it — but that is a consequence of the refusal, not of the budget.**

**4. WHAT THE LAST CUT DID TO THE SIX: direction survives, magnitude and causation do not.** Cohorts
by *the constant in force at close-out* — S105's receipt was `status: complete` 45 minutes before
`6ebe84d`, so it belongs to the 18,432 regime. D (S98–S105, n=8) → E (S106–S125, n=20): the six
**−18.6%**, essays **−48.2%**; `next_steps` −27.8%, `what_was_done` −24.0%, `key_files` −18.6%,
`active_task` −12.2%, `gotchas` −2.0%. **But the confound is not cleared.** Cohort C (the last
pre-budget fortnight) is itself a **+36.2%** excursion over cohort B that began *six days before
`RECORD_BUDGET_BYTES` existed*; E sits **+2.7%** above the pooled 92-receipt pre-08-12 baseline and at
the **48th percentile** of all 132 per-record six-field values. The six returned to corpus normal from
a pre-budget excursion that was already receding inside D (D is −4.5% from C). **`check-handoff:638`'s
*"the six requirements survive unchanged"* is therefore UNVERIFIED, not falsified** — they moved, and
this design cannot separate the cut from the excursion's own decay.

**5. THE PLAN'S NAMED QUALITY DETECTOR SHOWS A SMOOTH DRIFT, NOT A STEP.** An 8-receipt rolling mean
of `predecessor_score` falls **8.25 → 7.75** across S103→S125 with **no discontinuity at either budget
event**. The longest run of 9s is S90–S97 (**eight**, pre-budget) and the corpus record is nine
(S60–S67); a two-run (S103, S104) *does* occur after the budget. Post-08-12 there are **five** 7s
(S88, S102, S106, S113, S124) and one 6 (S121). Scores grade the **predecessor**, so grouping them by
the scorer's cohort misattributes — S98's 8 grades a receipt written before the budget commit.
**The detector neither indicts nor exonerates the last cut. It supplies no evidence that a further one
is safe.**

**6. THE GATE'S POPULATION IS UNDER-DETERMINED, AND THE `Do` CLAUSE IS WHAT SETTLES IT.**
`max(fenced)` is **16,889 B** over all 132 (S38), **14,310 B** in D (S100), **10,827 B** in E (S117).
The all-132 reading would forbid the very 12,288 this plan's status line records as ratified, so it
cannot be the intended one. Nor does `bin/check-handoff:632-640` supply a cohort: its *"current fenced
fields run 10,920–13,019 B"* is **S103 and S104** (S102's 12,386 B between them; mean 12,108 B = this
plan's own *"fenced-field mean"*), written **by `6ebe84d` itself**, before a single 12,288-era receipt
existed. And a floor that forbids 10,240 contradicts §4.2, which rated it *viable* while saying
outright that it cuts into fenced fields — making this phase self-cancelling. **Settled from
provenance instead: §4.2 + the `Do` clause define the gate as a test — *does compression move the
floor down?* It does not (§1). So the floor stays where it is, and neither candidate becomes
available.**

**RECOMMENDATION — do not reduce `RECORD_BUDGET_BYTES`.** In order of strength: **(a)** the condition
§4.2 attached to 8,192 is measured and not met — the fields do not compress, by an order of magnitude
(1–3% available against 16.7% / 33.3% required); **(b)** 10,240 still cuts into fenced fields, exactly
as §4.2 said, since `max(fenced)` is 10,827 B; **(c)** the whole benefit available is **one session**
(S128 → S129), against a deadline that returns; **(d)** the six demonstrably moved across the last cut
and nothing here shows they were spared. **This phase's question — *"only if the operator wants a
harder stop"* — is answered: this lever cannot deliver one.**

**The one durable finding for a future cut, so it is not re-derived — and its population matters.**
Over **cohort E (n=20)** `runtime_smoke` is the largest single field at **1,990 B/receipt, 21.0%** of
field bytes, and it is **not one of the six** (the six 75.9%; remainder 3.1%). Over **all 132** the
picture inverts: the six are **80.5%**, `runtime_smoke` is **14.4%** and ranks **fourth**, behind
`what_was_done` (2,161 B, 23.7%). It is the only substantial non-six mass either way, so it is where a
cut should land — but at **95.7%** utilization a *sub-budget* reallocates rather than reduces. Only
the total budget moves the rate.

**Verification, reported as it actually returned.** `python3 bin/check-handoff --all` on the working
tree: **FAIL, exit 1, 20 receipts** — the sole finding is S126's own `status: pending` stub. Against
the measured tree (`git show 41b27fb:HANDOFFS.md`): **OK, exit 0, 19 receipts.** `bash bin/tests.sh`
deliberately not re-run: this section scopes it *"only if a constant actually changes"*, and none did.
**No reformatting trial was run**, so the stated purpose of the `--all` command here — *"population
intact after any reformatting trial"* — was not exercised. Nothing in the tree was modified by the
measurement; it reads `41b27fb` through `git show`.

**Surface, and what it cannot enforce.** The committed ledger plus all ten shards — 132 receipts. It
cannot enforce handoff *quality*: §5 is observational with no control arm, and the scores are assigned
by successors, so a stricter scoring culture would produce the same curve. It cannot separate the
budget from the pre-budget excursion (§4). And the compression measurement (§1) bounds *lossless*
redundancy — it cannot rule out that a human editor could say the same things in fewer words.

**Adversarial review.** Six independent read-only lenses were run against a frozen draft of this
block; **all six returned PARTIALLY_REFUTED**, and their corrections are incorporated above. They
overturned the cohort boundary, the utilization claim, the −24.1% magnitude, the confound's sign, the
"sharp step" in §5, the citation in §6, an invented 11,264 B candidate, a false `check-handoff` result,
and a cross-check that was self-confirmation. **The recommendation is the only part of the first draft
that survived unchanged.**

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
