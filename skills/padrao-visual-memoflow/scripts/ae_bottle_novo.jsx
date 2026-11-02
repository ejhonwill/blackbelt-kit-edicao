(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  function pasta(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof FolderItem&&x.name===n)return x;}return p.items.addFolder(n);}
  var ARQ="/Users/jhonwill/Library/CloudStorage/GoogleDrive-jhonatan.araujo@hw-publishing.com/Drives compartilhados/H&W - Edição de Vídeo -Q3/Arquivo de Edição /08. Memory/MemoFlow/OT/[160926][OT] Upsell #1 [MemoFlow] [Squad]/MEDIA/BOTTLE/1-MemoFlow.png";
  var novo=null;
  for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof FootageItem && x.name==="1-MemoFlow.png") novo=x; }
  if(!novo){ var f=new File(ARQ); if(!f.exists) throw new Error("PNG nao encontrado"); novo=p.importFile(new ImportOptions(f)); novo.parentFolder=pasta("01 MATERIAL"); }
  try{ novo.mainSource.alphaMode=AlphaMode.STRAIGHT; }catch(e0){}
  out.push("fonte: "+novo.name+" "+novo.width+"x"+novo.height);

  // geometria medida no PNG: frasco em x579-839, y25-874 -> centro (709,450), altura 850
  var CX=709, CY=450, ALT=850;
  var ALT_ANTES=1830*0.44;                 // altura que o frasco antigo tinha na tela
  var ESC=ALT_ANTES/ALT*100;               // mesma altura na tela com a fonte nova

  var B=comp("MEMOFLOW_BOTTLE_CUTOUT"); if(!B) throw new Error("sem MEMOFLOW_BOTTLE_CUTOUT");
  var trocadas=0;
  for(var k=1;k<=B.numLayers;k++){
    var L=B.layer(k);
    if(L.name!=="FRASCO" && L.name!=="LIGHT WRAP") continue;
    var pos=L.property("Transform").property("Position").value;
    L.replaceSource(novo,false);
    L.property("Transform").property("Anchor Point").setValue([CX,CY]);
    L.property("Transform").property("Scale").setValue([ESC,ESC]);
    L.property("Transform").property("Position").setValue([pos[0],pos[1]]);
    trocadas++;
  }
  out.push("camadas trocadas="+trocadas+" | escala "+ESC.toFixed(1)+"% | ancora no centro do frasco ("+CX+","+CY+")");

  // ainda existe algum uso do recorte antigo fora dessa comp?
  var antigo=null;
  for(var q=1;q<=p.numItems;q++){ var y=p.item(q); if(y instanceof FootageItem && y.name==="MEMOFLOW_FRASCO_RECORTE.png") antigo=y; }
  var usos=[];
  if(antigo){
    for(var c=1;c<=p.numItems;c++){ var cc=p.item(c); if(!(cc instanceof CompItem)) continue;
      for(var l=1;l<=cc.numLayers;l++){ try{ if(cc.layer(l).source===antigo) usos.push(cc.name+"/"+cc.layer(l).name); }catch(e1){} } }
  }
  out.push("usos restantes do recorte antigo: "+(usos.length?usos.join(", "):"nenhum"));

  B.saveFrameToPng(1.6, new File("/tmp/bn_cutout.png"));
  var A=comp("DR 01 ABERTURA"); if(A){ A.saveFrameToPng(5.40, new File("/tmp/bn_take.png")); A.saveFrameToPng(30.20, new File("/tmp/bn_hero.png")); }
  app.project.save();
  var fo=new File("/tmp/ae_bn.txt"); fo.open("w"); fo.write(out.join(String.fromCharCode(10))); fo.close();
 }catch(e){ var fe=new File("/tmp/ae_bn.txt"); fe.open("w"); fe.write("ERRO: "+e.toString()+" linha "+e.line); fe.close(); }
})();
