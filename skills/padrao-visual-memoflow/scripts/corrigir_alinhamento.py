#!/usr/bin/env python3
"""Corrige a primeira frase do alinhamento usando o áudio como verdade.

O Whisper gruda a primeira palavra em 0,00 e estica a frase até o fim dela.
No áudio a frase começa depois e é mais curta. Fora isso o alinhamento é preciso,
então só a primeira frase é remapeada — o resto passa intacto.
"""
import json, sys

S = "/private/tmp/claude-501/-Users-jhonwill/aa133884-6487-45b8-a7a6-b0899fb49075/scratchpad"
L = ("/Users/jhonwill/Library/CloudStorage/GoogleDrive-jhonatan.araujo@hw-publishing.com/Drives compartilhados/"
     "H&W - Edição de Vídeo -Q3/Arquivo de Edição /08. Memory/MemoFlow/OT/[160926][OT] Upsell #1 [MemoFlow] [Squad]/MEMOFLOW_LIPSYNC")

sec = sys.argv[1]
P = json.load(open(f"{L}/16_ALINHAMENTO_DR/{sec}_alinhamento.json"))["palavras"]
med = json.load(open(f"{S}/blocos_{sec}.json"))

# extensão da primeira frase em cada lado
a0, a1 = P[0]["ini"], None
ant = P[0]["fim"]
for k in range(1, len(P)):
    if P[k]["ini"] - ant >= 0.12: a1 = ant; break
    ant = P[k]["fim"]
if a1 is None: a1 = P[-1]["fim"]
m0, m1 = med[0]

k = (m1 - m0) / (a1 - a0) if a1 > a0 else 1.0
novo = []
for w in P:
    if w["ini"] <= a1 + 0.01:
        novo.append(dict(p=w["p"], ini=round(m0 + w["ini"]*k, 3), fim=round(m0 + w["fim"]*k, 3)))
    else:
        novo.append(dict(p=w["p"], ini=round(w["ini"], 3), fim=round(w["fim"], 3)))

json.dump({"palavras": novo}, open(f"{S}/alinhado_{sec}.json", "w"), indent=1)
print(f"{sec}: primeira frase {a0:.2f}-{a1:.2f} remapeada para {m0:.2f}-{m1:.2f} (fator {k:.3f}, cabeca {m0-a0:+.2f}s)")
print(f"  palavras corrigidas: {sum(1 for w in P if w['ini']<=a1+0.01)} de {len(P)}")
print("  primeiras:", " ".join(f"{w['p']}@{w['ini']:.2f}" for w in novo[:8]))
