# PR3 re-run on the rebuilt candidate, the adopter-impact table: the record (S396, 2026-10-29)

Row PR3 of `docs/planning/upstream-pr-composition-plan.md` section 5 (line 181), re-run as the PR2b row asks (line 180): `bin/status` and
`bin/sync` from the candidate over the 12 adopters in `--no-local` clones, files written, files refused, seeds untouched, and two legacy
fixtures synced by upstream's tool and by the candidate's, trees diffed. Local only; nothing is sent to `KJ5HST/methodology`. The tables are
[`pr3b-adopters-output.md`](pr3b-adopters-output.md) (the script's own report, 267 s), the data [`pr3b-rows.json`](pr3b-rows.json), the script
[`pr3b-adopters.py`](pr3b-adopters.py) (S326's `pr3-adopters.py` with the candidate ref, the output names and the report's heading changed, nothing
else: `diff pr3-adopters.py pr3b-adopters.py`). The candidate is the local ref `pr2b/candidate` at `47637be2` (33 commits on `upstream/main`
`d50ce290`); upstream's tool is `upstream/main` at `d50ce290`. The baseline is S326's [`pr3-record.md`](pr3-record.md): candidate `ced2c823` on `f34769f3`.

## 1. The answer

| Adopter (layout at its HEAD) | Candidate's plain `bin/sync` | Refused: fork version / edit | A forced sync wrote | Seeds changed / created | Next plain sync |
|---|---|---|---:|---|---|
| `model_project_constructor`, `feedback-loop-comparison`, `airqino`, `chat_verification`, `church_growth` (new; HEADs unchanged since S326) | refuse, exit 2 | 6 / 0 each | 9 each | 0 / 0 | exit 0, writes 0 |
| `nprcgenekeepr` (new; 623 commits since S326) | refuses | 5 / **1** | 7 | 0 / 0 | exit 0, writes 0 |
| `vscode_quarto_ext` (new; 374 commits since) | refuses | 4 / 0 | 7 | 0 / 0 | exit 0, writes 0 |
| `mts-system` (2 commits since), `Philippians`, `wsfct` (14 since) (legacy) | refuse | 4 / 0 each | 22 each | 0 / 1 each | exit 0, writes 0 |
| `dalia_martinez_funeral` (legacy) | **plain, exit 0** | 0 / 0 | 25 | 0 / 3 | exit 0, writes 0 |
| `claude_work` (no commits; the clone is empty) | **plain, exit 0** | 0 / 0 | 30 | 0 / 7 | exit 0, writes 0 |

1. **10 of the 12 refuse a plain sync (exit 2), 52 files in all** (S326: 10 and 39). 51 are a blob found only in the fork's history of that file, a
   fork version and not an edit of the adopter's. **One is in no history: `nprcgenekeepr`'s `methodology/methodology_trim.py`**, the same file as at
   S326 (the register's **F19**), 49 changed lines against the fork tip's copy; the adopter's last commits on it are `e90a9b99` (2026-10-22, "put the
   project's SESSION_NOTES.md ledger spec back") and `3bc8a1e8` (the same day, a `bin/sync --force`). `--force` drops those lines without saying so.
2. **The refusal is a property of the candidate's history of each file.** In 12 of 12 the tool's refusal list equals the rule "the adopter's blob is in
   neither the candidate's history of that file nor its current blob" (output section 5). The fork tip's own `bin/sync` over the same clones exits 0
   at 11 and refuses only that one F19 file at the twelfth (not the candidate's bytes, so the operator's own tool and not a control).
3. **One forced sync, then plain.** A second plain sync after the forced one's commit exits 0 and writes nothing at 12 of 12, for both tools.
4. **Seeds: 0 changed, by either tool, at all 12.** The candidate created 13 where one was absent (`.gitattributes` at `mts-system`, `Philippians`
   and `wsfct`; 3 at `dalia_martinez_funeral`; 7 at `claude_work`) and none at the new-layout adopters. A dry run says `would create`, and the
   dry-run list equals the real write set (`git status --porcelain` in the clone) at 12 of 12.
5. **Upstream's tool at the 7 migrated adopters** exits 0 on a dry run and writes 23 framework files outside `methodology/` (a second copy) at each;
   it created 41 seeds at the root of six of them beside the adopter's own folder. `chat_verification`'s and `church_growth`'s own ratchet hook
   refuses that commit ("half-migrated: this commit's index holds the manifest at `.quality-gates.json` AND at `methodology/.quality-gates.json`").
   The candidate's tool refuses neither shape. At the 3 legacy adopters that carry fork versions, upstream's tool also exits 2, on the same 4 files
   the candidate refuses (`SESSION_RUNNER.md`, `BOOTSTRAP.md`, `methodology_dashboard.py`, `HOW_TO_USE.md`): the candidate adds no refusal there.
6. **Write sets at the 3 legacy adopters, `dalia_martinez_funeral` and the empty one:** the candidate's is a superset of upstream's (0 paths only
   upstream's; 6, 6, 2, 0 and 6 only the candidate's) and every path that differs is explained by one of the 22 source files that differ between
   upstream's tip and the candidate (output section 3: 0 unexplained).
7. **Fixture (a), an empty project:** both tools write the same 30 paths, 22 differ in bytes, 22 of 22 explained by a changed source; no
   `methodology/` directory. **Fixture (b), upstream's current files with the adopter's 7 seeds edited:** upstream's tool writes 0, the candidate's
   19 (every changed tracked source, nothing else), changes 0 seeds, needs no `--force`; the three changed seed sources stay the adopter's own.

Plan section 6's two rows, **re-run on the rebuilt candidate**: *a legacy project is unchanged in where its files sit* (items 6 and 7); *no file an
adopter owns is overwritten* (items 4 and 7).

## 2. What changed since S326, and why

| Figure | S326 (`ced2c823` on `f34769f3`) | Now (`47637be2` on `d50ce290`) |
|---|---|---|
| Adopters refusing a plain sync | 10 of 12 | 10 of 12 |
| Files refused, all 10 | 39 (38 fork versions, 1 edit) | **52** (51 fork versions, 1 edit) |
| Refused at each of the 5 unchanged new-layout adopters | 4 | **6** |
| Forced sync wrote, new-layout adopters | 8 (`nprcgenekeepr` 8, `vscode_quarto_ext` 6) | 9 (`nprcgenekeepr` 7, `vscode_quarto_ext` 7) |
| Forced sync wrote, legacy adopters | 22, 22, 25, 30, 22 | 22, 22, 25, 30, 22 |
| Upstream's tool wrote at `mts-system` and `Philippians` | 15 | 16 |
| Seeds the candidate created | 13 | 13 |

**The two added files are `methodology/methodology_trim.py` and `methodology/FRAMEWORK_APPARATUS.md`, and the cause is the history, not the
code.** At the 5 unchanged new-layout adopters and at `vscode_quarto_ext` the adopter holds the same two blobs (`24306a82`, `7288b952`).
[`pr3b-why-six-output.txt`](pr3b-why-six-output.txt) (script `pr3b-why-six.py`, read-only) finds each blob at exactly one commit of the OLD candidate
`pr2/candidate` (`98ca7fc9` "methodology_trim.py 1.8.0", `04918ce3` "the framework documents ... hold in both layouts") and in no commit of
`pr2b/candidate` or `upstream/main`; the fork's `main` has both. The old candidate happened to carry the bytes these adopters were synced
with; the rebuilt one, regrouped and scrubbed, does not. `nprcgenekeepr` moved on its own (it re-synced on 2026-10-22) and its set changed in
other files (`BOOTSTRAP.md` and `CLAUDE_TEMPLATE.md` out; `FRAMEWORK_APPARATUS.md`, `methodology_dashboard.py` and `quality_ratchet.py` in).

## 3. The sixteen expectations, scored (`pr3b-expectations.txt`, saved 14:16:45; the run started 14:17:12)

**14 confirmed, 2 not.**

- **E1 wrong (85%):** the exit codes held at the 8 unmoved adopters (2, 2, 2, 2, 2, 2, 0, 0) but the refused-file counts did not: 6, 6, 4, 6, 6, 6, 0, 0
  against the predicted 4, 4, 4, 4, 4, 4, 0, 0. Five of the eight differ. I had written that E1, E2 and E5 ride one fact ("an adopter's blob is a
  fork version, so the candidate's changed history does not reach it"); that fact was false for two files, and section 2 is the finding.
- **E15 not as stated (97%):** 11 of 12 real trees have identical HEAD, refs, status and config before and after. `wsfct` differs in its refs
  only (HEAD `214a8ddc`, status and config equal). Its own reflog shows why: the branch `docs/s740-record-277-prod-deploy` was created at 14:18:49
  (CDT) from HEAD and took two commits at 14:19:06 and 14:19:56, a session of that project, the only ref entries in the window. This run
  only clones and runs `git config --get` against a real tree.
- E2 confirmed (7 new, 4 legacy, 1 none); E3 (72 of 72 dry runs leave the clone clean); E4 (0 seeds changed at 12); E5 (12 of 12); E6 (12 of 12);
  E7 (11 created at the 8 unmoved: `Philippians` 1, `dalia_martinez_funeral` 3, `claude_work` 7); E8 (10 of 12 exit 2); E9 (40%: `nprcgenekeepr` still has
  exactly one file in no history, the same F19 file); E10 (23 at each of 7); E11 (both hooks refuse); E12 (same 30 paths); E13 (30, no `methodology/`);
  E14 (0 against 19, no seed, no `--force`); E16 (267 s, S326: 303 s).

## 4. How the instrument was checked

- The report's own audit columns (output section 5) read yes at 12 of 12: dry runs leave the clone clean, the refusals equal the history rule, the
  plain real run's refusal equals the dry run's.
- Upstream's tool writing 0 at fixture (b) is the zero control for the write-set reader; the explained-by-a-changed-source check found 0 unexplained.
- A fingerprint of the 12 real trees (HEAD, `for-each-ref`, `status --porcelain`, local config) before and after: 11 identical, `wsfct` as in section 3.

## 5. What this does not show

- **The route an adopter takes from GitHub** (`--source=github`) was not run; all runs used the local source.
- **The rule reads the candidate's whole history.** If upstream squash-merges, its history of a file holds fewer intermediate blobs and the
  refused count can only grow; if it merges the 33 commits, as measured. Not measured.
- **The 12 are the operator's own adopters and all carry fork versions**, so the 52 is specific to them and to this history. An adopter on
  upstream's own files is fixture (b): no refusal. An adopter on any other version is unmeasured.
- An adopter's own CI, Windows, a maintainer's machine; `claude_work` has no commits, so its row reads as a fresh install.
- `nprcgenekeepr`, `vscode_quarto_ext`, `mts-system` and `wsfct` moved since S326; their rows are their committed HEADs of 2026-10-29, read in
  clones, and say nothing about their working trees.

## 6. For the pull request's text (PR4)

S326's section 4 said "files this history never carried"; that still holds, but **no number of refused files should be quoted** (S326's 38 is now 51,
and it moves with how the pull request's history is composed). It can say, each tied to a command in the diff: the first sync from the candidate's
tool needs one `--force` where the project holds files this history never carried, and every later sync is plain; the tool refuses by name and
says what to diff; it never changes a seed and installs one only where absent; a migrated project synced by an older tool gets a second copy,
which is why the sync layer is in the pull request. It should not say the operator's 10 are typical.

## 7. His calls this leaves open

None new. F19 stands (`--force` at `nprcgenekeepr` drops its 49 lines). Whether the pull request should say how it expects to be merged, given
section 5's second bullet, is PR4's question.
