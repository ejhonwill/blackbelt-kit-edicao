(function(){
  var p=app.project; var out=[]; var C=null;
  for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof CompItem && x.name==="DR 01 ABERTURA") C=x; }
  var cam=null; for(var k=1;k<=C.numLayers;k++){ if(C.layer(k) instanceof CameraLayer) cam=C.layer(k); }
  var cp=cam.property("Transform").property("Position");
  out.push("chaves da camera (primeiras 10):");
  for(var n=1;n<=Math.min(10,cp.numKeys);n++){
    var v=cp.keyValue(n); out.push("  k"+n+" t="+cp.keyTime(n).toFixed(2)+" -> "+v[0].toFixed(0)+","+v[1].toFixed(0));
  }
  var T=[16.2,18.2,23.5];
  for(var t=0;t<T.length;t++){
    var tt=T[t]; var v=cp.valueAtTime(tt,false);
    out.push("t="+tt+" camera="+v[0].toFixed(0)+","+v[1].toFixed(0));
    for(var q=1;q<=C.numLayers;q++){
      var l=C.layer(q);
      if(l.inPoint<=tt && l.outPoint>tt && (l.name.indexOf("BR ")===0||l.name.indexOf("CARD ")===0)){
        var pv=l.property("Transform").property("Position").value;
        out.push("   ativo "+l.name+" em "+pv[0].toFixed(0)+","+pv[1].toFixed(0));
      }
    }
  }
  var f=new File("/tmp/ae_diag3.txt"); f.open("w"); f.write(out.join("\n")); f.close();
})();
