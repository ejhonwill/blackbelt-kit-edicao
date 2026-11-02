#!/usr/bin/env python3
"""Upsell #2 CardioFlush → NightRenew (346_PG). 9:16 1080×1920, 25 fps. Gera hyperframes/up2-nightrenew/index.html.
O roteiro visual vem do storyboard do IA Creator (_SAMURAI/storyboard.md), lido pelo motor; padrão da skill upsell-premium-916.
Editar AQUI ou no storyboard, nunca o index.html."""
import json, os, re, html, subprocess

J = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(J, "hyperframes", "up2-nightrenew")
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
TARJA = {"DP_linda1": "Linda, 67 · Ohio", "DP_linda2": "Linda, 67 · Ohio", "DP_inicio": "Walter, 71 · Michigan", "DP_idade": "Gary, 66 · Texas", "DP_ansiedade": "Denise, 63 · Georgia"}
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
    W[:] = [x for x in W if not (d["ini"] - 0.05 <= x["s"] < d["fim"] - 0.15)] + novas
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
SB = os.path.join(os.path.dirname(J), "..", "_SAMURAI", "storyboard.md")
LINHAS = []
for l in open(SB):
    if re.match(r"\| *\d+ *\|", l):
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        LINHAS.append(dict(n=int(c[0]), frases=c[2], tipo=c[3], visual=c[4], asset=c[5], texto=c[8]))
def aspas(s): return re.findall(r"“([^”]+)”", s)
CTA_TXT = "YES, I WANT TO COMPLETE MY TREATMENT"
SETA = ('<svg class="seta" viewBox="0 0 120 120"><circle cx="60" cy="60" r="54" fill="#FBD643"/>'
        '<path d="M60 30v52M38 62l22 22 22-22" fill="none" stroke="#0b1630" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg>')
IMG = {"cardioflush_oficial": "cardioflush.png", "nr_mockup": "nr_frasco.png", "selo_garantia_1year": "selo_garantia_1year.png",
       "cardioflush_edição-1": "cf_kit1.png", "cardioflush_edição-2": "cf_kit2.png", "cardioflush_edição-3": "cf_kit3.png"}
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
POS_TXT = ["deep sleep", "repairs", "repaired", "repairing", "repair", "dipping", "dips", "dip", "protected", "protection", "protects", "rested",
           "energy", "together", "every penny back", "no questions", "no hassle", "keep the bottles", "sleeping through", "still left", "refund",
           "cleanup", "cleans", "clean", "healthy", "calm", "refreshed", "120/80", "available"]
NEG_TXT = ["heart attacks", "heart attack", "strokes", "stroke", "non-dippers", "non-dipper", "non-dipping", "floating", "too late", "runs out",
           "run out", "risk", "danger", "dangerous", "damage", "pounding", "hardens", "double charge", "disappears"]
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
    if re.search(r"✕|RISK|DOUBLE|NOT |NO MORE|LOST|LATE|RUNS OUT|FLOATING|STROKE|ATTACK", txt, re.I): return "red"
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
    return s.replace("class=red", 'class="red"').replace("class=yel", 'class="yel"').strip(" ·")

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
    m = re.match(r"^(?:número\s+)?([−~≈+]?[$]?[\d][\d,.:–-]*\s?(?:%|¢|PM|AM|/80)?)(?:\s+(.*))?$", it)
    if m and len(m.group(1)) <= 9 and not re.search(r"\d", m.group(2) or ""):
        num, resto = m.group(1).strip(), limpa(m.group(2) or "")
        bate(f"#{i}", t)
        tam = 330 if len(num) <= 3 else (250 if len(num) <= 5 else 190)
        cor = tom(resto) or "yel"
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
        topo = f'<div class="prods" id="{i}">' + "".join(f'<img src="assets/img/{x}">' for x in imgs) + '</div>'
    return topo + "".join(partes)

