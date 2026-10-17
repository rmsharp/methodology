# PR4's text, drafts 4 to 9: the record (2026-10-15 and 16)

At his direction, after he read draft 3 and found it "too difficult to understand" for its jargon: recompose the whole text in plain, formal language ("Clarity does not imply informality such as 'Hi'"; the
salutation `@KJ5HST:` stays). The text is [`../upstream-pr-body.md`](../upstream-pr-body.md) (everything below its first rule). Local only; nothing is sent to `KJ5HST/methodology`.

## 1. The answer

**Draft 9** (`docs/planning/upstream-pr-body.md`) is the text now. **It has had no read of its own.** Four fresh readers read drafts 4, 5, 6 and 8; each was given only the text that would be posted, read-only, no repository.

| Draft | Frozen at | Body | Reader | Rating | What it found that was true |
|---|---|---|---|---|---|
| 3 | `025afed` (figures `ab4f563`) | 18,479 B, 3,038 words | two reviewers (S327) | | the jargon he named; length |
| 4 | `d5bb53b` | 21,650 B, 3,563 | A, told the framework may be unfamiliar | 5 / 10 | my wrong "your open pull request #94"; contradictions inherited from draft 3; ~12 undefined phrases; informal wording |
| 5 | `9becf89` | 23,559 B, 3,878 | B, told the same | 5 / 10 | "everything you need to decide" was false; an unsupported sentence about moved projects; misplaced and mislabelled items |
| 6 | `dfc31ab` | 23,751 B, 3,893 | C, **told the maintainer knows his own framework** | 6 / 10 | the "at least 56" claim; Test 15 misplaced by me; undefined limits and thresholds; missing motivation and the "no" branch |
| 7 | `93245dc` | 25,959 B, 4,326 | none | | |
| 8 | `faffc98` | 19,990 B, 3,325 | D, told the maintainer knows his vocabulary (as C was) | 5 / 10 | ambiguities of mine: "I asked for it", which hook, whose remedy, unlettered rows, "the master", "main"; the effect of dropping the ten commits was lost in the cut |
| 9 | (the S332 close-out commit) | 20,117 B, 3,322 | none | | |

Readers A and B were told the framework might be unfamiliar, so they flagged words the maintainer coined himself (ledger, ratchet, gates, receipt). That test design over-counts; C was told otherwise and its
findings are the ones that mostly concern what the maintainer would actually not follow. **The text is longer at every draft** (draft 3 to draft 7: +7,480 B): each definition and each decision made self-contained cost words.
All three readers said the whole text is too long for deciding whether to engage; C said the first part (about 1,300 words) is the right size. Draft 7's decisions come first (8,102 B, about 1,330 words).
**S332 cut draft 7 by 23% to a byte budget stated before the edit (20,000 B)**: the commit table, the 12-projects and conflict paragraphs, one weak evidence row and the rebuild offer his picker left unticked; draft 9 lands at 20,117 B
(0.6% over, after the fixes below were paid for by further cuts). **Ratings by reader: 5, 5, 6, 5 of 10.** They stopped moving, so they stopped being informative; what stayed informative is each reader's list of specific failures.
Reader D's own framing is the honest summary: "the structure is good, but the density of numbers, private script names and unseen commits makes me re-read most paragraphs." A text for a change of this size may not get above that.

## 2. Every finding was a claim, checked before it was acted on

**Mine, introduced or kept, and now fixed:**

- Draft 4's Summary said "your open pull request #94". #94, #92 and #93 are the contributor's own (`gh`: #94 and #92 by rmsharp, #93 by rmsharp; #67 and #73 by KJ5HST). Draft 3 had said only "#94".
- Draft 4 listed the Test 15 rewrite (`4c0bdde`) as work "not about the directory". It is caused by the layout work: `bin/status` now prints a `layout:` line that names the project, and the old assertion counted 31 lines for 30 files. Draft 6 had moved it out of its group; draft 7 restores it.
- Draft 3's "at least 56 added lines of that kind remain" cannot be supported by a pattern with false positives (`Learning #N` rows are upstream's own). It now says the search *matches* 56 lines and that some may be legitimate.
- Draft 3's "my fix for #93 as its own commits" is false (the fix is inside `bbe0dc3`); "separate commits, so you can take or leave them" contradicted `c8c0b21` depending on `fd96593`; "that gate" named the budget tool, which is not one of the 18 gates; the five new risk rows read as four (the dashboard has 2 + 2 + 1); "41 across six projects" stood beside "7 under `methodology/`" (23 files at each of 7; 41 seeds at six).
- Draft 5's "that is everything you need to decide" was false until the dashboard detail moved into decision 2; draft 5's sentence about this branch's sync at moved projects rested on an inference (now measured, `pr4-moved.sh`: upstream's plain sync writes 30 paths outside `methodology/`, this branch's 0).
- In conversation I told him I had pasted the text "exactly" and had added "upstream-facing" to one bullet; the file was right. And I told him the dashboard timings were "within 0.03 s"; that was an ad-hoc run on this repository's 2,490-commit history; the saved script's largest difference is 0.09 s.

