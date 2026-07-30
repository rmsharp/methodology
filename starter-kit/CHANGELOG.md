# Changelog — Authoritative Action Ledger

The cumulative, append-only record of **actions taken** in this repository — across backlog
items, repository issues, and ad-hoc work. It is the authoritative answer to *"what was done
here, ever?"* Every session records its actions here at close-out (`SESSION_RUNNER.md`
Phase 3F); Phase 0 reconciles it against `git log` and backfills anything a crashed or
out-of-band session missed. Taking an action — any commit, or any non-commit action — and
not recording it is failure mode #27.

<!-- METHODOLOGY-SEED-SENTINEL: fresh ledger, no entries yet. While this line is present AND
     there are no dated (### YYYY-MM-DD) entries below, this is a freshly-seeded ledger, not a
     stale or abandoned one — the freshness check keys on this exact token plus the absence of
     any `### <real-date>` header. Delete this line when you add your first real entry. -->

## How to add an entry

At close-out, prepend one entry per action, **newest on top**. Key on a mechanical fact, not
judgment: *did this session author or retain any commit, or take any non-commit action?* If
yes, an entry is owed — "too small to log" or "I'll batch it next time" **is** failure mode
#27, not an exception. The only exemption is a session whose diff is empty and that took no
action at all.

**Source tag — exactly one per entry, from this closed vocabulary** (so the audit
`grep -E '\[(issue #|BL-|ad hoc)' CHANGELOG.md` enumerates every logged action and proves all
three sources landed):

- `[issue #<N>]` — a repository issue. If issues live in another repo (e.g. an upstream parent
  of a fork), cite an absolute URL, not a bare `#<N>`.
- `[BL-<N>]` — a `BACKLOG.md` item. Remove it from `BACKLOG.md` in the same commit.
- `[ad hoc]` — work with no backlog or issue origin (the source most prone to vanishing):
  releases, tag/branch ops, PR opens, upstream issue closes, access grants, and
  decline/wontfix/grooming decisions all land here.

**Format** — the `###` header line is the required, greppable unit; the detail bullets are
recommended, plus one further bullet, `Model`, that is optional even relative to the others:

```
### YYYY-MM-DD · [SOURCE] one-line outcome-focused summary
- **Change:** what is now true in the repo/product that was not before
- **Commit/PR:** `<short-sha>`  —or—  PR #<N> (merged `<sha>`)
- **Session:** S<N> · **Verified:** <build/test/render/runtime evidence, or "n/a — docs-only">
- **Model:** <acting model> (optional — omit the line entirely when not recorded)
```

*(The `[SOURCE]`, `[issue #<N>]`, `[BL-<N>]`, and `[ad hoc]` tokens above are illustrative; the
freshness check keys on dated `###` entries, of which a fresh seed has none.)*

**Model:** — self-reported, free text; omit the line when not recorded. Names which model
executed the action — an agent-independent key with a concrete value, the same pattern
`key_files` already uses for paths. Single-tier work names one model:

```
### 2026-01-15 · [ad hoc] Ship the export-retry fix
- **Change:** exports now retry once on a transient network error instead of failing immediately
- **Commit/PR:** `a1b2c3d`
- **Session:** S42 · **Verified:** unit suite green, manual retry reproduced and confirmed fixed
- **Model:** <model>
```

Capability-tiered work (one session whose layers are built or reviewed across different tiers) is
recorded *per entry*, not compressed into one line: each layer/checkpoint already gets its own
`CHANGELOG.md` entry, so each entry's **Model:** bullet states only its own role:

```
### 2026-01-16 · [ad hoc] Layer 3 — draft the parser (delegated layer)
- **Change:** the new input format parses without a follow-up fixup pass
- **Commit/PR:** `d4e5f6a`
- **Session:** S43 · **Verified:** unit tests for the new parser pass
- **Model:** <model A> (delegated; reviewed by <model B>)

### 2026-01-16 · [ad hoc] Layer 4 — review and land the parser (primary layer)
- **Change:** the delegated layer's diff is reviewed and the checkpoint committed
- **Commit/PR:** `b7c8d9e`
- **Session:** S43 · **Verified:** full suite green after review fixes
- **Model:** <model B> (primary)
```

`HANDOFFS.md`'s "How to write a receipt" section documents a complementary session-level
convention: naming the model once in a receipt's free-text prose, for a reader who wants one
session's answer without correlating multiple entries here. That convention adds no new
`HANDOFFS.md` schema key — it is not a second, competing structured field, and it is fine for both
files to name the same model for a single-tier session, since they answer different questions
("what happened, action by action" vs. "which model ran this session"). A canonical-only
`bin/model-report` (copy it into your `bin/` if you want it) reads this file's **Model:** bullets
back alongside `HANDOFFS.md`'s free-text mentions and git's `Co-Authored-By` trailers, keeping all
three visually separate — see that tool's own docstring for why trailers are corroboration-only,
never authoritative.

Work committed but not finished — an in-progress hand-off, a reverted slice — still owes an
entry: mark it `(in progress)` in the summary, and a later session closes it out or records
the revert as its own entry. Reverse-chronological, prepend-only, so close-out never re-sorts.
Promote to `## YYYY-MM` sections as the list grows — group by month, **not** by release.

## CHANGELOG.md vs SESSION_NOTES.md — two files, two questions, one shared key

`SESSION_NOTES.md` is the **transient handoff** — *"what's next, what traps?"* — overwritten
every session. `CHANGELOG.md` is the **cumulative ledger** — *"what was done, ever?"* —
append-only. The commit SHA is the only intended intersection. Close-out **distills** the
durable outcome into a ledger entry; it does not copy the handoff. The belongs-here test:
*would the operator, six months out, need this to know what the repo does or how it got there?*

---

<!-- Entries go below, newest on top. Delete the seed-sentinel line near the top when you add the first one. -->
