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

GITIGNORE = """# generated by the methodology tools: the page is anchored to the root, the results file is not;
# the two history files are tracked (nothing here ignores them), as five of the twelve real adopters keep them
/dashboard.html
.quality-gates-results.json
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
        git(project, "config", "user.name", "Adopter")
        git(project, "config", "user.email", "adopter@example.com")
        git(project, "config", "commit.gpgsign", "false")
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
        self.assertTrue(tracked["dashboard_history.jsonl"])
        self.assertTrue(tracked[".context-budget-history.jsonl"])
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


def name_status(project, rev="HEAD"):
    """{(src, dest): score} for the renames of one commit as git reports them (-M, so 50% and up are found)."""
    out = git(project, "diff", "-M", "--name-status", "-z", rev + "~1", rev).split("\0")
    renames, i = {}, 0
    while i < len(out):
        status = out[i]
        if status.startswith("R"):
            renames[(out[i + 1], out[i + 2])] = int(status[1:])
            i += 3
        else:
            i += 2 if status else 1
    return renames


def configs_rewritten_by_layer_3(path):
    return path in (".context-budget.json", ".quality-gates.json")


class TestApply(Adopter):
    """--apply writes the migration as ONE commit (plan 4.7.2): every tracked move a rename git can follow."""

    def apply(self, *args):
        before = git(self.project, "rev-parse", "HEAD").strip()
        r = run_migrate(self.project, "--apply", *args)
        return before, r

    def test_it_makes_exactly_one_commit_on_top_of_head_and_leaves_the_tree_clean(self):
        before, r = self.apply()
        self.assertEqual(r.returncode, 0, r.out)
        self.assertEqual(r.report["status"], "applied")
        self.assertEqual(git(self.project, "rev-list", "--count", before + "..HEAD").strip(), "1")
        self.assertEqual(git(self.project, "rev-parse", "HEAD~1").strip(), before)
        self.assertEqual(git(self.project, "status", "--porcelain"), "")
        self.assertEqual(r.report["commit"]["sha"], git(self.project, "rev-parse", "HEAD").strip())

    def test_every_planned_move_happened_and_a_file_that_is_not_rewritten_keeps_its_bytes(self):
        before = {rel: (self.project / rel).read_bytes() for rel in files_of(self.project)}
        plan = run_migrate(self.project).report
        moves = {m["src"]: m["dest"] for m in plan["moves"]}
        self.assertGreaterEqual(len(moves), 30)
        _, r = self.apply()
        self.assertEqual(r.returncode, 0, r.out)
        for src, dest in moves.items():
            self.assertFalse((self.project / src).exists(), "%s was left behind" % src)
            self.assertTrue((self.project / dest).is_file(), "%s did not arrive" % dest)
            if not configs_rewritten_by_layer_3(src):
                self.assertEqual((self.project / dest).read_bytes(), before[src], "%s changed in the move" % dest)

    def test_git_sees_each_tracked_move_as_a_rename_at_90_percent_or_better(self):
        plan = run_migrate(self.project).report
        tracked = {m["src"]: m["dest"] for m in plan["moves"] if m["tracked"]}
        _, r = self.apply()
        seen = name_status(self.project)
        for src, dest in tracked.items():
            self.assertIn((src, dest), seen, "git does not see %s -> %s as a rename" % (src, dest))
            self.assertGreaterEqual(seen[(src, dest)], 90, "%s -> %s fell below 90%%" % (src, dest))
        reported = {(x["src"], x["dest"]): x["score"] for x in r.report["commit"]["renames"]}
        self.assertEqual(reported, {(s, d): seen[(s, d)] for s, d in tracked.items()}, "the report and git disagree")

    def test_an_ignored_generated_file_is_moved_without_git_and_stays_ignored(self):
        _, r = self.apply()
        self.assertEqual(r.returncode, 0, r.out)
        for name in ("dashboard.html", ".quality-gates-results.json"):
            self.assertFalse((self.project / name).exists())
            self.assertTrue((self.project / "methodology" / name).is_file())
            self.assertNotIn("methodology/" + name, git(self.project, "ls-files").splitlines())
            ignored = subprocess.run(["git", "-C", str(self.project), "check-ignore", "-q", "methodology/" + name])
            self.assertEqual(ignored.returncode, 0, "methodology/%s is not ignored after the move" % name)

    def test_an_anchored_gitignore_entry_follows_its_file_and_an_unanchored_one_is_left(self):
        _, r = self.apply()
        text = (self.project / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("/methodology/dashboard.html\n", text)
        self.assertNotIn("\n/dashboard.html\n", text)
        self.assertIn("\n.quality-gates-results.json\n", text, "an unanchored entry still matches and must not change")
        self.assertIn("# generated by the methodology tools", text, "a comment was disturbed")
        rewrite = next(x for x in r.report["rewrites"] if x["path"] == ".gitignore")
        self.assertEqual(rewrite["replacements"], 1)

    def test_what_the_tool_leaves_stays_and_only_the_directories_it_emptied_go(self):
        _, r = self.apply()
        self.assertTrue((self.project / "docs" / "methodology" / "PROJECT_CONVENTIONS.md").is_file())
        self.assertTrue((self.project / "docs" / "archive" / "project-notes.md").is_file())
        self.assertFalse((self.project / "docs" / "methodology" / "workstreams").exists(), "an emptied directory was left")

    def test_a_directory_the_moves_emptied_entirely_is_removed(self):
        git(self.project, "rm", "-q", "-r", "docs/methodology/PROJECT_CONVENTIONS.md", "docs/archive/project-notes.md")
        self.commit("remove the project's own files")
        _, r = self.apply()
        self.assertEqual(r.returncode, 0, r.out)
        self.assertFalse((self.project / "docs" / "methodology").exists())
        self.assertFalse((self.project / "docs" / "archive").exists())

    def test_the_commit_message_names_the_tool_the_tier_and_carries_every_trailer(self):
        _, r = self.apply("--trailer", "Co-Authored-By: A Tester <a@example.com>", "--trailer", "Reviewed-by: B <b@example.com>")
        message = git(self.project, "log", "-1", "--format=%B")
        subject = message.splitlines()[0]
        self.assertIn("methodology/", subject)
        self.assertIn("bin/migrate-layout", message)
        self.assertIn("tier all", message)
        self.assertIn("a rename at 90% similarity or better", message)
        self.assertIn(r.report["canonical"]["sha"], message)
        self.assertTrue(message.rstrip().endswith("Reviewed-by: B <b@example.com>"), message)
        self.assertIn("Co-Authored-By: A Tester <a@example.com>", message)

    def test_bin_status_then_reads_every_tracked_file_current_at_its_new_place(self):
        _, r = self.apply()
        status = subprocess.run([sys.executable, "-B", str(STATUS), str(self.project)], capture_output=True, text=True)
        self.assertEqual(status.returncode, 0, status.stderr)
        self.assertRegex(status.stdout, r"layout: adopter\s+new")
        rows = [line for line in status.stdout.splitlines() if " tracked " in line]
        self.assertEqual(len(rows), len(TRACKED_DESTS))
        for line in rows:
            self.assertTrue(line.rstrip().endswith("current"), line)
            self.assertIn(" methodology/", " " + line)

    def test_a_second_run_finds_nothing_to_do_and_adds_no_commit(self):
        self.apply()
        head = git(self.project, "rev-parse", "HEAD").strip()
        r = run_migrate(self.project, "--apply")
        self.assertEqual(r.returncode, 0, r.out)
        self.assertEqual(r.report["status"], "nothing-to-do")
        self.assertEqual(git(self.project, "rev-parse", "HEAD").strip(), head)


class TestTheTiers(Adopter):
    """Plan 4.6: tier 1 is the framework's files, tier 2 the project's state; tier 1 alone is a stopping point."""

    def test_tier_1_moves_the_tracked_files_and_nothing_of_the_projects_state(self):
        r = run_migrate(self.project, "--apply", "--tier", "1")
        self.assertEqual(r.returncode, 0, r.out)
        for dest in TRACKED_DESTS:
            self.assertTrue((self.project / NEW_OF[dest]).is_file(), dest)
            self.assertFalse((self.project / dest).exists(), dest)
        for dest in SEED_DESTS:
            self.assertTrue((self.project / dest).is_file(), "%s moved in tier 1" % dest)
            self.assertFalse((self.project / NEW_OF[dest]).exists(), dest)
        for name in ("dashboard.html", "dashboard_history.jsonl"):
            self.assertTrue((self.project / name).is_file(), "%s moved in tier 1" % name)
        self.assertTrue((self.project / "docs" / "archive" / "CHANGELOG-through-2026-08-01.md").is_file())
        self.assertEqual(git(self.project, "status", "--porcelain"), "")

    def test_tier_2_alone_is_refused_before_tier_1(self):
        before = tree_state(self.project)
        r = run_migrate(self.project, "--apply", "--tier", "2")
        self.assertEqual(r.returncode, 1, r.out)
        self.assertEqual([x["code"] for x in r.report["refusals"]], ["tier-order"])
        self.assertEqual(tree_state(self.project), before)

    def test_tier_1_then_tier_2_reaches_the_same_tree_as_all_at_once(self):
        a = self.project
        b = Path(self._td.name) / "second"
        shutil.copytree(a, b, symlinks=True)
        self.assertEqual(run_migrate(a, "--apply", "--tier", "1").returncode, 0)
        r = run_migrate(a, "--apply", "--tier", "2")
        self.assertEqual(r.returncode, 0, r.out)
        self.assertEqual(run_migrate(b, "--apply").returncode, 0)
        self.assertEqual(files_of(a), files_of(b))
        for rel in sorted(files_of(a)):
            if not configs_rewritten_by_layer_3(Path(rel).name):
                self.assertEqual((a / rel).read_bytes(), (b / rel).read_bytes(), rel)

    def test_all_after_tier_1_moves_only_what_tier_1_left(self):
        run_migrate(self.project, "--apply", "--tier", "1")
        plan = run_migrate(self.project)
        self.assertEqual(plan.returncode, 0, plan.out)
        srcs = {m["src"] for m in plan.report["moves"]}
        self.assertTrue(srcs.isdisjoint(TRACKED_DESTS))
        self.assertTrue(set(SEED_DESTS) <= srcs)

    def test_a_second_tier_1_run_finds_nothing_to_do(self):
        run_migrate(self.project, "--apply", "--tier", "1")
        r = run_migrate(self.project, "--apply", "--tier", "1")
        self.assertEqual(r.report["status"], "nothing-to-do")


class TestTheGitattributesSeed(Adopter):
    """The seed moves; a .gitattributes that holds rules of the project's own stays where it is."""

    def test_the_seed_moves_with_the_rest(self):
        r = run_migrate(self.project, "--apply")
        self.assertTrue((self.project / "methodology" / ".gitattributes").is_file())
        self.assertFalse((self.project / ".gitattributes").exists())

    def test_a_file_with_a_rule_of_the_projects_own_stays_and_is_named(self):
        ga = self.project / ".gitattributes"
        ga.write_text(ga.read_text(encoding="utf-8") + "inst/extdata/example.txt text eol=lf\n", encoding="utf-8")
        self.commit("a rule of the project's own")
        r = run_migrate(self.project, "--apply")
        self.assertEqual(r.returncode, 0, r.out)
        self.assertTrue(ga.is_file(), "the project's own .gitattributes was moved")
        self.assertIn("inst/extdata/example.txt", ga.read_text(encoding="utf-8"))
        self.assertFalse((self.project / "methodology" / ".gitattributes").exists())
        self.assertIn(".gitattributes", [x["path"] for x in r.report["left_in_place"]])