def cena_F(L, tipo):
    @cena(f"c{L['n']:03d}", tipo, L["ini"], L["fim"])
    def _(a, b):
        txt = L["texto"]; bg = novo(L["asset"]); imgs = imgs_do_asset(L["asset"])
        if L["n"] in ESPECIAIS: return ESPECIAIS[L["n"]](a, b)
        if txt.lower().startswith("bolhas:"):
            return mensagem_html(a, b, [limpa(x) for x in txt.split(":", 1)[1].split(" / ") if limpa(x)])
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

def mensagem_html(a, b, bolhas):
    i = nid("m"); entra3d(f"#{i}", a + 0.02)
    hs = ""
    for k, tx in enumerate(bolhas):
        j = nid("b"); t = quando(tx, a, b, k, len(bolhas))
        em(f"#{j}", t - 0.1, "{y:40, scale:.9, opacity:0, filter:'blur(10px)'}", "{y:0, scale:1, opacity:1, filter:'blur(0px)'}", 0.4, "back.out(1.8)")
        S(t - 0.1, "k_pop", 0.06, 0.74); hs += f'<div class="bolha" id="{j}">{html.escape(tx.strip("…"))}</div>'
    return (f'<div class="fone msg" id="{i}"><div class="scr"><div class="mh"><u>L</u><b>Linda, 67 · Ohio</b><i>New message · Cardio Flush patient</i></div>'
            + hs + '</div></div>')

def pedido_html(a, b, estado_txt):
    i = nid("f"); entra3d(f"#{i}", a + 0.02)
    s = [nid("o") for _ in range(3)]
    for k, x in enumerate(s): em(f"#{x}", a + 0.5 + k * 0.3, "{x:-40, opacity:0}", "{x:0, opacity:1}", 0.35)
    return (f'<div class="fone" id="{i}"><div class="scr"><div class="oh">Order #CF-30417</div>'
            '<div class="orow"><img src="assets/img/cardioflush.png" width="90" height="288"><div><b>Cardio Flush</b><i>Cardio support drops</i></div></div>'
            f'<div class="ost" id="{s[0]}"><u class="ok">✓</u>Order confirmed</div><div class="ost" id="{s[1]}"><u class="on">●</u>{estado_txt}</div>'
            f'<div class="ost dim" id="{s[2]}"><u>○</u>Shipped</div></div></div>')
def esp_2(a, b):
    t = ach("could cause a shipping error,", a, b) or a + 3; t2 = ach("charge your card twice.", a, b) or a + 5
    em("#al2", t, "{scale:.6, opacity:0}", "{scale:1, opacity:1}", 0.35, "back.out(2)")
    em("#al2", t + 0.4, "{x:0}", "{x:10, repeat:5, yoyo:true}", 0.05, "none"); entra("#ch2", t2); S(t, "k_impacto", 0.09, 0.3)
    return pedido_html(a, b, "Processing your order…") + '<div class="alerta" id="al2">⚠ DON\'T CLOSE THIS PAGE</div><div class="chip red big" id="ch2" style="position:absolute;left:50%;transform:translateX(-50%);top:1590px;white-space:nowrap">RISK OF A DOUBLE CHARGE</div>'
def esp_171(a, b):
    return pedido_html(a, b, "Being packed right now…")

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
def prods_html(t, imgs, h=430, cls=""):
    i = nid("pd")
    em(f"#{i}", t, "{y:300, rotationY:-50, z:-400, opacity:0, filter:'blur(24px)'}", "{y:0, rotationY:0, z:0, opacity:1, filter:'blur(0px)'}", 0.7)
    return f'<div class="prods {cls}" id="{i}" style="height:{h}px">' + "".join(f'<img src="assets/img/{x}">' for x in imgs) + '</div>'
def duas(a, b, t2, h1, h2):  # duas telas na mesma cena: a 1ª sai e a 2ª entra em t2
    i1 = nid("s")
    em(f"#{i1}", t2 - 0.25, "{opacity:1, y:0}", "{opacity:0, y:-60, filter:'blur(12px)'}", 0.3, "power2.in")
    return f'<div class="fs" id="{i1}">{h1}</div><div class="fs">{h2}</div>'
