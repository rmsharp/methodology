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


def _load_script(name, path):
    import importlib.machinery
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
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


def run_migrate(project, *args, json_out=True, checks=False):
    """bin/migrate-layout as a command. With json_out the report is read as data into .report (None when the
    output is not JSON); .out is stdout and stderr joined. An --apply skips the before-and-after checks unless
    `checks` is asked for: they take seconds, and TestTheChecks is where they are asserted."""
    cmd = [sys.executable, "-B", str(MIGRATE), str(project)]
    if json_out:
        cmd.append("--json")
    if "--apply" in args and not checks and "--skip-checks" not in args:
        cmd.append("--skip-checks")
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
    entries = "".join("### 2026-09-%02d · [ad hoc] Entry %d\n\n%s%s\n\n" % (
        1 + i % 28, i, ("Body of entry %d. " % i) * 14,
        " See SESSION_RUNNER.md and [the guide](docs/methodology/HOW_TO_USE.md)." if i == 3 else "") for i in range(n))
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

def gates_text():
    """The seed .quality-gates.json (its prose and all, so it is the size a real adopter's is) with one gate declared,
    which is what an adopter that has started using the ratchet holds."""
    cfg = json.loads((REPO / "starter-kit" / "quality-gates.json").read_text(encoding="utf-8"))
    cfg["results_file"] = ".quality-gates-results.json"
    cfg["gates"] = [{
        "name": "ledger-lag", "direction": "max", "threshold": 3,
        "command": "git rev-list --count --no-merges \"$(git log -1 --format=%H -- CHANGELOG.md)..HEAD\"",
        "why": "Commits after the newest commit that touched CHANGELOG.md -- Phase 0's reconcile set.",
    }]
    return json.dumps(cfg, indent=2, ensure_ascii=False) + "\n"


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
    (p / ".quality-gates.json").write_text(gates_text(), encoding="utf-8")
    (p / "docs" / "methodology").mkdir(parents=True, exist_ok=True)
    (p / "docs" / "methodology" / "PROJECT_CONVENTIONS.md").write_text("# Conventions\n\nThis project's own.\n", encoding="utf-8")
    for name in ("dashboard_history.jsonl", ".context-budget-history.jsonl"):
        (p / name).write_text('{"timestamp": "2026-09-01T00:00:00"}\n', encoding="utf-8")
    # places that name a moved file and that the tool reports and does not edit (plan 4.7.1)
    (p / ".github" / "workflows").mkdir(parents=True)
    (p / ".github" / "workflows" / "ci.yml").write_text(
        "on:\n  push:\n    paths-ignore:\n      - 'CHANGELOG.md'\n      - 'SESSION_NOTES.md'\n      - 'docs/methodology/**'\njobs: {}\n", encoding="utf-8")
    (p / ".claude").mkdir()
    (p / ".claude" / "settings.json").write_text(
        '{"permissions": {"allow": ["Read(SESSION_RUNNER.md)", "Bash(python3 methodology_dashboard.py:*)"]}}\n', encoding="utf-8")
    (p / ".githooks").mkdir()
    (p / ".githooks" / "pre-commit").write_text(
        "#!/bin/sh\ngit ls-files --error-unmatch CHANGELOG.md >/dev/null 2>&1 || exit 0\n", encoding="utf-8")
    (p / "README.md").write_text("See docs/methodology/HOW_TO_USE.md for the method; the product log is CHANGELOG.md.\n", encoding="utf-8")
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


