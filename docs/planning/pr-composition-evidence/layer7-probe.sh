#!/usr/bin/env bash
# PR2 Part 2, layer 7 (bin/migrate-layout): what its own suite needs from the candidate beyond the tool.
#
# Layer 6's record (section 7) left this NOT CHECKED. The probe puts the fork tip's tool and its suite into clean
# --no-local clones of the candidate (nothing is committed anywhere) in four states and runs the suite:
#
#   base      the candidate as it is                                     the WHOLE suite   (280 tests, about 6 minutes)
#   checkers  + the tip's bin/check-ledger and bin/check-handoff         the two classes that fail on base
#   docs      + the tip's framework documents (the prose layer)          the same two classes
#   both      + both                                                     the WHOLE suite
#
# The two classes are TestTheChecks and TestTheShardRehearsal (23 tests, about a minute). Each state prints its
# summary line and the sorted names of the tests that failed. Serial: the suite builds scratch git projects and
# a parallel run reads the other's load as failures (failure mode #29). Run it as
#   nohup bash layer7-probe.sh <fork-repo> <candidate-rev> <tip-rev> > layer7-probe-output.txt 2>&1 &
# and wait for its last line (`layer7-probe done`). About 14 minutes on a quiet machine.
#
# What it proves and what it does not: it shows which tests need which addition, on this machine, once. It does not show
# the suite green on a maintainer's machine, and "both" is the tip's own bytes, not the pull request's hand-built
# version of them (D5 option b carries the layout hunks of the two checkers, not their other differences).
set -u
SRC=${1:?fork repository}; CAND=${2:?candidate rev}; TIP=${3:?tip rev}
CLASSES="TestTheChecks TestTheShardRehearsal"
DOCS=$(git -C "$SRC" ls-tree -r --name-only "$TIP" -- starter-kit workstreams ITERATIVE_METHODOLOGY.md FRAMEWORK_APPARATUS.md HOW_TO_USE.md | grep '\.md$')

state() {   # state-name  checkers(0|1)  docs(0|1)  scope(whole|classes)
    local name=$1 checkers=$2 docs=$3 scope=$4 dst="$HOME/.cache/layer7-probe-$1"
    rm -rf "$dst"
    git clone --no-local -q "$SRC" "$dst" || { echo "clone failed"; return 3; }
    ( cd "$dst" || exit 3
      git checkout -q -b probe "$CAND" || exit 3
      git config --unset core.hooksPath 2>/dev/null
      for f in bin/migrate-layout tools/test_migrate_layout.py tools/test_sync_layouts.py; do
          git -C "$SRC" show "$TIP:$f" > "$f"
      done
      chmod 755 bin/migrate-layout
      if [ "$checkers" = 1 ]; then
          for f in bin/check-ledger bin/check-handoff; do git -C "$SRC" show "$TIP:$f" > "$f"; chmod 755 "$f"; done
      fi
      if [ "$docs" = 1 ]; then
          for f in $DOCS; do mkdir -p "$(dirname "$f")"; git -C "$SRC" show "$TIP:$f" > "$f"; done
      fi
      echo "== state $name: candidate $(git rev-parse --short "$CAND") + tip $(git -C "$SRC" rev-parse --short "$TIP")'s tool and suite;" \
           "checkers=$checkers docs=$docs; $(git status --short | wc -l | tr -d ' ') paths differ from the candidate; scope $scope"
      echo "   load at start: $(uptime | sed 's/.*load averages*: //')"
      local start out
      start=$(date +%s); out="$dst.out"
      if [ "$scope" = whole ]; then python3 tools/test_migrate_layout.py > "$out" 2>&1; else python3 tools/test_migrate_layout.py $CLASSES > "$out" 2>&1; fi
      echo "   exit $? in $(( $(date +%s) - start )) s"
      grep -a -E '^Ran |^OK|^FAILED' "$out" | sed 's/^/   /'
      grep -a -E '^(FAIL|ERROR): ' "$out" | sed -E 's/^(FAIL|ERROR): (\S+) \(__main__\.(\S+)\)/   failed: \3.\2/' | sort
    )
}

echo "layer7-probe: fork $(git -C "$SRC" rev-parse --short HEAD), candidate $CAND, tip $TIP; $(date -u +%Y-%m-%dT%H:%M:%SZ)"
state base     0 0 whole
state checkers 1 0 classes
state docs     0 1 classes
state both     1 1 whole
echo "layer7-probe done"
