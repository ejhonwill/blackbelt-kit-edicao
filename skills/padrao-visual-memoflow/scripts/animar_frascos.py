#!/usr/bin/env python3
"""Anima os planos de frasco com movimento mínimo.

O Kling reescreve rótulo quando há movimento grande. Aqui a câmera fica travada e só
o entorno respira — o frasco praticamente não se move, que é o que preserva a marca.
"""
import json, os, subprocess, sys, time, urllib.request
S = os.path.dirname(os.path.abspath(__file__))
L = ("/Users/jhonwill/Library/CloudStorage/GoogleDrive-jhonatan.araujo@hw-publishing.com/Drives compartilhados/"
     "H&W - Edição de Vídeo -Q3/Arquivo de Edição /08. Memory/MemoFlow/OT/[160926][OT] Upsell #1 [MemoFlow] [Squad]/MEMOFLOW_LIPSYNC")
TRAVA = ("The bottle and its white MemoFlow label must stay pixel-identical to the first frame: "
         "same wording, same logo, same layout, same colours. Do not redraw the label, do not change any letter. ")
CENA = {
 ("19_INSERTS_MECANISMO","B06"): "The bottle stays perfectly still on the table; only the steam over the coffee cup drifts and the light shifts very slightly. Camera locked.",
 ("20_INSERTS_OFERTA","B01"):    "The three bottles stay perfectly still on the shelf; only the leaves behind them move a little in the air. Camera locked.",
 ("20_INSERTS_OFERTA","B02"):    "The empty bottle stays still on the counter; one last drop slides down the inside of the glass. Camera locked.",
 ("20_INSERTS_OFERTA","B22"):    "The hands finish settling the last bottle into the box and withdraw; the tissue paper relaxes. Camera locked, bottles stay upright and still.",
}
BASE = ("Photoreal, 35mm grain preserved, natural and restrained, no speed ramp, no whip pan, no zoom, "
        "no new objects, no text other than the product's own label, no watermark.")

def json1(raw, a):
    i = raw.find(a)
    if i < 0: return None
    try: return json.JSONDecoder().raw_decode(raw[i:])[0]
    except Exception: return None

modo = sys.argv[1]
if modo == "submit":
    reg = {}
    for (pasta, k), cena in CENA.items():
        img = f"{L}/{pasta}/imagens/{k}.png"
        r = subprocess.run(["higgsfield","generate","create","kling3_0_turbo","--prompt",TRAVA+cena+" "+BASE,
                            "--aspect_ratio","1:1","--resolution","1080p","--duration","5",
                            "--start-image",img,"--json"], capture_output=True, text=True, timeout=900)
        raw=(r.stdout or "").strip(); arr=json1(raw,"[")
        jid = arr[0] if isinstance(arr,list) and arr else None
        reg[f"{pasta}/{k}"]=jid
        print(f"{pasta[:2]} {k} -> {jid or 'ERRO '+(raw or r.stderr)[:90]}", flush=True)
        time.sleep(1.5)
    json.dump(reg, open(f"{S}/frascos_vid.json","w"), indent=1)
else:
    reg=json.load(open(f"{S}/frascos_vid.json")); pend={k:v for k,v in reg.items() if v}
    t0=time.time()
    while pend and time.time()-t0<3000:
        for k in list(pend):
            raw=subprocess.run(["higgsfield","generate","get",pend[k],"--json"],capture_output=True,text=True,timeout=180).stdout
            d=json1(raw,"{")
            if not d: continue
            st=d.get("status")
            if st in ("completed","succeeded","success"):
                pasta,nome=k.split("/")
                urllib.request.urlretrieve(d["result_url"], f"{L}/{pasta}/broll/{nome}.mp4")
                print("OK",k,flush=True); pend.pop(k)
            elif st in ("failed","error","cancelled","nsfw"):
                print("FALHOU",k,st,flush=True); pend.pop(k)
        if pend: time.sleep(20)
    print("FIM | pendentes:",len(pend),flush=True)
