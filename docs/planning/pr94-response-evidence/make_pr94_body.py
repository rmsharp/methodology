"""Build the revised PR #94 description from the one now posted (docs/planning/pr94-rewrite/body.md).

Usage: python3 -I make_pr94_body.py <repo-root>

Every replacement asserts that its anchor occurs exactly once, so a body that is not the one this was
written for fails loudly. Writes docs/planning/pr94-response-evidence/pr94-new-body.md.
"""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
body = (root / "docs/planning/pr94-rewrite/body.md").read_text(encoding="utf-8")


def once(text, old, new, what):
    assert text.count(old) == 1, "%s: expected exactly one match, found %d" % (what, text.count(old))
    return text.replace(old, new)


def between(text, start, end, new, what):
    """Replace text[start:end) where `start` and `end` each occur once; `end` is kept."""
    assert text.count(start) == 1, "%s: start found %d times" % (what, text.count(start))
    i = text.index(start)
    assert text.count(end, i) >= 1, "%s: end not found after start" % what
    j = text.index(end, i + len(start))
    return text[:i] + new + text[j:]


# ---- Summary ---------------------------------------------------------------------------------
body = between(body, "## Summary\n", "## Background\n", """## Summary

This PR changes `methodology_trim.py` (the trimmer), the tool that moves the oldest records out of a growing file into an archive file and writes a script, a *proof*, that re-checks that nothing was lost. Issue #93 reports 10 of 54 proofs, in one project, failing on trims that lost nothing, and traces them to three causes. This PR has 14 commits. The first fixes one cause (2 of the 10 proofs). The second teaches the proof to recognise the shape behind most of the other 8, a trim committed together with the finishing of a session's placeholder record, and to name it instead of printing generic failures. The third adds a command, `methodology_trim.py --reverify <shard>` (a *shard* is an archive file that an earlier trim wrote), that builds a new proof for a shard from the current template and runs it, so a shard whose proof was written earlier gets a second verdict. The fourth makes the proof print the diff of the placeholder against the record that replaced it, and the fifth makes an abort before the proof's checks exit 3 instead of 1. Commits 6 to 14 answer a review of the first five; see "Changes since the first review". An earlier version of this PR also added the project's third ledger, `SESSION_NOTES.md`, to the trimmer's table; at the reviewer's request that change is now a separate pull request.

Under `--reverify`, 46 of the 54 proofs pass and 1 is named as a stub finalize (exit 4, with the diff printed). The other 7 are `SESSION_NOTES.md` shards: they keep the generic exit 1 until the separate pull request lands, and with it all 8 are named at exit 4. The named ones stay FAILs by design, for the reason "What remains" explains. Whether a named FAIL with its diff answers the report is for issue #93's author; this PR does not close the issue.

""", "summary")

# ---- Background ------------------------------------------------------------------------------
body = once(body,
    "Before this PR the table had two entries: `CHANGELOG.md` (one record per action) and `HANDOFFS.md` (one record per session, called a receipt). The fourth commit adds a third, `SESSION_NOTES.md` (one or two records per session; see Commit 4). When it trims,",
    "The table has two entries: `CHANGELOG.md` (one record per action) and `HANDOFFS.md` (one record per session, called a receipt). When it trims,",
    "background table")
body = once(body, "(the text below the last record; `HANDOFFS.md` and `SESSION_NOTES.md` have none)",
            "(the text below the last record; `HANDOFFS.md` has none)", "footer clause")
body = once(body,
    "The table in this repository's `methodology_trim.py` had no such entry before this PR's fourth commit.",
    "The table in this repository's `methodology_trim.py` has no such entry; the separate pull request adds it.",
    "no entry")

# ---- What this PR changes --------------------------------------------------------------------
body = once(body,
    "The four share the proof template and its tests, so they are one change set.",
    "They share the proof template and its tests, so they are one change set. Commits 4 and 5 replace the commits of the same names in the first version of this PR (see \"Changes since the first review\").",
    "one change set")
body = once(body,
    "The *timing rule* avoids the problem: trim while record 0 is complete, that is, before the claim or after the finalize is committed, never in the same commit as the finalize.",
    "The *timing rule* avoids the problem: give the trim a commit of its own, never in the same commit that edits record 0. (This commit stated the rule more strongly than the proof enforces; Commit 13 corrects the wording.)",
    "timing rule")

