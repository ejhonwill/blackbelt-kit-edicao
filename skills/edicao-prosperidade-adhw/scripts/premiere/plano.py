import json,sys,re,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import cfg; C=cfg.load()
T,k=sys.argv[1],sys.argv[2]
d=json.load(open(f"{T}/{k}_timeline.json")); M=d["marcadores"]; dur=d["duracao"]
B=json.load(open(f"{T}/../broll/broll.json")); slug={b[0]:re.sub(r"[^A-Z0-9]+","-",b[1].upper()).strip("-") for b in B["items"]}
V=[];A=[]
brs=[m for m in M if m["nome"].startswith("BROLL")]
# hook push-in (avatar mudo em V2)
hook=[m for m in M if m["nome"]=="CENA_01_HOOK"][0]
he=min(hook["e"],brs[0]["s"] if brs else hook["e"])
V.append({"tr":1,"bin":"02. Brutos/AVATARES HEYGEN (SEM AUDIO)","nm":f"{k}_AVATAR_heygen-IV_v01_mute.mp4","t":0,"in":0,"dur":round(he,3),"kb":[100,110]})
ALT={"BR13":["BR13","BR10","BR12","BR09","BR21","BR26"],"BR10":["BR10","BR13","BR12","BR21","BR09"],"BR12":["BR12","BR21","BR10","BR13","BR11"],
"BR01":["BR01","BR04","BR20","BR03"],"BR04":["BR04","BR20","BR01"],"BR03":["BR03","BR19","BR25","BR01"],"BR02":["BR02","BR04","BR01"],
"BR08":["BR08","BANCO_Cerebro_007","BANCO_Cerebro_017","BANCO_Cerebro_001","BR09"],"BR09":["BR09","BR08","BANCO_Cerebro_007"],
"BR14":["REAL_MJ_01","REAL_MJ_04","REAL_MJ_05","REAL_MJ_03","BR14","BR15","BR18","BANCO_Multidoes_002"],"BR15":["REAL_MJ_02","REAL_MJ_03","REAL_MJ_05","BR15","BR14","BANCO_Multidoes_002","BR18"],"BR16":["BR16","BR17","BR20","BR04"],"BR17":["BR17","BR16","BR41"],
"BR07":["BR07","BR05","BR06","BR29"],"BR05":["BR05","BR07","BR06"],"BR06":["BR06","BR05","BR07"],"BR11":["BR11","BR12","BR21"],
"BR19":["BR19","BR46","BR03","BR24"],"BR20":["BR20","BR04","BR16"],"BR21":["BR21","BR12","BR10"],"BR22":["BR22","BR19","BR25"],"BR23":["BR23","BR24","BR25"],
"BR24":["BR24","BR42","BR19","BR23"],"BR25":["BR25","BR05","BR23"],"BR26":["BR26","BR27","BR28"],"BR27":["BR27","BR26","BR28"],"BR28":["BR28","BR26","BR27"],
"BR29":["BR29","BR30","BR03"],"BR30":["BR30","BR29","BANCO_Multidoes_002"],"BR31":["BR31","BR45","BR32","BR22","BR26","BR28"],"BR32":["BR32","BR31","BR22"],
"BR33":["REAL_ALI_04","REAL_ALI_02","BR33","BR34"],"BR34":["REAL_PHELPS_01","REAL_PHELPS_03","REAL_PHELPS_02","BR34","BR33"],"BR35":["REAL_CARREY_01","REAL_CARREY_02","BR35","BR04"],"BR36":["BR36","BR43","BR41"],"BR37":["BR37","BR39"],"BR38":["BR38","BR20","BR04"],
"BR39":["BR39","BR37","BR41"],"BR40":["BR40","BR44","BR41","BR26"],"BR41":["BR41","BR17","BR36"]}
BANCO={"BANCO_Cerebro_007":("BANCO_Cerebro_007_mute.mov",83.4),"BANCO_Cerebro_017":("BANCO_Cerebro_017_mute.mp4",179.1),"BANCO_Cerebro_001":("BANCO_Cerebro_001_mute.mp4",177.8),"BANCO_Multidoes_002":("BANCO_Multidoes_002_mute.mp4",177.8)}
usados=set(); escolha={}
for m in brs:
    bid0=m["obs"].split()[0]; bid=next((b for b in ALT.get(bid0,[bid0]) if b not in usados),None)
    if not bid: escolha[m["nome"]]=None; continue
    usados.add(bid); escolha[m["nome"]]=bid
    if bid.startswith("REAL_"):
        V.append({"tr":1,"bin":"03.Medias/FIGURAS PUBLICAS","nm":bid+".mp4","t":m["s"],"in":0.3,"dur":round(min(m["e"]-m["s"],4.6),3),"kb":[101,108],"id":bid})
    elif bid.startswith("BANCO"):
        nm,f=BANCO[bid]; V.append({"tr":1,"bin":"03.Medias/BANCO FOOTAGE (SEM AUDIO)","nm":nm,"t":m["s"],"in":1.0,"dur":round(min(m["e"]-m["s"],4.6),3),"kb":[round(f*1.01,1),round(f*1.08,1)],"id":bid})
    else:
        V.append({"tr":1,"bin":"03.Medias/BROLL KLING (SEM AUDIO)","nm":f"{bid}_{slug[bid]}_kling-turbo_v01_mute.mp4","t":m["s"],"in":0.2,"dur":round(min(m["e"]-m["s"],4.6),3),"kb":[101,108],"id":bid})
