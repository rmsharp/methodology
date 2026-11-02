#!/usr/bin/env python3
"""plan-evidence.py -- the grep-based inventory behind docs/planning/issue100-fixes-plan.md.

READ-ONLY. Reads git objects (`git show`, `git diff`); writes nothing in the repository; standard
library only. Run from the repository root:

    python3 -I docs/planning/issue100-plan-evidence/plan-evidence.py

What it answers, for the plan's five edit targets and its own phases:

  [site-*]    WHERE each edit would land: for every site, the line span of its region at six refs.
              A region is found by a start pattern (and an end pattern or a fixed line count); the
              plan's "files to change" list comes from this output and not from memory.
  [overlap-*] WHICH open pull request changes lines inside, or next to, that region on upstream's
              `main`. Git conflicts when two changes touch the same or ADJACENT lines, so a hunk within
              one line of the region counts. "yes" means a textual conflict is possible and the
              sequencing section of the plan applies; "no" is NOT a promise of a clean merge (the
              implementing phase proves that with `git merge-tree`).
  [size-*]    how many bytes the runner is at each ref (the file every session reads in full).
  [mode-*]    the 0600 file-mode loss, reproduced with upstream's own `atomic_write`.

Refs (resolved and printed on the first lines, so a moved branch is visible in the output):
  V42   tag v4.2        the release the issue cites
  MAIN  upstream/main   the base for anything sent upstream
  FORK  HEAD            this fork's committed tree
  PR99  origin/feat/methodology-directory           (pull request #99)
  PR98  origin/feat/trim-session-notes-ledger-issue93   (pull request #98)
  PR96  origin/feat/close-out-report-tool           (pull request #96)

Exit 0 always: it prints tables for a human to read; it is not a gate.
"""
import importlib.util
import os
import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

REFS = {
    "V42": "v4.2",
    "MAIN": "upstream/main",
    "FORK": "HEAD",
    "PR99": "origin/feat/methodology-directory",
    "PR98": "origin/feat/trim-session-notes-ledger-issue93",
    "PR96": "origin/feat/close-out-report-tool",
}
PRS = ("PR99", "PR98", "PR96")
ANSI = re.compile("\x1b\\[[0-9;]*m")

# id, file, start pattern, end pattern (first later line that matches ends the region, exclusive) or None,
# and nlines (region length when there is no end pattern).
SITES = [
    ("f1-status-main", "bin/status", r"^def main\(\) -> int:", r"^def report\(", 1),
    ("f1-budget-synced", "starter-kit/context_budget.py", r"^def check_synced\(", r"^def _behind\(", 1),
    ("f2-runner-step5", "starter-kit/SESSION_RUNNER.md", r"^5\. Run: `python3 methodology_dashboard\.py`", None, 1),
    ("f2-runner-3f", "starter-kit/SESSION_RUNNER.md", r"^### 3F: Commit", r"^### 3G:", 1),
    ("f2-runner-degradation", "starter-kit/SESSION_RUNNER.md", r"^\| A file Phase 0 mandates reading is larger", None, 1),
    ("f2-bootstrap-step10", "starter-kit/BOOTSTRAP.md", r"^## Step 10: Set Up Git Hooks", r"^## (?!Step 10)", 1),
    ("f3-template-comment", "starter-kit/CLAUDE_TEMPLATE.md", r"^<!-- This table is loaded every session", r"-->\s*$", 1),
    ("f3-bootstrap-step5", "starter-kit/BOOTSTRAP.md", r"^\*\*Keep CLAUDE\.md lean", r"^## Step 6", 1),
    ("f3-bootstrap-table", "starter-kit/BOOTSTRAP.md", r"^\| `CLAUDE\.md` → Adaptations → Learnings", None, 1),
    ("f3-seed-name", "starter-kit/context-budget.json", r'"path": "LEARNINGS\.md"', None, 1),
    ("f3-runner-3c", "starter-kit/SESSION_RUNNER.md", r"^- \*\*Adopter project\*\*", None, 1),
    ("f4-seed-footer", "starter-kit/SESSION_NOTES.md", r"^\*Session history accumulates below this line", None, 1),
    ("f4-runner-3d", "starter-kit/SESSION_RUNNER.md", r"^Update `SESSION_NOTES\.md`\. \*\*You will be judged", None, 1),
    ("f5-runner-3g-stop", "starter-kit/SESSION_RUNNER.md", r"^\*\*Then STOP\. The session is over\.\*\*", None, 1),
    ("f5-safeguards-hook", "starter-kit/SAFEGUARDS.md", r"^### Close-Out Completeness Hook", r"^### Disclosure Hook", 1),
    ("f6-trim-p1", "starter-kit/methodology_trim.py", r"^def check_P1\(", r"^def check_P1a\(", 1),
    ("f6-sync-ignore", "bin/sync", r"^def ensure_gitignore_entries\(", r"^def (?!ensure_gitignore_entries)", 1),
    ("f6-status-seed", "bin/status", r"^def seed_status\(", r"^def render_table\(", 1),
    ("s1-trim-atomic", "starter-kit/methodology_trim.py", r"^def atomic_write\(", r"^# =====", 1),
]


