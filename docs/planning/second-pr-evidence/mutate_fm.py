import hashlib, pathlib, subprocess, sys
root = pathlib.Path(sys.argv[1]); target = root / "starter-kit" / "methodology_trim.py"
orig = target.read_text(encoding="utf-8"); h0 = hashlib.sha256(orig.encode()).hexdigest()
M = [
 ("M1 no blank filter", "if ln.strip() and ln not in now and not _regenerated_partner(ln, spec, now)]",
                         "if ln not in now and not _regenerated_partner(ln, spec, now)]"),
 ("M2 substring membership", "if ln.strip() and ln not in now and not", "if ln.strip() and ln not in zones.front and not"),
 ("M3 no regen carve-out", " and not _regenerated_partner(ln, spec, now)]", "]"),
 ("M4 partner ignores residue", " and nl[:nm.start()] + nl[nm.end():] == residue):", "):"),
 ("M5 partner ignores prefix group", "if (nm and nm.group(1) == m.group(1) and nm.group(3) == m.group(3)\n                    and",
                                       "if (nm and nm.group(3) == m.group(3)\n                    and"),
 ("M6 count off by one", "% (live_rel, len(lost), lost[0][:70]", "% (live_rel, len(lost) + 1, lost[0][:70]"),
 ("M7 quotes last lost line", "lost[0][:70]", "lost[-1][:70]"),
 ("M8 guard never adds", "    if lost:\n        result.add(\n            \"FRONTIER_FRONT_MATTER_UNCOMMITTED\"", "    if False and lost:\n        result.add(\n            \"FRONTIER_FRONT_MATTER_UNCOMMITTED\""),
 ("M10 hz None unguarded", "    if hz is None:\n        return\n    # splitlines() folds", "    # splitlines() folds"),
 ("M11 CRLF not folded", "now = set(zones.front.splitlines())", "now = set(zones.front.split(\"\\n\"))"),
 ("M12 call removed", "    check_front_matter_frontier(repo, path, spec, zones, result)\n", ""),
 ("M13 compares the working tree to itself", "hz = classify_zones(head.decode(\"utf-8\", \"replace\"), spec, Result(path))\n    if hz is None:",
                                              "hz = zones\n    if hz is None:"),
]
try:
    for name, a, b in M:
        n = orig.count(a)
        if n != 1:
            print("%-40s ANCHOR COUNT %d -- not run" % (name, n)); continue
        target.write_text(orig.replace(a, b), encoding="utf-8")
        r = subprocess.run([sys.executable, "tools/test_methodology_trim.py", "TestWriteTimeGuardForAFrontMatterEdit"],
                           cwd=str(root), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        fails = [l.split()[1] for l in r.stdout.splitlines() if l.startswith(("FAIL:", "ERROR:"))]
        print("%-40s %s %s" % (name, "KILLED  by" if r.returncode else "SURVIVED  ", ", ".join(fails)[:150]))
finally:
    target.write_text(orig, encoding="utf-8")
    assert hashlib.sha256(target.read_text(encoding="utf-8").encode()).hexdigest() == h0
    print("restored; sha256 identical")
