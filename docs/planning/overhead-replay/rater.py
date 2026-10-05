#!/usr/bin/env python3
"""M5, the blind rater, and the packet for the operator's own blind rating (BL-94 P2a (d); plan section 2.3 M5, section 4 items 3 and 4, D5).

    python3 rater.py defects  [--out DIR]                        # $0: write the planted-defect set, and check each defect removed its evidence
    python3 rater.py packet   [--out DIR] [--seed N]             # $0: the operator's blind packet, score sheet and (separate) key
    python3 rater.py dry-run  --call-cap 0.75 --total-cap 100    # PAID: the rater on the planted-defect set; P2, not P2a
    python3 rater.py score-human SHEET.csv KEY.json              # $0: his sheet scored against the key

What the rater sees: ONE record, rendered as neutral "Document n" blocks (no file names, no run id, no arm) plus the session's final
message, and nothing else: no tools, no repository, an empty working directory. It answers the fixed yes / no / cannot-tell list below
and then guesses which of three protocol versions wrote the record. Each record is rated twice, the question list in opposite order,
so an order effect shows as a disagreement. It is the writers' model family; that is stated beside every M5 figure (plan 4 item 3).

The planted-defect set is the rater's validity check, made mechanically from an honest record (no model): `missing` drops the next-step
parts, `wrong` replaces them with a statement that contradicts the rest, `vague` replaces every path, anchor and sha with a generic word,
`fabricated` swaps the shas for invented ones. A defective record must score LOWER than its honest original on the questions it was built
to break. `fabricated` is the exception: a sha cannot be checked from the text alone (M1 does that against git), so it is reported and
not required. A rater that cannot rank a record with no next step below one with a next step is not measuring usefulness.

The packet is the same rendering the model sees, so the two sets of ratings are comparable. His six records are drawn with a fixed seed,
stratified 2 / 2 / 2 across v3.0, v3.7 and v3.8-text; the key that says which record is which is a SEPARATE file.
"""
import argparse, collections, csv, hashlib, json, os, random, re, shutil, subprocess, sys, tempfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doc_evidence, doc_score, driver, p1b_score, probe

EVIDENCE = os.path.join(doc_evidence.PILOT, "doc-evidence")
OUT = os.path.join(doc_evidence.PILOT, "doc-probe")
SCORES = os.path.join(EVIDENCE, "p1b-scores.json")

QUESTIONS = [
    ("next_step", "Does the record state a next step specific enough that a successor could start it without first reading the code?"),
    ("where", "Does it say where the next work begins, by naming at least one file, function or location?"),
    ("state", "Does it say unambiguously whether the session's task is finished, partly finished or not started?"),
    ("evidence", "Does it say what was checked (a test run, a command, a count) and what the result was?"),
    ("hazard", "Does it warn of at least one specific pitfall a successor could hit?"),
    ("commits", "Does it identify the commits this session made, by hash or by subject?"),
    ("consistent", "Is the record free of statements that contradict one another?"),
    ("loose_ends", "Does it say whether anything was left uncommitted, pending or unrecorded?"),
]
KEYS = [k for k, _ in QUESTIONS]
ANSWERS = ("yes", "no", "cannot_tell")
ARM_CHOICES = ("3.0", "3.7", "3.8", "cannot_tell")
GROUP_LABEL = {"v3.0": "3.0", "v3.7": "3.7", "v3.8-text": "3.8"}
STRATA = {"v3.0": 2, "v3.7": 2, "v3.8-text": 2}            # six: his choice at the S258 picker (the plan said about ten; ten was 168 minutes of reading)
SEED = 20261004
# A next-step paragraph starts with one of these. This is wider than the scorer's PART_LABEL on purpose: S259 found `**=> SUGGESTED NEXT.**` in
# all three real records and the scorer's set (which this copied) does not name it. "Gotchas for next session" and a mid-sentence "next steps"
# are not labels. A body separated from its label by a blank line is not removed (none of the real records has one; see `defect_check`).
NEXT_LABEL = re.compile(r"(?i)^\W*(?:(?:suggested|recommended|natural)\s+next\b|next[ _]steps?\b|what.s next\b|next session\b|next up\b|next task\b|next action\b)")
# What `check` reports beside a `missing` defect: any other line that still says "next steps" and the like. Informational, never a refusal.
NEXT_CUE = re.compile(r"(?i)\b(?:suggested|recommended|natural) next\b|\bnext[ _]steps?\b|\bwhat.s next\b|\bnext up\b|\bnext task\b|\bnext action\b")
SYSTEM = ("You are a careful reader. You are shown one document: the text that one working session added to a software project's own "
          "records. You have no tools and no access to the project. Judge only from the text. Reply with one JSON object and nothing else.")
NEW_NEXT = "Next: start the task from the beginning; nothing described above has been done yet."