brs_ok=[m for m in brs if escolha.get(m["nome"])]
ocup=[(v["t"],v["t"]+v["dur"]) for v in V]
for m in M:
    if not m["nome"].startswith("CORTE_RITMO"): continue
    t=m["s"]; prox=min([b["s"] for b in brs if b["s"]>t]+[dur]); e=min(t+2.4,prox-0.05)
    if e-t<0.8 or any(a<e and t<b for a,b in ocup): continue
    V.append({"tr":1,"bin":"02. Brutos/AVATARES HEYGEN (SEM AUDIO)","nm":f"{k}_AVATAR_heygen-IV_v01_mute.mp4","t":round(t,3),"in":round(t,3),"dur":round(e-t,3),"sc":112}); ocup.append((t,e))
FIG={"MICHAEL JACKSON":["REAL_MJ_01","REAL_MJ_04","REAL_MJ_05","REAL_MJ_02","REAL_MJ_03"],"ALI":["REAL_ALI_04","REAL_ALI_02"],"PHELPS":["REAL_PHELPS_01","REAL_PHELPS_03","REAL_PHELPS_02"],"CARREY CHECK":["REAL_CARREY_01","REAL_CARREY_02"]}
def realitem(rid,t,d): return {"tr":1,"bin":"03.Medias/FIGURAS PUBLICAS","nm":rid+".mp4","t":round(t,3),"in":0.3,"dur":round(d,3),"kb":[101,108],"id":rid}
for m in M:
    if not m["nome"].startswith("KEYWORD"): continue
    fk=m["obs"].split(" — ")[0]
    if fk not in FIG: continue
    livre=[r for r in FIG[fk] if r not in usados]
    if not livre: continue
    ks=m["s"]; cob_=[v for v in V if v["tr"]==1 and v["t"]-0.3<=ks<v["t"]+v["dur"]]
    if cob_:
        v=cob_[0]
        if v.get("id","").startswith("REAL_"): continue
        if "AVATAR" in v["nm"]:
            V.remove(v)
        else:
            usados.discard(v.get("id")); r=livre[0]; usados.add(r); v.update(realitem(r,v["t"],min(v["dur"],4.6))); continue
    prox=min([v["t"] for v in V if v["tr"]==1 and v["t"]>ks]+[dur])
    d_=min(2.6,prox-ks-0.04)
    if d_>=1.2: r=livre[0]; usados.add(r); V.append(realitem(r,ks,d_))
V2=sorted([v for v in V if v["tr"]==1],key=lambda v:v["t"])
MAXD=lambda v: 4.84 if "kling" in v["nm"] else (4.7 if v["nm"].startswith("REAL_") else 9)
for a_,b_ in zip(V2,V2[1:]):
    gap=b_["t"]-(a_["t"]+a_["dur"])
    if 0<gap<0.6:
        if "AVATAR" in a_["nm"] or a_["dur"]+gap<=MAXD(a_): a_["dur"]=round(a_["dur"]+gap,3)
        elif "AVATAR" not in b_["nm"]: b_["t"]=round(b_["t"]-gap,3); b_["dur"]=round(min(b_["dur"]+gap,MAXD(b_)),3)
        else: a_["dur"]=round(a_["dur"]+gap,3)
cob=sorted((v["t"],v["t"]+v["dur"]) for v in V2); win=[];cur=0.0
for a_,b_ in cob:
    if a_-cur>=2.0: win.append((round(cur,3),round(a_,3)))
    cur=max(cur,b_)
