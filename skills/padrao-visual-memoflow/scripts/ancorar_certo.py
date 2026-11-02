#!/usr/bin/env python3
"""Re-ancora cada lettering no SEU proprio texto, não numa sub-frase dele.

O erro anterior: eu procurava só a expressão-chave ("tripled the dose") e fazia a cartela
entrar ali — mas a cartela começa em "THEY", que foi dito antes. Resultado: tudo atrasado.
Aqui procuro a frase inteira da cartela no alinhamento e cada palavra recebe o tempo em
que ela é realmente falada.
"""
import json, os, re, difflib

S = os.path.dirname(os.path.abspath(__file__))
nrm = lambda s: re.sub(r"[^a-z0-9]+", "", s.lower())
LEAD, MINC, MAXC = 0.16, 1.30, 2.80

for sec in ["01_MEDICO_ABERTURA", "05_MEDICO_MECANISMO", "07_MEDICO_OFERTA"]:
    PAL = json.load(open(f"{S}/corrigido_{sec}.json"))["palavras"]
    SEQ = [nrm(w["p"]) for w in PAL]
    cards = json.load(open(f"{S}/cartelas_{sec}.json"))
    rel = []
    for c in cards:
        ws = [w for ln in c["L"] for g in ln for w in g["s"].split()]
        alvo = [nrm(w) for w in ws]
        # janela do alinhamento que melhor casa com a frase inteira da cartela
        JAN = 5.0
        cand = [i for i in range(max(1, len(SEQ) - len(alvo) + 1)) if abs(PAL[i]["ini"] - c["t"]) <= JAN]
        if not cand: cand = list(range(max(1, len(SEQ) - len(alvo) + 1)))
        melhor, best = cand[0], -1.0
        for i in cand:
            r = difflib.SequenceMatcher(None, SEQ[i:i+len(alvo)], alvo).ratio()
            if r > best: best, melhor = r, i
        jan = list(range(melhor, min(melhor + len(alvo) + 6, len(PAL))))

        # casa palavra a palavra; o que nao casa é interpolado entre os vizinhos
        sm = difflib.SequenceMatcher(None, [SEQ[j] for j in jan], alvo)
        t = [None] * len(alvo)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag != "equal": continue
            for k in range(j2 - j1): t[j1+k] = PAL[jan[i1+k]]["ini"]
        conhecidos = [k for k, v in enumerate(t) if v is not None]
        if not conhecidos:
            t0 = PAL[jan[0]]["ini"]; passo = 0.26
            t = [round(t0 + k*passo, 3) for k in range(len(alvo))]
        else:
            for k in range(len(t)):
                if t[k] is not None: continue
                ant = max([q for q in conhecidos if q < k], default=None)
                dep = min([q for q in conhecidos if q > k], default=None)
                if ant is None:   t[k] = t[dep] - 0.22*(dep-k)
                elif dep is None: t[k] = t[ant] + 0.22*(k-ant)
                else:             t[k] = t[ant] + (t[dep]-t[ant])*(k-ant)/(dep-ant)
        t = [round(max(0.0, x), 3) for x in t]
        for k in range(1, len(t)):
            if t[k] <= t[k-1]: t[k] = round(t[k-1] + 0.12, 3)

        antes, ini = c["t"], max(0.0, t[0] - LEAD)
        dur = min(MAXC, max(MINC, (t[-1] - t[0]) + 1.05))
        c["t"], c["d"] = round(ini, 3), round(dur, 3)
        it = iter(t)
        for ln in c["L"]:
            for g in ln: g["w"] = [next(it) for _ in g["s"].split()]
        rel.append((c["id"], antes, c["t"], best))
    json.dump(cards, open(f"{S}/cartelas_{sec}.json", "w"), indent=1)
    print(f"=== {sec}")
    for cid, a, b, r in rel:
        print(f"   {cid}  {a:6.2f} -> {b:6.2f}  ({b-a:+.2f}s)  casamento {r*100:.0f}%")
