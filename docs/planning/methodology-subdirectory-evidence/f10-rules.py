#!/usr/bin/env python3
"""BL-101 F10 and F11 measurement (S290): what each candidate rule would add over the 10 adopters, BEFORE any was built.

Read-only. Usage: python3 -I f10-rules.py <the directory f5-population.py wrote> <tool revision> [--rows]
The tool revision is the one BEFORE F10 (S290: aae6c22): `git show <rev>:bin/migrate-layout` is loaded as the tool, so the figures
are what the tool said then, not what it says now (F11 has since moved `.vscodeignore` out of `other`). Rules measured, each over
the clones f5-population.py left (the S286 pins, synced in the clone, tier all):
  S  broad stem (the register's F10 wording): a non-comment line of a machine-read file or an ignore-style file naming a moved file
     by its stem (SESSION_RUNNER, CHANGELOG, dashboard, ...) with no whole name on that line. The files the tool moves, and the
     root .gitignore it rewrites, are not read.
  M  module stem: the same, only for the moved .py tools, word-bounded.
  P  pattern: a line of a root .Rbuildignore, read as R reads it (every non-empty line a case-insensitive regular expression,
     a line that starts with # included; a line that matches a path or a directory above it covers it), that covers a moved file
     where it is and no line covers it where it goes. S290's first draft of this script had no directory rule and read 21 lines;
     with it, as the tool reads, 22 lines cover 143 entries of the moved-or-generated map (`^docs$` covers the 122 moved files under docs/).
  G  an ignore-style file (a dot-file that ends in `ignore`) that the tool at <rev> files under `other`, with prose.
"""
import importlib.machinery
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

CANON = Path(__file__).resolve().parents[3]
args = [a for a in sys.argv[1:] if not a.startswith("--")]
POP = Path(args[0])
REV = args[1]
ROWS = "--rows" in sys.argv


def load_tool():
    """The tool at REV, beside the real bin/ helpers it imports (a copy in a scratch directory, never the working one)."""
    home = Path(tempfile.mkdtemp(prefix="f10-tool-"))
    (home / "bin").mkdir()
    src = subprocess.run(["git", "-C", str(CANON), "show", REV + ":bin/migrate-layout"], capture_output=True, text=True, check=True).stdout
    (home / "bin" / "migrate-layout").write_text(src, encoding="utf-8")
    for name in ("_manifest.py", "_manifest_reader.py"):
        (home / "bin" / name).symlink_to(CANON / "bin" / name)
    for name in ("starter-kit", "tools", "docs"):
        (home / name).symlink_to(CANON / name)
    loader = importlib.machinery.SourceFileLoader("ml", str(home / "bin" / "migrate-layout"))
    sys.path.insert(0, str(home / "bin"))
    spec = importlib.util.spec_from_loader("ml", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


ml = load_tool()
COMMENT = ml.COMMENT_STARTS


def git(clone, *args):
    r = subprocess.run(["git", "--no-optional-locks", "-C", str(clone), *args], capture_output=True, text=True, errors="replace")
    return r.stdout


def stems_of(mapping):
    out = {}
    for src in mapping:
        base = src.rsplit("/", 1)[-1]
        if base.startswith(".") or "." not in base:
            continue
        out[re.sub(r"\.(md|py|json|jsonl|html)$", "", base)] = base
    return out


def main():
    tot = {"S": [0, 0], "M": [0, 0], "P": [0, 0], "G": [0, 0]}
    new_s = 0
    for rj in sorted(POP.glob("*.json")):
        name = rj.stem
        rep = json.loads(rj.read_text(encoding="utf-8"))
        if rep["status"] != "ok":
            print("%-26s %s" % (name, rep["status"]))
            continue
        clone = POP / "clones" / name
        mapping = ml.logical_map(rep["moves"], rep["tier"])
        stems = stems_of(mapping)
        lit = ml.token_pattern(mapping)
        stem_re = re.compile(r"(?<![\w.-])(%s)(?![\w-])" % "|".join(re.escape(s) for s in sorted(stems, key=len, reverse=True)))
        py_stems = {s for s, b in stems.items() if b.endswith(".py")}
        mod_re = re.compile(r"(?<![\w.-])(%s)(?![\w-]|\.py)" % "|".join(re.escape(s) for s in sorted(py_stems, key=len, reverse=True)))
        res = {"S": {}, "M": {}, "P": {}, "G": {}}
        for path in git(clone, "ls-files").splitlines():
            if path in mapping or path == ".gitignore":
                continue  # a file the tool moves, or rewrites as text, is not a file that names one
            f = clone / path
            try:
                text = f.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            cat = ml.hit_category(path, text)
            base = path.rsplit("/", 1)[-1].lower()
            ignoreish = base.startswith(".") and base.endswith("ignore")
            if cat in ml.MACHINE_READ or ignoreish:
                for n, line in enumerate(text.splitlines(), 1):
                    if line.lstrip().startswith(COMMENT):
                        continue
                    if lit.search(line):
                        continue
                    for m in stem_re.finditer(line):
                        res["S"].setdefault(path, []).append((n, m.group(1), line.strip()[:110]))
                    for m in mod_re.finditer(line):
                        res["M"].setdefault(path, []).append((n, m.group(1), line.strip()[:110]))
            if ignoreish and cat == "other" and lit.search(text):
                res["G"].setdefault(path, []).append((0, "", "%d literal mention(s)" % len(lit.findall(text))))
            if path == ".Rbuildignore":
                rules = []
                for n, line in enumerate(text.splitlines(), 1):
                    if not line:
                        continue
                    try:
                        rules.append((n, line, re.compile(line, re.I)))
                    except re.error:
                        continue

                def covering(p):
                    parts = p.split("/")
                    return [r for r in rules if any(r[2].search("/".join(parts[:i])) for i in range(1, len(parts) + 1))]
                for src, dest in mapping.items():
                    now = covering(src)
                    if now and not covering(dest):
                        for n, line, _rx in now:
                            res["P"].setdefault(path, []).append((n, src, line))
        line = "%-26s" % name
        for k in "SMPG":
            files = len(res[k])
            # P rows are (line, moved file, text): count the distinct lines, and say how many moved files they cover
            hits = len({(p, r[0]) for p, v in res[k].items() for r in v}) if k == "P" else sum(len(v) for v in res[k].values())
            tot[k][0] += files
            tot[k][1] += hits
            line += "  %s: %d file(s) %d line(s)" % (k, files, hits)
            if k == "P" and files:
                line += " covering %d moved file(s)" % len({r[1] for v in res[k].values() for r in v})
        listed = {x["file"] for c in ml.MACHINE_READ for x in rep["not_rewritten"][c]["paths"]}
        fresh = [p for p in res["S"] if p not in listed]
        new_s += len(fresh)
        line += "  S new to the F5 list: %d" % len(fresh)
        print(line)
        if ROWS:
            for k in "SMPG":
                for p, rows in sorted(res[k].items()):
                    for r in rows[:6]:
                        print("    [%s] %s:%s  %s  | %s" % (k, p, r[0], r[1], r[2]))
                    if len(rows) > 6:
                        print("    [%s] %s: ... %d more" % (k, p, len(rows) - 6))
    print("TOTAL " + "  ".join("%s: %d file(s) %d line(s)" % (k, *tot[k]) for k in "SMPG") + "  S new to the F5 list: %d file(s)" % new_s)


main()
