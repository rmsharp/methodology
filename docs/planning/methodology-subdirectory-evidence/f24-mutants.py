"""The mutants of the BL-101 F24 pass (S299), for mutate-p7.py (the runner is not specific to P7). Each is (id, file, old, new,
test classes): `old` occurs exactly once in `file`; the classes are where the killing test is expected to live (the fast ones
first). Written from the new code, one mutant per behaviour F24 added, as F10's were (f10-mutants.py): the lesson of F5's
first round (7 of 30 survived, each a behaviour no test pinned) is that the mutant to aim at is the behaviour the tests were
written together with the code and not before it. Round 2 (`ROUND2`) is aimed at the behaviours round 1 did not name.
Usage: mutate-p7.py <scratch clone of the commit under test> f24-mutants.py [ids...]"""
T = "bin/migrate-layout"
PURE = ["TestThePureRules"]
CMD = ["TestAPackagersIgnoreFileIsEvaluated"]
BOTH = PURE + CMD

MUTANTS = [
    # --- brace lists
    ("B01", T, 'return None if "}" in pattern else [pattern]', 'return [pattern]', PURE),
    ("B02", T, '    if end < 0 or not commas:\n        return None\n', '    if end < 0:\n        return None\n', PURE),
    ("B03", T, 'elif pattern[i] == "," and depth == 1:', 'elif pattern[i] == ",":', PURE),
    ("B04", T, 'cuts = [first] + commas + [end]', 'cuts = [first] + commas[:1] + [end]', PURE),
    ("B05", T, 'any(matches(parts, path.split("/")) for parts in compiled)', 'all(matches(parts, path.split("/")) for parts in compiled)', PURE),
    # --- one segment of a glob
    ("S01", T, '        if c == "\\\\":\n            return None\n        if c == "*":', '        if c == "*":', PURE),
    ("S02", T, '            if seg[i + 1:i + 2] == "(":\n                return None\n            out.append("[^/]*")', '            out.append("[^/]*")', PURE),
    ("S03", T, 'elif c in "+@!?" and seg[i + 1:i + 2] == "(":', 'elif False:', PURE),
    ("S04", T, 'negated = seg[j:j + 1] in ("!", "^")', 'negated = seg[j:j + 1] in ("!",)', PURE),
    ("S05", T, 'if end < 0 or seg[j] == "]":', 'if end < 0:', PURE),
    ("S06", T, 'if "[" in body or "\\\\" in body:', 'if "\\\\" in body:', PURE),
    ("S07", T, 'out.append("[^/]*")', 'out.append("[^/]+")', PURE),
    ("S08", T, 'out.append("[^/]")', 'out.append("[^/]?")', PURE),
    # S09 (the run of stars collapsed to one) and the `.*` / `.` forms of S07 and S08 are EQUIVALENT mutants and not run: a segment
    # holds no `/`, and `a[^/]*[^/]*b` matches what `a[^/]*b` does (the collapse is there so a long run of stars cannot make the
    # regular expression back-track without end, which no test asserts).
    ("S10", T, 'out.append("[%s%s]" % ("^" if negated else "", members))', 'out.append("[%s%s]" % ("", members))', PURE),
    # --- a whole glob
    ("G01", T, 'if "" in segments[1:-1]:', 'if False:', PURE),
    ("G02", T, '                parts.append(None)\n                continue', '                parts.append(re.compile("[^/]*"))\n                continue', PURE),
    ("G03", T, 'done[(i, j)] = j < len(path) if i == len(parts) - 1 else', 'done[(i, j)] = True if i == len(parts) - 1 else', PURE),
    ("G04", T, 'for k in range(j, len(path) + 1)', 'for k in range(j + 1, len(path) + 1)', PURE),
    ("G05", T, 'parts[i].fullmatch(path[j])', 'parts[i].match(path[j])', PURE),
    ("G06", T, 'done[(i, j)] = j == len(path)', 'done[(i, j)] = True', PURE),
    ("G07", T, 'except re.error:\n                return None\n        compiled.append(parts)', 'except re.error:\n                pass\n        compiled.append(parts)', PURE),
    # --- vsce's list
    ("L01", T, 'if not line or line.startswith("#"):\n            continue\n        negated', 'if not line:\n            continue\n        negated', PURE),
    ("L02", T, 'line = raw.strip().strip("\\ufeff").strip()', 'line = raw.strip()', PURE),
    ("L03", T, 'enumerate(re.split(r"\\r\\n|\\r|\\n", text), 1)', 'enumerate(re.split(r"\\n", text), 1)', PURE),
    ("L04", T, 'enumerate(re.split(r"\\r\\n|\\r|\\n", text), 1)', 'enumerate(re.split(r"\\r|\\n", text), 1)', PURE),
    ("L05", T, 'patterns = [line] + ([] if VSCE_LEAF_GLOB_RE.search(line) else [line + "**" if line.endswith("/") else line + "/**"])', 'patterns = [line]', PURE),
    ("L06", T, 'patterns = [line] + ([] if VSCE_LEAF_GLOB_RE.search(line) else [line + "**" if line.endswith("/") else line + "/**"])', 'patterns = [line] + [line + "**" if line.endswith("/") else line + "/**"]', PURE),
    ("L07", T, '[line + "**" if line.endswith("/") else line + "/**"]', '[line + "/**"]', PURE),
    ("L08", T, '(negations if negated else entries).extend', '(entries if negated else negations).extend', PURE),
    ("L09", T, 'globs = [vsce_glob(p[1:] if negated else p) for p in patterns]', 'globs = [vsce_glob(p) for p in patterns]', PURE),
    ("L10", T, 'for name in VSCE_DEFAULT_IGNORE:\n        entries.append', 'for name in ():\n        entries.append', PURE),
    ("L11", T, 'negations += [(0, "!" + name, vsce_glob(name)) for name in VSCE_NOT_IGNORED]', 'pass', PURE),
    ("L12", T, 'return [] if hit and any(g(path) for _n, _t, g in negations) else hit', 'return hit', PURE),
    ("L13", T, 'return [] if hit and any(g(path) for _n, _t, g in negations) else hit', 'return [] if hit and all(g(path) for _n, _t, g in negations) else hit', PURE),
    ("L14", T, 'entries.append((0, "(vsce default) " + name, vsce_glob(name)))', 'entries.append((0, name, vsce_glob(name)))', PURE),
    ("L15", T, '            unread += 1\n            continue\n        (negations', '            continue\n        (negations', PURE),
    ("L16", T, 'VSCE_LEAF_GLOB_RE = re.compile(r"(^|/)[^/]*\\*[^/]*\\Z")', 'VSCE_LEAF_GLOB_RE = re.compile(r"[^/]*\\*[^/]*\\Z")', PURE),
    # --- the exposure
    ("E01", T, '        if now and not covering(dest):\n            exposed.append(src)\n            for key in now:', '        if now:\n            exposed.append(src)\n            for key in now:', PURE),
    ("E02", T, '        if now and not covering(dest):\n            exposed.append(src)\n            for key in now:', '        if not covering(dest):\n            exposed.append(src)\n            for key in now:', PURE),
    ("E03", T, 'by_line.setdefault(key, []).append(src)\n    lines = [{"line": n, "text": s, "files": sorted(set(f))}', 'by_line.setdefault(key, []).append(dest)\n    lines = [{"line": n, "text": s, "files": sorted(set(f))}', PURE),
    ("E04", T, 'key=lambda kv: (kv[0][0] == 0, kv[0]))]', 'key=lambda kv: kv[0])]', PURE),
    ("E05", T, '"files": sorted(set(f))} for (n, s), f in sorted(by_line.items(), key=lambda kv: (kv[0][0] == 0, kv[0]))]', '"files": list(f)} for (n, s), f in sorted(by_line.items(), key=lambda kv: (kv[0][0] == 0, kv[0]))]', PURE),
    ("E06", T, 'return {"exposed": sorted(exposed), "lines": lines, "unread": unread}\n\n\nDIR_RE', 'return {"exposed": exposed, "lines": lines, "unread": unread}\n\n\nDIR_RE', PURE),
    # --- the wiring and the text
    ("W01", T, 'for ignore_name, exposure_of in ((".Rbuildignore", pattern_exposure), (".vscodeignore", vscodeignore_exposure)):', 'for ignore_name, exposure_of in ((".Rbuildignore", pattern_exposure),):', CMD),
    ("W02", T, '        if ignore_name not in root_tracked:\n            continue\n', '', CMD + ["TestAPatternThatStopsMatchingIsListed"]),
    ("W03", T, '                            if ln["line"]:\n', '                            if True:\n', CMD),
    ("W04", T, 'vsce = x["file"] == ".vscodeignore"', 'vsce = False', CMD),
    ("W05", T, '"a glob" if vsce else "a regular expression"', '"a regular expression"', CMD),
    ("W06", T, 'for ignore_name, exposure_of in ((".Rbuildignore", pattern_exposure), (".vscodeignore", vscodeignore_exposure)):', 'for ignore_name, exposure_of in ((".Rbuildignore", vscodeignore_exposure), (".vscodeignore", pattern_exposure)):', CMD),
]