# ---- the record, rendered neutrally -----------------------------------------------------------------------------------------------
def record_docs(rec, final_message=""):
    """{docs: [[line, ...], ...], final: [line, ...]} from doc_score.record(): the added lines per record file in path order (blank lines
    kept so a paragraph can end), and the final message. File names are dropped here and never reach the rater."""
    docs = [list(lines) for _, lines in sorted(rec["raw"].items()) if any(lines)]
    return {"docs": docs, "final": [l.rstrip() for l in (final_message or "").splitlines()]}


def render(rd):
    out = []
    for i, lines in enumerate(rd["docs"], 1):
        out.append(f"=== Document {i} (text added by the session) ===")
        out.extend(lines)
        out.append("")
    if any(l.strip() for l in rd["final"]):
        out.append("=== The session's final message ===")
        out.extend(rd["final"])
    return "\n".join(out).strip() + "\n"


# ---- planted defects (mechanical, no model) ----------------------------------------------------------------------------------------
HEADING = re.compile(r"^#{1,6}\s")      # a markdown heading: `#28/#12` (an issue list) is not one, though doc_score._parts treats any leading `#` as one


def drop_parts(lines, replacement=None, ends=None):
    """Remove every paragraph whose first line is a next-step label. Like doc_score._parts a paragraph runs from its label to a blank line, a
    heading, a fence or the next receipt field, and a one-line field (`next_steps: ...`) is its own paragraph; unlike it, only `#` followed by a
    space is a heading (S260: a line that opens with `#28/#12/...` ended a block early and left half of it in the record). `replacement` (a line)
    is put where the first one was. `ends`, if given, collects the first line KEPT after each removed block (None at the end of the text), so the
    boundary every removal stopped at can be read."""
    out, skipping, placed = [], False, False
    for line in lines:
        if NEXT_LABEL.match(line):
            skipping = True
            if replacement and not placed:
                out.append(replacement)
                placed = True
            continue
        if skipping:
            if not line.strip() or HEADING.match(line) or line.startswith("```") or doc_score.RECEIPT_FIELD_LINE.match(line):
                skipping = False
                if ends is not None:
                    ends.append(line)
            else:
                continue
        out.append(line)
    if skipping and ends is not None:
        ends.append(None)
    return out, placed


def _map(rd, fn_lines):
    return {"docs": [fn_lines(l) for l in rd["docs"]], "final": fn_lines(rd["final"])}


# ---- units: a hard-wrapped paragraph is one thing -----------------------------------------------------------------------------------
UNIT_START = re.compile(r"^\s*(?:[-*+]\s|\d+[.)]\s|#{1,6}\s|```)")     # a list item, a heading or a fence line opens a unit


def units(lines):
    """`lines` grouped into units: a paragraph, a list item, a heading or a receipt field together with the hard-wrapped lines that continue it.
    A blank line and a fence line are each a unit of their own. S262: the builders worked one line at a time, so a backtick span or a sentence
    that wrapped onto the next line was cut in two, and the odd backtick paired every later span on its line the wrong way (the R1-r2 `vague`
    variant read `codeis.nathe`, with `is.na` left standing)."""
    out, cur = [], []
    for line in lines:
        opens = (not line.strip() or UNIT_START.match(line) or doc_score.RECEIPT_FIELD_LINE.match(line)
                 or (cur and (not cur[0].strip() or cur[0].lstrip().startswith("```"))))
        if cur and opens:
            out.append(cur)
            cur = []
        cur.append(line)
    return out + [cur] if cur else out


def _body(line):
    """(label, rest): a receipt field's name (`key_files: `) is a label and not a place, so it is set apart before anything is found or replaced."""
    m = doc_score.RECEIPT_FIELD_LINE.match(line)
    return (line[:m.end()], line[m.end():]) if m else ("", line)


def unit_text(unit):
    """(label, text): a unit's receipt-field label, and its lines joined by newlines with the label taken off the first."""
    label, first = _body(unit[0])
    return label, "\n".join([first] + unit[1:])


def per_unit(lines, fn):
    """`fn(text) -> text` applied to every unit of `lines`; the label stays and is never seen by `fn`. A unit `fn` empties is dropped, label and
    all; a blank line stays as it is."""
    out = []
    for unit in units(lines):
        if not unit[0].strip():
            out.extend(unit)
            continue
        label, text = unit_text(unit)
        text = fn(text)
        if text.strip():
            out.extend((label + text).split("\n"))
    return out


