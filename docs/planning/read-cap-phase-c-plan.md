# Phase C — What each guard WATCHES, and what it CLAIMS

**Status:** **RATIFIED by the operator 2026-08-26**, at S115's claim. The recommendation in §8 —
`A1 → (A2 + C1 together) → A3 → (B1 + B2)`, as three sessions — is the approved sequence, and
**Phase C1 is authorized as S115's single deliverable.** Phases C2 and C3 remain unstarted and are
**not** authorized by this ratification; each is a separate session (§9), and every outward-facing
action still needs the operator's explicit go-ahead, each time.
**Author:** S113 (2026-08-26), at claim commit `f06b6f7`.

> **⚠ `C1` NAMES TWO DIFFERENT THINGS IN THIS PLAN, and a successor will meet both.** **Option C1**
> (§7) is *decide `DEFAULT_BUDGET_BYTES`*. **Phase C1** (§9) is *split the watched population by
> class*, which is **option A1**. So §9's Phase C2 instruction — *"Do: A2 and C1 in one commit"* —
> means **option** C1, the constant, and not Phase C1, which by then is already shipped. Read every
> bare `C1` by its section: §7 and §8 mean the option, §9 means the phase.
>
> **⚠ Phase C1 CHANGES NO THRESHOLD, and §7's A1 row reads as if it does.** That row's mechanism
> cell says the two classes get *"two thresholds"*; §8 says A1 *"changes no threshold and cannot
> degenerate anything"*, and §9's Phase C1 criterion names none. **§8 and §9 are binding and §7's
> cell is the summary that drifted** — the threshold move is **Phase C2** (option A2), which §8
> requires be bundled with option C1 or it is inert. Phase C1 is structure only.
**Origin:** the operator's proposal at S112's close-out — *"perhaps we should only worry about the
256 KB limit for trimming. Would that satisfy all methodology's needs?"*
**Predecessor:** [`read-cap-premise-correction-plan.md`](read-cap-premise-correction-plan.md)
§8 Phase C, whose one-line brief (*"two rows or one"*) this plan argues is too small.
**Scope:** fork-side planning only. The carriers are **distributed**, so implementation lands
upstream and batches with BL-46(2)/47/48/49. **No outward-facing action** is proposed, and none may
be taken without the operator's explicit go-ahead, each time.

**How to read the numbers.** **[M]** measured by a command this session ran (Appendix A).
**[D]** derived by arithmetic from an [M]. **[C]** claimed in existing prose and not re-derived.
Sizes are **as of 2026-08-26** and several moved during S112's own close-out; **re-measure rather
than cite** — that is the defect this campaign exists to correct, and it applies to this file.

---

## 0. The verdict

**The proposal is right for the files the trimmer can actually act on, and wrong as a blanket rule.**
The six watched names are **two classes**, and the class the proposal fits is not the class that
needs the smaller guard.

| | Class A | Class B |
|---|---|---|
| names | `CHANGELOG.md`, `HANDOFFS.md` | `SESSION_NOTES.md`, `BACKLOG.md` ×3 |
| structure | dated/fenced **records**, newest-on-top | prose; no uniform record delimiter |
| what the protocol reads | a **frontier** from `git log`; **one** record at Phase 3A | **the file** (Phase 0 steps 2, 3) |
| whole-file reads | **1 in 85** transcripts [M] | the instructed access path |
| can the trimmer act? | **yes** — the only two in `LEDGERS` | **no** — answers `NO_CONFIG` by design |
| does truncation lose what is needed? | **no**, between the two boundaries | **yes** — the tail is content you were told to consult |

**So: adopt the 256 KB rule for Class A (with two caveats, §3), keep the token-cap guard for
Class B (§4).** They are not competing thresholds; they are answers to different questions about
different files, and Phase B's mistake-in-waiting was treating the six names as one population.

