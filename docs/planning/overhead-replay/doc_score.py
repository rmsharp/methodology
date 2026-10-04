#!/usr/bin/env python3
"""Documentation scorer for the BL-94 study (plan docs/planning/documentation-quality-experiment-plan.md, sections 2 to 4).

    python3 doc_score.py REPO BASE PIN [--final FILE] [--task-done true|false] [--measured JSON]
    python3 doc_score.py key REPO BASE PIN                       # the M4 answer key, from the tree and git only
    python3 doc_score.py report-score KEY.json REPORT.txt        # M4: score a cold session's Phase 0 report
    python3 doc_score.py smoke MANIFEST_DIR [--project PATH]     # parse every saved run; prints parse facts, never a score

REPO is a git repository holding the run (a saved tree, or a clone with the evidence bundle fetched); BASE is the sha of the
harness's "Install methodology arm" commit; PIN is the pinned end sha (the first close-out commit, plan 2.5). Everything here is a
function of the commits in BASE..PIN and the PIN tree, plus the session's final message when one is passed. Mechanical: the only
places a reading is built into a rule are the two keyword rules, SAYS_DONE (M2 c) and STATED_REMOVED (M1 b), and they are the
constants named so. Python 3 stdlib only.

THE RECORD (plan 2.2). The lines the session ADDED to tracked files that are not code, tests, generated output or machine
configuration, across BASE..PIN, plus the session's final message. A line is dropped when the same line, whitespace-stripped, is
DELETED from any file in the same range (a moved line is not a new claim); a line copied from the base and not deleted elsewhere
stays, because carrying a stale line forward is what the measure is for. It is defined by the diff and not by a file name, so
v3.0's SESSION_NOTES.md and v3.8's HANDOFFS.md are read alike. The install commit is BASE and so is never in the range.

M1 (checkable-reference accuracy): distinct shas, paths, path:line anchors and test-count statements in the record, each checked
against the PIN tree. M2 (action coverage and stub resolution): (a) commits named, (b) pending stubs left, (c) done claimed against
the task's own check; reported as separate parts, never summed. M3 has no target yet (plan 3.4): only the path classification is
here. M4: the key builder and the report scorer. M5 is a model rater and lives elsewhere.

THE SCORER IS FROZEN at the end of P1a (plan section 4, item 1). After the freeze a defect is fixed only with the operator's word,
everything is re-scored, and both versions are reported.
"""
import argparse, json, os, re, subprocess, sys
from collections import Counter
sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- definitions: every number or word list the plan leaves to P1a is a named constant ---------------------------------------
ANCHOR_WINDOW = 5            # plan 2.3 M1: an identifier beside an anchor must occur within five lines of it
CEILING = 0.95               # plan 2.3 M1 ceiling rule: at or above this in every saved run, M1 is reported as uninformative
BESIDE_GAP = 10              # at most this many characters of punctuation or "at/in/of/see/near/line" between anchor and identifier

# Not the record: code, tests, generated output, machine configuration and metadata (plan 2.2 lists R sources, man/, NAMESPACE, test
# files and test_results_summary.md; the other entries are the same kinds in this project's tree and are listed so the choice is visible).
NOT_RECORD_DIRS = ("R/", "src/", "tests/", "man/", "data/", "data-raw/", "inst/", "renv/", "bin/", ".githooks/")
NOT_RECORD_NAMES = {"NAMESPACE", "DESCRIPTION", "test_results_summary.md", "renv.lock", ".Rbuildignore", ".gitignore", ".Rprofile",
                    "LICENSE", "LICENSE.md", "Makefile"}
NOT_RECORD_EXT = {".r", ".c", ".cc", ".cpp", ".h", ".py", ".sh", ".js", ".css", ".rd", ".rda", ".rds", ".rdata", ".csv", ".tsv", ".json",
                  ".jsonl", ".yml", ".yaml", ".toml", ".cfg", ".lock", ".svg", ".png", ".jpg", ".jpeg", ".pdf", ".html", ".xlsx", ".zip"}

# M1 (b): what a path token looks like. Receipts name paths bare (`key_files: R/x.R:27, ...`), so bare tokens count, not only backticked.
PATH_EXT = ("R", "r", "Rmd", "md", "Rd", "yml", "yaml", "json", "jsonl", "py", "sh", "txt", "html", "csv", "toml", "cfg", "c", "cpp", "h",
            "js", "css", "Rproj", "rds", "rda")
