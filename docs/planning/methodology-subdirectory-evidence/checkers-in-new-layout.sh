#!/usr/bin/env bash
# BL-101 P4 runtime check, on REAL data: this repository's own ledgers and configs, moved under methodology/
# in scratch clones the way the migration will move them, then read by the CURRENT checkers and the budget
# gate. Three trees come from one commit (nothing is written to the real repository; it is only cloned):
#
#   legacy  the repository as it is (the control: every figure below is read here first)
#   new     CHANGELOG.md, HANDOFFS.md, .context-budget.json, .context-budget-history.jsonl and
#           .quality-gates.json moved under methodology/, a runner placed there as the framework anchor
#   tie     the same, and a root file of someone else's left at each of the five old places (a product
#           changelog, a receipt file that is not a ledger, a tight budget config, a loose manifest, a history
#           line): the tools must read the methodology copies and not these
#
# For each checker the output of the new and the tie tree must equal the legacy tree's, modulo the project's
# path and the `methodology/` prefix; then a loosened floor staged in methodology/.quality-gates.json must be
# refused by the ratchet (exit 2) in both, and a change to the root manifest of someone else's must not be judged.
# Run from the repo root:   bash docs/planning/methodology-subdirectory-evidence/checkers-in-new-layout.sh
set -u
SRC="$(git rev-parse --show-toplevel)" || exit 3
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
STATE="CHANGELOG.md HANDOFFS.md .context-budget.json .context-budget-history.jsonl .quality-gates.json"

clone() { # $1 name
  git clone -q --no-local "$SRC" "$T/$1" || exit 3
  ( cd "$T/$1" && git config core.hooksPath /dev/null && git config user.email t@t && git config user.name t && git config commit.gpgsign false )
}
move() { # $1 name: the state files go under methodology/, a runner there anchors the layout
  ( cd "$T/$1" && mkdir methodology && for f in $STATE; do git mv "$f" methodology/; done \
    && cp starter-kit/SESSION_RUNNER.md methodology/SESSION_RUNNER.md \
    && python3 - methodology/.context-budget.json <<'PYEOF'
import re, sys
p = sys.argv[1]
s = open(p).read()
# What bin/migrate-layout (P7) will do: the config's files[] paths are relative to the PROJECT root, so a
# file that moved is named under methodology/ there (plan C9).
open(p, "w").write(re.sub(r'"path": "(CHANGELOG|HANDOFFS)\.md"', r'"path": "methodology/\1.md"', s))
PYEOF
  git -C "$T/$1" add -A && git -C "$T/$1" commit -q -m "move the state files under methodology/" )
}
users_own() { # $1 name: a file of someone else's at each old place (none is a ledger or a config of this tool's)
  ( cd "$T/$1" && printf '# Product changelog\n\n## 1.0\n\n- shipped\n' > CHANGELOG.md \
    && printf '# Not a receipt ledger\n\n```handoff\nsession: SX\n' > HANDOFFS.md \
    && printf '{"files": [{"path": "nothing.md", "class": "read-set", "max_bytes": 1}]}\n' > .context-budget.json \
    && printf '{"version": 1, "gates": [{"name": "theirs", "direction": "min", "threshold": 1}]}\n' > .quality-gates.json \
    && printf '{"timestamp": "2000-01-01T00:00:00Z", "files": {}}\n' > .context-budget-history.jsonl \
    && git add -A && git commit -q -m "the project's own files at the root" )
}
clone legacy; clone new; clone tie
move new; move tie; users_own tie
norm() { sed -e "s#/private##g" -e "s#$T/[a-z]*#<root>#g" -e 's#methodology/##g' -e 's/\x1b\[[0-9;]*m//g' -e 's/  */ /g'; }   # a longer path widens a table column: spacing is not a difference
printf 'commit under test: %s\n' "$(git -C "$SRC" rev-parse --short HEAD)"
printf 'new tree:  methodology/ holds %s files; the root holds %s of the five\n' \
  "$(ls -A "$T/new/methodology" | grep -cE '^(CHANGELOG.md|HANDOFFS.md|\.context-budget\.json|\.context-budget-history\.jsonl|\.quality-gates\.json)$')" \
  "$(cd "$T/new" && ls -A | grep -cE '^(CHANGELOG.md|HANDOFFS.md|\.context-budget\.json|\.context-budget-history\.jsonl|\.quality-gates\.json)$')"
