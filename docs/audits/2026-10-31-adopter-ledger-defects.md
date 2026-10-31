# Audit: three adopter handoff ledgers with structure defects

**Date:** 2026-10-31 · **Session:** S407 (a numbered run of the methodology on this repository) ·
**Kind:** read-only audit, following [`workstreams/AUDIT_WORKSTREAM.md`](../../workstreams/AUDIT_WORKSTREAM.md)

> **Nothing was changed.** No file in any adopter project was written (all 15 ledger files were hashed
> before and after each run: identical). Nothing was sent to `KJ5HST/methodology`, and no project was
> contacted. Every claim below is re-derived from the files as they are today; the script that does it
> is saved beside this report.

**The state in one paragraph.** On 2026-10-20 a session (S352) found real defects in the handoff ledgers of
three adopter projects: `church_growth`, `mts-system` and `vscode_quarto_ext`. **All three are still
there, unchanged in kind and in count (1, 2 and 12 checker findings), eleven days later, and no other
project has one.** None loses any text: every receipt is intact in its file and in git. In two of the three
projects (`vscode_quarto_ext`, `mts-system`) the checker reads a receipt wrongly (skipped or merged with
another); in the third (`church_growth`) only an identity repeats. Each defect has a one- or two-line repair,
tested on a copy (section "Recommendations"). The projects have not repaired them
because nothing in their workflow shows them: the checker that finds the defects is canonical-only
(`bin/check-handoff` is not distributed to adopters).

## Audit Summary

- **Scope:** the three ledgers S352 flagged, read line by line. For coverage, all 15 `HANDOFFS.md` files under
  `~/Development` were checked: 13 project ledgers, one git worktree of this repository
  (`methodology-bl57`, not an adopter), and this repository's own ledger as the control.
- **Criteria:** the structure checks of this repository's `bin/check-handoff` (table below).
- **Coverage:** 15 of 15 ledgers checked; 3 of 3 flagged ledgers investigated to the receipt, the line and the
  commit that made them. The other classes of finding (counted below) were *not* investigated line by line.
- **Findings:** 0 critical, 2 moderate, 1 minor (severity scale below). Three projects, two mechanisms
  (section "Structural Observations").

**Words used here.** A *ledger* is a project's `HANDOFFS.md`. A *receipt* is one block in it that a session
writes at close-out: a line of three backticks plus `handoff`, then `key: value` lines, then a closing line of
three backticks (together a *fence*). A receipt's *identity* is its `session:` value plus its `date:` value.
`reconciled` marks a receipt that a *later* session rebuilt from `git log` for work that has none of its own.

### Criteria

| Dimension | Question | Pass | Fail |
|---|---|---|---|
| Fence | Is every receipt opened and closed, and is none swallowed by another fence? | each opener has one closer; no opener inside a plain fence | an unclosed receipt, an opener inside a plain 3-backtick fence, fields outside any fence |
| Identity | Is each receipt's session + date unique in the ledger? | no pair repeats | "duplicate receipt identity" |
| Visibility | Does the checker see every receipt the file holds? | its receipt count equals the openers | a receipt the checker skips |

**Severity scale (so the numbers survive a hostile reading).** *Critical:* receipt text is lost, or the
project's next Phase 0 would act on false information. *Moderate:* the text is intact but a tool reads a
receipt wrongly (invisible, merged with another, or of ambiguous identity). *Minor:* only the checker's
complaint; every tool still reads every receipt.

## Findings

### Finding 1: `vscode_quarto_ext` — two receipts invisible to every check (Moderate)

