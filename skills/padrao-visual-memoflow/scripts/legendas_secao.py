#!/usr/bin/env python3
"""Legenda corrida das seções: texto da copy, tempo do alinhamento corrigido.

O texto NUNCA vem do Whisper — ele escreve "Memo Flow" e "co -founder". Vem da copy.
O tempo vem do alinhamento já conferido contra o áudio. Quebra em ponto de pontuação
ou a cada 4 palavras / 1,6 s, e vão menor que 0,45 s é fechado para a legenda não piscar.
"""
import json, os, re, sys

S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
from blocos import B

FAIXA = {"05_MEDICO_MECANISMO": range(13, 22), "07_MEDICO_OFERTA": range(22, 43)}
nrm = lambda s: re.sub(r"[^a-z0-9]+", "", s.lower())

for sec, rng in FAIXA.items():
    texto = " ".join(b["texto"] for b in B if b.get("persona") == "MEDICO" and b.get("bloco") in rng)
    palavras = texto.split()
    PAL = json.load(open(f"{S}/alinhado_{sec}.json"))["palavras"]

    # casa a copy com o alinhamento andando nos dois ao mesmo tempo
    tempos, j = [], 0
    for w in palavras:
        alvo = nrm(w)
        if not alvo: tempos.append(PAL[min(j, len(PAL)-1)]["ini"]); continue
        k, achou = j, None
        while k < min(j+4, len(PAL)):
            if nrm(PAL[k]["p"]) and (nrm(PAL[k]["p"]) in alvo or alvo in nrm(PAL[k]["p"])): achou = k; break
            k += 1
        if achou is None: achou = min(j, len(PAL)-1)
        tempos.append(PAL[achou]["ini"]); j = achou + 1

    grupos, cur, t0 = [], [], None
    for i, w in enumerate(palavras):
        if t0 is None: t0 = tempos[i]
        cur.append(w)
        pont = w.endswith((".", ",", "!", "?", ":", ";", "…", "—"))
        fim = (len(cur) >= 4) or (tempos[i] - t0 > 1.6) or (pont and len(cur) >= 2)
        if fim:
            fimT = tempos[i+1] if i+1 < len(tempos) else tempos[i] + 0.5
            grupos.append(dict(t=round(t0, 2), f=round(fimT, 2), s=" ".join(cur)))
            cur, t0 = [], None
    if cur:
        grupos.append(dict(t=round(t0, 2), f=round(tempos[-1]+0.5, 2), s=" ".join(cur)))
    for i in range(len(grupos)-1):
        if grupos[i+1]["t"] - grupos[i]["f"] < 0.45: grupos[i]["f"] = grupos[i+1]["t"]
    grupos = [g for g in grupos if g["f"] - g["t"] > 0.12]

    json.dump(grupos, open(f"{S}/legendas_{sec}.json", "w"), indent=1)
    print(f"{sec}: {len(palavras)} palavras da copy -> {len(grupos)} legendas | {grupos[0]['t']:.2f} a {grupos[-1]['f']:.2f}s")
    for g in grupos[:4]: print(f"   {g['t']:6.2f}-{g['f']:6.2f}  {g['s']}")
