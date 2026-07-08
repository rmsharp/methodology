# Close-Out Receipt — a durable, machine-checkable handoff artifact

**Status:** RATIFIED 2026-07-08 — all decisions settled (§12). Implementation P1→P6 pending; a separate
session (or a pre-declared vertical slice) per "1 and done".
**Date:** 2026-07-08
**Fork-only:** lives in `docs/planning/`; not part of the canonical framework or any upstream PR
(same convention as [`changelog-authoritative-ledger-gate-plan.md`](changelog-authoritative-ledger-gate-plan.md)).
Branch the implementation from `upstream/main` for a clean PR.
**Provenance:** design workflow `wf_4793d8f5-b5b` (6 readers → 5 lens proposals → ranked synthesis
+ adversarial critique). Operator scope decision 2026-07-08: **"Durable receipt + reconcile — NO CI."**

---

## 1. The problem

Last session the agent completed its work, committed cleanly, and then **fell silent — it had to be
prompted by the operator to produce the mandatory close-out report.** This is not a one-off lapse; it
sits in a structurally uncoverable gap.

Of the seven close-out sub-steps (`SESSION_RUNNER.md` §3A–3G), **only Phase 3F produces a git-tracked
artifact** (the `CHANGELOG.md` ledger entry). The other six land in transient, often-uncommitted
`SESSION_NOTES.md` (3A/3B/3C/3D) or leave no file at all (the 3G spoken report). So when a session
commits its deliverable with a clean CHANGELOG line and then goes quiet:

- the pre-commit hook is satisfied (CHANGELOG was co-staged);
- Phase 0 **reconcile-on-read passes** — the ledger frontier equals HEAD, no `git-log` gap;
- nothing anywhere records that the **handoff / report was never written.**

The enforcement audit (workflow `enforcement-mechanisms` reader) is blunt: *"NO mechanism
machine-forces the close-out report / handoff narrative — only the CHANGELOG ledger ENTRY has a
commit-time gate; the handoff is enforced solely by the accountability loop, which is retroactive,
non-blocking, and contingent on a next session running."*

## 2. The honest ceiling (read this before the design)

**A pure-instruction methodology cannot *force* a forgetful agent to act at the moment it stops.** The
only forcing function keyed on the actual session-end event is an **agent-harness stop hook**, which is
agent-specific, human-dismissable, and cannot be shipped by the methodology — only recommended.
Git has no "session-end" hook; the operator has (correctly) declined server-side CI for this docs-only
repo, and CI would have been canonical-only anyway — it never reaches the solo-adopter-session
population that actually hit this failure.

So this plan does **not** claim to *prevent* the silence. What it does, and all it honestly does:

> Convert the handoff from a **no-trace transient** into a **durable, committed, machine-checkable
> artifact whose absence or incompleteness is auto-detected at the next Orient** — a strict
> improvement over today's "vanished, no evidence." True dependability still rests on
> reconcile-on-read running next Orient — the same keystone, and the same instruction-class ceiling,
> as the v3.1 ledger.

This mirrors v3.1 exactly: **gate-on-write AND reconcile-on-read**, because no write-gate is dependable
alone.

## 3. Scope decision (ratified 2026-07-08)

**Chosen: durable receipt + reconcile, agent/vendor-neutral, no server-side CI.** The four layers,
honestly ordered by what they actually deliver:

| Layer | Mechanism | Agent-independent? | Ships to adopters? | What it delivers |
|-------|-----------|:---:|:---:|------------------|
| **Core** | `HANDOFFS.md` receipt + `bin/check-handoff` + Phase 3D/3G write-step | ✅ | ✅ (receipt as SEED) / checker canonical-only | Handoff is durable; its absence is machine-detectable |
| **Backstop** | Phase 0 reconcile-on-read greps for a missing/pending receipt | ✅ | ✅ (synced Phase 0) | Catches the omission **next Orient** — the real keystone |
| **In-session catch** | *Recommend* a harness stop hook (SAFEGUARDS/BOOTSTRAP) | ❌ agent-specific | recommendation only | The only thing that heads off "had-to-be-prompted"; can't be shipped |
| **Framing** | Strengthen FM #6 + degradation row + Learning #9 | ✅ | ✅ (synced) | Names the failure; wires detection into the protocol |

