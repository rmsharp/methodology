#!/usr/bin/env bash
# Smoke tests for bin/sync and bin/status.
# Run: ./bin/tests.sh  (from methodology repo root)
set -uo pipefail

BIN="$(cd "$(dirname "$0")" && pwd)"
METHODOLOGY="$(dirname "$BIN")"
STARTER="$METHODOLOGY/starter-kit"
PASS=0
FAIL=0

pass() { echo "  PASS: $*"; PASS=$((PASS+1)); }
fail() { echo "  FAIL: $*"; FAIL=$((FAIL+1)); }

mktemp_project() {
    local dir
    dir="$(mktemp -d)"
    git -C "$dir" init -q
    echo "$dir"
}

echo "== Test 1: commit mode + local source (baseline) =="
P="$(mktemp_project)"
"$BIN/sync" "$P" --mode=commit --source=local >/dev/null
diff -q "$P/SESSION_RUNNER.md" "$STARTER/SESSION_RUNNER.md" >/dev/null && pass "SESSION_RUNNER matches canonical" || fail "SESSION_RUNNER drift"
diff -q "$P/SAFEGUARDS.md" "$STARTER/SAFEGUARDS.md" >/dev/null && pass "SAFEGUARDS matches canonical" || fail "SAFEGUARDS drift"
diff -q "$P/methodology_dashboard.py" "$STARTER/methodology_dashboard.py" >/dev/null && pass "dashboard matches canonical" || fail "dashboard drift"
[ -x "$P/methodology_dashboard.py" ] && pass "dashboard is executable" || fail "dashboard not executable"
[ ! -f "$P/.gitignore" ] && pass "commit mode leaves .gitignore alone" || fail "commit mode created .gitignore"
rm -rf "$P"

echo "== Test 2: dry-run doesn't modify =="
P="$(mktemp_project)"
"$BIN/sync" "$P" --dry-run >/dev/null
[ ! -f "$P/SESSION_RUNNER.md" ] && pass "dry-run skipped SESSION_RUNNER" || fail "dry-run wrote SESSION_RUNNER"
[ ! -f "$P/.gitignore" ] && pass "dry-run skipped .gitignore" || fail "dry-run wrote .gitignore"
rm -rf "$P"

echo "== Test 3: ignore mode adds .gitignore + warns on tracked files =="
P="$(mktemp_project)"
"$BIN/sync" "$P" --mode=commit --source=local >/dev/null
(cd "$P" && git add -A && git -c user.email=t@t -c user.name=t commit -q -m "baseline")
OUTPUT="$("$BIN/sync" "$P" --mode=ignore 2>&1)"
grep -q "^/SESSION_RUNNER.md$" "$P/.gitignore" && pass "gitignore has SESSION_RUNNER" || fail "gitignore missing SESSION_RUNNER"
grep -q "^/SAFEGUARDS.md$" "$P/.gitignore" && pass "gitignore has SAFEGUARDS" || fail "gitignore missing SAFEGUARDS"
grep -q "^/methodology_dashboard.py$" "$P/.gitignore" && pass "gitignore has dashboard" || fail "gitignore missing dashboard"
echo "$OUTPUT" | grep -q "WARNING" && pass "ignore mode warns on tracked files" || fail "ignore mode silent on tracked files"
echo "$OUTPUT" | grep -q "git -C .* rm --cached" && pass "warning includes rm --cached command" || fail "warning missing rm command"
# Idempotent on second run
"$BIN/sync" "$P" --mode=ignore >/dev/null
[ "$(grep -c '^/SESSION_RUNNER.md$' "$P/.gitignore")" = "1" ] && pass "idempotent gitignore" || fail "gitignore duplicated"
rm -rf "$P"

echo "== Test 4: auto-detect mode from .gitignore =="
P="$(mktemp_project)"
printf "/SESSION_RUNNER.md\n/SAFEGUARDS.md\n/methodology_dashboard.py\n" > "$P/.gitignore"
OUTPUT="$("$BIN/sync" "$P" 2>&1)"
echo "$OUTPUT" | grep -q "mode:    ignore" && pass "auto-detected ignore mode" || fail "mode auto-detect wrong: $OUTPUT"
rm -rf "$P"

echo "== Test 5: auto-detect source prefers local sibling =="
P="$(mktemp_project)"
OUTPUT="$("$BIN/sync" "$P" --dry-run 2>&1)"
echo "$OUTPUT" | grep -q "source:  local" && pass "auto-detected local source" || fail "source auto-detect wrong"
rm -rf "$P"

echo "== Test 6: status reports current / modified / N-behind / missing =="
P="$(mktemp_project)"
"$BIN/sync" "$P" --mode=commit >/dev/null
OUT="$("$BIN/status" "$P")"
echo "$OUT" | grep -q "current" && pass "status: current" || fail "status: current missing"

echo "# local edit" >> "$P/SESSION_RUNNER.md"
OUT="$("$BIN/status" "$P")"
echo "$OUT" | grep -q "locally modified" && pass "status: locally modified" || fail "status: locally modified missing"

# Revert to an older blob from methodology history
OLDER_COMMIT="$(git -C "$METHODOLOGY" log --format=%H -- starter-kit/SESSION_RUNNER.md | sed -n '2p')"
if [ -n "$OLDER_COMMIT" ]; then
    git -C "$METHODOLOGY" show "$OLDER_COMMIT:starter-kit/SESSION_RUNNER.md" > "$P/SESSION_RUNNER.md"
    OUT="$("$BIN/status" "$P")"
    echo "$OUT" | grep -Eq "[0-9]+ version" && pass "status: N versions behind detected" || fail "status: N-behind not detected"
fi

rm "$P/SAFEGUARDS.md"
OUT="$("$BIN/status" "$P")"
echo "$OUT" | grep -q "missing" && pass "status: missing" || fail "status: missing not detected"
rm -rf "$P"

echo "== Test 7: sync refuses to overwrite locally-modified files without --force =="
P="$(mktemp_project)"
"$BIN/sync" "$P" --mode=commit >/dev/null
echo "# LOCAL CUSTOMIZATION" >> "$P/SESSION_RUNNER.md"
BEFORE="$(cat "$P/SESSION_RUNNER.md")"
OUTPUT="$("$BIN/sync" "$P" 2>&1)"; RC=$?
[ "$RC" != "0" ] && pass "sync exits non-zero when local drift present" || fail "sync exited 0 despite local drift"
echo "$OUTPUT" | grep -q "ERROR" && pass "sync prints ERROR on local drift" || fail "no ERROR printed"
echo "$OUTPUT" | grep -q -- "--force" && pass "ERROR mentions --force" || fail "ERROR missing --force hint"
[ "$(cat "$P/SESSION_RUNNER.md")" = "$BEFORE" ] && pass "file unchanged when blocked" || fail "file modified despite block"

# --force proceeds
"$BIN/sync" "$P" --force >/dev/null && pass "--force overrides block" || fail "--force did not override"
diff -q "$P/SESSION_RUNNER.md" "$STARTER/SESSION_RUNNER.md" >/dev/null && pass "--force restores canonical" || fail "--force did not restore canonical"
rm -rf "$P"

echo "== Test 8: sync upgrades N-versions-behind without --force =="
P="$(mktemp_project)"
"$BIN/sync" "$P" --mode=commit >/dev/null
OLDER_COMMIT="$(git -C "$METHODOLOGY" log --format=%H -- starter-kit/SESSION_RUNNER.md | sed -n '2p')"
if [ -n "$OLDER_COMMIT" ]; then
    git -C "$METHODOLOGY" show "$OLDER_COMMIT:starter-kit/SESSION_RUNNER.md" > "$P/SESSION_RUNNER.md"
    "$BIN/sync" "$P" >/dev/null && pass "upgrade from older version proceeds without --force" || fail "upgrade blocked incorrectly"
    diff -q "$P/SESSION_RUNNER.md" "$STARTER/SESSION_RUNNER.md" >/dev/null && pass "upgraded to canonical" || fail "not upgraded"
fi
rm -rf "$P"

echo "== Test 9: github source (requires gh auth; skipped if unauthenticated) =="
if gh auth status >/dev/null 2>&1; then
    P="$(mktemp_project)"
    "$BIN/sync" "$P" --source=github --dry-run >/dev/null && pass "github source dry-run works" || fail "github source dry-run failed"
    rm -rf "$P"
else
    echo "  SKIP: gh unauthenticated"
fi

echo "== Test 10: distributed-file links resolve in the simulated adopter tree =="
if "$BIN/check-links" >/dev/null 2>&1; then
    pass "check-links: all relative links resolve in adopter layout"
else
    "$BIN/check-links" 2>&1 | sed 's/^/    /'
    fail "check-links: dangling link(s) in adopter layout (see above)"
fi

echo "== Test 11: sync produces the full manifest tree (faithful, per-file) =="
P="$(mktemp_project)"
"$BIN/sync" "$P" --mode=commit >/dev/null
MANIFEST_OK=1
COUNT=0
while IFS='|' read -r src dest disp; do
    [ -z "$dest" ] && continue
    COUNT=$((COUNT+1))
    if [ ! -f "$P/$dest" ]; then MANIFEST_OK=0; echo "    MISSING: $dest"; continue; fi
    if [ "$disp" = "tracked" ]; then
        diff -q "$P/$dest" "$METHODOLOGY/$src" >/dev/null || { MANIFEST_OK=0; echo "    DRIFT: $dest"; }
    fi
done < <(python3 -c "import sys; sys.path.insert(0, '$BIN'); import _manifest; [print('%s|%s|%s' % (s, d, x)) for s, d, x in _manifest.DISTRIBUTION]")
[ "$MANIFEST_OK" = "1" ] && pass "all $COUNT manifest files present; tracked files match canonical" || fail "manifest tree incomplete/drifted"
# subdir dest spot-check (the multi-dir tree, not just root files)
[ -f "$P/docs/methodology/ITERATIVE_METHODOLOGY.md" ] && pass "framework doc landed under docs/methodology/" || fail "docs/methodology/ doc missing"
[ -f "$P/docs/methodology/workstreams/AUDIT_WORKSTREAM.md" ] && pass "workstream landed under docs/methodology/workstreams/" || fail "workstreams/ doc missing"
rm -rf "$P"

echo "== Test 12: seed files created once, never clobbered (even --force) =="
P="$(mktemp_project)"
"$BIN/sync" "$P" >/dev/null
[ -f "$P/SESSION_NOTES.md" ] && pass "seed SESSION_NOTES created when absent" || fail "seed not created"
echo "ADOPTER LOG ENTRY" > "$P/SESSION_NOTES.md"
"$BIN/sync" "$P" >/dev/null
grep -q "ADOPTER LOG ENTRY" "$P/SESSION_NOTES.md" && pass "seed not overwritten on normal sync" || fail "seed overwritten on sync"
"$BIN/sync" "$P" --force >/dev/null
grep -q "ADOPTER LOG ENTRY" "$P/SESSION_NOTES.md" && pass "seed not overwritten even with --force" || fail "seed overwritten by --force"
rm -rf "$P"

echo "== Test 13: adopter-owned instances are never sync targets =="
P="$(mktemp_project)"
"$BIN/sync" "$P" >/dev/null
[ ! -f "$P/CONTEXT.md" ] && pass "sync did not create instance CONTEXT.md" || fail "sync created instance CONTEXT.md"
[ ! -f "$P/CLAUDE.md" ] && pass "sync did not create instance CLAUDE.md" || fail "sync created instance CLAUDE.md"
[ -f "$P/CONTEXT_TEMPLATE.md" ] && pass "template CONTEXT_TEMPLATE.md is present" || fail "template CONTEXT_TEMPLATE.md missing"
rm -rf "$P"

echo "== Test 14: check-links validates the sync-produced tree without mutating it (issue #36) =="
P="$(mktemp_project)"
"$BIN/sync" "$P" >/dev/null
BEFORE="$(cd "$P" && find . -type f | sort)"
if "$BIN/check-links" --tree "$P" >/dev/null 2>&1; then
    pass "check-links --tree: links resolve in the sync-produced tree"
else
    "$BIN/check-links" --tree "$P" 2>&1 | sed 's/^/    /'
    fail "check-links --tree: dangling link(s) in sync-produced tree"
fi
# A checker must not write to the tree it validates (issue #36): it must not
# fabricate the adopter-owned placeholder files (CONTEXT.md, CLAUDE.md, …) that a
# sync-produced tree legitimately lacks.
AFTER="$(cd "$P" && find . -type f | sort)"
if [ "$BEFORE" = "$AFTER" ]; then
    pass "check-links --tree: left the validated tree unmodified (issue #36)"
else
    fail "check-links --tree: mutated the tree it validated (issue #36)"
    diff <(printf '%s\n' "$BEFORE") <(printf '%s\n' "$AFTER") | sed 's/^/    /'
