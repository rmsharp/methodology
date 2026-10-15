#!/usr/bin/env bash
# PR4: how much of open pull request #94 the candidate already contains, line for line.
# For each file #94 changes in the same place as the candidate (the three that conflict): the lines #94 adds to it
# that are NOT present, as exact lines, in the candidate's copy. Reads git objects only; writes nothing.
#   bash docs/planning/pr-composition-evidence/pr4-supersede.sh <repo> <candidate> <upstream> <pr94-head>
set -u
SRC=${1:?repository}; CAND=${2:?candidate commit}; UP=${3:?upstream commit}; H94=${4:?PR 94 head}
cd "$SRC" || exit 3
git cat-file -e "$H94^{commit}" 2>/dev/null || { echo "#94 head $H94 is not in $SRC"; exit 3; }
python3 - "$CAND" "$UP" "$H94" <<'PY'
import subprocess, sys
cand, up, h94 = sys.argv[1:4]
def sh(*a): return subprocess.run(a, capture_output=True, text=True).stdout
mb = sh('git', 'merge-base', up, h94).strip()
print(f'#94 head {h94[:12]}; its merge-base with upstream {mb[:9]}; the candidate is {sh("git", "rev-parse", "--short", cand).strip()}')
print('files #94 changes:', ', '.join(sh('git', 'diff', '--name-only', mb, h94).split()))
for f in ('starter-kit/methodology_trim.py', 'tools/test_methodology_trim.py', '.quality-gates.json'):
    diff = sh('git', 'diff', '-U0', mb, h94, '--', f)
    added = [l[1:] for l in diff.splitlines() if l.startswith('+') and not l.startswith('+++')]
    have = {l.strip() for l in sh('git', 'show', f'{cand}:{f}').splitlines()}
    missing = [l for l in added if l.strip() and l.strip() not in have]
    print(f'{f}: #94 adds {len(added)} lines; absent from the candidate as exact lines: {len(missing)}')
    for l in missing:
        print('     ', l.rstrip()[:160])
PY
