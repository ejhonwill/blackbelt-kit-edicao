(function(){
  var p=app.project; var out=[];
  var alvo=["CARD T01","CARD T02","CARD T05","CARD T08","CARD T10","CARD T11"];
  for(var a=0;a<alvo.length;a++){
    var c=null;
    for(var i=1;i<=p.numItems;i++){ var it=p.item(i); if(it instanceof CompItem && it.name===alvo[a]) c=it; }
    if(!c){ out.push("sem "+alvo[a]); continue; }
    c.saveFrameToPng(c.duration*0.75, new File("/tmp/c2_"+a+".png")); out.push(alvo[a]+" ok");
  }
  var f=new File("/tmp/ae_pc2.txt"); f.open("w"); f.write(out.join("\n")); f.close();
})();
