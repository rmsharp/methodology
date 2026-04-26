# Design Plan: Promote Protocols to a First-Class Methodology Layer

**Status:** Phase 3 design — pending methodology-lead approval (the proposal article was approved offline; this is the implementable plan)
**Created:** 2026-04-25
**Type:** Planning-session deliverable per [`ITERATIVE_METHODOLOGY.md` §Session Types](../../ITERATIVE_METHODOLOGY.md#planningpreparation-sessions). The implementation session executes this plan mechanically; no decisions are deferred.
**Inputs:** [`docs/planning/protocols-as-first-class.md`](protocols-as-first-class.md) (the proposal), [`docs/planning/protocols-integration-session-plan.md`](protocols-integration-session-plan.md) (the brief).

---

## 1. Executive Summary

The methodology has a structural addition pending: a vocabulary layer for multi-session campaign templates, called **protocols**. One protocol already exists in the file tree (`workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md`), but the layer is not named in `ITERATIVE_METHODOLOGY.md` or `SESSION_RUNNER.md`. This plan specifies the exact edits needed to name the layer: a new ~350-word section in the master framework, a ~100-word orientation step in the cockpit checklist, a new blank template, and small updates to `CLAUDE.md`, `README.md`, and `HOW_TO_USE.md`. No principle, phase, gate, or workstream changes. The realized example needs zero migration edits — its terminology was authored consistently with the new methodology vocabulary.

Version: **v2.4** (minor). Effort: a single implementation session.

---

## 2. Decisions Made (with rationale)

### 2.1 Directory placement: `workstreams/*_PROTOCOL.md`

**Decision:** Protocols live in `workstreams/` alongside their parent workstreams, distinguished by the `_PROTOCOL.md` suffix. Not a separate `protocols/` directory.

**Rationale:** A protocol always extends a parent workstream — placing them together keeps the "campaign within a workstream" framing. The proposal article and the existing realized protocol both assume this layout. A separate directory would force a story for orphan protocols that never need to exist.

### 2.2 Terminology: keep "protocol," disambiguate explicitly

**Decision:** Coin "protocol" as a technical noun ("a protocol," "this protocol," "the Research Exhaustive Verification Protocol") for the new sense. Leave existing usage ("the protocol" generic, "Protocol Erosion" coined, "SESSION PROTOCOL — FOLLOW BEFORE DOING ANYTHING" header, "protocol violation" idiom) unchanged. Address the polysemy with an explicit terminology paragraph in the new methodology section.

**Rationale:** Renaming existing terms (Protocol Erosion → Methodology Erosion, SESSION PROTOCOL → SESSION RULES, Failure Mode #17 → Methodology erosion) would ripple through `ITERATIVE_METHODOLOGY.md`, `SESSION_RUNNER.md`, `CLAUDE_TEMPLATE.md`, `README.md`, `HOW_TO_USE.md`, and starter-kit files for nominal benefit. Native English handles "a protocol" (countable, named) vs. "the protocol" (uncountable, the rules) without intervention. The proposal author chose "protocol" deliberately; preserving that choice respects the proposal as an input.

**Inventory of existing usages** (from grep, 2026-04-25):
- Generic: "the protocol," "the whole protocol collapses," "Reset to full protocol," "follow the protocol," "compensates for documented tendencies" → `ITERATIVE_METHODOLOGY.md`, `SESSION_RUNNER.md`, `CLAUDE_TEMPLATE.md`, `README.md`
- Coined: "Protocol Erosion" (section + indicator), "Failure Mode #17 Protocol erosion" → `ITERATIVE_METHODOLOGY.md`, `SESSION_RUNNER.md`, `HOW_TO_USE.md`
- Compound headers: "SESSION PROTOCOL — FOLLOW BEFORE DOING ANYTHING," "Session Recovery Protocol" → `CLAUDE_TEMPLATE.md`, `README.md`, `SAFEGUARDS.md`
- Idiomatic: "protocol violation," "protocol step" → `SESSION_RUNNER.md`

All existing usages remain valid under the new vocabulary because the new sense is countable/named while the existing senses are uncountable/headers.

### 2.3 Version: v2.4 minor (not v2.3.1 patch)

**Decision:** Bump to v2.4.

**Rationale:** v2.3.1 implies a typo fix or small clarification within v2.3's scope. This change adds a vocabulary concept and a structural layer to the document hierarchy — the same kind of change that drove v1.2 (planning sessions promoted to a discipline), v2.0 (dashboard added), v2.1 (CHANGELOG/ROADMAP split), v2.2 (sync tooling), and v2.3 (research workstream). Each was a v2.X minor. Protocol promotion is consistent with that cadence.

### 2.4 SESSION_RUNNER insertion point: Phase 1 (not Phase 0)

**Decision:** The new orientation step lives in Phase 1 (Receive Task), after the task-to-workstream mapping table and the Plan Mode exit-trap warning, before the "If no workstream document exists" fallback.

**Rationale:** Phase 0 is about workspace state; Phase 1 is about task shape. Protocol awareness is a task-shape question — "is this work part of a multi-session campaign?" The Plan Mode trap is also a task-shape special case; the protocol check is structurally parallel and belongs adjacent to it.

### 2.5 No new failure mode

**Decision:** Do not add Failure Mode #24 ("Protocol blindness — running ad-hoc multi-session work without checking for an existing protocol").

**Rationale:** The methodology's own discipline (`ITERATIVE_METHODOLOGY.md` §Knowledge Accumulation System): *"Every entry in the anti-pattern list exists because a real session made that exact mistake. Do not add hypothetical anti-patterns. Only actual failures earn a number."* No real session has yet made this mistake — the protocol layer is being named for the first time. Defer adding the failure mode until the first real session attempts a campaign without checking for a protocol. Document the watch-for as a paragraph in the new methodology section instead.

### 2.6 No new quality gate

**Decision:** Do not add a 13th gate. The protocol layer uses existing per-session gates within its constituent sessions. The campaign-level gate (stakeholder approval of `CAMPAIGN.md`) is already covered by the Phase 4 Present gate of the planning session.

### 2.7 No worked example in HOW_TO_USE.md

**Decision:** Add a short Protocols subsection to Core Concepts, but defer a worked example to a follow-on session. The realized protocol (`RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md`) already serves as a worked example for readers who want detail.

---

## 3. Exact Text — for the implementation session to copy verbatim

### 3.1 ITERATIVE_METHODOLOGY.md — new section

**Insertion point:** Between current line 302 (the `---` separator that ends `## Session Types`) and current line 304 (`## The Session Runner`). Insert the section, then a `---` separator, so the result is:

```
[existing line 302] ---
[NEW SECTION]
---
[existing line 304] ## The Session Runner
```

**Exact text to insert:**

```markdown

## Protocols and Multi-Session Campaigns

Some deliverables cannot be produced in one session even when the work is decomposed correctly: paper-wide claim verification across hundreds of citations; security hardening across dozens of endpoints; familiarization with an inherited 40-module codebase. The 6 phases bound a single session and **Principle 9: Session Scope Bounding** bounds what one session may produce. Cross-session coordination toward a single deliverable operates at a different scale.

A **protocol** is a multi-session campaign template. It prescribes a session sequence, a deliverable contract at each session boundary, and exit criteria for the campaign as a whole. Each session within a protocol still runs the 6 phases; the protocol coordinates *across* sessions toward a deliverable that no single session could produce.

A protocol is **not** a workstream. Workstreams adapt the 6 phases to a domain (what does Phase 2 research look like for UI design vs. for research papers vs. for system audits). Protocols sequence sessions toward one specific deliverable type within a workstream. One workstream may host many protocols.

A protocol is **not** a planning-session output. A planning session produces a bespoke plan for one campaign; a protocol is reusable across every campaign of its type. The planning session for an individual campaign uses the protocol as its template, not its alternative.

### When to write or invoke a protocol

Use a protocol when **all three** apply:

1. The deliverable cannot be produced in one session even under correct decomposition.
2. The campaign shape is, or will be, repeatable.
3. Cross-session coordination — shared schemas, checkpoint deliverables, calibration rules — is load-bearing for quality.

Do **not** use a protocol when: the work fits in one session; the campaign is genuinely one-off (no expectation of repetition); or the right artifact is a domain adaptation, in which case the answer is a new workstream.

If a campaign has the multi-session shape but no protocol exists yet, the first campaign produces both a planning-session plan AND a draft protocol; the second campaign tightens the protocol from experience. This is the same compounding mechanism the methodology applies at the session and workstream layers, applied at the campaign layer.

### Where protocols live

Protocols live in `workstreams/` alongside their parent workstream, under the naming convention `*_PROTOCOL.md`. A blank starting point is `workstreams/TEMPLATE_PROTOCOL.md`. A protocol always extends a parent workstream — its `Relationship to Other Documents` table names that parent — and references the master framework for principles, phases, and gates.

The first realized example is [`workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md`](workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md): a campaign template that decomposes exhaustive primary-source verification into a planning → execution → consolidation sequence, supporting both creation (writing) and audit (reviewing) modes.

### Terminology

This document uses "protocol" in two senses. The longstanding generic sense — *"the protocol"* or *"session protocol"* referring to the methodology itself; **Protocol Erosion** naming the discipline-decay failure mode; *"protocol violation"* as an idiom — is unchanged. The new technical sense — *"a protocol"* or *"this protocol"* or *"the [Name] Protocol"* — refers to a multi-session campaign template as defined in this section. Readers disambiguate from context: the indefinite article and a named referent indicate the new sense; *"the protocol"* in the abstract refers to the methodology.

```

(End of new section. The implementation session writes a `---` separator after this section before the existing `## The Session Runner` heading.)

**Word count:** ~410 words (over the 200-300 brief; the terminology paragraph is the overrun and is necessary because the polysemy is real). Acceptable.

**No other edits to ITERATIVE_METHODOLOGY.md.** The §Adapting to Your Domain list (line 775+) lists workstreams; protocols are not domain adaptations and do not belong there. The Quality Gates summary (line 326+) does not get a new row — protocols use existing gates.

---

### 3.2 starter-kit/SESSION_RUNNER.md — new orientation step

**Insertion point:** Phase 1 (Receive Task), between current line 57 (the `**⚠ Plan Mode exit trap.**` paragraph) and current line 59 (`**If no workstream document exists for the task type...`). Insert as a new paragraph parallel in style to the Plan Mode trap.

**Exact text to insert:**

```markdown

**⚠ Multi-session campaign check.** If your work cannot be produced cleanly in one session even after correct decomposition — paper-wide verification, repository-wide hardening, multi-module familiarization — look for a matching `*_PROTOCOL.md` in `workstreams/`. If one exists, your session is one unit within its campaign: read the protocol and follow its planning → execution → consolidation sequence. If none exists but the work has that shape, raise it before starting work — a planning session may be needed to either adopt an existing protocol or draft one. See [`ITERATIVE_METHODOLOGY.md` §Protocols and Multi-Session Campaigns](../docs/methodology/ITERATIVE_METHODOLOGY.md#protocols-and-multi-session-campaigns).

```

**Note on the relative link path:** The starter-kit `SESSION_RUNNER.md` is copied into adopting projects to their root, where the master framework lives at `docs/methodology/ITERATIVE_METHODOLOGY.md` (per the README's setup instructions). The relative link reflects the post-copy layout; in this repo's own copy at `starter-kit/SESSION_RUNNER.md` the path resolves to a file that doesn't exist locally — that's acceptable because this is a template, not an executable runner. The same convention is used elsewhere in this file (e.g., `SESSION_NOTES.md`, `SAFEGUARDS.md` references). No change needed.

**No other edits to SESSION_RUNNER.md.** The mapping table (line 46-56) does NOT get a new row — protocols are orthogonal to workstream selection, not a parallel category. The Known Failure Modes table does NOT get a new entry (per Decision 2.5). The Degradation Detection table does NOT get a new row.

---

### 3.3 workstreams/TEMPLATE_PROTOCOL.md — new file

**Action:** Create the file. Full content below.

```markdown
# [Domain/Scope] [Campaign Name] Protocol

A multi-session campaign template for [describe the campaign-scale deliverable]. This protocol extends [`PARENT_WORKSTREAM.md`](PARENT_WORKSTREAM.md) — its [parent-workstream phase or primitive] is the per-session primitive this protocol scales into a [paper-wide / repository-wide / system-wide] discipline.

[Optional: any modes the protocol supports — e.g., creation/audit/maintenance — and a one-line description of each. Delete this paragraph if the protocol has only one mode.]

This is a **protocol**, not a workstream. It does not replace [parent workstream]; it prescribes a campaign structure for a specific deliverable: [name the campaign deliverable].

---

## Relationship to Other Documents

| Document | Role |
|----------|------|
| [`ITERATIVE_METHODOLOGY.md`](../ITERATIVE_METHODOLOGY.md) | Master framework — 9 principles, 6 phases, 12 quality gates. This protocol obeys all of them. See §Protocols and Multi-Session Campaigns. |
| [`PARENT_WORKSTREAM.md`](PARENT_WORKSTREAM.md) | Parent workstream. Defines the per-session primitives this protocol scales. |
| [`../starter-kit/SESSION_RUNNER.md`](../starter-kit/SESSION_RUNNER.md) | Operational checklist — every session in the campaign runs against it. |

[Add additional rows for sibling workstreams the protocol borrows session patterns from — e.g., `AUDIT_WORKSTREAM.md` for review-mode sessions.]

---

## When to Use

[State trigger conditions. Be specific — this is the "should I use this protocol?" gate. If multiple modes exist (creation/audit), provide trigger conditions per mode.]

### Triggers

[State the umbrella condition that makes this protocol applicable, AND any of:]
- [Specific trigger 1]
- [Specific trigger 2]
- [Specific trigger 3]

### When NOT to use

- [Case where the cost outweighs the value]
- [Case where a simpler tool fits — single session, sample-based audit, etc.]
- [Case where the deliverable is out of scope for this protocol]

---

## Why This Is a Campaign, Not a Mode

A single session attempting this campaign's full scope will fail in one of three ways:

1. **Context exhaustion.** [How holding the corpus, inputs, and per-unit ledger degrades reasoning quality long before raw token limits hit.]
2. **"1 and done" violation.** [Why this deliverable is hundreds of micro-deliverables fused into one artifact, and the second half receives less rigor than the first.]
3. **No resumability.** [Why a crashed mid-session leaves the next session unable to recover without checkpoint files.]

This protocol decomposes the work into a planning session, N execution sessions, and a consolidation session — each obeying the methodology's session-scope rules and producing a checkpoint deliverable.

---

## Campaign Structure

```
Session 1: Campaign Planning
    └─ Produces: CAMPAIGN.md ([what's in it])

Sessions 2..N+1: Per-Unit Execution (one per scoped unit)
                   └─ Produces: units/<unit>.md ([what's in it])

Session N+2: Consolidation
                   └─ Produces: REPORT.md ([what's in it])
```

[Describe typical campaign size. Where do per-unit splits happen? What governs N? Provide concrete numbers if possible.]

All campaign artifacts live under `[campaign-directory]/`:

```
[campaign-directory]/
├── CAMPAIGN.md                    # Planning session output
├── units/
│   ├── unit-1.md                  # Per-unit deliverables
│   └── ...
└── REPORT.md                       # Consolidation session output
```

---

## Session 1: Campaign Planning

A planning session per [`ITERATIVE_METHODOLOGY.md` §Session Types](../ITERATIVE_METHODOLOGY.md#planningpreparation-sessions). Heavy Phase 2; produces a Phase 3 design that subsequent sessions execute mechanically.

### Steps

1. [Step] — [what to produce / verify]
2. [Step] — [what to produce / verify]
3. **Choose the scoping unit.** Default: [default split]. Split smaller when [criterion]. Never split below [floor].
4. **Define the deliverable contract** (see Deliverable Contracts below). Lock the schema before execution begins; schema drift across units forces consolidation rework.
5. **Allocate sub-agent strategy.** [Decisions per unit: parent-only, parent-with-read-only-sub-agents, parallel sub-agents. See Sub-Agent Dispatch Pattern below.]
6. **Set exit criteria.** Per-unit completion thresholds and campaign-level halt conditions.
7. **Write `CAMPAIGN.md`** as the session's Phase 3 deliverable. Stakeholder approves before any execution session begins.

### Gate (Phase 4 in this session)

Stakeholder approval of `CAMPAIGN.md` is the second-highest-leverage gate in the protocol (after the per-execution-session implement gate). A bad plan multiplies cost across N sessions.

---

## Sessions 2..N+1: Per-Unit Execution

[Describe the per-session shape. Specify session type per `ITERATIVE_METHODOLOGY.md` §Session Types — implementation (all 6 phases) or review/audit (Phases 1-4 + 6, skip 5).]

### Common steps

1. **Pre-Flight.** Read `CAMPAIGN.md`. Read prior unit deliverables. Verify [domain-specific state] matches planning-session inventory.
2. **Phase 1.5 (Claim the Session).** Stub names the unit in progress. A ghost session here is detectable because the stub names exactly which unit was being worked on.
3. **Research.** [What to extract for this unit, with no exceptions.]
4. **[Mode-specific work]** (see below).
5. **Present.** Surface the unit deliverable to the stakeholder. Highlight: [protocol-specific items — e.g., blocked rows, calibration adjustments, patterns visible at unit scope].
6. **Phase 6 close-out.** Standard. Handoff records: [protocol-specific items].

### Mode-specific steps

[If the protocol supports multiple modes, describe each separately under sub-headings.]

### Critical disciplines

- **Evidence is non-negotiable.** [Define what "evidence" means in this protocol's deliverables — a quoted passage, a verified measurement, a reproducible test result.]
- **Append-only within a session.** Rows are not deleted. A row whose status changes during the session gets a `superseded` mark and a new row.
- [Other domain-specific disciplines.]

---

## Session N+2: Consolidation

A review/audit session whose deliverable is the campaign-wide report.

### Steps

1. **Pre-Flight.** Read `CAMPAIGN.md` and every unit deliverable. Verify completeness — no unit has unresolved [protocol-specific status] rows. If any do, this session halts and flags them as a follow-on execution session.
2. **Research.** Aggregate across units. Identify cross-unit patterns: [examples].
3. **Create the report.** [Use the structure below.] The consolidation session does **not** re-do per-unit work — its job is merging, pattern-finding, and remediation/integration planning.
4. **Present.** Stakeholder approves the report. Open items become input to follow-on sessions.
5. **Phase 6 close-out.** Standard.

### `REPORT.md` structure

```markdown
## Coverage
[What was covered, with statistics.]

## [Mode-specific findings/results structure]

## Cross-Unit Patterns
[What was visible at the campaign scale that wasn't visible per unit.]

## Open Items / Remediation Plan
[Prioritized punch list for follow-on sessions.]
```

---

## Sub-Agent Dispatch Pattern

[If applicable. Many protocols benefit from sub-agent fan-out at per-unit scale. Describe the pattern, when to fan out, and calibration rules. See `RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md` for a worked example.]

---

## Deliverable Contracts

### Per-unit schema

```markdown
| # | [Field 1] | [Field 2] | [Field 3] | [Status/Verdict] | [Evidence] |
|---|-----------|-----------|-----------|------------------|------------|
```

**[Status / Verdict] vocabulary:**

| Value | Meaning |
|-------|---------|
| [value] | [meaning] |

The vocabulary is **locked at planning time**. Schema drift across units forces consolidation rework.

---

## Calibration and Exit Criteria

### Baseline expectations

[If the protocol has empirical baselines from prior runs, document them with bands and recommended actions.]

| Observed [metric] | Interpretation | Action |
|--|--|--|
| [band] | [interpretation] | [action] |

### Stop conditions

The campaign **halts** (not pauses — halts) when:
- [Stop condition 1]
- [Stop condition 2]
- A systemic finding emerges that invalidates the campaign premise.
- Stakeholder direction changes.

A halted campaign produces a partial `REPORT.md` covering completed units. Do not synthesize coverage you did not produce.

---

## Resumability

Each unit deliverable is a checkpoint. After every execution session, commit the unit file before close-out:

```
[campaign-directory]/units/<unit>.md
```

A crashed mid-unit session is recovered by the next session reading the unit file from the last committed state and resuming from the first row marked [pending-status]. The Phase 1.5 stub records which unit is in progress, so a ghost session is detectable.

**Unit deliverables are append-only within a session.** Never delete a row; mark it `superseded` and add a new row. The history of changed statuses is itself a signal — for calibration, scope drift, and the consolidation session's pattern detection.

---

## Anti-Patterns

[Numbered list. Same discipline as workstream anti-patterns: every entry exists because a real session made that exact mistake. Do not add hypothetical entries until evidence accumulates.]

1. **One-session attempt.** Trying to run the entire campaign in a single session. Context degrades; the second half is less reliable than the first. Use the campaign decomposition.
2. **Skipping the planning session.** Jumping to per-unit execution without a `CAMPAIGN.md`. Schema drift across units forces consolidation rework that exceeds the planning-session cost.
3. **Evidence-free rows.** Marking a row complete without the required evidence. The unit deliverable becomes an assertion list, not a [verified / drafted / audited] record.
4. **Cross-unit consolidation creep.** Doing per-unit work in the consolidation session because "I notice a problem in this unit while merging." Stop, log it as a follow-on, return to merging.
5. **Sub-agent calibration drift.** Dispatching sub-agents without explicit vocabulary calibration. Different sub-agents will produce different rates of [protocol-specific verdicts] for identical evidence.
6. [Domain-specific anti-pattern from real sessions in this protocol.]

---

## Verification Checklist

### Per execution session, before close-out

- [ ] Every [unit-scope claim/item] has a row in the [map/grid]
- [ ] Every row has a [status/verdict] drawn from the locked vocabulary
- [ ] Every row has the required evidence
- [ ] No row is in a transient/pending state
- [ ] Unit deliverable is committed
- [ ] Handoff records sub-agent strategy and calibration adjustments

### Per campaign, before close-out (consolidation session)

- [ ] Every unit listed in `CAMPAIGN.md` has a corresponding deliverable
- [ ] No unit deliverable contains pending or open rows
- [ ] Statistics tables sum correctly to total counts
- [ ] Every finding cites at least one unit deliverable row as evidence
- [ ] Cross-unit patterns are surfaced explicitly, not buried in per-finding remediation
- [ ] Remediation plan is ordered by priority and dependency, not by unit order
- [ ] Estimate-to-actual ratio is recorded for future-campaign calibration

---

## Example Campaign Outline

```
Campaign: [Name]
Mode: [creation/audit/etc.]
Trigger: [What kicked off this campaign]

Session 1 (Planning):
    Inventory: [what was inventoried]
    Estimate: [N units, M items per unit]
    Decomposition: [per-unit split]
    Sub-agent strategy: [chosen pattern]
    CAMPAIGN.md committed.

Sessions 2..N+1 (Execution, one per unit):
    Session 2 (unit-1): [results, calibration, anomalies]
    ...

Session N+2 (Consolidation):
    Aggregate: [totals, ratios]
    Cross-unit patterns: [what emerged]
    Findings/Open items: [count, priorities]
    Recommendation: [follow-on session count]
    REPORT.md committed.

Total: [N] sessions over [duration].
```
```

(End of TEMPLATE_PROTOCOL.md content.)

---

### 3.4 CLAUDE.md — audit and small updates

**Audit of already-added Protocols subsection (current line 66-70):**

| Check | Status |
|-------|--------|
| Title says "campaign-scale procedures within a workstream" | ✓ matches new methodology section |
| "Multi-session campaign template" phrasing | ✓ matches |
| "Extends the Research Documentation workstream" | ✓ matches |
| Both modes (creation/audit) mentioned | ✓ matches |

**No edits needed to the Protocols subsection itself.**

**Edits needed elsewhere in CLAUDE.md:**

**Edit A — Document Hierarchy table (current lines 17-21):** split the "Mission procedures" row into two rows to surface protocols.

Current:
```markdown
| Layer | File | Role |
|-------|------|------|
| Cockpit checklist | `starter-kit/SESSION_RUNNER.md` | Step-by-step operating procedure for every session |
| Flight manual | `ITERATIVE_METHODOLOGY.md` | Theory: 9 principles, 6 phases, 12 quality gates |
| Mission procedures | `workstreams/*.md` | Domain-specific adaptations (design, architecture, development, audit) |
```

Replace with:
```markdown
| Layer | File | Role |
|-------|------|------|
| Cockpit checklist | `starter-kit/SESSION_RUNNER.md` | Step-by-step operating procedure for every session |
| Flight manual | `ITERATIVE_METHODOLOGY.md` | Theory: 9 principles, 6 phases, 12 quality gates |
| Mission procedures | `workstreams/*_WORKSTREAM.md` | Domain-specific adaptations (design, architecture, development, audit, research documentation) |
| Campaign templates | `workstreams/*_PROTOCOL.md` | Multi-session campaigns extending a workstream |
```

**Edit B — Versioning section (after current line 92):** add the v2.4 entry.

Append after the v2.3 line:
```markdown
- **v2.4:** Protocols promoted to first-class layer — new vocabulary and document home for multi-session campaign templates that extend a workstream. New section in `ITERATIVE_METHODOLOGY.md` (§Protocols and Multi-Session Campaigns); new orientation step in `SESSION_RUNNER.md` (Phase 1 multi-session campaign check); new `workstreams/TEMPLATE_PROTOCOL.md`. No principle, phase, gate, or workstream changes. Realized example: `workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md`.
```

**Edit C — Versioning section header line (current line 84):** update the version reference.

Current: `Changes are tracked via git commits and the README's "What's New" section. Current version: v2.3.`

Replace with: `Changes are tracked via git commits and the README's "What's New" section. Current version: v2.4.`

**Edit D — Protocols subsection table (current line 66-70):** add a row for `TEMPLATE_PROTOCOL.md`.

Current:
```markdown
### Protocols (campaign-scale procedures within a workstream)

| File | Purpose |
|------|---------|
| `workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md` | Multi-session campaign template for exhaustive primary-source verification. Extends the Research Documentation workstream when per-session Phase 6 audit cannot complete the work. Supports both creation mode (writing) and audit mode (reviewing). |
```

Replace with:
```markdown
### Protocols (campaign-scale procedures within a workstream)

| File | Purpose |
|------|---------|
| `workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md` | Multi-session campaign template for exhaustive primary-source verification. Extends the Research Documentation workstream when per-session Phase 6 audit cannot complete the work. Supports both creation mode (writing) and audit mode (reviewing). |
| `workstreams/TEMPLATE_PROTOCOL.md` | Blank template for creating new protocols (parallel to `TEMPLATE_WORKSTREAM.md`). |
```

---

### 3.5 README.md — updates

**Edit A — Document hierarchy table (current lines 11-15):**

Current:
```markdown
| Layer | Document | Purpose |
|-------|----------|---------|
| **Cockpit checklist** | `SESSION_RUNNER.md` | Step-by-step procedure. Follow this. |
| **Flight manual** | `ITERATIVE_METHODOLOGY.md` | Theory and principles. Reference this. |
| **Mission procedures** | `workstreams/*.md` | Domain-specific adaptations. Execute these. |
```

Replace with:
```markdown
| Layer | Document | Purpose |
|-------|----------|---------|
| **Cockpit checklist** | `SESSION_RUNNER.md` | Step-by-step procedure. Follow this. |
| **Flight manual** | `ITERATIVE_METHODOLOGY.md` | Theory and principles. Reference this. |
| **Mission procedures** | `workstreams/*_WORKSTREAM.md` | Domain-specific adaptations. Execute these. |
| **Campaign templates** | `workstreams/*_PROTOCOL.md` | Multi-session campaign sequences extending a workstream. |
```

Update the surrounding sentence (current line 17): `The checklist constrains. The manual teaches. The mission procedures specialize. All three are needed.`

Replace with: `The checklist constrains. The manual teaches. The mission procedures specialize. Protocols sequence sessions across a campaign. All four are needed.`

**Edit B — Repository Structure tree (current lines 145-174):** add a comment line about protocols inside the `workstreams/` block.

Current:
```
├── workstreams/                      ← Domain-specific adaptations
│   ├── DESIGN_WORKSTREAM.md          ← UI/UX design, visual design, layout
│   ├── ARCHITECTURE_WORKSTREAM.md    ← System architecture, API design
│   ├── DEVELOPMENT_WORKSTREAM.md     ← Feature implementation, bug fix campaigns
│   ├── AUDIT_WORKSTREAM.md           ← Code audits, security reviews, quality gates
│   ├── RESEARCH_DOCUMENTATION_WORKSTREAM.md ← Research papers, technical reports, regulatory analyses
│   └── TEMPLATE_WORKSTREAM.md        ← Create your own workstream
```

Replace with:
```
├── workstreams/                      ← Domain-specific adaptations and campaign templates
│   ├── DESIGN_WORKSTREAM.md          ← UI/UX design, visual design, layout
│   ├── ARCHITECTURE_WORKSTREAM.md    ← System architecture, API design
│   ├── DEVELOPMENT_WORKSTREAM.md     ← Feature implementation, bug fix campaigns
│   ├── AUDIT_WORKSTREAM.md           ← Code audits, security reviews, quality gates
│   ├── RESEARCH_DOCUMENTATION_WORKSTREAM.md ← Research papers, technical reports, regulatory analyses
│   ├── TEMPLATE_WORKSTREAM.md        ← Create your own workstream
│   ├── RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md ← Multi-session campaign for exhaustive claim-source verification
│   └── TEMPLATE_PROTOCOL.md          ← Create your own multi-session campaign template
```

**Edit C — Workstreams table (current lines 200-208):** no change to the table. Add a paragraph below it (after the closing `|` of the last row).

Append after line 208:
```markdown

**Protocols** (multi-session campaign templates) extend a workstream when a deliverable cannot be produced in one session even after correct decomposition. Protocols live in `workstreams/` under the `*_PROTOCOL.md` naming convention. See [`ITERATIVE_METHODOLOGY.md` §Protocols and Multi-Session Campaigns](ITERATIVE_METHODOLOGY.md#protocols-and-multi-session-campaigns) and the realized example [`workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md`](workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md).
```

**Edit D — What's New section:** insert v2.4 above v2.3 (above current line 228).

Insert before the existing `### What's New in v2.3` heading:
```markdown
### What's New in v2.4

- **Protocols promoted to first-class layer** — multi-session campaign templates are now an explicit layer in the document hierarchy alongside workstreams. New section in `ITERATIVE_METHODOLOGY.md` (`§Protocols and Multi-Session Campaigns`); new orientation step in `SESSION_RUNNER.md` (Phase 1 multi-session campaign check); new `workstreams/TEMPLATE_PROTOCOL.md` skeleton.
- **Realized example:** `workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md` — the first concrete protocol, decomposing exhaustive primary-source verification into a planning → execution → consolidation campaign. Supports creation and audit modes.
- **No new principles, phases, gates, or workstreams.** The change is structural-vocabulary only: it names the campaign layer that already exists in practice and gives it a documented home.

```

---

### 3.6 HOW_TO_USE.md — Core Concepts addition

**Insertion point:** Inside the `## Core Concepts` section, between the `### Workstreams` subsection (ends around current line 65) and the `### The Self-Improvement Loop` subsection (starts around current line 66).

**Exact text to insert:**

```markdown

### Protocols

A **protocol** is a multi-session campaign template — a reusable shape for work too large to fit in one session even after correct decomposition. Protocols extend a workstream (which adapts the 6 phases to a domain) by sequencing N sessions toward a single campaign deliverable: planning → per-unit execution → consolidation.

Examples of work that benefits from a protocol:
- Verifying every numeric, dated, or attributed claim in a 5-paper research repository against its primary sources (~500 verification events) — see `workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md`
- Familiarizing a new owner with a 40-module codebase inherited from a departing engineer (one session per module + planning + consolidation)
- Conducting a security-hardening pass across a system with 80+ endpoints (one session per endpoint cluster)

When you face a deliverable that exceeds one session and the campaign shape will recur, write a protocol. Protocols live in `workstreams/` under the `*_PROTOCOL.md` naming convention. The blank starting point is `workstreams/TEMPLATE_PROTOCOL.md`.

A protocol is not a workstream (workstreams adapt the 6 phases to a domain) and not a planning-session output (which is a one-off plan). It is a campaign template — written once, invoked for every campaign of its type. See [`ITERATIVE_METHODOLOGY.md` §Protocols and Multi-Session Campaigns](ITERATIVE_METHODOLOGY.md#protocols-and-multi-session-campaigns) for the formal definition.

```

**No worked example.** Defer to a follow-on session if the realized protocol turns out to be insufficient as a worked example for readers.

---

## 4. Migration: workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md

**Verification done at design time (2026-04-25):**

| Check | Result |
|-------|--------|
| Self-description ("This is a **protocol**, not a workstream...") at line 12 | ✓ Aligns with new methodology vocabulary |
| Use of "protocol" throughout (9 occurrences) | ✓ All 9 in the new technical sense; none in the generic "the methodology" sense |
| Cross-references resolve | ✓ `../ITERATIVE_METHODOLOGY.md`, `RESEARCH_DOCUMENTATION_WORKSTREAM.md`, `AUDIT_WORKSTREAM.md`, `../starter-kit/SESSION_RUNNER.md` all exist |
| References from other files | ✓ `RESEARCH_DOCUMENTATION_WORKSTREAM.md` lines 39 and 218 link to it; `CLAUDE.md` line 70 lists it; both planning docs link to it |
| Filename suffix `_PROTOCOL.md` | ✓ Matches new naming convention |
| Document layout (When to Use, Campaign Structure, per-session sections, Anti-Patterns, Verification Checklist, Example Campaign Outline) | ✓ Matches the structure formalized in `TEMPLATE_PROTOCOL.md` |

**Required edits: zero.**

**Optional refinement (deferred unless lead requests):** add a one-line cross-reference to `§Protocols and Multi-Session Campaigns` in the Relationship to Other Documents table. The current row for `ITERATIVE_METHODOLOGY.md` reads: `Master framework — 9 principles, 6 phases, 12 quality gates. This protocol obeys all of them.` It could be augmented to: `Master framework — 9 principles, 6 phases, 12 quality gates. §Protocols and Multi-Session Campaigns defines this layer. This protocol obeys all of it.` This is cosmetic and does not change behavior; skip during the implementation session unless the lead asks for it during PR review.

---

## 5. Risk Assessment

| # | Risk | Severity | Likelihood | Mitigation in this plan | Residual |
|---|------|----------|------------|-------------------------|----------|
| R1 | **Terminology collision** — "protocol" already means "the methodology" in 8+ existing places (Protocol Erosion, SESSION PROTOCOL, "follow the protocol"). Polysemy may confuse newcomers. | Medium | High | Explicit terminology paragraph in the new methodology section (§3.1); existing uses preserved unchanged; rely on context to disambiguate (countable "a protocol" vs. uncountable "the protocol"). | Some readers will momentarily conflate the two. Cost is mild reading friction. Acceptable. |
| R2 | **Workstream/protocol confusion** — sessions invoke the wrong vocabulary; "workstream" applied to campaign work (no checkpoints written) or "protocol" applied to single-session work (campaign overhead for nothing). | Medium | Moderate | New methodology section explicitly distinguishes; `SESSION_RUNNER.md` Phase 1 multi-session campaign check; `TEMPLATE_PROTOCOL.md` skeleton makes the campaign shape visible by example. | Until a real session makes the mistake, the exact failure shape is unknown. Failure Mode #24 deferred until evidence (per Decision 2.5). |
| R3 | **Discoverability of TEMPLATE_PROTOCOL** — new protocols don't get written because the template isn't visible. | Low | Moderate | Linked from `CLAUDE.md`, `README.md`, `ITERATIVE_METHODOLOGY.md` (in §Protocols), `HOW_TO_USE.md`. | Validate at the next opportunity by tracking whether a second protocol gets written within ~3 months. |
| R4 | **Drift between protocol and parent workstream** — workstream evolves, protocol doesn't. Or protocol's vocabulary diverges from the workstream's primitives (e.g., `RESEARCH_DOCUMENTATION_WORKSTREAM.md` renames Claim-Source Map; `RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md` still references old name). | Medium | Low (near-term) | Each protocol's `Relationship to Other Documents` table names the parent workstream — drift becomes visible at PR-review time on either document. The methodology's self-correcting loop (§Self-Correcting Loop) handles this when drift causes a session failure. | Nominal — same risk applies to any cross-document link in the methodology. |
| R5 | **Adopters miss the new orientation step** — projects that adopted v2.1–v2.3 don't re-sync their `SESSION_RUNNER.md` and never see the multi-session campaign check. | Low | Moderate | `bin/sync` from v2.2 propagates changes; `bin/status` reports drift. Adopters who follow the v2.2+ workflow pick up the change automatically. | Adopters who don't re-sync don't get the check. This is a pre-existing condition for any methodology change, not new. |
| R6 | **Plan execution drift** — implementation session reads this design plan and improvises. Adds scope, omits an item, or reinterprets a decision. | Medium | Low | This document specifies exact text and named insertion points. The implementation session's job is mechanical. The Implementation Session Execution Checklist (§6) is the runbook. | If the implementation session deviates, close-out flags it; PR review catches it before merge. |
| R7 | **CLAUDE.md / README.md hierarchy table de-sync** — only one of the two tables gets updated, leaving an inconsistency. | Low | Low | §3.4 and §3.5 both specify the table edit explicitly with current and replacement text. Both edits are in §6 checklist as separate line items. | Verification step in §6 grep-checks for `workstreams/*.md` (the old pattern) to confirm both tables were updated. |
| R8 | **Anchor-link breakage** — the new section's auto-generated GitHub anchor (`#protocols-and-multi-session-campaigns`) is referenced by `SESSION_RUNNER.md` and `HOW_TO_USE.md`. Typos in either side break the link. | Low | Low | All anchor references in this plan use the same lowercased-and-hyphenated form. Verification step in §6 includes a render-check on GitHub or a markdown previewer to confirm anchors resolve. | If GitHub's anchor algorithm is updated, links break for everyone simultaneously and are easy to detect. |

**No critical risks identified.** The change is structural-vocabulary, not behavioral.

---

## 6. Implementation Session Execution Checklist

The implementation session should be a single session per the methodology's "1 and done" rule. It is a writing-and-editing session, not a campaign — protocol promotion is itself one deliverable, even though it touches multiple files.

### 6.1 Pre-flight

- [ ] On a feature branch (recommended: `feature/protocols-as-first-class`)
- [ ] `git status` clean apart from this design plan and the WIP files (`docs/planning/protocols-as-first-class.md`, `docs/planning/protocols-integration-session-plan.md`, `workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md`, modified `CLAUDE.md`, modified `workstreams/RESEARCH_DOCUMENTATION_WORKSTREAM.md`)
- [ ] Read this design plan in full
- [ ] Read the proposal article and session-plan brief

### 6.2 Edits in order

| # | File | Action | Reference |
|---|------|--------|-----------|
| 1 | `ITERATIVE_METHODOLOGY.md` | Insert new section between current line 302 and line 304 | §3.1 |
| 2 | `starter-kit/SESSION_RUNNER.md` | Insert new paragraph between current line 57 and line 59 | §3.2 |
| 3 | `workstreams/TEMPLATE_PROTOCOL.md` | Create file | §3.3 |
| 4 | `CLAUDE.md` | Update hierarchy table (Edit A), add v2.4 versioning entry (Edit B), update version reference (Edit C), add `TEMPLATE_PROTOCOL.md` row to Protocols subsection (Edit D) | §3.4 |
| 5 | `README.md` | Update hierarchy table (Edit A), update repo structure tree (Edit B), add post-table paragraph (Edit C), insert What's New v2.4 (Edit D) | §3.5 |
| 6 | `HOW_TO_USE.md` | Insert Protocols subsection in Core Concepts | §3.6 |

### 6.3 Verification

- [ ] `grep -n "workstreams/\*\.md" CLAUDE.md README.md` returns no results (both hierarchy tables updated to use specific suffixes)
- [ ] `grep -rn "EXHAUSTIVE_VERIFICATION" .` shows the same set of references as before (no new orphan links)
- [ ] `grep -n "TEMPLATE_PROTOCOL" CLAUDE.md README.md HOW_TO_USE.md ITERATIVE_METHODOLOGY.md` shows references in all four files
- [ ] Render `README.md`, `ITERATIVE_METHODOLOGY.md`, and `HOW_TO_USE.md` (markdown previewer or GitHub) and verify the new anchor `#protocols-and-multi-session-campaigns` resolves
- [ ] Confirm `workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md` is unchanged (zero migration edits per §4)
- [ ] Re-read the new methodology section and the new SESSION_RUNNER step to verify they say what this plan specifies (failure mode #20: edit from memory)

### 6.4 Commit message template

```
feat: promote protocols to first-class methodology layer (v2.4)

Adds explicit vocabulary and a documented home for multi-session
campaign templates. Protocols extend a workstream when a deliverable
cannot be produced in one session even after correct decomposition.

- ITERATIVE_METHODOLOGY.md: new §Protocols and Multi-Session Campaigns
- starter-kit/SESSION_RUNNER.md: new Phase 1 multi-session campaign check
- workstreams/TEMPLATE_PROTOCOL.md: new blank template
- CLAUDE.md, README.md, HOW_TO_USE.md: hierarchy updates and version bump

No new principles, phases, gates, or workstreams. The realized example
(workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md) was authored
with consistent terminology and required zero migration edits.

Implements docs/planning/protocols-integration-design.md.
Closes the proposal in docs/planning/protocols-as-first-class.md.
```

### 6.5 PR description template

```
## Summary

Promotes "protocol" from an implicit file-tree pattern to a first-class
methodology layer alongside workstreams. v2.4 minor.

## What changes

- New ~410-word section in `ITERATIVE_METHODOLOGY.md` defining the layer
- New ~100-word orientation step in `SESSION_RUNNER.md` Phase 1
- New `workstreams/TEMPLATE_PROTOCOL.md` skeleton
- Hierarchy-table updates in `CLAUDE.md` and `README.md` (split workstreams from protocols)
- New "What's New in v2.4" section in `README.md`
- New "Protocols" subsection in `HOW_TO_USE.md` Core Concepts
- Version bumped to v2.4 in CLAUDE.md

## What does not change

- 9 principles unchanged
- 6 phases unchanged
- 12 quality gates unchanged
- 5 workstreams unchanged
- 23 failure modes unchanged
- `workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md` unchanged
  (terminology was authored consistent with the new vocabulary)

## Test plan

- [ ] Render README, ITERATIVE_METHODOLOGY, HOW_TO_USE in a markdown previewer; confirm new anchor resolves
- [ ] Read the new methodology section end-to-end; confirm terminology paragraph disambiguates the two senses of "protocol"
- [ ] Read the new SESSION_RUNNER step in context with surrounding Phase 1 content; confirm it doesn't disrupt the existing flow
- [ ] Read TEMPLATE_PROTOCOL.md against RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md; confirm the realized protocol fits the skeleton
- [ ] Approve via review

## Background

- Proposal article: `docs/planning/protocols-as-first-class.md`
- Session-plan brief: `docs/planning/protocols-integration-session-plan.md`
- Design plan: `docs/planning/protocols-integration-design.md` (this PR)
```

---

## 7. Out of Scope (Explicit)

- **Writing additional protocols.** Only the existing one stays; no new protocols are authored.
- **Adding Failure Mode #24** (per Decision 2.5).
- **Adding a new quality gate** (per Decision 2.6).
- **Renaming "Protocol Erosion" or any existing "protocol" usage** (per Decision 2.2).
- **Bumping past v2.4** to combine with future minor changes.
- **Editing `workstreams/RESEARCH_EXHAUSTIVE_VERIFICATION_PROTOCOL.md`** (per §4: zero migration edits required).
- **Adding a worked example to HOW_TO_USE.md** (per Decision 2.7).
- **Updating any starter-kit file other than `SESSION_RUNNER.md`** (no other starter-kit files reference protocols and none need to).

---

## 8. Acceptance criteria

This design plan is complete when:

- [x] All 8 deliverables in `docs/planning/protocols-integration-session-plan.md` are addressed with exact text or explicit decisions
- [x] Every edit is specified by file + insertion point + replacement text
- [x] Every decision is justified
- [x] Risk assessment covers terminology, drift, and execution
- [x] Implementation session checklist is mechanical (no further design decisions required)

The plan is **not** complete if:

- It contains "TBD" sections (none do)
- It surfaces multiple alternatives without choosing one (each decision is bound)
- It defers decisions to the implementation session (none are deferred apart from the §4 cosmetic option, which is explicitly skippable)

The next step is methodology-lead review of this PR. After approval, a separate implementation session executes §6 mechanically.
