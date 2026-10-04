#!/usr/bin/env python3
"""Mutants of probe.py and rater.py: do their tests fail when the code is wrong? (BL-94 P2a; the same check P1b ran on p1b_score.py.)

    python3 docs/planning/overhead-replay/mutants_p2a.py probe|rater [--jobs 3]

Each mutant is one text replacement in a COPY of this directory's modules (the real files are never touched). A mutant is KILLED when
the target's test file (tests_probe.py, tests_rater.py) exits non-zero against it. The unmutated copy must pass first, or nothing here
means anything. A mutant whose pattern does not occur exactly once is reported BAD MUTANT and counts as not killed. Exit 0 only if every
mutant is killed.
"""
import argparse, concurrent.futures, glob, os, shutil, subprocess, sys, tempfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))

MUTANTS_PROBE = [
    ("cap check off by one (>=)", "if before + session_cap > total_cap:", "if before + session_cap >= total_cap:"),
    ("cap check removed", "if before + session_cap > total_cap:", "if False:"),
    ("cap check skipped at launch", "        refuse_over_cap(out, session_cap, total_cap)\n", "        pass\n"),
    ("CLI flag check skipped", "            check_cli_flags(argv, help_text)\n", "            pass\n"),
    ("CLI flag check passes any missing flag", "    if missing:\n        raise Refused(f\"the CLI no longer", "    if False:\n        raise Refused(f\"the CLI no longer"),
    ("duplicate probe allowed", "if not again and os.path.exists(rows)", "if False and os.path.exists(rows)"),
    ("duplicate check ignores the control", "{k: json.loads(l).get(k) for k in key} == key", "json.loads(l).get(\"run\") == run_id"),
    ("pin ref ignored (always the head ref)", "ref = f\"refs/pins/{run['id']}\" if run[\"pin\"] != run[\"head\"] else f\"refs/runs/{run['id']}\"", "ref = f\"refs/runs/{run['id']}\""),
    ("fetched sha not compared with the manifest pin", "if got != run[\"pin\"]:", "if False:"),
    ("existing destination overwritten", "    if os.path.exists(dest):\n        raise Refused(f\"{dest} exists; refusing to overwrite\")\n", ""),
    ("clone verification skipped", "    verify_clone(facts)\n", ""),
    ("verify ignores a later commit", "(\"a later commit of the original session is present\", facts[\"later_commits_absent\"] is not False)", "(\"a later commit of the original session is present\", True)"),
    ("verify ignores a remote", "(\"a remote exists\", not facts[\"remotes\"])", "(\"a remote exists\", True)"),
    ("verify ignores a dirty tree", "(\"the tracked tree is not clean\", facts[\"tracked_clean\"])", "(\"the tracked tree is not clean\", True)"),
    ("verify ignores a wrong HEAD", "(\"HEAD is not the pinned sha\", facts[\"head_is_pin\"])", "(\"HEAD is not the pinned sha\", True)"),
    ("uncommitted-edits refusal removed", "    if run.get(\"uncommitted_tracked\"):", "    if False:"),
    ("missing-install refusal removed", "    if not run.get(\"install\"):", "    if False:"),
    ("control restores code files too", "        if not doc_score.is_record_path(p):\n            continue\n", ""),
    ("control leaves added record files", "            git(dest, \"rm\", \"-q\", \"-f\", \"--\", p)\n            removed.append(p)", "            removed.append(p)"),
    ("control not committed", "    git(dest, \"commit\", \"-q\", \"--no-verify\", \"-m\", CONTROL_SUBJECT)\n", ""),
    ("control with nothing to revert allowed", "    if not restored and not removed:", "    if False:"),
    ("control directory shares the end state's", "(f\"+{control}\" if control else \"\")", "\"\""),
    ("report takes the first result", "            text = m[\"result\"]", "            text = text or m[\"result\"]"),
    ("probe allowed a second stop", "max_stops=1, popen=popen", "max_stops=2, popen=popen"),
    ("probe opens with something other than go", "PROBE_SCRIPT = [stakeholder.OPENING]", "PROBE_SCRIPT = [\"Hello\"]"),
    ("spend line only on success", "    with open(os.path.join(out, \"spend.jsonl\"), \"a\") as f:\n        f.write(", "    if res[\"stops\"] == 1:\n      with open(os.path.join(out, \"spend.jsonl\"), \"a\") as f:\n        f.write("),
    ("driver errors not caught", "    except OSError as e:", "    except ZeroDivisionError as e:"),
    ("probe_ok ignores the stop count", "\"probe_ok\": res[\"stops\"] == 1 and report is not None", "\"probe_ok\": report is not None"),
    ("scratch repository kept", "        shutil.rmtree(scratch, ignore_errors=True)     # holds every run", "        pass     # holds every run"),
    ("a cost at the cap still counts as a good probe", " and report is not None and res[\"cost_usd\"] < CAP_HIT * session_cap,", " and report is not None,"),
    ("the cap-hit flag is never set", "\"cap_hit\": res[\"cost_usd\"] >= CAP_HIT * session_cap,", "\"cap_hit\": False,"),
    ("verify-all leaves its clones behind", "            shutil.rmtree(os.path.join(work, slug(r[\"id\"], control)), ignore_errors=True)\n", ""),
    ("verify-all calls every rebuilt run ok", "row[\"ok\"] = all(row[k] == \"ok\" for k in (\"end_state\", \"git-only\")) if not row[\"expected_refusal\"] else all(", "row[\"ok\"] = True if not row[\"expected_refusal\"] else all("),
    ("verify-all fails a by-design refusal", "else all(str(row[k]).startswith(\"refused\") for k in (\"end_state\", \"git-only\"))", "else False"),
    ("no-launch still writes the ledger directory", "    if not launch:\n        row[\"launched\"] = False", "    os.makedirs(out, exist_ok=True)\n    if not launch:\n        row[\"launched\"] = False"),
]

