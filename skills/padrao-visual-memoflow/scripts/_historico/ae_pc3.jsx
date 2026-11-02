(function(){
  var p=app.project; var alvo=["CARD T01","CARD T02","CARD T05","CARD T08","CARD T10","CARD T11"]; var out=[];
  for(var a=0;a<alvo.length;a++){ var c=null;
    for(var i=1;i<=p.numItems;i++){ var it=p.item(i); if(it instanceof CompItem && it.name===alvo[a]) c=it; }
    if(c){ c.saveFrameToPng(c.duration*0.8,new File("/tmp/c3_"+a+".png")); out.push(alvo[a]); } }
  var f=new File("/tmp/ae_pc3.txt"); f.open("w"); f.write(out.join(" ")); f.close();
})();
