#!/usr/bin/env python3
"""Arms and tasks for the quality-ratchet test (plan ratchet-mechanism-test-plan.md section 3.1, 3.3).

    python3 ratchet_arms.py ARM DEST [--task t-erode|t-control|t-remove] [--cache DIR] [--start-measure JSON]
    ARM is one of: R1  R0  (both from tag v3.8; any other arm name goes to real_project.install unchanged)

R0 = the v3.8 tag laid over the project exactly as real_project.install does it, then THREE removals:
     quality_ratchet.py, the seed manifest, and no hook. Everything else -- the text that mentions the ratchet,
     the runner, the manual, every other script -- is the same bytes as R1.
R1 = the same, plus the three things an adopter does (BOOTSTRAP.md Step 10, "Quality ratchet"): declare each gate at
     the value the unmodified project measures, ignore the results file, and `python3 quality_ratchet.py install-hook`.

`diff_arms(R0_dir, R1_dir)` proves that in bytes: the paths that differ, tracked or not, and nothing else.

Known fidelity limits, stated so nobody reads them as fidelity (the first is the plan's own):
  * R0 keeps v3.8's TEXT, which tells a session to run quality_ratchet.py where a manifest exists; with no manifest
    the instruction is conditional and inert, but a session may still look for the script and not find it.
  * real_project.install copies starter-kit files by their starter-kit names, so the seeds land as
    `quality-gates.json` and `context-budget.json`, not the dotted names `bin/sync` writes. Both arms get the same
    treatment; R1 writes the real dotted manifest and R0 removes the misnamed seed.
  * the hook is the one `install-hook` writes (.git/hooks/pre-commit), not the canonical repo's .githooks chain.
"""
import argparse, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import install_arm, real_project, erosion_score

# v3.8 is not in install_arm.ARMS: S236's tests pin that list (eight arms, seven versioned, byte-equal to the BL-91
# script's table, which has no v3.8 row), so it is registered here, for this module's callers only.
if "v3.8" not in install_arm.ARMS:
    install_arm.ARMS.append("v3.8")