def git(*args):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    return r.returncode, r.stdout


def blob(ref, path):
    rc, out = git("show", f"{ref}:{path}")
    return out.splitlines() if rc == 0 else None


def find_region(lines, start, end, nlines):
    """(first, last) 1-based line numbers of the region, or None when `start` is not in the file."""
    if lines is None:
        return None
    for i, ln in enumerate(lines):
        if re.search(start, ln):
            if end is None:
                return i + 1, i + nlines
            inclusive = end == r"-->\s*$"  # a comment's closing line belongs to it; a section heading does not
            for j in range(i + 1, len(lines)):
                if re.search(end, lines[j]):
                    return i + 1, (j + 1 if inclusive else j)
            return i + 1, len(lines)
    return None


def hunks_on_main_side(ref, path):
    """[(first, last)] line spans a pull request's changes occupy on upstream/main's side of the file."""
    rc, out = git("diff", "-U0", f"{REFS['MAIN']}...{ref}", "--", path)
    spans = []
    for m in re.finditer(r"^@@ -(\d+)(?:,(\d+))? \+", out, re.M):
        a = int(m.group(1))
        n = 1 if m.group(2) is None else int(m.group(2))
        # a pure insertion (n == 0) sits BETWEEN line a and a+1; treat it as touching both
        spans.append((a, a + max(n, 1) - 1) if n else (a, a + 1))
    return spans


def touches(region, spans, margin=1):
    a, b = region
    return [(x, y) for x, y in spans if x <= b + margin and y >= a - margin]


def count_in(ref, path, rx):
    lines = blob(ref, path)
    return None if lines is None else sum(1 for ln in lines if re.search(rx, ln))


def extras():
    """Population-of-zero claims and two behaviours the pieces depend on."""
    print("\n# none: claims of the shape 'nothing does X' (a count over a file that exists; None = file absent)")
    for k in ("V42", "MAIN", "FORK"):
        print(f"[none-remote-calls-{k}] ls-remote in bin/status: {count_in(REFS[k], 'bin/status', r'ls-remote')}; "
              f"in context_budget.py: {count_in(REFS[k], 'starter-kit/context_budget.py', r'ls-remote')}")
    for k in ("V42", "MAIN", "FORK"):
        print(f"[none-runner-{k}] 'context_budget' in the runner: {count_in(REFS[k], 'starter-kit/SESSION_RUNNER.md', r'context_budget')}; "
              f"'bin/status' in the runner: {count_in(REFS[k], 'starter-kit/SESSION_RUNNER.md', r'bin/status')}; "
              f"'bin/status' in SAFEGUARDS.md: {count_in(REFS[k], 'starter-kit/SAFEGUARDS.md', r'bin/status')}")
    for k in ("V42", "MAIN", "FORK"):
        n = count_in(REFS[k], "bin/sync", r"deliberately excluded from both")
        print(f"[sync-seeds-not-ignored-{k}] bin/sync says seeds are deliberately excluded from ignore mode: {'HOLDS' if n else 'ABSENT'}")

    print("\n# comments: the HTML comments in the CLAUDE.md template (Claude Code strips block-level ones from CLAUDE.md)")
    lines = blob(REFS["MAIN"], "starter-kit/CLAUDE_TEMPLATE.md") or []
    text = "\n".join(lines)
    found = list(re.finditer(r"<!--(.*?)-->", text, re.S))
    print(f"[comments-claude-template-MAIN] {len(found)} comments")
    for i, m in enumerate(found, 1):
        line = text[: m.start()].count("\n") + 1
        print(f"[comment-{i}] line {line}: " + " ".join(m.group(1).split())[:96])

    print("\n# no-config: what the budget tool does in a project with no .context-budget.json (MAIN's copy, temp dir)")
    src = "\n".join(blob(REFS["MAIN"], "starter-kit/context_budget.py") or [])
    with tempfile.TemporaryDirectory(prefix="plan-evidence-cb-") as tmp:
        proj = Path(tmp) / "proj"
        proj.mkdir()
        subprocess.run(["git", "init", "-q", str(proj)], capture_output=True)
        (proj / "context_budget.py").write_text(src + "\n", encoding="utf-8")
        for flag in ("--status", "--precommit"):
            r = subprocess.run([sys.executable, "-I", "context_budget.py", flag], cwd=proj,
                               capture_output=True, text=True)
            first = (r.stdout + r.stderr).strip().splitlines()[:1]
            msg = ANSI.sub("", first[0]).split(" at or above")[0] if first else ""  # the rest is a machine-local path
            print(f"[no-config{flag}] exit {r.returncode}: {msg[:70]}")


