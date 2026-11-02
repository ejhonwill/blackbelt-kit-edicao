(function(){
 try{
  var p=app.project; function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var C=comp("DR 01 ABERTURA");
  var T=[4.08,4.22,4.34,4.48,4.64,4.84,5.40,6.20,6.62,6.86,7.12,7.44];
  for(var i=0;i<T.length;i++) C.saveFrameToPng(T[i], new File("/tmp/tk_"+(100+i)+".png"));
  var f=new File("/tmp/ae_qtk.txt"); f.open("w"); f.write("ok "+T.length); f.close();
 }catch(e){ var fe=new File("/tmp/ae_qtk.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
