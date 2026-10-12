# BL-105 build phase 3 — the distributed prose (S304, 2026-10-12)

Plan [`methodology-subdirectory-plan.md`](../methodology-subdirectory-plan.md) D10; backlog row BL-105 ([`BACKLOG.md`](../BACKLOG.md), [detail](../BACKLOG-DETAIL.md#bl-105)); the contract is the rehearsal record's section 7 item 2 ([`bl105-rehearsal-record.md`](bl105-rehearsal-record.md)); the tool is [`bl105-phase2-record.md`](bl105-phase2-record.md). Written after the work; every figure was read from a command's output in this session.

## 1. The answer first

**Done, on the fork only (nothing sent to `KJ5HST/methodology`, no adopter's tree touched):** the three distributed texts that place `PROJECT_LEARNINGS.md` now hold in both layouts, and `bin/check-links` allows the file where the layout keeps it. **One more fact the phase did not plan for:** the line in `bin/check-links` was not only a comment. It put the file among the project's files "at its root in either layout" and allowed it absent at the root only, so a link to it from a distributed document in the new layout would have read as dangling. That is now code, held by a test written first.

**Held by:** one new test, red first (`4ea9ce9`, failing at the new-layout sibling link: exit 1, not 0), green with the fix (`fce5c67`); `tools/test_sync_layouts.py` reads **82 tests OK** (81 before; gate floor `sync-layout-unit-tests` 81 to 82); **9 mutants of the new code, 9 killed** ([`mutate-bl105-phase3.py`](mutate-bl105-phase3.py), which refuses any path outside `~/.cache`); the gate run in a clean `--no-local` clone of `69fe69a`: **18/18 pass · 0 fail · 0 unmeasured · results `0ca51b2444cc` · manifest `5ba29f982c78`**.

## 2. The inventory, and what each site became

`git grep -n PROJECT_LEARNINGS` over the tree (frozen evidence, archives and the ledgers excluded) finds the six sites of the plan and four that are history or a comment. The prose edits keep every line count (the edit script asserted each file's newline count equal before and after), because frozen plans cite these files by line.

| Site | Before | After | Why |
|---|---|---|---|
| `starter-kit/BOOTSTRAP.md:218` | "at your project root" | "beside `FRAMEWORK_LEARNINGS.md` (your project root, or `methodology/` if your project uses that layout)", and the pointer "names the file where it lives (`methodology/PROJECT_LEARNINGS.md` in that layout)" | false in the new layout |
| `BOOTSTRAP.md:220` | the pointer quoted with the bare name | **unchanged** | bare names are the rule (`BOOTSTRAP.md:68`); the sentence before the quote now says to name the path |
| `BOOTSTRAP.md:222` | "needs no tooling changes" | "needs no tooling of yours: if your project later moves to the `methodology/` layout, `bin/migrate-layout` moves it with the methodology files (when git tracks it) and rewrites the pointer in `CLAUDE.md`" | the tool now acts on it; both halves have a test (`test_the_claude_md_pointer_the_budget_path_and_the_gate_command_follow`, `test_a_copy_git_does_not_track_stays_and_is_named`) |
| `BOOTSTRAP.md:439` | a table row naming it bare, "see Step 5" | **unchanged** | a bare name that points at Step 5, which now says where |
| `starter-kit/CLAUDE_TEMPLATE.md:83-84` | "at the project root" | "beside FRAMEWORK_LEARNINGS.md (in methodology/ if your methodology files are there)" | false in the new layout; the template's own line 10 uses the same idiom |
| `bin/check-links:80-120` | `PROJECT_LEARNINGS.md` in `ADOPTER_LOCAL_FILES` | `COMPANION_FILES`, `COMPANION_NEIGHBOUR`, `beside_in`, `companions_in`; `placeholder_in` now calls the one helper | the file is allowed absent beside `FRAMEWORK_LEARNINGS.md` in each layout and not at the root of the new one |

**Not edited, by design:** `README.md:651`, `docs/RELEASE_HISTORY.md:38` and `docs/versioning-archive.md:25` (the v2.6.1 history, which says what v2.6.1 did); `.context-budget.json:42` (this repository's own comment, which names the file generally and is still true). **Two sites of the plan left as they were (`BOOTSTRAP.md:220` and `:439`)** are a judgement, his to overrule: each is a bare name under a rule the guide states, so an edit would add words where the rule already covers them. If he wants them to say "beside `FRAMEWORK_LEARNINGS.md`" too, each is a one-line edit.

## 3. Sync channels and the adopters' cost (scratch projects under `~/.cache/s304-sim`)

- **`bin/sync` from `69fe69a`, legacy and `--layout new`:** both exit 0; `BOOTSTRAP.md` and `CLAUDE_TEMPLATE.md` land **byte-identical** to `starter-kit/` (`cmp`); `check-links --tree` passes on each tree (80 links, 23 files).
- **A project synced at `fce5c67`, read by `69fe69a`'s `bin/status`:** exactly two rows are not current, `BOOTSTRAP.md` and `CLAUDE_TEMPLATE.md`, **1 version behind** each; the dry run of `bin/sync` writes exactly those two, 21 files read `unchanged` and 7 seeds `present (left as-is)`. **That is the whole adopter cost:** two documents on the next `bin/sync`; no tool, config or behavior changes (`bin/check-links` is canonical-only).
- **`--source=github`:** reads upstream's `main`, so an adopter gets the new text only after a pull request merges; not simulated beyond that statement.
- **The resync:** `upstream/main` is an ancestor of `HEAD` (0 behind), and `git merge-tree --write-tree upstream/main HEAD` exits 0. **Open pull requests:** the heads of #94 and #92 each conflict with this repository's `main` (`.quality-gates.json`, `starter-kit/methodology_trim.py`, `tools/test_methodology_trim.py` for #94; `CLAUDE.md` for #92) and **the conflicted files are the same set at `2c62927`**, the commit before this phase: this phase adds none. The set matters to whoever composes the one pull request; it is not a defect of this phase.

## 4. What was not run

GitHub CI; `bin/sync --source=github` against a merged change (there is none); a fresh agent reading the new paragraph (nothing here measures whether it is read as intended); the adopters' own live trees (none was touched). No test pins the prose: the facts it states are held where they are true (the tool's tests, the check-links test), and a test of wording would fail on the next edit that changes no meaning.

## 5. Found on the way

- **S303's receipt `commit:` slot read `6583022`, all decimal digits, which `bin/check-handoff` does not accept as a sha**; it is exempt while the receipt is the newest and red once the next claim stub is. Reconciled in its own commit (`3fae110`, to `65830220967e`, the same commit), as S254 did for S253 (`d45afa4`). The checker that found it is the guard; nothing further was built.
- **The gate's 600 s limit bit again (BL-103):** the first gate run at `2c62927` read 17/18 with `migrate-layout-unit-tests` unmeasured (exit 127 is `TimeoutExpired`) under a load average of about 180 from other sessions' work; by hand the suite read 275 tests OK in 675.9 s. The run at `69fe69a`, at a load of 10, read 18/18.

## 6. His calls this leaves

- **The two bare-name sites** (`BOOTSTRAP.md:220` and `:439`): leave, or add "beside `FRAMEWORK_LEARNINGS.md`".
- **The pull request:** this change is one of the fork's distributed edits that wait for the one vetted pull request (D8); nothing is sent, and when it is composed the conflicts of #94 and #92 with `main` (section 3) need a decision first.
- **Phase 4 (the adopters):** unchanged by this phase; each adopter's hand edits first, in its own commit.
