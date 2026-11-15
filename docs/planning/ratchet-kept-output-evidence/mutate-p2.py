#!/usr/bin/env python3
"""Mutation round for P2 (S450): quality_ratchet.py 1.6.0, the code that keeps a failing gate's output.

Each mutant rewrites one place in a scratch copy of starter-kit/quality_ratchet.py (every `old` text must occur in
the tool exactly once); the six new classes of tools/test_quality_ratchet.py then run against that copy with
`-f` (stop at the first failure). A mutant is KILLED when they do not all pass, and SURVIVES when they do.
Run from anywhere:  python3 docs/planning/ratchet-kept-output-evidence/mutate-p2.py [first [last]] [M12 M26 ...]

Two controls come first, so a zero from this instrument means something: M00 changes nothing and must SURVIVE
(the classes pass on the unmutated copy), and M01 removes the call that hands a result to the keeper and must be
KILLED. The four older load-sensitive classes (terminal and signal tests) are not run: they test code this round
does not touch and flake with the machine's load.
"""
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CLASSES = ["TestAGateThatDidNotPassKeepsItsOutput", "TestWhereTheOutputGoesAndHowLongItStays",
           "TestKeepingNeverChangesTheRun", "TestWhatIsKeptOfALongStream", "TestWhatThePersonSees",
           "TestRunGatesHandsEachResultToTheKeeper"]

# (name, [(old, new), ...])
MUTANTS = [
    ("M00 CONTROL: nothing changed (must SURVIVE)", []),
    ("M01 CONTROL: run_gates never calls the keeper (must be KILLED)",
     [("        if keep is not None:\n            keep(results[-1], memo.get(g.get(\"command\")))\n", "")]),
    ("M02 a timed-out command is kept",
     [('if result["status"] == "pass" or raw is None or raw[3]:', 'if result["status"] == "pass" or raw is None:')]),
    ("M03 a passing gate is kept",
     [('if result["status"] == "pass" or raw is None or raw[3]:', 'if raw is None or raw[3]:')]),
    ("M04 a gate with no command reaches the keeper's body",
     [('if result["status"] == "pass" or raw is None or raw[3]:', 'if result["status"] == "pass" or raw[3]:')]),
    ("M05 a shared command is written once per gate", [("if cmd not in self.saved:", "if True:")]),
    ("M06 every failure warns", [("if not self.warned:", "if True:")]),
    ("M07 the folder is named by the LAST gate over a command", [("self.gates_over[cmd][0]", "self.gates_over[cmd][-1]")]),
    ("M08 the .gitignore holds something else", [('f.write("*\\n")', 'f.write("# nothing\\n")')]),
    ("M09 the .gitignore is not written",
     [('        with open(os.path.join(self.base, ".gitignore"), "w", newline="\\n") as f:   # every write: the directory stays invisible to git\n            f.write("*\\n")\n', "")]),
    ("M10 a kept file may be overwritten (not exclusive)", [('"x", encoding="utf-8"', '"w", encoding="utf-8"')]),
    ("M11 the second file of a second gets the wrong number", [('f"{stem}-{n}.txt"', 'f"{stem}-{n + 1}.txt"')]),
    ("M12 a stream of exactly the cap is cut", [("if len(b) <= KEEP_HEAD + KEEP_TAIL:", "if len(b) < KEEP_HEAD + KEEP_TAIL:")]),
    ("M13 the head is one byte longer", [("head = b[:KEEP_HEAD].decode", "head = b[:KEEP_HEAD + 1].decode")]),
    ("M14 the tail is one byte longer", [("b[len(b) - KEEP_TAIL:]", "b[len(b) - KEEP_TAIL - 1:]")]),
    ("M15 a split head character becomes U+FFFD", [('head = b[:KEEP_HEAD].decode("utf-8", "ignore")', 'head = b[:KEEP_HEAD].decode("utf-8", "replace")')]),
    ("M16 a split tail character becomes U+FFFD", [('tail = b[len(b) - KEEP_TAIL:].decode("utf-8", "ignore")', 'tail = b[len(b) - KEEP_TAIL:].decode("utf-8", "replace")')]),
    ("M17 the omitted count is one over", [("{len(b) - kept} bytes omitted", "{len(b) - kept + 1} bytes omitted")]),
    ("M18 the kept count is the caps, not what was kept",
     [('kept = len(head.encode("utf-8")) + len(tail.encode("utf-8"))', "kept = KEEP_HEAD + KEEP_TAIL")]),
    ("M19 pruning removes the newest", [("key=_kept_order, reverse=True", "key=_kept_order, reverse=False")]),
    ("M20 one file too many stays", [("keep = names[:KEEP_FILES]\n", "keep = names[:KEEP_FILES + 1]\n")]),
    ("M21 the file just written is not protected", [("if just_written not in keep:", "if False:")]),
    ("M22 the protected file is kept on top of five", [("keep = keep[:max(KEEP_FILES - 1, 0)] + [just_written]", "keep = keep[:KEEP_FILES] + [just_written]")]),
    ("M23 a link is counted and pruned as a kept file",
     [(" and not os.path.islink(os.path.join(folder, n))]", "]")]),
    ("M24 a link is written through", [("    if os.path.islink(path):\n        raise OSError", "    if False:\n        raise OSError")]),
    ("M25 a missing parent is made (makedirs)", [("        os.mkdir(path)\n", "        os.makedirs(path)\n")]),
    ("M26 a made-safe name is not lowercased", [("re.sub(r\"[^a-z0-9._-]\", \"_\", name.lower())", "re.sub(r\"[^a-z0-9._-]\", \"_\", name)")]),
    ("M27 the name hash is five digits", [(".hexdigest()[:6]}\"", ".hexdigest()[:5]}\"")]),
    ("M28 the readable part is not cut", [('"_", name.lower())[:48]', '"_", name.lower())[:480]')]),
    ("M29 a leading dot is not made safe", [('if safe[:1] in (".", "-"):', 'if safe[:1] in ("-",):')]),
    ("M30 a leading hyphen is not made safe", [('if safe[:1] in (".", "-"):', 'if safe[:1] in (".",):')]),
    ("M31 a long plain-looking name is its own folder", [("{0,63}$", "{0,200}$")]),
    ("M32 do_run passes no keeper", [("snap = run_gates(root, cfg, keep=keeper)", "snap = run_gates(root, cfg)")]),
    ("M33 run_gates hands the keeper no raw output", [('keep(results[-1], memo.get(g.get("command")))', "keep(results[-1], None)")]),
    ("M34 an empty kept map is stored", [("if keeper is not None and keeper.kept:", "if keeper is not None:")]),
    ("M35 --run prints nothing about kept output", [('        render(snap, "quality gates — run")\n        show_kept(root, cfg, snap)\n', '        render(snap, "quality gates — run")\n')]),
    ("M36 --status prints nothing about kept output", [('f"citing it{R}")\n        show_kept(root, cfg, snap)\n', 'f"citing it{R}")\n')]),
    ("M37 a stored path may name any directory", [('parts[1] not in ("", ".", "..")', "True")]),
    ("M38 a stored path need not start with the directory", [("parts[0] == KEEP_DIR", "True")]),
    ("M39 a stored path need not be a kept file's name", [("_KEPT_NAME.match(parts[2])", "True")]),
    ("M40 a stored path that is a link is printed", [("                if os.path.isfile(path) and not os.path.islink(path):\n", "                if os.path.isfile(path):\n")]),
    ("M41 a gate folder that is a link is counted", [("if os.path.islink(path) or not os.path.isdir(path):", "if not os.path.isdir(path):")]),
    ("M42 the on-disk line names the OLDEST across folders", [("_kept_order(top)[:2] > _kept_order(newest[0])[:2]", "_kept_order(top)[:2] < _kept_order(newest[0])[:2]")]),
    ("M43 a directory that is a link is scanned", [("if not os.path.isdir(base) or os.path.islink(base):", "if not os.path.isdir(base):")]),
    ("M44 the start time is taken when the file is written, not before the first gate",
     [("        self.started = datetime.now(timezone.utc)\n", "        self.started = None\n"),
      ("        stem = f\"{self.started.strftime", "        self.started = datetime.now(timezone.utc)\n        stem = f\"{self.started.strftime")]),
    ("M45 no commit reads as an empty name", [('head_sha(root) or "nohead"', 'head_sha(root) or ""')]),
    ("M46 only OSError is caught", [("except Exception as e:   # not only OSError", "except OSError as e:   # not only OSError")]),
    ("M47 the warning goes to stdout",
     [('could not keep the output of gate {name}: {e}{R}", file=sys.stderr)', 'could not keep the output of gate {name}: {e}{R}")')]),
    ("M48 same-second files sort by name, not by their number", [("int(m.group(3) or 1)", "1")]),
    ("M49 the on-disk count counts files twice", [("files, folders = files + len(names), folders + 1", "files, folders = files + 2 * len(names), folders + 1")]),
    ("M50 a failure to build the keeper is silent", [('        print(f"{YEL}quality-ratchet: could not keep the output of this run: {e}{R}", file=sys.stderr)\n', "        pass\n")]),
]


