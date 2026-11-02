#!/usr/bin/env python3
"""Legenda dos depoimentos: texto da copy, tempo do Whisper conferido contra o áudio.

Mesma disciplina das seções do médico — inclusive a correção da primeira frase, que o
Whisper gruda em 0,00 quando na verdade a fala começa depois.
"""
import json, os, re, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blocos import B
from emocoes import SECOES

S = os.path.dirname(os.path.abspath(__file__))
nrm = lambda s: re.sub(r"[^a-z0-9]+", "", s.lower())

def blocos_audio(wav, fecha=0.12):
    w = wave.open(wav); sr = w.getframerate()
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)/32768
    h = int(sr*0.01); n = len(a)//h
    env = np.array([np.sqrt((a[i*h:(i+1)*h]**2).mean()+1e-12) for i in range(n)])
    db = 20*np.log10(env+1e-9); lim = np.percentile(db,10)+12
    bl=[]; dentro=False; ini=0; sil=0; passos=int(fecha/0.01)
    for i in range(n):
        f = db[i] > lim
        if f and not dentro: dentro, ini, sil = True, i, 0
        elif dentro:
            if f: sil = 0
            else:
                sil += 1
                if sil >= passos: bl.append((round(ini*0.01,2), round((i-sil)*0.01,2))); dentro=False
    if dentro: bl.append((round(ini*0.01,2), round(n*0.01,2)))
    return bl

resumo = []
for sec, per, rng, desc in SECOES:
    if "DEPOIMENTO" not in sec: continue
    tx = f"{S}/dep/tx/{sec}.json"
    if not os.path.exists(tx): print(f"{sec}: sem transcricao"); continue
    d = json.load(open(tx))
    PAL = [dict(p=w["word"].strip(), ini=round(w["start"],3), fim=round(w["end"],3))
           for seg in d["segments"] for w in seg.get("words", [])]
    if not PAL: print(f"{sec}: transcricao sem palavras"); continue

    med = blocos_audio(f"{S}/dep/{sec}.wav")
    # corrige a primeira frase, como nas secoes do medico
    a0, a1, ant = PAL[0]["ini"], None, PAL[0]["fim"]
    for k in range(1, len(PAL)):
        if PAL[k]["ini"] - ant >= 0.12: a1 = ant; break
        ant = PAL[k]["fim"]
    if a1 is None: a1 = PAL[-1]["fim"]
    m0 = med[0][0]; m1 = min((b[1] for b in med), key=lambda x: abs(x-a1))
    kf = (m1-m0)/(a1-a0) if a1 > a0 else 1.0
    cab = m0 - a0
    for w in PAL:
        if w["ini"] <= a1 + 0.01:
            w["ini"] = round(m0 + w["ini"]*kf, 3); w["fim"] = round(m0 + w["fim"]*kf, 3)

    texto = " ".join(b["texto"] for b in B if b.get("persona")==per and b.get("bloco") in rng)
    palavras = texto.split()
    tempos, j = [], 0
    for w in palavras:
        alvo = nrm(w)
        if not alvo: tempos.append(PAL[min(j,len(PAL)-1)]["ini"]); continue
        achou = None
        for k in range(j, min(j+4, len(PAL))):
            if nrm(PAL[k]["p"]) and (nrm(PAL[k]["p"]) in alvo or alvo in nrm(PAL[k]["p"])): achou = k; break
        if achou is None: achou = min(j, len(PAL)-1)
        tempos.append(PAL[achou]["ini"]); j = achou + 1

    grupos, cur, t0 = [], [], None
    for i, w in enumerate(palavras):
        if t0 is None: t0 = tempos[i]
        cur.append(w)
        pont = w.endswith((".", ",", "!", "?", ":", ";", "…", "—"))
        if (len(cur) >= 4) or (tempos[i]-t0 > 1.6) or (pont and len(cur) >= 2):
            f = tempos[i+1] if i+1 < len(tempos) else tempos[i]+0.5
            grupos.append(dict(t=round(t0,2), f=round(f,2), s=" ".join(cur))); cur, t0 = [], None
    if cur: grupos.append(dict(t=round(t0,2), f=round(tempos[-1]+0.5,2), s=" ".join(cur)))
    for i in range(len(grupos)-1):
        if grupos[i+1]["t"]-grupos[i]["f"] < 0.45: grupos[i]["f"] = grupos[i+1]["t"]
    grupos = [g for g in grupos if g["f"]-g["t"] > 0.12]

    json.dump(grupos, open(f"{S}/legendas_{sec}.json","w"), indent=1)
    resumo.append((sec, len(palavras), len(grupos), cab, grupos[0]["t"], grupos[-1]["f"]))

print(f"{'secao':<24}{'copy':>6}{'legendas':>10}{'cabeca':>9}{'inicio':>8}{'fim':>8}")
for s,n,g,c,a,b in resumo:
    print(f"{s:<24}{n:>6}{g:>10}{c:>+9.2f}{a:>8.2f}{b:>8.2f}")
