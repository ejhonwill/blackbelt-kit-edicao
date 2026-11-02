(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var C=comp("DR 01 ABERTURA");

  // tira a duplicata do beat de produto
  var visto={}, dup=0;
  for(var k=C.numLayers;k>=1;k--){
    var nm=C.layer(k).name;
    if(nm.indexOf("PROD")!==0) continue;
    if(visto[nm]){ C.layer(k).remove(); dup++; } else visto[nm]=1;
  }
  out.push("beats de produto duplicados removidos="+dup);

  // cada titulo passa a pendurar num controle unico, centrado em 540,540
  var ZI=90, ZF=-360, nc=0, nt=0;
  for(var c=1;c<=p.numItems;c++){
    var cc=p.item(c);
    if(!(cc instanceof CompItem) || cc.name.indexOf("CARD ")!==0) continue;

    for(var q=cc.numLayers;q>=1;q--){ if(cc.layer(q).name==="CTRL") cc.layer(q).remove(); }
    var ctrl=cc.layers.addNull(cc.duration);
    ctrl.name="CTRL"; ctrl.threeDLayer=true; ctrl.enabled=false; ctrl.moveToBeginning();
    var cp=ctrl.property("Transform").property("Position");
    cp.setValueAtTime(0,[540,540,ZI]);
    cp.setValueAtTime(cc.duration,[540,540,ZF]);
    try{ cp.setInterpolationTypeAtKey(1,KeyframeInterpolationType.BEZIER,KeyframeInterpolationType.BEZIER); }catch(e0){}

    // o conjunto tem de ficar simetrico no eixo X: mede as linhas e recentra
    var linhas={};
    for(var t=1;t<=cc.numLayers;t++){
      var L=cc.layer(t); if(L.name.indexOf("TXT ")!==0) continue;
      var li=L.name.split(" ")[1].split(".")[0];
      var r=L.sourceRectAtTime(0,false);
      var pos=L.property("Transform").property("Position");
      var v=(pos.numKeys>0)? pos.keyValue(1) : pos.value;
      var e=v[0]+r.left, d=v[0]+r.left+r.width;
      if(!linhas[li]) linhas[li]={e:e,d:d,ls:[]};
      linhas[li].e=Math.min(linhas[li].e,e); linhas[li].d=Math.max(linhas[li].d,d);
      linhas[li].ls.push({L:L,v:v});
    }
    for(var li2 in linhas){
      var ln=linhas[li2];
      var desloc=540-(ln.e+ln.d)/2;      // erro optico da linha inteira
      for(var z=0;z<ln.ls.length;z++){
        var L2=ln.ls[z].L, v2=ln.ls[z].v;
        var pos2=L2.property("Transform").property("Position");
        while(pos2.numKeys>0) pos2.removeKey(1);
        L2.threeDLayer=true;
        L2.parent=ctrl;                                   // o titulo anda junto
        pos2.setValue([v2[0]+desloc-540, v2[1]-540, 0]);  // relativo ao controle
        nt++;
      }
    }
    nc++;
  }
  out.push("titulos re-ancorados="+nc+" | camadas de texto="+nt);
  app.project.save();
  var f=new File("/tmp/ae_ctr.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_ctr.txt"); fe.open("w"); fe.write("ERRO "+e.toString()+" linha "+e.line); fe.close(); }
})();
