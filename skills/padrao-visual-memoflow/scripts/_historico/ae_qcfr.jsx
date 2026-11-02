(function(){
 try{
  var p=app.project; function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var A=comp("DR 05 MECANISMO"); A.saveFrameToPng(9.90, new File("/tmp/fr_mec_B06.png"));
  var B=comp("DR 07 OFERTA");
  B.saveFrameToPng(6.30, new File("/tmp/fr_ofe_B01.png"));
  B.saveFrameToPng(7.90, new File("/tmp/fr_ofe_B02.png"));
  B.saveFrameToPng(80.70, new File("/tmp/fr_ofe_B22.png"));
  var f=new File("/tmp/ae_qcfr.txt"); f.open("w"); f.write("ok 4"); f.close();
 }catch(e){ var fe=new File("/tmp/ae_qcfr.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
