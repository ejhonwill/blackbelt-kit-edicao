#!/usr/bin/env python3
"""Upsell #2 EreVanton → Procarven (345_BM) — revisão 1 (Jhon 28/10): a DOUTORA conduz o vídeo.
9:16 1080×1920, 25 fps. Gera hyperframes/up2-procarven/index.html. Editar AQUI, nunca o index.html.
Tipos de momento:
  D = doutora sozinha (punch-in + legenda pop)
  T = lettering ATRÁS da doutora (fundo escurece, ela recortada por cima: assets/doutora_alpha)
  F = doutora desfocada/escurecida atrás de card, celular, produto ou número (padrão MemoPryl/CardioFlush)
  R = react: b-roll em tela cheia + doutora recortada no canto comentando
  B = b-roll curto em tela cheia
Transições: luz (light leak, screen) + continuidade de zoom; movimento 3D com motion blur.
Regra do Jhon: nenhuma footage repete na timeline."""
import json, os, re, html, subprocess

J = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(J, "hyperframes", "up2-procarven")
FPS = 25
def r(x): return round(x + 1e-9, 3)
def q(x): return round(round(x * FPS) / FPS, 3)
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)

# ---------------------------------------------------------------- fala (alinhamento ElevenLabs)
BL = json.load(open(os.path.join(J, "ia", "voz", "blocos.json")))
SEG, W, t0 = [], [], 0.0
for b in BL:
    d = dur(os.path.join(H, "assets", "doutora", b["id"] + ".mp4"))
    a = json.load(open(os.path.join(J, "ia", "voz", "blocos", b["id"] + "_alin.json")))
    cur, cs = "", None
    for ch, s, e in zip(a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]):
        if ch.isspace():
            if cur: W.append({"w": cur, "s": t0 + cs, "e": t0 + pe}); cur = ""
        else:
            if not cur: cs = s
            cur += ch; pe = e
    if cur: W.append({"w": cur, "s": t0 + cs, "e": t0 + pe})
    SEG.append({"id": b["id"], "s": t0, "d": d}); t0 += d
FIM = q(t0)
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
TETO = {"B": 6.0, "R": 8.0, "T": 6.5}
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

# ================================================================ roteiro visual (revisão 2, 28/10: Jhon + IA Creator)
# S01 — abre na doutora; o rastreio entra como card na frente dela desfocada
@cena("c01", "F", "Do not close this video", "Before finalizing everything")
def _(a, b):
    entra3d("#c01f", a + 0.02)
    for k, t in enumerate([a + 0.5, a + 0.8, a + 1.1]): em(f"#c01s{k}", t, "{x:-40, opacity:0}", "{x:0, opacity:1}", 0.35)
    em("#c01al", achar("a delivery error"), "{scale:.6, opacity:0}", "{scale:1, opacity:1}", 0.35, "back.out(2)")
    em("#c01al", achar("a delivery error") + 0.4, "{x:0}", "{x:10, repeat:5, yoyo:true}", 0.05, "none")
    entra("#c01dc", achar("a duplicate charge"))
    S(achar("a delivery error"), "k_impacto", 0.09, 0.3)
    return ('<div class="fone" id="c01f"><div class="scr"><div class="oh">Order #EV-48213</div>'
            '<div class="orow"><img src="assets/img/erevanton.png" width="120" height="200"><div><b>EreVanton</b><i>Accelerated protocol</i></div></div>'
            '<div class="ost" id="c01s0"><u class="ok">✓</u>Order confirmed</div><div class="ost" id="c01s1"><u class="on">●</u>Packing your box…</div>'
            '<div class="ost dim" id="c01s2"><u>○</u>Shipped</div></div></div>'
            '<div class="alerta" id="c01al">⚠ DON\'T CLOSE THIS VIDEO</div><div class="chip red" id="c01dc">risk of a duplicate charge</div>')

TB("c02", "become the man who dominates", "or whether you will continue", "assets/ia3/casal_domina.mp4", "ONCE AND FOR ALL", 'DOMINATE<br><span class="yel">IN BED</span>', cls="huge", modo="bate")
B("c03", "failing at the most important moment.", "She gets closer,", "assets/ia/ia_homem_beira_cama.mp4",
  extra=letra_em("c03t", "failing at the most important moment.", 'FAILING AT<br><span class="red">THE WORST MOMENT</span>', "glowr", "entra"))
R("c04", "She gets closer,", "There's that second of silence", "assets/ia/p1_beijo.mp4")
B("c05", "There's that second of silence", "She says it's okay.", "assets/ia/ia_casal_cama.mp4", luz=False)
B("c06", "She says it's okay.", "Then comes the same old excuse.", "assets/ia/p2_tudobem.mp4", luz=False)

@cena("c07", "R", "Then comes the same old excuse.", "And the next time,", True)
def _(a, b):
    ts = [achar("Tiredness,"), achar("stress,"), achar("it was just today.")]
    for t in ts: S(t, "k_pop", 0.05, 0.74)
    t2 = achar("It happened again.")
    em("#c07s", t2 - 0.1, "{opacity:1}", "{opacity:0}", 0.15, "none")
    em("#c07i .fill", t2, "{filter:'saturate(1) brightness(1)'}", "{filter:'saturate(0.15) brightness(0.55)'}", 0.3, "power2.out")
    bate("#c07t", t2)
    return (media("assets/ia/p4_cansaco.mp4", a, b) + '<div class="gradt"></div><div class="swp" id="c07s" style="top:170px">' + troca("c07w", ts, ["TIREDNESS", "STRESS", "JUST TODAY"]) + '</div>'
            '<div class="disp huge c tback red glowr" id="c07t" style="top:640px">IT HAPPENED<br>AGAIN.</div>')
