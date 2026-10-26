#!/usr/bin/env bash
# A standalone `---` inside the oldest RETAINED record makes the trimmed notes file unclassifiable (footer_mode 'none').
# Usage: bash notes_rule_in_last_record.sh <clone of a project whose SESSION_NOTES.md has such a rule> <trimmer> [line-of-the-rule]
set -eu
clone=$1; trim=$2; rule=${3:-31}
cd "$clone"
echo "trimmer: $(python3 -I "$trim" --version)"
echo "records: $(grep -c -E '^### (What Session [0-9]+ Did|Session [0-9]+ Handoff Evaluation \(by Session [0-9]+\))' SESSION_NOTES.md), standalone rules at lines: $(grep -n -E '^---\s*$' SESSION_NOTES.md | cut -d: -f1 | tr '\n' ' ')"
for cut in 3 2; do
  printf -- "--cut %s: " "$cut"; python3 -I "$trim" --file SESSION_NOTES.md --cut "$cut" --today 2026-10-26 2>&1 | grep -E "ARTIFACT_UNPARSEABLE|DRY_RUN" | cut -c1-110
done
sed -i.bak "${rule}d" SESSION_NOTES.md
printf -- "--cut 3 with line %s removed: " "$rule"; python3 -I "$trim" --file SESSION_NOTES.md --cut 3 --today 2026-10-26 2>&1 | grep -E "ARTIFACT_UNPARSEABLE|DRY_RUN" | cut -c1-110
mv SESSION_NOTES.md.bak SESSION_NOTES.md