MUTANTS_RATER = [
    ("a next-step paragraph never ends at a heading", "if not line.strip() or line.startswith(\"#\") or line.startswith(\"```\") or doc_score.RECEIPT_FIELD_LINE.match(line):", "if not line.strip():"),
    ("a next-step paragraph never ends at a receipt field", " or doc_score.RECEIPT_FIELD_LINE.match(line):", ":"),
    ("missing removes nothing", "    return _map(rd, lambda lines: drop_parts(lines)[0])", "    return _map(rd, lambda lines: lines)"),
    ("wrong places its sentence everywhere", "NEW_NEXT if not placed else None)\n        out[\"docs\"].append(new)", "NEW_NEXT)\n        out[\"docs\"].append(new)"),
    ("vague leaves the shas", "        return _sub_sha(line, lambda s: \"the commit\")", "        return line"),
    ("vague leaves the paths", "        line = doc_score.PATH_RE.sub(\"the relevant file\", line)\n", ""),
    ("every hex-looking token is a sha", "    return bool(re.search(r\"[a-f]\", tok)) and bool(re.search(r\"\\d\", tok))", "    return True"),
    ("fabricated shas are random", "hashlib.sha1((\"fabricated:\" + s).encode()).hexdigest()[:len(s)]", "os.urandom(8).hex()[:len(s)]"),
    ("fabricated shas have another length", "hexdigest()[:len(s)]", "hexdigest()[:7]"),
    ("order B is not reversed", "qs = QUESTIONS if order == \"A\" else list(reversed(QUESTIONS))", "qs = QUESTIONS"),
    ("the record is not between markers", "\"----- BEGIN -----\\n\" + record_text + \"----- END -----\\n\\n\"", "record_text"),
    ("arm_guess is not validated", "    if d.get(\"arm_guess\") not in ARM_CHOICES:\n        raise ValueError(f\"arm_guess must be one of {ARM_CHOICES}\")\n", ""),
    ("extra answer keys are accepted", "set(ans) != set(KEYS)", "not set(KEYS) <= set(ans)"),
    ("an answer outside yes/no/cannot_tell is accepted", "    if bad:\n        raise ValueError(f\"answers outside {ANSWERS}: {bad}\")\n", ""),
    ("the rater runs in the caller's directory", "run(argv, input=user_prompt, capture_output=True, text=True, cwd=cwd)", "run(argv, input=user_prompt, capture_output=True, text=True, cwd=None)"),
    ("the prompt is not sent on stdin", "run(argv, input=user_prompt, capture_output=True", "run(argv, input=\"\", capture_output=True"),
    ("a CLI error is treated as a reply", "    if env.get(\"is_error\") or env.get(\"subtype\", \"success\") != \"success\":", "    if False:"),
    ("a failed call loses its cost", "        return None, cost, f\"CLI error {env.get('subtype')}\"", "        return None, 0.0, f\"CLI error {env.get('subtype')}\""),
    ("the rater gets tools", "\"--tools\", \"\", ", ""),
    ("only yes -> no counts as a drop", "dropped = [q for q in yes if defects[name][q] != \"yes\"]", "dropped = [q for q in yes if defects[name][q] == \"no\"]"),
    ("a defect against a failed question is still judged", "(\"not testable\" if not yes else", "(\"not testable\" if False else"),
    ("a defect with no target is required", "verdict = \"reported only\" if not targets else", "verdict = \"MISSED\" if not targets else"),
    ("orders are not combined strictly", "out[name] = va if va == vb else (\"order-sensitive\" if \"caught\" in (va, vb) else \"MISSED\" if \"MISSED\" in (va, vb) else va)", "out[name] = va"),
    ("the dry run skips the total-cap check", "                probe.refuse_over_cap(out, call_cap, total_cap)\n", "                pass\n"),
    ("the dry run rates one order only", "        for order in (\"A\", \"B\"):\n            try:", "        for order in (\"A\",):\n            try:"),
    ("the dry run writes no ledger line", "            with open(os.path.join(out, \"spend.jsonl\"), \"a\") as f:\n                f.write(json.dumps({\"kind\": \"rater\"", "            with open(os.devnull, \"a\") as f:\n                f.write(json.dumps({\"kind\": \"rater\""),
    ("the honest set is every record", "        if g not in seen:\n            seen.add(g)\n            out.append(rid)", "        out.append(rid)"),
    ("the sample ignores the strata", "        pool = sorted(r for r, (grp, _) in records.items() if grp == g)", "        pool = sorted(records)"),
    ("the packet names the run", "md += [f\"\\n---\\n\\n# Record {labels[rid]}\\n\", text]", "md += [f\"\\n---\\n\\n# Record {labels[rid]} ({rid})\\n\", text]"),
    ("the human arm guess is checked against the group", "guesses.append((g, k[\"arm_label\"]))", "guesses.append((g, k[\"group\"]))"),
    ("the summary drops the cost", "                cost += r.get(\"cost_usd\") or 0.0\n", ""),
    ("the summary hides failed calls", "                    failed.append(f\"{rid}/{kind}/{order}: {r.get('error') or r.get('refused')}\")", "                    pass"),
]

