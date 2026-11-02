#!/usr/bin/env python3
"""Upsell 01 EreVanton (362_BM, protocolo acelerado +9 frascos). 9:16 1080×1920, 25 fps. Gera hyperframes/up1-erevanton/index.html.
Adaptado do motor do 346_PG (skill upsell-premium-916).
O roteiro visual vem do storyboard do IA Creator (_SAMURAI/storyboard.md), lido pelo motor; padrão da skill upsell-premium-916.
Editar AQUI ou no storyboard, nunca o index.html."""
import json, os, re, html, subprocess

J = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(J, "hyperframes", "up1-erevanton")
FPS = 25
def r(x): return round(x + 1e-9, 3)
def q(x): return round(round(x * FPS) / FPS, 3)
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)

# ---------------------------------------------------------------- fala (alinhamento ElevenLabs)
BL = json.load(open(os.path.join(J, "ia", "voz", "blocos.json")))
SEG, W, t0 = [], [], 0.0
for b in BL:
    d = dur(os.path.join(H, "assets", "avatar", b["id"] + ".mp4"))
    a = json.load(open(os.path.join(J, "ia", "voz", "blocos", b["id"] + "_alin.json")))
    cur, cs = "", None
    for ch, s, e in zip(a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]):
        if ch.isspace():
            if cur: W.append({"w": cur, "s": t0 + cs, "e": t0 + pe, "ea": t0 + pa}); cur = ""
        else:
            if not cur: cs = s; pa = e
            cur += ch; pe = e
            if ch.isalnum(): pa = e  # fim acústico: a pontuação carrega a pausa seguinte (+0,2–0,3 s medidos no áudio)
    if cur: W.append({"w": cur, "s": t0 + cs, "e": t0 + pe, "ea": t0 + pa})
    SEG.append({"id": b["id"], "s": t0, "d": d}); t0 += d
FIM = q(t0)
DEPO = json.load(open(os.path.join(J, "ia", "depoentes", "depoentes.json")))
for d in DEPO:  # 362: vão aberto no bloco do expert com a duração natural do depoente (sem atempo)
    s0 = next(x["s"] for x in SEG if x["id"] == d["bloco"]); d["ini"] = s0 + d["ini_bloco"] + 0.15; d["fim"] = s0 + d["fim_bloco"]
TARJA = {"DP_klaus": "Klaus, 58 · Milwaukee, WI", "DP_mark": "Mark, 47 · Phoenix, AZ"}
for d in DEPO:
    a = json.load(open(os.path.join(J, "ia", "depoentes", "fit", d["id"] + "_alin.json")))
    base = d["ini"] - 0.15; novas, cur, cs = [], "", None
    for ch, s_, e_ in zip(a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]):
        if ch.isspace():
            if cur: novas.append({"w": cur, "s": base + cs, "e": base + pe, "ea": base + pe}); cur = ""
        else:
            if not cur: cs = s_
            cur += ch; pe = e_
    if cur: novas.append({"w": cur, "s": base + cs, "e": base + pe, "ea": base + pe})
    W[:] = [x for x in W if not (d["ini"] - 0.4 <= x["s"] < d["fim"] - 0.15)] + novas
    W.sort(key=lambda x: x["s"])
def norm(w): return re.sub(r"[^a-z0-9$%]", "", w.lower().replace("’", "'"))
NW = [norm(x["w"]) for x in W]
_cursor = [0.0]
def achar(frase, depois=None):
    alvo = [norm(x) for x in frase.split() if norm(x)]
    lim = _cursor[0] if depois is None else depois
    for i in range(len(W)):
        if W[i]["s"] < lim - 0.01: continue
        if NW[i:i + len(alvo)] == alvo: return W[i]["s"]
    raise SystemExit(f"frase não achada: {frase!r} depois de {lim:.1f}s")
def palavras(frase):
    t = achar(frase); i = next(k for k in range(len(W)) if abs(W[k]["s"] - t) < 1e-6)
    return W[i:i + len(frase.split())]

clips, js, sfx, anim = [], [], [], []
def S(t, f, v, d=None): sfx.append((q(t), f, v, d))
def em(sel, t, de, para, d=0.45, e="expo.out"): anim.append((sel, t, de, para, d, e))
def entra(sel, t, de="{y:70, opacity:0, filter:'blur(14px)'}", para="{y:0, opacity:1, filter:'blur(0px)'}", d=0.5, e="expo.out"): em(sel, t, de, para, d, e)
def entra3d(sel, t, d=0.7):  # entrada com câmera 3D + motion blur (Jhon: "trabalhe o movimento blur nas câmeras 3D")
    em(sel, t, "{rotationY:55, rotationX:12, z:-600, x:260, opacity:0, filter:'blur(26px)'}",
       "{rotationY:0, rotationX:0, z:0, x:0, opacity:1, filter:'blur(0px)'}", d, "expo.out")
TRK = [40]
def media(src, a, b, cls="fill", ini=0.0, idp="m"):
    TRK[0] += 1
    sd = dur(os.path.join(H, src)) - 0.04 - ini
    rate = 1.0 if sd >= b - a else max(0.55, round(sd / (b - a) - 0.005, 3))
    ratt = f' data-playback-rate="{rate}"' if rate < 1 else ""
    return (f'<video id="{idp}{TRK[0]}" class="clip {cls}" src="{src}" muted playsinline data-start="{q(a)}" data-duration="{r(b - a)}" '
            f'data-media-start="{r(ini)}" data-track-index="{TRK[0]}"{ratt}></video>')
def recorte(a, b, cls):  # doutora recortada (alpha) sincronizada com a fala, quebrando por bloco
    out = ""
    for s in SEG:
        x0, x1 = max(a, s["s"]), min(b, s["s"] + s["d"])
        if x1 - x0 > 0.04:
            TRK[0] += 1
            out += (f'<video id="al{TRK[0]}" class="clip {cls}" src="assets/doutora_alpha/{s["id"]}.webm" muted playsinline data-start="{q(x0)}" '
                    f'data-duration="{r(q(x1) - q(x0))}" data-media-start="{r(q(x0) - s["s"])}" data-track-index="{TRK[0]}"></video>')
    return out
def pp(cid, frase, cls, size, hl=(), red=(), style=""):
    out = []
    for k, x in enumerate(palavras(frase)):
        w = html.escape(x["w"].strip(",.:!…—\"“”").upper() if "cond" in cls or "up" in cls else x["w"].strip(",:—\"“”"))
        c = cls + (" hl" if k in hl else "") + (" red" if k in red else "")
        out.append(f'<span class="w {c}" id="{cid}w{k}">{w}</span>')
        em(f"#{cid}w{k}", x["s"] - 0.04, "{y:'55%', opacity:0, filter:'blur(12px)'}", "{y:'0%', opacity:1, filter:'blur(0px)'}", 0.36)
    return f'<div class="ln" style="font-size:{size}px;{style}">{" ".join(out)}</div>'
def bate(sel, t):
    em(sel, t, "{scale:2.2, opacity:0, filter:'blur(22px)'}", "{scale:1, opacity:1, filter:'blur(0px)'}", 0.5)
    S(t, "k_impacto", 0.09, 0.3)
def troca(cid, ts, pal):
    h = "".join(f'<b id="{cid}{k}">{html.escape(p)}</b>' for k, p in enumerate(pal))
    for k, t in enumerate(ts):
        em(f"#{cid}{k}", t - 0.04, "{y:'100%', opacity:0, filter:'blur(10px)'}", "{y:'0%', opacity:1, filter:'blur(0px)'}", 0.32)
        if k + 1 < len(ts): em(f"#{cid}{k}", ts[k + 1] - 0.08, "{y:'0%', opacity:1}", "{y:'-100%', opacity:0}", 0.22, "power3.in")
    return h

CENAS = []
TETO = {"B": 6.0, "R": 8.0, "T": 8.0}  # T 8 s (rodada 2: mais 3D)
def cena(cid, tipo, ini, fim, luz=False, teto=None):
    def reg(fn):
        _cursor[0] = 0.0
        a = achar(ini) if isinstance(ini, str) else ini
        b = achar(fim, a + 0.1) if isinstance(fim, str) else (a + fim[1] if isinstance(fim, tuple) else fim)
        lim = teto or TETO.get(tipo)
        if lim: b = min(b, a + lim)  # clipe de 5 s não estica além disso; a doutora volta
        CENAS.append((cid, tipo, a, b, fn, luz)); return fn
    return reg
def B(cid, ini, fim, src, ini_m=0.0, luz=True, extra="", teto=None):
    @cena(cid, "B", ini, fim, luz, teto)
    def _(a, b): return media(src, a, b, ini=ini_m) + (extra(a, b) if callable(extra) else extra)
def R(cid, ini, fim, src, ini_m=0.0, extra=""):
    @cena(cid, "R", ini, fim, True)
    def _(a, b): return media(src, a, b, ini=ini_m) + '<div class="gradt"></div>' + (extra(a, b) if callable(extra) else extra)
def M(cid, ini, fim, html_fn):  # lettering centralizado na frente da doutora desfocada (palco de marca)
    @cena(cid, "M", ini, fim)
    def _(a, b): return html_fn(a, b)
def TL(cid, ini, d, kick, txt, cls="", modo="entra"):
    @cena(cid, "M", ini, ("+", d))
    def _(a, b):
        (bate if modo == "bate" else entra)(f"#{cid}t", a + 0.04)
        k = f'<div class="kick c" style="top:110px">{kick}</div>' if kick else ""
        return k + f'<div class="disp big c tback {cls}" id="{cid}t" style="top:170px">{txt}</div>'
def fundo(src, a, b, cls="tbg"):
    return f'<div class="{cls}">' + media(src, a, b) + '</div>'
def TB(cid, ini, fim, src, kick, txt, quando=None, cls="", modo="entra", extra=""):  # lettering sobre 3D que exemplifica a fala
    @cena(cid, "T", ini, fim, True)
    def _(a, b):
        (bate if modo == "bate" else entra)(f"#{cid}t", achar(quando) if quando else a + 0.12)
        k = f'<div class="kick c" style="top:110px">{kick}</div>' if kick else ""
        return (fundo(src, a, b) + '<div class="tgrad"></div>' + k + f'<div class="disp big c tback {cls}" id="{cid}t" style="top:170px">{txt}</div>'
                + (extra(a, b) if callable(extra) else extra))
def letra_em(cid, frase, txt, cls="", modo="bate", top=170):  # lettering que bate por cima do b-roll numa frase
    def f(a, b):
        (bate if modo == "bate" else entra)(f"#{cid}", achar(frase))
        return f'<div class="tgrad"></div><div class="disp big c tback {cls}" id="{cid}" style="top:{top}px">{txt}</div>'
    return f
def chip_em(cid, frase, txt, cls=""):
    def f(a, b):
        entra(f"#{cid}", achar(frase) if frase else a + 0.25)
        return f'<div class="gradb"></div><div class="kbx"><div class="chip big {cls}" id="{cid}">{txt}</div></div>'
    return f


# ================================================================ roteiro visual: lido do storyboard do IA Creator (_SAMURAI/storyboard.md)
# Cada linha da tabela vira um momento. D = expert sozinho (não gera cena). As outras colunas escolhem o componente:
# itens separados por " · ", etapas por " → ", ✓/✕ viram linha de lista, "chip:" vira chip, número vira número com extrusão,
# aspas viram citação, "bolhas:" vira mensagem no celular, "CTA"/"YES, I WANT…" vira o botão validado, kicker/título no T.
SB = os.path.join(J, "_SAMURAI", "storyboard.md")
LINHAS = []
for l in open(SB):
    if re.match(r"\| *\d+ *\|", l):
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        LINHAS.append(dict(n=int(c[0]), frases=c[2], tipo=c[3], visual=c[4], asset=c[5], texto=c[8]))
def aspas(s): return re.findall(r"“([^”]+)”", s)
CTA_TXT = "YES, I WANT TO ACCELERATE MY RESULTS"
SETA = ('<svg class="seta" viewBox="0 0 120 120"><circle cx="60" cy="60" r="54" fill="#FBD643"/>'
        '<path d="M60 30v52M38 62l22 22 22-22" fill="none" stroke="#0b1630" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg>')
IMG = {"1-erevanton": "ev_1.png", "3-erevanton": "ev_3.png", "9-erevanton": "ev_9.png", "selo_garantia_1year": "selo_garantia_1year.png"}
def imgs_do_asset(s):
    out = []
    for k, v in IMG.items():
        if k in s.lower() and v not in out: out.append(v)
    return out
def novo(s):  # só vale se o vídeo existe (nr_mockup virou o PNG oficial do frasco)
    m = re.search(r"NOVO:(\w+)", s)
    return m.group(1) if m and os.path.exists(os.path.join(H, "assets", "ia3", m.group(1) + ".mp4")) else None
def ach(frase, a, b=None):  # frase dentro da cena (ou None)
    try:
        t = achar(frase, a - 0.3)
        return t if b is None or t < b + 0.5 else None
    except SystemExit:
        return None
# ---- psicologia das cores (V3): verde = ganho/solução; vermelho = dor/risco
POS_TXT = ["faster", "accelerated", "accelerate", "regeneration", "regenerate", "permanent", "permanently", "solved", "free shipping", "free", "reserved",
           "secured", "keep the bottles", "refund", "zero risk", "lowest price ever", "lowest price", "dissolve", "flow", "firm", "reliable",
           "self-confidence", "confidence", "gifts", "natural", "same product", "without interruption"]
NEG_TXT = ["toxins", "the problem", "halfway", "disappear again", "disappears", "ran out of bottles", "ran out", "run out", "side effects", "addictive",
           "let it pass", "risk", "failure", "blocks"]
_RX_COR = re.compile(r"(?<![\w-])(" + "|".join(re.escape(x) for x in sorted(POS_TXT + NEG_TXT, key=len, reverse=True)) + r")(?![\w-])", re.I)
def colore(txt, so=None):
    """pinta as palavras-chave do texto (fora de tags e de spans já coloridos): positivas verdes, negativas vermelhas.
    so='neg'/'pos' restringe; em texto negado (✕, LOST, NOT, NO, OFF…) a palavra positiva não fica verde."""
    plano = re.sub(r"<[^>]+>", " ", txt)
    if so is None and re.search(r"✕|\b(LOST|NOT|NO|OFF|WITHOUT|NEVER|STILL DRAINED)\b", plano, re.I) and not re.search(r"NO QUESTIONS|NO HASSLE", plano, re.I): so = "neg"
    garantia = re.search(r"ON ME\b", plano, re.I)
    def cor(m):
        w = m.group(1); neg = w.lower() in NEG_TXT
        if (so == "neg" and not neg) or (so == "pos" and neg) or (garantia and w.lower() == "risk"): return w
        return f'<span class="{"red" if neg else "grn"}">{w}</span>'
    out, prof = [], 0
    for parte in re.split(r"(<[^>]+>)", txt):
        if parte.startswith("<"):
            if re.match(r"<span\b", parte): prof += 1
            elif parte.startswith("</span"): prof = max(0, prof - 1)
            out.append(parte); continue
        if prof: out.append(parte); continue
        out.append(_RX_COR.sub(cor, parte))
    return "".join(out)
def tom(txt):  # cor do chip
    if re.search(r"✕|RAN OUT|RUN OUT|DISAPPEAR|PROBLEM|HALFWAY|TOXIN", txt, re.I): return "red"
    if re.search(r"✓|" + "|".join(re.escape(x) for x in POS_TXT), txt, re.I): return "grn"
    return ""
PARE = set("the a an and or of to in on at is it its it's you your for with this that by not no as be are was".split())
def quando(txt, a, b, k, n):  # entrada do item: 1º na abertura da tela; os outros na palavra-chave, sem passar de 55% da cena
    if k == 0: return a + 0.15
    t = _quando(txt, a, b, k, n)
    return min(max(t, a + 0.15 + k * 0.3), a + 0.15 + (b - a) * 0.55)
def _quando(txt, a, b, k, n):
    ws = [norm(w) for w in re.sub(r"<[^>]+>", " ", txt).split()]
    ws = [w for w in ws if len(w) > 2 and w not in PARE and not re.match(r"^[\d$%]+$", w)]
    for w in ws[:3]:
        for x in W:
            if a - 0.2 <= x["s"] <= b - 0.3 and norm(x["w"]).startswith(w[:6]): return x["s"] - 0.05
    passo = min(1.1, max(0.35, (b - a - 1.0) / max(1, n)))
    return a + 0.3 + k * passo
UID = [0]
def nid(p="e"):
    UID[0] += 1; return f"{p}{UID[0]}"
def limpa(s):
    s = re.sub(r"\((?:glow\w|bate[^)]*|legenda[^)]*|teto[^)]*)\)", "", s)
    s = re.sub(r"\([^)]*[a-zà-ú][^)]*\)", "", s)  # anotação do storyboard entre parênteses
    s = re.sub(r"^(bolhas?|bolha|letra_em|chip_em)\s*:\s*", "", s.strip())
    s = re.sub(r"\s*\[(g|r)\]", "", s)
    return s.replace("class=red", 'class="red"').replace("class=yel", 'class="yel"').replace("class=grn", 'class="grn"').strip(" ·")

def item_html(it, a, b, k, n, estado):
    """um item da coluna 'texto na tela' → (html, id). estado guarda o grupo de lista aberto."""
    it = it.strip(); i = nid()
    t = quando(it, a, b, k, n)
    if not it: return "", None
    if it.lower().startswith("chip"):
        txt = limpa(it.split(":", 1)[1] if ":" in it else it)
        cor = tom(txt)
        entra(f"#{i}", t, "{scale:.6, opacity:0}", "{scale:1, opacity:1}", 0.35, "back.out(2)")
        return f'<div class="chip big {cor}" id="{i}">{txt if cor else colore(txt)}</div>', i
    if CTA_TXT in it.upper() or it.upper().startswith("CTA"):
        em(f"#{i}", t, "{scale:.4, opacity:0, filter:'blur(20px)'}", "{scale:1, opacity:1, filter:'blur(0px)'}", 0.45, "back.out(2)")
        js.append(f'tl.to("#{i} .bt", {{scale:1.04, duration:0.45, ease:"sine.inOut", yoyo:true, repeat:{max(1, int((b - t) / 0.45) - 2)}}}, {r(t + 0.5)});')
        js.append(f'tl.to("#{i} .seta", {{y:16, duration:0.4, ease:"sine.inOut", yoyo:true, repeat:{max(1, int((b - t) / 0.4) - 2)}}}, {r(t + 0.5)});')
        S(t, "k_pop", 0.09, 0.74)
        return f'<div class="cta-g rel" id="{i}"><div class="bt">{CTA_TXT}</div>{SETA}</div>', i
    if it.lower().startswith("carimbo"):
        em(f"#{i}", t, "{scale:3, rotation:-20, opacity:0, filter:'blur(20px)'}", "{scale:1, rotation:-6, opacity:1, filter:'blur(0px)'}", 0.4, "back.out(2)")
        S(t, "k_impacto", 0.1, 0.3)
        return f'<div class="stamp red rel" id="{i}">{limpa(it[7:])}</div>', i
    marca = None
    if re.match(r"^(✓|✕|\$ )", it) or re.search(r"(✓|✕)$", it):
        marca = "✕" if "✕" in it else ("$" if it.startswith("$ ") else "✓")
        txt = limpa(re.sub(r"^(✓|✕|\$)\s*|\s*(✓|✕)$", "", it))
        if txt:
            em(f"#{i}", t, "{x:-160, opacity:0, filter:'blur(16px)'}", "{x:0, opacity:1, filter:'blur(0px)'}", 0.45)
            S(t, "k_clique", 0.18, 0.08)
            if marca == "✕" and re.match(r"^\$\d", txt):  # preço cheio na lista: mantém o $ e vai riscado em vermelho
                return pcheio(t, txt, risca=t + 0.35, tam=150), i
            return f'<div class="li {"x" if marca == "✕" else ""}" id="{i}"><b>{marca}</b><span>{colore(txt, "neg" if marca == "✕" else "pos")}</span></div>', i
    if it.startswith("“") or it.startswith('"'):
        entra(f"#{i}", t)
        return f'<div class="qt" id="{i}">{limpa(it)}</div>', i
    it = re.sub(r"^bolha:\s*", "", it)
    forca = "grn" if "[g]" in it else ("red" if "[r]" in it else None); it = re.sub(r"\s*\[(g|r)\]", "", it)
    m = re.match(r"^(?:número\s+)?([−~≈+]?[$]?[\d][\d,.:–-]*\s?(?:%|¢|PM|AM|/80|X|\+)?)(?:\s+(.*))?$", it)
    if m and len(m.group(1)) <= 9 and not re.search(r"\d", m.group(2) or ""):
        num, resto = m.group(1).strip(), limpa(m.group(2) or "")
        bate(f"#{i}", t)
        tam = 330 if len(num) <= 3 else (250 if len(num) <= 5 else 190)
        cor = forca or tom(resto) or "yel"
        return (f'<div class="numw" id="{i}"><div class="num {cor}" style="font-size:{tam}px">{num}</div>'
                + (f'<div class="cond mid">{colore(resto)}</div>' if resto else "") + '</div>'), i
    if "riscado" in it:
        entra(f"#{i}", t); x = nid()
        em(f"#{x}", t + 0.5, "{scaleX:0}", "{scaleX:1}", 0.35, "power2.out"); S(t + 0.5, "k_swish", 0.05, 0.57)
        return f'<div class="price rel" id="{i}">{limpa(it.replace("riscado", ""))}<i class="risco" id="{x}"></i></div>', i
    if it.lower().startswith("kicker"):
        entra(f"#{i}", t)
        return f'<div class="kick" id="{i}">{limpa(it[6:])}</div>', i
    if it.lower().startswith("cond"):
        entra(f"#{i}", t)
        return f'<div class="cond mid" id="{i}">{colore(limpa(it[4:]))}</div>', i
    txt = limpa(re.sub(r"^título\s*", "", it))
    if not estado.get("titulo"):
        estado["titulo"] = 1; bate(f"#{i}", t) if len(txt) < 16 else entra(f"#{i}", t)
        tam = "huge" if len(re.sub(r"<[^>]+>", "", txt)) <= 10 else "big"
        return f'<div class="disp {tam} tback" id="{i}">{colore(txt)}</div>', i
    entra(f"#{i}", t)
    return f'<div class="cond mid" id="{i}">{colore(txt)}</div>', i

