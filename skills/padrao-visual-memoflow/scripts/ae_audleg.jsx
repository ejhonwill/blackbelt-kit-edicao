(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var C=comp("DR 01 ABERTURA");
  // junta os pares
  var pares={};
  for(var i=1;i<=C.numLayers;i++){
    var L=C.layer(i), n=L.name;
    var m=/^(LEG|PIL) (\d+)$/.exec(n);
    if(!m) continue;
    if(!pares[m[2]]) pares[m[2]]={};
    pares[m[2]][m[1]]=L;
  }
  var lista=[];
  for(var k in pares){ if(pares[k].LEG) lista.push({k:parseInt(k,10), L:pares[k].LEG, P:pares[k].PIL, i:pares[k].LEG.inPoint}); }
  lista.sort(function(a,b){return a.i-b.i;});

  var ligadas=0, aparadas=0, dessinc=0;
  for(var j=0;j<lista.length;j++){
    var it=lista[j];
    if(!it.L.enabled){ it.L.enabled=true; ligadas++; }
    if(it.P && !it.P.enabled){ it.P.enabled=true; ligadas++; }
    // a legenda nao pode invadir a proxima
    if(j+1<lista.length){
      var prox=lista[j+1].i;
      if(it.L.outPoint>prox+0.02){ it.L.outPoint=prox; if(it.P) it.P.outPoint=prox; aparadas++; }
    }
    // pilula tem de acompanhar o texto
    if(it.P && (Math.abs(it.P.inPoint-it.L.inPoint)>0.02 || Math.abs(it.P.outPoint-it.L.outPoint)>0.02)){
      it.P.startTime=it.L.startTime; it.P.inPoint=it.L.inPoint; it.P.outPoint=it.L.outPoint; dessinc++;
    }
  }
  out.push("pares="+lista.length+" | camadas reativadas="+ligadas+" | saidas aparadas="+aparadas+" | pilulas ressincronizadas="+dessinc);
  // prova final
  var ruim=[];
  for(var q=0;q<lista.length;q++){
    var it2=lista[q];
    if(!it2.L.enabled || (it2.P && !it2.P.enabled)) ruim.push(it2.k+" desativada");
    if(q+1<lista.length && it2.L.outPoint>lista[q+1].i+0.02) ruim.push(it2.k+" invade a proxima");
  }
  out.push(ruim.length? ("AINDA RUIM: "+ruim.join(", ")) : "todas ligadas e sem sobreposicao entre si");
  app.project.save();
  var f=new File("/tmp/ae_aud.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_aud.txt"); fe.open("w"); fe.write("ERRO "+e.toString()+" linha "+e.line); fe.close(); }
})();
