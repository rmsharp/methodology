I went through this branch at `c84e7d96` and re-ran its own checks before questioning any of them. Everything I could check reproduced. In a fresh clone: `quality_ratchet.py --run` gave **9/9 pass, results hash `74c773523dab`** — the same hash the receipt in `HANDOFFS.md` cites, so the hash really is deterministic across machines; `--selftest` observed all 17 checks; `bin/tests.sh` read 134 passed / 1 failed (test 9, by construction, as the description says); `context_budget.py --status` exited 0; and no tracked file changed. `--precommit` refused every loosening it claims to refuse. The token figures in the description reproduce too.

Below are the changes I'd suggest before merge: two about how file sizes are measured, three about what the ratchet holds, four smaller ones, and one about the description itself. Everything is measured at `c84e7d96` and reproducible — see the bottom.

---

## 1. Two budgets are denominated in bytes where tokens is the measure that matters

**How I measured tokens.** I concatenated each file with itself, read the result through a tool that refuses any file over 25,000 tokens, and halved the number in the refusal message. I checked the instrument before trusting it, by reproducing three figures already recorded in this repository exactly (48,555, 49,683 and 36,955).

**`CLAUDE.md` — the reduction went the other way in tokens.** The description says the PR pays for its growth by reduction rather than by a raised ceiling, and against the byte pin that is true: 59,168 → **59,153 B, 15 B under**. Measured in tokens the same change is **23,420.5 → 23,482.5, 62 tokens larger**. A byte pin cannot see this, because bytes per token is a property of the content: the new table rows are dense with backticked paths and tokenize at fewer bytes per token than the prose that was shortened to pay for them. This is the same substitution PR #80 already made for the orientation read-set, where a byte class ceiling became per-file token ceilings at measured densities.

Two facts behind it:

- The budget tool judges this file at **2.93 bytes/token**, the seed's fallback — `.context-budget.json` is explicit that this is inherited and not measured here. Measured on this branch it is **2.519**. So the tool reports 20,188 tokens where there are 23,482.5: **14% low**, and it shows roughly 4,800 tokens of headroom under its derived 25,000 where there are about 1,500.
- Worth noting what the pin is mostly pinning: **87% of the file's bytes** (51,617 of 59,153) are the release history below `## Versioning`. Whether that belongs in a file injected into every session is a bigger decision than this PR.

*Suggested:* measure this file's density and declare `max_tokens` — 23,483 if a no-growth pin is what's wanted — keeping `max_bytes` only as a coarse backstop.

**`starter-kit/SESSION_RUNNER.md` — right unit, stale density.** This one is budgeted in tokens, which is the right call. The density 2.8248 was measured correctly in `008d656`, on the file as it stood then (52,195 bytes). The **next** commit, `628d218`, edited that file to 53,301 bytes, and `b4226d3` took it to 53,328 — and the density was never re-measured. The config comment still describes the measured blob as "this branch's file", which it stopped being two commits later.

The effect is small but it points the wrong way. Measured on the current file the runner is **18,897.5 of its 18,900 tokens — 2.5 tokens of room**, not the 22 the tool reports and the description repeats. Because the tool divides by the stale density, it would admit growth to 53,391 bytes, which measures about **18,920 tokens — roughly 20 over the ceiling the config itself declares.** The safeguard meant for this, `measured_bytes`, warns only at 25% drift, about 13,000 bytes away, against a margin of 2.5 tokens.

*Suggested:* re-measure and record 53,328 bytes at 2.8220, and consider binding a density to the blob it was measured on so an edit to that file invalidates it. Practically, after this PR every edit to the runner has to be net-negative in tokens.

**No declared gate covers any of this.** `context_budget.py --status` is the actual verdict on every budget above, and it is not one of the nine gates, not chained into `.githooks/pre-commit`, and not run by `bin/tests.sh` — which runs the tool's self-test and unit tests but never `--status` against the tree. So a commit that breaks the read budget passes every gate this PR declares. It passes today, so declaring it costs nothing:

```json
{ "name": "context-budget", "direction": "max", "threshold": 0,
  "command": "python3 starter-kit/context_budget.py --status",
  "why": "exit code: every declared file and class within its budget" }
```

