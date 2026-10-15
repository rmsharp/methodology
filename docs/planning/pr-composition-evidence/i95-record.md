# Upstream issue #95 against the pull request candidate: the record (S328, 2026-10-15)

The issue is <https://github.com/KJ5HST/methodology/issues/95>, "Fresh sync fails its own context budget", opened 2026-10-15 21:00Z by KJ5HST, 0 comments.
Backlog item: BL-114 in `docs/planning/BACKLOG.md`. This record is local; nothing is sent to `KJ5HST/methodology`, and no comment is made on the issue. Three trees are read, each pinned: upstream's `main` at
`f34769f`, this fork's `main` at `981c33a`, and the pull request candidate at `ced2c82` (the local ref `pr2/candidate`, the one pull request's branch).
Everything below is the output of a committed script, saved beside it: `i95-dayzero.py` (output `i95-dayzero-output.txt`), `i95-adopters.py`
(`i95-adopters-output.txt`) and `i95-compose.py` (`i95-compose-output.txt`), each run once, serially, with `python3 -I`.

## 1. The answer

1. **All four findings are real and reproduce byte for byte on all three trees.** The seeds are the same blobs on all three (`starter-kit/SESSION_NOTES.md` `63917c7`,
   `starter-kit/context-budget.json` `d0d363b`); `starter-kit/CLAUDE_TEMPLATE.md` differs (upstream `d9a111d`, fork and candidate `e0c35a8`) and fails the same way.
   The candidate fixes none of them and makes none worse. The issue's own control (line 5 wrapped, a second `## ` heading) passes on every tree. Every line citation in
   the issue checks out on `f34769f`. (§2)
2. **The issue's suggested fix 3, applied alone, does not make a fresh project green.** Fencing the template's `## Purpose` placeholder turns "the fence is missing" into
   "the fence block is only 182 B — it looks emptied", still exit 2, because the seed config's floor is 800 characters. The two ways out are the issue's own "alternatively"
   (the tool treats a still-placeholder purpose as unmeasured) or a placeholder of at least 800 characters, which costs +620 B in the template and lets a never-customised
   project pass the guard that exists to catch an emptied purpose. Which one is a design call for him. (§3.1)
3. **Measuring `max_line_bytes` in bytes changes no verdict at my 12 adopters:** 10 of 12 declare the cap (all on `SESSION_NOTES.md`), 0 lines pass today and would fail
   after the change. (§5)
4. **The issue's four changes, applied literally to upstream's tip, merge with the candidate** with two exceptions, both artefacts of placement and not of substance: the tool's
   `VERSION` line if both sides bump it, and the new unit-test class if it is appended at the end of `tools/test_context_budget.py`, where the candidate also appends. The
   change touches 5 files, 6 with the ledger entry the pre-commit hook requires, so it is two commits under the 5-file cap. (§4)
5. **Recommendation, not a decision:** do not fold it into the one pull request; the plan already lists the context-budget seed work as a separate decision
   (`docs/planning/upstream-pr-composition-plan.md:251-252`). The cheapest outward step, if he wants one, is a comment on #95 carrying §3's three verified facts, offered
   before any pull request. Every outward step is his go-ahead. (§6)

## 2. The four findings, reproduced (`i95-dayzero-output.txt`)

Run with the tool each tree ships (`python3 context_budget.py --status --json`, parsed), in a git-initialised directory holding that tree's `context_budget.py`, seed
`.context-budget.json` and the files named; exit codes are the tool's (0 clean, 1 warn or unmeasured, 2 over a hard ceiling).

| Case | upstream `f34769f` | fork `981c33a` | candidate `ced2c82` |
|---|---|---|---|
| seed `SESSION_NOTES.md` alone | exit 2: line 5 "317 B" over 280; `^## ` matched 1 of an expected 2 | same (`:46`) | same (`:94`) |
| `CLAUDE_TEMPLATE.md` as `CLAUDE.md` alone | exit 2: the `budget:protected` fence is missing | same (`:52`) | same (`:100`) |
| the issue's control | exit 1 (the absent files are unmeasured), `SESSION_NOTES.md` ok | same (`:57`) | same (`:105`) |
| the real route: `bin/sync` into an empty project, then the tool, with `CLAUDE.md` copied from the template | exit 2, all three findings together | same | same |

