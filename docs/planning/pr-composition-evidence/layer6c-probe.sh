#!/usr/bin/env bash
# PR2 Part 2, the prose layer: does the LAYOUT-ONLY prose make the migration tool's own suite pass?
#
# Two earlier probes answered half of this. layer7-probe.sh put the tip's WHOLE framework documents into the candidate and the
# whole 280-test suite passed (with the tip's whole checkers); layer6b-probe.sh did the same with the checkers' layer and the
# tip's whole documents. Neither could say whether the layout hunks alone are enough, because the tip's documents carry text that
# is not layout (a session number, the unmeasured-gate clause, issue #75's plan-surface rule, a model-tag sentence). This probe
# runs the migration tool and its suites on the candidate at two commits:
#
#   parent   the checkers' layer, no prose        the two classes that hold the failures (23 tests; the contrast)
#   layer    the prose layer's last commit        the WHOLE suite (280 tests, about 6 minutes)
#
# Expected: `parent` fails the same 10 tests as layer6b-probe's `layer` state, and `layer` runs 280 OK. A different outcome on
# `layer` means a hunk this layer leaves out is one the tool reads. Serial, as every probe. Run as
#   nohup bash layer6c-probe.sh <fork-repo> <candidate-repo> <parent-commit> <layer-commit> <tip-rev> <scratch-dir> > layer6c-probe-output.txt 2>&1 &
# and wait for the last line (`layer6c-probe done`).
set -u
FORK=${1:?fork repository}; CAND=${2:?candidate repository}; PARENT=${3:?parent commit}; LAYER=${4:?layer commit}; TIP=${5:?tip rev}; OUT=${6:?scratch dir}
CLASSES="TestTheChecks TestTheShardRehearsal"

state() {   # state-name  commit  scope(whole|classes)
    local name=$1 commit=$2 scope=$3 dst="$OUT/layer6c-probe-$1"
    rm -rf "$dst"
    git clone --no-local -q "$CAND" "$dst" || { echo "clone failed"; return 3; }
    ( cd "$dst" || exit 3
      git checkout -q "$commit" || exit 3
      git config --unset core.hooksPath 2>/dev/null
      for f in bin/migrate-layout tools/test_migrate_layout.py tools/test_sync_layouts.py; do
          git -C "$FORK" show "$TIP:$f" > "$f"
      done
      chmod 755 bin/migrate-layout
      echo "== state $name: $(git rev-parse --short HEAD) + tip $(git -C "$FORK" rev-parse --short "$TIP")'s tool and suite;" \
           "$(git status --short | wc -l | tr -d ' ') paths differ from the commit; scope $scope"
      echo "   load at start: $(uptime | sed 's/.*load averages*: //')"
      local start out
      start=$(date +%s); out="$dst.out"
      if [ "$scope" = whole ]; then python3 tools/test_migrate_layout.py > "$out" 2>&1; else python3 tools/test_migrate_layout.py $CLASSES > "$out" 2>&1; fi
      echo "   exit $? in $(( $(date +%s) - start )) s"
      grep -a -E '^Ran |^OK|^FAILED' "$out" | sed 's/^/   /'
      grep -a -E '^(FAIL|ERROR): ' "$out" | sed -E 's/^(FAIL|ERROR): ([^ ]+) \(__main__\.([^)]+)\)/   failed: \3.\2/' | sort
    )
}

echo "layer6c-probe: fork $(git -C "$FORK" rev-parse --short HEAD), parent $PARENT, layer $LAYER, tip $TIP; $(date -u +%Y-%m-%dT%H:%M:%SZ)"
state parent "$PARENT" classes
state layer  "$LAYER"  whole
echo "layer6c-probe done"
