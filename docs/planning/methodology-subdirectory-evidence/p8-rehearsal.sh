#!/usr/bin/env bash
# BL-101 P8 -- the rehearsal of THIS repository's own move, in scratch clones, shipping nothing.
# Two --no-local clones of the SAME commit: U (unmoved, the control) and M (moved by bin/migrate-layout).
# The real repository is only cloned and read. Stages (P8_STAGES selects; the default is all, in this order):
#   tool     the tool as written on this repository (its refusal, P8's first finding), then the tool with the
#            one inapplicable precondition suppressed (p8-apply-tool.py): dry run, apply through the hooks,
#            the tool's own before-and-after checks
#   proofs   every tracked *.verify.sh run in U and in M: exit-code histogram, and any proof that differs
#   trim     one real trim of each ledger in the new layout, hooks ON: dry run, write, the proof before the
#            commit, after it, from a second --no-local clone, and --reverify
#   hook     the X2 test: a later commit after the move that does not touch the ledger is REFUSED (and one that
#            co-stages the ledger passes); the control in U
#   dash     the dashboard on U and on M: the same card?
#   resync   plan 5A.4 re-run with the tool's own move against the current upstream/main
#   suites   plan 3.1: `bash bin/tests.sh` in U and in M, serially; the triples must be equal
#   ratchet  `quality_ratchet.py --run` in U and in M (the gates, including the gate commands the tool rewrote)
# Run from the repo root, on a committed tree (the base is HEAD):
#   bash docs/planning/methodology-subdirectory-evidence/p8-rehearsal.sh > p8-rehearsal-output.txt
# Takes about forty minutes; P8_KEEP=1 keeps the scratch directory, P8_STAGES="tool proofs" runs part of it.
set -u
# The disclosure hook (.githooks/commit-msg) is not what is measured; the tool's apply passes a trailer anyway.
export METHODOLOGY_REQUIRE_COAUTHOR=0
SRC="$(git rev-parse --show-toplevel)" || exit 3
EV="$SRC/docs/planning/methodology-subdirectory-evidence"
BASE="$(git -C "$SRC" rev-parse HEAD)"
UPSTREAM="$(git -C "$SRC" rev-parse upstream/main)" || { echo "needs the ref upstream/main"; exit 3; }
STAGES="${P8_STAGES:-tool proofs trim hook dash resync suites ratchet}"
T="$(mktemp -d)"; [ -n "${P8_KEEP:-}" ] || trap 'rm -rf "$T"' EXIT
want() { case " $STAGES " in *" $1 "*) return 0 ;; esac; return 1; }
mk() {  # mk <dir> [<commit>]: a --no-local clone at a commit, hooks ON, a committer
  rm -rf "$1"; git clone -q --no-local "$SRC" "$1" && git -C "$1" checkout -q "${2:-$BASE}" || return 1
  git -C "$1" config core.hooksPath .githooks; git -C "$1" config user.email t@t
  git -C "$1" config user.name t; git -C "$1" config commit.gpgsign false
}
nospace() { tr -d ' '; }
TRAILER='Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>'
h() { printf '\n== %s ==\n' "$1"; }

printf 'BL-101 P8 rehearsal. base commit %s; upstream/main %s\n' "$(git -C "$SRC" rev-parse --short "$BASE")" "$(git -C "$SRC" rev-parse --short "$UPSTREAM")"
printf 'stages: %s\n' "$STAGES"
mk "$T/U" || exit 3; mk "$T/M" || exit 3
printf 'root entries (ls -A, without .git): unmoved %s\n' "$(ls -A "$T/U" | grep -vc '^\.git$')"

