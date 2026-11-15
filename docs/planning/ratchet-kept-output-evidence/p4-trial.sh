#!/usr/bin/env bash
# p4-trial.sh -- P4 of docs/planning/ratchet-kept-output-plan.md (section 6): a merge trial of the ratchet's
# changes since its 1.5.0 text, laid on the pull request that carries 1.5.0. Read-only toward the repository
# it is given; every write goes to <work-dir>, a scratch directory OUTSIDE the repository.
#
# Usage:
#   bash p4-trial.sh merge  <work-dir> <repo> <base> <ours> <theirs>   three-way merge of the three shipped files
#                                                                      (git merge-file), with a positive and a
#                                                                      negative control
#   bash p4-trial.sh patch  <work-dir> <repo> <base> <ours> <theirs>   the same change as a PATCH (git apply
#                                                                      --3way) in a scratch clone at <ours>, then
#                                                                      byte-compared with what `merge` produced
#   bash p4-trial.sh resolve <work-dir>                                resolve the one conflict by one stated rule in
#                                                                      both outputs and byte-compare them
#   bash p4-trial.sh compose <work-dir> <repo> <ours>                  two scratch clones at <ours>: composed (the
#                                                                      three resolved files) and control (untouched)
#   bash p4-trial.sh lint <work-dir> <repo> <ours> <lint-commit> <main>  the one unit test that errors on the composed
#                                                                      tree, and the lint it needs (two copies)
#   bash p4-trial.sh census <repo> <base> <ours> <theirs>              the project-internal codes (backlog ids,
#                                                                      session numbers, 'fork', plan paths) in the
#                                                                      ADDED lines, and in <ours> as the control
#
# <base> is the last commit whose copy of the tool is the 1.5.0 text (0df0bae8^), <ours> the pull request head
# (47637be2), <theirs> the commit whose tool is wanted (main). The expectations are in the record that cites
# this file; this script only builds the states they read.
set -uo pipefail

FILES=(starter-kit/quality_ratchet.py tools/test_quality_ratchet.py starter-kit/quality-gates.json)
phase="${1:-}"
[ -n "$phase" ] || { sed -n '2,32p' "$0" >&2; exit 3; }
flat() { echo "$1" | tr '/' '_'; }

case "$phase" in
merge)
    work="${2:-}"; repo="${3:-}"; base="${4:-}"; ours="${5:-}"; theirs="${6:-}"
    [ -n "$theirs" ] || { echo "merge needs <work-dir> <repo> <base> <ours> <theirs>" >&2; exit 3; }
    out="$work/merge"; mkdir -p "$out"
    echo "base   $(git -C "$repo" rev-parse --short=8 "$base")  ours $(git -C "$repo" rev-parse --short=8 "$ours")  theirs $(git -C "$repo" rev-parse --short=8 "$theirs")"
    total=0
    for f in "${FILES[@]}"; do
        n=$(flat "$f")
        git -C "$repo" show "$base:$f"   > "$out/$n.base"   || exit 1
        git -C "$repo" show "$ours:$f"   > "$out/$n.ours"   || exit 1
        git -C "$repo" show "$theirs:$f" > "$out/$n.theirs" || exit 1
        git merge-file -p --diff3 -L ours -L base -L theirs "$out/$n.ours" "$out/$n.base" "$out/$n.theirs" > "$out/$n.merged"
        rc=$?
        total=$((total + rc))
        echo "  merge   $f  conflicts=$rc  lines: ours $(wc -l < "$out/$n.ours" | tr -d ' ') base $(wc -l < "$out/$n.base" | tr -d ' ') theirs $(wc -l < "$out/$n.theirs" | tr -d ' ') merged $(wc -l < "$out/$n.merged" | tr -d ' ')  sha256 $(shasum -a 256 "$out/$n.merged" | cut -c1-12)"
        [ "$rc" -eq 0 ] || grep -n '^<<<<<<<\|^=======$\|^>>>>>>>' "$out/$n.merged" | sed 's/^/      marker /'
    done
    echo "  total conflicts: $total"
    echo "  merged tool VERSION: $(grep -m1 '^VERSION' "$out/$(flat starter-kit/quality_ratchet.py).merged")   (ours: $(grep -m1 '^VERSION' "$out/$(flat starter-kit/quality_ratchet.py).ours"), theirs: $(grep -m1 '^VERSION' "$out/$(flat starter-kit/quality_ratchet.py).theirs"))"
    # Positive control: the instrument must SEE a conflict. Change the VERSION line in <ours>, a line the change also
    # changes (1.5.0 to 1.7.0); the merge must report at least one conflict.
    q="$out/$(flat starter-kit/quality_ratchet.py)"
    sed 's/^VERSION = "1.5.0"/VERSION = "1.5.0-control"/' "$q.ours" > "$q.ours-control"
    if cmp -s "$q.ours" "$q.ours-control"; then echo "  CONTROL BROKEN: the control edit changed nothing"; exit 1; fi
    git merge-file -p --diff3 "$q.ours-control" "$q.base" "$q.theirs" > /dev/null; crc=$?
    echo "  positive control (a changed VERSION line in <ours>): conflicts=$crc  $([ "$crc" -ge 1 ] && echo 'the instrument sees a conflict: ok' || echo 'NOT SEEN: the zero above means nothing')"
    # Negative control: theirs == base is no change at all; the merge must be clean and equal <ours>.
    git merge-file -p "$q.ours" "$q.base" "$q.base" > "$q.neg"; nrc=$?
    cmp -s "$q.neg" "$q.ours" && same=equal || same=DIFFERENT
    echo "  negative control (nothing changes): conflicts=$nrc, result $same to <ours>"
    ;;
