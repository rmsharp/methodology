I went through this branch at `c84e7d96` and re-ran its own checks before questioning any of them. Everything I could check reproduced: in a fresh clone, `quality_ratchet.py --run` gave **9/9 pass with results hash `74c773523dab`** — the same hash the receipt in `HANDOFFS.md` cites, so that hash really is reproducible on another machine; `--selftest` observed all 17 checks; `bin/tests.sh` printed `134 passed, 1 failed` (test 9, by construction, as you say); `context_budget.py --status` exited 0; no tracked file changed. `--precommit` refused every loosening it claims to refuse.

My main suggestion is about the description rather than the code, so I've put it first and written it as text you could lift. Everything after it uses the vocabulary that section establishes. All of it is measured at `c84e7d96` and reproducible — see the last section.

---

## 1. The description needs a plain statement of purpose, approach and mechanism

I had to read the plan alongside the PR to follow it, and I don't think a reader should have to. The description opens on decision codes (`D1`–`D10`, `P0`, `G1`), cross-references that aren't summarized ("the #80 shape", "the PR #71 discipline"), and coined phrases used before they're defined ("the ratchet, not the ruler", "scanner twins", "the doubled-file Read" — the last is the measurement method behind the headline numbers, so it especially needs a sentence). Each one is resolvable if you've read the plan. None is resolvable from this page.

More importantly, **the description never says plainly what a quality gate is, or why the thing is called a ratchet.** Here is a rewording that tries to. Take it as a starting point, not a correction — the facts are yours, only the framing is mine.

> **The problem.** Almost every quality check in this methodology is a question the session asks itself: *did the tests pass? is the handoff specific enough? is the file still small enough?* Whoever is running answers it, and the answer moves with how careful, how hurried and how capable they are. Putting a better reviewer on the job does not fix that — it produces a better answer to the same kind of question. What is weak is the *class* of check, not the judge answering it. That is this PR's thesis: **enforce quality on the artifact, not on the actor.**
>
> **The approach: restate some of those standards in a form a program can evaluate.** Note what this is *not*. It is not "write the standards down" — they are written down already, at length, and this repository is mostly made of them. The change is narrower: a standard stops being a question a person or agent answers and becomes a measurement a program takes. A new file at the repository root, `.quality-gates.json` — the **manifest** — holds them. Each entry is a **gate**: a name, a command to run, and a number the result must clear. *Run `bin/tests.sh`, read the number of passing tests, require at least 134.* Where there is no number to read, the command's exit code is the measurement, so *"this check must exit 0"* is expressible too. Gates are declared **at the values the repository measures today**, not at aspirational ones, so the manifest is green the day it lands.
>
> **What that buys, beyond consistency: the bar acquires a history.** This is the part that makes a ratchet possible at all. A judgment leaves no trace of *how strict it was.* If one session required 134 passing tests and the next quietly settled for 120, no artifact anywhere changed — there is nothing to compare, so there is nothing to notice, and the standard can erode without any single moment where it visibly moved. A number in a committed file is a versioned object with an author, a date, and a diff. **You can only refuse to let a standard slip if the standard is a thing that has a former self.**
>
> **What the number does.** A gate's number is a pass/fail boundary, and its direction says which side passes: *at least* means the measurement must reach the number, *at most* means it must stay under. The number is only meaningful together with the command, which decides *what quantity* is being measured — the same number against a different command is a different claim entirely. Two separate parts of the system read that number, and they work differently.
>
> **When you run the gates,** `quality_ratchet.py --run` executes each gate's command, pulls the number out of its output, and applies the boundary. That is what says whether the repository is green today, and it is the number's ordinary, obvious job.
>
> **When you commit, and this is the ratchet:** the pre-commit hook runs `quality_ratchet.py --precommit`, which **runs no commands at all.** It reads two versions of the manifest — the one you are about to commit and the one already committed — and compares them field by field. If a gate disappeared, if a direction flipped, if an *at least* number went down or an *at most* number went up, **the commit is refused.** Nothing is measured; the hook is reading your edit, not its consequences. That is precisely why it works as a ratchet: it doesn't need to know whether the tests pass, only whether you have just made it easier for them to count as passing. Teeth that let the wheel turn forward and catch it turning back — declared quality can rise freely and cannot quietly fall.
>
> **Where that guarantee stops.** Because the check is a comparison of declarations rather than of results, it holds **thresholds, not measurements.** Changing a gate's *command* is therefore a warning rather than a refusal: the tool has no way to know whether the new command is easier than the old one without running both. Loosening on purpose also remains possible with `git commit --no-verify` — which leaves a deliberate, reviewable act in the history instead of a silent edit, and the tool prints what the bypass costs before you take it.
>
> **What you see.** `--run` also prints a one-line summary of the whole set, which sessions paste into their close-out receipt — so "everything was green" arrives with its own evidence attached rather than as an assertion. The dashboard reads the manifest, the most recent run, and the manifest's own git history, and flags any threshold that was lowered, naming the commit that did it.
>
> **Scope.** The tool ships to adopters with an **empty** gate list, deliberately: a ratchet starts where a project actually is. This repository declares nine gates for itself as the first worked example. Adopter rollout and the release are separate, later steps.