Finding 1 in numbers: the seed's line 5 is **317 characters and 321 bytes** (`i95-dayzero-output.txt:6`); the tool prints 317 and calls it B, which is finding 4.
The upstream tree prints `bin/sync` as having no `--layout` flag, so the new-layout rows exist for the fork and the candidate only.

## 3. What the issue does not say

1. **Suggested fix 3 is incomplete (§1 item 2).** `i95-dayzero-output.txt:22` (case `fenced`, the template's `## Purpose` body wrapped in the fence, nothing else): exit 2,
   "the budget:protected block is only 182 B — it looks emptied", on all three trees. `i95-compose-output.txt:93-95` shows it again through the pass-control the issue
   asks for: that test goes red on the unfixed seeds and **still red on the issue's fix applied literally**. `i95-compose-output.txt:100-102`: with the placeholder padded to
   801 characters it passes, at +620 B in the template.
2. **The fence floor has the same unit slip as the line cap.** `protected_min_bytes` is compared with `len(body.strip())`, characters, and the message prints "B"
   (`starter-kit/context_budget.py:453,455` on upstream, `:546,548` on the candidate; the open backlog item BL-84 in `docs/planning/BACKLOG.md` already records it for the
   fork). A bytes count is never smaller than a character count, so measuring bytes there can only move a file toward passing, never to failing. The issue names only the line cap
   (`:384`); a fix that changes one site and not the other leaves the unit inconsistent inside one function. My instrument changed both.
3. **A fresh `bin/sync --layout new` hides findings 1 and 2.** On the fork and the candidate (the only trees with the flag), `SESSION_NOTES.md` is installed under
   `methodology/` while the seed config's rows still name root paths, so the tool reads "unmeasured (file does not exist)"; the as-synced exit is 1, not 2, and with the template copied as `CLAUDE.md` it is 2 for finding 3 only
   (`i95-dayzero-output.txt:80-88` and `:128-136`). The migration tool rewrites those paths for an existing project (`docs/planning/methodology-subdirectory-plan.md:158`, row
   C9); a project that never migrated is a different case, and I found no record of it (greps for a fresh new-layout sync and for the seed config's paths over the plan, the
   findings register and `BACKLOG-DETAIL.md`: no hit). It exists only on the fork and the candidate, neither of which he has been sent, and it also means the pass-control he suggests would
   pass vacuously in the new layout: it has to run in the legacy layout.
4. **The suggested bytes expression and the exact count differ only on invalid UTF-8.** The tool decodes with replacement, so a stray byte `0xFF` is 1 byte raw, 1 character
   decoded and **3 bytes** re-encoded (`python3 -c` check, this session). At all 10 adopter files the two counts are equal (`i95-adopters-output.txt`, the `bytes` and `encode` columns).

## 4. What a fix touches and how it composes (`i95-compose-output.txt`)

The patch in `i95-compose.py` is a **measuring instrument, not a proposed fix**: the issue's four suggested changes as exact-string edits that refuse when an anchor is absent
or not unique, in a scratch repository. It is my reading of his suggestion, not his patch; his own will differ, so every conclusion here is an estimate of his.

| File | Edit |
|---|---|
| `starter-kit/SESSION_NOTES.md` | line 5 wrapped, a `## Session History` heading above the italic marker (+4 / -1) |
| `starter-kit/CLAUDE_TEMPLATE.md` | the `## Purpose` placeholder fenced (+2 / -0) |
| `starter-kit/context_budget.py` | the line cap and both fence-floor sites measured in bytes, the version bumped (+4 / -4) |
| `tools/test_context_budget.py` | a new unit class, red on the unfixed tool and green on the fixed one (`:91-92`) (+18 / -0) |
| `bin/tests.sh` | the pass-control, a fresh project with the untouched seeds (+12 / -0) |

**Merge against the candidate** (`git merge-tree --write-tree`, symmetric, so it answers "he fixes first, we rebase" and "we land first, he rebases" alike; `:6-9`):
the new unit class at the end of the test file: 1 conflict (that file), because the candidate also appends there; the class before an existing class: **clean**.
With the version bump on both sides: 1 conflict, the `VERSION` line (upstream's `1.3.2` against the candidate's `1.4.0` and the lines it inserts after it). The four
other files merge clean in all four variants, including `bin/tests.sh`, which the candidate changes in 18 hunks. **Fold test** (`:82-88`): every anchor exists exactly once
on the candidate itself and the same edits apply (+40 / -5 over five files).

**The cap.** 5 files edited plus the ledger entry `.githooks/pre-commit` requires is 6, over `SAFEGUARDS.md`'s 5 per commit, so a build is two commits (one possible split: the tool with its two
tests; the two seeds), each verified on its own when it is built.