def esp_136(a, b):  # #2 do Frame.io: aparecer 3 potes do NightRenew (antes: 3 CardioFlush × 1 NightRenew)
    t1 = ach("Three for the day,", a, b) or a + 2.5; t2 = ach("three for the night.", a, b) or t1 + 1.2; t3 = ach("They start together,", a, b) or t2 + 1.5
    l1, l2, l3 = nid("q"), nid("q"), nid("q")
    entra(f"#{l1}", t1); entra(f"#{l2}", t2); bate(f"#{l3}", t3)
    S(a + 0.05, "k_pop", 0.06, 0.74); S(t2, "k_pop", 0.06, 0.74)
    return ('<div class="fs">'
            '<div class="par">'
            f'<div class="lado">{prods_html(a + 0.05, ["cf_kit3.png"], 470)}<div class="cond mid dia" id="{l1}">3 FOR THE DAY</div></div>'
            f'<div class="lado">{prods_html(t2 - 0.1, ["nr_kit3.png"], 470)}<div class="cond mid noite" id="{l2}">3 FOR THE NIGHT</div></div>'
            '</div>'
            f'<div class="disp big" id="{l3}">START &amp; FINISH <span class="grn">TOGETHER</span></div></div>')
def esp_146(a, b):  # preço de prateleira (preço cheio = vermelho, ainda sem risco)
    t2 = ach("The 3 bottles for the", a, b) or a + (b - a) * 0.55; t300 = ach("almost $300.", a, b) or t2 + 1.5
    t98 = ach("would cost $98.", a, b); t98 = (t98 + 0.6) if t98 else a + 1.2
    tx = ach("14 natural extracts,", a, b) or t98 + 1.2
    k1 = nid("q"); entra(f"#{k1}", a + 0.3); c1 = nid("q"); entra(f"#{c1}", tx)
    h1 = (prods_html(a + 0.05, ["nr_frasco.png"], 520) + f'<div class="kick" id="{k1}">SHELF PRICE</div>' + pcheio(t98, "$98", tam=230)
          + f'<div class="cond mid" id="{c1}">14 NATURAL EXTRACTS</div>')
    k2 = nid("q"); entra(f"#{k2}", t2 + 0.1)
    h2 = (prods_html(t2, ["nr_kit3.png"], 470) + f'<div class="kick" id="{k2}">3 BOTTLES · FULL TREATMENT</div>'
          + pcheio(t300, "$300", rot="ALMOST", tam=230))
    return duas(a, b, t2, h1, h2)
def esp_157(a, b):  # escada de preços cheios riscados (com $) → oferta verde
    em(f"#c157i .fbgv", a, "{opacity:0, scale:1.2}", "{opacity:1, scale:1}", 0.6)
    out = fundo("assets/ia3/nr_kit3.mp4", a, b, "fbgv") + '<div class="fgrad"></div><div class="fgrad2"></div>'
    ts = [ach("pay $294.", a, b) or a + 0.8, ach("Not $150.", a, b) or a + 2.6, ach("even $100.", a, b) or a + 4.2]
    ts = [ts[0] + 0.25, ts[1] + 0.2, ts[2] + 0.3]
    t2 = ach("Today, you get all", a, b) or a + (b - a) * 0.55; t48 = ach("just $48.", a, b) or t2 + 2.2
    h1 = '<div class="escada">' + "".join(pcheio(t - 0.35, p, risca=t + 0.25, tam=170, rot="NOT") for t, p in zip(ts, ["$294", "$150", "$100"])) + '</div>'
    k = nid("q"); entra(f"#{k}", t2 + 0.05)
    h2 = (f'<div class="kick" id="{k}">TODAY · ALL 3 BOTTLES OF NIGHTRENEW</div>' + poferta(t48 - 0.1, "$48", "TOTAL", 330)
          + setas_verdes(t48 + 0.4))
    return out + duas(a, b, t2, h1, h2)
