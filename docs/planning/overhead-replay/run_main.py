#!/usr/bin/env python3
"""P3, T-remove: run the main ablation serially, one driver.py launch per (arm, rep), and stop on trouble.

    python3 run_main.py [--reps 5] [--out /tmp/ratchet-main] [--total-cap 100] [--session-cap 10] [--arms R1,R0,v3.0 | R1:5,R0:3] [--task t-remove] [--seed LEDGER]

Order is rep-major (R1 rep 1, R0 rep 1, v3.0 rep 1, R1 rep 2, ...), so an interrupted batch is balanced, not three arms of unequal size.
The shared ledger OUT/spend.jsonl is seeded once from the P2 pilot's ledger, so the operator's $100 cap (plan section 7, D2) is
CUMULATIVE: driver.py refuses to launch any run whose session cap would take the ledger past --total-cap, and this script stops then.
A cell that already has a row in OUT/rows.jsonl is skipped, so a re-run resumes. Two consecutive failed launches stop the batch.
The pilot's three runs are NOT rows of this study (they used the old stop-2 wording, plan D8); only their dollars count.
"""
import argparse, json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PILOT_LEDGER = os.path.join(HERE, "pilot", "ratchet-t-remove", "spend.jsonl")


def done_cells(out):
    p = os.path.join(out, "rows.jsonl")
    return {(r["arm"], r["rep"]) for r in map(json.loads, open(p)) if "arm" in r} if os.path.exists(p) else set()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=5); ap.add_argument("--out", default="/tmp/ratchet-main")
    ap.add_argument("--total-cap", type=float, default=100.0); ap.add_argument("--session-cap", type=float, default=10.0)
    ap.add_argument("--arms", default="R1,R0,v3.0"); ap.add_argument("--task", default="t-remove")
    ap.add_argument("--seed", default=PILOT_LEDGER, help="a spend ledger copied into a NEW out dir, so the cap stays cumulative across batches")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    ledger = os.path.join(a.out, "spend.jsonl")
    if not os.path.exists(ledger):
        shutil.copy(a.seed, ledger)
    fails = 0
    plan = {x.split(":")[0]: int(x.split(":")[1]) if ":" in x else a.reps for x in a.arms.split(",")}  # "R1:5,R0:3" gives each arm its own n
    for rep in range(1, max(plan.values()) + 1):
        for arm, n in plan.items():
            if rep > n or (arm, rep) in done_cells(a.out):
                continue
            shutil.rmtree(os.path.join(a.out, f"{arm}-r{rep}"), ignore_errors=True)  # a half-run cell is rebuilt, not resumed
            p = subprocess.run([sys.executable, os.path.join(HERE, "driver.py"), arm, str(rep), "--project", "ratchet", "--task", a.task,
                                "--out", a.out, "--session-cap", str(a.session_cap), "--total-cap", str(a.total_cap)],
                               capture_output=True, text=True)
            ok = p.returncode == 0 and (arm, rep) in done_cells(a.out)
            print(f"{arm} rep {rep}: {'ok' if ok else 'FAILED rc=' + str(p.returncode)}", flush=True)
            if "refused: spent" in (p.stderr + p.stdout):
                print("stopped: the cumulative cap would be passed", flush=True); return 2
            fails = 0 if ok else fails + 1
            if fails >= 2:
                print("stopped: two consecutive failures; last stderr:", p.stderr[-600:], flush=True); return 1
    print("batch complete", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