This is also the PR's own new rule applied to itself — the Phase 3C branch it adds says a mechanical invariant is a gate, not a row.

---

## 2. Three things the ratchet doesn't hold

Each of these I ran in a scratch repository rather than reading off the code.

**(a) Deleting the manifest is the loosest possible loosening, and everything passes it.** The hook only runs the tool when `.quality-gates.json` exists in the working tree; `precommit()` returns clean when the index has no manifest ("manifest not in this commit: nothing to ratchet"); and the dashboard returns early when the file is absent, so its history walk skips that version rather than reading it as a removal.

Observed, in order: lowering a floor 5 → 4 is **refused** (exit 1, correctly); deleting the manifest **passes** (exit 0); re-adding it at floor 1 **passes**, reporting "first manifest commit — nothing to compare against". The dashboard afterwards reports only the 5 → 4 attempt. **The 4 → 1 achieved by deleting and re-adding is invisible to every mechanism in this PR.**

*Suggested:* in `precommit()`, refuse when `HEAD` carries a manifest with gates and the index carries none ("manifest removed"); in the hook, run the tool whenever `HEAD` tracks the manifest, not only when the working tree has it; in the dashboard, read a deletion as an empty gate set so every gate reads as removed.

**(b) The count gates cannot see failures or skips.** Four of the nine gates extract `Ran (\d+) tests` — the number of test methods that exist, not how they did. Given a manifest of such gates, `--run` reported **3/3 pass and exited 0** over: a suite where two of three tests fail; a suite where all three are skipped; and a summary line reading `134 passed, 1 failed`.

The manifest's note says green/red is carried by the passed-count gate, and that holds only while no test is added — one new passing check offsets one new failure. The gate that would catch it, `tests-sh-failed ≤ 0`, is deferred until after merge because test 9 fails on the branch. I'd suggest that deferral isn't needed: **declare it now at `max 1`**, the value the branch actually measures. That follows the manifest's own rule of declaring gates at their current measured values, it catches a second failure today, and it tightens to 0 in the first commit after merge. Pairing each unit-suite count with an exit-code gate would likewise make a red suite fail its own gate — and it would ease a second consequence of counting, which the plan itself flags ("'130 checks' is a count, not a target"): with five of the nine gates counting, pruning a dead or duplicated test becomes a loosening that needs plan-mode approval.

**(c) The receipt's gate citation is checked for shape only, and nothing performs the comparison.** `bin/check-handoff` requires a match for `quality_ratchet:\s*\d+/\d+\s+pass`. A receipt citing **`quality_ratchet: 0/9 pass` exits 0**; only a receipt citing nothing exits 1.

The plan asked for "a lint that the citation resolves … Phase 0 reconcile compares the newest receipt's claim to the newest results", and the description says Phase 0 compares the cited counts against the results file. But Phase 0 in `starter-kit/SESSION_RUNNER.md` has no such step — its eight steps are unchanged by this PR, and the only places the runner mentions gates are Phase 3C, Phase 3E and failure mode 17. The results file is also gitignored, so a fresh clone has nothing to compare against.

Worth saying clearly: **the comparison itself is sound.** The results hash excludes the commit and the timestamp, and my clean-clone re-run reproduced the receipt's `74c773523dab` exactly. It just needs someone or something to run it.

*Suggested:* have the lint require 0 failed, 0 unmeasured, and a measured count equal to the declared gate count — cheap and local. Then either add the comparison to Phase 0 as a step, or support something like `--status --expect <hash>`. If neither, say in the docs that the citation is checked for shape only.

---

## 3. Four smaller ones

- **A forced manifest deletion locks the repository.** The hook `install-hook` writes runs the tool with no guard, and with no manifest the tool exits 3. After deleting the manifest with `--no-verify`, **every later commit is refused**, including unrelated ones, with "no `.quality-gates.json` found … refuses to invent thresholds" — a message that doesn't name the cause. An adopter who tries the ratchet and backs out by deleting its manifest can't commit again without `--no-verify`. Suggested: with no manifest in the index, pass cleanly when `HEAD` has none, and refuse with the "removed" message when it does.

