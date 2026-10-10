# F5 — the tool lists the machine-read files a move relocates (BL-101, plan section 7.6, S289)

Register row F5 ([`findings-register.md`](findings-register.md)), his decision at the S288 close-out that it comes before P13, his design choices at the S289 picker: **list only** (no new refusal, no exit-code change), **split `other` into kinds**, implement. Nothing was run in an adopter's real tree and nothing went upstream; the tool is canonical-only, so no adopter receives it until D8.

## 1. The problem, reproduced first

P11 moved `model_project_constructor` at `--tier all`; every check the tool runs passed and the adopter's own CI broke (41 tests, 2 of 13 proofs). The tool's dry run, run now on that adopter at `63cedc5` (the sync commit, tier all), printed `other: 2647 mentions in 73 files` and showed 25 sites. **None of the 4 files that broke was among them** (`s286-adopter-survey-record.md` section 4 had said why: `scan_hits` lumped tests, scripts and proofs with prose in `other` and showed the first 25 lines).

## 2. The change (`fb71d55`, `4b80afe`)

- `hit_category(path, text="")` (`bin/migrate-layout:442`) sorts a file that names a moved path into `ci`, `hooks`, `tests`, `proofs`, `scripts`, `config`, `harness`, `ledger` or `other` (nine; was five). A prose extension is prose wherever it sits (the survey prototype `kind_of` sorted `tests/eval/PHASE_E_AGREEMENT_REPORT.md` as a test because its directory rule ran first); a `#!` first line makes an extensionless file a script (`bin/check-handoff` in `dalia_martinez_funeral` was in `other` in P7's reports); `.husky/` and `.pre-commit-config.yaml` are hooks.
- `scan_hits` keeps its matching rule, byte for byte, and adds `paths` to each machine-read category: one row per file, **uncapped**, with its mentions, its mentions on non-comment lines, the names it carries and its first mention on a code line. The 25-site cap stays, because one file can use all 25 (the crowd-out F5 found); a test pins that.
- The text prints the rows under a sentence saying they are candidates the tool does not run, that a name on a code line is necessary and not sufficient, and what to rehearse; a file whose mentions are all on comment lines is marked `[comment lines only]` and printed after the others.

## 3. What was measured

| Check | Result |
|---|---|
| Tests, written failing first | 12 red (5 failures, 7 errors) for the intended reasons, then green. `tools/test_migrate_layout.py` 136 to 150 tests; the full suite `Ran 146 tests in 373.158s, OK` before the last four were added, and the round 2 baseline ran all 150 green. |
| The control, same adopter and commit as section 1 | **All 4 files that broke are listed**, under `tests` (2) and `proofs` (2). After: `tests` 26 mentions in 8 files, `proofs` 215 in 13, `scripts` 1 in 1, `config` 3 in 2, `other` 2,402 in 49. **Sum 2,647 mentions in 73 files: identical to before.** |
| The scan is unchanged, on real trees | The old tool (`fb71d55~1`) and the new one on the same 10 clones: `ledger`, `harness`, `ci` and `hooks` identical, and the old `other` equals `tests + proofs + scripts + config + other` in mentions and files, **in all 10** (`f5-identity.py`, output `f5-identity-output.txt`; the numbers: Philippians 24/7, airqino 469/19, chat_verification 21/4, church_growth 54/6, dalia_martinez_funeral 118/6, feedback-loop-comparison 93/9, mts-system 2050/33, nprcgenekeepr 1345/119, vscode_quarto_ext 265/43, wsfct 2988/61). |
| Against the S286 survey, 10 adopters at its pinned revisions (`f5-population.py`, output `f5-population-output.txt`, reproduced on a second run) | **24 of the survey's 25 strong-name candidates are listed, each under the matching kind.** The 25th, `nprcgenekeepr`'s `.Rbuildignore`, was a hit on `.gitattributes` (`^\.gitattributes$`), which this migration leaves in place (`left_in_place`: "holds rules of the project's own"); the tool lists the file anyway, under `config`, for 3 mentions on comment lines. **5 files the survey did not list:** `airqino`'s nested copy under `docs/methodology/` (`bin/_manifest.py`, `bin/check-links`, `bin/tests.sh`, two dashboard copies): the survey excluded everything under that directory by rule, the tool leaves a file that is not in the manifest and so lists it, as it counted it in `other` before. |
| Mutation round 1 (`f5-mutants.py`, `mutate-p7.py`, a scratch clone of `fb71d55`, baseline green) | 30 mutants, **23 killed, 7 survived**: F17, F18, F20, F22, F23, F27, F28. Each named a behaviour no test pinned; F22 was the sharpest: the old assertion `assertIn("not tracked", text)` was satisfied by the moves list's own `(not tracked: a plain move)`. Output `f5-mutation-round-1.txt`. |
| Mutation round 2 (the seven against `4b80afe`, which adds four tests and three table rows) | **7 of 7 killed**, baseline green at 150 tests. Output `f5-mutation-round-2.txt`. |
| `bin/check-layout-literals` | 0 sites (the classifier carries no moved-file name). |

## 4. What the list cannot show (stated in the tool's text too)

1. **Candidates, never verdicts.** The control lists 13 proofs; 11 of them read the ledger at an old commit through git, which a move cannot break, and only 2 broke (F4). The list is an upper bound, and a zero is the strong result.
2. **Names are literal, and the row shows the first code-line mention.** A pattern that names a moved file by stem is not seen: `nprcgenekeepr`'s `.Rbuildignore` ignores framework files by 16 regex lines (`^SESSION_RUNNER.*\.md$`, `^methodology_trim\.py$`, `^context_budget\.py$`, ...), which stop matching once the files sit under `methodology/` (survey record section 3). The tool lists the file only for its 3 comment-line mentions, so **the row a person reads is the harmless one: register row F10, open**. A module imported by its stem is the same class.
3. **A docstring line is a code line.** The comment test is by first character. `tests/test_read_budget.py` prints line 4, a docstring, not the `RUNNER =` line that broke (13 mentions, 11 on code lines).
4. **`.qmd` and `.Rmd` are prose** whatever chunks they hold; `spec/`, `test/` and `tests/` directories are tests by name (a `docs/spec/schema.json` would be read as a test); untracked and ignored files are not scanned, except the hooks git runs.
5. **An `--apply` prints the list after it has applied.** The dry run, the default, prints it first; the text says to rehearse in a clone before applying. A refusal on the list was offered and he chose not to (an upper bound that is mostly false positives is not a ground to refuse).
6. **Not shown:** an adopter that read the list and acted on it; the list on `claude_work` (no commit, the tool refuses); a run on a live adopter's own tree.

## 5. Reproduce

    python3 tools/test_migrate_layout.py TestThePureRules TestTheMachineReadFilesAreListedApartFromProse     # about 30 s
    python3 tools/test_migrate_layout.py                                                                     # 150 tests, 6 to 7 minutes
    python3 -I docs/planning/methodology-subdirectory-evidence/f5-population.py <an empty directory>        # about 3 minutes, clones the adopters, writes nothing in them
    python3 -I docs/planning/methodology-subdirectory-evidence/f5-identity.py <that directory>             # old tool against new on those clones, about 1 minute
    git clone --no-local . <scratch> && git -C <scratch> checkout fb71d55 && \
      python3 -B docs/planning/methodology-subdirectory-evidence/mutate-p7.py <scratch> docs/planning/methodology-subdirectory-evidence/f5-mutants.py   # round 1, about 50 minutes at a load of 8 to 20

The population script needs the adopters under `~/Development/` at the S286 pinned revisions (`PINS` in the script).