def setas_verdes(t):
    i = nid("sv"); entra(f"#{i}", t, "{y:-40, opacity:0}", "{y:0, opacity:1}", 0.4, "back.out(2)")
    js.append(f'tl.to("#{i} svg", {{y:14, duration:0.4, ease:"sine.inOut", yoyo:true, repeat:5, stagger:0.12}}, {r(t + 0.45)});')
    seta = '<svg viewBox="0 0 100 100"><path d="M50 12v62M24 50l26 26 26-26" fill="none" stroke="#2BD67B" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    return f'<div class="setasv" id="{i}">{seta * 3}</div>'
def esp_158(a, b):  # #1 remover a palavra "riscado" · #4 moeda: 53¢ → $0.53
    t16 = ach("That’s $16 a bottle.", a, b) or a; t98 = ach("normally cost $98.", a, b); t98 = (t98 + 0.5) if t98 else a + 3
    t2 = ach("Break it down by night,", a, b) or a + (b - a) * 0.5; t53 = ach("about 53 cents.", a, b); t53 = (t53 + 0.2) if t53 else t2 + 1.5
    tst = ach("Less than a postage", a, b) or t53 + 1.2
    h1 = (poferta(t16 + 0.1, "$16", "PER BOTTLE", 330, "ding") + pcheio(t98 - 0.3, "$98", risca=t98 + 0.25, tam=150, rot="INSTEAD OF"))
    c = nid("q"); entra(f"#{c}", tst)
    h2 = poferta(t53, "$0.53", "PER NIGHT", 300, "ding") + f'<div class="disp big" id="{c}">LESS THAN A<br>POSTAGE STAMP</div>'
    return duas(a, b, t2, h1, h2)
def cta_html(t, b):
    i = nid("ct")
    em(f"#{i}", t, "{scale:.4, opacity:0, filter:'blur(20px)'}", "{scale:1, opacity:1, filter:'blur(0px)'}", 0.45, "back.out(2)")
    js.append(f'tl.to("#{i} .bt", {{scale:1.04, duration:0.45, ease:"sine.inOut", yoyo:true, repeat:{max(1, int((b - t) / 0.45) - 2)}}}, {r(t + 0.5)});')
    js.append(f'tl.to("#{i} .seta", {{y:16, duration:0.4, ease:"sine.inOut", yoyo:true, repeat:{max(1, int((b - t) / 0.4) - 2)}}}, {r(t + 0.5)});')
    S(t, "k_pop", 0.09, 0.74)
    return f'<div class="cta-g rel" id="{i}"><div class="bt">{CTA_TXT}</div>{SETA}</div>'
def oferta_linha(t):  # 3 frascos + "3 BOTTLES · $48" verde: a oferta fica visível no pitch do botão (#5 do Frame.io)
    i = nid("q"); entra(f"#{i}", t + 0.2)
    return prods_html(t, ["nr_kit3.png"], 400) + f'<div class="ofl" id="{i}">3 BOTTLES · <b>$48</b> <s>$294</s></div>'
def esp_160(a, b):
    t2 = ach("Click the button below that", a, b) or a + (b - a) * 0.5
    i = nid("q"); entra(f"#{i}", a + 0.15, "{scale:.6, opacity:0}", "{scale:1, opacity:1}", 0.35, "back.out(2)"); S(a + 0.15, "ding", 0.05, 1.0)
    h1 = (prods_html(a + 0.05, ["nr_kit3.png"], 420) + f'<div class="chip big grn" id="{i}">✓ BOTTLES STILL LEFT FOR YOU</div>')
    return duas(a, b, t2, h1, oferta_linha(t2 - 0.05) + cta_html(t2 + 0.3, b))
