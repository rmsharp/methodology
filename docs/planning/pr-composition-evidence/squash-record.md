# The squash-merge check for pull request #99: the record (S400, 2026-10-30)

**The question.** `bin/sync` in the pull request's branch refuses to overwrite a file in an adopter's project when the adopter's copy is a
version it cannot find in the source's history of that file (the history rule, `pr3b-record.md` section 1, item 2). That history is
what the maintainer merges into `main`. If he merges the 33 commits (a merge commit or a rebase), the history holds every intermediate
version of each file; if he uses GitHub's squash button, it holds upstream's own history plus **one** commit with the final version. S396
left this open ("Not measured", `pr3b-record.md:94`) and wrote that a squash "can only raise" the 52 files refused. This session measured it.
Local only: nothing was sent to `KJ5HST/methodology`; #99, #98 and #96 were not touched.

**The method.** A local branch `pr2b/squash-check` (`ea256adbe208`, never pushed) is `upstream/main` `d50ce290d921` plus one commit whose tree
is the candidate's (`pr2b/candidate` `47637be21425`, the head of #99): same tree `382d305a4c27`, one commit above upstream, 47 files each.
`pr3b-adopters.py` (S396's script, unchanged) then ran twice back to back, from the repository root, over the same 12 adopters: first against
`pr2b/candidate` (the **control**, because four adopters have moved since S396's run), then against `pr2b/squash-check`. The tool code is
byte-identical in both runs, so any difference comes from history alone. The comparison is `squash-compare.py` (read-only), output
`squash-compare-output.txt`.

## 1. The answer

| | Merge route (the control) | Squash route |
|---|---:|---:|
| Adopters that refuse a plain `bin/sync` (exit 2) | 10 of 12 | the same 10 of 12 |
| **Files refused over those 10** | **52** | **71** (+19) |
| Files a forced sync then writes, at each adopter | 9, 9, 7, 22, 7, 22, 9, 9, 9, 25, 30, 22 | identical |
| Seeds changed / the plain sync after the forced one | 0 / writes 0 at 12 of 12 | identical |
| Refusal list equals the history rule (output section 5) | 12 of 12 | 12 of 12 |
| Upstream's tool, and the two legacy fixtures | | identical to the control |

1. **The control reproduces S396 exactly:** 52 files, and the refused set at each adopter equals S396's at 12 of 12.
2. **The squash raises the count by 19 and changes nothing else.** The same 10 adopters refuse; the forced sync writes the same files; no seed
   changes; the next plain sync writes nothing. For the operator's own 12 projects the practical effect is that the refusal names 9 files
   where it named 6 (and 7 where it named 4 or 6): one `--force` is needed either way.
3. **The 19 are 4 file versions** (output section 4 of `squash-compare-output.txt`), each held by an adopter and each carried by exactly **one**
   of the 33 commits, in no commit of upstream's history of that file and not the candidate's final version:

   | File | Version | Held by | The one commit that carries it |
   |---|---|---|---|
   | `methodology/context_budget.py` | `f824ed6178` | 7 adopters | `f767ced0` "context_budget.py 1.4.0" |
   | `methodology/methodology_dashboard.py` | `6a3147468b` | 6 adopters | `e5210601` "methodology_dashboard.py 2.22.0" |
   | `methodology/quality_ratchet.py` | `04da5abc2a` | 5 adopters | `7d87cb2b` "the ledger hook and the quality ratchet find the files under methodology/" |
   | `methodology/quality_ratchet.py` | `312f230140` | `vscode_quarto_ext` | `1d93579a` "quality_ratchet 1.5.0" |

   (7 + 6 + 5 + 1 = 19.) Each is a version that is also in my fork's history (`in_fork` true at every row), and one of the 33 commits holds the same
   bytes at that point (the first two commits are cherry-picks, the last two are not). Under a merge the adopter's copy is "in the source's
   history"; under a squash it is not. Checked again by plain `git rev-parse <commit>:<path>` for all four: each matches, and none appears in
   `git log upstream/main` of that path.
4. **The posted text.** #99's body says: "this branch's `bin/sync` refuses 10 of them, over 52 files: 51 are versions from my fork's history
   that no commit of this branch carries, and one is a project's own edit of `methodology_trim.py`". That is true of the branch as pushed
   (the merge route). Under a squash the same sentence would read **71 files: 70 and one**. S396's record (`pr3b-record.md` section 6)
   advised quoting no number because it "moves with how the pull request's history is composed"; this is the measurement of how far.
   The text does tell the maintainer that a squash folds the commits in (decision 4, second bullet), but not that it moves this figure.

## 2. The fourteen expectations, scored (`squash-expectations.txt`, saved 13:12, before the ref was built; the first run began 13:12:37)

**12 confirmed, 1 wrong, 1 not measured.**

- **E5 wrong (50%):** I expected the squash total to equal the control's, on the premise that no adopter holds a version that exists only as
  an intermediate one. Four adopters' files do. The written fallback ("between 52 and 80", 80%) held: 71.
- **E14 not measured (80%):** I wrote that the 12 real trees would be unchanged before and after, then took no fingerprint before launching,
  so there is nothing to compare. What exists is `squash-reflog-output.txt` (read after the runs): `model_project_constructor` (3 commits at
  13:14, 13:20, 13:22), `nprcgenekeepr` (1 at 13:18) and `wsfct` (2 at 13:12:47) were committed to by their own sessions in or just after the
  window; the other nine moved nothing. The script itself only runs `git clone --no-local` and `git config --get` against a real tree.
- Confirmed: E1 (the ref), E2 (10 of 12 refuse), **E3 (55%: exactly 52, and equal to S396's at 12 of 12)**, E4 (squash contains the control's
  set at every adopter), E6 to E10, E11 (upstream's tool identical at 12 of 12), E12 (both fixtures), E13 (272 s and 266 s; S396: 267 s).

## 3. How the instrument was checked

- **Control against S396:** the refused sets are equal at 12 of 12 (E3), which is the evidence the adopters' framework files did not move.
- **One HEAD moved between the two runs:** `model_project_constructor` (`d7ed920` cloned for the control, `24629e6` for the squash, one commit
  of its own at 13:14:07). `git diff --stat` between them over `methodology/`, `.githooks/` and `bin/` is empty, so the +3 there is not that move;
  the same three files are newly refused at five adopters whose HEADs did not move.
- **The report's header sentence** in `squash-adopters-output.md` says "the local ref `pr2b/candidate` at `ea256ad`". The ref name is hard-coded
  in the script; the sha is the squash branch's. I left the script unchanged rather than edit evidence.
- **Both runs exit 0** and each was one `nohup` job with a done-file (`squash-run-times.txt`); `uptime` load was 5.0 to 7.0.

## 4. What this does not show

- **The squash commit is a stand-in.** GitHub's would carry a different message and author; the tree is what matters, and it is the candidate's. If
  #98 or #96 merges first, the squashed tree is the merge of #99 onto that, not this tree (decision 3 of #99 asks about the order).
- **The route from GitHub** (`--source=github`) was not run; all runs used the local source (as in S396).
- **The 12 are the operator's own projects** and all carry fork versions, so 71 is specific to them. An adopter on upstream's own files refuses nothing
  under either route.
- **A rebase merge** keeps the 33 commits, so by the history rule it reads as the control (52); it was not run separately.

## 5. His calls this leaves open

1. **Whether #99 needs a word about this.** I recommend nothing now: the number belongs to his own 12 projects, the text describes the branch as pushed,
   and the practical effect (one `--force` either way) is the same. If the maintainer says he will squash, one sentence in the reply gives 71 and
   the four versions above. Any comment on #99 is an outward act with its own go-ahead, shown to him first.
2. **Whether to fix the sentence on the fork's side** (`docs/planning/upstream-pr-body.md` line 74 is what was posted; the file would change, the
   posted text would not).

## 6. Files

All in this directory: `squash-expectations.txt`, `squash-compare.py` and `squash-compare-output.txt`, `squash-control-rows.json` and
`squash-control-adopters-output.md` (the control, 272 s), `squash-rows.json` and `squash-adopters-output.md` (the squash, 266 s),
`squash-run-times.txt`, `squash-reflog-output.txt`, this record. Re-run (about 10 minutes, `nohup`, serially):
`T=$(git rev-parse 47637be21425^{tree}); S=$(git commit-tree "$T" -p d50ce290d921 -m squash-check); git update-ref refs/heads/pr2b/squash-check "$S"`, then
`python3 docs/planning/pr-composition-evidence/pr3b-adopters.py --candidate-ref <pr2b/candidate | pr2b/squash-check> --work <dir> --out <dir>` for each
(copy the two `pr3b-rows.json` to `squash-control-rows.json` and `squash-rows.json`; the squash commit's sha differs on re-creation, its tree does not),
then `python3 docs/planning/pr-composition-evidence/squash-compare.py`.
