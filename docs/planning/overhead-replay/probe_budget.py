#!/usr/bin/env python3
"""What a cold-start probe costs, from the saved runs (BL-94 P2a (c); plan section 5 P2a).

    python3 probe_budget.py            # prints the table; writes pilot/doc-evidence/p2a-probe-budget.json

A probe opens "go" and stops at the runner's Phase 0 report. Every saved run of the three contrast sets also opened "go", so its FIRST
stop is the same turn, on the start state instead of the end state. This reads, for each scored run: the CLI's own `total_cost_usd` and
turn count at that first stop (from the run's stream log, which the driver wrote), and from the on-disk transcript what the session did
in that turn: tool calls, and which files it read, split into FRAMEWORK files (what the install commit added or changed), RECORD files
(doc_score.is_record_path, not framework) and the rest, with the characters its tool result returned to the model (a Read with an offset or limit returns less than the file)
and the file's whole size at the pin for comparison.

It measures the original sessions' first turn. It does NOT measure a probe: an end state has more commits and a longer record, and the
model may behave differently with nothing to do after the report. The pilot (P2) is what measures a probe; this sets the cap to ask for.
"""
import json, os, statistics, subprocess, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doc_evidence, doc_score, p1b_score, replaylib

EVIDENCE = os.path.join(doc_evidence.PILOT, "doc-evidence")
OUT = os.path.join(EVIDENCE, "p2a-probe-budget.json")
SAVED_SCORES = os.path.join(EVIDENCE, "p1b-scores.json")
MARGIN = 0.25          # the plan's margin for defects (24% of S237's spend was lost to them)


def first_stop(stream_path):
    """The first `result` message of a stream log: the cost and turns at the Phase 0 stop. None if there is no log or no result."""
    if not os.path.exists(stream_path):
        return None
    with open(stream_path, errors="replace") as f:
        for line in f:
            if '"type":"result"' not in line.replace(" ", ""):
                continue
            try:
                m = json.loads(line)
            except ValueError:
                continue
            if m.get("type") == "result":
                u = m.get("usage") or {}
                return {"cost_usd": m.get("total_cost_usd"), "turns": m.get("num_turns"), "duration_s": round((m.get("duration_ms") or 0) / 1000, 1),
                        "subtype": m.get("subtype"), "is_error": m.get("is_error"), "report_chars": len(m.get("result") or ""),
                        "input": u.get("input_tokens"), "output": u.get("output_tokens"), "cache_read": u.get("cache_read_input_tokens"),
                        "cache_write": u.get("cache_creation_input_tokens")}
    return None


def phase0_records(records):
    """The records of the first turn: from the opening message up to (not including) the second human message."""
    out, humans = [], 0
    for r in records:
        if r.get("isSidechain") is True:
            continue
        c = (r.get("message") or {}).get("content")
        if r.get("type") == "user" and (isinstance(c, str) or (isinstance(c, list) and not any(b.get("type") == "tool_result" for b in c) and any(b.get("type") == "text" for b in c))):
            humans += 1
            if humans == 2:
                break
        out.append(r)
    return out


def result_chars(block):
    c = block.get("content")
    if isinstance(c, str):
        return len(c)
    return sum(len(x.get("text", "")) for x in c if isinstance(x, dict)) if isinstance(c, list) else 0


def size_at(repo, rev, path):
    p = subprocess.run(["git", "-C", repo, "cat-file", "-s", f"{rev}:{path}"], capture_output=True, text=True)
    return int(p.stdout) if p.returncode == 0 else None


def classify_read(rel, framework):
    if rel in framework:
        return "framework"
    return "record" if doc_score.is_record_path(rel) else "other"


def run_phase0(transcript, tree, scratch, run, framework):
    """What the first turn did. Sizes: `returned` is what the tool result carried back to the model (characters, close to bytes), which
    is the cost-relevant figure; `bytes_pin` is the file's whole size at the pin, for comparison (a partial read returns far less)."""
    recs = phase0_records(replaylib.load_records(transcript))
    uses, results, tools = {}, {}, 0
    for r in recs:
        c = (r.get("message") or {}).get("content")
        if not isinstance(c, list):
            continue
        for b in c:
            if r.get("type") == "assistant" and b.get("type") == "tool_use":
                uses.setdefault(b["id"], b)
                tools += 1 if uses[b["id"]] is b else 0
            elif r.get("type") == "user" and b.get("type") == "tool_result":
                results[b.get("tool_use_id")] = result_chars(b)
    reads, bash = [], []
    for tid, b in uses.items():
        if b["name"] == "Read":
            path = b["input"].get("file_path", "")
            rel = next((os.path.relpath(path, t) for t in (tree, os.path.realpath(tree)) if path.startswith(t + "/")), None)   # macOS: /tmp is /private/tmp
            reads.append({"path": rel or path, "kind": classify_read(rel, framework) if rel else "outside",
                          "partial": bool(b["input"].get("offset") or b["input"].get("limit")), "returned": results.get(tid),
                          "bytes_pin": size_at(scratch, run["pin"], rel) if rel else None})
        elif b["name"] == "Bash":
            bash.append({"command": b["input"].get("command", "")[:90], "returned": results.get(tid)})
    by = {k: {"n": sum(1 for x in reads if x["kind"] == k), "returned": sum(x["returned"] or 0 for x in reads if x["kind"] == k)}
          for k in ("framework", "record", "other", "outside")}
    return {"tool_calls": len(uses), "tool_result_chars": sum(v or 0 for v in results.values()), "reads": reads, "reads_by_kind": by,
            "bash": bash, "bash_returned": sum(x["returned"] or 0 for x in bash)}


