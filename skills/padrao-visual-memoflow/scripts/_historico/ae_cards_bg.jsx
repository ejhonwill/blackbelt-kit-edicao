(function(){
  var out=[]; var p=app.project;
  function comp(n){ for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof CompItem && x.name===n) return x; } return null; }
  var BG=comp("BG LETTERING");
  if(!BG){ var fe=new File("/tmp/ae_cbg.txt"); fe.open("w"); fe.write("sem BG"); fe.close(); return; }
  var n=0;
  for(var i=1;i<=p.numItems;i++){
    var C=p.item(i);
    if(!(C instanceof CompItem) || C.name.indexOf("CARD ")!==0) continue;
    var nomes=[];
    for(var k=C.numLayers;k>=1;k--){
      var nm=C.layer(k).name; nomes.push(nm);
      if(nm==="FUNDO"||nm==="BGL") C.layer(k).remove();
    }
    var L=C.layers.add(BG);
    L.name="BGL";
    L.startTime=-(i%7)*1.3;              // cada cartela pega um trecho diferente da aurora
    L.property("Transform").property("Scale").setValue([118,118]);
    L.property("Transform").property("Opacity").setValue(100);
    L.moveToEnd();
    n++; out.push(C.name+" ["+nomes.join("|")+"]");
  }
  app.project.save();
  var f=new File("/tmp/ae_cbg.txt"); f.open("w"); f.write("cartelas="+n+"\n"+out.join("\n")); f.close();
})();
