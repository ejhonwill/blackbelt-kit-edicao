(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  function pasta(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof FolderItem&&x.name===n)return x;}return p.items.addFolder(n);}
  var FONTE="HelveticaNeue-Bold";
  var D=[__DEPOIMENTOS__];
  var nc=0;
  for(var d=0;d<D.length;d++){
    var dd=D[d];
    var f=new File(dd.arq);
    if(!f.exists){ out.push("FALTA "+dd.nome); continue; }
    var item=null;
    for(var q=1;q<=p.numItems;q++){ var x=p.item(q); if(x instanceof FootageItem && x.name===dd.nome) item=x; }
    if(!item){ item=p.importFile(new ImportOptions(f)); item.parentFolder=pasta("01 MATERIAL"); item.name=dd.nome; }
    var C=comp(dd.comp); if(C) C.remove();
    C=p.items.addComp(dd.comp,1080,1080,1,item.duration,25);
    C.parentFolder=pasta("02 COMPS");
    var v=C.layers.add(item); v.name="VIDEO";
    var esc=1080/item.width*100;
    v.property("Transform").property("Scale").setValue([esc,esc]);

    // depoimento leva SO legenda: sem lettering, sem b-roll
    var nl=0;
    for(var g=0;g<dd.LG.length;g++){
      var G=dd.LG[g];
      var tl=C.layers.addText(G.s);
      var td=tl.property("Source Text").value;
      td.fontSize=54; td.font=FONTE; td.applyFill=true; td.fillColor=[0.07,0.07,0.09]; td.applyStroke=false;
      td.justification=ParagraphJustification.CENTER_JUSTIFY; td.tracking=-8;
      tl.property("Source Text").setValue(td);
      var r=tl.sourceRectAtTime(0,false);
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
      nl++;
    }
    for(var z=1;z<=C.numLayers;z++){ if(C.layer(z).name==="VIDEO"){ C.layer(z).moveToEnd(); break; } }
    out.push(dd.comp+": "+C.duration.toFixed(2)+"s, "+nl+" legendas, "+C.numLayers+" camadas");
    nc++;
  }
  out.unshift("depoimentos montados="+nc);
  app.project.save();
  var fo=new File("/tmp/ae_dep.txt"); fo.open("w"); fo.write(out.join(String.fromCharCode(10))); fo.close();
 }catch(e){ var fe=new File("/tmp/ae_dep.txt"); fe.open("w"); fe.write("ERRO: "+e.toString()+" linha "+e.line); fe.close(); }
})();