fi
rm -rf "$P"

echo "== Test 15: status emits per-file rows with a disposition column (Phase 4) =="
P="$(mktemp_project)"
"$BIN/sync" "$P" --mode=commit >/dev/null
OUT="$("$BIN/status" "$P")"
echo "$OUT" | grep -q "Disposition" && pass "status: Disposition column present" || fail "status: no Disposition column"
echo "$OUT" | grep -q "tracked" && pass "status: tracked disposition shown" || fail "status: no tracked rows"
echo "$OUT" | grep -q "seed" && pass "status: seed disposition shown" || fail "status: no seed rows"
# One data row per manifest entry (full Option-B corpus, not a fixed three)
EXPECTED="$(python3 -c "import sys; sys.path.insert(0, '$BIN'); import _manifest; print(len(_manifest.DISTRIBUTION))")"
GOT="$(echo "$OUT" | grep -c "$(basename "$P")")"
[ "$GOT" = "$EXPECTED" ] && pass "status: one row per manifest file ($GOT == $EXPECTED)" || fail "status: row count $GOT != manifest $EXPECTED"
# Freshly-synced tree: every tracked file current, nothing flagged as drift
echo "$OUT" | grep -q "current" && pass "status: fresh tree shows current" || fail "status: fresh tree missing current"
if echo "$OUT" | grep -Eq "locally modified|versions? behind"; then fail "status: fresh tree shows spurious drift"; else pass "status: fresh tree shows no drift"; fi
rm -rf "$P"

echo "== Test 16: an absent seed file is reported, never flagged as drift (Phase 4 DONE) =="
P="$(mktemp_project)"
"$BIN/sync" "$P" >/dev/null
rm -f "$P/CHANGELOG.md"   # CHANGELOG.md is a SEED file (adopter-owned)
SEEDLINE="$("$BIN/status" "$P" | grep "CHANGELOG.md")"
echo "$SEEDLINE" | grep -q "seed" && pass "status: CHANGELOG shown with seed disposition" || fail "status: CHANGELOG not marked seed"
echo "$SEEDLINE" | grep -q "absent" && pass "status: absent seed shown as 'absent'" || fail "status: absent seed not 'absent'"
if echo "$SEEDLINE" | grep -q "missing"; then fail "status: absent seed mislabeled as drift (missing)"; else pass "status: absent seed NOT flagged as drift"; fi
rm -rf "$P"

echo "== Test 17: a partially-stale tree flags only the stale file (Phase 4) =="
P="$(mktemp_project)"
"$BIN/sync" "$P" >/dev/null
echo "# local edit" >> "$P/SESSION_RUNNER.md"
OUT="$("$BIN/status" "$P")"
NMOD="$(echo "$OUT" | grep -c "locally modified")"
[ "$NMOD" = "1" ] && pass "status: exactly one file locally modified" || fail "status: expected 1 modified, got $NMOD"
echo "$OUT" | grep "SESSION_RUNNER.md" | grep -q "locally modified" && pass "status: the stale file is SESSION_RUNNER" || fail "status: wrong file flagged stale"
rm -rf "$P"

echo "== Test 18: dashboard scoring unit tests (BL-5 doc-only reshape) =="
if python3 "$METHODOLOGY/tools/test_methodology_dashboard.py" >/dev/null 2>&1; then
    pass "dashboard scoring unit tests green"
else
    fail "dashboard scoring unit tests failed"
fi

echo "== Test 19: dashboard twins byte-identical + same DASHBOARD_VERSION =="
diff -q "$METHODOLOGY/tools/methodology_dashboard.py" "$STARTER/methodology_dashboard.py" >/dev/null \
    && pass "dashboard twins byte-identical" || fail "dashboard twins differ"
TV="$(grep -E '^DASHBOARD_VERSION' "$METHODOLOGY/tools/methodology_dashboard.py")"
SV="$(grep -E '^DASHBOARD_VERSION' "$STARTER/methodology_dashboard.py")"
[ "$TV" = "$SV" ] && pass "dashboard twins carry the same DASHBOARD_VERSION" || fail "DASHBOARD_VERSION mismatch across twins"

echo "== Test 20: a seed whose format predates canonical is flagged advisory-only (BL-6 item 2) =="
P="$(mktemp_project)"
"$BIN/sync" "$P" >/dev/null
# Row-vs-note isolation: the migration note also names CHANGELOG.md and contains the tokens 'seed'
# and 'stale format', so any row-specific assertion must exclude the note line (`grep -v '^note:'`)
# or it is vacuous — it would pass on the prose note regardless of the table row (adversarial-review fix).
# (a) Freshly-seeded CHANGELOG carries the current action-ledger format → plain 'present', no note.
OUT="$("$BIN/status" "$P")"
echo "$OUT" | grep "CHANGELOG.md" | grep -v '^note:' | grep -q "stale format" && fail "status: current-format (fresh) seed mis-flagged stale" || pass "status: current-format (fresh) seed not flagged"
echo "$OUT" | grep -q "^note:" && fail "status: spurious stale-format note on fresh tree" || pass "status: no stale-format note on fresh tree"
# (b) In-use current-format ledger: the METHODOLOGY-SEED-SENTINEL is deleted (as the adopter does on its
# first real entry) and a dated entry appended, but the ledger TITLE is retained. This is the exact case
# the marker choice is engineered around (key on the lifetime-stable title, NOT the deletable sentinel);
# it must NOT be flagged, or binding constraint #2 (no false positive on a current-format seed) breaks.
printf '# Changelog — Authoritative Action Ledger\n\nThe action ledger.\n\n---\n\n### 2026-01-01 · [ad hoc] a real entry\n- Change: something real.\n' > "$P/CHANGELOG.md"
grep -q "METHODOLOGY-SEED-SENTINEL" "$P/CHANGELOG.md" && fail "test-bug: in-use fixture still carries the sentinel" || pass "test: in-use fixture is title-only (sentinel deleted)"
OUT="$("$BIN/status" "$P")"
echo "$OUT" | grep "CHANGELOG.md" | grep -v '^note:' | grep -q "stale format" && fail "status: in-use current-format ledger mis-flagged stale (constraint #2)" || pass "status: in-use current-format ledger not flagged"
echo "$OUT" | grep -q "^note:" && fail "status: spurious note on in-use current-format ledger" || pass "status: no note on in-use current-format ledger"
# (c) Replace the seed with a pre-v3.1 (Keep-a-Changelog) shape lacking the ledger-title marker.
printf '# Changelog\n\nAll notable changes to this project.\n\n## [Unreleased]\n' > "$P/CHANGELOG.md"
OUT="$("$BIN/status" "$P")"
ROW="$(echo "$OUT" | grep "CHANGELOG.md" | grep -v '^note:')"   # table row only, note excluded
echo "$ROW" | grep -q "seed" && pass "status: stale seed keeps its seed disposition" || fail "status: stale seed lost seed disposition"
echo "$ROW" | grep -q "stale format" && pass "status: pre-v3.1 seed flagged 'present (stale format)'" || fail "status: stale seed not flagged"
# Advisory only — never reclassified as drift.
if echo "$ROW" | grep -Eq "missing|locally modified|versions? behind"; then fail "status: stale seed mislabeled as drift"; else pass "status: stale seed NOT treated as drift"; fi
echo "$OUT" | grep -q "^note:" && pass "status: emits the migration note beneath the table" || fail "status: no migration note for stale seed"
# (d) A seed without a format marker (SESSION_NOTES.md) is never format-checked → never stale.
echo "arbitrary adopter content" > "$P/SESSION_NOTES.md"
"$BIN/status" "$P" | grep "SESSION_NOTES.md" | grep -v '^note:' | grep -q "stale format" && fail "status: markerless seed mis-flagged" || pass "status: markerless seed never flagged stale"
# (e) The flag never triggers an overwrite: sync leaves the adopter-owned stale seed untouched.
"$BIN/sync" "$P" >/dev/null
grep -q "\[Unreleased\]" "$P/CHANGELOG.md" && pass "sync: stale seed left untouched (still adopter-owned)" || fail "sync: stale seed was overwritten"
"$BIN/status" "$P" | grep "CHANGELOG.md" | grep -v '^note:' | grep -q "stale format" && pass "status: still flags stale after a re-sync" || fail "status: stale flag lost after re-sync"
# (f) Multi-project scan: the note headline counts stale INSTANCES (one per project), matching the number
# of flagged table rows — not distinct file types (adversarial-review fix). P is still stale from (c/e).
P2="$(mktemp_project)"
"$BIN/sync" "$P2" >/dev/null
printf '# Changelog\n\n## [Unreleased]\n' > "$P2/CHANGELOG.md"
MULTI="$("$BIN/status" "$P" "$P2")"
NROWS="$(echo "$MULTI" | grep -v '^note:' | grep -c "stale format")"
[ "$NROWS" = "2" ] && pass "status: two stale rows across two projects" || fail "status: expected 2 stale rows, got $NROWS"
echo "$MULTI" | grep '^note:' | grep -q "2 seeds predate" && pass "status: note count matches flagged rows (2), not deduped file types" || fail "status: note count != flagged rows"
rm -rf "$P" "$P2"

# Shared fixture builder for Tests 21-22: a fully well-formed, status: complete
# `handoff` receipt (starter-kit/HANDOFFS.md field list). Each variant below pipes
# this through sed/grep to break exactly one thing.
good_handoff() {
    cat <<'EOF'
```handoff
session: S12
date: 2026-07-08
status: complete
self_score: 8
predecessor_score: 7
active_task: Implementing bin/check-handoff (Phase P2)
what_was_done: Wrote bin/check-handoff and Tests 21-22; commit a1b2c3d
next_steps: Wire bin/check-handoff into SESSION_RUNNER.md Phase 3D close-out gate
key_files: bin/check-handoff:1, bin/tests.sh:230
gotchas: A bare-backtick wrapper around an example must not parse as a real block
runtime_smoke: n/a — docs-only
changelog_ref: PR #52
commit: a1b2c3d
```
Free-text prose: implemented the checker end to end, self-score +8/-2 (docstring could be tighter).
EOF
}

echo "== Test 21: check-handoff — well-formed receipt passes; field/value defects are caught =="
F="$(mktemp)"
good_handoff > "$F"
"$BIN/check-handoff" --file "$F" >/dev/null 2>&1 && pass "well-formed complete receipt passes" || fail "well-formed complete receipt should pass"
rm -f "$F"

F="$(mktemp)"
good_handoff | grep -v '^gotchas:' > "$F"
"$BIN/check-handoff" --file "$F" >/dev/null 2>&1 && fail "missing required key (gotchas) not caught" || pass "missing required key (gotchas) caught"
rm -f "$F"

F="$(mktemp)"
good_handoff | sed 's/^next_steps:.*/next_steps: /' > "$F"
"$BIN/check-handoff" --file "$F" >/dev/null 2>&1 && fail "empty required field (next_steps) not caught" || pass "empty required field (next_steps) caught"
rm -f "$F"

F="$(mktemp)"
good_handoff | sed 's/^self_score:.*/self_score: 11/' > "$F"
"$BIN/check-handoff" --file "$F" >/dev/null 2>&1 && fail "self_score out of 1..10 not caught" || pass "self_score out of 1..10 caught"
rm -f "$F"

F="$(mktemp)"
good_handoff | sed 's#^key_files:.*#key_files: bin/check-handoff, bin/tests.sh#' > "$F"
"$BIN/check-handoff" --file "$F" >/dev/null 2>&1 && fail "key_files missing path:line token not caught" || pass "key_files missing path:line token caught"
rm -f "$F"

# Regression (final-review C1): an incidental colon-digit run in prose (a scripture
# ref, a time, a ratio) must NOT satisfy key_files — the pre-colon token must be path-like.
F="$(mktemp)"
good_handoff | sed 's#^key_files:.*#key_files: reviewed the citation John 3:16, no files edited#' > "$F"
"$BIN/check-handoff" --file "$F" >/dev/null 2>&1 && fail "key_files incidental colon-digit (John 3:16) wrongly passed" || pass "key_files incidental colon-digit (no path) caught"
rm -f "$F"

# Regression (final-review C2): a bare 7+ digit decimal (a count/timestamp) must NOT
# satisfy what_was_done's sha-shape check — a real sha carries a hex letter.
F="$(mktemp)"
good_handoff | sed 's#^what_was_done:.*#what_was_done: processed 12345678 records, forgot to note the sha#' > "$F"
"$BIN/check-handoff" --file "$F" >/dev/null 2>&1 && fail "what_was_done decimal-only (12345678, no sha) wrongly passed" || pass "what_was_done decimal-only (no hex letter) caught"
rm -f "$F"

