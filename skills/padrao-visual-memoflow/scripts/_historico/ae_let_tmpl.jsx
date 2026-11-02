(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var C=comp("DR 01 ABERTURA"); if(!C) throw new Error("sem DR 01 ABERTURA");

  var FONTE="Montserrat-ExtraBold", BRANCO=[1,1,1], LARANJA=[1,0.42,0.16];
  var MAXW=920, BASE=78, MINF=48, Y1=772, Y2=882, YU=828;
  var ZI=150, ZF=-900, CAUDA=0.55;

  // limpa legenda antiga (pilula inclusive) e camera de lettering
  for(var k=C.numLayers;k>=1;k--){ var nm=C.layer(k).name;
    if(nm.indexOf("LEG ")===0||nm.indexOf("PIL ")===0||nm==="CAM LET") C.layer(k).remove(); }

  function novo(s,cor,tam){
    var t=C.layers.addText(s);
    var d=t.property("Source Text").value;
    d.fontSize=tam; d.font=FONTE; d.applyFill=true; d.fillColor=cor; d.applyStroke=false;
    d.tracking=-14; d.justification=ParagraphJustification.LEFT_JUSTIFY;
    t.property("Source Text").setValue(d);
    return t;
  }
  function larguraEspaco(tam){
    var a=novo("nn",BRANCO,tam), b=novo("n n",BRANCO,tam);
    var w=b.sourceRectAtTime(0,false).width-a.sourceRectAtTime(0,false).width;
    a.remove(); b.remove(); return w;
  }
  function mede(s,tam){ var t=novo(s,BRANCO,tam); var w=t.sourceRectAtTime(0,false).width; t.remove(); return w; }

  var D=[__DADOS__];
  var nL=0, nS=0, nG=0;

  for(var g=0;g<D.length;g++){
    var G=D[g], ini=Math.max(0,G.t-0.05), fim=G.f+CAUDA;

    // corpo que cabe nas duas linhas
    var tam=BASE, esp=larguraEspaco(tam);
    function larguraLinha(ln,tm,es){ var w=0; for(var i=0;i<ln.length;i++){ w+=mede(ln[i].s,tm); if(i<ln.length-1) w+=es; } return w; }
    var larg=0;
    for(var q=0;q<G.L.length;q++) larg=Math.max(larg,larguraLinha(G.L[q],tam,esp));
    while(larg>MAXW && tam>MINF){
      tam-=4; esp=larguraEspaco(tam); larg=0;
      for(var q2=0;q2<G.L.length;q2++) larg=Math.max(larg,larguraLinha(G.L[q2],tam,esp));
    }

    for(var li=0;li<G.L.length;li++){
      var ln=G.L[li];
      var y=(G.L.length===1)?YU:(li===0?Y1:Y2);
      var total=larguraLinha(ln,tam,esp), x=540-total/2;
      for(var si=0;si<ln.length;si++){
        var sg=ln[si];
        var t=novo(sg.s,sg.c?LARANJA:BRANCO,tam);
        t.name="LEG "+(g+1)+"."+(li+1)+"."+(si+1);
        var r=t.sourceRectAtTime(0,false);
        var px=x-r.left, py=y;
        t.threeDLayer=true; t.motionBlur=true;
        var pp=t.property("Transform").property("Position");
        pp.setValueAtTime(G.t,[px,py,ZI]);
        pp.setValueAtTime(fim,[px,py,ZF]);
        try{ pp.setInterpolationTypeAtKey(1,KeyframeInterpolationType.BEZIER,KeyframeInterpolationType.BEZIER); }catch(e0){}
        var op=t.property("Transform").property("Opacity");
        op.setValueAtTime(G.t,100); op.setValueAtTime(G.f,100); op.setValueAtTime(fim,0);
        t.startTime=0; t.inPoint=ini; t.outPoint=fim;

        // construcao palavra a palavra: o seletor esconde o que ainda nao foi dito
        var an=t.property("Text").property("Animators").addProperty("ADBE Text Animator");
        an.property("ADBE Text Animator Properties").addProperty("ADBE Text Opacity").setValue(0);
        var sel=an.property("ADBE Text Selectors").addProperty("ADBE Text Selector");
        sel.property("ADBE Text Range Type2").setValue(2);   // unidades: indice
        sel.property("ADBE Text Range Type").setValue(3);    // base: palavras
        var st=sel.property("ADBE Text Index Start");
        sel.property("ADBE Text Index End").setValue(999);
        st.setValueAtTime(Math.max(0,G.t-0.30),0);
        for(var w=0;w<sg.w.length;w++) st.setValueAtTime(Math.max(0.001,sg.w[w]),w+1);
        for(var e=1;e<=st.numKeys;e++){ try{ st.setInterpolationTypeAtKey(e,KeyframeInterpolationType.HOLD,KeyframeInterpolationType.HOLD); }catch(e1){} }

        // Deep Glow: forte na palavra-chave, discreto no branco
        var dg=t.property("Effects").addProperty("PEDG2");
        dg.property(24).setValue(sg.c?78:34);   // Radius
        dg.property(25).setValue(sg.c?1.45:0.55); // Exposure

        x+=r.width+esp; nS++;
      }
      nL++;
    }
    nG++;
  }

  // camera unica: so o lettering e 3D, o resto ignora
  var cam=C.layers.addCamera("CAM LET",[540,540]);
  cam.moveToBeginning();
  out.push("grupos="+nG+" linhas="+nL+" segmentos="+nS+" camadas="+C.numLayers);
  out.push("camera z="+cam.property("Transform").property("Position").value[2]);

  C.motionBlur=true;
  for(var v=1;v<=C.numLayers;v++){ if(C.layer(v).name==="VIDEO"){ C.layer(v).moveToEnd(); break; } }
  app.project.save();
  var f=new File("/tmp/ae_let.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(err){ var fe=new File("/tmp/ae_let.txt"); fe.open("w"); fe.write("ERRO: "+err.toString()+" linha "+err.line); fe.close(); }
})();
