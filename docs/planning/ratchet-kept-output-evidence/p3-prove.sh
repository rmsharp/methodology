#!/usr/bin/env bash
# p3-prove.sh -- P3 of docs/planning/ratchet-kept-output-plan.md (section 6): the 1.6.0 keeper on the real suite.
#
# Usage (the work directory is a scratch directory OUTSIDE this repository):
#   bash p3-prove.sh setup   <work-dir> <source-repo> <commit>   clone <source-repo> to <work-dir>/methodology at <commit>
#   bash p3-prove.sh inject  <work-dir>                          add the one deliberate `fail` line after Test 1's header
#   bash p3-prove.sh launch  <work-dir> <tag>                    detached `quality_ratchet.py --run`; writes <tag>.out, .err, .done
#   bash p3-prove.sh restore <work-dir>                          `git checkout -- bin/tests.sh`
#
# The clone is named `methodology` because the gates' `../methodology` paths resolve only under that name.
# NEVER run this against the working tree: `--run` overwrites its results file and keeps output beside it.
# The expectations are in p3-check.py; this file only builds the state they read.
set -uo pipefail

phase="${1:-}"
work="${2:-}"
[ -n "$phase" ] && [ -n "$work" ] || { sed -n '2,13p' "$0" >&2; exit 3; }
clone="$work/methodology"

case "$phase" in
setup)
    repo="${3:-}"; commit="${4:-}"
    [ -n "$repo" ] && [ -n "$commit" ] || { echo "setup needs <source-repo> <commit>" >&2; exit 3; }
    [ ! -e "$clone" ] || { echo "refusing: $clone already exists" >&2; exit 1; }
    mkdir -p "$work"
    git clone -q "$repo" "$clone" || exit 1
    git -C "$clone" config core.hooksPath .githooks
    git -C "$clone" reset -q --hard "$commit" || exit 1
    echo "clone:    $clone"
    echo "HEAD:     $(git -C "$clone" rev-parse HEAD)"
    echo "branch:   $(git -C "$clone" rev-parse --abbrev-ref HEAD)"
    echo "tool:     $(grep -m1 '^VERSION' "$clone/starter-kit/quality_ratchet.py")"
    echo "gates:    $(python3 -I -c 'import json,sys; print(len(json.load(open(sys.argv[1]))["gates"]))' "$clone/.quality-gates.json")"
    echo "porcelain lines: $(git -C "$clone" status --porcelain | wc -l | tr -d ' ')"
    [ ! -e "$clone/.quality-gates-output" ] && [ ! -e "$clone/.quality-gates-results.json" ] \
        && echo "no kept directory and no results file yet: ok" \
        || { echo "a kept directory or results file is already there" >&2; exit 1; }
    ;;
inject)
    python3 -I - "$clone/bin/tests.sh" <<'PY'
import sys
path = sys.argv[1]
text = open(path, encoding="utf-8").read()
lines = text.split("\n")
assert lines[28].startswith('echo "== Test 1:'), "line 29 is not Test 1's header: " + lines[28]
assert 'kept-output proof' not in text, "already injected"
lines.insert(29, 'fail "kept-output proof: deliberate failure"')
with open(path, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines))
PY
    [ $? -eq 0 ] || exit 1
    bash -n "$clone/bin/tests.sh" && echo "bash -n bin/tests.sh: ok"
    git -C "$clone" diff --stat | cat
    git -C "$clone" diff -U1 bin/tests.sh | sed -n '5,20p'
    ;;
launch)
    tag="${3:-}"
    [ -n "$tag" ] || { echo "launch needs <tag>" >&2; exit 3; }
    [ ! -e "$work/$tag.done" ] || { echo "refusing: $work/$tag.done exists" >&2; exit 1; }
    date -u +%Y-%m-%dT%H:%M:%SZ > "$work/$tag.started"
    uptime > "$work/$tag.load-at-start"
    cd "$clone" || exit 1
    nohup bash -c 'python3 starter-kit/quality_ratchet.py --run >"$1.out" 2>"$1.err"; echo $? >"$1.done"; date -u +%Y-%m-%dT%H:%M:%SZ >"$1.ended"' _ "$work/$tag" >/dev/null 2>&1 &
    echo "launched $tag at $(cat "$work/$tag.started"), pid $!"
    ;;
restore)
    git -C "$clone" checkout -- bin/tests.sh || exit 1
    echo "porcelain lines after restore: $(git -C "$clone" status --porcelain | wc -l | tr -d ' ')"
    ;;
*)
    echo "unknown phase: $phase" >&2; exit 3
    ;;
esac
