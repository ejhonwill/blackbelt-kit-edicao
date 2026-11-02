(function(){
 try{
  var p=app.project; var n=0;
  function comp(x){for(var i=1;i<=p.numItems;i++){var z=p.item(i);if(z instanceof CompItem&&z.name===x)return z;}return null;}
  var C=comp("DR 01 ABERTURA");
  for(var k=C.numLayers;k>=1;k--){ var nm=C.layer(k).name;
    if(nm.indexOf("LEG ")===0||nm.indexOf("PIL ")===0||nm==="CAM LET"){ C.layer(k).remove(); n++; } }
  var f=new File("/tmp/ae_volta.txt"); f.open("w"); f.write("removidas="+n+" restam="+C.numLayers); f.close();
 }catch(e){ var fe=new File("/tmp/ae_volta.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
