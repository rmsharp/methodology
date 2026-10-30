#!/usr/bin/env python3
"""Draft 12 of the one upstream pull request's text: draft 11 checked, claim by claim, against the rebuilt branch.

  python3 docs/planning/pr-composition-evidence/pr4b-draft12-build.py [--check]

Draft 11 described `pr2/candidate` (34 commits over `f34769f`). #92 and #94 have merged, `upstream/main` is `d50ce290`,
and the branch was rebuilt on it as `pr2b/candidate` (33 commits). The old and the new branch differ in 9 files only
(`pr4b-facts.sh` section 4), so every claim about the other files stands by identity and only what rests on the
trimmer, its tests, the gate file, the apparatus and the commit list is re-measured (`pr4b-record.md`).

Every edit is an exact-once replacement on `docs/planning/upstream-pr-body.md`. The script refuses, writing nothing,
unless the file equals draft 11 as commit `7d00d29` holds it, or if any text to replace is not found exactly once (a
`line` edit: exactly one line starts with the given text; a `block` edit: one run of lines, first and last given by
their starts). To reproduce draft 12 from a tree that already has it: `git show 7d00d29:docs/planning/upstream-pr-body.md
> docs/planning/upstream-pr-body.md`, then run this. The body's size (the bytes below the first rule, as
`pr4-body-check.py` splits it) is computed after the edits and written into the status paragraph, which sits above the
rule, so the figure cannot move the size. `--check` does everything but write.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DRAFT = ROOT / "docs" / "planning" / "upstream-pr-body.md"
DRAFT11 = "7d00d29"   # draft 11, approved: the text this script starts from

READ = "@@READ@@"     # filled from the constant below, so the status paragraph can say what read the draft had
READ_TEXT = ("Draft 12 was read cold by one fresh agent after it was frozen at `357ae739` (6 of 10; "
             "[`pr4b-record.md`](pr-composition-evidence/pr4b-record.md) section 7); drafts 9 to 11 had no read.")

# ---------------------------------------------------------------------------------------------------------
# kind "sub":   (old, new)                  the old text occurs exactly once in the file
# kind "line":  (prefix, new_line)          exactly one line starts with prefix; the whole line is replaced
# kind "block": (first_prefix, last_prefix, new_text)   one run of lines, first and last given by their starts
# ---------------------------------------------------------------------------------------------------------
EDITS = [
    # ---- above the rule: the heading and the status paragraph ------------------------------------------
    ("sub", "# The text of the one upstream pull request (draft 11)\n",
     "# The text of the one upstream pull request (draft 12)\n"),
    ("block", "**Status: DRAFT 11, APPROVED by the operator", "from the local branch `pr2/candidate` at `3cba1e5`",
     "**Status: DRAFT 12, awaiting the operator's approval; nothing sent. PR5 (the push and the opening) comes at his "
     "go-ahead, each step its own.** Draft 11 (`7d00d29`, approved by him as the pull request's text at the S338 "
     "picker, 2026-10-18) described `pr2/candidate`, 34 commits over `upstream/main` `f34769f`. That branch no longer "
     "fits: #92 and #94 merged on 2026-10-24, `upstream/main` is now `d50ce290`, and the branch was rebuilt on it as "
     "`pr2b/candidate`, 33 commits. Draft 12 is draft 11 checked against the rebuilt branch, claim by claim; "
     "[`pr4b-record.md`](pr-composition-evidence/pr4b-record.md) lists every edit and the command behind every figure. "
     "What changed in the text: #94 and #92 are merged, so decision 3 now asks about #98 and names #96; the trimmer is "
     "your 1.8.2 with the layout changes on top, so the earlier work is two commits (37% of the added lines, not 42%) "
     "and the whole-file bullet is about the dashboard alone; the sizes, the commit list, the figures for my 12 "
     "projects (52 files refused, not 39) and the evidence table are re-measured. The body is @@SIZE@@ B against the "
     "20,000 B budget he set at S332 (draft 11 was 21,486 B). @@READ@@ The history before draft 11 is in "
     "[`bl119-record.md`](pr-composition-evidence/bl119-record.md) and "
     "[`draft4-record.md`](pr-composition-evidence/draft4-record.md). Everything below the rule is the text that would "
     "be posted: the title on its own line, then the body. Written for `KJ5HST/methodology` from the local branch "
     "`pr2b/candidate` at `47637be` (33 commits over `upstream/main` `d50ce29`). Every number in it is printed by a "
     "command named beside it, and the text is read by `pr4-body-check.py`."),

    # ---- the body: the numbered items, the hashes ---------------------------------------------------------
    ("sub", "and #94 is my pull request that fixes it; #92 is my pull request with the release notes for v4.2; #67 was "
            "your issue",
     "which #94 fixed, and #92 added the release notes for v4.2 (both merged); #98 and #96 are my two "
     "other open pull requests; #67 was your issue"),
    ("sub", "(the `pr3-` and `pr4-` in their names are my own numbering, not pull request numbers)",
     "(the `pr3`, `pr3b`, `pr4` and `pr4b` in their names are my own numbering, not pull request numbers)"),
    ("sub", "which are on my fork's `main`, and `1082d3b`, the head of #94.",
     "which are on my fork's `main`, and `65990cd`, the head of #98."),

    # ---- decision 1 -----------------------------------------------------------------------------------------
    ("sub", "The branch is 34 commits and adds 19,983 lines.", "The branch is 33 commits and adds 18,367 lines."),
    ("sub", "the first commit, `bbe0dc3`, can be taken alone", "the first commit, `fbcef39`, can be taken alone"),

    # ---- decision 2 -----------------------------------------------------------------------------------------
    ("sub", "These come with the earlier work in `bbe0dc3`, and they are policy",
     "These come with the earlier work in `fbcef39`, and they are policy"),
    ("sub", "The other dashboard changes in `bbe0dc3` (2.11.3 to 2.21.0)",
     "The other dashboard changes in `fbcef39` (2.11.3 to 2.21.0)"),
    ("sub", "All 4 versions of the trimmer in your history have that line.",
     "Every version of the trimmer in your history (17 commits, 1.5.0 to 1.8.2) has that line."),
    ("sub", "are restored as you wrote them (`cfcc713`).", "are restored as you wrote them (`9848b62`)."),

    # ---- decision 3: #94 and #92 have merged; the question is now about #98 (and #96) --------------------------
    ("line", "3. **In what order should this and #94 go?**",
     "3. **In what order should this and #98 go?** #98 (open) and this branch both rewrite "
     "`starter-kit/methodology_trim.py` and its tests. Against #98's current head (`65990cd`), "
     "`git merge-tree` reports conflicts in 3 files and 5 regions (the trimmer 3, its tests 1, `.quality-gates.json` "
     "1); #96 (open) conflicts in 2 files and 3 regions (`.quality-gates.json` 2, `bin/tests.sh` 1). This branch carries none of #98's "
     "three commits (`SESSION_NOTES.md` in the trimmer's ledger table; two messages and three exit-3 statements made "
     "true; a warning for an uncommitted front-matter edit): the trimmer here is your 1.8.2 with the layout changes "
     "on top. Both name the trimmer 1.9.0 for different changes (#98's first commit, and this branch's trimmer "
     "commit), so whichever lands second takes a later number. Please say "
     "whether I should wait for #98 and rebase on it, or whether you will take this first and I rebase #98 and #96 "
     "on it. I have not resolved the conflicts."),

    # ---- decision 4 -------------------------------------------------------------------------------------------
    ("sub", "`ced2c82` drops a duplicated example command", "`6ce88cd` drops a duplicated example command"),
    ("sub", "the 34 commits were made without your pre-commit hook", "the 33 commits were made without your pre-commit hook"),

    # ---- size ---------------------------------------------------------------------------------------------------
    ("line", "**Size.** The branch adds 19,983 lines",
     "**Size.** The branch adds 18,367 lines and removes 1,098 (`git diff --shortstat d50ce29 HEAD`). Most of that never "
     "reaches a project. `bin/sync` writes 19 of the changed files into a project, with 2,540 lines added and 526 "
     "removed in all; 3 more changed files are the sources of seeds, which only a new project receives. The other 25 "
     "files, with 15,820 of the added lines (86%), stay in this repository: tests, tools that only this repository "
     "runs, and its gate configuration. The dashboard is counted twice in that total (as "
     "`starter-kit/methodology_dashboard.py` and as an identical copy in `tools/`). About 37% of the added lines "
     "(6,883, in `fbcef39` and `1d93579`) are earlier work of mine that is not about the directory "
     "(`pr4-distribution.py` prints the split, `pr4b-facts.sh` the 37%)."),

    # ---- the commits ------------------------------------------------------------------------------------------
    ("line", "Each commit's message describes it.",
     "Each commit's message describes it. A suggested order for reading: `fbcef39`, then `41a1e58` (the foundation: "
     "the layout resolver, test projects in both layouts, `bin/check-layout-literals`, which finds a tool that names a "
     "file by its root path, and `NEW_LAYOUT`), then the rest in order. Of the last twelve commits, ten drop "
     "references that only my fork can resolve (decision 4); `fd43f70` corrects four stale statements in comments and "
     "gate reasons, and `9848b62` restores the two tests named in decision 2 (e) and raises their gate's floor by two "
     "(neither changes a code path)."),
    ("block", "- **`bbe0dc3` (9 files", "- **Whole files, not hunks.**",
     "- **`fbcef39` (6 files, +6,187 / -552), earlier work.** The dashboard 2.11.3 to 2.21.0 (both copies) and its "
     "tests. In `bin/tests.sh`: three blocks changed so that `cmd | grep -q` under `pipefail` cannot report a match as "
     "a failure, a lint for that pattern, a `skip` helper and an executable-bit check derived from the manifest. It "
     "also adds to `BOOTSTRAP.md` a row, in its table of files `bin/sync` never overwrites, that names every seed, and "
     "raises two thresholds in `.quality-gates.json` (the shell suite's, 261 to 271, and the dashboard's, 229 to 354). "
     "It fixes one defect: `git log --reverse --format=%ai -1` applies `-1` before it reverses, so "
     "`first_commit_date` was the newest commit and a project's age was the days since its last commit; the "
     "dashboard now reads the root commits (`--max-parents=0`).\n"
     "- **`1d93579` (4 files, +696 / -20), earlier work.** The quality ratchet's 1.4.0 and 1.5.0. A gate may set "
     "`timeout_seconds`; a command that outlives it is reported `unmeasured` (its result could not be determined), not "
     "as exit code 127, and its whole process group is stopped. Two gates that read the same command's output share "
     "one run of it. Changing `timeout_seconds` is a warning, not a refusal. It does not depend on the layout, but it "
     "is built on the ratchet's layout commit `7d87cb2`.\n"
     "- **`d818ca1` (2 files, +5 / -2), a small change elsewhere.** A rule in `starter-kit/HANDOFFS.md` and "
     "`HOW_TO_USE.md` for a close-out receipt that cites a gate run: a gate that read `unmeasured` must be repaired, "
     "or named in the receipt. Its check is in my version of `bin/check-handoff`, which is not carried, so the rule is "
     "prose only.\n"
     "- **One of your tests is rewritten** (`07ec025`): Test 15 now counts the status table's rows, because "
     "`bin/status` prints a `layout:` line that names the project and the old assertion counted lines naming the "
     "project (31 for 30 files).\n"
     "- **`62680cd` (5 files, +1,247 / -105), the trimmer.** Your 1.8.2 with the layout changes on top, named 1.9.0: it "
     "finds a ledger at the root or under `methodology/`, writes its archive piece beside it and proves the trim. Its "
     "tests go from 227 to 265, and some of them compare against a frozen copy of the proof template 1.8.2 writes "
     "(`tools/fixtures/trim-verify-template-1.8.2.sh`, 483 lines).\n"
     "- **The dashboard is a whole file, not hunks,** because my version had diverged from yours: a three-way merge "
     "of your copy with mine, from the copy my work began with (`c8b9ddd`), conflicts in 17 places in each of its two "
     "copies (`pr4-mergefile.sh`, with my fork's `main` as of `e7b389f`). The trimmer is not (the same merge "
     "conflicts in 1 place there and 1 in its tests). For `bin/check-ledger` and `bin/check-handoff` it contains "
     "the layout hunks only."),

    # ---- what a project sees: the figures for my 12 projects ---------------------------------------------------
    ("line", "**My own 12 projects**",
     "**My own 12 projects** (7 under `methodology/`, 5 not; `pr3b-adopters.py` is the method) are mine, so you cannot "
     "run this on them. Without `--force`, this branch's `bin/sync` refuses 10 of them, over 52 files: 51 are versions "
     "from my fork's history that no commit of this branch carries, and one is a project's own edit of "
     "`methodology_trim.py` (49 lines differ from my fork's copy), which `--force` drops without saying so. After one "
     "`--force`, a plain run writes nothing at any of the 12; it changed none of their seeds."),

    # ---- the evidence table -----------------------------------------------------------------------------------
    ("sub", "`pr4-claims.sh` runs them all (about 35 minutes).", "`pr4b-claims.sh` runs them all (about 30 minutes)."),
    ("sub", "| Check | Command | upstream `f34769f` | this branch |", "| Check | Command | upstream `d50ce29` | this branch |"),
    ("sub", "| 0 refusals over 34 commits; gates 12 to 18; five thresholds raised |",
     "| 0 refusals over 33 commits; gates 12 to 18; five thresholds raised |"),
]


def git(*a):
    return subprocess.run(["git", *a], cwd=str(ROOT), capture_output=True, text=True).stdout.strip()


def apply(text, kind, a, b, c=None):
    if kind == "sub":
        n = text.count(a)
        if n != 1:
            sys.exit("refused: a text to replace occurs %d times, not once:\n%s" % (n, a[:140]))
        return text.replace(a, b, 1)
    lines = text.split("\n")
    if kind == "line":
        hits = [i for i, l in enumerate(lines) if l.startswith(a)]
        if len(hits) != 1:
            sys.exit("refused: %d lines start with %r, not one" % (len(hits), a[:80]))
        lines[hits[0]] = b
        return "\n".join(lines)
    if kind == "block":
        first = [i for i, l in enumerate(lines) if l.startswith(a)]
        last = [i for i, l in enumerate(lines) if l.startswith(b)]
        if len(first) != 1 or len(last) != 1 or last[0] < first[0]:
            sys.exit("refused: block %r .. %r is not one run (%d starts, %d ends)" % (a[:50], b[:50], len(first), len(last)))
        lines[first[0]:last[0] + 1] = c.split("\n")
        return "\n".join(lines)
    sys.exit("unknown edit kind %r" % kind)


def main():
    check_only = "--check" in sys.argv[1:]
    text = DRAFT.read_text(encoding="utf-8")
    blob = git("hash-object", str(DRAFT))
    committed = git("rev-parse", DRAFT11 + ":docs/planning/upstream-pr-body.md")
    if blob != committed:
        sys.exit("refused: %s is not draft 11 as %s holds it (%s != %s)" % (DRAFT.name, DRAFT11, blob[:12], committed[:12]))
    for e in EDITS + EXTRA_EDITS:
        text = apply(text, *e)
    body = text.split("\n---\n", 1)[1]
    size = len(body.encode("utf-8"))
    text = text.replace("@@SIZE@@", "{:,}".format(size), 1).replace(READ, READ_TEXT, 1)
    assert "@@" not in text, "a placeholder is left"
    print("edits applied: %d; body %s B (draft 11: 21,486 B)" % (len(EDITS) + len(EXTRA_EDITS), "{:,}".format(size)))
    if check_only:
        print("--check: nothing written")
    else:
        DRAFT.write_text(text, encoding="utf-8")
        print("wrote %s" % DRAFT.relative_to(ROOT))


# Edits that rest on the last runs (first commit alone, cost, fixtures); filled in from their saved outputs.
EXTRA_EDITS = [
    # cold read, finding 1: the changed paragraph is the third, and the documents' path mentions change with it
    ("sub", "and finds the first paragraph of `SESSION_RUNNER.md` changed (it says where to look for the other "
            "framework files)",
     "and finds its framework documents naming one another by bare name (28 fewer lines name `docs/methodology/`), "
     "with a new paragraph, the third of `SESSION_RUNNER.md`, saying where to look"),
    # cold read: the 138 is the scanner's own count, not a grep
    ("sub", "`# layout: ok -- <reason>` (`python3 bin/check-layout-literals`)",
     "`# layout: ok -- <reason>` (the \"acknowledged\" count of `python3 bin/check-layout-literals`)"),
    # cold read: two classes of the migration suite do run in bin/tests.sh
    ("sub", "Its own suite of 280 tests (separate from `bin/tests.sh`) takes about 6 minutes,",
     "Its own suite of 280 tests takes about 6 minutes (two fast classes of it also run in `bin/tests.sh`),"),
    # decision 4 (cold read): the ten are seven commits and a tail of three, not one run at the tip; the seven and the
    # tail are named; 27 of the 33 commits end in a cherry-pick line that names a commit only the fork has
    ("line", "   - Ten commits remove references",
     "   - Ten commits remove references that only my fork can resolve, such as backlog and session codes in comments and "
     "messages: seven (`e051462` to `8c37c28`) and a tail of three (`1477af2` to `47637be`). Please tell me whether to "
     "keep these commits or drop them; if you drop them, the references stay in the code. A merge commit or a rebase "
     "keeps them as separate commits and a squash folds them in. The tail can be dropped alone; the seven only with "
     "`9848b62` rebased. They are not exhaustive: some references of that kind remain, and 27 of the 33 commits end "
     "with a `(cherry picked from commit ...)` line that names a commit only my fork has."),
    # the cost run (pr4b-cost-output.txt): the dashboard on the larger project is now quicker, not "within 0.1 s"
    ("sub", "took the same time as upstream's versions, within 0.1 s on two test projects (`pr4-cost.sh`).",
     "took no longer than upstream's: the same on a project of 3 commits, and on one of 517 the dashboard took "
     "0.66 s against 0.92 s (`pr4-cost.sh`)."),
]

if __name__ == "__main__":
    main()
