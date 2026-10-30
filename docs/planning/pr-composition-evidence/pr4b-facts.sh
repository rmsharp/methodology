#!/usr/bin/env bash
# PR4b: the derived facts the pull request's text states that no other script prints. Read-only: git objects only,
# nothing is written in the repository. Run from the repository root:
#   bash docs/planning/pr-composition-evidence/pr4b-facts.sh <upstream> <candidate> <old-candidate> <pr98-head> <pr96-head>
# e.g.   ... d50ce290d921 47637be21425 pr2/candidate 65990cda6afd ad5c980f3457
# Exit codes are read bare; every figure is printed beside the command that made it.
set -u
UP=${1:?upstream commit}; CAND=${2:?candidate commit}; OLD=${3:?old candidate ref}; H98=${4:?#98 head}; H96=${5:?#96 head}
UPF=$(git rev-parse "$UP^{commit}") || exit 3; CANDF=$(git rev-parse "$CAND^{commit}") || exit 3
OLDF=$(git rev-parse "$OLD^{commit}") || exit 3
echo "upstream $UPF"; echo "candidate $CANDF ($(git rev-list --count "$UPF..$CANDF") commits over upstream)"; echo "old candidate $OLDF"

echo; echo "== 1. each commit: files, added, removed (git show --shortstat --format=), in series order"
i=0; maxf=0
for h in $(git rev-list --reverse "$UPF..$CANDF"); do
  i=$((i+1))
  read -r f a d < <(git show --numstat --format= "$h" | awk '{f++; a+=$1; d+=$2} END {print f, a, d}')
  printf "%2d %s  %2d files  +%-5d -%-5d  %s\n" "$i" "$(git rev-parse --short=8 "$h")" "$f" "$a" "$d" "$(git log -1 --format=%s "$h" | cut -c1-90)"
  [ "$f" -gt "$maxf" ] && maxf=$f
done
echo "most files in one commit: $maxf"

echo; echo "== 2. the commits that remove references only my fork can resolve (subject starts 'docs: drop internal references')"
git log --format='%h' --grep='^docs: drop internal references' "$UPF..$CANDF" | wc -l | tr -d ' '

echo; echo "== 3. earlier work, not about the directory: the first commit and the ratchet commit (git show --numstat, added lines)"
tot=$(git diff --numstat "$UPF" "$CANDF" | awk '{a+=$1} END {print a}')
ew=$(git show --numstat --format= $(git rev-list --reverse "$UPF..$CANDF" | sed -n '1p;4p') | awk '{a+=$1} END {print a}')
echo "commits: $(git rev-list --reverse "$UPF..$CANDF" | sed -n '1p;4p' | cut -c1-8 | tr '\n' ' ')"
python3 - "$ew" "$tot" <<'PY'
import sys
ew, tot = int(sys.argv[1]), int(sys.argv[2])
print(f"added lines in them: {ew:,} of {tot:,} = {100*ew/tot:.1f}%")
PY

echo; echo "== 4. the old candidate's tree against this one: the files that differ (everything else is byte-identical)"
git diff --name-status "$OLDF" "$CANDF" | cat
echo "files differing: $(git diff --name-only "$OLDF" "$CANDF" | wc -l | tr -d ' ')"

echo; echo "== 5. upstream's history of the trimmer: commits that touched it, each with its TRIM_VERSION line"
n=0; miss=0; vers=""
for h in $(git log --format=%H "$UPF" -- starter-kit/methodology_trim.py); do
  n=$((n+1)); v=$(git show "$h:starter-kit/methodology_trim.py" | grep -m1 -o 'TRIM_VERSION = "[0-9.]*"' | tr -dc '0-9.\n')
  [ -z "$v" ] && miss=$((miss+1)); vers="$vers $v"
done
echo "commits: $n; without a TRIM_VERSION line: $miss; distinct versions: $(echo $vers | tr ' ' '\n' | sort -uV | tr '\n' ' ')"

echo; echo "== 6. the dashboard's own tests: names in upstream's file and not in the candidate's (def test_*)"
echo "upstream distinct names: $(git show "$UPF:tools/test_methodology_dashboard.py" | grep -o '    def test_[A-Za-z0-9_]*' | sed 's/ *def //' | sort -u | wc -l | tr -d ' '); candidate: $(git show "$CANDF:tools/test_methodology_dashboard.py" | grep -o '    def test_[A-Za-z0-9_]*' | sed 's/ *def //' | sort -u | wc -l | tr -d ' ')"
comm -23 <(git show "$UPF:tools/test_methodology_dashboard.py" | grep -o '    def test_[A-Za-z0-9_]*' | sed 's/ *def //' | sort -u) \
         <(git show "$CANDF:tools/test_methodology_dashboard.py" | grep -o '    def test_[A-Za-z0-9_]*' | sed 's/ *def //' | sort -u) | sed 's/^/absent from the candidate: /'

echo; echo "== 7. #98 and the candidate: the trimmer's version at each commit of #98, and whether the candidate carries its content"
for h in $(git rev-list --reverse "$UPF..$H98"); do
  printf "#98 %s TRIM_VERSION %s\n" "$(git rev-parse --short=8 "$h")" "$(git show "$h:starter-kit/methodology_trim.py" | grep -m1 -o 'TRIM_VERSION = "[0-9.]*"' | tr -dc '0-9.')"
done
printf "candidate TRIM_VERSION %s\n" "$(git show "$CANDF:starter-kit/methodology_trim.py" | grep -m1 -o 'TRIM_VERSION = "[0-9.]*"' | tr -dc '0-9.')"
for pat in FRONTIER_FRONT_MATTER_UNCOMMITTED '"SESSION_NOTES.md"'; do
  printf "%-38s occurrences in the trimmer: upstream %s, candidate %s, #98 head %s\n" "$pat" \
    "$(git show "$UPF:starter-kit/methodology_trim.py" | grep -c -- "$pat")" "$(git show "$CANDF:starter-kit/methodology_trim.py" | grep -c -- "$pat")" "$(git show "$H98:starter-kit/methodology_trim.py" | grep -c -- "$pat")"
done
echo "#96 commits over its merge-base with upstream: $(git rev-list --count "$(git merge-base "$UPF" "$H96")..$H96")"
echo; echo "== 8. git merge-tree --write-tree --name-only, with the repository's attributes (merge=union applies, as in a checkout) and with none (as GitHub merges); controls are upstream's tip"
EMPTY=$(git hash-object -t tree /dev/null)
mt() { # label, then the git arguments
  label=$1; shift; out=$(git "$@" 2>&1); rc=$?; tree=$(printf '%s\n' "$out" | head -1); res="exit $rc"
  if [ "$rc" -eq 1 ]; then
    for f in $(printf '%s\n' "$out" | sed -n '2,/^$/p' | grep -v '^$'); do res="$res; $f $(git show "$tree:$f" | grep -c '^<<<<<<<')"; done
  fi
  echo "  $label: $res"
}
for pr in "98 $H98" "96 $H96"; do set -- $pr
  echo "#$1 head $(git rev-parse --short=8 "$2")"
  mt "upstream tip, attributes   " merge-tree --write-tree --name-only "$UPF" "$2"
  mt "upstream tip, no attributes" --attr-source="$EMPTY" merge-tree --write-tree --name-only "$UPF" "$2"
  mt "candidate, attributes      " merge-tree --write-tree --name-only "$CANDF" "$2"
  mt "candidate, no attributes   " --attr-source="$EMPTY" merge-tree --write-tree --name-only "$CANDF" "$2"
done
echo; echo "== 9. what a project's documents say about where the framework files are (added after the cold read)"
echo "position of the runner's 'Where the files are' paragraph (line of the file; line 1 is the title): $(git show "$CANDF:starter-kit/SESSION_RUNNER.md" | grep -n '^\*\*Where the files are' | cut -d: -f1)"
tot_up=0; tot_c=0
for f in $(git diff --name-only "$UPF" "$CANDF" -- '*.md' ':!docs' ':!CHANGELOG.md' ':!HANDOFFS.md' ':!README.md' ':!CLAUDE.md'); do
  a=$(git show "$UPF:$f" 2>/dev/null | grep -c 'docs/methodology'); b=$(git show "$CANDF:$f" 2>/dev/null | grep -c 'docs/methodology')
  [ "$a" != "$b" ] && printf "  %-48s %2d -> %2d\n" "$f" "$a" "$b"
  tot_up=$((tot_up+a)); tot_c=$((tot_c+b))
done
echo "lines naming docs/methodology/ in the changed markdown files: upstream $tot_up, candidate $tot_c"

echo; echo "== 10. commit messages ending with a (cherry picked from commit ...) line, which names a commit only the fork has"
echo "$(git log --format=%B "$UPF..$CANDF" | grep -c '^(cherry picked from commit') of $(git rev-list --count "$UPF..$CANDF") commits"

echo; echo "== 11. the migration tool's own suite: classes that bin/tests.sh also runs"
git show "$CANDF:bin/tests.sh" | grep -n 'test_migrate_layout.py' | sed 's/>\/dev\/null.*//' | cut -c1-170
git show "$(git rev-list --reverse "$UPF..$CANDF" | sed -n '20p')" --format=%B --no-patch | grep -i 'fast class' | head -2
echo; echo "pr4b-facts done"