Two notes on that rewording. It drops every decision code — where one mattered I'd state the decision instead ("the principle ships as a section, not as a tool-only change"). And it spends its middle on the two things I could not reconstruct from the description alone: *why* a number in a committed file differs from the same standard held as a judgment, and *what the pre-commit check actually compares.* Everything else in this comment follows from that second answer, which is why it's worth the space.

---

## 2. Three ways the ratchet can still turn backwards

Everything above follows from one design choice: the ratchet compares two *declarations* — the manifest you are committing against the manifest already committed. That is what makes it cheap and unarguable, and it also draws the boundary of what it can protect. Three gaps follow from that boundary directly: the comparison can be made not to happen at all (a); it can be guarding a number whose underlying quantity barely tracks quality (b); and the record that the gates were ever actually run is checked only for shape (c). I ran all three in scratch repositories rather than reading them off the code.

### (a) Removing the whole manifest is treated as nothing happening

A comparison needs two sides. Delete `.quality-gates.json` and there is no second side — and every part of the system reads that absence as a non-event rather than as the largest loosening available:

- the pre-commit hook runs the tool only when `.quality-gates.json` is present in the working tree, so deleting it skips the check entirely;
- even when the tool does run, `precommit()` returns clean the moment it finds no manifest in the commit ("manifest not in this commit: nothing to ratchet");
- the dashboard's history walk reads the manifest at each commit that touched it, and a commit that *deleted* it fails to parse — so that version, **and both pairs it sits between**, are skipped rather than read as "every gate removed."

**What I ran.** A scratch repository with one gate reading *"at least 5"*, and the hook chained exactly as this PR chains it. Committing each step in turn:

| Step | Result |
|---|---|
| Edit the gate from *at least 5* to *at least 4* | **Refused** (exit 1) — the ratchet works |
| The same, with `--no-verify` | Allowed, as designed — a recorded bypass |
| Delete `.quality-gates.json` | **Allowed** (exit 0) |
| Re-add it reading *at least 1* | **Allowed** (exit 0) — "first manifest commit, nothing to compare against" |

So the gate went from *at least 5* to *at least 1* in two ordinary commits, neither of which was refused and neither of which needed a bypass. Afterwards the dashboard reported exactly one thing: the 5 → 4 attempt that had already been refused. The 5 → 1 that actually happened appears nowhere.

*Suggested:* refuse in `precommit()` when the previous commit had gates and the new one has no manifest at all, with a message like "manifest removed"; run the hook whenever the manifest is tracked in `HEAD`, not only when it's on disk; and in the dashboard, read a failed parse at a deletion as an empty gate set — `_gate_loosenings` already has a "removed" branch, it just never reaches it.

### (b) Most of the gates count tests rather than check them

This is the case the boundary above matters for. The ratchet guards these four numbers perfectly; the trouble is what the numbers are attached to. Four of the nine gates measure `Ran (\d+) tests` — how many test methods **executed**, not how they turned out. A failing test still ran. A skipped test still ran. So those four numbers track the size of the suite and are blind to its health, and holding them steady holds nothing steady.

**What I ran.** Three gates, each requiring *at least 3*, pointed at deliberately sick suites:

| Gate's command | Reality | Gate said |
|---|---|---|
| A suite of 3 tests, 2 of them failing | red | **pass** |
| A suite of 3 tests, all 3 skipped | nothing verified | **pass** |
| A command printing `134 passed, 1 failed` | red | **pass** |

`--run` reported **3 of 3 passing and exited 0.**

The manifest's own note anticipates this and says pass/fail is carried by the gate that counts *passing* tests instead. That holds only while the suite doesn't grow: one new passing test exactly offsets one new failure, and the count gate never dips. The gate that would actually catch it — `tests-sh-failed` at *at most 0* — is deferred until after the merge, because test 9 fails on the branch by construction.

*Suggested:* the deferral isn't necessary. **Declare `tests-sh-failed` now at *at most 1*** — the value the branch genuinely measures, which is what the manifest says gates should be declared at. It's green today, it catches a *second* failure immediately, and it tightens to 0 in the first commit after the merge, which is a tightening and so needs no approval. Separately, pairing each count gate with an exit-code gate on the same suite would make a red suite fail its own gate. That would also relieve a side effect of counting that the plan itself warns about ("'130 checks' is a count, not a target"): with five of nine gates counting tests, deleting a dead or duplicated test is a loosening that needs plan-mode approval.

