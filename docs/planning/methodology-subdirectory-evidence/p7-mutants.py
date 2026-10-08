"""The mutants of the BL-101 P7 pass (S280), for mutate-p7.py. Each is (id, file, old, new, test classes): `old` occurs
exactly once in `file`; the classes are where the killing test is expected to live (the fast ones first). Round 1 (M, C)
was written from the new code; round 2 (R) was aimed at behaviours I could not name a test for."""
T = "bin/migrate-layout"
PURE = ["TestThePureRules"]
USAGE = ["TestUsageAndNothingToDo"]
REFUSE = ["TestRefusals"]
APPLY = ["TestApply"]
TIERS = ["TestTheTiers"]
LEDGER = ["TestTheLedgerEntry"]
CHECKS = ["TestTheChecks"]
REHEARSE = ["TestTheShardRehearsal"]
HITS = ["TestTheHitsItWillNotRewrite", "TestWhatTheHitsSayAboutHooksAndDirectories"]
ROLLBACK = ["TestARefusedCommitRollsBack"]

MUTANTS = [
    # --- round 1: the rules as functions
    ("M01", T, '        s = s[1:] if neg else s\n', '        s = s\n', PURE),
    ("M02", T, 'if (s.startswith("/") or "/" in path.rstrip("/")) and path in mapping:', 'if path in mapping:', PURE),
    ("M03", T, 'out.append(("!" if neg else "") + "/" + mapping[path] + eol)', 'out.append(("!" if neg else "") + "/" + mapping[path] + "\\n")', PURE),
    ("M05", T, '(?<![\\w./~-])(?:%s)(?!\\w|\\.\\w)', '(?<![\\w.~-])(?:%s)(?!\\w|\\.\\w)', PURE),
    ("M06", T, '(?<![\\w./~-])(?:%s)(?!\\w|\\.\\w)', '(?<![\\w./~-])(?:%s)(?!\\w)', PURE),
    ("M07", T, '(?<![\\w./~-])(?:%s)(?!\\w|\\.\\w)', '(?<![\\w./-])(?:%s)(?!\\w|\\.\\w)', PURE),
    ("M08", T, '(?<![\\w./~-])(?:%s)(?!\\w|\\.\\w)', '(?<![\\w./~])(?:%s)(?!\\w|\\.\\w)', PURE),
    ("M09", T, '(?<![\\w./~-])(?:%s)(?!\\w|\\.\\w)', '(?<![\\w/~-])(?:%s)(?!\\w|\\.\\w)', PURE),
    ("M10", T, '    if not mapping:\n        return lambda text: (text, 0)\n    pattern = token_pattern(mapping)', '    pattern = token_pattern(mapping)', PURE),
    ("M11", T, '                if k.startswith("_") or k == "canonical":\n                    continue', '                if k.startswith("_"):\n                    continue', PURE),
    ("M12", T, '                if k.startswith("_") or k == "canonical":\n                    continue', '                if k == "canonical":\n                    continue', PURE),
    ("M13", T, '            return {k: (o[k] if k.startswith("_") or k == "canonical"', '            return {k: (o[k] if k == "canonical"', PURE),
    ("M14", T, '        if key == "command":\n            return tokens(value)[0]\n        return mapping.get(value, value)', '        return mapping.get(value, value)', PURE),
    ("M15", T, '            return tokens(value)[0]\n        return mapping.get(value, value)', '            return tokens(value)[0]\n        return tokens(value)[0]', PURE),
    ("M16", T, '            count += 1\n            return m.group(1) + json.dumps(new, ensure_ascii=False)', '            return m.group(1) + json.dumps(new, ensure_ascii=False)', PURE),
    ("M17", T, 'return m.group(1) + json.dumps(new, ensure_ascii=False)', 'return m.group(1) + json.dumps(new)', PURE),
    ("M18", T, '    if json.loads(text) != expected(data):', '    if False:', PURE),
    ("M19", T, '    if m.group(1) == "## " + month:', '    if True:', PURE),
    ("M20", T, '        while i < len(text) and text[i] == "\\n":\n            i += 1\n', '', PURE),
    ("M21", T, '        return SENTINEL_RE.sub("", text).rstrip("\\n") + "\\n\\n" + block.rstrip("\\n") + "\\n"', '        return text.rstrip("\\n") + "\\n\\n" + block.rstrip("\\n") + "\\n"', PURE),
    ("M22", T, '    if m.group(1) is None:\n        return text[:m.start()] + block + text[m.start():]', '    if m.group(1) is None:\n        return text + block', PURE),
    ("M23", T, '    sha = (report["canonical"]["sha"] or "an unknown commit")[:7]', '    sha = (report["canonical"]["sha"] or "an unknown commit")[:9]', PURE),
    ("M24", T, 'after["history"]["commits"] < before["history"]["commits"] + 1', 'after["history"]["commits"] < before["history"]["commits"]', PURE),
    ("M25", T, '    if before["history"]["commits"] and after', '    if after', PURE),
    ("M27", T, '    for name in ("ledger", "handoff"):\n        if before[name]["exit"] != after[name]["exit"]:', '    for name in ("ledger",):\n        if before[name]["exit"] != after[name]["exit"]:', PURE),
    ("M28", T, '    if before["proofs"] != after["proofs"]:', '    if False:', PURE),
    ("M29", T, 'CI_FILES = (".gitlab-ci.yml", ".travis.yml", "Jenkinsfile", "azure-pipelines.yml")', 'CI_FILES = (".gitlab-ci.yml", ".travis.yml", "azure-pipelines.yml")', PURE),
    ("M30", T, 'CI_PREFIXES = (".github/", ".circleci/")', 'CI_PREFIXES = (".github/",)', PURE),
    ("M31", T, 'or path in tuple(NEW_DIR + "/" + n for n in LEDGER_FILES):', ':', PURE),
    ("M32", T, '(?:CHANGELOG|HANDOFFS|SESSION_NOTES)-through-', '(?:CHANGELOG|HANDOFFS)-through-', PURE),
    ("M33", T, '-through-[^/]+\\.md(?:\\.verify\\.sh)?$', '-through-[^/]+\\.md$', PURE),
    ("M34", T, '    return rules(text) <= rules(seed_text)', '    return rules(text) == rules(seed_text)', PURE),
    ("M35", T, '            entries.add("/" + NEW_LAYOUT[src])', '            pass', PURE),
    ("M36", T, '            entries.add("/" + dest)\n', '            pass\n', PURE),
    ("M37", T, 'or (disp == SEED and tier in ("2", "all"))', 'or (disp == SEED and tier in ("1", "all"))', PURE),
    ("M38", T, '    if tier in ("2", "all"):\n        for name in GENERATED:\n            new = NEW_DIR', '    if tier in ("1", "all"):\n        for name in GENERATED:\n            new = NEW_DIR', PURE),
    ("M39", T, '            if old_here and new_here:\n                collisions.append(new)\n            elif old_here:\n                add(name, new, "generated")', '            if old_here:\n                add(name, new, "generated")', PURE),
    ("M40", T, '                if (root / new).is_file():\n                    collisions.append(new)\n                else:\n                    add(path, new, "shard")', '                add(path, new, "shard")', PURE),
    ("M41", T, 'if "/" not in name and SHARD_RE.match(name):', 'if SHARD_RE.match(name.rsplit("/", 1)[-1]):', PURE),
    ("M45", T, '        if entry[0] in "RC":\n            i += 1  # a rename or copy carries its source as the next field\n', '', PURE),
    # --- round 1: the commands
    ("C01", T, '    if top.returncode != 0 or Path(top.stdout.strip()).resolve() != root.resolve():', '    if top.returncode != 0:', USAGE),
    ("C02", T, '    if run(root, "rev-parse", "--verify", "-q", "HEAD").returncode != 0:', '    if False:', USAGE),
    ("C03", T, '    if dirty:\n        refusals.append', '    if False:\n        refusals.append', REFUSE),
    ("C04", T, '    if kind == "half":\n        where', '    if False:\n        where', REFUSE),
    ("C05", T, '    if tier == "2" and kind != "new":', '    if False:', TIERS),
    ("C06", T, '    if collisions:\n        refusals.append(refusal("destination-exists"', '    if False:\n        refusals.append(refusal("destination-exists"', REFUSE),
    ("C07", T, '    if is_ignore_mode(root):', '    if False:', REFUSE),
    ("C08", T, '    if present:\n        rows, why = read_status(root)', '    if False:\n        rows, why = read_status(root)', REFUSE),
    ("C09", T, 'if d == TRACKED and s != "current" and s != "half-migrated"]', 'if s != "current" and s != "half-migrated"]', REFUSE),
    ("C10", T, '        moves, more_left, report["rehearsal"] = rehearse_shards(root, moves)', '        pass', REHEARSE),
    ("C11", T, '    if not refusals and not moves:\n        report["status"] = "nothing-to-do"', '    if False:\n        report["status"] = "nothing-to-do"', APPLY),
    ("C13", T, '        for m in moves:\n            remove_empty_parents(root, m["src"])', '        for m in moves:\n            pass', APPLY),
    ("C14", T, '                if score is None or score < 90:', '                if score is None or score < 50:', LEDGER),
    ("C16", T, '["git", "-C", str(root), "commit", "-q", "-F", "-"]', '["git", "-C", str(root), "commit", "-q", "--no-verify", "-F", "-"]', ROLLBACK),
    ("C17", T, '    for src, dest in reversed(done_plain):\n        if (root / dest).is_file() and not (root / src).exists():\n            os.rename(root / dest, root / src)', '    for src, dest in reversed(done_plain):\n        pass', ROLLBACK),
    ("C18", T, '    if not methodology_existed:', '    if False:', ROLLBACK),
    ("C19", T, '    run(root, "reset", "-q", "--hard", "HEAD")', '    pass', ROLLBACK),
    ("C20", T, '    after = run_checks(root, proof_dests, ledger_final)', '    after = run_checks(root, proof_srcs, ledger_final)', CHECKS),
    ("C22", T, '    return 0 if report["checks"]["ok"] else 4', '    return 0', CHECKS),
    ("C23", T, 'before = None if skip_checks else run_checks(root, proof_srcs, ledger_src)', 'before = None if skip_checks else run_checks(root, proof_dests, ledger_src)', CHECKS),
    ("C24", T, 'for src in sorted(s for s in before if before[s] != after[s]):', 'for src in sorted(s for s in before if before[s] == after[s]):', REHEARSE),
    ("C25", T, '        drop |= {src, shard}', '        drop |= {src}', REHEARSE),
    ("C29", T, 'skip = {m["src"] for m in moves if hit_category(m["src"]) != "ledger"} | {p for p in new_text if p.endswith(".json")}', 'skip = {p for p in new_text if p.endswith(".json")}', HITS),
    ("C31", T, 'site["runs_tool"] = any(n.endswith(".py") for n in names)', 'site["runs_tool"] = False', HITS),
    ("C35", T, '            mapping.setdefault(name, NEW_DIR + "/" + name)', '            pass', ["TestTheRewriteOfTheConfigs"]),
    ("C37", T, 'rewrites.append(Rewrite(path, moved.get(path, path), old, new, n))', 'rewrites.append(Rewrite(path, path, old, new, n))', ["TestTheRewriteOfTheConfigs"]),
    ("C40", T, '    if skip_checks:\n        report["checks"] = {"ran": False}\n        return 0\n', '', CHECKS),
    # --- round 2: aimed at behaviours I could not name a test for
    ("R01", T, 'or after["status"]["exit"] != 0 or after["status"]["current"] != after["status"]["tracked"]:', ':', PURE),
    ("R02", T, '        if parent == Path(root):\n            break\n', '', PURE),
    ("R03", T, '"half": "half-migrated", "none": "none"}[kind]', '"half": "half", "none": "none"}[kind]', REFUSE),
    ("R04", T, '            if not (kind == "half" and legacy == "SESSION_RUNNER.md"):', '            if True:', REFUSE),
    ("R05", T, '                if score is None or score < 90:', '                if score is not None and score < 90:', ["TestALedgerSoSmallThatGitSeesNoRenameAtAll", "TestASmallLedgerIsRefusedWithAReason"]),
    ("R06", T, '"ok": not differences and clean,', '"ok": not differences,', CHECKS),
    ("R07", T, 'if cat != "ledger" and shown[cat] < SITES_SHOWN:', 'if cat != "ledger":', HITS),
    ("R08", T, 'r = run(root, "grep", "-I", "-l", "-z", "-F", *probe)', 'r = run(root, "grep", "-l", "-z", "-F", *probe)', HITS),
    ("R09", T, '(("\\n\\n" + "\\n".join(trailers)) if trailers else "")', '(("\\n" + "\\n".join(trailers)) if trailers else "")', APPLY),
    ("R10", T, '% len(plain)) if plain else ""),', '% len(plain)) if False else ""),', APPLY),
    ("R11", T, '        elif path.startswith(ARCHIVE_OLD + "/") and tier in ("2", "all"):', '        elif path.startswith(ARCHIVE_OLD + "/"):', TIERS),
]
