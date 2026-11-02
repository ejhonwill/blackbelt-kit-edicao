(function(){
 try{
  var out=[]; var p=app.project; var n=0;
  var ALVO=["MEC_B06.mp4","OFE_B01.mp4","OFE_B02.mp4","OFE_B22.mp4"];
  function tem(x){ for(var i=0;i<ALVO.length;i++) if(ALVO[i]===x) return true; return false; }
  for(var i=1;i<=p.numItems;i++){
    var it=p.item(i);
    if(!(it instanceof FootageItem) || !tem(it.name)) continue;
    try{ it.mainSource.reload(); n++;
         out.push(it.name+" recarregado | dur="+it.duration.toFixed(2)+"s");
    }catch(e){ out.push(it.name+" ERRO: "+e.toString()); }
  }
  out.unshift("fontes recarregadas="+n+" de "+ALVO.length);
  // onde cada um aparece
  function comp(n2){for(var k=1;k<=p.numItems;k++){var x=p.item(k);if(x instanceof CompItem&&x.name===n2)return x;}return null;}
  var cs=["DR 05 MECANISMO","DR 07 OFERTA"];
  for(var c=0;c<cs.length;c++){
    var C=comp(cs[c]); if(!C) continue;
    for(var j=1;j<=C.numLayers;j++){
      var L=C.layer(j);
      try{ if(tem(L.source.name)) out.push("  "+cs[c]+" -> "+L.name+" ["+L.inPoint.toFixed(2)+"-"+L.outPoint.toFixed(2)+"]"); }catch(e2){}
    }
  }
  app.project.save();
  var f=new File("/tmp/ae_rec.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_rec.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
