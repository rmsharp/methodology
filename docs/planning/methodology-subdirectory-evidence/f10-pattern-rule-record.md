# F10 and F11 — the tool reads a root `.Rbuildignore` for what its patterns cover, and files a packager's ignore list as config (BL-101, plan section 7.6, S290)

Register rows F10 and F11 ([`findings-register.md`](findings-register.md)). At the S290 Phase 0 picker he chose F10 as the deliverable; at the design gate he chose **the pattern rule in place of the register's stem rule**, and **to record F11 and fix it in the same change**. Nothing was run in an adopter's real tree and nothing went upstream; the tool is canonical-only, so no adopter receives it until D8.

## 1. The problem

F5's list reads whole names. A `.Rbuildignore` of regular expressions (`^SESSION_RUNNER.*\.md$`) names no file, so the tool listed `nprcgenekeepr`'s only for 3 comment lines that spell a name out, flagged `[comment lines only]`: the row a person read was the harmless one (F10). Measuring the rules for it found a second defect of F5's kind: `vscode_quarto_ext`'s `.vscodeignore` carries 26 mentions of moved names (21 on code lines), and `hit_category` filed it under `other` with the prose, 26 of that adopter's 254 mentions there (F11); the S286 survey's `kind_of` had filed it as `other` too, so S289's comparison against the survey could not see it.

## 2. What the rules would add, measured BEFORE building (`f10-rules.py`, output `f10-rules-output.txt`)

The 10 adopters at the S286 pins, synced in `--no-local` clones, tier all, the tool at `aae6c22` (before F10). Every row was read by eye, not only counted.

| Rule | Result | Verdict |
|---|---|---|
| **S**, the stem rule as the register words it | 78 files, 256 lines; **68 files new to F5's list, 0 real.** Of the 183 rows printed, 127 are the word `dashboard`; `vscode_quarto_ext`'s 20 are `CHANGELOG: <title>` citations in test names; the rest are docstrings, a nested framework copy, fixture strings. The one real file among the 78, `nprcgenekeepr`'s `.Rbuildignore`, was already listed (for its comment lines). | not built |
| **M**, a module imported by its stem | 1 file, 4 lines: all four are `.Rbuildignore` regex lines. No `import`, `from` or `-m` of a moved tool in 10 adopters. | not built; the limit stays in the text |
| **P**, the pattern evaluation of the root `.Rbuildignore` | 1 file (`nprcgenekeepr`): **22 lines cover 143 entries of the moved-or-generated map** (139 moves and the generated files the tools write beside them). Every line is a framework file's name by regex, plus `^docs$`, which covers the 122 moved files under `docs/`. No line is wrong. | **built** |
| **G**, an ignore-style file the tool files under `other` | 1 file: `vscode_quarto_ext`'s `.vscodeignore`. | **built (F11)** |

**Three figures I gave him at the design gate were wrong and are corrected here, none of which changes the choice:** the stem rule's 68 new files held **0** real ones, not 1 (the real file was among the 10 already listed); the pattern rule reads **22** lines, not 21 (my measuring script had no parent-directory rule, which the design text described; `^docs$` is the 22nd, line 15, and is real: the `docs/archive` shards and `docs/methodology` files leave `docs/`); and the file has **99** non-comment lines, not 34 (a figure I stated and had not measured).

## 3. What R and vsce do (`f10-probes.sh`, output `f10-probes-output.txt`)

A toy project built with R 4.6.1 (`R CMD build`) and one with `npx @vscode/vsce@3.6.0 ls`, read from the output:

1. **R matches case-insensitively:** `^foo\.txt$` left `FOO.txt` out of the package.
2. **A line that matches a directory covers what is under it:** `^docsdir$` left `docsdir/inner.txt` out.
3. **A line that starts with `#` is a regular expression, not a comment:** the single line `# |ALPHA` left `ALPHA.md` out (a control with no such line packaged it). The rule therefore evaluates every non-empty line.
4. **The break is real:** with `^SESSION_RUNNER.*\.md$`, `SESSION_RUNNER.md` is out; moved to `methodology/`, **`methodology/SESSION_RUNNER.md` is packaged**; one more line, `^methodology$`, takes `methodology/` out again.
5. **vsce 3.6.0** (source read: `package.js` matches each line with `minimatch(f, pattern, { dot: true })`, no `matchBase`; run: `ls --no-dependencies`): with `.vscodeignore` = `SESSION_RUNNER.md`, `methodology/SESSION_RUNNER.md` is listed for packaging; adding `methodology/**` takes it out. A bare name is the project root's: the literal names in `vscode_quarto_ext`'s `.vscodeignore` are a real exposure, which is what filing the file apart from prose is for. A `.gitignore` stays prose: git matches a bare name at any depth.

## 4. The change (`ec8a38d`, `b06f8d1`; `bin/migrate-layout`)

- `pattern_exposure(text, mapping)`: every non-empty line a case-insensitive regular expression; a line covers a path when it matches the path or a directory above it; a moved file is exposed when a line covers where it is and none covers where it goes. A line Python's `re` cannot compile, or that holds a POSIX class (`[[:alpha:]]`, which `re` reads as a different set), is counted as not evaluated, never misread.
- `scan_hits` reads the root `.Rbuildignore` **if it is tracked** (an untracked one is not), whether or not it spells a name out; its row keeps F5's fields and gains `patterns` (`lines`, `exposed`, `unread`); a file with no exposure gets no row it did not already have.
- The text prints one line per exposing line (`line 72: ^SESSION_RUNNER.*\.md$  stops covering SESSION_RUNNER.md`; three names and a count when a line covers many), then one sentence: how many lines cover how many moved files, that a line such as `^methodology$` would cover the new directory, and that each line is read by Python's `re`, not R's engine: **a candidate, not a verdict**. The `[comment lines only]` mark is not printed on a row whose patterns are the exposure.
- `is_pattern_list`: a dot-file whose name ends in `ignore`, `.gitignore` apart, is `config`.
- The tool lists and never edits; no refusal, no new exit code.