# ---- a sentence that states a pending action ----------------------------------------------------------------------------------------
SENT_END = re.compile(r"[.!?][)\]\"'*_]*(?=\s|$)\s*")                         # a stop before a space; `x.R:24`, `0.5` and `R/y.R` do not end one
# What the records say when something is left to do. S261: the rater answered yes to `next_step` on every `missing` variant because a pending
# action stood as status, in every record ("#121 is NOT closed; run `gh issue close 121`", "still needs closing", "left alone", "Deferred").
# These cues were fitted to the sentences of the three honest-set records read at S262; a fourth record may say it another way, which is what
# `residue_pending` is for. A bare "decide", "must", "should" or "leave ... alone" is guidance or a hazard, not a pending action, and is not here.
PENDING = re.compile(r"(?i)\b(?:not (?:yet )?(?:closed|fixed|done|do|acted on|ratcheted|addressed|resolved|attempted)|still (?:open|needs?|to be|remains?)"
                     r"|left (?:\w+ ){0,2}alone|deferred|(?:you|they|we)(?:['’]ll| will)? need to|(?:must|has to|have to|needs? to) be (?:run|closed|done|fixed|decided)"
                     r"|must run|needs? (?:its own|closing|a follow)|decide (?:whether|if)|should decide|owner action|could(?:n['’]t| not) (?:be )?(?:close|push)\w*"
                     r"|nothing could be pushed|impossible here|I left (?:it|that|them)|say the word|if you want|TODO)\b")


def sentences(text):
    """`text` cut after every sentence stop, each piece keeping its trailing space, so that the pieces join back to `text` exactly."""
    out, pos = [], 0
    for m in SENT_END.finditer(text):
        out.append(text[pos:m.end()])
        pos = m.end()
    return out + [text[pos:]] if pos < len(text) else out


def _drop_pending(text):
    """`text` without its pending-action sentences. A removed sentence takes its trailing space, so only the end needs trimming."""
    return "".join(p for p in sentences(text) if not PENDING.search(p)).rstrip()


def drop_pending(lines):
    return per_unit(lines, _drop_pending)


def pending_sentences(lines):
    """Every sentence of `lines` that states a pending action, as the builder sees them."""
    return [s.strip()[:160] for u in units(lines) for s in sentences(unit_text(u)[1]) if PENDING.search(s)]


def defect_missing(rd):
    return _map(rd, lambda lines: drop_pending(drop_parts(lines)[0]))


def defect_wrong(rd):
    out, placed = {"docs": [], "final": None}, False
    for lines in rd["docs"]:
        new, p = drop_parts(lines, NEW_NEXT if not placed else None)
        out["docs"].append(new)
        placed = placed or p
    new, p = drop_parts(rd["final"], NEW_NEXT if not placed else None)
    out["final"] = new if (placed or p) else new + ["", NEW_NEXT]
    return out


def _shaish(tok):
    return bool(re.search(r"[a-f]", tok)) and bool(re.search(r"\d", tok))


def _sub_sha(text, fn):
    return doc_score.SHA_RE.sub(lambda m: fn(m.group(1)) if _shaish(m.group(1)) else m.group(0), text)


# What the `where` question accepts: "naming at least one file, function or location". These are the ways the records name a place in the code,
# one finder per way; `location_tokens` finds them and `defect_vague` removes exactly them, so what the rater is shown has none (S259: the old
# builder removed paths and anchors only, and 273 to 338 backticked spans and 19 to 24 function names per record were left standing; S262: it
# left the issue and ticket references the next steps point at, the document names, "Age-Sex Pyramid", and any span that wrapped onto a second line).
CODE_SPAN = re.compile(r"`[^`]+`")                                         # the records quote code, names, commands and files in backticks; a span may wrap, a unit holds no blank line
CALL = re.compile(r"\b[A-Za-z_][\w.]*\(\)")                                  # getPedMaxAge(), obj.method()
QUALIFIED = re.compile(r"\b\w+::\w+")                                       # pkg::fn
CAMEL = re.compile(r"\b[a-z][a-z0-9]*(?:[A-Z][a-z0-9]*)+\b")                # getPedMaxAge, qcStudbook
SNAKE = re.compile(r"\b[a-z][a-z0-9]*(?:_[a-z0-9]+)+\b")                    # spell_check_package (a receipt's own field names are labels, see `_body`)
LINE_REF = re.compile(r"(?:[Ll]ines?\s+|L)\d+(?:\s?[-\u2013/]\s?L?\d+)*\b|\u00a7\s?\d+(?:\.\d+)*")     # line 24, L512/L763-765, section sign 11
DOTTED = re.compile(r"\b[a-z]{2,}(?:\.[a-z]{2,})+\b")                         # is.na, data.frame (a number has no letters; "e.g" has one)
DOC_NAMES = ("NEWS", "CHANGELOG", "README", "ROADMAP", "BACKLOG", "HANDOFFS", "SAFEGUARDS", "CLAUDE", "LICENSE")
UPPER_NAME = re.compile(r"\b(?:[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+|%s)\b" % "|".join(DOC_NAMES))   # SESSION_RUNNER, NOT_CRAN, NEWS; RED, DONE, NOT and TDD are emphasis
HYPHEN_TITLE = re.compile(r"\b[A-Z][a-z]+(?:-[A-Z][a-z]+)+(?:\s+[A-Z][a-z]+)*\b")  # Age-Sex Pyramid: a screen or tab named in title case
ISSUE_REF = re.compile(r"(?<![\w&])#\d+\b")                                   # #121: where the next work begins, to anyone who reads the tracker
TICKET = re.compile(r"\b[A-Z]\d{1,2}\b")                                      # E4, D6; S313 (a session number) has three digits and stays
LOCATION_FINDERS = (CODE_SPAN, doc_score.ANCHOR_RE, doc_score.PATH_RE, CALL, QUALIFIED, CAMEL, SNAKE, DOTTED, UPPER_NAME, HYPHEN_TITLE, LINE_REF, ISSUE_REF, TICKET)
GENERIC = ("the relevant place", "the relevant file", "the relevant code", "the relevant name")


