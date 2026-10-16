#!/usr/bin/env bash
# PR4: does the pull request change what it costs a session to use the framework? Two kinds of cost, measured apart.
#   1. tokens: the files a session must read whole (the runner and SAFEGUARDS.md), by bytes, in an export of each tip,
#      as `python3 starter-kit/context_budget.py --status` reports them
#   2. clock time: the programs a session runs (the dashboard at every start, the trimmer's check, the budget tool),
#      each version of the tool run on the SAME project, alternating, three rounds; wall and CPU seconds
# The heavy project is a clone of <repo> at <candidate> (its whole history); the light one is a fresh repository of three
# commits. Writes only under <work-dir>. A timing is one machine at one load: the load average is printed with it.
#   bash docs/planning/pr-composition-evidence/pr4-cost.sh <repo> <upstream> <candidate> <work-dir>
set -u
SRC=${1:?repository holding both commits}; UP=${2:?upstream commit}; CAND=${3:?candidate commit}; W=${4:?work dir}
rm -rf "$W"; mkdir -p "$W/up" "$W/cand"
git -C "$SRC" archive "$UP" | tar -x -C "$W/up" || exit 3
git -C "$SRC" archive "$CAND" | tar -x -C "$W/cand" || exit 3
strip() { sed 's/\x1b\[[0-9;]*m//g'; }

echo "== 1. what a session must read whole: bytes, from context_budget.py --status in an export of each tip"
for t in up cand; do
  if [ "$t" = up ]; then echo "-- upstream ${UP:0:7}"; else echo "-- candidate ${CAND:0:7}"; fi
  ( cd "$W/$t" && python3 -I starter-kit/context_budget.py --status 2>&1 | strip | grep -E 'SESSION_RUNNER|SAFEGUARDS|read-set total' )
done
python3 -I - "$W" <<'PY'
import os, sys
w = sys.argv[1]
def size(t, f): return os.path.getsize(os.path.join(w, t, "starter-kit", f))
tot = {}
for f in ("SESSION_RUNNER.md", "SAFEGUARDS.md"):
    u, c = size("up", f), size("cand", f)
    tot[f] = (u, c)
    print("%-20s %6d B -> %6d B  (%+d B)" % (f, u, c, c - u))
u, c = sum(v[0] for v in tot.values()), sum(v[1] for v in tot.values())
print("both together        %6d B -> %6d B  (%+d B, %+.2f%%)" % (u, c, c - u, 100.0 * (c - u) / u))
print("at the budget tool's densities (2.81 B per token) that is about %+.0f tokens" % ((c - u) / 2.81))
PY

echo; echo "== 2. what a session runs: wall and CPU seconds, the two versions alternating, on the same project"
git clone --no-local -q "$SRC" "$W/heavy" && git -C "$W/heavy" checkout -q "$CAND" || exit 3
git init -q "$W/light"
for i in 1 2 3; do echo $i > "$W/light/f$i.txt"; git -C "$W/light" add .; git -C "$W/light" -c user.name=t -c user.email=t@example.invalid commit -q -m "c$i"; done
echo "heavy project: $(git -C "$W/heavy" rev-list --count HEAD) commits; light project: $(git -C "$W/light" rev-list --count HEAD) commits"
git -C "$SRC" show "$UP:starter-kit/methodology_dashboard.py" > "$W/dash-up.py"
git -C "$SRC" show "$CAND:starter-kit/methodology_dashboard.py" > "$W/dash-cand.py"
echo "dashboard versions: upstream $(grep -m1 '^DASHBOARD_VERSION' "$W/dash-up.py"), candidate $(grep -m1 '^DASHBOARD_VERSION' "$W/dash-cand.py")"
echo "load average at the start: $(uptime | sed 's/.*load averages*: //')"

timed() {  # $1 label, $2 directory, then the command
  local label=$1 dir=$2; shift 2
  ( cd "$dir" || exit 3
    /usr/bin/time -p "$@" > "$W/out.txt" 2> "$W/time.txt"; rc=$?
    awk -v l="$label" -v rc="$rc" '/^real/{r=$2}/^user/{u=$2}/^sys/{s=$2}END{printf "%-46s exit %s  wall %5.2f s  cpu %5.2f s\n", l, rc, r, u+s}' "$W/time.txt" )
}
dash() {  # $1 project (heavy|light), $2 version (up|cand)
  local P="$W/$1"
  git -C "$P" checkout -q -- . 2>/dev/null; git -C "$P" clean -fdq 2>/dev/null
  cp "$W/dash-$2.py" "$P/methodology_dashboard.py"
  timed "dashboard, $1 project, $2" "$P" python3 -I methodology_dashboard.py --no-open
  grep -q 'Health' "$W/out.txt" || echo "  (no health score printed: the run did not do its work)"
}
for proj in light heavy; do
  for round in 1 2 3; do dash $proj up; dash $proj cand; done
done
LEDGER="$W/heavy/CHANGELOG.md"
echo "trimmer check on a ledger of $(wc -c < "$LEDGER" | tr -d ' ') B"
for round in 1 2 3; do
  timed "trimmer --check, upstream's trimmer" "$W/up" python3 -I starter-kit/methodology_trim.py --file "$LEDGER" --check
  timed "trimmer --check, the candidate's trimmer" "$W/cand" python3 -I starter-kit/methodology_trim.py --file "$LEDGER" --check
done
for round in 1 2 3; do
  timed "context_budget --status, upstream" "$W/up" python3 -I starter-kit/context_budget.py --status
  timed "context_budget --status, candidate" "$W/cand" python3 -I starter-kit/context_budget.py --status
done
echo "load average at the end: $(uptime | sed 's/.*load averages*: //')"
echo; echo "pr4-cost done"
