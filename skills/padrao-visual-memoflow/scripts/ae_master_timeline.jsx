(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  function pasta(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof FolderItem&&x.name===n)return x;}return p.items.addFolder(n);}
  // ordem da copy
  var ORDEM=["DR 01 ABERTURA","DEP 02 MARK","DEP 03 ELAINE","DEP 04 ROBERT",
             "DR 05 MECANISMO","DEP 06 MARGARET","DR 07 OFERTA",
             "DEP 08 FRANK","DEP 09 NANCY","DEP 10 GEORGE"];
  var partes=[], total=0, faltou=[];
  for(var i=0;i<ORDEM.length;i++){
    var c=comp(ORDEM[i]);
    if(!c){ faltou.push(ORDEM[i]); continue; }
    partes.push(c); total+=c.duration;
  }
  if(faltou.length) out.push("FALTAM: "+faltou.join(", "));
  var M=comp("UPSELL #1 - DR (MASTER)");
  if(M){ for(var k=M.numLayers;k>=1;k--) M.layer(k).remove(); M.duration=total; }
  else { M=p.items.addComp("UPSELL #1 - DR (MASTER)",1080,1080,1,total,25); M.parentFolder=pasta("03 MASTER"); }
  M.duration=total;
  var t=0;
  for(var j=0;j<partes.length;j++){
    var L=M.layers.add(partes[j]);
    L.startTime=t; L.inPoint=t; L.outPoint=t+partes[j].duration;
    out.push("  "+String(t.toFixed(2))+"  "+partes[j].name+"  ("+partes[j].duration.toFixed(2)+"s)");
    t+=partes[j].duration;
  }
  // primeira parte no topo da pilha, para a ordem de leitura bater com a timeline
  for(var z=M.numLayers;z>=1;z--) M.layer(z).moveToBeginning();
  out.unshift("MASTER: "+partes.length+" partes, "+total.toFixed(2)+"s ("+Math.floor(total/60)+"m"+Math.round(total%60)+"s)");
  app.project.save();
  var f=new File("/tmp/ae_master.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_master.txt"); fe.open("w"); fe.write("ERRO: "+e.toString()+" linha "+e.line); fe.close(); }
})();
