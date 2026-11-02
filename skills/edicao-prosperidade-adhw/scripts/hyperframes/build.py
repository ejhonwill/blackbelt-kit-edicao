"""Gera um projeto HyperFrames por body: legenda animada + lettering + flash/light + CTA, fundo transparente.
Uso: python3 build.py B01 [B02 ...]   (lê ../_dados/Bxx_timeline.json, Bxx_plano.json e ../../MEDIA/LEGENDAS/Bxx_LETTERING_v01.srt)"""
import json,os,re,sys,shutil,html
AQUI=os.path.dirname(os.path.abspath(__file__)); RAIZ=os.path.dirname(AQUI); JOB=os.path.dirname(RAIZ)
FONTE=os.path.expanduser("~/Library/Fonts/Montserrat-ExtraBold.otf"); FPS=25
def sec(x): h,m,r=x.split(":"); s,ms=r.split(","); return int(h)*3600+int(m)*60+int(s)+int(ms)/1000
def cues(words):
    out=[];cur=[]
    for w in words:
        cur.append(w); txt=" ".join(x["w"] for x in cur)
        if re.search(r"[.!?…,:;]$",w["w"]) or len(cur)>=4 or len(txt)>=20: out.append(cur);cur=[]
    if cur: out.append(cur)
    return out