echo "== Test 22: check-handoff — anti-pattern lints, modes (--allow-pending), fresh-seed, block isolation =="
F="$(mktemp)"
good_handoff | sed 's/^next_steps:.*/next_steps: pick next from backlog/' > "$F"
"$BIN/check-handoff" --file "$F" >/dev/null 2>&1 && fail "'pick next from backlog' not caught" || pass "'pick next from backlog' caught"
rm -f "$F"

F="$(mktemp)"
good_handoff | sed 's/^gotchas:.*/gotchas: need to verify this later/' > "$F"
"$BIN/check-handoff" --file "$F" >/dev/null 2>&1 && fail "'need to verify' placeholder not caught" || pass "'need to verify' placeholder caught"
rm -f "$F"

F="$(mktemp)"
good_handoff | sed 's/^commit:.*/commit: pending/' > "$F"
"$BIN/check-handoff" --file "$F" >/dev/null 2>&1 && pass "commit: pending is accepted" || fail "commit: pending should be accepted"
rm -f "$F"

F="$(mktemp)"
good_handoff | sed 's/^session:.*/session: S1/' | grep -v '^predecessor_score:' > "$F"
"$BIN/check-handoff" --file "$F" >/dev/null 2>&1 && pass "Session-1 fixture without predecessor_score passes" || fail "Session-1 exemption not honored"
rm -f "$F"

F="$(mktemp)"
good_handoff | sed 's/^status:.*/status: pending/' > "$F"
"$BIN/check-handoff" --file "$F" >/dev/null 2>&1 && fail "status: pending should fail by default" || pass "status: pending fails by default"
"$BIN/check-handoff" --file "$F" --allow-pending >/dev/null 2>&1 && pass "status: pending passes with --allow-pending" || fail "--allow-pending did not accept status: pending"
rm -f "$F"

F="$(mktemp)"
good_handoff | sed 's/^status:.*/status: reconciled/' > "$F"
"$BIN/check-handoff" --file "$F" >/dev/null 2>&1 && pass "status: reconciled (Phase 0 backfill) is accepted" || fail "status: reconciled should be accepted"
rm -f "$F"

F="$(mktemp)"
cat > "$F" <<'EOF'
# Handoff Receipts

<!-- METHODOLOGY-SEED-SENTINEL: fresh receipt ledger, no receipts yet. -->

Receipts go below, newest on top.
EOF
"$BIN/check-handoff" --file "$F" >/dev/null 2>&1 && pass "fresh-seed fixture (sentinel, no blocks) passes" || fail "fresh-seed fixture should pass"
rm -f "$F"

# Block isolation: a prose line OUTSIDE the fenced block contains the exact
# anti-pattern text, and does not satisfy any field either — the real block below
# it is well-formed, so the outside noise must not affect the verdict either way.
F="$(mktemp)"
{
    echo 'NOTE: a bad example looks like "next_steps: pick next from backlog" - avoid it.'
    echo
    good_handoff
} > "$F"
"$BIN/check-handoff" --file "$F" >/dev/null 2>&1 && pass "prose outside the fenced block does not trigger the lint (block isolation)" || fail "block isolation: outside prose leaked into the check"
rm -f "$F"

echo "== Test 23: model-report — three sources stay visually/structurally separate (RED-first, Learning #12) =="
CL="$(mktemp)"
cat > "$CL" <<'EOF'
# Changelog

### 2026-01-01 · [ad hoc] entry with a Model bullet
- **Change:** something shipped
- **Commit/PR:** `abc1234`
- **Session:** S40 · **Verified:** n/a — fixture
- **Model:** Claude Sonnet 5

### 2026-01-02 · [ad hoc] entry with NO Model bullet
- **Change:** something else shipped
- **Commit/PR:** `def5678`
- **Session:** S41 · **Verified:** n/a — fixture
EOF

HO="$(mktemp)"
cat > "$HO" <<'EOF'
```handoff
session: S1
date: 2026-01-01
status: complete
self_score: 8
predecessor_score: 7
active_task: fixture
what_was_done: abc1234
next_steps: fixture
key_files: a.py:1
gotchas: fixture
runtime_smoke: n/a
changelog_ref: n/a
commit: abc1234
```
Hybrid model split: Sonnet 5 built P2/P4, Opus 4.8 did P3/P5/P6 and reviewed all Sonnet output.
EOF

OUT="$("$BIN/model-report" --changelog "$CL" --handoffs "$HO" --no-git 2>&1)"

PRIMARY_LN="$(echo "$OUT" | grep -n "PRIMARY" | head -1 | cut -d: -f1)"
SECONDARY_LN="$(echo "$OUT" | grep -n "SECONDARY" | head -1 | cut -d: -f1)"
SONNET_LN="$(echo "$OUT" | grep -n "Claude Sonnet 5" | head -1 | cut -d: -f1)"
HYBRID_LN="$(echo "$OUT" | grep -n "Hybrid model split" | head -1 | cut -d: -f1)"

if [ -n "$PRIMARY_LN" ] && [ -n "$SECONDARY_LN" ] && [ "$PRIMARY_LN" -lt "$SECONDARY_LN" ]; then
    pass "PRIMARY section header precedes SECONDARY section header"
else
    fail "section headers missing or out of order (PRIMARY=$PRIMARY_LN SECONDARY=$SECONDARY_LN)"
fi

if [ -n "$SONNET_LN" ] && [ -n "$PRIMARY_LN" ] && [ -n "$SECONDARY_LN" ] \
   && [ "$SONNET_LN" -gt "$PRIMARY_LN" ] && [ "$SONNET_LN" -lt "$SECONDARY_LN" ]; then
    pass "CHANGELOG Model value falls structurally within the PRIMARY section"
else
    fail "CHANGELOG Model value leaked out of the PRIMARY section (SONNET_LN=$SONNET_LN)"
fi

if [ -n "$HYBRID_LN" ] && [ -n "$SECONDARY_LN" ] && [ "$HYBRID_LN" -gt "$SECONDARY_LN" ]; then
    pass "HANDOFFS free-text mention falls structurally within the SECONDARY section"
else
    fail "HANDOFFS free-text mention leaked before/out of the SECONDARY section (HYBRID_LN=$HYBRID_LN)"
fi

echo "$OUT" | grep -q "S41" && fail "entry with no Model bullet was fabricated into the PRIMARY section" || pass "entry without a Model bullet correctly omitted from PRIMARY"

echo "$OUT" | grep -qi "never authoritative\|non-authoritative\|corroboration" && pass "corroboration/non-authoritative disclaimer present in output" || fail "no corroboration/non-authoritative disclaimer in output"

# Same fixture, but WITHOUT --no-git: exercises the real SOURCE 3 (git trailers)
# against this repo's actual commit history, since the plan's own completion
# criterion is "the THREE sources stay separate" -- a fixture that always
# passes --no-git never proves trailer data (source 3) stays out of 1/2.
OUT_GIT="$("$BIN/model-report" --changelog "$CL" --handoffs "$HO" 2>&1)"
CORRO_LN="$(echo "$OUT_GIT" | grep -n "CORROBORATION-ONLY" | head -1 | cut -d: -f1)"
SECONDARY_LN2="$(echo "$OUT_GIT" | grep -n "SECONDARY" | head -1 | cut -d: -f1)"
TRAILER_LN="$(echo "$OUT_GIT" | grep -n "noreply@anthropic.com" | head -1 | cut -d: -f1)"

if [ -n "$CORRO_LN" ] && [ -n "$SECONDARY_LN2" ] && [ "$CORRO_LN" -gt "$SECONDARY_LN2" ]; then
    pass "CORROBORATION-ONLY section header follows the SECONDARY section header"
else
    fail "CORROBORATION-ONLY header missing or out of order (SECONDARY=$SECONDARY_LN2 CORRO=$CORRO_LN)"
fi

if [ -n "$TRAILER_LN" ] && [ -n "$CORRO_LN" ] && [ "$TRAILER_LN" -gt "$CORRO_LN" ]; then
    pass "a real git Co-Authored-By trailer value falls structurally within the CORROBORATION-ONLY section"
else
    fail "no real trailer value found after the CORROBORATION-ONLY header (TRAILER_LN=$TRAILER_LN CORRO_LN=$CORRO_LN)"
fi

if [ -n "$SECONDARY_LN2" ]; then
    BEFORE_SECONDARY_TRAILERS="$(echo "$OUT_GIT" | head -n "$SECONDARY_LN2" | grep -c "noreply@anthropic.com")"
    [ "$BEFORE_SECONDARY_TRAILERS" = "0" ] && pass "no real trailer data leaked into the PRIMARY/SECONDARY sections" || fail "real trailer data leaked before the SECONDARY section"
else
    fail "SECONDARY header missing in git-enabled run, cannot check for trailer leakage"
fi

rm -f "$CL" "$HO"

echo "== Test 24: check-handoff — a Phase 1B stub validates against the stub schema (RED-first, Learning #12) =="
# WHY THIS TEST EXISTS. Tests 21-22 build every fixture from good_handoff(), a
# fully-populated `status: complete` receipt, and reach the pending path with
# `sed 's/^status:.*/status: pending/'`. That is a close-out receipt with one word
# changed — it is NOT a Phase 1B stub, so the --allow-pending assertion at :378 has
# been green since 1646773 while every real stub failed. The guard was proved; the
# FIXTURE never was. These three fixtures are the missing ones: each is a verbatim
# shape taken from the 21 stubs actually committed to this repo, and each is written
# out in full rather than sed-derived, so a fixture can never drift into a receipt.
#
# Stub schema (bin/check-handoff STUB_REQUIRED_KEYS): a block is a stub iff its OWN
# `status` is `pending` — dispatch is on the block, never on the flag. See N1.

# FLOOR-4 dialect: exactly the (session, date, active_task) triple SESSION_RUNNER.md:91
# names, plus status. 4 real stubs: da46b19 S8, 65b1e8e S15, 71ae4a1 S16, 9e93588 S3.
stub_floor() {
    cat <<'EOF'
```handoff
session: S15
date: 2026-07-25
status: pending
active_task: Layer 4 — dashboard self-scan false risk (issue #59)
```
Phase 1B claim stub — `status: pending`.
EOF
}

# FORK-11 dialect: all 13 keys minus the two scores. The 14-stub pre-change majority
# (S9-S14, S18-S20, S22-S26).
stub_fork() {
    cat <<'EOF'
```handoff
session: S25
date: 2026-08-01
status: pending
active_task: BL-9 Layer 2 — the action ledger size discipline
what_was_done: pending
next_steps: pending
key_files: CHANGELOG.md:45 (the ordering rule), bin/tests.sh:504
gotchas: The risk is outbound here, not inbound — sweep for links INSIDE frozen entries
runtime_smoke: pending
changelog_ref: pending
commit: pending
```
Phase 1B claim stub — `status: pending`.
EOF
}

# SENTINEL-13 dialect: all 13 keys, the two scores written `pending`. 3 real stubs,
# all authored by the framework's own maintainer: c3157e8 S5, a4e2b30 S7, 9c9c39c S8.
stub_sentinel() {
    cat <<'EOF'
```handoff
session: S7
date: 2026-08-01
status: pending
self_score: pending
predecessor_score: pending
active_task: File the upstream issue for the enumerable-set invariant gap
what_was_done: pending
next_steps: pending
key_files: bin/check-handoff:50 (REQUIRED_KEYS; newest-receipt-only scope is the gap)
gotchas: Numbered S7 — never renumber an already-written receipt
runtime_smoke: pending
changelog_ref: pending
commit: pending
```
Phase 1B claim stub — `status: pending`.
EOF
}

# Count findings from the checker's own `  error:` lines, never the "N issue(s)"
# headline — the headline is prose, the error lines are the structured rows.
# (Isolate the row from the advisory text before counting.)
nfind() { "$BIN/check-handoff" --file "$1" --allow-pending 2>&1 | grep -c '^  error:' || true; }

# --- C1: THE UNMUTATED-FIXTURE CONTROL (positive) ---------------------------
# All three real-shaped stubs must pass cleanly. This is the control Tests 21-22
# never had: if C1 ever goes red, the FIXTURE is broken, not the guard.
for d in floor fork sentinel; do
    F="$(mktemp)"; "stub_$d" > "$F"
    if "$BIN/check-handoff" --file "$F" --allow-pending >/dev/null 2>&1; then
        pass "C1 unmutated control: $d-dialect stub passes --allow-pending cleanly"
    else
        fail "C1 unmutated control: $d-dialect stub should pass (got $(nfind "$F") finding(s))"
    fi
    rm -f "$F"
done

# --- N1: THE KILLER TEST (flag-dispatch vs status-dispatch) -----------------
# The most likely wrong patch is `required = STUB if allow_pending else REQUIRED_KEYS`.
# Under it, a `status: complete` receipt one key short passes silently WITH the flag.
# Dispatching on the BLOCK's own status is what makes this fail correctly.
F="$(mktemp)"
good_handoff | grep -v '^gotchas:' > "$F"
"$BIN/check-handoff" --file "$F" --allow-pending >/dev/null 2>&1 \
    && fail "N1 flag-dispatch hole: a status:complete receipt missing gotchas passed WITH --allow-pending" \
    || pass "N1 status-dispatch: --allow-pending does not relax a status:complete receipt"
