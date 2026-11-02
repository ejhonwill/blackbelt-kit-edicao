#!/usr/bin/env python3
"""Reconstrói o lettering no padrão LETTERING_contador-numerico-cutaway.

Caixa alta grande sem pílula, construção palavra a palavra, palavra-chave em laranja
com Deep Glow, e camada 3D vindo na direção da câmera — a linha anterior continua
viva e passa por fora do quadro enquanto a próxima entra. É esse atravessamento que
a referência chama de cutaway.
"""
import json, os, re, sys

S = os.path.dirname(os.path.abspath(__file__))
L = ("/Users/jhonwill/Library/CloudStorage/GoogleDrive-jhonatan.araujo@hw-publishing.com/Drives compartilhados/"
     "H&W - Edição de Vídeo -Q3/Arquivo de Edição /08. Memory/MemoFlow/OT/[160926][OT] Upsell #1 [MemoFlow] [Squad]/MEMOFLOW_LIPSYNC")

# grupos validados (texto vem da copy, não do Whisper)
src = open(os.path.join(S, "ae_legenda2.jsx")).read()
bruto = re.search(r"var LG=\[(.*?)\];", src, re.S).group(1)
GR = [dict(t=float(a), f=float(b), s=c)
      for a, b, c in re.findall(r"\{t:([\d.]+),f:([\d.]+),s:\"(.*?)\"\}", bruto)]

# tempo de cada palavra: consome o alinhamento em ordem
PAL = json.load(open(os.path.join(L, "16_ALINHAMENTO_DR", "01_MEDICO_ABERTURA_alinhamento.json")))["palavras"]
pt = 0
for g in GR:
    ws = g["s"].split()
    ts = []
    for k, _ in enumerate(ws):
        if pt < len(PAL) and PAL[pt]["ini"] <= g["f"] + 0.05:
            ts.append(round(max(g["t"], PAL[pt]["ini"]), 3)); pt += 1
        else:  # sem palavra sobrando: reparte o que resta do grupo
            ts.append(round(g["t"] + (g["f"] - g["t"]) * k / max(1, len(ws)), 3))
    g["ws"], g["ts"] = ws, sorted(ts)

# palavra-chave: o que a copy quer que fique na retina
CHAVE = {"MEMOFLOW", "EASY", "NATURALLY", "NORMAL", "SAFE", "HALFWAY", "FASTER",
         "SOONER", "MONTHS", "THOUSANDS", "IMPORTANT", "FREE"}
def chave(w):
    n = re.sub(r"[^A-Z0-9]", "", w.upper())
    return bool(n) and (n in CHAVE or n.isdigit())

def quebra(ws):
    """Duas linhas no máximo, partidas no ponto que equilibra a largura."""
    if len(" ".join(ws)) <= 20 or len(ws) < 3:
        return [ws]
    alvo, melhor, corte = len(" ".join(ws)) / 2, 1e9, 1
    acc = 0
    for i in range(1, len(ws)):
        acc += len(ws[i-1]) + 1
        if abs(acc - alvo) < melhor: melhor, corte = abs(acc - alvo), i
    return [ws[:corte], ws[corte:]]

def segmentos(ws, ts, i0):
    """Agrupa palavras vizinhas de mesma cor; só o primeiro trecho-chave recebe destaque."""
    marcas = [chave(w) for w in ws]
    if any(marcas):                       # um destaque por grupo, não um arco-íris
        p = marcas.index(True)
        q = p
        while q + 1 < len(marcas) and marcas[q+1]: q += 1
        marcas = [p <= k <= q for k in range(len(marcas))]
    segs, atual = [], None
    for k, w in enumerate(ws):
        if atual is None or atual["c"] != marcas[k]:
            atual = dict(c=marcas[k], ws=[], ts=[]); segs.append(atual)
        atual["ws"].append(w.upper()); atual["ts"].append(ts[i0 + k])
    return segs

dados = []
for g in GR:
    linhas, i = [], 0
    for ws in quebra(g["ws"]):
        linhas.append(segmentos(ws, g["ts"], i)); i += len(ws)
    dados.append(dict(t=g["t"], f=g["f"], linhas=linhas))

def esc(s): return s.replace("\\", "").replace('"', "'")
JS = ",".join(
    "{t:%.3f,f:%.3f,L:[%s]}" % (d["t"], d["f"], ",".join(
        "[%s]" % ",".join('{s:"%s",c:%d,w:[%s]}' % (esc(" ".join(sg["ws"])), 1 if sg["c"] else 0,
                                                    ",".join("%.3f" % x for x in sg["ts"])) for sg in ln)
        for ln in d["linhas"]))
    for d in dados)
open(os.path.join(S, "lettering_dados.txt"), "w").write(JS)

nseg = sum(len(ln) for d in dados for ln in d["linhas"])
ndest = sum(1 for d in dados for ln in d["linhas"] for sg in ln if sg["c"])
print(f"{len(dados)} grupos | {nseg} segmentos | {ndest} com destaque")
for d in dados[:6]:
    print("  %6.2f  %s" % (d["t"], "  /  ".join(
        " ".join(("[%s]" % " ".join(sg["ws"])) if sg["c"] else " ".join(sg["ws"]) for sg in ln) for ln in d["linhas"])))
