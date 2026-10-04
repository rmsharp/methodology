#!/usr/bin/env python3
"""The M3 task search (BL-94 P2a (e); plan section 3.4): is there a task in the project's history whose honest completion makes at least
two live documents false, and that those documents are demonstrably read?

    python3 m3_search.py [--project PATH] [--out FILE]

The only kind of "removed thing" searched for is a function: a commit that deletes a top-level `name <- function` from R/ and defines it
nowhere else in the same commit. For each, the live documents at the commit's PARENT (doc_score.classify_path == "live") that name it as a
whole word are listed, with whether the commit itself changed them (so the real fix is the answer key for what had to be updated) and
whether the mention is one a tool must parse:

  * `chunk`   inside a ```{r} code chunk of a vignette or README.Rmd, which `R CMD build` / `rmarkdown::render` run, so a removed
              function is an error and the document is demonstrably read;
  * `pkgdown` in the pkgdown config, which pkgdown parses (the project's own commit d14cd913d is the precedent for "read by the tool");
  * `agent`   in CLAUDE.md, which every session of the project reads;
  * `prose`   anything else in a live file. NOT demonstrably read.
NEWS* is live by the plan's classification, but a NEWS entry naming a function that was later removed is history and stays true, so a
NEWS mention is counted apart ("news") and never makes a candidate.

A STRONG candidate has at least two `chunk`, `pkgdown` or `agent` documents at the parent that the commit also changed. The search is
mechanical and has blind spots, named in the output: removed arguments, renamed files, options and config keys are not searched, and
a function removed over several commits is seen at each, not as one task. It finds or fails to find a candidate; it does not build the
task, which would be a different start state with its own harness, runs and cost.
"""
import argparse, json, os, re, subprocess, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doc_score

DEFAULT_PROJECT = os.path.expanduser("~/Development/nprcgenekeepr")
DEF = re.compile(r"^([A-Za-z_.][A-Za-z0-9_.]*)\s*(?:<-|=)\s*function\b")
DOC_PATHSPEC = ["README*", "NEWS*", "CLAUDE.md", "_pkgdown.yml", "pkgdown", "vignettes"]
MIN_NAME = 5          # shorter names ("x", "get") match prose


def git(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True, errors="replace").stdout


def removed_functions(repo):
    """{commit: (parent, [names])} for every commit that removes a top-level function definition from R/ and does not define it again."""
    p = subprocess.Popen(["git", "-C", repo, "log", "--no-merges", "-p", "-U0", "--no-renames", "--format=\x01%H %P", "--", "R/"],
                         stdout=subprocess.PIPE, text=True, errors="replace")
    out, cur, gone, came = {}, None, set(), set()

    def flush():
        if cur and cur[1]:
            names = sorted(n for n in gone - came if len(n) >= MIN_NAME)
            if names:
                out[cur[0]] = (cur[1], names)
    for line in p.stdout:
        if line.startswith("\x01"):
            flush()
            parts = line[1:].split()
            cur = (parts[0], parts[1] if len(parts) > 1 else None)
            gone, came = set(), set()
        elif line.startswith("-") and not line.startswith("---"):
            m = DEF.match(line[1:])
            if m:
                gone.add(m.group(1))
        elif line.startswith("+") and not line.startswith("+++"):
            m = DEF.match(line[1:])
            if m:
                came.add(m.group(1))
    flush()
    p.wait()
    return out


def mention_kinds(repo, rev, path, name):
    """How `name` appears in `path` at `rev`: the set of kinds among chunk / pkgdown / agent / prose."""
    text = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True, text=True, errors="replace").stdout
    word = re.compile(r"(?<![\w.])" + re.escape(name) + r"(?![\w.])")
    base = os.path.basename(path)
    kinds, in_chunk, in_fence = set(), False, False
    for line in text.splitlines():
        if re.match(r"^\s*```\{r", line):
            in_fence, in_chunk = True, not re.search(r"eval\s*=\s*(FALSE|F)\b", line)     # a chunk with eval = FALSE is shown, never run
            continue
        if in_fence and line.strip().startswith("```"):
            in_fence = in_chunk = False
            continue
        if not word.search(line):
            continue
        if base.startswith("NEWS"):
            kinds.add("news")
        elif base in ("_pkgdown.yml",) or "pkgdown" in path:
            kinds.add("pkgdown")
        elif base == "CLAUDE.md":
            kinds.add("agent")
        elif in_chunk and not line.lstrip().startswith("#") and (path.startswith("vignettes/") or base.startswith("README")) and path.lower().endswith(".rmd"):
            kinds.add("chunk")             # an R comment inside a chunk is text, not code
        else:
            kinds.add("prose")
    return kinds


