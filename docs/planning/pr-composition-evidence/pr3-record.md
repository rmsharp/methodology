# PR3, the adopter-impact table: the record (S326, 2026-10-15)

Row PR3 of `docs/planning/upstream-pr-composition-plan.md` section 5: `bin/status` and `bin/sync` from the candidate over the 12
adopters in `--no-local` clones, files written, files refused, seeds untouched, and a legacy fixture synced by upstream's tool and
by the candidate's, trees diffed. Local only; nothing is sent to `KJ5HST/methodology`. The tables are
[`pr3-adopters-output.md`](pr3-adopters-output.md) (the script's own report, 303 s), the data [`pr3-rows.json`](pr3-rows.json),
the script [`pr3-adopters.py`](pr3-adopters.py) (`python3 docs/planning/pr-composition-evidence/pr3-adopters.py` from the
repository root; it clones, never touches a real tree, and takes `--only NAME ...`). The candidate is the local ref `pr2/candidate`
at `ced2c82`, upstream's tool is `upstream/main` at `f34769f`.

## 1. The answer

| Adopter (layout at its HEAD) | Candidate's plain `bin/sync` | Refused: fork version / edit | A forced sync wrote | Seeds changed / created | Next plain sync |
|---|---|---|---:|---|---|
| `model_project_constructor` (new) | refuses, exit 2 | 4 / 0 | 8 | 0 / 0 | exit 0, writes 0 |
| `feedback-loop-comparison` (new) | refuses | 4 / 0 | 8 | 0 / 0 | exit 0, writes 0 |
| `nprcgenekeepr` (new) | refuses | 4 / **1** | 8 | 0 / 0 | exit 0, writes 0 |
| `vscode_quarto_ext` (new) | refuses | 2 / 0 | 6 | 0 / 0 | exit 0, writes 0 |
| `airqino`, `chat_verification`, `church_growth` (new) | refuse | 4 / 0 each | 8 each | 0 / 0 | exit 0, writes 0 |
| `mts-system`, `Philippians`, `wsfct` (legacy) | refuse | 4 / 0 each | 22 each | 0 / 1 each | exit 0, writes 0 |
| `dalia_martinez_funeral` (legacy) | **plain, exit 0** | 0 / 0 | 25 | 0 / 3 | exit 0, writes 0 |
| `claude_work` (no commits; the clone is empty) | **plain, exit 0** | 0 / 0 | 30 | 0 / 7 | exit 0, writes 0 |

1. **10 of the 12 refuse a plain sync (exit 2), 39 files in all.** 38 are a blob found only in the fork's history of that file:
   a fork version, not an edit of the adopter's. **One is in no history: `nprcgenekeepr`'s `methodology/methodology_trim.py`**, 49
   changed lines against the fork tip's copy, its own commit `5a41dbbd` (2026-10-11) "put the project's SESSION_NOTES.md ledger
   spec back"; this is the register's **F19** (open, his triage), and `--force` drops those lines without saying so.
2. **The refusal is a property of the source's history, not of an adopter or of the code.** In 12 of 12 the tool's refusal list
   equals the rule "the adopter's blob is in neither the candidate's history of that file nor its current blob" (section 5 of the
   output). The fork tip's own `bin/sync` over the same clones exits 0 at 11 and refuses only that one F19 file at the twelfth. (It
   is not the candidate's bytes, `df1b7ea` against `8471117`, so this is the operator's own tool, not a control.)
3. **One forced sync, then plain.** A second plain sync after the forced one's commit exits 0 and writes nothing at all 12.
4. **Seeds: 0 changed, by either tool, at all 12.** The candidate created 13 where one was absent (`.gitattributes` at three legacy
   adopters, three at `dalia_martinez_funeral`, seven at `claude_work`) and none beside an adopter's own. A dry run says
   `would create`, and the dry-run list equals the real write set (`git status --porcelain` in the clone) at 12 of 12.
