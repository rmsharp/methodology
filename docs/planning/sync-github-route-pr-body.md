# Pull-request body — the `--source=github` update route

**Status:** drafted for the operator's review. Nothing has been pushed or opened. The text below the rule is the
body verbatim; everything above it is fork-side scaffolding and is not part of the pull request.

**Suggested title:** `bin/sync --source=github`: an update route that can recognize a file as merely behind, and a
refusal that names its own cause

**Recognized-terms check** (0 hits required). It reads only the body — everything after the first standalone
rule — because the pattern would otherwise match this very command:

```sh
sed -n '/^---$/,$p' docs/planning/sync-github-route-pr-body.md \
  | grep -nE 'S[0-9]{2,3}\b|BL-[0-9]+|\bD[0-9]\b|b1-sync|sync-github-route'
```

---

`README.md` tells every adopter to update with the repository URL. The only command the documents give that
instruction is `bin/sync --source=github`, and that route cannot recognize a file as merely behind — so it refuses an
unedited project's files as *local modifications* and tells the reader to pass `--force`.

This was a deliberate deferral, not an oversight. Issue #32 put it out of scope in as many words —
*"`--source=github` incremental history walk (defer + document)"* — and half of that deferral landed:
`starter-kit/BOOTSTRAP.md` has said to prefer `--source=local` ever since. The other half did not. `--source`'s help
text still reads *"local (default if sibling methodology/ exists) or github"*, and `README.md` still lists the URL
route beside the other two marked only *"(needs gh CLI)"* — a tooling requirement, not the limitation. So the
documents disagree with each other, and the route the top-level instruction points at is the one that fails.

## What the route does now

`--source=github` clones the repository for the run instead of fetching file contents one at a time. The clone carries
the history, so the existing local-source code path — the one that already recognizes an unmodified file as an older
canonical version and upgrades it without `--force` — is what runs. Nothing about the local route changes.

Three consequences, all of them measured below:

1. **A project that is merely behind updates cleanly.** No `--force`, no refusal.
2. **A genuine local edit is still refused,** with the identical file list. The guard is not weakened; it is given the
   evidence it needed.
3. **The `gh` CLI is no longer required.** The route needs `git` and network. Four documents said otherwise and now
   say *needs git and network*.

## A source that has no history says so

The same refusal had a second failure: from a shallow clone or a downloaded tarball, `bin/sync` blamed the project's
files for a gap in the *source*. `BOOTSTRAP.md` already warned that a shallow clone or a tarball loses that history;
the refusal did not. It now asks its source what history it has before refusing. A source with no `.git` is named as
such and given the `git clone` command; a shallow checkout is named with its own commit count and given
`git -C <source> fetch --unshallow`. Either cause changes the header from *local modifications* to *differ from the
canonical version* and keeps exit 2. A full-history source prints exactly the text it printed before.

The *"To inspect the drift first:"* header used to print with no lines under it on the URL route, because there was no
checkout to diff against. It now prints a clone pinned to the commit the run read, plus one `diff` per file.

## The history-walk fix rides with it

This is the follow-up PR #84's body promised:

> The history-walk fix for `bin/sync` and `bin/status` (git's default walk can hide a published version behind a
> merge, so an unmodified file reads *locally modified*) — a separate, small PR to follow.

It is here rather than separate because the GitHub route is built on exactly those two walks. Shipping the route on
the unfixed walk would put a known defect into a new path; the two are one change. `bin/status` now counts the
versions that landed on the first-parent line and falls back to the full walk, and both tools look up history blobs in
one batched `git` call rather than one call per commit.

## Evidence

**Six projects that use this framework, updated by both the old and the new route** (`--dry-run`, nothing written):

| Before (contents fetched one file at a time) | After (the run clones the repository) |
|---|---|
| exit 2, 10 files refused as *local modifications* | **exit 0, 15 files would be written** |
| exit 2, 8 files refused | **exit 0, 16 files would be written** |
| exit 2, 7 files refused | exit 2, **the identical 7** refused |
| exit 2, 8 files refused | exit 2, **the identical 8** refused |
| exit 2, 8 files refused | exit 2, **the identical 8** refused |
| exit 2, 7 files refused | exit 2, **the identical 7** refused |

On the two projects that flip, **every file the old route refused is one the new route writes** — the refused set is a
subset of the written set, checked file by file, not by count. On the other four the refused sets are identical
member for member: those projects have real local edits, and both routes are right to hold them back.

**Incidentally faster and less fragile.** The old route issued one HTTPS request per distributed file — 29 per run,
12–15 s. In one of the twelve runs above, 4 of those 29 timed out (*"net/http: TLS handshake timeout"*) and the run
exited 1 having read nothing; a retry succeeded. The new route is one clone: 1.7–2.7 s in the same session.

**Tests.** `bash bin/tests.sh` reports **139 passed, 0 failed** at the commit this branch starts from and **188
passed, 0 failed** at its tip, both in clones with no local state. Diffing the two runs' `PASS:` lines names **49
assertions present only on this branch and none of the base's missing** from it. `.quality-gates.json` raises
`tests-sh-passed` to 188 in the same branch, so the new assertions are ratcheted rather than merely present.

The tests are hermetic: they build a fixture repository with two merge-hiding shapes, serve it over `file://`, and
assert `status` and `sync` per version — including a shallow clone and a tree with no `.git`, and a control in which
the full-history source upgrades the same file. Both refusal causes and the inspect hint are covered; the hint's test
runs the printed commands and checks the `diff` actually shows the edit, so a wording match cannot pass for it.

## Merging

The branch is based directly on the current `main` — merging it is a fast-forward today, and the resulting tree is
byte-identical to the branch tip (checked with `git merge-tree --write-tree`, not assumed).

Against the other open pull requests, two conflicts, both mechanical, both tested:

- **PR #84 — `starter-kit/BOOTSTRAP.md`.** Both branches edit the one-line *Updating an existing project* paragraph:
  #84 rewrites its **tail** and leaves the head byte-identical to `main`; this branch rewrites its **head** and leaves
  the tail byte-identical. So the resolution is #84's tail after this branch's head. Built and run: the merged tree
  passes **212 assertions, 0 failures**, including both of #84's own assertions that pin phrases in that paragraph.
- **PR #86 — `.quality-gates.json`.** One line: #86 raises `tests-sh-passed` to 142, this branch to 188. A minimum
  resolves to the larger. Built and run: the merged tree measures **191 passed, 0 failed**, so whoever merges second
  should set the floor to 191.

`CHANGELOG.md` conflicts with PRs #83, #85 and #86, as ledger entries do; keeping both sides resolves it.

## Deliberately not in this PR

- No change to the local route's behaviour, to the manifest, or to any distributed document beyond the sentences that
  described this route.
- `bin/status` reading a merely-behind file as *locally modified* when its **source** has no history. `bin/sync`
  refuses and so has somewhere to say why; `status` prints a table of per-file rows with no such place. Found and
  recorded, not fixed here.
- No principle, phase, gate or workstream change; no release.
