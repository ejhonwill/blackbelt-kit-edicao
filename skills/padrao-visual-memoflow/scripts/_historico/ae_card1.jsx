(function(){
  var out=[]; var p=app.project;
  function passo(n,fn){ try{ fn(); out.push("ok "+n); }catch(e){ out.push("FALHOU "+n+": "+e.toString()); } }
  var cc=null, tl=null;
  passo("criar comp", function(){ cc=p.items.addComp("TESTE CARD",1080,1080,1,2,25); cc.bgColor=[0,0,0]; });
  passo("solido", function(){ cc.layers.addSolid([0,0,0],"FUNDO",1080,1080,1); });
  passo("addText", function(){ tl=cc.layers.addText("teste"); });
  var td=null;
  passo("ler TextDocument", function(){ td=tl.property("Source Text").value; out.push("  fonte atual="+td.font); });
  passo("fontSize", function(){ td.fontSize=96; tl.property("Source Text").setValue(td); });
  passo("fonte HelveticaNeue-Bold", function(){ var d=tl.property("Source Text").value; d.font="HelveticaNeue-Bold"; tl.property("Source Text").setValue(d); out.push("  aplicada="+tl.property("Source Text").value.font); });
  passo("fillColor", function(){ var d=tl.property("Source Text").value; d.applyFill=true; d.fillColor=[1,1,1]; tl.property("Source Text").setValue(d); });
  passo("justification", function(){ var d=tl.property("Source Text").value; d.justification=ParagraphJustification.CENTER_JUSTIFY; tl.property("Source Text").setValue(d); });
  passo("animator", function(){
    var an=tl.property("Text").property("Animators").addProperty("ADBE Text Animator");
    var rs=an.property("ADBE Text Selectors").addProperty("ADBE Text Selector");
    rs.property("ADBE Text Index Start").setValue(0);
    rs.property("ADBE Text Index End").setValue(4);
    an.property("ADBE Text Animator Properties").addProperty("ADBE Text Fill Color").setValue([0.91,0.38,0.17]);
  });
  passo("range type", function(){
    var an=tl.property("Text").property("Animators").property(1);
    an.property("ADBE Text Selectors").property(1).property("ADBE Text Range Type2").setValue(1);
  });
  passo("limpar", function(){ cc.remove(); });
  var f=new File("/tmp/ae_card1.txt"); f.open("w"); f.write(out.join("\n")); f.close();
})();
