"""Read a Claude Code session transcript (JSONL) into a flat event list and a usage total.

Facts about the format this relies on (checked against real local transcripts, CLI 2.1.267):
  * one API message is written as SEVERAL 'assistant' records (one per content block) that
    share message.id and repeat message.usage -- usage must be counted once per message.id;
  * a human turn is a 'user' record whose content is a string, or a list holding a text block
    and no tool_result block; tool results also arrive as 'user' records.
"""
import json, re
from datetime import datetime

SOURCE_EDIT_TOOLS = {"Edit", "Write", "NotebookEdit", "MultiEdit"}


def _ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None


def load_records(path):
    out = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except ValueError:
                    pass  # a torn last line from a killed session
    return out


def events(records):
    """Ordered events: {kind: human|text|tool_use, ts, ...}. Sidechain (subagent) records are skipped."""
    ev, seen_blocks = [], set()
    for r in records:
        if r.get("isSidechain") is True:
            continue
        t, msg, ts = r.get("type"), r.get("message") or {}, _ts(r.get("timestamp"))
        content = msg.get("content")
        if t == "user":
            if isinstance(content, str):
                ev.append({"kind": "human", "ts": ts, "text": content})
            elif isinstance(content, list) and not any(b.get("type") == "tool_result" for b in content):
                txt = " ".join(b.get("text", "") for b in content if b.get("type") == "text")
                if txt:
                    ev.append({"kind": "human", "ts": ts, "text": txt})
        elif t == "assistant" and isinstance(content, list):
            for b in content:
                key = (r.get("uuid"), b.get("id") or b.get("type"))
                if key in seen_blocks:
                    continue
                seen_blocks.add(key)
                if b.get("type") == "text":
                    ev.append({"kind": "text", "ts": ts, "text": b.get("text", "")})
                elif b.get("type") == "tool_use":
                    ev.append({"kind": "tool_use", "ts": ts, "name": b.get("name"), "input": b.get("input") or {}})
    return ev


def usage_total(records):
    """Sum usage once per API message id. Returns dict incl. request count and model."""
    by_id, model = {}, None
    for r in records:
        if r.get("type") != "assistant" or r.get("isSidechain") is True:
            continue
        m = r.get("message") or {}
        if m.get("id") and m.get("usage"):
            by_id[m["id"]] = m["usage"]
            model = model or m.get("model")
    tot = {"requests": len(by_id), "input": 0, "output": 0, "cache_read": 0, "cache_write": 0, "model": model}
    for u in by_id.values():
        tot["input"] += u.get("input_tokens", 0)
        tot["output"] += u.get("output_tokens", 0)
        tot["cache_read"] += u.get("cache_read_input_tokens", 0)
        tot["cache_write"] += u.get("cache_creation_input_tokens", 0)
    return tot


BASH_WRITE = [re.compile(p) for p in (
    r"sed\s+-i[^\n;&|]*textkit\.py",                 # sed -i ... textkit.py
    r">>?\s*\S*textkit\.py",                          # redirect into it
    r"\btee\b[^\n]*textkit\.py",
)]
PY_PATH_VAR = re.compile(r"(\w+)\s*=\s*['\"][^'\"]*textkit\.py['\"]")  # p='textkit.py'
PY_WRITE = r"open\(\s*(%s|['\"][^'\"]*textkit\.py['\"])\s*,\s*['\"][wa]"


def is_source_edit(e, source_names=("textkit.py",)):
    if e["kind"] == "tool_use" and e["name"] == "Bash":
        # Found at the P2 pilot: a session may edit the source with a Bash heredoc, which the tool-name test misses.
        cmd = e["input"].get("command", "")
        if any(p.search(cmd) for p in BASH_WRITE):
            return True
        v = PY_PATH_VAR.search(cmd)  # python that names the file in a variable and later opens that variable to write
        return bool(v and re.search(PY_WRITE % re.escape(v.group(1)), cmd))
    if e["kind"] != "tool_use" or e["name"] not in SOURCE_EDIT_TOOLS:
        return False
    path = e["input"].get("file_path") or e["input"].get("path") or ""
    return any(path.endswith(n) for n in source_names)


def is_test_run(e):
    if e["kind"] != "tool_use" or e["name"] != "Bash":
        return False
    cmd = e["input"].get("command", "")
    return any(k in cmd for k in ("unittest", "pytest", "tests/"))
