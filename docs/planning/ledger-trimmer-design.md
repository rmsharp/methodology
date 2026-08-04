# The Ledger Trimmer — design

**Session:** S35 of [`framework-context-cost-plan.md`](framework-context-cost-plan.md) §5.
**Deliverable:** this document. **Design only — no code.** The build is S37, a separate session.
**Workstream:** [`ARCHITECTURE_WORKSTREAM.md`](../../workstreams/ARCHITECTURE_WORKSTREAM.md).

**Every figure in this document carries the command that produces it** (operator decision 3, plan §7:
DVX covers `docs/planning/`). Unless a figure names its own commit, it is measured **at `2fc2c5b`**,
this session's Phase 1B claim — pinned deliberately, because this session's own close-out rewrites
two of the files being measured, and a figure measured mid-change rots before the session ends.

```sh
C=2fc2c5b   # reproduce any size below with:
git show $C:<path> | wc -c        # bytes
git show $C:<path> | wc -l        # lines
```

---

## 0. What this design must answer

The brief, from plan §5: *"What is trimmed, the trigger, how losslessness is proven mechanically (the
manual procedure already proves it byte-for-byte, so it is mechanizable), where it lives, and the
search path that lets the dashboard detect it."*

Five questions, answered in §3–§7. Two things the brief asserts turned out to need correction, and
both changed the design:

1. **"The manual procedure already proves it byte-for-byte."** Partly true, and the true part is not
   sufficient. Event 3 (`020ba3f`) really did prove whole-file byte identity — and **silently lost a
   paragraph anyway**, because the proof it used cannot see that class of loss (§4.1). Event 2's
   published payload digest is **not reproducible** from the committed artifacts (§8, D3).
2. **The architecture's cost estimate.** Plan §5 says the distribution cost of a second tool is *"one
   line in `bin/_manifest.py`."* The measured precedent for a strictly simpler change — S34 adding one
   distributed **markdown** file — touched **21 files** (§6.2).

---

## 1. Context

### 1.1 The problem, restated from measurement

G2 of the operator's three goals: **automated trimming of files that both grow and must be read.**
The plan records that manual trimming does not hold. It holds worse than the plan says.

| File | at `2fc2c5b` | lines | B/line | records |
|---|---:|---:|---:|---:|
| `HANDOFFS.md` | 227,538 B | 896 | 253 | 20 receipts |
| `CHANGELOG.md` | 72,661 B | 879 | 82 | 18 entries |
| `docs/planning/BACKLOG.md` | 47,266 B | 498 | 94 | — (§3.3) |

```sh
for f in HANDOFFS.md CHANGELOG.md docs/planning/BACKLOG.md; do
  echo "$f $(git show 2fc2c5b:$f | wc -c) B $(git show 2fc2c5b:$f | wc -l) L"; done
git show 2fc2c5b:HANDOFFS.md  | grep -c '^```handoff'
git show 2fc2c5b:CHANGELOG.md | grep -c '^### '
```

`HANDOFFS.md` was archived on 2026-08-01 (`7a71df0`), 224,368 B → 52,927 B. **Two days later it is
larger than before that archive.**

```sh
git cat-file -s $(git rev-parse 7a71df0^:HANDOFFS.md)   # 224368  pre
git cat-file -s $(git rev-parse 7a71df0:HANDOFFS.md)    #  52927  post
git cat-file -s $(git rev-parse 2fc2c5b:HANDOFFS.md)    # 227538  now
```

**SRF = (227,538 − 52,927) / (224,368 − 52,927) = 1.0185** — past the plan's own RED threshold of
1.00 (**plan** §3.3, H3). The archive bought nothing. It bought slightly less than nothing.

### 1.2 The constraint that outranks the brief

Plan §3.3 states the action rule for SRF RED: **"do not archive again; the next deliverable is a rate
cut, not another reset."**

An automated trimmer is a **faster reset**. On the one file that most needs help, the repo's own
metric says a reset is the wrong move. This design does not paper over that. It ships the trimmer the
operator asked for, and it makes the trimmer **refuse to auto-fire on a RED file** (§5.3) rather than
industrialise the sawtooth. The rate problem is named, scoped out, and handed forward (§10.2).

### 1.3 Ratified architecture — binding, not re-opened

From the plan's §5 block *"Architecture ratified 2026-08-03 (operator + agent)"*
(`framework-context-cost-plan.md:491`). This design is verified against these four
constraints, not against the section's illustrative wording:

| # | Constraint | Where honoured |
|---|---|---|
| A1 | Metrics → `methodology_dashboard.py`. Read-only rows. | §7, **with the split below** |
| A2 | The **write** → a separate executable. | §6 |
| A3 | The remedy is named **conditionally** on the trimmer being present. | §7.3 |
| A4 | **Two tests** — present-branch goes stale; absent-branch never runs here. | §7.4 |

**A1 needs one thing said out loud, because this design otherwise computes the same metrics twice.**
The trimmer must evaluate headroom and SRF to decide whether to act (§5); the dashboard must display
them (S38). That is the same arithmetic in two executables — and a silently diverging pair of gauges
is worse than one, because the row an operator reads would stop matching the tool's behaviour.

**The split:** the **trimmer owns the computation** and exposes it as data via `--check`; the
**dashboard owns presentation** and, when the trimmer is present, *reads the number rather than
re-deriving it*. When it is absent, the dashboard computes the **line** metric only — the one whose
formula is already published in `CHANGELOG.md` front matter and needs no tool — and says the byte
metric is unavailable. This keeps A1's "metrics in the dashboard, read-only" true of what an adopter
sees, without minting a second source of truth. **S38 owes an agreement test:** with the trimmer
present, the dashboard's displayed headroom equals `--check`'s.

### 1.4 Operator decision received 2026-08-03, mid-claim

> *"ships to adopter; gates S40's wording"*

**The trimmer ships to adopters.** This settles queue item **S39 ahead of its slot** (the plan had it
decided on S37's evidence; the operator decided earlier, which is his to do — recorded, not
re-litigated). It is a binding input, and it is the reason §6 is as long as it is: a distributed
executable inherits a large surface that a canonical-only tool would not touch.

A4 **survives** the decision. An adopter who has not yet synced does not have the tool, so the
absent-branch is real and must still be designed and tested.

---

## 2. The record model — the finding that drives everything

### 2.1 A ledger is three zones, not one list

```
┌─────────────────┐
│  FRONT MATTER   │  doctrine, pointer, counts   → PINNED, except declared regenerated fields
├─────────────────┤
│    RECORDS      │  the only partitionable zone → SPLIT live | shard
├─────────────────┤
│     FOOTER      │  file-scoped, NOT a record   → PINNED to live, always
└─────────────────┘
```

**Why the footer zone is not pedantry: in a newest-on-top file the footer is at the bottom, which is
exactly where the cut takes from.** It is inside the excised span *by position*, so "move everything
below the cut point" loses it by construction — which is precisely what happened.

```sh
git show 020ba3f^:CHANGELOG.md | grep -n '^### ' | tail -1     # last record  @ 1204
git show 020ba3f^:CHANGELOG.md | grep -n 'Release history'     # footer       @ 1228
git show 020ba3f^:CHANGELOG.md | wc -l                         # EOF          @ 1231
```

**Zone detection is declared, never inferred — and ambiguity is a refusal.** The two families differ
irreconcilably: in `CHANGELOG.md` trailing content below the last record is a **footer**; in
`HANDOFFS.md` trailing content below the last fence **belongs to that record** (§2.2). No generic
rule distinguishes them. So each family declares its zone anchors in the trimmer's config, and **any
trailing content the config does not account for aborts the run** with the unclassified span printed.
Guessing here is how the paragraph was lost; abstention is already a ratified first-class result in
this codebase (decision D4).

**The footer zone exists because ignoring it has already destroyed content.** Event 2 (`3aee4e3`)
explicitly retained the pre-v3.0 scope footer, recording that it *"declares the whole ledger's scope
and does not migrate."* Event 3 (`020ba3f`) let it migrate into the shard. It is **still missing from
`CHANGELOG.md` today**:

```sh
for s in 3aee4e3^ 3aee4e3 020ba3f^ 020ba3f HEAD; do
  printf '%-10s %s\n' "$s" "$(git show $s:CHANGELOG.md | grep -c 'Release history before v3.0')"
done                    # → 1  1  1  0  0
grep -rn 'Release history before v3.0' CHANGELOG.md docs/archive/
                        # → only docs/archive/CHANGELOG-through-2026-08-01.md:800
