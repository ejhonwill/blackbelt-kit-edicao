(function(){
  var p=app.project; var out=[];
  var alvo=["CARD T02","CARD T06","CARD T10","CARD T11"];
  for(var a=0;a<alvo.length;a++){
    var c=null;
    for(var i=1;i<=p.numItems;i++){ var it=p.item(i); if(it instanceof CompItem && it.name===alvo[a]) c=it; }
    if(!c){ out.push("sem "+alvo[a]); continue; }
    try{ c.saveFrameToPng(c.duration*0.7, new File("/tmp/card_"+a+".png")); out.push(alvo[a]+" ok dur="+c.duration.toFixed(2)); }
    catch(e){ out.push(alvo[a]+" FALHOU "+e.toString()); }
  }
  var f=new File("/tmp/ae_prova_cards.txt"); f.open("w"); f.write(out.join("\n")); f.close();
})();
