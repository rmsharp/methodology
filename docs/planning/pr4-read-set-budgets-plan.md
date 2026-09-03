# PR 4 plan — ship the context-budget gate to `read-set-budgets` (read-set budgets, 4 of 4)

**Status: PLAN, written S145 (2026-09-02). Nothing here is implemented, pushed, or opened.** The
plan is the session's one deliverable (`starter-kit/SESSION_RUNNER.md` Phase 2 §Planning Sessions;
FM #18). It is the fourth and last payload of
[`upstream-read-set-pr-plan.md`](upstream-read-set-pr-plan.md) §5 — **Phase 3, "the gate"**, shipped in
this fork at S129 and never carried upstream. PRs 1–3 of the series are merged into
`KJ5HST/methodology:read-set-budgets` ([#76](https://github.com/KJ5HST/methodology/pull/76),
[#77](https://github.com/KJ5HST/methodology/pull/77), [#78](https://github.com/KJ5HST/methodology/pull/78));
`upstream/main` has received none of them and stands at `512c2ed`.

**Base: `cea3068`** — the tip of `read-set-budgets` after #78 merged (2026-09-03T02:04Z, a
2026-09-02 evening session locally). `tree(cea3068) == tree(2c30d0f)`, the tree PR 3 was measured
on. Nothing else is in flight on that branch, so PR 4 needs no stacking.

Every number below was **measured this session** in a clean clone of `cea3068`, never predicted, and
the command that produced it is in §8. Where the plan cannot measure — the maintainer's machine, the
network — it says so by name.

---

## 0. The answer, in one paragraph

**The file port is clean by construction, and the record saying otherwise is corrected in §1.1.**
Upstream's `starter-kit/context_budget.py` is blob `be2721a5`, unchanged since `14bd88a` (v3.7, PR
#66), and that same blob is the exact ancestor of the fork's seven commits on the path. The
path-restricted end-state patch applies to it; so do the seven per-commit patches, in sequence, ending
at the fork's blob `c5ff15e5` (§8, R3). **What is hard is everything coupled to the file.** The fork's
tool **refuses to run without a root `.context-budget.json`** (exit 3, *"refuses to invent budgets for
a project that has not declared them"*), the canonical repo upstream has none, and the distributed
seed dropped in as that config is red on day one for reasons unrelated to this series (`CLAUDE.md`
59,168 B against the seed's 28,000 B; a `budget:protected` fence that file has never had). So PR 4
must **author the canonical root config**, and that config — not the code — is the decision this
plan puts in front of the operator. A candidate is shipped beside this plan as
[`pr4-candidate.context-budget.json`](pr4-candidate.context-budget.json), and it was run: bare exit
**2** with `(read-set total) 67,581 B / 56,750 B over` — the 10,831 B the series exists to make
visible; **0** config defects; `--selftest` **52 PASS / 0 FAIL**; the 116-test module **OK, 2
skipped**; `--precommit` refuses +1 B on every budgeted file and passes every shrink; `bin/tests.sh`
**115 passed / 1 failed** against a control of **114 / 1** — 115 shared rows, one added, zero flips.

---

## 1. The target, and one correction to the record

### 1.1 What S141 and S144 said, and what is true

Two receipts call this payload *"the only [one] with no clean starting point"* and gloss it as *"the
two versions diverged rather than one being a prefix of the other, so there is no single commit to
port"* (`HANDOFFS.md`, S144 `next_steps` (1); S143 `next_steps` (2)). **The file half of that is
false, and the tree half is true — the sentence conflated them.**

| Claim | Measured |
|---|---|
| the two versions diverged | **No.** `git rev-parse upstream/read-set-budgets:starter-kit/context_budget.py` = `be2721a5` = `14bd88a:…` = `upstream/main:…`. The fork's history on the path is **linear from that blob**: 7 commits, no merge, ending at `c5ff15e5`. Upstream's copy is a strict ancestor of the fork's, not a sibling. |
| no single commit to port | **True, and irrelevant to the file.** The seven fork commits touch other files too (`bin/tests.sh`, both dashboard twins, `methodology_trim.py`, `CHANGELOG.md`); *those* trees diverged. The path-restricted patches apply cleanly (§8, R3). |
| ~2.5× size difference | **True**: 29,549 B → 73,014 B, 674 → 1,400 lines, `VERSION` `1.0.0` → `1.2.0`. |

The claim reached three receipts without anyone running `git rev-parse` on the two blobs. Recorded
here, sha-qualified, so the next reader does not inherit it.

### 1.2 What PR 4 is for

`upstream-read-set-pr-plan.md` §3.4 and §5 Phase 3: **per-file ceilings on the Phase 0 read pair,
then a class total whose ceiling is a partition of the read cap, enforced in `precommit()` as well as
reported in `main()`**, with the two shipped defects beneath it repaired (a gate that measured one byte
short and raised on non-UTF-8 content; a `KeyError` on any config without `classes`). Read that plan's
§9 before quoting §3.4 — S129 refuted three of its claims while shipping it.

PRs 1 and 3 **shed** bytes (the Learnings table, the apparatus). PR 2 shipped the **trimmer**. PR 4 is
the only one that **refuses growth**. Without it the series measured a problem and shipped remedies;
with it the repository declines to make the problem worse.

**Title, matching the series:**
`Ship the context-budget gate: token ceilings, class totals, and the repairs beneath them (read-set budgets, 4 of 4)`

---

## 2. Baseline, verified 2026-09-02 on `cea3068`

### 2.1 The payload's files

| Path | `cea3068` (upstream) | fork `main` | Delta |
|---|---|---|---|
| `starter-kit/context_budget.py` | 29,549 B · 674 lines · blob `be2721a5` · `VERSION = "1.0.0"` | 73,014 B · 1,400 lines · blob `c5ff15e5` · `VERSION = "1.2.0"` | 922 changed lines (`--stat`); 1,088-line patch |
| `tools/test_context_budget.py` | **absent** | 1,311 lines · 116 tests · 13 classes | new file |
| `.context-budget.json` (root) | **absent** | 29,813 B, calibrated to *this fork's* files | **do not port**; see §3.3 |
| `.context-budget-history.jsonl` | **absent** | tracked measurement series | **do not port**; §4 D3 |
| `bin/tests.sh` | `== Test: context_budget.py ==` block at `:591` | `== Test 35: … ==` | **block bodies are byte-identical** except the heading line; the fork has one 9-line unit-test wiring block (`:263-271`) upstream lacks |
| `bin/_manifest.py` | `("starter-kit/context_budget.py", "context_budget.py", TRACKED)` at `:46`; seed row `:52` | same rows; +2 placement comments; different `SEED_FORMAT_MARKERS` | **no change** — the comments and the marker change are fork doctrine, not this PR |
| `starter-kit/context-budget.json` (SEED) | 3 files, `resident` total 34,000 | +6 lines: `read_cap_tokens` + its note, `max_tokens` on two entries, a `_max_tokens` note on `LEARNINGS.md` | port (§3.5) |
| `.gitignore` | 5 lines | same 5 + 6 comment lines explaining why the history file is tracked | port the comments (§3.6, optional) |

### 2.2 The files the canonical config would budget

`git cat-file -s cea3068:<path>`:

| File | Bytes | Against |
|---|---|---|
| `CLAUDE.md` | 59,168 | seed resident 28,000 / class 34,000 → **over by 31,168 / 25,168** on arrival under the seed |
| `starter-kit/SESSION_RUNNER.md` | 52,195 | partition ceiling 41,364 → **over by 10,831** |
| `starter-kit/SAFEGUARDS.md` | 15,386 | pinned at 15,386 → **at ceiling** (`new > ceil` is strict) |
| read-set pair | **67,581** | derived class ceiling 56,750 → **over by 10,831** |
| `CHANGELOG.md` | 91,365 | 65,536 → over by 25,829; ≈31,182 tok at the seed's 2.93 B/tok, over the 25,000 cap |
| `HANDOFFS.md` | 70,182 | 65,536 → over by 4,646; 10 receipts |
| `starter-kit/FRAMEWORK_LEARNINGS.md` | 56,673 | not budgeted upstream by this plan (on-demand; see §4 D7) |
| `FRAMEWORK_APPARATUS.md` / `ITERATIVE_METHODOLOGY.md` / `README.md` | 15,493 / 55,976 / 74,636 | not budgeted — read on demand, by humans |

Structure witnesses the candidate config's `structure` patterns need, counted on `cea3068`: **39**
`### YYYY-MM-DD · [` entries in `CHANGELOG.md` (pattern wants ≥ 5), **10** ` ```handoff ` fences in
`HANDOFFS.md` (≥ 1), **1** `## Versioning` heading in `CLAUDE.md` (≥ 1, at `:92`).

### 2.3 The behaviours that forced the design — each one run, not read

| Probe | Setup | Result |
|---|---|---|
| **A** | fork tool + fork test module dropped onto pristine `cea3068`, **no root config** | `Ran 116 tests … FAILED (failures=1, skipped=2)`. The one failure: `TestToolInvariants.test_the_tool_and_its_selftest_agree_the_gates_all_fire` (`tools/test_context_budget.py:468`), *"0 not greater than 30 : selftest row population collapsed"* — it runs `--selftest` with `cwd=REPO`. |
| **A′** | `python3 starter-kit/context_budget.py --selftest` at that root, no config | **exit 3**, *"no .context-budget.json found at or above … This tool refuses to invent budgets for a project that has not declared them."* Zero rows. **This is why the config is in the PR and not left to the maintainer.** |
| **B** | the distributed SEED copied to `cea3068`'s root as the config | **exit 2**: `CLAUDE.md 59,168 B / 28,000 B over`; `(resident total) 59,168 / 34,000 over`; *"the budget:protected fence is missing"*. Red for three reasons that have nothing to do with the read-set. `upstream-read-set-pr-plan.md` §3.4 predicted this (*"Do not port this fork's `.context-budget.json` wholesale … upstream's `CLAUDE.md` is 58,652 B"*); it is 59,168 B today. |
| **C** | fork tool vs upstream tool, each run in an empty adopter dir holding the **unchanged upstream seed** and a 954 B `CLAUDE.md` | **whole-stdout byte-identical, same exit (1)**. An adopter whose config is the old seed sees no output change from the new tool. |
| **D** | the candidate config (§3.3, Appendix A) on `cea3068` with the fork tool | see §3.3 — the numbers in §0. |

### 2.4 Who has the tool today

Three sibling projects on this machine carry `context_budget.py` (the population S129 called *"the
three instrumented adopters"*, inferred there and stated here):

| Adopter | Blob | Bytes | Config | History |
|---|---|---|---|---|
| `chat_verification` | `be2721a5` (= upstream) | 29,549 | yes | yes |
| `wsfct` | `be2721a5` (= upstream) | 29,549 | yes | yes |
| `vscode_quarto_ext` | `73fb90aa` | 41,986 | yes | yes |

`73fb90aa` matches **no commit in this repository's history** on that path (`git log --all -- starter-kit/context_budget.py`, every blob checked) — a locally modified or hand-copied intermediate.
`bin/status` would report it *locally modified*. Not this PR's problem; recorded so the build session
does not treat it as a canonical state. None of the three is at `c5ff15e5`; all three reach it only
after `read-set-budgets` merges to `main` and they sync (`bin/sync --source=github` reads `main`).

---

## 3. What PR 4 carries, file by file — and what it does not

### 3.1 `starter-kit/context_budget.py` → blob `c5ff15e5`, byte-identical to fork `main`

**Ship the end state, not a replay.** Verified (§8, R3): the single path-restricted patch
`git diff 14bd88a main -- starter-kit/context_budget.py` applies to `be2721a5`; the seven per-commit
patches also apply in sequence. The end state is the same either way, and the DONE criterion is the
blob, not the patch: `git rev-parse <branch>:starter-kit/context_budget.py` = `c5ff15e5…`.

**Why not seven commits (refuted):** every intermediate state fails the wired unit test until the
root config exists (Probe A′), so a 7-commit replay is either 7 red intermediate states or the config
landing first against a tool that does not yet read half its keys. The series' convention is 1–3
commits per PR (#76: 1, #77: 1, #78: 3). The fork's commit history stays citable from the PR body,
which is where the reviewer reads it.

What the end state carries, in the fork's own commit order — the PR body's *what changed* section:

| Fork commit | Date | What it did to the tool |
|---|---|---|
| `6a91660` | 2026-08-15 | **BL-38, five defects in the distributed tool.** D1 `size_history()` walks `--first-parent` (two lineages interleaved by date after a sync, so "size at T" stopped being a function); D2 ISO stamps compared as aware datetimes, not strings; D3 `calibration_verdict()` refuses a fit below R² 0.50, a negative slope, an undefined R² — and a refused fit **suppresses** the bytes/token line; D4 the ledger row names the ceiling that fired in its own unit; D5 remediation prose stops naming the home project. Effect at n=76: 14.75 B/tok at R² 0.05 → 2.81 at 0.81. |
| `84abc60` | 2026-08-26 | Read-cap Phase A: the false *"returns the first 2,000 lines silently"* premise corrected in prose. |
| `9e71f83` | 2026-08-26 | Read-cap Phase B: `READ_CAP_TOKENS = 25_000`, `MIN_BYTES_PER_TOKEN = 2.27`, `READ_CAP_BYTES` computed at import; the line-denominated rule deleted. Same constants and same expression the trimmer (#77) already carries upstream — `test_it_agrees_with_the_trimmer_which_computes_it_the_same_way` (`:1230`) asserts that. |
| `28a02a6` | 2026-08-29 | **Ceilings denominated in tokens, gated by class.** `file_density()`, `token_ceiling()` (explicit `max_tokens` governs; else derived from `max_bytes` at the 2.27 floor, clamped at the cap), `config_defects()` (a declared `max_tokens` above the cap is *reported*, never clamped), `WHOLE_READ_CLASSES`. `VERSION` 1.1.0 → 1.2.0. |
| `9999410` | 2026-08-30 | The two defects the gate depends on: `blob_bytes()` via `git cat-file -s` (the old `len(stdout.strip().encode())` was 1 B short on LF, 3 B on CRLF, and **raised `UnicodeDecodeError`** on non-UTF-8); `class_spec()` replaces two `cfg["classes"]["resident"]` accesses that raised `KeyError`. |
| `beffbd0` | 2026-08-30 | **The class-aggregate gate**: `class_totals()` over N classes, in `main()`, `render()` **and `precommit()`**; `framework_share()`, `class_ceiling()` with `derive_from_read_cap`; the read-set class. |
| `c9c9b7b` | 2026-08-30 | Ten reviewed defects in the above — chiefly **a commit contains the index, not the worktree**: `precommit()` is index-driven and reads `HEAD:.context-budget.json` for its baseline, so a `git rm` or rename of a member is a shrink, not a refusal; `config_defects()` gained its first call sites. |

Symbols, at blob `c5ff15e5` (navigate by `grep -n 'def <name>'`; these numbers are true of that blob
only): `file_density` `:99`, `token_ceiling` `:112`, `class_spec` `:128`, `framework_share` `:139`,
`class_ceiling` `:166`, `class_totals` `:178`, `config_defects` `:225`, `blob_bytes` `:285`,
`find_root` `:307`, `load_config` `:315`, `append_history` `:506`, `render` `:581`,
`ledger_dimension` `:672`, `size_history` `:759`, `calibration_verdict` `:837`, `calibrate` `:855`,
`install_hook` `:968`, `precommit` `:1000`, `selftest` `:1106`, `main` `:1314`. Exit codes
`CLEAN, WARN, BREACH, USAGE = 0, 1, 2, 3` (`:49`) — **unchanged from upstream** (`:48` there).

Added since upstream: 13 `def`s (`blob_bytes calibration_verdict class_ceiling class_spec
class_totals config_defects file_density framework_share ledger_dimension linfit parse_iso size_at
size_history token_ceiling`), 6 module constants (`_ISO DENSITY_DRIFT_WARN MIN_BYTES_PER_TOKEN
READ_CAP_BYTES READ_CAP_TOKENS WHOLE_READ_CLASSES`), one removed (`cfg_lookup`). Config keys newly
read: `read_cap_tokens`, `max_tokens`, `bytes_per_token` (per file), `measured_bytes`,
`adopter_reserve_bytes`, `derive_from_read_cap`. **Every one of them defaults when absent** —
`read_cap_tokens` to `READ_CAP_TOKENS` (`:118`, `:160`, `:229`) — which is what Probe C shows.

### 3.2 `tools/test_context_budget.py` — canonical-only, 116 tests, ships as-is

Its own docstring: *"CANONICAL-ONLY. Not in bin/_manifest.py, so adopters do not receive it."* Same
disposition as `tools/test_methodology_trim.py`, which #77 shipped. Sets `sys.dont_write_bytecode`
(`:44`) so it leaves no `starter-kit/__pycache__`.

**It needs almost nothing from this fork — the opposite of PR 2's experience.** Every fixture is a
scratch git repository built in `tempfile` (`git()` helper `:58`), except three tests:

| Test | Needs | On `cea3068` |
|---|---|---|
| `TestToolInvariants.test_the_tool_and_its_selftest_agree_the_gates_all_fire` (`:468`) | a root `.context-budget.json` — it runs `--selftest` at `REPO` | **FAILS without the config** (Probe A), **passes with the candidate** (Probe D). |
| `TestFitGateEndToEnd` ×2 (`:330`, `:356`, `:362`) | *this repository's* session transcripts under `~/.claude/projects/<slug>/*.jsonl` **and** a root config | **skip** — by design, its docstring says *"Skipped is honest; asserting against whatever transcripts happen to be present would not be."* |
| `TestTokenCeiling.test_it_agrees_with_the_trimmer…` (`:1230`) | `starter-kit/methodology_trim.py` source carrying `READ_CAP_BYTES = int(READ_CAP_TOKENS * MIN_BYTES_PER_TOKEN)` | **passes** — #77 put that line upstream at `:129`. |

**The two skips are a surface this plan cannot verify (Learning #13).** On the maintainer's machine the
slug resolves to *his* path; if he has transcripts there, both tests **run** against his transcripts,
his `CLAUDE.md` history and the candidate config's `calibrate_against`, asserting that an impossible R²
floor yields `WARN` + *"no constant recommended"* and a floor of 0.0 yields `CLEAN` + a `bytes/token`
line. Both follow from `calibration_verdict()`'s contract on *any* non-degenerate series, but nobody has
run them on a series other than this fork's. **The PR body must name the two tests and say this.**

### 3.3 The canonical root `.context-budget.json` — the decision

**Design: pin what is over, derive what the series is about, declare what Phase 0 reads.** The
candidate is Appendix A / [`pr4-candidate.context-budget.json`](pr4-candidate.context-budget.json)
(7,764 B). It is the fork's config with every fork-specific measurement removed and every ceiling
re-derived from `cea3068`:

| Entry | Value | Derivation | Day-one status |
|---|---|---|---|
| `classes.resident.total_bytes` | 59,168 | **pinned** = `git cat-file -s cea3068:CLAUDE.md`; one-file class | ok, at ceiling |
| `files[CLAUDE.md].max_bytes` | 59,168 | same pin; `structure` `^## Versioning` ≥ 1; **no `protected_fence`** (the file has none — declaring it manufactures a red) | ok |
| `classes.read-set` | 56,750 derived (`derive_from_read_cap: true`), `warn_bytes` 51,000 | `READ_CAP_BYTES − adopter_reserve_bytes` = 25,000 × 2.27 − 0, computed at run time; a written value that disagrees is a **config defect** | **over by 10,831** |
| `files[starter-kit/SESSION_RUNNER.md].max_bytes` | 41,364 | 56,750 − 15,386 — the partition; identical to the fork's row | **over by 10,831** — the ratchet |
| `files[starter-kit/SAFEGUARDS.md].max_bytes` | 15,386 | pinned at size; byte-identical on both trees (blob `f0964195`) | at ceiling |
| `files[CHANGELOG.md]` / `files[HANDOFFS.md]` | `read-mandated`, 65,536 B, 25,000 tok | the fork's ledger ceilings since 2026-08-15; the token ceiling is the read cap itself | **over** (91,365; 70,182) — see D1 |
| `read_cap_tokens` 25,000 · `bytes_per_token` 2.93 · `fixed_harness_tokens` 35,700 · `growth_run` 10 | **inherited from the seed, labelled so** | the fork's 2.8 / 42,033 were fitted on *this fork's* transcripts and do not transfer; `--calibrate` is the remedy and the `_` keys say so | — |
| `synced` | `[]` | this repo *is* the canonical; a self-comparison is an identity no change can falsify | — |
| `_tool_location` | says **do not run `install-hook` here** | `install_hook()` writes a hook that execs `<root>/context_budget.py`, which does not exist at the canonical root; with `core.hooksPath=.githooks` set it declines (*"already exists and is not ours"*) | — |

**Measured on `cea3068` with the fork tool (Probe D):**

```
context budget  OVER   resident 59,168 B ≈ 20,194 tok
file                                      size     ceiling  status
CLAUDE.md                             59,168 B    59,168 B  ok
starter-kit/SESSION_RUNNER.md         52,195 B    41,364 B  over
starter-kit/SAFEGUARDS.md             15,386 B    15,386 B  ok
CHANGELOG.md                          91,365 B    65,536 B  over
HANDOFFS.md                           70,182 B    65,536 B  over
(read-set total)                      67,581 B    56,750 B  over
resident total 59,168 B / 59,168 B ceiling   growth run 0/10
read-set total 67,581 B / 56,750 B ceiling  over
```

exit **2**; **0** occurrences of *defect* in the output; `--selftest` **52 PASS / 0 FAIL, exit 0**;
the unit module **116 run, OK, 2 skipped**. The `--precommit` matrix, each case staged against a
commit holding the candidate, exit read bare:

| Staged change | Exit | Output |
|---|---|---|
| `SESSION_RUNNER.md` +1 B | **2** | `REFUSED … 52,195 -> 52,197 B ceiling 41,364 B` (the +2 is the appended `x\n`) |
| `SESSION_RUNNER.md` −5,000 B | **0** | passes while still 5,831 B over — *a commit that shrinks always passes* |
| `SAFEGUARDS.md` +1 B | **2** | `15,386 -> 15,388 B ceiling 15,386 B` — the pin holds at exactly the size |
| `CLAUDE.md` +1 B / −3,000 B | **2 / 0** | the ratchet on the resident file |
| `CHANGELOG.md` + one 52 B ledger entry | **2** | `91,365 -> 91,417 B ceiling 65,536 B` — **see D1** |
| `README.md` +1 B (unbudgeted) | **0** | |
| nothing staged | **0** | |

**Not ported from the fork's config, deliberately:** `docs/planning/BACKLOG.md` (fork-only file);
`starter-kit/FRAMEWORK_LEARNINGS.md` on-demand ceiling 73,728 B (D7); every `measured_bytes` /
`measured_on` / per-file `bytes_per_token` (fork measurements); `max_lines` on the ledgers (the
line-denominated form Phase B deleted); the fork's `_` narrative, which cites fork sessions (S90, S129),
BL numbers and fork transcripts.

### 3.4 `bin/tests.sh` — one 9-line wiring block; the test body is already upstream

The upstream `== Test: context_budget.py ==` block (`:591`) and the fork's Test 35 are **byte-identical
apart from the heading line** — install-hook, `core.hooksPath`, foreign-hook, sync distribution and
seed-clobber assertions are all already there. **Do not renumber or retitle it**: upstream's suite has
26 headings with that block unnumbered after Test 25, and a retitle changes no assertion while
touching a row-for-row baseline.

The one addition — the block that runs the module — goes immediately after the trimmer's wiring
(`:240-244`, the `fi` closing `test_methodology_trim.py`), mirroring how #77 wired the trimmer:

```sh
# Same argument as the trimmer's, one tool over. The context_budget.py block below covers the
# budget gate's install/sync/selftest surface; until this line its calibrate() had no test of
# its ARITHMETIC at all, and returned noise on any repo that had merged another lineage of
# its regressor while every row here stayed green.
if python3 "$METHODOLOGY/tools/test_context_budget.py" >/dev/null 2>&1; then
    pass "context budget gate unit tests green"
else
    fail "context budget gate unit tests failed"
fi
```

**Measured effect on the suite** (§8, R6): control `cea3068` **114 passed / 1 failed**; candidate
**115 / 1**; **115 shared row labels, exactly one row added (`context budget gate unit tests green`),
zero status flips**. The one failure on both sides is Test 9, `github source dry-run failed` —
`bin/sync --source=github` reads `KJ5HST/methodology:main`, where three manifest sources are still
absent; it clears only when `read-set-budgets` merges to `main`, and no PR on this branch can clear it.

### 3.5 `starter-kit/context-budget.json` (the SEED) — +6 lines, port

The fork adds a `read_cap_tokens: 25000` key with its `_` note, `max_tokens: 12334` on the seed's
`CLAUDE.md` entry (= 28,000 / 2.27, exactly what the tool derives when the key is absent),
`max_tokens: 25000` on `SESSION_NOTES.md`, and a `_max_tokens` note on `LEARNINGS.md` explaining why an
on-demand file gets no token verdict. It is **documentation of keys the new tool reads**, distributed
to adopters as a seed-once file (`bin/_manifest.py:52`, `SEED`), so it does not overwrite anyone's
existing config; Probe C shows the tool's behaviour on the *old* seed is byte-identical. Covered by the
existing `seed .context-budget.json parses as JSON` row.

### 3.6 `.gitignore` — six comment lines, optional but recommended

The fork's `.gitignore` explains why `dashboard_history.jsonl` and `.context-budget-history.jsonl`
are deliberately **not** ignored (append-only, non-regenerable, the growth-run trigger reads the
second). The first bare run of the tool on the canonical repo creates `.context-budget-history.jsonl`
untracked, and without the comment the maintainer meets an unexplained file. Comments only; no ignore
rule changes.

### 3.7 What PR 4 does **not** carry, each named so it is chosen rather than forgotten

| Not carried | Why | Where it belongs |
|---|---|---|
| `starter-kit/methodology_dashboard.py` / `tools/methodology_dashboard.py` | upstream `2.10.7` vs fork `2.17.0`, a 1,318-line diff per twin plus 2,841 in its tests; the read-cap Phase A/B edits to the dashboard are 2 of 7 versions | its own PR series. Note the inconsistency it leaves: upstream's trimmer (#77) and this tool carry `READ_CAP_TOKENS/MIN_BYTES_PER_TOKEN`; upstream's dashboard carries **no** read-cap premise at all (grep returns nothing) |
| `.githooks/pre-commit` (+86 lines on the fork) | the Phase 1B claim carve-out and its corpus measurements — fork doctrine | the fork; or a separate proposal |
| `bin/_manifest.py` comments and `SEED_FORMAT_MARKERS` | the marker change is S40 doctrine (`Size, and when to archive`) the upstream seeds do not carry | the deferred documentation PR, if at all |
| `bin/check-handoff` comments naming `.context-budget.json` (`:596`, `:650`) | fork-only checker text | — |
| `starter-kit/BOOTSTRAP.md` ownership table naming `.context-budget.json` adopter-owned (`:355-356`) | upstream's BOOTSTRAP has no such table | the **deferred small PR** (S143, operator-chosen): trimmer mentioned 0 times upstream; two stale *"25 distributed"* counts |
| `.context-budget-history.jsonl` | measurements belong to whoever runs the tool; the growth-run series must be *that* repo's | created by the maintainer's first bare run (D3) |
| the fork's own root config | calibrated to an 11,368 B `CLAUDE.md`, cites fork sessions | replaced by Appendix A |
| the two deliberately-left defects (`upstream-read-set-pr-plan.md` §9 footer) | the growth-run advisory prints *"Nothing is over a ceiling yet"* while files are over; `append_history()`'s change test ignores `class_bytes` | follow-ons; both are one-line decisions. Neither is day-one visible upstream (the advisory needs a 10-run history) |
| any edit to `starter-kit/SESSION_RUNNER.md` naming the gate (dragon 4) | grows the capped file ~300 B; an operator decision | raised in the PR body as a question, not made |

---

## 4. Decisions for the operator — recommendation first, alternative stated

**D1 — Declare the two ledgers, or not?** *Recommend: declare them* (as the candidate does). FM #28's
own text says *every artifact the protocol mandates reading gets a declared ceiling*, Phase 0 step 6
reads the newest receipt and reconciles the ledger every session, and omitting the two red rows is the
*Raise the ceiling* remedy wearing a different coat. **The cost, measured:** while either ledger is over
65,536 B, `--precommit` **refuses every commit that appends a ledger entry** (+52 B → `REFUSED`).
Today that bites nobody, because the gate is **not wired** on the canonical repo (dragon 1 below); the
day someone chains it into `.githooks/pre-commit`, no close-out lands until `methodology_trim.py`
(#77) brings both files under 65,536 B. That is a feature of the design — the same relative rule that
refuses growth passes the trim — but the PR body must say it in those words. *Alternative:* omit the
ledgers and let the trimmer's own 196,608 B trigger be their control; then the config budgets only the
files this series is about, and the bare run still exits 2 on the read-set.

**D2 — `CLAUDE.md` at 59,168 B: pin, or seed number?** *Recommend: pin at arrival size.* The seed's
28,000 / 34,000 reads `over by 31,168` on day one for a reason unrelated to the read-set, and the target
for that file is the maintainer's to set. A pin refuses growth today and shrink passes; the `_` key
says the number is a ratchet, not a defended budget.

**D3 — `.context-budget-history.jsonl`: ship, track, or ignore?** *Recommend: ship nothing; port the
`.gitignore` comment; the maintainer commits the file after his first bare run,* as the fork does
(tracked deliberately, `.gitignore:3-9`). Bare and `--json` runs append; `--precommit`, `--selftest`,
`--calibrate`, `--help` write nothing.

**D4 — Commit shape.** *Recommend two commits:* (1) `feat(starter-kit): …` — the tool, the test module,
the `bin/tests.sh` wiring, the seed; (2) `chore(budget): …` — the canonical root config and the
`.gitignore` comment, so the policy file the maintainer may edit is separable from the code. Plus the
upstream `CHANGELOG.md` entry (D6), in whichever commit the build session finds cleanest. One commit
is acceptable; seven is refuted (§3.1).

**D5 — Version.** Not PR 4's to decide. PRs 1–3 were unversioned feature PRs onto `read-set-budgets`;
the version event, if any, belongs to `read-set-budgets` → `main`. The tool's own `VERSION` moves
`1.0.0` → `1.2.0` inside the file regardless.

**D6 — Upstream ledger entry.** *Follow the series' convention: one `CHANGELOG.md` entry in-branch,
no `HANDOFFS.md` receipt* (#76 `5b92b2f` +71 lines and #78 `2897983` +35 lines did this; upstream's
newest receipt is still its own S12). **Observation for the operator, not a PR 4 task:** #77 (the
trimmer) left **no** upstream ledger entry — `git show upstream/read-set-budgets:CHANGELOG.md | grep -i
trimmer` finds only PR 3's mention of the file. That is FM #27 on the upstream ledger; a one-line
backfill could ride with PR 4's entry or with the deferred docs PR. Your call.

**D7 — `starter-kit/FRAMEWORK_LEARNINGS.md` (56,673 B upstream): budget it?** *Recommend: not in PR 4.*
The fork budgets it `on-demand` at 73,728 B, a byte ceiling S121/S131 already flagged as the rot-prone
form for a file whose real unit is the row (`bin/check-learnings` enforces 1,500 B/row upstream
already). Adding a ceiling nobody has defended is policy, not provisioning.

---

## 5. Phases — each one session, each closing at its own STOP

**Phase A — this plan. ✅ DONE at S145.** STOP.

**Phase B — Build PR 4 on `cea3068`, verify, do not push.** One session.

*Do:* in a **clean clone** (`git clone --no-local`, or `git init` + `git fetch <local-repo>
refs/remotes/upstream/read-set-budgets:refs/heads/read-set-budgets` — §8 R1; **never a worktree of
this repo**, whose `bin/tests.sh` mutates live ledgers), branch `pr4/context-budget-gate` from
`cea3068`; `git show main:starter-kit/context_budget.py >` the tool (keep mode 100755); copy
`tools/test_context_budget.py`; insert the §3.4 block after `:244`; copy
`docs/planning/pr4-candidate.context-budget.json` to `.context-budget.json` **after re-running
`git cat-file -s` on `CLAUDE.md`, `SESSION_RUNNER.md`, `SAFEGUARDS.md` at the base and confirming the
pins still equal the sizes** (if the base moved, re-derive; do not ship a stale pin); apply the seed's
+6 lines and the `.gitignore` comments; write the upstream `CHANGELOG.md` entry; commit per D4.

*DONE looks like:* `git rev-parse pr4/…:starter-kit/context_budget.py` = `c5ff15e5…`;
`python3 tools/test_context_budget.py` → `Ran 116 … OK (skipped=2)`; `--selftest` → 52 PASS / 0 FAIL,
exit 0; bare run → exit 2 and the §3.3 table (same rows, same numbers, unless the base moved);
the §3.3 `--precommit` matrix reproduced (7 cases, exits 2/0/2/2/0/2/0, plus nothing-staged 0);
`bin/tests.sh` on a pristine control clone **and** on the branch, rows diffed: **one added row, zero
flips**, both 1 failure = Test 9; `bin/check-links`, `bin/check-learnings`, `bin/check-handoff`,
`bin/check-handoff --all` each **0**, read bare; `git status --porcelain` empty after deleting the
history file the bare run created; `git diff --stat cea3068 pr4/…` lists exactly the §3 files.

*Surface:* the clean clone on this machine. **What it cannot enforce:** the two `TestFitGateEndToEnd`
skips (they need the maintainer's transcripts — state, do not pretend); Test 9 (network + `main`);
the dashboard — at upstream's `2.10.7` it prints `No projects found` at the repo root on both clones,
so **no dashboard criterion is available on this surface** and none is set; and anything about
`bin/sync --source=github`, which cannot see this branch.

*Do not:* push; edit `SESSION_RUNNER.md`; run `install-hook` at the clone root; run `bin/tests.sh`
in this repository's own worktree. **STOP.**

**Phase C — Push the branch and open the PR. REQUIRES THE OPERATOR'S EXPLICIT GO-AHEAD; approving this
plan is not it.** One session. Record the claim in `CHANGELOG.md` **before** acting (a push and a PR
leave no commit here). Push `pr4/context-budget-gate` to `origin`; `git rev-parse origin/pr4/…^{tree}`
equals the measured tree; `gh pr create --repo KJ5HST/methodology --base read-set-budgets` with the
Appendix B body finalised from Phase B's numbers; read back `gh pr view --json state,baseRefName,
mergeable,mergeStateStatus,files` — OPEN, `read-set-budgets`, MERGEABLE, the §3 file list.
`upstream/main` untouched. **STOP.**

**Phase D — Merge, on its own go-ahead.** `gh pr merge --merge` (never squash: #76/#77/#78 are all
two-parent, and a squash breaks the ancestry `read-set-budgets` → `main` will later carry); `gh pr merge`
can print nothing — read `gh pr view --json state,mergeCommit` back; `tree(<merge>) == tree(<head>)`;
read the tool's blob off the merged branch. **STOP.**

*After D, outside this plan:* `read-set-budgets` → `main` (clears Test 9; the version decision), the
deferred documentation PR, and the three adopters' `bin/sync`.

---

## 6. Evidence-based inventory

Every file naming `context_budget` / `context-budget` on either tree, `git grep -c -iE
'context[_-]budget'` excluding the two ledgers, `docs/archive/` and the history file:

| File | fork `main` | `cea3068` | PR 4 |
|---|---|---|---|
| `bin/tests.sh` | 32 | 30 | +1 block (§3.4) |
| `tools/test_context_budget.py` | 17 | — | new (§3.2) |
| `tools/test_methodology_dashboard.py` | 16 | 16 | untouched (BL-31, already upstream via #71) |
| `starter-kit/context_budget.py` | 11 | 10 | replaced (§3.1) |
| `starter-kit/methodology_dashboard.py` / `tools/…` | 10 / 10 | 7 / 7 | untouched (§3.7) |
| `.context-budget.json` | 5 | — | new, from Appendix A (§3.3) |
| `starter-kit/FRAMEWORK_LEARNINGS.md` | 4 | 4 | untouched |
| `README.md` | 3 | 2 | untouched — upstream's two are the v3.7 What's New lines; the fork's third is a fork-only table |
| `bin/_manifest.py` | 3 | 2 | untouched — the row exists (`:46`); the fork's third is a comment |
| `starter-kit/BOOTSTRAP.md` | 2 | 0 | untouched (deferred docs PR) |
| `bin/check-handoff` | 2 | 0 | untouched (fork-only comments) |
| `.gitignore` | 2 | 0 | +comments (§3.6) |
| `CLAUDE.md` | 0 | 1 | untouched (the v3.7 line) |
| `starter-kit/methodology_trim.py`, `bin/check-learnings`, `starter-kit/context-budget.json` | 1 / 1 / 1 | 1 / 1 / 1 | trimmer + checker untouched; seed +6 (§3.5) |
| `docs/planning/*.md` (13 files, 131 mentions) | — | 0 | fork-only; not shipped |

Consumers of the root `.context-budget.json` other than the tool, on `cea3068`: the dashboard's
`_CONTEXT_BUDGET_JSON_SIGNATURES` (`starter-kit/methodology_dashboard.py:747` on the fork; present
upstream since #71) — it *recognises* the file as framework-installed for scoring and reads nothing
from it. `bin/tests.sh` copies the **seed** into scratch projects, never the root file. No other
reader.

---

## 7. Here be dragons — PR 4's own

1. **The tool exits 3 without a root config, and prints zero rows.** Anything that runs it at the
   canonical root — the wired unit test, a maintainer's first `--selftest` — fails until
   `.context-budget.json` exists. The config is not optional decoration on this PR; it is what makes
   the test suite green (Probe A vs D).
2. **Never run `install-hook` at the canonical root.** It writes a hook that execs
   `$(git rev-parse --show-toplevel)/context_budget.py`, which lives in `starter-kit/` here; with
   `core.hooksPath=.githooks` set it declines. The gate on the canonical repo is **measuring only**
   (`python3 starter-kit/context_budget.py --precommit` by hand) until someone chains it into
   `.githooks/pre-commit` — which is `upstream-read-set-pr-plan.md` §6 dragons 1 and 2, and the PR body
   owes them an answer: *the gate binds only someone who chooses to be bound, and this PR does not
   change that.*
3. **With the ledgers declared (D1), a wired gate refuses every close-out until a trim.** Measured:
   a 52 B `CHANGELOG.md` entry → `REFUSED`. Say so before anyone wires it.
4. **Bare and `--json` runs append to `.context-budget-history.jsonl`.** Measure in the clone; delete
   the file before `git status` is read as a criterion; never run a bare measurement in this
   repository's worktree while `bin/tests.sh` runs (governing plan dragon 5).
5. **The two skipped tests may run on the maintainer's machine** (§3.2). A skip that hides an
   unexercised assertion is a mute button; here the skip is honest and documented, but the PR body must
   name both tests so a failure there is recognised as *his transcripts*, not *the tool*.
6. **Do not port the fork's config or its narrative.** It pins `CLAUDE.md` at 18,600 B against an
   11,368 B file and cites S90/S129/BL-37; every such sentence is false on the target tree.
7. **The pins are true of `cea3068` only.** If `read-set-budgets` moves before Phase B, re-run
   `git cat-file -s` and re-derive; a stale pin that is *below* the new size turns a ratchet into a
   red row on arrival. The partition numbers (41,364 / 15,386 / 56,750) do not move unless
   `SAFEGUARDS.md` does.
8. **Keep mode 100755 on the tool.** `git apply` warns on a 644 target; the suite asserts
   `context_budget.py is executable`.
9. **Test 9 is red on both trees and stays red.** It is not a regression of anything on this branch.
10. **`gh pr merge` can succeed silently** (S144). Read state back; compare trees.
11. **Dates cross midnight in UTC.** #78 merged at `2026-09-03T02:04Z` in a 2026-09-02 local session.
    Cite the zone when a date is load-bearing.
12. **The PR 1 body wrote *"The remaining 10,831 B is what the later PRs on this branch are for."***
    No later PR shrank the pair; PR 4 makes the 10,831 B **refuse to grow**. The PR 4 body must not
    imply the pair is fixed — it is exactly as over as PR 1 left it, and now says so out loud.

---

## 8. Reproduction

All run 2026-09-02 from this repository; `$S` is a scratch directory.

**R1 — a clean clone of `cea3068` without network:**
```sh
git init -q "$S/probe/base" && git -C "$S/probe/base" fetch -q "$PWD" \
  refs/remotes/upstream/read-set-budgets:refs/heads/read-set-budgets \
  && git -C "$S/probe/base" checkout -q read-set-budgets      # HEAD = cea3068
```

**R2 — the blob identity behind §1.1:**
```sh
for r in upstream/read-set-budgets upstream/main 14bd88a main; do
  echo "$r $(git rev-parse "${r}:starter-kit/context_budget.py")"; done
# be2721a5… ×3, then c5ff15e5…
git log --oneline main -- starter-kit/context_budget.py | wc -l      # 9 = 7 fork + 2 upstream
```

**R3 — the patches apply (base blob written from THIS repo; the first attempt wrote an empty file by
running `git show` in the scratch repo, and every patch "failed" — check the base blob first):**
```sh
mkdir -p "$S/pc/starter-kit" && git show be2721a5 > "$S/pc/starter-kit/context_budget.py"
git -C "$S/pc" init -q && git -C "$S/pc" add -A && git -C "$S/pc" -c user.name=t -c user.email=t@t commit -qm base
git -C "$S/pc" hash-object starter-kit/context_budget.py                 # be2721a5…
git diff 14bd88a main -- starter-kit/context_budget.py | git -C "$S/pc" apply --check && echo applies
for c in 6a91660 84abc60 9e71f83 28a02a6 9999410 beffbd0 c9c9b7b; do
  git diff "$c^" "$c" -- starter-kit/context_budget.py | git -C "$S/pc" apply && echo "$c ok"; done
git -C "$S/pc" hash-object starter-kit/context_budget.py                 # c5ff15e5…
```

**R4 — Probes A, A′, B (in the R1 clone):**
```sh
cp starter-kit/context_budget.py "$S/probe/base/starter-kit/"; cp tools/test_context_budget.py "$S/probe/base/tools/"
( cd "$S/probe/base" && python3 tools/test_context_budget.py > A.log 2>&1; echo "A exit=$?"; grep -E '^(Ran|OK|FAILED|FAIL:)' A.log )
( cd "$S/probe/base" && python3 starter-kit/context_budget.py --selftest; echo "A' exit=$?" )        # 3
( cd "$S/probe/base" && cp starter-kit/context-budget.json .context-budget.json && python3 starter-kit/context_budget.py; echo "B exit=$?"; rm -f .context-budget.json .context-budget-history.jsonl )
```

**R5 — Probe D (candidate config; commit it so `--precommit` has a HEAD baseline):**
```sh
cp docs/planning/pr4-candidate.context-budget.json "$S/probe/base/.context-budget.json"
# insert the §3.4 block after the trimmer `fi` (upstream bin/tests.sh:244), then:
( cd "$S/probe/base" && git add -A && git -c user.name=t -c user.email=t@t commit -qm candidate
  python3 starter-kit/context_budget.py; echo "bare exit=$?"
  python3 starter-kit/context_budget.py --selftest | grep -cE '^\s*(PASS|FAIL)'      # 52, all PASS
  python3 tools/test_context_budget.py 2>&1 | tail -3                                # OK (skipped=2)
  echo x >> starter-kit/SESSION_RUNNER.md && git add -A && python3 starter-kit/context_budget.py --precommit; echo "exit=$?"; git reset -q --hard )   # 2
```

**R6 — the suite, control vs candidate, rows diffed:**
```sh
( cd "$S/probe/control" && bash bin/tests.sh > "$S/ctl.log" 2>&1 )   # pristine cea3068: 114 passed, 1 failed
( cd "$S/probe/base"    && bash bin/tests.sh > "$S/cnd.log" 2>&1 )   #                  115 passed, 1 failed
for f in ctl cnd; do grep -E '^\s*(PASS|FAIL|SKIP):' "$S/$f.log" | sed 's/^ *//' | sort > "$S/$f.rows"; done
comm -12 "$S/ctl.rows" "$S/cnd.rows" | wc -l      # 115 shared
comm -3  "$S/ctl.rows" "$S/cnd.rows"              # exactly: PASS: context budget gate unit tests green
```

**R7 — sizes and witnesses on the base:**
```sh
for f in CLAUDE.md starter-kit/SESSION_RUNNER.md starter-kit/SAFEGUARDS.md CHANGELOG.md HANDOFFS.md; do
  printf '%-32s %s\n' "$f" "$(git cat-file -s upstream/read-set-budgets:$f)"; done
git show upstream/read-set-budgets:CHANGELOG.md | grep -cE '^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \['   # 39
git show upstream/read-set-budgets:HANDOFFS.md  | grep -c '^```handoff'                             # 10
```

---

## Appendix A — the candidate canonical root config

Shipped as [`pr4-candidate.context-budget.json`](pr4-candidate.context-budget.json) (7,764 B) so the
build session copies a file rather than transcribing one. Its shape, without the `_` prose:

```json
{
  "read_cap_tokens": 25000, "bytes_per_token": 2.93, "fixed_harness_tokens": 35700,
  "growth_run": 10, "calibrate_against": "CLAUDE.md",
  "classes": {
    "resident": { "total_bytes": 59168 },
    "read-set": { "total_bytes": 56750, "warn_bytes": 51000, "derive_from_read_cap": true }
  },
  "files": [
    { "path": "CLAUDE.md", "class": "resident", "max_bytes": 59168,
      "structure": [ { "pattern": "^## Versioning", "expect_min": 1 } ] },
    { "path": "starter-kit/SESSION_RUNNER.md", "class": "read-set", "max_bytes": 41364 },
    { "path": "starter-kit/SAFEGUARDS.md",     "class": "read-set", "max_bytes": 15386 },
    { "path": "CHANGELOG.md", "class": "read-mandated", "max_bytes": 65536, "max_tokens": 25000,
      "structure": [ { "pattern": "^### \\d{4}-\\d{2}-\\d{2} · \\[", "expect_min": 5 } ] },
    { "path": "HANDOFFS.md",  "class": "read-mandated", "max_bytes": 65536, "max_tokens": 25000,
      "structure": [ { "pattern": "^```handoff", "expect_min": 1 } ] }
  ],
  "synced": []
}
```

Every `_` key in the shipped file states the derivation of the number beside it and names the
command that re-derives it. The four calibration constants are labelled **inherited from the seed,
not measured on this repo**, with `--calibrate` as the remedy.

## Appendix B — PR body, draft for Phase C to finalise

> **Base: `read-set-budgets`, not `main`.** Fourth and last of the four PRs staged there. Nothing here
> is proposed for `main` yet.
>
> ## What this does
>
> Ships the context-budget gate the first three PRs measured against: `starter-kit/context_budget.py`
> `1.0.0` → `1.2.0` (29,549 → 73,014 B), its 116-test module, and a root `.context-budget.json` for
> this repository. PRs 1 and 3 shed bytes; this one **refuses growth**. On this branch today:
>
> | | bytes | ceiling | |
> |---|---|---|---|
> | `starter-kit/SESSION_RUNNER.md` | 52,195 | 41,364 | over by 10,831 |
> | `starter-kit/SAFEGUARDS.md` | 15,386 | 15,386 | at ceiling |
> | read-set pair | **67,581** | **56,750** | **over by 10,831** — exactly what PR 1's table left |
>
> The bare run exits 2 and prints that. `--precommit` refuses any commit that grows either file and
> passes any that shrinks one (verified: +1 B refused; −5,000 B passed while still over). **Nothing on
> this branch shrinks the pair; this PR makes it stop growing and say why.**
>
> ## The tool refuses to run without a config, so this PR provisions one
>
> `context_budget.py` exits 3 — *"refuses to invent budgets for a project that has not declared
> them"* — at any root without `.context-budget.json`, and the seed adopters receive reads red here
> for reasons unrelated to this series (`CLAUDE.md` is 59,168 B against the seed's 28,000). So the
> config in this PR **pins** what is over at its arrival size (`CLAUDE.md`), **derives** the read-set
> ceiling from the read cap (25,000 tok × 2.27 B/tok = 56,750, computed at run time), and **declares**
> the two ledgers Phase 0 reads (both over 65,536 B today; `methodology_trim.py` from #77 is the
> remedy). Four calibration constants are inherited from the seed and say so; `--calibrate` replaces
> them.
>
> ## What this does not do, and one thing to decide
>
> - **The gate does not bind anyone here.** `core.hooksPath` is local config; `.githooks/pre-commit`
>   is the ledger gate and this PR does not chain the budget into it; `install-hook` must not be run at
>   this root. It measures. Wiring it is your decision — and with the ledgers declared, a wired gate
>   refuses every ledger-appending commit until both files are trimmed under 65,536 B.
> - `SESSION_RUNNER.md` Phase 0 still never names the tool. Adding one line grows the capped file
>   ~300 B. Not done here.
> - The dashboard twins are untouched (fork is 7 versions ahead; separate series).
>
> ## What changes for adopters who sync
>
> Behaviour on an unchanged seed config is byte-identical (verified). New: ceilings may be declared in
> tokens (`max_tokens`; derived from `max_bytes` at the 2.27 floor when absent); a `max_tokens` above
> the cap is reported as a config defect, never clamped; the gate sizes the **index** with
> `git cat-file -s` (the old path was 1–3 B short and raised on non-UTF-8 content); `precommit` gains
> the class-total arm; `calibrate` walks first-parent history, compares timezone-aware stamps, and
> refuses a fit below R² 0.50; the ledger row names the ceiling that fired in its own unit.
>
> ## Verification
>
> Clean clone of `cea3068`. Unit module 116 run, OK, **2 skipped** — `TestFitGateEndToEnd`, which
> needs *this repository's* session transcripts on the running machine; on yours they may run.
> `--selftest` 52 PASS / 0 FAIL. `bin/tests.sh` **115 passed / 1 failed** vs **114 / 1** on the
> untouched base: one row added, zero status flips; the failure on both is Test 9 (`--source=github`
> reads `main`). `check-links`/`check-learnings`/`check-handoff`/`--all` 0/0/0/0.
