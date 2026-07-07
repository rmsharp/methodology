# Authoritative CHANGELOG.md — Enforcement Gap Closer (Plan)

> **Fork-only planning proposal.** Lives in `docs/planning/`; not part of the canonical framework
> or any upstream PR (same convention as the sibling plans here). **Present-only** — this document
> is the deliverable; **no canonical file is edited until the operator approves.**
>
> **Status:** Decisions D1–D7 **ratified 2026-07-07**; ready for implementation (S2). **Date:** 2026-07-07.
> **Origin:** operator request to depend on `CHANGELOG.md` as *"the authoritative source for a
> summary of actions taken … based on our response to backlog items, repository issues, and ad-hoc
> actions."* **Scope decision (locked):** strengthen the **canonical framework** gate for all
> adopters **and** dogfood a root `CHANGELOG.md` in this repo.
> **Method:** an 8-agent design + dual adversarial-verification workflow (invariant-compliance and
> dependability). Both verdicts are recorded verbatim below; the design was *revised* in response to them.

---

## 1. The verified gap

The rule *"when you complete work, remove it from `BACKLOG.md` and add an entry to `CHANGELOG.md`"*
exists — but only as **advisory prose in setup/reference docs**, with no gate anywhere in the session loop:

| Where the rule lives | Strength | Evidence |
|---|---|---|
| Setup/reference prose | advisory | `starter-kit/BOOTSTRAP.md:132`, `starter-kit/CHANGELOG.md:6`, `README.md:96` |
| Session-start read (Phase 0) | gates **reading**, not updating; BACKLOG is the *fallback* | `SESSION_RUNNER.md:15`, `SAFEGUARDS.md:117` ("Check GitHub Issues… fall back to BACKLOG.md if no repo exists") |
| Close-out (Phase 3 / Phase 6) | **no step touches CHANGELOG** | `SESSION_RUNNER.md` §3A–3G; `ITERATIVE_METHODOLOGY.md` Phase 6 steps 1–8 |
| Dashboard | **presence only**, never freshness | `tools/methodology_dashboard.py:114-115`, checked via `full_path.exists()` (`:617`/`:627`) |

