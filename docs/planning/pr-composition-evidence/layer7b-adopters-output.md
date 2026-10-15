# PR2, the last layer: the twelve adopters, the candidate's tree against the fork tip's (S322)

`migrate-12-adopters.py` (methodology-subdirectory-evidence/) run twice, one after the other, from a clean clone of each tree, over the twelve adopters' committed HEADs in `--no-local` clones, with `--out` and `--work` in a scratch directory. Sections 1 and 2 are the script's own `summary.md` (its first lines say what each run was); section 3 is the comparison; section 4 is one refusal read in full.

## 1. Run A: the candidate `ab35e96` (223 s)

Run A: `migrate-12-adopters.py` from a clean clone of the candidate `ab35e96`, 223 s, twelve adopters' committed HEADs in `--no-local` clones (S322).

| adopter | hooks | status before sync | sync | dry run | apply | exit | refusals | its hook refused the commit | shards kept (rehearsal) | moves | min rename | rewrites | left | not rewritten (mentions) | ledger entry | checks | proofs | history | check-links | clean | health before | health after | ratchet before | ratchet after | s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| model_project_constructor | armed: /Users/rmsharp/Development/model_project_constructor/.githooks | 23 tracked, 5 not current | committed with --force (5 files, ok) | ok | applied | 0 | none | - | no proofs to rehearse | 8 (8 tracked, 0 plain) | R97 | .context-budget.json 1, .quality-gates.json 1, CLAUDE.md 27 | 2 | ci 1, harness 0, hooks 0, ledger 814, other 2296 | methodology/CHANGELOG.md | ok | {} -> {} | 335 -> 336 | exit 1 -> exit 1 | yes | 96 | 96 | cite in the receipt: quality_ratchet: 0/0 pass · 0 fail · 0 unmeasured · results 4f53cda18c2b · manifest 4f53cda18c2b | cite in the receipt: quality_ratchet: 0/0 pass · 0 fail · 0 unmeasured · results 4f53cda18c2b · manifest 4f53cda18c2b | 20 |
| feedback-loop-comparison | none | 23 tracked, 5 not current | committed with --force (5 files, ok) | nothing-to-do | nothing-to-do | 0 | none | - | no proofs to rehearse | 0 (0 tracked, 0 plain) | - | none | 4 | - | no ledger | not run (nothing-to-do) | - | - | - | yes | 59 | not migrated | cite in the receipt: quality_ratchet: 0/0 pass · 0 fail · 0 unmeasured · results 4f53cda18c2b · manifest 4f53cda18c2b | not migrated | 5 |
| nprcgenekeepr | none | 23 tracked, 6 not current | committed with --force (6 files, ok) | ok | applied | 0 | none | - | no proofs to rehearse | 1 (1 tracked, 0 plain) | R100 | CLAUDE.md 7 | 3 | ci 5, harness 0, hooks 0, ledger 3388, other 322 | methodology/CHANGELOG.md | ok | {} -> {} | 1924 -> 1925 | exit 1 -> exit 1 | yes | 96 | 96 | cite in the receipt: quality_ratchet: 0/1 pass · 0 fail · 1 unmeasured · results bd4e76335429 · manifest aa983075d6a2 | cite in the receipt: quality_ratchet: 0/1 pass · 0 fail · 1 unmeasured · results bd4e76335429 · manifest aa983075d6a2 | 43 |
| mts-system | armed: .githooks | 23 tracked, 21 not current | committed with --force (22 files, ok) | ok | applied | 0 | none | - | 4 proof(s) run, kept in place: none | 41 (41 tracked, 0 plain) | R97 | .context-budget.json 6, .quality-gates.json 1, CLAUDE.md 27 | 0 | ci 0, harness 0, hooks 0, ledger 1837, other 2478 | methodology/CHANGELOG.md | ok | {"0": 4} -> {"0": 4} | 450 -> 451 | exit 0 -> exit 1 | yes | 92 | 92 | cite in the receipt: quality_ratchet: 0/0 pass · 0 fail · 0 unmeasured · results 4f53cda18c2b · manifest 4f53cda18c2b | cite in the receipt: quality_ratchet: 0/0 pass · 0 fail · 0 unmeasured · results 4f53cda18c2b · manifest 4f53cda18c2b | 17 |
| vscode_quarto_ext | none | 23 tracked, 2 not current | committed with --force (2 files, ok) | nothing-to-do | nothing-to-do | 0 | none | - | 1 proof(s) run, kept in place: docs/archive/SESSION_NOTES-through-S253.md | 0 (0 tracked, 0 plain) | - | none | 3 | - | no ledger | not run (nothing-to-do) | - | - | - | yes | 76 | not migrated | cite in the receipt: quality_ratchet: 0/2 pass · 2 fail · 0 unmeasured · results a5df9c4dde18 · manifest 334939914945 | not migrated | 28 |
| Philippians | none | 23 tracked, 21 not current | committed with --force (22 files, ok) | ok | applied | 0 | none | - | no proofs to rehearse | 32 (32 tracked, 0 plain) | R97 | .context-budget.json 3, .quality-gates.json 1, CLAUDE.md 16 | 0 | ci 0, harness 0, hooks 0, ledger 333, other 23 | methodology/CHANGELOG.md | ok | {} -> {} | 124 -> 125 | exit 0 -> exit 1 | yes | 51 | 51 | cite in the receipt: quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 2ef8d5a97abe · manifest 90d698a42ac4 | cite in the receipt: quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 2ef8d5a97abe · manifest 90d698a42ac4 | 8 |
| airqino | none | 23 tracked, 5 not current | committed with --force (5 files, ok) | nothing-to-do | nothing-to-do | 0 | none | - | no proofs to rehearse | 0 (0 tracked, 0 plain) | - | none | 19 | - | no ledger | not run (nothing-to-do) | - | - | - | yes | 68 | not migrated | cite in the receipt: quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 2993256f954d · manifest 0f1d28b61292 | not migrated | 7 |
| chat_verification | armed: .githooks | 23 tracked, 5 not current | committed with --force (5 files, its own hook refused (d. "Too small to log" is the failure mode, not an exception (the session runner's FM #27).); committed with --no-verify) | nothing-to-do | nothing-to-do | 0 | none | - | no proofs to rehearse | 0 (0 tracked, 0 plain) | - | none | 0 | - | no ledger | not run (nothing-to-do) | - | - | - | yes | 45 | not migrated | cite in the receipt: quality_ratchet: 0/0 pass · 0 fail · 0 unmeasured · results 4f53cda18c2b · manifest 4f53cda18c2b | not migrated | 5 |
| church_growth | armed: .githooks | 23 tracked, 5 not current | committed with --force (5 files, its own hook refused (d. "Too small to log" is the failure mode, not an exception (the session runner's FM #27).); committed with --no-verify) | nothing-to-do | nothing-to-do | 0 | none | - | no proofs to rehearse | 0 (0 tracked, 0 plain) | - | none | 1 | - | no ledger | not run (nothing-to-do) | - | - | - | yes | 49 | not migrated | cite in the receipt: quality_ratchet: 0/0 pass · 0 fail · 0 unmeasured · results 4f53cda18c2b · manifest 4f53cda18c2b | not migrated | 5 |
| dalia_martinez_funeral | none | 23 tracked, 22 not current | committed (25 files, ok) | ok | applied | 0 | none | - | no proofs to rehearse | 30 (30 tracked, 0 plain) | R97 | .context-budget.json 3, .quality-gates.json 1, CLAUDE.md 12 | 1 | ci 0, harness 0, hooks 0, ledger 104, other 110 | methodology/CHANGELOG.md | ok | {} -> {} | 19 -> 20 | exit 0 -> exit 0 | yes | 48 | 49 | cite in the receipt: quality_ratchet: 0/0 pass · 0 fail · 0 unmeasured · results 4f53cda18c2b · manifest 4f53cda18c2b | cite in the receipt: quality_ratchet: 0/0 pass · 0 fail · 0 unmeasured · results 4f53cda18c2b · manifest 4f53cda18c2b | 7 |
| claude_work | none | 23 tracked, 23 not current | committed (27 files, ok) | ok | rolled-back | 3 | none | - | no proofs to rehearse | 30 (30 tracked, 0 plain) | - | .context-budget.json 3, .quality-gates.json 1 | 0 | ci 0, harness 0, hooks 0, ledger 32, other 0 | methodology/CHANGELOG.md | not run (rolled-back) | - | - | - | - | no commits | not migrated | no commits | not migrated | 5 |
| wsfct | armed: /Users/rmsharp/Development/wsfct/.git/hooks | 23 tracked, 21 not current | committed with --force (22 files, ok) | ok | rolled back by its hook; applied with hooks off | 3 (hooks on) then 0 (hooks off) | none | git commit was refused: python3: can't open file '/private/tmp/claude-501/-Users-rmsharp-Development-methodology/61c2d328-63f6-439e-a95b-4c09ba34edb3/scratchpad/s322-adopters-A-work/wsfct/context_budg | 6 proof(s) run, kept in place: none | 44 (44 tracked, 0 plain) | R97 | .context-budget.json 5, .gitignore 2, .quality-gates.json 1, CLAUDE.md 48 | 11 | ci 2, harness 0, hooks 0, ledger 1910, other 3939 | methodology/CHANGELOG.md | ok | {"1": 6} -> {"1": 6} | 536 -> 537 | exit 0 -> exit 1 | yes | 94 | 94 | cite in the receipt: quality_ratchet: 0/0 pass · 0 fail · 0 unmeasured · results 4f53cda18c2b · manifest 4f53cda18c2b | cite in the receipt: quality_ratchet: 0/0 pass · 0 fail · 0 unmeasured · results 4f53cda18c2b · manifest 4f53cda18c2b | 67 |

## 2. Run B: the fork tip `91fdf8c` (270 s)

Run B: the same script from a clean clone of the fork tip `91fdf8c`, 270 s, straight after run A (S322).

| adopter | hooks | status before sync | sync | dry run | apply | exit | refusals | its hook refused the commit | shards kept (rehearsal) | moves | min rename | rewrites | left | not rewritten (mentions) | ledger entry | checks | proofs | history | check-links | clean | health before | health after | ratchet before | ratchet after | s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| model_project_constructor | armed: /Users/rmsharp/Development/model_project_constructor/.githooks | 23 tracked, 5 not current | committed (5 files, ok) | ok | applied | 0 | none | - | no proofs to rehearse | 8 (8 tracked, 0 plain) | R97 | .context-budget.json 1, .quality-gates.json 1, CLAUDE.md 27 | 2 | ci 1, harness 0, hooks 0, ledger 814, other 2296 | methodology/CHANGELOG.md | ok | {} -> {} | 335 -> 336 | exit 1 -> exit 1 | yes | 96 | 96 | cite in the receipt: quality_ratchet: 0/0 pass · 0 fail · 0 unmeasured · results 4f53cda18c2b · manifest 4f53cda18c2b | cite in the receipt: quality_ratchet: 0/0 pass · 0 fail · 0 unmeasured · results 4f53cda18c2b · manifest 4f53cda18c2b | 24 |
| feedback-loop-comparison | none | 23 tracked, 5 not current | committed (5 files, ok) | nothing-to-do | nothing-to-do | 0 | none | - | no proofs to rehearse | 0 (0 tracked, 0 plain) | - | none | 4 | - | no ledger | not run (nothing-to-do) | - | - | - | yes | 59 | not migrated | cite in the receipt: quality_ratchet: 0/0 pass · 0 fail · 0 unmeasured · results 4f53cda18c2b · manifest 4f53cda18c2b | not migrated | 8 |
| nprcgenekeepr | none | 23 tracked, 6 not current | committed with --force (6 files, ok) | ok | applied | 0 | none | - | no proofs to rehearse | 1 (1 tracked, 0 plain) | R100 | CLAUDE.md 7 | 3 | ci 5, harness 0, hooks 0, ledger 3388, other 322 | methodology/CHANGELOG.md | ok | {} -> {} | 1924 -> 1925 | exit 1 -> exit 1 | yes | 96 | 96 | cite in the receipt: quality_ratchet: 0/1 pass · 0 fail · 1 unmeasured · results bd4e76335429 · manifest aa983075d6a2 | cite in the receipt: quality_ratchet: 0/1 pass · 0 fail · 1 unmeasured · results bd4e76335429 · manifest aa983075d6a2 | 46 |
| mts-system | armed: .githooks | 23 tracked, 21 not current | committed (22 files, ok) | ok | applied | 0 | none | - | 4 proof(s) run, kept in place: none | 41 (41 tracked, 0 plain) | R97 | .context-budget.json 6, .quality-gates.json 1, CLAUDE.md 27 | 0 | ci 0, harness 0, hooks 0, ledger 1837, other 2478 | methodology/CHANGELOG.md | ok | {"0": 4} -> {"0": 4} | 450 -> 451 | exit 0 -> exit 1 | yes | 92 | 92 | cite in the receipt: quality_ratchet: 0/0 pass · 0 fail · 0 unmeasured · results 4f53cda18c2b · manifest 4f53cda18c2b | cite in the receipt: quality_ratchet: 0/0 pass · 0 fail · 0 unmeasured · results 4f53cda18c2b · manifest 4f53cda18c2b | 21 |
| vscode_quarto_ext | none | 23 tracked, 0 not current | not needed | nothing-to-do | nothing-to-do | 0 | none | - | 1 proof(s) run, kept in place: docs/archive/SESSION_NOTES-through-S253.md | 0 (0 tracked, 0 plain) | - | none | 3 | - | no ledger | not run (nothing-to-do) | - | - | - | yes | 76 | not migrated | cite in the receipt: quality_ratchet: 0/2 pass · 2 fail · 0 unmeasured · results 411131e807f2 · manifest 334939914945 | not migrated | 27 |
| Philippians | none | 23 tracked, 21 not current | committed (22 files, ok) | ok | applied | 0 | none | - | no proofs to rehearse | 32 (32 tracked, 0 plain) | R97 | .context-budget.json 3, .quality-gates.json 1, CLAUDE.md 16 | 0 | ci 0, harness 0, hooks 0, ledger 333, other 23 | methodology/CHANGELOG.md | ok | {} -> {} | 124 -> 125 | exit 0 -> exit 1 | yes | 51 | 51 | cite in the receipt: quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 2ef8d5a97abe · manifest 90d698a42ac4 | cite in the receipt: quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 2ef8d5a97abe · manifest 90d698a42ac4 | 14 |
| airqino | none | 23 tracked, 5 not current | committed (5 files, ok) | nothing-to-do | nothing-to-do | 0 | none | - | no proofs to rehearse | 0 (0 tracked, 0 plain) | - | none | 19 | - | no ledger | not run (nothing-to-do) | - | - | - | yes | 68 | not migrated | cite in the receipt: quality_ratchet: 2/2 pass · 0 fail · 0 unmeasured · results 2993256f954d · manifest 0f1d28b61292 | not migrated | 10 |
| chat_verification | armed: .githooks | 23 tracked, 5 not current | committed (5 files, its own hook refused (d. "Too small to log" is the failure mode, not an exception (the session runner's FM #27).); committed with --no-verify) | nothing-to-do | nothing-to-do | 0 | none | - | no proofs to rehearse | 0 (0 tracked, 0 plain) | - | none | 0 | - | no ledger | not run (nothing-to-do) | - | - | - | yes | 45 | not migrated | cite in the receipt: quality_ratchet: 0/0 pass · 0 fail · 0 unmeasured · results 4f53cda18c2b · manifest 4f53cda18c2b | not migrated | 9 |
| church_growth | armed: .githooks | 23 tracked, 5 not current | committed (5 files, its own hook refused (d. "Too small to log" is the failure mode, not an exception (the session runner's FM #27).); committed with --no-verify) | nothing-to-do | nothing-to-do | 0 | none | - | no proofs to rehearse | 0 (0 tracked, 0 plain) | - | none | 1 | - | no ledger | not run (nothing-to-do) | - | - | - | yes | 49 | not migrated | cite in the receipt: quality_ratchet: 0/0 pass · 0 fail · 0 unmeasured · results 4f53cda18c2b · manifest 4f53cda18c2b | not migrated | 9 |
| dalia_martinez_funeral | none | 23 tracked, 22 not current | committed (25 files, ok) | ok | applied | 0 | none | - | no proofs to rehearse | 30 (30 tracked, 0 plain) | R97 | .context-budget.json 3, .quality-gates.json 1, CLAUDE.md 12 | 1 | ci 0, harness 0, hooks 0, ledger 104, other 110 | methodology/CHANGELOG.md | ok | {} -> {} | 19 -> 20 | exit 0 -> exit 0 | yes | 48 | 49 | cite in the receipt: quality_ratchet: 0/0 pass · 0 fail · 0 unmeasured · results 4f53cda18c2b · manifest 4f53cda18c2b | cite in the receipt: quality_ratchet: 0/0 pass · 0 fail · 0 unmeasured · results 4f53cda18c2b · manifest 4f53cda18c2b | 13 |
| claude_work | none | 23 tracked, 23 not current | committed (27 files, ok) | ok | rolled-back | 3 | none | - | no proofs to rehearse | 30 (30 tracked, 0 plain) | - | .context-budget.json 3, .quality-gates.json 1 | 0 | ci 0, harness 0, hooks 0, ledger 32, other 0 | methodology/CHANGELOG.md | not run (rolled-back) | - | - | - | - | no commits | not migrated | no commits | not migrated | 10 |
| wsfct | armed: /Users/rmsharp/Development/wsfct/.git/hooks | 23 tracked, 21 not current | committed (22 files, ok) | ok | rolled back by its hook; applied with hooks off | 3 (hooks on) then 0 (hooks off) | none | git commit was refused: python3: can't open file '/private/tmp/claude-501/-Users-rmsharp-Development-methodology/61c2d328-63f6-439e-a95b-4c09ba34edb3/scratchpad/s322-adopters-B-work/wsfct/context_budg | 6 proof(s) run, kept in place: none | 44 (44 tracked, 0 plain) | R97 | .context-budget.json 5, .gitignore 2, .quality-gates.json 1, CLAUDE.md 48 | 11 | ci 2, harness 0, hooks 0, ledger 1910, other 3939 | methodology/CHANGELOG.md | ok | {"1": 6} -> {"1": 6} | 536 -> 537 | exit 0 -> exit 1 | yes | 94 | 94 | cite in the receipt: quality_ratchet: 0/0 pass · 0 fail · 0 unmeasured · results 4f53cda18c2b · manifest 4f53cda18c2b | cite in the receipt: quality_ratchet: 0/0 pass · 0 fail · 0 unmeasured · results 4f53cda18c2b · manifest 4f53cda18c2b | 74 |

## 3. The comparison, column by column (`layer7b-adopters-compare.py`)

adopters: A 12, B 12; columns compared: 27 (apply_exit, apply_status, checks, dry_exit, dry_status, head, health_after, health_before, history, hits, hook_rollback, hooks, ledger_entry, left_in_place, links, min_similarity, moves, proofs, ratchet_after, ratchet_before, refusals, rehearsal, rewrites, status_after_sync, status_before_sync, sync, tree_clean)

== model_project_constructor: 1 differing column(s)
   sync:
      A  committed with --force (5 files, ok)
      B  committed (5 files, ok)

== feedback-loop-comparison: 1 differing column(s)
   sync:
      A  committed with --force (5 files, ok)
      B  committed (5 files, ok)

== nprcgenekeepr: 0 differing column(s)

== mts-system: 1 differing column(s)
   sync:
      A  committed with --force (22 files, ok)
      B  committed (22 files, ok)

== vscode_quarto_ext: 3 differing column(s)
   ratchet_before:
      A  cite in the receipt: quality_ratchet: 0/2 pass · 2 fail · 0 unmeasured · results a5df9c4dde18 · manifest 334939914945
      B  cite in the receipt: quality_ratchet: 0/2 pass · 2 fail · 0 unmeasured · results 411131e807f2 · manifest 334939914945
   status_before_sync:
      A  23 tracked, 2 not current
      B  23 tracked, 0 not current
   sync:
      A  committed with --force (2 files, ok)
      B  not needed

== Philippians: 1 differing column(s)
   sync:
      A  committed with --force (22 files, ok)
      B  committed (22 files, ok)

== airqino: 1 differing column(s)
   sync:
      A  committed with --force (5 files, ok)
      B  committed (5 files, ok)

== chat_verification: 1 differing column(s)
   sync:
      A  committed with --force (5 files, its own hook refused (d. "Too small to log" is the failure mode, not an exception (the session runner's FM #27).); committed with --no-verify)
      B  committed (5 files, its own hook refused (d. "Too small to log" is the failure mode, not an exception (the session runner's FM #27).); committed with --no-verify)

== church_growth: 1 differing column(s)
   sync:
      A  committed with --force (5 files, its own hook refused (d. "Too small to log" is the failure mode, not an exception (the session runner's FM #27).); committed with --no-verify)
      B  committed (5 files, its own hook refused (d. "Too small to log" is the failure mode, not an exception (the session runner's FM #27).); committed with --no-verify)

== dalia_martinez_funeral: 0 differing column(s)

== claude_work: 0 differing column(s)

== wsfct: 1 differing column(s)
   sync:
      A  committed with --force (22 files, ok)
      B  committed (22 files, ok)

columns equal in all 12 adopters: apply_exit, apply_status, checks, dry_exit, dry_status, head, health_after, health_before, history, hits, hook_rollback, hooks, ledger_entry, left_in_place, links, min_similarity, moves, proofs, ratchet_after, refusals, rehearsal, rewrites, status_after_sync, tree_clean
columns that differ in at least one: ratchet_before (1), status_before_sync (1), sync (9)

## 4. The candidate's `bin/sync` over `model_project_constructor` (why 9 of 12 need `--force` with the candidate's tree)

The candidate's `bin/sync` (no `--force`) over a clean clone of `model_project_constructor`'s committed HEAD: why 9 of 12 adopters need `--force` with the candidate's tree and 3 do not (the fork's `bin/sync`, same bytes, over the same clone exits 0).

sync: /private/tmp/claude-501/-Users-rmsharp-Development-methodology/61c2d328-63f6-439e-a95b-4c09ba34edb3/scratchpad/s322-probe-mpc
  source:  local (/private/tmp/claude-501/-Users-rmsharp-Development-methodology/61c2d328-63f6-439e-a95b-4c09ba34edb3/scratchpad/s322-repoA)
  mode:    commit
  version: v4.2-19-gab35e96
  layout:  new (found methodology/SESSION_RUNNER.md)

  ERROR: the following files have local modifications that don't match
  any canonical or historical version and would be overwritten:
    methodology/SESSION_RUNNER.md
    methodology/CLAUDE_TEMPLATE.md
    methodology/BOOTSTRAP.md
    methodology/HOW_TO_USE.md

  The recommended pattern (see plan §3.2) is to move per-project
  customizations into CLAUDE.md's 'Project-Specific Methodology
  Adaptations' section, keeping synced files byte-identical to canonical.

  To proceed anyway and overwrite local changes, pass --force.
  To inspect the drift first:
    diff /private/tmp/claude-501/-Users-rmsharp-Development-methodology/61c2d328-63f6-439e-a95b-4c09ba34edb3/scratchpad/s322-probe-mpc/methodology/SESSION_RUNNER.md /private/tmp/claude-501/-Users-rmsharp-Development-methodology/61c2d328-63f6-439e-a95b-4c09ba34edb3/scratchpad/s322-repoA/starter-kit/SESSION_RUNNER.md
    diff /private/tmp/claude-501/-Users-rmsharp-Development-methodology/61c2d328-63f6-439e-a95b-4c09ba34edb3/scratchpad/s322-probe-mpc/methodology/CLAUDE_TEMPLATE.md /private/tmp/claude-501/-Users-rmsharp-Development-methodology/61c2d328-63f6-439e-a95b-4c09ba34edb3/scratchpad/s322-repoA/starter-kit/CLAUDE_TEMPLATE.md
    diff /private/tmp/claude-501/-Users-rmsharp-Development-methodology/61c2d328-63f6-439e-a95b-4c09ba34edb3/scratchpad/s322-probe-mpc/methodology/BOOTSTRAP.md /private/tmp/claude-501/-Users-rmsharp-Development-methodology/61c2d328-63f6-439e-a95b-4c09ba34edb3/scratchpad/s322-repoA/starter-kit/BOOTSTRAP.md
    diff /private/tmp/claude-501/-Users-rmsharp-Development-methodology/61c2d328-63f6-439e-a95b-4c09ba34edb3/scratchpad/s322-probe-mpc/methodology/HOW_TO_USE.md /private/tmp/claude-501/-Users-rmsharp-Development-methodology/61c2d328-63f6-439e-a95b-4c09ba34edb3/scratchpad/s322-repoA/HOW_TO_USE.md
