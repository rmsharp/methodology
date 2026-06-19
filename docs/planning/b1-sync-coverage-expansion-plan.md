# B1 — Expand `bin/sync` / `bin/status` Distribution Coverage

**Status:** PLAN (deliverable of a planning session). Not yet ratified; not implemented.
**Date:** 2026-06-19
**Author:** methodology session (canonical-repo dogfooding)
**Governing discipline:** `starter-kit/SESSION_RUNNER.md` §Planning Sessions (evidence-based inventory mandatory — this is a move/rename/migration plan) + `workstreams/ARCHITECTURE_WORKSTREAM.md` for structure.
**Fork-only doc** per the established branching pattern: planning docs live on `origin/main`; the B1 *execution* branches come clean from `upstream/main` for the upstream PR.
**Relationship to other work:** Independent of the four awaiting-merge PRs (#28–#31, issues #15/#16/#17/#19). This is a candidate **v2.8** change — the first non-docs change in many releases.

---

## 1. Problem statement

`bin/sync` and `bin/status` propagate only **three files**:

```python
# bin/sync:15  AND  bin/status:15  (duplicated, not shared)
SYNC_FILES = ("SESSION_RUNNER.md", "SAFEGUARDS.md", "methodology_dashboard.py")
```

Both scripts read each name from `starter-kit/<name>` (`sync:45-46`) and write it to the project **root** (`sync:152`) — there is no notion of a destination subdirectory. Nearly every release since v2.5 also changed files *outside* that set (RECOMMENDED_SKILLS, CONTEXT_TEMPLATE, ITERATIVE_METHODOLOGY, workstreams). Adopters who update "by the book" with `bin/sync` silently fall behind on framework docs, while `bin/status` reports `current` because it only inspects the same three files (`status:15-17`, `status:147-149`). **False confidence — the failure this fix targets.**

The gap is already visible *in the project's own docs*: the README documents two install paths that disagree about scope.

| Path | What it distributes | Source |
|------|--------------------|--------|
| **Option A (scripted, `bin/sync`)** | 3 files → project root | `README.md:64-72` |
| **Option B (manual)** | `SESSION_RUNNER`, `SAFEGUARDS`, `SESSION_NOTES`, `CHANGELOG`, `ROADMAP` → **root**; `ITERATIVE_METHODOLOGY`, `HOW_TO_USE`, `workstreams/` → **`docs/methodology/`** | `README.md:74-76` |

`HOW_TO_USE.md:820` ("place `SESSION_RUNNER.md` at the project root") and `HOW_TO_USE.md:832` ("put the framework in `docs/methodology/`") confirm Option B as the canonical adopter layout. **B1's baseline goal: make the scripted path reach (at least) Option-B completeness, and add the two files that have no documented adopter home at all.**

---

## 2. Evidence-based inventory (grep, run 2026-06-19)

### 2.1 The distributable corpus

`starter-kit/` (10 files): `SESSION_RUNNER.md`, `SAFEGUARDS.md`, `SESSION_NOTES.md`, `CHANGELOG.md`, `ROADMAP.md`, `BOOTSTRAP.md`, `CLAUDE_TEMPLATE.md`, `CONTEXT_TEMPLATE.md`, `RECOMMENDED_SKILLS.md`, `methodology_dashboard.py`.
Framework docs (root): `ITERATIVE_METHODOLOGY.md`, `HOW_TO_USE.md` (+ the canonical repo's own `README.md`, `CLAUDE.md` — **not** distributable).
`workstreams/` (9 files): 5 workstreams + 2 campaigns + `TEMPLATE_WORKSTREAM.md` + `TEMPLATE_CAMPAIGN.md`.

### 2.2 Affected symbols (what the executor will touch)

| Symbol / token | Where | Note |
|---|---|---|
| `SYNC_FILES` | `bin/sync:15`, `bin/sync:16`, `bin/sync:128-136`, `bin/sync:195`, `bin/sync:225`; `bin/status:15`, `:16`, `:130-132`, `:147` | flat tuple, **duplicated** in both scripts |
| `IGNORE_ENTRIES` | `bin/sync:16,114`; `bin/status:16,34` | derived from `SYNC_FILES`; assumes root-relative `/name` |
| `COLUMNS` | `bin/status:17`, `:103` | 3 fixed table columns |
| `read_local` / `sync_file` | `bin/sync:45-46`, `:151-161` | hard-codes `starter-kit/<name>` → `project/<name>` (root only) |
| `.gitignore` entry format | `bin/sync:16`, `:114-125` | `/SESSION_RUNNER.md` style — breaks for files in subdirs |
| 9 smoke tests | `bin/tests.sh:25-29,44-46,71-88,107-114` | filenames hard-coded throughout |

### 2.3 Cross-reference edges to the two homeless files (the link-debt)

Today **no script copies `RECOMMENDED_SKILLS.md` or `CONTEXT_TEMPLATE.md` anywhere**, yet distributed files link to them. Every edge below is a *dangling link in adopters today*:

| # | Source file (adopter location) | → Target | Current path in source | Lines |
|---|---|---|---|---|
| 1 | `SESSION_RUNNER.md` (root) | RECOMMENDED_SKILLS | `RECOMMENDED_SKILLS.md` (sibling) | 57, 247, 255 |
| 2 | `CONTEXT_TEMPLATE.md` | RECOMMENDED_SKILLS | `RECOMMENDED_SKILLS.md` (sibling) | 74 |
| 3 | `RECOMMENDED_SKILLS.md` | CONTEXT_TEMPLATE | `CONTEXT_TEMPLATE.md` (sibling) | 29 |
| 4 | `RECOMMENDED_SKILLS.md` | ITERATIVE_METHODOLOGY | `../ITERATIVE_METHODOLOGY.md` | 29 |
| 5 | `ITERATIVE_METHODOLOGY.md` (`docs/methodology/`) | RECOMMENDED_SKILLS | `starter-kit/RECOMMENDED_SKILLS.md` | 180, 210, 288, 333, 377 |
| 6 | `ITERATIVE_METHODOLOGY.md` (`docs/methodology/`) | CONTEXT_TEMPLATE | `starter-kit/CONTEXT_TEMPLATE.md` | 180 |
| 7 | `workstreams/DEVELOPMENT_WORKSTREAM.md` | RECOMMENDED_SKILLS | `../starter-kit/RECOMMENDED_SKILLS.md` | 60 |
| 8 | `workstreams/AUDIT_WORKSTREAM.md` | RECOMMENDED_SKILLS | `../starter-kit/RECOMMENDED_SKILLS.md` | 24 |
| 9 | `workstreams/ARCHITECTURE_WORKSTREAM.md` | RECOMMENDED_SKILLS | `../starter-kit/RECOMMENDED_SKILLS.md` | 189 |

### 2.4 Latent bug found in passing

`SESSION_RUNNER.md:62` links `[…](../docs/methodology/ITERATIVE_METHODOLOGY.md#multi-session-campaigns)`. From an adopter's **project root** (where SESSION_RUNNER lives), `../docs/methodology/` points **above** the project. Every other framework reference in the file (`:50-56`) correctly uses `docs/methodology/…`. **Fix `:62` to `docs/methodology/…` as part of B1.** (Confirmed sole occurrence by grep.)

---

## 3. The taxonomy (core design work)

B1 is not "sync everything." Each distributable file falls into exactly one class:

### TRACKED — sync keeps current; drift-safe; overwrites toward canonical
The existing drift/force/upgrade machinery (`sync:139-148`, `sync:205-222`) applies unchanged.

| File | Adopter dest |
|---|---|
| `SESSION_RUNNER.md` | root |
| `SAFEGUARDS.md` | root |
| `methodology_dashboard.py` | root |
| `RECOMMENDED_SKILLS.md` | **TBD — Decision 1** |
| `CONTEXT_TEMPLATE.md` (the *template*, see below) | **TBD — Decision 1** |
| `ITERATIVE_METHODOLOGY.md` | `docs/methodology/` |
| `HOW_TO_USE.md` | `docs/methodology/` |
| `workstreams/*` (all 9) | `docs/methodology/workstreams/` |

### SEED-ONCE — copied at bootstrap, then owned by the adopter; sync must NEVER clobber
The clean discriminator is **filename**: the template and its instance have *different names*, so SYNC simply never lists the instance as a destination.

| Template (TRACKED, may be synced) | Instance (adopter-owned, NEVER a sync dest) |
|---|---|
| `CLAUDE_TEMPLATE.md` | `CLAUDE.md` |
| `CONTEXT_TEMPLATE.md` | `CONTEXT.md` |
| — | `SESSION_NOTES.md` *(working log — adopter writes every session)* |
| — | `CHANGELOG.md` *(adopter's own history)* |
| — | `ROADMAP.md` *(adopter's own plans)* |
| — | `BACKLOG.md` *(adopter-created, never shipped)* |

> **Decision 2 (recommended): track the *template*, never the *instance*.** Sync may copy `CONTEXT_TEMPLATE.md` / `CLAUDE_TEMPLATE.md` so template improvements (e.g. v2.7.2's CONTEXT_TEMPLATE change) propagate, but it must never write `CONTEXT.md` / `CLAUDE.md` / `SESSION_NOTES.md` / `CHANGELOG.md` / `ROADMAP.md`. Because dest filenames differ from instance filenames, this needs **no special-case guard** — it falls out of the mapping. The only guard needed: do not add the instance filenames to the mapping.

> **Open sub-question (Decision 2a):** `SESSION_NOTES.md`, `CHANGELOG.md`, `ROADMAP.md` are *seed* templates today (Option B copies them to root). If they stay SEED-ONCE, the scripted path should copy them **only when absent** (create-if-missing, never overwrite) — distinct behavior from TRACKED. Recommend: a third sync disposition `seed` = write only if the dest does not exist.

### NOT-DISTRIBUTED — canonical repo's own; never copied
`README.md`, `CLAUDE.md` (this repo's), `tools/methodology_dashboard.py` (the *portfolio* scanner — distinct from the per-project `starter-kit/` copy), `bin/*`, `docs/`.

---

## 4. ⚠ Here be dragons: the link-topology paradox (the long pole)

This is the load-bearing finding and the reason B1 is design-heavy, not Python-heavy. **The memory's Decision 1 ("root, zero rewrites") under-counted it.**

The canonical repo and the adopter use **different directory layouts**:

```
CANONICAL REPO                          ADOPTER PROJECT (Option B)
/                                       project-root/
  ITERATIVE_METHODOLOGY.md                SESSION_RUNNER.md, SAFEGUARDS.md, …
  HOW_TO_USE.md                           docs/methodology/
  starter-kit/  (SR, SAFEGUARDS, RS,        ITERATIVE_METHODOLOGY.md
                CT, dashboard, …)           HOW_TO_USE.md
  workstreams/                              workstreams/
```

A relative markdown link is only verbatim-correct in **both** layouts when the target's position *relative to the source* is identical in both. That holds **only for files that are siblings in both layouts.** It fails for every edge that crosses the `starter-kit/`↔framework boundary, because that boundary's depth differs (canonical: `ITER` at root, `RS` at `starter-kit/` → `starter-kit/RS`; adopter: `ITER` at `docs/methodology/`, `RS` at root → `../../RS`). **No single relative path satisfies both.**

**Established convention (already in the repo):** `SESSION_RUNNER.md` authors its forward references for the **adopter layout** (`:50-56` use `docs/methodology/…`), accepting that they are dead inside the canonical repo. B1 should extend this convention consistently: **distributed files' cross-references target the adopter layout and are validated there**, not in-repo.

Consequence: the edges in §2.3 #5–#9 (ITER/workstreams → starter-kit files) currently use *canonical-layout* paths and are **already dead in adopters today**. Fixing them to adopter-correct paths is a strict improvement for adopters, at the cost of making them dead inside the canonical repo (exactly as SESSION_RUNNER already is).

### 4.1 Rewrite cost per placement (Decision 1, quantified)

Counting the §2.3 edges, with the "sibling-in-both-layouts ⇒ no change" rule:

| Placement of RS + CT | Edges needing rewrite | Files touched | SESSION_RUNNER touched? |
|---|---|---|---|
| **Adopter root** *(recommended)* | #4 (1), #5 (5), #6 (1), #7–9 (3) = **~10 refs** | RS, ITER, 3 workstreams (**5 files**) | **No** (#1 sibling-in-both ✓; #2,#3 unchanged) |
| Adopter `docs/methodology/` | #1 (3), #4 (1), #5 (5), #6 (1), #7–9 (3) = **~13 refs** | SR, RS, ITER, 3 workstreams (**6 files**) | Yes (3 refs) |

**Recommendation — Decision 1: place `RECOMMENDED_SKILLS.md` and `CONTEXT_TEMPLATE.md` at adopter root.** Root wins on two independent grounds: (a) fewer rewrites across fewer files; (b) it leaves `SESSION_RUNNER.md` — the most-synced, most-sensitive, must-stay-byte-identical file — **untouched**, because SR↔RS and CT↔RS are siblings in *both* layouts. The only forced change to a root file is RS:29's `../ITERATIVE_METHODOLOGY.md` → `docs/methodology/ITERATIVE_METHODOLOGY.md`.

### 4.2 The bigger alternative (Decision 1b — surfaced, recommended *against* for now)

The paradox vanishes entirely if the **canonical repo restructures to mirror the adopter layout** (move `starter-kit/` root-files to repo root, framework to `docs/methodology/`). Then every distributed link resolves identically in-repo and in adopters, and cross-reference completeness (Learning #7) becomes checkable in-repo with no simulation. **But** this rewrites README paths, every `starter-kit/…` and `workstreams/…` reference, and the `bin/sync` source paths — a large structural change with its own blast radius. **Recommend: defer to a possible future campaign; do not bundle into B1.** B1 takes the smaller, established path (adopter-layout links + a simulation test, §Phase 2).

---

## 5. Decisions to ratify at plan-review

| # | Decision | Recommendation |
|---|---|---|
| 1 | Adopter home for `RECOMMENDED_SKILLS.md` + `CONTEXT_TEMPLATE.md` | **Root** (§4.1: fewer rewrites, SESSION_RUNNER untouched) |
| 1b | Resolve link paradox by moving links, or by restructuring the canonical repo to mirror the adopter layout | **Move links** (adopter-layout convention + simulation test); defer restructure |
| 2 | Templates vs instances | **Track templates, never instances** (§3); falls out of the mapping, no guard needed |
| 2a | `SESSION_NOTES`/`CHANGELOG`/`ROADMAP` disposition | New **`seed`** disposition = write-if-absent, never overwrite |
| 3 | `--source=github` incremental safety | **Defer + document.** History walk is unimplemented for github source (`sync:201`, `status:137`), so any changed file misclassifies as "locally modified" and blocks → `--force`. Keep **local source** the supported update path to keep B1 small. Document the limitation in `--help` / BOOTSTRAP. |
| 4 | `bin/status` output for ~15 files | Switch the 3 fixed columns (`status:17,103`) to **per-file rows** (`Project · File · Disposition · Status`) |
| 5 | Avoid `SYNC_FILES` duplication across the two scripts | Extract the mapping to a shared **`bin/_manifest.py`** imported by both — single source of truth (Ousterhout deepening). Adds a Phase 3→4 dependency. |

---

## 6. Phased execution plan

Sizing: **1 planning (this) + 3 implementation ≈ 4 sessions.** The long pole is Phase 2 (link reconciliation) — **docs work, not Python** (confirms the memory's "design is the long pole"). One session for all of B1 would be **FM #26** (mega-session masquerading as a vertical slice): the phases span *distinct capabilities* (link hygiene; sync coverage; status reporting), not one capability's layers.

> **Vertical-slice note (FM #26 / §Vertical Slice Sessions).** Phases 2 and 3 are *separate capabilities* and must not be bundled. **Within** a single phase (esp. Phase 3) the layers MAY be run as a pre-declared vertical slice if the implementing session re-declares the layer set in a plan-mode contract at Orient and checkpoint-commits at each layer boundary (≤5 files/commit). Default to horizontal if any gate (a)–(d) cannot be met.

### Phase 2 — Link reconciliation in canonical source *(1 session; docs + test)*
Ratify Decisions 1, 1b, 2a at session start (plan-mode contract). Then:
1. Rewrite §2.3 edges #4–#9 to adopter-layout-correct paths for the chosen home (Decision 1).
2. Fix the `SESSION_RUNNER.md:62` `../docs/methodology` bug.
3. Add a **link-resolution test** (`bin/check-links` or a new `tests.sh` block) that materializes a *simulated adopter tree* (copy each distributable to its planned dest) and asserts every relative markdown link in the distributed files resolves to an existing file.
- **DONE:** link checker green against the simulated adopter tree; §2.3 edges all resolve; `:62` fixed.
- **Verify:** `./bin/tests.sh` (new link block green); manual `grep -rn "starter-kit/\|\.\./" <distributed files>` shows no canonical-only paths remain in distributed files.
- **Dragon:** these rewrites make the same links dead *inside* the canonical repo (accepted convention, §4). Do **not** "fix" them back — that is the paradox reasserting itself.
- **Independently shippable:** fixes today's dangling links even before sync is expanded. STOP. Close out.

### Phase 3 — Expand `bin/sync` coverage *(1 session; candidate vertical slice)*
1. Replace the flat `SYNC_FILES` tuple with a mapping: list of `(src_relpath, dest_relpath, disposition)` spanning root + `docs/methodology/` + `docs/methodology/workstreams/`. (Decision 5: put it in `bin/_manifest.py`.)
2. Generalize `read_local`/`sync_file` to honor `dest_relpath` and `mkdir -p` parent dirs; keep `.py` chmod (`sync:158-160`).
3. Implement the `seed` disposition (write-if-absent; Decision 2a) and confirm instances are never destinations (Decision 2).
4. Fix `.gitignore` entry generation for subdir paths (`sync:114-125` assumes root `/name`).
5. Drift/force/dry-run/history logic is already per-file (`sync:139-148`) — verify it generalizes; no redesign.
6. Expand `bin/tests.sh` mechanically to the new tree; **faithful verification (gate d):** tests must assert against the *actual multi-dir output tree*, not just filenames.
7. Update `README.md:64-72` (Option A scope) + `BOOTSTRAP.md` to match.
- **DONE:** `bin/sync <tmp>` produces the full Option-B+ tree; `./bin/tests.sh` green; Phase 2's link checker green **against the sync-produced tree** (not just the simulated one).
- **Verify:** `./bin/tests.sh`; `bin/sync $(mktemp -d) --dry-run` lists every mapped file at its dest; re-run sync is idempotent.
- **Dragon:** SEED-ONCE clobber — a regression here overwrites an adopter's `SESSION_NOTES.md`/`CONTEXT.md`. Add an explicit test that a pre-existing instance file is **never** modified. STOP. Close out.

### Phase 4 — Expand `bin/status` to per-file rows *(1 session)*
1. Import the shared manifest (Decision 5); drop the local `SYNC_FILES`/`COLUMNS`.
2. Replace `render_table` 5-column layout (`status:102-113`) with per-file rows; show disposition so `seed`/`tracked` differ visibly.
3. `file_status` (`status:88-99`) already returns the right states; reuse.
- **DONE:** `bin/status <project>` reports per-file drift for the full set; `seed` files absent ≠ flagged as drift.
- **Verify:** `./bin/tests.sh` (status block expanded); `bin/status` on a freshly-synced tree shows all `current`; on a partially-stale tree shows the stale file only.
- STOP. Close out.

---

## 7. Tracking issue & out of scope

- **Tracking issue:** none exists upstream (verified all states, memory note). **File a B1-scoped issue on `KJ5HST/methodology` before/with the upstream PR** for `Closes #N`.
- **Out of scope for B1:** github-source incremental history walk (Decision 3 = defer); canonical-repo restructure (Decision 1b = defer); behavioral-overlay skills, dashboard adoption metrics, any principle/phase/gate/workstream change.

---

## 8. Planning-session checklist (self-verification)

- [x] Plan written with file paths + line numbers (§2, §6)
- [x] Grep-based inventory completed for all affected symbols (§2.2, §2.3) — searches actually run, not from memory
- [x] Each phase has explicit DONE criteria + verification commands + a STOP (§6)
- [x] "Here be dragons" flagged (Learning #3): link-topology paradox (§4), SEED-ONCE clobber (Phase 3), github-source incremental (Decision 3)
- [x] Decisions surfaced with recommendations for operator ratification (§5)