**Explicitly out of scope** (per the scope decision): `.github/workflows/` / GitHub Actions / any
required-status-check merge gate. The `bin/check-handoff` script still makes the artifact **locally
CI-testable** (it is wired into `bin/tests.sh`); standing up a server-side pipeline is a separate,
later, operator-gated decision if ever.

## 4. The artifact — `starter-kit/HANDOFFS.md`

A new **receipt ledger**, deliberately a **structural twin of `starter-kit/CHANGELOG.md`**: append-only,
newest-on-top, `SEED` disposition, same seed-sentinel + `SEED_FORMAT_MARKERS` treatment. It reuses the
existing ledger machine one layer up — zero new concepts for `bin/sync`, `bin/status`, or reconcile.

**It does NOT replace `SESSION_NOTES.md`.** The load-bearing `SESSION_NOTES ↔ CHANGELOG` distinction
(transient scratchpad vs cumulative ledger) is preserved; `HANDOFFS.md` is a **third durable role** —
the *distilled, machine-checkable receipt* of each session's handoff. `SESSION_NOTES.md` stays the rich
working scratchpad; `HANDOFFS.md` is the greppable proof-of-close-out.

### 4.1 Granularity & keying — **one block per SESSION**, not per commit

One `handoff` block per session matches "1 and done" (a multi-commit vertical slice still writes exactly
one receipt) and **sidesteps the SHA chicken-egg** (the receipt is committed *in* the same commit whose
SHA it would name). Keyed on **session number + date**, not SHA. The shared key with the action ledger is
`changelog_ref`. `commit:` is written `pending` and reconciled to a short-SHA by the next session,
exactly as the ledger backfills.

### 4.2 Format — a fenced `handoff` block (front-matter keys + prose body)

````markdown
```handoff
session: S<N>
date: YYYY-MM-DD
status: pending            # "pending" at Phase 1B claim; "complete" at Phase 3D close-out
self_score: <1-10>         # Phase 3D field 6 — this session's own score
predecessor_score: <1-10>  # Phase 3A evaluation — OMITTED only on Session 1
active_task: <field 1 — current state>
what_was_done: <field 2 — must contain a sha-token OR the literal `pending`>
next_steps: <field 3 — specific & actionable>
key_files: <field 4 — each entry carries a `path:line` token>
gotchas: <field 5>
runtime_smoke: <Phase 3E — a run result, OR "n/a — docs-only", OR "impossible: <reason>">
changelog_ref: <pointer into CHANGELOG.md — PR #N / short-sha>
commit: pending            # reconciled to a short-sha by the next session
```
<free-text prose: the durable proxy for the 3G spoken report + the +/- self-score breakdown>
````

The front-matter keys are the six mandatory Phase 3D fields (`SESSION_RUNNER.md:239-246`) plus the two
distinct 1–10 scores. **`self_score` and `predecessor_score` are separate keys** so one can never
vacuously satisfy the other (closes the field-6-vs-3A ambiguity the readers flagged).

### 4.3 The Phase 1B refinement — the receipt stub IS the breadcrumb

**This resolves the critic's "commitless seal paradox."** Rather than a separate transient
`CLOSEOUT: pending` token in `SESSION_NOTES.md` (which does not survive a fresh clone), the receipt
**stub is written at Phase 1B and committed with the session claim**, carrying `status: pending`.
This unifies with the *existing* Phase 1B `CHANGELOG: pending` breadcrumb (`SESSION_RUNNER.md:77-91`):

- **Claim (1B):** write the `handoff` block with `status: pending` and the fields it can fill now.
- **Close-out (3D):** overwrite it in place to `status: complete`, fill all fields.
- **Crash between:** the committed `status: pending` block is the durable, fresh-clone-visible
  breadcrumb the next session's Phase 0 greps.

The receipt stub is committed *within the existing 1B claim commit* — no extra commit, and the
pending marker survives off-machine because it is committed, not working-tree-only.

### 4.4 SEED disposition & stale-format marker

Add to `bin/_manifest.py`:
- `("starter-kit/HANDOFFS.md", "HANDOFFS.md", SEED)` in `DISTRIBUTION` (adopter root, write-once,
  never clobbered — same class as `CHANGELOG.md`).
