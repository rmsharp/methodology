#!/usr/bin/env python3
"""Mutants of probe.py and rater.py: do their tests fail when the code is wrong? (BL-94 P2a; the same check P1b ran on p1b_score.py.)

    python3 docs/planning/overhead-replay/mutants_p2a.py probe|rater [--jobs 3]

Each mutant is one text replacement in a COPY of this directory's modules (the real files are never touched). A mutant is KILLED when
the target's test file (tests_probe.py, tests_rater.py) exits non-zero against it. The unmutated copy must pass first, or nothing here
means anything. A mutant whose pattern does not occur exactly once, or whose mutated source does not compile (a syntax error is "killed" by
every test and proves nothing: S260 found one from S258), is reported BAD MUTANT and counts as not killed. Exit 0 only if every mutant is killed.
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
    # S260 (c): a leftover clone is replaced only while it is a pristine copy of what the launch would build
    ("a leftover clone is replaced without looking at it", "    why = not_replaceable(dest, run, control)\n", "    why = None\n"),
    ("a link or a plain file counts as a clone", "    if os.path.islink(dest) or not os.path.isdir(dest):", "    if not os.path.isdir(dest):"),
    ("a directory inside another repository counts as a clone", "    if not top or os.path.realpath(top) != os.path.realpath(dest):", "    if not top:"),
    ("untracked files do not count against a leftover", "\"status\", \"--porcelain\", \"--ignored\", \"--untracked-files=all\"", "\"status\", \"--porcelain\", \"--ignored\", \"--untracked-files=no\""),
    ("ignored files do not count against a leftover", "\"status\", \"--porcelain\", \"--ignored\", \"--untracked-files=all\"", "\"status\", \"--porcelain\", \"--untracked-files=all\""),
    ("a leftover with a remote is replaced", "    if git(dest, \"remote\", check=False):\n        return \"it has a remote\"", "    if False:\n        return \"it has a remote\""),
    ("a leftover end state may sit at any commit", "        pristine = git(dest, \"rev-parse\", \"HEAD\", check=False) == run[\"pin\"]", "        pristine = True"),
    ("a leftover control may have any parent", "git(dest, \"rev-parse\", \"HEAD^\", check=False) == run[\"pin\"] and git(dest, \"log\"", "True and git(dest, \"log\""),
    ("a leftover control may have any subject", " and git(dest, \"log\", \"-1\", \"--format=%s\", check=False) == CONTROL_SUBJECT", ""),
    ("a replaceable leftover is not removed", "    shutil.rmtree(dest)\n    return True", "    return True"),
    ("the row says nothing was replaced", "    shutil.rmtree(dest)\n    return True", "    shutil.rmtree(dest)\n    return False"),
    ("the launch never clears a leftover", "        replaced = clear_leftover(dest, run, control)\n", "        replaced = False\n"),
    # S260 (a): the files a session read through a shell command or the Grep tool
    ("the Read tool's paths include every tool call", "e[\"kind\"] == \"tool_use\" and e[\"name\"] == \"Read\"]", "e[\"kind\"] == \"tool_use\"]"),
    ("wc is a content reader", "CONTENT_READERS = {\"cat\", \"tac\",", "CONTENT_READERS = {\"wc\", \"cat\", \"tac\","),
    ("ls is a content reader", "CONTENT_READERS = {\"cat\", \"tac\",", "CONTENT_READERS = {\"ls\", \"cat\", \"tac\","),
    ("sed -i is a read", "        if prog == \"sed\" and any(", "        if False and any("),
    ("sed -i with a suffix is a read", "a.startswith(\"--in-place\") or re.fullmatch(r\"-[A-Za-z]*i.*\", a)", "a.startswith(\"--in-place\")"),
    ("the pattern is taken for a file", "        if prog in PATTERN_FIRST and not given and ops:\n            ops = ops[1:]", "        if False:\n            ops = ops[1:]"),
    ("-e does not give the pattern", "                    given, skip = True, takes_next", "                    given, skip = False, takes_next"),
    ("an option's value is taken for a file", "                elif name in VALUE_OPTS.get(prog, ()):\n                    skip = takes_next", "                elif name in VALUE_OPTS.get(prog, ()):\n                    skip = False"),
    ("a letter cluster is read by its first letter", "        return \"-\" + token[-1], True", "        return \"-\" + token[1], True"),
    ("a long option with = still takes the next token", "        return token.split(\"=\", 1)[0], \"=\" not in token", "        return token.split(\"=\", 1)[0], True"),
    ("-- does not end the options", "            elif a == \"--\":\n                bare = True", "            elif a == \"--\":\n                pass"),
    ("a lone dash is a file", "                if a != \"-\":\n                    ops.append(a)", "                if True:\n                    ops.append(a)"),
    ("an input redirection is not a read", "                cur.append((\"in\", t))", "                pass"),
    ("an output redirection's target is a read", "            if redirect == \"<\":\n                cur.append((\"in\", t))", "            if True:\n                cur.append((\"in\", t))"),
    ("the fd digit of 2>&1 stays an operand", "                if cur and cur[-1][0] == \"arg\" and cur[-1][1].isdigit():\n                    cur.pop()", "                if False:\n                    cur.pop()"),
    ("a pipe does not end a command", "                cmds.append(cur)                              # | || && ; & ( ) end a simple command\n                cur = []", "                pass"),
    ("an environment assignment hides the program", "        while args and re.match(r\"[A-Za-z_]\\w*=\", args[0]):", "        while False:"),
    ("the program is matched by its full path", "os.path.basename(args[0]) not in CONTENT_READERS", "args[0] not in CONTENT_READERS"),
    ("a here-document is parsed", "    if \"<<\" in command:\n        return [], False", "    if False:\n        return [], False"),
    ("a command that will not tokenise is called parsed", "    except ValueError:\n        return [], False", "    except ValueError:\n        return [], True"),
    ("a file is listed once for every read", "    return list(dict.fromkeys(files)), True", "    return files, True"),
    ("a relative operand is not resolved", "    return os.path.normpath(os.path.join(cwd, path))", "    return path"),
    ("a variable is resolved against the clone", " or \"$\" in path or \"`\" in path:", " or \"`\" in path:"),
    ("a command substitution is resolved against the clone", " or \"$\" in path or \"`\" in path:", " or \"$\" in path:"),
    ("a ~ path is resolved against the clone", "path.startswith(\"~\") or ", ""),
    ("the Grep tool is not counted", "        elif e[\"name\"] == \"Grep\":", "        elif False:"),
    ("the Glob tool is counted", "        elif e[\"name\"] == \"Grep\":", "        elif e[\"name\"] in (\"Grep\", \"Glob\"):"),
    ("the Grep tool's glob is dropped", "os.path.join(base, e[\"input\"][\"glob\"]) if e[\"input\"].get(\"glob\") else base", "base"),
    ("an unparsed command is cut to nothing", "unparsed.append(e[\"input\"].get(\"command\", \"\")[:UNPARSED_KEEP])", "unparsed.append(\"\")"),
    ("an unparsed command is kept whole", "unparsed.append(e[\"input\"].get(\"command\", \"\")[:UNPARSED_KEEP])", "unparsed.append(e[\"input\"].get(\"command\", \"\"))"),
    ("a parsed command is listed as unparsed", "            if not ok:\n                unparsed.append", "            if True:\n                unparsed.append"),
    ("an event that is not a tool call is read", "        if e[\"kind\"] != \"tool_use\":\n            continue\n        if e[\"name\"] == \"Bash\":", "        if e[\"name\"] == \"Bash\":"),
    ("the row records the clone path unresolved", "phase0_other_reads(evs, os.path.realpath(dest))", "phase0_other_reads(evs, dest)"),
    ("the row never lists an unparsed command", "row[\"reads_other\"], row[\"reads_unparsed\"] = phase0_other_reads(evs, os.path.realpath(dest))", "row[\"reads_other\"], row[\"reads_unparsed\"] = phase0_other_reads(evs, os.path.realpath(dest))[0], []"),
]

MUTANTS_RATER = [
    ("a next-step paragraph never ends at a heading", "if not line.strip() or HEADING.match(line) or line.startswith(\"```\") or doc_score.RECEIPT_FIELD_LINE.match(line):", "if not line.strip():"),
    ("a next-step paragraph never ends at a receipt field", " or doc_score.RECEIPT_FIELD_LINE.match(line):", ":"),
    ("missing removes nothing", "    return _map(rd, lambda lines: drop_pending(drop_parts(lines)[0]))", "    return _map(rd, lambda lines: lines)"),
    ("wrong places its sentence everywhere", "NEW_NEXT if not placed else None)\n        out[\"docs\"].append(new)", "NEW_NEXT)\n        out[\"docs\"].append(new)"),
    ("vague leaves the shas", "    return _sub_sha(text, lambda s: \"the commit\")", "    return text"),
    ("vague leaves the paths", "    text = doc_score.PATH_RE.sub(\"the relevant file\", text)\n", ""),
    ("every hex-looking token is a sha", "    return bool(re.search(r\"[a-f]\", tok)) and bool(re.search(r\"\\d\", tok))", "    return True"),
    ("fabricated shas are random", "hashlib.sha1((\"fabricated:\" + s).encode()).hexdigest()[:len(s)]", "os.urandom(8).hex()[:len(s)]"),
    ("fabricated shas have another length", "hexdigest()[:len(s)]", "hexdigest()[:7]"),
    ("order B is not reversed", "qs = QUESTIONS if order == \"A\" else list(reversed(QUESTIONS))", "qs = QUESTIONS"),
    ("the record is not between markers", "\"----- BEGIN -----\\n\" + record_text + \"----- END -----\\n\\n\"", "\"\" + record_text + \"\""),
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
    # S260 (b): a failed call keeps the text that failed
    ("a reply that cannot be used loses its text", "f\"unusable reply: {e}\", keep(env.get(\"result\"))", "f\"unusable reply: {e}\", None"),
    ("a CLI error loses its envelope", "f\"CLI error {env.get('subtype')}\", keep(p.stdout)", "f\"CLI error {env.get('subtype')}\", None"),
    ("a CLI that gave no JSON loses its output", "keep((p.stdout or \"\") + (f\"\\n[stderr]\\n{p.stderr}\" if p.stderr else \"\"))", "None"),
    ("a CLI that gave no JSON loses its stderr", " + (f\"\\n[stderr]\\n{p.stderr}\" if p.stderr else \"\")", ""),
    ("the kept text is not bounded", "    return text if len(text) <= RAW_KEEP else text[:RAW_KEEP] + f\"\\n[cut: {len(text)} characters in all]\"", "    return text"),
    ("a text exactly at the bound is cut", "len(text) <= RAW_KEEP", "len(text) < RAW_KEEP"),
    ("the cut does not say how much was cut", "f\"\\n[cut: {len(text)} characters in all]\"", "\"\\n[cut]\""),
    ("a reply with no text keeps nothing", "    text = \"\" if text is None else", "    text = None if text is None else"),
    ("the dry run drops the text of a failed call", "\"error\": err, \"raw\": raw, \"check\"", "\"error\": err, \"check\""),
    ("a usable reply keeps raw text", "return parse_reply(env.get(\"result\")), cost, None, None", "return parse_reply(env.get(\"result\")), cost, None, env.get(\"result\")"),
    # S260 (d): the planted defects remove what their question rests on, and say so
    ("the label set misses SUGGESTED NEXT", "(?:(?:suggested|recommended|natural)\\s+next\\b|next[ _]steps?\\b|", "(?:next[ _]steps?\\b|"),
    ("a mention anywhere is a label", "(?i)^\\W*(?:(?:suggested", "(?i)^.*?(?:(?:suggested"),
    ("Next task is not a label", "|next up\\b|next task\\b|next action\\b)\")", "|next up\\b|next action\\b)\")"),
    ("an issue list ends a next-step paragraph", "HEADING.match(line) or line.startswith(\"```\")", "line.startswith(\"#\") or line.startswith(\"```\")"),
    ("a # with no space is a heading", "HEADING = re.compile(r\"^#{1,6}\\s\")", "HEADING = re.compile(r\"^#{1,6}\")"),
    ("only a level-1 heading ends a paragraph", "HEADING = re.compile(r\"^#{1,6}\\s\")", "HEADING = re.compile(r\"^#\\s\")"),
    ("a removal's boundary is not recorded", "                if ends is not None:\n                    ends.append(line)", "                pass"),
    ("a removal that runs to the end records nothing", "    if skipping and ends is not None:\n        ends.append(None)", "    pass"),
    ("the finders do not see a code span", "LOCATION_FINDERS = (CODE_SPAN, doc_score.ANCHOR_RE,", "LOCATION_FINDERS = (doc_score.ANCHOR_RE,"),
    ("overlapping matches are counted again", "                if not any(m.start() < e and s < m.end() for s, e in taken):", "                if True:"),
    ("a receipt field's name is counted as a place", "    return (line[:m.end()], line[m.end():]) if m else (\"\", line)", "    return (\"\", line)"),
    ("anchors are named after paths", "    text = doc_score.ANCHOR_RE.sub(\"the relevant place\", text)\n    text = doc_score.PATH_RE.sub(\"the relevant file\", text)\n",
     "    text = doc_score.PATH_RE.sub(\"the relevant file\", text)\n    text = doc_score.ANCHOR_RE.sub(\"the relevant place\", text)\n"),
    ("a code span is always named, never unwrapped", "m.group(0)[1:-1] if m.group(0)[1:-1] in GENERIC else \"the relevant code\"", "\"the relevant code\""),
    ("vague leaves calls", "    for rx in (CALL, QUALIFIED, CAMEL, SNAKE, DOTTED, UPPER_NAME):", "    for rx in (QUALIFIED, CAMEL, SNAKE, DOTTED, UPPER_NAME):"),
    ("vague leaves qualified names", "    for rx in (CALL, QUALIFIED, CAMEL, SNAKE, DOTTED, UPPER_NAME):", "    for rx in (CALL, CAMEL, SNAKE, DOTTED, UPPER_NAME):"),
    ("vague leaves camelCase names", "    for rx in (CALL, QUALIFIED, CAMEL, SNAKE, DOTTED, UPPER_NAME):", "    for rx in (CALL, QUALIFIED, SNAKE, DOTTED, UPPER_NAME):"),
    ("vague leaves snake_case names", "    for rx in (CALL, QUALIFIED, CAMEL, SNAKE, DOTTED, UPPER_NAME):", "    for rx in (CALL, QUALIFIED, CAMEL, DOTTED, UPPER_NAME):"),
    ("vague leaves line references", "    text = LINE_REF.sub(\"the relevant place\", text)\n", ""),
    ("the cue set counts an addressee", "\\bnext action\\b\")", "\\bnext action\\b|\\bnext session\\b\")"),
    ("a defect without a finder is checked", "        if name not in CHECKS:\n            continue", "        if False:\n            continue"),
    ("before is counted on the defective record", "\"before\": len(finder(rd)), \"after\": len(left)", "\"before\": len(left), \"after\": len(left)"),
    ("the cue lines are not collected", "\"cue_lines_left\": cues(made)[:5] if cues else []", "\"cue_lines_left\": []"),
    ("a defect that leaves its evidence is not a problem", "for name, c in per.items() if c[\"after\"]]", "for name, c in per.items() if False]"),
    ("the dry run does not refuse", "    if problems:                      # S259 paid", "    if False:                      # S259 paid"),
    ("a dry run result carries no check", "\"raw\": raw, \"check\": checks[rid].get(kind)}", "\"raw\": raw, \"check\": None}"),
    ("the summary drops the evidence", "\"planted_evidence\": evidence,", ""),
    ("the report does not say where a defect left evidence", "(f\"   LEAVES {c['left'][:3]}\" if c[\"after\"] else \"\")", "\"\""),
    ("the report lists no boundaries", "            lines += [f\"{'':24} {'':8} removal ended at: {e!r}\" for e in c[\"ends\"]]", "            pass"),
    ("the defects command prints no report", "        print(\"\\n\".join(lines))\n        if problems:", "        if problems:"),
    ("the defects command does not fail on a problem", "        if problems:\n            raise SystemExit(\"a planted defect leaves", "        if False:\n            raise SystemExit(\"a planted defect leaves"),
    # S262: the rebuild. Units (a hard-wrapped paragraph is one thing), the names `vague` also removes, the sentences `missing` also removes, the residue
    ("a wrapped paragraph is cut at every line", "        opens = (not line.strip() or UNIT_START.match(line) or doc_score.RECEIPT_FIELD_LINE.match(line)\n                 or (cur and (not cur[0].strip() or cur[0].lstrip().startswith(\"```\"))))", "        opens = True"),
    ("a list item does not open a unit", "UNIT_START = re.compile(r\"^\\s*(?:[-*+]\\s|\\d+[.)]\\s|#{1,6}\\s|```)\")", "UNIT_START = re.compile(r\"^\\s*(?:#{1,6}\\s|```)\")"),
    ("a numbered item does not open a unit", "UNIT_START = re.compile(r\"^\\s*(?:[-*+]\\s|\\d+[.)]\\s|#{1,6}\\s|```)\")", "UNIT_START = re.compile(r\"^\\s*(?:[-*+]\\s|#{1,6}\\s|```)\")"),
    ("a heading does not open a unit", "UNIT_START = re.compile(r\"^\\s*(?:[-*+]\\s|\\d+[.)]\\s|#{1,6}\\s|```)\")", "UNIT_START = re.compile(r\"^\\s*(?:[-*+]\\s|\\d+[.)]\\s|```)\")"),
    ("a receipt field does not open a unit", "UNIT_START.match(line) or doc_score.RECEIPT_FIELD_LINE.match(line)\n", "UNIT_START.match(line)\n"),
    ("a fence line does not stand alone", "(not cur[0].strip() or cur[0].lstrip().startswith(\"```\"))", "(not cur[0].strip())"),
    ("a blank line is not a unit of its own", "(not cur[0].strip() or cur[0].lstrip().startswith(\"```\"))", "(cur[0].lstrip().startswith(\"```\"))"),
    ("the last unit is lost", "    return out + [cur] if cur else out", "    return out"),
    ("a blank unit goes through the function", "        if not unit[0].strip():\n            out.extend(unit)\n            continue\n", ""),
    ("a unit the function empties is kept", "        if text.strip():\n            out.extend((label + text).split(\"\\n\"))", "        out.extend((label + text).split(\"\\n\"))"),
    ("a stop is a sentence end wherever it stands", "SENT_END = re.compile(r\"[.!?][)\\]\\\"'*_]*(?=\\s|$)\\s*\")", "SENT_END = re.compile(r\"[.!?][)\\]\\\"'*_]*\\s*\")"),
    ("a sentence stop leaves its markup behind", "SENT_END = re.compile(r\"[.!?][)\\]\\\"'*_]*(?=\\s|$)\\s*\")", "SENT_END = re.compile(r\"[.!?](?=\\s|$)\\s*\")"),
    ("a sentence loses its trailing space", "SENT_END = re.compile(r\"[.!?][)\\]\\\"'*_]*(?=\\s|$)\\s*\")", "SENT_END = re.compile(r\"[.!?][)\\]\\\"'*_]*(?=\\s|$)\")"),
    ("the last sentence is dropped when it has no stop", "    return out + [text[pos:]] if pos < len(text) else out", "    return out"),
    ("missing keeps its pending sentences", "    return _map(rd, lambda lines: drop_pending(drop_parts(lines)[0]))", "    return _map(rd, lambda lines: drop_parts(lines)[0])"),
    ("missing keeps its labelled paragraphs", "    return _map(rd, lambda lines: drop_pending(drop_parts(lines)[0]))", "    return _map(rd, lambda lines: drop_pending(lines))"),
    ("a pending sentence is kept", "    return \"\".join(p for p in sentences(text) if not PENDING.search(p)).rstrip()", "    return text"),
    ("a trailing space is left behind", "    return \"\".join(p for p in sentences(text) if not PENDING.search(p)).rstrip()", "    return \"\".join(p for p in sentences(text) if not PENDING.search(p))"),
    ("'not closed' is not a pending action", "not (?:yet )?(?:closed|fixed|done|do|acted on|ratcheted|addressed|resolved|attempted)|", ""),
    ("'still open' is not a pending action", "|still (?:open|needs?|to be|remains?)", ""),
    ("'left alone' is not a pending action", "|left (?:\\w+ ){0,2}alone", ""),
    ("'leave alone' is a pending action", "|left (?:\\w+ ){0,2}alone", "|(?:left|leave) (?:\\w+ ){0,2}alone"),
    ("'deferred' is not a pending action", "|deferred|", "|"),
    ("'you'll need to' is not a pending action", "|(?:you|they|we)(?:['’]ll| will)? need to", ""),
    ("'must be run' is not a pending action", "|(?:must|has to|have to|needs? to) be (?:run|closed|done|fixed|decided)", ""),
    ("'decide whether' is not a pending action", "|decide (?:whether|if)", ""),
    ("a bare 'decide' is a pending action", "|decide (?:whether|if)", "|decide"),
    ("a bare 'must' is a pending action", "|must run|", "|must|"),
    ("'owner action' is not a pending action", "|owner action", ""),
    ("'could not close' is not a pending action", "|could(?:n['’]t| not) (?:be )?(?:close|push)\\w*", ""),
    ("'could not run' is a pending action", "(?:be )?(?:close|push)\\w*", "(?:be )?(?:close|push|run)\\w*"),
    ("'say the word' is not a pending action", "|say the word|if you want", "|"),
    ("'I left it' is not a pending action", "|I left (?:it|that|them)", ""),
    ("the finders do not see a dotted name", "SNAKE, DOTTED, UPPER_NAME, HYPHEN_TITLE, LINE_REF, ISSUE_REF, TICKET)", "SNAKE, UPPER_NAME, HYPHEN_TITLE, LINE_REF, ISSUE_REF, TICKET)"),
    ("the finders do not see a document name", "SNAKE, DOTTED, UPPER_NAME, HYPHEN_TITLE, LINE_REF, ISSUE_REF, TICKET)", "SNAKE, DOTTED, HYPHEN_TITLE, LINE_REF, ISSUE_REF, TICKET)"),
    ("the finders do not see a hyphenated place name", "SNAKE, DOTTED, UPPER_NAME, HYPHEN_TITLE, LINE_REF, ISSUE_REF, TICKET)", "SNAKE, DOTTED, UPPER_NAME, LINE_REF, ISSUE_REF, TICKET)"),
    ("the finders do not see an issue reference", "SNAKE, DOTTED, UPPER_NAME, HYPHEN_TITLE, LINE_REF, ISSUE_REF, TICKET)", "SNAKE, DOTTED, UPPER_NAME, HYPHEN_TITLE, LINE_REF, TICKET)"),
    ("the finders do not see a ticket id", "SNAKE, DOTTED, UPPER_NAME, HYPHEN_TITLE, LINE_REF, ISSUE_REF, TICKET)", "SNAKE, DOTTED, UPPER_NAME, HYPHEN_TITLE, LINE_REF, ISSUE_REF)"),
    ("vague leaves dotted names", "    for rx in (CALL, QUALIFIED, CAMEL, SNAKE, DOTTED, UPPER_NAME):", "    for rx in (CALL, QUALIFIED, CAMEL, SNAKE, UPPER_NAME):"),
    ("vague leaves document names", "    for rx in (CALL, QUALIFIED, CAMEL, SNAKE, DOTTED, UPPER_NAME):", "    for rx in (CALL, QUALIFIED, CAMEL, SNAKE, DOTTED):"),
    ("vague leaves hyphenated place names", "    text = HYPHEN_TITLE.sub(\"the relevant place\", text)\n", ""),
    ("vague leaves issue references", "    for rx in (ISSUE_REF, TICKET):", "    for rx in (TICKET,):"),
    ("vague leaves ticket ids", "    for rx in (ISSUE_REF, TICKET):", "    for rx in (ISSUE_REF,):"),
    ("any capital and digit is a ticket", "TICKET = re.compile(r\"\\b[A-Z]\\d{1,2}\\b\")", "TICKET = re.compile(r\"\\b[A-Z]\\d+\\b\")"),
    ("a hash after a word is an issue reference", "ISSUE_REF = re.compile(r\"(?<![\\w&])#\\d+\\b\")", "ISSUE_REF = re.compile(r\"#\\d+\\b\")"),
    ("every upper-case word is a document name", "UPPER_NAME = re.compile(r\"\\b(?:[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+|%s)\\b\" % \"|\".join(DOC_NAMES))", "UPPER_NAME = re.compile(r\"\\b[A-Z][A-Z0-9_]{2,}\\b\")"),
    ("a number with a point is a dotted name", "DOTTED = re.compile(r\"\\b[a-z]{2,}(?:\\.[a-z]{2,})+\\b\")", "DOTTED = re.compile(r\"\\b\\w{2,}(?:\\.\\w{2,})+\\b\")"),
    ("a span cannot wrap onto the next line", "CODE_SPAN = re.compile(r\"`[^`]+`\")", "CODE_SPAN = re.compile(r\"`[^`\\n]+`\")"),
    ("vague works one line at a time", "    return _map(rd, lambda lines: per_unit(lines, _vague_text))", "    return _map(rd, lambda lines: [_vague_text(l) for l in lines])"),
    ("tokens are found one line at a time", "    for unit in units(lines):\n        text = unit_text(unit)[1]\n        taken = []", "    for unit in [[l] for l in lines]:\n        text = unit_text(unit)[1]\n        taken = []"),
    ("the missing check counts labels only", "(\"next-step labels and pending-action sentences\", next_step_evidence, next_step_cues)", "(\"next-step labels and pending-action sentences\", next_step_labels, next_step_cues)"),
    ("the residue is not collected", "\"residue\": RESIDUE[name](made) if name in RESIDUE else []}", "\"residue\": []}"),
    ("the residue is not printed", "            lines += [f\"{'':24} {'':8} still standing, counted by no finder: {r['what']}: {r['count']} (first: {r['first'][:5]})\" for r in c[\"residue\"]]", "            pass"),
    ("the summary drops the residue", "(\"evidence\", \"before\", \"after\", \"left\", \"cue_lines_left\", \"ends\", \"residue\")", "(\"evidence\", \"before\", \"after\", \"left\", \"cue_lines_left\", \"ends\")"),
    ("a residue is a refusal", "for name, c in per.items() if c[\"after\"]]", "for name, c in per.items() if c[\"after\"] or c[\"residue\"]]"),
    ("the names residue counts every occurrence", "out.append({\"what\": what, \"count\": len(tally), \"first\"", "out.append({\"what\": what, \"count\": sum(tally.values()), \"first\""),
    ("the names residue is not ordered by frequency", "[f\"{t}×{n}\" for t, n in tally.most_common(8)]", "[f\"{t}×{n}\" for t, n in sorted(tally.items())[:8]]"),
]

TARGETS = {"probe": ("probe.py", "tests_probe.py", MUTANTS_PROBE), "rater": ("rater.py", "tests_rater.py", MUTANTS_RATER)}


def run_one(args):
    name, old, new, src_dir, module, tests = args
    path = os.path.join(src_dir, module)
    text = open(path).read()
    if text.count(old) != 1:
        return name, "BAD MUTANT", f"pattern occurs {text.count(old)} times"
    mutated = text.replace(old, new)
    try:
        compile(mutated, module, "exec")
    except SyntaxError as e:
        return name, "BAD MUTANT", f"does not compile ({e.msg}): every test would kill it, so it proves nothing"
    open(path, "w").write(mutated)
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
