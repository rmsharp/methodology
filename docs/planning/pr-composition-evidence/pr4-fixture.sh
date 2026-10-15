#!/usr/bin/env bash
# PR4: plan section 6's first two claims as a recipe a reader can run, with no adopter in it.
#   claim 1  a project that keeps its files at the root is unchanged in where they sit
#   claim 2  no file a project owns (a seed) is overwritten
# Two checkouts (upstream's tip and the candidate's tip), each in a CLEAN --no-local clone; two throwaway projects
# synced once by each tool; the trees diffed. Writes nothing outside <work-dir>. Exit codes are read bare.
#   bash docs/planning/pr-composition-evidence/pr4-fixture.sh <repo> <candidate> <upstream> <work-dir>
set -u
SRC=${1:?repository holding both commits}; CAND=${2:?candidate commit}; UP=${3:?upstream commit}; W=${4:?work dir}
rm -rf "$W"; mkdir -p "$W"
git clone --no-local -q "$SRC" "$W/up" && git -C "$W/up" checkout -q "$UP" || exit 3
git clone --no-local -q "$SRC" "$W/pr" && git -C "$W/pr" checkout -q "$CAND" || exit 3
mkproj() {
  git init -q "$1" && git -C "$1" config user.email fixture@example.invalid && git -C "$1" config user.name fixture
  echo "a fixture project" > "$1/README.md"; git -C "$1" add -A; git -C "$1" commit -q -m init
}
paths() { git -C "$1" status --porcelain --untracked-files=all | sed 's/^...//' | sort; }

echo "== (a) an empty project, synced once by each tool"
mkproj "$W/a-up"; cp -R "$W/a-up" "$W/a-pr"
python3 -B "$W/up/bin/sync" "$W/a-up" > "$W/a-up.out" 2>&1; echo "upstream's bin/sync exit $?"
python3 -B "$W/pr/bin/sync" "$W/a-pr" > "$W/a-pr.out" 2>&1; echo "this branch's bin/sync exit $?"
paths "$W/a-up" > "$W/a-up.paths"; paths "$W/a-pr" > "$W/a-pr.paths"
echo "paths written: upstream $(wc -l < "$W/a-up.paths" | tr -d ' '), this branch $(wc -l < "$W/a-pr.paths" | tr -d ' '); the two lists are $(cmp -s "$W/a-up.paths" "$W/a-pr.paths" && echo identical || echo DIFFERENT)"
echo "a methodology/ directory in the project after this branch's sync: $( [ -e "$W/a-pr/methodology" ] && echo YES || echo no)"
diff -rq --exclude=.git "$W/a-up" "$W/a-pr" | grep -v '\.out\b' > "$W/a.diff"
echo "paths whose bytes differ: $(grep -c '^Files ' "$W/a.diff")"
UP_DIR="$W/up" PR_DIR="$W/pr" UPC="$UP" CANDC="$CAND" A_DIFF="$W/a.diff" python3 - <<'PY'
import os, re, subprocess
changed = subprocess.run(['git', '-C', os.environ['PR_DIR'], 'diff', '--name-only', os.environ['UPC'], os.environ['CANDC'], '--',
                          'starter-kit', 'workstreams', 'HOW_TO_USE.md', 'ITERATIVE_METHODOLOGY.md', 'FRAMEWORK_APPARATUS.md'],
                         capture_output=True, text=True).stdout.split()
norm = lambda n: n.lstrip('.')
names = {norm(os.path.basename(p)) for p in changed}
differ = [norm(os.path.basename(m.group(1))) for m in (re.match(r'Files (\S+) and ', l) for l in open(os.environ['A_DIFF'])) if m]
unexplained = sorted(set(differ) - names)
print(f"differing paths that are a file this branch changes (git diff --name-only, starter-kit, workstreams, the three manuals): {len(differ) - len(unexplained)} of {len(differ)}")
print('unexplained:', unexplained or 'none')
PY

echo; echo "== (b) a project that holds upstream's files and has edited every seed"
python3 - "$W/up" "$W/a-up" <<'PY'
import importlib.util, json, sys, pathlib
spec = importlib.util.spec_from_file_location('m', sys.argv[1] + '/bin/_manifest.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
proj = pathlib.Path(sys.argv[2])
seeds = [d for _s, d, disp in m.DISTRIBUTION if disp == m.SEED]
for d in seeds:
    p = proj / d
    if not p.is_file():
        continue
    if d.endswith('.json'):
        j = json.loads(p.read_text() or '{}'); j['_adopter_owned'] = 'a sync must leave this key'; p.write_text(json.dumps(j, indent=2) + '\n')
    else:
        with open(p, 'a') as fh:
            fh.write('\n# adopter-owned edit: a sync must leave this line\n')
print('seeds edited:', len(seeds))
PY
git -C "$W/a-up" add -A; git -C "$W/a-up" commit -q -m "synced and seeds edited"
cp -R "$W/a-up" "$W/b-up"; cp -R "$W/a-up" "$W/b-pr"
python3 -B "$W/up/bin/sync" "$W/b-up" > "$W/b-up.out" 2>&1; echo "upstream's bin/sync exit $?; paths it wrote: $(paths "$W/b-up" | wc -l | tr -d ' ')"
python3 -B "$W/pr/bin/sync" "$W/b-pr" > "$W/b-pr.out" 2>&1; echo "this branch's bin/sync exit $? (plain, no --force); paths it wrote: $(paths "$W/b-pr" | wc -l | tr -d ' ')"
SEEDS=$(python3 - "$W/up" <<'PY'
import importlib.util, sys
spec = importlib.util.spec_from_file_location('m', sys.argv[1] + '/bin/_manifest.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print(' '.join(d for _s, d, disp in m.DISTRIBUTION if disp == m.SEED))
PY
)
changed_seeds=0; for s in $SEEDS; do [ -f "$W/b-pr/$s" ] && ! git -C "$W/b-pr" diff --quiet -- "$s" && changed_seeds=$((changed_seeds+1)); done
echo "seeds this branch's sync changed (of $(echo $SEEDS | wc -w | tr -d ' ')): $changed_seeds"
echo "a methodology/ directory after this branch's sync: $( [ -e "$W/b-pr/methodology" ] && echo YES || echo no)"
echo; echo "pr4-fixture done"
