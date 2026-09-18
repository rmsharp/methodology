# Handoff Receipt Archive — Shard Index

One row per `methodology_trim.py` trim of the root [`HANDOFFS.md`](../HANDOFFS.md). The table lived in
that file's front matter until S174 (2026-09-16) and moved here with its rows unchanged except that their
links now start `archive/`. Each fold added a 125–129 B row against a fixed 7,168 B front-matter reserve
(`bin/check-handoff` `HEADER_RESERVE_BYTES`, asserted by `bin/tests.sh` Test 39 A2); with 140 B left, one
more row would have fit and the one after would not.

**Run the proofs rather than trusting this table.** Every row's shard is
`docs/archive/HANDOFFS-through-<date>.md`, with `-2` appended when that name was already taken, and its proof is the same path plus `.verify.sh`, which
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
| 2 | 2026-09-16 → 2026-09-16 | [`HANDOFFS-through-2026-09-16-2.md`](archive/HANDOFFS-through-2026-09-16-2.md) | v1.5.0 |
| 9 | 2026-09-14 → 2026-09-16 | [`HANDOFFS-through-2026-09-16-3.md`](archive/HANDOFFS-through-2026-09-16-3.md) | v1.5.0 |
| 4 | 2026-09-15 → 2026-09-16 | [`HANDOFFS-through-2026-09-16-4.md`](archive/HANDOFFS-through-2026-09-16-4.md) | v1.5.0 |
| 2 | 2026-09-16 → 2026-09-16 | [`HANDOFFS-through-2026-09-16-5.md`](archive/HANDOFFS-through-2026-09-16-5.md) | v1.5.0 |
| 2 | 2026-09-16 → 2026-09-17 | [`HANDOFFS-through-2026-09-17.md`](archive/HANDOFFS-through-2026-09-17.md) | v1.5.0 |
| 2 | 2026-09-17 → 2026-09-17 | [`HANDOFFS-through-2026-09-17-2.md`](archive/HANDOFFS-through-2026-09-17-2.md) | v1.5.0 |
| 2 | 2026-09-17 → 2026-09-17 | [`HANDOFFS-through-2026-09-17-3.md`](archive/HANDOFFS-through-2026-09-17-3.md) | v1.5.0 |
| 2 | 2026-09-17 → 2026-09-17 | [`HANDOFFS-through-2026-09-17-4.md`](archive/HANDOFFS-through-2026-09-17-4.md) | v1.5.0 |
| 2 | 2026-09-17 → 2026-09-17 | [`HANDOFFS-through-2026-09-17-5.md`](archive/HANDOFFS-through-2026-09-17-5.md) | v1.5.0 |

**Adding a row — the fold.** A trim writes a pointer block (three lines and a blank) into `HANDOFFS.md`'s
front matter — before its last standalone `---` line if it has one, at its end otherwise, which is where it
lands today (`starter-kit/methodology_trim.py:1093` `build_pointer_block`, `:1103` `insert_pointer`). Turn
it into one row at the bottom of this table — `n` is the record count, the span its two dates, the shard
cell the bare file name linked as `archive/<name>`, and `by` the trimmer version; the block's `.verify.sh`
link is dropped, since the proof sits beside its shard — and delete the block from `HANDOFFS.md`, **in its
own commit**: inside the trim commit the
shipped `.verify.sh` fails L2 ([fork Learning #58](FORK_LEARNINGS.md)). The generator is
distributed, so teaching it to write the row itself is an upstream change.
