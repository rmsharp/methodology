#!/bin/bash
# Evidence [E2] for docs/planning/ratchet-kept-output-plan.md: how big is what `bash bin/tests.sh` prints.
# Usage: suite-output-measure.sh <stdout-file> <stderr-file> <started-file> <finished-file> <exit-file>
# The five files are what a detached run of `bash bin/tests.sh > out 2> err` leaves (see the plan, section 9).
# Reads only those files. Prints counts and the first and last lines, never the whole output.
out=$1; err=$2; t0=$(cat "$3"); t1=$(cat "$4"); rc=$(cat "$5")
s0=$(date -j -u -f %Y-%m-%dT%H:%M:%SZ "$t0" +%s 2>/dev/null || date -u -d "$t0" +%s)
s1=$(date -j -u -f %Y-%m-%dT%H:%M:%SZ "$t1" +%s 2>/dev/null || date -u -d "$t1" +%s)
echo "run: $t0 to $t1 = $((s1 - s0)) s, exit $rc"
echo "stdout: $(wc -l < "$out" | tr -d ' ') lines, $(wc -c < "$out" | tr -d ' ') bytes; stderr: $(wc -c < "$err" | tr -d ' ') bytes"
echo "  PASS: lines $(grep -c '^  PASS: ' "$out"), FAIL: lines $(grep -c '^  FAIL: ' "$out"), SKIP: lines $(grep -c '^  SKIP: ' "$out"), '== Test' headers $(grep -c '^== Test' "$out")"
echo "longest line: $(awk '{ if (length($0) > m) m = length($0) } END { print m }' "$out") bytes"
echo "first line: $(head -1 "$out" | cut -c1-120)"
echo "last line:  $(tail -1 "$out" | cut -c1-120)"
echo "the failure-marker grep a person would run on a kept file: grep -c '^  FAIL: ' -> $(grep -c '^  FAIL: ' "$out") on this green run"
