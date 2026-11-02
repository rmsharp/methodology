# Triage of upstream issues #100 and #101 (S410, 2026-11-01)

**Status: a fork-only record. Nothing was sent to `KJ5HST/methodology`; no gate, hook, test or distributed file was changed.**
It answers one question for each issue: *is what it says true, here as well as upstream, and what would acting on it touch?*

## Words used here

- **upstream** is the repository `KJ5HST/methodology`; **the fork** is this clone (remote `origin`).
- **v4.2** is the release the issues cite (`f34769f`); **main** is `upstream/main` as read on 2026-11-01 (`d50ce290`).
- **a gate** is a threshold declared in `.quality-gates.json`; **the ratchet** (`quality_ratchet.py`) refuses a commit that loosens or removes one.
- **the Disclosure Hook** is `.githooks/commit-msg` plus the "Disclosure Hook" section of `starter-kit/SAFEGUARDS.md` plus the gate `commit-msg-selftest`.
- Every `[id]` below is a line of [`issue100-101-evidence/triage-evidence-output.txt`](issue100-101-evidence/triage-evidence-output.txt), produced by [`triage-evidence.py`](issue100-101-evidence/triage-evidence.py) (read-only, standard library only; `python3 -I docs/planning/issue100-101-evidence/triage-evidence.py`). It reads git objects at three refs, so a later change to the fork's files can move a "fork" line number without making the script wrong.

## Result in one paragraph

