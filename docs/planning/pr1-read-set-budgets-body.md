**Base: `read-set-budgets`, not `main`.** This is the first of four PRs staged on that branch so your
developers can test the file-size-budget work selectively. Nothing here is proposed for `main` yet.

## What this does

Extracts the Learnings table out of `starter-kit/SESSION_RUNNER.md` into a new distributed sibling,
`starter-kit/FRAMEWORK_LEARNINGS.md`, read on demand instead of on every session.

The Phase 0 mandatory read is the `SESSION_RUNNER.md` + `SAFEGUARDS.md` pair:

| | `SESSION_RUNNER.md` | `SAFEGUARDS.md` | pair | vs the 56,750 B read-set ceiling |
|---|---|---|---|---|
| before | 65,140 | 15,386 | **80,526** | 23,776 **over** |
| after | 52,195 | 15,386 | **67,581** | 10,831 **over** |

**−12,945 B (−16.1%), which clears 54% of the overage and does not eliminate it.** The remaining
10,831 B is what the later PRs on this branch are for. I would rather state that than let the table
imply the budget is fixed.

The new file is 56,673 B, class `on-demand`, ceiling 73,728 B — 17,055 B of headroom.

Also included: a scope repair to `bin/check-learnings`, whose row-budget exemption applied to the
wrong set of rows, plus the compaction it then drove.

## Verification

Run in fresh `--no-local` clones, control at `512c2ed` (= `read-set-budgets` at the time of writing),
never in a live tree. Every exit code read bare on the next line.

| | Result |
|---|---|
| Control, pristine base | **114 passed, 0 failed**, exit 0 |
| This branch | **113 passed, 1 failed**, exit 1 |
| Row-for-row | 114 rows both sides — **zero lost, zero added, exactly one status flip** |
| `bin/check-links` | exit **0** |
| `bin/check-learnings` | exit **0** — 46 rows, contiguous 1..46, 0 over 1,500 B |
| Manifest self-consistency | **25 sources listed, 25 present** |

Two further rows differ only in their label, because the label embeds the manifest count: *"all N
manifest files present"* and *"one row per manifest file (N == N)"* move 24 → 25 and **pass on both
sides**.

### The one failure, declared

`Test 9: github source dry-run` fails on this branch, and it will keep failing on
`read-set-budgets` until the branch merges to `main`. This is by construction, not a regression:

- The branch adds manifest row 25 for `starter-kit/FRAMEWORK_LEARNINGS.md`.
- `bin/sync --source=github` reads **`main`** — `bin/sync:93` issues `gh api .../contents/{src}` with
  no `?ref=`, so it resolves the default branch, and `:162` is literally `.../commits/main`.
- So the row points at a file GitHub cannot serve yet, and `fetch_all_github` exits before writing.

The tree itself is self-consistent (25/25 above), which is exactly the condition that makes this heal
the moment the content reaches `main`.

## ⚠ For anyone testing this branch

**Do not verify it with `bin/sync --source=github`.** Because of the pin above, that command syncs
**`main`'s** files while you believe you are testing this branch — it will not error, and it will look
clean. Use `--source=local` from a checkout of the branch.

That is the same species of failure as issue #75: a criterion demonstrated on a surface that cannot
fail the way the real one does. Teaching `bin/sync` to accept a ref is a small change, but it touches a
distributed file, so it belongs in its own PR rather than riding along here.

## A false claim in the ledger entry, corrected in this commit

The entry this change adds to `CHANGELOG.md` originally declined a ~400 B clarifying note on the
grounds that it *"would cost ~400 B against 77 B of remaining headroom under the 56,750 B one-read
cap, and would break the file's byte-identity with the fork, which is what lets `bin/sync` agree from
either source."* Both halves are wrong and are rewritten here rather than shipped:

- **56,750 B is the `read-set` class total** — the Phase 0 pair — and was never this file's ceiling.
  The file's class is `on-demand` at 73,728 B, so the real headroom is **17,055 B**, not 77 B.
- **`bin/sync` never consults a local ref.** `read_local` reads a working tree (`bin/sync:52`);
  `read_github` reads this repository. Nothing compares them, and the two already differ on several
  tracked files in every adopter measured.

The note is therefore deferred as *content*, not declined as *unaffordable*.

## Disclosures

- **10 of the 46 rows name artifacts that do not exist in this repository** (`.context-budget.json`,
  `methodology_trim.py`, `docs/planning/BACKLOG.md`, `docs/audits/…`, `.verify.sh`, two `BACKLOG.md`
  paths). None is a broken hyperlink — they are prose code spans, which is why `bin/check-links` is
  green and correctly so: it strips inline code, so its green says nothing about them.
- **32 of the 46 rows cite session numbers S35–S119** from the fork's sequence, which runs separately
  from this repository's and collides with it.
- **The table is frozen at 46 rows** — the compacted state — rather than refreshed from the fork's
  current 48. Refreshing would falsify three derived counts in the entry with no checker to catch it.
  Say the word if you would rather have the newer table.

## What is deliberately not here

The other three budget payloads — the ledger trimmer, the `FRAMEWORK_APPARATUS.md` extraction, and the
`context_budget.py` size gate — each land as their own PR on this branch, in that order. The trimmer
goes before the apparatus extraction because the dashboard's canonical-only tests require the trimmer
to be present; without it they abort with 13 errors rather than fail informatively.

Each PR lands its `bin/_manifest.py` row together with its file, so sources-listed equals
files-present at every step (24 → 25 → 26 → 27).

---

_Authored by an AI agent under the operator's direction; every figure above was re-derived in this
session rather than carried forward. Review before relying on it for human-facing work._
