# The one question to the maintainer for D2 (drafted S421, 2026-11-05)

**Status: DRAFT. NOT SENT.** Revised once at S421, at the operator's request after he saw the first text:
one sentence now states his preference for (a), transient. The operator is shown the text before anything else. Posting it is his
go-ahead, asked in the session that posts. Nothing has been commented, pushed or edited on
`KJ5HST/methodology`. Only the text between the two `PR TEXT` markers is meant for the maintainer;
everything else in this file is for this repository.

**Re-checked at S424 (2026-11-05), text unchanged.** Against `upstream/main` `d50ce290`, #98 at `65990cda`
(0 comments, last updated 2026-10-26) and #100 (0 comments, last updated 2026-11-01), as they stand: every row of
the table below holds (the seven line citations resolve on `upstream/main`: `starter-kit/SESSION_NOTES.md:5`
and `:27`, `starter-kit/SESSION_RUNNER.md:262` and `:333`, `ITERATIVE_METHODOLOGY.md:400`,
`FRAMEWORK_APPARATUS.md:552`, `starter-kit/HANDOFFS.md:6` and `:169`); the scan exits 0 with no hit in the PR TEXT
block. The operator was shown the text inline and chose 'Final as shown'. Posting is still his go-ahead, asked in
the session that posts; the venue is chosen then. Two things the re-check found, neither changing the text:
#100's author is `KJ5HST`, so finding 4's 'We chose transient' is the maintainer's own, about his adopter project;
and #100 cites `FRAMEWORK_APPARATUS.md:535` where the line is now 552 (the text names the file, not the line).

## What this is

[D2](issue100-fixes-plan.md) (the row at line 120) was decided (b) at S420: the maintainer's "We chose
transient" in upstream issue #100, finding 4, is one project's answer, so he is asked what the framework's
own answer is before piece 11 (the F4 fix: step 3D says *replace*, the seed footer agrees) is built, and
before #98's first commit is kept or withdrawn. This file is that question. It is ONE question with three
answers, because #98's "Underneath" section already asked him two and got no reply.

**Where to post it (the operator's call at post time).** Recommended: a comment on #100, under finding 4,
because it is his own sentence there ("whichever answer upstream takes") that leaves the framework's answer
open, and the text names #98, which GitHub then shows on #98's timeline. The other place is a comment on #98
(its "Underneath" section is the first time the question was asked). The text reads the same in either
thread. A reply on either is the trigger the plan names for building piece 11.

**What each answer sets going.** (a) piece 11 as the plan has it ("If transient"): 3D and the seed's last
line, paid for by a cut; #98 loses its first commit and the other two are rebased. (b) piece 11 becomes a
wording correction in the places the issue lists; #98 stands. (c) both of the first: 3D and the seed's last
line change, #98 stands. The plan's piece 11 text covers only (a); on (b) or (c) it is rewritten in the
session that builds it.

## Claims in the text, each against its source (read in full at S421)

| The text says | Source |
|---|---|
| finding 4 records the adopter project's answer: transient, 3D replaces the previous session's section, `HANDOFFS.md` is the durable copy | #100 finding 4, "We chose transient"; heading "This project's answer to #98's 'Underneath' question" |
| it proposes writing the answer as a 3D step with the seed's footer agreeing | #100 finding 4, "Proposal: whichever answer upstream takes, write it as a 3D step and make the seed's footer agree." (quoted from "write it as", so the word `upstream` stays out of the text) |
| #98's first commit adds `SESSION_NOTES.md` to the trimmer's ledger table | #98 body, "The three commits", item 1 |
| if transient: first commit would not merge, questions 1 to 3 would not arise | #98 body, "Underneath" |
| if it accumulates: commit 1 is right, questions 1 to 3 are the work that remains, the documents that say "transient" need correcting | #98 body, "Underneath" |
| the other two commits are rebased and the suite re-run | #98 body, "Underneath": "I would then rebase it and the third and re-run the suite" |
| the seed's last line reads "Session history accumulates below this line." | `starter-kit/SESSION_NOTES.md:27` on `upstream/main` `d50ce290` |
| the places that call it transient or overwritten: seed header, failure mode 27, the 3D receipt paragraph, `ITERATIVE_METHODOLOGY.md`, `FRAMEWORK_APPARATUS.md`, the `HANDOFFS.md` seed | #100 finding 4's own list; each still on `upstream/main` (`starter-kit/SESSION_NOTES.md:5`, `SESSION_RUNNER.md:333` and `:262`, `ITERATIVE_METHODOLOGY.md:400`, `FRAMEWORK_APPARATUS.md:552`, `starter-kit/HANDOFFS.md:6` and `:169`) |
| #98 has three numbered open questions | #98 body, "Three questions this pull request leaves open" |
| the preference is (a), transient | the operator, at the S421 picker that showed him the first text: 'change the wording a bit by indicating that I prefer transient use.' Phrased without a first-person pronoun so the scan still exits 0; posted under his own name it reads as his |
| (c) is a third answer | not in either thread; it is the option [D2](issue100-fixes-plan.md) listed as (c): transient going forward and the trimmer entry kept |

**Left out on purpose:** the adopter counts in [`d2-evidence-output.txt`](issue100-plan-evidence/d2-evidence-output.txt)
(4 hold at 3 records or fewer, 4 climb, 3 were cut, 1 uses another heading form). They are a second
set of figures beside the 13 notes files #98 already counted (that count was taken on a different date and
set), they decide nothing for the maintainer, and the question reads better without them. They can be added
as one sentence if the operator wants them.

<!-- BEGIN PR TEXT -->
#98's "Underneath" section and finding 4 of #100 ask one question, and for the framework itself it is still open: is `SESSION_NOTES.md` transient, or does it accumulate?

Finding 4 records the adopter project's answer: transient, with step 3D replacing the previous session's section and `HANDOFFS.md` holding the durable copy. It proposes that the framework's answer be written as a 3D step with the seed's footer agreeing ("write it as a 3D step and make the seed's footer agree"). The answer also decides #98's first commit, which adds `SESSION_NOTES.md` to the trimmer's ledger table, so one reply settles both.

Which answer should the framework's text give? The preference is (a), transient.

- **(a) Transient.** Step 3D says to replace the previous session's section, keeping the ACTIVE TASK and the new handoff, and the seed's last line ("Session history accumulates below this line.") is reworded to agree. #98's first commit is withdrawn, its questions 1 to 3 fall away, and its other two commits are rebased on `main` and re-tested.
- **(b) It accumulates.** #98 stays as it is, with its questions 1 to 3 still to answer, and the places that call the file transient or "overwritten" are corrected instead: the seed's header, failure mode 27, the 3D receipt paragraph, `ITERATIVE_METHODOLOGY.md`, `FRAMEWORK_APPARATUS.md` and the `HANDOFFS.md` seed.
- **(c) Transient from now on, and #98's first commit stays** as the way to cut a notes file that has already grown. Step 3D and the seed's last line change as in (a); #98's questions 1 to 3 stay open.

A letter is enough. Nothing is built, and #98 is not changed, until you answer.
<!-- END PR TEXT -->

## Scan

`bash docs/planning/issue100-plan-evidence/fork-word-scan.sh upstream/main docs/planning/issue100-d2-question-draft.md`
reads only the text between the markers (the diff and commit-message places are empty when the branch is
`upstream/main` itself). Result at S421 is recorded in the S421 ledger entry.
