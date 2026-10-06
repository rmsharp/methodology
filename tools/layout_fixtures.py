#!/usr/bin/env python3
"""Fixture trees in both layouts, for every phase of the methodology/ move to reuse (BL-101, P1).

CANONICAL-ONLY, like tools/layout_resolver.py and for the same reason: it is not in bin/_manifest.py.
The plan is docs/planning/methodology-subdirectory-plan.md: section 4.1 is the target layout, section
4.6 the two tiers. ``build_tree`` writes one of five shapes into an empty directory:

    legacy  what ``bin/sync`` writes into a project today: the manifest's destinations, as they are
    new     section 4.1: every methodology file one level down in methodology/
    tier1   the framework's own files (the manifest's TRACKED rows) moved, the project's state files
            (its SEED rows, the generated files, the archive) still at the root: section 4.6's
            "coherent end state", and the shape that needs a second anchor to resolve (layout_resolver)
    half    legacy plus a second runner under methodology/: the state the resolver must refuse
    empty   no files: a project that has not adopted the methodology

The tree is derived from bin/_manifest.py, so a file the manifest gains appears in the legacy shape
by itself. The new shape is derived from it by ``new_path``, and tools/test_layout_resolver.py holds
section 4.1 typed out as literals, so that change cannot also quietly reshape the target. Phase P6
makes the new destinations a second literal table inside the manifest (so ``--source=github`` can read
them as data); this module then reads that table and ``new_path`` goes away.

A tree here is files only. A phase that needs a git repository, hooks or a real ledger builds them on
top, passing ``contents`` for the files it cares about.
"""
import importlib.util
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # building a fixture must not generate bin/__pycache__

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
LAYOUTS = ("legacy", "new", "tier1", "half", "empty")
# What the tools write beside the methodology files (plan section 2.1, "Generated beside them").
GENERATED = ("dashboard.html", "dashboard_history.jsonl", ".context-budget-history.jsonl",
             ".quality-gates-results.json")
ARCHIVE_SHARD = "CHANGELOG-through-2000-01-01.md"  # a placeholder shard: the archive's location is the point


def _manifest():
    spec = importlib.util.spec_from_file_location("_manifest", REPO / "bin" / "_manifest.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def new_path(dest):
    """Where a manifest destination lands in the new layout: flat under methodology/, with
    workstreams/ the one subdirectory (plan decision D2). ``docs/methodology/`` is dropped."""
    prefix = "docs/methodology/"
    return "methodology/" + (dest[len(prefix):] if dest.startswith(prefix) else dest)


def _stub(name):
    if name.endswith(".json"):
        return "{}\n"
    if name.endswith(".jsonl"):
        return ""
    if name.endswith(".py"):
        return "# layout fixture\n"
    if name.endswith(".html"):
        return "<!-- layout fixture -->\n"
    return "# %s\n\nlayout fixture\n" % name


def build_tree(root, layout, *, contents=None, generated=True, archive=False):
    """Write the ``layout`` shape into the empty directory ``root`` and return the sorted relative
    paths (POSIX strings). ``contents`` maps a file NAME ("CHANGELOG.md") to the text to write, in
    whichever place that file lands; every other file gets a small stub. ``generated`` adds the four
    tool-output files, ``archive`` a placeholder ledger shard in the archive directory."""
    if layout not in LAYOUTS:
        raise ValueError("unknown layout %r; one of %s" % (layout, ", ".join(LAYOUTS)))
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    if any(root.iterdir()):
        raise ValueError("%s is not empty; a fixture tree is built into a fresh directory" % root)
    m = _manifest()
    files = []  # (relative path, file name)
    if layout != "empty":
        for _, dest, disposition in m.DISTRIBUTION:
            moved = layout == "new" or (layout == "tier1" and disposition == m.TRACKED)
            files.append((new_path(dest) if moved else dest, Path(dest).name))
        if generated:
            files += [(("methodology/" + g) if layout == "new" else g, g) for g in GENERATED]
        if archive:
            files.append((("methodology/archive/" if layout == "new" else "docs/archive/") + ARCHIVE_SHARD,
                          ARCHIVE_SHARD))
        if layout == "half":
            files.append(("methodology/SESSION_RUNNER.md", "SESSION_RUNNER.md"))
    contents = contents or {}
    for rel, name in files:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents.get(name, _stub(name)), encoding="utf-8")
    return sorted(rel for rel, _ in files)
