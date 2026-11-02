import json, os, subprocess, sys, time, urllib.request
L = ("/Users/jhonwill/Library/CloudStorage/GoogleDrive-jhonatan.araujo@hw-publishing.com/Drives compartilhados/"
     "H&W - Edição de Vídeo -Q3/Arquivo de Edição /08. Memory/MemoFlow/OT/[160926][OT] Upsell #1 [MemoFlow] [Squad]")
D = os.path.join(L, "MEDIA", "BG3D")
PR = ("The silk ribbon breathes and flows slowly, the folds rolling gently along its length, the glowing "
      "blue light travelling inside the curls, specular highlights sliding over the satin. Very slow, "
      "continuous, seamless, hypnotic. The background stays pure black. Camera locked, no zoom, no pan. "
      "Nothing enters the frame, no text, no logo, no watermark.")
JF = os.path.join(D, "jobs_mov.json")
jobs = json.load(open(JF)) if os.path.exists(JF) else {}
modo = sys.argv[1] if len(sys.argv) > 1 else "submit"
if modo == "submit":
    for k in ["BG_A"]:
        if jobs.get(k, {}).get("job"): continue
        r = subprocess.run(["higgsfield","generate","create","kling3_0_turbo","--prompt",PR,
                            "--aspect_ratio","1:1","--resolution","1080p","--duration","10",
                            "--start-image", os.path.join(D,f"{k}.png"), "--json"],
                           capture_output=True, text=True, timeout=900)
        raw=(r.stdout or "").strip()
        try: jid=json.JSONDecoder().raw_decode(raw[raw.find("["):])[0][0]
        except Exception: jid=None
        jobs[k]=dict(job=jid, raw=(raw or r.stderr)[:200])
        print(k,"->",jid or "ERRO "+(raw or r.stderr)[:120], flush=True)
        json.dump(jobs, open(JF,"w"), indent=1)
else:
    pend={k:v for k,v in jobs.items() if v.get("job") and not v.get("arquivo")}
    t0=time.time()
    while pend and time.time()-t0 < 3600:
        for k in list(pend):
            raw=subprocess.run(["higgsfield","generate","get",pend[k]["job"],"--json"],
                               capture_output=True,text=True,timeout=180).stdout
            try: d=json.JSONDecoder().raw_decode(raw[raw.find("{"):])[0]
            except Exception: continue
            st=d.get("status")
            if st in ("completed","succeeded","success"):
                f=os.path.join(D,f"{k}.mp4"); urllib.request.urlretrieve(d["result_url"], f)
                pr=subprocess.run(["ffprobe","-v","error","-show_entries","stream=width,height,r_frame_rate:format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout.replace("\n"," ").strip()
                jobs[k]["arquivo"]=f; print("OK",k,pr,flush=True); pend.pop(k)
            elif st in ("failed","error","cancelled","nsfw"):
                jobs[k]["status"]=st; print("FALHOU",k,st,flush=True); pend.pop(k)
        json.dump(jobs, open(JF,"w"), indent=1)
        if pend: time.sleep(20)
    print("FIM pendentes:",len(pend), flush=True)
