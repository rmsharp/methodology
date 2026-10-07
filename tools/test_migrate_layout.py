#!/usr/bin/env python3
"""Unit tests for bin/migrate-layout (BL-101, phase P7).

CANONICAL-ONLY, like tools/test_sync_layouts.py: bin/migrate-layout is not in bin/_manifest.py, so adopters
do not receive it. The contract is docs/planning/methodology-subdirectory-plan.md section 4.7 and section 7.3
row P7: a dry run by default; a refusal of a dirty tree, a half-migrated tree, a destination that exists and a
tree where bin/status does not read every TRACKED file current; the plan printed as data; the apply as ONE
commit with every moved file at 90% similarity or better; a committed ledger entry or a frozen shard never
rewritten.

Every test drives the tool as a command in a scratch git project that the real bin/sync wrote and that is
then committed, so the fixture is what an adopter is and not what a test imagines. The tool is asked for
--json, which is the report as data; a few tests read the text a person reads. Every rule is observed failing
as well as passing (Learning #12), and the tests are written before the code they pin.
"""
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True  # a test run must not generate bin/__pycache__ or tools/__pycache__

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
MIGRATE = REPO / "bin" / "migrate-layout"
SYNC = REPO / "bin" / "sync"
STATUS = REPO / "bin" / "status"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


manifest = _load("_manifest", REPO / "bin" / "_manifest.py")
LEGACY = [(src, dest, disp) for src, dest, disp in manifest.DISTRIBUTION]
TRACKED_DESTS = [dest for _s, dest, disp in LEGACY if disp == manifest.TRACKED]
SEED_DESTS = [dest for _s, dest, disp in LEGACY if disp == manifest.SEED]
NEW_OF = {dest: manifest.NEW_LAYOUT[src] for src, dest, _d in LEGACY}  # legacy destination -> new destination


def git(path, *args, check=True):
    """git -C path ... ; returns stdout. A failure raises, naming the command and what git said."""
    r = subprocess.run(["git", "-C", str(path), "-c", "user.email=t@t", "-c", "user.name=t",
                        "-c", "commit.gpgsign=false", *args], capture_output=True, text=True)
    if check and r.returncode:
        raise AssertionError("git %s failed in %s:\n%s%s" % (" ".join(args), path, r.stdout, r.stderr))
    return r.stdout


def run_migrate(project, *args, json_out=True):
    """bin/migrate-layout as a command. With json_out the report is read as data into .report (None when the
    output is not JSON); .out is stdout and stderr joined."""
    cmd = [sys.executable, "-B", str(MIGRATE), str(project)]
    if json_out:
        cmd.append("--json")
    r = subprocess.run([*cmd, *args], capture_output=True, text=True)
    r.out = r.stdout + r.stderr
    try:
        r.report = json.loads(r.stdout) if json_out else None
    except ValueError:
        r.report = None
    return r


def tree_state(project):
    """Everything about a project a read-only run must leave alone: HEAD, the status, and a digest of every
    file's bytes (the .git directory left out)."""
    root = Path(project)
    digests = {}
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root)
        if p.is_file() and ".git" not in rel.parts:
            digests[rel.as_posix()] = hashlib.sha1(p.read_bytes()).hexdigest()
    return (git(project, "rev-parse", "HEAD").strip(), git(project, "status", "--porcelain"), digests)


def files_of(project):
    root = Path(project)
    return {p.relative_to(root).as_posix() for p in root.rglob("*")
            if p.is_file() and ".git" not in p.relative_to(root).parts}


def commit_all(project, message):
    git(project, "add", "-A")
    git(project, "commit", "-q", "-m", message)


def ledger_with_entries(seed_text, n=40):
    """The CHANGELOG.md seed without its sentinel, followed by n dated entries: a ledger an adopter has been
    keeping, large enough that one more entry does not take a rename below 90% similarity."""
    text = re.sub(r"<!-- METHODOLOGY-SEED-SENTINEL.*?-->\n", "", seed_text, flags=re.S)
    entries = "".join("### 2026-09-%02d · [ad hoc] Entry %d\n\n%s\n\n" % (1 + i % 28, i, ("Body of entry %d. " % i) * 14)
                      for i in range(n))
    return text.rstrip("\n") + "\n\n" + entries


CLAUDE_MD = """# Project

<!-- SESSION PROTOCOL -->
Read and follow `SESSION_RUNNER.md` step by step. Orient first: read SAFEGUARDS.md, then SESSION_NOTES.md,
then run `methodology_dashboard.py`.

This project follows `docs/methodology/workstreams/DEVELOPMENT_WORKSTREAM.md` in standard mode, and the
theory is in [the manual](docs/methodology/ITERATIVE_METHODOLOGY.md).

Kept qualified on purpose (a path with a directory in front is not a bare name):
the canonical copy is `../methodology/starter-kit/SESSION_RUNNER.md`, and upstream is
https://github.com/KJ5HST/methodology/blob/main/SESSION_RUNNER.md and `starter-kit/SAFEGUARDS.md`.

Not a methodology file: SESSION_RUNNER.mdx, MY_CHANGELOG.md, NOTES-CHANGELOG.md.
"""

