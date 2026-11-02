(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var C=comp("DR 01 ABERTURA"); if(!C) throw new Error("sem comp");
  var DIS=0.22, FADE=0.18, ENT=0.34, DESL=44, BORR=46;

  var D=[__DADOS__];
  var achou=0, faltou=[], nent=0;
  for(var k=0;k<D.length;k++){
    var d=D[k], L=null;
    for(var q=1;q<=C.numLayers;q++){ if(C.layer(q).name===d.n){ L=C.layer(q); break; } }
    if(!L){ faltou.push(d.n); continue; }
    achou++;

    // a fonte tem fim: nao estica alem do que existe
    var lim=(L.source&&L.source.duration)? L.startTime+L.source.duration-0.02 : 1e9;
    var ini=Math.max(0,d.i-DIS), fim=Math.min(d.o,lim);
    if(L.startTime>ini) L.startTime=ini;      // puxa a fonte para tras se precisar
    L.inPoint=ini; L.outPoint=fim;

    // o plano que entra sobe por cima; o anterior so corta quando este ja esta cheio
    var op=L.property("Transform").property("Opacity");
    while(op.numKeys>0) op.removeKey(1);
    op.setValueAtTime(ini,0); op.setValueAtTime(d.i,100);
    if(d.u){ op.setValueAtTime(Math.max(d.i+0.05,fim-FADE),100); op.setValueAtTime(fim,0); }
    else    { op.setValueAtTime(fim,100); }
    for(var e=1;e<=op.numKeys;e++){ try{ op.setInterpolationTypeAtKey(e,KeyframeInterpolationType.BEZIER,KeyframeInterpolationType.BEZIER); }catch(er){} }

    // entrada com movimento e desfoque na direcao do deslocamento
    if(d.d!==""){
      var sc=L.property("Transform").property("Scale");
      while(sc.numKeys>0) sc.removeKey(1);
      var base=sc.value[0];
      var pp=L.property("Transform").property("Position");
      while(pp.numKeys>0) pp.removeKey(1);
      var dx=(d.d==="D")?DESL:0, dy=(d.d==="C")?-DESL:((d.d==="B")?DESL:0);
      var t0=ini, t1=Math.min(ini+ENT, fim-0.04);
      pp.setValueAtTime(t0,[540+dx,540+dy]); pp.setValueAtTime(t1,[540,540]);
      sc.setValueAtTime(t0,[base*1.10,base*1.10]); sc.setValueAtTime(t1,[base,base]);
      // respiro lento ate o fim, para o plano nao morrer parado
      sc.setValueAtTime(fim,[base*1.035,base*1.035]);
      function suave(P){
        for(var z=1;z<=P.numKeys;z++){
          try{ P.setInterpolationTypeAtKey(z,KeyframeInterpolationType.BEZIER,KeyframeInterpolationType.BEZIER);
               P.setTemporalEaseAtKey(z,[new KeyframeEase(0,z===1?18:85)],[new KeyframeEase(0,z===1?18:85)]); }catch(e2){}
        }
      }
      suave(pp); suave(sc);

      for(var f=L.property("Effects").numProperties;f>=1;f--){
        if(L.property("Effects").property(f).matchName==="ADBE Motion Blur") L.property("Effects").property(f).remove();
      }
      var db=L.property("Effects").addProperty("ADBE Motion Blur");
      db.property(1).setValue((d.d==="D")?90:0);      // eixo do movimento
      var cl=db.property(2);
      cl.setValueAtTime(t0,BORR); cl.setValueAtTime(t1,0);
      for(var e2b=1;e2b<=cl.numKeys;e2b++){ try{ cl.setInterpolationTypeAtKey(e2b,KeyframeInterpolationType.BEZIER,KeyframeInterpolationType.BEZIER); }catch(e3){} }
      nent++;
    }
    L.motionBlur=true;
  }
  C.motionBlur=true;
  out.push("planos ajustados="+achou+" | entradas="+nent+" | nao encontrados="+(faltou.length?faltou.join(","):"nenhum"));
  app.project.save();
  var f2=new File("/tmp/ae_cob2.txt"); f2.open("w"); f2.write(out.join(String.fromCharCode(10))); f2.close();
 }catch(e){ var fe=new File("/tmp/ae_cob2.txt"); fe.open("w"); fe.write("ERRO "+e.toString()+" linha "+e.line); fe.close(); }
})();
