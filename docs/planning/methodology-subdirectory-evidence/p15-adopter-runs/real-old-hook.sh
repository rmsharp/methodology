#!/bin/sh
# installed by context_budget.py — refuses a commit that GROWS a budgeted file past
# its ceiling. A commit that shrinks such a file always passes.
exec python3 "$(git rev-parse --show-toplevel)/context_budget.py" --precommit