- **Location:** `methodology/HANDOFFS.md:907` (a one-line stub), `:908-919` (the S284 receipt body, no opening
  fence), `:920` (a lone closing fence), `:922` (S283's opener).
- **Evidence:** the checker reports 12 structure findings: eleven "receipt field outside any fence" (eleven of the
  twelve lines of S284's body, 2026-10-01; the twelfth, `whats_next`, is not one of the checker's required keys) and one
  "a handoff opener inside the 3-backtick fence opened at line 920". Line 907 reads, in full:

  ````text
  ⚠ **The record grammar is FENCE-AWARE, so `grep -c '^```handoff
  ````

  It stops mid-sentence. It is the first half of a
  front-matter sentence (written whole at S254, `b17a0d0`, 2026-08-26); the second half exists nowhere in the
  file (`grep -c FENCE-AWARE` returns 1). The lone fence at 920 therefore *opens* a plain fence, which swallows
  S283's receipt (`:922-935`). The checker reads 91 receipts; after the repair below it reads 93: the two it
  was missing are S283 and S284.
- **How it got there (from the project's git history):** a session's claim stub was spliced into that sentence at its
  literal text `` ```handoff `` — at the S274 claim (`e979bd4`) and again at the S282 claim (`9bc4f01`,
  2026-10-01 12:49). The first was repaired by the next claim (`242e4f1`); the second never was. From the S285
  claim (`a6c7714`) on, the damaged line moves down the file as new receipts land above it: line 23 until S284's
  close-out, 31 at the S285 claim, 100 at the S289 close-out (`4a02cce`), 907 today. I did not find which tool or
  step does the insertion (the project has no claim script); the diffs show where it landed, not what did it.
- **Impact:** the checker, and anything that reads fences the way it does, skips S283 and S284. No text is lost.
  Nothing recent depends on them (the newest receipt is S338), so the next Phase 0 is not misled today.
- **Recommendation:** replace line 907 with an opening fence (`` ```handoff ``). Tested on a copy: 12 findings to 0,
  receipts seen 91 to 93. **Deleting line 907 alone does not work** (still 12). Optionally rewrite the lost sentence
  without the three-backtick text in mid-line prose (see Observation 3).

### Finding 2: `mts-system` — two reused identities and an unclosed receipt (Moderate)

- **Location:** `HANDOFFS.md:351` and `:367` (both `S195`, 2026-10-05); `:383` and `:398` (both `S194`, 2026-10-05).
  The block opened at 383 is never closed before the opener at 398.
- **Evidence:** 2 checker findings: at line 398, "a handoff opener inside the receipt opened at line 383 — the receipt was
  begun twice and is read as one block", and at line 367, "duplicate receipt identity — session 'S195' on date '2026-10-05'
  (first seen at line 351)". The `reconciled` receipts at 351 and 383 do not repeat the `complete` ones; they record
  commits the session's own receipt does not name (S195: `eab83f8`, `684ba16`, 18:00, a dashboard sync and a rule edit;
  its receipt says "Out-of-session commits after the S195 close-out". S194: `831549c`, 17:22, a CLAUDE.md amendment).
  They reused the owning session's id and date, which is what collides.
  The S194 pair hides the same collision: the missing closing fence makes the checker read the two blocks as one, so it
  never reaches the duplicate.