printf 'tie tree:  methodology/ holds the same five, and the root holds a file of someone else'"'"'s at each: %s\n\n' \
  "$(cd "$T/tie" && ls -A | grep -cE '^(CHANGELOG.md|HANDOFFS.md|\.context-budget\.json|\.context-budget-history\.jsonl|\.quality-gates\.json)$')"

rc=0
run() { # $1 label, then the command, run in each tree; the legacy output is the control
  local label="$1"; shift
  for t in legacy new tie; do ( cd "$T/$t" && "$@" 2>&1 | norm > "$T/out-$t.txt" ); done
  local n=1 same=1
  cmp -s "$T/out-legacy.txt" "$T/out-new.txt" || same=0
  cmp -s "$T/out-legacy.txt" "$T/out-tie.txt" || n=0
  printf '== %s ==\n' "$label"
  printf '   legacy: %s\n' "$(grep -m1 . "$T/out-legacy.txt" | cut -c1-160)"
  printf '   new identical to legacy: %s   tie identical to legacy: %s   (output %s lines)\n' \
    "$([ $same = 1 ] && echo yes || echo NO)" "$([ $n = 1 ] && echo yes || echo NO)" "$(wc -l < "$T/out-legacy.txt" | tr -d ' ')"
  if [ $same = 0 ]; then diff "$T/out-legacy.txt" "$T/out-new.txt" | head -6 | sed 's/^/     new  | /' | cut -c1-170; rc=1; fi
  if [ $n = 0 ]; then diff "$T/out-legacy.txt" "$T/out-tie.txt" | head -6 | sed 's/^/     tie  | /' | cut -c1-170; rc=1; fi
}
run "bin/check-ledger --all"                 python3 -B "$SRC/bin/check-ledger" --all
run "bin/check-handoff --all --allow-pending" python3 -B "$SRC/bin/check-handoff" --all --allow-pending
run "bin/check-overhead"                     python3 -B "$SRC/bin/check-overhead"
run "bin/model-report --no-git"              python3 -B "$SRC/bin/model-report" --no-git
run "context_budget.py --status"             python3 -B "$SRC/starter-kit/context_budget.py" --status
echo

# The ratchet, through its --precommit, on the real manifest: a loosened floor in the methodology copy is
# refused in both trees, and an edit to the root manifest of someone else's is not judged (the tie tree).
loosen() { # $1 tree, $2 file: lower the first floor declared there by one, staged
  ( cd "$T/$1" && python3 - "$2" <<'PYEOF'
import json, sys
p = sys.argv[1]
cfg = json.load(open(p))
g = next(g for g in cfg["gates"] if g.get("direction") == "min" and g["threshold"] > 1)
g["threshold"] -= 1
json.dump(cfg, open(p, "w"), indent=2)
PYEOF
    git add "$2" )
}
for t in new tie; do
  loosen "$t" methodology/.quality-gates.json
  out="$(cd "$T/$t" && python3 -B "$SRC/starter-kit/quality_ratchet.py" --precommit 2>&1 | sed 's/\x1b\[[0-9;]*m//g')"
  r="$(cd "$T/$t" && python3 -B "$SRC/starter-kit/quality_ratchet.py" --precommit >/dev/null 2>&1; echo $?)"
  printf '%s: loosened methodology/.quality-gates.json -> exit %s: %s\n' "$t" "$r" "$(printf '%s' "$out" | grep -m1 -o 'floor lowered[^—]*' | cut -c1-80)"
  [ "$r" = 2 ] || rc=1   # the ratchet's REFUSED
  ( cd "$T/$t" && git reset -q HEAD -- methodology/.quality-gates.json && git checkout -q -- methodology/.quality-gates.json )
done
( cd "$T/tie" && printf '{"version": 1, "gates": [{"name": "theirs", "direction": "min", "threshold": 0}]}\n' > .quality-gates.json && git add .quality-gates.json )
r="$(cd "$T/tie" && python3 -B "$SRC/starter-kit/quality_ratchet.py" --precommit >/dev/null 2>&1; echo $?)"
printf 'tie: the root manifest of someone else'"'"'s lowered (1 -> 0) -> exit %s (not judged)\n' "$r"
[ "$r" = 0 ] || rc=1
echo
printf 'result: %s\n' "$([ $rc = 0 ] && echo 'every comparison held' || echo 'A COMPARISON FAILED')"
exit $rc
