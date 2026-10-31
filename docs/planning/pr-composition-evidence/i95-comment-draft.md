Thanks for the detailed write-up. I reproduced all four findings on `main` @ `f34769f` (the four files involved are unchanged on `main` today), and your control passes. While checking the suggested fixes I found three things that bear on them, and I have built the change with those taken into account. The repros below run against `f34769f`. ("The tool" means `starter-kit/context_budget.py`.)

**1. Fix 3, as first worded, changes the message but not the exit code.** The placeholder under `## Purpose` in `CLAUDE_TEMPLATE.md` is 182 characters (182 bytes), and `protected_min_bytes` is 800 (`starter-kit/context-budget.json:34`). With only the fence added, finding 3 changes from "the budget:protected fence is missing" to "the budget:protected block is only 182 B — it looks emptied", and a fresh project still exits 2:

```sh
M=/path/to/methodology   # checked out at f34769f
R=$(mktemp -d); cp "$M/starter-kit/context_budget.py" "$R/"
cp "$M/starter-kit/context-budget.json" "$R/.context-budget.json"
python3 - "$M" "$R" <<'PY'
import os, re, sys
m, r = sys.argv[1:]
t = open(m + "/starter-kit/CLAUDE_TEMPLATE.md").read()
def fence(x):   # fence the placeholder; BODY=... swaps in other text
    return (x.group(1) + "<!-- budget:protected -->\n" + (os.environ.get("BODY") or x.group(2))
            + "\n<!-- /budget:protected -->" + x.group(3))
t = re.sub(r"(## Purpose\n\n)(.*?)(\n\n---\n)", fence, t, count=1, flags=re.S)
open(r + "/CLAUDE.md", "w").write(t)
PY
(cd "$R" && git init -q && python3 context_budget.py --status; echo "exit=$?")
```

The two ways out that I can see are to treat a still-placeholder purpose as not over budget (your "alternatively"), or to make the placeholder at least 800 characters. I tried the second: 800 characters passes and 799 does not, so it means 618 more characters in a template every project copies, and a project that never wrote its own purpose then passes the check that exists to notice an emptied one. So I built the first, as a warning rather than as "unmeasured": the config names the placeholder text, and while the fenced block still holds it, `CLAUDE.md` reads `warn` with the remedy "Write your purpose", keeps its size in the table, and the 800 floor is not applied. Once the placeholder is replaced the floor applies as before (799 bytes is over, 800 passes). Which of the two statuses is better is your design call.

**2. The 800 floor has the same characters-versus-bytes slip as finding 4.** `starter-kit/context_budget.py:453` compares `len(body.strip())` with `protected_min_bytes`, and `:455` prints that count followed by "B". One line earlier, `:452`, the tool already records `len(body.encode())` as the block's size in bytes. So a fix that changes only the line cap (`:384`) leaves the tool counting two ways. For multi-byte text the floor is stricter than its message says: a fenced block of 300 Chinese characters is 900 bytes, and the tool reports "only 300 B — it looks emptied" (run the repro above after `export BODY=$(python3 -c 'print("目" * 300)')`). A byte count is never smaller than a character count, so measuring bytes here can only turn refusals into passes, never the reverse.

**3. Measuring the line cap in bytes changes no result on the projects I can check.** Of 12 projects of mine that use the framework, 10 declare `max_line_bytes`, all on `SESSION_NOTES.md`. Read at each project's committed `HEAD`, no line goes from within the cap to over it under a byte count, and the tool's own `measure_file` gives the same count as my script on every file. (Raw bytes and `len(l.encode("utf-8"))` differ only when a file contains invalid UTF-8; the two counts are equal on all 10.)

With the change, a fresh `bin/sync` into an empty project, with `CLAUDE_TEMPLATE.md` copied to `CLAUDE.md`, exits 1 with no row over budget, the same exit as your control (`LEARNINGS.md` does not exist yet, so that row is unmeasured). The one finding is the placeholder warning, and `SESSION_NOTES.md` reads ok. Both the line cap and the floor count bytes.

The change is two small commits: the tool (bytes for the cap and the floor, and the placeholder warning) with its tests, then the two seed files, the config line that names the placeholder, and the pass-control test you describe in `bin/tests.sh`, with a control that fails when a seed line goes over the cap. It is built and passing on my own copy of the repository, which has other changes beside it, so I would re-run it on your `main` before opening anything. If you want it, say so and I'll open a pull request; otherwise I'll leave the fix with you.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
