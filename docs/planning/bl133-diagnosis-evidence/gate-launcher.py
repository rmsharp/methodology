"""gate-launcher.py -- run `bash bin/tests.sh` the way quality_ratchet.py launches a gate command, N times, keeping each
run's whole output. It calls the clone's own run_gate_command (a shell, pipes for stdout and stderr, a session of its
own), so the launch is the tool's, not a copy of it.
Usage: python3 -B gate-launcher.py <clone-directory> <output-directory> <N>
Run it on a SCRATCH clone. Prints one line per run: exit code, seconds, the load average at the end, the suite's summary
line and any FAIL lines."""
import sys, os, time
sys.dont_write_bytecode = True
CLONE, OUT, N = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]), int(sys.argv[3])
sys.path.insert(0, os.path.join(CLONE, "starter-kit"))
import quality_ratchet as qr
os.makedirs(OUT, exist_ok=True)
for i in range(1, N + 1):
    t = time.time()
    rc, out, err, timed_out = qr.run_gate_command("bash bin/tests.sh", CLONE, 3600)
    open(f"{OUT}/run{i}.out", "w").write(out); open(f"{OUT}/run{i}.err", "w").write(err)
    summ = [l for l in out.splitlines() if l.startswith("== Summary")]
    bad = [l for l in out.splitlines() if "FAIL:" in l]
    print(f"run {i} rc={rc} timed_out={timed_out} secs={time.time()-t:.0f} load={os.getloadavg()} summary={summ} fails={[b[:140] for b in bad]}", flush=True)
print("DONE", flush=True)