KNOWN_BARE_FILES = ("DESCRIPTION", "NAMESPACE", "LICENSE", "Makefile", ".Rbuildignore", ".gitignore", ".Rprofile")
_P = r"(?:[\w.-]+/)*[\w.-]+\.(?:%s)" % "|".join(PATH_EXT)
_PB = "|".join(re.escape(n) for n in KNOWN_BARE_FILES)
PATH_RE = re.compile(r"(?<![\w/.:~$<{*-])((?:%s|%s))(?![\w/-])" % (_P, _PB))
ANCHOR_RE = re.compile(r"(?<![\w/.:~$<{*-])((?:%s))(?::(\d+)(?:[-–](\d+))?)(?![\w/-])" % _P)
URL_RE = re.compile(r"\b(?:https?|ftp)://\S+")
SHA_RE = re.compile(r"(?<![0-9A-Za-z_-])([0-9a-f]{7,40})(?![0-9A-Za-z_-]|\.\w)")
SHA_ANY_RE = SHA_RE      # any 7-40 hex token, for matching against known commits; SHA_RE's extra rules (digit and letter) are in extract_refs
SHA_CONTEXT_RE = re.compile(r"(?i)\b(commit|sha|hash|rev)\b")
IDENT_RE = re.compile(r"^[A-Za-z_.][A-Za-z0-9_.]*(?:\(\))?$")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
# M1 (b): "stated as removed" -- the line that names a missing path says it is gone. The first of the two keyword rules.
STATED_REMOVED = re.compile(r"(?i)\b(remov\w*|delet\w*|drop(?:ped)?|retir\w*|archiv\w*|gone|no longer exist\w*|deprecat\w*|renam\w*|"
                            r"moved?\s+(?:to|into)|replac\w*|obsolete|superseded)\b")
# M1 (d): a stated test count. Baseline statements are about another state and are not checked against the end state.
COUNT_RE = re.compile(r"(?i)(?<![\w.])(\d[\d,]*)\s+(?:tests?\s+|expectations?\s+)?(pass(?:ed|ing|es)?|fail(?:ed|ures?|ing)?|warn(?:ings?|ed)?|errors?|skipped|skips?)\b")
TESTTHAT_RE = re.compile(r"FAIL\s+(\d+)\s*\|\s*WARN\s+(\d+)\s*\|\s*SKIP\s+(\d+)\s*\|\s*PASS\s+(\d+)")
BASELINE_RE = re.compile(r"(?i)\b(baseline|before|previous|prior|earlier|pre-?fix|was|were|from|had)\b|->|→|=>")
COUNT_KIND = {"pass": "passed", "fail": "failed", "warn": "warnings", "error": "errors", "skip": "skipped"}

# M2 (c): "the record says the deliverable is done". The second keyword rule. A line says done when a task word and a done word
# sit within 100 characters and no negator or qualifier sits just before or after the done word. A receipt's own `status:` field
# is the close-out's status, not the deliverable's, and is never read as a claim.
TASK_WORD = re.compile(r"(?i)\b(active[_ ]task|deliverable|task|status|issue\s*#?\d+|#\d+)\b")
DONE_WORD = re.compile(r"(?i)\b(done|complete[d]?|finished|resolved|shipped|delivered|closed|fixed)\b")
NEG_BEFORE = re.compile(r"(?i)(\bnot\b|\bnever\b|n't\b|\bno longer\b|\bnot yet\b|\bincomplete\b|\bunfinished\b|\bunresolved\b|\bpartial(?:ly)?\b|"
                        r"\bpending\b|\bin[- ]progress\b|\bstill\b|\bonly\b|\buntil\b|\bonce\b|\bwhen\b|\bif\b|\bbefore\b)[^.;\n]{0,40}$")
NEG_AFTER = re.compile(r"(?i)^[^.;\n]{0,15}(\bpartial\b|\bexcept\b|\bbut not\b|\bnot (?:yet|fully)\b)")
STATUS_FIELD = re.compile(r"^status:\s*\w+\s*$")

# M2 (b): the stubs a session writes. Only where the installed runner has such an artifact (plan 2.3 M2).
LEDGER_PENDING = re.compile(r"(?i)^\W*(?:\*\*)?ledger:?(?:\*\*)?\W.*CHANGELOG:\s*`?pending")
RUNNER_PENDING_MARKERS = ("status: pending", "CHANGELOG: pending")

# M3 (plan 3.4, written before any scorer): which documents are history and which are live. M3 itself waits for a task.
HISTORICAL = ("CHANGELOG.md", "SESSION_NOTES.md", "HANDOFFS.md", "PROJECT_LEARNINGS.md", "TECH_DEBT_AUDIT_2026-05-30.md", "test_results_summary.md")
HISTORICAL_PREFIXES = ("docs/planning/", "docs/archive/")
LIVE_PATHS = ("CLAUDE.md", "_pkgdown.yml", "pkgdown/_pkgdown.yml")     # the pkgdown config pkgdown reads; inst/_pkgdown.yml is shadowed (plan 3.4)
LIVE_NAME_PREFIXES = ("README", "NEWS")
LIVE_PREFIXES = ("vignettes/",)

