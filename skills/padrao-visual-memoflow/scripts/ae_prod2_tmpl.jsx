(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var C=comp("DR 01 ABERTURA"), PH=comp("PRODUTO HERO");
  if(!PH) throw new Error("sem PRODUTO HERO");
  var DIS=0.22, FADE=0.18;
  for(var k=C.numLayers;k>=1;k--){ if(C.layer(k).name.indexOf("PROD")===0) C.layer(k).remove(); }
  var D=[__DADOS__]; var n=0;
  for(var j=0;j<D.length;j++){
    var d=D[j];
    var l=C.layers.add(PH); l.name=d.n; l.motionBlur=true;
    var ini=d.i-DIS;
    l.startTime=ini; l.inPoint=ini; l.outPoint=d.o;
    var op=l.property("Transform").property("Opacity");
    while(op.numKeys>0) op.removeKey(1);
    op.setValueAtTime(ini,0); op.setValueAtTime(d.i,100);
    if(d.u){ op.setValueAtTime(d.o-FADE,100); op.setValueAtTime(d.o,0); } else op.setValueAtTime(d.o,100);
    for(var e=1;e<=op.numKeys;e++){ try{ op.setInterpolationTypeAtKey(e,KeyframeInterpolationType.BEZIER,KeyframeInterpolationType.BEZIER); }catch(er){} }
    l.moveToBeginning(); n++;
  }
  // a legenda tem de ficar por cima do produto
  for(var z=C.numLayers;z>=1;z--){ var nm=C.layer(z).name;
    if(nm.indexOf("LEG ")===0||nm.indexOf("PIL ")===0) C.layer(z).moveToBeginning(); }
  out.push("beats de produto recolocados="+n+" camadas="+C.numLayers);
  app.project.save();
  var f=new File("/tmp/ae_prod2.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_prod2.txt"); fe.open("w"); fe.write("ERRO "+e.toString()+" linha "+e.line); fe.close(); }
})();