def candidates(repo, funcs):
    rows = []
    for c, (parent, names) in funcs.items():
        changed = set(git(repo, "diff", "--name-only", "--no-renames", parent, c).split("\n")) - {""}
        for name in names:
            hits = [h.split(":", 1)[1] for h in git(repo, "grep", "-l", "-w", "-F", "-e", name, parent, "--", *DOC_PATHSPEC).split("\n") if ":" in h]
            live = [h for h in hits if doc_score.classify_path(h) == "live"]
            if not live:
                continue
            docs = []
            for h in sorted(set(live)):
                k = mention_kinds(repo, parent, h, name)
                if k:
                    docs.append({"path": h, "kinds": sorted(k), "changed_by_commit": h in changed})
            if docs:
                strong = [d for d in docs if set(d["kinds"]) & {"chunk", "pkgdown", "agent"} and d["changed_by_commit"]]
                rows.append({"commit": c, "parent": parent, "name": name, "docs": docs, "strong_docs": len(strong),
                             "subject": git(repo, "log", "-1", "--format=%s", c).strip(), "date": git(repo, "log", "-1", "--format=%cs", c).strip()})
    return rows


def exports_named_in_live_docs(repo, rev):
    """The constructed-task scan: exported functions at `rev` that at least two live documents name where a tool must parse them (an
    executed chunk, the pkgdown config) or an agent reads them (CLAUDE.md). A rename of one of these would honestly make those
    documents false. It says nothing about whether such a task is a good one; that is a design decision, not a search result."""
    ns = subprocess.run(["git", "-C", repo, "show", f"{rev}:NAMESPACE"], capture_output=True, text=True, errors="replace").stdout
    names = sorted({m.group(1) for m in re.finditer(r"^export\(([A-Za-z_.][A-Za-z0-9_.]*)\)", ns, re.M) if len(m.group(1)) >= MIN_NAME})
    rows = []
    for name in names:
        hits = [h.split(":", 1)[1] for h in git(repo, "grep", "-l", "-w", "-F", "-e", name, rev, "--", *DOC_PATHSPEC).split("\n") if ":" in h]
        docs = []
        for h in sorted(set(hits)):
            if doc_score.classify_path(h) != "live":
                continue
            k = mention_kinds(repo, rev, h, name) & {"chunk", "pkgdown", "agent"}
            if k:
                docs.append({"path": h, "kinds": sorted(k)})
        if len(docs) >= 2:
            rows.append({"name": name, "docs": docs})
    return {"rev": rev, "exports": len(names), "named_in_two_or_more": rows}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--project", default=DEFAULT_PROJECT)
    ap.add_argument("--start", default="879503cce", help="the start state the constructed-task scan reads (plan 3.2)")
    ap.add_argument("--out", default=os.path.join(HERE, "pilot", "doc-evidence", "p2a-m3-search.json"))
    a = ap.parse_args(argv)
    funcs = removed_functions(a.project)
    rows = candidates(a.project, funcs)
    strong = [r for r in rows if r["strong_docs"] >= 2]
    built = exports_named_in_live_docs(a.project, a.start)
    result = {"project": a.project, "head": git(a.project, "rev-parse", "HEAD").strip(), "commits_with_a_removed_function": len(funcs),
              "removed_function_names": sum(len(v[1]) for v in funcs.values()), "names_in_a_live_doc": len(rows), "strong_candidates": strong,
              "candidates_with_one_strong_doc": [r for r in rows if r["strong_docs"] == 1], "constructed_task_scan": built, "all": rows,
              "blind_spots": ["removed arguments, renamed files, options and config keys are not searched", "a function removed across several commits appears at each",
                              "a mention in a code chunk is not shown to be executed (eval = FALSE is not parsed)", "NEWS mentions are counted apart: history stays true"]}
    with open(a.out, "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
        f.write("\n")
    print(f"{len(funcs)} commits remove a function; {result['removed_function_names']} names; {len(rows)} named in a live document; "
          f"{len(strong)} strong candidates (>= 2 parsed-or-agent documents the commit also changed)")
    print(f"at {built['rev']}: {built['exports']} exports; {len(built['named_in_two_or_more'])} named in two or more parsed-or-agent live documents")
    for r in built["named_in_two_or_more"][:15]:
        print(f"  {r['name']}: " + "; ".join(f"{d['path']} ({','.join(d['kinds'])})" for d in r["docs"]))
    for r in strong:
        print(f"  {r['date']} {r['commit'][:9]} {r['name']}: {r['subject'][:70]}")
        for d in r["docs"]:
            print(f"      {d['path']}  {','.join(d['kinds'])}{'  (changed)' if d['changed_by_commit'] else ''}")
    return result


if __name__ == "__main__":
    main()
