#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
montar_relatorio.py  —  Gera o relatório combinado de criativo (padrão PONTE).

Junta 3 camadas num único HTML auto-contido, por criativo:
  1) QA técnico   (checks automáticos vindos do _QA/dados.json)
  2) Detalhamento (card AD-por-AD: visual + edição + transcrição + pontos de atenção)
  3) PONTE        (análise estratégica de conversão: nota por letra + matriz de teste)

O QA (camada 1) é 100% automático. As camadas 2 e 3 dependem de JULGAMENTO
(ler o mosaico, avaliar a copy) — por isso vêm de um "análise.json" que o Claude
preenche por criativo. Este script só faz o templating consistente.

USO:
  python3 montar_relatorio.py --qa "<pasta>/_QA" --analise analise.json -o "<pasta>"

FORMATO do analise.json (lista, um objeto por criativo — a chave `name` casa com o _QA):
[
  {
    "name": "AD10_H1",
    "badge": "AD10 H1",
    "produto": "Sonnus — gummies naturais p/ dormir (nutra EN/US)",
    "one_line": "Criadora loira, filmada em casa; b-roll de melatonina, frasco azul, laudos...",
    "resumo_edicao": "Talking-head no ângulo '...'. Alterna ... Fecha com ...",
    "transcricao": "It is impossible to take this melatonin...",
    "atencao": [
      {"sev": "orange", "texto": "Duração 2:08 (>120s) — longo pra tráfego frio."},
      {"sev": "yellow", "texto": "Mecanismo afirmado sem nomear ingrediente."},
      {"sev": "plain",  "texto": "Mesma criadora/roteiro dos demais ADs da série."}
    ],
    "ponte": {
      "O": {"nota": 4, "veredito": "Dor cirúrgica; falta rastrear origem",
            "pontos": [{"tipo":"good","txt":"Dor sensorial (3h, café, filhos)"},
                       {"tipo":"bad","txt":"Origem do hook não rastreada"}]},
      "P": {"nota": 4, "veredito": "...", "pontos": [...]},
      "T": {"nota": 3, "veredito": "...", "pontos": [...]},
      "N": {"nota": 4, "veredito": "...", "pontos": [...]},
      "E": {"nota": 2, "veredito": "...", "pontos": [...]},
      "global": 3.4,
      "acoes": ["Reescrever CTA com oferta+garantia+urgência", "...", "..."],
      "matriz": [
        {"eixo":"Hook","de":"O","testar":"H2 descoberta pela filha · H3 choque do exame"},
        {"eixo":"CTA/oferta","de":"P","testar":"+ desconto · + garantia · + urgência"}
      ]
    }
  }
]

