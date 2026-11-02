import json,sys,subprocess,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import cfg; C=cfg.load()
T=sys.argv[1]
for k in sys.argv[2:]:
    js="""var K=%s,NOME=K+"""+json.dumps(C["seq_sufixo"])+""";var seq=null;
for(var i=0;i<app.project.sequences.numSequences;i++)if(String(app.project.sequences[i].name)==NOME)seq=app.project.sequences[i];
if(!seq)return {erro:"sem seq"};app.project.activeSequence=seq;
function achar(bin,nm){var r=app.project.rootItem;var p=bin.split('/');for(var i=0;i<p.length;i++){for(var j=0;j<r.children.numItems;j++)if(String(r.children[j].name)==p[i]){r=r.children[j];break;}}
for(var j=0;j<r.children.numItems;j++)if(String(r.children[j].name)==nm)return r.children[j];return null;}
var av=achar("02. Brutos/AVATARES HEYGEN",K+"_AVATAR_heygen-IV_v01.mp4");var vz=achar("03.Medias/AUDIO FALAS DECUPADA",K+"_VOZ_decupada_v02.wav");
if(!av||!vz)return {erro:"midia",av:!!av,vz:!!vz};
var t0=new Time();t0.seconds=0;
if(seq.videoTracks[0].clips.numItems==0)seq.videoTracks[0].overwriteClip(av,t0);
if(seq.audioTracks[1].clips.numItems==0)seq.audioTracks[1].overwriteClip(vz,t0);
seq.audioTracks[0].setMute(1);
var q=qe.project.getActiveSequence();
var vn=["V1 AVATAR","V2 BROLL","V3 LETTERING"],an=["A1 AVATAR (MUDO)","A2 VOZ DECUPADA","A3 TRILHA","A4 SFX"];
for(var i=0;i<3;i++)try{q.getVideoTrackAt(i).setName(vn[i]);}catch(e){}
for(var i=0;i<4;i++)try{q.getAudioTrackAt(i).setName(an[i]);}catch(e){}
var c1=seq.videoTracks[0].clips[0],c2=seq.audioTracks[1].clips[0],c0=seq.audioTracks[0].clips[0];
return {seq:NOME,V1:[c1.start.seconds,c1.end.seconds,String(c1.name)],A1:c0?[c0.start.seconds,c0.end.seconds]:null,A2:[c2.start.seconds,c2.end.seconds,String(c2.name)],A1mudo:seq.audioTracks[0].isMuted()};"""%json.dumps(k)
    open(T+"/br.jsx","w").write(js)
    r=subprocess.run([T+"/pr.sh",T+"/br.jsx"],capture_output=True,text=True).stdout
    try: print(json.loads(json.loads(r)["result"]["content"][0]["text"]).get("retorno"),flush=True)
    except Exception: print(k,"ERRO",r[:400],flush=True)
