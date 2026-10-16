#!/usr/bin/env bash
# PR4: do the maintainer's own tests still pass against the candidate's code?
# Upstream's three unit-test files for the tools the candidate rewrites (the dashboard, the quality ratchet, the
# context-budget tool), exactly as they are at the upstream commit, run against the candidate's tree; and the
# ledger hook's own selftest, whose 17 labels at upstream are looked for in the candidate's selftest.
# ONE change is made to upstream's dashboard test file and it is printed: its fixture helper builds a metrics
# dict without the key `read_cap_watch`, which the candidate's new risk rows index directly. The dashboard file
# is run both ways, so the effect of that one line is on the page.
# Reads git objects into a scratch directory; writes nothing in the repository.
#   bash docs/planning/pr-composition-evidence/pr4-oracle.sh <repo> <upstream> <candidate> <scratch-dir>
set -u
SRC=${1:?repository}; UP=${2:?upstream commit}; CAND=${3:?candidate commit}; T=${4:?scratch dir}
cd "$SRC" || exit 3
rm -rf "$T"; mkdir -p "$T"
git archive "$CAND" | tar -x -C "$T"
for t in test_methodology_dashboard test_quality_ratchet test_context_budget; do
  git show "$UP:tools/$t.py" > "$T/tools/${t}_up.py"
done
python3 -I - "$T/tools/test_methodology_dashboard_up.py" "$T/tools/test_methodology_dashboard_up_shim.py" <<'PY'
import sys
src = open(sys.argv[1], encoding="utf-8").read()
old = '"files": {"largest_files": []},'
assert src.count(old) == 1, src.count(old)
open(sys.argv[2], "w", encoding="utf-8").write(src.replace(old, '"files": {"largest_files": [], "read_cap_watch": []},'))
print("the one change to upstream's dashboard tests (base_metrics):")
print("   -", old); print('   + "files": {"largest_files": [], "read_cap_watch": []},')
PY
run() {   # <label> <file>
  ( cd "$T" && python3 -B "tools/$2" > "$T/out-$2.txt" 2>&1 )
  printf '%-52s %s' "$1" "$(grep -E '^Ran ' "$T/out-$2.txt" | head -1)"
  s=$(grep -E '^(OK|FAILED)' "$T/out-$2.txt" | tail -1); echo "  -> ${s:-no verdict}"
  grep -E '^(FAIL|ERROR):' "$T/out-$2.txt" | sed 's/^/      /' | cut -c1-170
}
echo
run "dashboard tests, upstream's file as it is" test_methodology_dashboard_up.py
echo "      error kinds: $(grep -E '^(KeyError|AttributeError|TypeError)' "$T/out-test_methodology_dashboard_up.py.txt" | sort | uniq -c | tr -s ' ' | tr '\n' ';')"
run "dashboard tests, with the one fixture line" test_methodology_dashboard_up_shim.py
run "quality-ratchet tests, upstream's file" test_quality_ratchet_up.py
run "context-budget tests, upstream's file" test_context_budget_up.py
echo
echo "the ledger hook's own selftest, the candidate's:"
( cd "$T" && sh .githooks/pre-commit --selftest 2>&1 | tail -1 )
python3 -I - "$SRC" "$UP" "$CAND" <<'PY'
import re, subprocess, sys
src, up, cand = sys.argv[1:4]
def labels(ref):
    t = subprocess.run(["git", "-C", src, "show", ref + ":.githooks/pre-commit"], capture_output=True, text=True).stdout
    return re.findall(r'expect "([^"]+)"', t)
u, c = labels(up), set(labels(cand))
miss = [l for l in u if l not in c]
print("upstream's selftest has %d labelled checks; %d appear word for word in the candidate's (%d in all)" % (len(u), len(u) - len(miss), len(c)))
for l in miss:
    print("   reworded:", l)
PY
