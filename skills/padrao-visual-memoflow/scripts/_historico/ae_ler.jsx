(function(){
  var out=[]; var p=app.project;
  out.push("projeto=" + (p.file ? p.file.fsName : "sem arquivo"));
  out.push("itens=" + p.numItems);
  for (var i=1;i<=p.numItems;i++){
    var it=p.item(i); var t="?";
    if (it instanceof CompItem) t="COMP " + it.width + "x" + it.height + " " + it.duration.toFixed(3) + "s " + it.frameRate.toFixed(3) + "fps " + it.numLayers + "cam";
    else if (it instanceof FolderItem) t="PASTA";
    else if (it instanceof FootageItem) t="FOOTAGE " + it.width + "x" + it.height + " " + it.duration.toFixed(3) + "s";
    out.push("  [" + i + "] " + it.name + " | " + t);
  }
  for (var j=1;j<=p.numItems;j++){
    var c=p.item(j);
    if (c instanceof CompItem && c.name.indexOf("MASTER")>=0){
      for (var k=1;k<=c.numLayers;k++){
        var l=c.layer(k);
        out.push("  master cam" + k + ": " + l.name + " in=" + l.inPoint.toFixed(2) + " out=" + l.outPoint.toFixed(2) + " start=" + l.startTime.toFixed(2));
      }
    }
  }
  var f=new File("/tmp/ae_estado.txt"); f.open("w"); f.write(out.join("\n")); f.close();
})();
