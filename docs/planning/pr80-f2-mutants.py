#!/usr/bin/env python3
"""Plant one PR #80 F2 mutant into BOTH methodology_dashboard.py twins of a scratch clone.

Fork-only evidence for docs/planning/pr80-review-response.md §4 (S164). It rewrites
tools/methodology_dashboard.py and starter-kit/methodology_dashboard.py, so run it only in a
throwaway clone. Every textual edit is asserted to match exactly once per file and the result must
still compile, so a mutant that silently fails to apply can never be scored as survived or killed.

    git clone -q --no-local -b pr80/f2-installed-source-guard <this repo> f2 && cd f2
    python3 <this file> . M1
    git checkout d4e1570 -- tools/test_methodology_dashboard.py
    python3 tools/test_methodology_dashboard.py     # the old test file: OK (211) under M1, M4, M6
    git checkout HEAD -- tools/test_methodology_dashboard.py
    python3 tools/test_methodology_dashboard.py     # the new test file: FAILED under all but M3
    git checkout -- tools/methodology_dashboard.py starter-kit/methodology_dashboard.py

Usage: pr80-f2-mutants.py <clone-root> <M1..M6>
"""
import sys
from pathlib import Path

TWINS = ("tools/methodology_dashboard.py", "starter-kit/methodology_dashboard.py")
NEUTRAL_RE = 're.compile(r"^__NEUTRALIZED_VERSION__\\s*=", re.MULTILINE)'
END = "\n    },\n"


def entry_bounds(text, name):
    table = text.index("_FRAMEWORK_FILE_SIGNATURES = {")
    key = f'    "{name}": {{\n'
    assert text.count(key, table) == 1, f"entry {name!r}: {text.count(key, table)} matches"
    i = text.index(key, table)
    return i, text.index(END, i) + len(END)


def neutralize(text, name):
    """The maintainer's F2 mutant, per name: version_re becomes a pattern the file cannot
    contain (left None where it already is), every signature a string it cannot contain."""
    i, j = entry_bounds(text, name)
    out, in_sigs, n_sig, n_ver = [], False, 0, 0
    for ln in text[i:j].split("\n"):
        indent = ln[: len(ln) - len(ln.lstrip())]
        s = ln.strip()
        if s.startswith('"version_re":'):
            n_ver += 1
            if s != '"version_re": None,':
                ln = f'{indent}"version_re": {NEUTRAL_RE},'
        elif s.startswith('"signatures": ('):
            in_sigs = True
        elif in_sigs and s == "),":
            in_sigs = False
        elif in_sigs and s.startswith('"'):
            n_sig += 1
            ln = f'{indent}"__NEUTRALIZED_SIGNATURE_{n_sig}__",'
        out.append(ln)
    assert n_ver == 1 and n_sig >= 2, (name, n_ver, n_sig)
    return text[:i] + "\n".join(out) + text[j:]


def replace_once(text, old, new):
    assert text.count(old) == 1, f"{text.count(old)} matches for {old!r}"
    return text.replace(old, new)


def drop_trim_name(text):
    """M5: the scanner forgets methodology_trim.py entirely — name and signature entry both,
    so the name-vs-signature completeness gate stays green."""
    text = replace_once(text, '("methodology_dashboard.py", "methodology_trim.py",',
                        '("methodology_dashboard.py",')
    i, j = entry_bounds(text, "methodology_trim.py")
    return text[:i] + text[j:]


def narrow_call_site(text):
    """M6: the predicate is untouched; the one call site in collect_all stops applying it to
    methodology_trim.py. Only an end-to-end assertion can see this."""
    old = '            if category == "source" and is_framework_installed(rel_path, fpath):\n'
    new = ('            if category == "source" and is_framework_installed(rel_path, fpath) '
           'and fname != "methodology_trim.py":\n')
    return replace_once(text, old, new)


MUTANTS = {
    "M1": lambda t: neutralize(t, "methodology_trim.py"),
    "M2": lambda t: neutralize(t, "context_budget.py"),
    "M3": lambda t: neutralize(t, "methodology_dashboard.py"),
    "M4": lambda t: neutralize(t, ".context-budget.json"),
    "M5": drop_trim_name,
    "M6": narrow_call_site,
}

if __name__ == "__main__":
    root, mid = Path(sys.argv[1]), sys.argv[2]
    for rel in TWINS:
        p = root / rel
        before = p.read_text(encoding="utf-8")
        after = MUTANTS[mid](before)
        assert after != before, f"{mid} changed nothing in {rel}"
        compile(after, rel, "exec")
        p.write_text(after, encoding="utf-8")
    print(f"{mid} planted in both twins")
