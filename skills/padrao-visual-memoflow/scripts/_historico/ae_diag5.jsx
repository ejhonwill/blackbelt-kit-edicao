(function(){
  var p=app.project; var out=[]; var C=null;
  for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof CompItem && x.name==="DR 01 ABERTURA") C=x; }
  var cams=[];
  for(var k=1;k<=C.numLayers;k++){ if(C.layer(k) instanceof CameraLayer) cams.push(k+":"+C.layer(k).name); }
  out.push("cameras na comp: "+cams.length+" -> "+cams.join(", "));
  // conta camadas CARD duplicadas
  var cont={};
  for(var q=1;q<=C.numLayers;q++){ var n=C.layer(q).name; if(n.indexOf("CARD ")===0||n.indexOf("BR ")===0) cont[n]=(cont[n]||0)+1; }
  var dup=[]; for(var kk in cont){ if(cont[kk]>1) dup.push(kk+"x"+cont[kk]); }
  out.push("duplicadas: "+(dup.length?dup.join(", "):"nenhuma"));
  // posicao de TODAS as CARD
  for(var z=1;z<=C.numLayers;z++){
    var l=C.layer(z);
    if(l.name.indexOf("CARD ")===0){
      var pv=l.property("Transform").property("Position").value;
      out.push("  "+l.name+" in="+l.inPoint.toFixed(2)+" pos="+pv[0].toFixed(0)+","+pv[1].toFixed(0));
    }
  }
  var f=new File("/tmp/ae_diag5.txt"); f.open("w"); f.write(out.join("\n")); f.close();
})();