if dur-cur>=2.0: win.append((round(cur,3),round(dur,3)))
Z=[]
for i_,(a_,b_) in enumerate(win): Z.append([a_,b_,100 if i_%2==0 else 107,107 if i_%2==0 else 100])
TR=["Colorful Glitch 1_mute.mp4","_Burning Light Transition 1_mute.mp4","_Burning Light Transition 3_mute.mp4"]
for i,m in enumerate([m for m in M if m["nome"].startswith("TRANSICAO")]):
    V.append({"tr":2,"bin":"03.Medias/TRANSICOES","nm":TR[i%3],"t":round(max(0,m["s"]-0.2),3),"in":0,"dur":0.7,"sc":178,"blend":22})
    A.append({"tr":3,"bin":"03.Medias/SFX","nm":"SFX_Digital_TV_Glitch_1.wav","t":round(max(0,m["s"]-0.2),3),"in":0,"dur":0.8})
cta=[m for m in M if m["nome"].startswith("LETTERING") and "LEARN MORE" in m["obs"]]
if cta:
    c=cta[-1]["s"]; V.append({"tr":2,"bin":"03.Medias/CTA","nm":"learn more_mute.mov","t":round(c,3),"in":0,"dur":3.7,"sc":70,"pos":[0.5,0.74]})
    A.append({"tr":3,"bin":"03.Medias/SFX","nm":"SFX_ES_Riser_Suction_5.wav","t":round(max(0,c-2.9),3),"in":0,"dur":2.9})
for i,v in enumerate(sorted([v for v in V if v["tr"]==1 and v.get("id")],key=lambda v:v["t"])):
    A.append({"tr":3,"bin":"03.Medias/SFX","nm":["SFX_Cinematic_Whoosh.wav","SFX_Deep_Swoosh_01.wav"][i%2],"t":round(max(0,v["t"]-0.25),3),"in":0,"dur":1.0})
for m in M:
    if m["nome"].startswith("LETTERING") and "LEARN MORE" not in m["obs"]:
        nm="SFX_Ding.wav" if "15 MIN" in m["obs"] else ("SFX_Cinematic_Boom.wav" if "4 PHASES" in m["obs"] else "SFX_ES_Suction_Pop_5.wav")
        A.append({"tr":3,"bin":"03.Medias/SFX","nm":nm,"t":round(m["s"],3),"in":0,"dur":0.6 if "Pop" in nm else 1.4})
A.append({"tr":2,"bin":"03.Medias/TRILHA","nm":f"{k}_TRILHA_v01.wav","t":0,"in":0,"dur":round(dur,3)})
J=C["job"]
def sec(x): h,m,r=x.split(":"); s_,ms=r.split(","); return int(h)*3600+int(m)*60+int(s_)+int(ms)/1000
for blk in open(f"{J}/MEDIA/LEGENDAS/{k}_LETTERING_v01.srt").read().split("\n\n"):
    pp=blk.strip().split("\n")
    if len(pp)<3: continue
    a,b=[sec(x.strip()) for x in pp[1].split("-->")]; txt=pp[2].strip()
    V.append({"tr":2,"bin":"03.Medias/LETTERING","nm":"LETTERING_"+re.sub(r"[^A-Z0-9]+","-",txt.upper()).strip("-")+"_v01.png","t":a,"in":0,"dur":round(b-a,3),"pos":[0.5,0.62],"pop":[88,104,100]})
# SFX sem sobreposição: corta o anterior
A.sort(key=lambda x:(x["tr"],x["t"]))
sf=[a for a in A if a["tr"]==3]
for i in range(len(sf)-1):
    sf[i]["dur"]=round(max(0.2,min(sf[i]["dur"],sf[i+1]["t"]-sf[i]["t"]-0.02)),3)
F=lambda x:round(round(x*25)/25,3)
for v in V+A:
    v["t"]=F(v["t"]); v["dur"]=F(v["dur"])
    if v.get("in",0)>1: v["in"]=v["t"]
V2=sorted([v for v in V if v["tr"]==1],key=lambda v:v["t"])
for a_,b_ in zip(V2,V2[1:]):
    fim=round(a_["t"]+a_["dur"],3)
    if b_["t"]<fim: a_["dur"]=round(b_["t"]-a_["t"],3)
    elif 0<b_["t"]-fim<0.6: a_["dur"]=round(b_["t"]-a_["t"],3)
json.dump({"seq":cfg.seq(C,k),"V":V,"A":A,"escolha":escolha,"Z":Z},open(f"{T}/{k}_plano.json","w"),indent=1)
print(k,"V2/V3:",len(V),"audio:",len(A))
