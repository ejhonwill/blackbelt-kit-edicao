(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}

  // ---- cartelas: fundo preto, com a fita so como respiro ----
  var nc=0;
  for(var c=1;c<=p.numItems;c++){
    var cc=p.item(c);
    if(!(cc instanceof CompItem) || cc.name.indexOf("CARD ")!==0) continue;
    // preto opaco no fundo: sem ele a cartela fica translucida e o medico volta a aparecer
    var preto=null;
    for(var k=cc.numLayers;k>=1;k--){ if(cc.layer(k).name==="PRETO CARTELA") preto=cc.layer(k); }
    if(!preto){ preto=cc.layers.addSolid([0,0,0],"PRETO CARTELA",1080,1080,1); }
    preto.moveToEnd();
    preto.startTime=0; preto.inPoint=0; preto.outPoint=cc.duration;
    preto.property("Transform").property("Opacity").setValue(100);
    for(var q=1;q<=cc.numLayers;q++){
      var L=cc.layer(q);
      if(L.name==="BGL"){ L.property("Transform").property("Opacity").setValue(22); }
    }
    nc++;
  }
  out.push("cartelas com fundo preto="+nc);

  // ---- legenda corrida: pilula branca, texto escuro ----
  var C=comp("DR 01 ABERTURA");
  var np=0, nl=0;
  for(var i=1;i<=C.numLayers;i++){
    var L=C.layer(i), nm=L.name;
    if(nm.indexOf("PIL ")===0){
      var g=L.property("Contents").property(1).property("Contents");
      for(var f=1;f<=g.numProperties;f++){
        var pr=g.property(f);
        if(pr.matchName==="ADBE Vector Graphic - Fill"){
          pr.property("ADBE Vector Fill Color").setValue([1,1,1,1]); np++;
        }
      }
      L.property("Transform").property("Opacity").setValue(94);
    } else if(nm.indexOf("LEG ")===0){
      var td=L.property("Source Text").value;
      td.applyFill=true; td.fillColor=[0.07,0.07,0.09];
      L.property("Source Text").setValue(td); nl++;
    }
  }
  out.push("pilulas brancas="+np+" | textos escuros="+nl);
  app.project.save();
  var f2=new File("/tmp/ae_ctt.txt"); f2.open("w"); f2.write(out.join(String.fromCharCode(10))); f2.close();
 }catch(e){ var fe=new File("/tmp/ae_ctt.txt"); fe.open("w"); fe.write("ERRO "+e.toString()+" linha "+e.line); fe.close(); }
})();
