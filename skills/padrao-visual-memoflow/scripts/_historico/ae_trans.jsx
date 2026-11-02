(function(){
  var p=app.project; var C=null;
  for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof CompItem && x.name==="DR 01 ABERTURA") C=x; }
  if(!C) return;
  // 3 transicoes, 5 quadros cada, cobrindo o chicote
  var base=[21.19, 26.26, 29.40];
  var n=0;
  for(var b=0;b<base.length;b++){
    for(var k=-3;k<=2;k++){
      var t=base[b]+k*0.04;
      if(t<0) continue;
      try{ C.saveFrameToPng(t, new File("/tmp/tr_"+b+"_"+(k+3)+".png")); n++; }catch(e){}
    }
  }
  var f=new File("/tmp/ae_tr.txt"); f.open("w"); f.write("quadros="+n); f.close();
})();