GATES = {
    "version": 1,
    "results_file": ".quality-gates-results.json",
    "gates": [{
        "name": "ledger-lag", "direction": "max", "threshold": 3,
        "command": "git rev-list --count --no-merges \"$(git log -1 --format=%H -- CHANGELOG.md)..HEAD\"",
        "why": "Commits after the newest commit that touched CHANGELOG.md -- Phase 0's reconcile set.",
    }],
}

GITIGNORE = """# generated by the methodology tools
/dashboard.html
dashboard_history.jsonl
/.quality-gates-results.json
.context-budget-history.jsonl
"""


def customise(project):
    """Make the freshly synced project look like an adopter that has been working: a ledger with entries, a
    CLAUDE.md that names its methodology files, configs that name them too, a .gitignore, generated files, a
    project-owned file beside the methodology ones under docs/methodology/, and two ledger shards."""
    p = Path(project)
    seed = (REPO / "starter-kit" / "CHANGELOG.md").read_text(encoding="utf-8")
    (p / "CHANGELOG.md").write_text(ledger_with_entries(seed), encoding="utf-8")
    (p / "CLAUDE.md").write_text(CLAUDE_MD, encoding="utf-8")
    (p / ".gitignore").write_text(GITIGNORE, encoding="utf-8")
    (p / ".quality-gates.json").write_text(json.dumps(GATES, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (p / "docs" / "methodology").mkdir(parents=True, exist_ok=True)
    (p / "docs" / "methodology" / "PROJECT_CONVENTIONS.md").write_text("# Conventions\n\nThis project's own.\n", encoding="utf-8")
    for name in ("dashboard_history.jsonl", ".context-budget-history.jsonl"):
        (p / name).write_text('{"timestamp": "2026-09-01T00:00:00"}\n', encoding="utf-8")
    (p / "docs" / "archive").mkdir(parents=True, exist_ok=True)
    for name in ("CHANGELOG-through-2026-08-01.md", "CHANGELOG-through-2026-08-01.md.verify.sh",
                 "HANDOFFS-through-2026-08-02.md", "HANDOFFS-through-2026-08-02.md.verify.sh"):
        (p / "docs" / "archive" / name).write_text("# shard %s\n" % name, encoding="utf-8")
    (p / "docs" / "archive" / "project-notes.md").write_text("# The project's own archive\n", encoding="utf-8")


_BASE = []


def base_project():
    """A legacy adopter, built once by the real bin/sync, customised and committed. Tests copy it."""
    if not _BASE:
        keep = tempfile.mkdtemp(prefix="migrate-base-")
        project = Path(keep) / "adopter"
        project.mkdir()
        git(project, "init", "-q")
        r = subprocess.run([sys.executable, "-B", str(SYNC), str(project)], capture_output=True, text=True)
        assert r.returncode == 0, "the base project could not be synced:\n%s%s" % (r.stdout, r.stderr)
        customise(project)
        commit_all(project, "an adopter at the legacy layout")
        # generated files that are ignored, so not committed: they exist on disk only
        (project / "dashboard.html").write_text("<!-- generated -->\n", encoding="utf-8")
        (project / ".quality-gates-results.json").write_text("{}\n", encoding="utf-8")
        _BASE.append(project)
    return _BASE[0]


def tearDownModule():
    for project in _BASE:
        shutil.rmtree(project.parent, ignore_errors=True)


class Adopter(unittest.TestCase):
    """A scratch copy of the base project for each test."""

    def setUp(self):
        self._td = tempfile.TemporaryDirectory(prefix="migrate-layout-")
        self.addCleanup(self._td.cleanup)
        self.project = Path(self._td.name) / "adopter"
        shutil.copytree(base_project(), self.project, symlinks=True)

    def commit(self, message="a change"):
        commit_all(self.project, message)

    def moves(self, report):
        return {m["src"]: m["dest"] for m in report["moves"]}


class TestUsageAndNothingToDo(unittest.TestCase):
    """The shapes of project the tool is not for, and what it says about each."""

    def setUp(self):
        self._td = tempfile.TemporaryDirectory(prefix="migrate-usage-")
        self.addCleanup(self._td.cleanup)
        self.root = Path(self._td.name)

    def test_a_missing_directory_is_a_usage_error(self):
        r = run_migrate(self.root / "nope")
        self.assertEqual(r.returncode, 2, r.out)
        self.assertIn("not a directory", r.out)

    def test_a_directory_that_is_not_a_git_repository_is_refused(self):
        (self.root / "plain").mkdir()
        r = run_migrate(self.root / "plain")
        self.assertEqual(r.returncode, 1, r.out)
        self.assertEqual(r.report["status"], "refused")
        self.assertEqual([x["code"] for x in r.report["refusals"]], ["not-a-repository"])

    def test_a_repository_with_no_methodology_files_has_nothing_to_migrate(self):
        project = self.root / "bare"
        project.mkdir()
        git(project, "init", "-q")
        (project / "README.md").write_text("# bare\n", encoding="utf-8")
        commit_all(project, "a project that has not adopted the methodology")
        before = tree_state(project)
        r = run_migrate(project, "--apply")
        self.assertEqual(r.returncode, 0, r.out)
        self.assertEqual(r.report["status"], "nothing-to-do")
        self.assertEqual(r.report["moves"], [])
        self.assertEqual(tree_state(project), before, "a project with nothing to migrate was changed")

    def test_a_repository_with_no_commits_is_refused(self):
        project = self.root / "fresh"
        project.mkdir()
        git(project, "init", "-q")
        (project / "SESSION_RUNNER.md").write_text("# runner\n", encoding="utf-8")
        r = run_migrate(project)
        self.assertEqual(r.returncode, 1, r.out)
        self.assertIn("no-commits", [x["code"] for x in r.report["refusals"]])


class TestTheDryRun(Adopter):
    """Dry run is the default (plan 4.7): it reads, prints the plan as data and writes nothing."""

    def test_it_writes_nothing(self):
        before = tree_state(self.project)
        r = run_migrate(self.project)
        self.assertEqual(r.returncode, 0, r.out)
        self.assertEqual(r.report["mode"], "dry-run")
        self.assertEqual(tree_state(self.project), before, "a dry run changed the project")

    def test_it_plans_one_move_for_every_manifest_file_the_project_holds(self):
        r = run_migrate(self.project)
        got = self.moves(r.report)
        for dest in (d for _s, d, _x in LEGACY):
            self.assertEqual(got.get(dest), NEW_OF[dest], "no move planned for %s" % dest)

    def test_it_plans_the_two_tracked_history_files_the_generated_ignored_ones_and_the_ledger_shards(self):
        r = run_migrate(self.project)
        got = self.moves(r.report)
        self.assertEqual(got["dashboard_history.jsonl"], "methodology/dashboard_history.jsonl")
        self.assertEqual(got[".context-budget-history.jsonl"], "methodology/.context-budget-history.jsonl")
        self.assertEqual(got["dashboard.html"], "methodology/dashboard.html")
        self.assertEqual(got[".quality-gates-results.json"], "methodology/.quality-gates-results.json")
        for shard in ("CHANGELOG-through-2026-08-01.md", "CHANGELOG-through-2026-08-01.md.verify.sh",
                      "HANDOFFS-through-2026-08-02.md", "HANDOFFS-through-2026-08-02.md.verify.sh"):
            self.assertEqual(got["docs/archive/" + shard], "methodology/archive/" + shard)

    def test_it_moves_nothing_else_and_names_what_it_leaves(self):
        r = run_migrate(self.project)
        got = self.moves(r.report)
        self.assertNotIn("docs/methodology/PROJECT_CONVENTIONS.md", got)
        self.assertNotIn("docs/archive/project-notes.md", got)
        self.assertNotIn("CLAUDE.md", got)
        self.assertNotIn(".gitignore", got)
        left = {x["path"]: x["reason"] for x in r.report["left_in_place"]}
        self.assertIn("docs/methodology/PROJECT_CONVENTIONS.md", left)
        self.assertIn("docs/archive/project-notes.md", left)

    def test_each_move_says_whether_git_tracks_the_file(self):
        r = run_migrate(self.project)
        tracked = {m["src"]: m["tracked"] for m in r.report["moves"]}
        self.assertTrue(tracked["SESSION_RUNNER.md"])
        self.assertFalse(tracked["dashboard.html"])
        self.assertFalse(tracked[".quality-gates-results.json"])

    def test_the_text_a_person_reads_names_the_mode_and_prints_every_git_mv(self):
        r = run_migrate(self.project, json_out=False)
        self.assertEqual(r.returncode, 0, r.out)
        self.assertRegex(r.out, r"(?i)dry run")
        self.assertIn("--apply", r.out)
        self.assertIn("git mv SESSION_RUNNER.md methodology/SESSION_RUNNER.md", r.out)
        self.assertIn("git mv docs/methodology/ITERATIVE_METHODOLOGY.md methodology/ITERATIVE_METHODOLOGY.md", r.out)

    def test_the_report_names_the_layout_and_the_tier(self):
        r = run_migrate(self.project)
        self.assertEqual(r.report["layout"], "legacy")
        self.assertEqual(r.report["tier"], "all")


class TestRefusals(Adopter):
    """Plan 4.7: a dirty tree, a half-migrated tree, a destination that exists and a tree where bin/status does
    not read every TRACKED file current are each refused, under a dry run and under --apply, and nothing is written."""

    def refused(self, code, *args):
        before = tree_state(self.project)
        for mode in ((), ("--apply",)):
            r = run_migrate(self.project, *args, *mode)
            self.assertEqual(r.returncode, 1, r.out)
            self.assertEqual(r.report["status"], "refused", r.out)
            self.assertIn(code, [x["code"] for x in r.report["refusals"]], r.out)
            self.assertEqual(tree_state(self.project), before, "a refused run changed the project")
        return r.report

    def test_a_modified_tracked_file_is_a_dirty_tree(self):
        (self.project / "README.md").write_text("changed\n", encoding="utf-8")
        self.commit("a readme")
        (self.project / "README.md").write_text("changed again\n", encoding="utf-8")
        self.refused("dirty-tree")

    def test_an_untracked_file_is_a_dirty_tree(self):
        (self.project / "scratch.txt").write_text("x\n", encoding="utf-8")
        report = self.refused("dirty-tree")
        dirty = next(x for x in report["refusals"] if x["code"] == "dirty-tree")
        self.assertIn("scratch.txt", " ".join(dirty["paths"]))

    def test_a_runner_at_the_root_and_under_methodology_is_half_migrated(self):
        (self.project / "methodology").mkdir()
        (self.project / "methodology" / "SESSION_RUNNER.md").write_text("# a second runner\n", encoding="utf-8")
        self.commit("a second runner")
        report = self.refused("half-migrated")
        half = next(x for x in report["refusals"] if x["code"] == "half-migrated")
        self.assertIn("SESSION_RUNNER.md", half["message"])
        self.assertIn("methodology/SESSION_RUNNER.md", half["message"])

    def test_a_destination_that_exists_is_refused_and_named(self):
        (self.project / "methodology").mkdir()
        (self.project / "methodology" / "SAFEGUARDS.md").write_text("# someone else's\n", encoding="utf-8")
        self.commit("a file where a move would land")
        report = self.refused("destination-exists")
        found = next(x for x in report["refusals"] if x["code"] == "destination-exists")
        self.assertEqual(found["paths"], ["methodology/SAFEGUARDS.md"])

    def test_a_locally_modified_tracked_file_is_not_current(self):
        (self.project / "SAFEGUARDS.md").write_text("# edited here\n", encoding="utf-8")
        self.commit("edit a synced file")
        report = self.refused("not-current")
        found = next(x for x in report["refusals"] if x["code"] == "not-current")
        self.assertIn("SAFEGUARDS.md", " ".join(found["paths"]))
        self.assertIn("bin/sync", found["message"])

    def test_a_missing_tracked_file_is_not_current(self):
        git(self.project, "rm", "-q", "RECOMMENDED_SKILLS.md")
        self.commit("remove a synced file")
        report = self.refused("not-current")
        found = next(x for x in report["refusals"] if x["code"] == "not-current")
        self.assertIn("RECOMMENDED_SKILLS.md", " ".join(found["paths"]))

    def test_a_project_in_ignore_mode_is_refused_as_unsupported(self):
        gi = self.project / ".gitignore"
        gi.write_text(gi.read_text(encoding="utf-8") + "/SESSION_RUNNER.md\n", encoding="utf-8")
        self.commit("ignore mode")
        self.refused("ignore-mode")

    def test_a_stale_format_seed_is_advice_and_not_a_refusal(self):
        """bin/status reports a seed that predates the current format as advisory only; the tool must not
        read that as drift."""
        (self.project / "HANDOFFS.md").write_text("# Handoffs\n\nAn old shape, no format marker.\n", encoding="utf-8")
        self.commit("an old-format seed")
        r = run_migrate(self.project)
        self.assertEqual(r.returncode, 0, r.out)
        self.assertEqual(r.report["status"], "ok")

    def test_a_clean_current_project_has_no_refusal(self):
        r = run_migrate(self.project)
        self.assertEqual(r.report["refusals"], [])
        self.assertEqual(r.report["status"], "ok")

    def test_every_refusal_is_reported_together_not_one_at_a_time(self):
        (self.project / "scratch.txt").write_text("x\n", encoding="utf-8")
        (self.project / "methodology").mkdir()
        (self.project / "methodology" / "SAFEGUARDS.md").write_text("# someone else's\n", encoding="utf-8")
        r = run_migrate(self.project)
        codes = [x["code"] for x in r.report["refusals"]]
        self.assertIn("dirty-tree", codes)
        self.assertIn("destination-exists", codes)


if __name__ == "__main__":
    unittest.main()
