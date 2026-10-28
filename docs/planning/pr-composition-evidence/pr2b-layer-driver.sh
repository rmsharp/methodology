#!/usr/bin/env bash
# PR2b layer verification driver: the parts the layer records name, in order, serially, one output file.
#   Part 1  docs/planning/pr-composition-evidence/layer-verify.sh <build clone> <commit> <clean clone>
#           (the quality ratchet --run, the scanner's summary line, the read-set budget, every tracked .verify.sh)
#   Part 2  bash bin/tests.sh run directly in that clean clone afterwards (ANSI stripped)
#   Part 3  starter-kit/methodology_trim.py --reverify on the one tracked shard, in the same clean clone
#   Part 4  only when bin/check-links has a --layout flag: each --layout value's exit code and last line
# Usage:  nohup bash pr2b-layer-driver.sh <layer number> <repo> <build clone> <clean clone> <output file> <done file> &
# and wait for the done file; a launcher's "completed" notice is not completion (check the done file or pgrep).
# Written for S385 (layer 9) from S384's scratchpad driver (layer 8), which ran Parts 1 to 3 unchanged.
set -u
LAYER=${1:?layer number}; REPO=${2:?repository holding layer-verify.sh}; BUILD=${3:?build clone}
CLEAN=${4:?clean clone}; OUT=${5:?output file}; DONE=${6:?done file}
rm -f "$DONE"
COMMIT=$(git -C "$BUILD" rev-parse HEAD)
{
  echo "# PR2b layer $LAYER verification output ($(date +%Y-%m-%d)). Commit $COMMIT (the layer's tip on pr2b/candidate)."
  echo "# Part 1: docs/planning/pr-composition-evidence/layer-verify.sh <scratch build clone> <commit> <clean clone>"
  echo "# Part 2: bash bin/tests.sh run directly in that clean clone afterwards, serial, ANSI stripped."
  echo "# Part 3: starter-kit/methodology_trim.py --reverify on the one tracked shard (docs/archive/CHANGELOG-through-2026-09-30.md), in the same clean clone."
  echo "# Part 4: bin/check-links --layout <value> for each value, only when the flag exists in this tree."
  echo "# One verification only: the commit verified is the commit kept (the replay needed no edit)."
  echo
  echo "===== Part 1: layer-verify.sh ====="
  echo "part1 start $(date +%H:%M:%S)"
  bash "$REPO/docs/planning/pr-composition-evidence/layer-verify.sh" "$BUILD" "$COMMIT" "$CLEAN"
  rc=$?
  echo "part1 end $(date +%H:%M:%S) layer-verify exit $rc"
  echo
  echo "===== Part 2: bash bin/tests.sh ====="
  echo "part2 start $(date +%H:%M:%S)"
  cd "$CLEAN" || exit 3
  bash bin/tests.sh 2>&1 | sed $'s/\x1b\\[[0-9;]*m//g'
  rc=${PIPESTATUS[0]}
  echo "part2 end $(date +%H:%M:%S) bin/tests.sh exit $rc"
  echo
  echo "===== Part 3: methodology_trim.py --reverify docs/archive/CHANGELOG-through-2026-09-30.md ====="
  python3 starter-kit/methodology_trim.py --reverify docs/archive/CHANGELOG-through-2026-09-30.md 2>&1
  echo "part3 exit $?"
  echo
  echo "===== Part 4: bin/check-links --layout ====="
  if grep -q -- '--layout' bin/check-links; then
    T="$(dirname "$OUT")/check-links-part4.$$"
    bin/check-links > "$T" 2>&1; echo "default (no flag): exit $?  $(tail -1 "$T")"
    for v in legacy new both; do
      bin/check-links --layout "$v" > "$T" 2>&1; rc=$?
      echo "--layout $v: exit $rc  $(tail -1 "$T")  [lines: $(wc -l < "$T" | tr -d ' ')]"
    done
    rm -f "$T"
  else
    echo "bin/check-links has no --layout flag in this tree: not applicable"
  fi
  echo "driver done $(date +%H:%M:%S)"
} > "$OUT" 2>&1
touch "$DONE"