# M4 (plan 2.3): the facts a cold session's Phase 0 report is scored on.
DELIVERABLE_PREFIX = re.compile(r"^(fix|feat|refactor|perf|test|chore|build)(\([^)]*\))?!?:")
CODE_DELIVERABLE = re.compile(r"^(fix|feat|refactor|perf)(\([^)]*\))?!?:")
CLOSEOUT_SUBJECT = re.compile(r"(?i)close.?out|hand-?off|wrap.?up")
PART_LABEL = re.compile(r"(?i)^\W*(key[ _]files?|next[ _]steps?|what.s next|next session|next up)\b")
LEDGER_FINDING = re.compile(r"(?i)\b(ghost|undocumented|reconcil\w*|backfill\w*|unrecorded|ledger)\b")
CLEAN_TREE = re.compile(r"(?i)(working (?:tree|directory)|worktree|git status)[^.\n]{0,40}\b(clean|no changes|nothing to commit)\b|"
                        r"\b(no|nothing)\s+uncommitted\b|\bclean\b[^.\n]{0,20}\b(tree|working)\b|\bno uncommitted\b|\buncommitted:\s*none\b")
REPORT_DONE = re.compile(r"(?i)\b(complete[d]?|done|finished|closed out|resolved|delivered|fixed)\b")
REPORT_NOT_DONE = re.compile(r"(?i)\b(incomplete|unfinished|not (?:yet )?(?:complete|done|finished)|in progress|partial(?:ly)?|unresolved)\b")


# ---- git ------------------------------------------------------------------------------------------------------------------------
def git(repo, *args, check=True):
    p = subprocess.run(["git", "-c", "core.quotePath=false", "-C", repo, *args], capture_output=True, text=True, errors="replace")
    if check and p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed in {repo}: {p.stderr.strip()}")
    return p.stdout


def blob(repo, rev, path):
    p = subprocess.run(["git", "-c", "core.quotePath=false", "-C", repo, "show", f"{rev}:{path}"], capture_output=True, text=True, errors="replace")
    return p.stdout if p.returncode == 0 else None


def tree_paths(repo, rev):
    return git(repo, "ls-tree", "-r", "--name-only", rev).splitlines()


def session_commits(repo, base, pin):
    """The session's own commits, oldest first: [(sha, subject, committer epoch)]. The install commit (BASE) is not among them."""
    out = git(repo, "log", "--reverse", "--no-merges", "--format=%H%x1f%s%x1f%ct", f"{base}..{pin}")
    return [(h, s, int(t)) for h, s, t in (line.split("\x1f") for line in out.splitlines() if line)]


def reachable(repo, rev):
    return set(git(repo, "rev-list", rev).split())


# ---- the record -----------------------------------------------------------------------------------------------------------------
def is_record_path(path):
    name = os.path.basename(path)
    if path.startswith(NOT_RECORD_DIRS) or name in NOT_RECORD_NAMES:
        return False
    return os.path.splitext(name)[1].lower() not in NOT_RECORD_EXT


def diff_lines(repo, base, pin):
    """The net diff BASE..PIN as {path: (added, removed)}, read by hunk counts (-U0), never by looking for `+++`, so a content
    line that begins with `++` cannot be mistaken for a file header."""
    text = git(repo, "diff", "--no-renames", "--no-color", "-U0", base, pin)
    files, path, state = {}, None, None
    old = new = None
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("diff --git "):
            state, path, old, new = "header", None, None, None
        elif state == "header" and line.startswith("--- "):
            old = line[4:]
        elif state == "header" and line.startswith("+++ "):
            new = line[4:]
            p = new if new != "/dev/null" else old
            path = p[2:] if p and p[:2] in ("a/", "b/") else p
            files.setdefault(path, ([], []))
        elif line.startswith("@@") and path is not None:
            m = re.match(r"@@ -\d+(?:,(\d+))? \+\d+(?:,(\d+))? @@", line)
            nrem = int(m.group(1)) if m.group(1) is not None else 1
            nadd = int(m.group(2)) if m.group(2) is not None else 1
            for _ in range(nrem):
                i += 1
                files[path][1].append(lines[i][1:])
            if i + 1 < len(lines) and lines[i + 1].startswith("\\"):
                i += 1
            for _ in range(nadd):
                i += 1
                files[path][0].append(lines[i][1:])
            if i + 1 < len(lines) and lines[i + 1].startswith("\\"):
                i += 1
            state = "hunks"
        i += 1
    return files


