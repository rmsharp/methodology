"""Mutation check for P3 of docs/planning/issue93-trimmer-proof-false-red-plan.md (S266): `--reverify`.

Applies ONE textual mutant at a time to a scratch copy of starter-kit/methodology_trim.py and runs
TestReverify against it. KILLED = at least one test in the class fails or errors; SURVIVED = none does;
INVALID = the search text does not occur exactly once in the pristine source (never scored as a kill).
Where an intended test is named the report says whether that test was among the failures. Nothing under
the repository is written: the copy lives in a temp directory (with the repository's frozen proofs, which
one test lifts).

    python3 docs/planning/issue93-evidence/mutants_p3.py [--validate] [--only=<name substring> ...]

--validate only checks that every search text occurs exactly once, so a stale list is found in a second
rather than after the run. The mutant list was written against the tree at S266's implementation commit;
a later edit to the trimmer can make a search text stop matching, and the runner then says INVALID.
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CLASS = "TestReverify"

M = []


def mut(name, old, new, intended=""):
    M.append((name, old, new, intended))


# --- the lift: what it will and will not splice -------------------------------------------------
mut("a missing required line is not refused",
    '        if line is None:\n            raise ReverifyRefusal("REVERIFY_NOT_LIFTABLE",\n'
    '                                  "%s is not in the frozen proof: it predates',
    '        if False:\n            raise ReverifyRefusal("REVERIFY_NOT_LIFTABLE",\n'
    '                                  "%s is not in the frozen proof: it predates', "missing_any_required")
mut("the whole-line form check is dropped",
    '        if mm is None:\n            raise ReverifyRefusal("REVERIFY_NOT_LIFTABLE",\n'
    '                                  "%s is not in the form',
    '        if False:\n            raise ReverifyRefusal("REVERIFY_NOT_LIFTABLE",\n'
    '                                  "%s is not in the form', "not_in_the_form")
mut("a duplicated line is not refused",
    "    if len(hits) > 1:", "    if False:", "appears_twice")
mut("the line finder only knows KEY= and never KEY = ",
    r'''    hits = re.findall(r"^%s(?:=| = ).*$" % key, text, re.M)''',
    r'''    hits = re.findall(r"^%s(?:=).*$" % key, text, re.M)''', "")
mut("LIVE accepts any non-space text",
    '    ("LIVE", "live", r"LIVE=(%s)" % _PATH_TEXT),', '    ("LIVE", "live", r"LIVE=(\\S+)"),', "shell_payload")
mut("RECORD_START accepts anything up to the last quote",
    '''    ("RECORD_START", "start", r'RECORD_START = r"([^"\\n]*)"'),''',
    '''    ("RECORD_START", "start", r'RECORD_START = r"(.*)"'),''', "python_payload")
mut("RECORD_KIND accepts any word",
    '''r'RECORD_KIND = "(heading|fence)"\'''', '''r'RECORD_KIND = "(.*)"\'''', "not_in_the_form")
mut("FOOTER_MODE accepts any word",
    '''r'FOOTER_MODE = "(separator|none)"\'''', '''r'FOOTER_MODE = "(.*)"\'''', "not_in_the_form")
mut("FENCE_INFO accepts anything",
    '''r'FENCE_INFO = "([A-Za-z0-9_-]*)"\'''', '''r'FENCE_INFO = "(.*)"\'''', "not_in_the_form")
mut("an absolute or parent-relative LIVE/SHARD path is accepted",
    '        if out[field].startswith("/") or ".." in out[field].split("/"):', "        if False:", "not_in_the_form")
mut("a parent-relative path is accepted",
    '        if out[field].startswith("/") or ".." in out[field].split("/"):',
    '        if out[field].startswith("/"):', "not_in_the_form")
mut("an absolute path is accepted",
    '        if out[field].startswith("/") or ".." in out[field].split("/"):',
    '        if ".." in out[field].split("/"):', "not_in_the_form")
mut("a template placeholder in a lifted pattern is accepted",
    '    if "@@" in value:', "    if False:", "not_in_the_form")
mut("a pattern that does not compile is accepted",
    "        re.compile(value)\n    except re.error as e:", "        pass\n    except re.error as e:", "not_in_the_form")
mut("REGEN and STUB are EVALUATED, not parsed as literals",
    "            val = ast.literal_eval(rhs) if rhs is not None else None",
    "            val = eval(rhs) if rhs is not None else None", "expression_in_the_REGEN")
mut("REGEN items are not required to be strings",
    "        shaped = (isinstance(val, list) and all(isinstance(x, str) for x in val) if field == \"regen\"",
    "        shaped = (isinstance(val, list) if field == \"regen\"", "not_in_the_form")
mut("STUB is not required to be a string",
    "                  else isinstance(val, str))", "                  else True)", "not_in_the_form")
mut("a no-space REGEN/STUB line is read as if it had spaces",
    '        rhs = line[len(key) + 3:] if line.startswith(key + " = ") else None',
    "        rhs = line[len(key) + 3:]", "not_in_the_form")
mut("a lifted REGEN/STUB pattern is not compiled or checked",
    "            if pat:\n                _lift_pattern(key, pat)", "            if False:\n                _lift_pattern(key, pat)",
    "not_in_the_form")
mut("an absent REGEN line is not recorded as absent",
    '            out["absent"].append(key)\n', "            pass\n", "no_regen_line")
mut("an absent REGEN line defaults to nothing",
    '            out[field] = [] if field == "regen" else None', '            out[field] = None if field == "regen" else None',
    "no_regen_line")
mut("an absent STUB line defaults to an empty marker instead of None",
    '            out[field] = [] if field == "regen" else None', '            out[field] = [] if field == "regen" else ""',
    "older_than_the_stub_label")
mut("the writer's version is not lifted",
    '    out = {"version": m.group(1) if m else None, "absent": []}', '    out = {"version": None, "absent": []}', "rederived_green")

# --- the filler and the table --------------------------------------------------------------------
mut("a stub marker is keyed by the full path, not the basename",
    "    spec = LEDGERS.get(Path(live_rel).name)\n    return spec.stub_marker.pattern",
    "    spec = LEDGERS.get(live_rel)\n    return spec.stub_marker.pattern", "stub_marker_comes_from")
mut("a stub marker is returned for a ledger with none",
    "    return spec.stub_marker.pattern if spec is not None and spec.stub_marker else \"\"\n\n\ndef reverify",
    "    return spec.stub_marker.pattern if spec is not None and spec.stub_marker else \"x\"\n\n\ndef reverify",
    "stub_marker_comes_from")
mut("the filler drops the regenerated-field patterns",
    '("@@REGEN@@", repr(list(regen_patterns))),', '("@@REGEN@@", "[]"),', "")
mut("a hostile SHARD file name is not refused (SHARD checked only against the name it was asked about)",
    '    ("SHARD", "shard", r"SHARD=(%s)" % _PATH_TEXT),', '    ("SHARD", "shard", r"SHARD=(\\S+)"),',
    "shard_whose_own_file_name")
mut("the filler drops the stub marker",
    '("@@STUB@@", repr(stub_pattern))):', '("@@STUB@@", repr(""))):', "stub")
mut("build_verify stops carrying the stub marker",
    '                         spec.stub_marker.pattern if spec.stub_marker else "")',
    '                         "")', "stub")

# --- reverify(): the path, the refusals, the banner, the verdict --------------------------------
mut("the .verify.sh form is not accepted in place of the shard",
    '    if path.name.endswith(".verify.sh"):', "    if False:", "proof_path_is_accepted")
mut("a missing shard is not refused",
    "[:-len(\".verify.sh\")])\n    if not path.is_file():", "[:-len(\".verify.sh\")])\n    if False:", "missing_shard")
mut("a shard outside a repository is not refused",
    "    if repo is None:\n        result.add(\"NOT_A_REPO\", \"%s is not inside a git work tree\" % path, exit_code=3)\n        return result\n    shard_rel",
    "    if False:\n        result.add(\"NOT_A_REPO\", \"%s is not inside a git work tree\" % path, exit_code=3)\n        return result\n    shard_rel",
    "missing_shard")
mut("a shard with no proof is not refused",
    "    if not proof.is_file():\n        result.add(\"REVERIFY_NO_PROOF\"", "    if False:\n        result.add(\"REVERIFY_NO_PROOF\"",
    "no_proof_beside")
mut("a proof naming another shard is not refused",
    '    if g["shard"] != shard_rel:', "    if False:", "different_shard")
mut("the stub marker is not supplied when the proof predates it",
    "        stub = stub_pattern_for(g[\"live\"])\n", "        stub = \"\"\n", "older_than_the_stub_label")
mut("the substitution is not announced",
    "    if stub is None:\n        stub = stub_pattern_for(g[\"live\"])\n        result.add(\"REVERIFY_SUBSTITUTED\",",
    "    if stub is None:\n        stub = stub_pattern_for(g[\"live\"])\n        (lambda *a, **k: None)(\"REVERIFY_SUBSTITUTED\",",
    "older_than_the_stub_label")
mut("the banner stops saying it is not the shipped artifact",
    '"today\'s logic against this shard, NOT the artifact that was shipped; the frozen "\n               "proof is untouched. Nothing was written."',
    '"today\'s logic against this shard; the frozen "\n               "proof is untouched. Nothing was written."', "banner_says")
mut("the banner stops saying nothing was written",
    '"proof is untouched. Nothing was written."', '"proof is untouched."', "banner_says")
mut("the banner names today's version as the writer's",
    '% (shard_rel, TRIM_VERSION, g["version"] or "?", g["live"], g["kind"], g["footer"]))',
    '% (shard_rel, TRIM_VERSION, TRIM_VERSION, g["live"], g["kind"], g["footer"]))', "frozen_red_proof")
mut("the proof is run with no repository as its cwd",
    'subprocess.run(["bash", "-c", script], cwd=str(repo),', 'subprocess.run(["bash", "-c", script],', "another_repository")
mut("a scratch file is left in the repository",
    '    try:\n        run = subprocess.run(["bash", "-c", script]',
    '    (repo / "reverify.tmp").write_text(script, encoding="utf-8")\n    try:\n        run = subprocess.run(["bash", "-c", script]',
    "writes_nothing")
mut("a missing bash is not caught",
    "    except OSError as e:\n        result.add(\"REVERIFY_CANNOT_RUN\"", "    except ZeroDivisionError as e:\n        result.add(\"REVERIFY_CANNOT_RUN\"",
    "missing_bash")
mut("a signal death is passed through as a negative status",
    "    rc = run.returncode if run.returncode >= 0 else 3", "    rc = run.returncode", "killed_by_a_signal")
mut("the verdict never raises the exit status",
    "               exit_code=rc or None)", "               exit_code=None)", "rederived_green")
mut("the verdict exit is capped at 1 (a stub finalize reads as a plain FAIL)",
    "               exit_code=rc or None)", "               exit_code=min(rc, 1) or None)", "older_than_the_stub_label")

# --- the CLI ---------------------------------------------------------------------------------------
mut("--write is allowed beside --reverify", '(("--file", opts.file), ("--write", opts.write),', '(("--file", opts.file),',
    "refuses_to_be_combined")
mut("--file is allowed beside --reverify", '(("--file", opts.file), ("--write", opts.write),', '(("--write", opts.write),',
    "refuses_to_be_combined")
mut("--check is allowed beside --reverify", '("--check", opts.check), ("--cut", opts.cut),', '("--cut", opts.cut),',
    "refuses_to_be_combined")
mut("--cut is allowed beside --reverify", '("--check", opts.check), ("--cut", opts.cut),', '("--check", opts.check),',
    "refuses_to_be_combined")
mut("--budget-bytes is allowed beside --reverify", '("--budget-bytes", opts.budget_bytes is not None),', "",
    "refuses_to_be_combined")
mut("--force is allowed beside --reverify", '("--force", opts.force)) if on]', ") if on]", "refuses_to_be_combined")
mut("the combination refusal exits 0", '"be combined with %s." % ", ".join(clash), file=sys.stderr)\n            return 3',
    '"be combined with %s." % ", ".join(clash), file=sys.stderr)\n            return 0', "refuses_to_be_combined")
mut("main returns 0 whatever the re-derivation said", "        report(result, opts)\n        return result.exit\n\n    if not opts.file:",
    "        report(result, opts)\n        return 0\n\n    if not opts.file:", "rederived_green")
mut("the flag is hidden from --help",
    '                   help="re-derive a frozen shard\'s proof under THIS tool\'s template and print the "',
    '                   help=argparse.SUPPRESS or "re-derive a frozen shard\'s proof under THIS tool\'s template and print the "',
    "help_lists")


def pristine():
    return (REPO / "starter-kit" / "methodology_trim.py").read_text(encoding="utf-8")


def validate():
    src = pristine()
    bad = 0
    for name, old, new, _i in M:
        n = src.count(old)
        if n != 1:
            print("INVALID  %-70s (search text occurs %d times)" % (name, n))
            bad += 1
        elif old == new:
            print("NO-OP    %-70s (search and replacement are equal)" % name)
            bad += 1
    print("%d mutants, %d invalid or no-op" % (len(M), bad))
    return bad


def run(only=()):
    src = pristine()
    killed = survived = invalid = 0
    with tempfile.TemporaryDirectory() as td:
        tree = Path(td)
        (tree / "tools").mkdir()
        (tree / "starter-kit").mkdir()
        (tree / "docs" / "archive").mkdir(parents=True)
        shutil.copy(str(REPO / "tools" / "test_methodology_trim.py"), str(tree / "tools"))
        shutil.copy(str(REPO / "FRAMEWORK_APPARATUS.md"), str(tree))
        for proof in (REPO / "docs" / "archive").glob("*.verify.sh"):
            shutil.copy(str(proof), str(tree / "docs" / "archive"))
        target = tree / "starter-kit" / "methodology_trim.py"
        for name, old, new, intended in M:
            if only and not any(o in name for o in only):
                continue
            if src.count(old) != 1 or old == new:
                print("INVALID  %-70s" % name)
                invalid += 1
                continue
            target.write_text(src.replace(old, new, 1), encoding="utf-8")
            def failures(*extra):
                p = subprocess.run([sys.executable, "tools/test_methodology_trim.py", CLASS] + list(extra),
                                   cwd=str(tree), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                return re.findall(r"^(?:FAIL|ERROR): (test_\w+)", p.stdout, re.M)

            # FIRST the intended test alone (`-k`): if it fails, the mutant is killed and the other
            # tests of the class need not run. Only a mutant that test does NOT kill runs the whole class,
            # so a survivor is still a survivor of every test in TestReverify.
            failed = failures("-k", intended) if intended else []
            first_pass = bool(failed)
            if not failed:
                failed = failures()
            if failed:
                killed += 1
                if first_pass:
                    hit = "  by the intended test"
                elif intended:
                    hit = "  intended test DID NOT FAIL" if not any(intended in f for f in failed) else "  intended test FAILED"
                else:
                    hit = ""
                print("KILLED   %-70s by %d test(s)%s" % (name, len(set(failed)), hit))
            else:
                survived += 1
                print("SURVIVED %-70s" % name)
            sys.stdout.flush()
    print("%d killed, %d survived, %d invalid, of %d run (%d in the list)"
          % (killed, survived, invalid, killed + survived + invalid, len(M)))
    return survived + invalid


if __name__ == "__main__":
    only = [a[len("--only="):] for a in sys.argv[1:] if a.startswith("--only=")]
    sys.exit(1 if (validate() if "--validate" in sys.argv else run(only)) else 0)