Campos ausentes são tolerados (a seção correspondente é omitida). Se o analise.json
não existir, o script gera só a camada de QA técnico.
"""
import argparse, base64, html, json, os, sys

# -------- helpers --------
LETRAS = {
    "O": ("Orgânico decupado", "Combustível"),
    "P": ("Persuasão", "Esqueleto"),
    "T": ("Traduzir mecanismo", "Diferencial"),
    "N": ("Native creator", "Embalagem"),
    "E": ("Experimentação", "Motor"),
}
SEV_DOT = {"red": "&#128308;", "orange": "&#128992;", "yellow": "&#128993;", "plain": "&#9899;"}

def esc(s):
    return html.escape(str(s), quote=False) if s is not None else ""

def fmt_dur(sec):
    sec = int(round(sec or 0)); return f"{sec//60}:{sec%60:02d}"

def nota_classe(n):
    try: n = float(n)
    except Exception: return "s3"
    return "s4" if n >= 4 else ("s3" if n >= 3 else "s2")

def data_uri(path):
    if not path or not os.path.isfile(path): return ""
    ext = os.path.splitext(path)[1].lower().lstrip(".") or "jpeg"
    if ext == "jpg": ext = "jpeg"
    with open(path, "rb") as f:
        return f"data:image/{ext};base64," + base64.b64encode(f.read()).decode()

def load_qa(qa_dir):
    """Devolve dict name -> record (do dados.json) e caminhos de mosaico/transcrição."""
    dados = {}
    p = os.path.join(qa_dir, "dados.json")
    if os.path.isfile(p):
        for r in json.load(open(p, encoding="utf-8")):
            dados[r.get("name", "")] = r
    return dados

def read_transcript(qa_dir, name):
    p = os.path.join(qa_dir, "transcripts", name + ".txt")
    if os.path.isfile(p):
        # remove timestamps [..] no começo de cada linha, junta em parágrafo
        import re
        txt = open(p, encoding="utf-8").read()
        txt = re.sub(r"^\[[^\]]*\]\s*", "", txt, flags=re.M)
        return " ".join(l.strip() for l in txt.splitlines() if l.strip())
    return ""

# -------- render de um card --------
def render_card(a, qa, qa_dir):
    name = a.get("name", "")
    rec = qa.get(name, {})
    info = rec.get("info", {})
    dur = fmt_dur(info.get("dur", 0)) if info else a.get("duracao", "—")
    res = f'{info.get("w","?")}&times;{info.get("h","?")}' if info else a.get("resolucao", "—")
    fps = info.get("fps", a.get("fps", "—"))
    audio = "sim" if info.get("audio", True) else "não"
    flags = rec.get("flags", [])

    mosaic = a.get("mosaic_path") or os.path.join(qa_dir, "montage", name + ".jpg")
    mosaic_uri = data_uri(mosaic)
    transcript = a.get("transcricao") or read_transcript(qa_dir, name)

    # ---- QA técnico chips ----
    if flags:
        chips = "".join(
            f'<span class="chip {f["sev"]}">{esc(f.get("code",""))}: {esc(f.get("msg",""))}</span>'
            for f in flags)
        qa_line = chips
    else:
        qa_line = '<span class="chip ok">Sem apontes técnicos — pronto pra subir</span>'

    # ---- pontos de atenção ----
    at = ""
    for it in a.get("atencao", []):
        dot = SEV_DOT.get(it.get("sev", "yellow"), SEV_DOT["yellow"])
        cls = "plain" if it.get("sev") == "plain" else ""
        at += f'<li class="{cls}"><span class="dot">{dot}</span>{esc_rich(it.get("texto",""))}</li>'

    # ---- PONTE ----
    ponte_html = render_ponte(a.get("ponte"))

    return f"""
    <div class="card">
      <div class="head">
        <div class="badge">{esc(a.get("badge", name))}</div>
        <div class="desc">{esc_rich(a.get("one_line",""))}
          {f'<span class="prod">— {esc(a.get("produto"))}</span>' if a.get("produto") else ''}</div>
      </div>
      <div class="grid">
        <div class="mosaic">
          {f'<img src="{mosaic_uri}" alt="mosaico {esc(name)}">' if mosaic_uri else '<div class="nomosaic">mosaico indisponível</div>'}
          <div class="cap">Referência visual — frames amostrados com timestamp (arco completo do AD)</div>
        </div>
        <div class="col">
          <div class="meta"><b>Duração:</b> {dur} &nbsp;&middot;&nbsp; <b>Resolução:</b> {res} &nbsp;&middot;&nbsp; <b>FPS:</b> {esc(fps)} &nbsp;&middot;&nbsp; <b>Áudio:</b> {audio}</div>

          <h4>QA técnico <span class="lbl">automático</span></h4>
          <div class="qa">{qa_line}</div>

          {f'<h4>Resumo da edição</h4><div class="prose">{esc_rich(a.get("resumo_edicao"))}</div>' if a.get("resumo_edicao") else ''}

          {f'<h4>Transcrição de áudio <span class="lbl">palavra por palavra</span></h4><div class="trans">{esc_rich(transcript)}</div>' if transcript else ''}

          {f'<h4>Pontos de atenção</h4><ul class="pts">{at}</ul>' if at else ''}

          {ponte_html}
        </div>
      </div>
    </div>"""

def esc_rich(s):
    """Escapa mas preserva **negrito** -> <b> e 'aspas'."""
    if not s: return ""
    s = html.escape(str(s), quote=False)
    import re
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return s

def render_ponte(p):
    if not p: return ""
    rows = ""
    for L in ["O", "P", "T", "N", "E"]:
        d = p.get(L)
        if not d: continue
        nome, camada = LETRAS[L]
        cls = nota_classe(d.get("nota"))
        rows += (f'<tr><td><span class="letter">{L}</span> — {esc(nome)}</td>'
                 f'<td>{esc(camada)}</td>'
                 f'<td class="score {cls}">{esc(d.get("nota","—"))}/5</td>'
                 f'<td>{esc_rich(d.get("veredito",""))}</td></tr>')
    # cards por letra (opcional — só se tiver pontos)
    cards = ""
    for L in ["O", "P", "T", "N", "E"]:
        d = p.get(L)
        if not d or not d.get("pontos"): continue
        nome, _ = LETRAS[L]
        lis = ""
        for pt in d.get("pontos", []):
            mark = "good" if pt.get("tipo") == "good" else "bad"
            lis += f'<li class="{mark}">{esc_rich(pt.get("txt",""))}</li>'
        cards += (f'<div class="lcard"><b><span class="letter">{L}</span> {esc(nome)} '
                  f'<span class="chip mini {nota_classe(d.get("nota"))}">{esc(d.get("nota","—"))}/5</span></b>'
                  f'<ul class="lu">{lis}</ul></div>')
    # matriz
    matriz = ""
    if p.get("matriz"):
        mr = "".join(f'<tr><td>{esc(m.get("eixo",""))}</td><td class="from">{esc(m.get("de",""))}</td>'
                     f'<td>{esc_rich(m.get("testar",""))}</td></tr>' for m in p["matriz"])
        matriz = (f'<h5>Matriz de experimentação (letra E)</h5>'
                  f'<table class="mtx"><tr><th>Eixo</th><th>Vem de</th><th>Testar</th></tr>{mr}</table>')
    acoes = ""
    if p.get("acoes"):
        acoes = "<h5>Ações que mais movem o ponteiro</h5><ol class='act'>" + \
                "".join(f"<li>{esc_rich(x)}</li>" for x in p["acoes"]) + "</ol>"
    glob = ""
    if p.get("global") is not None:
        gval = str(p["global"]).replace(".", ",")  # decimal pt-BR
        glob = (f'<div class="global"><div class="big">{esc(gval)}<small>/5</small>'
                f'<span class="gl">Nota global PONTE</span></div></div>')
    return (f'<h4>Análise PONTE <span class="lbl">estratégia de conversão</span></h4>'
            f'<table class="ptable"><tr><th>Letra</th><th>Camada</th><th class="score">Nota</th><th>Veredito</th></tr>{rows}</table>'
            f'{cards}{matriz}{acoes}{glob}')

# -------- documento --------
CSS = """
* { box-sizing:border-box; }
body { margin:0; background:#0d0d1a; color:#e7e7f0; font-family:-apple-system,"Helvetica Neue",Arial,sans-serif; font-size:14px; line-height:1.55; padding:30px 22px; }
.wrap { max-width:1180px; margin:0 auto; }
.title { font-size:22px; font-weight:800; margin:0 0 2px; }
.kicker { font-size:12px; letter-spacing:2px; color:#8a8aa8; text-transform:uppercase; font-weight:700; margin-bottom:4px; }
.top { padding-bottom:16px; border-bottom:1px solid #23233a; margin-bottom:22px; }
.top .meta2 { color:#8a8aa8; font-size:12px; margin-top:6px; }
.card { background:#15152a; border:1px solid #262642; border-radius:16px; padding:22px; margin-bottom:26px; }
.head { display:flex; align-items:flex-start; gap:14px; margin-bottom:18px; }
.badge { background:#3b5bff; color:#fff; font-weight:800; font-size:16px; padding:8px 14px; border-radius:10px; white-space:nowrap; }
.desc { color:#c7c7de; padding-top:6px; } .desc .prod { color:#8a8aa8; }
.grid { display:grid; grid-template-columns:300px 1fr; gap:22px; align-items:start; }
.mosaic img { width:100%; border-radius:10px; display:block; } .mosaic .nomosaic { color:#6f6f90; padding:40px 0; text-align:center; border:1px dashed #333; border-radius:10px; }
.mosaic .cap { text-align:center; color:#6f6f90; font-size:11px; margin-top:8px; }
.meta { background:#101024; border:1px solid #262642; border-radius:10px; padding:11px 15px; font-size:13px; margin-bottom:6px; } .meta b { color:#fff; }
h4 { color:#5b8bff; font-size:12px; letter-spacing:1.1px; text-transform:uppercase; margin:20px 0 8px; }
h4 .lbl { color:#6f6f90; font-weight:400; letter-spacing:0; text-transform:none; font-size:11px; margin-left:6px; }
h5 { color:#b9b9d6; font-size:12px; text-transform:uppercase; letter-spacing:.6px; margin:16px 0 6px; }
.prose { color:#d3d3e6; } .prose b, .trans b, .prose b { color:#fff; }
.trans { background:#101024; border-left:3px solid #d9a520; border-radius:8px; padding:14px 16px; color:#cfcfe4; font-size:13px; }
.qa .chip { display:inline-block; font-size:12px; padding:4px 10px; border-radius:20px; margin:2px 4px 2px 0; }
.chip.ok { background:#123524; color:#4ade80; } .chip.aten { background:#3a2a10; color:#fbbf24; } .chip.crit { background:#3a1414; color:#f87171; }
.pts { list-style:none; padding:0; margin:0; } .pts li { padding:5px 0 5px 26px; position:relative; color:#d3d3e6; } .pts li b { color:#fff; }
.pts .plain { color:#9a9ab5; font-style:italic; } .dot { position:absolute; left:0; top:5px; font-size:12px; }
table { width:100%; border-collapse:collapse; margin:6px 0; }
th,td { text-align:left; padding:7px 9px; border-bottom:1px solid #23233a; vertical-align:top; font-size:13px; }
th { background:#101024; color:#9fb0ff; font-size:11px; text-transform:uppercase; letter-spacing:.4px; }
.letter { font-weight:800; color:#5b8bff; }
.score { text-align:center; font-weight:800; white-space:nowrap; }
.s4 { color:#4ade80; } .s3 { color:#fbbf24; } .s2 { color:#f87171; }
.lcard { background:#101024; border:1px solid #23233a; border-left:3px solid #5b8bff; border-radius:8px; padding:9px 13px; margin:8px 0; }
.lu { margin:5px 0 2px; padding-left:18px; } .lu li { margin:2px 0; color:#d3d3e6; }
.lu .good::marker { content:"✓ "; color:#4ade80; } .lu .bad::marker { content:"✗ "; color:#f87171; }
.chip.mini { font-size:11px; padding:1px 8px; border-radius:20px; margin-left:6px; }
.chip.mini.s4 { background:#123524; } .chip.mini.s3 { background:#3a2a10; } .chip.mini.s2 { background:#3a1414; }
.mtx .from { color:#5b8bff; font-weight:700; text-align:center; }
.act { margin:4px 0; padding-left:20px; } .act li { margin:4px 0; color:#e7e7f0; }
.global { background:linear-gradient(135deg,#3b5bff,#12123a); border-radius:12px; padding:14px 18px; margin-top:16px; }
.global .big { font-size:30px; font-weight:800; color:#fff; } .global small { font-size:15px; opacity:.8; } .global .gl { font-size:14px; font-weight:600; margin-left:12px; }
.foot { text-align:center; color:#5f5f7a; font-size:11px; margin-top:10px; }
"""

def build_doc(analises, qa, qa_dir, projeto):
    cards = "".join(render_card(a, qa, qa_dir) for a in analises)
    n = len(analises)
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Análise de criativos — {esc(projeto)}</title><style>{CSS}</style></head>
<body><div class="wrap">
  <div class="top">
    <div class="kicker">Detalhamento AD por AD · Método PONTE</div>
    <div class="title">Análise de criativos — {esc(projeto)}</div>
    <div class="meta2">{n} criativo(s) · QA técnico automático + detalhamento editorial + análise PONTE de conversão</div>
  </div>
  {cards}
  <div class="foot">Gerado pela skill analise-criativos-ponte · QA (conferir.py) + montar_relatorio.py</div>
</div></body></html>"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--qa", required=True, help="pasta _QA gerada pelo conferir.py")
    ap.add_argument("--analise", default=None, help="analise.json (preenchido pelo Claude)")
    ap.add_argument("-o", "--out", required=True, help="pasta ou arquivo .html de saída")
    ap.add_argument("--projeto", default=None)
    args = ap.parse_args()

    qa = load_qa(args.qa)
    projeto = args.projeto or os.path.basename(os.path.dirname(os.path.abspath(args.qa))) or "criativos"

    if args.analise and os.path.isfile(args.analise):
        analises = json.load(open(args.analise, encoding="utf-8"))
        if isinstance(analises, dict):
            analises = [analises]
    else:
        # fallback: só QA técnico, um card mínimo por vídeo detectado
        analises = [{"name": n, "badge": n} for n in qa]
        if not analises:
            print("ERRO: sem analise.json e sem dados de QA. Rode conferir.py antes.", file=sys.stderr)
            sys.exit(1)

    out = args.out
    if os.path.isdir(out) or not out.lower().endswith(".html"):
        os.makedirs(out, exist_ok=True)
        out = os.path.join(out, f"Analise Criativos - {projeto}.html")

    open(out, "w", encoding="utf-8").write(build_doc(analises, qa, args.qa, projeto))
    print("Relatório gerado:", out)

if __name__ == "__main__":
    main()
