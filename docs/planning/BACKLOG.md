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
- **Mechanism = the documented update workflow, not PR-resurrection.** Bring an adopter current
  with `bin/status` → `bin/sync` from a canonical `methodology/` checkout (history-aware drift
  guard; `--source=local` preferred — it auto-updates version-behind files and blocks only on real
  customizations), or the agent prompt *"Update methodology using
  https://github.com/KJ5HST/methodology"* (README:58; BOOTSTRAP §"Without `bin/sync`"). This is
  exactly what v2.8's full-corpus `bin/sync` was built for. An adopter does **not** need to host
  `bin/sync` — it is pointed *at* the adopter from a checkout. Resolving conflicts on a stale
  2026-06-12 PR is the wrong default: supersede the stale PR with a fresh update, then close it.
  (Exception: a full-repo *mirror* adopter like airqino, BL-3, vendors more than the manifest
  distributes, so its extra mirror files are refreshed manually; `bin/sync` still covers its
  operating files.)
- **Merge only when the target repo is between sessions.** Every adopter PR rewrites live
  operating files (`SESSION_RUNNER.md`, and `CLAUDE.md`/`SAFEGUARDS.md`/`SESSION_NOTES.md`).
  Landing one mid-session would change the operating procedure under an active session. Wait for
  a quiet window in *that* repo.
- **One repo = one session.** Each adopter remains its own session/deliverable (per the
  remediation plan's execution model). Housekeeping is its own session too.

## Items

### BL-1 — wsfct: bring methodology current → v2.9 (supersede #520)
- **Repo:** `rmsharp/wsfct` (default branch **`master`**). Existing PR #520 (*reconcile sync drift —
  customizations to CLAUDE.md, synced files to canonical*) is the v2.7-era attempt at this; it was
  going to migrate wsfct's customizations into `CLAUDE.md` and resync the operating files.
- **State (verified 2026-06-22):** PR #520 is now **`CONFLICTING` / `DIRTY`** vs `master` (10 days of
  intervening RBAC/e2e merges) and v2.7-era. wsfct is **not** operationally sync-wired — **no root
  `bin/`**; the only `bin/sync` is inside the v2.7-era vendored `docs/methodology/` mirror (a
  reference copy, **pre-v2.8**, not wired). wsfct is **mid-heavy-development** (RBAC/e2e on `master`),
  so it is *not* between sessions. *(Corrects the prior "wsfct is the one adopter with `bin/sync`"
  note — that was wrong.)*
- **Tasks (use the documented update workflow — see Conventions):**
  1. From a canonical `methodology/` checkout: `bin/status <wsfct>` to read drift, then
     `bin/sync <wsfct>` (`--source=local` preferred). The drift-guard auto-updates version-behind
     files and **blocks** on wsfct's genuine customizations → relocate those to `CLAUDE.md`
     "Project-Specific Methodology Adaptations", then re-run. (Equivalent: the *"Update methodology
     using https://github.com/KJ5HST/methodology"* agent prompt.) Do **not** conflict-resolve #520.
  2. `bin/sync` covers the manifest corpus (root operating files +
     `docs/methodology/{ITERATIVE_METHODOLOGY,HOW_TO_USE,workstreams/}`). wsfct also carries an extra
     *full* mirror (README/LICENSE/`bin/`/`tools/`/audits under `docs/methodology/`) the manifest does
     not manage — refresh that manually only if you want the reference copy current (not operationally
     required).
  3. Open a fresh PR, **close #520**, and merge — only when wsfct is between sessions.

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
- **Repo / PR:** `rmsharp/airqinodashboard` #1 — *PR #25/#27 remediation — receptacle + learnings (PART 1), full re-vendor → v2.9 (PART 2)*
- **What it does:** PART 1 — root receptacle + learnings (`CLAUDE.md`, `SAFEGUARDS.md`,
  `SESSION_NOTES.md`, `SESSION_RUNNER.md`). PART 2 — full re-vendor of the entire framework under
  `docs/methodology/`. (+10102/−103, 40 files.)
- **State (2026-06-22):** OPEN, `MERGEABLE` + `CLEAN`. Re-vendor **refreshed to v2.9** this session
  (commits `28db357` mirror, `0c59e5e` root `SESSION_RUNNER.md`); PR title/body updated to v2.9.
  Only the merge remains — held pending an airqino between-sessions window.
- **Tasks:**
  1. ~~Re-do the full re-vendor against the **v2.9** corpus.~~ **✅ DONE 2026-06-22** — 30-file
     `docs/methodology/` mirror refreshed verbatim from canonical `upstream/main` (= v2.9 + #41/#42
     reconciles): 19 files refreshed + 2 new v2.8 bin files (`_manifest.py`, `check-links`);
     `bin/sync`/`bin/status` now manifest-driven. Also caught and fixed the root `SESSION_RUNNER.md`
     drift to restore the PR's root==vendored invariant (and a broken `../docs/methodology` →
     `docs/methodology` link). `SAFEGUARDS.md`/`methodology_dashboard.py` were unchanged v2.7→v2.9
     so already matched; the 4 unadopted root TRACKED files left absent (no adoption-surface
     expansion). Adversarial 4-lens verify: all faithful, 0 must-fix. Both commits pushed.
  2. Merge — only when airqino is between sessions. *(pending)*

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
