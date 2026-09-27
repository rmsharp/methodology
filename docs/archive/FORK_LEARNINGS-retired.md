# Fork Learnings — retired rows

Rows retired from [`../FORK_LEARNINGS.md`](../FORK_LEARNINGS.md) under **D1** of
[`../planning/fork-learnings-retirement-rule-plan.md`](../planning/fork-learnings-retirement-rule-plan.md) §6,
by the **D2 reserved-gap mechanism**: the row's text moves here **verbatim**, the live file gains one
`` > **`#N` is reserved …** `` line, and **numbers never change** — neither here nor there. A retired
number is never reused, so every citation of every row keeps resolving.

**A row retires only on a cited criterion, never on age or file size** (D1): **(a)** a gate in
`.quality-gates.json`, a test in `bin/tests.sh` or a numbered failure mode now enforces its lesson;
**(b)** a later row states that lesson at least as generally; **(c)** the artifact, tool or defect it
is about no longer exists. **The retiring commit cites which** — and a criterion is the only ground.
Age and file size are never grounds, which is why this file is short and why that is not a defect.

**This file was created at the first retirement, 2026-09-27 (S225).** Before it, no row had ever
retired. S200 adjudicated all 69 then-existing rows against the ratified criterion and retired
**none** ([`../planning/fork-learnings-adjudication-2026-09-20.md`](../planning/fork-learnings-adjudication-2026-09-20.md) §5
carries the row-by-row basis; read it before re-adjudicating anything), and S221–S224 each appended a
row and **refused** under D3, naming the rows they had considered.

**Newest first.** Each entry states the criterion and its citation, then the row exactly as it stood.

---

## `#85` — retired 2026-09-27 (S225), criterion (b): superseded

**Superseded by `#98`**, which states the lesson at least as generally — *grep for the behaviour a note
asserts, not the fields it names* — and corrects the example this row got wrong. The row's central
claim is false: it says the `.context-budget.json` ratchet *"does not exist"*, and it does, as
`def precommit` (`starter-kit/context_budget.py:1000`, byte arm `:1037`). It is merely unwired in this
clone — nothing in `.githooks/pre-commit` or `.quality-gates.json` calls it.

Raised as **BL-83** at S216, where the claim was first measured false. **Re-measured at S225 in a
`--no-local` clone at `28c24d3`** rather than inherited: nothing staged → exit 0; a staged growth of
`starter-kit/SESSION_RUNNER.md` → `context-budget: REFUSED`, **exit 2**; a staged shrink → exit 0.

Its *Repair* advice — grep the tool for every field the note names — is sound, and following it is how
S201 reached the wrong answer: the note's claim rests on `max_bytes`, which the note never names. That
is the correction `#98` carries. Note also that **`#86` inherited this row's false premise** the day
after it was written; `#86` stays live, its own lesson being sound.

**The row, verbatim as it stood at `28c24d3`:**

| # | Learning | Source | When to Apply |
|---|----------|--------|---------------|
| 85 | **A config's note can describe an enforcement the tool does not implement — grep the tool for the field before citing the note as a control.** A budget entry declared *"every commit that grows it is refused while every commit that shrinks it passes: a ratchet, not a wall"*, and two sessions read that as an enforcement merely not wired into the commit path. It is not wired **and it does not exist**: the field that sentence rests on, `measured_bytes`, appears **once** in the tool and feeds **only** a density-drift warning, itself gated on `status == "ok"` — so for a file already `over` it emits nothing. The only growth signal is a series over one other field entirely, which is why its run counter read **159** while both governed files grew past their declared sizes. **The tell is grammatical:** the note is present indicative (*"is refused"*) but names no command, gate or exit code — prose asserting a behaviour instead of citing what performs it. **Repair:** before a remedy is costed as *wire the existing check*, grep the tool for every field the note names and read each use; a shape that must **build** the check is a different size of work from one that must enable it. | S201 (2026-09-20), a Phase 0 budget finding: the ratchet two sessions had called unwired turned out to be absent | Any config or front-matter note stating what happens on violation. Also any backlog item whose remedy is phrased as enabling something already written. |
