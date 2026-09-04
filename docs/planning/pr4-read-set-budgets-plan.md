# PR 4 plan — ship the context-budget gate to `read-set-budgets` (read-set budgets, 4 of 4)

**Status: RATIFIED by the operator 2026-09-03, at S146 — D1–D11 stand as recorded in §4's ratification
record (D1–D10 as recommended; D4 reshaped and D11 added on the second review's findings). Phase B
(build on `cea3068` in a clean clone, verify, do not push) is authorized as the next session's single
deliverable; Phases C and D are NOT authorized by this ratification and each needs its own explicit
go-ahead. Phase B BUILT at S147 (2026-09-03) as `f3a4b6d`; the self-review's six-row fix-round ran at S148 (2026-09-03), a review lens added fourteen items, and the branch was REBUILT as `pr4/context-budget-gate` = `cf15489` (tree `c857734`), re-verified. Phase C DONE at S149 (2026-09-03): pushed to `origin` and OPEN upstream as [PR #79](https://github.com/KJ5HST/methodology/pull/79) against `read-set-budgets`, MERGEABLE, NOT merged — see §5 Phase B and Phase C for the records; Phase D still needs its own go-ahead.** Written S145 (2026-09-02), adversarially
reviewed and repaired in the same session and again at S146 (below). The plan is the session's one deliverable
(`starter-kit/SESSION_RUNNER.md` Phase 2 §Planning Sessions; FM #18). It is the fourth and last
payload of [`upstream-read-set-pr-plan.md`](upstream-read-set-pr-plan.md) §5 — **Phase 3, "the gate"**,
shipped in this fork at S129 and never carried upstream. PRs 1–3 of the series are merged into
`KJ5HST/methodology:read-set-budgets` ([#76](https://github.com/KJ5HST/methodology/pull/76),
[#77](https://github.com/KJ5HST/methodology/pull/77), [#78](https://github.com/KJ5HST/methodology/pull/78));
`upstream/main` has received none of them and stands at `512c2ed`.

**Base: `cea3068`** — the tip of `read-set-budgets` after #78 merged (2026-09-03T02:04Z, a
2026-09-02 evening session locally). `tree(cea3068) == tree(2c30d0f)`, the tree PR 3 was measured
on. Nothing else is in flight on that branch, so PR 4 needs no stacking.

Every number below was **measured this session** in a clean clone of `cea3068`, never predicted, and
the command that produced it is in §8. Where the plan cannot measure — the maintainer's machine, the
network — it says so by name. **The first draft was frozen at `5394079` and attacked by eight
independent read-only reviewers** (five refuters over disjoint claim slices, three critique lenses):
97 claims confirmed, 28 refuted, 2 unverifiable, 32 findings. Every refutation and every HIGH/MEDIUM
finding is repaired below; the ones that changed the design are named in §4. **A second round ran at
S146 (2026-09-03) against the frozen close-out tree `67982cc`** — eight read-only slices, then one
independent skeptic per refutation, per HIGH/MEDIUM finding and per unclosed round-1 item — 45 agents in
all (8 + 37; the run is logged in the S146 receipt and ledger entry): 120 claims re-derived
(102 confirmed, 17 refuted, 1 unverifiable); of round 1's 59 items 53 fixed, 5 partial, 1 not; 19 new
findings (1 HIGH, 9 MEDIUM, 9 LOW); 36 of the 37 adjudications stand and one was overturned (the claim
that the round-1 repair dropped nothing — it had dropped Phase C's post-push read-back, restored below).
Every standing item is repaired in this draft; the four that reached a decision are in §4's ratification
record.

---

## 0. The answer, in one paragraph

**The file port is clean by construction, and the record saying otherwise is corrected in §1.1.**
Upstream's `starter-kit/context_budget.py` is blob `be2721a5`, unchanged since `14bd88a` (v3.7, PR
#66), and that same blob is the exact ancestor of the fork's seven commits on the path. The
path-restricted end-state patch applies to it; so do the seven per-commit patches, in sequence, ending
at the fork's blob `c5ff15e5` (§8, R3). **What is hard is everything coupled to the file.** The fork's
tool **refuses to run without a root `.context-budget.json`** (exit 3, *"refuses to invent budgets for
a project that has not declared them"* — the maintainer's own 1.0.0 behaviour, unchanged), the
canonical repo upstream has none, and the distributed seed dropped in as that config is red on day
one for reasons unrelated to this series. So PR 4 must **author the canonical root config**, and that
config — not the code — is the decision this plan puts in front of the operator. A candidate is
shipped beside this plan as [`pr4-candidate.context-budget.json`](pr4-candidate.context-budget.json),
and it was run on `cea3068`: bare exit **2** with `(read-set total) 67,581 B / 56,750 B over` — the
10,831 B the series exists to make visible; **0** config defects; `--selftest` **52 PASS / 0 FAIL**;
the 116-test module **OK, 2 skipped**; `--precommit` refuses growth (+2 B, or a 52 B ledger entry on `CHANGELOG.md`) on every one of the five
over-or-pinned files and passes every shrink; `bin/tests.sh` **115 passed / 1 failed** against a
control of **114 / 1** — 115 shared rows, one added, zero flips, measured on the shipped config and
re-measured at S146. **Two things the review
changed:** the PR's own upstream ledger entry is one the shipped gate refuses by hand once a config exists (exit 3 before it, 2 after), and upstream's
own pre-commit hook wants a ledger line on every commit, so both commits carry one (D4, reshaped at S146); and the trimmer the first draft named as the ledgers' remedy does
not fire at their sizes, so the remedy is now a named command (D1).

---

## 1. The target, and one correction to the record

### 1.1 What the receipts said, and what is true

Six live receipts carry the phrase *"no clean starting point"* about this payload — S136, S140,
S141, S142, S143 and S144, each in its `next_steps` (`HANDOFFS.md` `:316`, `:236`, `:216`, `:172`,
`:129`, `:89` at `5394079`). S143 says *"the only payload with no clean starting point"*. S144 says *"the
one payload S141 called 'with no clean starting point'"* — attributing to S141 a phrase S136 wrote
first — and alone adds the gloss *"the two versions diverged rather than one being a prefix of the
other, so there is no single commit to port."* **The file half of that gloss is false, and the tree
half is true — the sentence conflated them.**

| Claim | Measured |
|---|---|
| the two versions diverged | **No.** `git rev-parse upstream/read-set-budgets:starter-kit/context_budget.py` = `be2721a5` = `14bd88a:…` = `upstream/main:…`. The fork's history on the path is **linear from that blob**: 7 single-parent commits, no merge, ending at `c5ff15e5`. Upstream's copy is a strict ancestor of the fork's, not a sibling. |
| no single commit to port | **True, and irrelevant to the file.** The seven fork commits touch other files too (`bin/tests.sh`, both dashboard twins, `methodology_trim.py`, `CHANGELOG.md`); *those* trees diverged. The path-restricted patches apply cleanly (§8, R3). |
| ~2.5× size difference | **True**: 29,549 B → 73,014 B (2.47×), 674 → 1,400 lines, `VERSION` `1.0.0` → `1.2.0`. |

Nobody ran `git rev-parse` on the two blobs across six receipts. Recorded here, sha-qualified, so the
next reader does not inherit it.

### 1.2 What PR 4 is for

`upstream-read-set-pr-plan.md` §3.4 and §5 Phase 3: **per-file ceilings on the Phase 0 read pair,
then a class total whose ceiling is a partition of the read cap, enforced in `precommit()` as well as
reported in `main()`**, with the two shipped defects beneath it repaired (a gate that measured short
and raised on non-UTF-8 content; a `KeyError` on any config without `classes`). Read that plan's §9
before quoting §3.4 — S129 refuted three of its claims while shipping it.

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
| `starter-kit/context_budget.py` | 29,549 B · 674 lines · blob `be2721a5` · `VERSION = "1.0.0"` | 73,014 B · 1,400 lines · blob `c5ff15e5` · `VERSION = "1.2.0"` | 922 changed lines (824 + / 98 −); 1,088-line patch |
| `tools/test_context_budget.py` | **absent** | 1,311 lines · 116 tests · 13 classes | new file; four fork-relative identifiers to scrub (D9) |
| `.context-budget.json` (root) | **absent** | 29,813 B, calibrated to *this fork's* files | **do not port**; §3.3 |
| `.context-budget-history.jsonl` | **absent** | tracked measurement series | **do not port**; D3 |
| `bin/tests.sh` | `== Test: context_budget.py ==` block at `:591` | `== Test 35: … ==` | **block bodies are byte-identical** except the heading line; the fork has one 9-line unit-test wiring block (`:263-271`) upstream lacks |
| `bin/_manifest.py` | tool row `:46`, seed row `:52` | same rows; +2 placement comments; different `SEED_FORMAT_MARKERS` | **no change** — the comments and the marker change are fork doctrine |
| `starter-kit/context-budget.json` (SEED) | 3 files, `resident` total 34,000, no `read_cap_tokens` | +6 lines: `read_cap_tokens` + its note, `max_tokens` on two entries, a `_max_tokens` note on `LEARNINGS.md` | port (§3.5) |
| `.gitignore` | 5 lines | same 5 + **7** comment lines (`:3-9`: three about `dashboard_history.jsonl`, four about the budget history) | port the comments (§3.6) |

Line numbers into upstream files are **pre-patch**; the wiring block shifts everything after `:244`
down by 9 lines (the CB block heading moves `:591` → `:600`).

### 2.2 The files the canonical config budgets, sized on `cea3068`

Bytes: `git cat-file -s cea3068:<path>`. Lines: `git show cea3068:<path> | wc -l` — the tool reports
**one more** for every file here (`len(text.split("\n"))`, `context_budget.py:347-349`, keeps the empty
string after the final newline, and every file listed ends in one), but the ceiling check (`context_budget.py:366`) is a strict `>`, so `max_lines: 200` fires at `wc -l`
200, when the tool counts 201. One unit per column, the tool's count in parentheses:

| File | Bytes | Lines | Against |
|---|---|---|---|
| `CLAUDE.md` | 59,168 | 126 (tool 127) | seed resident 28,000 / class 34,000 → **over by 31,168 / 25,168** under the seed; pinned at 59,168 (D2); `max_lines` 200 → green |
| `starter-kit/SESSION_RUNNER.md` | 52,195 | 390 (tool 391) | partition ceiling 41,364 → **over by 10,831** |
| `starter-kit/SAFEGUARDS.md` | 15,386 | 242 (tool 243) | pinned at 15,386 → **at ceiling** (`new > ceil` is strict); blob `f0964195` on both trees |
| read-set pair | **67,581** | | derived class ceiling 56,750 → **over by 10,831** |
| `CHANGELOG.md` | 91,365 | 1,028 (tool 1,029) | 65,536 → over by 25,829; ≈37,028 tok at the measured 2.4674 B/tok, over the 25,000 cap |
| `HANDOFFS.md` | 70,182 | 226 (tool 227) | 65,536 → over by 4,646; ≈29,677 tok at 2.3648 B/tok, over the cap (at the seed's 2.93 it would read 23,952, under — which is why the measured density is carried) |
| `starter-kit/FRAMEWORK_LEARNINGS.md` | 56,673 | 79 (tool 80) | on-demand 73,728 → ok; blob `b21854cc`, the exact blob the fork's density was measured on (D7) |
| `FRAMEWORK_APPARATUS.md` / `ITERATIVE_METHODOLOGY.md` / `README.md` / `HOW_TO_USE.md` / `starter-kit/BOOTSTRAP.md` | 15,493 / 55,976 / 74,636 / 55,528 / 28,211 | | not budgeted — read on demand, by humans; listed in the config's `_deliberate_exclusions` |

Structure witnesses the config's `structure` patterns need, counted on `cea3068`: **39**
`### YYYY-MM-DD · [` entries in `CHANGELOG.md` (≥ 5), **10** ` ```handoff ` fences in `HANDOFFS.md`
(≥ 1), **1** `## Versioning` in `CLAUDE.md` (≥ 1, at `:92`), **46** table rows in
`FRAMEWORK_LEARNINGS.md` (≥ 5).

### 2.3 The behaviours that forced the design — each one run, not read

| Probe | Setup | Result |
|---|---|---|
| **A** | fork tool + fork test module dropped onto pristine `cea3068`, **no root config** | `Ran 116 tests … FAILED (failures=1, skipped=2)`. The one failure: `TestToolInvariants.test_the_tool_and_its_selftest_agree_the_gates_all_fire` (`tools/test_context_budget.py:468`), *"0 not greater than 30 : selftest row population collapsed"* — it runs `--selftest` with `cwd=REPO`. |
| **A′** | `python3 starter-kit/context_budget.py --selftest` at that root, no config | **exit 3**, *"no .context-budget.json found at or above … This tool refuses to invent budgets for a project that has not declared them."* Zero rows. Same message and exit from the upstream 1.0.0 tool. **This is why the config is in the PR and not left to the maintainer.** |
| **B** | the distributed SEED copied to `cea3068`'s root as the config | **exit 2**, four red lines from three causes: `CLAUDE.md 59,168 B / 28,000 B over`; its derived token ceiling (verbatim: `≈20,193 tokens exceeds the 12,334-token ceiling by 7,859 — at 2.9300 B/token (config), derived from max_bytes at the 2.27 floor`); `(resident total) 59,168 / 34,000 over`; *"the budget:protected fence is missing"* — printed in the order byte, token, fence, resident total. None of it about the read-set. `upstream-read-set-pr-plan.md` §3.4 predicted this. |
| **C** | fork tool vs upstream tool, each run in an empty adopter dir holding the **unchanged upstream seed** and only a 954 B `CLAUDE.md` (the fence plus 900 `y`, `bin/tests.sh:613-614`'s fixture) | whole-stdout byte-identical, same exit. **A reviewer showed this fixture cannot exhibit the changes** — two of the seed's three files were absent. Superseded by C4. |
| **C4** | same, with a seed-compliant `SESSION_NOTES.md` (one `## ACTIVE TASK`, two `## ` headings, 304 lines by `wc -l` — `305 ln` as the tool counts — lines < 280 B) at four sizes and a `LEARNINGS.md` | **Two adopter-visible changes.** (1) When nothing fires, the read-mandated row reports **bytes, not lines**: `305 ln / 400 ln ok` → `60,048 B / 120,000 B ok`; exit unchanged (1). (2) Above **73,252 B** — the first size whose truncated estimate `int(bytes / 2.93)` exceeds 25,000 tokens is **73,253 B** (≈25,001 tok; `:386` truncates, `:391` compares strictly; 73,250–73,252 B still `ok`) — the new tool derives a token ceiling the old tool never had: `72,948 B` → identical verdicts, exit 1 both; `73,548 B` → old `ok`, exit **1**; new `≈25,101 tok / 25,000 tok over`, header `UNMEASURED` → `OVER`, exit **2**. A compliant file under every ceiling the adopter declared goes red on sync. Disclosed in Appendix B. |
| **D** | the candidate config (§3.3, Appendix A) on `cea3068` with the fork tool | §3.3 — the numbers in §0. |

### 2.4 Who has the tool today

Three sibling projects on this machine carry `context_budget.py` (the population S129 called *"the
three instrumented adopters"*, inferred there and stated here):

| Adopter | Blob | Bytes | = fork commit | `bin/status` (default `--source=local`) |
|---|---|---|---|---|
| `chat_verification` | `be2721a5` | 29,549 | upstream's `14bd88a` | 7 versions behind |
| `wsfct` | `be2721a5` | 29,549 | upstream's `14bd88a` | 7 versions behind |
| `vscode_quarto_ext` | `73fb90aa` | 41,986 | `6a91660` (2026-08-15, the BL-38 repair) | 6 versions behind, **unmodified** |

**The first draft called `73fb90aa` "a locally modified or hand-copied intermediate" that "matches no
commit in this repository's history". That was false, and the cause was a shell bug, not the
adopter:** in `zsh`, `$c:starter-kit/context_budget.py` applies the `:s` history modifier to `$c`, so
every `git rev-parse` in the enumeration received the mangled argument `<sha>/context_budget.py`, exited
128 with `fatal: ambiguous argument` on stderr and the mangled path on stdout, and the trailing
`grep 73fb90aa` matched nothing — loud on stderr, empty only where it was read. Written as
`${c}:starter-kit/…` the loop finds it at once (§8, R2). The same bug had already bitten the blob-identity
check earlier in the session and was caught there; it was not caught here until a reviewer re-ran the
loop. None of the three adopters is at `c5ff15e5`; all three reach it only after `read-set-budgets`
merges to `main` and they sync (`bin/sync --source=github` reads `main`).

---

## 3. What PR 4 carries, file by file — and what it does not

### 3.1 `starter-kit/context_budget.py` → blob `c5ff15e5`, byte-identical to fork `main` (since S148: `d91677b5`, after the comment-only `22c6cf0` and `544cfb0`)

**Ship the end state, not a replay.** Verified (§8, R3): the single path-restricted patch
`git diff 14bd88a main -- starter-kit/context_budget.py` applies to `be2721a5`; the seven per-commit
patches also apply in sequence, each intermediate blob equal to that commit's own. The DONE criterion
is the blob, not the patch: `git rev-parse <branch>:starter-kit/context_budget.py` = `c5ff15e5…` — **re-stated at S148 as `d91677b5…`**, fork `main`'s blob after `22c6cf0` and `544cfb0` reworded eight comment lines for the port (size and line count unchanged, so the symbol numbers below hold for both blobs).

**Why not seven commits (refuted):** every intermediate state fails the fork's test module — it tests
features the intermediates lack, config or not (`73fb90aa`: 14 failures, 49 errors) — and the end state
fails until the root config exists (Probe A′), so a 7-commit replay is either 7 red intermediate states or the config
landing first against a tool that does not yet read half its keys. The series' convention is 1–3
commits per PR (#76: 1, #77: 1, #78: 3). The fork's history stays citable from the PR body.

What the end state carries, **re-derived from each commit's path-restricted diff** (`git diff <c>^ <c>
-- starter-kit/context_budget.py`), not from its whole-repo message — the first draft attributed three
changes to the wrong commits by reading the messages:

| Fork commit | Date | What it did to the tool |
|---|---|---|
| `6a91660` | 2026-08-15 | **BL-38, five defects.** D1 `size_history()` walks `--first-parent` (two lineages interleaved by date after a sync, so "size at T" stopped being a function); D2 ISO stamps compared as aware datetimes (`parse_iso`, `_ISO`), not strings; D3 `calibration_verdict()` + `MIN_R2 = 0.50` refuse a fit below R² 0.50, a negative slope, an undefined R² — and a refused fit **suppresses** the bytes/token line; D4 `ledger_dimension()` names the ceiling that fired in its own unit; D5 remediation prose stops naming the home project. `linfit` extracted. **`VERSION` 1.0.0 → 1.1.0.** Effect at n=76: 14.75 B/tok at R² 0.05 → 2.81 at 0.81. |
| `84abc60` | 2026-08-26 | 7 lines: the `ledger_dimension()` docstring stops asserting the read cap is line-denominated. |
| `9e71f83` | 2026-08-26 | 42 lines: `ledger_dimension()`'s nothing-fired default flips lines → bytes; the docstring and two selftest checks follow (one rewritten to expect bytes with nothing fired, one added to prove a `lines` finding still reports lines). The line-rate deletion this commit is known for happened in the dashboard twins and the trimmer, **not in this tool** — `READ_CAP_LINES` never existed here. |
| `28a02a6` | 2026-08-29 | **Ceilings denominated in tokens, gated by class.** `READ_CAP_TOKENS = 25_000`, `MIN_BYTES_PER_TOKEN = 2.27`, `WHOLE_READ_CLASSES`, `DENSITY_DRIFT_WARN`; `file_density()` (per-file measured beats the config global beats the floor, and returns its source), `token_ceiling()` (explicit `max_tokens` governs; else derived from `max_bytes` at the 2.27 floor; **clamped at the cap either way**), `config_defects()` (a declared `max_tokens` above the cap is reported as a defect — the clamp is never *silent*) — defined and unit-tested, **not yet called**. `VERSION` 1.1.0 → 1.2.0. |
| `9999410` | 2026-08-30 | `blob_bytes()` via `git cat-file -s` — the old path — in effect `len(stdout.strip().encode())` — was at least 1 B short on LF content (`.strip()` removes every trailing whitespace byte, so 1 B is the floor of the error, as the fixture's own docstring at `tools/test_context_budget.py:828-829` says), **1 + (number of CRLF line endings)** short on CRLF (3 B on the two-line fixture at `tools/test_context_budget.py:824-838`), and **raised `UnicodeDecodeError`** on non-UTF-8; `class_spec()` replaces two `cfg["classes"]["resident"]` accesses that raised `KeyError`. |
| `beffbd0` | 2026-08-30 | **The class-aggregate gate**: `READ_CAP_BYTES` computed at import; `class_totals()` over N classes, called from `main()` and `render()`, with `precommit()` summing staged/HEAD bytes per class inline and sharing only `class_ceiling()` with them; `framework_share()`, `class_ceiling()` with `derive_from_read_cap`; `read-set` joins `WHOLE_READ_CLASSES`; **`config_defects()` gains its first call sites** (`main()`, `precommit()`). |
| `c9c9b7b` | 2026-08-30 | Ten reviewed defects in the above — chiefly **a commit contains the index, not the worktree**: `precommit()` is index-driven and reads `HEAD:.context-budget.json` for its baseline, so a `git rm` or rename of a member is a shrink, not a refusal; the test module's call-site guard narrowed so it no longer matches its own comment. |

Symbols, at blob `c5ff15e5` (navigate by `grep -n 'def <name>'`; these numbers are true of that blob
only): `file_density` `:99`, `token_ceiling` `:112`, `class_spec` `:128`, `framework_share` `:139`,
`class_ceiling` `:166`, `class_totals` `:178`, `config_defects` `:225`, `blob_bytes` `:285`,
`find_root` `:307`, `load_config` `:315`, `append_history` `:506`, `render` `:581`,
`ledger_dimension` `:672`, `MIN_R2` `:722`, `size_history` `:759`, `calibration_verdict` `:837`,
`calibrate` `:855`, `install_hook` `:968`, `precommit` `:1000`, `selftest` `:1106`, `main` `:1314`.
Exit codes `CLEAN, WARN, BREACH, USAGE = 0, 1, 2, 3` (`:49`) — **unchanged from upstream** (`:48`).

Added since upstream: **14** top-level `def`s (`blob_bytes calibration_verdict class_ceiling
class_spec class_totals config_defects file_density framework_share ledger_dimension linfit parse_iso
size_at size_history token_ceiling` — `size_at` hoisted from a nested def inside `calibrate`), **7**
module constants (`_ISO DENSITY_DRIFT_WARN MIN_BYTES_PER_TOKEN MIN_R2 READ_CAP_BYTES READ_CAP_TOKENS
WHOLE_READ_CLASSES`), one `def` removed (`cfg_lookup`). Config keys newly read: `read_cap_tokens`,
`max_tokens`, `bytes_per_token` (per file at `:103`, and as the config-global fallback at `:106`),
`measured_bytes`, `adopter_reserve_bytes`, `derive_from_read_cap`. **Every one of them defaults when
absent** — `read_cap_tokens` to `READ_CAP_TOKENS` (`:118`, `:229`; at `:161` the same default arrives as `READ_CAP_BYTES` through a `None` check) — which is why Probe C4's
first two sizes are verdict-identical.

### 3.2 `tools/test_context_budget.py` — canonical-only, 116 tests

Its own docstring: *"CANONICAL-ONLY. Not in bin/_manifest.py, so adopters do not receive it."* Same
disposition as `tools/test_methodology_trim.py`, which #77 shipped. Sets `sys.dont_write_bytecode`
(`:44`) so it leaves no `starter-kit/__pycache__`.

**It needs almost nothing from this fork — the opposite of PR 2's experience.** Every fixture is a
scratch git repository built in `tempfile` (`git()` helper `:55`). Four tests read something else:

| Test | Reads | On `cea3068` |
|---|---|---|
| `TestToolInvariants.test_the_tool_and_its_selftest_agree_the_gates_all_fire` (`:468`) | a root `.context-budget.json` — it runs `--selftest` at `REPO` | **FAILS without the config** (Probe A), **passes with the candidate** (Probe D). |
| `TestFitGateEndToEnd` ×2 (`:330`; `:356`, `:362`) | *this repository's* session transcripts under `~/.claude/projects/<slug>/*.jsonl` **and** a root config | **skip** in the clean clone — by design, its docstring says *"Skipped is honest."* **On this fork, on this machine, both RUN and pass** — recorded at S146 (2026-09-03): `python3 tools/test_context_budget.py -v > u.log 2>&1; echo $?` → 0, `Ran 116 tests … OK`, both `TestFitGateEndToEnd` rows `ok`, no skips (87 transcripts under `~/.claude/projects/-Users-rmsharp-Development-methodology`). |
| `TestReserveIdentity.test_it_agrees_with_the_trimmer_which_computes_it_the_same_way` (`:1230`; class `:1222`) | `starter-kit/methodology_trim.py` source carrying `READ_CAP_BYTES = int(READ_CAP_TOKENS * MIN_BYTES_PER_TOKEN)` | **passes** — #77 put that line upstream at `:129`. |

**The two skips are a surface this plan cannot verify (Learning #13), and they can fail for reasons that
are not defects.** On the maintainer's machine the slug resolves to *his* checkout path; if
`~/.claude/projects/<that slug>/*.jsonl` exists, both tests **run** against his transcripts and the
candidate config's `calibrate_against`. `calibrate()` (`:855`) returns `WARN` **without** the *"no
constant recommended"* line for three reasons, each printing its own line: fewer than 3 first-parent
commits touch the `calibrate_against` file (`:880-882`; not live on `cea3068`, which has 38), fewer than
4 transcripts carry a parseable opening timestamp, a usage record **and** a recorded size at that moment
(`:922-924` — sessions opened before the file's first first-parent record are dropped), or the file was
the same size at every usable session (`:926-928`, `linfit` returns `None`) — and under any of them
**both** tests fail: one wants that line, the other wants `CLEAN` and a `bytes/token` line. A fitted
slope ≤ 0 or an undefined R² (opening context that never varied) fails the second alone. None of that
is the tool. Appendix B names the two tests, the causes, and the diagnosis command — which must read the
`AssertionError:` line, because the tests capture `calibrate()`'s stdout (`_run`, `:349-354`) and the
tool's own diagnosis appears only inside it.

**Four fork-relative identifiers ship in the module and must be scrubbed (D9):** `BL-38` at `:8` and
`:288`, `S129` at `:561`, `S119` at `:613`. Each names a record in a repository the maintainer does not
have; S142 scrubbed two such numbers from PR 3 as a recorded step. After the scrub the module's blob
differs from fork `main`'s by exactly those four lines — the DONE criterion says so rather than
claiming byte-identity. *(S148: six lines — row 1 of the fix-round re-pointed `:9` and `:13` at the
unnumbered upstream block — and the fork's copy itself changed in `22c6cf0` and `544cfb0`, six
vocabulary lines the branch carries identically.)*

### 3.3 The canonical root `.context-budget.json` — the decision

**Design: pin what is over, derive what the series is about, declare what Phase 0 reads, and mark
every number the maintainer may move as a PROPOSAL.** The candidate is Appendix A /
[`pr4-candidate.context-budget.json`](pr4-candidate.context-budget.json) (17,934 B). It is the fork's
config with every fork-specific measurement removed or re-labelled and every ceiling re-derived from
`cea3068`. The review's *what-was-lost* lens found the first draft had dropped design intent the
fork's config carries; the second draft restores it (marked ↺ below).

| Entry | Value | Derivation | Day one |
|---|---|---|---|
| top-level `_` | prose | this repo's own budget; the tool lives in `starter-kit/`; **do not run `install-hook` here** — on a fresh clone (`core.hooksPath` unset) it *installs* `.git/hooks/pre-commit` exec'ing `<root>/context_budget.py`, which does not exist here, and **every commit then fails** with `can't open file`; recover with `rm .git/hooks/pre-commit`; with `core.hooksPath=.githooks` set it declines instead. The gate is measuring-only until chained. Exit 3 without a config is the tool's own 1.0.0 behaviour | — |
| `_precommit_scope` ↺ | prose | `--precommit` sizes the index against HEAD and **evaluates neither `structure` nor `max_lines`**; bare/`--json` runs do, create the history file on the first run and append only when the measurement changes | — |
| `read_cap_tokens` | 25,000 | the Claude Code Read tool's own refusal message (*"exceeds maximum allowed tokens (25000)"*), first observed 2026-08-26 (S111) and re-confirmed 2026-09-03 on Claude Code 2.1.259; equals the tool's module default; **upstream's seed does not carry this key** — the +6-line seed edit in this PR introduces it. If the harness differs, set it and every derived ceiling follows | — |
| `bytes_per_token` 2.93 · `fixed_harness_tokens` 35,700 · `growth_run` 10 | seed values on `cea3068` | inherited, labelled; `--calibrate` **proposes and writes nothing** | — |
| `classes.resident.total_bytes` | 59,168 **PROPOSAL** | pinned = `git cat-file -s cea3068:CLAUDE.md`; one-file class; ↺ *not* an identity check (a second resident file would be seen); ↺ agent memory excluded, per-operator | ok, at ceiling |
| `files[CLAUDE.md]` | `max_lines` 200 ↺ · `max_bytes` 59,168 · `structure` `^## Versioning` ≥ 1 | 200 is `starter-kit/BOOTSTRAP.md:198`'s *"roughly 200 lines"* — the framework's own published number, green at 126 lines; no `warn_bytes` (a warn under a pin at current size fires on every run); no `protected_fence` (the file has none) | ok |
| `classes.read-set` | 56,750 derived, `warn_bytes` 51,000 | `READ_CAP_BYTES − adopter_reserve_bytes`, computed at run time; a written value that disagrees is a config defect; ↺ why a class separate from read-mandated; ↺ **the aggregate arm cannot fire before a per-file arm on this config** — the two ceilings partition the total exactly — so it is redundant by construction today and its witness is the shipped `--selftest`, not this repo's rows; `warn_bytes` 51,000 is inert while the class is over (`over` shadows `warn`, and the class arm in `precommit()` reads only the ceiling) — labelled so in the config (D10) | **over by 10,831** |
| `files[starter-kit/SESSION_RUNNER.md]` | 41,364 | 56,750 − 15,386, the partition; identical to the fork's row | **over by 10,831** — the ratchet |
| `files[starter-kit/SAFEGUARDS.md]` | 15,386 **PROPOSAL** (the split) | pinned; blob `f0964195` on both trees | at ceiling |
| `files[CHANGELOG.md]` / `files[HANDOFFS.md]` | `read-mandated`, 65,536 B **PROPOSAL**, 25,000 tok, `bytes_per_token` **2.4674 / 2.3648** ↺ | the fork's ledger ceilings since 2026-08-15, **decoupled from the trimmer since 2026-08-26** (D1); densities measured on the fork's ledgers 2026-08-29, same format — carried so the token arm is load-bearing (at the seed's 2.93, `HANDOFFS.md` would read *under* the cap) | **over**, byte and token arms both |
| `files[starter-kit/FRAMEWORK_LEARNINGS.md]` ↺ | `on-demand`, 73,728 B **PROPOSAL**, `bytes_per_token` 2.8897, row-shape `structure`, **no `max_tokens`** | D7: measured 2026-08-29 on blob `b21854cc` — the exact blob `cea3068` carries; the derivation upstream's `bin/check-learnings:87-89` already points at; caveat: at 2.8897 the ceiling sits 1,486 B above the one-read cliff (72,242 B) | ok |
| `_deliberate_exclusions` ↺ | prose | the five on-demand files with `cea3068` sizes | — |
| `synced` | `[]` | this repo *is* the canonical | — |

**Measured on `cea3068` with the fork tool (Probe D, the shipped third draft — every key the tool evaluates — all but the `_` prose and the `why` strings — is identical to config v2, on which `39c81ab` measured) —
the box and the finding lines; the full stdout is 49 lines, the rest being the five-item remedies block
(Move / Compute / Archive / Delete / Raise the ceiling — the list `--precommit` labels *Cheapest legal
actions*; the bare run prints it unlabelled) printed under each of the **four byte-ceiling** findings;
the two token-ceiling findings print none, because `REMEDIES` has no `tokens` key:**

```
context budget  OVER   resident 59,168 B ≈ 20,194 tok
file                                      size     ceiling  status
CLAUDE.md                             59,168 B    59,168 B  ok
starter-kit/SESSION_RUNNER.md         52,195 B    41,364 B  over
starter-kit/SAFEGUARDS.md             15,386 B    15,386 B  ok
CHANGELOG.md                          91,365 B    65,536 B  over
HANDOFFS.md                           70,182 B    65,536 B  over
starter-kit/FRAMEWORK_LEARNINGS.md    56,673 B    73,728 B  ok
(read-set total)                      67,581 B    56,750 B  over
resident total 59,168 B / 59,168 B ceiling   growth run 0/10
read-set total 67,581 B / 56,750 B ceiling  over

starter-kit/SESSION_RUNNER.md — 52,195 B exceeds the 41,364 B ceiling by 10,831
CHANGELOG.md — 91,365 B exceeds the 65,536 B ceiling by 25,829
CHANGELOG.md — ≈37,028 tokens exceeds the 25,000-token ceiling by 12,028 — at 2.4674 B/token (measured)
HANDOFFS.md — 70,182 B exceeds the 65,536 B ceiling by 4,646
HANDOFFS.md — ≈29,677 tokens exceeds the 25,000-token ceiling by 4,677 — at 2.3648 B/token (measured)
(read-set total) — 67,581 B across the read-set class exceeds the 56,750 B ceiling
```

exit **2** (the header rounds — `≈ 20,194 tok` — where finding lines and `--json` truncate to 20,193); **0** occurrences of *defect*; `--json` reports `config_defects: []`; `--selftest` **52 PASS
/ 0 FAIL, exit 0**; the unit module **116 run, OK, 2 skipped**. The `--precommit` matrix, each case
staged against a commit holding the candidate, exit read bare on the next line (the "+2" is `x\n`). A
growth refusal on a class member prints **two** rows — the file row and then the class row beneath it
(`(read-set total) 67,581 -> 67,583 B ceiling 56,750 B`, `(resident total) 59,168 -> 59,170 B ceiling
59,168 B`) — because the class grew too; the table quotes the file row:

| Staged change | Exit | Output |
|---|---|---|
| `SESSION_RUNNER.md` +2 B / −5,000 B | **2 / 0** | `REFUSED … 52,195 -> 52,197 B ceiling 41,364 B`; the shrink passes while still 5,831 B over |
| `SAFEGUARDS.md` +2 B | **2** | `15,386 -> 15,388 B ceiling 15,386 B` — the pin holds at exactly the size |
| `CLAUDE.md` +2 B / −3,000 B | **2 / 0** | the ratchet on the resident file |
| `CHANGELOG.md` + one 52 B ledger entry / −5,000 B | **2 / 0** | `91,365 -> 91,417 B ceiling 65,536 B` — **see D1 and D4** |
| `HANDOFFS.md` +2 B / −1,000 B | **2 / 0** | |
| `FRAMEWORK_LEARNINGS.md` +2 B | **0** | under its ceiling |
| `README.md` +2 B (unbudgeted) | **0** | |
| `CLAUDE.md` with `## Versioning` → `## Version` (−3 B) | **0** | **`--precommit` sees neither structure nor `max_lines`** (a 250-line, 512 B `CLAUDE.md` passes it and the bare run reports `251 ln / 200 ln over`); the bare run on the same worktree exits 2, `CLAUDE.md … instrument-failed` |
| nothing staged | **0** | |

**Not ported from the fork's config, each named:** `docs/planning/BACKLOG.md` (fork-only file);
every `measured_bytes` / `measured_on` (fork sizes) except where the blob is identical; `max_lines`
on the two ledgers (a live guard — Phase B deleted the line *rate*, not the key — left off because the
byte and token arms already fire on both and a third red row on the same two files adds no
information); `warn_bytes` on `CLAUDE.md` (meaningless under a pin); the fork's `_` narrative that
cites fork sessions and BL numbers (rewritten, not dropped — the design sentences are kept).

### 3.4 `bin/tests.sh` — one 9-line wiring block; the test body is already upstream

The upstream `== Test: context_budget.py ==` block (`:591`) and the fork's Test 35 are **byte-identical
apart from the heading line** — install-hook, `core.hooksPath`, foreign-hook, sync-distribution and
seed-clobber assertions are all already there. **Do not renumber or retitle it**: upstream's suite has
26 headings with that block unnumbered after Test 25, and a retitle changes no assertion while
touching a row-for-row baseline.

The one addition goes immediately after the trimmer's wiring (`:240-244`, the `fi` closing
`test_methodology_trim.py`), mirroring how #77 wired the trimmer. **Its comment is adapted from the
fork's `:263-266`, not copied**: the fork's names `BL-38` and `Test 35`, both fork-relative. The fork's own
`bin/tests.sh:263-266` therefore differs from the ported block once PR 4 lands — a fork-side follow-on
beside the D9 back-port (D11).

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

**Measured effect on the suite** (§8, R6): control `cea3068` **114 passed / 1 failed**; the candidate
(the shipped config) **115 / 1** — 115 shared row labels, exactly one row added (`context budget gate
unit tests green`), zero status flips; re-measured at S146 on fresh clones with the same result. The one
failure on both sides is Test 9, `github source dry-run failed`: `bin/sync`'s `read_github()` (`:80-86`)
passes no `ref`, so `--source=github` reads `KJ5HST/methodology:main`, where three manifest sources are
still absent — `starter-kit/FRAMEWORK_LEARNINGS.md` (#76), `starter-kit/methodology_trim.py` (#77),
`FRAMEWORK_APPARATUS.md` (#78). The log names only the **first** (`FRAMEWORK_LEARNINGS.md`, HTTP 404)
because `read_github()` exits on the first failure (`:88-90`); do not go hunting for the other two. It
stays red on this branch unless that function grows a `ref` parameter, which this PR does not do;
merging `read-set-budgets` to `main` is expected to clear it (the row also needs the network and `gh`
auth).

### 3.5 `starter-kit/context-budget.json` (the SEED) — +6 lines, port

The fork adds a `read_cap_tokens: 25000` key with its `_` note, `max_tokens: 12334` on the seed's
`CLAUDE.md` entry (= 28,000 / 2.27, exactly what the tool derives when the key is absent),
`max_tokens: 25000` on `SESSION_NOTES.md`, and a `_max_tokens` note on `LEARNINGS.md` explaining why an
on-demand file gets no token verdict. It is **documentation of keys the new tool reads**, distributed
as a seed-once file (`bin/_manifest.py:52`, `SEED`), so it overwrites no existing config. Covered by the
existing `seed .context-budget.json parses as JSON` row. The +6 is `--numstat`'s count: five content
lines and one blank. The seed's `SESSION_NOTES.md` keeps its `max_lines: 400` beside the new
`max_tokens: 25000` — different guards (line count; whole-file read cap), neither subsuming the other —
and its `_` note is not extended in PR 4, so +6 stays +6.

### 3.6 `.gitignore` — seven comment lines, optional but recommended

The fork's `.gitignore:3-9` explains why `dashboard_history.jsonl` and `.context-budget-history.jsonl`
are deliberately **not** ignored. The first bare run of the tool on the canonical repo creates
`.context-budget-history.jsonl` untracked, and without the comment the maintainer meets an unexplained
file. Comments only; no ignore rule changes.

### 3.7 What PR 4 does **not** carry, each named so it is chosen rather than forgotten

| Not carried | Why | Where it belongs |
|---|---|---|
| `starter-kit/methodology_dashboard.py` / `tools/methodology_dashboard.py` | upstream `2.10.7` vs fork `2.17.0`: **ten** fork-only version labels above the base (`2.11.0`, `2.12.0`, `2.13.0`, `2.14.0`, `2.15.0`, `2.15.1`, `2.15.2`, `2.16.0`, `2.16.1`, `2.17.0` — enumerate `DASHBOARD_VERSION` over `git log --full-history main -- starter-kit/methodology_dashboard.py` and subtract the labels reachable from `upstream/read-set-budgets`; the first draft's 7 and a round-2 reviewer's 9 each missed some), of which the read-cap work is 3 (Phase B `2.16.0`, C1 `2.16.1`, C2 `2.17.0`; Phase A bumped nothing); a 1,318-line diff per twin plus 2,841 in its tests | its own PR series. The inconsistency it leaves: upstream's trimmer (#77) and this tool carry `READ_CAP_TOKENS`/`MIN_BYTES_PER_TOKEN`; upstream's dashboard carries **no** read-cap premise at all |
| `.githooks/pre-commit` (+86 lines on the fork) | the Phase 1B claim carve-out and its corpus measurements — fork doctrine | the fork; or a separate proposal |
| `bin/_manifest.py` comments and `SEED_FORMAT_MARKERS` | the marker change is S40 doctrine the upstream seeds do not carry | the deferred documentation PR, if at all |
| `bin/check-handoff` comments naming `.context-budget.json` (`:596`, `:650`) | fork-only checker text | — |
| `starter-kit/BOOTSTRAP.md` ownership table naming `.context-budget.json` adopter-owned (`:355-356`) | upstream's BOOTSTRAP has no such table | the **deferred small PR** (S143, operator-chosen) |
| `.context-budget-history.jsonl` | measurements belong to whoever runs the tool | created by the maintainer's first bare run (D3) |
| the fork's own root config | calibrated to an 11,368 B `CLAUDE.md`, cites fork sessions | upstream gets Appendix A; **the fork keeps its own** (D11) |
| the three deliberately-left defects (two from `upstream-read-set-pr-plan.md` §9's footer, one found at S146) | the growth-run advisory prints *"Nothing is over a ceiling yet"* while files are over — the string is split across a line break at `c5ff15e5:653`, so a one-line grep for it returns nothing; `append_history()`'s change test ignores `class_bytes`; and the exit-3 message `no .context-budget.json found at or above <dir>` prints `os.getcwd()` (`c5ff15e5:1321`, identical in upstream 1.0.0), not the directory `find_root()` stopped at — cosmetic, exit and rows unaffected | follow-ons; all one-line decisions. None changes an exit code, and the advisory needs a 10-run history before it is visible upstream |
| governing-plan **dragon 2** (the bypass reflex: the upstream hook documents `--no-verify`; a budget check chained into it inherits that bypass) | answered in Appendix B as a sentence, not a mechanism | the PR body |
| governing-plan **dragon 3** (bytes moved into a fourth mandatory file evade the aggregate) and its partial mitigation — a `bin/tests.sh` row asserting the filenames Phase 0 orders read in full equal the `read-set` members | not built; the honest split is caught only by a reader | follow-on, named here so it is not lost |
| any edit to `starter-kit/SESSION_RUNNER.md` naming the gate (governing-plan dragon 4) | grows the capped file ~300 B; an operator decision | raised in the PR body as a question |

---

## 4. Decisions for the operator — recommendation first, alternative stated

**Ratification record — 2026-09-03, S146.** Put to the operator as one question after the Phase 0
report, with the ten recommendations and their alternatives tabled: *"All ten as recommended."* Then,
once the second review round had run against the frozen close-out tree `67982cc` (header), the four
items it reopened were put back as separate questions and answered: **D4** reshaped (two commits, each
with a ledger line); **D11** added (the fork keeps its own config); **D2**'s token arm (accept the
derived clamp, document it); **D6**'s residue (the #77 backfill is not in PR 4). **D1–D11 stand as
recorded below.** The six sizes in §2.2 (including both pins) were re-read at ratification with `git cat-file -s` on
`upstream/read-set-budgets` (still `cea3068`) and are unchanged. **What this ratifies:** Appendix A as
the config Phase B copies (after re-checking the pins, §5), with the `_`-key corrections made at S146;
the two-commit shape (D4); the D7 row; the D8 entry shape and date rule; the D9 scrub. **What it
authorizes:** Phase B, as the next session's single deliverable, and nothing more. **What it does not:**
Phases C and D each need their own explicit go-ahead; the version (D5) and the PROPOSAL-labelled numbers
(D10) remain the maintainer's. **D5, the observation half of D6, and D10 are records, not decisions** —
D5 defers the version event, D6 reports upstream's missing #77 entry, D10 lists what the maintainer owns.

**D1 — Declare the two ledgers, or not?** *Recommend: declare them* (as the candidate does). FM #28's
own text says every artifact the protocol mandates reading gets a declared ceiling; Phase 0 step 6
reads the newest receipt and reconciles the ledger every session; omitting the two red rows is the
*Raise the ceiling* remedy in a different coat. **The cost, measured:** while a ledger is over 65,536
B, `--precommit` **refuses every commit that appends to it** (+52 B → `REFUSED`). Today that bites
nobody, because the gate is not wired on the canonical repo; the day someone chains it, no close-out
lands until **the file being appended to** is under ceiling. **The first draft named `methodology_trim.py`
(#77) as the remedy that "fires on its own trigger". It does not:** its `DEFAULT_BUDGET_BYTES` is
**196,608 B** (`:186`, 3× this ceiling), and on `cea3068` `--file CHANGELOG.md --check` reports
*"91,365 B against a 196,608 B budget … trigger does not fire"*, likewise `HANDOFFS.md` at 70,182 B.
The fork decoupled the two numbers on 2026-08-26 and its own config says so; the first draft dropped
that sentence. The remedy is `python3 starter-kit/methodology_trim.py --file <ledger> --budget-bytes
65536` (dry-run first, then `--write`) on a reconciled tree — the trimmer refuses `[P1_UNDOCUMENTED]`
on a tree whose newest commits have no ledger line — or moving the number. **65,536 B is the fork's
number and needs its own defence; the PR body marks it a proposal.** *Alternative:* omit the ledgers
and let the trimmer's 196,608 B be their only control; the bare run still exits 2 on the read-set.
**Added at S146, measured:** trim `CHANGELOG.md` **first** — a `HANDOFFS.md` trim writes its own P1A
entry into `CHANGELOG.md` (91,504 → 92,284 B, +780 B, on a clone whose `CHANGELOG.md` carried a 139 B
reconcile line so the trimmer's `P1_UNDOCUMENTED` check passed), which the gate refuses while that file
is over; the other order passes both. The trimmer stops at **half** the budget (`BYTE_STOP_FRACTION` 0.5:
91,365 → 30,920 B, 30 of 39 records; 70,182 → 26,891 B, 7 of 10), appends one ledger entry per trim,
warns `[FRONTMATTER_FIELD_ABSENT]` on upstream's `HANDOFFS.md` (its front matter lacks the *retained
receipt count* field the trimmer's `LedgerSpec` declares), and refuses `[P1_UNDOCUMENTED]` on any tree
with commits past the ledger frontier. And its own `--check` names **56,750 B** as the one-read cap, so
65,536 B sits *above* the number the sibling tool prints — part of the defence D1 says the ceiling needs.
**And at the carried densities the token arm binds first:** 25,000 tok × 2.4674 = 61,685 B for
`CHANGELOG.md` and 25,000 × 2.3648 = 59,120 B for `HANDOFFS.md`, both below 65,536 B — the byte ceiling
fires first only if a re-measured density exceeds 65,536 / 25,000 = 2.6214 B/tok (verified at S146:
`CHANGELOG.md` truncated to 62,000 B reports `≈25,127 tok / 25,000 tok over`, exit 2, with no byte row).
The alternative therefore has two shapes: drop `max_bytes` and keep `max_tokens`, or drop both.

**D2 — `CLAUDE.md` at 59,168 B: pin, or seed number?** *Recommend: pin at arrival size*, plus the
framework's own `max_lines: 200` (green at 126 lines). The seed's 28,000 / 34,000 reads `over by
31,168` on day one for a reason unrelated to the read-set, and the target for that file is the
maintainer's. A pin refuses growth today and shrink passes. *(The tool counts 127: `text.split("\n")`
keeps the empty string after the final newline; the check (`:366`) is a strict `>`, so `max_lines: 200` fires at
`wc -l` 200, when the tool counts 201.)* **Token arm,
ratified at S146:** with `max_bytes` set and no `max_tokens`, `token_ceiling()` derives 59,168 / 2.27 =
26,065 tok and clamps it to the 25,000 cap **silently** — `config_defects()` reports a clamp only on a
*declared* `max_tokens` — and the verdict (20,193 tok, `ok`; the header rounds to 20,194) is computed at the seed's 2.93 B/tok —
as are `SESSION_RUNNER.md`'s and `SAFEGUARDS.md`'s, because `read-set` is a whole-read class and neither
declares a density (`--json`: `density_source: config` on all three; derived ceilings 18,222 and 6,777
tok, both `ok` today); at the 2.27 floor `CLAUDE.md` would read 26,065, over.
**Decision: accept the derived clamp and document it** (no `max_tokens` key; the config's `_` keys say
so; re-judge after `--calibrate`). *Alternative:* declare `max_tokens` at arrival (20,193 at 2.93), a
second ratchet whose meaning moves with the density constant.

**D3 — `.context-budget-history.jsonl`: ship, track, or ignore?** *Recommend: ship nothing; port the
`.gitignore` comment; the maintainer commits the file after his first bare run,* as the fork does.

**D4 — Commit shape and ORDER.** *Ratified at S146 as: two commits, in this order, **each carrying a
`CHANGELOG.md` line.*** **(1)** `feat(starter-kit): ship the context-budget gate — token ceilings, class
totals, and the repairs beneath them (read-set budgets, 4 of 4)` — the tool, the scrubbed test module,
the `bin/tests.sh` wiring, the seed, **and the upstream `CHANGELOG.md` entry (D6/D8)**; **(2)**
`chore(budget): declare this repository's own context budget` — the canonical root config, the
`.gitignore` comments, **and one bullet appended to that same entry naming the config** (the #78
precedent: its entry was edited across two of its three commits, `2897983` +3,073 B then `2c30d0f`
+220 B). No fork session or BL number in either message. **The second draft's reason for the order was
refuted at S146 and is replaced.** It said the gate would pass commit (1)'s entry and refuse it once the
config existed. Measured in a clean clone, `--precommit` by hand **exits 3** on commit (1) staged
against `cea3068` with the worktree at commit (1) — no config, nothing evaluated — and **exits 2** on
the same index with the candidate present (`91,365 -> 92,471 B` for a 1,106 B entry; `94,746` for a
3,381 B one); on commit (2) it **exits 2** because of its own ledger bullet (0 without it). The order
buys nothing the unwired gate can see. What forces a ledger line on **both** commits is upstream's own
`.githooks/pre-commit`, which refuses a content commit without `CHANGELOG.md` co-staged (FM #27) — and
without one, commit (2) would be an undocumented commit that Phase 0 step 6 reports and the trimmer's
`P1_UNDOCUMENTED` check refuses on. What the two-commit shape still buys is separability: the policy
file apart from the code. Seven commits is refuted (§3.1). *Alternative, also measured:* one commit
with the entry inside it — by hand the gate exits 2 on it; the policy file and the code are no longer
separable.

**D5 — Version.** Not PR 4's to decide. PRs 1–3 were unversioned feature PRs onto `read-set-budgets`;
the version event, if any, belongs to `read-set-budgets` → `main`. The tool's own `VERSION` moves
`1.0.0` → `1.2.0` inside the file regardless.

**D6 — Upstream ledger entry.** *Follow the series' convention: one `CHANGELOG.md` entry in-branch,
no `HANDOFFS.md` receipt* (#76 `5b92b2f` +6,342 B and #78 `2897983` +3,073 B did this; upstream's
newest receipt is its own S12). **Observation for the operator, not a PR 4 task:** #77 (the trimmer)
left **no** upstream ledger entry — `grep -i methodology_trim` on `cea3068:CHANGELOG.md` finds one
line, `:124`, which `git blame` puts in PR 1's entry (`5b92b2f`); `grep -i trimmer` finds nothing;
`git show --stat 56997af -- CHANGELOG.md` is empty. That is FM #27 on the upstream ledger — and one no mechanism will surface: the frontier-based
reconcile (Phase 0 step 6, and the trimmer's `P1` check) looks only past the last commit that touched
`CHANGELOG.md`, which is `2c30d0f` (PR 3), and `56997af` sits below it. **Decision, ratified at S146:
the #77 backfill is NOT in PR 4.** It is listed under *After D* (§5) with its shape — its own dated
`Backfilled (reconcile-on-read)` heading in its own commit; PR 4's diff stays about the gate. Also for
the record: #78's entry was edited across two of its commits (`2897983` +3,073 B, `2c30d0f` +220 B),
the precedent D4's second commit follows.

**D7 — `starter-kit/FRAMEWORK_LEARNINGS.md`: budget it?** *Recommend: yes, port the fork's row* —
the first draft said no on a reason a reviewer refuted. The fork's `bytes_per_token: 2.8897` was
measured 2026-08-29 on blob `b21854cc`, which is **the exact blob `cea3068` carries** (46 rows, 56,673
B), so "fork measurements do not transfer" was false for this file. And upstream's
`bin/check-learnings:87-89` already says *"the canonical repo's root `.context-budget.json` carries
the long-form derivation"* of its 1,500 B row budget — creating that file without the derivation would
turn a citation to a missing file into a citation to a file that lacks the text. The row carries the
derivation (why per-row: read whole once, in part 243 times over 80 transcripts), the doubled-file
measurement method, and the caveat that 73,728 B sits 1,486 B above the one-read cliff at today's
density. **No `max_tokens`**, by the tool's own on-demand rule.

**D8 — The upstream `CHANGELOG.md` entry, as a checklist** (the first draft pointed at two commits and
gave no format; the second draft's date rule and bullet shape were refuted at S146 and are replaced):
heading `### <date> · [ad hoc] <title>` where `<date>` is the **author date of commit (1) in the
author's local zone**, as the ledger's own entries are dated — #78's (`cea3068:CHANGELOG.md:38`) reads
2026-09-02 for a commit authored 20:33 −04:00, i.e. 00:33Z the next day, and #76's (`:75`) kept its
2026-08-28 author date through a 2026-09-02 rebase — never re-dated on rebase; one source tag,
`[ad hoc]`, matching #76/#78 (the fork commits were BL-tagged; the fork's `BACKLOG.md` does not exist
upstream, though `BL-` identifiers already appear in 16 files there via #76/#77); prepended directly
under the `---` at `cea3068:CHANGELOG.md:36`, above PR 3's entry; bullets in the shape #76 and #78
actually use — **Change:** / **What it buys** / one or more narrative sentence-headed bullets /
**Scanner:**, plus **Verification:** and **Provenance:** as #76 carries (`:138`, `:141`; #78 carries
neither) — *What changes for adopters* is Appendix B's section, not a ledger bullet; no `Model:` bullet
(upstream's ledger excludes it, `:144`). **Before committing anything that lands upstream, grep the
ADDED LINES of the diff, not the whole files:** `git diff cea3068 pr4/… | grep '^+' | grep -v '^+++' |
grep -nE '\bS[0-9]{1,3}\b|BL-[0-9]+'` must print nothing — `CHANGELOG.md` (65 matching lines) and
`bin/tests.sh` (11) already carry such identifiers on `cea3068`, which PR 4 neither touches nor may
scrub. Today the only source of hits is the test module's four (D9); the tool, the candidate config,
the seed's six added lines and the `.gitignore` comments have none. Apply the same regex to both commit
messages.

**D9 — Scrub the four fork-relative identifiers in the test module.** *Recommend: yes.* `BL-38` (`:8`,
`:288`) → *"the 2026-08-15 `calibrate()` repair"*; `S129` (`:561`) and `S119` (`:613`) → their dates
(2026-08-30, 2026-08-27). At `:288` reword the sentence whole — *"The table from the 2026-08-15
`calibrate()` repair is a claim about arithmetic"* — rather than substituting the phrase, or it reads *"The
the …"* (a verifier built it at S146 and saw it). #76/#77 already carry such identifiers upstream — by D8's regex on `cea3068`,
`FRAMEWORK_LEARNINGS.md` has 50 matches on 37 lines (42 S-numbers, 8 `BL-`) and `methodology_trim.py`
28 on 23 (6 S-numbers, 22 `BL-` across BL-9/27/28/32/36/41/52); the second draft's 35 and 5 were line
counts under a narrower, unstated regex — so this is a consistency choice, made visibly, and a weaker
one than it read. Fork-side follow-on: back-port the
four scrubbed lines so the two copies agree.

**D10 — The maintainer's numbers.** **Five** distinct values in the candidate are labelled **PROPOSAL** in
their `_` keys (seven label sites: the `CLAUDE.md` pin is stated twice, the ledger ceiling twice) and
listed in Appendix B: the `CLAUDE.md` pin 59,168 (D2); the ledger ceiling 65,536 on both ledgers (D1,
one decision); the `SAFEGUARDS.md` pin 15,386 that puts all headroom debt on `SESSION_RUNNER.md`; the
`FRAMEWORK_LEARNINGS.md` ceiling 73,728 (D7); and — labelled at S146, after the self-review caught the
plan calling it "inherited" while the config called it a proposal — `read-set.warn_bytes` 51,000, the
fork's own choice (the seed has no read-set class; its `warn_bytes` are 30,000 and 24,000), inert while
the class is over (`over` shadows `warn`; the class arm in `precommit()` reads only the ceiling), so it
informs nobody until the pair is under 56,750 B. **One threshold is inherited rather than proposed:**
`CLAUDE.md.max_lines` 200, the framework's own published number. `calibrate_against` now
carries its own `_` key; `fixed_harness_tokens` is read by nothing in the tool and is carried for seed
parity, and its `_` says so. **`--calibrate` is the maintainer's step after merge; Phase B does not run
it.** The PR body says all of them are his.

**D11 — What the fork does the day PR 4 merges.** *Ratified at S146: the fork keeps its own root
config.* Its ceilings and narrative are its own (the same 65,536 B on ledgers that stood at 202,279 B and
159,483 B on `67982cc`, the round-2 review tree, and grow every session; a `CLAUDE.md` ceiling of 18,600 B,
with `max_tokens` 7,114, calibrated against an 11,368 B file), and nothing changes for the fork on merge day —
its `.githooks/pre-commit` does not chain the gate either. The fork-side follow-ons are fork commits made
**after Phase D and before the next upstream sync**: the D9 back-port of the four scrubbed lines, and
aligning the fork's `bin/tests.sh:263-266` wiring comment with the ported block (§3.4). That sync — a merge, the
fork's usual shape — already conflicts on **17 paths** between fork `main` and `cea3068` with no PR 4 at
all (`git merge-tree --write-tree --name-only`, measured at S146 — the command prints the result tree's OID
first; a draft that counted it said 18: the two ledgers, `CLAUDE.md`,
`README.md`, the dashboards and their tests, `bin/tests.sh` in 5 hunks, and more). PR 4's own share is
**two more, 19 in all**: the add/add on `tools/test_context_budget.py` (4 hunks, the D9 lines) and the
add/add on `.context-budget.json` (the fork's 29,813 B config against the candidate — unavoidable whichever
upstream config lands); the §3.4 block's first two comment lines land inside `bin/tests.sh`'s pre-existing
second hunk against the fork's `:263-264` (the `if/else/fi` merges as shared text), so that file stays at
5 hunks — which is §3.4's point. Resolve PR 4's share by keeping the fork's config and taking upstream's
test module and comment. The §3.7 row for the fork's own
root config now says which repository gets which file. *Alternative:* the fork adopts Appendix A — red on every ledger commit and
mis-pinned on `CLAUDE.md` from day one.

---

## 5. Phases — each one session, each closing at its own STOP

**Phase A — this plan. ✅ DONE at S145; ratified at S146.** *Verification, runnable:* `git cat-file -e
5394079 && git cat-file -e 29054c7 && git cat-file -e 67982cc; echo $?` → 0 (the frozen draft, the
repaired draft and the close-out all exist); `git diff --stat 5394079 29054c7 -- 'docs/planning/pr4-*'`
→ 2 files changed, 517 insertions, 326 deletions (the round-1 repair is real, not a re-label); the S145
receipt in `HANDOFFS.md` and the S146 ratification record in §4. *Verification, not a command:* the two
adversarial rounds named in the header, every refutation re-derived before adoption. *Surface:* this
machine; it cannot verify the maintainer's environment (§3.2). STOP.

**Phase B — Build PR 4 on `cea3068`, verify, do not push.** One session.

**✅ DONE at S147 (2026-09-03) — built and verified in the R1 clone; NOT pushed; fetched into this fork as
the local ref `pr4/context-budget-gate` only.** Head `f3a4b6d` (tree `7541e3ee`): `28406ce` commit (1),
`f3a4b6d` commit (2), both through upstream's `.githooks/pre-commit` with `core.hooksPath` set in the
clone — it refused a first attempt whose edit script had aborted before a ledger line was staged
(Learning #53). Every item of the DONE list below was measured on that tree and matched: blob `c5ff15e5`;
four D9 hunks; `Ran 116 … OK (skipped=2)`, exit 0; `--selftest` 52 / 0; bare exit 2 with `CHANGELOG.md`
at **96,750 B** (+5,385 B, the entry), six findings, `config_defects: []`; the 13-case matrix; by-hand
exits **3 / 2 / 2 / 0**; suite 114/1 → 115/1 (115 shared rows, one added, zero flips; **114/2 at commit (1)
alone** — the wired row is red until the config lands, and that commit's message says so); checkers
0/0/0/0; seven files; both identifier greps empty; PROPOSAL 8; config byte-identical to Appendix A.
*Verification, runnable:* `git rev-parse pr4/context-budget-gate^{tree}` → `7541e3ee…`; `git diff --stat
cea3068 pr4/context-budget-gate` → 7 files. Body: [`pr4-read-set-budgets-body.md`](pr4-read-set-budgets-body.md).
**The self-review (two read-only reviewers, one against this DONE list, one as the maintainer) found
twelve items, every one re-derived by hand, none repaired — each sits inside a ratified artifact** (the
D9 four-line scrub, the verbatim Appendix A, the `c5ff15e5` blob, the §3.6 lines); the decision table is
in the body file's header, and the recommendation is a fix-round before Phase C.

**✅ FIX-ROUND DONE at S148 (2026-09-03) — the six rows applied, one review lens re-run, the branch REBUILT
as `cf15489` (tree `c857734`; `8df8faa` commit (1), `cf15489` commit (2)), every DONE item above re-measured
on the fresh tree and matched again; `f3a4b6d` and the two reviewed intermediates `46089f1` and `c6577f2`
kept under `refs/archive/pr4-context-budget-gate-*`; still NOT pushed.** Fork side first: `22c6cf0` on `main` reworded
six comment lines of the tool and four of the test module and amended the candidate config (row 3); a
maintainer's-eye lens on the first rebuild returned fourteen items, all re-derived, and `544cfb0` reworded
four more sites of the same class (two tool comments, two test comments, the seed's `_read_cap_tokens`);
tool blob `c5ff15e5` → `d91677b5` (73,040 B, size and line count unchanged), so the ported blob stays
byte-identical to fork `main`; then rows 1, 4, 5, 6 inside the branch. A delta lens on the third build
(`c6577f2`) confirmed all fourteen dispositions and returned seven more — two of them false provenance
sentences the rebuild itself had written into commit (1)'s message and the entry (*"eight commits … one
reword"* where it is nine and two; *"every intermediate fails"* where the last two pass) — repaired in the
fourth build together with a `.gitignore` clause and the bullet naming both histories; three disclosed in
the PR body (the module's colliding `D1`–`D5` labels, the 20,193/20,194 rounding pair, the seed naming the
fork). **One row-2 site was left alone on
evidence:** `:409` *"learning #22 / #26a"* is upstream's own 1.0.0 line (`git blame` → `df6a991`, KJ5HST,
2026-08-08; in blob `be2721a5`) — the review had read the maintainer's citation as fork residue (Learning
#54). New figures: `CHANGELOG.md` 97,257 B at the head (+5,892 B, the entry, now citing #76/#78 by absolute
URL per the ledger's own rule); by hand `91,365 -> 95,557` at commit (1) with the candidate present and
`95,557 -> 97,257` at commit (2); `git diff --stat` 7 files, 2,320 / 98; the module differs from fork `main`
in six lines. Two follow-ons for the maintainer are disclosed in the PR body (`bin/check-learnings:87-89`'s
comment, an eighth file this plan does not include; the `:341` `ResourceWarning`). The record, the numbers
and both review lenses are in the body file's header.

*Do:* make a clean clone with the **§8 R1 recipe only** — `git init` + `git fetch <this repo>
refs/remotes/upstream/read-set-budgets:refs/heads/read-set-budgets`. A bare `git clone --no-local` of
this repository does **not** work: it clones local branches only, so `cea3068` is unreachable and
fork fixtures are reachable — a reviewer measured both (`git cat-file -t cea3068` → *not a valid
object*, `7a71df0` → *commit*). **Prove fixture unreachability per clone**, as S142 did: `git cat-file
-t` on `020ba3f`, `7a71df0`, `e02881a`, `e5cdc66` each fails, and `docs/archive/` does not exist. Never a
worktree of this repo, whose `bin/tests.sh` mutates live ledgers. Then: branch `pr4/context-budget-gate`
from `cea3068`; `git show main:starter-kit/context_budget.py >` the tool (mode 100755); copy
`tools/test_context_budget.py` and apply D9; insert the §3.4 block after `:244`; apply the seed's +6
lines; write the D8 ledger entry; **commit (1)** (subject in D4). Then copy
`docs/planning/pr4-candidate.context-budget.json` to `.context-budget.json` **after re-running
`git cat-file -s` on `CLAUDE.md`, `SESSION_RUNNER.md`, `SAFEGUARDS.md` — the three files the pins and the partition depend on — at the base and confirming the
pins still equal the sizes** (if the base moved, re-derive; a stale pin *below* the new size turns a
ratchet into a red row on arrival); add the `.gitignore` comments and append the one-bullet ledger
line naming the config to PR 4's entry (D4); **commit (2)**. Do not run `--calibrate` (D10). Write
`docs/planning/pr4-read-set-budgets-body.md` (the series' recording precedent: pr1/pr2/pr3 bodies)
with the body as it will be submitted and a status header that Phases C and D update from server
reads.

*DONE looks like — every figure taken from the tree that will be pushed, after the last edit:*
`git rev-parse pr4/…:starter-kit/context_budget.py` = `c5ff15e5…` (**`d91677b5…` since S148**); the test module's diff against
`main:tools/test_context_budget.py` touches exactly the four D9 lines (**six since S148: plus row 1's `:9` and `:13`**); `python3
tools/test_context_budget.py > u.log 2>&1; echo $?` → 0 and `Ran 116 … OK (skipped=2)` (the two skips are the machine-dependent pair; the fork-machine run that exercises them is recorded in §3.2, not repeated in the clone); `--selftest
> s.log 2>&1; echo $?` → 0, `grep -cE '^\s*PASS' s.log` 52, `grep -cE '^\s*FAIL' s.log` 0; the bare run
→ exit 2 = BREACH, expected, and the §3.3 rows **with `CHANGELOG.md` re-measured after the D8 entry
landed** (its row grows by the entry's size — state the number); the §3.3 `--precommit` matrix
reproduced (13 cases); **`--precommit` run by hand with each PR commit's index staged against its parent, the exit read bare
and recorded for each** — measured at S146: commit (1) with the worktree at commit (1) (no config) →
**exit 3**, nothing evaluated; the same index with the candidate present in the worktree → **exit 2**,
`CHANGELOG.md 91,365 -> <after> B ceiling 65,536 B`; commit (2) against commit (1) → **exit 2** on its own
ledger bullet (0 without it). The body says so: the gate this PR ships refuses the PR that ships it, by
hand, and is not wired; `bin/tests.sh` on a pristine control clone **and** on the branch, run to
their summaries, rows diffed: one added row, zero flips, both 1 failure = Test 9; `bin/check-links`,
`bin/check-learnings`, `bin/check-handoff`, `bin/check-handoff --all` each **0**, read bare; `git
status --porcelain` empty after deleting `.context-budget-history.jsonl` — the bare and `--json` runs
create it on the first run and it reappears on every later one, so delete it last; `git diff --stat
cea3068 pr4/…` lists exactly seven files — the six of §3.1–3.6 plus `CHANGELOG.md` (D8);
`git diff cea3068 pr4/… | grep '^+' | grep -v '^+++' | grep -nE '\bS[0-9]{1,3}\b|BL-[0-9]+'` prints
nothing — the check is over **added lines**, because `CHANGELOG.md` (65 lines) and `bin/tests.sh` (11)
already carry such identifiers on `cea3068` and PR 4 may not scrub them; the same regex over both
commit messages (`git log -2 --format=%B`) prints nothing; `grep -c PROPOSAL .context-budget.json` → 8
(one definition line and seven value sites, five distinct values), the count Appendix B states. **Fix-round discipline (S142's precedent):** after any edit that follows a
measurement, re-run the suite on a *fresh* clone of the fixed tree; one adversarial self-review of the
frozen branch before STOP; every Appendix B number re-derived from `git rev-parse <branch>^{tree}`.

*Surface:* the clean clone on this machine. **What it cannot enforce:** the two `TestFitGateEndToEnd`
skips (state, do not pretend — §3.2); Test 9 (network + `main`); the dashboard — at upstream's
`2.10.7` it prints `No projects found` at the repo root on both clones, so **no dashboard criterion is
available** and none is set; anything about `bin/sync --source=github`, which reads `main`.

*Do not:* push; edit `SESSION_RUNNER.md`; run `install-hook` at the clone root; run `bin/tests.sh`
in this repository's own worktree. **STOP.**

**Phase C — Push the branch and open the PR. REQUIRES THE OPERATOR'S EXPLICIT GO-AHEAD; approving this
plan is not it.** One session. Record the claim in this fork's `CHANGELOG.md` **before** acting (a push
and a PR leave no commit here). Re-check `git rev-parse pr4/…^{tree}` equals the tree Phase B measured;
push to `origin`; after the push, `git fetch origin && git rev-parse origin/pr4/context-budget-gate^{tree}`
equals that tree, and once the PR exists `gh pr view --json headRefOid` equals `git rev-parse
pr4/context-budget-gate` (the read-back the round-1 repair dropped, restored at S146); `gh pr create
--repo KJ5HST/methodology --base read-set-budgets` with the body
finalised from Phase B's numbers; read back `gh pr view --json state,baseRefName,mergeable,
mergeStateStatus,files` — OPEN, `read-set-budgets`, MERGEABLE, the §3 file list; `upstream/main`
untouched; update the body file's status header from those reads. *Surface:* GitHub. **What it cannot
enforce:** MERGEABLE is server-computed against the base at that moment; nothing here verifies the
maintainer's review or his machine. **STOP.**

**✅ DONE at S149 (2026-09-03) — the operator's *"1"* answering the S148 close-out's numbered list; the
claim recorded in `CHANGELOG.md` first (`974db79`).** Tree re-checked `c857734`; `git push origin
pr4/context-budget-gate` → `* [new branch]`; `origin/pr4/context-budget-gate` read back `cf15489` / tree
`c857734`; `gh pr create --repo KJ5HST/methodology --base read-set-budgets --head
rmsharp:pr4/context-budget-gate` with the body file's *Title* and the Body + two trailing sections (14,003 B,
no fork-internal identifier by grep) → **[PR #79](https://github.com/KJ5HST/methodology/pull/79)**, created
`2026-09-04T00:59:58Z` (dragon 14: a 2026-09-03 local session); read back `state OPEN`, `baseRefName
read-set-budgets`, `headRefOid cf15489…` = `git rev-parse pr4/context-budget-gate`, `mergeable UNKNOWN` at
creation then **`MERGEABLE` / `CLEAN`** on the second read, `changedFiles 7` (the §3 list exactly),
`+2,320 / −98`, two commits, body 14,004 B (a trailing newline), `isDraft false`; `upstream/main` `512c2ed`
and `upstream/read-set-budgets` `cea3068` untouched; `gh pr list --state open` → #79 alone; the body file's
header updated from those reads. **What this did not verify:** the maintainer's review or machine
(§3.2). STOP.

**Phase D — Merge, on its own go-ahead.** One session. Record the claim in this fork's `CHANGELOG.md`
first. `gh pr merge --merge` (never squash: #76/#77/#78 are all two-parent — measured, `46b56fd`, `907a696`, `cea3068` — and a
squash is expected to break the ancestry `read-set-budgets` → `main` will later carry, an inference from
S144's gotcha, not a measurement); `gh pr merge` can print nothing — read
`gh pr view --json state,mergeCommit` back; `tree(<merge>) == tree(<head>)`; `git ls-remote --heads
upstream` shows `main` unchanged and `read-set-budgets` at the merge sha; `gh pr list --state open`
empty; the tool's blob read off the merged branch; the body file's header updated. *Surface:* GitHub,
same limits as C. **STOP.**

*After D, outside this plan:* `read-set-budgets` → `main` (expected to clear Test 9; the version decision);
the deferred documentation PR; **the #77 ledger backfill (D6, not in PR 4)** — its own heading
`### 2026-09-02 · [ad hoc] Backfilled (reconcile-on-read): undocumented commit 56997af (PR #77, merged
907a696) — the ledger trimmer`, in its own `docs(changelog): backfill …` commit per `SESSION_RUNNER.md`
Phase 0 step 6, and written deliberately, because the frontier-based reconcile can never surface it
(`56997af` sits below the frontier `2c30d0f`); the fork-side follow-ons of D11 (the D9 back-port, the
`bin/tests.sh` comment alignment, PR 4's two added conflicts on the next sync); the three deliberately-left
tool defects (§3.7), each a one-line follow-on; dragon 3's mitigation test;
the maintainer's `--calibrate` (D10); and the three adopters' `bin/sync`.

---

## 6. Evidence-based inventory

Every file naming `context_budget` / `context-budget` on either tree, `git grep -c -iE
'context[_-]budget' <tree> -- . ':!CHANGELOG.md' ':!HANDOFFS.md' ':!docs/archive'
':!.context-budget-history.jsonl'`, **counted on the pre-change tree `8c701b5`** (counting on a tree that
holds this plan adds the plan's own mentions):

| File | fork `8c701b5` | `cea3068` | PR 4 |
|---|---|---|---|
| `bin/tests.sh` | 32 | 30 | +1 block (§3.4) |
| `tools/test_context_budget.py` | 17 | — | new (§3.2) |
| `tools/test_methodology_dashboard.py` | 16 | 16 | untouched (BL-31, upstream via #71) |
| `starter-kit/context_budget.py` | 11 | 10 | replaced (§3.1) |
| `starter-kit/methodology_dashboard.py` / `tools/…` | 10 / 10 | 7 / 7 | untouched (§3.7) |
| `.context-budget.json` | 5 | — | new, from Appendix A (§3.3) |
| `starter-kit/FRAMEWORK_LEARNINGS.md` | 4 | 4 | untouched |
| `README.md` | 3 | 2 | untouched — upstream's two are v3.7 What's New lines; the fork's third is a fork-only table |
| `bin/_manifest.py` | 3 | 2 | untouched — the row exists (`:46`); the fork's third is a comment |
| `starter-kit/BOOTSTRAP.md` | 2 | 0 | untouched (deferred docs PR) |
| `bin/check-handoff` | 2 | 0 | untouched (fork-only comments) |
| `docs/RELEASE_HISTORY.md` | 2 | — | fork-only file; untouched |
| `.gitignore` | 2 | 0 | +7 comment lines (§3.6) |
| `CLAUDE.md` | 0 | 1 | untouched (the v3.7 line) |
| `starter-kit/methodology_trim.py` / `bin/check-learnings` / `starter-kit/context-budget.json` | 1 / 1 / 1 | 1 / 1 / 1 | trimmer untouched; **`bin/check-learnings:87-89` cites the canonical root config's derivation — satisfied by D7**; seed +6 (§3.5) |
| `docs/planning/*.md` | 14 files, 116 mentions | 0 | fork-only; not shipped |

Consumers of the root `.context-budget.json` other than the tool, on `cea3068`: the dashboard
recognises the file as framework-installed through its per-file signature entry
(`starter-kit/methodology_dashboard.py:508-523` upstream — the tool's own `context_budget.py` entry is `:498-507` — since #71, `b5be407:479`) and an exclusion tuple (`:360-361`) —
the fork's `_CONTEXT_BUDGET_JSON_SIGNATURES` symbol the first draft named **does not exist upstream** —
and upstream's own comment on that entry (`:509`) says it is *"Structurally unreachable today"* for
scoring, so it reads nothing and scores nothing. `bin/tests.sh` copies the **seed** into scratch projects,
never the root file. No other reader.

---

## 7. Here be dragons — PR 4's own

1. **The tool exits 3 without a root config, and prints zero rows.** Anything that runs it at the
   canonical root — the wired unit test, a maintainer's first `--selftest` — fails until
   `.context-budget.json` exists. The config is what makes the test suite green (Probe A vs D).
2. **Never run `install-hook` at the canonical root, and the consequence differs by clone.** On a
   fresh clone (`core.hooksPath` unset) it **installs** `.git/hooks/pre-commit` exec'ing
   `<root>/context_budget.py`, which lives in `starter-kit/` here, and every subsequent commit fails
   with `can't open file`; recover with `rm .git/hooks/pre-commit`. With `core.hooksPath=.githooks`
   set (BOOTSTRAP Step 10) it declines — because a `pre-commit` that is not ours already exists there
   (the FM #27 ledger gate), not because of the setting itself; a `hooksPath` pointing at an empty
   directory would be installed into. The gate is **measuring only** here until someone chains it
   into `.githooks/pre-commit` — governing-plan dragons 1 and 2, answered in Appendix B as a
   disclosure, not a mechanism.
3. **With the ledgers declared (D1), a wired gate refuses every close-out until the appended file is
   under 65,536 B** — and the trimmer does not fire until 196,608 B. Measured both ways.
4. **Every PR 4 commit is such a commit** — both carry a ledger line (D4), and by hand the gate exits 3
   before the config exists and 2 after. The body says it.
5. **Bare and `--json` runs create `.context-budget-history.jsonl` on the first run and append only when
   the measurement changes — the file reappears on every later run; `--precommit` evaluates neither
   `structure` nor `max_lines`.** Measure in the clone; delete the history file before `git status` is a criterion;
   never run a bare measurement in this repository's worktree while `bin/tests.sh` runs.
6. **The two skipped tests may run on the maintainer's machine and fail for non-defect reasons** (§3.2).
   The body names both, the three causes, and the diagnosis.
7. **Do not port the fork's config or its narrative.** It sets a `CLAUDE.md` ceiling of 18,600 B against an
   11,368 B file and cites S90/S129/BL-37; every such sentence is false on the target tree.
8. **The pins are true of `cea3068` only** (§5 Phase B). The partition numbers (41,364 / 15,386 /
   56,750) move if `SAFEGUARDS.md` does, if `read_cap_tokens` changes, or if the `SAFEGUARDS.md` pin (a
   PROPOSAL) is moved.
9. **Keep mode 100755 on the tool.** `git apply` warns on a 644 target; the suite asserts
   `context_budget.py is executable`.
10. **In `zsh`, `$c:starter-kit/…` is a `:s` substitution modifier on `$c`, not a git revision.** It
    rewrites the argument to `<c>/context_budget.py`; `git rev-parse` then exits 128, prints `fatal:
    ambiguous argument` on stderr and echoes the mangled path on stdout, so a trailing `| grep <blob>`
    matches nothing. Loud on stderr; it looks silent only when stderr is discarded or only the final
    grep is read. Write `${c}:path`. It mangled two enumerations at S145; one reached the frozen draft.
11. **Read every exit code bare on the next line.** A pipeline reports only its last stage's status, and
    under `pipefail` an early-exiting consumer (`grep -q`, `head`, `grep -m1`) closes the pipe, the
    producer dies of SIGPIPE (141) and the pipeline reports failure **on a match**; `grep -c` reads to
    EOF and is immune to that inversion but exits 1 on zero matches. §8's commands redirect to files
    first.
12. **Test 9 is red on both trees and is expected to stay red** until `read-set-budgets` reaches `main`
    (it also needs the network and `gh` auth); the limit
    lives in `bin/sync`'s `read_github()` (`:80-86`), not in the branch model.
13. **`gh pr merge` can succeed silently** (S144). Read state back; compare trees.
14. **Dates cross midnight in UTC.** #78 merged at `2026-09-03T02:04Z` in a 2026-09-02 local session.
15. **The PR 1 body wrote *"The remaining 10,831 B is what the later PRs on this branch are for."***
    No later PR shrank the pair; PR 4 makes the 10,831 B **refuse to grow**. The body must not imply
    the pair is fixed — it is exactly as over as PR 1 left it, and now says so out loud.
16. **Two units answer to "lines".** `wc -l` and the tool's count differ by one on every LF-terminated
    file (§2.2); a fixture described as 304 lines prints `305 ln`. Name the unit.

---

## 8. Reproduction

All run 2026-09-02 from this repository; `$S` is a scratch directory. Exit codes are read bare.

**R1 — a clean clone of `cea3068` without network (the only recipe; see Phase B):**
```sh
git init -q "$S/probe/base" && git -C "$S/probe/base" fetch -q "$PWD" \
  refs/remotes/upstream/read-set-budgets:refs/heads/read-set-budgets \
  && git -C "$S/probe/base" checkout -q read-set-budgets      # HEAD = cea3068
for f in 020ba3f 7a71df0 e02881a e5cdc66; do git -C "$S/probe/base" cat-file -t $f 2>&1; done   # 4× not a valid object
ls "$S/probe/base/docs/archive" 2>&1                                                              # no such directory
```

**R2 — the blob identity behind §1.1 and §2.4 (note the braces — dragon 10):**
```sh
for r in upstream/read-set-budgets upstream/main 14bd88a main; do
  echo "$r $(git rev-parse "${r}:starter-kit/context_budget.py")"; done     # be2721a5… ×3, then c5ff15e5…
git log --oneline --graph --parents main -- starter-kit/context_budget.py | wc -l   # 9 = 7 fork + 2 upstream, no merge
for c in $(git log --all --format=%h -- starter-kit/context_budget.py); do
  echo "$c $(git rev-parse "${c}:starter-kit/context_budget.py" | cut -c1-8)"; done | grep 73fb90aa   # 6a91660
```

**R3 — the patches apply (write the base blob FROM THIS REPO; the first attempt ran `git show` inside
the scratch repo, produced an empty file, and every patch "failed" — check the base blob first):**
```sh
mkdir -p "$S/pc/starter-kit" && git show be2721a5 > "$S/pc/starter-kit/context_budget.py" && chmod 755 "$S/pc/starter-kit/context_budget.py"
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
( cd "$S/probe/base" && python3 starter-kit/context_budget.py --selftest > A2.log 2>&1; echo "A' exit=$?" )        # 3
( cd "$S/probe/base" && cp starter-kit/context-budget.json .context-budget.json && python3 starter-kit/context_budget.py > B.log 2>&1; echo "B exit=$?"; rm -f .context-budget.json .context-budget-history.jsonl )
```

**R5 — Probe D (candidate config; commit it so `--precommit` has a HEAD baseline):**
```sh
cp docs/planning/pr4-candidate.context-budget.json "$S/probe/base/.context-budget.json"
# insert the §3.4 block after the trimmer `fi` (upstream bin/tests.sh:244), then:
cd "$S/probe/base" && git add -A && git -c user.name=t -c user.email=t@t commit -qm candidate
python3 starter-kit/context_budget.py > bare.log 2>&1; echo "bare exit=$?"          # 2 = BREACH, expected; 49 lines
grep -ci defect bare.log                                                              # 0
python3 starter-kit/context_budget.py --selftest > s.log 2>&1; echo "selftest exit=$?" # 0
grep -cE '^\s*PASS' s.log; grep -cE '^\s*FAIL' s.log                                  # 52, 0
python3 tools/test_context_budget.py > u.log 2>&1; echo "unit exit=$?"; tail -3 u.log   # 0; OK (skipped=2)
echo x >> starter-kit/SESSION_RUNNER.md && git add -A
python3 starter-kit/context_budget.py --precommit > p.log 2>&1; echo "precommit exit=$?"; git reset -q --hard   # 2
rm -f .context-budget-history.jsonl
```

**R6 — the suite, control vs candidate, run to their summaries, rows diffed:**
```sh
( cd "$S/probe/control" && bash bin/tests.sh > "$S/ctl.log" 2>&1 )   # pristine cea3068: 114 passed, 1 failed
( cd "$S/probe/base"    && bash bin/tests.sh > "$S/cnd.log" 2>&1 )   #                  115 passed, 1 failed
for f in ctl cnd; do grep -E '^\s*(PASS|FAIL|SKIP):' "$S/$f.log" | sed 's/^ *//' | sort > "$S/$f.rows"; done
comm -12 "$S/ctl.rows" "$S/cnd.rows" | wc -l      # 115 shared
comm -3  "$S/ctl.rows" "$S/cnd.rows"              # exactly: PASS: context budget gate unit tests green
```

**R7 — sizes and witnesses on the base:**
```sh
for f in CLAUDE.md starter-kit/SESSION_RUNNER.md starter-kit/SAFEGUARDS.md CHANGELOG.md HANDOFFS.md starter-kit/FRAMEWORK_LEARNINGS.md; do
  printf '%-38s %s\n' "$f" "$(git cat-file -s upstream/read-set-budgets:$f)"; done
git show upstream/read-set-budgets:CHANGELOG.md | grep -cE '^### [0-9]{4}-[0-9]{2}-[0-9]{2} · \['   # 39
git show upstream/read-set-budgets:HANDOFFS.md  | grep -c '^```handoff'                             # 10
git show upstream/read-set-budgets:starter-kit/FRAMEWORK_LEARNINGS.md | grep -cE '^\| *[0-9]+ *\|'   # 46
python3 starter-kit/methodology_trim.py --file CHANGELOG.md --check   # in the R1 clone: 91,365 B against a 196,608 B budget, trigger does not fire
```

**R8 — Probe C4, the adopter fixture (old = `git show upstream/read-set-budgets:starter-kit/context_budget.py`,
new = `main:`, seed = `upstream/read-set-budgets:starter-kit/context-budget.json`):**
```sh
# CLAUDE.md: the seed's fence around 900 'y' (bin/tests.sh:613-614 fixture). LEARNINGS.md: 3,000 B of 'l'.
# SESSION_NOTES.md: '## ACTIVE TASK\nsomething\n\n## What Session 1 Did\n' + 300 lines of (W-1) 'x' + '\n'
# W=200 → 60,048 B: both exit 1, stdout differs only in the row's unit (ln → B)
# W=243 → 72,948 B: same.   W=245 → 73,548 B: old exit 1 `ok`; new exit 2 `≈25,101 tok / 25,000 tok over`
# the flip is at 73,253 B exactly (≈25,001 tok): 73,250–73,252 B still `ok`, exit 1 — int() truncates, the compare is strict
```

---

## Appendix A — the candidate canonical root config

Shipped as [`pr4-candidate.context-budget.json`](pr4-candidate.context-budget.json) (17,934 B; third
draft, S146) so the build session copies a file rather than transcribing one. Its shape, without the `_` prose:

```json
{
  "read_cap_tokens": 25000, "bytes_per_token": 2.93, "fixed_harness_tokens": 35700,
  "growth_run": 10, "calibrate_against": "CLAUDE.md",
  "classes": {
    "resident": { "total_bytes": 59168 },
    "read-set": { "total_bytes": 56750, "warn_bytes": 51000, "derive_from_read_cap": true }
  },
  "files": [
    { "path": "CLAUDE.md", "class": "resident", "max_lines": 200, "max_bytes": 59168,
      "structure": [ { "pattern": "^## Versioning", "expect_min": 1 } ] },
    { "path": "starter-kit/SESSION_RUNNER.md", "class": "read-set", "max_bytes": 41364 },
    { "path": "starter-kit/SAFEGUARDS.md",     "class": "read-set", "max_bytes": 15386 },
    { "path": "CHANGELOG.md", "class": "read-mandated", "max_bytes": 65536, "max_tokens": 25000, "bytes_per_token": 2.4674,
      "structure": [ { "pattern": "^### \\d{4}-\\d{2}-\\d{2} · \\[", "expect_min": 5 } ] },
    { "path": "HANDOFFS.md",  "class": "read-mandated", "max_bytes": 65536, "max_tokens": 25000, "bytes_per_token": 2.3648,
      "structure": [ { "pattern": "^```handoff", "expect_min": 1 } ] },
    { "path": "starter-kit/FRAMEWORK_LEARNINGS.md", "class": "on-demand", "max_bytes": 73728, "bytes_per_token": 2.8897,
      "structure": [ { "pattern": "^\\| *[0-9]+ *\\|", "expect_min": 5 } ] }
  ],
  "synced": []
}
```

Every number's `_` key in the shipped file states its derivation and the command that re-derives it
(`calibrate_against` gained its key at S146), marks the five PROPOSAL values (seven label sites), and labels the one
inherited threshold, `CLAUDE.md.max_lines` 200 (D10). The calibration constants are labelled
**inherited from the seed, not measured on this repo**, with `--calibrate` as the remedy — which
proposes and writes nothing.

## Appendix B — PR body, draft for Phase C to finalise from the pushed tree

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
> | `CHANGELOG.md` | 91,365 | 65,536 | over by 25,829; ≈37,028 tok at 2.4674 B/tok |
> | `HANDOFFS.md` | 70,182 | 65,536 | over by 4,646; ≈29,677 tok at 2.3648 B/tok |
>
> The bare run exits 2 with that table: six red findings on day one — five per-file ceilings across three
> files, plus the read-set class total. The two token estimates use densities measured on the fork's
> copies of these same-format ledgers, not on this tree; each ledger's `_` key gives the doubled-file
> method to re-measure them here. `--precommit` refuses any commit that grows either file in bytes (or,
> for a whole-read class, in estimated tokens) and passes any that shrinks one (verified: +2 B refused;
> −5,000 B passed while still over); line-count and structure checks run in the bare and `--json` modes
> only. **Nothing on this branch shrinks the pair; this PR makes it stop growing and say why.**
>
> ## The tool refuses to run without a config, so this PR provisions one
>
> Your 1.0.0 already exits 3 — *"refuses to invent budgets for a project that has not declared them"*
> — at any root without `.context-budget.json`; that is unchanged. The seed adopters receive reads red
> here for reasons unrelated to this series (`CLAUDE.md` is 59,168 B against the seed's 28,000). So the
> config in this PR **pins** `CLAUDE.md` at its arrival size, **derives** the read-set ceiling from the
> read cap (25,000 tok × 2.27 B/tok = 56,750, computed at run time — 25,000 is `read_cap_tokens` in the
> config — the number in the Read tool's own refusal, `exceeds maximum allowed tokens (25000)`, Claude Code
> 2.1.259; 2.27 is the tool's `MIN_BYTES_PER_TOKEN` floor at `starter-kit/context_budget.py:68`, a
> constant, not a key, so a different floor is a tool edit), and **declares** the two ledgers
> Phase 0 reads and the Learnings table your `bin/check-learnings` already cites this file for.
>
> ## Every ceiling in that config is yours; five are proposals rather than measurements
>
> 1. **`CLAUDE.md` pinned at 59,168 B** (growth refused, shrink passes). Alternative: the seed's
>    28,000 / 34,000, which reads *over by 31,168* today.
> 2. **`CHANGELOG.md` and `HANDOFFS.md` at 65,536 B** — the fork's ceiling, **not the trimmer's**:
>    #77's `methodology_trim.py` triggers at 196,608 B and reports *trigger does not fire* on both
>    ledgers today (91,365 B and 70,182 B). Bringing either under this ceiling is
>    `python3 starter-kit/methodology_trim.py --file <ledger> --budget-bytes 65536` (dry-run by
>    default; add `--write`), `CHANGELOG.md` first — a `HANDOFFS.md` trim writes its own entry into
>    `CHANGELOG.md`, which the gate refuses while that file is over. The trimmer stops at half the budget
>    (91,365 → 30,920 B, 30 of 39 records; 70,182 → 26,891 B, 7 of 10), appends one `CHANGELOG.md` entry
>    per trim, and refuses on an unreconciled tree. **At the carried densities the token ceiling binds
>    first** — 25,000 tok is 61,685 B for `CHANGELOG.md` and 59,120 B for `HANDOFFS.md` — so 65,536 B
>    fires first only if a re-measured density comes in above 2.62 B/tok. Alternative: omit the byte
>    ceiling and keep `max_tokens`, or omit both and let the trimmer's number govern.
> 3. **`SAFEGUARDS.md` pinned at 15,386 B**, so the whole 10,831 B of debt sits on `SESSION_RUNNER.md`.
> 4. **`FRAMEWORK_LEARNINGS.md` at 73,728 B**, on-demand, no token ceiling — at its measured 2.8897
>    B/tok that sits 1,486 B above the one-read cliff; the `_` key says so.
> 5. **Two more numbers, neither measured:** `read-set.warn_bytes` 51,000 B is the fork's choice, marked
>    PROPOSAL in its `_` key — ~10% under the derived total so the class warns before it refuses; inert
>    while the class is over, which it is today — and `CLAUDE.md.max_lines` 200 is
>    `starter-kit/BOOTSTRAP.md:198`'s own *"roughly 200 lines"* applied to your `CLAUDE.md` (126 lines
>    today by `wc -l`; bare run only, `--precommit` ignores it). Delete either key if you do not want it.
>
> The calibration constants are the seed's. After merge, run `python3 starter-kit/context_budget.py
> --calibrate`; it writes nothing. If it admits a fit (R² ≥ 0.50, positive slope), set `bytes_per_token`
> to the fitted value. Until then `CLAUDE.md`, `SESSION_RUNNER.md` and `SAFEGUARDS.md` are judged at the
> seed's 2.93 B/tok — `CLAUDE.md` reads ≈20,194 tok in the header, `ok`; at the 2.27 floor the same bytes
> read 26,065, `over` — and `CLAUDE.md`'s derived 26,065-token ceiling is clamped to 25,000 without a
> message, because only a *declared* `max_tokens` is reported when clamped. If your harness's read cap
> differs, set `read_cap_tokens` and every derived ceiling follows.
>
> ## Day one, and what does not change
>
> - **This PR's own two commits fail the gate it ships, run by hand:** exit 3 on the first (no config
>   yet), exit 2 on the second (its `CHANGELOG.md` bullet grows a file already over 65,536 B). The gate is
>   not wired into `.githooks/pre-commit`; nothing refuses these commits. Both carry a ledger line because
>   your `.githooks/pre-commit` requires one. If you chain the budget check in later, every commit that
>   appends to a ledger is refused until **that** ledger is under 65,536 B — and the hook's documented
>   `--no-verify` bypass applies to the budget check too. This PR claims no enforcement.
> - `python3 starter-kit/context_budget.py` exits 2 with the table above and creates
>   `.context-budget-history.jsonl`, untracked (the fork tracks it; your call — the `.gitignore` comment
>   explains). `--precommit`, `--selftest`, `bin/tests.sh` write nothing.
> - **Nothing else in your workflow changes unless you wire the hook — except one added `bin/tests.sh`
>   row**, which fails whenever the unit module fails (including the two machine-dependent tests under
>   Verification). `core.hooksPath` is local config; `.githooks/pre-commit` is the ledger gate and this PR
>   does not chain the budget into it.
> - **Do not run `install-hook` at this root.** On a clone without `core.hooksPath` it installs
>   `.git/hooks/pre-commit` pointing at `<root>/context_budget.py`, which does not exist here, and every
>   commit then fails with `can't open file`; recover with `rm .git/hooks/pre-commit`. With
>   `core.hooksPath=.githooks` it declines.
> - `SESSION_RUNNER.md` Phase 0 still never names the tool. Adding one line grows the capped file
>   ~300 B. Not done here; your decision.
> - The dashboard twins are untouched (`2.17.0` on the fork vs `2.10.7` here; separate series).
>
> ## What changes for adopters who sync
>
> Exit codes are unchanged (`0/1/2/3`). On an unchanged seed config, two things differ:
> (1) when nothing fires, a read-mandated row reports **bytes, not lines** (`305 ln / 400 ln ok` →
> `60,048 B / 120,000 B ok`); (2) a read-mandated file **above 73,252 B** — the first size whose
> truncated estimate `int(bytes / 2.93)` exceeds 25,000 tokens is 73,253 B (≈25,001 tok) — now gets a
> **derived token ceiling** the old tool never had, and goes `ok` → `over`, exit 1 → 2, even under every
> byte and line ceiling the adopter declared — measured at 73,253 B and 73,548 B; 73,252 B still `ok`. Also new: ceilings may be declared in tokens (`max_tokens`); a `max_tokens` above the cap
> is **clamped to the cap and reported as a config defect** — the clamp is never silent; the gate sizes
> the **index** with `git cat-file -s` (the old path was 1 B short on LF, more on CRLF, and raised on
> non-UTF-8 content); `precommit` gains a class-total arm; `calibrate` walks first-parent history,
> compares timezone-aware stamps, and refuses a fit below R² 0.50; the ledger row names the ceiling
> that fired in its own unit; remediation text no longer says *here* about a measurement taken on another project.
>
> ## Verification
>
> Clean clone of `cea3068`. Unit module 116 run, OK, **2 skipped** — `TestFitGateEndToEnd`
> (`tools/test_context_budget.py:330`), which needs *this repository's* session transcripts on the
> running machine. **On yours they run if `~/.claude/projects/<your-checkout-slug>/*.jsonl` exists,
> and they can fail for reasons that are not the tool:** fewer than 3 commits touching `CLAUDE.md`, fewer
> than 4 transcripts with a usage record dated at or after the file's first recorded size, a `CLAUDE.md`
> that was the same size at every usable session, a fitted slope ≤ 0, or opening context that never
> varied (R² undefined). If the new `bin/tests.sh` row is red, run `python3 tools/test_context_budget.py
> -v 2>&1 | grep -B1 -A1 AssertionError` — the tests capture `calibrate()`'s stdout, so its own
> diagnosis (*"only N usable sessions — not enough to fit"*, *"no variation in CLAUDE.md size"*) appears
> only inside the `AssertionError:` text; `grep -A2 FitGateEndToEnd` shows a `skipped` suffix naming the
> missing directory.
> `--selftest` 52 PASS / 0 FAIL. `bin/tests.sh` **115 passed / 1 failed** vs **114 / 1** on the
> untouched base: one row added, zero status flips; the failure on both is Test 9 (`bin/sync
> --source=github` reads `main`, where three manifest sources are absent until this branch merges).
> `bin/check-links`, `bin/check-learnings`, `bin/check-handoff`, `bin/check-handoff --all`: 0/0/0/0.
