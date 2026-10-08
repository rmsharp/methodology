# S284: `bin/migrate-layout` judges the framework documents' links

**A tool change, not a plan phase.** It closes the carry S282 and S283 left: the apply's `check-links` cell was
`INFORMATIONAL` "until P9" (plan 4.7.4 step 4 lists `bin/check-links` among the apply's verifications). P9 is done, so
the cell had to start counting. The rule below was chosen from a measurement, because the obvious rule is wrong.

## The obvious rule fails, and the fixture said so before any adopter did

Judging the exit code (before must equal after) turns every apply test red: the fixture's ledger
(`ledger_with_entries`, `tools/test_migrate_layout.py`) holds a committed entry that links
`docs/methodology/HOW_TO_USE.md`, right where the ledger sat. The move leaves a committed entry alone (C6), so the link
dangles in `methodology/CHANGELOG.md`. A real adopter's ledger does the same.

## The measurement (`links-after-move-12-adopters.py`, `links-after-move-runs/`)

12 adopters, each in a `--no-local` clone of its committed HEAD, synced from `15c7e3c` with that sha's `bin/sync`, then that
sha's `check-links --tree` before, `bin/migrate-layout --apply --skip-checks`, `check-links --tree` after. Every
dangling link sorted by the manifest disposition of the file it sits in.

| | adopters | dangling in framework documents (`tracked`) | dangling in the adopter's own files (`seed`) |
|---|---|---|---|
| migrated | 11 | **0 before, 0 after, in every one** | 8 of 11 have some after: 6, 23 (4 before), 108, 15, 18, 2, 1, 12 (185 in all) |
| rolled back | 1 (`claude_work`) | - | - |

All 185 sit in three files: `CHANGELOG.md` (63), `SESSION_NOTES.md` (76), `HANDOFFS.md` (46). A plain exit-code
comparison would have flagged 7 of the 11 (0 before, 1 after); the framework count flags none.

## The rule

`links_cell` parses check-links' own lines (`  <file>:<line>  ->  <target>`) and counts each dangling link by whether
its file is a TRACKED framework document, under either layout's name (`framework`, **judged**: the count must not change,
like the other checks) or a file the project owns (`project`, **reported**). A run that did not decide (exit 2, a
timeout), or an exit 1 whose lines are not in that shape, has no counts (`None`) and so differs from a clean before: an
unreadable result never reads as zero. The report drops its `informational` key.

## Tests

`tools/test_migrate_layout.py` 128 to 136 (ten new tests, two retired), written before the code: against the old tool 4
failed and 1 errored of the 10 selected by name. A mutation round on the new lines: 15 mutants, 14 killed at once, the 15th (the
`code in (0, 1)` guard, near-equivalent for real output) pinned by a case that gives an exit 2 a dangling-shaped line and
killed after. The gate `migrate-layout-unit-tests` is tightened 128 to 136.

## The acceptance run (`s284-adopter-runs/`)

`migrate-12-adopters.py` (P7's script, checks on, adopters' hooks armed as in the real clone) from a clean clone of
`7c377c2`, the commit holding the changed tool. **11 of 12 migrate with `checks ok` and no difference**; the links cell
reads 0 framework before and after in all eleven, and, for the eight with project-file links, the same counts as the
measurement (6, 23 from 4, 108, 15, 18, 2, 1, 12). `claude_work` rolls back as at P7 (its ledger holds 1,305 bytes and would fall to
67% as a rename; the tool's own rule). `wsfct`'s own hook refuses the commit until its `context_budget.py` path is
updated, as at P7; with its hooks off it applies and checks ok. `links-cells.json` holds the cells and the causes.

## Not verified

An adopter's own CI or tests; a real (non-clone) adopter; the first real migration (P11). A project whose framework
documents are older than P9 never reaches this check: it is refused first (`not-current`), so the judged count assumes
documents that `bin/sync` just wrote. For P11, `model_project_constructor` will print
`links: exit 0; 0 framework, 0 project dangling -> exit 1; 0 framework, 6 project dangling` and exit 0; the six are its ledger
and notes entries (`CHANGELOG.md` 2, `HANDOFFS.md` 1, `SESSION_NOTES.md` 3).
