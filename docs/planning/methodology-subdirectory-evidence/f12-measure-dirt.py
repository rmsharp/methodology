#!/usr/bin/env python3
"""BL-101 F12 evidence: would a rule that stops counting generated files as dirt clear any remaining adopter?

Row F12 of findings-register.md: bin/migrate-layout refuses a tree whose only dirt is generated files its own plan moves
(`airqino`: untracked at the root). The register left the rule to him: count untracked generated files as not-dirt, or let
each adopter ignore them. This script asks the question of the population, read-only (nothing in a real tree is written or
run; `git status` is the only command run in a real tree), in three parts:

  1. each adopter's dirt, classified by git's status code (untracked, or tracked and changed) and by whether the path is
     one of the tool's own GENERATED names, with the number of adopters each candidate rule would leave clean:
       rule A  untracked generated files are not dirt (what the register's row describes)
       rule B  rule A, and a modified TRACKED generated file is not dirt either
  2. the tool's own dry run, in a `git clone --no-local` of the two adopters whose dirt is a generated file, with the real
     modified file copied over the clone's so the clone carries the real dirt: what the refusal says today
  3. what git does to a MODIFIED tracked file that `git mv` carries and that `reset --hard` rolls back, in a scratch
     repository: the two facts rule B would have to handle

    python3 -I -B docs/planning/methodology-subdirectory-evidence/f12-measure-dirt.py

Limits, stated where the number is: untracked files are read in git's default mode (a whole untracked directory is ONE
entry), which is faithful here because the GENERATED names live at the project root and a root-level file is always listed
by itself; the adopters are the ones on this machine at the time of the run, so the output is a measurement of that day and
not a figure to re-derive later; an adopter that has already moved under `methodology/` is not measured (it is not a
candidate for another move); rule A and rule B are read as sets of paths, so a project whose only dirt is the generated
files reads clean under the rule, which is what the rule would let the tool proceed on.
"""
import shutil
import subprocess
import sys
import tempfile
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

sys.dont_write_bytecode = True

REPO = Path(__file__).resolve().parents[3]
DEV = Path.home() / "Development"
ADOPTERS = ["model_project_constructor", "feedback-loop-comparison", "nprcgenekeepr", "mts-system", "vscode_quarto_ext",
            "Philippians", "airqino", "chat_verification", "church_growth", "dalia_martinez_funeral", "claude_work", "wsfct"]
REAL_DIRT = ["mts-system", "chat_verification"]  # part 2: the two whose dirt is a generated file


def load_tool():
    loader = SourceFileLoader("migrate_layout", str(REPO / "bin" / "migrate-layout"))
    mod = module_from_spec(spec_from_loader("migrate_layout", loader))
    sys.path.insert(0, str(REPO / "bin"))
    loader.exec_module(mod)
    return mod


def status_entries(project):
    """[(xy, path)] from `git status --porcelain=v1 -z`, git's default untracked mode."""
    r = subprocess.run(["git", "-C", str(project), "status", "--porcelain=v1", "-z"], capture_output=True, text=True)
    entries, out, i = r.stdout.split("\0"), [], 0
    while i < len(entries):
        entry = entries[i]
        i += 1
        if not entry:
            continue
        out.append((entry[:2], entry[3:]))
        if entry[0] in "RC":
            i += 1  # a rename or copy carries its source as the next field
    return out


