# BL-57 P11 (`model_project_constructor`) — launch prompt

Fork-only, like the plan it serves ([`changelog-rules-contradictions-plan.md`](changelog-rules-contradictions-plan.md),
P11 row `:1138` on fork `main` at this file's commit). Written at S195 (2026-09-19). The operator pastes everything below
the rule into a session run **from `model_project_constructor`**; that session does the work, and S195 (or its
successor) records it here when the report is relayed, as S194 did for P10.

**How the facts were measured.** Read-only against `model_project_constructor` at `a18706f` (its Session 258's
close-out, clean), with `bin/status` and `bin/sync` from fork `main` `25249d7` (`v3.7-971-g25249d7`). Everything that
writes — the forced sync, the ledger edits, every synced tool's first run, the project's test suite and ledger proofs —
ran in a `--no-local` scratch clone with no `core.hooksPath`, never in the project. **Decided by the operator at S195
(picker), from options each run there first:** (a) move the runner's task-to-workstream rows and its *Wiki sync*
paragraph into `CLAUDE.md`, and retire its step 5; (b) adopt the ledger rules going forward, cadence included. Not
taken for (a): move all three verbatim, which leaves step 5 forbidding a file every sync installs. Not taken for (b): the
new format with the old cadence, and pointer-only with everything kept; both would need `CLAUDE.md` to override the
runner's Phase 0 step 6 and Phase 3F, which name one opt-out only (delete the file and record it).

**Corrections, made at the recording (the prompt below is left as it was sent).** Three facts measured differently in
Session 259, none of which changed a step. **Fact 6** overstated the trim: it would archive **143** of the 156 legacy
entries, back to **2026-04-16**, not all 156 back to 2026-04-10 — a standalone `---` zones the last 13 as the footer,
which a trim never moves — and it also emits `CUT_STRADDLES_DAY`. Re-measured here by writing the trim in a scratch
clone; plan item (34) carries the corrected figures. **Facts 9 and 10** name `context_budget.py --status`; that command
does not exist, and the tool ignores the unknown argument and performs its default run (BL-75). **Fact 4** says that
project's `docs/methodology/README.md` dates from its first commit `ff0228e`: it was added there and last updated
2026-06-01 (`5c37d2b`) to the canonical 2026-05-25 version (BL-74).

---

**Task: BL-57 phase P11 — bring this project's `CHANGELOG.md` to the current methodology's ledger rules, syncing the
framework files on the way, and move this project's customizations out of the synced runner first.** Run this project's
own session: Phase 0 and the claim under the runner you have now, then the steps below. Reasoning: high. The plan is
`../methodology/docs/planning/changelog-rules-contradictions-plan.md` (fork `main`): the steps for every adopter at
`:1086`, the DONE list at `:1111`, this project's row at `:1138`, the removed-lines check (§9.8) at `:1351`, and what
the measurement found at items (32)–(34) (`:512`–`:529`). Line numbers in this project were read at `a18706f`;
**re-derive each one at your claim.**

**Decided before this session (the operator, 2026-09-19).** Don't re-open these; if a fact below turns out false, stop
and report it instead.
- **(a)** The seven task-to-workstream rows and the *Wiki sync* paragraph move into `CLAUDE.md`. Step 5's *"run the
  shared dashboard … do not create a copy in this repo"* is retired: the sync installs `methodology_dashboard.py` at the
  root, every later sync rewrites it, and your `CLAUDE.md:10` already says to run it.
- **(b)** From this session on, every action gets a tagged entry, `### YYYY-MM-DD · [tag] …`, under a `## YYYY-MM`
  heading above `## [0.3.0]`, newest on top. The 156 existing entries stay byte-identical, where they are, as legacy.
  This supersedes the cadence in `docs/methodology/PROJECT_CONVENTIONS.md` §2, including its two rulings marked SETTLED
  (2026-08-17 and 2026-08-25).

**Measured facts:**

1. **The sync.** `python3 ../methodology/bin/sync --dry-run .` exits 2, refusing `SESSION_RUNNER.md` and
   `SAFEGUARDS.md`. With `--force` the dry run exits 0 and writes 26 files. 11 at the root: `SESSION_RUNNER.md`,
   `SAFEGUARDS.md`, and nine new files (`FRAMEWORK_LEARNINGS.md`, `RECOMMENDED_SKILLS.md`, `CONTEXT_TEMPLATE.md`,
   `CLAUDE_TEMPLATE.md`, `BOOTSTRAP.md`, `methodology_dashboard.py`, `methodology_trim.py`, `context_budget.py`,
   `quality_ratchet.py`). 12 under `docs/methodology/`: `ITERATIVE_METHODOLOGY.md`, `HOW_TO_USE.md`, the nine workstream
   and campaign files, and the new `FRAMEWORK_APPARATUS.md`. 3 seeds created: `HANDOFFS.md`, `.context-budget.json`,
   `.quality-gates.json`. `SESSION_NOTES.md`, `CHANGELOG.md` and `ROADMAP.md` are left as they are.
2. **`SAFEGUARDS.md` holds no local edit** (the plan's item (32)). It is byte-identical to a canonical version from the
   methodology fork's pre-rebase history (blob `6ba2c156`, commit `b91ac8c`, 2026-04-10). The sync can't see that
   history, so it calls the file modified. Nothing in it needs preserving. **`SESSION_RUNNER.md`** is that same
   version plus exactly three edits of yours: step 5 (`:17`), the task table's seven rows in place of four canonical
   ones (`:48`–`:54`), and the *Wiki sync* paragraph (`:209`). Its path, `docs/wiki/claims-model-starter/`, is the old
   one; your `CLAUDE.md:73`–`:75` corrects it. Every other differing line is canonical text.
3. **`CLAUDE.md` sites** (`a18706f`): `:10` names `methodology_dashboard.py`; `:59` calls the runner *"customized Phase
   1 mapping for this project"*; `:71` is the attribution bullet; `:73`–`:75` is the *":209 names the OLD wiki
   directory"* bullet, which the sync makes moot; `:92`–`:94` *Additional Phase 0 steps* and `:96`–`:98` *Additional
   task-to-workstream mappings*, both `(none)`; `:102` says base learnings *"remain in `SESSION_RUNNER.md`"*, and after
   the sync they are in `FRAMEWORK_LEARNINGS.md`. **`:90`'s *"Step 14"* and *"Step 18"* still hold:** the new runner's
   lines 14 and 18 are the same two steps, and step 6 now adds the ledger reconcile.
4. **Attribution.** `NOTICE` §1 and `CLAUDE.md:71` list the methodology material: the runner, `SAFEGUARDS.md`,
   *"`docs/methodology/` (12 files)"* (`ITERATIVE_METHODOLOGY.md`, `HOW_TO_USE.md`, `README.md`, which is the methodology's
   own README from your first commit `ff0228e`, and the nine workstream files), and two more. The sync adds
   `FRAMEWORK_APPARATUS.md` (so 13) and the nine new root files, plus three seeds it writes from the methodology's
   templates. Those two lists are how this project keeps the author's copyright notice with the material (MIT's one
   condition), so both should name the new files.
5. **`CHANGELOG.md`** is 671,658 B and 1,715 lines. It has 156 `### ` lines: 144 `### YYYY-MM-DD — …` and 12 older
   `### <phase> — … — <date>` (`:1606`–`:1696`). None matches the anchored audit
   `^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \[(issue #[0-9]+|BL-[^]]+|ad hoc)\]`. Its `## ` headings: `:16` `## [0.3.0] -
   2026-07-27`, `:624`, `:954`, `:1602`, `:1702`. Header: title `:1`; the per-file opener `:3`, which your §2 requires, so
   keep it; **`:5`–`:6`, *"All notable changes …"* and *"Format loosely follows Keep a Changelog"*, is the block**; `:8`,
   `:10` and `:12` stay; `:14` is `---`. Your `BACKLOG.md:569` item records that four older entries (`:20`, `:31`,
   `:41`, `:51`) sit above the newest (`:63`). Under (b) new entries go above all of them, so that item's placement
   sentence is superseded; its reorder question is not part of P11.
6. **The trimmer and this ledger** (item (34)). Today `methodology_trim.py --check --file CHANGELOG.md` refuses with
   `GRAMMAR_MISMATCH`. Once tagged entries sit above the legacy, it reads all 156 legacy entries as the body of the
   oldest tagged record. At one record it fires and archives nothing. At three, its dry run would archive *"1 of 3
   record(s) (2026-09-19 → 2026-09-19)"*: 660 KB reaching back to 2026-04-10, lossless (`L1_OK`–`L3_OK`) but
   mislabelled. **Don't trim.** Your S257 ruling says nothing trims this file; record in `CLAUDE.md` why it must stay that
   way unless someone plans a legacy archive first.
7. **The cadence is written down in** `docs/methodology/PROJECT_CONVENTIONS.md` §2 (`:17`–`:49`): the table row `:23`
   (*"Per behavior change"*), *CHANGELOG cadence* `:29`, the `.github/workflows/` ruling `:31`–`:47`, and the
   measurement-only ruling `:49`. It is also in `docs/wiki/model_project_constructor/Evolution.md:442`. **Don't edit
   `docs/wiki/`:** your `post-commit` hook publishes the live wiki on any commit touching it, and §4 makes `Evolution.md`
   a rewrite on request only. Record that line as stale instead. `docs/planning/opencode-adapter-spec.md:530` stays true.
8. **Your gates, in the scratch clone.** At `a18706f`, `pytest -q` (your `.venv`) gave 1395 passed, 9 skipped (the
   live-provider tier, no credentials), 97.98% coverage, about 40 s. It gave the same after the forced sync, and again
   after a (b)-shaped ledger edit. `tests/test_read_budget.py` reads the runner's Phase 1B line *"**Status:** Session
   claimed. Work beginning."*, which the new runner keeps (`../methodology/starter-kit/SESSION_RUNNER.md:87`). Every
   `docs/architecture-history/*.verify.sh` passed, plain and `--self-test`, before and after the sync. On the synced
   tree CI's `ruff check src/ tests/ packages/ scripts/` passes and `mypy` finds no issues in 68 files. None of the new
   root files is in their scope, in the wheel's (`src/model_project_constructor`) or in `mkdocs.yml`'s `exclude_docs`
   allowlist (read from the configs; the plan's item (25)).
9. **What the synced tools write** (item (29)). After one run of each, three files showed as untracked and not ignored:
   `dashboard_history.jsonl` (`methodology_dashboard.py`; `dashboard.html` is already ignored, `.gitignore:1`),
   `.context-budget-history.jsonl` (`context_budget.py --status`) and `.quality-gates-results.json` (`quality_ratchet.py
   --run`). The methodology repo ignores the results file and tracks both histories; here it is your call.
10. **The new seeds report against you, and that is expected.** `context_budget.py --status` exits 2: `CLAUDE.md` is
    32,734 B against the seed's 28,000 B, and `SESSION_NOTES.md` is over and *instrument-failed*. Your own budget is
    `tests/test_read_budget.py` and §5, with different ceilings. Whether to configure the seed or record that your test
    is the budget is your call. `.quality-gates.json` starts empty (`0/0 pass`). The synced dashboard gives 96/100 with
    three HIGH signals: `CHANGELOG.md` past 262,144 B (your S257 ruling covers it), and `SESSION_NOTES.md` and
    `BACKLOG.md` past the dashboard's one-read budget (your read-budget test governs both).
11. **Hooks.** `core.hooksPath` is `.githooks`, which holds only `post-commit`. No step here touches `docs/wiki/`, so it
    prints *"wiki publish skipped"* on each commit. There is no pre-commit hook, so nothing enforces an entry per commit.

**Steps** (the plan's `:1086`, with this project's specifics; each commit carries its own tagged entry, per (b)):

1. **Measure again, then claim.** Run `python3 ../methodology/bin/status .`, `python3 ../methodology/bin/sync --dry-run
   .` and the same with `--force`. Compare them with facts 1–2, and note the source version the sync prints. Your claim
   commit's entry is the first tagged one: add `## 2026-09` between `:14` (`---`) and `:16` (`## [0.3.0]`), with the
   entry under it. Tag every P11 commit `[ad hoc]` unless `BACKLOG.md` holds an item for it.
2. **Ignores first, one commit** (item (29)): your choice for the three files in fact 9.
3. **`CLAUDE.md`, decision (a), one commit, before the sync**, so no commit lacks the customization. Put the seven rows
   under *Additional task-to-workstream mappings*. Put the *Wiki sync* paragraph, with the live path
   `docs/wiki/model_project_constructor/`, in place of the `:73`–`:75` bullet. Record step 5's retirement in one line,
   so no later session restores it. Fix `:59` and `:102` (fact 3). Run the suite; `tests/test_session_notes_census.py`
   and `tests/test_read_budget.py` read this file.
4. **The sync, one commit** (item (18)): `python3 ../methodology/bin/sync --force .`, then commit exactly the 26 files
   the dry run listed, plus that commit's entry, and nothing else.
5. **Attribution, one commit** (fact 4): `NOTICE` §1 and `CLAUDE.md:71` name what the sync brought.
6. **`CHANGELOG.md`'s header, one commit:** replace `:5`–`:6` with the seed's pointer-and-marker paragraph
   (`../methodology/starter-kit/CHANGELOG.md:10`–`:12`, from *"**The rules** — how to add an entry"* to
   *"ledger-format: 2 — keep this marker; `bin/status` reads it."*). No other header line changes.
7. **Conventions, one commit:** in `PROJECT_CONVENTIONS.md` §2, mark the cadence (`:23`, `:29`, `:31`–`:47`, `:49`)
   superseded by the operator's decision of 2026-09-19, keeping the old text readable as history. In `CLAUDE.md`, record
   as adaptations: the legacy forms (release groups, untagged entries), where new entries go, fact 6's *don't trim*, and
   fact 7's stale wiki line. Update `BACKLOG.md:569`'s placement sentence in the same commit.
8. **Verify** (the plan's DONE list, `:1111`):
   - `bin/status` reads `present` for `CHANGELOG.md` and `HANDOFFS.md` with no file locally modified, and `bin/sync
     --dry-run` exits 0 with nothing to write.
   - §9.8 (copy the script from `:1351`) on the step 6 commit, bounds `5 6`, prints *only the block changed*; bounds
     `5 5` as a control names the hunk, `(5, 2)`.
   - `git diff --numstat a18706f HEAD -- CHANGELOG.md` shows exactly 2 deletions, and every other old line survives in
     order.
   - `methodology_trim.py --check --file CHANGELOG.md` and `--file HANDOFFS.md`: report what each prints, and don't
     `--write` (fact 6).
   - Your full suite, `ruff check src/ tests/ packages/ scripts/`, `mypy`, and both proof modes still pass.
9. **Predicted counts, from `a18706f`:** `grep -c '^### ' CHANGELOG.md` rises by exactly the entries P11 adds, and the
   anchored audit goes from 0 to that same number, since every new entry is tagged. Nothing leaves the file except
   `:5`–`:6`.
10. **Close out under the new runner:** your first `HANDOFFS.md` receipt, written `status: complete` at close-out (the
    file did not exist at your claim). `python3 ../methodology/bin/check-handoff --file HANDOFFS.md` checks its shape.
    Don't push; that is this project's go-ahead.

**Report back, for the recording session in the methodology fork:** the commit list with shas; `bin/status` before and
after; the sync's printed source version; the `### ` and audit counts at claim and close-out; the §9.8 outputs and the
numstat check; each trimmer check; the suite, ruff, mypy and proof results; what you chose for fact 9 and fact 10; and
every place a fact above turned out different.
