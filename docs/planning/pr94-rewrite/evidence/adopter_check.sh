#!/bin/bash
# usage: adopter_check.sh TRIM_TOOL DIR [DIR ...]   -- `--check` (read-only) of TRIM_TOOL on each project's notes file
T=$1; shift
for d in "$@"; do
  f="SESSION_NOTES.md"; [ -f "$d/$f" ] || f="methodology/SESSION_NOTES.md"; [ -f "$d/$f" ] || continue
  out=$(cd "$d" && python3 -I "$T" --file "$f" --check 2>&1); rc=$?
  codes=$(echo "$out" | grep -oE '^\s*\[[A-Z0-9_]+\]' | tr -d ' []' | tr '\n' ' ')
  printf "%-26s %-28s exit=%s codes: %s\n" "$(basename "$d")" "$f" "$rc" "$codes"
done