def etapa_html(txt, a, b, imgs, bgv):
    itens = [x for x in re.split(r"\s+·\s+", txt) if x.strip()]
    estado, partes, lista = {}, [], []
    def fecha():
        if lista: partes.append('<div class="vidro2">' + "".join(lista) + '</div>'); lista.clear()
    for k, it in enumerate(itens):
        h, _ = item_html(it, a, b, k, len(itens), estado)
        if h.startswith('<div class="li'): lista.append(h)
        else: fecha(); partes.append(h)
    fecha()
    topo = ""
    if imgs:
        i = nid()
        em(f"#{i}", a + 0.05, "{y:300, rotationY:-50, z:-400, opacity:0, filter:'blur(24px)'}", "{y:0, rotationY:0, z:0, opacity:1, filter:'blur(0px)'}", 0.7)
        topo = (f'<div class="prods" id="{i}" style="height:auto">' + kit_html(sum(KIT_N[x] for x in imgs)) + '</div>') if all(x in KIT_N for x in imgs) else (f'<div class="prods" id="{i}">' + "".join(f'<img src="assets/img/{x}">' for x in imgs) + '</div>')
    return topo + "".join(partes)

def cena_F(L, tipo):
    @cena(f"c{L['n']:03d}", tipo, L["ini"], L["fim"])
    def _(a, b):
        txt = L["texto"]; bg = novo(L["asset"]); imgs = imgs_do_asset(L["asset"]); ib = imgs_bg(L["asset"])
        if L["n"] in ESPECIAIS:
            if getattr(ESPECIAIS[L["n"]], "__name__", "") == "f" and ESPECIAIS[L["n"]].__qualname__.startswith("presentes_caixa"): return ESPECIAIS[L["n"]](a, b)
            if ESPECIAIS[L["n"]] in (tres_caps, ritmo, presentes_soltos): return ESPECIAIS[L["n"]](a, b)
            if ESPECIAIS[L["n"]] in (triptico, meses):
                if len(ib) >= 3: return ESPECIAIS[L["n"]](a, b)
                return '<div class="fs top"><div class="disp big">(aguardando imagens)</div></div>'
            return (bg_html(ib[0], a, b) if ib else "") + ESPECIAIS[L["n"]](a, b)
        if ib:
            out = bg_html(ib[0], a, b)
            etapas = [x for x in re.split(r"\s+→\s+", txt) if x.strip()]
            if len(etapas) == 1: return out + '<div class="fs top">' + etapa_html(etapas[0], a, b, imgs, None) + '</div>' + LOGO("topo")
            t2 = min(max(_quando(etapas[1], a + (b - a) * 0.3, b, 0, 1), a + (b - a) * 0.3), a + (b - a) * 0.6)
            i1 = nid("s"); em(f"#{i1}", t2 - 0.25, "{opacity:1, y:0}", "{opacity:0, y:-60, filter:'blur(12px)'}", 0.3, "power2.in")
            return (out + f'<div class="fs top" id="{i1}">' + etapa_html(etapas[0], a, t2, imgs, None) + '</div>'
                    + '<div class="fs top">' + etapa_html(" · ".join(etapas[1:]), t2, b, [], None) + '</div>' + LOGO("topo"))
        if txt.lower().startswith("bolhas:"):
            raise SystemExit("bolhas: não usado no 362 (depoimento é vídeo)")
        out = ""
        if bg:
            em(f"#c{L['n']:03d}i .fbgv", a, "{opacity:0, scale:1.2}", "{opacity:1, scale:1}", 0.6)
            out += fundo(f"assets/ia3/{bg}.mp4", a, b, "fbgv") + '<div class="fgrad"></div>'
        etapas = [x for x in re.split(r"\s+→\s+", txt) if x.strip()]
        if len(etapas) == 1:
            return out + '<div class="fs">' + etapa_html(etapas[0], a, b, imgs, bg) + '</div>'
        # duas etapas: a primeira sai e a segunda entra na palavra-chave (ou no meio da cena)
        t2 = min(max(_quando(etapas[1], a + (b - a) * 0.3, b, 0, 1), a + (b - a) * 0.3), a + (b - a) * 0.6)
        i1, i2 = nid("s"), nid("s")
        em(f"#{i1}", t2 - 0.25, "{opacity:1, y:0}", "{opacity:0, y:-60, filter:'blur(12px)'}", 0.3, "power2.in")
        return (out + f'<div class="fs" id="{i1}">' + etapa_html(etapas[0], a, t2, imgs, bg) + '</div>'
                + f'<div class="fs" id="{i2}">' + etapa_html(" · ".join(etapas[1:]), t2, b, [], bg) + '</div>')

def pedido_html(a, b, estado_txt):
    i = nid("f"); entra3d(f"#{i}", a + 0.02)
    s = [nid("o") for _ in range(3)]
    for k, x in enumerate(s): em(f"#{x}", a + 0.5 + k * 0.3, "{x:-40, opacity:0}", "{x:0, opacity:1}", 0.35)
    return (f'<div class="fone" id="{i}"><div class="scr"><div class="oh">Order #EV-48213</div>'
            '<div class="orow"><img src="assets/img/ev_1.png" width="150" height="268"><div><b>EreVanton</b><i>Testosterone support</i></div></div>'
            f'<div class="ost" id="{s[0]}"><u class="ok">✓</u>Order confirmed</div><div class="ost" id="{s[1]}"><u class="on">●</u>{estado_txt}</div>'
            f'<div class="ost dim" id="{s[2]}"><u>○</u>Shipped</div></div></div>')
# ---------------------------------------------------------------- V3 (30/10): ofertas e cores (comentários do copywriter no Frame.io)
# Psicologia das cores: verde = ganho/solução/preço da oferta/✓; vermelho = dor/risco/preço cheio riscado/✕.
def pcheio(t, txt, risca=None, tam=150, rot=""):  # preço cheio: vermelho; o risco (branco, para aparecer sobre o vermelho) entra na palavra
    i = nid("pc"); entra(f"#{i}", t, "{scale:.7, opacity:0, filter:'blur(14px)'}", "{scale:1, opacity:1, filter:'blur(0px)'}", 0.4, "back.out(2)")
    h = (f'<div class="pfull" id="{i}">' + (f'<span class="prot">{rot}</span>' if rot else "") + f'<span class="pv" style="font-size:{tam}px">{txt}')
    if risca is not None:
        x = nid("rk"); em(f"#{x}", risca, "{scaleX:0}", "{scaleX:1}", 0.3, "power2.out"); S(risca, "k_swish", 0.05, 0.57)
        h += f'<i class="risco2" id="{x}"></i>'
    return h + '</span></div>'
def poferta(t, txt, sub="", tam=300, som="cash"):  # preço da oferta: verde grande com extrusão
    i = nid("po"); bate(f"#{i}", t)
    if som: S(t, som, 0.12)
    return (f'<div class="numw" id="{i}"><div class="num grn" style="font-size:{tam}px">{txt}</div>'
            + (f'<div class="cond mid grn">{sub}</div>' if sub else "") + '</div>')
BOTTLE_H = 330  # Jhon 30/10: um frasco EreVanton = sempre a mesma altura em todas as telas; kits só repetem o frasco
KIT_N = {"ev_1.png": 1, "ev_3.png": 3, "ev_9.png": 9}
BW = round(BOTTLE_H * 476 / 851)  # largura do frasco recortado (ev_1.png 476×851)
def kit_html(n):
    pos = {1: [(0, 0)], 3: [(-175, 0), (175, 0), (0, 0)]}.get(n)
    if pos is None:  # 9 = 5 atrás + 4 na frente, todos do mesmo tamanho
        pos = [(-340 + 170 * k, -95) for k in range(5)] + [(-255 + 170 * k, 0) for k in range(4)]
    hh = BOTTLE_H + (95 if n > 3 else 0)
    imgs = "".join(f'<img src="assets/img/ev_1.png" style="position:absolute;left:50%;bottom:{-y}px;margin-left:{x - BW // 2}px;height:{BOTTLE_H}px;width:{BW}px;'
                   + ("filter:brightness(.8) drop-shadow(0 20px 26px rgba(0,0,0,.6))" if y < 0 or (n == 3 and x == 0 and False) else "filter:drop-shadow(0 26px 34px rgba(0,0,0,.65))") + '">'
                   for x, y in pos)
    return f'<div class="kit k{n}" style="position:relative;width:960px;height:{hh}px">{imgs}</div>'
def prods_html(t, imgs, h=430, cls=""):
    i = nid("pd")
    em(f"#{i}", t, "{y:300, rotationY:-50, z:-400, opacity:0, filter:'blur(24px)'}", "{y:0, rotationY:0, z:0, opacity:1, filter:'blur(0px)'}", 0.7)
    if imgs and all(x in KIT_N for x in imgs): return f'<div class="prods {cls}" id="{i}" style="height:auto">' + kit_html(sum(KIT_N[x] for x in imgs)) + '</div>'
    return f'<div class="prods {cls}" id="{i}" style="height:{h}px">' + "".join(f'<img src="assets/img/{x}">' for x in imgs) + '</div>'
def duas(a, b, t2, h1, h2):  # duas telas na mesma cena: a 1ª sai e a 2ª entra em t2
    i1 = nid("s")
    em(f"#{i1}", t2 - 0.25, "{opacity:1, y:0}", "{opacity:0, y:-60, filter:'blur(12px)'}", 0.3, "power2.in")
    return f'<div class="fs" id="{i1}">{h1}</div><div class="fs">{h2}</div>'
def setas_verdes(t):
    i = nid("sv"); entra(f"#{i}", t, "{y:-40, opacity:0}", "{y:0, opacity:1}", 0.4, "back.out(2)")
    js.append(f'tl.to("#{i} svg", {{y:14, duration:0.4, ease:"sine.inOut", yoyo:true, repeat:5, stagger:0.12}}, {r(t + 0.45)});')
    seta = '<svg viewBox="0 0 100 100"><path d="M50 12v62M24 50l26 26 26-26" fill="none" stroke="#2BD67B" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    return f'<div class="setasv" id="{i}">{seta * 3}</div>'
def cta_html(t, b):
    i = nid("ct")
    em(f"#{i}", t, "{scale:.4, opacity:0, filter:'blur(20px)'}", "{scale:1, opacity:1, filter:'blur(0px)'}", 0.45, "back.out(2)")
    js.append(f'tl.to("#{i} .bt", {{scale:1.04, duration:0.45, ease:"sine.inOut", yoyo:true, repeat:{max(1, int((b - t) / 0.45) - 2)}}}, {r(t + 0.5)});')
    js.append(f'tl.to("#{i} .seta", {{y:16, duration:0.4, ease:"sine.inOut", yoyo:true, repeat:{max(1, int((b - t) / 0.4) - 2)}}}, {r(t + 0.5)});')
    S(t, "k_pop", 0.09, 0.74)
    return f'<div class="cta-g rel" id="{i}"><div class="bt">{CTA_TXT}</div>{SETA}</div>'
# ---------------------------------------------------------------- 362_BM: telas especiais (pedido, preço, presentes)
def esp_pedido(a, b):
    t = ach("Please do not close this", a, b) or a + 2.5
    em("#al7", t, "{scale:.6, opacity:0}", "{scale:1, opacity:1}", 0.35, "back.out(2)")
    em("#al7", t + 0.4, "{x:0}", "{x:10, repeat:5, yoyo:true}", 0.05, "none"); S(t, "k_impacto", 0.09, 0.3)
    return pedido_html(a, b, "Packing your box…") + '<div class="alerta" id="al7">⚠ DON\'T CLOSE THIS PAGE</div>'
def esp_pedido2(a, b):
    i = nid("q"); t = ach("All you need to do", a, b) or a + (b - a) * 0.6
    entra(f"#{i}", a + 1.4, "{scale:.6, opacity:0}", "{scale:1, opacity:1}", 0.35, "back.out(2)"); S(a + 1.4, "ding", 0.05, 1.0)
    return pedido_html(a, b, "Being packed right now…") + f'<div class="chip big grn" id="{i}" style="position:absolute;left:50%;transform:translateX(-50%);top:1500px;white-space:nowrap">✓ 9 BOTTLES RESERVED</div>'
def esp_15(a, b):
    t15 = ach("for just $15 each,", a, b) or a + 0.6
    t1 = ach("less than $1 per", a, b) or a + (b - a) * 0.5; t2 = ach("less than $2 per", a, b) or t1 + 1.5
    c1, c2 = nid("k"), nid("k")
    entra(f"#{c2}", t2, "{scale:.6, opacity:0}", "{scale:1, opacity:1}", 0.35, "back.out(2)")
    S(t2, "k_clique", 0.15, 0.08)
    return ('<div class="fs top">' + poferta(t15 + 0.25, "$15", "PER BOTTLE", 320)
            + f'<div class="kbx2"><div class="chip big grn" id="{c2}">LESS THAN $2 A DAY</div></div></div>')
def esp_135(a, b):
    t = ach("For less than $140,", a, b) or a + 0.3; t3 = ach("3 times faster.", a, b) or a + (b - a) * 0.65
    k, x = nid("q"), nid("q"); entra(f"#{k}", a + 0.15); bate(f"#{x}", t3)
    return ('<div class="fs top">' + f'<div class="kick" id="{k}">9 BOTTLES × $15</div>' + poferta(t + 0.2, "$135", "TOTAL", 330)
            + setas_verdes(t + 0.7) + f'<div class="disp big" id="{x}"><span class="grn">3X</span> FASTER</div></div>')
def esp_15b(a, b):
    t = ach("the price of $15 per", a, b) or a + 1.5; td = ach("this price will disappear.", a, b)
    k = nid("q"); entra(f"#{k}", a + 0.2)
    h = ('<div class="fs top">' + poferta(t + 0.2, "$15", "PER BOTTLE", 300, "ding")
         + f'<div class="chip big" id="{k}">ONLY ON THIS PAGE</div>')
    if td:
        x = nid("q"); entra(f"#{x}", td, "{scale:.6, opacity:0}", "{scale:1, opacity:1}", 0.35, "back.out(2)")
        h += f'<div class="chip big red" id="{x}" style="margin-top:24px">✕ THEN THIS PRICE DISAPPEARS</div>'
    return h + '</div>'
def esp_gift(n, titulo, tipo, valor_frase):
    def f(a, b):
        c = nid("gf"); entra3d(f"#{c}", a + 0.05); S(a + 0.05, "k_pop", 0.08, 0.74)
        ico = ('<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="none" stroke="#FFD23F" stroke-width="6"/><path d="M41 32l28 18-28 18z" fill="#FFD23F"/></svg>' if tipo == "VIDEO LESSON"
               else '<svg viewBox="0 0 100 100"><rect x="20" y="12" width="60" height="76" rx="8" fill="none" stroke="#FFD23F" stroke-width="6"/><path d="M32 34h36M32 48h36M32 62h24" stroke="#FFD23F" stroke-width="6" stroke-linecap="round"/></svg>')
        return (f'<div class="fs"><div class="gift" id="{c}"><i>GIFT #{n}</i>{ico}<b>{titulo}</b><u>{tipo}</u></div></div>')
    return f
def esp_441(a, b):
    t = ach("worth over $400,", a, b) or a + 1.0; tz = ach("a single penny more", a, b) or a + (b - a) * 0.6
    c = nid("q"); entra(f"#{c}", tz, "{scale:.6, opacity:0}", "{scale:1, opacity:1}", 0.35, "back.out(2)"); S(tz, "ding", 0.06, 1.0)
    pilha = "".join(f'<div class="gmini g{k}"><i>GIFT #{k+1}</i><b>{nm}</b></div>' for k, nm in enumerate(["MASTER OF ORGASM", "MASTER OF FOREPLAY", "365 KAMA SUTRA"]))
    p_ = nid("gp"); entra3d(f"#{p_}", a + 0.05)
    return (f'<div class="fs top" style="gap:46px"><div class="gpilha" id="{p_}">{pilha}</div>' + poferta(t, "$441", "IN GIFTS", 230, "cash")
            + f'<div class="chip big grn" id="{c}" style="margin-top:10px">✓ $0 EXTRA</div></div>')

# ---------------------------------------------------------------- 362 rodada premium (Jhon 30/10): todo card em cena real, nunca a Jennifer borrada
BGDIR = os.path.join(H, "assets", "bg")
def imgs_bg(asset): return [x for x in re.findall(r"IMG:(\w+)", asset or "") if os.path.exists(os.path.join(BGDIR, x + ".jpg"))]
def bg_html(iid, a, b, escuro=True, cls="fbgi"):
    i = nid("bg")
    js.append(f'tl.fromTo("#{i} img", {{scale:1.14, x:0}}, {{scale:1.0, x:0, duration:{r(max(0.5, b - a))}, ease:"none", immediateRender:false}}, {a});')
    return f'<div class="{cls}" id="{i}"><img src="assets/bg/{iid}.jpg"></div>' + ('<div class="fgradi"></div>' if escuro else "")
def tela_quad(iid):  # cantos da tela branca: maior componente conexa clara (lâmpada/janela não entram)
    import numpy as np
    from PIL import Image
    from scipy import ndimage
    im = np.asarray(Image.open(os.path.join(BGDIR, iid + ".jpg")).convert("L")).astype(int)
    lab, n = ndimage.label(im > 228)
    if n == 0: raise SystemExit("tela branca não achada em " + iid)
    tam = ndimage.sum(np.ones_like(im), lab, range(1, n + 1)); k = int(np.argmax(tam)) + 1
    ys, xs = np.nonzero(lab == k); s_, d_ = xs + ys, xs - ys
    return [(xs[s_.argmin()], ys[s_.argmin()]), (xs[d_.argmax()], ys[d_.argmax()]), (xs[s_.argmax()], ys[s_.argmax()]), (xs[d_.argmin()], ys[d_.argmin()])]
def matrix3d(w, h, q):
    import numpy as np
    src = [(0, 0), (w, 0), (w, h), (0, h)]; A = []; B_ = []
    for (x, y), (u, v) in zip(src, q):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); B_.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); B_.append(v)
    a_, b_, c_, d_, e_, f_, g_, h_ = np.linalg.solve(np.array(A, float), np.array(B_, float))
    M_ = [a_, d_, 0, g_, b_, e_, 0, h_, 0, 0, 1, 0, c_, f_, 0, 1]
    return "matrix3d(" + ",".join(f"{x:.8f}" for x in M_) + ")"
def ui_pedido(a, b):
    i, s1, s2, bar = nid("ui"), nid("u"), nid("u"), nid("u")
    entra(f"#{s1}", a + 0.35, "{y:20, opacity:0}", "{y:0, opacity:1}", 0.35); entra(f"#{s2}", a + 0.9, "{y:20, opacity:0}", "{y:0, opacity:1}", 0.35)
    js.append(f'tl.fromTo("#{bar}", {{scaleX:.1}}, {{scaleX:.72, duration:{r(max(1, b - a - 1))}, ease:"sine.inOut", immediateRender:false}}, {r(a + 0.9)});')
    S(a + 0.35, "ding", 0.05, 1.0)
    return (f'<div class="ui" id="{i}"><div class="ub"><span>9:41</span><b>🔒 secure checkout</b><span>●●●</span></div>'
            f'<div class="uk" id="{s1}"><i>✓</i><h3>Thank you, Michael!</h3><p>Your order is confirmed</p></div>'
            '<div class="uc"><div class="ur"><span>Order number</span><b>#EV-48213</b></div>'
            '<div class="up"><img src="assets/img/ev_1.png"><div><b>EreVanton</b><span>Testosterone Support · 3-month supply</span></div></div>'
            '<div class="ur"><span>Shipping</span><b class="g">FREE</b></div><div class="ur"><span>Delivery</span><b>5–7 business days</b></div></div>'
            f'<div class="us" id="{s2}"><b>● Processing your order</b><span>Packing your box…</span><div class="ubar"><i id="{bar}"></i></div><em>Please don\'t close this page</em></div><div class="ubtn">Track your order</div></div>')
def ui_reembolso(a, b):
    i, s1, s2 = nid("ui"), nid("u"), nid("u")
    t2 = ach("we'll refund the full", a, b) or a + 2.5
    entra(f"#{s1}", a + 0.3, "{y:20, opacity:0}", "{y:0, opacity:1}", 0.35); entra(f"#{s2}", t2, "{scale:.6, opacity:0}", "{scale:1, opacity:1}", 0.4, "back.out(2)")
    S(t2, "ding", 0.06, 1.0)
    return (f'<div class="ui" id="{i}"><div class="ub"><span>9:41</span><b>Mail</b><span>●●●</span></div>'
            f'<div class="um" id="{s1}"><div class="uh"><u>To:</u> support@erevanton</div><div class="uh"><u>Subject:</u> Refund request</div><p>Hi, I would like a full refund for my order #EV-48213.</p><b class="send">Sent ✓</b></div>'
            f'<div class="uk g2" id="{s2}"><i>✓</i><h3>Refund issued</h3><p>Full amount · same day</p></div></div>')
TAM_UI = {}
def cena_celular(cid, tipo, ini, fim, iid, ui_fn, extra=None):
    @cena(cid, tipo, ini, fim, True, 11.0)
    def _(a, b):
        q_ = tela_quad(iid)
        import math
        W_, H_ = TAM_UI.get(iid) or (390, 844)
        if iid.endswith("_casal"):  # proporção pela tela detectada
            W_ = round(math.dist(q_[0], q_[1]) * 1.6); H_ = round(math.dist(q_[0], q_[3]) * 1.6)
        # tela um pouco maior que o branco detectado (cobre a borda arredondada)
        cx = sum(x for x, _ in q_) / 4; cy = sum(y for _, y in q_) / 4
        q2 = [(cx + (x - cx) * 1.012, cy + (y - cy) * 1.008) for x, y in q_]
        i = nid("ph")
        js.append(f'tl.fromTo("#{i}", {{scale:1.10}}, {{scale:1.0, duration:{r(max(0.5, b - a))}, ease:"none", immediateRender:false}}, {a});')
        return (f'<div class="phwrap" id="{i}"><img class="phbg" src="assets/bg/{iid}.jpg">'
                f'<div class="uiq" style="width:{W_}px;height:{H_}px;transform:{matrix3d(W_, H_, q2)}"><!--ui-->{ui_fn(a, b)}<!--/ui--></div></div>'
                + (extra(a, b) if extra else ""))
