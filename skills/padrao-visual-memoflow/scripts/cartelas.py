#!/usr/bin/env python3
"""Reconstrói as 11 cartelas de lettering no padrão da referência.

CAPSLOCK em Montserrat ExtraBold, construção palavra a palavra ancorada na fala,
palavra-chave em laranja com Deep Glow e a linha vindo na direção da câmera.
Fundo: a fita 3D renderizada no Kling, não mais o ruído 2D.
"""
import json, os, re

S = os.path.dirname(os.path.abspath(__file__))
L = ("/Users/jhonwill/Library/CloudStorage/GoogleDrive-jhonatan.araujo@hw-publishing.com/Drives compartilhados/"
     "H&W - Edição de Vídeo -Q3/Arquivo de Edição /08. Memory/MemoFlow/OT/[160926][OT] Upsell #1 [MemoFlow] [Squad]")

D = re.search(r"var D=\[(.*?)\]; var n=0;", open(os.path.join(S, "ae_cards3.jsx")).read(), re.S).group(1)
CART = []
for m in re.finditer(r'\{id:"(\w+)",t:([\d.]+),d:([\d.]+),l1:\[(.*?)\],l2:\[(.*?)\]\}', D):
    tri = lambda s: [x.strip('"') for x in re.findall(r'"(.*?)"', s)]
    CART.append(dict(id=m.group(1), t=float(m.group(2)), d=float(m.group(3)),
                     l1=tri(m.group(4)), l2=tri(m.group(5))))

# a agenda manda no tempo real da cartela (foi ela que ancorou na palavra)
ag = {a["id"]: a for a in json.load(open(os.path.join(L, "MEMOFLOW_LIPSYNC/17_INSERTS_ABERTURA/agenda_abertura.json")))
      if a["tipo"] == "CARD"}
PAL = json.load(open(os.path.join(L, "MEMOFLOW_LIPSYNC/16_ALINHAMENTO_DR/01_MEDICO_ABERTURA_alinhamento.json")))["palavras"]
nrm = lambda s: re.sub(r"[^a-z0-9]+", "", s.lower())
SEQ = [nrm(w["p"]) for w in PAL]

def tempos(palavras, t0, t1):
    """Casa as palavras da cartela com o alinhamento; se não casar, reparte no tempo."""
    alvo = [nrm(w) for w in palavras if nrm(w)]
    janela = [i for i, w in enumerate(PAL) if t0 - 1.2 <= w["ini"] <= t1 + 1.2]
    for i in janela:
        if SEQ[i:i+len(alvo)] == alvo:
            return [round(PAL[i+k]["ini"], 3) for k in range(len(alvo))]
    passo = (t1 - t0) * 0.55 / max(1, len(alvo))
    return [round(t0 + 0.12 + k * passo, 3) for k in range(len(alvo))]

def esc(s): return s.replace("\\", "").replace('"', "'")
saida, casadas = [], 0
for c in CART:
    a = ag.get(c["id"])
    t, d = (a["ini"], round(a["fim"] - a["ini"], 2)) if a else (c["t"], c["d"])
    ws = [w for tr in (c["l1"], c["l2"]) for s in tr if s for w in s.split()]
    ts = tempos(ws, t, t + d)
    casadas += 1 if ts and abs(ts[0] - t) < 1.3 else 0
    it = iter(ts)
    linhas = []
    for tr in (c["l1"], c["l2"]):
        segs = []
        for k, s in enumerate(tr):
            if not s: continue
            n = len(s.split())
            segs.append(dict(s=s.upper(), c=1 if k == 1 else 0, w=[next(it) for _ in range(n)]))
        if segs: linhas.append(segs)
    saida.append(dict(id=c["id"], t=round(t, 3), d=d, L=linhas))

JS = ",".join('{id:"%s",t:%.3f,d:%.3f,L:[%s]}' % (
    o["id"], o["t"], o["d"],
    ",".join("[%s]" % ",".join('{s:"%s",c:%d,w:[%s]}' % (esc(g["s"]), g["c"], ",".join("%.3f" % x for x in g["w"]))
                               for g in ln) for ln in o["L"])) for o in saida)
open(os.path.join(S, "cartelas_dados.txt"), "w").write(JS)
print(f"{len(saida)} cartelas | {casadas} ancoradas na fala")
for o in saida[:4]:
    print("  %s %6.2f +%.2f  %s" % (o["id"], o["t"], o["d"],
          " / ".join(" ".join(("[%s]" % g["s"]) if g["c"] else g["s"] for g in ln) for ln in o["L"])))
