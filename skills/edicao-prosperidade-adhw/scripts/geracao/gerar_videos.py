import json,subprocess,sys,os,time
W=sys.argv[1]; H=os.path.expanduser("~/.npm-global/bin/higgsfield"); B=json.load(open(W+"/broll/broll.json"))
log=W+"/broll/videos_jobs.json"; jobs=json.load(open(log)) if os.path.exists(log) else {}
TAIL=" Realistic natural motion, cinematic and subtle, physically plausible, stable anatomy and hands, the same faces and objects throughout, no morphing, no new people appearing, no text changes, no camera cuts."
for bid,kw,scene,pessoa,mov in B["items"]:
    if bid in jobs and jobs[bid]!="ERR": continue
    jpg=f"{W}/broll/stills/{bid}.jpg"
    subprocess.run(["ffmpeg","-v","error","-i",f"{W}/broll/stills/{bid}.png","-q:v","3",jpg,"-y"],check=True)
    for tent in range(3):
        out=subprocess.run([H,"generate","create","kling3_0_turbo","--prompt",mov.capitalize()+"."+TAIL,"--start-image",jpg,"--aspect_ratio","9:16","--resolution","1080p","--duration","5","--json"],capture_output=True,text=True)
        ids=out.stdout.strip().replace('"','').replace('[','').replace(']','').split()
        if ids: break
        print(bid,"tentativa",tent,out.stderr[-150:],flush=True); time.sleep(8)
    jobs[bid]=ids[0] if ids else "ERR"
    json.dump(jobs,open(log,"w"),indent=1); time.sleep(3)
print("enviados",sum(1 for v in jobs.values() if v!="ERR"),"de",len(B["items"]))
