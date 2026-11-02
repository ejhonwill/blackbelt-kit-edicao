(function(){
  var p=app.project; var C=null;
  for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof CompItem && x.name==="DR 01 ABERTURA") C=x; }
  var base=[19.50, 21.19, 22.48];   // tres cortes seguidos: cima, baixo, direita
  var n=0;
  for(var b=0;b<base.length;b++){
    for(var k=0;k<6;k++){
      var t=base[b]-0.20+k*0.04;
      try{ C.saveFrameToPng(t, new File("/tmp/w_"+b+"_"+k+".png")); n++; }catch(e){}
    }
  }
  var f=new File("/tmp/ae_w.txt"); f.open("w"); f.write("n="+n); f.close();
})();