B("c09", "you already go to bed feeling afraid.", "That's exactly why you bought", "assets/ia/p3_teto.mp4")

@cena("c10", "F", "you chose the accelerated protocol.", "By tripling the dose,")
def _(a, b):
    for k in range(3):
        em(f"#c10f{k}", a + 0.05 + k * 0.12, "{y:420, rotationY:70, z:-400, opacity:0, filter:'blur(26px)'}", "{y:0, rotationY:0, z:0, opacity:1, filter:'blur(0px)'}", 0.7)
    entra("#c10t", a + 0.1)
    S(a + 0.05, "k_swish", 0.06, 0.57)
    return ('<i class="halo"></i>' + "".join(f'<img class="fan f{k}" id="c10f{k}" src="assets/img/erevanton.png" width="330" height="548">' for k in range(3)) +
            '<div class="kick c" style="top:330px">YOU CHOSE THE</div><div class="disp big c tback" id="c10t" style="top:390px">ACCELERATED<br><span class="yel">PROTOCOL</span></div>'
            '<div class="chip big c2" style="top:1560px">3× THE DOSE</div>')

# S03 — triplo de velocidade no sangue, semanas × meses, não é genética nem testosterona
@cena("c11", "F", "By tripling the dose,", "That's excellent,")
def _(a, b):
    bate("#c11n", achar("tripled the speed"))
    js.append(f'(function(){{var o={{v:1}},el=document.querySelector("#c11n b");tl.fromTo(o,{{v:1}},{{v:3,duration:0.6,ease:"power2.out",immediateRender:false,'
              f'onUpdate:function(){{if(el)el.textContent=Math.round(o.v);}}}},{r(achar("tripled the speed"))});}})();')
    entra("#c11t", achar("your blood is purified."))
    em("#c11i .fbgv", a, "{opacity:0, scale:1.2}", "{opacity:1, scale:1}", 0.6)
    return (fundo("assets/ia3/3d_sangue_rapido.mp4", a, b, "fbgv") + '<div class="fgrad"></div><div class="kick c" style="top:520px">TRIPLE DOSE</div>'
            '<div class="num c" id="c11n" style="top:600px"><b>1</b><em>×</em></div><div class="chip big c2" id="c11t" style="top:1040px">FASTER BLOOD CLEANSE</div>')

@cena("c12", "F", "in just a few weeks,", "And it's exactly at this point")
def _(a, b):
    tm = achar("only reach after months.")
    entra3d("#c12a", a + 0.02); em("#c12b", tm - 0.2, "{x:400, rotationY:-50, opacity:0, filter:'blur(24px)'}", "{x:0, rotationY:0, opacity:1, filter:'blur(0px)'}", 0.6)
    for el, v0, v1, t, d in [("c12an", 0, 21, a + 0.3, 1.2), ("c12bn", 0, 180, tm, 2.4)]:
        js.append(f'(function(){{var o={{v:{v0}}},el=document.getElementById("{el}");tl.fromTo(o,{{v:{v0}}},{{v:{v1},duration:{d},ease:"power2.out",immediateRender:false,'
                  f'onUpdate:function(){{if(el)el.textContent=Math.round(o.v);}}}},{r(t)});}})();')
    em("#c12aw", a + 1.55, "{scale:.5, opacity:0}", "{scale:1, opacity:1}", 0.35, "back.out(2)")
    em("#c12bw", tm + 2.4, "{scale:.5, opacity:0}", "{scale:1, opacity:1}", 0.35, "back.out(2)")
    S(a + 1.55, "ding", 0.06, 1.0)
    return ('<div class="kick c" style="top:300px">TIME TO REACH THE SAME STAGE</div>'
            '<div class="cal g" id="c12a"><i>YOU</i><b id="c12an">0</b><u>DAYS</u><em id="c12aw">≈ 3 WEEKS</em></div>'
            '<div class="cal r" id="c12b"><i>MOST MEN</i><b id="c12bn">0</b><u>DAYS</u><em id="c12bw">≈ 6 MONTHS</em></div>')

@cena("c13", "F", "It's not your genetics", "It's something far more overlooked:")
def _(a, b):
    tt = achar("your testosterone.")
    em("#c13a", a + 0.02, "{x:-300, opacity:0, filter:'blur(24px)'}", "{x:0, opacity:1, filter:'blur(0px)'}", 0.5)
    em("#c13b", tt - 0.25, "{x:300, opacity:0, filter:'blur(24px)'}", "{x:0, opacity:1, filter:'blur(0px)'}", 0.5)
    for k, t in [("a", tt - 0.3), ("b", tt + 0.6)]:
        em(f"#c13{k} .xs path", t, "{strokeDashoffset:420}", "{strokeDashoffset:0}", 0.28, "power2.in")
        em(f"#c13{k} .fill", t + 0.2, "{filter:'saturate(1) brightness(1)'}", "{filter:'saturate(0) brightness(0.45)'}", 0.4, "power2.out")
        S(t + 0.2, "k_impacto", 0.08, 0.3)
    x = '<svg class="xs" viewBox="0 0 200 200"><path d="M30 30L170 170" /><path d="M170 30L30 170" /></svg>'
    return ('<div class="meia top" id="c13a">' + media("assets/ia3/3d_dna.mp4", a, b) + '<div class="rot">NOT YOUR <b>GENETICS</b></div>' + x + '</div>'
            '<div class="meia bot" id="c13b">' + media("assets/ia3/3d_testosterona.mp4", a, b) + '<div class="rot">NOT YOUR <b>TESTOSTERONE</b></div>' + x + '</div>')

