(function(){
  var out=[]; var p=app.project;
  var cc=p.items.addComp("T COR",1080,1080,1,2,25); cc.bgColor=[0,0,0];
  cc.layers.addSolid([0,0,0],"F",1080,1080,1);
  var tl=cc.layers.addText("much much sooner");
  var td=tl.property("Source Text").value;
  td.fontSize=92; td.font="HelveticaNeue-Bold"; td.applyFill=true; td.fillColor=[1,1,1];
  td.justification=ParagraphJustification.CENTER_JUSTIFY;
  tl.property("Source Text").setValue(td);
  tl.property("Transform").property("Position").setValue([540,540]);
  // variante 1: applyFill no intervalo
  try{
    var cr=tl.property("Source Text").value.characterRange(10,16);
    cr.applyFill=true; cr.fillColor=[0.91,0.38,0.17];
    out.push("v1 applyFill+fillColor: aplicado");
  }catch(e){ out.push("v1 falhou: "+e.toString()); }
  cc.saveFrameToPng(1,new File("/tmp/cor_v1.png")); out.push("v1 exportado");
  // variante 2: guardar o doc e reescrever
  var tl2=cc.layers.addText("much much sooner");
  var d2=tl2.property("Source Text").value;
  d2.fontSize=92; d2.font="HelveticaNeue-Bold"; d2.applyFill=true; d2.fillColor=[1,1,1];
  d2.justification=ParagraphJustification.CENTER_JUSTIFY;
  tl2.property("Source Text").setValue(d2);
  tl2.property("Transform").property("Position").setValue([540,760]);
  try{
    var st=tl2.property("Source Text");
    var cr2=st.value.characterRange(10,16);
    cr2.applyFill=true; cr2.fillColor=[0.91,0.38,0.17];
    st.setValue(st.value);   // reescreve o documento
    out.push("v2 com setValue de volta: aplicado");
  }catch(e){ out.push("v2 falhou: "+e.toString()); }
  cc.saveFrameToPng(1.5,new File("/tmp/cor_v2.png")); out.push("v2 exportado");
  var f=new File("/tmp/ae_cor.txt"); f.open("w"); f.write(out.join("\n")); f.close();
})();
