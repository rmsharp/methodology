#!/usr/bin/env bash
# BL-134 (a): the 14 pipelines in bin/tests.sh that feed an early-exiting `grep -q` from a command or a chain.
# Each site is replayed with the SAME producer and the SAME consumer text as at bin/tests.sh:LINE, against a
# fixture built the way the suite builds it, under the suite's own `set -uo pipefail`, keeping the exit status of
# EVERY stage (PIPESTATUS). A pipeline reads as failed when any stage is not 0; "141" is 128 + 13, SIGPIPE: a stage
# was writing to a pipe whose reader (the next `grep -q`) had already quit.
#
# Usage: bash bl134-measure.sh list
#        bash bl134-measure.sh check [SITE ...]    one run of each site: statuses, and the bytes and lines the
#                                                  stream that feeds the final `grep -q` carries
#        bash bl134-measure.sh loop SITE N         N runs of the exact pipeline; one summary line
#        bash bl134-measure.sh amp  SITE N         N runs with the final `grep -q` replaced by a WAITING reader that
#                                                  quits after ONE byte (the worst case a consumer can be)
#        bash bl134-measure.sh pieces SITE N       how the stream reaches the final `grep -q`: the size of each read
#        bash bl134-measure.sh control [N]         positive control for `amp`: bash `echo` of 2,186 B (must kill sometimes)
# Functions the suite defines (surface_check, mutate, s34_*, two_block_ledger) are lifted from bin/tests.sh by
# name at run time, so the replay follows the suite.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
METHODOLOGY="$(cd "$HERE/../../.." && pwd)"; BIN="$METHODOLOGY/bin"; STARTER="$METHODOLOGY/starter-kit"
SITES="s259 s388 s397 s411 s431 s432 s2318 s2326 s2335 s2343 s2351 s3377 s4725 s5533"
export TMPDIR; TMPDIR="$(mktemp -d)"; trap 'rm -rf "$TMPDIR"' EXIT

mktemp_project() { local dir; dir="$(mktemp -d)"; git -C "$dir" init -q; echo "$dir"; }
lift() { # $1 function name: print its definition from the suite (one-liner, or up to the first '^}')
    awk -v n="$1()" 'index($0,n)==1 { print; if ($0 ~ /\}[[:space:]]*$/) exit; p=1; next } p { print } p && /^\}$/ { exit }' "$BIN/tests.sh"
}
for f in surface_check mutate s34_case s34_project s34_sync two_block_ledger nslot; do eval "$(lift "$f")"; done

# --- the 14 sites: setup_X (once), stream_X (the pipeline minus its final `grep -q`), run_X (the exact pipeline) ---
status_stale_changelog() { # Test 19 (c) and (e): a project whose CHANGELOG.md is a pre-v3.1 shape, synced again
    P="$(mktemp_project)"; "$BIN/sync" "$P" >/dev/null
    printf '# Changelog\n\nAll notable changes to this project.\n\n## [Unreleased]\n' > "$P/CHANGELOG.md"
    echo "arbitrary adopter content" > "$P/SESSION_NOTES.md"; "$BIN/sync" "$P" >/dev/null
}
setup_s259() { P="$(mktemp_project)"; "$BIN/sync" "$P" >/dev/null; echo "# local edit" >> "$P/SESSION_RUNNER.md"; OUT="$("$BIN/status" "$P")"; }
stream_s259() { echo "$OUT" | grep "SESSION_RUNNER.md"; }
run_s259() { echo "$OUT" | grep "SESSION_RUNNER.md" | grep -q "locally modified"; PS="${PIPESTATUS[*]}"; }

setup_s388() { status_stale_changelog; }
stream_s388() { "$BIN/status" "$P" | grep "CHANGELOG.md" | grep -v '^note:'; }
run_s388() { "$BIN/status" "$P" | grep "CHANGELOG.md" | grep -v '^note:' | grep -q "stale format"; PS="${PIPESTATUS[*]}"; }

setup_s397() { status_stale_changelog; P2="$(mktemp_project)"; "$BIN/sync" "$P2" >/dev/null
    printf '# Changelog\n\n## [Unreleased]\n' > "$P2/CHANGELOG.md"; MULTI="$("$BIN/status" "$P" "$P2")"; }
stream_s397() { echo "$MULTI" | grep '^note:'; }
run_s397() { echo "$MULTI" | grep '^note:' | grep -q "2 seeds predate"; PS="${PIPESTATUS[*]}"; }

setup_s411() { P2="$(mktemp_project)"; "$BIN/sync" "$P2" >/dev/null; cp "$STARTER/CHANGELOG.md" "$P2/CHANGELOG.md"
    printf '# Handoff Receipts\n\nNewest on top; prepend-only.\n\n```handoff\nsession: S1\ndate: 2026-01-01\nstatus: complete\n```\n' > "$P2/HANDOFFS.md"
    OUT="$("$BIN/status" "$P2")"; }