patch)
    work="${2:-}"; repo="${3:-}"; base="${4:-}"; ours="${5:-}"; theirs="${6:-}"
    [ -n "$theirs" ] || { echo "patch needs <work-dir> <repo> <base> <ours> <theirs>" >&2; exit 3; }
    clone="$work/patch-clone/methodology"
    [ ! -e "$clone" ] || { echo "refusing: $clone exists" >&2; exit 1; }
    mkdir -p "$work/patch-clone"
    git clone -q "$repo" "$clone" || exit 1
    git -C "$clone" reset -q --hard "$ours" || exit 1
    git -C "$repo" diff "$base" "$theirs" -- "${FILES[@]}" > "$work/net.patch"
    echo "  patch: $(grep -c '^@@' "$work/net.patch") hunks, $(wc -c < "$work/net.patch" | tr -d ' ') B, applied with git apply --3way at $(git -C "$clone" rev-parse --short=8 HEAD)"
    git -C "$clone" apply --3way "$work/net.patch" 2>&1 | sed 's/^/    /'
    echo "  apply exit: ${PIPESTATUS[0]}"
    for f in "${FILES[@]}"; do
        n=$(flat "$f")
        if git -C "$clone" diff --name-only --diff-filter=U | grep -qxF "$f"; then
            echo "  conflicted in the clone, so the two outputs carry different marker styles; compared after \`resolve\`   $f"
        elif cmp -s "$clone/$f" "$work/merge/$n.merged"; then echo "  patch result == merge result   $f"; else echo "  patch result DIFFERS from merge result   $f"; fi
    done
    echo "  unmerged paths in the clone: $(git -C "$clone" diff --name-only --diff-filter=U | wc -l | tr -d ' ')"
    ;;
resolve)
    # One rule for every conflict block, applied to BOTH outputs (the diff3 markers of `merge` and the two-way
    # markers of `patch`): keep <ours>' side, then add each line of <theirs>' side that is not in the base file
    # and not already there. That is right only where <ours> edited a line the change leaves alone and the change
    # adds lines beside it; the script checks that for the diff3 output (the base side must equal the theirs
    # lines that are in the base file) and refuses otherwise.
    work="${2:-}"
    [ -n "$work" ] || { echo "resolve needs <work-dir>" >&2; exit 3; }
    mkdir -p "$work/resolved"
    for f in "${FILES[@]}"; do
        n=$(flat "$f")
        python3 -I - "$work/merge/$n.base" "$work/merge/$n.merged" "$work/patch-clone/methodology/$f" "$work/resolved/$n.from-merge" "$work/resolved/$n.from-patch" <<'PY'
