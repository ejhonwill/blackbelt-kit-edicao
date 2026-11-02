import json,sys,subprocess,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import cfg; C=cfg.load()
T=sys.argv[1]; H=os.path.join(C["job"],"HYPERFRAMES"); V=C.get("overlay_versao","v02")
for k in sys.argv[2:]:
    js="""var K=%s,NOME=K+"""+json.dumps(C["seq_sufixo"])+""",F=%s;var seq=null;
for(var i=0;i<app.project.sequences.numSequences;i++)if(String(app.project.sequences[i].name)==NOME)seq=app.project.sequences[i];
app.project.activeSequence=seq;
function bin(p){var parts=p.split('/'),cur=app.project.rootItem;for(var i=0;i<parts.length;i++){var f=null;for(var j=0;j<cur.children.numItems;j++){var c=cur.children[j];if(c.type==2&&String(c.name)==parts[i]){f=c;break;}}if(!f)f=cur.createBin(parts[i]);cur=f;}return cur;}
var b=bin("03.Medias/HYPERFRAMES OVERLAY");var nm=F.split('/').pop();var it=null;
for(var j=0;j<b.children.numItems;j++)if(String(b.children[j].name)==nm)it=b.children[j];
if(!it){app.project.importFiles([F],true,b,false);for(var j=0;j<b.children.numItems;j++)if(String(b.children[j].name)==nm)it=b.children[j];}
if(!it)return {erro:"import"};
var tr=seq.videoTracks[2];for(var c=tr.clips.numItems-1;c>=0;c--)tr.clips[c].remove(false,false);
var t0=new Time();t0.seconds=0;tr.overwriteClip(it,t0);tr=seq.videoTracks[2];var c=tr.clips[0];
c.end=seq.videoTracks[0].clips[0].end;
return {seq:NOME,v3:tr.clips.numItems,nome:String(c.name),ini:c.start.seconds,fim:c.end.seconds,fimV1:seq.videoTracks[0].clips[0].end.seconds,a3:seq.audioTracks[2].clips.numItems,a2:seq.audioTracks[1].clips.numItems};"""%(json.dumps(k),json.dumps(f"{H}/{k}_OVERLAY_hyperframes_{V}.mov"))
    open(T+"/ov.jsx","w").write(js)
    r=subprocess.run([T+"/pr.sh",T+"/ov.jsx","300"],capture_output=True,text=True).stdout
    try: print(json.loads(json.loads(r)["result"]["content"][0]["text"]).get("retorno"),flush=True)
    except Exception: print(k,"ERRO",r[:400],flush=True)
