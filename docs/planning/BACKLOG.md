# Operational Backlog (fork-only)

Operational/coordination backlog for **rmsharp's** methodology work. Fork-only — it lives in
`docs/planning/` and is **not** part of the canonical framework or any upstream PR (same
convention as [`adopter-pr25-27-remediation-plan.md`](adopter-pr25-27-remediation-plan.md)).

This is a backlog, **not** GitHub issues, by operator decision.

## Conventions

- **"Update to v2.9"** — all three adopter PRs below were authored **2026-06-12 against canonical
  v2.7**. Canonical has since moved **v2.7 → v2.7.1 → v2.7.2 → v2.8 → v2.9**, so each PR's
  synced/vendored content is ~2 minor versions stale and must be refreshed to **v2.9** before it
  merges. The v2.8 jump matters most: it expanded `bin/sync`/`bin/status` from the legacy 3-file
  scope to the full corpus via `bin/_manifest.py` (issue #32), so any vendored copy carrying the
  old tooling is the thing to refresh.
- **Merge only when the target repo is between sessions.** Every adopter PR rewrites live
  operating files (`SESSION_RUNNER.md`, and `CLAUDE.md`/`SAFEGUARDS.md`/`SESSION_NOTES.md`).
  Landing one mid-session would change the operating procedure under an active session. Wait for
  a quiet window in *that* repo.
- **One repo = one session.** Each adopter remains its own session/deliverable (per the
  remediation plan's execution model). Housekeeping is its own session too.

## Items

### BL-1 — wsfct #520: reconcile sync drift → merge
- **Repo / PR:** `rmsharp/wsfct` #520 — *reconcile sync drift — customizations to CLAUDE.md, synced files to canonical*
- **What it does:** resyncs `SESSION_RUNNER.md` (+45/−45) and `SAFEGUARDS.md` (+65/−61) back to
  canonical; moves project customizations into `CLAUDE.md` (+70/−1); adds the missing
  `methodology_dashboard.py` (+1614). (+1794/−107, 4 files.)
- **State (2026-06-22):** OPEN, `mergeable=UNKNOWN` — GitHub needs to recompute; after 10 days +
  intervening merges in wsfct, expect a conflict check. wsfct is the one adopter with `bin/sync`,
  so its drift-guard is in play.
- **Tasks:**
  1. Resolve conflicts / get a clean recompute.
  2. Refresh synced files + dashboard to **v2.9** (incl. v2.8 full-corpus `bin/sync`/`bin/status`).
  3. Merge — only when wsfct is between sessions.

### BL-2 — mts #1: adopt PR #25/#27 → merge
- **Repo / PR:** `rmsharp/mts` #1 — *adopt PR #25/#27 — migrate learnings, restore canonical runner, slim CLAUDE.md 908→360*
- **What it does:** slims `CLAUDE.md` (+27/−575), adds `PROJECT_LEARNINGS.md` overflow valve
  (+25), restores canonical `SESSION_RUNNER.md` (+12/−19); rest is additive new project docs.
  (+1038/−607, 21 files.)
- **State (2026-06-22):** OPEN, `MERGEABLE` but `UNSTABLE` — a CI check is failing/pending;
  investigate before merge.
- **Tasks:**
  1. Investigate the unstable CI check.
  2. Refresh the restored runner + wording to **v2.9**.
  3. Merge — only when mts is between sessions.

### BL-3 — airqino #1: remediation + full re-vendor → merge
- **Repo / PR:** `rmsharp/airqinodashboard` #1 — *PR #25/#27 remediation — receptacle + learnings (PART 1), full re-vendor v2.1→v2.7 (PART 2)*
- **What it does:** PART 1 — root receptacle + learnings (`CLAUDE.md`, `SAFEGUARDS.md`,
  `SESSION_NOTES.md`, `SESSION_RUNNER.md`). PART 2 — full re-vendor of the entire framework under
  `docs/methodology/`. (+9582/−92, 37 files.)
- **State (2026-06-22):** OPEN, `MERGEABLE` + `CLEAN` — mergeable today, **but the re-vendor is
  v2.7-era**, so it would land an already-stale copy — notably the *old* pre-v2.8 `bin/sync`.
- **Tasks:**
  1. Re-do the full re-vendor against the **v2.9** corpus (this is the bulk of the work — the
     v2.7→v2.9 delta includes the entire v2.8 `bin/_manifest.py` sync expansion).
  2. Merge — only when airqino is between sessions.

### BL-4 — Housekeeping: methodology repo (its own session)
- **Repo:** `rmsharp/methodology` (this repo). Not an adopter task; not a GitHub issue.
- **Tasks:**
  1. Decide prune-vs-keep on the two stale **fork-only** local planning branches
     `docs/reasoning-tier-plan` and `docs/tutorial-series-plan` (both shipped in v2.9).
  2. Confirm fork / upstream / tags are fully in sync and v2.9 close-out is intact.
  3. Verify nothing else is stranded after the tutorial campaign + #41/#42 reconciles.
- **Run as its own dedicated session.**

## Not in this backlog (rollout context)

The PR #25/#27 remediation plan covered **5** adopters. The other two are out of scope here:
- **nprcgenekeepr** — the reference end-state (already clean); a local `chore/methodology-pr2527-wording`
  branch was noted unpushed pending its session. Track in that repo, not here.
- **model_project_constructor** — drift noted in the plan; PR status TBD. Confirm separately.