### (c) The evidence in the receipt is checked for shape, not for content

The close-out receipt is supposed to carry proof that the gates were run. `bin/check-handoff` enforces that by looking for text matching `quality_ratchet: <number>/<number> pass`.

**What I ran.** Three versions of the newest receipt:

| The receipt says | Checker |
|---|---|
| `quality_ratchet: 9/9 pass` (as published) | passes |
| `quality_ratchet: 0/9 pass` — every gate failing | **passes** |
| nothing at all | fails |

So the check confirms a sentence is present, not that it says anything good.

The plan asked for more than that — *"a lint that the citation resolves … Phase 0 reconcile compares the newest receipt's claim to the newest results"* — and the description says Phase 0 performs that comparison. It doesn't: Phase 0 in `starter-kit/SESSION_RUNNER.md` is byte-unchanged by this PR (the runner's diff touches only the Phase 3C, Phase 3E and failure-mode sections), and the results file is gitignored, so a fresh clone has nothing to compare against anyway.

**Worth stating plainly, because it's the good news:** the comparison itself is sound. The results hash deliberately excludes the commit and the timestamp, and my clean-clone re-run reproduced the published `74c773523dab` exactly. The mechanism works; nothing currently runs it.

*Suggested:* have the checker require that the cited numbers say *0 failed, 0 unmeasured, and as many gates measured as the manifest declares* — cheap, local, and it turns the citation from a formality into a claim. Then either add the comparison to Phase 0 as an actual numbered step, or give the tool something like `--status --expect <hash>`. If neither is wanted, say in the docs that the citation is checked for shape only, so nobody relies on more.

---

## 3. Two file budgets are measured in bytes where tokens is the operative unit

Separately from the gates, this repository already budgets the *size* of the documents a session must read, because the read tool refuses any single file over 25,000 tokens and the always-loaded file costs tokens on every session. That budget is what this PR's "pays for its own growth by reduction" claim is measured against — and in two places it's measured in bytes, which can move opposite to tokens.

**How I measured tokens.** I concatenated each file with itself, read the result through the tool that refuses anything over 25,000 tokens, and halved the number in its refusal message. I checked the instrument before trusting it, by reproducing three figures already recorded in this repository exactly (48,555, 49,683 and 36,955).

**`CLAUDE.md`: the reduction went the other way.** Against the byte pin the claim holds — 59,168 → **59,153 bytes, 15 under**. Measured in tokens the same change is **23,420.5 → 23,482.5: 62 tokens larger.** The file grew in the unit that costs, and shrank in the unit that's checked. That isn't a fluke: bytes-per-token depends on content, and the new table rows are dense with backticked paths, which tokenize at fewer bytes per token than the prose that was shortened to pay for them. A byte pin structurally cannot see this. It's the same substitution PR #80 already made for the two orientation files, where a byte ceiling became per-file token ceilings at measured densities.

Two supporting facts:

- The budget tool judges this file at **2.93 bytes/token** — the seed's fallback, and `.context-budget.json` says outright that the value is inherited rather than measured here. Measured on this branch it is **2.519**. So the tool reports 20,188 tokens where there are 23,482.5 (**14% low**) and shows about 4,800 tokens of headroom where there are about 1,500.
- Worth knowing what the pin is mostly pinning: **87% of the file's bytes** (51,617 of 59,153) are release history below `## Versioning`. Whether that belongs in a file injected into every session is a larger question than this PR.

*Suggested:* measure this file's density and declare a token ceiling — 23,483 if a no-growth pin is the intent — keeping the byte figure only as a coarse backstop.

**`starter-kit/SESSION_RUNNER.md`: right unit, stale number.** This file *is* budgeted in tokens, which is the right call. The density 2.8248 was measured correctly in `008d656`, against the file as it stood at that commit (52,195 bytes). The **next** commit, `628d218`, edited that same file to 53,301 bytes, and `b4226d3` took it to 53,328 — and the density was never re-measured. The config comment still describes the measured version as "this branch's file", which it stopped being two commits later.

The gap is small but points the wrong way. Measured against the current file, the runner sits at **18,897.5 of its 18,900-token ceiling — 2.5 tokens of room**, not the 22 the tool reports and the description repeats. Because the tool divides by the stale density it would admit growth to 53,391 bytes, which actually measures about **18,920 tokens, roughly 20 over the ceiling the config itself declares.** The guard meant for exactly this, `measured_bytes`, only warns at 25% drift — about 13,000 bytes away, against a real margin of 2.5 tokens.