body = between(body, "**Commit 4 (", "**Commit 5 (", """**Commit 4 (`TRIM_VERSION` 1.8.0): the proof prints the record-0 diff.** Whenever the proof sees the finalize pattern (record 0 edited in the trim commit, for a recognised stub finalize at exit 4 and for the generic case at exit 1 alike), it prints, after its `FAIL:` and `NOTE:` lines, a unified diff of record 0 before the trim commit against the record that replaced it, headed `DIFF: record 0, ...` with the line count. This is issue #93's first suggestion. The diff is output, not a verdict: it changes no exit status, and a record other than record 0 that differs gets no diff, because that is a plain loss (Commit 11 extends this to a record 0 edit beside other records moving). Three tests; 7 mutants of the printing code (never printed, printed for any missing record, printed only for the recognised case, reversed, header dropped, lines dropped, the wrong record compared) are all caught. Minor, not patch: new proof output, no verdict changes.

""", "commit 4")

body = once(body, "the `trimmer-unit-tests` gate 199 → 203; the 54 proofs read the same under 1.8.1 as under 1.8.0.",
            "the `trimmer-unit-tests` gate 184 → 188; the 54 proofs read the same under 1.8.1 as under 1.8.0. (Commit 6 refines which aborts are exit 3: a path missing from a commit the clone can read is a FAIL.)",
            "commit 5")

# ---- Changes since the first review (new) ----------------------------------------------------
body = between(body, "## Where to read closely\n", "`--reverify` reads values out of a proof file", """## Changes since the first review

Commits 6 to 14 answer the nine points of the review of the first version of this PR, one commit each, and add one fix the review did not ask for. Each has its own tests, its own record in `CHANGELOG.md` and a mutation round. Every point reproduced on a throwaway repository before any change was made.

| Point | What was wrong | What changed | Commit (number, hash) |
|---|---|---|---|
| 1 | A trim commit that also deleted the live ledger made the proof exit 3, "did not finish", where 1.5.0 exited 1: a total loss read as no verdict. | Exit 3 only for a commit, tree or blob the clone cannot read; a path absent from one it can read is a `FAIL:` line at exit 1 (also for a deleted file in the working-tree mode). | 6, `38419e9` |
| 2 | `python3 -` puts the working directory on the import path, so a `difflib.py` or `subprocess.py` at the repository root ran inside the proof (also under 1.5.0's template, for `subprocess`). | The proof's interpreter line is `python3 -I -`. | 7, `159e600` |
| 3 | The `SESSION_NOTES.md` table entry was part of this PR. | Commits 4 and 5 rebuilt without it; the entry is the `SESSION_NOTES.md` pull request. | 4 and 5, `e88d1fd` and `9a4bf79` |
| 4 | The timing rule was stronger than the proof: a trim committed on its own while record 0 is a stub passes. | The rule is "give the trim a commit of its own, never in the same commit that edits record 0", in the same words everywhere. (The `ACTIVE TASK` half concerns `SESSION_NOTES.md`'s front matter and goes with the separate pull request.) | 13, `5741d2e` |
| 5 | The `HANDOFFS.md` stub marker matched a `status: pending` line anywhere in a record, so a real loss from a complete receipt could be labelled a stub finalize (exit 4). | The line must sit inside the receipt's own fence. | 8, `261a7b2` |
| 6 | `--reverify` did not lift `PREFIX`, so a proof written for another depth read exit 1. | `--reverify` refuses such a proof at exit 3, naming both values. | 9, `ec4e7df` |
| 7 | A carriage return in `RECORD_START` made the spliced proof a `SyntaxError`, read as exit 1; a NUL crashed `--reverify` itself. | Both are refused at the lift, exit 3. | 10, `ad46648` |
| 8 | The frontier note and the record-0 diff said nothing of other records that had moved. | They are printed only when no other record moved; otherwise a note says the others did. | 11, `d53f68f` |
| 9 | Narrowing `other_fails` to one failure kind passed every test. | Five tests pin the other kinds (tests only). | 12, `252613c` |
| extra | The proof ignored a failure of the `git log` walk that finds the trim commit, so a failed walk read as "not committed yet" and the proof printed `OK` having compared nothing (also under 1.5.0). | A failed walk is exit 3. Separable: drop the commit and the nine stand. | 14, `1670c5d` |

""" + "## Where to read closely\n\n", "changes since the first review")

