# A file-management system for the methodology — full scope

**Status: DRAFT. The plan is this session's (S117) deliverable; nothing in it is implemented.**
Six operator decisions in §6 are unanswered and gate Phase 1.

> **Why this plan exists, in the operator's words.** Asked to choose among BL-45's four re-costed
> options, the operator declined the choice and said instead: *"perhaps we need a full scope plan
> made because we have been solving localized problems and not solving for making methodology as
> efficient and effective as possible from the standpoint of file management."*
>
> **The record supports that characterisation.** Every prior effort here is a point fix on one
> artifact: BL-19, BL-22, BL-32, BL-37, BL-42–BL-52, [`read-cap-phase-c-plan.md`](read-cap-phase-c-plan.md)
> Phases A–C, [`record-budget-reduction-plan.md`](record-budget-reduction-plan.md),
> [`ledger-trimmer-design.md`](ledger-trimmer-design.md),
> [`framework-context-cost-plan.md`](framework-context-cost-plan.md). Each is defensible alone.
> Together they produced a system in which **the guards sit on the files that can afford to grow and
> are absent from the files that cannot** (§4 F2), and in which **the single automated remedy makes
> the repository larger every time it runs** (§4 F3).

> **This plan is an instance of the problem it addresses**, and says so rather than being caught at
> it. `docs/planning/` is 31 files / 865,895 B — larger than the entire distributed payload — with
> no ceiling and no retirement rule. This document is file 32. **Its declared budget is 65,000 B**,
> chosen so it is deliverable in one agent read at prose density; §7 Phase 4 owns the directory's
> retirement rule, and this file is in its population like any other.

---

## 1. The two hard limits everything here is measured against

| limit | value | behaviour past it |
|---|---:|---|
| single agent `Read` | **25,000 tokens** | returns a truncated **ordered prefix** — the top of the file |
| hard refusal | **262,144 B** | returns **no content at all** |

**Bytes-per-token is a property of content type, not a constant** — so "25,000 tokens" is a
different byte count for every file. Measured this session with the no-content token meter (double
the file, read the doubled file with a spanning `limit`, halve the reported count — the over-cap
error reports exact tokens and costs nothing):

| file | bytes | tokens | B/token | its own cliff | one read? |
|---|---:|---:|---:|---:|---|
| `starter-kit/SESSION_RUNNER.md` | 54,363 | 19,172 | 2.8355 | 70,887 B | yes, 5,828 tok spare |
| `ITERATIVE_METHODOLOGY.md` | 68,240 | 23,432 | 2.9123 | 72,808 B | yes, **1,568 spare** |
| `starter-kit/FRAMEWORK_LEARNINGS.md` | 72,646 | 23,842 | 3.0469 | 76,173 B | yes, **1,158 spare** |
| **R1 aggregate (the mandatory read set)** | **80,813** | **28,832** | 2.8029 | 70,072 B | **NO — over by 3,832** |

**⚠ Two instruments disagree by up to 25%, and the plan must pick one (decision D5).**
`starter-kit/methodology_trim.py:120` sets `MIN_BYTES_PER_TOKEN = 2.27`, *the floor of a measured
2.2705–3.0300 band*, giving `READ_CAP_BYTES = 56,750`. That floor is correct for a file whose
density is unknown and **wrong for one that has been measured**: it puts `SESSION_RUNNER.md` at
2,387 B of headroom when its own density gives 16,524 B — a 6.9× difference. A session that treats
the floor as a measurement will make an urgent, fleet-shipping edit to the framework's most
load-bearing distributed file on a number wrong by 14,142 B.

---

## 2. The delivery classes — the organising idea

Size cost is determined by **how a session receives a file**, not by how large it is. Four classes,
each with a different cost function:

