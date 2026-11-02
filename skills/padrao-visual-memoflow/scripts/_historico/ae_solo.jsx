(function(){
  var p=app.project; var C=null; var out=[];
  for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof CompItem && x.name==="DR 01 ABERTURA") C=x; }
  // ordem das 12 primeiras camadas
  for(var k=1;k<=Math.min(12,C.numLayers);k++) out.push("  "+k+": "+C.layer(k).name+(C.layer(k).threeDLayer?" [3D]":""));
  out.push("  ...");
  for(var k2=C.numLayers-4;k2<=C.numLayers;k2++) out.push("  "+k2+": "+C.layer(k2).name+(C.layer(k2).threeDLayer?" [3D]":""));
  C.saveFrameToPng(18.2, new File("/tmp/solo_a.png"));
  C.saveFrameToPng(16.2, new File("/tmp/solo_b.png"));
  var f=new File("/tmp/ae_solo.txt"); f.open("w"); f.write(out.join("\n")); f.close();
})();
