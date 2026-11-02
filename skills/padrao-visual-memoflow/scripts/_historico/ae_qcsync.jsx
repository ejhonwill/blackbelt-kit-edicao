(function(){
 try{
  var p=app.project; function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var C=comp("DR 01 ABERTURA");
  var T=[0.40,0.90,1.90,2.60,3.30,3.75,4.40,4.90,5.25,5.70,6.30,6.85];
  for(var i=0;i<T.length;i++) C.saveFrameToPng(T[i], new File("/tmp/sy_"+(100+i)+".png"));
  var f=new File("/tmp/ae_qsy.txt"); f.open("w"); f.write("ok "+T.length); f.close();
 }catch(e){ var fe=new File("/tmp/ae_qsy.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
