#!/usr/bin/env python3
"""Gera as imagens do plano.json no HWStudio (GPT Image 2.5 Flare/OpenRouter), 5 por vez. Pula as que já existem."""
import json, os, subprocess, sys, glob, shutil, tempfile
from concurrent.futures import ThreadPoolExecutor
B = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(B, "imagens"); os.makedirs(OUT, exist_ok=True)
HWS = sys.argv[1]; REF = os.path.join(B, "..", "avatar", "H1_start.png")
plano = json.load(open(os.path.join(B, "plano.json")))
so = set(sys.argv[2:])
def um(p):
    dest = os.path.join(OUT, p["id"] + ".png")
    if os.path.exists(dest) and not so: return p["id"], "já existe"
    tmp = tempfile.mkdtemp()
    cmd = [HWS, "gerar", "or:openai/gpt-image-2.5-flare", p["prompt"], "aspect_ratio=9:16", "quality=high", "--sim", "--esperar", "--baixar", tmp]
    if p["ref"]: cmd += ["--imagem", REF]
    r = subprocess.run(cmd, capture_output=True, text=True)
    f = glob.glob(os.path.join(tmp, "*.png")) + glob.glob(os.path.join(tmp, "*.jp*g")) + glob.glob(os.path.join(tmp, "*.webp"))
    if f: shutil.move(f[0], dest); return p["id"], "ok"
    erro = [l for l in (r.stdout + r.stderr).splitlines() if "erro" in l.lower()]
    return p["id"], "FALHOU " + (erro[-1] if erro else (r.stdout + r.stderr)[-200:])
alvo = [p for p in plano if not so or p["id"] in so]
with ThreadPoolExecutor(5) as ex:
    for i, s in ex.map(um, alvo): print(i, s, flush=True)
