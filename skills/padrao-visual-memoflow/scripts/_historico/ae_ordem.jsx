(function(){
 try{
  var p=app.project; var out=[];
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var C=comp("DR 01 ABERTURA");
  function topo(pre){ for(var z=C.numLayers;z>=1;z--){ if(C.layer(z).name.indexOf(pre)===0) C.layer(z).moveToBeginning(); } }
  // a pilula sobe primeiro; o texto sobe depois e fica por cima dela
  topo("PIL "); topo("LEG ");
  // confere
  var iL=0, iP=0;
  for(var i=1;i<=C.numLayers;i++){
    var n=C.layer(i).name;
    if(!iL && n.indexOf("LEG ")===0) iL=i;
    if(!iP && n.indexOf("PIL ")===0) iP=i;
  }
  out.push("primeiro LEG no indice "+iL+" | primeiro PIL no indice "+iP+" | texto acima da pilula: "+(iL<iP));
  out.push("camadas="+C.numLayers);
  app.project.save();
  var f=new File("/tmp/ae_ord.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_ord.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
