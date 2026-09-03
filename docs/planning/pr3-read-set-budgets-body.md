# PR 3 body — the apparatus extraction (read-set budgets, 3 of 4)

**Status: SHIPPED — [PR #78](https://github.com/KJ5HST/methodology/pull/78) is OPEN against
`read-set-budgets`.** Pushed and opened by S143 (2026-09-02) on the operator's explicit go-ahead,
three commits as-is. Body as submitted is below.

- **Head:** `pr3/apparatus-extraction` = `2c30d0f`, on `origin`
- **Base:** `read-set-budgets` — advanced to `907a696` when [#77](https://github.com/KJ5HST/methodology/pull/77)
  merged at 2026-09-03T01:38:22Z. **`tree(907a696)` is identical to `tree(56997af)`**, the tree PR 3
  was built and measured on, so S142's verification carried over and no rebase was needed
  (`merge-tree` exit 0).
- **Server-verified on open:** OPEN, base `read-set-budgets`, head `rmsharp:pr3/apparatus-extraction`,
  **12 files +426/−348**, 3 commits, `MERGEABLE`. `upstream/main` untouched at `512c2ed`.

---

## Title

`Extract the flight manual's apparatus to FRAMEWORK_APPARATUS.md (read-set budgets, 3 of 4)`

## Body

The six contiguous apparatus sections of `ITERATIVE_METHODOLOGY.md` — Knowledge Accumulation System,
Honest Accounting Framework, Scope Validation System, Verification Hierarchy, Session Document
Template, Performance Tracking — move **verbatim** into a new distributed sibling
`FRAMEWORK_APPARATUS.md` → `docs/methodology/FRAMEWORK_APPARATUS.md`, `TRACKED`. The manual keeps a
*Reference Apparatus* stub naming all six and linking the file. **Nothing was deleted.**

`ITERATIVE_METHODOLOGY.md` **68,240 → 55,976 B (−12,264, −18.0%)**, landing **774 B under the
56,750 B one-read cap** it had been over. The sibling is **15,493 B**, read on demand. Manifest
**26 → 27**.

The apparatus is *reference, not theory*: you open it to fill in a session document, validate a scope
or score a claim — not to understand why the phases exist. That is the same split `SESSION_RUNNER.md`
made when its learnings became `FRAMEWORK_LEARNINGS.md` in PR #76.

### The extraction was the easy half; reachability was not

The move updated every place that *names* the six sections and, at first, no place that *invokes*
what is in them. Those sections used to be reached by **scrolling**, so no link-based proof can see
their loss — and `bin/check-links` strips the `#fragment` and validates existence only, so it stays
green either way.

Nine pointers were added where none existed; four more sites already pointed at these sections in
prose and were converted in place. `ITERATIVE_METHODOLOGY.md` now carries **14** references to the
sibling — **13 pointer sites plus the stub's own link** — and the stub enumerates all thirteen.

### The manual-copy path is documented, not just the tool path

`README.md`'s Option B and `starter-kit/BOOTSTRAP.md`'s Step 1 enumerate the framework files **by
hand**. Left alone they would have told an adopter to copy a `docs/methodology/` **missing the file
those 14 links point at** — an install broken in a way `bin/check-links` structurally cannot report,
because it builds its simulated tree from `bin/_manifest.py`, which was correct. Fixed at `README.md`
(both the Option A sentence and the Option B list), `starter-kit/BOOTSTRAP.md` (tree diagram, sync
sentence, manual-copy step) and `docs/tutorials/T1_setup.md`.

`CLAUDE.md` gains a Reference-apparatus row; `HOW_TO_USE.md`'s layer table gains a row and its
`ITERATIVE_METHODOLOGY.md` length is re-derived (**~880 → ~580 lines**, sibling ~330).

### Scanner

`docs/methodology/FRAMEWORK_APPARATUS.md` joins `FRAMEWORK_DISTINCTIVE_DOCS` in both
`methodology_dashboard.py` twins, so a synced project is still classified by a name only this
framework installs. Twins remain byte-identical.

### Verification

Measured in `git clone --no-local --single-branch`, with the fork's history unreachable — never a
worktree, which reports a far healthier suite than an upstream-like tree has.

| | base `56997af` | this branch |
|---|---|---|
| `bash bin/tests.sh` | **114 passed / 1 failed** | **114 passed / 1 failed** |
| `tools/test_methodology_dashboard.py` | — | **211 tests, exit 0** |
| `tools/test_methodology_trim.py` | — | **exit 0** |
| `check-links` / `check-learnings` / `check-handoff` | — | **0 / 0 / 0**, each read bare |

Diffed **row for row**: **113 shared labels, zero status flips.** The only two differing rows are
self-describing counters — `all 26 → 27 manifest files present` and `one row per manifest file
(26 == 26 → 27 == 27)` — both passing on both sides. The single failure is the same on both sides:
Test 9's `bin/sync --source=github`, pre-existing and already declared in PR #76; it reads `main`,
where this branch's newest manifest rows do not yet exist, and heals on merge.

**End to end, not only through the suite:** a real `bin/sync` into a scratch git repo lands
`docs/methodology/FRAMEWORK_APPARATUS.md`, and in that installed layout all **14** references resolve
with **7 distinct fragments and 0 unresolved**.

---

## What a reviewer should look at

1. **`ITERATIVE_METHODOLOGY.md`'s Reference Apparatus stub** — it is the one sentence an adopter would
   use to audit whether the extraction left anything unreachable. It enumerates all 13 pointer sites.
2. **`README.md` Option B and `BOOTSTRAP.md` Step 1** — the manual-install path no checker models.
3. **`bin/_manifest.py`** — one row, landing with its file.

## Two things this PR deliberately does not do

- **It does not carry `collect_trim_metrics()` or the `## What It Costs` README section.** Both exist
  in the downstream fork this was ported from, and `git` offered both (11,834 B and 14,429 B) as
  conflict resolutions because the originating commits edited text inside them. Neither belongs to
  this change and neither exists on this base.
- **It does not fix two pre-existing count defects it noticed.** Both dashboard twins (`:185`) and
  `docs/tutorials/T8_keeping_current.md:183` say **"25 distributed sources/files"** where the manifest
  holds **26** on the base and **27** here — wrong before this change and after it. Out of scope;
  worth a separate one-line PR.
