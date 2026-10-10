"""The mutants of the BL-101 F10 and F11 pass (S290), for mutate-p7.py (the runner is not specific to P7). Each is (id, file, old,
new, test classes): `old` occurs exactly once in `file`; the classes are where the killing test is expected to live (the fast
ones first). Written from the new code, one mutant per behaviour F10 and F11 added, after the lesson of F5's first round (7 of
30 survived, each a behaviour no test pinned): a mutant named for a behaviour the tests were written together with the code, not
before it, is the one to aim at. Usage: mutate-p7.py <scratch clone of the commit under test> f10-mutants.py [ids...]"""
T = "bin/migrate-layout"
PURE = ["TestThePureRules"]
CMD = ["TestAPatternThatStopsMatchingIsListed"]
BOTH = PURE + CMD

MUTANTS = [
    # --- F11: the pattern list a program reads is config, the gitignore apart
    ("G01", T, ' and low != ".gitignore"', '', PURE),
    ("G02", T, 'return low.startswith(".") and low.endswith("ignore")', 'return low.endswith("ignore")', PURE),
    ("G03", T, 'low.endswith("ignore") and low != ".gitignore"', '"ignore" in low and low != ".gitignore"', PURE),
    ("G04", T, 'low.endswith(CONFIG_EXT) or is_pattern_list(low):', 'low.endswith(CONFIG_EXT):', PURE),
    ("G05", T, 'low.endswith(CONFIG_EXT) or is_pattern_list(low):', 'low.endswith(CONFIG_EXT) or is_pattern_list(path.lower()):', PURE),
    # --- F10: the rule as a function
    ("P01", T, 'rules.append((number, line, re.compile(line, re.IGNORECASE)))', 'rules.append((number, line, re.compile(line)))', PURE),
    ("P02", T, '            if not line:\n                continue\n            if POSIX', '            if not line or line.startswith("#"):\n                continue\n            if POSIX', PURE),
    ("P03", T, '            if not line:\n                continue\n            if POSIX', '            if not line.strip():\n                continue\n            if POSIX', PURE),
    ("P04", T, '            if POSIX_CLASS_RE.search(line):', '            if False:', PURE),
    ("P05", T, r'POSIX_CLASS_RE = re.compile(r"\[:\^?[a-z]+:\]")', r'POSIX_CLASS_RE = re.compile(r"\[:[a-z]+:\]")', PURE),
    ("P06", T, '            except re.error:\n                unread += 1', '            except re.error:\n                pass', PURE),
    ("P07", T, 'prefixes = ["/".join(parts[:i]) for i in range(1, len(parts) + 1)]', 'prefixes = [path]', PURE),
    ("P08", T, 'prefixes = ["/".join(parts[:i]) for i in range(1, len(parts) + 1)]', 'prefixes = ["/".join(parts[:i]) for i in range(1, len(parts))]', PURE),
    ("P09", T, 'any(r[2].search(p) for p in prefixes)', 'any(r[2].match(p) for p in prefixes)', PURE),
    ("P10", T, '        if now and not covering(dest):', '        if now:', PURE),
    ("P11", T, '        if now and not covering(dest):', '        if not covering(dest):', PURE),
    ("P12", T, 'by_line.setdefault((number, line), []).append(src)', 'by_line.setdefault((number, line), []).append(dest)', PURE),
    ("P13", T, '"text": s, "files": sorted(f)} for (n, s), f in sorted(by_line.items())]', '"text": s, "files": f} for (n, s), f in sorted(by_line.items())]', PURE),
    ("P14", T, 'return {"exposed": sorted(exposed), "lines": lines, "unread": unread}', 'return {"exposed": exposed, "lines": lines, "unread": unread}', BOTH),
    ("P15", T, 'for (n, s), f in sorted(by_line.items())]', 'for (n, s), f in by_line.items()]', PURE),
    ("P16", T, 'prefixes = ["/".join(parts[:i]) for i in range(1, len(parts) + 1)]', 'prefixes = ["/".join(parts[:i]) for i in range(max(1, len(parts) - 1), len(parts) + 1)]', PURE),
    # --- F10: the wiring in scan_hits
    ("W01", T, '    if ".Rbuildignore" in tracked_files(root):', '    if True:', CMD),
    ("W02", T, '        if exposure["exposed"]:', '        if exposure["exposed"] or exposure["unread"]:', CMD),
    ("W03", T, 'row = {"file": ".Rbuildignore", "line": first["line"], "text": first["text"].strip()[:200], "mentions": 0,', 'row = {"file": ".Rbuildignore", "line": first["line"], "text": first["text"].strip()[:200], "mentions": 1,', CMD),
    ("W04", T, '                out["config"]["files"] += 1\n', '', CMD),
    ("W05", T, '            row["patterns"] = exposure\n', '            pass\n', CMD),
    ("W06", T, 'row = next((x for x in out["config"]["paths"] if x["file"] == ".Rbuildignore"), None)', 'row = None', CMD),
    ("W07", T, 'row = {"file": ".Rbuildignore", "line": first["line"],', 'row = {"file": ".Rbuildignore", "line": 1,', CMD),
    ("W08", T, '(root / ".Rbuildignore").read_text(encoding="utf-8", errors="replace")', '(root / ".Rbuildignorex").read_text(encoding="utf-8", errors="replace")', CMD),
    ("W09", T, '"code_mentions": 0, "names": [], "untracked": False}\n                out["config"]["paths"].append(row)', '"code_mentions": 0, "names": ["x"], "untracked": False}\n                out["config"]["paths"].append(row)', CMD),
    # --- F10: the text
    ("R01", T, 'key=lambda x: (x["code_mentions"] == 0 and not x.get("patterns"), x["file"])', 'key=lambda x: (x["code_mentions"] == 0, x["file"])', CMD),
    ("R02", T, 'more = "" if x["mentions"] <= 1 else', 'more = "" if x["mentions"] == 1 else', CMD),
    ("R03", T, ' or not x["mentions"] or x.get("patterns") else "   [comment lines only]"', ' or not x["mentions"] else "   [comment lines only]"', CMD),
    ("R04", T, 'shown = ", ".join(names[:3]) +', 'shown = ", ".join(names[:30]) +', CMD),
    ("R05", T, '(" and %d more" % (len(names) - 3) if len(names) > 3 else "")', '""', CMD),
    ("R06", T, '                    if p:\n                        for ln in p["lines"]:', '                    if False:\n                        for ln in p["lines"]:', CMD),
    ("R07", T, '% (len(p["lines"]), len(p["exposed"]), NEW_DIR, NEW_DIR))', '% (len(p["exposed"]), len(p["lines"]), NEW_DIR, NEW_DIR))', CMD),
    ("R08", T, '                        if p["unread"]:', '                        if False:', CMD),
    ("R09", T, '"      line %d: %s  stops covering %s" % (ln["line"], ln["text"][:120], shown)', '"      line %d: %s  stops covering %s" % (ln["line"] + 1, ln["text"][:120], shown)', CMD),
    ("R10", T, 'a line such as ^%s$ would"', 'a line such as %s would"', CMD),
]