**And Phase C is bigger than the dedup it was scoped as.** Deciding *"two rows or one"* presumes
both rows watch the same set. They should not.

**⚠ The finding this plan did not expect, and the one most worth the operator's attention.**
**Class B has 7 of 9 files over the read cap [M] and, for `SESSION_NOTES.md`, no documented remedy
at all.** The framework warns about a condition it never says how to fix. `BACKLOG.md` has one
remedy (`BOOTSTRAP.md:144-151`, "split out completed work") and **Learning #26 proves it
insufficient in general** — on this repo it recovered 33% and still left the file at 1.40× its
yardstick, because the *open* items alone exceeded it. **A guard whose remedy cannot reach is the
misdirection `ledger-trimmer-design.md` §7.3 exists to prevent**, and it is currently shipping.

---

## 1. What Phase B established that this plan rests on

All [M], reproduction in the predecessor plan's Appendix A and this one's.

1. **Three delivery modes, not two.** ≤25,000 tokens → whole. Over that but ≤**262,144 B** →
   truncated to an ordered prefix, **with a banner**. Over 262,144 B → **refused outright, zero
   content, front matter included.**
2. **The guard is now byte-denominated**: `READ_CAP_BYTES = READ_CAP_TOKENS(25,000) ×
   MIN_BYTES_PER_TOKEN(2.27) = 56,750`, derived at import; `READ_REFUSE_BYTES = 262,144`.
3. **BL-52 is adjudicated for `HANDOFFS.md`**: a whole-file read still delivers the front matter and
   the **4 newest** receipts; Phase 3A needs **one**; the trim on offer would have archived records
   already outside the delivered prefix. The trim was **declined on evidence**.
4. **The rate rule is gone**, because it demanded 30 records of headroom on files that hold 20.9 and
   4.3.

---

## 2. The two classes, evidenced per name — not asserted

**Class membership is not a judgment.** It is read off two independent facts, each machine-checkable:
*is the name in the trimmer's `LEDGERS` table?* and *does `SESSION_RUNNER.md` instruct a read of it?*

| watched name | in `LEDGERS`? | what the runner says | class |
|---|---|---|---|
| `CHANGELOG.md` | **yes** | step 6 reconciles it **against `git log`** (`SESSION_RUNNER.md:18`, `:37-39`) | **A** |
| `HANDOFFS.md` | **yes** | step 6 computes a **frontier**; a pending receipt is found by **grep** (`SAFEGUARDS.md:179`); Phase 3A reads **one** receipt | **A** |
| `SESSION_NOTES.md` | no | step 2: *"then read it — focus on the ACTIVE TASK section at the top"* (`:14`), and *"Steps 1-3 are READS, not skims"* (`:33`) | **B** |
| `BACKLOG.md` | no | step 3: *"Fall back to `BACKLOG.md` if no repo exists"* (`:15`) — **conditional** | **B** |
| `docs/BACKLOG.md` | no | **named nowhere** in the runner or `SAFEGUARDS.md` [M] | **B** |
| `docs/planning/BACKLOG.md` | no | **named nowhere** [M] | **B** |

**Two honesty notes this table must carry.** The runner says *"in full"* about exactly **one** file —
`SAFEGUARDS.md` (`:13`) — which is **deliberately not watched**, being a `TRACKED` dest a canonical
test forbids flagging. And **two of the six names have no protocol basis at all**; they are watched
by analogy to the root basename. Both facts are corrections to BL-52's own addendum, which said
*"three of the five watched names"* — the set holds six.

**The fleet, by class** [M], 18 files across 5 repos:

| class | n | over `READ_CAP_BYTES` | over `READ_REFUSE_BYTES` |
|---|--:|--:|--:|
| **A** — trimmer can act | 9 | 8 | 2 |
| **B** — trimmer refuses | 9 | **7** | 3 |

---

## 3. Class A — the proposal holds, with two caveats

