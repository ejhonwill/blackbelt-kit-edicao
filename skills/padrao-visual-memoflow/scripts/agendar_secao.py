#!/usr/bin/env python3
"""Cronograma de uma seção: cartelas ancoradas + b-roll preenchendo o resto.

Mesma disciplina da abertura: nada invade bloco de avatar, blocos de insert vizinhos
viram um trecho contínuo (o médico não volta entre eles) e a corrente de planos não
deixa buraco — o plano que entra sobe por cima do anterior.
"""
import json, os, sys

S = os.path.dirname(os.path.abspath(__file__))
L = ("/Users/jhonwill/Library/CloudStorage/GoogleDrive-jhonatan.araujo@hw-publishing.com/Drives compartilhados/"
     "H&W - Edição de Vídeo -Q3/Arquivo de Edição /08. Memory/MemoFlow/OT/[160926][OT] Upsell #1 [MemoFlow] [Squad]/MEMOFLOW_LIPSYNC")

MIN_BR, ALVO_BR, MINF = 1.00, 1.75, 0.55

def agenda(sec, fim_fala):
    reg = [x for x in json.load(open(f"{L}/16_ALINHAMENTO_DR/regra_edicao_dr.json")) if x["secao"] == sec]
    _b = [(x["ini"], round(x["ini"]+x["dur"], 2)) for x in reg if x["regra"] == "INSERT"]
    trechos = []
    for a, z in _b:
        if trechos and a - trechos[-1][1] < 0.15: trechos[-1] = (trechos[-1][0], z)
        else: trechos.append((a, z))
    if trechos: trechos[-1] = (trechos[-1][0], max(trechos[-1][1], fim_fala))

    cards = json.load(open(f"{S}/cartelas_{sec}.json"))
    plano = []
    for t0, t1 in trechos:
        dentro = sorted([(c["t"], round(c["t"]+c["d"], 2), c["id"]) for c in cards
                         if min(c["t"]+c["d"], t1) - max(c["t"], t0) >= 0.9])
        dentro = [(max(t0, a), min(t1, b), k) for a, b, k in dentro if min(t1, b) - max(t0, a) >= 0.9]
        marcos = [t0] + [x for d in dentro for x in (d[0], d[1])] + [t1]
        vazios = []
        for i in range(0, len(marcos)-1, 2):
            a, b = marcos[i], marcos[i+1]
            if b - a >= MIN_BR: vazios.append((a, b))
        itens = [dict(tipo="CARD", id=k, i=round(a,2), o=round(b,2)) for a,b,k in dentro]
        for a, b in vazios:                       # quebra em planos de ~1,75 s
            n = max(1, round((b-a)/ALVO_BR)); passo = (b-a)/n
            for j in range(n):
                itens.append(dict(tipo="BR", id=None, i=round(a+j*passo,2), o=round(a+(j+1)*passo,2)))
        itens.sort(key=lambda z: z["i"])
        if not itens: continue
        itens[0]["i"] = min(itens[0]["i"], t0)
        for k2 in range(len(itens)-1):
            vao = itens[k2+1]["i"] - itens[k2]["o"]
            if vao > 0: itens[k2]["o"] = itens[k2+1]["i"]    # corrente sem buraco
        itens[-1]["o"] = max(itens[-1]["o"], t1)
        for k3, it in enumerate(itens):
            it["primeiro"] = (k3 == 0); it["ultimo"] = (k3 == len(itens)-1)
        plano += itens
    for n, it in enumerate([x for x in plano if x["tipo"] == "BR"]):
        it["id"] = "B%02d" % (n+1)
    plano.sort(key=lambda z: z["i"])
    json.dump(plano, open(f"{S}/plano_{sec}.json","w"), indent=1)
    nb = sum(1 for x in plano if x["tipo"] == "BR")
    nc = sum(1 for x in plano if x["tipo"] == "CARD")
    cob = sum(x["o"]-x["i"] for x in plano)
    print(f"{sec}: {len(plano)} planos | {nc} cartelas | {nb} b-rolls | cobre {cob:.1f}s "
          f"| plano medio {cob/len(plano):.2f}s | {len(trechos)} trechos de insert")
    return nb

a = agenda("05_MEDICO_MECANISMO", 51.58)
b = agenda("07_MEDICO_OFERTA", 114.70)
print(f"\nTOTAL de b-roll novo a gerar: {a+b} clipes")