def limpa(w): return html.escape(re.sub(r"(\.\.\.|…|[.,:;])+$","",w).upper().replace("’","'"))
def build(k):
    d=json.load(open(f"{RAIZ}/_dados/{k}_timeline.json")); P=json.load(open(f"{RAIZ}/_dados/{k}_plano.json"))
    dur=round(max(d["duracao"],max(v["t"]+v["dur"] for v in P["V"]))+0.4,2); M=d["marcadores"]
    proj=f"{RAIZ}/{k}"; os.makedirs(proj+"/assets",exist_ok=True); shutil.copy(FONTE,proj+"/assets/Montserrat-ExtraBold.otf")
    C=cues(d["palavras"]); els=[]; js=[]
    Lt=[]
    for blk in open(f"{JOB}/MEDIA/LEGENDAS/{k}_LETTERING_v01.srt").read().split("\n\n"):
        pp=blk.strip().split("\n")
        if len(pp)>=3: a,b=[sec(x.strip()) for x in pp[1].split("-->")]; Lt.append((a,b,pp[2].strip()))
    for i,c in enumerate(C):
        txt=" ".join(limpa(w["w"]) for w in c)
        if any(t==txt and a<c[-1]["e"] and c[0]["s"]<b for a,b,t in Lt): continue
        s=c[0]["s"]; e=C[i+1][0]["s"] if i+1<len(C) and C[i+1][0]["s"]-c[-1]["e"]<0.35 else c[-1]["e"]+0.12
        e=max(e,s+0.2); spans=""
        for j,w in enumerate(c): spans+=f'<span class="w" id="c{i}w{j}"><i class="hl" id="c{i}h{j}"></i><b>{limpa(w["w"])}</b></span> '
        els.append(f'<div class="clip cap" data-start="{s:.3f}" data-duration="{e-s:.3f}" data-track-index="1"><div class="capin" id="c{i}">{spans}</div></div>')
        js.append(f'tl.fromTo("#c{i}",{{scale:0.86,opacity:0}},{{scale:1,opacity:1,duration:0.12,ease:"back.out(2)"}},{s:.3f});')
        for j,w in enumerate(c):
            ws=w["s"]; we=c[j+1]["s"] if j+1<len(c) else e
            js.append(f'tl.fromTo("#c{i}h{j}",{{opacity:0,scale:0.7}},{{opacity:1,scale:1,duration:0.06,ease:"power2.out"}},{ws:.3f});')
            if we-ws>0.08: js.append(f'tl.fromTo("#c{i}h{j}",{{opacity:1}},{{opacity:0,duration:0.04}},{max(ws+0.06,we-0.04):.3f});')
    # lettering
    L=[]
    for blk in open(f"{JOB}/MEDIA/LEGENDAS/{k}_LETTERING_v01.srt").read().split("\n\n"):
        pp=blk.strip().split("\n")
        if len(pp)>=3: a,b=[sec(x.strip()) for x in pp[1].split("-->")]; L.append((a,b,pp[2].strip()))
    FASES={"RESET","SYNTAX","MIRROR","ANCHOR"}
    KWMAP={"THE KING'S CODE":{"KING'S","CODE"},"15 MIN / DAY":{"15","MIN"},"THE MIRROR DETAIL":{"MIRROR"},"4 PHASES":{"PHASES"}}
    for i,(a,b,t) in enumerate(L):
        pal=t.split(); kws=KWMAP.get(t) or ({p_ for p_ in pal if p_.startswith("#")} if t.startswith("LIE") else set(pal))
        partes=""
        for j,p_ in enumerate(pal):
            e_=html.escape(p_)
            if p_ in kws: partes+=f'<span class="kw" data-layout-allow-overlap><span class="kwg" data-layout-allow-overlap id="l{i}g{j}">{e_}</span><span class="kwt" data-layout-allow-overlap>{e_}</span></span>'
            else: partes+=f'<span class="nw">{e_}</span>'
        tam="fase" if t in FASES else ""
        els.append(f'<div class="clip letc" data-start="{a:.3f}" data-duration="{b-a:.3f}" data-track-index="2"><div class="letbox" id="l{i}"><div class="halo" id="lh{i}"></div><div class="lt {tam}" id="lt{i}">{partes}</div></div></div>')
        js.append(f'tl.fromTo("#lh{i}",{{opacity:0,scale:0.7}},{{opacity:1,scale:1,duration:0.25,ease:"power2.out"}},{a:.3f});')
        js.append(f'tl.fromTo("#lt{i}",{{scale:0.6,opacity:0,filter:"blur(18px)"}},{{scale:1.06,opacity:1,filter:"blur(0px)",duration:0.22,ease:"power3.out"}},{a:.3f});')
        js.append(f'tl.fromTo("#lt{i}",{{scale:1.06}},{{scale:1,duration:0.16,ease:"power2.out"}},{a+0.22:.3f});')
        for j,p_ in enumerate(pal):
            if p_ in kws:
                js.append(f'tl.fromTo("#l{i}g{j}",{{opacity:0,scale:0.9}},{{opacity:1,scale:1.12,duration:0.12,ease:"power2.out"}},{a+0.1:.3f});')
                js.append(f'tl.fromTo("#l{i}g{j}",{{opacity:1,scale:1.12}},{{opacity:0.6,scale:1,duration:0.45,ease:"sine.out"}},{a+0.22:.3f});')
        if b-a>0.5: js.append(f'tl.fromTo("#l{i}",{{opacity:1}},{{opacity:0,duration:0.12}},{b-0.12:.3f});')
    # transicoes flash/light
    fl=[0.0]
    hook=[m for m in M if m["nome"]=="CENA_01_HOOK"]; 
    brs=sorted(v["t"] for v in P["V"] if v.get("id"))
    if brs: fl.append(brs[0])
    fl+= [m["s"] for m in M if m["nome"].startswith("TRANSICAO")]
    cta=[m for m in M if m["nome"]=="CENA_99_CTA"]
    if cta: fl.append(cta[0]["s"])
    fl=sorted(set(round(x,2) for x in fl if x>0.3))
    lights=[t for i,t in enumerate(brs[1:],1) if i%3==0 and all(abs(t-f)>1 for f in fl)]
    for i,t in enumerate(fl):
        els.append(f'<div class="clip" data-start="{max(0,t-0.08):.3f}" data-duration="0.4" data-track-index="3"><div class="flash" id="f{i}"></div></div>')
        js.append(f'tl.fromTo("#f{i}",{{opacity:0}},{{opacity:0.92,duration:0.07,ease:"power2.in"}},{max(0,t-0.08):.3f});')
        js.append(f'tl.fromTo("#f{i}",{{opacity:0.92}},{{opacity:0,duration:0.28,ease:"power2.out"}},{max(0,t-0.08)+0.07:.3f});')
    for i,t in enumerate(lights):
        els.append(f'<div class="clip" data-start="{max(0,t-0.15):.3f}" data-duration="0.9" data-track-index="4"><div class="light" id="g{i}"></div></div>')
        js.append(f'tl.fromTo("#g{i}",{{xPercent:-60,opacity:0}},{{xPercent:10,opacity:0.75,duration:0.35,ease:"sine.in"}},{max(0,t-0.15):.3f});')
        js.append(f'tl.fromTo("#g{i}",{{xPercent:10,opacity:0.75}},{{xPercent:60,opacity:0,duration:0.5,ease:"sine.out"}},{max(0,t-0.15)+0.35:.3f});')
    # CTA
    ctaL=[m for m in M if m["nome"].startswith("LETTERING") and "LEARN MORE" in m["obs"]]
    if ctaL:
        a=ctaL[-1]["s"]; b=dur-0.3
        els.append(f'<div class="clip ctac" data-start="{a:.3f}" data-duration="{b-a:.3f}" data-track-index="5"><div class="cta" id="cta"><span>LEARN MORE</span><em id="seta">↓</em></div></div>')
        js.append(f'tl.fromTo("#cta",{{y:120,opacity:0,scale:0.8}},{{y:0,opacity:1,scale:1,duration:0.35,ease:"back.out(1.8)"}},{a:.3f});')
        n=int((b-a-0.4)/0.8)
        if n>0: js.append(f'tl.fromTo("#cta",{{scale:1}},{{scale:1.06,duration:0.4,ease:"sine.inOut",yoyo:true,repeat:{2*n-1}}},{a+0.4:.3f});')
        if n>0: js.append(f'tl.fromTo("#seta",{{y:-6}},{{y:10,duration:0.4,ease:"sine.inOut",yoyo:true,repeat:{2*n-1}}},{a+0.4:.3f});')
    doc=f'''<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/><title>{k} overlay</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
@font-face{{font-family:"MontX";src:url("assets/Montserrat-ExtraBold.otf") format("opentype");font-weight:800;}}
html,body{{margin:0;background:transparent;}}
#root{{position:relative;width:100%;height:100%;overflow:hidden;font-family:"MontX",sans-serif;}}
.clip{{position:absolute;inset:0;}}
.cap{{display:flex;justify-content:center;align-items:flex-start;}}
.capin{{position:absolute;top:71%;left:60px;right:60px;display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:6px 18px;text-align:center;}}
.w{{position:relative;display:inline-block;padding:4px 12px;}}
.w b{{position:relative;font-weight:800;font-size:76px;line-height:1.05;color:#fff;letter-spacing:0.5px;-webkit-text-stroke:3px #0a0a0a;paint-order:stroke fill;text-shadow:0 6px 18px rgba(0,0,0,.55);}}
.hl{{position:absolute;inset:2px 0;background:#6C2BD9;border-radius:14px;opacity:0;box-shadow:0 6px 20px rgba(108,43,217,.45);}}
.letc{{display:flex;justify-content:center;}}
.letbox{{position:absolute;top:47%;left:0;right:0;display:flex;justify-content:center;}}
.halo{{position:absolute;top:50%;left:50%;width:1000px;height:420px;margin:-210px 0 0 -500px;background:radial-gradient(ellipse at center,rgba(0,0,0,.55),rgba(0,0,0,0) 68%);opacity:0;}}
.lt{{position:relative;display:flex;flex-wrap:wrap;justify-content:center;gap:0 28px;max-width:1000px;font-weight:800;font-size:128px;line-height:1.04;text-align:center;}}
.lt.fase{{font-size:178px;}}
.nw{{color:#fff;-webkit-text-stroke:4px #0a0a0a;paint-order:stroke fill;text-shadow:0 8px 26px rgba(0,0,0,.6);}}
.kw{{position:relative;display:inline-block;}}
.kwt{{position:relative;color:#FFD60A;-webkit-text-stroke:3px #3a2600;paint-order:stroke fill;text-shadow:0 0 6px rgba(255,240,140,.95),0 0 18px rgba(255,214,10,.85),0 0 42px rgba(255,190,0,.7),0 0 85px rgba(255,150,0,.5),0 0 140px rgba(255,120,0,.32);}}
.kwg{{position:absolute;left:0;top:0;color:#FFC400;filter:blur(24px);opacity:0;white-space:nowrap;}}
.flash{{position:absolute;inset:0;background:#fff;opacity:0;}}
.light{{position:absolute;top:-10%;left:-30%;width:160%;height:120%;opacity:0;background:radial-gradient(ellipse 45% 60% at 50% 50%,rgba(255,214,140,.95),rgba(255,140,40,.55) 40%,rgba(255,90,0,0) 72%);}}
.ctac{{display:flex;justify-content:center;}}
.cta{{position:absolute;top:84%;display:flex;align-items:center;gap:18px;background:#fff;border-radius:999px;padding:24px 56px;box-shadow:0 12px 36px rgba(0,0,0,.45);}}
.cta span{{font-weight:800;font-size:64px;color:#E31B23;letter-spacing:1px;}}
.cta em{{font-style:normal;font-weight:800;font-size:64px;color:#E31B23;display:block;}}
</style></head><body>
<div id="root" data-composition-id="{k.lower()}" data-start="0" data-width="1080" data-height="1920" data-fps="{FPS}" data-duration="{dur}">
{chr(10).join(els)}
</div>
<script>
const tl=gsap.timeline({{paused:true}});
{chr(10).join(js)}
window.__timelines["{k.lower()}"]=tl;
</script></body></html>'''
    open(proj+"/index.html","w").write(doc)
    if not os.path.exists(proj+"/hyperframes.json"): json.dump({"name":f"kingscode-{k.lower()}-overlay"},open(proj+"/hyperframes.json","w"))
    print(k,"cues",len(C),"lettering",len(L),"flash",len(fl),"light",len(lights),"dur",dur)
for k in sys.argv[1:]: build(k)
