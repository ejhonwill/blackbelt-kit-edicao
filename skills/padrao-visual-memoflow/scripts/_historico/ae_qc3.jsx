(function(){
 try{
  var p=app.project; function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var C=comp("DR 01 ABERTURA");
  var T=[18.20,20.60,27.00,34.40,42.10,56.60,60.00,67.50,24.00,30.60,50.00,72.00];
  for(var i=0;i<T.length;i++) C.saveFrameToPng(T[i], new File("/tmp/q3_"+(100+i)+".png"));
  var f=new File("/tmp/ae_q3.txt"); f.open("w"); f.write("ok "+T.length); f.close();
 }catch(e){ var fe=new File("/tmp/ae_q3.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
