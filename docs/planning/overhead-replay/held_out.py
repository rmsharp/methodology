"""Independent checks on each run's final tree, with no model spend (R only).

    python3 held_out.py OUTJSON

For each valid run, in a clone of the run's tree at the commit where #121 was closed out:
  held_out   the REAL fix's test files (54b87c1da, never visible to a session) run against the run's source
             (test_getPedMaxAge.R and test_gvaConvergence_kinshipOverrides.R), plus test_modPyramid.R from the
             start commit (which carried the 5 pyramid warnings): counts of failures/errors/warnings
  reverse    the run's OWN changed test files run against the ORIGINAL source (R/ restored to the start commit):
             a test that cannot fail on the bug proves nothing; expects failures > 0 for a source-fixing run
"""
import json, os, shutil, subprocess, sys
REAL = "54b87c1da"; START = "879503cce9936704eafc3709c2fc9db8328ccc43"; REPO = os.path.expanduser("~/Development/nprcgenekeepr")
RUNS = {("v3.7", 2): "7b9bd618", ("v3.7", 3): None, ("v3.7", 4): None, ("v3.7", 6): None, ("v3.7", 7): None,
        ("v3.0", 1): None, ("v3.0", 3): "b15ae1c5", ("v3.0", 4): None, ("v3.0", 5): None, ("v3.0", 6): None, ("v3.7", 5): None}
R = """suppressMessages(pkgload::load_all('.', quiet=TRUE)); f <- commandArgs(TRUE)
for (x in f) { r <- as.data.frame(testthat::test_file(x, reporter='silent'))
  cat('RES', basename(x), sum(r$failed), sum(r$error), sum(r$warning), sum(r$nb), '\\n') }"""


def sh(*a, cwd=None):
    return subprocess.run(list(a), cwd=cwd, capture_output=True, text=True)


def run_tests(tree, files):
    env = dict(os.environ, NOT_CRAN="true")
    p = subprocess.run(["Rscript", "--vanilla", "-e", R, *files], cwd=tree, capture_output=True, text=True, env=env, timeout=900)
    return {l.split()[1]: list(map(int, l.split()[2:])) for l in p.stdout.splitlines() if l.startswith("RES")}


def main(out):
    res = {}
    real = {n: sh("git", "show", f"{REAL}:tests/testthat/{n}", cwd=REPO).stdout for n in
            ("test_getPedMaxAge.R", "test_gvaConvergence_kinshipOverrides.R")}
    pyr = sh("git", "show", f"{START}:tests/testthat/test_modPyramid.R", cwd=REPO).stdout
    for (arm, rep), sha in RUNS.items():
        src = f"/tmp/overhead-real/{arm}-r{rep}"
        t = f"/tmp/held/{arm}-r{rep}"
        shutil.rmtree(t, ignore_errors=True)
        sh("git", "clone", "-q", "--no-local", src, t)
        if sha:
            sh("git", "checkout", "-q", sha, cwd=t)
        base = next(l.split()[0] for l in sh("git", "log", "--format=%h %s", cwd=t).stdout.splitlines() if "Install methodology arm" in l)
        changed = [f for f in sh("git", "diff", "--name-only", base, "HEAD", "--", "tests/testthat", cwd=t).stdout.split() if f.endswith(".R")]
        # reverse: own tests against ORIGINAL R/
        shutil.rmtree(f"/tmp/held/{arm}-r{rep}-rev", ignore_errors=True)
        sh("git", "clone", "-q", "--no-local", t, f"/tmp/held/{arm}-r{rep}-rev")
        rev = f"/tmp/held/{arm}-r{rep}-rev"
        sh("git", "checkout", "-q", base, "--", "R", cwd=rev)
        own = run_tests(rev, changed) if changed else {}
        # held-out: real tests + original pyramid test against the run's source
        for n, body in real.items():
            open(os.path.join(t, "tests/testthat", n), "w").write(body)
        open(os.path.join(t, "tests/testthat/test_modPyramid.R"), "w").write(pyr)
        held = run_tests(t, [f"tests/testthat/{n}" for n in (*real, "test_modPyramid.R")])
        res[f"{arm}-r{rep}"] = {"held_out": held, "reverse_own_tests_on_original_source": own, "own_test_files": changed}
        print(arm, rep, "held-out", held, "| own tests on original source", own, flush=True)
    json.dump(res, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
