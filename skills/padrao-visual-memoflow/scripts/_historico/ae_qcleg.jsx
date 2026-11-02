(function(){
 try{
  var p=app.project; function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var D=[["DR 01 ABERTURA",2.30],["DR 01 ABERTURA",8.20],["DEP 02 MARK",6.0],["DEP 03 ELAINE",7.0],
         ["DR 05 MECANISMO",5.0],["DEP 06 MARGARET",8.0],["DR 07 OFERTA",12.0],["DEP 09 NANCY",14.0]];
  for(var i=0;i<D.length;i++){
    var C=comp(D[i][0]); if(!C) continue;
    C.saveFrameToPng(D[i][1], new File("/tmp/lg_"+(100+i)+".png"));
  }
  var f=new File("/tmp/ae_qcleg.txt"); f.open("w"); f.write("ok "+D.length); f.close();
 }catch(e){ var fe=new File("/tmp/ae_qcleg.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();