- **The dashboard's loosening detector misses two changes the tool catches.** It reports a changed threshold only when the direction is unchanged, and it ignores commands. A direction flip (`min 5` → `max 5`) is refused by the tool but **reported as nothing**; a command swapped for `echo 'Ran 999 tests'` is warned by the tool and **reported as nothing**. That matters because the bypass message promises "the manifest's git history shows the loosening and the dashboard reports it as a risk" — so a bypassed flip leaves no advisory at all. Suggested: report flips as loosenings, and command or extract changes as "gate redefined" at low severity.

- **The coverage bonus keys on a gate's name.** A passing gate whose *name* matches `coverage` earns +2 testing points. A gate named `coverage` running `echo 100` earns it — I checked. The plan explicitly did not adopt "any coverage floor without a faithfulness check beside it", and this rewards exactly that, from a file that is gitignored and locally written. Suggested: drop the bonus until a faithfulness gate is required beside a coverage gate, and in any case don't key on names.

- **`install-hook` in a fresh clone of this repository breaks every commit.** It exits 0; the next commit fails with "can't open file `<root>/quality_ratchet.py`", because the tool lives under `starter-kit/` here and a fresh clone has no `core.hooksPath`. `.context-budget.json` already carries exactly this warning for the sibling tool ("DO NOT RUN `install-hook` HERE", with the `rm .git/hooks/pre-commit` recovery); `.quality-gates.json` carries none. Suggested: add the same warning, or have `install-hook` write the path of the file actually running.

---

## 4. One thing about enforcement, and one about the description

**What binds today.** The new section says the mechanical form "binds every actor: every tier, every agent, every human, every session". What enforces it right now is a per-clone, opt-in hook that each clone enables separately and that `--no-verify` bypasses, and this repository has no CI. That's a real gap between the claim and the mechanism, not a defect in the code — a CI job running `--run` plus the comparison against the base branch is what would bind someone who never sets a hook. Short of that, I'd state the enforcement point plainly in the section itself.

**The description is hard to read without the plan open beside it.** This is worth fixing because the PR description is the durable explanation of what shipped and why, and it is what a newcomer or a future maintainer reads first. As written it assumes the reader has read the plan and several earlier PRs:

- Decision codes (`D1–D10`, `D4`, `D9`, `P0`, `G1`) appear without expansion; a reader on this page can't resolve them.
- References like "the #80 shape", "the PR #71 discipline" and "the #80 re-review's G1" name discussions that aren't linked or summarized.
- Coined phrases — "the ratchet, not the ruler", "scanner twins", "the doubled-file Read" — carry real meaning but are never defined here. The last is the measurement method behind the headline token numbers, so it especially deserves a sentence.

None of this is wrong, and the density is clearly deliberate. But the same content reads much more easily if each code is replaced by what it decided ("the principle ships as a section, not as a tool-only change"), each cross-reference says in a clause what it refers to, and the measurement method gets one plain sentence. Concretely: "the Phase 0 pair is measured by the doubled-file Read at 24,842 tokens" becomes "the two files a session must read at orientation measure 24,842 tokens together — measured by concatenating them, doubling the result, reading it through the 25,000-token limit, and halving the count in the refusal." Same fact, no prior reading required.

---

## Reproduction, and what I did not check

Every result above came from a run, not from reading the code. The behavioural ones are scripted end to end — each prints what it observed beside what I recorded — at [`pr82-review-repro.sh`](https://github.com/rmsharp/methodology/blob/4ffcb25327cabc3bfcf0f76dfca39d8fd231b7ce/docs/planning/pr82-review-repro.sh) in my fork; it writes only under a temporary directory and touches no repository. Run it as `bash pr82-review-repro.sh upstream/feat/quality-ratchet`. The token measurements in section 1 are manual, since the instrument is a tool's refusal message; the script prints the exact steps and the figures to expect.

Not checked: CI (there is none); `bin/sync` of this branch into a real adopter; the fleet delta of 27 repositories; Windows; and the tokens of the release-history section separately from the rest of `CLAUDE.md`. All of it is pinned to `c84e7d96` — if the branch moves, re-run before relying on any of it.
