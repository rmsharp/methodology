#!/usr/bin/env bash
# Runs E1-E7 of body-check-expectations.txt against pr4-body-check.py and judges each one.
#
#   bash docs/planning/pr-composition-evidence/body-check-run.sh <scratch-dir>      (from the repository root)
#
# Read-only toward the repository; writes only under <scratch-dir>. The old script is the committed blob 7733b493f116,
# so the comparison needs no copy kept outside git. Exit status = the number of expectations that failed.
set -u
W=${1:?usage: body-check-run.sh <scratch-dir>}
mkdir -p "$W"
S=docs/planning/pr-composition-evidence/pr4-body-check.py
D=docs/planning/upstream-pr-body.md
C=47637be21425
U=d50ce290d921
THREE="65990cd c8b9ddd e7b389f"
HEADSHA=$(git rev-parse --short=7 HEAD)
fails=0
judge() {   # judge <id> <description> <0|1: condition holds>
    if [ "$3" = 1 ]; then echo "PASS $1  $2"; else echo "FAIL $1  $2"; fails=$((fails + 1)); fi
}
run() {     # run <out-file> <script> <args...>; prints nothing, sets RC
    local out=$1; shift
    python3 "$@" > "$out" 2>&1
    RC=$?
}

git cat-file blob 7733b493f116 > "$W/old.py" || { echo "cannot read the old blob 7733b493f116"; exit 99; }
git merge-base --is-ancestor "$HEADSHA" "$C" && { echo "HEAD $HEADSHA is inside the candidate; the negative control needs one outside"; exit 99; }

run "$W/old.txt" "$W/old.py" "$D" "$C" "$U"; OLDRC=$RC
echo "old script on the posted draft: exit $OLDRC, $(grep -c 'in upstream..candidate: True' "$W/old.txt") True, $(grep -c 'in upstream..candidate: False' "$W/old.txt") False"

# E1: no extras
run "$W/e1.txt" "$S" "$D" "$C" "$U"; R1=$RC
n=$(grep -c 'OUTSIDE and not allowed' "$W/e1.txt")
ok=1; [ "$R1" = 1 ] || ok=0; [ "$n" = 3 ] || ok=0
for h in $THREE; do grep -q "hash \`$h\` .*OUTSIDE and not allowed" "$W/e1.txt" || ok=0; done
grep -q "hash \`d50ce29\` .*allowed (upstream's tip)" "$W/e1.txt" || ok=0
judge E1 "no extras: exit 1 (got $R1), three outside (got $n): $THREE; d50ce29 allowed as upstream's tip" $ok

# E2: the three as extras
run "$W/e2.txt" "$S" "$D" "$C" "$U" $THREE; R2=$RC
ok=1; [ "$R2" = 0 ] || ok=0
[ "$(grep -c 'OUTSIDE' "$W/e2.txt")" = 0 ] || ok=0
[ "$(grep -c 'allowed (named on the command line)' "$W/e2.txt")" = 3 ] || ok=0
judge E2 "three extras: exit 0 (got $R2), no outside line, three 'named on the command line'" $ok

# E3: only the four False lines differ from the old output
changed=$(diff "$W/old.txt" "$W/e2.txt" | grep -c '^>')
removed=$(diff "$W/old.txt" "$W/e2.txt" | grep -c '^<')
ok=1; [ "$OLDRC" = 0 ] || ok=0; [ "$changed" = 4 ] || ok=0; [ "$removed" = 4 ]  || ok=0
diff "$W/old.txt" "$W/e2.txt" | grep '^>' | grep -qv 'in upstream..candidate: False; allowed (' && ok=0
judge E3 "against the old output only the four False lines changed (old exit $OLDRC; $removed removed, $changed added)" $ok

# E4: negative control, a hash outside the range that the body cites, the three extras given
cp "$D" "$W/neg.md"
printf '\nA further hash the branch does not hold: `%s`.\n' "$HEADSHA" >> "$W/neg.md"
run "$W/e4.txt" "$S" "$W/neg.md" "$C" "$U" $THREE; R4=$RC
n=$(grep -c 'OUTSIDE and not allowed' "$W/e4.txt")
ok=1; [ "$R4" = 1 ] || ok=0; [ "$n" = 1 ] || ok=0
grep -q "hash \`$HEADSHA\` .*OUTSIDE and not allowed" "$W/e4.txt" || ok=0
judge E4 "negative control (\`$HEADSHA\`, outside the range): exit 1 (got $R4), exactly that one outside (got $n)" $ok

# E5: an extra that does not resolve fails; an extra that resolves but is not cited prints and passes
run "$W/e5a.txt" "$S" "$D" "$C" "$U" $THREE deadbee; R5a=$RC
run "$W/e5b.txt" "$S" "$D" "$C" "$U" $THREE "$HEADSHA"; R5b=$RC
ok=1; [ "$R5a" = 1 ] || ok=0; grep -q "UNRESOLVED allowed hash 'deadbee'" "$W/e5a.txt" || ok=0
[ "$R5b" = 0 ] || ok=0; grep -q "allowed hash '$HEADSHA' is not cited in the body" "$W/e5b.txt" || ok=0
judge E5 "unresolved extra: exit 1 (got $R5a); uncited extra: exit 0 (got $R5b) with its line" $ok

# E6: an in-range hash also named as an extra changes nothing
run "$W/e6.txt" "$S" "$D" "$C" "$U" $THREE 1477af2; R6=$RC
ok=1; [ "$R6" = 0 ] || ok=0
[ "$(grep 'hash `1477af2`' "$W/e6.txt")" = "$(grep 'hash `1477af2`' "$W/old.txt")" ] || ok=0
judge E6 "in-range hash named as an extra: exit 0 (got $R6), its line equals the old script's" $ok

# E7: fewer than three arguments fails the same way as before
python3 "$W/old.py" "$D" "$C" > "$W/e7-old.txt" 2>&1; RO=$?
python3 "$S" "$D" "$C" > "$W/e7-new.txt" 2>&1; RN=$?
ok=1; [ "$RO" != 0 ] || ok=0; [ "$RN" = "$RO" ] || ok=0
grep -q ValueError "$W/e7-old.txt" || ok=0; grep -q ValueError "$W/e7-new.txt" || ok=0
judge E7 "two arguments: old exit $RO, new exit $RN, both a ValueError from the unpacking" $ok

echo "expectations failed: $fails"
exit "$fails"
