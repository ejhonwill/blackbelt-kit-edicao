(function(){
 try{
  var p=app.project; function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var M=comp("UPSELL #1 - DR (MASTER)");
  var T=[20.0,85.0,108.0,130.0,158.0,205.0,232.0,340.0,368.0,400.0];
  for(var i=0;i<T.length;i++) M.saveFrameToPng(T[i], new File("/tmp/ms_"+(100+i)+".png"));
  var f=new File("/tmp/ae_qcm.txt"); f.open("w"); f.write("ok "+T.length); f.close();
 }catch(e){ var fe=new File("/tmp/ae_qcm.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
