#!/usr/bin/env bash
# Re-derives, from git alone, each factual claim in the maintainer's comment on PR #92
# (issuecomment-6257621669). Read-only. Needs the tags v3.8..v4.2 and the commits named below
# (git fetch upstream --tags; git fetch origin). Run from any clone of the repository.
set -u
echo "== 1. The two defects existed only in 9b69070 (PR #91 branch), never in v4.1"
for t in v4.1 v4.2; do
  git merge-base --is-ancestor 9b69070 "$t"; echo "9b69070 ancestor of $t: exit $? (0 = yes, 1 = no)"
done
echo "-- v4.1 bin/sync imports the checkout's own manifest (:15) and iterates it (:297)"
git show v4.1:bin/sync | sed -n '15p;297p'
echo "-- v4.1 bin/status does the same (:28, :254)"
git show v4.1:bin/status | sed -n '28p;254p'
echo "-- bin/_manifest_reader.py exists in v4.1? (no output = no)"
git ls-tree -r --name-only v4.1 | grep '_manifest_reader' || echo "(absent)"
echo "-- 9b69070's bin/sync executes the clone's manifest"
git show 9b69070:bin/sync | grep -n 'exec_module\|spec_from_file_location' | head -3
echo "== 2. Release-entry precedents, and the rule that each non-commit action gets its own entry"
git show f34769f:CHANGELOG.md | grep -n 'tagged and released'
git show f34769f:FRAMEWORK_APPARATUS.md | grep -n 'each non-commit action gets one of its own'
echo "== 3. Nothing under bin/ is distributed; the only distributed file changed v4.1..v4.2"
tmp=$(mktemp -d); git show v4.2:bin/_manifest.py > "$tmp/_manifest.py"
python3 -I - "$tmp" <<'PY'
import subprocess, sys
sys.path.insert(0, sys.argv[1])
import _manifest as m
srcs = {r[0] for r in m.DISTRIBUTION}
print("DISTRIBUTION rows:", len(srcs))
print("sources under bin/:", sorted(s for s in srcs if s.startswith("bin/")))
changed = subprocess.run(["git", "diff", "--name-only", "v4.1", "v4.2"], capture_output=True, text=True).stdout.split()
print("changed v4.1..v4.2 and distributed:", [c for c in changed if c in srcs])
PY
rm -rf "$tmp"
for t in v4.1 v4.2; do printf '%s ' "$t"; git show "${t}:starter-kit/methodology_dashboard.py" | grep -m1 '^DASHBOARD_VERSION'; done
echo "== 4. The tag: v4.2 lightweight, v3.8-v4.1 annotated; v3.8's tag stayed put while its docs landed in 2f911c9"
git tag -l --format='%(refname:short) %(objecttype) %(*objectname:short)' v3.8 v4.0 v4.1 v4.2
git log -1 --format='2f911c9 %cI %s' 2f911c9
echo "== 5. Small points"
git show v4.2:bin/_manifest_reader.py | sed -n '43,44p'
git log -1 --format='merge e107356 committed %cI' e107356
