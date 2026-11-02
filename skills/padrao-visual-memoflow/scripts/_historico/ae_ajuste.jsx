(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}

  // fita mais baixa e um veu escuro atras do texto
  var BG=comp("BG LETTERING");
  for(var i=1;i<=BG.numLayers;i++){
    var l=BG.layer(i);
    if(l.name==="FITA 3D"){
      l.property("Transform").property("Position").setValue([540,742]);
      l.property("Transform").property("Opacity").setValue(86);
    }
    if(l.name==="VEU") { l.remove(); i--; }
  }
  var veu=BG.layers.addSolid([0,0,0],"VEU",1080,1080,1);
  var rp=veu.property("Effects").addProperty("ADBE Ramp");
  rp.property(1).setValue([540,300]); rp.property(2).setValue([0,0,0,1]);
  rp.property(3).setValue([540,900]); rp.property(4).setValue([0,0,0,0]);
  veu.property("Transform").property("Opacity").setValue(72);
  // o veu fica acima da fita, abaixo da vinheta
  for(var q=1;q<=BG.numLayers;q++){ if(BG.layer(q).name==="FITA 3D"){ veu.moveBefore(BG.layer(q)); break; } }
  out.push("fundo: fita em y=742, veu 72%");

  // avanco da camera mais contido
  var n=0;
  for(var c=1;c<=p.numItems;c++){
    var cc=p.item(c);
    if(!(cc instanceof CompItem) || cc.name.indexOf("CARD ")!==0) continue;
    for(var k=1;k<=cc.numLayers;k++){
      var t=cc.layer(k); if(t.name.indexOf("TXT ")!==0) continue;
      var pp=t.property("Transform").property("Position");
      if(pp.numKeys<2) continue;
      var v0=pp.keyValue(1), v1=pp.keyValue(pp.numKeys);
      pp.setValueAtTime(pp.keyTime(1),[v0[0],v0[1],90]);
      pp.setValueAtTime(pp.keyTime(pp.numKeys),[v1[0],v1[1],-360]);
      n++;
    }
  }
  out.push("camadas de texto reajustadas="+n);
  app.project.save();
  var f=new File("/tmp/ae_aj.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_aj.txt"); fe.open("w"); fe.write("ERRO "+e.toString()+" linha "+e.line); fe.close(); }
})();