@cena("c14", "T", "It's something far more overlooked:", "You already know that toxins")
def _(a, b):
    em("#c14t", achar("your prostate."), "{scaleX:1.5, opacity:0, filter:'blur(18px)'}", "{scaleX:1, opacity:1, filter:'blur(0px)'}", 0.6)
    em("#c14d", a + 0.1, "{scale:.6, opacity:0, filter:'blur(30px)'}", "{scale:1, opacity:1, filter:'blur(0px)'}", 0.9, "expo.out")
    S(achar("your prostate."), "k_impacto", 0.09, 0.3)
    return ('<div class="d3 atras" id="c14d">' + media("assets/ia/3d_prostata.mp4", a, b) + '</div>'
            '<div class="disp big c tback" id="c14t" style="top:170px">YOUR<br><span class="yel">PROSTATE</span></div>')
B("c14m", "toxins are what clog your smooth muscles", "What we discovered", "assets/ia3/musculo_portas.mp4",
  extra=chip_em("c14mc", "close the doors", "CLOGGED SMOOTH MUSCLES", "red"))

# S04/S05 — acúmulo, esponja, cristais, gotejamento, banheira → ralo anatômico
B("c15", "they don't just circulate", "And the main place", "assets/ia/3d_cristais_sangue.mp4")
TB("c16", "And the main place", "The prostate works like a sponge", "assets/ia3/pelve_acumulo.mp4", "WHERE TOXINS PILE UP", '#1 · THE<br><span class="yel">PROSTATE</span>', "is precisely the prostate.")
R("c17", "The prostate works like a sponge", "Over the years,", "assets/ia/3d_esponja.mp4",
  extra='<div class="ser big c" style="top:200px">like a <span class="yel">sponge</span></div>')
TB("c17b", "this sponge becomes soaked with poison,", "now even more resistant and hardened.", "assets/ia3/esponja_saturando.mp4", "THE SPONGE GETS", 'SOAKED WITH<br><span class="red">POISON</span>', cls="glowr")
TB("c18", "now even more resistant and hardened.", "While EreVanton eliminates", "assets/ia3/cristal_macro.mp4", "EVEN MORE RESISTANT", 'CRYSTALLIZED<br><span class="yel">TOXINS</span>', "I call these crystallized toxins,", "glowy")
B("c18g", "continues releasing these crystallized toxins", "It's like trying to fill a bathtub", "assets/ia3/prostata_gotejando.mp4",
  extra=letra_em("c18gt", "drop by drop.", 'DROP BY<br><span class="yel">DROP</span>'))
B("c19", "It's like trying to fill a bathtub", "with the drain open.", "assets/ia/ia_banheira_ralo.mp4")
B("c19v", "with the drain open.", "And with the accelerated protocol,", "assets/ia3/vaso_ralo.mp4", luz=False,
  extra=chip_em("c19vc", None, "THE OPEN DRAIN = YOUR PROSTATE", "red"))

@cena("c20", "F", "You're emptying the bathtub", "The faster you clean your blood,")
def _(a, b):
    bate("#c20n", achar("three times faster,"))
    entra("#c20s", achar("but the drain remains open."), "{scale:.6, opacity:0}", "{scale:1, opacity:1}", 0.35, "back.out(2)")
    em("#c20i .fbgv", a, "{opacity:0, scale:1.2}", "{opacity:1, scale:1}", 0.6)
    return (fundo("assets/ia3/vaso_ralo_3x.mp4", a, b, "fbgv") + '<div class="fgrad"></div>'
            '<div class="num c" id="c20n" style="top:180px">3<em>×</em></div><div class="chip red big c2" id="c20s" style="top:1500px">…BUT THE DRAIN IS STILL OPEN</div>')

# S06 — sintomas e recaída
@cena("c21", "F", "if you're over 40", "constantly have to get up")
def _(a, b):
    itens = [("over 40", "OVER 40"), ("experience failures in bed,", "FAILURES IN BED"), ("feel desire but your penis", "DESIRE, NO RESPONSE")]
    rows = ""
    for k, (f, t) in enumerate(itens):
        tt = achar(f); em(f"#c21r{k}", tt, "{x:-160, opacity:0, filter:'blur(16px)'}", "{x:0, opacity:1, filter:'blur(0px)'}", 0.45); S(tt, "k_clique", 0.18, 0.08)
        rows += f'<div class="li" id="c21r{k}"><b>✓</b><span>{t}</span></div>'
    entra3d("#c21c", a + 0.02)
    return '<div class="vidro alto" id="c21c" style="top:520px"><div class="kick">DOES THIS SOUND LIKE YOU?</div>' + rows + '</div>'
B("c22", "constantly have to get up", "or notice that your erection", "assets/ia/ia_noite_banheiro.mp4")
B("c23", "your prostate has already accumulated", "Now I want you to imagine", "assets/ia3/prostata_carregada.mp4",
  extra=chip_em("c23c_", "a large amount", "ALREADY LOADED WITH CRYSTALS", "red"))