rm -f "$F"

# --- N2: blank is not absent ------------------------------------------------
# TWO keys, not one. B4 is a loop over all nine optional keys, so pinning it with a
# single representative would let the loop be narrowed to that one key while the suite
# stayed green — a plural claim resting on a sample of one. (Adversarial review caught
# exactly this: `if key not in required` narrowed to `if key == "key_files"` passed
# 31/31 while a blank `gotchas:` sailed through.)
for k in key_files gotchas; do
    F="$(mktemp)"
    stub_fork | sed "s/^$k:.*/$k: /" > "$F"
    "$BIN/check-handoff" --file "$F" --allow-pending >/dev/null 2>&1 \
        && fail "N2 blank bypass: a blanked optional key ($k) passed" \
        || pass "N2 blank optional key is a finding ($k) — omit the line instead"
    rm -f "$F"
done

# --- N3: the score sentinel must not leak onto the close-out path -----------
F="$(mktemp)"
good_handoff | sed 's/^self_score:.*/self_score: pending/' > "$F"
"$BIN/check-handoff" --file "$F" --allow-pending >/dev/null 2>&1 \
    && fail "N3 sentinel leak: self_score: pending accepted on a status:complete receipt" \
    || pass "N3 score sentinel is stub-scoped, not close-out-scoped"
rm -f "$F"

# --- N4: the sentinel is two named keys, not "any key" ----------------------
F="$(mktemp)"
stub_fork | sed 's#^key_files:.*#key_files: pending#' > "$F"
"$BIN/check-handoff" --file "$F" --allow-pending >/dev/null 2>&1 \
    && fail "N4 sentinel over-reach: key_files: pending satisfied the path:line check" \
    || pass "N4 score sentinel does not reach key_files"
rm -f "$F"

# --- N5/N6: present optional keys are validated at FULL strength ------------
F="$(mktemp)"
stub_sentinel | sed 's/^self_score:.*/self_score: 11/' > "$F"
"$BIN/check-handoff" --file "$F" --allow-pending >/dev/null 2>&1 \
    && fail "N5 range check skipped: self_score: 11 accepted in a stub" \
    || pass "N5 a non-sentinel score value still gets the 1..10 range check"
rm -f "$F"

F="$(mktemp)"
stub_fork | sed 's/^next_steps:.*/next_steps: pick next from backlog/' > "$F"
"$BIN/check-handoff" --file "$F" --allow-pending >/dev/null 2>&1 \
    && fail "N6 lint skipped: 'pick next from backlog' accepted in a stub" \
    || pass "N6 anti-pattern lints still fire inside a stub"
rm -f "$F"

# B2 covers FIVE value checks that can reach the nine optional keys; N4/N5/N6 pin three
# of them. These two pin the remaining pair — the what_was_done sha-shape check and the
# bare-placeholder sweep — so no check is correct-by-assumption in the stub branch.
F="$(mktemp)"
stub_fork | sed 's/^what_was_done:.*/what_was_done: refactored the parser/' > "$F"
"$BIN/check-handoff" --file "$F" --allow-pending >/dev/null 2>&1 \
    && fail "N6b sha-shape check skipped: sha-less what_was_done accepted in a stub" \
    || pass "N6b what_was_done still needs a sha or the literal pending inside a stub"
rm -f "$F"

F="$(mktemp)"
stub_fork | sed 's/^gotchas:.*/gotchas: TODO/' > "$F"
"$BIN/check-handoff" --file "$F" --allow-pending >/dev/null 2>&1 \
    && fail "N6c placeholder lint skipped: 'gotchas: TODO' accepted in a stub" \
    || pass "N6c bare-placeholder lint still fires inside a stub"
rm -f "$F"

# --- N7: the floor keys must carry real values ------------------------------
# Again TWO keys, for the same reason as N2: B5 loops over session/date/active_task, so
# one representative would let it be narrowed to that key alone. `status` is deliberately
# NOT tested here — `pending` is its mandated value and is the schema selector.
for k in active_task date; do
    F="$(mktemp)"
    stub_floor | sed "s/^$k:.*/$k: pending/" > "$F"
    "$BIN/check-handoff" --file "$F" --allow-pending >/dev/null 2>&1 \
        && fail "N7 floor value: $k: pending accepted at Phase 1B" \
        || pass "N7 floor key $k rejects the pending sentinel (knowable at claim time)"
    rm -f "$F"
done

# N7b: the converse — `status: pending` is REQUIRED, never a finding. Without this, a
# future session "fixing" B5 to cover all four floor keys would break every stub, and
# only the C1 control would say so.
F="$(mktemp)"
stub_floor > "$F"
"$BIN/check-handoff" --file "$F" --allow-pending >/dev/null 2>&1 \
    && pass "N7b status: pending is exempt from B5 — it is the schema selector" \
    || fail "N7b status: pending was itself flagged; B5 must exempt status"
rm -f "$F"

# --- N8: default mode still refuses a stub, with ONE honest finding ---------
# The flag gates exactly one finding and nothing else, so an unflagged stub still
# exits 1 — no schema relaxation can produce a false green.
F="$(mktemp)"
stub_fork > "$F"
"$BIN/check-handoff" --file "$F" >/dev/null 2>&1 \
    && fail "N8 a stub passed without --allow-pending" \
    || pass "N8 a stub still fails by default (the flag gates one finding, not the schema)"
N8="$("$BIN/check-handoff" --file "$F" 2>&1 | grep -c '^  error:' || true)"
[ "$N8" = "1" ] \
    && pass "N8 default mode yields exactly ONE finding, naming the real problem" \
    || fail "N8 default mode yielded $N8 findings, expected exactly 1"
rm -f "$F"

# --- C2/R4: the tool must stop advertising a capability, and --help must work -
HELP="$("$BIN/check-handoff" --help 2>&1)"
case "$HELP" in
    *--allow-pending*) pass "C2 presence control: --help renders and documents --allow-pending" ;;
    *)                 fail "C2 presence control: --help did not mention --allow-pending" ;;
esac
if printf '%s' "$HELP" | grep -qiE '1B|stub'; then
    fail "R4 --help still advertises the flag as a Phase 1B/stub checker"
else
    pass "R4 --help no longer claims the flag checks a Phase 1B stub"
fi

# --- R5: the stub schema is a strict subset of the close-out schema ---------
python3 - "$BIN/check-handoff" <<'PY' && pass "R5 STUB_REQUIRED_KEYS is a strict subset of the 13 REQUIRED_KEYS" || fail "R5 stub schema is not a strict subset of REQUIRED_KEYS"
import sys, importlib.machinery, importlib.util
sys.dont_write_bytecode = True
ldr = importlib.machinery.SourceFileLoader("ch", sys.argv[1])
spec = importlib.util.spec_from_loader("ch", ldr)
m = importlib.util.module_from_spec(spec); ldr.exec_module(m)
sub = set(m.STUB_REQUIRED_KEYS) < set(m.REQUIRED_KEYS)
sys.exit(0 if sub and len(m.REQUIRED_KEYS) == 13 and len(m.STUB_REQUIRED_KEYS) == 4 else 1)
PY

echo '== Test 25: check-handoff — the `commit:` answer-slot rule (BL-14, RED-first per Learning #12) =='
# WHY THIS TEST EXISTS. `commit:` may legitimately read `pending` when written — a
# close-out receipt ships INSIDE the commit whose sha it would name. The distributed
# spec (starter-kit/HANDOFFS.md:64, :78-79) then promises the NEXT session reconciles
# it. Nothing performed that promise: 9 of 32 receipts named no sha in the answer
# slot, one 25 days old, and this checker passed every one of them because it reads
# only blocks[0] and `pending` is not a BARE_PLACEHOLDER.
#
# RED-FIRST WAS RUN AGAINST THE REAL CORPUS, not a fixture: the new pass was executed
# against the pre-repair ledger at fd5d2d8 and returned exactly 9 findings — the same
# 9 derived independently by walking git history with the checker's own parser. That
# run is also what caught N5's hole (see below), which the fixtures alone would not
# have.
#
# THE RULE: the answer slot is the value's FIRST token, and on every receipt except
# the newest it must be a sha. Leading-token, not "contains" — see N7.