For `CHANGELOG.md` and `HANDOFFS.md` the operator's reasoning is sound and this plan endorses it.
What the protocol consumes fits comfortably and stays fitting as the file grows:

| | front matter + newest record | share of one read | growth headroom before the newest record is cut |
|---|--:|--:|--:|
| `HANDOFFS.md` | 18,650 B | **32%** | ~40,455 B |
| `CHANGELOG.md` | 18,995 B | **30%** | ~43,880 B |

Because truncation is ordered and these files are newest-on-top, **letting them run well past
`READ_CAP_BYTES` costs nothing anyone reads.** The only failure that matters is crossing
`READ_REFUSE_BYTES`, where the front matter itself stops being delivered.

**Caveat 1 — fire BELOW 262,144 B, never at it.** A trigger set at the refusal parks the file exactly
on the edge where the rare whole-file read stops degrading gracefully and starts returning **nothing**.
Proposed: **fire above 192 KB, cut back to 96 KB** — judgment, labelled as such, and the shape
(`level with hysteresis`) is the one `ledger-trimmer-design.md` §5.2 prescribes for a threshold at
operating size.

**Caveat 2 — assert the invariant that actually breaks, because 256 KB does not imply it.**
*Front matter + the K newest records must fit one read.* Today satisfied with ~40 KB of slack, but it
is a **separate condition**, it is what Phase 3A depends on, and the trimmer already parses records
so it is cheap. **The failure mode it guards is front-matter growth, not record accumulation** — the
`HANDOFFS.md` archive table gains a row per trim, and under this proposal trims get rarer, so the
risk falls rather than rises. Assert it anyway: a condition nobody checks is how this campaign began.

---

## 4. Class B — where the proposal does not hold, and the gap it exposes

**Truncation is only harmless when the part you need is at the top.** Class B files have no record
ordering that guarantees that. A backlog's bottom items are as live as its top ones; a truncated read
loses open work, and the reader is told *that* something was cut but not *what*.

**Under a 256 KB-only rule these go unwarned while truncating today** [M]:

| file | bytes | tokens | B/token | × the read cap |
|---|--:|--:|--:|--:|
| `wsfct/BACKLOG.md` | 252,089 | **98,966** [M] | 2.5472 | **3.96×** |
| `model_project_constructor/SESSION_NOTES.md` | 149,569 | **55,791** [M] | 2.6809 | **2.23×** |
| `nprcgenekeepr/BACKLOG.md` | 121,672 | **41,817** [M] | 2.9096 | **1.67×** |
| `model_project_constructor/BACKLOG.md` | 72,493 | ~28,400 [D] | — | ~1.14× |

> **⚠ THESE FIGURES REPLACE A DRAFT THAT CARRIED A CLASS A RATIO ONTO CLASS B CONTENT, and the
> correction is this campaign's own lesson landing on the plan that states it.** The first draft
> multiplied Class B byte counts by **2.4 B/token** — measured on *ledger* content — and published
> 4.2× / 2.5× / 2.0×. Measured directly, **Class B content is LESS dense than Class A**
> (2.5472–2.9096 against 2.2705–2.5150), so the draft **overstated every multiple by 6–20%**.
> The finding is unchanged — all four are over the cap and the class distinction holds — but the
> numbers were wrong, in the direction of making the case look stronger than it is.
> **A ratio is a property of its content type; it does not transfer between classes, including
> between the two classes this plan exists to separate.**
>
> **One consequence worth keeping:** `MIN_BYTES_PER_TOKEN = 2.27` is set by **Class A** content
> (`vscode_quarto_ext/HANDOFFS.md`, 2.2705). For a guard covering both classes that is the
> conservative direction — it fires early on Class B rather than late — which is the behaviour a
> guard should have, and it should be stated in the code comment rather than left to be rediscovered.

### 4.1 The remedy gap — the part that is not a threshold question

**A guard must name a remedy its reader can reach.** Class B's do not.

