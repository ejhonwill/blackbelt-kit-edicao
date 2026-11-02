(function(){
 var out=[]; var p=app.project;
 function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
 var nomes=["DR 05 MECANISMO","DR 07 OFERTA"];
 for(var k=0;k<nomes.length;k++){
   var C=comp(nomes[k]);
   if(!C){ out.push(nomes[k]+": comp nao existe"); continue; }
   var s=nomes[k]+": "+C.width+"x"+C.height+" dur="+C.duration.toFixed(2)+" fps="+C.frameRate+" camadas="+C.numLayers;
   for(var i=1;i<=C.numLayers;i++){
     var L=C.layer(i);
     s+=" | ["+L.name+"] esc="+L.property("Transform").property("Scale").value[0].toFixed(1);
     try{ s+=" fonte="+L.source.name; }catch(e){}
     s+=" in="+L.inPoint.toFixed(2)+" out="+L.outPoint.toFixed(2);
   }
   out.push(s);
 }
 var f=new File("/tmp/ae_sec.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
})();
