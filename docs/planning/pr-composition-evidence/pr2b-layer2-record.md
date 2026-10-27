# PR2b layer 2: the layout resolver, the fixture trees and the literal scanner on `upstream/main` (S378, 2026-10-27)

**Status: BUILT and verified, local, un-pushed, nothing sent to `KJ5HST/methodology`.** This is the second checkpoint of PR2b
(`../upstream-pr-composition-plan.md` section 5, the PR2b row; layer 1 is `pr2b-layer1-record.md`). Every figure is printed by a script here or by a
command named beside it; the saved output is `pr2b-layer2-verify-output.txt`. What I read from files and what a command measured are labelled.

## 1. The answer first

1. **The layer exists.** Branch `pr2b/candidate` (a local ref with no upstream, so a bare `git push` cannot send it) now has two commits on `upstream/main`
   `d50ce290`: layer 1 `fbcef390` (unchanged, an ancestor) and layer 2 `41a1e580` (tree `86571e72`): **7 files, +1,225 / -2**, built in a scratch
   `--no-local` clone and fetched here. `pr2/candidate` (`3cba1e50`) is kept as it was.
2. **It applied with no conflict**, as the sizing record predicted (`pr2b-sizing-record.md`): `git cherry-pick -x 14ef9597` onto `fbcef390`, no marker, no
   file edited by hand. The prediction is now a fact for this commit.
3. **One thing differs from the candidate's commit: its message.** It said the scanner "reads 158 sites over 9 files of the tree as it stands"; on this
   tree the scanner reads **159 over 9** (section 3), so the message says 159. Tree before and after the amend: `86571e72`. The `-x` trailer was dropped.
4. **It is green in a clean clone** (section 4): the quality ratchet **13/13 pass, 0 fail, 0 unmeasured**, every measured value equal to its floor
   (272 and 74 are exact); the shell suite run directly: **272 passed, 0 failed, 0 skipped**.
5. **No region needed his judgment**, and no gate floor needed re-deriving upward: the floors the commit declares are the numbers measured here.

## 2. What it carries

| File | Change | Why it is in the layer |
|---|---|---|
| `tools/layout_resolver.py` | new, 76 lines | the resolver: which layout does a project keep, from one anchor file, by a four-row table; one marked block of standard-library code the later layers embed byte for byte (this layer embeds it nowhere) |
| `tools/layout_fixtures.py` | new, 88 lines | scratch trees in both layouts, and the tier-1, half-migrated and empty shapes, built from the manifest |
| `bin/check-layout-literals` | new, 299 lines | lists every line of a shipped tool that names a methodology file by a root path; not a gate yet |
| `tools/test_layout_resolver.py` | new, 702 lines | 74 tests for the three above |
| `bin/_manifest.py` | +43 / -1 | `NEW_LAYOUT`, the target layout as a table of literals beside `DISTRIBUTION`; only the fixtures and their test read it |
| `bin/tests.sh` | +8 | wires the new unit tests in as one assertion |
| `.quality-gates.json` | +9 / -1 | a new `layout-unit-tests` gate (74) and `tests-sh-passed` 271 to 272 |

All seven are Theme A of plan section 4 ("Carried"); none is in its "Not carried" column. **By reading, not by a script** (as in layer 1): section 4 lists
themes, not files, so there is nothing for a script to compare against.

## 3. The scanner on this tree (the to-do list, not a failure)

`python3 -I bin/check-layout-literals` reads **159 sites (102 path, 57 text) over 9 files**, exit 1; `layer-verify.sh` prints the same line. By file:
`.githooks/pre-commit` 21, `bin/check-handoff` 6, `bin/check-ledger` 4, `bin/check-links` 1, `bin/status` 3, `starter-kit/context_budget.py` 8,
`starter-kit/methodology_dashboard.py` 79, `starter-kit/methodology_trim.py` 21, `starter-kit/quality_ratchet.py` 16 (sum 159).

**Measured against the candidate's own tree** (a clone checked out at `14ef9597`, same scanner): 158 sites (102 path, 56 text), the same 9 files, the same counts
in eight of them; `starter-kit/methodology_trim.py` is 20 there and 21 here. The cause is the trimmer: this branch carries upstream's 1.8.2, the candidate's
tree 1.7.0, and one more text site comes with the newer file. The plan's criterion (0 sites) belongs to the last layer that resolves a tool; a count above 0
here is the to-do list the layers that follow work down, and `layer-verify.sh`'s header says so.

