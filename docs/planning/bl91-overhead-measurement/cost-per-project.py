#!/usr/bin/env python3
"""BL-91 evidence: what each project's Claude Code sessions COST, from the local transcripts.

    python3 docs/planning/bl91-overhead-measurement/cost-per-project.py /tmp/out.json

Reads ~/.claude/projects/*/*.jsonl, which carry per-request `usage` (input, output, cache
read, cache creation split by TTL) and the model id, and prices them at the published
per-MTok rates in P below.

THREE LIMITS, none of them incidental:
  1. These are LIST PRICES applied to measured tokens. On a subscription plan this is what
     the traffic would cost at list, not an invoice.
  2. The price table is a snapshot and is hardcoded. Re-check it before quoting a total.
  3. Transcripts begin 2026-08-16 on this machine, so no result from this script can be
     indexed by methodology version -- v3.7 shipped 2026-08-12. Use
     mandated-load-per-version.py for anything version-indexed.
Records whose model is not in P (e.g. "<synthetic>") are counted as unknown and skipped.
"""
import json, os, glob, collections, sys
P = {"claude-opus-5":(5,25,0.50,6.25,10),"claude-opus-5-5":(4,20,0.20,5,8),
     "claude-opus-4-8":(5,25,0.50,6.25,10),"claude-opus-4-7":(5,25,0.50,6.25,10),
     "claude-opus-4-6":(5,25,0.50,6.25,10),"claude-sonnet-5":(2,10,0.20,2.5,4),
     "claude-sonnet-4-6":(3,15,0.30,3.75,6),"claude-haiku-4-5":(1,5,0.10,1.25,2),
     "claude-fable-5-1":(10,50,0.25,12.5,20)}
out={}
for proj in sorted(glob.glob(os.path.expanduser("~/.claude/projects/*/"))):
    name=os.path.basename(proj.rstrip("/"))
    cost=0.0; reqs=0; tout=0; tread=0; twrite=0; days=set()
    for path in glob.glob(proj+"*.jsonl"):
        for line in open(path, errors="replace"):
            if '"usage"' not in line: continue
            try: d=json.loads(line)
            except: continue
            m=d.get("message") or {}
            u=m.get("usage") if isinstance(m,dict) else None
            if not isinstance(u,dict): continue
            pr=P.get(m.get("model",""))
            if not pr: continue
            pi,po,prd,pw5,pw1=pr
            cc=u.get("cache_creation") or {}
            w5=cc.get("ephemeral_5m_input_tokens",0); w1=cc.get("ephemeral_1h_input_tokens",0)
            if not (w5 or w1): w5=u.get("cache_creation_input_tokens",0)
            i=u.get("input_tokens",0); o=u.get("output_tokens",0); r=u.get("cache_read_input_tokens",0)
            cost+=(i*pi+o*po+r*prd+w5*pw5+w1*pw1)/1e6
            reqs+=1; tout+=o; tread+=r; twrite+=w5+w1
            ts=d.get("timestamp")
            if ts: days.add(ts[:10])
    if reqs: out[name]=dict(cost=cost,reqs=reqs,out=tout,read=tread,write=twrite,days=len(days))
json.dump(out, open(sys.argv[1],"w"))
tot=sum(v["cost"] for v in out.values())
print(f"{'project':>42} {'$':>10} {'requests':>9} {'days':>5} {'$/day':>8} {'ctx/req':>9}")
for k,v in sorted(out.items(), key=lambda x:-x[1]["cost"])[:12]:
    print(f"{k.replace('-Users-rmsharp-Development-',''):>42} {v['cost']:>10,.0f} {v['reqs']:>9,} {v['days']:>5} {v['cost']/v['days']:>8,.0f} {v['read']/v['reqs']:>9,.0f}")
print(f"\nTOTAL across all projects: ${tot:,.0f}")
