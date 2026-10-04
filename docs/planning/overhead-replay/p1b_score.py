#!/usr/bin/env python3
"""BL-94 P1b: score the saved v3.0, v3.7 and v3.8-text runs ONCE with the frozen scorer (plan section 5, P1b).

    python3 p1b_score.py score  OUT.json [--project PATH]   # the one scoring run; refuses to start unless doc_score.py is the frozen file
                                                            # and refuses to overwrite OUT.json (a second run needs --again, and the report says so)
    python3 p1b_score.py report OUT.json                    # the by-arm tables from the saved scores; it scores nothing
    python3 p1b_score.py inputs [--project PATH]            # inclusion, pin, task check, measurement and final message per run; no score is computed

This file is glue, not a scorer: every number comes from `doc_score.py` (frozen, `doc_score.frozen`), `doc_evidence.rebuild` (the runs
from the committed bundle) and the saved rows. It adds no rule to the scorer. Where it decides anything it is the plan's section 2.5
(inclusion by `reached_closeout`) and the three inputs the plan names for P1b: the final message (the transcript, cut at the pin
commit's time), the task check (`pilot/real-3.7/held_out_results.json` for S237's runs, the row's own `ratchet.task_done` for the
T-control runs, which is `ratchet_arms.held_out_task` run when the row was written) and the measured test counts (`final_measure`,
which only the ratchet study's rows carry).

Arms: v3.0 and v3.7 are S237's (set `real-3.7`); v3.8-text is the ratchet study's T-control (sets `t-control` and `t-control-fix`, arms
R0 and R1). R1 carries the quality-ratchet hook, R0 does not; `t-control-fix` is the same R1 with the corrected close-out reply.
Those are covariates, never separate arms. T-remove is not scored here: it was the calibration set (`CALIBRATION.md`).

Pooling check, defined before any number was read (plan 5, P1b): for each process measure (cost, requests, tool calls, commits) the
report gives each group's mean and spread, how many v3.8-text runs lie inside the span of the v3.0 and v3.7 runs together, the one
within-arm batch contrast the data holds (R1, old reply against fixed reply: same arm, same start state, same CLI, a different day),
and an exact permutation test of each pair. It can show a batch difference; it cannot show their absence, because no arm appears in
two batches except R1, so arm and batch are confounded for every v3.0 against v3.8-text comparison and the report says that.
Python 3 stdlib only.
"""
import argparse, hashlib, itertools, json, math, os, random, statistics, sys
sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SCORER = os.path.join(HERE, "doc_score.py")
FROZEN = os.path.join(HERE, "doc_score.frozen")
PILOT = os.path.join(HERE, "pilot")
EVIDENCE = os.path.join(PILOT, "doc-evidence")
SCORED_SETS = ("real-3.7", "t-control", "t-control-fix")
GROUPS = ("v3.0", "v3.7", "v3.8-text")
ROW_FILES = {"real-3.7": "real-3.7/rows.jsonl", "t-control": "ratchet-control-t-control/rows.jsonl",
             "t-control-fix": "ratchet-control-t-control-reply-fix/rows.jsonl"}
PROCESS = (("cost_usd", "cost (USD)"), ("requests", "requests"), ("tool_calls", "tool calls"), ("commits", "commits to the pin"))
POWER_D = 0.20                     # plan 3.8: the difference worth detecting; n = 15.7 sigma^2 / d^2


def process_of(r):
    """The process measures of a scored run. Cost, requests and tool calls are the saved row's (S237's rows for the two runs that ran on
    were cut at the close-out by hand); commits are those in BASE..PIN, from the scorer's own range, because the manifest's
    `commits_after_start` counts to HEAD and v3.7 rep 2 runs 13 commits past its pin."""
    return {"cost_usd": r["cost_usd"], "requests": r["requests"], "tool_calls": r["tool_calls"],
            "commits": r["score"]["m2"]["a"]["commits"] + 1}


