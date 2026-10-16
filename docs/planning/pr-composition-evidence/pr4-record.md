# PR4, the text of the pull request: the record (S327, 2026-10-15)

Row PR4 of `docs/planning/upstream-pr-composition-plan.md` section 5: a body in recognised terms, every number tied to a command in the
diff, a fresh reviewer's read of a frozen draft, shown inline, each claim of section 6 re-run. Local only; nothing is sent to
`KJ5HST/methodology`. The text is [`../upstream-pr-body.md`](../upstream-pr-body.md) (everything below its first rule); the candidate is the
local ref `pr2/candidate` at `ced2c82`, upstream's tip `f34769f`. Re-runs: `pr4-claims.sh` (output `pr4-claims-output.txt`),
`pr4-fixture.sh`, `pr4-mergefile.sh`, `pr4-supersede.sh`, `pr4-first-commit.sh`, each with its `-output.txt`; the text is read by `pr4-body-check.py`.

## 1. The answer

1. **The text exists:** [`../upstream-pr-body.md`](../upstream-pr-body.md), draft 3 (`025afed`), 18,051 B below its rule. Draft 1 (`ef98e78`, frozen) was read by
   a fresh reviewer, draft 2 (`a6ad168`) by a second, who had not seen the first's report. **Draft 3 has had no fresh read:** each change after the second read was
   checked by me against a command. Nothing is sent; the draft is shown to him in the close-out report, in a turn that ends, and asked in plain words.
2. **Every number in it is a command's output,** on `ced2c82` in clean `--no-local` clones, serial, exits read bare (section 2): the suite 302 / 0 / 0 against upstream's
   261 / 0; the gate 18/18, 0 unmeasured, against 12/12; the first commit alone 271 / 0 / 0 and 12/12 on upstream's tip.
3. **The two reviews found 25 things; each I acted on, I re-ran first.** The ones that mattered: the branch **deletes four of upstream's own tests** (the three of
   `TestCliRemedyProportionality`, and one signature test) and the draft said it dropped "two of the dashboard's tests"; "nothing changes for a project that does not
   ask" (its next sync rewrites 19 tracked files); "rolled back if a check fails" (the checks run after the commit; exit 4 keeps it); 36 links in the distributed documents
   became bare names and every legacy project gets a new first paragraph in its runner; five dashboard risk rows with hard-coded constants went unmentioned.
