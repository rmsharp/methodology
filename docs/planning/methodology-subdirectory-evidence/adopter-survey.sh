#!/usr/bin/env bash
# Where do the 12 sibling adopters keep the methodology files today, and what else names them?
# Read-only. Run from anywhere:   PORTFOLIO=~/Development bash adopter-survey.sh
# bash, not zsh: the file list is an array, because zsh does not word-split an unquoted variable
# (the first run of this survey, in zsh, counted 0 root files for every project).
PORTFOLIO="${PORTFOLIO:-$HOME/Development}"
ADOPTERS=(airqino chat_verification church_growth claude_work dalia_martinez_funeral
          feedback-loop-comparison model_project_constructor mts-system nprcgenekeepr
          Philippians vscode_quarto_ext wsfct)
FILES=(SESSION_RUNNER.md FRAMEWORK_LEARNINGS.md SAFEGUARDS.md RECOMMENDED_SKILLS.md CONTEXT_TEMPLATE.md
       CLAUDE_TEMPLATE.md BOOTSTRAP.md methodology_dashboard.py methodology_trim.py context_budget.py
       quality_ratchet.py SESSION_NOTES.md CHANGELOG.md HANDOFFS.md ROADMAP.md BACKLOG.md CONTEXT.md
       .context-budget.json .quality-gates.json .gitattributes)
PAT='SESSION_RUNNER|SAFEGUARDS|FRAMEWORK_LEARNINGS|RECOMMENDED_SKILLS|CONTEXT_TEMPLATE|CLAUDE_TEMPLATE|BOOTSTRAP\.md|methodology_dashboard|methodology_trim|context_budget|quality_ratchet|SESSION_NOTES|HANDOFFS\.md|CHANGELOG\.md|ROADMAP\.md|docs/methodology|\.quality-gates|\.context-budget'
cd "$PORTFOLIO" || exit 3
printf '%-26s %-6s %-8s %-8s %-6s %-6s %-6s %-6s %-6s\n' project atroot ignored tracked docm# CLAUDE ctxbud qgates ci
for p in "${ADOPTERS[@]}"; do
  r=0; ig=0; tr=0
  for f in "${FILES[@]}"; do
    if [ -e "$p/$f" ]; then
      r=$((r+1))
      if git -C "$p" check-ignore -q "$f" 2>/dev/null; then ig=$((ig+1))
      elif git -C "$p" ls-files --error-unmatch "$f" >/dev/null 2>&1; then tr=$((tr+1)); fi
    fi
  done
  dm=$(ls "$p/docs/methodology" 2>/dev/null | wc -l | tr -d ' ')
  c1=$(grep -cE "$PAT" "$p/CLAUDE.md" 2>/dev/null); c2=$(grep -cE "$PAT" "$p/.context-budget.json" 2>/dev/null)
  c3=$(grep -cE "$PAT" "$p/.quality-gates.json" 2>/dev/null)
  c4=$(cat "$p"/.github/workflows/* 2>/dev/null | grep -cE "$PAT")
  printf '%-26s %-6s %-8s %-8s %-6s %-6s %-6s %-6s %-6s\n' "$p" "$r" "$ig" "$tr" "$dm" "${c1:-na}" "${c2:-na}" "${c3:-na}" "${c4:-0}"
done