**Asymmetry that matters for "authoritative":** the one path with *any* documentation is backlog
completion. **Repository-issue responses and ad-hoc work have no CHANGELOG landing at all** — so a
ledger built on today's rules is silently incomplete for exactly two of the three sources the
operator named. And `SESSION_NOTES.md` — where "what was done" is actually recorded at close-out
(Phase 3D req #1, "ACTIVE TASK updated") — is **overwritten every session**: its durable outcome is
lost the instant the next session runs. There is no cumulative, authoritative record.

For contrast: `SESSION_NOTES.md` is protected by **four** mechanisms (the Phase 1B stub, 3A scoring,
3D's six minimum requirements, and two Degradation-Detection rows). `CHANGELOG.md` maintenance has **zero.**

---

## 2. The central finding — a write-gate alone is *not* dependable

The design's first draft was the obvious one: a hard **close-out gate** (new failure mode + degradation
row + a Phase 3F / Phase 6 step) that forces a CHANGELOG entry before commit, plus a dashboard freshness
check. The adversarial **dependability** pass (default-to-refute, against an explicit escape-path list)
returned:

> **`is_dependable: false`.**

Because a close-out gate lives in the *one place a session may never reach* (Phase 3F), and it can only
see *this* session. Eight **high-severity** escape paths let an action land in git history with **no
ledger entry**, defeating "authoritative":

1. **Ghost / crashed session (FM #14)** — checkpoint commits already landed the work; close-out never fires.
2. **Out-of-band commit** — hotfix, operator hand-commit, human-direct edit: a session-protocol step has zero reach over it.
3. **In-progress hand-off** — work committed, session ends "in progress," never "completes"; the draft's own *"completed units only"* format rule **exempts it**.
4. **Absent-CHANGELOG adopter** — an established repo that predates the feature (or never ran `bin/sync`) silently no-ops the gate — the original hole, hard-coded as a valid exemption.
5. **Canonical repo has no runner** — this repo has **no root `SESSION_RUNNER.md`**, so the gate *cannot fire on the very ledger the operator wants to depend on.*
6. **Non-commit actions** — cutting a release, mirroring a tag, opening a PR, closing an upstream issue, granting access: the gate keys on *commits*, but "actions taken" is broader.
7. **Multi-commit session** — only the terminal SHA logged; intermediate checkpoints unlocatable.
8. **Self-contradiction** — the close-out step says *"each action this session produced"* while the format says *"completed units only"*; under close-out pressure an agent invokes the permissive reading and skips.

**Conclusion that reshapes the proposal:** *authoritative* requires **two mechanisms, not one** —

- **Gate-on-write** (close-out): the fast path; logs the action while the session is live.
- **Reconcile-on-read** (orient): the **backstop** that makes the ledger *self-healing* — every session,
  at Phase 0, diffs `git log` since the ledger last moved and **backfills** any undocumented commit
  *before* new work. This is the single addition that closes escapes 1, 2, 3, 7 and backstops the rest.
  A write-gate promises *"this session won't lie."* Reconcile-on-read delivers *"the ledger is true when you read it,"* which is what "depend on it" actually means.

---

## 3. Design (five components)

### Component A — Write-time hard gate  *(gate-on-write)*

- **New failure mode `FM #27 — "Unrecorded action"`** (appended; FMs 1–26 unchanged, not renumbered):
  *complete an action and commit it, then close out without recording it in the authoritative ledger
  because the work already feels recorded in the session notes and the commit message.* Countermeasure:
  Phase 3F records every action before commit, one dated entry per action, source-tagged. Keyed to
  **file existence, not agent judgment** — "too small to log" / "batch it next time" **is** this failure mode.
- **New Degradation-Detection row:** *"Session committed an action but `CHANGELOG.md` was not touched this session → FM #27 active."*
- **Close-out step** — first bullet of `SESSION_RUNNER.md` §3F and a rewrite of `ITERATIVE_METHODOLOGY.md`
  Phase 6 step 8: append a dated, source-tagged entry for **each action**; for a backlog item, remove it
  from `BACKLOG.md` **in the same commit**.
- **Cross-source coverage:** backlog (now *enforced*, was advisory) · repository issue (**new landing**) ·
  ad-hoc (**new landing** — the source most prone to vanishing).
- **Conditional / no-op:** the gate keys on one mechanically-checkable fact — *does `CHANGELOG.md` exist
  at the project root?* The **only** opt-out is deleting the file **and** recording that in `CLAUDE.md`
  (a visible, one-time, git-traceable project decision) — never a per-session skip.

### Component B — Reconcile-on-read backstop  *(the dependability keystone — NEW, added after verification)*

Extend the existing Phase 0 **ghost-session detection** (`SESSION_RUNNER.md` Phase 0 step 5/6) with a
`CHANGELOG`-vs-`git` reconciliation: on Orient, compare `git log` since the newest CHANGELOG-touching
commit against the ledger; **backfill any undocumented commit** with a distinctly-tagged
`[backfilled — undocumented session, commits X..Y]` entry **before** starting new work. Back it with a
`CHANGELOG: pending` marker written into the Phase 1B stub so a post-compaction agent re-reading
`SESSION_NOTES.md` sees the outstanding obligation.

This is what makes the ledger **authoritative-on-read**; the write-gate alone cannot.

### Component C — Dashboard freshness monitor  *(stop rewarding mere presence)*

`"Ledger lag"` — git-only, source-agnostic, **advisory** (a RISK line + at most a 1-point documentation
nudge; **never** a hard fail — the hard gate is Component A):

- **Signal C (authoritative):** `unlogged = git rev-list --count --no-merges <last-CHANGELOG-commit>..HEAD` ≥ 10.
- **Signal B (time-lag):** ledger frontier > 21 days behind newest commit on an active repo.
- **Signal D (never-used):** file present, zero dated entries, still carries the seed sentinel on a repo with real history.
- **Signal F (the other half):** `BACKLOG.md` holds done-marked items not migrated.
- **New-adopter grace** suppresses a freshly bootstrapped seed. Split the existing
  `if has_changelog: doc_score += 2` into **+1 present / +1 fresh**. Apply to **both** byte-identical
  twins (`tools/` and `starter-kit/`); bump `DASHBOARD_VERSION`.

### Component D — Entry format + `SESSION_NOTES` division of labor

```
### YYYY-MM-DD · [SOURCE] one-line outcome-focused summary
- **Change:** what is now true in the repo/product that was not before
- **Commit/PR:** `<short-sha>`  —or—  PR #<N> (merged `<sha>`)
- **Session:** S<N> · **Verified:** <build/test/render/runtime evidence, or "n/a — docs-only">
```

`[SOURCE]` is **exactly one** uniform, greppable token — the audit
`grep -E '\[(issue #|BL-|ad hoc)' CHANGELOG.md` enumerates every logged action and proves all three
sources landed. **Reverse-chronological, newest on top** (same scan direction as `SESSION_NOTES.md`);
prepend-only, so close-out never re-sorts; promote to `## YYYY-MM` sections as it grows (time-grouped,
**not** release-grouped).

**Two files, two questions, one shared key.** `SESSION_NOTES.md` = transient handoff (*"what next, what
traps?"* — overwritten each session). `CHANGELOG.md` = cumulative ledger (*"what was done, ever?"* —
append-only). The commit SHA is the **only** intended intersection. Close-out **distills** the durable
outcome line into CHANGELOG (it does not copy the handoff); the belongs-in-CHANGELOG test is *"would the
operator, six months out, need this to know what the repo does or how it got there?"*

### Component E — Dogfood this repo

- Create a **root `CHANGELOG.md`** — this repo's own instance, **distinct from** the `CLAUDE.md`
  §Versioning ledger. It is a normally-committed canonical file; `bin/sync` never touches it (not in the manifest).
- **Boundary / anti-contradiction rule (crux):** `CLAUDE.md` §Versioning owns *released-version
  semantics* (one narrated entry per shipped version); `README.md` §What's New is its public-facing
  restatement. Root `CHANGELOG.md` is the *per-action operational timeline*, including **non-release
  work** (housekeeping, doc-only PRs, adopter-coordination, backlog retirement) that today has no home
  but raw git. Where they overlap — a release — CHANGELOG carries a **one-line pointer** into §Versioning,
  never a re-narration (cite-don't-restate), so the two ledgers **cannot diverge.**
- **"Repository issues" here = upstream KJ5HST** (the fork has Issues disabled) → cite **absolute issue
  URLs**, never bare `#NN`.
- **Bounded backfill:** ~5 verifiable entries covering everything since v3.0 (2026-06-25) — v3.0/#43,
  PR #44, backlog retirement `ff5cee9`, v3.0.1, PR #45 — plus a single pointer line for v1.0–v3.0.
  (Not start-empty: an authoritative ledger with a hole at its most-recent edge isn't dependable.
  Not full reconstruction: §Versioning already narrates every release; duplicating it violates cite-don't-restate.)

---

## 4. Dependability ledger — escape path × closing mechanism

The acceptance test for "authoritative." H/M/L = severity from the dependability pass.

| # | Escape path | Sev | Closed by |
|---|---|---|---|
| 1 | Ghost / crashed session before close-out | H | **B** reconcile-on-read backfill |
| 2 | Out-of-band commit (hotfix / hand-commit) | H | **B** + optional pre-commit hook *(decision D1)* |
| 3 | In-progress session commits, never "completes" | H | resolve gate/format contradiction: key on *"authored/retained a commit,"* not *"completed unit"* *(decision D2)* |
| 4 | Absent-CHANGELOG adopter silently no-ops | H | **self-provision** (create from seed if absent); dashboard treats *absent + commits* as a defect *(decision D3)* |
| 5 | Canonical repo has no runner to gate on | H | **E** + real enforcement hook *(decision D1)* |
| 6 | Non-commit actions (release, tag, issue-close) escape a commit-keyed gate | H | broaden the definition of "action" *(decision D4)* |
| 7 | Multi-commit session, only terminal SHA logged | M | entry carries a commit **range** / PR #; reconcile compares vs full authored set |
| 8 | New close-out step omitted from other session-type checklists | M | add to Planning / Review-Audit / Debugging / vertical-slice-revert checklists + a Learning-#7 grep reminder |
| — | Whitespace-gaming dashboard freshness; bot-commit false positives; new-adopter over-exemption | M | harden Signal C (assert a real list item added; exclude bot authors; scope the grace) |
| — | Multi-repo session logs to wrong CHANGELOG | M | extend the `SESSION_NOTES` pwd/boundary rule: N repos → N entries, reconcile per-repo |
| — | Merge-conflict drops an entry; revert leaves stale "done"; false-credit entry | L | keep-both-sides on conflict; a revert is its own append-only entry; bind entries to the Phase 3D Evidence Requirement |

**Verbatim verdicts** (for the record): invariant-compliance `overall_survives: true` (5 fixable/minor
items, §5). Dependability `is_dependable: false` **for the write-gate-only draft** — closed to *dependable*
by Component B + self-provisioning + the D1/D2/D4 decisions, **all now ratified (§6)**. The full escape-path
and `required_additions` lists are in the workflow journal (`wf_a78c8d66-d03`).

---

## 5. Invariant compliance — must-fix before **any** canonical edit

Framework rules the design must not break (from the invariants pass; the first is ship-blocking):

1. **Learning #7 count reconciliation (MANDATORY).** Adding FM #27 makes every live *"26 failure modes"*
   claim stale. Bump **26 → 27** at the **7 verified live sites** — `CLAUDE.md:77` (and change
   *"FMs 1–25 must not be renumbered"* → *"FMs 1–26"* + append *"FM #27 in v3.x"* to the parenthetical),
   `README.md:206`, `docs/tutorials/TUTORIAL_TEMPLATE.md:10`, `docs/tutorials/README.md:66`,
   `docs/tutorials/T5_cautionary.md:3/19/80`, `docs/tutorials/T2_first_session.md:116`. **Leave dated
   history verbatim** (README §What's New, `docs/planning/*`, `docs/audits/*`, `CLAUDE.md` §Versioning
   entries that read "26" as record). *"12 quality gates" is **not** affected* — this adds a failure mode
   and close-out steps, not a 13th numbered gate. All 7 sites are canonical-only → no adopter edit, no sync drift.
2. **One source-tag vocabulary.** The draft used three (`[issue #N]/[BL-N]/[ad hoc]` vs `[issue]/[backlog]/[ad-hoc]` vs prose). Pick **one** (recommend `[issue #<N>]` · `[BL-<N>]` · `[ad hoc]`) and use it verbatim in FM #27, both close-out steps, the format template, and the dogfood seed — otherwise the greppable audit silently misses entries.
3. **Anti-erosion clause (FM #17).** Add to FM #27 + the close-out step: *"The ledger records what the session did; it does not authorize what it produces. 1-and-done still bounds scope; N blocks = N layers of ONE deliverable, never N deliverables."*
4. **Two no-op cases, reconciled.** The gate is a no-op when **(a)** the project keeps no `CHANGELOG.md` by design **and (b)** the session produced no action — a Phase 0 orient-only STOP never reaches 3F. Keep "too small to log" *inside* FM #27.
5. **Dashboard wiring anchor.** Insert `metrics['changelog'] = evaluate_changelog_freshness(path, git)` **after** the metrics dict is built (after line ~1118) and **before** the scores block (~1120), in **both** twins; bump `DASHBOARD_VERSION`.

Dual-audience is respected: all **step text** lives in `tracked`/synced canonical docs; all **per-session
data** lands in the `seed`, adopter-owned `CHANGELOG.md` (never clobbered by `bin/sync`). No adopter is
ever told to edit a synced file.

---

## 6. Decisions — RATIFIED 2026-07-07

All seven accepted at the recommended default (operator). These are the campaign's binding contract;
implementation sessions S2–S7 obey them and must not re-open them without a new operator decision.

- **D1 — Canonical-repo enforcement → git pre-commit hook (DECIDED).** A `--no-verify`-bypassable
  pre-commit hook refuses a source/doc commit unless `CHANGELOG.md` is co-staged, with Component B
  (reconcile-on-read) as the guarantee. (A `CLAUDE.md` paragraph alone was rejected — structurally the
  same class as the gap.) Lands in S7.
- **D2 — Trigger key → "authored/retained a commit" (DECIDED).** The obligation keys on *"this session
  authored or retained any commit,"* **not** "completed units only." Delete the "completed units only"
  rule from Component D; in-progress and reverted-slice work logs under an in-progress marker; the only
  per-session exemption is an **empty session diff**. Closes escape #3. (This edits Component D's format spec.)
- **D3 — Self-provisioning (DECIDED).** Close-out and reconcile **create `CHANGELOG.md` from seed if
  absent**; the dashboard treats *absent + authored commits* as a **defect**, not silent `present=False`.
  Closes escape #4.
- **D4 — Breadth of "action" → broadened beyond commits (DECIDED).** "Action" includes releases,
  tag/branch ops, PR opens, upstream issue closes, access grants, and wontfix/decline/grooming decisions.
  FM #27, the close-out step, and the reconcile pass must not key **solely** on commits. Closes escape #6.
- **D5 — Backfill depth → bounded v3.0-forward (DECIDED).** ~5 verifiable entries since v3.0 + a single
  pointer line for v1.0–v3.0. Lands in S6.
- **D6 — Seed-template recompose (DECIDED).** Recompose `starter-kit/CHANGELOG.md` from
  Keep-a-Changelog/[Unreleased] to the action-log shape **now**, keeping it a `seed` file and keeping the
  Signal-D sentinel consistent so a fresh seed isn't flagged "never used." Lands in S4.
- **D7 — Release double-write → accept the pointer (DECIDED).** A release touches §Versioning + README
  §What's New + a one-line CHANGELOG pointer; the pointer keeps the ledger hole-free. *(Flag only, out of
  scope: a later slimming of README §What's New to pointers remains possible.)*

---

## 7. Implementation plan (multi-session; strict "1 and done")

This is a **multi-session campaign**, not one session. Each row is one deliverable; close out between them.
Order puts the dependability keystone early and the ship-blocking reconciliation last-before-each-commit.

| # | Session deliverable | Notes / 🐉 dragons |
|---|---|---|
| S1 | **This plan** + operator decisions D1–D7 | ← you are here; planning deliverable only |
| S2 | Component A: FM #27 + degradation row + 3F/Phase-6 step (with §5 fixes 2–4 baked in) | 🐉 append-only FM; 🐉 run the Learning-#7 grep (§5.1) *in the same commit* |
| S3 | Component B: Phase 0 reconcile-on-read + 1B `pending` marker | 🐉 the keystone — verify it actually backfills a synthesized undocumented commit before claiming done |
| S4 | Component D: entry format + `SESSION_NOTES` division; recompose `starter-kit/CHANGELOG.md` (D6) | 🐉 keep it a `seed`; 🐉 Signal-D sentinel consistency |
| S5 | Component C: dashboard freshness (both twins) | 🐉 reproduce against a stale-CHANGELOG fixture; 🐉 wiring anchor (§5.5) |
| S6 | Component E: root `CHANGELOG.md` + bounded backfill (D5) + §Versioning boundary header | 🐉 absolute upstream-issue URLs; 🐉 pointer-not-restate for releases |
| S7 | D1 pre-commit hook + add the step to the other session-type checklists (escape #8) | 🐉 `--no-verify` bypass documented; 🐉 grep every checklist |

**Versioning:** a framework change of this size (new FM, new Phase 0 step, dashboard behavior) is a
**minor bump** candidate — but per prior guidance, *don't presume a release event*; decide at the end.
**Effort:** the design/verify already ran at high parallelism; the *implementation* sessions S2/S3 (gate
semantics + reconcile logic) warrant deep-reasoning mode — blast radius is every adopter's close-out.

---

## 8. What the adversarial pass bought

The naive plan — a close-out gate + a freshness check — **looked** sufficient and **was not**: it would
have shipped a ledger the operator was told to depend on while eight high-severity paths let actions
escape it. The dependability pass converted *"add a gate"* into *"gate-on-write **and** reconcile-on-read,
self-provisioning, keyed on commits-authored, with real enforcement where there's no runner."* That is the
difference between *"sessions are asked to log"* and *"the ledger is true when you read it."*