B("c23c", "Imagine getting everything back.", "Your wife starts looking at you", "assets/org/casal_danca.mp4")
R("c24", "Your wife starts looking at you", "And then, a few months later,", "assets/ia/p7_olhar.mp4")

@cena("c25", "F", "And then, a few months later,", "You already know what that means.")
def _(a, b):
    em("#c25t", achar("you start failing again."), "{scale:3, rotation:-20, opacity:0, filter:'blur(20px)'}", "{scale:1, rotation:-6, opacity:1, filter:'blur(0px)'}", 0.4, "back.out(2)")
    S(achar("you start failing again."), "k_impacto", 0.1, 0.3)
    return '<div class="kick c" style="top:640px">A FEW MONTHS LATER…</div><div class="stamp red" id="c25t" style="top:780px">RELAPSE</div>'
TB("c26", "That's exactly what a clogged prostate does.", "I'm not going to let that happen", "assets/ia3/recaida_vaso.mp4", "", 'A CLOGGED<br><span class="red">PROSTATE</span>',
   extra=lambda a, b: (entra("#c26s", achar("and then takes it all away")) or '') + '<div class="ser mid c" id="c26s" style="top:440px">takes it all away again</div>')

@cena("c26b", "F", "our first idea was to add", "So we did something better.")
def _(a, b):
    entra3d("#c26bc", a + 0.02)
    em("#c26bx", achar("But that would destroy"), "{scale:3, rotation:-20, opacity:0, filter:'blur(20px)'}", "{scale:1, rotation:-8, opacity:1, filter:'blur(0px)'}", 0.4, "back.out(2)")
    S(achar("But that would destroy"), "k_impacto", 0.09, 0.3)
    return ('<img class="hero sm" id="c26bc" src="assets/img/erevanton.png" width="400" height="664" style="top:420px">'
            '<div class="kick c" style="top:110px">ADD IT TO THE FORMULA?</div><div class="stamp red" id="c26bx" style="top:1180px;font-size:96px">✕ SYNERGY LOST</div>')

# S08 — solução: laboratório, revelação (packshot), licopeno
B("c27", "After nine months", "we created Procarven.", "assets/org/lab_maquina.mp4",
  extra='<div class="gradb"></div><div class="kbx"><div class="chip big">9 MONTHS OF R&amp;D</div></div>')
B("c28", "we created Procarven.", "And the secret lies", "assets/ia3/packshot_procarven.mp4", teto=7.5,
  extra=lambda a, b: (bate("#c28t", a + 0.1) or '') + (entra("#c28c", achar("A 100% natural formula,")) or '') +
  '<div class="tgrad"></div><div class="disp big c" id="c28t" style="top:150px">PROCARVEN</div><div class="kbx"><div class="chip big c3s" id="c28c">100% NATURAL · FOR THE PROSTATE</div></div>')
B("c29b", "And the secret lies", "active lycopene", "assets/org/tomate_close.mp4",
  extra='<div class="gradb"></div><div class="kbx"><div class="chip big">ONE UNIQUE INGREDIENT</div></div>')
B("c30", "active lycopene", "Lycopene has a property", "assets/org/tomate_aberto.mp4")
R("c31", "It doesn't simply pass through the prostate.", "However, to reach a concentration", "assets/ia/3d_licopeno.mp4",
  extra='<div class="disp big c" style="top:180px">IT <span class="yel">ACCUMULATES</span></div>')
B("c31b", "However, to reach a concentration", "pounds and pounds of tomatoes", "assets/org/tomate_pe.mp4")
B("c32", "pounds and pounds of tomatoes", "And that's exactly the gap", "assets/org/tomate_caixas.mp4",
  extra=letra_em("c32t", "No man does that.", 'NO MAN<br>DOES THAT.'))
R("c34", "It works like a natural detergent.", "The result?", "assets/ia/3d_cristais_dissolvendo.mp4",
  extra='<div class="ser big c" style="top:200px">a natural <span class="yel">detergent</span></div>')
B("c35", "The result?", "as if you were 20 years old again.", "assets/ia/3d_fluxo_livre.mp4")
M("c36", "as if you were 20 years old again.", "This isn't just about prostate health.",
  lambda a, b: (bate("#c36n", achar("20 years old again.")) or '') + '<div class="kick c" style="top:110px">LIKE YOU\'RE</div><div class="num c yel tback" id="c36n" style="top:170px">20</div><div class="cond mid c" style="top:510px">AGAIN</div>')

