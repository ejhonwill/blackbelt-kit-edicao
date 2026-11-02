(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  function midia(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof FootageItem&&x.name===n)return x;}return null;}
  function pasta(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof FolderItem&&x.name===n)return x;}return p.items.addFolder(n);}
  function suave(P,ent,sai){
    for(var z=1;z<=P.numKeys;z++){ try{
      P.setInterpolationTypeAtKey(z,KeyframeInterpolationType.BEZIER,KeyframeInterpolationType.BEZIER);
      P.setTemporalEaseAtKey(z,[new KeyframeEase(0,ent||70)],[new KeyframeEase(0,sai||70)]);
    }catch(e){} }
  }
  function elipse(L,cx,cy,rx,ry,pena){
    var m=L.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
    var k=0.5523,V=[],I=[],T=[];
    for(var a=0;a<8;a++){ var th=Math.PI*2*a/8;
      V.push([cx+rx*Math.cos(th), cy+ry*Math.sin(th)]);
      var tx=-rx*Math.sin(th)*k*Math.PI*2/8, ty=ry*Math.cos(th)*k*Math.PI*2/8;
      T.push([tx,ty]); I.push([-tx,-ty]); }
    var s=new Shape(); s.vertices=V; s.inTangents=I; s.outTangents=T; s.closed=true;
    m.property("ADBE Mask Shape").setValue(s);
    m.property("ADBE Mask Feather").setValue([pena,pena]);
  }

  // ---- padrao mestre, tirado do lettering aprovado ----
  var FONTE="Montserrat-ExtraBold", BRANCO=[1,1,1], AZUL=[0.40,0.44,1.0];
  var TRACK=-14, MAXW=900, BASE=96, MINF=56, MENOR=0.62;   // linha de apoio a 62% da principal
  var GLOW_BR=[28,0.40], GLOW_AZ=[78,1.35];                // Deep Glow: raio, exposicao
  var ZOOM=1500, ZFUNDO=400, ZESC=300, ZHALO=150, ZI=80, ZF=-210, SEGURO=940;
  var ESC_FUNDO=103.1*(ZOOM+ZFUNDO)/ZOOM;
  var DR=midia("DR 01 ABERTURA");
  if(!DR) throw new Error("sem a midia do medico");

  function fundoAprovado(cc, tIni){
    // 1) o video atras, desfocado e escurecido  2) halo azul  — a atmosfera da imagem 1
    var fu=cc.layers.add(DR); fu.name="FUNDO";
    fu.startTime=-tIni; fu.inPoint=0; fu.outPoint=cc.duration;
    fu.threeDLayer=true; fu.audioEnabled=false;
    fu.property("Transform").property("Position").setValue([540,540,ZFUNDO]);
    fu.property("Transform").property("Scale").setValue([ESC_FUNDO,ESC_FUNDO,100]);
    var b=fu.property("Effects").addProperty("ADBE Box Blur2");
    b.property(1).setValue(26); b.property(2).setValue(3);

    var es=cc.layers.addSolid([0.01,0.012,0.03],"ESCURECER",1080,1080,1);
    es.threeDLayer=true;
    var mE=ZOOM/(ZOOM+ZESC);
    es.property("Transform").property("Position").setValue([540,540,ZESC]);
    es.property("Transform").property("Scale").setValue([100/mE,100/mE,100]);
    es.property("Transform").property("Opacity").setValue(78);

    var ha=cc.layers.addSolid([0.26,0.32,1.0],"HALO",1080,1080,1);
    ha.threeDLayer=true; ha.blendingMode=BlendingMode.ADD;
    elipse(ha,540,540,395,268,215);
    var mH=ZOOM/(ZOOM+ZHALO);
    ha.property("Transform").property("Position").setValue([540,540,ZHALO]);
    ha.property("Transform").property("Scale").setValue([100/mH,100/mH,100]);
    ha.property("Transform").property("Opacity").setValue(26);
    var hb=ha.property("Effects").addProperty("ADBE Box Blur2"); hb.property(1).setValue(56); hb.property(2).setValue(3);
  }

  function estiloTexto(cc,s,cor,tam){
    var t=cc.layers.addText(s);
    var d=t.property("Source Text").value;
    d.fontSize=tam; d.font=FONTE; d.applyFill=true; d.fillColor=cor; d.applyStroke=false;
    d.tracking=TRACK; d.justification=ParagraphJustification.LEFT_JUSTIFY;
    t.property("Source Text").setValue(d);
    return t;
  }

  var INI=[__INICIOS__], D=[__DADOS__];
  var mapa={}; for(var q=0;q<INI.length;q++) mapa[INI[q].id]=INI[q].t;

  // ---- composicao de referencia do padrao ----
  var M=comp("MASTER_LETTERING_MEMOFLOW"); if(M) M.remove();
  M=p.items.addComp("MASTER_LETTERING_MEMOFLOW",1080,1080,1,2.4,25);
  M.parentFolder=pasta("05 CARTELAS"); M.motionBlur=true;
  fundoAprovado(M, 4.10);
  var mc=M.layers.addCamera("CAM",[540,540]); mc.moveToBeginning();
  mc.property("Transform").property("Anchor Point").setValue([540,540,0]);
  mc.property("Transform").property("Position").setValue([540,540,-ZOOM]);

  var nc=0, rel=[];
  for(var g=0;g<D.length;g++){
    var G=D[g], cc=comp("CARD "+G.id);
    if(!cc){ out.push("sem CARD "+G.id); continue; }
    for(var k=cc.numLayers;k>=1;k--) cc.layer(k).remove();
    var dur=G.d+0.8; if(cc.duration<dur){ try{ cc.duration=dur; }catch(e1){} }
    fundoAprovado(cc, mapa[G.id]!==undefined?mapa[G.id]:G.t);

    // hierarquia: a linha que carrega o destaque e a principal
    var iPrinc=0;
    for(var li=0;li<G.L.length;li++){
      for(var si=0;si<G.L[li].length;si++) if(G.L[li][si].c) iPrinc=li;
    }
    function esp(tam){ var a=estiloTexto(cc,"nn",BRANCO,tam), b=estiloTexto(cc,"n n",BRANCO,tam);
      var w=b.sourceRectAtTime(0,false).width-a.sourceRectAtTime(0,false).width; a.remove(); b.remove(); return w; }
    function mede(s,tam){ var t=estiloTexto(cc,s,BRANCO,tam); var w=t.sourceRectAtTime(0,false).width; t.remove(); return w; }
    function largura(ln,tm,es2){ var w=0; for(var i2=0;i2<ln.length;i2++){ w+=mede(ln[i2].s,tm); if(i2<ln.length-1) w+=es2; } return w; }
    function tamLinha(li,base){ return (G.L.length>1 && li!==iPrinc)? Math.round(base*MENOR) : base; }

    var base=BASE, larg=0;
    function recalcula(){
      larg=0;
      for(var q2=0;q2<G.L.length;q2++){ var tm=tamLinha(q2,base); larg=Math.max(larg, largura(G.L[q2],tm,esp(tm))); }
    }
    recalcula();
    while(larg>MAXW && base>MINF){ base-=5; recalcula(); }

    var dy=Math.round(base*1.06);
    var yTopo=(G.L.length===1)?540:540-dy/2;
    var ctrl=cc.layers.addNull(cc.duration);
    ctrl.name="CTRL"; ctrl.threeDLayer=true; ctrl.enabled=false;
    var cp=ctrl.property("Transform").property("Position");
    cp.setValueAtTime(0,[540,540,ZI]); cp.setValueAtTime(cc.duration,[540,540,ZF]);
    suave(cp,60,70);

    var maiorW=0;
    for(var li2=0;li2<G.L.length;li2++){
      var ln=G.L[li2], tam=tamLinha(li2,base), es3=esp(tam);
      var total=largura(ln,tam,es3); maiorW=Math.max(maiorW,total);
      var x=540-total/2, y=(G.L.length===1)?540:(yTopo+li2*dy);
      for(var si2=0;si2<ln.length;si2++){
        var sg=ln[si2];
        var t=estiloTexto(cc,sg.s,sg.c?AZUL:BRANCO,tam);
        t.name="TXT "+(li2+1)+"."+(si2+1);
        var r=t.sourceRectAtTime(0,false);
        var px=x-r.left;
        t.threeDLayer=true; t.motionBlur=true;
        t.parent=ctrl;
        t.property("Transform").property("Position").setValue([px-540, y-540, 0]);

        // entrada igual a do lettering aprovado: sobe 28 px, escala 93 -> 100, ease
        var an=t.property("Text").property("Animators").addProperty("ADBE Text Animator");
        var ap=an.property("ADBE Text Animator Properties");
        ap.addProperty("ADBE Text Opacity").setValue(0);
        try{ ap.addProperty("ADBE Text Position 3D").setValue([0,28,0]); }catch(ea){}
        try{ ap.addProperty("ADBE Text Scale 3D").setValue([93,93,100]); }catch(eb){}
        var sel=an.property("ADBE Text Selectors").addProperty("ADBE Text Selector");
        var av=sel.property("ADBE Text Range Advanced");
        av.property("ADBE Text Range Units").setValue(2);
        av.property("ADBE Text Range Type2").setValue(3);
        try{ av.property("ADBE Text Selector Smoothness").setValue(100); }catch(ec){}
        var st=sel.property("ADBE Text Index Start");
        sel.property("ADBE Text Index End").setValue(999);
        st.setValueAtTime(0,0);
        for(var w=0;w<sg.w.length;w++){
          var tw=Math.max(0.04, sg.w[w]-G.t);
          var prox=(w+1<sg.w.length)? (sg.w[w+1]-G.t) : cc.duration;
          var rampa=Math.max(0.14, Math.min(0.26, prox-tw-0.03));
          st.setValueAtTime(Math.min(tw, cc.duration-0.10), w);
          st.setValueAtTime(Math.min(tw+rampa, cc.duration-0.04), w+1);
        }
        suave(st,18,84);

        var dg=t.property("Effects").addProperty("PEDG2");
        dg.property(24).setValue(sg.c?GLOW_AZ[0]:GLOW_BR[0]);
        dg.property(25).setValue(sg.c?GLOW_AZ[1]:GLOW_BR[1]);
        var ds=t.property("Effects").addProperty("ADBE Drop Shadow");
        try{ ds.property(2).setValue(52); ds.property(3).setValue(135); ds.property(4).setValue(8); ds.property(5).setValue(14); }catch(ed){}
        x+=r.width+es3;
      }
    }
    // margem de seguranca com o avanco da camera
    var mag=ZOOM/(ZOOM+ZF), fator=SEGURO/(maiorW*mag);
    var escala=(fator<1)? fator*100 : 100;
    ctrl.property("Transform").property("Scale").setValue([escala,escala,100]);

    var cam=cc.layers.addCamera("CAM",[540,540]); cam.moveToBeginning();
    cam.property("Transform").property("Anchor Point").setValue([540,540,0]);
    cam.property("Transform").property("Position").setValue([540,540,-ZOOM]);
    cc.motionBlur=true;
    rel.push(G.id+":"+base+"/"+Math.round(base*MENOR)+"px"+(escala<100?(" esc"+Math.round(escala)):""));
    nc++;
  }
  out.push("cartelas no padrao mestre="+nc);
  out.push(rel.join(" "));
  app.project.save();
  var f=new File("/tmp/ae_mst.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_mst.txt"); fe.open("w"); fe.write("ERRO: "+e.toString()+" linha "+e.line); fe.close(); }
})();
