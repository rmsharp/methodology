#!/usr/bin/env python3
"""Mutation round for piece 2 (S415). Each mutant breaks ONE guard in a copy of the tree's file,
the four new test classes run, and the mutant must be CAUGHT (at least one test fails).
Every file is restored in a `finally` and the tree is hash-checked at the end.
Usage: python3 s415-mutants.py <tree> <out-file>
"""
import hashlib, subprocess, sys, time
from pathlib import Path

TREE = Path(sys.argv[1])
OUT = Path(sys.argv[2])
CB = "starter-kit/context_budget.py"
ST = "bin/status"
TESTS = ["tools.test_context_budget.TestReleaseOrdering", "tools.test_context_budget.TestReleaseLag",
         "tools.test_context_budget.TestRemoteFlag", "tools.test_context_budget.TestStatusReleaseLag"]

# (name, file, [(old, new), ...])
MUTANTS = [
 ("M01 kill the child only, wait on the pipes with a bound", CB,
  [("os.killpg(p.pid, signal.SIGKILL)", "p.kill()")]),
 ("M02 kill the child only and wait on the pipes without a bound (subprocess.run's behaviour)", CB,
  [("os.killpg(p.pid, signal.SIGKILL)", "p.kill()"), ("p.communicate(timeout=2)", "p.communicate()")]),
 ("M03 no session of its own for the call", CB,
  [("start_new_session=True", "start_new_session=False")]),
 ("M04 GIT_TERMINAL_PROMPT not set", CB,
  [('env = dict(os.environ, GIT_TERMINAL_PROMPT="0")', "env = dict(os.environ)")]),
 ("M05 ssh BatchMode never added", CB,
  [("    _ssh_never_prompts(checkout, env)\n", "    pass\n")]),
 ("M06 a configured core.sshCommand is ignored", CB,
  [("base = configured if rc == 0 and configured else None", "base = None")]),
 ("M07 the environment's GIT_SSH_COMMAND is ignored", CB,
  [('base = env.get("GIT_SSH_COMMAND")', "base = None")]),
 ("M08 a GIT_SSH wrapper is overridden", CB,
  [('    if base is None and "GIT_SSH" in env:\n        return\n', "")]),
 ("M09 releases ordered as text", CB,
  [("return max(keyed)[1] if keyed else None", "return max(t for _k, t in keyed) if keyed else None")]),
 ("M10 a pre-release tag counts as a release", CB,
  [('RELEASE_TAG = re.compile(r"v(\\d+(?:\\.\\d+)*)")', 'RELEASE_TAG = re.compile(r"v(\\d+(?:\\.\\d+)*)[-\\w]*")')]),
 ("M11 one remote call per synced file, not per checkout", CB,
  [("        if d in seen:\n            continue\n", "")]),
 ("M12 --precommit asks the remote", CB,
  [('    if "--precommit" in args:\n        return precommit(root, cfg)',
    '    if "--remote" in args:\n        check_remote(root, cfg)\n    if "--precommit" in args:\n        return precommit(root, cfg)')]),
 ("M13 a stale checkout is a breach", CB,
  [('"status": "warn",\n                         "findings": [{"kind": "remote"',
    '"status": "over",\n                         "findings": [{"kind": "remote"')]),
 ("M14 a checkout that could not be checked becomes a warn row", CB,
  [('        elif why:\n            notes.append(f"{d}: {why}")',
    '        elif why:\n            rows.append({"path": "(x)", "status": "unmeasured", "reason": why, "findings": []})')]),
 ("M15 a checkout ahead of its remote is called behind", CB,
  [("if release_key(newest) > release_key(tag):", "if release_key(newest) != release_key(tag):")]),
 ("M16 a timeout is reported as an ordinary failure", CB,
  [('    if rc == 124:\n        return None, f"origin did not answer within {timeout} s (timed out)"\n', "")]),
 ("M17 git describe failing is silent", CB,
  [('return None, f"git describe found no release tag ({err.splitlines()[-1] if err else rc})"',
    "return None, None")]),
 ("M18 an origin with no release tags crashes", CB,
  [('    if newest is None:\n        return None, "origin lists no release tag"\n', "")]),
 ("M19 a nearest tag that is not a release crashes", CB,
  [('    if release_key(tag) is None:\n        return None, f"the nearest tag, {tag}, is not a release tag"\n', "")]),
 ("M20 a missing synced checkout is asked anyway", CB,
  [('        if not os.path.isdir(d):\n            notes.append(f"{d} is not a directory")\n            continue\n', "")]),
 ("M21 --remote with nothing synced says nothing", CB,
  [('        return [], ["no synced file is declared"]', "        return [], []")]),
 ("M22 --json loses the not-checked list", CB,
  [('            payload["remote_not_checked"] = remote_notes\n', "            pass\n")]),
 ("M23 bin/status prints before the table", ST,
  [("        rc = report(args.paths, methodology_root, source, str(methodology_root))\n"
    "        line = release_lag_line(methodology_root)\n        if line:\n            print(line)\n        return rc\n",
    "        line = release_lag_line(methodology_root)\n        if line:\n            print(line)\n"
    "        rc = report(args.paths, methodology_root, source, str(methodology_root))\n        return rc\n")]),
 ("M24 bin/status also asks in --source=github", ST,
  [("        return report(args.paths, clone, source, url)",
    "        release_lag_line(clone)\n        return report(args.paths, clone, source, url)")]),
 ("M25 bin/status lets a load failure crash", ST,
  [("    except Exception as e:  # a report", "    except KeyboardInterrupt as e:  # a report")]),
 ("M28 the call uses git's default protocol again", CB,
  [('["git", "-C", checkout, "-c", "protocol.version=0",\n                                "ls-remote",', '["git", "-C", checkout,\n                                "ls-remote",')]),
 ("M26 bin/status leaves bytecode in the checkout", ST,
  [("    sys.dont_write_bytecode = True  # loading it must not leave starter-kit/__pycache__ in a checkout\n", "")]),
 ("M27 bin/status never prints why it could not check", ST,
  [('    return f"remote not checked: {reason}" if reason else None', "    return None")]),
]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:12]