def part1(tool):
    print("== 1. each adopter's dirt, by status code and by the tool's GENERATED names (%s)" % ", ".join(tool.GENERATED))
    measured = clear_a = clear_b = 0
    for name in ADOPTERS:
        path = DEV / name
        if not (path / ".git").exists():
            print("  %-26s not on this machine" % name)
            continue
        kind = tool.resolve_layout(path)[0]
        if kind == "new":
            print("  %-26s migrated (not measured)" % name)
            continue
        entries = status_entries(path)
        gen_untracked = [p for xy, p in entries if xy == "??" and p in tool.GENERATED]
        gen_modified = [p for xy, p in entries if xy != "??" and p in tool.GENERATED]
        other = [p for xy, p in entries if p not in tool.GENERATED]
        measured += 1
        if not entries:
            print("  %-26s clean tree" % name)
            continue
        a = not other and not gen_modified
        b = not other
        clear_a += a
        clear_b += b
        print("  %-26s %d entries: generated untracked %d, generated modified-tracked %d, other %d   rule A clears it: %s   rule B clears it: %s"
              % (name, len(entries), len(gen_untracked), len(gen_modified), len(other), "yes" if a else "no", "yes" if b else "no"))
    print("  measured %d adopters not yet moved; trees rule A leaves clean: %d; trees rule B leaves clean: %d" % (measured, clear_a, clear_b))


def part2():
    print("\n== 2. the tool's dry run in a --no-local clone, the real modified generated file copied over the clone's")
    tool_path = REPO / "bin" / "migrate-layout"
    for name in REAL_DIRT:
        src = DEV / name
        if not (src / "dashboard_history.jsonl").is_file():
            print("  %-20s no dashboard_history.jsonl on this machine" % name)
            continue
        with tempfile.TemporaryDirectory() as tmp:
            clone = Path(tmp) / name
            subprocess.run(["git", "clone", "-q", "--no-local", str(src), str(clone)], check=True)
            shutil.copyfile(src / "dashboard_history.jsonl", clone / "dashboard_history.jsonl")
            r = subprocess.run([sys.executable, "-I", "-B", str(tool_path), str(clone)], capture_output=True, text=True)
            lines = r.stdout.splitlines()
            refused = []
            if "REFUSED:" in lines:
                for line in lines[lines.index("REFUSED:"):]:
                    if not line.strip():
                        break
                    refused.append(line)
            print("  %-20s exit %d; clone status: %s" % (name, r.returncode,
                  "; ".join("%s %s" % (xy.strip() or "?", p) for xy, p in status_entries(clone)) or "clean"))
            for line in refused:
                print("    " + line[:600])


def scratch(tmp):
    """A repository with h.jsonl committed ('one') and then modified ('one', 'two'), moved with git mv, NOT committed."""
    def git(*args):
        return subprocess.run(["git", "-C", tmp, *args], capture_output=True, text=True, check=True).stdout
    git("init", "-q", ".")
    git("config", "user.email", "probe@example.invalid")
    git("config", "user.name", "probe")
    (Path(tmp) / "h.jsonl").write_text("one\n")
    git("add", "h.jsonl")
    git("commit", "-q", "-m", "base")
    (Path(tmp) / "h.jsonl").write_text("one\ntwo\n")  # the adopter's uncommitted line
    (Path(tmp) / "methodology").mkdir()
    git("mv", "h.jsonl", "methodology/h.jsonl")
    return git


def part3():
    print("\n== 3. git mv of a MODIFIED tracked file, in a scratch repository: the two paths the tool would have to handle")
    with tempfile.TemporaryDirectory() as tmp:  # the apply commits: what the tree reads afterwards
        git = scratch(tmp)
        git("commit", "-q", "-m", "move")
        print("  after the move commit, status:                 %r" % git("status", "--porcelain").rstrip())
        print("  committed at the new path / worktree there:    %r / %r"
              % (git("show", "HEAD:methodology/h.jsonl"), (Path(tmp) / "methodology" / "h.jsonl").read_text()))
    with tempfile.TemporaryDirectory() as tmp:  # the apply fails before its commit: rollback() runs `reset --hard HEAD`
        git = scratch(tmp)
        git("reset", "-q", "--hard", "HEAD")
        print("  after rollback's reset --hard HEAD, h.jsonl:   %r  (the adopter's second line is gone)"
              % (Path(tmp) / "h.jsonl").read_text())


def main():
    tool = load_tool()
    part1(tool)
    part2()
    part3()


if __name__ == "__main__":
    main()
