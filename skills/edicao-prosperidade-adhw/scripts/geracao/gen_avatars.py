import json,subprocess,time,os,sys
os.chdir(sys.argv[1]); H=os.path.expanduser("~/.npm-global/bin/higgsfield")
P=json.load(open("avatars/prompts.json")); jobs={}
ups={}
for k,v in P["items"].items():
    if v["ref"] and v["ref"] not in ups:
        r=subprocess.run([H,"upload","create",v["ref"],"--json"],capture_output=True,text=True).stdout
        d=json.JSONDecoder().raw_decode(r[r.find('{'):])[0] if '{' in r else None
        ups[v["ref"]]=d.get("id") if d else None; print("upload",v["ref"],ups[v["ref"]],flush=True)
for k,v in P["items"].items():
    prompt=" ".join([v["scene"],P["SELFIE"] if v.get("selfie",True) else "Looking straight into the lens, mouth gently closed in a relaxed neutral expression about to speak, face fully unobstructed.",P["ANTI"],P["SKIN"]])
    for n in (1,2):
        cmd=[H,"generate","create","gpt_image_2_5","--prompt",prompt,"--aspect_ratio","9:16","--quality","high","--resolution","2k","--json"]
        if v["ref"]: cmd+=["--image-references",ups[v["ref"]]]
        out=subprocess.run(cmd,capture_output=True,text=True)
        ids=out.stdout.strip().replace('"','').replace('[','').replace(']','').split()
        jobs[f"{k}_v{n:02d}"]=ids[0] if ids else "ERR:"+out.stderr[-200:]
        print(k,n,jobs[f"{k}_v{n:02d}"],flush=True); time.sleep(3)
json.dump(jobs,open("avatars/jobs.json","w"),indent=1)
