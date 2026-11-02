(function(){
  var p=app.project; var out=[]; var C=null;
  for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof CompItem && x.name==="DR 01 ABERTURA") C=x; }
  if(!C) return;
  var T=[21.19,26.26,29.40];
  for(var t=0;t<T.length;t++){
    var tt=T[t]; out.push("== t="+tt);
    var cam=null;
    for(var k=1;k<=C.numLayers;k++){ if(C.layer(k) instanceof CameraLayer) cam=C.layer(k); }
    if(cam){ var v=cam.property("Transform").property("Position").valueAtTime(tt,false);
      out.push("  camera em "+v[0].toFixed(0)+","+v[1].toFixed(0)+","+v[2].toFixed(0)); }
    var n=0;
    for(var q=1;q<=C.numLayers;q++){
      var l=C.layer(q);
      if(l.inPoint<=tt && l.outPoint>tt && (l.name.indexOf("BR ")===0||l.name.indexOf("CARD ")===0)){
        var pv=l.property("Transform").property("Position").value;
        var sv=l.property("Transform").property("Scale").valueAtTime(tt,false);
        out.push("  "+l.name+" 3D="+l.threeDLayer+" pos="+pv[0].toFixed(0)+","+pv[1].toFixed(0)+(pv.length>2?","+pv[2].toFixed(0):"")+" escala="+sv[0].toFixed(1));
        n++;
      }
    }
    out.push("  inserts ativos="+n);
  }
  var f=new File("/tmp/ae_diag2.txt"); f.open("w"); f.write(out.join("\n")); f.close();
})();
