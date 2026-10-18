# D1 and D4 answered: the record (S339, 2026-10-18)

Two decisions that stood between the finished pull request candidate and PR5 (the push and the opening) in
[`../upstream-pr-composition-plan.md`](../upstream-pr-composition-plan.md) section 7. He answered both at a picker after the S339
claim, each as recommended. **Nothing is sent to `KJ5HST/methodology`:** `gh` and `git ls-remote` were read-only.

## 1. His answers

| Decision | What it asked | His answer |
|---|---|---|
| **D1** | The plan's rule (section 7.6 of `methodology-subdirectory-plan.md`): the pull request waits while a finding the tool's own checks did not report is open, unless he waives it and the ledger says so. | **Waive it, the text unchanged.** The ledger entry of 2026-10-18 (S339) in `CHANGELOG.md` is the "ledger says so". |
| **D4** | Keep waiting for the maintainer's answer on #92 and #94 before PR5, or stop waiting. | **Keep waiting, and ask again on or after 2026-10-25.** |

## 2. D1: the 13 open rows, as `register-open-rows.py` reads them

`python3 -I docs/planning/pr-composition-evidence/register-open-rows.py` (read-only, run on `2be18304`): **13 open of 33 rows.** The
saved output was made when the register had 31 rows; the two added since, F32 and F33, are both fixed, so the 13 are the same.
Its "seen" column is the script's reading of the register's *Seen* cell: whether the tool's own checks reported the finding.

| Row | Script: seen by the checks? | In the approved text's *Known gaps*? | What closes it |
|---|---|---|---|
| F6 | NOT SEEN | yes (the second `dashboard_history.jsonl` under `methodology/`) | his triage |
| F8 | NOT SEEN | yes (an old-format ledger gets the entry at its end) | his triage |
| F17 | not seen (the warning is the tool's own and false) | yes (the warning about the hook `context_budget.py install-hook` writes) | his triage |
| F27 | NOT SEEN | **not literally**: it is the text a project's own tool writes later naming the moved path, the nearest bullet is the class below, which names reading a moved file | closed by F26's edit |
| F25, F26, F28 | probably not seen | yes, as one class: a project's own tests or scripts that read a moved file by name | each adopter's own commit before its move (BL-105 phase 4, blocked by live sessions in those projects) |
| F7, F19 | in part (the refusal is seen; what the dropped lines are is not) | yes (one bullet: a sync refuses an edited file by name, `--force` drops the edit; upstream's `bin/sync` does the same) | F19 his triage; F7 is the same refusal |
| F2 | in part | yes (an earlier ledger hook keeps looking at the root) | each adopter's session; `wsfct` is last |
| F4 | n/a, a limit of static search | yes, the same class as F25 | a stated limit |
| F13 | in part (the count is seen, its cause is not) | **no** | his triage; tier 1 only |
| F14 | seen (the tool lists the 19 files it leaves) | **no** | the adopter's own cleanup |

**Why waiving was recommended and is now recorded.** (1) The text already tells the maintainer in plain words 10 of the 13
(F2, F4, F6, F7, F8, F17, F19, and F25, F26, F28 through the one class); F27 is covered only by the nearest bullet (above) and is
closed by F26's edit; F13 and F14 are not in the text. The wait's purpose, that a reader is not surprised, is met for all but those three. (2) None is a loss this pull request newly causes: F19's dropped edit is upstream's own `bin/sync` behaviour, and
the text says so. (3) Fixing the four that await his triage would add commits to a 34-commit candidate and mean the 28-minute
`pr4-claims.sh` run again and a re-measure of the text. **The two rows the text leaves out entirely are F13 and F14**, both seen at
least in part and neither a new loss; adding them was offered as an option (b) and not chosen. (At the picker I summarised F25 to F28
as one class; F27 belongs there only loosely, as the table now says.)

## 3. D4: the facts, with a correction

Read on 2026-10-18 (`gh pr view`, `gh issue view`, `git ls-remote upstream refs/heads/main`):

- #92 (the v4.2 release notes): open since 2026-10-03, MERGEABLE, 0 comments, 0 reviews, **15 days**.
- #94 (the #93 fix): open since 2026-10-05, head `1082d3b` (pushed 2026-10-17), MERGEABLE, 0 comments, 0 reviews, **13 days**.
- Issue #93 (his own, one comment of his): open. Issue #95 (the maintainer's): filed 2026-10-15 21:00 UTC, 0 comments.
- `upstream/main` is `f34769f`, the maintainer's commit of 2026-10-02. Nothing has merged there since #91 (the maintainer's own pull request) on 2026-10-03.

His pull requests the maintainer has merged, by `gh pr list --state merged`:

| PR | Opened | Merged | Wait | Merged by |
|---|---|---|---|---|
| #80 | 2026-09-10 | 2026-09-15 | 5.7 d | the maintainer |
| #84 | 2026-09-18 | 2026-10-01 20:19 | 13.6 d | the maintainer |
| #85 | 2026-09-20 | 2026-10-01 20:19 | 10.9 d | the maintainer |
| #86 | 2026-09-21 | 2026-10-01 20:19 | 9.8 d | the maintainer |
| #87 | 2026-09-27 | 2026-10-01 20:19 | 4.7 d | the maintainer |
| #88 | 2026-09-27 | 2026-10-01 20:19 | 4.6 d | the maintainer |

So the maintainer merged five of his pull requests in one minute, after waits of 4.6 to 13.6 days. **#92 at 15 days has already
outwaited the longest of these (13.6 days, #84), and #94 at 13 days is at it.** #76 to #79 were merged by him himself, so their 0
days is not a review wait.

**Correction of what I said at the picker (S339).** I told him "the longest wait was #83 at 15 days, which is where #92 is now" and
that one more week "takes #92 past the longest earlier wait". Both are wrong: #83 is the maintainer's own pull request (14.9 days,
merged by them), the longest wait for one of his is #84's 13.6 days, and #92 is already past it. He chose the wait on that
statement. The choice is recorded as he gave it; whether it stands on the corrected figures is asked at the S339 close-out
picker, and the wait is date-limited so the correction costs at most a week.

**What the wait is, and is not.** `CLAUDE.md` §Contributing upstream: a rule about sequence and batching, never a suspension. The wait
has an end, **2026-10-25** (then #92 is 22 days old and #94 20). Every Phase 0 still reads `gh pr list`, `gh issue list` and
`git ls-remote upstream refs/heads/main` against `f34769f`; a reply, a review or a merge ranks first. A merge of #94 or #92 changes
the candidate's conflict figures, so the claims run (`pr4-claims.sh`, with the environment `HEAD94=<new head> HEAD92=<new head>`)
and the text's decision 3 are re-measured before PR5. Settling D4 sends nothing, and PR5 stays three separate go-aheads of his
(push the branch to `origin`, open the pull request, answer comments).

## 4. What this leaves for PR5

1. His go-ahead for each outward step, none implied by the one before; no earlier than 2026-10-25 unless he changes D4.
2. Nothing in the candidate or the text changes because of D1 or D4 (`pr2/candidate` is still `3cba1e5`, draft 11 is still 21,486 B).
3. Still not done, from S338's receipt: the 12-project paragraph's "49 lines" was not re-run (`pr3-adopters.py`) and `pr4-claims.sh`'s
   `HEAD94` default is stale (`972eb2c`); pass the environment.