def record(repo, base, pin, final_message=""):
    """The session's record (module docstring). Returns {lines: [(source, text)], raw: {path: [text, '' for a blank line]}, added, moved,
    files}; `text` is whitespace-stripped and non-empty in `lines`. `moved` counts added lines dropped because the same line was deleted
    somewhere in the range; `raw` keeps the blank lines so a labelled paragraph can be found."""
    files = diff_lines(repo, base, pin)
    removed = {r.strip() for _, (_, rem) in files.items() for r in rem if r.strip()}
    lines, raw, added, moved, per_file = [], {}, 0, 0, Counter()
    for path, (add, _) in sorted(files.items()):
        if not is_record_path(path):
            continue
        raw[path] = []
        for a in add:
            t = a.strip()
            if not t:
                raw[path].append("")
                continue
            added += 1
            if t in removed:
                moved += 1
                continue
            lines.append((path, t))
            raw[path].append(t)
            per_file[path] += 1
    for t in (final_message or "").splitlines():
        if t.strip():
            lines.append(("<final message>", t.strip()))
            per_file["<final message>"] += 1
    return {"lines": lines, "raw": raw, "added": added, "moved": moved, "files": dict(per_file)}


def final_message(events, pin_epoch=None):
    """The session's final message at the pin: the last assistant text between the pin commit's time and the next human turn
    (the whole transcript's last text when no time is given). `events` is replaylib.events() output; times are epoch seconds."""
    if pin_epoch is None:
        texts = [e["text"] for e in events if e["kind"] == "text"]
        return texts[-1] if texts else ""
    last, started = "", False
    for e in events:
        ts = e.get("ts")
        if not started:
            started = ts is not None and ts.timestamp() >= pin_epoch
            if not started:
                continue
        if e["kind"] == "human":
            break
        if e["kind"] == "text":
            last = e["text"]
    return last


# ---- receipts -------------------------------------------------------------------------------------------------------------------
RECEIPT_BLOCK = re.compile(r"```handoff\n(.*?)\n```", re.S)
FIELD_RE = re.compile(r"^([a-z_]+):\s?(.*)$")


def parse_receipts(text):
    """Receipt blocks, newest first, as dicts of field -> value (multi-line values joined). A block whose `session:` line contains `<`
    or `>` is the format example in the file's front matter and is skipped (plan P1a (c); it fooled two earlier tallies)."""
    out = []
    for m in RECEIPT_BLOCK.finditer(text or ""):
        fields, last = {}, None
        for line in m.group(1).split("\n"):
            f = FIELD_RE.match(line)
            if f:
                last = f.group(1)
                fields[last] = f.group(2)
            elif last is not None:
                fields[last] += "\n" + line
        sess = fields.get("session", "")
        if "<" in sess or ">" in sess or not sess:
            continue
        fields["_block"] = m.group(1)
        out.append(fields)
    return out


# ---- M1 -------------------------------------------------------------------------------------------------------------------------
def _spans(regex, line):
    return [(m.start(), m.end(), m) for m in regex.finditer(line)]


def _blanked(line, spans):
    """The line with each span replaced by spaces, so later patterns cannot match inside an earlier match."""
    chars = list(line)
    for s, e, *_ in spans:
        for k in range(s, e):
            chars[k] = " "
    return "".join(chars)


def extract_refs(rec_lines):
    """Distinct checkable references in the record: {shas, paths, anchors, counts}. Each entry carries the line it came from."""
    shas, paths, anchors, counts = {}, {}, {}, []
    for source, line in rec_lines:
        url_spans = _spans(URL_RE, line)
        work = _blanked(line, url_spans)
        anchor_spans = [(s, e, m) for s, e, m in _spans(ANCHOR_RE, work) if not (m.group(1).startswith("/") or ".." in m.group(1))]
        for s, e, m in anchor_spans:
            key = (m.group(1).removeprefix("./"), int(m.group(2)), int(m.group(3)) if m.group(3) else None)
            anchors.setdefault(key, {"line": line, "span": (s, e)})
        work2 = _blanked(work, anchor_spans)
        for s, e, m in _spans(PATH_RE, work2):
            p = m.group(1).removeprefix("./")
            if p.startswith("/") or ".." in p or ("/" in p and re.search(r"\.(com|org|net|io|dev)$", p.split("/")[0])):
                continue
            paths.setdefault(p, {"line": line})
        for s, e, m in _spans(SHA_RE, work):
            tok = m.group(1)
            mixed = re.search(r"\d", tok) and re.search(r"[a-f]", tok)
            if mixed or SHA_CONTEXT_RE.search(line):        # an all-digit or all-letter token counts only on a line that speaks of a commit
                shas.setdefault(tok, {"line": line})
        counts.extend(count_claims(line))
    return {"shas": shas, "paths": paths, "anchors": anchors, "counts": counts}


