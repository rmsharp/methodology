#!/usr/bin/env bash
# PR2 Part 2, the checkers' layer: does the HAND-BUILT layout reading make the migration tool's own suite pass?
#
# The earlier probe (layer7-probe.sh) put the tip's WHOLE bin/check-ledger and bin/check-handoff into the candidate: it showed the tool's
# suite needs the checkers AND the prose, and left "which hunks make the 280 pass" NOT CHECKED. This probe answers it for the layer built
# in this session: the candidate at the layer's LAST COMMIT (so the hand-built checkers, not the tip's), plus the fork tip's tool, its
# suite and its sync suite, in two states:
#
#   layer         the layer, no prose                                          the two classes that hold the failures (23 tests)
#   layer+docs    the layer + the tip's framework documents (the prose layer)  the WHOLE suite (280 tests, about 6 minutes)
#
# Expected from the earlier probe: `layer` fails the same 10 tests as the whole-file `checkers` state (the prose is what they need), and
# `layer+docs` runs 280 OK. A different outcome means the hand-built hunks differ from the tip's in something the tool reads.
# Serial, as every probe: the suite builds scratch git projects and a parallel run reads the other's load as failures. Run as
#   nohup bash layer6b-probe.sh <fork-repo> <candidate-repo> <layer-commit> <tip-rev> <scratch-dir> > layer6b-probe-output.txt 2>&1 &
# and wait for the last line (`layer6b-probe done`).
set -u
FORK=${1:?fork repository}; CAND=${2:?candidate repository}; COMMIT=${3:?layer commit}; TIP=${4:?tip rev}; OUT=${5:?scratch dir}
CLASSES="TestTheChecks TestTheShardRehearsal"
DOCS=$(git -C "$FORK" ls-tree -r --name-only "$TIP" -- starter-kit workstreams ITERATIVE_METHODOLOGY.md FRAMEWORK_APPARATUS.md HOW_TO_USE.md | grep '\.md$')

state() {   # state-name  docs(0|1)  scope(whole|classes)
    local name=$1 docs=$2 scope=$3 dst="$OUT/layer6b-probe-$1"
    rm -rf "$dst"
    git clone --no-local -q "$CAND" "$dst" || { echo "clone failed"; return 3; }
    ( cd "$dst" || exit 3
      git checkout -q "$COMMIT" || exit 3
      git config --unset core.hooksPath 2>/dev/null
      for f in bin/migrate-layout tools/test_migrate_layout.py tools/test_sync_layouts.py; do
          git -C "$FORK" show "$TIP:$f" > "$f"
      done
      chmod 755 bin/migrate-layout
      if [ "$docs" = 1 ]; then
          for f in $DOCS; do mkdir -p "$(dirname "$f")"; git -C "$FORK" show "$TIP:$f" > "$f"; done
      fi
      echo "== state $name: layer $(git rev-parse --short HEAD) + tip $(git -C "$FORK" rev-parse --short "$TIP")'s tool and suite;" \
           "docs=$docs; $(git status --short | wc -l | tr -d ' ') paths differ from the layer; scope $scope"
      echo "   load at start: $(uptime | sed 's/.*load averages*: //')"
      local start out
      start=$(date +%s); out="$dst.out"
      if [ "$scope" = whole ]; then python3 tools/test_migrate_layout.py > "$out" 2>&1; else python3 tools/test_migrate_layout.py $CLASSES > "$out" 2>&1; fi
      echo "   exit $? in $(( $(date +%s) - start )) s"
      grep -a -E '^Ran |^OK|^FAILED' "$out" | sed 's/^/   /'
      grep -a -E '^(FAIL|ERROR): ' "$out" | sed -E 's/^(FAIL|ERROR): ([^ ]+) \(__main__\.([^)]+)\)/   failed: \3.\2/' | sort
    )
}

echo "layer6b-probe: fork $(git -C "$FORK" rev-parse --short HEAD), layer $COMMIT, tip $TIP; $(date -u +%Y-%m-%dT%H:%M:%SZ)"
state layer      0 classes
state layer-docs 1 whole
echo "layer6b-probe done"
