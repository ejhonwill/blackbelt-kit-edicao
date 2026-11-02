(function(){
  var p=app.project; var out=[]; var C=null;
  for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof CompItem && x.name==="DR 01 ABERTURA") C=x; }
  for(var q=1;q<=C.numLayers;q++){
    var l=C.layer(q);
    if(l.name==="CARD T01"||l.name==="BR F01"){
      var pos=l.property("Transform").property("Position");
      var anc=l.property("Transform").property("Anchor Point");
      var esc=l.property("Transform").property("Scale");
      out.push(l.name+" 3D="+l.threeDLayer+" in="+l.inPoint.toFixed(2)+" out="+l.outPoint.toFixed(2));
      out.push("   pos.value="+pos.value.join(",")+"  pos@18.2="+pos.valueAtTime(18.2,false).join(","));
      out.push("   anchor="+anc.value.join(",")+"  scale="+esc.value.join(","));
      out.push("   fonte="+(l.source?l.source.name+" "+l.source.width+"x"+l.source.height:"?"));
      out.push("   numKeys pos="+pos.numKeys);
    }
  }
  var f=new File("/tmp/ae_diag4.txt"); f.open("w"); f.write(out.join("\n")); f.close();
})();
