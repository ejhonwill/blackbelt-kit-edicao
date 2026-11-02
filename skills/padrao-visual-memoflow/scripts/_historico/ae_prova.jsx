(function(){
 try{
  var p=app.project; function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var C=comp("DR 01 ABERTURA");
  var T=[19.46,19.54,24.33,24.41,29.26,29.34,33.56,33.64,39.46,39.54,44.16,44.24,
         48.54,48.62,53.21,53.29,57.18,57.26,62.58,62.66,68.49,68.57,73.80,73.88];
  for(var i=0;i<T.length;i++) C.saveFrameToPng(T[i], new File("/tmp/pv_"+(100+i)+".png"));
  var f=new File("/tmp/ae_pv.txt"); f.open("w"); f.write("quadros="+T.length); f.close();
 }catch(e){ var fe=new File("/tmp/ae_pv.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
