(function(){
 try{
  var p=app.project; function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var C=comp("DR 01 ABERTURA");
  var T=[4.60,4.90,5.40,5.80];         // entrada, pouso, leitura, antes do recuo
  for(var i=0;i<T.length;i++) C.saveFrameToPng(T[i], new File("/tmp/ar_"+(100+i)+".png"));
  C.saveFrameToPng(30.20, new File("/tmp/ar_110.png"));   // beat de produto 1
  C.saveFrameToPng(52.40, new File("/tmp/ar_111.png"));   // beat de produto 2
  var f=new File("/tmp/ae_arco.txt"); f.open("w"); f.write("ok"); f.close();
 }catch(e){ var fe=new File("/tmp/ae_arco.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
