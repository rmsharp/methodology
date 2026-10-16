# PR4's text, drafts 4 to 7: the record (2026-10-15 and 16)

At his direction, after he read draft 3 and found it "too difficult to understand" for its jargon: recompose the whole text in plain, formal language ("Clarity does not imply informality such as 'Hi'"; the
salutation `@KJ5HST:` stays). The text is [`../upstream-pr-body.md`](../upstream-pr-body.md) (everything below its first rule). Local only; nothing is sent to `KJ5HST/methodology`.

## 1. The answer

**Draft 7** (`docs/planning/upstream-pr-body.md`) is the text now. **It has had no read of its own.** Three fresh readers read drafts 4, 5 and 6; each was given only the text that would be posted, read-only, no repository.

| Draft | Frozen at | Body | Reader | Rating | What it found that was true |
|---|---|---|---|---|---|
| 3 | `025afed` (figures `ab4f563`) | 18,479 B, 3,038 words | two reviewers (S327) | | the jargon he named; length |
| 4 | `d5bb53b` | 21,650 B, 3,563 | A, told the framework may be unfamiliar | 5 / 10 | my wrong "your open pull request #94"; contradictions inherited from draft 3; ~12 undefined phrases; informal wording |
| 5 | `9becf89` | 23,559 B, 3,878 | B, told the same | 5 / 10 | "everything you need to decide" was false; an unsupported sentence about moved projects; misplaced and mislabelled items |
| 6 | `dfc31ab` | 23,751 B, 3,893 | C, **told the maintainer knows his own framework** | 6 / 10 | the "at least 56" claim; Test 15 misplaced by me; undefined limits and thresholds; missing motivation and the "no" branch |
| 7 | (this commit) | 25,959 B, 4,326 | none | | |

Readers A and B were told the framework might be unfamiliar, so they flagged words the maintainer coined himself (ledger, ratchet, gates, receipt). That test design over-counts; C was told otherwise and its
findings are the ones that mostly concern what the maintainer would actually not follow. **The text is longer at every draft** (draft 3 to draft 7: +7,480 B): each definition and each decision made self-contained cost words.
All three readers said the whole text is too long for deciding whether to engage; C said the first part (about 1,300 words) is the right size. Draft 7's decisions come first (8,102 B, about 1,330 words).

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
- Reader C's "why can `c8c0b21` not be rebased so the ratchet fix survives a no?": **not answered by a test**; the text now says the other commits have not been tested without the directory work and offers a separate pull request. That offer is a commitment of his work: he should confirm it.
- Reader C's "the sync tools are justified by projects moved with this unmerged tool: circular": rephrased to say that once a project can move, the sync tools must change with it; the measurement is now `pr4-moved.sh`.

## 3. What is open for him

1. **The text itself**: post as it is, change it, or hold; it is long (25,959 B); the reference tier (everything after the decisions, size and cost) could lose the commit table and the 12-projects paragraph.
2. **A fourth read**: draft 7 changed after the third read and has none; a fourth costs about 85,000 subagent tokens and three minutes.
3. **The offer in decision 1** to rebuild any commit as a separate pull request (the text commits him to it).
4. **A known false warning stays in the pull request**: the migration warns that the hook `context_budget.py install-hook` writes "will refuse the migration commit"; it does not. The text says so under "Known gaps". Fixing it before sending is a build session.
5. Unchanged from `pr4-record.md` §5: D1 (the open findings and the waiver), D4 (#94 and #92), what the pull request carries besides the series, the push, PR5.
