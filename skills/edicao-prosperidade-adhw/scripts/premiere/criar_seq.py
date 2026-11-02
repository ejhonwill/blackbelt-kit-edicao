import json,sys,subprocess,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import cfg; C=cfg.load()
T=sys.argv[1]
for k in sys.argv[2:]:
    nome=cfg.seq(C,k)
    js="""var NOME=%s;var src=null,ex=null,ids={};
for(var i=0;i<app.project.sequences.numSequences;i++){var s=app.project.sequences[i];ids[String(s.sequenceID)]=1;if(String(s.name)=="9x16")src=s;if(String(s.name)==NOME)ex=s;}
if(ex)return {ja:NOME};
src.clone();var nv=null;
for(var i=0;i<app.project.sequences.numSequences;i++){var s=app.project.sequences[i];if(!ids[String(s.sequenceID)]){nv=s;break;}}
if(!nv)return {erro:"clone nao achado"};
nv.name=NOME;
var st=nv.getSettings();var t=new Time();t.ticks="10160640000";st.videoFrameRate=t;nv.setSettings(st);
for(var v=0;v<nv.videoTracks.numTracks;v++){var tr=nv.videoTracks[v];for(var c=tr.clips.numItems-1;c>=0;c--)tr.clips[c].remove(false,false);}
for(var a=0;a<nv.audioTracks.numTracks;a++){var tr=nv.audioTracks[a];for(var c=tr.clips.numItems-1;c>=0;c--)tr.clips[c].remove(false,false);}
var m=nv.markers;var mk=m.getFirstMarker();while(mk){var nx=m.getNextMarker(mk);m.deleteMarker(mk);mk=nx;}
var bin=null;for(var j=0;j<app.project.rootItem.children.numItems;j++){var c=app.project.rootItem.children[j];if(String(c.name)=="01. Sequences")bin=c;}
var pi=nv.projectItem; if(bin&&pi)pi.moveBin(bin);
return {nome:String(nv.name),tb:String(nv.timebase),w:nv.frameSizeHorizontal,h:nv.frameSizeVertical,vt:nv.videoTracks.numTracks,at:nv.audioTracks.numTracks};"""%json.dumps(nome)
    open(T+"/seq.jsx","w").write(js)
    r=subprocess.run([T+"/pr.sh",T+"/seq.jsx"],capture_output=True,text=True).stdout
    try: print(k,json.loads(json.loads(r)["result"]["content"][0]["text"]),flush=True)
    except Exception: print(k,"ERRO",r[:400],flush=True)