- **Impact:** a tool reading this ledger sees S194 as one receipt and S195 as two with one identity. No text lost.
- **Recommendation:** two edits, both needed. Give the `reconciled` receipts at `:352` and `:384` ids that differ from the
  `complete` ones, and add the missing closing fence after `:396`. Tested on copies: the fence alone leaves 2 findings (it
  *exposes* the S194 duplicate), the relabel alone leaves 1, both give 0. Both `ad-hoc-1`/`ad-hoc-2` and the project's own
  precedent at `:662` (`S179 (post-close-out housekeeping, …)`, the owning session's id plus a parenthesis) clear it.

### Finding 3: `church_growth` — one reconstructed receipt wears a session's id (Minor)

- **Location:** `methodology/HANDOFFS.md:756` (`S4`, `complete`, commit `692d2b7`) and `:817` (`S4`, `reconciled`, commit `3bfac0e`),
  both dated 2026-07-11.
- **Evidence:** 1 checker finding (duplicate identity). The two receipts are about different work (a visitor follow-up process
  draft; a PDF/HTML render of another document); 817 says of itself "Ad hoc rendering of two existing docs". The project's
  other reconstructed receipts (`:722`, `:795`) use `session: ad-hoc`.
- **Impact:** the checker's complaint only; each receipt is read separately.
- **Recommendation:** change line 818 (`session: S4`) to `session: ad-hoc-2`. Tested: 1 finding to 0. **Do not use
  `ad-hoc`**: the checker has no exemption for it, and `:795` is already `ad-hoc` on the same date (tested: it collides).

## Items Audited

Result is for the structure class (what S352 flagged). The right-hand counts are the checker's *other* classes, listed for
coverage and **not investigated**. Versions are the file's sha256 prefix and the project's git HEAD at audit time; no file in
a git project differed from its HEAD.

| Ledger | Version | Structure | Newest receipt | `commit:` slots | Over 65,536 B |
|---|---|---|---|---|---|
| airqino | 06a02646 @ f7a0194 | Pass | 0 | 6 | yes |
| chat_verification | 59453713 @ 0a8ef90 | Pass | 0 | 0 | yes |
| **church_growth** | dbb62d30 @ 62f7d8a | **Fail (1)** | 2 | 5 | yes |
| claude_work (no git) | f9a83f51 | Pass | 0 | 0 | no |
| dalia_martinez_funeral | 5513a4d1 @ 5cd7b91 | Pass | 0 | 0 | no |
| data_quality_assurance | 8f112910 @ 31fb7a8 | Pass | 0 | 2 | yes |
| feedback-loop-comparison | 60fa0a03 @ 2e77a73 | Pass | 0 | 0 | no |
| methodology (this repo, control) | ed68a423 @ 137238ee | Pass | 0 | 0 | no |
| methodology-bl57 (worktree) | b8d4b2a5 @ 77afc127 | Pass | 0 | 2 | yes |
| model_project_constructor | cb66fdd8 @ 66fbd6f | Pass | 0 | 20 | yes |
| **mts-system** | 2174c09d @ 512b3f7 | **Fail (2)** | 1 | 20 | yes |
| nprcgenekeepr | 3cb6544d (HEAD moved during the audit) | Pass | 0 | 1 | no |
| Philippians | f4bdd29a @ 427e634 | Pass | 0 | 24 | yes |
| **vscode_quarto_ext** | beb4464e @ 3be8ca8 | **Fail (12)** | 3 | 88 | yes |
| wsfct | e209a54c (HEAD moved during the audit) | Pass | 0 | 137 | yes |

`wsfct` and `nprcgenekeepr` committed during this session (their git HEAD moved); their ledger files were byte-identical across
both of my runs.

## Structural Observations

1. **The three duplicate-identity pairs (two in `mts-system`, one in `church_growth`) share one cause: a `reconciled` receipt for
   work that no session receipt covers, written with an id already in use.** The format has no id for it. `starter-kit/HANDOFFS.md:72-73` defines `reconciled` only for
   "a receipt a crashed session never completed", and `:82` makes identity `session` + `date` with no exemption. A session that
   reconstructs a receipt for out-of-session commits (`mts-system`, twice) or for ad hoc work (`church_growth`, once) must invent
   an id, and two projects invented one that collides. This is a gap in the distributed text, not only in three projects.
2. **Nothing shows adopters.** `bin/check-handoff` is canonical-only, so all three defects survived the 11 days with 2 ledger
   commits in `mts-system` and 41 in `vscode_quarto_ext` (`church_growth`'s ledger has not been committed since 2026-10-10).
3. **The splice is the second mechanism, and it has happened here too.** S352's own measurement found this repository's ledger with
   a claim stub spliced into the front matter in four committed versions (S196, S246, S252, S267). Today four ledgers carry the text
   `` ```handoff `` mid-line in prose, the exposure: `vscode_quarto_ext` lines 907 and 1448, `mts-system` 71, 828, 829,
   `methodology-bl57` 130 and 132, and this repository's 22, 41, 76 and 92 (line numbers at the time of the audit). The distributed
   seed `starter-kit/HANDOFFS.md` has none.
4. **The wider picture, counted and not investigated:** 11 of the 15 ledgers fail the checker, but for other reasons. 10 ledgers carry
   305 older receipts whose `commit:` slot is not a sha (`wsfct` 137, `vscode_quarto_ext` 88, `Philippians` 24,
   `model_project_constructor` 20, `mts-system` 20, then 6, 5, 2, 2, 1); 10 are over this repository's 65,536 B ceiling (a rule of this
   repository, not of theirs); `methodology-bl57` also has 3 "positional ledger address" findings; the newest receipt fails its schema only
   in the three flagged projects. **Do not read the 305 as adopter defects.** The checker's comments (`bin/check-handoff:56-60`, `:748`) and
   the backlog row BL-14 (`docs/planning/BACKLOG-DETAIL.md:174-212`) say the spec promises that the next session reconciles `commit:`.
   The spec says the opposite: `starter-kit/HANDOFFS.md:76-80` calls `pending` "a legitimate resting value … not a promise a later session
   owes", wording that commit `33d8c640` (2026-08-10) put in on purpose, and `upstream/main` has the same text. So the checker flags, as errors,
   values the distributed spec allows, and BL-14's premise ("the spec still promises a reconcile") is stale. I found this while counting;
   it is not resolved here.

## Comparison with the Prior Audit (S352, 2026-10-20)

Source: the ledger entry "2026-10-20 · [BL-89] S352 -- `bin/check-handoff`'s everyday run reads the ledger's structure" in
[`docs/archive/CHANGELOG-through-2026-10-23.md`](../archive/CHANGELOG-through-2026-10-23.md) (line 438), and the versions of the three files
that existed then, reproduced from each project's git history (script, part B).

| Metric | S352 (file version then) | Now | Trend |
|---|---|---|---|
| Projects with structure findings | 3 of 14 | 3 of 14 (the same three) | unchanged |
| Findings: church_growth / mts-system / vscode_quarto_ext | 1 / 2 / 12 | 1 / 2 / 12 | unchanged |
| Repaired since | n/a | 0 of 3 | none |
| Ledger commits to the file since | n/a | 0 / 2 / 41 | projects kept working |
| Line shift | n/a | 0 / +16 / +217 | the numbers S352 quoted have moved |
| New findings | n/a | 0 | none |

**One correction to S352's record.** It says "`mts-system` S195 begun twice and twice on one date". In the file as S352 read it
(version `467c11d`), the receipt begun twice is **S194** (openers at 367 and 382); S195 is the pair on one date (335, 351). Today's
lines are 383/398 and 351/367.

## Recommendations

Nothing here has been done. Edits to another project's file belong to a session in that project; the choices are the operator's.

1. **The three repairs** (each tested on a copy, never on the adopter), as listed under each finding: `church_growth:818` to
   `session: ad-hoc-2`; `mts-system:352` and `:384` relabelled plus a closing fence after `:396`; `vscode_quarto_ext:907` to an opening fence.
   Whether to hand them to the projects, and how, is the operator's call (the line numbers move as the projects write; the script's asserts
   will say so).
2. **A convention for the id of a reconstructed receipt** in `starter-kit/HANDOFFS.md` (Observation 1), with a checker test. It is a change to
   a distributed file, so it is upstream-facing: it would ride a future batch (`CLAUDE.md` prefers one vetted pull request to several small
   ones) and needs the operator's go-ahead to leave this repository; nothing is started.
3. **Whether adopters should be able to see this** (Observation 2): distributing the structure half of the checker is a design question for
   the maintainer, not a fix to apply.
4. **Reconcile the checker with the spec on `commit:` slots** (Observation 4): either the checker's note and BL-14's premise are corrected
   to the spec's text, or the spec is changed back on purpose. That is its own session in this repository (a fork-only checker, and a
   distributed spec if the second way); nothing is started.

## Limits of this audit

- The checker is this repository's at commit `3f97ba72`; a different version would count differently. Class counts other than structure
  are descriptive only.
- Two projects were live (`wsfct`, `nprcgenekeepr`); a run at another time may differ. The three audited ledgers did not change between runs.
- The cause of the splice (Finding 1) is shown by diffs, not by finding the tool; the other reading ("a person edited by hand") is not ruled out.
- I did not test any adopter's own tooling against these defects (for example its copy of the trimmer).

## Reproduce

`python3 -I docs/audits/2026-10-31-adopter-ledger-defects-evidence.py` (read-only; `-v` prints every finding, about 200 KB). Its
saved output is [`2026-10-31-adopter-ledger-defects-evidence-output.txt`](2026-10-31-adopter-ledger-defects-evidence-output.txt); the script is
[`2026-10-31-adopter-ledger-defects-evidence.py`](2026-10-31-adopter-ledger-defects-evidence.py). Part C asserts the exact line each repair test edits and
prints SKIPPED, with the reason, if a project has moved or repaired it since.
