(function(){
  var p=app.project; var out=[]; var C=null;
  for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof CompItem && x.name==="DR 01 ABERTURA") C=x; }
  if(!C) return;
  var cam=null; for(var k=1;k<=C.numLayers;k++){ if(C.layer(k) instanceof CameraLayer) cam=C.layer(k); }
  if(cam){
    out.push("camera indice="+cam.index+" zoom="+cam.property("Camera Options").property("Zoom").value.toFixed(1));
    out.push("comp renderer="+C.renderer);
  }
  var T=[16.2, 18.2, 23.5, 30.5, 34.4];
  for(var t=0;t<T.length;t++){ try{ C.saveFrameToPng(T[t], new File("/tmp/mid_"+t+".png")); }catch(e){ out.push("x "+T[t]); } }
  var f=new File("/tmp/ae_mid.txt"); f.open("w"); f.write(out.join("\n")); f.close();
})();