def location_tokens(lines):
    """Every place-in-the-code token in `lines`, each character counted once: the finders run in the order above and a match that overlaps an
    earlier one is skipped, so a function name inside a backticked span is one token and not three. One unit at a time, so a token that wraps
    onto the next line is one token."""
    found = []
    for unit in units(lines):
        text = unit_text(unit)[1]
        taken = []
        for rx in LOCATION_FINDERS:
            for m in rx.finditer(text):
                if not any(m.start() < e and s < m.end() for s, e in taken):
                    taken.append((m.start(), m.end()))
                    found.append(m.group(0))
    return found


def _vague_text(text):
    text = doc_score.ANCHOR_RE.sub("the relevant place", text)
    text = doc_score.PATH_RE.sub("the relevant file", text)
    text = CODE_SPAN.sub(lambda m: m.group(0)[1:-1] if m.group(0)[1:-1] in GENERIC else "the relevant code", text)    # a span that was only a path is unwrapped
    for rx in (CALL, QUALIFIED, CAMEL, SNAKE, DOTTED, UPPER_NAME):
        text = rx.sub("the relevant name", text)
    text = HYPHEN_TITLE.sub("the relevant place", text)
    text = LINE_REF.sub("the relevant place", text)
    for rx in (ISSUE_REF, TICKET):
        text = rx.sub("the relevant issue", text)
    return _sub_sha(text, lambda s: "the commit")


def defect_vague(rd):
    return _map(rd, lambda lines: per_unit(lines, _vague_text))


def defect_fabricated(rd):
    fake = lambda s: hashlib.sha1(("fabricated:" + s).encode()).hexdigest()[:len(s)]
    return _map(rd, lambda lines: [_sub_sha(l, fake) for l in lines])


# name -> (builder, the questions it is built to break: it is CAUGHT when any of them goes from yes to not yes; none = reported only).
# `vague` targets `where` alone: the commits question accepts a subject, which the defect leaves in place.
DEFECTS = {"missing": (defect_missing, ["next_step"]), "wrong": (defect_wrong, ["consistent", "state"]),
           "vague": (defect_vague, ["where"]), "fabricated": (defect_fabricated, [])}


def changed(rd, other):
    return render(rd) != render(other)


# ---- the evidence check: did a defect remove what its question rests on? ----------------------------------------------------------------
def record_lines(rd):
    return [l for lines in rd["docs"] for l in lines] + list(rd["final"])


def next_step_labels(rd):
    return [l.strip()[:120] for l in record_lines(rd) if NEXT_LABEL.match(l)]


def next_step_evidence(rd):
    """What the `next_step` question rests on: a labelled next-step paragraph, or a sentence that states a pending action (S262)."""
    return next_step_labels(rd) + pending_sentences(record_lines(rd))


def next_step_cues(rd):
    return [l.strip()[:160] for l in record_lines(rd) if NEXT_CUE.search(l)]


def location_evidence(rd):
    return location_tokens(record_lines(rd))


# What no finder counts, printed beside the check so a pass is not read as a proof (S261: the check passed, the rater still found what it needed).
# Informational, never a refusal: these classes are broader than any builder uses, so they flag ordinary words too, to be read and not obeyed.
PENDING_BROAD = re.compile(r"(?i)\b(?:needs?|must|should|will|remain(?:s|ed)?|pending|follow-?ups?|decide|until|outstanding|unresolved|owner|next)\b")
NAME_CLASSES = (("ALL-CAPS words", re.compile(r"\b[A-Z]{3,}\b")), ("Title-case words inside a sentence", re.compile(r"(?<=[a-z,;:)] )[A-Z][a-z]{2,}\b")),
                ("dotted or slashed names", re.compile(r"\b[a-z]\w*(?:[./][\w-]+)+\b")), ("letter-and-digit ids", re.compile(r"\b[A-Za-z]+\d+[A-Za-z]*\b")))


def residue_pending(rd):
    found = [s.strip()[:120] for u in units(record_lines(rd)) for s in sentences(unit_text(u)[1]) if PENDING_BROAD.search(s)]
    what = "sentences with a broad cue (need, must, should, will, remain, pending, follow-up, decide, until, owner, next)"
    return [{"what": what, "count": len(found), "first": found[:5]}] if found else []


