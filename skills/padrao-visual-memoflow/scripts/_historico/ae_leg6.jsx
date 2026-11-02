(function(){
 var out=[]; var p=app.project;
 function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
 var C=comp("DR 01 ABERTURA");
 for(var i=1;i<=C.numLayers;i++){
   var L=C.layer(i), n=L.name;
   if(n!=="LEG 6" && n!=="PIL 6" && n!=="LEG 5" && n!=="PIL 5" && n!=="LEG 7" && n!=="PIL 7") continue;
   var s=i+" ["+n+"] in="+L.inPoint.toFixed(2)+" out="+L.outPoint.toFixed(2)+" start="+L.startTime.toFixed(2);
   try{ s+=" ativo="+L.enabled+" op="+L.property("Transform").property("Opacity").value; }catch(e){}
   try{ var v=L.property("Transform").property("Position").value; s+=" pos="+v[0].toFixed(0)+","+v[1].toFixed(0); }catch(e){}
   try{ s+=" fx="+L.property("Effects").numProperties; }catch(e){}
   if(n.indexOf("LEG ")===0){ try{ s+=' txt="'+L.property("Source Text").value.text.substring(0,26)+'"'; }catch(e){} }
   out.push(s);
 }
 var f=new File("/tmp/ae_l6.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
})();