APPLIED=0
if want tool; then
  h "1. the tool as written, on a scratch clone of this repository"
  for tier in all 2; do
    python3 "$T/M/bin/migrate-layout" --tier "$tier" "$T/M" > "$T/raw-$tier.txt" 2>&1; rc=$?
    printf -- '--tier %s: exit %s, "layout:" line: %s\n' "$tier" "$rc" "$(grep -m1 '^layout:' "$T/raw-$tier.txt")"
    grep '^  - \[' "$T/raw-$tier.txt" | cut -c1-150 | sed 's/^/   /'
    printf '   (missing) rows in the [not-current] refusal: %s\n' "$(grep '^  - \[not-current\]' "$T/raw-$tier.txt" | grep -o '(missing)' | wc -l | nospace)"
  done
  h "1b. the tool with ONE precondition suppressed (p8-apply-tool.py: read_status reports no rows), dry run"
  python3 "$EV/p8-apply-tool.py" "$T/M/bin/migrate-layout" --json "$T/M" > "$T/dry.json" 2> "$T/dry.err"; rc=$?
  printf 'exit %s; %s\n' "$rc" "$(cat "$T/dry.err")"
  python3 -I - "$T/dry.json" <<'PYEOF'
import json, sys
r = json.load(open(sys.argv[1]))
print("status %s; refusals %d; layout read as %s; tier %s" % (r["status"], len(r["refusals"]), r["layout"], r["tier"]))
kinds = {}
for m in r["moves"]:
    kinds[m["kind"]] = kinds.get(m["kind"], 0) + 1
print("moves %d: %s" % (len(r["moves"]), ", ".join("%s %d" % kv for kv in sorted(kinds.items()))))
print("   the instance files:", ", ".join(m["src"] for m in r["moves"] if m["kind"] != "shard"))
print("left in place (%d):" % len(r["left_in_place"]))
for x in r["left_in_place"]:
    print("   %s -- %s" % (x["path"], x["reason"]))
print("rewrites (path -> final, replacements):")
for x in r["rewrites"]:
    print("   %s -> %s, %d" % (x["path"], x["final"], x["replacements"]))
print("shard rehearsal: ran %s, proofs %d, excluded %d" % (r["rehearsal"]["ran"], r["rehearsal"]["proofs"], len(r["rehearsal"]["excluded"])))
print("hits left, by kind: " + "; ".join("%s %d mentions in %d files" % (k, v["mentions"], v["files"]) for k, v in r["not_rewritten"].items()))
hooks = r["not_rewritten"].get("hooks", {})
print("hooks that run the moved tool: %s; hook files: %s" % (hooks.get("runs_moved_tool"), sorted({s["file"] for s in hooks.get("sites", [])})))
PYEOF
  h "1c. the apply: ONE commit through the clone's hooks, then the tool's own before-and-after checks"
  python3 "$EV/p8-apply-tool.py" "$T/M/bin/migrate-layout" --apply --trailer "$TRAILER" --json "$T/M" > "$T/apply.json" 2> "$T/apply.err"; rc=$?
  printf 'exit %s (0 = applied and the checks agree; 3 = rolled back; 4 = applied, a check differs)\n' "$rc"
  python3 -I - "$T/apply.json" <<'PYEOF'
import json, sys
r = json.load(open(sys.argv[1]))
print("status %s" % r["status"])
c = r.get("commit") or {}
if "error" in c:
    print("commit error:", c["error"][:600])
