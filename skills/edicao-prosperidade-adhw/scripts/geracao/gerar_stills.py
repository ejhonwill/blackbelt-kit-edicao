import json,subprocess,sys,os,time
W=sys.argv[1]; H=os.path.expanduser("~/.npm-global/bin/higgsfield"); B=json.load(open(W+"/broll/broll.json"))
log=W+"/broll/stills_jobs.json"; jobs=json.load(open(log)) if os.path.exists(log) else {}
for bid,kw,scene,pessoa,mov in B["items"]:
    if bid in jobs: continue
    p=scene+" "+B["STYLE"]+(" "+B["SKIN"] if pessoa else "")
    out=subprocess.run([H,"generate","create","gpt_image_2_5","--prompt",p,"--aspect_ratio","9:16","--quality","high","--resolution","2k","--json"],capture_output=True,text=True)
    ids=out.stdout.strip().replace('"','').replace('[','').replace(']','').split()
    jobs[bid]=ids[0] if ids else "ERR"
    if not ids: print(bid,"ERRO",out.stderr[-200:],flush=True)
    json.dump(jobs,open(log,"w"),indent=1); time.sleep(2)
print("enviados",sum(1 for v in jobs.values() if v!="ERR"),"de",len(B["items"]))
