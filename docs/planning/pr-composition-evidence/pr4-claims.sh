#!/usr/bin/env bash
# PR4: plan section 6's claims, re-run on the candidate's tip and on upstream's tip, each in a CLEAN --no-local
# clone (0 dirty paths), serially. Prints the figure each sentence of the pull request's body rests on, beside the
# command that produced it. Takes 20 to 40 minutes. Run it as
#   nohup bash docs/planning/pr-composition-evidence/pr4-claims.sh <repo> <candidate> <upstream> <work-dir> > <work-dir>/out.txt 2>&1 &
# and wait for the last line, `pr4-claims done`. Exit codes are read bare, never through a pipe.
set -u
SRC=${1:?repository holding both commits}; CAND=${2:?candidate commit}; UP=${3:?upstream commit}; W=${4:?work dir}
HEAD94=${HEAD94:-972eb2cd6263}; HEAD92=${HEAD92:-fa2bb5d464f9}
mkdir -p "$W"; rm -rf "$W/cand" "$W/up"
git clone --no-local -q "$SRC" "$W/cand" || exit 3
git clone --no-local -q "$SRC" "$W/up" || exit 3
( cd "$W/cand" && git checkout -q "$CAND" && git config --unset core.hooksPath 2>/dev/null; true )
( cd "$W/up" && git checkout -q "$UP" && git config --unset core.hooksPath 2>/dev/null; true )
CANDFULL=$(git -C "$W/cand" rev-parse HEAD); UPFULL=$(git -C "$W/up" rev-parse HEAD)
echo "candidate $CANDFULL ($(git -C "$W/cand" status --short | wc -l | tr -d ' ') dirty paths)"
echo "upstream  $UPFULL ($(git -C "$W/up" status --short | wc -l | tr -d ' ') dirty paths)"

echo; echo "== 1. size: git diff --shortstat $UP $CAND ; git rev-list --count $UP..$CAND"
git -C "$W/cand" diff --shortstat "$UPFULL" "$CANDFULL"
echo "commits: $(git -C "$W/cand" rev-list --count "$UPFULL..$CANDFULL")"
echo "merge-base is upstream's tip: $( [ "$(git -C "$W/cand" merge-base "$UPFULL" "$CANDFULL")" = "$UPFULL" ] && echo yes || echo NO )"
echo "-- changed paths by status (git diff --name-status):"
git -C "$W/cand" diff --name-status "$UPFULL" "$CANDFULL" | cut -c1 | sort | uniq -c
echo "-- paths outside the shipped set (docs/, CLAUDE.md, README.md, the ledgers):"
git -C "$W/cand" diff --name-only "$UPFULL" "$CANDFULL" | grep -E '^(docs/|CLAUDE\.md|README\.md|CHANGELOG\.md|HANDOFFS\.md|\.context-budget\.json)' || echo "  (none beyond .context-budget.json shown above if any)"

echo; echo "== 2. the shell suite, each tip: bash bin/tests.sh (captured, exit read bare)"
( cd "$W/up" && bash bin/tests.sh > "$W/up-suite.txt" 2>&1; echo "upstream suite exit $?" )
tail -4 "$W/up-suite.txt"
( cd "$W/cand" && bash bin/tests.sh > "$W/cand-suite.txt" 2>&1; echo "candidate suite exit $?" )
tail -4 "$W/cand-suite.txt"

echo; echo "== 3. the gates, each tip: python3 starter-kit/quality_ratchet.py --run"
( cd "$W/up" && python3 starter-kit/quality_ratchet.py --run > "$W/up-ratchet.txt" 2>&1; echo "upstream ratchet exit $?" )
grep -E 'quality gates — run|cite in the receipt' "$W/up-ratchet.txt"
( cd "$W/cand" && python3 starter-kit/quality_ratchet.py --run > "$W/cand-ratchet.txt" 2>&1; echo "candidate ratchet exit $?" )
cat "$W/cand-ratchet.txt"

echo; echo "== 4. links and literals, candidate: bin/check-links --layout both ; bin/check-layout-literals"
( cd "$W/cand" && python3 bin/check-links --layout both > "$W/cand-links.txt" 2>&1; echo "check-links --layout both exit $?" )
tail -3 "$W/cand-links.txt"
( cd "$W/cand" && python3 bin/check-layout-literals > "$W/cand-literals.txt" 2>&1; echo "check-layout-literals exit $?" )
tail -1 "$W/cand-literals.txt"