def esp_173(a, b):  # #6 "dá para deixar mais premium": balança de vidro verde × vermelho com câmera 3D
    tn = ach("Not clicking costs every", a, b) or a + 2.5; tf = ach("floating in your arteries.", a, b) or tn + 3
    t2 = ach("Click the button below right now:", a, b) or a + (b - a) * 0.62
    g, rr, x = nid("cg"), nid("cr"), nid("cx")
    entra3d(f"#{g}", a + 0.05); entra3d(f"#{rr}", tn - 0.05); S(a + 0.05, "cash", 0.1); S(tn, "k_impacto", 0.09, 0.3)
    em(f"#{rr}", tf, "{x:0}", "{x:12, repeat:7, yoyo:true}", 0.05, "none")
    em(f"#{x}", tf, "{opacity:0, scale:.6}", "{opacity:1, scale:1}", 0.35, "back.out(2)")
    h1 = ('<div class="bal">'
          f'<div class="bcard g" id="{g}"><i>CLICKING COSTS</i><div class="num grn" style="font-size:250px">$48</div><u>ONCE · 3 BOTTLES · 90 NIGHTS OF REPAIR</u></div>'
          '<div class="vs">VS</div>'
          f'<div class="bcard r" id="{rr}"><i>NOT CLICKING COSTS</i><b>EVERY NIGHT</b><u>FOR THE NEXT 3 MONTHS</u>'
          f'<em id="{x}">✕ CEMENT FLOATING IN YOUR ARTERIES</em></div></div>')
    return duas(a, b, t2, h1, oferta_linha(t2 - 0.05) + cta_html(t2 + 0.3, b))
ESPECIAIS = {2: esp_2, 171: esp_171, 136: esp_136, 146: esp_146, 157: esp_157, 158: esp_158, 160: esp_160, 173: esp_173}

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
            bate(f"#{i}", t); out += f'<div class="tgrad"></div><div class="disp big c tback" id="{i}" style="top:170px">{colore(tx)}</div>'
        m = re.search(r"bate:\s*([^·]+?)(?=\s+·|$)", txt)
        if m:
            i = nid("l"); bate(f"#{i}", a + 0.15); out += f'<div class="tgrad"></div><div class="disp big c tback" id="{i}" style="top:170px">{colore(limpa(m.group(1)))}</div>'
        for m in re.finditer(r"chip_em '([^']+)':\s*([^→·(]+)", txt): chips.append((ach(m.group(1), a, b) or a + 0.3, limpa(m.group(2))))
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

def DEP_JANELAS(): return [(d["ini"] - 0.15, d["ini"] - 0.15 + dur(os.path.join(H, "assets", "depo", d["id"] + ".mp4"))) for d in DEPO]
for d in DEPO:
    ini = d["ini"] - 0.15; du = dur(os.path.join(H, "assets", "depo", d["id"] + ".mp4"))
    @cena("dp_" + d["id"].lower(), "B", ini, ini + du - 0.04, d["fim"] - d["ini"] > 5, 60)
    def _(a, b, d=d):
        TRK[0] += 1; i = "dp" + d["id"].lower()
        em(f"#{i}t", a + 0.25, "{x:-300, opacity:0, filter:'blur(14px)'}", "{x:0, opacity:1, filter:'blur(0px)'}", 0.45)
        return (f'<video id="{i}v" class="clip fill" src="assets/depo/{d["id"]}.mp4" playsinline data-start="{q(a)}" data-duration="{r(b - a)}" data-track-index="{TRK[0]}" data-has-audio="true" data-volume="1"></video>'
                f'<div class="tarja" id="{i}t"><b>{TARJA[d["id"]].split(" · ")[0]}</b><span>{TARJA[d["id"]].split(" · ")[1]} · Cardio Flush patient</span></div>')
# frases de entrada/saída e montagem dos momentos
for k, L in enumerate(LINHAS):
    fr = aspas(L["frases"]); L["ini"] = fr[0]; L["fim"] = fr[1] if len(fr) > 1 and not fr[1].startswith("(") else FIM
