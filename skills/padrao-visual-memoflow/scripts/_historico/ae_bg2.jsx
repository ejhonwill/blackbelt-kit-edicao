(function(){
  var out=[]; var p=app.project;
  function passo(n,fn){ try{ fn(); out.push("ok "+n); }catch(e){ out.push("FALHOU "+n+": "+e.toString()); } }
  function comp(n){ for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof CompItem && x.name===n) return x; } return null; }
  function pasta(n){ for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof FolderItem && x.name===n) return x; } return p.items.addFolder(n); }
  var v=comp("BG LETTERING"); if(v) v.remove();
  var BG=p.items.addComp("BG LETTERING",1080,1080,1,12,25); BG.parentFolder=pasta("05 CARTELAS"); BG.bgColor=[0,0,0];
  var base,fita,tn,tri;
  passo("base", function(){ base=BG.layers.addSolid([0.02,0.023,0.04],"BASE",1080,1080,1); });
  passo("solido fita", function(){ fita=BG.layers.addSolid([0.5,0.5,0.5],"FITA",1080,1080,1); });
  passo("turbulent noise", function(){ tn=fita.property("Effects").addProperty("ADBE Turbulent Noise"); });
  passo("contraste", function(){ tn.property("Contrast").setValue(190); });
  passo("brilho", function(){ tn.property("Brightness").setValue(-34); });
  passo("complexidade", function(){ tn.property("Complexity").setValue(2); });
  passo("scale width", function(){ tn.property("Transform").property("Scale Width").setValue(520); });
  passo("scale height", function(){ tn.property("Transform").property("Scale Height").setValue(60); });
  passo("evolution", function(){ var ev=tn.property("Evolution"); ev.setValueAtTime(0,0); ev.setValueAtTime(12,140); });
  passo("tritone", function(){ tri=fita.property("Effects").addProperty("ADBE Tritone"); });
  passo("cores tritone", function(){
    tri.property("Highlights").setValue([0.42,0.40,0.95,1]);
    tri.property("Midtones").setValue([0.10,0.11,0.34,1]);
    tri.property("Shadows").setValue([0.015,0.018,0.035,1]);
  });
  passo("blur", function(){ var b=fita.property("Effects").addProperty("ADBE Box Blur2"); b.property("Blur Radius").setValue(38); b.property("Iterations").setValue(3); });
  passo("blend add", function(){ fita.blendingMode=BlendingMode.ADD; });
  passo("opacidade fita", function(){ fita.property("Transform").property("Opacity").setValue(72); });
  passo("vinheta", function(){
    var vin=BG.layers.addSolid([0,0,0],"VINHETA",1080,1080,1);
    var ef=vin.property("Effects").addProperty("ADBE Ramp");
    ef.property("Start of Ramp").setValue([540,540]);
    ef.property("End of Ramp").setValue([540,1160]);
    ef.property("Start Color").setValue([0,0,0,0]);
    ef.property("End Color").setValue([0,0,0,1]);
    ef.property("Ramp Shape").setValue(2);   // radial
    vin.property("Transform").property("Opacity").setValue(60);
  });
  passo("prova", function(){ BG.saveFrameToPng(3.0,new File("/tmp/bg_a.png")); BG.saveFrameToPng(8.0,new File("/tmp/bg_b.png")); });
  out.push("camadas="+BG.numLayers);
  app.project.save();
  var f=new File("/tmp/ae_bg2.txt"); f.open("w"); f.write(out.join("\n")); f.close();
})();