import sys
base_p, merged_p, patched_p, out_a, out_b = sys.argv[1:6]
base_set = set(open(base_p, encoding="utf-8").read().split("\n"))
def resolve(text, check):
    lines, out, i, blocks = text.split("\n"), [], 0, 0
    while i < len(lines):
        if lines[i].startswith("<<<<<<< "):
            blocks += 1
            o, b, t, sect = [], [], [], "o"
            i += 1
            while not lines[i].startswith(">>>>>>> "):
                l = lines[i]
                if l.startswith("||||||| "): sect = "b"
                elif l == "=======": sect = "t"
                else: {"o": o, "b": b, "t": t}[sect].append(l)
                i += 1
            if check:
                kept = [l for l in t if l in base_set]
                assert kept == b, f"theirs changed a line of the base side too: refusing\n{kept}\n{b}"
            out += o + [l for l in t if l not in base_set and l not in o]
        else:
            out.append(lines[i])
        i += 1
    return "\n".join(out), blocks
for src, dst, check in ((merged_p, out_a, True), (patched_p, out_b, False)):
    text, blocks = resolve(open(src, encoding="utf-8").read(), check)
    open(dst, "w", encoding="utf-8", newline="").write(text)
    print(f"    {dst.rsplit('/', 1)[-1]}: {blocks} conflict block(s) resolved, {len(text.split(chr(10)))} lines")
PY
        if cmp -s "$work/resolved/$n.from-merge" "$work/resolved/$n.from-patch"; then
            echo "  resolved: merge == patch (byte-identical)   $f   sha256 $(shasum -a 256 "$work/resolved/$n.from-merge" | cut -c1-12)"
        else
            echo "  resolved: merge DIFFERS from patch   $f"
        fi
    done
    ;;
compose)
    # Two scratch clones named `methodology` (the gates' ../methodology paths resolve only under that name), both at
    # <ours>: composed/ gets the three resolved files, control/ stays as the pull request has it.
    work="${2:-}"; repo="${3:-}"; ours="${4:-}"
    [ -n "$ours" ] || { echo "compose needs <work-dir> <repo> <ours>" >&2; exit 3; }
    for side in composed control; do
        clone="$work/$side/methodology"
        [ ! -e "$clone" ] || { echo "refusing: $clone exists" >&2; exit 1; }
        mkdir -p "$work/$side"
        git clone -q "$repo" "$clone" || exit 1
        git -C "$clone" reset -q --hard "$ours" || exit 1
    done
    for f in "${FILES[@]}"; do cp "$work/resolved/$(flat "$f").from-merge" "$work/composed/methodology/$f"; done
    echo "  composed: $(git -C "$work/composed/methodology" status --porcelain | wc -l | tr -d ' ') modified file(s), tool $(grep -m1 '^VERSION' "$work/composed/methodology/starter-kit/quality_ratchet.py")"
    git -C "$work/composed/methodology" diff --shortstat | sed 's/^/    /'
    echo "  control:  $(git -C "$work/control/methodology" status --porcelain | wc -l | tr -d ' ') modified file(s), tool $(grep -m1 '^VERSION' "$work/control/methodology/starter-kit/quality_ratchet.py")"
    for side in composed control; do python3 -I -m py_compile "$work/$side/methodology/starter-kit/quality_ratchet.py" && echo "  $side: quality_ratchet.py compiles"; done
    ;;