def residue_names(rd):
    text, out = "\n".join(record_lines(rd)), []
    for what, rx in NAME_CLASSES:
        tally = collections.Counter(rx.findall(text))
        if tally:
            out.append({"what": what, "count": len(tally), "first": [f"{t}×{n}" for t, n in tally.most_common(8)]})
    return out


RESIDUE = {"missing": residue_pending, "vague": residue_names}


def next_step_ends(rd):
    """The first line kept after each next-step block removed from the honest record: where each removal stopped, to be read. A finder of labels
    cannot see a body that survives a wrong boundary (S260: it reported `3 -> 0` over a record that still held half of a block)."""
    ends = []
    for lines in rd["docs"] + [rd["final"]]:
        drop_parts(lines, ends=ends)
    return ["<end of the text>" if e is None else e.strip()[:100] for e in ends]


ENDS = {"missing": next_step_ends}
# defect -> (what its finder counts, the finder, informational cues or None)
CHECKS = {"missing": ("next-step labels and pending-action sentences", next_step_evidence, next_step_cues), "vague": ("location tokens", location_evidence, None)}


def defect_check(rd, defects=None):
    """For each defect that has a finder: how much of the evidence its target question rests on the honest record holds (`before`), how much the
    defective one still holds (`after`; the first few are `left`), and, for `missing`, the other lines that still say "next steps" and the like
    (`cue_lines_left`, informational). A defect with after > 0 did not remove what it was built to remove, so a rater that answers yes to its target
    question may be right (S259: both misses were this); `problems_from` turns that into a refusal before any call is paid for. What this proves is
    relative to the finders: a place named in words no finder knows, or a next step implied by a status line, is not counted. S262: `residue` lists
    what the defective record still holds in classes no builder uses, so the report shows that gap instead of only describing it (S261's check passed
    over a `missing` variant that still said "#121 is NOT closed" and a `vague` one that still named `#120`).
    `wrong` and `fabricated` have no finder: the first adds a sentence, the second changes shas that only git can check."""
    out = {}
    for name, (fn, targets) in (defects or DEFECTS).items():
        if name not in CHECKS:
            continue
        what, finder, cues = CHECKS[name]
        made = fn(rd)
        left = finder(made)
        out[name] = {"targets": targets, "evidence": what, "before": len(finder(rd)), "after": len(left), "left": left[:5],
                     "cue_lines_left": cues(made)[:5] if cues else [], "ends": ENDS[name](rd) if name in ENDS else [],
                     "residue": RESIDUE[name](made) if name in RESIDUE else []}
    return out


def problems_from(checks):
    """One string per (record, defect) whose evidence was not removed, from {record id: defect_check(...)}."""
    return [f"{rid}: {name} leaves {c['after']} of {c['before']} {c['evidence']} (first: {c['left'][:3]})"
            for rid, per in checks.items() for name, c in per.items() if c["after"]]


def check_defects(records, defects=None):
    """The problems over the honest set (the records a dry run rates): [] when every defect removed what it was built to remove."""
    return problems_from({rid: defect_check(records[rid][1], defects) for rid in honest_set(records)})


def defects_report(records, defects=None):
    """(lines to print, problems): one line per honest record and defect, its evidence before -> after, LEAVES where that did not reach zero."""
    lines, checks = [], {}
    for rid in honest_set(records):
        checks[rid] = defect_check(records[rid][1], defects)
        for name, c in checks[rid].items():
            lines.append(f"{rid:24} {name:8} {c['evidence']:16} {c['before']} -> {c['after']}" + (f"   LEAVES {c['left'][:3]}" if c["after"] else "")
                         + (f"   ({len(c['cue_lines_left'])} line(s) still mention next steps)" if c["cue_lines_left"] else ""))
            lines += [f"{'':24} {'':8} removal ended at: {e!r}" for e in c["ends"]]
            lines += [f"{'':24} {'':8} still standing, counted by no finder: {r['what']}: {r['count']} (first: {r['first'][:5]})" for r in c["residue"]]
    return lines, problems_from(checks)


# ---- the rating call ----------------------------------------------------------------------------------------------------------------
def prompt(record_text, order="A"):
    qs = QUESTIONS if order == "A" else list(reversed(QUESTIONS))
    lines = [f"{i}. [{k}] {q}" for i, (k, q) in enumerate(qs, 1)]
    form = {"answers": {k: "yes | no | cannot_tell" for k, _ in qs}, "arm_guess": "3.0 | 3.7 | 3.8 | cannot_tell", "reason": "one sentence"}
    return ("The text below is everything one working session added to its project's records, followed by the message it ended on.\n\n"
            "----- BEGIN -----\n" + record_text + "----- END -----\n\n"
            "Answer each question from the text alone. Use cannot_tell only when the text does not let you decide.\n\n" + "\n".join(lines) + "\n\n"
            "Then, last, say which of three versions of a session protocol (called 3.0, 3.7 and 3.8) the author was following, or cannot_tell.\n\n"
            "Reply with one JSON object of exactly this form and nothing else:\n" + json.dumps(form, indent=1) + "\n")