5. **Upstream's tool at the 7 migrated adopters** exits 0 on the plain run, writes 23 framework files outside `methodology/` (a second
   copy) at each, and creates seeds at the root of six of them (41 in all) beside the adopter's own. `chat_verification` and
   `church_growth`'s own ratchet hook refuses that commit: "half-migrated: this commit's index holds the manifest at
   `.quality-gates.json` AND at `methodology/.quality-gates.json`". The candidate's tool refuses neither shape. At the 3 legacy adopters
   that carry fork versions, upstream's tool also exits 2 on the same 4 files the candidate refuses (`SESSION_RUNNER.md`, `BOOTSTRAP.md`,
   `methodology_dashboard.py`, `docs/methodology/HOW_TO_USE.md`): the candidate adds no refusal there.
6. **Write sets at the 4 legacy adopters and the empty one:** the candidate's is a superset of upstream's (0 paths only upstream's; 7, 7, 2, 0 and 6 only the
   candidate's) and every path that differs is explained by one of the 22 source files that differ between upstream's tip and the
   candidate (output section 3: 0 unexplained).
7. **Fixture (a), an empty project:** both tools write the same 30 paths, 22 differ in bytes, **22 of 22 explained by a changed source
   and every changed source differs**; no `methodology/` directory. **Fixture (b), upstream's current files with the adopter's 7
   seeds edited:** upstream's tool writes 0, the candidate's 19 (every changed tracked source, nothing else), changes 0 seeds, needs
   no `--force`; the three changed seed sources (`CHANGELOG.md`, `HANDOFFS.md`, `quality-gates.json`) stay the adopter's own.

Plan section 6's two rows, **re-run**: *a legacy project is unchanged in where its files sit* (items 6 and 7); *no file an adopter owns is
overwritten* (items 4 and 7: seeds read `present (seed; left as-is)` or `not created: ... (seed; left as-is)`).

## 2. How the instrument was checked, and what it got wrong

- **The first full run read "dry run equals the real write set: NO" at 5 adopters.** The cause was mine: a dry run says
  `would create` for an absent seed and my parser counted only `would write`. Fixed in `phrase_class`; the final run reads yes at 12.
  The check is the point: a report read from the tool's own words would have shown 21 where 22 are written.
- Each dry run was followed by `git status --porcelain` in the clone: clean after all 72 (3 tools, 12 adopters, two dry runs each).
- Upstream's tool writing 0 at fixture (b) is the zero control for the write-set reader.
- **Two numbers carried from earlier sessions are corrected.** "9 of 12 need `--force`" (S322's `layer7b-adopters-output.md`) counted the
  adopters whose result differed between its two tips, which leaves out `nprcgenekeepr`; the refusing adopters are 10, as S322's own run A
  forced (10). And "the fork's `bin/sync`, same bytes" was true at S322's tips (`df1b7ea` at both `ab35e96` and `91fdf8c`); the candidate's
  file changed afterwards (the scrub and the reduction), the fork's did not.
- `nprcgenekeepr` has a live session: its HEAD moved from `aaebcced` to `245c742b` (two commits, 13:37 and 13:41) between this
  session's first and last runs. The runs read committed HEADs in clones; the counts for it are the same in both.

## 3. What this does not show

- **The route an adopter takes from GitHub** (`--source=github`) was not run; all runs used the local source. The rule (a blob in no
  history of the file) is the same, but a clone of a merged upstream is not the candidate's clone.
- **The 12 are the operator's own adopters and all carry fork versions**, so item 1's 38 is specific to them. An adopter on upstream's own files
  is fixture (b): no refusal. An adopter on a version that is in neither is unmeasured.
- An adopter's own CI, Windows and a maintainer's machine; `claude_work` has no commits, so its clone is empty and its row reads as a
  fresh install (its real files are untracked and were not read).
- Hooks: the adopters' hooks ran armed as in the real clones. `wsfct`'s is an absolute path into its real `.git/hooks` and its commit was accepted here.

## 4. For the pull request's text (PR4)

It can say, each tied to a command in the diff: the first sync from the candidate's tool needs one `--force` where the project holds
files this history never carried, and every later sync is plain; the tool refuses by name and says what to diff; it never changes a
seed and installs one only where absent; a migrated project synced by an older tool gets a second copy, which is why the sync layer is in
the pull request. It should not say the operator's 10 are typical.

## 5. His calls this leaves open

None new. F19 (above) is the one the measurement touches: with the candidate's tool, `--force` at `nprcgenekeepr` drops its 49 lines.
