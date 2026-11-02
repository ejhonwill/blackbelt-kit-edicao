(function(){
  var out=[]; var p=app.project;
  var VAR=[{c:110,b:6,bl:28,op:100},{c:75,b:24,bl:36,op:100},{c:140,b:-4,bl:22,op:100}];
  for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof CompItem && x.name.indexOf("BGT")===0){ x.remove(); i=0; } }
  for(var v=0;v<VAR.length;v++){
    var s=VAR[v];
    var C=p.items.addComp("BGT"+v,1080,1080,1,6,25); C.bgColor=[0,0,0];
    C.layers.addSolid([0.02,0.023,0.04],"BASE",1080,1080,1);
    var fita=C.layers.addSolid([0.5,0.5,0.5],"FITA",1080,1080,1);
    var tn=fita.property("Effects").addProperty("ADBE AIF Perlin Noise 3D");
    tn.property(4).setValue(s.c); tn.property(5).setValue(s.b);
    tn.property(11).setValue(560); tn.property(12).setValue(58); tn.property(16).setValue(2);
    tn.property(21).setValue(40);
    var tri=fita.property("Effects").addProperty("ADBE Tritone");
    tri.property(1).setValue([0.50,0.47,1.0,1]); tri.property(2).setValue([0.13,0.14,0.45,1]); tri.property(3).setValue([0.01,0.012,0.03,1]);
    var b=fita.property("Effects").addProperty("ADBE Box Blur2"); b.property(1).setValue(s.bl); b.property(2).setValue(3);
    fita.blendingMode=BlendingMode.ADD; fita.property("Transform").property("Opacity").setValue(s.op);
    C.saveFrameToPng(2, new File("/tmp/bgt_"+v+".png"));
    out.push("BGT"+v+" contraste="+s.c+" brilho="+s.b+" blur="+s.bl);
  }
  var f=new File("/tmp/ae_bgt.txt"); f.open("w"); f.write(out.join("\n")); f.close();
})();