- **`SESSION_NOTES.md`: no documented remedy anywhere in the distributed corpus** [M]. Four of five
  repos hold one over the cap; two are past the hard refusal. The framework warns and stops.
- **`BACKLOG.md`: one remedy, and Learning #26 bounds it.** `BOOTSTRAP.md:144-151` says split out
  completed work — correct, and a *bootstrap-time* instruction, not ongoing maintenance. **L#26,
  earned on this repo's own backlog at S89, records that archiving everything finished recovered
  33% and did not reach the ceiling, because the open items alone were 1.04× the budget.** Its rule:
  *sum the part you are NOT allowed to remove and compare THAT to the ceiling first.*
- **The remedy that actually worked here is not distributed.** This repo split
  `docs/planning/BACKLOG.md` into a one-row **index** plus `BACKLOG-DETAIL.md`, with a runnable
  losslessness proof (`BACKLOG-DETAIL.md.verify.sh`, C1–C5). That pattern is **fork-only**; no
  adopter is told it exists.

**So Class B's real question is a policy one** — *how much live work may an artifact hold?* — which no
threshold answers. This plan's position: **say so in the row.** A guard that names an unreachable
remedy is worse than one that names none, and better than either is one that says *"this is a
structural split, here is the worked example."*

---

## 5. `DEFAULT_BUDGET_BYTES` must be decided in the same change, or the proposal is inert

`Trigger.fires` is `read_fires or byte_fires`, and `byte_fires` is `size > DEFAULT_BUDGET_BYTES`
(**65,536**). **A 256 KB read trigger changes nothing while a 64 KiB byte trigger fires first.**

**The evidence for and against, stated so the operator decides on it rather than on the constant's
age.** *Against keeping it at 65,536:* it claims **context tax**, and S112 measured that cost as paid
**per read-span** — 1,797 partial reads against 1 whole [M] — not per file size; `.context-budget.json`
already says of it, in its own words, *"MAX_BYTES 65,536 IS RETAINED BUT NO LONGER THE OPERATIVE
GUARD"*; and the guard that does bind, `RECORD_BUDGET_BYTES`, is **canonical-only** and reaches no
adopter. *For keeping it:* it encodes **G1, the operator's stated goal**, and it is the number
BL-9/BL-32/BL-36/S87/S89 have all measured against — retiring it invalidates a lot of recorded work
as a baseline. **This plan does not decide it. §7 option C1 is a decision, not a derivation.**

---

## 6. Evidence-based inventory (MANDATORY)

