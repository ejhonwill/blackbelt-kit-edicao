(function(){
 try{
  var out=[]; var p=app.project;
  var C=p.items.addComp("__sonda",600,300,1,2,25);
  var t=C.layers.addText("TESTE");
  var dg=t.property("Effects").addProperty("PEDG2");
  out.push("Deep Glow 2 propriedades ("+dg.numProperties+"):");
  for(var i=1;i<=dg.numProperties;i++){
    var pr=dg.property(i);
    var v="";
    try{ v=" = "+pr.value; }catch(e){}
    out.push("  "+i+" ["+pr.matchName+"] "+pr.name+v);
  }
  // fontes
  var TENTA=["HelveticaNeue-CondensedBlack","HelveticaNeue-Bold","Helvetica-Bold","Impact",
             "Montserrat-ExtraBold","Poppins-Bold","Inter-Black","Archivo-Black","Anton-Regular","Roboto-Black"];
  out.push("FONTES:");
  for(var j=0;j<TENTA.length;j++){
    var td=t.property("Source Text").value; td.font=TENTA[j];
    t.property("Source Text").setValue(td);
    var lida=t.property("Source Text").value.font;
    out.push("  "+TENTA[j]+" -> "+lida+(lida===TENTA[j]?"  OK":"  (substituida)"));
  }
  C.remove();
  var fo=new File("/tmp/ae_sonda2.txt"); fo.open("w"); fo.write(out.join(String.fromCharCode(10))); fo.close();
 }catch(err){ var fe=new File("/tmp/ae_sonda2.txt"); fe.open("w"); fe.write("ERRO "+err.toString()); fe.close(); }
})();
