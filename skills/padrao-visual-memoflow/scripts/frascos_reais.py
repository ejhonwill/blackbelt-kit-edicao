#!/usr/bin/env python3
"""Refaz os planos com frasco usando o produto oficial como referência.

A trava do produto vem PRIMEIRO no prompt — se ela entra depois do bloco de estilo,
o gerador afoga a marca e devolve um vidro azul genérico, que foi o que aconteceu.
"""
import json, os, subprocess, sys, time, urllib.request

S = os.path.dirname(os.path.abspath(__file__))
L = ("/Users/jhonwill/Library/CloudStorage/GoogleDrive-jhonatan.araujo@hw-publishing.com/Drives compartilhados/"
     "H&W - Edição de Vídeo -Q3/Arquivo de Edição /08. Memory/MemoFlow/OT/[160926][OT] Upsell #1 [MemoFlow] [Squad]")
REF = f"{L}/MEMOFLOW_PERSONAS_APROVACAO/01_REFERENCIA_PRODUTO/MEMOFLOW_REF_BOTTLE_2K_WHITE.png"
LP = f"{L}/MEMOFLOW_LIPSYNC"

TRAVA = ("The bottle in this scene is the product in the reference image and nothing else: "
         "deep cobalt blue glass, black ribbed dropper cap, white label reading MemoFlow. "
         "Reproduce the label, the logo, the wording, the proportions and the colours EXACTLY as in the reference. "
         "Do not redesign, do not restyle, do not invent text, do not change the cap or the bottle shape. ")
ESTILO = ("Macro product-still photograph, Sony A7 IV, 90mm macro at f/4, soft north window light, "
          "Kodak Portra 400 colour science, muted warm neutrals, square 1:1 frame, shallow depth of field, "
          "real lived-in surface, fine 35mm grain, not a stock image, no extra text, no logos other than the product's own, no watermark.")

ALVOS = {
 "19_INSERTS_MECANISMO": {
   "B06": "One bottle standing on a breakfast table beside a ceramic coffee cup and a bowl of berries, morning light from a window",
 },
 "20_INSERTS_OFERTA": {
   "B01": "Three identical bottles standing in a row on a kitchen shelf, morning light, plants out of focus behind",
   "B02": "One bottle lying empty on its side on a bathroom counter, its black dropper cap resting beside it",
   "B22": "Two hands nesting three identical bottles into a cardboard shipping box lined with tissue paper, seen from above",
 },
}

def json1(raw, abre):
    i = raw.find(abre)
    if i < 0: return None
    try: return json.JSONDecoder().raw_decode(raw[i:])[0]
    except Exception: return None

modo = sys.argv[1]
if modo == "submit":
    reg = {}
    for pasta, shots in ALVOS.items():
        for k, cena in shots.items():
            pr = TRAVA + cena + ". " + ESTILO
            r = subprocess.run(["higgsfield","generate","create","gpt_image_2_5","--prompt",pr,
                                "--image-references",REF,"--aspect_ratio","1:1",
                                "--quality","high","--resolution","2k","--json"],
                               capture_output=True, text=True, timeout=900)
            raw = (r.stdout or "").strip()
            arr = json1(raw, "[")
            jid = arr[0] if isinstance(arr, list) and arr else None
            reg[f"{pasta}/{k}"] = jid
            print(f"{pasta[:2]} {k} -> {jid or 'ERRO '+(raw or r.stderr)[:100]}", flush=True)
            time.sleep(1)
    json.dump(reg, open(f"{S}/frascos_jobs.json","w"), indent=1)
else:
    reg = json.load(open(f"{S}/frascos_jobs.json"))
    pend = {k:v for k,v in reg.items() if v}
    t0 = time.time()
    while pend and time.time()-t0 < 2400:
        for k in list(pend):
            raw = subprocess.run(["higgsfield","generate","get",pend[k],"--json"],
                                 capture_output=True,text=True,timeout=180).stdout
            d = json1(raw, "{")
            if not d: continue
            st = d.get("status")
            if st in ("completed","succeeded","success"):
                pasta, nome = k.split("/")
                f = f"{LP}/{pasta}/imagens/{nome}.png"
                urllib.request.urlretrieve(d["result_url"], f)
                print("OK", k, flush=True); pend.pop(k)
            elif st in ("failed","error","cancelled","nsfw"):
                print("FALHOU", k, st, flush=True); pend.pop(k)
        if pend: time.sleep(15)
    print("FIM | pendentes:", len(pend), flush=True)