class TestThePureRules(unittest.TestCase):
    """The rules the tool applies, called as functions: a command costs seconds, a rule costs nothing, and these are
    the cases a whole-project test only reaches by accident."""

    @classmethod
    def setUpClass(cls):
        cls.m = _load_script("migrate_layout", MIGRATE)

    # --- .gitignore ---
    def test_a_gitignore_entry_follows_only_when_it_is_anchored_and_exactly_a_moved_path(self):
        mapping = {"dashboard.html": "methodology/dashboard.html", "docs/archive/CHANGELOG-through-2026-01-01.md":
                   "methodology/archive/CHANGELOG-through-2026-01-01.md"}
        text = ("# a comment naming /dashboard.html\n/dashboard.html\ndashboard.html\n!/dashboard.html\n"
                "/dashboard.html.bak\ndocs/archive/CHANGELOG-through-2026-01-01.md\n/other.html\n\n")
        got, n = self.m.rewrite_gitignore(text, mapping)
        self.assertEqual(got, ("# a comment naming /dashboard.html\n/methodology/dashboard.html\ndashboard.html\n"
                               "!/methodology/dashboard.html\n/dashboard.html.bak\n"
                               "/methodology/archive/CHANGELOG-through-2026-01-01.md\n/other.html\n\n"))
        self.assertEqual(n, 3)

    def test_a_gitignore_keeps_its_line_endings(self):
        got, n = self.m.rewrite_gitignore("a\r\n/dashboard.html\r\nb", {"dashboard.html": "methodology/dashboard.html"})
        self.assertEqual(got, "a\r\n/methodology/dashboard.html\r\nb")

    # --- the standing-alone rule ---
    def rewrite(self, text, mapping=None):
        mapping = mapping or {"SESSION_RUNNER.md": "methodology/SESSION_RUNNER.md"}
        return self.m.token_rewriter(mapping)(text)

    def test_a_name_is_rewritten_where_it_stands_alone(self):
        for text in ("SESSION_RUNNER.md", "`SESSION_RUNNER.md`", "(SESSION_RUNNER.md)", "read SESSION_RUNNER.md.", '"SESSION_RUNNER.md"',
                     "--file=SESSION_RUNNER.md", "SESSION_RUNNER.md:12", "[x](SESSION_RUNNER.md#top)", "SESSION_RUNNER.md, and"):
            got, n = self.rewrite(text)
            self.assertEqual(n, 1, text)
            self.assertEqual(got, text.replace("SESSION_RUNNER.md", "methodology/SESSION_RUNNER.md"), text)

    def test_a_name_inside_another_name_or_behind_a_directory_is_left(self):
        for text in ("SESSION_RUNNER.mdx", "SESSION_RUNNER.md.bak", "SESSION_RUNNER.md2", "/SESSION_RUNNER.md", "./SESSION_RUNNER.md",
                     "~/SESSION_RUNNER.md", "~SESSION_RUNNER.md", "a/SESSION_RUNNER.md", "MY_SESSION_RUNNER.md", "my-SESSION_RUNNER.md",
                     "xSESSION_RUNNER.md", ".SESSION_RUNNER.md", "https://example.org/SESSION_RUNNER.md"):
            self.assertEqual(self.rewrite(text), (text, 0), text)

    def test_the_longest_path_wins_and_each_occurrence_is_counted(self):
        mapping = {"docs/x/a.md": "m/a.md", "a.md": "m/a.md"}
        self.assertEqual(self.rewrite("docs/x/a.md and a.md and a.md", mapping), ("m/a.md and m/a.md and m/a.md", 3))

    def test_an_empty_map_changes_nothing(self):
        """An empty alternation matches the empty string between two non-word characters, so the text must have some."""
        for text in ("SESSION_RUNNER.md", "a  b , c", "", "(  )"):
            self.assertEqual(self.m.token_rewriter({})(text), (text, 0), repr(text))

    # --- a JSON config, rewritten as text ---
    MAP = {"SESSION_RUNNER.md": "methodology/SESSION_RUNNER.md", "CHANGELOG.md": "methodology/CHANGELOG.md",
           ".quality-gates-results.json": "methodology/.quality-gates-results.json"}

    def rj(self, text):
        return self.m.rewrite_json(text, self.MAP)

    def test_a_value_that_is_exactly_a_moved_path_follows_and_the_layout_of_the_file_is_kept(self):
        text = '{\n\t"files": [\n\t\t{"path": "SESSION_RUNNER.md", "n": 1},\n\t\t{ "path":"CHANGELOG.md" }\n\t],\n\t"results_file": ".quality-gates-results.json"\n}\n'
        got, n = self.rj(text)
        self.assertEqual(got, text.replace('"SESSION_RUNNER.md"', '"methodology/SESSION_RUNNER.md"')
                         .replace('"CHANGELOG.md"', '"methodology/CHANGELOG.md"')
                         .replace('".quality-gates-results.json"', '"methodology/.quality-gates-results.json"'))
        self.assertEqual(n, 3)

    def test_a_value_that_only_contains_a_moved_path_is_not_a_path(self):
        text = '{"path": "docs/SESSION_RUNNER.md", "note": "see SESSION_RUNNER.md", "name": "CHANGELOG.md.bak"}'
        self.assertEqual(self.rj(text), (text, 0))

    def test_canonical_and_every_underscore_key_are_left(self):
        text = '{"synced": [{"path": "SESSION_RUNNER.md", "canonical": "SESSION_RUNNER.md", "_": "SESSION_RUNNER.md"}], "_why": "CHANGELOG.md"}'
        got, n = self.rj(text)
        self.assertEqual(got, text.replace('"path": "SESSION_RUNNER.md"', '"path": "methodology/SESSION_RUNNER.md"'))
        self.assertEqual(n, 1)

    def test_a_path_bearing_key_inside_a_prose_subtree_makes_the_rewrite_unsafe(self):
        """The text rewrite cannot tell scope; the structure check can. The file is not half-edited: it is refused."""
        with self.assertRaises(self.m.Unsafe):
            self.rj('{"_example": {"path": "SESSION_RUNNER.md"}, "files": [{"path": "SESSION_RUNNER.md"}]}')

    def test_a_gate_command_is_rewritten_by_token_and_the_prose_beside_it_is_not(self):
        text = '{"gates": [{"command": "git log -- CHANGELOG.md && cat SESSION_RUNNER.md.bak", "why": "see CHANGELOG.md"}]}'
        got, n = self.rj(text)
        self.assertEqual(got, text.replace("-- CHANGELOG.md", "-- methodology/CHANGELOG.md"))
        self.assertEqual(n, 1)

    def test_non_ascii_text_survives_byte_for_byte(self):
        raw = '{"_": "a — dash é", "dash": "—", "path": "SESSION_RUNNER.md", "raw": "—"}'
        got, n = self.rj(raw)
        self.assertEqual(got, raw.replace('"SESSION_RUNNER.md"', '"methodology/SESSION_RUNNER.md"'))
        self.assertEqual(n, 1)

    def test_a_rewritten_command_keeps_its_non_ascii_characters_as_they_were_written(self):
        text = '{"gates": [{"command": "echo — CHANGELOG.md é"}]}'
        got, n = self.rj(text)
        self.assertEqual(got, '{"gates": [{"command": "echo — methodology/CHANGELOG.md é"}]}')
        self.assertEqual(n, 1)

    def test_text_that_is_not_json_is_a_value_error(self):
        with self.assertRaises(ValueError):
            self.rj("{ not json")

    def test_a_value_that_is_not_a_string_is_left(self):
        text = '{"path": 3, "files": [1, null, true], "results_file": null}'
        self.assertEqual(self.rj(text), (text, 0))

    # --- the ledger entry ---
    ENTRY = "### 2026-10-07 · [ad hoc] Layout migration: x\n\nbody\n"

    def test_an_entry_goes_under_the_current_months_heading(self):
        text = "front\n\n---\n\n## 2026-10\n\n### 2026-10-01 · [ad hoc] old\n\nold body\n"
        got = self.m.insert_entry(text, self.ENTRY, "2026-10")
        self.assertEqual(got, "front\n\n---\n\n## 2026-10\n\n" + self.ENTRY + "\n### 2026-10-01 · [ad hoc] old\n\nold body\n")

    def test_an_entry_gets_a_new_month_heading_above_an_older_months(self):
        text = "front\n\n## 2026-09\n\n### 2026-09-01 · [ad hoc] old\n\nold body\n"
        got = self.m.insert_entry(text, self.ENTRY, "2026-10")
        self.assertEqual(got, "front\n\n## 2026-10\n\n" + self.ENTRY + "\n## 2026-09\n\n### 2026-09-01 · [ad hoc] old\n\nold body\n")

    def test_an_entry_goes_above_the_first_entry_when_there_is_no_month_heading(self):
        text = "front\n\n### 2026-09-01 · [ad hoc] old\n\nold body\n"
        got = self.m.insert_entry(text, self.ENTRY, "2026-10")
        self.assertEqual(got, "front\n\n" + self.ENTRY + "\n### 2026-09-01 · [ad hoc] old\n\nold body\n")

    def test_an_entry_goes_at_the_end_of_a_ledger_with_no_entry_and_the_seed_sentinel_is_dropped(self):
        text = ("front\n\n<!-- METHODOLOGY-SEED-SENTINEL: fresh ledger.\n     more. -->\n\n---\n\n<!-- Entries go below. -->\n")
        got = self.m.insert_entry(text, self.ENTRY, "2026-10")
        self.assertNotIn("SENTINEL", got)
        self.assertTrue(got.endswith("<!-- Entries go below. -->\n\n" + self.ENTRY), got)

    def test_the_entry_text_names_the_tool_the_tier_the_count_and_what_was_edited(self):
        report = {"tier": "1", "canonical": {"sha": "abcdef0123456789", "modified": False}}
        text = self.m.ledger_entry_text(report, [{}] * 5, ["CLAUDE.md", ".gitignore"], "2026-10-07")
        self.assertTrue(text.startswith("### 2026-10-07 · [ad hoc] Layout migration: "))
        for piece in ("tier 1", "5 files", "abcdef0", "`CLAUDE.md`, `.gitignore`", "`bin/migrate-layout`"):
            self.assertIn(piece, text)
        self.assertNotIn("abcdef01", text)
        none = self.m.ledger_entry_text(report, [{}] * 5, [], "2026-10-07")
        self.assertIn("no file (none named a moved path)", none)

    # --- what a check difference is ---
    def sides(self, **over):
        side = {"status": {"exit": 0, "tracked": 23, "current": 23}, "ledger": {"exit": 0}, "handoff": {"exit": 1},
                "links": {"exit": 0, "framework": 0, "project": 0}, "proofs": {"count": 2, "histogram": {"0": 2}},
                "history": {"commits": 4}}
        before, after = dict(side), dict(side)
        after["history"] = {"commits": 5}
        for k, (b, a) in over.items():
            before[k], after[k] = b, a
        return before, after

    def test_nothing_that_must_hold_changing_is_no_difference(self):
        self.assertEqual(self.m.check_differences(*self.sides()), [])

    def test_each_rule_names_itself(self):
        s = lambda **kw: self.m.check_differences(*self.sides(**kw))
        self.assertEqual(s(status=({"exit": 0, "tracked": 23, "current": 23}, {"exit": 0, "tracked": 23, "current": 22})), ["status"])
        self.assertEqual(s(status=({"exit": 0, "tracked": 23, "current": 23}, {"exit": 1, "tracked": 0, "current": 0})), ["status"])
        self.assertEqual(s(ledger=({"exit": 0}, {"exit": 1})), ["ledger"])
        self.assertEqual(s(handoff=({"exit": 1}, {"exit": 0})), ["handoff"])
        self.assertEqual(s(proofs=({"count": 2, "histogram": {"0": 2}}, {"count": 2, "histogram": {"0": 1, "1": 1}})), ["proofs"])
        self.assertEqual(s(history=({"commits": 4}, {"commits": 4})), ["history"])

    def test_a_status_that_is_bad_on_both_sides_is_still_a_difference_because_the_rule_is_about_after(self):
        """bin/status must read every TRACKED file current AFTER the move, whatever it read before."""
        s = lambda **kw: self.m.check_differences(*self.sides(**kw))
        short = {"exit": 0, "tracked": 23, "current": 22}
        self.assertEqual(s(status=(short, short)), ["status"])
        failed = {"exit": 1, "tracked": 0, "current": 0}
        self.assertEqual(s(status=(failed, failed)), ["status"], "tracked == current == 0 but bin/status did not run")

    def test_a_project_without_a_ledger_has_no_history_to_lose(self):
        self.assertEqual(self.m.check_differences(*self.sides(history=({"commits": 0}, {"commits": 0}))), [])

    # --- the links cell: the framework's documents are judged, the project's own files are reported ---
    def cell(self, exit_code, framework, project):
        return {"exit": exit_code, "framework": framework, "project": project}

    def test_a_framework_link_that_newly_dangles_is_a_difference_and_the_rule_is_about_the_count(self):
        s = lambda **kw: self.m.check_differences(*self.sides(**kw))
        self.assertEqual(s(links=(self.cell(0, 0, 0), self.cell(1, 2, 0))), ["links"])
        self.assertEqual(s(links=(self.cell(1, 2, 0), self.cell(1, 3, 0))), ["links"], "one more is a change")
        self.assertEqual(s(links=(self.cell(1, 2, 0), self.cell(1, 2, 0))), [], "a count that did not change is not one")
        self.assertEqual(s(links=(self.cell(1, 3, 0), self.cell(1, 2, 0))), ["links"], "nor is one fewer: like the other checks, the rule is that it did not change")

    def test_links_in_the_projects_own_files_are_reported_and_never_a_difference(self):
        """A committed ledger entry is never edited, so a link in one that was right where the ledger sat is not the move's defect."""
        s = lambda **kw: self.m.check_differences(*self.sides(**kw))
        self.assertEqual(s(links=(self.cell(0, 0, 0), self.cell(1, 0, 6))), [])

    def test_a_links_check_that_could_not_be_read_after_the_move_is_a_difference_never_a_zero(self):
        s = lambda **kw: self.m.check_differences(*self.sides(**kw))
        self.assertEqual(s(links=(self.cell(0, 0, 0), self.cell(2, None, None))), ["links"])
        self.assertEqual(s(links=(self.cell(0, 0, 0), self.cell("timeout", None, None))), ["links"])

    def test_the_cell_counts_the_dangling_links_by_whether_the_file_they_sit_in_is_the_frameworks(self):
        legacy, new = TRACKED_DESTS[0], NEW_OF[TRACKED_DESTS[0]]
        owned = NEW_OF[SEED_DESTS[0]]
        text = ("check-links: FAIL — 3 dangling link(s) in the tree at /x (new layout):\n"
                "  %s:12  ->  gone.md\n  %s:7  ->  docs/methodology/HOW_TO_USE.md\n  %s:3  ->  also-gone.md\n\n"
                "Distributed files author cross-references for the ADOPTER layout (B1 plan section 4). Fix the target above, not the layout.\n"
                % (new, owned, legacy))
        got = self.m.links_cell(1, text)
        self.assertEqual((got["exit"], got["framework"], got["project"]), (1, 2, 1), "either layout's name for a framework file counts")
        ok = self.m.links_cell(0, "check-links: OK — 80 relative link(s) across 23 distributed markdown files resolve in the tree at /x.\n")
        self.assertEqual((ok["exit"], ok["framework"], ok["project"]), (0, 0, 0))

    def test_a_framework_document_missing_from_the_tree_counts_as_a_framework_failure(self):
        """check-links reports a distributed file it cannot find as line 0 with a placeholder target; that is a framework document too."""
        text = ("check-links: FAIL — 1 dangling link(s) in the tree at /x (new layout):\n"
                "  %s:0  ->  <distributed file missing from tree>\n" % NEW_OF[TRACKED_DESTS[0]])
        got = self.m.links_cell(1, text)
        self.assertEqual((got["framework"], got["project"]), (1, 0))

    def test_a_failure_whose_lines_cannot_be_read_is_unknown_and_a_run_that_could_not_decide_has_no_counts(self):
        """An exit 1 with no line in the known shape would otherwise read as zero dangling: a green made of a format change."""
        shaped = "  %s:3  ->  x.md\n" % NEW_OF[TRACKED_DESTS[0]]  # a line in the known shape, from a run that did not decide
        for code, text in ((1, "check-links: FAIL — the output changed shape\n"), (2, "usage: check-links\n"), (2, shaped), ("timeout", shaped)):
            got = self.m.links_cell(code, text)
            self.assertEqual((got["framework"], got["project"]), (None, None), (code, text))

    # --- which files are a ledger, a CI file and the rest ---
    def test_a_path_is_sorted_into_its_category(self):
        want = {".github/workflows/ci.yml": "ci", ".circleci/config.yml": "ci", ".gitlab-ci.yml": "ci", "Jenkinsfile": "ci",
                ".claude/settings.json": "harness", ".githooks/pre-commit": "hooks", "CHANGELOG.md": "ledger",
                "methodology/HANDOFFS.md": "ledger", "SESSION_NOTES.md": "ledger",
                "docs/archive/CHANGELOG-through-2026-01-01.md": "ledger", "methodology/archive/HANDOFFS-through-2026-01-01-2.md": "ledger",
                "docs/archive/notes.md": "other", "README.md": "other", "src/CHANGELOG.md": "other", "ROADMAP.md": "other"}
        for path, cat in want.items():
            self.assertEqual(self.m.hit_category(path), cat, path)

    def test_only_the_files_the_trimmer_writes_are_shards(self):
        yes = ("CHANGELOG-through-2026-08-01.md", "HANDOFFS-through-2026-08-02-3.md.verify.sh", "SESSION_NOTES-through-x.md")
        no = ("CHANGELOG-archive.md", "CHANGELOG-through-x.md.bak", "ROADMAP-through-x.md", "a/CHANGELOG-through-x.md", "CHANGELOG-through-.txt")
        for name in yes:
            self.assertTrue(self.m.SHARD_RE.match(name), name)
        for name in no:
            self.assertFalse(self.m.SHARD_RE.match(name), name)

    # --- the gitattributes rule ---
    def test_a_gitattributes_that_holds_only_the_seeds_rules_is_the_seeds(self):
        seed = "# comment\nCHANGELOG.md merge=union\n*.jsonl merge=union\n"
        self.assertTrue(self.m.seed_rules_only("CHANGELOG.md merge=union\n\n# another comment\n", seed))
        self.assertTrue(self.m.seed_rules_only(seed, seed))
        self.assertTrue(self.m.seed_rules_only("", seed))
        self.assertFalse(self.m.seed_rules_only(seed + "*.png binary\n", seed))

    # --- ignore mode ---
    def test_ignore_mode_is_a_gitignore_that_lists_a_tracked_destination_in_either_layout(self):
        with tempfile.TemporaryDirectory() as d:
            gi = Path(d) / ".gitignore"
            self.assertFalse(self.m.is_ignore_mode(d))
            for text, want in (("/SESSION_RUNNER.md\n", True), ("/methodology/SESSION_RUNNER.md\n", True),
                               ("/docs/methodology/ITERATIVE_METHODOLOGY.md\n", True), ("SESSION_RUNNER.md\n", False),
                               ("/CHANGELOG.md\n", False), ("/dashboard.html\n", False), ("# /SESSION_RUNNER.md\n", False)):
                gi.write_text(text, encoding="utf-8")
                self.assertEqual(self.m.is_ignore_mode(d), want, text)

    # --- what the plan moves ---
    def plan(self, files, tier="all", kind="legacy"):
        with tempfile.TemporaryDirectory() as d:
            for rel in files:
                path = Path(d) / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("x\n", encoding="utf-8")
            return self.m.plan_moves(d, tier, set(files), kind)

    def test_a_session_notes_shard_moves_and_a_nested_or_lookalike_file_does_not(self):
        files = ["docs/archive/SESSION_NOTES-through-2026-08-01.md", "docs/archive/SESSION_NOTES-through-2026-08-01.md.verify.sh",
                 "docs/archive/sub/CHANGELOG-through-2026-08-01.md", "docs/archive/CHANGELOG-archive.md"]
        moves, left, collisions = self.plan(files)
        self.assertEqual({m["src"]: m["dest"] for m in moves},
                         {"docs/archive/SESSION_NOTES-through-2026-08-01.md": "methodology/archive/SESSION_NOTES-through-2026-08-01.md",
                          "docs/archive/SESSION_NOTES-through-2026-08-01.md.verify.sh": "methodology/archive/SESSION_NOTES-through-2026-08-01.md.verify.sh"})
        self.assertEqual({x["path"] for x in left}, {"docs/archive/sub/CHANGELOG-through-2026-08-01.md", "docs/archive/CHANGELOG-archive.md"})
        self.assertEqual(collisions, [])

    def test_a_generated_file_and_a_shard_that_already_exist_at_their_destination_are_collisions(self):
        files = ["dashboard.html", "methodology/dashboard.html", "docs/archive/CHANGELOG-through-2026-08-01.md",
                 "methodology/archive/CHANGELOG-through-2026-08-01.md", "SESSION_NOTES.md", "methodology/SESSION_NOTES.md"]
        moves, left, collisions = self.plan(files)
        self.assertEqual(collisions, ["methodology/SESSION_NOTES.md", "methodology/archive/CHANGELOG-through-2026-08-01.md",
                                      "methodology/dashboard.html"])
        self.assertEqual(moves, [])

    def test_tier_1_plans_only_the_tracked_rows_and_tier_2_only_the_rest(self):
        files = ["SESSION_RUNNER.md", "CHANGELOG.md", "dashboard.html", "docs/archive/CHANGELOG-through-2026-08-01.md"]
        self.assertEqual([m["src"] for m in self.plan(files, "1")[0]], ["SESSION_RUNNER.md"])
        self.assertEqual(sorted(m["src"] for m in self.plan(files, "2")[0]),
                         sorted(["CHANGELOG.md", "dashboard.html", "docs/archive/CHANGELOG-through-2026-08-01.md"]))

    # --- directories a move empties ---
    def test_only_the_directories_a_move_emptied_are_removed_and_never_the_root(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "a" / "b").mkdir(parents=True)
            (root / "a" / "keep.txt").write_text("x", encoding="utf-8")
            (root / "c" / "d" / "e").mkdir(parents=True)
            self.m.remove_empty_parents(root, "a/b/gone.md")
            self.assertFalse((root / "a" / "b").exists())
            self.assertTrue((root / "a").is_dir(), "a directory that still holds a file was removed")
            self.m.remove_empty_parents(root, "c/d/e/gone.md")
            self.assertFalse((root / "c").exists())
            self.assertTrue(root.is_dir())

    # --- what git calls dirty ---
    def test_the_cleanup_never_removes_the_project_root_even_when_it_empties_it(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "project"
            (root / "c" / "d").mkdir(parents=True)
            self.m.remove_empty_parents(root, "c/d/gone.md")
            self.assertFalse((root / "c").exists())
            self.assertTrue(root.is_dir(), "the project root was removed")

    def test_a_staged_rename_is_one_dirty_path_and_not_two(self):
        with tempfile.TemporaryDirectory() as d:
            git(d, "init", "-q")
            (Path(d) / "a.txt").write_text("hello world\n" * 20, encoding="utf-8")
            commit_all(d, "a")
            git(d, "mv", "a.txt", "b.txt")
            (Path(d) / "new.txt").write_text("n\n", encoding="utf-8")
            self.assertEqual(sorted(self.m.dirty_paths(d)), ["b.txt", "new.txt"])


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

    def test_a_subdirectory_of_a_repository_is_not_the_top_of_one(self):
        outer = self.root / "outer"
        (outer / "inner").mkdir(parents=True)
        git(outer, "init", "-q")
        (outer / "inner" / "SESSION_RUNNER.md").write_text("# runner\n", encoding="utf-8")
        commit_all(outer, "a repository with a project inside it")
        r = run_migrate(outer / "inner")
        self.assertEqual(r.returncode, 1, r.out)
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
        self.assertEqual(report["layout"], "half-migrated")
        self.assertEqual([x["code"] for x in report["refusals"]], ["half-migrated"],
                         "the runner's collision is the half-migrated refusal and is not listed a second time")
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
    """The files whose bytes a migration changes on purpose: the two configs, and the ledger that takes its entry."""
    return Path(path).name in (".context-budget.json", ".quality-gates.json", "CHANGELOG.md")


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
        moves = r.report["moves"]
        plain = sum(1 for m in moves if not m["tracked"])
        self.assertEqual(plain, 2)
        self.assertIn("%d file(s) with git mv, %d without git" % (len(moves) - plain, plain), message)
        self.assertIn(r.report["canonical"]["sha"], message)
        self.assertTrue(message.rstrip().endswith("Reviewed-by: B <b@example.com>"), message)
        self.assertIn("Co-Authored-By: A Tester <a@example.com>", message)
        parsed = git(self.project, "log", "-1", "--format=%(trailers:only,unfold)")
        self.assertIn("Co-Authored-By: A Tester <a@example.com>", parsed, "git does not read the trailers as trailers")
        self.assertIn("Reviewed-by: B <b@example.com>", parsed)

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

    def test_tier_1_names_what_it_leaves_of_the_framework_directory_and_not_the_archive_it_does_not_touch(self):
        r = run_migrate(self.project, "--tier", "1")
        left = [x["path"] for x in r.report["left_in_place"]]
        self.assertIn("docs/methodology/PROJECT_CONVENTIONS.md", left)
        self.assertNotIn("docs/archive/project-notes.md", left, "the archive is tier 2's: a tier-1 run has no opinion about it")
        both = [x["path"] for x in run_migrate(self.project).report["left_in_place"]]
        self.assertIn("docs/archive/project-notes.md", both)

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
        self.assertEqual((a / "methodology" / "CHANGELOG.md").read_text(encoding="utf-8").count("Layout migration"), 2,
                         "each run of the tool owes the ledger one entry")
        self.assertEqual((b / "methodology" / "CHANGELOG.md").read_text(encoding="utf-8").count("Layout migration"), 1)
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
        self.assertEqual(rw["replacements"], 6)
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
        self.assertIn("below 90% similarity", r.report["commit"]["error"])
        self.assertIn("CHANGELOG.md", r.report["commit"]["error"])
        self.assertEqual(tree_state(self.project), before)


class TestTheHitsItWillNotRewrite(Adopter):
    """Plan 4.7.1: the tool lists every hit it will not rewrite and why: CI workflows, `.claude/` rules, `.githooks/`
    copies, ledger links (a committed ledger entry is never edited, C6) and anything else that names a moved file."""

    PLACES = {"ci": ".github/workflows/ci.yml", "harness": ".claude/settings.json", "hooks": ".githooks/pre-commit",
              "other": "README.md"}

    def test_each_category_counts_its_mentions_and_names_the_files_and_lines(self):
        nr = run_migrate(self.project).report["not_rewritten"]
        self.assertEqual({k: (v["mentions"], v["files"]) for k, v in nr.items() if k != "ledger"},
                         {"ci": (3, 1), "harness": (2, 1), "hooks": (1, 1), "other": (2, 1)})
        self.assertEqual([(s["file"], s["line"]) for s in nr["ci"]["sites"]],
                         [(".github/workflows/ci.yml", 4), (".github/workflows/ci.yml", 5), (".github/workflows/ci.yml", 6)])
        self.assertEqual(nr["ci"]["sites"][2]["names"], ["docs/methodology/"], "a CI filter on the directory is a hit")
        self.assertEqual([(s["file"], s["line"]) for s in nr["hooks"]["sites"]], [(".githooks/pre-commit", 2)])
        site = nr["harness"]["sites"][0]
        self.assertEqual((site["file"], site["line"]), (".claude/settings.json", 1))
        self.assertEqual(sorted(site["names"]), ["SESSION_RUNNER.md", "methodology_dashboard.py"])
        self.assertIn("Read(SESSION_RUNNER.md)", site["text"])

    def test_a_binary_file_that_contains_a_moved_name_is_not_a_hit(self):
        (self.project / "data.bin").write_bytes(b"\x00\x01\x02 CHANGELOG.md \x00\xff")
        self.commit("a binary file")
        other = run_migrate(self.project).report["not_rewritten"]["other"]
        self.assertEqual((other["mentions"], other["files"]), (2, 1), "only README.md names a moved file")
        self.assertNotIn("data.bin", [s["file"] for s in other["sites"]])

    def test_sites_are_capped_per_category_and_the_count_is_not(self):
        (self.project / "README.md").write_text("see CHANGELOG.md\n" * 30, encoding="utf-8")
        self.commit("a readme that names the ledger thirty times")
        other = run_migrate(self.project).report["not_rewritten"]["other"]
        self.assertEqual((other["mentions"], other["files"], len(other["sites"])), (30, 1, 25))

    def test_the_ledger_links_are_counted_and_not_listed(self):
        nr = run_migrate(self.project).report["not_rewritten"]
        self.assertGreaterEqual(nr["ledger"]["mentions"], 2)
        self.assertGreaterEqual(nr["ledger"]["files"], 1)
        self.assertEqual(nr["ledger"]["sites"], [], "a ledger's links are counted, never listed one by one")

    def test_none_of_them_is_edited_by_an_apply(self):
        before = {rel: (self.project / rel).read_bytes() for rel in self.PLACES.values()}
        r = run_migrate(self.project, "--apply")
        self.assertEqual(r.returncode, 0, r.out)
        for rel, data in before.items():
            self.assertEqual((self.project / rel).read_bytes(), data, "%s was edited" % rel)
        self.assertEqual(r.report["not_rewritten"]["ci"]["mentions"], 3)

    def test_a_moved_file_a_rewritten_file_and_a_qualified_name_are_not_hits(self):
        nr = run_migrate(self.project).report["not_rewritten"]
        self.assertEqual(sorted(nr), ["ci", "harness", "hooks", "ledger", "other"], "nothing was scanned")
        listed = {s["file"] for cat in nr.values() for s in cat["sites"]}
        self.assertIn(".github/workflows/ci.yml", listed, "the scan found nothing, so the absences below prove nothing")
        self.assertNotIn("SAFEGUARDS.md", listed, "a moved framework document is not scanned")
        self.assertNotIn("CLAUDE.md", listed, "a file the tool rewrites is not a hit")
        self.assertNotIn(".gitignore", listed)

    def test_no_hits_still_prints_every_category(self):
        for rel in self.PLACES.values():
            git(self.project, "rm", "-q", rel)
        self.commit("remove the places that name a moved file")
        nr = run_migrate(self.project).report["not_rewritten"]
        self.assertEqual(sorted(nr), ["ci", "harness", "hooks", "ledger", "other"])
        for name in ("ci", "harness", "hooks", "other"):
            self.assertEqual((nr[name]["mentions"], nr[name]["files"], nr[name]["sites"]), (0, 0, []), name)

    def test_the_text_a_person_reads_lists_them(self):
        r = run_migrate(self.project, json_out=False)
        self.assertRegex(r.out, r"(?m)^not rewritten")
        self.assertIn(".github/workflows/ci.yml:4", r.out)
        self.assertRegex(r.out, r"(?m)^\s+ledger:\s+\d+ mention")


class TestTheChecks(Adopter):
    """Plan 4.7.4: an apply verifies itself, before and after, with the read-only checks: bin/status, the two ledger
    checkers, check-links, every shard's proof (the exit histogram must not change) and the ledger's history across the
    move. A difference does not undo a commit that is made; it is reported, with the way back, and the exit is 4."""

    NAMES = ["handoff", "history", "ledger", "links", "proofs", "status"]

    def with_real_shard(self):
        """Trim the fixture's ledger with the project's own trimmer, so one shard has a real proof beside it."""
        r = subprocess.run([sys.executable, "-B", "methodology_trim.py", "--file", "CHANGELOG.md", "--cut", "25",
                            "--force", "--write"], cwd=self.project, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.commit("trim the ledger")

    def test_an_apply_runs_every_check_before_and_after_with_no_cell_left_blank(self):
        r = run_migrate(self.project, "--apply", checks=True)
        self.assertEqual(r.returncode, 0, r.out)
        checks = r.report["checks"]
        self.assertTrue(checks["ran"])
        for side in ("before", "after"):
            self.assertEqual(sorted(checks[side]), self.NAMES)
            for name in self.NAMES:
                self.assertTrue(checks[side][name], "%s %s is blank" % (side, name))
        self.assertEqual(checks["before"]["status"], {"exit": 0, "tracked": len(TRACKED_DESTS), "current": len(TRACKED_DESTS)})
        self.assertEqual(checks["after"]["status"], {"exit": 0, "tracked": len(TRACKED_DESTS), "current": len(TRACKED_DESTS)})
        self.assertTrue(checks["clean"])
        self.assertTrue(checks["ok"])
        self.assertEqual(checks["differences"], [])

    def test_the_proofs_of_the_moved_shards_give_the_same_histogram_and_the_real_one_still_holds(self):
        self.with_real_shard()
        r = run_migrate(self.project, "--apply", checks=True)
        self.assertEqual(r.returncode, 0, r.out)
        checks = r.report["checks"]
        self.assertEqual(checks["before"]["proofs"], {"count": 3, "histogram": {"0": 3}})
        self.assertEqual(checks["after"]["proofs"], {"count": 3, "histogram": {"0": 3}})
        proof = self.project / "methodology" / "archive" / "CHANGELOG-through-2026-09-28.md.verify.sh"
        again = subprocess.run(["bash", str(proof)], cwd=self.project, capture_output=True, text=True)
        self.assertEqual(again.returncode, 0, again.stdout + again.stderr)

    def test_a_proof_that_stops_holding_is_reported_exits_4_and_names_the_way_back(self):
        """The shard rehearsal catches a proof that reads its shard by the old path, so the proof here is one a rehearsal
        cannot predict: it depends on the newest commit's subject, which the rehearsal's commit does not share with the
        migration's. Whatever the cause, a check that differs after a commit is made is reported, not undone."""
        proof = self.project / "docs" / "archive" / "CHANGELOG-through-2026-08-01.md.verify.sh"
        proof.write_text("#!/bin/sh\ngit log -1 --format=%s | grep -q '^chore(methodology)' && exit 1\nexit 0\n", encoding="utf-8")
        self.commit("a proof that depends on the newest commit")
        r = run_migrate(self.project, "--apply", checks=True)
        self.assertEqual(r.returncode, 4, r.out)
        self.assertEqual(r.report["status"], "applied")
        self.assertEqual(r.report["rehearsal"]["excluded"], [], "the rehearsal could not have seen this")
        self.assertEqual(git(self.project, "status", "--porcelain"), "", "the commit was made and must stand")
        checks = r.report["checks"]
        self.assertFalse(checks["ok"])
        self.assertEqual(checks["differences"], ["proofs"])
        self.assertEqual(checks["before"]["proofs"]["histogram"], {"0": 2})
        self.assertEqual(checks["after"]["proofs"]["histogram"], {"0": 1, "1": 1})
        self.assertIn("git revert " + r.report["commit"]["sha"][:12], r.report["checks"]["way_back"])

    def test_a_tree_the_commit_leaves_dirty_is_reported_and_exits_4(self):
        """A post-commit hook that writes a file: the commit stands, and the tree is not clean. Nothing else differs."""
        hook = self.project / ".git" / "hooks" / "post-commit"
        hook.write_text("#!/bin/sh\ntouch stray.txt\n", encoding="utf-8")
        hook.chmod(0o755)
        r = run_migrate(self.project, "--apply", checks=True)
        self.assertEqual(r.returncode, 4, r.out)
        checks = r.report["checks"]
        self.assertFalse(checks["clean"])
        self.assertFalse(checks["ok"])
        self.assertEqual(checks["differences"], [], "only the tree differs")
        self.assertEqual(r.report["status"], "applied")

    def test_the_text_says_so_when_the_tree_is_not_clean(self):
        hook = self.project / ".git" / "hooks" / "post-commit"
        hook.write_text("#!/bin/sh\ntouch stray.txt\n", encoding="utf-8")
        hook.chmod(0o755)
        r = run_migrate(self.project, "--apply", json_out=False, checks=True)
        self.assertEqual(r.returncode, 4, r.out)
        self.assertIn("clean tree: NO", r.out)
        self.assertIn("CHECKS DIFFER (tree not clean)", r.out)

    def test_the_ledgers_history_is_reached_across_the_move(self):
        r = run_migrate(self.project, "--apply", checks=True)
        h = r.report["checks"]
        self.assertGreaterEqual(h["after"]["history"]["commits"], h["before"]["history"]["commits"] + 1)
        followed = git(self.project, "log", "--follow", "--format=%h", "--", "methodology/CHANGELOG.md").split()
        self.assertEqual(len(followed), h["after"]["history"]["commits"])
        self.assertIn(git(self.project, "rev-parse", "--short=7", "HEAD~1").strip(), [c[:7] for c in followed])

    def test_a_link_in_the_projects_own_ledger_that_the_move_leaves_dangling_is_reported_and_not_a_failure(self):
        """The fixture's ledger holds a committed entry that links docs/methodology/HOW_TO_USE.md, right where the ledger
        sat. The move leaves the entry alone (a committed entry is never edited), so the link dangles: the project's own
        file, counted beside the framework's, and no difference."""
        r = run_migrate(self.project, "--apply", checks=True)
        self.assertEqual(r.returncode, 0, r.out)
        checks = r.report["checks"]
        self.assertNotIn("informational", checks, "no check is exempt any more: P9 rewrote the documents")
        self.assertEqual((checks["before"]["links"]["exit"], checks["before"]["links"]["framework"], checks["before"]["links"]["project"]), (0, 0, 0))
        self.assertEqual((checks["after"]["links"]["exit"], checks["after"]["links"]["framework"], checks["after"]["links"]["project"]), (1, 0, 1))
        self.assertEqual(checks["differences"], [])

    def test_a_framework_document_that_dangles_after_the_move_is_a_difference_exits_4_and_the_commit_stands(self):
        """The after-checks run on the working tree, so a post-commit hook that writes a legacy-style link into a framework
        document stands in for a document authored for the old layout: the link resolved before, and does not now."""
        how = NEW_OF["docs/methodology/HOW_TO_USE.md"]
        hook = self.project / ".git" / "hooks" / "post-commit"
        hook.write_text("#!/bin/sh\nprintf '\\n[x](docs/methodology/ITERATIVE_METHODOLOGY.md)\\n' >> %s\n" % how, encoding="utf-8")
        hook.chmod(0o755)
        r = run_migrate(self.project, "--apply", checks=True)
        self.assertEqual(r.returncode, 4, r.out)
        self.assertEqual(r.report["status"], "applied")
        checks = r.report["checks"]
        self.assertIn("links", checks["differences"])
        self.assertEqual((checks["after"]["links"]["framework"], checks["after"]["links"]["project"]), (1, 1))
        self.assertIn("git revert " + r.report["commit"]["sha"][:12], checks["way_back"])

    def test_the_text_says_which_links_are_judged_and_which_only_reported(self):
        r = run_migrate(self.project, "--apply", json_out=False, checks=True)
        self.assertEqual(r.returncode, 0, r.out)
        self.assertRegex(r.out, r"(?m)^\s+links:\s+exit 0; 0 framework, 0 project dangling -> exit 1; 0 framework, 1 project dangling")
        self.assertNotIn("informational until P9", r.out)
        self.assertIn("framework documents are judged", r.out)

    def test_skip_checks_runs_none_and_says_so(self):
        r = run_migrate(self.project, "--apply", "--skip-checks")
        self.assertEqual(r.returncode, 0, r.out)
        self.assertEqual(r.report["checks"], {"ran": False})

    def test_a_dry_run_runs_no_check(self):
        r = run_migrate(self.project)
        self.assertIsNone(r.report["checks"])

    def test_the_text_a_person_reads_lists_each_check_before_and_after(self):
        r = run_migrate(self.project, "--apply", json_out=False, checks=True)
        self.assertEqual(r.returncode, 0, r.out)
        self.assertRegex(r.out, r"(?m)^checks \(before -> after\):")
        for name in self.NAMES:
            self.assertRegex(r.out, r"(?m)^\s+%s:" % name)


WORKING_TREE_PROOF = """#!/bin/sh
# an older-format proof: it reads its shard by the path it was written at, in the working tree
cd "$(git rev-parse --show-toplevel)" || exit 3
test -f docs/archive/HANDOFFS-through-2026-08-02.md || { echo "FAIL: docs/archive/HANDOFFS-through-2026-08-02.md not found" >&2; exit 2; }
"""


class TestTheShardRehearsal(Adopter):
    """Real data (vscode_quarto_ext): an older-format proof reads its shard by its working-tree path, so it exits 2 once
    the shard moves, while the trimmer's current proofs read git history and survive. The tool rehearses the shard moves
    in a throwaway clone, before the plan is shown, and leaves a shard whose proof would regress where it is."""

    def old_format_proof(self):
        (self.project / "docs" / "archive" / "HANDOFFS-through-2026-08-02.md.verify.sh").write_text(WORKING_TREE_PROOF, encoding="utf-8")
        self.commit("an older-format proof")

    def test_a_shard_whose_proof_would_regress_stays_with_its_proof_and_the_plan_says_why(self):
        self.old_format_proof()
        r = run_migrate(self.project)
        got = self.moves(r.report)
        self.assertNotIn("docs/archive/HANDOFFS-through-2026-08-02.md", got)
        self.assertNotIn("docs/archive/HANDOFFS-through-2026-08-02.md.verify.sh", got)
        self.assertIn("docs/archive/CHANGELOG-through-2026-08-01.md", got, "a shard whose proof holds must still move")
        left = {x["path"]: x["reason"] for x in r.report["left_in_place"]}
        for path in ("docs/archive/HANDOFFS-through-2026-08-02.md", "docs/archive/HANDOFFS-through-2026-08-02.md.verify.sh"):
            self.assertIn("proof", left[path])
            self.assertIn("exits 2", left[path])
        self.assertEqual(r.report["rehearsal"]["excluded"], ["docs/archive/HANDOFFS-through-2026-08-02.md"])

    def test_the_apply_leaves_them_where_they_are_and_the_proofs_histogram_is_unchanged(self):
        self.old_format_proof()
        r = run_migrate(self.project, "--apply", checks=True)
        self.assertEqual(r.returncode, 0, r.out)
        self.assertTrue((self.project / "docs" / "archive" / "HANDOFFS-through-2026-08-02.md").is_file())
        self.assertTrue((self.project / "docs" / "archive" / "HANDOFFS-through-2026-08-02.md.verify.sh").is_file())
        self.assertTrue((self.project / "methodology" / "archive" / "CHANGELOG-through-2026-08-01.md").is_file())
        proofs = r.report["checks"]
        self.assertEqual(proofs["before"]["proofs"]["histogram"], {"0": 1})
        self.assertEqual(proofs["before"]["proofs"], proofs["after"]["proofs"])
        again = subprocess.run(["bash", "docs/archive/HANDOFFS-through-2026-08-02.md.verify.sh"], cwd=self.project, capture_output=True, text=True)
        self.assertEqual(again.returncode, 0, again.stdout + again.stderr)

    def test_a_proof_that_failed_before_and_fails_the_same_way_after_still_moves(self):
        (self.project / "docs" / "archive" / "HANDOFFS-through-2026-08-02.md.verify.sh").write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
        self.commit("a proof that always fails")
        r = run_migrate(self.project)
        self.assertIn("docs/archive/HANDOFFS-through-2026-08-02.md.verify.sh", self.moves(r.report))
        self.assertEqual(r.report["rehearsal"]["excluded"], [])

    def test_the_rehearsal_leaves_no_trace_in_the_project_or_in_the_temporary_directory(self):
        self.old_format_proof()
        before = tree_state(self.project)
        tmp = Path(tempfile.gettempdir())
        clones_before = {p.name for p in tmp.glob("migrate-rehearsal-*")}
        run_migrate(self.project)
        self.assertEqual(tree_state(self.project), before)
        self.assertEqual({p.name for p in tmp.glob("migrate-rehearsal-*")}, clones_before)

    def test_a_project_with_no_proofs_is_not_rehearsed(self):
        for name in ("CHANGELOG-through-2026-08-01.md.verify.sh", "HANDOFFS-through-2026-08-02.md.verify.sh"):
            git(self.project, "rm", "-q", "docs/archive/" + name)
        self.commit("no proofs")
        r = run_migrate(self.project)
        self.assertEqual(r.report["rehearsal"], {"ran": False, "proofs": 0, "excluded": []})

    def test_the_rehearsal_says_how_many_proofs_it_ran(self):
        r = run_migrate(self.project)
        self.assertEqual(r.report["rehearsal"], {"ran": True, "proofs": 2, "excluded": []})


class TestWhatTheHitsSayAboutHooksAndDirectories(Adopter):
    """Real data: wsfct's pre-commit hook runs context_budget.py from the root, so it refuses the migration commit; and a
    CLAUDE.md that says `docs/methodology/` as a directory still says it after the paths in it are rewritten."""

    def test_a_hook_that_runs_a_moved_tool_is_flagged_and_one_that_only_names_a_file_is_not(self):
        (self.project / ".githooks" / "pre-push").write_text("#!/bin/sh\npython3 context_budget.py --status || exit 1\n", encoding="utf-8")
        self.commit("a hook that runs a methodology tool")
        r = run_migrate(self.project)
        sites = {s["file"]: s for s in r.report["not_rewritten"]["hooks"]["sites"]}
        self.assertTrue(sites[".githooks/pre-push"]["runs_tool"])
        self.assertFalse(sites[".githooks/pre-commit"]["runs_tool"])
        self.assertEqual(r.report["not_rewritten"]["hooks"]["runs_moved_tool"], 1)
        text = run_migrate(self.project, json_out=False).out
        self.assertIn("refuse the migration commit", text)

    def test_a_hook_in_the_hooks_directory_that_git_does_not_track_is_found_and_flagged(self):
        """Real data (wsfct): context_budget.py install-hook writes .git/hooks/pre-commit, which is per clone and not
        tracked, and which runs $top/context_budget.py: the scan of tracked files could not see the hook that refused."""
        hook = self.project / ".git" / "hooks" / "pre-commit"
        hook.write_text('#!/bin/sh\n# installed by context_budget.py\nexec python3 "$(git rev-parse --show-toplevel)/context_budget.py" --precommit\n', encoding="utf-8")
        hook.chmod(0o755)
        (self.project / ".git" / "hooks" / "commit-msg.sample").write_text("#!/bin/sh\n# CHANGELOG.md in a sample\n", encoding="utf-8")
        before = tree_state(self.project)
        r = run_migrate(self.project)
        self.assertEqual(tree_state(self.project), before)
        sites = [s for s in r.report["not_rewritten"]["hooks"]["sites"] if s["file"] == ".git/hooks/pre-commit"]
        self.assertEqual([(s["line"], s["runs_tool"], s["untracked"]) for s in sites], [(2, False, True), (3, True, True)],
                         "line 2 is a comment naming the tool, and a comment runs nothing; line 3 execs it")
        self.assertEqual(r.report["not_rewritten"]["hooks"]["runs_moved_tool"], 1)
        self.assertFalse([s for s in r.report["not_rewritten"]["hooks"]["sites"] if "sample" in s["file"]], "a .sample hook is not a hook")
        text = run_migrate(self.project, json_out=False).out
        self.assertIn("not tracked", text)
        self.assertIn("refuse the migration commit", text)

    def test_a_hook_directory_the_project_tracks_is_not_counted_twice(self):
        git(self.project, "config", "core.hooksPath", ".githooks")
        r = run_migrate(self.project)
        sites = [s for s in r.report["not_rewritten"]["hooks"]["sites"] if s["file"] == ".githooks/pre-commit"]
        self.assertEqual(len(sites), 1)
        self.assertEqual(r.report["not_rewritten"]["hooks"]["mentions"], 1)

    def test_a_hook_that_runs_a_moved_tool_refuses_the_commit_and_the_tool_rolls_back_and_says_so(self):
        hook = self.project / ".githooks" / "pre-commit"
        hook.write_text("#!/bin/sh\npython3 context_budget.py --status || exit 1\n", encoding="utf-8")
        hook.chmod(0o755)
        git(self.project, "add", "-A")
        git(self.project, "commit", "-q", "--no-verify", "-m", "a hook that runs a methodology tool")
        git(self.project, "config", "core.hooksPath", ".githooks")
        before = tree_state(self.project)
        r = run_migrate(self.project, "--apply")
        self.assertEqual(r.returncode, 3, r.out)
        self.assertEqual(r.report["status"], "rolled-back")
        self.assertIn("context_budget.py", r.report["commit"]["error"])
        self.assertEqual(tree_state(self.project), before)

    def test_a_directory_named_in_a_rewritten_file_is_reported_after_its_paths_are_rewritten(self):
        claude = self.project / "CLAUDE.md"
        claude.write_text(claude.read_text(encoding="utf-8") + "\nThe 13 files under `docs/methodology/` and the shards in docs/archive are the framework's.\n",
                          encoding="utf-8")
        self.commit("a directory mentioned in prose")
        r = run_migrate(self.project)
        sites = [s for s in r.report["not_rewritten"]["other"]["sites"] if s["file"] == "CLAUDE.md"]
        self.assertEqual(len(sites), 1)
        self.assertEqual(sites[0]["names"], ["docs/archive", "docs/methodology/"])
        self.assertIn("The 13 files under", sites[0]["text"])
        rewritten = next(x for x in r.report["rewrites"] if x["path"] == "CLAUDE.md")
        self.assertIn("+Read and follow `methodology/SESSION_RUNNER.md`", rewritten["diff"])

    def test_a_directory_mentioned_in_a_file_the_tool_does_not_edit_is_reported_and_a_full_path_is_not_counted_twice(self):
        (self.project / "README.md").write_text("Methodology lives in docs/methodology/ now.\nSee docs/methodology/HOW_TO_USE.md.\n", encoding="utf-8")
        self.commit("a readme")
        other = run_migrate(self.project).report["not_rewritten"]["other"]
        by_line = {s["line"]: s for s in other["sites"] if s["file"] == "README.md"}
        self.assertEqual(by_line[1]["names"], ["docs/methodology/"])
        self.assertEqual(by_line[2]["names"], ["docs/methodology/HOW_TO_USE.md"])


class TestALedgerSoSmallThatGitSeesNoRenameAtAll(Adopter):
    """Below 50% similarity git reports a delete and an add: the guard must say that, not only "below 90%"."""

    def test_the_rollback_says_it_is_not_a_rename_and_why(self):
        (self.project / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")
        self.commit("a ledger of one line")
        before = tree_state(self.project)
        r = run_migrate(self.project, "--apply")
        self.assertEqual(r.returncode, 3, r.out)
        error = r.report["commit"]["error"]
        self.assertIn("CHANGELOG.md -> methodology/CHANGELOG.md (not a rename: the ledger is too small", error)
        self.assertIn("it holds 12 bytes", error)
        self.assertEqual(tree_state(self.project), before)


class TestASmallLedgerIsRefusedWithAReason(Adopter):
    """Real data (claude_work): a ledger that is only the seed cannot take its entry and stay a rename at 90%."""

    def test_the_rollback_says_the_ledger_is_too_small_and_how_big_it_is(self):
        seed = (REPO / "starter-kit" / "CHANGELOG.md").read_text(encoding="utf-8")
        (self.project / "CHANGELOG.md").write_text(seed, encoding="utf-8")
        self.commit("a ledger with no entries yet")
        r = run_migrate(self.project, "--apply")
        self.assertEqual(r.returncode, 3, r.out)
        error = r.report["commit"]["error"]
        self.assertIn("too small to take its entry", error)
        self.assertIn("%d bytes" % len(seed.encode("utf-8")), error)


if __name__ == "__main__":
    unittest.main()
