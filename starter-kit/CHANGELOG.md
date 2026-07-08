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
recommended:

```
### YYYY-MM-DD · [SOURCE] one-line outcome-focused summary
- **Change:** what is now true in the repo/product that was not before
- **Commit/PR:** `<short-sha>`  —or—  PR #<N> (merged `<sha>`)
- **Session:** S<N> · **Verified:** <build/test/render/runtime evidence, or "n/a — docs-only">
```

*(The `[SOURCE]`, `[issue #<N>]`, `[BL-<N>]`, and `[ad hoc]` tokens above are illustrative; the
freshness check keys on dated `###` entries, of which a fresh seed has none.)*

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