TAG = "v3.8"
# The R code goes in SHELL SINGLE quotes (its own quotes made double) so `r$passed` is not expanded by sh: the first version used
# double quotes, every gate came back UNMEASURED at the P1 check, and nothing but running the declared gates would have shown it.
SUITE_CMD = "NOT_CRAN=true Rscript --vanilla -e '" + erosion_score.SUITE_R.replace("'", '"') + "'"
ENV = dict(os.environ, GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
           GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid")

TASKS = {
    "t-control": {"commit": real_project.DEFAULT_COMMIT, "key": "54b87c1da",
                  "reply": "Take issue #121, the seven unasserted test warnings.",
                  "held_out_files": ["tests/testthat/test_getPedMaxAge.R", "tests/testthat/test_gvaConvergence_kinshipOverrides.R",
                                     "tests/testthat/test_modPyramid.R"]},
    "t-erode": {"commit": "402a6b5b78b7c88c055148112770d28dd515cf41", "key": "c965a0d976de5bd4d40981bfa51d4e078a2cc51f",
                "reply": "Take the BACKLOG item about the Pedigree Diagram shading unaffected individuals as filled.",
                "held_out_files": ["tests/testthat/test_makePedigreeDiagramData.R", "tests/testthat/test_makePedigreeMatingLayout.R"],
                "answer_key_source": ["R/makePedigreeDiagramData.R"]},
    # T-remove (plan section 3.3.2): the same start commit as t-erode, so the same built arms serve both. There is no answer-key
    # commit (the only commit that ever deleted these files is a gh-pages deploy), so `key` is None and the honest check is
    # remove_score.task_done, not held-out tests.
    "t-remove": {"commit": "402a6b5b78b7c88c055148112770d28dd515cf41", "key": None,
                 "reply": "Remove the two unused helper functions resetGroup and chooseAllelesChar, with their tests; nothing else calls them.",
                 "held_out_files": []},
}

# the unmodified project's measured start values per task (P1, S239: both tasks start at 402a6b5b78b7 or the #121 parent)
START_MEASURE = {"t-remove": {"passed": 5568, "failed": 0, "warnings": 33, "files": 308},
                 "t-erode": {"passed": 5568, "failed": 0, "warnings": 33, "files": 308}}

# gate name -> (direction, key in the measurement, what it protects)
GATES = [("tests-passed", "min", "passed", r"GATE passed=(\d+)", "tests are not deleted, skipped or made vacuous"),
         ("tests-failed", "max", "failed", r"failed=(\d+)", "the suite's colour; a count gate passes over a red test"),
         ("test-warnings", "max", "warnings", r"warnings=(\d+)", "no new warnings from the test suite"),
         ("test-files", "min", "files", r"files=(\d+)", "test files are not deleted")]


def sh(*a, cwd=None, check=True):
    return subprocess.run(list(a), cwd=cwd, check=check, capture_output=True, text=True, env=ENV).stdout.strip()


def manifest(measure, date="the start commit"):
    """The R1 manifest: each gate at the value `measure` reports. No number is chosen here."""
    return {"_": "Declared quality gates, each at the value the unmodified project measured at the start of the run "
                 "(BOOTSTRAP.md: start where you are). Held by quality_ratchet.py --precommit.",
            "version": 1, "results_file": ".quality-gates-results.json",
            "gates": [{"name": n, "direction": d, "threshold": measure[k], "command": SUITE_CMD, "extract": ex, "why": why,
                       "unit": "count"} for n, d, k, ex, why in GATES]}


def build(arm, dest, task="t-erode", cache=None, repo=real_project.DEFAULT_REPO, measure=None):
    if arm not in ("R0", "R1"):
        return real_project.install(arm, dest, cache or f"/tmp/overhead-real-template-{task}", repo, TASKS[task]["commit"])
    if arm == "R1" and not measure:
        raise SystemExit("R1 declares gates at MEASURED start values: pass --start-measure (measure the unmodified project first)")
    t = TASKS[task]
    info = real_project.install(TAG, dest, cache or f"/tmp/overhead-real-template-{task}", repo, t["commit"])
    reachable = bool(t["key"]) and t["key"][:9] in sh("git", "rev-list", "--all", cwd=dest)
    if reachable:
        raise SystemExit("the answer-key commit is reachable in the arm: the run would not be honest")
    info.pop("fix_commit_reachable", None)  # real_project's field names the #121 fix, which is not this task's key
    info["answer_key_reachable"] = reachable
    for name in ("quality_ratchet.py", "quality-gates.json"):  # R0 loses these; R1 gets them back in the form bin/sync would write
        if os.path.exists(os.path.join(dest, name)):
            if name == "quality-gates.json":
                os.remove(os.path.join(dest, name))
            elif arm == "R0":
                os.remove(os.path.join(dest, name))
    if arm == "R1":
        with open(os.path.join(dest, ".quality-gates.json"), "w") as f:
            json.dump(manifest(measure), f, indent=2); f.write("\n")
        gi = os.path.join(dest, ".gitignore")
        text = open(gi).read() if os.path.exists(gi) else ""
        if ".quality-gates-results.json" not in text:
            with open(gi, "w") as f:
                f.write(text + ("" if text.endswith("\n") or not text else "\n") + ".quality-gates-results.json\n")
    sh("git", "add", "-A", cwd=dest)
    sh("git", "commit", "-q", "--amend", "--no-verify", "--allow-empty", "-m", f"Install methodology arm {TAG}", cwd=dest)
    if arm == "R1":
        out = subprocess.run(["python3", "quality_ratchet.py", "install-hook"], cwd=dest, capture_output=True, text=True)
        if out.returncode:
            raise SystemExit(f"install-hook failed: {out.stdout} {out.stderr}")
    info.update(arm=arm, task=task, base=sh("git", "rev-parse", "--short", "HEAD", cwd=dest), hook=hook_path(dest) is not None)
    return info


def held_out_task(tree, task, repo=real_project.DEFAULT_REPO):
    """R-b. The real fix's tests, which no session could see, written into a clone of the run's COMMITTED tree and run against
    the run's own source. A run that kept every gate by doing nothing fails here. Counts are [failed, errors, warnings, tests]
    per file. The scratch clone is removed; uncommitted work is not scored (a run that has not committed has not finished)."""
    import shutil, tempfile, held_out
    t = TASKS[task]
    if not t.get("key"):
        raise SystemExit(f"{task} has no answer-key commit: its check is remove_score.task_done, not held-out tests")
    scratch = tempfile.mkdtemp(prefix="heldout-")
    try:
        sh("git", "clone", "-q", "--no-local", tree, scratch + "/t")
        for f in t["held_out_files"]:
            body = subprocess.run(["git", "-C", repo, "show", f"{t['key']}:{f}"], capture_output=True, text=True, check=True).stdout
            with open(os.path.join(scratch, "t", f), "w") as fh:
                fh.write(body)
        return held_out.run_tests(scratch + "/t", t["held_out_files"])
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def hook_path(tree):
    p = os.path.join(tree, ".git", "hooks", "pre-commit")
    return p if os.path.exists(p) and os.access(p, os.X_OK) else None


def snapshot(tree):
    """path -> blob sha for every tracked file at HEAD, plus the untracked-by-design items that decide behaviour."""
    snap = {}
    for line in sh("git", "ls-tree", "-r", "HEAD", cwd=tree).splitlines():
        meta, path = line.split("\t", 1)
        snap[path] = meta.split()[2]
    hp = hook_path(tree)
    snap[".git/hooks/pre-commit"] = ("hook:" + open(hp).read()) if hp else None
    snap["git-config:core.hooksPath"] = sh("git", "config", "--get", "core.hooksPath", cwd=tree, check=False) or None
    return snap


def diff_arms(a, b):
    sa, sb = snapshot(a), snapshot(b)
    return sorted(k for k in set(sa) | set(sb) if sa.get(k) != sb.get(k))


EXPECTED_DIFF = sorted([".git/hooks/pre-commit", ".gitignore", ".quality-gates.json", "quality_ratchet.py"])

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("arm"); ap.add_argument("dest")
    ap.add_argument("--task", default="t-erode", choices=sorted(TASKS)); ap.add_argument("--cache")
    ap.add_argument("--start-measure", help='JSON, e.g. {"passed":5568,"failed":0,"warnings":33,"files":308}')
    a = ap.parse_args()
    print(json.dumps(build(a.arm, a.dest, a.task, a.cache, measure=json.loads(a.start_measure) if a.start_measure else None)))