def spread(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return {"n": 0}
    return {"n": len(xs), "mean": round(statistics.mean(xs), 3), "min": round(min(xs), 3), "max": round(max(xs), 3),
            "sd": round(statistics.stdev(xs), 3) if len(xs) > 1 else None}


def main():
    scores = json.load(open(SAVED_SCORES))["runs"]
    scratch, manifest = doc_evidence.rebuild(EVIDENCE, doc_evidence.DEFAULT_PROJECT)
    rows, missing = {}, []
    for r in manifest["runs"]:
        s = scores.get(r["id"])
        if not s or not s["included"]:
            continue
        framework = set(subprocess.run(["git", "-C", scratch, "diff", "--name-only", "--no-renames", r["start"], r["install"]],
                                       capture_output=True, text=True, check=True).stdout.split("\n")) - {""}
        stop = first_stop(r["tree_was"] + ".stream.jsonl")
        p0 = run_phase0(r["transcript"], r["tree_was"], scratch, r, framework) if r["transcript"] and os.path.exists(r["transcript"]) else None
        if stop is None or p0 is None:
            missing.append({"id": r["id"], "stream": stop is not None, "transcript": p0 is not None})
        rows[r["id"]] = {"group": s["group"], "arm": s["arm"], "cli": r["cli"], "framework_files": len(framework), "first_stop": stop, "phase0": p0}
    groups = {}
    for g in ("v3.0", "v3.7", "v3.8-text"):
        sel = [v for v in rows.values() if v["group"] == g]
        costs = [v["first_stop"]["cost_usd"] for v in sel if v["first_stop"]]
        groups[g] = {"runs": len(sel), "cost_usd": spread(costs), "turns": spread([v["first_stop"]["turns"] for v in sel if v["first_stop"]]),
                     "duration_s": spread([v["first_stop"]["duration_s"] for v in sel if v["first_stop"]]),
                     "tool_calls": spread([v["phase0"]["tool_calls"] for v in sel if v["phase0"]]),
                     "framework_reads": spread([v["phase0"]["reads_by_kind"]["framework"]["n"] for v in sel if v["phase0"]]),
                     "record_reads": spread([v["phase0"]["reads_by_kind"]["record"]["n"] for v in sel if v["phase0"]]),
                     "framework_returned": spread([v["phase0"]["reads_by_kind"]["framework"]["returned"] for v in sel if v["phase0"]]),
                     "record_returned": spread([v["phase0"]["reads_by_kind"]["record"]["returned"] for v in sel if v["phase0"]]),
                     "bash_returned": spread([v["phase0"]["bash_returned"] for v in sel if v["phase0"]]),
                     "tool_result_chars": spread([v["phase0"]["tool_result_chars"] for v in sel if v["phase0"]])}
    allc = [v["first_stop"]["cost_usd"] for v in rows.values() if v["first_stop"]]
    mean_all = statistics.mean(allc)
    per_group_mean = {g: groups[g]["cost_usd"].get("mean") for g in groups}
    est = {"basis": "mean first-stop cost over the scored runs that have a stream log; a measurement of the ORIGINAL sessions' first turn, not of a probe",
           "mean_all": round(mean_all, 3), "max_any": round(max(allc), 3), "per_group_mean": per_group_mean,
           "pilot_four_probes": round(sum(per_group_mean[g] for g in ("v3.0", "v3.7", "v3.8-text")) + per_group_mean["v3.8-text"], 2),
           "main_27_probes": round(27 * mean_all, 2), "main_27_probes_with_margin": round(27 * mean_all * (1 + MARGIN), 2), "margin": MARGIN,
           "plan_guess_per_probe": 1.0}
    result = {"about": __doc__.split("\n")[0], "scored_runs": len(rows), "missing_inputs": missing, "groups": groups, "estimate": est, "runs": rows}
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print(f"{len(rows)} scored runs; missing a stream log or a transcript: {[m['id'] for m in missing] or 'none'}")
    print(f"{'group':10}{'n':>3}  {'first-stop cost $':>26}  {'turns':>12}  {'tool calls':>12}  {'fw reads':>9} {'rec reads':>9}  {'fw KB':>7} {'rec KB':>7} {'bash KB':>8}")
    for g, v in groups.items():
        c = v["cost_usd"]
        print(f"{g:10}{v['runs']:>3}  {c.get('mean', 0):>7.3f} ({c.get('min', 0):.3f}-{c.get('max', 0):.3f})  {v['turns'].get('mean', 0):>12.1f}  {v['tool_calls'].get('mean', 0):>12.1f}  "
              f"{v['framework_reads'].get('mean', 0):>9.1f} {v['record_reads'].get('mean', 0):>9.1f}  {v['framework_returned'].get('mean', 0) / 1024:>7.1f} {v['record_returned'].get('mean', 0) / 1024:>7.1f} {v['bash_returned'].get('mean', 0) / 1024:>8.1f}")
    print(json.dumps(est, indent=1))


if __name__ == "__main__":
    main()