# Two-block ledger: newest on top, exactly as the real file is ordered.
two_block_ledger() {   # $1 = older block's commit: value
    cat <<EOF
\`\`\`handoff
session: S13
date: 2026-08-02
status: complete
self_score: 8
predecessor_score: 8
active_task: The newest receipt — exempt from the answer-slot rule by construction
what_was_done: Shipped the thing; commit b2c3d4e
next_steps: Reconcile the predecessor's commit: field at Phase 0
key_files: bin/check-handoff:1
gotchas: none
runtime_smoke: n/a — docs-only
changelog_ref: PR #99
commit: pending
\`\`\`
Prose for the newest receipt.

\`\`\`handoff
session: S12
date: 2026-08-01
status: complete
self_score: 8
predecessor_score: 7
active_task: The OLDER receipt — this one is governed by the rule
what_was_done: Did the earlier thing; commit a1b2c3d
next_steps: Something specific and actionable
key_files: bin/tests.sh:230
gotchas: none
runtime_smoke: n/a — docs-only
changelog_ref: PR #52
commit: $1
\`\`\`
Prose for the older receipt.
EOF
}

# Count only the structured finding rows, never the "N issue(s)" headline or the
# advisory note footer — the footer contains the phrase "answer slot" too, and
# grepping for it counted the advice as a finding on this test's first draft.
nslot() { "$BIN/check-handoff" --file "$1" ${2-} 2>&1 | grep -c '^  error: receipt'; }

# --- C1: THE UNMUTATED-FIXTURE CONTROL --------------------------------------
# The older receipt names a real sha. If C1 ever goes red, the FIXTURE is broken,
# not the guard.
F="$(mktemp)"; two_block_ledger 'a1b2c3d' > "$F"
if "$BIN/check-handoff" --file "$F" >/dev/null 2>&1; then
    pass "C1 unmutated control: older receipt naming a sha passes"
else
    fail "C1 unmutated control: should pass (got $(nslot "$F") finding(s))"
fi
rm -f "$F"

# --- N1: the `pending` dialect below the newest is caught -------------------
F="$(mktemp)"; two_block_ledger 'pending — reconciled at next Orient' > "$F"
[ "$(nslot "$F")" = "1" ] && pass "N1 older receipt with commit: pending is caught" \
    || fail "N1 older commit: pending not caught (got $(nslot "$F"))"
rm -f "$F"

# --- N2: the `this commit` dialect is caught (S25/S26 — names no sha at all) -
F="$(mktemp)"; two_block_ledger 'this commit — the split and this receipt ship together' > "$F"
[ "$(nslot "$F")" = "1" ] && pass "N2 older receipt with 'this commit' (no sha) is caught" \
    || fail "N2 'this commit' dialect not caught (got $(nslot "$F"))"
rm -f "$F"

# --- N3: THE KILLER TEST — the newest receipt is NEVER failed for pending ----
# C1/N1/N2 all carry `commit: pending` on the NEWEST block. If the exemption were
# value-based instead of positional, or if the rule ran over blocks[0], every one of
# them would fail — and the chicken-egg the ratified plan solved would be back. This
# also pins bin/tests.sh:366's long-standing "commit: pending is accepted" assertion
# at ledger scope rather than single-block scope.
F="$(mktemp)"; two_block_ledger 'a1b2c3d' > "$F"
if "$BIN/check-handoff" --file "$F" 2>&1 | grep -q 'S13'; then
    fail "N3 the NEWEST receipt was failed for commit: pending — chicken-egg re-created"
else
    pass "N3 newest receipt is exempt by construction (never failed for commit: pending)"
fi
rm -f "$F"

# --- N4: absence is not a pass ----------------------------------------------
# A rule that only reads PRESENT values makes deleting the line a free escape.
F="$(mktemp)"; two_block_ledger 'a1b2c3d' | sed '20,$ s/^commit: a1b2c3d$//' > "$F"
[ "$(nslot "$F")" = "1" ] && pass "N4 older receipt missing commit: entirely is caught" \
    || fail "N4 missing commit: key below the newest not caught (got $(nslot "$F"))"
rm -f "$F"

# --- N5: --archived removes the exemption (the hole RED-first found) --------
# "Newest" is a property of the LEDGER, not of a file. In a sharded ledger the
# archive's blocks[0] is merely the newest IN THAT SHARD. Without --archived the
# real S18 receipt passed for three days.
F="$(mktemp)"; two_block_ledger 'a1b2c3d' > "$F"     # newest block has commit: pending
[ "$(nslot "$F" --archived)" = "1" ] && pass "N5 --archived checks block 0 too (no unearned exemption)" \
    || fail "N5 --archived did not check the first block (got $(nslot "$F" --archived))"
[ "$(nslot "$F")" = "0" ] && pass "N5b without --archived the same file's block 0 stays exempt" \
    || fail "N5b exemption leaked away without --archived"
rm -f "$F"

# --- N6: the issue-#65 boundary — validate() is still blocks[0] ONLY --------
# The 13-key schema must NOT spread to older receipts. Upstream issue #65 proposes a
# separate `--all` mode over different ground; this is not that and must not become
# it by accident.
F="$(mktemp)"; two_block_ledger 'a1b2c3d' | sed '20,$ s/^gotchas: none$//' > "$F"
if "$BIN/check-handoff" --file "$F" 2>&1 | grep -q 'missing required key'; then
    fail "N6 the 13-key schema leaked onto an older receipt (issue #65 scope boundary crossed)"
else
    pass "N6 schema validation stays on blocks[0]; only the answer slot spans the ledger"
fi
rm -f "$F"

# --- N7: leading-token, not "contains" --------------------------------------
# `search` instead of `fullmatch` on the first token would accept any prose that
# merely CONTAINS a sha-shaped run — which every one of the 7 `pending` receipts did
# (they all cite their own claim-stub sha in the trailing prose).
F="$(mktemp)"; two_block_ledger 'pending — the prior claim commit is a1b2c3d' > "$F"
[ "$(nslot "$F")" = "1" ] && pass "N7 a sha in trailing prose does not satisfy the answer slot" \
    || fail "N7 trailing-prose sha wrongly satisfied the leading-token rule"
rm -f "$F"

# --- N8: a bare decimal is not a sha ----------------------------------------
F="$(mktemp)"; two_block_ledger '12345678' > "$F"
[ "$(nslot "$F")" = "1" ] && pass "N8 an all-decimal token is not accepted as a sha" \
    || fail "N8 all-decimal token wrongly accepted as a sha"
rm -f "$F"

# --- N9: fullmatch, not search — the token must BE a sha, not CONTAIN one ---
# N7 does not cover this and a mutation run proved it: N7's first token is plain
# `pending`, which contains no sha-shaped run, so search and fullmatch agree on it and
# the fullmatch->search mutant SURVIVED the whole suite. This fixture is the one that
# separates them — an em-dash bound directly to the sha with no space, one typo away
# from what S27's real receipt wrote. leads_with_sha() deliberately does not strip it.
F="$(mktemp)"; two_block_ledger 'pending—a1b2c3d' > "$F"
[ "$(nslot "$F")" = "1" ] && pass "N9 a token CONTAINING a sha does not satisfy the slot (fullmatch, not search)" \
    || fail "N9 fullmatch degraded to search — a token merely containing a sha was accepted"
rm -f "$F"

# --- N10: an unfinished stub below the newest is NOT double-reported --------
# A `status: pending` block below the newest means a session claimed and never closed
# out. That is the status finding's business and Phase 0 reconcile's remedy; reporting
# its empty answer slot here too would be noise pointing at the wrong repair. Pins the
# stub-skip guard, which no other assertion reaches.
F="$(mktemp)"
{ two_block_ledger 'a1b2c3d' | sed -n '1,17p'
  printf '\n```handoff\nsession: S11\ndate: 2026-07-31\nstatus: pending\nactive_task: Claimed and never closed out\n```\nProse.\n'
} > "$F"
[ "$(nslot "$F")" = "0" ] && pass "N10 an unfinished stub below the newest is not reported for its answer slot" \
    || fail "N10 stub below the newest was double-reported (got $(nslot "$F"))"
rm -f "$F"

# --- L1: THE LIVE-CORPUS ASSERTION ------------------------------------------
# Every other check-handoff assertion in this file runs against a mktemp fixture, so
# nothing observes the REAL ledger. This is the half of Learning #9 the `commit:`
# field never had: it trips on the next `bash bin/tests.sh` rather than waiting for
# someone to remember. Precedent: Test 10 runs check-links bare against the real tree.
# If this goes red, the ledger drifted — reconcile it, do not weaken the test.
# SCOPE-ISOLATED ON PURPOSE — count answer-slot ROWS, never the process exit status.
# As first written these two assertions keyed on the exit code, which is 1 if ANY of the
# tool's three passes finds anything. The moment Test 26's locator pass was added, both
# went red against a ledger whose `commit:` fields were all correct, reporting "an
# unreconciled commit: answer slot" for a defect in a different field. An exit code is a
# union; these assertions are about one member of it. Same reason nslot() exists at all.
LEDGER="$(cd "$BIN/.." && pwd)"
if [ -f "$LEDGER/HANDOFFS.md" ]; then
    if [ "$(nslot "$LEDGER/HANDOFFS.md" --allow-pending)" = "0" ]; then
        pass "L1 live ledger: every receipt below the newest names a commit sha"
    else
        "$BIN/check-handoff" --file "$LEDGER/HANDOFFS.md" --allow-pending 2>&1 | sed 's/^/    /'
        fail "L1 live ledger has an unreconciled commit: answer slot (see above)"
    fi
else
    pass "L1 skipped: no root HANDOFFS.md (adopter tree or fresh clone)"
fi
if [ -f "$LEDGER/docs/archive/HANDOFFS-archive.md" ]; then
    if [ "$(nslot "$LEDGER/docs/archive/HANDOFFS-archive.md" --archived)" = "0" ]; then
        pass "L1b archived ledger shard: every receipt names a commit sha"
    else
        "$BIN/check-handoff" --file "$LEDGER/docs/archive/HANDOFFS-archive.md" --archived 2>&1 | sed 's/^/    /'
        fail "L1b archived ledger shard has an unreconciled commit: answer slot (see above)"
    fi
else
    pass "L1b skipped: no archived ledger shard"
fi

# --- R6: --help documents --archived ----------------------------------------
case "$("$BIN/check-handoff" --help 2>&1)" in
    *--archived*) pass "R6 --help documents --archived" ;;
    *)            fail "R6 --help does not mention --archived" ;;
esac

echo ''
echo '== Test 26: check-handoff — the `changelog_ref` locator-form rule (BL-15, RED-first) =='
# WHY THIS TEST EXISTS. BL-15 alleged `changelog_ref` carried BL-14's escape. It does
# carry the deictic-deferral population BL-15 counted — 13 of 32, "this commit" x12 plus
# archive-S1's "this branch" — but all 13 name their entry by a quoted ### title BEFORE
# the deferral, and since 7752114 all 13 carry a real sha in their own `commit:`. The
# deferral is a resolvable back-reference, not an escape. What the measurement DID find
# is a different defect: 9 root-relative `CHANGELOG.md:<N>` anchors in 8 receipts, 8 of
# them correct the day they were written and 0 of 9 resolving to their stated referent
# afterwards. Four land in front matter above every entry; four land inside an entry
# written on a later day.
#
# RED-FIRST WAS RUN AGAINST THE REAL CORPUS, not a fixture: executed against the
# unrepaired ledger the new pass returned exactly 9 findings — the same 9 derived
# independently by walking git history — and 0 against the archive shard, measured
# rather than assumed.
#
# THE RULE is a PROHIBITION, not a resolution check. Its truth value depends only on the
# receipt's own bytes, so no later prepend, retitle or archive split can turn a passing
# receipt red. The rejected alternative — assert each reference RESOLVES to a real ###
# heading — goes red whenever someone legitimately retitles a ledger entry, which this
# repo does to correct false claims (de46858). NO blocks[0] exemption: unlike `commit:`
# there is no chicken-egg, so the prohibition is satisfiable the instant it is written.

# One receipt, one changelog_ref value. Newest-position by default so the absence of a
# blocks[0] exemption is what every positive assertion below actually exercises.
one_ref_ledger() {   # $1 = changelog_ref value
    cat <<EOF
\`\`\`handoff
session: S31
date: 2026-08-02
status: complete
self_score: 8
predecessor_score: 8
active_task: Sole receipt — newest by position, and NOT exempt from this rule
what_was_done: Shipped the thing; commit b2c3d4e
next_steps: Something specific and actionable
key_files: bin/check-handoff:1
gotchas: none
runtime_smoke: n/a — docs-only
changelog_ref: $1
commit: a1b2c3d
\`\`\`
Prose.
EOF
}

# Count ONLY locator rows. Deliberately not `^  error: receipt` — that is nslot()'s
# prefix, and a row starting that way would be absorbed into Test 25's assertions
# instead of this one's. The checker's message begins "changelog_ref in receipt" for
# exactly this reason.
nloc() { "$BIN/check-handoff" --file "$1" ${2-} 2>&1 | grep -c '^  error: changelog_ref'; }

# --- C0: THE UNMUTATED-FIXTURE CONTROL --------------------------------------
# The house form: name the entry by its quoted heading. If C0 goes red the FIXTURE is
# broken, not the guard. Broken once by hand and watched to fail before being trusted.
F="$(mktemp)"; one_ref_ledger 'CHANGELOG.md "2026-08-02 · [BL-15] The locator-form rule"' > "$F"
if "$BIN/check-handoff" --file "$F" >/dev/null 2>&1; then
    pass "C0 unmutated control: a quoted-heading changelog_ref passes"
else
    "$BIN/check-handoff" --file "$F" 2>&1 | sed 's/^/    /'
    fail "C0 unmutated control went red — the fixture is broken, not the guard"
fi
rm -f "$F"

# --- C1/C2/C3: FALSE-POSITIVE CONTROLS, all three measured in the corpus -----
# The two prescribed seed forms (starter-kit/HANDOFFS.md:63) must stay legal, or the
# rule would fail the very form the distributed spec asks adopters to write.
F="$(mktemp)"; one_ref_ledger 'PR #52' > "$F"
[ "$(nloc "$F")" = "0" ] && pass "C1 the seed's own 'PR #N' form is not a finding" \
    || fail "C1 'PR #52' was flagged — the rule contradicts starter-kit/HANDOFFS.md:63"
rm -f "$F"

# A distributed TEMPLATE is stable: it is not prepended to and its front matter is not
# rewritten per session. 16 such prefixed citations exist across the live corpus.
F="$(mktemp)"; one_ref_ledger 'the rule at starter-kit/CHANGELOG.md:92, entry "Foo"' > "$F"
[ "$(nloc "$F")" = "0" ] && pass "C2 a starter-kit/ template line cite is not a finding" \
    || fail "C2 prefix-awareness lost — starter-kit/CHANGELOG.md:92 was flagged"
rm -f "$F"

# An archived shard is frozen at write, so a line number into it cannot decay.
F="$(mktemp)"; one_ref_ledger 'docs/archive/CHANGELOG-through-v3.6.md:46 "Foo"' > "$F"
[ "$(nloc "$F")" = "0" ] && pass "C3 a frozen archive shard line cite is not a finding" \
    || fail "C3 prefix-awareness lost — an archived-shard anchor was flagged"
rm -f "$F"

# --- N1: the defect itself, on the NEWEST receipt ---------------------------
# The whole point of having no blocks[0] exemption. If the answer-slot rule's positional
# skip were copied here, this returns 0 and the rule guards nothing at the head of the file.
F="$(mktemp)"; one_ref_ledger 'CHANGELOG.md:68 "2026-08-01 · [BL-9] Layer 2"' > "$F"
[ "$(nloc "$F")" = "1" ] && pass "N1 a root CHANGELOG.md:<N> anchor is caught on the NEWEST receipt" \
    || fail "N1 root anchor not caught on blocks[0] (got $(nloc "$F")) — exemption wrongly copied"
rm -f "$F"

# --- N2: an anchor in TRAILING prose, not the leading token ------------------
# S28's second anchor is exactly this shape, and it is the one anchor in the corpus that
# was wrong the day it was written. A leading-token predicate (the answer-slot rule's
# shape) would miss it entirely.
F="$(mktemp)"; one_ref_ledger 'CHANGELOG.md "Some entry"; the repair entry is CHANGELOG.md:118' > "$F"
[ "$(nloc "$F")" = "1" ] && pass "N2 an anchor in trailing prose is caught (not a leading-token rule)" \
    || fail "N2 trailing-prose anchor missed (got $(nloc "$F"))"
rm -f "$F"

# --- N3: HANDOFFS.md is a live ledger too ------------------------------------
F="$(mktemp)"; one_ref_ledger 'CHANGELOG.md "Entry"; see HANDOFFS.md:8 for the count' > "$F"
[ "$(nloc "$F")" = "1" ] && pass "N3 a root HANDOFFS.md:<N> anchor is caught, not only CHANGELOG" \
    || fail "N3 root HANDOFFS.md anchor missed (got $(nloc "$F"))"
rm -f "$F"

# --- N4: one finding PER ANCHOR, so the count equals the repair size ---------
# S28 carries two. A per-receipt count would understate every multi-anchor repair.
F="$(mktemp)"; one_ref_ledger 'CHANGELOG.md:70 "A"; the repair entry is CHANGELOG.md:118' > "$F"
[ "$(nloc "$F")" = "2" ] && pass "N4 two anchors in one value yield two findings (per anchor, not per receipt)" \
    || fail "N4 expected 2 findings for a two-anchor value (got $(nloc "$F"))"
rm -f "$F"

# --- N5: a bare filename mention, with no line number, stays legal -----------
# This is what the repair turns every flagged value INTO, so if it were a finding the
# repair could not converge.
F="$(mktemp)"; one_ref_ledger 'CHANGELOG.md "2026-08-01 · [BL-9] Layer 2", commit 3aee4e3' > "$F"
[ "$(nloc "$F")" = "0" ] && pass "N5 a filename with no :<N> is legal (the repaired form converges)" \
    || fail "N5 the repaired form was itself flagged (got $(nloc "$F")) — the rule cannot converge"
rm -f "$F"

# --- N6: an older receipt is checked too ------------------------------------
# Complements N1: the rule spans the ledger, so neither end is exempt.
F="$(mktemp)"
{ one_ref_ledger 'CHANGELOG.md "Newest entry"'
  cat <<'EOS'

```handoff
session: S30
date: 2026-08-01
status: complete
self_score: 8
predecessor_score: 8
active_task: The OLDER receipt — clean newest above it, so only this one can fire
what_was_done: Did the earlier thing; commit a1b2c3d
next_steps: Something specific and actionable
key_files: bin/tests.sh:1
gotchas: none
runtime_smoke: n/a — docs-only
changelog_ref: CHANGELOG.md:35 "Older entry"
commit: a1b2c3d
```
Prose for the older receipt.
EOS
} > "$F"
[ "$(nloc "$F")" = "1" ] && pass "N6 an older receipt's anchor is caught (the rule spans the ledger)" \
    || fail "N6 older-receipt anchor missed (got $(nloc "$F"))"
rm -f "$F"

# --- N7: a Phase 1B stub is skipped whole -----------------------------------
# changelog_ref is not in STUB_REQUIRED_KEYS; a stub that carries one anyway is not this
# pass's business, and reporting it would fire during every session's own claim commit.
F="$(mktemp)"
cat > "$F" <<'EOS'
```handoff
session: S32
date: 2026-08-02
status: pending
active_task: Claimed, not closed out
changelog_ref: CHANGELOG.md:68 "not yet real"
```
Prose.
EOS
[ "$(nloc "$F")" = "0" ] && pass "N7 a status: pending stub is skipped whole" \
    || fail "N7 a Phase 1B stub was flagged (got $(nloc "$F"))"
rm -f "$F"

# --- N8: an empty value is validate()'s finding, not this pass's ------------
# Pins the BEHAVIOUR, and deliberately not a guard: the checker has no empty-value skip,
# because an empty string contains no anchor, so no mutant could falsify one. Written
# this way so nobody adds an unkillable line later believing this test covers it.
F="$(mktemp)"; one_ref_ledger '' > "$F"
[ "$(nloc "$F")" = "0" ] && pass "N8 an empty changelog_ref is not double-reported here" \
    || fail "N8 empty value double-reported as a locator finding (got $(nloc "$F"))"
rm -f "$F"

# --- N9: a time, a ratio, and a URL are not ledger anchors ------------------
# The naive `path:digits` shape matches all three; requiring the CHANGELOG/HANDOFFS stem
# plus `.md` is what keeps them out.
F="$(mktemp)"
one_ref_ledger 'CHANGELOG.md "Entry"; written 18:24, ratio 3:1, https://github.com/KJ5HST/methodology/pull/63' > "$F"
[ "$(nloc "$F")" = "0" ] && pass "N9 a time, a ratio and a URL are not ledger anchors" \
    || fail "N9 false positive on non-anchor colon-digit text (got $(nloc "$F"))"
rm -f "$F"

# --- L2: THE LIVE-CORPUS ASSERTIONS -----------------------------------------
# Same role as Test 25's L1: every assertion above runs on a mktemp fixture, so nothing
# observes the REAL ledger. If these go red the ledger drifted — repair it, do not
# weaken the test. --allow-pending so an in-flight Phase 1B stub is not the finding.
if [ -f "$LEDGER/HANDOFFS.md" ]; then
    if [ "$(nloc "$LEDGER/HANDOFFS.md" --allow-pending)" = "0" ]; then
        pass "L2 live ledger: no changelog_ref addresses a live ledger by line number"
    else
        "$BIN/check-handoff" --file "$LEDGER/HANDOFFS.md" --allow-pending 2>&1 | sed 's/^/    /'
        fail "L2 live ledger carries a positional ledger address (see above)"
    fi
else
    pass "L2 skipped: no root HANDOFFS.md (adopter tree or fresh clone)"
fi
if [ -f "$LEDGER/docs/archive/HANDOFFS-archive.md" ]; then
    if [ "$(nloc "$LEDGER/docs/archive/HANDOFFS-archive.md" --archived)" = "0" ]; then
        pass "L2b archived ledger shard: no positional ledger address"
    else
        "$BIN/check-handoff" --file "$LEDGER/docs/archive/HANDOFFS-archive.md" --archived 2>&1 | sed 's/^/    /'
        fail "L2b archived ledger shard carries a positional ledger address (see above)"
    fi
else
    pass "L2b skipped: no archived ledger shard"
fi

echo ""
echo "== Test 27: .githooks/pre-commit — the Phase 1B claim carve-out (RED-first, S32) =="
# The FM #27 gate refused the one commit the methodology REQUIRES: the Phase 1B claim,
# which by definition has no action to log yet. Measured message-independently and FROZEN
# AT c000a90, the pre-change tree — 32 commits stage HANDOFFS.md and nothing else, 26 of
# them claims, all 32 postdating the hook (dc8aa76), every claim shipped with --no-verify.
# Those two figures are historical and do not move; the live ones are re-derived by the
# replay below and printed by 27.L1a/27.L1b/27.L1c, which is why they read higher here.
# The carve-out is deliberately NARROWER than "a HANDOFFS.md commit": 6 of those 32 are
# not claims — 2 close-out receipts committed alone and 4 later repairs of an older
# receipt — and a path-only exemption would have waved through exactly what FM #27 exists
# to catch. Every assertion below is therefore about the staged DIFF, not the path.

# HOOKS_DIR/HOOK are variables, not constants: the mutation section at the bottom points
# them at a scratch COPY so that no mutant is ever written into the tracked file. Two suite
# runs overlapped during development and one mutant leaked into the other run — with the
# copy there is nothing to leak.
HOOKS_DIR="$METHODOLOGY/.githooks"
HOOK="$HOOKS_DIR/pre-commit"
REAL_HOOK_CKSUM="$(cksum < "$HOOK")"
[ -x "$HOOK" ] && pass "27.0 the hook is executable" || fail "27.0 the hook lost its exec bit"

# A claim stub and a close-out receipt are written as DISTINCT LITERALS, never by mutating
# one into the other. A receipt sed'd to `status: pending` is not a Phase 1B stub, and a
# fixture built that way would make the assertions below green for the wrong reason.
handoff_claim() {     # $1 = session — the shape every real claim commit has
    printf '```handoff\nsession: %s\ndate: 2026-08-03\nstatus: pending\nactive_task: Do the one thing\n```\n\n' "$1"
}
handoff_receipt() {   # $1 = session — the shape of a Phase 3D close-out receipt
    printf '```handoff\nsession: %s\ndate: 2026-08-03\nstatus: complete\nself_score: 8\npredecessor_score: 9\nactive_task: Did the one thing\ncommit: pending\n```\n\n' "$1"
}

mk_hookrepo() {
    local dir; dir="$(mktemp -d)"
    git -C "$dir" init -q
    git -C "$dir" config user.email t@t
    git -C "$dir" config user.name t
    git -C "$dir" config core.hooksPath "$HOOKS_DIR"
    printf '# Changelog\n' > "$dir/CHANGELOG.md"
    handoff_receipt S1 > "$dir/HANDOFFS.md"
    printf '# Session notes\n' > "$dir/SESSION_NOTES.md"
    printf '# Readme\n' > "$dir/README.md"
    git -C "$dir" add -A
    git -C "$dir" commit -q --no-verify -m baseline
    echo "$dir"
}

# Runs the hook the way git runs it — from the repo root, against the staged index — and
# reports WHY, not just whether. A shell error inside the carve-out also exits non-zero, so
# without this a crashed hook would read as "correctly refused" in every negative case.
hook_verdict() {   # $1 = repo -> "pass" | "refuse" | "crash:<rc>:<first line>"
    local out rc
    out="$(cd "$1" && "$HOOK" 2>&1)"; rc=$?
    if [ "$rc" = "0" ]; then echo "pass"
    elif printf '%s' "$out" | grep -q 'failure mode #27'; then echo "refuse"
    else echo "crash:$rc:$(printf '%s' "$out" | head -1)"; fi
}

# --- C0: THE UNMUTATED-FIXTURE CONTROLS -------------------------------------
# If the gate is not live in the fixture, every "passes" below is vacuous. Broken once by
# hand (hooksPath unset) and watched to go green — which is precisely the failure this
# control exists to catch.
P="$(mk_hookrepo)"
printf '# Readme\nedited\n' > "$P/README.md"; git -C "$P" add README.md
[ "$(hook_verdict "$P")" = "refuse" ] && pass "27.C0 control: an ordinary single-file commit is still refused" \
    || fail "27.C0 control went red/green wrongly ($(hook_verdict "$P")) — the fixture cannot prove anything"
# ...and git really invokes THIS hook through core.hooksPath, not some other one. The refusal
# MESSAGE is asserted, not just the non-zero exit: a crashing hook also fails the commit, and
# this is the one assertion in Test 27 that does not route through hook_verdict.
C0B_OUT="$(git -C "$P" commit -m "probe" 2>&1)"; C0B_RC=$?
if [ "$C0B_RC" = "0" ]; then
    fail "27.C0b git committed a ledger-less change — the hook was never invoked"
elif printf '%s' "$C0B_OUT" | grep -q 'failure mode #27'; then
    pass "27.C0b git invokes the hook through core.hooksPath (real commit refused, FM #27)"
else
    fail "27.C0b the commit failed without the FM #27 message — the hook crashed: $(printf '%s' "$C0B_OUT" | head -1)"
fi
rm -rf "$P"

# --- N1: THE TWO-POINT TEST, positive end -----------------------------------
# A claim commit staging only HANDOFFS.md passes. Asserted through a REAL `git commit`,
# because that is the operation 26 sessions had to bypass.
P="$(mk_hookrepo)"
{ handoff_claim S2; cat "$P/HANDOFFS.md"; } > "$P/H.tmp" && mv "$P/H.tmp" "$P/HANDOFFS.md"
git -C "$P" add HANDOFFS.md
[ "$(hook_verdict "$P")" = "pass" ] && pass "27.N1 a Phase 1B claim staging only HANDOFFS.md passes" \
    || fail "27.N1 the claim carve-out did not fire ($(hook_verdict "$P"))"
if git -C "$P" commit -q -m "claim S2" 2>/dev/null; then
    pass "27.N1b the same claim commits for real, with no --no-verify"
else
    fail "27.N1b a real claim commit still needs --no-verify — the bypass is not removed"
fi
rm -rf "$P"

# --- N2: SESSION_NOTES.md may ride along ------------------------------------
# Distributed Phase 1B (starter-kit/SESSION_RUNNER.md §1B) tells every adopter to write the
# SESSION_NOTES.md stub and "commit it with this claim", and SESSION_NOTES.md is a
# DISTRIBUTION seed. A HANDOFFS-only carve-out would fix this repo and leave every adopter's
# prescribed claim shape refused.
P="$(mk_hookrepo)"
{ handoff_claim S2; cat "$P/HANDOFFS.md"; } > "$P/H.tmp" && mv "$P/H.tmp" "$P/HANDOFFS.md"
printf '# Session notes\n### What Session 2 Did\n' > "$P/SESSION_NOTES.md"
git -C "$P" add HANDOFFS.md SESSION_NOTES.md
[ "$(hook_verdict "$P")" = "pass" ] && pass "27.N2 a claim co-staging SESSION_NOTES.md passes (the adopter shape)" \
    || fail "27.N2 the prescribed adopter claim shape was refused ($(hook_verdict "$P"))"
rm -rf "$P"

# --- N3: SESSION_NOTES.md alone is not a claim ------------------------------
# There is no receipt in the diff, so there is no claim signature to read.
P="$(mk_hookrepo)"
printf '# Session notes\nedited\n' > "$P/SESSION_NOTES.md"; git -C "$P" add SESSION_NOTES.md
[ "$(hook_verdict "$P")" = "refuse" ] && pass "27.N3 SESSION_NOTES.md alone is refused (no receipt, no claim)" \
    || fail "27.N3 SESSION_NOTES.md alone slipped through ($(hook_verdict "$P"))"
rm -rf "$P"

# --- N4: THE KILLER TEST — a close-out receipt committed alone --------------
# f2d013b and 21fb521 are exactly this, and a path-only carve-out exempts them. This is the
# commit FM #27 was written for: work landed, and the ledger says nothing.
P="$(mk_hookrepo)"
{ handoff_receipt S2; cat "$P/HANDOFFS.md"; } > "$P/H.tmp" && mv "$P/H.tmp" "$P/HANDOFFS.md"
git -C "$P" add HANDOFFS.md
[ "$(hook_verdict "$P")" = "refuse" ] && pass "27.N4 a close-out receipt committed alone is STILL refused" \
    || fail "27.N4 a close-out receipt was exempted ($(hook_verdict "$P")) — the carve-out is path-only"
rm -rf "$P"

# --- N5: a claim bundled with a close-out is not a claim --------------------
# Every added `status:` line must read `pending`; one `complete` in the same diff means an
# action landed in this commit.
P="$(mk_hookrepo)"
{ handoff_claim S3; handoff_receipt S2; cat "$P/HANDOFFS.md"; } > "$P/H.tmp" && mv "$P/H.tmp" "$P/HANDOFFS.md"
git -C "$P" add HANDOFFS.md
[ "$(hook_verdict "$P")" = "refuse" ] && pass "27.N5 a claim bundled with a close-out is refused" \
    || fail "27.N5 bundling a close-out into a claim commit slipped through ($(hook_verdict "$P"))"
rm -rf "$P"

# --- N6: a prose edit to HANDOFFS.md is an action ---------------------------
# The archive front matter, the receipt-count line, the ledger doctrine — all live in this
# file and all are actions. Only the claim is exempt.
P="$(mk_hookrepo)"
printf 'Front matter edited by hand.\n' >> "$P/HANDOFFS.md"; git -C "$P" add HANDOFFS.md
[ "$(hook_verdict "$P")" = "refuse" ] && pass "27.N6 a prose edit to HANDOFFS.md is refused" \
    || fail "27.N6 a prose edit was exempted ($(hook_verdict "$P"))"
rm -rf "$P"

# --- N7: a status flipped in place adds no block ----------------------------
# `+status: pending` alone is not a claim: this diff adds that exact line while adding no
# receipt. Without the fence conjunct the carve-out would accept it (mutant M1).
P="$(mk_hookrepo)"
sed 's/^status: complete$/status: pending/' "$P/HANDOFFS.md" > "$P/H.tmp" && mv "$P/H.tmp" "$P/HANDOFFS.md"
git -C "$P" add HANDOFFS.md
[ "$(hook_verdict "$P")" = "refuse" ] && pass "27.N7 flipping an existing receipt to pending is refused (no block added)" \
    || fail "27.N7 an in-place status flip was read as a claim ($(hook_verdict "$P"))"
rm -rf "$P"

# --- N8: THE TWO-POINT TEST, negative end -----------------------------------
# A claim is a claim only when nothing else rides with it.
P="$(mk_hookrepo)"
{ handoff_claim S2; cat "$P/HANDOFFS.md"; } > "$P/H.tmp" && mv "$P/H.tmp" "$P/HANDOFFS.md"
printf '# Readme\nedited\n' > "$P/README.md"
git -C "$P" add HANDOFFS.md README.md
[ "$(hook_verdict "$P")" = "refuse" ] && pass "27.N8 a claim carrying a third file is refused" \
    || fail "27.N8 a claim smuggled a source file past the gate ($(hook_verdict "$P"))"
rm -rf "$P"

# --- N9: the main path is untouched -----------------------------------------
P="$(mk_hookrepo)"
{ handoff_claim S2; cat "$P/HANDOFFS.md"; } > "$P/H.tmp" && mv "$P/H.tmp" "$P/HANDOFFS.md"
printf '# Changelog\n### 2026-08-03 · [ad hoc] Something\n' > "$P/CHANGELOG.md"
git -C "$P" add HANDOFFS.md CHANGELOG.md
[ "$(hook_verdict "$P")" = "pass" ] && pass "27.N9 CHANGELOG.md co-staged still passes (main path unchanged)" \
    || fail "27.N9 the carve-out broke the main co-staging path ($(hook_verdict "$P"))"
rm -rf "$P"

# --- N10: the first session, where HANDOFFS.md is created by the claim ------
P="$(mk_hookrepo)"
git -C "$P" rm -q --cached HANDOFFS.md >/dev/null; rm -f "$P/HANDOFFS.md"
git -C "$P" commit -q --no-verify -m "remove receipts ledger"
handoff_claim S2 > "$P/HANDOFFS.md"; git -C "$P" add HANDOFFS.md
[ "$(hook_verdict "$P")" = "pass" ] && pass "27.N10 a claim that CREATES HANDOFFS.md passes (adopter session 1)" \
    || fail "27.N10 the first-ever claim was refused ($(hook_verdict "$P"))"
rm -rf "$P"

# --- N11: a fence with no status line is not a claim ------------------------
# HANDOFFS.md's own front matter documents the block format, so a ```handoff fence can be
# added as an EXAMPLE. Without the `pending > 0` conjunct the counts would read 0 == 0 and
# the carve-out would fire on it (mutant M7).
P="$(mk_hookrepo)"
printf '\nBlock format:\n\n```handoff\nsession: S<N>\n```\n' >> "$P/HANDOFFS.md"
git -C "$P" add HANDOFFS.md
[ "$(hook_verdict "$P")" = "refuse" ] && pass '27.N11 a handoff fence with no status line is refused' \
    || fail "27.N11 an example block was read as a claim ($(hook_verdict "$P"))"
rm -rf "$P"

# --- N12: the measured WIDTH of the exemption, asserted rather than assumed --
# Measured over all 27 real claims, not sampled — an earlier draft of this comment said "2",
# which was two commits noticed rather than a population counted. ALL 27 add lines outside
# the new block (separator, blanks, the prescribed annotation line) and 5 also DELETE one:
# four bump the front matter's receipt count, and 63316ca reconciles a predecessor's
# `commit:` field. So a claim commit may carry other HANDOFFS.md edits past the FM #27 gate
# with it — the honest width of this exemption. Narrowing to "only the receipt block" would
# refuse 27 of 27 and turn 27.L1b red against real history, which is the signal that the
# tighter rule is wrong for this repo, not that the history is.
P="$(mk_hookrepo)"
{ handoff_claim S2; cat "$P/HANDOFFS.md"; } > "$P/H.tmp" && mv "$P/H.tmp" "$P/HANDOFFS.md"
printf 'This file currently holds 2 receipts.\n' >> "$P/HANDOFFS.md"
git -C "$P" add HANDOFFS.md
[ "$(hook_verdict "$P")" = "pass" ] && pass "27.N12 a claim carrying an incidental HANDOFFS.md edit passes (74479df's shape)" \
    || fail "27.N12 a real historical claim shape was refused ($(hook_verdict "$P"))"
rm -rf "$P"

# --- N13: the rename escape (found by adversarial review, not by design) -----
# `git diff --cached --name-only` collapses a rename to its DESTINATION path, so before
# `--no-renames` was added to the staged-set query, `git mv <tracked source> SESSION_NOTES.md`
# read as the two exempt paths and deleted a tracked file with no ledger line. The carve-out
# is what made that reachable — the pre-change hook refused every commit without CHANGELOG.md.
P="$(mk_hookrepo)"
git -C "$P" rm -q SESSION_NOTES.md >/dev/null
printf 'def real_code():\n    return 1\n' > "$P/src.py"
git -C "$P" add -A >/dev/null; git -C "$P" commit -q --no-verify -m "drop notes, add source"
git -C "$P" mv src.py SESSION_NOTES.md
{ handoff_claim S2; cat "$P/HANDOFFS.md"; } > "$P/H.tmp" && mv "$P/H.tmp" "$P/HANDOFFS.md"
git -C "$P" add HANDOFFS.md
[ "$(hook_verdict "$P")" = "refuse" ] && pass "27.N13 a claim smuggling a renamed source file is refused" \
    || fail "27.N13 a tracked source file left the repo through the carve-out ($(hook_verdict "$P"))"
rm -rf "$P"

# --- N14: a documentation example is not a receipt ---------------------------
# HANDOFFS.md's front matter documents the block format, so a ```handoff fence WITH a
# `status: pending` line can be added while filing no receipt at all. `bin/check-handoff`'s
# extract_blocks already skips a block inside a stronger wrapper for exactly this reason;
# the hook approximates the same rule line-wise. N11 (no status line) misses this by one line.
P="$(mk_hookrepo)"
printf '\nBlock format:\n\n````\n```handoff\nsession: S<N>\nstatus: pending\n```\n````\n' >> "$P/HANDOFFS.md"
git -C "$P" add HANDOFFS.md
[ "$(hook_verdict "$P")" = "refuse" ] && pass "27.N14 a fenced documentation example is refused (no receipt filed)" \
    || fail "27.N14 a documentation example was read as a claim ($(hook_verdict "$P"))"
rm -rf "$P"

# --- N15/N16: the diff is read as DATA, not as the committer's presentation ---
# `diff.external` (difftastic's documented global setup) and `color.ui = always` both replace
# or decorate the diff body, so `grep '^+'` matches nothing and a textbook claim is refused.
# It fails CLOSED — no gate is weakened — but it silently reinstates the --no-verify reflex
# this carve-out exists to remove, and only for people whose tooling is configured.
P="$(mk_hookrepo)"
printf '#!/bin/sh\necho EXT\n' > "$P/ext.sh"; chmod +x "$P/ext.sh"
git -C "$P" config diff.external "$P/ext.sh"
{ handoff_claim S2; cat "$P/HANDOFFS.md"; } > "$P/H.tmp" && mv "$P/H.tmp" "$P/HANDOFFS.md"
git -C "$P" add HANDOFFS.md
[ "$(hook_verdict "$P")" = "pass" ] && pass "27.N15 a claim still passes under diff.external (difftastic)" \
    || fail "27.N15 diff.external defeated the carve-out ($(hook_verdict "$P"))"
rm -rf "$P"

P="$(mk_hookrepo)"
git -C "$P" config color.ui always
{ handoff_claim S2; cat "$P/HANDOFFS.md"; } > "$P/H.tmp" && mv "$P/H.tmp" "$P/HANDOFFS.md"
git -C "$P" add HANDOFFS.md
[ "$(hook_verdict "$P")" = "pass" ] && pass "27.N16 a claim still passes under color.ui = always" \
    || fail "27.N16 colourised diff output defeated the carve-out ($(hook_verdict "$P"))"
rm -rf "$P"

# --- L1: THE CORPUS REPLAY --------------------------------------------------
# Every real single-file HANDOFFS.md commit in this repo's history, replayed against the
# hook as written today. The population is DERIVED from git, not hardcoded, so a future
# claim joins it automatically; the six non-claims are named by sha because they are frozen
# history and cannot decay. A vacuity guard runs first: an empty population would make the
# whole replay green while asserting nothing.
REPLAY="$(mk_hookrepo)"
SOLO_HANDOFF=""
for c in $(git -C "$METHODOLOGY" log --format=%H -- HANDOFFS.md); do
    files="$(git -C "$METHODOLOGY" show --name-only --format= "$c" | sed '/^$/d')"
    [ "$files" = "HANDOFFS.md" ] && SOLO_HANDOFF="$SOLO_HANDOFF $c"
done
CLAIMS=""
for c in $SOLO_HANDOFF; do
    case "$(git -C "$METHODOLOGY" log -1 --format=%s "$c")" in
        *"claim S"*) CLAIMS="$CLAIMS $c" ;;
    esac
