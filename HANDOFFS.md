# Handoff Receipts — durable close-out proof

This repository dogfoods its own methodology: every session records a durable, machine-checkable
`handoff` receipt here at close-out (Phase 3D), and Phase 0 reconciles it against `git log`. See
[`starter-kit/HANDOFFS.md`](starter-kit/HANDOFFS.md) for the block format and the write points, and
`bin/check-handoff` for the checker. Newest on top; prepend-only.

**Retention policy — keep ONE receipt, trim above TWO.** Everything older is archived under
`docs/archive/` and indexed in [`docs/HANDOFFS_ARCHIVE_INDEX.md`](docs/HANDOFFS_ARCHIVE_INDEX.md). **N=1 is an operator decision (2026-09-16, S172)
replacing S127's N=4**, taken against BL-59's measurement of what actually reads this file: the
handoff is done by the newest receipt alone. **Depth and trigger are separate on purpose:**
every trim pays a FIXED ~16 KB proof, so the trigger sits one above the depth (BL-60). **`methodology_trim.py` fires on BYTES (196,608 B),
never on a record count**, so the policy is applied by the session that notices: Phase 0 runs
`grep -c '^```handoff' HANDOFFS.md` and reports the count; **above 2**, the trim is its own action after
that report, never inside Phase 0, which is read-only apart from the reconcile backfill
(`starter-kit/SESSION_RUNNER.md` Phase 0): `--cut 1 --force`. The force is
warranted, not an override — `SRF_RED` refuses every on-schedule retention trim by construction
(BL-59). `bin/check-handoff` validates the 13-key schema on the **newest** receipt; `--all` checks
every receipt and `--archived` a frozen shard. Below three receipts Test 34 prints six named `SKIP` rows — stated, never silent.

**Two session sequences share this ledger and their numbers collide.** This fork and
`upstream/main` each run their own `S<N>` counter, so a receipt is identified by **session + date**,
never by number alone. **Every upstream receipt is now archived**; every receipt retained here is
the fork's. At a resync the two sequences stay separate and unrenumbered, each incoming receipt is
checked against ours before it is kept, and within a shared date the fork's precede the arriving
upstream ones (precedent: `fc4d297`).

