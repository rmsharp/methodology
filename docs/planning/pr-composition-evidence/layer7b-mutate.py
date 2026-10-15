#!/usr/bin/env python3
"""Mutants for PR2 Part 2's last layer (bin/migrate-layout), aimed at what the LAYER adds, not at the tool.

    python3 layer7b-mutate.py <candidate-repo> <layer-commit> <work-dir> [--fast] [--e2e-wiring] [--e2e-gates]

The tool and its 280-test suite are the fork's bytes whole (`git rev-parse` equal; the fork mutated them in its own P7 evidence:
`methodology-subdirectory-evidence/p7-mutants.py`, `f10-mutation-round-1.txt`), so this script does not re-mutate the tool's logic.
It aims at the lines this layer wrote and asks whether anything reads them:

  fast    L1  the layout suite's COPIES loses the tool                       expect: the layout suite fails
          L2  one line of the resolver block in the tool is changed          expect: the layout suite fails
          L3  the tool is not a file (the assertion the sync suite regains)  expect: the sync class fails
          L4  the wiring block names a class that does not exist             (the command alone; the e2e below is the real test)
  e2e     W1  the same wiring mutant through the WHOLE shell suite           expect: 1 failed in the summary, exit 1
          G1  the tool's exit code changed so command-level tests fail, then the layer's TWO gates run through the candidate's own
              run_gates() over their real command: expect the count gate PASS at 280 (the hole), the failed gate FAIL, and the
              command run ONCE (a counter line added to the suite file at import). Three variants of the failed gate ride in the
              same call over the same command string (one suite run serves all): V1 gains an `extract`, V2's threshold is 5 (a
              loosening), V3 loses its `timeout_seconds` (which nothing but a loaded machine reads). Expected, and what the run
              printed: V2 reads PASS over the red suite (the mutant the real gate must not become); V3 reads like the real gate (no
              test sees a timeout); V1 reads FAIL for the wrong reason, because its extract measures the test count (280 > 0), so
              it would be red on a green suite too. The first draft of this docstring expected V1 to pass: the hole is a `min`
              count gate, which the first gate already shows, and not a `max 0` gate with an extract.

Everything happens in its OWN clone of <candidate-repo> at <layer-commit>, made under <work-dir>; each mutant is undone with
`git checkout -- .` in that clone, so no uncommitted work of anyone's is at risk (the S300 hazard of `mutate-p7.py`).
Each mutant prints the one line it changed, so a mutant that landed in a docstring or a comment is visible (the S318 hazard).
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
PY = sys.executable


def run(cmd, cwd, env=None, timeout=3600):
    t0 = time.time()
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout, env=env or os.environ)
    return p.returncode, p.stdout + p.stderr, time.time() - t0


def git(cwd, *a):
    return subprocess.run(["git", "-C", str(cwd), *a], capture_output=True, text=True, check=True).stdout


def mutate(root, rel, old, new, what):
    p = Path(root) / rel
    text = p.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise SystemExit("refused: %s: %r occurs %d times in %s" % (what, old[:60], text.count(old), rel))
    p.write_text(text.replace(old, new), encoding="utf-8")
    changed = [l for l in git(root, "diff", "-U0", "--", rel).splitlines() if l[:1] in "+-" and l[:3] not in ("+++", "---")]
    print("  changed %s:" % rel)
    for l in changed:
        print("    " + l[:170])


def restore(root):
    git(root, "checkout", "--", ".")


def verdict(code, out, expect_fail):
    tail = [l for l in out.splitlines() if l.startswith(("Ran ", "OK", "FAILED"))]
    got = "FAILED" if code != 0 else "passed"
    ok = (code != 0) == expect_fail
    return "%s -> exit %s, %s [%s]" % ("KILLED" if (code != 0 and expect_fail) else ("SURVIVED" if expect_fail else "expected pass"),
                                       code, "; ".join(tail[-3:]) or got, "as expected" if ok else "NOT AS EXPECTED")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo"); ap.add_argument("commit"); ap.add_argument("work")
    ap.add_argument("--fast", action="store_true"); ap.add_argument("--e2e-wiring", action="store_true")
    ap.add_argument("--e2e-gates", action="store_true")
    a = ap.parse_args()
    root = Path(a.work) / "mutants"
    if root.exists():
        subprocess.run(["rm", "-rf", str(root)], check=True)
    Path(a.work).mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "clone", "--no-local", "-q", a.repo, str(root)], check=True)
    git(root, "checkout", "-q", a.commit)
    print("mutants in a fresh clone at %s (%s dirty paths)" % (git(root, "rev-parse", "--short", "HEAD").strip(),
                                                              len(git(root, "status", "--short").splitlines())))
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    wiring_old = "TestThePureRules TestUsageAndNothingToDo >/dev/null"
    wiring_new = "TestNoSuchClassHere TestUsageAndNothingToDo >/dev/null"

    if a.fast:
        print("\nL1 COPIES loses the tool")
        mutate(root, "tools/test_layout_resolver.py", '"bin/check-handoff",   # the checkers\' layer\n              "bin/migrate-layout")',
               '"bin/check-handoff")', "L1")
        print("  " + verdict(*run([PY, "tools/test_layout_resolver.py"], root, env)[:2], True)); restore(root)
        print("\nL2 one line of the resolver block in the tool")
        mutate(root, "bin/migrate-layout", 'return "half", None, found', 'return "half", None, ()', "L2")
        print("  " + verdict(*run([PY, "tools/test_layout_resolver.py"], root, env)[:2], True)); restore(root)
        print("\nL3 the tool is not a file (the assertion the sync suite regains)")
        subprocess.run(["git", "-C", str(root), "mv", "bin/migrate-layout", "bin/migrate-layout-x"], check=True)
        print("  moved bin/migrate-layout -> bin/migrate-layout-x")
        print("  " + verdict(*run([PY, "tools/test_sync_layouts.py", "TestSyncRefusesWhatWouldDamageAProject"], root, env)[:2], True))
        git(root, "reset", "-q", "--hard", a.commit)
        print("\nL4 the wiring block's command names a class that does not exist (the command alone)")
        mutate(root, "bin/tests.sh", wiring_old, wiring_new, "L4")
        cmd = [PY, "tools/test_migrate_layout.py", "TestNoSuchClassHere", "TestUsageAndNothingToDo"]
        print("  " + verdict(*run(cmd, root, env)[:2], True)); restore(root)

    if a.e2e_wiring:
        print("\nW1 the wiring mutant through the whole shell suite")
        mutate(root, "bin/tests.sh", wiring_old, wiring_new, "W1")
        code, out, secs = run(["bash", "bin/tests.sh"], root, env)
        keep = [l for l in out.splitlines() if "migration tool" in l or l.startswith("== Summary")]
        print("  exit %s in %.0f s" % (code, secs))
        for l in keep:
            print("   " + l[:200])
        restore(root)

    if a.e2e_gates:
        print("\nG1 the layer's two gates over a red command-level suite, through the candidate's own run_gates()")
        counter = str(Path(a.work) / "g1-counter")
        Path(counter).write_text("")
        mutate(root, "bin/migrate-layout", 'return 0 if report["checks"]["ok"] else 4', 'return 0 if report["checks"]["ok"] else 5', "G1 tool")
        suite = root / "tools" / "test_migrate_layout.py"
        text = suite.read_text(encoding="utf-8")
        first, rest = text.split("\n", 1)
        suite.write_text(first + '\nopen(__import__("os").environ["S322_COUNTER"], "a").write("x")   # G1: one mark per suite run\n' + rest,
                         encoding="utf-8")
        cfg = json.loads((root / ".quality-gates.json").read_text(encoding="utf-8"))
        gates = [g for g in cfg["gates"] if g["name"].startswith("migrate-layout-unit-tests")]
        failed = next(g for g in gates if g["name"] == "migrate-layout-unit-tests-failed")
        gates = gates + [dict(failed, name="V1-failed-with-extract", extract="Ran (\\d+) tests"),
                         dict(failed, name="V2-failed-threshold-5", threshold=5),
                         {k: v for k, v in dict(failed, name="V3-failed-no-timeout").items() if k != "timeout_seconds"}]
        print("  gates: " + ", ".join("%s (%s %s, %s s, extract %s)" % (g["name"], g["direction"], g["threshold"],
                                                                    g.get("timeout_seconds"), "yes" if "extract" in g else "no") for g in gates))
        probe = ("import importlib.util,json,sys\n"
                 "spec=importlib.util.spec_from_file_location('qr','starter-kit/quality_ratchet.py')\n"
                 "qr=importlib.util.module_from_spec(spec); spec.loader.exec_module(qr)\n"
                 "cfg=json.loads(sys.argv[1])\n"
                 "res=qr.run_gates('.',cfg,600)\n"
                 "rows=res if isinstance(res,list) else res.get('gates',res)\n"
                 "for r in rows: print('%-34s measured=%s status=%s' % (r['name'], r['measured'], r['status']))\n")
        code, out, secs = run([PY, "-c", probe, json.dumps({"version": 1, "gates": gates})], root, dict(env, S322_COUNTER=counter))
        print("  run_gates exit %s in %.0f s" % (code, secs))
        for l in out.splitlines()[-6:]:
            print("   " + l[:200])
        print("  suite executions (marks in the counter): %d" % len(Path(counter).read_text()))
        restore(root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