done
NCLAIM=0; for c in $CLAIMS; do NCLAIM=$((NCLAIM+1)); done
if [ "$NCLAIM" -ge 26 ]; then
    pass "27.L1a vacuity guard: $NCLAIM real claim commits found to replay"
else
    fail "27.L1a the replay population collapsed to $NCLAIM (26 existed at c000a90) — the query is wrong, not the history"
fi

replay_verdict() {   # $1 = commit sha -> hook verdict for that commit's HANDOFFS.md diff
    if git -C "$METHODOLOGY" cat-file -e "$1~1:HANDOFFS.md" 2>/dev/null; then
        git -C "$METHODOLOGY" show "$1~1:HANDOFFS.md" > "$REPLAY/HANDOFFS.md"
    else
        rm -f "$REPLAY/HANDOFFS.md"
    fi
    git -C "$REPLAY" add -A HANDOFFS.md >/dev/null 2>&1
    git -C "$REPLAY" commit -q --no-verify -m "replay base $1" >/dev/null 2>&1
    git -C "$METHODOLOGY" show "$1:HANDOFFS.md" > "$REPLAY/HANDOFFS.md"
    git -C "$REPLAY" add HANDOFFS.md
    hook_verdict "$REPLAY"
}

BAD=""
for c in $CLAIMS; do
    v="$(replay_verdict "$c")"
    [ "$v" = "pass" ] || BAD="$BAD $(git -C "$METHODOLOGY" log -1 --format=%h "$c"):$v"
