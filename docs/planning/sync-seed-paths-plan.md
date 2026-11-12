# Plan: make `bin/sync --layout new` seed the two config files with the paths `bin/migrate-layout` produces

**Status: APPROVED by the operator 2026-11-12 with D1 to D3 as recommended. P2 is built (S440, `1c5ceba9`) and so is P3, the fix (S441, `41c6ab34`: 12 tests added red first, 101 in the suite, the plan's [E4] reads no differing line); what is left is his (the two projects that have the defect today, and the route upstream). No ref moved, nothing sent to `KJ5HST/methodology`. `sync-seed-paths-evidence/reproduce-output.txt` stays the measurement of the defect before the fix; running `reproduce.sh` now prints the fixed state.** Written 2026-11-11 as a DRAFT; the sections below are as written, except that the citations into `bin/migrate-layout` now name where the code moved to, and the count of names moved reads seven.
A planning session's deliverable is the plan; each *piece* below is a later session of its own. The decisions the operator owes are in section 8. Backlog row: BL-131.

**Origin.** The adopter project `gaius` logged it as its BL-3 (`gaius/BACKLOG.md:29`, "Upstream" section). The operator asked for it to be read as a possible issue, then chose fix (a): sync writes the paths migration would have written.

## Words used here

- A **seed** is a file `bin/sync` creates once, when it is absent, and the project then owns. It is never overwritten, not even with `--force` (`bin/sync:330`, `tools/test_sync_layouts.py:478`).
- **The two configs** are `.context-budget.json` and `.quality-gates.json`, seeded from `starter-kit/context-budget.json` and `starter-kit/quality-gates.json`.
- **Legacy layout**: the methodology files at the project root. **New layout**: the same files under `methodology/`. **Migration** is `bin/migrate-layout`, which moves a legacy project into the new layout and rewrites the paths in the two configs.
- **The oracle** is what migration produces. The fix is right when `bin/sync --layout new` writes the same bytes into the two configs.
- A **row** is an entry of the budget config's `files` or `synced` list. Its `path` is read **from the project root** (`starter-kit/context_budget.py:345`, `expand`).
- **The surface** of a piece is where its DONE criterion is shown, with what that surface cannot enforce (runner, Planning Sessions).
- **[E1]** to **[E6]** are lines of [`sync-seed-paths-evidence/reproduce-output.txt`](sync-seed-paths-evidence/reproduce-output.txt), made by [`reproduce.sh`](sync-seed-paths-evidence/reproduce.sh) in the same directory. The script reads this repository and writes only to a throwaway directory.

## 1. Context: what is wrong, measured

Into an empty project, `bin/sync --layout new` puts every file under `methodology/`, **and copies the two config seeds unchanged**. Both seeds were written for the legacy layout, so four of their values name a place the file is not in [E1]:

| Config | Value | Seeded by `--layout new` | Migration produces [E5] | What the tool does with the seeded value |
|---|---|---|---|---|
| budget, `files` row | notes file | `SESSION_NOTES.md` | `methodology/SESSION_NOTES.md` | reads `unmeasured (file does not exist)`: the notes' size ceiling is never checked [E2] |
| budget, `synced` row | runner | `SESSION_RUNNER.md` | `methodology/SESSION_RUNNER.md` | reads `unmeasured`: the drift check against the canonical runner does not run [E2] |
| budget, `synced` row | safeguards | `SAFEGUARDS.md` | `methodology/SAFEGUARDS.md` | the same, for `SAFEGUARDS.md` [E2] |
| gates, `results_file` | results | `.quality-gates-results.json` | `methodology/.quality-gates-results.json` | an explicit value counts from the project root (`starter-kit/quality_ratchet.py:567-574`), so `--run` writes outside `methodology/` [E3] |

- **BL-3 undercounts.** It names two values (the notes row and `results_file`). Migration rewrites **four** [E4], and the two it misses are the drift check, which is the check `check_synced` exists for (`starter-kit/context_budget.py:569`: "Both went 48 days behind unnoticed").
- **It is not silent, but it misleads.** A fresh new-layout project exits 1 from `context_budget.py --status` with three rows `unmeasured`, where the same project after migration exits 0 with all three measured [E2, E6]. The word `unmeasured` reads as "the file is missing" and not as "the config names the wrong path", so the adopter has nothing pointing at the config.
- **Who has it today** (read 2026-11-11 from the files of the sibling projects on this machine; not reproducible elsewhere). Nine projects carry a `methodology/.context-budget.json`. Seven name only files that exist (apart from the optional `LEARNINGS.md`). **Two were started with `--layout new` and have the defect:**
  - **`gaius`**: its first session corrected two of the four values by hand (the notes row and `results_file`); its two `synced` rows still name `SESSION_RUNNER.md` and `SAFEGUARDS.md` at the root, where neither exists, while `methodology/SESSION_RUNNER.md` and `methodology/SAFEGUARDS.md` do.
  - **`pedkindraw`**: synced on 2026-11-10 by this repository's `HEAD` (`34067813`), **none of the four corrected**, and a live session is open in it now. Not touched.
- Every other row in those configs that read "missing" is `LEARNINGS.md`, an optional file the project may never have made. That is a different thing and is not part of this defect.

## 2. Scope boundary

**Changes:** what `bin/sync` writes when it *creates* one of the two config seeds in the new layout.

**Does not change** (each is held by a test in section 6):
- The legacy layout: its two configs stay byte-identical to the shipped seeds.
- Any seed that already exists. Decision 2a stands: never overwritten, even with `--force`. So **this fix repairs no existing project**; `gaius` needs two values corrected by hand and `pedkindraw` four (section 6, last heading).
- The shipped seeds `starter-kit/context-budget.json` and `starter-kit/quality-gates.json`, and the distributed tools `context_budget.py` and `quality_ratchet.py`. **No distributed file changes, so no adopter has anything to re-sync and no version number moves.** `bin/sync` and `bin/migrate-layout` are canonical-only.
- What migration produces. It is the oracle, and the fix does not alter it.

## 3. Decision: the design

**Rewrite the config seed's path values in `bin/sync`, at the moment it creates the seed, in the new layout only, with the same function migration uses.**

How it works:

1. **Which seeds.** The two whose legacy name is in the migration's `CONFIG_FILES` (`bin/_seed_paths.py:24`, moved there by P2). Only when the layout is `new` and the seed is about to be written (the target is absent).
2. **The mapping** (legacy path to where this run puts it). For each distributed row (`bin/sync:449` already walks them: `dest = legacy_dest if layout == "legacy" else NEW_LAYOUT[src]`), `legacy_dest -> dest`, **except a row whose seed is "present at root"** (a project's own file beside the new tree, the case `seed_file` calls `beside`, `bin/sync:337-341`): its row keeps the root path, because that is where the file really is. Plus the generated names (migration's `GENERATED`, `bin/_seed_paths.py:21-22`) as `methodology/<name>`: that is what gives `results_file` its new value.
3. **The rewrite** is migration's `rewrite_json` (`bin/_seed_paths.py:50-99`; the draft's range 323-366 in `bin/migrate-layout` stopped six lines short of the function's end). It changes only a value that is exactly a mapped path, leaves every key beginning with `_` (the prose) and `canonical` (the path to the sibling checkout) alone, keeps every other byte, and re-parses the result against the structure the rule predicts, refusing when it does not match (`Unsafe`).

Interface contract of the new step:

| | |
|---|---|
| Input | the seed's bytes (from `read_local`, `bin/sync:105`, or the `--source github` clone), the run's entries, the layout |
| Output | the same bytes with the mapped path values replaced; in the legacy layout, the input unchanged |
| Error | the seed is not JSON, or the rewrite is `Unsafe`: **refuse the whole run before any write, exit 2, naming the seed** (decision D2) |
| `--dry-run` | prints `would create` as now, writes nothing; the refusal is still raised, because it comes before the writes |
| Idempotence | a second run finds the seed present and leaves it, as now |

**One function, two callers.** Migration and sync must give the same bytes, so they should share the code that decides them rather than keep two copies. Where that code lives is decision D1 (section 8): the recommendation is a small new module, `bin/_seed_paths.py`, holding `rewrite_json`, `token_pattern`, `token_rewriter`, `Unsafe`, `GENERATED`, `CONFIG_FILES` and the directory name, **moved without editing** out of `bin/migrate-layout` and imported back under the same names, so the migration tool's 280 tests are the proof the move changed nothing.

## 4. Alternatives considered

| Alternative | Pros | Cons | Why not |
|---|---|---|---|
| **Chosen: (a), shared function in a new module** | one rewrite, so the two tools cannot disagree on a byte; the move is mechanically provable | touches `bin/migrate-layout` (a refactor, which needs the operator's approval under `SAFEGUARDS.md`) | |
| (a) with `bin/sync` loading `bin/migrate-layout` as a module | touches nothing in the migration tool; one session fewer | loads 1,459 lines for about 60; a rename or edit of the migration tool breaks sync at import; `bin/check-layout-literals` already loads siblings by path, so there is precedent | **the fallback if D1 is declined.** Cheaper, not better |
| (a) with a second, smaller rewriter written inside `bin/sync` | no coupling | a byte-preserving JSON rewriter with a structure check is about 45 lines; two copies will drift, and the migration tool is the one with 12 adopters of evidence | the drift is the failure this plan exists to remove |
| A second pair of seeds shipped for the new layout | no rewrite code at all | two copies of a 74-line, prose-heavy config that must be edited together forever; the manifest holds exactly one `NEW_LAYOUT` row per source and its reader refuses a second | a new place for the same bug to start |
| The tools resolve a legacy-looking row to where the layout keeps it | one fix for every project, including `gaius` and `pedkindraw` | changes two **distributed** tools, so every adopter must re-sync; the config would then hold paths that are not the real ones, and `bin/migrate-layout` rewrites them precisely so that it does not | a bigger blast radius for the same result; keep the config true |
| (b): drop the explicit `results_file` from the shipped seed (the tool's default already sits beside the manifest) | fixes one of the four values with no code | the other three stay; changes a distributed seed; migration of an old seed still writes an explicit value, so the two no longer match | at most a later tidy-up, not the fix |
| Do nothing; adopters correct by hand | free | already two projects, one of which corrected half and one none | the status quo is the defect |

## 5. Failure modes of the new step

- **The seed is not JSON** (a canonical defect, or a source from an unexpected ref): the run is refused before any write. It would otherwise ship the defect silently, and migration also refuses rather than leave a file half done.
- **A value the rule does not know becomes path-bearing** (a later canonical edit adds a key holding a file name). Neither tool would rewrite it, and parity with migration would not notice, because both would skip it. Held by the guard test T9 in section 6.
- **A project's own file is at the root beside the new tree** (the `beside` case): handled by the mapping rule in section 3 and tested (T5).
- **An interrupted run** leaves some seeds created and some not; a re-run creates the rest and leaves the existing ones. Unchanged behaviour.

## 6. Pieces, each one session, each with its own STOP

### P1: this plan (done at close-out of the session that wrote it)

DONE: this document, the evidence directory, one backlog row, committed with the ledger entry. **Surface:** this repository. **Cannot enforce:** that the operator agrees; that is the gate before P2.

### P2: move the shared code (only if D1 is approved; if not, skip to P3)

**DONE looks like:** `bin/_seed_paths.py` exists and holds the seven names in section 3 (the six identifiers and the directory name, `NEW_DIR`); `bin/migrate-layout` imports them and no longer defines them; **no test file is edited**.
**Verification, repo root, serially:**
- `git diff --color-moved=dimmed-zebra` shows the block moved with no changed line except the imports.
- `python3 tools/test_migrate_layout.py` passes with the count unchanged (`migrate-layout-unit-tests` min 280, `.quality-gates.json`). **It takes about 14 minutes** (280 tests, 840 s measured on 2026-11-11); run it alone, before the full run, as the cheapest check that reads the moved code.
- `python3 bin/check-layout-literals` reads 0 sites (the gate `layout-literals`); the new module carries the same `# layout: ok -- <reason>` markers the moved lines carry.
- `python3 tools/test_sync_layouts.py` and `python3 tools/test_layout_resolver.py` unchanged.
- `bash bin/tests.sh > <file>` then `python3 starter-kit/quality_ratchet.py --run`: 25 of 25, `tests-sh-passed` at or above 702.

**Files:** `bin/_seed_paths.py` (new), `bin/migrate-layout`, `CHANGELOG.md`: three, under the five-file cap.
**Surface:** this repository, a clean clone, one writer. **Cannot enforce:** behaviour on a real adopter. A verbatim move makes that a non-question; the 12-adopter rehearsal (`docs/planning/methodology-subdirectory-evidence/migrate-12-adopters.py`) is the heavier check and is not required.
**STOP** after the commit and the close-out. P3 is the next session.

### P3: the fix

**DONE looks like:** a fresh `bin/sync --layout new` project's two configs equal the canonical seeds with the four values replaced, and nothing else differs; the tools run from the project root measure the three rows and write the results under `methodology/`.

**Tests, added to `tools/test_sync_layouts.py`** (a `Scratch` project each, as the neighbouring tests build them; the migration suite already pins the same four replacements as text at `tools/test_migrate_layout.py:1425-1436`, which is the cheap oracle):

| # | Asserts |
|---|---|
| T1 | `--layout new`: `.context-budget.json` rows `SESSION_NOTES.md`, `SESSION_RUNNER.md`, `SAFEGUARDS.md` read `methodology/...`; `CLAUDE.md` and `LEARNINGS.md` do not change; `canonical` and every `_` key do not change |
| T2 | `--layout new`: `.quality-gates.json` `results_file` is `methodology/.quality-gates-results.json` |
| T3 | **Only those values differ:** each new-layout config, with the four values put back, equals the shipped seed byte for byte |
| T4 | **Oracle parity:** each new-layout config equals the shipped seed with the four replacements migration's own test applies |
| T5 | a project whose own `SESSION_NOTES.md` sits at the root beside the new tree: the created config keeps the row `SESSION_NOTES.md` and rewrites the other two |
| T6 | `--layout legacy`, and `--layout auto` on a legacy project: both configs byte-equal to the shipped seeds |
| T7 | **End to end:** in a fresh new-layout project, with the sibling checkout reachable as an adopter has it, `context_budget.py --status` reads the three rows as measured (not `unmeasured`) and exits 0, and `quality_ratchet.py --run` writes `methodology/.quality-gates-results.json` and nothing at the root |
| T8 | an existing config under `methodology/` is left as it is, with and without `--force`; a seed that cannot be rewritten (not JSON, in a source built for the test) refuses the run with exit 2, names the seed, and writes no file |
| T9 | **The guard:** every path-looking value in the shipped seeds (a string value outside the `_` keys that ends in a known extension) is either rewritten in the new layout or on a short allow-list written in the test (`CLAUDE.md`, `LEARNINGS.md`, the `canonical` paths). A new seed value that is neither fails the test and forces a decision |
| T10 | the `--source github` path (the existing local-bare-repository fixture, `TestSyncFromGithubReadsTheTable`): the seed that arrives from a clone is rewritten the same |

**Verification, repo root, serially:**
- **Red first.** Run the new tests against the unfixed `bin/sync` and keep the output: T1, T2, T4, T5, T7, T9 and T10 must fail on it, and so must T8's refusal case, which is the positive control; T3 and T6 must pass on both the unfixed and the fixed code, because they guard against rewriting too much. A test that cannot fail proves nothing.
- Then `python3 tools/test_sync_layouts.py` (takes about 96 s now; 89 tests) green with the new count, and `sync-layout-unit-tests` raised to that measured count in `.quality-gates.json` (a tightening, so no approval is needed).
- `python3 tools/test_migrate_layout.py`, `python3 bin/check-layout-literals` (0 sites; `bin/sync` must not name a methodology file as a literal, which is why the mapping comes from the manifest), `bin/check-links`, `check-ledger`, then the full `bash bin/tests.sh > <file>` and `quality_ratchet.py --run`: 25 of 25.
- `bash docs/planning/sync-seed-paths-evidence/reproduce.sh`: [E4] shows **no differing line** and [E2] reads the rows as measured.

**Files:** `bin/sync`, `tools/test_sync_layouts.py`, `bin/tests.sh`, `.quality-gates.json`, `CHANGELOG.md`: five, at the cap. `bin/tests.sh` was missing from the draft's list; S440 derived it: its fixture `mh_fixture` copies `bin/sync`, `bin/status`, `bin/_manifest.py` and `bin/_manifest_reader.py` into a scratch `bin/` (`:3686`) and six tests run that copy of `sync` (`:3712`, `:3730`, `:4315`, `:4382`, `:4424`, `:5380`), so once `bin/sync` imports `bin/_seed_paths.py` that `cp` line must name it or each of them fails at import. The fixtures near `:4390` (`$H`) also carry a copy of `bin/sync`; read them in the same change.
**Surface:** this repository; throwaway projects built by the real `bin/sync` and the real tools run from their root. **Cannot enforce:** that the network clone behaves the same (the suite uses a local bare repository, as it already does); that a project synced before this fix is repaired (it is not, section 2).
**STOP** after the commit and the close-out. Nothing is pushed or proposed upstream in the same session.

### Not a piece of this repository's work: the two projects that have it today

`gaius` (two `synced` rows) and `pedkindraw` (the notes row, two `synced` rows and `results_file`) each need their config's path values corrected by hand to what [E5] shows. They are other projects' files, and `pedkindraw` has a live session, so this plan does not run it: decision D3.

## 7. Impact

| Place | Impact | Action |
|---|---|---|
| `bin/sync` | one step added before the seed write; one pre-write refusal | P3 |
| `bin/migrate-layout` | seven names move to a new module; no behaviour change | P2 (if D1) |
| `bin/_seed_paths.py` | new, canonical-only | P2 |
| `tools/test_sync_layouts.py` | ten tests added | P3 |
| `.quality-gates.json` | `sync-layout-unit-tests` raised; no other gate loosened | P3 |
| `starter-kit/*` seeds and tools | **none** | none |
| `bin/status`, `bin/check-links`, the dashboard | read configs and seeds where the layout keeps them; none reads a seed's content (`SEED_FORMAT_MARKERS` names only the two ledgers, `bin/_manifest.py:169-172`) | none |
| Adopters | none receives a file; the next `--layout new` into an empty project is right | D3 for the two that are not |
| Upstream | **every file this fix touches is in the diff of the open pull request #99** (`bin/migrate-layout` is entirely new there), so it reaches upstream stacked on #99 or after it | his decision, each time (section 8) |

## 8. Decisions for the operator

- **D1: where the shared code lives.** Recommended: **move it to `bin/_seed_paths.py`** (P2 then P3, two sessions). The alternative is `bin/sync` loading `bin/migrate-layout` (one session, no change to the migration tool). Moving is a refactor, which `SAFEGUARDS.md` says needs plan approval; that is why it is asked.
- **D2: a seed that cannot be rewritten.** Recommended: **refuse the run before any write.** The alternative writes the seed unchanged and prints a warning, which ships the defect to whoever misses the line.
- **D3: the two projects that have it.** Not run from here. His options: correct them himself; or give each project's own session the values in [E5]; or leave them. `pedkindraw` has a live session.
- **Not decided here, and not asked yet:** whether this goes upstream in the pull request that carries the folder move or in a later one. That belongs with the composition of the upstream pull request, and anything sent is his go-ahead.

## 9. What was checked, and what was not

Checked by running it: the reproduction and the oracle [E1] to [E6]; `tools/test_sync_layouts.py` (89 tests, 96 s) and `tools/test_migrate_layout.py` (280 tests, 840 s), both green on `main` before any change; the two real projects' configs against the files on disk; the overlap of every touched file with #99's head.
**Not checked:** that `rewrite_json` rewrites the four values when called from sync (it is the function migration used to produce [E5], but sync does not call it yet); whether `bin/check-layout-literals` accepts the new module without further markers. Each is a P2 or P3 criterion above, not an assumption.
