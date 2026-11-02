(function(){
  var out=[]; var p=app.project;
  function passo(n,fn){ try{ fn(); out.push("ok "+n); }catch(e){ out.push("FALHOU "+n+": "+e.toString()); } }
  function comp(n){ for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof CompItem && x.name===n) return x; } return null; }
  function pasta(n){ for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof FolderItem && x.name===n) return x; } return p.items.addFolder(n); }
  var v=comp("BG LETTERING"); if(v) v.remove();
  var BG=p.items.addComp("BG LETTERING",1080,1080,1,14,25); BG.parentFolder=pasta("05 CARTELAS"); BG.bgColor=[0,0,0];
  BG.layers.addSolid([0.02,0.023,0.04],"BASE",1080,1080,1);
  var fita=BG.layers.addSolid([0.5,0.5,0.5],"FITA",1080,1080,1);
  var tn;
  passo("ruido", function(){ tn=fita.property("Effects").addProperty("ADBE AIF Perlin Noise 3D"); });
  passo("contraste", function(){ tn.property(4).setValue(200); });
  passo("brilho",    function(){ tn.property(5).setValue(-38); });
  passo("largura",   function(){ tn.property(11).setValue(560); });
  passo("altura",    function(){ tn.property(12).setValue(58); });
  passo("complexidade", function(){ tn.property(16).setValue(2); });
  passo("evolucao",  function(){ var ev=tn.property(21); ev.setValueAtTime(0,0); ev.setValueAtTime(14,150); });
  var tri;
  passo("tritone", function(){ tri=fita.property("Effects").addProperty("ADBE Tritone"); });
  passo("realces",   function(){ tri.property(1).setValue([0.44,0.42,0.96,1]); });
  passo("meiostons", function(){ tri.property(2).setValue([0.10,0.11,0.36,1]); });
  passo("sombras",   function(){ tri.property(3).setValue([0.015,0.018,0.035,1]); });
  passo("desfoque",  function(){ var b=fita.property("Effects").addProperty("ADBE Box Blur2"); b.property(1).setValue(42); b.property(2).setValue(3); });
  passo("mesclagem", function(){ fita.blendingMode=BlendingMode.ADD; fita.property("Transform").property("Opacity").setValue(74); });
  passo("vinheta", function(){
    var vin=BG.layers.addSolid([0,0,0],"VINHETA",1080,1080,1);
    var r=vin.property("Effects").addProperty("ADBE Ramp");
    r.property(1).setValue([540,540]); r.property(3).setValue([540,1180]);
    r.property(2).setValue([0,0,0,0]); r.property(4).setValue([0,0,0,1]);
    r.property(5).setValue(2);
    vin.property("Transform").property("Opacity").setValue(58);
  });
  passo("prova", function(){ BG.saveFrameToPng(3,new File("/tmp/bg_a.png")); BG.saveFrameToPng(9,new File("/tmp/bg_b.png")); });
  out.push("camadas="+BG.numLayers);
  app.project.save();
  var f=new File("/tmp/ae_bg3.txt"); f.open("w"); f.write(out.join("\n")); f.close();
})();
