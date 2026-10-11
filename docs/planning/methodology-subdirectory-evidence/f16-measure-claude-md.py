#!/usr/bin/env python3
"""BL-101 F16 evidence: which CLAUDE.md lines does bin/migrate-layout's text rewrite change, and how many sit under a
Learnings heading?

Row F16 of findings-register.md: the tool rewrites a project's CLAUDE.md as text, and 9 of the 16 lines it changed at
`church_growth` sit inside the project's own `### Project-specific Learnings`, which record past events at the old paths.
This script asks the same question of every adopter, read-only: it reads each adopter's COMMITTED CLAUDE.md with
`git show` (nothing in a real tree is opened, written or run), applies the tool's own rule (`token_rewriter` over the
manifest's whole legacy-to-new table, tier all), and counts the changed lines outside and inside a Learnings region.

    python3 -I docs/planning/methodology-subdirectory-evidence/f16-measure-claude-md.py [--lines]

--lines also prints each changed line inside a Learnings region, with the standing-alone paths the rule would change and the
text around them, so the reader can judge each one: that judgement is the reader's, not this script's.

Limits, stated where the number is: a Learnings region is the text under a heading whose own text contains "earning", up to
the next heading of the same or a higher level (a project that names it otherwise is counted as outside); the mapping is the
manifest's whole table, so it is an upper bound for an adopter that has not synced every file; `church_growth` is read at the
commit before its move (it is migrated, and its HEAD already carries the new paths); the adopters are the ones on this
machine at the time of the run, so the output is a measurement of that day, not a figure to re-derive years later.
"""
import re
import subprocess
import sys
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

sys.dont_write_bytecode = True

REPO = Path(__file__).resolve().parents[3]
DEV = Path.home() / "Development"
ADOPTERS = ["model_project_constructor", "feedback-loop-comparison", "nprcgenekeepr", "mts-system", "vscode_quarto_ext",
            "Philippians", "airqino", "chat_verification", "church_growth", "dalia_martinez_funeral", "claude_work", "wsfct"]
READ_AT = {"church_growth": "62f7d8a~1"}  # already moved: the commit before its move still has the old paths
HEADING = re.compile(r"^(#+)\s+(.*)")
CONTEXT_BEFORE, CONTEXT_AFTER = 110, 70


def load_tool():
    loader = SourceFileLoader("migrate_layout", str(REPO / "bin" / "migrate-layout"))
    mod = module_from_spec(spec_from_loader("migrate_layout", loader))
    sys.path.insert(0, str(REPO / "bin"))
    loader.exec_module(mod)
    return mod


def main():
    show_lines = "--lines" in sys.argv[1:]
    tool = load_tool()
    moves = [{"src": legacy, "dest": tool.NEW_LAYOUT[srcname]} for srcname, legacy, _disp in tool.DISTRIBUTION]
    mapping = tool.logical_map(moves, "all")
    pattern = tool.token_pattern(mapping)
    total_out = total_in = 0
    for name in ADOPTERS:
        ref = READ_AT.get(name, "HEAD")
        shown = subprocess.run(["git", "-C", str(DEV / name), "show", ref + ":CLAUDE.md"], capture_output=True, text=True)
        if shown.returncode != 0:
            print("%-28s no committed CLAUDE.md" % name)
            continue
        inside, level, n_out, n_in, samples = False, 0, 0, 0, []
        for line in shown.stdout.split("\n"):
            heading = HEADING.match(line)
            if heading:
                depth = len(heading.group(1))
                if inside and depth <= level:
                    inside = False
                if not inside and "earning" in heading.group(2):
                    inside, level = True, depth
            hits = list(pattern.finditer(line))
            if not hits:
                continue
            if inside:
                n_in += 1
                samples.append("      | %s  ==> %s" % (
                    " || ".join(line[max(0, h.start() - CONTEXT_BEFORE):h.end() + CONTEXT_AFTER].strip() for h in hits[:2]),
                    ", ".join(sorted({h.group(0) for h in hits}))))
            else:
                n_out += 1
        total_out += n_out
        total_in += n_in
        print("%-28s changed lines: %3d outside Learnings, %3d inside   (read at %s)" % (name, n_out, n_in, ref))
        if show_lines and samples:
            print("\n".join(samples))
    print("TOTAL changed lines: %d outside, %d inside (%d)" % (total_out, total_in, total_out + total_in))


if __name__ == "__main__":
    main()
