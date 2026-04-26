# Plan the Integration of Protocols as a First-Class Methodology Layer

**Status:** Open — to be addressed in the next session as a **planning session**.
**Created:** 2026-04-25
**Type:** Planning/Preparation session per [`ITERATIVE_METHODOLOGY.md` §Session Types](../../ITERATIVE_METHODOLOGY.md#planningpreparation-sessions).

---

## Context

Session of 2026-04-25 produced two artifacts:

1. [`workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md`](../../workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md) — a multi-session campaign template for exhaustive primary-source verification, supporting both creation and audit modes.
2. [`docs/planning/protocols-as-first-class.md`](protocols-as-first-class.md) — an argumentative article proposing that the "protocol" layer (multi-session campaign template) be promoted to first-class status in the methodology, alongside workstreams.

The protocol artifact already exists in the file tree, but the concept of "protocol" is not named in `ITERATIVE_METHODOLOGY.md` or `SESSION_RUNNER.md`. This is the worst-of-both state: a structural addition exists implicitly without being documented in the methodology's load-bearing files.

The next session's job is to **plan** — not implement — the transformation that would resolve this asymmetry. The plan goes to the methodology lead (Terrell Deppe / KJ5HST) for approval; an implementation session executes only after approval.

---

## Deliverable for the next session

A Phase 3 design document covering:

1. **Exact text** for a new section in `ITERATIVE_METHODOLOGY.md` that defines protocols as a layer parallel to (but distinct from) Session Types and Workstreams. Should be ~200-300 words. Must address: when a protocol is appropriate, when it isn't, the relationship to workstreams, the relationship to planning sessions.
2. **Exact text** for a new orientation step in `SESSION_RUNNER.md` Phase 0/1: *"Check whether this work has a documented protocol. If yes, follow its session sequence; if no, evaluate whether it should."* Locate the precise insertion point in `SESSION_RUNNER.md` and verify it does not disrupt other orientation steps.
3. **Skeleton** for `workstreams/TEMPLATE_PROTOCOL.md`, structured parallel to the existing `TEMPLATE_WORKSTREAM.md`. Should include placeholder sections for: when to use, campaign structure, per-session-type steps, deliverable contracts, exit criteria, anti-patterns, verification checklist, example campaign outline.
4. **Update plan** for `CLAUDE.md` (this repo's) — the Protocols subsection already exists; verify it's consistent with the new methodology vocabulary and tighten if needed.
5. **Update plan** for `README.md` — one bullet under "What's New" and one row in the document hierarchy table. Determine version number (v2.4 minor or v2.3.1 point — the addition is structural but small).
6. **Update plan** for `HOW_TO_USE.md` — assess whether protocols warrant a section or example.
7. **Migration plan** for the existing `workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md` — since it was authored before the protocol vocabulary was named, verify its terminology is consistent with the new methodology section, or list edits needed.
8. **Risk assessment** — what could go wrong with this transformation, and how does the plan mitigate?

The plan must be detailed enough that a follow-on implementation session can execute it mechanically without re-deriving any decisions. ([Iterative Methodology §Planning Sessions](../../ITERATIVE_METHODOLOGY.md#planningpreparation-sessions): "The value is front-loaded: a good plan collapses multi-session implementation work into a single session.")

---

## Pre-flight reading required

Before the planning session begins:

- [`docs/planning/protocols-as-first-class.md`](protocols-as-first-class.md) — the proposal article (read in full)
- [`workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md`](../../workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md) — the existing protocol document (read in full)
- [`ITERATIVE_METHODOLOGY.md`](../../ITERATIVE_METHODOLOGY.md) §§ Session Types, Adapting to Your Domain — to identify the exact insertion point for the new protocol section
- [`starter-kit/SESSION_RUNNER.md`](../../starter-kit/SESSION_RUNNER.md) — to identify the exact insertion point for the new orientation step
- [`workstreams/TEMPLATE_WORKSTREAM.md`](../../workstreams/TEMPLATE_WORKSTREAM.md) — as the structural model for `TEMPLATE_PROTOCOL.md`
- Lead developer's response to the proposal article (if available before the planning session runs) — direction may shape the plan

---

## Acceptance criteria

The planning session is complete when the design document above is committed to `docs/planning/protocols-integration-design.md` (or similar) and presented to the stakeholder for approval per the methodology's [Phase 4 Present gate](../../ITERATIVE_METHODOLOGY.md#phase-4-present).

The planning session is **not** complete when:

- The plan exists but contains "TBD" sections (defeats the purpose of front-loading the design)
- The plan recommends multiple alternatives without choosing one (the planning session is for deciding, not for surfacing options)
- The plan has not been reviewed against the methodology's principles and gate requirements

A successful planning session collapses what would otherwise be 2-3 implementation sessions into 1, by surfacing all decisions, exact text, and edit locations in advance.

---

## Out of scope for the next session

- Actually editing `ITERATIVE_METHODOLOGY.md`, `SESSION_RUNNER.md`, or any other methodology file. (That is the implementation session that follows.)
- Writing additional protocol documents beyond the existing one. (That happens after the layer is named.)
- Bumping the methodology version number. (The implementation session decides version after edits are concrete.)
- Re-litigating whether protocols should exist as a layer. (The proposal article is the input; the planning session presumes the lead has approved direction. If direction is not approved, this entry retracts and no planning session runs.)

---

## Dependency

This planning session depends on the methodology lead's response to [`docs/planning/protocols-as-first-class.md`](protocols-as-first-class.md). If the lead rejects the proposal, this entry should be closed with a note; the existing `RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md` would then need to be either retracted or reframed to fit within the existing workstream concept.
