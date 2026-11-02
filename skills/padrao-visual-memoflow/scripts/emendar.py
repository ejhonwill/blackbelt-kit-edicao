#!/usr/bin/env python3
"""Fecha vaos entre planos cheios e regera os scripts de montagem. Roda DEPOIS de qualquer ajuste.

Lição cara: toda vez que desloquei uma cartela depois de fechar a corrente, abriu um vao
de 2 a 12 quadros e o medico aparecia. Cartela nao estica alem da propria comp — nesse caso
o B-roll seguinte vem para tras. Vao com bloco de avatar no meio fica: e o medico voltando.
"""
import json, os, sys
S = os.path.dirname(os.path.abspath(__file__))
L = ("/Users/jhonwill/Library/CloudStorage/GoogleDrive-jhonatan.araujo@hw-publishing.com/Drives compartilhados/"
     "H&W - Edição de Vídeo -Q3/Arquivo de Edição /08. Memory/MemoFlow/OT/[160926][OT] Upsell #1 [MemoFlow] [Squad]/MEMOFLOW_LIPSYNC")
reg = json.load(open(L + "/16_ALINHAMENTO_DR/regra_edicao_dr.json"))
esc = lambda s: s.replace("\\", "").replace('"', "'")
SEC = {"01_MEDICO_ABERTURA": ("plano_cobertura.json", None, None, None),
       "05_MEDICO_MECANISMO": ("plano_05_MEDICO_MECANISMO.json", "MEC", "DR 05 MECANISMO", L + "/19_INSERTS_MECANISMO"),
       "07_MEDICO_OFERTA": ("plano_07_MEDICO_OFERTA.json", "OFE", "DR 07 OFERTA", L + "/20_INSERTS_OFERTA")}

def emenda(sec):
    pa = SEC[sec][0]
    cards = {c["id"]: c for c in json.load(open(f"{S}/cartelas_{sec}.json"))}
    plano = json.load(open(f"{S}/{pa}"))
    av = sorted((r["ini"], round(r["ini"] + r["dur"], 2)) for r in reg if r["secao"] == sec and r["regra"] == "AVATAR")
    cheios = sorted([x for x in plano if not x.get("sobre")], key=lambda z: z["i"]); n = 0
    for k in range(len(cheios) - 1):
        a, b = cheios[k], cheios[k + 1]
        vao = b["i"] - a["o"]
        if vao <= 0.005 or vao >= 0.9: continue
        if any(z0 < b["i"] and a["o"] < z1 for z0, z1 in av): continue
        if a["tipo"] == "CARD" and a["id"] in cards and b["i"] > cards[a["id"]]["t"] + cards[a["id"]]["d"] + 0.75:
            b["i"] = a["o"]
        else:
            a["o"] = b["i"]
        a["ultimo"] = False; n += 1
    json.dump(plano, open(f"{S}/{pa}", "w"), indent=1)
    return n, plano

def regera(sec, plano):
    pa, pref, comp, dirp = SEC[sec]
    if pref is None:                                 # abertura usa a corrente (ae_cob2)
        visto = set(); lim = []
        for it in plano:
            if it["nome"] in visto: continue
            visto.add(it["nome"]); lim.append(it)
        CIC = ["D", "C", "B"]; n = 0; js = []
        for it in lim:
            d = "" if it["tipo"] in ("CARD", "PROD") else CIC[n % 3]
            if d: n += 1
            js.append('{n:"%s",t:"%s",i:%.3f,o:%.3f,u:%d,d:"%s"}' % (it["nome"], it["tipo"], it["i"], it["o"], 1 if it.get("ultimo") else 0, d))
        open(f"{S}/ae_cob2.jsx", "w").write(open(f"{S}/ae_cob_tmpl.jsx").read().replace("__DADOS__", ",".join(js)))
        return "ae_cob2.jsx"
    legs = json.load(open(f"{S}/legfinal_{sec}.json"))
    jp = ",".join('{tipo:"%s",id:"%s",i:%.3f,o:%.3f,ultimo:%d,sobre:%d}' % (x["tipo"], x["id"], x["i"], x["o"], 1 if x.get("ultimo") else 0, 1 if x.get("sobre") else 0) for x in plano)
    jl = ",".join('{t:%.3f,f:%.3f,s:"%s"}' % (g["t"], g["f"], esc(g["s"])) for g in legs)
    jc = ",".join('{a:%.3f,b:%.3f}' % (x["i"] - 0.22, x["o"]) for x in plano if x["tipo"] == "CARD")
    open(f"{S}/ae_montar_{pref}.jsx", "w").write(open(f"{S}/ae_montar_tmpl.jsx").read()
        .replace("__PLANO__", jp).replace("__LEGENDAS__", jl).replace("__CARTAS__", jc)
        .replace("__SECAO__", comp).replace("__PREFIXO__", pref).replace("__DIR__", dirp))
    return f"ae_montar_{pref}.jsx"

for sec in (sys.argv[1:] or list(SEC)):
    n, plano = emenda(sec)
    print(f"{sec}: {n} vaos emendados -> {regera(sec, plano)}")
