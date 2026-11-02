(function(){
 try{
  var p=app.project; function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var C=comp("DR 01 ABERTURA"); C.saveFrameToPng(5.20, new File("/tmp/fq_take.png"));
  var B=comp("MEMOFLOW_BOTTLE_CUTOUT"); if(B) B.saveFrameToPng(1.0, new File("/tmp/fq_cutout.png"));
  var f=new File("/tmp/ae_qfr.txt"); f.open("w"); f.write("ok"); f.close();
 }catch(e){ var fe=new File("/tmp/ae_qfr.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
