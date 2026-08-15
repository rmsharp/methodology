# Backlog archive — closed items, frozen 2026-08-15

**Frozen.** These are the **11 closed items** that had accumulated inside
[`BACKLOG.md`](BACKLOG.md)'s `## Open items` section. Each body below is **byte-identical** to
the text that stood in `BACKLOG.md` at commit `201e84e`, moved here unchanged — nothing was
summarised, reworded, or dropped. `BACKLOG.md` keeps a one-line pointer row for each in its
`## Completed items` table.

**Why this file exists.** `SESSION_RUNNER.md` Phase 3F requires removing a completed item from
`BACKLOG.md` in the same commit that closes it. That step was skipped 11 times, so a file whose
job is *"open work only"* carried 45,288 B — a third of itself — of finished work, and grew to
2.10x the 65,536 B budget its own ledgers are held to. S88 measured the cost: BL-36 was raised
into this file 471 lines below **BL-27, which already contained its answer**, and no one found it.
That is failure mode #28 (unbounded mandatory read), and this is its decay term.

**This is not a `methodology_trim.py` trim, and could not have been.** Every `LedgerSpec` in that
tool requires a `date_of_record` and freezes the **oldest by date**. A backlog's reduction axis is
**status, not age** — BL-11 (2026-08-01) is open and retained here, while BL-35 (2026-08-11) is
fixed and archived. A date-keyed trim would have archived the open items and kept the closed ones.
See `BL-32` in `BACKLOG.md` for the standing question that finding answers in part.

**Losslessness is proved, not asserted.** Run
[`BACKLOG-archive-2026-08-15.md.verify.sh`](BACKLOG-archive-2026-08-15.md.verify.sh), which
re-extracts each item from `git show 201e84e:docs/planning/BACKLOG.md` and compares it
**byte-for-byte against this file, keyed on the item's own identity (`BL-N`), never on its
position** — the positional-identity defect that makes four of the six shipped ledger `.verify.sh`
proofs read FAIL on intact archives (BL-36, `docs/audits/2026-08-15-bl36-archive-losslessness.md`).

**Order is numeric, not chronological**, so an item is found by its number alone. Items are *not*
renumbered, here or in `BACKLOG.md`.

**One item was not fully archived.** `BL-20` closed as option (1) of three and left option (3)
**genuinely open** — a DISTRIBUTED seed change needing its own go-ahead. Its closed history is
below; a live stub carrying only that open residual stays in `BACKLOG.md` §Open items.

| Item | Subject | Outcome |
|------|---------|---------|
| **BL-8** | Subagent capability-tiering — adopt as an operational default, or decline | ADOPTED 2026-08-11 (S78) |
| **BL-15** | `changelog_ref`'s deictic deferral — raised correctly, already discharged | CLOSED 2026-08-02 (S29) |
| **BL-20** | `bin/model-report`'s Source 1 is blind to the `**Model:**` form this repo writes | FIXED 2026-08-11 (S79), option (1) |
| **BL-24** | `mts-system` cleared both UAT blocking conditions — focused re-run | CLOSED 2026-08-08 (S50) |
| **BL-25** | Focused `vscode_quarto_ext` UAT re-run | CLOSED 2026-08-08 (S53) |
| **BL-27** | `methodology_trim.py`'s generated `.verify.sh` — two false-positive triggers on `HANDOFFS.md` | CLOSED 2026-08-10 (S65) |
| **BL-28** | The generated `.verify.sh`'s L2 front-matter check was a substring test, not exact-line-set membership | CLOSED 2026-08-10 (S68) |
| **BL-29** | D4(c)'s directory-exclusion fix did not cover the self-scan case it was meant to close | CLOSED 2026-08-10 (S72) |
| **BL-33** | `bin/model-report`'s `CHANGELOG_ENTRY_RE` can't parse a multi-tag `### ` header | FIXED 2026-08-11 (S80) |
| **BL-34** | `methodology_dashboard.py`'s `LANG_MAP`/`DOC_EXTS` are blind to R, Quarto, and R Markdown | FIXED 2026-08-11 (S81), merged upstream + synced 2026-08-12 (S86) |
| **BL-35** | `starter-kit/FRAMEWORK_LEARNINGS.md` rows 18 and 19 were malformed 2-column rows | FIXED 2026-08-11 (S84) |

---

**BL-8 — Subagent capability-tiering: adopt as an operational default, or decline. ADOPTED (S78).**
*Not a methodology change, and no document needs editing.* `SESSION_RUNNER.md` §Vertical Slice
Sessions already carries the decision rule (v3.5, BL-7) — explicitly **elective**, scoped to
pre-declared vertical slices — and `RECOMMENDED_SKILLS.md` states the default outright:
*"Elective; single-tier-throughout remains the default."* The open question is narrower and purely
operational: when a session authors a **workflow** whose subagent roles rest on an objective,
checkable gate (extraction re-verified by executing the module; corpus sweeps re-verified downstream),
should those roles be authored onto a lighter tier while judgment roles and review stay on the
strongest? Note the current campaign is **horizontal** (one layer per session), not a slice, so the
v3.5 mechanism does not formally govern it — this would be applying its *principle* to a context the
document does not cover.
*Measured in S14, against its own 48 subagents:* all-Opus **$132**; all-Sonnet **$79** standard /
**$53** intro; **hybrid ~13–19% saving** — much less than the headline, because the judgment-heavy
verifier role is **61% of input tokens**. Cache reads are **91.7%** of all input. Sonnet intro
pricing ends **2026-08-31**.
*The larger lever measured alongside it, and the better first move:* **8 of 36 verifier agents
re-verified a site another slice had already surfaced** (dedupe findings before spawning verifiers),
and the review budget should be reserved *before* the discovery sweep — S14's sweep consumed the
budget and its review then died on a usage limit, which is why Layer 5 shipped unreviewed and later
needed three prose fixes. Both are free of any quality tradeoff.
**"Decline and keep single-tier" is a correct outcome** and matches the documented default; the only
cost is the saving above.

