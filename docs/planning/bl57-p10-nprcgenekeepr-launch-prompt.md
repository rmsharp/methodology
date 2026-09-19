# BL-57 P10 (`nprcgenekeepr`) — launch prompt

Fork-only, like the plan it serves ([`changelog-rules-contradictions-plan.md`](changelog-rules-contradictions-plan.md),
P10 row `:1062`). Written at S194 (2026-09-19). The operator pastes everything below the rule into a session run
**from `nprcgenekeepr`**; that session does the work, and S194 (or its successor) records it here when the report is
relayed, as S193 did for P9.

**How the facts were measured.** Read-only against `nprcgenekeepr` at `312996b0` (S718's last commit, clean apart from
untracked files that aren't this phase's), with `bin/status` and `bin/sync` from fork `main` `c20d6ab`
(`v3.7-963-gc20d6ab`). Everything that writes — the forced sync, the patch, the tool runs, a simulated backfill — ran in
a `--no-local` scratch clone, never in the project. **The route was decided by the operator at S194 (picker):** force
the sync, then re-apply the local extension in its own commit. The other three options, measured and not taken: seed
only (the new header's link would dangle, since `docs/methodology/FRAMEWORK_APPARATUS.md` is missing there);
force and drop the extension (`SESSION_NOTES.md` then reads `NO_CONFIG`, exit 3); settle BL-32 first (a design
session and an upstream PR before P10 could run).

**Correction, S194 close-out (the prompt below is left as it was sent):** fact 4 credits the rules block's move to
*"S700's and S710's trims"*. The shard holding it was written by S702's trim (`6bac092f`, 2026-09-17); S700 archived
`SESSION_NOTES.md`, and S710 trimmed `CHANGELOG.md` again later. P10's steps did not depend on which session it was.

---

**Task: BL-57 phase P10 — bring this project's `CHANGELOG.md` and `HANDOFFS.md` to the current methodology's ledger
rules, syncing the framework files on the way.** Run this project's own session: Phase 0 first (it will backfill
`312996b0`, S718's self-reconcile commit, into `CHANGELOG.md`), then claim, then the steps below. Reasoning: high. The
plan is `../methodology/docs/planning/changelog-rules-contradictions-plan.md`: the steps and DONE criteria for every
adopter at `:1011`, this project's row at `:1062`, the removed-lines check (§9.8) at `:1276`. Line numbers below were
read at `312996b0`; **re-derive each one at your claim**, because every prepended entry moves them.

**Decided before this session (the operator, 2026-09-19):** sync with `--force`, then re-apply this project's 49-line
`SESSION_NOTES.md` extension to `methodology_trim.py` in its own commit. Don't re-open that choice; if a fact below
turns out false, stop and report it instead.

**Measured facts (read-only, from `../methodology` at `c20d6ab`, in a scratch clone of this repo):**

1. **The sync.** `python3 ../methodology/bin/sync --dry-run .` exits 2 and refuses `methodology_trim.py`, locally
   modified: 49 added lines in two hunks (`_session_notes_date`, and the `"SESSION_NOTES.md": LedgerSpec(...)` entry),
   from `c75bb9da` (S518) and `9bfc8bb4` (S528) on top of the `18d8e3c7` sync. With `--force` the dry run exits 0 and
   lists 15 files: 13 written (`SESSION_RUNNER.md`, `FRAMEWORK_LEARNINGS.md`, `SAFEGUARDS.md`, `BOOTSTRAP.md`,
   `methodology_dashboard.py`, `methodology_trim.py`, `context_budget.py`, `quality_ratchet.py`,
   `docs/methodology/ITERATIVE_METHODOLOGY.md`, `docs/methodology/HOW_TO_USE.md`,
   `docs/methodology/FRAMEWORK_APPARATUS.md`, `docs/methodology/workstreams/DEVELOPMENT_WORKSTREAM.md`,
   `docs/methodology/workstreams/AUDIT_WORKSTREAM.md`) and 2 created (`.context-budget.json`, `.quality-gates.json`).
   The four seeds (`SESSION_NOTES.md`, `CHANGELOG.md`, `HANDOFFS.md`, `ROADMAP.md`) are left as they are.
2. **The extension survives a re-apply.** After the forced sync, `python3 methodology_trim.py --file SESSION_NOTES.md
   --check` answers `NO_CONFIG` (exit 3). The patch `git diff 18d8e3c7 HEAD -- methodology_trim.py` — **save it to a
   file before the sync overwrites the tool** — passes `git apply --check` onto trimmer 1.5.0. With it applied, `--check`
   reads all three ledgers, and a dry run `--file SESSION_NOTES.md --cut 1 --force` prints the same as the old 1.1.2
   copy: `L1_OK`, `L2_OK`, `L3_OK`, 19 records, 18 would be archived, 70,138 B → 3,979 B. (Both versions first refused
   with `P1_UNDOCUMENTED` until `312996b0` was backfilled; that backfill is your Phase 0's.) The file stays locally
   modified, so every later sync refuses it again until the framework settles BL-32; this project's `CLAUDE.md:277`
   already prescribes the re-add.
3. **1.1.2 → 1.5.0 changes when a trim fires.** The byte budget goes from 65,536 B to 196,608 B, and the line-headroom
   trigger is gone. At `312996b0` `SESSION_NOTES.md` (70,138 B) fires under 1.1.2 and not under 1.5.0. Adding
   `--budget-bytes 65536` restores the old verdict on all three ledgers (`SESSION_NOTES.md` fires; `HANDOFFS.md`
   56,781 B and `CHANGELOG.md` 37,090 B don't). Whether to keep the old cadence is this project's call; if you keep it,
   record it in `CLAUDE.md`.
4. **`CHANGELOG.md`** is 37,090 B and 491 lines, with 35 `### ` lines. 22 of them match the anchored audit
   (`grep -cE '^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[(issue #[0-9]+|BL-[^]]+|ad hoc)\]' CHANGELOG.md`): 19 `[ad hoc]`, 2
   `[BL-Up-Next]`, 1 `[issue #148]`. The other 13 use a bare `[BL]`, which that audit doesn't match. Its only `## `
   headings are `## 2026-08` (`:17`, empty) above `## 2026-09` (`:19`), then two trimmer pointer blocks, then entries.
   **The rules block the plan row names (`:3946`–`:4065`, measured 2026-09-14) is no longer in the live file:** S700's
   and S710's trims moved it into the frozen shard `docs/archive/CHANGELOG-through-2026-09-17.md` (`## How to add an
   entry` at `:4171`). Shards are frozen, so leave it there. Step 3 for this file is therefore a pure insertion, as
   P9 did in `mts-system`.
5. **`HANDOFFS.md`** reads *present (stale format)* in `bin/status`. It holds an older copy of `## Size, and when to
   archive` at `:62`–`:117` (a blank `:118`, then the first pointer block at `:119`); 28 lines differ from the current
   seed's section. Everything else stays byte-identical: the four-backtick worked example at `:31`–`:55` (its
   `handoff` fence at `:32` is not a receipt), the pointer blocks at `:119`–`:145`, and the *"This file currently holds
   **2** receipt(s)"* sentence at `:135` (the trimmer's regenerated field). The first real receipt opens at `:146`.
6. **The R build (the plan's item (25)).** Six root files match no `.Rbuildignore` pattern: `context_budget.py`,
   `quality_ratchet.py`, `.context-budget.json`, `.quality-gates.json` (the sync installs them), and
   `.context-budget-history.jsonl`, `.quality-gates-results.json` (written when `context_budget.py --status` and
   `quality_ratchet.py --run` run). `docs/methodology/FRAMEWORK_APPARATUS.md` is covered by `^docs$`, and the files
   already installed are covered by their own patterns. Expected, not run: `R CMD check` notes them as non-standard or
   hidden top-level files.
7. **Ignores (item (29)).** After both tools ran in the scratch clone, `.context-budget-history.jsonl` and
   `.quality-gates-results.json` showed as untracked, not ignored. The methodology repo ignores the results file and
   tracks the history on purpose; here it is your call.
8. **`CLAUDE.md`.** `:271` (S325, *"freeze legacy, go forward"*), `:273` and `:275` (S546/S547's relocation) hold the
   ledger's legacy history. `:277` says `methodology_trim.py` *"is not actually part of real upstream
   `KJ5HST/methodology`"*: that held for every tag through v3.7, but `upstream/main` now distributes it
   (`bin/_manifest.py:45`). The build equivalent is at `:114`–`:115` (`devtools::check()`, `devtools::test()`).
9. **No git hooks here** (`core.hooksPath` is unset), so nothing enforces an entry per commit; each commit still
   carries its own `CHANGELOG.md` entry.

**Steps** (the plan's `:1011`, with this project's specifics):

1. **Measure again.** Save the patch (fact 2). Run `python3 ../methodology/bin/status .` and `python3
   ../methodology/bin/sync --dry-run --force .`, and compare them with facts 1 and 5. Note the source version the sync
   prints.
2. **Build and ignore files first, one commit** (items (25) and (29)), so no commit ships the new files into the
   package build: `.Rbuildignore` patterns for the six files in fact 6, and whatever `.gitignore` treatment you choose
   for the two tool outputs.
3. **The sync, one commit** (item (18)): `python3 ../methodology/bin/sync --force .`, then commit exactly the files
   the dry run listed, plus that commit's entry, and nothing else.
4. **Re-apply the extension, its own commit:** `git apply` the saved patch. Then `--check` on `SESSION_NOTES.md` must
   not say `NO_CONFIG`, and its dry run must print `L1_OK`–`L3_OK`.
5. **`CHANGELOG.md`, its own commit:** insert the current seed's pointer-and-marker paragraph
   (`../methodology/starter-kit/CHANGELOG.md:10`–`:12`, from *"**The rules** — how to add an entry"* to *"ledger-format:
   2 — keep this marker; `bin/status` reads it."*) after the intro and its Note (`:1`–`:15`), before `## 2026-08`. No
   other line changes.
6. **`HANDOFFS.md`, its own commit:** replace `:62`–`:117` with the current seed's `## Size, and when to archive`
   section (`../methodology/starter-kit/HANDOFFS.md:89`–`:148`; its `:91` is the `handoffs-format: 2` marker). Keep
   everything in fact 5.
7. **`CLAUDE.md`** (step 4): bring `:277` up to date with fact 8, and record the ledger's legacy forms as adaptations:
   the bare `[BL]` tag, and the empty `## 2026-08` sitting above `## 2026-09`. Record the `--budget-bytes` choice here
   too, if you made one.
8. **Verify** (the plan's DONE list, `:1011`): `bin/status` reads `present` for `CHANGELOG.md` and `HANDOFFS.md`.
   §9.8 (copy the script from `:1276`) prints *only the block changed* on the step 6 commit with bounds `62 117
   HANDOFFS.md`; that removes lines, so it can fail. On the step 5 commit it is an insertion, so check it with
   `git diff --numstat` (0 deletions) and that every old line survives in order. The trimmer's dry run (`--cut 1
   --force`, no `--write`) prints `L1_OK`–`L3_OK` on `CHANGELOG.md` and `HANDOFFS.md`. The package's own check or tests
   still pass.
9. **Predicted counts, measured from your claim commit:** `grep -c '^### ' CHANGELOG.md` rises by exactly the number
   of entries this phase adds (the step 5 commit: +1, its own entry). Nothing leaves the file. The anchored audit rises
   by those entries that use `[ad hoc]`, `[BL-<id>]` or `[issue #<N>]`, and by none that use a bare `[BL]`.
10. **Close out** in this project. Don't push; that is this project's go-ahead.

**Report back, for the recording session in the methodology fork:** the commit list with shas; `bin/status` before and
after; the sync's printed source version; the `### ` and audit counts at claim and close-out; each §9.8 output and the
numstat check; each trimmer dry run; the check or test result; and every place a fact above turned out different.