ONLY = sys.argv[3] if len(sys.argv) > 3 else ''
MUTANTS = [m for m in MUTANTS if m[0].startswith(ONLY)]

before = {f: sha(TREE / f) for f in (CB, ST, "tools/test_context_budget.py")}
lines = []
caught = 0
for name, rel, edits in MUTANTS:
    path = TREE / rel
    original = path.read_text()
    text = original
    for old, new in edits:
        assert text.count(old) == 1, f"{name}: pattern found {text.count(old)}x: {old[:60]!r}"
        text = text.replace(old, new)
    began = time.monotonic()
    try:
        path.write_text(text)
        p = subprocess.run([sys.executable, "-m", "unittest", *TESTS], cwd=TREE,
                           capture_output=True, text=True, timeout=300)
        tail = [l for l in p.stderr.splitlines() if l.startswith(("FAIL:", "ERROR:"))]
        verdict = "CAUGHT" if p.returncode != 0 else "SURVIVED"
        caught += verdict == "CAUGHT"
        detail = "; ".join(sorted({l.split(" (")[0].replace("FAIL: ", "").replace("ERROR: ", "") for l in tail}))[:160]
    except subprocess.TimeoutExpired:
        verdict, detail = "CAUGHT", "timed out after 300 s (a hang is a catch)"
        caught += 1
    finally:
        path.write_text(original)
    lines.append(f"{verdict:8s} {name}  [{time.monotonic() - began:5.1f}s]  {detail}")
    OUT.write_text("\n".join(lines) + "\n")

after = {f: sha(TREE / f) for f in before}
lines.append(f"\n{caught} of {len(MUTANTS)} mutants caught")
lines.append("tree restored: " + ("yes, every hash equal" if before == after else f"NO -- {before} vs {after}"))
OUT.write_text("\n".join(lines) + "\n")
print("\n".join(lines))
