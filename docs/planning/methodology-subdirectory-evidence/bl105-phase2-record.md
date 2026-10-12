# BL-105 build phase 2 — the tool (S303, 2026-10-12)

Plan [`methodology-subdirectory-plan.md`](../methodology-subdirectory-plan.md) D10; backlog row BL-105 ([`BACKLOG.md`](../BACKLOG.md), [detail](../BACKLOG-DETAIL.md#bl-105)); the contract is the rehearsal record's section 7 ([`bl105-rehearsal-record.md`](bl105-rehearsal-record.md)). Written after the work; every figure was read from a command's output in this session.

## 1. The answer first

**Built, in `bin/migrate-layout` only (canonical-only; nothing distributed, no adopter's live tree touched, nothing upstream):** a **companion rule** (`PROJECT_LEARNINGS.md` moves with tier 2 and `all`, when git tracks it and the project has a runner in either layout); a **top-up**, which is the same plan run on a tree the tool calls migrated (the plan is the companion's move alone, one commit, one ledger entry headed *Layout top-up*; today's `nothing to migrate` is now the answer only when nothing is left); the two configs **read where the layout puts them** (F29); and **F30 as he decided it, list only**: every link in a live Markdown document to a file the run moves is listed in `live_links` (JSON: all of them; text: the first 25 and a count of the rest) and none is rewritten.

**Tests:** 39 new in `tools/test_migrate_layout.py`, written and seen failing first (27 of the first 35 red for the intended reasons, 8 pinning behavior that had to stay), **275 in the file** against 236. **Mutation:** 32 distinct mutants of the new code in a `--no-local` clone ([`mutate-bl105-phase2.py`](mutate-bl105-phase2.py), which refuses to run in the working tree it mutates); 31 killed on the first run, 1 survived (the ledger exclusion of the link list: the fixture moved every ledger, so the clause could not show) and was killed once a tier-1 test was added. **Real population:** the built tool applied in `--no-local` clones of the five adopters that track the file (section 3): all five apply, the tool's own before-and-after checks read no difference, and the two with a comparator (`nprcgenekeepr`, `mts-system`) come out **tree-equal to S302's simulation except the tool's ledger entry**.

## 2. What was built

| Where | What |
|---|---|
| `bin/migrate-layout` `COMPANIONS`, `plan_moves` | the rule: tier 2 or `all`, a runner in either layout, tracked by git; a copy under `methodology/` already is a `destination-exists` refusal; an untracked copy stays and is named |
| `is_top_up`, `logical_map`, `ledger_entry_text`, `commit_message` | a run whose every move is a companion: no generated names added to the map, its own ledger heading and commit subject (`move PROJECT_LEARNINGS.md under methodology/ (top-up, tier all, 1 file)`) |
| `config_location`, `plan_rewrites` | F29: the two configs are read under `methodology/` in a tree whose runner is there, at the root otherwise |
| `link_targets`, `resolve_link`, `live_links`, `render_text` | F30: inline, image and reference links outside a fence, resolved against the linking document; not listed: a ledger or shard (counted with the ledger's), a file the run moves unedited, a file the run rewrites |

**Not seen by the list, by design:** an HTML `href`, a link built in code, a link in a document that is not Markdown. **The moved file's own prose is not scanned** for the names of other moved files (as in the S302 simulation).

## 3. The five adopters (`bl105-phase2-runs.json`)

Clones under `~/.cache/s303-adopters`, `git clone --no-local`, pinned where S302 pinned. Never the live trees.

| Adopter (layout) | Result of `--apply` in the clone | Companion rename | Rewrites | Live links | Checks |
|---|---|---|---|---|---|
| `nprcgenekeepr` (new, tier all) | applied; **the live tree is refused `not-current`** (F7, F19: its `methodology_trim.py` carries a deliberate project edit); the clone took the canonical copy to get past it | 100% | `CLAUDE.md` 7 | 0 | no difference |
| `vscode_quarto_ext` (new, tier all) | applied | 100% | `CLAUDE.md` 6, `methodology/.context-budget.json` 1 | 0 | no difference |
| `model_project_constructor` (new, tier 1) | applied: `all` also takes its tier 2 (8 moves) | 100% | `CLAUDE.md` 27, both configs at the root 1 each | 5 in 3 files | no difference |
| `mts-system` (legacy) | applied after `bin/sync` in the clone: one commit, 41 renames | 100% | `CLAUDE.md` 27, `methodology/.context-budget.json` 6, `.quality-gates.json` 1 | 3 | no difference |
| `wsfct` (legacy) | applied after `bin/sync` in the clone: 44 renames | 100% | `.gitignore` 2, `CLAUDE.md` 48, both configs 5 and 1 | 10 in 3 files | no difference |

**Against the simulation of S302:** `nprcgenekeepr` `CLAUDE.md` 7 replacements, none elsewhere (the same); `git diff` of the tool's tree against the simulation's `npr-move`: the ledger entry (4 lines) and the trimmer I replaced to pass the check. `mts-system`: the tool's one commit against the simulation's two steps (`mts-mig`, `mts-move`): the ledger entry (2 lines), nothing else. `model_project_constructor`'s 4 companion links are the 4 of F30 (`BACKLOG.md:80`, `ledger-budgets-review.md:17,126,269`); the fifth is a link to `SESSION_NOTES.md`, which tier 2 takes too.

## 4. What this run found

**Nothing new broke.** Two things are worth the next session's reading: (1) **the top-up refuses at the real `nprcgenekeepr`**, as any run of the tool does while a TRACKED file reads `locally modified` (F7, F19); were the refusal skipped, the apply's own check would call the unchanged status a difference (exit 4: `check_differences` called on an unchanged 22-of-23 status returns `['status']`). What a top-up should do about a project's deliberate edit of a synced file is **his call** (record section 5). (2) A project at tier 1 (`model_project_constructor`) takes its tier 2 with the companion: the companion is tier 2's, so there is no companion-only run for it.

## 5. His calls this leaves

- **A top-up at a tree with a locally modified TRACKED file** (`nprcgenekeepr`): keep refusing (the project settles the edit first: sync would overwrite it without `--force`), or let a top-up proceed when every non-current row is a file it does not move. Not built either way.
- The tool **does not run a project's own tests, gates or package build**; the hand edits of F25, F26/F27, F28 stay phase 4's, each in the adopter's own commit before the move.

## 6. Not done, not run

Phase 3 (the distributed prose: `BOOTSTRAP.md:218,220,222,439`, `CLAUDE_TEMPLATE.md:83`, `bin/check-links:84`) and phase 4 (the adopters) are not started. Not run: the adopters' own test suites and declared gates against the tool's trees (S302 ran them against the simulation, whose trees these equal); the live trees; GitHub CI; a clone of `Philippians` or `dalia_martinez_funeral`, which carry no such file.
