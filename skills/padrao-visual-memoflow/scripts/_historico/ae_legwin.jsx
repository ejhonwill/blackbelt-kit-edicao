(function(){
 var out=[]; var p=app.project;
 function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
 var C=comp("DR 01 ABERTURA");
 var L=[];
 for(var i=1;i<=C.numLayers;i++){
   var z=C.layer(i); if(z.name.indexOf("LEG ")!==0) continue;
   if(z.outPoint<0.5 || z.inPoint>9.5) continue;
   var s="";
   try{ s=z.property("Source Text").value.text; }catch(e){}
   L.push({i:z.inPoint,o:z.outPoint,n:z.name,s:s,idx:i});
 }
 L.sort(function(a,b){return a.i-b.i;});
 for(var k=0;k<L.length;k++) out.push("  %s".replace("%s", L[k].n+" ["+L[k].i.toFixed(2)+"-"+L[k].o.toFixed(2)+"] \""+L[k].s+"\""));
 out.unshift("legendas ate 9,5s: "+L.length);
 // buracos
 var bur=[]; var t=0.67;
 for(var j=0;j<L.length;j++){ if(L[j].i>t+0.25) bur.push(t.toFixed(2)+"-"+L[j].i.toFixed(2)); t=Math.max(t,L[j].o); }
 out.push("buracos de legenda: "+(bur.length?bur.join(", "):"nenhum"));
 // a camada do take cobre a legenda?
 for(var q=1;q<=C.numLayers;q++){ if(C.layer(q).name==="TAKE FRASCO") out.push("TAKE FRASCO no indice "+q); }
 for(var q2=1;q2<=C.numLayers;q2++){ if(C.layer(q2).name.indexOf("LEG ")===0){ out.push("primeira LEG no indice "+q2); break; } }
 var f=new File("/tmp/ae_lw.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
})();