BOLHAS = {
    "c37": ("Daniel, 57", ["EreVanton worked perfectly at first, but a few months later, the failures came back. 😞",
                          "I understood the toxins in my prostate were blocking the system. I added Procarven to my treatment.",
                          "The difference was definitive. My firmness returned permanently. No more relapses! 🙌"],
            ["\"EreVanton worked perfectly", "I understood that the toxins", "The difference was definitive,"]),
    "c43": ("Rick, 63", ["I had to get up 4 times a night to urinate, and in bed my erection constantly failed.",
                        "Procarven cleaned my prostate and unlocked the system.",
                        "The nighttime discomfort disappeared. Now my erections are firm and consistent 💪"],
            ["\"I had to get up four times", "Procarven cleaned my prostate", "The nighttime discomfort simply"]),
}
def mensagem(cid, ini, fim_):
    nome, bolhas, gatilhos = BOLHAS[cid]
    @cena(cid, "F", ini, fim_)
    def _(a, b):
        entra3d(f"#{cid}f", a + 0.02)
        for k, g in enumerate(gatilhos):
            t = achar(g); em(f"#{cid}b{k}", t - 0.1, "{y:40, scale:.9, opacity:0, filter:'blur(10px)'}", "{y:0, scale:1, opacity:1, filter:'blur(0px)'}", 0.4, "back.out(1.8)")
            S(t - 0.1, "k_pop", 0.06, 0.74)
        return ('<div class="fone msg" id="' + cid + 'f"><div class="scr"><div class="mh"><u>' + nome[0] + '</u><b>' + html.escape(nome) + '</b><i>New message · EreVanton patient</i></div>' +
                "".join(f'<div class="bolha" id="{cid}b{k}">{html.escape(t)}</div>' for k, t in enumerate(bolhas)) + '</div></div>')
mensagem("c37", "\"EreVanton worked perfectly", "That's exactly what I tell all my patients.")

@cena("c38", "F", "EreVanton and Procarven are the two parts", "One without the other")
def _(a, b):
    em("#c38e", a + 0.05, "{x:-500, rotationY:60, opacity:0, filter:'blur(24px)'}", "{x:0, rotationY:0, opacity:1, filter:'blur(0px)'}", 0.7)
    em("#c38p", achar("and Procarven are"), "{x:500, rotationY:-60, opacity:0, filter:'blur(24px)'}", "{x:0, rotationY:0, opacity:1, filter:'blur(0px)'}", 0.7)
    entra("#c38t", achar("of the same protocol."))
    return ('<i class="halo"></i><img class="dup e" id="c38e" src="assets/img/erevanton.png" width="380" height="631"><img class="dup p" id="c38p" src="assets/img/procarven.png" width="372" height="630">'
            '<div class="kick c" style="top:110px">ONE PROTOCOL · TWO PARTS</div><div class="cond mid c" style="top:1150px">BLOOD <span class="yel">+</span> PROSTATE</div>'
            '<div class="disp big c" id="c38t" style="top:1290px">= <span class="yel">100%</span></div>')
M("c39", "One without the other", "Separately, they help.",
  lambda a, b: (bate("#c39n", achar("only half of the treatment.")) or '') + '<div class="kick c" style="top:110px">ONE WITHOUT THE OTHER</div><div class="num c red tback" id="c39n" style="top:170px">50<em>%</em></div>')
B("c40", "like having a Ferrari", "If you were in my office today,", "assets/org/ferrari_volante.mp4",
  extra='<div class="gradb"></div><div class="kbx"><div class="chip red big">A FERRARI WITHOUT THE KEY</div></div>')

@cena("c41", "F", "That's exactly what I prescribe", "\"I had to get up")
def _(a, b):
    em("#c41c", a + 0.05, "{y:300, rotationX:50, rotation:8, opacity:0, filter:'blur(24px)'}", "{y:0, rotationX:0, rotation:-3, opacity:1, filter:'blur(0px)'}", 0.7)
    return ('<div class="rx" id="c41c"><div class="rxh">DOCTOR\'S RECOMMENDATION</div><div class="rxl">EreVanton <i>— blood</i></div><div class="rxl">Procarven <i>— prostate</i></div>'
            '<div class="rxs">COMPLETE PROTOCOL</div></div>')
mensagem("c43", "\"I had to get up four times", "That's exactly why my team reserved")

# S13/S14 — exclusividade, frete, preço, kit
@cena("c44", "F", "It is not sold separately,", "This offer exists exclusively here,")
def _(a, b):
    rows = ""
    for k, (f, t) in enumerate([("not available on our website,", "WEBSITE"), ("on Amazon,", "AMAZON"), ("or in pharmacies.", "PHARMACIES")]):
        tt = achar(f); em(f"#c44r{k}", tt, "{scale:.6, opacity:0, filter:'blur(14px)'}", "{scale:1, opacity:1, filter:'blur(0px)'}", 0.32, "back.out(2)"); S(tt, "k_clique", 0.18, 0.08)
        rows += f'<div class="li x" id="c44r{k}"><b>✕</b><span>{t}</span></div>'
    entra3d("#c44c", a + 0.02)
    return '<div class="vidro alto" id="c44c" style="top:520px"><div class="kick">NOT SOLD SEPARATELY</div>' + rows + '<div class="chip c3">ONLY ON THIS PAGE</div></div>'
B("c45", "for those who are already following the protocol.", "And because both orders", "assets/ia/q3_criado.mp4")
B("c46", "the laboratory can combine the shipping,", "The regular price", "assets/ia/nb_caixa_dois_frascos.mp4")

@cena("c47", "F", "The regular price", "The Procarven protocol consists")
def _(a, b):
    em("#c47p", a + 0.05, "{y:300, rotationY:-50, opacity:0, filter:'blur(24px)'}", "{y:0, rotationY:0, opacity:1, filter:'blur(0px)'}", 0.7)
    entra("#c47v", a + 0.3)
    em("#c47x", achar("but today you can add it"), "{scaleX:0}", "{scaleX:1}", 0.35, "power2.out")
    entra("#c47t", achar("practically the cost of production."))
    S(achar("but today you can add it"), "k_swish", 0.05, 0.57)
    return ('<i class="halo"></i><img class="hero sm" id="c47p" src="assets/img/procarven.png" width="400" height="677"><div class="kick c" style="top:1140px">REGULAR PRICE</div>'
            '<div class="price c" id="c47v" style="top:1220px">$97<small>/bottle</small><i class="risco" id="c47x"></i></div>'
            '<div class="cond mid c yel" id="c47t" style="top:1480px">TODAY: AT COST</div>')