## 5. The 12 adopters (`i95-adopters-output.txt`)

Read at each adopter's committed `HEAD` with `git show`, never from a working tree (an adopter's live session cannot move the numbers while the script runs). 10 of 12 declare `max_line_bytes`, all on
`SESSION_NOTES.md` (eight at 280, one at 2,000, one at 4,000); `dalia_martinez_funeral` declares none and `claude_work` has no commits. **0 lines would flip** from passing to
failing under a bytes count. The instrument is audited: for every file the tool's own `measure_file` (imported from the fork) reported the same "N line(s) exceed" count as the
script's character count, and the script stops on a mismatch. A side reading, not part of the question: three adopters already have 38 to 44 lines over their cap today
(`model_project_constructor` 41, `feedback-loop-comparison` 44, `wsfct` 38), so the cap is already red where it is declared.

## 6. Routes (his calls)

| Route | What it costs | Against it |
|---|---|---|
| **R1. A comment on #95**, offering a pull request and carrying §3.1, §3.2 and §3.3 | one outward action, text shown to him first | none beyond his time to read it |
| **R2. A separate small pull request** that fixes #95, after R1 or without it | 2 commits, 5 files; merges with the candidate in either order, apart from the version line | it is his own issue with his own suggested fix: a pull request next to his fix is duplicate effort unless he asks; and one more thing to review while #94 (10 days) and #92 (12 days) have 0 comments |
| **R3. Fold it into the one pull request** | a new commit on the candidate, then the text's figures and the 40-minute re-runs again | ties a fix he wants now to a review he has not begun; the plan lists this seed work as a separate decision |
| **R4. Wait** | nothing | if he fixes it first, the candidate's `VERSION` line conflicts and the candidate is rebased once |

Recommended: **R1 first, R2 only if he asks; not R3.** Because the work is fork-side first, the fork's own `main` takes the fix at the next resync from upstream whichever
route lands it.

## 7. What none of it shows

- **His actual fix.** The instrument is mine; his may touch other regions, and `main` may move before anything is sent (`f34769f` is the tip at this reading).
- **The full suite on the instrument.** Only the new unit class (red then green) and the extracted shell block were run, not `bash bin/tests.sh`.
- **Adopters' working trees,** and anyone's project that is not mine; the `--source github` route; Windows; a maintainer's machine.
- **Whether a project that never ran the migration tool is meant to be a supported day-zero case** (§3.3): that is a design question the candidate's plan did not answer in writing.

## 8. His calls this leaves

1. Whether to comment on #95 (R1), and the text if so (not drafted yet: it is shown to him before any post).
2. Whether the candidate should carry a fix for the new-layout day-zero case (§3.3), or whether a fresh project is expected to run the migration tool.
3. The design choice inside fix 3 (§3.1): a still-placeholder purpose as unmeasured, or a placeholder at the floor.