- `SEED_FORMAT_MARKERS["HANDOFFS.md"] = "Handoff Receipts"` (a lifetime-stable title token, NOT the
  deletable seed-sentinel — same reasoning as the CHANGELOG entry at `_manifest.py:83-85`), so
  `bin/status` reports a pre-format adopter receipt `present (stale format)`, advisory-only.

## 5. The checker — `bin/check-handoff` (canonical-only, python3 stdlib)

Same shape as `bin/status`/`bin/check-links`: shebang, `sys.path.insert(0, BIN)` → `import _manifest`,
`argparse`, exit `0`/`1`. **Not** added to `bin/_manifest.py` (canonical-only, per scope + the BL-6
item-3 hook precedent).

**Modes:** `--range base..head` (a commit span); default = HEAD's block via the HANDOFFS frontier
(`git log -1 --format=%H -- HANDOFFS.md`, same computation reconcile uses); `--file <path>` (fixture,
for tests).

**Asserts (structural — statically gradeable):**
- a ```handoff` block exists for the range;
- every required key present and non-empty;
- `self_score` / `predecessor_score` are integers 1–10 and **distinct keys**;
- each `key_files` entry carries a `:line` token;
- `what_was_done` carries a sha-shaped token **or** the literal `pending`;
- `status: complete` for a closed session (a lingering `pending` in-range is a finding).

**Anti-pattern lints (exit 1):** reject `pick next( from)?( the)? backlog`, empty/whitespace
`next_steps`, `need to verify`, and bare placeholders (`TODO|TBD|Done\.|Fixed stuff|\.\.\.`) in a
non-exempt field. **Isolate the fenced block from surrounding prose before grepping** so an advisory
note can't vacuously satisfy a field (the BL-6 Test-20 lesson — see
[[feedback_test_output_isolate_row_from_advisory_prose]]).

**Exemptions (so it never false-fails a legitimate close-out):** Session-1 (no `predecessor_score`);
empty-diff/no-action (`--allow-none`); a recorded `CLAUDE.md` "no HANDOFFS" opt-out; `runtime_smoke:
n/a — docs-only` is a valid value; `commit: pending` accepted (reconciled next session).

