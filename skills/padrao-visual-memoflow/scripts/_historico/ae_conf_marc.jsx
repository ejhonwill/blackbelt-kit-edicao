(function(){
  var p=app.project; var out=[]; var master=null;
  for(var i=1;i<=p.numItems;i++){ var it=p.item(i); if(it instanceof CompItem && it.name.indexOf("MASTER")>=0) master=it; }
  if(!master){ var f0=new File("/tmp/ae_conf.txt"); f0.open("w"); f0.write("sem master"); f0.close(); return; }
  var mp=master.markerProperty;
  out.push("master: " + mp.numKeys + " marcadores | dur " + master.duration.toFixed(2) + "s");
  for(var k=1;k<=mp.numKeys;k++){
    var t=mp.keyTime(k); var v=mp.keyValue(k);
    out.push("  " + t.toFixed(2) + "s  cor" + v.label + "  " + v.comment);
  }
  var f=new File("/tmp/ae_conf.txt"); f.open("w"); f.write(out.join("\n")); f.close();
})();
