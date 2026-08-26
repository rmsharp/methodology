# CHANGELOG.md — archive: 2026-08-25 → 2026-08-25

Retired records from [`CHANGELOG.md`](../../CHANGELOG.md), moved here so the live ledger stays small enough to read
in one pass. Same format, same newest-on-top order — this is the same ledger, continued.

Holds **12 record(s), 2026-08-25 → 2026-08-25**. Cut key: `2026-08-25`. Counts here are computed from the file
itself, never carried forward. This shard is frozen: it states no forward-looking rule,
because the live file owns those and a copy of one was wrong a day after it was written.

---

### 2026-08-25 · [ad hoc] S109 close-out — Phase 2 shipped: front matter −16.2%, the header reserve named and asserted

Phase 3D receipt in [`HANDOFFS.md`](../../HANDOFFS.md), **inside the 12,288 B per-record budget** — which
took seven trim passes against `bin/check-handoff`, run each time rather than estimated.
Commits: `bd3f026` (Phase 1B claim) + **`eec1cbb`** (the deliverable) + this close-out.
**Phase 2 of [`record-budget-reduction-plan.md`](../../docs/planning/record-budget-reduction-plan.md),
ratified at S105.** `RECORD_BUDGET_BYTES` **unchanged at 12,288** (§4.3).

**The four-repo measurement that reframed the session.** The operator asked why this repo spends
its effort trimming when three larger adopters do not. Read-only, same 65,536 B ceiling:

| repo | `CHANGELOG.md` | `HANDOFFS.md` | `--check` | median B/receipt | archive shards |
|---|--:|--:|---|--:|--:|
| **methodology** | 37,659 | 51,622 | **silent, both** | **11,483** (n=115) | 17 |
| wsfct | 74,180 | 51,983 | FIRES (CHANGELOG) | 4,059 (n=67) | 6 |
| nprcgenekeepr | 218,298 | 286,154 | FIRES, both | 4,664 (n=325) | 13 |
| vscode_quarto_ext | 811,069 | **1,780,187** | FIRES / **cannot parse** | 7,912 (n=216) | **0** |

They do not lack the symptom; they lack the measurement. This repo has the **smallest** ledgers of
the four and is the **only one under the ceiling**. The per-receipt figures are taken over live
ledgers **plus every archive shard**, so the population is the whole history rather than the
post-trim remnant. This repo's receipts run **2.5–2.8× the adopter median** — 5.7 receipts to fill
the ceiling against their 14–16 — while its `CHANGELOG` entries are the *smallest* of the four
(median 1,387 B). The excess is entirely in `HANDOFFS.md`, which is §2 of the plan restated by
independent measurement: *"the term worth attacking is the receipt, not the file."*

**What shipped.** The 8 archive pointer blocks (3,587 B, **48.6%** of a 7,361 B front matter,
growing ~447 B per trim) collapsed into one table stating the naming rule once:
**7,361 → 6,170 B (−16.2%)**, per-trim growth **~447 → ~190 B**. Lossless, proved from the written
artifact against the pre-change blocks re-derived from `git show`: 7 facts × 8 shards, 92 = 92
records, parse-completeness asserted so an empty match could not read as success, plus a tamper
control. All 16 shard links preserved (`check-links` 88/22, unchanged). The live receipt count in
the same front matter said **3** where the file held **5**; corrected.

**The half the plan did not know was there.** `HEADER_RESERVE_BYTES` did not exist — 8,000 B lived
only inside a derivation comment, so the term Phase 2 was told to re-derive had nothing to
re-derive it *in*, and nothing failed when it went wrong. **It had already gone wrong: the front
matter had crept to 92.0% of it, two trims from a silent breach.** Now `CEILING_BYTES = 65536`,
`HEADER_RESERVE_BYTES = 7168`, `RETENTION_FLOOR = 3` sit beside the per-record constant, with
`bin/tests.sh` **Test 39**: **A1** the fit (`3 × 12,288 + 7,168 = 44,032 ≤ 65,536`) and **A2** the
live front matter held under the reserve. **Every byte of that 92% creep satisfies A1**, which is
why A2 exists. A2 was observed **RED two independent ways** and restored. The fit assertion is a
**test, never a module-scope `assert`** — decided at claim, per S108's `next_steps` (d).

