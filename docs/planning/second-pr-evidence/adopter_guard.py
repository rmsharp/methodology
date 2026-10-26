"""Run the trimmer's dry run over every adopter's ledgers in --no-local clones (clean HEAD), then with one
synthetic front-matter edit, then read-only over the live trees. Reports the guard's code and any crash."""
import os, re, shutil, subprocess, sys, pathlib
trim, scratch = sys.argv[1], pathlib.Path(sys.argv[2])
dev = pathlib.Path.home() / "Development"
names = ["airqino", "chat_verification", "church_growth", "claude_work", "dalia_martinez_funeral",
         "feedback-loop-comparison", "model_project_constructor", "mts-system", "nprcgenekeepr",
         "Philippians", "vscode_quarto_ext", "wsfct"]
CODE = "FRONTIER_FRONT_MATTER_UNCOMMITTED"
def run(cwd, rel):
    p = subprocess.run([sys.executable, "-I", trim, "--file", rel, "--cut", "3", "--today", "2026-10-26"],
                       cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    codes = re.findall(r"^\s*\[([A-Z0-9_]+)\]", p.stdout, re.M)
    return p.returncode, codes, p.stdout
def ledgers(root):
    for led in ("SESSION_NOTES.md", "CHANGELOG.md", "HANDOFFS.md"):
        for sub in ("", "methodology/"):
            if (root / (sub + led)).is_file():
                yield sub + led; break
tot = dict(files=0, clean_fire=0, crash=0, reached=0, syn_fire=0, syn_reached=0, live_fire=0)
for n in names:
    src = dev / n
    if not src.is_dir():
        print("%-26s (no such directory)" % n); continue
    dst = scratch / n; shutil.rmtree(dst, ignore_errors=True)
    subprocess.run(["git", "clone", "--no-local", "-q", str(src), str(dst)], check=True)
    for rel in ledgers(dst):
        tot["files"] += 1
        rc, codes, out = run(dst, rel)
        crash = "Traceback" in out
        tot["crash"] += crash
        reached = any(c in codes for c in ("DRY_RUN", "WOULD_WRITE")) or "DRY_RUN" in codes
        fire = CODE in codes
        tot["clean_fire"] += fire; tot["reached"] += reached
        # synthetic edit: change the first non-blank line of the front matter (the title)
        f = dst / rel; t = f.read_text(encoding="utf-8")
        lines = t.split("\n"); i = next(k for k, l in enumerate(lines) if l.strip())
        lines[i] = lines[i] + " (synthetic edit)"; f.write_text("\n".join(lines), encoding="utf-8")
        rc2, codes2, out2 = run(dst, rel)
        syn = CODE in codes2; synr = "DRY_RUN" in codes2
        tot["syn_fire"] += syn; tot["syn_reached"] += synr; tot["crash"] += ("Traceback" in out2)
        subprocess.run(["git", "checkout", "-q", "--", rel], cwd=str(dst))
        # live tree, read-only: porcelain before == after
        live = src
        before = subprocess.run(["git", "status", "--porcelain"], cwd=str(live), stdout=subprocess.PIPE, text=True).stdout
        rc3, codes3, out3 = run(live, rel)
        after = subprocess.run(["git", "status", "--porcelain"], cwd=str(live), stdout=subprocess.PIPE, text=True).stdout
        assert before == after, "a dry run changed %s" % live
        tot["live_fire"] += CODE in codes3
        print("%-26s %-28s clean: rc=%d reached=%-5s fire=%-5s | synthetic: reached=%-5s fire=%-5s | live: fire=%s%s"
              % (n, rel, rc, reached, fire, synr, syn, CODE in codes3, " | CRASH" if crash else ""))
print(tot)