## 5. What was measured after

| Check | Result |
|---|---|
| Tests | `tools/test_migrate_layout.py` 150 to 182 (floor 182). The first 24 were run before the change: 3 failures and 17 errors, all for the intended reasons (no `pattern_exposure`, no `patterns` rows, `.vscodeignore` still under `other`); 4 passed because they pin behaviour that stays (a covered directory clears a line, only the root file is read, a project without one, a nested `.gitignore` stays prose). Seven more were written with the code, not before it: the tag on a row of patterns, the POSIX class, three names and a count, the unread line in the text, an only-unreadable file, an untracked file, the file order across lines; mutants R03, P04, P05, R04, R05, R07, R08, W01, W02 and P15 stand for them (all killed). The 32nd, the order of the files under one line, came from round 1 (P13). `Ran 182 tests in 367.349s, OK`. |
| The scan, on real trees | The tool at `aae6c22` and the new one on the same 10 clones (`f10-identity.py`, output `f10-identity-output.txt`, identical on a second run): `ledger`, `harness`, `ci`, `hooks`, `tests`, `proofs`, `scripts` identical in rows and totals in all 10; `config + other` identical in mentions and files; the **two differences** are `nprcgenekeepr`'s `.Rbuildignore` (`patterns`: 22 lines, 143 moved files, 0 not evaluated) and `vscode_quarto_ext`'s `.vscodeignore` (other to config). |
| Against the S286 survey | By F5's own comparison (a file with a mention on a code line), **24 of 25 before, 25 of 25 now**. The 25th was listed before too, but only for 3 comment lines; now it is listed for its patterns. |
| Mutation round 1 (`f10-mutants.py`, `mutate-p7.py`, a scratch clone of `ec8a38d`, baseline green) | 40 mutants, **37 killed, 3 survived**: **G05** (my mutant was equivalent: `low` is the basename, so a `/` test on it changes nothing; replaced), **P03** (skipping whitespace-only lines: equivalent over this tool's domain, since no moved path contains a space for such a line to match; not pinned), **P13** (the files of one line unsorted: a real gap). Output `f10-mutation-round-1.txt`. |
| Mutation round 2 (G05 replaced, and P13, against `b06f8d1`, which adds the test for it) | **2 of 2 killed**, baseline green at 182. Output `f10-mutation-round-2.txt`. In all, 39 of 40 killed and 1 equivalent survivor. |
| `bin/check-layout-literals` | 0 sites. |

## 6. What the list cannot show

1. **Python's `re` is not R's engine.** A line using a construct the two read differently is answered for the wrong pattern; POSIX classes and uncompilable lines are counted (`unread`), the rest is not known. The answer is a candidate.
2. **Only the root `.Rbuildignore` is evaluated.** Other pattern lists (`.vscodeignore`, `.npmignore`, `.vercelignore`, ...) are listed apart from prose by name (F11) but not judged: their dialects differ (vsce's minimatch without `matchBase`, gitignore's any-depth, ...) and only vsce's was read and run here.
3. **CI path filters with globs are not evaluated.** 20 of the 21 entries of `nprcgenekeepr`'s four `paths-ignore` lists are literal names, which F5's list already sees; the 21st, `docs/**`, is a glob that covers the files that leave `docs/`, and the tool does not judge it (a missed filter here costs a CI run on a push that touches `methodology/`, not a package).
4. **A module imported by its stem is still not seen**, as the tool's text says: 0 cases in 10 adopters.
5. **Not shown:** an adopter that read the row and acted on it; `R CMD build` or `R CMD check` run on `nprcgenekeepr` itself (the probe is a toy package); a run in any adopter's own tree.
6. **The row counts the tool's map, not the disk:** "143 moved file(s)" includes the files the tools generate and write beside the moved configs, whether or not they exist yet.

## 7. Reproduce

    python3 tools/test_migrate_layout.py TestThePureRules TestAPatternThatStopsMatchingIsListed     # about 1 minute
    python3 tools/test_migrate_layout.py                                                            # 182 tests, about 6 minutes
    python3 -I docs/planning/methodology-subdirectory-evidence/f5-population.py <an empty directory>   # clones the adopters, writes nothing in them
    python3 -I docs/planning/methodology-subdirectory-evidence/f10-rules.py <that directory> aae6c22 --rows
    python3 -I docs/planning/methodology-subdirectory-evidence/f10-identity.py <that directory> aae6c22
    bash docs/planning/methodology-subdirectory-evidence/f10-probes.sh <an empty directory>        # needs R, and node and the network for the vsce half
    git clone --no-local . <scratch> && git -C <scratch> checkout ec8a38d && \
      python3 -B docs/planning/methodology-subdirectory-evidence/mutate-p7.py <scratch> docs/planning/methodology-subdirectory-evidence/f10-mutants.py   # round 1

The population scripts need the adopters under `~/Development/` at the S286 pinned revisions (`PINS` in `f5-population.py`).
