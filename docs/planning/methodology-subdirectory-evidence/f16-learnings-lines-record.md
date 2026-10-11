# F16 — the `CLAUDE.md` rewrite inside a project's own Learnings: measured over every adopter, then kept (BL-101, plan section 7.6, S294)

Register row F16 ([`findings-register.md`](findings-register.md)). At the S294 Phase 0 picker he chose F16 as the deliverable; the rule was his call (the register says so). I had suggested the opposite of what the measurement shows, said so at the decision picker, and he chose **to keep the rewrite and close F16**. Nothing was run in an adopter's real tree (committed text only, read with `git show`), nothing went upstream, and the tool did not change.

## 1. The question

`bin/migrate-layout` rewrites a project's `CLAUDE.md` as text (`plan_rewrites`, `add("CLAUDE.md", tokens)`): every standing-alone path of a moved file becomes its new path. At `church_growth` 9 of the 16 changed lines sat inside the project's own `### Project-specific Learnings`, which record past events, and the tool "cannot tell a live pointer from a past-tense account" ([`p14-church-growth-record.md`](p14-church-growth-record.md) section 4). The register's own reason for the rule: `CLAUDE.md` is read every session, and a rule that skipped the Learnings would leave live pointers there stale. Two questions the one adopter could not answer: is `church_growth` typical, and does any in-Learnings line become **false** by the rewrite?

## 2. The instrument

[`f16-measure-claude-md.py`](f16-measure-claude-md.py), output [`f16-measure-output.txt`](f16-measure-output.txt): for each of the 12 adopters on this machine, the committed `CLAUDE.md` (`git show`; `church_growth` at `62f7d8a~1`, the commit before its move), the tool's own `token_rewriter` pattern over the manifest's whole legacy-to-new table at tier all, and a count of the changed lines outside and inside a Learnings region (the text under a heading whose own text contains "earning", up to the next heading of the same or a higher level). It reproduces the P14 record: **16 changed lines at `church_growth`, 9 inside**. `claude_work` has no commit, so no `CLAUDE.md`.

## 3. The result

| Adopter | Changed lines outside Learnings | Inside |
|---|---|---|
| `church_growth` | 7 | **9** |
| `chat_verification` | 5 | 3 |
| `Philippians` | 8 | 2 |
| `nprcgenekeepr`, `mts-system`, `wsfct` | 20, 17, 37 | 1 each |
| `model_project_constructor`, `vscode_quarto_ext`, `dalia_martinez_funeral` | 11, 21, 9 | 0 |
| `feedback-loop-comparison`, `airqino` | 0 | 0 |
| **Total** | **135** | **17** |

So `church_growth` is the extreme, not the typical case: 17 of 152 changed lines (11%) are inside a Learnings region, in 6 of 11 adopters, and 9 of the 17 are one adopter's.

## 4. What the 17 lines say (read, not counted)

I read every one, with the text around the changed path; for `church_growth` the 9 whole lines in the P14 diff; for `chat_verification` the lines and their neighbours.

- **`nprcgenekeepr`, `mts-system`, `wsfct` (3 lines):** "Base methodology-level learnings remain in `SESSION_RUNNER.md`": a present-tense pointer. `wsfct`'s line also says the learnings were "Extracted from the synced `SESSION_RUNNER.md` table", a past account naming a file that still exists.
- **`Philippians` (2):** P2, "the durable ratification record lives in ... `CHANGELOG.md`": a present-tense rule. P8, "run `python3 quality_ratchet.py --run` and cite its summary line": **a runnable command and a gate file**, which a skipped rewrite would leave to fail after the move.
- **`chat_verification` (3):** "`SESSION_RUNNER.md` §3D already says ..." (a rule cited), "Reconciling `CHANGELOG.md`/`HANDOFFS.md` against the newly-synced methodology" (a past account naming the ledgers), "`FRAMEWORK_LEARNINGS.md` #19's exact failure" (a document cited).
- **`church_growth` (9):** past accounts and citations: a grep that found ~80 hits "inside `CHANGELOG.md`, `HANDOFFS.md`, and past `SESSION_NOTES.md` session entries", a `[WIP]` commit with "no `CHANGELOG.md` entry, no completed `HANDOFFS.md` receipt", `SESSION_RUNNER.md` FM #11/#20, `BOOTSTRAP.md`, `methodology_dashboard.py:1209-1243`, `SAFEGUARDS.md`'s blast-radius principle.

**None of the 17 says where a file was or is** (a search of all 152 changed lines for "root", "top-level", "used to", "formerly", "previously", "was at", "moved", "relocat", "old" and "legacy" found 8 lines, none among the 17). **In every one the changed path names a file that exists at its new place after the move**, so the rewritten line is still true of the file it names. The nearest thing to a falsified line is a past account whose path now reads `methodology/CHANGELOG.md` where the July grep ran against `CHANGELOG.md`: the file is the same file.

## 5. Limits, stated where the number is

- **n is small:** 17 lines, 6 adopters, one reader. "None is false" is my reading, not a machine test; a line that says "at the repository root" about a moved ledger would be false after the rewrite, and none of the 17 does.
- **The Learnings test is a heading containing "earning".** A project that names the section otherwise is counted as outside; the 135 outside lines were not read one by one here (the register's concern was the Learnings).
- **The mapping is the manifest's whole table**, an upper bound for an adopter that has not synced every file; the 12 adopters are the ones on this machine at the run, so the output is a measurement of 2026-10-10.
- **Three adopters keep their learnings in `PROJECT_LEARNINGS.md`** (`nprcgenekeepr`, `mts-system`, `wsfct`: 451 learnings in `wsfct`'s). The tool does not rewrite that file (`plan_rewrites` edits only `.gitignore`, `CLAUDE.md`, the two configs and the ledger); it is prose, so where it names a moved path the tool counts it under `other` and leaves it, like the rest of the project's prose. The rule is therefore uneven by file, not by section: `CLAUDE.md` is rewritten because it is read as live instructions every session, and a project that keeps its history in another file keeps it untouched.

## 6. The decision (his, 2026-10-10)

| Option | What it would do | Why not / why |
|---|---|---|
| **Keep the rewrite, close F16 (chosen)** | nothing in the tool; this record and a dated line under the row | 17 of 17 lines stay true; the diff is already printed before an apply, which is the review point |
| Keep the rewrite and report the lines under a Learnings heading | a count and list in the dry run; tool change, tests, a higher `migrate-layout-unit-tests` floor | it directs attention to lines the measurement shows are fine, and still does not tell a live pointer from a past account |
| Skip Learnings and list instead (my first suggestion) | those lines left unchanged and listed | leaves live pointers and a runnable command stale at 6 adopters to protect 17 lines that were never false |

**What would reopen F16:** a line inside a Learnings region that states where a moved file is or was ("at the root"), found in a real adopter's `CLAUDE.md` or at an adopter's own dry-run diff. The first such line is a finding of the F5 kind; this measurement has none.

## 7. Not done

No adopter was touched, no tool or test changed, no gate floor moved, and nothing was sent upstream. F6, F8, F12, F13 and F14 still await his triage.
