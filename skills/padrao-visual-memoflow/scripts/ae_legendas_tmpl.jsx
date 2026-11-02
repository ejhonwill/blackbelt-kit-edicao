(function(){
 try{
  var out=[]; var p=app.project; var LIM=980;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var FONTE="HelveticaNeue-Bold";
  var D=[__DADOS__]; var total=0, encolhidas=0;
  for(var d=0;d<D.length;d++){
    var dd=D[d]; var C=comp(dd.comp);
    if(!C){ out.push("sem comp "+dd.comp); continue; }
    for(var k=C.numLayers;k>=1;k--){ var nm=C.layer(k).name;
      if(nm.indexOf("LEG ")===0||nm.indexOf("PIL ")===0) C.layer(k).remove(); }
    var n=0;
    for(var g=0;g<dd.LG.length;g++){
      var G=dd.LG[g];
      var tl=C.layers.addText(G.s);
      var td=tl.property("Source Text").value;
      td.fontSize=54; td.font=FONTE; td.applyFill=true; td.fillColor=[0.07,0.07,0.09]; td.applyStroke=false;
      td.justification=ParagraphJustification.CENTER_JUSTIFY; td.tracking=-8;
      tl.property("Source Text").setValue(td);
      // encolhe so o que nao cabe na margem
      var r=tl.sourceRectAtTime(0,false), corpo=54;
      while(corpo>38 && r.width+56>LIM){
        corpo-=2; td=tl.property("Source Text").value; td.fontSize=corpo;
        tl.property("Source Text").setValue(td); r=tl.sourceRectAtTime(0,false);
      }
      if(corpo<54) encolhidas++;
      tl.name="LEG "+(g+1);
      tl.property("Transform").property("Position").setValue([540,952]);
      tl.startTime=G.t; tl.inPoint=G.t; tl.outPoint=Math.min(G.f, C.duration);
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
      sol.startTime=G.t; sol.inPoint=G.t; sol.outPoint=Math.min(G.f, C.duration);
      tl.moveBefore(sol);
      n++; total++;
    }
    // texto ja nasce logo acima da sua pilula (moveBefore por par); so o VIDEO vai para o fundo
    for(var v=1;v<=C.numLayers;v++){ if(C.layer(v).name==="VIDEO"){ C.layer(v).moveToEnd(); break; } }
    out.push("  "+dd.comp+": "+n+" legendas");
  }
  out.unshift("legendas refeitas="+total+" | encolhidas para caber="+encolhidas);
  app.project.save();
  var f=new File("/tmp/ae_legtodas.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_legtodas.txt"); fe.open("w"); fe.write("ERRO: "+e.toString()+" linha "+e.line); fe.close(); }
})();
