Closes #75.

The checklist line you drafted, plus the requirement it verifies — and a test that pins the two together.

## What changed

`starter-kit/SESSION_RUNNER.md`, two sites:

- **§Per-Phase Completion Criteria** gains a `**The surface**` bullet — *where* the DONE criterion will be demonstrated, and what that surface **cannot** enforce — followed by a paragraph anchoring it to §Vertical Slice Sessions gate (d), and the adoption note citing this issue.
- **§Planning Session Checklist** gains your line, unmodified in substance. Six items → **seven**.

`bin/tests.sh` gains **Test 26** (canonical-only; upstream already has this file). `CHANGELOG.md` gains the ledger entry FM #27 requires.

## Why two sites and not the one line

All six pre-existing checklist items mirror a requirement stated in a section above them — I checked that mechanically rather than assuming it. Your line alone would have been the list's only orphan. So the requirement is **stated** in §Per-Phase Completion Criteria and **verified** by the checklist, matching the shape already there.

This is the one place I departed from your diff, and it is the thing to push back on if you disagree. Reverting to the single line is a two-line edit and the test's assertion (2) is what would then fail — deliberately, since it asserts exactly this property.

## The finding that shaped it: the framework already owned this doctrine, as an orphan

§Vertical Slice Sessions gate (d) — *"Faithful verification, per surface"* — already says faithfulness is established and never assumed. That **is** the principle this issue asks for, already ratified. What failed was **reachability**, in two coordinates:

- **Who it binds.** Gate (d) belongs to the *elective* vertical-slice allowance, so it reaches only sessions that opted into a slice. The 3-phase plan in your report was an ordinary plan; gate (d) never applied to it.
- **When it fires.** Even inside a slice it binds only once a layer is built — which is *after* the last moment naming the surface could have changed the plan.

Measured on `main` before the change, both spellings, because one spelling is one sample:

```sh
git grep -c "Faithful verification, per surface"   # 1  — its own definition
git grep -n  "gate (d)"                            # 0
git grep -n  "gate d"                              # 1  — and that one is INSIDE gate (d)'s own section
```

No line outside §Vertical Slice Sessions referred to it at all. So the fix here is not a new rule: it **projects gate (d) to plan time by quoting it**. Two copies of one rule drift apart; a quotation cannot. They are one rule at two times — the plan names the surface, the implementation establishes that it is faithful.

## Test 26 is a coupling guard, not a presence grep

Quoting gate (d) creates a citation that can dangle: rename or move the gate and the new prose silently quotes a rule that no longer exists under that name — both halves still "present," the reference broken. **A test that greps for the added lines survives that mutation.** So one of the five mutants renames the **gate** and leaves the citation untouched.

Six assertions, five mutants, every mutation vacuity-checked by the existing `mutate` helper. Both section populations are guarded before any absence is believed — an absence computed over an empty set is vacuously "clean" — and a fifth mutant renames a heading to prove that guard itself fires rather than trusting it. (That guard was not theoretical: while this test was being written, a `re.S` without `re.M` made every section extract to `""`, and the guard caught it on the first run instead of reporting a green.)

Driven RED first: with the test added and the runner unpatched, 5 of its 6 rows fail.

## Verification

Run on a branch built from `main`, not on the fork it was authored in:

| Stage | Result |
|---|---|
| Pre-change control, pristine tree | 114 passed / 0 failed |
| RED — test added, runner unpatched | 5 of Test 26's 6 rows fail; populations non-empty (`crit=390 items=6 slice=5469`) |
| GREEN — final state | **120 passed / 0 failed** |
| Row-for-row diff vs. control, both populations non-empty | exactly **6 rows added, zero lost** |
| `bin/check-links` | OK — 83 links / 21 distributed files |
| `bin/check-learnings` | OK — 13 rows, contiguous 1..13 |
| Adopter smoke — `bin/sync` into a fresh repo | delivered `SESSION_RUNNER.md` byte-identical; 7 checklist items; **both** occurrences of the quoted phrase, so the citation's referent travels in the same file and cannot dangle at an adopter merely by being synced |

**What none of this exercises:** GitHub delivery, review, or merge. Naming that is the requirement this PR adds, applied to itself.

## Two things deliberately left out

- **A Learnings row.** The generalization — *a rule is only as reachable as the section it sits in, and its inbound-citation count says which sessions it binds* — belongs in the Learnings table, but that would edit a numbered set Tests 23/24 pin, in a PR about something else. Happy to send it separately if you want it.
- **The two *Related* items from your issue** (Phase 3E naming the surface; `runtime_smoke` leading with it). Both are about the *other* end — whether the named surface survives into the record a successor reads. They touch two further distributed files plus `ITERATIVE_METHODOLOGY.md`, and the `runtime_smoke` half changes a documented field format existing receipts were written against. Sequenced, not dropped.

## Honest caveat

This is a **requirement, not a gate**. Nothing refuses a plan that omits its surface — the checklist is read by an agent following a procedure, and an agent that skips the line is the failure mode the Degradation Detection table exists for. That is this repo's own standard turned on this proposal, and worth saying out loud rather than leaving you to notice.

---

_Authored by an AI agent during a session on the `rmsharp` fork — review before relying on this for human-facing work._