TARGETS = {"probe": ("probe.py", "tests_probe.py", MUTANTS_PROBE), "rater": ("rater.py", "tests_rater.py", MUTANTS_RATER)}


def run_one(args):
    name, old, new, src_dir, module, tests = args
    path = os.path.join(src_dir, module)
    text = open(path).read()
    if text.count(old) != 1:
        return name, "BAD MUTANT", f"pattern occurs {text.count(old)} times"
    open(path, "w").write(text.replace(old, new))
    p = subprocess.run([sys.executable, tests], cwd=src_dir, capture_output=True, text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    tail = [l for l in p.stderr.splitlines() if l.startswith(("FAIL:", "ERROR:"))][:2]
    return name, "killed" if p.returncode != 0 else "SURVIVED", "; ".join(tail)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", choices=sorted(TARGETS))
    ap.add_argument("--jobs", type=int, default=3)
    a = ap.parse_args()
    module, tests, mutants = TARGETS[a.target]
    root = tempfile.mkdtemp(prefix="probe-mutants-")
    try:
        def copy(i):
            d = os.path.join(root, str(i))
            os.makedirs(d)
            for f in glob.glob(os.path.join(HERE, "*.py")):
                shutil.copy(f, d)
            return d
        base = copy("base")
        p = subprocess.run([sys.executable, tests], cwd=base, capture_output=True, text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        if p.returncode != 0:
            print(f"the UNMUTATED {a.target} fails its own tests; nothing below means anything\n" + p.stderr[-2000:])
            return 2
        jobs = [(n, o, nw, copy(i), module, tests) for i, (n, o, nw) in enumerate(mutants)]
        with concurrent.futures.ThreadPoolExecutor(a.jobs) as ex:
            results = list(ex.map(run_one, jobs))
        for name, verdict, detail in results:
            print(f"{verdict:10} {name}" + (f"  [{detail}]" if detail and verdict != "killed" else ""))
        bad = [r for r in results if r[1] != "killed"]
        print(f"\n{len(results) - len(bad)} of {len(results)} killed")
        return 1 if bad else 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
