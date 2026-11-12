"""The code that decides what a methodology config's path values become when a project moves to the new layout.

CANONICAL-ONLY, like bin/migrate-layout, which defined all of it until BL-131 phase P2: it is not in bin/_manifest.py, so
adopters do not receive it. It holds, MOVED WITHOUT EDITING out of bin/migrate-layout, the names the migration tool
rewrites a config with: NEW_DIR (the directory the new layout keeps the methodology files in), GENERATED (the files the
tools write beside them), CONFIG_FILES (the two configs whose path values are rewritten), Unsafe, token_pattern,
token_rewriter and rewrite_json (the byte-preserving rewrite and its structure check).

Why a module of its own: bin/sync is to seed the same two configs with the same rewrite (docs/planning/sync-seed-paths-plan.md,
section 3), and the two tools must not be able to disagree on a byte. bin/migrate-layout imports these names back under the
same names, so everything that reads them there still does.

Python 3 stdlib only.
"""
import json
import re

NEW_DIR = "methodology"
# What the tools write beside the methodology files (plan section 2.1, "Generated beside them"). They are not in
# the manifest, so the table is here; tools/layout_fixtures.GENERATED is the test suite's copy of it.
GENERATED = ("dashboard.html", "dashboard_history.jsonl", ".context-budget-history.jsonl",  # layout: ok -- the files the tools generate; this tool moves them
             ".quality-gates-results.json")  # layout: ok -- same
# The two configs whose path values the tool rewrites. BL-105 F29: they are read where the layout puts them.
CONFIG_FILES = (".context-budget.json", ".quality-gates.json")  # layout: ok -- the two seeds the tool edits the values of


class Unsafe(Exception):
    """A file the tool could not rewrite faithfully: the migration is refused rather than left half done."""


def token_pattern(names):
    """The regular expression for a methodology file's path where it stands alone: not behind a directory, a dot, a
    hyphen, a tilde or a word character (so `starter-kit/X`, a URL, `MY_X` and `NOTES-X` are not the project's file),
    and not before a word character or a dot and a word character (`X.mdx`, `X.bak`)."""
    names = sorted(names, key=len, reverse=True)
    return re.compile(r"(?<![\w./~-])(?:%s)(?!\w|\.\w)" % "|".join(re.escape(n) for n in names))


def token_rewriter(mapping):
    """A function (text) -> (text, replacements) that rewrites each standing-alone path of `mapping` to its value."""
    if not mapping:
        return lambda text: (text, 0)
    pattern = token_pattern(mapping)

    def rewrite(text):
        return pattern.subn(lambda m: mapping[m.group(0)], text)
    return rewrite


def rewrite_json(text, mapping):
    """A config's path-bearing values, rewritten in the text so every other byte is what it was: a value that is
    exactly a moved file's path, and the tokens of a gate's `command`. Prose (a key that starts with an underscore)
    and `canonical`, the path to the sibling checkout, are left. Returns (text, replacements); raises ValueError when
    the text is not JSON and Unsafe when the result is not the structure the rule predicts."""
    data = json.loads(text)
    tokens = token_rewriter(mapping)
    keys = set()

    def new_value(key, value):
        if key == "command":
            return tokens(value)[0]
        return mapping.get(value, value)

    def expected(o):
        if isinstance(o, dict):
            return {k: (o[k] if k.startswith("_") or k == "canonical"
                        else (new_value(k, o[k]) if isinstance(o[k], str) else expected(o[k]))) for k in o}
        if isinstance(o, list):
            return [expected(x) for x in o]
        return o

    def collect(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k.startswith("_") or k == "canonical":
                    continue
                if isinstance(v, str):
                    if new_value(k, v) != v:
                        keys.add(k)
                else:
                    collect(v)
        elif isinstance(o, list):
            for x in o:
                collect(x)
    collect(data)
    count = 0
    for key in sorted(keys):
        def sub(m, key=key):
            nonlocal count
            old = json.loads(m.group(2))
            new = new_value(key, old)
            if new == old:
                return m.group(0)
            count += 1
            return m.group(1) + json.dumps(new, ensure_ascii=False)
        text = re.sub(r'("%s"\s*:\s*)("(?:[^"\\]|\\.)*")' % re.escape(key), sub, text)
    if json.loads(text) != expected(data):
        raise Unsafe("the rewrite of this file does not give the structure the rule predicts (a path-bearing key inside a prose key?)")
    return text, count