```

The root action ledger no longer declares its own pre-v3.0 scope. **This is a live defect, found
during this design, recorded not fixed** (§8, D1 — FM #17).

### 2.2 Record boundaries, per family

| Family | Record starts | Record ends | Trap |
|---|---|---|---|
| `CHANGELOG.md` | `^### YYYY-MM-DD · [tag] …` | line before next `^### ` / footer | `###` lines **inside fenced blocks** |
| `HANDOFFS.md` | ``^```handoff`` | **closing fence + all trailing prose**, up to the next opening fence | prose is **outside** the fence |

**`HANDOFFS.md`: 23.1% of the payload lives outside the fences.** A fence-only cut severs each
receipt's self-score and predecessor-score paragraphs from the receipt they belong to.

```sh
git show 2fc2c5b:HANDOFFS.md | python3 -c '
import sys
t = sys.stdin.read(); total = len(t.encode())
inside = 0; on = False
for line in t.splitlines(keepends=True):
    b = len(line.encode())
    if line.startswith("```handoff"):      on = True;  inside += b; continue
    if on and line.startswith("```"):      inside += b; on = False; continue
    if on:                                 inside += b
print(f"total {total} B | inside {inside} B ({inside/total:.1%}) | outside {total-inside} B ({(total-inside)/total:.1%})")'
# → total 227538 B | inside 174957 B (76.9%) | outside 52581 B (23.1%)
```

**Never split on `^---$`.** Event 1 tried it and found 10 sections where there are 25, caught by a dry
run before any write. **The recorded cause is wrong**, and a trimmer built from the recorded cause
would guard the wrong hazard:

```sh
git show 7a71df0^:HANDOFFS.md > /tmp/pre.md
grep -c '^---$' /tmp/pre.md                       # 10  standalone separators
grep -c -- '---' /tmp/pre.md                      # 10  lines containing '---'
grep -- '---' /tmp/pre.md | grep -vc '^---$'      #  0  non-standalone occurrences
```

`7a71df0`'s message says *"receipt prose contains the same separator."* **Zero** receipt-prose
occurrences exist. The real cause is the converse: separators do not appear between every pair of
receipts, so 10 separators bound 11 sections over 25 records and one section swallows many. Same fix
(anchor on fences), opposite diagnosis (§8, D5).

**Fence-awareness is mandatory, and the seed files prove it.** `starter-kit/CHANGELOG.md` contains 3
`^### YYYY-MM-DD` lines and **all 3 are inside fenced documentation examples** — zero real entries.

```sh
grep -c '^### 20' starter-kit/CHANGELOG.md    # 3, all fenced examples
grep -c '^```handoff' starter-kit/HANDOFFS.md # 1, inside a 4-backtick wrapper
```

A trimmer that is not fence-aware will "trim" an adopter's freshly-seeded ledger on day one.

### 2.3 Records are not ordered by their obvious key

`HANDOFFS.md` interleaves **two independent `S<N>` sequences** (this fork and `upstream/main`) by
date, and they collide. The live file runs S35…S22, then S8, S7, S5, then S21, S20, S19
(`HANDOFFS.md:16-21` states the rule). A calendar day also straddles the existing cut: 2026-07-30
appears in both the live file and the archive.

**Consequence:** the record identity key is **session + date**, never session number; and cuts are by
**position in file order**, never by sorting on a parsed key. The existing cut was made at index 6 of
25 — positionally.

---

## 3. What is trimmed

### 3.1 In scope

| File | Record unit | Cut key | Why |
|---|---|---|---|
| `CHANGELOG.md` | `^### ` dated entry | position | 82 B/line, uniform records, already has a rate trigger |
| `HANDOFFS.md` | fence **+ trailing prose** | position | 53.9% of the Phase-0 read set; SRF RED |

`HANDOFFS.md` is **53.9%** of this repo's six-file Phase-0 read set (422,363 B at `2fc2c5b`):

```sh
for f in starter-kit/SESSION_RUNNER.md starter-kit/SAFEGUARDS.md CLAUDE.md \
         docs/planning/BACKLOG.md HANDOFFS.md CHANGELOG.md; do
  git show 2fc2c5b:$f | wc -c; done | paste -sd+ | bc      # 422363
```

### 3.2 Out of scope — grow by prose accretion, not by history

Archiving moves **history**. These files grow because someone keeps adding **procedure**, which has no
past to move to:

| File | at `2fc2c5b` | Why not archivable |
|---|---:|---|
| `starter-kit/SESSION_RUNNER.md` | 49,465 B | Procedure, needed every session. Its largest block is the 27-row failure-mode table — countermeasures, not history |
| `starter-kit/SAFEGUARDS.md` | 15,386 B | The only file the runner mandates as a **full** read |
| `ITERATIVE_METHODOLOGY.md` | 68,240 B | Theory; not in the read set |

The right move for these is **extraction with a pointer** — the `CLAUDE.md` → `docs/RELEASE_HISTORY.md`
(`7603f10`) and S34 → `starter-kit/FRAMEWORK_LEARNINGS.md` (`ed22ace`) pattern. That is a different
mechanism with a different proof, and it is **not** this tool's job.

Also excluded, each for a stated reason: `README.md` §What's New (47,003 B of 69,493 is version
history and structurally trimmable — but README is neither distributed nor in the read set, so
trimming it buys **zero context**); `docs/RELEASE_HISTORY.md` and `starter-kit/FRAMEWORK_LEARNINGS.md`
(append-only and unbounded, but **read on demand** — outside the read set, outside the motivation).

### 3.3 `docs/planning/BACKLOG.md` — **not trimmable by this mechanism**, and saying so is the answer

This was open at claim time. The evidence settles it:

```sh
git show 2fc2c5b:docs/planning/BACKLOG.md | grep -c '^### '   # 0
git show 2fc2c5b:docs/planning/BACKLOG.md | grep -c '^## '    # 3
```

**Zero `###` headings. No dated records. No uniform delimiter.** Its item marker is bold *inline* text
(`**BL-N — …**`), and it is not even enumerable that way: **BL-16 is an open item with no heading of
its own**, living inside BL-14's follow-on paragraph. The file says this about itself.

Structurally: §Open items is **69.2%** of the file and is **live state, not history** — the one thing
an archiver must never touch. Only §Completed items + §Historical context (7,645 B, **16.2%**) are
archivable at all, and for those the framework's own distributed doctrine already prescribes a
*different* sink: completed work moves into `CHANGELOG.md`, a live sibling, not a frozen shard.

**Verdict: out of scope, permanently, not "later."** A 16% ceiling on a file that is 11% of the read
set, via a mechanism the framework says not to use here. Trimming `BACKLOG.md` is a **grooming**
problem, not an archiving problem. (One trap for whoever does groom it: BL-1, BL-2 and BL-3 have **no
ledger entry anywhere**, so moving §Completed items to `CHANGELOG.md` as-is would lose them.)

---

## 4. How losslessness is proven — three assertions, because one is provably insufficient

### 4.1 Why one assertion is not enough

Event 3 proved whole-file concatenation identity, correctly:

> *"Reversing the one mechanical edit and concatenating shard onto live reproduces the pre-split file
> byte-for-byte, md5 f5af5eb58b647d1bba5b4c5d9375a38c"* — `020ba3f`

**That proof passed, and the footer was lost in the same commit** (§2.1). It had to pass: moving a
paragraph from the live file into the shard is *exactly* byte-preserving under concatenation. The
proof is structurally incapable of detecting a **zone** violation. It answers *"is every byte still
somewhere?"* and the question that matters is also *"is every byte still in the right file?"*

### 4.2 The three assertions

**L1 — Concatenation identity, over the RECORDS zone only.**

```
invert(transform(records(shard))) ++ records(live_after)  ==  records(live_before)
```

byte-for-byte. Catches loss and duplication. *(The existing manual proof, retained — but scoped.)*

> **Why "records only", and why the unscoped form is not merely imprecise but unsatisfiable.** The
> whole-file form — *concatenate the two files and compare to the original* — is what event 3
> published, and it cannot hold on any run that regenerates the pointer's counts (§4.5a), which every
> run does. It does not hold on the real event either: concatenating `020ba3f`'s shard and live file
> in **either** order differs from the pre-split file, at char 44 one way and char 3,389 the other —
> both inside front matter. A design that demanded it would refuse every run, including the three
> that succeeded.
>
> ```sh
> git show 020ba3f^:CHANGELOG.md > /tmp/before.md
> git show 020ba3f:CHANGELOG.md  > /tmp/live.md
> git show 020ba3f:docs/archive/CHANGELOG-through-2026-08-01.md > /tmp/shard.md
> cat /tmp/shard.md /tmp/live.md > /tmp/a.md; cmp /tmp/a.md /tmp/before.md   # differ: char 44
> cat /tmp/live.md /tmp/shard.md > /tmp/b.md; cmp /tmp/b.md /tmp/before.md   # differ: char 3389
> ```
>
> Scoping L1 to records is what lets L2 pin the other two zones *with their own rule* instead of one
> rule that fits none of them. **The three assertions partition the file; none of them is the
> whole-file check, and that is deliberate.**

