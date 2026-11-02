(function(){
 var out=[]; var p=app.project;
 function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
 var C=comp("DR 01 ABERTURA");
 out.push("comp "+C.width+"x"+C.height+" dur="+C.duration.toFixed(2)+" fps="+C.frameRate);
 for(var i=1;i<=C.numLayers;i++){
   var L=C.layer(i);
   if(L.name!=="VIDEO" && L.name!=="SELO FRASCO") continue;
   var s=L.name+": ";
   try{ s+="fonte="+L.source.name+" "+(L.source.width||0)+"x"+(L.source.height||0); }catch(e){}
   try{ s+=" start="+L.startTime.toFixed(2)+" in="+L.inPoint.toFixed(2)+" out="+L.outPoint.toFixed(2); }catch(e){}
   try{ var sc=L.property("Transform").property("Scale").value; s+=" esc="+sc[0].toFixed(1); }catch(e){}
   try{ var q=L.property("Transform").property("Position").value; s+=" pos="+q[0].toFixed(0)+","+q[1].toFixed(0); }catch(e){}
   try{ s+=" indice="+i+" 3D="+L.threeDLayer; }catch(e){}
   try{ if(L.source.duration) s+=" durFonte="+L.source.duration.toFixed(2); }catch(e){}
   out.push(s);
 }
 // o que existe entre 4,1 e 7,5
 out.push("--- camadas ativas em 5,5s ---");
 for(var j=1;j<=C.numLayers;j++){
   var L2=C.layer(j);
   if(5.5>=L2.inPoint && 5.5<=L2.outPoint) out.push("  "+j+" "+L2.name);
 }
 var f=new File("/tmp/ae_vid.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
})();
