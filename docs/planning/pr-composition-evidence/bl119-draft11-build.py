#!/usr/bin/env python3
"""Draft 11 of the one upstream pull request's text: draft 10 re-measured after two changes it did not know.

  python3 docs/planning/pr-composition-evidence/bl119-draft11-build.py [--check]

PR #94 gained a fifth commit (`1082d3b`, trimmer 1.8.1: a proof that cannot read git exits 3, not 1), and
the candidate took the same change as its 34th commit (`3cba1e5`). Every edit below is an exact-once
replacement on `docs/planning/upstream-pr-body.md`; the script refuses, writing nothing, unless the file
equals draft 10 as commit `8d7316e` holds it (the commit that recorded his approval; `150e1bf` is the same
text with an earlier status line), or if any text to replace is not found exactly once. To reproduce draft 11
from a tree that already has it: `git show 8d7316e:docs/planning/upstream-pr-body.md >
docs/planning/upstream-pr-body.md`, then run this.
The body's size (the bytes below the first rule, as `pr4-body-check.py` splits it) is computed after the
edits and written into the status paragraph, which sits above the rule, so the figure cannot move the size.
`--check` does everything but write.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DRAFT = ROOT / "docs" / "planning" / "upstream-pr-body.md"
DRAFT10 = "8d7316e"   # draft 10, approved: the text this script starts from

EDITS = [
    # ---- above the rule: the heading and the status paragraph --------------------------------------
    ("# The text of the one upstream pull request (draft 9)\n",
     "# The text of the one upstream pull request (draft 11)\n"),
    ("**Status: DRAFT 10, APPROVED by the operator as the pull request's text (S336 picker, 2026-10-17), "
     "frozen at `150e1bf`; nothing sent, PR5 (the push and the opening) comes after D1 and D4 at his "
     "go-ahead.** The body is 20,863 B, 863 B over the 20,000 B budget he set at S332, kept at his word: "
     "the additions are his two decisions and decision 3 re-measured. Draft 10 is draft 9 (`d2cc1e9`)",
     "**Status: DRAFT 11, awaiting the operator's approval; draft 10 (approved at the S336 picker, "
     "2026-10-17, frozen at `150e1bf`; `git show 8d7316e:docs/planning/upstream-pr-body.md` restores it) is "
     "the text before it. Nothing sent; PR5 (the push and the opening) "
     "comes after D1 and D4 at his go-ahead.** Draft 11 is draft 10 re-measured after two changes it did "
     "not know of: PR #94 gained a fifth commit (`1082d3b`, 2026-10-17: a proof that cannot read git "
     "exits 3, not 1; trimmer 1.8.1), and this branch took the same change as its 34th commit "
     "(`3cba1e5`); [`bl119-record.md`](pr-composition-evidence/bl119-record.md) lists every edit. The body "
     "is @@SIZE@@ B against the 20,000 B budget he set at S332 (draft 10 was 20,863 B and he kept it at "
     "his word). Draft 10 is draft 9 (`d2cc1e9`)"),
    ("(`93245dc`), 9 and 10 had no read. **Draft 10 has had no read of its own.**",
     "(`93245dc`), 9, 10 and 11 had no read. **Drafts 10 and 11 have had no read of their own.**"),
    ("from the local branch `pr2/candidate` at `cfcc713` (33 commits over `upstream/main` `f34769f`)",
     "from the local branch `pr2/candidate` at `3cba1e5` (34 commits over `upstream/main` `f34769f`)"),
    # ---- the body: the hashes sentence, the sizes, decision 3, the commit list ---------------------
    ("The commit hashes below are this branch's, except `c8b9ddd` and `e7b389f`, which are on my fork's "
     "`main`.",
     "The commit hashes below are this branch's, except `c8b9ddd` and `e7b389f`, which are on my fork's "
     "`main`, and `1082d3b`, the head of #94."),
    ("The branch is 33 commits and adds 19,822 lines.",
     "The branch is 34 commits and adds 19,983 lines."),
    ("Against #94's current head (`2308553`, its fourth commit), `git merge-tree`",
     "Against #94's current head (`1082d3b`, its fifth commit), `git merge-tree`"),
    ("This branch contains my fix for #93 as #94's first three commits had it (inside `bbe0dc3`), not its "
     "fourth (`SESSION_NOTES.md` in the trimmer's ledger table, and the proof's diff of record 0): of the "
     "506 lines #94 adds to the trimmer and the 1,558 to its tests, 77 and 294 are not in this branch as "
     "identical lines",
     "This branch contains my fix for #93 as #94's first three commits had it (inside `bbe0dc3`) and "
     "#94's fifth commit (`3cba1e5`), not its fourth (`SESSION_NOTES.md` in the trimmer's ledger table, "
     "and the proof's diff of record 0): of the 536 lines #94 adds to the trimmer and the 1,640 to its "
     "tests, 77 and 295 are not in this branch as identical lines"),
    ("Both branches name their trimmer 1.8.0 for different changes, so whichever lands second takes the "
     "next number.",
     "Both branches name their trimmer 1.8.1, for different changes (each is a different 1.8.0 plus the "
     "same abort fix), so whichever lands second takes the next number."),
    ("the 33 commits were made without your pre-commit hook",
     "the 34 commits were made without your pre-commit hook"),
    ("**Size.** The branch adds 19,822 lines and removes 1,102 (`git diff --shortstat f34769f HEAD`).",
     "**Size.** The branch adds 19,983 lines and removes 1,105 (`git diff --shortstat f34769f HEAD`)."),
    ("with 2,959 lines added and 530 removed in all",
     "with 2,991 lines added and 533 removed in all"),
    ("The other 25 files, with 16,856 of the added lines (85%)",
     "The other 25 files, with 16,985 of the added lines (85%)"),
    ("About 43% of the added lines (8,461,",
     "About 42% of the added lines (8,461,"),
    ("The last two commits change no code path: `a62bfec` corrects four stale statements in comments and "
     "gate reasons, and `cfcc713` restores the two tests named in decision 2 (e) and raises their gate's "
     "floor by two.",
     "Of the last three commits, `a62bfec` corrects four stale statements in comments and gate reasons "
     "and `cfcc713` restores the two tests named in decision 2 (e) and raises their gate's floor by two "
     "(neither changes a code path); `3cba1e5` is #94's fifth commit, described below."),
    ("- **Whole files, not hunks.**",
     "- **`3cba1e5` (4 files, +165 / -7), #94's fifth commit carried over.** A generated proof that cannot "
     "read an artifact from git (a shallow or partial clone) exited 1, the code for a failed check; it "
     "now says why and exits 3, \"the proof did not finish\". The trimmer is 1.8.1. The four tests are "
     "#94's, plus one edit only here: the test that pins the proof template to 1.7.0's bytes maps the "
     "new block back and asserts it is the block in use.\n"
     "- **Whole files, not hunks.**"),
]


def main():
    check_only = "--check" in sys.argv
    text = DRAFT.read_text(encoding="utf-8")
    blob = subprocess.run(["git", "hash-object", str(DRAFT)], cwd=str(ROOT), capture_output=True,
                          text=True).stdout.strip()
    committed = subprocess.run(["git", "rev-parse", DRAFT10 + ":docs/planning/upstream-pr-body.md"], cwd=str(ROOT),
                               capture_output=True, text=True).stdout.strip()
    if blob != committed:
        sys.exit("refused: %s is not draft 10 as %s holds it (%s != %s)" % (DRAFT.name, DRAFT10, blob[:12], committed[:12]))
    for old, new in EDITS + TABLE_EDITS:
        n = text.count(old)
        if n != 1:
            sys.exit("refused: a text to replace occurs %d times, not once:\n%s" % (n, old[:140]))
        text = text.replace(old, new, 1)
    body = text.split("\n---\n", 1)[1]
    size = len(body.encode("utf-8"))
    text = text.replace("@@SIZE@@", "{:,}".format(size), 1)
    assert "@@" not in text
    print("edits applied: %d; body %s B (draft 10: 20,863 B)" % (len(EDITS) + len(TABLE_EDITS), "{:,}".format(size)))
    if check_only:
        print("--check: nothing written")
    else:
        DRAFT.write_text(text, encoding="utf-8")
        print("wrote %s" % DRAFT.relative_to(ROOT))


# The evidence table's rows, filled from the claims run on 3cba1e5 (see bl119-record.md).
TABLE_EDITS = [
    ("0 refusals over 33 commits; gates 12 to 18; five thresholds raised",
     "0 refusals over 34 commits; gates 12 to 18; five thresholds raised"),
]

if __name__ == "__main__":
    main()
