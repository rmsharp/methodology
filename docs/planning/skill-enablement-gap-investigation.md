# Pocock Skill Enablement — Investigation, Damage Assessment, and Multi-Session Plan

**Date:** 2026-05-27.
**Session-type:** Planning. Session 1 of an expected multi-session investigation. No implementation.
**Branch at time of writing:** `feature/skill-citation-completion` (working tree only — commit/branch strategy is part of the open decision).
**Triggered by:** Operator report 2026-05-27 — invoking `/improve-codebase-architecture` on a methodology-adopting repo failed because `CONTEXT.md` and `docs/adr/` did not exist; `BOOTSTRAP.md` had not instructed the adopter to create them.
**Operator constraint, 2026-05-27:** *"Damage to methodology must be assessed before any change is proposed. Both static documentation damage and runtime performance damage are in scope."*

---

## 1. Problem statement

Methodology v2.6 **recommends** seven Pocock skills via `starter-kit/RECOMMENDED_SKILLS.md`. Two of them (`/improve-codebase-architecture`, `/grill-with-docs`) read or modify files (`CONTEXT.md`, `docs/adr/`) that `BOOTSTRAP.md` neither references nor copies. A third (`/triage`) recommends a pre-flight skill that methodology has explicitly declined.

This investigation answers two questions, in this order:

1. **Should methodology change at all to enable Pocock skills?** Per operator constraint, this requires explicit damage assessment.
2. **If methodology should change, what is the smallest change with the largest benefit?**

The v2.6 principle *"methodology recommends; methodology does not reimplement"* is load-bearing for both.

---

## 2. Evidence the gap is real

### 2.1 What the skills expect

`/improve-codebase-architecture` (SHA `a36584e09eae`) YAML description, verbatim:

> *"Find deepening opportunities in a codebase, informed by the domain language in CONTEXT.md and the decisions in docs/adr/."*

The SKILL.md body references `CONTEXT.md`, `docs/adr/`, and `LANGUAGE.md` as adopter-side files.

`/grill-with-docs` (SHA `e7df78bb81da`) file-creation behavior, verbatim:

> *"Create files lazily — only when you have something to write. If no `CONTEXT.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed."*

The two skills **compose**: `/grill-with-docs` scaffolds the same files `/improve-codebase-architecture` reads.

### 2.2 What methodology provides (grep-verified)

| Asset | Status |
|---|---|
| `starter-kit/CONTEXT_TEMPLATE.md` | Exists (shipped v2.6) |
| `starter-kit/ADR_TEMPLATE.md` (any name) | Does **not** exist |
| `BOOTSTRAP.md` Step 2 copy list includes `CONTEXT_TEMPLATE.md` | No |
| `BOOTSTRAP.md` mentions `CONTEXT.md` or `docs/adr/` | Zero hits |
| `RECOMMENDED_SKILLS.md` row for `/improve-codebase-architecture` names a prerequisite | No |

An adopter who follows `BOOTSTRAP.md` Steps 1–9 verbatim ends up without `CONTEXT.md` or `docs/adr/`.

### 2.3 Adopter's reported experience

Operator, 2026-05-27: invoking `/improve-codebase-architecture` on a methodology-adopting repo flagged missing files the adopter had never been instructed to create.

---

## 3. Per-skill dependency catalog

| Skill | Files expected in adopter repo | Skill self-creates? | Methodology template ships? | `BOOTSTRAP.md` ensures? | Gap? |
|---|---|---|---|---|---|
| `/git-guardrails-claude-code` | `.claude/hooks/`, `.claude/settings.json` | Yes (skill installs them) | n/a | Step 10 recommends | No |
| `/grill-me` | None | n/a | n/a | n/a | No |
| `/grill-with-docs` | `CONTEXT.md`, `docs/adr/` (read) | Yes, lazy | `CONTEXT_TEMPLATE.md` ✓; no ADR | No copy step | **Documentation-only** |
| `/diagnose` | Runnable app, tests, git, debugger, domain glossary, ADRs | No | `CONTEXT_TEMPLATE.md` ✓ (glossary proxy); no ADR | No (glossary/ADRs) | **Soft (consults if present)** |
| `/triage` | Issue tracker labels, `.out-of-scope/`, `AGENT-BRIEF.md`, `OUT-OF-SCOPE.md` | Partial; conditional `/setup-matt-pocock-skills` prerequisite (verbatim: *"The mapping should have been provided to you — run `/setup-matt-pocock-skills` if not"*) | None | No | **Contradiction** |
| `/improve-codebase-architecture` | `CONTEXT.md`, `docs/adr/`, `LANGUAGE.md` | No | `CONTEXT_TEMPLATE.md` ✓; no ADR; no LANGUAGE | No | **Missing files** |
| `/setup-pre-commit` | `package.json`, lockfile | Creates `.husky/`, `.lintstagedrc` itself | n/a | Implicit | No |

