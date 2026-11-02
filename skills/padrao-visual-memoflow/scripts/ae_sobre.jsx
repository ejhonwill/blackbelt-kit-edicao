(function(){
 try{
  var out=[]; var p=app.project;
  var ALVO=["CARD O05","CARD O06","CARD O07","CARD O08","CARD O12","CARD O13"];
  function tem(n){ for(var i=0;i<ALVO.length;i++) if(ALVO[i]===n) return true; return false; }
  var n=0;
  for(var c=1;c<=p.numItems;c++){
    var cc=p.item(c);
    if(!(cc instanceof CompItem) || !tem(cc.name)) continue;
    for(var i=1;i<=cc.numLayers;i++){
      var L=cc.layer(i);
      // 54% deixava o jaleco claro atras do texto branco; 68 traz para o nivel aprovado
      if(L.name==="ESCURECER") L.property("Transform").property("Opacity").setValue(68);
      if(L.name==="FUNDO"){
        for(var f=1;f<=L.property("Effects").numProperties;f++){
          var e=L.property("Effects").property(f);
          if(e.matchName==="ADBE Box Blur2") e.property(1).setValue(20);
        }
      }
    }
    n++; out.push(cc.name);
  }
  out.unshift("cartelas sobre o avatar recalibradas="+n+" (escurecer 54 -> 68, desfoque 16 -> 20)");
  app.project.save();
  var f2=new File("/tmp/ae_sobre.txt"); f2.open("w"); f2.write(out.join(String.fromCharCode(10))); f2.close();
 }catch(e){ var fe=new File("/tmp/ae_sobre.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