body = between(body, "The new `SESSION_NOTES.md` entry's stub marker is a regular expression", "## What remains", """`--reverify` now also refuses, by name and at exit 3, a frozen proof whose `PREFIX` line is missing, repeated, not in the form the template writes, or not `"../../"` (Commit 9), and one whose `RECORD_START` line carries a carriage return or a NUL (Commit 10). Each has tests that build the hostile proof and assert the refusal.

`HANDOFFS.md`'s stub marker is now `\\A(`{3,}|~{3,})handoff[^\\n]*\\n(?:(?!\\1)[^\\n]*\\n)*?status: pending[ \\t\\r]*$` under `re.M`: the line must be inside the fence that opens the record, whose own opening run closes it. It is a lazy line-by-line scan, linear in the record; a test searches a 400,000-line record that has no marker. The diff is built with Python's `difflib` from the two record texts the proof already holds.

""", "read closely tail")

# ---- What remains ----------------------------------------------------------------------------
body = between(body, "## What remains, and why the 8 stay FAILs\n", "## Evidence\n", """## What remains, and why the named ones stay FAILs

The authors of #93 ask for these false FAILs to stop. The original proof files do not change, so for a proof already written this PR can only add a second verdict, the one `--reverify` gives. Under that verdict, 2 of the 10 proofs pass and 1 is recognised as a stub finalize: a specific `FAIL:` line, exit 4, and the diff of the stub against the record that replaced it. The other 7 are `SESSION_NOTES.md` shards and still print the generic failures, with the diff, at exit 1 until the separate pull request adds that ledger to the table; with it all 8 are recognised.

Each of the 10 original proofs prints exactly one of three failure lines that tell the causes apart: `L2 FRONT MATTER leaked` is cause 2, `L3 record count 79 != 78` is cause 3, and `L3 1 record(s) present before the trim are MISSING` is cause 1. (The cause-1 and cause-3 proofs also print an L1 failure line, which does not tell the causes apart.) Sorting by line gives 7 proofs for cause 1, 2 for cause 2 and 1 for cause 3, which are the counts #93 gives.

| #93's cause | Failing proofs | `--reverify` result with this PR | with the separate `SESSION_NOTES.md` pull request |
|---|---|---|---|
| 1: a trim in the same commit as a finalize | 7: one `HANDOFFS.md` shard and six `SESSION_NOTES.md` shards | the `HANDOFFS.md` shard exits 4; the six `SESSION_NOTES.md` shards exit 1 | all 7 exit 4, named, with the diff |
| 2: L2 compares by substring | 2: one `CHANGELOG.md` shard and one `HANDOFFS.md` shard | both pass (exit 0) | both pass (exit 0) |
| 3: a proof already written | 1: a `SESSION_NOTES.md` shard, written by trimmer version 1.1.2 | exit 1 | exit 4, named, with the diff |

With the separate pull request applied, in each of the 8 the re-derived proof reports the finalize pattern: record 0 was a stub before the trim commit, a record with the same heading or `session:` line replaced it, and no other record differs. The cause-3 proof shows the same pattern, because its trim commit overwrote the stub as well as adding a record. The pattern stays a FAIL by design, because neither the original proof nor the re-derived one can tell it from a real loss: if the edit to record 0 had also deleted part of its text, the proof would see the same pattern, record 0 changed and everything else identical. In all 8 the finished record rewrote the stub's text; apart from the identifying lines, no line of the stub survives as a whole line in the finished record, and one stub carried 23 lines of prose written into it. #93's authors judged by hand that nothing of value was lost; a proof cannot, and a proof that exited 0 here would certify a replaced stub it has not read. What the proof can do is show the edit, which is what the diff is for: in these 8 the diff runs from 30 to 176 lines (all 8 print it with this PR alone), and a reader sees in seconds that the removed lines are the placeholder's and the added lines are the session's write-up.

""", "what remains")