**Verification.** `bin/tests.sh` **286/1/0** against a **279/1/0** control, diffed row for row:
**7 new rows, 0 status flips, 0 regressions**; the 3 rows whose text changed carry derived counts
this session's own claim moved (`**Model:**` 8→9, receipts 4→5), PASS on both sides. All **16**
shipped `.verify.sh` proofs run: 12 OK / 4 FAIL, the same four (BL-36). `check-links`,
`check-handoff`, `--all`, `check-learnings` OK. `context_budget.py`: no file over its ceiling.
`trim --check`: silent on both ledgers.

**Five findings recorded rather than absorbed — [BL-42 … BL-46](../../docs/planning/BACKLOG-DETAIL.md).**
BL-42 the trimmer still generates the fat block (distributed; the plan's §7 forbade touching it
while §6 asked for the compaction — a scope collision recorded in the plan). BL-43 six
`bin/tests.sh` assertions flake under `pipefail`, enumerated, all noisy-polarity. BL-44
`check-learnings` prints `contiguous 1..len(rows)`, false whenever a number is reserved — it
already contaminated S108's receipt. **BL-45 `FRAMEWORK_LEARNINGS.md` is 16 B from its ceiling and
this blocks Phase 3C for the next session.** BL-46 an adopter's trimmer inert since bootstrap
because the seed sentinel was never deleted, and nothing checks that it was.

**Canonical-only. Nothing distributed, nothing outward-facing.**

**Model:** Claude Opus 5 (1M context).

### 2026-08-25 · [ad hoc] S109 claim — Phase 2 of the record-budget reduction

`CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in
[`HANDOFFS.md`](../../HANDOFFS.md). **Phase 2 of an already-RATIFIED plan**
([`docs/planning/record-budget-reduction-plan.md`](../../docs/planning/record-budget-reduction-plan.md)
§6), so there is no new design gate. Phase 1 landed at S106; Phases 2 and 3 have stood pending
through six sessions that trimmed files instead.

**Why now — the operator asked why this repo spends its effort trimming when three larger adopters
do not, and the answer inverts the premise.** Measured read-only across all four repos: this repo
holds the **smallest** ledgers of the four (`CHANGELOG.md` 37,659 B, `HANDOFFS.md` 51,622 B) and is
the **only one under the 65,536 B ceiling** — `--check` is silent on both. `wsfct` FIRES on
`CHANGELOG.md` (74,180 B); `nprcgenekeepr` FIRES on both (218,298 / 286,154 B); `vscode_quarto_ext`
FIRES on `CHANGELOG.md` (811,069 B) and its `HANDOFFS.md` (1,780,187 B, **27× the ceiling**) cannot
be trimmed at all — the trimmer refuses with `[ZONE_UNCLASSIFIED]` because the bootstrap
seed-sentinel line was never deleted, so it has **zero** archive shards. They do not lack the
symptom; they lack the measurement.

**The term that is genuinely wrong here is the RECEIPT, not the file.** Measured over live ledgers
**plus every archive shard**, so the population is the whole history and not the post-trim
remnant: median B/receipt — this repo **11,483** (n=115), `vscode_quarto_ext` 7,912 (n=216),
`nprcgenekeepr` 4,664 (n=325), `wsfct` 4,059 (n=67). This repo's receipts are **2.5–2.8× the
adopter median**, which is 5.7 receipts to fill the ceiling against their 14–16. Its `CHANGELOG`
entries are the *smallest* of the four (median 1,387 B), so the whole excess sits in `HANDOFFS.md`.
That is §2 of the plan restated by independent measurement: *"the term worth attacking is the
receipt, not the file."*

**What Phase 2 does, per §6.** (1) Collapse the archive pointer blocks in `HANDOFFS.md` front
matter into one compact index. Re-measured at this Orient rather than inherited: there are **8**
blocks, not the plan's 7, totalling **3,580 B = 48.6%** of a **7,360 B** front matter — the plan
recorded 7 blocks / 3,132 B / 45% of 6,913 B, and the drift is exactly one block at the stated
~447 B, so the growth model is confirmed by its own error. (2) Give the **8,000 B header reserve a
name and an executable fit assertion** — today it exists only in prose in `bin/check-handoff`'s
derivation comment, with no constant and nothing that fails when it is wrong.

**Why the reserve is the urgent half:** the front matter is at **92.0% of it** (7,360 / 8,000) and
grows ~447 B per trim, so it **breaches in two trims** — and because the reserve is only a comment,
nothing would say so.

**Decided here, not discovered later (S108's next_steps (d)):** the fit assertion goes in
`bin/tests.sh` reading the constants out of `bin/check-handoff`, **never as a module-scope
`assert`** — that runs at import, so a mutant violating it dies with a traceback before the code
under test executes and is scored killed by the crash rather than by behaviour.

**`RECORD_BUDGET_BYTES` stays 12,288.** §4.3 is binding: shrinking the front matter must **bank**
the saving as slack, never feed it back through a division to raise the budget.

**What does NOT change:** the 65,536 B ceiling, Test 34's floor of 3, `methodology_trim.py`, and
anything distributed. **Nothing outward-facing.**

**Recorded at claim: a scope collision in the ratified plan.** §7 puts `methodology_trim.py` and
"anything distributed" out of scope, but the pointer blocks are *generated* by
`starter-kit/methodology_trim.py:935-936`, which **is** distributed. So the compaction is durable
only until the next trim appends a fresh 447 B block in the old format. Compacting is a data edit
and is in scope; teaching the generator the compact format is not, and is raised as a follow-on
rather than taken.

**Model:** Claude Opus 5 (1M context).

### 2026-08-25 · [ad hoc] S108 close-out — `CHANGELOG.md` trim shipped, 66,553 B → 34,044 B

Phase 3D receipt in [`HANDOFFS.md`](../../HANDOFFS.md), **12,288 B inside the 12,288 B per-record
budget** — over on the first write and on three later passes, each time cut from the trailing prose, which is
where the checker says to cut. Predecessor **S107 scored 8/10**; **self-score 8/10**.

**The deliverable.** 23 records spanning `2026-08-18 → 2026-08-24` archived to
[`docs/archive/CHANGELOG-through-2026-08-24.md`](../../docs/archive/CHANGELOG-through-2026-08-24.md) with
its `.verify.sh`; 8 retained, all `2026-08-25`. Live file **66,553 B → 34,044 B** against the
65,536 B ceiling — from OVER by 1,017 to **31,492 B clear**. `--check` reports *trigger does not
fire* on both triggers (was FIRES); `context_budget.py` went **BREACH (exit 2) → no file over a ceiling**; it still exits **1
(WARN)**, from the growth run alone (57 non-shrinking measurements vs a threshold of 10), which
is independent of any ceiling. I nearly recorded `exit 0` without measuring it. The tool was
**run, not edited**.

**`--cut N` retains the N newest; it does not archive N** — settled from
`methodology_trim.py:1730`/`:888`, not from S107's worked example, which used a six-record file on
which both readings are the same command. On 31 records the wrong reading inverts the operation and
**passes every check in the repo**.

**This file's retention floor is a CONTENT floor, not a record count.** `bin/tests.sh` Test 30's
real-file arm (`:1891-1892`) fails on **zero** `**Model:**` bullets in the live ledger; Test 31
(`:1960-1962`) re-reads that population. Asserted on the retained set after the write: **7 of 9**.
It does not generalise from `HANDOFFS.md`, whose floor is a record count.

**Losslessness, three ways, one independent of the tool.** The tool's `L1`/`L2`/`L3`/`P1A`; its
emitted `verify.sh` **run** (`31 before = 8 retained + 23 archived; added by the trim commit: 1`,
exit 0); and every record re-extracted from `git show f40793c:CHANGELOG.md` and byte-compared with
**my own inverter** — retained 8/8, archived 23/23 both directions, concatenation reconstructs the
original zone, front matter +4/−0 lines. Seam proved on the artifacts: retained `{2026-08-25}`,
archived `{2026-08-18, 2026-08-23, 2026-08-24}`, intersection **empty**.

**A correct artifact read as 21 corrupted records, and the proof was what was wrong.** The trimmer
rebases root-relative link targets by `../../` (32 targets × 6 B across 21 records) and refuses to
unless the rebase round-trips to the identity, so `L3`'s "byte-identical" is identity *modulo* that
transform. Recorded as **Learning #37** (`starter-kit/FRAMEWORK_LEARNINGS.md`, 1,413 B, now 36 rows
— **997 B free**, so the next owed row will not fit without removing one).

**Suite:** control at the claim commit `f40793c` **280 rows, 279/1/0**; after, **280 rows, 279/1/0**,
same sole failure (`github source dry-run failed`, Test 9's pre-existing 404). Row-for-row: **zero
lost, zero gained, zero skipped, one pair differing** — Test 31's count `26 → 7`, PASS both sides.

**Measured last (FM #28 gate), after this entry:** `CHANGELOG.md` **37,659 B**, **27,877 B clear**.
**`HANDOFFS.md` is the one to watch: 51,622 B, only 13,914 B clear, against a 12,288 B receipt** — one
more fits, two do not, and at 4 records against the `--cut 3` floor a trim could archive exactly
one. Re-run `wc -c`; `context_budget.py` now shows both files on the LINES axis, where the bytes
that are the whole constraint do not appear.

**Model:** Claude Opus 5 (1M context).

### 2026-08-25 · [ad hoc] Ledger trim: `CHANGELOG.md` → `docs/archive/CHANGELOG-through-2026-08-24.md` (23 record(s), 69,370 B → 34,044 B)

**Written by:** `methodology_trim.py` v1.3.0 — a tool action, not a session's judgment.
Moved the oldest **23** record(s) (2026-08-18 → 2026-08-24) out of [`CHANGELOG.md`](../../CHANGELOG.md) into
[`docs/archive/CHANGELOG-through-2026-08-24.md`](../../docs/archive/CHANGELOG-through-2026-08-24.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/CHANGELOG-through-2026-08-24.md.verify.sh`](../../docs/archive/CHANGELOG-through-2026-08-24.md.verify.sh)
rather than trusting a digest printed here. Live file 69,370 B → 34,044 B (−50.9%).

