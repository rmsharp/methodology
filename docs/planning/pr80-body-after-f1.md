**Base `main`, head `read-set-budgets` (`d4e1570`).** This merges the four PRs already staged on
that branch — #76, #77, #78, #79 — plus your merge of `main` into it (`b82dcff`) and the two commits
that answer your review's F1 (`5c9f0f3`, `d4e1570`). `git merge-tree` against `main` (`9fa3141`)
reports no conflicts. 28 files, +7,795 / −554.

## The number this is about

`SESSION_RUNNER.md` Phase 0 orders every session to read `SAFEGUARDS.md` *"in full, not skimmed"*
and to follow the runner *"step by step"*. On `main` that pair **does not fit in one agent read**,
and the failure is silent: the agent reads a window, infers the rest, and its inferences get
written back into the highest-authority file. That is failure mode #28, which this repository
documents and, on `main` today, exhibits.

| the Phase 0 pair | bytes | tokens | of the 25,000-token read cap |
|---|---:|---:|---:|
| `main` today | 80,526 | **28,234** | 112.9% — **refused** |
| with this merge | 67,581 | **23,902** | **95.6% — fits, 1,098 tokens spare** |

**Both token figures are measured, not derived from an assumed density.** Concatenate the two
files, double the result, ask the agent to read it, and halve the count its refusal reports — a
refused read returns no content, so the measurement costs nothing:

```sh
git show <ref>:starter-kit/SESSION_RUNNER.md  > /tmp/pair.txt
git show <ref>:starter-kit/SAFEGUARDS.md     >> /tmp/pair.txt
cat /tmp/pair.txt /tmp/pair.txt > /tmp/pair2.txt   # then Read /tmp/pair2.txt and halve
```

`main`'s doubled pair reports 56,469 tokens → **28,234**; read undoubled it reports **28,237**, so
the method reproduces itself to 3 tokens. This branch's doubled pair reports 47,805 → **23,902**.
At the conservative 2.27 B/token floor the pair still reads over (29,772 tokens); **at every
measured density it fits, and on `main` it fits at neither.** That is the honest form of the
claim, and it is the reason to merge.

**The bytes moved; they were not deleted.**

- `starter-kit/SESSION_RUNNER.md` **65,140 → 52,195 B**. Its 13 inline learnings are now rows
  #1–#13 of `starter-kit/FRAMEWORK_LEARNINGS.md`, distributed to adopters (#76). **Eleven of the
  thirteen are byte-identical; rows #12 and #13 are shortened, and that is the one place this PR
  changes wording rather than location** — 2,400 → 1,450 B and 1,572 → 1,446 B, −1,076 B in total.
  The reason is in the same PR: `bin/check-learnings` gains `ROW_BUDGET_BYTES = 1500` (`:106`,
  a constant `main` does not have), and your #12 and #13 are the two rows that breach it. Both now
  pass. Every other row arrives at its exact current bytes. **The file holds those 13 rows and the
  reserved `#14`, nothing else** — #76 had also carried the contributor fork's rows #15–#47, and your
  review's F1 took them out (`d4e1570`).
