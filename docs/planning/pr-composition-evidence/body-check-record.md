# `pr4-body-check.py`: a cited commit hash outside the branch now fails (local only; nothing sent to `KJ5HST/methodology`)

**Result.** Check 3 of `pr4-body-check.py` used to print `in upstream..candidate: False` for a hash outside the branch and still
exit 0; it failed only on a hash that did not resolve (`pr4b-record.md` item 5 named the hole, section 7 item 7 asked for the
fix). It now exits 1 on a cited hash that is outside `<upstream>..<candidate>` unless that hash is `<upstream>`'s own tip
(allowed without being named) or is given as an extra argument after `<upstream>`. All seven expectations
(`body-check-expectations.txt`, written before the edit) were confirmed, and the same seven fail five times when the judge is
pointed at the old script (so the judge can fail).

## 1. The change

`pr4-body-check.py:57` to `:90` (check 3) and the usage and item 3 text in its docstring (`:4`, `:8` to `:9`). 26 lines added, 3 removed.

- `python3 docs/planning/pr-composition-evidence/pr4-body-check.py <draft.md> <candidate> <upstream> [<hash> ...]`
- `:60` the tip of `<upstream>` is allowed without being named: it is the base the text says the branch sits on, and deriving
  it from the argument means no hash is baked into the script to go stale.
- `:62` each extra is resolved; one that does not resolve fails (`UNRESOLVED allowed hash`), so a typo cannot silently exempt
  nothing.
- `:85` a cited hash that resolves, is outside the range and is not allowed prints `OUTSIDE and not allowed` and fails.
- `:89` an extra the body does not cite is printed and does not fail: a stale exemption is not a fault in the text.
- In-range lines print exactly as before; an allowed outside line is the old line plus `; allowed (upstream's tip)` or
  `; allowed (named on the command line)`.

The exemptions live on the command line, which the record of a run quotes beside its output, instead of inside the script.

## 2. What a reader of the older records must know

The older records report runs of the OLD script, blob `7733b493f116` (`pr4-record.md:38`, `restore33-record.md:48`: "exit 0"). Run
with three arguments it exits 0 on the posted draft; the new script with the same three arguments exits 1, because that draft
cites four hashes that are not the branch's. The command for the posted draft (#99's body, candidate
`47637be21425`, upstream `d50ce290d921`) is now:

    python3 docs/planning/pr-composition-evidence/pr4-body-check.py docs/planning/upstream-pr-body.md 47637be21425 d50ce290d921 65990cd c8b9ddd e7b389f

`65990cd` is #98's head, `c8b9ddd` and `e7b389f` are two hashes of the fork's `main`, and `d50ce29` (upstream's tip) needs no
argument. The text names each of them as not the branch's (`pr4b-record.md` item 5). Nothing was edited in #99's body, in any
earlier record, or on GitHub.

## 3. Evidence

| What | Where |
|---|---|
| Expectations E1 to E7 with confidences, saved before the edit | `body-check-expectations.txt` |
| The defect reproduced with the committed script before any edit (exit 0, 14 `True`, four `False`: `65990cd`, `c8b9ddd`, `e7b389f`, `d50ce29`) | the counts on the first line of `body-check-output.txt`; the four hashes in `body-check-expectations.txt` |
| The run and judge of E1 to E7 | `body-check-run.sh <scratch-dir>` (from the repository root; exit status = expectations failed) |
| Its output, 7 PASS, exit 0 | `body-check-output.txt` |
| The judge pointed at the old blob (`S=` changed by one `sed` line), 5 FAIL (E1 to E5), E6 and E7 PASS because the two scripts agree there, exit 5 | `body-check-mutant-output.txt` |

E4 and E5 use the commit the run starts on as the "outside" hash, so a re-run prints that commit's short hash (this run: `e66ee17`,
the claim commit) and the script refuses to run if it is inside the candidate.

## 4. Expectations scored

E1 (90%) confirmed: no extras, exit 1, exactly `65990cd`, `c8b9ddd`, `e7b389f` outside, `d50ce29` allowed as upstream's tip.
E2 (90%) confirmed: the three as extras, exit 0. E3 (90%) confirmed: against the old output only the four `False` lines changed.
E4 (95%) confirmed: the negative control (one more cited hash, outside the range, with the three extras given) exits 1 and names
exactly that hash. E5 (85%) confirmed: an unresolved extra exits 1; an uncited extra prints and exits 0. E6 (80%) confirmed: an
in-range hash also named as an extra prints as the old script printed it. E7 (97%) confirmed: with two arguments both scripts
fail with the same `ValueError`. 7 of 7 confirmed; none wrong, none unmeasured.

## 5. What this does not do

- It does not check that an allowed hash is the thing the text says it is (`65990cd` really is #98's head). That is the text's
  claim, and `pr5-step2-readback.sh` reads #98's head from GitHub.
- It does not look at hashes written in a form check 3 does not read (not backticked, more than 12 hex digits, upper case).
- It is not wired into `bin/tests.sh` or a gate: no live caller invokes the script, and the older evidence scripts are not
  tested either. `body-check-run.sh` is its test, run by hand.

## 6. His calls

None outstanding from this. The next time a draft body is checked, pass the hashes the draft names as not the branch's.
