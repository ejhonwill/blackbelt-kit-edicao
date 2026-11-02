(function(){
 try{
  var p=app.project; var out=[];
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var C=comp("DR 01 ABERTURA");
  out.push("COMP dur="+C.duration.toFixed(3)+" fps="+C.frameRate+" camadas="+C.numLayers);
  for(var i=1;i<=C.numLayers;i++){
    var l=C.layer(i), n=l.name;
    if(!(n.indexOf("BR ")===0||n.indexOf("CARD ")===0||n.indexOf("PROD")===0||n==="SELO FRASCO")) continue;
    var op=l.property("Transform").property("Opacity");
    var ks=[];
    for(var k=1;k<=op.numKeys;k++) ks.push(op.keyTime(k).toFixed(3)+"@"+Math.round(op.keyValue(k)));
    var sc=l.property("Transform").property("Scale").value;
    out.push([i,n,l.inPoint.toFixed(3),l.outPoint.toFixed(3),l.startTime.toFixed(3),
              Math.round(sc[0]),ks.join("/")].join("|"));
  }
  var f=new File("/tmp/ae_cob.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_cob.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
