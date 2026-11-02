(function(){
 var out=[]; var p=app.project;
 function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
 var M=comp("UPSELL #1 - DR (MASTER)");
 if(!M){ var fe=new File("/tmp/ae_mchk.txt"); fe.open("w"); fe.write("MASTER nao existe"); fe.close(); return; }
 out.push("MASTER: "+M.width+"x"+M.height+" | "+M.duration.toFixed(2)+"s | "+M.frameRate+" fps | "+M.numLayers+" camadas");
 var t=0, buracos=[];
 var L=[];
 for(var i=1;i<=M.numLayers;i++) L.push(M.layer(i));
 L.sort(function(a,b){return a.inPoint-b.inPoint;});
 for(var k=0;k<L.length;k++){
   var z=L[k]; var tipo="";
   try{ tipo = (z.source instanceof CompItem) ? "composicao" : "midia"; }catch(e){ tipo="?"; }
   out.push("  "+z.inPoint.toFixed(2)+" - "+z.outPoint.toFixed(2)+"  "+z.name+"  ["+tipo+"]");
   if(z.inPoint > t+0.02) buracos.push(t.toFixed(2)+"-"+z.inPoint.toFixed(2));
   t=Math.max(t,z.outPoint);
 }
 out.push(buracos.length? ("BURACOS: "+buracos.join(", ")) : "sem buraco entre as partes");
 out.push("cobre ate "+t.toFixed(2)+"s de "+M.duration.toFixed(2)+"s");
 var f=new File("/tmp/ae_mchk.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
})();
