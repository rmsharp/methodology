# Operational Backlog (fork-only)

> **STATUS: 1 open item (BL-5), reopened 2026-07-07.** BL-1 – BL-4 are complete (the operational
> rollout that originally justified this file); it was marked RETIRED on 2026-07-06 and reopened
> when a new item surfaced. The verbose BL-1 – BL-4 task bodies were removed on 2026-07-06; git
> history preserves them (commits `b091fba` … `69dad12`).

Operational/coordination backlog for **rmsharp's** methodology work. Fork-only — it lives in
`docs/planning/` and is **not** part of the canonical framework or any upstream PR (same convention
as [`adopter-pr25-27-remediation-plan.md`](adopter-pr25-27-remediation-plan.md)).

This is a backlog, **not** GitHub issues, by operator decision.

## Open items

### BL-5 — Dashboard: adapt scoring to document-only repositories

**Problem.** `tools/methodology_dashboard.py` (and its `starter-kit/` twin) scores every repo on a
code-centric rubric, so it penalizes **document-only** repositories for having no code. Affected
populations: research-documentation projects (per `RESEARCH_DOCUMENTATION_WORKSTREAM.md` — papers,
dissertations, technical reports, regulatory analyses) and the methodology framework's own doc corpus.
Concretely, a doc-only repo:

- scores **0/20 on Testing** (`test_to_source_ratio` = 0, `test_file_count` = 0) and draws a **HIGH
  "No test infrastructure"** risk — a false penalty; there is nothing to unit-test.
- can draw a **"No CI/CD"** risk even when a docs-render / link-check pipeline is the real equivalent.
- has an unstable `doc_to_source_ratio` when `source_loc` ≈ 0.

**Desired.** Detect a doc-only / research repo (e.g. `source_loc` below a threshold, or an explicit
opt-in marker) and **conditionally re-shape scoring** — reweight or exempt the Testing dimension,
substitute a **render/verification** dimension (leverages the v2.5 render-dependency discipline and
the Research-Documentation workstream's verification checklist), and suppress the code-centric risks.
Advisory tool → no hard gate; the goal is fair scoring, not a new gate. Apply to **both byte-identical
twins**; bump `DASHBOARD_VERSION`.

**Related polish (from the S5 / Component C review, low priority, fold in if cheap):**
- Signal F's advisory RISK line is not adopter-scoped, so it can fire on a non-adopter sibling repo
  that keeps a `BACKLOG.md` with `- [x]` history plus a `CHANGELOG.md`. Same "adapt to repo type"
  class; consider gating it (or the freshness signals generally) on methodology adoption.
- `.gitignore` covers `tools/__pycache__/` and `bin/__pycache__/` but **not** `starter-kit/__pycache__/`,
  which the dashboard module now produces when imported/tested. Add the missing rule.

## Completed items (BL-1 – BL-4)

| Item | Scope | Outcome |
|------|-------|---------|
| **BL-1** | wsfct → v2.9 (supersede #520) | ✅ Complete in `rmsharp/wsfct` (operator). Legacy PR #520 closed. |
| **BL-2** | mts #1 — adopt PR #25/#27, refresh → v2.9 | ✅ Complete in `rmsharp/mts` (operator). |
| **BL-3** | airqino #1 — remediation + full re-vendor → v2.9 | ✅ Complete in `rmsharp/airqinodashboard` (operator). |
| **BL-4** | Housekeeping: methodology repo | ✅ DONE 2026-07-06 — plans archived to `docs/planning/`, 3 stale branches pruned, fork/upstream/tags in sync. |

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