# ---- Evidence --------------------------------------------------------------------------------
body = between(body, "## Evidence\n", "## Adopter impact\n", """## Evidence

- **Tests.** `tools/test_methodology_trim.py` goes from 124 to 227 tests (103 new). The `trimmer-unit-tests` floor in `.quality-gates.json` (the lowest test count the quality ratchet accepts) rises with each commit: 129, 154, 181, 184, 188, 196, 199, 206, 210, 213, 216, 221, 224, 227. In a clean `--no-local` clone of this branch's head, `quality_ratchet.py --run` reports 12 of 12 gates pass, 0 fail, 0 unmeasured (results `b49e29a9e5ea`, manifest `06181a10ec42`), and `bin/tests.sh` reports 261 passed, 0 failed. `bin/tests.sh` runs the trimmer's test file as one check, so the new tests do not change that total.
- **Mutation testing.** A mutant is a small deliberate breakage of the code; every commit's tests were run against its mutants. Commit 1: 9 mutants; 7 of them change behaviour and a test catches all 7, and the other 2 behave exactly like the original code, so no test can catch them. Commit 2: 37 mutants, all caught. Commit 3: 54 mutants, all caught. Those three rounds ran in my fork (`rmsharp/methodology`) when the code was first written there. Commit 4: 7 mutants, all caught. Commit 5: 6 mutants, all caught (run when it was written, against the code before Commit 6). Commits 6 to 14, run on this branch: 8, 3, 6, 3, 3, 4, 8, 4 and 2 mutants, all caught; for Commit 12 one further mutant ("every failure that starts with `L2`") survives, and is equivalent, because every failure string starts with `L1`, `L2` or `L3`.
- **The #93 repository.** A scratch clone at `82433662`: 54 proofs; 44 pass as written and 10 fail, the numbers the review reproduced. `--reverify` over every shard, by running the command itself: under 1.8.1 (this PR as first reviewed, with the `SESSION_NOTES.md` entry) 46 at exit 0 and 8 at exit 4; under this branch 46 at exit 0, 1 at exit 4 and 7 at exit 1; under this branch plus the separate pull request 46 at exit 0 and 8 at exit 4, row for row the same as 1.8.1. The fixes change no verdict among the 54. At that repository's HEAD, 2 of 59 proofs carry `PREFIX = "../"` (both under `methodology/archive/`): under 1.8.1 `--reverify` read the CHANGELOG one at exit 1 and the HANDOFFS one at exit 0, and this branch refuses both at exit 3. `--reverify` writes nothing.
- **The two existing ledgers' verdicts.** The 179 frozen shards of my fork (`CHANGELOG.md` and `HANDOFFS.md` shards, written by trimmer versions 1.1.1 to 1.8.1 of the fork's own line): proof as written, 174 at exit 0 and 5 at exit 1; `--reverify`, 176 at exit 0, 2 at exit 1 and 1 at exit 4 under 1.7.0 and the same under this branch, every exit code identical. All 179 still lift under the new `PREFIX` and `RECORD_START` checks.
- **This repository.** Its one existing proof exits 0 as written and under `--reverify` at 1.7.0 and at 1.8.2. In a throwaway clone (a scratch copy made for the test) of the branch at Commit 3, I trimmed its own `HANDOFFS.md` with `--cut 2 --force` (38 receipts, 221,642 B, above the 196,608 B size at which the trimmer says a trim is due). `--cut 2` keeps the newest 2 receipts; `--force` overrides the trimmer's refusal (`SRF_RED`) to trim a ledger that has regrown all the space its previous trim freed. The trim wrote a shard whose proof exits 0. In the same clone, with a pending stub committed as record 0, the trimmer printed `FRONTIER_PENDING_STUB`; finalizing the stub and trimming in one commit gave a proof that exits 4 with the specific `FAIL:` line and a `NOTE:` line stating the timing rule. (Measured at Commit 3 and not repeated at the later commits, whose tests cover the same shapes in scratch repositories.)
- **Sync.** `bin/sync --source local` from this branch into a throwaway project: `methodology_trim.py` and `FRAMEWORK_APPARATUS.md` arrive byte-identical to this branch's, and the project's copy reports version 1.8.2.
- **Merge.** `git merge-tree` of this branch against the branch of pull request #92 (the v4.2 release notes), which also prepends to `CHANGELOG.md`, and against `main`, reports no conflict for either. `CHANGELOG.md` has the `merge=union` driver, which keeps the lines added by both sides.
- **What the review did not test.** The two stub markers (this PR's and the separate pull request's) searched over a 400,000-line record with no match: 0.13 s and 0.17 s. A symlink where the proof reads a file: inside the trim commit the proof fails (exit 1, records missing); uncommitted, the working-tree read follows the link and passes, which becomes a FAIL once committed. Repository-local git config (`diff.external`, `core.pager`, `core.fsmonitor`, `core.sshCommand`, `core.editor` set to a script): none ran during the proof.

""", "evidence")

