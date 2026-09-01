# The `SRF_RED` refusal of the `HANDOFFS.md` trim — adjudicated

**Session:** S124 (2026-08-29), fork side. **Deliverable:** this document.
**Predecessor's brief:** S123 `next_steps` **(c)** — *"`HANDOFFS.md` is past the trimmer's budget and
the trigger fires… that trim is the obvious next deliverable; run `--check` rather than trusting
these numbers."*

Both were run at the claim. `--check` **FIRES**. The `--cut 3` dry run **REFUSES** — exit 2,
`SRF_RED`. So the assigned deliverable did not exist as described, and the refusal became the
deliverable.

**Verdict up front: the refusal STANDS, the trim must not be forced, and the reason is not the one
the tool gives.** This question was already adjudicated for this exact file, on measurement, twelve
sessions ago; a standing instruction to honour it is live in the ledger; and the metric the tool
refuses on is, in this instance, outside its own domain of validity. Separately, the adjudication
that settles it **expires in ~4.6 sessions by its own stated terms**, and the remedy it named has
never been built.

**Nothing was trimmed, forced, or written to `HANDOFFS.md` by this session** beyond its Phase 1B
claim stub and its close-out receipt.

---

## 1. The finding under adjudication

`starter-kit/methodology_trim.py` reports a Sawtooth Recovery Fraction (SRF) against two boundaries
and refuses on one of them:

```
[TRIGGER_BYTES] 205,704 B against a 196,608 B budget
[SRF] SRF 7.2806 vs the most recent archive 9038e40; 0.4550 vs H3's largest-drop boundary a46f2f9
      — the two boundaries differ by 16.00x on the same file
[SRF_RED] SRF 7.2806 (RED) against 9038e40. The last archive has been entirely given back;
      archiving again resets the LEVEL and not the RATE — see plan §3.3, whose action rule for RED
      is "do not archive again". Re-run with --force to archive anyway.
```

The tool prints **both a trigger that fires and a refusal to act on it**, in one report. That is the
surface conflict. The boundary spread — 16× on one file — is the surface question.

**Both are red herrings.** They are answered in §3, after the two findings that actually decide it.

---

## 2. Why the refusal stands — three independent reasons, any one sufficient

### 2.1 This exact question was adjudicated for this exact file, on measurement, and the answer was recorded

`docs/planning/BACKLOG-DETAIL.md:1474` — **BL-52's third addendum (S112, Phase B)**, verbatim:

> **⚠ THIRD ADDENDUM (S112, Phase B): BL-52 IS NOW ADJUDICATED FOR THIS REPO'S `HANDOFFS.md`, ON
> MEASUREMENT, AND THE ANSWER IS THAT THE TRIM BUYS NOTHING.** The occasion was mundane — a trim was
> due as close-out housekeeping and `methodology_trim.py` refused it (`[SRF_RED]` 1.1198…). The
> session was about to `--force` past it. **It had not asked BL-52's own question first.**

It then measured, rather than modelled, what a whole-file read delivers, and concluded:

> **So the tool's refusal was right, and right for a STRONGER reason than the one it gave.** It
> diagnosed a level remedy applied to a rate problem. The measurement adds: the level is not costing
> anything yet.
>
> The remedy between here and there is the **record budget**, not archiving.

S113 turned that into a standing instruction, `HANDOFFS.md:433-447`, `next_steps` **(d)**, verbatim:

> **`HANDOFFS.md` IS OVER BOTH ITS CEILINGS BY ADJUDICATION, NOT NEGLECT** (BL-52 third addendum) —
> **do not trim it on sight**; `context_budget.py` exits **2** for that reason and that is expected.

