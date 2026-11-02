// ae_cta.jsx — fecho 'Click the button below…' no padrao MemoFlow.
// Placeholders do gerador: __DUR__ (duracao da comp, s), __T_SETA__ (segundo em que 'below' e dito),
// __LJS__ (linhas do lettering: [{s,c,w:[tempos]}], tempos no relogio da comp). Sem audio por dentro.
(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  function pasta(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof FolderItem&&x.name===n)return x;}return p.items.addFolder(n);}
  function suave(P,e1,e2){ for(var z=1;z<=P.numKeys;z++){ try{ P.setInterpolationTypeAtKey(z,KeyframeInterpolationType.BEZIER,KeyframeInterpolationType.BEZIER); P.setTemporalEaseAtKey(z,[new KeyframeEase(0,e1||70)],[new KeyframeEase(0,e2||70)]); }catch(e){} } }
  var FONTE="Montserrat-ExtraBold", BRANCO=[1,1,1], AZUL=[0.40,0.44,1.0], TRACK=-14, MAXW=960, MENOR=0.62;
  var DUR=__DUR__, T_SETA=__T_SETA__;
  var C=comp("DR 08 CTA FINAL"); if(C) C.remove();
  C=p.items.addComp("DR 08 CTA FINAL",1080,1080,1,DUR,25); C.parentFolder=pasta("02 COMPS"); C.motionBlur=true;
  // fundo: preto + fita 3D como respiro (mesma receita das cartelas)
  C.layers.addSolid([0,0,0],"PRETO",1080,1080,1);
  var BG=comp("BG LETTERING"); if(BG){ var lb=C.layers.add(BG); lb.name="BGL"; lb.property("Transform").property("Scale").setValue([112,112]); lb.property("Transform").property("Opacity").setValue(28); }
  // frasco: a pre-comp com o recorte do Jhon, sobe do rodape e assenta no alto
  var FR=comp("MEMOFLOW_BOTTLE_CUTOUT"); if(!FR) throw new Error("sem MEMOFLOW_BOTTLE_CUTOUT");
  var lf=C.layers.add(FR); lf.name="FRASCO"; lf.motionBlur=true;
  lf.property("Transform").property("Scale").setValue([46,46]);
  var pf=lf.property("Transform").property("Position");
  pf.setValueAtTime(0.00,[540,480]); pf.setValueAtTime(0.42,[540,238]); pf.setValueAtTime(0.56,[540,252]);
  pf.setValueAtTime(DUR,[540,246]); suave(pf,16,84);
  var of=lf.property("Transform").property("Opacity"); of.setValueAtTime(0,0); of.setValueAtTime(0.30,100); suave(of);
  var db=lf.property("Effects").addProperty("ADBE Motion Blur"); db.property(1).setValue(0);
  var cl=db.property(2); cl.setValueAtTime(0,36); cl.setValueAtTime(0.42,0); suave(cl);
  // lettering no padrao mestre, palavra a palavra na fala
  var L=[__LJS__];
  function novo(s,cor,tam){ var t=C.layers.addText(s); var d=t.property("Source Text").value; d.fontSize=tam; d.font=FONTE; d.applyFill=true; d.fillColor=cor; d.applyStroke=false; d.tracking=TRACK; d.justification=ParagraphJustification.LEFT_JUSTIFY; t.property("Source Text").setValue(d); return t; }
  function mede(s,tam){ var t=novo(s,BRANCO,tam); var w=t.sourceRectAtTime(0,false).width; t.remove(); return w; }
  var base=96; var iPrinc=2;
  function tam(li){ return (li===1)? Math.round(base*MENOR) : base; }
  function larg(){ var m=0; for(var q=0;q<L.length;q++){ var w=0; for(var s=0;s<L[q].length;s++) w+=mede(L[q][s].s,tam(q)); m=Math.max(m,w); } return m; }
  while(larg()>MAXW && base>50) base-=4;
  var ys=[560, 560+Math.round(base*1.06), 560+Math.round(base*1.06)+Math.round(base*1.06)];
  var ctrl=C.layers.addNull(DUR); ctrl.name="CTRL"; ctrl.threeDLayer=true; ctrl.enabled=false;
  var cp=ctrl.property("Transform").property("Position"); cp.setValueAtTime(0,[540,540,60]); cp.setValueAtTime(DUR,[540,540,-120]); suave(cp,60,70);
  for(var li=0;li<L.length;li++){ var ln=L[li], tm=tam(li);
    var total=0; for(var s2=0;s2<ln.length;s2++) total+=mede(ln[s2].s,tm);
    var x=540-total/2;
    for(var si=0;si<ln.length;si++){ var sg=ln[si]; var t=novo(sg.s, sg.c?AZUL:BRANCO, tm); t.name="TXT "+(li+1)+"."+(si+1);
      var r=t.sourceRectAtTime(0,false); t.threeDLayer=true; t.motionBlur=true; t.parent=ctrl;
      t.property("Transform").property("Position").setValue([x-r.left-540, ys[li]-540, 0]);
      var an=t.property("Text").property("Animators").addProperty("ADBE Text Animator"); var ap=an.property("ADBE Text Animator Properties");
      ap.addProperty("ADBE Text Opacity").setValue(0); try{ ap.addProperty("ADBE Text Position 3D").setValue([0,28,0]); ap.addProperty("ADBE Text Scale 3D").setValue([93,93,100]); }catch(ea){}
      var sel=an.property("ADBE Text Selectors").addProperty("ADBE Text Selector"); var av=sel.property("ADBE Text Range Advanced");
      av.property("ADBE Text Range Units").setValue(2); av.property("ADBE Text Range Type2").setValue(3); try{ av.property("ADBE Text Selector Smoothness").setValue(100); }catch(ec){}
      var st=sel.property("ADBE Text Index Start"); sel.property("ADBE Text Index End").setValue(999); st.setValueAtTime(0,0);
      for(var w=0;w<sg.w.length;w++){ var tw=Math.max(0.04,sg.w[w]); var prox=(w+1<sg.w.length)?sg.w[w+1]:DUR; var rampa=Math.max(0.14,Math.min(0.26,prox-tw-0.03));
        st.setValueAtTime(Math.min(tw,DUR-0.10),w); st.setValueAtTime(Math.min(tw+rampa,DUR-0.04),w+1); }
      suave(st,18,84);
      var dg=t.property("Effects").addProperty("PEDG2"); dg.property(24).setValue(sg.c?78:28); dg.property(25).setValue(sg.c?1.35:0.40);
      var ds=t.property("Effects").addProperty("ADBE Drop Shadow"); try{ ds.property(2).setValue(52); ds.property(3).setValue(135); ds.property(4).setValue(8); ds.property(5).setValue(14); }catch(ed){}
      x+=r.width; }
  }
  // seta para baixo: entra em "below", pulsa apontando o botao
  var seta=C.layers.addShape(); seta.name="SETA"; seta.motionBlur=true;
  var g=seta.property("Contents").addProperty("ADBE Vector Group"); var pth=g.property("Contents").addProperty("ADBE Vector Shape - Group");
  var sh=new Shape(); sh.vertices=[[-16,-70],[16,-70],[16,10],[54,10],[0,70],[-54,10],[-16,10]]; sh.closed=true;
  pth.property("ADBE Vector Shape").setValue(sh);
  var fl=g.property("Contents").addProperty("ADBE Vector Graphic - Fill"); fl.property("ADBE Vector Fill Color").setValue([0.40,0.44,1.0,1]);
  var yS=Math.min(985, ys[2]+Math.round(base*1.55));
  seta.property("Transform").property("Position").setValue([540,yS]);
  seta.inPoint=T_SETA;
  var os=seta.property("Transform").property("Opacity"); os.setValueAtTime(T_SETA,0); os.setValueAtTime(T_SETA+0.22,100); suave(os);
  var ss=seta.property("Transform").property("Scale"); ss.setValueAtTime(T_SETA,[60,60]); ss.setValueAtTime(T_SETA+0.30,[100,100]); suave(ss,18,84);
  var ps=seta.property("Transform").property("Position");
  var tt=T_SETA+0.30, k=0; while(tt<DUR){ ps.setValueAtTime(tt,[540,yS+(k%2?0:18)]); tt+=0.42; k++; } suave(ps,50,50);
  var dgs=seta.property("Effects").addProperty("PEDG2"); dgs.property(24).setValue(70); dgs.property(25).setValue(1.2);
  var cam=C.layers.addCamera("CAM",[540,540]); cam.moveToBeginning();
  cam.property("Transform").property("Anchor Point").setValue([540,540,0]); cam.property("Transform").property("Position").setValue([540,540,-1500]);
  // provas
  C.saveFrameToPng(0.55,new File("/tmp/cta_a.png")); C.saveFrameToPng(1.40,new File("/tmp/cta_b.png")); C.saveFrameToPng(3.20,new File("/tmp/cta_c.png")); C.saveFrameToPng(DUR-0.2,new File("/tmp/cta_d.png"));
  app.project.save();
  out.push("DR 08 CTA FINAL: "+DUR+"s | corpo "+base+"px | seta em "+T_SETA+"s | camadas="+C.numLayers);
  var f=new File("/tmp/ae_cta.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_cta.txt"); fe.open("w"); fe.write("ERRO: "+e.toString()+" linha "+e.line); fe.close(); }
})();
