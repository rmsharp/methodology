# The overhead ratchet — gating what the framework costs its own users

**Deliverable of S232 (2026-09-28). Planning session: this document is the deliverable and nothing
here is implemented.** Commissioned by the operator on 2026-09-28 for
[BL-91](BACKLOG-DETAIL.md#bl-91), re-confirmed at this session's Phase 0 picker. Written at maximum
reasoning depth (`SESSION_RUNNER.md` §Planning Sessions).

**Every number below was re-derived on this tree at `98545c1`.** Nothing is carried from BL-91's
prose, which says so itself: *"re-run them, do not quote this paragraph."* Two of BL-91's own
framings did not survive that re-derivation — §4 F1 and F5.

---

## §0 The verdict

**The overhead gate is not missing. It exists, it is distributed, it has no escape hatch, it works,
and it is red on this repository right now — and nothing in this repository's gate chain has ever
run it against this repository.** `context_budget.py --precommit` compares every budgeted file's
staged size against both its ceiling and its size at `HEAD`, refuses a growth, and passes a shrink
(`starter-kit/context_budget.py:1000`; the byte refusal is `:1038` — `new > ceil and new > old`, so a
commit that shrinks an over-budget file is never blocked; token arm `:1044-1051`). The eleven gates in
`.quality-gates.json` measure test counts and exit codes; the one named `context-budget-unit-tests`
runs the tool's **unit tests**, not this repository's budget. `.githooks/pre-commit`'s single gate
call is `quality_ratchet.py --precommit` (`:133`). `bin/tests.sh` exercises the budget tool only
against scratch fixtures.

**So BL-91's structural claim — "the quality ratchet only tightens and NOTHING ratchets overhead" —
is half right in a way that matters.** Nothing ratchets overhead *here*. But the mechanism was not
absent; it was **declined**. The operator declined enforcement at S206 (BL-78 P3), on evidence, and
that decision is not this plan's to overturn. Two sessions before him claimed the ratchet "does not
exist" and both were wrong; BL-83 closed that at S225 with fork Learning #98.

**What this plan therefore proposes is not the declined thing.** What was declined was a *hook*
enforcement requiring a new comparison in a **distributed tool** plus a change to a **distributed
hook**. What is available and was never put to the operator is a **ratchet gate**: one entry in this
repository's own `.quality-gates.json`, whose measurement is the read-set byte total, declared at
today's value with `direction: max` so it can only ever come down. It touches no distributed file, it
builds nothing, and because `quality_ratchet.py --run` measures the **resulting tree** once per
session rather than each commit, it is indifferent to how the bytes arrived — which is the exact
objection that killed the hook shape.

**Recommended: D1 option (b), the ratchet gate on the class total, declared at 72,535 B.** It is the
smallest thing that converts five months of unwatched monotone growth into a number that cannot rise
without a recorded, reviewable decision.

---

## §1 What is already settled — do not re-litigate any of this

A plan that re-proposes a ratified decision costs a session and loses trust. Four are binding here.

| # | Decision | Who, when | Scope — read this column before citing it |
|---|---|---|---|
| S1 | The `FORK_LEARNINGS.md` 81,920 B figure is a **reported series, not a limit**; the per-row `ROW_BUDGET_BYTES` = 1,500 is what still refuses | operator, S201, ratified S202 (BL-53 D4, option C) | **That file's row only.** It says nothing about the read-set class total, and nothing about whether the tool runs |
| S2 | `starter-kit/SAFEGUARDS.md`'s row is a **reported series** | operator, S205 (BL-78 P2, option β) | That file's row only |
| S3 | **No enforcement** — do not build a growth comparison into the distributed tool and wire it into the distributed hook | **operator, S206 (BL-78 P3)** | The **hook shape**. The evidence put to him was the merge finding (§4 F1). He was not asked about a ratchet gate, and `.quality-gates.json` was not on the table |
| S4 | The `.context-budget.json` ceiling is a reported series; the per-row budget stays | operator, S202, option C | `CLAUDE.md` §Contributing records this. `.context-budget.json` still calls the figure a warning until BL-53's P5 rewrites it |

**S3 is the one a reader will misremember as wider than it is.** It is a decision about a *mechanism*,
taken against that mechanism's measured incompleteness and its distributed blast radius. It is not a
standing prohibition on watching overhead, and no session may record it as one — `CLAUDE.md` names
that failure by name, and it cost this repository ten sessions once already.

**What BL-91 adds that none of S1–S4 covers:** the **release-indexed series**. S1–S4 each argue about
one file's number at one moment. Nobody had asked what the curve does across versions, and the answer
is §2.

---

## §2 The evidence, re-derived this session

### 2.1 The series — 27 releases, re-run not quoted

`python3 docs/planning/bl91-overhead-measurement/mandated-load-per-version.py`, run at `98545c1`:

| version | date | runner B | safeguards B | per-session mandated read |
|---|---|---|---|---|
| v1.0.0 | 2026-03-09 | 9,765 | 7,850 | 17,615 |
| v2.0 | 2026-03-27 | 20,023 | 7,850 | 27,873 |
| v2.7 | 2026-06-12 | 38,591 | 11,961 | 50,552 |
| v3.0 | 2026-06-25 | 40,474 | 11,961 | 52,435 |
| v3.3 | 2026-07-08 | 52,994 | 15,386 | 68,380 |
| v3.7 | 2026-08-12 | 65,140 | 15,386 | **80,526** |
| HEAD | 2026-09-28 | 55,406 | 17,129 | 72,535 |

**v1.0.0 → v3.7 is 4.6x, and the series never falls once across any of the 27 releases.** The one
fall is HEAD, unreleased, 9.9% below v3.7 — the S130 apparatus extraction, the only time the
reduction mechanism has been used.

**A decomposition BL-91 does not carry, and it matters for §5.** The runner went 9,765 → 65,140 B
(**6.7x**); `SAFEGUARDS.md` went 7,850 → 15,386 B (**2.0x**). The extraction that produced HEAD's fall
was applied to the runner alone: since v3.7 the runner is **−9,734 B** while `SAFEGUARDS.md` is
**+1,743 B**. **The one lever that has ever worked has never been pointed at the smaller file**, and
that file is now above its v3.7 size while the larger one is below it.

### 2.2 The instrument agrees, independently

`python3 starter-kit/context_budget.py --json` at `98545c1` reports the `read-set` class total as
**72,535 B against 56,750 B, status `over`** — and 55,406 + 17,129 = 72,535 **exactly**. The config's
`read-set` class (`.context-budget.json`) contains precisely `starter-kit/SESSION_RUNNER.md` and
`starter-kit/SAFEGUARDS.md` — the same two files BL-91's script measures, arrived at independently.
**Two instruments, same definition, same number.** That is the corroboration a single-script finding
would otherwise lack.

The tool exits **2** on this tree, every run, and has no `--force`: *"The only way to permit growth is
to edit `.context-budget.json`, so the decision lands as a reviewable diff."*

### 2.3 The ceiling is a partition, which constrains every per-file shape

`41,364 + 15,386 = 56,750` = `read_cap_tokens` 25,000 × `MIN_BYTES_PER_TOKEN` 2.27
(`.context-budget.json:4`, `starter-kit/context_budget.py:68`), **exactly**. So the two per-file
ceilings are a partition of one token cap: re-pinning either forces re-partitioning the other, and
BL-78 §(1) measured that the **byte** half of that identity has no guard — only the token half, held
by a canonical-only test (`tools/test_context_budget.py:1258`).

**This is the decisive argument for gating the TOTAL rather than the members.** A gate on the sum is
immune to the partition problem: it neither reads nor moves either per-file ceiling, so S1, S2 and S4
all stand untouched.

### 2.4 What could not be measured, restated because it bounds every dollar figure

Observed dollars per version do not exist. Local transcripts begin 2026-08-16; v3.7 shipped
2026-08-12. **Every dollar figure in BL-91 is a byte proxy priced at list**, and the larger cost term
— turns — is not measured per version at all. Mandated artifacts going 8 → 18 is a plausible turn
multiplier and **is not evidence of one.** No phase below is allowed to claim otherwise.

---

## §3 Inventory — where enforcement could attach, taken by grep

Mandatory for this plan because §5's shapes move enforcement between files
(`SESSION_RUNNER.md` §Planning Sessions). Every row below is a search result, not recollection.

```
git grep -n "context_budget" -- .githooks/ bin/ .quality-gates.json
git grep -n "quality-gates" -- bin/_manifest.py
python3 -c "import json; [print(g['name'], g['direction'], g['threshold']) for g in json.load(open('.quality-gates.json'))['gates']]"
```

| Attachment point | What it is today | Distributed? | Verdict |
|---|---|---|---|
| `.quality-gates.json` `gates[]` | **11 gates**, every one a test count or an exit code; **not one measures a size** | `bin/_manifest.py:62` ships `starter-kit/quality-gates.json` → `.quality-gates.json` as a **SEED** — installed once, then the adopter's own. The seed's `gates` array is **empty** | **The attachment point.** Editing this repo's copy is **canonical-only** and changes nothing an adopter receives |
| `.githooks/pre-commit` | one gate call, `quality_ratchet.py --precommit` (`:133`); never calls the budget tool | canonical-only, copied by hand | Blind to merges by construction — `SAFEGUARDS.md` §Blast Radius says so |
| `starter-kit/context_budget.py` | `precommit` exists (`:1000`), byte refusal `:1038`, token arm `:1044-1051`; `install-hook` ships | **DISTRIBUTED** (`bin/_manifest.py:54`) | Changing it is upstream-facing. **S3 declined exactly this** |
| `.context-budget.json` | 4 classes: `resident`, `read-mandated`, `on-demand`, `read-set` | this repo's own config, **not** the seed | Its numbers are reported series by S1/S2/S4. Do not move them |
| `bin/tests.sh` Test 35 | proves the tool refuses/passes correctly — against **scratch trees** (`$P`), never this repository | canonical-only | Correct as written; it tests the tool, not the subject |
| `tools/test_context_budget.py:1258` | `TestThisRepoReadSetPartition`, token half only | canonical-only | The partition's only guard |

**The finding this table exists to produce:** the only attachment point that is (a) not distributed,
(b) already run every session, and (c) already structurally required to be cited, is
`.quality-gates.json`. `bin/check-handoff` enforces that citation — gate `check-handoff-all`: *"with a
manifest present the newest complete receipt must cite its gate run."*

---

## §4 Findings

**F1 — "A hook would have caught none of it" is true of a 3-event window and false of the
55-to-62-event population. This is the correction that most changes the picture.** BL-78 §(3)
measured `SESSION_RUNNER.md` growth *since `measured_on` (2026-08-30)* and found **3 of 3 were
merges** — re-verified here: `421ebf9`, `7245f79`, `22ce71b` each have 2 parents; `ad7bd37`,
`628d218`, `df926b6`, `0d63410` each have 1. That measurement is correct. **It is also 3 events out
of the pair's whole history, and it was the evidence for S3.**

Measured over all history, and the instrument was audited because `git log -- <path>` prunes merges —
the hazard BL-78 itself warned about:

| walk | commits | single-parent growth | merge growth | merge share of bytes |
|---|---|---|---|---|
| default `git log -- <path>` | 68 | 52 events, +99,090 B | 3 events, +2,622 B | **2.6%** |
| `git log --full-history` | 124 | 51 events, +98,001 B | 11 events, +10,710 B | **9.9%** |

**The two disagree by ~4x on the merge share, and the default walk — the one a session reaches for —
understates it.** So the honest statement brackets it: **between 2.6% and 9.9% of read-set growth
bytes arrived by merge; 90–97% arrived in ordinary commits a hook would have refused.** Neither walk
supports *none*. `--full-history` also attributes a merge's whole delta to the merge even when the
bytes were authored on the merged branch, so 9.9% is an upper bound on "growth only a merge-aware
check could see," not a clean partition.

**What this does and does not do to S3.** It does not reopen it: the operator also weighed the cost —
a new comparison in a distributed tool plus a distributed hook change — and that cost was real and is
unchanged. It does mean **no session may carry "a hook catches nothing" forward as a general fact**,
and it strengthens the ratchet-gate shape, which catches 100% because it measures the tree.

**F2 — The gate exists and is red; only the wiring is absent.** §0 and §3. The tool exits 2 on every
run of this tree and has no `--force`.

**F3 — `direction: max` in the ratchet already means "only tightens" for a ceiling.**
`starter-kit/quality_ratchet.py:200`: raising a `max` threshold is refused as a loosening; `:198`:
lowering a `min` threshold is refused. Adding a gate always passes (`:181`). **So a `max` gate on a
byte count is a ceiling that can only come down — precisely the overhead mirror of the quality
ratchet, with no new tool.** The tool self-tests this: `check("raising a ceiling is refused", ...)` at `:459`, beside
`"lowering a floor is refused"` at `:458` (`:458-462`).

**F4 — Gating the class total sidesteps the partition.** §2.3. A gate on 72,535 reads no per-file
ceiling and moves none, so S1, S2 and S4 are untouched.

**F5 — "Nothing was looking" is not quite it: something was looking, reporting, and being read past.**
BL-78 §(4) found the tool's headline hardcoded at `context_budget.py:652-653` under `if run_hit:`,
printing *"Nothing is over a ceiling yet — that is the point"* while four rows read `over`. **It still
does — this session's Phase 0 saw exactly that.** That is BL-80, and it is PR #86's subject. **A
reported series is worth what its report is worth**, and this one contradicts its own table. So the
failure was not blind instrumentation; it was an instrument whose summary line told readers to
relax. This is why D1 option (a) — keep reporting, report better — is a live option and not a
strawman, and why any option that stays with reporting inherits a dependency on #86.

**F6 — The growth-run counter does not measure what its name suggests.** `growth_run` reads **174**,
and the tool appends a history line only when the measurement *changes* — three consecutive
invocations this session appended nothing. Its unit is **distinct measurements, not sessions**, and
per BL-78 it is *"a series over `resident_bytes`"* — `CLAUDE.md` alone. **The read-set total sat at
72,535 across the last three history entries while `HANDOFFS.md` moved 24,934 → 29,385 → 22,003**,
because `HANDOFFS.md` is in `read-mandated`, not `read-set`. **Do not cite `growth_run` as evidence
about the read set.** No phase below does.

**F7 — The read-set class total has no ceiling guard in the suite, in either unit.** The partition
test guards the *token* identity of the two members (`tools/test_context_budget.py:1258`). Nothing
asserts the class total against `read_cap_tokens × 2.27`, and nothing asserts it does not rise. This
is the specific hole D1(b) fills.

---

## §5 The three shapes

**Shape A — report better, gate nothing.** Take PR #86 (or its fork-side equivalent) so the headline
stops contradicting the table, and publish the version series somewhere a release must look. Cost:
one dependency on an unreviewed PR. **Catches nothing**; F5 is the evidence that a truthful report
is necessary and was not sufficient for five months.

**Shape B — one ratchet gate on the read-set class total, canonical-only. RECOMMENDED.** Add one
entry to this repository's `.quality-gates.json`: `direction: max`, `threshold: 72535`, a `command`
that prints the total and an `extract` that reads it. Every session already runs
`quality_ratchet.py --run` and is already required to cite it. **The number can then only come
down**, and a decision to raise it is refused by the hook, must be made in its own commit with the
reason in the ledger, and is visible in the manifest's history to the dashboard. Cost: one gate
entry plus a small printer; no distributed file; nothing built inside the distributed tool.

**Shape C — distributed enforcement.** Wire the budget into the shipped hook so adopters get it too.
**This is what S3 declined.** It is in this list for completeness and because BL-91 asks whether the
gate should be distributed; it is not recommended, and it may not be proposed again without the
operator reopening S3 himself.

**Why B and not A.** A is what we have had. **Why B and not C.** C is decided. **Why the total and not
the files.** F4.

---

## §6 Decisions — none of these is ratified; D1 governs

**D1 — the shape. Governing; everything below can be deferred without blocking it.**
- **(a)** Shape A — reporting only. Inherits a dependency on PR #86 (0 reviews).
- **(b)** Shape B — one `max` gate on the read-set class total at 72,535 B, canonical-only. **RECOMMENDED.**
- **(c)** Shape C — distributed enforcement. **Requires the operator to reopen S3 himself.**
- **(d)** Nothing yet. Live and defensible: six pull requests sit upstream with 0 reviews, and this
  repository's purpose is reaching adopters through merged pull requests.

**D2 — the unit.** Bytes (what every existing instrument measures, and what `extract` reads cleanly),
tokens (what the cap is actually denominated in — 25,000 × 2.27), or dollars at a reference session
shape. **Recommended: bytes**, with the token figure reported beside it. Dollars are not available per
version (§2.4) and a gate must not imply they are.

**D3 — what a release that raises the ceiling must state.** BL-91 asks this directly. Options: nothing
beyond the ledger line the ratchet already forces; a required "what it bought" clause in the
`CLAUDE.md` §Versioning entry; or a required entry in a standing overhead table. **Recommended: the
§Versioning clause**, because that file is already the home of released-version semantics and is
already read every session.

**D4 — whether `SAFEGUARDS.md` gets the extraction lever.** §2.1: it is the only read-set file above
its v3.7 size, and the one lever that has ever worked has never been aimed at it. This is a *finding*,
not a proposal — extracting from it is its own plan.

**D5 — how BL-60 folds in.** BL-91 says it folds in as a question, not dropped. The trim-proof pile is
11.1% of the tracked repository and the largest growth term, but it is **written**, not **read** —
a different gate on a different axis. **Recommended: keep it separate.** One plan, one axis; a gate on
the read set says nothing about the write side and should not pretend to.

**D6 — procedural.** On the BL-88 plan's D6 precedent: if D1(b) is taken, the gate lands in its own
commit with its `why` field stating the measurement and date, and the receipt cites the new 12-gate
summary line.

---

## §7 Phases — if D1(b) is ratified

Each phase is ONE session and closes out when done (`SESSION_RUNNER.md` §Planning Sessions). Every
phase names the **surface** its DONE criterion is demonstrated on and what that surface cannot show.

### P1 — the printer: one line, one number, no writes

**DONE:** a canonical-only `bin/check-overhead` prints exactly one line carrying the read-set class
total in bytes and its token equivalent, exits 0, and **writes nothing** — no history append, no
`dashboard.html`. It reads `.context-budget.json` and the files it names; it does not import
`context_budget.py`'s history path.

**Why a printer and not the tool directly:** `context_budget.py --json` emits `class_totals` as a
list, so an `extract` regex would have to depend on key order to pick `read-set` over `resident` —
an operand that can silently start matching the wrong row. A one-line printer makes the gate's
measurement unambiguous, and it matches the existing `bin/check-*` family that the other gates use.

**Verify:** `bin/check-overhead` twice in a row, with `git status --short` clean after each (the
no-write assertion — F6 is why this is asserted and not assumed); the printed byte figure equals
`python3 starter-kit/context_budget.py --json | jq '.class_totals[]|select(.class=="read-set").bytes'`;
a RED-first test in `bin/tests.sh` that fails before the tool exists.

**Surface:** this repository's working tree **and** a `--no-local` clone at the commit, HEAD asserted
by sha. **What it cannot show:** anything about an adopter tree — `.context-budget.json` here is this
repo's own config, not the distributed seed, so the printer's behaviour under a seed config is
untested by construction and the phase must say so rather than leave it to be discovered.

**Session boundary:** this phase is one session. Close out when done.

### P2 — the gate: declared at the measured value, direction max

**DONE:** one entry in `.quality-gates.json` — `name: read-set-bytes`, `direction: max`,
`threshold:` the value P1's printer reports on that tree, `command: bin/check-overhead`, `extract:`
its capture, `why:` the measurement, its date, and the §2.1 series in one sentence.
`quality_ratchet.py --run` reports **12/12 pass**, and `--precommit` refuses a staged raise of that
threshold.

**The threshold is set from P1's measurement on the tree, never from this document.** 72,535 is
today's figure and will be stale; a plan that hardcodes it into a later session's gate hands that
session a wrong number. Re-measure.

**Verify, and the order matters:** `quality_ratchet.py --run` (expect 12/12, 0 fail, 0 unmeasured,
and a **moved** manifest hash — a gate was added); then, in a scratch clone, stage a raise of the
threshold and confirm `--precommit` prints `REFUSED` and exits non-zero, and stage a lowering and
confirm it passes. **A green run does not prove the gate can fail** — exercise the refusal, or the
gate is unkillable and proves nothing.

**Surface:** a `--no-local` clone at the commit with `core.hooksPath` set — **a scratch clone runs no
hooks unless you set it**, so the refusal test is meaningless without that line. **What it cannot
show:** that the gate would have refused any historical growth; the ratchet measures trees, not
history, and the counterfactual in F1 is arithmetic, not a test.

**Session boundary:** one session. Close out when done.

### P3 — the release clause (only if D3 takes the §Versioning option)

**DONE:** `CLAUDE.md` §Versioning states that a release raising the declared read-set ceiling records
what the increase bought, in that release's `docs/RELEASE_HISTORY.md` entry. One paragraph; no
renumbering; the `## Versioning` heading stays put so `CLAUDE.md#versioning` still resolves.

**Verify:** `python3 bin/check-links` OK; `python3 starter-kit/context_budget.py --json` shows
`CLAUDE.md` still under its 18,600 B resident ceiling (it is 14,392 B — this phase spends resident
budget, so measure it); `git grep -n 'CLAUDE.md#versioning'` still resolves.

**Surface:** this repository. **What it cannot show:** whether a future release actually honours the
clause — that is a prose obligation with no gate, and the phase must say so rather than imply
enforcement it does not have.

**Session boundary:** one session. Close out when done.

---

## §8 Dragons

1. **The gate will be red the day the ceiling is right.** Declared at the measured value it passes on
   arrival — which means it ratifies 72,535 B as acceptable. It stops the curve; it does not bend it.
   Anyone expecting a reduction from this plan will not get one, and §2.1's decomposition (D4) is
   where reduction actually lives.
2. **A `max` gate with no escape becomes a `--no-verify` habit.** `SAFEGUARDS.md` already prescribes
   the answer — a genuinely wrong threshold changes by plan-mode approval, in its own commit, reason
   in the ledger — and the bypass is recorded, not exempt. If a session finds itself bypassing this
   gate twice, the gate is wrong and that is a finding, not a nuisance.
3. **Do not re-derive the threshold from the token cap.** `56,750 = 25,000 × 2.27` is a *check*, never
   a formula that produces a number; BL-78 §(1) is explicit that re-deriving a budget from a ceiling
   hands the reduction straight back.
4. **`git log -- <path>` will lie to the next session that measures this.** F1: it walked 68 commits
   where `--full-history` walks 124, and understated merge-borne growth ~4x. Any re-measurement uses
   `--full-history`, and states which walk produced its number.
5. **F5's contradiction is still live.** Until PR #86 or a fork-side equivalent lands, the tool tells
   its reader *"Nothing is over a ceiling yet"* while four rows read `over`. A new gate does not fix
   that sentence, and a session that reads the tool's headline instead of its table will still be
   misled.
6. **Nothing here is upstream-facing, and that is a property to preserve, not a limitation to fix.**
   The moment this touches `starter-kit/context_budget.py` or `.githooks/`, it becomes shape C and
   runs into S3. If a phase finds itself editing a distributed file, stop and ask.