def triptico(a, b):  # 3 CAPSULES A DAY: manhã / tarde / noite reais + palma com 3 cápsulas
    t0 = ach("three capsules a day:", a, b) or a + 0.1
    t1, t2, t3 = t0 + 0.05, t0 + 0.35, t0 + 0.65
    out = '<div class="tri">'
    for k_, (iid, t_, rot) in enumerate([("cap_manha", t1, "MORNING"), ("cap_tarde", t2, "AFTERNOON"), ("cap_noite", t3, "NIGHT")]):
        j = nid("tp")
        em(f"#{j}", t_ - 0.15, "{clipPath:'inset(0 100% 0 0)', opacity:0}", "{clipPath:'inset(0 0% 0 0)', opacity:1}", 0.55, "expo.out")
        js.append(f'tl.fromTo("#{j} img", {{scale:1.15}}, {{scale:1.0, duration:{r(max(0.5, b - t_))}, ease:"none", immediateRender:false}}, {r(t_ - 0.15)});')
        S(t_ - 0.15, "k_swish", 0.05, 0.57)
        pos = {"cap_manha": "50% 16%", "cap_tarde": "50% 22%", "cap_noite": "50% 34%"}[iid]
        out += f'<div class="tpb" id="{j}"><img src="assets/bg/{iid}.jpg" style="object-position:{pos}"><span>{rot}</span></div>'
    k = nid("q"); entra(f"#{k}", a + 0.1)
    jb = nid("tb"); js.append(f'tl.fromTo("#{jb} img", {{scale:1.2}}, {{scale:1.1, duration:{r(max(0.5, b - a))}, ease:"none", immediateRender:false}}, {a});')
    return (f'<div class="fbgi tribgr" id="{jb}"><img src="assets/bg/cap_manha.jpg"></div><div class="fgradi"></div>' + out + '</div>' + f'<div class="trik" id="{k}"><b>3</b><span>CAPSULES A DAY</span></div>')
def meses(a, b):  # MONTH 1 → 2 → 3 no mesmo vaso + barra que trava em PERMANENT
    ts = [a, ach("because that's how long", a, b) or a + (b - a) * .35, ach("to fully regenerate", a, b) or a + (b - a) * .6]
    tp_ = ach("permanently sealed.", a, b) or a + (b - a) * .85
    out = ""
    for k_, (iid, t_) in enumerate(zip(["vaso_m1b", "vaso_m2", "vaso_m3"], ts)):
        j = nid("mv")
        if k_: em(f"#{j}", t_ - 0.2, "{opacity:0}", "{opacity:1}", 0.5, "sine.inOut")
        js.append(f'tl.fromTo("#{j} img", {{scale:1.12}}, {{scale:1.0, duration:{r(max(0.5, b - t_))}, ease:"none", immediateRender:false}}, {r(t_ - 0.2)});')
        out += f'<div class="fbgi" id="{j}"><img src="assets/bg/{iid}.jpg"></div>'
    out += '<div class="fgradi"></div>'
    ms = ""
    for k_, t_ in enumerate(ts):
        j = nid("mm"); em(f"#{j}", t_ - 0.1, "{opacity:.35, scale:.9}", "{opacity:1, scale:1}", 0.35, "back.out(2)"); S(t_, "k_clique", 0.15, 0.08)
        ms += f'<b id="{j}">MONTH {k_ + 1}</b>'
    bar, lk = nid("pb"), nid("pl")
    js.append(f'tl.fromTo("#{bar}", {{scaleX:0}}, {{scaleX:1, duration:{r(max(0.5, tp_ - a - 0.2))}, ease:"none", immediateRender:false}}, {r(a + 0.2)});')
    em(f"#{lk}", tp_, "{scale:2, opacity:0, filter:'blur(16px)'}", "{scale:1, opacity:1, filter:'blur(0px)'}", 0.45, "back.out(2)"); S(tp_, "k_impacto", 0.09, 0.3)
    return (out + '<div class="mes"><div class="kick">THE FOLLOWING MONTHS</div><div class="mrow">' + ms + '</div>'
            f'<div class="mbar"><i id="{bar}"></i></div><div class="disp big mlk" id="{lk}">🔒 <span class="grn">PERMANENT</span></div></div>')

PC_T0 = [0.0]
def preco_card(a, b, corpo, tag=""):
    i = nid("pc")
    js.append(f'tl.fromTo("#{i}", {{x:-90, opacity:0, scale:.94}}, {{x:0, opacity:1, scale:1, duration:0.5, ease:"power3.out", immediateRender:false}}, {r(a + 0.25)});')
    js.append(f'tl.set("#{i}", {{opacity:0}}, 0);')
    return LOGO("pclogo") + f'<div class="pcard2" id="{i}">' + (f'<i class="pctag">{tag}</i>' if tag else "") + corpo + '</div>'
def pc_num(t, val, unid):
    t = min(t, PC_T0[0] + 0.55)
    i = nid("pn"); em(f"#{i}", t, "{y:30, opacity:0, filter:'blur(10px)'}", "{y:0, opacity:1, filter:'blur(0px)'}", 0.45, "power3.out"); S(t, "cash", 0.1)
    return f'<div class="pnum" id="{i}"><sup>$</sup>{val}<em>{unid}</em></div>'
def pc_chip(t, txt, cor="g"):
    i = nid("pk"); em(f"#{i}", t, "{x:-40, opacity:0}", "{x:0, opacity:1}", 0.35, "power3.out"); S(t, "k_clique", 0.15, 0.08)
    return f'<div class="pchip2 {cor}" id="{i}">{txt}</div>'
def pr_48(a, b):
    PC_T0[0] = a; t9 = a + 0.6; i = nid("pn"); em(f"#{i}", t9 - 0.1, "{scale:.6, opacity:0}", "{scale:1, opacity:1}", 0.45, "back.out(2)")
    return preco_card(a, b, f'<div class="pnum" id="{i}">9<em> BOTTLES</em></div><div class="psub">EreVanton · additional supply</div>', "FIRST-TIME BUYERS ONLY")
def pr_49(a, b):
    PC_T0[0] = a; t15 = ach("for just $15 each,", a, b) or a + 0.6; t2 = ach("less than $2 per", a, b) or a + (b - a) * .7
    return preco_card(a, b, pc_num(t15 + 0.2, "15", "/bottle") + '<div class="ptot">$135 total · 9 bottles</div>' + pc_chip(t2, "✓ LESS THAN $2 A DAY"), "TODAY ONLY")
def pr_52(a, b):
    PC_T0[0] = a; t = ach("For less than $140,", a, b) or a + 0.3; t3 = ach("3 times faster.", a, b) or a + (b - a) * .65
    return preco_card(a, b, pc_num(t + 0.25, "135", " total") + '<div class="ptot">9 bottles × $15</div>' + pc_chip(t3, "⚡ 3X FASTER RESULTS"), "LESS THAN $140")
def pr_87(a, b):
    PC_T0[0] = a; t = ach("the price of $15 per", a, b) or a + 1.5; td = ach("this price will disappear.", a, b) or b - 1.5
    return preco_card(a, b, pc_num(t + 0.2, "15", "/bottle") + '<div class="ptot">$135 total · free shipping</div>' + pc_chip(td, "✕ THEN THIS PRICE DISAPPEARS", "r"), "ONLY ON THIS PAGE")
def pr_74(a, b):
    its = [("That's $135 for the", "✓ $135 · 9 BOTTLES"), ("That's $441 in gifts", "✓ $441 GIFTS FREE"), ("plus 1 full year", "✓ 1-YEAR GUARANTEE")]
    h = "".join(pc_chip((ach(f, a, b) or a + 0.5 + k * 1.5), t_) for k, (f, t_) in enumerate(its))
    return preco_card(a, b, '<div class="psub2">TODAY</div>' + h, "YOUR ORDER")
PRICE_R = {"That's why, right now, exclusively on": ("img:kit_a", pr_48), "That's 9 full bottles for just": ("img:kit_b", pr_49),
           "For less than $140, you'll get": ("img:kit_c", pr_52), "Your order will be shipped in": ("img:kit_i", pr_87),
           "That's $135 for the remaining 60": ("img:kit_e", pr_74)}
def gift_tag(a, b, n, val):
    i, x, f = nid("gt"), nid("rk"), nid("gf")
    em(f"#{i}", a + 0.3, "{y:-40, opacity:0}", "{y:0, opacity:1}", 0.4, "back.out(2)")
    tv = ach("Value: $" + val + ".", a, b) or b - 1.6
    em(f"#{x}", tv + 0.3, "{scaleX:0}", "{scaleX:1}", 0.3, "power2.out"); S(tv + 0.3, "k_swish", 0.05, 0.57)
    em(f"#{f}", tv + 0.6, "{scale:.5, opacity:0}", "{scale:1, opacity:1}", 0.4, "back.out(2)"); S(tv + 0.6, "ding", 0.06, 1.0)
    return (LOGO("corner") + f'<div class="gtag" id="{i}"><b>GIFT #{n}</b><span class="gval">${val}<i class="risco2" id="{x}"></i></span><span class="gfree" id="{f}">FREE</span></div>')
def ui_video(titulo):
    def f(a, b):
        bar = nid("vb")
        js.append(f'tl.fromTo("#{bar}", {{scaleX:.05}}, {{scaleX:.55, duration:{r(max(1, b - a))}, ease:"none", immediateRender:false}}, {a});')
        return (f'<div class="uiv"><img src="assets/bg/gift_thumb.jpg"><div class="uivg"></div><div class="uivt"><i>VIDEO LESSON</i><b>{titulo}</b></div>'
                f'<div class="uivp">▶</div><div class="uivbar"><i id="{bar}"></i></div></div>')
    return f
def ui_ebook(titulo, sub):
    def f(a, b):
        pg = nid("pg"); js.append(f'tl.fromTo("#{pg}", {{rotationY:0}}, {{rotationY:-160, duration:0.9, ease:"power2.inOut", immediateRender:false}}, {r(b - 1.6)});')
        return (f'<div class="uie"><div class="uiec"><i>THE COMPLETE GUIDE</i><b>{titulo}</b><em>{sub}</em><div class="orn">❦</div></div>'
                f'<div class="uiep" id="{pg}"></div></div>')
    return f
GIFT_B = {"The first gift is Master of": ("gift1_casal", ui_video("MASTER OF ORGASM"), 1, "197", 1180, 760),
          "The second gift is Master of": ("gift2_laptop", ui_video("MASTER OF FOREPLAY"), 2, "197", 1280, 800),
          "The third gift is The 365": ("gift3_casal", (lambda a, b: ui_ebook2("365 KAMA SUTRA POSITIONS", "A new position for every day of the year")(a, b)), 3, "47", 600, 860)}
def oferta_some(a, b):  # relógio é o foco: contagem 05:00 grande + headline vermelha
    i, k = nid("cd"), nid("q"); t0 = a + 0.2
    js.append(f'(function(){{var o={{v:300}};tl.to(o,{{v:300-{r(b - a)}*6,duration:{r(b - a)},ease:"none",onUpdate:function(){{var s=Math.max(0,Math.round(o.v));var e=document.getElementById("{i}");if(e)e.textContent=String(Math.floor(s/60)).padStart(2,"0")+":"+String(s%60).padStart(2,"0");}}}},{r(t0)});}})();')
    entra(f"#{k}", a + 0.15); bate(f"#{i}w", a + 0.3)
    return (LOGO("topo") + '<div class="fs top">' + '<div class="disp big red" id="' + k + '">THIS OFFER<br>DISAPPEARS</div>'
            f'<div class="cdw" id="{i}w"><b id="{i}">05:00</b><span>WHILE YOUR ORDER IS PROCESSED</span></div></div>')
def aceita(a, b):  # ✓ ACCEPT IT ALL × ✕ LET IT PASS, grandes
    tl_ = ach("or let this opportunity", a, b) or a + (b - a) * .55
    g, x_ = nid("ac"), nid("ac"); entra3d(f"#{g}", a + 0.2); entra3d(f"#{x_}", tl_ - 0.1); S(a + 0.2, "k_pop", 0.08, 0.74); S(tl_, "k_impacto", 0.08, 0.3)
    return (LOGO("topo") + '<div class="fs top">' + '<div class="kick">YOUR CHOICE</div>'
            f'<div class="duo"><div class="dcard g" id="{g}"><b>✓</b><span>ACCEPT<br>IT ALL</span></div>'
            f'<div class="dcard r" id="{x_}"><b>✕</b><span>LET IT<br>PASS</span></div></div></div>')

def LOGO(cls=""): return f'<div class="evlg {cls}"><img src="assets/img/ev_logo.png"><span>TESTOSTERONE SUPPORT*</span></div>'
COVERS = [("VIDEO LESSON", "MASTER OF ORGASM", "v"), ("VIDEO LESSON", "MASTER OF FOREPLAY", "v"), ("E-BOOK", "365 KAMA SUTRA POSITIONS", "e")]
def presentes_caixa(iid, valor, rot):
    def f(a, b):
        out = bg_html(iid, a, b)
        frases = ["The first gift", "The second gift", "The third gift"]
        ts = [a + 0.35, a + 0.95, a + 1.55]
        cv = ""
        for k_, ((tp_, tit, kind), t_) in enumerate(zip(COVERS, ts)):
            j = nid("cv")
            em(f"#{j}", t_, "{y:-260, x:120, rotation:18, opacity:0, filter:'blur(14px)'}", "{y:0, x:0, rotation:" + str([-7, -2, 4][k_]) + ", opacity:1, filter:'blur(0px)'}", 0.6, "back.out(1.4)")
            S(t_, "k_pop", 0.07, 0.74)
            ico = "▶" if kind == "v" else "❦"
            capa_ = {0: "capa_orgasm.jpg", 1: "capa_foreplay.jpg", 2: "capa_ebook.jpg"}[k_]
            cv += (f'<div class="gcov img g{k_}" id="{j}"><img src="assets/img/{capa_}"></div>' if os.path.exists(os.path.join(H, "assets", "img", capa_))
                   else f'<div class="gcov {kind} g{k_}" id="{j}"><i>{tp_}</i><b>{tit}</b><u>{ico}</u></div>')
        t2 = a + 2.4; i1, i2 = nid("q"), nid("q")
        em(f"#{i1}", t2, "{scale:.6, opacity:0}", "{scale:1, opacity:1}", 0.45, "back.out(2)"); S(t2, "cash", 0.1)
        em(f"#{i2}", t2 + 0.5, "{scale:.6, opacity:0}", "{scale:1, opacity:1}", 0.35, "back.out(2)")
        return (out + f'<div class="gcovs">{cv}</div>'
                + LOGO("topo") + '<div class="fs top" style="gap:18px">' + f'<div class="numw" id="{i1}"><div class="num grn" style="font-size:190px">{valor}</div><div class="cond mid grn">{rot}</div></div>'
                + f'<div class="chip big grn" id="{i2}">✓ $0 EXTRA</div></div>')
    return f
def ui_compra(a, b):
    i, bt, ok, rp = nid("ui"), nid("u"), nid("u"), nid("u")
    tt = ach("All you need to do", a, b) or a + (b - a) * .7
    em(f"#{bt}", tt + 0.6, "{scale:1}", "{scale:.92}", 0.12, "power2.out")
    em(f"#{rp}", tt + 0.6, "{scale:0, opacity:.7}", "{scale:3, opacity:0}", 0.5, "power2.out")
    em(f"#{ok}", tt + 1.0, "{scale:.7, opacity:0}", "{scale:1, opacity:1}", 0.35, "back.out(2)"); S(tt + 0.6, "click", 0.2); S(tt + 0.9, "ding", 0.06, 1.0)
    return (f'<div class="ui" id="{i}"><div class="ub"><span>9:41</span><b>🔒 secure checkout</b><span>●●●</span></div>'
            '<div class="uc"><div class="ur"><span>Special offer · this page only</span></div>'
            '<div class="up2"><img src="assets/bg/kit_b.jpg"><div><b>EreVanton · 9 bottles</b><span>Accelerated protocol supply</span><em>$15/bottle · $135 total</em></div></div>'
            '<div class="ur"><span>Shipping</span><b class="g">FREE</b></div><div class="ur"><span>One-time payment</span><b>No subscription</b></div></div>'
            f'<div class="uk" id="{ok}"><i>✓</i><h3>Order confirmed</h3><p>Added to the same box · ships free</p></div>'
            f'<div class="ubig" id="{bt}"><i id="{rp}"></i>YES, I WANT TO ACCELERATE MY RESULTS</div></div>')

LINHA_SVG = ('<svg viewBox="0 0 200 200" class="lsvg"><path d="M70 40c-14 0-22 12-20 26 2 13 12 18 14 30 3 18-10 30-6 52 3 16 18 26 32 26" fill="none" stroke="#d9a86c" stroke-width="3" stroke-linecap="round"/>'
             '<path d="M128 38c14 2 21 14 18 28-3 12-13 17-15 29-2 17 9 31 4 52-4 15-19 24-33 24" fill="none" stroke="#f3dcc0" stroke-width="3" stroke-linecap="round"/>'
             '<circle cx="70" cy="34" r="12" fill="none" stroke="#d9a86c" stroke-width="3"/><circle cx="130" cy="32" r="12" fill="none" stroke="#f3dcc0" stroke-width="3"/>'
             '<path d="M64 92c18 10 54 10 72 0" fill="none" stroke="#d9a86c" stroke-width="2.5" stroke-linecap="round" opacity=".8"/></svg>')
def ui_ebook2(titulo, sub):
    def f(a, b):
        pg = nid("pg"); tf = a + min(3.0, (b - a) * .45)
        js.append(f'tl.fromTo("#{pg}", {{rotationY:-178, opacity:0}}, {{rotationY:0, opacity:1, duration:0.8, ease:"power2.inOut", immediateRender:false}}, {r(tf)});')
        S(tf, "k_swish", 0.05, 0.57)
        return (f'<div class="uie"><div class="uiec"><i>THE COMPLETE GUIDE</i><b>{titulo}</b><em>{sub}</em><div class="orn">❦</div></div>'
                f'<div class="uiep2" id="{pg}"><i>POSITION 1 OF 365</i><b>The Embrace</b>{LINHA_SVG}<p>Start slow. Face each other, breathe together and let the connection build before anything else.</p><u>— 1 —</u></div></div>')
    return f
def gift2_cena(a, b):
    src_v = "assets/ia3/gift2_casal.mp4"
    fundo_ = media(src_v, a, b) if os.path.exists(os.path.join(H, src_v)) else bg_html("gift2_casal", a, b, False, "fill2")
    c, bar = nid("ch"), nid("cb"); entra(f"#{c}", a + 0.5, "{y:40, opacity:0, filter:'blur(12px)'}", "{y:0, opacity:1, filter:'blur(0px)'}", 0.5)
    js.append(f'tl.fromTo("#{bar}", {{scaleX:.08}}, {{scaleX:.42, duration:{r(max(1, b - a))}, ease:"none", immediateRender:false}}, {a});')
    return (fundo_ + '<div class="gradt"></div>' + gift_tag(a, b, 2, "197")
            + f'<div class="chap" id="{c}"><i>VIDEO LESSON · CHAPTER 1</i><b>MASTER OF FOREPLAY</b><span>Awakening desire before you even begin</span>'
            f'<div class="chbar"><u>▶</u><div class="chtrk"><em id="{bar}"></em></div><span>04:12 / 18:40</span></div></div>')
GIFTS_INFO = {"The first gift is Master of": (1, "MASTER OF ORGASM", "VIDEO LESSON", "197", "gift1_casal2"),
              "The second gift is Master of": (2, "MASTER OF FOREPLAY", "VIDEO LESSON", "197", "gift2_casal"),
              "The third gift is The 365": (3, "365 KAMA SUTRA POSITIONS", "E-BOOK", "47", "gift3_casal3")}
def gift_cena(n, titulo, tipo_, val, iid):
    def f(a, b):
        v_ = f"assets/ia3/{iid}.mp4"
        fundo_ = media(v_, a, b) if os.path.exists(os.path.join(H, v_)) else bg_html(iid, a, b, False, "fill2")
        c, x, fr = nid("gc"), nid("rk"), nid("gf")
        entra(f"#{c}", a + 0.25, "{y:-60, opacity:0, filter:'blur(14px)'}", "{y:0, opacity:1, filter:'blur(0px)'}", 0.55)
        tv = ach("Value: $" + val + ".", a, b) or b - 1.6
        em(f"#{x}", tv + 0.3, "{scaleX:0}", "{scaleX:1}", 0.3, "power2.out"); S(tv + 0.3, "k_swish", 0.05, 0.57)
        em(f"#{fr}", tv + 0.6, "{scale:.5, opacity:0}", "{scale:1, opacity:1}", 0.4, "back.out(2)"); S(tv + 0.6, "ding", 0.06, 1.0)
        S(a + 0.25, "k_pop", 0.08, 0.74)
        ebk = ""
        capa_g = {1: "capa_orgasm.jpg", 2: "capa_foreplay.jpg", 3: "capa_ebook.jpg"}[n]
        if os.path.exists(os.path.join(H, "assets", "img", capa_g)):
            jc = nid("cp"); em(f"#{jc}", a, "{scale:.92, opacity:.4}", "{scale:1, opacity:1}", 0.3, "power2.out")
            js.append(f'tl.to("#{jc}", {{x:330, y:-430, scale:.42, rotation:4, duration:0.7, ease:"power3.inOut"}}, {r(a + 1.1)});')
            dm = nid("dm"); js.append(f'tl.fromTo("#{dm}", {{opacity:1}}, {{opacity:0, duration:0.6, immediateRender:false}}, {r(a + 1.1)});')
            ebk = f'<div class="gdim" id="{dm}"></div>'
            ebk += f'<img class="gcover" id="{jc}" src="assets/img/{capa_g}">'
        return (fundo_ + ebk + '<div class="ggrad"></div>' + f'<div class="gcard" id="{c}">' + LOGO("sm")
                + f'<div class="gline"><b>GIFT #{n}</b><i>{tipo_}</i></div><div class="gtit">{titulo}</div>'
                + f'<div class="gvals"><span class="gval">${val}<i class="risco2" id="{x}"></i></span><span class="gfree" id="{fr}">FREE</span></div></div>')
    return f

