# Using `read-set-budgets` in your projects before PR #80 merges — the routes, each run

**Status: S161's deliverable (2026-09-11), fork-only.** It answers the request carried as item (1)
of S160's receipt — *"clarify the upstream merge options"* — which the operator scoped at S161's
Phase 0 to one question: **how to use the `read-set-budgets` content in your own projects before
[PR #80](https://github.com/KJ5HST/methodology/pull/80) merges.** Two other strands were offered and
not chosen: what the maintainer's merge method does to this fork, and what could be sent upstream.
Nothing here is outward-facing, and **no real project was written to** — every sync ran against
scratch copies (§3).

**Measured 2026-09-11** against `upstream/read-set-budgets` = `598c459` (PR #80's head), fork `main`
= `18957077`, `upstream/main` = `512c2ed`, and the 12 projects under `~/Development` that carry a
`SESSION_RUNNER.md`. The numbers describe that tree and those projects on that day; re-run §8 before
acting on them (Learning #61). **Declared budget: 20,000 B.**

## 0. The answer

**Nothing is waiting on the maintainer.** Syncing from a local checkout works today; only the GitHub
route waits for the merge. There are two local sources, and they leave a project in different places:

| Route | Source | Syncs cleanly today | When #80 merges unchanged |
|---|---|---:|---|
| **A** | a full clone of the branch (`598c459`) | **3 of 12** | those 3 are already **current** against upstream |
| **B** | this fork's `main` | **8 of 12** | 5 files per project read **locally modified** against upstream; an upstream sync refuses until `--force`, which rolls them back |
| **C** | GitHub (`--source=github`, or *"Update methodology using …"*) | **0** — exits 1 | refuses **all 12** projects as they stand today |

Your 12 projects fall into three groups (§3 has each one):

- **Clean on both routes — a real choice** (`airqino`, `church_growth`, `dalia_martinez_funeral`).
  **Route A** gives exactly what #80 ships and needs nothing when it merges. **Route B** adds the
  fork's later work (§1) but ties the project to the fork. Default to A unless you want that work
  there now — and note that moving from A to B later trips a `bin/sync` defect (§5.1).
- **Already on the fork's lineage** (`chat_verification`, `claude_work`, `mts-system`,
  `vscode_quarto_ext`, `wsfct`). **Route B** — what you already do. Route A refuses them, and
  forcing it would move each dashboard from the fork's 2.13–2.15 line to upstream's 2.10.7.
- **Blocked on every route by a genuine local edit** (`feedback-loop-comparison`,
  `model_project_constructor` and its copy under `mpc_tests/`, `nprcgenekeepr`). One modified file
  refuses the whole sync (`bin/sync:291-307`), so nothing updates until each edit is moved or
  deliberately dropped (§5.6).

## 1. What a project gets

The point of `read-set-budgets` is that Phase 0's mandatory pair — `SESSION_RUNNER.md` +
`SAFEGUARDS.md` — fits in one agent read again. Measured today with PR #80's own method (concatenate,
double, read, halve the refused count); the branch row reproduces the body's recorded 47,805 → 23,902
exactly, which validated the method before it was applied to fork `main`:

| Source | Pair bytes | Tokens | Of the 25,000-token read cap |
|---|---:|---:|---:|
| `upstream/main`, v3.7 (PR #80's body; not re-measured) | 80,526 | 28,234 | 112.9% — refused |
| the branch, `598c459` | 67,581 | **23,902** | 95.6% — 1,098 spare |
| fork `main`, `18957077` | 69,749 | **24,598** | 98.4% — 402 spare |

Both local routes also install three files v3.7 lacks — `FRAMEWORK_LEARNINGS.md`,
`docs/methodology/FRAMEWORK_APPARATUS.md`, `methodology_trim.py` (`TRIM_VERSION` 1.5.0 on both).
What Route B adds on top, in 5 of the 27 distributed files: 62 learning rows instead of 46; dashboard
2.17.0 instead of 2.10.7; issue #75's plan-phase *surface* rule in `SESSION_RUNNER.md`; the agent
update rules in `BOOTSTRAP.md`; one line of `HOW_TO_USE.md`. **Seeds are never overwritten by any
route** (`SESSION_NOTES.md`, `CHANGELOG.md`, `HANDOFFS.md`, `ROADMAP.md`, `.context-budget.json`).
The per-file table is PR #80's body, [`read-set-budgets-to-main-pr-body.md`](read-set-budgets-to-main-pr-body.md) §2.

## 2. Why the routes differ — how `bin/sync` decides

Line numbers are fork `main`'s `bin/sync`; the branch's copy differs only in its GitHub error path.

- **`--source=local` copies from the checkout the script sits in** (`bin/sync:25-27`), reading its
  **working tree** (`:52`) — whichever branch that checkout has out, uncommitted edits included.
- **A file that differs is "upgradable" only if its exact bytes appear in that checkout's history**
  (`:206`), gathered with `git log -- <path>` (`:60`). Otherwise it is "modified", and one modified
  tracked file refuses the entire sync, exit 2, unless `--force` (`:291-307`).
- **`--source=github` reads `KJ5HST/methodology`'s default branch** (`:17`, `:93`); there is no ref
  option (`:245`); and it uses an **empty history** (`:283`), so every tracked file not byte-identical
  to upstream counts as modified. `bin/status` has the same gap (`bin/status:165`).
- **The branch's `bin/sync` stops at the first missing GitHub file and says `hint: run gh auth
  login`** — a 404 misdiagnosed as authentication. Fork `main`'s lists all three missing files
  instead. Both run the same classification code over the same 27-row manifest (22 tracked, 5 seed).
- **The two `bin/status` runs disagree about stale seeds**: the branch's manifest keys seed format
  on each seed's title, fork `main`'s on its *Size, and when to archive* heading.

## 3. Your projects, dry-run

**Surface.** Each project was copied into the session scratchpad as exactly what `bin/sync` and
`bin/status` read in commit mode — `.gitignore` plus whichever of the 27 destination paths exist. All
12 are commit mode (none lists a tracked destination in `.gitignore`), so the copies are faithful for
these two tools; no session in any project was run. Route A ran from a fresh GitHub clone of the
branch, Route B from a `--no-local` clone of fork `main`.

| Project | Route A now | Route B now | Notes |
|---|---|---|---|
| `airqino` | clean — 18 written, 2 seeded | clean — same | on `chore/methodology-pr2527-remediation` |
| `chat_verification` | refuses 5 † | clean — 9 written | |
| `church_growth` | clean — 13 written, 1 seeded | clean — same | |
| `claude_work` | refuses 1 † (dashboard) | clean — 13 written, 1 seeded | see §5.5 |
| `dalia_martinez_funeral` | clean — 14 written, 1 seeded | clean — same | |
| `feedback-loop-comparison` | refuses 2 ‡ | refuses 2 ‡ | |
| `model_project_constructor` | refuses 2 ‡ | refuses 2 ‡ | |
| `mpc_tests/model_project_constructor` | refuses 2 ‡ | refuses 2 ‡ | a second checkout; its runner differs slightly |
| `mts-system` | refuses 5 † | clean — 10 written, 1 seeded | |
| `nprcgenekeepr` | refuses 5 † | refuses 1 ‡ (`methodology_trim.py`) | |
| `vscode_quarto_ext` | refuses 6 † | clean — 8 written | |
| `wsfct` | refuses 5 † | clean — 8 written | on `chore/s628-migration-264-deploy-bundle` |

**†** A version that exists only in the fork's history, so the branch has never seen it:
`SESSION_RUNNER.md`, `FRAMEWORK_LEARNINGS.md`, `BOOTSTRAP.md`, `methodology_dashboard.py`,
`methodology_trim.py` (`vscode_quarto_ext` adds `context_budget.py`). Forcing Route A here is **mixed**:
learnings rise (18–37 rows → 46) and the trimmer rises (1.1.1–1.3.0 → 1.5.0), but the dashboard moves
from the fork's 2.13–2.15 line to 2.10.7 — the line S150's merge plan judged the fork's a superset of
([`upstream-read-set-budgets-merge-plan.md`](upstream-read-set-budgets-merge-plan.md) §2.2 row 16) —
`wsfct` and `vscode_quarto_ext` lose the surface rule, and five lose `BOOTSTRAP.md`'s update rules.
**‡** A genuine local edit, in no published version on either side (§5.6).

Every refusal above was checked against the source checkout's **full** history (`--full-history`):
none is in it, so none of these twelve outcomes is the §5.1 defect. The real runs on the copies wrote
exactly what the dry runs predicted.

## 4. When #80 merges — simulated

The stand-in for upstream after the merge is `upstream/main` with `598c459` merged `--no-ff`; its tree
is **byte-identical to `598c459`** (empty diff), so it is what #80 ships if it merges unchanged. Each
route was applied for real to fresh copies, then checked from that stand-in:

- **After Route A,** the three it synced are **fully current**: every tracked file `current` in
  `bin/status`, and both a local and a GitHub sync report 22 unchanged, exit 0.
- **After Route B,** every project it synced has **the same 5 files `locally modified`** —
  `SESSION_RUNNER.md`, `FRAMEWORK_LEARNINGS.md`, `BOOTSTRAP.md`, `methodology_dashboard.py`,
  `docs/methodology/HOW_TO_USE.md` — so a sync from upstream, local or GitHub, **refuses with exit 2**.
  Three ways on: keep syncing from the fork; `--force` once (a rollback: 62 → 46 learning rows,
  dashboard 2.17.0 → 2.10.7, the surface rule and the update rules removed); or wait until upstream
  carries those 5 files.
- **The GitHub route refuses all 12 projects as they stand today** — 7 to 13 tracked files each —
  because it never consults history (§2). **After #80 merges, update from a local clone of upstream,
  not `--source=github`.**

**Merge method.** Only a merge commit was simulated. Route A's *current* result does not depend on it:
`bin/sync` compares bytes with the source before it looks at any history (`:204`), and a squash or a
rebase of an unchanged PR produces the same files. If #80 **changes** before it merges **and** is
squashed or rebased, `598c459`'s versions would be in no upstream history, and a Route A project would
read *modified* for each changed file. That case is derived from the code, not run.

## 5. Hazards found

1. **`bin/sync` walks history without `--full-history`, so it cannot see the side of a merge whose
   content was not kept.** Fork `main` kept its own content when it merged the branch (`213f841`), so
   for `SESSION_RUNNER.md` its walk visits 46 commits and never reaches the branch's version
   (`c0550acd`); with `--full-history` it visits 77 and finds it. **Measured consequence:** a project
   synced by Route A and then by Route B is refused on 4 files — `SESSION_RUNNER.md`, `BOOTSTRAP.md`,
   `methodology_dashboard.py`, `HOW_TO_USE.md` — for all three Route-A-clean projects, and all 4 are
   in fork `main`'s full history. `--force` is then safe, since nothing unique is lost, but the tool
   cannot say so. The fix is `--full-history` at `bin/sync:60` and `bin/status:56`; neither file is
   distributed, and neither was changed here.
2. **The branch's GitHub error names the wrong cause** (§2). Fork `main`'s `bin/sync` has the fix;
   the branch does not.
3. **A shallow clone breaks upgrade detection** — with no history, every older file reads modified
   ([`BOOTSTRAP.md`](../../starter-kit/BOOTSTRAP.md):86). Clone in full.
4. **The source is a working tree.** Sync from a checkout with no uncommitted edits to distributed
   files, on the branch you mean.
5. **Project state.** `claude_work` holds all 22 of its methodology files **untracked** — never
   committed — on a detached `HEAD` with 16 entries in `git status`; a sync there records nothing. `airqino`
   and `wsfct` are on feature branches, and a sync writes into whatever is checked out. No project has
   an uncommitted methodology file other than `claude_work`.
6. **The genuine local edits**, each against its closest of every published version:
   - `feedback-loop-comparison`: `SESSION_RUNNER.md` is the 2026-04-16 version (`274dcd4a`) plus 3
     later lines, and `RESEARCH_DOCUMENTATION_WORKSTREAM.md` the 2026-04-25 version (`b1ba27ee`)
     minus its 9-line *Phases Covered* section — partial hand-updates, not customizations.
   - `model_project_constructor` (and its `mpc_tests/` copy): `SESSION_RUNNER.md` is the 2026-04-04
     version (`3d648abc`) with +23/−8 lines, including a step 5 that runs *"the shared methodology
     dashboard (external to this repo…)"* — a real customization; `SAFEGUARDS.md` is the same base
     with one later upstream line pasted in.
   - `nprcgenekeepr`: `methodology_trim.py` is the 2026-08-10 version (`c43e7eec`) plus **49 added
     lines**, among them `_session_notes_date` — a local extension. `--force` discards it, and a
     `CLAUDE.md` Adaptations section cannot hold code, so this one needs a decision of its own.

   The documented remedy for prose customizations is to move them into `CLAUDE.md`'s *Project-Specific
   Methodology Adaptations* section, then sync with `--force`
   ([`BOOTSTRAP.md`](../../starter-kit/BOOTSTRAP.md):75).

## 6. Commands

**Route A**, from a full clone (not `--depth`) kept beside the fork:

```sh
git clone --branch read-set-budgets https://github.com/KJ5HST/methodology.git ~/Development/methodology-read-set-budgets
M=~/Development/methodology-read-set-budgets
P=~/Development/<project>
"$M/bin/status" "$P"                          # behind / modified / missing, per file
"$M/bin/sync" "$P" --source=local --dry-run   # exit 2 = refused, and nothing is written
"$M/bin/sync" "$P" --source=local             # then review and commit inside the project
```

**Route B**, with this checkout on `main`: the same last three commands with
`M=~/Development/methodology`.

**After #80 merges:** `git -C "$M" switch main && git -C "$M" pull`, then the same commands. Prefer
this to `--source=github` (§4).

## 7. What this does not establish

- **No real project was touched, and no session ran in one.** The copies hold only what the two tools
  read.
- **The post-merge GitHub result is simulated.** It ran the stand-in's own `bin/sync` with only the
  network read replaced by the stand-in's bytes (§8); authentication, rate limits and the live API
  were not exercised. The live GitHub route was run once per checkout, today, against `airqino`: exit
  1 from both.
- **It assumes #80 merges unchanged** and that `upstream/main` has not moved from `512c2ed`.
- **Only a merge commit was simulated** (§4).
- **Seed format lag** — `bin/status`'s *present (stale format)* — is out of scope; no route changes
  a seed.

## 8. Reproduce

Copy each project's `.gitignore` and existing destination paths (`bin/_manifest.py`) into a scratch
directory, then run §6's commands against the copy. The post-merge GitHub rows used this harness,
which runs the checkout's real `bin/sync` and replaces only the network read:

```python
import sys, importlib.machinery, importlib.util, pathlib
P = pathlib.Path(sys.argv[1]); project = sys.argv[2]        # P: the post-merge checkout
loader = importlib.machinery.SourceFileLoader("sync_mod", str(P / "bin" / "sync"))
spec = importlib.util.spec_from_loader("sync_mod", loader)
m = importlib.util.module_from_spec(spec); loader.exec_module(m)
m.read_github = lambda src: (P / src).read_bytes()
m.methodology_version = lambda root, source: "github:<simulated post-merge main>"
sys.argv = ["sync", project, "--source=github", "--dry-run"]
sys.exit(m.main())
```

The post-merge stand-in: `git clone https://github.com/KJ5HST/methodology.git X`, then in `X`
`git fetch origin read-set-budgets && git merge --no-ff FETCH_HEAD`, then confirm
`git diff --stat 598c459 HEAD` is empty.

## 9. What this builds on

- **S123's adjudication** first measured the GitHub route's empty history: five adopters refused on
  7–8 files each ([`port-branch-identity-adjudication.md`](port-branch-identity-adjudication.md) §2.3,
  `136fb34`). This document reproduces it for 12 projects (7–13).
- **PR #76's body** already advised *"Use `--source=local` from a checkout of the branch"*
  ([`pr1-read-set-budgets-body.md`](pr1-read-set-budgets-body.md):60) — Route A.
- **S150's merge plan** chose fork `main`'s own content for these files when merging the branch
  ([`upstream-read-set-budgets-merge-plan.md`](upstream-read-set-budgets-merge-plan.md) §2.2), which is
  the cause of both Route B's post-merge refusals and hazard 5.1.