class TestARefusedCommitRollsBack(Adopter):
    """A hook that refuses the migration commit must leave the project exactly as it was, files that git does not
    track included: the tool started from a clean tree and gives one back."""

    def test_a_refusing_hook_restores_the_tree_and_exits_3(self):
        hook = self.project / ".git" / "hooks" / "pre-commit"
        hook.write_text("#!/bin/sh\necho 'refused by the test hook' >&2\nexit 1\n", encoding="utf-8")
        hook.chmod(0o755)
        before = tree_state(self.project)
        r = run_migrate(self.project, "--apply")
        self.assertEqual(r.returncode, 3, r.out)
        self.assertEqual(r.report["status"], "rolled-back")
        self.assertIn("refused by the test hook", r.report["commit"]["error"])
        self.assertEqual(tree_state(self.project), before, "the rollback did not restore the project")
        self.assertFalse((self.project / "methodology").exists(), "an empty methodology/ was left behind")

    def test_the_hook_ran_because_the_tool_does_not_bypass_it(self):
        marker = self.project / "hook-ran"
        hook = self.project / ".git" / "hooks" / "pre-commit"
        hook.write_text("#!/bin/sh\ntouch '%s'\nexit 0\n" % marker, encoding="utf-8")
        hook.chmod(0o755)
        r = run_migrate(self.project, "--apply")
        self.assertEqual(r.returncode, 0, r.out)
        self.assertTrue(marker.exists(), "the pre-commit hook did not run: the tool bypassed it")


