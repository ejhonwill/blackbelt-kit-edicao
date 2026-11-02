(function(){
  var out=[]; var p=app.project;
  var cc=p.items.addComp("TESTE CARD2",1080,1080,1,2,25); cc.bgColor=[0,0,0];
  cc.layers.addSolid([0,0,0],"FUNDO",1080,1080,1);
  var tl=cc.layers.addText("much much sooner");
  var d=tl.property("Source Text").value;
  d.fontSize=96; d.font="HelveticaNeue-Bold"; d.applyFill=true; d.fillColor=[1,1,1];
  d.justification=ParagraphJustification.CENTER_JUSTIFY;
  tl.property("Source Text").setValue(d);
  try{
    var cr=tl.property("Source Text").value.characterRange(10,16);  // "sooner"
    out.push("characterRange existe");
    cr.fillColor=[0.91,0.38,0.17];
    out.push("cor aplicada no trecho");
    out.push("  leitura de volta="+cr.fillColor.join(","));
  }catch(e){ out.push("characterRange FALHOU: "+e.toString()); }
  try{
    tl.property("Transform").property("Position").setValue([540,540]);
    out.push("posicao ok");
  }catch(e){ out.push("posicao falhou: "+e.toString()); }
  try{
    cc.saveFrameToPng(1, new File("/tmp/ae_card2.png")); out.push("frame exportado");
  }catch(e){ out.push("frame falhou: "+e.toString()); }
  var f=new File("/tmp/ae_card2.txt"); f.open("w"); f.write(out.join("\n")); f.close();
})();
