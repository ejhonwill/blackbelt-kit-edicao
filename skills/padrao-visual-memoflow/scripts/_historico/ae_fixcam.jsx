(function(){
  var p=app.project; var out=[]; var C=null;
  for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof CompItem && x.name==="DR 01 ABERTURA") C=x; }
  if(!C) return;
  var cam=null;
  for(var k=1;k<=C.numLayers;k++){ if(C.layer(k) instanceof CameraLayer){ cam=C.layer(k); break; } }
  if(!cam){ out.push("sem camera"); }
  else{
    var poi=cam.property("Transform").property("Point of Interest");
    var pos=cam.property("Transform").property("Position");
    out.push("camera: POI existe="+(poi!=null)+" | chaves pos="+pos.numKeys+" | autoOrient="+cam.autoOrient);
    if(poi){
      // copia as chaves de posicao para o ponto de interesse, no plano z=0
      while(poi.numKeys>0) poi.removeKey(1);
      for(var n=1;n<=pos.numKeys;n++){
        var t=pos.keyTime(n); var v=pos.keyValue(n);
        poi.setValueAtTime(t,[v[0],v[1],0]);
      }
      for(var e=1;e<=poi.numKeys;e++){ try{ poi.setInterpolationTypeAtKey(e,KeyframeInterpolationType.BEZIER,KeyframeInterpolationType.BEZIER); }catch(er){} }
      out.push("POI com "+poi.numKeys+" chaves (agora translada, nao gira)");
    }
    out.push("z da camera="+pos.valueAtTime(0,false)[2].toFixed(1));
  }
  var f=new File("/tmp/ae_fixcam.txt"); f.open("w"); f.write(out.join("\n")); f.close();
})();