B("c48", "The Procarven protocol consists", "The prostate cannot be accelerated.", "assets/ia/q2_capsula.mp4")
B("c49", "Each bottle lasts for 30 days.", "Below this video,", "assets/ia/q1_pia.mp4")

@cena("c50", "F", "Below this video,", "Not $99 per bottle.")
def _(a, b):
    em("#c50k", a + 0.02, "{scale:1.25, opacity:0, filter:'blur(24px)'}", "{scale:1, opacity:1, filter:'blur(0px)'}", 0.8)
    em("#c50c", achar("for just $99."), "{y:200, rotationX:40, opacity:0, filter:'blur(20px)'}", "{y:0, rotationX:0, opacity:1, filter:'blur(0px)'}", 0.6, "back.out(1.4)")
    S(achar("for just $99."), "cash", 0.12, 1.0)
    return ('<div class="kitbg" id="c50k">' + media("assets/ia/q5_kit6.mp4", a, b) + '</div><div class="kick c" style="top:220px"><span style="background:rgba(5,9,20,.82);padding:14px 26px;border-radius:40px">COMPLETE 180-DAY PROTOCOL</span></div>'
            '<div class="pcard" id="c50c"><b>6 BOTTLES</b><span>$99</span><i>total · 180 days</i></div>')

@cena("c51", "F", "Not $99 per bottle.", "We're practically offering")
def _(a, b):
    entra("#c51t", a + 0.02, "{scale:.6, opacity:0}", "{scale:1, opacity:1}", 0.35, "back.out(2)")
    for k in range(3): em(f"#c51a{k}", a + 0.1 + k * 0.1, "{y:-40, opacity:0}", "{y:0, opacity:1}", 0.3)
    js.append(f'tl.to("#c51i .seta3", {{y:30, duration:0.4, ease:"sine.inOut", yoyo:true, repeat:{max(1, int((b - a) / 0.4) - 1)}}}, {r(a + 0.4)});')
    return ('<div class="disp big c" style="top:520px">$99 <span class="yel">TOTAL</span></div><div class="chip red big c2" id="c51t" style="top:820px">NOT $99 PER BOTTLE</div>'
            '<div class="seta3">' + "".join(f'<svg id="c51a{k}" viewBox="0 0 120 120"><path d="M60 18v70M28 60l32 32 32-32" fill="none" stroke="#2BD67B" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></svg>' for k in range(3)) + '</div>')
B("c51b", "We're practically offering", "And I need to be honest", "assets/org/lab_frascos.mp4",
  extra='<div class="gradb"></div><div class="kbx"><div class="chip big c3s">AT COST · UNDER $100</div></div>')

# S15/S16 — janela, agora, dois caminhos
@cena("c52", "F", "The first 60 to 90 days", "This is the period")
def _(a, b):
    bate("#c52n", a + 0.2)
    return '<div class="kick c" style="top:560px">YOUR MOST IMPORTANT WINDOW</div><div class="num c yel" id="c52n" style="top:700px;font-size:250px">60–90</div><div class="cond mid c" style="top:1040px">DAYS</div>'
TB("c53", "It's also the shortest.", "If the prostate isn't included", "assets/ia3/ampulheta.mp4", "IT'S ALSO THE SHORTEST", 'THE WINDOW<br><span class="red">IS CLOSING</span>', cls="glowr")
TL("c53c", "it will be too late.", 2.4, "", 'TOO<br><span class="red">LATE</span>', "glowr", "bate")
M("c54", "The time is now,", "Because tomorrow,",
  lambda a, b: (bate("#c54t", a + 0.02) or '') + (entra("#c54s", achar("not tomorrow.")) or '') + '<div class="disp huge c yel glowy tback" id="c54t" style="top:170px">NOW.</div><div class="ser big c" id="c54s" style="top:360px">not tomorrow</div>')

@cena("c55", "F", "the two paths ahead of you,", "On the first path,")
def _(a, b):
    em("#c55a", a + 0.1, "{x:-600, rotationY:40, opacity:0, filter:'blur(24px)'}", "{x:0, rotationY:0, opacity:1, filter:'blur(0px)'}", 0.6)
    em("#c55b", a + 0.3, "{x:600, rotationY:-40, opacity:0, filter:'blur(24px)'}", "{x:0, rotationY:0, opacity:1, filter:'blur(0px)'}", 0.6)
    return '<div class="path g" id="c55a"><b>1</b><span>ACCEPT<br>TODAY</span></div><div class="path r" id="c55b"><b>2</b><span>REJECT<br>THE OFFER</span></div>'
B("c56", "On the first path,", "You'll be hard as steel,", "assets/ia/p5_caminho1.mp4", extra='<div class="tag g">PATH 1 · YOUR FIRMNESS STAYS</div>')
B("c56b", "You'll be hard as steel,", "On the second path,", "assets/ia3/casal_noite.mp4", teto=8.0,
  extra=letra_em("c56bt", "The entire night will belong", 'THE ENTIRE NIGHT<br><span class="yel">IS YOURS</span>', "glowy", "entra"))
