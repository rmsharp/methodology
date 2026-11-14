#!/usr/bin/env bash
# Run ONLY Test 45 of the repo's bin/tests.sh against the tree given as $1 (default: cwd's repo).
set -uo pipefail
ROOT="${1:-$(git rev-parse --show-toplevel)}"
T="$ROOT/bin/tests.sh"
S="$(grep -n '^echo "== Test 45:' "$T" | cut -d: -f1)"
E="$(grep -n "^# upstream's Tests 27-34" "$T" | cut -d: -f1)"
H="$(grep -n '^echo "== Test 1:' "$T" | cut -d: -f1)"
TMP="$(mktemp)"
{ sed -n "1,$((H-1))p" "$T"; echo "BIN=\"$ROOT/bin\"; METHODOLOGY=\"$ROOT\"; STARTER=\"$ROOT/starter-kit\""; sed -n "${S},$((E-1))p" "$T"; echo 'echo "== Summary: $PASS passed, $FAIL failed, $SKIP skipped =="; [ "$FAIL" = 0 ]'; } > "$TMP"
bash "$TMP"; RC=$?
rm -f "$TMP"; exit $RC
