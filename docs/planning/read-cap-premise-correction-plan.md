# Correcting the Read-Cap Premise — Plan

**Status:** **RATIFIED by the operator at S111 (2026-08-26), A → B → C as three separate sessions. PHASE A IS SHIPPED** (S111, commits `84abc60` / `86037bd` / `85a2158`); **Phases B and C are not started.** §5.4's open question was settled at the same time: *leave the design and audit records, annotate `ledger-trimmer-design.md` only* — done. Phase A also raised **BL-52** and settled **dragon 8**; see §11. Nothing outside Phase A is implemented. Every repair
named below is a *proposal* (`SESSION_RUNNER.md` FM #18/#19: the plan is the deliverable).
**Author:** S110 (2026-08-26), at claim commit `8decf71`.
**Origin:** the operator handed over `../model_project_constructor/docs/planning/ledger-budgets-review.md`
(that repo's S248, same day), which found its own trim trigger's stated rationale false by
measurement. That rationale is not only theirs — **this repository authors and distributes it.**
**Scope:** fork-side preparation only. The carriers are **distributed**, so the fix lands upstream
and batches with BL-46(2)/47/48/49 into one pull request. **No outward-facing action** is proposed
by this plan, and none may be taken without the operator's explicit go-ahead, each time.

**How to read the numbers.** **[M]** = measured by a command this session ran, reproduction in
Appendix A. **[D]** = derived by arithmetic from an [M] figure, and labelled so because arithmetic
across content types is exactly where this session's own first attempt went wrong (§1.4).
**[C]** = claimed in existing prose and *not* re-derived. This convention is not decoration: the
defect being corrected here is a number that was measured once, in one unit, and then carried.

---

## 0. The verdict

`READ_CAP_LINES = 2000` is a **distributed** constant that is wrong three separate ways, and the
three have to be separated because they have different remedies and different risks.

1. **Its stated behaviour is false.** The justification shipped beside it — *"a Read past it
   returns the first 2,000 lines with no error and no missing-data marker"* — is wrong in both
   halves. Truncation is **loudly announced**, and it does not deliver 2,000 lines. [M, §1]
2. **Its unit is wrong.** The cap is denominated in **tokens (~25,000)**, not lines. [M, §1]
3. **Its value is wrong in the unsafe direction.** At this repo's ledger density a Read cliffs near
   line **690**, so the guard is roughly **2.9× too permissive** — a ledger at 1,999 lines passes
   every check while delivering about a third of itself. [M, §1.3]

**And the cheap fix is a trap.** Correcting the constant *alone* makes the trimmer's line-rate rule
**degenerate on both of this repo's ledgers** — it fires permanently and its stop condition becomes
unsatisfiable at every file size, because `LINE_FIRE_BELOW`/`LINE_STOP_ABOVE` are denominated in
*records of headroom to `READ_CAP_LINES`*. Measured through the tool's own code path in §3. **This
is the finding that decides the plan's shape**, and no grep for `2000` reaches it.

**And the most adopter-facing sites cannot be fixed by syncing.** The premise is stated as doctrine,
in a table, in `starter-kit/CHANGELOG.md:103` and `starter-kit/HANDOFFS.md:97` — the two ledger
**seeds**. `bin/_manifest.py` marks them `SEED`, which `bin/sync` writes *only when the destination
is absent and never overwrites afterward*. **So a correction there reaches future adopters only; every
already-bootstrapped project keeps the false doctrine permanently** (§5.1, §5.3). That is the same
defect class as BL-46/47/48, and it is the substantive reason this work batches with them.

**The structural result, which is better news than the above.** The framework **already ships a
guard on the right axis at very nearly the right value**: `DEFAULT_BUDGET_BYTES = 64 * 1024 =
65,536 B` sits *inside* the measured one-read band of **60,475–66,425 B**. [M/D, §4] It was
calibrated for an unrelated reason and lands on the real cliff by good luck. So the line cap is not
a missing guard needing a better number — it is a **redundant second guard on the wrong axis,
firing ~3× too late**, beside a byte guard that is already approximately correct.

**Recommendation: A → B → C as three separate sessions** (§7). Correct the false prose first,
because everything downstream inherits it and it blocks nothing; then re-denominate; then reconcile
the two now-overlapping signals. **Decline the one-pass fix.**

**What this plan deliberately does not claim.** The practical harm here is **modest**. Truncation is
*ordered* top-down and both ledgers are newest-on-top, so Phase 0's frontier read and Phase 3A's
single-receipt read land inside the delivered prefix; this repo measured whole-file reads at
**1-in-81** [C, `.context-budget.json`]. What is defective is the **published claim** and the
constant's **unit**, more than any outcome anyone has suffered. A plan that oversells this would be
committing the error it is correcting.

---

## 1. The premise, measured

### 1.1 The probes

Four, this session, this harness (Claude Code, Opus 5 1M-context, macOS, 2026-08-26). Probes A and
B reproduce the sibling document's; **probe C and probe D are this session's**, and D is the one
that falsified this session's own first draft.

| # | file | shape | result |
|---|---|---|---|
| A | `probe_lines.txt` | 3,000 ln / 21,000 B | **returned whole.** The documented "up to 2000 lines by default" **did not bind** [M] |
| B | `probe_bytes.txt` | 101 ln / 199,700 B | **cut at line 10**, banner: `PARTIAL view … lines 1-10 of 101 total (199405 tokens, cap 25000)` [M] |
| **C** | **2,000 ln of this repo's real `CHANGELOG.md` content, 149,585 B, 74.8 B/line** | **61,844 tokens vs cap 25,000 — cut at line 687 of 2,001. 34% delivered.** [M] |
| **D** | `starter-kit/FRAMEWORK_LEARNINGS.md`, 66 ln / 65,520 B | **returned whole, no banner** — so ≥ **2.62 B/token** for that content [M] |

### 1.2 What they establish

- **The binding limit is tokens, not lines.** A 3,000-line file passed; a 101-line file did not.
- **Truncation is loud.** The banner reports the partial view, total lines, total tokens, the cap,
  the exact pagination call to make next, and *"Do NOT answer from this page alone if the answer
  may be further in the file."* The repository asserts the exact opposite in shipped code (§5).
- **Nothing is unreachable.** The banner names the next call; `offset`/`limit` address any span.
- **Truncation is ordered.** Probe C's 687 delivered lines are the **first** 687. In a
  newest-on-top ledger that means a Read delivers the front matter and the newest records — which
  is exactly what Phase 0 and Phase 3A need. **This is why the harm is modest and why the fix is
  still worth making:** the invariant worth protecting is *"front matter + the K newest records fit
  in one read"*, and total file length does not appear in that sentence.

### 1.3 The value is wrong, not only the unit

> **⚠ CORRECTED BY MEASUREMENT AT PHASE B — see §12.3.** The *~2.9× too permissive* below was
> measured on `CHANGELOG.md` content only. Re-measured per ledger it is **2.32× for
> `CHANGELOG.md` and 8.75× for `HANDOFFS.md`** — this section understates the second by 3×.

Probe C is the load-bearing measurement: at **this repository's own ledger density**, a file at the
declared 2,000-line ceiling delivers **687 lines**. The real cliff is ~**2.9× lower** than the
constant. A ledger sitting at 1,999 lines passes `READ_CAP_LINES` while a reader sees a third of it.

**The constant's own cited basis says the same thing when re-measured.** The comment at
`starter-kit/methodology_dashboard.py:266-268` grounds the value in a real incident:

```
# BASIS — the failure already happened here, and was found by accident rather than by any check:
#   git show 3aee4e3^:CHANGELOG.md | wc -l    -> 2,090
```

Re-measured [M]: `3aee4e3^:CHANGELOG.md` is **2,090 lines / 186,704 B / 89.3 B per line** — that is
**2.8–3.1× the token cap** [D], so it had been truncating since roughly **line 676–743** [D]. The
incident is real and the diagnosis was right. **The number derived from it records the size at
which the problem was *noticed*, not the size at which it *starts*.**

### 1.4 The unit argument inverts — and this session got it wrong first, which is the lesson

The comment at `starter-kit/methodology_dashboard.py:258-262` argues the unit explicitly:

> `# UNIT: LINES, because the cap is in lines. Bytes are not a proxy — measured in this repo,`
> `# HANDOFFS.md runs ~265 B/line and CHANGELOG.md ~83 B/line, so any single byte threshold is`
> `# wrong for one of them by ~3x, and would flag the file that is NOT truncating while missing`
> `# the one that did.`

The ~3× spread is real — re-measured today at **74.7 and 227.4 B/line** [M]. But the cap is
token-denominated, and tokens track **bytes**, not lines. **So the comment's own evidence, correctly
measured, argues for the opposite conclusion:** it is precisely that 3× B/line spread which makes a
single **line** threshold wrong for one ledger by ~3×.

**And bytes are only a proxy too — which this session established by being wrong.** A first draft
extrapolated probe C's 2.419 B/token across every governed file and produced a table asserting that
two of them *already truncate today*. Probe D was run to confirm it and **falsified it**:
`FRAMEWORK_LEARNINGS.md` at 65,520 B came back **whole**, so its content runs ≥2.62 B/token. The
measured range across real markdown this session is **2.42–2.66 B/token** — enough spread that a
single published conversion would be a new wrong constant of exactly the kind being removed.

> **The durable form of this correction is a METHOD, not a number.** "Re-run Appendix A" stays true
> when the harness changes; "25,000 tokens" does not. Any repair that writes a new numeral without
> writing the command that re-derives it has reproduced the defect one level over.

---

## 2. What the constant actually does — three jobs, three sensitivities

`READ_CAP_LINES` is not one guard. It feeds three consumers with different failure modes, and a
correction affects them differently. All line numbers verified by re-reading the cited line [M].

| # | consumer | site | what it does | effect of a 3× correction |
|---|---|---|---|---|
| **J1** | dashboard risk | `starter-kit/methodology_dashboard.py:3006-3013` | emits a **`high`**-severity risk when a watched file exceeds the cap | fires **earlier and far more often**, across the whole fleet. This is the point, and it is a fleet-visible behaviour change. |
| **J2** | trim rate rule | `starter-kit/methodology_trim.py:729`, `:809`; `starter-kit/methodology_dashboard.py:1046` | `headroom = (READ_CAP_LINES − line_count) × de ÷ dl`, in **records**; feeds `choose_cut`, `--check`'s exit code and the write gate | **degenerates — see §3.** `choose_cut` falls through to `return 1`: every adopter's next trim retains ONE record. |
| **J3** | grammar refusal | `starter-kit/methodology_trim.py:1589` | one of three disjuncts choosing `NO_RECORDS` (benign) vs `GRAMMAR_MISMATCH` (refusal) | **widens the refusal population.** A record-less file of 700–2,000 lines newly refuses instead of reporting empty. Nobody would predict this from "fix the read cap". |

J3 deserves a sentence of its own because it is the least obvious. There, the cap is not a
truncation guard at all — it is a **plausibility test** (*"a file this big is not really empty; I
should refuse to guess rather than report zero records"*). Its correct value is a question about
seed plausibility, not about the Read tool. **It may be right to leave J3's threshold where it is
and give it its own name**, rather than let it inherit a correction made for a different reason.

---

## 3. The coupling that makes the naive fix dangerous

> **⚠ UNDERSTATED, AND PHASE B MEASURED THE STRONGER RESULT — see §12.3.** This section shows
> the rate rule degenerating at a *corrected* cap. It is degenerate at **every honest cap**:
> a one-read `CHANGELOG.md` holds **20.9** records and a one-read `HANDOFFS.md` **4.3**,
> against a rule demanding **30** records of headroom. The shipped 2,000-line cap is what
> hid that, by granting 2.32×/8.75× more capacity than a real read. **The conclusion below
> stands and is strengthened: the rule was removed, not re-derived.**

`LINE_FIRE_BELOW = 15` and `LINE_STOP_ABOVE = 30` (`starter-kit/methodology_trim.py:94-95`) are the
published rate rule: *archive when headroom falls below 15 records; cut oldest-first until it is
back above 30.* **Headroom is denominated in records of headroom to `READ_CAP_LINES`.** They are not
free parameters — their calibration only holds while the cap sits far above operating size.

Evaluated through the tool's own arithmetic, with `de`/`dl` taken from each ledger's real baseline
commit exactly as `evaluate_trigger` does [M]:

| ledger | baseline | growth | cap = 2000 (shipped) | cap = 690 (measured cliff) |
|---|---|---|---|---|
| `CHANGELOG.md` | `95ac6ea` | 54.4 ln/record | headroom **23** — does not fire; stop arm reachable (max 36) | headroom **−1 — FIRES**; **max possible headroom on an empty file = 12**, so `>30` is **unreachable at every size** |
| `HANDOFFS.md` | `9cf4ae0` | 31.0 ln/record | headroom **55** — does not fire; stop arm satisfied | headroom **12 — FIRES**; **max possible = 22**, `>30` **unreachable at every size** |

`Trigger.stops()` returns `byte_ok and line_ok` where `line_ok = headroom > LINE_STOP_ABOVE`
(`:725-733`). **With the line arm permanently false, `stops()` can never return true.** And
`stops()` has exactly one caller — `choose_cut` (`:876-881`):

```python
for k in range(n - 1, 0, -1):
    b, l = resulting(k)
    if trigger.stops(b, l, de, dl):
        return k
return 1                      # <-- the fall-through when NOTHING satisfies stops()
```

`k` is the number of records **retained**; everything past it is archived. So the failure is not
that the tool reports oddly — **`choose_cut` falls through to `return 1`, and the next `--write` at
every adopter retains ONE record and archives the rest.**

This repo has already measured what that costs. S94 recorded that a cut retaining **two** receipts
took `bin/tests.sh` from 235/1 to 229/6, because Test 34 reads its mutation anchors as `ids[1]`/`ids[2]`
of the live ledger (Learning #31); S96 then found the true figure was **six** assertions, not five,
because one emitted no row at all (Learning #33). A cut to **one** is strictly worse than the case
those two learnings were written about.

**The write path is gated by the same value.** `:809`'s headroom feeds `Trigger.fires`, which drives
both `--check`'s exit code (`:1698`) and the gate on the entire write path (`:1702`,
`if not trigger.fires and opts.cut is None: NOTHING_TO_DO`). So the corrected constant decides
*whether* a trim runs, and `choose_cut` decides *how deep* — and both move the wrong way together.

> **Conclusion, and it is the plan's spine: `READ_CAP_LINES` cannot be corrected in isolation.**
> Whatever replaces it, `LINE_FIRE_BELOW` and `LINE_STOP_ABOVE` must be re-derived in the same
> change or removed with it. A session that "just fixes the number" ships a degenerate trigger to
> every adopter, and **every existing test stays green**, because no test evaluates the rate rule
> at a corrected cap.

---

## 4. The framework already has a guard on the right axis

> **⚠ THE COINCIDENCE IS LOOSER THAN STATED — see §12.3.** Against the *watched* population's
> re-measured one-read band (**56,762–62,875 B**), `DEFAULT_BUDGET_BYTES = 65,536` sits
> **above** it, not inside: 65,536 B is **27,720 tokens** at `HANDOFFS.md` density, over the
> cap by 11%. Directionally the section's point holds — the byte guard is approximately the
> real cliff and the line guard is not — but it is *permissive* by ~11%, not centred.

| conversion | one-read boundary in bytes |
|---|---|
| 25,000 tok × **2.419** B/tok (probe C, `CHANGELOG` content) | **60,475 B** [M/D] |
| 25,000 tok × **2.621** B/tok (probe D, lower bound) | **65,520 B** [M/D] |
| 25,000 tok × **2.657** B/tok (sibling probe, prose) | **66,425 B** [C/D] |
| **`starter-kit/methodology_trim.py:93` `DEFAULT_BUDGET_BYTES = 64 * 1024`** | **65,536 B** |

**The byte budget already in the framework sits inside the measured one-read band.** Its stated
derivation is unrelated — *"design §5.4: calibrated to the three sizes this repo operated at"* — so
this is a coincidence, not a design. It is nonetheless the most consequential fact in this plan: the
framework's byte guard is approximately the real read cliff, and its line guard is not.

The repo has already half-recorded this. `starter-kit/methodology_dashboard.py:292-294` says
the D4(b) cap row and the S38 trim-trigger row are *"separate risks on purpose and neither
subsumes the other"*, and `:3001-3003` says **"the dedup between the two rows is raised and
undecided (S38's residual 1)"**.
**This plan's measurement answers that open question:** on the corrected axis one row very nearly
*does* subsume the other, and the dedup should be decided rather than left standing.

---

## 5. Evidence-based inventory (MANDATORY)

Produced by **six independent search angles run blind to each other**, plus two adversarial critics —
because this repo's own history says a single pattern misses derived neighbours (S106 found a prior
plan's inventory short by two sites, one of which *stayed green while testing nothing*, because the
pattern `18,?432` cannot match `18433`).

**Every reported citation was then re-read and machine-verified against the actual file: 255 of 255
matched** [M]. A subagent's citation is a claim until the line is read. **301 sites across 30 files**, all six angles complete;
**265 live/repairable, 34 frozen or false-positive**; **92 of the live ones are distributed.**

> **The sweep earned its cost, and the honest way to say so is that it caught THIS PLAN.** A first
> draft of §5 was written from this session's own reading and named 19 sites. The completed sweep
> found live sites in **ten further files**, three of them **distributed seeds** — including the two
> that state the false claim as doctrine, in a table, in the documents every adopter receives
> (§5.3). Had the plan shipped on one reader's inventory it would have sent an executor to fix the
> code and leave the doctrine.

Commands are in Appendix A. **Distribution verdicts are read off `bin/_manifest.py`'s SOURCE (first)
column**, never a bare filename — grepping the name matches the DEST column and inverts the answer.

### 5.1 Two distribution kinds, and the difference decides the remedy

`bin/_manifest.py:19-22` defines them, and this plan turns on the distinction:

- **`TRACKED`** — sync overwrites toward the adopter. **A fix here reaches every adopter at their
  next `bin/sync`.**
- **`SEED`** — *"adopter owns it after first creation; sync writes it ONLY when the dest is absent
  and never overwrites it afterward"* (`bin/sync:225-230`). **A fix here reaches only FUTURE
  adopters. Every already-bootstrapped project keeps its copy of the false doctrine permanently,
  and no sync will ever touch it.**

> **This is the same defect class as BL-46/47/48** — seed content that went wrong and that `bin/sync`
> structurally cannot repair — which is the substantive reason this work batches with them rather
> than merely a scheduling convenience.

### 5.2 TRACKED carriers — a fix reaches existing adopters

```
bin/_manifest.py:44   ("starter-kit/methodology_dashboard.py", "methodology_dashboard.py", TRACKED)
bin/_manifest.py:50   ("starter-kit/methodology_trim.py",      "methodology_trim.py",      TRACKED)
bin/_manifest.py:54   ("starter-kit/context_budget.py",        "context_budget.py",        TRACKED)
```

| site | category | what it is |
|---|---|---|
| `starter-kit/methodology_trim.py:92` | constant | `READ_CAP_LINES = 2000  # agent Read truncation cap — harness behaviour, not a repo property` |
| `starter-kit/methodology_trim.py:696` | behaviour-claim | *"Lines protect against SILENT TRUNCATION (a Read past the cap returns no error and no marker)."* — the header comment for the whole two-metric trigger block, and **the stated raison d'être of the line metric** |
| `starter-kit/methodology_dashboard.py:269` | constant | `READ_CAP_LINES = 2000` — twin, **byte-identical** to `tools/methodology_dashboard.py` (`diff -q` [M]) |
| `starter-kit/methodology_dashboard.py:258-262` | behaviour-claim | the `UNIT: LINES` argument (§1.4) |
| `starter-kit/methodology_dashboard.py:262-263` | behaviour-claim | *"returns the first 2,000 lines with no error and no missing-data marker"* — **false in both halves** |
| `starter-kit/methodology_dashboard.py:266-268` | behaviour-claim | the `BASIS` incident — real, but re-measured at 2.8–3.1× the cap (§1.3) |
| `starter-kit/methodology_dashboard.py:3010-3013` | adopter-doc | the shipped **`high`**-severity risk text, repeating *"silently truncated … no error and no missing-data marker"* |
| `starter-kit/methodology_trim.py:94-95` | derived-arithmetic | `LINE_FIRE_BELOW = 15`, `LINE_STOP_ABOVE = 30` — **denominated in the cap (§3)** |
| `starter-kit/methodology_trim.py:729`, `:809` | derived-arithmetic | the two headroom call sites (fire arm and stop arm — fixing one only splits the semantics) |
| `starter-kit/methodology_trim.py:1589` | consumer | J3, the `classify_empty` refusal disjunct |
| `starter-kit/methodology_dashboard.py:1046` | derived-arithmetic | `(READ_CAP_LINES - live_lines) * de // dl` |
| `starter-kit/context_budget.py:374-375` | config-axis | the docstring justifying the LINES axis *"because that is the unit an agent's read cap comes in"* |

### 5.3 SEED carriers — a fix reaches only FUTURE adopters

```
bin/_manifest.py:57   ("starter-kit/CHANGELOG.md",        "CHANGELOG.md",        SEED)
bin/_manifest.py:58   ("starter-kit/HANDOFFS.md",         "HANDOFFS.md",         SEED)
bin/_manifest.py:60   ("starter-kit/context-budget.json", ".context-budget.json", SEED)
```

**These are the most adopter-facing sites in the whole inventory, and the first draft of this plan
missed all three.** Both ledger seeds carry the same doctrine table, which states the premise, its
falsity and its derived thresholds in a single row:

> `starter-kit/CHANGELOG.md:103` — *"| **Lines** — ~2,000, the agent `Read` truncation cap |
> **silent truncation**: a read past the cap returns no error and no marker, so the oldest entries
> simply stop existing for the reader | a **rate** | headroom < **15** entries | headroom > **30** |"*
>
> `starter-kit/HANDOFFS.md:97` — the same row, worded for receipts.

**Read the row beneath it in the same table:** *"| **Bytes** — a per-file budget, default **65,536 B**
(64 KB) | **context tax** … |"*. **The seed puts the wrong guard and the approximately-right one
side by side (§4) and tells the adopter neither subsumes the other.**

| site | category | what it is |
|---|---|---|
| `starter-kit/CHANGELOG.md:97-103` | behaviour-claim / adopter-doc | the two-caps doctrine table and its preamble |
| `starter-kit/HANDOFFS.md:91-97` | behaviour-claim / adopter-doc | the same, for receipts |
| `starter-kit/context-budget.json:36-37` | config-axis | `max_lines: 400`, `max_bytes: 120000` on `SESSION_NOTES.md` — the axis question one level down |

### 5.4 Canonical-only — live, but a different repair class

`tools/test_methodology_dashboard.py:3190-3193` (**pins the two distributed literals to each other**)
and `:3256-3262` (the exactly-at-cap boundary test, written because a `>`→`>=` mutant survived);
`tools/test_methodology_trim.py` (22 live sites — a test coupling the first draft missed entirely);
`.context-budget.json:45`, `:59`; `README.md:375-378`, `:390`; `CHANGELOG.md` front matter;
`starter-kit/SESSION_RUNNER.md:336` (FM #28's row); `docs/planning/BACKLOG.md:158` (BL-9's row);
`bin/tests.sh` (4 sites).

**And a judgment this plan raises rather than settles.** The sweep also found live sites in
`docs/planning/ledger-trimmer-design.md` (11), `docs/planning/framework-context-cost-plan.md` (18),
`docs/planning/uat-2026-08-04-six-adopters.md` (7), `uat-2026-08-08-followup.md` (1),
`docs/audits/2026-08-15-bl36-archive-losslessness.md` (2) and `BACKLOG-DETAIL.md` (1). These are
**design and audit records** — not ledgers, so FM #22 does not obviously bind, but they state what
was believed when written. **Annotate, or leave? The operator should decide before Phase A**, because
the answer sets the size of the repair set and Phase A's verify grep depends on it. This plan's
recommendation: **leave them, and annotate only `ledger-trimmer-design.md`**, which is the design a
future session would read to re-derive the rate rule.

### 5.5 Frozen — must NOT be repaired (FM #22)

Every statement of the 2,000-line cap inside `CHANGELOG.md` records, `HANDOFFS.md` receipts, and
everything under `docs/archive/**` is a record of **what was believed when written** and is correct
as such. **A repair that edits them is a defect, not a completion.** This is the rule S106 applied
when it rewrote two live sentences to say "18 KiB" rather than exempt them — keeping the zero-hit
grep a live detector without falsifying history.

## 6. Options

Independent unless noted. **Cost** in sessions.

| | option | mechanism | buys | costs / breaks |
|---|---|---|---|---|
| **A** | **Correct the premise text only** | Rewrite the live behaviour claims in §5.2 (TRACKED), §5.3 (SEED) and §5.4 to state measured behaviour **and the reproduction method**; state that frozen occurrences stay wrong. Leave every numeral alone. | Removes a false foundation from six distributed files, **including the two seed doctrine tables**. Blocks nothing. Cannot degenerate anything. | ~⅓ session. The pinned literals do not move, so no test changes. **Does not fix the 3× permissiveness.** |
| **B** | **Re-denominate on bytes, via the repo's own calibrated ratio** | Replace the line cap with a byte cap derived from `context_budget.py`'s already-calibrated `bytes_per_token` × a token cap constant. Re-derive `LINE_FIRE_BELOW`/`LINE_STOP_ABOVE` in the same change (§3). | Puts the guard on the axis the cap is actually denominated in, using an instrument the framework **already ships and tests**. | ~1 session. **Two estimators are not one:** `context_budget.py`'s 2.80 B/tok is calibrated against *opening context vs `CLAUDE.md` size*, a different quantity from the Read tool's own estimator (2.42–2.66 measured). The plan must not silently equate them. |
| **C** | **Decide the dedup (S38's residual 1)** | Given §4, decide whether the D4(b) cap row and the S38 trim-trigger row remain two risks or become one. | Ends an open question the code itself flags, and stops a ledger past both thresholds getting two remedies for one problem. | ~½ session. Pure judgment; needs A and B settled first or it is decided on false premises. |
| **D** | **Delete the line axis entirely** | Drop `READ_CAP_LINES` and the `max_lines` ceilings; rely on the byte budget, which §4 shows is already approximately the real cliff. | Simplest. Removes a whole wrong-unit mechanism rather than re-tuning it. | ~1 session. Loses J3's plausibility test unless it is re-homed under its own name, and loses the `max_lines` structural signal in `context_budget.py`. **Irreversible in a distributed file** — recovering it later is a second upstream PR. |
| **E** | **Probe-based measurement** | Ship a probe that measures the real cliff per repo. | Exact, and immune to harness change. | **Not buildable as specified.** `methodology_dashboard.py`, `methodology_trim.py` and `context_budget.py` are Python; **none can invoke the agent's `Read` tool.** They can only ever proxy. Recorded so a future session does not re-propose it. |

**Rejected on mechanism, not taste:** raising `LINE_STOP_ABOVE` to keep the rate rule satisfiable
under a corrected cap. It re-tunes a threshold to make a wrong-unit rule survivable, which is the
move §1.4 names as reproducing the defect one level over.

---

## 7. Recommendation

**Rule for A, then B, then C — three separate sessions, in that order. Decline the one-pass fix.
Decline D for now.**

**Why A first.** The rule's stated rationale is false and everything downstream inherits it. It is
the cheapest item, it blocks nothing, it changes no numeral, and it cannot degenerate anything.
Doing it first means the B decision is made on true premises. It is also the only part that is
unambiguously right regardless of what the operator decides about the number.

**Why B second and not bundled.** §3 shows the number cannot move alone. Bundling A and B makes it
impossible to tell which half moved a test — and the suite is the only feedback available, since no
test can invoke the real cap (§8, surface).

**Why C last.** It is a judgment about redundancy between two signals, and §4's measurement is what
makes it answerable. Deciding it before B means deciding it on the old axis.

**Why not D.** It is probably right in the long run, and it is irreversible in a distributed file.
The evidence for it — §4's coincidence — is one session old and rests on a token ratio measured
across two content types. **Let B ship, watch what the fleet's dashboards actually say, then revisit.**
Recording that this is a *deferral on evidence*, not a rejection.

**What I am least confident about.** Whether 25,000 tokens is stable across harness versions, or
whether it is a current configuration that will move. Probe A shows the *documentation* already
disagrees with behaviour, which is weak evidence that the number is not contractual. **This is the
strongest argument for A's "state the method, not the number" framing, and against baking any new
numeral anywhere.**

---

## 8. Phases

Each is **one session. Close out when its criterion passes. Do not bundle.**

### The surface, stated once because it governs every phase

> **Every DONE criterion below is demonstrated on the canonical repo's own suites — `bin/tests.sh`
> and the three Python suites — run locally. That surface CANNOT enforce the property under test.**
> `methodology_dashboard.py`, `methodology_trim.py` and `context_budget.py` are Python; none can
> invoke the agent's `Read` tool, and `bin/tests.sh` contains **zero** `READ_CAP` references [M].
> **No test in this repository can falsify a claim about the read cap.** The only instrument that
> can is a live agent session running Appendix A.
>
> **Consequence, and it is binding:** a green suite is evidence that nothing *else* broke. It is not
> evidence that the cap claim is right. Each phase below therefore requires **Appendix A re-run in
> the implementing session**, and its output pasted into the close-out receipt — not "the plan says
> 25,000". That is Learning #18 applied to this plan: *for every behavioural sentence you ship, name
> the command whose output you watched.*

### Phase A — correct the premise text

- **Do:** rewrite every behaviour-claim and adopter-doc row in **§5.2 (TRACKED), §5.3 (SEED) and
  §5.4** to state measured behaviour **and the method**. State explicitly, in the live copies, that
  frozen occurrences remain wrong and why. **Change no numeral.**
- **The two seed doctrine tables are the priority** (`starter-kit/CHANGELOG.md:103`,
  `starter-kit/HANDOFFS.md:97`) — they are the most adopter-facing statement of the false claim in
  the corpus, and §5.1 means correcting them helps only future adopters, so the session must also
  record what existing adopters need done to them by hand.
- **First act:** settle §5.4's open question with the operator (annotate the design records, or
  leave them?), since Phase A's verify grep depends on the answer.
- **DONE:** no live site asserts that truncation is silent or that a Read returns the first 2,000
  lines; **both seed doctrine tables corrected**; every rewritten site names Appendix A;
  `docs/archive/**`, `CHANGELOG.md` records and `HANDOFFS.md` receipts are **untouched**; the
  existing-adopter remediation note written (§5.1).
- **Verify:** `git grep -nE 'no (error|missing-data) marker|silently truncat'` returns **only**
  frozen paths · `bash bin/tests.sh` matches its pre-change control row-for-row · `python3 bin/check-links` ·
  `python3 bin/check-learnings` · `diff -q starter-kit/methodology_dashboard.py tools/methodology_dashboard.py`
- **Surface:** local suites; see above. **Plus Appendix A re-run.**

### Phase B — re-denominate

- **Do:** replace the line cap with a byte-denominated term derived from a stated token cap and a
  calibrated ratio. **Re-derive `LINE_FIRE_BELOW` and `LINE_STOP_ABOVE` in the same commit (§3).**
  Decide explicitly whether J3 (`:1589`) keeps its own threshold under its own name (§2).
- **DONE:** the rate rule is **non-degenerate at both ledgers' real densities**, demonstrated by the
  §3 table recomputed and pasted into the receipt; the pinning test at
  `tools/test_methodology_dashboard.py:3190-3193` re-points to whatever the new source of truth is,
  or is deliberately removed with a stated reason; both twins byte-identical.
- **Verify:** re-run §3's arithmetic through `evaluate_trigger` at the new value and show
  `stops()` is satisfiable · `python3 starter-kit/methodology_trim.py --file CHANGELOG.md --check`
  and `--file HANDOFFS.md --check` · the Python suites · `bash bin/tests.sh` against a **worktree
  control at the claim commit**, diffed row-for-row, expecting zero rows lost.
- **Surface:** local suites — **and a fleet check.** Run the corrected dashboard read-only against
  the four known adopter repos and record which risks newly fire. That is the closest available
  surface to the one the change actually ships to, and it is still not production.
- **⚠ Do not bundle with A.**

### Phase C — decide the dedup

- **Do:** settle S38's residual 1 (§4) — two rows or one.
- **DONE:** the decision recorded in `CHANGELOG.md` **and** in the code comment that currently says
  it is undecided; `starter-kit/methodology_dashboard.py:3001-3003` no longer describes an open
  question.
- **Verify:** prose plus suites.
- **Surface:** local suites.

---

## 9. Here be dragons

1. **The rate rule is denominated in the cap (§3).** This is the one that turns a one-line fix into
   a fleet-wide degenerate trigger, with every test green. Re-derive together or not at all.
2. **The two `methodology_dashboard.py` twins must stay byte-identical** — a canonical test compares
   them, and S37 recorded the exact failure of editing one after mirroring. Mirror **last**, then
   re-run; any number recorded before the mirror is false without anything failing.
3. **The pinning test asserts two copies against each other**, not against an independent truth
   (`tools/test_methodology_dashboard.py:3190-3193`). It is honest about this in its own docstring —
   *"Independent operands"* refers to *where each is read from*, not to what they mean. It will keep
   both literals consistent while both are wrong. Changing one without it is caught; changing the
   premise both encode is not.
4. **`READ_CAP_LINES` has three jobs (§2) and the third is not about truncation at all.** Do not let
   J3 inherit a number corrected for J1's reasons.
5. **Correcting the value makes adopter dashboards go red.** That is the guard working, and it is
   still a fleet-visible behaviour change that the operator should expect rather than discover.
   Of the four known repos, at least `nprcgenekeepr` (218,298 / 286,154 B) and this repo's own
   `HANDOFFS.md` would newly fire [C, S109's four-repo table].
6. **Frozen records must not be repaired (§5.3).** They look like repair targets. They are not.
7. **Two estimators are not one.** `context_budget.py`'s `bytes_per_token` (2.80 here, R² 0.81) is
   calibrated on *opening context*, not on the Read tool's estimator (2.42–2.66 measured). Option B
   must state which it uses and why.
8. **Whether `limit` bypasses the token cap is UNTESTED.** Probe D passed an explicit
   `limit=66` and returned whole; probe C used no limit and truncated. **These are not a controlled
   pair.** If `limit` bypasses the cap, probe D's conclusion is an artifact. Settle it first with the
   bounded test in Appendix A — it is one command and it gates §1.4's ratio range.
9. **A SEED fix reaches nobody who has already bootstrapped (§5.1).** `bin/sync` writes a SEED only
   when the dest is absent and never overwrites it. Correcting `starter-kit/CHANGELOG.md` and
   `starter-kit/HANDOFFS.md` helps **future adopters only**; every existing project keeps the false
   doctrine table forever unless someone edits it by hand, per repo. Do not close this work
   believing the fleet is fixed.
10. **The first draft of §5 was short by ten files, three of them distributed seeds.** The completed
   sweep is in §5; do not re-derive the inventory from one reader's grep.

---

## 10. Explicitly not in scope

The 65,536 B ceiling · `RECORD_BUDGET_BYTES` · `HEADER_RESERVE_BYTES` · Test 34's retention floor ·
BL-42/43/44 · **BL-45** (the `FRAMEWORK_LEARNINGS.md` ceiling — an operator decision, unaffected by
this plan except that probe D measured that file to be *inside* the read cap, so the read cap is not
an argument for or against any BL-45 option) · BL-46(2)/47/48/49 · issue #75's unsent PR ·
**any outward-facing action whatsoever.**

---

## 11. Phase A close-out — what shipped, and what existing adopters still need by hand

**Written by S111 (2026-08-26), the implementing session. This section is a record, not a proposal.**

### 11.1 What shipped

| half | files | reaches |
|---|---|---|
| **TRACKED** | `starter-kit/methodology_dashboard.py` (+ its `tools/` twin), `starter-kit/methodology_trim.py`, `starter-kit/context_budget.py` | **every existing adopter**, at their next `bin/sync` |
| **SEED** | `starter-kit/CHANGELOG.md`, `starter-kit/HANDOFFS.md` | **future adopters only** — see §11.2 |
| **canonical-only** | `README.md`, this repo's `CHANGELOG.md` front matter, `ledger-trimmer-design.md` (annotated per §5.4) | this repository |

**No numeral moved.** `READ_CAP_LINES` = `2000`, `LINE_FIRE_BELOW` = `15`, `LINE_STOP_ABOVE` = `30`.

### 11.2 ⚠ The remediation existing adopters need, by hand, per repo

**`bin/sync` cannot do this and never will.** `bin/sync:225-230` writes a `SEED` **only when the
destination is absent**, and never overwrites afterward. So every project bootstrapped before
2026-08-26 holds a `CHANGELOG.md` and a `HANDOFFS.md` whose *"Size, and when to archive"* table still
states, as doctrine, that a read past the cap **"returns no error and no marker"**. Nothing in the
framework will ever correct it, and **nothing detects it** — the same shape as BL-46/47/48.

**Per adopter, one edit each in two files.** Locate the row and replace the *Protects against* cell:

```sh
grep -n 'silent truncation' CHANGELOG.md HANDOFFS.md     # the doctrine row, if present
```

Replace with the corrected cell from `starter-kit/CHANGELOG.md` / `starter-kit/HANDOFFS.md` at or
after this date. **Do not edit records or receipts below the front matter** — those are frozen
statements of what was believed when written (FM #22, §5.5).

**Known population at the time of writing — four repos, none remediated:** `wsfct`,
`nprcgenekeepr`, `vscode_quarto_ext`, `model_project_constructor`. Each needs the two edits above.
**This is unfinished work and is deliberately left unfinished:** it is cross-repo and touches
adopter-owned files, which is not this session's one deliverable.

### 11.3 Two findings Phase A produced that the plan did not anticipate

**Dragon 8 is SETTLED, and the plan's stated test could not have settled it.** Appendix A proposed
reading `FRAMEWORK_LEARNINGS.md` with and without an explicit `limit` — but that file returns
**whole** either way, so both hypotheses predict the same observation. Re-run on a file that *does*
truncate (`limit` the only variable), the answer is decisive and is a **third delivery mode** the
plan did not know about: an explicit `limit` spanning an over-cap region **neither bypasses the cap
nor truncates — it errors and returns no content at all.** So `limit` cannot mask the cap, probe D's
"returned whole" is **not** an artifact, and §1.4's 2.42–2.66 B/token range stands. Appendix A's
probe D should be re-worded to name a truncating file.

**Phase A's DONE criterion, as written in §8, is not satisfiable — and the reason is instructive.**
It requires `git grep -nE 'no (error|missing-data) marker|silently truncat'` to return **only frozen
paths**. It cannot: `starter-kit/methodology_trim.py:1077` matches *"command substitution strips
trailing newlines, which **silently truncates** the LAST record"* — a live, **distributed**,
**correct** sentence about `$(...)` in a shell proof, with no connection to the read cap. Eleven
shipped `.verify.sh` files carry the same line. **A repair there would be a defect.** The criterion's
real content is *no live site **asserts** the read-cap claim*; a site that **quotes** it in order to
correct it, or that uses the same words about an unrelated mechanism, is not a violation. The
corrected verify command, which returns **zero** rows across all live paths:

```sh
git grep -nE 'no (error|missing-data) marker|silently truncat' -- starter-kit bin tools README.md \
  | grep -v 'trailing newlines'        # the one carve-out: an unrelated $(...) hazard
```

**And one site was reworded rather than exempted, following S106's precedent (§5.5).** `README.md`
disclosed the correction by *quoting* the false phrase, which would have kept the detector returning
a row forever. The disclosure is worth keeping, so the sentence now names the old claim without
reproducing its exact words: the grep stays a **live zero-hit tripwire** and no history is
falsified. An exemption list would have retired the detector instead.

**This is the plan's own §5-inventory lesson landing on its §8:** a criterion is only as good as the
population its command actually enumerates.

---

## 12. Phase B close-out — what shipped, what it measured, and what it hands forward

**Written by S112 (2026-08-26), the implementing session. This section is a record, not a
proposal.** Operator's scope decision at Phase 1: **"B-min"** — re-denominate, delete the line
rate, rename J3, correct the false justification; leave `READ_CAP_WATCHED`, `DEFAULT_BUDGET_BYTES`
and the prefix guard for Phase C. Design presented and approved before any distributed constant
moved.

### 12.1 What shipped

| half | files | reaches |
|---|---|---|
| **TRACKED** | `starter-kit/methodology_trim.py` (1.3.0 → **1.4.0**), `starter-kit/methodology_dashboard.py` (+ its `tools/` twin, 2.15.2 → **2.16.0**), `starter-kit/context_budget.py` | **every existing adopter**, at their next `bin/sync` |
| **canonical-only** | `tools/test_methodology_trim.py`, `tools/test_methodology_dashboard.py`, `tools/test_context_budget.py`, this plan | this repository |

**No `SEED` was touched.** `starter-kit/context-budget.json`'s only `read-mandated` entry is
`SESSION_NOTES.md`, whose justification (*"Phase 0 step 2 orders a read of this file"*) is **true**
— checked before assuming the defect generalised.

```
READ_CAP_TOKENS      = 25_000    [M] verbatim from the tool: "exceeds maximum allowed tokens (25000)"
MIN_BYTES_PER_TOKEN  = 2.27      [M] FLOOR of 2.2705–3.0300 over 9 real files in 5 repos
READ_CAP_BYTES       = int(READ_CAP_TOKENS * MIN_BYTES_PER_TOKEN) = 56,750   — computed, never written
READ_REFUSE_BYTES    = 256 * 1024 = 262,144                                  — the hard, zero-content boundary
SEED_PLAUSIBLE_MAX_LINES = 2000  — J3's value, unchanged, under its own name
DELETED: READ_CAP_LINES, LINE_FIRE_BELOW, LINE_STOP_ABOVE, TRIM_LINE_FIRE_BELOW, trim_line_headroom()
```

### 12.2 The eleven measurements, all first-hand

Instrument: an explicit `limit` spanning an over-cap region **errors and returns no content**,
reporting the span's exact token count — a *free, exact* token meter. Three controls validate it:
a 3,000-line file returns **whole** (lines do not bind), a **536-line** file is **over** (lines do
not bind in the other direction either), and the estimator is **linear in content** —
`CHANGELOG.md`×2 = 42,767 tok, ×3 = 64,148 against 64,150 predicted, **0.004%**.

1. **The cap is 25,000 tokens**, stated by the tool itself.
2. **B/token over 9 real markdown files in 5 repos: 2.2705–3.0300 (1.33×).** One-read band
   **56,762–75,751 B**.
3. **B/line over the same fleet population: 70.8–611.9 (8.6×).** The byte axis is the tighter proxy
   by an order of magnitude.
4. **The line guard is STRICTLY DOMINATED.** Over 18 watched ledgers in 5 repos it fires on **3**;
   a byte cap fires on **11–14** at *every* threshold in the measured band. Files the line cap
   catches that even the most permissive byte cap misses: **none**. Files it misses that even the
   most permissive byte cap catches: **8**.
5. **`HANDOFFS.md` here is over the cap TODAY** — 69,266 B = **29,300 tokens measured**, 1.17× —
   and the shipped guard reported **no risk**, because it is 268 lines.
6. **A THIRD delivery mode.** Past **262,144 B** a default read is **refused outright with zero
   content**: `File content (256.1KB) exceeds maximum allowed size (256KB)`. Verified first-hand,
   and a bounded `offset`/`limit` span of the same file still returns content, so the refusal is
   on the *unbounded* read. **5 of the 18 fleet ledgers are already past it.**
7. **The rate rule is unsatisfiable at every honest cap** — §12.3 below.
8. **BL-52's precondition, re-derived not cited:** each root ledger read **whole once in 85
   transcripts**, in **part 1,696 / 1,797** times.
9. **The invariant the protocol actually needs is a PREFIX one.** `HANDOFFS.md`: front matter +
   the **4** newest receipts fit one read (Test 34's floor is 3). Satisfied today with a receipt of
   margin, **while the whole-file guard says OVER**.
10. **Both per-record guards are canonical-only** — `RECORD_BUDGET_BYTES` and `ROW_BUDGET_BYTES`
    are absent from `bin/_manifest.py`. No adopter has either.
11. **`context_budget.py`'s `bytes_per_token` is not the right instrument**, which is why nothing
    here uses it: re-running its own `--calibrate` today returns **2.46 at R² 0.59** (the config
    records 2.80 at R² 0.81), and at 2.46 it predicts `FRAMEWORK_LEARNINGS.md` truncates when a
    probe shows it returns whole. It estimates *opening context vs `CLAUDE.md` size* — a different
    quantity. Dragon 7, confirmed by measurement.

### 12.3 Three corrections to this plan's own earlier sections

- **§1.3** said *~2.9× too permissive*. Per ledger: **2.32× (`CHANGELOG.md`), 8.75×
  (`HANDOFFS.md`)** — measured on one content type and carried, which is the defect this plan
  exists to correct, one level over.
- **§3** said a *corrected* cap degenerates the rate rule. It is degenerate at **every** honest
  cap. A one-read `CHANGELOG.md` holds **20.9** records; a one-read `HANDOFFS.md` **4.3**; the rule
  demands **30** of headroom. **`LINE_FIRE_BELOW`/`LINE_STOP_ABOVE` were never satisfiable on
  `HANDOFFS.md` by any honest threshold** — the 2,000-line cap hid it. `ledger-trimmer-design.md`
  §5.2 already contained the reason: units-of-headroom is well-formed only while the cap *"sits far
  above normal operating size"*, and at operating size it prescribes *"a level with hysteresis, not
  a rate — the form that terminates"*. Removal was the design's own prescription, not a preference.
- **§4** said 65,536 B *"sits inside the measured one-read band"*. Against the **watched**
  population's re-measured band (56,762–62,875 B) it sits **above** it — 27,720 tokens at
  `HANDOFFS.md` density, over the cap by **11%**.

### 12.4 What Phase B hands to Phase C — sharper than it received it

- **The dedup (S38's residual 1) is now a decision between two BYTE levels**, 56,750 and 65,536,
  with distinct claims (read delivery vs context tax) and unrelated provenance. Phase B did not
  merge them and says so in the code.
- **The prefix guard is the strongest form of that decision and is measured, not sketched:**
  *front matter + the K newest records ≤ one read* is what Phase 0 and Phase 3A actually consume,
  it needs the record grammar (so the trimmer, not the dashboard), and on this repo today it says
  **OK with one receipt of margin** where the whole-file guard says **OVER**.
- **Narrowing `READ_CAP_WATCHED`** — deliberately not done. The justification was false for 2 of
  its **6** names (BL-52's addendum says *"three of the five"*: the population is six, and
  `SAFEGUARDS.md`, one of the three it credits, is **not in the set** — excluded as a `TRACKED`
  dest). No protocol text names `docs/BACKLOG.md` or `docs/planning/BACKLOG.md` at all.
- **`_newest_archive_sha` / `_trim_record_count` lost their only production consumer** and are kept,
  labelled, with 18 assertions still pinning them. Delete or re-wire them when Phase C decides the
  row's shape.
- **BL-52 IS ADJUDICATED FOR THIS REPO'S `HANDOFFS.md` AND THE TRIM WAS DECLINED ON EVIDENCE.**
  Measured: a whole-file read delivers the front matter + the **4 newest receipts** (23,370 tok
  measured against 23,409 predicted); the cut on offer would have archived two records **already
  outside** that prefix; Phase 3A reads **one** receipt and Phase 0 greps. The trimmer's `SRF_RED`
  refusal was honoured rather than `--force`d. Detail in `BACKLOG-DETAIL.md#bl-52`, third addendum.
  **Consequence Phase C must weigh: this repo now carries two red signals that are true and, on
  this measurement, not worth acting on.** That makes the dedup question larger than *two rows or
  one* — it is what population and claim each row carries, and the prefix guard above answers both.
- **`choose_cut` would retain 2 on `HANDOFFS.md`**, below Test 34's floor of 3 — **unchanged by
  Phase B** (it was 2 at the shipped line cap too), and the reason sessions pass `--cut 3`
  explicitly. Learning #35's collision, still standing.

---

## Appendix A — reproduction

```sh
# --- the read-cap probes. Read each with the Read tool, DEFAULT parameters, and record
# --- whether a PARTIAL-view banner appears and at which line it cuts.
awk 'BEGIN{for(i=1;i<=3000;i++) printf "L%05d\n", i}' > probe_lines.txt          # A: expect WHOLE
awk 'BEGIN{pad=sprintf("%*s",1990," "); gsub(/ /,"x",pad);
          for(i=1;i<=100;i++) printf "B%05d%s\n", i, pad}' > probe_bytes.txt     # B: expect cut ~line 10

# C: real ledger content at this repo's own density, built to the declared ceiling
head -667 CHANGELOG.md > probe_density.txt
head -667 CHANGELOG.md >> probe_density.txt
head -666 CHANGELOG.md >> probe_density.txt          # 2,000 lines; expect cut ~line 687

# D: a real governed file, and the CONTROLLED PAIR that dragon 8 requires --
#    read starter-kit/FRAMEWORK_LEARNINGS.md twice: once with NO limit, once with limit=<its line count>.
#    Same delivered span => limit does not bypass the cap. Different => probe D is an artifact.

# --- the constant, its consumers and its derived neighbours
git grep -n 'READ_CAP_LINES'
git grep -nE '2,?000|1,?999|2,?001|1,?500|75 ?%'
git grep -nE 'LINE_FIRE_BELOW|LINE_STOP_ABOVE|headroom'

# --- the behavioural claim
git grep -niE 'silent|quietly|no error|missing-data marker|truncat|stops at'

# --- separate live from frozen
git grep -nE '2,?000' -- docs/archive CHANGELOG.md HANDOFFS.md     # FROZEN: do not repair
git grep -nE '2,?000' -- starter-kit bin tools README.md           # LIVE: the repair set

# --- distribution, read off the SOURCE column (never the bare filename)
grep -nE '^\s*\("starter-kit/' bin/_manifest.py

# --- the cited basis, re-measured
git show 3aee4e3^:CHANGELOG.md | wc -lc          # -> 2090 lines, 186704 B

# --- the rate rule at a corrected cap (the §3 table)
#     recompute (cap - line_count) * de // dl with de/dl taken from each ledger's baseline commit,
#     exactly as starter-kit/methodology_trim.py:806-809 does, then check
#     stops() = byte_ok and (headroom > LINE_STOP_ABOVE) is still satisfiable at SOME file size.

# --- twins and checkers
diff -q starter-kit/methodology_dashboard.py tools/methodology_dashboard.py
bash bin/tests.sh ; python3 bin/check-links ; python3 bin/check-learnings ; python3 bin/check-handoff
python3 starter-kit/context_budget.py
```