def tres_caps(a, b):  # "you take three capsules a day instead of just one": 1 → 3, número grande nas palmas
    t3 = ach("three capsules a day", a, b) or a + (b - a) * .45
    j1, j2, n1, n3 = nid("pa"), nid("pa"), nid("q"), nid("q")
    js.append(f'tl.fromTo("#{j1} img", {{scale:1.1}}, {{scale:1.0, duration:{r(max(0.5, b - a))}, ease:"none", immediateRender:false}}, {a});')
    em(f"#{j2}", t3 - 0.15, "{opacity:0}", "{opacity:1}", 0.35, "sine.inOut")
    js.append(f'tl.fromTo("#{j2} img", {{scale:1.1}}, {{scale:1.0, duration:{r(max(0.5, b - t3))}, ease:"none", immediateRender:false}}, {r(t3 - 0.15)});')
    bate(f"#{n1}", a + 0.2); em(f"#{n1}", t3 - 0.2, "{opacity:1}", "{opacity:0}", 0.2, "power2.in"); bate(f"#{n3}", t3)
    return (f'<div class="fbgi" id="{j1}"><img src="assets/bg/cap_palma12.jpg"></div><div class="fbgi" id="{j2}"><img src="assets/bg/cap_palma32.jpg"></div><div class="fgradi"></div>'
            + LOGO("topo") + f'<div class="fs top"><div class="numw" id="{n1}"><div class="num yel" style="font-size:330px">1</div><div class="cond mid">CAPSULE A DAY</div></div></div>'
            + f'<div class="fs top"><div class="numw" id="{n3}"><div class="num grn" style="font-size:330px">3</div><div class="cond mid grn">CAPSULES A DAY</div></div></div>')
def ritmo(a, b):  # NORMAL PACE × ACCELERATED PACE em dois blocos iguais, acelerado em destaque
    tl_ = ach("or the accelerated pace?", a, b) or a + (b - a) * .55
    g, x_ = nid("ac"), nid("ac"); entra3d(f"#{g}", a + 0.2); entra3d(f"#{x_}", tl_ - 0.1); S(a + 0.2, "k_pop", 0.08, 0.74); S(tl_, "k_impacto", 0.08, 0.3)
    return (bg_html("bg_estrada2", a, b) + LOGO("topo") + '<div class="fs top"><div class="kick">WHICH PATH?</div>'
            f'<div class="duo"><div class="dcard n" id="{g}"><b>⏳</b><span>NORMAL<br>PACE</span><em>MONTHS</em></div>'
            f'<div class="dcard g big" id="{x_}"><b>⚡</b><span>ACCELERATED<br>PACE</span><em>WEEKS</em></div></div></div>')
def presentes_soltos(a, b):
    f_ = presentes_caixa("bg_presentes2", "$400+", "IN GIFTS")
    return f_(a, b).replace('class="gcovs"', 'class="gcovs solo"')

def ebook_capa():
    return ('<div class="ebc"><i>THE COMPLETE GUIDE</i><b>365 KAMA SUTRA POSITIONS</b><em>A new position for every day of the year</em>'
            '<div class="orn">❦</div><div class="ebsel">E-BOOK</div><div class="ebmk"><img src="assets/img/ev_logo.png"></div><div class="ebsh"></div></div>')
def ebook_layer(a, dur=2.6):
    import math
    q_ = tela_quad("ebook_mock"); W_ = round(math.dist(q_[0], q_[1]) * 1.4); H_ = round(math.dist(q_[0], q_[3]) * 1.4)
    cx = sum(x for x, _ in q_) / 4; cy = sum(y for _, y in q_) / 4
    q2 = [(cx + (x - cx) * 1.01, cy + (y - cy) * 1.006) for x, y in q_]
    i = nid("eb"); js.append(f'tl.fromTo("#{i}", {{scale:1.06}}, {{scale:1.0, duration:{dur}, ease:"none", immediateRender:false}}, {a});')
    js.append(f'tl.to("#{i}", {{opacity:0, duration:0.35, ease:"sine.inOut"}}, {r(a + dur - 0.35)});')
    return (f'<div class="phwrap ebw" id="{i}"><img class="phbg" src="assets/bg/ebook_mock.jpg">'
            f'<div class="uiq" style="width:{W_}px;height:{H_}px;border-radius:4px;transform:{matrix3d(W_, H_, q2)}"><!--ui-->{ebook_capa()}<!--/ui--></div></div>')
ESPECIAIS = {}  # preenchido por frase de entrada (os números da tabela mudam quando o storyboard é editado)
ESP_FRASE = {"On top of that, I want": presentes_soltos, "With the accelerated protocol, you take": tres_caps, "The only question left is: do": ritmo, "And as soon as your order": oferta_some, "You just need to stay with": aceita, "That's three capsules a day: one": triptico, "The following months make those results": meses,
             
             "These three gifts, which together are": presentes_caixa("kit_f", "$441", "IN GIFTS")}


def cena_T(L):
    txt = L["texto"]
    kick = re.search(r"kicker\s+(.*?)\s+·\s+título", txt); tit = re.search(r"título\s+(.*?)(?:\s*\(|$)", txt)
    bt = re.search(r"bate em '([^']+)'", txt)
    TB(f"c{L['n']:03d}", L["ini"], L["fim"], f"assets/ia3/{novo(L['asset'])}.mp4", limpa(kick.group(1)) if kick else "",
       colore(limpa(tit.group(1)) if tit else limpa(txt)), cls="glowr" if "glowr" in txt else ("glowy" if "glowy" in txt else ""), modo="bate" if bt else "entra")

def extras_broll(L):
    txt = L["texto"]
    def f(a, b):
        out, chips = "", []
        for m in re.finditer(r"letra_em(?: '([^']+)')?:\s*(.+?)(?=\s+·\s+chip|\s+→\s+chip|$)", txt):
            fr, tx = m.group(1), limpa(m.group(2)); i = nid("l"); t = (ach(fr, a, b) if fr else None) or a + 0.3
            bate(f"#{i}", t); out += f'<div class="tgrad"></div><div class="disp big c tback" id="{i}" style="top:84px;font-size:118px">{colore(tx)}</div>'
        m = re.search(r"bate:\s*([^·]+?)(?=\s+·|$)", txt)
        if m:
            i = nid("l"); bate(f"#{i}", a + 0.15); out += f'<div class="tgrad"></div><div class="disp big c tback" id="{i}" style="top:170px">{colore(limpa(m.group(1)))}</div>'
        for m in re.finditer(r"chip_em '([^']+)':\s*([^→·(]+)", txt): chips.append((ach(m.group(1), a, b) or a + 0.3, limpa(m.group(2))))
        if "FREE SHIPPING · SAME BOX" in txt:
            i = nid("lc"); entra(f"#{i}", a + 0.3, "{y:-60, opacity:0, filter:'blur(14px)'}", "{y:0, opacity:1, filter:'blur(0px)'}", 0.5)
            return out + f'<div class="evcard" id="{i}">{LOGO()}<div class="chip big grn">✓ FREE SHIPPING · SAME BOX</div></div>'
        for m in re.finditer(r"chip(?: em '([^']+)')?:\s*([^→(]+?)(?=\s+·\s+letra|\s+→|$)", txt):
            if "chip_em" in txt[max(0, m.start() - 3):m.start() + 4]: continue
            fr = m.group(1); chips.append(((ach(fr, a, b) if fr else None) or a + 0.3, limpa(m.group(2))))
        m = re.search(r"chips[^:]*:\s*(.+)$", txt)
        if m:
            its = [x for x in re.split(r"\s+·\s+", m.group(1)) if x.strip()]
            for k, x in enumerate(its): chips.append((quando(x, a, b, k, len(its)), limpa(x)))
        if chips:
            hs = ""
            for t, tx in sorted(chips)[:4]:
                i = nid("k"); entra(f"#{i}", t, "{scale:.6, opacity:0}", "{scale:1, opacity:1}", 0.35, "back.out(2)"); S(t, "k_clique", 0.15, 0.08)
                hs += f'<div class="chip big {tom(tx)}" id="{i}">{tx if tom(tx) else colore(tx)}</div>'
            out += '<div class="gradb"></div><div class="kbx col">' + hs + '</div>'
        return out
    return f

DEPO_BROLL = {"DP_klaus": ("Everything happened so quickly that", "p_klaus_frasco_vazio2"), "DP_mark": ("I became the man I", "p_mark_esposa")}
def depo_broll(d, a, b):  # corte para o b-roll do desfecho no meio do depoimento (camada por cima do vídeo dele; a voz continua)
    if d["id"] not in DEPO_BROLL: return ""
    fr, nm = DEPO_BROLL[d["id"]]; src = f"assets/ia3/{nm}.mp4"
    if not os.path.exists(os.path.join(H, src)): return ""
    t = ach(fr, a, b)
    if t is None: return ""
    t = q(t - 0.1); e_ = min(b, t + 4.2); i = nid("db")
    js.append(f'tl.set("#{i}", {{opacity:0}}, 0); tl.fromTo("#{i}", {{opacity:0, scale:1.08}}, {{opacity:1, scale:1, duration:0.35, ease:"sine.out", immediateRender:false}}, {t}); tl.to("#{i}", {{opacity:0, duration:0.3}}, {r(e_ - 0.3)});')
    LUZES.append(t)
    return f'<div class="dbr" id="{i}">' + media(src, t, e_) + '</div>'
DEP_JANELAS_ = None
def DEP_JANELAS(): return [(d["ini"] - 0.15, d["ini"] - 0.15 + dur(os.path.join(H, "assets", "depo", d["id"] + ".mp4"))) for d in DEPO]
for d in DEPO:
    ini = d["ini"] - 0.15; du = dur(os.path.join(H, "assets", "depo", d["id"] + ".mp4"))
    @cena("dp_" + d["id"].lower(), "B", ini, ini + du - 0.04, d["fim"] - d["ini"] > 5, 60)
    def _(a, b, d=d):
        TRK[0] += 1; i = "dp" + d["id"].lower()
        em(f"#{i}t", a + 0.25, "{x:-300, opacity:0, filter:'blur(14px)'}", "{x:0, opacity:1, filter:'blur(0px)'}", 0.45)
        return (f'<video id="{i}v" class="clip fill" src="assets/depo/{d["id"]}.mp4" playsinline data-start="{q(a)}" data-duration="{r(b - a)}" data-track-index="{TRK[0]}" data-has-audio="true" data-volume="1"></video>'
                + depo_broll(d, a, b) +
                f'<div class="tarja" id="{i}t"><b>{TARJA[d["id"]].split(" · ")[0]}</b><span>{TARJA[d["id"]].split(" · ")[1]} · EreVanton customer</span></div>')
ANAT = []
CTA_D = []
ATRAS = []  # 362 (Jhon 30/10): lettering de destaque ATRÁS da Jennifer, com o recorte alpha dela por cima
# frases de entrada/saída e montagem dos momentos
for k, L in enumerate(LINHAS):
    fr = aspas(L["frases"]); L["ini"] = fr[0]; L["fim"] = fr[1] if len(fr) > 1 and not fr[1].startswith("(") else FIM
    if L["ini"] in ESP_FRASE: ESPECIAIS[L["n"]] = ESP_FRASE[L["ini"]]
for k, L in enumerate(LINHAS):
    if L["fim"] is None: L["fim"] = ("+", 6.0)
    tp = L["tipo"]
    if tp == "D" and "atrás:" in L["texto"]:
        _cursor[0] = 0.0; a_ = achar(L["ini"]); b_ = achar(L["fim"], a_ + 0.1) if isinstance(L["fim"], str) else FIM
        ATRAS.append((f"a{L['n']:03d}", a_, min(b_, a_ + 6.0), limpa(L["texto"].split("atrás:", 1)[1].split(" · legenda")[0])))
    if tp == "D" and L["texto"].startswith("CTA:"):
        _cursor[0] = 0.0; a_ = q(achar(L["ini"]) - 0.1); b_ = q(achar(L["fim"], a_ + 0.1))
        CTA_D.append((a_, b_))
    if tp in ("D", "D2"): continue
    try:
        _cursor[0] = 0.0; t_ini = achar(L["ini"])
    except SystemExit:
        t_ini = None
    if t_ini is not None and any(a_ - 0.1 <= t_ini < b_ - 0.3 for a_, b_ in DEP_JANELAS()): continue
    if L is LINHAS[-1] and CTA_TXT in L["texto"].upper(): continue  # o fim já tem o CTA fixo; não duplicar o botão
    if tp in ("F", "M"): cena_F(L, "M" if tp == "M" else "F")
    elif tp == "A3D":
        var = (re.search(r"variante (\w+)", L["visual"]) or [None, "mechanism"])[1]
        def _a3d(a, b, L=L, var=var):
            ANAT.append(1); k_ = re.search(r"kicker\s+(.*?)\s+·\s+título\s+(.*)$", L["texto"])
            h = (f'<canvas id="anatomia-c{L["n"]:03d}" class="clip fill" data-anatomia="{var}" data-start="{a}" data-duration="{r(b - a)}" width="1080" height="1920" '
                 'data-layout-ignore="true" aria-label="Medical 3D illustration of arterial inflow and cavernous tissue expansion"></canvas><div class="tgrad"></div>')
            if k_:
                i = nid("an"); entra(f"#{i}", a + 0.2)
                h += f'<div class="kick c" style="top:110px">{limpa(k_.group(1))}</div><div class="disp big c tback" id="{i}" style="top:170px">{colore(limpa(k_.group(2)))}</div>'
            return h
        cena(f"c{L['n']:03d}", "B", L["ini"], L["fim"], True, 8.0)(_a3d)
    elif L["ini"] in PRICE_R:
        vid, fn = PRICE_R[L["ini"]]
        def _pr(a, b, vid=vid, fn=fn):
            if vid.startswith("img:"):
                j_ = nid("bg")
                js.append(f'tl.fromTo("#{j_} img", {{scale:1.03}}, {{scale:1.0, duration:{r(max(0.5, b - a))}, ease:"none", immediateRender:false}}, {a});')
                fundo_ = f'<div class="fill2 prbg" id="{j_}"><img src="assets/bg/{vid[4:]}.jpg"></div>'
            else: fundo_ = media(f"assets/ia3/{vid}.mp4", a, b)
            return fundo_ + '<div class="pgrad"></div>' + fn(a, b)
        if os.path.exists(os.path.join(H, "assets", "ia3", vid + ".mp4")) or (vid.startswith("img:") and os.path.exists(os.path.join(BGDIR, vid[4:] + ".jpg"))):
            cena(f"c{L['n']:03d}", "R", L["ini"], L["fim"], True, 11.0)(_pr)
        else: print("  (preço sem vídeo ainda:", vid, ")")
    elif L["ini"] in GIFTS_INFO:
        n_, tit_, tp_, val_, iid_ = GIFTS_INFO[L["ini"]]
        if os.path.exists(os.path.join(BGDIR, iid_ + ".jpg")) or os.path.exists(os.path.join(H, "assets", "ia3", iid_ + ".mp4")):
            cena(f"c{L['n']:03d}", "B", L["ini"], L["fim"], True, 9.0)(gift_cena(n_, tit_, tp_, val_, iid_))
        else: print("  (presente sem imagem ainda:", iid_, ")")
    elif False and L["ini"] in GIFT_B:
        iid, ui, n_, val, w_, h_ = GIFT_B[L["ini"]]
        if not iid.endswith("_casal"): TAM_UI[iid] = (w_, h_)
        if os.path.exists(os.path.join(BGDIR, iid + ".jpg")):
            cena_celular(f"c{L['n']:03d}", "B", L["ini"], L["fim"], iid, ui, (lambda a, b, n_=n_, val=val: gift_tag(a, b, n_, val)))
        else: print("  (presente sem imagem ainda:", iid, ")")
    elif L["ini"] == "Your supply is already reserved in" and os.path.exists(os.path.join(BGDIR, "p_celular_compra.jpg")):
        cena_celular(f"c{L['n']:03d}", "B", L["ini"], L["fim"], "p_celular_compra", ui_compra)
    elif L["ini"] == "The process is simple, and I'll" and os.path.exists(os.path.join(BGDIR, "p_celular_sofa.jpg")):
        def _chips(a, b, L=L): return extras_broll(L)(a, b)
        cena_celular(f"c{L['n']:03d}", "B", L["ini"], L["fim"], "p_celular_sofa", ui_reembolso, _chips)
    elif tp in ("B", "R") and imgs_bg(L["asset"]):
        iid = imgs_bg(L["asset"])[0]
        if iid == "p_celular_pedido": cena_celular(f"c{L['n']:03d}", "B", L["ini"], L["fim"], iid, ui_pedido)
        else:
            def _st(a, b, L=L, iid=iid): return bg_html(iid, a, b, False, "fill2") + '<div class="gradt"></div>' + extras_broll(L)(a, b)
            cena(f"c{L['n']:03d}", tp, L["ini"], L["fim"], True)(_st)
    elif tp in ("T", "B", "R") and not novo(L["asset"]): print(f"  (sem vídeo ainda: #{L['n']} {L['asset'][:40]})"); continue
    elif tp == "T": cena_T(L)
    elif tp in ("B", "R"):
        src = f"assets/ia3/{novo(L['asset'])}.mp4"
        (B if tp == "B" else R)(f"c{L['n']:03d}", L["ini"], L["fim"], src, extra=extras_broll(L))
# vídeo do paciente (D2): tarja + chip do 120/80
PAC = {"s": -99, "d": 0}
CTA_INI = achar("Secure your supply, complete your three", 0)
# ================================================================ montagem
# verifica repetição de footage (regra do Jhon)
usos = {}
for cid, tipo, a, b, fn, luz in CENAS:
    pass
CENAS.sort(key=lambda c: c[2])
for i in range(len(CENAS) - 1):  # nenhum momento invade o próximo
    c = CENAS[i]
    if c[3] > CENAS[i + 1][2]: CENAS[i] = (c[0], c[1], c[2], CENAS[i + 1][2], c[4], c[5])
for i in range(len(CENAS) - 1):  # vão curto entre duas cenas faria o expert piscar (Jhon 29/10): estica a anterior
    c = CENAS[i]
    if 0 < CENAS[i + 1][2] - c[3] < 0.7: CENAS[i] = (c[0], c[1], c[2], CENAS[i + 1][2], c[4], c[5])
LUZES, COMTEXTO = [], []
for k, (cid, tipo, a, b, fn, luz) in enumerate(CENAS):
    _cursor[0] = max(0.0, a - 1.0)
    a, b = max(0.0, q(a - 0.04)), q(b - 0.04)
    h = fn(a, b)
    cls = {"F": "st f", "M": "st f" if 'class="fbgi"' in h else "st f meio", "T": "st t", "R": "st br", "B": "st br"}[tipo]
    clips.append(f'<div class="{cls}" id="{cid}"><div class="in" id="{cid}i">{h}</div></div>')
    js.append(f'tl.set("#{cid}", {{opacity:0}}, 0); tl.set("#{cid}", {{opacity:1}}, {a}); tl.set("#{cid}", {{opacity:0}}, {b});')
    # 362 (Jhon 30/10: transições mais suaves): saindo da Jennifer ou voltando para ela, dissolve curto + luz; entre duas telas, corte com luz
    if tipo in "BRT":
        cola_ant = k > 0 and a - q(CENAS[k - 1][3] - 0.04) < 0.08
        cola_prox = k + 1 < len(CENAS) and q(CENAS[k + 1][2] - 0.04) - b < 0.08
        if not cola_ant: js.append(f'tl.fromTo("#{cid}", {{opacity:0}}, {{opacity:1, duration:0.32, ease:"sine.inOut", immediateRender:false}}, {a});')
        if not cola_prox: js.append(f'tl.to("#{cid}", {{opacity:0, duration:0.3, ease:"sine.inOut"}}, {r(b - 0.3)});')
    if False:  # react com card (reprovado 28/10): o card cai da câmera 3D com motion blur; a imagem segue num push lento
        js.append(f'tl.fromTo("#{cid} .tdark", {{opacity:0}}, {{opacity:1, duration:0.3, ease:"power2.out", immediateRender:false}}, {a});')
        js.append(f'tl.fromTo("#{cid} .rcard", {{rotationX:38, y:-260, z:-400, opacity:0, filter:"blur(24px)"}}, {{rotationX:0, y:0, z:0, opacity:1, filter:"blur(0px)", duration:0.65, ease:"expo.out", immediateRender:false}}, {a});')
        js.append(f'tl.fromTo("#{cid} .rcard .fill", {{scale:1.0}}, {{scale:1.1, duration:{r(b - a)}, ease:"none", immediateRender:false}}, {a});')
    elif tipo in "BR":  # b-roll: entra com continuidade de zoom + blur curto; sai em corte limpo
        js.append(f'tl.fromTo("#{cid}i", {{scale:1.12, filter:"blur(10px)"}}, {{scale:1.0, filter:"blur(0px)", duration:0.35, ease:"power3.out", immediateRender:false}}, {a});')
        js.append(f'tl.fromTo("#{cid}i .fill", {{scale:1.0}}, {{scale:1.08, duration:{r(b - a)}, ease:"none", immediateRender:false}}, {a});')
    elif tipo in "FM":
        js.append(f'tl.fromTo("#{cid}i", {{opacity:0}}, {{opacity:1, duration:0.25, ease:"power2.out", immediateRender:false}}, {a});')
    else:  # T: o fundo escurece em fade, o lettering entra pelas próprias animações
        js.append(f'tl.fromTo("#{cid} .tbg .fill", {{scale:1.0}}, {{scale:1.12, duration:{r(b - a)}, ease:"none", immediateRender:false}}, {a});')
        js.append(f'tl.fromTo("#{cid} .tbg", {{scale:1.25, filter:"blur(18px)"}}, {{scale:1, filter:"blur(0px)", duration:0.55, ease:"expo.out", immediateRender:false}}, {a});')
    if tipo in "BR" and re.search(r'class="(disp|kbx|tag|ser|swp)', h): COMTEXTO.append((a, b))  # b-roll com texto próprio fica sem legenda
    if luz: LUZES.append(a)
    if tipo in "BR": S(a - 0.04, "k_swish", 0.035, 0.57)