def parse_reply(text):
    """The first JSON object in the reply, validated against the fixed list. Raises ValueError on anything else."""
    m = re.search(r"\{.*\}", text or "", re.S)
    if not m:
        raise ValueError("no JSON object in the reply")
    d = json.loads(m.group(0))
    ans = d.get("answers")
    if not isinstance(ans, dict) or set(ans) != set(KEYS):
        raise ValueError(f"answers must hold exactly {KEYS}")
    bad = {k: v for k, v in ans.items() if v not in ANSWERS}
    if bad:
        raise ValueError(f"answers outside {ANSWERS}: {bad}")
    if d.get("arm_guess") not in ARM_CHOICES:
        raise ValueError(f"arm_guess must be one of {ARM_CHOICES}")
    return {"answers": ans, "arm_guess": d["arm_guess"], "reason": str(d.get("reason", ""))[:300]}


def rater_cmd(model, effort, call_cap):
    return ["claude", "-p", "--model", model, "--effort", effort, "--max-budget-usd", str(call_cap), "--no-session-persistence",
            "--setting-sources", "", "--strict-mcp-config", "--disable-slash-commands", "--tools", "", "--output-format", "json",
            "--system-prompt", SYSTEM]


RAW_KEEP = 20000        # characters of a failed call's text kept: a rating reply is a few hundred, and the results file is committed


def keep(text):
    """A failed call's text, bounded. The cause of a failure is in the text, and the first characters show it."""
    text = "" if text is None else (text if isinstance(text, str) else json.dumps(text))
    return text if len(text) <= RAW_KEEP else text[:RAW_KEEP] + f"\n[cut: {len(text)} characters in all]"


def call_rater(user_prompt, argv, run=subprocess.run):
    """One rating call: the prompt on stdin, an EMPTY working directory, no tools. Returns (parsed or None, cost, error or None, raw or None).
    `raw` is the text that failed, so a failure can be diagnosed afterwards (S259: one of 31 calls cost $0.0635 and left only a parse error's
    position): the CLI's stdout and stderr when it gave no JSON, its envelope on a CLI error, the reply itself when it could not be used. It is
    bounded (`keep`) and is None when the reply was usable."""
    with tempfile.TemporaryDirectory(prefix="rater-") as cwd:
        p = run(argv, input=user_prompt, capture_output=True, text=True, cwd=cwd)
    try:
        env = json.loads(p.stdout)
    except ValueError:
        return None, 0.0, f"no JSON from the CLI (exit {p.returncode}): {(p.stderr or p.stdout)[:200]}", keep((p.stdout or "") + (f"\n[stderr]\n{p.stderr}" if p.stderr else ""))
    cost = float(env.get("total_cost_usd") or 0.0)
    if env.get("is_error") or env.get("subtype", "success") != "success":
        return None, cost, f"CLI error {env.get('subtype')}", keep(p.stdout)
    try:
        return parse_reply(env.get("result")), cost, None, None
    except ValueError as e:
        return None, cost, f"unusable reply: {e}", keep(env.get("result"))


def total(parsed):
    a = parsed["answers"]
    return {"yes": sum(v == "yes" for v in a.values()), "cannot_tell": sum(v == "cannot_tell" for v in a.values()), "of": len(KEYS)}


def planted_check(honest, defects):
    """honest: {question: answer}; defects: {name: {question: answer}}, one question order. A defect is `caught` when any question it
    targets was `yes` in the honest rating and is not `yes` in the defective one; `MISSED` when some targeted question was `yes` and none
    dropped; `not testable` when no targeted question was `yes` to begin with; `reported only` for a defect with no target."""
    out = {}
    for name, (_, targets) in DEFECTS.items():
        if name not in defects:
            continue
        yes = [q for q in targets if honest[q] == "yes"]
        dropped = [q for q in yes if defects[name][q] != "yes"]
        verdict = "reported only" if not targets else ("not testable" if not yes else ("caught" if dropped else "MISSED"))
        out[name] = {"verdict": verdict, "dropped": dropped, "targets": targets}
    return out


def combine_orders(a, b):
    """A defect is `caught` only when it is caught in both question orders; one order only is `order-sensitive`."""
    out = {}
    for name in a:
        va, vb = a[name]["verdict"], b[name]["verdict"]
        out[name] = va if va == vb else ("order-sensitive" if "caught" in (va, vb) else "MISSED" if "MISSED" in (va, vb) else va)
    return out


