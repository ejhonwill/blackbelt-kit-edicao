(function(){
 var out=[]; var p=app.project;
 function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
 var C=comp("DR 01 ABERTURA");
 var L=[];
 for(var i=1;i<=C.numLayers;i++){
   var z=C.layer(i); if(z.name.indexOf("LEG ")!==0) continue;
   if(z.inPoint>15) continue;
   var t=""; try{ t=z.property("Source Text").value.text; }catch(e){}
   L.push({i:z.inPoint,o:z.outPoint,n:z.name,s:t,on:z.enabled});
 }
 L.sort(function(a,b){return a.i-b.i;});
 for(var k=0;k<L.length;k++)
   out.push("  "+L[k].i.toFixed(2)+" - "+L[k].o.toFixed(2)+"  ["+L[k].n+(L[k].on?"":" DESLIGADA")+"]  \""+L[k].s+"\"");
 out.unshift("legendas ate 15s: "+L.length);
 var f=new File("/tmp/ae_lab.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
})();
