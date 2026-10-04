#!/usr/bin/env python3
"""M5, the blind rater, and the packet for the operator's own blind rating (BL-94 P2a (d); plan section 2.3 M5, section 4 items 3 and 4, D5).

    python3 rater.py defects  [--out DIR]                        # $0: write the planted-defect set for inspection
    python3 rater.py packet   [--out DIR] [--seed N]             # $0: the operator's blind packet, score sheet and (separate) key
    python3 rater.py dry-run  --call-cap 0.75 --total-cap 100    # PAID: the rater on the planted-defect set; P2, not P2a
    python3 rater.py score-human SHEET.csv KEY.json              # $0: his sheet scored against the key

What the rater sees: ONE record, rendered as neutral "Document n" blocks (no file names, no run id, no arm) plus the session's final
message, and nothing else: no tools, no repository, an empty working directory. It answers the fixed yes / no / cannot-tell list below
and then guesses which of three protocol versions wrote the record. Each record is rated twice, the question list in opposite order,
so an order effect shows as a disagreement. It is the writers' model family; that is stated beside every M5 figure (plan 4 item 3).

The planted-defect set is the rater's validity check, made mechanically from an honest record (no model): `missing` drops the next-step
parts, `wrong` replaces them with a statement that contradicts the rest, `vague` replaces every path, anchor and sha with a generic word,
`fabricated` swaps the shas for invented ones. A defective record must score LOWER than its honest original on the questions it was built
to break. `fabricated` is the exception: a sha cannot be checked from the text alone (M1 does that against git), so it is reported and
not required. A rater that cannot rank a record with no next step below one with a next step is not measuring usefulness.

The packet is the same rendering the model sees, so the two sets of ratings are comparable. His ten records are drawn with a fixed seed,
stratified 3 / 3 / 4 across v3.0, v3.7 and v3.8-text; the key that says which record is which is a SEPARATE file.
"""
import argparse, csv, hashlib, json, os, random, re, shutil, subprocess, sys, tempfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doc_evidence, doc_score, driver, p1b_score, probe

EVIDENCE = os.path.join(doc_evidence.PILOT, "doc-evidence")
OUT = os.path.join(doc_evidence.PILOT, "doc-probe")
SCORES = os.path.join(EVIDENCE, "p1b-scores.json")

QUESTIONS = [
    ("next_step", "Does the record state a next step specific enough that a successor could start it without first reading the code?"),
    ("where", "Does it say where the next work begins, by naming at least one file, function or location?"),
    ("state", "Does it say unambiguously whether the session's task is finished, partly finished or not started?"),
    ("evidence", "Does it say what was checked (a test run, a command, a count) and what the result was?"),
    ("hazard", "Does it warn of at least one specific pitfall a successor could hit?"),
    ("commits", "Does it identify the commits this session made, by hash or by subject?"),
    ("consistent", "Is the record free of statements that contradict one another?"),
    ("loose_ends", "Does it say whether anything was left uncommitted, pending or unrecorded?"),
]
KEYS = [k for k, _ in QUESTIONS]
ANSWERS = ("yes", "no", "cannot_tell")
ARM_CHOICES = ("3.0", "3.7", "3.8", "cannot_tell")
GROUP_LABEL = {"v3.0": "3.0", "v3.7": "3.7", "v3.8-text": "3.8"}
STRATA = {"v3.0": 3, "v3.7": 3, "v3.8-text": 4}            # about ten (plan 4 item 4)
SEED = 20261004
NEXT_LABEL = re.compile(r"(?i)^\W*(next[ _]steps?|what.s next|next session|next up)\b")
SYSTEM = ("You are a careful reader. You are shown one document: the text that one working session added to a software project's own "
          "records. You have no tools and no access to the project. Judge only from the text. Reply with one JSON object and nothing else.")
NEW_NEXT = "Next: start the task from the beginning; nothing described above has been done yet."


# ---- the record, rendered neutrally -----------------------------------------------------------------------------------------------
def record_docs(rec, final_message=""):
    """{docs: [[line, ...], ...], final: [line, ...]} from doc_score.record(): the added lines per record file in path order (blank lines
    kept so a paragraph can end), and the final message. File names are dropped here and never reach the rater."""
    docs = [list(lines) for _, lines in sorted(rec["raw"].items()) if any(lines)]
    return {"docs": docs, "final": [l.rstrip() for l in (final_message or "").splitlines()]}