COBRE = [(max(0.0, q(a - 0.04)), q(b - 0.04), "F" if t == "M" else t) for _, t, a, b, _, _ in CENAS]
def coberto(t, tipos): return any(a <= t < b and tp in tipos for a, b, tp in COBRE)

# T: fundo escuro + lettering ficam entre a doutora e o recorte dela
for k, (cid, tipo, a, b, fn, luz) in enumerate(CENAS):
    if tipo in "TFM":
        i = next(j for j, c in enumerate(clips) if f'id="{cid}"' in c)
        clips[i] = clips[i].replace('<div class="in"', f'<div class="{"tdark" if tipo == "T" else "fdark"}"></div><div class="in"', 1)
ALPHA = ""
ALPHA_PEDIDOS = []
for cid, a, b, txt in ATRAS:
    a, b = q(a - 0.15), q(b)
    for x0, x1, _ in COBRE:
        if x0 <= a < x1: a = q(x1)
    for x0, x1, _ in COBRE:
        if a < x0 < b: b = q(x0)
    if b - a < 1.5: print("  atrás pulado (sem espaço):", cid); continue
    sg = next(x for x in SEG if x["s"] <= a + 0.05 < x["s"] + x["d"]); a = max(a, q(sg["s"])); b = min(b, q(sg["s"] + sg["d"]))
    ALPHA_PEDIDOS.append({"id": cid, "bloco": sg["id"], "ini": r(a - sg["s"]), "dur": r(b - a)})
    src = f"assets/doutora_alpha/{cid}.webm"
    if os.path.exists(os.path.join(H, src)):
        TRK[0] += 1
        ALPHA += (f'<video id="al{cid}" class="clip" src="{src}" muted playsinline data-start="{a}" data-duration="{r(b - a)}" data-track-index="{TRK[0]}"></video>')
    TRK[0] += 1; t1 = nid("at")
    l1_, _, l2_ = txt.partition("<br>")
    clips.append(f'<div id="{cid}" class="clip atrz" data-start="{a}" data-duration="{r(b - a)}" data-track-index="{TRK[0]}"><div class="atr" id="{t1}"><div class="l1">{colore(l1_)}</div><div class="l2">{colore(l2_)}</div></div></div>')
    js.append(f'tl.fromTo("#{t1}", {{z:-500, scale:1.35, opacity:0, filter:"blur(24px)"}}, {{z:0, scale:1, opacity:1, filter:"blur(0px)", duration:0.7, ease:"expo.out", immediateRender:false}}, {r(a + 0.02)});')
    js.append(f'tl.to("#{t1}", {{scale:1.06, duration:{r(max(0.5, b - a - 0.9))}, ease:"none"}}, {r(a + 0.72)});')
    js.append(f'tl.to("#{t1}", {{opacity:0, filter:"blur(16px)", duration:0.25, ease:"power2.in"}}, {r(b - 0.27)});')
    S(a + 0.02, "whoosh2", 0.05)
json.dump(ALPHA_PEDIDOS, open(os.path.join(J, "edicao", "alpha_pedidos.json"), "w"), indent=1)

# doutora + recorte (mesmo punch-in nos dois)
clips.insert(0, '<div id="cam"><div id="cam-in">' + "".join(
    f'<video id="v{s["id"]}" class="clip" src="assets/avatar/{s["id"]}.mp4" playsinline data-start="{q(s["s"])}" data-duration="{r(s["d"])}" data-track-index="0" data-has-audio="true" data-volume="1"></video>'
    for s in SEG) + '</div></div>')
clips.append(f'<div id="al"><div id="al-in">{ALPHA}</div></div>')
frases = [W[0]["s"]] + [W[i]["s"] for i in range(1, len(W)) if re.search(r"[.?!…]\"?$", W[i - 1]["w"])]
esc, ult = 1.0, -9
pontos = sorted(set([q(x) for x in frases] + [b for a, b, _ in COBRE] + [a for a, b, t in COBRE if t == "T"]))
for t in pontos:
    if coberto(t + 0.05, "BRF") or t - ult < 2.2 or any(x0 - 0.3 <= t <= x1 for _, x0, x1, _ in ATRAS): continue
    esc = 1.12 if esc == 1.0 else 1.0
    js.append(f'tl.set("#cam-in, #al-in", {{scale:{esc}}}, {q(t - 0.02)});'); ult = t
for _, x0, x1, _ in ATRAS: js.append(f'tl.set("#cam-in, #al-in", {{scale:1}}, {q(x0 - 0.17)});')
# deriva lenta contínua (a câmera nunca fica parada)
js.append(f'tl.fromTo("#cam", {{x:0}}, {{x:0, duration:{FIM}, ease:"none"}}, 0);')

# F: doutora desfoca e escurece atrás do card (intervalos colados viram um só)
fs = sorted((a, b) for a, b, t in COBRE if t == "F")
merg = []
for a, b in fs:
    if merg and a - merg[-1][1] < 0.2: merg[-1][1] = max(merg[-1][1], b)
    else: merg.append([a, b])
for a, b in merg:
    js.append(f'tl.fromTo("#cam", {{filter:"blur(0px) brightness(1) saturate(1)"}}, {{filter:"blur(22px) brightness(0.6) saturate(1.2)", duration:0.3, ease:"power2.out", immediateRender:false}}, {a});')
    js.append(f'tl.fromTo("#cam", {{filter:"blur(22px) brightness(0.6) saturate(1.2)"}}, {{filter:"blur(0px) brightness(1) saturate(1)", duration:0.3, ease:"power2.out", immediateRender:false}}, {r(b - 0.3)});')

# palco: no T a doutora desce e recua para o lettering respirar acima da cabeça; no R desce mais para o card caber acima
PALCO = {}
seg = []
for a, b, t in sorted(COBRE):
    if t not in PALCO: continue
    if seg and a - seg[-1][1] < 0.6 and seg[-1][2] == t: seg[-1][1] = max(seg[-1][1], b)
    else: seg.append([a, b, t])
for i, (a, b, t) in enumerate(seg):
    y, sc = PALCO[t]
    ant = seg[i - 1] if i and a - seg[i - 1][1] < 0.6 else None
    y0, s0 = PALCO[ant[2]] if ant else (0, 1)
    js.append(f'tl.fromTo("#cam, #al", {{y:{y0}, scale:{s0}}}, {{y:{y}, scale:{sc}, duration:0.45, ease:"power3.inOut", immediateRender:false}}, {r(max(0, a - 0.1))});')
    if not (i + 1 < len(seg) and seg[i + 1][0] - b < 0.6):
        js.append(f'tl.fromTo("#cam, #al", {{y:{y}, scale:{sc}}}, {{y:0, scale:1, duration:0.4, ease:"power3.inOut", immediateRender:false}}, {r(b - 0.2)});')

# produto entra quando o nome é falado (fora de telas cheias); "Cardio Flush" vem em duas palavras
ult_p = -9
for k_, x in enumerate(W):
    n = norm(x["w"]).replace("'s", "")
    if n != "erevanton": continue
    t = q(x["s"] - 0.15)
    if coberto(t + 1.0, "TFBR") or coberto(t + 0.1, "TFBR") or t - ult_p < 6 or PAC["s"] - 0.5 < t < PAC["s"] + PAC["d"]: continue
    ult_p = t; k = len(clips)
    img, nome, w_ = ("ev_1.png", "EreVanton", BW)
    clips.append(f'<div id="pr{k}" class="clip prod" data-start="{t}" data-duration="2.4" data-track-index="9"><i class="pglow"></i><img src="assets/img/{img}" style="width:{w_}px;height:{BOTTLE_H}px"><b>{nome}</b></div>')
    js.append(f'tl.fromTo("#pr{k}", {{x:420, rotationY:-55, opacity:0, filter:"blur(22px)"}}, {{x:0, rotationY:-12, opacity:1, filter:"blur(0px)", duration:0.55, ease:"expo.out", immediateRender:false}}, {t});')
    js.append(f'tl.to("#pr{k}", {{rotationY:6, y:-14, duration:1.5, ease:"sine.inOut"}}, {r(t + 0.55)});')
    js.append(f'tl.to("#pr{k}", {{x:420, opacity:0, filter:"blur(22px)", duration:0.35, ease:"power3.in"}}, {r(t + 2.05)});')
    S(t, "k_swish", 0.05, 0.57)
# 362 (regra do Jhon 30/10): toda menção falada a N frascos mostra N frascos EreVanton, na palavra
KIT = {"9": "ev_9.png", "3": "ev_3.png", "1": "ev_1.png"}
FRSOLO = []
COM_KIT = []  # cenas que já mostram o kit certo (preenchidas pelas telas especiais/F com 9-Erevanton)
for cid, tipo, a, b, fn, luz in CENAS:
    h = next((c for c in clips if f'id="{cid}"' in c), "")
    for n_ in KIT:
        if f'class="kit k{n_}"' in h: COM_KIT.append((a, b, n_))
    if re.search(r"pr_cozinha|pk9_|pk_kit_luz|bg_caixa9|p_caixa_unica|kit9_premium|bg/kit_[a-e]", h): COM_KIT.append((a, b, "9"))
for k_, x in enumerate(W):
    w0 = norm(x["w"]); w1 = norm(W[k_ + 1]["w"]) if k_ + 1 < len(W) else ""
    m_ = re.match(r"^(\d+)(?:bottles?)?$", w0) if ("bottle" in w0 or w1.startswith("bottle") or (w1 == "full" and k_ + 2 < len(W) and norm(W[k_ + 2]["w"]).startswith("bottle"))) else None
    if not m_ or m_.group(1) not in KIT: continue
    t = q(x["s"] - 0.15); n_ = m_.group(1)
    if any(a - 0.2 <= t <= b and nn == n_ for a, b, nn in COM_KIT): continue
    k = len(clips)
    kimg = '<div class="kitimg"><img src="assets/bg/kit_h.jpg"></div>' if n_ == "9" and os.path.exists(os.path.join(BGDIR, "kit_h.jpg")) else kit_html(int(n_))
    FR_IMG = {"9": "pk9_slate"}  # Jhon 30/10: na fala dos frascos a tela mostra SÓ os frascos (sem caixa, sem a cena por trás)
    if n_ in FR_IMG and os.path.exists(os.path.join(BGDIR, FR_IMG[n_] + ".jpg")):
        jb = nid("fb")
        js.append(f'tl.fromTo("#{jb} img", {{scale:1.2}}, {{scale:1.15, duration:2.8, ease:"none", immediateRender:false}}, {t});')
        clips.append(f'<div id="ktw{k}" class="clip cta frsolo" data-start="{t}" data-duration="2.8" data-track-index="{320 + k % 5}"><div class="fill2" id="{jb}"><img src="assets/bg/{FR_IMG[n_]}.jpg"></div>'
                     f'<div class="fgradi"></div>{LOGO("topo")}<div id="kt{k}" class="frnum"><b>{n_}</b><span>BOTTLES</span></div></div>')
        FRSOLO.append((t, t + 2.8)); S(t, "k_swish", 0.05, 0.57)
    else:
        clips.append(f'<div id="ktw{k}" class="clip cta" data-start="{t}" data-duration="2.8" data-track-index="{320 + k % 5}"><div id="kt{k}" class="kitov"><i class="pglow"></i>{kimg}<b>{n_} BOTTLE{"S" if n_ != "1" else ""}</b></div></div>')
    js.append(f'tl.set("#ktw{k}", {{opacity:0}}, 0);')
    js.append(f'tl.fromTo("#ktw{k}", {{opacity:0}}, {{opacity:1, duration:0.3, ease:"sine.inOut", immediateRender:false}}, {t});')
    js.append(f'tl.fromTo("#kt{k}", {{y:260, rotationX:35, opacity:0, filter:"blur(22px)"}}, {{y:0, rotationX:0, opacity:1, filter:"blur(0px)", duration:0.6, ease:"expo.out", immediateRender:false}}, {t});')
    js.append(f'tl.to("#kt{k} img", {{scale:1.05, duration:1.6, ease:"sine.inOut"}}, {r(t + 0.6)});')
    js.append(f'tl.to("#ktw{k}", {{opacity:0, duration:0.3, ease:"sine.inOut"}}, {r(t + 2.5)});')
    S(t, "k_pop", 0.08, 0.74); print(f"frascos falados: {n_} em {t:.1f}s → card de kit")

# luz nas entradas de b-roll/react
for k, t in enumerate(LUZES):
    clips.append(f'<div class="luz" id="lz{k}"><video id="vlz{k}" class="clip" src="assets/luz/lk{k % 6}.mp4" muted playsinline data-start="{q(max(0, t - 0.1))}" data-duration="0.24" data-track-index="{200 + k % 4}"></video></div>')
    js.append(f'tl.set("#lz{k}", {{opacity:0}}, 0); tl.set("#lz{k}", {{opacity:1}}, {q(max(0, t - 0.2))}); tl.set("#lz{k}", {{opacity:0}}, {q(t + 0.14)});')

YEL, RED, BLU, GRN = "#FFD23F", "#FF4B3E", "#2F7BFF", "#2BD67B"
# legenda pop (doutora sozinha, b-roll e react; nunca sob lettering T/F)
# V3: palavra falada positiva fica verde, negativa vermelha, o resto amarelo
POS1 = {"faster", "accelerated", "regenerate", "permanent", "permanently", "firm", "firmer", "firmness", "reliable", "free", "refund", "guarantee",
        "safe", "natural", "gifts", "confidence", "self-confidence", "solved", "dissolve", "congratulate"}
NEG1 = {"toxins", "xenotoxins", "blocks", "weaken", "disappear", "failure", "skeptical", "problem", "risk", "unbearable", "halfway"}
POS2 = {("blood", "flow"), ("one-time", "payment"), ("money", "back")}
NEG2 = {("run", "out"), ("ran", "out"), ("side", "effects"), ("given", "up")}
def _n2(w): return re.sub(r"[^a-z0-9\-]", "", w.lower().replace("’", "'").split("'")[0])
COR_W = {}
for k_ in range(len(W)):
    a_ = _n2(W[k_]["w"]); b_ = _n2(W[k_ + 1]["w"]) if k_ + 1 < len(W) else ""
    if (a_, b_) in POS2: COR_W[k_] = COR_W[k_ + 1] = GRN
    elif (a_, b_) in NEG2: COR_W[k_] = COR_W[k_ + 1] = RED
    elif k_ not in COR_W and a_ in POS1: COR_W[k_] = GRN
    elif k_ not in COR_W and a_ in NEG1: COR_W[k_] = RED
IDX_W = {id(x): k_ for k_, x in enumerate(W)}
ASP = '"“”'
HEADS = []
for cid_, tipo_, a_, b_, fn_, luz_ in CENAS:
    h_ = next((c for c in clips if f'id="{cid_}"' in c), "")
    h2_ = re.sub(r'<!--ui-->(?:(?!<div class="uiv"|<div class="uie").)*?<!--/ui-->', "", h_, flags=re.S)  # tela de celular (UI pequena) não conta como headline; capa do presente conta
    txt_ = re.sub(r"<[^>]+>", " ", h2_)
    HEADS.append((q(a_ - 0.04), q(b_ - 0.04), {norm(w) for w in txt_.split() if len(norm(w)) > 1} - {"to", "you", "your", "the", "and", "of", "a", "in", "on", "for", "is", "it", "i", "my", "this", "with", "per"}))
for cid_, a_, b_, t_ in ATRAS: HEADS.append((a_, b_, {norm(w) for w in re.sub(r"<[^>]+>", " ", t_).split() if len(norm(w)) > 1}))
def na_headline(x):
    n_ = norm(x["w"])
    return len(n_) > 1 and any(a_ <= x["s"] < b_ and n_ in ws for a_, b_, ws in HEADS)
PILHA = [(q(a_ - 0.04), q(b_ - 0.04)) for cid_, tipo_, a_, b_, fn_, luz_ in CENAS if re.search(r'class="kbx col">(<div class="chip[^>]*>[^<]*</div>){2,}', next((c for c in clips if f'id="{cid_}"' in c), ""))]
BAIXO = [(q(a_ - 0.04), q(b_ - 0.04)) for cid_, tipo_, a_, b_, fn_, luz_ in CENAS if re.search(r'class="gcovs"|class="gcard"|class="tri"|caixa_premium_envio', next((c for c in clips if f'id="{cid_}"' in c), ""))]
FAIXA = [(q(a_ - 0.04), q(b_ - 0.04)) for cid_, tipo_, a_, b_, fn_, luz_ in CENAS if fn_.__name__ == "_pr"]
# Jhon 30/10: a legenda acompanha a fala o tempo todo; pula só a FRASE que repete a headline (com os artigos/preposições órfãos)
STOPW = set("the a an and or of to in on at is it its it's you your for with this that by as be are was per than from into".split())
ESC = [na_headline(x) for x in W]
# conta da oferta fora da tela (decisão do Jhon): a legenda não mostra o $/cápsula nem "9 frascos = 60 dias"
for fr_ in ["equivalent to 63 cents per capsule, less than $1 per capsule", "And those are exactly the 60 days you need to complete your three months without a single interruption.",
            "You're still missing 60 days, and those are exactly the 60 days I've reserved here for you.", "That's $135 for the remaining 60 days you need to complete your full treatment."]:
    _cursor[0] = 0.0; t_ = achar(fr_); k0 = next(k for k in range(len(W)) if abs(W[k]["s"] - t_) < 1e-6)
    for m_ in range(k0, k0 + len(fr_.split())): ESC[m_] = True
for _ in range(3):  # órfãos colados na headline
    for k_ in range(len(W)):
        if ESC[k_]: continue
        viz = (k_ > 0 and ESC[k_ - 1]) or (k_ + 1 < len(W) and ESC[k_ + 1])
        if viz and norm(W[k_]["w"]) in STOPW: ESC[k_] = True
k_ = 0
while k_ < len(W):  # trecho visível de 1–2 palavras encostado numa headline não aparece
    if ESC[k_]: k_ += 1; continue
    j_ = k_
    while j_ < len(W) and not ESC[j_]: j_ += 1
    enc = (k_ > 0 and ESC[k_ - 1]) or (j_ < len(W) and ESC[j_])
    if enc and j_ - k_ <= 2:
        for m_ in range(k_, j_): ESC[m_] = True
    else:
        fimf = lambda m_: re.search(r"[.?!…]\"?$", W[m_]["w"])
        if k_ > 0 and ESC[k_ - 1]:  # cauda de frase depois da headline ("normal.") não fica solta
            e_ = next((m_ for m_ in range(k_, j_) if fimf(m_)), None)
            if e_ is not None and e_ - k_ + 1 <= 2:
                for m_ in range(k_, e_ + 1): ESC[m_] = True
        if j_ < len(W) and ESC[j_]:  # começo de frase antes da headline com 1–2 palavras
            s_ = max([m_ + 1 for m_ in range(k_, j_) if fimf(m_)] or [k_])
            if 0 < j_ - s_ <= 2 and s_ > k_:
                for m_ in range(s_, j_): ESC[m_] = True
    k_ = j_
grupos, g = [], []
for k_, x in enumerate(W):
    if ESC[k_]:
        if g: grupos.append(g); g = []
        continue
    g.append(x)
    prox_esc = k_ + 1 < len(W) and ESC[k_ + 1]
    if prox_esc and len(g) == 1 and grupos and not re.search(r"[.?!…]\"?$", grupos[-1][-1]["w"]) and grupos[-1][-1] is W[k_ - 1]:
        grupos[-1].append(x); g = []; continue  # palavra solta antes da headline junta ao grupo anterior
    if len(g) == 3 or re.search(r"[.,?!…:;—]\"?$", x["w"]): grupos.append(g); g = []
if g: grupos.append(g)
for i, g in enumerate(grupos):
    a = q(g[0]["s"]); b = q(grupos[i + 1][0]["s"]) if i + 1 < len(grupos) else q(g[-1]["ea"] + 0.3)
    b = min(b, q(g[-1]["ea"] + 0.5))  # "ea" = fim da última letra (o "e" do ElevenLabs inclui a pausa da pontuação)
    spans = "".join(f'<span id="cw{i}_{k}">{html.escape(x["w"].strip(ASP))}</span> ' for k, x in enumerate(g))
    baixa = " capbaixa faixa" if any(x0 - 0.1 <= a < x1 for x0, x1 in BAIXO + FRSOLO) else " faixa" if any(x0 - 0.1 <= a < x1 for x0, x1 in FAIXA) else (" capcta" if a >= CTA_INI - 0.1 or any(x0 - 0.1 <= a < x1 for x0, x1 in CTA_D) else " capalta" if any(x0 - 0.1 <= a < x1 for x0, x1 in PILHA) else "")
    clips.append(f'<div id="cap{i}" class="clip cap{baixa}" data-start="{a}" data-duration="{r(max(0.12, b - a))}" data-track-index="8"><div class="cap-in">{spans}</div></div>')
    js.append(f'tl.fromTo("#cap{i} .cap-in", {{scale:.8, y:20, opacity:0}}, {{scale:1, y:0, opacity:1, duration:0.16, ease:"back.out(2.4)", immediateRender:false}}, {a});')
    for k, x in enumerate(g):
        js.append(f'tl.set("#cw{i}_{k}", {{color:"{COR_W.get(IDX_W[id(x)], YEL)}", scale:1.08}}, {q(x["s"])}); tl.set("#cw{i}_{k}", {{color:"#ffffff", scale:1}}, {q(max(x["ea"] + 0.05, x["s"] + 0.08))});')

for k_, (a_, b_) in enumerate(CTA_D):  # CTA no meio do vídeo sobre a Jennifer nítida
    clips.append(f'<div id="ctad{k_}" class="clip cta" data-start="{a_}" data-duration="{r(b_ - a_)}" data-track-index="9"><div class="cta-g fixo">{LOGO("ctalg")}<div class="bt">{CTA_TXT}</div>{SETA}</div></div>')
    js.append(f'tl.fromTo("#ctad{k_} .cta-g", {{y:220, opacity:0, filter:"blur(16px)"}}, {{y:0, opacity:1, filter:"blur(0px)", duration:0.45, ease:"back.out(1.6)", immediateRender:false}}, {a_});')
    S(a_, "k_pop", 0.09, 0.74)
