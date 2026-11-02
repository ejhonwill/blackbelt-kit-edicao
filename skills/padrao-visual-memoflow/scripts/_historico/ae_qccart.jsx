(function(){
 try{
  var p=app.project; function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var cc=comp("CARD T01");
  var T=[0.15,0.45,0.75,1.05,1.45,1.95];
  for(var i=0;i<T.length;i++) cc.saveFrameToPng(T[i], new File("/tmp/cq_"+(10+i)+".png"));
  var C=comp("DR 01 ABERTURA");
  var M=[18.20,20.30,27.00,34.40,42.10,68.00];
  for(var j=0;j<M.length;j++) C.saveFrameToPng(M[j], new File("/tmp/cm_"+(10+j)+".png"));
  var f=new File("/tmp/ae_qcc2.txt"); f.open("w"); f.write("ok"); f.close();
 }catch(e){ var fe=new File("/tmp/ae_qcc2.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
