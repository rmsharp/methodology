#!/bin/sh
# installed by context_budget.py — refuses a commit that GROWS a budgeted file past its ceiling. A commit
# that shrinks such a file always passes. The tool is looked for where it was installed and at its
# twin in the other layout (the root, or methodology/), so a project that moves its methodology
# files does not leave a hook that cannot find it.
top=$(git rev-parse --show-toplevel)
for t in "context_budget.py" "methodology/context_budget.py"; do
    if [ -f "$top/$t" ]; then
        exec python3 "$top/$t" --precommit
    fi
done
echo "context-budget: context_budget.py not found under $top (looked for: "context_budget.py" "methodology/context_budget.py") -- refusing, not passing." >&2
echo "  Re-run the tool's install-hook from where it now lives." >&2
exit 2