# CTA fixa do fim (mesmo desenho do validado)
clips.append(f'<div id="cta" class="clip cta" data-start="{q(CTA_INI)}" data-duration="{r(FIM - CTA_INI)}" data-track-index="9"><div class="cta-g fixo">{LOGO("ctalg")}<div class="bt">{CTA_TXT}</div>{SETA}</div></div>')
js.append(f'tl.fromTo("#cta .cta-g", {{y:220, opacity:0, filter:"blur(16px)"}}, {{y:0, opacity:1, filter:"blur(0px)", duration:0.5, ease:"back.out(1.6)", immediateRender:false}}, {q(CTA_INI)});')
js.append(f'tl.to("#cta .bt", {{scale:1.05, duration:0.45, ease:"sine.inOut", yoyo:true, repeat:{int((FIM - CTA_INI) / 0.45) - 1}}}, {q(CTA_INI + 0.5)});')
js.append(f'tl.to("#cta .seta", {{y:16, duration:0.4, ease:"sine.inOut", yoyo:true, repeat:{int((FIM - CTA_INI) / 0.4) - 1}}}, {q(CTA_INI + 0.5)});')

for sel, t, de, para, d, e in anim:
    if re.search(r"opacity:\s*0[,}\s]", de): js.append(f'tl.set("{sel}", {{opacity:0}}, 0);')  # só entradas começam invisíveis (saída não!)
    js.append(f'tl.fromTo("{sel}", {de}, {{...{para}, duration:{d}, ease:"{e}", immediateRender:false}}, {r(t)});')

auto = {"version": 1, "lanes": [{"target": "volume", "points": [{"t": 0, "v": 0.0}, {"t": 0.6, "v": 0.34}, {"t": r(FIM - 4), "v": 0.34}, {"t": r(FIM - 2.5), "v": 0.8}, {"t": FIM, "v": 0.0}]}]}
clips.append(f"<audio id=\"trilha\" src=\"assets/music/bed.m4a\" data-start=\"0\" data-duration=\"{FIM}\" data-track-index=\"10\" data-volume=\"1\" data-automation='{json.dumps(auto)}'></audio>")
SD = {}
for k, (t, f, v, d) in enumerate(sorted(sfx)):
    if t < 0: continue
    if f not in SD: SD[f] = dur(os.path.join(H, "assets", "sfx", f + ".mp3"))
    clips.append(f'<audio id="sfx{k}" src="assets/sfx/{f}.mp3" data-start="{t}" data-duration="{r(min(d or SD[f], SD[f]))}" data-track-index="{11 + k % 12}" data-volume="{v}"></audio>')

