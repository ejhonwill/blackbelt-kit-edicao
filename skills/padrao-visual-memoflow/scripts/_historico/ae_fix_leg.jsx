(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var C=comp("DR 01 ABERTURA");
  var claras=0, nf=0;
  for(var i=1;i<=C.numLayers;i++){
    var L=C.layer(i); if(L.name.indexOf("LEG ")!==0) continue;
    var cor=L.property("Source Text").value.fillColor;
    if(cor && cor[0]>0.5) claras++;
    // Preenchimento como efeito: nao depende do TextDocument aceitar a cor
    for(var f=L.property("Effects").numProperties;f>=1;f--){
      if(L.property("Effects").property(f).matchName==="ADBE Fill") L.property("Effects").property(f).remove();
    }
    var fi=L.property("Effects").addProperty("ADBE Fill");
    var posto=false;
    for(var k=1;k<=fi.numProperties;k++){
      var pr=fi.property(k);
      if(pr.propertyValueType===PropertyValueType.COLOR){ pr.setValue([0.07,0.07,0.09,1]); posto=true; break; }
    }
    if(!posto) out.push("cor nao aplicada em "+L.name);
    nf++;
  }
  out.unshift("legendas que tinham ficado claras="+claras+" | preenchimento aplicado em "+nf);

  // frasco: brilho contido para o rotulo ficar legivel
  var B=comp("MEMOFLOW_BOTTLE_CUTOUT");
  if(B){
    for(var q=1;q<=B.numLayers;q++){
      var Z=B.layer(q);
      if(Z.name==="LIGHT WRAP") Z.property("Transform").property("Opacity").setValue(16);
      if(Z.name==="SWEEP")      Z.property("Transform").property("Opacity").setValue(13);
      if(Z.name==="GLOW FUNDO") Z.property("Transform").property("Opacity").setValue(44);
    }
    out.push("frasco: light wrap 16%, sweep 13%, glow 44%");
  }
  app.project.save();
  var f2=new File("/tmp/ae_fleg.txt"); f2.open("w"); f2.write(out.join(String.fromCharCode(10))); f2.close();
 }catch(e){ var fe=new File("/tmp/ae_fleg.txt"); fe.open("w"); fe.write("ERRO "+e.toString()+" linha "+e.line); fe.close(); }
})();
