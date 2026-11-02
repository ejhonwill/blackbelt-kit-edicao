#!/usr/bin/env python3
"""Gera imagem (GPT Image 2.5) e depois vídeo (Kling Turbo) dos inserts novos.

Mesma disciplina da abertura: a imagem é aprovada primeiro e o vídeo parte dela,
para o vídeo não jogar fora o look já validado.
"""
import json, os, subprocess, sys, time, urllib.request

S = os.path.dirname(os.path.abspath(__file__))
L = ("/Users/jhonwill/Library/CloudStorage/GoogleDrive-jhonatan.araujo@hw-publishing.com/Drives compartilhados/"
     "H&W - Edição de Vídeo -Q3/Arquivo de Edição /08. Memory/MemoFlow/OT/[160926][OT] Upsell #1 [MemoFlow] [Squad]/MEMOFLOW_LIPSYNC")
PASTA = {"05_MEDICO_MECANISMO": f"{L}/19_INSERTS_MECANISMO", "07_MEDICO_OFERTA": f"{L}/20_INSERTS_OFERTA"}

bib = json.load(open(f"{L}/17_INSERTS_ABERTURA/plano_abertura.json"))
BIBLIA, OBJ = bib["biblia"], bib["biblia_objeto"]
COLAGEM = ("Editorial cut-out collage, flat matte cream background, torn paper edges with visible fibre, "
           "hand-drawn marker strokes in warm orange, subtle paper grain and soft drop shadows, "
           "square 1:1 frame, graphic and clean, NO legible text, no words, no letters, no logos, no watermark")
LIMPO = " No text, no words, no letters, no captions, no logos, no watermark anywhere in the image."
MOV = ("Documentary photography come to life, natural and restrained. Keep the framing, the lighting, the colours "
       "and every face exactly as in the still. No new people, no new objects, no text, no captions, no logos, "
       "no watermark. Photoreal, 35mm grain preserved, no speed ramp, no whip pan, no zoom burst. "
       "Subtle natural continuation of the moment, very slow camera.")

def prompt(tipo, conteudo):
    if tipo == "FOTO":   return f"{conteudo}. {BIBLIA}.{LIMPO}"
    if tipo == "OBJETO": return f"{conteudo}. {OBJ}.{LIMPO}"
    return f"{conteudo}. {COLAGEM}."

def json1(raw, abre):
    i = raw.find(abre)
    if i < 0: return None
    try: return json.JSONDecoder().raw_decode(raw[i:])[0]
    except Exception: return None

planos = json.load(open(f"{S}/broll_novos.json"))
sec, modo = sys.argv[1], sys.argv[2]
D = PASTA[sec]; shots = planos[sec]
JF = f"{D}/jobs_{modo.split('_')[0]}.json"
jobs = json.load(open(JF)) if os.path.exists(JF) else {}

if modo == "img_submit":
    for k, (tipo, conteudo) in shots.items():
        if jobs.get(k, {}).get("job"): continue
        pr = prompt(tipo, conteudo)
        r = subprocess.run(["higgsfield","generate","create","gpt_image_2_5","--prompt",pr,
                            "--aspect_ratio","1:1","--quality","high","--resolution","2k","--json"],
                           capture_output=True, text=True, timeout=600)
        raw = (r.stdout or "").strip()
        arr = json1(raw, "[")
        jid = arr[0] if isinstance(arr, list) and arr else None
        jobs[k] = dict(job=jid, tipo=tipo, raw=(raw or r.stderr)[:140])
        print(f"{k} {tipo:8s} -> {jid or 'ERRO '+(raw or r.stderr)[:80]}", flush=True)
        json.dump(jobs, open(JF,"w"), indent=1); time.sleep(1)

elif modo == "img_collect":
    pend = {k:v for k,v in jobs.items() if v.get("job") and not v.get("arquivo")}
    t0 = time.time()
    while pend and time.time()-t0 < 3000:
        for k in list(pend):
            raw = subprocess.run(["higgsfield","generate","get",pend[k]["job"],"--json"],
                                 capture_output=True,text=True,timeout=180).stdout
            d = json1(raw, "{")
            if not d: continue
            st = d.get("status")
            if st in ("completed","succeeded","success"):
                f = f"{D}/imagens/{k}.png"; urllib.request.urlretrieve(d["result_url"], f)
                jobs[k]["arquivo"] = f; print("OK", k, flush=True); pend.pop(k)
            elif st in ("failed","error","cancelled","nsfw"):
                jobs[k]["status"] = st; print("FALHOU", k, st, flush=True); pend.pop(k)
        json.dump(jobs, open(JF,"w"), indent=1)
        if pend: time.sleep(15)
    print(f"IMAGENS {sec}: prontas {sum(1 for v in jobs.values() if v.get('arquivo'))}/{len(shots)} | pendentes {len(pend)}", flush=True)

elif modo == "vid_submit":
    imgs = json.load(open(f"{D}/jobs_img.json"))
    for k, (tipo, conteudo) in shots.items():
        if jobs.get(k, {}).get("job"): continue
        img = imgs.get(k, {}).get("arquivo")
        if not img or not os.path.exists(img): print(f"{k}: sem imagem", flush=True); continue
        pr = f"{conteudo}. {MOV}"
        r = subprocess.run(["higgsfield","generate","create","kling3_0_turbo","--prompt",pr,
                            "--aspect_ratio","1:1","--resolution","1080p","--duration","5",
                            "--start-image",img,"--json"], capture_output=True, text=True, timeout=900)
        raw = (r.stdout or "").strip()
        arr = json1(raw, "[")
        jid = arr[0] if isinstance(arr, list) and arr else None
        jobs[k] = dict(job=jid, raw=(raw or r.stderr)[:140])
        print(f"{k} -> {jid or 'ERRO '+(raw or r.stderr)[:80]}", flush=True)
        json.dump(jobs, open(JF,"w"), indent=1); time.sleep(1.5)

elif modo == "vid_collect":
    pend = {k:v for k,v in jobs.items() if v.get("job") and not v.get("arquivo")}
    t0 = time.time()
    while pend and time.time()-t0 < 4200:
        for k in list(pend):
            raw = subprocess.run(["higgsfield","generate","get",pend[k]["job"],"--json"],
                                 capture_output=True,text=True,timeout=180).stdout
            d = json1(raw, "{")
            if not d: continue
            st = d.get("status")
            if st in ("completed","succeeded","success"):
                f = f"{D}/broll/{k}.mp4"; urllib.request.urlretrieve(d["result_url"], f)
                jobs[k]["arquivo"] = f; print("OK", k, flush=True); pend.pop(k)
            elif st in ("failed","error","cancelled","nsfw"):
                jobs[k]["status"] = st; print("FALHOU", k, st, flush=True); pend.pop(k)
        json.dump(jobs, open(JF,"w"), indent=1)
        if pend: time.sleep(20)
    print(f"VIDEOS {sec}: prontos {sum(1 for v in jobs.values() if v.get('arquivo'))}/{len(shots)} | pendentes {len(pend)}", flush=True)