Derived from greps, not architectural memory. **Live sites only**; `docs/archive/**` and every frozen
record are excluded and must not be repaired (FM #22). Distribution read off `bin/_manifest.py`'s
**SOURCE** column by importing `DISTRIBUTION`, never by grepping a bare filename.

| site | what changes | distribution |
|---|---|---|
| `starter-kit/methodology_trim.py:108-142` | the constants block; a new fire/stop pair if C1 adopted | **TRACKED** |
| `…:780-811` `Trigger` | `read_fires` threshold; `stops()` if the byte arm moves | **TRACKED** |
| `…:1711-1721` `--check` output | the `TRIGGER_READ` / `TRIGGER_BYTES` rows | **TRACKED** |
| `starter-kit/methodology_dashboard.py:296-302` (+ `tools/` twin) | the same constants, pinned to the trimmer by test | **TRACKED** |
| `…:338` `READ_CAP_WATCHED` | **the population**, if it is split by class | **TRACKED** |
| `…:2097-2140` `collect_trim_metrics` | per-class branching; the remedy sentence | **TRACKED** |
| `…:3045-3072` the D4(b) risk rows | per-class thresholds and per-class remedy | **TRACKED** |
| `starter-kit/context_budget.py:371-392` `ledger_dimension` | unaffected unless ceilings move | **TRACKED** |
| `starter-kit/context-budget.json` | `SESSION_NOTES.md`'s `max_lines` 400 / `max_bytes` 120,000 | **SEED** ⚠ |
| `starter-kit/BOOTSTRAP.md:144-151` | where a Class B remedy would be documented | **TRACKED** |
| `tools/test_methodology_dashboard.py` | `TestD4ReadCapTruncation`, `TestS38TrimTriggerRow` | canonical-only |
| `tools/test_methodology_trim.py` | `TestTrigger` | canonical-only |

**⚠ `starter-kit/context-budget.json` is a `SEED`.** `bin/sync:225-230` writes a SEED **only when the
destination is absent and never overwrites it**, so any change there reaches **future adopters only** —
the same defect class as BL-46/47/48, and it must be stated in the implementing session's receipt.

---

## 7. Options

Independent unless noted. **Cost** in sessions.

| | option | mechanism | buys | costs / breaks |
|---|---|---|---|---|
| **A1** | **Split the watched population by class** | `READ_CAP_WATCHED` becomes two sets with two thresholds: Class A on `READ_REFUSE_BYTES`-derived, Class B on `READ_CAP_BYTES`. | Each guard finally claims something true of the files it watches. Ends the dedup by making the rows *different*, not by deleting one. | ~1 session. Fleet-visible: Class A rows drop, Class B rows stay. A canonical test must assert class membership against `LEDGERS`, not restate it. |
| **A2** | **Class A trigger: fire >192 KB, cut to 96 KB** | Replace the read arm's threshold for the two ledgers. | The operator's proposal, with the cliff margin of §3. Trims become rare and each buys a lot. | ~⅓ session **if** C1 is settled; **inert without it** (§5). |
| **A3** | **Assert the prefix invariant** | `front + K newest records ≤ READ_CAP_BYTES`, checked where the records are already parsed. | Guards the thing that actually breaks, which no size threshold implies. | ~⅓ session. Needs K defined — Test 34's floor is 3; Phase 3A needs 1. |
| **B1** | **Give Class B a reachable remedy** | Document the index+detail **structural split** in `BOOTSTRAP.md`, citing this repo's own worked example and its `.verify.sh`; have the row name it. | Closes the §4.1 gap. Turns a warning into an action. | ~1 session, and it is **doc work on a TRACKED file**, so it reaches every adopter. |
| **B2** | **Say the honest thing when no remedy exists** | For `SESSION_NOTES.md`, the row states the policy question rather than implying archiving fixes it (L#26). | Stops shipping a guard whose remedy cannot reach. | ~⅓ session. Prose only. |
| **C1** | **Decide `DEFAULT_BUDGET_BYTES`** | Retire it, raise it to the Class A trigger, or keep it and accept that A2 is inert. | Unblocks A2. | **Judgment, not derivation.** Retiring it orphans a baseline five recorded items measured against. |
| **D** | **Narrow `READ_CAP_WATCHED` to drop the two ledgers** | BL-52's literal reading. | Simplest. | **Rejected here:** the row reports a real property that stays true however rarely anyone reads the file, and Class A is where the trimmer *can* act. Dropping them removes the only signal that reaches an adopter's dashboard. |

---

## 8. Recommendation

**A1 → (A2 + C1 together) → A3 → (B1 + B2), in that order, as three sessions.**

- **A1 first**, because every other option needs the classes named. It changes no threshold and
  cannot degenerate anything.
- **A2 and C1 in the SAME session**, for the reason §5 gives: separately, A2 ships a trigger that
  never fires. This is the same coupling that made Phase B's §3 dangerous, one level over — a
  threshold whose meaning depends on a constant nobody moved.
- **A3 next**, once the classes exist to attach it to.
- **B1 + B2 last** and together: they are the adopter-facing half, they are prose, and B1 without B2
  documents a remedy for one Class B file while the other still has none.

**What I am least confident about.** Whether **192 KB / 96 KB** is right, or merely defensible. It is
judgment calibrated on one repo's record sizes; an adopter whose receipts are half the size gets
twice the records per trim and may want a different pair. **The honest form is a per-file setting with
this default**, exactly as `DEFAULT_BUDGET_BYTES` already is — and that is a reason to keep C1's
machinery rather than delete it.

---

## 9. Phases

Each is **one session. Close out when its criterion passes. Do not bundle** (except A2+C1, which
§8 requires be bundled).

### The surface, stated once because it governs every phase

> **Unchanged from Phase B and still binding: no test in this repository can falsify a read-cap
> claim.** Nothing here invokes the agent's `Read` tool. A green suite is evidence that nothing
> *else* broke. **Each phase re-runs Appendix A in the implementing session** and pastes the output
> into its receipt.

### Phase C1 — split the population by class
- **Do:** `READ_CAP_WATCHED` becomes class-aware. Class membership **asserted against the trimmer's
  `LEDGERS` table**, not restated (the existing `test_grammars_agree_with_the_trimmer_config_table`
  is the pattern).
- **DONE:** every watched name resolves to exactly one class; a canonical test fails if a name is
  added to `LEDGERS` without moving class; the two `docs/**/BACKLOG.md` locations are explicitly
  dispositioned (they have no protocol basis — keep by analogy, or drop, but **decide it**).
- **Verify:** `bash bin/tests.sh` row-for-row against a worktree control · the three Python suites ·
  twins byte-identical, **mirrored last** · the fleet re-scanned read-only, rows tabulated by class.

### Phase C2 — the Class A trigger, and `DEFAULT_BUDGET_BYTES` with it
- **Do:** A2 and C1 in one commit. Re-derive the fire/stop pair; state the hysteresis as judgment.
- **DONE:** `--check` fires on neither ledger at today's sizes **and** demonstrably fires on a
  synthetic file above the new threshold; `choose_cut` returns a real cut at both ledgers'
  densities (the §3-style table recomputed and pasted); **no ledger can stop above
  `READ_REFUSE_BYTES`**.
- **⚠ Do not ship A2 without C1.**

### Phase C3 — the prefix invariant, and the Class B remedy
- **Do:** A3, B1, B2.
- **DONE:** the prefix assertion exists and has an edge test on both sides; `BOOTSTRAP.md` documents
  the structural split with a worked example; the Class B row names a remedy a reader can reach, or
  states plainly that the question is a policy one.

---

## 10. Here be dragons

1. **A2 is inert without C1** (§5). The byte arm fires first. This is Phase B's §3 coupling
   recurring one level over: a threshold whose effect depends on a constant nobody moved.
2. **`starter-kit/context-budget.json` is a SEED.** A fix there reaches **future adopters only**;
   every bootstrapped project keeps the old ceilings forever. Do not close this work believing the
   fleet is fixed (dragon 9 of the predecessor plan, still live).
3. **The two dashboard twins must stay byte-identical.** Mirror **last**, then re-run; any number
   recorded before the mirror is false without anything failing (S37).
4. **The pinning test now pins BOTH INPUTS, not the product.** Adding a per-class threshold means
   adding to that test, not replacing it — and it still only keeps the two copies *consistent*, not
   *correct*.
5. **Class B has no trimmer, so a Class B row can only ever advise.** Resist the pull to make the
   trimmer swallow `BACKLOG.md`: `ledger-trimmer-design.md` §3.3 settled that on evidence — zero
   `###` headings, no uniform delimiter, and one open item living inside another's paragraph.
6. **Widening the trimmer's `LEDGERS` would silently move a file's class** under A1. Whatever
   asserts class membership must fail on that, not follow it.
7. **A guard can be correct and not worth acting on** (S112's finding, BL-52 third addendum). Before
   any new row is added, ask what a reader is expected to *do* — and whether measurement supports it.
8. **`HANDOFFS.md` in this repo is over both its ceilings by adjudication, not neglect.** A Phase C
   session that "tidies" it up has undone a decision, not done housekeeping. Read BL-52's third
   addendum first.

---

## 11. Explicitly not in scope

`RECORD_BUDGET_BYTES` and the record-budget plan's Phase 2/3 (**the highest-value unstarted work in
this area, and a different campaign**) · `HEADER_RESERVE_BYTES` · Test 34's retention floor ·
BL-42/43/44 · **BL-45** (the `FRAMEWORK_LEARNINGS.md` ceiling — an operator decision, now blocking
Phase 3C for a fifth session) · BL-46(2)/47/48/49 · issue #75's unsent PR · the predecessor plan's
§11.2 cross-repo adopter remediation · **any outward-facing action whatsoever.**

---

## Appendix A — reproduction

```sh
# --- the three delivery modes. Read each with the Read tool and record what comes back.
#     An over-cap explicit `limit` ERRORS with the span's exact token count and NO content --
#     that error is a free, exact token meter, and it is how every ratio below was measured.
#     A: >2,000 lines but small          -> expect WHOLE (lines do not bind)
#     B: few lines but large             -> expect PARTIAL + banner
#     C: >256 KiB, DEFAULT parameters    -> expect "exceeds maximum allowed size (256KB)", zero content
#     control for C: the same file with an explicit small offset/limit -> returns content,
#                    proving the refusal is on the UNBOUNDED read, not on the file.

# --- B/token for a real file, without paying for its content: double it, read the doubled
#     file with a spanning limit, halve the reported token count. Linear to 0.004% (S112).
cat FILE FILE > /tmp/x.txt        # then Read /tmp/x.txt with offset=1 limit=<its line count>

# --- class membership, from the two independent facts, never from memory
python3 -c "import sys;sys.dont_write_bytecode=True;sys.path.insert(0,'starter-kit');\
 import methodology_trim as t, methodology_dashboard as d;\
 print('A:',sorted(t.LEDGERS));print('B:',sorted(set(d.READ_CAP_WATCHED)-set(t.LEDGERS)))"
grep -nE 'SESSION_NOTES|BACKLOG' starter-kit/SESSION_RUNNER.md starter-kit/SAFEGUARDS.md
grep -nEi 'in full|not skimmed' starter-kit/SESSION_RUNNER.md      # -> :13 SAFEGUARDS.md only

# --- the fleet, by class, read-only. collect_all() reaches no writer (verify by call graph
#     before running it anywhere you do not own).
for R in ../wsfct ../nprcgenekeepr ../vscode_quarto_ext ../model_project_constructor; do
  for F in CHANGELOG.md HANDOFFS.md SESSION_NOTES.md BACKLOG.md docs/planning/BACKLOG.md; do
    [ -f "$R/$F" ] && wc -c "$R/$F"; done; done

# --- the remedy gap: does ANY distributed file say what to do about an oversized Class B file?
python3 -c "import sys;sys.dont_write_bytecode=True;sys.path.insert(0,'bin');\
 from _manifest import DISTRIBUTION;print([r[0] for r in DISTRIBUTION if r[0].endswith('.md')])"
grep -nE 'BACKLOG|SESSION_NOTES' starter-kit/BOOTSTRAP.md | grep -iE 'split|archiv|trim'

# --- distribution, read off the SOURCE column (never the bare filename)
grep -nE '^\s*\("starter-kit/' bin/_manifest.py

# --- twins and checkers
diff -q starter-kit/methodology_dashboard.py tools/methodology_dashboard.py
bash bin/tests.sh ; python3 bin/check-links ; python3 bin/check-learnings ; python3 bin/check-handoff
python3 tools/test_methodology_trim.py ; python3 tools/test_methodology_dashboard.py
python3 tools/test_context_budget.py       # run these from a FOREIGN CWD: bin/tests.sh does
```