## 4. The checks of the PR2 row, and which of them apply here

Clean `--no-local` clone, serial, `layer-verify.sh`; the verified commit was `41a1e580` (message already amended, so the commit verified is the commit kept).

| Check (plan section 5, PR2 row) | Result |
|---|---|
| `quality_ratchet.py --run` (`pr2b-layer2-verify-output.txt`) | **13/13 pass, 0 fail, 0 unmeasured**; results `0c5f3696f6d3`, manifest `75d87bc42f8b`. Measured against floors: `tests-sh-passed` 272/272, `dashboard-unit-tests` 354/354, `context-budget-unit-tests` 148/148, `trimmer-unit-tests` 227/227, `ratchet-unit-tests` 45/45, `layout-unit-tests` 74/74 |
| `bash bin/tests.sh` run directly (Part 3 of `pr2b-layer2-verify-output.txt`, complete) | **272 passed, 0 failed, 0 skipped**. Test 9 (the `--source=github` row) needs the network and passed, so the network was reachable on this run (the test's own header says it is skipped when the repository is unreachable; I did not run it offline) |
| every shipped `.verify.sh` exit histogram equal to upstream's | one tracked proof (`docs/archive/CHANGELOG-through-2026-09-30.md.verify.sh`): exit 0 on the layer; exit 0 on the layer-1 base (`pr2b-layer1-record.md` section 4) |
| `bin/check-layout-literals` | applicable now: **159 sites, a to-do list** (section 3); the row's 0 is for the last tool-resolving layer |
| `bin/check-links --layout both` | **not applicable at this layer**: the flag arrives with the sync layer (commit 9) |
| the changed-file list equal to section 4 | by reading (section 2) |
| PR2b row: `conflicts-after-merge` reads 0 | `git merge-tree --write-tree upstream/main <layer 2 tip>` exits 0; `upstream/main` is an ancestor; the branch is 2 commits ahead |
| the read-set budget (`context_budget.py --status`) | nothing over budget, exit 0 |

No threshold was loosened: the one new gate and the one raised floor are exactly what the layer adds.

## 5. What this does not show

1. **The surface** is this machine: clean clones, serial runs, hooks **not armed** (`layer-verify.sh` unsets `core.hooksPath`), so the ratchet's pre-commit
   refusal was not exercised on this commit. It cannot show Windows, the maintainer's machine or upstream's CI (there is none).
2. **The resolver is embedded nowhere yet.** The commit's own message says "the lists of tools that embed the block start empty, so two of its loops compare
   nothing until the next layer fills them": green here is green for the resolver, the fixtures and the scanner on scratch trees, not for any tool using them.
3. **Fork-internal references ride along.** 22 of the layer's 1,225 added lines name a backlog id, a session number, a plan or decision label or "he overruled"
   (`bin/_manifest.py` 3, `bin/check-layout-literals` 5, `tools/layout_fixtures.py` 3, `tools/layout_resolver.py` 2, `tools/test_layout_resolver.py` 9, `.quality-gates.json` and `bin/tests.sh` 0; counted over the added lines of `git show HEAD -U0` by this regex, which is rough and was typed
   inline, not saved as a script: `BL-\d+|\bS\d{3}\b|\bthe fork\b|[Ll]earning #\d+|plan C\d+|\(plan |decision D\d+|phase P\d+|\bP[1-9]\b.*phase|overruled|\bhe\b (?:overruled|decided)`). The plan puts the scrub in its own commit later in the series (the candidate's commit 26), so the layer carries
   them and this is not a defect here; the count is the size of that scrub for these files.
4. **PR3's table and PR4's text** are not re-run (the plan's PR2b row says they are, after all layers).
5. **The gate floors will move again.** They are exact for this layer; every later layer re-derives them (tighten only).

## 6. Next

The next layers, from the sizing record's order, are **commits 3 and 4** (the ledger hook and the ratchet find the files under `methodology/`; the ratchet 1.5.0,
`fd965939` and `c8c0b213`), which apply with no conflict by the sizing and are the "gate layer", then 5 by reading (the layout hunks of the trimmer, the only new
judgment). One layer per session, a claim first. Re-run this layer: fetch `pr2b/candidate` into a scratch `--no-local` clone and run
`docs/planning/pr-composition-evidence/layer-verify.sh <clone> <commit>`; allow about 20 minutes.
