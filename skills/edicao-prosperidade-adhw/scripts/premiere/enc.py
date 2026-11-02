"""Fila do Media Encoder para todas as sequências do job. uso: python3 enc.py   (lê job.json)"""
import json,os,subprocess,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import cfg; C=cfg.load(); T=os.path.dirname(os.path.abspath(__file__))
P="/Applications/Adobe Media Encoder 2026/Adobe Media Encoder 2026.app/Contents/MediaIO/systempresets/4E49434B_48323634/00 - Match Source - High bitrate.epr"
os.makedirs(os.path.join(C["job"],"EXPORT"),exist_ok=True)
itens=[[cfg.seq(C,k),os.path.join(C["job"],"EXPORT",C["entrega"].format(AD="AD"+k[1:]))] for k in sorted(C["bodies"])]
js="""var L=%s,P=%s;app.encoder.launchEncoder();var ok=[];
for(var n=0;n<L.length;n++){var seq=null;for(var i=0;i<app.project.sequences.numSequences;i++)if(String(app.project.sequences[i].name)==L[n][0])seq=app.project.sequences[i];
 if(!seq){ok.push("SEM "+L[n][0]);continue;}var id=app.encoder.encodeSequence(seq,L[n][1],P,0,1);ok.push(L[n][0]+" -> "+id);}
app.encoder.startBatch();return ok;"""%(json.dumps(itens),json.dumps(P))
open(T+"/enc.jsx","w").write(js)
print(subprocess.run([T+"/pr.sh",T+"/enc.jsx","300"],capture_output=True,text=True).stdout[:1500])
