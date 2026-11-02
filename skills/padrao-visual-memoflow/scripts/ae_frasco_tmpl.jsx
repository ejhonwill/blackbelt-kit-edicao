(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  function pasta(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof FolderItem&&x.name===n)return x;}return p.items.addFolder(n);}
  function elipse(L,cx,cy,rx,ry,pena){
    var m=L.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
    var k=0.5523, V=[],I=[],T=[];
    for(var a=0;a<8;a++){
      var th=Math.PI*2*a/8;
      V.push([cx+rx*Math.cos(th), cy+ry*Math.sin(th)]);
      var tx=-rx*Math.sin(th)*k*Math.PI*2/8, ty=ry*Math.cos(th)*k*Math.PI*2/8;
      T.push([tx,ty]); I.push([-tx,-ty]);
    }
    var s=new Shape(); s.vertices=V; s.inTangents=I; s.outTangents=T; s.closed=true;
    m.property("ADBE Mask Shape").setValue(s);
    m.property("ADBE Mask Feather").setValue([pena,pena]);
    return m;
  }

  // ---- recorte importado ----
  var fr=null;
  for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof FootageItem && x.name==="MEMOFLOW_FRASCO_RECORTE.png") fr=x; }
  if(!fr){
    var f=new File("__RECORTE__");
    if(!f.exists) throw new Error("recorte nao encontrado");
    fr=p.importFile(new ImportOptions(f)); fr.parentFolder=pasta("01 MATERIAL");
  }
  try{ fr.mainSource.alphaMode=AlphaMode.STRAIGHT; }catch(e0){ out.push("alfa: "+e0.toString()); }

  // ---- MEMOFLOW_BOTTLE_CUTOUT ----
  var B=comp("MEMOFLOW_BOTTLE_CUTOUT"); if(B) B.remove();
  B=p.items.addComp("MEMOFLOW_BOTTLE_CUTOUT",1080,1080,1,5,25);
  B.parentFolder=pasta("04 INSERTS"); B.motionBlur=true;
  var ESC=44, CX=540, CY=500;

  // glow atras: mancha azul-violeta, nunca um circulo duro
  var gl=B.layers.addSolid([0.30,0.34,1.0],"GLOW FUNDO",1080,1080,1);
  elipse(gl,CX,CY+30,300,430,240);
  gl.blendingMode=BlendingMode.ADD;
  gl.property("Transform").property("Opacity").setValue(52);
  var gb=gl.property("Effects").addProperty("ADBE Box Blur2"); gb.property(1).setValue(60); gb.property(2).setValue(3);

  // sombra de apoio, so para assentar o produto
  var so=B.layers.addSolid([0,0,0],"SOMBRA",1080,1080,1);
  elipse(so,CX,CY+404,230,52,90);
  so.property("Transform").property("Opacity").setValue(64);

  // frasco
  var fa=B.layers.add(fr); fa.name="FRASCO";
  fa.property("Transform").property("Scale").setValue([ESC,ESC]);
  fa.property("Transform").property("Position").setValue([CX,CY]);

  // light wrap: fio de luz azul por dentro da borda do vidro
  var lw=B.layers.add(fr); lw.name="LIGHT WRAP";
  lw.property("Transform").property("Scale").setValue([ESC,ESC]);
  lw.property("Transform").property("Position").setValue([CX,CY]);
  var fi=lw.property("Effects").addProperty("ADBE Fill");
  try{ fi.property("ADBE Fill-0002").setValue([0.42,0.56,1,1]); }catch(e1){ try{ fi.property(3).setValue([0.42,0.56,1,1]); }catch(e2){ out.push("fill: "+e2.toString()); } }
  var lb=lw.property("Effects").addProperty("ADBE Box Blur2"); lb.property(1).setValue(16); lb.property(2).setValue(3);
  lw.blendingMode=BlendingMode.ADD;
  lw.property("Transform").property("Opacity").setValue(34);
  lw.moveBefore(fa);

  // brilho passando pelo vidro, recortado no proprio frasco
  var mt=B.layers.add(fr); mt.name="FRASCO MATTE"; mt.enabled=false;
  mt.property("Transform").property("Scale").setValue([ESC,ESC]);
  mt.property("Transform").property("Position").setValue([CX,CY]);
  var sw=B.layers.addSolid([1,1,1],"SWEEP",260,1200,1);
  sw.blendingMode=BlendingMode.ADD; sw.motionBlur=true;
  sw.property("Transform").property("Rotation").setValue(16);
  sw.property("Transform").property("Opacity").setValue(26);
  var sp=sw.property("Transform").property("Position");
  sp.setValueAtTime(0.7,[200,CY]); sp.setValueAtTime(2.6,[900,CY]);
  var sb=sw.property("Effects").addProperty("ADBE Box Blur2"); sb.property(1).setValue(60); sb.property(2).setValue(3);
  sw.moveBefore(mt);
  try{ sw.setTrackMatte(mt, TrackMatteType.ALPHA); out.push("sweep recortado no frasco"); }
  catch(e3){ out.push("matte do sweep: "+e3.toString()); }

  // ---- PRODUTO HERO: fundo da marca + entrada do frasco ----
  var BG=comp("BG LETTERING");
  var PH=comp("PRODUTO HERO"); if(PH) PH.remove();
  PH=p.items.addComp("PRODUTO HERO",1080,1080,1,4,25); PH.parentFolder=pasta("04 INSERTS"); PH.motionBlur=true;
  if(BG){ var lb2=PH.layers.add(BG); lb2.name="BGL"; lb2.property("Transform").property("Scale").setValue([120,120]); }
  var lf=PH.layers.add(B); lf.name="FRASCO"; lf.motionBlur=true;
  var T0=0.0, T1=0.34, T2=0.50;
  var pp=lf.property("Transform").property("Position");
  pp.setValueAtTime(T0,[540+190,540+46]); pp.setValueAtTime(T1,[540-13,540-4]); pp.setValueAtTime(T2,[540,540]);
  var sc=lf.property("Transform").property("Scale");
  sc.setValueAtTime(T0,[113,113]); sc.setValueAtTime(T1,[98.5,98.5]); sc.setValueAtTime(T2,[100,100]);
  sc.setValueAtTime(4,[103,103]);
  function suave(P){ for(var z=1;z<=P.numKeys;z++){ try{
    P.setInterpolationTypeAtKey(z,KeyframeInterpolationType.BEZIER,KeyframeInterpolationType.BEZIER);
    P.setTemporalEaseAtKey(z,[new KeyframeEase(0,z===1?16:84)],[new KeyframeEase(0,z===1?16:84)]); }catch(e4){} } }
  suave(pp); suave(sc);
  var db=lf.property("Effects").addProperty("ADBE Motion Blur");
  db.property(1).setValue(76);                       // acompanha a diagonal de entrada
  var cl=db.property(2);
  cl.setValueAtTime(T0,52); cl.setValueAtTime(T1,6); cl.setValueAtTime(T2,0);
  for(var e5=1;e5<=cl.numKeys;e5++){ try{ cl.setInterpolationTypeAtKey(e5,KeyframeInterpolationType.BEZIER,KeyframeInterpolationType.BEZIER); }catch(e6){} }

  // ---- na abertura: PROD so dissolve, quem se move e o frasco dentro ----
  var C=comp("DR 01 ABERTURA"); var np=0;
  for(var q=1;q<=C.numLayers;q++){
    var l=C.layer(q); if(l.name.indexOf("PROD")!==0) continue;
    if(l.source!==PH) l.replaceSource(PH,false);
    var P1=l.property("Transform").property("Position"); while(P1.numKeys>0) P1.removeKey(1); P1.setValue([540,540]);
    var S1=l.property("Transform").property("Scale");   while(S1.numKeys>0) S1.removeKey(1); S1.setValue([100,100]);
    for(var f2=l.property("Effects").numProperties;f2>=1;f2--){
      if(l.property("Effects").property(f2).matchName==="ADBE Motion Blur") l.property("Effects").property(f2).remove();
    }
    l.motionBlur=true; np++;
  }
  // o selo branco sobre o medico vira o recorte
  for(var s2=1;s2<=C.numLayers;s2++){
    var sl=C.layer(s2); if(sl.name!=="SELO FRASCO") continue;
    if(sl.source!==fr) sl.replaceSource(fr,false);
    sl.property("Transform").property("Scale").setValue([16,16]);
    sl.property("Transform").property("Position").setValue([842,726]);
    out.push("selo trocado pelo recorte");
  }
  out.push("PRODUTO HERO refeito | camadas PROD na abertura="+np);
  app.project.save();
  var fo=new File("/tmp/ae_frasco.txt"); fo.open("w"); fo.write(out.join(String.fromCharCode(10))); fo.close();
 }catch(e){ var fe=new File("/tmp/ae_frasco.txt"); fe.open("w"); fe.write("ERRO "+e.toString()+" linha "+e.line); fe.close(); }
})();
