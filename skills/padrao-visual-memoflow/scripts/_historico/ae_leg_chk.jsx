(function(){
 try{
  var p=app.project; var out=[];
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var C=comp("DR 01 ABERTURA"); var n=0, fora=[];
  for(var i=1;i<=C.numLayers;i++){
    var L=C.layer(i), nm=L.name;
    if(nm.indexOf("LEG ")!==0 && nm.indexOf("PIL ")!==0) continue;
    n++;
    var v=L.property("Transform").property("Position").value;
    if(L.inPoint<73.5 && L.outPoint<73.5) continue;
    fora.push(nm+" y="+Math.round(v[1])+" ["+L.inPoint.toFixed(2)+"-"+L.outPoint.toFixed(2)+"]");
  }
  out.push("camadas de legenda="+n);
  out.push("no fim: "+fora.join(" | "));
  var f=new File("/tmp/ae_lchk.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_lchk.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
