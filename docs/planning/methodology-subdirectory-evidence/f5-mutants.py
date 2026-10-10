"""The mutants of the BL-101 F5 pass (S289), for mutate-p7.py (the runner is not specific to P7). Each is (id, file, old, new,
test classes): `old` occurs exactly once in `file`; the classes are where the killing test is expected to live (the fast
ones first). Round 1 was written from the new code, one mutant per behaviour F5 added: 23 of 30 were killed, and the 7 that
survived (F17, F18, F20, F22, F23, F27, F28) each named a behaviour no test pinned. Round 2 re-ran those seven against
the tests added for them (usage: mutate-p7.py <scratch clone> f5-mutants.py F17 F18 F20 F22 F23 F27 F28)."""
T = "bin/migrate-layout"
PURE = ["TestThePureRules"]
HITS = ["TestTheMachineReadFilesAreListedApartFromProse", "TestTheHitsItWillNotRewrite", "TestWhatTheHitsSayAboutHooksAndDirectories"]
LIST = ["TestTheMachineReadFilesAreListedApartFromProse"]

MUTANTS = [
    # --- round 1: the sorting, as a function
    ("F01", T, 'HOOK_DIRS = (".githooks/", ".husky/")', 'HOOK_DIRS = (".githooks/",)', PURE),
    ("F02", T, 'HOOK_FILES = (".pre-commit-config.yaml",)', 'HOOK_FILES = ()', PURE),
    ("F03", T, '    if low.endswith(".verify.sh") or re.match(r"verify[^/]*\\.sh$", low):', '    if low.endswith(".verify.sh"):', PURE),
    ("F04", T, '    if low.endswith(".verify.sh") or re.match(r"verify[^/]*\\.sh$", low):\n        return "proofs"\n', '', PURE),
    ("F05", T, '    if low.endswith(PROSE_EXT):\n        return "other"\n', '', PURE),
    ("F06", T, '|conftest\\.py)$")', ')$")', PURE),
    ("F07", T, '    if low in CONFIG_NAMES or low.endswith(CONFIG_EXT):', '    if low.endswith(CONFIG_EXT):', PURE),
    ("F08", T, '    if low.endswith(SCRIPT_EXT) or text.startswith("#!"):', '    if low.endswith(SCRIPT_EXT):', PURE),
    ("F09", T, 'MACHINE_READ = ("ci", "hooks", "tests", "proofs", "scripts", "config")', 'MACHINE_READ = ("ci", "hooks", "tests", "proofs", "scripts")', PURE),
    ("F10", T, 'CATEGORIES = MACHINE_READ + ("harness", "ledger", "other")', 'CATEGORIES = MACHINE_READ + ("ledger", "harness", "other")', PURE),
    # --- round 1: the scan and the listing
    ("F11", T, '        visit(path, text, hit_category(path, text), rewritten)', '        visit(path, text, hit_category(path), rewritten)', HITS),
    ("F12", T, 'COMMENT_STARTS = ("#", "//", "<!--", "/*", "*", ";", "%")', 'COMMENT_STARTS = ()', LIST),
    ("F13", T, '                number, line = first_code or first\n', '                number, line = first\n', LIST),
    ("F14", T, '                number, line = first_code or first\n', '                number, line = first_code\n', LIST),
    ("F15", T, '"code_mentions": code, "names": sorted(found), "untracked": untracked})', '"code_mentions": code, "names": sorted(found), "untracked": False})', LIST),
    ("F16", T, '"code_mentions": code, "names": sorted(found), "untracked": untracked})', '"code_mentions": code, "names": [], "untracked": untracked})', LIST),
    ("F17", T, '                    code += len(names)\n', '                    code += 1\n', LIST),
    ("F18", T, '    for c in MACHINE_READ:\n        out[c]["paths"].sort(key=lambda x: x["file"])\n', '', LIST),
    ("F19", T, '            if cat in MACHINE_READ:\n                found.update(names)', '            if cat in MACHINE_READ and False:\n                found.update(names)', LIST),
    ("F20", T, '                    out.append("    %s:%d  %s%s%s%s" % (x["file"], x["line"], x["text"][:120], more,', '                    out.append("    %s:%d  %s%s%s%s" % (x["file"], x["line"], x["text"][:120], "",', LIST),
    ("F21", T, '                                                        "" if x["code_mentions"] else "   [comment lines only]",', '                                                        "",', LIST),
    ("F22", T, '                                                        "   [not tracked: per clone]" if x.get("untracked") else ""))\n            else:', '                                                        ""))\n            else:', HITS),
    ("F23", T, 'for x in sorted(c["paths"], key=lambda x: (x["code_mentions"] == 0, x["file"])):', 'for x in sorted(c["paths"], key=lambda x: x["file"]):', LIST),
    ("F24", T, '        out.append("  machine-read files that name a moved path (candidates: this tool does not run them):")\n', '', LIST),
    ("F25", T, '            if cat in MACHINE_READ:\n                for x in sorted(c["paths"]', '            if cat in ():\n                for x in sorted(c["paths"]', LIST),
    ("F26", T, '    out = {c: {"mentions": 0, "files": 0, "sites": [], "paths": []} for c in CATEGORIES}', '    out = {c: {"mentions": 0, "files": 0, "sites": [], "paths": []} for c in CATEGORIES if c != "proofs"}', LIST),
    ("F27", T, 'TEST_DIR_RE = re.compile(r"(^|/)(tests?|specs?|testthat|__tests__)(/|$)")', 'TEST_DIR_RE = re.compile(r"(^|/)(specs?|testthat|__tests__)(/|$)")', PURE),
    ("F28", T, 'TEST_DIR_RE = re.compile(r"(^|/)(tests?|specs?|testthat|__tests__)(/|$)")', 'TEST_DIR_RE = re.compile(r"(^|/)(tests?|testthat|__tests__)(/|$)")', PURE),
    ("F29", T, '|[^/]*\\.test\\.[^/]*|', '|', PURE),
    ("F30", T, '|[^/]*_test\\.[^/]*|', '|', PURE),
]
