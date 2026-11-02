#!/usr/bin/env python3
"""Corrige SÓ a primeira palavra, em vez de esticar a frase inteira.

O Whisper gruda a 1a palavra em 0,00. Eu tinha remapeado a frase toda linearmente para
o tempo medido — e com isso empurrei para a direita as palavras que já estavam certas.
A correção certa: a 1a palavra passa a começar onde o áudio começa, e as demais ficam
exatamente como o Whisper marcou.
"""
import json, os, re, wave
import numpy as np

S = os.path.dirname(os.path.abspath(__file__))
L = ("/Users/jhonwill/Library/CloudStorage/GoogleDrive-jhonatan.araujo@hw-publishing.com/Drives compartilhados/"
     "H&W - Edição de Vídeo -Q3/Arquivo de Edição /08. Memory/MemoFlow/OT/[160926][OT] Upsell #1 [MemoFlow] [Squad]/MEMOFLOW_LIPSYNC")

def inicio_da_fala(wav):
    w = wave.open(wav); sr = w.getframerate()
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)/32768
    h = int(sr*0.01); n = len(a)//h
    env = np.array([np.sqrt((a[i*h:(i+1)*h]**2).mean()+1e-12) for i in range(n)])
    db = 20*np.log10(env+1e-9); lim = np.percentile(db,10)+12
    for i in range(n):
        if db[i] > lim: return round(i*0.01, 3)
    return 0.0

FONTES = {
 "01_MEDICO_ABERTURA":   (f"{L}/16_ALINHAMENTO_DR/01_MEDICO_ABERTURA_alinhamento.json", f"{S}/dr01.wav"),
 "05_MEDICO_MECANISMO":  (f"{L}/16_ALINHAMENTO_DR/05_MEDICO_MECANISMO_alinhamento.json", f"{S}/05_MEDICO_MECANISMO.wav"),
 "07_MEDICO_OFERTA":     (f"{L}/16_ALINHAMENTO_DR/07_MEDICO_OFERTA_alinhamento.json", f"{S}/07_MEDICO_OFERTA.wav"),
}
for sec in ["02_DEPOIMENTO_MARK","03_DEPOIMENTO_ELAINE","04_DEPOIMENTO_ROBERT","06_DEPOIMENTO_MARGARET",
            "08_DEPOIMENTO_FRANK","09_DEPOIMENTO_NANCY","10_DEPOIMENTO_GEORGE"]:
    pasta = "tx" if sec == "08_DEPOIMENTO_FRANK" else "tx2"
    FONTES[sec] = (f"{S}/dep/{pasta}/{sec}.json", f"{S}/dep/{sec}.wav")

for sec, (tx, wav) in FONTES.items():
    if not (os.path.exists(tx) and os.path.exists(wav)): print(f"{sec}: fonte ausente"); continue
    d = json.load(open(tx))
    if "palavras" in d:
        PAL = [dict(p=w["p"], ini=w["ini"], fim=w["fim"]) for w in d["palavras"]]
    else:
        PAL = [dict(p=w["word"].strip(), ini=round(w["start"],3), fim=round(w["end"],3))
               for s in d["segments"] for w in s.get("words", [])]
    t0 = inicio_da_fala(wav)
    antes = PAL[0]["ini"]
    # a 1a palavra vai ate onde a 2a comeca; as demais ficam intactas
    PAL[0]["ini"] = t0
    if len(PAL) > 1: PAL[0]["fim"] = max(t0+0.15, min(PAL[0]["fim"], PAL[1]["ini"]))
    json.dump({"palavras": PAL}, open(f"{S}/corrigido_{sec}.json","w"), indent=1)
    print(f"{sec}: 1a palavra \"{PAL[0]['p']}\" {antes:.2f} -> {t0:.2f}  (as outras {len(PAL)-1} intactas)")
