#!/usr/bin/env bash
# The contrast for one layer's test file (plan section 5's "the new tests exercise the new behaviour"):
#   layer-contrast.sh <old-checkout> <new-checkout> <test-file-relative-to-checkout> [<out-dir>]
# <old-checkout> is a clean checkout of the layer's PARENT commit (the old tool and the old tests); <new-checkout> holds the
# layer (the new tool and the new tests). The new test file is copied over the old checkout's own, so it runs against the OLD
# tool, and the old file runs on the old tool as the control. Outcomes come from layer-outcomes.py (subtests counted).
# Prints: tests in each file, how many added tests fail on the old tool, whether any old test does, and the added tests that
# pass on both tools. Overwrites <test-file> in <old-checkout>: pass a scratch clone.
set -u
OLD=${1:?old checkout}; NEW=${2:?new checkout}; T=${3:?test file}; OUT=${4:-${TMPDIR:-/tmp}/layer-contrast}
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$OUT"
( cd "$OLD" && python3 "$HERE/layer-outcomes.py" "$T" ) > "$OUT/old-on-old.txt" 2>/dev/null
cp "$NEW/$T" "$OLD/$T"
( cd "$OLD" && python3 "$HERE/layer-outcomes.py" "$T" ) > "$OUT/new-on-old.txt" 2>/dev/null
( cd "$NEW" && python3 "$HERE/layer-outcomes.py" "$T" ) > "$OUT/new-on-new.txt" 2>/dev/null
python3 - "$OUT" <<'PY'
import sys
out = sys.argv[1]
def load(n):
    return dict(l.rsplit(" ", 1) for l in open("%s/%s" % (out, n)).read().splitlines() if l)
a, b, c = load("old-on-old.txt"), load("new-on-old.txt"), load("new-on-new.txt")
added = sorted(set(c) - set(a)); removed = sorted(set(a) - set(c))
bad_added = [t for t in added if b.get(t) == "bad"]
bad_old = [t for t in a if b.get(t) == "bad"]
both = [t for t in added if b.get(t) in ("ok", "skip") and c.get(t) in ("ok", "skip")]
print("tests: new file %d, old file %d, added %d, removed %d" % (len(c), len(a), len(added), len(removed)))
print("on the OLD tool: %d of the %d added tests fail or error; %d of the %d old tests do" % (len(bad_added), len(added), len(bad_old), len(a)))
print("added tests that pass on BOTH tools (%d):" % len(both))
for t in both:
    print("  " + t)
print("on the NEW tool: %d bad, %d skipped" % (sum(1 for v in c.values() if v == "bad"), sum(1 for v in c.values() if v == "skip")))
print("old tests on the old tool: %d bad, %d skipped (the control)" % (sum(1 for v in a.values() if v == "bad"), sum(1 for v in a.values() if v == "skip")))
PY
