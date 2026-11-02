(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var C=comp("DR 01 TAKE FRASCO");
  var gl=null;
  for(var i=1;i<=C.numLayers;i++){ if(C.layer(i).name==="GLOW") gl=C.layer(i); }
  if(!gl) throw new Error("sem GLOW");
  // mancha menor e mais contida: o glow separa o vidro do fundo, nao ilumina a cena
  var mp=gl.property("ADBE Mask Parade");
  while(mp.numProperties>0) mp.property(1).remove();
  var m=mp.addProperty("ADBE Mask Atom");
  var k=0.5523,V=[],I=[],T=[],cx=540,cy=575,rx=196,ry=302;
  for(var a=0;a<8;a++){ var th=Math.PI*2*a/8;
    V.push([cx+rx*Math.cos(th), cy+ry*Math.sin(th)]);
    var tx=-rx*Math.sin(th)*k*Math.PI*2/8, ty=ry*Math.cos(th)*k*Math.PI*2/8;
    T.push([tx,ty]); I.push([-tx,-ty]); }
  var s=new Shape(); s.vertices=V; s.inTangents=I; s.outTangents=T; s.closed=true;
  m.property("ADBE Mask Shape").setValue(s);
  m.property("ADBE Mask Feather").setValue([165,165]);
  var op=gl.property("Transform").property("Opacity");
  for(var e=1;e<=op.numKeys;e++){
    var v=op.keyValue(e); if(v>1) op.setValueAtKey(e, Math.round(v*0.55));
  }
  for(var f=gl.property("Effects").numProperties;f>=1;f--){
    if(gl.property("Effects").property(f).matchName==="ADBE Box Blur2") gl.property("Effects").property(f).remove();
  }
  var b=gl.property("Effects").addProperty("ADBE Box Blur2"); b.property(1).setValue(52); b.property(2).setValue(3);

  // o escurecimento segura o fundo sem precisar do glow
  for(var j=1;j<=C.numLayers;j++){
    if(C.layer(j).name!=="ESCURECER") continue;
    var oe=C.layer(j).property("Transform").property("Opacity");
    for(var e2=1;e2<=oe.numKeys;e2++){ var v2=oe.keyValue(e2); if(v2>1) oe.setValueAtKey(e2, 66); }
  }
  var vals=[];
  for(var e3=1;e3<=op.numKeys;e3++) vals.push(Math.round(op.keyValue(e3)));
  out.push("glow: elipse 196x302, pena 165, desfoque 52, opacidade "+vals.join("/"));
  app.project.save();
  var fo=new File("/tmp/ae_glow.txt"); fo.open("w"); fo.write(out.join(String.fromCharCode(10))); fo.close();
 }catch(e){ var fe=new File("/tmp/ae_glow.txt"); fe.open("w"); fe.write("ERRO "+e.toString()+" linha "+e.line); fe.close(); }
})();
