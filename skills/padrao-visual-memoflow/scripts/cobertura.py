#!/usr/bin/env python3
"""Recalcula a corrente de cobertura da abertura.

O médico piscava porque a dissolvência era simétrica: o plano que saía chegava a zero
enquanto o que entrava ainda subia, e o fundo aparecia no meio. Aqui o plano que entra
sobe POR CIMA do anterior, que só corta quando o novo já está cheio. Buraco de verdade
(onde não havia plano nenhum) ganha um plano de preenchimento com outro trecho da fonte.
"""
import json, os

S = os.path.dirname(os.path.abspath(__file__))
L = ("/Users/jhonwill/Library/CloudStorage/GoogleDrive-jhonatan.araujo@hw-publishing.com/Drives compartilhados/"
     "H&W - Edição de Vídeo -Q3/Arquivo de Edição /08. Memory/MemoFlow/OT/[160926][OT] Upsell #1 [MemoFlow] [Squad]/MEMOFLOW_LIPSYNC")
ag = json.load(open(os.path.join(L, "17_INSERTS_ABERTURA/agenda_abertura.json")))
reg = [x for x in json.load(open(os.path.join(L, "16_ALINHAMENTO_DR/regra_edicao_dr.json")))
       if x["secao"] == "01_MEDICO_ABERTURA"]
BLOCOS = [(x["ini"], round(x["ini"] + x["dur"], 2)) for x in reg if x["regra"] == "INSERT"]
FALA_FIM = 75.30
BLOCOS[-1] = (BLOCOS[-1][0], max(BLOCOS[-1][1], FALA_FIM))

DIS  = 0.22   # o novo plano sobe por cima do anterior
FADE = 0.18   # só no fim do bloco, quando o médico deve mesmo voltar
MINF = 0.55   # buraco abaixo disso a gente fecha esticando; acima, entra plano novo
SRC  = 4.80   # duração útil de cada clipe do Kling depois de conformar a 25 fps

itens = [dict(tipo=a["tipo"], id=a["id"], i=a["ini"], o=a["fim"]) for a in ag]
itens += [dict(tipo="PROD", id="PROD 1", i=29.30, o=31.95),
          dict(tipo="PROD", id="PROD 2", i=51.50, o=53.25)]
itens.sort(key=lambda z: z["i"])

# PROD ocupa a tela: quem estiver embaixo cede o lugar
final = []
for it in itens:
    if it["tipo"] == "PROD": final.append(it); continue
    conflito = [p for p in itens if p["tipo"] == "PROD" and p["i"] < it["o"] and it["i"] < p["o"]]
    if not conflito: final.append(it); continue
    p = conflito[0]
    if it["i"] < p["i"] - 0.3: final.append(dict(it, o=p["i"]))
    if it["o"] > p["o"] + 0.3: final.append(dict(it, i=p["o"]))
itens = sorted(final, key=lambda z: z["i"])

plano, preench = [], []
for b0, b1 in BLOCOS:
    dentro = [it for it in itens if it["o"] > b0 + 0.05 and it["i"] < b1 - 0.05]
    if not dentro: continue
    dentro[0]["i"] = min(dentro[0]["i"], b0)
    for k in range(len(dentro) - 1):
        a, prox = dentro[k], dentro[k+1]
        vao = prox["i"] - a["o"]
        if vao <= 0: a["o"] = prox["i"]
        elif vao < MINF: a["o"] = prox["i"]                    # estica o anterior
        else:
            fonte = a["id"] if a["tipo"] == "BR" else prox["id"]
            preench.append(dict(tipo="BR", id=fonte, i=round(a["o"], 2), o=round(prox["i"], 2),
                                alt=True, nome="BR %s b%d" % (fonte, len(preench)+1)))
    dentro[-1]["o"] = max(dentro[-1]["o"], b1)
    for k, it in enumerate(dentro):
        it["primeiro"] = (k == 0); it["ultimo"] = (k == len(dentro) - 1)
    plano += dentro

plano += preench
plano.sort(key=lambda z: z["i"])
for it in plano:
    it.setdefault("nome", ("%s %s" % ("CARD" if it["tipo"] == "CARD" else ("PROD" if it["tipo"]=="PROD" else "BR"), it["id"]))
                  if it["tipo"] != "PROD" else it["id"])
    it.setdefault("primeiro", False); it.setdefault("ultimo", False); it.setdefault("alt", False)

# confere: sobrou algum quadro de médico dentro de bloco?
resto = []
for b0, b1 in BLOCOS:
    seg = sorted([(it["i"], it["o"]) for it in plano if it["o"] > b0 and it["i"] < b1])
    t = b0
    for a, z in seg:
        if a > t + 0.02: resto.append((round(t,2), round(a,2)))
        t = max(t, z)
    if t < b1 - 0.02: resto.append((round(t,2), round(b1,2)))

json.dump(plano, open(os.path.join(S, "plano_cobertura.json"), "w"), indent=1)
print(f"{len(plano)} planos ({len(preench)} de preenchimento) | buracos restantes: {len(resto)}")
for a, z in resto: print("   AINDA ABERTO %.2f-%.2f" % (a, z))
for p in preench: print("   preenche %6.2f-%6.2f com outro trecho de %s" % (p["i"], p["o"], p["id"]))
lon = [p for p in plano if p["tipo"]=="BR" and p["o"]-p["i"] > 3.6]
for p in lon: print("   ATENCAO plano longo %s %.2fs (fonte tem %.1fs)" % (p["nome"], p["o"]-p["i"], SRC))
