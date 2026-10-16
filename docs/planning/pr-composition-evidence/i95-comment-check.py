#!/usr/bin/env python3
"""i95-comment-check.py -- upstream issue #95: re-derive, on upstream's tip alone, every figure the draft
comment (`i95-comment-draft.md`) states about the tool.

Usage:  python3 -I i95-comment-check.py SCRATCH_DIR     (SCRATCH_DIR is created; an existing one is removed)

Reads upstream `main` at the pinned commit with `git archive` (the working tree is never touched), runs the
tool that tree ships (`context_budget.py --status --json`, parsed, never read by eye) against the files that
tree ships, and prints what the draft says: the source lines it cites, the config values, and five cases.
It borrows `export`, `measure`, `seed_project`, `fenced_template` and `sh` from `i95-dayzero.py` (S328), so the
cases the issue's own repro uses are run by the same code.

Cases (each a git-initialised directory holding the tool, the seed config and one file):
  fenced    the template's `## Purpose` placeholder wrapped in the fence, nothing else (the issue's fix 3)
  at-800    the same block padded with ASCII to exactly 800 characters
  at-799    the same, 799 characters (the floor is a strict "fewer than 800")
  cjk-300   a fenced block of 300 CJK characters: 300 characters, 900 bytes
  ascii-800 control: 800 ASCII characters, which the tool accepts
"""
import importlib.util
import os
import re
import shutil
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("i95_dayzero", os.path.join(HERE, "i95-dayzero.py"))
dz = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dz)

UPSTREAM = "f34769f31ca351a520c2da4fa5f9e65b5153bffa"
FENCE_OPEN, FENCE_CLOSE = "<!-- budget:protected -->\n", "\n<!-- /budget:protected -->"


def lines_of(path, wanted):
    src = open(path, encoding="utf-8").read().split("\n")
    return [f"      {n}: {src[n - 1].strip()}" for n in wanted]


def template_with_body(tpl_bytes, body):
    """The template with the `## Purpose` body replaced by `body`, fenced."""
    t = tpl_bytes.decode("utf-8")
    m = re.search(r"(## Purpose\n\n)(.*?)(\n\n---\n)", t, re.S)
    assert m, "no `## Purpose` block in the template"
    return (t[:m.start(2)] + FENCE_OPEN + body + FENCE_CLOSE + t[m.end(2):]).encode("utf-8")


def case(tdir, scratch, name, claude_md, out):
    d = dz.seed_project(tdir, scratch, name, {"CLAUDE.md": claude_md})
    rc, rows = dz.measure(d)
    status, finds = rows["CLAUDE.md"]
    msgs = "; ".join(dz.ANSI.sub("", m) for _, m in finds) or "no finding"
    out.append(f"  {name}: exit {rc}; CLAUDE.md {status}; {msgs}")
    return rc, status, msgs


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    if dz.sh(["git", "rev-parse", "refs/remotes/upstream/main"], cwd=dz.REPO).stdout.strip() != UPSTREAM:
        sys.exit("pinned revision moved: refs/remotes/upstream/main is not " + UPSTREAM[:7])
    scratch = os.path.abspath(sys.argv[1])
    if os.path.exists(scratch):
        shutil.rmtree(scratch)
    os.makedirs(scratch)
    tdir = os.path.join(scratch, "tree")
    dz.export(UPSTREAM, tdir)
    sk = os.path.join(tdir, "starter-kit")
    out = [f"i95-comment-check.py: upstream main {UPSTREAM[:7]}", ""]

    out.append("source lines the draft cites (starter-kit/context_budget.py):")
    out += lines_of(os.path.join(sk, "context_budget.py"), [384, 452, 453, 455])
    out.append("config values the draft cites (starter-kit/context-budget.json):")
    out += lines_of(os.path.join(sk, "context-budget.json"), [34, 43])
    out.append("")

    tpl = open(os.path.join(sk, "CLAUDE_TEMPLATE.md"), "rb").read()
    m = re.search(r"## Purpose\n\n(.*?)\n\n---\n", tpl.decode("utf-8"), re.S)
    body = m.group(1)
    out.append(f"template Purpose placeholder: {len(body.strip())} characters, {len(body.strip().encode())} bytes")
    out.append("cases:")
    results = {}
    results["fenced"] = case(tdir, scratch, "fenced", template_with_body(tpl, body), out)

    def pad(n):
        assert n > len(body.strip())
        return body.strip() + "\n" + "x" * (n - len(body.strip()) - 1)

    for n in (799, 800):
        padded = pad(n)
        assert len(padded.strip()) == n
        results[f"at-{n}"] = case(tdir, scratch, f"at-{n}", template_with_body(tpl, padded), out)
        out.append(f"      (padded to {n}: {n - len(body.strip())} more characters than the placeholder)")

    cjk = ("本项目记录结构化会话的目标与做法。" * 20)[:300]
    assert len(cjk) == 300 and len(cjk.encode()) == 900, (len(cjk), len(cjk.encode()))
    results["cjk-300"] = case(tdir, scratch, "cjk-300", template_with_body(tpl, cjk), out)
    out.append(f"      (the block is {len(cjk)} characters and {len(cjk.encode())} bytes; a bytes count clears the 800 floor)")
    results["ascii-800"] = case(tdir, scratch, "ascii-800", template_with_body(tpl, "x" * 800), out)

    out.append("")
    out.append("the issue's control (seed SESSION_NOTES.md, line 5 wrapped, a `## Session History` heading):")
    notes = open(os.path.join(sk, "SESSION_NOTES.md"), "rb").read()
    d = dz.seed_project(tdir, scratch, "control", {"SESSION_NOTES.md": dz.wrapped_notes(notes)})
    rc, rows = dz.measure(d)
    out.append(f"  exit {rc}; " + "; ".join(f"{p} {s}" for p, (s, _) in rows.items()))

    out.append("")
    checks = [
        ("fenced: exit 2, 'only 182 B'", results["fenced"][0] == 2 and "only 182 B" in results["fenced"][2]),
        ("at-799: refused", results["at-799"][1] == "over"),
        ("at-800: accepted", results["at-800"][1] == "ok"),
        ("cjk-300: refused as 'only 300 B' though 900 bytes", results["cjk-300"][1] == "over" and "only 300 B" in results["cjk-300"][2]),
        ("ascii-800: accepted", results["ascii-800"][1] == "ok"),
        ("control: exit 1 and SESSION_NOTES.md ok", rc == 1 and rows["SESSION_NOTES.md"][0] == "ok"),
    ]
    for label, ok in checks:
        out.append(f"  {'PASS' if ok else 'FAIL'}  {label}")
    print("\n".join(out))
    if not all(ok for _, ok in checks):
        sys.exit(1)


if __name__ == "__main__":
    main()