> **THE HAND-MAINTAINED RECEIPT COUNT IS GONE, DELIBERATELY.** S172's rewrite dropped *"This file
> currently holds **N**"* — the number [Learning #12](starter-kit/FRAMEWORK_LEARNINGS.md) and upstream
> [issue #65](https://github.com/KJ5HST/methodology/issues/65) both cite as always wrong by the next
> close-out. The trimmer still declares it, so **every trim now reports `FRONTMATTER_FIELD_ABSENT`**:
> stated, expected, not a failure. Removing the declaration is distributed — its own go-ahead (BL-60).
> **Count with `grep -c '^```handoff' HANDOFFS.md`.**

> **⚠ THREE is the floor the retention policy sits one above.** `bin/tests.sh` Test 34 mutates *this*
> ledger to check `check-handoff --all`'s whole-ledger invariants, reading two anchors from the live
> file — not hardcoded, so it survives *which* receipts rotate, but it needs three to exist. A short
> ledger is **stated rather than silent** (BL-40 (b)): below the floor those six assertions print as
> `SKIP` rows naming themselves, the summary carries a skip count, and a ledger with *zero* receipts
> still FAILS — corruption is not rotation. **Nothing prevents a cut below three; the policy is what
> makes it not happen.** Re-run `bash bin/tests.sh` after any trim of this file.

**The shard index is not in this front matter, on purpose.** It lived here until S174 and grew a row
with every trim against the fixed 7,168 B header reserve (Test 39 A2), so it moved out rather than the
reserve rising. A trim commit still carries the trimmer's ~448 B pointer block; the fold removes it, so a
trim-and-fold no longer grows this front matter. The fold rule is in the index.

<!-- NEXT TRIMMING SESSION: methodology_trim.py appends a 3-line pointer block here
     (starter-kit/methodology_trim.py:1093 build_pointer_block, :1103 insert_pointer). Fold it into
     docs/HANDOFFS_ARCHIVE_INDEX.md as one row and delete the block, IN ITS OWN COMMIT: inside the
     trim commit the shipped .verify.sh fails L2 (fork Learning #58). -->

```handoff
session: S208
date: 2026-09-20
status: pending
active_task: **BL-82 — post §6 of `docs/planning/pr83-decisions-review.md` to upstream PR #83 as one comment, and read it back.** Chosen at this session's Phase 0 picker, with one sentence added first (the trim case was run on `HANDOFFS.md` only) and the final text shown to the operator before posting. **Side actions approved at the same picker, each its own commit:** the `HANDOFFS.md` retention trim this receipt makes owed (three receipts, `--cut 2 --force`); a scoped `CHANGELOG.md` trim, dry run first; correcting §4.1's false *"only in agent memory"* (`docs/planning/pr83-decisions-review.md:180`; S44's receipt records it at `docs/archive/HANDOFFS-through-2026-08-09.md:411`); and pushing fork `main` to `origin`.
commit: pending
```

```handoff
session: S207
date: 2026-09-20
status: complete
self_score: 8
predecessor_score: 8
active_task: **BL-82's §6 IS REWRITTEN (`1259287`) AND WAITS ON THE OPERATOR'S REVIEW. NOTHING IS POSTED.** The deliverable is a recomposed §6 (*"Proposed comment for #83"*) of `docs/planning/pr83-decisions-review.md`, written against the three defects the operator named at this session's picker: **too dense, undefined terms, poor structure.** The comment now opens in two sentences. **Part 1** is the one change (leave `HANDOFFS.md` out of `merge=union`), with *what goes wrong*, *why* and *how I checked* as separate short paragraphs, the repro's four cases as a table, and four consequences for the plan. **Part 2** is one note per §8 item (2, 4, 5, 7, 10, 11, 12), each named by its number and subject. A closing line covers items 1, 3, 6, 8 and 9. **No bare plan code remains in the comment text.** The old text carried ten (D1, D2, D4, D5, D6, D8, D11, D14, "FM", "Shape B"), while its preface certified only *"no session numbers or backlog codes"*. **Cost, stated:** about 1,075 words pasted, against 523. **BL-82 is open on one step:** posting to #83, which is outward and needs its own go-ahead on the exact text.
what_was_done: **Phase 0:** both ledger frontiers = HEAD `8f5bbb7`, gaps empty, no pending stub, 2 receipts; nothing backfilled. Gate citation **re-run, not read**, in a `--no-local` clone at `8f5bbb7`: S206's citation exactly. Dashboard 76/100, medium, 0 high+. Upstream 0 open issues; #83 still `219fb9d`, 0 comments, 0 reviews; #84's one comment is the fork's own check-in, already in the ledger; #85 unchanged. **`555bbce`** claim. **`003a243`** the owed retention trim (`--cut 2 --force`, dry run first, 24,443 → 15,670 B; SRF / CUT_STRADDLES_DAY / SHARD_NAME_DISAMBIGUATED (-8) / FRONTMATTER_FIELD_ABSENT, all expected). Its `.verify.sh` printed L1/L2/L3 OK, **bare exit 0**, against `003a243` in a `--no-local` clone. **`7f77925`** the fold. `bash bin/tests.sh` after the trim: **343 passed, 0 failed, 6 skipped**. **Research:** the plan's §3A, §4 (union, identity, merge-receipt, worker, manifest and failure-mode decisions), its alternatives table, Phase 1 and §8, read at `219fb9d`. The repro re-run (exit 0, output identical to S206's), and the fused block read line by line to describe it. Upstream has no `.github/` at `6b29d3d` or `219fb9d`, so *"GitHub's merge button runs no checker"* holds. **Drafting:** in the scratchpad first, so the running suite saw no change. First pass 1,269 words, cut to 1,075 pasted. The comment, extracted with its `>` markers stripped, renders under `pandoc -f gfm`: one table of 5 rows, both triple-backtick code spans intact. **`1259287`** the deliverable, plus BL-82's index row (`docs/planning/BACKLOG.md:170`) and an S207 update (`docs/planning/BACKLOG-DETAIL.md:3144`); `BACKLOG-DETAIL.md.verify.sh` C1–C5 OK. **Phase 3C:** no fork-learnings row. The lesson is an operator preference for outward text, recorded in agent memory (`feedback_outward_text_uses_recognized_terms.md`), so D3's retirement obligation does not arise.
next_steps: **(1) DONE AFTER CLOSE-OUT: THE OPERATOR REVIEWED THE NEW §6** (`docs/planning/pr83-decisions-review.md:278`–`:368`) and wrote *"Those look fine"*. That is approval of the text, **not** a go-ahead to post; whether it also covers the two considerations in step (2) is not settled by those words, so put both on the posting picker. **(2) ONLY THEN, POSTING TO #83**, which is outward and needs its own go-ahead on the exact text. The pre-checks are S206's and still hold: `gh pr view 83 -R KJ5HST/methodology --json headRefOid,comments,reviews`; if the head is no longer `219fb9d` or anyone has commented, re-derive §5 and §1(d) first. Extract the paste-ready text with `awk '/^> Thanks/,/^> above theirs/' docs/planning/pr83-decisions-review.md | sed -E 's/^> ?//'`, post it as one comment, and read it back. BL-82 closes after that. **Decide with the operator before posting:** the comment recommends keeping union for `CHANGELOG.md`, but the trim-against-prepend case (table row 4) was run on `HANDOFFS.md` only. A `CHANGELOG.md` trim merged against a prepend under union is **untested**. Either test it first (a new measurement, so its own scope) or post with that stated. **(3) FORK PUSH NOT TAKEN:** local `main` is 6 ahead of `origin/main` (`8f5bbb7` plus this session's five) because no go-ahead was given this session. Posting does not depend on it, since the comment links `c3a096b`, which is already public. **(4) `CHANGELOG.md` WAS 172,079 B BEFORE THIS CLOSE-OUT'S ENTRIES**, 24,529 B under the 196,608 B trigger. At S206's ~9 KB per session that is about two sessions away, an estimate from one rate. Put a scoped trim on the next picker (S203's recipe, `--cut <date> --force`, dry run first). **(5) THE NEXT CLAIM MAKES THREE `HANDOFFS.md` RECEIPTS**, so the retention trim (`--cut 2 --force`) falls due right after its Phase 0 report. The prediction has held seven times. **(6) BL-78'S CLOSING EDITS ARE THEIR OWN SESSION:** the index row at `docs/planning/BACKLOG.md:166`, the archive move, and `.context-budget.json:101` (`files[4]._`), whose *"every commit that grows it is refused"* describes a refusal nothing calls. **(7) BL-81, BL-80, BL-79, BL-77, BL-74 AND BL-75 REMAIN UNDECIDED.** **CARRIED:** S206's list, unchanged.
key_files: `docs/planning/pr83-decisions-review.md` — §6 `:278` (its preface `:280`), part 1 `:289`, *what goes wrong* `:296`, *why* `:302`, *how I checked* `:308`, the table `:314`, *what this changes* `:321`, part 2 `:334`, the closing line `:367`, §7 `:372`; §0–§5 unchanged. `docs/planning/BACKLOG.md:170` (BL-82's row) and `:166` (BL-78's stale row, owed). `docs/planning/BACKLOG-DETAIL.md:3144` (BL-82's S207 update, at the file's end). `docs/planning/pr83-union-repro.py` (unchanged; `report_trim` `:177` is the only trim case, and it is `HANDOFFS.md`-shaped). `docs/HANDOFFS_ARCHIVE_INDEX.md` (last row = shard **-8**). The plan itself: `git show 219fb9d:docs/planning/parallel-sessions-plan.md`, §3A `:74`, union `:154`, alternatives `:254` (per-session receipt files `:259`), Phase 1 `:300`, §8 `:414`.
gotchas: **(1) `git fetch --all --prune` DELETES `refs/remotes/upstream/pr83`** (and `pr84`, `pr85`). Those refs were fetched with an explicit refspec, not configured, so prune removes them. The object `219fb9d` survives until gc, which is why the repro still ran. If it is gone: `git fetch upstream refs/pull/83/head:refs/remotes/upstream/pr83`. **(2) THE COMMENT'S CARRIED FIGURES WERE NOT RE-DERIVED:** 17 against 71 tokens of headroom, ~29 API calls per Test 9 run, `56997af`, and "over 200 sessions" come from S206's review. Only the repro and the no-CI claim were re-checked. **(3) ITEM 10'S FIRST EXAMPLE, a review agent writing into `starter-kit/CHANGELOG.md`, rests on evidence found only in agent memory** (S206 gotcha (4), carried). **(4) A CODE SPAN HOLDING TRIPLE BACKTICKS (` ```handoff `) RENDERS CORRECTLY IN GFM**, checked with pandoc. A line *starting* with three backticks inside the comment would open a code block; none does. **(5) `methodology_trim.py` TAKES `--file PATH`, NOT A POSITIONAL PATH.** A dry run needs `--force` too, and `--cut N` retains N. **(6) zsh: an unquoted `echo =====` FAILS** (*"==== not found"*); it bit at Phase 0 again. **(7) `HANDOFFS.md`'s front matter still says `--cut 1 --force`,** wrong through seven trims now. **(8) `CHANGELOG.md` HAS NO FOLD.**
runtime_smoke: **NO APPLICATION; THE BUILD-EQUIVALENT IS `starter-kit/quality_ratchet.py --run` IN A `--no-local` CLONE WITH HEAD ASSERTED BY SHA.** **Citation, clone of `1259287`: `quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results 10575dac7361 · manifest 01a4ae7aa511`**. `tests-sh-passed` is **343 / 0 failed** at two receipts, exactly on the floor; the digests are identical to Phase 0's re-run at `8f5bbb7`, since no gate moved. Also green: `bash bin/tests.sh` **343 / 0 / 6 skipped** after the trim; `docs/archive/HANDOFFS-through-2026-09-20-8.md.verify.sh` **L1/L2/L3 OK, bare exit 0** against `003a243`, in a clone; `docs/planning/BACKLOG-DETAIL.md.verify.sh` **C1–C5 OK**; `bin/check-links` **111 links / 23 files**; `python3 docs/planning/pr83-union-repro.py` exit 0, output identical to S206's; the extracted comment renders under `pandoc -f gfm` (one table of 5 rows, both triple-backtick code spans intact). **NOT EXERCISED:** this close-out commit itself (BL-64); GitHub's own rendering of the comment; GitHub's handling of `merge=union`; a `CHANGELOG.md` trim merged against a prepend under union.
changelog_ref: CHANGELOG.md "2026-09-20 · [BL-82] S207 claim", the `HANDOFFS.md` trim (written by the trimmer), "[ad hoc] S207 — `HANDOFFS.md`: the trim's pointer block folded into the shard index", "[BL-82] S207 — §6 of the PR #83 review recomposed for readability (not posted)", and this close-out
commit: 555bbce (claim) + 003a243 (HANDOFFS trim) + 7f77925 (fold) + 1259287 (the deliverable) + this close-out
```

