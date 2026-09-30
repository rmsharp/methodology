"""Process-rigor indicators for a real-project run, read from the transcript (what the session DID, not what it said).

    python3 rigor_score.py pilot/real-3.7/rows.jsonl

Indicators (each True/False; none judges whether the fix is correct):
  full_suite     a Bash command ran the whole R test directory (test_dir / test_local / devtools::test)
  pkg_check      R CMD check / devtools::check was run
  lint           lintr was run
  red_observed   a test command ran after the first edit to a test file and before the first edit to R/ code
                 (True also when no R/ edit happened, if a test ran after the test edit)
  handoff_graded the session wrote an evaluation of its predecessor's handoff
  learning       PROJECT_LEARNINGS.md was written
  receipt_done   a handoff receipt with `status: complete` was written (v3.6+ only: v3.0 has no receipt)
  source_fix     R/getPedMaxAge.R was changed (the real fix changed it; a test-only fix is another valid route)
"""
import json, re, sys
import replaylib as L

TEST_CMD = re.compile(r"test_file|test_dir|test_local|testthat::|devtools::test")
FULL = re.compile(r"test_dir|test_local|devtools::test\(")


def indicators(row):
    ev = L.events(L.load_records(row["transcript"]))
    tu = [(i, e) for i, e in enumerate(ev) if e["kind"] == "tool_use"]
    cmds = [(i, e["input"].get("command", "")) for i, e in tu if e["name"] == "Bash"]
    writes = [(i, e["input"].get("file_path", "")) for i, e in tu if e["name"] in ("Edit", "Write")]
    t_edit = next((i for i, p in writes if "/tests/testthat/" in p), None)
    r_edit = next((i for i, p in writes if "/R/" in p), None)
    if r_edit is None:  # a Bash-made source edit
        r_edit = next((i for i, c in cmds if "R/getPedMaxAge.R" in c and re.search(r"write\(|sed -i|cat\s*>", c)), None)
    red = None
    if t_edit is not None:
        end = r_edit if r_edit is not None else len(ev)
        red = any(TEST_CMD.search(c) for i, c in cmds if t_edit < i < end)
    blob = " ".join(c for _, c in cmds) + " ".join(json.dumps(e["input"]) for _, e in tu if e["name"] in ("Edit", "Write"))
    return {"full_suite": any(FULL.search(c) for _, c in cmds),
            "pkg_check": any(re.search(r"R CMD check|devtools::check|rcmdcheck", c) for _, c in cmds),
            "lint": any("lintr" in c for _, c in cmds),
            "red_observed": red,
            "handoff_graded": bool(re.search(r"Handoff Evaluation|Evaluation of S313|predecessor_score|S313 handoff", blob, re.I)),
            "learning": "PROJECT_LEARNINGS" in blob,
            "receipt_done": bool(re.search(r"status: complete", blob)),
            "source_fix": "R/getPedMaxAge.R" in row["real"]["changed_files"]}


if __name__ == "__main__":
    rows = {}
    for l in open(sys.argv[1]):
        r = json.loads(l); rows[(r["arm"], r["rep"])] = r
    keys = [k for k in sorted(rows) if k[0] in ("v3.7", "v3.0") and rows[k].get("complete")]
    cols = ["full_suite", "pkg_check", "lint", "red_observed", "handoff_graded", "learning", "receipt_done", "source_fix"]
    print("run      " + " ".join(f"{c[:11]:11}" for c in cols))
    for k in keys:
        if (k[0] == "v3.0" and k[1] == 2) or rows[k]["real"]["commits_after_base"] < 3 and k != ("v3.7", 5):
            continue
        ind = indicators(rows[k])
        print(f"{k[0]}-r{k[1]:<3} " + " ".join(f"{str(ind[c]):11}" for c in cols))