def count_claims(line):
    """Stated test counts on one line: [{kind, n, line}]. A line that speaks of another state (baseline, before, ->) yields none."""
    if BASELINE_RE.search(line):
        return []
    out = []
    m = TESTTHAT_RE.search(line)
    if m:
        for kind, g in (("failed", 1), ("warnings", 2), ("skipped", 3), ("passed", 4)):
            out.append({"kind": kind, "n": int(m.group(g)), "line": line})
        return out
    for m in COUNT_RE.finditer(line):
        kind = next(v for k, v in COUNT_KIND.items() if m.group(2).lower().startswith(k))
        out.append({"kind": kind, "n": int(m.group(1).replace(",", "")), "line": line})
    return out


def compare_counts(claims, measured):
    """(checkable, verified, mismatches): a claim is checkable only for a kind the measurement has; it is verified when it equals it."""
    checkable = verified = 0
    bad = []
    for c in claims:
        if measured is None or c["kind"] not in measured:
            continue
        checkable += 1
        if measured[c["kind"]] == c["n"]:
            verified += 1
        else:
            bad.append({**c, "measured": measured[c["kind"]]})
    return checkable, verified, bad


def _idents_beside(line, span):
    """Backticked identifiers directly beside an anchor: before or after it, with only punctuation or one of at/in/of/see/near/line
    between (BESIDE_GAP characters at most)."""
    s, e = span
    found = []
    for m in BACKTICK_RE.finditer(line):
        tok = m.group(1).strip()
        if not IDENT_RE.fullmatch(tok) or ANCHOR_RE.search(tok) or len(tok.removesuffix("()")) < 3 or tok.isdigit():
            continue
        if m.start() <= s and m.end() >= e:        # the anchor's own backticks
            continue
        gap = line[m.end():s] if m.end() <= s else line[e:m.start()] if m.start() >= e else None
        if gap is None or len(gap) > BESIDE_GAP:
            continue
        if re.fullmatch(r"[\s`'\"(\[,:;–—-]*(?:at|in|of|see|near|line)?[\s`'\"(\[,:;–—-]*", gap):
            found.append(tok.removesuffix("()"))
    return found


def _resolve(repo, pin, path, names):
    """The path's text at the pin, or None. A token with no directory part may name a file anywhere in the tree (by basename)."""
    t = blob(repo, pin, path)
    if t is not None:
        return t
    if "/" not in path:
        hits = [p for p in names if os.path.basename(p) == path]
        if hits:
            return blob(repo, pin, sorted(hits)[0])
    return None


def score_m1(repo, base, pin, rec, measured=None):
    """M1 over one run. Each kind reports its checkable count and how many verified; `accuracy` pools them. `failures` names every
    reference that did not verify, so a hand-read can see exactly what the scorer held against the record."""
    refs = extract_refs(rec["lines"])
    names = tree_paths(repo, pin)
    nameset = set(names)
    reach = reachable(repo, pin)
    out = {"shas": {"checkable": 0, "verified": 0}, "paths": {"checkable": 0, "verified": 0, "stated_removed": 0},
           "anchors": {"checkable": 0, "verified": 0}, "counts": {"checkable": 0, "verified": 0}, "failures": []}
    for tok, info in sorted(refs["shas"].items()):
        p = subprocess.run(["git", "-C", repo, "rev-parse", "--verify", "--quiet", f"{tok}^{{commit}}"], capture_output=True, text=True)
        full = p.stdout.strip()
        out["shas"]["checkable"] += 1
        if p.returncode == 0 and full in reach:
            out["shas"]["verified"] += 1
        else:
            out["failures"].append({"kind": "sha", "token": tok, "why": "not a commit reachable from the pin" if p.returncode == 0 else "does not resolve",
                                    "line": info["line"][:200]})
    for path, info in sorted(refs["paths"].items()):
        out["paths"]["checkable"] += 1
        if path in nameset or ("/" not in path and any(os.path.basename(n) == path for n in names)):
            out["paths"]["verified"] += 1
        elif STATED_REMOVED.search(info["line"]):
            out["paths"]["verified"] += 1
            out["paths"]["stated_removed"] += 1
        else:
            out["failures"].append({"kind": "path", "token": path, "why": "absent at the pin and not stated removed", "line": info["line"][:200]})
    for (path, a, b), info in sorted(refs["anchors"].items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2] or 0)):
        out["anchors"]["checkable"] += 1
        text = _resolve(repo, pin, path, names)
        if text is None:
            if STATED_REMOVED.search(info["line"]):
                out["anchors"]["verified"] += 1
            else:
                out["failures"].append({"kind": "anchor", "token": f"{path}:{a}" + (f"-{b}" if b else ""), "why": "file absent at the pin", "line": info["line"][:200]})
            continue
        flines = text.split("\n")
        if flines and flines[-1] == "":
            flines.pop()
        hi = b if b else a
        if a < 1 or hi < a or hi > len(flines):
            out["failures"].append({"kind": "anchor", "token": f"{path}:{a}" + (f"-{b}" if b else ""),
                                    "why": f"line outside the file ({len(flines)} lines)", "line": info["line"][:200]})
            continue
        idents = _idents_beside(info["line"], info["span"])
        window = "\n".join(flines[max(0, a - 1 - ANCHOR_WINDOW):hi + ANCHOR_WINDOW])
        if idents and not any(i in window for i in idents):
            out["failures"].append({"kind": "anchor", "token": f"{path}:{a}" + (f"-{b}" if b else ""),
                                    "why": f"{idents} not within {ANCHOR_WINDOW} lines", "line": info["line"][:200]})
            continue
        out["anchors"]["verified"] += 1
    c, v, bad = compare_counts(refs["counts"], measured)
    out["counts"].update(checkable=c, verified=v, claimed=len(refs["counts"]))
    out["failures"].extend({"kind": "count", "token": f"{b['n']} {b['kind']}", "why": f"measured {b['measured']}", "line": b["line"][:200]} for b in bad)
    tot_c = sum(out[k]["checkable"] for k in ("shas", "paths", "anchors", "counts"))
    tot_v = sum(out[k]["verified"] for k in ("shas", "paths", "anchors", "counts"))
    out["checkable"], out["verified"] = tot_c, tot_v
    out["accuracy"] = (tot_v / tot_c) if tot_c else None
    return out


