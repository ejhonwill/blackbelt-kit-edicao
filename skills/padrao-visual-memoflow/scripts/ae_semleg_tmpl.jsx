(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var C=comp("DR 01 ABERTURA");
  var CART=[__CARDS__];
  var tirados=0, cortados=0, mantidos=0;
  for(var k=1;k<=200;k++){
    var leg=null,pil=null;
    for(var i=1;i<=C.numLayers;i++){
      var nm=C.layer(i).name;
      if(nm==="LEG "+k) leg=C.layer(i); else if(nm==="PIL "+k) pil=C.layer(i);
    }
    if(!leg) continue;
    var a=leg.inPoint, b=leg.outPoint, dur=b-a;
    var sob=0, ca=0, cb=0;
    for(var c=0;c<CART.length;c++){
      var o=Math.min(b,CART[c].b)-Math.max(a,CART[c].a);
      if(o>sob){ sob=o; ca=CART[c].a; cb=CART[c].b; }
    }
    if(sob<=0.02){ mantidos++; continue; }
    if(sob/dur>=0.6){                       // a cartela ja diz a frase
      leg.remove(); if(pil) pil.remove(); tirados++;
    }else{
      // sobra so o pedaco fora da cartela
      var na=a, nb=b;
      if(a<ca) nb=Math.min(b,ca); else na=Math.max(a,cb);
      if(nb-na<0.35){ leg.remove(); if(pil) pil.remove(); tirados++; }
      else{
        leg.inPoint=na; leg.outPoint=nb;
        if(pil){ pil.inPoint=na; pil.outPoint=nb; }
        cortados++;
      }
    }
  }
  out.push("legendas removidas sobre lettering="+tirados+" | aparadas="+cortados+" | intactas="+mantidos);
  // prova: sobrou alguma legenda dentro de cartela?
  var resta=0;
  for(var j=1;j<=C.numLayers;j++){
    var L=C.layer(j); if(L.name.indexOf("LEG ")!==0) continue;
    for(var c2=0;c2<CART.length;c2++){
      if(Math.min(L.outPoint,CART[c2].b)-Math.max(L.inPoint,CART[c2].a)>0.05) resta++;
    }
  }
  out.push("legendas ainda sobrepostas a cartela: "+resta);
  app.project.save();
  var f=new File("/tmp/ae_sl.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_sl.txt"); fe.open("w"); fe.write("ERRO "+e.toString()+" linha "+e.line); fe.close(); }
})();