if "sha" in c:
    scores = sorted(x["score"] for x in c["renames"])
    print("commit %s on parent %s; %d moves recorded as renames; lowest similarity %d%%, median %d%%" % (c["sha"][:7], c["parent"][:7], len(scores), scores[0], scores[len(scores) // 2]))
ch = r.get("checks") or {}
if ch.get("ran"):
    print("checks ok: %s; differences: %s; clean tree after: %s; informational: %s" % (ch["ok"], ch["differences"], ch["clean"], ch["informational"]))
    for k in ("status", "ledger", "handoff", "links", "proofs", "history"):
        print("   %-8s before %s | after %s" % (k, json.dumps(ch["before"][k]), json.dumps(ch["after"][k])))
PYEOF
  [ "$rc" = 0 ] && [ "$(git -C "$T/M" rev-parse HEAD)" != "$BASE" ] && APPLIED=1
  printf 'M after the apply: %s; the migration commit is the only commit past the base: %s\n' "$(git -C "$T/M" rev-parse --short HEAD)" "$(git -C "$T/M" rev-list --count "$BASE"..HEAD | nospace)"
  printf 'root entries (ls -A, without .git): moved %s\n' "$(ls -A "$T/M" | grep -vc '^\.git$')"
  printf 'a root CHANGELOG.md / HANDOFFS.md / .quality-gates.json remains in M: %s\n' "$(cd "$T/M" && ls CHANGELOG.md HANDOFFS.md .quality-gates.json .context-budget.json 2>/dev/null | wc -l | nospace)"
  printf 'git log --follow reaches the ledger history from the new path: %s commits (the unmoved ledger, by path: %s)\n' \
    "$(git -C "$T/M" log --follow --format=%H -- methodology/CHANGELOG.md | wc -l | nospace)" "$(git -C "$T/U" log --follow --format=%H -- CHANGELOG.md | wc -l | nospace)"
fi

if [ "$APPLIED" != 1 ]; then
  want tool && printf '\nthe apply did not land, so the stages that need the moved tree stop here\n' && exit 1
  printf '\n(no "tool" stage in this run: the stages that need the moved tree cannot run)\n'; exit 1
fi
MV="$(git -C "$T/M" rev-parse HEAD)"

if want proofs; then
  h "2. every tracked *.verify.sh, run in the unmoved clone and in the moved one"
  run_proofs() { ( cd "$1" && git ls-files '*.verify.sh' | sort | while read -r f; do bash "$f" > /dev/null 2>&1; printf '%s\t%s\n' "$?" "$(basename "$f")"; done ) > "$2"; }
  run_proofs "$T/U" "$T/pu.txt"; run_proofs "$T/M" "$T/pm.txt"
  for d in u m; do
    printf '%-9s proofs=%s  ' "$([ $d = u ] && echo unmoved || echo moved)" "$(wc -l < "$T/p$d.txt" | nospace)"
    cut -f1 "$T/p$d.txt" | sort | uniq -c | awk '{printf "exit%s x%s  ", $2, $1}'; printf '\n'
  done
  printf 'proofs whose exit code differs, unmoved vs moved: %s\n' \
    "$(join -t"$(printf '\t')" -j2 <(sort -k2 "$T/pu.txt") <(sort -k2 "$T/pm.txt") | awk -F'\t' '$2!=$3' | wc -l | nospace)"
  printf 'proofs present in only one of the two: %s\n' "$(join -t"$(printf '\t')" -j2 -v1 -v2 <(sort -k2 "$T/pu.txt") <(sort -k2 "$T/pm.txt") | wc -l | nospace)"
  printf 'the unmoved clone'"'"'s exit-1 proofs (pre-existing, the BL-36 class):\n'; awk -F'\t' '$1 == 1 {print "   " $2}' "$T/pu.txt"
fi

if want trim; then
  h "3. one real trim of each ledger in the new layout, hooks ON"
  mk "$T/MT" "$MV" || exit 3
  TOOL="$T/MT/starter-kit/methodology_trim.py"
  printf 'tool: %s\n' "$(python3 "$TOOL" --version)"
  rc_all=0
  for spec in "HANDOFFS.md KEEP2" "CHANGELOG.md HALF"; do
    set -- $spec; name="$1"; f="methodology/$1"
    if [ "$2" = KEEP2 ]; then keep=2; else keep=$(( $(grep -c '^### ' "$T/MT/$f") / 2 )); fi
    printf '\n-- %s (keep %s records of %s) --\n' "$f" "$keep" "$(grep -c "$([ "$name" = HANDOFFS.md ] && echo '^```handoff' || echo '^### ')" "$T/MT/$f")"
    ( cd "$T/MT" && python3 "$TOOL" --file "$f" --cut "$keep" --force | grep -E '^\s+\[(DRY_RUN|L1_OK|L2_OK|L3_OK|LAYOUT_|TRANSFORM_)' | sed 's/^ *//' | cut -c1-170 )
    ( cd "$T/MT" && python3 "$TOOL" --file "$f" --cut "$keep" --force --write > "$T/write.txt" 2>&1 ); wrc=$?
    printf 'write exit %s\n' "$wrc"
    grep -E '\[(WROTE|P1A_OK|L1_OK|L2_OK|L3_OK)\]' "$T/write.txt" | sed 's/^ *//' | cut -c1-150
    shard="$(cd "$T/MT" && git status --short -uall | awk '/^\?\? methodology\/archive\/.*[^h]\.md$/ {print $2}' | head -1)"
    [ -n "$shard" ] || { echo "FAIL: no shard under methodology/archive/ was written"; sed 's/^/    | /' "$T/write.txt" | cut -c1-200 | head -8; rc_all=1; continue; }
    printf 'shard: %s (%s B)\n' "$shard" "$(wc -c < "$T/MT/$shard" | nospace)"
    printf 'files written outside methodology/ (the trim): %s\n' "$(cd "$T/MT" && git status --short -uall | awk '{print $2}' | grep -vc '^methodology/')"
    ( cd "$T/MT" && bash "$shard.verify.sh" > "$T/pre.txt" 2>&1 ); pre=$?
    ( cd "$T/MT" && git add -A && git commit -q -m "trim $f" > "$T/commit.txt" 2>&1 ); crc=$?
    if [ "$crc" != 0 ]; then
      printf 'COMMIT REFUSED by the hooks (exit %s): %s\n' "$crc" "$(head -3 "$T/commit.txt" | tr '\n' ' ' | cut -c1-300)"
      ( cd "$T/MT" && git commit -q --no-verify -m "trim $f" ); rc_all=1
    fi
    ( cd "$T/MT" && bash "$shard.verify.sh" > "$T/post.txt" 2>&1 ); post=$?
    rm -rf "$T/c-$name"; git clone -q --no-local "$T/MT" "$T/c-$name" && ( cd "$T/c-$name" && bash "$shard.verify.sh" > "$T/clone.txt" 2>&1 ); clone=$?
    ( cd "$T/MT" && python3 "$TOOL" --reverify "$shard" > "$T/rev.txt" 2>&1 ); rev=$?
    printf 'commit exit %s (0 = the hooks passed it); proof exit: before the commit %s, after it %s, from a --no-local clone %s; --reverify %s\n' "$crc" "$pre" "$post" "$clone" "$rev"
    tail -1 "$T/clone.txt" | cut -c1-150
    [ "$pre$post$clone$rev" = "0000" ] || rc_all=1
  done
  printf '\nledger entries the trims wrote into methodology/CHANGELOG.md: %s\n' "$(grep -c 'Ledger trim: `methodology/' "$T/MT/methodology/CHANGELOG.md")"
  printf 'a root CHANGELOG.md or HANDOFFS.md appeared: %s\n' "$(cd "$T/MT" && ls CHANGELOG.md HANDOFFS.md 2>/dev/null | wc -l | nospace)"
  printf 'check-ledger / check-handoff after the trims (exit codes): %s / %s\n' \
    "$(cd "$T/MT" && python3 bin/check-ledger > /dev/null 2>&1; echo $?)" "$(cd "$T/MT" && python3 bin/check-handoff > /dev/null 2>&1; echo $?)"
  printf 'trim stage: %s\n' "$([ $rc_all = 0 ] && echo 'every proof held and the hooks passed both commits' || echo 'NOT clean: read the lines above')"
fi

if want hook; then
  h "4. X2: a later commit after the move that does not touch the ledger, hooks ON"
  later() {  # later <clone> <err file>: a content change, no ledger
    printf '\nx\n' >> "$1/docs/planning/BACKLOG.md"; git -C "$1" add docs/planning/BACKLOG.md
    git -C "$1" commit -q -m later > /dev/null 2> "$2"; echo $?
  }
  mk "$T/hc"; printf 'C  control, UNMOVED ledger, later commit: exit=%s (expect nonzero: refused)\n' "$(later "$T/hc" "$T/hc.err")"; head -2 "$T/hc.err" | cut -c1-200 | sed 's/^/     /'
  mk "$T/hx" "$MV"; printf 'X2 MOVED by the tool, later commit without the ledger: exit=%s (expect nonzero: refused; 0 = the gate fails OPEN)\n' "$(later "$T/hx" "$T/hx.err")"; head -2 "$T/hx.err" | cut -c1-200 | sed 's/^/     /'
  mk "$T/hp" "$MV"
  python3 -I - "$T/hp/methodology/CHANGELOG.md" <<'PYEOF'
import sys
p = sys.argv[1]; t = open(p, encoding="utf-8").read()
i = t.index("\n## 2026-10\n") + len("\n## 2026-10\n\n")
open(p, "w", encoding="utf-8").write(t[:i] + "### 2026-10-07 · [ad hoc] P8 probe\n\nA new entry, to show the gate lets a commit that co-stages the moved ledger through.\n\n" + t[i:])
PYEOF
  printf '\nx\n' >> "$T/hp/docs/planning/BACKLOG.md"; git -C "$T/hp" add docs/planning/BACKLOG.md methodology/CHANGELOG.md
  git -C "$T/hp" commit -q -m later-with-ledger > /dev/null 2> "$T/hp.err"; printf 'X2+ MOVED, the same change with methodology/CHANGELOG.md co-staged (a NEW entry): exit=%s (expect 0)\n' "$?"; head -2 "$T/hp.err" | cut -c1-200 | sed 's/^/     /'
  mk "$T/he" "$MV"
  python3 -I - "$T/he/methodology/CHANGELOG.md" <<'PYEOF'
import sys
p = sys.argv[1]; t = open(p, encoding="utf-8").read()
open(p, "w", encoding="utf-8").write(t.replace("S280 close-out", "S280 CLOSE-OUT", 1))
PYEOF
  git -C "$T/he" add methodology/CHANGELOG.md; git -C "$T/he" commit -q -m edit-an-entry > /dev/null 2> "$T/he.err"; rc=$?
  printf 'N  MOVED, an EDIT to a committed ledger entry (the never-edit gate, C6): exit=%s (expect nonzero: refused)\n' "$rc"; head -2 "$T/he.err" | cut -c1-200 | sed 's/^/     /'
fi

if want dash; then
  h "5. the dashboard on the unmoved and the moved clone"
  for d in U M; do
    ( cd "$T/$d" && python3 tools/methodology_dashboard.py --no-open 2> /dev/null | sed 's/\x1b\[[0-9;]*m//g' | grep -E 'Health:|Project|methodology  ' | sed "s/^ */$d: /" )
  done
fi

if want resync; then
  h "6. plan 5A.4: the resync, with the tool's own move, against the current upstream/main"
  rm -rf "$T/R"; git clone -q --no-local "$T/M" "$T/R"; cd "$T/R" || exit 3
  git config core.hooksPath /dev/null; git config user.email t@t; git config user.name t; git config commit.gpgsign false
  git fetch -q "$SRC" "refs/remotes/upstream/main:refs/heads/upstream-main" || exit 3
  UNMOVED="$(git rev-parse "$MV^")"; MB="$(git merge-base "$MV" upstream-main)"
  printf 'upstream/main %s; merge base with the fork %s; fork unmoved %s; fork moved %s\n' "$(git rev-parse --short upstream-main)" "$(git rev-parse --short "$MB")" "$(git rev-parse --short "$UNMOVED")" "$(git rev-parse --short "$MV")"
  printf '\n-- 1. rename detection, merge base -> the moved fork --\n'
  git diff -M --name-status "$MB" "$MV" | grep -E 'CHANGELOG|HANDOFFS|context-budget|quality-gates|gitattributes|dashboard_history' | grep -v 'archive/' | sed 's/^/   /'
  printf '   archive entries paired as renames (R*): %s; as a delete and an add (D, A): %s and %s\n' \
    "$(git diff -M --name-status "$MB" "$MV" | grep -c '^R.*archive/')" "$(git diff -M --name-status "$MB" "$MV" | grep -c '^D.*archive/')" "$(git diff -M --name-status "$MB" "$MV" | grep -c '^A.*archive/')"
  printf '   ledgers at a 30%% threshold: '; git diff -M30% --name-status "$MB" "$MV" -- CHANGELOG.md HANDOFFS.md methodology/CHANGELOG.md methodology/HANDOFFS.md | tr '\n' ' '; printf '\n'
  git checkout -q -b up "$MB"
  printf '\n<!-- up -->\n' >> CHANGELOG.md; printf '\n<!-- up -->\n' >> HANDOFFS.md; printf 'x\n' >> .gitattributes
  python3 -I - <<'PYEOF'
import json
for f in (".context-budget.json", ".quality-gates.json"):
    d = json.load(open(f)); d["_up_edit"] = "x"; open(f, "w").write(json.dumps(d, indent=2) + "\n")
PYEOF
  printf 'new shard\n' > docs/archive/CHANGELOG-through-2099-01-01.md
  git add -A; git commit -q -m 'upstream-like edit'; UPC="$(git rev-parse HEAD)"
  printf '\n-- 2a. fork UNMOVED vs the upstream-like edit (control) --\n'
  git merge-tree --write-tree --name-only "$UNMOVED" "$UPC" 2>&1 | grep -E '^(CONFLICT|Auto-merging)' | cut -c1-120 | sed 's/^/   /'
  printf '\n-- 2b. fork MOVED by the tool vs the same edit --\n'
  git merge-tree --write-tree --name-only "$MV" "$UPC" 2>&1 | grep -E '^(CONFLICT|Auto-merging)' | cut -c1-120 | sed 's/^/   /'
  cd "$SRC" || exit 3
fi

triple() { grep -m1 '^== Summary:' "$1" | sed 's/^== Summary: //; s/ ==$//'; }
if want suites; then
  h "7. plan 3.1: bash bin/tests.sh, the unmoved clone and the moved one, serially, same commit family"
  for d in U M; do
    ( cd "$T/$d" && bash bin/tests.sh > "$T/suite-$d.txt" 2>&1 ); printf '%s: exit %s; %s\n' "$([ $d = U ] && echo unmoved || echo moved)" "$?" "$(triple "$T/suite-$d.txt")"
  done
  printf 'FAIL lines: unmoved %s, moved %s; SKIP lines: unmoved %s, moved %s\n' \
    "$(grep -c '^  FAIL' "$T/suite-U.txt")" "$(grep -c '^  FAIL' "$T/suite-M.txt")" "$(grep -c '^  SKIP' "$T/suite-U.txt")" "$(grep -c '^  SKIP' "$T/suite-M.txt")"
  [ "$(triple "$T/suite-U.txt")" = "$(triple "$T/suite-M.txt")" ] && echo 'the criterion HOLDS: the moved tree reads exactly the unmoved tree'"'"'s triple' || echo 'the criterion FAILS: the triples differ'
  printf 'assertions that FAIL or SKIP in the moved run and not in the unmoved one:\n'
  diff <(grep -E '^  (FAIL|SKIP)' "$T/suite-U.txt" | sort -u) <(grep -E '^  (FAIL|SKIP)' "$T/suite-M.txt" | sort -u) | grep '^>' | cut -c1-200 | head -30
fi

if want ratchet; then
  h "8. quality_ratchet.py --run, the unmoved clone and the moved one (the gates, with the commands the tool rewrote)"
  for d in U M; do
    ( cd "$T/$d" && python3 starter-kit/quality_ratchet.py --run > "$T/ratchet-$d.txt" 2>&1 ); printf '%s: exit %s; %s\n' "$([ $d = U ] && echo unmoved || echo moved)" "$?" "$(grep -E 'pass .* fail .* unmeasured' "$T/ratchet-$d.txt" | tail -1 | cut -c1-200)"
  done
  printf 'gate rows that are not a pass, moved clone:\n'; grep -E 'FAIL|UNMEASURED|unmeasured|REFUSED' "$T/ratchet-M.txt" | grep -v 'pass ·' | cut -c1-200 | head -12
fi
exit 0
