import subprocess, sys, collections
N = int(sys.argv[1]); mode = sys.argv[2]
res = collections.Counter(); sample = {}
for i in range(N):
    if mode == "plain":
        p = subprocess.run(["bash", "./repro-snippet.sh"], capture_output=True, text=True)
    else:  # the ratchet's launch: a shell, pipes for stdout and stderr, a session of its own
        p = subprocess.Popen("bash ./repro-snippet.sh", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             text=True, start_new_session=True)
        out, err = p.communicate()
        class R: pass
        p2 = R(); p2.stdout, p2.stderr, p2.returncode = out, err, p.returncode; p = p2
    key = (p.stdout.strip().split("\n")[-1] if p.stdout.strip() else "NO-OUTPUT") + (" | stderr: " + p.stderr.strip()[:80] if p.stderr.strip() else "")
    res[key] += 1
for k, v in res.most_common(): print(f"{mode:8} {v:4}  {k}")
