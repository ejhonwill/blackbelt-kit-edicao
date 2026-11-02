(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  function pasta(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof FolderItem&&x.name===n)return x;}return p.items.addFolder(n);}

  // ---- fundo: a fita 3D do Kling no lugar do ruido 2D ----
  var BG=comp("BG LETTERING");
  if(!BG) throw new Error("sem BG LETTERING");
  for(var k=BG.numLayers;k>=1;k--) BG.layer(k).remove();
  var fita=null;
  for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof FootageItem && x.name==="BG_A.mp4") fita=x; }
  if(!fita){
    var ff=new File("__BG3D__");
    if(ff.exists){ fita=p.importFile(new ImportOptions(ff)); fita.parentFolder=pasta("01 MATERIAL"); }
  }
  BG.layers.addSolid([0,0,0],"PRETO",1080,1080,1);
  if(fita){
    try{ fita.mainSource.conformFrameRate=25; }catch(e0){}
    var lf=BG.layers.add(fita); lf.name="FITA 3D";
    var es=1080/fita.width*100*1.06;
    lf.property("Transform").property("Scale").setValue([es,es]);
    lf.property("Transform").property("Position").setValue([540,640]);  // fita embaixo, texto respira em cima
    lf.audioEnabled=false;
    lf.property("Transform").property("Opacity").setValue(92);
    var lp=BG.duration>fita.duration?fita.duration:BG.duration;
    out.push("fita 3D "+Math.round(es)+"% dur="+fita.duration.toFixed(2));
  } else out.push("SEM BG_A.mp4");
  var vg=BG.layers.addSolid([0,0,0],"VINHETA",1080,1080,1);
  var mv=vg.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
  var sv=new Shape(); sv.vertices=[[60,60],[1020,60],[1020,1020],[60,1020]]; sv.closed=true;
  mv.property("ADBE Mask Shape").setValue(sv); mv.maskMode=MaskMode.SUBTRACT;
  mv.property("ADBE Mask Feather").setValue([280,280]);
  vg.property("Transform").property("Opacity").setValue(62);

  // ---- as 11 cartelas ----
  var FONTE="Montserrat-ExtraBold", BRANCO=[1,1,1], AZUL=[0.40,0.44,1.0];
  var MAXW=900, BASE=96, MINF=54, ZI=90, ZF=-360;
  var D=[__DADOS__]; var n=0, rel=[];

  for(var g=0;g<D.length;g++){
    var G=D[g], cc=comp("CARD "+G.id);
    if(!cc){ out.push("sem CARD "+G.id); continue; }
    for(var k2=cc.numLayers;k2>=1;k2--) cc.layer(k2).remove();
    var dur=G.d+0.8; if(cc.duration<dur){ try{ cc.duration=dur; }catch(e1){} }

    var lb=cc.layers.add(BG); lb.name="BGL";
    lb.startTime=-(g%6)*1.4;
    lb.property("Transform").property("Scale").setValue([112,112]);

    function novo(s,cor,tam){
      var t=cc.layers.addText(s);
      var d2=t.property("Source Text").value;
      d2.fontSize=tam; d2.font=FONTE; d2.applyFill=true; d2.fillColor=cor; d2.applyStroke=false;
      d2.tracking=-16; d2.justification=ParagraphJustification.LEFT_JUSTIFY;
      t.property("Source Text").setValue(d2);
      return t;
    }
    function larguraEspaco(tam){
      var a=novo("nn",BRANCO,tam), b=novo("n n",BRANCO,tam);
      var w=b.sourceRectAtTime(0,false).width-a.sourceRectAtTime(0,false).width;
      a.remove(); b.remove(); return w;
    }
    function mede(s,tam){ var t=novo(s,BRANCO,tam); var w=t.sourceRectAtTime(0,false).width; t.remove(); return w; }
    function larguraLinha(ln,tm,es2){ var w=0; for(var i2=0;i2<ln.length;i2++){ w+=mede(ln[i2].s,tm); if(i2<ln.length-1) w+=es2; } return w; }

    var tam=BASE, esp=larguraEspaco(tam), larg=0;
    for(var q=0;q<G.L.length;q++) larg=Math.max(larg,larguraLinha(G.L[q],tam,esp));
    while(larg>MAXW && tam>MINF){
      tam-=5; esp=larguraEspaco(tam); larg=0;
      for(var q2=0;q2<G.L.length;q2++) larg=Math.max(larg,larguraLinha(G.L[q2],tam,esp));
    }
    var dy=Math.round(tam*1.22);
    for(var li=0;li<G.L.length;li++){
      var ln=G.L[li];
      var y=(G.L.length===1)?540:(li===0?540-dy/2:540+dy/2);
      var total=larguraLinha(ln,tam,esp), x=540-total/2;
      for(var si=0;si<ln.length;si++){
        var sg=ln[si];
        var t=novo(sg.s,sg.c?AZUL:BRANCO,tam);
        t.name="TXT "+(li+1)+"."+(si+1);
        var r=t.sourceRectAtTime(0,false);
        var px=x-r.left;
        t.threeDLayer=true; t.motionBlur=true;
        var pp=t.property("Transform").property("Position");
        pp.setValueAtTime(0,[px,y,ZI]); pp.setValueAtTime(cc.duration,[px,y,ZF]);
        try{ pp.setInterpolationTypeAtKey(1,KeyframeInterpolationType.BEZIER,KeyframeInterpolationType.BEZIER); }catch(e2){}

        var an=t.property("Text").property("Animators").addProperty("ADBE Text Animator");
        an.property("ADBE Text Animator Properties").addProperty("ADBE Text Opacity").setValue(0);
        var sel=an.property("ADBE Text Selectors").addProperty("ADBE Text Selector");
        var av=sel.property("ADBE Text Range Advanced");
        av.property("ADBE Text Range Units").setValue(2);
        av.property("ADBE Text Range Type2").setValue(3);
        var st=sel.property("ADBE Text Index Start");
        sel.property("ADBE Text Index End").setValue(999);
        st.setValueAtTime(0,0);
        for(var w=0;w<sg.w.length;w++){
          var tw=Math.max(0.04, sg.w[w]-G.t);           // tempo local da cartela
          st.setValueAtTime(Math.min(tw, cc.duration-0.04), w+1);
        }
        for(var e=1;e<=st.numKeys;e++){ try{ st.setInterpolationTypeAtKey(e,KeyframeInterpolationType.HOLD,KeyframeInterpolationType.HOLD); }catch(e3){} }

        var dg=t.property("Effects").addProperty("PEDG2");
        dg.property(24).setValue(sg.c?84:30);
        dg.property(25).setValue(sg.c?1.55:0.45);
        x+=r.width+esp;
      }
    }
    var cam=cc.layers.addCamera("CAM",[540,540]); cam.moveToBeginning();
    cc.motionBlur=true;
    rel.push(G.id+":"+tam+"px"); n++;
  }
  out.push("cartelas="+n+" | "+rel.join(" "));
  app.project.save();
  var f=new File("/tmp/ae_cart.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(err){ var fe=new File("/tmp/ae_cart.txt"); fe.open("w"); fe.write("ERRO: "+err.toString()+" linha "+err.line); fe.close(); }
})();
