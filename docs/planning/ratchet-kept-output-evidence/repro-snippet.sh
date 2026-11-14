#!/bin/bash
# The Test 40 (5) assertion of bin/tests.sh (lines 3330-3345), alone, with the suite's own `set -uo pipefail`.
set -uo pipefail
BIN="$(cd "$(dirname "$0")/../../../bin" && pwd)"
P40="$(mktemp -d)"; git -C "$P40" init -q
printf '# Changelog\n\n### 2026-01-01 · [ad hoc] fixture\n\n**Model:** Fixture Model 1\n' > "$P40/CHANGELOG.md"
printf '```handoff\nsession: S1\ndate: 2026-01-01\nstatus: complete\n```\n\nprose mentioning a model here\n' > "$P40/HANDOFFS.md"
mkdir -p "$P40/docs/archive"
printf '# Changelog\n\n### 2025-12-01 · [ad hoc] archived fixture\n\n**Model:** Fixture Model 2\n' > "$P40/docs/archive/CHANGELOG-through-2025-12-01.md"
chmod 000 "$P40/docs/archive/CHANGELOG-through-2025-12-01.md"
OUT="$( (cd "$P40" && "$BIN/model-report" --no-git) 2>&1 )"
echo "$OUT" | grep -q '1 file UNREADABLE and excluded'
rc=$?
chmod 644 "$P40/docs/archive/CHANGELOG-through-2025-12-01.md"; rm -rf "$P40"
echo "rc=$rc outbytes=${#OUT}"