### 2026-08-25 · [ad hoc] S108 claim — run the `CHANGELOG.md` trim, losslessly

`CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in
[`HANDOFFS.md`](../../HANDOFFS.md). **A maintenance session running a shipped tool** — the deliverable is
the archive shard and the restored headroom, not a change to the tool.

**Why now.** S107's next_steps (a), which predicted this file might be the next trim and named
itself as the possible cause. Re-measured at this Orient rather than inherited, exactly as it
instructed: `context_budget.py` reports **66,553 B against the 65,536 B ceiling, over by 1,017**,
and `--check` reports **trigger FIRES** on bytes. S107 recorded 66,410 B; its own close-out entry
is what carried the file over, and 143 B more arrived after its measurement. The line trigger does
not fire (32 records of headroom) and `HANDOFFS.md` does not fire at all — a one-file job.

**The cut is `--cut 8`, chosen before the write, and `--cut N` retains the N newest rather than
archiving N** — read off `methodology_trim.py:1730` (`retained, archived = records[:k], records[k:]`)
and `:888`, not inferred from prose. With this entry prepended the file holds 31 records, so
`--cut 8` retains all eight of `2026-08-25` and archives the 23 spanning `2026-08-18 → 2026-08-24`:
disjoint date sets, so `CHANGELOG-through-2026-08-24.md` is a true day boundary and not a span
label, and no shard by that name exists. Dry runs at all three calendar seams were measured rather
than estimated — retain 7/16/23 give 31,227 / 48,476 / 53,756 B — and the deepest was chosen
because a trim session is itself expensive: S107's cost this ledger 5,483 B across its claim, its
auto-entry and its close-out, so a cut buying two or three sessions nearly pays for itself and no
more. 31,227 B is 47.6% of ceiling, where S107 left `HANDOFFS.md` (48.6%), and it leaves the live
ledger covering the same three sessions whose receipts `HANDOFFS.md` still retains.

**This file's retention floor is a CONTENT floor, not a record count — the finding this cut turned
on.** `bin/tests.sh` Test 30's real-file arm (`:1891-1892`) fails if the live `CHANGELOG.md` carries
**zero** `**Model:**` bullets, and Test 31 (`:1960-1962`) re-reads that population. 25 of 30 records
carry one; only the five auto-generated `Ledger trim:` entries do not. Any cut retaining the newest
record clears it — to be asserted on the retained set after the write, not reasoned about.

**What does NOT change:** the 65,536 B ceiling, `RECORD_BUDGET_BYTES`, `methodology_trim.py` itself,
`HANDOFFS.md` (its trigger does not fire), BL-36's four failing shipped proofs, and every shard
already frozen. No distributed file — the trimmer is distributed but is only being *run*, not
edited.

**Model:** Claude Opus 5 (1M context).

### 2026-08-25 · [ad hoc] S107 close-out — `HANDOFFS.md` trim shipped, 82,406 B → 31,875 B

Phase 3D receipt in [`HANDOFFS.md`](../../HANDOFFS.md), **9,332 B inside the 12,288 B per-record budget
S106 introduced — 2,956 B of headroom, reached on the first pass.** Self-score 8/10; predecessor
S106 scored 9/10, for warning that its own arithmetic was stale rather than leaving me to discover
it (its Orient figures were four records old, and it said so).

**The breach is closed.** `HANDOFFS.md` went from **OVER its 65,536 B ceiling by 16,870** to
**26,505 B clear** at close-out. Both triggers now silent; `context_budget.py` exits 0.

**Measured last, per FM #28:** `HANDOFFS.md` **39,031 B** (3 receipts), archive shard
**HANDOFFS-through-2026-08-24.md** frozen with 3, `CHANGELOG.md` **now over its own 65,536 B ceiling, this entry included — see below**,
`FRAMEWORK_LEARNINGS.md` 63,126 B (2,410 B free), `main` 51 ahead of `origin/main`, nothing pushed.

**⚠ THIS ENTRY IS ITSELF THE NEXT SESSION'S PROBLEM, AND SAYING SO IS THE POINT.** Before it was
written `CHANGELOG.md` measured **63,868 B against 65,536 B — 1,668 B clear, less than one close-out
entry** — and its trim trigger did **not** fire. This entry is larger than that margin, so the byte
trigger is expected to fire on the very next `--check`. That is the designed rhythm, not a defect:
the ledger that records the trim is the ledger that then needs one. **Re-run
`python3 starter-kit/methodology_trim.py --file CHANGELOG.md --check` — do not trust this
sentence.** Its line trigger is nowhere near (33 records of headroom): this is a BYTE breach, and
`context_budget.py` confirms it — `66,410 B ... over by 874`. The axis caveat below applies to
`HANDOFFS.md`, which is now green and therefore displayed in LINES; a file that IS over is shown in
bytes and red.

**Verification, three ways, one independent of the instrument:** the tool's L1/L2/L3/P1A; its
emitted `verify.sh` run rather than trusted; and all six records re-extracted from
`git show HEAD:HANDOFFS.md` and byte-compared against their destinations — six identical, none in
two places, 3 + 3 = 6. `bin/tests.sh` 280 rows before and after, **zero lost, zero gained, zero
skipped**, four derived counts moved; sole failure `github source dry-run failed` on both sides
(Test 9's pre-existing 404).

**Carve-out, re-derived after a first attempt got it backwards:** none of the four files touched is
a `bin/_manifest.py` **source** — adopters receive `starter-kit/HANDOFFS.md`, the SEED template,
which is untouched. **No adopter receives anything from this session. No outward-facing action.**

**Model:** Claude Opus 5 (1M context).

### 2026-08-25 · [ad hoc] Ledger trim: `HANDOFFS.md` → `docs/archive/HANDOFFS-through-2026-08-24.md` (3 record(s), 82,406 B → 31,875 B)

**Written by:** `methodology_trim.py` v1.3.0 — a tool action, not a session's judgment.
Moved the oldest **3** record(s) (2026-08-24 → 2026-08-24) out of [`HANDOFFS.md`](../../HANDOFFS.md) into
[`docs/archive/HANDOFFS-through-2026-08-24.md`](../../docs/archive/HANDOFFS-through-2026-08-24.md). Losslessness is asserted by L1 (records-zone concatenation), L2 (zone
pinning) and L3 (record partition), and is **re-derivable** — run [`docs/archive/HANDOFFS-through-2026-08-24.md.verify.sh`](../../docs/archive/HANDOFFS-through-2026-08-24.md.verify.sh)
rather than trusting a digest printed here. Live file 82,406 B → 31,875 B (−61.3%).

### 2026-08-25 · [ad hoc] S107 claim — run the `HANDOFFS.md` trim, losslessly

`CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in
[`HANDOFFS.md`](../../HANDOFFS.md). **A maintenance session running a shipped tool** — the deliverable is
the archive shard and the restored headroom, not a change to the tool.

