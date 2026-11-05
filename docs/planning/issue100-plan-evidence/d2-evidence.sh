#!/usr/bin/env bash
# Evidence for decision D2 of docs/planning/issue100-fixes-plan.md (S420): does upstream issue #100
# finding 4 ("we chose transient") settle PR #98's "Underneath" question, and does #98's first commit stand?
#   bash docs/planning/issue100-plan-evidence/d2-evidence.sh [ADOPTER_PARENT_DIR]
# READ-ONLY. It reads each named adopter's SESSION_NOTES.md (never writes, never recurses over the parent
# directory; the twelve names are listed below), greps `upstream/main` with `git grep`, and runs
# `git merge-tree --write-tree`, which builds objects only; --attr-source is the EMPTY tree so merge=union
# does not apply, as on GitHub.
# Tags: [notes-*] the adopters' notes files; [text-*] where the framework says "transient" or "accumulates";
#       [drop-*] #98's second and third commits replayed onto upstream/main WITHOUT its first commit.
set -u
PARENT=${1:-$HOME/Development}
cd "$(git rev-parse --show-toplevel)" || exit 3
EMPTY=4b825dc642cb6eb9a060e54bf8d69288fbee4904
UP=upstream/main
echo "# d2-evidence: fork HEAD $(git rev-parse --short=8 HEAD), $UP $(git rev-parse --short=8 $UP)"

echo
echo "# 1. the notes files as they are today, and how each has behaved. A record is a '### What Session N Did' heading"
echo "#    (the runner's 1B/3D form); 0 records means the file uses another grammar, so its shape is UNKNOWN here."
echo "#    A snapshot cannot tell 'transient by design' from 'just trimmed', so [notes-series] gives the record count"
echo "#    at each of the file's last 15 commits (oldest first): holding at 3 or fewer is transient behaviour (the"
echo "#    claim adds this session's record, the close-out replaces it), a climb of 3 or more is accumulation, a drop"
echo "#    of 3 or more between neighbours is a trim or an archive ('cut'); no heading of the runner form throughout"
echo "#    means the file is unreadable by this count ('other-grammar')."
CEIL_BYTES=$(python3 -I - <<'PY'
import json
d = json.load(open("starter-kit/context-budget.json"))
for f in d.get("files", d.get("budgets", [])):
    s = json.dumps(f)
    if "SESSION_NOTES" in s:
        print(f.get("max_bytes", f.get("bytes", "?"))); break
else:
    print("?")
PY
)
echo "[notes-seed-ceiling] starter-kit/context-budget.json caps SESSION_NOTES.md at $CEIL_BYTES B"
ADOPTERS="airqino chat_verification church_growth colossians_1_15_20 data_quality_assurance feedback-loop-comparison model_project_constructor mts-system nprcgenekeepr Philippians vscode_quarto_ext wsfct"
n=0; have=0; acc=0; trans=0; unk=0; over=0; untracked=0; flat=0; climb=0; cut=0; og=0; fa=0
for d in $ADOPTERS; do
  dir="$PARENT/$d"
  [ -d "$dir" ] || { echo "[notes-skip] $d: no directory under $PARENT"; continue; }
  n=$((n+1))
  f=""
  for cand in SESSION_NOTES.md methodology/SESSION_NOTES.md; do [ -f "$dir/$cand" ] && { f=$cand; break; }; done
  if [ -z "$f" ]; then echo "[notes-adopter] $d: no SESSION_NOTES.md"; continue; fi
  have=$((have+1))
  b=$(wc -c < "$dir/$f" | tr -d ' ')
  l=$(wc -l < "$dir/$f" | tr -d ' ')
  r=$(grep -c '^### What Session [^ ]* Did' "$dir/$f")
  if git -C "$dir" ls-files --error-unmatch -- "$f" >/dev/null 2>&1; then tr_=tracked; else tr_=UNTRACKED; untracked=$((untracked+1)); fi
  if [ "$r" -eq 0 ]; then shape=other-grammar; unk=$((unk+1)); elif [ "$r" -le 2 ]; then shape=1-or-2-records-now; trans=$((trans+1)); else shape=3-or-more-records-now; acc=$((acc+1)); fi
  ov=no; if [ "$CEIL_BYTES" != "?" ] && [ "$b" -gt "$CEIL_BYTES" ]; then ov=OVER; over=$((over+1)); fi
  echo "[notes-adopter] $d: $f bytes=$b lines=$l records=$r $shape $tr_ over_seed_ceiling=$ov"
  series=""
  # --follow carries the series across a move into methodology/; --name-only gives the path AT each commit
  pairs=$(git -C "$dir" log --follow --name-only --format='@%h' -n 15 -- "$f" | grep -v '^$' | paste -d' ' - - | sed 's/^@//' | sed '1!G;h;$!d')   # oldest first
  while read -r h p; do
    [ -n "$h" ] || continue
    c=$(git -C "$dir" show "$h:$p" 2>/dev/null | grep -c '^### What Session [^ ]* Did')
    series="$series $c"
  done <<EOF2