for k, L in enumerate(LINHAS):
    if L["fim"] is None: L["fim"] = ("+", 6.0)
    tp = L["tipo"]
    if tp in ("D", "D2"): continue
    try:
        _cursor[0] = 0.0; t_ini = achar(L["ini"])
    except SystemExit:
        t_ini = None
    if t_ini is not None and any(a_ - 0.1 <= t_ini < b_ - 0.3 for a_, b_ in DEP_JANELAS()): continue
    if L is LINHAS[-1] and CTA_TXT in L["texto"].upper(): continue  # o fim já tem o CTA fixo; não duplicar o botão
    if tp in ("F", "M"): cena_F(L, "M" if tp == "M" else "F")
    elif tp == "T": cena_T(L)
    elif tp in ("B", "R"):
        src = f"assets/ia3/{novo(L['asset'])}.mp4"
        (B if tp == "B" else R)(f"c{L['n']:03d}", L["ini"], L["fim"], src, extra=extras_broll(L))
# vídeo do paciente (D2): tarja + chip do 120/80
PAC = next(s for s in SEG if s["id"] == "P01")
CTA_INI = achar("So click the button below,", 0)
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
    cls = {"F": "st f", "M": "st f meio", "T": "st t", "R": "st br", "B": "st br"}[tipo]
    clips.append(f'<div class="{cls}" id="{cid}"><div class="in" id="{cid}i">{h}</div></div>')
    js.append(f'tl.set("#{cid}", {{opacity:0}}, 0); tl.set("#{cid}", {{opacity:1}}, {a}); tl.set("#{cid}", {{opacity:0}}, {b});')
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
ALPHA = "".join(recorte(max(0.0, q(a - 0.04)), q(b - 0.04), "alv") for _, t, a, b, _, _ in CENAS if False)

# doutora + recorte (mesmo punch-in nos dois)
clips.insert(0, '<div id="cam"><div id="cam-in">' + "".join(
    f'<video id="v{s["id"]}" class="clip" src="assets/avatar/{s["id"]}.mp4" playsinline data-start="{q(s["s"])}" data-duration="{r(s["d"])}" data-track-index="0" data-has-audio="true" data-volume="1"></video>'
    for s in SEG) + '</div></div>')
clips.append(f'<div id="al"><div id="al-in">{ALPHA}</div></div>')
frases = [W[0]["s"]] + [W[i]["s"] for i in range(1, len(W)) if re.search(r"[.?!…]\"?$", W[i - 1]["w"])]
esc, ult = 1.0, -9
pontos = sorted(set([q(x) for x in frases] + [b for a, b, _ in COBRE] + [a for a, b, t in COBRE if t == "T"]))
for t in pontos:
    if coberto(t + 0.05, "BRF") or t - ult < 2.2: continue
    esc = 1.12 if esc == 1.0 else 1.0
    js.append(f'tl.set("#cam-in, #al-in", {{scale:{esc}}}, {q(t - 0.02)});'); ult = t
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
    if n == "cardio" and k_ + 1 < len(W) and norm(W[k_ + 1]["w"]).startswith("flush"): n = "cardioflush"
    if n not in ("cardioflush", "nightrenew"): continue
    t = q(x["s"] - 0.15)
    if coberto(t + 1.0, "TFBR") or coberto(t + 0.1, "TFBR") or t - ult_p < 6 or PAC["s"] - 0.5 < t < PAC["s"] + PAC["d"]: continue
    ult_p = t; k = len(clips)
    img, nome, w_ = ("cardioflush.png", "Cardio Flush", 200) if n == "cardioflush" else ("nr_frasco.png", "NightRenew", 300)
    clips.append(f'<div id="pr{k}" class="clip prod" data-start="{t}" data-duration="2.4" data-track-index="9"><i class="pglow"></i><img src="assets/img/{img}" style="width:{w_}px"><b>{nome}</b></div>')
    js.append(f'tl.fromTo("#pr{k}", {{x:420, rotationY:-55, opacity:0, filter:"blur(22px)"}}, {{x:0, rotationY:-12, opacity:1, filter:"blur(0px)", duration:0.55, ease:"expo.out", immediateRender:false}}, {t});')
    js.append(f'tl.to("#pr{k}", {{rotationY:6, y:-14, duration:1.5, ease:"sine.inOut"}}, {r(t + 0.55)});')
    js.append(f'tl.to("#pr{k}", {{x:420, opacity:0, filter:"blur(22px)", duration:0.35, ease:"power3.in"}}, {r(t + 2.05)});')
    S(t, "k_swish", 0.05, 0.57)
