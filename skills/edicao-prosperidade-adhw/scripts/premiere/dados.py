import json,re,sys,difflib
W=sys.argv[1]; C=json.load(open(W+"/voz/copy_en.json")); B=json.load(open(W+"/broll/broll.json"))
KW={i[0]:i[1] for i in B["items"]}
N={"1":"one","2":"two","3":"three","4":"four","3rd":"third","4phase":"fourphase","10":"ten"}
nz=lambda x:N.get(re.sub(r"[^a-z0-9']","",x.lower().replace("’","'")),re.sub(r"[^a-z0-9']","",x.lower().replace("’","'")))
# regra: (regex na frase, keyword, broll, lettering ou None)
R=[(r"eye level",'MIRROR DETAIL','BR11','THE MIRROR DETAIL'),
(r"\breset\b",'RESET','BR19','RESET'),(r"\bsyntax\b",'SYNTAX','BR20','SYNTAX'),(r"\banchor\b",'ANCHOR','BR22','ANCHOR'),
(r"^mirror[.…]*$|mirror phase",'MIRROR PHASE','BR21','MIRROR'),
(r"15 minutes",'15 MINUTES A DAY','BR23','15 MIN / DAY'),
(r"four (specific )?phases|4 phases|4-phase|four-phase|the order mattered|order matters",'4 PHASES',None,'4 PHASES'),
(r"king.s code",'THE KING\'S CODE',None,"THE KING'S CODE"),
(r"muhammad ali",'ALI','BR33',None),(r"phelps",'PHELPS','BR34',None),(r"jim carrey|\$10 million",'CARREY CHECK','BR35','$10,000,000'),
(r"lie number (1|one)",'LIE #1','BR36','LIE #1'),(r"lie number (2|two)",'LIE #2','BR36','LIE #2'),(r"lie number (3|three)",'LIE #3','BR36','LIE #3'),
(r"learn more|link is|leave the link",'CTA','BR37','TAP LEARN MORE ↓'),
(r"pen and paper",'PEN AND PAPER','BR38',None),
(r"presentation|video explaining|short video|the video below",'PRESENTATION','BR39',None),
(r"handwritten|private writings|michael's writings|writings",'HANDWRITTEN','BR16',None),
(r"hidden for decades|hidden inside|allegedly hidden",'HIDDEN','BR17',None),
(r"michael jackson|michael (wasn|was|apparently|may|didn)",'MICHAEL JACKSON','BR14',None),
(r"affirmation",'AFFIRMATIONS','BR01',None),(r"vision board",'VISION BOARDS','BR02',None),(r"visualiz",'VISUALIZATION','BR03',None),
(r"journaling|writing (the same )?goal|wrote down|writing my goals|goals over",'WRITING GOALS','BR04',None),
(r"meditat",'MEDITATION','BR29',None),(r"neuroscience|brain|neurological",'BRAIN','BR08',None),
(r"old version|same person|same old",'OLD VERSION','BR10',None),
(r"same patterns|snapping back|returning|keep returning|same decisions",'SAME PATTERNS','BR07',None),
(r"pray|god |christian|faith",'FAITH','BR31',None),(r"universe",'UNIVERSE','BR40',None),
(r"mirror",'MIRROR','BR12',None),(r"identity",'IDENTITY','BR13',None),
(r"morning",'MORNING','BR24',None),(r"night|before going to sleep",'BEFORE SLEEP','BR25',None),
(r"opportunit",'OPPORTUNITIES','BR28',None),(r"decision",'DECISIONS','BR27',None),
(r"gurus|been told|teaching manifestation|millions of people",'GURUS','BR30',None),
(r"nobody (is )?talking|strange discovery|secret|here's what was discovered",'SECRET','BR41',None),
(r"stuck|limits|haven't changed|nothing changed",'STUCK','BR05',None),
(r"wealth|successful|rich|money",'SUCCESS','BR26',None)]
TRANS=r"here's where|that's where|which brings us|this is where|here's why|and that's when|but then|until i|that's why"
for k in sorted(C):
    toks=[t for line in C[k] for t in line.split()]
    wh=[x for s in json.load(open(f"{W}/voz/whisper/{k}_VOZ_decupada_v02.json"))["segments"] for x in s["words"]]
    a=[nz(t) for t in toks]; b=[nz(x["word"]) for x in wh]
    T=[None]*len(toks)
    for tag,i1,i2,j1,j2 in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
        if tag=="equal":
            for d in range(i2-i1): T[i1+d]=(wh[j1+d]["start"],wh[j1+d]["end"])
        elif tag=="replace" and j2>j1:
            s0,e0=wh[j1]["start"],wh[j2-1]["end"]; n=i2-i1
            for d in range(n): T[i1+d]=(s0+(e0-s0)*d/n,s0+(e0-s0)*(d+1)/n)
    for i in range(len(T)):  # buracos: herda vizinho
        if T[i] is None: p=T[i-1] if i else (0,0.2); T[i]=(p[1],p[1]+0.2)
    words=[{"w":toks[i],"s":round(T[i][0],3),"e":round(T[i][1],3)} for i in range(len(toks))]
    # SRT: 2-4 palavras, quebra em pontuação, max 22 chars
    cues=[];cur=[]
    for w in words:
        cur.append(w); txt=" ".join(x["w"] for x in cur)
        if re.search(r"[.!?…,:;]$",w["w"]) or len(cur)>=4 or len(txt)>=20: cues.append(cur);cur=[]
    if cur: cues.append(cur)
    def ts(t): h=int(t//3600);m=int(t%3600//60);s=t%60; return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s-int(s))*1000)):03d}".replace(",1000",",999")
    srt=[]
    for n,c in enumerate(cues,1):
        st=c[0]["s"]; en=cues[n][0]["s"] if n<len(cues) and cues[n][0]["s"]-c[-1]["e"]<0.35 else c[-1]["e"]+0.08
        txt=re.sub(r"[.…]+$",""," ".join(x["w"] for x in c)).replace("...","").strip()
        srt.append(f"{n}\n{ts(st)} --> {ts(en)}\n{txt}\n")
    open(f"{W}/timeline/{k}_LEGENDA_v01.srt","w").write("\n".join(srt))
    # frases
    sents=[];cur=[]
    for w in words:
        cur.append(w)
        if re.search(r"[.!?…:]$",w["w"]): sents.append(cur);cur=[]
    if cur: sents.append(cur)
    M=[];nb=nl=nk=nc=nt=0;last_br_end=3.2;usados={}
    total=words[-1]["e"]
    def add(nome,cor,s,e,obs): M.append({"nome":nome,"cor":cor,"s":round(s,3),"e":round(e,3),"obs":obs})
    # cenas
    M.append({"nome":"CENA_01_HOOK","cor":"red","s":0,"e":round(sents[0][-1]["e"],3),"obs":"Hook: avatar cheio na tela, sem b-roll nos 3 s iniciais. Punch-in leve na 1ª frase."})
    cta_s=None
    for snt in sents:
        txt=" ".join(x["w"] for x in snt); low=txt.lower().replace("’","'")
        s0,e0=snt[0]["s"],snt[-1]["e"]
        if re.search(TRANS,low): nt+=1; add(f"TRANSICAO_{nt:02d}","purple",s0,s0+0.4,f"Virada do copy: \"{txt[:60]}\" — whoosh/riser + glitch curto ou flash de luz")
        if cta_s is None and re.search(r"learn more|link|i recorded|i put together|i've left|the video (below|explaining)|saved the short video",low): cta_s=s0
        hits=0
        for rgx,kwn,br,let in R:
            m=re.search(rgx,low)
            if not m or hits>=2: continue
            hits+=1
            # palavra de início do match
            pos=len(re.findall(r"\S+",low[:m.start()])); ks=snt[min(pos,len(snt)-1)]["s"]
            nk+=1; add(f"KEYWORD_{nk:02d}","yellow",ks,min(e0,ks+1.2),f"{kwn} — \"{txt[:70]}\"")
            if let: nl+=1; add(f"LETTERING_{nl:02d}","orange",ks,min(ks+1.6,e0+0.3),f"Texto na tela: {let} | entra com pop/scale 90→100% + hit de SFX, sai em fade 6f")
            if br and ks>=last_br_end+0.7 and ks<total-1.5:
                be=min(max(e0,ks+2.0),ks+3.2); usados[br]=usados.get(br,0)+1
                nb+=1; add(f"BROLL_{nb:02d}","green",ks,be,f"{br} ({KW[br]}) — cobre: \"{txt[:70]}\" | entrada com whoosh, Ken Burns leve; legenda segue por cima")
                last_br_end=be
        dur=e0-s0
        if dur>3.5 and not any(x["nome"].startswith("BROLL") and x["s"]<=s0+1 and x["e"]>=s0 for x in M):
            nc+=1; add(f"CORTE_RITMO_{nc:02d}","blue",s0+dur/2,s0+dur/2+0.1,"Frase longa no avatar — punch-in 100→112% (corte seco) pra quebrar o plano")
    if cta_s: M.append({"nome":"CENA_99_CTA","cor":"red","s":round(cta_s,3),"e":round(total,3),"obs":"Bloco de CTA: seta animada 'Learn More ↓' no rodapé, riser antes, trilha sobe 2 dB"})
    M.sort(key=lambda x:x["s"])
    json.dump({"palavras":words,"marcadores":M,"duracao":total},open(f"{W}/timeline/{k}_timeline.json","w"),indent=1,ensure_ascii=False)
    c=lambda p:sum(1 for x in M if x["nome"].startswith(p))
    print(k,f"{total:.1f}s legendas={len(cues)} BROLL={c('BROLL')} LETTERING={c('LETTERING')} KEYWORD={c('KEYWORD')} CORTE={c('CORTE')} TRANS={c('TRANS')} cobertura_broll={sum(x['e']-x['s'] for x in M if x['nome'].startswith('BROLL'))/total*100:.0f}%")
