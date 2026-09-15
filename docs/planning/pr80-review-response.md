# PR #80 — answering the maintainer's review (F1 published; F2 done locally; F3 next)

**Fork-only.** S163, 2026-09-15; F2 added at S164, the same day. The review is the maintainer's comment
on [PR #80](https://github.com/KJ5HST/methodology/pull/80#issuecomment-5674670153), posted 2026-09-15
04:19 UTC and addressed to the contributor. His upstream receipt (S18) says the thread is now ours and
that he will not merge until F1 is answered. **F1 was published at S163**: pushed (`b82dcff..d4e1570`),
the description updated, the reply posted ([comment](https://github.com/KJ5HST/methodology/pull/80#issuecomment-5676599724)).
**F2 is on a local branch and not pushed** (§4). Every push, description edit and comment is its own
go-ahead from the operator.

## 1. The review, in one table

| | Kind | What it asks | Status |
|---|---|---|---|
| F1 | decision | `starter-kit/FRAMEWORK_LEARNINGS.md` carries 46 rows; the description says 13. (a) cut to 1–13 + the `#14` callout, or (b) argue for 46 | **(a), chosen by the operator at S163; pushed, described and answered at S163** (§2, §3) |
| F2 | fix | the `methodology_trim.py` doc-only exclusion is unguarded: generalize the regression test over every `FRAMEWORK_INSTALLED_SOURCE` name, RED first | **done at S164 on local branch `pr80/f2-installed-source-guard`, `37740763`; not pushed** (§4) |
| F3 | fix or state | the root `.context-budget.json` reports the PR's own headline as `OVER` | **next session; starts with a decision** (§5) |
| F4 | can follow | two limits on `CHANGELOG.md`: the budget's 65,536 B against the trimmer's 196,608 B | BL-57's C2, fixed by its P2 — a new PR after #80 merges (plan D5) |
| F5 | can follow | the trimmer's docstring cites an unpublished design doc and a `--no-renames` the branch's hook lacks | open (§6) |
| F6 | can follow | *"`--source=github` installs nothing today"* is true of the branch's copy only | open (§6) |

## 2. F1 (a) — what the local branch holds

Branch **`pr80/f1-learnings-1-13`** in this repository, worktree `../methodology-pr80`, from #80's head
`b82dcff`. Two commits, each carrying its own entry in the branch's `CHANGELOG.md`:

1. **`5c9f0f3`** — every citation the cut would leave dangling states its rule instead of a number:
   `starter-kit/context_budget.py:77`, `:378` (Learning #34) and `:409` (*"learning #22 / #26a"*: this
   table has no `#26a`, and its #22 is about backlog deletion, so the pair cites another numbering);
   `tools/test_context_budget.py:489`, `:546`, `:563`; `tools/test_methodology_trim.py:1244`, `:2063`.
   `context_budget.py` and `test_methodology_trim.py` parse to an AST identical to `b82dcff`'s.
2. **`d4e15706`** — the file keeps rows 1–13 (byte-identical) and the `#14` callout, reworded because no
   row 15 exists now; `bin/check-learnings`' comment quoting the old callout follows it.
   56,673 → 13,983 B.

**Why the repair came first:** `bin/check-learnings` sweeps only the distributed **Markdown**
(`distributed_md_files`, `bin/check-learnings:255` at `b82dcff`), so the `context_budget.py` citations —
a distributed file — would have dangled in every adopter with the check green. That scope gap is worth
its own follow-up upstream; the reply names it.

**Ledger placement.** Both entries sit with #80's own entries, below `main`'s, as the maintainer's
conflict-resolution entry at the top of that ledger prescribes: an entry prepended at the top
re-conflicts with the next `main` prepend. `git merge-tree --write-tree --name-only upstream/main
d4e15706` against `9fa3141`: **no conflicts**.

**Verified**, in `--no-local` clones, every exit code read bare:

| tree | `bin/tests.sh` | unit suites | `check-links` | `check-learnings` |
|---|---|---|---|---|
| `b82dcff` (control) | 115 / 1, exit 1 | 116 + 211 + 123 OK (4 skipped) | OK, 105 / 23 | OK, 46 rows |
| `5c9f0f3` | 115 / 1, exit 1 | same | OK | OK, 46 rows |
| `d4e15706` | 115 / 1, exit 1 | same | OK | OK, **13 rows**, contiguous 1..13 |

116 rows on each side, **0 status flips, 0 rows differing even in a number**; the failure is Test 9 on
all three, as before. A `Learning #20` planted in `starter-kit/SAFEGUARDS.md` is caught (exit 1) and the
restored tree passes. `context_budget.py --status` changes no row's status.

## 3. Publishing it — three separate go-aheads, in this order

```sh
# 0. Nothing moved? #80's head must still be b82dcff, and no new comment unanswered.
git fetch upstream && git rev-parse --short upstream/read-set-budgets
gh pr view 80 --repo KJ5HST/methodology --json headRefOid,comments --jq '.headRefOid, (.comments|length)'
# 1. Push, fast-forward only.
git push upstream pr80/f1-learnings-1-13:read-set-budgets
# 2. The description: every figure F1 moves, plus a verification row.
gh pr edit 80 --repo KJ5HST/methodology --body-file docs/planning/pr80-body-after-f1.md
# 3. The reply.
gh pr comment 80 --repo KJ5HST/methodology --body-file docs/planning/pr80-reply-f1.md
```

If the head has moved, **do not force.** Rebase the two commits onto the new head, re-run the suites and
`git merge-tree`, and re-derive every figure in the description (head sha, `28 files, +7,795 / −554`,
the corpus total 838,416 B, the two table rows) at publish time — a document that waits for approval
keeps measuring the tree it was written against (*fork* Learning #61). The figures come from the method
that reproduced the description's own 658,788 / 881,137 B first: sum `git cat-file -s` over
`bin/_manifest.py`'s `DISTRIBUTION` sources at the ref.

After the push, `git worktree remove ../methodology-pr80`; the branch can stay until #80 merges.

## 4. F2 — done at S164 on a local branch, not pushed

**The ask:** *"Neutralize its `version_re` and its four signatures in both twins and the unit suite stays
OK (211) while the synced fixture flips to `code` with the false HIGH … Parametrize it over every
`FRAMEWORK_INSTALLED_SOURCE` name using the real `starter-kit/` file, RED first."*

**What the branch holds.** `pr80/f2-installed-source-guard`, from #80's head `d4e1570`, one commit:
**`37740763`**, touching `tools/test_methodology_dashboard.py` and the branch's `CHANGELOG.md` only —
canonical-only, so adopters receive nothing, and neither scanner twin changes. The test at `:2666`
(`d4e1570`), `test_a_synced_repo_with_context_budget_installed_is_still_doc_only`, is generalized in
place as `test_a_synced_repo_with_each_installed_source_file_is_still_doc_only`:
- every non-markdown dest in `bin/_manifest.py`'s `DISTRIBUTION` (the four `FRAMEWORK_INSTALLED_SOURCE`
  names today) is written from its real `starter-kit/` source into the Quarto doc-only fixture, alone and
  then all together, and must leave `source_loc` 0, `doc_only` true and no "No test infrastructure" risk;
- each file must also pass `is_framework_installed` directly;
- the names come from the manifest, not the constant under test, so a file the manifest installs and the
  scanner does not list fails here by name, and a last assertion checks the test covered exactly the
  scanner's list. A fifth name is therefore parametrized without anyone adding it — the *"cannot
  enforce"* this section used to carry.

**`.context-budget.json` is covered, not excluded.** It categorizes as `config` before the predicate is
consulted, so its end-to-end half cannot fail on its signatures: the direct predicate call holds its
signature entry, and its category is asserted so that reason stays checked.

**RED first — six mutants,** each planted in both twins of a `--no-local` clone by
[`pr80-f2-mutants.py`](pr80-f2-mutants.py) (its docstring has the commands), which asserts every edit
matched once per file; the old test file (`d4e1570`) and the new one run against each. Controls
211 OK on both sides; the clone verified clean after every mutant. The round ran twice — the second time
on the final docstring — with identical results.

| mutant | old suite | new suite |
|---|---|---|
| M1 — `methodology_trim.py`'s `version_re` and 4 signatures neutralized (the review's) | **OK (211)** | FAIL ×2 — `2181 != 0` source LOC, alone and all together |
| M2 — the same for `context_budget.py` | FAIL ×2 | FAIL ×3 |
| M3 — the same for `methodology_dashboard.py` | FAIL ×12 | FAIL ×12, **none of them this test** |
| M4 — `.context-budget.json`'s 4 signatures neutralized | **OK (211)** | FAIL ×1 — the direct predicate call |
| M5 — `methodology_trim.py` dropped from the tuple and the table | FAIL ×1 | FAIL ×4 — this test by name, and its coverage check |
| M6 — the `collect_all` call site skips `methodology_trim.py`; predicate untouched | **OK (211)** | FAIL ×2 — end to end |

**Cannot enforce: M3.** The neutralized strings sit in the scanner's own signature table, so the real
`methodology_dashboard.py` still matches itself; the class's twelve stand-in fixtures
(`installed_scanner()`) catch it, and the docstring says so. M4 shows the direct half is live on its own,
M6 the end-to-end half.

**Verified**, in `--no-local` clones, every exit code read bare:

| | `d4e1570` (control) | `37740763` |
|---|---|---|
| `tools/test_methodology_dashboard.py` | 211 OK | 211 OK |
| `tools/test_methodology_trim.py` | 123 OK (2 skipped) | 123 OK (2 skipped) |
| `tools/test_context_budget.py` | 116 OK (2 skipped) | 116 OK (2 skipped) |
| `bin/check-links` | OK, 105 links / 23 files | OK, 105 links / 23 files |
| `bin/check-learnings` | OK, 13 rows | OK, 13 rows |
| `bin/tests.sh` | 115 / 1, exit 1 (Test 9) | 115 / 1, exit 1 (Test 9) — 116 rows, 0 status flips, 0 rows differing |

`git merge-tree --write-tree --name-only upstream/main 37740763` (`upstream/main` = `9fa3141`): no
conflicts; `read-set-budgets` is an ancestor, so the push is a fast-forward.

**Publishing is held** (S164 Phase 0's suggestion) so F2 and F3 go up in one push and one reply. F3 commits
on top of `37740763`; then §3's order applies — re-check the head and comments, push, then the
description, then the reply (`gh api -X PATCH` for the description; `gh pr edit` fails). The description
needs nothing for F2: it names no test and quotes no figure F2 moves. The reply's F2 paragraph can take the
table above.

## 5. F3 — set up for the next session; it starts with a decision

`context_budget.py --status` on the branch exits 2. At `d4e15706`, from the root `.context-budget.json`:

| row | size | ceiling | config line |
|---|---:|---:|---|
| read-set total | 67,581 B | 56,750 B (derived: 25,000 × 2.27) | `:26`–`:30` |
| `starter-kit/SESSION_RUNNER.md` | 52,195 B | 41,364 B | `:47`–`:49` |
| `CHANGELOG.md` | 105,876 B (grows with every entry) | 65,536 B | `:59`–`:61` |
| `HANDOFFS.md` | 82,069 B | 65,536 B | `:71`–`:73` |

The maintainer offers three answers: **(i)** denominate the read-set ceiling in tokens at measured
density (the tool already does this for `CHANGELOG.md`, *"at 2.4674 B/token (measured)"*); **(ii)** set
the ledger ceilings where the ledgers are and let the ratchet hold from there; **(iii)** say *"over at
install, by design"* in the file and the body. The read-set pair measured 23,902 tokens by the
doubled-file method — it fits at every measured density and not at the 2.27 floor.

**Bring the operator this link before choosing:** under BL-57's Q2 A, `CHANGELOG.md` is not a
read-budget file at all — nothing reads it whole — and this fork removed it from its own budget
(`3c8acd5`). That is a fourth answer for the ledger rows (drop them), and it is the one BL-57's P2
will argue upstream anyway. Explain the options in prose and take a letter.

## 6. F5 and F6 — open, can follow the merge

- **F5:** `starter-kit/methodology_trim.py:9` and `:155` cite `docs/planning/ledger-trimmer-design.md`,
  absent upstream (this fork has it, 74,109 B); `:33` cites *"`--no-renames` in the FM #27 pre-commit
  hook"* — 0 occurrences in the branch's `.githooks/pre-commit`, 3 in this fork's. Publish the design
  doc with a PR, and correct the hook claim.
- **F6:** the description's *"`bin/sync --source=github` installs nothing today"* is true of the
  branch's copy only; `main`'s 24-row sync works (Test 9 passes there). Wording.

## 7. Hazards

- `context_budget.py --status` writes an untracked `.context-budget-history.jsonl` into the tree it
  measures. Never commit it; delete it after verifying it holds only your run.
- The worktree's `.githooks/pre-commit` (the branch's) refuses a commit without `CHANGELOG.md`
  co-staged. Place any new branch entry with #80's block, not at the top.
- A `--no-local` clone lacks `upstream/*` refs: check out the local branch or a sha, and let the runner
  refuse a wrong `HEAD` before it runs anything.
