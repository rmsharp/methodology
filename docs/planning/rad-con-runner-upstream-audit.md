# Audit: rad-con SESSION_RUNNER.md — Upstream Candidates for Canonical

**Issue:** [methodology#6](https://github.com/KJ5HST/methodology/issues/6) — *Post-v2.2: audit rad-con SESSION_RUNNER.md for content worth upstreaming*
**Session:** 367 (2026-04-21)
**Workstream:** `workstreams/AUDIT_WORKSTREAM.md`
**Status:** AUDIT COMPLETE — recommendations pending user approval for a v2.3 content release.

---

## 1. Audit Summary

- **Scope:** Classify every substantive deviation of `rad-con/SESSION_RUNNER.md` (837 lines, ~90 sessions of operator evolution) against canonical `methodology/starter-kit/SESSION_RUNNER.md` (297 lines, shipped in v2.2 on 2026-04-21).
- **Criteria:** For each rad-con-only passage, classify as **Universal** / **Project-specific** / **Already-canonical-in-spirit** / **Noise (editing artifact)**.
- **Coverage:** 100%. Both files read end-to-end. Diff hunks identified by structural walk, not automated diff (cleaner than `diff -u` for this purpose because rad-con's structural renumbering makes hunk-level diff noisy).
- **Finding count:** 6 Universal upgrade candidates, 4 Project-specific exclusions, 3 Already-canonical, 1 Noise/bug, 1 structural change (3E Runtime Smoke Test).
- **Scope boundary honored:** This audit does NOT propose content changes to rad-con, does NOT touch ftx1-hamlib, and does NOT draft the v2.3 content PR. That's a separate session.

---

## 2. Structural Comparison

Both files follow the same Phase 0 → 1 → 1B → 2 → 3 → FMs → Degradation → Learnings → Templates spine. The deviations fall in predictable places:

| Area | Canonical (v2.2) | rad-con | Nature of divergence |
|------|------------------|---------|----------------------|
| Phase 0 step 3 | BACKLOG.md fallback | same | none of substance |
| Phase 1 task-mapping table | 7 generic rows | 10 rows incl. 3 rad-con-specific | rad-con added project-specific rows |
| Phase 1B stub | 4-line block | same + "structural control, not a suggestion" w/ Session 62+ evidence | rad-con adds universal framing |
| Phase 2 Planning Sessions | grep-inventory rule + checklist | same + Session 93-95 anecdote | rad-con adds evidence |
| Phase 3 structure | 3A–3F (no runtime test) | 3A–3G incl. **3E Runtime Smoke Test** | **rad-con has an entire extra phase step** |
| Phase 3D evidence requirement | 2 paragraphs, generic | same + Session 38/40/43/44/61/63 citations | rad-con adds evidence |
| FM table | 23 FMs | **24 FMs** — extra FM #20 "Build-passes-ship-it" | rad-con adds one universal FM |
| Degradation Detection | "Failure mode #N (…) is active" | **"Session N (…) is active"** in several rows | **Editing artifact / bug in rad-con** |
| Learnings table | 1 entry (plan-mode draft) | **8 entries (nums 1-8)** | rad-con has 7 more, mix of universal and project |
| Launch Prompts | generic "Design" | "Profile design" | project-specific |
| Session Learnings section | (none) | **lines 329-838 (509 lines)** | 100% project-specific case studies |

---

## 3. Findings

### Finding #1 — [UNIVERSAL, HIGH VALUE] Add Phase 3E "Runtime Smoke Test"

- **Severity:** Moderate (structural addition, touches phase numbering).
- **Location:** rad-con lines 205–217.
- **Evidence:**
  ```
  ### 3E: Runtime Smoke Test

  **If your deliverable changes runtime behavior** (plugin loading, service
  registration, startup config, WebSocket handlers, handler dispatch, config
  resolution), launch the application before committing and verify the behavior:
  ...
  **This step exists because:** Sessions 151-152 shipped code that compiled
  and built cleanly but broke at runtime due to plugin version collision and
  registration order.
  ```
- **Impact:** Canonical currently stops at "build clean = verify correctness." Any adopting project that ships runtime integrations (plugins, services, WebSocket handlers, DI wiring, config resolution) is vulnerable to shipping a build-passing bug that only manifests at startup. The tax-forms and wsjtx workstreams have both hit this class of failure in other guises.
- **Recommendation (for v2.3 PR):**
  1. Insert canonical Phase 3E: Runtime Smoke Test between canonical current 3D and 3E (Commit).
  2. Renumber current 3E Commit → 3F, 3F Report and STOP → 3G.
  3. Generalize the vocabulary. rad-con's examples ("plugin loading, WebSocket handlers, handler dispatch") are rad-con-specific. Canonical should use "startup behavior, service registration, integration points, dispatch wiring" + a generic example.
  4. Replace "Sessions 151-152" citation with a generic "shipped code that passed the build but broke at startup — invisible to static analysis" — canonical does not track sessions by number.
  5. Add the matching FM entry (see Finding #2).

### Finding #2 — [UNIVERSAL, HIGH VALUE] Add FM #24 "Build-passes-ship-it"

- **Severity:** Moderate.
- **Location:** rad-con line 261 (FM #20).
- **Evidence:**
  ```
  | 20 | **Build-passes-ship-it** | Session confirms `mvn clean package` or
  `npm run build` succeeds and treats that as verification of correctness.
  But the deliverable involves runtime behavior ... Build tools verify
  compilation, not integration. |
  ```
- **Impact:** The paired FM makes 3E enforceable. Without this FM, 3E is a recommendation; with it, degradation detection can flag its absence.
- **Recommendation:** In canonical's v2.3 FM table, add this as FM #24 (current canonical ends at FM #23). Keep the Degradation Detection table in sync — a new row: *"Self-assessment notes 'no runtime verification' without treating it as a defect | FM #24 (build-passes-ship-it) is active | Run the runtime smoke test or document why it's impossible."*
- **Caveat:** rad-con numbers this FM as #20 and pushes canonical's FMs 20–23 down to 21–24. Canonical should append as #24 instead (stable numbering — existing adopters' memories reference FMs by number).

### Finding #3 — [UNIVERSAL] Add "structural control, not a suggestion" framing

- **Severity:** Minor.
- **Location:** rad-con line 79.
- **Evidence:**
  ```
  **This is a structural control, not a suggestion.** Sessions 62+ demonstrated
  that sessions which skip close-out leave the next session blind, which causes
  cascading failures.
  ```
- **Impact:** The canonical Phase 1B block currently says *why* the stub exists (ghost sessions) but does not invoke the "structural control" framing. That framing is a generalizable discipline lever — it applies to any mandatory step. Adopting projects gain a reusable vocabulary.
- **Recommendation:** Add to canonical Phase 1B as a closing line, or — better — promote to a short callout near the top of Phase 3 ("Close-out steps are structural controls, not suggestions"). Strip the "Sessions 62+" citation; replace with "this is how clean-delivery streaks collapse: each session drops one mandatory step until nothing remains" (abstracts the same insight from rad-con Learning #6, see Finding #4).

### Finding #4 — [UNIVERSAL] Add "Protocol discipline is perishable" as a canonical Learning

- **Severity:** Moderate (adds teeth to FM #17 Protocol erosion).
- **Location:** rad-con line 303 (Learning #6).
- **Evidence:**
  ```
  Protocol discipline is perishable. Sessions 34-47 maintained 14 consecutive
  clean deliveries through rigorous protocol adherence. Within 12 hours of
  relaxed discipline (Sessions 62-63+), scores collapsed from 9/10 to 1/10
  with ghost sessions leaving no trace. **The protocol doesn't maintain itself.**
  ```
- **Impact:** Canonical's FM #17 "Protocol erosion" describes the slow-drip case (each session shaves off one step). rad-con Learning #6 documents the fast-collapse case (12-hour failure cascade after 14 clean sessions). These are different failure shapes — the slow-drip erodes the protocol; the fast-collapse is what happens when the protocol is briefly unsupervised. Both belong in the record.
- **Recommendation:** Add to canonical's Learnings table as Learning #2 (after the existing plan-mode entry). Generalize: "14 clean sessions can collapse to 1/10 within 12 hours of relaxed discipline. The protocol is perishable — it doesn't maintain itself. Each session must actively re-internalize it." Strip the session numbers.

### Finding #5 — [UNIVERSAL] Add grep-inventory anecdote as reinforcement for Planning Sessions rule

- **Severity:** Minor.
- **Location:** rad-con line 108 (Planning Sessions subsection) + rad-con Learning #7 (line 302).
- **Evidence:**
  ```
  **Evidence from Sessions 93-95:** Session 93 wrote a plan to delete
  HamlibHandler and all related code. The plan listed the "obviously named"
  files but missed 10+ files with scattered references — because it never
  ran `grep -ri hamlib` across the codebase. Session 95 (the executor) had
  to discover all of them independently. Every missed file would have been
  found by 2 grep commands during the planning session.
  ```
- **Impact:** Canonical's Evidence-Based Inventory rule is already strong. Adding a concrete example ("2 grep commands would have found 10+ missed files") makes the cost of skipping it vivid.
- **Recommendation:** Add a short anecdote at the end of canonical's Planning Sessions section (after "an assumption, not an inventory"). Generalize the rad-con specifics — replace "HamlibHandler" with "a class scheduled for deletion" and drop session numbers.

### Finding #6 — [UNIVERSAL] Add Learnings #1, #2, #3, #5 to canonical Learnings table

- **Severity:** Minor (each is generic professional wisdom; upstream value is moderate).
- **Location:** rad-con lines 297–301.
- **Evidence:**
  | rad-con # | Content (abbreviated) | Universal? | Notes |
  |---|---|---|---|
  | 1 | Plans should flag "here be dragons" areas | Yes | Generic planning discipline |
  | 2 | High-quality plans collapse multi-session work — speed not evidence of quality | Yes | Important corrective — a fast plan is not necessarily a good plan |
  | 3 | Code review is a distinct deliverable, not overhead | Yes | Maps to canonical's "Review [code/PR]" task mapping |
  | 4 | Handoff evaluation is not optional | **Already canonical** | Redundant with Phase 3A |
  | 5 | A plan written from file-read memory = Verification Level 1 | Yes | Reinforces FM #11 (Gaps from memory) |
  | 6 | Protocol discipline is perishable | Yes — **see Finding #4** | |
  | 7 | Planning sessions need evidence-based discipline | Partial — **see Finding #5** | Overlaps with FM #19 and Evidence-Based Inventory |
  | 8 | Plan-mode output is a draft | **Already canonical** | This IS canonical Learning #1 |
- **Recommendation:** Add rad-con Learnings #1, #2, #3, #5 to canonical's Learnings table (as #3, #4, #5, #6 — #2 is Protocol Perishability per Finding #4). Skip #4 (redundant) and #8 (already there). Strip all "Session N" citations.

### Finding #7 — [NOISE / BUG — do not upstream, do not fix rad-con in this session] rad-con Degradation Detection table has incorrect "Session N" references

- **Severity:** Minor (rad-con internal bug; does not affect canonical).
- **Location:** rad-con lines 275–281.
- **Evidence:**
  ```
  | Handoff is <5 lines | Session 15 (minimal handoff) is active | ...
  | No handoff evaluation of predecessor | Session 10 (skip evaluation) is active | ...
  ```
  These should read "Failure mode #15" / "Failure mode #10" — "Session 15" makes no sense in context (Session 15 is not in the learnings table, and the referent is clearly FM #15). Canonical's equivalent table (lines 252–264) correctly says "Failure mode #N (…) is active" throughout.
- **Impact:** Confuses rad-con's own readers. No impact on canonical.
- **Recommendation:** **Do not address in this session or the v2.3 PR.** Out of scope (the issue forbids touching rad-con). The next time rad-con syncs from canonical in committed mode — or explicitly, via a separate rad-con-internal fix session — this will self-correct. Noted here for completeness and to prevent the v2.3 PR from accidentally copying the bug into canonical.

### Finding #8 — [ALREADY CANONICAL — do not upstream]

- **Scope:** The Task-in-prompt bypass explanatory text (rad-con line 33 "Steps 1-3 are READS, not skims. Session 63 skipped..."), the Plan-mode-bypass Learning (rad-con #8 = canonical Learning #1), and the 6 Minimum Handoff Requirements table.
- **Status:** All already in canonical. rad-con's versions add session citations (Sessions 63, 98, 62) which canonical chose not to include. No action required.

### Finding #9 — [PROJECT-SPECIFIC — do not upstream]

Exclusion list (for the v2.3 PR author):

1. **Task-mapping rows** referencing `docs/internal/PROFILE_DESIGN_PROMPT.md` and `docs/internal/AUDIT_PROMPT_TEMPLATE.md` (rad-con lines 48, 54). These are rad-con's internal adoption of the methodology.
2. **"Profile design" launch prompt template** (rad-con line 313). Rad-con has profile design as a distinct workstream; canonical does not.
3. **"Build [feature]" task mapping row** (rad-con line 57). Ambiguous-by-design for rad-con; canonical's existing rows already cover this via the free-form fallback.
4. **All `Session N` citations embedded in FMs, Learnings, and Phase 3 steps.** Canonical made the deliberate choice in v1.0 to generalize these (the FM rationale stands without the session number), and v2.2 kept that convention. Preserve it.
5. **The entire "Session Learnings" section (rad-con lines 329–838, 509 lines).** 100% rad-con-specific case studies, tied to specific commits, packages, components. Do not upstream any of it.

### Finding #10 — [STRUCTURAL — no upstream needed] rad-con's Learnings structure uses `SESSION_RUNNER learnings table` vs canonical's "workstream document and/or the Learnings table below"

- **Location:** rad-con line 167 vs canonical line 159.
- **Status:** Canonical's phrasing is a superset (includes both the workstream doc and the runner's Learnings table as targets). No change needed.

---

## 4. Items Audited

| Item | Status | Findings |
|------|--------|----------|
| rad-con Phase 0 | Pass (no substantive divergence) | — |
| rad-con Phase 1 task mapping | Mixed | #9 (exclusions for internal doc rows) |
| rad-con Phase 1B framing | Universal addition | #3 |
| rad-con Phase 2 Planning Sessions | Partial upstream candidate | #5 |
| rad-con Phase 3A evaluation | Already canonical | #8 |
| rad-con Phase 3D minimum requirements | Already canonical | #8 |
| rad-con Phase 3E Runtime Smoke Test | **High-value universal** | #1 (structural addition) |
| rad-con FM #20 (Build-passes-ship-it) | **High-value universal** | #2 |
| rad-con FMs #21–24 | Already canonical (as #20–23) | — |
| rad-con Degradation Detection table | Has a rad-con-internal bug | #7 (do not upstream) |
| rad-con Learnings table (8 entries) | 4 universal, 1 partial, 2 redundant, 1 already canonical | #4, #6 |
| rad-con Launch Prompt Templates | Project-specific deltas only | #9 |
| rad-con Session Learnings section (509 lines) | Entirely project-specific | #9 |

Coverage: all 837 rad-con lines examined; 297 canonical lines cross-referenced.

---

## 5. Structural Observations

1. **The compounding mechanism worked inside rad-con but not between rad-con and canonical.** rad-con's 837 lines embody ~90 sessions of learning; canonical's 297 lines have received one Learning since v1.0. The gap is exactly the "distribution disconnect" v2.2 was designed to close going forward. The audit exists because prior to v2.2 there was no `bin/sync` to pull rad-con's discoveries back into canonical.

2. **The most valuable upstream is a phase, not a paragraph.** Finding #1 (Phase 3E Runtime Smoke Test) is the single largest content gap between rad-con and canonical — and it's structurally load-bearing, not incidental. rad-con invented it *because* the project ships runtime integrations (plugins, WebSocket handlers). Canonical needs it because many adopting projects will too.

3. **FM numbering is a minor but real migration concern.** rad-con and canonical agree on FMs 1–19 but diverge at #20. An eventual v2.3 that adds "Build-passes-ship-it" as FM #24 will leave rad-con on a different numbering until rad-con itself re-syncs. Adopters who reference FMs by number (see `CLAUDE.md` or memory entries citing "FM #17") need canonical numbering to remain stable — appending is safer than inserting.

4. **rad-con's session citations are rhetorical, not structural.** They give the reader a story ("Session 63 scored 1/10 after skipping steps 1 and 3") but cost generality. Canonical has intentionally stripped them and should continue to — the rule stands without the anecdote. Findings #3, #4, #5, #6 all recommend stripping specifics when upstreaming.

5. **The "Session Learnings" 509-line section is a red herring for this audit.** Its volume is intimidating but none of it is upstreamable. It's rad-con's workstream journal, not methodology content. The real upstream value is concentrated in ~50 lines total (the 6 Findings above).

---

## 6. Recommendations for a v2.3 Content Release

Ordered by value × confidence:

| Priority | Change | File | Lines | Risk |
|---|---|---|---|---|
| 1 | Add Phase 3E Runtime Smoke Test (renumber 3E→3F, 3F→3G) | `starter-kit/SESSION_RUNNER.md` | +15 canonical lines | Low. Phase number bump affects memories that cite "Phase 3E Commit" — search for such citations before merging. |
| 2 | Add FM #24 "Build-passes-ship-it" + matching Degradation Detection row | `starter-kit/SESSION_RUNNER.md` | +3 canonical lines | Low. Append-only at end of FM table; no renumbering. |
| 3 | Add Learnings #2 (Protocol Perishability) from Finding #4 | `starter-kit/SESSION_RUNNER.md` Learnings table | +1 row | Trivial. |
| 4 | Add Learnings #3, #4, #5, #6 (rad-con #1, #2, #3, #5 abstracted) | `starter-kit/SESSION_RUNNER.md` Learnings table | +4 rows | Trivial. |
| 5 | Add "structural control" framing line to Phase 1B | `starter-kit/SESSION_RUNNER.md` | +1 line | Trivial. |
| 6 | Add grep-inventory "2 commands would have found 10 files" anecdote to Planning Sessions section | `starter-kit/SESSION_RUNNER.md` | +2 lines | Trivial. |

**Non-recommendations** (things the v2.3 PR should NOT do):

- Do NOT copy session numbers. All upstreamed content must be generalized.
- Do NOT renumber existing canonical FMs (1–23). Append new FM as #24.
- Do NOT add any of the rad-con "Session Learnings" case studies.
- Do NOT add PROFILE_DESIGN or AUDIT_PROMPT_TEMPLATE task mapping rows.
- Do NOT touch rad-con's runner in the v2.3 PR. rad-con will receive the upgrades the next time it runs `bin/sync` (after its own re-integration session decides how to merge its 509-line learnings against a newly-upgraded canonical).
- Do NOT copy rad-con's Degradation Detection "Session 15 (…)" phrasing — that is a bug in rad-con (Finding #7).

**Scope of the v2.3 content release:** ~25 lines of canonical net-new + 1 structural phase rename. Everything else is deferred to later audits (`ftx1-hamlib` has its own runner that should be audited separately when the user requests).

---

## 7. Verification Trail

- **rad-con file read in full:** `/Users/terrell/Documents/code/rad-con/SESSION_RUNNER.md` (837 lines, two reads — lines 1–300 and 300–838).
- **Canonical file read in full:** `/Users/terrell/Documents/code/methodology/starter-kit/SESSION_RUNNER.md` (297 lines).
- **Workstream read in full:** `/Users/terrell/Documents/code/methodology/workstreams/AUDIT_WORKSTREAM.md` (231 lines).
- **Issue body re-confirmed:** `gh issue view 6 --repo KJ5HST/methodology`.
- **Metric claim from issue body (837 / 297 / 594 / 54 / 31 hunks):** line counts verified via `wc -l`; line-delta claims not independently recomputed (trust the issue's original field-test numbers).
- **FM numbering cross-check:** manual walk of rad-con FMs 1–24 (lines 241–265) against canonical FMs 1–23 (lines 220–242). FMs 1–19 identical; rad-con inserts new FM at slot 20; canonical FMs 20–23 appear at rad-con slots 21–24.

---

## 8. What's Next (for the Executor of This Audit)

This document IS the audit deliverable. The next step is **a separate session** that:

1. Opens a branch like `v2.3-content-release`.
2. Edits `starter-kit/SESSION_RUNNER.md` per the 6 recommendations in §6.
3. Runs `bin/tests.sh` (should pass — these are doc-only changes but the sync tests validate file presence).
4. Updates `README.md` "What's New in v2.3" with a one-paragraph summary citing this audit doc.
5. Bumps methodology version to v2.3 in `CLAUDE.md`.
6. Commits, tags `v2.3`, creates GitHub release.
7. **Does NOT sync to rad-con.** rad-con is excluded (issue body, "Non-goals").
8. Self-assessment should explicitly evaluate: did the PR strip all session numbers? Did it renumber any existing FM? (Both should be "no" per §6.)

**Do NOT bundle this audit with the v2.3 content PR.** Session boundary rule (FM #18 Planning-to-implementation bleed): the audit is the plan; the content PR is the implementation. Two sessions, not one.
