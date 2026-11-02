#!/usr/bin/env python3
"""Letterings do mecanismo e da oferta, ancorados na palavra falada.

Regra herdada da abertura: a cartela entra na palavra que ela cita, nunca num tempo
digitado. Cada cartela tem no máximo duas linhas e UMA expressão em azul; a linha que
carrega o azul é a principal, a outra fica a 62% dela.
"""
import json, os, re, sys

S = os.path.dirname(os.path.abspath(__file__))

# (id, frase-âncora falada, [(texto, azul?), ...] por linha)
CARTELAS = {
"05_MEDICO_MECANISMO": [
 ("M01","tripled the dose",        [[("THEY",0),("TRIPLED",1)], [("THE DOSE",0)]]),
 ("M02","with each meal",          [[("ONE DROPPER WITH",0)], [("EACH MEAL",1)]]),
 ("M03","three times a day",       [[("THREE TIMES",1)], [("A DAY",0)]]),
 ("M04","your brain needs",        [[("THE KEY NUTRIENTS",0)], [("YOUR BRAIN NEEDS",1)]]),
 ("M05","more efficiently",        [[("YOUR BODY ABSORBS",0)], [("MORE EFFICIENTLY",1)]]),
 ("M06","repair years of damage",  [[("REPAIR",1)], [("YEARS OF DAMAGE",0)]]),
 ("M07","reconnecting wires",      [[("LIKE AN ELECTRICIAN",0)], [("RECONNECTING WIRES",1)]]),
 ("M08","becomes natural again",   [[("REMEMBERING BECOMES",0)], [("NATURAL AGAIN",1)]]),
 ("M09","completely safe",         [[("100% NATURAL",0)], [("COMPLETELY SAFE",1)]]),
],
"07_MEDICO_OFERTA": [
 ("O01","three times sooner",      [[("YOUR SUPPLY RUNS OUT",0)], [("THREE TIMES SOONER",1)]]),
 ("O02","almost sold out",         [[("OUR CURRENT BATCH IS",0)], [("ALMOST SOLD OUT",1)]]),
 ("O03","months to arrive",        [[("THE NEXT SHIPMENT",0)], [("UP TO 5 MONTHS",1)]]),
 ("O04","stop halfway through",    [[("YOUR TREATMENT",0)], [("STOPS HALFWAY",1)]]),
 ("O05","emergency solution",      [[("AN EMERGENCY SOLUTION",1)]]),
 ("O06","already covered",         [[("PACKAGING AND SHIPPING",0)], [("ALREADY COVERED",1)]]),
 ("O07","directly to you",         [[("ALL THE SAVINGS",0)], [("DIRECTLY TO YOU",1)]]),
 ("O08","the right thing to do",   [[("NOT A SALE",0)], [("THE RIGHT THING TO DO",1)]]),
 ("O09","a month for a year",      [[("JUST $39",1)], [("A MONTH",0)]]),
 ("O10","no recurring charges",    [[("ONE PAYMENT",0)], [("NO RECURRING CHARGES",1)]]),
 ("O11","literally our cost",      [[("THIS IS LITERALLY",0)], [("OUR COST",1)]]),
 ("O12","money back guarantee",    [[("100% MONEY-BACK",1)], [("GUARANTEE",0)]]),
 ("O13","every penny you paid",    [[("IMMEDIATE REFUND",0)], [("OF EVERY PENNY",1)]]),
 ("O14","as our gift",             [[("KEEP YOUR TREATMENT",0)], [("AS OUR GIFT",1)]]),
 ("O15","add and continue",        [[("CLICK",0)], [("ADD & CONTINUE",1)]]),
 ("O16","with breakfast",          [[("BREAKFAST, LUNCH",0)], [("AND DINNER",1)]]),
],
}
ALT = {
 "O03": ["five months to arrive","5 months to arrive"],
 "O09": ["a month for a year","per month for a year"],
 "O15": ["add and continue","add continue","button below"],
 "O12": ["money-back guarantee","money back guarantee"],
}
LEAD, MINC, MAXC = 0.18, 1.30, 2.60

def carrega(sec):
    return json.load(open(f"{S}/alinhado_{sec}.json"))["palavras"]

def busca(PAL, SEQ, frase):
    alvo = [re.sub(r"[^a-z0-9]+","",w.lower()) for w in frase.split()]
    alvo = [w for w in alvo if w]
    for i in range(len(SEQ)-len(alvo)+1):
        if SEQ[i:i+len(alvo)] == alvo:
            return i, PAL[i]["ini"], PAL[i+len(alvo)-1]["fim"]
    return None

for sec, defs in CARTELAS.items():
    PAL = carrega(sec)
    SEQ = [re.sub(r"[^a-z0-9]+","",w["p"].lower()) for w in PAL]
    achou, perdeu, plano = 0, [], []
    for cid, frase, linhas in defs:
        r = busca(PAL, SEQ, frase)
        if not r:
            for a in ALT.get(cid, []):
                r = busca(PAL, SEQ, a)
                if r: break
        if not r:
            perdeu.append(f"{cid} ({frase})"); continue
        i0, t0, t1 = r
        ini = max(0.0, t0 - LEAD)
        dur = min(MAXC, max(MINC, (t1-t0) + 0.85))
        # tempo de cada palavra do lettering: usa as palavras faladas a partir da ancora
        n = sum(len(t.split()) for ln in linhas for t,_ in ln)
        tempos = [PAL[min(i0+k, len(PAL)-1)]["ini"] for k in range(n)]
        if tempos[-1] > ini + dur - 0.12:                    # nao cabe: reparte no proprio card
            passo = (dur*0.55)/max(1,n)
            tempos = [round(ini+0.12+k*passo,3) for k in range(n)]
        it = iter(tempos)
        L = [[dict(s=t, c=c, w=[next(it) for _ in t.split()]) for t,c in ln] for ln in linhas]
        plano.append(dict(id=cid, t=round(ini,3), d=round(dur,3), L=L))
        achou += 1
    json.dump(plano, open(f"{S}/cartelas_{sec}.json","w"), indent=1)
    print(f"{sec}: {achou}/{len(defs)} ancoradas" + (f" | NAO ACHEI: {', '.join(perdeu)}" if perdeu else ""))
    for c in plano:
        txt = " / ".join(" ".join(("[%s]"%g['s']) if g['c'] else g['s'] for g in ln) for ln in c["L"])
        print(f"   {c['id']} {c['t']:6.2f} +{c['d']:.2f}  {txt}")
