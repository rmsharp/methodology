import hashlib, pathlib, subprocess, sys
root = pathlib.Path(sys.argv[1]); target = root / "starter-kit" / "methodology_trim.py"
orig = target.read_text(encoding="utf-8"); h0 = hashlib.sha256(orig.encode()).hexdigest()
M = [("F1a no-entry case treated as declared-none", "        elif live_name in LEDGERS:\n", "        elif True:\n"),
     ("F1b entry case treated as no-entry", "        elif live_name in LEDGERS:\n", "        elif live_name not in LEDGERS:\n"),
     ("F1c marker case loses the pattern text", "            how = (\"supplied from this tool's ledger table by the live basename %s: %r\"\n                   % (live_name, stub))",
                                                "            how = (\"supplied from this tool's ledger table by the live basename %s\" % live_name)"),
     ("F2 refusal says depth again", "the proof was written for a different layout, \"", "the links were rebased for a different depth, \"")]
try:
    for name, a, b in M:
        if orig.count(a) != 1: print("%-45s ANCHOR COUNT %d" % (name, orig.count(a))); continue
        target.write_text(orig.replace(a, b), encoding="utf-8")
        r = subprocess.run([sys.executable, "tools/test_methodology_trim.py", "TestReverify", "TestReverifyRefusesAPrefixItCannotHonour"],
                           cwd=str(root), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        fails = [l.split()[1] for l in r.stdout.splitlines() if l.startswith(("FAIL:", "ERROR:"))]
        print("%-45s %s %s" % (name, "KILLED  by" if r.returncode else "SURVIVED", ", ".join(fails)[:140]))
finally:
    target.write_text(orig, encoding="utf-8")
    assert hashlib.sha256(target.read_text(encoding="utf-8").encode()).hexdigest() == h0
    print("restored; sha256 identical")