stream_s411() { echo "$OUT" | grep "HANDOFFS.md" | grep -v '^note:'; }
run_s411() { echo "$OUT" | grep "HANDOFFS.md" | grep -v '^note:' | grep -q "stale format"; PS="${PIPESTATUS[*]}"; }

setup_s431() { :; }
stream_s431() { grep '^\*\*Updating an existing project from an earlier methodology version:\*\*' "$STARTER/BOOTSTRAP.md"; }
run_s431() { grep '^\*\*Updating an existing project from an earlier methodology version:\*\*' "$STARTER/BOOTSTRAP.md" | grep -q "Size, and when to archive"; PS="${PIPESTATUS[*]}"; }
setup_s432() { :; }
stream_s432() { stream_s431; }
run_s432() { grep '^\*\*Updating an existing project from an earlier methodology version:\*\*' "$STARTER/BOOTSTRAP.md" | grep -q "keeping any archive-pointer block and month heading"; PS="${PIPESTATUS[*]}"; }

surface_fixture() { RUNNER36="$STARTER/SESSION_RUNNER.md"; F36="$(mktemp)"; mutate "$RUNNER36" "$F36" "$1"; }
setup_s2318() { surface_fixture 're.sub(r"(?m)^- \[ \] Each phase names the SURFACE.*\n", "", s, count=1)'; }
stream_s2318() { surface_check "$F36"; }
run_s2318() { surface_check "$F36" | grep -q "MISSING-CHECKLIST-SURFACE"; PS="${PIPESTATUS[*]}"; }
setup_s2326() { surface_fixture 're.sub(r"(?m)^- \*\*The surface\*\*.*\n", "", s, count=1)'; }
stream_s2326() { surface_check "$F36"; }
run_s2326() { surface_check "$F36" | grep -q "MISSING-CRITERIA-SURFACE"; PS="${PIPESTATUS[*]}"; }
setup_s2335() { surface_fixture 's.replace("**(d) Faithful verification, per surface.**", "**(d) Verification fidelity.**", 1)'; }
stream_s2335() { surface_check "$F36"; }
run_s2335() { surface_check "$F36" | grep -q "DANGLING-GATE-D"; PS="${PIPESTATUS[*]}"; }
setup_s2343() { surface_fixture 's.replace("gate (d)", "the slice gates", 1)'; }
stream_s2343() { surface_check "$F36"; }
run_s2343() { surface_check "$F36" | grep -q "MISSING-GATE-D-ANCHOR"; PS="${PIPESTATUS[*]}"; }
setup_s2351() { surface_fixture 's.replace("#### Planning Session Checklist", "#### Planning Session Checkboxes", 1)'; }
stream_s2351() { surface_check "$F36"; }
run_s2351() { surface_check "$F36" | grep -q "EMPTY-CHECKLIST"; PS="${PIPESTATUS[*]}"; }

setup_s3377() { EMPTY40="$(mktemp)"
    printf '# Changelog\n\n### 2026-01-01 · [ad hoc] readable, genuinely no bullet\n\nprose.\n' > "$EMPTY40"; }
stream_s3377() { "$BIN/model-report" --changelog "$EMPTY40" --handoffs "$METHODOLOGY/HANDOFFS.md" --no-git 2>&1; }
run_s3377() { "$BIN/model-report" --changelog "$EMPTY40" --handoffs "$METHODOLOGY/HANDOFFS.md" --no-git 2>&1 | grep -q 'no CHANGELOG.md entries carry a'; PS="${PIPESTATUS[*]}"; }

setup_s4725() { # Test 53's fixture (bin/tests.sh:4649-4657) and its first refusal case, gitdest
    T34="$(mktemp -d)"; B34="$T34/base"; git -C "$T34" init -q -b main base
    mkdir -p "$B34/bin"; cp "$BIN/_manifest.py" "$B34/bin/"
    python3 -c "import sys; sys.path.insert(0, '$B34/bin'); import _manifest; print('\n'.join(s for s, _d, _x in _manifest.DISTRIBUTION))" \
        | while read -r src; do mkdir -p "$B34/$(dirname "$src")"; cp "$METHODOLOGY/$src" "$B34/$src"; done
    rm -rf "$B34/bin/__pycache__"
    git -C "$B34" add -A; git -C "$B34" -c user.email=t@t -c user.name=t commit -qm "a complete source"
    S34_SRC="$(s34_case gitdest '"ROADMAP.md", SEED)' '".git/hooks/pre-commit", SEED)')"; P="$(s34_project)"
    OUT="$(s34_sync "$S34_SRC" "$P")"; }