**`bin/tests.sh` wiring:** append `== Test 21 ==` / `== Test 22 ==` blocks over `mktemp` fixtures
(well-formed passes; each missing/empty field fails; abdication phrase fails; `key_file` without
`:line` fails; `commit: pending` passes; Session-1 without `predecessor_score` passes; a prose note does
not satisfy a field). The suite self-counts via `$PASS`/`$FAIL` (no total constant to bump), **but** the
fixed check-count prose in `README.md`/`CLAUDE.md` ("54 → 5x checks") must be hand-updated in the same
change (Learning #7 cross-reference hazard — grep it).

## 6. The backstop — Phase 0 reconcile-on-read extension

Extend the Phase 0 step-6 reconcile (`SESSION_RUNNER.md:18`, mechanics `:35-42`) to cover the receipt,
for the case CI could never see (a session that committed but wrote no receipt, or crashed):

- **Detection signal:** at Orient, compute the HANDOFFS frontier and (a) diff `git log
  <changelog-frontier>..HEAD` for commit spans with **no corresponding `handoff` block**, and
  (b) grep `HANDOFFS.md` for a trailing block still at `status: pending` (a crashed session).
- **Backfill action:** if the prior session left commits but no complete receipt, reconstruct a
  best-effort receipt block from `git log` + the (transient) `SESSION_NOTES.md` if still present, mark
  it `status: reconciled`, and note the gap in the Phase 0 report — the same "repair the record"
  posture as the ledger backfill, done during step 6 before the report and STOP.

## 7. Framing — FM decision, degradation row, Learning #9

**Recommended: strengthen FM #6, do NOT mint FM #28.** The report/handoff failure is already tiled by
FM #6 (skip close-out), #10 (skip handoff evaluation), and #15 (minimal handoff); v3.1's FM #27 carved a
genuinely *uncovered* artifact (the ledger), whereas this failure is a non-compliance with an existing
AUTOMATIC phase. Minting FM #28 dilutes the guarded "empirically-derived failure modes" invariant.
**(Decision D1 — RATIFIED 2026-07-08: strengthen FM #6; FM count stays 27.)**

Under the recommended path:
- **FM #6** (`SESSION_RUNNER.md:298`): extend the countermeasure to name the durable receipt — *"…
  Close-out is not done until the `HANDOFFS.md` receipt is written; its absence is detected at the next
  Orient."*
- **Degradation Detection** (`:327-345`): add a row — *"Ledger frontier advanced this session but the
  Phase 1B receipt stub was never completed (`status: pending`) → FM #6 active → complete the receipt
  before the final commit."* (the git-visible XOR signal).
- **Learning #9** (append after #8 at `:364`; append-only): *"The handoff is only dependable when it is
  a durable, machine-checkable artifact — a transient narrative leaves no evidence of its own absence.
  Gate-on-write (the receipt + `bin/check-handoff`) AND reconcile-on-read (Phase 0 greps for a
  missing/pending receipt), because neither is dependable alone. Learning #8 applied to the report
  itself, not just the ledger."*

## 8. In-session catch — the harness stop-hook recommendation (recommendation layer only)

A new subsection in `starter-kit/SAFEGUARDS.md` (and a pointer in `BOOTSTRAP.md`) that **recommends,
never ships**, an agent-harness session-end hook that re-prompts the agent to complete the receipt
before the turn ends — the fastest catch, and the only one that fires before the operator notices the
silence. Brand-neutral, reusing the v2.7.2 "agent-level memory"-style framing (the hook is
agent-specific; different harnesses implement it differently or not at all). Carries the same "fast
path, not the guarantee" disclaimer the pre-commit hook already carries. **Default posture: soft-remind**
(agent retains control — avoids livelock), noted as open decision D7.

## 9. Distribution split

| Artifact | Disposition | Rationale |
|----------|-------------|-----------|
| `HANDOFFS.md` | **SEED → adopters** | Adopters need the durable-handoff discipline; same class as their `CHANGELOG.md` seed |
| Synced Phase 3D/3G/1B/Phase-0 wording, FM #6, degradation row, Learning #9 | **TRACKED → adopters** | The instruction-class enforcement travels with `SESSION_RUNNER.md` |
| `bin/check-handoff`, its `bin/tests.sh` blocks | **canonical-only** | Not in `_manifest.py`; adopters who want a local checker copy the portable stdlib script (BL-6 item-3 precedent) |
| SAFEGUARDS stop-hook recommendation | **TRACKED → adopters** | Recommendation text travels; the hook itself is never shipped |

Adopter net-new burden: **~10 structured lines at close-out** instead of only prose in transient notes.
Everything mechanical is opt-in. Graceful degradation: an adopter whose seed predates the change simply
has no receipt-format marker — `bin/status` flags it advisory-only; nothing false-alarms.

## 10. Honest ceiling — what this does NOT do (from the adversarial critique)

State these verbatim in the shipped docs so the ceiling is not narrower than reality:

1. **Semantic quality is never certified.** A well-formed but hollow or wrong receipt (`next_steps: "do
   the thing"`; line numbers pointing at the wrong code; a dishonest `self_score`) passes every static
   check. Faithfulness stays a next-session 1–10-scoring property. **A green `bin/check-handoff` must
   never be read as "good handoff"** — that conflation is FM #17 in a tool costume.
2. **A session that makes no commit AND never reached Phase 1B** leaves nothing — no receipt stub, no
   `git-log` gap. (A *correctly-run* session is not commitless: 1B commits the stub. The uncovered case
   is a session that skipped 1B entirely — a pre-existing FM #14 gap, out of scope here.)
3. **Frontier-poisoning transfers verbatim** from the ledger: a commit that lands without a receipt but
   later falls *behind* the next HANDOFFS-touching commit is never inside `frontier..HEAD` and is not
   backfilled. Same soundness gap as the ledger; carry it into the ceiling note.
4. **Delete + opt-out** silently disables the receipt discipline (parallels the `CHANGELOG` delete
   escape) — an accepted, `CLAUDE.md`-recorded opt-out, not a bug, but name it.
5. **The Phase 3G spoken report is inherently non-persistable** — the receipt asserts the prose body
   exists, never that the operator was verbally briefed.
6. **Non-commit actions** (release, tag, PR-open, issue-close, access-grant, grooming) leave no diff and
   trigger no receipt — they remain the FM #27 Phase 3F ledger write-gate's job, exactly as today.

## 11. Implementation phases (one session each; per-phase completion criteria)

Horizontal by default; MAY be run as a pre-declared vertical slice under the §Vertical Slice Sessions
gates if the operator pre-approves this exact layer set. Each phase closes out (dogfood: each writes its
own `HANDOFFS.md` receipt once the artifact exists — Phase P1 seeds it first).

- **P1 — Artifact + manifest.** Create `starter-kit/HANDOFFS.md` (twin of the CHANGELOG seed); add the
  `DISTRIBUTION` + `SEED_FORMAT_MARKERS` entries. **DONE:** `bin/status` on a fresh sync shows
  `HANDOFFS.md present`; a pre-format fixture shows `present (stale format)`; `bin/sync` never clobbers
  it. **Verify:** `bin/tests.sh` green.
- **P2 — Checker + tests.** Add `bin/check-handoff` + Tests 21–22. **DONE:** all new assertions pass;
  README/CLAUDE check-count prose updated. **Verify:** `bin/tests.sh` green; `bin/check-handoff --file`
  on good/bad fixtures exits 0/1 correctly.
- **P3 — Protocol wiring (the write-step).** Edit `SESSION_RUNNER.md` §1B (receipt stub), §3D (write the
  receipt), §3G, and `ITERATIVE_METHODOLOGY.md` Phase 6; reconcile into **every** session-type +
  campaign checklist (Learning #8 meta-gate — Planning `:142`, Vertical-slice revert `:155`, Debugging,
  Review/Audit, both campaigns). **DONE:** grep confirms the receipt step in each checklist. **Verify:**
  Learning #8 reconciliation grep clean.
- **P4 — Backstop.** Extend Phase 0 step 6 reconcile (`:18`, `:35-42`) with the receipt detection +
  backfill. **DONE:** a fixture repo with a committed-but-unreceipted commit is detected at a simulated
  Orient. 
- **P5 — Framing + recommendation.** Strengthen FM #6, add the degradation row, append Learning #9, add
  the SAFEGUARDS stop-hook recommendation + BOOTSTRAP pointer. **DONE:** cross-reference grep (Learning
  #7) clean; FM count unchanged at 27 (recommended path).
- **P6 — Dogfood + close.** Run the full suite, update `CLAUDE.md` §Versioning + root `CHANGELOG.md`
  ledger, confirm both dashboard twins byte-identical if touched.

## 12. Operator decisions — RATIFIED 2026-07-08

**Settled:** D1 → strengthen FM #6 (FM count stays 27). D2 → per-session `handoff` block as specified.
D3 → fold the breadcrumb into the Phase 1B receipt stub. D4 → version event deferred to merge (per
"not every contribution needs a release"). D5 → soft-remind stop-hook. Implementation may begin (P1).

| # | Decision | Ratified choice |
|---|----------|----------------|
| **D1** | New **FM #28** ("silently-skipped close-out") vs **strengthen FM #6** + degradation row + Learning #9 (FM count stays 27) | **Strengthen FM #6** — the failure is non-compliance with an existing AUTOMATIC phase, already tiled by FM #6/#10/#15. But minting a genuinely-new durable artifact is arguably as novel as the ledger → real call. |
| **D2** | Artifact format & granularity: fenced ```handoff` block, one per **session**, keyed session#+date (§4) | Confirm as specified (rejected: per-commit files and SHA-keyed blocks — both hit the chicken-egg). |
| **D3** | Fold the crash breadcrumb into the committed Phase 1B **receipt stub** (§4.3) vs a separate `SESSION_NOTES` seal | **Fold into the receipt stub** — resolves the fresh-clone paradox; one artifact, committed. |
| **D4** | Version event at merge | Likely a **CLAUDE.md §Versioning entry** (v3.3 minor) *or* none, per your "not every contribution needs a release" guidance. Defer to merge; not presumed. |
| **D5** | Stop-hook default posture in the SAFEGUARDS recommendation | **Soft-remind** (agent keeps control; avoids livelock). |

---

*Once these are ratified, implementation is P1→P6 above, one session each (or a pre-declared slice), on
a branch off `upstream/main`. This plan is the Present-phase deliverable; no framework files are touched
until it is ratified.*