def run_one(src, name, edits):
    out = src
    for old, new in edits:
        if out.count(old) != 1:
            return "BAD", f"the old text occurs {out.count(old)} times: {old[:60]!r}", 0.0
        out = out.replace(old, new)
    with tempfile.TemporaryDirectory() as t:
        (Path(t) / "starter-kit").mkdir()
        (Path(t) / "tools").mkdir()
        (Path(t) / "starter-kit" / "quality_ratchet.py").write_text(out, encoding="utf-8")
        shutil.copy(REPO / "tools" / "test_quality_ratchet.py", Path(t) / "tools")
        started = time.time()
        p = subprocess.run([sys.executable, str(Path(t) / "tools" / "test_quality_ratchet.py"), "-f", *CLASSES],
                           capture_output=True, text=True, cwd=t)
        killers = [m.group(1) for m in re.finditer(r"^(?:FAIL|ERROR): (\w+)", p.stderr, re.M)]
        return ("KILLED" if p.returncode else "SURVIVED"), (killers[0] if killers else ""), time.time() - started


def main():
    src = (REPO / "starter-kit" / "quality_ratchet.py").read_text(encoding="utf-8")
    ids = [a for a in sys.argv[1:] if a.startswith("M")]          # e.g. M12 M26: only those mutants
    nums = [int(a) for a in sys.argv[1:] if a.isdigit()]
    lo, hi = (nums[0] if nums else 0), (nums[1] if len(nums) > 1 else len(MUTANTS) - 1)
    for i, (name, edits) in enumerate(MUTANTS):
        if (ids and name.split()[0] not in ids) or not lo <= i <= hi:
            continue
        verdict, by, secs = run_one(src, name, edits)
        print(f"{verdict:8} {name}  ({secs:.0f} s)", flush=True)
        if by:
            print(f"           {'by' if verdict == 'KILLED' else '!'} {by}", flush=True)


if __name__ == "__main__":
    main()