**Facts read from the sources for the definitions (none from memory):** the limits are an agent's file read (cut short past about 25,000 tokens, counted at 2.27 B/token, the densest content measured, 56,750 B; refused outright past 256 KiB), `starter-kit/methodology_dashboard.py` comments above `READ_CAP_TOKENS`; what a rewrite cannot do safely, `bin/migrate-layout` (`Unsafe`); the before-and-after checks, `run_checks`; ignore mode, `is_ignore_mode`; the two configuration files, `CONFIG_FILES`; why 36 links became plain names, `layer6c-record.md:31`; the exception for a file in both places, `tools/layout_resolver.py`'s docstring; `bbe0dc3` alone against #94 (`git merge-tree`: 6 regions in 2 files); every trimmer commit in upstream's history carries `TRIM_VERSION` (4 of 4); the motivation, his request of 2026-10-06 (`methodology-subdirectory-plan.md:9`), and a search of upstream's issues today that found none asking for it.

**Not acted on, and why:**

- The framework-vocabulary findings of readers A and B (proof, ledger, trimmer, gate, ratchet, receipt, seed): terms the maintainer coined. Defined by file name at first use only where it costs a few words.
- "Cut a quarter" lists (the commit table, the grep, the 12-projects paragraph, the conflict paragraph): the grep moved out of the table and the conflict paragraph shortened; the table and the 12-projects paragraph stay (adopter impact; navigation). His call.
- Reader C's "why can `c8c0b21` not be rebased so the ratchet fix survives a no?": **not answered by a test**; the text says the other commits have not been tested without the directory work. Draft 7 offered a separate pull request; his S331 picker did not tick that offer, so draft 8 removed it.
- Reader C's "the sync tools are justified by projects moved with this unmerged tool: circular": rephrased to say that once a project can move, the sync tools must change with it; the measurement is now `pr4-moved.sh`.

## 3. S332: reader D's findings on draft 8, each checked

**Fixed in draft 9 (errors or ambiguities in my wording; each re-read against its source):**