**Why now.** S106 handed this forward as next_steps (a): the trim was due before it arrived and it
did not run it (a second capability — FM #26). Re-measured at this session's Orient rather than
inherited: `context_budget.py` reports `HANDOFFS.md` at **80,230 B against the 65,536 B ceiling,
over by 14,694**, and `methodology_trim.py --file HANDOFFS.md --check` reports **trigger FIRES** on
the byte trigger. The line trigger does not fire (17 records of headroom) and `CHANGELOG.md` does
not fire at all — this is a one-file job.

**The cut is `--cut 3`, chosen before the write, for the reason S104 recorded and one it did not
have.** Three is the retention **floor**, not a preference: below it `bin/tests.sh` Test 34's six
whole-ledger assertions drop into their SKIP arm, and Test 38's fixture builder aborts outright.
The new reason is the calendar seam — with this claim receipt prepended the file holds six records,
and `--cut 3` retains S107/S106/S105 (all `2026-08-25`) while archiving S104/S103/S102 (all
`2026-08-24`), so the retained and archived date sets are disjoint and the shard name
`HANDOFFS-through-2026-08-24.md` is a true day boundary rather than a span label. That is the
`[CUT_STRADDLES_DAY]` note the tool raised against a five-record file at Orient, and the claim
receipt is what resolves it. **Measured after the claim, not predicted from it.**

**What does NOT change:** the 65,536 B ceiling, `RECORD_BUDGET_BYTES`, `methodology_trim.py` itself,
`CHANGELOG.md` (its trigger does not fire), and every archived shard already frozen. No distributed
file — the trimmer is distributed but is only being *run*, not edited.

**Model:** Claude Opus 5 (1M context).

### 2026-08-25 · [ad hoc] S106 close-out — Phase 1 shipped, per-record budget 18,432 → 12,288

Phase 3D receipt in [`HANDOFFS.md`](../../HANDOFFS.md), **inside the NEW 12,288 B budget it introduces —
12,264 B, 24 B of headroom, reached in seven trim passes.** The guard applied to its own author, the
precedent set when the budget was introduced. Self-score 8/10; predecessor S105 scored 7/10.

**Phase 1 of [`docs/planning/record-budget-reduction-plan.md`](../../docs/planning/record-budget-reduction-plan.md)
is complete.** `RECORD_BUDGET_BYTES` is now **12,288**, and — the part that matters more than the
number — it is a **policy number with a fit assertion**, no longer a quotient. The old figure was
`(65,536 − 8,000) / 3`, a formula that sizes the budget *to* the ceiling and therefore accommodates
growth rather than restraining it. Steady state falls **63,296 B → 44,864 B** (96.6% → 68.5% of the
ceiling); slack rises **2,240 B → 20,672 B**, more than one whole receipt, so a trim becomes
occasional instead of mandatory-every-session.

**THE PLAN'S MANDATORY GREP INVENTORY WAS INCOMPLETE BY TWO SITES, AND ONE OF THEM WOULD HAVE STAYED
GREEN WHILE TESTING NOTHING.** §5.2 listed nine `bin/tests.sh` couplings; there are **thirteen**.

- **`bin/tests.sh:2833-2837`** — the one-byte-OVER half of the edge test (`add_record38 18433`).
  **Missed because the inventory's own grep pattern was `18,?432`, which cannot match the derived
  neighbour `18433`.** Left unchanged it would still have passed: an 18,433 B record is over a 12,288
  B budget, so the assertion still matches — while exercising a record **6,145 B** past the cap
  instead of one byte past it, and leaving the `>` → `>=` boundary mutant scored *killed* by a record
  any budget catches. Its at-budget twin fails loudly; only this half is silent.
- **`bin/tests.sh:2946`** — the forged summary payload inside mutant M3. Functionally inert, but its
  job is to be a convincing forgery of a line the code can emit.

**The generalisation, recorded because it outlives this change:** a value's *derived neighbours* —
`N+1`, `N + 512`, an overage term computed from `N` — do not match a grep for `N`. Enumerate the edge
cases and the arithmetic, not only the literal. The correction is written into the plan beneath §5.2
so Phases 2 and 3 inherit it rather than repeat it.

**A HAZARD FOUND AND DELIBERATELY NOT SHIPPED, HANDED TO PHASE 2 INSTEAD.** §4.3 wants the fit rule
`3 × budget + allowance ≤ 65,536` *asserted*, and Phase 2's DONE criterion says so. But a module-scope
`assert` in `bin/check-handoff` is evaluated at **import**, and `bin/tests.sh:2957` (mutant M4)
rewrites the constant to 50,000 — `3 × 50,000 + 8,000 = 158,000`, so the mutated interpreter dies with
an `AssertionError` before reaching the code under test. M4 greps for the *absence* of a catch, and a
traceback contains no catch, so **the mutant would be scored killed by a crash rather than by the
budget behaviour.** Any value large enough to survive M4 breaks the fit check by construction. The fit
rule therefore ships as prose beside the constant; the two concrete fixes are in the receipt's
`next_steps` (b).

**Verified, not asserted.** Pre-change control run in a `git worktree` at the claim commit — not in the
tree being edited — giving **280 rows, 279/1**, sole failure named (`github source dry-run failed`,
Test 9's pre-existing `--source=github` 404). After: **280 rows, 279/1, same sole failure.**
Row-for-row diff of the sorted rows, both populations asserted non-empty: **zero lost, zero gained,
exactly four pairs differ** — the two edge rows, and the two scope-control rows whose *population
count* moved 1 → 3 because a lower budget puts more frozen receipts over it. That last pair is worth
noting: it is a **stronger** control, but it is not what the plan predicted (*"changes confined to rows
whose names carry the budget number"*) — those two names carry a derived count instead. Python suites
**451/451**. `check-handoff --all` OK over all 5 receipts, confirming the **prospective-only** property:
no committed receipt reddened and none needed rewriting. The rewritten user-facing remediation text was
exercised by **triggering a real failure** on a throwaway git fixture, not by reading the format string.

**FM #28 gate, measured after the last write.** `CLAUDE.md` 11,064 B ok · `CHANGELOG.md` 837 ln ok ·
`docs/planning/BACKLOG.md` 184 ln ok · `starter-kit/FRAMEWORK_LEARNINGS.md` 63,126 / 65,536 ok
(2,410 B free, unchanged) · **`HANDOFFS.md` 80,230 B — OVER the 65,536 B whole-file ceiling by 14,694.**
It arrived over (67,966, by 2,430) and this receipt adds 12,264. **This is the one Phase 1 verification
command the plan lists that Phase 1 cannot satisfy** — `context_budget.py` exit 0 — because the breach
is the *whole-file* ceiling and the plan's own §7 puts the ceiling and the trim out of scope. The
**record** budget is green. The trim is the next deliverable and is a second capability (FM #26).

**Not changed, verified rather than assumed:** no distributed file — neither `bin/check-handoff` nor
`bin/tests.sh` has a row in `bin/_manifest.py`, so no adopter receives any of this; the 65,536 B
ceiling; Test 34's floor of 3; `methodology_trim.py`; and every historical statement of 18,432 in this
ledger, in `HANDOFFS.md` and in the archived shards, which are frozen records of what was true when
written (FM #22). Inside `bin/`, two past-tense sentences were rewritten to say **"18 KiB"** rather than
be exempted, so that `git grep -nE '18,?432' -- bin/` remains a live detector of a missed coupling.

**Model:** Claude Opus 5 (1M context).

### 2026-08-25 · [ad hoc] S106 claim — Phase 1 of the record-budget reduction: lower the constant

`CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in
[`HANDOFFS.md`](../../HANDOFFS.md). **An implementation session executing a ratified plan** — Phase 1 of
[`docs/planning/record-budget-reduction-plan.md`](../../docs/planning/record-budget-reduction-plan.md),
one phase, one session, per that plan's own STOP.

**The blocking decision was settled at Phase 1, not assumed.** Plan §9 made ratification of the
number the one thing Phase 1 could not start without, because every site in §5.2 encodes it. The
operator ratified **12,288 (12 KiB)** — the plan's recommendation — over the costed alternatives
10,240 and 8,192. That choice is recorded here so a later session can see it was made rather than
inherited.

**What changes:** `RECORD_BUDGET_BYTES` 18,432 → 12,288 in `bin/check-handoff`, its derivation
comment rewritten from a ceiling-fitting *formula* into a **policy number plus a fit assertion**
(plan §4.3 — otherwise Phase 2's front-matter saving would be handed straight back), the
user-facing remediation text, the nine `bin/tests.sh` couplings, and the `_` note in
`.context-budget.json`.

**What does NOT change, verified rather than assumed:** no distributed file — `bin/check-handoff`
and `bin/tests.sh` are both canonical-only, so **no adopter receives anything this touches**; the
65,536 B ceiling; Test 34's floor of 3; `methodology_trim.py`, which couples only to the whole-file
budget; and every historical statement of 18,432 in this ledger, in `HANDOFFS.md`, and in the
archived shards — those are frozen records of what was true when written (FM #22).

**Why no existing receipt reddens.** `check_record_budget` is **prospective-only**: it checks the
newest record, and only when it differs from its frozen copy at git HEAD. Committed receipts are
exempt by construction. Lowering the budget therefore requires no migration and rewrites no receipt.

**Model:** Claude Opus 5 (1M context).

### 2026-08-25 · [ad hoc] S105 close-out — plan delivered, self-score 8/10, predecessor S104 scored 8/10

Phase 3D receipt in [`HANDOFFS.md`](../../HANDOFFS.md). **A planning session: the plan is the deliverable
and nothing was implemented** (FM #18/#19) — zero files touched under `bin/`, `tools/` or
`starter-kit/`. Claim `2cdda38`, this close-out.

**The deliverable:** [`docs/planning/record-budget-reduction-plan.md`](../../docs/planning/record-budget-reduction-plan.md),
DRAFT awaiting ratification. Recommends `RECORD_BUDGET_BYTES` **18,432 → 12,288**, taking the steady
state from **63,296 B (96.6% of ceiling, 2,240 B slack)** to **44,864 B (68.5%, 20,672 B slack)** and
the per-session context cost from ~25 KB to ~19 KB.

**Three measurements decided the plan's shape.** (1) The ledger is **read and gleaned, never
resident** — no `@`-import; measured across 81 transcripts as read whole **once**, in part **593**
times. So a session pays *front matter + one receipt*, and **the receipt is the only lever that
touches recurring cost.** (2) The budget is **prospective-only** — `check_record_budget` compares the
newest record against its frozen copy at HEAD — so **no existing receipt reddens and none needs
rewriting.** (3) Trailing prose is **27–30%** of a receipt while fenced fields mean **12,108 B**,
which is exactly why 12,288 preserves all six mandatory requirements and 8,192 would cut into them
(FM #15). A 17-site grep inventory is in §5, every `bin/` line number verified by re-reading it.

**Two of my own errors, caught at Phase 3F and fixed before commit.** The first draft wrote
`3 × 18,432 + 8,000 = 61,312`, mixing two header terms — the derivation's **8,000 B allowance** gives
**63,296**, while S103's quoted 61,312 uses the header **as measured then** (6,016; today 6,913). The
second: twelve `CHANGELOG.md` line citations were taken *before* this session's own claim entry and
were stale by **5**; re-derived. A line number measured before your own write fails silently.

**`HANDOFFS.md` IS OVER ITS CEILING AGAIN — 67,966 B against 65,536, over by 2,430** (`context_budget.py`
exits 2; `--check` FIRES). **Recorded, not fixed:** a trim is a second capability (FM #26) and this was
a planning session (FM #18). S104 predicted this at its close-out — the breach arrived in exactly one
session, which is the plan's own premise demonstrated rather than argued. **The next session's first
act is the trim (`--cut 3`, never the default); the plan is what stops it recurring.** This receipt was
deliberately written under the **proposed** 12,288 B budget and measures **10,074 B**, 2,214 B clear —
one worked example that the recommendation is livable.

**Model:** Claude Opus 5 (1M context).

### 2026-08-25 · [ad hoc] S105 claim — plan the per-record budget reduction

`CHANGELOG: pending` — set at claim; receipt stub with `status: pending` in
[`HANDOFFS.md`](../../HANDOFFS.md). **A planning session: the plan is the deliverable and nothing is
implemented** (FM #18, FM #19).

**Why.** S104 established that `HANDOFFS.md` cannot be fixed by trimming: Test 34's retention floor
of 3 receipts × `check-handoff`'s 18,432 B per-record budget + ~6 KB of front matter = **61,312 B
against a 65,536 B ceiling**, and the file sits at 94.4% of that immediately after a trim. The
operator's concern is session context cost, so the target is the number a session actually pays.

**Two measurements that shape the plan, taken before it was written.** (1) The ledger is **read and
gleaned, never resident** — no `@`-import; measured across 81 transcripts as read whole **once** and
in part **593** times, median span 25 lines — so the per-session cost is front matter + **one**
receipt, ~25 KB, not the file. (2) **Trailing prose is 27–30% of every recent receipt** (S104 5,388 B,
S103 4,613 B, S102 4,653 B), and it is the Phase 3A/3B essays — *additive* to the six mandatory
requirements, which the receipt already summarises as the structured `predecessor_score` and
`self_score` fields.

**Model:** Claude Opus 5 (1M context).