def m1_at_ceiling(results):
    """Plan 2.3: M1 is uninformative when it sits at or above CEILING in every saved run. `results` is a list of score_m1 outputs;
    a run with nothing checkable cannot show a defect and does not break the ceiling."""
    scored = [r["accuracy"] for r in results if r.get("accuracy") is not None]
    return bool(scored) and all(a >= CEILING for a in scored)


# ---- M2 -------------------------------------------------------------------------------------------------------------------------
def _norm(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def _subject_core(subject):
    return _norm(re.sub(r"^\w+(\([^)]*\))?!?:\s*", "", subject))


def says_done(rec_lines):
    """The record says the deliverable is done (the second keyword rule; module constants)."""
    for _, line in rec_lines:
        if STATUS_FIELD.match(line):
            continue
        for d in DONE_WORD.finditer(line):
            before, after = line[:d.start()], line[d.end():]
            tw = list(TASK_WORD.finditer(before[-100:])) or list(TASK_WORD.finditer(after[:100]))
            if not tw:
                continue
            if NEG_BEFORE.search(before) or NEG_AFTER.search(after):
                continue
            return True
    return False


def runner_has_pending_artifacts(repo, base):
    """M2(b) is defined only where the installed runner has a pending receipt or a CHANGELOG: pending marker (plan 2.3)."""
    runner = blob(repo, base, "SESSION_RUNNER.md") or ""
    return any(m in runner for m in RUNNER_PENDING_MARKERS)


def pending_left(repo, base, pin, rec):
    """Stubs the session wrote and left: pending receipts (blocks not present verbatim at BASE) and `Ledger: CHANGELOG: pending` lines."""
    base_blocks = {r["_block"] for r in parse_receipts(blob(repo, base, "HANDOFFS.md") or "")}
    receipts = [r for r in parse_receipts(blob(repo, pin, "HANDOFFS.md") or "")
                if r.get("status", "").strip() == "pending" and r["_block"] not in base_blocks]
    marker = [t for p, t in rec["lines"] if p != "<final message>" and LEDGER_PENDING.search(t)]
    return {"receipts": [r.get("session", "?") for r in receipts], "changelog_markers": marker}


def commit_slot_pending(repo, pin):
    """Descriptive only (plan 2.3: the `commit:` slot may legitimately read pending): the newest receipt's slot value, or None."""
    rs = parse_receipts(blob(repo, pin, "HANDOFFS.md") or "")
    return rs[0].get("commit", "").strip() if rs else None


def score_m2(repo, base, pin, rec, task_done=None):
    """M2's three parts, never summed. (a) commits named by sha or subject; the pin commit cannot name its own sha and is reported apart.
    (b) None for a version with no pending artifact ("not applicable", not a pass). (c) None when the task's check was not supplied."""
    commits = session_commits(repo, base, pin)
    text = _norm("\n".join(t for _, t in rec["lines"]))
    toks = set(SHA_ANY_RE.findall("\n".join(t for _, t in rec["lines"])))
    pin_full = git(repo, "rev-parse", pin).strip()
    named, missing = 0, []
    own = [c for c in commits if c[0] != pin_full]
    for sha, subject, _ in own:
        by_sha = any(sha.startswith(t) for t in toks)
        core = _subject_core(subject)
        if by_sha or (core and core in text):
            named += 1
        else:
            missing.append({"sha": sha[:8], "subject": subject[:100]})
    pin_commit = next((c for c in commits if c[0] == pin_full), None)
    applicable = runner_has_pending_artifacts(repo, base)
    left = pending_left(repo, base, pin, rec)
    done = says_done(rec["lines"])
    return {"a": {"commits": len(own), "named": named, "coverage": (named / len(own)) if own else None, "missing": missing,
                  "pin_commit_named": bool(pin_commit and _subject_core(pin_commit[1]) and _subject_core(pin_commit[1]) in text)},
            "b": ({"left": len(left["receipts"]) + len(left["changelog_markers"]), **left} if applicable else None),
            "b_descriptive": left, "b_applicable": applicable,
            "commit_slot": commit_slot_pending(repo, pin),
            "c": ({"says_done": done, "task_done": task_done, "flag": bool(done and task_done is False)} if task_done is not None else None),
            "says_done": done}



# ---- M3: classification only ----------------------------------------------------------------------------------------------------
def classify_path(path):
    """'historical' (never edited), 'live' (must stay true) or 'unclassified' (classified when found, plan 3.4)."""
    name = os.path.basename(path)
    if path in HISTORICAL or name in HISTORICAL or path.startswith(HISTORICAL_PREFIXES):
        return "historical"
    if path in LIVE_PATHS or name.startswith(LIVE_NAME_PREFIXES) or path.startswith(LIVE_PREFIXES):
        return "live"
    return "unclassified"


# ---- M4 -------------------------------------------------------------------------------------------------------------------------
RECEIPT_FIELD_LINE = re.compile(r"^[a-z_]+:\s")


def _parts(raw):
    """The record's key-files and next-steps parts: a labelled paragraph runs from its label to a blank line, a heading, a fence or
    the next receipt field. Receipt fields are one line each, so a field `key_files:` or `next_steps:` is its own part."""
    parts = []
    for path, lines in sorted(raw.items()):
        cur = None
        for line in lines:
            if not line:
                cur = None
            elif PART_LABEL.match(line):
                cur = [line]
                parts.append(cur)
            elif cur is not None and (line.startswith("#") or line.startswith("```") or RECEIPT_FIELD_LINE.match(line)):
                cur = None
            elif cur is not None:
                cur.append(line)
    return ["\n".join(p) for p in parts]


def build_key(repo, base, pin):
    """The M4 answer key, from the repository alone (the signature admits nothing else). Git-derivable facts, then the record-only
    facts, then the ledger-or-ghost finding on its own line, which is in no arm's denominator (plan 2.3)."""
    commits = session_commits(repo, base, pin)
    subjects = [s for _, s, _ in commits]
    sess = Counter(m for s in subjects for m in re.findall(r"\bS(\d+)\b", s))
    issues = Counter(m for s in subjects for m in re.findall(r"#(\d+)", s))
    deliv = [c for c in commits if CODE_DELIVERABLE.match(c[1])] or [c for c in commits if DELIVERABLE_PREFIX.match(c[1])]
    last_deliv = deliv[-1] if deliv else None          # a fix, feature or refactor is the deliverable; a test or chore only if there is none
    terms = sorted({f"#{n}" for n in issues} | ({m.removesuffix("()") for m in re.findall(r"\b\w+\(\)", last_deliv[1])} if last_deliv else set()))
    pin_full = git(repo, "rev-parse", pin).strip()
    pin_subject = next((s for h, s, _ in commits if h == pin_full), "")
    rec = record(repo, base, pin)
    pending = pending_left(repo, base, pin, rec)
    complete = bool(CLOSEOUT_SUBJECT.search(pin_subject)) and not pending["receipts"] and not pending["changelog_markers"]
    parts = _parts(rec["raw"])
    refs = extract_refs([("<part>", t) for p in parts for t in p.split("\n")])
    return {"git_derivable": {"session": f"S{sess.most_common(1)[0][0]}" if sess else None,
                              "deliverable_terms": terms or None,
                              "deliverable_commit": last_deliv[0] if last_deliv else None,
                              "complete": complete,
                              "uncommitted": False},
            "record_only": {"paths": sorted({p for p in refs["paths"]} | {a[0] for a in refs["anchors"]}), "shas": sorted(refs["shas"])},
            "ledger_finding": {"key": "reported on its own line; no v3.0 counterpart"},
            "pin": pin_full}


def score_report(key, report):
    """M4 for one cold report: each git-derivable fact stated or not, the record-only fraction, and the ledger line apart."""
    text = report or ""
    low = text.lower()
    g = key["git_derivable"]
    facts = {}
    if g.get("session"):
        facts["session"] = bool(re.search(r"(?i)\bs(?:ession)?\s*%s\b" % re.escape(g["session"][1:]), text))
    if g.get("deliverable_terms"):
        facts["deliverable"] = any(t.lower() in low for t in g["deliverable_terms"])
    if g.get("deliverable_commit"):
        facts["deliverable_commit"] = any(g["deliverable_commit"].startswith(t) for t in SHA_ANY_RE.findall(text))
    if g.get("complete") is not None:
        says_complete = bool(REPORT_DONE.search(text)) and not REPORT_NOT_DONE.search(text)
        facts["complete"] = says_complete == bool(g["complete"])
    facts["uncommitted"] = bool(CLEAN_TREE.search(text)) == (not g.get("uncommitted", False))
    ro = key["record_only"]
    named = [p for p in ro["paths"] if p.lower() in low or os.path.basename(p).lower() in low]
    named_shas = [s for s in ro["shas"] if any(s.startswith(t) or t.startswith(s) for t in SHA_ANY_RE.findall(text))]
    denom = len(ro["paths"]) + len(ro["shas"])
    return {"git_derivable": facts, "git_derivable_score": (sum(facts.values()) / len(facts)) if facts else None,
            "record_only": {"named": len(named) + len(named_shas), "of": denom, "fraction": ((len(named) + len(named_shas)) / denom) if denom else None},
            "ledger_finding_reported": bool(LEDGER_FINDING.search(text))}


# ---- one run, and the smoke test ------------------------------------------------------------------------------------------------
def score_run(repo, base, pin, final="", task_done=None, measured=None):
    rec = record(repo, base, pin, final)
    return {"record": {"lines": len(rec["lines"]), "added": rec["added"], "moved": rec["moved"], "files": rec["files"]},
            "m1": score_m1(repo, base, pin, rec, measured), "m2": score_m2(repo, base, pin, rec, task_done)}


def parse_facts(repo, base, pin):
    """What parsing found, with no score computed: the P1a (d) smoke test prints this and nothing else."""
    rec = record(repo, base, pin)
    refs = extract_refs(rec["lines"])
    pin_receipts = parse_receipts(blob(repo, pin, "HANDOFFS.md") or "")
    return {"record_lines": len(rec["lines"]), "added": rec["added"], "moved": rec["moved"], "record_files": len(rec["files"]),
            "shas": len(refs["shas"]), "paths": len(refs["paths"]), "anchors": len(refs["anchors"]), "count_claims": len(refs["counts"]),
            "receipts_at_pin": len(pin_receipts), "commits": len(session_commits(repo, base, pin)),
            "parts": len(_parts(rec["raw"])), "runner_has_pending_artifacts": runner_has_pending_artifacts(repo, base)}


def smoke(manifest_dir, project=None):
    """P1a (d): rebuild every saved run from the evidence bundle and print what PARSING found for each, never a score, so a record
    format that does not parse is found before the freeze and no score is read before it (plan section 4, item 1)."""
    sys.path.insert(0, HERE)
    import doc_evidence
    scratch, manifest = doc_evidence.rebuild(manifest_dir, project or doc_evidence.DEFAULT_PROJECT)
    cols = ["record_lines", "added", "moved", "record_files", "shas", "paths", "anchors", "count_claims", "receipts_at_pin", "commits", "parts"]
    print("run".ljust(24) + " ".join(c[:9].rjust(9) for c in cols) + "  pending-artifacts")
    for r in manifest["runs"]:
        f = parse_facts(scratch, r["install"], r["pin"])
        print(r["id"].ljust(24) + " ".join(str(f[c]).rjust(9) for c in cols) + "  " + str(f["runner_has_pending_artifacts"]))


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "key":
        k = build_key(argv[1], argv[2], argv[3])
        print(json.dumps(k, indent=1, sort_keys=True))
        return
    if argv and argv[0] == "report-score":
        key = json.load(open(argv[1]))
        print(json.dumps(score_report(key, open(argv[2]).read()), indent=1, sort_keys=True))
        return
    if argv and argv[0] == "smoke":
        ap = argparse.ArgumentParser(prog="doc_score.py smoke")
        ap.add_argument("manifest_dir"); ap.add_argument("--project", default=None)
        a = ap.parse_args(argv[1:])
        return smoke(a.manifest_dir, a.project)
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("repo"); ap.add_argument("base"); ap.add_argument("pin")
    ap.add_argument("--final"); ap.add_argument("--task-done", choices=["true", "false"]); ap.add_argument("--measured")
    a = ap.parse_args(argv)
    final = open(a.final).read() if a.final else ""
    td = None if a.task_done is None else a.task_done == "true"
    print(json.dumps(score_run(a.repo, a.base, a.pin, final, td, json.loads(a.measured) if a.measured else None), indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