$pairs
EOF2
  summ=$(printf '%s\n' $series | python3 -I -c '
import sys
v=[int(x) for x in sys.stdin.read().split()]
if not v: print("no-history"); raise SystemExit
cut=any(a-b>=3 for a,b in zip(v,v[1:]))
# order matters: a file with no heading of the runner form throughout is unreadable here, not transient
kind=("other-grammar" if max(v)==0 else ("cut" if cut else ("climb" if v[-1]>=v[0]+3 else ("holds-at-3-or-fewer" if max(v)<=3 else "flat-above-3"))))
print("min=%d max=%d last=%d n=%d kind=%s" % (min(v),max(v),v[-1],len(v),kind))')
  echo "[notes-series] $d:$series | $summ"
  case "$summ" in *kind=holds-at-3-or-fewer*) flat=$((flat+1));; *kind=climb*) climb=$((climb+1));; *kind=cut*) cut=$((cut+1));; *kind=other-grammar*) og=$((og+1));; *kind=flat-above-3*) fa=$((fa+1));; esac
done
echo "[notes-total] adopters=$n with_notes_file=$have 1_or_2_records_now=$trans 3_or_more_now=$acc other_grammar=$unk over_seed_ceiling=$over untracked=$untracked"
echo "[notes-behaviour] over the last 15 commits of each file (renames followed): holds_at_3_or_fewer=$flat climbing=$climb cut_at_least_once=$cut flat_above_3=$fa other_grammar_throughout=$og (these five add to the adopters read)"

echo
echo "# 2. what $UP says: every place that calls the file transient or says it accumulates"
echo "#    (the issue cites v4.2 f34769f; these are the lines on $UP, so a cited line that moved shows here)"
git grep -n -i -E 'overwritten every session|overwritten next session|is transient|transient handoff|transient scratchpad|transient session-notes|session history accumulates' "$UP" -- \
  starter-kit/SESSION_NOTES.md starter-kit/SESSION_RUNNER.md starter-kit/HANDOFFS.md ITERATIVE_METHODOLOGY.md FRAMEWORK_APPARATUS.md |
  sed 's/^upstream\/main://' | cut -c1-170 | sed 's/^/[text-upstream] /'
echo "# the steps that add (1B stub, 3A evaluation 'under a heading', 3D 'Update SESSION_NOTES.md') on $UP:"
git grep -n -E 'Update `SESSION_NOTES.md`|under a heading|write a stub to `SESSION_NOTES.md`' "$UP" -- starter-kit/SESSION_RUNNER.md |
  sed 's/^upstream\/main://' | cut -c1-170 | sed 's/^/[text-steps] /'
echo "# the seed's own context-budget note on UPDATE read as ADD:"
git grep -n -i -E 'UPDATE|ADD' "$UP" -- starter-kit/context-budget.json | grep -i -E 'session_notes|structure|update' |
  sed 's/^upstream\/main://' | cut -c1-200 | sed 's/^/[text-budget] /' | head -4

echo
echo "# 3. #98 without its first commit: its second (3df5b0cd) and third (65990cda) commits replayed onto $UP"
echo "#    (#98 = 39825279 -> 3df5b0cd -> 65990cda; the third's parent is the second). --merge-base is each commit's own parent."
for c in 39825279 3df5b0cd 65990cda; do
  git cat-file -e "$c^{commit}" 2>/dev/null || git fetch -q upstream "pull/98/head"
done
for c in 39825279 3df5b0cd 65990cda; do
  echo "[drop-commit] $c $(git log -1 --format=%s "$c" | cut -c1-90) | files: $(git diff --name-only "$c^" "$c" | tr '\n' ' ')"
done
trial() {   # trial <commit>
  local c=$1 out rc tree f n detail=""
  out=$(git --attr-source=$EMPTY merge-tree --write-tree --name-only --merge-base="$c^" "$UP" "$c" 2>&1); rc=$?
  tree=$(printf '%s\n' "$out" | head -1)
  if [ "$rc" -eq 1 ]; then
    for f in $(printf '%s\n' "$out" | sed -n '2,/^$/p' | grep -v '^$' | sort -u); do
      n=$(git show "$tree:$f" 2>/dev/null | grep -c '^<<<<<<<'); detail="$detail $f:$n"
    done
    echo "[drop-trial] $c onto $UP: CONFLICTS (file:regions)$detail"
  elif [ "$rc" -eq 0 ]; then echo "[drop-trial] $c onto $UP: clean"
  else echo "[drop-trial] $c onto $UP: merge-tree failed rc=$rc: $(printf '%s' "$out" | head -1)"; fi
}
trial 39825279
trial 3df5b0cd
trial 65990cda
echo "# the third commit carries the second's changes in its own diff only if replayed with the second as base;"
echo "# its parent-relative diff above (65990cda^ = 3df5b0cd) is what a cherry-pick of it alone sees:"
echo "[drop-note] a conflict in a trial above is against $UP as it is today ($(git rev-parse --short=8 $UP)); #98 itself is MERGEABLE/CLEAN"
ver() { git show "$1:starter-kit/methodology_trim.py" | grep -m1 '^TRIM_VERSION' | sed 's/^TRIM_VERSION *= *"\([^"]*\)".*/\1/'; }
floor() { git show "$1:.quality-gates.json" | python3 -I -c 'import json,sys; d=json.load(sys.stdin); print([g["threshold"] for g in d["gates"] if g["name"]=="trimmer-unit-tests"][0])'; }
echo "[drop-version] methodology_trim.py TRIM_VERSION: $UP $(ver $UP); 39825279 $(ver 39825279); 3df5b0cd $(ver 3df5b0cd); 65990cda $(ver 65990cda)"
echo "[drop-floor] trimmer-unit-tests threshold (.quality-gates.json): $UP $(floor $UP); 39825279 $(floor 39825279); 3df5b0cd $(floor 3df5b0cd); 65990cda $(floor 65990cda)"