def blob_bytes(ref, path):
    r = subprocess.run(["git", "show", f"{ref}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def budget():
    """The runner and SAFEGUARDS.md each have a token ceiling in the repository's own .context-budget.json.
    The two ceilings sum to the read cap, so a byte added to either is paid for by a cut in either."""
    import json
    print("\n# budget: each read-set file's configured token ceiling against its size at the ref")
    for k in ("MAIN", "PR99", "FORK"):
        raw = blob_bytes(REFS[k], ".context-budget.json")
        if raw is None:
            print(f"[budget-{k}] no .context-budget.json at this ref")
            continue
        cfg = json.loads(raw)
        cap = cfg.get("read_cap_tokens")
        parts = []
        total_ceiling = 0
        for f in cfg.get("files", []):
            if f.get("class") != "read-set" or "max_tokens" not in f:
                continue
            data = blob_bytes(REFS[k], f["path"])
            size = len(data) if data is not None else None
            bpt = f.get("bytes_per_token", cfg.get("bytes_per_token"))  # a file may inherit the config-wide density
            ceiling = f["max_tokens"] * bpt
            total_ceiling += f["max_tokens"]
            head = None if size is None else round(ceiling) - size
            parts.append(f"{f['path'].split('/')[-1]}: {size} B of {round(ceiling)} B "
                         f"({f['max_tokens']} tok @ {bpt}), headroom {head} B")
        print(f"[budget-{k}] read cap {cap} tok, per-file ceilings sum {total_ceiling} tok; " + "; ".join(parts))
    src = blob(REFS["MAIN"], "starter-kit/context_budget.py") or []
    for i, ln in enumerate(src, 1):
        if re.match(r"^CLEAN, WARN, BREACH, USAGE\s*=", ln):
            print(f"[exit-codes-MAIN] context_budget.py:{i}: {ln.strip()}  (0 clean, 1 warn, 2 breach, 3 usage OR no config)")
    rc, out = git("tag", "-l")
    tags = sorted(t for t in out.split() if re.match(r"^v[0-9]", t))
    other = sorted(t for t in out.split() if not re.match(r"^v[0-9]", t))
    print(f"[tags-release-shaped] {len(tags)}: " + " ".join(tags))
    print(f"[tags-other] {len(other)}: " + " ".join(other))


def fresh_sync():
    """What `context_budget.py --status` says about a project made of MAIN's stock seed files (the files
    bin/sync installs), with nothing edited: the state of an adopter on the day of the sync (upstream issue #95)."""
    print("\n# fresh-sync: the budget tool on a project made only of MAIN's stock files, nothing edited")
    layout = {  # published name in the project <- path at MAIN
        "context_budget.py": "starter-kit/context_budget.py",
        ".context-budget.json": "starter-kit/context-budget.json",
        "CLAUDE.md": "starter-kit/CLAUDE_TEMPLATE.md",
        "SESSION_NOTES.md": "starter-kit/SESSION_NOTES.md",
        "SESSION_RUNNER.md": "starter-kit/SESSION_RUNNER.md",
        "SAFEGUARDS.md": "starter-kit/SAFEGUARDS.md",
    }
    with tempfile.TemporaryDirectory(prefix="plan-evidence-fresh-") as tmp:
        proj = Path(tmp) / "proj"
        proj.mkdir()
        subprocess.run(["git", "init", "-q", str(proj)], capture_output=True)
        for name, src in layout.items():
            data = blob_bytes(REFS["MAIN"], src)
            if data is None:
                print(f"[fresh-sync-skipped] {src} absent at MAIN")
                return
            (proj / name).write_bytes(data)
        r = subprocess.run([sys.executable, "-I", "context_budget.py", "--status"], cwd=proj,
                           capture_output=True, text=True)
        rows = [ANSI.sub("", ln) for ln in r.stdout.splitlines()]
        head = next((ln.strip() for ln in rows if "context budget" in ln), "")
        print(f"[fresh-sync-exit] {r.returncode}   headline: {' '.join(head.split())[:60]}")
        for ln in rows:
            m = re.match(r"^\s+(CLAUDE\.md|SESSION_NOTES\.md|LEARNINGS\.md)\s+.*?(over|unmeasured|warn|ok)\b", ln)
            if m:
                print(f"[fresh-sync-row] {m.group(1)}: {m.group(2)}")
        for ln in rows:
            if re.match(r"^\s+\S.* — .*(fence is missing|exceed \d+ B|fewer than the declared minimum)", ln):
                print("[fresh-sync-finding] " + " ".join(ln.split())[:140])


def main():
    rc, _ = git("rev-parse", "--git-dir")
    if rc:
        print("not a git repository; run from the repository root")
        return 0
    print("# refs")
    shas = {}
    for k, v in REFS.items():
        rc, out = git("rev-parse", "--short=8", f"{v}^{{commit}}")
        shas[k] = out.strip() if rc == 0 else "UNRESOLVED"
        print(f"[ref-{k}] {v} = {shas[k]}")

    print("\n# sites: line span of each edit region at each ref (ABSENT = pattern not found)")
    regions = {}
    for sid, path, start, end, n in SITES:
        row = []
        for k in ("V42", "MAIN", "FORK"):
            r = find_region(blob(REFS[k], path), start, end, n)
            regions[(sid, k)] = r
            row.append(f"{k} " + (f"{r[0]}-{r[1]}" if r else "ABSENT"))
        print(f"[site-{sid}] {path}: " + "; ".join(row))

    print("\n# overlap: does an open pull request change lines in or beside the region on upstream/main?")
    for sid, path, *_ in SITES:
        region = regions[(sid, "MAIN")]
        if region is None:
            print(f"[overlap-{sid}] region not found on MAIN; not computed")
            continue
        parts = []
        for pr in PRS:
            hit = touches(region, hunks_on_main_side(REFS[pr], path))
            parts.append(f"{pr} " + ("yes " + ",".join(f"{x}-{y}" for x, y in hit) if hit else "no"))
        print(f"[overlap-{sid}] region MAIN {region[0]}-{region[1]}: " + "; ".join(parts))

    print("\n# size: the runner every session reads in full")
    for k in REFS:
        lines = blob(REFS[k], "starter-kit/SESSION_RUNNER.md")
        size = len(("\n".join(lines) + "\n").encode()) if lines else None
        print(f"[size-runner-{k}] {size if size is not None else 'ABSENT'} B")

    extras()
    budget()
    fresh_sync()

    print("\n# mode: upstream's atomic_write on a 0644 ledger, a new shard, and a verify script (umask 022)")
    src = "\n".join(blob(REFS["MAIN"], "starter-kit/methodology_trim.py") or [])
    if not src:
        print("[mode-skipped] no trimmer at MAIN")
        return 0
    with tempfile.TemporaryDirectory(prefix="plan-evidence-") as tmp:
        mod_path = Path(tmp) / "trim_main.py"
        mod_path.write_text(src + "\n", encoding="utf-8")
        spec = importlib.util.spec_from_file_location("trim_main", str(mod_path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        d = Path(tmp) / "t"
        d.mkdir()
        old = os.umask(0o022)
        try:
            ledger = d / "LEDGER.md"
            ledger.write_text("old\n")
            os.chmod(ledger, 0o644)
            before = stat.S_IMODE(ledger.stat().st_mode)
            mod.atomic_write(ledger, "new\n")
            after = stat.S_IMODE(ledger.stat().st_mode)
            shard = d / "shard.md"
            mod.atomic_write(shard, "x\n")
            verify = d / "shard.md.verify.sh"
            mod.atomic_write(verify, "#!/bin/sh\n", executable=True)
            print(f"[mode-existing-ledger] before {before:o} -> after {after:o}")
            print(f"[mode-new-shard] {stat.S_IMODE(shard.stat().st_mode):o}")
            print(f"[mode-verify-script] {stat.S_IMODE(verify.stat().st_mode):o}")
        finally:
            os.umask(old)
    return 0


if __name__ == "__main__":
    sys.exit(main())