def summarize_dry_run(results):
    """From dry_run()'s output: per honest record its score, each defect's verdict and score, the two orders' disagreement, the arm
    guess on the honest ratings, and the cost. Pure: it reads the results and nothing else."""
    rows, guesses, cost, failed = {}, [], 0.0, []
    for rid, kinds in results.items():
        ok = lambda kind, order: (kinds.get(kind, {}).get(order) or {}).get("parsed")
        for kind in kinds:
            for order, r in kinds[kind].items():
                cost += r.get("cost_usd") or 0.0
                if not r.get("parsed"):
                    failed.append(f"{rid}/{kind}/{order}: {r.get('error') or r.get('refused')}")
        if not (ok("honest", "A") and ok("honest", "B")):
            rows[rid] = {"honest": "unrated"}
            continue
        h = {o: ok("honest", o)["answers"] for o in "AB"}
        guesses += [(ok("honest", o)["arm_guess"], rid) for o in "AB"]
        per = {}
        for o in "AB":
            per[o] = planted_check(h[o], {k: ok(k, o)["answers"] for k in DEFECTS if ok(k, o)})
        evidence = {}
        for k in DEFECTS:
            c = next((c for c in ((kinds.get(k, {}).get(o) or {}).get("check") for o in "AB") if c), None)
            if c:
                evidence[k] = {f: c[f] for f in ("evidence", "before", "after", "left", "cue_lines_left", "ends", "residue")}
        rows[rid] = {"honest_total": {o: total(ok("honest", o)) for o in "AB"}, "planted_evidence": evidence,
                     "order_disagreement": [q for q in KEYS if h["A"][q] != h["B"][q]],
                     "defects": combine_orders(per["A"], per["B"]) if per["A"] and per["B"] else {},
                     "defect_totals": {k: {o: total(ok(k, o)) for o in "AB" if ok(k, o)} for k in DEFECTS if ok(k, "A") or ok(k, "B")}}
    return {"records": rows, "arm_guesses": guesses, "cost_usd": round(cost, 4), "failed_calls": failed}


# ---- the runs (read from the saved evidence) ---------------------------------------------------------------------------------------
def load_records(evidence=EVIDENCE, scores=SCORES, project=doc_evidence.DEFAULT_PROJECT):
    """{run_id: (group, record_docs)} for every scored run, from the bundle and the saved scores. Nothing is scored again."""
    with open(scores) as f:
        saved = json.load(f)["runs"]
    scratch, manifest = doc_evidence.rebuild(evidence, project)
    out = {}
    try:
        for r in manifest["runs"]:
            s = saved.get(r["id"])
            if not s or not s["included"]:
                continue
            out[r["id"]] = (s["group"], record_docs(doc_score.record(scratch, r["install"], r["pin"]), s["final_message"]))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    return out


def honest_set(records):
    """One honest record per group: the first run id in sorted order, so the dry run's inputs are not chosen after seeing a rating."""
    seen, out = set(), []
    for rid in sorted(records):
        g = records[rid][0]
        if g not in seen:
            seen.add(g)
            out.append(rid)
    return out


# ---- the operator's packet -----------------------------------------------------------------------------------------------------------
def draw_sample(records, seed=SEED, strata=STRATA):
    rng = random.Random(seed)
    chosen = []
    for g, n in strata.items():
        pool = sorted(r for r, (grp, _) in records.items() if grp == g)
        chosen += rng.sample(pool, min(n, len(pool)))
    rng.shuffle(chosen)
    return chosen


def build_packet(records, sample):
    labels = {rid: f"R{i:02d}" for i, rid in enumerate(sample, 1)}
    md = ["# Blind rating packet", "",
          f"{len(sample)} records, each the text one working session added to its project's records plus the message it ended on. Nothing here says which",
          "version of the protocol wrote it or which run it came from. For each record answer the eight questions from the text alone",
          "(yes / no / ?), then guess which of three versions, 3.0, 3.7 or 3.8, was being followed (or ?). Record your answers in `sheet.csv`.",
          "Do not open `KEY-do-not-open-before-rating.json`.", "", "## The questions", ""]
    md += [f"{i}. **{k}** — {q}" for i, (k, q) in enumerate(QUESTIONS, 1)] + [""]
    words = 0
    for rid in sample:
        text = render(records[rid][1])
        words += len(text.split())
        md += [f"\n---\n\n# Record {labels[rid]}\n", text]
    key = {labels[rid]: {"run": rid, "group": records[rid][0], "arm_label": GROUP_LABEL[records[rid][0]]} for rid in sample}
    sheet = [["record", *KEYS, "arm_guess", "notes"]] + [[labels[rid]] + [""] * (len(KEYS) + 2) for rid in sample]
    return "\n".join(md) + "\n", sheet, key, {"records": len(sample), "words": words, "minutes_at_200_wpm": round(words / 200)}


