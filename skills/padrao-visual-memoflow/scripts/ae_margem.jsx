(function(){
 try{
  var p=app.project; var out=[]; var ZI=80, ZF=-210, ZOOM=1500, SEGURO=940;
  var n=0, red=0;
  for(var c=1;c<=p.numItems;c++){
    var cc=p.item(c);
    if(!(cc instanceof CompItem) || cc.name.indexOf("CARD ")!==0) continue;
    var ctrl=null;
    for(var i=1;i<=cc.numLayers;i++){ if(cc.layer(i).name==="CTRL"){ ctrl=cc.layer(i); break; } }
    if(!ctrl) continue;
    var cp=ctrl.property("Transform").property("Position");
    while(cp.numKeys>0) cp.removeKey(1);
    cp.setValueAtTime(0,[540,540,ZI]);
    cp.setValueAtTime(cc.duration,[540,540,ZF]);
    try{ cp.setInterpolationTypeAtKey(1,KeyframeInterpolationType.BEZIER,KeyframeInterpolationType.BEZIER); }catch(e0){}

    // largura do bloco no quadro final, ja com a ampliacao da camera
    var tm=cc.duration-0.05, W=0;
    for(var t=1;t<=cc.numLayers;t++){
      var L=cc.layer(t); if(L.name.indexOf("TXT ")!==0) continue;
      var r=L.sourceRectAtTime(tm,false), v=L.property("Transform").property("Position").value;
      W=Math.max(W, 2*Math.abs(v[0]+r.left), 2*Math.abs(v[0]+r.left+r.width));
    }
    var mag=ZOOM/(ZOOM+ZF);
    var fator=SEGURO/(W*mag);
    var esc=(fator<1)? fator*100 : 100;
    ctrl.property("Transform").property("Scale").setValue([esc,esc,100]);
    if(fator<1) red++;
    out.push(cc.name+" bloco="+Math.round(W)+"px final="+Math.round(W*mag*esc/100)+"px escala="+Math.round(esc)+"%");
    n++;
  }
  out.unshift("titulos="+n+" | reduzidos para caber na margem="+red);
  app.project.save();
  var f=new File("/tmp/ae_marg.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_marg.txt"); fe.open("w"); fe.write("ERRO "+e.toString()+" linha "+e.line); fe.close(); }
})();