Both issues were opened by the maintainer on 2026-11-01 (#100 at 00:05 UTC, #101 at 00:22 UTC), after the last time a session read upstream, and no backlog row mentions either. **Every line citation in both was re-derived and none is false.** At v4.2 all of them hold; on main they hold except the trimmer's lines (which #100 says move) and one `FRAMEWORK_APPARATUS.md` line (535 to 552, immaterial) [100-4e]. On the fork fifteen of the same lines sit at different numbers because the fork's files are longer; the text is the same. **All six findings of #100 hold on the fork as well as on main**, and two of its three "smaller points" do too; the third (the dashboard's only size risk) is already answered on the fork by the rows PR #99 (d) adds. **#101's central claim, that nothing in the tests or other hooks depends on the hook, holds on main and holds in code on the fork**, but the fork has six prose or tool references to the hook or its trailer that the issue could not know about (below). Nothing here is urgent: neither issue changes any gate result.

## #101 — remove the Disclosure Hook

**What it asks.** Delete `.githooks/commit-msg` (78 lines), the "Disclosure Hook" section of `starter-kit/SAFEGUARDS.md` (lines 184 to 187) and the gate `commit-msg-selftest`. Its reasons: a `Co-Authored-By` trailer is credit, not disclosure (GitHub reads it as a co-author); the rule reaches every adopter through `SAFEGUARDS.md`, which says it wins over other guidance; failure mode #16 does not ask for a trailer; a project that wants disclosure can say so itself.

**Citations re-derived.**

| Claim in the issue | v4.2 | main | fork |
|---|---|---|---|
| `SAFEGUARDS.md:3` "this file wins" | holds | holds | holds [101-a] |
| `SAFEGUARDS.md:184-187` section and trailer rule | holds | holds | holds [101-b] |
| `.quality-gates.json:80-86` the gate | holds | holds | **moved to 173** (the fork declares more gates) [101-c] |
| hook is 78 lines | holds | holds | holds [101-d] |
| hook header calls itself "the honesty counterpart of failure mode #16" | holds | holds | holds [101-e] |
| FM #16 (`SESSION_RUNNER.md:322`) says nothing about a trailer | holds | holds | holds, at line 325 [101-f, 101-g] |
| `CLAUDE_TEMPLATE.md:51` "base files govern unless explicitly overridden" | holds | holds | moved to 54 [101-h] |
| `BOOTSTRAP.md:327` and `quality_ratchet.py`: removing a gate is refused | holds | holds | moved to 345; refusal holds [101-i, 101-j] |
| `FRAMEWORK_APPARATUS.md:433-436`, `starter-kit/HANDOFFS.md:44-46` mention trailers and `bin/model-report` | holds | holds | holds [101-k, 101-l] |
| `bin/model-report` "is not in the tree" | true | true | **false for the fork: it is present** [101-m] |
| nothing in `bin/tests.sh`, `bin/_manifest.py` or the other hook names the hook | zero | zero | zero [101-n] |

**What else on the fork names the hook or the trailer** (the issue's "nothing depends on it" is about code and is right; items 1 to 6 are references it could not see, and item 7 is a fact about the history). The search excluded archives, ledgers and run-output evidence; 14 files name the hook and 14 name the trailer [evidence, second block].

1. **A declared gate to remove, and a second gate's text that cites it.** `.quality-gates.json:173-178` is the gate; line 184, the `why` of `pre-commit-selftest`, says it is built "on the commit-msg-selftest precedent beside it". Removing a gate is a loosening: `SAFEGUARDS.md:55` makes that a plan-mode decision and the ratchet refuses it. Editing any text in the manifest also changes its hash, which every receipt's gate citation quotes.
2. **Fork Learning #67** (`docs/FORK_LEARNINGS.md:85`) is about this hook's arrival at the S175 resync. If the hook goes, the row's subject no longer exists, which is retirement criterion (c) of the retirement rule in `CLAUDE.md`. I did **not** adjudicate it: that needs the row read against the criterion (basis: `fork-learnings-adjudication-2026-09-20.md` §5).
3. **`bin/model-report`** (fork only, 35 KB) has a "CORROBORATION-ONLY" section that reads `Co-Authored-By` trailers (`:24`, `:626-644`), and `bin/tests.sh:706` asserts that section handles a real trailer. With the hook gone, trailers become optional, so the section would thin over time; nothing breaks.
4. **`bin/migrate-layout --trailer`** (`:1439`) and 5 test lines in `tools/test_migrate_layout.py` (`:1209-1224`, `:2723-2730`) pass a `Co-Authored-By` line through to the commit the tool makes. They work with or without the hook.
5. **Two frozen evidence scripts** set `METHODOLOGY_REQUIRE_COAUTHOR=0` (`docs/planning/methodology-subdirectory-evidence/hook-after-move.sh:15`, `p8-rehearsal.sh:22`). Harmless afterwards.
6. **Plans and the backlog** use the hook as a precedent (`BACKLOG-DETAIL.md:2883`, `:2908`, `:2931`; `upstream-resync-2026-09-plan.md`, 8 mentions). Prose only.
7. **The history already carries the trailer:** 2,005 of the 2,006 commits since the S176 fix (`8c35872`) have one; the one that does not is the merge of upstream PR #82 (`64f23bf6`). Nothing needs rewriting either way.

**Until he decides**, the fork's hook is live, so the commits of every session keep the trailer; that is the status quo, not a position on #101.

**Options (none started; each outward act is his go-ahead).**
(a) *Wait.* Upstream decides first; the fork takes the removal at its next resync, as its own plan-mode decision, because removing a gate is a loosening. Costs nothing now.
(b) *Take it on the fork now*, in a plan-mode session: the hook, the section, the gate, the `why` text, and the adjudication of Learning #67. The `SAFEGUARDS.md` hunk is a distributed file, so it also joins the fork's held upstream-facing hunks listed in BL-46's index row. I see no gain over (a): it would only make the fork differ from main before main has decided.
(c) *Tell the maintainer the fork-side facts above* (items 1 to 7) as a comment on #101. Outward; I do not propose it.
**I recommend (a).**

## #100 — an adopter three months behind

**What it is.** Six findings and three "smaller points" from an adopter project that ran 93 sessions on v3.5 and found that the size guards of v3.6 to v4.2 never reached it. Each finding ends in a proposal. Facts about that project (93 sessions, a 154,279 B `CLAUDE.md`, 79 receipts across 50 transcripts, 56 denied commands out of 11,631, and so on) are its own and **I did not and cannot verify them**; I re-derived only what is in this repository.

| # | Finding | Holds on main / on the fork | Already tracked? | What acting on it would touch |
|---|---|---|---|---|
| 1 | `bin/status` in local mode compares against the checkout's own history and never asks the remote; the budget's `synced` check reads `../methodology/` the same way | holds / holds [100-1a, 100-1b]. The fork's `bin/status` does mention `fetch --unshallow`, but only in a hint for a shallow clone | no | `bin/status` (canonical-only; the fix adds a call to the remote) and the `synced` check in `starter-kit/context_budget.py` (distributed) |
| 2 | No protocol step runs `context_budget.py`; failure mode #28's countermeasure names no tool | holds / holds. None of the six session-read documents or `workstreams/` names the tool in any spelling, 14 files searched [100-2d]; `install-hook` is opt-in [100-2b] | no. PR #99 (d) adds dashboard risk rows, which the issue itself calls "another route" | `SESSION_RUNNER.md` Phase 0 step 5 and close-out, `BOOTSTRAP.md` Step 10. The runner is the entry point and is read in full at Phase 0, so each added line adds to the read-set the budget measures as a whole: measure before proposing |
| 3 | The only resident instruction to move Learnings out of `CLAUDE.md` is an HTML comment, which Claude Code strips; the file is called `PROJECT_LEARNINGS.md` in `BOOTSTRAP.md` and `LEARNINGS.md` in the budget seed | holds / holds, at `CLAUDE_TEMPLATE.md:84-86` on the fork [100-3a to 100-3e] | no. BL-105 edited the same comment (it added "beside `FRAMEWORK_LEARNINGS.md`") and left it a comment | `CLAUDE_TEMPLATE.md`, `BOOTSTRAP.md`, `context-budget.json` (the seed), `SESSION_RUNNER.md` 3C. **For the name:** the fork's move tooling already uses `PROJECT_LEARNINGS.md` (`bin/migrate-layout` 2 mentions, `tools/test_migrate_layout.py` 37), so making the seed agree is an edit to the seed, not to the tools |
| 4 | Is `SESSION_NOTES.md` transient or does it accumulate? Every step only adds; the prose says "overwritten"; the seed's last line says "history accumulates below this line". The adopter chose *transient* | holds / holds; on the fork the footer is at `SESSION_NOTES.md:31` [100-4a to 100-4g] | **partly: it is the question PR #98 asks** ("Underneath: is `SESSION_NOTES.md` transient, or does it accumulate?", body lines 59 to 64) | the seed, the runner's 3D, and PR #98's first commit |
| 5 | No rule for work after the 3G STOP; follow-on sessions skipped Phase 0 and wrote no stub, so a stop hook keyed on a pending receipt has nothing to fire on | holds / holds. The runner has the 3G heading and no sentence about a new task after it, 1 file searched, zero hits [100-5a, 100-5b] | no. PR #96 (`close_out_report.py`, with its hook) is the nearest, and is CONFLICTING | one runner sentence ("a new task after STOP is a new session") and a hook recipe in `SAFEGUARDS.md:175` |
| 6 | An adopter whose seeds are untracked gets no commit-keyed guard: the trimmer refuses with `P1_NO_LEDGER`, `SRF_UNDEFINED` follows a trim, the budget pre-commit check never fires, Phase 0's reconcile frontier is empty | the code sites hold / hold: the refusal is at `methodology_trim.py:1640` (v4.2), `:2131` (main), `:2100` (fork) [100-6a, 100-6b]; I did not run the trimmer on an untracked ledger | no | `bin/sync` and `bin/status` warnings (canonical-only) and the trimmer's refusal wording (distributed) |
| s1 | The trimmer writes ledgers and shards with mode 0600 (`mkstemp` then `os.replace`, chmod only for `.verify.sh`) | holds / holds [100-s1]. **Measured on the fork's own tree: 152 of 462 files in `docs/archive/` are mode 0600**, 81 are 0644, 229 are 0755 | no | one line in `methodology_trim.py` (distributed). Git records only the executable bit, so the mode is invisible in a commit and absent from a fresh clone: it is a property of the tree the trimmer ran in |
| s2 | Every `HANDOFFS.md` trim warns `FRONTMATTER_FIELD_ABSENT` | holds / holds [100-s2] | **yes: BL-60** (`BACKLOG-DETAIL.md:1249`, raised 2026-08-26 from an adopter) and this fork's `HANDOFFS.md` front matter calls it "stated, expected" | removing the declaration is distributed and is its own go-ahead (BL-60) |
| s3 | The dashboard's only size risk names a vendored header | true on main (one row, "Large files detected") / **answered on the fork**: the fork's dashboard has 3 matching lines ("... lines) — past ...") that main lacks [100-s3a, 100-s3b]; PR #99 (d) describes five new risk rows, and I did not match them one to one | **yes: PR #99 (d)** | nothing further |

*"Holds" means the cited text or code is where the issue says and says what it says. I ran none of the proposals and reproduced no behaviour except the file-mode count in s1.*

**Where #100 meets the open pull requests** (#98, #99 and #96 each have 0 comments and 0 reviews at the time of reading; #95 is an issue with one comment, mine):
- **#98.** Finding 4 says "We chose transient" and that this "makes #98's commit 1 unnecessary for projects that follow it". #98's own body says that if the file is transient, "Commit 1 would not merge". That is the nearest thing to an answer on #98, and it is in an issue, not on the pull request. **It is his to see and decide; I answer nothing.**
- **#99.** Finding 2 names (d) as a related route, so the issue shows the maintainer has read #99's description.
- **#96.** Finding 5 names it, and notes its re-fire after a close-out is keyed on a later commit, which an untracked-ledger adopter never makes (finding 6).
- **#95.** Finding 4's last line says #95 covers the seed tripping its own budget.

## What this record does not do

- It does not reply on #100 or #101, comment on #95 to #99, push a branch, or open anything. Each is his go-ahead.
- It does not remove or loosen any gate and does not touch a distributed file. Every proposal above is a candidate, and a prototype was built for none of them, so **no proposal is shown to work**.
- It does not check the adopter project's own facts (see above).

## Expectations written before the research, and what happened

Written in the scratchpad before any search: **E1** (the issues' cites hold on main, move on the fork's gate lines) held. **E2** ("some fork test depends on the hook") was **wrong in code**: zero, as the issue says; the dependences are prose and tools. **E3, E4, E6, E7, E9** held (E7 on the fork's real files: 152 at 0600). **E5** held in part (the lines moved; the comment is still a comment). **E8** held (BL-60). **E10** held: findings 1, 2, 3, 5, 6 and the mode point have no backlog row.

## What this triage adds to the backlog

Two rows, added in the next commit: **BL-129** (the Disclosure Hook, #101: options (a) to (c) above) and **BL-130** (#100: findings 1 to 6 and the mode point as candidates for the next upstream-facing batch, with the table above as its body).
