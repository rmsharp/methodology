"""Which exit code does a proof written by trimmer vX give when git cannot read the trim commit's
parent (a depth-1 clone)? Usage: python3 -I exit_by_version.py <tests module> <label=trimmer>..."""
import importlib.util, pathlib, subprocess, sys, tempfile
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("t", sys.argv[1])
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
for arg in sys.argv[2:]:
    label, path = arg.split("=", 1)
    t.TRIM_PY = pathlib.Path(path)
    with tempfile.TemporaryDirectory() as tmp:
        p = t.make_handoff_repo(tmp)
        r = t.run_trim(p, "--file", "HANDOFFS.md", "--cut", "2", "--write", "--today", "2026-02-01")
        assert "[WROTE]" in r.stdout, r.stdout
        t.sh(p, "git", "add", "-A"); t.sh(p, "git", "commit", "-qm", "trim")
        shard = sorted((p / "docs" / "archive").glob("HANDOFFS-through-*.md"))[0].relative_to(p).as_posix()
        clone = pathlib.Path(tmp) / "shallow"
        subprocess.run(["git", "clone", "-q", "--depth", "1", "file://" + str(p), str(clone)], check=True)
        run = subprocess.run(["bash", str(clone / (shard + ".verify.sh"))], cwd=str(clone),
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        last = [ln for ln in run.stdout.splitlines() if ln.strip()][-1:] or [""]
        print("%-8s proof exit %d | %s" % (label, run.returncode, last[0][:140]))
