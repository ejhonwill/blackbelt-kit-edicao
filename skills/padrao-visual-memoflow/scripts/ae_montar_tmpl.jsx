(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  function pasta(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof FolderItem&&x.name===n)return x;}return p.items.addFolder(n);}
  function suave(P,ent,sai){ for(var z=1;z<=P.numKeys;z++){ try{
      P.setInterpolationTypeAtKey(z,KeyframeInterpolationType.BEZIER,KeyframeInterpolationType.BEZIER);
      P.setTemporalEaseAtKey(z,[new KeyframeEase(0,ent||70)],[new KeyframeEase(0,sai||70)]); }catch(e){} } }

  var SECAO="__SECAO__", PREFIXO="__PREFIXO__", DIR="__DIR__";
  var C=comp(SECAO); if(!C) throw new Error("sem a comp "+SECAO);
  var DIS=0.22, FADE=0.18, ENT=0.34, DESL=44, BORR=46;

  // limpa tudo menos o video base
  for(var k=C.numLayers;k>=1;k--){ if(C.layer(k).name!=="VIDEO") C.layer(k).remove(); }
  var bB=pasta("06 BROLL");

  var PL=[__PLANO__];
  var CICLO=["D","C","B"], nd=0;
  var nb=0, nc=0, faltou=[];
  for(var i=0;i<PL.length;i++){
    var d=PL[i], L=null;
    var ini=Math.max(0, d.i-DIS);
    if(d.tipo==="BR"){
      var f=new File(DIR+"/broll/"+d.id+".mp4");
      if(!f.exists){ faltou.push(d.id); continue; }
      var item=null, nome=PREFIXO+"_"+d.id+".mp4";
      for(var q=1;q<=p.numItems;q++){ var x=p.item(q); if(x instanceof FootageItem && x.name===nome) item=x; }
      if(!item){ item=p.importFile(new ImportOptions(f)); item.parentFolder=bB; item.name=nome; }
      try{ item.mainSource.conformFrameRate=25; }catch(e0){}
      L=C.layers.add(item); L.name="BR "+d.id; L.audioEnabled=false;
      var esc=1080/item.width*100;
      L.startTime=Math.min(ini, d.i-0.6);
      L.inPoint=ini; L.outPoint=d.o;
      var dir=CICLO[nd%3]; nd++;
      var dx=(dir==="D")?DESL:0, dy=(dir==="C")?-DESL:((dir==="B")?DESL:0);
      var t1=Math.min(ini+ENT, d.o-0.04);
      var pp=L.property("Transform").property("Position");
      pp.setValueAtTime(ini,[540+dx,540+dy]); pp.setValueAtTime(t1,[540,540]);
      var sc=L.property("Transform").property("Scale");
      sc.setValueAtTime(ini,[esc*1.10,esc*1.10]); sc.setValueAtTime(t1,[esc,esc]);
      sc.setValueAtTime(d.o,[esc*1.035,esc*1.035]);
      suave(pp,18,85); suave(sc,18,85);
      var db=L.property("Effects").addProperty("ADBE Motion Blur");
      db.property(1).setValue((dir==="D")?90:0);
      var cl=db.property(2); cl.setValueAtTime(ini,BORR); cl.setValueAtTime(t1,0); suave(cl,70,70);
      nb++;
    }else{
      var cc=comp("CARD "+d.id);
      if(!cc){ faltou.push("CARD "+d.id); continue; }
      L=C.layers.add(cc); L.name="CARD "+d.id;
      L.startTime=d.i; L.inPoint=ini; L.outPoint=d.o;
      nc++;
    }
    L.motionBlur=true;
    var op=L.property("Transform").property("Opacity");
    while(op.numKeys>0) op.removeKey(1);
    op.setValueAtTime(ini,0); op.setValueAtTime(d.i,100);
    if(d.ultimo || d.sobre){ op.setValueAtTime(Math.max(d.i+0.1,d.o-FADE),100); op.setValueAtTime(d.o,0); }
    else op.setValueAtTime(d.o,100);
    suave(op,70,70);
  }

  // ---- legenda corrida: pilula branca, texto escuro ----
  var LG=[__LEGENDAS__];
  var CART=[__CARTAS__];
  var FONTE="HelveticaNeue-Bold", nl=0, pulou=0;
  for(var g=0;g<LG.length;g++){
    var G=LG[g];
    var sobreposto=false;
    for(var c=0;c<CART.length;c++){
      var o=Math.min(G.f,CART[c].b)-Math.max(G.t,CART[c].a);
      if(o > (G.f-G.t)*0.6){ sobreposto=true; break; }
    }
    if(sobreposto){ pulou++; continue; }          // onde tem lettering nao precisa de legenda
    var tl=C.layers.addText(G.s);
    var td=tl.property("Source Text").value;
    td.fontSize=54; td.font=FONTE; td.applyFill=true; td.fillColor=[0.07,0.07,0.09]; td.applyStroke=false;
    td.justification=ParagraphJustification.CENTER_JUSTIFY; td.tracking=-8;
    tl.property("Source Text").setValue(td);
    var r=tl.sourceRectAtTime(0,false);
    tl.name="LEG "+(g+1);
    tl.property("Transform").property("Position").setValue([540,952]);
    tl.startTime=G.t; tl.inPoint=G.t; tl.outPoint=G.f;
    var fi=tl.property("Effects").addProperty("ADBE Fill");
    for(var w=1;w<=fi.numProperties;w++){ var pr=fi.property(w);
      if(pr.propertyValueType===PropertyValueType.COLOR){ pr.setValue([0.07,0.07,0.09,1]); break; } }
    var sol=C.layers.addShape(); sol.name="PIL "+(g+1);
    var grp=sol.property("Contents").addProperty("ADBE Vector Group");
    var ret=grp.property("Contents").addProperty("ADBE Vector Shape - Rect");
    ret.property("ADBE Vector Rect Size").setValue([r.width+56, r.height+34]);
    ret.property("ADBE Vector Rect Roundness").setValue((r.height+34)/2);
    var fil=grp.property("Contents").addProperty("ADBE Vector Graphic - Fill");
    fil.property("ADBE Vector Fill Color").setValue([1,1,1,1]);
    sol.property("Transform").property("Position").setValue([540, 952-r.height/2-2]);
    sol.property("Transform").property("Opacity").setValue(94);
    sol.startTime=G.t; sol.inPoint=G.t; sol.outPoint=G.f;
    tl.moveBefore(sol);                           // texto sempre acima da pilula
    nl++;
  }

  // ordem: legenda no topo, cartelas, b-roll, VIDEO no fundo
  function fim(pre){ for(var z=C.numLayers;z>=1;z--){ if(C.layer(z).name.indexOf(pre)===0) C.layer(z).moveToEnd(); } }
  fim("CARD "); fim("BR ");
  for(var v=1;v<=C.numLayers;v++){ if(C.layer(v).name==="VIDEO"){ C.layer(v).moveToEnd(); break; } }
  C.motionBlur=true; try{ C.shutterAngle=180; C.shutterPhase=-90; }catch(e5){}

  out.push(SECAO+": b-roll="+nb+" cartelas="+nc+" legendas="+nl+" (puladas sobre lettering="+pulou+")");
  out.push("camadas="+C.numLayers+(faltou.length? (" | FALTOU: "+faltou.join(",")) : " | nada faltando"));
  app.project.save();
  var f2=new File("/tmp/ae_mont_"+PREFIXO+".txt"); f2.open("w"); f2.write(out.join(String.fromCharCode(10))); f2.close();
 }catch(e){ var fe=new File("/tmp/ae_mont___PREFIXO__.txt"); fe.open("w"); fe.write("ERRO: "+e.toString()+" linha "+e.line); fe.close(); }
})();