echo; echo "== 5. the resolver block is one block, byte-identical in every tool that embeds it"
( cd "$W/cand" && python3 tools/test_layout_resolver.py > "$W/cand-layout.txt" 2>&1; echo "layout suite exit $?" )
tail -4 "$W/cand-layout.txt"
( cd "$W/cand" && python3 - <<'PY'
import sys
sys.path.insert(0, 'tools')
import layout_resolver as lr
import test_layout_resolver as t
block = lr.embedded_block(open('tools/layout_resolver.py', encoding='utf-8').read())
copies = list(t.TestEveryEmbeddedCopyIsByteIdentical.COPIES) + ['tools/methodology_dashboard.py']
equal = 0
for rel in copies:
    text = open(rel, encoding='utf-8').read()
    ok = text.count(lr.BEGIN) == 1 and lr.embedded_block(text) == block
    equal += ok
    print('  ', 'equal    ' if ok else 'DIFFERENT', rel)
print(f'files embedding the block: {len(copies)}; each carries exactly one and equals tools/layout_resolver.py: {equal}')
PY
)

echo; echo "== 6. every frozen proof gives the verdict it gave: exit of each tracked *.verify.sh, both tips"
for side in up cand; do
  ( cd "$W/$side" && for proof in $(git ls-files '*.verify.sh'); do bash "$proof" > /dev/null 2>&1; echo "$side $proof exit $?"; done )
done

echo; echo "== 7. no threshold loosens, at any of the commits: compare() of the candidate's ratchet, each commit against its parent"
( cd "$W/cand" && UPFULL=$UPFULL CANDFULL=$CANDFULL python3 - <<'PY'
import importlib.util, os, subprocess
spec = importlib.util.spec_from_file_location('qr', 'starter-kit/quality_ratchet.py')
qr = importlib.util.module_from_spec(spec); spec.loader.exec_module(qr)
def git(*a): return subprocess.run(['git', *a], capture_output=True, text=True).stdout
def cfg(rev):
    t = git('show', f'{rev}:.quality-gates.json')
    c, d = qr.load_manifest_text(t, rev[:9])
    return c, d
up, cand = os.environ['UPFULL'], os.environ['CANDFULL']
revs = git('rev-list', '--reverse', f'{up}..{cand}').split()
prev, total_ref, total_warn, defects = up, 0, 0, 0
for r in revs:
    old, _ = cfg(prev); new, d = cfg(r)
    if d: defects += len(d)
    ref, warn = qr.compare(old, new)
    total_ref += len(ref); total_warn += len(warn)
    prev = r
print(f'commits compared: {len(revs)}; refusals: {total_ref}; warnings: {total_warn}; manifest defects: {defects}')
o, _ = cfg(up); n, _ = cfg(cand)
go, gn = qr.gate_map(o), qr.gate_map(n)
print(f'gates at upstream tip: {len(go)}; at candidate tip: {len(gn)}; removed: {sorted(set(go)-set(gn))}')
raised = [k for k in go if k in gn and go[k] != gn[k]]
print('thresholds changed (upstream -> candidate):')
for k in sorted(raised):
    a, b = go[k], gn[k]
    print(f"  {k}: {a.get('direction')} {a.get('threshold')} -> {b.get('direction')} {b.get('threshold')}")
print('added gates:', sorted(set(gn) - set(go)))
PY
)

echo; echo "== 8. against the two open pull requests: git merge-tree --write-tree --name-only (exit 0 clean, 1 conflicts)"
for pair in "94 $HEAD94" "92 $HEAD92"; do
  set -- $pair; n=$1; sha=$2
  git -C "$SRC" cat-file -e "$sha^{commit}" 2>/dev/null || { echo "#$n head $sha is not in $SRC"; continue; }
  out=$(git -C "$SRC" merge-tree --write-tree --name-only "$CANDFULL" "$sha" 2>&1); rc=$?
  tree=$(printf '%s\n' "$out" | head -1)
  echo "#$n head $sha: merge-tree exit $rc"
  if [ "$rc" -eq 1 ]; then
    for f in $(printf '%s\n' "$out" | sed -n '2,/^$/p' | grep -v '^$'); do
      echo "   $f: $(git -C "$SRC" show "$tree:$f" | grep -c '^<<<<<<<') conflict region(s)"
    done
  fi
done
echo; echo "pr4-claims done"
