(function(){
 try{
  var p=app.project; var out=[];
  var C=p.items.addComp("__sel",600,300,1,2,25);
  var t=C.layers.addText("um dois tres");
  var an=t.property("Text").property("Animators").addProperty("ADBE Text Animator");
  an.property("ADBE Text Animator Properties").addProperty("ADBE Text Opacity").setValue(0);
  var sel=an.property("ADBE Text Selectors").addProperty("ADBE Text Selector");
  out.push("seletor ("+sel.numProperties+"):");
  for(var i=1;i<=sel.numProperties;i++){
    var pr=sel.property(i); var v="";
    try{ v=" = "+pr.value; }catch(e){}
    out.push("  "+i+" ["+pr.matchName+"] "+pr.name+v);
  }
  C.remove();
  var f=new File("/tmp/ae_sel.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(err){ var fe=new File("/tmp/ae_sel.txt"); fe.open("w"); fe.write("ERRO "+err.toString()); fe.close(); }
})();
