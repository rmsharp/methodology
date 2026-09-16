# Handoff Receipt Archive — Shard Index

One row per `methodology_trim.py` trim of the root [`HANDOFFS.md`](../HANDOFFS.md). The table lived in
that file's front matter until S174 (2026-09-16), moved here with its rows unchanged: each trim added a
row, and the front matter has a fixed 7,168 B reserve (`bin/check-handoff` `HEADER_RESERVE_BYTES`,
asserted by `bin/tests.sh` Test 39 A2) that the next row would have overflowed.

**Run the proofs rather than trusting this table.** Every row's shard is
`docs/archive/HANDOFFS-through-<date>.md`, and its proof is the same path plus `.verify.sh`, which
re-derives L1/L2/L3 from git. A shard keeps the live file's format and newest-on-top order, frozen at
write. **No total is written here**, because a hand-maintained count is stale by the next trim; derive it:

```
git ls-files 'docs/archive/HANDOFFS-*.md' | wc -l                       # shard files
cat $(git ls-files 'docs/archive/HANDOFFS-*.md') | grep -c '^```handoff$'   # archived receipts
```

**One shard predates the trimmer and has no row:** [`HANDOFFS-archive.md`](archive/HANDOFFS-archive.md),
receipts dated 2026-07-08 → 2026-07-30, archived by hand with no `.verify.sh`. `bin/tests.sh` checks it
with `bin/check-handoff --archived`, and `bin/model-report` reads it with the rest.

**Do not rename this file to `docs/archive/HANDOFFS-*.md`.** `bin/model-report`, `methodology_trim.py`
and `methodology_dashboard.py` all find shards by that glob, so an index there would be read as a shard.

| n | span | shard | by |
|--:|---|---|---|
| 16 | 2026-07-30 → 2026-08-02 | [`HANDOFFS-through-2026-08-02.md`](archive/HANDOFFS-through-2026-08-02.md) | v1.1.1 |
| 30 | 2026-08-03 → 2026-08-09 | [`HANDOFFS-through-2026-08-09.md`](archive/HANDOFFS-through-2026-08-09.md) | v1.1.1 |
| 25 | 2026-08-02 → 2026-08-11 | [`HANDOFFS-through-2026-08-11.md`](archive/HANDOFFS-through-2026-08-11.md) | v1.1.3 |
| 8 | 2026-08-11 → 2026-08-15 | [`HANDOFFS-through-2026-08-15.md`](archive/HANDOFFS-through-2026-08-15.md) | v1.2.0 |
| 4 | 2026-08-15 → 2026-08-17 | [`HANDOFFS-through-2026-08-17.md`](archive/HANDOFFS-through-2026-08-17.md) | v1.2.0 |
| 3 | 2026-08-17 → 2026-08-18 | [`HANDOFFS-through-2026-08-18.md`](archive/HANDOFFS-through-2026-08-18.md) | v1.3.0 |
| 3 | 2026-08-18 → 2026-08-23 | [`HANDOFFS-through-2026-08-23.md`](archive/HANDOFFS-through-2026-08-23.md) | v1.3.0 |
| 3 | 2026-08-24 → 2026-08-24 | [`HANDOFFS-through-2026-08-24.md`](archive/HANDOFFS-through-2026-08-24.md) | v1.3.0 |
| 2 | 2026-08-25 → 2026-08-25 | [`HANDOFFS-through-2026-08-25.md`](archive/HANDOFFS-through-2026-08-25.md) | v1.3.0 |
| 17 | 2026-08-25 → 2026-08-29 | [`HANDOFFS-through-2026-08-29.md`](archive/HANDOFFS-through-2026-08-29.md) | v1.5.0 |
| 5 | 2026-08-29 → 2026-08-30 | [`HANDOFFS-through-2026-08-30.md`](archive/HANDOFFS-through-2026-08-30.md) | v1.5.0 |
| 23 | 2026-08-12 → 2026-09-04 | [`HANDOFFS-through-2026-09-04.md`](archive/HANDOFFS-through-2026-09-04.md) | v1.5.0 |
| 2 | 2026-09-04 → 2026-09-07 | [`HANDOFFS-through-2026-09-07.md`](archive/HANDOFFS-through-2026-09-07.md) | v1.5.0 |
| 2 | 2026-09-08 → 2026-09-08 | [`HANDOFFS-through-2026-09-08.md`](archive/HANDOFFS-through-2026-09-08.md) | v1.5.0 |
| 2 | 2026-09-09 → 2026-09-09 | [`HANDOFFS-through-2026-09-09.md`](archive/HANDOFFS-through-2026-09-09.md) | v1.5.0 |
| 1 | 2026-09-09 → 2026-09-09 | [`HANDOFFS-through-2026-09-09-2.md`](archive/HANDOFFS-through-2026-09-09-2.md) | v1.5.0 |
| 2 | 2026-09-10 → 2026-09-10 | [`HANDOFFS-through-2026-09-10.md`](archive/HANDOFFS-through-2026-09-10.md) | v1.5.0 |
| 2 | 2026-09-11 → 2026-09-11 | [`HANDOFFS-through-2026-09-11.md`](archive/HANDOFFS-through-2026-09-11.md) | v1.5.0 |
| 2 | 2026-09-14 → 2026-09-15 | [`HANDOFFS-through-2026-09-15.md`](archive/HANDOFFS-through-2026-09-15.md) | v1.5.0 |
| 2 | 2026-09-15 → 2026-09-15 | [`HANDOFFS-through-2026-09-15-2.md`](archive/HANDOFFS-through-2026-09-15-2.md) | v1.5.0 |
| 6 | 2026-09-15 → 2026-09-16 | [`HANDOFFS-through-2026-09-16.md`](archive/HANDOFFS-through-2026-09-16.md) | v1.5.0 |

**Adding a row — the fold.** A trim appends a 3-line pointer block to the end of `HANDOFFS.md`'s front
matter (`starter-kit/methodology_trim.py:1093` `build_pointer_block`, `:1103` `insert_pointer`). Turn it
into one row at the bottom of this table (`n`, the span, the shard link as `archive/…`, the trimmer
version) and delete the block from `HANDOFFS.md`, **in its own commit**: inside the trim commit the
shipped `.verify.sh` fails L2 ([Learning #58](../starter-kit/FRAMEWORK_LEARNINGS.md)). The generator is
distributed, so teaching it to write the row itself is an upstream change.
