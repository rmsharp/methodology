# BL-113's reduction commit: the record (S325, 2026-10-15)

Option (a) of `docs/planning/BACKLOG-DETAIL.md#bl-113`, decided at S324's picker: a reduction commit on the pull request
candidate so the runner reads under its read-set ceiling. Local ref only; nothing is sent to `KJ5HST/methodology`.

## 1. The answer

One commit on top of the scrub: **`ced2c82`**, now the tip of the local ref `pr2/candidate` (31 commits over `upstream/main`;
the previous tip `28f99a7` is pinned as `refs/pr2/candidate-before-reduction`, read back: 1 ahead, 0 behind). Two files,
+3 / -3 lines (`git diff --numstat`):

| File | Change |
|------|--------|
| `starter-kit/SESSION_RUNNER.md` (1 / 1) | the "Where the files are" paragraph loses its example command: 84 B, **53,184 B to 53,100 B** |
| `.context-budget.json` (3 / 3) | the runner's row records the new blob's density and size and a sentence saying how it was measured; `max_tokens` stays 18,900 |

`context_budget.py --status` reads **ok, exit 0** (was over, exit 2). The doubled read, the number the ceiling is really about:
**18,911.5 tokens before (11.5 over), 18,876.5 after (23.5 under).** The edits are `bl113-build.py` (it refuses on drift),
the message is `bl113-message.txt`. The message and the config sentence carry no session number, backlog code or plan
reference (checked with a pattern over both; the fork-token scan's strict count is the same before and after: 25 lines in 6 files).

## 2. What was measured, and one correction to BL-113

The doubled read (each blob written twice, the Read tool's truncation notice gives the whole-file count; an opus subagent
copied the notices verbatim, `bl113-meter-output.txt`). **The control reproduced:** upstream's blob (`71ad950f`, 52,839 B) read
37,599 doubled, the figure `.context-budget.json` records for it.

| Blob | Bytes | Doubled | Tokens | B/token | Against 18,900 |
|------|-------|---------|--------|---------|----------------|
| control, upstream's runner `71ad950f` | 52,839 | 37,599 | 18,799.5 | 2.8107 | reproduced |
| the candidate's runner before, `3d09a4a8` | 53,184 | 37,823 | 18,911.5 | 2.8123 | **+11.5** |
| after the cut, `07ef7250` (committed) | 53,100 | 37,753 | 18,876.5 | 2.8130 | **-23.5** |

**BL-113 said "21 tokens over"; the measurement says 11.5.** The 21 is the tool's, at 2.8107 B/token, a density measured on
upstream's blob; the candidate's added text is denser (2.8123), so the tool over-read. The config's own note warns of the
opposite direction (text dense in backticked paths costing more per byte); here it went the other way. Either way the
candidate was over, and the cut needed was 12 tokens, not 21.

## 3. The shape: an 11th commit at the tip, not a rebuild of `c8d4375`

His decision at S324 was option (a), a reduction commit. The commit sits after the scrub, at the tip, because that is the only
shape that leaves every verified commit and its tree untouched (three builds of the scrub's ten commits gave one tree, `9c570fa5cf84`, and it was
verified in a clean clone; option (b), a rebuild of `c8d4375`, rewrites the 17 commits after it, the scrub's ten included, and
`scrub-run.sh` pins a base that would be gone). What it costs: a reviewer sees `c8d4375` add the example and this commit drop it.
It is also the shape a reviewer can refuse alone.

## 4. What was cut, and why this

The example command in a migrated project (`python3 methodology/methodology_trim.py --file methodology/CHANGELOG.md --check`).
`FRAMEWORK_APPARATUS.md:487-489` (in the candidate) already carries the same command word for word and cites the runner's
"Where the files are" section by name, so the runner's copy was a duplicate in the file that has a ceiling, and the rule that
the example illustrates ("put `methodology/` in front of the tool and of any methodology file it takes") stays in the
runner. The section's name does not change, so the apparatus's citation holds. A second variant (99 B: two more wording
changes) was measured and not used (`bl113-meter-output.txt`): 23.5 tokens of margin is enough, and fewer changed words is
a smaller thing to review.

## 5. The one hunk he can strip: the density row

The `.context-budget.json` hunk is not what makes the commit pass. At the old density the cut runner reads
int(53,100 / 2.8107) = 18,892, already under 18,900. What the hunk does is follow the file's own rule (a density is tied to
the blob it was measured on; re-measure when the blob changes): the tool now reads this blob at its measured 2.8130, so its
18,876 sits within 0.5 token of the doubled read's 18,876.5. **It is also a loosening of the tool's line by 43 B**, which the
record states rather than hides: with the same ceiling, the runner may now grow to 53,168 B (ok) where the old density allowed 53,125 B at most (`bl113-status-output.txt` §3, a +68 / +69 B mutation on the commit: exit 0 then exit 2). If that is not wanted,
the hunk is separable: drop the `.context-budget.json` change, keep the runner's.

## 6. Verification

- **The tool**, in a clean clone: exit 2 at `28f99a7`, exit 0 at `ced2c82`; the mutation shows the ceiling is live
  (`bl113-status-output.txt`).
- **The gate**, `layer-verify.sh` in a clean `--no-local` clone of `ced2c82` (0 dirty paths): ratchet **18/18, 0 fail,
  0 unmeasured**, results `23481eb88ba1` and manifest `cfa4d5b5fa67`, both equal to the scrub tip's run (the commit changes
  no measured value); the layout scanner 15 files, 0 sites; the shipped proof exit 0 (`bl113-gate-output.txt`). A first run on an
  earlier build of this commit (`7180021`) was stopped and not used: its config sentence read 2.8122 where the figure is 2.8123
  (53,184 / 18,911.5); the build script was corrected and the commit rebuilt, which is `ced2c82`.
- **Blob equality:** `git rev-parse pr2/candidate:starter-kit/SESSION_RUNNER.md` reads `07ef7250`, the blob the meter measured.
- **Fork tokens:** `scrub-derive.py` on the new tip: strict 25 lines in 6 files, the same as before; the one new soft line is
  upstream's own note line, which this commit touches.

## 7. What none of it shows

The meter's tokenizer is the harness's, not a maintainer's agent's; the density is one number per blob and says nothing about
where in the file the tokens fall; the ratchet does not run `context_budget.py --status` (BL-113 (e), still open: add it to
`layer-verify.sh`), so the next layer can cross the ceiling unread again; a maintainer's machine and upstream's CI were not
run; the candidate merged with #94 was not recounted (#94 conflicts in `.quality-gates.json`, `starter-kit/methodology_trim.py` and `tools/test_methodology_trim.py`; this commit touches none of the three); the
subagent that read the notices read two of the four files in one batch, which cannot change a per-file count.
The reading cost was 150,520 subagent tokens.
