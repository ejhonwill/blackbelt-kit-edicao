(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var B=comp("MEMOFLOW_BOTTLE_CUTOUT");
  out.push("camadas de "+B.name+":");
  for(var i=1;i<=B.numLayers;i++){
    var L=B.layer(i);
    var s="  "+i+" ["+L.name+"] ativo="+L.enabled+" mistura="+L.blendingMode+" op="+L.property("Transform").property("Opacity").value;
    try{ var sc=L.property("Transform").property("Scale").value; s+=" esc="+sc[0].toFixed(0); }catch(e){}
    try{ var q=L.property("Transform").property("Position").value; s+=" pos="+q[0].toFixed(0)+","+q[1].toFixed(0); }catch(e){}
    try{ s+=" matte="+L.trackMatteType; }catch(e){}
    try{ if(L.source) s+=" fonte="+L.source.name+" "+(L.source.width||0)+"x"+(L.source.height||0); }catch(e){}
    out.push(s);
  }
  // renderiza com e sem as camadas de brilho
  B.saveFrameToPng(1.6, new File("/tmp/iso_todos.png"));
  var guard=[];
  for(var k=1;k<=B.numLayers;k++){
    var n=B.layer(k).name;
    if(n==="SWEEP"||n==="LIGHT WRAP"){ guard.push([k,B.layer(k).enabled]); B.layer(k).enabled=false; }
  }
  B.saveFrameToPng(1.6, new File("/tmp/iso_semluz.png"));
  for(var g=0;g<guard.length;g++) B.layer(guard[g][0]).enabled=guard[g][1];
  var f=new File("/tmp/ae_iso.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_iso.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
