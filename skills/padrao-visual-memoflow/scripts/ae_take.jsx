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

  var DR=midia("DR 01 ABERTURA"), FR=comp("MEMOFLOW_BOTTLE_CUTOUT");
  if(!DR) throw new Error("sem a midia do medico");
  if(!FR) throw new Error("sem MEMOFLOW_BOTTLE_CUTOUT");

  // --- tempos (locais; o take comeca em 4,10 na abertura) ---
  var T0=4.10, DUR=3.40;
  var E0=0.06, E1=0.50, E2=0.70;     // entrada: 11 quadros ate o pouso, 5 de acomodacao
  var S0=2.50, S1=3.10;              // volta ao medico
  var ZOOM=1500;                      // 50 mm num quadro de 1080
  var ZFUNDO=400, ZESC=300, ZGLOW=150, ZLONGE=1400, ZPERTO=-40, ZOVER=-95;

  var C=comp("DR 01 TAKE FRASCO"); if(C) C.remove();
  C=p.items.addComp("DR 01 TAKE FRASCO",1080,1080,1,DUR,25);
  C.parentFolder=pasta("04 INSERTS"); C.motionBlur=true;
  try{ C.shutterAngle=180; C.shutterPhase=-90; }catch(e0){}

  // --- fundo: o medico, atras no eixo Z ---
  var fu=C.layers.add(DR); fu.name="FUNDO MEDICO";
  fu.startTime=-T0; fu.inPoint=0; fu.outPoint=DUR;
  fu.threeDLayer=true;
  var mag=ZOOM/(ZOOM+ZFUNDO);
  var escFundo=103.1/mag;
  fu.property("Transform").property("Position").setValue([540,540,ZFUNDO]);
  fu.property("Transform").property("Scale").setValue([escFundo,escFundo,100]);
  fu.audioEnabled=false;                       // o audio ja vem da abertura
  var bf=fu.property("Effects").addProperty("ADBE Box Blur2");
  var rb=bf.property(1);
  rb.setValueAtTime(0,0); rb.setValueAtTime(E1,26); rb.setValueAtTime(S0,26); rb.setValueAtTime(S1,0);
  bf.property(2).setValue(3); suave(rb,70,70);

  // --- escurecimento ---
  var es=C.layers.addSolid([0.01,0.012,0.03],"ESCURECER",1080,1080,1);
  es.threeDLayer=true;
  var magE=ZOOM/(ZOOM+ZESC);
  es.property("Transform").property("Position").setValue([540,540,ZESC]);
  es.property("Transform").property("Scale").setValue([100/magE,100/magE,100]);
  var oe=es.property("Transform").property("Opacity");
  oe.setValueAtTime(0,0); oe.setValueAtTime(E1,58); oe.setValueAtTime(S0,58); oe.setValueAtTime(S1,0);
  suave(oe,70,70);

  // --- glow atras do produto ---
  var gl=C.layers.addSolid([0.26,0.32,1.0],"GLOW",1080,1080,1);
  gl.threeDLayer=true; gl.blendingMode=BlendingMode.ADD;
  elipse(gl,540,560,290,400,250);
  var magG=ZOOM/(ZOOM+ZGLOW);
  gl.property("Transform").property("Position").setValue([540,560,ZGLOW]);
  var bg=100/magG;
  var sg=gl.property("Transform").property("Scale");
  sg.setValueAtTime(E0,[bg*0.72,bg*0.72,100]); sg.setValueAtTime(E2,[bg*1.12,bg*1.12,100]);
  sg.setValueAtTime(S0,[bg*1.18,bg*1.18,100]); sg.setValueAtTime(S1,[bg*0.72,bg*0.72,100]);
  var og=gl.property("Transform").property("Opacity");
  og.setValueAtTime(E0,0); og.setValueAtTime(E2,58); og.setValueAtTime(S0,52); og.setValueAtTime(S1-0.05,0);
  suave(sg,70,70); suave(og,70,70);
  var gb=gl.property("Effects").addProperty("ADBE Box Blur2"); gb.property(1).setValue(80); gb.property(2).setValue(3);

  // --- frasco: vem de longe pelo Z, sobe do rodape e resolve o foco ---
  var fa=C.layers.add(FR); fa.name="FRASCO";
  fa.threeDLayer=true; fa.motionBlur=true;
  fa.startTime=0; fa.inPoint=E0-0.04; fa.outPoint=S1;
  var ESCF=82;
  fa.property("Transform").property("Scale").setValue([ESCF,ESCF,100]);
  var pf=fa.property("Transform").property("Position");
  pf.setValueAtTime(E0,[540,1185,ZLONGE]);
  pf.setValueAtTime(E1,[540,578,ZOVER]);          // passa um pouco do ponto
  pf.setValueAtTime(E2,[540,593,ZPERTO]);         // acomoda
  pf.setValueAtTime(S0,[547,586,ZPERTO-18]);      // respiro durante a leitura
  pf.setValueAtTime(S1,[540,1185,ZLONGE]);
  suave(pf,16,86);
  var fb=fa.property("Effects").addProperty("ADBE Box Blur2");
  var rf=fb.property(1);
  rf.setValueAtTime(E0,22); rf.setValueAtTime(E1+0.06,0); rf.setValueAtTime(S0,0); rf.setValueAtTime(S1-0.06,24);
  fb.property(2).setValue(3); suave(rf,70,70);
  var db=fa.property("Effects").addProperty("ADBE Motion Blur");
  db.property(1).setValue(0);                      // o deslocamento e vertical
  var cl=db.property(2);
  cl.setValueAtTime(E0,44); cl.setValueAtTime(E1,4); cl.setValueAtTime(E2,0);
  cl.setValueAtTime(S0,0); cl.setValueAtTime(S1-0.06,38);
  suave(cl,70,70);

  // --- lettering em etapas, acima do frasco ---
  var FONTE="Montserrat-ExtraBold", BRANCO=[1,1,1], AZUL=[0.40,0.44,1.0];
  function texto(s,cor,tam,y,tEnt){
    var t=C.layers.addText(s);
    var d=t.property("Source Text").value;
    d.fontSize=tam; d.font=FONTE; d.applyFill=true; d.fillColor=cor; d.applyStroke=false;
    d.tracking=-14; d.justification=ParagraphJustification.LEFT_JUSTIFY;
    t.property("Source Text").setValue(d);
    var r=t.sourceRectAtTime(0,false);
    var px=540-r.width/2-r.left;
    t.threeDLayer=true; t.motionBlur=true;
    t.inPoint=tEnt; t.outPoint=S0+0.30;
    var pp=t.property("Transform").property("Position");
    pp.setValueAtTime(tEnt,[px,y+28,0]); pp.setValueAtTime(tEnt+0.24,[px,y,0]);
    var op=t.property("Transform").property("Opacity");
    op.setValueAtTime(tEnt,0); op.setValueAtTime(tEnt+0.20,100);
    op.setValueAtTime(S0+0.06,100); op.setValueAtTime(S0+0.30,0);
    var sc=t.property("Transform").property("Scale");
    sc.setValueAtTime(tEnt,[93,93,100]); sc.setValueAtTime(tEnt+0.26,[100,100,100]);
    suave(pp,18,84); suave(op,70,70); suave(sc,18,84);
    var dg=t.property("Effects").addProperty("PEDG2");
    dg.property(24).setValue(cor===AZUL?78:28);
    dg.property(25).setValue(cor===AZUL?1.35:0.4);
    return t;
  }
  var l2=texto("MEMOFLOW",AZUL,84,236,0.62); l2.name="LET MEMOFLOW";
  var l1=texto("CO-FOUNDER OF",BRANCO,52,152,0.30); l1.name="LET CO-FOUNDER";

  // --- camera 50 mm, com deriva minima durante a leitura ---
  var cam=C.layers.addCamera("CAM",[540,540]);
  cam.moveToBeginning();
  var TC=cam.property("Transform");
  TC.property("Anchor Point").setValue([540,540,0]);   // em camera o ancoragem E o ponto de interesse
  var pc=TC.property("Position");
  pc.setValueAtTime(0,[540,540,-ZOOM]);
  pc.setValueAtTime(E2,[540,540,-ZOOM+46]);
  pc.setValueAtTime(S0,[548,533,-ZOOM+70]);
  pc.setValueAtTime(S1,[540,540,-ZOOM]);
  suave(pc,70,70);
  try{ cam.property("Camera Options").property("Zoom").setValue(ZOOM); }catch(e1){ out.push("zoom: "+e1.toString()); }

  // --- entra na abertura no lugar do selo ---
  var A=comp("DR 01 ABERTURA");
  for(var k=A.numLayers;k>=1;k--){ var nm=A.layer(k).name; if(nm==="SELO FRASCO"||nm==="TAKE FRASCO") A.layer(k).remove(); }
  var lt=A.layers.add(C); lt.name="TAKE FRASCO"; lt.motionBlur=true;
  lt.startTime=T0; lt.inPoint=T0; lt.outPoint=T0+DUR;
  // fica sob a legenda e sobre o video
  for(var v=1;v<=A.numLayers;v++){ if(A.layer(v).name==="VIDEO"){ lt.moveBefore(A.layer(v)); break; } }

  out.push("take "+T0.toFixed(2)+"-"+(T0+DUR).toFixed(2)+" | pouso "+(T0+E2).toFixed(2)+" | volta "+(T0+S0).toFixed(2)+"-"+(T0+S1).toFixed(2));
  out.push("camadas no take="+C.numLayers+" | escala do fundo="+Math.round(escFundo)+"% | escala do frasco="+ESCF+"%");
  app.project.save();
  var f=new File("/tmp/ae_take.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_take.txt"); fe.open("w"); fe.write("ERRO: "+e.toString()+" linha "+e.line); fe.close(); }
})();
