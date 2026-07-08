# Operational Backlog (fork-only)

> **STATUS: 1 open item — BL-7 (consider: model-tiering as an elective feature) added 2026-07-08. BL-1 – BL-6 all complete.**
> BL-6's last two items closed today: item 2 (seed-format migration discoverability) shipped in
> [PR #51](https://github.com/KJ5HST/methodology/pull/51) (merge `48c253f`, no version event), and item 3
> (hook distribution) was **decided — keep `.githooks/pre-commit` canonical-only** (see the Completed
> table + `CHANGELOG.md`). Verbose task bodies are removed at close-out; git history preserves them
> (`b091fba` … `69dad12`; BL-5 `b2efd76` … the v3.2 merge; the BL-6 item-1/1a/1b/1c detail up to the
> `9a84b8e` fork-sync merge).

Operational/coordination backlog for **rmsharp's** methodology work. Fork-only — it lives in
`docs/planning/` and is **not** part of the canonical framework or any upstream PR (same convention
as [`adopter-pr25-27-remediation-plan.md`](adopter-pr25-27-remediation-plan.md)).

This is a backlog, **not** GitHub issues, by operator decision.

## Open items

### BL-7 — Model-tiering by task complexity as an elective methodology feature (consider)

**Question (operator, 2026-07-08):** matching *model* capability to task complexity — as demonstrated
live in the close-out-receipt slice (Sonnet 5 for spec-driven, test-graded phases; Opus 4.8 for
high-blast-radius doc surgery + reviewing all sub-agent output before commit) — is a valuable pattern
the operator had not seen before. Could it be codified as an **elective** feature of the methodology?

This is a **planning/design** consideration (not implementation). Points for that session to weigh:

- **Where it lands:** the recommendation layer, not a hard rule ("methodology recommends; does not
  reimplement"). Likely a new *elective* section extending §Matching Reasoning Effort to Stakes (v2.9)
  and the `RECOMMENDED_SKILLS.md` Reasoning Effort table — which today cover *reasoning tier* but not
  *model selection*.
- **Agent-independence:** "models" (Sonnet/Opus/…) are agent-specific brand tokens → frame the core as
  **capability tiers** (cheaper/faster vs most-capable), model names illustrative only — same convention
  the reasoning-effort table already uses.
- **The risk lens is already ours:** tier ∝ blast radius × irreversibility × compounding cost
  (Principle 3, Principle 9, §Matching Reasoning Effort to Stakes). Model-tiering is that same lens
  applied to model choice rather than effort setting.
- **The generalizable pattern:** the cheaper tier drafts *test-graded / spec-driven* work; the strongest
  tier does *un-test-catchable* doc-surgery-on-invariants **and reviews all cheaper-tier output before
  commit**. An objective gate (a test suite, a grep-reconciliation) is what makes delegating the
  mechanical phases safe; the review pass is where the capability difference pays off.
- **Elective & additive:** changes no phase, gate, principle, or FM; a project that ignores it operates
  the methodology unchanged. Interaction to check: the vertical-slice per-boundary review discipline.
- **Open sub-questions:** core (brand-neutral) text in `ITERATIVE_METHODOLOGY.md` + model specifics in
  `RECOMMENDED_SKILLS.md`? Does the hybrid orchestration warrant a worked tutorial example?

*Provenance: surfaced while executing the close-out-receipt slice's own hybrid model split (P2/P4 on
Sonnet 5, P3/P5 on Opus 4.8) — see `close-out-receipt-durable-artifact-plan.md` and `CHANGELOG.md`.*

## Completed items (BL-1 – BL-6)

| Item | Scope | Outcome |
|------|-------|---------|
| **BL-1** | wsfct → v2.9 (supersede #520) | ✅ Complete in `rmsharp/wsfct` (operator). Legacy PR #520 closed. |
| **BL-2** | mts #1 — adopt PR #25/#27, refresh → v2.9 | ✅ Complete in `rmsharp/mts` (operator). |
| **BL-3** | airqino #1 — remediation + full re-vendor → v2.9 | ✅ Complete in `rmsharp/airqinodashboard` (operator). |
| **BL-4** | Housekeeping: methodology repo | ✅ DONE 2026-07-06 — plans archived to `docs/planning/`, 3 stale branches pruned, fork/upstream/tags in sync. |
| **BL-5** | Dashboard: fair scoring for document-only / research repos | ✅ SHIPPED 2026-07-08 in **v3.2** ([PR #50](https://github.com/KJ5HST/methodology/pull/50), merge `9bda167`). `detect_doc_only` + Render/Verification proxy; code-centric risks suppressed; Large-files ext-filter; both polish items (Signal-F adopter-gate + `starter-kit/__pycache__` gitignore) done; `DASHBOARD_VERSION` 2.8.0; first functional scoring tests (29). |
| **BL-6** | v3.1 adopter-migration completeness (pedagogical + seed-format + hook distribution) | ✅ CLOSED 2026-07-08. **Item 1** (pedagogical refresh) + follow-ups **1a/1b/1c** shipped via [PR #47](https://github.com/KJ5HST/methodology/pull/47) / [#48](https://github.com/KJ5HST/methodology/pull/48) / [#49](https://github.com/KJ5HST/methodology/pull/49) (docs/tutorial lag; no version event). **Item 2** (seed-format migration discoverability) shipped via [PR #51](https://github.com/KJ5HST/methodology/pull/51) (merge `48c253f`, no version event) — `bin/status` flags a pre-v3.1-shaped seed `present (stale format)` with a migration note, advisory-only (generic `_manifest.SEED_FORMAT_MARKERS`; `sync` never auto-overwrites). **Item 3** (hook distribution) **DECIDED: keep `.githooks/pre-commit` canonical-only** — adopters run the Phase 3F ledger gate via their root `SESSION_RUNNER.md`, so distributing the hook would add a per-clone `core.hooksPath` enable step + a maintenance surface for a mechanism they already have; the hook exists only because *this* repo has no root runner. Not added to `bin/_manifest.py`. |

**Not in this backlog:** upstream **PR #44** (REUSE compliance + license/REUSE README badges) is being
handled directly with the maintainer (Terrell) and was never a backlog item.

## Historical context (for the record)

The backlog existed to bring three v2.7-era adopter PRs (all authored 2026-06-12) current to canonical
**v2.9** before merging, and to run one methodology-repo housekeeping session. Two conventions governed it:

- **Mechanism = the documented update workflow, not PR-resurrection.** Bring an adopter current with
  `bin/status` → `bin/sync` from a canonical `methodology/` checkout (`--source=local` preferred), or the
  *"Update methodology using https://github.com/KJ5HST/methodology"* agent prompt — then supersede the
  stale PR rather than conflict-resolving it. This is exactly what v2.8's full-corpus `bin/sync`
  (`bin/_manifest.py`, issue #32) was built for.
- **Merge only when the target repo is between sessions**, since each adopter PR rewrites live operating
  files (`SESSION_RUNNER.md`, `CLAUDE.md`, `SAFEGUARDS.md`, `SESSION_NOTES.md`). One repo = one session.

Two adopters from the original PR #25/#27 rollout were always out of this backlog's scope:
**nprcgenekeepr** (the clean reference end-state) and **model_project_constructor** (tracked separately).
