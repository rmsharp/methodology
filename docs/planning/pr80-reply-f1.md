**F1 — (a), done.** Two commits on `read-set-budgets`, on top of your `b82dcff`:

- **`5c9f0f3`** first repairs every citation the cut would leave dangling, stating the rule instead of
  the number: `starter-kit/context_budget.py:77` and `:378` (Learning #34) and `:409` (*"learning #22 /
  #26a"* — this table has no `#26a`, so that pair cited another numbering), plus five comments and
  docstrings in the two canonical-only test files. `bin/check-learnings` sweeps only the distributed **Markdown**
  (`distributed_md_files`), so the two `context_budget.py` citations would have dangled in every adopter
  with the check green. That scope is probably worth its own follow-up, since `context_budget.py` is
  distributed and invisible to it.
- **`d4e1570`** cuts `starter-kit/FRAMEWORK_LEARNINGS.md` to rows 1–13 plus the reserved `#14`
  (56,673 → 13,983 B). Rows 1–13 are byte-identical; the `#14` callout is reworded because there is no
  row 15 now, and `bin/check-learnings`' comment quoting it follows.

Both ledger entries sit with #80's own, below `main`'s, so `git merge-tree --write-tree --name-only
origin/main origin/read-set-budgets` is still empty (against `9fa3141`).

Verified in clones, each exit code read bare: `bin/tests.sh` **115 / 1** at `b82dcff`, `5c9f0f3` and
`d4e1570` — 116 rows each, zero status flips, the failure Test 9 as before; unit suites 116 + 211 + 123
OK at all three; `bin/check-links` OK (105 links, 23 files); `bin/check-learnings` *"13 Learning
row(s), contiguous 1..13; all citations resolve"*, and a `Learning #20` planted in
`starter-kit/SAFEGUARDS.md` is caught. The description now matches: the head, the corpus total
(658,788 → 838,416 B, +179,628), the two table rows that moved, and a verification row.

F2 and F3 next, each its own commit. F4 — the two `CHANGELOG.md` limits — is one of several
contradictions in the ledger rules that I have a plan for; it will come as its own PR after this one
merges. F5 and F6 can follow.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