stream_s4725() { head -1 <<<"$OUT"; }
run_s4725() { head -1 <<<"$OUT" | grep -q "^error: the bin/_manifest.py in file://$S34_SRC "; PS="${PIPESTATUS[*]}"; }

setup_s5533() { H62="$(mktemp -d)"; two_block_ledger 'pending' > "$H62/two.md"
    NOTE62="$("$BIN/check-handoff" --file "$H62/two.md" 2>&1 | grep -A8 '^  note:')"; Q62="$(grep -o '"[^"]*"' <<<"$NOTE62" | head -1 | tr -d '"')"; }
stream_s5533() { tr -s '\n ' '  ' < "$STARTER/HANDOFFS.md"; }
run_s5533() { tr -s '\n ' '  ' < "$STARTER/HANDOFFS.md" | grep -qF "$Q62"; PS="${PIPESTATUS[*]}"; }

clean() { [[ "$1" =~ ^(0\ )*0$ ]]; }
prep() { # $1 site: run its setup, prove one clean run, or say why not
    "setup_$1" >/dev/null 2>&1; "run_$1"
    clean "$PS" || { echo "FIXTURE-BROKEN $1: statuses [$PS]" >&2; return 1; }
}
cmd="${1:-}"
case "$cmd" in
list) echo $SITES ;;
check)
    shift; for s in ${@:-$SITES}; do
        if prep "$s"; then
            n="$("stream_$s" | wc -c | tr -d ' ')"; l="$("stream_$s" | wc -l | tr -d ' ')"
            printf '%-7s statuses [%s]  stream into the final grep -q: %s B, %s lines\n' "$s" "$PS" "$n" "$l"
        else printf '%-7s statuses [%s]  FIXTURE-BROKEN\n' "$s" "$PS"; fi
    done ;;
loop)
    s="$2"; N="${3:-1000}"; prep "$s" || exit 3
    bad=0; killed=0; seen=""
    for ((i = 0; i < N; i++)); do
        "run_$s"
        clean "$PS" && continue
        bad=$((bad + 1)); [[ "$PS" == *141* ]] && killed=$((killed + 1)); seen="$seen [$PS]"
    done
    echo "site=$s N=$N not-clean=$bad sigpipe=$killed statuses:${seen:- none}" | cut -c1-300 ;;
amp)
    # The reader is ALREADY WAITING when the first bytes land (the producer starts 20 ms late) and quits after one
    # byte: bl133-diagnosis-evidence/waiting-reader.sh's form. A reader started with its producer is not parked yet
    # and killed nothing in 600 runs of the positive control (see `control`), so it proved nothing.
    s="$2"; N="${3:-1000}"; prep "$s" || exit 3
    killed=0; seen=""
    for ((i = 0; i < N; i++)); do
        { sleep 0.02; "stream_$s"; } | head -c 1 >/dev/null; PS="${PIPESTATUS[0]}"
        [ "$PS" = 141 ] && { killed=$((killed + 1)); seen="$seen [$PS]"; }
    done
    echo "site=$s N=$N (waiting reader quits after 1 byte) sigpipe=$killed statuses:${seen:- none}" | cut -c1-300 ;;
pieces)
    # How the stream reaches the final `grep -q`: whole (one read) or in pieces (several). A reader already waiting
    # sees each write() as its own read; one piece means the stage wrote once and nothing can be killed after the match.
    s="$2"; N="${3:-100}"; prep "$s" || exit 3
    declare -A tally=()
    for ((i = 0; i < N; i++)); do
        r="$({ sleep 0.06; "stream_$s"; } | python3 -I "$HERE/piece-reader.py")"; tally["$r"]=$(( ${tally["$r"]:-0} + 1 ))
    done
    out=""; for k in "${!tally[@]}"; do out="$out [$k]x${tally[$k]}"; done
    echo "site=$s N=$N reads seen:$out" | cut -c1-300 ;;
control)
    # POSITIVE CONTROL for `amp`: bash `echo` of a 2,186 B single line and of 27 lines of 80 B, the forms
    # bl133-diagnosis-evidence/waiting-reader.sh killed 15 and 9 times in 200. If this reads 0 the amplifier is blind.
    N="${2:-200}"
    for label in SL ML; do
        case $label in SL) V="$(python3 -c "print('x'*2186, end='')")";; ML) V="$(python3 -c "print('\n'.join(['x'*80]*27), end='')")";; esac
        k=0
        for ((i = 0; i < N; i++)); do { sleep 0.02; echo "$V"; } | head -c 1 >/dev/null; [ "${PIPESTATUS[0]}" = 141 ] && k=$((k + 1)); done
        echo "control $label (${#V} B): echo killed (141) $k of $N"
    done ;;
*) sed -n '2,15p' "$0"; exit 2 ;;
esac
