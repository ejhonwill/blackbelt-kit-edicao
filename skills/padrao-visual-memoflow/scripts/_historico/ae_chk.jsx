(function(){
  var p=app.project; var out=[];
  for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof CompItem && x.name==="BG LETTERING"){ out.push("existe: "+x.width+"x"+x.height+" camadas="+x.numLayers); } }
  if(out.length===0) out.push("BG LETTERING nao existe");
  var f=new File("/tmp/ae_chk.txt"); f.open("w"); f.write(out.join("\n")); f.close();
})();