**ADOPTED 2026-08-11 (S78), operator-directed.** Presented the measured tradeoff above (13-19%
saving, driven down because the judgment-heavy verifier role is 61% of input tokens; the
dedupe/budget-reservation lever is separate and free of the tradeoff) and asked the operator to
choose between adopt and decline; the answer was **adopt**, accepting the modest saving.
**The operational rule this fork now applies when authoring a `Workflow` script:** a subagent role
whose correctness rests on an objective, checkable gate (a test suite it must pass, an exhaustive
grep-reconciliation, a module it re-verifies by executing — the same bar `SESSION_RUNNER.md`'s
§Vertical Slice Sessions "Capability-tiered review" already sets for slice layers) may be authored on
a lighter/faster tier; a role whose correctness rests on judgment across interacting constraints no
such gate expresses (the verifier/refuter role, any role adjudicating "is this finding real," brand-
neutral wording, cross-file invariants) stays on the strongest available tier — and so does every
review pass over a delegated role's output, never batched at the end. This extends the
already-documented principle from its current scope (pre-declared vertical slices) to horizontal
`Workflow`-authored campaigns, which that text does not formally cover. **Still not a methodology
change** — no distributed document is edited, because the extension is this fork's own operational
practice for authoring its own workflows, not a new recommendation for adopters.
Independently of tiering, also adopt the two tradeoff-free levers measured alongside it: dedupe
findings against what earlier stages already surfaced before spawning verifiers, and reserve the
review budget before the discovery sweep can spend it down (S14's own failure: the sweep spent the
budget and Layer 5 shipped unreviewed).

**BL-15 — `changelog_ref`'s deictic deferral: RAISED CORRECTLY, AND ALREADY DISCHARGED.**
*Settled 2026-08-02 (S29). Do not re-raise; the count below is the third time this population has
been measured and the first time it was measured right.*
**BL-15's "13 of 32" is exact.** 13 `changelog_ref` values defer deictically instead of naming an
identifier — **12 × `this commit` plus archive-S1's `this branch`**. S29's claim stub asserted the
population did not reproduce under any predicate; that assertion was **wrong**, and wrong the way
[`feedback_a_grep_count_is_a_sample`] describes: it grepped one literal phrasing, reached 12, and
stopped one variant short. `bin/check-handoff:69-70` names the dialect in writing —
*"it catches the `this commit — ...` dialect that names no sha at all"* — so the key was documented
and was not used. The provenance settles the "identical" wording too, and it is textual rather than
analogy: `starter-kit/HANDOFFS.md:63` specifies `changelog_ref: <PR #N or a short-sha into
CHANGELOG.md>` and `:88` says outright *"the shared key across all three is the commit sha
(`changelog_ref` / `commit` here)"*; the ratified plan agrees at
[`close-out-receipt-durable-artifact-plan.md:105`](close-out-receipt-durable-artifact-plan.md).
**Why it is nonetheless closed rather than open.** Two measured facts, neither of which was
available when BL-15 was raised one session earlier:
- **All 13 name their entry by a quoted `### ` title BEFORE the deferral** — "…entry, this commit".
  The deferral is a trailing modifier, never the answer slot. BL-14's escape was categorical: S25
  and S26's `commit:` read `this commit` **and nothing else, with no sha anywhere in the receipt**.
- **All 13 now carry a real sha as their own `commit:` first token**, because `7752114` and
  `6d47624` forced it. Each deictic reference is therefore a one-hop back-reference to a field the
  checker already guarantees. **BL-14 discharged BL-15 as a side effect** — which is the honest
  finding, and better than either "wrong" or "open".
*What no longer stands:* the parenthetical about a *"legitimately pending PR number"*. Zero of the
32 values contain the literal `pending`, and the seed's `PR #N` form appears in **no** receipt —
only in `bin/tests.sh` fixtures. Nothing in the corpus can produce that false positive.
*Residual, deliberately not mechanized:* the one-hop resolution is a convention no document states.
Writing it down means editing `starter-kit/HANDOFFS.md`, which is **DISTRIBUTED** — see BL-17.

