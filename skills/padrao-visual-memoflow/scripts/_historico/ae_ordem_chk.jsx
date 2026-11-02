(function(){
 var out=[]; var p=app.project;
 function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
 var nomes=["DR 01 ABERTURA","DEP 02 MARK","DEP 03 ELAINE","DEP 04 ROBERT","DR 05 MECANISMO",
            "DEP 06 MARGARET","DR 07 OFERTA","DEP 08 FRANK","DEP 09 NANCY","DEP 10 GEORGE"];
 var totPar=0, totRuim=0;
 for(var k=0;k<nomes.length;k++){
   var C=comp(nomes[k]); if(!C) continue;
   var idx={};
   for(var i=1;i<=C.numLayers;i++) idx[C.layer(i).name]=i;
   var par=0, ruim=0;
   for(var j=1;j<=400;j++){
     if(idx["LEG "+j]===undefined||idx["PIL "+j]===undefined) continue;
     par++; if(idx["LEG "+j]>idx["PIL "+j]) ruim++;
   }
   totPar+=par; totRuim+=ruim;
   out.push("  "+nomes[k]+": "+par+" pares, "+ruim+" com a pilula por cima do texto");
 }
 out.unshift("pares="+totPar+" | INVERTIDOS="+totRuim);
 var f=new File("/tmp/ae_ord2.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
})();