lint)
    # The one unit test that errors on the composed tree loads bin/check-handoff and expects its lint to refuse a
    # citation that does not name the unmeasured gates. Show that THAT is the cause: in two copies of the composed
    # clone give the test the lint it expects, and run the 1.7.0 test class.
    #   v1: <ours>' lint with ONE commit merged in on blobs (<lint-commit>, the commit that added the rule)
    #   v2: the whole lint of <main> (causal evidence only: it is not a merge)
    work="${2:-}"; repo="${3:-}"; ours="${4:-}"; lintc="${5:-}"; main="${6:-}"
    [ -n "$main" ] || { echo "lint needs <work-dir> <repo> <ours> <lint-commit> <main>" >&2; exit 3; }
    T=test_the_lint_accepts_the_pasted_pair_and_refuses_the_citation_without_the_clause
    d="$work/lint"; mkdir -p "$d"
    git -C "$repo" show "$lintc^:bin/check-handoff" > "$d/base"
    git -C "$repo" show "$ours:bin/check-handoff"   > "$d/ours"
    git -C "$repo" show "$lintc:bin/check-handoff"  > "$d/theirs"
    echo "  lint sizes: base($lintc^) $(wc -l < "$d/base" | tr -d ' ') lines, <ours> $(wc -l < "$d/ours" | tr -d ' ') lines, $lintc $(wc -l < "$d/theirs" | tr -d ' ') lines; the commit itself: $(git -C "$repo" show --shortstat --format= "$lintc" -- bin/check-handoff | tr -s ' ')"
    echo "  names rule in the lint, by ref: <ours> $(grep -c 'receipt names' "$d/ours") hit(s); $lintc $(grep -c 'receipt names' "$d/theirs") hit(s)"
    for v in v1 v2; do
        rm -rf "$work/$v"; mkdir -p "$work/$v"; cp -R "$work/composed/methodology" "$work/$v/methodology"
    done
    git merge-file -p "$d/ours" "$d/base" "$d/theirs" > "$work/v1/methodology/bin/check-handoff"; echo "  v1 (lint = <ours> + $lintc on blobs): conflicts=$?"
    git -C "$repo" show "$main:bin/check-handoff" > "$work/v2/methodology/bin/check-handoff"
    for v in v1 v2; do
        ( cd "$work/$v/methodology" && chmod +x bin/check-handoff
          printf '  %s, the one test:  ' "$v"; python3 tools/test_quality_ratchet.py "TestTheUnmeasuredGatesAreNamed.$T" 2>&1 | grep -E '^(OK|FAILED)' | tr '\n' ' '; echo
          printf '  %s, the whole 1.7.0 class:  ' "$v"; python3 tools/test_quality_ratchet.py TestTheUnmeasuredGatesAreNamed 2>&1 | grep -E '^(Ran|OK|FAILED)' | tr '\n' ' '; echo )
    done
    rm -rf "$work/v1" "$work/v2"
    ;;
census)
    repo="${2:-}"; base="${3:-}"; ours="${4:-}"; theirs="${5:-}"
    [ -n "$theirs" ] || { echo "census needs <repo> <base> <ours> <theirs>" >&2; exit 3; }
    for f in "${FILES[@]}"; do
        python3 -I - "$repo" "$base" "$ours" "$theirs" "$f" <<'PY'
import re, subprocess, sys
repo, base, ours, theirs, f = sys.argv[1:6]
CODES = {
    "backlog id":     re.compile(r"\bBL-\d+"),
    "session number": re.compile(r"\bS\d{3}\b"),
    "fork":           re.compile(r"\bfork\b", re.I),
    "plan path":      re.compile(r"docs/planning"),
    "operator":       re.compile(r"\boperator\b", re.I),
    "learning":       re.compile(r"\bLearning #\d+", re.I),
}
def git(*a):
    return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True, check=True).stdout
diff = git("diff", "-U0", base, theirs, "--", f)
added, n = [], 0
for line in diff.split("\n"):
    m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)", line)
    if m:
        n = int(m.group(1)); continue
    if line.startswith("+") and not line.startswith("+++"):
        added.append((n, line[1:])); n += 1
counts = {k: sum(1 for _, t in added if r.search(t)) for k, r in CODES.items()}
anyhit = sorted({ln for ln, t in added if any(r.search(t) for r in CODES.values())})
ours_text = git("show", f"{ours}:{f}").split("\n")
ours_counts = {k: sum(1 for t in ours_text if r.search(t)) for k, r in CODES.items()}
print(f"  {f}")
print(f"    added lines {len(added)}; lines with any code {len(anyhit)}")
print("    by code (added lines):  " + "  ".join(f"{k}={v}" for k, v in counts.items()))
print("    control, the whole file at <ours>:  " + "  ".join(f"{k}={v}" for k, v in ours_counts.items()))
for ln, t in added:
    if any(r.search(t) for r in CODES.values()):
        print(f"    ADDED  L{ln}: {t.strip()[:120]}")
for i, t in enumerate(ours_text, 1):
    if any(r.search(t) for r in CODES.values()):
        print(f"    OURS   L{i}: {t.strip()[:120]}")
PY
    done
    ;;
*)
    echo "unknown phase: $phase" >&2; exit 3
    ;;
esac
