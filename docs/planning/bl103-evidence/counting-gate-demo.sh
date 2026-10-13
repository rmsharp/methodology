#!/bin/bash
# BL-103 repair 3 (S307): "a gate that counts the unmeasured" cannot see its own run. The ratchet writes the
# results file AFTER every gate has run (quality_ratchet.py run_gates, then do_run), so a gate that reads that
# file reads the previous run. Run from the repository root; the scratch project goes under $TMPDIR.
set -u
ROOT=$(git rev-parse --show-toplevel)
W=$(mktemp -d); cd "$W" && git init -q . && git -c user.email=t@t -c user.name=t commit -q --allow-empty -m init
cat > counter.py <<'PY'
import json
try:
    print(json.load(open('.quality-gates-results.json'))['summary']['unmeasured'])
except Exception:
    print(0)
PY
cat > .quality-gates.json <<'JSON'
{"version":1,"gates":[
 {"name":"no-command-gate","direction":"max","threshold":0},
 {"name":"unmeasured-count","direction":"max","threshold":0,"command":"python3 counter.py","extract":"(\\d+)"}
]}
JSON
for i in 1 2 3; do
  echo "--- run $i"
  python3 "$ROOT/starter-kit/quality_ratchet.py" --run 2>&1 | sed 's/\x1b\[[0-9;]*m//g' | grep -E 'unmeasured-count|no-command-gate|cite in the receipt'
done
rm -rf "$W"
