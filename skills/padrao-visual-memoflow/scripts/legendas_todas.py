#!/usr/bin/env python3
"""Reconstrói a legenda das 10 partes a partir do alinhamento corrigido.

Texto sempre da copy. Tempo do alinhamento em que só a 1a palavra foi mexida.
Quebra em pontuação ou a cada 4 palavras / 1,6 s, fecha vão < 0,45 s, e pula
onde existe lettering — quem já leu a frase grande não precisa da legenda.
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blocos import B
from emocoes import SECOES

S = os.path.dirname(os.path.abspath(__file__))
nrm = lambda s: re.sub(r"[^a-z0-9]+", "", s.lower())

COPY = {"01_MEDICO_ABERTURA": ("MEDICO", range(1,13)),
        "05_MEDICO_MECANISMO": ("MEDICO", range(13,22)),
        "07_MEDICO_OFERTA": ("MEDICO", range(22,43))}
for sec, per, rng, _ in SECOES:
    if "DEPOIMENTO" in sec: COPY[sec] = (per, rng)

def janelas_lettering(sec):
    m = {"01_MEDICO_ABERTURA": "plano_cobertura.json",
         "05_MEDICO_MECANISMO": "plano_05_MEDICO_MECANISMO.json",
         "07_MEDICO_OFERTA": "plano_07_MEDICO_OFERTA.json"}
    if sec not in m: return []
    p = f"{S}/{m[sec]}"
    if not os.path.exists(p): return []
    return [(x["i"]-0.22, x["o"]) for x in json.load(open(p)) if x["tipo"] == "CARD"]

total = 0
for sec, (per, rng) in COPY.items():
    f = f"{S}/corrigido_{sec}.json"
    if not os.path.exists(f): print(f"{sec}: sem alinhamento corrigido"); continue
    PAL = json.load(open(f))["palavras"]
    texto = " ".join(b["texto"] for b in B if b.get("persona") == per and b.get("bloco") in rng)
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
            fim = tempos[i+1] if i+1 < len(tempos) else tempos[i]+0.5
            grupos.append(dict(t=round(t0,2), f=round(fim,2), s=" ".join(cur))); cur, t0 = [], None
    if cur: grupos.append(dict(t=round(t0,2), f=round(tempos[-1]+0.5,2), s=" ".join(cur)))
    for i in range(len(grupos)-1):
        if grupos[i+1]["t"]-grupos[i]["f"] < 0.45: grupos[i]["f"] = grupos[i+1]["t"]
    grupos = [g for g in grupos if g["f"]-g["t"] > 0.12]

    LET = janelas_lettering(sec)
    fica = []
    for g in grupos:
        sob = max((min(g["f"],b)-max(g["t"],a) for a,b in LET), default=0)
        if sob > (g["f"]-g["t"])*0.6: continue
        fica.append(g)
    json.dump(fica, open(f"{S}/legfinal_{sec}.json","w"), indent=1)
    total += len(fica)
    print(f"{sec:<24} {len(grupos):>3} grupos -> {len(fica):>3} legendas (puladas {len(grupos)-len(fica)})  1a em {fica[0]['t']:.2f}s")
print(f"\ntotal de legendas: {total}")
