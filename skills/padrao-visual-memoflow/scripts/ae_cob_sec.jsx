(function(){
 var p=app.project; var out=[];
 function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
 var nomes=["DR 05 MECANISMO","DR 07 OFERTA"];
 for(var k=0;k<nomes.length;k++){
   var C=comp(nomes[k]); if(!C) continue;
   out.push("#COMP "+nomes[k]+" dur="+C.duration.toFixed(3));
   for(var i=1;i<=C.numLayers;i++){
     var L=C.layer(i), n=L.name;
     if(!(n.indexOf("BR ")===0||n.indexOf("CARD ")===0)) continue;
     var op=L.property("Transform").property("Opacity"); var ks=[];
     for(var j=1;j<=op.numKeys;j++) ks.push(op.keyTime(j).toFixed(3)+"@"+Math.round(op.keyValue(j)));
     out.push([n,L.inPoint.toFixed(3),L.outPoint.toFixed(3),ks.join("/")].join("|"));
   }
 }
 var f=new File("/tmp/ae_cobsec.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
})();
