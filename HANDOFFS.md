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

**Archived 1 record(s), 2026-09-20 → 2026-09-20** into [`docs/archive/HANDOFFS-through-2026-09-20-11.md`](docs/archive/HANDOFFS-through-2026-09-20-11.md) — same format, same order, frozen.
Losslessness is proved by [`docs/archive/HANDOFFS-through-2026-09-20-11.md.verify.sh`](docs/archive/HANDOFFS-through-2026-09-20-11.md.verify.sh), which re-derives L1/L2/L3 from git; run it rather
than trusting this sentence. Written by `methodology_trim.py` v1.5.0.

```handoff
session: S210
date: 2026-09-21
status: pending
active_task: **BL-75 — P1 of [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md) §5 (D1 + D2 + D4): `--status` becomes a write-free default measurement, an unrecognised argument exits 3 with usage and touches nothing, `VERSION` 1.2.0 → 1.3.0.** Seven tests RED first against blob `b1111d92`, two `bin/tests.sh` rows, three mutants run. Branch `fix/context-budget-status` cut from `upstream/main` `6b29d3d` in a `--no-local` clone, fetched back here as a **local** branch; nothing pushed, nothing upstream-facing (P4's go-ahead). Chosen at this session's Phase 0 picker. **Side actions approved at the same picker:** the `HANDOFFS.md` retention trim this receipt makes owed (three receipts, `--cut 2 --force`) and its fold; pushing fork `main` to `origin` at close-out.
commit: pending
```