- "I asked for it": read as asking the maintainer. Now "I wanted it for my own 12 projects".
- "A ledger hook that a project installed itself": which hook. It is the ledger pre-commit hook that `SAFEGUARDS.md` describes (a project copies it into its own `.githooks/`; `.githooks/pre-commit` here is the reference copy). Named in decision 1 and in "Known gaps"; "the migration reports such a hook and leaves it" is from the tool's own report.
- "a remedy that rewrote 26 files in 25 repositories": whose. Now "#67 ... found that the old warning advised a `--sync` that rewrote 26 files across 25 repositories".
- The risk rows and the removed tests had no letter; now (d) and (e). "such as a backlog ... the trimmer can archive it": the trimmer archives ledgers, not a backlog; now "a ledger or a backlog ... lower severity if the project's own trimmer can archive it" (the code lowers the severity when the project's trimmer lists the file).
- "the limits": unsourced and tied to an unnamed agent; now "the limits I measured for an agent's file-read tool" (the comments above `READ_CAP_TOKENS` record the measurement). The 2.27 and 2.81 ratios: the cost line now says 2.81 is "the runner's measured" rate.
- "that file's own rule": now "the note in that file asks when the file changes" (BL-113's record, §5).
- Dropping the ten commits: the cut had lost "those references stay"; restored. The 56-line count and its command were dropped from the text (a regex with false positives gave the number; "not exhaustive" says what is true).
- "pr4-*.sh reads like my PR #4": the parenthetical (my own numbering, not pull request numbers) is back. `c8b9ddd` and `e7b389f` "I can't see": the intro now says they are on my fork's `main`.
- `--tier 1` used before it is defined: "(below)". "the master": now `tools/layout_resolver.py`; the reason for 11 copies now covers the six repository-only tools ("so one test covers all 11"), which the reader said it did not.
- "the last commit of each group": groups no longer exist after the table was cut; now "at points through the series, not at every commit". "the bin/sync on main": now "upstream's `bin/sync`" (three places). "templates that only a new project receives": now "the sources of seeds".
- "a ledger too small ... fails": now says a project with a very short ledger must add entries first (the tool's own message). "Its 280 tests" beside 261 to 302: now "its own suite of 280 tests (separate from `bin/tests.sh`)".
- Moved projects: the 23 framework files per moved project were lost in the cut; restored beside the 41 seeds (the fixture's 30 is a new project's full set, the real projects' 23 + 41 is a different count, as the text now reads).
- What `bin/sync` does by default: stated (`auto` keeps the layout a project has and gives an empty project the current one; `bin/sync --help`).

**Not acted on, because only he can answer, or because it needs new work:**

- **A recommendation for each decision.** The text asks four questions and recommends nothing. Whether it should is his call.
- **An itemised list of the dashboard changes 2.11.3 to 2.21.0**, and a reason for (b) (`"methodology"` out of `EXCLUDE_DIRS`): the text says they are not itemised; he can supply the reason.
- **What the 20 lines of #94 that differ change in behaviour**, and what happens to #94 if it is superseded: `pr4-supersede.sh` prints the lines; the consequence is his decision.
- **An assurance that none of the maintainer's own changes since `c8b9ddd` are lost** by sending whole files for the dashboard and the trimmer. **This is a real gap that I did not check**: a script like `pr4-supersede.sh`, over upstream's changes to those files since `c8b9ddd` against the branch's copies, would answer it. The text's (a), (c) and (e) disclose the changes I know of. Whether to do it before sending is his call; it is the one finding I think a maintainer would most want answered.
- **What `bin/migrate-layout` did on the 12 projects.** The text reports only the gaps; the run over the 12 adopters in `--no-local` clones exists (`docs/planning/methodology-subdirectory-evidence/migrate-12-adopters.py` and its output) and was not re-read for this text.
- **Wall time of the added suite**, **whether intermediate commits pass**, **an adopter-facing migration guide**: not measured, not asked in the plan, not written.
- The ledger-hook gap is described as a regression by the reader: the text states it plainly and in decision 1; whether it blocks the pull request is his and the maintainer's.
- "Cut another tenth": the reader's list (the ledger-hook gap stated once, the conflict detail, the timing ranges, the Test 15 bullet, the 2.27 derivation, the grep command, `5afc962`) was applied in part (the timing ranges, the 2.27 derivation and the grep command are cut; the conflict detail was already shortened in draft 8; the ledger-hook gap is still stated twice, in decision 1 and in "Known gaps"); the Test 15 bullet stays (it discloses a change to one of the maintainer's own tests) and `5afc962` stays (it is a change to `starter-kit/HANDOFFS.md` and `HOW_TO_USE.md`).

## 4. What is open for him

1. **The text itself**: post as it is, change it, or hold. *Answered at S336: draft 10 approved as the pull request's text and held for PR5 (§6).* Draft 9 has no read; a fifth read costs about 85,000 subagent tokens and three minutes, and four reads have rated 5, 5, 6 and 5 of 10.
2. **The check in §3 that I did not do: DONE at S333, §5.** Its two findings were settled at S333 and carried out at S336 (§6).
3. **A recommendation per decision, the reason for (b), the itemised dashboard changes** (§3).
4. **A known false warning stays in the pull request**: the migration warns that the hook `context_budget.py install-hook` writes "will refuse the migration commit"; it does not. The text says so under "Known gaps". Fixing it before sending is a build session.
5. Unchanged from `pr4-record.md` §5: D1 (the open findings and the waiver), D4 (#94 and #92), what the pull request carries besides the series, the push, PR5.

## 5. S333: do the maintainer's own lines survive the whole files? (the check §3 left open)

Scripts: `pr4-survive.py` (output `pr4-survive-output.txt`) and `pr4-oracle.sh` (output `pr4-oracle-output.txt`). Both read git objects only, from `f34769f` (upstream) and `a62bfec` (the candidate), so they give the same output from any checkout.

**The answer.** He has changed nothing since `c8b9ddd`: `f34769f` (2026-10-02) is an ancestor of `c8b9ddd` (2026-10-06) and is still `upstream/main`, so no change of his can be lost *since* then. What can be lost is a line of his in `f34769f`'s copies that the 32 commits remove or rewrite. **Every such line is accounted for by a change the text names (two of them only in part), except one (F2), and the reason the text gives for removing two of his tests is wrong (F1): both are his to settle.** Upstream's own tests agree: 417 of the 422 in the three unit-test files for these tools do not fail against the candidate's code, and each of the five that do fails on a pinned version, a pinned piece of source text, an import list or a disclosed change.

**What was counted.** The 32 commits remove or rewrite 1,152 lines of upstream's copies in 38 files (git's own deletion count; the script's total equals it). He wrote 487 of them (blame at `f34769f`; the authors `KJ5HST`, `Terrell Deppe`, `Terrell`); counting the dashboard's byte-identical twin once, 366 of 865. Of his 476 non-blank lines: 38 are still in the file as exact lines, 48 are the same line followed only by a `# layout: ok` comment, 31 are inside a longer or re-wrapped line (all 31 read by eye: reflowed prose, a lone `),`, and calls and returns that now carry the layout table or `out_dir`; none removes a behaviour of his) and **359 are gone (279 with the twin once)**. The trimmer has **0** of his lines: all four commits that touch it are the fork operator's. Each of the 279 is assigned a reason by file and line range in the script's table (a judgment, written out so it can be disputed one range at a time); none is left without one:

| Reason | Lines | Where the text says so |
|---|---|---|
| the `methodology/` directory work (the resolver, names in constants, messages) | 113 | decision 1; "What a project sees" |
| (e) the four tests removed | 59 | decision 2 (e) |
| (a) `--sync [DIR]`, the `--force` gate, the stale-copy remedy | 32 | decision 2 (a) |
| (c) one table for installed-source recognition | 25 | decision 2 (c) |
| the ratchet's `timeout_seconds` | 16 | the `c8c0b21` bullet |
| a version constant, its pin, the re-recorded bytes per token | 9 | decision 2, decision 4 |
| the runner's task table (paths relative to the runner) | 7 | in part: the text names the first paragraph |
| five gate thresholds raised (all `min`, so tighter) | 5 | in part: the `bbe0dc3` bullet says three; later commits raise those three again and two more |
| the dashboard's gate-history walk is first-parent (2.21.0) | 4 | **no** (F2) |
| (b) `"methodology"` out of `EXCLUDE_DIRS` | 3 | decision 2 (b) |
| `first_commit_date` reads the root commits | 3 | the `bbe0dc3` bullet |
| `bin/tests.sh`: executable bit from the manifest, the skip count | 2 | the `bbe0dc3` bullet |
| `starter-kit/HANDOFFS.md`: the unmeasured-gate rule | 1 | the `5afc962` bullet |

**Upstream's tests as the oracle** (`pr4-oracle.sh`; some of the tests are his, some the fork operator's). The three unit-test files at `f34769f`, unchanged, run against the candidate's code: the ratchet 44 of 45 (the failure is `test_stdlib_only`: the import allow-list gained `signal`, `time`, `pathlib`); the budget tool 147 of 148 (`test_the_head_baseline_comes_from_heads_config_not_the_staged_one` pins the *source text* `f"HEAD:{CONFIG_NAME}"`; the candidate reads HEAD's config through `head_config_text(root)` and its copy of the test pins that; the behavioural tests of that class pass); the dashboard 226 of 229 **after one fixture line** (his `base_metrics` builds a metrics dict without `read_cap_watch`, which the candidate's new risk rows (d) index directly; without that line 14 tests raise `KeyError`; the candidate's test file adds the key). The three dashboard failures are `test_dashboard_version` (the pin), `test_stale_warning_leads_with_the_project_scoped_remedy` ((a)) and `test_every_framework_installed_source_name_has_a_signature` ((c)). Also: the ledger hook's selftest (his hook) has 17 labelled checks at `f34769f`; 16 appear word for word in the candidate's selftest (the 17th is reworded, "a `docs/archive/` shard" to "a shard in the legacy archive directory"), which passes (43 checks); all 34 numbered tests of `bin/tests.sh` are present with their titles (3 added); by name, **4 of upstream's 553 tests are absent from the candidate, the four the text names** (an earlier count of 10 was a renamed class, not a loss). The series raises five thresholds and adds six gates; it lowers none and removes none.

**F1. (e) is exact about the count and loose about the reason.** The text says the three tests in `TestCliRemedyProportionality` go "because (a) replaces the remedy they assert". Only one of the three asserts a remedy and fails on the candidate's code (`cp ` in the warning). The other two pass on it: `test_bare_dry_run_refuses_instead_of_writing` (exit 2, nothing written), which the candidate's own Row 13 test also asserts, and **`test_a_normal_run_still_writes`**, a presence control for exactly the failure the first one could hide. For a copy kept at the project root the candidate has no counterpart: its only positive assertion that a plain run writes `dashboard.html` is for the `methodology/` layout (`tools/test_methodology_dashboard.py` at `a62bfec`, line 6795). Two ways to settle it, his: restore the two tests on the candidate (a build session: the head moves, `pr4-claims.sh` again, about 35 minutes, and `dashboard-unit-tests` can rise by 2), or change the sentence in (e) to say that two of the three assert behaviour the candidate keeps and are dropped anyway.

**F2. A change to his code that the text does not itemise.** `_gate_manifest_history` and `has_manifest_history` walk the manifest's history with `git log --first-parent` (2.21.0). Effect: the comparison is one line of ancestry, so a merge of two lineages no longer prints a "floor lowered" nobody lowered, and a loosening resolved into a merge is compared with the line it landed on; a loosening made on a side branch is reported at the merge that carried it in. Decision 2 says the other changes in `bbe0dc3` are not itemised, so the text is not wrong, but it changes what his dashboard reports about the ratchet he wrote. One sentence in decision 2 would name it.

**F3. Minor, no action proposed.** The runner's task table (7 of his lines) now gives workstream paths relative to the runner (`workstreams/DESIGN_WORKSTREAM.md`, not `docs/methodology/workstreams/...`); the text names the first paragraph, which is what resolves them for a legacy project (`SESSION_RUNNER.md` line 7).

**Not checked.** `bin/tests.sh` at `f34769f` was not run against the candidate (7 minutes, 300 to 375 assertions; its four changed lines of his were read). The gone-line reasons are by range from reading each hunk, not by running anything; the first-parent walk was read, not run on a merged history. Files the candidate adds carry no upstream line to lose.

**His answers at the S333 close-out (2026-10-16), neither carried out yet.** F1: **restore the two tests** on `pr2/candidate` (the upstream class is `git show f34769f:tools/test_methodology_dashboard.py` lines 2410 to 2482, its helper `_project` at 2423; the candidate's file has a "deliberately not carried" note in its place, which the build rewrites). F2: **name the first-parent walk in one clause** in decision 2. Both change draft 9, so they belong together in a draft 10 built after the restore. The restore moves the candidate's head from `a62bfec`, so `pr4-claims.sh` runs again and the text's figures (32 commits, the shortstat, `dashboard-unit-tests` 395 to 397) change; item (e) then reads "two of your tests are removed" (the `cp ` remedy test, because (a) replaces what it asserts, and the signature test, because of (c)). Where the restore lands is a design point for that build: a new top commit keeps the other 31 hashes, but `bbe0dc3` taken alone (decision 1's fallback) would still lack the two tests; putting it inside `bbe0dc3` rebuilds the 31 commits above it, which he declined once (the unticked rebuild offer).

## 6. S336: draft 10 (F1 and F2 carried out, decision 3 re-measured)

Both decisions of §5 are done: F1 on the branch (`cfcc713`, the 33rd commit, [`restore33-record.md`](restore33-record.md) §1 and §2), F2 in the text. Draft 10 (`9ecd0a8`) is draft 9 with the ten edits and three cuts listed in that record's §5; `pr4-body-check.py` exit 0 against `cfcc713`; the body is 20,863 B, 863 B over the 20,000 B budget (F2 +273 B, (e) and decision 3 +492 B, the commits paragraph +85 B, the cuts -104 B). New since draft 9 and not a §5 finding: PR #94 gained a fourth commit (`2308553`, 2026-10-17) between draft 9 and this build, so decision 3's figures changed (conflicts 3 files and 17 regions to 4 files and 22; #94's lines absent from the branch 11 and 9 to 77 and 294; `bbe0dc3` alone 6 regions to 13), and the text now says the branch carries the #93 fix as #94's first three commits had it and not the fourth, and that both trimmers are named 1.8.0 (that record's §4). No read of draft 10. His answers at the S336 picker, after the text was shown inline: draft 10 is approved as the pull request's text and held for PR5 (nothing sent; D1 and D4 come first), and the 863 B are kept, the additions being facts. §4 item 1 is closed by that; the size paragraph of `restore33-record.md` §5 is the account.