# ---- Adopter impact --------------------------------------------------------------------------
body = between(body, "## Adopter impact\n", "🤖 Generated with", """## Adopter impact

- `bin/sync` copies `methodology_trim.py` (from 1.5.0 to 1.8.2) and one paragraph of `FRAMEWORK_APPARATUS.md` into adopters. Commits 1, 2, 4 and 6 to 14 change only what a *new* trim writes and warns about and what a new or re-derived proof prints or refuses; commit 3 adds a flag. Nothing rewrites a proof already in an adopter's `docs/archive/` directory.
- **Exit codes mean more exactly.** A proof that finds a path absent from a commit or working tree it can read now exits 1 (it exited 3 under 1.8.1, and 1 under 1.5.0); a proof whose history walk fails now exits 3 (it printed `OK`). `--reverify` refuses more frozen proofs, at exit 3, by name: a `PREFIX` other than `"../../"`, a carriage return or a NUL in `RECORD_START`. A caller that treated 3 as "could not run" is unaffected.
- **Exit status 4 is new** for a generated proof. A caller that tests `== 1` rather than `!= 0` would miss exit 4. Nothing in this repository calls a proof that way (outside `docs/archive/`, the tests and the trimmer, `verify.sh` appears only in prose and a hook comment); an adopter's own script might.
- **A proof's output grows** when record 0 was edited in the trim commit: the diff is printed after the `FAIL:` and `NOTE:` lines, 30 to 176 lines in the 8 shards of the #93 repository. A proof whose checks hold prints nothing new.
- **The timing rule's wording changes** (in the trimmer's warnings, the proof's notes and `FRAMEWORK_APPARATUS.md`): "give the trim a commit of its own, never in the same commit that edits record 0". It no longer tells a session to wait for a complete record 0.
- **`SESSION_NOTES.md` is not in the table in this PR.** A project that carries its own table entry for it (the #93 repository does) is unaffected until the separate pull request lands. `bin/sync` stops on a locally edited `methodology_trim.py` (exit 2, naming the file, `--force` to overwrite), as it does for any local edit; this PR does not change that.
- The dashboard (`methodology_dashboard.py`) reads `TRIM_VERSION` with a regex, and the regex still matches.
- A newly generated proof differs from an older one in its text as well as its behaviour: new comments, one reworded comment (it no longer calls committing a finalize together with a trim this repository's practice), the reworded `NOTE:` lines, and the interpreter line `python3 -I -`.
- This is not a framework release; the only version that moves is the trimmer's own `TRIM_VERSION`.

""", "adopter impact")


# ---- Second pass: the fresh reader's findings -----------------------------------------------
SEP = "the separate pull request"
NOTES_PR = "the `SESSION_NOTES.md` pull request"

# Summary: the commit count and what "the notes pull request" is
body = once(body, "The second teaches the proof to recognise the shape behind most of the other 8, a trim committed together with the finishing of a session's placeholder record, and to name it instead of printing generic failures.",
    "The second teaches the proof to recognise the shape behind the other 8, a trim committed together with the finishing of a session's placeholder record, and, where the ledger table declares a stub marker, to name it instead of printing generic failures; in this PR that reaches 1 of the 8, and the other 7 are `SESSION_NOTES.md` shards (see below).", "summary c2")
