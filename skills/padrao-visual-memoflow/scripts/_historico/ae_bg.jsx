(function(){
  var out=[]; var p=app.project;
  function comp(n){ for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof CompItem && x.name===n) return x; } return null; }
  function pasta(n){ for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof FolderItem && x.name===n) return x; } return p.items.addFolder(n); }
  var bC=pasta("05 CARTELAS");
  var velho=comp("BG LETTERING"); if(velho) velho.remove();
  var BG=p.items.addComp("BG LETTERING",1080,1080,1,12,25); BG.parentFolder=bC; BG.bgColor=[0,0,0];

  // base quase preta com leve azul
  var base=BG.layers.addSolid([0.02,0.023,0.04],"BASE",1080,1080,1);

  // fita de luz: ruido turbulento esticado + tritone azul + desfoque
  var fita=BG.layers.addSolid([0.5,0.5,0.5],"FITA",1080,1080,1);
  var tn=fita.property("Effects").addProperty("ADBE Turbulent Noise");
  try{ tn.property("Contrast").setValue(190); }catch(e){ out.push("contraste: "+e.toString()); }
  try{ tn.property("Brightness").setValue(-34); }catch(e){}
  try{ tn.property("Complexity").setValue(2); }catch(e){}
  try{ tn.property("Transform").property("Scale Width").setValue(520); }catch(e){ out.push("scale width: "+e.toString()); }
  try{ tn.property("Transform").property("Scale Height").setValue(60); }catch(e){}
  try{ tn.property("Transform").property("Offset Turbulence").setValue([540,540]); }catch(e){}
  var ev=null;
  try{ ev=tn.property("Evolution"); ev.setValueAtTime(0,0); ev.setValueAtTime(12, 140); }catch(e){ out.push("evolution: "+e.toString()); }
  var tri=fita.property("Effects").addProperty("ADBE Tritone");
  try{
    tri.property("Highlights").setValue([0.42,0.40,0.95,1]);   // azul-violeta
    tri.property("Midtones").setValue([0.10,0.11,0.34,1]);
    tri.property("Shadows").setValue([0.015,0.018,0.035,1]);
  }catch(e){ out.push("tritone: "+e.toString()); }
  try{ var bl=fita.property("Effects").addProperty("ADBE Box Blur2"); bl.property("Blur Radius").setValue(38); bl.property("Iterations").setValue(3); }
  catch(e){ try{ var bl2=fita.property("Effects").addProperty("ADBE Fast Blur"); bl2.property("Blurriness").setValue(40); }catch(e2){ out.push("blur: "+e2.toString()); } }
  try{ fita.blendingMode=BlendingMode.ADD; }catch(e){}
  fita.property("Transform").property("Opacity").setValue(72);

  // vinheta suave para o texto respirar
  var vin=BG.layers.addSolid([0,0,0],"VINHETA",1080,1080,1);
  var mk=vin.property("Masks").addProperty("Mask");
  var sh=new Shape(); sh.vertices=[[-160,-160],[1240,-160],[1240,1240],[-160,1240]];
  sh.inTangents=[[0,0],[0,0],[0,0],[0,0]]; sh.outTangents=[[0,0],[0,0],[0,0],[0,0]]; sh.closed=true;
  mk.property("Mask Path").setValue(sh);
  mk.maskMode=MaskMode.SUBTRACT; mk.maskFeather.setValue([420,420]);
  vin.property("Transform").property("Opacity").setValue(55);

  out.push("BG LETTERING criada: "+BG.width+"x"+BG.height+" "+BG.duration+"s, camadas="+BG.numLayers);
  try{ BG.saveFrameToPng(3.0,new File("/tmp/bg_a.png")); BG.saveFrameToPng(8.0,new File("/tmp/bg_b.png")); out.push("prova exportada"); }catch(e){ out.push("prova falhou "+e.toString()); }
  app.project.save();
  var f=new File("/tmp/ae_bg.txt"); f.open("w"); f.write(out.join("\n")); f.close();
})();
