(function(){
 try{
  var p=app.project; function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var A=comp("DR 01 ABERTURA"), M=comp("DR 05 MECANISMO"), O=comp("DR 07 OFERTA"), N=comp("DEP 09 NANCY");
  var T=[[A,5.40],[A,16.30],[A,19.30],[A,32.20],[A,38.70],[M,14.10],[M,23.80],[M,43.30],[O,7.90],[O,28.40],[O,56.40],[N,6.0]];
  for(var i=0;i<T.length;i++){ if(T[i][0]) T[i][0].saveFrameToPng(T[i][1], new File("/tmp/q4_"+(100+i)+".png")); }
  var f=new File("/tmp/ae_q4.txt"); f.open("w"); f.write("ok "+T.length); f.close();
 }catch(e){ var fe=new File("/tmp/ae_q4.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