body = once(body, "Commits 6 to 14 answer a review of the first five; see \"Changes since the first review\". An earlier version of this PR also added the project's third ledger, `SESSION_NOTES.md`, to the trimmer's table; at the reviewer's request that change is now a separate pull request.",
    "Commits 6 to 14 answer your review of the first version of this PR: eight of your nine points, one commit each, plus one extra fix (point 3, the split, is the rebuild of Commits 4 and 5); see \"Changes since the first review\". The first version also added the project's third ledger, `SESSION_NOTES.md`, to the trimmer's table; at your request that change is now the `SESSION_NOTES.md` pull request (not yet opened: branch `feat/trim-session-notes-ledger-issue93` of my fork, based on this branch's head `1670c5d`).", "summary p1 tail")
body = once(body, "they keep the generic exit 1 until the separate pull request lands, and with it all 8 are named at exit 4.",
    "they keep the generic exit 1 until the `SESSION_NOTES.md` pull request lands; once it has landed, all 8 are named at exit 4.", "summary p2")

# Orientation block
body = once(body, "Commits 4 and 5 replace the commits of the same names in the first version of this PR (see \"Changes since the first review\").",
    "\n\n**Orientation for a reader of the first version.** The head you reviewed was `1082d3b`; the current head is `1670c5d`. Commits 1 to 3 are unchanged (`68d8a06`, `965f136`, `972eb2c`). Commits 4 and 5 are rebuilt as `e88d1fd` and `9a4bf79`, without the `SESSION_NOTES.md` entry; they keep the version numbers 1.8.0 and 1.8.1 of the commits they replace but their content differs, so \"1.8.1\" below means the rebuilt Commit 5 unless it says `1082d3b`. Commits 6 to 14 are new and move `TRIM_VERSION` to 1.8.2. The table in \"Changes since the first review\" gives each commit's number and hash.", "orientation")

# Commit 2: the marker was narrowed later; the rule's old wording stated
body = once(body, "so a receipt that merely quotes the marker inside a longer line is not taken for a stub).",
    "so a receipt that merely quotes the marker inside a longer line is not taken for a stub; Commit 8 narrows this further, to a line inside the receipt's own fence).", "marker narrowed")
body = once(body, "(This commit stated the rule more strongly than the proof enforces; Commit 13 corrects the wording.)",
    "(This commit worded the rule as \"trim while record 0 is complete, that is, before the claim or after the finalize is committed\", which is stronger than the proof enforces; Commit 13 replaces that with the wording above. See \"Changes since the first review\" for what Commits 8 and 13 are.)", "rule paragraph")

# Commit 4
body = once(body, "(Commit 11 extends this to a record 0 edit beside other records moving)",
    "(Commit 11 also withholds the diff, and says so in a note, when record 0 was edited and other records moved as well)", "commit 4 ref")
body = once(body, "Minor, not patch: new proof output, no verdict changes.", "Minor version bump: new proof output, no verdict changes.", "minor not patch")

# Commit 5: the sweep
body = once(body, "the sweep behind this PR saw it once (exit 0 on the re-run)", "a run of `--reverify` over all 54 shards of the #93 repository (see Evidence) saw it once (exit 0 on the re-run)", "sweep")
body = once(body, "(Commit 6 refines which aborts are exit 3: a path missing from a commit the clone can read is a FAIL.)",
    "(Commit 6, in the table below, refines which aborts are exit 3: a path missing from a commit the clone can read is a FAIL.)", "commit 5 ref")

# Changes since the first review: accounting, glosses
body = once(body, "Commits 6 to 14 answer the nine points of the review of the first version of this PR, one commit each, and add one fix the review did not ask for. Each has its own tests, its own record in `CHANGELOG.md` and a mutation round. Every point reproduced on a throwaway repository before any change was made.",
    "Commits 6 to 14 answer eight of your nine points (one commit each; point 3, the split, is the rebuild of Commits 4 and 5) and add one fix you did not ask for (Commit 14). Each has its own tests, its own record in `CHANGELOG.md` and a mutation round. Every defect (points 1, 2, 4 to 9, and the extra fix) was reproduced on a throwaway repository before any change was made; point 3 was a request.", "changes intro")
body = once(body, "(The `ACTIVE TASK` half concerns `SESSION_NOTES.md`'s front matter and goes with the separate pull request.)",
    "(The second half of your point 4, an `ACTIVE TASK` edit in the trim commit failing L2 after `L2_OK`, concerns `SESSION_NOTES.md`'s front matter and goes with the `SESSION_NOTES.md` pull request.)", "point 4 half")
