#!/usr/bin/env python3
"""Mede onde a fala realmente acontece e confronta com o alinhamento gravado.

A lição da abertura: o Whisper gruda a primeira palavra no zero e estica a frase.
Aqui o áudio é a verdade — o alinhamento só vale depois de bater com ele.
"""
import json, sys, wave
import numpy as np

S = "/private/tmp/claude-501/-Users-jhonwill/aa133884-6487-45b8-a7a6-b0899fb49075/scratchpad"
L = ("/Users/jhonwill/Library/CloudStorage/GoogleDrive-jhonatan.araujo@hw-publishing.com/Drives compartilhados/"
     "H&W - Edição de Vídeo -Q3/Arquivo de Edição /08. Memory/MemoFlow/OT/[160926][OT] Upsell #1 [MemoFlow] [Squad]/MEMOFLOW_LIPSYNC")

def blocos_do_audio(wav, fecha=0.12):
    w = wave.open(wav); sr = w.getframerate()
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    h = int(sr * 0.01); n = len(a) // h
    env = np.array([np.sqrt((a[i*h:(i+1)*h]**2).mean() + 1e-12) for i in range(n)])
    db = 20*np.log10(env + 1e-9)
    lim = np.percentile(db, 10) + 12
    bl = []; dentro = False; ini = 0; sil = 0; passos = int(fecha/0.01)
    for i in range(n):
        f = db[i] > lim
        if f and not dentro: dentro, ini, sil = True, i, 0
        elif dentro:
            if f: sil = 0
            else:
                sil += 1
                if sil >= passos:
                    bl.append((round(ini*0.01, 2), round((i-sil)*0.01, 2))); dentro = False
    if dentro: bl.append((round(ini*0.01, 2), round(n*0.01, 2)))
    return bl, len(a)/sr

def blocos_do_alinhamento(P, pausa=0.12):
    bl = []; a0 = P[0]["ini"]; ant = P[0]["fim"]
    for k in range(1, len(P)):
        if P[k]["ini"] - ant >= pausa: bl.append((round(a0, 2), round(ant, 2))); a0 = P[k]["ini"]
        ant = P[k]["fim"]
    bl.append((round(a0, 2), round(ant, 2)))
    return bl

sec = sys.argv[1]
P = json.load(open(f"{L}/16_ALINHAMENTO_DR/{sec}_alinhamento.json"))["palavras"]
med, dur = blocos_do_audio(f"{S}/{sec}.wav")
ali = blocos_do_alinhamento(P)
print(f"{sec}: audio {dur:.2f}s | {len(med)} blocos medidos | {len(ali)} blocos no alinhamento")
print(f"  fala comeca em {med[0][0]:.2f}s; alinhamento diz {ali[0][0]:.2f}s  -> desvio de cabeca {med[0][0]-ali[0][0]:+.2f}s")
print(f"  fala termina em {med[-1][1]:.2f}s; alinhamento diz {ali[-1][1]:.2f}s")
# casa cada bloco do alinhamento com o medido mais proximo e mede o desvio
desv = []
for a in ali:
    j = min(range(len(med)), key=lambda x: abs(med[x][0]-a[0]))
    if abs(med[j][0]-a[0]) < 1.0: desv.append(med[j][0]-a[0])
if desv:
    desv = np.array(desv)
    print(f"  pareados {len(desv)}/{len(ali)} | desvio mediano {np.median(desv):+.3f}s | desvio absoluto medio {np.abs(desv).mean():.3f}s")
json.dump(med, open(f"{S}/blocos_{sec}.json", "w"))
