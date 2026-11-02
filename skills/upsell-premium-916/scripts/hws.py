#!/usr/bin/env python3
"""Lote no HWStudio da empresa reaproveitando o conector MCP (~/hwstudio_mcp.py). Token lido do ~/.claude.json, nunca impresso.
    python3 hws.py avatar <blocos_dir> <imagem.png> <ids.tsv> <pasta> [prompt] [--so ID,ID] [--ar 16:9]
    python3 hws.py gerar <lote.json> <ids.tsv> <pasta>      # lote.json = [{"id","modelo","entrada":{...}, "imagem": caminho opcional -> image_url/image_urls}]
    python3 hws.py baixar <ids.tsv> <pasta_saida>           # baixa os prontos como <id>.<ext>; mostra os pendentes
"""
import json, os, sys, importlib.util, urllib.request
cfg = json.load(open(os.path.expanduser("~/.claude.json")))["mcpServers"]["hwstudio-empresa"]["env"]
os.environ.update(cfg)
spec = importlib.util.spec_from_file_location("hws", os.path.expanduser("~/hwstudio_mcp.py")); H = importlib.util.module_from_spec(spec); spec.loader.exec_module(H)
_cache = {}
def enviar(p):
    if p not in _cache: _cache[p] = H.t_enviar({"caminho": p})["url"]
    return _cache[p]
def registra(tsv, nome, jid):
    with open(tsv, "a") as f: f.write(f"{nome}\t{jid}\n")
def feitos(tsv):
    return dict(l.rstrip("\n").split("\t") for l in open(tsv)) if os.path.exists(tsv) else {}
cmd = sys.argv[1]
if cmd == "avatar":
    d, img, tsv, pasta = sys.argv[2:6]
    prompt = sys.argv[6] if len(sys.argv) > 6 and not sys.argv[6].startswith("--") else "Expressiveness: medium. Natural, calm and confident delivery, subtle head movement, natural blinking, hands stay still."
    so = sys.argv[sys.argv.index("--so") + 1].split(",") if "--so" in sys.argv else None
    ja = feitos(tsv); iu = enviar(img)
    for f in sorted(os.listdir(d)):
        if not f.endswith(".mp3"): continue
        b = f[:-4]
        if (so and b not in so) or b in ja: continue
        r = H.t_gerar({"modelo": "or:heygen/avatar-iv", "entrada": {"prompt": prompt, "image_urls": [iu], "audio_urls": [enviar(os.path.join(d, f))], "resolution": "1080p", "aspect_ratio": (sys.argv[sys.argv.index("--ar") + 1] if "--ar" in sys.argv else "9:16")},
                       "idempotency_key": f"{os.path.basename(tsv)}-{b}", "pasta": pasta})
        registra(tsv, b, r["id"]); print(b, r["id"], r.get("status"), flush=True)
elif cmd == "gerar":
    lote, tsv, pasta = sys.argv[2:5]; ja = feitos(tsv)
    for it in json.load(open(lote)):
        if it["id"] in ja: continue
        e = dict(it["entrada"])
        if it.get("imagens"):
            e["image_urls"] = [enviar(x) for x in it["imagens"]]
        elif it.get("imagem"):
            u = enviar(it["imagem"])
            if "image_urls" in e or it.get("lista"): e["image_urls"] = [u]
            else: e["image_url"] = u
        try:
            r = H.t_gerar({"modelo": it["modelo"], "entrada": e, "idempotency_key": f"{os.path.basename(tsv)}-{it['id']}", "pasta": pasta})
            registra(tsv, it["id"], r["id"]); print(it["id"], r["id"], r.get("status"), flush=True)
        except Exception as ex:
            print(it["id"], "FALHOU", ex, flush=True)
elif cmd == "baixar":
    tsv, out = sys.argv[2:4]; os.makedirs(out, exist_ok=True); pend = []
    for nome, jid in feitos(tsv).items():
        j = H.chamar("GET", "/api/jobs/" + jid)
        if j["status"] != "completed" or not j.get("saidas"): pend.append((nome, j["status"])); continue
        s = j["saidas"][0]; url = s.get("url") or ""
        if any(f.startswith(nome + ".") for f in os.listdir(out)): continue
        r = H.t_baixar({"id": jid, "pasta": out})
        arq = (r.get("arquivos") or [None])[0]
        if arq and os.path.exists(arq): os.replace(arq, os.path.join(out, nome + os.path.splitext(arq)[1])); print("ok", nome)
    print("pendentes:", pend)