4. **Four defects in the candidate, confirmed, NOT fixed** (a build is its own session, as BL-113's reduction commit was): the `layout-literals` gate's `why` says two
   checkers are not scanned, and they are; the `layout-unit-tests` `why` says "74 is measured" against a floor of 76; the dashboard's comment above the stale-copy
   warning says the safe action is one `cp` while the code prints `--sync`; `bin/migrate-layout`'s header lists exits 0 to 3 and omits 4. All are text. A fix commit makes
   the series 32 commits and moves the head's shortstat and the gate's two ids, so `pr4-claims.sh` is re-run after it.
   **Superseded 2026-10-15: all four are fixed at `a62bfec` and the claims re-run ([`fix32-record.md`](fix32-record.md)); of the gate's two ids only the manifest's moved.** The
   paragraph above is left as written at the time.
5. **Not ready to send:** his approval of the text (the four fixes and the re-run are since done, `a62bfec`); D1's open rows and #94 / #92 are his calls (section 5).

## 2. Section 6's claims, re-run on `ced2c82` (clean `--no-local` clones, serial, exits read bare)

| Claim | Re-run | Result |
|---|---|---|
| a legacy project is unchanged in where its files sit | `pr4-fixture.sh` (a): an empty project synced by each tool | the same 30 paths; no `methodology/`; 22 differ in bytes, 22 of 22 are files the branch changes |
| no file an adopter owns is overwritten | `pr4-fixture.sh` (b): upstream's files, 7 seeds edited | upstream's tool writes 0, the branch's 19, 0 of 7 seeds changed, no `--force`; PR3's 12 real projects: 0 seeds changed |
| the resolver is one block, byte-identical | `python3 tools/test_layout_resolver.py`, and a read of the 11 copies | 76 tests OK; 11 of 11 equal |
| every frozen proof gives the verdict it gave | each tracked `*.verify.sh`, both tips | 1 at each, exit 0 at both (a population of one: upstream ships one proof) |
| both layouts' links resolve; no path literal left | `bin/check-links --layout both`; `bin/check-layout-literals` | OK, 80 links in 23 documents in each layout; 15 files, 0 sites |
| the gates tighten and none loosens | `compare()` of the branch's own ratchet, each of 31 commits against its parent | 0 refusals, 0 warnings; 12 to 18 gates, five floors raised |
| the counts in the prose are true | `pr4-body-check.py` (no banned token, 31 hashes resolve, paths exist, shortstat); the manifest's 30 = 18 + 12 and 11 + 7 derived from `bin/_manifest.py` by a command; the 11 copies by `pr4-claims.sh` section 5; per-commit file counts from `git show --numstat` | all equal the text |
| the first commit stands alone | `pr4-first-commit.sh`: `bbe0dc3` in a clean clone, parent `f34769f` | 271 passed, 0 failed, 0 skipped; gates 12/12, results `3d7518cbbfea` |

Not a claim of section 6 but the first thing a reader asks: the suite and the gate on the tip, in clean clones: `bash bin/tests.sh` **302 passed,
0 failed, 0 skipped** (upstream 261 / 0); `quality_ratchet.py --run` **18/18 pass, 0 unmeasured**, results `23481eb88ba1`, manifest `cfa4d5b5fa67`
(the same ids as the last run of this commit; upstream 12/12).

## 3. How the instrument was checked, and what it got wrong

- **Pilots.** The two Python sections of `pr4-claims.sh` were run on a scratch clone before the 40-minute run: the first pilot failed on two of my own mistakes (a
  gate's keys are `direction` and `threshold`, not `min` / `max`; a clone has no `upstream/main` ref) and the script was corrected, not the pilot read as a result.
  `pr4-claims.sh` was not edited while it ran.
- **Errors of mine in the first draft, found before or by the reviews:** the dashboard's third "policy" was described as new behaviour and is a restructuring of code
  upstream already has (read upstream's table before rewriting it); "I have not changed a version number" was false (four tools' versions moved); "each commit leaves the tree
  green" and "at most 5 files" were written from the layer records, and the per-commit table I had printed myself showed 9, 7 and 6 (the first review's finding 3); a figure from an earlier probe ("nine of 54 blocks, 14 checks") was not re-run and was cut to a sentence without it.
- **Reviewers' numbers are claims.** Every item I acted on was re-run first and held. Not acted on: the first reviewer's note that the dashboard's header lists 2.19 to 2.22
  and nothing for 2.13 to 2.18 (true, not in the text); the second's 37 comment lines (the stated method, first non-blank character `#` or `//`, gives 36); both reviewers'
  advice to cut (section 3, last bullet).
- **Inherited numbers corrected:** the plan's "52 conflict regions in 16 files" does not reproduce (`pr4-mergefile.sh`: 51 in 8, the dashboard 17 + 17 as before); #94's conflicts at
  the tip are 17 regions (trimmer 10, tests 6, gates 1), not 15; `bl113-record.md` says the reduction commit is "+3 / -3" and its own table sums to +4 / -4; the findings register
  has 33 rows, not 31 (F32 and F33 fixed, 13 still open); the layer records' "at most five files per commit" holds from layer 6b on and not for `bbe0dc3` (9), `14ef959` (7),
  `fd96593` (6); plan section 4 lists `.context-budget.json` as not carried and the candidate carries a 3-line hunk of it (`ced2c82`).
- **The text's length is a cost I did not remove:** 18 KB for a 19.8 KB-line pull request; the cuts I would make are the twelve-projects paragraph, the commit table's detail and
  the six known gaps, all of which are one sentence away from a link to the fork.

## 4. What none of it shows

- The route a project takes alone from GitHub (`--source=github`) was not run; the 12 real projects are the operator's own and 10 of them carry fork versions
  (`pr3-record.md` section 3). A project on upstream's own files is the fixture.
- The reviewer read the text and the branch, not the suite: the long runs (the shell suite, the gate) are mine, in section 2.
- The maintainer's machine, Windows, hooks armed in another clone, a project's own CI; upstream has no CI.
- The text was not read by the maintainer, and a read by one fresh agent is not a read by the person who will decide.

## 5. His calls this leaves

1. **The text** (draft 3): post as it is, change it, or hold. It is longer than the reviewers advised; section 3 says what would go.
2. **D1: the register's 13 open rows and the section 7.6 waiver.** The directory plan's rule: the pull request waits while a finding the tool's own checks did not report is open,
   unless he waives it and the ledger says so. By the register's *Seen* column the checks did not report **F6, F8, F17, F27**, and probably not F25, F26, F28; F13 and F19
   were half seen; F2, F4, F7, F14 are stated limits or resolve in an adopter's own commit. The text states F6, F8, F17, F19, F2, F4 and F7 in plain words as known gaps.
   He may waive, fix first, or wait for the adopter sessions.
3. **D4: #94 and #92.** Both open, no comment (`gh`, 2026-10-15). The default: wait for them to merge or be answered before the push; if #94 is still open then, ask whether to stack
   on it or state that this supersedes it (closing it is outward). The text asks the maintainer the same question.
4. **The four text defects in the candidate:** fix before PR5 (recommended; a build session, then `pr4-claims.sh` again, then the text's figures), or send as they are. *Taken 2026-10-15: fixed at `a62bfec`, see [`fix32-record.md`](fix32-record.md).*
5. **What the pull request carries besides the series.** D4's default says the register, the plan and the records; the candidate holds no such commit, those documents are written in
   the fork's shorthand (session numbers, backlog and plan codes on nearly every line), and the text links the fork's evidence directory instead. Recommended: do not carry them.
6. **A `CHANGELOG.md` entry in the pull request:** the plan leaves the ledgers out and the text says so and offers one. Add one (as #91 did) or leave it to the maintainer.
7. **His, unchanged:** F19 (the candidate's tool needs `--force` at `nprcgenekeepr`, which drops its 49 lines), F6, F8, F13, F14, F17; the push of this session's commits;
   the HANDOFFS trim; BL-108's build; BL-113 (e); the `BACKLOG.md` size flag; BL-94's third run; BL-105 phase 4.