```handoff
session: S209
date: 2026-09-20
status: complete
self_score: 8
predecessor_score: 9
active_task: **BL-75 + BL-80 ARE PLANNED AS ONE UPSTREAM PR AND THE PLAN IS RATIFIED; NOTHING IS BUILT, NOTHING IS UPSTREAM-FACING. NEXT: THE PLAN'S P1.** The deliverable is [`docs/planning/context-budget-status-plan.md`](docs/planning/context-budget-status-plan.md) (`87857ba` draft, `a39cf1c` decisions). The operator took all five decisions at this session's decision picker, each as recommended: **D1 (b)** `--status` becomes a real, **write-free** default run (same ledger and exit code, no history append); **D2 (a)** unknown arguments are refused with **exit 3** (usage printed, nothing read or written; `--help` still wins); **D3 (a)** the growth-run advisory's second sentence is chosen by `worst`, the headline's own variable; **D4** `VERSION` 1.2.0 → **1.3.0** (tool constant only, no repository release); **D5** upstream's `context-budget-unit-tests` (118) and `tests-sh-passed` (139) floors are tightened in the PR. The tool is **one blob, `b1111d92`**, on fork `main`, `upstream/main` and all three open PR heads. The PR answers the maintainer's own PR #82 point 6 ([#issuecomment-5701463025](https://github.com/KJ5HST/methodology/pull/82#issuecomment-5701463025)): *"`--status` writes `.context-budget-history.jsonl` … Tracked-or-ignored gets decided first; then the gate."* **#83, #84, #85: still no maintainer response; nothing owed upstream.** Side actions, all approved at the Phase 0 picker: the `HANDOFFS.md` retention trim and its fold; §4.2 of the PR #83 review corrected (the third false "agent memory" claim); and the fork push, taken after this commit, with its record following.
what_was_done: **Phase 0:** `CHANGELOG.md` frontier = HEAD `73b9536`, gap empty; `HANDOFFS.md` frontier `1c56948`, the one commit after it being S208's announced push record. No pending stub, 2 receipts; nothing backfilled. Gate citation **re-run** in a `--no-local` clone at `73b9536`, HEAD asserted: S208's exactly. Dashboard 76/100, medium, 0 high+. Upstream 0 issues; #83/#84/#85 heads `219fb9d`/`77afc12`/`e2501c5`, 0 reviews, only our own comments. **`366dfc4`** the claim. **`adb9d8f`** the retention trim (`--cut 2 --force`, dry run first, 22,946 → 14,362 B, shard **-10**; SRF, CUT_STRADDLES_DAY, SHARD_NAME_DISAMBIGUATED and FRONTMATTER_FIELD_ABSENT reported, all expected). Its `.verify.sh` gave **L1/L2/L3 OK, exit 0** in a clone at `adb9d8f`. **`d473719`** the fold; `bash bin/tests.sh` in a clone at `d473719`: **343 / 0 / 6 skipped**. **`84c75e0`** §4.2 fixed, citing S115's receipt; §6 confirmed `cmp`-identical to `f7fc621`, so the posted comment is unaffected. **Research:** the tool's dispatch, render and history code read in full; blobs compared across five trees (the test file differs: #84 changes it). Every caller and citation grepped across fork, upstream and seven adopter clones: 122 fork `--status` (34 live, 88 archived), 12 upstream (all in the maintainer's receipts S19–S23), 1 in `mts-system`, 1 in #84's posted body, and `wsfct`'s 4 `--check`. Found the sibling `quality_ratchet.py --status`, which is read-only (`:543`). The maintainer's #82 reply verified on GitHub. Upstream's `--status` leaves an untracked history file. The upstream test count (118) measured in a clone at `6b29d3d`. **The premise was tested on a throwaway patch in a scratch clone (not committed):** `--selftest` exit 0, 122 unit tests OK, the `bin/tests.sh` `--force` grep green; `--status` wrote nothing and printed output byte-identical to the bare run after it; `--zzz`, `--force` and `--check` gave exit 3 and wrote nothing. **`87857ba`** the draft, frozen before the picker. **`a39cf1c`** the decisions recorded (status line, §3), with S209 updates under BL-75 (`docs/planning/BACKLOG-DETAIL.md:2676`) and BL-80 (`:3060`) and their index rows; `BACKLOG-DETAIL.md.verify.sh` C1–C5 OK, exit 0. **Close-out:** the plan's `wsfct` citations now name their tree. **Phase 3C:** no fork-learnings row, so D3's retirement obligation does not arise; the lesson (a phantom flag comes from a sibling tool, so match the sibling's meaning) went to agent memory.
next_steps: **(1) THE PLAN'S P1 — BL-75, THE CLI (D1 + D2 + D4), ONE SESSION** (`docs/planning/context-budget-status-plan.md:295`). Cut `fix/context-budget-status` from `upstream/main`: re-check it is still `6b29d3d`, and if it moved, re-derive §2.1/§2.5 first. Work in a `git clone --no-local`, with `git config core.hooksPath .githooks` set before the first commit. Write the seven tests in §5 P1 **RED first**, against the unchanged blob `b1111d92`, and record the failures. Then change `starter-kit/context_budget.py:1314-1333` (reject), `:1375` (skip the append under `--status`), `:1290-1311` (usage) and `:41` (`VERSION`), and add the two shell rows in upstream's budget block (`upstream:bin/tests.sh:607-689`). One upstream `CHANGELOG.md` entry per commit; at most 5 files per commit. Kill the three named mutants by running them. **(2) THEN P2** (BL-80, `:651-653`), **P3** (vet, `merge-tree` against #84/#85/#83, tighten floors, PR body for the operator's review), **P4** (open: outward, needs a go-ahead on the exact body AND on pushing the branch to `origin`) and **P5** (fork-side adoption), each its own session. **(3) AT PHASE 0, CHECK #83/#84/#85 FOR A MAINTAINER RESPONSE**, with the same commands as S208: #83 1 comment (ours, `5755256040`), head `219fb9d`; #84 1 comment (ours), head `77afc12`; #85 0 comments, head `e2501c5`. A reply is new work with its own go-ahead. **(4) THE NEXT CLAIM MAKES THREE `HANDOFFS.md` RECEIPTS**: trim (`--cut 2 --force`) right after its Phase 0 report; this has held nine times. **(5) NO `CHANGELOG.md` TRIM OWED:** about 92 KB after this close-out, roughly 104 KB under the 196,608 B trigger (an estimate, at about 9–11 KB per session). **(6) STILL OWED, UNCHANGED:** BL-78's closing edits as their own session (`docs/planning/BACKLOG.md:166`, the archive move, `.context-budget.json:101` `files[4]._`); BL-81, BL-79, BL-77, BL-74 undecided. **CARRIED:** S206's list.
key_files: `docs/planning/context-budget-status-plan.md` (the deliverable): status `:4`, §2.3 callers `:131`, §3 decisions `:202`, §4.1 interface contract `:260`, §5 P1 `:295`, P2 `:326`, P3 `:339`, P4 `:357`, P5 `:367`, §6 `:382`, §7 `:394`. The code (blob `b1111d92`, lines valid in every tree): `starter-kit/context_budget.py` dispatch `:1314-1333`, append `:1375`, usage `:1290-1311`, advisory `:651-653`, `worst` `:584-596`, the selftest `--force` guard `:1282-1283`, the installed hook `:964`. Guards: `upstream:bin/tests.sh:622` (fork `:1971`) and `tools/test_context_budget.py:485-487`. The new tests go after `TestToolInvariants` (`upstream:tools/test_context_budget.py:476-489`), clear of #84's `:1231-1279`. The dashboard fingerprint is `upstream:starter-kit/methodology_dashboard.py:500-508`; the sibling is `starter-kit/quality_ratchet.py:543`; the maintainer's reply is fork copy `docs/planning/pr82-maintainer-reply.md:17`. Backlog: `docs/planning/BACKLOG-DETAIL.md:2676` (BL-75) and `:3060` (BL-80); index `docs/planning/BACKLOG.md:164`, `:168`. Also `docs/planning/pr83-decisions-review.md:194` (§4.2, fixed) and `docs/HANDOFFS_ARCHIVE_INDEX.md` (last row = shard **-10**).
gotchas: **(1) FOUR FLAGS RUN THE SAME MEASUREMENT TODAY.** `--status`, `--check`, `--force` and any typo all exit 2 by verdict and append a history row when a size changed. In P1, compare `--status` with the bare run by running `--status` FIRST: the append advances the growth counter (fork Learning #88's instrument delta). **(2) THE `--force` STRING IS GUARDED THREE TIMES BY SOURCE-GREP** (§2.2): the accepted-argument literal and every message must not contain `--force` before `def selftest`. The tests may say it; the tool may not. **(3) THE DASHBOARD FINGERPRINTS THE TOOL** on the docstring's *"context_budget.py — size budgets"*, `CONFIG_NAME`, `HISTORY_NAME` and `growth_run`, with at least 2 required; do not rename them. **(4) ADOPTER CLONES MOVE UNDER YOU:** a parallel `wsfct` session committed `ef3eade3` mid-session, moving its `--check` instruction from `SESSION_NOTES.md:797` to `:847`. Name the head beside every adopter line. **(5) THE GROWTH COUNTER READS +1 ON EVERY RUN AFTER THE FIRST ON AN UNCHANGED TREE** (168, then 169 held). Out of scope and not a backlog item (§7); offer it as one if wanted. **(6) zsh:** `"$r:path"` (the `:s` modifier) bit again, as did an empty derived `$n` in `sed -n "${n},…p"`. **(7) `bin/check-handoff` READS EACH FIELD AS ONE LINE:** a multi-line `key_files` failed the structure check at this close-out; keep every value on its line. **(8) `HANDOFFS.md`'s front matter still says `--cut 1 --force`**, now wrong through nine trims. **`CHANGELOG.md` HAS NO FOLD.**
runtime_smoke: **NO APPLICATION. THE BUILD-EQUIVALENT IS `starter-kit/quality_ratchet.py --run` IN A `--no-local` CLONE WITH HEAD ASSERTED BY SHA.** **Citation, clone of `a39cf1c`: `quality_ratchet: 11/11 pass · 0 fail · 0 unmeasured · results 10575dac7361 · manifest 01a4ae7aa511`.** `tests-sh-passed` is **343** at two receipts, the floor; the digests match Phase 0's re-run at `73b9536`, since no gate moved. Also green: `bash bin/tests.sh` **343 / 0 / 6 skipped** in a clone at `d473719`, after the trim; the trim's `.verify.sh` **OK, exit 0** in a clone at `adb9d8f`; `BACKLOG-DETAIL.md.verify.sh` **C1–C5 OK, exit 0**; `bin/check-links` **111 links / 23 files**, exit 0. **NOT EXERCISED:** this close-out commit itself (BL-64); the plan's design beyond the throwaway patch (no full `bin/tests.sh` with it, no synced adopter, not the not-over, run-hit advisory branch), which P1–P3 own.
changelog_ref: CHANGELOG.md "2026-09-20 · [BL-75] S209 claim", the `HANDOFFS.md` trim (written by the trimmer), "[ad hoc] S209 — `HANDOFFS.md`: the trim's pointer block folded into the shard index", "[ad hoc] S209 — the PR #83 review's third false 'agent memory' claim corrected (§4.2)", "[BL-75] S209 — plan drafted", "2026-09-21 · [BL-75] S209 — the plan's five decisions taken by the operator", and this close-out
commit: 366dfc4 (claim) + adb9d8f (HANDOFFS trim) + d473719 (fold) + 84c75e0 (§4.2) + 87857ba (draft plan) + a39cf1c (decisions) + this close-out
```