def sha256_of(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def frozen_sha():
    with open(FROZEN) as f:
        return json.load(f)["sha256"]


def group_of(set_name, arm):
    """v3.0 and v3.7 are S237's arms; every T-control run is v3.8 text (R0 and R1 are covariates inside it)."""
    return arm if set_name == "real-3.7" else "v3.8-text"


def task_from_held_out(counts):
    """S237's task check: every held-out file with no failures and no errors (counts are [failed, errors, warnings, tests])."""
    return all(c[0] == 0 and c[1] == 0 for c in counts.values())


def measured_from_row(row):
    fm = row.get("final_measure") or {}
    m = {k: fm[k] for k in ("passed", "failed", "warnings") if k in fm}
    return m or None


def run_inputs(run, row, held_out):
    """The task check and the measurement for one run, from the saved rows only. None where the evidence holds none."""
    if run["set"] == "real-3.7":
        h = held_out.get(f"{run['arm']}-r{run['rep']}")
        return (task_from_held_out(h["held_out"]) if h else None), measured_from_row(row)
    return row["ratchet"]["task_done"], measured_from_row(row)


def load_rows():
    rows = {}
    for set_name, rel in ROW_FILES.items():
        with open(os.path.join(PILOT, rel)) as f:
            for line in f:
                r = json.loads(line)
                rows[f"{set_name}/{r['arm']}-r{r['rep']}"] = r
    return rows


def require_frozen():
    if sha256_of(SCORER) != frozen_sha():
        raise SystemExit("doc_score.py differs from doc_score.frozen: stop and ask the operator (plan section 4, item 1)")


def gather(project):
    """Everything a score needs and nothing that is one: inclusion (plan 2.5), the pin, the task check, the measurement and the final
    message, per run. `inputs` prints this, so the inputs can be read and corrected before the one scoring run."""
    import doc_evidence, doc_score, replaylib
    scratch, manifest = doc_evidence.rebuild(EVIDENCE, project)
    rows = load_rows()
    with open(os.path.join(PILOT, "real-3.7", "held_out_results.json")) as f:
        held_out = json.load(f)
    runs = {}
    for run in manifest["runs"]:
        if run["set"] not in SCORED_SETS:
            continue
        row = rows[run["id"]]
        entry = {"id": run["id"], "set": run["set"], "arm": run["arm"], "group": group_of(run["set"], run["arm"]),
                 "ratchet": (run["arm"] == "R1") if run["set"] != "real-3.7" else None,
                 "reply": {"t-control": "old", "t-control-fix": "fixed"}.get(run["set"]),
                 "cli": run["cli"], "install": run["install"], "pin": run["pin"], "pin_rule": run["pin_rule"],
                 "row_end": row.get("end"), "cost_usd": row["cost_usd"], "requests": row["O3_requests"], "tool_calls": row["O3_tool_calls"],
                 "commits_after_start": run["commits_after_start"],   # to HEAD: kept as provenance, not used by the report
                 "cost_valid": None if run["set"] != "real-3.7" else not (run["arm"] == "v3.7" and str(run["rep"]) == "5")}
        entry["included"] = doc_score.reached_closeout(scratch, run["install"], run["pin"])
        if entry["included"]:
            td, measured = run_inputs(run, row, held_out)
            epoch = int(doc_score.git(scratch, "log", "-1", "--format=%ct", run["pin"]).strip())
            final = doc_score.final_message(replaylib.events(replaylib.load_records(run["transcript"])), epoch)
            entry.update(task_done=td, measured=measured, final_message=final, pin_epoch=epoch)
        runs[run["id"]] = entry
    return scratch, runs


def collect(project, again=False, out=None):
    """The one scoring run: `gather`, then `doc_score.score_run` and `doc_score.build_key` for each included run."""
    import doc_score
    require_frozen()
    if out and os.path.exists(out) and not again:
        raise SystemExit(f"{out} exists: P1b scores once. Pass --again only for a driver defect, and say so in the report.")
    scratch, runs = gather(project)
    for e in runs.values():
        if e["included"]:
            e["score"] = doc_score.score_run(scratch, e["install"], e["pin"], e["final_message"], e["task_done"], e["measured"])
            e["key"] = doc_score.build_key(scratch, e["install"], e["pin"])
    return {"about": "BL-94 P1b: the frozen doc_score.py over the saved v3.0, v3.7 and v3.8-text runs (p1b_score.py). Scored once.",
            "scorer_sha256": sha256_of(SCORER), "scorer_frozen": json.load(open(FROZEN)), "again": bool(again),
            "manifest_sha256": hashlib.sha256(open(os.path.join(EVIDENCE, "manifest.json"), "rb").read()).hexdigest(),
            "runs": runs}


def print_inputs(runs):
    """No score: inclusion, pin, the task check, the measurement and the size of the final message for each run."""
    print("| run | group | in | pin | task done | measured | final message (chars) | cli | ratchet / reply |")
    print("|---|---|---|---|---|---|---|---|---|")
    for e in runs.values():
        m = e.get("measured")
        print(f"| {e['id']} | {e['group']} | {'yes' if e['included'] else 'NO (' + str(e['row_end']) + ')'} | {e['pin'][:8]}{' (override)' if e['pin_rule'] == 'override' else ''} | "
              f"{e.get('task_done', '-')} | {('P%s F%s W%s' % (m.get('passed'), m.get('failed'), m.get('warnings'))) if m else '-'} | "
              f"{len(e['final_message']) if e['included'] else '-'} | {','.join(e['cli'])} | {e['ratchet']} / {e['reply']} |")


# ---- summaries: pure functions over the saved scores -----------------------------------------------------------------------------
def sd(xs):
    """Sample standard deviation (n - 1); None below two values."""
    return statistics.stdev(xs) if len(xs) > 1 else None


def spread(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return {"n": 0, "mean": None, "sd": None, "min": None, "max": None}
    return {"n": len(xs), "mean": statistics.mean(xs), "sd": sd(xs), "min": min(xs), "max": max(xs)}


def perm_p(a, b, cap=200000, seed=1):
    """Two-sided permutation p-value for a difference of means: exact when the number of splits is at most `cap`, else `cap` random
    splits with a fixed seed. Small n, no distributional assumption, no extra library."""
    a, b = list(a), list(b)
    if not a or not b:
        return None
    obs = abs(statistics.mean(a) - statistics.mean(b))
    pool, na = a + b, len(a)
    total = math.comb(len(pool), na)
    hits = n = 0
    if total <= cap:
        for idx in itertools.combinations(range(len(pool)), na):
            s = set(idx)
            x = [pool[i] for i in idx]
            y = [pool[i] for i in range(len(pool)) if i not in s]
            hits += abs(statistics.mean(x) - statistics.mean(y)) >= obs - 1e-12
            n += 1
    else:
        rng = random.Random(seed)
        for _ in range(cap):
            rng.shuffle(pool)
            hits += abs(statistics.mean(pool[:na]) - statistics.mean(pool[na:])) >= obs - 1e-12
            n += 1
    return hits / n


def n_per_arm(sigma, d=POWER_D):
    """Plan 3.8: n = 15.7 sigma^2 / d^2 for 80% power at 5% (normal approximation; a t-test needs about one more). None without spread."""
    return None if not sigma else math.ceil(15.7 * sigma * sigma / (d * d))


def _kind(runs, kind):
    c = sum(r["score"]["m1"][kind]["checkable"] for r in runs)
    v = sum(r["score"]["m1"][kind]["verified"] for r in runs)
    return {"checkable": c, "verified": v, "accuracy": (v / c) if c else None}


def summarize(data):
    """Everything the report prints, from the saved scores alone."""
    from doc_score import m1_at_ceiling
    runs = list(data["runs"].values())
    scored = [r for r in runs if r["included"]]
    by_group = {g: [r for r in scored if r["group"] == g] for g in GROUPS}
    out = {"excluded": [{"id": r["id"], "group": r["group"], "row_end": r["row_end"]} for r in runs if not r["included"]], "groups": {}}
    for g, rs in by_group.items():
        m1 = [r["score"]["m1"]["accuracy"] for r in rs]
        m2a = [r["score"]["m2"]["a"]["coverage"] for r in rs]
        b = [r["score"]["m2"]["b"] for r in rs]
        c = [r["score"]["m2"]["c"] for r in rs]
        out["groups"][g] = {
            "n": len(rs), "ids": [r["id"] for r in rs],
            "record_lines": spread([r["score"]["record"]["lines"] for r in rs]),
            "m1": spread(m1), "m1_checkable": spread([r["score"]["m1"]["checkable"] for r in rs]),
            "m1_by_kind": {k: _kind(rs, k) for k in ("shas", "paths", "anchors", "counts")},
            "m1_failures": sum(len(r["score"]["m1"]["failures"]) for r in rs),
            "m1_runs_below_ceiling": [r["id"] for r in rs if (r["score"]["m1"]["accuracy"] or 1) < 0.95],
            "m2a": spread(m2a), "m2a_missing": sum(len(r["score"]["m2"]["a"]["missing"]) for r in rs),
            "m2a_commits": spread([r["score"]["m2"]["a"]["commits"] for r in rs]),
            "m2b_applicable": any(x is not None for x in b),
            "m2b_left": None if not any(x is not None for x in b) else sum(x["left"] for x in b if x is not None),
            "m2b_descriptive_left": sum(len(r["score"]["m2"]["b_descriptive"]["receipts"]) + len(r["score"]["m2"]["b_descriptive"]["changelog_markers"]) for r in rs),
            "m2c_supplied": sum(x is not None for x in c), "m2c_flags": [r["id"] for r, x in zip(rs, c) if x and x["flag"]],
            "says_done": [r["id"] for r in rs if r["score"]["m2"]["says_done"]],
            "task_done_false": [r["id"] for r in rs if r["task_done"] is False],
            "commit_slot_pending": sum(1 for r in rs if str(r["score"]["m2"]["commit_slot"] or "").strip().lower().startswith("pending")),
            "process": {k: spread([process_of(r)[k] for r in rs]) for k, _ in PROCESS},
            "n_for_m1": n_per_arm(sd([x for x in m1 if x is not None])), "n_for_m2a": n_per_arm(sd([x for x in m2a if x is not None])),
        }
    out["m1_at_ceiling"] = m1_at_ceiling([r["score"]["m1"] for r in scored])
    out["m1_ceiling_runs_checked"] = len(scored)
    # pairwise tests on M1 and M2(a) and the process measures
    pairs = list(itertools.combinations(GROUPS, 2))
    tests = {}
    for label, getter in (("m1", lambda r: r["score"]["m1"]["accuracy"]), ("m2a", lambda r: r["score"]["m2"]["a"]["coverage"]),
                          *((k, (lambda k: lambda r: process_of(r)[k])(k)) for k, _ in PROCESS)):
        for ga, gb in pairs:
            xa = [getter(r) for r in by_group[ga] if getter(r) is not None]
            xb = [getter(r) for r in by_group[gb] if getter(r) is not None]
            tests[f"{label}:{ga}~{gb}"] = {"mean_a": statistics.mean(xa) if xa else None, "mean_b": statistics.mean(xb) if xb else None,
                                           "p": perm_p(xa, xb)}
    out["tests"] = tests
    # pooling: v3.8-text runs inside the span of v3.0 and v3.7 together; R1 old reply against R1 fixed reply
    span = {}
    for k, _ in PROCESS:
        both = [process_of(r)[k] for r in by_group["v3.0"] + by_group["v3.7"]]
        lo, hi = min(both), max(both)
        span[k] = {"lo": lo, "hi": hi, "inside": sum(lo <= process_of(r)[k] <= hi for r in by_group["v3.8-text"]), "of": len(by_group["v3.8-text"])}
    out["pooling_span"] = span
    r1_old = [r for r in by_group["v3.8-text"] if r["arm"] == "R1" and r["reply"] == "old"]
    r1_fix = [r for r in by_group["v3.8-text"] if r["arm"] == "R1" and r["reply"] == "fixed"]
    out["pooling_batch"] = {"n_old": len(r1_old), "n_fixed": len(r1_fix),
                            **{k: {"old": spread([process_of(r)[k] for r in r1_old]), "fixed": spread([process_of(r)[k] for r in r1_fix]),
                                   "p": perm_p([process_of(r)[k] for r in r1_old], [process_of(r)[k] for r in r1_fix])} for k, _ in PROCESS}}
    # covariates: every scored run by the factors the plan names (CLI version; ratchet hook and close-out reply wording inside v3.8-text)
    def cov(label, key):
        rows = {}
        for r in scored:
            rows.setdefault((r["group"], key(r)), []).append(r)
        return {f"{g} / {k}": {"n": len(rs), "m1": spread([r["score"]["m1"]["accuracy"] for r in rs]), "m2a": spread([r["score"]["m2"]["a"]["coverage"] for r in rs]),
                               "flags": [r["id"] for r in rs if (r["score"]["m2"]["c"] or {}).get("flag")], "cost": spread([r["cost_usd"] for r in rs])}
                for (g, k), rs in sorted(rows.items())}
    out["covariates"] = {"cli": cov("cli", lambda r: ",".join(r["cli"])),
                         "ratchet_reply": cov("ratchet_reply", lambda r: (("R1" if r["ratchet"] else "R0") + "/" + str(r["reply"])) if r["group"] == "v3.8-text" else "-")}
    return out


def fmt(x, nd=3):
    return "n/a" if x is None else (f"{x:.{nd}f}" if isinstance(x, float) else str(x))


def report(data):
    s = summarize(data)
    P = print
    P(f"scorer sha-256 {data['scorer_sha256'][:12]} (frozen {data['scorer_frozen']['frozen']}) · manifest {data['manifest_sha256'][:12]} · again={data['again']}")
    P("\nNot scored (no close-out in the final tree, plan 2.5): " + ", ".join(f"{e['id']} ({e['row_end']})" for e in s["excluded"]))
    P("\n| group | n | record lines mean (sd) | M1 mean | M1 sample sd | M1 min | checkable mean | M1 failures | runs under 0.95 |")
    P("|---|---|---|---|---|---|---|---|---|")
    for g, x in s["groups"].items():
        P(f"| {g} | {x['n']} | {fmt(x['record_lines']['mean'], 1)} ({fmt(x['record_lines']['sd'], 1)}) | {fmt(x['m1']['mean'])} | {fmt(x['m1']['sd'])} | "
          f"{fmt(x['m1']['min'])} | {fmt(x['m1_checkable']['mean'], 1)} | {x['m1_failures']} | {', '.join(x['m1_runs_below_ceiling']) or 'none'} |")
    P(f"\nM1 ceiling rule (>= 0.95 in every scored run): {'AT CEILING, M1 is uninformative' if s['m1_at_ceiling'] else 'NOT at ceiling'} ({s['m1_ceiling_runs_checked']} runs)")
    P("\nM1 by kind, pooled over each group's runs (verified/checkable):")
    P("| group | shas | paths | anchors | counts |")
    P("|---|---|---|---|---|")
    for g, x in s["groups"].items():
        k = x["m1_by_kind"]
        P(f"| {g} | " + " | ".join(f"{k[n]['verified']}/{k[n]['checkable']}" for n in ("shas", "paths", "anchors", "counts")) + " |")
    P("\n| group | M2(a) mean | sd | min | commits per run | commits not named | M2(b) left | M2(c) flags | says done | task not done | commit slot pending |")
    P("|---|---|---|---|---|---|---|---|---|---|---|")
    for g, x in s["groups"].items():
        P(f"| {g} | {fmt(x['m2a']['mean'])} | {fmt(x['m2a']['sd'])} | {fmt(x['m2a']['min'])} | {fmt(x['m2a_commits']['mean'], 1)} | {x['m2a_missing']} | "
          f"{('n/a (no stub artifact); descriptive ' + str(x['m2b_descriptive_left'])) if not x['m2b_applicable'] else x['m2b_left']} | "
          f"{', '.join(x['m2c_flags']) or 'none'} ({x['m2c_supplied']} supplied) | {len(x['says_done'])}/{x['n']} | {', '.join(x['task_done_false']) or 'none'} | {x['commit_slot_pending']} |")
    P(f"\nSection 3.8, n per arm = 15.7 sigma^2 / {POWER_D}^2 (a t-test needs about one more): " +
      "; ".join(f"{g}: M1 {fmt(x['n_for_m1'])}, M2(a) {fmt(x['n_for_m2a'])}" for g, x in s["groups"].items()) + "  (n/a = no spread)")
    P("\nProcess rows (mean, sample sd; scored runs only):")
    P("| group | " + " | ".join(lbl for _, lbl in PROCESS) + " |")
    P("|---|" + "---|" * len(PROCESS))
    for g, x in s["groups"].items():
        P(f"| {g} | " + " | ".join(f"{fmt(x['process'][k]['mean'], 2)} ({fmt(x['process'][k]['sd'], 2)})" for k, _ in PROCESS) + " |")
    P("\nPooling, v3.8-text runs inside the span of v3.0 and v3.7 together: " +
      "; ".join(f"{lbl} {v['inside']}/{v['of']} in [{fmt(v['lo'], 2)}, {fmt(v['hi'], 2)}]" for (k, lbl), v in zip(PROCESS, (s['pooling_span'][k] for k, _ in PROCESS))))
    b = s["pooling_batch"]
    P(f"\nPooling, R1 old reply (n={b['n_old']}) against R1 fixed reply (n={b['n_fixed']}), the one within-arm batch contrast:")
    for k, lbl in PROCESS:
        P(f"  {lbl}: old {fmt(b[k]['old']['mean'], 2)} (sd {fmt(b[k]['old']['sd'], 2)}) against fixed {fmt(b[k]['fixed']['mean'], 2)} (sd {fmt(b[k]['fixed']['sd'], 2)}), permutation p = {fmt(b[k]['p'])}")
    for label, tbl in s["covariates"].items():
        P(f"\nCovariate: {label} (scored runs; M1 and M2(a) mean, cost mean, M2(c) flags):")
        P("| group / level | n | M1 | M2(a) | cost | flags |")
        P("|---|---|---|---|---|---|")
        for k, v in tbl.items():
            P(f"| {k} | {v['n']} | {fmt(v['m1']['mean'])} | {fmt(v['m2a']['mean'])} | {fmt(v['cost']['mean'], 2)} | {', '.join(v['flags']) or 'none'} |")
    P("\nPairwise permutation p (exact, two-sided, difference of means; uncorrected; small n):")
    for key, t in s["tests"].items():
        P(f"  {key}: {fmt(t['mean_a'], 3)} against {fmt(t['mean_b'], 3)}, p = {fmt(t['p'])}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sc = sub.add_parser("score")
    sc.add_argument("out")
    sc.add_argument("--project", default=None)
    sc.add_argument("--again", action="store_true")
    rp = sub.add_parser("report")
    rp.add_argument("saved")
    ip = sub.add_parser("inputs")
    ip.add_argument("--project", default=None)
    a = ap.parse_args(argv)
    if a.cmd == "inputs":
        import doc_evidence
        require_frozen()
        print_inputs(gather(a.project or doc_evidence.DEFAULT_PROJECT)[1])
    elif a.cmd == "score":
        import doc_evidence
        data = collect(a.project or doc_evidence.DEFAULT_PROJECT, a.again, a.out)
        with open(a.out, "w") as f:
            json.dump(data, f, indent=1, sort_keys=True)
        print(f"wrote {a.out}: {len(data['runs'])} runs, {sum(r['included'] for r in data['runs'].values())} scored")
    else:
        with open(a.saved) as f:
            report(json.load(f))


if __name__ == "__main__":
    main()
