(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var nomes=["DR 01 ABERTURA","DEP 02 MARK","DEP 03 ELAINE","DEP 04 ROBERT","DR 05 MECANISMO",
             "DEP 06 MARGARET","DR 07 OFERTA","DEP 08 FRANK","DEP 09 NANCY","DEP 10 GEORGE"];
  for(var k=0;k<nomes.length;k++){
    var C=comp(nomes[k]); if(!C){ out.push(nomes[k]+" AUSENTE"); continue; }
    var comAudio=[], mudos=0;
    for(var i=1;i<=C.numLayers;i++){
      var L=C.layer(i);
      if(!L.hasAudio) continue;
      if(L.audioEnabled) comAudio.push(L.name); else mudos++;
    }
    out.push(nomes[k]+": com audio ["+comAudio.join(", ")+"] | mudos="+mudos);
  }
  // modelos de saida
  var M=comp("UPSELL #1 - DR (MASTER)");
  var rq=app.project.renderQueue;
  var it=rq.items.add(M);
  var om=it.outputModule(1);
  out.push("modelos de saida: "+om.templates.join(" | "));
  out.push("modelos de render: "+it.templates.join(" | "));
  it.remove();
  var f=new File("/tmp/ae_aud.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_aud.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
