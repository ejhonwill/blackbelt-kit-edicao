(function(){
  var p=app.project; var out=[]; var C=null;
  for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof CompItem && x.name==="DR 01 ABERTURA") C=x; }
  var alvos=[{n:"CARD T01",i:17.02,o:19.50,e:"C",s:"B"},{n:"CARD T05",i:39.50,o:41.44,e:"D",s:"C"}];
  var W=1080,H=1080,TR=0.20;
  function desloc(d){ if(d==="D") return [-W,0]; if(d==="C") return [0,H]; if(d==="B") return [0,-H]; return [0,0]; }
  for(var a=0;a<alvos.length;a++){
    var d=alvos[a]; var l=null;
    for(var q=1;q<=C.numLayers;q++){ if(C.layer(q).name===d.n){ l=C.layer(q); break; } }
    if(!l){ out.push("ausente "+d.n); continue; }
    out.push(d.n+" in="+l.inPoint.toFixed(2)+" out="+l.outPoint.toFixed(2)+" start="+l.startTime.toFixed(2));
    l.threeDLayer=false;
    var pp=l.property("Transform").property("Position");
    while(pp.numKeys>0) pp.removeKey(1);
    var de=desloc(d.e);
    pp.setValueAtTime(Math.max(0,l.inPoint-TR),[540-de[0],540-de[1]]);
    pp.setValueAtTime(l.inPoint,[540,540]);
    var ds=desloc(d.s);
    pp.setValueAtTime(l.outPoint-TR,[540,540]);
    pp.setValueAtTime(l.outPoint,[540+ds[0],540+ds[1]]);
    for(var e=1;e<=pp.numKeys;e++){ try{ pp.setInterpolationTypeAtKey(e,KeyframeInterpolationType.BEZIER,KeyframeInterpolationType.BEZIER); }catch(er){} }
    out.push("  corrigido, chaves="+pp.numKeys);
  }
  // confere que ninguem ficou 3D
  var t3=0; for(var z=1;z<=C.numLayers;z++){ if(C.layer(z).threeDLayer) t3++; }
  out.push("camadas ainda 3D="+t3);
  app.project.save();
  var f=new File("/tmp/ae_fix2.txt"); f.open("w"); f.write(out.join("\n")); f.close();
})();
