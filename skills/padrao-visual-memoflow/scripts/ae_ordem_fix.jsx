(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var nomes=["DR 01 ABERTURA","DEP 02 MARK","DEP 03 ELAINE","DEP 04 ROBERT","DR 05 MECANISMO",
             "DEP 06 MARGARET","DR 07 OFERTA","DEP 08 FRANK","DEP 09 NANCY","DEP 10 GEORGE"];
  var mov=0;
  for(var k=0;k<nomes.length;k++){
    var C=comp(nomes[k]); if(!C) continue;
    // um par por vez: mover em lote embaralha, porque os indices andam durante o laco
    for(var j=1;j<=400;j++){
      var leg=null, pil=null;
      for(var i=1;i<=C.numLayers;i++){
        var nm=C.layer(i).name;
        if(nm==="LEG "+j) leg=C.layer(i); else if(nm==="PIL "+j) pil=C.layer(i);
      }
      if(!leg||!pil) continue;
      leg.moveBefore(pil); mov++;
    }
  }
  // prova
  var totPar=0, ruim=0, det=[];
  for(var k2=0;k2<nomes.length;k2++){
    var C2=comp(nomes[k2]); if(!C2) continue;
    var idx={};
    for(var i2=1;i2<=C2.numLayers;i2++) idx[C2.layer(i2).name]=i2;
    var r=0, pr=0;
    for(var j2=1;j2<=400;j2++){
      if(idx["LEG "+j2]===undefined||idx["PIL "+j2]===undefined) continue;
      pr++; if(idx["LEG "+j2]>idx["PIL "+j2]) r++;
    }
    totPar+=pr; ruim+=r;
    if(r) det.push(nomes[k2]+"="+r);
  }
  out.push("pares reordenados="+mov+" | pares="+totPar+" | invertidos restantes="+ruim+(det.length?(" ("+det.join(", ")+")"):""));
  app.project.save();
  var f=new File("/tmp/ae_ordfix.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_ordfix.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