- `ITERATIVE_METHODOLOGY.md` **68,247 → 55,976 B**. Its tables, tests and scoring scales are now
  `FRAMEWORK_APPARATUS.md`, also distributed (#78).

## What it fixes the same day it merges

**`bin/sync --source=github` installs nothing today.** Of `bin/_manifest.py`'s **27 SOURCE** paths,
**3 are absent from `main`** — `starter-kit/FRAMEWORK_LEARNINGS.md`,
`starter-kit/methodology_trim.py`, `FRAMEWORK_APPARATUS.md`. `read_github` (`bin/sync:80`) calls
`gh api repos/KJ5HST/methodology/contents/<src>` with no ref, so it reads the default branch; a
404 on any one source hits `sys.exit` at `bin/sync:89`. The read loop at `bin/sync:217-226` fills
`entries` for **every** row before the first `write_bytes` (`:164`, `:180`), so the exit lands
during the read pass and **not one file is written** — a partial install is not the failure mode;
a total one is.

**0 of 27 are absent from this branch.** Merging it is what makes `--source=github` work, and it
is also what turns this repository's own suite green (below).

## What an adopter's tree gets on its next `bin/sync`

14 of 27 manifest rows change. The corpus grows **658,788 → 838,416 B (+179,628)** — stated first
because it is the number a reviewer will find on their own. Almost all of it is the trimmer and
the two extracted siblings, all three **read on demand**; what shrinks is the part read **every
session**.

| | source | adopter destination | before | after |
|---|---|---|---:|---:|
| tracked | `starter-kit/SESSION_RUNNER.md` | `SESSION_RUNNER.md` | 65,140 | **52,195** (−12,945) |
| tracked | `starter-kit/FRAMEWORK_LEARNINGS.md` | `FRAMEWORK_LEARNINGS.md` | absent | **13,983** (new) |
| tracked | `starter-kit/methodology_trim.py` | `methodology_trim.py` | absent | **113,629** (new) |
| tracked | `FRAMEWORK_APPARATUS.md` | `docs/methodology/FRAMEWORK_APPARATUS.md` | absent | **15,493** (new) |
| tracked | `ITERATIVE_METHODOLOGY.md` | `docs/methodology/ITERATIVE_METHODOLOGY.md` | 68,247 | **55,976** (−12,271) |
| tracked | `starter-kit/context_budget.py` | `context_budget.py` | 29,549 | 73,009 (+43,460) |
| tracked | `starter-kit/methodology_dashboard.py` | `methodology_dashboard.py` | 161,753 | 162,537 (+784) |
| tracked | `starter-kit/BOOTSTRAP.md` | `BOOTSTRAP.md` | 27,748 | 28,211 (+463) |
| tracked | `starter-kit/CLAUDE_TEMPLATE.md` | `CLAUDE_TEMPLATE.md` | 3,079 | 3,137 (+58) |
| tracked | `HOW_TO_USE.md` | `docs/methodology/HOW_TO_USE.md` | 55,352 | 55,528 (+176) |
| tracked | `workstreams/AUDIT_WORKSTREAM.md` | `…/AUDIT_WORKSTREAM.md` | 13,536 | 13,529 (−7) |
| seed | `starter-kit/CHANGELOG.md` | `CHANGELOG.md` | 3,622 | 12,893 (+9,271) |
| seed | `starter-kit/HANDOFFS.md` | `HANDOFFS.md` | 5,314 | 11,442 (+6,128) |
| seed | `starter-kit/context-budget.json` | `.context-budget.json` | 4,360 | 5,766 (+1,406) |

The three **seed** rows are adopter-owned: `bin/sync` never overwrites an existing one, so an
established adopter sees no change there and a new bootstrap gets the fuller template.

## Verification

`bash bin/tests.sh`, each exit code read bare on its own line, in detached worktrees:

| tree | result | exit |
|---|---|---:|
| `main` (`512c2ed`), pristine control | **114 passed / 0 failed** | 0 |
| `read-set-budgets` (`598c459`) | **115 passed / 1 failed** | 1 |
| `read-set-budgets` (`d4e1570`), after F1 | **115 passed / 1 failed** | 1 |

**Row-for-row by normalised assertion label: 111 shared rows, zero status flips.** The suite gains
two genuinely new assertions — `ledger trimmer unit tests green` (#77) and `context budget gate
unit tests green` (#79) — and three rows differ only because the label states a count or an
outcome the change itself moves: `all 24 manifest files present` → `all 27`,
`status: one row per manifest file (24 == 24)` → `(27 == 27)`, and
`github source dry-run works` → `failed`.

## The one failing test — and why merging this PR is what fixes it

That third row **is** the single failure, and it is not a defect this branch introduces. Test 9
runs `bin/sync --source=github`, which reads `KJ5HST/methodology`'s **default branch**. The branch
declares 27 manifest sources; three of them exist only here, on `read-set-budgets`. So the branch
fails a test **about `main`'s contents**, and the merge is the only thing that can flip it. Run the
same suite after this merges and the row returns to `github source dry-run works`.

## What this does not do, and does not claim

- **It ships no enforcement.** `.githooks/pre-commit` is **byte-identical on both sides** — this PR
  does not touch it — and `.githooks/` appears in no manifest row, so no adopter receives it.
  `core.hooksPath` is local git config that never travels in a clone, and this repository has no
  `.github/workflows`. A framework author on a fresh clone has **no gate — not a weakened one,
  none.** `context_budget.py --precommit` exists and is wired to nothing; running it is a choice.
- **The procedure still never mentions the gate.** `grep -n context_budget
  starter-kit/SESSION_RUNNER.md starter-kit/SAFEGUARDS.md` returns **0 hits on this branch**,
  exactly as on `main`. Closing that gap means editing Phase 0, which grows the very file this PR
  shrinks — deliberately left as your call rather than smuggled in here.
- **It does not bring the fork's `main` across.** As of 2026-09-09 `rmsharp/methodology` is 590
  commits ahead of this branch, and 5 of the 27 distributed sources have drifted further there since #79 merged
  (`SESSION_RUNNER.md`, `FRAMEWORK_LEARNINGS.md`, `BOOTSTRAP.md`, `methodology_dashboard.py`,
  `HOW_TO_USE.md`). Those are later PRs, if you want them at all. **This is scoped, not
  "merge the fork."**
- **It claims no version.** `README.md` and `CLAUDE.md` say v3.7 on both sides and the branch adds
  no release entry. See below.

## The version call is yours

Your own precedent is a **separate release PR** — v3.7 shipped as
[#74](https://github.com/KJ5HST/methodology/pull/74) from `release/v3.7`, after the feature PRs it
covered. Merging this unversioned and cutting v3.8 separately (or not at all) matches that pattern
and is what the branch is built for. Nothing here forces the choice.

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_0193vQmoYCLGUYwRpcniWkZi

