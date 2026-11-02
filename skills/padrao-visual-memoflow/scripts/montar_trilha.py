#!/usr/bin/env python3
"""Coloca a trilha no master: um movimento por trecho, com cruzamento e nível medido.

Espera os arquivos em 21_TRILHA nomeados pelo movimento (A_ESPERANCA..., B_INTIMO...).
O nível vem da medição da locução, não de chute: a cama fica 19 dB abaixo da voz e
sobe 8 dB nas respiradas entre as frases.
"""
import json, os, re, sys

S = os.path.dirname(os.path.abspath(__file__))
L = ("/Users/jhonwill/Library/CloudStorage/GoogleDrive-jhonatan.araujo@hw-publishing.com/Drives compartilhados/"
     "H&W - Edição de Vídeo -Q3/Arquivo de Edição /08. Memory/MemoFlow/OT/[160926][OT] Upsell #1 [MemoFlow] [Squad]")
D = f"{L}/MEMOFLOW_LIPSYNC/21_TRILHA"
plano = json.load(open(f"{D}/mapa_trilha.json"))

arqs = {}
for f in sorted(os.listdir(D)):
    if not f.lower().endswith((".wav", ".mp3", ".aif", ".aiff", ".m4a")): continue
    for fid in plano["faixas_necessarias"]:
        if f.upper().startswith(fid): arqs.setdefault(fid, os.path.join(D, f))

faltam = [f for f in plano["faixas_necessarias"] if f not in arqs]
if faltam:
    print("faltam faixas em 21_TRILHA:", ", ".join(faltam))
    print("nomeie cada arquivo comecando pelo id do movimento, por exemplo A_ESPERANCA_<nome>.wav")
    sys.exit(1)

NIV = plano["cama_sob_fala_dBFS"]; RESP = plano["cama_nas_respiradas_dBFS"]
FADE = plano["abertura_e_fechamento_s"]; CRUZ = plano["cruzamento_entre_movimentos_s"]
mv = plano["movimentos"]
js = ",".join('{id:"%s",arq:"%s",t:%.3f,f:%.3f,primeiro:%d,ultimo:%d}' %
              (m["id"], arqs[m["id"]], m["t"], m["f"], 1 if i == 0 else 0, 1 if i == len(mv)-1 else 0)
              for i, m in enumerate(mv))

JS = '''(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  function pasta(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof FolderItem&&x.name===n)return x;}return p.items.addFolder(n);}
  var M=comp("UPSELL #1 - DR (MASTER)"); if(!M) throw new Error("sem MASTER");
  for(var k=M.numLayers;k>=1;k--){ if(M.layer(k).name.indexOf("TRILHA")===0) M.layer(k).remove(); }
  var bA=pasta("07 AUDIO");
  var NIV=%d, FADE=%.2f, CRUZ=%.2f;
  var T=[%s]; var n=0;
  for(var i=0;i<T.length;i++){
    var d=T[i]; var f=new File(d.arq);
    if(!f.exists){ out.push("FALTA "+d.arq); continue; }
    var item=null, nome=d.arq.split("/").pop();
    for(var q=1;q<=p.numItems;q++){ var x=p.item(q); if(x instanceof FootageItem && x.name===nome) item=x; }
    if(!item){ item=p.importFile(new ImportOptions(f)); item.parentFolder=bA; }
    var L2=M.layers.add(item);
    L2.name="TRILHA "+(i+1)+" "+d.id;
    var ini=Math.max(0, d.t-(d.primeiro?0:CRUZ));
    L2.startTime=ini; L2.inPoint=ini; L2.outPoint=Math.min(d.f+ (d.ultimo?0:CRUZ), M.duration);
    var au=L2.property("Audio").property("Audio Levels");
    var a=L2.inPoint, b=L2.outPoint;
    var subir=d.primeiro?FADE:CRUZ, descer=d.ultimo?FADE:CRUZ;
    au.setValueAtTime(a,[-48,-48]);
    au.setValueAtTime(a+subir,[NIV,NIV]);
    au.setValueAtTime(b-descer,[NIV,NIV]);
    au.setValueAtTime(b,[-48,-48]);
    for(var e=1;e<=au.numKeys;e++){ try{ au.setInterpolationTypeAtKey(e,KeyframeInterpolationType.BEZIER,KeyframeInterpolationType.BEZIER); }catch(er){} }
    n++;
    out.push("  "+L2.name+"  "+a.toFixed(2)+"-"+b.toFixed(2)+"s  a "+NIV+" dB");
  }
  out.unshift("movimentos de trilha colocados="+n+" | cama "+NIV+" dB, cruzamento "+CRUZ+"s");
  app.project.save();
  var fo=new File("/tmp/ae_trilha.txt"); fo.open("w"); fo.write(out.join(String.fromCharCode(10))); fo.close();
 }catch(e){ var fe=new File("/tmp/ae_trilha.txt"); fe.open("w"); fe.write("ERRO: "+e.toString()+" linha "+e.line); fe.close(); }
})();''' % (NIV, FADE, CRUZ, js)
open(f"{S}/ae_trilha.jsx", "w").write(JS)
print("faixas encontradas:")
for k, v in arqs.items(): print(f"   {k:<14} {os.path.basename(v)}")
print(f"\nscript pronto: {len(mv)} movimentos, cama a {NIV} dB, cruzamento {CRUZ}s")