**BL-20 — `bin/model-report`'s Source 1 is blind to the `**Model:**` form this repo actually writes.**
*Raised 2026-08-02 (S31), found while verifying a claim S31 was about to publish about its own split.
Not fixed in that session (FM #17): the split was the deliverable, and this is a tool/convention
mismatch with at least three defensible fixes.*
**The defect.** `CHANGELOG_MODEL_RE` (`bin/model-report:51`) is `^-\s*\*\*Model:\*\*\s*(.+)$` — the
list form the distributed seed documents (`starter-kit/CHANGELOG.md:42`, `:57`, `:69`). This repo's
live ledger writes the bullet as a bare `**Model:**` at line start, which that regex cannot match. So
`python3 bin/model-report` prints *"(no CHANGELOG.md entries carry a **Model:** bullet)"* against a
file containing nine of them. Source 1 is the **primary, structured** source; it fails silently and
reads as "no data recorded" rather than "not parsed."
**Population, both dialects, frozen at the tree it was measured against** (`74479df`, S31's claim, so
the figure cannot decay): 14 bullets corpus-wide — **9** bare, all in the live `CHANGELOG.md`, and
**5** list-form, all in `docs/archive/CHANGELOG-through-2026-08-01.md`; 0 in the v3.6 shard. It is
already stale at HEAD — S31's own close-out entry made it 10 bare / 15 total, which is the point.
Re-measure, never recall:
`grep -cE '^-?[[:space:]]*\*\*Model:\*\*' CHANGELOG.md docs/archive/CHANGELOG-*.md`
**Drift point, derived not guessed:** `54426cb` (2026-08-01) is the last commit with list-form only;
`1298af7` (2026-08-02) is the first bare-form entry, and every one of the nine entries since has
followed it — a same-day convention change that no check noticed because the only reader is
non-gating and its empty output is indistinguishable from an unrecorded field.
**Consequence of S31's split, recorded because it is counterintuitive:** the split moved 100% of what
Source 1 can parse into the archive. The tool's default invocation is now empty, and its front-matter
note in both ledgers says so.
**Three fixes, and the choice is the deliverable:** (1) widen the regex to accept both dialects —
smallest, but blesses a form the seed does not document; (2) normalize the nine live entries to the
seed's list form — restores the documented convention, but rewrites dated entries, which the v2.7.1
convention forbids; (3) change the seed to document the bare form — **DISTRIBUTED, so it ships
upstream and needs a go-ahead.** Note (1) and (2) are fork-side, so this can advance today either
way.
**Related:** this is the same shape as BL-14/BL-15 — a promise in the seed with no detector — except
here the detector exists and reads the wrong dialect.

**FIXED 2026-08-11 (S79), option (1).** `CHANGELOG_MODEL_RE` (`bin/model-report:51`) widened from
`^-\s*\*\*Model:\*\*\s*(.+)$` to `^-?\s*\*\*Model:\*\*\s*(.+)$` — the leading `- ` is now optional,
not required, so Source 1 matches both dialects. Option (2) (normalize the live entries to list
form) was ruled out, not chosen against: it rewrites dated `CHANGELOG.md` entries, which the
v2.7.1 convention forbids outright. Option (3) (change the seed to document the bare form) remains
genuinely open — it would close the last gap (the seed still only documents the list form the live
ledger doesn't use) but is a DISTRIBUTED change that ships upstream and needs its own go-ahead;
not taken this session, not blocking this fix.
RED-first (Learning #12): confirmed pre-fix that a bare-form fixture, and this repo's own live
`CHANGELOG.md`, both fell through to `(no CHANGELOG.md entries carry a **Model:** bullet)` before
touching the regex. New Test 30 in `bin/tests.sh` fixtures both dialects side by side plus a
no-bullet control (so an over-wide fix would still be caught), and asserts against this repo's own
live `CHANGELOG.md` directly, not only a synthetic fixture.
Re-measured, not recalled, and reconciled against the tool's own post-fix output rather than trusted
as a bare grep count: `grep -cE '^-?[[:space:]]*\*\*Model:\*\*' CHANGELOG.md` → **52** anchored
bullets in the live file (5/10/68/0 across the four archive shards); `bin/model-report`'s own
post-fix entry count is **51**, one lower. The gap is real and is NOT this fix — re-derived down to
a single cause, a second, separate, pre-existing `bin/model-report` defect (a multi-tag `### `
header silently folding into its predecessor rather than failing to match loudly), raised as its own
item, **BL-33**, and deliberately not fixed here (FM #17: this session's one deliverable was BL-20).

**BL-24 — `mts-system` cleared both UAT blocking conditions; focused re-run CLOSED (S50).**
*Raised 2026-08-08 (S49), from a live conversational spot-check triggered by the operator, not a
scheduled sweep. Closed the same day (S50). Full evidence:
[`uat-2026-08-08-followup.md`](uat-2026-08-08-followup.md) §7 (raised) and §8 (closed).*

`mts-system` was one of three repos the S48 UAT follow-up recorded as carrying uncommitted work
(§6 there). Re-checked live at ~15:30 today: `git status --porcelain` reads **0** dirty paths (was
**2** at S48's 14:00 snapshot), and `bin/sync --dry-run ../mts-system` remains unblocked (exit 0 —
it was never F4-blocked, only the "carries uncommitted work" condition applied). The change is real,
independent adopter-side activity, not anything this fork did: `mts-system`'s own commit log shows an
internal session (its own "S95") closed out and left the tree clean about 1.5 hours after S48's
snapshot. Two things also worth noting, found in the same spot-check but out of this item's own
scope: `mts-system`'s `dashboard_history.jsonl` (F9) now looks independently tracked/resolved there
too; F2's dangerous `BOOTSTRAP.md:330` text is unchanged, byte-identical (closes only upstream, §6).

**CLOSED 2026-08-08 (S50):** ran the focused UAT pass this item queued — re-derived F6, F7, F9, F10,
F11 against `mts-system`'s current state (F1/F3/F4/F8/F12 correctly scoped out, per this item's own
framing). **F9 confirmed resolved** (tracked, deliberately unignored, documented in `.gitignore`) —
S49's "looks independently resolved" hedge is now a verified fact. **F10 improved, 1 → 0** reconcile
debt — new information this item's own scope didn't originally ask for but the re-run surfaced.
**F6 and F7 reproduce unchanged, still open** — the dashboard's presence-only compliance blind spot
and `check-handoff`'s all-numeric-sha false positive on receipt S74 both still stand exactly as S43
found them. **F11 not applicable** — `mts-system` was never one of the three repos missing
`HANDOFFS.md`. Zero regressions. Read-only throughout; `git status --porcelain` inside `mts-system`
confirmed 0 dirty paths both before and after. No sync or write action was taken or authorized.

**BL-25 — Focused `vscode_quarto_ext` UAT re-run, raised and CLOSED same session (S53).**
*Operator-directed 2026-08-08 (S53), choosing `vscode_quarto_ext` from three offered alternatives
(issue #67/PR #66, this fork's own F9 instance, F3). The `mts-system` counterpart to BL-24, run
against the other repo §7 flagged as "closer, not identical." Full evidence:
[`uat-2026-08-08-followup.md`](uat-2026-08-08-followup.md) §9.*

Pre-condition re-verified at claim: `git status --porcelain` **1** dirty path (`?? scratchpad/`, an
untracked non-methodology scratch directory, not a modified-tracked-file conflict — unchanged from
§7's S49 snapshot); `bin/sync --dry-run ../vscode_quarto_ext` exit 0, unblocked (never F4-blocked).
Re-derived **F2, F3, F6, F8, F9, F10, F11**, plus two bonus checks never run against this repo before
(**F1**, **F4**). **F9 confirmed resolved** — tracked, not ignored, not dirty; last touched by
`fe1e05b` with two further unrelated session commits landing since and leaving it untouched, which
upgrades §7's (S49) "committed cleanly today" hedge to a verified fact, the same upgrade BL-24 gave
`mts-system`'s F9. **F2, F3, F6, F8 reproduce unchanged, still open** — `BOOTSTRAP.md:330`'s
"overlay them" text is byte-identical; `SESSION_NOTES.md` grew to 7,549 lines/506 headings (+81/+6
since S43); the dashboard's 100%-compliance/11-drifting-files blind spot reproduces exactly, `bin/status`
now naming `SESSION_RUNNER.md`/`BOOTSTRAP.md` 8 versions behind; `ZONE_UNCLASSIFIED` still fires on
`HANDOFFS.md`, now at line 2807 (was 2771 — the shift is the file growing, not a new defect). **F10
unchanged at 0; F11 not applicable** (has `HANDOFFS.md`). **Both bonus checks came back clean**: F1's
original grammar-mismatch bug was never present in this repo's `CHANGELOG.md` (the trimmer's
`TRIGGER_BYTES` check fires correctly, no `NO_RECORDS`/`GRAMMAR_MISMATCH`); F4 confirms this repo was
correctly excluded from the "2 of 6 blocked" set. Adjacent, not a numbered finding:
`bin/check-handoff` now counts 96 unreconciled `commit:` answer slots (S38–S186), up from §4's 93
(S38–S184) — ordinary adopter ledger-hygiene drift, not a new tool defect. **Net: 1 of 7 improved
(F9), 4 unchanged/open (F2, F3, F6, F8), 2 unchanged-and-clean (F10, F11), zero regressions.**
Read-only throughout; `git status --porcelain` inside `vscode_quarto_ext` confirmed identical (1
dirty path) both before and after. No sync or write action was taken or authorized.

**BL-27 — `methodology_trim.py`'s generated `.verify.sh` has two known false-positive triggers on
`HANDOFFS.md`, distinct from the internal `--check`/`--write` assertions, which do not share them.
CLOSED (S65).**
*Raised 2026-08-10 (S64), found while independently re-running the tool's own generated proof for a
routine `HANDOFFS.md` archive-cut — the practice this repo's own precedent (S61, S63) established
specifically to avoid trusting the tool's write-time summary.* Both are reproduced, not inferred:

1. **Front-matter field regeneration reads as data loss.** `HANDOFFS.md`'s front matter carries a
   `This file currently holds **N**` receipt count that the tool mechanically regenerates on every
   archive (`[FRONTMATTER_FIELD_REGENERATED]`, e.g. `30 → 3` this session). The internal `assert_L2`
   check correctly excuses this — it reverses every *declared* regeneration and requires the original
   bytes back (`starter-kit/methodology_trim.py:523-563`) — but the simpler, self-contained check
   embedded in the generated `.verify.sh` only asserts "every non-blank line of the original front
   matter survives verbatim," with no concept of a declared exception. Any archive that changes this
   line — every one, since the count always changes — makes the standalone proof report
   `FAIL: L2 FRONT MATTER lost 1 line(s)` even though nothing was lost. Reproduced live this session:
   `docs/archive/HANDOFFS-through-2026-08-09.md.verify.sh` fails this way; manually diffing
   `HEAD:HANDOFFS.md` against the pre-commit working tree confirmed the *only* front-matter changes
   were the declared count regeneration and the declared pointer-block insertion — genuinely lossless,
   just not provable by the generated script as currently written.
2. **A same-commit close-out bundling reads as record alteration.** This repo's own established
   practice (S61, S63, and this session) commits an archive's `--write` output together with
   finalizing the session's *own* close-out receipt (`status: pending` → `complete`) in one commit.
   The frontier record (the newest, never archived) therefore legitimately differs between that
   commit's parent and itself — a fact the internal test suite already names and accepts
   (`tools/test_methodology_trim.py`'s `test_L3_fixture_is_the_event_that_bundled_an_edit_with_the_move`,
   fixture `7a71df0`, S23's original archive). But `.verify.sh`, re-run in commit-comparison mode
   after the fact, has no such exception and reports `FAIL: L3 record(s) not byte-identical … [0]` /
   an `L1` mismatch. Reproduced live this session against `docs/archive/HANDOFFS-through-2026-08-02.md.verify.sh`
   (S61's shard, untouched since `c0e6944`, same tool version `v1.1.1` throughout) — its record-0
   "alteration" is exactly S61's own receipt going from its pending stub to its finished self-score-7
   form, all within `c0e6944`. **This is not evidence of historical data loss** — S61's actual archive
   move is intact — but it does mean a past session's disclosed "independently re-ran `.verify.sh` —
   OK" can go stale the moment the receipt is later finalized into the same commit, and a *future*
   re-run of that same frozen script, done for due diligence, will misread as a fresh finding of loss
   unless the reader already knows this pattern.

**Practical mitigation already used this session, not a fix:** run `.verify.sh`'s underlying check
in the working-tree window *before* finalizing the session's own receipt (which is when `L1`/`L3`
are still meaningful), and rely on a manual front-matter diff — not the generated script's verdict —
for `L2`. **Not fixed here (FM #17):** the two real fixes are (a) teach the `.verify.sh` generator
the same declared-field-reversal exception `assert_L2` already has, and (b) either exempt the
frontier record from the generated script's `L1`/`L3` comparison when it's the only one to change, or
document the bundled-commit pattern in the script's own output so a `FAIL` doesn't read as an
unqualified loss. Both are changes to a canonical, adopter-distributed tool (`bin/_manifest.py`) and
need their own RED-first tests against `tools/test_methodology_trim.py`'s existing 91-test suite —
scoped as a session of its own, not folded into a trim.

**CLOSED 2026-08-10 (S65):** fixed both, in `VERIFY_TEMPLATE`/`build_verify`
(`starter-kit/methodology_trim.py`, the sole canonical copy — no `tools/` twin to mirror). (1) A new
`@@REGEN@@` template variable carries `spec.regenerated`'s declared field patterns into the
generated script (`repr()`'d, since it is 0-or-more patterns, not the single-pattern case
`@@START@@`'s r-string wrapper already handled); a `field_reversible()` helper excuses a "missing"
line only when it has a same-shaped partner elsewhere in the new front matter, identical everywhere
outside the declared field's own span. (2) L1/L3 now share one `rebuilt`/`bad`-index computation;
when the only altered record is position 0 (the frontier) the script still FAILs — a real loss can
have this exact shape — but also prints a `NOTE:` naming the known bundled-commit pattern, so a
`FAIL` here no longer reads as unqualified. RED-first: 4 new tests in a new
`TestVerifyShHandoffFalsePositives` class (`tools/test_methodology_trim.py`), a new
`make_handoff_repo` fixture (the suite's first end-to-end `HANDOFFS.md` trim through the actual
subprocess, not just `assert_L2` in isolation); both fix-tests confirmed RED against unpatched code
for the exact defects above, both narrowed controls confirmed already-green unpatched (proving the
fix doesn't become a blanket permit). Suite 91 → 95, all green; full `bin/tests.sh` unaffected.
`TRIM_VERSION` 1.1.1 → 1.1.2 (patch — no new finding code or exit status on the tool's own CLI, a
correctness fix to generated output). One real finding surfaced while building the first control
test, not fixed here: **BL-28**, its own entry below.

**BL-28 — the generated `.verify.sh`'s L2 "missing front-matter line" check is a substring test,
not an exact-line-set membership test, so an APPEND-style edit that keeps the original text as a
literal substring of the new line is invisible to it.** *Raised 2026-08-10 (S65), found while
building BL-27's own narrowed control test.* The check is `ln not in afront` — `afront` is the
whole front-matter TEXT, not a list of lines, so `in` is substring containment. A tamper of
`"# Handoff Receipts"` → `"# Handoff Receipts EDITED"` (append, not replace) left the original 19
characters intact as a literal prefix of the new line, and the check reported no loss — reproduced
live via the actual generated script, not inferred. **Pre-existing, not introduced by BL-27's fix**:
the same substring check was there before this session touched the file; BL-27's own fix (the
declared-field-reversal exemption) only *exposed* it, by removing a co-occurring, unrelated false
positive (the regen-field "loss") that had been accidentally covering for it in BL-27's own first
draft of that control test — the tamper appeared caught, but for the wrong reason. **The INTERNAL
`assert_L2` (used by `--check`/`--write`) does not share this defect** — it compares the whole
front-matter TEXT for exact equality after reversing declared changes (`residue != before_zones.front`),
which an append-style edit still fails correctly; the bug is specific to the standalone script's
separately-written, weaker line-based reimplementation. **Not fixed here (FM #17):** the fix is to
compare an exact set/sequence of lines (or reuse the internal residue-equality approach) instead of
substring containment — a change to the same canonical, adopter-distributed tool, needing its own
RED-first test. Low severity in practice (an append that happens to preserve the exact original
text as a contiguous substring is a narrow tamper shape), but real, and this file's own precedent
(BL-27) is to record what is found even when it is not what was being looked for.

**CLOSED 2026-08-10 (S68):** fixed in the same `starter-kit/methodology_trim.py` template (the sole
canonical copy — no `tools/` twin to mirror). The "missing" check now builds `afront_lines =
set(afront.splitlines())` once and tests `ln not in afront_lines` — exact membership in the new
front matter's line set — instead of `ln not in afront` (substring containment on the whole text).
`field_reversible()`'s own separate, correct line-by-line carve-out for the declared regenerated
fields is untouched. RED-first: a new `TestVerifyShAppendTamperEvadesSubstringCheck` class
(`tools/test_methodology_trim.py`) with the exact reproduction from this entry (`"# Handoff
Receipts"` → `"# Handoff Receipts EDITED"`, append not replace) — confirmed FAILing (no `FAIL:` in
the script's output) against unpatched code before the fix, `FAIL: L2 FRONT MATTER` after; a
narrowed control re-confirms the regenerated-count field still passes unpatched-and-patched, so the
fix doesn't turn the exact-line-set comparison into a blanket new false positive. Trimmer suite 95 →
97, all green; full `bin/tests.sh` unaffected. `TRIM_VERSION` 1.1.2 → 1.1.3 (patch — no new finding
code or exit status on the tool's own CLI, a correctness fix to generated output, same class as
1.1.2). The sibling BL-27 control test's own comment about needing a full-line replacement (not an
append) for its tamper — because an append would have been invisible to *this* defect — is now
historical: an append-shaped tamper is caught too, verified by the new test above it in the same
file.

**BL-29 — D4(c)'s "methodology" directory-exclusion fix does not cover the self-scan case it was
meant to close.** *Raised 2026-08-10 (S70), found while investigating cross-repo methodology-adoption
effects for the operator; reproduced live, not inferred.*

D4(c) (`0e188f5`, 2026-08-03, `DASHBOARD_VERSION` 2.10.3 → 2.11.0) removed `"methodology"` from
`EXCLUDE_DIRS` — but its own commit message discloses the naive form couldn't ship as worded, because
`discover_projects()` has two consumers and `sync_dashboards()` is a write path, so the naive removal
"would have made `--sync` install a third copy into this repo's own root." A different fix landed
instead ("Fixed and mutation-proved"), and S69's own `HANDOFFS.md` receipt separately flagged, but did
not chase, that `python3 tools/methodology_dashboard.py` run in-place from this repo's own root still
reports "No projects found" rather than scanning this repo as a single project. Reproduced live this
session, against current `HEAD` (`DASHBOARD_VERSION` 2.14.0):

```sh
$ python3 tools/methodology_dashboard.py --no-open
Methodology Dashboard: No projects found.
```

The portfolio-root copy (`/Users/rmsharp/Development/methodology_dashboard.py`) scans this repo
correctly as part of the 13-project portfolio — the defect is specific to running the in-repo copy
from its own root in single-project mode, the same `single_project = (root / ".git").exists()` branch
`main()` already special-cases for its title text but apparently not for discovery. **Not fixed here
(FM #17):** whoever revives it should first re-read the D4(c) commit's own account of why the naive
fix was rejected, so a second attempt doesn't reintroduce the write-path collision it already found
and avoided once.

**CLOSED 2026-08-10 (S72).** Re-read D4(c)'s own account first, as this entry asked: its collision
was in `sync_dashboards()` (a WRITE path taking `discover_projects()`'s exclusion set with it), a
different function from the one `main()`'s plain scan calls `discover_projects()` through — so this
fix never touches `EXCLUDE_DIRS`, `discover_projects()`, or `sync_dashboards()` at all, and cannot
reintroduce that collision. The actual defect was `ROOT = Path(__file__).parent`: correct for every
adopter-installed and portfolio-root copy (all sit exactly where `bin/_manifest.py` /
`sync_dashboards()` place them), wrong for the methodology repo's own two checked-in copies
(`tools/`, `starter-kit/`), which file the script one level BELOW the repo they belong to. Fixed with
a new `resolve_single_project_root()` (both twins) that bridges `ROOT` to its parent only when
`ROOT.name` is `tools` or `starter-kit` AND the parent both is a git repo and carries
`bin/_manifest.py` — the same structural marker `detect_repo_role()` already trusts to prove "this
is the framework's own publishing repo", which no adopter can acquire via `bin/sync`. Deliberately
narrow: not a generic upward walk, which could let an accidental copy anywhere in an unrelated
subdirectory tree claim its ancestor as "the project". `main()`'s single call site
(`root = resolve_single_project_root(ROOT)`) is the only line changed in `main()` itself.
Verified live, both copies, from this repo's own root:
```sh
$ python3 tools/methodology_dashboard.py --no-open
  METHODOLOGY — METHODOLOGY DASHBOARD  │  1 projects  │  v2.15.0
  Health: 76/100    High+ Risk: 0    Commits: 491
```
— matching the portfolio scan's own row for this repo exactly. `DASHBOARD_VERSION` 2.14.0 → 2.15.0.
6 new RED-first tests (`TestBL29SelfScanRoot`, `tools/test_methodology_dashboard.py`): each failed
with `AttributeError` pre-fix except the end-to-end reproduction, which failed by actually printing
"No projects found" — confirmed the exact reported symptom before patching it. Coverage includes a
negative control (`test_a_tools_dir_with_no_manifest_marker_is_not_bridged`): an adopter repo with
its own unrelated `tools/` directory and no `bin/_manifest.py` is NOT bridged, proving the marker
check — not just the directory name — gates the new behavior. Dashboard suite 284 → 290, all green;
full `bin/tests.sh` 185/186 unaffected (Test 9's pre-existing upstream-404 baseline). Twins verified
byte-identical after the mirror. `dashboard_history.jsonl` gained two real entries from the live
verification runs above — first time this repo's own root copy could write its own history.

**BL-33 — `bin/model-report`'s `CHANGELOG_ENTRY_RE` can't parse a multi-tag `### ` header, and
silently folds that entry into the PRECEDING one instead of dropping it loudly.**
*Raised 2026-08-11 (S79), found incidentally while re-measuring BL-20's population against the real
live ledger — not the item this session was assigned, and not fixed here (FM #17: one deliverable).
Fork-side tool only; canonical-only, not distributed.*
**The defect.** `CHANGELOG_ENTRY_RE` (`bin/model-report:50`) is
`^### (\d{4}-\d{2}-\d{2}) · \[([^\]]+)\] (.+)$` — exactly one bracketed tag, then a required space,
then the summary. `CHANGELOG.md:378`'s real header — `### 2026-08-10 · [BL-14][BL-17] Two defects in
the HANDOFFS.md receipt spec — PR opened upstream` — carries two adjacent tags with no space between
the first `]` and the second `[`, so the regex never matches. `parse_changelog_models()` never resets
`cur` on that line, so the entry gets no dict of its own: its `**Model:**` bullet, date, and summary
are silently absorbed as if they belonged to the PRECEDING entry (`### 2026-08-10 · [BL-21] …`,
2 headers up) instead. In this one instance both entries happen to carry the identical value ("Claude
Sonnet 5."), so the report's Model *value* doesn't visibly corrupt — but the **entry count** does:
this is exactly how BL-20's own re-verification found `bin/model-report` reporting **51** entries
against a raw anchored `**Model:**` grep of **52** (`grep -cE '^-?[[:space:]]*\*\*Model:\*\*'
CHANGELOG.md docs/archive/CHANGELOG-*.md` → 52 for the live file; the tool's own count is one lower).
A future ledger entry whose merged-away Model value genuinely *disagrees* with the entry it gets
folded into would misattribute silently, not just undercount.
**Population, re-derived here:** exactly **one** live occurrence
(`grep -noE '^### [0-9-]+ · \[[^]]+\](\[[^]]+\])+' CHANGELOG.md docs/archive/CHANGELOG-*.md` → only
`CHANGELOG.md:378`); none in any archive shard.
**Not fixed.** Out of scope for BL-20 (a different regex, a different failure mode — silent
misattribution vs. silent non-match), and this session's one deliverable was already BL-20. A fix
widens `CHANGELOG_ENTRY_RE` to accept one-or-more adjacent `[TAG]` groups (mirroring how the source
tag list already documents `[BL-<N>]`/`[issue #<N>]`/`[ad hoc]` as a closed set but never says only
one can appear) and should fail loudly (or at minimum count) an unparsed `### ` header rather than
silently folding it into its neighbor — a "line starts with `### ` but doesn't match" trap this tool
does not currently guard at all.

**FIXED 2026-08-11 (S80), both halves.** `CHANGELOG_ENTRY_RE` (`bin/model-report:52`) widened from
`^### (\d{4}-\d{2}-\d{2}) · \[([^\]]+)\] (.+)$` to
`^### (\d{4}-\d{2}-\d{2}) · ((?:\[[^\]]+\])+) (.+)$` — one-or-more adjacent `[TAG]` groups, captured
whole (brackets included) into `source`, so `CHANGELOG.md:378`'s `[BL-14][BL-17]` header now parses
as its own entry rather than donating its `**Model:**` bullet to its predecessor. Separately,
`parse_changelog_models()` now returns `(entries, unparsed_headers)`: any `### `-prefixed line that
still fails to match resets `cur` to `None` (so nothing after it can be misattributed to a stale
entry) and is collected with its 1-based line number; `render()` prints a `WARNING:` block naming the
file, line number, and raw text for each one, in Source 1's own output — loud, not silent, and not
merely counted. `render()`'s per-entry format string dropped its own `[%s]` wrapping (now redundant
since `source` already carries its brackets), so single-tag output is byte-identical to before the
fix; multi-tag output now prints the header's literal tag group, e.g. `[BL-14][BL-17]`.
RED-first (Learning #12): confirmed pre-fix, by direct execution against a fixture and against this
repo's own live `CHANGELOG.md`, that the multi-tag entry's Model bullet was absorbed into the
preceding entry and that no unparsed-header signal existed at all. New Test 31 in `bin/tests.sh`
fixtures a multi-tag header (must parse as its own entry), a deliberately malformed `### ` header
with no middle dot (must be reported and must not donate its bullet to either neighbor), and a valid
entry immediately after it (must still parse — proves the malformed line doesn't wedge the parser) —
8 assertions, all green.
Re-measured against this repo's own live `CHANGELOG.md`, not recalled: `bin/model-report`'s own
post-fix Source 1 count is **55**, now exactly equal to
`grep -cE '^-?[[:space:]]*\*\*Model:\*\*' CHANGELOG.md` (**55**) — the population gap BL-20's
closure note reported (51 vs. 52) is closed, and no `WARNING` fires against the real file (confirmed
by an explicit negative assertion in Test 31, not merely by the count matching). Full suite
`bash bin/tests.sh`: 197 passed / 1 failed (Test 9's pre-existing `gh api`/upstream-lag baseline,
unrelated, same failure class reported by every session since at least S75). `python3 bin/check-links`
unaffected (88 links / 22 files).

**BL-34 — `methodology_dashboard.py`'s `LANG_MAP`/`DOC_EXTS` are blind to R, Quarto, and R
Markdown, silently undercounting a real adopter's code and doc corpus.**
*Raised and FIXED same session, 2026-08-11 (S81), operator-directed — found while answering an
operator question about `../nprcgenekeepr`'s dashboard card, not from a pre-existing complaint.
DISTRIBUTED (`tools/methodology_dashboard.py` + `starter-kit/` twin), so the fix lands here AND
ships upstream; PR opened same session.*
**The defect, two independent gaps in the same three constants.** `SOURCE_EXTS` already had `.r`
(R source always counted toward Source LOC), but `LANG_MAP` had no entry for it, so R never got
its own row in the "Code by Language" card — measured against `../nprcgenekeepr`: **603** `.r`
files, **77,773** LOC (the bulk of that project's 99,482-LOC Source total), completely invisible
in `by_language`. Separately, `.qmd` (Quarto) and `.rmd` (R Markdown) were in neither
`SOURCE_EXTS` nor `DOC_EXTS`, so a file with either extension outside a `docs/` path fell through
`categorize_file`'s entire ladder to `"other"` — not source, not docs, and (per `collect_file_metrics`)
not even LOC-counted, since LOC is skipped entirely for `"other"`. Measured on the same corpus: 28
`.rmd` files at **0** counted LOC (all 28), and 11 of 12 `.qmd` files also at 0 (the 12th happened
to sit under a `docs/` path, which counts regardless of extension).
**Fix.** `.r": "R"` added to `LANG_MAP`. `.qmd`/`.rmd` added to `DOC_EXTS` (operator-specified
target — these are literate-document formats, prose with embedded code, the same bucket `.md`
already lives in, not `SOURCE_EXTS`'s). Re-measured post-fix against the same corpus: `by_language["R"]`
now reads 603/77,773 (exact match to Source's own R contribution); `by_category["docs"]` grew from
415/161,362 to 454/171,766 (+39 files, +10,404 LOC — every `.rmd`/`.qmd` file, accounted for
exactly). `DASHBOARD_VERSION` 2.15.0 → 2.15.1.
**Interaction found and handled, not assumed harmless:** adding `.qmd`/`.rmd` to `DOC_EXTS` feeds
`detect_doc_only`'s corpus disjunction (clause 4), whose own comment stated a pure-Quarto repo's
`.qmd` was "not counted as docs" — the exact reason the `render.toolchain_present` fallback arm
exists (Layer 7's `TestFrameworkInstalledExclusion.QUARTO` fixture proved that arm's real-scan
correctness in isolation). Verified before assuming: the QUARTO fixture (two ~200-line chapters)
now *also* clears `DOC_ONLY_DOC_LOC_MIN` on its own, so it stopped isolating the toolchain arm —
still green, but silently narrower coverage. Fixed the comment (now names only `.tex`, since that
stays uncounted) and added a new minimal fixture (`QUARTO_MINIMAL`, a single short chapter kept
under both corpus thresholds even with `.qmd` counted) plus a dedicated test that asserts
`doc_loc`/`doc_files` stay below threshold AND `is_doc_only` is still `True` — restoring the
toolchain-arm-in-isolation proof the original fixture could no longer carry alone.
**RED-first (Learning #12):** all 6 new/changed assertions run against the pre-fix module (via
`git stash` on just the two dashboard.py twins, tests kept) and confirmed failing — 4 hard
failures/errors, plus the 2 unaffected guard tests (the "not also a language row" negative
assertion and the toolchain-isolation regression-lock) correctly staying green throughout, since
neither is proving this fix. Post-fix: `python3 -m unittest tools.test_methodology_dashboard` —
**296 passed** (290 prior + 6 new). `bash bin/tests.sh` unaffected (197/198, Test 9's pre-existing
baseline). Twins confirmed byte-identical (`diff`) both before and after.
**PR OPENED 2026-08-11 (S81), same session, operator pre-authorized in the task assignment
itself:** built independently in an isolated `git worktree` at `upstream/main` (`a2a7275`) rather
than porting the fork's own evolved file — confirmed upstream carries the byte-identical
pre-fix `SOURCE_EXTS`/`DOC_EXTS`/`LANG_MAP`/disjunction-comment block, so the same minimal patch
applied cleanly. Comments written with no fork-only vocabulary (`BL-34`, `S81`) inside the
upstream-shipped source — the near-miss BL-31/S75 already flagged and caught once. `DASHBOARD_VERSION`
2.10.2 → 2.10.3 in the isolated worktree (upstream's own version, far behind the fork's 2.15.x —
matches the BL-31/PR #71 precedent exactly); this collides with #70 and #71, which independently
propose the same "2.10.3" for unrelated changes — a known, already-disclosed (BL-22) sequencing
risk, not new, not pre-empted here. Verified RED against a **clean, unmodified** `upstream/main`
worktree first (2 pre-existing failures, same `FRAMEWORK_INSTALLED_SOURCE`/`context_budget.py` gap
#71 already targets, confirmed unrelated to this change), then against the fix branch — 203/203
minus the identical 2 pre-existing failures, all 6 new tests green. Pushed to `origin`, opened
[KJ5HST/methodology#72](https://github.com/KJ5HST/methodology/pull/72).
Isolated worktrees removed after pushing; nothing left behind on this fork's own tree from the
upstream-targeted work.
**MERGED 2026-08-11 (S85; operator reported it, verified rather than taken on word):** `gh api
repos/KJ5HST/methodology/pulls/72` confirms `merged: true`, `merged_by: KJ5HST`, merge commit
`5c59f0b`. Independently re-verified in an isolated worktree at that exact merge commit (mirroring
the BL-26/PR #66 precedent, not trusting the commit messages alone): `python3 -m unittest
tools.test_methodology_dashboard` 208/208; `bash bin/tests.sh` 114/114 (upstream's own smaller
suite scope). Confirms both of the maintainer's review requests actually landed, not just posted —
`DASHBOARD_VERSION` reads `2.10.5` there (the resolved three-way collision), and
`test_rmd_analysis_repo_flips_doc_only_and_softens_the_test_risk` (the classification-consequence
pin) is present. **Not synced into local `main` here** — `git merge-tree` against local `main`
shows a real 4-file conflict (`CHANGELOG.md`, both `methodology_dashboard.py` twins,
`tools/test_methodology_dashboard.py`), because this item's own fix was ALSO built and landed
directly on local `main` in the same S81 session (this entry's own "Fix" section above,
`DASHBOARD_VERSION` 2.15.0 → 2.15.1) — two independent applications of the same feature against
two different base trees. Resolving that is real judgment (which side's structure to keep across
4 files), deliberately deferred to a dedicated sync rather than folded into this verification.

**SYNCED 2026-08-12 (S86; operator-directed).** Local `main` merged with `upstream/main`
(`aa378ab`), resolving this item's own conflict — which had grown to 6 files by the time the sync
ran (upstream had moved to `dcb6fc6`: issue #67's own independent fix, PR #73, plus the v3.6→v3.7
release itself, PR #74). Kept this fork's own BL-34 comments/`DASHBOARD_VERSION` (`2.15.2`)
throughout; for issue #67, kept this fork's own `--sync [DIR]` scoping design over upstream's
`cp`-based one (already covered by ~15 existing tests upstream's simpler design has no equivalent
for). Full resolution narrative: `CHANGELOG.md` "2026-08-12 · [BL-34] Local `main` synced with
`upstream/main` ...". Verified: unittest 300/300, `bin/tests.sh` 228/229 (Test 9's pre-existing gap
aside), twins byte-identical. **This item is now fully closed** — both the PR #72 merge and the
local sync are done.

**BL-35 — `starter-kit/FRAMEWORK_LEARNINGS.md` rows 18 and 19 have been malformed 2-column rows,
missing their `Source` and `When to Apply` cells, since S40/S41 (2026-08-04).**
*Raised 2026-08-11 (S83), found by `bin/check-learnings` — a tool arriving via this session's
`upstream/main` merge (issue #65) that this fork had never run against its own extracted Learnings
table before. Not fixed here (FM #17: one deliverable, and reconstructing two real learnings' Source
and When-to-Apply cells needs real editorial judgement this session should not fabricate). Content
defect only; canonical checker itself was adapted to locate and tolerate it (`bin/tests.sh` Tests
32/33 assert on this exact, disclosed shape rather than papering over it).*
**The defect.** `starter-kit/FRAMEWORK_LEARNINGS.md:40-41` — Learning rows `18` and `19` — are each
one physical line with exactly 2 pipe-delimited cells (`| 18 | <prose> |`), not the table's own
4-column shape (`# | Learning | Source | When to Apply`) every other row (1-17, 20-23) carries.
`git blame` traces both to their original authoring commits (`11b843a`, `12463dd`, both 2026-08-04,
S40/S41) — this is not a regression from this session's merge, it has been live and undetected since
those rows were written, because no structural checker for this table existed in this fork until
`bin/check-learnings` arrived just now.
**Why not fixed here.** Reconstructing the missing `Source`/`When to Apply` cells requires
correctly characterizing what session/context each learning came from and what concrete guidance it
implies — real content the original author would need to supply or confirm, not something to invent
from the prose alone. A future session (ideally the operator, or a session that can ask) should
either recover the intended cells or, if unrecoverable, decide how the row should read instead.
**Distribution note.** `FRAMEWORK_LEARNINGS.md` is `bin/_manifest.py`-TRACKED, so every adopter
already has this malformed content in their own synced copy, unnoticed for the same reason.

**FIXED 2026-08-11 (S84):** recovered both cells from the rows' own authoring commits rather than
inventing from the prose. `11b843a`'s message states "Recorded as Learning #18" and narrates the
exact defect (the ledger-doctrine seed's `--write` text claimed "leaves the change staged for you"
while the shipped tool never `git add`s and leaves the shard untracked); `12463dd`'s states
"Recorded as Learning #19" and narrates its own (`SEED_FORMAT_MARKERS` keyed on a stable H1 title,
so every pre-doctrine adopter matched as "current"). Both `Source`/`When to Apply` cells were
written from that provenance, presented to the operator for approval before writing, and approved
as drafted. `bin/check-learnings` now reports the table fully clean (22 contiguous rows, no
malformed shape); `bin/tests.sh` Tests 32/33's presence/restoration controls, pinned to the
disclosed 2-finding shape, updated to assert clean instead — full suite 228/229, the sole failure
being Test 9's pre-existing, unrelated `starter-kit/FRAMEWORK_LEARNINGS.md`/`methodology_trim.py`
github-source gap (those two files not yet merged upstream). Distributed to every adopter at their
next `bin/sync`.