This is an **attributed** constraint with a **dated warrant** and a **named record** — the three
things [Learning #48](../../starter-kit/FRAMEWORK_LEARNINGS.md) and `CLAUDE.md`'s own rule require
before a blocker may be honoured. It is not the unattributed kind this repository has been burned by.
Its other edge — *does it still hold?* — is §4.

### 2.2 SRF's two operands come from opposite sides of a deliberate 3.00× policy change

This is the finding that says the number itself is invalid here, and it appears nowhere on record.

```sh
git merge-base --is-ancestor 9038e40 0afe9d6 && echo "trim PREDATES the raise"   # -> it does
git log -1 --format='%h %ad %s' --date=short 9038e40   # 2026-08-26 docs(trim): archive 2 receipts
git log -S'DEFAULT_BUDGET_BYTES = 192 * 1024' --format='%h %ad %s' --date=short \
    -- starter-kit/methodology_trim.py                 # 0afe9d6 2026-08-26 Phase C2
```

- **Denominator** — 22,146 B, the amount `9038e40` removed. That trim fired when the file reached
  ~66,614 B, because the trigger was then **65,536 B**.
- **Numerator** — 164,184 B of regrowth since. That regrowth was *permitted* because Phase C2
  (`0afe9d6`, operator decision) raised the trigger to **196,608 B**.

SRF divides the second by the first: **a 3.00× more permissive ceiling on the numerator than on the
denominator.** H3 exists to distinguish *"my ledger is big"* from *"my ledger is big **again, on
schedule, for the same reason**"* (`framework-context-cost-plan.md:263-264`). A deliberate 3× ceiling
change is not "the same reason" — the file gave back more than the last archive removed **because the
operator decided to let it**.

H3 already documents one limit — *"SRF is undefined before an adopter's first archive"* — and the
trimmer honours it by abstaining (`:978-980`). **It needs a second limit of exactly the same kind:
SRF is undefined across a trigger change.** Until the file has been archived once under the current
trigger, the denominator belongs to a policy that no longer exists.

This also disposes of the "decaying mechanism" reading. The removals shrank —
171,441 / 169,853 / 369,255 / 214,539 / 103,014 / 68,955 / 56,208 / 52,902 / 50,531 / **22,146** —
because the *number of records removed* collapsed (19 → 16 → 30 → 25 → 8 → 4 → 3 → 3 → 3 → **2**)
under a tight trigger that fired constantly. That is a trigger set low, not a mechanism decaying.

### 2.3 Executed, the trim does not clear the ceiling — and every trim in this file's history is net-additive

A real trim was executed in a scratchpad clone and measured, not predicted. It writes **exactly four
files** and never stages or commits:

| file | before | after |
|---|--:|--:|
| `HANDOFFS.md` | 208,652 B | **91,796 B** |
| new shard | — | 117,861 B |
| new `.verify.sh` | — | 16,011 B |
| `CHANGELOG.md` | 180,559 B | 181,331 B |

- **It does not clear the ceiling.** 91,796 B is still **26,260 B over** the 65,536 B ceiling, and
  `context_budget.py` still exits 2. It satisfies only the trimmer's own hysteresis stop (98,304 B).
- **It is net-additive**: relieves 116,856 B, adds 134,644 B → **net +17,788 B, a 1.152× growth/relief
  ratio.**

That is not an accident of this one run. Across all ten archive events, adjusted for the two commits
that bundle unrelated work (`c0e6944`, `a46f2f9`):

> trim-attributable relief **1,304,337 B** against trim-attributable additions **1,448,576 B** =
> **net +144,239 B (1.111×)**. Every single trim is net-additive; the smallest is +4,787 B.

The archive those ten trims built now holds **1,437,228 B** on disk — *more than the 1,304,337 B of
cumulative relief it bought.* And `docs/archive/` is inside **no ceiling anywhere**.

The honest statement of what a trim does: it **relocates** bytes out of a read-mandated file into an
unmeasured one, at a near-fixed ~17.8 KB toll. That is a real service — resident cost is what matters,
not repo size — but it is a transfer, not a saving, and it must not be described as freeing anything.

---

## 3. Where the confusion came from — and why the boundary spread is a red herring

**The boundary choice is documented, deliberate, and correctly labelled.** Settled from provenance
rather than by reading the sentence harder:

- **H3, the originating rule**, lives at `docs/planning/framework-context-cost-plan.md:246-247` —
  **not** in `ledger-trimmer-design.md`, whose own §3.3 is about `BACKLOG.md` and contains zero SRF
  text. H3 says *"around the largest single size drop in the file's history."* Its text has never
  been amended (`git log -S 'largest single size drop'` → exactly one commit).
- **The design departed from it on purpose**, `ledger-trimmer-design.md:613-634`: *"pinning it
  differently is ADDING POLICY — labelled here as such… use the **most recent archive** for the §5.3
  refusal — because the refusal acts on current cadence, and the largest-drop boundary recedes
  further into the past with every archive, diluting exactly the signal the refusal exists to
  catch… **H3 itself is unchanged.**"*
- **The tool says so in its own output** (`:1876-1879`): *"a policy addition on top of H3 … labelled
  as an addition, not dressed as a reading."*

So the 16× spread is not drift, and **flipping the boundary is not the remedy**. It is a two-line
edit whose test blast radius is **zero — but only because the choice is untested**: 123/123 trim
tests and 321 dashboard tests return byte-identical results before and after. A choice no test can
kill is a choice no suite defends. Flipping it would also make the tool's own `[SRF]` report string
assert a falsehood, and `methodology_trim.py` **is adopter-facing** (`bin/_manifest.py` SOURCE column,
`TRACKED`), so any edit reaches every adopter at their next `bin/sync` and needs the operator's
go-ahead.

**The actual defect in the record is that a settled question was re-opened without citing its
settlement.** S123's `next_steps` (c) called the trim *"the obvious next deliverable"* and cited
neither BL-52's third addendum nor S113's standing instruction. Both are one grep away
(`grep -rn 'do not trim it on sight' HANDOFFS.md`). This document's own claim stub inherited that
framing and spent its first hours costing a remedy the record had already declined — which is the
same shape as the mistake, one session later.

---

## 4. What the adjudication does *not* settle — and it expires in ~4.6 sessions

BL-52's third addendum bounded itself explicitly, and named its own expiry trigger:

> It settles **this file, at this size, with these record sizes** — the middle regime, between the
> 25,000-token cap and the 256 KiB refusal…
> **The threshold that will actually bite is `READ_REFUSE_BYTES` = 262,144**, where the front matter
> itself stops being delivered. From 77,265 B at ~12,288 B per close-out that is **~16 sessions**.

**That projection is being confirmed almost exactly.** S112 measured 77,265 B; the file is now
208,652 B, twelve close-outs later — 10,949 B/session actual against its 12,288 B estimate:

| | |
|---|--:|
| S112's prediction | ~16 sessions |
| elapsed S112 → S124 | 12 sessions |
| remaining at the measured rate | **4.6 sessions** |
| **total** | **16.6 sessions** |

`READ_REFUSE_BYTES` is not truncation. Per `starter-kit/methodology_trim.py:130-135`: *"past it a
default Read is refused outright with ZERO content… Past this one nothing arrives at all, front
matter included."* A bounded `offset`/`limit` span still returns content; an unbounded read returns
none.

**Stated in tokens, which is the unit S121's adjudication ruled this capacity must carry** — a byte
ceiling is tokens × density, and density rots silently:

| | bytes | tokens @ 2.3648 B/tok |
|---|--:|--:|
| ceiling | 65,536 | **25,000** |
| now | 208,652 | **88,232** |
| hard refusal | 262,144 | **110,852** |
| **headroom** | **53,492** | **22,620** |
| per session | 11,727 | **4,959** |

**~22,620 tokens, ~4.6 sessions.** And the failure mode has already occurred once in this repo, on
the very tier that is supposed to be the escape hatch: `docs/archive/HANDOFFS-through-2026-08-09.md`
is **382,071 B**, past the refusal, unreadable in one read.

**The remedy BL-52 named — the record budget — has never been built.** `RECORD_BUDGET_BYTES = 12288`
(`bin/check-handoff:665`) is already fully complied with: all 18 live records are ≤ 12,288 B, the
maximum is *exactly* 12,288, and nine of eighteen sit within 0.06% of it. **The cap is functioning as
a quota, not a limit.** The ledger's 200 KB is eighteen near-maximal receipts, not oversized ones, so
lowering the cap is the only lever that changes the rate. And the mechanism that would enforce it is
**canonical-only** — `bin/check-handoff` is absent from `bin/_manifest.py`'s SOURCE column, so no
adopter has ever received it.

---

## 5. An independent defect found while locating the insertion point

Unrelated to the trim, free to fix, and **currently red**.

`HANDOFFS.md:73-101` holds **2,678 B** of S119's prose — its Phase 3A predecessor evaluation and
Phase 3B self-assessment — stranded *above the first receipt*, detached from S119's own block at
line 217.

**Cause: an insertion-point collision, not a trim.** S119's close-out (`2b4dcc6`) replaced its claim
stub's HTML comment — which sat *above* the fence — with its full prose. Every session since prepends
at the first line-anchored `` ```handoff ``, which is *below* that prose. The result is
self-perpetuating: across all ten commits since, the first fence has been at line 103 and the prose
at line 73, and the front matter has measured **exactly 9,041 B** every time.

**Live consequence, established by running the suite, not by predicting it** — `bash bin/tests.sh`,
exit code read bare on the next line: `TESTS_EXIT=1`, **286 passed / 3 failed / 0 skipped**.

```
FAIL: A2 truth VIOLATED: live front matter 9041 B exceeds the 7168 B header reserve by 1873
```

Test 39 measures the front matter as everything above the first fence, so the stranded prose is
inside it. Without it the front matter is 6,362 B and A2 holds. Attributing all three failures:

| failure | onset | cause |
|---|---|---|
| Test 39 `A2 truth VIOLATED` | `2b4dcc6` (S119, 2026-08-27) | the stranded prose — red for **six sessions** |
| Test 18 (dashboard ×2) | `ccfbe1c` (S123's claim) | file crossed 196,608 B; the advisory switched to the hard-refusal branch and severity escalated, while the assertions stay pinned to the pre-crossing text |
| Test 9 github dry-run | long-standing | upstream has not merged `FRAMEWORK_LEARNINGS.md` / `methodology_trim.py` |

S121 and S122 both recorded **287 passed / 2 failed**. The suite went **287/2 → 286/3** the moment
S123's claim stub pushed the ledger past the trim trigger — the same commit whose message records
*"the trimmer's trigger now FIRES"*. It measured the crossing and did not run the suite.

**Three things this defect is not**, each checked rather than assumed:

1. **Nothing is lost.** S119's prose exists exactly once in the tree; the receipt population
   reconciles at 18 live + 94 archived + 19 in `HANDOFFS-archive.md` = 131.
2. **No losslessness proof passed over it.** The orphan post-dates the last trim by a day, so no
   proof has ever run over it. And the proof's `zones()` partitions *every* line into three zones —
   the orphan lands in the front-matter zone, which L2 *does* assert on. The population was never
   "records only".
3. **No trim can remove it.** L2 pins the front matter, so a compliant trim can never archive it.
   It will be copied forward indefinitely.

A **second, distinct misalignment** exists in the same scan: record S119's span carries S118's prose
and S118's carries S117's, while S117, S116 and S107 carry no trailing prose at all. Every other live
record is correctly paired. Both defects are invisible to `bin/check-handoff`, which exits **0** in
default and `--all` modes.

---

## 6. The options, costed

None of these is being executed by this session.

### (i) `--force` the trim now — **REFUTED**
Contradicts a standing adjudication and instruction. `--force` is a one-guard flag (`opts.force`
appears exactly once in 2,181 lines, at `:1895`) and would bypass only `SRF_RED`. It buys **13-14
sessions** of a number going down, costs **+17,788 B net**, does **not** clear the ceiling
(91,796 B), imposes a manual step — the front matter's own HTML comment orders a future session to
fold the generated 449 B pointer block into the table by hand — and would archive S108/S107, which
are already outside the delivered prefix. This is precisely the move S112 stopped and BL-52 refuted.

### (ii) Flip the SRF boundary to H3's largest-drop — **WEAK, and it treats the symptom**
Two-line edit, zero test blast radius *because the choice is untested*. Would turn the refusal GREEN
(0.4630) and let the trim proceed with no `--force` — i.e. it delivers option (i) while hiding that
it did. It also leaves the tool's own report string asserting a falsehood, and it is **adopter-facing**.
The real objection to the current boundary is §2.2, which flipping does not address.

### (iii) Do nothing — **REFUTED by the deadline, not by the ceiling**
Breaks nothing mechanically today: there is no CI, the installed pre-commit hook has zero size logic,
and `context_budget.py --precommit` is not wired in. But it runs out in ~4.6 sessions, and the
archive tier already contains one file past the refusal.

### (iv) Raise the ceiling — **LAST BY DOCTRINE**
`max_bytes` 65,536 → ≥208,652 (3.18×) and `max_tokens` 25,000 → ≥88,232 (3.53×).
`context_budget.py`'s own remediation list ranks *"Raise the ceiling"* fifth of five, *"last for a
reason"*, and the tool deliberately ships no `--force` so the decision must land as a reviewable diff.

### (v) Cut the rate — **the remedy the record already prescribes, and it has never been built**
H3's RED action rule (`framework-context-cost-plan.md:265-267`): *"RED: **do not archive again**; the
next deliverable is a rate cut, not another reset."* BL-52: *"the remedy between here and there is
the record budget, not archiving."* Precedent exists — `bin/check-learnings` enforces
`ROW_BUDGET_BYTES = 1500` over **every** row, not just the one being written, whereas
`check_record_budget` tests only the newest record and only while it differs from `HEAD`. The
prerequisite measurement in `record-budget-reduction-plan.md` Phase 3 has never been run.

### (vi) Repair the stranded prose — **INDEPENDENT, cheap, and it turns a red assertion green**
Relocate 2,678 B from above the first fence to below S119's block. Restores A2
(9,041 → 6,362 B against a 7,168 B reserve). Does not depend on any trim decision. Note the trap:
`check_record_budget` inspects only `extents[0]`, so a repair that grows S119's record past 12,288 B
would breach a budget no instrument would report.

### (vii) Answer the operator decisions the plan is blocked on — **OUTRANKS ALL OF THE ABOVE**
`docs/planning/file-management-system-plan.md` §6 registers six operator decisions. **D4** is this
question — *"Is 'undeliverable in one Read' a fault or an accepted operating state?"* — and **D1**,
*"What is the framework's target cost per session?"*, is recorded as not derivable from measurement,
under a heading stating Phase 1 does not start until it is answered. Every option above is a
different answer to D1 with the question left implicit.

---

## 7. Recommendation — two tiers, two different owners

### Tier 1 — settled by measurement; nothing here is a preference

1. **Do not trim, and do not `--force`.** The standing adjudication holds on its own terms today.
2. **Record that SRF is undefined across a trigger change** (§2.2), as a second known limit beside
   H3's existing one. This is the durable framework finding. Note that the channel matters: a
   Learning row has zero inbound citations and a handoff gotcha expires in one session, whereas the
   constant's own comment block is read by anyone who re-opens the number.
3. **Repair the stranded prose** (§5, option vi) and re-run `bin/tests.sh` to watch 286/3 become
   287/2. Independent of every trim question.
4. **Correct the record** (§8).

### Tier 2 — the operator's, and deliberately not ranked here

5. **D1 and D4** (§6 option vii). Not agent-decidable, and every remaining choice is downstream of
   them.
6. **Which remedy to fund before the ~4.6-session deadline**, given that Tier 1 forbids the reset and
   the prescribed rate cut has never been built. The honest statement of the position: *the record
   forbids the only remedy that is ready, and the remedy it prescribes does not exist yet.* That is a
   funding decision, not a measurement.

**The one thing that must not happen** is a session arriving at the deadline, finding the refusal in
its way, and forcing past it because nothing else was ready — which is exactly what S112 caught, and
what S123's handoff had set up to happen again.

---

## 8. The record to repair

| where | what is wrong | correct |
|---|---|---|
| `CHANGELOG.md` S124 claim | attributed H3 §3.3 to `ledger-trimmer-design.md` | corrected in `5637383`; H3 is `framework-context-cost-plan.md:246-247` |
| `HANDOFFS.md` front matter | states the file holds **4** receipts | **18** (`grep -c '^```handoff'`); only a trim regenerates it |
| `HANDOFFS.md` front matter | *"`bin/check-handoff` validates only the newest receipt"* | false — default mode runs four scopes, two traversing every receipt |
| `HANDOFFS.md:702` (S109) | cites the regenerating regex at `methodology_trim.py:222` | it is `:338` |
| `HANDOFFS.md:73-101` | S119's prose stranded above the first fence | §5 |
| `docs/archive/HANDOFFS-through-2026-08-09.md` | 382,071 B — past the hard refusal | the escape hatch is itself unreadable in one read |

---

## 9. Reproduction

```sh
# the refusal, and its two boundaries — run bare, read $? on the NEXT line
python3 starter-kit/methodology_trim.py --check --file HANDOFFS.md   # exit 1, trigger FIRES
python3 starter-kit/methodology_trim.py --file HANDOFFS.md --cut 3   # exit 2, SRF_RED

# 2.2 — the operands straddle the trigger raise
git merge-base --is-ancestor 9038e40 0afe9d6 && echo "trim predates the 64->192 KiB raise"
#   denominator 22,146 B removed under a 65,536 B trigger
#   numerator  164,184 B regrown  under a 196,608 B trigger  => 3.00x more permissive

# 2.3 — every trim is net-additive (drop in HANDOFFS.md vs bytes added elsewhere, per commit)
for s in 7a71df0 c0e6944 a46f2f9 721853b 17753d9 7fee8bd 5ec1bd2 470cfd4 9cf4ae0 9038e40; do
  echo "$s $(( $(git cat-file -s $s^:HANDOFFS.md) - $(git cat-file -s $s:HANDOFFS.md) ))"; done

# 4 — the deadline, in the unit S121 ruled this must carry
#   208,652 B / 2.3648 = 88,232 tok ; refusal 262,144 B = 110,852 tok
#   headroom 22,620 tok / 4,959 tok per session = 4.6 sessions

# 5 — the stranded prose and the red assertion
python3 -c "import re;t=open('HANDOFFS.md').read();m=re.search(r'(?m)^\`\`\`handoff$',t);print(len(t[:m.start()].encode()))"
#   -> 9041, against HEADER_RESERVE_BYTES = 7168 (bin/check-handoff:663)
bash bin/tests.sh   # TESTS_EXIT=1 -- 286 passed / 3 failed / 0 skipped

# the standing instruction and its warrant
grep -rn 'do not trim it on sight' HANDOFFS.md
sed -n '1474,1524p' docs/planning/BACKLOG-DETAIL.md
```

---

## 10. What this document does *not* establish

- **It does not re-verify BL-52's own read-delivery measurements.** It cites them and confirms their
  *projection* against today's size; it did not re-run the over-cap error-path probes that produced
  the 4-and-5-receipt prefix table.
- **It does not establish that the operator ratified the most-recent-boundary policy addition.**
  `ledger-trimmer-design.md:634` required that adoption be *"an explicit call in S37's close-out"*.
  No such call was found, and the session/queue-item axes both read "S36/S37", so the search is not
  conclusive either way. The boundary is documented and deliberate; whether it was *ratified* is
  open.
- **It did not run the trim in this repository.** The four-file write inventory and the
  91,796 B result come from an execution in a scratchpad clone.
- **It does not cost the rate cut.** `record-budget-reduction-plan.md` Phase 3's gate measurement has
  not been run here; a probe over the full 131-record population suggests the fenced-field maximum is
  **16,889 B**, above today's cap, which would make the gate as literally written block 10,240, 8,192
  *and* the status quo. That needs its own session.
- **It changes no constant, ships no code, and takes no outward-facing action.**

---

## 11. S132 (2026-08-31) — the refusal is structurally unsatisfiable, and both ledgers were trimmed

**S124 adjudicated the refusal for `HANDOFFS.md` and was right.** This section does not disturb that.
It records three things S124 could not have known: an impossibility proof about the rule itself, a
regime this document's governing authority explicitly excluded, and a claim S132 published and
retracted.

### 11.1 `SRF_RED` cannot be satisfied by any steady-state retention policy — a proof, not a complaint

`SRF_RED = 1.00` (`:203`) and the refusal votes with the **most recent** archive
(`:1895`, `trigger.srf[0] >= SRF_RED`), where `srf(pre, post) = (size - post) / (pre - post)` —
that is, **regrowth ÷ relief** (`:982`).

Let a policy trim at a high-water mark **X** back to a low-water mark **Y**. Relief is `X − Y`. The
trigger next fires when the file returns to **X**, so regrowth is also `X − Y`. Therefore

> **SRF = (X − Y) / (X − Y) = 1.0000 exactly — and the test is `>=`.**

**Every on-schedule trim under any retention policy is refused, for any X, any Y, and any file.**
The rule is satisfiable only by trimming *late* — letting the ledger overshoot X so the prior relief
exceeds the next regrowth. It therefore **rewards overshoot and punishes maintenance on time**, which
is precisely how `CHANGELOG.md` reached 283,078 B. Executed here: this session's cut gives SRF
**0.0149** today and **≈1.07** at the next trigger — but a trim *then*, back to the same level, makes
the trigger after that **exactly 1.0000**. The deadlock is two cycles away, by construction.

**H3 as written does not have this defect.** H3 says *"the largest single size drop"*. Against that
boundary a steady-state policy stays green forever, because the largest relief is a maximum and
regrowth is bounded by `X − Y`. The tool **computes** that number (`trigger.srf_largest`), **prints**
it in every report, and **never votes with it** — and says so in its own output: *"the refusal below
uses the MOST RECENT one, which is a policy addition on top of H3 … labelled as an addition, not
dressed as a reading."* This is the *measured-but-never-voted* shape: the evidence is produced and
discarded at the decision.

**What is new here, stated against §6 (ii) so it is not read as a re-proposal.** §6 (ii) offered
*flipping the boundary* as a remedy and rated it **WEAK**, on the ground that it *"delivers option (i)
while hiding that it did"*. **That objection stands and this section does not lift it.** What is new
is not the remedy but the **impossibility**: §6 (ii) treated the boundary choice as a judgement call
with a symptom attached; the arithmetic above shows the current choice makes the rule *unsatisfiable
in principle* by the very instrument the refusal text tells you to build instead
(*"the next deliverable is a rate cut"*). §10's open question — whether the most-recent boundary was
ever **ratified** — becomes materially more important as a result. **No constant was changed here.**

### 11.2 Why `CHANGELOG.md` was trimmed anyway, and on whose warrant

**Not on this session's judgement.** BL-52's third addendum — the authority behind the standing
*"do not trim it on sight"* — **self-limits in its own words**:

> *"It settles **this file, at this size, with these record sizes** — the middle regime, between the
> 25,000-token cap and the 256 KiB refusal. It does **not** settle the general question, and it says
> nothing about **a repo well past the refusal, where a cut back under it turns nothing into
> something**."*

`CHANGELOG.md` was at **283,078 B**, past `READ_REFUSE_BYTES` = 262,144. Verified **empirically, not
from the constant**: a default `Read` returned `File content (274.8KB) exceeds maximum allowed size
(256KB)` — zero content, front matter included. That is the excluded regime, and the same addendum
names it as *"the threshold that will actually bite"*.

**The depth is the ratified one, not a new number.** No `--cut` was passed; `choose_cut` applied
`CLASS_A_STOP_BYTES = 98,304` — *"cut back to at or under this"* — which Phase C2 (S116) set **by
operator decision** and which `methodology_trim.py:142-153` denominates against the **refusal**, not
the one-read cap, because *"these ledgers are newest-on-top and delivery is an ORDERED PREFIX, so
truncation removes the OLDEST records, which is the end nothing was reading."* 58 of 79 records
archived; **283,078 → 98,037 B**. `--force` was required (SRF 7.7908) and **operator-approved for
this file, in this regime, on this evidence** — it is not a precedent for any other trim.

**`HANDOFFS.md` needed no force** (SRF 0.2315) and was cut to the S127 retention of **four** —
91,588 → 34,721 B, then 34,462 B after the pointer-block fold.

### 11.3 What the trim achieved, and what it did not — measured, with the shortfall stated first

**It did NOT make the ledger deliverable in one read, and no one should record that it did.** A
default `Read` now **succeeds** but returns a banner:

> `[Truncated: PARTIAL view — … showing lines 1-667 of 1276 total (40592 tokens, cap 25000) …]`

So the file went from **zero content** to **the front matter plus the newest ~52%, announced**. That
is the graceful, oldest-first degradation Phase C2 ratified as *not a fault* — and this measurement
is the first direct confirmation that its premise holds on this file. The one-read cap was **not**
the target; had it been, the cut would have had to reach ~9 entries, which would have archived the
retention policy's own warrant (§11.5).

**Two second-order effects, both predicted before the run and both confirmed after:**

- **`context_budget.py` moved `HANDOFFS.md` from `over` to `warn`, and that is correct behaviour.**
  Under ceiling, the density-drift check unmasks: *"density 2.3648 B/token was measured at 186,617 B;
  the file is now 34,462 B (82% drift). The token figure above is provisional."* **`measured_bytes`
  was deliberately NOT bumped.** It records the size at which the density was measured, not the
  file's size; raising it without re-deriving the density would write a false provenance record and
  silence the check exactly where it is designed to speak. The honest remedy — a per-file
  re-measurement — has no instrument here: `--calibrate` fits one global constant against `CLAUDE.md`.
- **`bin/model-report` lost most of its primary structured source, silently and greenly.**
  `**Model:**` bullets: **43 live before → 8 live after**, 238 now in shards. `bin/tests.sh` Test 30's
  real-file arm passes on **one** bullet, so an 81% loss is invisible to it. The repo has already
  fixed this exact shape once — Test 29 was re-scoped to glob `docs/archive/CHANGELOG-*.md` because
  *"a correct, operator-directed archive turned this test red while nothing had eroded"* — and the
  precedent was never generalised to the tool the test guards. **This is a real cost of the trim,
  not a hypothetical, and it is not repaired here.**

### 11.4 A claim S132 published in its own claim entry and retracts here

S132's Phase 1B claim states: ***"The ledger every Phase 0 must reconcile against cannot be
opened."*** **The operative half is false.** `starter-kit/SESSION_RUNNER.md` Phase 0 step 6 is
**frontier-based**: it runs `git log -1 --format=%H -- CHANGELOG.md` and lists
`<frontier>..HEAD`. **That reads git history, not the file** — the correction is already recorded at
`tools/methodology_dashboard.py:329-333`, from BL-52's second addendum, and S132 reproduced the error
anyway. Reconcile was never blocked.

**What the refusal actually cost is the front matter** — 14,295 B carrying the archive index, the
published audit grep, the trim-trigger rule and the retention doctrine, none of which arrived. That
is a smaller claim than the one made, and it is still sufficient warrant for the cut: it is the
half of the file a trimming session reads *to decide whether to trim*.

### 11.5 What is now owed — ordered, and none of it done here

1. **A per-entry budget for `CHANGELOG.md`.** This is the *rate* fix BL-52 named (*"the record
   budget, not archiving"*) and the one `SRF_RED`'s own text asks for. The repo has the pattern twice
   — `RECORD_BUDGET_BYTES = 12,288` (`bin/check-handoff:665`), `ROW_BUDGET_BYTES = 1,500`
   (`bin/check-learnings:104`) — and **no `CHANGELOG` analogue exists**. Mean entry: 3,402 B.
2. **`bin/model-report` must glob the shards**, as Test 29 already does. Until then every trim silently
   guts its aggregate and no test says so.
3. **`bin/tests.sh` L1b/L2b name only `HANDOFFS-archive.md`**, so the eleven `HANDOFFS-through-*.md`
   shards are checked by nothing; each trim narrows the asserted population and the greens get cheaper.
4. **The retention policy's warrant is a dangling reference.** `HANDOFFS.md` says the warrant *"is in
   that session's `CHANGELOG.md` entry"* with **no sha and no shard name**. Those entries survived
   this cut with three entries of margin; the next cut takes them. Give it a sha.
5. **`HANDOFFS.md`'s stated N=4 warrant rests on the retired axis** — *"under the 56,750 B one-read
   cap"*, a detector floor, the same substitution S131 retracted a claim for. The policy stands as an
   operator decision; **a later session must not re-derive its depth from that sentence.**
6. **Out-of-repo citation rot, which no checker here can see.** 15 bare `CHANGELOG.md:<line>` /
   `HANDOFFS.md:<line>` anchors live in the operator's cross-session memory; at least two were already
   stale before this session, and this trim invalidates more.
