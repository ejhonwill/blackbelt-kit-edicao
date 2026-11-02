(function(){
 var out=[]; var p=app.project;
 function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
 var M=comp("UPSELL #1 - DR (MASTER)");
 if(M){
   out.push("MASTER: "+M.duration.toFixed(2)+"s, "+M.numLayers+" camadas");
   for(var i=1;i<=M.numLayers;i++){
     var L=M.layer(i); var s="  "+L.name;
     try{ s+=" <- "+L.source.name; }catch(e){}
     s+=" ["+L.inPoint.toFixed(2)+"-"+L.outPoint.toFixed(2)+"]";
     out.push(s);
   }
 } else out.push("sem comp MASTER");
 var nomes=["DR 01 ABERTURA","DR 05 MECANISMO","DR 07 OFERTA"];
 for(var k=0;k<nomes.length;k++){
   var C=comp(nomes[k]); if(!C) continue;
   var br=0,cd=0,lg=0,pil=0;
   for(var j=1;j<=C.numLayers;j++){
     var n=C.layer(j).name;
     if(n.indexOf("BR ")===0)br++; else if(n.indexOf("CARD ")===0)cd++;
     else if(n.indexOf("LEG ")===0)lg++; else if(n.indexOf("PIL ")===0)pil++;
   }
   out.push(nomes[k]+": broll="+br+" cartelas="+cd+" legendas="+lg+" pilulas="+pil+" total="+C.numLayers+" motionBlur="+C.motionBlur);
 }
 p.save();
 var f=new File("/tmp/ae_final.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
})();
