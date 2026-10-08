#!/usr/bin/env bash
# BL-101 P10 evidence: sync-in-both-layouts.sh (the P6 check) at the sha adopters may sync from.
#
# Parts A and B of that script compare the OLD tools (OLD_REV) with the NEW tools on the same adopters, and they assume the
# distributed DOCUMENTS are the same on both sides, because each side reads its own checkout's starter-kit. That held at P6. It
# stopped holding when P9 edited documents: run as it stands at the candidate it reads "25 CHECK(S) FAILED", every one a
# "N versions behind" or "would write" difference between two different sets of documents (p10-sync-in-both-layouts-at-candidate.txt).
#
# This script holds the content equal so only the tools differ: it builds a HYBRID (the candidate's files with the tools of
# OLD_TOOLS: bin/sync, bin/status, bin/check-links, bin/_manifest.py) on a side branch of a scratch clone, and runs the same script
# there with the hybrid as OLD_REV and the candidate as the commit under test. Nothing is written to this repository or to a real
# adopter (the script works in --no-local clones). The scratch clone sits in a temporary directory, so the portfolio root the script
# reads adopters from is passed in explicitly (default: the parent of this repository).
#
#   bash docs/planning/methodology-subdirectory-evidence/p10-sync-hybrid.sh <candidate sha> [old tools rev, default 7f7f74f]
set -u
CAND="${1:?usage: p10-sync-hybrid.sh <candidate sha> [old tools rev]}"
OLD_TOOLS="${2:-7f7f74f}"
SRC="$(git rev-parse --show-toplevel)" || exit 3
PORT="${PORT:-$(dirname "$SRC")}"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
git clone -q --no-local "$SRC" "$T/h" || exit 3
cd "$T/h" || exit 3
git config user.email t@t; git config user.name t; git config core.hooksPath /dev/null
git checkout -q -b hybrid "$CAND" || exit 3
for f in bin/sync bin/status bin/check-links bin/_manifest.py; do git show "$OLD_TOOLS:$f" > "$f" || exit 3; done
git commit -q -am "hybrid: the files of $CAND with the tools of $OLD_TOOLS" || exit 3
HYB="$(git rev-parse --short HEAD)"
git checkout -q --detach "$CAND" || exit 3
printf 'candidate %s   hybrid (old tools, new files) %s   old tools from %s   portfolio %s\n\n' "$(git rev-parse --short HEAD)" "$HYB" "$OLD_TOOLS" "$PORT"
sed "s|^PORT=.*|PORT=\"$PORT\"|" "$SRC/docs/planning/methodology-subdirectory-evidence/sync-in-both-layouts.sh" > "$T/run.sh"
OLD_REV="$HYB" bash "$T/run.sh"
