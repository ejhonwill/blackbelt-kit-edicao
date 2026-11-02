(function(){
 try{
  var p=app.project; var out=[];
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var C=comp("DR 01 ABERTURA"); var T=18.20;
  for(var i=1;i<=C.numLayers;i++){
    var L=C.layer(i), nm=L.name;
    if(nm.indexOf("LEG ")!==0 && nm.indexOf("PIL ")!==0) continue;
    if(T<L.inPoint || T>L.outPoint) continue;
    var s=i+" ["+nm+"] in="+L.inPoint.toFixed(2)+" out="+L.outPoint.toFixed(2)+" op="+L.property("Transform").property("Opacity").valueAtTime(T,false);
    s+=" ativo="+L.enabled+" pos="+L.property("Transform").property("Position").value;
    if(nm.indexOf("LEG ")===0){
      var td=L.property("Source Text").valueAtTime(T,false);
      s+=' texto="'+td.text+'" corpo='+td.fontSize+' cor=['+td.fillColor+'] fill='+td.applyFill;
      s+=" efeitos="+L.property("Effects").numProperties;
      var r=L.sourceRectAtTime(T,false); s+=" rect(w="+r.width.toFixed(0)+",h="+r.height.toFixed(0)+")";
    }
    out.push(s);
  }
  out.unshift("em t=18.20 -> "+out.length+" camadas de legenda");
  var f=new File("/tmp/ae_l18.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_l18.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
