(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var C=comp("DR 01 ABERTURA");
  // cada texto vai para logo acima da SUA pilula, um par por vez
  var mov=0;
  for(var k=1;k<=200;k++){
    var leg=null, pil=null;
    for(var i=1;i<=C.numLayers;i++){
      var nm=C.layer(i).name;
      if(nm==="LEG "+k) leg=C.layer(i);
      else if(nm==="PIL "+k) pil=C.layer(i);
    }
    if(!leg||!pil) continue;
    leg.moveBefore(pil); mov++;
  }
  // confere os 57 pares
  var idx={}, ruim=[];
  for(var j=1;j<=C.numLayers;j++) idx[C.layer(j).name]=j;
  for(var k2=1;k2<=200;k2++){
    if(idx["LEG "+k2]===undefined||idx["PIL "+k2]===undefined) continue;
    if(idx["LEG "+k2]>idx["PIL "+k2]) ruim.push(k2);
  }
  out.push("pares reordenados="+mov+" | invertidos que sobraram="+ruim.length+(ruim.length?(" -> "+ruim.join(",")):""));
  app.project.save();
  var f=new File("/tmp/ae_par.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_par.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