# Round 2 is written after round 1 is read, against the behaviours no round-1 mutant named.
ROUND2 = [
    ("R01", T, 'if "" in segments[1:-1]:', 'if "" in segments[:-1]:', PURE),
    ("R02", T, '        if exposure["exposed"]:\n            row = next((x for x in out["config"]["paths"] if x["file"] == ignore_name), None)', '        if exposure["exposed"] or exposure["unread"]:\n            row = next((x for x in out["config"]["paths"] if x["file"] == ignore_name), None)', CMD),
    ("R03", T, '% (len(p["lines"]), len(p["exposed"]), NEW_DIR, NEW_DIR, VSCE_PINNED))', '% (len(p["exposed"]), len(p["lines"]), NEW_DIR, NEW_DIR, VSCE_PINNED))', CMD),
    ("R04", T, 'VSCE_PINNED = "vsce 3.9.2, minimatch 10.2.5"', 'VSCE_PINNED = "vsce 3.6.0, minimatch 3.0.4"', CMD),
    ("R05", T, 'enumerate(re.split(r"\\r\\n|\\r|\\n", text), 1)', 'enumerate(re.split(r"\\r\\n|\\r|\\n", text), 0)', PURE),
    ("R06", T, 'ln["text"].replace("(vsce default) ", "", 1)', 'ln["text"]', CMD),
    ("R07", T, '"text": first["text"].strip()[:200], "mentions": 0,\n                       "code_mentions": 0, "names": [], "untracked": False}', '"text": first["text"].strip()[:200], "mentions": 0,\n                       "code_mentions": 0, "names": [], "untracked": True}', CMD),
    ("R08", T, 'negated = line.startswith("!")', 'negated = False', PURE),
    ("R09", T, 'elif c in "+@!?" and seg[i + 1:i + 2] == "(":', 'elif c in "+@!" and seg[i + 1:i + 2] == "(":', PURE),
    ("R10", T, 'elif c in "+@!?" and seg[i + 1:i + 2] == "(":', 'elif c in "@!?" and seg[i + 1:i + 2] == "(":', PURE),
    ("R11", T, 'elif c in "+@!?" and seg[i + 1:i + 2] == "(":', 'elif c in "+!?" and seg[i + 1:i + 2] == "(":', PURE),
    ("R12", T, 'elif c in "+@!?" and seg[i + 1:i + 2] == "(":', 'elif c in "+@?" and seg[i + 1:i + 2] == "(":', PURE),
    ("R13", T, '    alternatives = expand_braces(pattern)\n    if alternatives is None:\n        return None\n', '    alternatives = expand_braces(pattern) or [pattern]\n', PURE),
    ("R14", T, 'entries.append((0, "(vsce default) " + name, vsce_glob(name)))', 'entries.append((1, "(vsce default) " + name, vsce_glob(name)))', PURE),
]
