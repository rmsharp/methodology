# The 32nd commit on the pull request candidate: the record (2026-10-15)

His call 4 in `pr4-record.md` section 5, taken at the Phase 0 picker: fix the four text defects of section 1 item 4 before PR5, then re-run
`pr4-claims.sh`. Local ref only; nothing is sent to `KJ5HST/methodology`. The edits are `fix32-build.py` (it refuses on drift), the message is
`fix32-message.txt`, the re-run is `pr4-claims.sh` saved as `fix32-claims-output.txt`.

## 1. The answer

One commit on top of the reduction commit: **`a62bfec`**, now the tip of the local ref `pr2/candidate` (32 commits over `upstream/main` `f34769f`; the previous tip
`ced2c82` is pinned as `refs/pr2/candidate-before-fix32`, read back: 0 behind, 1 ahead). Four files, +8 / -5 (`git diff --numstat`: 2/2, 2/1, 2/1, 2/1). No code path
and no threshold changes. Against upstream the shortstat moves by +5 / -2 (47 files, +19,826 / -1,152): of the 5 lines removed, 2 are upstream's own comment line
(once in each dashboard copy) and 3 were added by the series.

| File | What it said | What is true | Re-derived by |
|------|--------------|--------------|---------------|
| `.quality-gates.json`, gate `layout-literals`, `why` | `bin/check-handoff` and `bin/check-ledger` "are not scanned ... and this change does not give them the layout reading" | the scan takes `starter-kit/*.py`, every file in `bin/` but `bin/_manifest.py` and `bin/tests.sh`, and `.githooks/*`; both checkers are among its 15 files and each calls `resolve_layout(root, LEDGER_NAME)` (`bin/check-handoff:459`, `bin/check-ledger:132`) | `scan_root('.')` listed the 15 files; `grep -n 'resolve_layout('` |
| `.quality-gates.json`, gate `layout-unit-tests`, `why` | "74 is measured (Ran 74 tests, OK)" against a floor of 76 | `python3 -I tools/test_layout_resolver.py`: `Ran 76 tests`; the gate row reads `>= 76`, measured 76 | the run |
| `starter-kit/methodology_dashboard.py` and its `tools/` twin, the comment above the stale-copy warning | "the safe per-project action is one `cp`, and the message never printed it" | the warning prints `python3 <canonical> --sync <project root>` (`:1212`); upstream's own message printed `cp` (`f34769f`, line 668 and the print below it), which is what made the sentence true there | `git show upstream/main:` against the candidate |
| `bin/migrate-layout`, header | exit list `0 ... 1 ... 2 ... 3`, nothing for 4 | `main` returns 4 when an apply's after-checks differ from its before-checks or the tree is dirty (`return 0 if report["checks"]["ok"] else 4`) and prints "CHECKS DIFFER ... The commit stands" (`:1420`) | reading the function; the exit logic is unchanged |

**Where each came from** (`git log -S` on the candidate): the `layout-literals` sentence was true when written (`0aa1897`: the scanner then skipped both checkers by name) and
became false one commit later (`a459b8b`, which gave them the resolver); the `layout-unit-tests` sentence was written at `14ef959` for 74 and the floor went to 76 at `0aa1897`
with the sentence left; the dashboard sentence is upstream's, made false when the candidate's first commit (`bbe0dc3`) changed what the warning prints; the exit list was
wrong from the day `bin/migrate-layout` was written (`2942e46`: the header and `else 4` are in the same commit).

## 2. What the builder proves

`fix32-build.py` refuses, writing nothing, on a file that is not the blob it was derived from, an anchor not found once, or two dashboard copies that differ; it then
checks its own output: the gate manifest differs from the old one in exactly two `why` strings (every other key, threshold and command equal), `starter-kit/methodology_dashboard.py` and
`bin/migrate-layout` have the same syntax tree before and after once the docstring is set aside, and the dashboard twins are byte-identical. A second run on the edited tree
refused ("not the blob this was derived from"). The commit ran `python3 starter-kit/quality_ratchet.py --precommit` by hand (exit 0); the scratch clone runs no hooks, as for the
reduction commit.