done
[ -z "$BAD" ] && pass "27.L1b all $NCLAIM historical claim commits pass the carve-out" \
    || fail "27.L1b historical claims still refused —$BAD"

# The non-claims are DERIVED as the complement of the claim set, not hardcoded, so a future
# solo-HANDOFFS commit that is not a claim joins them automatically. The six known members are
# named only as a coverage check on the query itself: 2 close-out receipts committed alone
# (f2d013b, 21fb521) and 4 repairs of an older receipt (f9ea5d7, faf2c42, a7c814d, 1626e09).
# Each is an action; each must still be refused.
NONCLAIMS=""
for c in $SOLO_HANDOFF; do
    case " $CLAIMS " in *" $c "*) ;; *) NONCLAIMS="$NONCLAIMS $c" ;; esac
done
MISSING=""
for want in f2d013b 21fb521 f9ea5d7 faf2c42 a7c814d 1626e09; do
    full="$(git -C "$METHODOLOGY" rev-parse "$want")"
    case " $NONCLAIMS " in *" $full "*) ;; *) MISSING="$MISSING $want" ;; esac
done
[ -z "$MISSING" ] && pass "27.L1c-cov the derived non-claim set still contains all 6 known members" \
    || fail "27.L1c-cov the derived non-claim set lost —$MISSING — the query is wrong, not the history"