| class | definition | cost of growth | members |
|---|---|---|---|
| **R1** | read in full, **every** session | paid every session; the aggregate must fit one read | `CLAUDE.md`, `starter-kit/SESSION_RUNNER.md`, `starter-kit/SAFEGUARDS.md` |
| **R2** | read in full, **sometimes** | paid on demand; each file must fit one read | `starter-kit/FRAMEWORK_LEARNINGS.md`, `ITERATIVE_METHODOLOGY.md`, one `workstreams/*.md`, `docs/planning/BACKLOG.md` |
| **R3** | read only at a **frontier / newest record** | nearly free | `CHANGELOG.md`, `HANDOFFS.md` |
| **R4** | never read by the session protocol | free | `README.md`, `HOW_TO_USE.md`, `docs/RELEASE_HISTORY.md`, `docs/archive/**`, `docs/tutorials/**` |

R3's cheapness is not an assumption — it is the contract those files state and their readers
implement: `bin/check-handoff` validates only the newest receipt, Phase 0 reconcile is
frontier-based, and `HANDOFFS.md:14` says so outright.

**The ordering, not the size, decides whether truncation hurts.** A truncated read returns the
**top** of the file:

| file | record order | truncation drops | harm |
|---|---|---|---|
| `CHANGELOG.md`, `HANDOFFS.md` | newest-first | the **oldest** records | harmless — deliberate |
| `starter-kit/FRAMEWORK_LEARNINGS.md` | **oldest-first** (rows #1 → #44) | the **newest** learnings | **harmful** |
| `docs/planning/BACKLOG-DETAIL.md` | **oldest-first** (BL-11 → BL-52) | the **newest** items — BL-49…BL-52 | **harmful** |
| `ITERATIVE_METHODOLOGY.md` | prose, front-to-back | the closing sections | **harmful** |

The framework's truncation-safety argument is encoded **only** for the two Class A ledgers — which
are exactly the two files where truncation was already harmless.

---

## 3. Evidence-based inventory

Produced by a 6-census / 12-verifier / 1-critic read-only workflow plus direct measurement. Every
figure below was reproduced by a command; §10 has the reproductions.

### 3.1 Coverage — which guard sees which file

| artifact | bytes | class | `.context-budget.json` | trimmer `LEDGERS` | dashboard `READ_CAP_WATCHED` | per-record/row guard |
|---|---:|---|:--:|:--:|:--:|:--:|
| `CLAUDE.md` | 11,064 | R1 | ✅ 18,600 | ✗ | ✗ | ✗ |
| `starter-kit/SESSION_RUNNER.md` | 54,363 | R1 | **✗** | ✗ | ✗ | ✗ |
| `starter-kit/SAFEGUARDS.md` | 15,386 | R1 | **✗** | ✗ | ✗ | ✗ |
| `starter-kit/FRAMEWORK_LEARNINGS.md` | 72,646 | R2 | ✅ 73,728 | ✗ | **✗** | ✅ row 1,500 B |
| `ITERATIVE_METHODOLOGY.md` | 68,240 | R2 | **✗** | ✗ | ✗ | ✗ |
| `docs/planning/BACKLOG.md` | 30,786 | R2 | ✅ 65,536 | ✗ | ✅ Class B | ✗ |
| `docs/planning/BACKLOG-DETAIL.md` | 116,749 | R2 | **✗** | ✗ | ✗ | ✗ |
| `CHANGELOG.md` | 98,811 | R3 | ✅ 65,536 | ✅ | ✅ Class A | ✗ |
| `HANDOFFS.md` | 128,081 | R3 | ✅ 65,536 | ✅ | ✅ Class A | ✅ record 12,288 B |
| `docs/archive/**` (35 files) | 2,188,360 | R4 | **✗** | ✗ | ✗ | ✗ |
| `bin/tests.sh` | 174,172 | — | **✗** | ✗ | ✗ | ✗ |
| `docs/images/dashboard-detail.png` | 424,186 | — | **✗** | ✗ | ✗ | ✗ |

Five paths carry a ceiling. **Three of them are R3 or a lightly-read R2 — the classes that can
afford to grow. Neither R1 file without `CLAUDE.md` carries one.**

### 3.2 The fleet — 11 real adopters on this machine, measured read-only

| adopter | CLAUDE | RUNNER | SAFEG | mandatory-read B | est. tokens | guard |
|---|---:|---:|---:|---:|---:|---|
| `airqino` | 3,182 | 40,474 | 11,961 | 55,617 | 19,843 | none |
| `chat_verification` | 20,583 | 52,386 | 15,386 | 88,355 | **31,523** | budget |
| `church_growth` | 22,867 | 57,400 | 15,386 | 95,653 | **34,126** | none |
| `claude_work` | 2,725 | 59,801 | 15,386 | 77,912 | **27,797** | none |
| `dalia_martinez_funeral` | 16,299 | 57,400 | 15,386 | 89,085 | **31,783** | none |
| `feedback-loop-comparison` | 9,135 | 23,319 | 9,673 | 42,127 | 15,030 | none |
| `model_project_constructor` | 27,600 | 25,643 | 8,018 | 61,261 | 21,856 | none |
| `mts-system` | 21,117 | 49,465 | 15,386 | 85,968 | **30,671** | none |
| `nprcgenekeepr` | 38,692 | 52,386 | 15,386 | 106,464 | **37,984** | none |
| `vscode_quarto_ext` | 16,607 | 54,363 | 15,386 | 86,356 | **30,810** | budget |
| `wsfct` | 43,956 | 54,363 | 15,386 | 113,705 | **40,567** | budget |

**8 of 11 exceed the single-read limit**, and the finding is robust to the density assumption —
the same 8 are over at 2.8029 B/tok *and* at 3.0469, the most token-sparse density measured
anywhere in this repo. **The adopter token column is an extrapolation from a measured ratio, not a
measurement** (only the canonical 28,832 figure was metered directly); the *membership* of the
over-set is what is robust, not the individual numbers.

**3 of 11 have any size instrument.** `bin/check-handoff` — which the framework's own analysis calls
the operative guard for `HANDOFFS.md` — is canonical-only, so **10 of 11 declined a manual copy
step**: measured evidence that "ship a canonical-only tool" is not a delivery mechanism. Ten files
across five adopters are already past the 262,144 B refusal boundary.

---

## 4. The seven structural findings

Each is a property of the **system**, not of one file. Each was reproduced by command.

### F1 — The mandatory read set exceeds one read, and nothing sums it

`CLAUDE.md` + `SESSION_RUNNER.md` + `SAFEGUARDS.md` = **80,813 B = 28,832 tokens = 115.3% of the
25,000-token cap**, metered directly. It would have to shed **10,741 B** to fit.

**No per-file ceiling can ever catch this, because the failure is in a sum that nothing sums.**
`starter-kit/context_budget.py:888-898` computes exactly one class total and hardcodes which class:

```python
resident = sum(r.get("bytes", 0) for r in results if r["class"] == "resident")
tot = cfg["classes"]["resident"]
```

`read-mandated` exists as a per-file *label* with no total. Adding a `read-mandated` total to the
config today would be **silently ignored** — the key is never read. And the `resident` class is
degenerate: it has exactly one member (`CLAUDE.md`), so its total can never differ from its
per-file ceiling.

### F2 — The guards are on the files that can afford to grow

The two files reported red today — `CHANGELOG.md` (150.8% of ceiling) and `HANDOFFS.md` (195.4%) —
are R3: read at a frontier, newest-first, truncation harmless. Phase C2 already concluded their real
threshold is 196,608 B and `methodology_trim.py --check` fires on neither.

The files with *no* ceiling include both un-`CLAUDE.md` R1 files and two oldest-first R2 files whose
truncation drops their newest content. **The ceiling distribution is close to inverted with respect
to the harm distribution.**

### F3 — The only automated decay mechanism is net-additive by 1.79×

Full byte accounting of the most recent trim, commit `9038e40` (2026-08-26):

| file | before | after | delta |
|---|---:|---:|---:|
| `HANDOFFS.md` | 66,614 | 44,468 | **−22,146** |
| `docs/archive/HANDOFFS-through-2026-08-25.md` | 0 | 22,893 | +22,893 |
| `…-2026-08-25.md.verify.sh` | 0 | 16,011 | +16,011 |
| `CHANGELOG.md` (forced by the pre-commit ledger hook) | 58,774 | 59,542 | +768 |
| | | **net** | **+17,526 B** |

**To relieve 22,146 B the repository grew 17,526 B.** The proof script is **70%** of the shard it
certifies, and the proof tier's per-trim overhead has itself grown 7,842 → 16,011 B as the tool
matured. `docs/archive/` is now **2,188,360 B — 35.0% of the tracked repository** — has a ceiling in
no instrument, and has never had a file removed. One shard, `HANDOFFS-through-2026-08-09.md`
(382,071 B), is past the 262,144 B refusal: **the documented escape hatch to older receipts returns
no content to any agent that opens it.**

### F4 — The framework has a create verb and no retire verb

In **693 commits, exactly one tracked file has ever been deleted** — `LICENSE`, at `d207d1c`
(2026-03-09), and it was re-added at `31fdb79` as a mistake. Every plan, audit, tutorial, shard,
learning row and receipt is permanent by default, and nothing has ever tested otherwise. This is the
structural form of the degradation-table row the runner already publishes:

> *"A close-out appends to a mandated-read file, and no close-out has ever removed anything from one
> | The protocol has a compounding term and no decay term"* — `starter-kit/SESSION_RUNNER.md`

### F5 — Nothing mechanically enforces any ceiling

There is no CI. `core.hooksPath=.githooks`, whose `pre-commit` enforces the **CHANGELOG ledger**
gate and contains **zero size logic** — and that hook *forces growth*, since every commit touching
tracked content must also append to `CHANGELOG.md`. `context_budget.py` has a `--precommit` mode
that **is not wired to anything**. Every size guard in the system fires only when a human types the
command. FM #28 says to *"treat exceeding it as a defect rather than housekeeping"*; the instrument
has recorded that defect on `HANDOFFS.md` in 53 of 79 recorded runs and nothing has ever acted on
it. This is verbatim the runner's own row: *"A health check has reported the same finding for
several consecutive sessions and nothing has changed → Do not add a second report. Add a gate."*

### F6 — Two artifact classes are ungoverned and one of them is not a file

- **The archive tier** (F3) — the destination of the only remedy.
- **`docs/planning/`** — 31 files, 865,895 B, larger than the whole distributed payload, no ceiling,
  no retirement rule. `BACKLOG-DETAIL.md` (116,749 B) is the fastest-growing markdown in the repo,
  is oldest-first, and already truncates away BL-49…BL-52 — the newest and most active items,
  including the read-cap work itself.
- **Command output is a read artifact with zero possible decay.** Phase 0 step 6 mandates
  reconciling `CHANGELOG.md` against `git log`. `git log --oneline` is **56,856 B** — it crossed
  `READ_CAP_BYTES` (56,750) this week. You cannot archive git history.

### F7 — The instrument and the ceilings are unsettled

Three live ceilings — 65,536 (three `.context-budget.json` entries, now a fork-local leftover),
73,728 (`FRAMEWORK_LEARNINGS.md`), 196,608 (`DEFAULT_BUDGET_BYTES` after Phase C2) — and **no rule
says which is authoritative**. Two densities (2.27 floor vs measured per-file) differ by up to 25%
(§1). `CEILING_BYTES = 65536` at `bin/check-handoff:662` is a fourth independent copy of the value —
and grepping the **value** rather than the name finds the literal `65536` at **20 sites across 8
files** (`.context-budget.json` ×7, `bin/check-handoff` ×5, `starter-kit/context_budget.py` ×3, both
dashboard twins, `bin/check-learnings:88`, `starter-kit/methodology_trim.py:52`). Nothing keeps any
of them consistent, and `bin/check-learnings:88` is already stale — it still defends the row budget
as *"a quarter of the file's remaining headroom against its 65,536 B ceiling"* when that ceiling
became 73,728 at S114 and the real headroom is 1,082 B.

### Also found, recorded, and NOT fixed by this session

Real defects outside this plan's scope, handed forward rather than lost:

- **5 of 16 shipped `.verify.sh` losslessness proofs exit 1** — BL-36's four legacy v1.1.1 proofs,
  **plus a new current-generation v1.3.0 failure**: `HANDOFFS-through-2026-08-25.md.verify.sh`,
  `L2 FRONT MATTER lost 1 line(s)`, caused by the hand-maintained *"Archived shards — N trims, M
  receipts"* sentence that is not in `spec.regenerated` and that the next trim edited.
- **`bin/check-learnings` can be silently disarmed by one blank line.** A blank line inside the
  Learnings table ends the parsed region with no finding: the checker prints
  `OK — 21 Learning row(s), contiguous 1..21; all citations resolve` at **exit 0** with 43 rows
  present. On today's file only an *incidental* citation catches it.
- **The "out of ascending order" guard is dead code** (nested inside the contiguity-failure branch);
  reversing all 43 rows returns exit 0.
- **Four `[[N]]` cross-references** in rows #32/#33/#36/#38 are invisible to `CITATION_RE`.
- **The seed `starter-kit/context-budget.json` declares `LEARNINGS.md`**, which no manifest dest
  ever installs; adopters receive `FRAMEWORK_LEARNINGS.md` and it is declared nowhere.
- **BL-45's citation figure is an undercount**: *"five, in two files"* at N=10 is **9, in 4 files**,
  measured by running the checker. It omitted the table's own 18 self-citations and counted a `.py`
  the sweep excludes. **Its byte columns, by contrast, still reproduce exactly** — this session's
  own claim commit was wrong to say every figure in it is stale, and that is corrected here.

---

## 5. What this plan supersedes, absorbs, and leaves alone

**Absorbed** — these become phases here rather than independent items: BL-37 (this repo ships a size
gate and does not run it on itself), BL-45 (the learnings ceiling — its remedy is Phase 4's first
instance, not a point fix), BL-47 (seed omits the ledgers), BL-32 (LEDGERS covers only two files).

**Left independent** — real defects with their own causes, not file-management design: BL-36/BL-49/
BL-50 (proof correctness), BL-42/BL-43/BL-44, BL-46, BL-48, BL-51 Phase C3, BL-52.

**Not superseded**: [`ledger-trimmer-design.md`](ledger-trimmer-design.md) §3.3's evidence that
`BACKLOG.md` cannot be trimmed still holds and this plan does not reopen it.

**⚠ Read prior plans' status from `git log`, not from their headers.** Two of nine planning
documents contradict their own bodies about what shipped.

---

## 6. The six decisions only the operator can make

**Phase 1 does not start until these are answered.** Each is recorded in `CHANGELOG.md` as its own
entry, the way S116 recorded its three. None is derivable from measurement — that is why they are
here and not in §4.

| | decision | why it cannot be derived |
|---|---|---|
| **D1** | **What is the framework's target cost per session?** A number for "a session should pay ≤ N tokens before it starts work." | None exists anywhere in the repo. Without it every ceiling is arbitrary and every raise is defensible — which is how `FRAMEWORK_LEARNINGS.md` went 60,000 → 65,536 → 73,728 with no argument available against a third raise. |
| **D2** | **How many of each thing should the framework carry?** 43 learnings? 28 failure modes? 31 plans? | BL-45's own close-out reached this and stopped: *"The real question is policy — how many learnings should the framework carry before old ones retire — and no ceiling answers it."* |
| **D3** | **On what semantic event does an artifact retire?** Not "when it is big" — that is the level question, already answered badly. | F4: the framework has never retired anything, so there is no precedent to read the rule off. |
| **D4** | **Is "undeliverable in one Read" a fault or an accepted operating state?** | The trimmer has already answered *not a fault* in code (Phase C2); `.context-budget.json` still answers *fault*. Both ship. Nobody has adjudicated. |
| **D5** | **Are ceilings denominated in the conservative 2.27 B/tok floor or each file's measured density?** | §1: they differ by up to 25%, and by 6.9× in headroom terms for `SESSION_RUNNER.md`. Both are defensible; they are answers to different questions. |
| **D6** | **Does the framework have jurisdiction over adopter-owned files, and what is the delivery mechanism?** | `PROJECT_LEARNINGS.md` is 2,678,328 B at one adopter and is in no manifest. 10 of 11 adopters declined the manual `bin/check-handoff` copy. Shipping a canonical-only tool is measurably not delivery. |

**A seventh, smaller decision rides with Phase 1:** whether `SESSION_RUNNER.md` and `SAFEGUARDS.md`
get ceilings at all. Adding them **constrains future canonical work and ships upstream** — the
`_deliberate_exclusions` note in `.context-budget.json` declined it once already on exactly that
ground (FM #17). It is the operator's, not a session's.

---

## 7. Phases

**Every phase is ONE session and closes out at its own STOP.** Phases are vertically sliced: each
ships a working end-to-end capability, never a horizontal layer (FM #25). The dependency is strict —
Phase 1 needs §6's answers; Phases 2–5 need Phase 1's vocabulary.

### The surface, stated once because it governs every phase

> **No test in this repository can falsify a read-cap claim** — nothing here invokes the agent's
> `Read` tool, so a green suite is evidence that nothing *else* broke. Every phase that asserts a
> read-delivery property **re-runs the §10 token meter in the implementing session and pastes the
> output into its receipt.** The fleet surface is read-only measurement of the eleven sibling repos;
> **no phase may write to an adopter repository**, and no phase's DONE criterion may be demonstrated
> there.

---

### Phase 1 — The read-set gate

**Do.** Teach `starter-kit/context_budget.py` to total **any** declared class, not only `resident`
(`:888-898`). Declare a `read-mandated` class total in `.context-budget.json` set from D1, and add
entries for `starter-kit/SESSION_RUNNER.md` and `starter-kit/SAFEGUARDS.md` denominated per D5.

**DONE.** `python3 starter-kit/context_budget.py` prints an **R1 aggregate row** naming its members
and its ceiling; it exits non-zero when the aggregate is over **even though every member is under**;
and a synthetic config with a third class totals correctly, proving the generalisation rather than a
second hardcode. The pre-existing `resident` total still fires unchanged.

**Verify.**
```sh
python3 starter-kit/context_budget.py > /dev/null 2>&1; echo $?   # bare; never through a pipe
python3 -m unittest discover -s tools -p 'test_context_budget*.py'
bash bin/tests.sh          # ~7 min, background it; EXITS 1 EVEN WHEN GREEN (Test 9's 404)
```
Row-for-row diff of `bin/tests.sh` output against a worktree control, both populations asserted
non-empty.

**Surface.** Canonical repo only. **`context_budget.py` is a TRACKED manifest source** — this ships
to every adopter at their next `bin/sync`. The `.context-budget.json` change does **not** (the seed
is a different file). **This phase is one session. STOP when done.**

---

### Phase 2 — Net accounting, and a governed archive tier

**Do.** Make `methodology_trim.py` report the **net repository delta** of a proposed trim (relieved
bytes vs shard + proof bytes), and bring `docs/archive/**` inside a guard: a per-shard ceiling and a
hard finding for any shard past `READ_REFUSE_BYTES`.

**DONE.** `--check` prints the net delta for a real trim and it reproduces F3's `+17,526 B` when run
against `9038e40~1`; a shard past 262,144 B is reported as a finding by name; and the existing
`HANDOFFS-through-2026-08-09.md` (382,071 B) is detected on the live tree without being modified.

**Verify.**
```sh
python3 starter-kit/methodology_trim.py --file HANDOFFS.md --check > /dev/null 2>&1; echo $?
python3 -m unittest discover -s tools -p 'test_methodology_trim*.py'
for f in docs/archive/*.verify.sh; do bash "$f" >/dev/null 2>&1; echo "$? $f"; done
```
The proof sweep is a **control, not a criterion**: 5 of 16 already fail (§4) and this phase does not
fix them — the count must not *increase*.

**Surface.** Canonical, plus a synthetic over-refusal fixture in a scratch directory. **The trimmer
is a TRACKED source — this reaches every adopter.** **One session. STOP.**

---

### Phase 3 — Truncation-end safety

**Do.** Give every watched artifact a declared **record order** (newest-first / oldest-first /
prose), and make an oldest-first artifact within a declared margin of its own cliff a finding —
because that is the case where truncation silently drops the newest content.

**DONE.** The order is asserted **against the artifact**, never restated in config: a file whose
first record number exceeds its last is newest-first, proven by parsing. `FRAMEWORK_LEARNINGS.md`
(1,158 tok of headroom, oldest-first) and `BACKLOG-DETAIL.md` (oldest-first, already truncating)
both raise the finding; `CHANGELOG.md` and `HANDOFFS.md` do not. A test fails if a file's declared
order stops matching its parsed order.

**Verify.** The three Python suites; `bin/tests.sh` row-for-row; and the §10 meter re-run to confirm
the headroom figures the finding is denominated in.

**Surface.** Canonical. **One session. STOP.**

---

### Phase 4 — The retire verb

**Do.** Implement the retirement policy chosen in D2/D3, for **one artifact class only** — the class
the operator names. `FRAMEWORK_LEARNINGS.md` is the obvious first instance (BL-45), and this phase
is where BL-45 is finally closed — as an instance of a rule, not as a point fix.

**⚠ Whatever the class, the mechanism must clear the three traps this session measured:** the
blank-line disarm (a pointer block is exactly what introduces it), the contiguity assertion that
fails at N=1, and the `reserved` hatch that silences contiguity while leaving citations dangling —
and which at N=5 goes **fully green on a false summary**.

**DONE.** A retirement can be executed and **reversed**; the retired content stays reachable and a
reader is told where; every guard still reports truthfully afterwards, demonstrated by re-running
the checker on the post-retirement artifact; and the **net repository delta is reported** (Phase 2)
rather than assumed negative.

**Verify.** The checker for that artifact class, run bare; `bin/tests.sh` row-for-row; the §10 meter.
**Surface.** Canonical; the artifact class named in D3. **One session. STOP.**

---

### Phase 5 — Fleet delivery

**Do.** Close the gap between what canonical has and what an adopter gets: fix the seed's
`LEARNINGS.md` entry to the name the manifest actually installs, declare the growing ledgers in the
seed, add a **size / readability column to `bin/status`** (the cheapest fleet-wide detector that
does not exist in any form today), and give `BOOTSTRAP.md` a step that sets up a size guard.

**DONE.** `bin/status` reports, per adopter, each methodology-managed file's bytes and whether it is
past one-read or past refusal — and reproduces §3.2's "8 of 11 over, 10 files past refusal" **without
writing to any adopter repo**. A fresh bootstrap ends with a working size guard, demonstrated on a
scratch directory.

**Verify.** `bash bin/tests.sh`; `python3 bin/check-links`; `bin/status` run against the eleven
siblings read-only, with `git status --porcelain` asserted clean **in each** afterwards.
**Surface.** Canonical + read-only fleet measurement + a scratch bootstrap. **One session. STOP.**

---

### Phase 6 — Contribute upstream

**Do.** One substantial, fully vetted pull request to `KJ5HST/methodology` carrying the distributed
half of Phases 1–5.

**⚠ REQUIRES THE OPERATOR'S EXPLICIT GO-AHEAD, EACH TIME, and it is not implied by approving this
plan.** No phase above authorises any outward-facing action. Per `CLAUDE.md`, batching to one
reviewable PR is the point; the contribution route is **open**, and no session may record it as
closed, paused, or unavailable.

**DONE.** Not defined here — a PR's shape depends on what Phases 1–5 actually land.

---

## 8. Here be dragons

1. **`context_budget.py`, `methodology_trim.py` and `methodology_dashboard.py` are TRACKED manifest
   sources.** Every code change in Phases 1–3 reaches all eleven adopters at their next `bin/sync`.
   The `.context-budget.json` at this root does not — the **seed** is a different file, and a fix
   there reaches *future* adopters only. Parse the manifest's **source** column; a bare-filename
   grep matches the dest and gives the opposite answer.
2. **The dashboard has a byte-identical `tools/` twin. Mirror LAST, then re-measure** — any number
   recorded before the mirror is false with nothing failing.
3. **Adding a ceiling to an R1 file constrains future canonical work and ships upstream.** That is
   why it is decision D7 and not a session's call.
4. **Do not "reconcile" the trimmer's basename lookup with the dashboard's path lookup.** The
   divergence is deliberate, documented at `methodology_trim.py:947-965`, and pinned by 8 test
   references. Harmonising it hands the relaxed 196,608 B arm to the distributed seed templates —
   precisely what the scoping decision was written to prevent.
5. **Harmonising the three ceilings *upward* silently multiplies the record budget** through the
   Class A arithmetic. Adjudicate D4 before touching any of the three.
6. **`bin/tests.sh` takes ~7 minutes and EXITS 1 EVEN WHEN GREEN.** Background it; read `$?` bare on
   the next line; never through a pipe. Test 34 and Test 37 **mutate the live `HANDOFFS.md` and
   `FRAMEWORK_LEARNINGS.md`** — do not run it concurrently with other work on those files.
7. **`bin/check-*` are Python with no extension.** The two `*.jsonl` go dirty from Phase 0 alone —
   **do not `git reset --hard`.**
8. **Test 37's mutant M2 hardcodes the anchor `^\| 3 \| `.** Any retirement reaching row #3 must
   move that anchor first — while the *same* test's `add_row37` deliberately derives its number as
   `max+1` because a hardcoded number collided once before.
9. **The proof tier is 70% of the shard and is itself a growth term.** A phase that adds proofs
   without counting them repeats F3.
10. **This plan is file 32 in an ungoverned directory.** Its 65,000 B budget is declared in the
    header and it is in Phase 4's population like anything else.

---

## 9. Explicitly not in scope

Implementing any phase in the planning session · BL-51 Phase C3 (A3/B1/B2) · `RECORD_BUDGET_BYTES`
and the record-budget campaign · repairing the five failing `.verify.sh` proofs (BL-36/49/50) ·
BL-42/43/44/46/48/52 · issue #75's unsent PR · trimming `CHANGELOG.md` or `HANDOFFS.md` (over by
adjudication, not neglect — BL-52) · `.git` object-store size, which no working-tree measure reaches
· **any outward-facing action whatsoever.**

---

## 10. Appendix — reproduction

```sh
# --- the token meter. The over-cap error reports EXACT tokens and returns NO content, so this
#     costs nothing. Double the file, Read the double with a spanning limit, halve the count.
cat FILE FILE > /tmp/x.txt && wc -l /tmp/x.txt     # then Read /tmp/x.txt offset=1 limit=<lines>

# --- R1, the mandatory read set, as one artifact
cat CLAUDE.md starter-kit/SESSION_RUNNER.md starter-kit/SAFEGUARDS.md > /tmp/r1.txt
wc -c /tmp/r1.txt; wc -l /tmp/r1.txt               # 80,813 B / 757 lines -> meter it -> 28,832 tok

# --- F3: the net delta of a trim, all four files, not just the one that shrank
for f in $(git show --name-only --format= 9038e40); do
  b=$(git show "9038e40~1:${f}" 2>/dev/null | wc -c); a=$(git show "9038e40:${f}" 2>/dev/null | wc -c)
  printf '%-58s %9s -> %9s\n' "$f" "${b:-0}" "${a:-0}"
done                                                # note ${sha}:path -- zsh mangles $sha:path

# --- F4: every tracked file ever deleted, in the whole history
git log --diff-filter=D --name-only --format= | sort -u | grep -v '^$'   # -> LICENSE, re-added

# --- F6: command output is a read artifact
git log --oneline | wc -c                          # 56,856 B vs READ_CAP_BYTES 56,750

# --- class membership, from the two independent sources, never from memory
python3 -c "import sys;sys.dont_write_bytecode=True;sys.path.insert(0,'starter-kit');\
 import methodology_trim as t, methodology_dashboard as d;\
 print('A:',sorted(t.LEDGERS));print('B:',sorted(set(d.READ_CAP_WATCHED)-set(t.LEDGERS)))"

# --- the fleet, READ-ONLY. Never write to a sibling repo.
cd .. && for d in */; do [ -f "$d/SESSION_RUNNER.md" ] && \
  echo "$d $(cat "$d/CLAUDE.md" "$d/SESSION_RUNNER.md" "$d/SAFEGUARDS.md" 2>/dev/null | wc -c)"; done
```

**Every checker is run bare with `$?` read on the next line** — `producer | grep -q` under
`set -o pipefail` reports a *failed* pipeline even when the pattern matched, because grep
short-circuits and the producer takes SIGPIPE.