# vídeo do paciente: tarja "vídeo de paciente" + chip do 120/80 na frase
clips.append(f'<div id="pac" class="clip pactag" data-start="{q(PAC["s"])}" data-duration="{r(PAC["d"])}" data-track-index="9"><div class="ptag">● VIDEO MESSAGE FROM A PATIENT</div></div>')
js.append(f'tl.fromTo("#pac .ptag", {{y:-120, opacity:0}}, {{y:0, opacity:1, duration:0.45, ease:"back.out(1.8)", immediateRender:false}}, {q(PAC["s"] + 0.2)});')
t120 = achar("120 over 80.", PAC["s"] - 0.1)
clips.append(f'<div id="pac2" class="clip pactag" data-start="{q(t120)}" data-duration="{r(min(4.0, PAC["s"] + PAC["d"] - t120))}" data-track-index="10"><div class="chip big pchip">120/80 ✓</div></div>')
js.append(f'tl.fromTo("#pac2 .pchip", {{scale:.5, opacity:0}}, {{scale:1, opacity:1, duration:0.35, ease:"back.out(2)", immediateRender:false}}, {q(t120)});')
S(t120, "ding", 0.06, 1.0)

# luz nas entradas de b-roll/react
for k, t in enumerate(LUZES):
    clips.append(f'<div class="luz" id="lz{k}"><video id="vlz{k}" class="clip" src="assets/luz/lk{k % 6}.mp4" muted playsinline data-start="{q(max(0, t - 0.2))}" data-duration="0.56" data-track-index="{200 + k % 4}"></video></div>')
    js.append(f'tl.set("#lz{k}", {{opacity:0}}, 0); tl.set("#lz{k}", {{opacity:1}}, {q(max(0, t - 0.2))}); tl.set("#lz{k}", {{opacity:0}}, {q(t + 0.36)});')

YEL, RED, BLU, GRN = "#FFD23F", "#FF4B3E", "#2F7BFF", "#2BD67B"
# legenda pop (doutora sozinha, b-roll e react; nunca sob lettering T/F)
# V3: palavra falada positiva fica verde, negativa vermelha, o resto amarelo
POS1 = {"repair", "repairs", "repaired", "repairing", "dips", "dip", "dipping", "protected", "protection", "protects", "rested", "energy",
        "refreshed", "restful", "healthy", "refund", "guarantee"}
NEG1 = {"stroke", "strokes", "non-dipper", "non-dippers", "non-dipping", "floating", "risk", "danger", "dangerous", "pounding", "hardens", "attack", "attacks"}
POS2 = {("deep", "sleep"), ("sleeping", "through")}
NEG2 = {("heart", "attack"), ("heart", "attacks"), ("too", "late"), ("runs", "out"), ("run", "out")}
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
grupos, g = [], []
for x in W:
    g.append(x)
    if len(g) == 3 or re.search(r"[.,?!…:;—]\"?$", x["w"]): grupos.append(g); g = []
