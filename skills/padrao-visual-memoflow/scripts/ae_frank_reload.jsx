(function(){
 try{
  var out=[]; var p=app.project; var it=null;
  for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof FootageItem && x.name==="08_DEPOIMENTO_FRANK_LIPSYNC.mp4") it=x; }
  if(!it) throw new Error("fonte do Frank nao achada");
  var antes=it.duration; it.mainSource.reload();
  var C=null; for(var j=1;j<=p.numItems;j++){ var y=p.item(j); if(y instanceof CompItem && y.name==="DEP 08 FRANK") C=y; }
  if(!C) throw new Error("comp DEP 08 FRANK nao achada");
  C.duration=it.duration;
  for(var l=1;l<=C.numLayers;l++){ if(C.layer(l).name==="VIDEO") C.layer(l).outPoint=it.duration; }
  out.push("Frank: "+antes.toFixed(2)+" -> "+it.duration.toFixed(2)+"s | arquivo "+it.mainSource.file.fsName.split("/").pop());
  app.project.save();
  var f=new File("/tmp/ae_frank.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_frank.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