def render(rd):
    out = []
    for i, lines in enumerate(rd["docs"], 1):
        out.append(f"=== Document {i} (text added by the session) ===")
        out.extend(lines)
        out.append("")
    if any(l.strip() for l in rd["final"]):
        out.append("=== The session's final message ===")
        out.extend(rd["final"])
    return "\n".join(out).strip() + "\n"


# ---- planted defects (mechanical, no model) ----------------------------------------------------------------------------------------
def drop_parts(lines, replacement=None):
    """Remove every paragraph whose first line is a next-step label, with the same ending rules doc_score._parts uses: a paragraph runs
    from its label to a blank line, a heading, a fence or the next receipt field. A one-line field (`next_steps: ...`) is its own
    paragraph. `replacement` (a line) is put where the first one was."""
    out, skipping, placed = [], False, False
    for line in lines:
        if NEXT_LABEL.match(line):
            skipping = True
            if replacement and not placed:
                out.append(replacement)
                placed = True
            continue
        if skipping:
            if not line.strip() or line.startswith("#") or line.startswith("```") or doc_score.RECEIPT_FIELD_LINE.match(line):
                skipping = False
            else:
                continue
        out.append(line)
    return out, placed


def _map(rd, fn_lines):
    return {"docs": [fn_lines(l) for l in rd["docs"]], "final": fn_lines(rd["final"])}


def defect_missing(rd):
    return _map(rd, lambda lines: drop_parts(lines)[0])


def defect_wrong(rd):
    out, placed = {"docs": [], "final": None}, False
    for lines in rd["docs"]:
        new, p = drop_parts(lines, NEW_NEXT if not placed else None)
        out["docs"].append(new)
        placed = placed or p
    new, p = drop_parts(rd["final"], NEW_NEXT if not placed else None)
    out["final"] = new if (placed or p) else new + ["", NEW_NEXT]
    return out


def _shaish(tok):
    return bool(re.search(r"[a-f]", tok)) and bool(re.search(r"\d", tok))


def _sub_sha(text, fn):
    return doc_score.SHA_RE.sub(lambda m: fn(m.group(1)) if _shaish(m.group(1)) else m.group(0), text)


def defect_vague(rd):
    def one(line):
        line = doc_score.ANCHOR_RE.sub("the relevant place", line)
        line = doc_score.PATH_RE.sub("the relevant file", line)
        return _sub_sha(line, lambda s: "the commit")
    return _map(rd, lambda lines: [one(l) for l in lines])


def defect_fabricated(rd):
    fake = lambda s: hashlib.sha1(("fabricated:" + s).encode()).hexdigest()[:len(s)]
    return _map(rd, lambda lines: [_sub_sha(l, fake) for l in lines])


# name -> (builder, the questions it is built to break: it is CAUGHT when any of them goes from yes to not yes; none = reported only).
# `vague` targets `where` alone: the commits question accepts a subject, which the defect leaves in place.
DEFECTS = {"missing": (defect_missing, ["next_step"]), "wrong": (defect_wrong, ["consistent", "state"]),
           "vague": (defect_vague, ["where"]), "fabricated": (defect_fabricated, [])}


def changed(rd, other):
    return render(rd) != render(other)


# ---- the rating call ----------------------------------------------------------------------------------------------------------------
def prompt(record_text, order="A"):
    qs = QUESTIONS if order == "A" else list(reversed(QUESTIONS))
    lines = [f"{i}. [{k}] {q}" for i, (k, q) in enumerate(qs, 1)]
    form = {"answers": {k: "yes | no | cannot_tell" for k, _ in qs}, "arm_guess": "3.0 | 3.7 | 3.8 | cannot_tell", "reason": "one sentence"}
    return ("The text below is everything one working session added to its project's records, followed by the message it ended on.\n\n"
            "----- BEGIN -----\n" + record_text + "----- END -----\n\n"
            "Answer each question from the text alone. Use cannot_tell only when the text does not let you decide.\n\n" + "\n".join(lines) + "\n\n"
            "Then, last, say which of three versions of a session protocol (called 3.0, 3.7 and 3.8) the author was following, or cannot_tell.\n\n"
            "Reply with one JSON object of exactly this form and nothing else:\n" + json.dumps(form, indent=1) + "\n")


