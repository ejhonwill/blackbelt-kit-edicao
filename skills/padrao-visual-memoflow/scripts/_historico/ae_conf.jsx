(function(){
 var out=[]; var p=app.project;
 function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
 var M=comp("MASTER_LETTERING_MEMOFLOW");
 out.push("MASTER_LETTERING_MEMOFLOW: "+(M?("existe, "+M.numLayers+" camadas, "+M.duration.toFixed(2)+"s"):"NAO EXISTE"));
 // confere a receita em cada cartela
 var falta=[];
 for(var c=1;c<=p.numItems;c++){
   var cc=p.item(c);
   if(!(cc instanceof CompItem) || cc.name.indexOf("CARD ")!==0) continue;
   var tem={FUNDO:0,ESCURECER:0,HALO:0,CTRL:0,CAM:0,TXT:0,glow:0,sombra:0};
   for(var i=1;i<=cc.numLayers;i++){
     var L=cc.layer(i), n=L.name;
     if(tem[n]!==undefined) tem[n]=1;
     if(n.indexOf("TXT ")===0){
       tem.TXT++;
       for(var f=1;f<=L.property("Effects").numProperties;f++){
         var mn=L.property("Effects").property(f).matchName;
         if(mn==="PEDG2") tem.glow++;
         if(mn==="ADBE Drop Shadow") tem.sombra++;
       }
     }
   }
   var ruim=[];
   for(var k in tem) if(!tem[k]) ruim.push(k);
   if(tem.glow<tem.TXT) ruim.push("glow "+tem.glow+"/"+tem.TXT);
   if(tem.sombra<tem.TXT) ruim.push("sombra "+tem.sombra+"/"+tem.TXT);
   if(ruim.length) falta.push(cc.name+" -> "+ruim.join(","));
   else out.push(cc.name+": fundo+escurecer+halo+ctrl+cam, "+tem.TXT+" textos com glow e sombra");
 }
 out.push(falta.length? ("INCOMPLETAS: "+falta.join(" | ")) : "todas as cartelas com a receita completa");
 p.save();
 var f2=new File("/tmp/ae_conf.txt"); f2.open("w"); f2.write(out.join(String.fromCharCode(10))); f2.close();
})();
