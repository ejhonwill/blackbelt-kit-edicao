(function(){
 try{
  var p=app.project; var out=[];
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var cc=comp("CARD T01");
  out.push("comp "+cc.width+"x"+cc.height+" dur="+cc.duration.toFixed(2)+" camadas="+cc.numLayers);
  for(var i=1;i<=cc.numLayers;i++){
    var L=cc.layer(i);
    var a=L.property("Transform").property("Anchor Point").value;
    var q=L.property("Transform").property("Position").value;
    var s=L.property("Transform").property("Scale").value;
    var linha=i+" ["+L.name+"] 3D="+(L.threeDLayer?1:0)+" anc=["+a.join(",")+"] pos=["+q.join(",")+"] esc="+s[0];
    if(L instanceof CameraLayer){
      try{ linha+=" POI=["+L.property("Transform").property("Point of Interest").value.join(",")+"]"; }catch(e){}
      try{ linha+=" zoom="+L.property("Camera Options").property("Zoom").value.toFixed(1); }catch(e2){}
    }
    if(L.parent) linha+=" pai="+L.parent.name;
    if(L.name.indexOf("TXT ")===0){
      var r=L.sourceRectAtTime(cc.duration-0.05,false);
      linha+=" rect(l="+r.left.toFixed(1)+",w="+r.width.toFixed(1)+",t="+r.top.toFixed(1)+",h="+r.height.toFixed(1)+")";
      var td=L.property("Source Text").value;
      linha+=" just="+td.justification;
    }
    out.push(linha);
  }
  var f=new File("/tmp/ae_diag.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_diag.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