body = once(body, "| `--reverify` did not lift `PREFIX`, so a proof written for another depth read exit 1. |",
    "| `--reverify` reads (\"lifts\") each grammar line out of a frozen proof, but not `PREFIX` (the relative path a shard's links climb back to the repository root), so a proof written for another depth read exit 1. |", "row 6")
body = once(body, "made the spliced proof a `SyntaxError`", "made the re-derived proof a `SyntaxError`", "row 7")
body = once(body, "| The frontier note and the record-0 diff said nothing of other records that had moved. | They are printed only when no other record moved; otherwise a note says the others did. |",
    "| The `NOTE:` line about a record 0 edit, and the record-0 diff, said nothing of other records that had moved. | They are printed only when no other record moved; otherwise a note says the others did. |", "row 8")
body = once(body, "| Narrowing `other_fails` to one failure kind passed every test. |", "| Narrowing `other_fails` (every failure that is not L1 or L3) to one kind passed every test. |", "row 9")
body = once(body, "Separable: drop the commit and the nine stand.", "Separable: drop Commit 14 and the other answers stand.", "extra row")

# Where to read closely: the marker in a fenced block
i = body.index("`HANDOFFS.md`'s stub marker is now ")
j = body.index("\n\n", body.index("The diff is built with Python's `difflib`", i)) 
new_marker = ("`HANDOFFS.md`'s stub marker is, since Commit 8, this regular expression under `re.M`:\n\n"
              "```\n" + r"\A(`{3,}|~{3,})handoff[^\n]*\n(?:(?!\1)[^\n]*\n)*?status: pending[ \t\r]*$" + "\n```\n\n"
              "The line must be inside the fence that opens the record, which ends at a line starting with the same run of backticks or tildes that opened it. It is a lazy line-by-line scan, linear in the record; a test searches a 400,000-line record that has no marker. The diff is built with Python's `difflib` from the two record texts the proof already holds.")
body = body[:i] + new_marker + body[j:]

# Evidence
body = once(body, "In a clean `--no-local` clone of this branch's head, `quality_ratchet.py --run` reports 12 of 12 gates pass, 0 fail, 0 unmeasured (results `b49e29a9e5ea`, manifest `06181a10ec42`)",
    "In a clean `--no-local` clone of this branch's head (`1670c5d`), `quality_ratchet.py --run` reports 12 of 12 gates pass, 0 fail, 0 unmeasured (the ratchet's results digest `b49e29a9e5ea` and manifest digest `06181a10ec42`)", "gate")
body = once(body, "Those three rounds ran in my fork (`rmsharp/methodology`) when the code was first written there. Commit 4:",
    "Those three rounds ran in my fork (`rmsharp/methodology`) when the code was first written there; Commits 1 to 3 here differ from the fork's finished code in six places, seven lines in all (comments and one assertion message), none changing behaviour. Commit 4:", "six places")
body = once(body, "Commits 6 to 14, run on this branch: 8, 3, 6, 3, 3, 4, 8, 4 and 2 mutants, all caught; for Commit 12 one further mutant (\"every failure that starts with `L2`\") survives, and is equivalent, because every failure string starts with `L1`, `L2` or `L3`.",
    "Commits 6 to 14, run on this branch: 8, 3, 6, 3, 3, 4, 8, 4 and 2 mutants, all caught. Commit 12 has one further mutant (\"every failure that starts with `L2`\"), a ninth, that survives; it is equivalent, because every failure string starts with `L1`, `L2` or `L3`.", "mutants")
body = once(body, "under 1.8.1 (this PR as first reviewed, with the `SESSION_NOTES.md` entry) 46 at exit 0 and 8 at exit 4;",
    "at `1082d3b` (the head you reviewed, with the entry) 46 at exit 0 and 8 at exit 4;", "1082d3b sweep")