B("c57", "On the second path,", "Except by then,", "assets/ia/p6_caminho2.mp4", extra='<div class="tag r">PATH 2 · THE SILENCE RETURNS</div>')
TL("c57b", "this page will no longer exist.", 2.6, "BY THEN", 'THIS PAGE<br><span class="red">IS GONE</span>', "glowr")
TL("c57c", "You don't need another treatment.", 4.0, "NOT ANOTHER TREATMENT", 'FINISH<br><span class="yel">THIS ONE</span>')
B("c58", "Your Procarven is already waiting", "Click the button below", "assets/ia/q4_caixa_casa.mp4")

# CTA (padrão do upsell validado: pílula laranja-amarela + seta redonda pulsando) e garantia
SETA = ('<svg class="seta" viewBox="0 0 120 120"><circle cx="60" cy="60" r="54" fill="#FBD643"/>'
        '<path d="M60 30v52M38 62l22 22 22-22" fill="none" stroke="#0b1630" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg>')
@cena("c59", "F", "Click the button below", "If, within 1 year,")
def _(a, b):
    em("#c59b", a + 0.05, "{scale:.4, opacity:0, filter:'blur(20px)'}", "{scale:1, opacity:1, filter:'blur(0px)'}", 0.45, "back.out(2)")
    em("#c59s", achar("1-year guarantee."), "{scale:2.2, rotation:-30, opacity:0, filter:'blur(20px)'}", "{scale:1, rotation:0, opacity:1, filter:'blur(0px)'}", 0.45, "back.out(2)")
    js.append(f'tl.to("#c59b .bt", {{scale:1.05, duration:0.45, ease:"sine.inOut", yoyo:true, repeat:{max(1, int((b - a) / 0.45) - 2)}}}, {r(a + 0.5)});')
    js.append(f'tl.to("#c59b .seta", {{y:18, duration:0.4, ease:"sine.inOut", yoyo:true, repeat:{max(1, int((b - a) / 0.4) - 2)}}}, {r(a + 0.5)});')
    S(a + 0.05, "k_pop", 0.09, 0.74); S(achar("1-year guarantee."), "k_impacto", 0.09, 0.3)
    return ('<div class="cta-g" id="c59b" style="top:640px"><div class="bt">COMPLETE MY PROTOCOL</div>' + SETA + '</div>'
            '<img class="selo" id="c59s" src="assets/img/selo_garantia_1year.png" width="500" height="500">')

@cena("c59b", "F", "We'll refund every penny", "Zero risk.")
def _(a, b):
    em("#c59bc", a + 0.02, "{y:300, rotationX:50, opacity:0, filter:'blur(24px)'}", "{y:0, rotationX:0, opacity:1, filter:'blur(0px)'}", 0.6)
    for k, f in enumerate(["No questions asked,", "no hassle."]):
        t = achar(f); em(f"#c59br{k}", t, "{x:-160, opacity:0, filter:'blur(16px)'}", "{x:0, opacity:1, filter:'blur(0px)'}", 0.4); S(t, "k_clique", 0.18, 0.08)
    return ('<div class="vidro alto" id="c59bc" style="top:560px"><div class="kick">1-YEAR GUARANTEE</div><div class="li"><b>$</b><span>EVERY PENNY BACK</span></div>'
            '<div class="li" id="c59br0"><b>✓</b><span>NO QUESTIONS</span></div><div class="li" id="c59br1"><b>✓</b><span>NO HASSLE</span></div></div>')
M("c60", "Zero risk.", "The only real risk",
  lambda a, b: (bate("#c60t", a + 0.02) or '') + '<div class="disp huge c yel glowy tback" id="c60t" style="top:170px">ZERO<br>RISK.</div>')
TL("c60b", "And you know that doesn't make any sense.", 2.6, "", 'MAKES <span class="red">NO</span><br>SENSE', "", "bate")
CTA_INI = achar("Complete the protocol, accept your Procarven,")

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
    f'<video id="v{s["id"]}" class="clip" src="assets/doutora/{s["id"]}.mp4" playsinline data-start="{q(s["s"])}" data-duration="{r(s["d"])}" data-track-index="0" data-has-audio="true" data-volume="1"></video>'
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

# produto entra quando o nome é falado (fora de telas cheias)
ult_p = -9
for x in W:
    n = norm(x["w"]).replace("'s", "")
    if n not in ("erevanton", "procarven"): continue
    t = q(x["s"] - 0.15)
    if coberto(t + 1.0, "TFBR") or coberto(t + 0.1, "TFBR") or t - ult_p < 6: continue
    ult_p = t; k = len(clips)
    img = "erevanton.png" if n == "erevanton" else "procarven.png"
    clips.append(f'<div id="pr{k}" class="clip prod" data-start="{t}" data-duration="2.4" data-track-index="9"><i class="pglow"></i><img src="assets/img/{img}" width="330" height="550"><b>{"EreVanton" if n == "erevanton" else "Procarven"}</b></div>')
    js.append(f'tl.fromTo("#pr{k}", {{x:420, rotationY:-55, opacity:0, filter:"blur(22px)"}}, {{x:0, rotationY:-12, opacity:1, filter:"blur(0px)", duration:0.55, ease:"expo.out", immediateRender:false}}, {t});')
    js.append(f'tl.to("#pr{k}", {{rotationY:6, y:-14, duration:1.5, ease:"sine.inOut"}}, {r(t + 0.55)});')
    js.append(f'tl.to("#pr{k}", {{x:420, opacity:0, filter:"blur(22px)", duration:0.35, ease:"power3.in"}}, {r(t + 2.05)});')
    S(t, "k_swish", 0.05, 0.57)