**L2 — Zone pinning.** Every byte the classifier assigned to **FOOTER** is present in `live_after`,
byte-identical, and **absent from the shard**. Every byte assigned to **FRONT MATTER** is likewise
byte-identical and absent from the shard, **except within the declared regenerated fields** (§4.5) —
and the front-matter diff must be *confined* to those fields, which is itself an assertion, not a
carve-out. Catches §2.1's footer migration. *(New. This is the assertion whose absence cost a
paragraph.)*

*The exception is load-bearing and was initially written as a contradiction: the zone model says
front matter is rewritten (the pointer's counts and spans change every run), while a flat
"byte-identical" L2 would forbid exactly that. Naming the regenerated fields is what makes both true
at once — and it converts the rewrite from an unconstrained edit into a bounded one.*

**L3 — Record partition.** `records(live_before)` equals `records(live_after) ++ records(shard)` by
**identity, order, and byte-equality of each record**. Catches a move co-mingled with an edit.

L3 is not hypothetical. **Event 1 was not a pure move**: in the same commit that archived 19 receipts,
the *retained* S22 receipt's `next_steps` was rewritten in place (1,791 → 1,799 chars, "PR #64 … is
OPEN" → "PR #64 is CLOSED"). The correction was right; bundling it into the move made *"the move was
verbatim"* unfalsifiable. **L3 forces the trimmer to refuse**: a run is a pure partition, or it aborts.

### 4.3 The only permitted mutation, and why it must be uniform

Records that move two directories deeper need their root-relative links rebased. Event 3 got this
exactly right and stated the principle:

> *"a UNIFORM `../../` prefix — uniform because uniform is invertible and therefore provable"*

**Contract:** the trimmer applies **at most one** transform class — a uniform prefix on **root-relative
link targets** — and **L1 runs against its inverse**. Anything not expressible that way is not
applied: the run aborts and reports the record.

**The domain predicate is the whole contract, and `](` alone is not it.** A target is in-domain only
when **all** of these hold. Each exclusion is a link the naive key would have corrupted:

| Must | Excludes |
|---|---|
| matches `](<target>)` | bare URLs in prose |
| `<target>` has **no URI scheme** (`https:`, `http:`, `mailto:`) | `](https://github.com/…)` → `](../../https://…)` |
| does **not** start with `#` | in-page anchors |
| does **not** already start with `../` or `/` | double-prefixing an already-rebased or absolute path |
| the match is **not inside a fenced block or an inline code span** | prose *about* the rebase, which the corpus contains |

**Measured on the corpus the design cites** — of 23 link targets in the 2026-08-01 shard, only **one**
is a genuine rewrite candidate; **14 are absolute URLs** the bare `](` key would have mangled:

```sh
git show 2fc2c5b:docs/archive/CHANGELOG-through-2026-08-01.md \
 | grep -o '](\([^)]*\))' | sed 's/^](//;s/)$//' \
 | awk '{ if ($0 ~ /^https?:\/\//) print "absolute-URL";
          else if ($0 ~ /^\.\.\//)  print "already-relative";
          else if ($0 ~ /^#/)       print "fragment";
          else print "root-relative -> rewritten" }' | sort | uniq -c
# → 14 absolute-URL   8 already-relative   1 root-relative -> rewritten
```

The code-span exclusion is not hypothetical either: that same shard contains `](../../` **inside an
inline code span**, in a sentence explaining the rebase. The key would have rewritten the explanation
of the rewrite.

**The inverse must be checked, not assumed.** Before writing, the trimmer applies the transform and
then its inverse to every affected record and asserts the round-trip is the identity. A transform
whose inverse is not the identity on this corpus is rejected — that is what *"uniform because uniform
is invertible and therefore provable"* means operationally.

### 4.4 The proof must be re-runnable, not published

Event 2 published payload digest `f3d20156fae054d59b0b0447e3b55b06` and it is **not reproducible from
the committed artifacts** — five candidate payload definitions all disagree, and the commit records
neither boundary nor command. A digest without its payload definition and its command is an assertion
wearing a hash's clothes.

**Contract:** the trimmer writes `docs/archive/<shard>.verify.sh` — a self-contained script that
re-derives L1/L2/L3 from git and exits non-zero on failure. The commit message cites the script; it
never carries a bare digest. The trimmer **emits its own size figures with the unit and the command**,
because a hand-typed one has now been wrong three times, most recently `020ba3f`'s "101,608 B", which
is `wc -m` characters against 102,407 bytes (§8, D4).

### 4.5 What the trimmer writes

**(a) The live file's regenerated fields — the only front-matter bytes L2 permits to change.**
Each is *computed*, never carried forward, because every one of them has already drifted by hand:

| Field | Computed as | Current drift |
|---|---|---|
| retained record count | `len(records(live_after))` | `HANDOFFS.md:8` says **19**, file holds **20** (D2) |
| archived record count | `len(records(shard))` | — |
| archived span | first/last `date:` in the shard | — |
| shard link(s) | relative path(s) to every shard | — |

Anything else changing inside front matter **fails L2 and aborts the run.**

**(b) Shard naming — a contract, because two consumers glob for it.**

```
docs/archive/<LIVE_BASENAME>-through-<CUTKEY>.md
```

`docs/archive/` is mandatory (§8.2: the dashboard's non-recursive `(root, root/docs)` scan, and root
sort-order shadowing). The `<LIVE_BASENAME>-` prefix is mandatory because the rate trigger the design
keeps globs `docs/archive/CHANGELOG-*.md` to find its own baseline, and it is **single-level and
case-sensitive** — a nested or differently-cased name is silently excluded and the trigger then
computes against the wrong baseline.

The existing `docs/archive/HANDOFFS-archive.md` **does not match this pattern** and is grandfathered.
S37 must therefore derive shard lists by glob, never by the hardcoded literal paths `bin/tests.sh`
uses today in two places (§8.2) — otherwise a second shard is created, moved into, and never checked,
**and the suite still passes.**

**Shard paths are write-once: an existing path is a refusal, never an overwrite.** Two runs on the
same file can resolve to the same `<CUTKEY>` — trivially, two cuts on the same date, or two
count-based cuts. Overwriting would destroy the first shard's records while L1/L2/L3 all still pass,
because they quantify only over *this* run's triple and say nothing about any other file in
`docs/archive/`. **This is the one corruption the three assertions cannot see, so it is excluded by
construction rather than detected:** if the resolved shard path exists, the run aborts (exit 2) and
prints the collision. `--cut` lets the operator disambiguate.

**(c) The shard's own preamble, and what it must NOT contain.** Title, back-link to the live file,
span + count (computed), and the cut key used. It must **not restate any forward-looking rule.** The
v3.6 shard restated the next-archive rule and **both halves were wrong one day later**, forcing the
only edit that shard has ever received. Cite the live file; do not copy it.

**(d) Freeze semantics are asymmetric, and the trimmer must not "fix" that.** `CHANGELOG` shards
freeze dated entries absolutely. The `HANDOFFS` shard permits `commit:` answer-slot reconciliation
after the fact (`7752114` rewrote that field inside two archived receipts). The trimmer writes shards;
it never rewrites one, and it must not treat a later reconcile edit as corruption.

---

## 5. The trigger

### 5.1 The existing trigger is blind to the file that needs it most

The governing rule lives in `CHANGELOG.md` front matter (S31, `020ba3f`): fire when headroom to the
2,000-line agent `Read` cap divided by lines-per-entry falls below **15 entries**; cut until back
above **30**. It is a **rate**, it re-derives its own baseline from `git log --diff-filter=A`, and it
abstains out loud. All of that is right and is kept.

**It is denominated in lines, and the two ledgers sit on opposite sides of a 3× density gap** (253 vs
82 B/line, §1.1). Run it on each file today:

```sh
# CHANGELOG.md — the published command, verbatim from its own front matter
split=$(git log --diff-filter=A -1 --format=%H -- 'docs/archive/CHANGELOG-*.md')
live=$(wc -l < CHANGELOG.md); dl=$(( live - $(git show $split:CHANGELOG.md | wc -l) ))
de=$(( $(grep -c '^### ' CHANGELOG.md) - $(git show $split:CHANGELOG.md | grep -c '^### ') ))
echo $(( (2000 - live) * de / dl ))          # → 32 entries of headroom
```

| File | line headroom | fires at <15? | bytes | SRF |
|---|---:|:---:|---:|---:|
| `CHANGELOG.md` | 32 entries | no | 72,661 | 0.44 |
| `HANDOFFS.md` | **24 receipts** | **no** | **227,538** | **1.0185** |

`HANDOFFS.md` is **896 lines / 227,538 B**; the file whose size justified the last archive was **997
lines / 224,368 B**. **Fewer lines, more bytes.** Its own stated trigger — *"approaches ~1,200
lines"* — cannot fire on a file already larger in bytes than the one that triggered the last archive.
Consuming its remaining 24 receipts of line-headroom at the observed 12,472 B/receipt would put it
near **527 KB**, still "under" the line trigger.

```sh
# slope, denominated in the framework's own unit
split=$(git log --diff-filter=A -1 --format=%H -- 'docs/archive/HANDOFFS-archive.md')   # 7a71df0
db=$(( $(git show 2fc2c5b:HANDOFFS.md | wc -c) - $(git show $split:HANDOFFS.md | wc -c) ))
dr=$(( $(git show 2fc2c5b:HANDOFFS.md | grep -c '^```handoff') \
     - $(git show $split:HANDOFFS.md | grep -c '^```handoff') ))
echo "$((db/dr)) B per receipt over $dr receipts"        # → 12472 B per receipt over 14 receipts
```

### 5.2 Two metrics, because there are two distinct failure modes

They are not interchangeable and neither subsumes the other:

| Metric | Protects against | Cap |
|---|---|---|
| **Lines** | **silent truncation** — a `Read` past the cap returns no error and no marker | 2,000 lines |
| **Bytes** | **context tax** — G1, the operator's stated goal | per-file budget |

**The two metrics take different FORMS, and transplanting one onto the other does not work.** The
line rule is *units-of-headroom* (fire <15, cut until >30) because its cap — 2,000 lines — sits far
above normal operating size, so "how many more entries fit" is a meaningful quantity. The byte budget
sits **at** operating size, so the same expression degenerates:

```sh
python3 -c '
slope = 12472; floor = 2025 + 3767      # B/receipt; front matter + one receipt-with-prose
for b in (52927, 65536, 131072, 262144):
    print(f"budget {b:7,}: headroom now {(b-227538)/slope:6.1f} | "
          f"best case, 1 record left {(b-floor)/slope:5.1f} | reaches 30? {(b-floor)/slope>=30}")'
# → every budget, including 256 KB: "reaches 30? False"
```

**"Cut until back above 30" is unreachable on the byte metric at every budget — even trimming to a
single record.** A trimmer using it would trim to empty and still report the trigger unsatisfied.

**Rule, as two correctly-formed conditions:**

| Metric | Fire when | Cut until |
|---|---|---|
| **Lines** (truncation) | headroom < **15 entries/receipts** | headroom > **30** |
| **Bytes** (context tax) | `size > budget` | `size ≤ 0.5 × budget` |

The byte metric is a **level with hysteresis**, not a rate — the form that terminates. The 0.5 factor
is the hysteresis that stops a trim firing again on the next record; it is judgment, and the sawtooth
it must avoid is measured in §1.1.

**Fire if EITHER condition fires; stop only when BOTH stop conditions hold.** Both re-derived at every
read; the line metric abstains out loud when there is no slope. Under this rule `CHANGELOG.md` reads
32 entries of line-headroom (no fire) but **72,661 B against a 64 KB budget — it fires on bytes**;
`HANDOFFS.md` fires on bytes at 3.5× budget, which its own line trigger cannot see.

*The 2,000-line cap is agent-harness behaviour, not a property of this repo — the live `CHANGELOG.md`
concedes this about itself.*

### 5.4 The byte budget — default **64 KB per ledger**, and where that number comes from

The line cap cannot supply it. At each file's measured density, 2,000 lines means **164 KB** for
`CHANGELOG.md` (82 B/line) and **506 KB** for `HANDOFFS.md` (253 B/line) — the same rule yielding a
3× different ceiling is exactly the blindness §5.1 documents. The budget must come from the **context**
side instead.

**Calibrated to sizes this repo actually operated at**, not invented: the three archives reset their
files to **52,927 B**, **53,512 B** and **49,382 B**, and the sessions of that period ran normally at
those sizes. 64 KB sits just above all three, and holds the two ledgers together (128 KB) at roughly
**2×** the 64,851 B mandatory floor.

```sh
git cat-file -s $(git rev-parse 7a71df0:HANDOFFS.md)     # 52927
git cat-file -s $(git rev-parse 3aee4e3:CHANGELOG.md)    # 53512
git cat-file -s $(git rev-parse 020ba3f:CHANGELOG.md)    # 49382
```

**This is judgment, and it is labelled as such** — the same way the plan labels H3's AMBER and H2's
CRITICAL as judgment. It is a per-file project setting with this default; S37 exposes it, S40
documents choosing it. Against it today: `CHANGELOG.md` **72,661 B** is already over, and
`HANDOFFS.md` **227,538 B** is **3.5×** over.

### 5.3 The refusal that keeps this honest

**The trimmer computes SRF and refuses to auto-fire when SRF ≥ 1.00.** It reports:

> `HANDOFFS.md: SRF 1.02 (RED). The last archive has been entirely given back. Archiving again resets
> the level and not the rate — see plan §3.3. Re-run with --force to archive anyway.`

This is the plan's own H3 action rule, mechanised. Without it the tool's first act on this repo would
be to automate precisely the sawtooth its own metric flags. `--force` exists because a human may have
a reason; the default must not.

**SRF is undefined before a file's first archive — which is every adopter on day one — and the tool
must say so rather than compute a zero.** With no prior archive there is no `(pre, post)` boundary:
`git log --diff-filter=A -- 'docs/archive/<BASENAME>-*.md'` returns empty, and `git show :<path>`
against an empty sha silently succeeds against the index, so a naive implementation gets a *plausible
wrong number* instead of an error. The branch is explicit: **no prior archive → SRF abstains, prints
that it abstains, and does not block.** This is H3's own stated limit (*"undefined before an adopter's
first archive"*) and the same abstention discipline §5.2 requires of the line metric.

**H3's boundary rule is specified, and pinning it differently is ADDING POLICY — labelled here as
such.** H3 says *"around the largest single size drop in the file's history"*, which unambiguously
selects `3aee4e3` for `CHANGELOG.md` (drop 133,192 B vs `020ba3f`'s 53,025 B). There is no ambiguity
to resolve. What there *is* is a consequence worth stating, because the two readings differ by 3× on
the same file on the same day:

```sh
# H3 says "the largest single size drop in the file's history"
# largest  (3aee4e3): pre 186704 post 53512 → SRF (72661-53512)/(186704-53512) = 0.1438
# most recent (020ba3f): pre 102407 post 49382 → SRF (72661-49382)/(102407-49382) = 0.4390
for s in 3aee4e3^ 3aee4e3 020ba3f^ 020ba3f 2fc2c5b; do
  echo "$s $(git cat-file -s $(git rev-parse $s:CHANGELOG.md))"; done
```

**0.1438 vs 0.4390 — a 3.05× spread.** H3's own reading is 0.1438.

**Recommendation, stated as a departure and not as a reading:** S37 should report **both**, label each
with its boundary sha, and use the **most recent archive** for the §5.3 refusal — because the refusal
acts on *current cadence*, and the largest-drop boundary recedes further into the past with every
archive, diluting exactly the signal the refusal exists to catch. That is a policy addition on top of
H3, it belongs to the trimmer and not to H3, and adopting it should be an explicit call in S37's
close-out rather than something a reader discovers. **H3 itself is unchanged.**

---

## 6. Where it lives

### 6.1 `bin/` is excluded by the shipping decision

`bin/_manifest.py` `DISTRIBUTION` contains **zero `bin/` sources** — `bin/` ships nothing. Since the
operator's decision is that the trimmer ships, it cannot live there.

```sh
python3 -c "import sys; sys.path.insert(0,'bin'); import _manifest as m; \
  print(len(m.DISTRIBUTION), 'entries;', sum(1 for s,d,_ in m.DISTRIBUTION if s.startswith('bin/')), 'from bin/')"
```

**Placement: `starter-kit/methodology_trim.py` → adopter-root dest `methodology_trim.py`, disposition
TRACKED.** Constraints that force each part:

- **`.py` suffix** — `bin/sync` sets the executable bit on suffix alone, not on the source's git mode.
- **Adopter-root dest (no `/`)** — this is what makes **Learning #12's guard fire**. The guard filters
  `if "/" not in dest`, so a `docs/`-style dest would skip it *silently* and still report green. S34
  faced the same choice and recorded it; **facing the guard is the design decision**, not an accident.
- **TRACKED, not SEED** — SEED is written once and never updated; a tool must be upgradable.
- **`starter-kit/` src** — not required by tooling (two current entries have root srcs), but it is the
  sentinel directory distinguishing `--source=local` from `--source=github`.

### 6.2 The real cost of shipping an executable

Plan §5's *"one line in `bin/_manifest.py`"* understates this materially. The precedent for a
**simpler** change — S34 adding one distributed markdown file — touched **21 files**:

```sh
git show --stat ed22ace | tail -3      # 21 files changed, 181 insertions(+), 76 deletions(-)
```

An **executable** additionally faces gates markdown never touches:

| Gate | What it requires | Consequence of missing it |
|---|---|---|
| `FRAMEWORK_INSTALLED_SOURCE` | tuple equality (**order-sensitive**) with the manifest's non-markdown dests, asserted by a canonical test | test red |
| `is_framework_installed()` | **content** verification — declares a version constant, or ≥2 of 5 structural signatures | trimmer counted as *adopter source* |
| `DOC_ONLY_SOURCE_LOC_MAX = 200` | if the above fails and the trimmer exceeds 200 LOC | **a doc-only adopter flips to "code"** and re-earns the false HIGH "No test infrastructure" risk that v3.2 exists to remove |
| `DASHBOARD_VERSION` | bump, pinned by exact-string tests in two places | test red |
| twin byte-identity | every dashboard edit mirrored into both copies | Test 19 + `test_twins_byte_identical` red |
| `IGNORE_ENTRIES` | derived from TRACKED dests — `/methodology_trim.py` is appended to adopter `.gitignore` | adopters who git-tracked it get a warning |
| executable-bit test | hardcoded to the dashboard, **not** derived from the manifest | new executable ships with **zero** exec-bit coverage |

**The 200-LOC ceiling is a hard design constraint, not trivia.** A trimmer that is large *and*
unrecognised silently degrades every doc-only adopter's dashboard. S37 must make
`is_framework_installed()` recognise it — and that is a dashboard change, so it lands in **both twins**.

**Test 9 will fail until upstream merges.** `bin/tests.sh:120` dry-runs `--source=github` against the
pinned `KJ5HST/methodology`; a manifest entry for a file not yet upstream 404s. This is the known,
expected shape — the suite is **175 passed / 1 failed** today for exactly this reason on
`FRAMEWORK_LEARNINGS.md`. **Do not weaken Test 9.**

Two tests derive their expectations *from* the manifest and cover a new entry with no edit: Test 11
(presence + byte-equality) and Test 15 (row count = `len(DISTRIBUTION)`).

---

### 6.3 The tool's surface — CLI, exit codes, config

**Dry-run is the default.** Writing requires an explicit flag. This inverts the usual default because
the tool rewrites tracked history, and because every manual event that went well ran a dry run first —
the separator trap (§2.2) was caught by one.

| Flag | Meaning |
|---|---|
| `--file <path>` | the ledger to trim (repeatable). Required |
| `--write` | actually write. **Absent → dry run**, the default |
| `--cut <N\|date\|@release>` | override the computed cut point |
| `--budget-bytes <N>` | override the §5.4 default for this run |
| `--force` | proceed despite the SRF-RED refusal (§5.3). Never implied |
| `--check` | evaluate the trigger and report; never writes, even with `--write` |

| Exit | Meaning |
|---|---|
| 0 | nothing to do (under budget), or a dry run that would succeed, or a write that succeeded |
| 1 | trigger fires / would trim — the `--check` signal for a hook or CI |
| 2 | **refusal**: L1/L2/L3 failed, zones ambiguous, undocumented set non-empty (P1), or SRF RED |
| 3 | usage error: file missing, no config for this file, no records |

**Never assert on the exit code as a proxy for one condition** — it is a union over every check the
tool runs, so adding a check silently re-labels unrelated assertions. Tests assert on the **named
finding**, not the code.

**Config is a table in the tool, not a config file.** Each entry declares: record-start pattern,
record-end rule, zone anchors (§2.1), the regenerated fields (§4.5a), and the byte budget. A file with
no entry exits 3 — it does **not** fall back to a generic rule, because a generic rule is exactly what
would mis-zone an adopter's differently-shaped ledger.

**Edge cases, all explicit refusals rather than best-effort:** file absent → 3; zero archivable
records → 0 with a stated reason; trimming would leave zero records → 2 (over-trimming to zero makes
`bin/check-handoff` hard-fail, §8.2); unclassified trailing content → 2 with the span printed.

### 6.4 Failure atomicity and rollback

A tool whose entire job is rewriting tracked history needs a crash story, and "git will save you" is
only true if the write never lands half-done in the same commit as the deletion.

**Atomicity.** Compute everything in memory; verify L1/L2/L3 on the in-memory result; only then write.
Write the shard **first**, to a temporary path in `docs/archive/`, `fsync`, rename into place, and
only then rewrite the live file — also via temp-and-rename. A crash before the final rename leaves the
live file untouched and at worst an orphan temp file; a crash after it leaves both files correct.
**At no point does a live record exist in neither file.**

**The trimmer never commits.** It leaves the working tree staged-but-uncommitted and prints the
suggested message. This keeps the operator between the rewrite and history, keeps the FM #27 hook in
its normal path, and means the rollback for *any* failure — including one the assertions did not
catch — is the ordinary one:

| Stage | Rollback |
|---|---|
| after a dry run | nothing to undo; the run wrote nothing |
| after `--write`, before commit | `git checkout -- <live>` + `rm <shard>` — the tool prints both |
| after commit, before push | `git revert <sha>` — the trim is a single, self-contained commit |
| after push | `git revert` + a ledger entry recording the revert (it is an action) |

**Why per-file and not batched:** one `--file` per commit. A batched trim of both ledgers has a
rollback that cannot be expressed as one revert without also reverting the other file's trim, and
`SAFEGUARDS.md` §Blast Radius Limits caps a commit at 5 files regardless. One ledger, one shard, one
ledger entry, one commit, one revert.

---

## 7. The dashboard's search path

### 7.1 What already exists — use it, don't invent

| Mechanism | Location | Reuse |
|---|---|---|
| `check_stale_version()` / `parse_version()` | dashboard | **The precedent.** Interrogates another executable **by regex, without importing it**, and names a command built from the located path |
| `is_framework_installed()` | dashboard | **The precedent for identity**: root-anchored dest membership, then whole-file content verification |
| `signals` list | collectors | A collector authors `(severity, description)` tuples; `assess_risks` re-emits them **verbatim** |
| `find_canonical()` | dashboard | The only walk-up locator — matches the literal directory name `methodology`; returns `None` on miss |

### 7.2 Detection contract

**Probe:** `(<scanned project>/methodology_trim.py).is_file()` — root-anchored on the **scanned
project**, mirroring `is_framework_installed`. Then **content-verify** by regex for the tool's version
constant, exactly as `parse_version` does.

Explicitly **not**: `PATH` lookup, the executable bit (nothing in the dashboard checks `X_OK`, and the
bit is unverified on Windows — there is no CI), or `.exists()` (a directory would pass).

**On miss: abstain, and say so.** Abstention is a ratified first-class result here (decision D4), with
the rule that *a 0 from an unread source must not be reported as a clean state*.

### 7.3 The conditional remedy (A3)

The trimmer row is authored by a **collector** into `signals`, and its text branches on detection:

- **present** → names the runnable command, built from the located path.
- **absent** → names the **documented manual procedure** — never a command the adopter does not have.

Advisory text in this file is required to **name the file it was computed against** rather than use a
generic noun, because a generic noun once misdirected an adopter.

**Budget note.** Risk descriptions render **only on the HTML project card**; the terminal prints only
the worst severity word per project. There is **no stdout size budget constant anywhere** in the
dashboard — the ≤300 B figure exists only in the plan. So the conditional row costs **0 B of stdout**
unless someone chooses to surface it in the terminal. *That choice is not this design's to make* —
it belongs with S45, and the operator should be asked.

### 7.4 The two tests (A4)

| Branch | Risk it addresses | Test |
|---|---|---|
| **present** | the dashboard carries a copy of another tool's interface and **goes stale** | assert the named command is one the trimmer actually accepts — parse the trimmer's own argument list, never a hardcoded literal |
| **absent** | this branch **never runs on a developer machine**, so nothing checks it says anything useful | fixture with no trimmer present; assert the row still points at the documented manual procedure and names the file |

---

## 8. Blast radius, and the defects found while mapping it

### 8.1 CONFIRMED CORRECTNESS BUG — frontier poisoning

Phase 0 reconcile computes `frontier = git log -1 --format=%H -- CHANGELOG.md`, then treats
`<frontier>..HEAD` as the undocumented set. **A trimmer commit rewrites `CHANGELOG.md`, so it advances
that frontier past any commit that was never recorded — permanently hiding it.**

Reproduced end-to-end in a scratch repo. **This is the reproduction script — run it; it is
self-contained and takes a second:**

```sh
SB=$(mktemp -d); cd "$SB"; git init -q .; git config user.email t@t; git config user.name T
printf '# Changelog\n\n### 2026-01-01 · [ad hoc] first\n' > CHANGELOG.md; echo hi > src.txt
git add -A && git commit -qm "c1: initial, ledger recorded"
echo more >> src.txt && git add -A && git commit -qm "c2: UNRECORDED ACTION (no ledger entry)"
F=$(git log -1 --format=%H -- CHANGELOG.md)
echo "BEFORE trim: undocumented = $(git rev-list --count --no-merges $F..HEAD)"
mkdir -p docs/archive
printf '# Archive\n\n### 2026-01-01 · [ad hoc] first\n' > docs/archive/CHANGELOG-through-2026-01.md
printf '# Changelog\n\nArchived: see docs/archive/\n' > CHANGELOG.md
git add -A && git commit -qm "trim: archive old entries"
F2=$(git log -1 --format=%H -- CHANGELOG.md)
echo "AFTER  trim: undocumented = $(git rev-list --count --no-merges $F2..HEAD)"
# → BEFORE trim: undocumented = 1
# → AFTER  trim: undocumented = 0        ← c2 is now permanently invisible
```

It is worse than one metric: the same poisoning blinds the **`HANDOFFS.md` reconcile** (whose second
trigger consumes the CHANGELOG-derived undocumented set) and silences the dashboard's **Signals B and
C**, which compute the identical quantity from the identical git command — resetting `unlogged_commits`
toward 0 and forcing `is_fresh = True`.

And it cannot be avoided by trimming only `HANDOFFS.md`: the FM #27 pre-commit gate requires
`CHANGELOG.md` co-staging for anything outside the Phase-1B carve-out, and a shard file is outside it.
**Every trim commit touches `CHANGELOG.md` by construction.**

> **P1 — MANDATORY PRECONDITION.** The trimmer **refuses to run** when the undocumented set is
> non-empty. Reconcile first, then trim. Cheap — two `git` calls.

> **P1a — AND THE TRIMMER'S OWN COMMIT, which P1 cannot see.** P1 runs *before* the trim commit
> exists, so it constrains only the commits before it. The trim commit then advances the frontier
> itself. The FM #27 hook does not close this: it passes on **mere co-staging** of `CHANGELOG.md` and
> never checks that an entry was *added* — and a `CHANGELOG.md` trim co-stages it by construction.
>
> ```sh
> grep -n 'co-staged' .githooks/pre-commit        # the gate is membership, not content
> ```
>
> So the trimmer **writes its own ledger entry as part of the trim** (it is an action — FM #27), and
> the run asserts as a **post-condition** that `live_after` contains exactly one more `^### ` entry
> than `live_before` did *after* accounting for the partition. Without P1a the tool's very first act
> would be to hide itself.

> **P2.** The trimmer must never be implemented as `git mv CHANGELOG.md <shard>` + fresh write: the
> hook's `--no-renames` means that shape **passes a gate meant to notice it**. The hook's own comment
> documents this as the opt-out.

### 8.2 Consumers that must be re-pointed or accepted

| Consumer | Behaviour after a trim | Action |
|---|---|---|
| `bin/check-handoff` | schema on `blocks[0]` only; `check_answer_slots` on `blocks[1:]`; `check_locator_forms` on all — **three different denominators** | Trimming lowers the "all N older receipts" population. Accept; document N |
| `bin/check-handoff --archived` | a shard checked **without** `--archived` silently exempts its own first block from the answer-slot rule | S37 must pass `--archived` for every shard |
| `bin/tests.sh` | wires **exactly one** shard, by **hardcoded literal path**, in two places | **A second shard would never be checked and the suite would still pass.** Derive the shard list |
| `bin/model-report` | **no archive awareness at all** — already blind to 68 of 86 entries and 19 of 39 receipts | Pre-existing; worsens with every shard. BL-20 |
| `bin/check-links` | walks only DISTRIBUTION dests — **neither root ledger nor any shard is checked** | The `../../` rebases are entirely unverified by the suite. S37 owes a check |
| `bin/status` | stale-seed detection keys on **title strings in ledger front matter** | A trimmer that reformats those titles makes every adopter's ledger report "stale format" |
| audit grep (front matter) | reads archives via a single-level, case-sensitive glob | A new shard counts **iff** named `docs/archive/CHANGELOG-<…>.md` |
| audit grep (**distributed**) | unanchored **and** archive-blind — returns **23** where the true population is **86** | Pre-existing defect in what adopters receive |
| over-trimming | zero blocks makes `check-handoff` **hard-fail** (no seed sentinel to excuse an empty ledger) | Floor: never trim below 1 record |

**Placement is load-bearing and already verified.** Shards must live in `docs/archive/`: the
dashboard's `_find_changelog` scans exactly `(path, path/"docs")`, **non-recursively**, and within a
base a root `CHANGELOG-archive.md` sorts **ahead** of `CHANGELOG.md` (`-` is 0x2D, `.` is 0x2E) — a
real shipped bug. A subdirectory cannot shadow the live file.

### 8.3 Defects found during this design — recorded, not fixed (FM #17)

| # | Defect | Evidence |
|---|---|---|
| **D1** | **`CHANGELOG.md` has lost its pre-v3.0 scope footer** since `020ba3f`. Live, uncorrected | §2.1 |
| **D2** | `HANDOFFS.md:8` says the file holds **19** receipts; it holds **20**. (Drifted by this session's own claim commit — the file's own blockquote admits the count is unguarded) | `grep -c '^```handoff' HANDOFFS.md` |
| **D3** | Event 2's payload md5 `f3d2015…` is **not reproducible** from the committed artifacts; no boundary, no command recorded | §4.4 |
| **D4** | `020ba3f`'s "101,608 B" is `wc -m` **characters**; the byte count is 102,407. Third recurrence of the unit-wrong class | §4.4 |
| **D5** | `7a71df0`'s recorded cause for the separator trap is **false** — zero non-standalone `---` in the pre-split file | §2.2 |
| **D6** | **Three live prose sentences** call the dashboard *"the only executable adopters receive"* — false the moment the trimmer ships: plan `:172`, `:391`, `:495`. The phrase also appears at `CHANGELOG.md:229` and `:509`, but both sit **inside dated entries**, which are corrected forward and never rewritten — those two are correctly left alone, and counting them as five would be the defect. **CORRECTED AT S39', WHICH DISCHARGED THIS ROW: the population is FIVE live sites, not three, and this row's own verification command is why it read three.** `:476` and `:599` say *"Adopters receive exactly one executable today"* — the same claim in different words, invisible to a grep for one literal (this repo's own *a grep count is a sample* lesson, landing on the row that taught it). `:495` is off by one; the third live site is `:496`. The two frozen `CHANGELOG.md` anchors have drifted ~428 lines each — the ledger is newest-first, so every prepend pushes them down — and are `:657` and `:937` today; the **verdict survives** (containment re-proved: `:657` sits inside the entry opening at `:622`, `:937` inside `:894`), but this row's own `head -229` containment command now inspects the wrong entry | `grep -rn "only executable" CHANGELOG.md docs/planning/framework-context-cost-plan.md`; entry containment: `head -229 CHANGELOG.md \| grep '^### 20' \| tail -1` |
| **D7** | `.gitignore` covers `dashboard.html` but **not** `dashboard_history.jsonl`, so a routine Phase-0 dashboard run dirties the tree | `cat .gitignore` |
| **D8** | Plan `:496`'s "3,336 lines" is stale by one (3,337 since `ed22ace`), and its "writes only its own HTML and copies of itself" omits the **JSONL history append** — three write sites, not two | `git show ed22ace:tools/methodology_dashboard.py \| wc -l` |
| **D9** | The plan's read-set figure (**379,206 B**, `:81`) is stale: the same six files sum to **422,363 B** at `2fc2c5b` (**+43,157 B, +11.4%**) — and it grew *despite* S34 removing 12,945 B. Its component values are pre-S34 (`SESSION_RUNNER.md` **62,410**, now 49,465), so the figure predates `326094d`, where the same six sum to **394,954** — i.e. it was already stale when the plan published it | `for f in …; do git show 2fc2c5b:$f \| wc -c; done \| paste -sd+ \| bc` → 422363; same at `326094d` → 394954 |

D1 is the only one that is content loss. It should be fixed by a session that can carry it as its
deliverable; it is **not** folded into S37, where it would re-create exactly the co-mingling that L3
exists to forbid.

---

## 9. Alternatives considered

Honest trade-offs, not straw men. Two of these are better than the chosen design on at least one axis.

### A. Keep archiving by hand (status quo)

**Pros:** no new code, no distribution surface, no 200-LOC ceiling, no new failure modes. A human can
apply judgement to a cut key that differs per event — and it did differ, three times out of three.
**Cons:** measured failure. SRF 1.0185. Three events produced three different cut keys, two proof gaps
(§8.3 D3, D4), one **content loss** (D1), and one move co-mingled with an edit (§4.2). The trigger has
never once fired at its stated level: HANDOFFS at 997 against a stated 1,200; CHANGELOG event 2 at
2,090 — already **past** the cap it exists to clear.
**Rejected because** the operator asked for automation (G2) and the manual record is the argument for it.

### B. Put the write inside `methodology_dashboard.py`

**Pros — real ones.** One tool, one manifest entry, no second executable, and the whole of §6.2
evaporates: no `FRAMEWORK_INSTALLED_SOURCE` tuple, no `is_framework_installed` content check, no
doc-only-flips-to-code hazard, no detection contract (§7.2) because there is nothing to detect.
**Cons:** the dashboard has never touched user content — its three write sites are its own HTML, its
own JSONL history, and (under `--sync`) copies of itself. Trimming rewrites *tracked history*. The
losslessness proof is substantial code with its own failure modes, landing in a 3,337-line file that
already carries a 2,684-line test file and a byte-identical twin.
**Rejected by ratified architecture A2** (plan §5, ratified-architecture block). Recorded here because A2's cost is real and this
document should not pretend the chosen split is free — it is not; §6.2 is what it costs.

### C. Git-only archiving — truncate the live file, let git be the archive

Every archived byte is already in git. Truncate; write no shard.

**Pros — the strongest technical alternative.** L1 becomes `git show <sha>:<file>`, exact and free. No
shard files, no `../../` link rebasing, so §4.3's entire invertible-transform contract disappears
along with its failure modes. No shard front matter to drift, no hand-written counts, no second file
for `bin/tests.sh` to forget (§8.2).
**Cons:** the archive stops being *readable as a document*. `bin/model-report --changelog <shard>`,
the audit greps, and `bin/check-handoff --archived` all operate on **files**; every one would need a
git-aware rewrite. A shallow clone loses the history entirely. An adopter browsing on GitHub, or
grepping their working tree, silently sees a truncated record with no pointer to the rest.
**Rejected because** the record must stay readable without git archaeology — but this is the option to
revisit if shard maintenance proves worse than predicted. It trades tooling breadth for proof
simplicity, and the proof is where the manual procedure actually failed.

### D. Rotate on write — a pre-commit hook instead of a tool

**Pros:** fully automatic; no session can forget it.
**Cons:** a hook that rewrites tracked content *during* a commit is precisely the blast radius
`SAFEGUARDS.md` §Blast Radius Limits exists to bound. It fires mid-session, inside someone else's
deliverable, and it cannot satisfy **P1** (§8.1) — at commit time the undocumented set is not yet
settled, because the commit being made is part of it.
**Rejected on blast radius.** The existing `.githooks/pre-commit` only *refuses*; it never rewrites.

### E. Attack the rate, not the level — a receipt-size norm

**Pros:** addresses `HANDOFFS.md`'s actual problem. Level control on a file at SRF 1.0185 is the move
the repo's own H3 rule tells you not to make (§1.2).
**Cons:** it is not what was asked, it does not help `CHANGELOG.md`, and enforcing a size cap on a
receipt is lossy by construction — H4 is explicitly *advisory, never blocking* for that reason.
**Not rejected — deferred and handed forward** as §10.2. This is a complement to the trimmer, not a
substitute, and the design says plainly that without it the read-set floor stops falling.

---

## 10. Scope boundary

### 10.1 What this design does not decide

- **No code.** That is S37.
- **The three dashboard defects (D4 in the plan).** That is S36, and S36 precedes S38.
- **Doctrine wording.** That was S40, **shipped (fork) 2026-08-04**. When this was written the gap
  was: **zero distributed files state any archive, split, size, or truncation policy**, and both
  ledger seeds described themselves as append-only and kept forever. (`grep -l archiv
  starter-kit/*.md` returned nothing then; by S39' it returned `FRAMEWORK_LEARNINGS.md` and
  `BOOTSTRAP.md`, neither of which stated a policy — the gap stood, the *command* had stopped
  demonstrating it. See Phase 4's closing note and Phase 5's own record.) Both seeds now carry a
  **Size, and when to archive** section; the `kept forever` clause is gone.
- **Whether the conditional row appears in terminal stdout** (§7.3) — an operator question for S45.

### 10.2 The rate problem, named and handed forward

This tool automates **level** control. `HANDOFFS.md`'s problem is **rate**: 12,472 B per receipt,
~87 KB/day, SRF 1.0185. Fourteen receipts gave back an entire session's deliverable in two days.

The plan already has the gauge — **H4, Receipt Inflation**, explicitly *advisory, never blocking*. The
lever is receipt size, and the mechanism would be a norm plus a check, not an archiver. **A session
should be queued for it.** Without one, the honest prediction is that the trimmer keeps `HANDOFFS.md`
under its cap and the read-set floor stops falling — which is level control working exactly as
specified, on the wrong axis.

---

## 11. Implementation phases — one session each

**Each phase is one session. Close out when done. STOP. Do not bundle** (FM #18: a plan and its code
are never one session; FM #26: two capabilities are never one slice).

**Every outward-facing step needs the operator's explicit go-ahead, each time** — `CLAUDE.md`
§Contributing upstream. Phases 3, 4 and 5 all end in adopter-facing changes; **none of them opens a
PR.** Prepare, vet, then ask. "The ship decision is made" settles *what* ships, never *when a PR is
opened*.

### Phase 1 → **S37**: build the trimmer, canonical-only, and prove it here

**Done looks like:** `starter-kit/methodology_trim.py` exists and is **not** in the manifest; dry-run
by default; refuses to write unless L1+L2+L3 pass; refuses on a non-empty undocumented set (P1);
writes its own ledger entry and asserts the P1a post-condition; refuses on an existing shard path;
refuses on SRF ≥ 1.00 without `--force`; abstains out loud when SRF is undefined; emits
`<shard>.verify.sh`; writes shard-then-live via temp-and-rename and **never commits**.

**Verify — in this order** (the verify script does not exist until a write has happened):
```sh
python3 starter-kit/methodology_trim.py --file HANDOFFS.md            # dry run is the default
git status --porcelain                                                # empty — nothing written
python3 starter-kit/methodology_trim.py --file HANDOFFS.md --write
bash docs/archive/<shard>.verify.sh; echo $?                          # 0
git status --porcelain                                                # exactly 2 paths, uncommitted
git checkout -- HANDOFFS.md && rm docs/archive/<shard>*              # the documented rollback
bash bin/tests.sh                                                     # 175 passed / 1 failed (Test 9)
python3 -m unittest discover -s tools                                 # green
```
**Gates:** drive **each** of L1, L2, L3 RED on a fixture and watch it fail before trusting green —
and **narrow** each guard's domain, not just delete it; a guard proven only by deletion is proven only
to run. Prove the **fixture** first with an unmutated control. Reproduce the §2.1 footer loss as the
L2 fixture and the §4.2 S22 edit as the L3 fixture: both are real, both already happened.
**Assert on named findings, never on the exit code** (§6.3).

**Session boundary: STOP after S37.** Shipping is Phase 4.

### Phase 2 → **S36**: the three dashboard defects

Independent of S37; precedes S38 (do not put gauges in a broken instrument).

**Done looks like:** all three plan-D4 defects fixed in **both** twins — (a) the root-date query
returns the newest commit, not the oldest; (b) a 2,090-line `.md` can trip the large-file risk
(`.md` is absent from `SOURCE_EXTS`, so no markdown file can trip it at any size); (c) the
`methodology` self-exclusion removed.

**Verify:**
```sh
diff -q tools/methodology_dashboard.py starter-kit/methodology_dashboard.py   # identical
python3 -m unittest discover -s tools                                          # green
bash bin/tests.sh                                                              # 175/1
```
Each defect needs a test driven RED before its fix. **Session boundary: STOP after S36.**

### Phase 3 → **S38**: the dashboard row

**Done looks like:** a collector authors the conditional `(severity, description)` signal; both twins
byte-identical; the two A4 tests exist and both have been observed failing.

**Verify:**
```sh
diff -q tools/methodology_dashboard.py starter-kit/methodology_dashboard.py   # identical
python3 -m unittest discover -s tools
```

### Phase 4 → **S39′**: ship it (the decision is already made) — **SHIPPED (fork) 2026-08-04, fork session S39**

**Done looks like:** manifest entry added; `FRAMEWORK_INSTALLED_SOURCE` tuple updated;
`is_framework_installed()` recognises the trimmer; `DASHBOARD_VERSION` bumped in both twins;
`CHECKLIST_EXEMPT` or `METHODOLOGY_ITEMS` updated with a stated reason; exec-bit assertion added;
D6's **three live prose sentences** corrected (the two inside dated `CHANGELOG.md` entries stay
frozen — do not rewrite a dated record).

**Verify:**
```sh
python3 -m unittest discover -s tools        # Learning #12's guard driven RED FIRST, then patched
bash bin/tests.sh                            # 178/1 at close (175/1 when written) → Test 9 will 404 until upstream merges
diff -q tools/methodology_dashboard.py starter-kit/methodology_dashboard.py
# real sync into a throwaway repo — not a simulation:
D=$(mktemp -d); git -C "$D" init -q .; bin/sync "$D" --source=local
ls -l "$D/methodology_trim.py"               # present, mode 0755
bin/status "$D" | grep methodology_trim      # emits its row
rm -rf "$D"
```
**Do not weaken Test 9** to make the suite green — its 404 is the correct signal for a manifest entry
not yet upstream. **Session boundary: STOP after S39′. Do not open the PR** — ask.

**What this phase learned, recorded against the plan that set it (S39').** Three of the done-list's
premises did not survive contact:

- **The `FRAMEWORK_INSTALLED_SOURCE` entry and the `is_framework_installed` recognition are not two
  tasks — the first is inert without the second, and it is the one that silences the test.** Measured:
  with the name on the tuple and no content rule for it, a synced doc fixture still read `doc_only`
  False, `source_loc` 1,632, HIGH "No test infrastructure" — **a green suite over a live fleet-wide
  regression.** The suite in that state was the PRE-change one, **323 tests**; it is 323 that would
  have passed, not the 334 this session leaves behind, because the tests that catch this are the
  ones S39' added. Quoting the post-change count here would have credited the fix with catching a
  defect it was written in response to. The membership list is now *derived from* a per-name content table, so a name
  cannot be added without declaring how the file proves it is ours.
- **`DASHBOARD_VERSION` bump | test red** (§6.2's table) reads as a gate and is not one. Measured, the
  whole suite is green at the old version with every functional change in place; the bump is a
  judgment about adopter-visible behaviour. It moves **five** sites, not the four a plain
  `grep '2\.12\.0'` returns — one pin spells the digits with backslashes inside a regex literal.
- **Test 9 does not 404 "for a second reason".** `bin/sync`'s `read_github` exits on the FIRST
  failure and `starter-kit/FRAMEWORK_LEARNINGS.md` sits at DISTRIBUTION index 1 against the trimmer's
  index 8, so the trimmer's 404 is **masked**. Test 9 is evidence of the trimmer's upstream status in
  neither direction — do not read it as one.

Also found while discharging D6, and it is Phase 5's to inherit: **§11 Phase 5's own verify command
`grep -l archiv starter-kit/*.md   # currently empty` is not empty and this session made it less
empty.** Re-derived over the whole distributed set, not the narrow glob:

```sh
python3 -c "import sys;sys.path.insert(0,'bin');import _manifest as m;\
  print('\n'.join(sorted(e[0] for e in m.DISTRIBUTION if e[0].endswith('.md'))))" | xargs grep -l -i archiv
```
returns **three** files — `HOW_TO_USE.md` (a worked example's `POST /projects/:id/archive`
endpoint), `starter-kit/FRAMEWORK_LEARNINGS.md` (Learning #15's prose about *proving* a split
lossless), and **`starter-kit/BOOTSTRAP.md`, which S39' added**: the one-line inventory entry saying
what the newly distributed tool does. **The gap §7.3 depends on is unchanged** — a tool description
is not a policy; none of the three states a size norm, a trigger, or a procedure — but the check as
written now returns hits for a repo that still documents nothing, so Phase 5 must ask *what the file
says*, not *whether the word appears*. §10.1's *"returns nothing"* is stale for the same reason and
is corrected there.

### Phase 5 → **S40**: the doctrine — **SHIPPED (fork) 2026-08-04, fork session S40**

**Done looks like:** `starter-kit/CHANGELOG.md` and `starter-kit/HANDOFFS.md` each state a size norm,
the archive trigger **as a rate**, and the one-line-pointer shard convention — wording *"run this"*,
since the tool now ships. Today **zero** distributed files say anything on the subject.

**Verify — the published form was broken, and S39' said so before this phase started.**
`grep -l archiv starter-kit/*.md   # currently empty` was not empty at S39' (2 files) and is not
empty now (4). **A word is not a policy**, so the check was replaced with one that asserts what the
file *says* — the section heading the doctrine actually introduces:

```sh
# must return EXACTLY the two ledger seeds
python3 -c "import sys;sys.path.insert(0,'bin');import _manifest as m;\
  print('\n'.join(sorted(e[0] for e in m.DISTRIBUTION if e[0].endswith('.md'))))" \
  | xargs grep -l '^## Size, and when to archive'
bin/check-links                              # OK — 88 links / 22 files
bash bin/tests.sh                            # 178/1 — Test 9's expected github 404, unmoved
python3 -m unittest discover -s tools        # 334 OK
```
**Session boundary: STOP. Do not open the PR** — ask.

**What this phase learned, recorded against the plan that set it (S40).** Four of the done-list's
premises did not survive contact, and two changed the artifact:

- **"the archive trigger *as a rate*" is half the rule, and shipping only that half would have been
  silent on the file this campaign exists for.** §5.2 of this document says the byte metric is a
  **level with hysteresis, not a rate** — and measured at S40's claim, the *line* rate does **not**
  fire on `HANDOFFS.md` (headroom 20 against a threshold of 15); only the byte level does. A
  rate-only doctrine reproduces exactly the blindness §5.1 was written to fix. Both seeds therefore
  state **both** conditions with the correct form for each. **This is a departure from Phase 5's
  wording, adopted deliberately and labelled here**; §5.2 is the specific rule and Phase 5's summary
  is the loose restatement.
- **§5.4's "S40 documents choosing it" is a fourth done-item this list omits.** The budget is
  judgment; both seeds now say how to calibrate it and name `--budget-bytes`.
- **"each state … the one-line-pointer shard convention" is load-bearing on *each*, and the first
  draft failed it.** The `HANDOFFS.md` seed delegated the whole shard convention to the
  `CHANGELOG.md` seed. Both files are **SEED** disposition — written only when the destination is
  absent — so they install independently, and an adopter can receive one whose entire convention
  lives in a section the other file never delivered. Caught by review; the receipt seed now states
  the path shape, the pointer rule and the span-both-by-glob rule in its own words, and cross-refers
  only for shared *reasoning*.
- **The seeds reach no *existing* adopter, and nothing in the shipped mechanism will tell them.**
  SEED means never-overwritten, and `bin/_manifest.py`'s `SEED_FORMAT_MARKERS` key on the files' H1
  titles, which this change deliberately leaves intact — so `bin/status` reports every existing
  adopter's ledger as `present`, not `present (stale format)`. Changing that marker would flag every
  adopter at once; it is a real operator decision and was **not** taken here. **Consequence for the
  successor:** the dashboard's absent-branch remedy must *not* be pointed at these sections. The two
  are anti-correlated — the trimmer is `TRACKED`, so "tool absent" means "has not synced since S39'",
  which means the adopter's seed also predates S40. Pointing there would name a section that reader
  is structurally guaranteed not to have. S39' handed that item forward; this is its answer, and the
  answer is *no*.

---

## 12. Verification plan for this design

| Claim | Command |
|---|---|
| Footer lost (D1) | `for s in 3aee4e3 020ba3f HEAD; do git show $s:CHANGELOG.md \| grep -c 'Release history before v3.0'; done` → `1 0 0` |
| SRF RED | `git cat-file -s $(git rev-parse 7a71df0^:HANDOFFS.md)` etc. → 224368 / 52927 / 227538 |
| Line trigger blind | `git show 2fc2c5b:HANDOFFS.md \| wc -l` → 896 vs 997 pre-archive; bytes 227538 vs 224368 |
| Prose outside fences | the fence scanner in **§2.2** → `total 227538 B \| inside 174957 B (76.9%) \| outside 52581 B (23.1%)` |
| BACKLOG not trimmable | `git show 2fc2c5b:docs/planning/BACKLOG.md \| grep -c '^### '` → 0 |
| Separator cause false (D5) | `git show 7a71df0^:HANDOFFS.md \| grep -- '---' \| grep -vc '^---$'` → 0 |
| **Frontier poisoning** | the **self-contained reproduction script in §8.1** — run it; → `BEFORE trim: undocumented = 1` / `AFTER trim: undocumented = 0` |
| L1's unscoped form unsatisfiable | the `cmp` block in **§4.2** → `differ: char 44` and `differ: char 3389` |
| `](` corrupts absolute URLs | the `awk` classifier in **§4.3** → `14 absolute-URL   8 already-relative   1 root-relative` |
| "above 30" unreachable on bytes | the `python3 -c` block in **§5.2** → `reaches 30? False` at every budget |
| `bin/` ships nothing | `python3 -c "import sys; sys.path.insert(0,'bin'); import _manifest as m; print(sum(1 for e in m.DISTRIBUTION if e[0].startswith('bin/')))"` → 0 |

**Every row above was executed during this session, not reasoned about.** Four findings in this
document were produced by an adversarial review of an earlier draft and are recorded in §8.3 or fixed
in place: the unscoped L1 (unsatisfiable), the `](` domain predicate (corrupts 14 URLs), the
transplanted 15/30 thresholds (unreachable), and the shard-collision blind spot (invisible to
L1/L2/L3). A fifth — the `../../` figure attributed to the wrong shard — is why §4.3 now carries its
own command.