EXPECTED_CLAUDE_MD = """# Project

<!-- SESSION PROTOCOL -->
Read and follow `methodology/SESSION_RUNNER.md` step by step. Orient first: read methodology/SAFEGUARDS.md, then methodology/SESSION_NOTES.md,
then run `methodology/methodology_dashboard.py`.

This project follows `methodology/workstreams/DEVELOPMENT_WORKSTREAM.md` in standard mode, and the
theory is in [the manual](methodology/ITERATIVE_METHODOLOGY.md).

Kept qualified on purpose (a path with a directory in front is not a bare name):
the canonical copy is `../methodology/starter-kit/SESSION_RUNNER.md`, and upstream is
https://github.com/KJ5HST/methodology/blob/main/SESSION_RUNNER.md and `starter-kit/SAFEGUARDS.md`.

Not a methodology file: SESSION_RUNNER.mdx, MY_CHANGELOG.md, NOTES-CHANGELOG.md.
"""


class TestTheRewriteOfClaudeMd(Adopter):
    """CLAUDE.md is loaded from the project root, so a name in it is relative to the root: the paths of the files
    that moved are rewritten (plan C11, 4.4) and a name with a directory in front of it, or inside a longer name,
    is not a methodology file of the project's and is left."""

    def test_a_moved_path_or_bare_name_is_rewritten_and_nothing_else_changes(self):
        r = run_migrate(self.project, "--apply")
        self.assertEqual(r.returncode, 0, r.out)
        self.assertEqual((self.project / "CLAUDE.md").read_text(encoding="utf-8"), EXPECTED_CLAUDE_MD)

    def test_the_report_counts_the_replacements_and_shows_the_diff(self):
        r = run_migrate(self.project)
        rw = next(x for x in r.report["rewrites"] if x["path"] == "CLAUDE.md")
        self.assertEqual(rw["replacements"], 8)
        self.assertEqual(rw["final"], "CLAUDE.md")
        self.assertIn("-Read and follow `SESSION_RUNNER.md` step by step.", rw["diff"])
        self.assertIn("+Read and follow `methodology/SESSION_RUNNER.md` step by step.", rw["diff"])

    def test_a_dry_run_does_not_write_it(self):
        before = (self.project / "CLAUDE.md").read_text(encoding="utf-8")
        run_migrate(self.project)
        self.assertEqual((self.project / "CLAUDE.md").read_text(encoding="utf-8"), before)

    def test_tier_1_rewrites_only_the_names_of_the_files_it_moved(self):
        r = run_migrate(self.project, "--apply", "--tier", "1")
        text = (self.project / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("`methodology/SESSION_RUNNER.md`", text)
        self.assertIn("methodology/SAFEGUARDS.md", text)
        self.assertIn(", then SESSION_NOTES.md,", text, "a tier-2 file is still at the root and must keep its bare name")

    def test_a_project_without_a_claude_md_is_migrated_all_the_same(self):
        git(self.project, "rm", "-q", "CLAUDE.md")
        self.commit("no CLAUDE.md")
        r = run_migrate(self.project, "--apply")
        self.assertEqual(r.returncode, 0, r.out)
        self.assertNotIn("CLAUDE.md", [x["path"] for x in r.report["rewrites"]])


class TestTheRewriteOfTheConfigs(Adopter):
    """The two JSON configs move with the project's state and name paths in their values (plan C9): the path a file
    is read at, the results file, a gate's command. They are rewritten as text, so the rest of the file is the bytes
    it was; a prose key (one that starts with an underscore) and the `canonical` path (the sibling checkout, which
    does not move) are left."""

    def budget(self):
        return (self.project / ".context-budget.json").read_text(encoding="utf-8")

    def test_the_budget_paths_follow_and_the_canonical_path_and_the_prose_do_not(self):
        before = self.budget()
        for old in ('"path": "SESSION_NOTES.md"', '"path": "SESSION_RUNNER.md"', '"path": "SAFEGUARDS.md"',
                    '"canonical": "../methodology/starter-kit/SESSION_RUNNER.md"'):
            self.assertEqual(before.count(old), 1, "the seed no longer has %s once" % old)
        r = run_migrate(self.project, "--apply")
        self.assertEqual(r.returncode, 0, r.out)
        want = (before.replace('"path": "SESSION_NOTES.md"', '"path": "methodology/SESSION_NOTES.md"')
                .replace('"path": "SESSION_RUNNER.md"', '"path": "methodology/SESSION_RUNNER.md"')
                .replace('"path": "SAFEGUARDS.md"', '"path": "methodology/SAFEGUARDS.md"'))
        self.assertEqual((self.project / "methodology" / ".context-budget.json").read_text(encoding="utf-8"), want)

    def test_the_gates_results_file_and_command_follow_and_the_prose_does_not(self):
        before = (self.project / ".quality-gates.json").read_text(encoding="utf-8")
        r = run_migrate(self.project, "--apply")
        want = (before.replace('"results_file": ".quality-gates-results.json"',
                               '"results_file": "methodology/.quality-gates-results.json"')
                .replace("-- CHANGELOG.md)..HEAD", "-- methodology/CHANGELOG.md)..HEAD"))
        self.assertNotEqual(want, before)
        got = (self.project / "methodology" / ".quality-gates.json").read_text(encoding="utf-8")
        self.assertEqual(got, want)
        self.assertIn("Commits after the newest commit that touched CHANGELOG.md", got, "a prose value was rewritten")
        json.loads(got)

    def test_the_rewritten_gate_command_still_counts_from_the_ledgers_newest_commit(self):
        """Right after the move both the old and the new command read 0 (the move commit is the newest commit that
        touched either path), so the discriminating case is later: a commit that touches the moved ledger, then one
        that does not. Counted from the ledger's real place that is 1; counted from the old path it is 2."""
        run_migrate(self.project, "--apply")
        ledger = self.project / "methodology" / "CHANGELOG.md"
        ledger.write_text(ledger.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        self.commit("a commit that touches the ledger")
        (self.project / "README.md").write_text("a later commit\n", encoding="utf-8")
        self.commit("a commit that does not")
        gates = json.loads((self.project / "methodology" / ".quality-gates.json").read_text(encoding="utf-8"))
        out = subprocess.run(gates["gates"][0]["command"], shell=True, cwd=self.project, capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(out.stdout.strip(), "1", "the command did not count from the ledger's newest commit")

    def test_the_report_names_each_config_by_its_old_and_its_new_place(self):
        r = run_migrate(self.project)
        got = {x["path"]: x["final"] for x in r.report["rewrites"]}
        self.assertEqual(got[".context-budget.json"], "methodology/.context-budget.json")
        self.assertEqual(got[".quality-gates.json"], "methodology/.quality-gates.json")

    def test_a_fresh_clone_with_no_generated_files_still_gets_the_results_file_and_the_ignore_entry_moved(self):
        (self.project / "dashboard.html").unlink()
        (self.project / ".quality-gates-results.json").unlink()
        r = run_migrate(self.project, "--apply")
        self.assertEqual(r.returncode, 0, r.out)
        gates = json.loads((self.project / "methodology" / ".quality-gates.json").read_text(encoding="utf-8"))
        self.assertEqual(gates["results_file"], "methodology/.quality-gates-results.json")
        self.assertIn("/methodology/dashboard.html\n", (self.project / ".gitignore").read_text(encoding="utf-8"))

    def test_tier_1_leaves_the_configs_at_the_root_and_rewrites_only_the_paths_of_files_it_moved(self):
        r = run_migrate(self.project, "--apply", "--tier", "1")
        self.assertEqual(r.returncode, 0, r.out)
        text = self.budget()
        self.assertIn('"path": "methodology/SESSION_RUNNER.md"', text)
        self.assertIn('"path": "SESSION_NOTES.md"', text, "a tier-2 file is still at the root")
        gates = json.loads((self.project / ".quality-gates.json").read_text(encoding="utf-8"))
        self.assertEqual(gates["results_file"], ".quality-gates-results.json")
        self.assertIn("-- CHANGELOG.md)", gates["gates"][0]["command"])

    def test_a_config_that_is_not_json_is_moved_and_not_rewritten(self):
        (self.project / ".quality-gates.json").write_text("{ this is not json\n", encoding="utf-8")
        self.commit("a broken config")
        r = run_migrate(self.project, "--apply")
        self.assertEqual(r.returncode, 0, r.out)
        self.assertEqual((self.project / "methodology" / ".quality-gates.json").read_text(encoding="utf-8"), "{ this is not json\n")
        self.assertNotIn(".quality-gates.json", [x["path"] for x in r.report["rewrites"]])


def entry_split(text):
    """(entries, rest): the `### ` headings of a ledger in order."""
    return re.findall(r"^### (\d{4}-\d{2}-\d{2} · .*)$", text, flags=re.M)


class TestTheLedgerEntry(Adopter):
    """Plan 4.7.2: the migration commit carries ONE new ledger entry, and 4.7.3: it never rewrites a committed one."""

    def ledger(self, rel="methodology/CHANGELOG.md"):
        return (self.project / rel).read_text(encoding="utf-8")

    def test_one_entry_is_prepended_and_every_older_line_is_untouched(self):
        before = self.ledger("CHANGELOG.md")
        r = run_migrate(self.project, "--apply")
        self.assertEqual(r.returncode, 0, r.out)
        after = self.ledger()
        new = entry_split(after)
        old = entry_split(before)
        self.assertEqual(len(new), len(old) + 1)
        self.assertEqual(new[1:], old)
        self.assertRegex(new[0], r"^\d{4}-\d{2}-\d{2} · \[ad hoc\] Layout migration: ")
        diff = git(self.project, "diff", "-M", "HEAD~1", "HEAD", "--", "methodology/CHANGELOG.md", "CHANGELOG.md")
        removed = [l for l in diff.splitlines() if l.startswith("-") and not l.startswith("---")]
        self.assertEqual(removed, [], "the migration removed or rewrote a line of the ledger")

    def test_the_entry_sits_above_the_first_entry_and_the_ledger_still_passes_check_ledger(self):
        run_migrate(self.project, "--apply")
        after = self.ledger()
        first = after.index("### ")
        self.assertTrue(after[first:].startswith("### 20"), after[first:first + 40])
        self.assertIn("Layout migration", after[first:after.index("### 2026-09-")])
        check = subprocess.run([sys.executable, "-B", str(REPO / "bin" / "check-ledger"), "--file", "methodology/CHANGELOG.md"],
                               cwd=self.project, capture_output=True, text=True)
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

    def test_the_entry_says_what_moved_what_was_rewritten_and_by_which_tool(self):
        r = run_migrate(self.project, "--apply")
        text = r.report["ledger_entry"]["text"]
        self.assertIn("`bin/migrate-layout`", text)
        self.assertIn("tier all", text)
        self.assertIn("38 files", text)
        for path in ("CLAUDE.md", ".gitignore", "methodology/.context-budget.json", "methodology/.quality-gates.json"):
            self.assertIn("`%s`" % path, text)
        self.assertIn(text.strip(), self.ledger())

    def test_a_dry_run_shows_the_entry_and_writes_nothing(self):
        before = tree_state(self.project)
        r = run_migrate(self.project)
        self.assertEqual(r.report["ledger_entry"]["path"], "methodology/CHANGELOG.md")
        self.assertIn("Layout migration", r.report["ledger_entry"]["text"])
        self.assertEqual(tree_state(self.project), before)

    def test_a_ledger_that_does_not_move_in_tier_1_takes_the_entry_where_it_is(self):
        r = run_migrate(self.project, "--apply", "--tier", "1")
        self.assertEqual(r.returncode, 0, r.out)
        self.assertIn("Layout migration", self.ledger("CHANGELOG.md"))
        self.assertFalse((self.project / "methodology" / "CHANGELOG.md").exists())
        self.assertEqual(r.report["ledger_entry"]["path"], "CHANGELOG.md")

    def test_a_project_with_no_ledger_gets_no_entry_and_is_migrated_all_the_same(self):
        git(self.project, "rm", "-q", "CHANGELOG.md")
        self.commit("no ledger")
        r = run_migrate(self.project, "--apply")
        self.assertEqual(r.returncode, 0, r.out)
        self.assertIsNone(r.report["ledger_entry"])

    def test_the_entry_goes_under_a_heading_for_the_current_month_and_makes_one_when_the_month_has_turned(self):
        import datetime
        month = datetime.date.today().strftime("%Y-%m")
        base = self.ledger("CHANGELOG.md")
        first = base.index("### ")
        for heading, expect_new_heading in (("## %s\n\n" % month, False), ("## 2001-01\n\n", True)):
            project = Path(self._td.name) / ("m%d" % expect_new_heading)
            shutil.copytree(self.project, project, symlinks=True)
            (project / "CHANGELOG.md").write_text(base[:first] + heading + base[first:], encoding="utf-8")
            commit_all(project, "a month heading")
            self.assertEqual(run_migrate(project, "--apply").returncode, 0)
            after = (project / "methodology" / "CHANGELOG.md").read_text(encoding="utf-8")
            self.assertEqual(after.count("## %s\n" % month), 1, after[first - 50:first + 400])
            i_entry = after.index("Layout migration")
            self.assertGreater(i_entry, after.index("## %s\n" % month))
            if expect_new_heading:
                self.assertLess(after.index("## %s\n" % month), after.index("## 2001-01"))
                self.assertLess(i_entry, after.index("## 2001-01"))

    def test_a_ledger_too_small_to_take_an_entry_and_stay_a_rename_is_refused_and_rolled_back(self):
        seed = (REPO / "starter-kit" / "CHANGELOG.md").read_text(encoding="utf-8")
        (self.project / "CHANGELOG.md").write_text(seed, encoding="utf-8")
        self.commit("a ledger with no entries yet")
        before = tree_state(self.project)
        r = run_migrate(self.project, "--apply")
        self.assertEqual(r.returncode, 3, r.out)
        self.assertEqual(r.report["status"], "rolled-back")
        self.assertIn("90%", r.report["commit"]["error"])
        self.assertIn("CHANGELOG.md", r.report["commit"]["error"])
        self.assertEqual(tree_state(self.project), before)


if __name__ == "__main__":
    unittest.main()
