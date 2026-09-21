# `context_budget.py`: a real `--status`, refused unknown arguments, and an advisory that agrees with its table

**Date:** 2026-09-20 (fork session S209)
**Status:** RATIFIED — all five decisions in §3 were decided 2026-09-21 by the operator at S209's
decision picker, each as recommended: D1 (b), D2 (a), D3 (a), D4 yes, D5 yes. Implementation is §5,
one phase per session. **P1 DONE 2026-09-21 (S210): `e859196` on the LOCAL branch `fix/context-budget-status`**
(not pushed; see *P1 outcome* under §5 P1). **P2 DONE 2026-09-21 (S211): `c299c30` on the same branch** (see
*P2 outcome* under §5 P2, which also records a status-precedence edge P3 must decide on). Nothing is
upstream-facing. **P3 DONE 2026-09-21 (S212) on `d4dbc26`, and AMENDED by its review:** the operator read the
drafted body and decided two more changes for the same PR, **D6** (an unknown argument's message answers what the
user meant; `--check` becomes a second name for `--status`) and **D7** (a byte ceiling's `over` is no longer
overwritten by a failed structure pattern). See *P3 outcome* under §5 P3. **P2b DONE 2026-09-21 (S213): `612570b`
on the same branch** (see *P2b outcome* under §5 P2b). **P2c and P3′ run in ONE session, by the operator's decision
after S213's close-out (the block just above §5 P2c). P2c DONE 2026-09-21 (S214): `2f73733` on the same branch** (see
*P2c outcome* under §5 P2c); its fresh-clone verification is green, so P3′ follows in the same session. **Then P4.**
Every other phase is one session.
**Backlog:** BL-75 ([detail](BACKLOG-DETAIL.md#bl-75)) and BL-80 ([detail](BACKLOG-DETAIL.md#bl-80)), fork-only.
**Route:** `starter-kit/context_budget.py` is distributed (`bin/_manifest.py:54` on fork `main`, `:46` on
`upstream/main`), so the fix reaches adopters only through **one upstream pull request**. Opening it is
its own go-ahead (§5 P4).

**Line citations name their tree.** The tool is **the same blob, `b1111d92`**, on fork `main` (`84c75e0`),
`upstream/main` (`6b29d3d`) and the heads of open PRs #83 (`219fb9d`), #84 (`77afc12`) and #85 (`e2501c5`),
so a `starter-kit/context_budget.py:N` citation holds in all of them. Everything else is cited as
`upstream:` or `fork:`, because the trees differ.

---

## 0. In one paragraph

`context_budget.py` has no `--status` command, and it ignores any argument it does not recognise, so
`--status`, `--check`, `--force` and `--zzz` all run the default measurement. The default measurement
writes to `.context-budget-history.jsonl` whenever a size changed. The flag is nonetheless cited **122**
times in this fork, **12** times in upstream's own ledgers, and **once** in the body of our open PR #84.
The maintainer's reply on PR #82 also cites it, naming its write as what blocks a context-budget gate.
Separately, whenever the growth run fires, the tool prints *"Nothing is over a ceiling yet"*. It does so
even in the same run whose headline reads `OVER` and whose table shows four rows `over`.
**Decided (§3):**
- make `--status` a real, **write-free** form of the default run;
- refuse unknown arguments with the tool's documented usage exit, 3;
- print the second half of the advisory only when it is true.

On a scratch patch, every existing guard stays green and each behaviour below was observed (§2.6).

---

## 1. Context

### 1.1 The two defects, reproduced

**BL-75: no `--status`, and unknown arguments ignored.** `main()` dispatches on membership tests
(`starter-kit/context_budget.py:1315-1333`: `"--selftest" in args`, `"--calibrate" in args`, `"install-hook"`
in args, `"--precommit" in args`), and anything else falls through to the default run (`:1335-1396`). That
run calls `append_history` (`:1375`) before it renders. Measured in a `--no-local` clone of fork `main` at
`84c75e0`:

| Invocation | Exit | History row written? |
|---|---|---|
| `python3 starter-kit/context_budget.py` | 2 | yes, 168 → 169 rows (a size had changed) |
| `… --status` | 2 | no (nothing changed since the previous run) |
| `… --zzz`, `… --force`, `… --check` | 2 each | no, same reason |

All four print the same ledger, which is why every reading taken under `--status` was sound, as BL-75
already says. At `upstream/main` (`6b29d3d`), in a clean clone, `--status` exits 0 and leaves
`?? .context-budget-history.jsonl` behind. Upstream's `.gitignore:6-9` says the file is deliberately not
ignored, because the series *"survives a fresh clone only if tracked"*, but the file is not in upstream's
tree. So every such run dirties the tree, and the series restarts in every clone.

**BL-80: the advisory contradicts the table.** `render()` prints, whenever the growth run fires
(`starter-kit/context_budget.py:651-653`):

```
growth run: 168 consecutive non-shrinking measurements. Nothing is
over a ceiling yet — that is the point. Ceilings fire late.
```

The second sentence is a literal. Same clone, same run: the headline reads `context budget OVER`
(`worst`, `:584-599`), and four rows read `over`: `docs/FORK_LEARNINGS.md`, `starter-kit/SESSION_RUNNER.md`,
`starter-kit/SAFEGUARDS.md` and `(read-set total)`. The tool already states the rule this sentence breaks
(`:622-624`, on why the growth run prints only on the resident row).

### 1.2 Why this is one pull request and not two

Both defects are about the tool's output contract: what an invocation does, and what the text it prints
claims. They touch one file and its one unit suite, and neither can be merged without the other
conflicting. Independent work *may* go upstream separately (`CLAUDE.md` §Contributing upstream). This
pair is small enough that two PRs would cost the maintainer two reviews for one subject.

### 1.3 Why it is worth the maintainer's review

The maintainer raised the write himself, reviewing PR #82. His reply
([#issuecomment-5701463025](https://github.com/KJ5HST/methodology/pull/82#issuecomment-5701463025), point 6;
fork copy `docs/planning/pr82-maintainer-reply.md:17`) says:

> The proposed `context-budget` gate has a side effect. `--status` writes `.context-budget-history.jsonl`
> into the tree on every run, and `.gitignore` deliberately doesn't ignore it. Tracked-or-ignored gets
> decided first; then the gate.

A write-free `--status` removes that blocker. The context-budget gate then becomes declarable without
first settling tracked-or-ignored. **Declaring that gate stays his decision and is not in this PR** (§7).

---

## 2. Evidence-based inventory

Searches were run on 2026-09-20 against fork `main` at `84c75e0` and `upstream/main` at `6b29d3d`, and
against the seven local adopter clones at these heads: `airqino` `998cd51`, `chat_verification` `107cbed`
(the only one on an older tool, `VERSION` 1.0.0), `model_project_constructor` `62da800`, `mts-system` `99f4e2a`,
`nprcgenekeepr` `589cf73c`, `vscode_quarto_ext` `5cc2717a`, `wsfct` `445b60fa`. The other six carry blob `b1111d92`.
**Adopter repos move under you:** a parallel `wsfct` session committed `ef3eade3` during this session.
**A regex is a sample.** The citation regex is `context_budget(\.py)?`? +--status`, and it misses prose
mentions that do not put the flag right after the name. Those were found separately by `git grep -e '--status'` and are listed by hand in §2.4.

### 2.1 Code sites (`starter-kit/context_budget.py`, blob `b1111d92`, every tree)

| Line(s) | What | Changed by |
|---|---|---|
| `:49` | `CLEAN, WARN, BREACH, USAGE = 0, 1, 2, 3` | nothing; D2 uses `USAGE` |
| `:506-515` | `append_history`: writes only when `files` differ from the last row | nothing |
| `:584-599` | `render()` computes `worst` and prints it as the headline | nothing; D3 reads `worst` |
| `:646-649` | the *"nothing over budget"* branch (correct: gated on no findings) | nothing |
| `:651-653` | the growth-run advisory, second sentence a literal | **D3** |
| `:964` | the installed hook: `exec python3 ".../context_budget.py" --precommit` (no `"$@"`) | nothing |
| `:1282-1283` | selftest: `"--force" not in` the source before `def selftest` | nothing; must stay green |
| `:1290-1311` | `print_usage()`; the default is described as *"append one history line"* (`:1296-1297`) | **D1** (adds `--status`, and makes the write conditional in the text, as BL-75's S202 note measured it is) |
| `:1314-1333` | `main()` argument dispatch by membership | **D2** (reject unknown) |
| `:1375` | `append_history(root, snapshot, hist)`, unconditional call | **D1** (skipped under `--status`) |
| `:1377` | `--json` output (also appends today, via `:1375`) | **D1** (`--status --json` writes nothing) |

### 2.2 Guards that constrain the change

| Guard | Tree and location | What it requires |
|---|---|---|
| Tool selftest | `starter-kit/context_budget.py:1282-1283` | the literal `--force` must not appear before `def selftest`, so the list of accepted arguments must not name it, and neither may any message |
| Shell suite | `upstream:bin/tests.sh:622` / `fork:bin/tests.sh:1971` | no `"--force" in args` in the tool |
| Unit suite | `tools/test_context_budget.py:485-487` (both trees) | the same, asserted in Python |
| Dashboard fingerprint | `upstream:starter-kit/methodology_dashboard.py:500-508` / `fork:…:722-728` | ≥ 2 of *"context_budget.py — size budgets"* (docstring line 2), `CONFIG_NAME`, `HISTORY_NAME`, `growth_run` stay in the source |
| Staleness | `bin/status:38` (both trees) | compares **blob identity**, not `VERSION`, so a bump is optional (D4) |
| Unit-count gate | `upstream:.quality-gates.json:32-37` (floor **118**, measured **118**) / `fork:.quality-gates.json:39` (floor 122) | test count never drops; tightening is owed when it rises (`upstream:.quality-gates.json:3`) |

### 2.3 Callers: who invokes the tool, with what

| Invocation | Where | Under D1(b) + D2(a) |
|---|---|---|
| bare | `upstream:bin/tests.sh:627,631,636`; `vscode_quarto_ext` (*"run it at Phase 0"*, its `HANDOFFS.md:403`) | unchanged |
| `--selftest` | `upstream:bin/tests.sh:615`; `tools/test_context_budget.py` `TestToolInvariants` | unchanged |
| `install-hook` | `upstream:bin/tests.sh:650,659,669`; `nprcgenekeepr` `CLAUDE.md:225` | unchanged |
| `--precommit` | the installed hook (`:964`), live in `nprcgenekeepr` and `wsfct` `.git/hooks/pre-commit:4` | unchanged |
| `--json` | `wsfct` (35 citations); `tools/test_context_budget.py` `TestClassSpec` | unchanged (still records) |
| `--calibrate` | seed config text; every adopter (1 each), `wsfct` 4 | unchanged |
| `--status` | fork (122), `upstream` ledgers (12), `mts-system` (1), PR #84's body (1), PR #82's review thread | **valid, and writes nothing** |
| `--check` | `wsfct` (4), **including a live instruction**: `wsfct/SESSION_NOTES.md:797` at `445b60fa` (`:847` at `ef3eade3`; that file is overwritten every session), *"Re-measure (`python3 context_budget.py --check`) before writing more"* | **exit 3, usage printed**: loud where it was silent (§6) |
| `--zzz-nonsense` | BL-75's own demonstration | exit 3 |
| `--force` | nowhere as a caller; the tool says *"There is deliberately no --force"* (`:1310`) | **exit 3**: the absence becomes observable |

No declared gate on either side runs the tool with an argument. `upstream:.quality-gates.json:35` and
`fork:.quality-gates.json:39` run the unit suite. Nothing in either `.githooks/` calls the tool.

### 2.4 Citations of `context_budget.py --status`, by occurrence

| Repo, head | Count | Where |
|---|---|---|
| fork `main`, `84c75e0` | **122** = 34 live + 88 archived | live, all under `docs/planning/`: `BACKLOG-DETAIL.md` 4, `bl57-p10-nprcgenekeepr-launch-prompt.md` 1, `bl57-p11-model-project-constructor-launch-prompt.md` 3, `changelog-rules-contradictions-plan.md` 6, `changelog-rules-pr-body.md` 1, `pr80-body-after-f3.md` 1, `pr80-f3-variants.py` 2, `pr80-review-response.md` 3, `pr82-comment.md` 3, `pr82-review.md` 5, `upstream-resync-2026-09-plan.md` 5. Archived: 17 shards under `docs/archive/` |
| `upstream/main`, `6b29d3d` | **12** | `CHANGELOG.md` 5, `HANDOFFS.md` 7, all in upstream's receipts S19–S23 (2026-09-15/16, the maintainer's own sessions), e.g. *"context_budget --status exit 0"* as verification |
| `mts-system`, `99f4e2a` | 1 | `CHANGELOG.md:109` (history) |
| GitHub, PR bodies | #84 **1** (ours, open: *"`python3 starter-kit/context_budget.py --status` — nothing over budget"*), #80 1 (ours, merged), #82 1 (the maintainer's, merged) | outward text |
| GitHub, PR #82 thread | our review [#issuecomment-5691623656](https://github.com/KJ5HST/methodology/pull/82#issuecomment-5691623656) proposes `python3 starter-kit/context_budget.py --status` as a gate command (`fork:docs/planning/pr82-comment.md:131`), and the maintainer's reply quoted in §1.3 | outward text |

**Prose mentions the regex misses** (`git grep -e '--status'`, fork `main`):
- `CLAUDE.md:102` (*"reported by `--status`"*);
- `.context-budget.json:92` (*"NOT `--status` -- the flag does not exist and is silently ignored"*, true today, **false after this PR**);
- fork Learnings **#73** (`docs/FORK_LEARNINGS.md:85`) and **#88** (`:100`), both about the history write.

`starter-kit/quality_ratchet.py:543,586` is **a different tool's own, real** `--status` (*"Report the last run
without running anything"*). It is the likeliest source of the habit, and it is the precedent D1 follows.

**Nothing in any distributed document cites `context_budget.py --status`.** On `upstream/main` the tool's
commands are documented only in `print_usage()`, apart from the seed config's one mention of `--calibrate`
(`starter-kit/context-budget.json`), so the PR's documentation surface is that function.

### 2.5 Overlap with the three open PRs (tree: `upstream/main` numbering)

| PR | Touches, among this PR's files | Where | Expected overlap |
|---|---|---|---|
| #84 (`77afc12`) | `tools/test_context_budget.py` (+84/−19), `bin/tests.sh` (+124) | tests `:1231-1279`; shell `:280-312`, `:433` | none if the new tests sit after `TestToolInvariants` (`:476-489`) and the new shell rows inside the budget block (`:607-689`) |
| #85 (`e2501c5`) | `.quality-gates.json` (+7), `CHANGELOG.md` | manifest `:78` (a new gate) | `.quality-gates.json` hunks two gates apart (D5 edits `:10`, `:34`); `CHANGELOG.md` will conflict at its top, as every fork PR does |
| #83 (`219fb9d`) | none of these files | — | none |

**This column is an estimate from hunk positions, not a measurement.** No branch exists to merge. P3
computes it with `git merge-tree --write-tree --name-only` (§5).

### 2.6 The premise, tested on a throwaway patch

This was a scratch clone of fork `main` at `84c75e0`, whose tool blob is upstream's. The patch had three
edits: reject arguments outside a fixed list, skip `append_history` under `--status`, and choose the
advisory's second sentence by `worst`. It was not committed and has been discarded. **Existing guards:**
`--selftest` exit 0 (52 PASS); `tools/test_context_budget.py` 122 tests OK; the `bin/tests.sh` source-grep
passes. **Behaviour, on a tree with a changed size:**
- `--status` exits 2 and writes nothing, and its output is byte-identical to the bare run that follows it.
- `--status --json` gives valid JSON and writes nothing.
- `--zzz`, `--force` and `--check` each exit 3, print `unknown argument: …` and the usage text, and write
  nothing.
- `--help --zzz` exits 0.
- The bare run still appends its row.
- The over-state advisory prints the new sentence.

**Not exercised:** the full `bin/tests.sh`, a synced adopter, and the not-over, run-hit branch. P1–P3 own
those.

---

## 3. Decisions

### D1: what `--status` means

| Option | For | Against |
|---|---|---|
| **(a) An alias of the default run** (measure, record if changed, render) | Smallest change; every past citation becomes literally true, including what it wrote | The name contradicts the sibling tool's `--status`, which runs nothing; the maintainer's blocker stays; fork Learning #73's hazard (a Phase 0 read that dirties the tree) stays |
| **(b) The default run, writing nothing** (measure, render, same exit code) | Every citation still prints the same ledger and exit code. It matches `quality_ratchet.py --status`, clears the maintainer's stated blocker, and makes a Phase 0 read read-only | The history is fed only by bare and `--json` runs. The two repos whose sessions type `--status` stop feeding it. Upstream's file is untracked, so its series already restarts in every clone (§1.1), and the fork's has fired continuously at 168/10. **No adopter types `--status`** (§2.3) |
| **(c) No `--status`**, fix the citations instead | No new surface | With D2(a), the maintainer's receipts, PR #84's body and our #82 review all name a command that now errors. It needs outward corrections, three of them in text we authored |

**DECIDED 2026-09-21 by the operator at S209's decision picker: (b).** It keeps every existing use valid and removes the one side effect anyone has
objected to. Its cost falls only on the two repos that chose the name.

### D2: an argument the tool does not recognise

| Option | For | Against |
|---|---|---|
| **(a) Refuse: exit 3 (`USAGE`, already documented as *"config or usage"*, `:1308`) and print the usage text; write nothing** | The next misremembered flag is loud. `--force` becomes observably absent | One live adopter instruction fails, `wsfct`'s `--check` (§6) |
| (b) Warn on stderr and run as today | Nobody breaks | The run still writes. Exit codes, the only thing scripts read, stay silent. `--force` still appears to work |
| (c) Keep ignoring | — | The defect |

**DECIDED 2026-09-21 by the operator at S209's decision picker: (a).** Two sub-rules: `-h` / `--help` still wins over everything, so `--help --zzz` prints
help and exits 0. The existing precedence between known commands is unchanged: rejecting *combinations* of
known commands is out of scope (§7).

### D3: the advisory's second sentence

| Option | For | Against |
|---|---|---|
| **(a) Choose it by `worst`, the headline's own variable**: keep today's sentence when nothing is over; print a true one when something is (e.g. *"A ceiling has fired as well — see the rows marked over."*) | The advisory and the headline cannot disagree, by construction. The sentence that is right in the common case keeps its point | Two strings to maintain |
| (b) One sentence true in both states (e.g. *"This fires on growth alone, before or after any ceiling."*) | One string | Loses *"nothing is over yet"*, which is the informative case |
| (c) Delete the second sentence | Smallest | Same loss as (b) |
| (d) Move the advisory above the table (BL-80's third idea) | — | Does not make the sentence true |

**DECIDED 2026-09-21 by the operator at S209's decision picker: (a).** The test that would have caught the defect is the invariant itself: across a matrix
of row states × growth-run states, the advisory never says *"Nothing is over a ceiling"* when `worst` is
`over`. It also asserts the not-over, run-hit case still prints the original sentence. That second check
proves the first one does not pass merely because the sentence was deleted.

### D4: `VERSION`

`1.2.0` → **`1.3.0`**, DECIDED 2026-09-21 by the operator at S209's decision picker. The CLI contract changes: one argument is added and input previously
accepted is refused. Nothing depends on the number (`bin/status:38` compares blobs; the dashboard's
fingerprint accepts any version), so this is for a human reading the usage banner. Precedent is mixed. The
maintainer bumped `1.0.0` → `1.2.0` when the tool grew (`8df8faa`), and did not bump for the install-hook fix
(`14bd88a`). **Not a repository release:** no `README.md` What's New entry and no `CLAUDE.md` version line.

### D5: upstream's gate floors

**Tighten in the PR**, DECIDED 2026-09-21 by the operator at S209's decision picker: `context-budget-unit-tests` 118 → the new count, and `tests-sh-passed`
139 → the count measured on the branch. Upstream's own manifest says the tightening is owed whenever a
measured value rises (`upstream:.quality-gates.json:3`), and tightening needs no approval. Leaving it to the
maintainer is the alternative. It costs him a follow-up commit.

### D6: what an unrecognised argument gets (amends D2)

**DECIDED 2026-09-21 by the operator at S212's review of the P3 body: "answer the intent".** The operator's
objection to the drafted body was that it named problems without fixes: for three of the four arguments people
typed, the only remedy was *exit 3 and the usage text*. D2's refusal stands (exit 3, nothing read or written);
what changes is what the refusal says, and one argument is accepted.

**Evidence (S212).** Every flag typed after the tool's name, `git grep -hoE 'context_budget(\.py)?`? +(--?[a-z][a-z-]*|install-hook)' HEAD`
on fork `main`, `upstream/main` and the seven adopter clones at their current heads. The arguments the tool does
not define that anyone typed are **`--status`** (fork 129, `upstream` 12, `mts-system` 1) and **`--check`**
(`wsfct` 4, among them the live instruction *"Re-measure (`python3 context_budget.py --check`) before writing more"*,
`wsfct:SESSION_NOTES.md:903` at `e4ccefb7`; the fork's 3 are quotes in this plan). The fork's 3 hits for `-v`
are `test_context_budget.py -v`, not this tool. Each flag's meaning in the sibling tools, from their `--help`:
`methodology_trim.py --check`, *"evaluate the trigger and report; never writes, even with --write"*;
`methodology_trim.py --force`, *"proceed despite the SRF-RED refusal"*; `methodology_dashboard.py --force`,
*"with --sync, also write targets that are git-tracked"*; `methodology_dashboard.py --dry-run`, *"show planned
changes without writing"*; `quality_ratchet.py --run`, *"run every declared gate, write the results file"*;
`methodology_trim.py --write`, *"actually write"*.

| Argument | Inferred purpose | Handling |
|---|---|---|
| `--check` | re-measure and report, change nothing (the trimmer's meaning; `wsfct`'s use) | **accepted**: the same run as `--status` |
| `--force` | override a refusal (trimmer, dashboard) | exit 3; the message says the one way to permit growth: raise that file's ceiling in `.context-budget.json` |
| `--dry-run` | preview without writing (dashboard) | exit 3; *"did you mean `--status`?"* |
| `--run`, `--write` | do the real thing (ratchet, trimmer) | exit 3; *"run with no argument to measure and record"* |
| a misspelling | a real command | exit 3; the nearest accepted argument, `difflib.get_close_matches(…, n=1, cutoff=0.75)` |
| anything else | unknown | exit 3; no suggestion |

**The cutoff was measured, not chosen (S212).** At `difflib`'s default 0.6, `--version` is offered `--json`, which
is wrong; at 0.75 it is offered nothing. Both cutoffs map `--stauts`, `--statu`, `status`, `--jsn`, `--selftset`,
`--calibrat`, `--precomit`, `--chek` and `--hlep` to the intended command, and neither offers anything for `--zzz`,
`--force`, `--dry-run`, `--run`, `--write`, `--verbose` or `-v`. The one loss at 0.75: `install` is no longer offered
`install-hook`. The candidate list is `ACCEPTED_ARGUMENTS` plus `-h` and `--help`.

### D7: a byte ceiling's `over` survives a failed structure pattern

**DECIDED 2026-09-21 by the operator at the same picker: "fix it in this PR"**, rather than list it or give it its
own item. It is the edge recorded under *P2 outcome* (§5 P2), and it is what keeps D3's sentence true in every
state: today a row over its byte ceiling that also fails a structure pattern reads `instrument-failed`, the headline
follows it, and the advisory says nothing is over. **Rule:** in `measure_file()`, a check may raise a row's status
but never lower it, by `render()`'s ranking (`order`, `starter-kit/context_budget.py:595` on `d4dbc26`:
ok < unmeasured < warn < instrument-failed < over). **Inventory of the status writes** in `measure_file()`
(`:339-450` on `d4dbc26`): `:348`, `:353` unmeasured, each on an early return; `:366` over (the `over()` helper, used
by the byte, line and read-cap checks); `:374` warn (an `elif` after the byte ceiling, while the status is still
`ok`); `:416` warn (guarded by `status == "ok"`); **`:427` instrument-failed, unconditional: the only write that can
lower a status**; `:441`, `:448` over. So the fix is one guard at `:427`. Both findings still print and the exit is
2 either way (`main()`, `:1420-1421`). **Also corrected:** the comment at `:1417-1419` says the tool's ordering
*"already ranks [an instrument failure] above `over`"*; `order` ranks it below.

---

## 4. The design (the decided options)

### 4.1 Interface contract

| Argument(s) | Measures | Writes history | Output | Exit |
|---|---|---|---|---|
| (none) | yes | when a size changed | ledger | 0 / 1 / 2 by verdict |
| `--json` | yes | when a size changed | JSON | same |
| **`--status`** | yes | **never** | ledger | same as (none) on the same tree |
| **`--status --json`** | yes | **never** | JSON | same |
| **`--check`**, **`--check --json`** (D6, P2b) | yes | **never** | as `--status` | same as `--status` |
| `--precommit`, `--calibrate`, `--selftest`, `install-hook` | as today | as today | as today | as today |
| `-h`, `--help` (with anything) | no | no | usage | 0 |
| **anything else** | **no** | **no** | `unknown argument: <arg>` + a hint per D6's table (P2b) + usage | **3** |

**Error contract:** the unknown-argument check runs before `find_root()` / `load_config()`, so a bad
argument never reads or writes the tree. The accepted list is a literal, **`ACCEPTED_ARGUMENTS`, at module
scope above `def selftest`** (S210; this sentence said *"in `main()`"*, where no existing guard could see it).
It must not contain the string `--force` (guards in §2.2). **Usage text:** one new line for `--status`. The default's
*"append one history line"* becomes *"… when a size changed"*, which is what `:511` does.

### 4.2 The advisory

`render()` already holds `worst` (`:584-596`). The growth-run branch (`:651-653`) prints the existing
sentence when `worst != "over"`, and a true alternative when it is. No other output changes.
`test_a_declared_ceiling_still_renders_exactly_as_before` (`tools/test_context_budget.py:935`, both trees) is the
byte-identity witness for everything else.

---

## 5. Phases: one per session, except P2c + P3′ (one session, by the operator's decision)

**Where the work happens:** branch `fix/context-budget-status`, cut from `upstream/main` (`6b29d3d`; re-check
it has not moved). Work in a `git clone --no-local` of this repo, not a worktree, since a worktree shares the
object database. Set `git config core.hooksPath .githooks` in that clone before the first commit. A scratch
clone runs no hooks otherwise, and upstream's hook is what requires `CHANGELOG.md` co-staged on every commit.
Each commit carries one upstream `CHANGELOG.md` entry, on #85's precedent (code + manifest + one entry, no
receipt). **≤ 5 files per commit** (`SAFEGUARDS.md`).

### P1: BL-75, the CLI (D1 + D2 + D4). One session.

- **Files:** `starter-kit/context_budget.py` (`:1290-1311`, `:1314-1333`, `:1375`, and `:41` for D4);
  `tools/test_context_budget.py` (a new class directly after `TestToolInvariants`, `upstream:…:476-489`);
  `bin/tests.sh` (two rows inside the budget block, `upstream:…:607-689`); `CHANGELOG.md`.
- **Tests, written RED first against the unchanged blob `b1111d92`, and the failures recorded:**
  1. `--status` then bare, on a tree with a changed size, print identical stdout, and only the bare run
     appends. Holding the counter still this way is fork Learning #88's control.
  2. `--status` and `--status --json` leave `git status --porcelain --ignored` empty. `--ignored` is
     needed because the history file can be untracked (upstream).
  3. Bare still appends. This is the presence control: the non-write is not a broken writer.
  4. `--zzz` exits 3, names the argument, prints usage, and writes nothing.
  5. `--force` exits 3.
  6. The accepted set equals a **frozen literal** `{"install-hook", "--precommit", "--calibrate",
     "--selftest", "--json", "--status"}` (plus `-h`/`--help`), and every member appears in the usage text.
     A set derived from the code cannot be asserted to cover the code.
  7. `--help --zzz` exits 0.
- **Shell rows** (the adopter-shaped surface: tool + seed config in a `mktemp` project): `--status` leaves
  the project's `git status --porcelain --ignored` empty; an unknown argument exits 3.
- **Mutants that must be killed** (run, not predicted): remove the `--status` guard at `:1375`; remove the
  rejection; add `--force` to the accepted list. The last one must be caught by the three existing guards,
  and by test 5.
- **DONE:** the seven tests and two rows green; mutants killed; `python3 starter-kit/context_budget.py
  --selftest` exit 0.
- **Verify:** `python3 tools/test_context_budget.py` (118 + k, OK); `bash bin/tests.sh` (0 failed) in a fresh
  `--no-local` clone of the branch tip, HEAD asserted by sha; `git grep -n '"--force" in args'
  starter-kit/context_budget.py` empty.
- **Surface:** a clone of the branch, and the suite's `mktemp` adopter projects. **It cannot show** a real
  adopter's hook or history file. Nor can it show upstream's own clones (P3 runs the suite there; adopters
  are P5).

**P1 outcome (S210, 2026-09-21).** One commit, **`e859196`**, on `fix/context-budget-status` from
`upstream/main` `6b29d3d`. It is a **local branch in this repository**, fetched back from the scratch clone;
nothing was pushed. Tool blob `b1111d92` → **`131158cb`**. **Verified in a fresh `--no-local` clone at
`e859196`:** 126 unit tests OK (118 + 8, 2 skipped); `--selftest` 52 PASS, exit 0; the `"--force" in args`
grep empty; `bin/tests.sh` **141 passed, 0 failed**; upstream's ratchet `10/10 pass · results 37bbefc55e64 ·
manifest 97a7aab85b9a`. **RED first on `b1111d92`:** 6 of 8 tests failed; the other 2 are controls that pass by
design (tests 3 and 7). Both shell rows failed, and so did the suite's unit-test row (138 / 3). **Three
departures from the text above:**
1. **The mutant sentence was wrong: none of the three existing guards could see a `--force` in a list inside
   `main()`.** `main()` and `print_usage()` sit below `def selftest`, and the selftest check reads only the
   source above it. The other two guards match `"--force" in args` and nothing else. So the list is
   module-level (§4.1 amended), which makes the selftest the one existing guard that catches it. The two greps
   still catch neither `--force` mutant.
2. **An eighth test.** While the list was being written, a comment above it named the selftest's definition.
   The check splits on the first mention, so the check narrowed to lines 1–55, and `--force` in the list
   passed the selftest. `test_the_selftest_escape_hatch_check_still_reads_the_accepted_list` pins the split
   point. `def selftest` legitimately appears twice (the definition and the check's own literal), so the
   invariant is *"the first mention is the definition"*, not a count of 1.
3. **Four mutants, not three**, all killed: unconditional append (3 unit tests + shell row 1); rejection
   removed (2 + shell row 2); `--force` accepted (tests 5 and 6, and the selftest, via
   `test_the_tool_and_its_selftest_agree_the_gates_all_fire`); a comment above the list naming the selftest's
   definition, plus `--force` (tests 5, 6 and 8, while the selftest misses it). Shell row 2 compares the tree
   with its state after `--status`, not with empty, so a `--status` write is attributed to row 1 alone.

**P2's lines on the branch (`e859196`):** the advisory is `starter-kit/context_budget.py:661-663` (it was
`:651-653` in `b1111d92`), `worst` is `:594-605`, and `render()` is `:591`. The byte-identity witness is
`tools/test_context_budget.py:1063`, and the new region is `:490-615` (`TestCommandLine` at `:503`); put
P2's tests after `:615`, before `TestTokenCeiling` (`:618`).

### P2: BL-80, the advisory (D3). One session, same branch.

- **Files:** `starter-kit/context_budget.py` (`:651-653`); `tools/test_context_budget.py` (same new region);
  `CHANGELOG.md`.
- **Tests, RED first:** (1) the matrix, in-process: `render()` called on synthetic rows for
  `worst` ∈ {ok, warn, unmeasured, over} × `run_hit` ∈ {True, False}, stdout captured, and the advisory
  never asserting *"Nothing is over a ceiling"* when `worst == "over"`; (2) the not-over, run-hit case still
  prints the original sentence; (3) one subprocess run over an `over` fixture with a small `growth_run`
  limit and a seeded history, so the real `main()` → `render()` path is covered.
- **Mutant:** restore the literal. (1) must fail.
- **DONE / Verify / Surface:** as P1, plus `test_a_declared_ceiling_still_renders_exactly_as_before` still
  green. **It cannot show** how a reader takes the new sentence. The operator reads it at P3.

**P2 outcome (S211, 2026-09-21).** One commit, **`c299c30`**, on `fix/context-budget-status` after `e859196`,
built in a `--no-local` clone of the local branch and fetched back as a fast-forward; nothing was pushed. Tool
blob `131158cb` → **`dd4803bf`**. The over-state sentence is the one §3 D3 gave as its example: *"A ceiling has
fired as well — see the rows marked over."* The not-over sentence is unchanged, word for word. **Verified in a
fresh `--no-local` clone at `c299c30`:** 129 unit tests OK (126 + 3, 2 skipped), the byte-identity witness among
them; `--selftest` 52 PASS, exit 0; the `"--force" in args` grep empty; `bin/tests.sh` **141 passed, 0 failed**
(no shell row added); upstream's ratchet `10/10 pass · results 43e25ddcd120 · manifest 97a7aab85b9a`. The tool
was also run on an over project and on a not-over one, each with the growth run fired. Each printed its
sentence, and `git status --porcelain --ignored` showed no write from `--status`. **RED first on `131158cb`:**
tests 1 and 3 failed, each at the assertion under test and not at a fixture check (only the `over` × run-hit
cell of the matrix). Test 2 passes on the old tool by design. **Mutants,** after the fixed tool passed the same
harness: the literal restored (tests 1 and 3); the sentence deleted in both states (all three); the condition
inverted (all three); the condition widened to `instrument-failed` (test 2). `--selftest` catches none of them.
**One extension, no departure:** the matrix covers all five statuses `render()` ranks, adding
`instrument-failed` to the four listed above.

**Found while building P2, and NOT fixed: a row can be over a ceiling and read `instrument-failed`.**
`measure_file()` gives a row the status of whichever check wrote last: a byte ceiling sets `over`
(`starter-kit/context_budget.py:366` on `c299c30`), and a structure pattern below its `expect_min` then
overwrites it with `instrument-failed` (`:427`). A protected-fence finding sets `over` again (`:441`, `:448`).
**Run, not predicted:** a file 1,500 B against a 1,000 B `max_bytes`, a failing `^## ` pattern, and the growth
run fired. Under `--status` on the fixed tool, the headline reads `INSTRUMENT-FAILED`, the row reads
`instrument-failed`, and the advisory keeps *"Nothing is over a ceiling yet"* directly above the finding
*"1,500 B exceeds the 1,000 B ceiling by 500"*. D3 follows `worst` exactly, so the advisory agrees with the
headline, which is what D3 promised. The contradiction left is with a finding. Its cause is status precedence
in `measure_file()`, and the comment at `:1417-1419` says an instrument failure ranks **above** `over`, while
`render()`'s `order` (`:595`) ranks it **below**. **Not in the backlog** (`instrument-failed` returns 0 hits in
`BACKLOG.md` and `BACKLOG-DETAIL.md`). **P3 decides**, as part of the operator's reading of the new sentence:
list it under the PR's *"not changed"* (the upstream entry already does), or make it its own backlog item. It
does not belong inside this PR's two defects.

**P3's lines on the branch (`c299c30`):** upstream's floors are `.quality-gates.json:10` (`tests-sh-passed`,
139; measured 141) and `:34` (`context-budget-unit-tests`, 118; measured 129). The two upstream entries are
`CHANGELOG.md:38` (P2) and `:67` (P1). `upstream:` still has no `.github/`.

### P3: vet and package. One session.

- **Measure on the branch tip** in a fresh clone, HEAD asserted: `python3 starter-kit/quality_ratchet.py
  --run` (the table, not the exit), and the unit count and `tests-sh-passed`.
- **D5:** tighten the two floors to the measured values, in its own commit.
- **Overlap, computed:** `git merge-tree --write-tree --name-only fix/context-budget-status <head>` for
  `77afc12`, `e2501c5` and `219fb9d` (re-fetch the PR refs first: `git fetch --all --prune` deletes
  `refs/remotes/upstream/pr8x`, so use `git fetch upstream refs/pull/<n>/head:refs/remotes/upstream/pr<n>`).
  Then, for each trial merge that is clean apart from `CHANGELOG.md`, run the unit suite and `bin/tests.sh`
  on the merge result. A green branch says nothing about a gate it never ran.
- **The PR body**, drafted to `docs/planning/context-budget-status-pr-body.md` (fork). **Recognized terms
  only:** no session numbers, backlog codes or this plan's D-numbers. It opens on the two defects,
  answers #82's point 6 by link, and states what it does not do (§7).
- **DONE:** branch green on every surface above; conflicts listed; body written and **reviewed by the
  operator**.
- **Surface:** clones and trial merges. **It cannot show** GitHub's merge, because upstream has no CI
  (`upstream:` has no `.github/`) and the merge button runs no checker.

**P3 outcome (S212, 2026-09-21).** **Vetting done on `d4dbc26`; packaging superseded by the review.**
- **Measured first** in a fresh `--no-local` clone at `c299c30`, HEAD asserted: upstream's ratchet `10/10 pass ·
  results 43e25ddcd120 · manifest 97a7aab85b9a` (S211's figure). Only D5's gates had risen: `tests-sh-passed` 141,
  `context-budget-unit-tests` 129. Every other gate measured exactly its threshold.
- **D5 = `d4dbc26`**, on the local branch, fetched back as a fast-forward (`c299c30..d4dbc26`), not pushed:
  `.quality-gates.json:10` 139 → 141 and `:34` 118 → 129, plus one upstream `CHANGELOG.md` entry (the new top entry
  at `CHANGELOG.md:38`; jargon scan 0 hits).
- **Overlap, computed from `d4dbc26`:** #84 (`77afc12`) clean, `CHANGELOG.md` included; #85 (`e2501c5`) and #83
  (`219fb9d`) conflict in `CHANGELOG.md` only, with `.quality-gates.json` auto-merging with #85's new gate. **Merged
  for real** in scratch clones (`CHANGELOG.md` by `git merge-file --union`, markers grepped before `git add`, entry
  counts 59 = 58 + 56 − 55). The ratchet on each merge result, run serially:
  - #84: `10/10 · results 03f9f21f348d`, `bin/tests.sh` 165 / 0, budget units 133.
  - #85: `11/11 · results 2bfa474023b7`, with its `pre-commit-selftest`; 141 / 0.
  - #83: `10/10 · results 02f2b08c7697`; 141 / 0.
- **Tip `d4dbc26` verified** in a fresh clone: `--selftest` 52 PASS, the `--force` grep empty, and the ratchet
  `10/10 · results 02f2b08c7697 · manifest ba1ef0894ed2` against the new floors (met exactly).
- **The body** was drafted to [`context-budget-status-pr-body.md`](context-budget-status-pr-body.md) and frozen
  (`e4ad63d`). **The operator's review did not approve it; it amended the design instead (D6, D7).** The frozen
  draft is kept as the record of what was reviewed. P3′ rewrites it (recompose, don't patch).
- **What carries forward:** the merge-tree method, the union resolution and the per-merge ratchet. **What does not:**
  every figure above is `d4dbc26`'s, and P2b/P2c move the tool, the unit count and the conflict surface.

**P3's lines on the branch (`d4dbc26`), for P2b and P2c:**
- **`starter-kit/context_budget.py`** (blob `dd4803bf`):
  - imports `:32-39`; `ACCEPTED_ARGUMENTS` `:58-59`; `measure_file` `:339`, the `:427` write (D7);
  - `render`'s `order` `:595`; `def selftest` `:1122`, its `--force` check `:1298-1299`;
  - `print_usage` `:1306-1331` (the `--force` sentence `:1329`); `main` `:1333`;
  - the rejection `:1337-1342`; the ranking comment `:1417-1419`; the write guard `:1402-1403`.
- **`tools/test_context_budget.py`:**
  - the `"--force" in args` guard `:487`; `TestCommandLine` `:503` (unknown `:580`, `--force` `:583`, frozen set
    `:588`);
  - `NOT_OVER_YET` `:625`; `TestGrowthRunAdvisory` `:634-705`; `TestTokenCeiling` `:706`.
- **`bin/tests.sh`:** the `--force` grep `:622`; the two P1 rows `:675-696`.

### P2b: D6, the argument messages and `--check`. One session, same branch.

- **Where:** a `--no-local` clone of the local branch, HEAD asserted `d4dbc26`, `core.hooksPath` set. Fetch back as
  a fast-forward. ≤ 5 files per commit.
- **Files:**
  - `starter-kit/context_budget.py`: `--check` into `ACCEPTED_ARGUMENTS` (`:58-59`); the write guard
    (`:1402-1403`) skips the append for `--check` too; `print_usage` gains `--check` on the `--status` line; the
    rejection (`:1337-1342`) prints one line per unknown argument, with D6's hint; `import difflib`.
  - `tools/test_context_budget.py`; `bin/tests.sh` (optional: one row, `--check` writes nothing in the `mktemp`
    project); `CHANGELOG.md` (one upstream entry, jargon-scanned).
- **Guards the change must not trip (§2.2):**
  - **The hint table names `--force`, so it must sit BELOW `def selftest`** (`:1122`): the selftest's check reads
    only the source above that line (`:1298-1299`). Just above `print_usage` works. `ACCEPTED_ARGUMENTS` stays
    above it, as P1 decided.
  - **Look a hint up by key** (`HINTS.get(a)`), never with `"--force" in args`: `bin/tests.sh:622` and
    `tools/test_context_budget.py:487` match that text.
  - Never name `def selftest` in a comment above the list (P1 outcome, test 8).
- **Tests, RED first against `dd4803bf`, failures recorded:**
  1. `--check` prints what `--status` prints on the same tree, with the same exit code, and leaves
     `git status --porcelain --ignored` empty (`--check --json` too).
  2. `--force` exits 3, writes nothing, and its line names `.context-budget.json`.
  3. `--dry-run` exits 3 and suggests `--status`; `--run` and `--write` exit 3 and say to run with no argument.
  4. `--stauts` exits 3 and suggests `--status`.
  5. `--zzz` exits 3 with no suggestion. This is the control: the suggestion is not unconditional.
  6. `--version` is offered nothing, which pins the 0.75 cutoff.
  7. The frozen accepted set (`:588`) gains `--check`, and every member is documented.
  - Update `:580` and `:583` only where the message format changes; do not weaken what they assert.
- **Mutants, run:**
  - `--check` dropped from the write guard (test 1);
  - the hint table emptied (tests 2 and 3);
  - cutoff 0.6 (test 6);
  - the suggestion printed unconditionally (test 5);
  - **the hint table moved above `def selftest`: `--selftest` must fail.** Run it, don't reason it.
  - Run the fixed baseline through the harness first (S210's gotcha).
- **DONE:** the tests green; mutants killed; `--selftest` exit 0; both `"--force" in args` greps empty.
- **Verify:** a fresh `--no-local` clone of the new tip, HEAD asserted: the unit suite (129 + k), `bin/tests.sh`
  (141 + 0 or 1 / 0), and upstream's ratchet. The floors are minimums, so they still pass.
- **Surface:** the clone and the suite's `mktemp` projects. **It cannot show** `wsfct`'s live `--check` instruction
  running (P5), or how a reader takes the messages (the operator, at P3′).

**P2b outcome (S213, 2026-09-21).** **Built as specified: `612570b` on the local branch**, fetched back as a
fast-forward `d4dbc26..612570b`, not pushed. Tool blob `dd4803bf` → `f75482c2`.
- **The change:** `--check` in `ACCEPTED_ARGUMENTS` and in the write guard; a `--check` line in the usage text;
  `REFUSED_ARGUMENT_HINTS`, `SUGGESTION_CUTOFF` (0.75) and `refusal_hint()` just above `print_usage`; one refusal
  line per unknown argument. The hints' wording is in the upstream `CHANGELOG.md` entry on the branch (`:38`).
  `VERSION` stays 1.3.0 (P1's bump; the PR is one release).
- **Re-measured before building:** the `difflib` table with `--check` in the candidate list (unchanged from D6), and
  the flag inventory at today's heads (fork, `upstream/main`, seven adopters): still only `--status` and `--check`,
  and `wsfct`'s quoted instruction is still in its `SESSION_NOTES.md` at `918dcef6`.
- **Tests, RED first against `dd4803bf`:** 7 new in `TestCommandLine`, plus `--check` in the frozen set (`:501`).
  6 fail on the old tool, each at the assertion under test. The `--zzz` and `--version` controls pass on it by
  design. One more than the plan's seven: *each unknown argument gets its own line and its own hint*, which covers
  the one-line-per-argument change the plan names but did not test. `:580`/`:583` (now `:602`/`:605`) needed no
  change: a single refusal still contains `unknown argument: <arg>`. `_assert_refused` now also returns the line.
  **`bin/tests.sh` gains the optional row** (`:680-699`): `--check` on the seed config exits as `--status` does and
  writes nothing. It fails on `dd4803bf` (exit 3 against 1), run standalone.
- **Mutants,** after the fixed baseline passed the same harness (`M0`), each test run by its own name:
  - `--check` dropped from the write guard: T1, and the shell row.
  - The table emptied: the `--force`, preview and one-line-each tests.
  - Cutoff 0.6: the `--version` test.
  - Unconditional suggestion: the `--zzz`, `--version` and one-line-each tests.
  - The table moved above `def selftest`: `--selftest` exits 2 (`FAIL --force is not offered`), and so does
    `test_the_tool_and_its_selftest_agree_the_gates_all_fire`.
  - `--selftest` catches only the last.
- **Verified** in a fresh `--no-local` clone at `612570b`, HEAD asserted:
  - 136 unit tests OK (2 skipped);
  - `--selftest` 52 PASS, exit 0;
  - both `--force` greps empty;
  - `bin/tests.sh` 142 / 0;
  - upstream's ratchet `10/10 · results c52d62cd50a4 · manifest ba1ef0894ed2`, with `tests-sh-passed` 142 (floor 141)
    and `context-budget-unit-tests` 136 (floor 129). P3′ tightens both.

**P2b's lines on the branch (`612570b`), for P2c.** Re-derive them anyway, since a line number is a claim about one tree.
- **`starter-kit/context_budget.py`:**
  - `measure_file` `:342-453`; its status writes: `:369` over (the `over()` helper), `:377` warn, `:419` warn,
    **`:430` instrument-failed (D7's guard)**, `:444`, `:451` over;
  - `render`'s `order` `:598`;
  - `def selftest` `:1125`;
  - the write guard `:1437`;
  - the ranking comment `:1452-1454`, BREACH `:1455-1456`.
- **`tools/test_context_budget.py`:** `TestGrowthRunAdvisory` `:695`; `TestTokenCeiling` `:767` (P2c's class goes
  between them).
- **Branch `CHANGELOG.md`:** P2b's entry is the top one (`:38`), and `c299c30`'s, whose *Not changed here* names the
  edge, is two below it.

**P2c and P3′ are ONE session.** The operator decided this on 2026-09-21, after S213's close-out: *"add combining P2c
and P3' into one session"*. The reason is cost. Most of each session goes on re-orienting and re-verifying the same
tree, and P3′'s first step is to re-measure the tip that P2c has just verified. The two phases keep their content;
only the session boundary moves. The combined session keeps that boundary as a gate inside itself:
- **Order:** P2c completely first: RED tests, the fix, mutants, its commit and upstream entry, fetched back as a
  fast-forward, verified in a fresh clone of the new tip. Then P3′ on that tip.
- **The gate between them:** P3′ starts only if P2c's fresh-clone verification is green. If it is not, the session
  closes out at P2c's last clean commit, and P3′ becomes the next session.
- **Separate commits:** P2c's fix and P3′'s floors stay separate commits (≤ 5 files each). Each can be reverted
  alone, and the body's *What can be dropped* stays true.
- **Re-check `upstream/main` and the PR queue** at Phase 0, and again right before the trial merges.
- **The session ends on the operator's review of the rewritten body**, pasted inline. P4 (outward) stays its own
  session and its own go-ahead.
- **Records:** a *P2c outcome* and a *P3′ outcome* block, and one receipt covering both.

### P2c: D7, status precedence in `measure_file()`. Same branch, after P2b; the first half of one session with P3′.

- **Files:** `starter-kit/context_budget.py` (the `:427` guard; the `:1417-1419` comment rewritten to say what the
  code does); `tools/test_context_budget.py` (a new class after `TestGrowthRunAdvisory`); `CHANGELOG.md`.
  **Re-derive every line number on P2b's tip first:** P2b moves them.
- **Tests, RED first against P2b's tool:**
  1. A row over `max_bytes` that also fails a structure pattern reads `over`, keeps both findings, and makes the
     headline `OVER`. With the growth run fired, the advisory prints the over-state sentence. Exit 2.
  2. Control: a row that only fails its pattern still reads `instrument-failed`.
  3. Raising still works: a `warn` row that fails its pattern reads `instrument-failed`.
  4. `--json` reports case 1's row as `over`.
- **Mutants:** the guard removed, so the last writer wins (test 1); the guard over-broad, so `instrument-failed` is
  never set (tests 2 and 3).
- **Do not edit `c299c30`'s upstream entry**, whose *Not changed here* names this edge. The new entry says the edge
  named there is fixed here.
- **DONE, Verify and Surface:** as P2b. `test_a_declared_ceiling_still_renders_exactly_as_before` still holds.

**P2c outcome (S214, 2026-09-21).** **Built as specified: `2f73733` on the local branch**, fetched back as a
fast-forward `612570b..2f73733`, not pushed. Tool blob `f75482c2` → `ea68573e`. Three files, 126 insertions and 4
deletions.
- **The change:** the guard at `:434` on `2f73733` (`if out["status"] != "over":`), with a comment saying a check may
  raise a row's status and never lower it. The comment above `main()`'s exit (`:1457-1460`) now says what the code
  does: a config defect exits BREACH as `over` does, and `order` (`:603`) ranks `instrument-failed` just below `over`,
  which decides only the headline. **Noticed, not changed:** `measure_file`'s docstring (`:343`) still lists
  `status ∈ ok | warn | over | unmeasured`, without `instrument-failed`; outside D7.
- **Tests, RED first against `f75482c2`:** 4 in a new `TestStatusPrecedence` (`tools/test_context_budget.py:779`,
  between `TestGrowthRunAdvisory` and `TestTokenCeiling`), with one module global `FAILING_PATTERN` (`:776`, grepped
  first: no other use in the tool, the tests or `bin/tests.sh`). This phase's tests 1 and 4 (the end-to-end run under
  `--status` and the `--json` row) fail on the old tool at the assertion under test, the headline reading
  `INSTRUMENT-FAILED` and the row `instrument-failed`, after every fixture assertion passed. Tests 2 and 3 pass there
  by design. The end-to-end row is resident, so it also trips its derived token ceiling (≈660 tokens against 440 at
  the floor density). The two unit controls use class `on-demand`, so only the byte and structure checks can write.
- **Mutants** (harness `p2c-mutants.py` in the session scratchpad; fixed baseline M0 first; each test run by name):
  M1, the guard removed, kills tests 1 and 4. M2, the guard never setting the status, kills tests 2 and 3. Two more
  than the plan's two, to show each control is load-bearing alone: M3, raising from `warn` blocked, kills test 3
  only; M4, raising from `ok` blocked, kills test 2 only. `--selftest` catches M2 and M4 (*"a pattern matching
  nothing is instrument-failed, not ok"*), not M1 or M3.
- **The upstream entry** is the branch's new top one (`CHANGELOG.md:38`), jargon scan 0 hits. It names the case in
  `c299c30`'s *Not changed here* (now `:120`) as fixed, and that entry is not edited (0 lines removed from
  `CHANGELOG.md` between `612570b` and `2f73733`).
- **Verified** in a fresh `--no-local` clone at `2f73733`, HEAD asserted:
  - 140 unit tests OK (2 skipped), `test_a_declared_ceiling_still_renders_exactly_as_before` among them, run by name too;
  - `--selftest` 52 PASS, exit 0, and the tool's `--force` grep empty;
  - `bin/tests.sh` 142 / 0;
  - upstream's ratchet `10/10 · results 43c4abce5653 · manifest ba1ef0894ed2`, with `context-budget-unit-tests` 140
    (floor 129) and `tests-sh-passed` 142 (floor 141). Only git-ignored files were written.
  **The gate to P3′ is open.**

### P3′: re-vet and re-package on the new tip. The second half of P2c's session.

- **As P3**, on P2c's tip:
  - measure;
  - tighten the two floors to the new values in a **new** commit (`d4dbc26` stays; its entry is recorded);
  - re-fetch the PR refs, re-run `merge-tree`, trial-merge and run the ratchet on each merge result, serially;
  - **re-check `upstream/main` and the PR queue first:** a merge there changes the base.
- **The body is rewritten from the frozen draft, not patched:**
  - *What this changes*: add D6 and D7.
  - *How it was tested*: add both phases' tests and mutants.
  - *Who notices*: the one adopter's `--check` now works as its author meant.
  - *Not changed here*: the edge leaves this section.
  - *What can be dropped*: two floor commits.
  - Jargon scan; `bin/check-links`.
- **DONE:** as P3, with the rewritten body **reviewed by the operator**.

### P4: open the PR. One session, outward.

- Needs the operator's go-ahead on **the exact body** and on **pushing the branch to fork `origin`**. The
  standing grant covers only `CHANGELOG.md`-only push records to `main`.
- **Before:** `gh pr list -R KJ5HST/methodology` and a check of #83/#84/#85 for a maintainer response. The
  opening decision should see the queue, because the maintainer's review time is the scarce resource. **This
  is sequencing, not a blocker.**
- **After:** `gh pr view <n> --json body,headRefOid` read back against the file; the ledger entry is a
  non-commit action.

### P5: fork-side adoption. After the upstream merge, or earlier by the operator's separate decision.

- Merge the branch (or upstream's merge) into fork `main`.
- `.context-budget.json:92` rewritten, since its *"the flag does not exist"* becomes false.
- `CLAUDE.md:102`: *"reported by `--status`"* → *"`--status` reports without recording"*.
- The fork's `context-budget-unit-tests` and `tests-sh-passed` floors tightened.
- BL-75 and BL-80 closed: index rows moved to §Completed items, detail updated.
- **Not edited:** fork Learnings #73 and #88 (rows are append-only), the ledgers, the archives, or the
  historical plans in §2.4.
- **Adopters:** each by `bin/status` → `bin/sync`, each its own decision. `wsfct`'s sync session must be
  told that `--check` now exits 3 (§6).
- **Surface:** this repo and each adopter clone. **It cannot show** adopters that are not cloned here.

---

## 6. What might break

| Who | What changes | Severity | Mitigation |
|---|---|---|---|
| `wsfct` | ~~`python3 context_budget.py --check` exits 3 with usage instead of measuring~~ **Under D6 (S212), `--check` is accepted as a second name for `--status`:** it measures and reports as before, but no longer appends a history row. That is the one change its live instruction (`SESSION_NOTES.md:903` at `e4ccefb7`) and three ledger citations will see | low: the instruction does what its author meant | name it in `wsfct`'s sync session (P5) |
| a script reading a row's status (`--json`) | under D7, a row over its byte ceiling that also fails a structure pattern reports `over`, not `instrument-failed`; the exit code is 2 either way | negligible | none found |
| fork and upstream sessions typing `--status` | same ledger and exit code; no history row | low | intended (§3 D1) |
| the fork's growth series | fed only by bare / `--json` runs | low: already firing at 168/10 | P5 may make Phase 0 run the bare form where the series matters |
| a script reading exit 3 as "no config" | 3 now also means a bad argument, which the usage line already documents (`:1308`) | negligible | none found (§2.3) |
| a caller passing `"$@"` | none found: the installed hook passes only `--precommit` (`:964`) | — | — |

---

## 7. Out of scope, deliberately

- **Declaring a context-budget gate** in either manifest. D1(b) makes one declarable. Whether to declare
  one is the maintainer's decision for upstream, and the operator's for the fork.
- **Rejecting combinations of known commands** (`--selftest --calibrate`): precedence stays as it is.
- **The growth-run counter reads one higher on every run after the first on an unchanged tree**, then
  holds (measured: 168, then 169, 169, 169 with 169 rows). `growth_run()` pairs the last recorded row with
  an identical snapshot (`:523-527`). Fork Learning #88 records the effect. It is not a backlog item, and
  this PR does not change it.
- BL-81 (stale sizes in `.context-budget.json`), BL-78's closing edits, and any `README.md` or release entry.
- Editing any archived receipt or ledger entry that cites `--status`. Each was a sound reading of the
  default run, and after this PR the command they name exists.

---

## 8. Verification commands (collected)

```
# the defects, before (any tree; blob b1111d92)
python3 starter-kit/context_budget.py --zzz; echo $?          # 2 today, 3 after
python3 starter-kit/context_budget.py --status; git status --porcelain --ignored
# the guards
python3 starter-kit/context_budget.py --selftest; echo $?     # 0
python3 tools/test_context_budget.py                          # Ran N tests ... OK
git grep -n '"--force" in args' starter-kit/context_budget.py # empty
bash bin/tests.sh                                             # 0 failed, in a --no-local clone, HEAD asserted
python3 starter-kit/quality_ratchet.py --run                  # cite the summary line
# overlap (P3)
git merge-tree --write-tree --name-only fix/context-budget-status 77afc12
```
