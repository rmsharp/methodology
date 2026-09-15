**F2 and F3 — done.** Two commits on `read-set-budgets`, on top of `d4e1570`; one push, so one notification.

**F2 — `37740763`.** `test_a_synced_repo_with_context_budget_installed_is_still_doc_only` is generalized in
place as `test_a_synced_repo_with_each_installed_source_file_is_still_doc_only`. Every non-markdown file
`bin/sync` installs — `bin/_manifest.py`'s dests, today the three `.py` tools and `.context-budget.json` — is
written from its real `starter-kit/` source into the doc-only fixture, one at a time and then all together,
and must leave `source_loc` 0, `doc_only` true and no *"No test infrastructure"* risk; each must also pass
`is_framework_installed` directly. The names come from the manifest, not `FRAMEWORK_INSTALLED_SOURCE`, so a
file the manifest installs and the scanner does not list fails by name, and a last assertion checks the test
covered exactly the scanner's list. RED first — your mutant and five more, each planted in both twins:

| mutant | suite before | suite after |
|---|---|---|
| M1 — `methodology_trim.py`'s `version_re` and four signatures neutralized (yours) | **OK (211)** | fails — `2181 != 0` source LOC |
| M2 — the same for `context_budget.py` | fails 2 | fails 3 |
| M3 — the same for `methodology_dashboard.py` | fails 12 | the same 12, **none of them this test** |
| M4 — `.context-budget.json`'s four signatures neutralized | **OK (211)** | fails, on the direct predicate call |
| M5 — `methodology_trim.py` dropped from the tuple and the table | fails 1 | fails 4 |
| M6 — the one `collect_all` call site skips `methodology_trim.py` | **OK (211)** | fails, end to end |

M3 is the one this test cannot catch: neutralizing the scanner's signatures writes the new strings into its
own table, so the real file still matches itself. The twelve stand-in fixtures catch it, and the docstring
says so.

**F3 — `aa36fd8`: your (i) for the pair, and for the ledgers a fourth answer — drop them.**

- **The pair.** `SESSION_RUNNER.md` and `SAFEGUARDS.md` trade their byte ceilings for token ceilings at
  densities measured by the doubled-file method on the blobs the merge produces — 19,200 and 5,800 tokens,
  which partition the 25,000-token cap. The `read-set` class keeps its total as a measurement with no ceiling
  beside it: `class_ceiling()` can take only a typed byte total or one derived at the 2.27 floor, and the
  floor is for a file nobody can meter. This pair has been metered. The runner can now grow about 2 KB
  (723 tokens) before `--precommit` refuses it; `SAFEGUARDS.md` is pinned at its size in the merge.
- **The ledgers** leave `files[]` for `_deliberate_exclusions`, with the reason and the command that
  recovers their entries. **Your (ii) does not work as written — I ran it.** In a whole-read class
  `token_ceiling()` clamps every file to the 25,000-token cap whatever `max_bytes` says, so pinning the
  ledgers at their size left both over on tokens (46,135 and 42,778 on the merge), and the pin refused the
  next append. Its workable form — both moved to `on-demand` at the trimmer's 196,608 B — also reports OK,
  but copies the trimmer's number into a second file that can drift from it. Dropped, each ledger has one
  limit, the trimmer's, which answers **F4** as you framed it. The seeds' prose still says *"default
  65,536 B"* (`starter-kit/CHANGELOG.md:104`, `starter-kit/HANDOFFS.md:98`); that stays with the
  ledger-rules PR.
- Every answer — yours three and this one, alone and combined — was run through `--status` and six staged
  commits on this branch and on its merge into `main`. `--status` now exits **0** on both, where it
  exited 2.

**One correction the measurement turned up.** Your S16 paragraph added 967 B to `main`'s `SAFEGUARDS.md`
after I had measured, so the merged pair is **68,548 B and 24,278 tokens** — 97.1% of the cap, 722 spare —
not 67,581 / 23,902, and `main`'s own pair is now 81,493 B and 28,610 tokens. Both re-measured the same way,
after the method reproduced the description's recorded 47,805 first. The description now carries them,
with the new head, the diff size (28 files, +7,892 / −580) and the corpus total (659,755 → 839,383 B, still
+179,628).

Verified in `--no-local` clones, each exit code read bare: `bin/tests.sh` **115 / 1** at `37740763` and
`aa36fd8` — 116 rows each, not one differing from `d4e1570`'s even in a number, the failure Test 9 as
before; unit suites 211 + 123 + 116 OK; `bin/check-links` OK (105 links, 23 files); `bin/check-learnings`
OK (13 rows). Both commits are canonical-only, so adopters receive nothing from either, and both ledger
entries sit with #80's, below `main`'s: `git merge-tree` against `9fa3141` is still empty, and the push
was a fast-forward.

F5 and F6 can follow the merge.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