def parse_reply(text):
    """The first JSON object in the reply, validated against the fixed list. Raises ValueError on anything else."""
    m = re.search(r"\{.*\}", text or "", re.S)
    if not m:
        raise ValueError("no JSON object in the reply")
    d = json.loads(m.group(0))
    ans = d.get("answers")
    if not isinstance(ans, dict) or set(ans) != set(KEYS):
        raise ValueError(f"answers must hold exactly {KEYS}")
    bad = {k: v for k, v in ans.items() if v not in ANSWERS}
    if bad:
        raise ValueError(f"answers outside {ANSWERS}: {bad}")
    if d.get("arm_guess") not in ARM_CHOICES:
        raise ValueError(f"arm_guess must be one of {ARM_CHOICES}")
    return {"answers": ans, "arm_guess": d["arm_guess"], "reason": str(d.get("reason", ""))[:300]}


def rater_cmd(model, effort, call_cap):
    return ["claude", "-p", "--model", model, "--effort", effort, "--max-budget-usd", str(call_cap), "--no-session-persistence",
            "--setting-sources", "", "--strict-mcp-config", "--disable-slash-commands", "--tools", "", "--output-format", "json",
            "--system-prompt", SYSTEM]


def call_rater(user_prompt, argv, run=subprocess.run):
    """One rating call: the prompt on stdin, an EMPTY working directory, no tools. Returns (parsed or None, cost, error or None)."""
    with tempfile.TemporaryDirectory(prefix="rater-") as cwd:
        p = run(argv, input=user_prompt, capture_output=True, text=True, cwd=cwd)
    try:
        env = json.loads(p.stdout)
    except ValueError:
        return None, 0.0, f"no JSON from the CLI (exit {p.returncode}): {(p.stderr or p.stdout)[:200]}"
    cost = float(env.get("total_cost_usd") or 0.0)
    if env.get("is_error") or env.get("subtype", "success") != "success":
        return None, cost, f"CLI error {env.get('subtype')}"
    try:
        return parse_reply(env.get("result")), cost, None
    except ValueError as e:
        return None, cost, f"unusable reply: {e}"


def total(parsed):
    a = parsed["answers"]
    return {"yes": sum(v == "yes" for v in a.values()), "cannot_tell": sum(v == "cannot_tell" for v in a.values()), "of": len(KEYS)}


def planted_check(honest, defects):
    """honest: {question: answer}; defects: {name: {question: answer}}, one question order. A defect is `caught` when any question it
    targets was `yes` in the honest rating and is not `yes` in the defective one; `MISSED` when some targeted question was `yes` and none
    dropped; `not testable` when no targeted question was `yes` to begin with; `reported only` for a defect with no target."""
    out = {}
    for name, (_, targets) in DEFECTS.items():
        if name not in defects:
            continue
        yes = [q for q in targets if honest[q] == "yes"]
        dropped = [q for q in yes if defects[name][q] != "yes"]
        verdict = "reported only" if not targets else ("not testable" if not yes else ("caught" if dropped else "MISSED"))
        out[name] = {"verdict": verdict, "dropped": dropped, "targets": targets}
    return out


def combine_orders(a, b):
    """A defect is `caught` only when it is caught in both question orders; one order only is `order-sensitive`."""
    out = {}
    for name in a:
        va, vb = a[name]["verdict"], b[name]["verdict"]
        out[name] = va if va == vb else ("order-sensitive" if "caught" in (va, vb) else "MISSED" if "MISSED" in (va, vb) else va)
    return out