Four categories of gap surface:

- **Hard missing-files gap** — `/improve-codebase-architecture` (reads `CONTEXT.md` / `docs/adr/` / `LANGUAGE.md`), `/grill-with-docs` (lazy-creates `CONTEXT.md` / `docs/adr/`).
- **Soft missing-files gap** — `/diagnose` consults a domain glossary and ADRs when present; degrades gracefully without them. Same template-shape as the hard gap above, lower-stakes.
- **Contradiction** — `/triage` recommends `/setup-matt-pocock-skills`, which methodology's "Skills not recommended" subsection declines.
- **No gap** — 3 of 7 skills (`/git-guardrails-claude-code`, `/grill-me`, `/setup-pre-commit`).

---

## 4. Damage assessment framework

Damage to methodology has **two axes**, evaluated separately. A change that passes one axis can fail the other; both must be measured.

### 4.1 The two axes

| Axis | What it measures | Who feels it |
|---|---|---|
| **Static** | Damage to the methodology documents at rest | Every adopter — most painfully, those who never use a Pocock skill (they read docs they don't need) |
| **Runtime** | Damage to methodology's functional value during a session | Adopters who use a Pocock skill (their session may compress methodology phases, skip gates, or erode handoff discipline) |

### 4.2 Static damage signals (S1–S10)

| # | Signal | How to measure | Pass = |
|---|---|---|---|
| S1 | Synced-file edits | Does the change touch `SESSION_RUNNER.md`, `SAFEGUARDS.md`, `methodology_dashboard.py`? (`bin/status` detects drift.) | No edits |
| S2 | Numbered-set growth | FM count (25), principle count (9), phase count (6), gate count (12) — silent growth? | No silent growth |
| S3 | Cross-reference density | Lines added vs. new `[label](path)` links. Healthy is ~50:1 or sparser. | Ratio not worsened |
| S4 | Agent-independence violations | Grep for Claude-Code-specific terms in framework files (`ITERATIVE_METHODOLOGY.md`, workstreams, `SESSION_RUNNER.md`, `SAFEGUARDS.md`). README line 232 ("agent-independent") must remain literally true. | Zero new violations in framework files |
| S5 | Principle preservation | After the change, can a reader still cite *"methodology recommends; does not reimplement"* without contradiction? Concrete test: does the change ship a template that duplicates an external file? | Yes |
| S6 | Bootstrap-time inflation | `BOOTSTRAP.md` Steps 1–10 word count (currently ~2400 → advertised "10 min"). Change pushes >10%? | No / explicit budget |
| S7 | Non-using-adopter friction | Does an adopter who never invokes a Pocock skill see new required reading at bootstrap or session start? | No |
| S8 | Reimplementation drift risk | Does the change pin to a Pocock SHA whose upstream bump would force methodology to bump too? | No SHA-coupling beyond the existing index |
| S9 | Self-contradiction grep | Grep for any new rule against existing rules. | No contradictions |
| S10 | Audit framing compatibility | Can the audit doc's drop/keep/refactor framing still apply to a re-audit of this work? | Yes |

### 4.3 Runtime damage signals (R1–R10)

Runtime damage occurs when a skill's invocation compresses multiple methodology phases without gate checks. Signals are scored on the worst plausible session, not the best-case one.

| # | Signal | Pass = |
|---|---|---|
| R1 | Phase 0 Orient preserved before the skill is invoked | Yes |
| R2 | Phase 1B Claim stub written before any skill artifact appears | Yes |
| R3 | Phase 4 Present gate fires before skill-driven file modifications | Yes |
| R4 | "1 and done" rule held after the skill completes | Yes |
| R5 | Phase 3D handoff written regardless of skill output | Yes |
| R6 | Build equivalent run after any skill-driven file modifications | Yes |
| R7 | Safety commit happens before skill-driven implementation | Yes |
| R8 | Phase 6 self-assessment + previous-handoff scoring performed | Yes |
| R9 | Workstream named in Phase 1 before the skill is invoked | Yes |
| R10 | *"A skill is not a phase"* applied when the skill tries to pull across a gate | Yes |

### 4.4 Per-skill phase-compression risk

| Skill | Phases the skill can span in one invocation | Compression risk |
|---|---|---|
| `/git-guardrails-claude-code` | Setup only (not in-session) | Zero |
| `/grill-me` | Phase 2.5 only | Low |
| `/grill-with-docs` | Phase 2 Research → Phase 3 Create → Phase 5 Implement (modifies `CONTEXT.md` / ADRs) | **High** |
| `/diagnose` | All 6 phases (debugging session — intentional alignment) | Medium (by design) |
| `/triage` | Phase 1 + DEVELOPMENT_WORKSTREAM Issue Lifecycle | Low |
| `/improve-codebase-architecture` | Phase 2 Research → Phase 3 Create (HTML report) → Phase 5 Implement (modifies `CONTEXT.md` / ADRs) | **High** |
| `/setup-pre-commit` | Setup only | Zero |

The two skills the operator is currently considering enabling are the two highest-runtime-damage skills. This is the load-bearing observation for the strategy decision.

### 4.5 Existing runtime safeguard

`ITERATIVE_METHODOLOGY.md` §Recommended Skills (this branch, commit `f1d1fbf`):

> *"A skill is not a phase. A recommended skill that pulls a session across a hard gate ... is failure mode #2 (keep-going) wearing a tool costume. Close out first."*

The safeguard is **textual**, not mechanical. Its effectiveness depends on the adopter's discipline; methodology has no `PreToolUse` hook intercepting skill invocations mid-flow.

---

## 5. Strategy space

The decision has **two orthogonal axes**, set independently.

### 5.1 Enablement axis

How does an adopter discover and satisfy file prerequisites?

| Strategy | Mechanism | Where the change lands |
|---|---|---|
| Never | Methodology does not change. Adopter handles their own setup (same posture as `/setup-pre-commit`). | Nothing |
| Reactive | Methodology unchanged in general. Adopters who ask receive a snippet for their CLAUDE.md "Project-Specific Methodology Adaptations" section. | Per-adopter CLAUDE.md, not methodology |
| Reactive (templated) | One commented-out paragraph in `starter-kit/CLAUDE_TEMPLATE.md` that adopters uncomment if they choose Pocock skills. | `CLAUDE_TEMPLATE.md` only |
| Preemptive A | `BOOTSTRAP.md` names `/grill-with-docs` as the seeding tool. `RECOMMENDED_SKILLS.md` adds a "Prerequisites" column. | `BOOTSTRAP.md` + `RECOMMENDED_SKILLS.md` |
| Preemptive B | Methodology ships `ADR_TEMPLATE.md` (and maybe `LANGUAGE_TEMPLATE.md`); `BOOTSTRAP.md` Step 2 copies them. | New template files + `BOOTSTRAP.md` |
| Preemptive C | Hybrid of A and B. | Both |
| Preemptive D | New `starter-kit/SKILL_ENABLEMENT.md` per-skill catalog. | New file |

### 5.2 Bounding axis

How does methodology protect its phases from skill phase-compression?

| Strategy | Mechanism | Where the change lands |
|---|---|---|
| None | No change. Existing *"A skill is not a phase"* is the only safeguard. | Nothing |
| Per-skill phase map | `RECOMMENDED_SKILLS.md` adds a "Phases spanned" column for each external skill. | `RECOMMENDED_SKILLS.md` |
| Per-skill break-point guidance | For high-compression skills (`/improve-codebase-architecture`, `/grill-with-docs`), document where to stop and apply methodology's gates. | `RECOMMENDED_SKILLS.md` and/or the cited workstream |
| Strengthened *"A skill is not a phase"* | Add per-high-risk-skill examples to the existing principle. | `ITERATIVE_METHODOLOGY.md` |

### 5.3 Enablement axis scored against static damage

| Strategy | Signals failed | Net |
|---|---|---|
| Never | None | Passes (no change) |
| Reactive (CLAUDE.md only) | None | Passes by construction |
| Reactive (templated) | None (S5 borderline; S4 footprint in a *template*, not a framework file) | Passes with small caveat |
| Preemptive A | S3, S6 measurable; S4 mild; S7 minor | Passes with measurable, contained cost |
| Preemptive B | S4, S5, S8 | **Fails** on principle preservation |
| Preemptive C | Inherits B's failures at smaller surface | **Fails** |
| Preemptive D | S6 (new file), S10 risk (rot) | Passes with high one-time cost |

### 5.4 Bounding axis scored against both damage axes

| Strategy | Static damage signals failed | Runtime damage reduction |
|---|---|---|
| None | None | None — adopter discipline only |
| Per-skill phase map | None (small column addition) | Awareness of which skills are high-compression |
| Per-skill break-point guidance | None (one paragraph per high-risk skill) | Reduces R3, R4, R5, R7 failures for high-risk skills |
| Strengthened *"A skill is not a phase"* | None (extends existing principle with concrete examples) | Marginal additional discipline |

All bounding options pass the static checklist because they are documentation additions, not structural changes to gates or phases.

---

## 6. Plausible pairings

The two axes are independent, so 28 combinations exist. Five are plausible; the rest either fail principle preservation (Preemptive B/C) or pair high cost with low marginal value (Preemptive D).

| Pair | When this is the right choice | Static cost | Runtime protection |
|---|---|---|---|
| **Never + None** | Operator believes Pocock skill compatibility is outside methodology's commitment surface. The existing *"A skill is not a phase"* is the only control. | Zero | Principle-only |
| **Never + Per-skill phase map** | Methodology stays out of bootstrap but publishes structural runtime information. Adopters who install skills independently still benefit. | Trivial (one column) | Awareness-based |
| **Reactive + Per-skill phase map** | Same as above plus per-request bootstrap support via CLAUDE.md adaptations when an adopter asks. | Trivial | Awareness-based |
| **Reactive (templated) + Per-skill break-point guidance** | Methodology hints at bootstrap and provides explicit runtime safeguards for the two high-risk skills. | Small | Explicit |
| **Preemptive A + Strengthened *"A skill is not a phase"*** | Methodology commits to enablement and reinforces the runtime principle. | Medium | Explicit |

The assessment narrows the realistic field to these five. The choice among them is a question of operator posture toward methodology evolution.

---

## 7. The `/triage` contradiction

`/triage` is a different gap. Methodology's `RECOMMENDED_SKILLS.md` recommends `/triage`; `/triage`'s SKILL.md recommends running `/setup-matt-pocock-skills` first; methodology's "Skills not recommended" subsection explicitly declines `/setup-matt-pocock-skills`. Transitive contradiction.

| Resolution | Effect | Cost |
|---|---|---|
| Drop | Remove `/triage` from `RECOMMENDED_SKILLS.md`; move to "Skills not recommended" | Low; loses a v2.6 audit decision |
| Document | Add a label-init paragraph to DEVELOPMENT_WORKSTREAM Issue Lifecycle, replacing what `/setup-matt-pocock-skills` would do | Medium; tracks a Pocock convention by hand |
| Footnote | Keep `/triage` cited; add a note in its `RECOMMENDED_SKILLS.md` row acknowledging the prereq contradiction | Low; less elegant |

This decision is independent of §6 and can be deferred under any pairing.

---

## 8. Multi-session roadmap

| Session | Deliverable | Stops when |
|---|---|---|
| S1 (this session) | This planning doc. | Operator has read it. |
| S2 | Operator selects an enablement + bounding pairing from §6 (or declines all). Decision recorded as a one-paragraph addendum to this doc, or as an upstream issue. No implementation. | Decision recorded somewhere durable. |
| S3 | (Conditional) Implement the selected pairing. Single PR. | Change merges, or operator rejects. |
| S4 | (Conditional, separate from S3) Address the `/triage` contradiction per §7. | Decision recorded. |
| S5+ | Deferred unless new evidence emerges. | n/a |

S2's deliverable is a decision, not implementation — separate session per methodology's "1 and done" rule.

---

## 9. Open questions for the operator

1. **Enablement axis choice** (§5.1). Among the five plausible pairings, four use Never / Reactive / Reactive (templated) on this axis; one uses Preemptive A.
2. **Bounding axis choice** (§5.2). Per-skill phase map appears in three of the five plausible pairings.
3. **`/triage` resolution** (§7). Drop / Document / Footnote.
4. **Commit strategy for this planning doc.** Even under Never + None (no methodology change), this doc records the investigation that justified the decision. Commit as institutional memory or leave untracked?
5. **Branch & PR strategy for any S3 implementation.** PR #18 is currently open on this branch. New branch + new PR for S3, or bundle?
6. **Issue or PR first?** Issues #15/#16/#17/#19 were filed first to invite operator response. The two-axis damage assessment framework here may merit a similar upstream issue independent of any implementation.
7. **Agent independence.** Pocock skills are Claude-Code-specific. Issue #16 already targets `CONTEXT_TEMPLATE.md`. Should the enablement story explicitly call out that Cursor / Cody / other adopters do not benefit?

---

## 10. Related open issues (not subsumed by this work)

| Issue | Why it's related | Why this work doesn't subsume it |
|---|---|---|
| #15 — Phase 2.5 vs Phase 2B naming | Same v2.6 release | Pure naming |
| #16 — `CONTEXT_TEMPLATE.md` auto-memory generalization | Same file | Content fix; this doc is about bootstrap of that file |
| #17 — Workstream citation pattern inconsistent | Same convention | Style of citation; this doc is about consumability of cited skills |
| #19 — Cross-reference completeness as Learning | Same review hygiene class | Process discipline; this doc is adopter ergonomics + damage posture |

None of these issues tracks the enablement gap or the meta-question of whether methodology should respond to it.

---

## 11. Provenance — what was read

- `starter-kit/BOOTSTRAP.md` — read in full; zero references to `CONTEXT.md` or `docs/adr/` (grep-verified).
- `starter-kit/CONTEXT_TEMPLATE.md` — read in full; references `docs/adr/` and `/grill-with-docs`.
- `starter-kit/RECOMMENDED_SKILLS.md` — read in full; per-skill rows for 7 Pocock skills + 6 Claude Code skills + "Skills not recommended" subsection.
- `workstreams/ARCHITECTURE_WORKSTREAM.md` — read in full; cites `/improve-codebase-architecture` without prerequisite guidance.
- `workstreams/DEVELOPMENT_WORKSTREAM.md` — read in full; cites `/triage` without prerequisite guidance.
- `ITERATIVE_METHODOLOGY.md` §Recommended Skills — read in full; includes *"A skill is not a phase"* principle.
- `docs/audits/2026-05-02-mattpocock-skills-evaluation.md` — read in full; F1–F10 history.
- Pocock SKILL.md files at their pinned SHAs from `RECOMMENDED_SKILLS.md` — all 7 verbatim-fetched:
  - `/git-guardrails-claude-code` at `62f43a18177b`
  - `/grill-me` at `62f43a18177b`
  - `/grill-with-docs` at `e7df78bb81da`
  - `/diagnose` at `7afa86d3a5dd` (the verbatim fetch surfaced the soft glossary/ADR dependency reflected in §3)
  - `/triage` at `179a14e72103` (the verbatim fetch confirmed §7's contradiction characterization — quoted in §3)
  - `/improve-codebase-architecture` at `a36584e09eae`
  - `/setup-pre-commit` at `62f43a18177b`
- Upstream issues #15, #16, #17, #19 — read in full.
- Upstream PR #18 — confirmed open with current branch's 3 commits.

---

## 12. Out of scope

- Implementation of any §6 pairing. This is a Planning Session.
- Audit of Pocock skills beyond the 7 currently cited.
- Skills-as-slash-commands packaging (the 2026-05-02 audit's Observation 1).
- Damage assessment of future hypothetical skill integrations beyond the 7 cited; the §4 framework can be reapplied per case.

---

*Author: Claude Opus 4.7 (1M context), session 2026-05-27.*
