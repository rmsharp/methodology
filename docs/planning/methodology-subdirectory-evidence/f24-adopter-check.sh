#!/bin/bash
# BL-101 F24 (S299): the tool's reading of `.vscodeignore` against real `vsce ls`, on the adopter the finding came from.
# `vscode_quarto_ext` at 507b9348 (the commit before P17), cloned with --no-local into SCRATCH (a path WITHOUT the word
# "scratchpad": its `.vscodeignore` has `scratchpad/**` and vsce lists nothing under such a path, F23). The real repository is
# only cloned and read. Arms, each synced with bin/sync (no --force) and committed with a ledger entry in its own format:
#   t1     --tier 1, the .vscodeignore as the adopter had it
#   tall   --tier all, the same
#   tallA  --tier all after the adopter's own remedy, `methodology/**` in its own commit (9a53b909 there)
# For each: the tool's dry run (JSON) before the move, `vsce ls` before and after a real --apply in the clone, and the
# comparison: the files the tool says are exposed, against the moved files vsce did not list at their old place and lists at
# the new one. Usage: SCRATCH=$HOME/.cache/f24 f24-adopter-check.sh
set -u
S=${SCRATCH:?set SCRATCH to a directory whose path does not contain "scratchpad"}
case "$S" in *scratchpad*) echo "SCRATCH must not contain scratchpad"; exit 9;; esac
R=$S/adopter-check
A=$HOME/Development/vscode_quarto_ext
M=$HOME/Development/methodology
BASE=507b9348
TRAILER='Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>'
rm -rf "$R"; mkdir -p "$R"
exec > "$R/log.txt" 2>&1
printf 'start %s\nadopter %s (base %s)\nmethodology HEAD %s\n' "$(date)" "$(git -C "$A" rev-parse --short HEAD)" "$BASE" "$(git -C "$M" rev-parse --short HEAD)"
printf 'vsce %s, minimatch %s\n' "$(node -p 'require(process.argv[1]).version' "$A/node_modules/@vscode/vsce/package.json")" "$(node -p 'require(process.argv[1]).version' "$A/node_modules/minimatch/package.json")"

ledger_entry() {  # a hand-written entry in the adopter's own format, newest on top under its first month heading
  python3 - "$1" "$2" <<'PYEOF'
import sys
p, title = sys.argv[1:3]
t = open(p, encoding="utf-8").read()
anchor = "## 2026-09\n\n"
assert t.count(anchor) == 1, "anchor not found exactly once in %s" % p
entry = ("### 2026-10-12 · [ad hoc] %s\n- **Change:** %s.\n- **Commit/PR:** the commit that ships this entry\n"
         "- **Session:** F24 check · **Verified:** n/a\n- **Model:** Claude Sonnet 5.5\n\n" % (title, title))
open(p, "w", encoding="utf-8").write(t.replace(anchor, anchor + entry, 1))
PYEOF
}
commit_all() { git -C "$1" add -A; git -C "$1" commit -q -m "$2" > /dev/null 2>&1; printf 'commit %s (%s) exit=%s\n' "$(basename "$1")" "$2" "$?"; }
vsce_ls() { ( cd "$1" && node_modules/.bin/vsce ls 2>/dev/null | sort ); }

for n in t1 tall tallA; do
  git clone -q --no-local "$A" "$R/$n" && git -C "$R/$n" checkout -q "$BASE"
  /bin/cp -Rc "$A/node_modules" "$R/$n/node_modules"
  /bin/cp -Rc "$A/dist" "$R/$n/dist" 2>/dev/null
  if [ "$n" = tallA ]; then
    printf '\n# Methodology: the directory the framework files move to (BL-101 P17); vsce matches without matchBase, so a bare name is the root only.\nmethodology/**\n' >> "$R/$n/.vscodeignore"
    ledger_entry "$R/$n/CHANGELOG.md" "Deny methodology/ in .vscodeignore"
    commit_all "$R/$n" "chore(vsix): deny methodology/ in .vscodeignore, before the move"
  fi
  "$M/bin/sync" "$R/$n" > "$R/$n.sync.txt" 2>&1; printf 'sync %s exit=%s\n' "$n" "$?"
  ledger_entry "$R/$n/CHANGELOG.md" "Methodology sync"
  commit_all "$R/$n" "chore(methodology): sync"
done

for n in t1 tall tallA; do
  t=all; [ "$n" = t1 ] && t=1
  vsce_ls "$R/$n" > "$R/$n.before.txt"
  "$M/bin/migrate-layout" "$R/$n" --tier $t --json > "$R/$n.dry.json" 2> "$R/$n.dry.err"; printf '%s dry run (tier %s) exit=%s\n' "$n" "$t" "$?"
  "$M/bin/migrate-layout" "$R/$n" --tier $t > "$R/$n.dry.txt" 2>&1
  "$M/bin/migrate-layout" "$R/$n" --tier $t --apply --skip-checks --trailer "$TRAILER" > "$R/$n.apply.txt" 2>&1; printf '%s apply exit=%s\n' "$n" "$?"
  vsce_ls "$R/$n" > "$R/$n.after.txt"
  python3 - "$R" "$n" <<'PYEOF'
import json, os, sys
R, n = sys.argv[1:3]
rep = json.load(open("%s/%s.dry.json" % (R, n)))
before = set(open("%s/%s.before.txt" % (R, n)).read().split("\n")) - {""}
after = set(open("%s/%s.after.txt" % (R, n)).read().split("\n")) - {""}
moves = {m["src"]: m["dest"] for m in rep["moves"]}
row = next((x for x in rep["not_rewritten"]["config"]["paths"] if x["file"] == ".vscodeignore"), None)
tool = set((row or {}).get("patterns", {}).get("exposed", [])) & set(moves)
unread = (row or {}).get("patterns", {}).get("unread")
# a moved file is exposed when vsce did not list it where it was and lists it where it went (the file existed at its old place)
vsce = {s for s, d in moves.items() if s not in before and d in after and os.path.exists("%s/%s/%s" % (R, n, d))}
only_tool, only_vsce = sorted(tool - vsce), sorted(vsce - tool)
print("%s: vsce lists %d paths before and %d after; %d moves; the tool says %d exposed, vsce says %d%s" %
      (n, len(before), len(after), len(moves), len(tool), len(vsce), "" if unread is None else " (lines not read: %d)" % unread))
print("%s: tool and vsce agree" % n if not (only_tool or only_vsce) else "%s: DISAGREE tool-only %s vsce-only %s" % (n, only_tool, only_vsce))
PYEOF
done
printf 'end %s\n' "$(date)"