BAD=""; NNON=0
for c in $NONCLAIMS; do
    NNON=$((NNON+1))
    v="$(replay_verdict "$c")"
    [ "$v" = "refuse" ] || BAD="$BAD $(git -C "$METHODOLOGY" log -1 --format=%h "$c"):$v"
done
[ -z "$BAD" ] && pass "27.L1c all $NNON historical non-claim HANDOFFS.md commits are still refused" \
    || fail "27.L1c a real non-claim commit was exempted —$BAD"
rm -rf "$REPLAY"

# --- M1-M5: MUTATION — each guard NARROWED, not deleted ---------------------
# A guard no mutant can falsify is a comment shaped like a guard. "Did not apply" is a
# distinct outcome from "survived": the mutant is diffed after patching, so a stale literal
# reports itself instead of silently scoring a kill.
MUTDIR="$(mktemp -d)"
MUTBAK="$MUTDIR/pristine"
cp "$HOOK" "$MUTBAK"
cp "$HOOK" "$MUTDIR/pre-commit"
chmod +x "$MUTDIR/pre-commit"
trap 'rm -rf "$MUTDIR"' EXIT INT TERM
# From here down the fixtures run the COPY, so the tracked hook is never edited.
HOOKS_DIR="$MUTDIR"
HOOK="$MUTDIR/pre-commit"

apply_mutant() {   # $1 = old literal, $2 = new literal -> 0 applied, 2 did not apply
    python3 - "$MUTBAK" "$HOOK" "$1" "$2" <<'PY'
import sys
src, dst, old, new = sys.argv[1:5]
t = open(src).read()
n = t.count(old)
if n == 0:
    sys.exit(2)          # did not apply — the literal is stale
if n > 1:
    sys.exit(3)          # AMBIGUOUS — replace(...,1) would patch the wrong site
open(dst, "w").write(t.replace(old, new, 1))
PY
}

# $1 = label, $2 = killer, $3 = old literal, $4 = new literal, $5 = fixture fn,
# $6 = the verdict the MUTANT is expected to produce on that fixture (i.e. the wrong one).
# Comparing against a named verdict rather than a boolean means a mutant that merely CRASHES
# the hook reports "crash:<rc>" instead of quietly scoring a kill it did not earn.
mutant_killed_by() {
    local label="$1" killer="$2" old="$3" new="$4" fixture="$5" wrong="$6" v
    apply_mutant "$old" "$new"; local rc=$?
    if [ "$rc" = "3" ]; then
        cp "$MUTBAK" "$HOOK"
        # Learned the hard way: ' --no-renames' also matched the COMMENT that explains it,
        # so the patch landed in prose and the mutant "survived" a guard it never removed.
        fail "$label MUTATION IS AMBIGUOUS — the literal occurs more than once; nothing was tested"
        return
    fi
    if [ "$rc" != "0" ]; then
        cp "$MUTBAK" "$HOOK"
        fail "$label MUTATION DID NOT APPLY — the literal is stale, so nothing was tested"
        return
    fi
    if diff -q "$MUTBAK" "$HOOK" >/dev/null 2>&1; then
        cp "$MUTBAK" "$HOOK"
        fail "$label MUTATION DID NOT APPLY — file unchanged after patch"
        return
    fi
    # The invariant that makes the scratch copy worth having: while a mutant is live, the
    # TRACKED hook is byte-unchanged. Checked here, per mutant, rather than only at the end —
    # an end-of-run check passes even when the harness mutates the real file, because each
    # mutant restores it. Delete the HOOKS_DIR redirection above and every mutant trips this.
    if [ "$(cksum < "$METHODOLOGY/.githooks/pre-commit")" != "$REAL_HOOK_CKSUM" ]; then
        fail "$label wrote into the TRACKED hook — the harness must mutate the scratch copy"
    fi
    v="$("$fixture")"
    cp "$MUTBAK" "$HOOK"
    if [ "$v" = "$wrong" ]; then
        pass "$label killed by $killer"
    else
        fail "$label SURVIVED $killer — the guard is not load-bearing (mutant verdict: $v)"
    fi
}

fx_flip() {            # N7's case: an in-place status flip, no block added
    local P; P="$(mk_hookrepo)"
    sed 's/^status: complete$/status: pending/' "$P/HANDOFFS.md" > "$P/H.tmp" && mv "$P/H.tmp" "$P/HANDOFFS.md"
    git -C "$P" add HANDOFFS.md
    hook_verdict "$P"
    rm -rf "$P"
}
fx_bundle() {          # N5's case: a claim bundled with a close-out
    local P; P="$(mk_hookrepo)"
    { handoff_claim S3; handoff_receipt S2; cat "$P/HANDOFFS.md"; } > "$P/H.tmp" && mv "$P/H.tmp" "$P/HANDOFFS.md"
    git -C "$P" add HANDOFFS.md
    hook_verdict "$P"
    rm -rf "$P"
}
fx_third_file() {      # N8's case: a claim carrying README.md
    local P; P="$(mk_hookrepo)"
    { handoff_claim S2; cat "$P/HANDOFFS.md"; } > "$P/H.tmp" && mv "$P/H.tmp" "$P/HANDOFFS.md"
    printf '# Readme\nedited\n' > "$P/README.md"
    git -C "$P" add HANDOFFS.md README.md
    hook_verdict "$P"
    rm -rf "$P"
}
fx_notes() {           # N2's case: the prescribed adopter claim shape
    local P; P="$(mk_hookrepo)"
    { handoff_claim S2; cat "$P/HANDOFFS.md"; } > "$P/H.tmp" && mv "$P/H.tmp" "$P/HANDOFFS.md"
    printf '# Session notes\nclaimed\n' > "$P/SESSION_NOTES.md"
    git -C "$P" add HANDOFFS.md SESSION_NOTES.md
    hook_verdict "$P"
    rm -rf "$P"
}
fx_example_fence() {   # N11's case: a fence added with no status line at all
    local P; P="$(mk_hookrepo)"
    printf '\nBlock format:\n\n```handoff\nsession: S<N>\n```\n' >> "$P/HANDOFFS.md"
    git -C "$P" add HANDOFFS.md
    hook_verdict "$P"
    rm -rf "$P"
}
fx_rename() {          # N13's case: a tracked source file renamed onto an exempt path
    local P; P="$(mk_hookrepo)"
    git -C "$P" rm -q SESSION_NOTES.md >/dev/null
    printf 'def real_code():\n    return 1\n' > "$P/src.py"
    git -C "$P" add -A >/dev/null; git -C "$P" commit -q --no-verify -m "drop notes, add source"
    git -C "$P" mv src.py SESSION_NOTES.md
    { handoff_claim S2; cat "$P/HANDOFFS.md"; } > "$P/H.tmp" && mv "$P/H.tmp" "$P/HANDOFFS.md"
    git -C "$P" add HANDOFFS.md
    hook_verdict "$P"
    rm -rf "$P"
}
fx_doc_example() {     # N14's case: a fenced documentation example, no receipt filed
    local P; P="$(mk_hookrepo)"
    printf '\nBlock format:\n\n````\n```handoff\nsession: S<N>\nstatus: pending\n```\n````\n' >> "$P/HANDOFFS.md"
    git -C "$P" add HANDOFFS.md
    hook_verdict "$P"
    rm -rf "$P"
}
fx_ext_diff() {        # N15's case: a claim under an external differ
    local P; P="$(mk_hookrepo)"
    printf '#!/bin/sh\necho EXT\n' > "$P/ext.sh"; chmod +x "$P/ext.sh"
    git -C "$P" config diff.external "$P/ext.sh"
    { handoff_claim S2; cat "$P/HANDOFFS.md"; } > "$P/H.tmp" && mv "$P/H.tmp" "$P/HANDOFFS.md"
    git -C "$P" add HANDOFFS.md
    hook_verdict "$P"
    rm -rf "$P"
}
fx_receipt() {         # N4's case: a close-out receipt committed alone
    local P; P="$(mk_hookrepo)"
    { handoff_receipt S2; cat "$P/HANDOFFS.md"; } > "$P/H.tmp" && mv "$P/H.tmp" "$P/HANDOFFS.md"
    git -C "$P" add HANDOFFS.md
    hook_verdict "$P"
    rm -rf "$P"
}

mutant_killed_by "27.M1 fence conjunct" "N7 (in-place status flip)" \
    '[ "$opened" -gt 0 ] && ' '' fx_flip pass
mutant_killed_by "27.M2 all-added-statuses-are-pending" "N5 (bundled close-out)" \
    ' && [ "$pending" -eq "$statuses" ]' '' fx_bundle pass
mutant_killed_by "27.M3 staged-set containment" "N8 (third file)" \
    '[ -z "$outside" ] && ' '' fx_third_file pass
mutant_killed_by "27.M4 SESSION_NOTES.md allowance" "N2 (adopter claim shape)" \
    "-e 'HANDOFFS.md' -e 'SESSION_NOTES.md'" "-e 'HANDOFFS.md'" fx_notes refuse
mutant_killed_by "27.M5 pending-line exactness" "N4 (close-out alone)" \
    "grep -cxE '\\+status:[[:space:]]*pending[[:space:]]*'" "grep -cE '^\\+status:'" fx_receipt pass
mutant_killed_by "27.M6 at-least-one-pending conjunct" "N11 (fence with no status line)" \
    '[ "$pending" -gt 0 ] && ' '' fx_example_fence pass
mutant_killed_by "27.M8 --no-renames on the staged-set query" "N13 (renamed source file)" \
    '--name-only --no-renames' '--name-only' fx_rename pass
mutant_killed_by "27.M9 stronger-wrapper conjunct" "N14 (documentation example)" \
    '[ "$wrapped" -eq 0 ] && ' '' fx_doc_example pass
mutant_killed_by "27.M10 plumbing-stable diff query" "N15 (external differ)" \
    '--cached --no-ext-diff --no-textconv --no-color -U0' '--cached -U0' fx_ext_diff refuse

# End-of-run backstop: the tracked hook still checksums to what it did before Test 27 started.
# Its honest scope is a LEAKED mutant — a restore that failed, or a crash between patch and
# restore. It does NOT catch a harness that mutates the tracked file and restores it each time
# (tried: removing the HOOKS_DIR redirection leaves this green), which is why the real
# invariant is asserted per mutant inside mutant_killed_by, where removing that redirection
# turns all six red. An earlier draft asserted the restore by comparing the file to the backup
# it had just been copied from — a line no mutant can falsify at all.
HOOKS_DIR="$METHODOLOGY/.githooks"
HOOK="$HOOKS_DIR/pre-commit"
if [ "$(cksum < "$HOOK")" = "$REAL_HOOK_CKSUM" ]; then
    pass "27.M7 the tracked hook was never modified by the mutation harness"
else
    fail "27.M7 the mutation harness wrote into the tracked hook — restore it before committing"
fi
rm -rf "$MUTDIR"; trap - EXIT INT TERM

echo ""
echo "== Summary: $PASS passed, $FAIL failed =="
[ "$FAIL" = "0" ]