*Suggested:* re-measure and record 53,328 bytes at 2.8220, and consider tying a density to the specific file version it was measured on so that editing the file invalidates it. Practically: after this PR, every edit to that file has to be net-negative in tokens.

**And no gate covers any of it.** `context_budget.py --status` is the actual verdict on every budget above, and it is not one of the nine gates, not in the pre-commit hook, and not run by `bin/tests.sh` — which runs that tool's self-test and unit tests but never `--status` against the tree itself. So a commit that breaks the read budget passes every gate this PR declares. It exits 0 today, so declaring it costs nothing:

```json
{ "name": "context-budget", "direction": "max", "threshold": 0,
  "command": "python3 starter-kit/context_budget.py --status",
  "why": "exit code: every declared file and class within its budget" }
```

That is also this PR's own new rule turned on itself — the Phase 3C branch it adds says a mechanical invariant belongs in a gate rather than in a written row.

---

## 4. Four smaller things

- **Backing out of the ratchet locks the repository.** The hook that `install-hook` writes calls the tool unconditionally, and with no manifest the tool exits 3. So after someone deletes the manifest with `--no-verify`, **every later commit is refused**, including unrelated ones, with *"no `.quality-gates.json` found … refuses to invent thresholds"* — a message that doesn't say what to do about it. An adopter who tries the ratchet and backs out can't commit again without `--no-verify` every time. *Suggested:* when there's no manifest in the commit, pass cleanly if the previous commit had none either, and refuse with (a)'s "removed" message if it did.

- **The dashboard misses two loosenings the tool catches.** It reports a changed threshold only when the direction stayed the same, and it ignores commands entirely. A direction flip (*at least 5* → *at most 5*) is refused by the tool but **reported as nothing**; swapping a gate's command for `echo 'Ran 999 tests'` is warned about by the tool and **reported as nothing**. That matters because the bypass message promises the opposite: *"the manifest's git history shows the loosening and the dashboard reports it as a risk."* A bypassed flip leaves no advisory at all. *Suggested:* report flips as loosenings, and command or extract changes as "gate redefined" at low severity.

- **The coverage bonus rewards a gate's name.** The dashboard awards +2 testing points when a *passing* gate's **name** matches "coverage". A gate named `coverage` whose command is `echo 100` earns it — I checked. The plan explicitly declined "any coverage floor without a faithfulness check beside it", and this rewards exactly that, from a file that is locally written and gitignored. *Suggested:* drop the bonus until a faithfulness gate is required alongside, and either way don't key on names.

- **`install-hook` breaks every commit in a fresh clone of this repository.** It exits 0, and then the next commit fails with *"can't open file `<root>/quality_ratchet.py`"* — because the tool lives under `starter-kit/` here, and a fresh clone has no `core.hooksPath` set. `.context-budget.json` already carries exactly this warning for the sibling tool ("DO NOT RUN `install-hook` HERE", with the `rm .git/hooks/pre-commit` recovery); `.quality-gates.json` carries none. *Suggested:* add the same warning, or have `install-hook` write the path of the file that's actually running.

---

## 5. One thing about who is bound

The new section says the mechanical form "binds every actor: every tier, every agent, every human, every session". What enforces it today is a pre-commit hook that each clone opts into separately by setting `core.hooksPath`, that `--no-verify` bypasses, and that (per section 2a) disappears with the manifest — in a repository with no CI. That's a gap between the claim and the mechanism rather than a defect in the code, and I raise it only because the claim is doing real work in the argument. A CI job running `--run`, plus the ratchet comparison against the base branch, is what would bind someone who never sets a hook. Short of that, I'd state the enforcement point plainly in the section itself, so the claim and the mechanism match.

---

## Reproduction, and what I did not check

Every result above came from a run, not from reading the code. The behavioural ones are scripted end to end, each printing what it observed beside what I recorded: [`pr82-review-repro.sh`](https://github.com/rmsharp/methodology/blob/4ffcb25327cabc3bfcf0f76dfca39d8fd231b7ce/docs/planning/pr82-review-repro.sh) in my fork. It writes only under a temporary directory and touches no repository. Run it as `bash pr82-review-repro.sh upstream/feat/quality-ratchet`. The token measurements in section 3 are manual, since the instrument is a tool's refusal message; the script prints the steps and the figures to expect.

Not checked: CI (there is none); `bin/sync` of this branch into a real adopter; the fleet delta across 27 repositories; Windows; and the release-history section's tokens separately from the rest of `CLAUDE.md`. Everything is pinned to `c84e7d96` — if the branch moves, re-run before relying on any of it.