tm = q(achar("a few minutes of your attention", 0) - 0.1)
clips.append(f'<div id="relogio" class="clip relogio" data-start="{tm}" data-duration="5" data-track-index="9"><svg viewBox="0 0 64 64"><circle cx="32" cy="34" r="24" fill="none" stroke="#FFD23F" stroke-width="5"/><path d="M32 34V20M32 34l9 6" stroke="#fff" stroke-width="5" stroke-linecap="round"/><path d="M24 6h16" stroke="#FFD23F" stroke-width="5" stroke-linecap="round"/></svg><b id="relt">05:00</b></div>')
js.append(f'tl.fromTo("#relogio", {{y:-160, scale:.7, opacity:0, filter:"blur(18px)"}}, {{y:0, scale:1, opacity:1, filter:"blur(0px)", duration:0.5, ease:"back.out(1.8)", immediateRender:false}}, {tm});')
js.append(f'(function(){{var o={{v:300}},el=document.getElementById("relt");tl.fromTo(o,{{v:300}},{{v:295,duration:4.6,ease:"none",immediateRender:false,onUpdate:function(){{var n=Math.ceil(o.v);if(el)el.textContent="0"+Math.floor(n/60)+":"+String(n%60).padStart(2,"0");}}}},{tm});}})();')
js.append(f'tl.to("#relogio", {{y:-160, opacity:0, filter:"blur(18px)", duration:0.35, ease:"power3.in"}}, {r(tm + 4.6)});')
S(tm, "k_pop", 0.07, 0.74)

# luz nas entradas de b-roll/react
for k, t in enumerate(LUZES):
    clips.append(f'<div class="luz" id="lz{k}"><video id="vlz{k}" class="clip" src="assets/luz/lk{k % 6}.mp4" muted playsinline data-start="{q(max(0, t - 0.2))}" data-duration="0.56" data-track-index="{200 + k % 4}"></video></div>')
    js.append(f'tl.set("#lz{k}", {{opacity:0}}, 0); tl.set("#lz{k}", {{opacity:1}}, {q(max(0, t - 0.2))}); tl.set("#lz{k}", {{opacity:0}}, {q(t + 0.36)});')

# legenda pop (doutora sozinha, b-roll e react; nunca sob lettering T/F)
ASP = '"“”'
grupos, g = [], []
for x in W:
    g.append(x)
    if len(g) == 3 or re.search(r"[.,?!…:;—]\"?$", x["w"]): grupos.append(g); g = []
if g: grupos.append(g)
for i, g in enumerate(grupos):
    a = q(g[0]["s"]); b = q(grupos[i + 1][0]["s"]) if i + 1 < len(grupos) else q(g[-1]["e"] + 0.3)
    b = min(b, q(g[-1]["e"] + 0.6))
    if any(x0 < b - 0.15 and a + 0.15 < x1 and tp in "TF" for x0, x1, tp in COBRE): continue
    if any(x0 < b - 0.15 and a + 0.15 < x1 for x0, x1 in COMTEXTO): continue
    spans = "".join(f'<span id="cw{i}_{k}">{html.escape(x["w"].strip(ASP))}</span> ' for k, x in enumerate(g))
    baixa = ""
    clips.append(f'<div id="cap{i}" class="clip cap{baixa}" data-start="{a}" data-duration="{r(max(0.12, b - a))}" data-track-index="8"><div class="cap-in">{spans}</div></div>')
    js.append(f'tl.fromTo("#cap{i} .cap-in", {{scale:.8, y:20, opacity:0}}, {{scale:1, y:0, opacity:1, duration:0.16, ease:"back.out(2.4)", immediateRender:false}}, {a});')
    for k, x in enumerate(g):
        js.append(f'tl.set("#cw{i}_{k}", {{color:"#FFD23F", scale:1.08}}, {q(x["s"])}); tl.set("#cw{i}_{k}", {{color:"#ffffff", scale:1}}, {q(x["e"] + 0.05)});')

# CTA fixa do fim (mesmo desenho do validado)
clips.append(f'<div id="cta" class="clip cta" data-start="{q(CTA_INI)}" data-duration="{r(FIM - CTA_INI)}" data-track-index="9"><div class="cta-g fixo"><div class="bt">COMPLETE MY PROTOCOL</div>{SETA}</div></div>')
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

YEL, RED, BLU = "#FFD23F", "#FF4B3E", "#2F7BFF"
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
.prod {{ position:absolute; right:30px; top:700px; width:330px; z-index:6; perspective:1200px; text-align:center; }}
.prod img {{ position:relative; width:330px; height:auto; filter:drop-shadow(0 30px 40px rgba(0,0,0,.6)); }}
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
.li b {{ flex:none; width:96px; height:96px; border-radius:50%; background:{YEL}; color:#081024; font-size:54px; display:flex; align-items:center; justify-content:center; box-shadow:0 0 40px rgba(255,210,63,.45); }}
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
fontes = re.findall(r'src="(assets/(?:ia|org)/[^"]+)"', "".join(c for c in clips if 'class="st' in c))
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
