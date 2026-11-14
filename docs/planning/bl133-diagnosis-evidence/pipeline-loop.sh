#!/usr/bin/env bash
# Test 40 (5) of bin/tests.sh (lines 3330-3345), the two pipelines only, looped, with the exit status of EACH stage
# kept. Same fixture, same `set -uo pipefail`, same pipeline form `echo "$VAR" | grep -q PATTERN`.
# Usage: bash pipeline-loop.sh [N]      (default 3000; prints one summary line)
# A failure is any status other than "0 0" (echo, grep). "141 0" = echo killed by SIGPIPE (128 + 13), grep matched.
set -uo pipefail
N=${1:-3000}
BIN="$(cd "$(dirname "$0")/../../../bin" && pwd)"
P="$(mktemp -d)"; git -C "$P" init -q
printf '# Changelog\n\n### 2026-01-01 · [ad hoc] fixture\n\n**Model:** Fixture Model 1\n' > "$P/CHANGELOG.md"
printf '```handoff\nsession: S1\ndate: 2026-01-01\nstatus: complete\n```\n\nprose mentioning a model here\n' > "$P/HANDOFFS.md"
mkdir -p "$P/docs/archive"
printf '# Changelog\n\n### 2025-12-01 · [ad hoc] archived fixture\n\n**Model:** Fixture Model 2\n' > "$P/docs/archive/CHANGELOG-through-2025-12-01.md"
chmod 000 "$P/docs/archive/CHANGELOG-through-2025-12-01.md"
OUT40_UNREAD="$( (cd "$P" && "$BIN/model-report" --no-git) 2>&1 )"
chmod 644 "$P/docs/archive/CHANGELOG-through-2025-12-01.md"; rm -rf "$P"
echo "payload ${#OUT40_UNREAD} B, $(printf '%s\n' "$OUT40_UNREAD" | wc -l | tr -d ' ') lines"
f_a=0; f_b=0; stat=""
for ((i=0;i<N;i++)); do
  echo "$OUT40_UNREAD" | grep -q '1 file UNREADABLE and excluded'; s1="${PIPESTATUS[*]}"
  [ "$s1" = "0 0" ] || { f_a=$((f_a+1)); stat="$stat [$s1]"; }
  echo "$OUT40_UNREAD" | grep -q 'UNREADABLE'; s2="${PIPESTATUS[*]}"
  [ "$s2" = "0 0" ] || { f_b=$((f_b+1)); stat="$stat b[$s2]"; }
done
echo "N=$N  5c-pattern (byte ~650) fails=$f_a   5b-pattern (byte ~416) fails=$f_b   statuses:${stat:-none}" | cut -c1-300
