(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var B=comp("MEMOFLOW_BOTTLE_CUTOUT");
  if(!B) throw new Error("sem MEMOFLOW_BOTTLE_CUTOUT");
  var tirou=0;
  for(var k=B.numLayers;k>=1;k--){
    var n=B.layer(k).name;
    // o brilho tinha borda dura e apagava o rotulo; o matte dele fica sem uso
    if(n==="SWEEP"||n==="FRASCO MATTE"){ B.layer(k).remove(); tirou++; }
  }
  // light wrap mais discreto: so um fio de luz na borda do vidro
  for(var i=1;i<=B.numLayers;i++){
    if(B.layer(i).name==="LIGHT WRAP") B.layer(i).property("Transform").property("Opacity").setValue(12);
  }
  out.push("camadas removidas="+tirou+" | light wrap a 12%");
  out.push("restam:");
  for(var j=1;j<=B.numLayers;j++) out.push("  "+j+" "+B.layer(j).name);
  B.saveFrameToPng(1.6, new File("/tmp/iso_ok.png"));
  app.project.save();
  var f=new File("/tmp/ae_sw.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_sw.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
