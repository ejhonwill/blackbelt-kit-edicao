(function(){
 var out=[]; var p=app.project;
 function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
 var C=comp("DR 01 ABERTURA"); var T=18.20;
 for(var i=1;i<=C.numLayers;i++){
   var L=C.layer(i), nm=L.name;
   if(nm.indexOf("LEG ")!==0 && nm.indexOf("PIL ")!==0) continue;
   if(T<L.inPoint || T>L.outPoint) continue;
   var s=i+" ["+nm+"]";
   try{ s+=" in="+L.inPoint.toFixed(2)+" out="+L.outPoint.toFixed(2); }catch(e){}
   try{ s+=" op="+L.property("Transform").property("Opacity").value; }catch(e){}
   try{ s+=" ativo="+L.enabled+" 3D="+L.threeDLayer; }catch(e){}
   try{ var v=L.property("Transform").property("Position").value; s+=" pos="+v[0].toFixed(0)+","+v[1].toFixed(0); }catch(e){ s+=" pos=ERR"; }
   try{ var sc=L.property("Transform").property("Scale").value; s+=" esc="+sc[0].toFixed(0); }catch(e){}
   if(nm.indexOf("LEG ")===0){
     try{ var td=L.property("Source Text").value; s+=' txt="'+td.text.substring(0,28)+'"'; }catch(e){ s+=" txt=ERR"; }
     try{ s+=" corpo="+L.property("Source Text").value.fontSize; }catch(e){ s+=" corpo=ERR"; }
     try{ s+=" cor="+L.property("Source Text").value.fillColor.join(","); }catch(e){ s+=" cor=ERR"; }
     try{ s+=" fx="+L.property("Effects").numProperties; }catch(e){}
     try{ var an=L.property("Text").property("Animators"); s+=" animadores="+an.numProperties; }catch(e){}
   }
   out.push(s);
 }
 out.unshift("t=18.20 camadas="+out.length);
 var f=new File("/tmp/ae_l18.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
})();