def summarize_dry_run(results):
    """From dry_run()'s output: per honest record its score, each defect's verdict and score, the two orders' disagreement, the arm
    guess on the honest ratings, and the cost. Pure: it reads the results and nothing else."""
    rows, guesses, cost, failed = {}, [], 0.0, []
    for rid, kinds in results.items():
        ok = lambda kind, order: (kinds.get(kind, {}).get(order) or {}).get("parsed")
        for kind in kinds:
            for order, r in kinds[kind].items():
                cost += r.get("cost_usd") or 0.0
                if not r.get("parsed"):
                    failed.append(f"{rid}/{kind}/{order}: {r.get('error') or r.get('refused')}")
        if not (ok("honest", "A") and ok("honest", "B")):
            rows[rid] = {"honest": "unrated"}
            continue
        h = {o: ok("honest", o)["answers"] for o in "AB"}
        guesses += [(ok("honest", o)["arm_guess"], rid) for o in "AB"]
        per = {}
        for o in "AB":
            per[o] = planted_check(h[o], {k: ok(k, o)["answers"] for k in DEFECTS if ok(k, o)})
        rows[rid] = {"honest_total": {o: total(ok("honest", o)) for o in "AB"},
                     "order_disagreement": [q for q in KEYS if h["A"][q] != h["B"][q]],
                     "defects": combine_orders(per["A"], per["B"]) if per["A"] and per["B"] else {},
                     "defect_totals": {k: {o: total(ok(k, o)) for o in "AB" if ok(k, o)} for k in DEFECTS if ok(k, "A") or ok(k, "B")}}
    return {"records": rows, "arm_guesses": guesses, "cost_usd": round(cost, 4), "failed_calls": failed}


# ---- the runs (read from the saved evidence) ---------------------------------------------------------------------------------------
def load_records(evidence=EVIDENCE, scores=SCORES, project=doc_evidence.DEFAULT_PROJECT):
    """{run_id: (group, record_docs)} for every scored run, from the bundle and the saved scores. Nothing is scored again."""
    with open(scores) as f:
        saved = json.load(f)["runs"]
    scratch, manifest = doc_evidence.rebuild(evidence, project)
    out = {}
    try:
        for r in manifest["runs"]:
            s = saved.get(r["id"])
            if not s or not s["included"]:
                continue
            out[r["id"]] = (s["group"], record_docs(doc_score.record(scratch, r["install"], r["pin"]), s["final_message"]))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    return out


def honest_set(records):
    """One honest record per group: the first run id in sorted order, so the dry run's inputs are not chosen after seeing a rating."""
    seen, out = set(), []
    for rid in sorted(records):
        g = records[rid][0]
        if g not in seen:
            seen.add(g)
            out.append(rid)
    return out


# ---- the operator's packet -----------------------------------------------------------------------------------------------------------
def draw_sample(records, seed=SEED, strata=STRATA):
    rng = random.Random(seed)
    chosen = []
    for g, n in strata.items():
        pool = sorted(r for r, (grp, _) in records.items() if grp == g)
        chosen += rng.sample(pool, min(n, len(pool)))
    rng.shuffle(chosen)
    return chosen


def build_packet(records, sample):
    labels = {rid: f"R{i:02d}" for i, rid in enumerate(sample, 1)}
    md = ["# Blind rating packet", "",
          "Ten records, each the text one working session added to its project's records plus the message it ended on. Nothing here says which",
          "version of the protocol wrote it or which run it came from. For each record answer the eight questions from the text alone",
          "(yes / no / ?), then guess which of three versions, 3.0, 3.7 or 3.8, was being followed (or ?). Record your answers in `sheet.csv`.",
          "Do not open `KEY-do-not-open-before-rating.json`.", "", "## The questions", ""]
    md += [f"{i}. **{k}** — {q}" for i, (k, q) in enumerate(QUESTIONS, 1)] + [""]
    words = 0
    for rid in sample:
        text = render(records[rid][1])
        words += len(text.split())
        md += [f"\n---\n\n# Record {labels[rid]}\n", text]
    key = {labels[rid]: {"run": rid, "group": records[rid][0], "arm_label": GROUP_LABEL[records[rid][0]]} for rid in sample}
    sheet = [["record", *KEYS, "arm_guess", "notes"]] + [[labels[rid]] + [""] * (len(KEYS) + 2) for rid in sample]
    return "\n".join(md) + "\n", sheet, key, {"records": len(sample), "words": words, "minutes_at_200_wpm": round(words / 200)}


