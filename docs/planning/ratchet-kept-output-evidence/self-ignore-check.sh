#!/bin/bash
# Evidence [E3] for docs/planning/ratchet-kept-output-plan.md: a directory that holds its own
# .gitignore containing `*` is invisible to `git status` in a project that never edited its own
# .gitignore, and git still reports a real change beside it. Writes only to a throwaway directory.
set -u
T=$(mktemp -d "${TMPDIR:-/tmp}/self-ignore.XXXXXX")
trap 'rm -rf "$T"' EXIT
cd "$T" || exit 2
git init -q . && git config user.email t@t && git config user.name t
printf 'tracked\n' > tracked.txt && git add tracked.txt && git commit -q -m base
echo "git: $(git --version)"
mkdir .quality-gates-output
echo "1. the directory exists and holds one file, no .gitignore of its own yet:"
printf 'FAIL: a test\n' > .quality-gates-output/out.txt
printf '   git status --porcelain -> [%s]\n' "$(git status --porcelain | tr '\n' '|')"
printf '*\n' > .quality-gates-output/.gitignore
echo "2. the same directory after it writes its own .gitignore containing *:"
printf '   git status --porcelain -> [%s]\n' "$(git status --porcelain | tr '\n' '|')"
printf '   git check-ignore -v on the file -> %s\n' "$(git check-ignore -v .quality-gates-output/out.txt)"
printf '   git status --ignored --porcelain -> [%s]\n' "$(git status --ignored --porcelain | tr '\n' '|')"
echo "3. a real change beside it is still reported:"
printf 'edited\n' >> tracked.txt
printf '   git status --porcelain -> [%s]\n' "$(git status --porcelain | tr '\n' '|')"
echo "4. git add -A stages nothing from the directory:"
git add -A && printf '   staged -> [%s]\n' "$(git diff --cached --name-only | tr '\n' '|')"
echo "5. a project with committed results, as the seed allows (the results file itself is tracked):"
git reset -q && git rm -q --cached -r . >/dev/null 2>&1; git add tracked.txt
printf '{}\n' > .quality-gates-results.json && git add .quality-gates-results.json
printf '   tracked results file + ignored directory: status -> [%s]\n' "$(git status --porcelain | tr '\n' '|')"