body = once(body, "row for row the same as 1.8.1. The fixes change no verdict among the 54. At that repository's HEAD, 2 of 59 proofs carry `PREFIX = \"../\"` (both under `methodology/archive/`): under 1.8.1 `--reverify` read the CHANGELOG one at exit 1 and the HANDOFFS one at exit 0, and this branch refuses both at exit 3. `--reverify` writes nothing.",
    "row for row the same as `1082d3b`. The fixes change no verdict among the 54. At that repository's HEAD (`d7d16f477`, 59 proofs; not the 54 above), 2 proofs carry `PREFIX = \"../\"` (both under `methodology/archive/`): at `1082d3b` `--reverify` read the CHANGELOG one at exit 1 and the HANDOFFS one at exit 0, and this branch refuses both at exit 3. So this branch cannot `--reverify` shards in that layout; lifting the prefix instead of refusing is a small change, and I followed your wording. `--reverify` writes nothing.", "head sweep")
body = once(body, "**The two existing ledgers' verdicts.** The 179 frozen shards of my fork (`CHANGELOG.md` and `HANDOFFS.md` shards, written by trimmer versions 1.1.1 to 1.8.1 of the fork's own line):",
    "**The two existing ledgers' verdicts.** The 181 shards of my fork (`CHANGELOG.md` and `HANDOFFS.md` shards, written by trimmer versions 1.1.1 to 1.8.1 of the fork's own line); 179 have a proof, and the 2 early hand-made ones have none and read exit 3 under 1.7.0 and under this branch alike. For the 179:", "fork shards")
body = once(body, "and a `NOTE:` line stating the timing rule. (Measured at Commit 3",
    "and a `NOTE:` line stating the timing rule as Commit 2 worded it (since reworded by Commit 13). (Measured at Commit 3", "timing note")
body = once(body, "uncommitted, the working-tree read follows the link and passes, which becomes a FAIL once committed.",
    "uncommitted, the working-tree read follows the link and passes, which becomes a FAIL once committed; this PR does not change that, since the committed proof is the one that decides and it fails closed.", "symlink status")

# Adopter impact
body = once(body, "Commits 1, 2, 4 and 6 to 14 change only what a *new* trim writes and warns about and what a new or re-derived proof prints or refuses; commit 3 adds a flag.",
    "Commits 1, 2, 4, 5 and 6 to 14 change only what a *new* trim writes and warns about and what a new or re-derived proof prints, refuses or exits with; commit 3 adds a flag.", "impact 1")
i = body.index("- **Exit codes mean more exactly.**")
j = body.index("- **Exit status 4 is new**")
body = body[:i] + "- **Exit codes are more specific, measured against 1.5.0 (what adopters hold).** A proof that cannot read a commit, tree or blob from git now exits 3 (it exited 1; Commit 5). A proof whose history walk fails now exits 3 (it printed `OK`; Commit 14). A path absent from something the proof can read still exits 1 (Commit 6 restores 1.5.0's answer after Commit 5 moved it to 3). `--reverify` refuses more frozen proofs, at exit 3, by name: a `PREFIX` other than `\"../../\"`, a carriage return or a NUL in `RECORD_START`. A caller that treated 3 as \"could not run\" is unaffected.\n" + body[j:]
body = once(body, "- **A proof's output grows** when record 0 was edited in the trim commit: the diff", "- **A proof's output grows** when record 0 was edited in the trim commit and no other record moved: the diff", "impact diff")
body = once(body, "A project that carries its own table entry for it (the #93 repository does) is unaffected until the separate pull request lands. `bin/sync` stops on a locally edited `methodology_trim.py` (exit 2, naming the file, `--force` to overwrite), as it does for any local edit; this PR does not change that.",
    "A project that carries its own table entry for it (the #93 repository does) is unaffected only while it does not sync: `bin/sync` stops on its locally edited `methodology_trim.py` (exit 2, naming the file), and with `--force` it overwrites the copy and removes the local entry, so that project cannot trim `SESSION_NOTES.md` again until the `SESSION_NOTES.md` pull request lands. This PR does not change how `bin/sync` treats a locally edited file.", "impact notes")
body = once(body, "`methodology_trim.py` (from 1.5.0 to 1.8.2)", "`methodology_trim.py` (from 1.5.0 to 1.8.2, the version Commits 6 to 14 move it to)", "impact version") if "`methodology_trim.py` (from 1.5.0 to 1.8.2)" in body else body

body = body.replace(SEP, NOTES_PR)

(root / "docs/planning/pr94-response-evidence/pr94-new-body.md").write_text(body, encoding="utf-8")
print("written; %d bytes" % len(body.encode("utf-8")))