def score_human(sheet_path, key):
    """His sheet against the key: per group, the share of `yes` on each question, and how often his arm guess was right."""
    with open(sheet_path, newline="") as f:
        rows = list(csv.DictReader(f))
    by_group, guesses = {}, []
    for r in rows:
        k = key[r["record"]]
        for q in KEYS:
            v = (r.get(q) or "").strip().lower()
            if v:
                by_group.setdefault(k["group"], {}).setdefault(q, []).append(1 if v in ("y", "yes") else 0)
        g = (r.get("arm_guess") or "").strip()
        if g:
            guesses.append((g, k["arm_label"]))
    return {"yes_share": {g: {q: round(sum(v) / len(v), 3) for q, v in qs.items()} for g, qs in by_group.items()},
            "arm_guess": {"answered": len(guesses), "right": sum(g == a for g, a in guesses), "of": len(rows), "chance": round(1 / 3, 3)}}


# ---- the paid dry run (P2, not P2a) ---------------------------------------------------------------------------------------------------
def dry_run(records, call_cap, total_cap, out=OUT, model="sonnet", effort="high", run=subprocess.run):
    """Rate the honest set and its planted defects, each record in both question orders, one call each. Every call is checked against
    the study's own spend ledger first and written to it after; a refused call ends the run with what it has."""
    os.makedirs(out, exist_ok=True)
    argv = rater_cmd(model, effort, call_cap)
    results = {}
    jobs = []
    for rid in honest_set(records):
        rd = records[rid][1]
        jobs.append((rid, "honest", rd))
        for name, (fn, _) in DEFECTS.items():
            made = fn(rd)
            if changed(rd, made):
                jobs.append((rid, name, made))
    for rid, kind, rd in jobs:
        for order in ("A", "B"):
            try:
                probe.refuse_over_cap(out, call_cap, total_cap)
            except SystemExit as e:
                results.setdefault(rid, {}).setdefault(kind, {})[order] = {"refused": str(e)}
                return results
            parsed, cost, err = call_rater(prompt(render(rd), order), argv, run)
            with open(os.path.join(out, "spend.jsonl"), "a") as f:
                f.write(json.dumps({"kind": "rater", "run": rid, "defect": kind, "order": order, "cost_usd": cost}) + "\n")
            results.setdefault(rid, {}).setdefault(kind, {})[order] = {"parsed": parsed, "cost_usd": cost, "error": err}
    return results


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("mode", choices=["defects", "packet", "dry-run", "score-human"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--out", default=os.path.join(OUT, "rating"), help="where artifacts are written")
    ap.add_argument("--ledger", default=OUT, help="the study's spend ledger directory (dry-run only)")
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--call-cap", type=float); ap.add_argument("--total-cap", type=float)
    ap.add_argument("--model", default="sonnet"); ap.add_argument("--effort", default="high")
    a = ap.parse_args(argv)
    if a.mode == "score-human":
        with open(a.args[1]) as f:
            print(json.dumps(score_human(a.args[0], json.load(f)), indent=1))
        return
    if a.mode == "dry-run" and (a.call_cap is None or a.total_cap is None):
        ap.error("dry-run is paid: --call-cap and --total-cap are both required")
    records = load_records()
    os.makedirs(a.out, exist_ok=True)
    if a.mode == "defects":
        for rid in honest_set(records):
            rd = records[rid][1]
            for name, (fn, _) in DEFECTS.items():
                made = fn(rd)
                with open(os.path.join(a.out, f"{probe.slug(rid)}.{name}.txt"), "w") as f:
                    f.write(render(made))
                print(f"{rid:24} {name:11} changed={changed(rd, made)}")
    elif a.mode == "packet":
        sample = draw_sample(records, a.seed)
        md, sheet, key, size = build_packet(records, sample)
        open(os.path.join(a.out, "packet.md"), "w").write(md)
        csv.writer(open(os.path.join(a.out, "sheet.csv"), "w", newline="")).writerows(sheet)
        json.dump(key, open(os.path.join(a.out, "KEY-do-not-open-before-rating.json"), "w"), indent=1, sort_keys=True)
        print(json.dumps(size))
    else:
        res = dry_run(records, a.call_cap, a.total_cap, a.ledger, a.model, a.effort)
        json.dump(res, open(os.path.join(a.out, "dry-run.json"), "w"), indent=1, sort_keys=True)
        json.dump(summarize_dry_run(res), open(os.path.join(a.out, "dry-run-summary.json"), "w"), indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
