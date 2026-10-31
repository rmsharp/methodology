Thanks for the detailed write-up. I reproduced all four findings on `main` @ `f34769f` (the four files involved are unchanged on `main` today), and your control passes. I have built a fix for all four. While doing it I found three things that bear on your suggested fixes. I label them A, B and C so they cannot be mixed up with your findings 1 to 4. ("The tool" means `starter-kit/context_budget.py`.)

**The result.** With my change, a fresh `bin/sync` into an empty project, with `CLAUDE_TEMPLATE.md` copied to `CLAUDE.md`, exits 1 with no row over budget. That is the same exit as your control (`LEARNINGS.md` does not exist yet, so that row is unmeasured). The only finding is a warning that the Purpose section still holds the template's placeholder, and `SESSION_NOTES.md` reads ok.

**A. Fencing the placeholder alone (your finding 3) still exits 2.**
The placeholder under `## Purpose` in `CLAUDE_TEMPLATE.md` is 182 bytes, but the minimum size of a fenced block (`protected_min_bytes`, `starter-kit/context-budget.json:34`) is 800. So with only the fence added, the message changes from "the budget:protected fence is missing" to "the budget:protected block is only 182 B — it looks emptied", and a fresh project still exits 2. The script at the end reproduces this.

There are two ways out:
- Treat a block that still holds the placeholder as unmeasured instead of over budget (your "alternatively").
- Make the placeholder at least 800 bytes. I tried this: 800 passes and 799 does not. But it adds 618 characters to a template every project copies, and a project that never writes its own purpose would then pass the check that exists to notice an emptied one.

I built the first, with one difference: the row reads `warn` rather than unmeasured. The config names a marker string that the template's placeholder contains (`protected_placeholder`, set to `<project-name>`). While the fenced block still contains it, the `CLAUDE.md` row reads `warn`, keeps its size in the table, and prints the remedy "Write your purpose"; the 800-byte minimum is not applied. Once the placeholder is replaced, the minimum applies as before (<800 bytes is under, >=800 passes). "Unmeasured" is the status the tool already uses for a file it cannot measure. Which of the two statuses is better is your design call.

**B. The 800-byte minimum has the same characters-versus-bytes slip as your finding 4.**
At `:453` the tool compares `len(body.strip())`, a count of characters, with `protected_min_bytes`, and `:455` prints that count followed by "B". One line earlier, `:452`, it already records the block's size in bytes (`len(body.encode())`). So fixing only the line cap (`:384`) would leave the tool counting in two different ways. For non-English text the minimum is stricter than its message says: 300 Chinese characters are 900 bytes, yet the tool reports "only 300 B — it looks emptied". (To see it, run the script below after `export BODY=$(python3 -c 'print("目" * 300)')`.) A byte count is never smaller than a character count, so measuring bytes here can only turn refusals into passes, never the reverse.

**C. Measuring the line cap in bytes (your finding 4) changes no result on the projects I can check.**
I have 12 projects that use the framework. Ten declare `max_line_bytes`, all on `SESSION_NOTES.md`. Read at each project's committed `HEAD`, no line goes from within the cap to over it when counted in bytes. The tool's own `measure_file` gives the same count as my script on every file. (Raw bytes and `len(l.encode("utf-8"))` differ only when a file contains invalid UTF-8; the two counts are equal on all 10.)

**The change** is two small commits:
1. The tool: bytes for both the line cap and the minimum, the placeholder warning, the config line that names the marker (`protected_placeholder`), and tests.
2. The two seed files and the pass-control test you describe. In `SESSION_NOTES.md`, line 5 is wrapped and a second `##` heading is added; in `CLAUDE_TEMPLATE.md`, the Purpose placeholder is fenced. The test, in `bin/tests.sh`, syncs into a temporary project, copies the template to `CLAUDE.md`, and checks that no row is over budget and the only finding is the placeholder warning. A paired control plants a 400-byte line in the seed `SESSION_NOTES.md` and checks that the same probe reports the breach.

It is built and passing on my own copy of the repository, which has other changes beside it, so I would re-run it on your `main` before opening anything. If you want it, say so and I'll open a pull request; otherwise I'll leave the fix with you.

**Repro for A and B**, run against `f34769f`:

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

🤖 Generated with [Claude Code](https://claude.com/claude-code)