## 3. Verification: `pr4-claims.sh` on `a62bfec`

Clean `--no-local` clones, serial, exits read bare (`fix32-claims-output.txt`, 106 lines, exit 0). Against S327's run on `ced2c82` (`pr4-claims-output.txt`) the output differs in
exactly these places and no other (`diff` of the two with colour codes stripped):

| Line | `ced2c82` | `a62bfec` |
|------|-----------|-----------|
| shortstat | 47 files, +19,821 / -1,150 | 47 files, +19,826 / -1,152 |
| commits over upstream | 31 | 32 |
| gate manifest id | `cfa4d5b5fa67` | `c7b9257ea110` |
| section 7, commits compared against their parents | 31 | 32 (0 refusals, 0 warnings, 0 manifest defects) |
| (a timing, not a figure) layout suite | 1.973 s | 19.865 s, at a load average of 21 to 54 from foreign processes |

Unchanged: the suite 302 / 0 / 0 (upstream 261 / 0), the gate **18/18, 0 unmeasured** (upstream 12/12), the **results id `23481eb88ba1`**, 80 links resolve in both layouts, the scanner 15 files and
0 sites, the resolver block equal in all 11 files that embed it, merge-tree against #94 (conflicts in `.quality-gates.json` 1 region, the trimmer 10, its tests 6) and #92 (clean).
**S327's expectation, that the commit "moves the gate's two ids", was half wrong:** `manifest` is a hash of the gate definitions, which include each `why` (`quality_ratchet.py:537`), so it moved;
`results` is a hash of the per-gate run results (`:538`), which did not change.

## 4. The draft text: figures only

`docs/planning/upstream-pr-body.md` (draft 3): the head `ced2c82` to `a62bfec`, "31 commits" to "32" in four places, "+19,821 / -1,150" to "+19,826 / -1,152", and one new row in the commit
table for `a62bfec`. `pr4-body-check.py` on the edited draft: exit 0, and its output differs from the unedited draft's against the same head by the one new line (`a62bfec` resolves);
run on the unedited draft against both heads, it differed in the shortstat and the count only. **That checker does not fail on a stale figure** (it prints the recomputed shortstat and count for a
reader to compare), so the comparison was made by command: no `31 commits`, `19,821` or `1,150` is left in the body, and the draft's own "at least 56 added lines of that kind, 36 starting with
`#` or `//`" re-ran at 56 and 36 on both heads. The text is still draft 3 in every other word and **has had no fresh read**; his approval of it, D1 and D4 stay open.

## 5. What none of it shows

- `layer-verify.sh` (the per-layer clone run of the reduction commit) was not run: its ratchet, scanner and proof lines are what `pr4-claims.sh` sections 3, 4 and 6 print for this head, and the one tracked
  proof in the clones exits 0 on both tips.
- A fifth stale statement, **seen and not fixed** (one commit, four defects, as he called it): the scanner's docstring says it reads "`bin/*` (a script with a shebang)", and `bin/_manifest_reader.py`
  has no shebang and is among the 15 files it scans (`bin/check-layout-literals`, the "Scanned:" paragraph). His call: leave it, fix it in a 33rd commit (a62bfec and this run stand), or amend `a62bfec` (the series stays 32 commits, but the hash changes and `pr4-claims.sh` runs again: about 35 minutes here, launched a little after 21:40 and its done-file written at 22:16, at a load average of 21 to 130 from foreign processes).
- The maintainer's machine, upstream's CI (it has none), Windows, a hooks-armed clone's run of the full suite on `a62bfec`, and a fresh reader of the text.
- Whether anything in the candidate asserts on the three comment/header strings: the suite and the gate (302 and 18/18) ran after the edit and read green, so nothing that runs does.