if g: grupos.append(g)
for i, g in enumerate(grupos):
    a = q(g[0]["s"]); b = q(grupos[i + 1][0]["s"]) if i + 1 < len(grupos) else q(g[-1]["ea"] + 0.3)
    b = min(b, q(g[-1]["ea"] + 0.5))  # "ea" = fim da última letra (o "e" do ElevenLabs inclui a pausa da pontuação)
    if any(x0 < b - 0.15 and a + 0.15 < x1 and tp in "TF" for x0, x1, tp in COBRE): continue
    if any(x0 < b - 0.15 and a + 0.15 < x1 for x0, x1 in COMTEXTO): continue
    if b > CTA_INI + 0.2: continue  # sem legenda sob o CTA fixo (padrão aprovado)
    spans = "".join(f'<span id="cw{i}_{k}">{html.escape(x["w"].strip(ASP))}</span> ' for k, x in enumerate(g))
    baixa = ""
    clips.append(f'<div id="cap{i}" class="clip cap{baixa}" data-start="{a}" data-duration="{r(max(0.12, b - a))}" data-track-index="8"><div class="cap-in">{spans}</div></div>')
    js.append(f'tl.fromTo("#cap{i} .cap-in", {{scale:.8, y:20, opacity:0}}, {{scale:1, y:0, opacity:1, duration:0.16, ease:"back.out(2.4)", immediateRender:false}}, {a});')
    for k, x in enumerate(g):
        js.append(f'tl.set("#cw{i}_{k}", {{color:"{COR_W.get(IDX_W[id(x)], YEL)}", scale:1.08}}, {q(x["s"])}); tl.set("#cw{i}_{k}", {{color:"#ffffff", scale:1}}, {q(max(x["ea"] + 0.05, x["s"] + 0.08))});')

# CTA fixa do fim (mesmo desenho do validado)
clips.append(f'<div id="cta" class="clip cta" data-start="{q(CTA_INI)}" data-duration="{r(FIM - CTA_INI)}" data-track-index="9"><div class="cta-g fixo"><div class="bt">{CTA_TXT}</div>{SETA}</div></div>')
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
.fdark {{ position:absolute; inset:0; background:radial-gradient(75% 50% at 50% 42%, rgba(24,52,120,.45) 0%, rgba(8,17,42,.72) 55%, rgba(3,6,15,.92) 100%); }}
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
.kbx {{ position:absolute; left:70px; right:70px; bottom:340px; z-index:3; text-align:center; }}
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
.ost u {{ text-decoration:none; width:56px; height:56px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:30px; background:#dde3ee; color:#778; }}
.ost u.ok {{ background:#21c26b; color:#fff; }} .ost u.on {{ background:{BLU}; color:#fff; }} .ost.dim {{ opacity:.45; }}
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
.d3.atras {{ top:420px; bottom:-420px; opacity:.95; mix-blend-mode:normal; -webkit-mask-image:radial-gradient(closest-side, #000 55%, transparent 100%); mask-image:radial-gradient(closest-side, #000 55%, transparent 100%); }}
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
.vidro2 {{ width:100%; padding:44px 46px 10px; border-radius:40px; background:linear-gradient(160deg, rgba(255,255,255,.14), rgba(255,255,255,.04));
  border:2px solid rgba(255,255,255,.25); box-shadow:0 30px 80px rgba(0,0,0,.45), inset 0 1px 0 rgba(255,255,255,.3); text-align:left; }}
.vidro2 .li span {{ font-size:68px; line-height:1.05; }} .vidro2 .li {{ margin-bottom:44px; }}
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
.cap-in span {{ display:inline-block; }}
.cta {{ position:absolute; inset:0; z-index:8; pointer-events:none; }}
.luz {{ position:absolute; inset:0; z-index:7; pointer-events:none; mix-blend-mode:screen; opacity:0; }}
.luz video {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; opacity:.7; }}
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
       f'<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>\n<style>{CSS}</style>\n</head>\n<body>\n'
       f'<div id="root" data-composition-id="main" data-start="0" data-duration="{FIM}" data-width="1080" data-height="1920" data-fps="{FPS}">\n'
       + "\n".join(clips) + '\n<div class="vinheta"></div><div class="grao"></div>\n</div>\n<script>\nwindow.__timelines = window.__timelines || {};\n'
       'const tl = gsap.timeline({ paused: true });\n' + "\n".join(js) + '\nwindow.__timelines["main"] = tl;\n</script>\n</body>\n</html>\n')
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
