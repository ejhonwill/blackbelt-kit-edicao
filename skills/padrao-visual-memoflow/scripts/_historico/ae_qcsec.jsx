(function(){
 try{
  var p=app.project; function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var A=comp("DR 05 MECANISMO");
  var TA=[2.20,5.40,10.30,14.60,16.60,22.00,26.90,29.10,32.60,35.50,45.20,50.60];
  for(var i=0;i<TA.length;i++) A.saveFrameToPng(TA[i], new File("/tmp/qm_"+(100+i)+".png"));
  var B=comp("DR 07 OFERTA");
  var TB=[3.00,9.20,18.50,24.10,29.60,34.00,40.80,47.60,58.20,70.50,89.60,106.20];
  for(var j=0;j<TB.length;j++) B.saveFrameToPng(TB[j], new File("/tmp/qo_"+(100+j)+".png"));
  var f=new File("/tmp/ae_qcsec.txt"); f.open("w"); f.write("ok "+(TA.length+TB.length)); f.close();
 }catch(e){ var fe=new File("/tmp/ae_qcsec.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
