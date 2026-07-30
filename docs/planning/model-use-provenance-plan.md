# Model-Use Provenance — a plan to record which model(s) ran each session

**Status:** RATIFIED 2026-07-30 — operator decisions D1–D4 taken (§9). Implementation P1→P3 pending;
a separate session per "1 and done" (P3 additionally gated on upstream PR #63 merging first — see P3).
**Date:** 2026-07-30. **Session:** S18 (planning session; deliverable is this document, not
implementation, per the S18 claim stub's own `active_task`).
**Scope:** Canonical methodology feature (`starter-kit/CHANGELOG.md`, `starter-kit/HANDOFFS.md`,
`starter-kit/SESSION_RUNNER.md`, new canonical-only `bin/model-report`). One fork-only touch point:
`docs/planning/BACKLOG.md` BL-8 gets an informational pointer in P3 — this plan does not resolve BL-8.
**Motivated by:** [BL-8](BACKLOG.md) (reopened 2026-07-25, sequenced after the now-closed dashboard
signal-integrity campaign) and general session-provenance/audit value, independent of BL-8.
**Provenance:** design workflow `wf_b2c55b26-bec` (3 independent candidate designs → 3 judges scoring
all candidates on 4 lenses → ranked synthesis grafting the best-verified elements of each → adversarial
completeness-critic pass on the synthesis; 8 agents, 733k tokens, 121 tool calls, all claims grounded in
direct `Read`/`Grep`/`git log` against this repo, not assumed). Operator ratified the synthesis's
recommendation on all 4 forks put to them (§9); two defects the completeness critic found in the
synthesis are corrected in place below (§8 Phase 1 completion criteria; §4.3 insertion anchor).

---

## 1. The problem

No methodology-defined field records which model executed a session, an action, or a layer of a
capability-tiered slice. Model identity currently leaks out only two ways, both incidental:

1. **Ad hoc free-text prose** inside a `HANDOFFS.md` receipt — e.g. session S1's real receipt
   (`HANDOFFS.md:729`): *"Hybrid model split: Sonnet 5 built P2/P4, Opus 4.8 did P3/P5/P6 and reviewed
   all Sonnet output."* This happens only on the minority of sessions that use capability-tiered review
   (`starter-kit/SESSION_RUNNER.md` §Vertical Slice Sessions, v3.5/BL-7); most sessions say nothing
   about model at all.
2. **Git `Co-Authored-By` trailers** — a Claude-Code/git convention, unrelated to either of the
   methodology's own schemas, unverifiable, agent-specific, and queryable only by grep archaeology.

Neither `REQUIRED_KEYS` in `bin/check-handoff:51-55` (13 keys) nor `starter-kit/CHANGELOG.md`'s
documented bullet set has a model field. BL-8's own evidence is that the absence is costly: its
cost/quality comparison (all-Opus $132 / all-Sonnet $79 / hybrid ~13–19% saving,
[`BACKLOG.md`](BACKLOG.md)) came from **one** session hand-measuring 48 subagents — expensive, one-off,
not repeatable across many sessions without a durable per-session record to mine.

## 2. Evidence-based inventory (grep-based, MANDATORY per Planning Sessions)

| Claim | Verified |
|---|---|
| `bin/check-handoff` `REQUIRED_KEYS` — 13 keys, no `model` | `bin/check-handoff:51-55` |
| Only the newest receipt (`blocks[0]`) is ever validated | `bin/check-handoff:255` |
| `starter-kit/CHANGELOG.md` bullets are documented "recommended," not required; no structural checker exists for CHANGELOG entries today | `starter-kit/CHANGELOG.md:33-38`; `bin/tests.sh` has no CHANGELOG-entry checker (Tests 1-20 cover sync/status/dashboard; 21-22 cover `check-handoff` only) |
| Root `CHANGELOG.md` has **52** `### ` entries; root `HANDOFFS.md` has **19** `handoff` blocks (18 closed + S18's `pending` stub) | `grep -c '^### ' CHANGELOG.md` → 52; `grep -c '^```handoff$' HANDOFFS.md` → 19 |
| `CHANGELOG.md` and `HANDOFFS.md` are both `SEED` disposition; `RECOMMENDED_SKILLS.md` and `SESSION_RUNNER.md` are `TRACKED` | `bin/_manifest.py:46-47` (SEED), `:35-37` (TRACKED) |
| `SEED_FORMAT_MARKERS` keys **only** on a stable per-file title string (`"Handoff Receipts"`, `"Authoritative Action Ledger"`), never on any particular field's presence | `bin/_manifest.py:90-93` |
| `RECOMMENDED_SKILLS.md` already carries brand tokens ("Sonnet", "Opus") in an illustrative table and the capability-tiered-review addendum; `starter-kit/HANDOFFS.md`, `starter-kit/CHANGELOG.md`, and `starter-kit/SESSION_RUNNER.md` carry **zero** | `grep -inE "Opus\|Sonnet\|Haiku\|Fable" starter-kit/RECOMMENDED_SKILLS.md` → 3 matching lines (5 occurrences); same pattern against the other three → 0 hits (exit 1) |
| v3.6's own campaign already produces one `CHANGELOG.md` entry **per layer/checkpoint commit** (Layers 1–8) | 7 distinct `### 2026-07-*` Layer headers in root `CHANGELOG.md` |
| Git history: 323 total commits; 205 carry a `Co-Authored-By` trailer (8 distinct strings), 118 carry none — **~63.5% coverage, not "essentially all commits"** | `git log --all --format='%H'\|wc -l` → 323; `git log --all --format='%(trailers:key=Co-Authored-By,valueonly)'` filtered non-empty → 205; distinct values sorted → 8 |
| One trailer value is a human, not a model: `R. Mark Sharp <rmsharp@me.com>` | same scan, 1 hit |
| **The flagship multi-tier example is internally inconsistent between its own prose and its own trailers.** S1's receipt (`HANDOFFS.md:729`) says *"Sonnet 5 built P2/P4, Opus 4.8 did P3/P5/P6."* All six of S1's real checkpoint commits (`4f0bea7`, `1646773`, `f722a84`, `afbbe7d`, `5f13c99`, `719a41d`) — **including the two the receipt attributes to Sonnet** — carry the identical trailer `Claude Opus 4.8 (1M context)`. The receipt's own `commit:` field (`e5638af`) points at the PR-merge commit, which carries **no** trailer at all. | Reproduced directly: `git log -1 --format='%(trailers:key=Co-Authored-By,valueonly)' <sha>` for each of the 7 shas |
| `docs/planning/BACKLOG.md` BL-8 is fork-only, sequenced after the (now-closed) dashboard campaign, and explicitly states single-tier remains the default | [`BACKLOG.md`](BACKLOG.md) |
| No file in the corpus currently uses the literal token `Model:` in any schema/format section | `grep -rn "Model:" starter-kit/ HANDOFFS.md CHANGELOG.md` → 0 hits (clean namespace) |
| `ITERATIVE_METHODOLOGY.md` (repo root, not `docs/methodology/` in the canonical checkout) already contains the literal string `"Claude Code"` twice, unrelated to model tiers (the v2.6 skill-citation convention) — a naive `grep "Claude "` (trailing space) would false-positive on it | `grep -n "Claude" ITERATIVE_METHODOLOGY.md` → lines 379, 381 |
| `starter-kit/SESSION_RUNNER.md`'s Phase 3F first bullet does not end at "...remove it from `BACKLOG.md` in the same commit." — that phrase is mid-sentence, immediately followed by the absent-ledger exemption clause; the bullet's real end is "...FM #17: the ledger records what the session did; it does not authorize a second deliverable)." | `starter-kit/SESSION_RUNNER.md:276` (full bullet text) |
| `starter-kit/SESSION_RUNNER.md`'s Learnings table currently ends at **#12** on this branch (`starter-kit/SESSION_RUNNER.md:377`); **#13** ("a handoff's predictions decay") exists only in unmerged upstream PR #63 | `starter-kit/SESSION_RUNNER.md:363-377`; `gh pr view 63 --repo KJ5HST/methodology` → OPEN |

The trailer-vs-prose row is the single most consequential finding of this planning session, and it
reshapes the recommendation below: **a git commit trailer records who ran `git commit`, not which
capability tier authored the content.** For the exact motivating multi-tier use case (BL-8-style hybrid
sessions), the trailer signal is not merely agent-specific — it is **actively wrong**, while the
session's own self-reported prose was correct. Any design that treats trailers as a source of truth for
tier attribution repeats this repo's own v3.2/v3.6 lesson ("a proxy presented as a semantic finding")
in a new subsystem.

## 3. Design-panel summary

Three candidates were scored by three judges on four lenses (brand-neutrality/honesty,
blast-radius/migration, SEED-mechanics fit, value-vs-overhead). Ranking split 1-1-1 across judges
(`convention-no-schema` 1st once, `changelog-line` 1st twice, `handoffs-field` never 1st). Adjudicated
against direct repo verification in §2:

- **`handoffs-field`** (add `model:` to the fixed `handoff` block) has the cleanest single-field
  mechanism and correctly states the self-report honesty ceiling, but its central migration argument —
  that `bin/status` will auto-flag existing adopters as stale once the schema doc changes — is **false
  as designed**: `SEED_FORMAT_MARKERS` keys on a title string the change never touches, so `STALE_SEED`
  never fires. All three judges independently caught this. It also can't scale past a small number of
  tiers (S14's real 40-subagent sweep has no per-tier breakdown in its receipt at all) without inventing
  new grammar.
- **`changelog-line`** (add an optional `**Model:**` bullet to `CHANGELOG.md`'s per-action entry) won
  or tied on 4 of 6 direct comparisons across judges, and every specific factual claim it made was
  independently verified true (52 entries, no marker-bump needed, per-layer granularity already in
  production via v3.6). Its main weakness — no checker scheduled — is real but not disqualifying
  (`CHANGELOG.md` has never had one).
- **`convention-no-schema`** (formalize prose + a git-trailer-reading `bin/model-report`, no schema
  change anywhere) is the lowest-blast-radius candidate and the only one to place its doc changes in a
  `TRACKED` file (so it actually propagates to already-adopted repos via `bin/sync`, unlike A/B's
  SEED-only edits). But its headline "already free, near-100%-coverage" claim is contradicted by the
  repo's own flagship example (§2): the trailer signal is not just agent-specific, it is **wrong** for
  the exact case that matters most.

No single candidate won outright. The ratified design below takes B's field mechanism and placement
(best-verified, best multi-tier fit), grafts A's honesty-ceiling phrasing and C's TRACKED-propagation
insight, and ships a corrected (never-authoritative-trailers) version of C's reporting tool. It
explicitly discards A's schema-checker-on-`HANDOFFS.md` approach and C's "trailers are near-free
coverage" framing as each having a concrete, verified defect.

## 4. Ratified design

### 4.1 Primary field — optional `**Model:**` bullet in `CHANGELOG.md`'s per-action entry

Add one optional 4th bullet to the format documented in `starter-kit/CHANGELOG.md`'s "How to add an
entry" section (currently 3 bullets: Change / Commit-PR / Session+Verified). Appended as its own
bullet, not spliced into the existing Session/Verified bullet:

```
### YYYY-MM-DD · [SOURCE] one-line outcome-focused summary
- **Change:** what is now true in the repo/product that was not before
- **Commit/PR:** `<short-sha>`  —or—  PR #<N> (merged `<sha>`)
- **Session:** S<N> · **Verified:** <build/test/render/runtime evidence, or "n/a — docs-only">
- **Model:** <value>                              (optional — omit the line entirely when not recorded)
```

Value grammar (free text, agent-independent field *name*, concrete session-specific *value* — the same
pattern `key_files` already uses for paths):

- Single-tier: `**Model:** Claude Opus 5` — one token.
- Capability-tiered: because `CHANGELOG.md`'s unit of record is already the *action*, not the session
  (proven by the real Layer 1–8 entries), each tier's own entry just states its own role — no
  compound/delimited grammar to invent:
  - On a delegated layer's entry: `**Model:** Claude Sonnet 5 (delegated; reviewed by Claude Opus 4.8)`
  - On a primary/judgment layer's entry: `**Model:** Claude Opus 4.8 (primary)`

This is why B outscored A on the multi-tier lens: S14's real 40-subagent sweep naturally decomposes
into however many `CHANGELOG` entries the session already writes for its layers/checkpoints, each
carrying its own short tag — never a single line trying to compress 40 subagents into one field.

**Why `CHANGELOG.md` and not `HANDOFFS.md`'s fixed schema:** `starter-kit/CHANGELOG.md`'s own inclusion
test — *"would the operator, six months out, need this to know what the repo does or how it got
there?"* (`starter-kit/CHANGELOG.md:52-58`) — is satisfied by model identity exactly as it is by
`Commit/PR` or `Verified`. Adding it to `HANDOFFS.md`'s `handoff` fence would touch
`REQUIRED_KEYS`/`KEY_RE` in a 269-line, already-tested checker for a field the checker can only
rubber-stamp as present, and its supporting migration claim (§3) doesn't hold. `CHANGELOG.md`'s bullets
are already documented as "recommended, not required," so one more optional, additive line is the
smallest departure from the file's existing formality bar.

### 4.2 Session-level lookup — formalize (not schema-ize) `HANDOFFS.md`'s existing free-text convention

No new key is added to the `handoff` fence — `REQUIRED_KEYS` stays at 13, `bin/check-handoff` is
untouched. Instead, `starter-kit/HANDOFFS.md`'s "How to write a receipt" section gains one clause
formalizing what S1's receipt already did organically: when a session-level summary is useful
(especially the common single-tier case, where one line answers "which model ran this session" without
cross-referencing `CHANGELOG.md`), the closing agent may write one sentence in the receipt's free-text
prose area (already documented as *"the durable proxy for the Phase 3G spoken report"*), citing S1's
own sentence as the precedent pattern. This resolves "provenance lookup for one session now means
correlating multiple `CHANGELOG` entries" without creating a second structured field that duplicates
the `CHANGELOG.md` bullet — the free-text area already exists, is already documented, and this only
adds a one-clause pointer to an established convention.

### 4.3 Propagation to already-adopted repos — one clause in `SESSION_RUNNER.md` Phase 3F

Both `starter-kit/CHANGELOG.md` and `starter-kit/HANDOFFS.md` are `SEED` disposition: `bin/sync` never
overwrites either file once an adopter has one. Editing their format sections reaches **new** adopters
bootstrapping after this ships, but reaches **zero** already-adopted repos (including this fork's own
root files) automatically — the gap `RECOMMENDED_SKILLS.md`-only placement would have sidestepped by
living in a `TRACKED` file instead.

**Ratified fix (D2):** add one clause to `starter-kit/SESSION_RUNNER.md`'s Phase 3F first bullet — a
`TRACKED` file, so it propagates to every already-adopted repo via ordinary `bin/sync`.

**Corrected insertion point** (the synthesis's original anchor was mid-bullet, flagged by the
completeness critic and confirmed in §2): the bullet at `starter-kit/SESSION_RUNNER.md:276` does **not**
end at "...remove it from `BACKLOG.md` in the same commit." — that phrase is immediately followed by
the absent-ledger exemption clause. The correct append point is the **true end of the bullet**, after
"...FM #17: the ledger records what the session did; it does not authorize a second deliverable)." —
i.e. append as a new trailing sentence to the whole bullet, not spliced mid-sentence:

> *(append to the existing Phase 3F first bullet, after its closing "...does not authorize a second
> deliverable)."):* Optionally tag the acting model with a `**Model:**` bullet when it's known and worth
> recording (`CHANGELOG.md`'s own format section documents the convention and the capability-tiered
> grammar).

Brand-neutral clause (no "Sonnet"/"Opus" — matches `SESSION_RUNNER.md`'s existing style of naming the
mechanism, not the brand), one sentence appended to an already-dense bullet.

### 4.4 Tooling — `bin/model-report` (canonical-only, non-gating reporter, built now per D3)

Reads three sources and **keeps them visually and structurally separate — never merges them into one
number**:

1. **Primary / structured:** `**Model:**` bullets in `CHANGELOG.md` (§4.1) — self-reported, explicit,
   per-action.
2. **Secondary / best-effort:** free-text `Model:`-shaped sentences in `HANDOFFS.md` (§4.2) —
   regex-fuzzy by nature, labeled as such.
3. **Corroboration-only, explicitly non-authoritative (D3):** git `Co-Authored-By` trailers — included
   only as raw supplementary data, under a hard-coded disclaimer citing the S1 case verbatim (§2) as
   concrete proof that trailer identity can contradict correct self-reported tier attribution. The tool
   must never present trailer data merged with sources 1–2, and must flag the one known non-model
   trailer pattern (`rmsharp@me.com`) rather than silently counting it as a model.

No pass/fail exit code — a reporter, not a gate, matching `bin/check-handoff`'s honesty-ceiling framing
("verifies presence/structure, never truth") but going one step further: this tool cannot even verify
presence/structure of a *true* fact, only of a *self-reported string*, so its own docstring must say so
before the tool is trusted for anything beyond an informal retrospective read (i.e., feeding BL-8, not
settling it). Python3 stdlib, canonical-only — absent from `bin/_manifest.py`, same distribution class
as `bin/check-handoff`.

### 4.5 Checker / honesty-ceiling behavior (summary)

No hard gate anywhere in this design — matches the dashboard's own "advisory, never a hard gate"
posture and `CHANGELOG.md`'s existing "recommended, not required" bullets. `bin/model-report` is
non-gating. `bin/check-handoff` is untouched (no new required key, no behavior change). The only
test-suite addition is a fixture-based smoke test for `bin/model-report`'s own source-separation logic
(`Test 23`, next available slot after 22) — testing that the tool *parses* correctly, never that a
recorded model name is *true*.

## 5. Canonical vs. fork-only placement

Canonical, matching all three candidates' shared conclusion (undisputed by any judge):
`starter-kit/CHANGELOG.md`, `starter-kit/HANDOFFS.md`, and `starter-kit/SESSION_RUNNER.md` are edited
in the canonical methodology repo and apply to every adopter — the same class of change v3.3 made when
`HANDOFFS.md` itself shipped, even though its immediate motivation was this fork's own practice.
`docs/planning/BACKLOG.md` BL-8 stays exactly where it is: an operational *decision* (adopt subagent
tiering as a default, or not) that this plan does not prejudge or resolve — it only gives BL-8 (and any
future retrospective) a data source to work from. `bin/model-report` is canonical-only (adopters copy it
manually if wanted), mirroring `bin/check-handoff`'s precedent exactly.

## 6. Migration story

No backfill of the 52 real `CHANGELOG.md` entries, 19 `HANDOFFS.md` receipts, or 323 commits (D5 — see
§9 for the explicit operator confirmation). Reasons:

- **`bin/check-handoff` is untouched**, so there is no retroactive validation obligation.
- **`CHANGELOG.md` has no structural checker today**, so an optional new bullet breaks nothing that
  exists.
- **Reconstructing history would fabricate data, not recover it.** Git trailers give only 63% commit
  coverage (204/323) with one non-model value and, per §2's flagship finding, are demonstrably wrong for
  the multi-tier sessions that matter most to BL-8. A blanket backfill using trailers as ground truth
  would silently launder a known-bad signal into the new field.
- **SEED mechanics mean existing adopters' own `CHANGELOG.md`/`HANDOFFS.md` content is never touched by
  this change regardless** — `bin/sync` never overwrites a present seed, so migration for the seed
  *content* itself is not a live question; only discoverability of the new convention is, which §4.3's
  `SESSION_RUNNER.md` clause addresses for `TRACKED`-propagated visibility, and §4.1's doc-section edit
  addresses for brand-new adopters.
- **This fork adopts it starting with the implementing session's own close-out** — the natural first
  real usage, mirroring how the close-out-receipt slice itself dogfooded on the session that shipped it.

Completion evidence for "no backfill occurred": `grep -c '\*\*Model:\*\*' CHANGELOG.md` must be
**non-zero but strictly less than** the `### `-entry count (52 at time of writing) after adoption —
proving the tag is being applied going forward, not retrofitted.

## 7. Honest ceiling — what this design does NOT solve or guarantee

This is self-reported, exactly like `commit`, `self_score`, or any other field in either schema — an
agent can misreport its own model, and neither the new `CHANGELOG.md` bullet nor the `HANDOFFS.md`
free-text convention is checked for truth by anything in this design; `bin/model-report` reads and
displays, it does not adjudicate. Git commit trailers cannot serve as independent verification of tier
attribution — proven concretely, not asserted (§2). Nothing here captures actual token counts or dollar
cost — a model *name* is a proxy for cost, not cost itself; BL-8's real dollar figures still require the
kind of manual measurement S14 did, and this design only supplies the join key for that analysis, not
the analysis itself. Coverage is voluntary and starts from zero: because both touched files are SEED, no
already-adopted repo receives the new field automatically, and even the `SESSION_RUNNER.md` propagation
clause only makes the convention *discoverable* via an ordinary sync diff — an adopter that never reads
Phase 3F's updated text will never learn the convention exists. For very large fan-out sessions (S14's
real 40 subagents), this design still asks the closing agent to compress attribution into however many
`CHANGELOG` entries the session already produces; it does not mechanically enumerate every subagent's
model. And as with every other field in both ledgers, a session that leaves no commit and writes nothing
still escapes entirely — a populated field is evidence of a claim, never proof of the claim.

## 8. Implementation phases (one session each; completion criteria + verification commands)

**Phase 1 — schema/docs (canonical, docs-only).**
Edit `starter-kit/CHANGELOG.md`'s format section (add the optional `**Model:**` bullet, one single-tier
example, one capability-tiered two-entry example mirroring the real Layer 1–8 pattern, plus a short
no-duplication note against `HANDOFFS.md`'s free-text convention). Edit `starter-kit/HANDOFFS.md`'s "How
to write a receipt" section (formalize the free-text session-summary convention, citing S1's real
sentence). Edit `starter-kit/SESSION_RUNNER.md` Phase 3F's first bullet using the **corrected anchor**
from §4.3 (append after the bullet's true end, not mid-sentence). The implementing session's own
close-out is the first real dogfood use of the new `**Model:**` bullet — no separate session needed for
that.
*Completion:*
- `grep -n '\*\*Model:\*\*' starter-kit/CHANGELOG.md` shows the new convention.
- `grep -n "Model" starter-kit/HANDOFFS.md` shows the formalized free-text pointer.
- `sed -n '276p' starter-kit/SESSION_RUNNER.md` (or the then-current line) shows the new clause appended
  after the bullet's closing parenthesis, not mid-sentence — read the surrounding lines to confirm the
  original sentence about the absent-ledger exemption is undisturbed.
- **Corrected regression check** (the synthesis's original command was wrong — it included
  `ITERATIVE_METHODOLOGY.md`, which this phase never touches and which already legitimately contains
  "Claude Code," and it matched on the bare word "Claude" rather than a model-tier name):
  `grep -inE "Opus|Sonnet|Haiku|Fable" starter-kit/CHANGELOG.md starter-kit/HANDOFFS.md starter-kit/SESSION_RUNNER.md`
  must return **empty** — checking only the three files this phase actually edits, for actual model-tier
  brand names rather than the ambiguous bare word "Claude."
- `bin/tests.sh` unchanged and green (no code touched).
- This session's own `CHANGELOG.md` close-out entry uses the new `**Model:**` bullet:
  `grep -c '\*\*Model:\*\*' CHANGELOG.md` is non-zero and strictly less than 53 (52 pre-existing + at
  most this session's own, proving no backfill).

**Phase 2 — tooling (canonical-only).**
Write `bin/model-report` (§4.4): parse `CHANGELOG.md` `**Model:**` bullets (primary), `HANDOFFS.md`
free-text `Model:` mentions (secondary/best-effort), and git trailers (corroboration-only,
disclaimer-gated, never merged with 1–2). Add `Test 23` to `bin/tests.sh`: a fixture asserting the three
sources stay visually/structurally separate in the tool's output — RED-first per Learning #12's
precedent (write the fixture, confirm it fails against a naive single-merged-list implementation, then
fix).
*Completion:* `python3 bin/model-report` runs clean against this fork's real history; `bin/tests.sh`
green including the new `Test 23`; the tool's own docstring/output states the S1 trailer-vs-prose
mismatch as its cited justification for never treating trailers as authoritative.

**Phase 3 — new Learning + close the loop with BL-8 (mixed canonical/fork-only, gated on PR #63).**
**Sequencing constraint:** do not start this phase until upstream PR #63 ("Learning #13 — a handoff's
predictions decay") has merged — the Learnings table currently ends at #12 on this branch and #13 exists
only on that unmerged PR (§2); starting Phase 3 first risks two sessions both claiming "#13." Once #63
is merged, append a new row (the next available number after #13) to
`starter-kit/SESSION_RUNNER.md`'s Learnings table (canonical, `TRACKED`) capturing the finding from §2:
git commit trailers can directly contradict correct self-reported capability-tier attribution, using
S1's own case as the cited evidence (receipt says Sonnet built P2/P4; all six checkpoint commits,
including those two, are trailer-tagged Opus). Separately (fork-only, informational): run
`bin/model-report` once for real and paste a short excerpt of its output as a new dated note under BL-8
in `docs/planning/BACKLOG.md` — no BL-8 resolution, no other file changes.
*Completion:* the Learnings table's new row numbers correctly following #13, cites `HANDOFFS.md`'s S1
receipt and this plan document, and states a concrete "when to apply" rule (don't treat a commit trailer
as authoritative for tier/model attribution without corroborating self-reported prose); `grep -c '^| ' `
against the table's row count matches the expected total; `docs/planning/BACKLOG.md` BL-8 gains one
dated pointer to the `bin/model-report` output with no other file in the diff.

## 9. Operator decisions — RATIFIED 2026-07-30

| # | Decision | Options considered | Ratified |
|---|---|---|---|
| D1 | Field placement | (a) `CHANGELOG.md` bullet + `HANDOFFS.md` free-text convention [recommended] (b) zero-schema, convention+tool only (c) new `HANDOFFS.md` fenced key | **(a)** — §4.1–4.2 |
| D2 | Touch `SESSION_RUNNER.md` Phase 3F? | Yes (propagates via `bin/sync` to already-adopted repos) / No (lower blast radius on the most load-bearing file) | **Yes** — §4.3, with the anchor-point correction folded in |
| D3 | Build `bin/model-report` now or defer? | Build now as Phase 2 [recommended] / defer until BL-8 is actually revisited | **Build now**, with git trailers included only as heavily-disclaimed, never-authoritative corroboration (per the D3 sub-decision folded into the same question) |
| D4 | New Learnings-table row for the trailer-vs-prose finding? | Yes, next available number after #13 / No, this plan doc + tool docstring suffice | **Yes** — Phase 3, gated on PR #63 merging first to avoid a numbering collision |

**Session defaults adopted without a separate question** (reasonable calls per the synthesis's own
well-evidenced recommendation; flagged here for visibility, not hidden — override any of them by asking
a future session to revisit this document):

- **D5 — no one-time historical backfill for this fork's S1–S17.** Rejected on the evidence in §2/§6:
  git trailers would produce a *provably wrong* backfill for the flagship multi-tier case (S1), and 63%
  trailer coverage plus one non-model value means a blanket backfill would fabricate data it cannot
  actually recover. Coverage starts fresh at the Phase-1 implementing session's own close-out.
- **D6 — value format is free text, not a constrained grammar.** Matches the precedent `key_files`
  already sets (neutral key, concrete free-text value); a semi-structured alternative
  (`tier=<primary|delegated> model=<name>`) starts inventing a mini-DSL, the exact style the rejected
  `handoffs-field` candidate was criticized for not scaling.
- **D7 — proceed ahead of BL-9 (ledger size discipline) rather than waiting for it.** BL-9
  ([`BACKLOG.md`](BACKLOG.md)) flags `CHANGELOG.md` at 103 KB and overdue for `## YYYY-MM` sharding, and
  `HANDOFFS.md` receipts growing with no archival rule. One optional bullet per future `CHANGELOG` entry
  is a marginal size increment relative to that existing problem, and nothing in this design's shape
  depends on BL-9's resolution (a sharded ledger would still have the same per-entry bullet format). If
  BL-9 lands first, Phase 1 simply edits whatever the then-current format section says.

---

**Key files grounded by direct read in this session:** `starter-kit/CHANGELOG.md:1-58`,
`starter-kit/HANDOFFS.md:1-79`, `bin/check-handoff:1-201,255`, `bin/_manifest.py:1-93`, `bin/status`
(`SEED_FORMAT_MARKERS` usage), `starter-kit/RECOMMENDED_SKILLS.md:3,62-75`,
`starter-kit/SESSION_RUNNER.md:270-278,360-378`, `HANDOFFS.md:9-21,723-743` (S18 stub, S1 receipt),
`ITERATIVE_METHODOLOGY.md:379-381`, `docs/planning/BACKLOG.md:1-65`,
`docs/planning/close-out-receipt-durable-artifact-plan.md` and
`docs/planning/dashboard-signal-integrity-plan.md` (format precedent), `git log --all` trailer scan (323
commits, 204 trailers, 8 distinct values, 1 human), and direct per-commit trailer checks on S1's six
checkpoint shas plus its merge commit.
