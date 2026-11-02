import json, os, subprocess, sys, time, urllib.request
L = ("/Users/jhonwill/Library/CloudStorage/GoogleDrive-jhonatan.araujo@hw-publishing.com/Drives compartilhados/"
     "H&W - Edição de Vídeo -Q3/Arquivo de Edição /08. Memory/MemoFlow/OT/[160926][OT] Upsell #1 [MemoFlow] [Squad]")
D = os.path.join(L, "MEDIA", "BG3D")
BASE = ("Abstract 3D render of a folded silk ribbon wave floating in pure black void. Smooth sculpted "
        "surface with soft curling folds, glossy satin material, deep cobalt blue and violet, "
        "an intense glowing electric blue light trapped inside the folds, crisp specular highlights along "
        "the ridges, deep self-shadowing, the ribbon occupies the middle band of the frame and dissolves "
        "into pure black at the edges. Octane render, studio lighting, high dynamic range, ultra clean, "
        "premium motion-design background, subtle film grain. "
        "No text, no words, no letters, no logos, no watermark, no objects, no people.")
VAR = {
 "BG_A": "One single wide ribbon crossing the frame diagonally from lower left to upper right, generous black space above and below.",
 "BG_B": "Three parallel ribbons stacked in soft diagonal rows, the middle one brightest, black space between them.",
 "BG_C": "One broad ribbon with deep S-curve folds filling the centre, edges melting into black, strongest glow at the centre of the curl.",
}
JF = os.path.join(D, "jobs.json")
jobs = json.load(open(JF)) if os.path.exists(JF) else {}
modo = sys.argv[1] if len(sys.argv) > 1 else "submit"
if modo == "submit":
    for k, v in VAR.items():
        if jobs.get(k, {}).get("job"): continue
        pr = f"{v} {BASE}"
        r = subprocess.run(["higgsfield","generate","create","gpt_image_2_5","--prompt",pr,
                            "--aspect_ratio","1:1","--quality","high","--resolution","2k","--json"],
                           capture_output=True, text=True, timeout=600)
        raw=(r.stdout or "").strip()
        try: jid=json.JSONDecoder().raw_decode(raw[raw.find("["):])[0][0]
        except Exception: jid=None
        jobs[k]=dict(job=jid, raw=(raw or r.stderr)[:160])
        print(k,"->",jid or "ERRO "+(raw or r.stderr)[:90], flush=True)
        json.dump(jobs, open(JF,"w"), indent=1); time.sleep(1)
else:
    pend={k:v for k,v in jobs.items() if v.get("job") and not v.get("arquivo")}
    t0=time.time()
    while pend and time.time()-t0 < 2400:
        for k in list(pend):
            raw=subprocess.run(["higgsfield","generate","get",pend[k]["job"],"--json"],
                               capture_output=True,text=True,timeout=180).stdout
            try: d=json.JSONDecoder().raw_decode(raw[raw.find("{"):])[0]
            except Exception: continue
            st=d.get("status")
            if st in ("completed","succeeded","success"):
                f=os.path.join(D,f"{k}.png"); urllib.request.urlretrieve(d["result_url"], f)
                jobs[k]["arquivo"]=f; print("OK",k,flush=True); pend.pop(k)
            elif st in ("failed","error","cancelled","nsfw"):
                jobs[k]["status"]=st; print("FALHOU",k,st,flush=True); pend.pop(k)
        json.dump(jobs, open(JF,"w"), indent=1)
        if pend: time.sleep(15)
    print("FIM pendentes:",len(pend), flush=True)
