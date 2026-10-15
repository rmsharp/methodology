#!/bin/bash
# The scrub builders' refusals, by mutation (S324). Each case copies a builder with a deliberately broken edits file to a scratch
# directory and runs it, DRY, against a clone, and the expected refusal is asserted on its text. READ-ONLY on the clone.
#   bash scrub-mutate.sh <phase-A-clone-at-5afc962> <phase-B-clone-at-the-phase-A-tip>
# Build the two clones with: scrub-run.sh <dir> C6 C7 C5 C4 C3 C2 C1   (the phase A tip) and a fresh clone of 5afc962 for the first.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
A=${1:?a clone at 5afc962 (phase A not applied)}; B=${2:?a clone at the phase A tip (phase B not applied)}
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT
mkdir -p "$W/scrub-msgs"
cp "$HERE"/scrub-build.py "$HERE"/scrub-build-b.py "$HERE"/scrub-derive-output.txt "$HERE"/scrub-derive-after-a.txt "$W/"
cp "$HERE"/scrub-msgs/*.txt "$W/scrub-msgs/"
fail=0
case_a() {   # name, sed expression over the edits, expected text, group
    sed -e "$2" "$HERE/scrub-edits.txt" > "$W/scrub-edits.txt"
    out=$(python3 -I "$W/scrub-build.py" "$A" "$4" 2>&1 | tail -1)
    if printf '%s' "$out" | grep -qF -- "$3"; then echo "ok    A $1 -> $3"; else echo "FAIL  A $1: wanted '$3', got: $out"; fail=1; fi
}
case_b() {
    sed -e "$2" "$HERE/scrub-edits-b.txt" > "$W/scrub-edits-b.txt"
    out=$(python3 -I "$W/scrub-build-b.py" "$B" "$4" 2>&1 | grep -E '^(REFUSED|dry run)' | tail -1)
    if printf '%s' "$out" | grep -qF -- "$3"; then echo "ok    B $1 -> $3"; else echo "FAIL  B $1: wanted '$3', got: $out"; fail=1; fi
}
cp "$HERE/scrub-edits.txt" "$W/scrub-edits.txt"; cp "$HERE/scrub-edits-b.txt" "$W/scrub-edits-b.txt"
out=$(python3 -I "$W/scrub-build.py" "$A" C6 2>&1 | tail -1);  [ "$out" = "dry run: nothing written" ] && echo "ok    A baseline -> dry run" || { echo "FAIL  A baseline: $out"; fail=1; }
out=$(python3 -I "$W/scrub-build-b.py" "$B" B1 2>&1 | grep -E '^(REFUSED|dry run)' | tail -1); [ "$out" = "dry run: nothing written" ] && echo "ok    B baseline -> dry run" || { echo "FAIL  B baseline: $out"; fail=1; }
# phase A (bin/sync's group, C6): an edit dropped; a token left in; a code line posing as a comment edit; a line past the end; a docstring turned into code; an indentation changed
case_a "an edit dropped"            '/^6|table/d'                                                     "neither edited nor left on purpose" C6
case_a "a fork token left in"       's/^55|# The tool that moves/55|# BL-9 The tool that moves/'      "still carries a fork token" C6
case_a "a code line as an edit"     's/^55|.*/55|MIGRATE_TOOL = "bin\/other"/'                        "NOT INERT" C6
case_a "a line past the end"        's/^6|table/99999|table/'                                         "is past the end" C6
case_a "a docstring made code"      's/^336|.*/336|    one created beside it."""; x = 1/'             "NOT INERT" C6
case_a "an indentation changed"     's/^336|    one created/336|one created/'                         "changes the line's indentation" C6
# phase B: the old text absent; the old text twice; a token left in; a flagged line neither edited nor left
case_b "the old text absent"        's/^1060| (plan 5A.2) ==>/1060| (plan 9Z.9) ==>/'                 "occurs 0 times" B1
case_b "a token left in"            's/^1122| (BL-101 P7) ==>$/1122| (BL-101 P7) ==> (BL-5)/'         "still carries a fork token" B1
case_b "a flagged line not edited"  '/^1352|/d'                                                       "neither edited nor left on purpose" B1
echo; [ $fail = 0 ] && echo "scrub-mutate: every refusal fired" || echo "scrub-mutate: A REFUSAL DID NOT FIRE"
exit $fail