def score_human(sheet_path, key):
    """His sheet against the key: per group, the share of `yes` on each question, and how often his arm guess was right."""
    with open(sheet_path, newline="") as f:
        rows = list(csv.DictReader(f))
    by_group, guesses = {}, []
    for r in rows:
        k = key[r["record"]]
        for q in KEYS:
            v = (r.get(q) or "").strip().lower()
            if v:
                by_group.setdefault(k["group"], {}).setdefault(q, []).append(1 if v in ("y", "yes") else 0)
        g = (r.get("arm_guess") or "").strip()
        if g:
            guesses.append((g, k["arm_label"]))
    return {"yes_share": {g: {q: round(sum(v) / len(v), 3) for q, v in qs.items()} for g, qs in by_group.items()},
            "arm_guess": {"answered": len(guesses), "right": sum(g == a for g, a in guesses), "of": len(rows), "chance": round(1 / 3, 3)}}


# ---- the paid dry run (P2, not P2a) ---------------------------------------------------------------------------------------------------
def dry_run(records, call_cap, total_cap, out=OUT, model="sonnet", effort="high", run=subprocess.run):
    """Rate the honest set and its planted defects, each record in both question orders, one call each. Every call is checked against
    the study's own spend ledger first and written to it after; a refused call ends the run with what it has."""
    checks = {rid: defect_check(records[rid][1]) for rid in honest_set(records)}
    problems = problems_from(checks)
    if problems:                      # S259 paid $1.66 to learn two defects were not defects; this is the same finding at $0
        raise probe.Refused("a planted defect leaves the evidence it was built to remove, so a rating of it would not mean what it says; nothing was sent:\n  "
                            + "\n  ".join(problems))
    os.makedirs(out, exist_ok=True)
    argv = rater_cmd(model, effort, call_cap)
    results = {}
    jobs = []
    for rid in honest_set(records):
        rd = records[rid][1]
        jobs.append((rid, "honest", rd))
        for name, (fn, _) in DEFECTS.items():
            made = fn(rd)
            if changed(rd, made):
                jobs.append((rid, name, made))
    for rid, kind, rd in jobs:
        for order in ("A", "B"):
            try:
                probe.refuse_over_cap(out, call_cap, total_cap)
            except SystemExit as e:
                results.setdefault(rid, {}).setdefault(kind, {})[order] = {"refused": str(e)}
                return results
            parsed, cost, err, raw = call_rater(prompt(render(rd), order), argv, run)
            with open(os.path.join(out, "spend.jsonl"), "a") as f:
                f.write(json.dumps({"kind": "rater", "run": rid, "defect": kind, "order": order, "cost_usd": cost}) + "\n")
            results.setdefault(rid, {}).setdefault(kind, {})[order] = {"parsed": parsed, "cost_usd": cost, "error": err, "raw": raw, "check": checks[rid].get(kind)}
    return results


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("mode", choices=["defects", "packet", "dry-run", "score-human"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--out", default=os.path.join(OUT, "rating"), help="where artifacts are written")
    ap.add_argument("--ledger", default=OUT, help="the study's spend ledger directory (dry-run only)")
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--call-cap", type=float); ap.add_argument("--total-cap", type=float)
    ap.add_argument("--model", default="sonnet"); ap.add_argument("--effort", default="high")
    a = ap.parse_args(argv)
    if a.mode == "score-human":
        with open(a.args[1]) as f:
            print(json.dumps(score_human(a.args[0], json.load(f)), indent=1))
        return
    if a.mode == "dry-run" and (a.call_cap is None or a.total_cap is None):
        ap.error("dry-run is paid: --call-cap and --total-cap are both required")
    records = load_records()
    os.makedirs(a.out, exist_ok=True)
    if a.mode == "defects":
        for rid in honest_set(records):
            rd = records[rid][1]
            for name, (fn, _) in DEFECTS.items():
                made = fn(rd)
                with open(os.path.join(a.out, f"{probe.slug(rid)}.{name}.txt"), "w") as f:
                    f.write(render(made))
                print(f"{rid:24} {name:11} changed={changed(rd, made)}")
        lines, problems = defects_report(records)
        print("\n".join(lines))
        if problems:
            raise SystemExit("a planted defect leaves the evidence it was built to remove:\n  " + "\n  ".join(problems))
    elif a.mode == "packet":
        sample = draw_sample(records, a.seed)
        md, sheet, key, size = build_packet(records, sample)
        open(os.path.join(a.out, "packet.md"), "w").write(md)
        csv.writer(open(os.path.join(a.out, "sheet.csv"), "w", newline="")).writerows(sheet)
        json.dump(key, open(os.path.join(a.out, "KEY-do-not-open-before-rating.json"), "w"), indent=1, sort_keys=True)
        print(json.dumps(size))
    else:
        res = dry_run(records, a.call_cap, a.total_cap, a.ledger, a.model, a.effort)
        json.dump(res, open(os.path.join(a.out, "dry-run.json"), "w"), indent=1, sort_keys=True)
        json.dump(summarize_dry_run(res), open(os.path.join(a.out, "dry-run-summary.json"), "w"), indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
