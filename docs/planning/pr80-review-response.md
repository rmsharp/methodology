# PR #80 — answering the maintainer's review (F1 published at S163; F2 and F3 published at S166)

**Fork-only.** S163, 2026-09-15; F2 added at S164 and F3 at S165, the same day. The review is the
maintainer's comment on [PR #80](https://github.com/KJ5HST/methodology/pull/80#issuecomment-5674670153),
posted 2026-09-15 04:19 UTC and addressed to the contributor. His upstream receipt (S18) says the thread
is now ours and that he will not merge until F1 is answered. **F1 was published at S163**: pushed
(`b82dcff..d4e1570`), the description updated, the reply posted ([comment](https://github.com/KJ5HST/methodology/pull/80#issuecomment-5676599724)).
**F2 and F3 were published at S166** (§4, §5), on the operator's go-ahead for all three actions: one
fast-forward push, `d4e1570..aa36fd8` — F3's branch `pr80/f3-read-set-token-ceilings` carries F2's
commit beneath it — then the description from [`pr80-body-after-f3.md`](pr80-body-after-f3.md), then
the reply ([comment](https://github.com/KJ5HST/methodology/pull/80#issuecomment-5685701488)). F4 is
answered with F3; F5 and F6 remain (§6). Every push, description edit and comment is its own go-ahead
from the operator.

## 1. The review, in one table

| | Kind | What it asks | Status |
|---|---|---|---|
| F1 | decision | `starter-kit/FRAMEWORK_LEARNINGS.md` carries 46 rows; the description says 13. (a) cut to 1–13 + the `#14` callout, or (b) argue for 46 | **(a), chosen by the operator at S163; pushed, described and answered at S163** (§2, §3) |
| F2 | fix | the `methodology_trim.py` doc-only exclusion is unguarded: generalize the regression test over every `FRAMEWORK_INSTALLED_SOURCE` name, RED first | **done at S164 (`37740763`); published at S166** with F3's push (§4) |
| F3 | fix or state | the root `.context-budget.json` reports the PR's own headline as `OVER` | **R1 L1, the operator's choice at S165 (`aa36fd8b`, on top of F2); published at S166** — pushed, described and answered (§3, §5) |
| F4 | can follow | two limits on `CHANGELOG.md`: the budget's 65,536 B against the trimmer's 196,608 B | **answered by F3 as the review framed it** — `CHANGELOG.md` leaves the budget, so the trimmer's is its one limit; the seeds' prose naming 65,536 B stays with BL-57's P2 (§5) |
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

## 3. Publishing — three separate go-aheads, in this order (F1 published at S163; F2 + F3 at S166)

```sh
# 0. Nothing moved? #80's head must still be d4e1570 and main 9fa3141, with no comment beyond the two.
git fetch upstream && git rev-parse upstream/read-set-budgets upstream/main | cut -c1-8
gh pr view 80 --repo KJ5HST/methodology --json headRefOid,comments --jq '.headRefOid, (.comments|length)'
# 1. Push, fast-forward only -- F2 (37740763) and F3 (aa36fd8b) together.
git push upstream pr80/f3-read-set-token-ceilings:read-set-budgets
# 2. The description. `gh pr edit` fails on the Projects-classic deprecation; S163 used the REST API.
gh api -X PATCH repos/KJ5HST/methodology/pulls/80 -F body=@docs/planning/pr80-body-after-f3.md
# 3. The reply.
gh pr comment 80 --repo KJ5HST/methodology --body-file docs/planning/pr80-reply-f2-f3.md
```

Read each back before the next: the branch head equals `aa36fd8b`; the live body equals the file (compare
after stripping the one trailing newline `gh api --jq` adds, not with `cmp`); the comment count is 3.
(`git rev-parse --short` takes one revision only — given two it fails with *"Needed a single revision"*.)

**S166 ran this recipe as written.** Every precondition held, and each read-back matched, with one lag:
seconds after the push, #80's `headRefOid` still read `d4e1570` (`mergeable` `UNKNOWN`); the second
query read `aa36fd8b`, `MERGEABLE`/`CLEAN`. Read the PR itself back, not only the ref, before a step
that names the new head. The reply went through the REST API (`gh api
repos/KJ5HST/methodology/issues/80/comments -F body=@…`), which returns the comment's id for the
read-back.

If anything has moved, **do not force.** Rebase F2 and F3 onto the new head, re-run the suites,
`git merge-tree` and `context_budget.py --status` on the branch and on its merge into `main`, and
re-derive every figure in the description at publish time — a document that waits for approval keeps
measuring the tree it was written against (*fork* Learning #61). The S165 figures, each from a method
that first reproduced the figure it replaces:

- the diff: `git diff --shortstat $(git merge-base upstream/main <head>) <head>` — 28 files,
  +7,892 / −580 at `aa36fd8b`, after reproducing +7,795 / −554 at `d4e1570`;
- the corpus: sum `git cat-file -s` over `bin/_manifest.py`'s `DISTRIBUTION` sources at `upstream/main` and
  at the merged tree — 659,755 → 839,383 B, after reproducing 658,788 at `512c2ed` and 838,416 at `d4e1570`;
- the pair: the doubled-file method on `main` and on the merged tree — 28,610 and 24,278 tokens, after
  reproducing 47,805 for this branch's doubled pair.

If `main` has touched `SESSION_RUNNER.md` or `SAFEGUARDS.md` again, re-measure the two `max_tokens` in
the branch's `.context-budget.json` too: `SAFEGUARDS.md`'s is pinned at `main`'s size at `9fa3141`.

The three local `pr80/*` branches can stay until #80 merges; F3's worktree `../methodology-pr80-f3` is
removed at S165's close-out.

## 4. F2 — done at S164 on a local branch, published at S166

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

**Publishing was held** (S164 Phase 0's suggestion) so F2 and F3 went up in one push and one reply, at
S166. F3 commits
on top of `37740763`; then §3's order applies — re-check the head and comments, push, then the
description, then the reply (`gh api -X PATCH` for the description; `gh pr edit` fails). The description
needs nothing for F2: it names no test and quotes no figure F2 moves. The reply's F2 paragraph can take the
table above.

## 5. F3 — done at S165 on a local branch, published at S166: R1 L1, the operator's choice

**The ask:** *"the root `.context-budget.json` reports this PR's own result as OVER … Either denominate
the read-set ceiling in tokens at measured density …, or set the ledger ceilings where the ledgers are
and let the ratchet hold from there, or say 'over at install, by design' in the file and the body."*
At `37740763`, `--status` exited 2: runner 52,195 B vs 41,364 B, read-set total 67,581 B vs 56,750 B
(derived: 25,000 × 2.27), `CHANGELOG.md` 108,552 B and `HANDOFFS.md` 82,069 B vs 65,536 B each.

**The four rows are two decisions** — the read-set pair and its total; the two ledgers — and every answer
was built as a config and run before any was offered: `--status`, and six staged commits under
`--precommit` (+300 B to each ledger; the runner +100 B, +2,100 B and −100 B; `SAFEGUARDS.md` +100 B), on
two trees: `37740763`, and its merge into `upstream/main` (`9fa3141`). [`pr80-f3-variants.py`](pr80-f3-variants.py)
reproduces every row; its docstring has the commands.

| variant | `--status` | `--precommit` refuses |
|---|---|---|
| V0 — as shipped | 2 OVER, both trees | every ledger append; any read-set growth |
| (ii) as written — ledgers pinned at their size | 2 OVER — the ledgers still over on tokens | every ledger append (the pin); any read-set growth |
| (ii) workable — ledgers `on-demand` at 196,608 B | 2 OVER (read-set) | read-set growth only |
| (iv) — ledgers dropped | 2 OVER (read-set) | read-set growth only |
| (iii) — byte ceilings kept, re-pinned for the merge | 2 OVER | every ledger append; every read-set growth; the runner's derived token arm also reads 17 over |
| (i) — read-set in tokens, class ceiling removed | 2 OVER (ledgers) | ledger appends; runner +2,100 B; `SAFEGUARDS.md` +100 B on the merge |
| (i) with the class typed at 70,587 B | 2 OVER (ledgers) | as (i), plus the typed class arm |
| **R1 L1 — (i) + (iv), chosen** | **0 OK, both trees** | runner +2,100 B (19,220 tok vs 19,200); `SAFEGUARDS.md` +100 B on the merge |
| R1 L2 — (i) + (ii) workable | 0 OK, both trees | the same |

**Two findings bound the choice.** (ii) cannot work as written: `token_ceiling()`
(`starter-kit/context_budget.py:112`) clamps every whole-read file to the 25,000-token cap whatever its
`max_bytes` says, so a ledger past ~60 KB is over for good unless it leaves the whole-read classes. And (i)
cannot be written as a class ceiling: `class_ceiling()` (`:166`) takes a typed byte total or one derived at
the 2.27 B/token floor (`framework_share()`, `:139`) — so the pair is bounded per file, its two token
ceilings partitioning the cap.

**The measurements the config carries**, by the doubled-file method, after it reproduced the description's
recorded 47,805 tokens for this branch's doubled pair: runner (blob `c0550acd`) ×2 → 36,955 tokens,
2.8248 B/token; `SAFEGUARDS.md` (blob `656beae7`, `main`'s, which the merge takes) ×7 → 40,605, 2.8191; the
merged pair ×2 → 48,555 → **24,278 tokens (68,548 B)**; `main`'s pair ×2 → 57,219 → 28,610 (81,493 B),
undoubled 28,612. **The merge is 967 B larger than this branch** — `main`'s S16 paragraph in
`SAFEGUARDS.md`, which landed after the description was measured — and that also put `SAFEGUARDS.md` over
its 15,386 B pin on the merged tree.

**The operator chose R1 L1** (S165): (i) for the pair, the review's first answer; (iv) for the ledgers.
The `CHANGELOG.md` half of (iv) is BL-57's D8 (ii), pulled forward into #80 (this fork did the same at
`3c8acd5`); the `HANDOFFS.md` half goes past that plan, whose D7 left `HANDOFFS.md` to the operator. F4 —
two limits on `CHANGELOG.md` — goes with it as the review framed it; the seeds' prose still names 65,536 B
(`starter-kit/CHANGELOG.md:104`, `starter-kit/HANDOFFS.md:98` at `aa36fd8b`), which stays with BL-57's P2.

**What the branch holds.** `pr80/f3-read-set-token-ceilings`, from F2's `37740763`, one commit,
**`aa36fd8b`**, touching `.context-budget.json` and the branch's `CHANGELOG.md` only (its entry above F2's,
below `main`'s). Canonical-only: `bin/_manifest.py` ships the seed, not this file. The config was
hand-edited to keep its layout, by a script that asserted every touched line and checked the result
against `HEAD` key by key; then the edited file itself was re-run through `--status` (exit 0 on both
trees), `--json` and `--selftest` (exit 0) and the six commits — the same as R1 L1's row above.

**Verified**, in `--no-local` clones, every exit code read bare:

| | `37740763` (control) | `aa36fd8b` |
|---|---|---|
| `bin/tests.sh` | 115 / 1, exit 1 (Test 9) | 115 / 1, exit 1 (Test 9) — 116 rows, 0 status flips, 0 rows differing |
| unit suites | 211 · 123 (2 skipped) · 116 (2 skipped) OK | the same |
| `bin/check-links` | OK, 105 links / 23 files | OK, 105 links / 23 files |
| `bin/check-learnings` | OK, 13 rows | OK, 13 rows |

`git merge-tree --write-tree --name-only upstream/main aa36fd8b`: no conflicts. `read-set-budgets`
(`d4e1570`) is an ancestor, so the push is a fast-forward and carries F2 with it.

**Prepared for the publish at S165, published at S166:** [`pr80-body-after-f3.md`](pr80-body-after-f3.md) — the
description with every figure re-derived at S165 (the head, 28 files +7,892 / −580, the headline table,
the pair paragraph, a paragraph on the config, the corpus 659,755 → 839,383 B, two verification rows),
each method first reproducing the figure it replaces; [`pr80-reply-f2-f3.md`](pr80-reply-f2-f3.md) — one
reply for F2 and F3.

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