CSS = f"""
@font-face {{ font-family:"Montserrat"; src:url("assets/fonts/Montserrat-VF.ttf"); font-weight:100 900; }}
@font-face {{ font-family:"InterV"; src:url("assets/fonts/Inter.ttf"); font-weight:100 900; }}
@font-face {{ font-family:"Archivo"; src:url("assets/fonts/ArchivoNarrow.ttf"); font-weight:400 700; }}
@font-face {{ font-family:"NewsI"; src:url("assets/fonts/NewsreaderItalic.woff2"); font-style:italic; font-weight:200 800; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
#root {{ position:relative; width:100%; height:100%; overflow:hidden; background:#000; font-family:"InterV"; }}
#cam {{ position:absolute; inset:0; overflow:hidden; z-index:1; }}
#cam-in, #al-in {{ position:absolute; inset:0; transform-origin:50% 30%; }}
#cam video, #al video {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
#al {{ position:absolute; inset:0; z-index:4; pointer-events:none; }}
.st {{ position:absolute; inset:0; overflow:hidden; opacity:0; color:#fff; perspective:1600px; }}
.st.f {{ z-index:5; }} .st.t {{ z-index:3; }}
.st.f.meio .in {{ transform:translateY(520px); }}
.tbg {{ position:absolute; inset:0; overflow:hidden; }} .tbg video {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
.tgrad {{ position:absolute; inset:0; background:linear-gradient(to bottom, rgba(3,6,15,.88) 0%, rgba(3,6,15,.45) 28%, rgba(3,6,15,0) 48%); }}
.fbgv {{ position:absolute; inset:0; overflow:hidden; }} .fbgv video {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
.fgrad {{ position:absolute; inset:0; background:radial-gradient(70% 45% at 50% 40%, rgba(3,6,15,.55), rgba(3,6,15,.2) 70%), linear-gradient(to bottom, rgba(3,6,15,.5), rgba(3,6,15,0) 30%, rgba(3,6,15,0) 70%, rgba(3,6,15,.6)); }}
.fan {{ position:absolute; top:760px; height:auto; z-index:2; filter:drop-shadow(0 30px 50px rgba(0,0,0,.6)); }}
.fan.f0 {{ left:60px; width:300px; transform:rotate(-10deg); }} .fan.f1 {{ left:375px; width:330px; top:720px; z-index:3; }} .fan.f2 {{ right:60px; width:300px; transform:rotate(10deg); }}
.cal {{ position:absolute; left:90px; right:90px; height:420px; border-radius:40px; z-index:3; display:flex; flex-direction:column; align-items:center; justify-content:center;
  background:linear-gradient(160deg, rgba(255,255,255,.14), rgba(255,255,255,.04)); border:2px solid rgba(255,255,255,.25); box-shadow:0 30px 80px rgba(0,0,0,.5), inset 0 1px 0 rgba(255,255,255,.3); }}
.cal.g {{ top:420px; border-color:rgba(255,210,63,.7); box-shadow:0 30px 80px rgba(0,0,0,.5), 0 0 80px rgba(255,210,63,.25); }} .cal.r {{ top:900px; opacity:.85; }}
.cal i {{ font-style:normal; font-family:"Archivo"; font-weight:700; font-size:46px; letter-spacing:.2em; color:#fff; }} .cal.g i {{ color:{YEL}; }}
.cal b {{ font-family:"InterV"; font-weight:900; font-size:190px; line-height:.95; color:#fff; font-variant-numeric:tabular-nums; text-shadow:0 6px 0 #6f8ccb, 0 20px 40px rgba(0,0,0,.5); }}
.cal.g b {{ color:{YEL}; text-shadow:0 6px 0 #966d05, 0 20px 40px rgba(0,0,0,.5), 0 0 80px rgba(255,210,63,.5); }} .cal.r b {{ color:#aab7d6; }}
.cal u {{ text-decoration:none; font-family:"Archivo"; font-weight:700; font-size:38px; letter-spacing:.3em; color:rgba(255,255,255,.7); }}
.cal em {{ position:absolute; right:-20px; top:-30px; font-style:normal; font-family:"InterV"; font-weight:900; font-size:44px; padding:12px 26px; border-radius:40px; background:{YEL}; color:#081024; box-shadow:0 10px 30px rgba(0,0,0,.5); }}
.cal.r em {{ background:#5a6a8a; color:#fff; }}
.meia {{ position:absolute; left:0; right:0; height:960px; overflow:hidden; z-index:2; }} .meia.top {{ top:0; border-bottom:4px solid rgba(255,255,255,.15); }} .meia.bot {{ top:960px; }}
.meia video {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
.meia .rot {{ position:absolute; left:0; right:0; bottom:70px; text-align:center; font-family:"Archivo"; font-weight:700; font-size:54px; letter-spacing:.06em; color:#fff; text-shadow:0 4px 20px rgba(0,0,0,.8); }}
.meia .rot b {{ display:block; font-family:"InterV"; font-weight:900; font-size:110px; letter-spacing:-.02em; }}
.xs {{ position:absolute; left:50%; top:50%; width:460px; height:460px; margin:-300px 0 0 -230px; }}
.xs path {{ fill:none; stroke:{RED}; stroke-width:26; stroke-linecap:round; stroke-dasharray:420; stroke-dashoffset:420; filter:drop-shadow(0 0 20px rgba(255,75,62,.8)); }} .st.br {{ z-index:6; background:#000; }}
.in {{ position:absolute; inset:0; transform-style:preserve-3d; }}
.tdark {{ position:absolute; inset:0; background:radial-gradient(90% 60% at 50% 40%, #12234a 0%, #08112a 45%, #03060f 85%); }}
.st.t .in::before {{ content:""; position:absolute; left:50%; top:22%; width:1100px; height:900px; margin-left:-550px; border-radius:50%;
  background:radial-gradient(circle, rgba(47,123,255,.35), rgba(0,0,0,0) 65%); }}
.fdark {{ position:absolute; inset:0; background:radial-gradient(75% 50% at 50% 42%, rgba(18,40,96,.66) 0%, rgba(8,17,42,.8) 55%, rgba(3,6,15,.94) 100%); }}
.st.f .in::before {{ content:""; position:absolute; left:50%; top:30%; width:1200px; height:1000px; margin-left:-600px; border-radius:50%;
  background:radial-gradient(circle, rgba(47,123,255,.28), rgba(0,0,0,0) 62%); }}
.prod {{ position:absolute; right:30px; top:520px; width:330px; z-index:6; perspective:1200px; text-align:center; }}
.prod img {{ position:relative; height:auto; display:block; margin:0 auto; filter:drop-shadow(0 30px 40px rgba(0,0,0,.6)); }}
.prod .pglow {{ position:absolute; left:50%; top:45%; width:520px; height:520px; margin:-260px 0 0 -260px; border-radius:50%; background:radial-gradient(circle, rgba(255,210,63,.45), rgba(0,0,0,0) 65%); }}
.prod b {{ position:relative; display:inline-block; margin-top:-10px; font-family:"Montserrat"; font-weight:900; font-size:40px; color:#081024; background:{YEL}; padding:10px 24px; border-radius:40px; box-shadow:0 10px 30px rgba(0,0,0,.5); }}
.relogio {{ position:absolute; left:50%; margin-left:-230px; top:150px; width:460px; z-index:8; display:flex; align-items:center; justify-content:center; gap:22px;
  padding:22px 30px; border-radius:80px; background:linear-gradient(180deg, rgba(20,30,60,.88), rgba(6,10,24,.92)); border:2px solid rgba(255,210,63,.6);
  box-shadow:0 20px 60px rgba(0,0,0,.6), 0 0 60px rgba(255,210,63,.3); }}
.relogio svg {{ width:84px; height:84px; }}
.relogio b {{ font-family:"Montserrat"; font-weight:900; font-size:96px; color:#fff; letter-spacing:.02em; font-variant-numeric:tabular-nums; }}
.fill {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
.gradb {{ position:absolute; inset:0; background:linear-gradient(to top, rgba(0,0,0,.8) 0%, rgba(0,0,0,.3) 30%, rgba(0,0,0,0) 55%); }}
.gradt {{ position:absolute; inset:0; background:linear-gradient(to bottom, rgba(0,0,0,.75) 0%, rgba(0,0,0,0) 35%); }}
.rcard {{ position:absolute; left:60px; right:60px; top:100px; height:800px; border-radius:40px; overflow:hidden; z-index:2;
  border:3px solid rgba(255,255,255,.85); box-shadow:0 40px 90px rgba(0,0,0,.7), 0 0 120px rgba(47,123,255,.35); background:#000; }}
.cap.low {{ top:1640px; }}
.pip {{ position:absolute; left:-40px; bottom:-30px; width:520px; height:924px; z-index:4; filter:drop-shadow(0 0 30px rgba(0,0,0,.6)); }}
.pip video {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
.kbx {{ position:absolute; left:70px; right:70px; bottom:190px; z-index:3; text-align:center; }}
.ln {{ color:#fff; line-height:1.05; text-shadow:0 6px 30px rgba(0,0,0,.6); }}
.w {{ display:inline-block; margin-right:.22em; }} .w.hl {{ color:{YEL}; }}
.red {{ color:{RED}; }} .yel {{ color:{YEL}; }}
.disp {{ font-family:"InterV"; font-weight:900; letter-spacing:-.03em; line-height:.96; }}
.cond {{ font-family:"Archivo"; font-weight:700; letter-spacing:.03em; line-height:1; }}
.ser {{ font-family:"NewsI"; font-style:italic; font-weight:500; color:{YEL}; line-height:1.05; text-shadow:0 0 40px rgba(255,210,63,.45); }}
.c {{ position:absolute; left:50px; right:50px; text-align:center; z-index:3; }}
.huge {{ font-size:170px; }} .big {{ font-size:132px; }} .mid {{ font-size:78px; }}
.ser.big {{ font-size:110px; }} .ser.mid {{ font-size:80px; }}
.tback {{ text-shadow:0 0 80px rgba(47,123,255,.35), 0 10px 40px rgba(0,0,0,.6); }}
.kick {{ font-family:"Archivo"; font-weight:700; font-size:44px; letter-spacing:.3em; color:{YEL}; text-shadow:0 0 30px rgba(255,210,63,.45); }}
.kick.c {{ position:absolute; left:40px; right:40px; text-align:center; z-index:3; }}
.num {{ font-family:"InterV"; font-weight:900; font-size:380px; line-height:.85; letter-spacing:-.06em; color:#fff;
  text-shadow:0 4px 0 #c9d8f7, 0 8px 0 #9db4e6, 0 12px 0 #6f8ccb, 0 16px 0 #4a66a6, 0 30px 50px rgba(0,0,0,.6), 0 0 110px rgba(47,123,255,.55); }}
.num em {{ font-family:"NewsI"; font-style:italic; font-weight:500; font-size:160px; color:{YEL}; letter-spacing:0; }}
.num.yel {{ color:{YEL}; text-shadow:0 4px 0 #e7b31c, 0 8px 0 #c18f0b, 0 12px 0 #966d05, 0 16px 0 #6e4f02, 0 30px 50px rgba(0,0,0,.6), 0 0 110px rgba(255,210,63,.5); }}
.num.red {{ color:{RED}; text-shadow:0 4px 0 #db3a2e, 0 8px 0 #b32c22, 0 12px 0 #8a2018, 0 16px 0 #63150f, 0 30px 50px rgba(0,0,0,.6), 0 0 110px rgba(255,75,62,.5); }}
.glowr {{ text-shadow:0 0 60px rgba(255,75,62,.6); }} .glowy {{ text-shadow:0 0 70px rgba(255,210,63,.55); }}
.strike {{ color:rgba(255,255,255,.9); text-decoration:line-through; text-decoration-color:{RED}; text-decoration-thickness:12px; }}
.chip {{ display:inline-block; font-family:"InterV"; font-weight:800; font-size:44px; padding:16px 30px; border-radius:60px; color:#fff;
  background:rgba(255,255,255,.12); border:2px solid rgba(255,255,255,.3); }}
.chip.red {{ background:{RED}; border-color:{RED}; box-shadow:0 0 50px rgba(255,75,62,.55); }}
.chip.big {{ font-size:54px; padding:22px 40px; }}
.chip.c2 {{ position:absolute; left:50%; transform:translateX(-50%); white-space:nowrap; z-index:3; }}
.chip.c3, .chip.c3s {{ background:rgba(47,123,255,.3); border-color:{BLU}; }}
.vidro {{ position:absolute; left:70px; right:70px; z-index:3; padding:50px 50px 30px; border-radius:40px; background:rgba(255,255,255,.08);
  border:2px solid rgba(255,255,255,.22); box-shadow:0 30px 80px rgba(0,0,0,.45), inset 0 1px 0 rgba(255,255,255,.25); backdrop-filter:blur(6px); }}
.vidro .kick {{ text-align:center; margin-bottom:40px; font-size:38px; }}
.vidro .chip {{ margin:10px auto 20px; display:block; width:max-content; }}
.tlr {{ display:flex; align-items:center; gap:24px; margin-bottom:46px; font-family:"Archivo"; font-weight:700; font-size:52px; }}
.tlr b {{ width:230px; }} .tlr span {{ width:190px; text-align:right; }}
.bar {{ position:relative; flex:1; height:30px; border-radius:15px; background:rgba(255,255,255,.14); overflow:hidden; display:block; }}
.bar u {{ position:absolute; left:0; top:0; bottom:0; border-radius:15px; background:linear-gradient(90deg, {BLU}, {YEL}); transform-origin:0 50%; }}
.bar.big {{ position:absolute; left:140px; right:140px; height:40px; z-index:3; }}
.bar.big u {{ background:linear-gradient(90deg, {RED}, {YEL}); }}
.li {{ display:flex; align-items:center; gap:28px; margin-bottom:38px; }}
.li b {{ flex:none; width:96px; height:96px; border-radius:50%; background:{GRN}; color:#06210f; font-size:54px; display:flex; align-items:center; justify-content:center; box-shadow:0 0 40px rgba(255,210,63,.45); }}
.li span {{ font-family:"Archivo"; font-weight:700; font-size:64px; letter-spacing:.02em; color:#fff; }}
.li.x b {{ background:{RED}; color:#fff; box-shadow:0 0 40px rgba(255,75,62,.5); }}
.alerta {{ position:absolute; left:80px; right:80px; top:1420px; text-align:center; font-family:"InterV"; font-weight:900; font-size:62px; color:#fff;
  background:{RED}; padding:26px 20px; border-radius:24px; box-shadow:0 0 80px rgba(255,75,62,.6); z-index:4; }}
#c01dc {{ position:absolute; left:50%; transform:translateX(-50%); top:1580px; white-space:nowrap; }}
.fone {{ position:absolute; left:50%; margin-left:-330px; top:240px; width:660px; height:1080px; border-radius:80px; background:#0d1220;
  border:16px solid #222a3a; box-shadow:0 40px 100px rgba(0,0,0,.6), 0 0 140px rgba(47,123,255,.45); z-index:2; }}
.scr {{ position:absolute; inset:12px; border-radius:60px; overflow:hidden; background:#f4f6fa; color:#111; padding:90px 40px 0; font-family:"InterV"; }}
.oh {{ font-size:44px; font-weight:900; margin-bottom:30px; }}
.orow {{ display:flex; align-items:center; gap:20px; background:#fff; border-radius:24px; padding:16px; box-shadow:0 6px 20px rgba(0,0,0,.08); margin-bottom:40px; }}
.orow img {{ width:120px; height:auto; }}
.orow b {{ display:block; font-size:40px; font-weight:900; }} .orow i {{ font-style:normal; font-size:28px; color:#556; }}
.ost {{ display:flex; align-items:center; gap:22px; font-size:38px; font-weight:700; margin-bottom:34px; }}
.ost u {{ text-decoration:none; width:56px; height:56px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:30px; background:#dde3ee; color:#3a4256; }}
.ost u.ok {{ background:#21c26b; color:#fff; }} .ost u.on {{ background:{BLU}; color:#fff; }} .ost.dim {{ color:#5a6274; }}
.fone.msg .scr {{ background:#eef1f6; padding-top:70px; }}
.mh {{ position:relative; padding:0 0 26px 104px; min-height:90px; border-bottom:1px solid #d6dbe4; margin-bottom:30px; }}
.mh u {{ position:absolute; left:0; top:0; width:86px; height:86px; border-radius:50%; background:{BLU}; color:#fff; text-decoration:none;
  display:flex; align-items:center; justify-content:center; font-size:42px; font-weight:900; }}
.mh b {{ display:block; font-size:40px; font-weight:900; padding-top:6px; }} .mh i {{ font-style:normal; font-size:26px; color:#667; }}
.bolha {{ background:#fff; border-radius:34px 34px 34px 10px; padding:24px 30px; font-size:36px; line-height:1.28; font-weight:500; margin-bottom:22px;
  box-shadow:0 6px 18px rgba(0,0,0,.08); max-width:94%; }}
.stamp {{ position:absolute; left:50%; margin-left:-330px; width:660px; text-align:center; font-family:"InterV"; font-weight:900; font-size:140px;
  border:14px solid currentColor; border-radius:30px; padding:10px 0; z-index:3; }}
.stamp.red {{ color:{RED}; text-shadow:0 0 50px rgba(255,75,62,.5); }}
.d3 {{ position:absolute; inset:0; mix-blend-mode:screen; }}
.kitov {{ position:absolute; left:50%; width:700px; margin-left:-350px; top:330px; z-index:8; text-align:center; }}
.kitov .kit {{ margin:0 auto; }}
.kitov .pglow {{ position:absolute; left:50%; top:40%; width:900px; height:600px; margin:-300px 0 0 -450px; border-radius:50%; background:radial-gradient(circle, rgba(255,210,63,.4), rgba(0,0,0,0) 65%); }}
.kitov b {{ position:relative; display:inline-block; margin-top:10px; font-family:"Montserrat"; font-weight:900; font-size:64px; color:#04140a; background:#21c26b; padding:14px 40px; border-radius:60px; box-shadow:0 0 50px rgba(43,214,123,.5); }}
.dbr {{ position:absolute; inset:0; z-index:2; overflow:hidden; }}
.atras {{ top:420px; bottom:-420px; opacity:.95; mix-blend-mode:normal; -webkit-mask-image:radial-gradient(closest-side, #000 55%, transparent 100%); mask-image:radial-gradient(closest-side, #000 55%, transparent 100%); }}
.halo {{ transform:translateZ(-700px) scale(1.45); position:absolute; left:50%; top:840px; width:1100px; height:1100px; margin:-550px 0 0 -550px; border-radius:50%;
  background:radial-gradient(circle, rgba(47,123,255,.55), rgba(47,123,255,.12) 45%, rgba(0,0,0,0) 70%); }}
.hero {{ position:absolute; left:50%; margin-left:-260px; top:420px; width:520px; height:auto; z-index:2; filter:drop-shadow(0 40px 60px rgba(0,0,0,.6)); }}
.hero.sm {{ margin-left:-200px; width:400px; top:380px; }}
.dup {{ position:absolute; top:470px; height:auto; z-index:2; filter:drop-shadow(0 30px 50px rgba(0,0,0,.6)); }}
.dup.e {{ left:110px; width:380px; }} .dup.p {{ right:110px; width:372px; }}
.rx {{ position:absolute; left:120px; right:120px; top:560px; background:#fbfaf5; color:#111; border-radius:24px; padding:60px 60px 70px; z-index:3;
  box-shadow:0 40px 100px rgba(0,0,0,.6); font-family:"InterV"; }}
.rxh {{ font-size:46px; font-weight:900; color:{BLU}; border-bottom:3px solid #ccd; padding-bottom:24px; margin-bottom:40px; }}
.rxl {{ font-family:"NewsI"; font-style:italic; font-size:66px; margin-bottom:26px; }} .rxl i {{ font-size:44px; color:#667; }}
.rxs {{ margin-top:40px; display:inline-block; font-size:40px; font-weight:900; color:#fff; background:{BLU}; padding:16px 30px; border-radius:14px; }}
.price {{ font-family:"InterV"; font-weight:900; font-size:170px; letter-spacing:-.04em; }}
.price small {{ font-size:60px; font-weight:700; letter-spacing:0; margin-left:8px; }}
.risco {{ position:absolute; left:18%; right:18%; top:50%; height:16px; margin-top:-8px; background:{RED}; border-radius:8px; transform-origin:0 50%;
  transform:rotate(-8deg); box-shadow:0 0 30px rgba(255,75,62,.6); display:block; }}
.kitbg {{ position:absolute; inset:0; }}
.pcard {{ position:absolute; left:150px; right:150px; top:1440px; z-index:3; background:#fff; color:#0b1630; border-radius:36px; padding:34px 40px; text-align:center;
  box-shadow:0 30px 80px rgba(0,0,0,.5); font-family:"InterV"; }}
.pcard b {{ display:block; font-size:50px; font-weight:900; letter-spacing:.06em; color:{BLU}; }}
.pcard span {{ display:block; font-size:140px; font-weight:900; line-height:1; letter-spacing:-.04em; }}
.pcard i {{ font-style:normal; font-size:38px; font-weight:700; color:#556; }}
.seta3 {{ position:absolute; left:0; right:0; top:1080px; display:flex; justify-content:center; gap:40px; z-index:3; }}
.seta3 svg {{ width:150px; height:150px; filter:drop-shadow(0 0 30px rgba(43,214,123,.6)); }}
.path {{ position:absolute; left:60px; right:60px; height:600px; border-radius:40px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:20px; z-index:3; }}
.path b {{ width:150px; height:150px; border-radius:50%; font-size:96px; font-weight:900; display:flex; align-items:center; justify-content:center; color:#061020; }}
.path span {{ font-family:"Archivo"; font-weight:700; font-size:96px; text-align:center; line-height:1; }}
.path.g {{ top:260px; background:rgba(33,194,107,.2); border:4px solid #21c26b; box-shadow:0 0 80px rgba(33,194,107,.35); }} .path.g b {{ background:#21c26b; }}
.path.r {{ top:1000px; background:rgba(255,75,62,.18); border:4px solid {RED}; box-shadow:0 0 80px rgba(255,75,62,.35); }} .path.r b {{ background:{RED}; color:#fff; }}
.tag {{ position:absolute; left:60px; right:60px; top:240px; text-align:center; font-family:"InterV"; font-weight:900; font-size:52px; padding:22px; border-radius:24px; z-index:3; }}
.tag.g {{ background:#21c26b; color:#061020; }} .tag.r {{ background:{RED}; color:#fff; }}
.cta-g {{ position:absolute; left:70px; right:70px; z-index:3; display:flex; flex-direction:column; align-items:center; gap:30px; }}
.cta-g .bt {{ width:100%; text-align:center; font-family:"Montserrat"; font-weight:900; font-size:62px; color:#1b1b1b; letter-spacing:.01em;
  padding:40px 20px; border-radius:200px; background:linear-gradient(180deg, #FFD54A 0%, #FFB52E 55%, #FF9A1F 100%);
  box-shadow:0 0 0 4px rgba(0,0,0,.25), 0 20px 50px rgba(0,0,0,.5), inset 0 4px 0 rgba(255,255,255,.55), 0 0 90px rgba(255,170,40,.5); }}
.cta-g .seta {{ width:150px; height:150px; filter:drop-shadow(0 12px 26px rgba(0,0,0,.45)); }}
.cta-g.fixo {{ top:1500px; gap:16px; }} .cta-g.fixo .bt {{ font-size:52px; padding:32px 20px; }} .cta-g.fixo .seta {{ width:110px; height:110px; }}
.selo {{ position:absolute; left:50%; margin-left:-250px; top:1040px; width:500px; height:500px; z-index:3; filter:drop-shadow(0 20px 40px rgba(0,0,0,.5)) drop-shadow(0 0 60px rgba(255,210,63,.35)); }}
.fs {{ position:absolute; left:60px; right:60px; top:0; bottom:0; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:34px; z-index:3; text-align:center; transform-style:preserve-3d; }}
.fs > * {{ position:relative; }}
.fs .disp {{ line-height:.98; }} .fs .cond.mid {{ font-size:70px; line-height:1.05; }} .fs .kick {{ font-size:42px; }}
.fs .chip.big {{ white-space:normal; max-width:940px; line-height:1.15; }}
.vidro2 {{ width:100%; display:flex; flex-direction:column; align-items:stretch; gap:20px; text-align:left; }}
.vidro2 .li {{ margin:0 !important; padding:18px 30px 18px 18px; border-radius:60px; background:linear-gradient(160deg, rgba(10,18,40,.82), rgba(10,18,40,.62));
  border:2px solid rgba(255,255,255,.22); box-shadow:0 20px 50px rgba(0,0,0,.45); backdrop-filter:blur(6px); }}
.vidro2 .li span {{ font-size:54px; line-height:1.05; }} .vidro2 .li b {{ width:78px; height:78px; font-size:44px; }}
.qt {{ font-family:"NewsI"; font-style:italic; font-weight:500; font-size:92px; line-height:1.08; color:#fff; text-shadow:0 0 50px rgba(47,123,255,.5); max-width:960px; }}
.numw {{ display:flex; flex-direction:column; align-items:center; gap:10px; }} .numw .num {{ line-height:.9; }}
.prods {{ display:flex; align-items:flex-end; justify-content:center; gap:30px; height:520px; }}
.prods img {{ height:100%; width:auto; filter:drop-shadow(0 30px 50px rgba(0,0,0,.6)); }}
.stamp.rel, .price.rel {{ position:relative; left:auto; margin:0; }}
.cta-g.rel {{ position:relative; left:auto; right:auto; width:100%; }}
.cta-g .bt {{ font-size:50px !important; line-height:1.1; padding:36px 30px !important; }}
.kbx.col {{ display:flex; flex-direction:column; align-items:center; gap:18px; }}
.pactag {{ position:absolute; inset:0; z-index:8; pointer-events:none; }}
.ptag {{ position:absolute; left:50%; top:120px; transform:translateX(-50%); white-space:nowrap; font-family:"InterV"; font-weight:900; font-size:40px; letter-spacing:.06em;
  color:#fff; background:rgba(215,38,46,.92); padding:16px 30px; border-radius:40px; box-shadow:0 10px 30px rgba(0,0,0,.5); }}
.pchip {{ position:absolute; left:50%; top:1080px; transform:translateX(-50%); background:#21c26b !important; border-color:#21c26b !important; font-size:64px !important; }}
.tarja {{ position:absolute; left:50px; top:1150px; z-index:4; padding:18px 30px 16px; border-radius:22px; background:rgba(8,14,32,.82); border-left:10px solid #D7262E;
  box-shadow:0 10px 30px rgba(0,0,0,.5); font-family:"InterV"; color:#fff; }}
.tarja b {{ display:block; font-weight:900; font-size:52px; line-height:1; }} .tarja span {{ display:block; margin-top:8px; font-weight:600; font-size:30px; color:#cfd8ee; }}
.cap {{ position:absolute; left:50px; right:50px; top:1330px; z-index:7; display:flex; justify-content:center; }}
.cap-in {{ font-family:"Montserrat"; font-weight:900; font-size:80px; color:#fff; text-align:center; line-height:1.08; text-transform:uppercase;
  -webkit-text-stroke:3px #000; paint-order:stroke fill; text-shadow:0 8px 24px rgba(0,0,0,.85); }}
.cap-in span {{ display:inline-block; margin:0 .1em; }}
.cap::before {{ content:""; position:absolute; left:-40px; right:-40px; top:-30px; bottom:-30px; z-index:-1; background:radial-gradient(60% 60% at 50% 50%, rgba(0,0,0,.42), rgba(0,0,0,0) 75%); }}
.cta {{ position:absolute; inset:0; z-index:8; pointer-events:none; }}
.luz {{ position:absolute; inset:0; z-index:7; pointer-events:none; mix-blend-mode:screen; opacity:0; }}
.luz video {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; opacity:.42; }}
.grao {{ position:absolute; inset:0; z-index:9; pointer-events:none; opacity:.06; mix-blend-mode:overlay;
  background-image:url("assets/img/grao.png"); background-size:4320px 1920px; background-repeat:no-repeat; }}
.vinheta {{ position:absolute; inset:0; z-index:9; pointer-events:none; background:radial-gradient(ellipse at center, rgba(0,0,0,0) 60%, rgba(0,0,0,.3) 100%); }}
.grn {{ color:{GRN}; }}
.num.grn {{ color:{GRN}; text-shadow:0 4px 0 #22b868, 0 8px 0 #1a9654, 0 12px 0 #137240, 0 16px 0 #0c4f2c, 0 30px 50px rgba(0,0,0,.6), 0 0 110px rgba(43,214,123,.55); }}
.cond.grn {{ color:{GRN}; text-shadow:0 0 30px rgba(43,214,123,.45); }}
.chip.grn {{ background:#21c26b; border-color:#21c26b; color:#04140a; box-shadow:0 0 50px rgba(43,214,123,.5); }}
.li b {{ box-shadow:0 0 40px rgba(43,214,123,.5) !important; }} .li.x b {{ box-shadow:0 0 40px rgba(255,75,62,.5) !important; }}
.pfull {{ display:flex; flex-direction:column; align-items:center; }}
.pfull .prot {{ font-family:"Archivo"; font-weight:700; font-size:44px; letter-spacing:.3em; color:#ffb3ad; margin-bottom:-6px; }}
.pfull .pv {{ position:relative; display:inline-block; font-family:"InterV"; font-weight:900; letter-spacing:-.04em; line-height:.95; color:{RED};
  text-shadow:0 4px 0 #b32c22, 0 8px 0 #8a2018, 0 12px 0 #63150f, 0 30px 50px rgba(0,0,0,.6), 0 0 90px rgba(255,75,62,.45); }}
.risco2 {{ position:absolute; left:-6%; right:-6%; top:50%; height:18px; margin-top:-9px; background:#fff; border-radius:9px; transform-origin:0 50%;
  transform:rotate(-9deg); box-shadow:0 0 0 4px rgba(120,10,10,.55), 0 0 30px rgba(255,255,255,.6); display:block; }}
.escada {{ display:flex; flex-direction:column; align-items:center; gap:26px; }}
.fgrad2 {{ position:absolute; inset:0; background:rgba(3,6,15,.45); }}
.par {{ display:flex; justify-content:center; gap:30px; width:100%; }} .lado {{ display:flex; flex-direction:column; align-items:center; gap:24px; width:470px; }}
.lado .prods {{ width:470px; }} .lado .prods img {{ max-width:470px; object-fit:contain; }}
.fbgi {{ position:absolute; inset:0; overflow:hidden; }} .fbgi img, .fill2 img, .phbg {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
.fill2 {{ position:absolute; inset:0; overflow:hidden; }} .fill2.prbg img {{ transform-origin:92% 56%; }}
.fgradi {{ position:absolute; inset:0; background:linear-gradient(to bottom, rgba(4,8,20,.9) 0%, rgba(4,8,20,.7) 30%, rgba(4,8,20,.45) 42%, rgba(4,8,20,.1) 62%, rgba(4,8,20,.55) 100%); }}
.fs.top .numw .cond {{ background:rgba(4,8,20,.72); padding:8px 22px; border-radius:30px; }}
.fs.top {{ justify-content:flex-start; padding-top:220px; bottom:640px; gap:26px; }}
.phwrap {{ position:absolute; inset:0; overflow:hidden; transform-origin:50% 45%; transform-style:flat; perspective:none; }}
.uiq {{ position:absolute; left:0; top:0; transform-origin:0 0; overflow:hidden; border-radius:34px; background:#fff; font-family:"InterV"; color:#0b1630; }}
.ui {{ position:absolute; inset:0; display:flex; flex-direction:column; justify-content:space-between; padding:22px 22px 30px; gap:14px; background:#f5f7fb; }}
.ubtn {{ background:#2F7BFF; color:#fff; text-align:center; font-weight:800; font-size:24px; padding:20px; border-radius:18px; }}
.ub {{ display:flex; justify-content:space-between; font-size:15px; font-weight:700; color:#333; padding:0 6px; }} .ub b {{ color:#0f5a30; font-size:14px; }}
.uk {{ background:#fff; border-radius:22px; padding:26px 18px 22px; text-align:center; box-shadow:0 6px 20px rgba(0,0,0,.06); }}
.uk i {{ display:inline-flex; width:74px; height:74px; border-radius:50%; background:#21c26b; color:#fff; font-style:normal; font-size:44px; font-weight:900; align-items:center; justify-content:center; }}
.uk h3 {{ font-size:36px; font-weight:900; margin-top:12px; letter-spacing:-.02em; }} .uk p {{ font-size:20px; color:#556; margin-top:4px; font-weight:600; }}
.uc {{ background:#fff; border-radius:22px; padding:16px 18px; display:flex; flex-direction:column; gap:12px; box-shadow:0 6px 20px rgba(0,0,0,.06); }}
.ur {{ display:flex; justify-content:space-between; font-size:21px; color:#556; }} .ur b {{ color:#0b1630; }} .ur b.g {{ color:#1f8f4e; }}
.up {{ display:flex; gap:14px; align-items:center; border-top:1px solid #e6e9f0; border-bottom:1px solid #e6e9f0; padding:12px 0; }}
.up img {{ width:58px; height:104px; object-fit:contain; }} .up b {{ display:block; font-size:22px; }} .up span {{ font-size:16px; color:#667; }}
.us {{ background:#0b1630; color:#fff; border-radius:22px; padding:18px; display:flex; flex-direction:column; gap:8px; }}
.us b {{ font-size:20px; color:#7fb2ff; }} .us span {{ font-size:24px; font-weight:800; }} .us em {{ font-style:normal; font-size:16px; color:#ffb3ad; font-weight:700; }}
.ubar {{ height:10px; border-radius:6px; background:rgba(255,255,255,.18); overflow:hidden; }} .ubar i {{ display:block; height:100%; background:#2F7BFF; transform-origin:0 50%; }}
.um {{ background:#fff; border-radius:22px; padding:18px; display:flex; flex-direction:column; gap:10px; font-size:19px; color:#334; }}
.um .uh {{ border-bottom:1px solid #e6e9f0; padding-bottom:8px; }} .um u {{ text-decoration:none; color:#889; margin-right:6px; }} .um .send {{ color:#2F7BFF; text-align:right; }}
.uk.g2 {{ margin-top:auto; }}
.tri {{ position:absolute; left:0; right:0; top:330px; height:1000px; display:flex; flex-direction:column; gap:10px; padding:0 40px; }}
.tpb {{ position:relative; flex:1; border-radius:26px; overflow:hidden; box-shadow:0 20px 50px rgba(0,0,0,.55); border:2px solid rgba(255,255,255,.25); }}
.tpb img {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; object-position:50% 16%; }}
.tpb span {{ position:absolute; left:26px; bottom:20px; font-family:"Archivo"; font-weight:700; font-size:44px; letter-spacing:.3em; color:#fff; text-shadow:0 4px 18px rgba(0,0,0,.8); }}
.trik {{ position:absolute; left:0; right:0; top:120px; text-align:center; z-index:3; }} .trik b {{ font-family:"InterV"; font-weight:900; font-size:150px; line-height:.9; color:{YEL}; text-shadow:0 6px 0 #966d05, 0 20px 40px rgba(0,0,0,.6); }}
.trik span {{ display:block; font-family:"Archivo"; font-weight:700; font-size:46px; letter-spacing:.3em; color:#fff; }}
.mes {{ position:absolute; left:60px; right:60px; top:140px; text-align:center; display:flex; flex-direction:column; gap:22px; align-items:center; }}
.mrow {{ display:flex; gap:18px; }} .mrow b {{ font-family:"Archivo"; font-weight:700; font-size:40px; letter-spacing:.18em; color:#fff; padding:10px 20px; border-radius:40px; background:rgba(255,255,255,.12); border:2px solid rgba(255,255,255,.35); }}
.mbar {{ width:860px; height:16px; border-radius:10px; background:rgba(255,255,255,.18); overflow:hidden; }} .mbar i {{ display:block; height:100%; background:linear-gradient(90deg,#2F7BFF,#2BD67B); transform-origin:0 50%; }}
.mlk {{ font-size:120px; }}
.pgrad {{ position:absolute; inset:0; background:linear-gradient(100deg, rgba(4,8,20,.55) 0%, rgba(4,8,20,.15) 45%, rgba(4,8,20,0) 70%); }}
.pcard2 {{ position:absolute; left:30px; top:190px; z-index:4; width:500px; padding:24px 30px 28px !important; padding:26px 36px 30px; border-radius:30px; background:rgba(8,16,40,.93);
  border:2px solid rgba(47,123,255,.6); box-shadow:0 30px 70px rgba(0,0,0,.5), 0 0 60px rgba(47,123,255,.25); color:#fff; font-family:"InterV"; }}
.pctag {{ display:block; width:fit-content; white-space:nowrap; font-style:normal; font-family:"Archivo"; font-weight:700; font-size:28px; letter-spacing:.2em; color:#081024; background:{YEL}; padding:6px 16px; border-radius:30px; margin-bottom:22px; }}
.pnum {{ margin-top:6px; font-weight:900; font-size:196px; line-height:1.0; letter-spacing:-.04em; color:#fff; text-shadow:0 0 50px rgba(47,123,255,.6); white-space:nowrap; }}
.pnum sup {{ font-size:84px; vertical-align:top; position:relative; top:16px; margin-right:4px; }} .pnum em {{ display:block; margin-left:6px; margin-top:-10px; font-style:normal; font-size:56px; font-weight:800; letter-spacing:0; color:#9fc1ff; }}
.ptot {{ font-size:36px; font-weight:800; color:#cfe0ff; margin-top:8px; white-space:nowrap; }} .psub {{ font-size:36px; font-weight:700; color:#cfe0ff; }} .psub2 {{ font-family:"Archivo"; font-weight:700; font-size:34px; letter-spacing:.2em; color:{YEL}; margin-bottom:12px; }}
.pchip2 {{ margin-top:14px; display:inline-block; font-weight:900; font-size:34px; white-space:nowrap; padding:12px 22px; border-radius:40px; }} .pchip2.g {{ background:#21c26b; color:#04140a; }} .pchip2.r {{ background:{RED}; color:#fff; }}
.pcard2 .pchip2 {{ display:block; width:fit-content; }}
.gtag {{ position:absolute; left:50px; top:140px; z-index:4; display:flex; align-items:center; gap:22px; font-family:"InterV"; }}
.gtag b {{ font-family:"Archivo"; font-weight:700; font-size:46px; letter-spacing:.25em; color:#081024; background:{YEL}; padding:10px 22px; border-radius:40px; }}
.gval {{ position:relative; font-weight:900; font-size:78px; color:{RED}; text-shadow:0 6px 24px rgba(0,0,0,.7); }} .gfree {{ font-weight:900; font-size:86px; color:{GRN}; text-shadow:0 0 40px rgba(43,214,123,.6), 0 6px 24px rgba(0,0,0,.7); }}
.uiv {{ position:absolute; inset:0; background:#000; }} .uiv img {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; filter:brightness(.6); }}
.uivg {{ position:absolute; inset:0; background:linear-gradient(to top, rgba(0,0,0,.85), rgba(0,0,0,0) 60%); }}
.uivt {{ position:absolute; left:40px; bottom:90px; color:#fff; display:flex; flex-direction:column; gap:12px; }} .uivt i {{ display:block; margin-bottom:8px; font-style:normal; font-family:"Archivo"; font-weight:700; font-size:30px; letter-spacing:.25em; color:{YEL}; }}
.uivt b {{ display:block; font-weight:900; font-size:76px; line-height:1.05; letter-spacing:-.02em; }}
.uivp {{ position:absolute; left:50%; top:42%; width:120px; height:120px; margin:-60px 0 0 -60px; border-radius:50%; background:rgba(255,255,255,.9); color:#0b1630; font-size:54px; display:flex; align-items:center; justify-content:center; padding-left:10px; }}
.uivbar {{ position:absolute; left:40px; right:40px; bottom:40px; height:10px; border-radius:6px; background:rgba(255,255,255,.3); overflow:hidden; }} .uivbar i {{ display:block; height:100%; background:#ff3b3b; transform-origin:0 50%; }}
.uie {{ position:absolute; inset:0; background:#140a0a; perspective:1600px; }}
.uiec {{ position:absolute; inset:0; padding:70px 50px; text-align:center; display:flex; flex-direction:column; align-items:center; gap:22px; color:#f3dcc0;
  background:radial-gradient(80% 60% at 50% 45%, #5a1e22 0%, #2a0d10 60%, #140a0a 100%); font-family:"InterV"; }}
.uiec i {{ font-style:normal; font-family:"Archivo"; font-weight:700; font-size:26px; letter-spacing:.3em; color:#d9a86c; }}
.uiec b {{ font-family:"NewsI"; font-style:italic; font-weight:600; font-size:84px; line-height:1; color:#f6e2c4; }}
.uiec em {{ font-style:normal; font-size:24px; color:#d9b48a; }} .orn {{ margin-top:auto; font-size:90px; color:#d9a86c; }}
.uiep {{ display:none; }}
.cap.faixa {{ top:1700px; }} .cap.faixa .cap-in {{ background:rgba(0,0,0,.55); padding:10px 26px; border-radius:18px; }} .cap.faixa::before {{ display:none; }}
.cap.capalta {{ top:1170px; }} .cap.capcta {{ top:860px !important; }} .cap.capbaixa {{ top:1690px !important; }}
.cdw {{ display:flex; flex-direction:column; align-items:center; gap:10px; padding:26px 50px; border-radius:40px; background:rgba(4,8,20,.72); border:3px solid rgba(255,75,62,.7); box-shadow:0 0 70px rgba(255,75,62,.35); }}
.cdw b {{ font-family:"Montserrat"; font-weight:900; font-size:200px; line-height:1; color:#fff; font-variant-numeric:tabular-nums; }} .cdw span {{ font-family:"Archivo"; font-weight:700; font-size:34px; letter-spacing:.18em; color:#ffb3ad; }}
.duo {{ display:flex; gap:28px; width:100%; }} .dcard {{ flex:1; display:flex; flex-direction:column; align-items:center; gap:14px; padding:34px 20px; border-radius:36px; background:rgba(4,8,20,.72); }}
.dcard b {{ width:130px; height:130px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:80px; font-weight:900; }}
.dcard span {{ font-family:"InterV"; font-weight:900; font-size:66px; line-height:1; text-align:center; color:#fff; }}
.dcard.g {{ border:4px solid #21c26b; box-shadow:0 0 60px rgba(33,194,107,.35); }} .dcard.g b {{ background:#21c26b; color:#04140a; }}
.dcard.r {{ border:4px solid {RED}; box-shadow:0 0 60px rgba(255,75,62,.35); }} .dcard.r b {{ background:{RED}; color:#fff; }}
.evlg {{ display:flex; flex-direction:column; align-items:center; gap:8px; filter:drop-shadow(0 8px 24px rgba(0,0,0,.6)); }}
.evlg img {{ width:420px; height:auto; }} .evlg span {{ background:#fff; color:#0b1630; font-family:"InterV"; font-weight:800; font-size:24px; letter-spacing:.08em; padding:5px 16px; border-radius:3px; }}
.evlg.topo {{ position:absolute; left:0; right:0; top:60px; z-index:4; }} .evlg.topo img {{ width:280px; }} .evlg.topo span {{ font-size:18px; padding:4px 12px; }}
.evlg.sm img {{ width:300px; }} .evlg.sm span {{ font-size:19px; padding:4px 12px; }}
.evlg.pclogo {{ position:absolute; left:34px; top:60px; z-index:4; align-items:flex-start; }} .evlg.pclogo img {{ width:300px; }} .evlg.pclogo span {{ font-size:18px; }}
.evlg.xs {{ align-items:flex-start; margin-top:20px; }} .evlg.xs img {{ width:230px; }} .evlg.xs span {{ font-size:15px; padding:3px 10px; }}
.evlg.corner {{ position:absolute; right:40px; top:120px; z-index:5; }} .evlg.corner img {{ width:250px; }} .evlg.corner span {{ font-size:16px; }}
.evlg.ctalg {{ position:absolute; left:0; right:0; bottom:calc(100% + 44px); }} .evlg.ctalg img {{ width:340px; }} .evlg.ctalg span {{ font-size:19px; }}
.evcard {{ position:absolute; left:70px; right:70px; top:180px; z-index:4; display:flex; flex-direction:column; align-items:center; gap:30px; padding:44px 30px 40px; border-radius:40px;
  background:linear-gradient(160deg, rgba(10,20,50,.86), rgba(6,12,30,.78)); border:2px solid rgba(47,123,255,.55); box-shadow:0 30px 80px rgba(0,0,0,.55), 0 0 60px rgba(47,123,255,.25); }}
.gcovs {{ position:absolute; left:40px; top:840px; width:600px; height:420px; z-index:3; }}
.gcov {{ position:absolute; bottom:0; width:200px; height:290px; border-radius:10px; padding:18px 14px; display:flex; flex-direction:column; gap:10px; color:#fff;
  box-shadow:0 26px 40px rgba(0,0,0,.55), inset 0 0 0 2px rgba(255,210,63,.45); font-family:"InterV"; overflow:hidden; }}
.gcov i {{ font-style:normal; font-family:"Archivo"; font-weight:700; font-size:15px; letter-spacing:.22em; color:{YEL}; }}
.gcov b {{ font-weight:900; font-size:30px; line-height:1; }} .gcov u {{ text-decoration:none; margin-top:auto; font-size:46px; color:{YEL}; }}
.gcov.v {{ background:linear-gradient(170deg, #1b2a55, #08112a); }} .gcov.e {{ background:radial-gradient(80% 60% at 50% 40%, #5a1e22, #1c0a0c); }} .gcov.e b {{ font-family:"NewsI"; font-style:italic; font-weight:600; color:#f6e2c4; }}
.gcov.g0 {{ left:0; }} .gcov.g1 {{ left:190px; bottom:12px; }} .gcov.g2 {{ left:380px; }}
.ubig {{ position:relative; overflow:hidden; text-align:center; font-family:"Montserrat"; font-weight:900; font-size:22px; color:#1b1b1b; padding:20px 12px; border-radius:40px;
  background:linear-gradient(180deg,#FFD54A,#FF9A1F); box-shadow:0 8px 20px rgba(0,0,0,.25); }}
.ubig i {{ position:absolute; left:50%; top:50%; width:80px; height:80px; margin:-40px 0 0 -40px; border-radius:50%; background:rgba(255,255,255,.8); }}
.up2 {{ display:flex; gap:14px; align-items:center; border-top:1px solid #e6e9f0; border-bottom:1px solid #e6e9f0; padding:12px 0; }}
.up2 img {{ width:110px; height:110px; object-fit:cover; object-position:70% 62%; border-radius:12px; }} .up2 b {{ display:block; font-size:22px; }} .up2 span {{ display:block; font-size:16px; color:#667; }} .up2 em {{ font-style:normal; font-size:18px; font-weight:800; color:#0f5a30; }}
.uiep2 {{ position:absolute; inset:0; background:#f6eee0; color:#3a1a1c; padding:60px 50px; display:flex; flex-direction:column; align-items:center; gap:18px; transform-origin:0 50%; backface-visibility:hidden; font-family:"InterV"; }}
.uiep2 i {{ font-style:normal; font-family:"Archivo"; font-weight:700; font-size:26px; letter-spacing:.25em; color:#9a5a3a; }}
.uiep2 b {{ font-family:"NewsI"; font-style:italic; font-weight:600; font-size:64px; color:#3a1a1c; }}
.uiep2 .lsvg {{ width:360px; height:360px; background:#2a0d10; border-radius:24px; padding:20px; }}
.uiep2 p {{ font-size:26px; line-height:1.35; text-align:center; color:#4a2a2a; }} .uiep2 u {{ text-decoration:none; margin-top:auto; font-size:22px; color:#9a5a3a; }}
.chap {{ position:absolute; left:50px; right:50px; top:1020px; z-index:4; padding:30px 34px; border-radius:30px; background:rgba(8,12,28,.82); border:2px solid rgba(255,210,63,.5); box-shadow:0 30px 70px rgba(0,0,0,.55); color:#fff; font-family:"InterV"; }}
.chap i {{ font-style:normal; font-family:"Archivo"; font-weight:700; font-size:26px; letter-spacing:.25em; color:{YEL}; }} .chap b {{ display:block; font-weight:900; font-size:66px; line-height:1.05; margin-top:8px; }}
.chap > span {{ display:block; font-size:28px; color:#cfd8ee; margin-top:6px; }}
.chbar {{ display:flex; align-items:center; gap:16px; margin-top:20px; }} .chbar u {{ text-decoration:none; width:56px; height:56px; border-radius:50%; background:#fff; color:#0b1630; display:flex; align-items:center; justify-content:center; font-size:24px; }}
.chtrk {{ flex:1; height:8px; border-radius:6px; background:rgba(255,255,255,.25); overflow:hidden; }} .chtrk em {{ display:block; height:100%; background:#ff3b3b; transform-origin:0 50%; }} .chbar span {{ font-size:22px; color:#cfd8ee; }}
.ggrad {{ position:absolute; inset:0; background:linear-gradient(to top, rgba(4,8,20,.92) 0%, rgba(4,8,20,.7) 22%, rgba(4,8,20,.3) 42%, rgba(4,8,20,0) 55%); }}
.gcard {{ position:absolute; left:50px; right:50px; top:1120px; z-index:4; display:flex; flex-direction:column; align-items:center; gap:14px; text-align:center; }}
.gline {{ display:flex; gap:16px; align-items:center; }} .gline b {{ font-family:"Archivo"; font-weight:700; font-size:40px; letter-spacing:.25em; color:#081024; background:{YEL}; padding:8px 20px; border-radius:40px; }}
.gline i {{ font-style:normal; font-family:"Archivo"; font-weight:700; font-size:34px; letter-spacing:.22em; color:#fff; }}
.gtit {{ font-family:"InterV"; font-weight:900; font-size:96px; line-height:.98; letter-spacing:-.03em; color:#fff; text-shadow:0 0 50px rgba(47,123,255,.5), 0 8px 30px rgba(0,0,0,.6); }}
.gvals {{ display:flex; gap:24px; align-items:center; }}
.tribg {{ position:absolute; inset:0; background:radial-gradient(90% 60% at 50% 40%, #12234a 0%, #08112a 55%, #03060f 100%); }}
.dcard.n {{ border:4px solid rgba(255,255,255,.35); }} .dcard.n b {{ background:rgba(255,255,255,.18); color:#fff; }}
.dcard em {{ font-style:normal; font-family:"Archivo"; font-weight:700; font-size:38px; letter-spacing:.2em; color:#cfd8ee; }} .dcard.g em {{ color:#2BD67B; }}
.dcard.g.big {{ transform:scale(1.06); }}
.kitimg {{ width:700px; height:640px; margin:0 auto; border-radius:40px; overflow:hidden; box-shadow:0 30px 80px rgba(0,0,0,.6), 0 0 0 3px rgba(255,255,255,.25); }}
.kitimg img {{ width:100%; height:100%; object-fit:cover; object-position:50% 72%; }}
.gcovs.solo {{ left:50%; margin-left:-300px; top:900px; }}
.frsolo {{ z-index:7 !important; background:#000; }}
.frsolo .fill2 img {{ transform-origin:50% 78%; }} .frnum {{ position:absolute; left:0; right:0; top:230px; text-align:center; }} .frnum b {{ display:block; font-family:"InterV"; font-weight:900; font-size:300px; line-height:.9; color:#2BD67B; text-shadow:0 4px 0 #22b868, 0 8px 0 #1a9654, 0 12px 0 #137240, 0 30px 50px rgba(0,0,0,.6), 0 0 110px rgba(43,214,123,.55); }} .frnum span {{ font-family:"Archivo"; font-weight:700; font-size:60px; letter-spacing:.3em; color:#fff; }}
.frpill {{ position:absolute; left:50%; top:430px; transform:translateX(-50%); white-space:nowrap; font-family:"Montserrat"; font-weight:900; font-size:72px; color:#04140a; background:#21c26b; padding:16px 46px; border-radius:60px; box-shadow:0 0 60px rgba(43,214,123,.55); }}
.tribgr img {{ filter:blur(14px) brightness(.55); }}
.tri {{ top:300px !important; height:1260px !important; }}
.ebw {{ z-index:2; }}
.ebc {{ position:absolute; inset:0; padding:9% 8%; display:flex; flex-direction:column; align-items:center; gap:5%; text-align:center; color:#f3dcc0;
  background:radial-gradient(80% 60% at 50% 42%, #6a2228 0%, #34101a 60%, #1a0709 100%); font-family:"InterV"; }}
.ebc i {{ font-style:normal; font-family:"Archivo"; font-weight:700; font-size:30px; letter-spacing:.32em; color:#d9a86c; }}
.ebc b {{ font-family:"NewsI"; font-style:italic; font-weight:600; font-size:104px; line-height:1; color:#f6e2c4; }}
.ebc em {{ font-style:normal; font-size:28px; color:#d9b48a; }} .ebc .orn {{ font-size:110px; color:#d9a86c; margin-top:auto; }}
.ebsel {{ position:absolute; right:7%; top:5%; font-family:"Archivo"; font-weight:700; font-size:26px; letter-spacing:.25em; color:#2a0d10; background:#d9a86c; padding:6px 16px; border-radius:30px; }}
.ebmk {{ position:absolute; left:0; right:0; bottom:4%; display:flex; justify-content:center; opacity:.8; }} .ebmk img {{ width:30%; }}
.ebsh {{ position:absolute; inset:0; background:linear-gradient(100deg, rgba(255,255,255,.08) 0%, rgba(0,0,0,0) 35%, rgba(0,0,0,.25) 100%); pointer-events:none; }}
.gcov.img {{ padding:0; background:#000; }} .gcov.img img {{ width:100%; height:100%; object-fit:cover; }}
.gdim {{ position:absolute; inset:0; background:rgba(5,9,20,.5); backdrop-filter:blur(10px); z-index:2; }}
.gcover {{ position:absolute; left:50%; margin-left:-260px; top:200px; width:520px; height:auto; z-index:3; border-radius:6px; box-shadow:0 30px 60px rgba(0,0,0,.7), 0 0 0 2px rgba(217,168,108,.5); }}
.atrz {{ position:absolute; inset:0; z-index:2; pointer-events:none; perspective:1400px; }}
.atr {{ position:absolute; left:24px; right:24px; top:34px; text-align:center; font-family:"InterV"; font-weight:900; letter-spacing:-.03em; color:#fff;
  text-transform:uppercase; -webkit-text-stroke:2px rgba(0,0,0,.35); paint-order:stroke fill; text-shadow:0 0 6px rgba(0,0,0,.75), 0 0 80px rgba(47,123,255,.5), 0 10px 34px rgba(0,0,0,.7); }}
.atr .l1 {{ font-size:78px; line-height:.95; }} .atr .l2 {{ font-size:122px; line-height:.92; white-space:nowrap; }}
.kbx2 {{ display:flex; flex-direction:column; align-items:center; gap:18px; }}
.gift {{ width:900px; padding:60px 50px 56px; border-radius:48px; display:flex; flex-direction:column; align-items:center; gap:22px;
  background:linear-gradient(160deg, rgba(255,255,255,.16), rgba(255,255,255,.04)); border:2px solid rgba(255,210,63,.55);
  box-shadow:0 40px 90px rgba(0,0,0,.55), 0 0 90px rgba(255,210,63,.22), inset 0 1px 0 rgba(255,255,255,.35); }}
.gift i {{ font-style:normal; font-family:"Archivo"; font-weight:700; font-size:46px; letter-spacing:.3em; color:{YEL}; }}
.gift svg {{ width:170px; height:170px; filter:drop-shadow(0 0 30px rgba(255,210,63,.45)); }}
.gift b {{ font-family:"InterV"; font-weight:900; font-size:104px; line-height:.98; letter-spacing:-.03em; color:#fff; text-shadow:0 0 60px rgba(47,123,255,.45); }}
.gift u {{ text-decoration:none; font-family:"Archivo"; font-weight:700; font-size:44px; letter-spacing:.25em; color:rgba(255,255,255,.75); }}
.gpilha {{ display:flex; gap:18px; justify-content:center; }}
.gmini {{ width:290px; height:250px; border-radius:30px; padding:26px 18px; display:flex; flex-direction:column; justify-content:center; gap:12px;
  background:linear-gradient(160deg, rgba(20,30,62,.92), rgba(8,14,32,.92)); border:2px solid rgba(255,210,63,.5); box-shadow:0 20px 50px rgba(0,0,0,.5); }}
.gmini i {{ font-style:normal; font-family:"Archivo"; font-weight:700; font-size:30px; letter-spacing:.2em; color:{YEL}; }}
.gmini b {{ font-family:"InterV"; font-weight:900; font-size:44px; line-height:1; color:#fff; }}
.gmini.g0 {{ transform:rotate(-5deg); }} .gmini.g2 {{ transform:rotate(5deg); }}
.cond.dia {{ color:#FFB547; text-shadow:0 0 30px rgba(255,181,71,.5); font-size:60px !important; }} .cond.noite {{ color:#DCE6FF; text-shadow:0 0 30px rgba(143,180,255,.7); font-size:60px !important; }}
.setasv {{ display:flex; justify-content:center; gap:40px; }} .setasv svg {{ width:110px; height:110px; filter:drop-shadow(0 0 24px rgba(43,214,123,.7)); }}
.ofl {{ font-family:"InterV"; font-weight:900; font-size:76px; color:#fff; letter-spacing:-.01em; text-shadow:0 8px 30px rgba(0,0,0,.6); }}
.ofl b {{ color:{GRN}; font-size:110px; text-shadow:0 0 50px rgba(43,214,123,.6); }}
.ofl s {{ color:{RED}; font-size:62px; text-decoration-thickness:7px; text-decoration-color:#fff; margin-left:12px; }}
.bal {{ display:flex; flex-direction:column; align-items:center; gap:22px; width:100%; perspective:1600px; }}
.bcard {{ width:100%; border-radius:44px; padding:44px 40px 40px; text-align:center; display:flex; flex-direction:column; align-items:center; gap:12px;
  background:linear-gradient(160deg, rgba(255,255,255,.16), rgba(255,255,255,.03)); backdrop-filter:blur(8px); }}
.bcard i {{ font-style:normal; font-family:"Archivo"; font-weight:700; font-size:46px; letter-spacing:.28em; color:#fff; }}
.bcard u {{ text-decoration:none; font-family:"Archivo"; font-weight:700; font-size:42px; letter-spacing:.08em; color:rgba(255,255,255,.85); }}
.bcard b {{ font-family:"InterV"; font-weight:900; font-size:150px; line-height:.95; letter-spacing:-.04em; color:{RED};
  text-shadow:0 4px 0 #b32c22, 0 8px 0 #8a2018, 0 12px 0 #63150f, 0 30px 50px rgba(0,0,0,.6), 0 0 90px rgba(255,75,62,.5); }}
.bcard em {{ font-style:normal; margin-top:14px; font-family:"InterV"; font-weight:900; font-size:40px; color:#fff; background:{RED}; padding:14px 26px; border-radius:40px; box-shadow:0 0 40px rgba(255,75,62,.55); }}
.bcard.g {{ border:3px solid rgba(43,214,123,.85); box-shadow:0 30px 80px rgba(0,0,0,.5), 0 0 90px rgba(43,214,123,.3), inset 0 1px 0 rgba(255,255,255,.35); }}
.bcard.g i {{ color:{GRN}; }}
.bcard.r {{ border:3px solid rgba(255,75,62,.85); box-shadow:0 30px 80px rgba(0,0,0,.5), 0 0 90px rgba(255,75,62,.3), inset 0 1px 0 rgba(255,255,255,.25); }}
.bcard.r i {{ color:#ff9b93; }}
.vs {{ font-family:"InterV"; font-weight:900; font-size:64px; color:#fff; width:120px; height:120px; border-radius:50%; display:flex; align-items:center; justify-content:center;
  background:linear-gradient(180deg,#1b2a55,#0a1330); border:3px solid rgba(255,255,255,.4); box-shadow:0 0 50px rgba(47,123,255,.5); margin:-50px 0; z-index:2; }}
#c148 .gradb {{ background:linear-gradient(to top, rgba(0,0,0,.85) 0%, rgba(0,0,0,.35) 12%, rgba(0,0,0,0) 22%); }}
#c148 .kbx {{ bottom:40px; flex-direction:row; flex-wrap:wrap; justify-content:center; gap:14px; }} #c148 .chip.big {{ font-size:38px; padding:14px 26px; }}
.swp {{ position:absolute; left:40px; right:40px; height:200px; overflow:hidden; z-index:3; }}
.swp b {{ position:absolute; left:0; right:0; top:0; text-align:center; font-family:"InterV"; font-weight:900; font-size:150px; letter-spacing:-.04em; color:#fff;
  text-shadow:0 0 60px rgba(47,123,255,.5); }}
"""
js.append(f'tl.fromTo(".grao", {{backgroundPosition:"0px 0px"}}, {{backgroundPosition:"-4320px 0px", duration:0.16, ease:"steps(4)", repeat:{int(FIM / 0.16)}}}, 0);')
doc = (f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="UTF-8" />\n<meta name="viewport" content="width=1080, height=1920" />\n'
       f'<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>\n'
       + ('<script>window.__hf=window.__hf||{};window.__hf.buildReady=window.__hf.buildReady||{};window.__hf.buildReady.anatomia=new Promise(function(resolve){window.__anatomiaReady=resolve;});</script>\n' if ANAT else '')
       + f'<style>{CSS}</style>\n</head>\n<body>\n'
       f'<div id="root" data-composition-id="main" data-start="0" data-duration="{FIM}" data-width="1080" data-height="1920" data-fps="{FPS}">\n'
       + "\n".join(clips) + '\n<div class="vinheta"></div><div class="grao"></div>\n</div>\n<script>\nwindow.__timelines = window.__timelines || {};\n'
       'const tl = gsap.timeline({ paused: true });\n' + "\n".join(js) + '\nwindow.__timelines["main"] = tl;\n</script>\n' + ('<script type="module" src="assets/anatomia3d.mjs"></script>\n' if ANAT else '') + '</body>\n</html>\n')
open(os.path.join(H, "index.html"), "w").write(doc)

# relatório: cobertura por tipo e footage repetida
fontes = re.findall(r'src="(assets/(?:ia\d*|org)/[^"]+)"', "".join(c for c in clips if 'class="st' in c))
rep = sorted({f for f in fontes if fontes.count(f) > 1})
NCAP = sum(1 for c in clips if 'class="clip cap"' in c)
tot = {}
for a, b, t in COBRE: tot[t] = tot.get(t, 0) + b - a
print(f"FIM {FIM:.2f}s · {len(CENAS)} momentos · {NCAP} legendas · {len(sfx)} SFX · luzes {len(LUZES)}")
print("tempo por tipo:", {k: round(v) for k, v in tot.items()}, f"· doutora sozinha ≈ {round(FIM - sum(tot.values()))}s")
print("footage repetida:", rep or "nenhuma")
oc = sorted((a, b) for a, b, _ in COBRE); ant = 0.0
for a, b in oc + [(FIM, FIM)]:
    if a - ant > 8: print(f"doutora sozinha {ant:.1f}-{a:.1f} ({a-ant:.0f}s):", " ".join(x["w"] for x in W if ant <= x["s"] < a))
    ant = max(ant, b)
