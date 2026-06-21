# Reasoning-Tier Generalization — Planning Document

**Status:** PLAN (decisions ratified 2026-06-21). Implementation is a **separate session + separate PR** — do **not** implement from this branch.
**Session type:** Planning session (`SESSION_RUNNER.md` §Planning Sessions — the plan is the deliverable).
**Plan branch (fork-only):** `docs/reasoning-tier-plan`, based on `origin/main` (v2.8-synced). This document never goes to upstream.
**Implementation target:** a new branch off `upstream/main` (v2.8) for a clean PR to `KJ5HST/methodology`. rmsharp has **no upstream merge rights** — the maintainer (KJ5HST) reviews, merges, and assigns the version + "What's New" entry.
**Recommended drafting effort for implementation:** deepest-reasoning mode (`/effort max`, Opus) — the rule this contribution encodes applies to its own authoring.
**Resolves:** the gap flagged in user feedback — the methodology recommends a reasoning tier for *research documentation only* and the operator expects it for all heavy work (refactoring, planning, research). This contribution generalizes that single-domain recommendation into a cross-cutting principle.
**Do NOT bundle** with the tutorials work (`feat/tutorials-p1-scaffolding` / PR #38) — independent deliverable, independent PR.

---

## 1. The gap (verified, not assumed)

A three-way adversarial corpus sweep (keyword + semantic + recommendation-layer reads over all 31 tracked markdown files) **confirms** the premise: exactly **one** line in the corpus recommends a reasoning/effort/model tier for a class of work —

> `workstreams/RESEARCH_DOCUMENTATION_WORKSTREAM.md:33` (inside its `## Recommended Operating Mode`, lines 29–35):
> *"This workstream benefits materially from your agent's deepest-reasoning mode (max-effort, deep-thinking, or extended-reasoning settings, depending on the toolchain). The marginal cost is latency and tokens; the cost of an undetected misattribution is reputational. Set the mode at session start — not after a problem appears."*

The recommendation layer (`RECOMMENDED_SKILLS.md`, `SAFEGUARDS.md`, `ITERATIVE_METHODOLOGY.md` §Recommended Skills) is **silent** on reasoning tiers — it recommends *skills* only, never a mode/model/effort setting. Near-misses were ruled out: the two campaign "context exhaustion" lines (`RESEARCH_EXHAUSTIVE_VERIFICATION_CAMPAIGN.md:62`, `INHERITED_CODEBASE_FAMILIARIZATION_CAMPAIGN.md:66`) argue for *splitting work across more sessions*, not raising a tier; `SAFEGUARDS.md`'s "modes" denote cognitive posture (Engineer/Architect) or the plan-mode gate, not a reasoning tier. The gap is real and is exactly the one to close.

## 2. The unifying rule — an instance, not an invention

**Rule to encode:** *reasoning tier ∝ blast radius × irreversibility × compounding cost.*

This is **not a new axis** — every multiplicand already exists as named methodology vocabulary, so the new principle must read as the *same risk lens* applied to "how hard to reason," not a fresh concept:

| Multiplicand | Already lives at | Verbatim anchor |
|---|---|---|
| **blast radius** | `SAFEGUARDS.md` §Blast Radius Limits | header `:42`; 5-file cap `:49` ("Forces incremental, recoverable progress") |
| **irreversibility / recoverability** | `SESSION_RUNNER.md` §Vertical Slice Sessions | `:144` ("Recoverability — not verifiability — is the ceiling on slice size"); `:146` (non-collapsible boundary list) |
| | `ITERATIVE_METHODOLOGY.md` Principle 9 (Session Scope Bounding) | `:126` |
| | `ITERATIVE_METHODOLOGY.md` Principle 3 (Hard Phase Gates) | `:84` ("the most valuable gate is between Present and Implement") |
| **compounding cost** | `ITERATIVE_METHODOLOGY.md` Principle 4 / "knowledge compounds" | `:55` |

The same intuition the framework already runs — *the most expensive, least-reversible transition gets the hardest gate; the largest blast radius gets the tightest commit cap* — generalized to: *the heaviest, least-reversible, most-compounding work gets the deepest reasoning.*

## 3. Design constraints (binding)

1. **Agent-independence (hard).** The core principle names the **capability** ("your agent's deepest-reasoning mode … depending on the toolchain"), not a brand token. Concrete `/effort max` / model-tier examples live only in the recommendation layer. Mirrors `CONTEXT_TEMPLATE.md:57` (the v2.7.2 "agent-level memory" rename) and the existing `RESEARCH_DOCUMENTATION_WORKSTREAM.md:33` phrasing.
2. **No renumbering.** The "9 principles, 6 phases, 12 quality gates" framing and the FM count (26) are load-bearing (`CLAUDE.md`). The principle ships as a **cross-cutting section**, *not* a 10th `### N.` principle. No FM/phase/gate touched.
3. **Cite-don't-restate (ownership split).** Methodology owns *when/why* to raise the tier; the agent owns *how*. State the rule **once** (core), and have workstreams **cite** it. Mirrors `ITERATIVE_METHODOLOGY.md:373` ("Methodology recommends; methodology does not reimplement").
4. **Count-threshold footprint.** One coherent idea → one canonical paragraph + inline citations, not a dedicated apparatus per file (`RECOMMENDED_SKILLS.md:11`).
5. **Anti-erosion guard (non-negotiable).** `SESSION_RUNNER.md:295` (FM #17) **already** names *"citing a 'deeper dive' or any high-parallelism mode to skip … is protocol erosion."* The new principle recommends **higher** effort while explicitly **not** licensing any gate-skip or scope-widening — the same shape as "A skill is not a phase" (`ITERATIVE_METHODOLOGY.md:381`). This guard must be stated *in* the new section so it can never be read as an erosion lever.
6. **Recompose, don't accrete.** The existing `RESEARCH_DOCUMENTATION_WORKSTREAM.md:33` paragraph is *recomposed* to read as a high-stakes instance of the general rule — not left as a one-off with a corrective note bolted on.

## 4. Ratified decisions (this session)

1. **Home/shape →** a **new cross-cutting section** in `ITERATIVE_METHODOLOGY.md` (in the §Recommended Skills register: bolded maxim + prose, *outside* the 9 numbered principles).
2. **Scope →** **heavy + planning + inverse:** core principle; recompose RESEARCH:33; thin cited notes in ARCHITECTURE (Refactor Heuristics), DEVELOPMENT, and SESSION_RUNNER (Planning Sessions); a medium note in AUDIT; an **inverse** note in DESIGN (lighter tier is the honest default); a reusable scaffold in TEMPLATE_WORKSTREAM. (Explicitly **not** a tier column on the SESSION_RUNNER session-type table — that would over-claim a tier for all 8 rows.)
3. **Concrete examples →** in **`RECOMMENDED_SKILLS.md`** (the brand-coupled recommendation layer); the core stays capability-framed.

## 5. Edit plan (file-by-file, verified anchors + text sketches)

> Cross-references between distributed files use the **section name** ("`ITERATIVE_METHODOLOGY.md` §Matching Reasoning Effort to Stakes"), not a fragile relative link — consistent with how the methodology already cites phases/skills by name and avoiding the v2.8 #33 link-topology paradox. Where a relative link *is* added, it must follow the per-file adopter-depth convention and pass `bin/check-links`. The proposed section name is **"Matching Reasoning Effort to Stakes"** (alt: "Recommended Reasoning Effort," parallel to the existing §Recommended Operating Mode / §Recommended Skills naming); maintainer may adjust at merge.

### A. `ITERATIVE_METHODOLOGY.md` — NEW cross-cutting section
**Anchor:** insert between the `---` at line 383 and `## The Session Runner` at line 385 (i.e. a new peer section immediately after §Recommended Skills, which ends at line 381). Verified exact.
**Sketch:**
```markdown
## Matching Reasoning Effort to Stakes

> **Match reasoning effort to the stakes, not the task label.**
>
> Set your agent's reasoning depth by the work's *blast radius × irreversibility ×
> compounding cost* — the same risk lens the methodology already uses to size a
> vertical slice (Principle 9) and to place its hardest gate (Principle 3). High on
> any axis — wide blast radius (changes ripple across many call sites or readers),
> low reversibility (migrations, cutovers, published claims, operator-approval
> boundaries), or high compounding cost (a planning or architecture error every later
> session inherits) — warrants your agent's deepest-reasoning mode (max-effort,
> extended-reasoning, or a larger thinking budget, depending on the toolchain). The
> marginal cost is latency and tokens; the cost of a shallow decision on heavy work is
> rework that compounds. Set the mode at session start — not after a problem appears.

Cheap, reversible, mechanical work — a one-line fix, a rename the compiler catches, a
reversible config tweak — does not need it; a lighter setting is the honest default
there. The axis runs both ways.

Methodology owns *when and why* to raise the tier (this rule); your agent owns *how*
(the specific effort or model mechanism — see
[`RECOMMENDED_SKILLS.md`](../../RECOMMENDED_SKILLS.md) for concrete Claude Code
settings). And a higher tier is not a license: like a skill, a deeper-reasoning mode
sharpens a phase — it never authorizes skipping orientation, the stub, close-out, or
any hard gate, nor widening a session beyond its one declared deliverable (failure
mode #17). Reason harder; stop at the same gates.
```
*(Relative link `../../RECOMMENDED_SKILLS.md` matches the existing usage at `ITERATIVE_METHODOLOGY.md:377`.)*

### B. `workstreams/RESEARCH_DOCUMENTATION_WORKSTREAM.md` — recompose the seed
**Anchor:** §Recommended Operating Mode, lines 29–35. Verified exact.
**Change:** keep the line-31 reputational-stakes paragraph; **recompose line 33** so it cites the core rule and keeps only the *research-specific* rationale; keep the line-35 human-author analogue. The capability gloss ("max-effort, extended-reasoning…") **relocates to the core section** to avoid duplication (Learning #7 drift).
**Sketch (replaces line 33):**
```markdown
Research documentation is a high-stakes instance of the general rule — *match reasoning
effort to the stakes* (`ITERATIVE_METHODOLOGY.md` §Matching Reasoning Effort to Stakes).
A misattribution is effectively irreversible once published and its cost compounds
across every reader who trusts it, so this workstream sits at the top of the tier: set
your agent's deepest-reasoning mode at session start — not after a problem appears.
```

### C. `workstreams/ARCHITECTURE_WORKSTREAM.md` — refactoring note (thin, cited)
**Anchor:** §Refactor Heuristics (line 187); append to the `### When to apply these heuristics` list (~line 214). Verified exact. (No `## Recommended Skills` section here — it cites `/improve-codebase-architecture` inline; do not add a section.)
**Sketch (appended bullet):**
```markdown
- Run these heuristics — and the refactor they motivate — at your agent's deepest
  available reasoning setting. Refactoring an existing module is high blast-radius
  (changes ripple across call sites) and often hard to reverse once committed; the
  cost of a shallow analysis compounds across every later session that navigates the
  result (`ITERATIVE_METHODOLOGY.md` §Matching Reasoning Effort to Stakes).
```

### D. `workstreams/DEVELOPMENT_WORKSTREAM.md` — campaign note (thin, cited)
**Anchor:** §When to Use (line 7); insert after the "Not for one-off fixes" paragraph (after line 15). Verified exact.
**Sketch (blockquote):**
```markdown
> Feature and bugfix campaigns mutate code and compound across sessions — heavy work.
> Default to a deeper reasoning tier (`ITERATIVE_METHODOLOGY.md` §Matching Reasoning
> Effort to Stakes).
```

### E. `workstreams/AUDIT_WORKSTREAM.md` — medium note (reuse "sharper instrument")
**Anchor:** after the existing §Recommended Skills section (closes ~line 32, "a sharper instrument, not a hard dependency"). Verified exact.
**Sketch (short paragraph):**
```markdown
Reasoning effort is the other sharper instrument. An audit mutates nothing (low
irreversibility), but a missed finding has high downstream cost and findings compound —
so scale reasoning depth to the cost of a missed finding (`ITERATIVE_METHODOLOGY.md`
§Matching Reasoning Effort to Stakes).
```

### F. `workstreams/DESIGN_WORKSTREAM.md` — INVERSE note (keeps the axis honest)
**Anchor:** §When to Use (line 7); insert after the bullet list (after line 13). Verified exact.
**Sketch (blockquote):**
```markdown
> Design output is iterative and cheap to revise — lower blast radius than development
> or research. A lighter reasoning tier is the honest default here; reserve the deepest
> mode for genuinely irreversible commitments (`ITERATIVE_METHODOLOGY.md` §Matching
> Reasoning Effort to Stakes). The axis runs both ways.
```

### G. `starter-kit/SESSION_RUNNER.md` — planning-session note
**Anchor:** §Planning Sessions umbrella paragraph, lines 96–97 (primary — fires at session start). Verified exact. Optional backstop: a checklist item near line 125 in §Planning Session Checklist.
**Sketch (sentence in the umbrella paragraph):**
```markdown
Set your agent's deepest available reasoning mode at session start (capability: maximum
reasoning depth — e.g. `/effort max` where supported). A plan is low-reversibility and
high-compounding: its errors propagate into every executor session that trusts it
(`ITERATIVE_METHODOLOGY.md` §Matching Reasoning Effort to Stakes).
```
**Optional checklist backstop (after line 125):** `- [ ] Deepest available reasoning mode set at session start`

### H. `starter-kit/RECOMMENDED_SKILLS.md` — concrete examples (the brand-coupled home)
**Anchor:** new `## Reasoning Effort` subsection (a setting, not a skill; ≥2 example mappings justify a section). Place near the top conventions or after the external-skills table.
**Sketch:**
```markdown
## Reasoning Effort

Not a skill — a setting. The methodology owns *when* to raise reasoning effort
(`ITERATIVE_METHODOLOGY.md` §Matching Reasoning Effort to Stakes: tier ∝ blast radius ×
irreversibility × compounding cost). This index — the recommendation layer — names the
concrete Claude Code mechanism that satisfies it. Like the skill SHAs above, these are
example settings for one agent; other agents expose the capability under other names.

| Work type | Why | Example (Claude Code) |
|---|---|---|
| Deep research / regulatory docs | misattribution is irreversible + reputational | `/effort max`, deepest model (e.g. Opus) |
| Architecture / cross-module refactor | wide blast radius, low reversibility | `/effort high`–`max`, deepest model |
| Planning sessions | errors compound across every executor session | `/effort high`–`max` |
| Audits | a missed finding has high downstream cost | `/effort high` |
| Feature / bugfix campaigns | quality compounds across sessions | `/effort medium`–`high` |
| Mechanical / reversible edits (rename, config) | cheap to undo | `/effort low`–`medium`, lighter model (e.g. Sonnet/Haiku) |

A higher tier sharpens a phase; it never licenses crossing a gate (failure mode #17).
```
*(Model names are illustrative and Claude-specific — acceptable here because this is the brand-coupled recommendation layer, not the agent-independent core.)*

### I. `workstreams/TEMPLATE_WORKSTREAM.md` — reusable scaffold
**Anchor:** after the optional `## Recommended Skills` scaffold (line 16), before the line-26 `---`. Verified exact.
**Sketch:**
```markdown
## Recommended Reasoning Tier *(optional — set this domain's default)*

One line keying this workstream's default reasoning tier to its blast radius ×
irreversibility × compounding cost, citing `ITERATIVE_METHODOLOGY.md` §Matching
Reasoning Effort to Stakes. Heavy / irreversible / compounding → deepest mode;
cheap / reversible / mechanical → lighter. Delete if the domain's tier is unremarkable.
```

## 6. Implementation phasing + commit discipline

One cohesive deliverable (a cross-cutting documentation convention, analogous to v2.6's skill-recommendation layer), shipped as **one PR** with **checkpoint commits ≤5 files each** (`SAFEGUARDS.md:49`, per-commit cap):

- **Commit 1 — spine (3 files):** A (core section) + B (recompose RESEARCH seed) + H (RECOMMENDED_SKILLS examples). Establishes the canonical rule + its brand-coupled instance before anything cites it.
- **Commit 2 — heavy workstreams (3 files):** C (ARCHITECTURE) + D (DEVELOPMENT) + E (AUDIT).
- **Commit 3 — inverse + planning + scaffold (3 files):** F (DESIGN inverse) + G (SESSION_RUNNER planning) + I (TEMPLATE scaffold).

At **each** commit boundary: render the touched markdown (no broken tables/links), run `bin/check-links` (simulated adopter tree) and `bin/tests.sh`. Note: `SESSION_RUNNER.md` and the workstream files are **distributed** (in the `bin/_manifest.py` corpus) — confirm no sync/disposition surprises, though these are all `tracked` framework docs, not `seed`.

## 7. Verification (Learning #7 — cross-reference completeness)

A change that adds a cross-reference or generalizes a scoped claim shows only the present-side edit in `git diff`; grep the rest:

1. **Stale "research-only" prose.** After generalizing, any text asserting the tier rec is research-specific becomes stale. Re-grep the corpus (incl. `README.md`, `CLAUDE.md` changelog prose) for "research" + tier language; the recomposed RESEARCH:33 must read as an *instance*, not the sole home.
2. **Each new cross-reference resolves.** Grep that every "§Matching Reasoning Effort to Stakes" citation has a real destination heading, and that `RECOMMENDED_SKILLS.md` §Reasoning Effort exists where cited.
3. **Link topology.** Any relative cross-doc link added → `bin/check-links` against the simulated adopter tree (v2.8 #33). Prefer name-based cross-reference to avoid the paradox entirely.
4. **Count claims unchanged.** Confirm "9 principles, 6 phases, 12 quality gates" and FM count (26) are untouched — the section is cross-cutting, not a 10th principle; no FM/phase/gate renumbered.
5. **FM #17 alignment.** The new section's anti-erosion clause must not contradict `SESSION_RUNNER.md:295`; ideally it cross-references it.

## 8. Process constraints (recap)

- Own planning session → **own PR**; **not** bundled with tutorials PR #38.
- Implementation branches off **`upstream/main` (v2.8)** for a clean PR; **this plan doc is fork-only** (`docs/reasoning-tier-plan`, pushed to `origin` only).
- **Version + "What's New" are the maintainer's call** (KJ5HST). Suggested framing: a **minor** release (it adds a new content convention alongside phases/principles/workstreams/skills, like v2.6 did for skills) — but defer to the maintainer; do not pre-stamp a version number.
- Recommend **`/effort max`** for the implementation drafting session.

## Appendix — verified anchor table (all exact, zero drift vs v2.8 tree)

| File | Anchor | Line | Role |
|---|---|---|---|
| `ITERATIVE_METHODOLOGY.md` | `## Recommended Skills` | 371 | register precedent for a cross-cutting section |
| | maxim "Methodology recommends…" | 373 | ownership-split model |
| | "A skill is not a phase." | 381 | anti-erosion model; §Recommended Skills ends here |
| | `---` / `## The Session Runner` | 383 / 385 | **insertion point for new section A (between them)** |
| | "When to Use" / Principle 9 / Principle 3 / "knowledge compounds" | 49 / 126 / 84 / 55 | risk-lens cross-refs |
| `RESEARCH_DOCUMENTATION_WORKSTREAM.md` | `## Recommended Operating Mode` (seed) | 29–35 (key 33) | recompose (B) |
| `ARCHITECTURE_WORKSTREAM.md` | `## Refactor Heuristics` / `### When to apply` | 187 / ~214 | refactor note (C) |
| `DEVELOPMENT_WORKSTREAM.md` | `## When to Use` | 7 (after 15) | campaign note (D) |
| `AUDIT_WORKSTREAM.md` | `## Recommended Skills` (closes ~32) | 22 | medium note (E) |
| `DESIGN_WORKSTREAM.md` | `## When to Use` | 7 (after 13) | inverse note (F) |
| `starter-kit/SESSION_RUNNER.md` | §Planning Sessions / Checklist / FM #17 | 93 (umbrella 96–97) / 121 / 295 | planning note (G) + guard |
| `starter-kit/RECOMMENDED_SKILLS.md` | count-threshold rule | 11 | new §Reasoning Effort (H) |
| `starter-kit/SAFEGUARDS.md` | §Blast Radius Limits / 5-file cap | 42 / 49 | "blast radius" term home |
| `starter-kit/CONTEXT_TEMPLATE.md` | "agent-level memory" | 57 | agent-independence model |
| `workstreams/TEMPLATE_WORKSTREAM.md` | optional `## Recommended Skills` scaffold | 16 | new tier scaffold (I) |

*Research basis: 8-agent verification workflow (3-way premise sweep + 4 anchor checks + precedent/risk-lens extraction), 2026-06-21. All line numbers verified against the v2.8 tree.*
